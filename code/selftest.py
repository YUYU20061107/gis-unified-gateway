# -*- coding: utf-8 -*-
"""
selftest.py — 网关 v0.3 离线协议自检（证据等级：离线协议自检，不是实机校准）。

A 段：注册表/生成物完整性——直读 build_mapping.py 的产物对账（GP 1833
      与 803/878/152、Processing 374 与 82/242/50、白名单 243/通道 239、
      模板占位符纪律、mock 面覆盖）。
B 段：进程内分发单测——stub 客户端截获网关发出的原生调用，断言 40 个
      动词逐个的 happy path 与拒绝路径（NOT_SUPPORTED / UNVERIFIED /
      DEFER_BLOCKED / DESTRUCTIVE_BLOCKED / GP_NOT_WHITELISTED /
      CONFIRM_REQUIRED / R3 三件套 / LICENSE_BLOCKED / 模板参数化）。
C 段：端到端——真起 gateway.py 子进程，后端全部指向 mock_server.py /
      mock_catalog.py 走完整 stdio MCP 协议；末段另起网关接真实
      data-catalog 对账 discover 计数（只读登记元数据）。

结果写 selftest-results.txt；任一断言失败退出码非 0。
"""
import importlib.util
import json
import os
import queue
import subprocess
import sys
import tempfile
import threading

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []
TMP = tempfile.mkdtemp(prefix="gis-gateway-v02-selftest-")


def check(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    print("%s %s%s" % ("PASS" if cond else "FAIL", name,
                       (" :: " + str(detail)) if (detail and not cond) else ""))


def load_json(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


# ---------------- A 段：注册表完整性 ----------------

gp_reg = load_json("gp_registry.json")
proc_reg = load_json("processing_registry.json")
verbs_doc = load_json("verbs.json")
tpl_doc = load_json("postgis_templates.json")
mock_tools = load_json("mock_tools.json")
with open(os.path.join(HERE, "..", "leaves-full.json"),
          encoding="utf-8") as f:
    leaves_ledger = json.load(f)

check("A1 GP 注册表计数 1833 / core803 / ext878 / defer152",
      gp_reg["counts"] == {"core": 803, "extension": 878, "defer": 152,
                           "total": 1833}, gp_reg["counts"])
check("A2 GP 白名单第一批 243、通道可调 239（扣破坏类）、破坏类 28",
      len(gp_reg["whitelist_batch1"]) == 243
      and len(gp_reg["channel_whitelist"]) == 239
      and len(gp_reg["destructive_blocklist"]) == 28,
      (len(gp_reg["whitelist_batch1"]), len(gp_reg["channel_whitelist"]),
       len(gp_reg["destructive_blocklist"])))
check("A3 通道白名单与 defer/破坏名单不交叠",
      not (set(gp_reg["channel_whitelist"])
           & set(gp_reg["defer_blocklist"]))
      and not (set(gp_reg["channel_whitelist"])
               & set(gp_reg["destructive_blocklist"])))
check("A4 Processing 种子账 374 / 82/242/50、硬拦截 51、全 seed",
      proc_reg["counts"] == {"core": 82, "extension": 242, "defer": 50,
                             "total": 374}
      and len(proc_reg["hard_blocklist"]) == 51
      and all(e["status"] == "seed" for e in proc_reg["entries"]),
      proc_reg["counts"])
check("A5 verbs.json 恰 40 动词且每动词至少一个后端映射",
      len(verbs_doc["verbs"]) == 40
      and all(v["backends"] for v in verbs_doc["verbs"].values()))
tpls = {t["template_id"]: t for t in tpl_doc["templates"]}
_slot_names = set()
import re as _re
for t in tpl_doc["templates"]:
    for m in _re.finditer(r"\{(?:ident|idents|enum|expr|fragment):([\w]+)\}"
                          r"|\%\(([\w]+)\)s", t["sql"]):
        _slot_names.add((t["template_id"], m.group(1) or m.group(2)))
check("A6 模板集 36 个；全部 SQL 槽名都在参数表内（无野槽）",
      len(tpls) == 36
      and all(name in tpls[tid]["params"] for tid, name in _slot_names),
      [x for x in _slot_names if x[1] not in tpls[x[0]]["params"]])
check("A7 mock 面覆盖通道/模板执行器与预检探针",
      "arcgis_run_gp" in mock_tools["arcgis-pro"]
      and "postgis_exec_template" in mock_tools["postgis"]
      and "postgis_table_summary" in mock_tools["postgis"]
      and "qgis_run_processing" in mock_tools["qgis"]
      and "geoserver_publish_layer" in mock_tools["geoserver"]
      and "istsos_query_entities" in mock_tools["istsos"]
      and "gdal_reproject" in mock_tools["gdal"]
      and "gdal_clip" in mock_tools["gdal"]
      and "qgis_run_processing" in mock_tools["qgis-cli"]
      and "iserver_list_services" in mock_tools["iserver"]
      and "iserver_list_datasets" in mock_tools["iserver"])

_spec_bm = importlib.util.spec_from_file_location(
    "build_mapping", os.path.join(HERE, "build_mapping.py"))
_bm = importlib.util.module_from_spec(_spec_bm)
_spec_bm.loader.exec_module(_bm)
_bm_tpls = {t["template_id"]: t for t in _bm.TEMPLATES}
check("A8 生成器 TEMPLATES 与在册模板集 36/36 一致（防漂移）",
      _bm_tpls == tpls,
      [k for k in tpls if _bm_tpls.get(k) != tpls[k]])


def _v32_status(mapping):
    if isinstance(mapping, dict) and "check" in mapping:
        return {mapping["check"].get("status"),
                mapping["repair"].get("status")}
    return {mapping.get("status")}


_v32_verbs = verbs_doc["verbs"]["gis_validate_geometry"]["backends"]
_v32_leaves = {r["backend"]: r["status"] for r in leaves_ledger
               if r["vid"] == "V32"}
check("A9 V32 三处状态统一：postgis ok / qgis+arcgis-pro unverified / "
      "supermap not_supported（verbs 与 leaves 一致）",
      _v32_status(_v32_verbs["postgis"]) == {"ok"}
      and _v32_status(_v32_verbs["qgis"]) == {"unverified"}
      and _v32_status(_v32_verbs["arcgis-pro"]) == {"unverified"}
      and _v32_status(_v32_verbs["supermap"]) == {"not_supported"}
      and _v32_leaves == {"postgis": "ok", "qgis": "unverified",
                          "arcgis-pro": "unverified",
                          "supermap": "not_supported"},
      (_v32_verbs, _v32_leaves))

_tier_counts = {t: sum(1 for r in leaves_ledger if r.get("tier") == t)
                for t in ("core", "extended", "exclusive")}
_exclusive = {(r["vid"], r["backend"]) for r in leaves_ledger
              if r.get("tier") == "exclusive"}
check("A10 tier exclusive 裁决：V01/V02 通道 4 叶；"
      "core174/ext30/excl4",
      _exclusive == {("V01", "arcgis-pro"), ("V01", "arcmap"),
                     ("V02", "qgis"), ("V02", "qgis-cli")}
      and _tier_counts == {"core": 174, "extended": 30, "exclusive": 4},
      (_tier_counts, sorted(_exclusive)))

# ---------------- B 段：进程内分发单测 ----------------

spec = importlib.util.spec_from_file_location(
    "gateway", os.path.join(HERE, "gateway.py"))
gw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gw)


def _cat_rec(did, cu):
    return {"id": did,
            "license": {"name": "Mock License", "commercial_use": cu,
                        "evidence_ref": "mock://evidence/%s" % did},
            "storage": {"uri": "mock://data/%s" % did},
            "status": "registered"}


CATALOG_RECORDS = {"mock-dem": _cat_rec("mock-dem", True),
                   "mock-restricted": _cat_rec("mock-restricted", False),
                   "mock-unknown-license": _cat_rec("mock-unknown-license",
                                                    "unknown")}


class Stub:
    def __init__(self, backend):
        self.backend = backend
        self.calls = []

    def call_tool(self, name, args):
        self.calls.append((name, args))
        if name == "gis_catalog_describe":
            rec = CATALOG_RECORDS.get(args.get("id"))
            if rec is None:
                raise gw.NativeCallError(
                    {"ok": False, "error_code": "DATASET_NOT_FOUND",
                     "message": "no such dataset"})
            return rec
        if name == "gis_catalog_list":
            return {"catalog": "mock catalog",
                    "counts": {"total": 3, "by_type": {}, "by_license": {},
                               "by_commercial_use": {}},
                    "index_updated_at": "2026-11-02T00:00:00Z"}
        if name == "arcmap_list_dataframes":
            return [{"name": "F1"}]
        if name.endswith("list_maps"):
            return [{"name": "M1"}]
        if name.endswith("list_datasets"):
            return [{"name": "roads_ds", "datasource": "ds1"}]
        if name == "postgis_table_columns":
            return {"table": args.get("table"),
                    "columns": [{"name": "id"}, {"name": "geom"}]}
        if name == "postgis_table_summary":
            return {"table": args.get("table"), "row_count": 42}
        if name == "postgis_exec_template":
            return {"applied_template": args.get("template_id"),
                    "sql": args.get("sql"), "params": args.get("params")}
        if name == "arcgis_run_gp":
            return {"executed_tool": args.get("tool")}
        if name == "qgis_run_processing":
            return {"ran_algorithm": args.get("algorithm")}
        return {"stub_tool": name, "args": args}


STUBS = {b: Stub(b) for b in gw.BACKENDS}
gw.get_client = lambda backend: STUBS[backend]  # noqa: E731


def D(tool, args):
    return gw.dispatch(tool, args)


def EC(p):
    return p.get("error_code")


def called(backend, tool=None):
    cs = STUBS[backend].calls
    if tool is None:
        return cs
    return [c for c in cs if c[0] == tool]


def clear():
    for s in STUBS.values():
        s.calls.clear()


# ---- 基础动词回归 + 新后端 ----
clear()
p = D("gis_zoom_to_layer", {"backend": "supermap",
                            "target": {"type": "layer", "id": "roads"}})
check("B01 supermap zoom 按图层 -> NOT_SUPPORTED 且未发原生调用",
      EC(p) == "NOT_SUPPORTED" and called("supermap") == [], p)
clear()
D("gis_zoom_to_layer", {"backend": "supermap", "datasource": "ds1",
                        "target": {"type": "dataset", "id": "roads"}})
check("B02 supermap zoom 按数据集翻译",
      called("supermap") == [("supermap_zoom_to_dataset",
                              {"dataset": "roads", "datasource": "ds1"})],
      called("supermap"))
clear()
D("gis_list_layers", {"backend": "arcmap", "map": "Main"})
check("B03 arcmap list_layers: map->dataframe",
      called("arcmap") == [("arcmap_list_layers", {"dataframe": "Main"})],
      called("arcmap"))
clear()
p = D("gis_list_datasets", {"backend": "postgis"})
check("B04 postgis list_datasets -> 空间表 + source_kind=server_database",
      p.get("source_kind") == "server_database"
      and called("postgis", "postgis_list_spatial_tables"), p)
clear()
D("gis_list_layers", {"backend": "geoserver", "workspace": "ws1"})
check("B05 geoserver list_layers: workspace 透传",
      called("geoserver") == [("geoserver_list_layers",
                               {"workspace": "ws1"})], called("geoserver"))
p = D("gis_ping", {"backend": "catalog"})
check("B06 catalog gis_ping -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)
p = D("gis_discover", {"backend": "arcgis-pro"})
gov = p.get("gp_governance", {})
check("B07 discover@arcgis-pro 带 gp_governance（243/239/152+三字段）",
      gov.get("whitelist_batch1") == 243
      and gov.get("channel_whitelist") == 239
      and gov.get("defer_blocked") == 152
      and gov.get("fields") == ["license_level", "requires_extension",
                                "deprecated"]
      and "gis_run_gp" in p.get("v02_verbs", {}).get("supported", []), gov)
p = D("gis_discover", {"backend": "qgis"})
check("B08 discover@qgis 带 processing_registry（374 seed）",
      p.get("processing_registry", {}).get("total") == 374
      and p.get("processing_registry", {}).get("status") == "seed", p)
p = D("gis_discover", {"backend": "postgis"})
check("B09 discover@postgis 带 postgis_templates（36）",
      p.get("postgis_templates", {}).get("count") == 36, p)

# ---- V01 GP 通道 ----
clear()
p = D("gis_run_gp", {"backend": "arcgis-pro",
                     "tool": "arcpy.management.CreateFeatureClass",
                     "args": {}})
check("B10 V01 白名单内工具直调放行",
      called("arcgis-pro", "arcgis_run_gp")
      and p.get("executed_tool") == "arcpy.management.CreateFeatureClass", p)
p = D("gis_run_gp", {"backend": "arcgis-pro", "tool": "arcpy.sa.Slope"})
check("B11 V01 SA core 未开批次 -> GP_NOT_WHITELISTED",
      EC(p) == "GP_NOT_WHITELISTED", p)
p = D("gis_run_gp", {"backend": "arcgis-pro", "tool": "arcpy.analysis.Enrich"})
check("B12 V01 defer 工具 -> DEFER_BLOCKED", EC(p) == "DEFER_BLOCKED", p)
p = D("gis_run_gp", {"backend": "arcgis-pro",
                     "tool": "arcpy.management.DeleteField"})
check("B13 V01 破坏类 -> DESTRUCTIVE_BLOCKED（优先于 defer）",
      EC(p) == "DESTRUCTIVE_BLOCKED", p)
p = D("gis_run_gp", {"backend": "arcgis-pro",
                     "tool": "arcpy.management.Append", "args": {}})
check("B14 V01 R2 级工具无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)
clear()
p = D("gis_run_gp", {"backend": "arcgis-pro",
                     "tool": "arcpy.management.Append", "args": {},
                     "confirm": True})
check("B15 V01 R2 级工具带 confirm 放行",
      called("arcgis-pro", "arcgis_run_gp"), p)
p = D("gis_run_gp", {"backend": "arcmap",
                     "tool": "arcpy.management.CreateFeatureClass"})
check("B16 V01 arcmap 冻结 -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)
p = D("gis_run_gp", {"backend": "arcgis-pro", "tool": "Buffer"})
check("B17 V01 tool 格式不合 -> INVALID_ARGUMENT",
      EC(p) == "INVALID_ARGUMENT", p)

# ---- V02 Processing 通道 ----
clear()
p = D("gis_run_processing", {"backend": "qgis", "algorithm": "native:buffer",
                             "params": {}, "confirm": True})
check("B18 V02 已登记 core 算法放行（回包带 seed 状态）",
      called("qgis", "qgis_run_processing")
      and p.get("registry_status") == "seed", p)
p = D("gis_run_processing", {"backend": "qgis", "algorithm": "qgis:executesql",
                             "confirm": True})
check("B19 V02 executesql -> DEFER_BLOCKED", EC(p) == "DEFER_BLOCKED", p)
p = D("gis_run_processing", {"backend": "qgis",
                             "algorithm": "native:printlayouttopdf",
                             "confirm": True})
check("B20 V02 批量图集类 defer -> DEFER_BLOCKED",
      EC(p) == "DEFER_BLOCKED", p)
p = D("gis_run_processing", {"backend": "qgis",
                             "algorithm": "bogus:doesnotexist",
                             "confirm": True})
check("B21 V02 未建账算法 -> ALGORITHM_NOT_REGISTERED",
      EC(p) == "ALGORITHM_NOT_REGISTERED", p)
p = D("gis_run_processing", {"backend": "qgis", "algorithm": "native:buffer"})
check("B22 V02 无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)

# ---- V03/V04 注册表 ----
p = D("gis_list_algorithms", {"backend": "qgis"})
check("B23 V03 qgis 注册表枚举 374 条全 seed",
      p.get("total") == 374
      and all(e["status"] == "seed" for e in p.get("entries", [])), p)
p = D("gis_list_algorithms", {"backend": "supermap"})
check("B24 V03 supermap 文件登记表（非运行时枚举）",
      p.get("registry") == "supermap_file_registry"
      and p.get("total") == len(gw.VERBS_DOC["supermap_registry"]["entries"])
      and p.get("total") > 0, p)
p = D("gis_list_algorithms", {"backend": "catalog"})
check("B25 V03 catalog -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)
p = D("gis_describe_algorithm", {"backend": "qgis",
                                 "algorithm": "native:buffer"})
check("B26 V04 qgis 自描述：种子条目 + 参数模式如实标 pending",
      p.get("algorithm_id") == "native:buffer"
      and p.get("params_schema") is None
      and "params_schema_note" in p, p)
p = D("gis_describe_algorithm", {"backend": "arcgis-pro",
                                 "algorithm": "arcpy.sa.Slope"})
check("B27 V04 GP 自描述带判断与许可三字段位",
      p.get("judgment") == "core" and "license_level" in p, p)
p = D("gis_describe_algorithm", {"backend": "postgis",
                                 "algorithm": "buffer_create"})
check("B28 V04 postgis 模板自描述", p.get("template_id") == "buffer_create",
      p)

# ---- V05–V13 造改组 ----
clear()
p = D("gis_create_dataset", {"backend": "arcgis-pro", "name": "fc1",
                             "kind": "vector", "confirm": True})
check("B29 V05 Pro 建要素类 -> GP CreateFeatureClass",
      called("arcgis-pro", "arcgis_run_gp")
      and called("arcgis-pro", "arcgis_run_gp")[-1][1]["tool"]
      == "arcpy.management.CreateFeatureClass", p)
p = D("gis_create_dataset", {"backend": "arcgis-pro", "name": "t1",
                             "kind": "table", "confirm": True})
check("B30 V05 Pro 建表（CreateTable 待导入核对）-> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)
p = D("gis_create_dataset", {"backend": "qgis", "name": "l1",
                             "kind": "vector", "confirm": True})
check("B31 V05 qgis 建层未核实 -> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)
clear()
p = D("gis_create_dataset", {"backend": "postgis", "name": "newtab",
                             "kind": "vector", "geometry_type": "Polygon",
                             "srid": 3857, "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B32 V05 postgis 建表模板：几何类型枚举拼入、SRID 绑定",
      tpl_call and tpl_call[-1][1]["sql"] ==
      "CREATE TABLE newtab (id serial PRIMARY KEY, "
      "geom geometry(Polygon, %(srid)s))"
      and tpl_call[-1][1]["params"] == {"srid": 3857}, tpl_call)
clear()
p = D("gis_add_field", {"backend": "qgis", "dataset": "roads",
                        "field": {"name": "f1", "type": "text"},
                        "confirm": True})
check("B33 V06 qgis 加字段 -> native:addfieldtoattributestable + in_place",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "native:addfieldtoattributestable"
      and p.get("in_place") is True, p)
p = D("gis_add_field", {"backend": "qgis", "dataset": "roads",
                        "field": {"name": "f1", "type": "text"}})
check("B34 V06 R2 无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)
p = D("gis_add_field", {"backend": "supermap", "dataset": "roads",
                        "field": {"name": "f1", "type": "text"},
                        "confirm": True})
check("B35 V06 supermap 字段接口待验 -> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)

# V07 R3 三件套（postgis）
args7 = {"backend": "postgis", "dataset": "roads", "fields": ["name"]}
p = D("gis_delete_field", dict(args7))
check("B36 V07 R3 无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)
p = D("gis_delete_field", dict(args7, confirm=True,
                               target_echo="roads.wrong"))
check("B37 V07 R3 回显不符 -> TARGET_ECHO_MISMATCH（带期望值）",
      EC(p) == "TARGET_ECHO_MISMATCH"
      and p.get("expected_target") == "roads.name", p)
clear()
p = D("gis_delete_field", dict(args7, confirm=True,
                               target_echo="roads.name"))
check("B38 V07 R3 首次 -> PREFLIGHT_REQUIRED 且探针已跑",
      EC(p) == "PREFLIGHT_REQUIRED"
      and called("postgis", "postgis_table_columns")
      and "columns" in p.get("preflight", {}).get("snapshot", {}), p)
pfid = p.get("preflight", {}).get("preflight_id")
check("B38b 预检回执 id 已发", bool(pfid), p)
clear()
p = D("gis_delete_field", dict(args7, confirm=True,
                               target_echo="roads.name",
                               preflight_id=pfid))
tpl_call = called("postgis", "postgis_exec_template")
check("B39 V07 R3 二次确认放行 -> drop_column 模板执行",
      tpl_call and tpl_call[-1][1]["sql"]
      == "ALTER TABLE roads DROP COLUMN name", tpl_call)
p = D("gis_delete_field", {"backend": "supermap", "dataset": "roads",
                           "fields": ["name"], "confirm": True,
                           "target_echo": "roads.name"})
check("B40 V07 supermap 待验（状态检查先于 R3 闸）-> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)

clear()
p = D("gis_calculate_field", {"backend": "postgis", "dataset": "roads",
                              "field": "len2",
                              "expression": "ST_Length(geom)",
                              "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B41 V08 postgis 字段计算模板",
      tpl_call and tpl_call[-1][1]["sql"]
      == "UPDATE roads SET len2 = ST_Length(geom)", tpl_call)
p = D("gis_calculate_field", {"backend": "postgis", "dataset": "roads",
                              "field": "x",
                              "expression": "1; DROP TABLE roads",
                              "confirm": True})
check("B42 V08 表达式含分号/DDL -> INVALID_ARGUMENT",
      EC(p) == "INVALID_ARGUMENT", p)
clear()
p = D("gis_calculate_field", {"backend": "arcgis-pro", "dataset": "roads",
                              "field": "x", "expression": "1",
                              "confirm": True})
check("B43 V08 Pro -> GP CalculateField + in_place",
      called("arcgis-pro", "arcgis_run_gp") and p.get("in_place") is True,
      p)
clear()
p = D("gis_copy_dataset", {"backend": "supermap", "source": "a",
                           "target": "b", "confirm": True})
check("B44 V09 supermap 复制 -> 桥侧 pending 工具被调",
      called("supermap", "supermap_copy_dataset")
      and p.get("bridge_tool_status") == "pending", p)
clear()
p = D("gis_copy_dataset", {"backend": "qgis", "source": "a", "target": "b",
                           "confirm": True})
check("B45 V09 qgis 近似映射带注记",
      called("qgis", "qgis_run_processing")
      and "近似" in (p.get("mapping_note") or ""), p)
p = D("gis_rename_dataset", {"backend": "qgis", "dataset": "a",
                             "new_name": "b", "confirm": True})
check("B46 V10 qgis 改名 -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)
p = D("gis_delete_dataset", {"backend": "qgis", "dataset": "a",
                             "confirm": True, "target_echo": "a"})
check("B47 V11 qgis 删除 -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)
clear()
args11 = {"backend": "supermap", "dataset": "roads_ds", "confirm": True,
          "target_echo": "roads_ds"}
p = D("gis_delete_dataset", dict(args11))
pfid11 = p.get("preflight", {}).get("preflight_id")
check("B48 V11 supermap R3 首次 -> PREFLIGHT_REQUIRED",
      EC(p) == "PREFLIGHT_REQUIRED" and bool(pfid11), p)
clear()
p = D("gis_delete_dataset", dict(args11, preflight_id=pfid11))
check("B49 V11 supermap R3 二次确认 -> 原生删除被调",
      called("supermap", "supermap_delete_dataset"), p)
p = D("gis_merge_datasets", {"backend": "supermap", "inputs": ["a", "b"],
                             "target": "c", "confirm": True})
check("B50 V12 supermap 合并具体名待验 -> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)
clear()
p = D("gis_merge_datasets", {"backend": "arcgis-pro",
                             "inputs": ["a", "b"], "target": "c",
                             "confirm": True})
check("B51 V12 Pro 合并 -> GP Merge",
      called("arcgis-pro", "arcgis_run_gp")
      and called("arcgis-pro", "arcgis_run_gp")[-1][1]["tool"]
      == "arcpy.management.Merge", p)
p = D("gis_append_dataset", {"backend": "supermap", "source": "a",
                             "target": "b", "confirm": True})
check("B52 V13 supermap 追加 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
p = D("gis_append_dataset", {"backend": "qgis", "source": "a",
                             "target": "b", "confirm": True})
check("B53 V13 qgis 追加 -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)
clear()
p = D("gis_append_dataset", {"backend": "postgis", "source": "a",
                             "target": "b", "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B54 V13 postgis 追加模板",
      tpl_call and tpl_call[-1][1]["sql"]
      == "INSERT INTO b SELECT * FROM a", tpl_call)

# ---- V14–V17 坐标系/转换 ----
clear()
p = D("gis_assign_projection", {"backend": "qgis", "dataset": "roads",
                                "srid": 4326, "confirm": True})
check("B55 V14 qgis 定义投影 + metadata_only",
      called("qgis", "qgis_run_processing")
      and p.get("metadata_only") is True, p)
p = D("gis_assign_projection", {"backend": "supermap", "dataset": "roads",
                                "srid": 4326, "confirm": True})
check("B56 V14 supermap 接口待验 -> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)
clear()
p = D("gis_reproject", {"backend": "qgis", "input": "dem.tif",
                        "target": "dem2.tif", "target_srid": 3857,
                        "kind": "raster", "confirm": True})
check("B57 V15 qgis 栅格重投影 -> gdal:warpreproject",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "gdal:warpreproject", p)
p = D("gis_reproject", {"backend": "postgis", "input": "roads",
                        "target": "roads2", "target_srid": 3857,
                        "overwrite": True, "confirm": True,
                        "target_echo": "roads"})
check("B58 V15 overwrite 升 R3 -> PREFLIGHT_REQUIRED",
      EC(p) == "PREFLIGHT_REQUIRED", p)
clear()
p = D("gis_convert_format", {"backend": "qgis", "input": "a.shp",
                             "target": "a.gpkg", "format": "GPKG",
                             "kind": "vector", "confirm": True})
check("B59 V16 qgis 矢量转换 -> gdal:convertformat",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "gdal:convertformat", p)
p = D("gis_convert_format", {"backend": "postgis", "input": "roads",
                             "target": "x.kml", "format": "KML",
                             "confirm": True})
check("B60 V16 postgis 非 GeoJSON 格式 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
clear()
p = D("gis_convert_format", {"backend": "postgis", "input": "roads",
                             "target": "/tmp/roads.geojson",
                             "format": "GeoJSON", "confirm": True})
check("B61 V16 postgis GeoJSON -> 桥既有导出工具",
      called("postgis", "postgis_export_geojson"), p)
clear()
p = D("gis_import_data", {"backend": "supermap", "source_uri": "file:///a.shp",
                          "target_name": "a", "confirm": True})
check("B62 V17 supermap 导入 -> supermap_import_data",
      called("supermap", "supermap_import_data"), p)
p = D("gis_import_data", {"backend": "postgis", "source_uri": "file:///a.shp",
                          "target_name": "a", "kind": "vector",
                          "confirm": True})
check("B63 V17 postgis 矢量文件入库（ogr2ogr 登记）-> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
clear()
p = D("gis_import_data", {"backend": "postgis", "source_uri": "file:///x.tif",
                          "target_name": "dem", "kind": "raster",
                          "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B64 V17 postgis 栅格入库模板：路径走绑定参数不拼 SQL",
      tpl_call and "%(file_path)s" in tpl_call[-1][1]["sql"]
      and "x.tif" not in tpl_call[-1][1]["sql"]
      and tpl_call[-1][1]["params"].get("file_path") == "file:///x.tif",
      tpl_call)

# ---- V18–V22 矢量分析 ----
clear()
p = D("gis_buffer", {"backend": "arcgis-pro", "input": "roads",
                     "target": "buf", "distance": 100, "confirm": True})
check("B65 V18 Pro 缓冲 -> GP Buffer",
      called("arcgis-pro", "arcgis_run_gp")
      and called("arcgis-pro", "arcgis_run_gp")[-1][1]["tool"]
      == "arcpy.analysis.Buffer", p)
clear()
p = D("gis_buffer", {"backend": "supermap", "input": "roads",
                     "target": "buf", "distance": 100, "confirm": True})
check("B66 V18 supermap 缓冲 -> create_buffer（轮子名透传）",
      called("supermap", "supermap_create_buffer")
      and p.get("wheel") == "iobjectspy.analyst.create_buffer", p)
clear()
p = D("gis_buffer", {"backend": "postgis", "input": "roads",
                     "target": "roads_buf", "distance": 50.5,
                     "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
sql = tpl_call[-1][1]["sql"] if tpl_call else ""
check("B67 V18 postgis 缓冲模板：距离绑定不拼入 SQL",
      tpl_call and "ST_Buffer" in sql and "%(distance)s" in sql
      and "50.5" not in sql
      and tpl_call[-1][1]["params"].get("distance") == 50.5, tpl_call)
clear()
p = D("gis_clip", {"backend": "qgis", "input": "dem.tif",
                   "clip_by": "mask.shp", "target": "out.tif",
                   "input_type": "raster", "confirm": True})
check("B68 V19 qgis 栅格裁剪 -> gdal:cliprasterbymasklayer",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "gdal:cliprasterbymasklayer", p)
clear()
p = D("gis_clip", {"backend": "supermap", "input": "roads",
                   "clip_by": "county", "target": "out",
                   "input_type": "vector", "confirm": True})
check("B69 V19 supermap 矢量裁剪 -> overlay 裁剪（明列）",
      called("supermap", "supermap_overlay_clip"), p)
clear()
p = D("gis_overlay", {"backend": "postgis", "input": "a", "overlay": "b",
                      "target": "c", "operation": "intersect",
                      "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B70 V20 postgis 相交模板",
      tpl_call and tpl_call[-1][1]["template_id"]
      if False else (tpl_call and "ST_Intersection" in
                     tpl_call[-1][1]["sql"]), tpl_call)
p = D("gis_overlay", {"backend": "qgis", "input": "a", "overlay": "b",
                      "target": "c", "operation": "identity",
                      "confirm": True})
check("B71 V20 qgis identity 无同名条目 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
p = D("gis_overlay", {"backend": "supermap", "input": "a", "overlay": "b",
                      "target": "c", "operation": "intersect",
                      "confirm": True})
check("B72 V20 supermap 叠加其余式待验 -> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)
clear()
p = D("gis_overlay", {"backend": "arcgis-pro", "input": "a", "overlay": "b",
                      "target": "c", "operation": "erase", "confirm": True})
check("B73 V20 Pro erase -> GP Erase",
      called("arcgis-pro", "arcgis_run_gp")
      and called("arcgis-pro", "arcgis_run_gp")[-1][1]["tool"]
      == "arcpy.analysis.Erase", p)
clear()
p = D("gis_dissolve", {"backend": "supermap", "input": "a", "target": "b",
                       "fields": ["type"], "confirm": True})
check("B74 V21 supermap 融合 -> supermap_dissolve",
      called("supermap", "supermap_dissolve"), p)
p = D("gis_spatial_join", {"backend": "supermap", "input": "a", "join": "b",
                           "target": "c", "predicate": "intersects",
                           "confirm": True})
check("B75 V22 supermap 空间连接未验前 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
p = D("gis_spatial_join", {"backend": "postgis", "input": "a", "join": "b",
                           "target": "c", "predicate": "nearest",
                           "confirm": True})
check("B76 V22 postgis nearest 模板未备 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
clear()
p = D("gis_spatial_join", {"backend": "qgis", "input": "a", "join": "b",
                           "target": "c", "predicate": "intersects",
                           "confirm": True})
check("B77 V22 qgis 空间连接 -> joinattributesbylocation",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "native:joinattributesbylocation", p)

# ---- V23–V33 栅格/PostGIS 集 ----
clear()
p = D("gis_raster_calc", {"backend": "postgis",
                          "inputs": {"a": "dem"},
                          "expression": "[a] * 2", "target": "out",
                          "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B78 V23 postgis 栅格代数：表达式作绑定值",
      tpl_call and "%(expression)s" in tpl_call[-1][1]["sql"]
      and tpl_call[-1][1]["params"].get("expression") == "[a] * 2",
      tpl_call)
clear()
p = D("gis_slope", {"backend": "qgis", "input": "dem", "target": "s",
                    "confirm": True})
check("B79 V24 qgis 坡度 -> qgis:slope",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "qgis:slope", p)
p = D("gis_slope", {"backend": "supermap", "input": "dem", "target": "s",
                    "confirm": True})
check("B80 V24 supermap 坡度函数名待验 -> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)
clear()
p = D("gis_aspect", {"backend": "postgis", "input": "dem", "target": "a",
                     "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B81 V25 postgis 坡向模板 ST_Aspect",
      tpl_call and "ST_Aspect" in tpl_call[-1][1]["sql"], tpl_call)
clear()
p = D("gis_hillshade", {"backend": "arcgis-pro", "input": "dem",
                        "target": "h", "confirm": True})
check("B82 V26 Pro 山体阴影 -> GP Hillshade",
      called("arcgis-pro", "arcgis_run_gp")
      and called("arcgis-pro", "arcgis_run_gp")[-1][1]["tool"]
      == "arcpy.sa.Hillshade", p)
p = D("gis_reclassify", {"backend": "arcgis-pro", "input": "dem",
                         "target": "r", "rules": [[0, 1, 1]],
                         "confirm": True})
check("B83 V27 Pro Reclassify 名待核对 -> UNVERIFIED_MAPPING",
      EC(p) == "UNVERIFIED_MAPPING", p)
clear()
p = D("gis_reclassify", {"backend": "qgis", "input": "dem", "target": "r",
                         "rules": [[0, 10, 1], [10, 20, 2]],
                         "confirm": True})
check("B84 V27 qgis 重分类 -> native:reclassifybytable",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "native:reclassifybytable", p)
clear()
p = D("gis_zonal_statistics", {"backend": "postgis", "zones": "zones",
                               "values": "dem", "target": "zs",
                               "confirm": True})
check("B85 V28 postgis 分区统计 derived 组合模板带注记",
      "derived" in (p.get("mapping_note") or "")
      and called("postgis", "postgis_exec_template"), p)
clear()
p = D("gis_field_statistics", {"backend": "qgis", "dataset": "roads",
                               "fields": ["pop"]})
check("B86 V29 qgis 字段统计 R0 免 confirm 放行",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "qgis:basicstatisticsforfields", p)
p = D("gis_field_statistics", {"backend": "supermap", "dataset": "roads",
                               "fields": ["pop"]})
check("B87 V29 supermap 统计类待验 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
p = D("gis_field_statistics", {"backend": "postgis", "dataset": "roads",
                               "fields": ["pop"], "statistics": ["avg"],
                               "output": "stored", "target": "stats"})
check("B88 V29 postgis 落表升 R1 无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)
clear()
p = D("gis_field_statistics", {"backend": "postgis", "dataset": "roads",
                               "fields": ["pop"],
                               "statistics": ["avg", "sum"],
                               "output": "stored", "target": "stats",
                               "confirm": True})
tpl_call = called("postgis", "postgis_exec_template")
check("B89 V29 postgis 落表模板：统计量枚举拼列",
      tpl_call and "CREATE TABLE stats AS" in tpl_call[-1][1]["sql"]
      and "avg(pop) AS pop_avg" in tpl_call[-1][1]["sql"], tpl_call)
clear()
p = D("gis_spatial_filter", {"backend": "postgis", "table": "roads",
                             "predicate": "intersects",
                             "reference_wkt": "POINT(1 2)", "limit": 10})
tpl_call = called("postgis", "postgis_exec_template")
check("B90 V30 postgis 空间过滤：WKT 绑定不拼 SQL",
      tpl_call and "ST_Intersects" in tpl_call[-1][1]["sql"]
      and "POINT(1 2)" not in tpl_call[-1][1]["sql"]
      and tpl_call[-1][1]["params"].get("reference_wkt") == "POINT(1 2)",
      tpl_call)
p = D("gis_spatial_filter", {"backend": "postgis", "table": "roads",
                             "predicate": "intersects; DROP TABLE x",
                             "reference_wkt": "POINT(1 2)"})
check("B91 V30 谓词注入 -> INVALID_ARGUMENT",
      EC(p) == "INVALID_ARGUMENT", p)
p = D("gis_spatial_filter", {"backend": "postgis",
                             "table": "roads; DROP TABLE x",
                             "predicate": "intersects",
                             "reference_wkt": "POINT(1 2)"})
check("B92 V30 表名注入 -> INVALID_ARGUMENT",
      EC(p) == "INVALID_ARGUMENT", p)
p = D("gis_spatial_filter", {"backend": "qgis", "table": "roads",
                             "predicate": "intersects",
                             "reference_wkt": "POINT(1 2)"})
check("B93 V30 桌面后端不开 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
clear()
p = D("gis_measure", {"backend": "postgis", "operation": "distance",
                      "a_wkt": "POINT(0 0)", "b_wkt": "POINT(1 1)"})
check("B94 V31 postgis 距离量测模板",
      called("postgis", "postgis_exec_template")
      and "ST_Distance" in
      called("postgis", "postgis_exec_template")[-1][1]["sql"], p)
p = D("gis_measure", {"backend": "supermap", "operation": "distance",
                      "a_wkt": "POINT(0 0)", "b_wkt": "POINT(1 1)"})
check("B95 V31 桌面后端本波不开 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
clear()
p = D("gis_validate_geometry", {"backend": "qgis", "dataset": "roads"})
check("B96 V32 qgis 校验未实机 -> UNVERIFIED_MAPPING（阶段 1 裁决）",
      EC(p) == "UNVERIFIED_MAPPING"
      and not called("qgis", "qgis_run_processing"), p)
p = D("gis_validate_geometry", {"backend": "postgis", "dataset": "roads",
                                "repair": True})
check("B97 V32 postgis 修复升 R2 无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)
clear()
p = D("gis_validate_geometry", {"backend": "postgis", "dataset": "roads",
                                "repair": True, "confirm": True,
                                "target": "roads_fixed"})
tpl_call = called("postgis", "postgis_exec_template")
check("B98 V32 postgis 修复模板 ST_MakeValid（v0.3 输出新表形态）",
      tpl_call and "ST_MakeValid" in tpl_call[-1][1]["sql"], tpl_call)
clear()
p = D("gis_serve_vector_tile", {"backend": "postgis", "table": "roads",
                                "z": 10, "x": 1, "y": 2})
tpl_call = called("postgis", "postgis_exec_template")
check("B99 V33 postgis MVT 直出：句柄形态 + 瓦片模板",
      p.get("content_type") == "application/vnd.mapbox-vector-tile"
      and tpl_call and "ST_AsMVT" in tpl_call[-1][1]["sql"]
      and tpl_call[-1][1]["params"].get("z") == 10, p)
p = D("gis_serve_vector_tile", {"backend": "qgis", "table": "roads",
                                "z": 1, "x": 0, "y": 0})
check("B100 V33 非 postgis -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)

# ---- V34 发布（许可闸） ----
p = D("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:mock-restricted",
                            "confirm": True})
check("B101 V34 commercial_use=false -> LICENSE_BLOCKED",
      EC(p) == "LICENSE_BLOCKED", p)
p = D("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:mock-restricted"})
check("B102 V34 许可闸先于 confirm（无 confirm 仍先 LICENSE_BLOCKED）",
      EC(p) == "LICENSE_BLOCKED", p)
clear()
p = D("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:mock-dem",
                            "confirm": True})
check("B103 V34 许可合规 -> 发布执行 + 回写 pending 如实标",
      called("geoserver", "geoserver_publish_layer")
      and p.get("publication", {}).get("writeback", {}).get("status")
      == "pending_catalog_support", p)
p = D("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:mock-dem"})
check("B104 V34 许可过但无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)
clear()
p = D("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "postgis:roads",
                            "confirm": True})
check("B105 V34 postgis 表直发：许可闸跳过并注记",
      called("geoserver", "geoserver_publish_layer")
      and "skipped" in p.get("license_gate", {}), p)
p = D("gis_publish_layer", {"backend": "geoserver", "dataset_ref": "roads",
                            "confirm": True})
check("B106 V34 dataset_ref 无前缀 -> INVALID_ARGUMENT",
      EC(p) == "INVALID_ARGUMENT", p)
p = D("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:mock-unknown-license",
                            "purpose": "commercial", "confirm": True})
check("B107 V34 unknown 许可 + 商用 -> LICENSE_BLOCKED",
      EC(p) == "LICENSE_BLOCKED", p)
clear()
p = D("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:mock-unknown-license",
                            "purpose": "research", "confirm": True})
check("B108 V34 unknown 许可 + 研究用途 -> 放行（带许可节）",
      called("geoserver", "geoserver_publish_layer")
      and p.get("license_gate", {}).get("catalog_id")
      == "mock-unknown-license", p)

# ---- V35/V36 服务与观测 ----
clear()
p = D("gis_list_services", {"backend": "geoserver"})
check("B109 V35 geoserver 服务面 -> capabilities 摘要（WMS 默认）",
      called("geoserver", "geoserver_capabilities_summary")
      and called("geoserver", "geoserver_capabilities_summary")[-1][1]
      == {"service": "WMS"}, p)
p = D("gis_list_services", {"backend": "supermap"})
check("B110 V35 supermap iServer 登记 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
clear()
p = D("gis_query_observations", {"backend": "istsos", "entity": "Things",
                                 "top": 5})
check("B111 V36 Things -> 桥既有 list_things",
      called("istsos", "istsos_list_things"), p)
p = D("gis_query_observations", {"backend": "istsos",
                                 "entity": "Observations"})
check("B112 V36 Observations 无 datastream_id -> INVALID_ARGUMENT",
      EC(p) == "INVALID_ARGUMENT", p)
clear()
p = D("gis_query_observations", {"backend": "istsos",
                                 "entity": "Observations",
                                 "datastream_id": 3})
check("B113 V36 Observations 带流 id -> get_observations",
      called("istsos", "istsos_get_observations"), p)
clear()
p = D("gis_query_observations", {"backend": "istsos", "entity": "Sensors"})
check("B114 V36 Sensors -> 通用实体查询（pending 如实标）",
      called("istsos", "istsos_query_entities")
      and p.get("bridge_tool_status") == "pending", p)
p = D("gis_query_observations", {"backend": "istsos", "entity": "Bogus"})
check("B115 V36 未知实体 -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)

# ---- V37/V38 点云 ----
clear()
p = D("gis_pointcloud_info", {"backend": "qgis", "input": "x.las"})
check("B116 V37 点云信息 -> pdal:info（R0 免 confirm）",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "pdal:info", p)
clear()
p = D("gis_pointcloud_process", {"backend": "qgis", "input": "x.las",
                                 "target": "y.las", "action": "thin_radius",
                                 "confirm": True})
check("B117 V38 点云抽稀 -> pdal:thinbyradius",
      called("qgis", "qgis_run_processing")
      and called("qgis", "qgis_run_processing")[-1][1]["algorithm"]
      == "pdal:thinbyradius", p)
p = D("gis_pointcloud_process", {"backend": "qgis", "input": "x.las",
                                 "target": "y.las", "action": "bogus",
                                 "confirm": True})
check("B118 V38 未知 action -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
p = D("gis_pointcloud_process", {"backend": "arcgis-pro", "input": "x.las",
                                 "target": "y.las", "action": "clip",
                                 "confirm": True})
check("B119 V38 非 qgis 后端 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)

# ---- V39 目录链路 ----
p = D("gis_add_layer_from_catalog",
      {"backend": "qgis", "catalog_id": "mock-unknown-license",
       "purpose": "commercial", "confirm": True})
check("B120 V39 unknown 许可 + 商用 -> LICENSE_BLOCKED",
      EC(p) == "LICENSE_BLOCKED", p)
clear()
p = D("gis_add_layer_from_catalog",
      {"backend": "qgis", "catalog_id": "mock-dem", "confirm": True})
check("B121 V39 合规 -> 以 storage.uri 加图层 + 许可节透传",
      called("qgis", "qgis_add_layer_from_path")
      and called("qgis", "qgis_add_layer_from_path")[-1][1].get("path")
      == "mock://data/mock-dem"
      and p.get("license_gate", {}).get("storage_uri")
      == "mock://data/mock-dem", p)
p = D("gis_add_layer_from_catalog",
      {"backend": "arcgis-pro", "catalog_id": "mock-dem"})
check("B122 V39 无 confirm -> CONFIRM_REQUIRED",
      EC(p) == "CONFIRM_REQUIRED", p)
p = D("gis_add_layer_from_catalog",
      {"backend": "qgis", "catalog_id": "nope", "confirm": True})
check("B123 V39 目录无此 id -> DATASET_NOT_FOUND",
      EC(p) == "DATASET_NOT_FOUND", p)

# ---- V40 出图 + 工具面外 ----
clear()
p = D("gis_export_map_image", {"backend": "supermap",
                               "target_path": "/tmp/x.png"})
check("B124 V40 supermap 出图（沿用桥规则免网关 confirm）",
      called("supermap", "supermap_export_map_image"), p)
p = D("gis_export_map_image", {"backend": "supermap",
                               "target_path": "/tmp/x.pdf", "format": "pdf"})
check("B125 V40 PDF/图集类 -> NOT_SUPPORTED", EC(p) == "NOT_SUPPORTED", p)
p = D("gis_export_map_image", {"backend": "arcmap",
                               "target_path": "/tmp/x.png"})
check("B126 V40 arcmap 冻结存量 -> NOT_SUPPORTED",
      EC(p) == "NOT_SUPPORTED", p)
p = D("gis_run_sql", {"backend": "postgis", "sql": "SELECT 1"})
check("B127 工具面外 gis_run_sql -> NOT_SUPPORTED（平台不开裸 SQL）",
      EC(p) == "NOT_SUPPORTED", p)


# ---------------- C 段：端到端（子进程 + 真实 stdio MCP） ----------------


class McpClient:
    """最小 stdio MCP 客户端：逐行 JSON-RPC，只用 tools/call。"""

    def __init__(self, argv, env=None):
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8",
            errors="replace", env=env)
        self.responses = queue.Queue()
        threading.Thread(target=self._reader, daemon=True).start()
        self._id = 0

    def _reader(self):
        for line in self.proc.stdout:
            if line.strip():
                self.responses.put(json.loads(line))

    def call(self, tool, args, timeout=30):
        self._id += 1
        self.proc.stdin.write(json.dumps(
            {"jsonrpc": "2.0", "id": self._id, "method": "tools/call",
             "params": {"name": tool, "arguments": args}},
            ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        msg = self.responses.get(timeout=timeout)
        content = (msg.get("result") or {}).get("content") or []
        text = content[0].get("text", "{}") if content else "{}"
        return json.loads(text)

    def close(self):
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except Exception:  # noqa: BLE001
            self.proc.kill()


def _mock(name):
    return [sys.executable, os.path.join(HERE, "mock_server.py"),
            "--backend", name]


def write_cfg(path, catalog_cmd):
    prod = load_json("backends.json")["backends"]
    cmds = {
        "supermap": _mock("supermap"),
        "arcgis-pro": _mock("arcgis-pro"),
        "arcmap": _mock("arcmap"),
        "qgis": _mock("qgis"),
        "catalog": catalog_cmd,
        "postgis": _mock("postgis"),
        "geoserver": _mock("geoserver"),
        "istsos": _mock("istsos"),
        "gdal": _mock("gdal"),
        "qgis-cli": _mock("qgis-cli"),
        "iserver": _mock("iserver"),
    }
    # mode / calibration 沿用 backends.json 的生产声明（透传不升格），
    # 只把 command 换成 mock——自检验的正是这份声明的透传路径。
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"backends": {
            k: {"command": v, "mode": prod[k]["mode"],
                "calibration": prod[k]["calibration"]}
            for k, v in cmds.items()}}, f, ensure_ascii=False, indent=2)


BASE_ENV = dict(os.environ, PYTHONIOENCODING="utf-8")

# —— C1：全 mock 后端 ——
cfg_mock = os.path.join(TMP, "backends-mock.json")
write_cfg(cfg_mock, [sys.executable,
                     os.path.join(HERE, "mock_catalog.py")])
env_mock = dict(BASE_ENV, GIS_GATEWAY_BACKENDS=cfg_mock)
client = McpClient([sys.executable, os.path.join(HERE, "gateway.py")],
                   env=env_mock)


def E(tool, args):
    return client.call(tool, args)


p = E("gis_discover", {"backend": "arcgis-pro"})
check("C01 e2e discover@arcgis-pro：gp_governance + v02_verbs + CALIBRATION 未改样",
      p.get("gp_governance", {}).get("whitelist_batch1") == 243
      and "gis_run_gp" in p.get("v02_verbs", {}).get("supported", [])
      and p.get("calibration", {}).get("level")
      == "protocol_selfcheck_only", p)
p = E("gis_discover", {"backend": "postgis"})
check("C02 e2e discover@postgis：模板 36 + calibration=calibrated"
      "（隔离本地集群范围）",
      p.get("postgis_templates", {}).get("count") == 36
      and p.get("calibration", {}).get("level")
      == "calibrated", p)
p = E("gis_run_gp", {"backend": "arcgis-pro", "tool": "arcpy.sa.Slope"})
check("C03 e2e GP 未开批次拦截 GP_NOT_WHITELISTED",
      EC(p) == "GP_NOT_WHITELISTED", p)
p = E("gis_run_gp", {"backend": "arcgis-pro",
                     "tool": "arcpy.management.CreateFeatureClass",
                     "args": {}})
check("C04 e2e GP 白名单内直调（mock 回声 executed_tool）",
      p.get("executed_tool") == "arcpy.management.CreateFeatureClass", p)
p = E("gis_buffer", {"backend": "postgis", "input": "roads",
                     "target": "roads_buf", "distance": 100,
                     "confirm": True})
check("C05 e2e postgis 缓冲模板：template_id + sql 绑定参数回包",
      p.get("template_id") == "buffer_create"
      and "%(distance)s" in p.get("sql", "")
      and p.get("bound_params", {}).get("distance") == 100, p)
p = E("gis_run_processing", {"backend": "qgis",
                             "algorithm": "qgis:executesql",
                             "confirm": True})
check("C06 e2e Processing defer 拦截", EC(p) == "DEFER_BLOCKED", p)
p = E("gis_publish_layer", {"backend": "geoserver", "dataset_ref": "roads"})
check("C07 e2e 发布无来源前缀 -> INVALID_ARGUMENT",
      EC(p) == "INVALID_ARGUMENT", p)
p = E("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:no-such-dataset",
                            "confirm": True})
check("C08 e2e 发布指向不存在的目录条目 -> DATASET_NOT_FOUND",
      EC(p) == "DATASET_NOT_FOUND", p)
p = E("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:mock-restricted",
                            "confirm": True})
check("C09 e2e 发布受限条目（mock 目录）-> LICENSE_BLOCKED",
      EC(p) == "LICENSE_BLOCKED", p)
p = E("gis_list_algorithms", {"backend": "qgis"})
check("C10 e2e V03 qgis 枚举 374", p.get("total") == 374, p)
p = E("gis_discover", {"backend": "gdal"})
check("C11 e2e discover@gdal：本地 CLI 后端 + 6 个 v02 动词",
      p.get("backend") == "gdal"
      and {"gis_reproject", "gis_convert_format", "gis_clip",
           "gis_slope", "gis_aspect", "gis_hillshade"}
      <= set(p.get("v02_verbs", {}).get("supported", [])), p)
p = E("gis_discover", {"backend": "qgis-cli"})
check("C12 e2e discover@qgis-cli：无头 Processing + V02/V03/V04",
      p.get("backend") == "qgis-cli"
      and {"gis_run_processing", "gis_list_algorithms",
           "gis_describe_algorithm"}
      <= set(p.get("v02_verbs", {}).get("supported", [])), p)
p = E("gis_discover", {"backend": "iserver"})
check("C13 e2e discover@iserver：demo 后端 + V35 服务目录",
      p.get("backend") == "iserver"
      and "gis_list_services"
      in p.get("v02_verbs", {}).get("supported", []), p)
client.close()

# —— C2：catalog 后端换成真实 data-catalog/catalog_server.py 对账 ——
REAL_SERVER = os.path.abspath(os.path.join(
    HERE, "..", "data-catalog", "catalog_server.py"))
cfg_real = os.path.join(TMP, "backends-real.json")
write_cfg(cfg_real, [sys.executable, REAL_SERVER])
env_real = dict(BASE_ENV, GIS_GATEWAY_BACKENDS=cfg_real)
real_client = McpClient([sys.executable, os.path.join(HERE, "gateway.py")],
                        env=env_real)


def R(tool, args):
    return real_client.call(tool, args)


p = R("gis_discover", {"backend": "catalog"})
check("C14 真实目录 discover：9 条登记 + by commercial_use 透传（9 条全 True）",
      p.get("data_catalog", {}).get("total") == 9
      and p.get("data_catalog", {}).get(
          "by_commercial_use", {}).get("True") == 9, p)
p = R("gis_publish_layer", {"backend": "geoserver",
                            "dataset_ref": "catalog:aw3d30",
                            "confirm": True})
check("C15 真实目录发布链路：许可闸过（cu=true）+ 回写 pending 如实标",
      p.get("license_gate", {}).get("catalog_id") == "aw3d30"
      and p.get("publication", {}).get("writeback", {}).get("status")
      == "pending_catalog_support", p)
p = R("gis_add_layer_from_catalog", {"backend": "qgis",
                                     "catalog_id": "srtm",
                                     "confirm": True})
check("C16 真实目录 V39：以 storage.uri（USGS 页）为路径透传 + 许可节",
      p.get("license_gate", {}).get("storage_uri", "").startswith(
          "https://www.usgs.gov/")
      and p.get("license_gate", {}).get("catalog_id") == "srtm", p)
real_client.close()

with open(os.path.join(HERE, "selftest-results.txt"), "w",
          encoding="utf-8", newline="\n") as f:
    total = len(RESULTS)
    failed = [r for r in RESULTS if not r[1]]
    f.write("GIS gateway v0.3 selftest（证据等级：离线协议自检，非实机校准）\n")
    f.write("checks: %d, passed: %d, failed: %d\n\n"
            % (total, total - len(failed), len(failed)))
    for name, ok, detail in RESULTS:
        f.write("%s %s%s\n" % ("PASS" if ok else "FAIL", name,
                               (" :: " + str(detail))
                               if (detail and not ok) else ""))

total = len(RESULTS)
failed = [r for r in RESULTS if not r[1]]
print("\nchecks: %d, passed: %d, failed: %d"
      % (total, total - len(failed), len(failed)))
if failed:
    print("FAILED:", [r[0] for r in failed])
    sys.exit(1)

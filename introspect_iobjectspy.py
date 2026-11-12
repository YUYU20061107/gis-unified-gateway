# -*- coding: utf-8 -*-
"""
B1 一次性清名脚本：在鱼鱼 Windows 的 sm35 venv 里跑一次，
dump iobjectspy 各模块的成员名+签名，与 gateway-v02 的 16 个待验接口逐条比对。

用法（在 E:\\ds工作区 里）：
    E:\\ds工作区\\.venvs\\sm35\\python.exe introspect_iobjectspy.py > introspect-result.json
把 introspect-result.json 回传给 Muse 对账即可。只读自省，不调用任何业务函数、不写数据。

环境：Python 3.5.4 + iobjectspy 10.1.0.0（SuperMap 专用运行时）。写法按 3.5 兼容（无 f-string）。
"""
import json
import sys
import traceback

MODULES = [
    "iobjectspy",
    "iobjectspy.data",
    "iobjectspy.analyst",
    "iobjectspy.conversion",
    "iobjectspy.mapping",
    "iobjectspy.topology",
    "iobjectspy.networkanalyst",
    "iobjectspy.spatialanalyst",
    "iobjectspy._iobjectspy",
]

# gateway-v02 待验接口（verbs.json 的 unverified 叶，2026-11-03 抽取）
# key = 统一动词侧工具名；hints = 猜测的原生名关键词（子串匹配，不分大小写）
WANTED = {
    "supermap_add_field":        ["addfield", "add_field", "createfield", "appendfield", "fieldinfo"],
    "supermap_delete_field":     ["deletefield", "removefield", "dropfield"],
    "supermap_calculate_field":  ["update", "recordset", "setvalue", "calculate"],
    "supermap_merge_datasets":   ["append", "merge", "uniondataset", "mergedataset"],
    "supermap_assign_projection": ["prjcoordsys", "setprj", "coordsys", "projection"],
    "supermap_reproject":        ["project", "transform", "convertdataset", "coordtransform"],
    "supermap_overlay":          ["overlay", "intersect", "union", "erase", "identity", "symdifference", "update"],
    "supermap_slope":            ["slope"],
    "supermap_aspect":           ["aspect"],
    "supermap_hillshade":        ["hillshade", "shadedrelief", "relief"],
    "supermap_append_dataset":   ["append"],
    "supermap_spatial_join":     ["spatialjoin", "join", "overlay"],
    "supermap_field_statistics": ["statistics", "summarize", "basicstatistics"],
    "supermap_validate_geometry": ["topology", "validate", "checkgeometry", "topologyvalidator"],
}


def safe_dir(mod):
    try:
        return sorted(dir(mod))
    except Exception:
        return []


def main():
    out = {"python": sys.version, "modules": {}, "wanted_hits": {}}
    imported = {}
    for name in MODULES:
        try:
            mod = __import__(name, fromlist=["*"])
            imported[name] = mod
            members = safe_dir(mod)
            out["modules"][name] = {"ok": True, "members": members}
            # 一层子模块也扫（analyst/conversion 常有子模块）
            subs = {}
            for m in members:
                if m.startswith("_"):
                    continue
                try:
                    sub = getattr(mod, m)
                    if type(sub).__name__ == "module":
                        subs[m] = safe_dir(sub)
                except Exception:
                    pass
            if subs:
                out["modules"][name]["submodules"] = subs
        except Exception:
            out["modules"][name] = {"ok": False, "error": traceback.format_exc(limit=2)}

    # 汇总全部成员名（含子模块）做待验比对
    all_names = []
    for name, info in out["modules"].items():
        if not info.get("ok"):
            continue
        for m in info["members"]:
            all_names.append((name, m))
        for sub, members in info.get("submodules", {}).items():
            for m in members:
                all_names.append((name + "." + sub, m))

    for tool, hints in WANTED.items():
        hits = []
        for modname, member in all_names:
            low = member.lower()
            for h in hints:
                if h in low:
                    hits.append({"module": modname, "member": member, "hint": h})
                    break
        out["wanted_hits"][tool] = hits

    json.dump(out, sys.stdout, ensure_ascii=False, indent=1, sort_keys=True)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

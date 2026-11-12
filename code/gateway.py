# -*- coding: utf-8 -*-
"""
gateway.py — GIS 桥统一入口网关 v0.3（stdio MCP 服务端，纯标准库）

对外工具面 = 基础 8 动词（v0.1）+ 第一波 40 动词（UPGRADE-DESIGN-V02
§2 的 V01–V40），后端 8 个（supermap / arcgis-pro / arcmap / qgis /
catalog / postgis / geoserver / istsos）。网关按 mapping.json /
verbs.json 把统一调用翻译成各后端原生调用：作为 MCP 客户端以子进程
拉起后端 stdio 服务端，逐行 JSON-RPC 代理。

v0.2 的治理面（设计 §3/§4）：
  - GP 直调通道（gis_run_gp）：白名单第一批（三箱 core 子集扣破坏类）
    外硬拦截；defer 回 DEFER_BLOCKED；破坏类回 DESTRUCTIVE_BLOCKED，
    强制走具名动词。discover 透传 gp_governance（含许可/扩展/弃用三
    字段的框架位，种子值未补齐处为 null，不冒充已知）。
  - Processing 执行面（gis_run_processing）：种子注册表校验（374 条
    seed，真源为实机枚举）；defer＋§3.1 点名类硬拦截回 DEFER_BLOCKED。
  - PostGIS 一律参数化模板（postgis_templates.json）：值走绑定参数，
    标识符过正则白名单，枚举走封闭集合；平台不开任何裸 SQL 动词。
  - 写操作分级确认门 R0–R3：R2 必需 confirm；R3 额外闸三件套
    （target_echo 逐字回显 + 只读预检回执二次确认 + 通道隔离）；
    网关只收紧、不放宽各桥既有 confirm 规则。
  - 许可闸：catalog 来源的发布/加图层（V34/V39）先查许可
    （evidence_ref 必须存在，commercial_use 与用途冲突回
    LICENSE_BLOCKED），与 confirm 无关、补 confirm 不能解闸。
  - 设计标待验/未核实的映射：登记在 verbs.json，网关拒绝执行并回
    UNVERIFIED_MAPPING，不写成可用。

calibration 只按 backends.json 声明透传、不升格；全部自检证据等级为
「离线协议自检」，不是实机校准。

配置：
  GIS_GATEWAY_BACKENDS  后端配置路径（默认同目录 backends.json）
  GIS_GATEWAY_TIMEOUT   单次后端调用超时秒数（默认 120）
日志写 stderr，stdout 只走 MCP 协议（与各桥同口径）。
"""
import hashlib
import io
import itertools
import json
import os
import queue
import re
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "gis-unified-gateway"
SERVER_VERSION = "0.3.0"
TIMEOUT = float(os.environ.get("GIS_GATEWAY_TIMEOUT", "120"))


def _load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


MAPPING = _load("mapping.json")
VERBS_DOC = _load("verbs.json")
VERBS = VERBS_DOC["verbs"]
VERB_ORDER = VERBS_DOC["verb_order"]
GP_REG = _load("gp_registry.json")
GP_ENTRIES = GP_REG["entries"]
GP_CHANNEL_WHITELIST = set(GP_REG["channel_whitelist"])
GP_DEFER = set(GP_REG["defer_blocklist"])
GP_DESTRUCTIVE = set(GP_REG["destructive_blocklist"])
PROC_REG = _load("processing_registry.json")
PROC_BY_ID = {e["algorithm_id"]: e for e in PROC_REG["entries"]}
PROC_HARD_BLOCK = {b["algorithm_id"]: b["reason"]
                   for b in PROC_REG["hard_blocklist"]}
TEMPLATES = {t["template_id"]: t
             for t in _load("postgis_templates.json")["templates"]}
BASE_TOOLS = list(MAPPING["tools"].keys())
UNIFIED_TOOLS = BASE_TOOLS + VERB_ORDER
BACKENDS = list(MAPPING["backends"].keys())
CATALOG_BACKEND = "catalog"


def log(*a):
    print("[gis-gateway]", *a, file=sys.stderr, flush=True)


def _dbg(msg):
    path = os.environ.get("GIS_GATEWAY_DEBUG")
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("%s %s\n" % (time.strftime("%H:%M:%S"), msg))
    except Exception:  # noqa: BLE001
        pass


# ---------------- 配置 ----------------

def load_config():
    path = os.environ.get("GIS_GATEWAY_BACKENDS") or os.path.join(HERE, "backends.json")
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    root = os.path.expanduser(cfg.get("bridges_root")
                              or "~/workspace/dsh-skills/gis-agent-bridges")
    catalog_dir = os.path.normpath(os.path.join(HERE, "..", "data-catalog"))

    def sub(s):
        return (s.replace("{python}", sys.executable)
                 .replace("{bridges}", root)
                 .replace("{here}", HERE)
                 .replace("{catalog}", catalog_dir))

    out = {}
    for name, b in cfg["backends"].items():
        out[name] = {"command": [sub(a) for a in b["command"]],
                     "mode": b["mode"], "calibration": b["calibration"]}
    return out


BACKEND_CONF = load_config()


def envelope(backend):
    c = BACKEND_CONF[backend]
    return {"backend": backend, "mode": c["mode"],
            "calibration": c["calibration"],
            "gateway": "%s/%s" % (SERVER_NAME, SERVER_VERSION)}


# ---------------- 错误 ----------------

class NotSupported(Exception):
    """统一层翻译不了/不在工具面内：回 NOT_SUPPORTED 并说明，不猜测。"""


class GatewayReject(Exception):
    """v0.2 治理拒绝（带明确 error_code 与可选附加段）。"""

    def __init__(self, code, message, extra=None):
        Exception.__init__(self, message)
        self.code = code
        self.message = message
        self.extra = extra or {}


class BackendError(Exception):
    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code
        self.message = message


class NativeCallError(Exception):
    """后端返回 isError：原生结构化错误原样透传（只叠加 envelope）。"""

    def __init__(self, payload):
        Exception.__init__(self, str(payload))
        self.payload = payload


# ---------------- 后端 stdio 客户端 ----------------

class StdioClient:
    """最小 MCP 客户端：子进程拉起后端 stdio 服务端，逐行 JSON-RPC 同步问答。"""

    def __init__(self, command):
        self.proc = subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            text=True, encoding="utf-8", errors="replace", bufsize=1)
        self.q = queue.Queue()
        self._id = 0
        self._lock = threading.Lock()
        threading.Thread(target=self._reader, daemon=True).start()
        self.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION, "capabilities": {},
            "clientInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized",
                    "params": {}})

    def _reader(self):
        try:
            for line in self.proc.stdout:
                line = line.strip()
                if not line:
                    continue
                try:
                    self.q.put(json.loads(line))
                except Exception:
                    pass
        finally:
            self.q.put(None)

    def _send(self, obj):
        self.proc.stdin.write(json.dumps(obj, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def request(self, method, params):
        with self._lock:
            self._id += 1
            mid = self._id
            self._send({"jsonrpc": "2.0", "id": mid, "method": method,
                        "params": params})
            while True:
                try:
                    msg = self.q.get(timeout=TIMEOUT)
                except queue.Empty:
                    raise BackendError("BACKEND_TIMEOUT",
                                       "后端 %.0fs 无响应" % TIMEOUT)
                if msg is None:
                    raise BackendError("BACKEND_EXITED", "后端进程已退出")
                if msg.get("id") == mid:
                    return msg

    def call_tool(self, name, args):
        resp = self.request("tools/call", {"name": name, "arguments": args or {}})
        if "error" in resp:
            raise BackendError("BACKEND_PROTOCOL_ERROR", str(resp["error"]))
        result = resp.get("result") or {}
        payload = result.get("structuredContent")
        if payload is None:
            texts = [c.get("text", "") for c in result.get("content", [])
                     if c.get("type") == "text"]
            if texts:
                try:
                    payload = json.loads(texts[0])
                except Exception:
                    payload = texts[0]
        if result.get("isError"):
            raise NativeCallError(payload if isinstance(payload, dict) else
                                  {"ok": False, "error_code": "NATIVE_ERROR",
                                   "message": str(payload)})
        return payload


_clients = {}
_clients_lock = threading.Lock()


def get_client(backend):
    with _clients_lock:
        if backend not in _clients:
            log("starting backend %s: %s" % (backend, BACKEND_CONF[backend]["command"]))
            _clients[backend] = StdioClient(BACKEND_CONF[backend]["command"])
        return _clients[backend]


def _data_catalog_section():
    """gis_discover 的 data_catalog 一节：实时调 catalog 后端聚合计数与
    许可摘要，不写死；catalog 未注册或不可达时 available=false 并说明。"""
    if CATALOG_BACKEND not in BACKEND_CONF:
        return {"available": False,
                "note": "本网关配置未注册 catalog 后端，无数据目录摘要"}
    try:
        res = get_client(CATALOG_BACKEND).call_tool("gis_catalog_list", {})
    except NativeCallError as e:
        return {"available": False, "error": e.payload}
    except BackendError as e:
        return {"available": False,
                "error": {"error_code": e.code, "message": e.message}}
    counts = res.get("counts") or {}
    return {"available": True,
            "catalog": res.get("catalog"),
            "total": counts.get("total"),
            "by_type": counts.get("by_type"),
            "by_license": counts.get("by_license"),
            "by_commercial_use": counts.get("by_commercial_use"),
            "index_updated_at": res.get("index_updated_at"),
            "license_note": "许可摘要透传自数据目录登记；逐条许可结论引用时带 "
                            "license.evidence_ref（见 gis_list_datasets "
                            "backend=catalog 的回包）"}


# ---------------- 基础 8 动词翻译（沿 v0.1，扩展至 8 后端） ----------------

def _sid(v):
    return v if isinstance(v, str) else str(v)


def translate(tool, backend, args):
    if backend not in BACKENDS:
        raise NotSupported("未知 backend=%r，支持：%s" % (backend, ", ".join(BACKENDS)))
    entry = MAPPING["tools"].get(tool)
    if entry is None:
        raise NotSupported("%s 不在基础工具面内" % tool)
    if backend == CATALOG_BACKEND:
        if tool == "gis_list_datasets":
            a = {}
            if args.get("type"):
                a["type"] = args["type"]
            if args.get("commercial_use") in (True, False):
                a["commercial_use"] = args["commercial_use"]
            return [(entry["backends"][backend]["native"][0], a, None)]
        raise NotSupported(
            "平台数据目录（catalog）只开放 gis_discover / gis_project_info / "
            "gis_list_datasets，%s 不在目录后端能力面内" % tool)
    if tool == "gis_list_maps" and backend == "qgis":
        return []  # 网关本地处理：空列表 + qgis_has_no_maps
    bmap = entry["backends"][backend]
    if bmap["native"] is None:
        raise NotSupported(bmap.get("note") or
                           "backend=%s 无 %s 能力" % (backend, tool))
    native = bmap["native"]

    if tool in ("gis_ping", "gis_discover", "gis_project_info"):
        return [(native[0], {}, None)]

    if tool == "gis_list_maps":
        return [(native[0], {}, None)]

    if tool == "gis_list_layers":
        if backend in ("supermap", "arcgis-pro"):
            a = {}
            if args.get("map"):
                a["map"] = args["map"]
            return [(native[0], a, None)]
        if backend == "arcmap":
            a = {}
            if args.get("map"):
                a["dataframe"] = args["map"]
            return [(native[0], a, None)]
        if backend == "geoserver":
            a = {}
            if args.get("workspace"):
                a["workspace"] = args["workspace"]
            return [(native[0], a, None)]
        if backend == "iserver":
            a = {}
            if args.get("map"):
                a["map"] = args["map"]
            return [(native[0], a, None)]
        return [(native[0], {}, None)]  # qgis：工程级，无 map 参数

    if tool == "gis_list_datasets":
        if backend == "postgis":
            return [(native[0], {}, None)]
        if backend == "iserver":
            a = {}
            if args.get("datasource"):
                a["datasource"] = args["datasource"]
            return [(native[0], a, None)]
        if backend != "supermap":
            raise NotSupported(
                "%s 没有数据源/数据集概念，gis_list_datasets 仅 SuperMap 系与 "
                "postgis（空间表）支持；该后端的图层数据源请看 gis_list_layers "
                "回包的 source 字段" % backend)
        a = {}
        if args.get("datasource"):
            a["datasource"] = args["datasource"]
        return [(native[0], {}, "datasources"), (native[1], a, "datasets")]

    if tool == "gis_set_layer_visible":
        if "layer" not in args or "visible" not in args:
            raise NotSupported("gis_set_layer_visible 需要 layer 与 visible 两个参数")
        a = {"layer": _sid(args["layer"]), "visible": bool(args["visible"])}
        if backend in ("supermap", "arcgis-pro"):
            if args.get("map"):
                a = dict({"map": args["map"]}, **a)
        elif backend == "arcmap":
            if args.get("map"):
                a = dict({"dataframe": args["map"]}, **a)
        return [(native[0], a, None)]

    if tool == "gis_zoom_to_layer":
        target = args.get("target") or {}
        ttype, tid = target.get("type"), target.get("id")
        if ttype not in ("layer", "dataset") or tid is None:
            raise NotSupported("gis_zoom_to_layer 需要 target={type: layer|dataset, id}")
        if backend == "supermap":
            if ttype != "dataset":
                raise NotSupported(
                    "SuperMap 的 zoom 只按数据集（supermap_zoom_to_dataset），"
                    "target.type=layer 无法翻译，不猜测")
            a = {"dataset": _sid(tid)}
            if args.get("datasource"):
                a["datasource"] = args["datasource"]
            if args.get("map"):
                a["map"] = args["map"]
            return [(native[0], a, None)]
        if ttype != "layer":
            raise NotSupported("%s 的 zoom 只按图层，target.type=dataset 无法翻译" % backend)
        if backend == "arcgis-pro":
            a = {"layer": _sid(tid)}
            if args.get("map"):
                a = dict({"map": args["map"]}, **a)
            return [(native[0], a, None)]
        if backend == "arcmap":
            a = {"layer": _sid(tid)}
            if args.get("map"):
                a = dict({"dataframe": args["map"]}, **a)
            return [(native[0], a, None)]
        return [(native[0], {"layer": _sid(tid)}, None)]  # qgis

    raise NotSupported("未实现的统一工具：%s" % tool)


# ---------------- 分发：基础动词 ----------------

def _merge_envelope(backend, payload):
    env = envelope(backend)
    if isinstance(payload, dict):
        out = dict(payload)
        out.update(env)
        return out
    out = {"result": payload}
    out.update(env)
    return out


def _v02_verbs_section(backend):
    supported, unverified = [], []
    for verb in VERB_ORDER:
        m = VERBS[verb]["backends"].get(backend)
        if not m:
            continue
        subs = []
        if "variants" in m:
            subs = list(m["variants"].values())
        elif "check" in m:
            subs = [m["check"], m["repair"]]
        else:
            subs = [m]
        sts = {s.get("status") for s in subs}
        if "ok" in sts:
            supported.append(verb)
        elif "unverified" in sts:
            unverified.append(verb)
    return {"supported": supported, "unverified_registered": unverified,
            "note": "unverified_registered 内的动词在本后端有登记映射但标"
                    "待验，调用回 UNVERIFIED_MAPPING，不写成可用"}


def dispatch_base(tool, args):
    args = args or {}
    backend = args.get("backend")
    try:
        if backend not in BACKENDS:
            raise NotSupported("参数 backend 必填且只能是：%s" % ", ".join(BACKENDS))
        if backend not in BACKEND_CONF:
            raise NotSupported("backend %s 未在本网关的 backends 配置中注册" % backend)
        meta = MAPPING["backends"][backend]

        if tool == "gis_discover":
            payload = {"supported_verbs": meta["supported_verbs"],
                       "extension_namespaces": meta["extension_namespaces"],
                       "extension_note": meta["extension_note"],
                       "project_kind": meta["project_kind"]}
            if backend != CATALOG_BACKEND:
                try:
                    payload["native_discover"] = get_client(backend).call_tool(
                        MAPPING["tools"]["gis_discover"]["backends"][backend]["native"][0], {})
                except (BackendError, NativeCallError) as e:
                    payload["native_discover_error"] = (
                        e.payload if isinstance(e, NativeCallError)
                        else {"error_code": e.code, "message": e.message})
            payload["v02_verbs"] = _v02_verbs_section(backend)
            if backend == "arcgis-pro":
                payload["gp_governance"] = {
                    "whitelist_batch1": len(GP_REG["whitelist_batch1"]),
                    "channel_whitelist": len(GP_REG["channel_whitelist"]),
                    "defer_blocked": len(GP_REG["defer_blocklist"]),
                    "destructive_blocked_in_channel":
                        len(GP_REG["destructive_blocklist"]),
                    "fields": ["license_level", "requires_extension",
                               "deprecated"],
                    "note": GP_REG["governance_fields_note"]}
            if backend == "qgis":
                payload["processing_registry"] = {
                    "total": PROC_REG["counts"]["total"],
                    "counts": PROC_REG["counts"], "status": "seed",
                    "hard_blocked": len(PROC_REG["hard_blocklist"]),
                    "note": PROC_REG["evidence_level"]}
            if backend == "postgis":
                payload["postgis_templates"] = {
                    "count": len(TEMPLATES), "policy":
                        "参数化模板，永不裸 SQL（设计 §3.3）；模板面未经"
                        "实机校准（本地实例未起，D2）"}
            payload["data_catalog"] = _data_catalog_section()
            return _merge_envelope(backend, payload)

        if tool == "gis_project_info" and backend == CATALOG_BACKEND:
            sec = _data_catalog_section()
            payload = {"object": "project", "kind": "catalog",
                       "stac_role": "catalog",
                       "title": sec.get("catalog") or "GIS 平台数据目录（data-catalog）"}
            if sec.get("available"):
                payload["datasets_total"] = sec.get("total")
                payload["index_updated_at"] = sec.get("index_updated_at")
            else:
                payload["data_catalog_error"] = sec
            return _merge_envelope(backend, payload)

        plan = translate(tool, backend, args)

        if tool == "gis_list_maps" and backend == "qgis":
            return _merge_envelope(backend, {"maps": [], "note": "qgis_has_no_maps"})

        client = get_client(backend)
        if len(plan) == 1 and plan[0][2] is None:
            payload = client.call_tool(plan[0][0], plan[0][1])
        else:
            payload = {}
            for native_name, native_args, key in plan:
                payload[key] = client.call_tool(native_name, native_args)

        if tool == "gis_list_datasets" and backend == CATALOG_BACKEND \
                and isinstance(payload, dict):
            ds = []
            for r in payload.get("datasets", []):
                r = dict(r)
                r["object"] = "dataset"
                r["stac_role"] = "collection"
                ds.append(r)
            payload = {"object": "dataset", "stac_role": "collection",
                       "source_kind": "platform_data_catalog",
                       "catalog": payload.get("catalog"),
                       "datasets": ds,
                       "count": payload.get("count"),
                       "counts": payload.get("counts"),
                       "index_updated_at": payload.get("index_updated_at"),
                       "note": "平台级数据目录的登记数据集（核心对象 dataset，"
                               "STAC Collection 对应物）；与厂商工作空间内的"
                               "数据源/数据集、postgis 的数据库空间表均不是"
                               "同一概念"}
        elif tool == "gis_list_datasets" and backend == "supermap" \
                and isinstance(payload, dict):
            payload = dict(payload)
            payload["source_kind"] = "vendor_workspace"
            payload["note"] = "厂商工作空间内的数据源/数据集（运行时现场状态）；" \
                              "平台数据目录的登记数据集走 backend=catalog"
        elif tool == "gis_list_datasets" and backend == "postgis":
            payload = {"object": "dataset", "source_kind": "server_database",
                       "tables": payload,
                       "note": "数据库中的空间表（服务端对象）；与厂商工作"
                               "空间数据集、平台目录登记数据集显式区分"}
        elif tool == "gis_project_info" and backend == "postgis":
            payload = {"object": "project", "kind": "database",
                       "tables": payload,
                       "note": "数据库无工程概念：以空间表清单作工程概览"}
        elif tool == "gis_project_info" and backend == "geoserver":
            payload = {"object": "project", "kind": "service",
                       "workspaces": payload,
                       "note": "服务无工程概念：以工作区清单作工程概览"}
        elif tool == "gis_project_info" and backend == "istsos" \
                and isinstance(payload, dict):
            payload = dict(payload)
            payload["object"] = "project"
            payload["kind"] = "service"

        if tool == "gis_list_maps" and backend == "arcmap" and isinstance(payload, list):
            maps = []
            for m in payload:
                m = dict(m) if isinstance(m, dict) else {"name": str(m)}
                m["type"] = "dataframe"
                maps.append(m)
            payload = {"maps": maps, "maps_kind": "dataframe"}
        elif tool == "gis_list_maps" and isinstance(payload, list):
            payload = {"maps": payload}
        if tool == "gis_list_layers" and backend == "qgis" and args.get("map"):
            if isinstance(payload, dict):
                payload = dict(payload)
                payload["note"] = "qgis layers are project-level; map argument ignored"
        return _merge_envelope(backend, payload)

    except NotSupported as e:
        out = {"ok": False, "error_code": "NOT_SUPPORTED", "message": str(e),
               "tool": tool, "supported_tools": UNIFIED_TOOLS}
        if backend in BACKEND_CONF:
            out.update(envelope(backend))
        return out
    except NativeCallError as e:
        return _merge_envelope(backend, e.payload)
    except BackendError as e:
        out = {"ok": False, "error_code": e.code, "message": e.message, "tool": tool}
        if backend in BACKEND_CONF:
            out.update(envelope(backend))
        return out


# ---------------- PostGIS 参数化模板 ----------------

IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
IDENT_TABLE_RE = re.compile(
    r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?$")
EXPR_BAD_RE = re.compile(
    r";|--|/\*|\b(drop|alter|create|insert|delete|update|grant|revoke|"
    r"truncate|copy|execute|vacuum)\b", re.I)
SLOT_RE = re.compile(r"\{(ident|idents|enum|expr|fragment|union_all|"
                     r"attr_columns):([\w]+)\}|\%\(([\w]+)\)s")


def _first(args, *keys):
    for k in keys:
        if args.get(k) is not None:
            return args[k]
    return None


def _check_ident(value, table=False):
    if not isinstance(value, str) or not (
            IDENT_TABLE_RE if table else IDENT_RE).match(value):
        raise GatewayReject("INVALID_ARGUMENT",
                            "标识符 %r 不合白名单正则，拒绝拼入 SQL" % (value,))
    return value


def _build_reclassarg(rules):
    parts = []
    for r in rules:
        if not (isinstance(r, (list, tuple)) and len(r) == 3):
            raise GatewayReject("INVALID_ARGUMENT",
                                "reclassify rules 每项须为 [from,to,new]")
        try:
            lo, hi, new = float(r[0]), float(r[1]), float(r[2])
        except Exception:
            raise GatewayReject("INVALID_ARGUMENT",
                                "reclassify rules 只接受数值：%r" % (r,))
        def num(x):
            return str(int(x)) if x == int(x) else str(x)
        parts.append("[%s-%s]:%s" % (num(lo), num(hi), num(new)))
    return ",".join(parts)


def gather_template_values(verb, tpl, args):
    """把统一动词参数按模板参数名归集（含动词参数名适配与默认值）。"""
    vals = {}
    P = tpl["params"]

    def put(name, value):
        if value is not None:
            vals[name] = value

    for name in P:
        put(name, args.get(name))
    if "table" in P:
        put("table", _first(args, "table", "dataset", "input", "name"))
    if "target" in P:
        put("target", _first(args, "target", "target_name"))
    if "source" in P:
        put("source", _first(args, "source", "input", "dataset", "table"))
        if isinstance(args.get("inputs"), dict) and args["inputs"]:
            put("source", next(iter(args["inputs"].values())))
    if "column" in P:
        col = _first(args, "column")
        if col is None:
            field = args.get("field")
            if isinstance(field, dict):
                col = field.get("name")
            else:
                col = field
        if col is None and isinstance(args.get("fields"), list) \
                and args["fields"]:
            if len(args["fields"]) > 1:
                raise GatewayReject(
                    "INVALID_ARGUMENT",
                    "模板 %s 一次只处理一个字段，多字段请逐次调用"
                    % tpl["template_id"])
            col = args["fields"][0]
        put("column", col)
    if "sql_type" in P and "sql_type" not in vals \
            and isinstance(args.get("field"), dict):
        put("sql_type", args["field"].get("type"))
    if "clip_table" in P:
        put("clip_table", args.get("clip_by"))
    if "clip_wkt" in P:
        cb = args.get("clip_by")
        if isinstance(cb, str) and re.match(
                r"^\s*(POLYGON|MULTIPOLYGON|LINESTRING|POINT|MULTIPOINT|"
                r"MULTILINESTRING)\s*\(", cb, re.I):
            put("clip_wkt", cb)
    if "overlay_table" in P:
        put("overlay_table", _first(args, "overlay", "overlay_table"))
    if "join_table" in P:
        put("join_table", _first(args, "join", "join_table"))
    if "zones_table" in P:
        put("zones_table", args.get("zones"))
    if "values_table" in P:
        put("values_table", args.get("values"))
    if "group_columns" in P:
        put("group_columns",
            args.get("fields") or args.get("group_by") or [])
    if "group_by" in P:
        put("group_by", args.get("group_by") or [])
    if "file_path" in P:
        put("file_path", args.get("source_uri"))
    if "reclassarg" in P and args.get("rules"):
        put("reclassarg", _build_reclassarg(args["rules"]))
    if "layer_name" in P:
        put("layer_name", args.get("layer_name") or args.get("table"))
    if "attributes" in P:
        put("attributes", args.get("attributes") or [])
    if "statistics" in P:
        put("statistics", args.get("statistics") or ["count"])
    for name, spec in P.items():
        if name not in vals and "default" in spec:
            vals[name] = spec["default"]
    return vals


def _substitute(tpl, sql, vals, params_out):
    """把一条 SQL 模板渲染为 (sql, bound_params)：值永不拼进 SQL 文本。"""
    P = tpl["params"]

    def repl(m):
        kind, name, vname = m.group(1), m.group(2), m.group(3)
        if vname is not None:  # %(name)s 绑定参数
            if vname not in vals:
                raise GatewayReject(
                    "INVALID_ARGUMENT",
                    "模板 %s 缺少必填参数 %s" % (tpl["template_id"], vname))
            params_out[vname] = vals[vname]
            return "%%(%s)s" % vname
        if name not in vals and kind not in ("attr_columns",):
            spec = P.get(name) or {}
            if "default" not in spec:
                raise GatewayReject(
                    "INVALID_ARGUMENT",
                    "模板 %s 缺少必填参数 %s" % (tpl["template_id"], name))
            vals[name] = spec["default"]
        v = vals.get(name)
        if kind == "ident":
            spec = P.get(name) or {}
            return _check_ident(v, table=(spec.get("kind") == "ident_table"))
        if kind == "idents":
            if not isinstance(v, list):
                raise GatewayReject("INVALID_ARGUMENT",
                                    "参数 %s 须为标识符列表" % name)
            return ", ".join(_check_ident(x) for x in v)
        if kind == "enum":
            spec = P.get(name) or {}
            if v not in (spec.get("values") or []):
                raise GatewayReject(
                    "INVALID_ARGUMENT",
                    "参数 %s=%r 不在封闭枚举 %s 内"
                    % (name, v, spec.get("values")))
            return str(v)
        if kind == "expr":
            if not isinstance(v, str) or EXPR_BAD_RE.search(v):
                raise GatewayReject(
                    "INVALID_ARGUMENT",
                    "表达式片段不合受限口径（单表达式，禁分号与 DDL/DML "
                    "关键字）：%r" % (v,))
            return v
        if kind == "fragment":
            frags = (tpl.get("fragments") or {}).get(name) or {}
            key = vals.get(name)
            if key not in frags:
                raise GatewayReject(
                    "INVALID_ARGUMENT",
                    "模板片段 %s 无 %r 对应（封闭映射）" % (name, key))
            return _substitute(tpl, frags[key], vals, params_out)
        if kind == "union_all":
            if not isinstance(v, list) or not v:
                raise GatewayReject("INVALID_ARGUMENT",
                                    "参数 %s 须为非空表名列表" % name)
            return " UNION ALL ".join(
                "SELECT * FROM %s" % _check_ident(x, table=True) for x in v)
        if kind == "attr_columns":
            attrs = vals.get("attributes") or []
            if not isinstance(attrs, list):
                raise GatewayReject("INVALID_ARGUMENT",
                                    "attributes 须为列名列表")
            return "".join(", %s" % _check_ident(x) for x in attrs)
        raise GatewayReject("INVALID_ARGUMENT", "未知模板槽 %s:%s" % (kind, name))

    return SLOT_RE.sub(repl, sql)


def build_template(verb, tpl_id, args):
    """渲染模板 -> (sql, bound_params, tpl)。builder 模板走专用拼装。"""
    tpl = TEMPLATES[tpl_id]
    vals = gather_template_values(verb, tpl, args)
    builder = tpl.get("builder")
    params = {}
    if builder == "field_stats":
        table = _check_ident(vals.get("table"), table=True)
        fields = vals.get("fields") or []
        if not fields:
            raise GatewayReject("INVALID_ARGUMENT",
                                "gis_field_statistics 需要 fields")
        stats = vals.get("statistics") or ["count"]
        allowed = tpl["params"]["statistics"]["values"]
        for s in stats:
            if s not in allowed:
                raise GatewayReject("INVALID_ARGUMENT",
                                    "统计量 %r 不在封闭枚举内" % (s,))
        group = vals.get("group_by") or []
        cols = [_check_ident(g) for g in group]
        for f in fields:
            f = _check_ident(f)
            for s in stats:
                cols.append("%s(%s) AS %s_%s" % (s, f, f, s))
        sql = "SELECT %s FROM %s" % (", ".join(cols), table)
        if group:
            sql += " GROUP BY %s" % ", ".join(
                _check_ident(g) for g in group)
        if args.get("output") == "stored":
            target = _check_ident(args.get("target"), table=True)
            sql = "CREATE TABLE %s AS %s" % (target, sql)
        return sql, params, tpl
    if builder == "spatial_filter":
        geom = _check_ident(vals.get("geometry_column") or "geom")
        pred = vals.get("predicate")
        if vals.get("reference_table"):
            ref = "(SELECT %s FROM %s LIMIT 1)" % (
                geom, _check_ident(vals["reference_table"], table=True))
        elif vals.get("reference_wkt"):
            ref = "ST_GeomFromText(%(reference_wkt)s, %(srid)s)"
            params["reference_wkt"] = vals["reference_wkt"]
            params["srid"] = vals.get("srid", 4326)
        else:
            raise GatewayReject(
                "INVALID_ARGUMENT",
                "gis_spatial_filter 需要 reference_wkt 或 reference_table")
        frags = {
            "intersects": "ST_Intersects(%s, %s)" % (geom, ref),
            "contains": "ST_Contains(%s, %s)" % (geom, ref),
            "within": "ST_Within(%s, %s)" % (geom, ref),
            "dwithin": "ST_DWithin(%s, %s, %%(distance)s)" % (geom, ref),
        }
        if pred not in frags:
            raise GatewayReject("INVALID_ARGUMENT",
                                "predicate %r 不在封闭枚举内" % (pred,))
        if pred == "dwithin":
            if vals.get("distance") is None:
                raise GatewayReject("INVALID_ARGUMENT",
                                    "predicate=dwithin 需要 distance")
            params["distance"] = vals["distance"]
        params["limit"] = vals.get("limit", 1000)
        sql = "SELECT * FROM %s WHERE %s LIMIT %%(limit)s" % (
            _check_ident(vals.get("table"), table=True), frags[pred])
        return sql, params, tpl
    if builder == "spatial_join":
        # 2026-11-03 实机校准定版：连接表属性显式列出并别名化，
        # 避免 a.*, b.* 在两表同名列（如 id）时建表失败。
        attrs = vals.get("attributes") or []
        if not isinstance(attrs, list) or not attrs:
            raise GatewayReject(
                "INVALID_ARGUMENT",
                "gis_spatial_join 需要 attributes 列出连接表要带出的属性列"
                "（带出列别名为 join_<列名>，连接表几何为 join_geom）")
        geom = _check_ident(vals.get("geometry_column") or "geom")
        frags = tpl["fragments"]["predicate"]
        pred = vals.get("predicate")
        if pred not in frags:
            raise GatewayReject("INVALID_ARGUMENT",
                                "predicate %r 不在封闭枚举内" % (pred,))
        frag = _substitute(tpl, frags[pred], vals, params)
        cols = ["a.*"]
        for c in attrs:
            ci = _check_ident(c)
            cols.append("b.%s AS join_%s" % (ci, ci))
        cols.append("b.%s AS join_geom" % geom)
        sql = "CREATE TABLE %s AS SELECT %s FROM %s a JOIN %s b ON %s" % (
            _check_ident(vals.get("target"), table=True), ", ".join(cols),
            _check_ident(vals.get("source"), table=True),
            _check_ident(vals.get("join_table"), table=True), frag)
        return sql, params, tpl
    sql = tpl["sql"]
    if tpl.get("sql_nogroup") is not None and not vals.get("group_columns"):
        sql = tpl["sql_nogroup"]
    if tpl.get("sql_table_clip") is not None and not vals.get("clip_wkt"):
        sql = tpl["sql_table_clip"]
    return _substitute(tpl, sql, vals, params), params, tpl


# ---------------- R3 额外闸（设计 §4.2 三件套） ----------------

_PREFLIGHTS = {}
_PREFLIGHT_SEQ = itertools.count(1)

PREFLIGHT_PROBES = {
    ("gis_delete_field", "postgis"):
        lambda a: ("postgis_table_columns", {"table": a.get("dataset")}),
    ("gis_delete_field", "arcgis-pro"):
        lambda a: ("arcgis_list_tables", {}),
    ("gis_delete_field", "supermap"):
        lambda a: ("supermap_list_datasets", {}),
    ("gis_delete_field", "qgis"):
        lambda a: ("qgis_list_fields", {"layer": a.get("dataset")}),
    ("gis_delete_dataset", "postgis"):
        lambda a: ("postgis_table_summary", {"table": a.get("dataset")}),
    ("gis_delete_dataset", "supermap"):
        lambda a: ("supermap_list_datasets", {}),
    ("gis_delete_dataset", "arcgis-pro"):
        lambda a: ("arcgis_list_tables", {}),
    ("gis_reproject", "postgis"):
        lambda a: ("postgis_table_summary", {"table": a.get("input")}),
    ("gis_reproject", "qgis"):
        lambda a: ("qgis_list_layers", {}),
    ("gis_reproject", "arcgis-pro"):
        lambda a: ("arcgis_list_tables", {}),
}


def _r3_echo_expected(verb, args):
    if verb == "gis_delete_field":
        return "%s.%s" % (args.get("dataset"),
                          ",".join(args.get("fields") or []))
    if verb == "gis_delete_dataset":
        return args.get("dataset")
    if verb == "gis_reproject":
        return args.get("input")
    return None


def r3_gate(verb, backend, args):
    """通过则静默返回；不通过抛 GatewayReject。
    件套 1 目标回显、件套 2 影响面预检回执二次确认（件套 3 通道隔离在
    V01/V02 与模板面的拦截逻辑里）。"""
    if args.get("confirm") is not True:
        raise GatewayReject("CONFIRM_REQUIRED",
                            "%s 为 R3 破坏性操作，confirm=true 必需，永不免确认"
                            % verb)
    expected = _r3_echo_expected(verb, args)
    if args.get("target_echo") != expected:
        raise GatewayReject(
            "TARGET_ECHO_MISMATCH",
            "target_echo 须与目标对象全名逐字一致",
            {"expected_target": expected})
    pfid = args.get("preflight_id")
    if pfid:
        rec = _PREFLIGHTS.get(pfid)
        if rec and rec["tool"] == verb and rec["backend"] == backend \
                and rec["target"] == expected:
            del _PREFLIGHTS[pfid]
            return
        raise GatewayReject(
            "PREFLIGHT_MISMATCH",
            "preflight_id 与本次调用的目标/后端/动词对不上，请重新预检")
    probe_fn = PREFLIGHT_PROBES.get((verb, backend))
    if probe_fn is None:
        raise GatewayReject("NOT_SUPPORTED",
                            "%s 在 backend=%s 未配置预检探针，R3 不放行"
                            % (verb, backend))
    native, pargs = probe_fn(args)
    try:
        snapshot = get_client(backend).call_tool(native, pargs)
    except NativeCallError as e:
        snapshot = {"probe_error": e.payload}
    except BackendError as e:
        snapshot = {"probe_error": {"error_code": e.code,
                                    "message": e.message}}
    pid = "pf_%s_%d" % (hashlib.sha1(
        ("%s|%s|%s" % (verb, backend, expected)).encode("utf-8")
    ).hexdigest()[:10], next(_PREFLIGHT_SEQ))
    _PREFLIGHTS[pid] = {"tool": verb, "backend": backend,
                        "target": expected}
    raise GatewayReject(
        "PREFLIGHT_REQUIRED",
        "R3 影响面预检已完成：请核对 preflight.snapshot 后，带同一 "
        "preflight_id 与 target_echo 二次确认再执行",
        {"preflight": {"preflight_id": pid, "target": expected,
                       "probe_tool": native, "snapshot": snapshot}})


def require_confirm(verb, level, spec, args, raised=False):
    if level == "R2":
        if args.get("confirm") is not True:
            raise GatewayReject(
                "CONFIRM_REQUIRED",
                "%s 为 R2 原地改写，confirm=true 必需（不许默认）" % verb)
    elif level == "R1":
        # 基础 R1：只透传桥侧 confirm 语义（spec.confirm=required 才拦）。
        # 动态升 R1（如 V29 output=stored 落表）：设计明示「升 R1 需
        # confirm」，且模板面没有桥侧 confirm 可透传，网关自己拦。
        if (spec.get("confirm") == "required" or raised) \
                and args.get("confirm") is not True:
            raise GatewayReject(
                "CONFIRM_REQUIRED",
                "%s 为 R1 写操作，本映射要求 confirm=true" % verb)


# ---------------- 许可闸（设计 §3.4 / §4.1-4） ----------------

def catalog_describe(catalog_id):
    try:
        rec = get_client(CATALOG_BACKEND).call_tool(
            "gis_catalog_describe", {"id": catalog_id})
    except NativeCallError as e:
        code = e.payload.get("error_code", "NATIVE_ERROR") \
            if isinstance(e.payload, dict) else "NATIVE_ERROR"
        raise GatewayReject(code, "目录查询失败：%s" % (e.payload,))
    if not isinstance(rec, dict):
        raise GatewayReject("LICENSE_BLOCKED",
                            "目录记录形态异常，许可闸不放行")
    return rec


def license_gate(catalog_id, purpose):
    """返回目录记录；不合闸抛 LICENSE_BLOCKED（与 confirm 无关）。"""
    rec = catalog_describe(catalog_id)
    lic = rec.get("license") or {}
    if not lic.get("evidence_ref"):
        raise GatewayReject(
            "LICENSE_BLOCKED",
            "数据集 %s 的许可无 evidence_ref，许可闸硬拦（设计 §3.4）"
            % catalog_id)
    cu = lic.get("commercial_use")
    if cu is False:
        raise GatewayReject(
            "LICENSE_BLOCKED",
            "数据集 %s 的 commercial_use=false，与发布/取用用途冲突"
            % catalog_id)
    if cu is not True and purpose == "commercial":
        raise GatewayReject(
            "LICENSE_BLOCKED",
            "数据集 %s 的 commercial_use=%s，商用用途下许可闸硬拦"
            % (catalog_id, cu))
    return rec


# ---------------- 第一波动词：映射解析与执行 ----------------

def resolve_mapping(verb, backend, args):
    """返回 (sub_mapping, variant_key)。variant 缺失/不合时返回一个
    not_supported 形态的子映射（带说明），不猜测。"""
    m = VERBS[verb]["backends"].get(backend)
    if m is None:
        return None, None
    if "variants" in m:
        key = args.get(m["variant_arg"])
        variants = m["variants"]
        if key in variants:
            return variants[key], key
        if "*" in variants:
            return variants["*"], key
        return ({"status": "not_supported",
                 "note": "%s 的 %s=%r 在 backend=%s 无映射（可选：%s）"
                         % (verb, m["variant_arg"], key, backend,
                            ", ".join(sorted(k for k in variants
                                             if k != "*")))},
                key)
    if "check" in m:
        return (m["repair"] if args.get("repair") else m["check"]), \
            ("repair" if args.get("repair") else "check")
    return m, None


def verb_level(verb, spec, args):
    lvl = spec["level"]
    if verb == "gis_reproject" and args.get("overwrite"):
        return "R3"
    if verb == "gis_field_statistics" and args.get("output") == "stored":
        return "R1"
    if verb == "gis_validate_geometry" and args.get("repair"):
        return "R2"
    return lvl


_GW_KEYS = {"backend", "confirm", "target_echo", "preflight_id"}


def _fwd_args(args):
    return {k: v for k, v in args.items() if k not in _GW_KEYS}


def execute_mapping(verb, backend, mapping, args):
    kind = mapping["kind"]
    fwd = _fwd_args(args)
    if kind == "native":
        _dbg("native start verb=%s backend=%s tool=%s args=%r"
             % (verb, backend, mapping["native"], fwd))
        try:
            res = get_client(backend).call_tool(mapping["native"], fwd)
            _dbg("native done verb=%s backend=%s tool=%s"
                 % (verb, backend, mapping["native"]))
            return res
        except Exception as e:  # noqa: BLE001
            _dbg("native error verb=%s backend=%s tool=%s: %r"
                 % (verb, backend, mapping["native"], e))
            raise
    if kind == "gp_named":
        return get_client("arcgis-pro").call_tool(
            "arcgis_run_gp", {"tool": mapping["func"], "args": fwd,
                              "via_verb": verb, "confirm": True})
    if kind == "processing":
        alg = mapping["algorithm"]
        if alg in PROC_HARD_BLOCK:
            raise GatewayReject(
                "DEFER_BLOCKED",
                "算法 %s 在硬拦截名单内：%s" % (alg, PROC_HARD_BLOCK[alg]))
        return get_client("qgis").call_tool(
            "qgis_run_processing", {"algorithm": alg, "params": fwd,
                                    "confirm": True})
    if kind == "template":
        sql, params, tpl = build_template(verb, mapping["template"], args)
        res = get_client("postgis").call_tool(
            "postgis_exec_template",
            {"template_id": mapping["template"], "sql": sql,
             "params": params, "confirm": True})
        return {"template_id": mapping["template"],
                "sql": sql, "bound_params": params,
                "note": "值经绑定参数传递（bound_params），未拼入 sql 文本；"
                        "模板执行器为桥侧 pending 工具，结果为其回包",
                "backend_result": res}
    raise GatewayReject("NOT_SUPPORTED", "未知映射类型 %s" % kind)


# ---------------- 第一波动词：通道与注册表 ----------------

GP_TOOL_RE = re.compile(r"^arcpy\.[a-z][\w]*\.[A-Z][\w]*$")


def dispatch_run_gp(verb, backend, args):
    tool = args.get("tool")
    if not tool or not GP_TOOL_RE.match(str(tool)):
        raise GatewayReject(
            "INVALID_ARGUMENT",
            "gis_run_gp 需要 tool='<module>.<Func>'（ArcPy 官方命名空间），"
            "收到 %r" % (tool,))
    if tool in GP_DESTRUCTIVE:
        raise GatewayReject(
            "DESTRUCTIVE_BLOCKED",
            "%s 为破坏类工具：GP 通道内硬拦截，请走具名动词"
            "（gis_delete_dataset / gis_delete_field）＋R3 额外闸" % tool)
    entry = GP_ENTRIES.get(tool)
    if entry is not None and entry["judgment"] == "defer":
        raise GatewayReject(
            "DEFER_BLOCKED",
            "%s 在普查 defer 名单内（152 条全量硬拦），通道不放行" % tool)
    if tool not in GP_CHANNEL_WHITELIST:
        why = "未在普查注册表中" if entry is None else \
            "平台判断=%s / 白名单批次未开（本波只开三箱 core 子集）" \
            % entry["judgment"]
        raise GatewayReject("GP_NOT_WHITELISTED",
                            "%s 不在通道白名单内：%s" % (tool, why))
    level = entry["level"]
    if level == "R2" and args.get("confirm") is not True:
        raise GatewayReject(
            "CONFIRM_REQUIRED",
            "%s 按语义定级 R2（原地改写类），confirm=true 必需" % tool)
    payload = get_client("arcgis-pro").call_tool(
        "arcgis_run_gp", {"tool": tool, "args": args.get("args") or {},
                          "via_verb": None,
                          "confirm": args.get("confirm")})
    return payload, level


def dispatch_run_processing(verb, backend, args):
    alg = args.get("algorithm")
    entry = PROC_BY_ID.get(alg)
    if entry is None:
        raise GatewayReject(
            "ALGORITHM_NOT_REGISTERED",
            "算法 %r 不在 Processing 种子注册表内（374 条）；未建账算法"
            "不许经执行面直通" % (alg,))
    if alg in PROC_HARD_BLOCK:
        raise GatewayReject(
            "DEFER_BLOCKED",
            "算法 %s 在硬拦截名单内：%s" % (alg, PROC_HARD_BLOCK[alg]))
    if args.get("confirm") is not True:
        raise GatewayReject(
            "CONFIRM_REQUIRED",
            "gis_run_processing 要求 confirm=true（桥既有规则，网关不放宽）")
    payload = get_client(backend).call_tool(
        "qgis_run_processing", {"algorithm": alg,
                                "params": args.get("params") or {},
                                "confirm": True})
    out = payload if isinstance(payload, dict) else {"result": payload}
    out = dict(out)
    out["registry_status"] = entry["status"]
    out["platform_judgment"] = entry["platform_judgment"]
    return out, "R1"


def dispatch_registry(verb, backend, mapping, args):
    reg = mapping["registry"]
    if verb == "gis_list_algorithms":
        if reg == "processing":
            entries = PROC_REG["entries"]
            if args.get("provider"):
                entries = [e for e in entries
                           if e["provider"] == args["provider"]]
            if args.get("judgment"):
                entries = [e for e in entries
                           if e["platform_judgment"] == args["judgment"]]
            return {"registry": "processing", "status": "seed",
                    "total": len(entries),
                    "counts": PROC_REG["counts"], "entries": entries,
                    "note": PROC_REG["evidence_level"]}
        if reg == "gp":
            entries = GP_ENTRIES
            items = [{"tool": fn, **e} for fn, e in sorted(entries.items())]
            if args.get("judgment"):
                items = [i for i in items
                         if i["judgment"] == args["judgment"]]
            total = len(items)
            return {"registry": "gp", "total": total,
                    "counts": GP_REG["counts"],
                    "whitelist_batch1": len(GP_REG["whitelist_batch1"]),
                    "channel_whitelist": len(GP_REG["channel_whitelist"]),
                    "entries": items[:500],
                    "truncated": total > 500,
                    "note": "许可三字段种子位见条目 license_level / "
                            "requires_extension / deprecated"}
        if reg == "templates":
            return {"registry": "postgis_templates",
                    "total": len(TEMPLATES),
                    "entries": [{"template_id": t["template_id"],
                                 "verbs": t["verbs"], "level": t["level"],
                                 "description": t["description"]}
                                for t in TEMPLATES.values()],
                    "note": "参数化模板清单（设计 §3.3），永不裸 SQL"}
        if reg == "supermap":
            sr = VERBS_DOC["supermap_registry"]
            return {"registry": "supermap_file_registry",
                    "total": len(sr["entries"]), "entries": sr["entries"],
                    "note": sr["evidence_level"] + "；" + sr["source"]}
    if verb == "gis_describe_algorithm":
        alg = args.get("algorithm")
        if reg == "processing":
            e = PROC_BY_ID.get(alg)
            if e is None:
                raise NotSupported("算法 %r 不在 Processing 种子注册表内"
                                   % (alg,))
            out = dict(e)
            out["params_schema_note"] = \
                "种子账无参数模式：参数模式待桥侧 algorithmHelp 建账" \
                "（D6），此处不编造"
            return out
        if reg == "gp":
            e = GP_ENTRIES.get(alg)
            if e is None:
                raise NotSupported("工具 %r 不在 GP 注册表内" % (alg,))
            out = {"tool": alg}
            out.update(e)
            out["signature_note"] = "函数名按普查口径，实际签名以目标机 " \
                                    "arcpy 导入为准"
            return out
        if reg == "templates":
            t = TEMPLATES.get(alg)
            if t is None:
                raise NotSupported("模板 %r 不在模板集中" % (alg,))
            return dict(t)
    raise NotSupported("%s 的注册表形态未实现" % verb)


# ---------------- 第一波动词：分发 ----------------

def dispatch_verb(verb, args):
    args = args or {}
    backend = args.get("backend")
    spec = VERBS[verb]
    try:
        if backend not in BACKENDS:
            raise NotSupported("参数 backend 必填且只能是：%s"
                               % ", ".join(BACKENDS))
        if backend not in BACKEND_CONF:
            raise NotSupported("backend %s 未在本网关的 backends 配置中注册"
                               % backend)
        if backend not in spec["backends"]:
            supported = ", ".join(sorted(spec["backends"].keys()))
            raise NotSupported("%s 不支持 backend=%s（支持：%s）"
                               % (verb, backend, supported))
        mapping, variant_key = resolve_mapping(verb, backend, args)
        if mapping is None:
            raise NotSupported("%s 不支持 backend=%s" % (verb, backend))
        if mapping.get("status") == "unverified":
            raise GatewayReject(
                "UNVERIFIED_MAPPING",
                "%s 在 backend=%s 的映射已登记但标待验/未核实，拒绝执行、"
                "不写成可用：%s" % (verb, backend, mapping.get("note", "")),
                {"wheel": mapping.get("wheel")})
        if mapping.get("status") == "not_supported":
            raise NotSupported(mapping.get("note")
                               or "%s 在 backend=%s 不支持" % (verb, backend))

        kind = mapping["kind"]
        extra = {}

        # 通道类（自带名单校验与定级）
        if kind == "gp_channel":
            payload, level = dispatch_run_gp(verb, backend, args)
            return _decorate(verb, spec, backend, payload, level, mapping,
                             extra)
        if kind == "processing_channel":
            payload, level = dispatch_run_processing(verb, backend, args)
            return _decorate(verb, spec, backend, payload, level, mapping,
                             extra)
        # 注册表类（网关本地）
        if kind == "registry":
            payload = dispatch_registry(verb, backend, mapping, args)
            return _decorate(verb, spec, backend, payload, "R0", mapping,
                             extra)

        level = verb_level(verb, spec, args)

        # 许可闸前置（V34/V39，先于 confirm，设计 §4.1-4）
        if verb == "gis_add_layer_from_catalog":
            rec = license_gate(args.get("catalog_id"),
                               args.get("purpose") or "research")
            extra["license_gate"] = {
                "catalog_id": args.get("catalog_id"),
                "license": rec.get("license"),
                "storage_uri": (rec.get("storage") or {}).get("uri")}
            extra["_catalog_record"] = rec
        if verb == "gis_publish_layer":
            ref = args.get("dataset_ref") or ""
            if ref.startswith("catalog:"):
                rec = license_gate(ref[len("catalog:"):],
                                   args.get("purpose") or "research")
                extra["license_gate"] = {
                    "catalog_id": ref[len("catalog:"):],
                    "license": rec.get("license")}
            elif ref.startswith("postgis:"):
                extra["license_gate"] = {
                    "skipped": "非目录数据（postgis 表），无目录许可记录，"
                               "发布方自担许可口径"}
            else:
                raise GatewayReject(
                    "INVALID_ARGUMENT",
                    "dataset_ref 须带前缀 catalog:<id> 或 postgis:<表名>，"
                    "收到 %r" % (ref,))

        # 分级确认门
        if level == "R3":
            r3_gate(verb, backend, args)
        else:
            require_confirm(verb, level, spec, args,
                            raised=(level != spec["level"]))

        # 执行（个别动词有专属参数翻译）
        if verb == "gis_add_layer_from_catalog":
            payload = _exec_add_layer_from_catalog(backend, mapping, args,
                                                   extra)
        elif verb == "gis_publish_layer":
            payload = _exec_publish_layer(backend, mapping, args, extra)
        elif verb == "gis_query_observations":
            payload = _exec_query_observations(backend, mapping, args,
                                               variant_key)
        elif verb == "gis_list_services":
            payload = _exec_list_services(backend, mapping, args)
        elif verb == "gis_export_map_image":
            if (args.get("format") or "png") == "pdf":
                raise NotSupported(
                    "各桥出图工具为 PNG 口径；PDF/批量图集类属 defer，"
                    "本波不开（设计 §2 V40）")
            payload = execute_mapping(verb, backend, mapping, args)
        elif verb == "gis_serve_vector_tile":
            res = execute_mapping(verb, backend, mapping, args)
            payload = {"content_type":
                       "application/vnd.mapbox-vector-tile",
                       "tile": {"z": args.get("z"), "x": args.get("x"),
                                "y": args.get("y")},
                       "encoding": "binary-handle（不进 JSON 文本面）",
                       "backend_result": res}
        else:
            payload = execute_mapping(verb, backend, mapping, args)

        return _decorate(verb, spec, backend, payload, level, mapping,
                         extra, variant_key)

    except NotSupported as e:
        out = {"ok": False, "error_code": "NOT_SUPPORTED", "message": str(e),
               "tool": verb, "supported_tools": UNIFIED_TOOLS}
        if backend in BACKEND_CONF:
            out.update(envelope(backend))
        return out
    except GatewayReject as e:
        out = {"ok": False, "error_code": e.code, "message": e.message,
               "tool": verb}
        out.update(e.extra)
        if backend in BACKEND_CONF:
            out.update(envelope(backend))
        return out
    except NativeCallError as e:
        return _merge_envelope(backend, e.payload)
    except BackendError as e:
        out = {"ok": False, "error_code": e.code, "message": e.message,
               "tool": verb}
        if backend in BACKEND_CONF:
            out.update(envelope(backend))
        return out


def _decorate(verb, spec, backend, payload, level, mapping, extra,
              variant_key=None):
    if not isinstance(payload, dict):
        payload = {"result": payload}
    out = dict(payload)
    out["verb"] = verb
    out["vid"] = spec["vid"]
    out["level"] = level
    if mapping and mapping.get("wheel"):
        out["wheel"] = mapping["wheel"]
    if mapping and mapping.get("note"):
        out["mapping_note"] = mapping["note"]
    if mapping and mapping.get("bridge_tool_status"):
        out["bridge_tool_status"] = mapping["bridge_tool_status"]
    if variant_key is not None:
        out["variant"] = variant_key
    if level == "R2":
        out["in_place"] = True
    if verb == "gis_assign_projection":
        out["metadata_only"] = True
    for k, v in extra.items():
        if not k.startswith("_"):
            out[k] = v
    return _merge_envelope(backend, out)


def _exec_add_layer_from_catalog(backend, mapping, args, extra):
    rec = extra["_catalog_record"]
    uri = (rec.get("storage") or {}).get("uri")
    if backend == "supermap":
        native_args = {"dataset": rec.get("id"), "confirm": True}
        if args.get("map"):
            native_args["map"] = args["map"]
    else:
        native_args = {"path": uri, "confirm": True}
        if args.get("map"):
            native_args["map"] = args["map"]
    return get_client(backend).call_tool(mapping["native"], native_args)


def _exec_publish_layer(backend, mapping, args, extra):
    ref = args.get("dataset_ref")
    workspace = args.get("workspace") or "gis-platform"
    native_args = {"dataset_ref": ref, "workspace": workspace,
                   "confirm": True}
    if args.get("style"):
        native_args["style"] = args["style"]
    res = get_client(backend).call_tool(mapping["native"], native_args)
    out = res if isinstance(res, dict) else {"result": res}
    out = dict(out)
    out["publication"] = {
        "service_backend": "geoserver", "dataset_ref": ref,
        "workspace": workspace,
        "chain": "REST 发布链 workspaces→stores→featuretypes/coverages"
                 "→layers/styles（桥侧发布工具 pending）",
        "writeback": {"status": "pending_catalog_support",
                      "note": "catalog 记录的 publication 回写位已在对象"
                              "模型 v0.2 定义，但 catalog_server 尚无回写"
                              "工具，本次未回写、不假装已回写"}}
    return out


def _exec_query_observations(backend, mapping, args, entity):
    native = mapping["native"]
    odata = {k: args[k] for k in ("filter", "top", "skip", "count",
                                  "expand", "select", "orderby")
             if args.get(k) is not None}
    if native == "istsos_list_things":
        native_args = dict(odata)
    elif native == "istsos_list_datastreams":
        native_args = dict(odata)
        if args.get("thing_id") is not None:
            native_args["thing_id"] = args["thing_id"]
    elif native == "istsos_get_observations":
        if args.get("datastream_id") is None:
            raise GatewayReject(
                "INVALID_ARGUMENT",
                "entity=Observations 须带 datastream_id（桥工具按流取观测）")
        native_args = {"datastream_id": args["datastream_id"]}
        native_args.update(odata)
    else:  # istsos_query_entities（桥侧 pending 通用实体查询）
        native_args = {"entity": entity}
        native_args.update(odata)
    return get_client(backend).call_tool(native, native_args)


def _exec_list_services(backend, mapping, args):
    if mapping["native"] == "geoserver_capabilities_summary":
        return get_client(backend).call_tool(
            mapping["native"], {"service": args.get("service") or "WMS"})
    return get_client(backend).call_tool(mapping["native"], {})


def dispatch(tool, args):
    if tool in VERBS:
        return dispatch_verb(tool, args)
    return dispatch_base(tool, args)


# ---------------- MCP 服务端外壳 ----------------

_STR = {"type": "string"}
BASE_TOOL_DEFS = [
    ("gis_ping", "统一入口：桥是否在线", {"backend": _STR}),
    ("gis_discover", "统一入口：能力协商 + 原生 discover 透传 + data_catalog 一节 + v0.2 治理节（gp_governance / processing_registry / postgis_templates / v02_verbs）", {"backend": _STR}),
    ("gis_project_info", "统一入口：工程概览（kind 按后端区分；catalog 后端回 project{kind:catalog}；postgis kind=database；geoserver/istsos kind=service）", {"backend": _STR}),
    ("gis_list_maps", "统一入口：列地图（ArcMap 返回数据框并标注；QGIS 返回空列表+注记；服务端后端无此概念）",
     {"backend": _STR}),
    ("gis_list_layers", "统一入口：列图层（map 可选；ArcMap 下 map 指数据框；QGIS 忽略 map；geoserver 用 workspace 前缀过滤）",
     {"backend": _STR, "map": dict(_STR, description="地图名（可选）"),
      "workspace": dict(_STR, description="工作区（可选，仅 geoserver）")}),
    ("gis_list_datasets", "统一入口：列数据集（核心对象 dataset）——supermap=工作空间数据源/数据集；catalog=平台目录登记数据集；postgis=数据库空间表；其余后端 NOT_SUPPORTED",
     {"backend": _STR, "datasource": dict(_STR, description="数据源别名（可选，仅 SuperMap）"),
      "type": dict(_STR, description="按类型过滤（可选，仅 catalog）"),
      "commercial_use": {"type": "boolean", "description": "按商用口径过滤（可选，仅 catalog）"}}),
    ("gis_set_layer_visible", "统一入口：视图级设图层显隐（可逆）",
     {"backend": _STR, "map": dict(_STR, description="地图名（可选）"),
      "layer": dict(_STR, description="图层名或下标"),
      "visible": {"type": "boolean", "description": "true=显示，false=隐藏"}}),
    ("gis_zoom_to_layer", "统一入口：视图级缩放；target={type: layer|dataset, id}，按后端翻译，翻译不了 NOT_SUPPORTED",
     {"backend": _STR, "map": dict(_STR, description="地图名（可选）"),
      "target": {"type": "object", "description": "缩放目标",
                 "properties": {"type": {"type": "string", "enum": ["layer", "dataset"]},
                                "id": _STR},
                 "required": ["type", "id"]},
      "datasource": dict(_STR, description="数据源别名（可选，仅 SuperMap 按数据集缩放时）")}),
]

_TYPEMAP = {"s": "string", "b": "boolean", "n": "number",
            "a": "array", "o": "object"}


def _verb_tool_defs():
    defs = []
    for verb in VERB_ORDER:
        spec = VERBS[verb]
        props = {}
        for pname, ptype in spec["params"].items():
            props[pname] = {"type": _TYPEMAP[ptype]}
        props["backend"] = dict(_STR, description="后端：%s"
                                % ", ".join(sorted(spec["backends"].keys())))
        defs.append((verb,
                     "[%s/%s] %s" % (spec["vid"], spec["level"],
                                     spec["semantics"]),
                     props))
    return defs


TOOL_DEFS = BASE_TOOL_DEFS + _verb_tool_defs()


def tools_list():
    out = []
    for name, desc, props in TOOL_DEFS:
        required = ["backend"]
        if name == "gis_set_layer_visible":
            required += ["layer", "visible"]
        elif name == "gis_zoom_to_layer":
            required += ["target"]
        out.append({"name": name, "description": desc,
                    "inputSchema": {"type": "object", "properties": props,
                                    "required": required}})
    return out


def _wrap(mid, payload):
    return {"jsonrpc": "2.0", "id": mid, "result": {
        "content": [{"type": "text",
                     "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
        "isError": payload.get("ok") is False,
        "structuredContent": payload}}


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools_list()}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        if name not in UNIFIED_TOOLS:
            payload = {"ok": False, "error_code": "NOT_SUPPORTED",
                       "message": "统一入口 v0.3 不提供 %s。工具面为基础 "
                                  "8 动词 + 第一波 40 动词（见 gis_discover）；"
                                  "裸 SQL、厂商专属能力与未列名调用一律 "
                                  "NOT_SUPPORTED，不静默降级。" % name,
                       "tool": name, "supported_tools": UNIFIED_TOOLS}
            return _wrap(mid, payload)
        return _wrap(mid, dispatch(name, args))
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": "method not found: %s" % method}}


def _lock_stdio_utf8():
    for _name in ("stdout", "stdin"):
        _stream = getattr(sys, _name, None)
        _buf = getattr(_stream, "buffer", None)
        if _buf is None or getattr(_stream, "encoding", None) == "utf-8":
            continue
        try:
            setattr(sys, _name, io.TextIOWrapper(_buf, encoding="utf-8",
                                                 errors="replace"))
        except Exception:
            pass


def main():
    _lock_stdio_utf8()
    log("starting v0.3; backends=%s tools=%d" % (", ".join(BACKENDS),
                                                 len(UNIFIED_TOOLS)))
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception as e:
            log("bad json:", e)
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

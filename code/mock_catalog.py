# -*- coding: utf-8 -*-
"""
mock_catalog.py — 自检用假数据目录后端（纯标准库 stdio MCP 服务端）。

冒充 data-catalog/catalog_server.py：只提供 gis_catalog_list /
gis_catalog_describe 两工具，回 3 条罐头登记记录（commercial_use 分别为
true / false / "unknown"，专为测许可闸与网关 discover 聚合而设）。
counts / annotate / 许可闸逻辑与真实 catalog_server 同口径（复制其实现，
不 import——保持自检替身独立）。每次调用把 {tool, args} 追加写到 --log
指定的 JSONL 文件，自检据此断言网关确实经 stdio 实时调用、计数不是写死的。
它不读真实 catalog.json、不连任何数据源——自检证据等级是「离线协议自检」。
"""
import json
import sys

LOG_PATH = None
for i, a in enumerate(sys.argv):
    if a == "--log":
        LOG_PATH = sys.argv[i + 1]

PROTOCOL_VERSION = "2024-11-05"
CATALOG_TITLE = "GIS 平台数据目录（mock）"
INDEX_UPDATED_AT = "2026-11-02T00:00:00Z"


def _rec(did, typ, lic_name, cu):
    return {
        "id": did,
        "name": {"en": "Mock %s" % did, "zh": "自检罐头 %s" % did},
        "type": typ,
        "source": {"provider": "Mock", "url": "mock://%s" % did,
                   "retrieved_at": "2026-11-02", "upstream": "selftest"},
        "license": {"name": lic_name, "commercial_use": cu,
                    "attribution": "mock attribution",
                    "evidence_ref": "mock://evidence/%s" % did},
        "coverage": {"bbox": None, "crs": "unknown", "temporal_start": "unknown",
                     "temporal_end": "unknown", "region_name": "mock"},
        "format": {"name": "mock", "spec": "canned record"},
        "update": {"frequency": "unknown", "last_checked": "2026-11-02",
                   "upstream_version": "unknown"},
        "storage": {"uri": "mock://data/%s" % did, "size_bytes": None,
                    "checksum": None},
        "quality_notes": "罐头记录，仅自检用，不是真实登记",
        "status": "registered",
    }


RECORDS = [
    _rec("mock-dem", "dem", "Mock Public Domain", True),
    _rec("mock-restricted", "vector", "Mock Restricted License", False),
    _rec("mock-unknown-license", "raster", "Mock Unknown License", "unknown"),
]
BY_ID = {r["id"]: r for r in RECORDS}


def counts(records):
    by_type, by_license, by_cu = {}, {}, {}
    for r in records:
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1
        lic = r["license"]
        by_license[lic["name"]] = by_license.get(lic["name"], 0) + 1
        k = str(lic.get("commercial_use"))
        by_cu[k] = by_cu.get(k, 0) + 1
    return {"total": len(records), "by_type": by_type,
            "by_license": by_license, "by_commercial_use": by_cu}


def annotate(record):
    """与 catalog_server.annotate 同口径：许可闸写进回包结构。"""
    out = dict(record)
    cu = record["license"].get("commercial_use")
    out["license_gate"] = {
        "commercial_use": cu,
        "notice": ("许可：%s；commercial_use=%s。Agent 不得默认可商用，"
                   "引用许可结论时带 license.evidence_ref。"
                   % (record["license"]["name"], cu)) if cu is not True else
                  ("许可：%s；commercial_use=true（义务见 license.attribution）。"
                   % record["license"]["name"]),
    }
    if cu is not True:
        out["commercial_use_notice"] = \
            "commercial_use != true：该数据集不得默认用于商业用途"
    return out


def tool_list(args):
    args = args or {}
    recs = RECORDS
    if args.get("type"):
        recs = [r for r in recs if r["type"] == args["type"]]
    if args.get("commercial_use") in (True, False):
        recs = [r for r in recs
                if r["license"].get("commercial_use") is args["commercial_use"]]
    return {"catalog": CATALOG_TITLE, "index_updated_at": INDEX_UPDATED_AT,
            "count": len(recs), "counts": counts(RECORDS),
            "datasets": [annotate(r) for r in recs],
            "note": "mock 罐头索引，仅自检用"}


def tool_describe(args):
    args = args or {}
    did = args.get("id")
    if not did:
        return {"ok": False, "error_code": "INVALID_ARGUMENT",
                "message": "gis_catalog_describe 需要参数 id",
                "available_ids": sorted(BY_ID)}
    rec = BY_ID.get(did)
    if rec is None:
        return {"ok": False, "error_code": "DATASET_NOT_FOUND",
                "message": "目录中没有 id=%r 的数据集" % did,
                "available_ids": sorted(BY_ID)}
    return annotate(rec)


TOOLS = {"gis_catalog_list": tool_list, "gis_catalog_describe": tool_describe}


def record(tool, args):
    if LOG_PATH:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tool": tool, "args": args},
                               ensure_ascii=False) + "\n")


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
            "serverInfo": {"name": "gis-data-catalog-mock", "version": "0.0.1"}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        tools = [{"name": n, "description": "mock catalog",
                  "inputSchema": {"type": "object", "properties": {}}}
                 for n in TOOLS]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name")
        args = params.get("arguments") or {}
        record(name, args)
        if name not in TOOLS:
            return _wrap(mid, {"ok": False, "error_code": "NOT_SUPPORTED",
                               "message": "mock catalog 只提供 gis_catalog_list / "
                                          "gis_catalog_describe，不提供 %s" % name,
                               "tool": name})
        return _wrap(mid, TOOLS[name](args))
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601, "message": "method not found: %s" % method}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except Exception:
            continue
        resp = handle(msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()

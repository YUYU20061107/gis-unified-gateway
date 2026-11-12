# -*- coding: utf-8 -*-
"""
catalog_server.py — 平台级数据目录服务端（B 阶段，stdio MCP，纯标准库）

与四家 GIS 桥并列的第五个后端（网关 backends.json 里 backend 名 catalog）：
登记的是「平台里有什么数据、能不能用、在哪」，不是任何厂商工作空间的现场状态
（与 A 阶段 gis_list_datasets 的数据源/数据集概念不是一回事，见 PHASE-B §先分清）。

对外两工具：
  gis_catalog_list      列登记数据集（可按 type / commercial_use 过滤），
                        每条带许可标注；commercial_use != true 的条目显式打
                        commercial_use_notice（许可闸写进回包结构，不靠口头约定）
  gis_catalog_describe  按 id 返回单条完整登记记录 + license_gate

数据源：优先读同目录 catalog.json（build_catalog.py 由 datasets/*/dataset.json
汇总生成）；catalog.json 不在时回退直扫 datasets/（index_updated_at 为 null 并附注）。
只登记、不搬运：storage.uri 指上游官方入口，本服务端不下载任何数据本体。

登记状态口径：status=registered 表示仅登记、未打开本体验证过；只有实际打开验过
结构的条目才许标 verified（本批 9 条均为 registered）。
日志写 stderr，stdout 只走 MCP 协议（与各桥同口径）。
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "gis-data-catalog"
SERVER_VERSION = "0.1.0"
CATALOG_TITLE = "GIS 平台数据目录（data-catalog）"

REQUIRED_FIELDS = ["id", "name", "type", "source", "license", "coverage",
                   "format", "update", "storage", "quality_notes", "status"]


def log(*a):
    print("[gis-catalog]", *a, file=sys.stderr, flush=True)


def _load():
    """返回 (records, index_updated_at)。catalog.json 优先，缺失时直扫 datasets/。"""
    idx_path = os.path.join(HERE, "catalog.json")
    if os.path.exists(idx_path):
        with open(idx_path, encoding="utf-8") as f:
            idx = json.load(f)
        return idx.get("datasets", []), idx.get("generated_at")
    records = []
    base = os.path.join(HERE, "datasets")
    for did in sorted(os.listdir(base)):
        p = os.path.join(base, did, "dataset.json")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                records.append(json.load(f))
    return records, None


RECORDS, INDEX_UPDATED_AT = _load()
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
    """许可闸：回包条目自带许可标注，商用口径非 true 时显式提醒。"""
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
    out = {"catalog": CATALOG_TITLE, "index_updated_at": INDEX_UPDATED_AT,
           "count": len(recs), "counts": counts(RECORDS),
           "datasets": [annotate(r) for r in recs],
           "note": "登记索引（status=registered 仅登记、未打开本体验证）；"
                   "许可结论引用时带每条的 license.evidence_ref"}
    if INDEX_UPDATED_AT is None:
        out["index_note"] = "catalog.json 未生成，本次直扫 datasets/ 登记文件"
    return out


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


TOOLS = {
    "gis_catalog_list": ("列平台数据目录的登记数据集（可按 type / commercial_use 过滤）；"
                         "每条带许可标注，commercial_use != true 显式打标", tool_list),
    "gis_catalog_describe": ("按 id 返回单条数据集的完整登记记录（含许可闸 license_gate）",
                             tool_describe),
}


def tools_list():
    schemas = {
        "gis_catalog_list": {"type": "object", "properties": {
            "type": {"type": "string",
                     "description": "按类型过滤（可选）：vector/raster/imagery/dem/poi/network/table"},
            "commercial_use": {"type": "boolean",
                               "description": "按商用口径过滤（可选）"}}},
        "gis_catalog_describe": {"type": "object",
                                 "properties": {"id": {"type": "string",
                                                       "description": "数据集 id"}},
                                 "required": ["id"]},
    }
    return [{"name": n, "description": d, "inputSchema": schemas[n]}
            for n, (d, _fn) in TOOLS.items()]


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
        if name not in TOOLS:
            return _wrap(mid, {"ok": False, "error_code": "NOT_SUPPORTED",
                               "message": "数据目录服务端只提供 gis_catalog_list / "
                                          "gis_catalog_describe，不提供 %s" % name,
                               "tool": name})
        return _wrap(mid, TOOLS[name][1](params.get("arguments") or {}))
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
    log("starting; %d datasets registered, index_updated_at=%s"
        % (len(RECORDS), INDEX_UPDATED_AT))
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

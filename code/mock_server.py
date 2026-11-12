# -*- coding: utf-8 -*-
"""
mock_server.py — 自检用通用假后端（纯标准库 stdio MCP 服务端）。

用法：mock_server.py --backend <name> --tools mock_tools.json [--log path]
提供的工具名取自 mock_tools.json 中该后端的清单（由 build_mapping.py 从
全部映射汇出，保证 mock 面与映射面一致）。每次调用把 {tool, args} 追加
写到 --log 的 JSONL 文件，自检据此断言网关翻译。回包为罐头数据：默认回
{ok, mock, tool, echo_args}；少数工具按网关消费形态特判（list_maps /
list_dataframes 回列表、postgis 预检探针回结构化摘要、模板执行回显
sql+params 供断言参数化）。
它不连任何真实 GIS 软件/数据库——自检证据等级是「离线协议自检」。
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BACKEND = "mock"
TOOLS_FILE = os.path.join(HERE, "mock_tools.json")
LOG_PATH = None
for i, a in enumerate(sys.argv):
    if a == "--backend":
        BACKEND = sys.argv[i + 1]
    if a == "--tools":
        TOOLS_FILE = sys.argv[i + 1]
    if a == "--log":
        LOG_PATH = sys.argv[i + 1]

with open(TOOLS_FILE, encoding="utf-8") as f:
    TOOLS = json.load(f).get(BACKEND, [])

PROTOCOL_VERSION = "2024-11-05"


def canned(name, args):
    short = name.split("_", 1)[1] if "_" in name else name
    if short in ("list_maps",):
        return [{"name": "MockMap", "type": "map"}]
    if short in ("list_dataframes",):
        return [{"name": "MockFrame", "layer_count": 2}]
    if name == "postgis_table_summary":
        return {"table": args.get("table"), "row_count": 42,
                "extent": [0, 0, 10, 10], "mock": True}
    if name == "postgis_table_columns":
        return {"table": args.get("table"),
                "columns": [{"name": "id", "type": "integer"},
                            {"name": "geom", "type": "geometry"},
                            {"name": "name", "type": "text"}],
                "mock": True}
    if name == "postgis_list_spatial_tables":
        return [{"table": "roads", "geometry_column": "geom",
                 "type": "LineString", "srid": 4326},
                {"table": "parcels", "geometry_column": "geom",
                 "type": "Polygon", "srid": 4326}]
    if name == "postgis_exec_template":
        return {"ok": True, "mock": True, "applied_template":
                args.get("template_id"), "sql": args.get("sql"),
                "params": args.get("params")}
    if name == "arcgis_run_gp":
        return {"ok": True, "mock": True, "executed_tool": args.get("tool"),
                "via_verb": args.get("via_verb")}
    if name == "arcgis_list_tables":
        return [{"name": "roads"}, {"name": "parcels"}]
    if name == "qgis_run_processing":
        return {"ok": True, "mock": True,
                "ran_algorithm": args.get("algorithm")}
    if name == "qgis_list_fields":
        return [{"name": "id", "type": "integer"},
                {"name": "name", "type": "string"}]
    if name == "geoserver_publish_layer":
        return {"ok": True, "mock": True, "published": True,
                "layer": args.get("dataset_ref"),
                "workspace": args.get("workspace"),
                "endpoints": {"wms": "mock://geoserver/wms",
                              "wfs": "mock://geoserver/wfs"}}
    if name == "istsos_service_root":
        return {"mock": True, "entities": [
            "Things", "Locations", "HistoricalLocations", "Datastreams",
            "Sensors", "ObservedProperties", "Observations",
            "FeaturesOfInterest"]}
    if name == "istsos_query_entities":
        return {"mock": True, "entity": args.get("entity"), "items": []}
    if short in ("discover",):
        return {"mock": True, "mode": "mock-live", "workspace_open": True}
    if short in ("workspace_info",):
        return {"mock": True, "kind": "workspace", "datasource_count": 1,
                "map_count": 1}
    if short in ("project_info",):
        return {"mock": True, "kind": "project", "layer_count": 2}
    if short in ("document_info",):
        return {"mock": True, "kind": "document", "dataframe_count": 1}
    if short in ("list_layers",):
        return [{"index": 0, "name": "roads", "visible": True},
                {"index": 1, "name": "water", "visible": False}]
    if short in ("list_datasources",):
        return [{"alias": "ds1", "engine": "mock"}]
    if short in ("list_datasets",):
        return [{"name": "roads_ds", "datasource": "ds1"}]
    if short in ("zoom_to_layer",):
        return {"mock": True, "zoomed": "layer"}
    if short in ("zoom_to_dataset",):
        return {"mock": True, "zoomed": "dataset"}
    return {"ok": True, "mock": True, "tool": name, "echo_args": args}


def record(tool, args):
    if LOG_PATH:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps({"tool": tool, "args": args},
                               ensure_ascii=False) + "\n")


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "%s-mock-bridge" % BACKEND,
                           "version": "0.0.1"}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        tools = [{"name": n, "description": "mock",
                  "inputSchema": {"type": "object", "properties": {}}}
                 for n in TOOLS]
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": tools}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name") or ""
        args = params.get("arguments") or {}
        record(name, args)
        if name not in TOOLS:
            payload = {"ok": False, "error_code": "UNKNOWN_TOOL",
                       "message": "mock(%s) has no tool: %s" % (BACKEND, name)}
            return {"jsonrpc": "2.0", "id": mid, "result": {
                "content": [{"type": "text",
                             "text": json.dumps(payload, ensure_ascii=False)}],
                "isError": True, "structuredContent": payload}}
        payload = canned(name, args)
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text",
                         "text": json.dumps(payload, ensure_ascii=False)}],
            "isError": False, "structuredContent": payload}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601,
                      "message": "method not found: %s" % method}}


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

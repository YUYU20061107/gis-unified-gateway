# -*- coding: utf-8 -*-
"""iserver_server.py — SuperMap iServer 只读 REST 适配（stdio MCP，纯标准库）。

证据等级：demo-instance-verified（官方公开演示实例，非本机，版本未确认）。
只允许 GET；本文件不实现任何 POST/PUT/DELETE，也不调用管理接口。

已由探针确认的面：
  GET /iserver/services.json                    200（115 个服务）
  GET /services/map-china/rest/maps.json        200（4 个地图）
  GET /services/map-china/rest/maps/China.json  200（地图元数据）
  GET /services/map-china/rest/maps/China/layers.json 200（1 顶层/13 子层）

未确认的面（演示实例 502，不登记）：
  data-*/rest/datasets.json
  spatialanalyst-*/restjsr
"""
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("GIS_ISERVER_BASE",
                      "https://iserver.supermap.io/iserver").rstrip("/")
DEFAULT_MAP_SERVICE = os.environ.get("GIS_ISERVER_MAP_SERVICE", "map-china")
DEFAULT_MAP = os.environ.get("GIS_ISERVER_MAP", "China")
DEFAULT_DATA_SERVICE = os.environ.get("GIS_ISERVER_DATA_SERVICE", "data-china")
DEFAULT_DATASOURCE = os.environ.get("GIS_ISERVER_DATASOURCE", "China")
PROTOCOL_VERSION = "2024-11-05"
SERVICE_RE = re.compile(r"^[A-Za-z0-9_.-]+$")
_TOOLS = ["iserver_ping", "iserver_discover", "iserver_project_info",
          "iserver_list_maps", "iserver_list_layers", "iserver_list_datasets",
          "iserver_list_services"]


def _fail(code, message, **extra):
    d = {"ok": False, "error_code": code, "message": message}
    d.update(extra)
    return d


def _get_json(path, timeout=30):
    if not path.startswith("/"):
        return _fail("INVALID_ARGUMENT", "只接受 / 开头的白名单路径")
    url = BASE + path
    req = urllib.request.Request(
        url, method="GET",
        headers={"Accept": "application/json",
                 "User-Agent": "gis-unified-gateway-iserver-probe/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            status = r.status
            ctype = r.headers.get("Content-Type", "")
    except urllib.error.HTTPError as e:
        body = e.read()
        return _fail("ISERVER_HTTP_ERROR",
                     "iServer 返回 HTTP %s" % e.code,
                     http_status=e.code, url=url,
                     body_snippet=body[:300].decode("utf-8", "replace"))
    except Exception as e:  # noqa: BLE001
        return _fail("ISERVER_NETWORK_ERROR", "%s: %s" % (type(e).__name__, e),
                     url=url)
    try:
        data = json.loads(body.decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        return _fail("ISERVER_JSON_ERROR", "响应不是 JSON: %s" % e,
                     url=url, http_status=status,
                     body_snippet=body[:300].decode("utf-8", "replace"))
    return {"ok": True, "http_status": status, "url": url,
            "bytes": len(body), "content_type": ctype, "data": data}


def _services():
    r = _get_json("/services.json")
    if not r.get("ok"):
        return None, r
    data = r["data"]
    if not isinstance(data, list):
        return None, _fail("ISERVER_SHAPE_ERROR",
                           "services.json 不是服务数组")
    return data, None


def _component_counts(services):
    counts = {}
    for s in services:
        c = (s.get("componentType") or "").rsplit(".", 1)[-1]
        counts[c] = counts.get(c, 0) + 1
    return counts


def _service_name(value, label):
    if value is None:
        return None, None
    s = str(value)
    if not SERVICE_RE.match(s):
        return None, _fail("INVALID_ARGUMENT",
                           "%s 只允许字母数字/下划线/点/中划线" % label)
    return s, None


def iserver_ping(args):
    services, err = _services()
    if err:
        return err
    return {"ok": True, "read_only": True,
            "evidence": "demo-instance-verified",
            "base": BASE, "service_count": len(services),
            "note": "官方公开演示实例；非本机；版本未确认；仅 GET"}


def iserver_discover(args):
    services, err = _services()
    if err:
        return err
    counts = _component_counts(services)
    return {"ok": True, "read_only": True,
            "evidence": "demo-instance-verified",
            "base": BASE, "service_count": len(services),
            "component_counts": counts,
            "map_services": counts.get("MapImpl", 0),
            "data_services": counts.get("DataImpl", 0),
            "spatial_analyst_services": counts.get("SpatialAnalystImpl", 0),
            "default_map_service": DEFAULT_MAP_SERVICE,
            "default_map": DEFAULT_MAP,
            "default_data_service": DEFAULT_DATA_SERVICE,
            "default_datasource": DEFAULT_DATASOURCE,
            "note": "services.json、map-china REST、data-china 数据集 REST "
                    "已探针确认；spatialanalyst 根/子资源形状已确认，"
                    "执行未尝试（仅 GET）；全部只读"}


def iserver_project_info(args):
    services, err = _services()
    if err:
        return err
    return {"ok": True, "object": "project", "kind": "service",
            "read_only": True, "evidence": "demo-instance-verified",
            "base": BASE, "service_count": len(services),
            "component_counts": _component_counts(services),
            "note": "iServer 服务端无工程概念：以服务目录作概览"}


def iserver_list_datasets(args):
    data_service = args.get("data_service") or DEFAULT_DATA_SERVICE
    data_service, err = _service_name(data_service, "data_service")
    if err:
        return err
    datasource = args.get("datasource") or DEFAULT_DATASOURCE
    datasource, err = _service_name(datasource, "datasource")
    if err:
        return err
    r = _get_json("/services/%s/rest/data/datasources.json" % data_service)
    if not r.get("ok"):
        return r
    names = (r["data"] or {}).get("datasourceNames") or []
    if datasource not in names:
        return _fail("DATASOURCE_NOT_FOUND",
                     "数据源 %s 不在 %s 的 datasources 中：%s"
                     % (datasource, data_service, names),
                     url=r.get("url"))
    r2 = _get_json(
        "/services/%s/rest/data/datasources/name/%s/datasets.json"
        % (data_service, datasource))
    if not r2.get("ok"):
        return r2
    d = r2["data"] or {}
    names = d.get("datasetNames") or []
    return {"ok": True, "read_only": True,
            "evidence": "demo-instance-verified",
            "data_service": data_service, "datasource": datasource,
            "dataset_count": d.get("datasetCount", len(names)),
            "datasets": names}


def iserver_list_services(args):
    services, err = _services()
    if err:
        return err
    filt = args.get("service")
    ctype = args.get("component_type")
    rows = []
    for s in services:
        alias = s.get("alias") or ""
        name = s.get("name") or ""
        comp = (s.get("componentType") or "").rsplit(".", 1)[-1]
        if filt and filt not in alias and filt not in name:
            continue
        if ctype and comp != ctype:
            continue
        rows.append({
            "alias": alias,
            "name": name,
            "component_type": comp,
            "interface_type": (s.get("interfaceType") or "").rsplit(".", 1)[-1],
            "url": s.get("url"),
            "status": s.get("status"),
            "additions_count": len(s.get("additions") or []),
            "additions_sample": (s.get("additions") or [])[:5],
        })
    return {"ok": True, "read_only": True,
            "evidence": "demo-instance-verified",
            "base": BASE, "total": len(services),
            "returned": len(rows),
            "services": rows[:200],
            "truncated": len(rows) > 200}


def iserver_list_maps(args):
    service = args.get("service") or DEFAULT_MAP_SERVICE
    service, err = _service_name(service, "service")
    if err:
        return err
    r = _get_json("/services/%s/rest/maps.json" % service)
    if not r.get("ok"):
        return r
    data = r["data"]
    if not isinstance(data, list):
        return _fail("ISERVER_SHAPE_ERROR", "maps.json 不是数组",
                     url=r.get("url"))
    maps = [{"name": m.get("name"), "path": m.get("path"),
             "resource_type": m.get("resourceType")}
            for m in data if isinstance(m, dict)]
    return {"ok": True, "read_only": True,
            "evidence": "demo-instance-verified",
            "service": service, "total": len(maps), "maps": maps}


def iserver_list_layers(args):
    service = args.get("service") or DEFAULT_MAP_SERVICE
    service, err = _service_name(service, "service")
    if err:
        return err
    map_name = args.get("map") or DEFAULT_MAP
    map_name, err = _service_name(map_name, "map")
    if err:
        return err
    r = _get_json("/services/%s/rest/maps/%s/layers.json"
                  % (service, map_name))
    if not r.get("ok"):
        return r
    data = r["data"]
    if not isinstance(data, list):
        return _fail("ISERVER_SHAPE_ERROR", "layers.json 不是数组",
                     url=r.get("url"))
    layers = []
    for i, layer in enumerate(data):
        if not isinstance(layer, dict):
            continue
        sub = (layer.get("subLayers") or {}).get("layers") or []
        layers.append({
            "index": i,
            "name": layer.get("name"),
            "caption": layer.get("caption"),
            "visible": layer.get("visible"),
            "sublayer_count": len(sub),
        })
    return {"ok": True, "read_only": True,
            "evidence": "demo-instance-verified",
            "service": service, "map": map_name,
            "total": len(layers), "layers": layers}


_HANDLERS = {
    "iserver_ping": iserver_ping,
    "iserver_discover": iserver_discover,
    "iserver_project_info": iserver_project_info,
    "iserver_list_maps": iserver_list_maps,
    "iserver_list_layers": iserver_list_layers,
    "iserver_list_datasets": iserver_list_datasets,
    "iserver_list_services": iserver_list_services,
}


def _tool_defs():
    return [{"name": n, "description": "iServer GET-only demo backend tool",
             "inputSchema": {"type": "object", "properties": {}}}
            for n in _TOOLS]


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "iserver-demo-bridge",
                           "version": "0.1.0"}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid,
                "result": {"tools": _tool_defs()}}
    if method == "tools/call":
        params = msg.get("params") or {}
        name = params.get("name") or ""
        args = params.get("arguments") or {}
        if name not in _HANDLERS:
            payload = _fail("UNKNOWN_TOOL", "iserver 没有工具：%s" % name)
        else:
            try:
                payload = _HANDLERS[name](args)
            except Exception as e:  # noqa: BLE001
                payload = _fail("ISERVER_EXEC_ERROR", "%s: %s" % (name, e))
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text",
                         "text": json.dumps(payload, ensure_ascii=False)}],
            "isError": payload.get("ok") is False,
            "structuredContent": payload}}
    return {"jsonrpc": "2.0", "id": mid,
            "error": {"code": -32601,
                      "message": "method not found: %s" % method}}


def _lock_stdio_utf8():
    for name in ("stdout", "stdin"):
        stream = getattr(sys, name, None)
        buf = getattr(stream, "buffer", None)
        if buf is None or getattr(stream, "encoding", None) == "utf-8":
            continue
        try:
            setattr(sys, name, io.TextIOWrapper(
                buf, encoding="utf-8", errors="replace"))
        except Exception:  # noqa: BLE001
            pass


def main():
    _lock_stdio_utf8()
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

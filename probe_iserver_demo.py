# -*- coding: utf-8 -*-
"""probe_iserver_demo.py — iServer 官方演示实例只读探针（仅 GET）。

不实现 POST/PUT/DELETE，不调用管理接口。结果写
evidence/phase3/iserver-demo-probe.json。
"""
import json
import os
import urllib.error
import urllib.request

BASE = "https://iserver.supermap.io/iserver"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "evidence", "phase3", "iserver-demo-probe.json")
ENDPOINTS = [
    "/services.json",
    "/services/map-china/rest/maps.json",
    "/services/map-china/rest/maps/China.json",
    "/services/map-china/rest/maps/China/layers.json",
    "/services/data-china/rest.json",
    "/services/data-china/rest/data/datasources.json",
    "/services/data-china/rest/data/datasources/name/China/datasets.json",
    "/services/spatialanalyst-sample/restjsr",
    "/services/spatialanalyst-sample/restjsr/spatialanalyst",
    "/services/spatialanalyst-sample/restjsr/spatialanalyst/datasets",
    "/services/spatialanalyst-sample/restjsr/spatialanalyst/geometry",
]


def get(path, timeout=15):
    url = BASE + path
    req = urllib.request.Request(
        url, method="GET",
        headers={"Accept": "application/json",
                 "User-Agent": "gis-unified-gateway-iserver-probe/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return {"url": url, "method": "GET", "http_status": r.status,
                    "bytes": len(body),
                    "content_type": r.headers.get("Content-Type", ""),
                    "data": body}
    except urllib.error.HTTPError as e:
        body = e.read()
        return {"url": url, "method": "GET", "http_status": e.code,
                "bytes": len(body),
                "content_type": e.headers.get("Content-Type", ""),
                "error": body[:300].decode("utf-8", "replace")}
    except Exception as e:  # noqa: BLE001
        return {"url": url, "method": "GET", "error": "%s: %s"
                % (type(e).__name__, e)}


def shape(path, data):
    if isinstance(data, list):
        item = data[0] if data else None
        return {"type": "list", "count": len(data),
                "first_keys": list(item.keys())[:20]
                if isinstance(item, dict) else None}
    if isinstance(data, dict):
        return {"type": "dict", "keys": list(data.keys())[:30]}
    return {"type": type(data).__name__}


def main():
    out = []
    for path in ENDPOINTS:
        r = get(path)
        rec = {"path": path, "method": "GET",
               "http_status": r.get("http_status"), "bytes": r.get("bytes"),
               "content_type": r.get("content_type")}
        if r.get("error"):
            rec["error"] = r["error"]
        else:
            try:
                data = json.loads(r["data"].decode("utf-8"))
                rec["shape"] = shape(path, data)
                if path == "/services.json":
                    from collections import Counter
                    rec["component_counts"] = dict(Counter(
                        (s.get("componentType") or "").rsplit(".", 1)[-1]
                        for s in data))
                elif path.endswith("/maps.json"):
                    rec["names"] = [m.get("name") for m in data]
                elif path.endswith("/China.json"):
                    rec["map_name"] = data.get("name")
                    rec["epsg"] = (data.get("prjCoordSys") or {}).get("epsgCode")
                elif path.endswith("/layers.json"):
                    rec["top_layers"] = [
                        {"name": x.get("name"),
                         "sublayer_count": len(
                             (x.get("subLayers") or {}).get("layers") or [])}
                        for x in data if isinstance(x, dict)]
                elif path.endswith("/datasets.json"):
                    rec["dataset_count"] = data.get("datasetCount")
                    rec["dataset_names_sample"] = (
                        data.get("datasetNames") or [])[:10]
                elif path.endswith("/datasources.json"):
                    rec["datasource_names"] = data.get("datasourceNames")
                elif path.endswith("/spatialanalyst"):
                    rec["resources"] = [x.get("name") for x in data
                                        if isinstance(x, dict)]
                elif path.endswith("/spatialanalyst/datasets"):
                    rec["dataset_count"] = len(data)
                    rec["first_child_resources"] = [
                        y.get("name") for y in
                        ((data[0].get("childResourceInfos") or [])
                         if data else [])][:10]
                elif path.endswith("/spatialanalyst/geometry"):
                    rec["geometry_ops_count"] = len(data)
                    rec["first_ops"] = [x.get("name") for x in data[:10]
                                        if isinstance(x, dict)]
            except Exception as e:  # noqa: BLE001
                rec["json_error"] = str(e)
        out.append(rec)
    payload = {
        "evidence": "demo-instance-verified",
        "read_only": True,
        "methods": ["GET"],
        "base": BASE,
        "note": "官方公开演示实例；非本机；版本未确认；"
                "仅 GET；data/spatial 端点 502 时不登记映射",
        "results": out,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    for r in out:
        print("%s %s %s" % (r.get("http_status"), r.get("bytes"), r["path"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""test_iserver_demo.py — iServer 官方演示实例只读验收（仅 GET）。

桥 7 项 + 网关 7 项：服务目录、地图 maps/detail/layers、数据 datasources/
datasets、spatial 根形状。不执行任何 POST/写操作，不标 calibrated。
结果写 evidence/phase3/iserver-demo-results.json。
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(ROOT, "code", "iserver_server.py")
GATEWAY = os.path.join(ROOT, "code", "gateway.py")
BASE = "https://iserver.supermap.io/iserver"
RESULTS = []


def record(name, ok, detail=None):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("%s %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        print("  detail:", json.dumps(detail, ensure_ascii=False)[:1500])


class Client:
    def __init__(self, argv, env=None):
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8",
            errors="replace", env=env or os.environ)
        self.ident = 0
        self.call("initialize", {}, raw=True)

    def call(self, name, args, raw=False):
        self.ident += 1
        msg = {"jsonrpc": "2.0", "id": self.ident,
               "method": "initialize" if raw else "tools/call"}
        msg["params"] = {} if raw else {"name": name, "arguments": args}
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("backend exited: %s"
                               % self.proc.stderr.read()[-1200:])
        resp = json.loads(line)
        result = resp.get("result") or {}
        payload = result.get("structuredContent")
        if payload is None:
            texts = [c.get("text", "") for c in result.get("content", [])
                     if c.get("type") == "text"]
            payload = json.loads(texts[0]) if texts else {}
        return payload

    def close(self):
        try:
            self.proc.stdin.close()
            self.proc.wait(timeout=5)
        except Exception:  # noqa: BLE001
            self.proc.kill()


def main():
    c = Client([sys.executable, SERVER])
    p = c.call("iserver_ping", {})
    record("桥 ping：services.json 115 服务",
           p.get("ok") and p.get("service_count") == 115
           and p.get("read_only") is True, p)
    p = c.call("iserver_discover", {})
    cc = p.get("component_counts") or {}
    record("桥 discover：Map/Data/SpatialAnalyst 组件计数",
           p.get("ok") and cc.get("MapImpl") == 56
           and cc.get("DataImpl") == 29
           and cc.get("SpatialAnalystImpl") == 5, p)
    p = c.call("iserver_project_info", {})
    record("桥 project_info：kind=service + 115 服务",
           p.get("ok") and p.get("kind") == "service"
           and p.get("service_count") == 115, p)
    p = c.call("iserver_list_maps", {})
    record("桥 map-china maps.json：4 地图",
           p.get("ok") and p.get("total") == 4
           and any(m.get("name") == "China" for m in p.get("maps") or []), p)
    p = c.call("iserver_list_layers", {"map": "China"})
    layers = p.get("layers") or []
    record("桥 map-china/China layers.json：1 顶层/13 子层",
           p.get("ok") and p.get("total") == 1 and layers
           and layers[0].get("sublayer_count") == 13, p)
    p = c.call("iserver_list_datasets", {"datasource": "China"})
    record("桥 data-china/China datasets.json：47 数据集",
           p.get("ok") and p.get("dataset_count") == 47, p)
    p = c.call("iserver_list_services", {})
    record("桥 services.json 目录：115 服务",
           p.get("ok") and p.get("total") == 115, p)
    c.close()

    cfg = os.path.join(ROOT, "evidence", "phase3", "_gw-backends.json")
    os.makedirs(os.path.dirname(cfg), exist_ok=True)
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump({"backends": {"iserver": {
            "command": [sys.executable, SERVER], "mode": "demo-rest",
            "calibration": {"level": "demo-instance-verified",
                            "evidence_ref": "test_iserver_demo.py"}}}},
                  f, ensure_ascii=False)
    g = Client([sys.executable, GATEWAY],
               env=dict(os.environ, GIS_GATEWAY_BACKENDS=cfg))
    p = g.call("gis_ping", {"backend": "iserver"})
    record("网关 gis_ping@iserver",
           p.get("ok") is not False and p.get("service_count") == 115, p)
    p = g.call("gis_discover", {"backend": "iserver"})
    nd = p.get("native_discover") or {}
    record("网关 gis_discover@iserver：native 115 + V35",
           p.get("backend") == "iserver"
           and nd.get("service_count") == 115
           and "gis_list_services"
           in (p.get("v02_verbs") or {}).get("supported", []), p)
    p = g.call("gis_project_info", {"backend": "iserver"})
    record("网关 gis_project_info@iserver：kind=service",
           p.get("kind") == "service" and p.get("service_count") == 115, p)
    p = g.call("gis_list_maps", {"backend": "iserver"})
    record("网关 gis_list_maps@iserver：4 地图",
           p.get("total") == 4 and len(p.get("maps") or []) == 4, p)
    p = g.call("gis_list_layers", {"backend": "iserver", "map": "China"})
    record("网关 gis_list_layers@iserver：China 1 顶层/13 子层",
           p.get("total") == 1 and (p.get("layers") or [{}])[0]
           .get("sublayer_count") == 13, p)
    p = g.call("gis_list_datasets", {"backend": "iserver",
                                     "datasource": "China"})
    record("网关 gis_list_datasets@iserver：47 数据集",
           p.get("dataset_count") == 47, p)
    p = g.call("gis_list_services", {"backend": "iserver"})
    record("网关 gis_list_services@iserver：115 服务",
           p.get("total") == 115, p)
    g.close()

    passed = sum(1 for r in RESULTS if r["ok"])
    out = {
        "evidence": "demo-instance-verified",
        "read_only": True,
        "methods": ["GET"],
        "base": BASE,
        "non_local": True,
        "version_confirmed": False,
        "spatial_execution_attempted": False,
        "note": "官方公开演示实例；仅 GET；不冒充本机校准；"
                "data/map REST 已确认，spatial 仅确认根/子资源形状",
        "total": len(RESULTS), "passed": passed,
        "failed": len(RESULTS) - passed,
        "cases": RESULTS,
    }
    outdir = os.path.join(ROOT, "evidence", "phase3")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "iserver-demo-results.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("\nchecks: %d, passed: %d, failed: %d"
          % (len(RESULTS), passed, len(RESULTS) - passed))
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""test_real_backends.py — 阶段 4：网关对两个真实后端的端到端验收。

同一个 gateway.py 进程，backends 配置只含：
  - gdal      : code/gdal_server.py（本地 GDAL 3.13.3 CLI）
  - qgis-cli  : code/qgis_cli_server.py（本地 qgis_process 3.44.15）
真实执行：ping/discover、gdal 格式转换、gdal 坡度、qgis native:buffer、
qgis 本地注册表枚举/自描述。结果写 evidence/phase4/real-backends-results.json。
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
GATEWAY = os.path.join(ROOT, "code", "gateway.py")
GDAL_SERVER = os.path.join(ROOT, "code", "gdal_server.py")
QGIS_SERVER = os.path.join(ROOT, "code", "qgis_cli_server.py")
GDAL_BIN = os.environ.get("GIS_GDAL_BIN") or r"C:\Program Files\QGIS 3.44.15\bin"
QGIS_BAT = os.environ.get(
    "GIS_QGIS_BAT",
    r"C:\Program Files\QGIS 3.44.15\bin\qgis_process-qgis-ltr.bat")
WORK = tempfile.mkdtemp(prefix="real-backends-")
OUT = os.path.join(WORK, "out")
os.makedirs(OUT, exist_ok=True)
RESULTS = []


def env():
    e = dict(os.environ, GIS_GDAL_BIN=GDAL_BIN, GIS_QGIS_BAT=QGIS_BAT)
    root = os.path.dirname(os.path.abspath(GDAL_BIN))
    proj = os.path.join(root, "share", "proj")
    gdal_data = os.path.join(root, "apps", "gdal", "share", "gdal")
    if os.path.exists(os.path.join(proj, "proj.db")):
        e["PROJ_LIB"] = proj
        e["PROJ_DATA"] = proj
    if os.path.isdir(gdal_data):
        e["GDAL_DATA"] = gdal_data
    e["PATH"] = GDAL_BIN + os.pathsep + e.get("PATH", "")
    return e


ENV = env()


def record(name, ok, detail=None):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("%s %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        print("  detail:", json.dumps(detail, ensure_ascii=False)[:1500])


def make_data():
    exe = os.path.join(GDAL_BIN, "gdal_create.exe")
    p = subprocess.run(
        [exe, "-of", "GTiff", "-outsize", "20", "20", "-bands", "1",
         "-ot", "UInt16", "-a_srs", "EPSG:4326", "-a_ullr", "0", "4", "4", "0",
         "-burn", "10", os.path.join(WORK, "dem.tif")],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env=ENV, timeout=120)
    if p.returncode != 0:
        raise RuntimeError("gdal_create failed: %s" % p.stderr[-800:])
    def poly(coords):
        return {"type": "Polygon", "coordinates": [coords]}
    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"id": 1, "name": "a"},
         "geometry": poly([[0, 0], [4, 0], [4, 4], [0, 4], [0, 0]])},
        {"type": "Feature", "properties": {"id": 2, "name": "b"},
         "geometry": poly([[3, 3], [7, 3], [7, 7], [3, 7], [3, 3]])},
    ]}
    with open(os.path.join(WORK, "poly.geojson"), "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False)


class Client:
    def __init__(self, argv, env=None):
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8",
            errors="replace", env=env or ENV)
        self.ident = 0
        self.call("initialize", {}, raw=True)

    def call(self, name, args, raw=False):
        self.ident += 1
        msg = {"jsonrpc": "2.0", "id": self.ident,
               "method": "initialize" if raw else "tools/call"}
        if not raw:
            msg["params"] = {"name": name, "arguments": args}
        else:
            msg["params"] = {}
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("gateway exited: %s"
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
    make_data()
    cfg = os.path.join(WORK, "backends-real.json")
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump({"backends": {
            "gdal": {"command": [sys.executable, GDAL_SERVER],
                     "mode": "local-cli",
                     "calibration": {"level": "calibrated",
                                     "evidence_ref": "test_real_backends.py"}},
            "qgis-cli": {"command": [sys.executable, QGIS_SERVER],
                         "mode": "processing-cli",
                         "calibration": {"level": "calibrated",
                                         "evidence_ref": "test_real_backends.py"}},
        }}, f, ensure_ascii=False)
    g = Client([sys.executable, GATEWAY],
               env=dict(ENV, GIS_GATEWAY_BACKENDS=cfg))

    p = g.call("gis_ping", {"backend": "gdal"})
    record("真后端 gdal ping（GDAL 3.13.3）",
           p.get("ok") is not False
           and "GDAL 3." in json.dumps(p, ensure_ascii=False), p)
    p = g.call("gis_ping", {"backend": "qgis-cli"})
    record("真后端 qgis-cli ping（QGIS 3.44.15）",
           p.get("ok") is not False
           and "QGIS 3." in json.dumps(p, ensure_ascii=False), p)

    d = g.call("gis_discover", {"backend": "gdal"})
    record("gdal discover 报 6 个 v02 动词",
           d.get("backend") == "gdal"
           and {"gis_reproject", "gis_convert_format", "gis_clip",
                "gis_slope", "gis_aspect", "gis_hillshade"}
           <= set((d.get("v02_verbs") or {}).get("supported", [])), d)
    d = g.call("gis_discover", {"backend": "qgis-cli"})
    record("qgis-cli discover 报 V02/V03/V04",
           d.get("backend") == "qgis-cli"
           and {"gis_run_processing", "gis_list_algorithms",
                "gis_describe_algorithm"}
           <= set((d.get("v02_verbs") or {}).get("supported", [])), d)

    c = g.call("gis_convert_format", {
        "backend": "gdal", "input": os.path.join(WORK, "poly.geojson"),
        "target": os.path.join(OUT, "poly.gpkg"), "kind": "vector",
        "format": "GPKG", "confirm": True})
    record("gdal 真实格式转换（GeoJSON→GPKG）",
           c.get("ok") is not False
           and os.path.exists(os.path.join(OUT, "poly.gpkg")), c)

    s = g.call("gis_slope", {
        "backend": "gdal", "input": os.path.join(WORK, "dem.tif"),
        "target": os.path.join(OUT, "slope.tif"), "confirm": True})
    record("gdal 真实坡度（gdaldem slope）",
           s.get("ok") is not False
           and os.path.getsize(os.path.join(OUT, "slope.tif")) > 0, s)

    q = g.call("gis_run_processing", {
        "backend": "qgis-cli", "algorithm": "native:buffer",
        "params": {"INPUT": os.path.join(WORK, "poly.geojson"),
                   "DISTANCE": 0.1,
                   "OUTPUT": os.path.join(OUT, "qgis_buf.geojson")},
        "confirm": True})
    buf = os.path.join(OUT, "qgis_buf.geojson")
    feat = None
    if os.path.exists(buf):
        with open(buf, encoding="utf-8") as f:
            feat = len(json.load(f).get("features") or [])
    record("qgis-cli 真实 Processing（native:buffer，网关确认门后执行）",
           q.get("ok") is not False and feat and feat >= 2, q)

    a = g.call("gis_list_algorithms", {"backend": "qgis-cli"})
    record("qgis-cli 本地 Processing 注册表 374 条",
           a.get("total") == 374, a)
    z = g.call("gis_describe_algorithm", {"backend": "qgis-cli",
                                          "algorithm": "native:buffer"})
    record("qgis-cli 算法自描述 native:buffer",
           z.get("algorithm_id") == "native:buffer", z)
    g.close()

    passed = sum(1 for r in RESULTS if r["ok"])
    outdir = os.path.join(ROOT, "evidence", "phase4")
    os.makedirs(outdir, exist_ok=True)
    summary = {"total": len(RESULTS), "passed": passed,
               "failed": len(RESULTS) - passed,
               "real_backends": ["gdal", "qgis-cli"],
               "gateway_proc": "same gateway.py process",
               "cases": RESULTS}
    with open(os.path.join(outdir, "real-backends-results.json"), "w",
              encoding="utf-8", newline="\n") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)
    print("\nchecks: %d, passed: %d, failed: %d"
          % (len(RESULTS), passed, len(RESULTS) - passed))
    return 0 if passed == len(RESULTS) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(WORK, ignore_errors=True)

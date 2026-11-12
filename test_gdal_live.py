# -*- coding: utf-8 -*-
"""test_gdal_live.py — GDAL 后端真跑验收（不是离线 mock）。

建 20x20 GeoTIFF + 两个 GeoJSON 面夹具，起 code/gdal_server.py 走 stdio
MCP，逐工具断言；再起 gateway.py 用临时 backends 配置跑通 gdal 的
discover / convert_format / slope 三条端到端。结果写
evidence/phase2/gdal-live-results.json。
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.abspath(__file__))
SERVER = os.path.join(ROOT, "code", "gdal_server.py")
GATEWAY = os.path.join(ROOT, "code", "gateway.py")
BIN = os.environ.get("GIS_GDAL_BIN") or r"C:\Program Files\QGIS 3.44.15\bin"
WORK = tempfile.mkdtemp(prefix="gdal-live-")
OUT = os.path.join(WORK, "out")
os.makedirs(OUT, exist_ok=True)
RESULTS = []


def env_for_gdal():
    env = dict(os.environ)
    root = os.path.dirname(os.path.abspath(BIN))
    proj = os.path.join(root, "share", "proj")
    gdal_data = os.path.join(root, "apps", "gdal", "share", "gdal")
    if os.path.exists(os.path.join(proj, "proj.db")):
        env["PROJ_LIB"] = proj
        env["PROJ_DATA"] = proj
    if os.path.isdir(gdal_data):
        env["GDAL_DATA"] = gdal_data
    env["PATH"] = BIN + os.pathsep + env.get("PATH", "")
    return env


GDAL_ENV = env_for_gdal()


def record(name, ok, detail=None):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("%s %s" % ("PASS" if ok else "FAIL", name))
    if not ok:
        print("  detail:", json.dumps(detail, ensure_ascii=False)[:1200])


def cli(name, args):
    exe = os.path.join(BIN, name + ".exe")
    p = subprocess.run([exe] + args, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=GDAL_ENV,
                       timeout=120)
    if p.returncode != 0:
        raise RuntimeError("%s failed: %s" % (name, p.stderr[-1000:]))
    return p.stdout


def make_data():
    cli("gdal_create", ["-of", "GTiff", "-outsize", "20", "20", "-bands", "1",
                        "-ot", "UInt16", "-a_srs", "EPSG:4326",
                        "-a_ullr", "0", "4", "4", "0", "-burn", "10",
                        os.path.join(WORK, "dem.tif")])

    def poly(coords):
        return {"type": "Polygon", "coordinates": [coords]}

    fc = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"id": 1, "name": "a"},
         "geometry": poly([[0, 0], [4, 0], [4, 4], [0, 4], [0, 0]])},
        {"type": "Feature", "properties": {"id": 2, "name": "b"},
         "geometry": poly([[3, 3], [7, 3], [7, 7], [3, 7], [3, 3]])},
    ]}
    with open(os.path.join(WORK, "poly.geojson"), "w",
              encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False)
    clip = {"type": "FeatureCollection", "features": [
        {"type": "Feature", "properties": {"id": 9},
         "geometry": poly([[1, 1], [5, 1], [5, 5], [1, 5], [1, 1]])},
    ]}
    with open(os.path.join(WORK, "clip.geojson"), "w",
              encoding="utf-8") as f:
        json.dump(clip, f, ensure_ascii=False)


class Client:
    def __init__(self, argv, env=None):
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8",
            errors="replace", env=env or GDAL_ENV)
        self.ident = 0
        self.call("initialize", {}, raw=True)

    def call(self, name, args, raw=False):
        self.ident += 1
        msg = {"jsonrpc": "2.0", "id": self.ident,
               "method": "tools/call" if not raw else "initialize",
               "params": {"name": name, "arguments": args} if not raw else {}}
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            err = self.proc.stderr.read()
            raise RuntimeError("backend exited: %s" % err[-1000:])
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
    c = Client([sys.executable, SERVER])
    ping = c.call("gdal_ping", {})
    record("gdal_ping 返回真实 GDAL 版本",
           ping.get("ok") and str(ping.get("version", "")).startswith("GDAL 3."),
           ping)
    disc = c.call("gdal_discover", {})
    record("gdal_discover 返回版本 + 栅格/矢量驱动计数 + 工具面",
           disc.get("ok") and disc.get("raster_format_count", 0) > 0
           and disc.get("vector_format_count", 0) > 0
           and set(disc.get("tools") or []) == {
               "gdal_ping", "gdal_discover", "gdal_reproject",
               "gdal_convert_format", "gdal_clip", "gdal_slope",
               "gdal_aspect", "gdal_hillshade"}, disc)

    cvt = c.call("gdal_convert_format", {
        "input": os.path.join(WORK, "poly.geojson"),
        "target": os.path.join(OUT, "poly.gpkg"),
        "kind": "vector", "format": "GPKG"})
    record("V16 矢量 GeoJSON -> GPKG（真实 ogr2ogr）",
           cvt.get("ok") and os.path.exists(os.path.join(OUT, "poly.gpkg"))
           and (cvt.get("output") or {}).get("feature_count") == 2, cvt)

    rep = c.call("gdal_reproject", {
        "input": os.path.join(WORK, "poly.geojson"),
        "target": os.path.join(OUT, "poly3857.gpkg"),
        "kind": "vector", "target_srid": 3857})
    record("V15 矢量重投影到 EPSG:3857",
           rep.get("ok") and "Pseudo-Mercator" in
           ((rep.get("output") or {}).get("srs_wkt") or ""), rep)

    clip = c.call("gdal_clip", {
        "input": os.path.join(WORK, "poly.geojson"),
        "clip_by": os.path.join(WORK, "clip.geojson"),
        "target": os.path.join(OUT, "poly_clip.gpkg"),
        "input_type": "vector"})
    record("V19 矢量裁剪（真实 ogr2ogr -clipsrc）",
           clip.get("ok") and os.path.exists(os.path.join(OUT, "poly_clip.gpkg"))
           and (clip.get("output") or {}).get("feature_count", 0) >= 1, clip)

    cvt_r = c.call("gdal_convert_format", {
        "input": os.path.join(WORK, "dem.tif"),
        "target": os.path.join(OUT, "dem.png"),
        "kind": "raster", "format": "PNG"})
    record("V16 栅格 GeoTIFF -> PNG（真实 gdal_translate）",
           cvt_r.get("ok") and os.path.exists(os.path.join(OUT, "dem.png"))
           and (cvt_r.get("output") or {}).get("driver") == "PNG", cvt_r)

    rep_r = c.call("gdal_reproject", {
        "input": os.path.join(WORK, "dem.tif"),
        "target": os.path.join(OUT, "dem3857.tif"),
        "kind": "raster", "target_srid": 3857})
    record("V15 栅格重投影到 EPSG:3857",
           rep_r.get("ok") and "Pseudo-Mercator" in
           ((rep_r.get("output") or {}).get("srs_wkt") or ""), rep_r)

    clip_r = c.call("gdal_clip", {
        "input": os.path.join(WORK, "dem.tif"),
        "clip_by": os.path.join(WORK, "clip.geojson"),
        "target": os.path.join(OUT, "dem_clip.tif"),
        "input_type": "raster"})
    record("V19 栅格裁剪（真实 gdalwarp -cutline）",
           clip_r.get("ok")
           and os.path.getsize(os.path.join(OUT, "dem_clip.tif")) > 0, clip_r)

    for tool, op in (("gdal_slope", "slope"),
                     ("gdal_aspect", "aspect"),
                     ("gdal_hillshade", "hillshade")):
        r = c.call(tool, {"input": os.path.join(WORK, "dem.tif"),
                          "target": os.path.join(OUT, "%s.tif" % op)})
        record("%s 真实 gdaldem %s" % (tool, op),
               r.get("ok") and os.path.getsize(
                   os.path.join(OUT, "%s.tif" % op)) > 0
               and (r.get("output") or {}).get("driver") == "GTiff", r)

    neg = c.call("gdal_convert_format", {
        "input": os.path.join(WORK, "poly.geojson"),
        "target": os.path.join(OUT, "poly.gpkg"),
        "kind": "vector", "format": "GPKG"})
    record("写操作不覆盖已存在 target（TARGET_EXISTS）",
           neg.get("ok") is False and neg.get("error_code") == "TARGET_EXISTS",
           neg)
    neg2 = c.call("gdal_reproject", {
        "input": os.path.join(WORK, "poly.geojson"),
        "target": os.path.join(OUT, "table.gpkg"),
        "kind": "table", "target_srid": 3857})
    record("表重投影概念不适用（NOT_SUPPORTED）",
           neg2.get("ok") is False and neg2.get("error_code") == "NOT_SUPPORTED",
           neg2)
    c.close()

    # ---- 网关 -> GDAL 真后端端到端 ----
    cfg = os.path.join(WORK, "backends-gdal.json")
    with open(cfg, "w", encoding="utf-8") as f:
        json.dump({"backends": {"gdal": {
            "command": [sys.executable, SERVER], "mode": "local-cli",
            "calibration": {"level": "calibrated",
                            "evidence_ref": "test_gdal_live.py"}}}},
                  f, ensure_ascii=False)
    gw_env = dict(GDAL_ENV, GIS_GATEWAY_BACKENDS=cfg)
    g = Client([sys.executable, GATEWAY], env=gw_env)
    d = g.call("gis_discover", {"backend": "gdal"})
    record("网关 e2e discover@gdal（6 个 v02 动词）",
           d.get("backend") == "gdal"
           and {"gis_reproject", "gis_convert_format", "gis_clip",
                "gis_slope", "gis_aspect", "gis_hillshade"}
           <= set((d.get("v02_verbs") or {}).get("supported", [])), d)
    e = g.call("gis_convert_format", {
        "backend": "gdal", "input": os.path.join(WORK, "poly.geojson"),
        "target": os.path.join(OUT, "gw_poly.gpkg"), "kind": "vector",
        "format": "GPKG", "confirm": True})
    record("网关 e2e gis_convert_format@gdal（真实产出）",
           e.get("ok") is not False
           and os.path.exists(os.path.join(OUT, "gw_poly.gpkg")), e)
    s = g.call("gis_slope", {
        "backend": "gdal", "input": os.path.join(WORK, "dem.tif"),
        "target": os.path.join(OUT, "gw_slope.tif"), "confirm": True})
    record("网关 e2e gis_slope@gdal（真实产出）",
           s.get("ok") is not False
           and os.path.getsize(os.path.join(OUT, "gw_slope.tif")) > 0, s)
    g.close()

    passed = sum(1 for r in RESULTS if r["ok"])
    summary = {"total": len(RESULTS), "passed": passed,
               "failed": len(RESULTS) - passed, "cases": RESULTS}
    outdir = os.path.join(ROOT, "evidence", "phase2")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "gdal-live-results.json"), "w",
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

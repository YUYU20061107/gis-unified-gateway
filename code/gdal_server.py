# -*- coding: utf-8 -*-
"""gdal_server.py — GDAL/OGR 本地 CLI 后端（stdio MCP，纯标准库）。

工具面只暴露已实跑验证的最小集：
  gdal_ping / gdal_discover
  gdal_reproject       (V15 vector/raster)
  gdal_convert_format  (V16 vector/raster/table)
  gdal_clip            (V19 vector/raster)
  gdal_slope / gdal_aspect / gdal_hillshade (V24/V25/V26)

证据等级：本地 GDAL CLI 实跑；不是离线 mock。所有写操作只写新 target，
target 已存在一律拒绝，不覆盖原件。
"""
import io
import json
import os
import shutil
import subprocess
import sys

QGIS_ROOT = r"C:\Program Files\QGIS 3.44.15"
GDAL_BIN = os.environ.get("GIS_GDAL_BIN") or os.path.join(QGIS_ROOT, "bin")
PROTOCOL_VERSION = "2024-11-05"

_TOOLS = [
    "gdal_ping", "gdal_discover", "gdal_reproject", "gdal_convert_format",
    "gdal_clip", "gdal_slope", "gdal_aspect", "gdal_hillshade",
]

_VECTOR_FMT = {
    "geojson": "GeoJSON", "json": "GeoJSON",
    "gpkg": "GPKG", "geopackage": "GPKG",
    "shp": "ESRI Shapefile", "shapefile": "ESRI Shapefile",
    "esri shapefile": "ESRI Shapefile",
    "csv": "CSV", "gml": "GML", "kml": "KML", "sqlite": "SQLite",
}
_RASTER_FMT = {
    "gtiff": "GTiff", "geotiff": "GTiff", "tif": "GTiff", "tiff": "GTiff",
    "png": "PNG", "jpeg": "JPEG", "jpg": "JPEG", "vrt": "VRT",
    "cog": "COG", "aaigrid": "AAIGrid", "xyz": "XYZ",
}
_RESAMPLING = {"near", "bilinear", "cubic", "cubicspline", "lanczos",
               "average", "mode", "max", "min", "med", "q1", "q3"}


def _env():
    env = dict(os.environ)
    root = os.path.dirname(os.path.abspath(GDAL_BIN))
    proj = os.path.join(root, "share", "proj")
    gdal_data = os.path.join(root, "apps", "gdal", "share", "gdal")
    if os.path.exists(os.path.join(proj, "proj.db")):
        env["PROJ_LIB"] = proj
        env["PROJ_DATA"] = proj
    if os.path.isdir(gdal_data):
        env["GDAL_DATA"] = gdal_data
    env["PATH"] = GDAL_BIN + os.pathsep + env.get("PATH", "")
    return env


ENV = _env()


def _exe(name):
    p = os.path.join(GDAL_BIN, name + (".exe" if os.name == "nt" else ""))
    if os.path.exists(p):
        return p
    return shutil.which(name)


def _fail(code, message, **extra):
    d = {"ok": False, "error_code": code, "message": message}
    d.update(extra)
    return d


def _run(name, args, timeout=120):
    exe = _exe(name)
    if not exe:
        return _fail("GDAL_NOT_FOUND", "找不到 GDAL 工具 %s（GIS_GDAL_BIN=%s）"
                     % (name, GDAL_BIN))
    cmd = [exe] + [str(a) for a in args]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace",
                           timeout=timeout, env=ENV)
    except subprocess.TimeoutExpired:
        return _fail("GDAL_TIMEOUT", "%s 超过 %ss 未完成" % (name, timeout),
                     command=" ".join(cmd))
    except Exception as e:  # noqa: BLE001
        return _fail("GDAL_EXEC_ERROR", "%s: %s" % (name, e),
                     command=" ".join(cmd))
    if p.returncode != 0:
        return _fail("GDAL_ERROR", (p.stderr or p.stdout or "").strip()[-2000:],
                     command=" ".join(cmd), returncode=p.returncode)
    return {"ok": True, "command": " ".join(cmd),
            "stdout": p.stdout or "", "stderr": p.stderr or ""}


def _path(value, label):
    if not isinstance(value, str) or not value.strip():
        return None, _fail("INVALID_ARGUMENT", "%s 必填且须为路径" % label)
    s = value.strip()
    if "://" in s or any(ord(c) < 32 for c in s):
        return None, _fail("INVALID_ARGUMENT", "%s 只接受本地路径" % label)
    return os.path.abspath(s), None


def _target(value):
    path, err = _path(value, "target")
    if err:
        return None, err
    if os.path.exists(path):
        return None, _fail("TARGET_EXISTS",
                           "target 已存在，拒绝覆盖：%s" % path)
    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    return path, None


def _is_wkt(s):
    head = (s or "").lstrip().upper()
    return head.startswith(("POLYGON", "MULTIPOLYGON", "ENVELOPE",
                            "POINT", "LINESTRING"))


def _size(path):
    try:
        if os.path.isfile(path):
            return os.path.getsize(path)
        if os.path.isdir(path):
            return sum(os.path.getsize(os.path.join(path, f))
                       for f in os.listdir(path)
                       if os.path.isfile(os.path.join(path, f)))
    except OSError:
        pass
    return None


def _ogr_layer(path):
    r = _run("ogrinfo", ["-json", "-so", path])
    if not r.get("ok"):
        return None, r
    try:
        data = json.loads(r["stdout"])
        layers = data.get("layers") or []
    except Exception as e:  # noqa: BLE001
        return None, _fail("GDAL_OUTPUT_ERROR", "ogrinfo JSON 解析失败: %s" % e)
    if not layers:
        return None, _fail("GDAL_NO_LAYER", "数据源没有图层：%s" % path)
    layer = layers[0]
    return {
        "layer": layer.get("name"),
        "feature_count": layer.get("featureCount"),
        "geometry_fields": [g.get("name") for g in
                            (layer.get("geometryFields") or [])],
        "fields": [f.get("name") for f in (layer.get("fields") or [])],
        "srs_wkt": (((layer.get("geometryFields") or [{}])[0]
                     .get("coordinateSystem") or {}).get("wkt") or ""),
    }, None


def _gdal_info(path):
    r = _run("gdalinfo", ["-json", path])
    if not r.get("ok"):
        return None, r
    try:
        data = json.loads(r["stdout"])
    except Exception as e:  # noqa: BLE001
        return None, _fail("GDAL_OUTPUT_ERROR", "gdalinfo JSON 解析失败: %s" % e)
    return {
        "size": data.get("size"),
        "driver": data.get("driverShortName"),
        "srs_wkt": ((data.get("coordinateSystem") or {}).get("wkt") or ""),
        "bands": len(data.get("bands") or []),
        "corner": data.get("cornerCoordinates"),
    }, None


def _vector_driver(fmt):
    key = (fmt or "").strip().lower()
    drv = _VECTOR_FMT.get(key)
    if not drv:
        return None, _fail("FORMAT_NOT_SUPPORTED",
                           "GDAL 矢量首版不支持格式 %r；支持：%s"
                           % (fmt, ", ".join(sorted(_VECTOR_FMT))))
    return drv, None


def _raster_driver(fmt):
    key = (fmt or "").strip().lower()
    drv = _RASTER_FMT.get(key)
    if not drv:
        return None, _fail("FORMAT_NOT_SUPPORTED",
                           "GDAL 栅格首版不支持格式 %r；支持：%s"
                           % (fmt, ", ".join(sorted(_RASTER_FMT))))
    return drv, None


def _infer_vector_driver(target):
    ext = os.path.splitext(target)[1].lower()
    return {".geojson": "GeoJSON", ".json": "GeoJSON", ".gpkg": "GPKG",
            ".shp": "ESRI Shapefile", ".csv": "CSV", ".gml": "GML",
            ".kml": "KML", ".sqlite": "SQLite"}.get(ext, "GPKG")


def gdal_ping(args):
    r = _run("gdalinfo", ["--version"])
    if not r.get("ok"):
        return r
    return {"ok": True, "version": r["stdout"].strip(),
            "bin": GDAL_BIN, "mode": "local-cli"}


def gdal_discover(args):
    ver = _run("gdalinfo", ["--version"])
    if not ver.get("ok"):
        return ver
    fmts = _run("gdalinfo", ["--formats"])
    vfmts = _run("ogrinfo", ["--formats"])
    def count(out):
        names = []
        for line in (out or "").splitlines():
            s = line.strip()
            if not s or s.lower().startswith("supported"):
                continue
            names.append(s.split()[0])
        return names
    rnames = count(fmts.get("stdout")) if fmts.get("ok") else []
    vnames = count(vfmts.get("stdout")) if vfmts.get("ok") else []
    return {"ok": True, "version": ver["stdout"].strip(),
            "bin": GDAL_BIN, "mode": "local-cli",
            "raster_format_count": len(rnames),
            "vector_format_count": len(vnames),
            "raster_formats_sample": rnames[:20],
            "vector_formats_sample": vnames[:20],
            "tools": _TOOLS}


def gdal_reproject(args):
    src, err = _path(args.get("input"), "input")
    if err:
        return err
    dst, err = _target(args.get("target"))
    if err:
        return err
    if not os.path.exists(src):
        return _fail("INPUT_NOT_FOUND", "input 不存在：%s" % src)
    try:
        srid = int(args.get("target_srid"))
    except Exception:
        return _fail("INVALID_ARGUMENT", "target_srid 必须是整数 EPSG")
    if not (1 <= srid <= 999999):
        return _fail("INVALID_ARGUMENT", "target_srid 超出 EPSG 范围")
    kind = (args.get("kind") or "").lower()
    if kind == "vector":
        drv = _infer_vector_driver(dst)
        r = _run("ogr2ogr", ["-t_srs", "EPSG:%d" % srid,
                             "-f", drv, dst, src])
        if not r.get("ok"):
            return r
        meta, merr = _ogr_layer(dst)
        out = {"ok": True, "input": src, "target": dst, "kind": kind,
               "driver": drv, "target_srid": srid,
               "size_bytes": _size(dst), "command": r["command"]}
        if meta:
            out["output"] = meta
        return out
    if kind == "raster":
        resampling = (args.get("resampling") or "near").lower()
        if resampling not in _RESAMPLING:
            return _fail("INVALID_ARGUMENT", "resampling 不在封闭枚举内")
        r = _run("gdalwarp", ["-t_srs", "EPSG:%d" % srid,
                              "-r", resampling, src, dst])
        if not r.get("ok"):
            return r
        meta, _ = _gdal_info(dst)
        out = {"ok": True, "input": src, "target": dst, "kind": kind,
               "target_srid": srid, "resampling": resampling,
               "size_bytes": _size(dst), "command": r["command"]}
        if meta:
            out["output"] = meta
        return out
    if kind == "table":
        return _fail("NOT_SUPPORTED", "表没有坐标，重投影概念不适用")
    return _fail("INVALID_ARGUMENT", "kind 须为 vector 或 raster")


def gdal_convert_format(args):
    src, err = _path(args.get("input"), "input")
    if err:
        return err
    dst, err = _target(args.get("target"))
    if err:
        return err
    if not os.path.exists(src):
        return _fail("INPUT_NOT_FOUND", "input 不存在：%s" % src)
    kind = (args.get("kind") or "").lower()
    fmt = args.get("format")
    if kind in ("vector", "table"):
        drv, err = _vector_driver(fmt)
        if err:
            return err
        r = _run("ogr2ogr", ["-f", drv, dst, src])
        if not r.get("ok"):
            return r
        meta, _ = _ogr_layer(dst)
        out = {"ok": True, "input": src, "target": dst, "kind": kind,
               "driver": drv, "format": fmt, "size_bytes": _size(dst),
               "command": r["command"]}
        if meta:
            out["output"] = meta
        return out
    if kind == "raster":
        drv, err = _raster_driver(fmt)
        if err:
            return err
        r = _run("gdal_translate", ["-of", drv, src, dst])
        if not r.get("ok"):
            return r
        meta, _ = _gdal_info(dst)
        out = {"ok": True, "input": src, "target": dst, "kind": kind,
               "driver": drv, "format": fmt, "size_bytes": _size(dst),
               "command": r["command"]}
        if meta:
            out["output"] = meta
        return out
    return _fail("INVALID_ARGUMENT", "kind 须为 vector/raster/table")


def gdal_clip(args):
    src, err = _path(args.get("input"), "input")
    if err:
        return err
    dst, err = _target(args.get("target"))
    if err:
        return err
    if not os.path.exists(src):
        return _fail("INPUT_NOT_FOUND", "input 不存在：%s" % src)
    clip = args.get("clip_by")
    if not isinstance(clip, str) or not clip.strip():
        return _fail("INVALID_ARGUMENT", "clip_by 必填")
    clip = clip.strip()
    if not _is_wkt(clip):
        clip_path, err = _path(clip, "clip_by")
        if err:
            return err
        if not os.path.exists(clip_path):
            return _fail("INPUT_NOT_FOUND", "clip_by 不存在：%s" % clip_path)
        clip = clip_path
    kind = (args.get("input_type") or "").lower()
    if kind == "vector":
        drv = _infer_vector_driver(dst)
        r = _run("ogr2ogr", ["-clipsrc", clip, "-f", drv, dst, src])
        if not r.get("ok"):
            return r
        meta, _ = _ogr_layer(dst)
        out = {"ok": True, "input": src, "clip_by": clip, "target": dst,
               "input_type": kind, "driver": drv,
               "size_bytes": _size(dst), "command": r["command"]}
        if meta:
            out["output"] = meta
        return out
    if kind == "raster":
        if _is_wkt(clip):
            return _fail("INVALID_ARGUMENT",
                         "GDAL 栅格裁剪首版要求 clip_by 为矢量文件路径")
        r = _run("gdalwarp", ["-cutline", clip, "-crop_to_cutline",
                              src, dst])
        if not r.get("ok"):
            return r
        meta, _ = _gdal_info(dst)
        out = {"ok": True, "input": src, "clip_by": clip, "target": dst,
               "input_type": kind, "size_bytes": _size(dst),
               "command": r["command"]}
        if meta:
            out["output"] = meta
        return out
    return _fail("INVALID_ARGUMENT", "input_type 须为 vector 或 raster")


def _terrain(args, op):
    src, err = _path(args.get("input"), "input")
    if err:
        return err
    dst, err = _target(args.get("target"))
    if err:
        return err
    if not os.path.exists(src):
        return _fail("INPUT_NOT_FOUND", "input 不存在：%s" % src)
    argv = [op, src, dst, "-of", "GTiff"]
    note = None
    z = args.get("z_factor")
    if z is not None:
        try:
            z = float(z)
            if z <= 0:
                raise ValueError
        except Exception:
            return _fail("INVALID_ARGUMENT", "z_factor 必须是正数")
        if op == "slope":
            argv += ["-s", str(z)]
        elif op == "hillshade":
            argv += ["-z", str(z)]
        else:
            note = "gdaldem aspect 不接受 z_factor，已忽略"
    r = _run("gdaldem", argv)
    if not r.get("ok"):
        return r
    meta, _ = _gdal_info(dst)
    out = {"ok": True, "input": src, "target": dst, "operation": op,
           "size_bytes": _size(dst), "command": r["command"]}
    if note:
        out["note"] = note
    if meta:
        out["output"] = meta
    return out


def gdal_slope(args):
    return _terrain(args, "slope")


def gdal_aspect(args):
    return _terrain(args, "aspect")


def gdal_hillshade(args):
    return _terrain(args, "hillshade")


_HANDLERS = {
    "gdal_ping": gdal_ping,
    "gdal_discover": gdal_discover,
    "gdal_reproject": gdal_reproject,
    "gdal_convert_format": gdal_convert_format,
    "gdal_clip": gdal_clip,
    "gdal_slope": gdal_slope,
    "gdal_aspect": gdal_aspect,
    "gdal_hillshade": gdal_hillshade,
}


def _tool_defs():
    return [{"name": n, "description": "GDAL local CLI backend tool",
             "inputSchema": {"type": "object", "properties": {}}}
            for n in _TOOLS]


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "gdal-cli-bridge", "version": "0.1.0"}}}
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
            payload = _fail("UNKNOWN_TOOL", "gdal 后端没有工具：%s" % name)
        else:
            try:
                payload = _HANDLERS[name](args)
            except Exception as e:  # noqa: BLE001
                payload = _fail("GDAL_EXEC_ERROR", "%s: %s" % (name, e))
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

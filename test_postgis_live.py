# -*- coding: utf-8 -*-
"""test_postgis_live.py — PostGIS 真后端验收（隔离临时集群）。

流程：
  1) initdb/启动一个隔离 PostgreSQL（trust、随机端口、临时数据目录）；
  2) 建 gisplat_test + postgis/postgis_raster；
  3) 用修正后的 test_templates_live.py 在实库逐条跑 36 模板（38 用例）；
  4) 起 code/postgis_server.py，直连验证元数据/模板/GeoJSON 导出；
  5) 起 gateway.py 只配 postgis，跑基础动词 + 建表/加字段/校验修复/
     量测/坡度/GeoJSON 导出；
  6) 查库确认对象存在，停库并清理临时目录。

证据落 evidence/phase4-postgis/。不触碰本机 5432 生产实例。
"""
import json
import os
import queue
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
PG_BIN = r"C:\Program Files\PostgreSQL\16\bin"
QGIS_PY = r"C:\Program Files\QGIS 3.44.15\apps\Python312\python.exe"
POSTGIS_SERVER = os.path.join(ROOT, "code", "postgis_server.py")
GATEWAY = os.path.join(ROOT, "code", "gateway.py")
TEMPLATE_TEST = os.path.join(ROOT, "test_templates_live.py")
EVID = os.path.join(ROOT, "evidence", "phase4-postgis")
os.makedirs(EVID, exist_ok=True)
RESULTS = []


def record(name, ok, detail=None):
    RESULTS.append({"name": name, "ok": bool(ok), "detail": detail})
    print("%s %s" % ("PASS" if ok else "FAIL", name), flush=True)
    if not ok:
        print("  detail:", json.dumps(detail, ensure_ascii=False)[:1500],
              flush=True)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def run(cmd, env=None, cwd=None, timeout=180, capture=True):
    if not capture:
        # 关键：pg_ctl start 会拉起常驻 postgres；不能给它 PIPE，
        # 否则 Windows 上父进程等管道 EOF 会永久挂住。
        p = subprocess.run(cmd, env=env, cwd=cwd, timeout=timeout,
                           stdin=subprocess.DEVNULL,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        if p.returncode != 0:
            raise RuntimeError("cmd failed (%s): %s"
                               % (p.returncode, cmd))
        return p
    p = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace",
                       env=env, cwd=cwd, timeout=timeout)
    if p.returncode != 0:
        raise RuntimeError("cmd failed: %s\n%s\n%s"
                           % (cmd, p.stdout[-2000:], p.stderr[-2000:]))
    return p


def psql(dsn, sql, timeout=60):
    p = subprocess.run(
        [os.path.join(PG_BIN, "psql.exe"), "-d", dsn, "-X", "-q",
         "-v", "ON_ERROR_STOP=1", "-At", "-c", sql],
        capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=timeout)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


class Client:
    def __init__(self, argv, env=None):
        self.proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8",
            errors="replace", env=env or os.environ)
        self.ident = 0
        self.q = queue.Queue()
        threading.Thread(target=self._reader, daemon=True).start()
        self.call("initialize", {}, raw=True)

    def _reader(self):
        try:
            for line in self.proc.stdout:
                if line.strip():
                    self.q.put(json.loads(line))
        finally:
            self.q.put(None)

    def call(self, name, args, raw=False):
        self.ident += 1
        msg = {"jsonrpc": "2.0", "id": self.ident,
               "method": "initialize" if raw else "tools/call"}
        msg["params"] = {} if raw else {"name": name, "arguments": args}
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        try:
            resp = self.q.get(timeout=180)
        except queue.Empty:
            raise RuntimeError(
                "backend timeout: %s\nstderr: %s"
                % (name, self.proc.stderr.read()[-1200:]))
        if resp is None:
            raise RuntimeError("backend exited: %s"
                               % self.proc.stderr.read()[-1200:])
        if resp.get("id") != self.ident:
            raise RuntimeError("unexpected response id: %r" % resp.get("id"))
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


def start_cluster():
    port = free_port()
    base = tempfile.mkdtemp(prefix="gisplat-pg-live-")
    data = os.path.join(base, "data")
    log = os.path.join(base, "pg.log")
    init = run([os.path.join(PG_BIN, "initdb.exe"), "-D", data,
                "-U", "postgres", "--auth=trust", "--encoding=UTF8",
                "--locale=C"], timeout=180)
    run([os.path.join(PG_BIN, "pg_ctl.exe"), "-D", data, "-l", log,
         "-o", "-p %d -h 127.0.0.1" % port, "-w", "start"],
        timeout=120, capture=False)
    dsn = "dbname=gisplat_test user=postgres host=127.0.0.1 port=%d" % port
    run([os.path.join(PG_BIN, "createdb.exe"), "-p", str(port),
         "-h", "127.0.0.1", "-U", "postgres", "gisplat_test"], timeout=60)
    rc, out, err = psql(dsn, "CREATE EXTENSION postgis; "
                             "CREATE EXTENSION postgis_raster; "
                             "SELECT version(); SELECT PostGIS_Version();")
    if rc != 0:
        raise RuntimeError("extensions failed: %s" % err)
    return {"base": base, "data": data, "log": log, "dsn": dsn,
            "port": port, "init_stdout": init.stdout[-500:],
            "versions": out}


def stop_cluster(c):
    try:
        subprocess.run([os.path.join(PG_BIN, "pg_ctl.exe"), "-D", c["data"],
                        "-m", "fast", "-w", "stop"],
                       stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=120)
    finally:
        shutil.rmtree(c["base"], ignore_errors=True)


def main():
    for name in ("bridge-t_polys.geojson", "gw_t_polys.geojson",
                 "postgis-export-debug.log", "gateway-debug.log"):
        path = os.path.join(EVID, name)
        if os.path.exists(path):
            os.remove(path)
    cluster = start_cluster()
    env_db = dict(
        os.environ, GIS_POSTGIS_DSN=cluster["dsn"],
        GIS_POSTGIS_DEBUG=os.path.join(EVID, "postgis-export-debug.log"),
        GIS_GATEWAY_DEBUG=os.path.join(EVID, "gateway-debug.log"))
    pg_path = PG_BIN + os.pathsep + os.environ.get("PATH", "")
    env_db["PATH"] = pg_path
    print("cluster started: %s" % cluster["dsn"], flush=True)
    try:
        # ---- 1) 模板测试（修正后的 psql 调用） ----
        print("running template test", flush=True)
        p = subprocess.run(
            [sys.executable, TEMPLATE_TEST, cluster["dsn"]],
            cwd=EVID, env=dict(env_db, PYTHONIOENCODING="utf-8"),
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=300)
        with open(os.path.join(EVID, "postgis-templates.log"), "w",
                  encoding="utf-8", newline="\n") as f:
            f.write(p.stdout or "")
            f.write("\n--- stderr ---\n")
            f.write(p.stderr or "")
        tpl = json.load(open(os.path.join(EVID, "postgis-test-results.json"),
                             encoding="utf-8"))
        tpass = sum(1 for x in tpl if x["status"] == "PASS")
        record("修正后模板实跑 38/38（真执行，非空跑）",
               p.returncode == 0 and len(tpl) == 38 and tpass == 38,
               {"returncode": p.returncode, "total": len(tpl),
                "pass": tpass, "stderr": (p.stderr or "")[-500:]})

        print("template test done", flush=True)
        # ---- 2) 桥直连 ----
        print("bridge direct starting", flush=True)
        c = Client([QGIS_PY, POSTGIS_SERVER], env=env_db)
        ping = c.call("postgis_ping", {})
        record("桥 ping：PostgreSQL/PostGIS 版本",
               ping.get("ok") and ping.get("postgis_version", "").startswith("3.6"),
               ping)
        tables = c.call("postgis_list_spatial_tables", {})
        record("桥 list_spatial_tables：t_polys/t_dem 在册",
               isinstance(tables, list)
               and any(t.get("table") == "t_polys" for t in tables)
               and any(t.get("table") == "t_dem" for t in tables),
               {"type": type(tables).__name__, "count": len(tables)
                if isinstance(tables, list) else None})
        summ = c.call("postgis_table_summary", {"table": "t_polys"})
        record("桥 table_summary：t_polys 3 行",
               summ.get("ok") and summ.get("row_count") == 3, summ)
        cols = c.call("postgis_table_columns", {"table": "t_polys"})
        record("桥 table_columns：t_polys 有 geom/val",
               cols.get("ok") and {"geom", "val"} <=
               {x["column_name"] for x in cols.get("columns") or []}, cols)
        chk = c.call("postgis_exec_template", {
            "template_id": "validate_check",
            "sql": "SELECT count(*) AS total, count(*) FILTER "
                   "(WHERE NOT ST_IsValid(geom)) AS invalid_count FROM t_bad",
            "params": {}, "confirm": True})
        record("桥 exec_template validate_check：1 坏几何",
               chk.get("ok") and chk.get("rows")
               and chk["rows"][0].get("invalid_count") == 1, chk)
        c.close()

        print("bridge direct done", flush=True)
        # ---- 3) 网关 -> PostGIS ----
        print("gateway starting", flush=True)
        cfg = os.path.join(EVID, "_gw-postgis.json")
        with open(cfg, "w", encoding="utf-8") as f:
            json.dump({"backends": {"postgis": {
                "command": [QGIS_PY, POSTGIS_SERVER],
                "mode": "local-instance",
                "calibration": {"level": "calibrated",
                                "evidence_ref": "test_postgis_live.py"}}}},
                f, ensure_ascii=False)
        g = Client([sys.executable, GATEWAY],
                   env=dict(env_db, GIS_GATEWAY_BACKENDS=cfg))
        p = g.call("gis_ping", {"backend": "postgis"})
        record("网关 gis_ping@postgis", p.get("ok") is not False, p)
        d = g.call("gis_discover", {"backend": "postgis"})
        record("网关 discover@postgis：36 模板 + PostGIS 3.6",
               (d.get("postgis_templates") or {}).get("count") == 36
               and (d.get("native_discover") or {}).get(
                   "postgis_version", "").startswith("3.6"), d)
        ds = g.call("gis_list_datasets", {"backend": "postgis"})
        record("网关 list_datasets@postgis：t_polys 在列表",
               isinstance(ds.get("tables"), list)
               and any(t.get("table") == "t_polys"
                       for t in ds["tables"]), ds)
        pi = g.call("gis_project_info", {"backend": "postgis"})
        record("网关 project_info@postgis：kind=database",
               pi.get("kind") == "database"
               and isinstance(pi.get("tables"), list), pi)

        ex = g.call("gis_convert_format", {
            "backend": "postgis", "input": "t_polys",
            "target": os.path.join(EVID, "gw_t_polys.geojson"),
            "format": "GeoJSON", "kind": "vector", "confirm": True})
        record("网关 convert_format@postgis：GeoJSON 3 要素",
               ex.get("ok") is True
               and ex.get("feature_count") == 3, ex)

        cr = g.call("gis_create_dataset", {
            "backend": "postgis", "name": "gw_t", "kind": "vector",
            "geometry_type": "Polygon", "srid": 4326, "confirm": True})
        record("网关 create_dataset@postgis：gw_t 建表",
               (cr.get("backend_result") or {}).get("ok") is True, cr)
        af = g.call("gis_add_field", {
            "backend": "postgis", "dataset": "gw_t",
            "field": {"name": "extra", "type": "text"}, "confirm": True})
        record("网关 add_field@postgis：extra 字段",
               (af.get("backend_result") or {}).get("ok") is True, af)
        cf = g.call("gis_calculate_field", {
            "backend": "postgis", "dataset": "gw_t", "field": "extra",
            "expression": "extra", "confirm": True})
        record("网关 calculate_field@postgis：表达式模板执行",
               (cf.get("backend_result") or {}).get("ok") is True, cf)
        m = g.call("gis_measure", {
            "backend": "postgis", "operation": "distance",
            "a_wkt": "POINT(0 0)", "b_wkt": "POINT(0 1)", "srid": 4326})
        record("网关 measure@postgis：距离 1.0",
               (m.get("backend_result") or {}).get("ok") is True
               and (m["backend_result"].get("rows") or [{}])[0].get("value") == 1.0,
               m)
        vc = g.call("gis_validate_geometry", {
            "backend": "postgis", "dataset": "t_bad"})
        record("网关 validate check@postgis：1 坏几何",
               (vc.get("backend_result") or {}).get("ok") is True
               and (vc["backend_result"].get("rows") or [{}])[0]
               .get("invalid_count") == 1, vc)
        vr = g.call("gis_validate_geometry", {
            "backend": "postgis", "dataset": "t_bad", "repair": True,
            "target": "gw_bad_fixed", "confirm": True})
        record("网关 validate repair@postgis：gw_bad_fixed",
               (vr.get("backend_result") or {}).get("ok") is True, vr)
        sl = g.call("gis_slope", {
            "backend": "postgis", "input": "t_dem", "target": "gw_slope",
            "confirm": True})
        record("网关 slope@postgis：gw_slope",
               (sl.get("backend_result") or {}).get("ok") is True, sl)
        sf = g.call("gis_spatial_filter", {
            "backend": "postgis", "table": "t_polys",
            "predicate": "intersects",
            "reference_wkt": "POLYGON((0 0,2 0,2 2,0 2,0 0))"})
        record("网关 spatial_filter@postgis：返回行",
               (sf.get("backend_result") or {}).get("ok") is True
               and len(sf["backend_result"].get("rows") or []) >= 1, sf)
        g.close()

        print("gateway done", flush=True)
        # ---- 4) 查库确认对象 ----
        rc1, out1, _ = psql(cluster["dsn"],
                            "SELECT column_name FROM information_schema.columns "
                            "WHERE table_name='gw_t' AND column_name='extra';")
        rc2, out2, _ = psql(cluster["dsn"],
                            "SELECT to_regclass('public.gw_bad_fixed'), "
                            "to_regclass('public.gw_slope');")
        record("DB 复核：gw_t.extra / gw_bad_fixed / gw_slope 均存在",
               rc1 == 0 and out1 == "extra" and rc2 == 0
               and "gw_bad_fixed" in out2 and "gw_slope" in out2,
               {"extra": out1, "objects": out2})
        with open(os.path.join(EVID, "gw_t_polys.geojson"),
                  encoding="utf-8") as f:
            feat = len(json.load(f).get("features") or [])
        record("导出文件复核：gw_t_polys.geojson 3 要素", feat == 3, feat)

        passed = sum(1 for r in RESULTS if r["ok"])
        out = {
            "evidence": "local-instance-verified",
            "isolated_cluster": True,
            "port": cluster["port"],
            "database": "gisplat_test",
            "versions": cluster["versions"],
            "production_dsn_untouched": True,
            "templates": {"total": len(tpl), "passed": tpass},
            "total": len(RESULTS), "passed": passed,
            "failed": len(RESULTS) - passed,
            "cases": RESULTS,
        }
        with open(os.path.join(EVID, "postgis-live-results.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print("\nchecks: %d, passed: %d, failed: %d"
              % (len(RESULTS), passed, len(RESULTS) - passed))
        return 0 if passed == len(RESULTS) else 1
    finally:
        stop_cluster(cluster)


if __name__ == "__main__":
    raise SystemExit(main())

# -*- coding: utf-8 -*-
"""postgis_server.py — PostGIS 本地实例后端（stdio MCP，psycopg2）。

运行解释器需带 psycopg2（本机用 QGIS 3.44.15 自带 Python；标准 Python
未装 psycopg2）。DSN 由 GIS_POSTGIS_DSN 提供，默认本机 5432 的 gisplat。

安全边界：模板执行只接受 postgis_templates.json 内的 template_id，并要求
confirm=true；SQL 由网关 build_template 渲染，值走 psycopg2 绑定参数。
本文件不提供任意 SQL 工具。
"""
import datetime
import io
import json
import os
import re
import sys
import time
from decimal import Decimal

import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

HERE = os.path.dirname(os.path.abspath(__file__))
DSN = os.environ.get(
    "GIS_POSTGIS_DSN",
    "dbname=gisplat user=postgres host=127.0.0.1 port=5432")
PROTOCOL_VERSION = "2024-11-05"
IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?$")
TEMPLATE_IDS = {t["template_id"] for t in json.load(
    open(os.path.join(HERE, "postgis_templates.json"), encoding="utf-8")
)["templates"]}
_TOOLS = ["postgis_ping", "postgis_discover", "postgis_list_spatial_tables",
          "postgis_table_summary", "postgis_table_columns",
          "postgis_exec_template", "postgis_export_geojson"]


def _debug(msg):
    path = os.environ.get("GIS_POSTGIS_DEBUG")
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8") as f:
            f.write("%s pid=%s %s\n"
                    % (time.strftime("%H:%M:%S"), os.getpid(), msg))
    except Exception:  # noqa: BLE001
        pass


def _fail(code, message, **extra):
    d = {"ok": False, "error_code": code, "message": message}
    d.update(extra)
    return d


def _jsonable(v):
    if isinstance(v, Decimal):
        return float(v)
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, (bytes, bytearray)):
        return v.hex()
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    return v


def _connect():
    return psycopg2.connect(DSN)


def _table_args(args):
    table = args.get("table") or args.get("dataset") or args.get("input")
    if not isinstance(table, str) or not IDENT_RE.match(table):
        return None, _fail("INVALID_ARGUMENT",
                           "table 须为 name 或 schema.name")
    return table, None


def _ident(table):
    parts = table.split(".")
    return sql.Identifier(*parts)


def _table_geom(cur, table):
    parts = table.split(".")
    if len(parts) == 2:
        cond = sql.SQL("f_table_schema=%s AND f_table_name=%s")
        params = (parts[0], parts[1])
    else:
        cond = sql.SQL("f_table_name=%s")
        params = (parts[0],)
    cur.execute(sql.SQL(
        "SELECT f_geometry_column FROM geometry_columns WHERE ")
        + cond + sql.SQL(" LIMIT 1"), params)
    row = cur.fetchone()
    return row["f_geometry_column"] if row else None


def postgis_ping(args):
    try:
        with _connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("SELECT version() AS pg, PostGIS_Version() AS postgis, "
                      "current_database() AS db, current_user AS usr")
            row = c.fetchone()
        return {"ok": True, "mode": "local-instance",
                "postgres_version": row["pg"],
                "postgis_version": row["postgis"],
                "database": row["db"], "user": row["usr"],
                "dsn_configured": "GIS_POSTGIS_DSN" in os.environ}
    except Exception as e:  # noqa: BLE001
        return _fail("POSTGIS_CONNECT_ERROR", str(e))


def postgis_discover(args):
    p = postgis_ping(args)
    if not p.get("ok"):
        return p
    try:
        with _connect() as conn, conn.cursor() as c:
            c.execute("SELECT count(*) FROM geometry_columns")
            geom = c.fetchone()[0]
            try:
                c.execute("SELECT count(*) FROM raster_columns")
                rast = c.fetchone()[0]
            except Exception:  # noqa: BLE001
                conn.rollback()
                rast = None
        p.update({"geometry_columns": geom, "raster_columns": rast})
        return p
    except Exception as e:  # noqa: BLE001
        return _fail("POSTGIS_DISCOVER_ERROR", str(e))


def postgis_list_spatial_tables(args):
    try:
        with _connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("""
                SELECT f_table_schema AS schema, f_table_name AS table,
                       f_geometry_column AS geometry_column, type, srid
                FROM geometry_columns
                UNION ALL
                SELECT r_table_schema, r_table_name, r_raster_column,
                       'RASTER', srid
                FROM raster_columns
                ORDER BY 1, 2
            """)
            rows = c.fetchall()
        return _jsonable(rows)
    except Exception as e:  # noqa: BLE001
        return _fail("POSTGIS_QUERY_ERROR", str(e))


def postgis_table_summary(args):
    table, err = _table_args(args)
    if err:
        return err
    try:
        with _connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute(sql.SQL("SELECT count(*) AS row_count FROM ")
                      + _ident(table))
            row = c.fetchone()
            geom = args.get("geometry_column") or _table_geom(c, table)
            extent = None
            if geom and re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", geom):
                try:
                    c.execute(sql.SQL("SELECT ST_Extent(")
                              + sql.Identifier(geom)
                              + sql.SQL(")::text AS extent FROM ")
                              + _ident(table))
                    extent = c.fetchone()["extent"]
                except Exception:  # noqa: BLE001
                    conn.rollback()
        return {"ok": True, "table": table, "row_count": row["row_count"],
                "geometry_column": geom, "extent": extent}
    except Exception as e:  # noqa: BLE001
        return _fail("POSTGIS_QUERY_ERROR", str(e))


def postgis_table_columns(args):
    table, err = _table_args(args)
    if err:
        return err
    parts = table.split(".")
    schema = parts[0] if len(parts) == 2 else "public"
    name = parts[-1]
    try:
        with _connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as c:
            c.execute("""
                SELECT column_name, data_type, udt_name
                FROM information_schema.columns
                WHERE table_schema=%s AND table_name=%s
                ORDER BY ordinal_position
            """, (schema, name))
            rows = c.fetchall()
        return {"ok": True, "table": table, "columns": _jsonable(rows)}
    except Exception as e:  # noqa: BLE001
        return _fail("POSTGIS_QUERY_ERROR", str(e))


def postgis_exec_template(args):
    tid = args.get("template_id")
    stmt = args.get("sql")
    params = args.get("params") or {}
    if tid not in TEMPLATE_IDS:
        return _fail("TEMPLATE_NOT_REGISTERED",
                     "template_id 不在 36 个在册模板内：%r" % (tid,))
    if not isinstance(stmt, str) or not stmt.strip():
        return _fail("INVALID_ARGUMENT", "sql 必填")
    if args.get("confirm") is not True:
        return _fail("CONFIRM_REQUIRED",
                     "模板执行 require confirm=true（桥侧不放宽）")
    try:
        with _connect() as conn, conn.cursor(cursor_factory=RealDictCursor) as c:
            if params:
                c.execute(stmt, params)
            else:
                c.execute(stmt)
            columns = [d[0] for d in (c.description or [])]
            rows = []
            if c.description:
                rows = [_jsonable(r) for r in c.fetchmany(200)]
            rowcount = c.rowcount
            conn.commit()
        return {"ok": True, "template_id": tid, "rowcount": rowcount,
                "columns": columns, "rows": rows,
                "truncated": len(rows) == 200, "committed": True}
    except Exception as e:  # noqa: BLE001
        return _fail("POSTGIS_ERROR", str(e), template_id=tid)


def postgis_export_geojson(args):
    table, err = _table_args(args)
    if err:
        return err
    target = args.get("target") or args.get("path")
    if not isinstance(target, str) or not target.strip():
        return _fail("INVALID_ARGUMENT", "target 必填（GeoJSON 文件路径）")
    target = os.path.abspath(target)
    if os.path.exists(target):
        return _fail("TARGET_EXISTS", "target 已存在，拒绝覆盖：%s" % target)
    parent = os.path.dirname(target)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)
    limit = int(args.get("limit") or 10000)
    _debug("export start table=%r target=%r" % (table, target))
    try:
        with _connect() as conn, conn.cursor(
                cursor_factory=RealDictCursor) as c:
            _debug("export connected")
            geom = args.get("geometry_column") or _table_geom(c, table)
            _debug("export geom=%r" % (geom,))
            if not geom or not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", geom):
                return _fail("NO_GEOMETRY", "表没有可用几何列：%s" % table)
            q = sql.SQL("""
                SELECT jsonb_build_object(
                  'type','FeatureCollection',
                  'features', coalesce(jsonb_agg(jsonb_build_object(
                    'type','Feature',
                    'geometry', ST_AsGeoJSON(t.{geom})::jsonb,
                    'properties', to_jsonb(t) - {geom_lit}
                  )), '[]'::jsonb)
                ) AS fc
                FROM (SELECT * FROM {table} LIMIT %s) t
            """).format(geom=sql.Identifier(geom),
                        geom_lit=sql.Literal(geom),
                        table=_ident(table))
            _debug("export query start")
            c.execute(q, (limit,))
            _debug("export query done")
            fc = c.fetchone()["fc"]
            _debug("export fetch done")
        _debug("export write start")
        with open(target, "w", encoding="utf-8", newline="\n") as f:
            json.dump(fc, f, ensure_ascii=False)
        _debug("export write done")
        return {"ok": True, "table": table, "target": target,
                "feature_count": len(fc.get("features") or []),
                "bytes": os.path.getsize(target)}
    except Exception as e:  # noqa: BLE001
        _debug("export error %r" % (e,))
        return _fail("POSTGIS_EXPORT_ERROR", str(e))


_HANDLERS = {
    "postgis_ping": postgis_ping,
    "postgis_discover": postgis_discover,
    "postgis_list_spatial_tables": postgis_list_spatial_tables,
    "postgis_table_summary": postgis_table_summary,
    "postgis_table_columns": postgis_table_columns,
    "postgis_exec_template": postgis_exec_template,
    "postgis_export_geojson": postgis_export_geojson,
}


def _tool_defs():
    return [{"name": n, "description": "PostGIS local instance backend tool",
             "inputSchema": {"type": "object", "properties": {}}}
            for n in _TOOLS]


def handle(msg):
    method = msg.get("method")
    mid = msg.get("id")
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "postgis-instance-bridge",
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
            payload = _fail("UNKNOWN_TOOL", "postgis 没有工具：%s" % name)
        else:
            try:
                payload = _HANDLERS[name](args)
            except Exception as e:  # noqa: BLE001
                payload = _fail("POSTGIS_EXEC_ERROR", "%s: %s" % (name, e))
        is_err = isinstance(payload, dict) and payload.get("ok") is False
        return {"jsonrpc": "2.0", "id": mid, "result": {
            "content": [{"type": "text",
                         "text": json.dumps(payload, ensure_ascii=False)}],
            "isError": is_err,
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

# -*- coding: utf-8 -*-
"""
C3 实机测试：用 gateway.py 自己的 build_template 渲染全部 PostGIS 模板，
在真实 PostgreSQL+PostGIS 实例上逐条执行，记录 PASS/FAIL 与错误原文。

用法：
    python3 test_templates_live.py "dbname=gisplat_test user=postgres host=/var/run/postgresql"
连接走 psql 子进程；绑定参数 %(name)s 在测试侧以字面量代入（值均为本脚本自备，
仅验 SQL 有效性与语义；生产绑定由 psycopg 规范完成，不拼字符串）。
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "code"))
import gateway  # noqa: E402

DSN = sys.argv[1] if len(sys.argv) > 1 else "dbname=gisplat_test"


def psql(sql):
    p = subprocess.run(
        ["psql", "-d", DSN, "-X", "-q", "-v", "ON_ERROR_STOP=1", "-At",
         "-c", sql],
        capture_output=True, text=True, timeout=60)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def literal(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, (bytes, bytearray)):
        return "'\\x%s'::bytea" % bytes(v).hex()
    return "'%s'" % str(v).replace("'", "''")


def render_and_run(verb, tpl_id, args):
    try:
        sql, params, _tpl = gateway.build_template(verb, tpl_id, args)
    except Exception as e:
        return "RENDER_FAIL", "", "%s: %s" % (type(e).__name__, e)
    sql_exec = re.sub(r"%\((\w+)\)s", lambda m: literal(params[m.group(1)]), sql)
    rc, out, err = psql(sql_exec)
    if rc != 0:
        return "FAIL", sql_exec, err.split("\n")[0][:220]
    return "PASS", sql_exec, out[:120]


FIXTURES = """
DROP TABLE IF EXISTS t_polys, t_pts, t_zones, t_bad, t_dem CASCADE;
CREATE TABLE t_polys (id serial PRIMARY KEY, name text, grp text, val double precision, geom geometry(Polygon,4326));
INSERT INTO t_polys (name, grp, val, geom) VALUES
 ('A','g1',10, ST_GeomFromText('POLYGON((0 0,2 0,2 2,0 2,0 0))',4326)),
 ('B','g1',20, ST_GeomFromText('POLYGON((1 1,3 1,3 3,1 3,1 1))',4326)),
 ('C','g2',5,  ST_GeomFromText('POLYGON((10 10,11 10,11 11,10 11,10 10))',4326));
CREATE TABLE t_pts (id serial PRIMARY KEY, geom geometry(Point,4326));
INSERT INTO t_pts (geom) VALUES (ST_GeomFromText('POINT(0.5 0.5)',4326)), (ST_GeomFromText('POINT(50 50)',4326));
CREATE TABLE t_zones (id serial PRIMARY KEY, geom geometry(Polygon,4326));
INSERT INTO t_zones (geom) VALUES (ST_GeomFromText('POLYGON((0 0,2 0,2 2,0 2,0 0))',4326));
CREATE TABLE t_bad (id serial PRIMARY KEY, geom geometry(Polygon,4326));
INSERT INTO t_bad (geom) VALUES (ST_GeomFromText('POLYGON((0 0,2 2,2 0,0 2,0 0))',4326));
CREATE TABLE t_dem (id serial PRIMARY KEY, rast raster);
INSERT INTO t_dem (rast) SELECT ST_SetValue(ST_AddBand(ST_MakeEmptyRaster(4,4,0,4,1,-1,0,0,4326),'32BF'), x, y, 100 + x + y*4) FROM generate_series(1,4) x, generate_series(1,4) y;
"""


def main():
    rc, _, err = psql("SELECT 1")
    if rc != 0:
        print("CONNECT_FAIL", err[:200])
        return 2
    rc, _, err = psql(FIXTURES)
    print("fixtures:", "ok" if rc == 0 else "FAIL " + err[:200])

    cases = [
        ("gis_create_dataset", "create_table", {"table": "t_new", "geometry_type": "Polygon", "srid": 4326}),
        ("gis_add_field", "add_column", {"table": "t_polys", "fields": ["extra"], "sql_type": "text"}),
        ("gis_calculate_field", "update_field", {"table": "t_polys", "fields": ["val"], "expression": "val * 2"}),
        ("gis_copy_dataset", "copy_table", {"source": "t_polys", "target": "t_polys_copy"}),
        ("gis_rename_dataset", "rename_table", {"table": "t_polys_copy", "new_name": "t_polys_rn"}),
        ("gis_append_dataset", "insert_select", {"target": "t_polys_rn", "source": "t_polys"}),
        ("gis_merge_datasets", "merge_tables", {"target": "t_merged", "inputs": ["t_polys", "t_polys_rn"]}),
        ("gis_assign_projection", "set_srid", {"table": "t_polys", "column": "geom", "srid": 4326}),
        ("gis_reproject", "transform_create", {"source": "t_polys", "target": "t_polys_3857", "target_srid": 3857}),
        ("gis_buffer", "buffer_create", {"source": "t_polys", "target": "t_buf", "distance": 0.5}),
        ("gis_clip", "clip_vector", {"source": "t_polys", "clip_by": "t_zones", "target": "t_clip"}),
        ("gis_overlay", "overlay_intersection", {"source": "t_polys", "overlay": "t_zones", "target": "t_ov_inter"}),
        ("gis_overlay", "overlay_union", {"source": "t_polys", "overlay": "t_zones", "target": "t_ov_union"}),
        ("gis_overlay", "overlay_difference", {"source": "t_polys", "overlay": "t_zones", "target": "t_ov_diff"}),
        ("gis_overlay", "overlay_symdifference", {"source": "t_polys", "overlay": "t_zones", "target": "t_ov_sym"}),
        ("gis_dissolve", "dissolve", {"source": "t_polys", "target": "t_diss", "fields": ["grp"]}),
        ("gis_spatial_join", "spatial_join", {"source": "t_pts", "join": "t_polys", "predicate": "intersects", "target": "t_sj", "attributes": ["name", "grp"]}),
        ("gis_spatial_filter", "spatial_filter", {"table": "t_polys", "predicate": "intersects", "reference_wkt": "POLYGON((0 0,2 0,2 2,0 2,0 0))"}),
        ("gis_spatial_filter", "spatial_filter", {"table": "t_polys", "predicate": "dwithin", "reference_wkt": "POINT(5 5)", "distance": 3}),
        ("gis_field_statistics", "field_stats", {"table": "t_polys", "fields": ["val"], "group_by": ["grp"], "statistics": ["count", "sum", "avg"]}),
        ("gis_measure", "measure_distance", {"a_wkt": "POINT(0 0)", "b_wkt": "POINT(0 1)"}),
        ("gis_measure", "measure_area", {"a_wkt": "POLYGON((0 0,1 0,1 1,0 1,0 0))"}),
        ("gis_measure", "measure_length", {"a_wkt": "LINESTRING(0 0,1 1)"}),
        ("gis_measure", "measure_azimuth", {"a_wkt": "POINT(0 0)", "b_wkt": "POINT(1 0)"}),
        ("gis_validate_geometry", "validate_check", {"table": "t_bad"}),
        ("gis_validate_geometry", "validate_repair", {"table": "t_bad", "target": "t_bad_fixed"}),
        ("gis_validate_geometry", "validate_check", {"table": "t_bad_fixed", "geometry_column": "geom_repaired"}),
        ("gis_serve_vector_tile", "mvt_tile", {"table": "t_polys", "layer_name": "polys", "z": 1, "x": 1, "y": 0, "attributes": ["name", "grp"]}),
        ("gis_slope", "slope", {"source": "t_dem", "target": "t_slope"}),
        ("gis_aspect", "aspect", {"source": "t_dem", "target": "t_aspect"}),
        ("gis_hillshade", "hillshade", {"source": "t_dem", "target": "t_hs"}),
        ("gis_raster_calc", "mapalgebra", {"source": "t_dem", "target": "t_calc", "expression": "[rast.val]*2"}),
        ("gis_reclassify", "reclass", {"source": "t_dem", "target": "t_recl", "rules": [[100, 110, 1], [110, 120, 2]]}),
        ("gis_clip", "clip_raster", {"source": "t_dem", "target": "t_rclip", "clip_wkt": "POLYGON((0 0,2 0,2 2,0 2,0 0))"}),
        ("gis_clip", "clip_raster", {"source": "t_dem", "target": "t_rclip2", "clip_table": "t_polys"}),
        ("gis_zonal_statistics", "zonal_stats", {"zones": "t_zones", "values": "t_dem", "target": "t_zonal"}),
        ("gis_delete_field", "drop_column", {"table": "t_polys", "fields": ["extra"]}),
        ("gis_delete_dataset", "drop_table", {"table": "t_merged"}),
    ]
    results = []
    for verb, tpl_id, args in cases:
        st, sql, note = render_and_run(verb, tpl_id, args)
        results.append((tpl_id, verb, st, note))
        print("%-22s %-24s %-11s %s" % (tpl_id, verb, st, note))
    npass = sum(1 for r in results if r[2] == "PASS")
    print("\nTOTAL %d/%d PASS" % (npass, len(results)))
    json.dump([{"template": r[0], "verb": r[1], "status": r[2], "note": r[3]} for r in results],
              open(os.path.join(os.getcwd(), "postgis-test-results.json"), "w",
                   encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())

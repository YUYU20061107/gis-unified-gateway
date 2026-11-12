# -*- coding: utf-8 -*-
"""
Calibration probe R1 (for WorkBuddy to run on the fish's Windows machine).

Purpose: B1 proved the method NAMES exist (dir-level). This probe goes one step
further and actually CALLS them on a tiny synthetic dataset inside a throwaway
datasource, to find the working call shapes before batch-1 tool writing.

Targets: V06 create_field, V07 remove_field, V12/V13 append, V29 statistic,
V14 set_prj_coordsys (attempt only), plus record add/update plumbing.

Safety: all writes happen inside ./calib_probe_scratch/ under the CWD, which is
deleted at the end. Nothing outside that folder is touched.

Python 3.5 compatible (SuperMap sm35 runtime). Every step is isolated: a failure
is recorded with its error and the probe continues. Output: one JSON on stdout.
"""
import json
import os
import shutil
import sys
import traceback

RESULT = {"python": sys.version, "phase0": {}, "steps": []}
SCRATCH = os.path.join(os.getcwd(), "calib_probe_scratch")


def record(name, ok, detail=None, error=None):
    rec = {"step": name, "ok": bool(ok)}
    if detail is not None:
        rec["detail"] = detail
    if error is not None:
        rec["error"] = error
    RESULT["steps"].append(rec)
    return rec["ok"]


def attempt(name, fn):
    """Run fn(); record ok + its return-detail, or the exception."""
    try:
        detail = fn()
        return record(name, True, detail=detail)
    except Exception as e:  # noqa: BLE001 - probe must never abort
        record(name, False, error=repr(e) + " | " + traceback.format_exc().strip().splitlines()[-1])
        return False


def variants(name, tries):
    """tries: list of (label, callable). First success wins; all errors kept."""
    errors = []
    for label, fn in tries:
        try:
            detail = fn()
            return record(name, True, detail={"variant": label, "result": detail})
        except Exception as e:  # noqa: BLE001
            errors.append(label + " -> " + repr(e))
    return record(name, False, error=" || ".join(errors))


def member_names(obj):
    try:
        return sorted([m for m in dir(obj) if not m.startswith("_")])
    except Exception as e:  # noqa: BLE001
        return ["<dir failed: " + repr(e) + ">"]


def main():
    # ---------- Phase 0: signature recon for the classes we must construct ----------
    try:
        import iobjectspy
        import iobjectspy.data as sdata
    except Exception as e:  # noqa: BLE001
        record("import_iobjectspy", False, error=repr(e))
        print(json.dumps(RESULT, ensure_ascii=False, indent=1))
        return
    record("import_iobjectspy", True, detail=getattr(iobjectspy, "__version__", "unknown"))

    for cls_name in ("DatasourceConnectionInfo", "FieldInfo", "DatasetVectorInfo"):
        cls = getattr(sdata, cls_name, None) or getattr(iobjectspy, cls_name, None)
        RESULT["phase0"][cls_name] = member_names(cls) if cls is not None else "NOT FOUND"
    root = member_names(iobjectspy)
    RESULT["phase0"]["root_enums"] = [n for n in root if ("Type" in n or "Engine" in n or "Statistic" in n or "Cursor" in n)]
    for enum_name in RESULT["phase0"]["root_enums"]:
        enum_obj = getattr(iobjectspy, enum_name, None)
        if enum_obj is not None:
            RESULT["phase0"]["enum_" + enum_name] = member_names(enum_obj)

    # ---------- Phase 1: build a throwaway datasource ----------
    if os.path.isdir(SCRATCH):
        shutil.rmtree(SCRATCH, ignore_errors=True)
    os.makedirs(SCRATCH)
    udb_path = os.path.join(SCRATCH, "probe.udb")

    holder = {}

    def make_conninfo():
        info = sdata.DatasourceConnectionInfo()
        holder["conninfo_dir"] = member_names(info)
        # Best-effort attribute setting; record exactly which attributes exist.
        settable = {}
        for attr, value in (("server", udb_path), ("alias", "calibprobe")):
            if hasattr(info, attr):
                try:
                    setattr(info, attr, value)
                    settable[attr] = "set ok"
                except Exception as e:  # noqa: BLE001
                    settable[attr] = "set failed: " + repr(e)
            else:
                settable[attr] = "attr missing"
        holder["conninfo_set"] = settable
        return info

    conn = {"obj": None}

    def create_ds():
        info = make_conninfo()
        ds = sdata.create_datasource(info)
        conn["obj"] = ds
        return {"datasource_type": type(ds).__name__, "conninfo": holder.get("conninfo_set")}

    if not attempt("create_datasource", create_ds):
        print(json.dumps(RESULT, ensure_ascii=False, indent=1))
        return
    ds = conn["obj"]

    # ---------- dataset + fields + records ----------
    state = {}

    def create_dataset():
        info_cls = getattr(sdata, "DatasetVectorInfo")
        # Dataset type enum: try the phase-0 discovered enum, fall back to string.
        dtype = None
        for enum_name in ("DatasetType",):
            enum_obj = getattr(iobjectspy, enum_name, None)
            if enum_obj is not None and hasattr(enum_obj, "POINT"):
                dtype = getattr(enum_obj, "POINT")
        tries = []
        if dtype is not None:
            tries.append(("DatasetVectorInfo(name, enum POINT)", lambda: ds.create_vector_dataset(info_cls("probe_pts", dtype))))
        tries.append(("DatasetVectorInfo(name, 'POINT')", lambda: ds.create_vector_dataset(info_cls("probe_pts", "POINT"))))
        tries.append(("create_dataset(name, 'POINT')", lambda: ds.create_dataset("probe_pts", "POINT")))
        ok = variants("create_vector_dataset", tries)
        if ok:
            state["dsv"] = ds.get_dataset("probe_pts")
        return ok

    if not create_dataset():
        print(json.dumps(RESULT, ensure_ascii=False, indent=1))
        return
    dsv = state.get("dsv")
    if dsv is None:
        record("get_dataset", False, error="create reported ok but get_dataset returned None")
        print(json.dumps(RESULT, ensure_ascii=False, indent=1))
        return
    record("get_dataset", True, detail=type(dsv).__name__)

    def make_field(name, type_names):
        field_cls = getattr(sdata, "FieldInfo")
        ftype_cls = getattr(iobjectspy, "FieldType", None) or getattr(sdata, "FieldType", None)
        tries = []
        for tname in type_names:
            tval = getattr(ftype_cls, tname, None) if ftype_cls is not None else None
            if tval is not None:
                tries.append(("FieldInfo(name, FieldType." + tname + ")", lambda t=tval: field_cls(name, t)))
        tries.append(("FieldInfo() + attrs", lambda: _field_by_attrs(field_cls, name)))
        return tries

    def _field_by_attrs(field_cls, name):
        fi = field_cls()
        for attr, val in (("name", name), ("caption", name)):
            if hasattr(fi, attr):
                setattr(fi, attr, val)
        return fi

    def add_fields():
        made = []
        for fname, types in (("score", ("DOUBLE", "FLOAT", "SINGLE")), ("label", ("TEXT", "STRING", "CHAR"))):
            ok = variants("create_field_" + fname, [
                (label, (lambda f=fn: (lambda: (dsv.create_field(f), "created")[1]))(fn))
                for label, fn in make_field(fname, types)
            ])
            made.append(fname + "=" + ("ok" if ok else "fail"))
        return "; ".join(made)

    attempt("create_fields_V06", add_fields)

    def add_records():
        rs = None
        errors = []
        for label, call in (("get_recordset(False)", lambda: dsv.get_recordset(False)),
                            ("get_recordset(True)", lambda: dsv.get_recordset(True)),
                            ("get_recordset()", lambda: dsv.get_recordset())):
            try:
                rs = call()
                state["rs_variant"] = label
                break
            except Exception as e:  # noqa: BLE001
                errors.append(label + " -> " + repr(e))
        if rs is None:
            return record("open_recordset", False, error=" || ".join(errors))
        record("open_recordset", True, detail=state["rs_variant"])
        gp_cls = getattr(sdata, "GeoPoint")
        p2_cls = getattr(sdata, "Point2D")
        rs.add(gp_cls(p2_cls(1.0, 2.0)))
        try:
            rs.set_value("score", 3.5)
        except Exception as e:  # noqa: BLE001
            record("set_value_score", False, error=repr(e))
        rs.update()
        count = rs.get_record_count()
        try:
            rs.close()
        except Exception:  # noqa: BLE001
            pass
        return record("add_record", True, detail={"record_count_after": count})

    add_records()

    def do_statistic():
        rs = dsv.get_recordset(False)
        mode_names = []
        for enum_name in RESULT["phase0"].get("root_enums", []):
            if "Statistic" in enum_name:
                mode_names = member_names(getattr(iobjectspy, enum_name))
        tries = [("statistic('score')", lambda: rs.statistic("score"))]
        stat_enum = None
        for enum_name in RESULT["phase0"].get("root_enums", []):
            if "Statistic" in enum_name:
                stat_enum = getattr(iobjectspy, enum_name)
        if stat_enum is not None:
            for m in ("AVERAGE", "MEAN", "SUM", "MAX"):
                if hasattr(stat_enum, m):
                    mv = getattr(stat_enum, m)
                    tries.append(("statistic('score', " + m + ")", (lambda v=mv: rs.statistic("score", v))))
        ok = variants("field_statistic_V29", tries)
        try:
            rs.close()
        except Exception:  # noqa: BLE001
            pass
        return ok

    do_statistic()

    def do_append():
        # second dataset with one record, then append into the first (V12/V13 path)
        info_cls = getattr(sdata, "DatasetVectorInfo")
        dtype = None
        enum_obj = getattr(iobjectspy, "DatasetType", None)
        if enum_obj is not None and hasattr(enum_obj, "POINT"):
            dtype = getattr(enum_obj, "POINT")
        src = None
        for make in (lambda: ds.create_vector_dataset(info_cls("probe_src", dtype)) if dtype is not None else None,
                     lambda: ds.create_vector_dataset(info_cls("probe_src", "POINT"))):
            try:
                src = make()
                if src is not None:
                    break
            except Exception:  # noqa: BLE001
                src = None
        if src is None:
            src = ds.get_dataset("probe_src")
        if src is None:
            return record("append_V12_V13", False, error="could not create source dataset")
        src = ds.get_dataset("probe_src") or src
        # mirror the score field so schemas are compatible
        variants("src_create_field_score", [
            (label, (lambda f=fn: (lambda: (src.create_field(f), "created")[1]))(fn))
            for label, fn in make_field("score", ("DOUBLE", "FLOAT", "SINGLE"))
        ])
        rs = src.get_recordset(state.get("rs_variant") == "get_recordset(True)")
        gp_cls = getattr(sdata, "GeoPoint")
        p2_cls = getattr(sdata, "Point2D")
        rs.add(gp_cls(p2_cls(5.0, 6.0)))
        rs.update()
        rs.close()
        tries = [("append(source_dataset)", lambda: dsv.append(src)),
                 ("append(source_recordset)", lambda: dsv.append(src.get_recordset(False)))]
        ok = variants("append_V12_V13", tries)
        rs2 = dsv.get_recordset(False)
        cnt = rs2.get_record_count()
        rs2.close()
        record("count_after_append", True, detail={"record_count": cnt})
        return ok

    do_append()

    def do_set_prj():
        prj_cls = getattr(sdata, "PrjCoordSys", None) or getattr(iobjectspy, "PrjCoordSys", None)
        if prj_cls is None:
            return record("assign_projection_V14", False, error="PrjCoordSys class not found")
        tries = [("set_prj_coordsys(PrjCoordSys())", lambda: dsv.set_prj_coordsys(prj_cls()))]
        return variants("assign_projection_V14", tries)

    do_set_prj()

    def do_remove_field():
        before = dsv.get_field_count()
        dsv.remove_field("label")
        after = dsv.get_field_count()
        return record("remove_field_V07", True, detail={"fields_before": before, "fields_after": after})

    do_remove_field()

    # ---------- cleanup ----------
    def cleanup():
        try:
            dsv.close()
        except Exception:  # noqa: BLE001
            pass
        try:
            sdata.close_datasource(ds)
        except Exception:  # noqa: BLE001
            try:
                ds.close()
            except Exception:  # noqa: BLE001
                pass
        shutil.rmtree(SCRATCH, ignore_errors=True)
        return {"scratch_removed": not os.path.isdir(SCRATCH)}

    attempt("cleanup", cleanup)
    print(json.dumps(RESULT, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

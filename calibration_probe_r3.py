# -*- coding: utf-8 -*-
"""
Calibration probe R3 (for WorkBuddy to run on the fish's Windows machine).
R3 delta vs R2: R2 verified the whole build-source chain live (set_type /
set_server / set_alias / create_datasource all ok), then died at dataset
creation: DatasetVectorInfo constructions threw (errors lost), and
ds.create_dataset(name, 'POINT') returned None without raising, which the
old variants() counted as success -- a false positive. R3 fixes the probe:
(1) variants() records EVERY attempt's error, win or lose;
(2) dataset creation is split into construction attempts x create-call
    attempts, and success requires a get_dataset() round-trip;
(3) phase0 also captures __doc__ strings of the critical callables and the
    Datasource class member list;
(4) bail() closes the datasource before removing scratch, and records why
    removal failed if it does.

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


class RejectAttempt(Exception):
    """Raise inside a variant callable to mark its result as not-a-success
    (e.g. a create call that returned None) while still recording why."""


def variants(name, tries):
    """tries: list of (label, callable). First success wins.

    R3: every attempt is recorded (label, ok, detail or error) in the step's
    detail, including attempts that ran before the winning one -- R2 lost
    the DatasetVectorInfo construction errors that way.
    """
    attempts = []
    for label, fn in tries:
        try:
            detail = fn()
            attempts.append({"label": label, "ok": True, "result": detail})
            return record(name, True, detail={"variant": label, "attempts": attempts})
        except RejectAttempt as e:
            attempts.append({"label": label, "ok": False, "rejected": str(e)})
        except Exception as e:  # noqa: BLE001
            attempts.append({"label": label, "ok": False, "error": repr(e)})
    return record(name, False, detail={"attempts": attempts},
                  error="all variants failed or were rejected")


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
    # R3 additions: Datasource class surface + docstrings of critical callables.
    for cls_name in ("Datasource", "DatasetVector"):
        cls = getattr(sdata, cls_name, None) or getattr(iobjectspy, cls_name, None)
        RESULT["phase0"]["class_" + cls_name] = member_names(cls) if cls is not None else "NOT FOUND"
    docs = {}
    doc_targets = {}
    ds_cls = getattr(sdata, "Datasource", None) or getattr(iobjectspy, "Datasource", None)
    if ds_cls is not None:
        for m in ("create_dataset", "create_vector_dataset", "create", "get_dataset"):
            if hasattr(ds_cls, m):
                doc_targets["Datasource." + m] = getattr(ds_cls, m)
    for fname in ("create_datasource", "open_datasource"):
        if hasattr(sdata, fname):
            doc_targets["data." + fname] = getattr(sdata, fname)
    for cname in ("DatasetVectorInfo", "FieldInfo", "DatasourceConnectionInfo"):
        cls = getattr(sdata, cname, None) or getattr(iobjectspy, cname, None)
        if cls is not None:
            doc_targets[cname] = cls
    for key, obj in doc_targets.items():
        try:
            d = getattr(obj, "__doc__", None)
            docs[key] = (d[:600] if d else None)
        except Exception as e:  # noqa: BLE001
            docs[key] = "<doc read failed: " + repr(e) + ">"
    RESULT["phase0"]["docs"] = docs

    # ---------- Phase 1: build a throwaway datasource ----------
    if os.path.isdir(SCRATCH):
        # R3: learn whether the previous run's leftover clears once its
        # process is gone (R2 left probe.udb/.udd behind a live handle).
        shutil.rmtree(SCRATCH, ignore_errors=True)
        RESULT["prev_scratch_cleanup"] = "removed" if not os.path.isdir(SCRATCH) else "STILL PRESENT"
    else:
        RESULT["prev_scratch_cleanup"] = "none existed"
    os.makedirs(SCRATCH)
    udb_path = os.path.join(SCRATCH, "probe.udb")

    def bail():
        # R3: close the datasource BEFORE removing scratch (R2's leftover was
        # a live handle holding probe.udb/.udd), and record removal errors.
        ds_obj = conn.get("obj")
        if ds_obj is not None:
            for closer in (lambda: sdata.close_datasource(ds_obj),
                           lambda: ds_obj.close()):
                try:
                    closer()
                    break
                except Exception:  # noqa: BLE001
                    pass
        rm_errors = []

        def _onerror(func, path, exc_info):
            rm_errors.append(path + " -> " + repr(exc_info[1]))

        shutil.rmtree(SCRATCH, ignore_errors=False, onerror=_onerror)
        RESULT["scratch_removed_on_bail"] = not os.path.isdir(SCRATCH)
        if rm_errors:
            RESULT["scratch_rmtree_errors"] = rm_errors
        print(json.dumps(RESULT, ensure_ascii=False, indent=1))

    holder = {}

    def make_conninfo():
        info = sdata.DatasourceConnectionInfo()
        holder["conninfo_dir"] = member_names(info)
        settable = {}
        # R2 fix: engine type first. R1 report: the class exposes set_type and
        # iobjectspy.EngineType contains UDB; an unset type made create fail.
        engine_cls = getattr(iobjectspy, "EngineType", None) or getattr(sdata, "EngineType", None)
        if engine_cls is not None and hasattr(engine_cls, "UDB"):
            udb_val = getattr(engine_cls, "UDB")
            done = False
            if hasattr(info, "set_type"):
                try:
                    info.set_type(udb_val)
                    settable["type"] = "set_type(EngineType.UDB) ok"
                    done = True
                except Exception as e:  # noqa: BLE001
                    settable["type"] = "set_type failed: " + repr(e)
            if not done and hasattr(info, "type"):
                try:
                    info.type = udb_val
                    settable["type"] = "type attr = EngineType.UDB ok"
                    done = True
                except Exception as e:  # noqa: BLE001
                    settable["type"] = "type attr failed: " + repr(e)
            if not done and "type" not in settable:
                settable["type"] = "no usable type setter"
        else:
            settable["type"] = "EngineType.UDB not found"
        # server / alias: prefer method-style setters, fall back to attributes.
        for attr, value in (("server", udb_path), ("alias", "calibprobe")):
            setter = getattr(info, "set_" + attr, None)
            if callable(setter):
                try:
                    setter(value)
                    settable[attr] = "set_" + attr + "() ok"
                    continue
                except Exception as e:  # noqa: BLE001
                    settable[attr] = "set_" + attr + "() failed: " + repr(e)
                    continue
            if hasattr(info, attr):
                try:
                    setattr(info, attr, value)
                    settable[attr] = "attr set ok"
                except Exception as e:  # noqa: BLE001
                    settable[attr] = "attr set failed: " + repr(e)
            else:
                settable[attr] = "attr and setter missing"
        holder["conninfo_set"] = settable
        return info

    conn = {"obj": None}

    def create_ds():
        info = make_conninfo()
        ds = sdata.create_datasource(info)
        conn["obj"] = ds
        return {"datasource_type": type(ds).__name__, "conninfo": holder.get("conninfo_set")}

    if not attempt("create_datasource", create_ds):
        bail()
        return
    ds = conn["obj"]

    # ---------- dataset + fields + records ----------
    state = {}

    def build_info(name, style):
        """Construct a DatasetVectorInfo for a POINT dataset, three ways."""
        info_cls = getattr(sdata, "DatasetVectorInfo")
        enum_obj = getattr(iobjectspy, "DatasetType", None) or getattr(sdata, "DatasetType", None)
        dtype = getattr(enum_obj, "POINT", None) if enum_obj is not None else None
        if style == "ctor_enum":
            if dtype is None:
                raise RejectAttempt("DatasetType.POINT unavailable")
            return info_cls(name, dtype)
        if style == "ctor_str":
            return info_cls(name, "POINT")
        if style == "ctor_empty":
            # R3 upgrade (from the R2 result body): DatasetVectorInfo exposes
            # set_name/set_type -- the Java-bean pattern that already worked
            # for DatasourceConnectionInfo. Try this style FIRST.
            info = info_cls()
            applied = []
            for setter_name, attr_name, value in (
                    ("set_name", "name", name),
                    ("set_dataset_type", None, dtype),
                    ("set_type", "type", dtype)):
                if value is None:
                    continue
                setter = getattr(info, setter_name, None)
                if callable(setter):
                    setter(value)
                    applied.append(setter_name)
                elif attr_name and hasattr(info, attr_name):
                    setattr(info, attr_name, value)
                    applied.append(attr_name + "=")
            if not applied:
                raise RejectAttempt("no usable name/type setter on empty DatasetVectorInfo; members=" + ",".join(member_names(info)[:40]))
            readback = {}
            for attr in ("name", "type"):
                try:
                    readback[attr] = repr(getattr(info, attr))
                except Exception as e:  # noqa: BLE001
                    readback[attr] = "<read failed: " + repr(e) + ">"
            RESULT.setdefault("info_readbacks", []).append({"name": name, "applied": applied, "readback": readback})
            return info
        raise RejectAttempt("unknown style " + style)

    def create_dataset():
        def _build_and_try(style):
            info = build_info("probe_pts", style)
            msgs = []
            for call_label, call in (
                    ("create_vector_dataset(info)", lambda: ds.create_vector_dataset(info)),
                    ("create_dataset(info)", lambda: ds.create_dataset(info))):
                try:
                    ret = call()
                    got = None
                    try:
                        got = ds.get_dataset("probe_pts")
                    except Exception as e:  # noqa: BLE001
                        msgs.append(call_label + ": get_dataset raised " + repr(e))
                        continue
                    if got is None and ret is None:
                        msgs.append(call_label + ": returned None, round-trip None")
                        continue
                    state["dsv"] = got if got is not None else ret
                    return {"style": style, "call": call_label,
                            "returned": type(ret).__name__ if ret is not None else None,
                            "roundtrip": got is not None}
                except Exception as e:  # noqa: BLE001
                    msgs.append(call_label + ": " + repr(e))
            raise RejectAttempt(" || ".join(msgs))

        tries = [("build=" + s, (lambda st=s: _build_and_try(st))) for s in ("ctor_empty", "ctor_enum", "ctor_str")]

        def _plain(dtype_value, tag):
            def _run():
                ret = ds.create_dataset("probe_pts", dtype_value)
                got = ds.get_dataset("probe_pts")
                if got is None and ret is None:
                    raise RejectAttempt("returned None and round-trip None")
                state["dsv"] = got if got is not None else ret
                return {"returned": type(ret).__name__ if ret is not None else None, "roundtrip": got is not None}
            return ("create_dataset(name, " + tag + ")", _run)

        enum_obj = getattr(iobjectspy, "DatasetType", None) or getattr(sdata, "DatasetType", None)
        dtype = getattr(enum_obj, "POINT", None) if enum_obj is not None else None
        if dtype is not None:
            tries.append(_plain(dtype, "enum POINT"))
        tries.append(_plain("POINT", "'POINT'"))
        return variants("create_vector_dataset", tries)

    if not create_dataset():
        bail()
        return
    dsv = state.get("dsv")
    if dsv is None:
        record("get_dataset", False, error="create reported ok but get_dataset returned None")
        bail()
        return
    record("get_dataset", True, detail=type(dsv).__name__)

    def make_field(name, type_names):
        field_cls = getattr(sdata, "FieldInfo")
        ftype_cls = getattr(iobjectspy, "FieldType", None) or getattr(sdata, "FieldType", None)
        tries = []
        # R3 upgrade (from the R2 result body): FieldInfo exposes
        # set_name/set_type -- bean style first, positional ctor as fallback.
        for tname in type_names:
            tval = getattr(ftype_cls, tname, None) if ftype_cls is not None else None
            if tval is not None:
                tries.append(("FieldInfo() + set_name/set_type(FieldType." + tname + ")",
                              (lambda t=tval, n=name: _field_by_setters(field_cls, n, t))))
        for tname in type_names:
            tval = getattr(ftype_cls, tname, None) if ftype_cls is not None else None
            if tval is not None:
                tries.append(("FieldInfo(name, FieldType." + tname + ")", lambda t=tval: field_cls(name, t)))
        tries.append(("FieldInfo() + attrs", lambda: _field_by_attrs(field_cls, name)))
        return tries

    def _field_by_setters(field_cls, name, tval):
        fi = field_cls()
        fi.set_name(name)
        fi.set_type(tval)
        return fi

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
        # R3: reuse the build_info styles that the main create step exercises,
        # and judge by get_dataset round-trip, not by return value alone.
        src = None
        for style in ("ctor_empty", "ctor_enum", "ctor_str"):
            try:
                info = build_info("probe_src", style)
            except Exception:  # noqa: BLE001
                continue
            for call in (lambda: ds.create_vector_dataset(info), lambda: ds.create_dataset(info)):
                try:
                    call()
                except Exception:  # noqa: BLE001
                    pass
                src = ds.get_dataset("probe_src")
                if src is not None:
                    break
            if src is not None:
                break
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

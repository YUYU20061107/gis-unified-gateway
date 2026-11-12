# -*- coding: utf-8 -*-
"""
B1 二轮下钻脚本：对 iobjectspy 核心类做 dir() 自省，补一轮模块级扫描的盲区。

一轮结论（2026-11-03）：V06 加字段、V07 删字段、V12 合并在模块级无对应函数，
疑为 DatasetVector 等核心类的方法；V20 的 difference 与 erase 关系需看 OverlayMode
枚举成员；V14/V15 的类级路径（PrjCoordSys / CoordSysTranslator）需看方法面。

用法（在 E:\\ds工作区 里）：
    E:\\ds工作区\\.venvs\\sm35\\python.exe introspect_iobjectspy_r2.py > introspect-r2-result.json
把 introspect-r2-result.json 回传给 Muse 对账即可。

只读自省：只对类对象做 dir() 与 getattr 取名，不实例化、不调用任何方法、不写数据。
环境：Python 3.5.4 + iobjectspy 10.1.0.0。写法按 3.5 兼容（无 f-string）。
"""
import json
import sys
import traceback

# 要下钻的类：名字 -> 与之相关的待验动词（仅用于报告标注）
TARGET_CLASSES = {
    "DatasetVector":      ["V06 add_field", "V07 delete_field", "V12 merge/append", "V13 append", "V29 field_statistics", "V14 assign_projection"],
    "Dataset":            ["V14 assign_projection", "V15 reproject"],
    "DatasetGrid":        ["V29 raster statistics ref"],
    "Recordset":          ["V08 calculate_field ref", "V07 delete_field ref"],
    "Datasource":         ["V12 merge/append ref"],
    "CoordSysTranslator": ["V15 reproject"],
    "PrjCoordSys":        ["V14 assign_projection"],
    "OverlayMode":        ["V20 difference vs erase"],
    "QueryParameter":     ["V22 spatial_join alt path"],
    "JoinItem":           ["V22 spatial_join ref"],
}

# 类可能出现的模块路径（逐个尝试，取到为止）
MODULE_CANDIDATES = [
    "iobjectspy",
    "iobjectspy.data",
    "iobjectspy.analyst",
    "iobjectspy.conversion",
    "iobjectspy.mapping",
    "iobjectspy.data.supermap",
    "iobjectspy.analyst.supermap",
    "iobjectspy.conversion.supermap",
    "iobjectspy.mapping.supermap",
    "iobjectspy.supermap",
]

# 命中关键词（小写子串），按动词分组
WANTED_PATTERNS = {
    "field":       ["field"],
    "appendMerge": ["append", "merge"],
    "join":        ["join"],
    "statistics":  ["statistic", "summar"],
    "coordsys":    ["prj", "coord", "translat", "convert", "project"],
    "overlay":     ["overlay", "difference", "erase", "intersect", "union", "identity", "update", "xor", "clip"],
    "delete":      ["delete", "remove", "drop"],
}


def find_class(name):
    """在候选模块里逐个找类对象，返回 (module_path, cls) 或 (None, None)。"""
    for path in MODULE_CANDIDATES:
        try:
            mod = __import__(path, fromlist=["*"])
        except Exception:
            continue
        obj = getattr(mod, name, None)
        if obj is not None and isinstance(obj, type):
            return path, obj
    return None, None


def class_members(cls):
    try:
        names = sorted(n for n in dir(cls) if not n.startswith("__"))
    except Exception:
        return []
    return names


def main():
    out = {"python": sys.version, "classes": {}, "pattern_hits": {}}
    for cname, verbs in TARGET_CLASSES.items():
        entry = {"for_verbs": verbs, "found_in": None, "members": [], "error": None}
        try:
            path, cls = find_class(cname)
            if cls is None:
                entry["error"] = "class not found in any candidate module"
            else:
                entry["found_in"] = path
                entry["members"] = class_members(cls)
        except Exception:
            entry["error"] = traceback.format_exc()
        out["classes"][cname] = entry

    # 关键词命中汇总：{pattern_group: {class: [members...]}}
    for group, pats in WANTED_PATTERNS.items():
        hits = {}
        for cname, entry in out["classes"].items():
            matched = [m for m in entry["members"]
                       if any(p in m.lower() for p in pats)]
            if matched:
                hits[cname] = matched
        out["pattern_hits"][group] = hits

    sys.stdout.write(json.dumps(out, ensure_ascii=False, indent=1))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()

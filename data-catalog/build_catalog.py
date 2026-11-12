# -*- coding: utf-8 -*-
"""build_catalog.py — 把 datasets/<id>/dataset.json 汇总生成 catalog.json 全量索引。

路子同 gateway 的 build_mapping.py：登记文件是唯一事实源，本脚本逐条校验后才
允许进索引，缺字段/许可无据/id 与目录名不一致就报错退出，不许带病汇总。
校验项：
  - 必填字段齐全（PHASE-B 登记表）
  - id 必须与所在目录名一致
  - license 必带 evidence_ref（许可要有据可查），commercial_use 只能是
    true/false/"unknown"
  - status 只能是 registered / verified / deprecated
生成物 catalog.json 含 counts（按 type / license / commercial_use），供
catalog_server.py 与网关 gis_discover 的 data_catalog 一节对账。
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "catalog.json")

REQUIRED = ["id", "name", "type", "source", "license", "coverage",
            "format", "update", "storage", "quality_notes", "status"]
TYPES = ["vector", "raster", "imagery", "dem", "poi", "network", "table"]
STATUSES = ["registered", "verified", "deprecated"]


def fail(msg):
    print("FAIL: %s" % msg, file=sys.stderr)
    sys.exit(1)


def main():
    base = os.path.join(HERE, "datasets")
    records = []
    for did in sorted(os.listdir(base)):
        p = os.path.join(base, did, "dataset.json")
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8") as f:
            rec = json.load(f)
        for k in REQUIRED:
            if k not in rec:
                fail("%s 缺必填字段 %s" % (did, k))
        if rec["id"] != did:
            fail("%s 的 id=%r 与目录名不一致" % (did, rec["id"]))
        if rec["type"] not in TYPES:
            fail("%s 的 type=%r 不在登记表枚举内" % (did, rec["type"]))
        if rec["status"] not in STATUSES:
            fail("%s 的 status=%r 不在枚举内" % (did, rec["status"]))
        lic = rec["license"]
        if not lic.get("evidence_ref"):
            fail("%s 的 license 缺 evidence_ref（许可必须有据可查）" % did)
        if lic.get("commercial_use") not in (True, False, "unknown"):
            fail("%s 的 license.commercial_use=%r 非法（只能 true/false/unknown）"
                 % (did, lic.get("commercial_use")))
        records.append(rec)

    by_type, by_license, by_cu = {}, {}, {}
    for r in records:
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1
        by_license[r["license"]["name"]] = by_license.get(r["license"]["name"], 0) + 1
        k = str(r["license"]["commercial_use"])
        by_cu[k] = by_cu.get(k, 0) + 1

    out = {
        "title": "GIS 平台数据目录（data-catalog）",
        "generated_by": "data-catalog/build_catalog.py",
        "generated_at": datetime.datetime.now(datetime.timezone.utc)
                        .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "evidence_level": "登记索引：status=registered 表示仅登记、未打开数据本体验证；"
                          "许可口径引 MATERIALS-INDEX 第二部分并逐条带 evidence_ref。",
        "counts": {"total": len(records), "by_type": by_type,
                   "by_license": by_license, "by_commercial_use": by_cu},
        "datasets": records,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("wrote %s (%d datasets)" % (OUT, len(records)))


if __name__ == "__main__":
    main()

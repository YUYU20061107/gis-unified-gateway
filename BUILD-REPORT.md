# BUILD-REPORT — 能力账本复探与漂移降级（v0.4 补充修复单）

施工：Muse，2026-11-14。源树 `gateway-public-staging/` 只读未动；
本目录 `gateway-v04-work/` 为施工副本。未推送、未发布、未发任何外部消息。

## 文件清单（相对源树的增减）

| 文件 | 变更 |
|---|---|
| `reprobe.py` | **新增**：复探命令（见下） |
| `leaves-full.json` | **修改（纯 additive）**：208 叶每叶补 `last_verified_at=null`、`last_probe_result=null`、`history=[]`；状态计数不变（ok 165／unverified 21／not_supported 22） |
| `code/selftest.py` | **修改（纯 additive）**：末尾加 D 段 1 项检查＋`import datetime`；原有检查一字未动 |
| `reports/reprobe-20261114-104321-579.{json,md}` | **新增**：本机真实全量复探的漂移报告（证据，见场景 E） |
| `code/selftest-results.txt` | 自检运行产物（可再生）：最终自检结果 155/155 |

注：修复单口径中的「leaves.json」即本树的 `leaves-full.json`（208 叶 dict
账本，自检 A 段与状态对账均读它）；树根另一份 `leaves.json`（132 条位置
元组导出）不是正账，未动。

## 实现要点（reprobe.py，纯标准库）

- **探针口径**：服务器型叶子复用 `code/backends.json` 登记的后端 MCP 服务
  本身——spawn 后 initialize＋tools/list，再调用后端自带的 `*_ping` 健康
  检查；登记 `native` 不在工具面内 = fail。只调用 tools/list 与 *_ping，
  **从不执行叶子工具**，无写副作用。通道类叶子（gp_channel／
  processing_channel，共 3 叶）算法级实机属写操作，只做工具面校验并列入
  报告「人工复探清单」。registry 型叶子（V03/V04 共 9 叶）校验其数据源
  文件（processing/gp 注册表、postgis 模板）可解析、非空且动词仍在
  verbs.json。
- **三态**：pass＝后端在活且登记工具在工具面；fail＝后端在活但工具消失；
  unreachable＝进程起不来／无应答／`*_ping` 报告其实机运行时不可用
  （GIS 桌面软件、GDAL、qgis_process 等不在本机时属此态，**不降级**）。
- **账本更新**：每叶写 `last_verified_at`（带时区 ISO）、`last_probe_result`、
  history 追加 `{at, probe, result, evidence}`；fail 且原 ok → 降
  unverified；unreachable 只记录，history 尾部连续 ≥3 次 unreachable 在
  报告标 stale；升回 ok 只许 `--include-unverified` 显式复探 unverified
  叶子且 pass 时触发。not_supported 叶子不探。
- **报告与退出码**：每次运行落 `reports/reprobe-<时间戳-毫秒>.{json,md}`
  （总数、三态清单、降/升清单、stale、人工清单、逐叶状态 diff、仅字段
  更新计数）；有降级退出 1，无降级退出 0，参数/IO 错误退出 2。
- 施工中修复的一个真缺陷：报告文件名原以秒为粒度，同秒两次运行会互相
  覆盖，已加毫秒后缀。

## 验收实测（修复单 §5 逐项）

夹具：仓内 `code/mock_server.py` 作可控 stub 后端（工具面由夹具
tools.json 控制），夹具账本 3 叶（stub×2＋stub2×1）。

| 场景 | 跑法 | 实测 |
|---|---|---|
| §5.2 全过 | 夹具全工具在位，跑 `reprobe.py --ledger 夹具 --backends 夹具` | pass 3／fail 0／unreachable 0，**退出 0**，报告 status_diff 为空，仅新鲜度字段更新 |
| §5.1 假失效 | 从夹具工具面删 `stub_beta`（模拟后端升级弄丢工具）后重跑 | T02 判 fail → **自动降级 unverified**，报告含该叶 status diff，**退出 1** |
| §3.2 升回 | 恢复 `stub_beta`，跑 `--include-unverified` | T02 pass → **升回 ok**，history 依次为 pass/fail/pass |
| §5.3 unreachable | stub2 命令指向不存在的服务脚本，连跑 3 次 | T03 三次均 unreachable、**状态保持 ok 不降级**，退出均 0；第 3 次报告 stale 清单含 T03 |
| §5.4 自检 | 工作副本跑 `code/selftest.py`，与基线逐项比对检查名 | 基线 **154/154**（源树副本未改时）；改后 **155/155**，原 154 项检查名零缺失、判定零变化，新增 D1「账本新鲜度字段自洽（208 叶）」PASS |
| §5.5 兼容 | 账本补字段后（先验）与最终版各跑一遍完整自检 | 两遍均全过；其中 B30/B31/B35/B40 的 UNVERIFIED_MAPPING 拒绝路径在新版账本下判定不变 |
| 场景 E 真实全量 | 真实账本副本＋真实 backends.json 在本机全量复探（165 叶） | pass 10（9 registry＋1 iserver）／unreachable 155／fail 0，**退出 0、零降级**；各桥后端均能应答 tools/list，但其 `*_ping` 如实报告实机运行时（ArcGIS/QGIS/SuperMap/GDAL/qgis_process/PostGIS DSN）不在本机 → unreachable，符合口径。报告存 `reports/` |

## 边界与未尽项（如实）

- 本机无任何实机 GIS 运行时，真实账本的 fail 路径只能由夹具场景证明
  （§5.1），实机环境下的全量 fail/降级需在装有后端的机器上再跑一遍
  `python3 reprobe.py` 即可（账本已备好字段）。
- PostGIS 生产 DSN 维持 deferred：本机其后端命令为 Windows 路径，
  复探记 unreachable 并注明原因，未在本单内解决（按护栏）。
- iServer 叶子在本机判 pass：其后端服务（iserver_server.py）应答且
  iserver_ping 通过、工具面齐全——这是该后端自带的最小实机检查口径，
  非人工浏览演示站复核。

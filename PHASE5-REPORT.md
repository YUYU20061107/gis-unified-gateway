# PHASE 5 · 收口报告

- 日期：2026-11-06
- 状态：**通过**
- 快照说明：本报告是 Phase 5 时点的账（207/164/21/22；tier 174/29/4；
  自检 153）。阶段 3 解封后新增 iServer V35 1 叶，当前终账
  **208＝ok 165＋unverified 21＋not_supported 22**；tier
  **core 174／extended 30／exclusive 4**；自检 154/154。
  见 `PHASE3-REPORT.md`。Phase 4B 另完成 PostGIS 隔离本地集群真后端
  （模板 38/38 + 网关 21/21，calibrated 仅限该集群；生产 DSN 未配置），
  账本叶数不变，见 `PHASE4-POSTGIS-REPORT.md`。
- 起点：`0e3ed5c`（Phase 4 验收提交）→ 本阶段提交
- 说明：阶段 3（iServer）无本机实例，经用户批准记 **deferred-unverified**；
  本阶段不把 iServer 写进正式后端。
- 证据目录：`evidence/phase5/`

## 1. 目标

tier 三级中 exclusive 的悬置候选给出裁决；全部文档数字与账本终对账；
写总 CHANGELOG。

## 2. 实际完成

### 2.1 tier exclusive 裁决

裁为 **exclusive** 的 4 叶：

| 叶 | 状态 | 理由 |
|---|---|---|
| V01 gis_run_gp @arcgis-pro | ok | ArcPy 算法宇宙通道，无跨平台语义对应 |
| V01 gis_run_gp @arcmap | not_supported | 同上；ArcMap 冻结存量不改变其通道语义 |
| V02 gis_run_processing @qgis | ok | QGIS Processing 算法宇宙通道 |
| V02 gis_run_processing @qgis-cli | ok | 同一 QGIS Processing 通道的无头形态 |

裁决理由：这些动词暴露的是**厂商自有算法宇宙**，参数与算法 ID 均绑定厂商；
“经通道执行后端自有算法”只是元语义，不足以把两个厂商通道合并成
core/extended。若将来要通用化，应新开独立的通用 `run_algorithm` 契约，
不把厂商通道混作通用语义。

最终 tier 分布：**core 174／extended 29／exclusive 4**（总 207）。
G3 §4 的悬置候选由此关账；Phase 4 新增的 qgis-cli V02 一并纳入同一裁决。

### 2.2 终对账

| 项目 | Phase 4 | Phase 5 | 说明 |
|---|---|---|---|
| 后端数 | 10 | **10** | 不变 |
| 叶子总数 | 207 | **207** | 不变 |
| ok | 164 | **164** | 不变 |
| unverified | 21 | **21** | 不变 |
| not_supported | 22 | **22** | 不变 |
| pending／existing | 21／22 | **21／22** | 不变 |
| tier core／extended／exclusive | 174／33／0 | **174／29／4** | exclusive 裁决 |
| 自检 | 152/152 | **153/153** | 新增 A10 tier 断言 |
| 生成器 6 产物 | 6/6 | **6/6** | 干净副本字节一致 |
| 真后端 e2e | 9/9 | **9/9** | gdal + qgis-cli |
| 运行时版本 | 0.2.0 | **0.3.0** | 版本落码 |

证据：`evidence/phase5/accounting.txt`、`evidence/phase5/selftest-153.log`、
`evidence/phase5/product-compare.txt`、`evidence/phase5/real-backends-results.json`。

### 2.3 版本落码

- `code/gateway.py`：文件头 v0.3、`SERVER_VERSION = "0.3.0"`、
  启动日志与工具面错误文案同步。
- `code/README.md`：标题升 **v0.3（gateway-v03）**，新增 v0.3 增量段。
- `code/selftest.py`：文档头与结果文件头升 v0.3。
- 生成器 `generated_by` 字符串保留 `gateway-v02` 来源标识（历史来源，
  不代表运行时版本）；已在 README/本报告注明。

### 2.4 总 CHANGELOG

新增 `CHANGELOG.md`：Added（GDAL、qgis-cli、双真后端）、Changed（207 账本、
V32、exclusive、0.3.0）、Fixed（7 模板、B1、Windows 编码/换行）、
Deferred（iServer、PostGIS e2e、余下动词、原始 manifest）、提交清单与证据索引。

### 2.5 文档终对账

- `code/README.md`：v0.3；207/164/21/22；tier 174/29/4；153 checks。
- `V03-WORKLIST-V2-...`：Phase 5 终账行 + Phase 5 执行记录。
- `V03-WORKLIST.md`：历史横幅指向 Phase 5 终账。
- `G3-TAGGING-CHANGELOG`：§7 exclusive 裁决。
- `PHASE1/2/4` 报告：快照说明指向 Phase 5 终账。
- `PHASE3-REPORT.md`：iServer 阻塞记录；本阶段追加 deferred 结论。

## 3. 未完成与原因

1. **iServer（阶段 3）**：本机无实例；记 `deferred-unverified`，未写入
   `backends.json`/`mapping.json`/`leaves-full.json`。拿到实例 URL 后另开
   阶段补探针与最小映射。
2. **PostGIS 真后端**：服务在跑但数据库密码未提供；阶段 4 用 GDAL +
   qgis-cli 满足两真后端。拿到 DSN 后可补一条 PostGIS e2e。
3. **GDAL/qgis-cli 余下动词**：见 Phase 2/4 报告；不登记不冒充。
4. **原始 manifest**：未提供；重建 manifest 的 scope_note 与在册
   `mapping.json` 逐字一致，6/6 字节一致；拿到原件后可再跑一次复核。
5. **in-app qgis 桥**：仍未实机校准；qgis-cli 是独立无头后端，不替代它。

## 4. 下一阶段入口条件

阶段 5 已收口；项目当前可交付状态：

- 10 后端（含 2 个 v0.3 新增真后端）；
- 207 叶，ok 164／unverified 21／not_supported 22；
- tier 三级全部在用：core 174／extended 29／exclusive 4；
- 自检 153/153；生成器 6/6；同一网关两真后端 9/9；
- 运行时版本 0.3.0。

后续若补 iServer/PostGIS，应按新阶段接入契约与证据纪律另开报告，不改写
本次终账的历史快照。

## 5. 证据索引

- `evidence/phase5/accounting.txt`：终账对照
- `evidence/phase5/selftest-153.log` / `selftest-results-153.txt`：153/153
- `evidence/phase5/product-compare.txt`：干净副本 6/6
- `evidence/phase5/real-backends-153.log` / `real-backends-results.json`：9/9
- `evidence/phase5/generator-phase5.log`：生成器 stdout
- `CHANGELOG.md`：总变更日志

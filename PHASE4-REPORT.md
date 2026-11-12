# PHASE 4 · 真后端端到端报告

- 日期：2026-11-06
- 状态：**通过**
- 快照说明：本报告是 Phase 4 时点的 tier（core 174／extended 33／exclusive 0）。
  Phase 5 exclusive 裁决后为 **core 174／extended 29／exclusive 4**；
  Phase 3 iServer 增补后当前终账 **208／ok 165／unverified 21／not_supported 22**，
  tier **174／30／4**；见 `PHASE5-REPORT.md` / `PHASE3-REPORT.md`。
- **Phase 4B 增补**：PostGIS 隔离本地集群真后端 38/38 模板 + 21/21 网关，
  见 `PHASE4-POSTGIS-REPORT.md`；账本叶数不变。
- 执行顺序说明：阶段 3（iServer）因本机无实例阻塞；经用户批准**改序**先做阶段 4。
- 起点：`b829322`（Phase 2 验收提交）→ 本阶段提交
- 环境：Windows 10.0.26300 x64；Python 3.12.9；QGIS 3.44.15；GDAL 3.13.3
- 证据目录：`evidence/phase4/`

## 1. 目标

让同一个 `gateway.py` 进程对**至少两个真实后端**跑通端到端调用，把
「进程级 live（mock）」推进到「真实后端 live」，证据落盘。

## 2. 实际完成（带证据）

### 2.1 第二个真后端：qgis-cli（无头 Processing）

- 新增 `code/qgis_cli_server.py`：纯标准库 stdio MCP，调用本地
  `qgis_process` 3.44.15；工具面仅 `qgis_ping`、`qgis_discover`、
  `qgis_run_processing`。
- 与现有 in-app `qgis` 桥**分开**：qgis-cli 只做无头 Processing，不冒充
  打开工程/图层视图；原有 qgis 映射不变。
- `code/backends.json` 注册第 10 后端：
  `command=["{python}","{here}/qgis_cli_server.py"]`，`mode=processing-cli`，
  `calibration.level=calibrated`，证据范围为“qgis_process 无头实跑
  native:buffer；仅 Processing 通道”。
- `gateway.py` 的 `dispatch_run_processing` 由硬编码 `get_client("qgis")`
  改为 `get_client(backend)`；qgis 与 qgis-cli 共用同一 Processing 契约，
  不再为单个后端开特例。

### 2.2 注册表与账本

- 基础 8 动词：qgis-cli 只开 `gis_ping`、`gis_discover`；工程/地图/图层/
  数据集/显隐/缩放如实 NULL。
- 40 动词中落 3 叶：
  - V02 `gis_run_processing`：`processing_channel`，原生 `qgis_run_processing`；
  - V03 `gis_list_algorithms`：`registry=processing`（网关本地 374 条）；
  - V04 `gis_describe_algorithm`：`registry=processing`（本地条目）。
- 账本：204 → **207＝ok 164＋unverified 21＋not_supported 22**；
  `existing` 21→22（仅 V02 新增），`pending` 21 不变；
  tier core 172→174、extended 32→33、exclusive 0。

### 2.3 同一网关、两个真后端：9/9 PASS

`test_real_backends.py` 用临时 `backends.json` 只注册 gdal + qgis-cli，
启动**同一个** `gateway.py` 子进程，真实调用：

```
checks: 9, passed: 9, failed: 0
```

| # | 调用 | 结果 |
|---|---|---|
| 1 | gis_ping@gdal | GDAL 3.13.3 |
| 2 | gis_ping@qgis-cli | QGIS 3.44.15 |
| 3 | gis_discover@gdal | 6 个 v02 动词 |
| 4 | gis_discover@qgis-cli | V02/V03/V04 |
| 5 | gis_convert_format@gdal | GeoJSON→GPKG 真实产出 |
| 6 | gis_slope@gdal | gdaldem slope 真实产出 |
| 7 | gis_run_processing@qgis-cli | native:buffer 真实产出（网关确认门后） |
| 8 | gis_list_algorithms@qgis-cli | 本地 Processing 注册表 374 |
| 9 | gis_describe_algorithm@qgis-cli | native:buffer 条目 |

证据：`evidence/phase4/real-backends-results.json`、
`evidence/phase4/real-backends.log`。

### 2.4 注册表 / 生成器 / 自检同步

- 干净副本重跑 `build_mapping.py`：6 个产物**全部字节级一致**。
- 自检 **152/152**：A 9、B 128、C 15（C11 gdal、C12 qgis-cli mock discover；
  真实目录三项顺延为 C13–C15）。
- 证据：`evidence/phase4/product-compare.txt`、
  `evidence/phase4/selftest-152.log`、`evidence/phase4/selftest-results-152.txt`。

### 2.5 文档同步

- `code/README.md`：总账 207/164/21/22、10 后端、qgis-cli 范围条目、文件表、
  验证级别表、自检 152。
- `V03-WORKLIST-V2-...`：终账行 + Phase 4 执行记录。
- `V03-WORKLIST.md`：历史横幅更新到 207。
- `G3-TAGGING-CHANGELOG`：Phase 4 增补注。
- `PHASE1-REPORT.md` / `PHASE2-REPORT.md`：顶部快照说明指向 207。

## 3. 账面数字变化对照表

| 项目 | 阶段前 | 阶段后 | 变化与理由 |
|---|---|---|---|
| 后端数 | 9 | **10** | 新增 qgis-cli |
| 叶子总数 | 204 | **207** | +3 条 qgis-cli 叶 |
| ok | 161 | **164** | +3（V02/V03/V04） |
| unverified | 21 | **21** | 不变 |
| not_supported | 22 | **22** | 不变 |
| pending / existing | 21 / 21 | **21 / 22** | 仅 V02 qgis-cli existing |
| tier core/extended/exclusive | 172/32/0 | **174/33/0** | V03/V04 core，V02 extended |
| 自检 | 151/151 | **152/152** | C12 qgis-cli mock discover |
| 生成器产物一致 | 6/6 | **6/6** | 含 qgis-cli 注册表 |
| 真后端 e2e | 1 个（gdal） | **2 个（gdal + qgis-cli）** | 同一网关进程 9/9 |

## 4. `git diff` 逐项解释

| 文件 | 改动 | 原因 |
|---|---|---|
| `code/qgis_cli_server.py` | 新增 3 工具 stdio 服务 | QGIS 无头 Processing 适配层 |
| `test_real_backends.py` | 新增 9 项验收 | 同一网关接两个真后端 |
| `code/gateway.py` | Processing 通道按 backend 取客户端 | qgis/qgis-cli 共用契约，去特例 |
| `code/backends.json` | +qgis-cli 条目、注释更新 | 第 10 后端注册 |
| `code/build_mapping.py` | +QGIS_CLI_TOOLS、BACKENDS/PKG、基础 TABLE、V02/V03/V04、BACKEND_META、native 校验 | 生成器与注册表同账 |
| `code/mapping.json` | +qgis-cli 基础映射 | 生成器产出 |
| `code/verbs.json` | +qgis-cli V02/V03/V04 映射 | 生成器产出 |
| `code/mock_tools.json` | +qgis-cli 工具面 | 自检 mock 用 |
| `code/selftest.py` | A7 覆盖 qgis-cli、C12 qgis-cli discover、C 编号顺延、write_cfg 加 qgis-cli | 离线自检覆盖新后端 |
| `code/selftest-results.txt` | 152/152 | 实测输出 |
| `leaves-full.json` | +3 条 qgis-cli 叶 | 账本 |
| `code/README.md` / 三份 changelog | 207/164/21、qgis-cli 说明 | 文档同步 |
| `evidence/phase4/*` | 真跑结果、日志、6/6 比对、账面变化 | 证据落盘 |

## 5. 未完成与原因

1. **Phase 3 iServer 仍阻塞**：本机无 iServer；Phase 4 是经用户批准改序先做，
   iServer 评估仍未启动。
2. **PostGIS 未用于 Phase 4**：本机 PostgreSQL 16 服务在跑，但数据库密码
   未提供（`psql -w` 报 `no password supplied`）；为不猜凭据，改用
   GDAL + qgis-cli 满足“两个真实后端”。拿到密码/DSN 后可补 PostGIS e2e。
3. **qgis-cli 首版只开 V02/V03/V04**：不提供 in-app 工程/图层视图；原
   `qgis` in-app 桥仍未实机校准。
4. **GDAL 余下动词未注册**：见 Phase 2 报告。
5. **原始 manifest 仍未提供**；生成器重跑沿用重建 manifest，6/6 字节一致。
6. **版本号未升 v0.3**；留阶段 5。

## 6. 下一阶段入口条件

- 阶段 4 目标已满足：同一网关 + 两个真实后端 + 9/9 真实产出。
- **阶段 3（iServer）仍未完成**，入口条件不变：需要本机/内网 iServer base URL、
  版本与认证方式；或再次批准“iServer 后置、先做阶段 5 收口”。
- 若继续按原计划，下一步是阶段 3；阶段 5 不应在阶段 3 未裁决前启动。

## 7. 证据索引

- `evidence/phase4/real-backends-results.json`：9 项真跑逐项结果
- `evidence/phase4/real-backends.log`：完整输出
- `evidence/phase4/product-compare.txt`：干净副本 6/6 产物一致
- `evidence/phase4/selftest-152.log`：152/152 完整输出
- `evidence/phase4/selftest-results-152.txt`：自检结果文件副本
- `evidence/phase4/generator-phase4.log`：生成器重跑 stdout
- `evidence/phase4/accounting.txt`：Phase 4 账面变化

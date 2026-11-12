# PHASE 2 · GDAL 后端接入报告

- 日期：2026-11-06
- 状态：**通过**
- 快照说明：本报告是 Phase 2 时点的账（204/161/21/22）。Phase 4 增 qgis-cli 3 叶、
  Phase 3 增 iServer V35 1 叶后，当前终账为
  **208＝ok 165＋unverified 21＋not_supported 22**；见 `PHASE3-REPORT.md`。
- 起点：`5e4e7c5`（Phase 1 验收提交）→ 本阶段提交
- 环境：Windows 10.0.26300 x64；Python 3.12.9；QGIS 3.44.15 自带 GDAL 3.13.3
- 证据目录：`evidence/phase2/`

## 1. 目标

按现有后端接入契约实现 `gdal` 适配层，先覆盖栅格与矢量最常用的动词子集；
每条 ok 映射必须有本地 GDAL 实跑证据，未跑通的诚实记 unverified 或不登记。

## 2. 实际完成（带证据）

### 2.1 第 9 个后端：gdal

- 新增 `code/gdal_server.py`：纯标准库 stdio MCP 服务，调用本地 GDAL CLI，
  不依赖 Python `osgeo`，因此可用网关自身解释器启动。
- 工具面 8 个：`gdal_ping`、`gdal_discover`、`gdal_reproject`、
  `gdal_convert_format`、`gdal_clip`、`gdal_slope`、`gdal_aspect`、
  `gdal_hillshade`。
- `code/backends.json` 注册：`command=["{python}","{here}/gdal_server.py"]`，
  `mode=local-cli`，`calibration.level=calibrated`，证据范围明确写为
  **桥层 8 工具本地 CLI 实跑；网关 e2e 已过 discover/convert_format/slope**。
- GDAL 环境修正：本机 `PROJ_LIB/GDAL_DATA` 被 PostgreSQL 16 占用，
  `gdal_server.py` 在子进程环境中显式指向 QGIS 的 `share/proj` 与
  `apps/gdal/share/gdal`；否则 EPSG 解析会失败（已实测并修复）。

### 2.2 映射与账本

- 基础 8 动词：gdal 只开 `gis_ping`、`gis_discover`；工程/地图/图层/数据集/
  显隐/缩放如实 NULL（文件后端无这些产品概念，网关回 NOT_SUPPORTED）。
- 40 动词中落 6 个动词 9 叶：

| 动词 | gdal 叶 | 原生工具 |
|---|---|---|
| V15 gis_reproject | vector、raster | `gdal_reproject`（ogr2ogr -t_srs / gdalwarp -t_srs） |
| V16 gis_convert_format | vector、raster | `gdal_convert_format`（ogr2ogr -f / gdal_translate -of） |
| V19 gis_clip | vector、raster | `gdal_clip`（ogr2ogr -clipsrc / gdalwarp -cutline） |
| V24 gis_slope | 1 | `gdal_slope`（gdaldem slope） |
| V25 gis_aspect | 1 | `gdal_aspect`（gdaldem aspect） |
| V26 gis_hillshade | 1 | `gdal_hillshade`（gdaldem hillshade） |

- V16 的 `table` 变体明确记 **not_supported**（首版未单独验表格式转换，
  不冒充）；V15 的 `table` 变体仍为 not_supported（表无坐标）。
- 未注册的 gdal 动词（buffer/overlay/spatial_join/raster_calc/reclassify/
  zonal_statistics/measure/validate_geometry 等）一律不登记，留批 2。

### 2.3 本地 GDAL 真跑证据

`test_gdal_live.py`：建 20×20 GeoTIFF（EPSG:4326、带 geotransform）与两个
GeoJSON 面夹具，起 `gdal_server.py` 走 stdio MCP，逐工具断言，再起
`gateway.py` 用临时 backends 配置跑端到端。结果：

```
checks: 16, passed: 16, failed: 0
```

覆盖 16 项：ping、discover、矢量/栅格转换、矢量/栅格重投影、矢量/栅格裁剪、
坡度/坡向/山体阴影、TARGET_EXISTS 拒绝覆盖、表重投影 NOT_SUPPORTED，
以及网关 e2e `discover@gdal`、`gis_convert_format@gdal`、`gis_slope@gdal`
（真实产出落盘）。证据：`evidence/phase2/gdal-live-results.json`、
`evidence/phase2/gdal-live.log`。

### 2.4 注册表 / 生成器 / 自检同步

- 在干净副本重跑 `build_mapping.py`，6 个产物**全部字节级一致**
  （mapping／verbs／gp／processing／postgis_templates／mock_tools）。
- 自检 **151/151**：A 9（含 A8 防漂移、A9 V32 三方对账）、B 128、
  C 14（C11 新增 gdal mock discover；原真实目录三项顺延为 C12–C14）。
- 证据：`evidence/phase2/product-compare.txt`、
  `evidence/phase2/selftest-151.log`、`evidence/phase2/selftest-results-151.txt`。

### 2.5 文档同步

- `code/README.md`：总账 195→204、ok 152→161、existing 12→21；新增
  “GDAL 后端首版”范围条目、文件表、验证级别表；自检 151。
- `V03-WORKLIST-V2-...`：终账行与 Phase 2 执行记录。
- `V03-WORKLIST.md`：历史横幅更新到 204。
- `G3-TAGGING-CHANGELOG`：Phase 2 增补注。
- `PHASE1-REPORT.md`：顶部注明其为 Phase 1 快照，当前终账见本报告。

## 3. 账面数字变化对照表

| 项目 | 阶段前 | 阶段后 | 变化与理由 |
|---|---|---|---|
| 后端数 | 8 | **9** | 新增 gdal |
| 叶子总数 | 195 | **204** | +9 条 gdal 叶 |
| ok | 152 | **161** | +9（全部本地 GDAL 实跑） |
| unverified | 21 | **21** | 不变 |
| not_supported | 22 | **22** | 不变 |
| pending / existing | 21 / 12 | **21 / 21** | gdal 9 叶均 existing |
| tier core/extended/exclusive | 163/32/0 | **172/32/0** | gdal 9 叶均 core |
| 每动词至少 1 条 ok | 40/40 | **40/40** | 不变 |
| 自检 | 150/150 | **151/151** | C11 gdal mock discover |
| 生成器产物一致 | 6/6 | **6/6** | 含 gdal 注册表；postgis_templates 仍字节一致 |
| GDAL 工具/动词/叶 | 0/0/0 | **8/6/9** | gdal_server.py + 实跑 |

## 4. `git diff` 逐项解释

| 文件 | 改动 | 原因 |
|---|---|---|
| `code/gdal_server.py` | 新增 8 工具 stdio 服务 | GDAL 适配层本体 |
| `test_gdal_live.py` | 新增真跑验收 16 项 | 每条 ok 叶的实跑证据 |
| `code/backends.json` | +gdal 条目、注释更新 | 第 9 后端注册 |
| `code/build_mapping.py` | +GDAL_TOOLS、BACKENDS/PKG、基础 TABLE、V15/V16/V19/V24–V26、BACKEND_META、native 校验 | 生成器与注册表同账 |
| `code/mapping.json` | +gdal 基础映射 | 生成器产出 |
| `code/verbs.json` | +gdal 40 动词映射 | 生成器产出 |
| `code/mock_tools.json` | +gdal 工具面 | 自检 mock 用 |
| `code/selftest.py` | A7 覆盖 gdal、C11 gdal discover、C 编号顺延、write_cfg 加 gdal | 离线自检覆盖新后端 |
| `code/selftest-results.txt` | 151/151 | 实测输出 |
| `leaves-full.json` | +9 条 gdal 叶（108 行） | 账本 |
| `code/README.md` / 三份 changelog | 204/161/21、gdal 说明 | 文档同步 |
| `evidence/phase2/*` | 真跑结果、日志、6/6 比对 | 证据落盘 |

## 5. 未完成与原因

1. **GDAL 余下动词未注册**：buffer/overlay/spatial_join/raster_calc/reclassify/
   zonal_statistics/measure/validate_geometry 等留批 2；不登记、不冒充。
2. **V16 table 变体未验**：显式 not_supported，等表格式转换单独校准。
3. **原始 manifest 仍未提供**：生成器重跑沿用 Phase 0 的名称补全重建 manifest
   （`scope_note` 与在册 mapping.json 逐字一致，6/6 产物字节一致）；拿到原件
   后应再跑一次复核。
4. **calibration 口径**：gdal 的 `calibrated` 指**桥层 8 工具本地 CLI 实跑**；
   网关 e2e 只过了 discover/convert_format/slope 三条，其余动词的网关 e2e
   未逐条跑；不把桥层证据扩写成整个后端的端到端。
5. **版本号未升 v0.3**：`gateway.py` 仍 0.2.0；版本落码与 tier exclusive 裁决
   留阶段 5。
6. **PostGIS/QGIS/ArcGIS Pro 实机未动**：按计划留阶段 4/后续。

## 6. 下一阶段入口条件

**不满足。** 阶段 3 需要 iServer REST 实例；本机实测：

- `curl localhost:8090/iserver/` → HTTP 000（无服务）
- `curl localhost:8080/iserver/` → HTTP 000
- `C:/Program Files`、`D:/`、`E:/` 未找到 iServer 安装；服务列表无 iServer

因此**阶段 3 未启动**。需要你提供以下之一：

1. 本机可访问的 iServer base URL（含版本、是否需 token/账号）与启动方式；
2. 一台可用的 iServer 测试实例（本地或内网），并确认允许只读探针；
3. 若短期拿不到 iServer，是否批准**改序**：先做阶段 4（QGIS/PostGIS 真后端
   e2e），iServer 评估后置。改序会偏离原定阶段顺序，需你明确批准。

## 7. 证据索引

- `evidence/phase2/gdal-live-results.json`：16 项真跑逐项结果
- `evidence/phase2/gdal-live.log`：真跑完整输出
- `evidence/phase2/product-compare.txt`：干净副本 6/6 产物一致
- `evidence/phase2/selftest-151.log`：151/151 完整输出
- `evidence/phase2/selftest-results-151.txt`：自检结果文件副本
- `evidence/phase2/generator-phase2.log`：生成器重跑 stdout
- `evidence/phase2/accounting.txt`：Phase 2 账面变化（见 §3）

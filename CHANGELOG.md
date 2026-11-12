# CHANGELOG · GIS 统一网关

## v0.3.0 — 2026-11-06

### Added

- **GDAL 后端（第 9 后端）**：`code/gdal_server.py`（纯标准库 stdio MCP，
  调本地 GDAL 3.13.3 CLI）。首版 8 工具、6 动词 9 叶：
  V15 重投影（矢量/栅格）、V16 格式转换（矢量/栅格）、V19 裁剪（矢量/栅格）、
  V24 坡度、V25 坡向、V26 山体阴影。真跑证据 `test_gdal_live.py` 16/16。
- **qgis-cli 后端（第 10 后端）**：`code/qgis_cli_server.py`（stdio MCP，
  调 `qgis_process` 3.44.15）。只开 V02 执行面 + V03/V04 注册表；
  `native:buffer` 真跑；与 in-app qgis 桥分开，不冒充工程/图层视图。
- **真后端 e2e**：`test_real_backends.py` 在同一 `gateway.py` 进程接
  gdal + qgis-cli，9/9 PASS（含真实产出）。
- **iServer 官方演示只读后端（第 11 后端）**：`code/iserver_server.py`
  （GET-only）。登记服务目录 115、map-china 4 地图 / China 13 子层、
  data-china 47 数据集、V35 服务目录；spatialanalyst 根/子资源形状确认，
  执行未尝试。`test_iserver_demo.py` 14/14；证据标注
  `demo-instance-verified`（非本机、版本未确认），**不是 calibrated**。
- **PostGIS 真后端**：`code/postgis_server.py`（psycopg2）接隔离本地
  PostgreSQL 16.15/PostGIS 3.6；模板 **38/38** 真执行 + 网关 **21/21**
  （建表/加字段/字段计算/量测/校验修复/坡度/空间过滤/GeoJSON 导出）。
  `calibrated` 仅限该隔离集群；生产 DSN 未配置。
- **自检防漂移**：A8 生成器模板 36/36 对账；A9 V32 三方对账；
  A10 tier exclusive 裁决断言。
- **总 CHANGELOG**（本文件）与 Phase 0–5 报告。

### Changed

- **总账**：198→195→204→207→**208＝ok 165＋unverified 21＋not_supported 22**；
  pending 21／existing 23；tier **core 174／extended 30／exclusive 4**；
  11 个后端。
- **V32 裁决**：postgis 升 ok（模板实机 38/38）；qgis／arcgis-pro 降
  unverified；supermap 维持 not_supported 并记录 B1/D5 `topology_validate`
  名验通。verbs／leaves／selftest 三处一致。
- **tier exclusive**：V01 arcgis-pro、V01 arcmap、V02 qgis、V02 qgis-cli
  4 叶裁决为 exclusive（厂商算法宇宙通道，无跨平台语义）。
- **版本落码**：`gateway.py` SERVER_VERSION 0.2.0 → **0.3.0**；
  README 标题升 v0.3；生成器 `generated_by` 保留 gateway-v02 来源标识。
- **Processing 通道去特例**：`dispatch_run_processing` 按请求 backend
  取客户端，qgis 与 qgis-cli 共用同一契约。

### Fixed

- **7 条实机校准模板回写生成器**：`clip_raster`、`spatial_join`、
  `mapalgebra`、`hillshade`、`reclass`、`validate_repair`、`mvt_tile`
  以 `CALIBRATED_TEMPLATES` 覆盖层封存；干净副本重跑 6/6 产物字节一致，
  不再回退。
- **B1 覆盖层回灌**：16 条 verdict 写入主账本 `b1_*` 字段；12 条名验通
  未升 ok，1 pending，3 unresolved。
- **生成器可移植性**：`GIS_GATEWAY_MANIFEST` 环境变量；6 产物
  `newline="\n"`；模板 JSON `indent=1`。
- **Windows 测试端编码**：selftest 子进程显式 UTF-8，自检不再依赖
  `PYTHONUTF8=1`。
- **模板测试假通过修正**：`test_templates_live.py` 原把 DSN 放在 `psql`
  选项前，Windows psql 忽略后续 `-c`；改为 `-d DSN` 后 38/38 为真实执行。
- **V06 模板参数适配**：`field={name,type}` 正确映射到模板
  `column/sql_type`（postgis 加字段路径）。
- **新桥 UTF-8 stdio 锁定**：gdal/qgis-cli/iserver/postgis 桥统一锁 UTF-8；
  中文 target 经网关下发不再被 Windows GBK 解码卡住。

### Deferred / Known

- **iServer 本机校准**：官方公开演示实例已完成 GET 只读验收
  （`demo-instance-verified`，非本机、版本未确认）；本机 iServer 校准、
  版本确认、权限模型、空间分析执行仍**未做**。演示实例只读不等于
  calibrated；空间分析的“形状已确认”不等于“可执行已验”。
- **PostGIS 生产实例/DSN**：隔离本地集群已完成 38/38 模板 + 21/21 网关；
  本机 5432 生产实例的密码/DSN 未配置，`calibrated` 不扩写到生产。
- **余下动词**：GDAL 的 buffer/overlay/spatial_join/raster_calc/reclassify/
  zonal_statistics/measure/validate_geometry 等未注册；qgis-cli 只开
  V02/V03/V04；in-app qgis 工程/图层桥仍未实机校准。
- **原始 manifest 未提供**：生成器重跑使用名称补全的重建 manifest
  （scope_note 与在册 mapping.json 逐字一致，6/6 字节一致）。

### Evidence

- `PHASE0-REPORT.md` / `PHASE1-REPORT.md` / `PHASE2-REPORT.md` /
  `PHASE3-REPORT.md` / `PHASE4-REPORT.md` / `PHASE5-REPORT.md`
- `evidence/phase0/` … `evidence/phase5/`
- 关键数字：自检 **154/154**；生成器 **6/6** 字节一致；
  真后端 **9/9**；iServer 演示只读 **14/14**；PostGIS 隔离集群
  **模板 38/38 + 网关 21/21**；GP 1833／Processing 374。

### Commits

- `66ba622` baseline：导入 gateway-v03 原包
- `681e9cc` / `205054e` / `d5ac022`：Phase 0 补发输入、复现与证据
- `5e4e7c5`：Phase 1 销账与防漂移
- `b829322`：Phase 2 GDAL 后端
- `0e3ed5c`：Phase 4 qgis-cli 与两真后端 e2e
- `5d52eb8`：Phase 3 初始阻塞记录
- Phase 3 解封后：iServer 官方演示只读接入（demo-instance-verified）
- Phase 4B：PostGIS 隔离本地集群真后端（calibrated scope）
- 本提交：PostGIS 真后端 + 终对账

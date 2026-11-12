# GIS 综合平台统一网关 v0.3（gateway-v03）

按已批准的设计 `../UPGRADE-DESIGN-V02.md`（鱼鱼 2026-11-02 拍板，7 条
决策全采设计推荐）实现的第一波升级：在 v0.1 骨架（统一 envelope、
calibration 透传、catalog 后端、discover 聚合）上，把后端从 4 个扩到
8 个（v0.3 增至 11 个：+ 本地 GDAL、qgis-cli 无头 Processing、iServer 官方演示只读）、统一动词从 8 个扩到 8＋40 个，
并落地两条总通道、注册表治理、PostGIS 参数化模板面与 R0–R3 确认门。

> **v0.3 增量（2026-11-06）**：第 9 后端 GDAL、第 10 后端 qgis-cli（无头
> Processing）、第 11 后端 iServer（官方公开演示、只读、demo-instance-verified）、
> PostGIS 真后端（隔离本地集群 38/38 + 21/21，calibrated 仅限该集群）、
> V32 裁决、tier exclusive 4 叶裁决；终账
> **208＝ok 165＋unverified 21＋not_supported 22**；tier
> **core 174／extended 30／exclusive 4**；自检 154/154。
> 详见 `../PHASE3-REPORT.md` / `../PHASE5-REPORT.md` 与 `../CHANGELOG.md`。

> **证据等级（先说清）**：本目录全部验收口径只是**离线协议自检**
> （mock 后端＋进程内 stub＋真实 data-catalog 只读对账），**不是实机
> 校准**。后端 calibration 按 backends.json 声明原样透传：
> qgis/geoserver/istsos/arcgis-pro/supermap 为 protocol_selfcheck_only，
> catalog 为登记索引口径 uncalibrated，arcmap 的 calibrated 是 v0.1
> 冻结存量口径；**postgis 为 calibrated，但范围仅限隔离本地
> PostgreSQL 16.15/PostGIS 3.6 集群（38/38 模板 + 网关 21/21），
> 生产 DSN 未配置**。
> **v0.3 Phase 2 的 gdal 是例外**：桥层经本地 GDAL 3.13.3 CLI 实跑
> （calibrated，`test_gdal_live.py` 16/16）；网关 e2e 已过
> discover / convert_format / slope 三条。
> **v0.3 Phase 4 的 qgis-cli 是第二个例外**：qgis_process 3.44.15 无头
> 实跑 `native:buffer`（calibrated）；只开 Processing 通道，不含 in-app
> 工程/图层视图。
> **v0.3 Phase 3 的 iServer 是第三种标注**：官方公开演示实例
> `demo-instance-verified`（非本机、版本未确认、仅 GET）；不是 calibrated，
> 也不是本机校准。

## 范围（设计 §5.1 本波）

1. **40 个第一波动词 V01–V40 全落地**（翻译层）：逐后端映射到设计
   给定的轮子名。叶子映射共 **208** 条：**ok 165**（设计落名；其中桥侧
   工具 existing 23、**pending 21**——工具名已定、桥侧待实现，见下）、
   **unverified 21**（登记但标待验，调用回 `UNVERIFIED_MAPPING` 拒绝
   执行）、**not_supported 22**（回 `NOT_SUPPORTED`，不静默降级）。
   40 个动词每个都至少有一条 ok 映射（V32@postgis 于 2026-11-05 按模板
   实机 38/38 证据升 ok；v0.3 Phase 2 新增 gdal 9 叶；Phase 4 新增
   qgis-cli 3 叶；Phase 3 新增 iServer V35 1 叶）。
2. **ArcGIS GP 直调通道**（V01）：普查 1,833 条全量登记
   （core 803 / extension 878 / defer 152）；白名单第一批＝三箱 core
   243 条（D5），通道实际可调 239 条（扣 4 条破坏类 core）；defer
   152 条回 `DEFER_BLOCKED`、破坏类 28 条回 `DESTRUCTIVE_BLOCKED`、
   其余回 `GP_NOT_WHITELISTED`。通道执行器 `arcgis_run_gp` 是桥侧
   **pending** 工具（无 Pro 环境，GP 校准 pending）。
3. **QGIS Processing 执行面**（V02）＋注册表双动词（V03/V04）：普查
   374 条 ID 只作**种子账**（82/242/50，全标 seed，D6）；defer 50 条
   ＋`qgis:executesql` 共 51 条硬拦截；未建账算法回
   `ALGORITHM_NOT_REGISTERED`。参数模式（params_schema）待桥侧自述
   工具，V04 如实回 null＋说明，不编造。
4. **PostGIS 服务端集**（V30–V33 及各动词的模板映射）：36 个参数化
   模板，**永不接受裸 SQL**——标识符走正则白名单、枚举封闭校验、
   值一律绑定参数、表达式槽有受限片段守卫；`gis_run_sql` 不在工具
   面内（调用回 NOT_SUPPORTED）。**隔离本地 PostgreSQL 16.15/PostGIS
   3.6 实跑：模板 38/38 + 网关 21/21**；生产实例/DSN 未配置
   （`GIS_POSTGIS_DSN` 由用户提供）。
5. **确认门 R0–R3**（设计 §4）：网关只收紧不放宽；动态定级
   （V15 overwrite→R3、V29 output=stored→R1、V32 repair→R2）；
   R3 三件套＝confirm＋目标回显（`target_echo` 逐字比对）＋影响面
   预检回执（`preflight_id` 二次确认，单次有效）＋通道隔离（删除类
   只许具名动词、GP/Processing 通道内硬拦）。许可闸（V34/V39）先于
   confirm：commercial_use=false 回 `LICENSE_BLOCKED`。
6. **discover 治理增补**：gp_governance（计数＋许可/扩展/弃用三字段
   名）、processing_registry 摘要、postgis_templates 摘要、v02_verbs
   支持面；v0.1 的 data_catalog 许可节保留（真实目录对账：9 条、
   commercial_use 全 True）。
7. **GDAL 后端首版（v0.3 Phase 2）**：新增第 9 个后端 `gdal`，纯标准库
   stdio 适配层（`gdal_server.py`）调用本地 GDAL 3.13.3 CLI。首版落 6 个
   动词 9 叶：V15 重投影（矢量/栅格）、V16 格式转换（矢量/栅格）、
   V19 裁剪（矢量/栅格）、V24 坡度、V25 坡向、V26 山体阴影。所有 ok 叶
   由 `test_gdal_live.py` 真实跑过（16/16），并含网关→GDAL 的
   discover / convert_format / slope 端到端；写操作只写新 target，
   target 已存在拒绝覆盖。
8. **QGIS 无头 Processing 后端（v0.3 Phase 4）**：新增第 10 个后端
   `qgis-cli`，纯标准库 stdio 适配层（`qgis_cli_server.py`）调用本地
   `qgis_process` 3.44.15。首版只开 V02 执行面（`native:buffer` 真跑）与
   V03/V04 注册表（网关本地 374 条）；不冒充打开工程/图层视图——那是
   in-app qgis 桥的面，二者分开。
9. **iServer 官方演示只读后端（v0.3 Phase 3）**：新增第 11 个后端
   `iserver`，纯标准库 stdio 适配层（`iserver_server.py`），默认打
   `https://iserver.supermap.io/iserver`。仅 GET；登记服务目录 115、
   map-china 4 地图 / China 1 顶层 13 子层、data-china 47 数据集、
   V35 服务目录；spatialanalyst 根/子资源形状已确认但**执行未尝试**
   （POST 不允许）。证据标注 `demo-instance-verified`，非本机、版本未确认，
   不标 calibrated；本机校准留待后续。

决策落点：D1 SuperMap 只对 iobjectspy 10.1.0 落地、12.x 只登记；
D2 PostGIS 本地实例形态（本波 mock 协议自检）；D3 ArcMap 冻结存量
（v0.2 动词在 arcmap 侧只保留 v0.1 已有面；V40@arcmap 按派单冻结
定义为 NOT_SUPPORTED——桥内虽有 arcmap_export_map_image，不升统一
面，与设计 §2 V40 的 arcmap 映射有此一处执行差异，特此注明）；
D4 官方 MCP 本波只登记不并网；D5 白名单分批；D6 种子账口径；
D7 四级 confirm 制。

## 文件

| 文件 | 内容 |
|---|---|
| `gateway.py` | 网关本体（stdio MCP，纯标准库） |
| `backends.json` | 11 后端生产配置（命令/mode/calibration 声明；v0.3 增 gdal、qgis-cli、iserver） |
| `build_mapping.py` | 注册表生成器：解析 `../help-survey/` 普查 → 下列 JSON |
| `mapping.json` / `verbs.json` | 基础 8 动词映射＋40 动词映射（含 SuperMap 文件登记表 32 条） |
| `gp_registry.json` | GP 1,833 条＋白名单/拦截名单 |
| `processing_registry.json` | Processing 374 条种子账＋51 条硬拦截 |
| `postgis_templates.json` | 36 个参数化模板 |
| `mock_server.py` / `mock_catalog.py` / `mock_tools.json` | 自检替身（工具面由 mock_tools.json 汇出） |
| `gdal_server.py` | 本地 GDAL CLI 后端（stdio MCP，纯标准库） |
| `qgis_cli_server.py` | QGIS 无头 Processing 后端（qgis_process CLI） |
| `iserver_server.py` | iServer 官方演示只读后端（GET-only，demo-instance-verified） |
| `postgis_server.py` | PostGIS 本地实例后端（psycopg2，模板/元数据/GeoJSON） |
| `../probe_iserver_demo.py` / `../test_iserver_demo.py` | iServer 只读探针与 14 项验收 |
| `../test_postgis_live.py` | PostGIS 隔离集群验收（模板 38/38 + 网关 21/21） |
| `../test_gdal_live.py` | GDAL 真跑验收（建夹具→逐工具断言→网关 e2e，16 项） |
| `../test_real_backends.py` | 阶段 4 验收：同一网关接 gdal + qgis-cli，9 项 |
| `selftest.py` / `selftest-results.txt` | 离线协议自检与结果 |
| `OBJECT-MODEL-V02.md` | 对象模型 v0.2 修订说明 |

## 自检

```
python3 build_mapping.py   # 注册表与普查逐数对账（1833/374/243…）
python3 selftest.py        # 154 checks：A 注册表完整性 10（含 A8 防漂移、A9 V32 三方对账、A10 tier exclusive 裁决）、B 进程内分发 128、C 端到端 16（C11 gdal / C12 qgis-cli / C13 iserver mock discover）＋真实目录对账含在 C 段
```

最近一次结果：**checks 154 / passed 154 / failed 0**（见
`selftest-results.txt`）。覆盖：每动词 happy path＋拒绝路径
（NOT_SUPPORTED / UNVERIFIED_MAPPING / DEFER_BLOCKED /
DESTRUCTIVE_BLOCKED / GP_NOT_WHITELISTED / ALGORITHM_NOT_REGISTERED /
CONFIRM_REQUIRED / TARGET_ECHO_MISMATCH / PREFLIGHT_REQUIRED /
PREFLIGHT_MISMATCH / LICENSE_BLOCKED / 模板注入拒绝）。

## 验证级别一览

| 能力面 | 级别 |
|---|---|
| 网关翻译/分发/闸门逻辑 | 离线协议自检（mock＋stub＋真实目录只读） |
| GP 通道、Processing 种子账 | 离线协议自检；执行器/枚举未实机 |
| PostGIS 模板与网关 | 隔离本地 PostgreSQL 16.15/PostGIS 3.6：模板 38/38 + 网关 21/21（`test_postgis_live.py`）；生产 DSN/权限未配置 |
| SuperMap v0.2 新映射 | 登记＋自检；10.1.0 待验 16 条（B1 覆盖层 12 条名验通已回灌 `b1_verdict`，仍未升 ok；V32 维持 not_supported） |
| ArcMap | v0.1 冻结存量（桥 v0.3 已校准口径不变） |
| GDAL 首版（6 动词/9 叶） | 本地 GDAL 3.13.3 CLI 实跑（`test_gdal_live.py` 16/16）；网关 e2e discover/convert_format/slope 已过 |
| qgis-cli 首版（V02/V03/V04） | qgis_process 3.44.15 无头实跑 `native:buffer`；同一网关接 gdal+qgis-cli 9/9（`test_real_backends.py`）；不含 in-app 工程/图层视图 |
| iServer 演示只读（V35 + 基础面） | 官方公开演示 `demo-instance-verified`（非本机、版本未确认、仅 GET）；服务目录/map-china/data-china 14/14；spatial 仅确认根/子资源形状，执行未尝试；不标 calibrated |

## 未做清单（v0.3 承接，设计 §5.2）

- GP 白名单扩批（栅格四箱 core 子集＋Spatial Statistics core）；
  GP 条目许可三字段的逐条数据补齐（本波只有字段位与计数）。
- QGIS 实机枚举建账（桥侧枚举/自述两只读工具）、种子账转 verified、
  GRASS/SAGA 建账——与 12 月 QGIS 校准排期合并。
- 生产 PostGIS 实例/DSN 与权限未配置（隔离本地集群已 38/38 模板 +
  21/21 网关）；GeoServer 发布回写 catalog 的工具（现 writeback 恒 pending）。
- 桥侧 pending 工具实现：arcgis_run_gp、supermap 文件面新工具 11 个、
  geoserver_publish_layer、istsos 通用实体查询与服务根（共 21 条
  pending 映射）。
- SuperMap 待验 16 条映射的 10.1.0 逐项验存（B1 12 条已名验通，待二轮
  类方法下钻清 V06/V07/V12 与 V20/difference）；网络分析 ext 试点；
  ENVI 具名动词；iServer/Esri 官方 MCP 并网评估（D4）。
- V33 瓦片的真实字节流出口（HTTP 面）；istSOS 写面。
- GDAL 余下动词（buffer/overlay/spatial_join/raster_calc/reclassify/
  zonal_statistics/measure/validate_geometry 等）未注册，留批 2；首版只落
  6 个动词 9 叶，不登记不冒充。
- qgis-cli 首版只开 V02/V03/V04；in-app qgis 桥的工程/图层工具不在 CLI
  模式提供。PostGIS 真后端因本机数据库密码未提供，阶段 4 未使用；
  GDAL + qgis-cli 已满足“两个真实后端”验收。
- iServer 只完成官方演示实例的 GET 只读面；**本机校准、版本确认、权限模型、
  空间分析执行**均未做。演示实例的 `demo-instance-verified` 不等于
  calibrated；不得把空间分析的“形状已确认”写成“可执行已验”。

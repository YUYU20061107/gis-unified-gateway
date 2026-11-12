# 统一入口对象模型 v0.2 修订说明

v0.2 在 v0.1 对象模型（project / map / layer / dataset 四核心对象、
dataset 双来源、project kind=catalog、discover 的 data_catalog 许可节）
之上做四处扩展，对应设计 `../UPGRADE-DESIGN-V02.md` §2/§3/§4。机器可读
版在 `mapping.json` 与各注册表文件里；本文件只记模型层面的增量与口径。

## 1. 后端面：4 → 8

后端集合扩为 supermap / arcgis-pro / arcmap / qgis / catalog /
**postgis / geoserver / istsos**。新后端的对象语义：

| 后端 | 核心对象 | 说明 |
|---|---|---|
| postgis | table（=dataset 的服务端形态） | 空间表即 dataset；`gis_list_datasets` 回 `source_kind=server_database`，与厂商工作空间、平台目录两个来源并列为第三种来源 |
| geoserver | service / published layer | 发布产物是 service 对象（见 §3）；工作空间内图层走 `gis_list_layers` |
| istsos | observation stream（Datastream）与实体集 | 观测查询以 Datastream 为锚（见 §4） |

arcmap 自 v0.2 起**冻结存量**（决策 D3）：只保留 v0.1 已有动词映射，
不新增任何 v0.2 动词（V40 出图亦不升统一面）。

## 2. 注册表对象（本波新增三类）

- **GP 工具条目**（`gp_registry.json`，1,833 条）：字段＝全名、工具箱、
  判断（core/extension/defer）、许可三字段位（license_level /
  requires_extension / deprecated，数据随治理透传补齐）、白名单批次。
  通道可调集＝白名单第一批 243 扣破坏类 4 条＝239 条。
- **Processing 算法条目**（`processing_registry.json`，374 条种子）：
  字段＝algorithm_id、判断、status。status 只有 `seed`——普查清单只是
  种子账，实机枚举（D6）才是真源；条目另带硬拦截名单 51 条
  （50 defer＋`qgis:executesql`）。
- **PostGIS 模板条目**（`postgis_templates.json`，36 个）：字段＝
  template_id、sql（槽位标记 `{ident:}/{idents:}/{enum:}/{expr:}/
  {fragment:}` 与绑定占位 `%(name)s`）、params（类型/枚举/范围）。
  模板是服务端能力的唯一入口对象：平台不开裸 SQL 面。

SuperMap 侧另有**文件登记表**（verbs.json 的 supermap_registry，32 条）：
设计 §1 矩阵落名的轮子清单，非运行时枚举，V03 对 supermap 返回它并
如实标 `registry=supermap_file_registry`。

## 3. service 对象与发布回写

- `gis_list_services`（V35）回服务面摘要（GeoServer capabilities 口径）；
  istsos 的服务根登记为 NOT_SUPPORTED（桥侧 service root 工具 pending，
  不冒充）。
- `gis_publish_layer`（V34）的产物带 `publication.writeback`：目录回写
  依赖 catalog 侧尚不存在的回写工具，现值恒为
  `status=pending_catalog_support`——发布成功 ≠ 目录已同步，不许写成
  已回写。

## 4. 观测对象

`gis_query_observations`（V36）以 SensorThings 实体为对象词表：
Things / Locations / Sensors / ObservedProperties / Datastreams /
Observations / FeaturesOfInterest。Observations 必须以 datastream_id
为锚（无锚回 INVALID_ARGUMENT）；桥侧只有 Things/Locations/
Observations 三个既有读工具，其余实体经待实现的通用实体查询，
回包带 `bridge_tool_status=pending`。

## 5. 瓦片句柄对象

`gis_serve_vector_tile`（V33）不把二进制塞进 JSON 文本面：回包是
句柄形态 `{content_type: application/vnd.mapbox-vector-tile, tile:
{z,x,y}, encoding: binary-handle, backend_result}`。真实字节流出口
（HTTP 面）不在本波。

## 6. 治理元数据（随每个回包透传，不升格）

- envelope 沿用 v0.1：`{backend, mode, calibration{level,
  evidence_ref}, gateway}`；calibration 只按 backends.json 声明透传。
- 动词回包带 `verb / vid / level（R0–R3 实际定级）/ wheel（落到的
  轮子名）`；映射状态三值：`ok`（设计落名；其中桥侧工具可能仍是
  pending，回包另带 bridge_tool_status）、`unverified`（登记但待验，
  调用回 UNVERIFIED_MAPPING）、`not_supported`（回 NOT_SUPPORTED，
  不静默降级）。
- discover 增补：arcgis-pro 带 `gp_governance`（白名单/拦截计数＋
  三字段名）、qgis 带 `processing_registry` 摘要、postgis 带
  `postgis_templates` 摘要、全后端带 `v02_verbs` 支持面与既有的
  `data_catalog` 许可节。
- 许可闸是对象级前置：V34/V39 在 confirm 之前先查 dataset 的
  license（commercial_use=false 必拦；unknown 仅研究用途放行）。

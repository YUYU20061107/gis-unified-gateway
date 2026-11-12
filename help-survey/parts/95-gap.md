## 4. 差距：现有两桥覆盖 vs 官方全集

现有两桥的工具面（据合集 manifest 实测）：arcgis-pro 桥 13 个工具、arcmap 桥 10 个工具，全部属于**应用操作面**（arcpy.mp / arcpy.mapping：工程信息、列地图/数据框、列图层/表/布局、显隐、缩放、加图层、出图、保存）。统一入口 v0 从中收了 8 个只读/视图动词。

| 覆盖面 | 官方全集 | 两桥已覆盖 | 缺口 |
| --- | ---: | ---: | ---: |
| 应用操作面（工程/地图/图层/视图） | 非工具箱口径（arcpy.mp/mapping 模块） | Pro 13＋ArcMap 10＝23 个工具，v0 已收 8 个统一动词 | 桥外尚有：Pro 桥的 list_tables/list_layouts/set_labels_visible 未进 v0；arcpy.mp 的布局导出、地图系列、图层文件管理等未桥接（属存量增补，非主缺口） |
| **地理处理面（44 箱工具）** | **1,833 个工具** | **0** | **1,833（100%）**——两桥目前调不动任何一个 GP 工具，Agent 无法真正"做分析"，只能"看工程" |
| 其中 core（可升统一动词池） | 803 | 0 | 803 |
| 其中 extension（留 `gis.arcgis.*`） | 878 | 0 | 878 |
| 其中 defer（暂不适合） | 152 | — | 多为门户/在线额度依赖与已弃用线，不计入近期缺口 |

按功能域看 GP 缺口（工具数 / 其中 core）：

| 功能域 | 官方工具 | core | 两桥 GP 覆盖 |
| --- | ---: | ---: | ---: |
| 核心通用（Analysis、Data Management、Conversion、Cartography、Editing） | 535 | 278 | 0 |
| 栅格与表面（Spatial Analyst、3D、Geostatistical、Image Analyst） | 513 | 330 | 0 |
| 网络与统计（Network Analyst、Spatial Statistics、Space Time Pattern Mining） | 98 | 60 | 0 |
| 服务与大数据（GeoAnalytics 桌面/服务器、Raster Analysis、Standard Feature Analysis、Ready To Use） | 110 | 57 | 0 |
| 数据生产与质量（Geocoding、Linear/Location Referencing、Data Interoperability、Data Reviewer、Multidimension，不含 Editing） | 93 | 28 | 0 |
| 行业与平台（GeoAI、BA、国防/情报/航空/海事、室内、宗地、网络族等 21 箱） | 484 | 50 | 0 |

另两条质性差距：
- **校准差**：arcmap 无头桥已实机校准，arcgis-pro 桥未校准；GP 通道若新建，属未验证新表面，须按既有校准纪律单独过一轮（先 Pro 后 ArcMap，且 ArcMap 侧见第 5 节第 8 条的冻结建议）。
- **治理差**：现有 discover 不透传"许可/扩展可用性"（哪些工具要 Spatial Analyst/3D/Network 扩展、哪些要 Advanced 级别、哪些已弃用），GP 通道上线前必须先补，否则 Agent 会频繁调用必失败的工具。已弃用/退役的官方线已在清单中可辨：GeoAnalytics Server（官方已弃用，最终版 Enterprise 11.3）、Workflow Manager (Classic)（Pro 3.4 已退役）、ArcMap 独有遗留（Coverage/Schematics/几何网络）。

---

## 5. 升级建议（按收益排序，共 8 条）

1. **先开 GP 直调总通道（总开关）**：给 arcgis-pro 桥加一个按官方命名空间直调 ArcPy GP 的通道（如 `gis.arcgis.run_gp`＋按箱的扩展命名空间），平台只做动词翻译、参数校验、confirm 确认门与结果回读，不自研任何算法。理由：1,833 条工具中绝大多数的轮子来源都是同一个——ArcPy GP 官方实现；一个通道即可把"全部升级"从口号变成可达，成本远低于逐个工具写桥。写/破坏类工具（删除、覆盖、批量编辑）默认走 confirm 门，defer 类（152 条）不进通道白名单。
2. **Analysis core 升为跨软件统一动词（第一批具名动词）**：Buffer、Clip、Intersect、Union、Erase、Select、Spatial Join、Dissolve、Summary Statistics、Summarize Within、Near/Generate Near Table 等约 30 条，是 QGIS/SuperMap/PostGIS/GRASS 各家都有的共同语义，最适合做 `gis_buffer`、`gis_clip` 这类统一动词并做跨桥对齐校准。理由：使用频率最高、多家可互验、是 Agent 真正开始"做 GIS"的第一步。
3. **Data Management 的"造数据"子集升 core 动词组**：创建要素类/表、加/删/改字段、定义投影与重投影、Merge/Append、Copy/Rename/Delete 数据集、加索引。理由：现在两桥只能看不能造，Agent 连分析的输入输出都管理不了；这批工具许可门槛低（多为 Basic）、语义跨家通用，是 GP 通道之后最先被用到的能力层。企业级版本/复制/归档类（extension）留扩展命名空间，不进 core。
4. **Conversion core 做成 `gis_convert_*` 格式互转动词**：Shapefile/GeoJSON/KML/GeoPackage/Excel/CSV 与要素类互转、栅格格式转换等 27 条。理由：与平台数据层（目录＋STAC）和 GDAL 桥天然衔接——同一转换在 ArcGIS 环境走 ArcPy GP、在开源环境走 GDAL，双轮子按环境择一，平台只维护语义映射。
5. **位置服务直接接 Esri 官方 MCP（零自建）**：地理编码、反地理编码、路径、高程、静态图等动词优先映射 **MCP for ArcGIS Location Services (beta)**（官方托管，入口见 2.8）；本地定位器场景再用 Geocoding 工具箱 ArcPy（15 条）补位。理由：官方已经给了智能体通道，自建即重复造轮子；且这批能力原本就不是桌面 GP 的强项。
6. **栅格分析与遥感主线对齐（鱼鱼主场）**：Spatial Analyst core 子集（坡度/坡向/山影、重分类、栅格计算、分区统计、水文基础）与 3D Analyst 的 LAS 基础处理升为统一栅格动词，与 GDAL/GRASS 桥的同名能力对齐互验；无桌面环境时可用 Esri 托管高程分析 REST（坡度/坡向/山影/可视域已有官方服务）作第二轮子。理由：遥感是鱼鱼的专业与数据层 B 的主战场，这批 core（四箱合计 330 条为全集最大）决定平台的分析成色。
7. **治理先行：discover 增补许可与弃用透传**：在统一入口的 discover/能力协商里增加每工具的许可级别、所需扩展、是否弃用三字段（数据源头就是官方各箱 licensing 页与工具页，本普查已摸清分布）。理由：成本最低、防错收益最高——避免 Agent 调用必然失败的工具（如无 SA 扩展调 Spatial Analyst），也让"校准三级口径"从桥级细化到工具级。
8. **ArcMap 线冻结存量**：arcmap 桥保留现有 10 个工具的兼容与已校准状态，不再为它新建 GP 通道；新能力一律 Pro 口径，统一动词在 ArcMap 侧只做"两边都有"的映射。理由：ArcMap 已于 2026-03-01 退役（Esri Support 官方口径）、其 ArcPy 为 Python 2.7，在退役运行时上投入新通道的产出比最低；鱼鱼本机只有 ArcMap 的现实由"存量兼容＋Pro 为纲"化解，而不是把平台绑在退役线上。

---

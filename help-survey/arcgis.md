
- 普查日期：2026-11-02
- 证据口径：一级证据＝Esri 官方文档（pro.arcgis.com / desktop.arcgis.com / support.esri.com）。本文件未使用论坛/博客内容下任何结论；个别生命周期信息引自 Esri Support 官方页（已在文中标注）。
- 版本口径：ArcGIS Pro 以 **3.4 工具参考**为准（ArcPy 模块总览页与各工具箱/工具集总览页均为 3.4 版页面，2026-11-02 实际打开核对）；ArcMap 以 **10.8**（Desktop 文档 "latest" 即 10.8.x；鱼鱼本机装的是 ArcMap 10.8）为准。
- 普查对象：ArcGIS Pro 地理处理工具全集（以官方工具参考目录为纲）＋ ArcPy 非工具模块 ＋ ArcMap 10.8 工具箱体系与差异。
- 平台判断标记：**core**＝多家 GIS 共有、可升为平台统一动词的候选；**extension**＝ArcGIS 专属或绑定其扩展/数据模型，留扩展命名空间（如 `gis.arcgis.*`）；**defer**＝依赖交互桌面、向导、门户/在线账号额度或对 Agent 不安全的破坏性操作，暂不适合。
- **升级原则（鱼鱼 2026-11-02 定）：全部升级＋不重复造轮子。** 平台层只做协议翻译与治理（发现、校准透传、确认门、许可标注），不自研算法。每条功能另标「轮子来源」＝官方现成可复用实现：ArcPy 地理处理（官方实现，桥直调）／ArcGIS REST 服务等价接口／ArcGIS Online 托管工具／arcgis Python API／Esri 官方 MCP（见 2.8）／仅桌面交互无脚本入口。桥接优先级：已有官方通道的，平台只做映射与治理，不另写实现。
- ArcPy 入口命名规则：工具在 ArcPy 中即 `arcpy.<模块>.<工具名去空格>`（如 `arcpy.analysis.Buffer`），下表按此规则书写；个别工具另有专用模块类 API（如 Network Analyst 的 arcpy.nax solver 对象），在对应节注记。

---

## 1. 文档入口与版本口径（实际查阅的官方页面）

### 1.1 ArcGIS Pro（全集纲）

| 入口 | URL | 用途 |
| --- | --- | --- |
| ArcPy modules—ArcGIS Pro（3.4） | http://pro.arcgis.com/en/pro-app/3.4/arcpy/get-started/arcpy-modules.htm | 工具箱全集的权威枚举：44 个工具箱模块＋11 个非工具模块 |
| ArcGIS Pro 工具参考（3.4）各工具箱总览页 | https://pro.arcgis.com/en/pro-app/3.4/tool-reference/<toolbox>/an-overview-of-the-<toolbox>-toolbox.htm | 每箱的工具集清单与官方定位 |
| 各工具集总览页 | 同域 tool-reference 下 "an-overview-of-the-<toolset>-toolset.htm" | 工具级全表（Tool｜Description），本普查工具清单的直接来源 |
| Analysis 工具箱许可页（示例） | https://pro.arcgis.com/en/pro-app/2.6/tool-reference/analysis/analysis-toolbox-license.htm | 每箱另有 "<toolbox> toolbox licensing" 页，给出工具×许可级别矩阵 |
| ListToolboxes / ListTools（ArcPy 函数参考） | https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/listtoolboxes.htm | 程序化枚举工具箱/工具的官方函数，桥侧可复用同一思路做 discover |

### 1.2 ArcMap 10.8（存量线）

| 入口 | URL | 用途 |
| --- | --- | --- |
| ArcMap Analysis 工具箱总览 | http://desktop.arcgis.com/en/arcmap/latest/tools/analysis-toolbox/an-overview-of-the-analysis-toolbox.htm | 证实 ArcMap 版 Analysis 只有 4 个工具集（无 Pairwise Overlay） |
| ArcMap Data Management 工具箱总览 | https://desktop.arcgis.com/en/desktop/latest/tools/data-management-toolbox/an-overview-of-the-data-management-toolbox.htm | 31 个工具集，含 Pro 已移除的 Distributed Geodatabase / Geometric Network / Graph / File Geodatabase 等 |
| ArcMap Coverage 工具箱总览 | https://desktop.arcgis.com/en/arcmap/10.5/tools/coverage-toolbox/an-overview-of-the-coverage-toolbox.htm | ArcMap（且需 ArcInfo Workstation）独有的 coverage 工具箱 |
| ArcMap Schematics 工具箱总览 | https://desktop.arcgis.com/de/arcmap/latest/tools/schematics-toolbox/an-overview-of-the-schematics-toolbox.htm | ArcMap 独有，5 个工具（Pro 由 Network Diagram 取代） |
| ArcMap Tracking Analyst 工具箱总览 | https://help.arcgis.com/en/arcgisdesktop/10.0/help/0064/006400000002000000.htm | ArcMap 独有的时态数据工具（10.0 帮助存档页，工具在 10.8 仍在） |
| Licensing for geoprocessing tools（Desktop） | https://desktop.arcgis.com/en/arcobjects/latest/java/dafdda57-4cb1-4d92-86fc-fed2ce0aac91.htm | Desktop 侧核心工具箱许可矩阵，列出核心箱名单 |
| ArcMap Life Cycle（Esri Support） | https://support.esri.com/en-us/products/arcmap/life-cycle | 官方口径：10.8.x 为 ArcMap 最终系列，2024-03-01 进入成熟支持，**2026-03-01 已退役**，无后续版本 |

> 版本与生命周期结论（平台决策相关）：Pro 是唯一仍在演进的线（工具参考已到 3.4+）；ArcMap 10.8 已于 2026-03-01 退役。因此本普查以 Pro 工具参考为全集纲，ArcMap 只标差异；平台新能力一律按 Pro 口径设计，ArcMap 桥维持存量兼容即可。

---

## 2. 功能域总览（按官方工具箱体系）

ArcGIS Pro 3.4 的 ArcPy 模块总览页共列 **44 个工具箱模块**。按平台视角归为六个域（归类为本普查所加，工具箱名与模块名为官方原名）：

### 2.1 核心通用域（平台 core 的主要来源）
- **Analysis（arcpy.analysis）**：叠加、缓冲、邻近、统计——最基础的 GIS 运算。
- **Data Management（arcpy.management）**：要素类/数据集/字段/栅格等数据结构的全生命周期管理，全集最大的箱。
- **Conversion（arcpy.conversion）**：格式互转（矢量/栅格/表/CAD/KML/JSON/GeoPackage 等）。
- **Cartography（arcpy.cartography）**：制图综合、掩膜、注记、地图系列。
- **Editing（arcpy.edit）**：批量编辑类工具。

### 2.2 栅格与表面分析域（遥感/GIS 分析主力）
- **Spatial Analyst（arcpy.sa）**：栅格代数、水文、表面、插值、密度、分区等。
- **3D Analyst（arcpy.ddd）**：TIN、terrain、LAS 点云、三维矢量分析与转换。
- **Geostatistical Analyst（arcpy.ga）**：克里金等空间插值与地统计图层。
- **Image Analyst（arcpy.ia）**：影像分析、栅格函数、变化检测、深度学习推理配套等。

### 2.3 网络与统计分析域
- **Network Analyst（arcpy.na / arcpy.nax）**：路径、最近设施、服务区、OD 成本矩阵、VRP、位置分配＋网络数据集维护。
- **Spatial Statistics（arcpy.stats）**：空间模式/聚类/回归（Moran's I、热点、GWR 等）。
- **Space Time Pattern Mining（arcpy.stpm）**：时空立方体与时空模式挖掘。

### 2.4 服务与大数据域（依赖门户/服务器/在线）
- **GeoAnalytics Desktop（arcpy.geoanalytics）**：本机 Spark 大数据分析。
- **GeoAnalytics Server（arcpy.gapro）**：服务器分布式大数据分析。
- **Raster Analysis（arcpy.ra）**：门户影像服务器栅格分析。
- **Standard Feature Analysis（arcpy.sfa）**：门户要素分析。
- **Ready To Use（arcpy.agolservices）**：ArcGIS Online 托管分析服务（耗额度）。

### 2.5 数据生产与质量域
- **Geocoding（arcpy.geocoding）**：地址定位器与地理编码。
- **Linear Referencing（arcpy.lr）**：路线与量测（LRS 基础）。
- **Location Referencing（arcpy.locref）**：LRS 网络配置与管理（Pro 新线，ArcMap 时代为 Pipeline/Roads and Highways 方案）。
- **Data Interoperability（arcpy.di）**：基于 FME 引擎的格式转换（Quick Import/Export、空间 ETL）。
- **Data Reviewer（arcpy.reviewer）**：数据质检检查框架。
- **Multidimension（arcpy.md）**：netCDF/GRIB/HDF/CRF 多维数据管理。

### 2.6 行业与平台域（多为专属扩展）
- **GeoAI（arcpy.geoai）**：深度学习/机器学习训练与推理。
- **Business Analyst（arcpy.ba）**、**Crime Analysis and Safety（arcpy.ca）**、**Defense（arcpy.defense）**、**AllSource（arcpy.intelligence）**：商业、治安、国防、情报。
- **Aviation（arcpy.aviation）**、**Bathymetry（arcpy.bathymetry）**、**Maritime（arcpy.maritime）**：航空、水深、海事制图。
- **Indoors（arcpy.indoors）**、**Indoor Positioning（arcpy.indoorpositioning）**：室内数据与室内定位。
- **Oriented Imagery（arcpy.oi）**：定向影像数据集。
- **Parcels（arcpy.parcels）**：宗地结构（parcel fabric）。
- **Public Transit（arcpy.transit）**：GTFS 公共交通数据。
- **Reality Mapping（arcpy.rm）**：无人机/航空影像生成正射、DSM、网格、点云产品。
- **Territory Design（arcpy.td）**、**Topographic Production（arcpy.topographic）**：区域划分、地形图生产。
- **Server（arcpy.server）**：Web 图层/地图管理与数据抽取。
- **Workflow Manager（arcpy.wmx）**：工作流作业信息。
- **Network Diagram（arcpy.nd）**、**Trace Network（arcpy.tn）**、**Utility Network（arcpy.un）**：网络图、追踪网络、公共设施网络。

### 2.7 ArcPy 非工具模块（不是工具箱，但对桥/平台极重要）
据 ArcPy 模块总览页 "Additional modules"：**arcpy.da**（游标/编辑会话/NumPy 互转——Agent 读写数据的最短路径）、**arcpy.mp**（工程/地图/图层/布局操作，Pro 版；ArcMap 对应为 arcpy.mapping）、**arcpy.charts**（图表）、**arcpy.metadata**（元数据）、**arcpy.sharing**（发布共享草稿）、**arcpy.geocoding / arcpy.ia / arcpy.nax / arcpy.sa / arcpy.un / arcpy.wmx** 的类 API 部分。现有两座 ArcGIS 桥的工具面本质上是 arcpy.mp/mapping 的一小片（工程、地图、图层、布局的查看与视图操作），**尚未触及任何地理处理工具**——这是第 4 节差距量化的基点。

### 2.8 Esri 官方智能体 / MCP 通道（单独标出）

| 通道 | 性质 | 入口 | 覆盖与口径 |
| --- | --- | --- | --- |
| **MCP for ArcGIS Location Services (beta)** | **Esri 官方托管**（developers.arcgis.com，页面标题即标 beta） | https://developers.arcgis.com/ai/mcp-arcgis-location-services/ | Esri 托管的 MCP 服务器，把 Location Services 以标准 MCP 工具暴露给 AI 应用/智能体：地理编码、反地理编码、高程、路线与导航、静态地图图片；其服务族另含 Basemap Styles/Tiles、Places、GeoEnrichment、Elevation。需 ArcGIS Location Platform 或 ArcGIS Online 账号。**范围仅限位置服务，不覆盖桌面地理处理工具与门户管理**——平台的地理编码/路径/高程类统一动词应优先映射到它，而不是自建 |
| ArcGIS 智能助手（AI Assistants） | Esri 产品内建（ArcGIS Pro / Enterprise 等产品内的 AI 助手功能） | 见各产品官方文档（本轮未逐页展开） | 产品内助手，非对外 MCP 通道；平台不依赖，仅记录生态位 |

> 非官方生态（二级证据，仅作参考，不计入官方口径）：社区已有 arcgis-portal-mcp（个人开源，面向 Portal/Online 管理与要素 CRUD）、CLI-Anything-Arcgis-Pro（社区，ArcPy CLI＋在 Pro 会话内的 MCP 桥，形态与本平台的桥相近）等项目。它们证明需求存在，但**不是 Esri 官方实现**，平台若参考须按社区项目对待，不得标为官方轮子。

---

## 3. 工具级清单（按工具箱，含轮子来源与平台判断）

全集口径：44 个工具箱、**1,833 个地理处理工具**逐条列名（下表为各箱计数，与正文逐条清单一致）。平台判断合计：**core 803 条 / extension 878 条 / defer 152 条**。

| 工具箱 | ArcPy 模块 | 工具数 | 其中 core |
| --- | --- | ---: | ---: |
| Analysis | arcpy.analysis | 35 | 30 |
| Data Management | arcpy.management | 387 | 186 |
| Conversion | arcpy.conversion | 47 | 27 |
| Cartography | arcpy.cartography | 48 | 19 |
| Spatial Analyst | arcpy.sa | 221 | （四箱合计 330） |
| 3D Analyst | arcpy.ddd | 138 |  |
| Geostatistical Analyst | arcpy.ga | 35 |  |
| Image Analyst | arcpy.ia | 119 |  |
| Network Analyst | arcpy.na / arcpy.nax | 32 | 9 |
| Spatial Statistics | arcpy.stats | 48 | 41 |
| Space Time Pattern Mining | arcpy.stpm | 18 | 10 |
| GeoAnalytics Desktop | arcpy.geoanalytics | 31 | 24 |
| GeoAnalytics Server | arcpy.gapro | 29 | 0 |
| Raster Analysis | arcpy.ra | 29 | 23 |
| Standard Feature Analysis | arcpy.sfa | 10 | 10 |
| Ready To Use | arcpy.agolservices | 11 | 0 |
| Editing | arcpy.edit | 18 | 16 |
| Geocoding | arcpy.geocoding | 15 | 4 |
| Linear Referencing | arcpy.lr | 7 | 7 |
| Location Referencing | arcpy.locref | 44 | 0 |
| Data Interoperability | arcpy.di | 2 | 0 |
| Data Reviewer | arcpy.reviewer | 5 | 0 |
| Multidimension | arcpy.md | 20 | 17 |
| GeoAI | arcpy.geoai | 18 | 17 |
| Business Analyst | arcpy.ba | 47 | 1 |
| Crime Analysis and Safety | arcpy.ca | 13 | 3 |
| Defense | arcpy.defense | 23 | 13 |
| AllSource | arcpy.intelligence | 18 | 4 |
| Aviation | arcpy.aviation | 40 | 0 |
| Bathymetry | arcpy.bathymetry | 10 | 0 |
| Maritime | arcpy.maritime | 14 | 0 |
| Indoors | arcpy.indoors | 16 | 0 |
| Indoor Positioning | arcpy.indoorpositioning | 8 | 0 |
| Oriented Imagery | arcpy.oi | 4 | 2 |
| Parcels | arcpy.parcel | 24 | 0 |
| Public Transit | arcpy.transit | 8 | 8 |
| Reality Mapping | arcpy.rm | 14 | 1 |
| Territory Design | arcpy.td | 19 | 0 |
| Topographic Production | arcpy.topographic | 55 | 1 |
| Server | arcpy.server | 19 | 0 |
| Workflow Manager | arcpy.wmx | 14 | 0 |
| Network Diagram | arcpy.nd | 74 | 0 |
| Trace Network | arcpy.tn | 9 | 0 |
| Utility Network | arcpy.un | 37 | 0 |
| **合计** |  | **1,833** | **803** |

口径与已知偏差（如实记录）：
- 各箱锚定版本不完全一致：ArcPy 模块总览、Analysis、Conversion、Cartography、栅格四箱、数据生产七箱锚定 **3.4**；Data Management 分册因搜索索引只返回 3.1 文档站，锚定 **3.1**（3.2–3.4 若有个别新增工具/工具集，可能有个位数遗漏，宣称"3.4 全量"前需对该箱做一次增量核对）；行业分册各箱总览页版本在 3.1–3.7/latest 间混合，已在该分册文件头逐项说明。
- Image Analyst 按 3.4 口径计 119 条；官方更高版本（3.5+）新增的 Spectral Analysis 工具集与扩展 SAR/深度学习工具未计入。
- Ready To Use 计 11 条：其中 Network Analysis 工具集 6 条未出现在 3.4/3.2 工具箱总览表中，但其 toolset 总览页仍在现行官方文档，故计入并在该节注明；若按总览表严格口径，全集为 1,827 条。
- 个别工具的 ArcPy 函数名以官方工具页 Syntax 为准的已逐个核对（Conversion/Cartography 分册）；其余分册按"去空格"规则生成，极少数带连字符/缩写的工具函数名可能与官方签名略有出入，桥接实现时须以 `arcpy` 实际导入为准。
- 工具计数为工具箱内条目数；个别工具跨工具集重复列名（如 3D Analyst 的 LAS Building Multipatch）已去重计一次。

---

## Analysis toolbox（arcpy.analysis）

工具集 5 个，工具 **35** 个。官方定位：执行最基础的 GIS 运算——叠加、缓冲、统计、邻近分析。这是全平台 core 密度最高的箱：35 个里 30 个判 core。许可：核心箱，多数工具 Basic 即可用，个别工具有许可级别限制（见官方 Analysis toolbox licensing 页）。

### Extract toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
| --- | --- | --- | --- | --- |
| Clip | 用裁剪要素的范围提取输入要素 | arcpy.analysis.Clip | core：裁剪是多家共有基础运算，可升统一动词 gis_clip | ArcPy GP（官方实现） |
| Select | 按 SQL/选择表达式抽取要素到新要素类 | arcpy.analysis.Select | core：属性筛选导出，统一动词候选 | ArcPy GP（官方实现） |
| Split | 用叠加要素把输入拆成多个输出要素类 | arcpy.analysis.Split | core：按区拆分，通用 | ArcPy GP（官方实现） |
| Split By Attributes | 按唯一属性值拆分数据集 | arcpy.analysis.SplitByAttributes | core：分组拆分导出，通用 | ArcPy GP（官方实现） |
| Table Select | 按 SQL 表达式选表记录写出新表 | arcpy.analysis.TableSelect | core：表级筛选，通用 | ArcPy GP（官方实现） |

### Overlay toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
| --- | --- | --- | --- | --- |
| Apportion Polygon | 按叠加面积比例把输入多边形属性分摊到目标多边形 | arcpy.analysis.ApportionPolygon | extension：面积分摊属较专的统计口径，先留扩展 | ArcPy GP（官方实现） |
| Count Overlapping Features | 生成平面化重叠要素并写入重叠计数 | arcpy.analysis.CountOverlappingFeatures | core：重叠计数，通用叠加分析 | ArcPy GP（官方实现） |
| Erase | 擦除与擦除要素重叠的部分 | arcpy.analysis.Erase | core：经典叠加，统一动词候选 gis_erase | ArcPy GP（官方实现）；REST Geometry Service 有 difference 等价 |
| Identity | 与标识要素做几何相交并带入其属性 | arcpy.analysis.Identity | core：经典叠加 | ArcPy GP（官方实现） |
| Intersect | 计算多图层共同重叠部分 | arcpy.analysis.Intersect | core：经典叠加，统一动词候选 gis_intersect | ArcPy GP（官方实现）；REST Geometry Service 有 intersect 等价 |
| Remove Overlap (multiple) | 移除多个输入图层多边形之间的重叠 | arcpy.analysis.RemoveOverlapMultiple | core：多图层去重叠，Pro 新增的通用整理运算 | ArcPy GP（官方实现） |
| Spatial Join | 按空间关系把一要素的属性连接到另一要素 | arcpy.analysis.SpatialJoin | core：空间连接，统一动词候选 gis_spatial_join | ArcPy GP（官方实现） |
| Symmetrical Difference | 输出两图层互不重叠的部分 | arcpy.analysis.SymmetricalDifference | core：经典叠加 | ArcPy GP（官方实现）；REST Geometry Service 有 difference 等价 |
| Union | 计算几何并集并保留全部要素与属性 | arcpy.analysis.Union | core：经典叠加，统一动词候选 gis_union | ArcPy GP（官方实现）；REST Geometry Service 有 union 等价 |
| Update | 用更新要素的几何与属性更新输入要素 | arcpy.analysis.Update | core：经典叠加更新 | ArcPy GP（官方实现） |

### Pairwise Overlay toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
| --- | --- | --- | --- | --- |
| Pairwise Buffer | 并行处理版 Buffer | arcpy.analysis.PairwiseBuffer | core：与 Buffer 同语义，性能实现差异 | ArcPy GP（官方实现）；REST Geometry Service 有 buffer 等价 |
| Pairwise Clip | 并行处理版 Clip | arcpy.analysis.PairwiseClip | core：同上 | ArcPy GP（官方实现） |
| Pairwise Dissolve | 并行处理版 Dissolve（按属性融合） | arcpy.analysis.PairwiseDissolve | core：融合是通用运算（经典版在 Data Management） | ArcPy GP（官方实现） |
| Pairwise Erase | 并行处理版 Erase | arcpy.analysis.PairwiseErase | core：同上 | ArcPy GP（官方实现）；REST Geometry Service 有 difference 等价 |
| Pairwise Integrate | 把容差内顶点吸附到公共坐标并补顶点（坐标整理） | arcpy.analysis.PairwiseIntegrate | extension：拓扑坐标整理口径专一，先留扩展 | ArcPy GP（官方实现） |
| Pairwise Intersect | 并行处理版 Intersect | arcpy.analysis.PairwiseIntersect | core：同上 | ArcPy GP（官方实现）；REST Geometry Service 有 intersect 等价 |

### Proximity toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
| --- | --- | --- | --- | --- |
| Buffer | 按指定距离生成缓冲多边形 | arcpy.analysis.Buffer | core：最基础邻近运算，统一动词候选 gis_buffer | ArcPy GP（官方实现）；REST Geometry Service 有 buffer 等价；Esri 官方 MCP 不覆盖 |
| Create Thiessen Polygons | 由点生成泰森（Voronoi）多边形 | arcpy.analysis.CreateThiessenPolygons | core：通用空间划分 | ArcPy GP（官方实现） |
| Generate Near Table | 计算要素间距离与邻近信息并写出新表 | arcpy.analysis.GenerateNearTable | core：距离矩阵类需求通用 | ArcPy GP（官方实现） |
| Generate Origin Destination Links | 生成起点到终点的连接线（蜘蛛图） | arcpy.analysis.GenerateOriginDestinationLinks | core：OD 连线，通用 | ArcPy GP（官方实现） |
| Graphic Buffer | 带制图式端头/拐角形状的缓冲 | arcpy.analysis.GraphicBuffer | extension：制图表现导向，留扩展 | ArcPy GP（官方实现） |
| Multiple Ring Buffer | 按多个距离生成多环缓冲 | arcpy.analysis.MultipleRingBuffer | core：Buffer 的通用变体 | ArcPy GP（官方实现） |
| Near | 计算输入要素到最近要素的距离并回写 | arcpy.analysis.Near | core：最近距离，通用（注意它改写输入，Agent 调用需确认门） | ArcPy GP（官方实现） |
| Polygon Neighbors | 按多边形邻接（重叠/共边/共点）生成统计表 | arcpy.analysis.PolygonNeighbors | core：邻接关系表，通用 | ArcPy GP（官方实现） |

### Statistics toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
| --- | --- | --- | --- | --- |
| Enrich | 给数据追加人口与景观等富化事实 | arcpy.analysis.Enrich | defer：依赖 Esri 富化服务与数据，属托管数据消费 | ArcGIS GeoEnrichment 服务（Esri 托管，REST；耗额度） |
| Frequency | 统计字段唯一值出现次数并写出新表 | arcpy.analysis.Frequency | core：通用频数统计 | ArcPy GP（官方实现） |
| Summarize Nearby | 汇总指定距离内要素并计算统计 | arcpy.analysis.SummarizeNearby | defer：行驶时间/距离模式需登录 ArcGIS Online 组织账号并耗额度，直线模式可由 core 组合替代 | ArcGIS Online 托管分析工具（耗额度）；直线模式可由 ArcPy GP 组合 |
| Summarize Within | 在多边形内汇总点/线/面数量与属性统计 | arcpy.analysis.SummarizeWithin | core：面内汇总，统一动词候选 | ArcPy GP（官方实现）；ArcGIS Online 有同名托管工具 |
| Summary Statistics | 对表字段计算汇总统计 | arcpy.analysis.SummaryStatistics | core：通用统计，统一动词候选 | ArcPy GP（官方实现） |
| Tabulate Intersection | 两要素类相交并交叉制表面积/长度/计数 | arcpy.analysis.TabulateIntersection | core：交叉面积统计，遥感/土地利用常用 | ArcPy GP（官方实现） |

---


> 普查口径：ArcGIS Pro 3.4 官方工具参考（pro.arcgis.com），由两箱总览页进入、逐个打开 23 个 toolset 总览页，Tool | Description 表逐条抄录；ArcPy 入口取自各工具页 Syntax 段的官方函数名；许可信息取自两箱官方 licensing 页。抓取日期：2026-11-02。证据等级：一级（官方文档）。
>
> 平台升级原则（2026-11-02 定）：全部升级＋不重复造轮子——平台层只做动词翻译与治理，不自研算法，一律复用官方现成实现。
>
> 「轮子来源」口径：本两箱 95 个工具在官方工具页均给出 ArcPy 函数，即主通道为「ArcPy GP（官方实现，桥直调）」，无一例「仅桌面交互、无脚本入口」；同一 GP 工具按官方共享机制（ArcGIS Pro 帮助《Introduction to sharing analysis》）运行成功后可发布为 Web Tool／地理处理服务（ArcGIS Enterprise / ArcGIS Server），供 REST 调用，属可选第二通道，不逐行重复；行内仅标注有专门通道或运行语境约束的工具（如需地图对象、输入端为服务等）。
>
> 「平台判断」口径：core＝通用 GIS 基础能力、多家（QGIS/SuperMap/PostGIS/GDAL 等）有对应物，适合升为平台统一动词候选；extension＝ArcGIS 专属或需特定扩展许可/数据模型，留扩展命名空间；defer＝依赖交互式桌面、向导、账号云端，或批量破坏性操作对 Agent 不安全，暂不适合。其中「需特定扩展许可」按官方许可页的扩展模块（Spatial Analyst、3D Analyst、LocateXT）认定；Basic/Standard/Advanced 属许可级别，仅在理由中作参考，不单独决定判断。

## Conversion toolbox（arcpy.conversion）

工具集数：17｜工具总数：47｜官方定位：该工具箱包含在各种格式之间转换数据的工具。

本节平台判断分布：core 27 / extension 17 / defer 3

### Excel toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Excel To Table | 将 Microsoft Excel 文件转换为表 | arcpy.conversion.ExcelToTable | ArcPy GP（官方实现，桥直调） | core — 表格导入为通用基础能力，GDAL/pandas/QGIS 皆有对应 |
| Table To Excel | 将表导出为 Excel 文件（.xls 或 .xlsx） | arcpy.conversion.TableToExcel | ArcPy GP（官方实现，桥直调） | core — 表格导出通用 |

### From PDF toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| PDF To TIFF | 将 PDF 文件导出为 TIFF 格式 | arcpy.conversion.PDFToTIFF | ArcPy GP（官方实现，桥直调） | core — PDF 栅格化为通用转换，GDAL 有对应 |

### From Raster toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Raster to ASCII | 将栅格数据集导出为表示栅格数据的 ASCII 文件 | arcpy.conversion.RasterToASCII | ArcPy GP（官方实现，桥直调） | core — 栅格文本导出通用（GDAL AAIGrid 对应） |
| Raster to Float | 将栅格数据集导出为表示栅格数据的二进制浮点值文件 | arcpy.conversion.RasterToFloat | ArcPy GP（官方实现，桥直调） | core — 栅格原始数值导出属通用栅格 I/O |
| Raster to Point | 将栅格数据集转换为点要素 | arcpy.conversion.RasterToPoint | ArcPy GP（官方实现，桥直调） | core — 栅格转点为通用栅格矢量化 |
| Raster to Polygon | 将栅格数据集转换为面要素 | arcpy.conversion.RasterToPolygon | ArcPy GP（官方实现，桥直调） | core — 栅格矢量化通用（GDAL Polygonize 对应） |
| Raster to Polyline | 将栅格数据集转换为线要素 | arcpy.conversion.RasterToPolyline | ArcPy GP（官方实现，桥直调） | core — 栅格转线属通用栅格矢量化 |

### From WFS toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| WFS To Feature Class | 将 Web 要素服务（WFS）的要素类型导入为地理数据库中的要素类 | arcpy.conversion.WFSToFeatureClass | ArcPy GP（官方实现，桥直调；数据入口为 WFS 服务） | core — OGC WFS 读取落地为通用能力，QGIS/OGR 皆有对应 |

### GPS toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Features To GPX | 将点、多点或线要素导出为 GPX 格式文件 | arcpy.conversion.FeaturesToGPX | ArcPy GP（官方实现，桥直调） | core — GPX 为开放交换格式，各平台通用 |
| GPX To Features | 将 GPX 文件中的点数据转换为要素 | arcpy.conversion.GPXtoFeatures | ArcPy GP（官方实现，桥直调） | core — GPX 导入通用 |

### Graphics toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Features To Graphics | 将要素图层符号化后的要素转换为图形图层中的图形元素 | arcpy.conversion.FeaturesToGraphics | ArcPy GP（官方实现，需地图中的图形图层） | defer — 图形图层是 Pro 地图/布局内的桌面产物，无跨平台对应 |
| Graphics To Features | 将图形图层按其图形元素的几何转换为要素图层 | arcpy.conversion.GraphicsToFeatures | ArcPy GP（官方实现，需地图中的图形图层） | defer — 依赖桌面图形图层环境 |

### JSON toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Features To JSON | 将要素的字段、几何与空间参考导出为 Esri JSON 或 GeoJSON 文件 | arcpy.conversion.FeaturesToJSON | ArcPy GP（官方实现，桥直调） | core — GeoJSON/JSON 导出为通用交换能力 |
| JSON To Features | 将 Esri JSON 或 GeoJSON 格式文件的要素集合转换为要素类 | arcpy.conversion.JSONToFeatures | ArcPy GP（官方实现，桥直调） | core — JSON/GeoJSON 导入通用 |

### KML toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| KML To Layer | 将 KML/KMZ 文件转换为地理数据库中的数据集与图层文件（保留源符号） | arcpy.conversion.KMLToLayer | ArcPy GP（官方实现，桥直调） | core — KML 导入为要素是通用动词（OGR 对应），附带 Esri 图层文件属输出细节 |
| Layer To KML | 将要素或栅格图层导出为 KML/KMZ（含几何、像元与符号转换） | arcpy.conversion.LayerToKML | ArcPy GP（官方实现，桥直调） | core — KML 导出通用 |
| Map To KML | 将整幅地图中的要素或栅格图层导出为 KMZ 文件 | arcpy.conversion.MapToKML | ArcPy GP（官方实现，需地图对象） | defer — 以整幅桌面地图为单位导出，依赖地图文档语境 |

### Point Cloud toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Convert LAS | 在 .las、.zlas 与 .laz 之间转换压缩方式、LAS 版本与点记录格式 | arcpy.conversion.ConvertLas | ArcPy GP（官方实现，桥直调） | extension — 官方许可页注明需 Spatial Analyst 或 3D Analyst 扩展 |
| LAS Dataset To Raster | 用 LAS 数据集所引用的激光雷达点的高度、强度或 RGB 值生成栅格 | arcpy.conversion.LasDatasetToRaster | ArcPy GP（官方实现，桥直调） | extension — 需 SA/3D 扩展，且 LAS 数据集为 Esri 数据模型 |
| Mesh To LAS | 将集成网格（integrated mesh）转换为 LAS 格式点云 | arcpy.conversion.MeshToLAS | ArcPy GP（官方实现，桥直调） | extension — 需 SA/3D 扩展，源为 Esri 集成网格/I3S 生态 |
| Point Cloud To Raster | 用点云场景图层包（.slpk）或 I3S 服务中的高度值生成栅格表面 | arcpy.conversion.PointCloudToRaster | ArcPy GP（官方实现，桥直调；输入可为 I3S 服务） | extension — 需 SA/3D 扩展，输入为 Esri 3D 场景生态 |

### SAS toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| SAS To Table | 将 SAS 数据集转换为表 | arcpy.conversion.SASToTable | ArcPy GP（官方实现，桥直调） | extension — SAS 为专有统计格式生态，非 GIS 通用交换格式 |
| Table To SAS | 将表导出为 SAS 数据集 | arcpy.conversion.TableToSAS | ArcPy GP（官方实现，桥直调） | extension — 写 SAS 专有格式，同上 |

### To CAD toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Add CAD Fields | 一步添加多个 Export To CAD 所用的预留 CAD 字段 | arcpy.conversion.AddCADFields | ArcPy GP（官方实现，桥直调） | extension — 绑定 Esri CAD 转换的预留字段数据模型 |
| Export to CAD | 将一个或多个输入要素图层或要素类导出为新建或既有 CAD 文件 | arcpy.conversion.ExportCAD | ArcPy GP（官方实现，桥直调） | core — 要素导出 CAD 为通用格式互转，GDAL/QGIS 皆有对应 |

### To Collada toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Multipatch To Collada | 将一个或多个多面体（multipatch）要素导出为 COLLADA（.dae）文件及引用的纹理影像 | arcpy.conversion.MultipatchToCollada | ArcPy GP（官方实现，桥直调） | extension — 源 multipatch 为 Esri 专有 3D 数据模型 |

### To dBASE toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Table To dBASE | 将一个或多个表转换为 dBASE 表 | arcpy.conversion.TableToDBASE | ArcPy GP（官方实现，桥直调） | core — dBASE 表转换通用（shapefile 属性生态，GDAL 支持） |

### To Geodatabase toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| BIM File To Geodatabase | 将一个或多个 BIM 文件工作空间的内容导入单个地理数据库要素数据集 | arcpy.conversion.BIMFileToGeodatabase | ArcPy GP（官方实现，桥直调） | extension — BIM 工作空间数据模型专属，目标为 Esri 地理数据库模型 |
| CAD To Geodatabase | 读取 CAD 数据集并按图纸创建要素类，写入地理数据库要素数据集 | arcpy.conversion.CADToGeodatabase | ArcPy GP（官方实现，桥直调） | core — CAD 图纸转要素为通用导入能力（OGR 读 CAD 对应） |
| Export Features | 将要素类或要素图层转换为一个新的要素类 | arcpy.conversion.ExportFeatures | ArcPy GP（官方实现，桥直调） | core — 要素另存为最基础的导出动词（ogr2ogr 对应） |
| Export Table | 将表或表视图的行导出为新表 | arcpy.conversion.ExportTable | ArcPy GP（官方实现，桥直调） | core — 表导出通用 |
| Extract BIM File Floorplan | 从 BIM 文件工作空间提取 2.5D 楼层平面数据到地理数据库数据集 | arcpy.conversion.ExtractBIMFileFloorplan | ArcPy GP（官方实现，桥直调） | extension — BIM 专属提取，绑定 BIM 数据模型 |
| Extract Locations From Document | 解析含非结构化或半结构化文本的文档（如邮件、差旅单），提取位置生成点要素类 | arcpy.conversion.ExtractLocationsFromDocument | ArcPy GP（官方实现，桥直调） | extension — 官方许可页注明需 LocateXT 扩展 |
| Extract Locations From Text | 解析输入文本或文本文件，提取位置生成点要素类 | arcpy.conversion.ExtractLocationsFromText | ArcPy GP（官方实现，桥直调） | extension — 需 LocateXT 扩展，同上 |
| Feature Class To Geodatabase | 将一个或多个要素类或要素图层批量转换为地理数据库要素类 | arcpy.conversion.FeatureClassToGeodatabase | ArcPy GP（官方实现，桥直调） | core — 批量要素入库为通用数据加载动词 |
| Mobile Geodatabase To File Geodatabase | 将移动地理数据库的全部内容复制到新的文件地理数据库 | arcpy.conversion.MobileGdbToFileGdb | ArcPy GP（官方实现，桥直调） | extension — Esri 两种专有容器格式之间的专属迁移 |
| Raster To Geodatabase | 将栅格数据集批量加载进地理数据库 | arcpy.conversion.RasterToGeodatabase | ArcPy GP（官方实现，桥直调） | core — 批量栅格入库为通用数据加载动词 |
| Table To Geodatabase | 将一个或多个表批量转换为输出地理数据库中的表 | arcpy.conversion.TableToGeodatabase | ArcPy GP（官方实现，桥直调） | core — 批量表入库通用 |

### To GeoPackage toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Add Raster To GeoPackage | 将栅格数据集加载进 OGC GeoPackage 栅格金字塔 | arcpy.conversion.AddRasterToGeoPackage | ArcPy GP（官方实现，桥直调） | core — GeoPackage 为 OGC 开放标准，GDAL 有对应 |

### To Raster toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Feature to Raster | 将要素转换为栅格数据集 | arcpy.conversion.FeatureToRaster | ArcPy GP（官方实现，桥直调） | core — 矢量栅格化为通用基础能力（GDAL Rasterize 对应），且全许可级别可用 |
| Multipatch to Raster | 将多面体要素转换为栅格数据集 | arcpy.conversion.MultipatchToRaster | ArcPy GP（官方实现，桥直调） | extension — 源 multipatch 为 Esri 专有 3D 数据模型 |
| Point to Raster | 将点要素转换为栅格数据集 | arcpy.conversion.PointToRaster | ArcPy GP（官方实现，桥直调） | extension — 官方许可页：Basic/Standard 级别需 Spatial Analyst 或 3D Analyst 扩展 |
| Polygon to Raster | 将面要素转换为栅格数据集 | arcpy.conversion.PolygonToRaster | ArcPy GP（官方实现，桥直调） | extension — 需 SA/3D 扩展（Basic/Standard 级别），同上 |
| Polyline to Raster | 将线要素转换为栅格数据集 | arcpy.conversion.PolylineToRaster | ArcPy GP（官方实现，桥直调） | extension — 需 SA/3D 扩展（Basic/Standard 级别），同上 |
| Raster To Other Format | 将一个或多个栅格数据集转换为其他格式 | arcpy.conversion.RasterToOtherFormat | ArcPy GP（官方实现，桥直调） | core — 栅格格式转换通用（GDAL Translate 对应） |

### To Shapefile toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Feature Class To Shapefile | 将一个或多个要素类或要素图层的要素转换为 shapefile 并放入 shapefile 文件夹 | arcpy.conversion.FeatureClassToShapefile | ArcPy GP（官方实现，桥直调） | core — shapefile 导出为通用基础能力 |

## Cartography toolbox（arcpy.cartography）

工具集数：6｜工具总数：48｜官方定位：该工具箱中的工具旨在生产和精化数据以支持地图制作，包括创建掩膜、简化与聚合要素并降低其密度，以及注记工具与地图系列的创建。

本节平台判断分布：core 19 / extension 25 / defer 4

### Annotation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Annotate Selected Features | 按指定关联注记类的标注属性，为图层中选中的要素创建注记 | arcpy.cartography.AnnotateSelectedFeatures | ArcPy GP（官方实现，需地图图层与选中集） | defer — 依赖桌面地图中的交互选中状态 |
| Contour Annotation | 为等高线要素创建注记 | arcpy.cartography.ContourAnnotation | ArcPy GP（官方实现，桥直调） | extension — 产物为 Esri 地理数据库注记要素，绑定注记数据模型 |
| Convert Labels To Annotation | 将单个图层或整幅地图的标注转换为注记（可建标准注记或要素关联注记） | arcpy.cartography.ConvertLabelsToAnnotation | ArcPy GP（官方实现，需地图图层的标注） | defer — 输入是地图渲染出的标注，依赖地图文档状态，产物亦为 Esri 注记模型 |
| Convert Labels To Graphics | 将单个图层或整幅地图的标注转换为图形 | arcpy.cartography.ConvertLabelsToGraphics | ArcPy GP（官方实现，需地图图层的标注） | defer — 依赖地图标注渲染，产物为桌面图形 |
| Map Server Cache Tiling Scheme To Polygons | 由既有切片方案创建面要素类 | arcpy.cartography.MapServerCacheTilingSchemeToPolygons | ArcPy GP（官方实现，桥直调；对象为 ArcGIS Server 缓存切片方案） | extension — 绑定 ArcGIS Server 缓存切片体系 |
| Tiled Labels To Annotation | 按面索引图层将地图中图层的标注分幅转换为注记 | arcpy.cartography.TiledLabelsToAnnotation | ArcPy GP（官方实现，需地图图层的标注） | defer — 依赖地图标注状态，属桌面制图流程 |
| Update Annotation Reference Scale | 更新既有注记或尺寸要素类的参考比例尺 | arcpy.cartography.UpdateAnnotationReferenceScale | ArcPy GP（官方实现，桥直调） | extension — 维护 Esri 注记数据模型的专属属性 |

### Cartographic Refinement toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Align Marker To Stroke Or Fill | 将点要素类的标记符号图层对齐到指定搜索距离内最近的线描边或面填充符号图层 | arcpy.cartography.AlignMarkerToStrokeOrFill | ArcPy GP（官方实现，桥直调） | extension — 操作 Esri 符号图层，符号体系专属，且官方许可页为 Advanced 级别 |
| Calculate Color Theorem Field | 填充一个整数字段，使面可用少数颜色符号化且任意相邻两面不同色 | arcpy.cartography.CalculateColorTheoremField | ArcPy GP（官方实现，桥直调） | core — 相邻面着色编号为通用算法（QGIS 拓扑着色有对应） |
| Calculate Line Caps | 修改输入图层线符号中描边符号图层的端头（cap）类型 | arcpy.cartography.CalculateLineCaps | ArcPy GP（官方实现，桥直调） | extension — 直接改 Esri 符号定义，符号体系专属 |
| Calculate Polygon Main Angle | 计算输入面要素的主导方向角并写入字段，供定向面内符号（如标记、晕线）使用 | arcpy.cartography.CalculatePolygonMainAngle | ArcPy GP（官方实现，桥直调） | core — 主方向角为通用几何量测，结果为普通字段 |
| Convert Control Points To Vertices | 将线或面要素图层中的控制点转换为折点 | arcpy.cartography.ConvertControlPointsToVertices | ArcPy GP（官方实现，桥直调） | extension — 控制点为 Esri 制图表达（representation）专属概念 |
| Convert Marker Placement To Points | 由符号化面的标记放置（marker placement）创建点 | arcpy.cartography.ConvertMarkerPlacementToPoints | ArcPy GP（官方实现，桥直调） | extension — 依赖 Esri 符号放置体系 |
| Create Overpass | 在线相交处创建桥护栏与面掩膜以表示上跨（立交桥） | arcpy.cartography.CreateOverpass | ArcPy GP（官方实现，桥直调） | extension — Esri 制图表达/掩膜工作流，且为 Advanced 级别 |
| Create Underpass | 在线相交处创建桥护栏与面掩膜以表示下穿 | arcpy.cartography.CreateUnderpass | ArcPy GP（官方实现，桥直调） | extension — 同上 |
| Disperse Markers | 找出参考比例尺下重叠或过近的点符号，按最小间距与疏散模式将其散开 | arcpy.cartography.DisperseMarkers | ArcPy GP（官方实现，桥直调） | extension — 基于 Esri 符号与参考比例尺的符号疏散，Advanced 级别 |
| Generate Hachures For Defined Slopes | 创建多部件线或面，表示坡体上下边线之间的坡度（示坡线） | arcpy.cartography.GenerateHachuresForDefinedSlopes | ArcPy GP（官方实现，桥直调） | extension — 专用制图算子，无通用对应，且为 Advanced 级别 |
| Set Control Point At Intersect | 在一个或多个线/面要素共享的折点处创建控制点（常用于同步相邻面边界符号） | arcpy.cartography.SetControlPointAtIntersect | ArcPy GP（官方实现，桥直调） | extension — 制图表达控制点专属 |
| Set Control Point By Angle | 在线/面轮廓上方向变化角不超过指定最大值的折点处放置控制点 | arcpy.cartography.SetControlPointByAngle | ArcPy GP（官方实现，桥直调） | extension — 制图表达控制点专属，同上 |

### Generalization toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Aggregate Points | 围绕邻近的点要素簇创建面要素 | arcpy.cartography.AggregatePoints | ArcPy GP（官方实现，桥直调） | core — 点聚合为通用综合算法，各平台均有聚类成面对应 |
| Aggregate Polygons | 将指定距离内的面合并为新面 | arcpy.cartography.AggregatePolygons | ArcPy GP（官方实现，桥直调） | core — 面聚合通用 |
| Collapse Dual Lines To Centerline | 按指定的宽度容差从双线要素（如道路边线）提取中心线 | arcpy.cartography.CollapseDualLinesToCenterline | ArcPy GP（官方实现，桥直调） | core — 中心线提取为通用综合能力 |
| Collapse Hydro Polygon | 按塌缩宽度将水系面全部或部分塌缩为中心线 | arcpy.cartography.CollapseHydroPolygon | ArcPy GP（官方实现，桥直调） | extension — 水系专用塌缩规则，无通用对应，Advanced 级别 |
| Collapse Road Detail | 塌缩打断路网总体走向的小型开放道路构型（如环岛），以简化形态替代 | arcpy.cartography.CollapseRoadDetail | ArcPy GP（官方实现，桥直调） | extension — 道路专用综合规则，与 Esri 冲突解决工作流联动 |
| Create Cartographic Partitions | 创建覆盖输入要素类的面网格，每格包含的输入要素或折点数不超过指定上限 | arcpy.cartography.CreateCartographicPartitions | ArcPy GP（官方实现，桥直调） | extension — 为 Esri 综合工具配套的分区预处理，绑定其工作流 |
| Delineate Built-Up Areas | 勾画建筑密集簇的轮廓面，表示小比例尺图上的建成区 | arcpy.cartography.DelineateBuiltUpAreas | ArcPy GP（官方实现，桥直调） | extension — 专用综合算子，无通用对应 |
| Merge Divided Roads | 用单线道路要素替代成对匹配的分隔式道路车道 | arcpy.cartography.MergeDividedRoads | ArcPy GP（官方实现，桥直调） | extension — 分隔道路配对合并为专用规则算子 |
| Simplify Building | 简化建筑面边界或足迹，同时保持其基本形态与大小 | arcpy.cartography.SimplifyBuilding | ArcPy GP（官方实现，桥直调） | core — 建筑轮廓简化属通用制图综合算子 |
| Simplify Line | 移除相对次要的折点简化线，同时保持其基本形态 | arcpy.cartography.SimplifyLine | ArcPy GP（官方实现，桥直调） | core — 线简化为全平台通用基础能力 |
| Simplify Polygon | 移除相对次要的折点简化面，同时保持其基本形态 | arcpy.cartography.SimplifyPolygon | ArcPy GP（官方实现，桥直调） | core — 面简化通用 |
| Simplify Shared Edges | 简化输入要素的边线，同时保持与其他要素共享边的拓扑关系 | arcpy.cartography.SimplifySharedEdges | ArcPy GP（官方实现，桥直调） | core — 保拓扑共享边简化通用（PostGIS 保拓扑简化有对应） |
| Smooth Line | 平滑线中的尖角以改善美观或制图质量 | arcpy.cartography.SmoothLine | ArcPy GP（官方实现，桥直调） | core — 线平滑为通用几何处理 |
| Smooth Polygon | 平滑面轮廓中的尖角以改善美观或制图质量 | arcpy.cartography.SmoothPolygon | ArcPy GP（官方实现，桥直调） | core — 面平滑通用 |
| Smooth Shared Edges | 平滑输入要素的边线，同时保持共享边的拓扑关系 | arcpy.cartography.SmoothSharedEdges | ArcPy GP（官方实现，桥直调） | core — 保拓扑共享边平滑通用 |
| Thin Road Network | 生成保持连通性与总体特征的简化路网，供更小比例尺显示 | arcpy.cartography.ThinRoadNetwork | ArcPy GP（官方实现，桥直调） | core — 路网稀疏化为通用网络综合动词 |

### Graphic Conflicts toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Detect Graphic Conflict | 创建两个或多个符号化要素发生图形冲突的面 | arcpy.cartography.DetectGraphicConflict | ArcPy GP（官方实现，桥直调） | extension — 基于 Esri 符号化渲染与参考比例尺的冲突检测，Advanced 级别 |
| Propagate Displacement | 将道路调整（Resolve Road Conflicts、Merge Divided Roads）产生的位移传播到相邻要素，重建空间关系 | arcpy.cartography.PropagateDisplacement | ArcPy GP（官方实现，桥直调） | extension — 承接 Esri 冲突解决工具的位移传播，工作流专属 |
| Resolve Building Conflicts | 相对线状障碍要素移位、缩放或隐藏建筑，解决建筑间的符号冲突 | arcpy.cartography.ResolveBuildingConflicts | ArcPy GP（官方实现，桥直调） | extension — Esri 符号冲突解决体系专属，Advanced 级别 |
| Resolve Road Conflicts | 调整线段局部位置，解决符号化道路要素之间的图形冲突 | arcpy.cartography.ResolveRoadConflicts | ArcPy GP（官方实现，桥直调） | extension — 同上 |

### Map Series toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Calculate Adjacent Fields | 为格网面要素类创建字段并计算各相邻页（面）的值 | arcpy.cartography.CalculateAdjacentFields | ArcPy GP（官方实现，桥直调） | core — 图幅邻接计算为通用分幅索引处理（QGIS Atlas 有对应概念） |
| Calculate Central Meridian and Parallels | 按要素范围中心点计算中央经线与可选标准纬线，以空间参考字符串存入文本字段 | arcpy.cartography.CalculateCentralMeridianAndParallels | ArcPy GP（官方实现，桥直调） | core — 按图幅算投影参数为通用量测 |
| Calculate Grid Convergence Angle | 按要素中心点计算真北旋转角（格网收敛角）并写入字段 | arcpy.cartography.CalculateGridConvergenceAngle | ArcPy GP（官方实现，桥直调） | core — 格网收敛角为通用投影量测 |
| Calculate UTM Zone | 按要素中心点计算其 UTM 分带，以空间参考字符串存入字段 | arcpy.cartography.CalculateUTMZone | ArcPy GP（官方实现，桥直调） | core — UTM 分带计算通用 |
| Grid Index Features | 创建矩形面格网，用作空间地图系列的页索引 | arcpy.cartography.GridIndexFeatures | ArcPy GP（官方实现，桥直调） | core — 格网索引生成通用（QGIS 创建格网有对应） |
| Strip Map Index Features | 沿单个或一组线要素创建带状矩形索引面，定义带状图或沿线地图集的页 | arcpy.cartography.StripMapIndexFeatures | ArcPy GP（官方实现，桥直调） | core — 沿线分幅索引为通用分幅动词变体 |

### Masking toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
| --- | --- | --- | --- | --- |
| Cul-De-Sac Masks | 由符号化的输入线图层创建断头路（cul-de-sac）面掩膜要素类 | arcpy.cartography.CulDeSacMasks | ArcPy GP（官方实现，桥直调） | extension — Esri 符号掩膜体系专属，Advanced 级别 |
| Feature Outline Masks | 按指定距离与形状，在输入图层的符号化要素周围创建掩膜面 | arcpy.cartography.FeatureOutlineMasks | ArcPy GP（官方实现，桥直调） | extension — 掩膜须配合 Esri 符号引擎使用，体系专属 |
| Intersecting Layers Masks | 在两个符号化图层（掩膜层与被掩膜层）相交处按指定形状与大小创建掩膜面 | arcpy.cartography.IntersectingLayersMasks | ArcPy GP（官方实现，桥直调） | extension — 符号图层掩膜专属，同上 |

## 附：Esri 官方智能体 / MCP 入口（本次普查中发现）

- **MCP for ArcGIS Location Services（beta）**——Esri 官方托管的 Model Context Protocol 服务器，供应用与 AI 智能体以标准化 MCP 工具调用 ArcGIS Location Services（底图样式、静态底图切片、静态地图、Places、地理编码、路径、GeoEnrichment、高程），免直接调用 REST API；需 ArcGIS Location Platform 或 ArcGIS Online 账号。官方文档：https://developers.arcgis.com/ai/mcp-arcgis-location-services/
  - 与本两箱的关系：该 MCP 的覆盖面是位置服务，**不含 Conversion / Cartography 地理处理工具**；本两箱工具的官方复用通道仍是 ArcPy GP 直调（或自行发布为 Web Tool／地理处理服务），平台若要把两箱能力给智能体调用，仍需自建桥接层。
- 检索另见社区/伙伴 MCP 项目（如社区开源的 arcgis-portal-mcp、伙伴 SkyFi MCP Server），均非 Esri 官方出品，未计入官方通道。

## Data Management toolbox（arcpy.management）

共 42 个工具集（含子集：顶层 35 个 + 子集 7 个）与 387 个工具。官方定位：该工具箱用于开发、管理与维护要素类、数据集、图层与栅格数据结构（The Data Management toolbox contains tools that are used to develop, manage, and maintain feature classes, datasets, layers, and raster data structures）。来源：ArcGIS Pro 工具参考（pro.arcgis.com）；注：搜索索引实际返回并逐页抓取的是 3.1 文档站，3.4 站未被索引返回，此版本差已在回报中注明，工具集结构以总览页为准。

> 轮子来源口径（主代理总装时补）：本箱 387 条的官方实现均为 ArcPy 地理处理（`arcpy.management.*`），已逐条标入表中。补充：当数据托管在 ArcGIS Online/Enterprise 时，其中一部分数据操作（要素增删改、查询）在服务侧另有 REST（Feature Service applyEdits/query）与 arcgis Python API 通道，属同一官方实现的服务侧等价入口，平台可按数据位置二选一，不逐条重复标注。

### 3D Objects toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add 3D Formats To Multipatch | 将多面体要素类关联一种或多种 3D 模型格式，转换为 3D 对象要素图层 | arcpy.management.Add3DFormatsToMultipatch | extension：3D 对象图层为 ArcGIS 专属存储与纹理优化机制 | ArcPy GP（官方实现） |
| Remove 3D Formats From Multipatch | 移除 3D 对象要素图层引用的 3D 格式 | arcpy.management.Remove3DFormatsFromMultipatch | extension：同上，ArcGIS 专属 | ArcPy GP（官方实现） |

### Archiving toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Disable Archiving | 对地理数据库要素类、表或要素数据集禁用归档 | arcpy.management.DisableArchiving | extension：地理数据库归档为 ArcGIS 专属机制 | ArcPy GP（官方实现） |
| Enable Archiving | 对表、要素类或要素数据集启用归档以记录历史变更 | arcpy.management.EnableArchiving | extension：同上 | ArcPy GP（官方实现） |
| Trim Archive History | 删除非版本化归档数据集中已退役的归档记录 | arcpy.management.TrimArchiveHistory | defer：破坏性删除历史记录，需谨慎与管理员确认 | ArcPy GP（官方实现） |

### Attachments toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Attachments | 按匹配表把文件附件添加到地理数据库要素类或表的记录 | arcpy.management.AddAttachments | extension：地理数据库附件表与关系为 ArcGIS 专属实现 | ArcPy GP（官方实现） |
| Disable Attachments | 禁用附件并删除附件关系类与附件表 | arcpy.management.DisableAttachments | extension：同上，且删除附件结构 | ArcPy GP（官方实现） |
| Downgrade Attachments | 降级要素类或表的附件功能版本 | arcpy.management.DowngradeAttachments | extension：ArcGIS 版本兼容专属操作 | ArcPy GP（官方实现） |
| Enable Attachments | 启用附件并创建附件关系类与附件表 | arcpy.management.EnableAttachments | extension：同上 | ArcPy GP（官方实现） |
| Generate Attachment Match Table | 创建供添加/移除附件工具使用的匹配表 | arcpy.management.GenerateAttachmentMatchTable | extension：为 ArcGIS 附件工作流配套 | ArcPy GP（官方实现） |
| Remove Attachments | 移除地理数据库要素类或表记录的附件 | arcpy.management.RemoveAttachments | extension：同上 | ArcPy GP（官方实现） |
| Upgrade Attachments | 升级数据的附件功能 | arcpy.management.UpgradeAttachments | extension：ArcGIS 版本兼容专属操作 | ArcPy GP（官方实现） |

### Attribute Rules toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Attribute Rule | 向数据集添加一条属性规则 | arcpy.management.AddAttributeRule | extension：地理数据库属性规则（Arcade）为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Alter Attribute Rule | 修改属性规则的属性 | arcpy.management.AlterAttributeRule | extension：同上 | ArcPy GP（官方实现） |
| Delete Attribute Rule | 从数据集删除一条或多条属性规则 | arcpy.management.DeleteAttributeRule | extension：同上 | ArcPy GP（官方实现） |
| Disable Attribute Rules | 禁用数据集的一条或多条属性规则 | arcpy.management.DisableAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Enable Attribute Rules | 启用数据集中的一条或多条属性规则 | arcpy.management.EnableAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Evaluate Rules | 评估地理数据库规则与功能 | arcpy.management.EvaluateRules | extension：同上 | ArcPy GP（官方实现） |
| Export Attribute Rules | 将属性规则导出为 CSV 文件 | arcpy.management.ExportAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Import Attribute Rules | 从 CSV 文件向数据集导入属性规则 | arcpy.management.ImportAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Reorder Attribute Rule | 调整属性规则的求值顺序 | arcpy.management.ReorderAttributeRule | extension：同上 | ArcPy GP（官方实现） |

### Catalog Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Items To Catalog Dataset | 将工作空间条目与图层（数据集、栅格、要素、镶嵌图层等）加入已有目录数据集 | arcpy.management.AddItemsToCatalogDataset | extension：目录数据集/目录图层为 ArcGIS 新专属概念 | ArcPy GP（官方实现） |
| Add Portal Items To Catalog Dataset | 将门户的要素、地图、影像、场景、切片等服务条目加入目录数据集 | arcpy.management.AddPortalItemsToCatalogDataset | extension：依赖 ArcGIS 门户体系 | ArcPy GP（官方实现） |
| Create Catalog Dataset | 创建可添加图层、栅格、数据集等集合的目录数据集 | arcpy.management.CreateCatalogDataset | extension：同上 | ArcPy GP（官方实现） |

### Contingent Values toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Contingent Value | 向要素类或表的字段组添加一个关联值（条件值） | arcpy.management.AddContingentValue | extension：关联值/字段组为地理数据库专属行为 | ArcPy GP（官方实现） |
| Alter Field Group | 修改字段组的属性 | arcpy.management.AlterFieldGroup | extension：同上 | ArcPy GP（官方实现） |
| Create Field Group | 为要素类或表创建供关联值使用的字段组 | arcpy.management.CreateFieldGroup | extension：同上 | ArcPy GP（官方实现） |
| Delete Field Group | 从表或要素类删除字段组 | arcpy.management.DeleteFieldGroup | extension：同上 | ArcPy GP（官方实现） |
| Export Contingent Values | 将字段组与关联值导出为 CSV 文件 | arcpy.management.ExportContingentValues | extension：同上 | ArcPy GP（官方实现） |
| Import Contingent Values | 从 CSV 文件导入多个关联值与字段组到数据集 | arcpy.management.ImportContingentValues | extension：同上 | ArcPy GP（官方实现） |
| Remove Contingent Value | 从字段组移除一个关联值 | arcpy.management.RemoveContingentValue | extension：同上 | ArcPy GP（官方实现） |

### Data Comparison toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Detect Feature Changes | 匹配更新线与基线线，检测空间/属性变化并输出带变化信息的要素类 | arcpy.management.DetectFeatureChanges | core：数据集变更检测为通用基础能力 | ArcPy GP（官方实现） |
| Feature Compare | 比较两个要素类或图层并返回比较结果 | arcpy.management.FeatureCompare | core：通用数据对比能力 | ArcPy GP（官方实现） |
| File Compare | 比较两个文件并返回比较结果 | arcpy.management.FileCompare | core：通用文件对比能力 | ArcPy GP（官方实现） |
| Raster Compare | 比较两个栅格数据集或镶嵌数据集的属性 | arcpy.management.RasterCompare | core：通用栅格对比能力 | ArcPy GP（官方实现） |
| Table Compare | 比较两个表或表视图并返回比较结果 | arcpy.management.TableCompare | core：通用表格对比能力 | ArcPy GP（官方实现） |
| TIN Compare | 比较两个 TIN 并返回比较结果 | arcpy.management.TINCompare | core：通用表面数据对比能力 | ArcPy GP（官方实现） |

### Distributed Geodatabase toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Compare Replica Schema | 生成描述副本与相对副本之间模式差异的 XML 文件 | arcpy.management.CompareReplicaSchema | extension：企业级地理数据库复制为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Create Replica | 从企业级地理数据库中指定的要素类、图层、数据集与表创建副本 | arcpy.management.CreateReplica | extension：同上 | ArcPy GP（官方实现） |
| Create Replica From Server | 通过 ArcGIS Server 地理数据服务从远程地理数据库创建副本 | arcpy.management.CreateReplicaFromServer | extension：同上，依赖 ArcGIS Server | ArcPy GP（官方实现） |
| Disable Replica Tracking | 禁用数据的副本追踪 | arcpy.management.DisableReplicaTracking | extension：同上 | ArcPy GP（官方实现） |
| Enable Replica Tracking | 启用副本追踪以支持离线地图与分布式协作 | arcpy.management.EnableReplicaTracking | extension：同上 | ArcPy GP（官方实现） |
| Export Acknowledgement Message | 创建确认已接收数据变更消息的确认文件 | arcpy.management.ExportAcknowledgementMessage | extension：同上 | ArcPy GP（官方实现） |
| Export Data Change Message | 创建包含副本更新的增量文件 | arcpy.management.ExportDataChangeMessage | extension：同上 | ArcPy GP（官方实现） |
| Export Replica Schema | 创建一向/双向副本的模式文件 | arcpy.management.ExportReplicaSchema | extension：同上 | ArcPy GP（官方实现） |
| Import Message | 将增量文件的变更或确认消息导入副本地理数据库 | arcpy.management.ImportMessage | extension：同上 | ArcPy GP（官方实现） |
| Import Replica Schema | 用副本地理数据库与 XML 模式文件应用副本模式差异 | arcpy.management.ImportReplicaSchema | extension：同上 | ArcPy GP（官方实现） |
| Re-export Unacknowledged Messages | 创建包含未确认副本更新的增量文件 | arcpy.management.ReexportUnacknowledgedMessages | extension：同上 | ArcPy GP（官方实现） |
| Synchronize Changes | 按指定方向在两个副本地理数据库之间同步更新 | arcpy.management.SynchronizeChanges | extension：同上 | ArcPy GP（官方实现） |
| Unregister Replica | 从企业级地理数据库注销副本 | arcpy.management.UnregisterReplica | extension：同上 | ArcPy GP（官方实现） |

### Domains toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Coded Value To Domain | 向域的编码值列表添加一个值 | arcpy.management.AddCodedValueToDomain | core：值域约束为多家数据库/GIS 通用的数据完整性能力 | ArcPy GP（官方实现） |
| Alter Domain | 修改工作空间中已有属性域的属性 | arcpy.management.AlterDomain | core：同上 | ArcPy GP（官方实现） |
| Assign Domain To Field | 为指定字段（可按子类型）设置域 | arcpy.management.AssignDomainToField | core：同上 | ArcPy GP（官方实现） |
| Create Domain | 在指定工作空间创建属性域 | arcpy.management.CreateDomain | core：同上 | ArcPy GP（官方实现） |
| Delete Coded Value From Domain | 从编码值域中移除一个值 | arcpy.management.DeleteCodedValueFromDomain | core：同上 | ArcPy GP（官方实现） |
| Delete Domain | 从工作空间删除一个域 | arcpy.management.DeleteDomain | core：同上，删除需谨慎但属通用域管理 | ArcPy GP（官方实现） |
| Domain To Table | 从属性域创建表 | arcpy.management.DomainToTable | core：域与表互转为通用能力 | ArcPy GP（官方实现） |
| Remove Domain From Field | 移除要素类或表字段与属性域的关联 | arcpy.management.RemoveDomainFromField | core：同上 | ArcPy GP（官方实现） |
| Set Value For Range Domain | 设置已有范围域的最小值与最大值 | arcpy.management.SetValueForRangeDomain | core：同上 | ArcPy GP（官方实现） |
| Sort Coded Value Domain | 按编码或描述升/降序排序编码值域 | arcpy.management.SortCodedValueDomain | core：同上 | ArcPy GP（官方实现） |
| Table To Domain | 用表中的值创建或更新编码值域 | arcpy.management.TableToDomain | core：同上 | ArcPy GP（官方实现） |

### Feature Binning toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Disable Feature Binning | 对要素类禁用数据库计算的要素分箱 | arcpy.management.DisableFeatureBinning | extension：要素分箱为 ArcGIS 高级可视化专属能力 | ArcPy GP（官方实现） |
| Enable Feature Binning | 对要素类启用数据库计算的要素分箱 | arcpy.management.EnableFeatureBinning | extension：同上 | ArcPy GP（官方实现） |
| Manage Feature Bin Cache | 管理已启用数据库计算分箱数据的分箱缓存 | arcpy.management.ManageFeatureBinCache | extension：同上 | ArcPy GP（官方实现） |

### Feature Class toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Append Annotation Feature Classes | 合并多个注记要素类为单个注记要素类或追加到已有注记要素类 | arcpy.management.AppendAnnotationFeatureClasses | extension：地理数据库注记为 ArcGIS 专属类型 | ArcPy GP（官方实现） |
| Create Feature Class | 在地理数据库中创建空要素类或在文件夹中创建 shapefile | arcpy.management.CreateFeatureClass | core：建要素类为通用基础能力，适合统一动词候选 | ArcPy GP（官方实现） |
| Create Unregistered Feature Class | 在数据库/企业级地理数据库中创建未注册的空要素类 | arcpy.management.CreateUnregisteredFeatureClass | extension：企业级地理数据库注册机制专属 | ArcPy GP（官方实现） |
| Integrate | 将容差内顶点赋予共同坐标并在交点/边附近加顶点，使要素重合对齐 | arcpy.management.Integrate | core：坐标整合/捕捉对齐为通用几何治理能力 | ArcPy GP（官方实现） |
| Recalculate Feature Class Extent | 按要素重算要素类的 XY/Z/M 范围属性 | arcpy.management.RecalculateFeatureClassExtent | core：范围重算为通用元数据维护 | ArcPy GP（官方实现） |
| Set Feature Class Split Model | 定义要素类上分割操作的行为 | arcpy.management.SetFeatureClassSplitModel | extension：ArcGIS 编辑分割模型专属 | ArcPy GP（官方实现） |

### Features toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add XY Coordinates | 添加 POINT_X/POINT_Y（及 Z/M）字段并计算点坐标值 | arcpy.management.AddXYCoordinates | core：坐标提取为通用能力 | ArcPy GP（官方实现） |
| Adjust 3D Z | 修改 3D 要素的 Z 值 | arcpy.management.Adjust3DZ | core：高程值调整为通用能力 | ArcPy GP（官方实现） |
| Bearing Distance To Line | 由表中 XY、方位角与距离字段生成测地/平面线要素 | arcpy.management.BearingDistanceToLine | core：方位距离建线为通用建图能力 | ArcPy GP（官方实现） |
| Calculate Geometry Attributes | 将长度、面积、坐标等几何特征写入属性字段 | arcpy.management.CalculateGeometryAttributes | core：几何属性计算为通用能力 | ArcPy GP（官方实现） |
| Check Geometry | 生成要素类几何问题报告 | arcpy.management.CheckGeometry | core：几何校验为通用能力 | ArcPy GP（官方实现） |
| Copy Features | 将输入要素类/图层要素复制到新要素类 | arcpy.management.CopyFeatures | core：复制要素为通用能力 | ArcPy GP（官方实现） |
| Delete Features | 删除输入中全部或选中的要素子集 | arcpy.management.DeleteFeatures | defer：破坏性批量删除，需确认 | ArcPy GP（官方实现） |
| Dice | 按顶点上限将超大要素切分为较小要素 | arcpy.management.Dice | core：大要素切分为通用性能治理能力 | ArcPy GP（官方实现） |
| Feature Envelope To Polygon | 为每个输入要素生成其包络矩形面 | arcpy.management.FeatureEnvelopeToPolygon | core：包络生成为通用几何转换 | ArcPy GP（官方实现） |
| Feature To Line | 将面边界转线或在交点处分割线/面生成线要素 | arcpy.management.FeatureToLine | core：几何类型转换为通用能力 | ArcPy GP（官方实现） |
| Feature To Point | 由要素质心或内部点生成点要素 | arcpy.management.FeatureToPoint | core：同上 | ArcPy GP（官方实现） |
| Feature To Polygon | 由线/面围成的区域生成面要素 | arcpy.management.FeatureToPolygon | core：同上 | ArcPy GP（官方实现） |
| Feature Vertices To Points | 由要素指定顶点/位置生成点要素 | arcpy.management.FeatureVerticesToPoints | core：同上 | ArcPy GP（官方实现） |
| Geodetic Densify | 用测地线段的加密近似替换要素线段 | arcpy.management.GeodeticDensify | core：测地加密为通用几何处理 | ArcPy GP（官方实现） |
| Minimum Bounding Geometry | 为每个要素或分组生成最小边界几何面 | arcpy.management.MinimumBoundingGeometry | core：最小边界为通用几何派生 | ArcPy GP（官方实现） |
| Multipart To Singlepart | 将多部件要素拆为单部件要素 | arcpy.management.MultipartToSinglepart | core：多部件拆分为通用能力 | ArcPy GP（官方实现） |
| Points To Line | 由点生成线要素 | arcpy.management.PointsToLine | core：点连线为通用能力 | ArcPy GP（官方实现） |
| Polygon To Line | 将面边界转换为线（可考虑邻接面） | arcpy.management.PolygonToLine | core：几何类型转换为通用能力 | ArcPy GP（官方实现） |
| Repair Geometry | 检查并修复要素几何问题 | arcpy.management.RepairGeometry | core：几何修复为通用能力 | ArcPy GP（官方实现） |
| Split Line At Point | 按与点要素的交点/邻近关系分割线要素 | arcpy.management.SplitLineAtPoint | core：按点分割为通用编辑能力 | ArcPy GP（官方实现） |
| Split Line At Vertices | 在顶点处分割线/面生成折线要素类 | arcpy.management.SplitLineAtVertices | core：同上 | ArcPy GP（官方实现） |
| Subdivide Polygon | 将面要素划分为若干等面积/等份部分 | arcpy.management.SubdividePolygon | core：面细分为通用能力 | ArcPy GP（官方实现） |
| Table To Ellipse | 由表中中心、长短轴与方位角字段生成测地/平面椭圆要素 | arcpy.management.TableToEllipse | core：参数化建要素为通用能力 | ArcPy GP（官方实现） |
| Unsplit Line | 聚合端点重合（可选属性相同）的线要素 | arcpy.management.UnsplitLine | core：线合并为通用能力 | ArcPy GP（官方实现） |
| XY Table To Point | 由表中 X/Y/Z 坐标生成点要素类 | arcpy.management.XYTableToPoint | core：坐标表建点为通用能力 | ArcPy GP（官方实现） |
| XY To Line | 由表中起止点坐标字段生成测地/平面线要素 | arcpy.management.XYToLine | core：坐标表建线为通用能力 | ArcPy GP（官方实现） |

### Fields toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Field | 向表、要素类表、图层或带属性表的栅格添加新字段 | arcpy.management.AddField | core：建字段为通用基础能力 | ArcPy GP（官方实现） |
| Add Fields (multiple) | 向表、要素类或栅格一次添加多个新字段 | arcpy.management.AddFields | core：批量建字段为通用能力 | ArcPy GP（官方实现） |
| Add Global IDs | 向地理数据库要素类、表与要素数据集列表添加全局 ID | arcpy.management.AddGlobalIDs | extension：GlobalID 为地理数据库专属标识机制 | ArcPy GP（官方实现） |
| Add GPS Metadata Fields | 向地理数据库要素类添加 GNSS 字段 | arcpy.management.AddGPSMetadataFields | core：GNSS 元数据字段为通用定位数据能力 | ArcPy GP（官方实现） |
| Add Incrementing ID Field | 向企业数据库表/要素类添加数据库维护的自增 ID 字段 | arcpy.management.AddIncrementingIDField | extension：依赖特定企业数据库与要素服务编辑 | ArcPy GP（官方实现） |
| Alter Field | 重命名地理数据库表/要素类的字段或字段别名 | arcpy.management.AlterField | core：字段改名为通用能力 | ArcPy GP（官方实现） |
| Assign Default To Field | 为指定字段创建默认值，新行自动填入 | arcpy.management.AssignDefaultToField | core：字段默认值为通用能力 | ArcPy GP（官方实现） |
| Batch Update Fields | 按定义表模式批量变换表/要素类字段并生成新表/要素类 | arcpy.management.BatchUpdateFields | core：批量字段变换为通用能力 | ArcPy GP（官方实现） |
| Calculate End Time | 基于另一字段的时间值计算要素结束时间 | arcpy.management.CalculateEndTime | core：时间字段计算为通用能力 | ArcPy GP（官方实现） |
| Calculate Field | 计算要素类、图层或栅格某个字段的值 | arcpy.management.CalculateField | core：字段计算为通用基础能力 | ArcPy GP（官方实现） |
| Calculate Fields (multiple) | 计算要素类、图层或栅格两个以上字段的值 | arcpy.management.CalculateFields | core：同上 | ArcPy GP（官方实现） |
| Convert Time Field | 将日期时间字段值转换到另一字段（类型/格式互转） | arcpy.management.ConvertTimeField | core：时间格式转换为通用能力 | ArcPy GP（官方实现） |
| Convert Time Zone | 将日期字段的时间值从一个时区转换到另一个时区 | arcpy.management.ConvertTimeZone | core：时区转换为通用能力 | ArcPy GP（官方实现） |
| Delete Field | 从表、要素类、图层或栅格删除一个或多个字段 | arcpy.management.DeleteField | defer：破坏性删字段，需确认 | ArcPy GP（官方实现） |
| Disable COGO | 对线要素类禁用 COGO 并移除 COGO 字段与标注/符号 | arcpy.management.DisableCOGO | extension：COGO 为 ArcGIS 测量编辑专属 | ArcPy GP（官方实现） |
| Disable Editor Tracking | 对要素类、表、要素数据集或镶嵌数据集禁用编辑追踪 | arcpy.management.DisableEditorTracking | extension：编辑追踪为地理数据库专属机制 | ArcPy GP（官方实现） |
| Enable COGO | 对线要素类启用 COGO 并添加 COGO 字段与标注 | arcpy.management.EnableCOGO | extension：同上 | ArcPy GP（官方实现） |
| Enable Editor Tracking | 对地理数据库要素类、表、要素数据集或关系类启用编辑追踪 | arcpy.management.EnableEditorTracking | extension：同上 | ArcPy GP（官方实现） |
| Encode Field | 将分类值转换为多个数值字段（独热等编码）供数据科学流程使用 | arcpy.management.EncodeField | core：分类编码为通用数据预处理 | ArcPy GP（官方实现） |
| Field Statistics To Table | 为一个或多个字段生成描述统计表 | arcpy.management.FieldStatisticsToTable | core：字段统计为通用能力 | ArcPy GP（官方实现） |
| Reclassify Field | 按手动界限或重分类方法将数值/文本字段值重分为类别 | arcpy.management.ReclassifyField | core：重分类为通用能力 | ArcPy GP（官方实现） |
| Standardize Field | 用 z-score、min-max 等方法将字段值标准化到指定尺度 | arcpy.management.StandardizeField | core：标准化为通用数据预处理 | ArcPy GP（官方实现） |
| Transform Field | 用对数、平方根、Box-Cox 等函数变换连续字段值分布 | arcpy.management.TransformField | core：字段变换为通用数据预处理 | ArcPy GP（官方实现） |
| Transpose Fields | 将字段/列中的数据转置为新表/要素类中的行 | arcpy.management.TransposeFields | core：转置为通用表格操作 | ArcPy GP（官方实现） |

### File Geodatabase toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Compact | 重排文件地理数据库磁盘存储，常可减小体积并提升性能 | arcpy.management.Compact | extension：文件地理数据库为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Compress File Geodatabase Data | 将地理数据库、要素数据集或单个要素类/表压缩为只读格式 | arcpy.management.CompressFileGeodatabaseData | extension：同上 | ArcPy GP（官方实现） |
| Generate File Geodatabase License | 生成用于显示许可文件地理数据库内容的许可文件（.sdlic） | arcpy.management.GenerateFileGeodatabaseLicense | extension：ArcGIS 许可机制专属 | ArcPy GP（官方实现） |
| Generate Licensed File Geodatabase | 生成定义并限制文件地理数据库内容显示的许可定义文件 | arcpy.management.GenerateLicensedFileGeodatabase | extension：同上 | ArcPy GP（官方实现） |
| Recover File Geodatabase | 从已损坏的文件地理数据库中恢复数据 | arcpy.management.RecoverFileGeodatabase | extension：同上 | ArcPy GP（官方实现） |
| Uncompress File Geodatabase Data | 解压地理数据库、要素数据集或单个要素类/表 | arcpy.management.UncompressFileGeodatabaseData | extension：同上 | ArcPy GP（官方实现） |

### General toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Append | 将多个输入数据集追加（可选更新）到已有目标数据集 | arcpy.management.Append | core：追加为通用基础能力，适合统一动词候选 | ArcPy GP（官方实现） |
| Copy | 复制输入数据 | arcpy.management.Copy | core：复制为通用能力 | ArcPy GP（官方实现） |
| Create Database View | 基于 SQL 表达式在数据库中创建视图 | arcpy.management.CreateDatabaseView | core：数据库视图为通用能力 | ArcPy GP（官方实现） |
| Delete | 永久删除数据、工作空间及其包含项 | arcpy.management.Delete | defer：永久破坏性删除，需管理员级确认 | ArcPy GP（官方实现） |
| Delete Identical | 删除一组字段值（可含几何）完全相同的重复记录 | arcpy.management.DeleteIdentical | defer：破坏性批量去重删除，需确认 | ArcPy GP（官方实现） |
| Export Report To PDF | 将 ArcGIS Pro 报表导出为 PDF 文件 | arcpy.management.ExportReportToPDF | defer：依赖桌面报表对象与交互环境 | ArcPy GP（官方实现） |
| Find Identical | 报告字段值完全相同的记录并生成清单表 | arcpy.management.FindIdentical | core：重复检测为通用能力 | ArcPy GP（官方实现） |
| Merge | 将多个输入数据集合并为单个新输出数据集 | arcpy.management.Merge | core：合并为通用基础能力 | ArcPy GP（官方实现） |
| Rename | 更改数据集名称 | arcpy.management.Rename | core：重命名为通用能力 | ArcPy GP（官方实现） |
| Sort | 按一个或多个字段升/降序重排记录并写入新数据集 | arcpy.management.Sort | core：排序为通用能力 | ArcPy GP（官方实现） |
| Transfer Files | 在文件系统与云存储工作空间之间传输文件 | arcpy.management.TransferFiles | core：文件传输为通用能力 | ArcPy GP（官方实现） |

### Generalization toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Dissolve | 按指定属性聚合要素（融合） | arcpy.management.Dissolve | core：融合为通用基础能力 | ArcPy GP（官方实现） |
| Eliminate | 将小面合并到面积最大或共享边界最长的邻接面，消除碎面 | arcpy.management.Eliminate | core：碎面消除为通用综合能力 | ArcPy GP（官方实现） |
| Eliminate Polygon Part | 删除面中指定大小的部件或洞并输出新要素类 | arcpy.management.EliminatePolygonPart | core：同上 | ArcPy GP（官方实现） |

### Geodatabase Administration toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze Datasets | 更新企业级地理数据库基表、增量表、归档表及其索引的数据库统计 | arcpy.management.AnalyzeDatasets | extension：企业级地理数据库运维专属 | ArcPy GP（官方实现） |
| Change Privileges | 设置/更改企业数据库数据集、要素类或表的用户访问权限 | arcpy.management.ChangePrivileges | defer：权限管理需管理员权限 | ArcPy GP（官方实现） |
| Compress | 压缩企业级地理数据库，删除未被版本引用的状态与冗余行 | arcpy.management.Compress | extension：版本状态压缩为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Configure Geodatabase Log File Tables | 更改旧版企业级地理数据库日志文件表类型 | arcpy.management.ConfigureGeodatabaseLogFileTables | extension：同上 | ArcPy GP（官方实现） |
| Create Database Sequence | 在地理数据库中创建数据库序列供自定义应用使用 | arcpy.management.CreateDatabaseSequence | extension：地理数据库专属 | ArcPy GP（官方实现） |
| Create Database User | 创建有足够权限在数据库中建数据的数据库用户 | arcpy.management.CreateDatabaseUser | defer：建用户需管理员权限 | ArcPy GP（官方实现） |
| Create Enterprise Geodatabase | 创建数据库、存储位置与地理数据库管理员用户并建企业级地理数据库 | arcpy.management.CreateEnterpriseGeodatabase | defer：建库需管理员权限且为 ArcGIS 专属部署 | ArcPy GP（官方实现） |
| Create Role | 创建数据库角色以便增删用户 | arcpy.management.CreateRole | defer：角色管理需管理员权限 | ArcPy GP（官方实现） |
| Delete Database Sequence | 从地理数据库删除数据库序列 | arcpy.management.DeleteDatabaseSequence | extension：地理数据库专属 | ArcPy GP（官方实现） |
| Delete Schema Geodatabase | 删除 Oracle 中用户模式下的地理数据库 | arcpy.management.DeleteSchemaGeodatabase | defer：破坏性删库，需管理员确认 | ArcPy GP（官方实现） |
| Diagnose Version Metadata | 识别传统版本与状态系统表的不一致 | arcpy.management.DiagnoseVersionMetadata | extension：版本元数据为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Diagnose Version Tables | 识别传统版本增量（A/D）表的不一致 | arcpy.management.DiagnoseVersionTables | extension：同上 | ArcPy GP（官方实现） |
| Enable Enterprise Geodatabase | 在已有数据库中创建系统表、存储过程等以启用地理数据库功能 | arcpy.management.EnableEnterpriseGeodatabase | defer：启用企业库需管理员权限 | ArcPy GP（官方实现） |
| Export Geodatabase Configuration Keywords | 将企业级地理数据库配置关键字及参数导出为可编辑文件 | arcpy.management.ExportGeodatabaseConfigurationKeywords | extension：配置关键字为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Import Geodatabase Configuration Keywords | 导入配置关键字文件以定义企业级地理数据库存储参数 | arcpy.management.ImportGeodatabaseConfigurationKeywords | extension：同上 | ArcPy GP（官方实现） |
| Migrate Storage | 将 Oracle/SQL Server 地理数据库列数据迁移到另一数据类型的列 | arcpy.management.MigrateStorage | extension：同上 | ArcPy GP（官方实现） |
| Rebuild Indexes | 重建企业级地理数据库的属性/空间索引及版本系统表索引 | arcpy.management.RebuildIndexes | extension：企业库索引重建，虽索引通用但此工具面向 ArcGIS 系统表 | ArcPy GP（官方实现） |
| Register With Geodatabase | 将第三方工具在数据库中创建的要素类、表、视图、栅格注册到地理数据库 | arcpy.management.RegisterWithGeodatabase | extension：地理数据库注册机制专属 | ArcPy GP（官方实现） |
| Repair Version Metadata | 修复传统版本系统表的不一致 | arcpy.management.RepairVersionMetadata | extension：同上 | ArcPy GP（官方实现） |
| Repair Version Tables | 修复传统版本增量（A/D）表的不一致 | arcpy.management.RepairVersionTables | extension：同上 | ArcPy GP（官方实现） |
| Update Enterprise Geodatabase License | 更新企业级地理数据库中的 ArcGIS Server 许可 | arcpy.management.UpdateEnterpriseGeodatabaseLicense | extension：ArcGIS 许可专属 | ArcPy GP（官方实现） |
| Update Portal Dataset Owner | 将数据集的门户所有者更新为另一用户 | arcpy.management.UpdatePortalDatasetOwner | extension：依赖 ArcGIS 门户体系 | ArcPy GP（官方实现） |
| Upgrade Dataset | 将镶嵌、网络、注记、宗地、追踪网络、公用设施网络等数据集模式升级到当前版本 | arcpy.management.UpgradeDataset | extension：ArcGIS 数据集版本升级专属 | ArcPy GP（官方实现） |
| Upgrade Geodatabase | 将地理数据库升级到最新 ArcGIS 版本 | arcpy.management.UpgradeGeodatabase | extension：同上 | ArcPy GP（官方实现） |

### Indexes toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Attribute Index | 向表、要素类、shapefile 或带属性关系类添加属性索引 | arcpy.management.AddAttributeIndex | core：属性索引为通用基础能力 | ArcPy GP（官方实现） |
| Add Spatial Index | 向 shapefile 或各类地理数据库要素类添加/重建空间索引 | arcpy.management.AddSpatialIndex | core：空间索引为通用基础能力 | ArcPy GP（官方实现） |
| Remove Attribute Index | 从表、要素类、shapefile 删除属性索引 | arcpy.management.RemoveAttributeIndex | core：索引管理为通用能力 | ArcPy GP（官方实现） |
| Remove Spatial Index | 从 shapefile 或各类地理数据库要素类删除空间索引 | arcpy.management.RemoveSpatialIndex | core：同上 | ArcPy GP（官方实现） |

### Joins and Relates toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Join | 基于公共字段将图层临时连接到另一图层或表 | arcpy.management.AddJoin | core：连接为通用基础能力 | ArcPy GP（官方实现） |
| Add Relate | 基于字段值将图层与另一图层或表临时关联 | arcpy.management.AddRelate | core：关联为通用能力 | ArcPy GP（官方实现） |
| Add Spatial Join | 基于空间关系将一个要素的属性临时连接到另一要素 | arcpy.management.AddSpatialJoin | core：空间连接为通用基础能力 | ArcPy GP（官方实现） |
| Join Field | 基于公共属性字段将表内容永久连接到另一表 | arcpy.management.JoinField | core：永久字段连接为通用能力 | ArcPy GP（官方实现） |
| Remove Join | 从要素图层或表视图移除连接 | arcpy.management.RemoveJoin | core：同上 | ArcPy GP（官方实现） |
| Remove Relate | 从要素图层或表视图移除关联 | arcpy.management.RemoveRelate | core：同上 | ArcPy GP（官方实现） |
| Validate Join | 验证两图层/表连接的字段名、OID、匹配与一对一/一对多等性质 | arcpy.management.ValidateJoin | core：连接校验为通用能力 | ArcPy GP（官方实现） |

### LAS Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Files To LAS Dataset | 向 LAS 数据集添加 LAS 文件与表面约束要素的引用 | arcpy.management.AddFilesToLASDataset | core：LAS 点云集合管理为多家共有能力（LAS 为开放格式） | ArcPy GP（官方实现） |
| Build LAS Dataset Pyramid | 构建/更新 LAS 数据集显示缓存以优化渲染 | arcpy.management.BuildLASDatasetPyramid | extension：LAS 数据集金字塔为 ArcGIS 数据集实现 | ArcPy GP（官方实现） |
| Create LAS Dataset | 创建引用一个或多个 LAS 文件（可选表面约束）的 LAS 数据集 | arcpy.management.CreateLASDataset | core：创建点云数据集为通用能力 | ArcPy GP（官方实现） |
| LAS Dataset Statistics | 计算/更新 LAS 数据集统计并可生成统计报告 | arcpy.management.LASDatasetStatistics | core：点云统计为通用能力 | ArcPy GP（官方实现） |
| LAS Point Statistics As Raster | 生成像元值反映 LAS 点统计信息的栅格 | arcpy.management.LASPointStatisticsAsRaster | core：点云栅格化统计为通用能力 | ArcPy GP（官方实现） |
| Remove Files From LAS Dataset | 从 LAS 数据集移除 LAS 文件与表面约束要素 | arcpy.management.RemoveFilesFromLASDataset | core：点云集合管理为通用能力 | ArcPy GP（官方实现） |

### Layers and Table Views toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Apply Symbology From Layer | 将指定图层/图层文件的符号系统应用到输入图层 | arcpy.management.ApplySymbologyFromLayer | defer：符号系统依赖桌面图层交互 | ArcPy GP（官方实现） |
| Make Aggregation Query Layer | 创建按时间/范围/属性动态汇总聚合 DBMS 表并连接要素图层的查询图层 | arcpy.management.MakeAggregationQueryLayer | core：动态聚合查询图层为通用能力 | ArcPy GP（官方实现） |
| Make Building Layer | 从 BIM 工作空间或地理数据库数据集创建复合建筑图层 | arcpy.management.MakeBuildingLayer | extension：建筑图层为 ArcGIS BIM 集成专属 | ArcPy GP（官方实现） |
| Make Feature Layer | 从要素类或图层文件创建临时要素图层 | arcpy.management.MakeFeatureLayer | core：建图层为通用基础能力 | ArcPy GP（官方实现） |
| Make Image Server Layer | 从影像服务创建临时栅格图层 | arcpy.management.MakeImageServerLayer | core：服务图层创建为通用能力 | ArcPy GP（官方实现） |
| Make LAS Dataset Layer | 创建可过滤 LAS 点并控制表面约束的 LAS 数据集图层 | arcpy.management.MakeLASDatasetLayer | core：点云图层创建为通用能力 | ArcPy GP（官方实现） |
| Make Mosaic Layer | 从镶嵌数据集或图层文件创建临时镶嵌图层 | arcpy.management.MakeMosaicLayer | extension：镶嵌数据集为 ArcGIS 专属概念 | ArcPy GP（官方实现） |
| Make Query Layer | 基于 SQL 查询从 DBMS 表创建查询图层 | arcpy.management.MakeQueryLayer | core：SQL 查询图层为通用能力 | ArcPy GP（官方实现） |
| Make Query Table | 对数据库执行 SQL 查询并以图层/表视图呈现（可连接多表或取子集） | arcpy.management.MakeQueryTable | core：同上 | ArcPy GP（官方实现） |
| Make Raster Layer | 从栅格数据集或图层文件创建临时栅格图层 | arcpy.management.MakeRasterLayer | core：建栅格图层为通用能力 | ArcPy GP（官方实现） |
| Make Scene Layer | 从场景图层包或场景服务创建场景图层 | arcpy.management.MakeSceneLayer | extension：场景图层/I3S 为 ArcGIS 平台概念 | ArcPy GP（官方实现） |
| Make Table View | 从表或要素类创建临时表视图 | arcpy.management.MakeTableView | core：建表视图为通用能力 | ArcPy GP（官方实现） |
| Make TIN Layer | 从 TIN 数据集或图层文件创建临时 TIN 图层 | arcpy.management.MakeTINLayer | core：建 TIN 图层为通用能力 | ArcPy GP（官方实现） |
| Make WCS Layer | 从 WCS 服务创建临时栅格图层 | arcpy.management.MakeWCSLayer | core：OGC WCS 为开放标准，通用能力 | ArcPy GP（官方实现） |
| Make XY Event Layer | 基于表中 XY（可选 Z）坐标创建临时点要素图层 | arcpy.management.MakeXYEventLayer | core：事件图层为通用能力 | ArcPy GP（官方实现） |
| Match Layer Symbology To A Style | 按字段/表达式匹配样式符号名，为图层创建唯一值符号系统 | arcpy.management.MatchLayerSymbologyToAStyle | defer：符号匹配依赖桌面样式交互 | ArcPy GP（官方实现） |
| Save To Layer File | 将地图图层保存为图层文件（.lyrx，含符号、标注、弹窗等） | arcpy.management.SaveToLayerFile | extension：.lyrx 为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Select Layer By Attribute | 按属性查询添加、更新或移除图层选择集 | arcpy.management.SelectLayerByAttribute | core：属性选择为通用基础能力 | ArcPy GP（官方实现） |
| Select Layer By Location | 按与另一数据集的空间关系选择要素 | arcpy.management.SelectLayerByLocation | core：空间选择为通用基础能力 | ArcPy GP（官方实现） |

### Package toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Consolidate Layer | 将一个或多个图层引用的数据源复制整合到单个文件夹 | arcpy.management.ConsolidateLayer | extension：ArcGIS 工程/图层打包体系专属 | ArcPy GP（官方实现） |
| Consolidate Locator | 将定位器/复合定位器复制整合到单个文件夹 | arcpy.management.ConsolidateLocator | extension：同上 | ArcPy GP（官方实现） |
| Consolidate Map | 将地图及全部引用数据源整合到指定文件夹 | arcpy.management.ConsolidateMap | extension：同上 | ArcPy GP（官方实现） |
| Consolidate Project | 将工程（.aprx）及引用地图与数据整合到指定文件夹 | arcpy.management.ConsolidateProject | extension：同上 | ArcPy GP（官方实现） |
| Consolidate Toolbox | 将一个或多个工具箱整合到指定文件夹 | arcpy.management.ConsolidateToolbox | extension：同上 | ArcPy GP（官方实现） |
| Create Map Tile Package | 由地图生成切片并打包为一个或多个切片包 | arcpy.management.CreateMapTilePackage | extension：ArcGIS 切片包格式专属（概念通用、格式专属） | ArcPy GP（官方实现） |
| Create Mobile Map Package | 将地图、底图及引用数据打包为单个 .mmpk 文件 | arcpy.management.CreateMobileMapPackage | extension：同上 | ArcPy GP（官方实现） |
| Create Mobile Scene Package | 由一个或多个场景创建移动场景包（.mspk） | arcpy.management.CreateMobileScenePackage | extension：同上 | ArcPy GP（官方实现） |
| Create Vector Tile Index | 创建多尺度多边形网格用作矢量切片包的索引面 | arcpy.management.CreateVectorTileIndex | core：矢量切片索引为通用瓦片能力 | ArcPy GP（官方实现） |
| Create Vector Tile Package | 由地图/底图生成矢量切片并打包为 .vtpk 文件 | arcpy.management.CreateVectorTilePackage | extension：.vtpk 为 ArcGIS 格式 | ArcPy GP（官方实现） |
| Extract Package | 将包内容解压到指定文件夹 | arcpy.management.ExtractPackage | extension：ArcGIS 包格式专属 | ArcPy GP（官方实现） |
| Package Layer | 将图层及引用数据打包为单个压缩 .lpkx 文件 | arcpy.management.PackageLayer | extension：同上 | ArcPy GP（官方实现） |
| Package Locator | 将定位器打包为单个压缩 .gcpk 文件 | arcpy.management.PackageLocator | extension：同上 | ArcPy GP（官方实现） |
| Package Map | 将地图及引用数据打包为单个压缩 .mpkx 文件 | arcpy.management.PackageMap | extension：同上 | ArcPy GP（官方实现） |
| Package Project | 将工程及引用地图与数据打包为 .ppkx 文件 | arcpy.management.PackageProject | extension：同上 | ArcPy GP（官方实现） |
| Package Result | 将地理处理结果（含工具与输入输出数据集）打包为 .gpkx 文件 | arcpy.management.PackageResult | extension：同上 | ArcPy GP（官方实现） |
| Share Package | 将包上传分享到 ArcGIS Online 或 Enterprise | arcpy.management.SharePackage | extension：依赖 ArcGIS 门户体系 | ArcPy GP（官方实现） |

### Scene Layers toolset（Package 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create 3D Object Scene Layer Content | 由多面体/3D 对象图层创建场景图层包（.slpk）或 I3S 内容 | arcpy.management.Create3DObjectSceneLayerContent | extension：I3S 场景图层为 ArcGIS 平台专属 | ArcPy GP（官方实现） |
| Create Building Scene Layer Content | 由建筑图层创建场景图层包或 I3S 内容 | arcpy.management.CreateBuildingSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Integrated Mesh Scene Layer Content | 由 OSGB 数据创建集成网格场景图层内容 | arcpy.management.CreateIntegratedMeshSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Point Cloud Scene Layer Content | 由 LAS/zLAS/LAZ 创建点云场景图层包或云端 I3S 内容 | arcpy.management.CreatePointCloudSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Point Scene Layer Content | 由点要素图层创建点场景图层包或 I3S 内容 | arcpy.management.CreatePointSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Voxel Scene Layer Content | 由体素图层创建场景图层包 | arcpy.management.CreateVoxelSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Upgrade Scene Layer | 将场景图层包升级到当前 I3S 版本（SLPK 或 i3sREST） | arcpy.management.UpgradeSceneLayer | extension：同上 | ArcPy GP（官方实现） |
| Validate Scene Layer | 在云存储中评估场景图层包是否符合 I3S 规范 | arcpy.management.ValidateSceneLayer | extension：同上 | ArcPy GP（官方实现） |

### Photos toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| GeoTagged Photos To Points | 由地理标记照片元数据中的 XYZ 坐标创建点（可加为附件） | arcpy.management.GeoTaggedPhotosToPoints | core：照片定位建点为通用能力 | ArcPy GP（官方实现） |
| Match Photos To Rows By Time | 按时间戳将照片文件匹配到表/要素类行并可加为附件 | arcpy.management.MatchPhotosToRowsByTime | core：按时间匹配为通用能力 | ArcPy GP（官方实现） |

### Projections and Transformations toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Batch Project | 将一组要素类/要素数据集批量投影到统一坐标系 | arcpy.management.BatchProject | core：批量投影为通用基础能力 | ArcPy GP（官方实现） |
| Convert Coordinate Notation | 将一/两个字段中的坐标表示格式互转 | arcpy.management.ConvertCoordinateNotation | core：坐标表示转换为通用能力 | ArcPy GP（官方实现） |
| Create Custom Geographic Transformation | 创建两个地理坐标系/基准面之间的自定义地理变换方法 | arcpy.management.CreateCustomGeographicTransformation | core：基准变换为通用能力 | ArcPy GP（官方实现） |
| Create Spatial Reference | 创建供 ModelBuilder 使用的空间参考 | arcpy.management.CreateSpatialReference | core：空间参考定义为通用能力 | ArcPy GP（官方实现） |
| Define Projection | 覆写数据集存储的坐标系信息（用于未知/错误坐标系） | arcpy.management.DefineProjection | core：定义投影为通用基础能力 | ArcPy GP（官方实现） |
| Project | 将空间数据从一个坐标系投影到另一个坐标系 | arcpy.management.Project | core：投影为通用基础能力，适合统一动词候选 | ArcPy GP（官方实现） |

### Projections and Transformations — Raster 子集 toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Flip | 沿中心水平轴上下翻转栅格 | arcpy.management.Flip | core：栅格翻转为通用能力 | ArcPy GP（官方实现） |
| Mirror | 沿中心垂直轴左右镜像栅格 | arcpy.management.Mirror | core：栅格镜像为通用能力 | ArcPy GP（官方实现） |
| Project Raster | 将栅格数据集从一个坐标系转换到另一个坐标系 | arcpy.management.ProjectRaster | core：栅格投影为通用基础能力 | ArcPy GP（官方实现） |
| Register Raster | 将栅格自动配准到参考影像或用控制点文件做地理配准（镶嵌数据集逐项处理） | arcpy.management.RegisterRaster | core：影像配准为通用能力 | ArcPy GP（官方实现） |
| Rescale | 按 X/Y 缩放因子调整栅格大小 | arcpy.management.Rescale | core：栅格缩放为通用能力 | ArcPy GP（官方实现） |
| Rotate | 绕指定枢轴点旋转栅格数据集 | arcpy.management.Rotate | core：栅格旋转为通用能力 | ArcPy GP（官方实现） |
| Shift | 按 X/Y 偏移量将栅格平移到新地理位置 | arcpy.management.Shift | core：栅格平移为通用能力 | ArcPy GP（官方实现） |
| Warp | 用源/目标控制点变换栅格数据集（类似地理配准） | arcpy.management.Warp | core：栅格纠正为通用能力 | ArcPy GP（官方实现） |
| Warp From File | 用含源/目标控制点的文本文件变换栅格数据集 | arcpy.management.WarpFromFile | core：同上 | ArcPy GP（官方实现） |

### Raster toolset

Raster 为伞形工具集，无直属工具，其全部 80 个工具分布在以下 5 个子集中：Mosaic Dataset（32）、Ortho Mapping（15）、Raster Dataset（8）、Raster Processing（11）、Raster Properties（14）。

### Raster — Mosaic Dataset toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Rasters To Mosaic Dataset | 从文件、文件夹、表或 Web 服务向镶嵌数据集添加栅格数据集 | arcpy.management.AddRastersToMosaicDataset | extension：镶嵌数据集为 ArcGIS 专属高级影像管理结构 | ArcPy GP（官方实现） |
| Alter Mosaic Dataset Schema | 定义非所有者在企业级地理数据库中编辑镶嵌数据集的操作权限 | arcpy.management.AlterMosaicDatasetSchema | extension：同上 | ArcPy GP（官方实现） |
| Analyze Mosaic Dataset | 检查镶嵌数据集的错误与可改进项 | arcpy.management.AnalyzeMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Build Boundary | 在新增栅格超出原覆盖时更新镶嵌数据集边界范围 | arcpy.management.BuildBoundary | extension：同上 | ArcPy GP（官方实现） |
| Build Footprints | 计算镶嵌数据集中每个栅格的足迹范围 | arcpy.management.BuildFootprints | extension：同上 | ArcPy GP（官方实现） |
| Build Mosaic Dataset Item Cache | 在镶嵌数据集所有函数链末步插入缓存栅格函数 | arcpy.management.BuildMosaicDatasetItemCache | extension：同上 | ArcPy GP（官方实现） |
| Build Overviews | 在镶嵌数据集上定义并生成概视图（金字塔） | arcpy.management.BuildOverviews | extension：同上 | ArcPy GP（官方实现） |
| Build Seamlines | 生成/更新镶嵌数据集的镶嵌线以平滑重叠影像排序 | arcpy.management.BuildSeamlines | extension：同上 | ArcPy GP（官方实现） |
| Calculate Cell Size Ranges | 按空间分辨率计算镶嵌数据集中栅格的可见级别 | arcpy.management.CalculateCellSizeRanges | extension：同上 | ArcPy GP（官方实现） |
| Clear Pixel Cache | 清除与镶嵌数据集关联的像素缓存 | arcpy.management.ClearPixelCache | extension：同上 | ArcPy GP（官方实现） |
| Color Balance Mosaic Dataset | 使相邻影像间过渡无缝的颜色平衡处理 | arcpy.management.ColorBalanceMosaicDataset | extension：同上（色彩平衡概念通用、实现依托镶嵌数据集） | ArcPy GP（官方实现） |
| Compute Dirty Area | 识别镶嵌数据集自某时刻以来发生变化的区域 | arcpy.management.ComputeDirtyArea | extension：同上 | ArcPy GP（官方实现） |
| Compute Mosaic Candidates | 找出最能代表镶嵌区域的影像候选 | arcpy.management.ComputeMosaicCandidates | extension：同上 | ArcPy GP（官方实现） |
| Create Mosaic Dataset | 在地理数据库中创建空镶嵌数据集 | arcpy.management.CreateMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Create Referenced Mosaic Dataset | 从已有镶嵌数据集的条目创建独立的引用镶嵌数据集 | arcpy.management.CreateReferencedMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Define Mosaic Dataset NoData | 指定一个或多个值表示为 NoData | arcpy.management.DefineMosaicDatasetNoData | extension：同上 | ArcPy GP（官方实现） |
| Define Overviews | 设置镶嵌数据集概视图的生成方式（供 Build Overviews 使用） | arcpy.management.DefineOverviews | extension：同上 | ArcPy GP（官方实现） |
| Delete Mosaic Dataset | 删除镶嵌数据集及其概视图与条目缓存 | arcpy.management.DeleteMosaicDataset | defer：破坏性删除镶嵌数据集，需确认（且属 ArcGIS 专属结构） | ArcPy GP（官方实现） |
| Edit Raster Function | 在镶嵌数据集或含栅格函数的图层中添加、替换或移除函数链 | arcpy.management.EditRasterFunction | extension：栅格函数链为 ArcGIS 影像处理专属机制 | ArcPy GP（官方实现） |
| Export Mosaic Dataset Geometry | 创建显示镶嵌数据集足迹、边界、镶嵌线或分辨率的要素类 | arcpy.management.ExportMosaicDatasetGeometry | extension：同上 | ArcPy GP（官方实现） |
| Export Mosaic Dataset Items | 将镶嵌数据集中处理后的影像另存到指定文件夹与格式 | arcpy.management.ExportMosaicDatasetItems | extension：同上 | ArcPy GP（官方实现） |
| Export Mosaic Dataset Paths | 创建镶嵌数据集每条目文件路径的表（可只列损坏路径） | arcpy.management.ExportMosaicDatasetPaths | extension：同上 | ArcPy GP（官方实现） |
| Generate Exclude Area | 按颜色或值域裁剪掩膜像素，供颜色平衡时排除云、水等干扰区 | arcpy.management.GenerateExcludeArea | extension：同上 | ArcPy GP（官方实现） |
| Generate Raster Collection | 对镶嵌数据集中的影像集合逐个或分组批量分析处理 | arcpy.management.GenerateRasterCollection | extension：同上 | ArcPy GP（官方实现） |
| Import Mosaic Dataset Geometry | 按要素类修改镶嵌数据集的足迹、边界或镶嵌线几何 | arcpy.management.ImportMosaicDatasetGeometry | extension：同上 | ArcPy GP（官方实现） |
| Merge Mosaic Dataset Items | 将镶嵌数据集中多个条目合并为一个条目 | arcpy.management.MergeMosaicDatasetItems | extension：同上 | ArcPy GP（官方实现） |
| Mosaic Dataset To Mobile Mosaic Dataset | 将镶嵌数据集转换为兼容 Runtime 的移动镶嵌数据集 | arcpy.management.MosaicDatasetToMobileMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Remove Rasters From Mosaic Dataset | 从镶嵌数据集移除选中的栅格 | arcpy.management.RemoveRastersFromMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Repair Mosaic Dataset Paths | 在移动/复制镶嵌数据集后重置源影像路径 | arcpy.management.RepairMosaicDatasetPaths | extension：同上 | ArcPy GP（官方实现） |
| Set Mosaic Dataset Properties | 定义镶嵌数据集显示与发布为影像服务的默认值 | arcpy.management.SetMosaicDatasetProperties | extension：同上 | ArcPy GP（官方实现） |
| Split Mosaic Dataset Items | 拆分先前合并的镶嵌数据集条目 | arcpy.management.SplitMosaicDatasetItems | extension：同上 | ArcPy GP（官方实现） |
| Synchronize Mosaic Dataset | 同步镶嵌数据集保持最新（可更新概视图、缓存、恢复配置、移除路径） | arcpy.management.SynchronizeMosaicDataset | extension：同上 | ArcPy GP（官方实现） |

### Raster — Ortho Mapping toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze Control Points | 分析控制点覆盖并指出需补充控制点以改善区域网平差的区域 | arcpy.management.AnalyzeControlPoints | core：正射校正控制点分析为遥感通用能力 | ArcPy GP（官方实现） |
| Append Control Points | 将控制点合并到已有控制点表 | arcpy.management.AppendControlPoints | core：同上 | ArcPy GP（官方实现） |
| Apply Block Adjustment | 用解算表将地理调整应用到镶嵌数据集条目 | arcpy.management.ApplyBlockAdjustment | core：区域网平差应用为摄影测量通用能力（此处依托镶嵌数据集） | ArcPy GP（官方实现） |
| Build Stereo Model | 基于用户提供的立体像对构建镶嵌数据集立体模型 | arcpy.management.BuildStereoModel | core：立体模型为摄影测量通用能力 | ArcPy GP（官方实现） |
| Compute Block Adjustment | 计算镶嵌数据集的调整量并生成解算表 | arcpy.management.ComputeBlockAdjustment | core：区域网平差为通用能力 | ArcPy GP（官方实现） |
| Compute Camera Model | 由原始影像 EXIF 估计并精化内外方位相机模型，可用 DSM 改善正射 | arcpy.management.ComputeCameraModel | core：相机模型估计为通用能力 | ArcPy GP（官方实现） |
| Compute Control Points | 在镶嵌数据集与参考影像之间创建控制点 | arcpy.management.ComputeControlPoints | core：控制点计算为通用能力 | ArcPy GP（官方实现） |
| Compute Fiducials | 计算镶嵌数据集每幅影像在影像/胶片空间的框标坐标 | arcpy.management.ComputeFiducials | core：框标计算为摄影测量通用能力 | ArcPy GP（官方实现） |
| Compute Tie Points | 计算重叠镶嵌条目之间的连接点 | arcpy.management.ComputeTiePoints | core：连接点计算为通用能力 | ArcPy GP（官方实现） |
| Export Frame and Camera Parameters | 从含框幅影像的镶嵌数据集导出帧与相机参数 | arcpy.management.ExportFrameAndCameraParameters | core：参数导出为通用能力 | ArcPy GP（官方实现） |
| Generate Block Adjustment Report | 生成正射区域网平差报告以评估产品质量与精度 | arcpy.management.GenerateBlockAdjustmentReport | core：平差报告为通用能力 | ArcPy GP（官方实现） |
| Generate Point Cloud | 由立体像对计算 3D 点并输出为 LAS 点云集 | arcpy.management.GeneratePointCloud | core：密集点云生成为通用能力 | ArcPy GP（官方实现） |
| Interpolate From Point Cloud | 由点云内插生成 DTM 或 DSM | arcpy.management.InterpolateFromPointCloud | core：点云内插地形为通用能力 | ArcPy GP（官方实现） |
| Match Control Points | 为给定地面控制点在重叠影像中创建匹配连接点 | arcpy.management.MatchControlPoints | core：控制点匹配为通用能力 | ArcPy GP（官方实现） |
| Update Interior Orientation | 用框标表构建仿射变换精化每幅影像的内定向 | arcpy.management.UpdateInteriorOrientation | core：内定向为摄影测量通用能力 | ArcPy GP（官方实现） |

### Raster — Raster Dataset toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Copy Raster | 保存栅格数据集副本或将镶嵌数据集转为单个栅格数据集 | arcpy.management.CopyRaster | core：栅格复制/转为通用能力 | ArcPy GP（官方实现） |
| Create Random Raster | 按指定分布创建随机值栅格数据集 | arcpy.management.CreateRandomRaster | core：随机栅格为通用能力 | ArcPy GP（官方实现） |
| Create Raster Dataset | 创建空栅格数据集 | arcpy.management.CreateRasterDataset | core：建栅格为通用基础能力 | ArcPy GP（官方实现） |
| Download Rasters | 从影像服务或镶嵌数据集下载源文件 | arcpy.management.DownloadRasters | core：下载栅格为通用能力 | ArcPy GP（官方实现） |
| Generate Raster From Raster Function | 由输入栅格函数/函数链生成栅格数据集 | arcpy.management.GenerateRasterFromRasterFunction | extension：栅格函数链为 ArcGIS 专属机制 | ArcPy GP（官方实现） |
| Mosaic | 将多个已有栅格/镶嵌数据集镶嵌到已有栅格数据集 | arcpy.management.Mosaic | core：栅格镶嵌为通用基础能力 | ArcPy GP（官方实现） |
| Mosaic To New Raster | 将多个栅格数据集镶嵌为新栅格数据集 | arcpy.management.MosaicToNewRaster | core：同上 | ArcPy GP（官方实现） |
| Workspace To Raster Dataset | 将文件夹中全部栅格数据集镶嵌为一个栅格数据集 | arcpy.management.WorkspaceToRasterDataset | core：同上 | ArcPy GP（官方实现） |

### Raster — Raster Processing toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Clip Raster | 裁剪栅格数据集、镶嵌数据集或影像服务图层的一部分 | arcpy.management.ClipRaster | core：栅格裁剪为通用基础能力 | ArcPy GP（官方实现） |
| Composite Bands | 由多个波段创建单个栅格数据集 | arcpy.management.CompositeBands | core：波段合成为通用能力 | ArcPy GP（官方实现） |
| Compute Pansharpen Weights | 为新/自定义传感器计算最优全色锐化权重 | arcpy.management.ComputePansharpenWeights | core：全色锐化为遥感通用能力 | ArcPy GP（官方实现） |
| Create Color Composite | 由多波段栅格创建三波段彩色合成栅格 | arcpy.management.CreateColorComposite | core：彩色合成为通用能力 | ArcPy GP（官方实现） |
| Create Ortho Corrected Raster Dataset | 用高程与 RPC 对卫星数据做正射校正生成栅格 | arcpy.management.CreateOrthoCorrectedRasterDataset | core：正射校正为遥感通用能力 | ArcPy GP（官方实现） |
| Create Pansharpened Raster Dataset | 融合高分辨率全色与低分辨率多波段生成高分辨率多波段栅格 | arcpy.management.CreatePansharpenedRasterDataset | core：全色锐化融合为通用能力 | ArcPy GP（官方实现） |
| Extract Subdataset | 从 HDF 或 NITF 数据集中提取子数据集生成新栅格 | arcpy.management.ExtractSubdataset | core：子数据集提取为通用能力 | ArcPy GP（官方实现） |
| Generate Table From Raster Function | 将栅格函数数据集转换为表或要素类 | arcpy.management.GenerateTableFromRasterFunction | extension：栅格函数为 ArcGIS 专属机制 | ArcPy GP（官方实现） |
| Raster To DTED | 按 DTED 切分结构将栅格拆为独立文件 | arcpy.management.RasterToDTED | core：DTED 为开放军用高程格式，通用能力 | ArcPy GP（官方实现） |
| Resample | 改变栅格空间分辨率并按规则聚合/内插像元值 | arcpy.management.Resample | core：重采样为通用基础能力 | ArcPy GP（官方实现） |
| Split Raster | 按瓦片或面要素将栅格数据集切分为小块 | arcpy.management.SplitRaster | core：栅格切分为通用能力 | ArcPy GP（官方实现） |

### Raster — Raster Properties toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Colormap | 向栅格数据集添加新颜色映射表或替换已有颜色映射表 | arcpy.management.AddColormap | core：颜色映射为通用栅格属性 | ArcPy GP（官方实现） |
| Batch Build Pyramids | 为多个栅格数据集批量建金字塔 | arcpy.management.BatchBuildPyramids | core：金字塔为通用栅格能力 | ArcPy GP（官方实现） |
| Batch Calculate Statistics | 为多个栅格数据集批量计算统计 | arcpy.management.BatchCalculateStatistics | core：栅格统计为通用能力 | ArcPy GP（官方实现） |
| Build Pyramids | 为栅格数据集建金字塔 | arcpy.management.BuildPyramids | core：同上 | ArcPy GP（官方实现） |
| Build Pyramids And Statistics | 遍历文件夹为全部栅格建金字塔并计算统计（亦可处理镶嵌条目） | arcpy.management.BuildPyramidsAndStatistics | core：同上 | ArcPy GP（官方实现） |
| Build Raster Attribute Table | 为栅格数据集添加/更新栅格属性表（主要用于离散数据） | arcpy.management.BuildRasterAttributeTable | core：栅格属性表为通用能力 | ArcPy GP（官方实现） |
| Calculate Statistics | 计算栅格或镶嵌数据集的统计 | arcpy.management.CalculateStatistics | core：同上 | ArcPy GP（官方实现） |
| Convert Raster Function Template | 在 rft.xml、json、二进制之间转换栅格函数模板格式 | arcpy.management.ConvertRasterFunctionTemplate | extension：栅格函数模板为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Delete Colormap | 移除栅格数据集关联的颜色映射表 | arcpy.management.DeleteColormap | core：颜色映射管理为通用能力 | ArcPy GP（官方实现） |
| Delete Raster Attribute Table | 移除栅格数据集关联的栅格属性表 | arcpy.management.DeleteRasterAttributeTable | core：同上 | ArcPy GP（官方实现） |
| Export Raster World File | 按像元大小与左上角位置创建世界文件 | arcpy.management.ExportRasterWorldFile | core：世界文件为通用格式 | ArcPy GP（官方实现） |
| Get Cell Value | 按 XY 坐标获取指定像元值 | arcpy.management.GetCellValue | core：像元查询为通用能力 | ArcPy GP（官方实现） |
| Get Raster Properties | 获取栅格数据集的元数据与描述统计信息 | arcpy.management.GetRasterProperties | core：栅格属性读取为通用能力 | ArcPy GP（官方实现） |
| Set Raster Properties | 设置栅格/镶嵌数据集的数据类型、统计与 NoData 值 | arcpy.management.SetRasterProperties | core：同上 | ArcPy GP（官方实现） |

### Relationship Classes toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Rule To Relationship Class | 向关系类添加一条规则 | arcpy.management.AddRuleToRelationshipClass | extension：地理数据库关系类为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Create Relationship Class | 创建存储源表与目标表字段/要素关联的关系类 | arcpy.management.CreateRelationshipClass | extension：同上（关系概念通用、实现专属） | ArcPy GP（官方实现） |
| Migrate Relationship Class | 将基于 ObjectID 的关系类迁移为基于 GlobalID 的关系类 | arcpy.management.MigrateRelationshipClass | extension：同上 | ArcPy GP（官方实现） |
| Remove Rule From Relationship Class | 从关系类移除一条规则 | arcpy.management.RemoveRuleFromRelationshipClass | extension：同上 | ArcPy GP（官方实现） |
| Set Relationship Class Split Policy | 定义关联要素的分割策略 | arcpy.management.SetRelationshipClassSplitPolicy | extension：同上 | ArcPy GP（官方实现） |
| Table To Relationship Class | 由源、目标与关系表创建带属性的关系类 | arcpy.management.TableToRelationshipClass | extension：同上 | ArcPy GP（官方实现） |

### Sampling toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Fishnet | 创建矩形格网（渔网），输出折线或面要素 | arcpy.management.CreateFishnet | core：格网生成为通用能力 | ArcPy GP（官方实现） |
| Create Random Points | 创建指定数量的随机点（可在范围、面内、点上或线沿线生成） | arcpy.management.CreateRandomPoints | core：随机采样为通用能力 | ArcPy GP（官方实现） |
| Generate Points Along Lines | 沿线/面边界按固定间隔或长度百分比生成点 | arcpy.management.GeneratePointsAlongLines | core：沿线布点为通用能力 | ArcPy GP（官方实现） |
| Generate Rectangles Along Lines | 沿单个或一组线要素生成系列矩形面 | arcpy.management.GenerateRectanglesAlongLines | core：沿线矩形为通用能力 | ArcPy GP（官方实现） |
| Generate Tessellation | 生成覆盖给定范围的规则多边形镶嵌网格（三角/方/菱/六边形/H3 等） | arcpy.management.GenerateTessellation | core：镶嵌网格为通用能力 | ArcPy GP（官方实现） |
| Generate Transects Along Lines | 沿线按固定间隔生成垂直样线（横断面） | arcpy.management.GenerateTransectsAlongLines | core：样线生成为通用能力 | ArcPy GP（官方实现） |

### Subtypes toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Subtype | 向输入表的子类型集合添加新子类型 | arcpy.management.AddSubtype | extension：子类型为地理数据库专属分组机制 | ArcPy GP（官方实现） |
| Remove Subtype | 按代码从输入表移除子类型 | arcpy.management.RemoveSubtype | extension：同上 | ArcPy GP（官方实现） |
| Set Default Subtype | 设置输入表子类型的默认值/代码 | arcpy.management.SetDefaultSubtype | extension：同上 | ArcPy GP（官方实现） |
| Set Subtype Field | 定义输入表/要素类中存储子类型代码的字段 | arcpy.management.SetSubtypeField | extension：同上 | ArcPy GP（官方实现） |

### Table toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze | 更新业务表、要素表、增量表及其索引的数据库统计 | arcpy.management.Analyze | core：表统计更新为通用数据库能力 | ArcPy GP（官方实现） |
| Copy Rows | 将表的行复制到另一表 | arcpy.management.CopyRows | core：行复制为通用能力 | ArcPy GP（官方实现） |
| Create Table | 创建地理数据库表或 dBASE 表 | arcpy.management.CreateTable | core：建表为通用基础能力 | ArcPy GP（官方实现） |
| Create Unregistered Table | 在数据库/企业级地理数据库中创建未注册的空表 | arcpy.management.CreateUnregisteredTable | extension：企业级地理数据库注册机制专属 | ArcPy GP（官方实现） |
| Delete Rows | 删除输入中全部或选中的行子集 | arcpy.management.DeleteRows | defer：破坏性批量删行，需确认 | ArcPy GP（官方实现） |
| Get Count | 返回表的总行数 | arcpy.management.GetCount | core：计数为通用能力 | ArcPy GP（官方实现） |
| Pivot Table | 对输入表透视以减少记录冗余、扁平化一对多关系 | arcpy.management.PivotTable | core：透视表为通用能力 | ArcPy GP（官方实现） |
| Truncate Table | 用数据库截断方式移除表/要素类的全部行 | arcpy.management.TruncateTable | defer：破坏性清空，需确认 | ArcPy GP（官方实现） |

### Tile Cache toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Export Tile Cache | 将已有切片缓存的切片导出为新缓存或切片包 | arcpy.management.ExportTileCache | core：切片缓存导出为通用瓦片能力（格式含 ArcGIS 包） | ArcPy GP（官方实现） |
| Generate Tile Cache Tiling Scheme | 生成定义切片缓存级别、尺寸等属性的 XML 切片方案文件 | arcpy.management.GenerateTileCacheTilingScheme | core：切片方案为通用瓦片能力 | ArcPy GP（官方实现） |
| Import Tile Cache | 将一个切片缓存的切片导入另一缓存 | arcpy.management.ImportTileCache | core：同上 | ArcPy GP（官方实现） |
| Manage Tile Cache | 在已有切片缓存中创建与更新切片 | arcpy.management.ManageTileCache | core：同上 | ArcPy GP（官方实现） |

### Toolbox toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze Toolbox For Version | 分析工具箱内容并识别与旧版 ArcGIS 的兼容问题 | arcpy.management.AnalyzeToolboxForVersion | extension：ArcGIS 工具箱版本兼容专属 | ArcPy GP（官方实现） |
| Analyze Tools For Pro | 分析 Python 脚本与自定义工具/工具箱中 ArcGIS Pro 不支持的功能 | arcpy.management.AnalyzeToolsForPro | extension：同上 | ArcPy GP（官方实现） |
| Save Toolbox To Version | 分析并将工具箱保存为指定 ArcGIS 版本可用 | arcpy.management.SaveToolboxToVersion | extension：同上 | ArcPy GP（官方实现） |

### Topology toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Feature Class To Topology | 向拓扑添加要素类 | arcpy.management.AddFeatureClassToTopology | extension：地理数据库拓扑为 ArcGIS 专属实现（拓扑概念通用） | ArcPy GP（官方实现） |
| Add Rule To Topology | 向拓扑添加规则 | arcpy.management.AddRuleToTopology | extension：同上 | ArcPy GP（官方实现） |
| Create Topology | 创建不含要素类与规则的空拓扑 | arcpy.management.CreateTopology | extension：同上 | ArcPy GP（官方实现） |
| Export Topology Errors | 将拓扑错误与例外导出到目标地理数据库供任意许可级别使用 | arcpy.management.ExportTopologyErrors | extension：同上 | ArcPy GP（官方实现） |
| Remove Feature Class From Topology | 从拓扑移除要素类 | arcpy.management.RemoveFeatureClassFromTopology | extension：同上 | ArcPy GP（官方实现） |
| Remove Rule From Topology | 从拓扑移除规则 | arcpy.management.RemoveRuleFromTopology | extension：同上 | ArcPy GP（官方实现） |
| Set Cluster Tolerance | 设置拓扑的簇容差 | arcpy.management.SetClusterTolerance | extension：同上 | ArcPy GP（官方实现） |
| Validate Topology | 验证地理数据库拓扑 | arcpy.management.ValidateTopology | extension：同上 | ArcPy GP（官方实现） |

### Trajectory Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Data To Trajectory Dataset | 向已有轨迹数据集添加轨迹数据 | arcpy.management.AddDataToTrajectoryDataset | extension：轨迹数据集（卫星测高）为 ArcGIS 专属数据类型 | ArcPy GP（官方实现） |
| Create Trajectory Dataset | 在地理数据库中创建空轨迹数据集 | arcpy.management.CreateTrajectoryDataset | extension：同上 | ArcPy GP（官方实现） |
| Repair Trajectory Dataset Paths | 修复轨迹数据集的源数据路径 | arcpy.management.RepairTrajectoryDatasetPaths | extension：同上 | ArcPy GP（官方实现） |

### Versions toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Field Conflict Filter | 为地理数据库表/要素类的指定字段添加字段冲突过滤器 | arcpy.management.AddFieldConflictFilter | extension：企业级地理数据库版本为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Alter Version | 修改地理数据库版本属性 | arcpy.management.AlterVersion | extension：同上 | ArcPy GP（官方实现） |
| Change Version | 修改图层/表视图的工作空间以连接指定版本 | arcpy.management.ChangeVersion | extension：同上 | ArcPy GP（官方实现） |
| Create Version | 在指定地理数据库中创建新版本 | arcpy.management.CreateVersion | extension：同上 | ArcPy GP（官方实现） |
| Delete Version | 从企业/工作组/桌面地理数据库删除指定版本 | arcpy.management.DeleteVersion | extension：同上 | ArcPy GP（官方实现） |
| Reconcile Versions | 将一个或多个版本与目标版本协调（reconcile） | arcpy.management.ReconcileVersions | extension：同上 | ArcPy GP（官方实现） |
| Register As Versioned | 将企业级地理数据库数据集注册为版本化 | arcpy.management.RegisterAsVersioned | extension：同上 | ArcPy GP（官方实现） |
| Remove Field Conflict Filter | 移除指定字段的字段冲突过滤器 | arcpy.management.RemoveFieldConflictFilter | extension：同上 | ArcPy GP（官方实现） |
| Unregister As Versioned | 取消企业级地理数据库数据集的版本化注册 | arcpy.management.UnregisterAsVersioned | extension：同上 | ArcPy GP（官方实现） |

### Workspace toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Clear Workspace Cache | 清除企业级地理数据库工作空间缓存 | arcpy.management.ClearWorkspaceCache | extension：企业级地理数据库缓存专属 | ArcPy GP（官方实现） |
| Create Cloud Storage Connection File | 创建 ArcGIS 支持的云存储连接文件以读写云栅格等数据 | arcpy.management.CreateCloudStorageConnectionFile | core：云存储连接为通用能力 | ArcPy GP（官方实现） |
| Create Database Connection | 创建 ArcGIS 连接数据库/企业级地理数据库的连接文件 | arcpy.management.CreateDatabaseConnection | core：数据库连接为通用能力 | ArcPy GP（官方实现） |
| Create Database Connection String | 创建地理处理工具连接数据库/企业级地理数据库的连接字符串 | arcpy.management.CreateDatabaseConnectionString | core：同上 | ArcPy GP（官方实现） |
| Create Feature Dataset | 在企业/文件/移动地理数据库中创建要素数据集 | arcpy.management.CreateFeatureDataset | extension：要素数据集为地理数据库专属容器 | ArcPy GP（官方实现） |
| Create File Geodatabase | 在文件夹中创建文件地理数据库 | arcpy.management.CreateFileGeodatabase | extension：文件地理数据库为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Create Folder | 在指定位置创建文件夹 | arcpy.management.CreateFolder | core：建文件夹为通用能力 | ArcPy GP（官方实现） |
| Create Mobile Geodatabase | 创建移动地理数据库 | arcpy.management.CreateMobileGeodatabase | extension：移动地理数据库为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Create Spatial Type | 向 Oracle/PostgreSQL 数据库添加 ST_Geometry 类型、子类型与函数（或升级） | arcpy.management.CreateSpatialType | core：ST_Geometry 为开放空间类型概念 | ArcPy GP（官方实现） |
| Create SQLite Database | 创建含 ST_Geometry 或 SpatiaLite 空间类型的 GeoPackage/SQLite 数据库 | arcpy.management.CreateSQLiteDatabase | core：GeoPackage/SQLite 为开放格式 | ArcPy GP（官方实现） |
| Export XML Workspace Document | 创建地理数据库内容的可读 XML 文档 | arcpy.management.ExportXMLWorkspaceDocument | extension：地理数据库 XML 工作空间为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Import XML Workspace Document | 将 XML 工作空间文档内容导入已有地理数据库 | arcpy.management.ImportXMLWorkspaceDocument | extension：同上 | ArcPy GP（官方实现） |
| Refresh Excel | 在 ArcGIS Pro 中刷新 Microsoft Excel 文件 | arcpy.management.RefreshExcel | defer：依赖桌面 Excel 交互刷新 | ArcPy GP（官方实现） |
| Update Geodatabase Connection Properties To Branch | 更新企业级地理数据库连接以支持分支版本 | arcpy.management.UpdateGeodatabaseConnectionPropertiesToBranch | extension：分支版本为 ArcGIS 专属 | ArcPy GP（官方实现） |


> 「GIS 综合平台能力底账」分节文件。证据口径：一级证据仅用 Esri 官方文档（pro.arcgis.com / developers.arcgis.com），以 ArcGIS Pro 3.4 工具参考为锚：Spatial Analyst 以 3.4《A complete listing of the Spatial Analyst tools》工具/工具集清单为准，逐 toolset 总览页核对作用；3D Analyst 以 3.4 工具箱许可页（逐 toolset 列全工具）+ 工具箱总览为准，去重跨 toolset 重复列名；Geostatistical Analyst 以 5 个 toolset 总览页（Tool | Description 表）为准，并纳入 3.4 新增的 Directional Trend（官方 3.4 工具页核实，arcpy.ga.DirectionalTrend）；Image Analyst 以工具箱许可页清单 + Interpolation / Utilities 等 toolset 总览页为准（不含 3.4 之后版本在最新完整清单中新增的 Spectral Analysis、扩展 SAR/InSAR 与新深度学习工具，见文末口径说明）。
>
> 平台升级原则（鱼鱼定版）：**全部升级＋不重复造轮子**——平台层只做翻译与治理、不自研算法。「轮子来源」列写明每条工具的官方现成复用通道：绝大多数地理处理工具的官方实现即 ArcPy GP 本身，桥直调即可；可发布为 ArcGIS Enterprise 的 REST 地理处理服务、或由 ArcGIS Online 托管分析工具/托管服务提供等价能力者，在该行注明；仅桌面交互、无独立脚本入口者在该行单独标出。
>
> 平台判断口径：core＝通用栅格/地形分析、多家共有（如坡度坡向、重分类、栅格计算、常用插值、TIN/LAS 基础处理）；extension＝ArcGIS 专属实现或许可绑定（如专属数据结构/文件格式、专属算法实现）；defer＝向导式建模、需交互标定或深度学习训练/推理管线，单独注记、暂缓直调。

## Spatial Analyst toolbox（arcpy.sa）

工具集数：25 组（见文末口径）；工具总数：221；所需扩展许可：Spatial Analyst license；官方定位：为栅格（像元）与要素数据提供丰富的空间分析与建模工具（地图代数、水文、地形、插值、适宜性叠加等）。

### Conditional toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Con | 按条件逐像元做 if/else 取值 | arcpy.sa.Con | core — 通用栅格条件运算，多家共有 | ArcPy GP（官方实现，桥直调） |
| Pick | 按位置栅格从多个输入栅格中逐像元挑选取值 | arcpy.sa.Pick | core — 通用栅格条件运算 | ArcPy GP（官方实现，桥直调） |
| Set Null | 满足条件的位置设为 NoData、其余保留指定值 | arcpy.sa.SetNull | core — 通用 NoData 处理 | ArcPy GP（官方实现，桥直调） |

### Density toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Kernel Density Ratio | 计算两个核密度面的比率（相对风险/相对密度） | arcpy.sa.CalculateKernelDensityRatio | extension — 核密度比率为较新的时空密度变体 | ArcPy GP（官方实现，桥直调） |
| Kernel Density | 用核函数把点/线量级摊到邻域内生成密度面 | arcpy.sa.KernelDensity | core — 通用密度分析 | ArcPy GP（官方实现，桥直调） |
| Line Density | 计算每像元邻域内线的密度 | arcpy.sa.LineDensity | core — 通用密度分析 | ArcPy GP（官方实现，桥直调） |
| Point Density | 计算每像元邻域内点的密度 | arcpy.sa.PointDensity | core — 通用密度分析 | ArcPy GP（官方实现，桥直调） |
| Space Time Kernel Density | 在空间与时间维度上做核密度估计 | arcpy.sa.SpaceTimeKernelDensity | extension — 时空核密度为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |

### Distance toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Distance Accumulation | 沿成本面累积最小行进成本并可生成回溯/分配栅格 | arcpy.sa.DistanceAccumulation | core — 成本距离为通用栅格分析 | ArcPy GP（官方实现，桥直调） |
| Distance Allocation | 把像元按最小累积成本分配到最近源 | arcpy.sa.DistanceAllocation | core — 通用成本分配 | ArcPy GP（官方实现，桥直调） |
| Least Cost Corridor | 在两地之间生成最小成本走廊栅格 | arcpy.sa.LeastCostCorridor | core — 通用最小成本路径分析 | ArcPy GP（官方实现，桥直调） |
| Optimal Corridor Connections | 在输入区域之间生成最优走廊连接网络 | arcpy.sa.OptimalCorridorConnections | extension — 区域最优连接为 ArcGIS 新一代距离工具实现 | ArcPy GP（官方实现，桥直调） |
| Optimal Path as Line | 把最优路径以线要素形式输出 | arcpy.sa.OptimalPathAsLine | core — 通用最小成本路径 | ArcPy GP（官方实现，桥直调） |
| Optimal Path as Raster | 把最优路径以栅格形式输出 | arcpy.sa.OptimalPathAsRaster | core — 通用最小成本路径 | ArcPy GP（官方实现，桥直调） |
| Optimal Region Connections | 生成区域之间的最优连接路径 | arcpy.sa.OptimalRegionConnections | extension — 区域最优连接为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |

### Distance (Legacy) toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Corridor | 对两个累积成本面求和生成成本走廊（旧版） | arcpy.sa.Corridor | extension — 旧版工具，已被新 Distance 工具替代 | ArcPy GP（官方实现，桥直调） |
| Cost Allocation | 按最小成本把像元分配给最近源（旧版） | arcpy.sa.CostAllocation | extension — 旧版工具，功能已被 Distance Allocation 取代 | ArcPy GP（官方实现，桥直调） |
| Cost Back Link | 生成指向最低成本邻居方向的回溯栅格（旧版） | arcpy.sa.CostBackLink | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Cost Connectivity | 连接指定区域的成本路径网络（旧版） | arcpy.sa.CostConnectivity | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Cost Distance | 计算到最近源的累积最小成本（旧版） | arcpy.sa.CostDistance | extension — 旧版工具，功能已被 Distance Accumulation 取代 | ArcPy GP（官方实现，桥直调） |
| Cost Path | 沿回溯栅格提取最小成本路径（旧版） | arcpy.sa.CostPath | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Cost Path as Polyline | 把最小成本路径输出为折线要素（旧版） | arcpy.sa.CostPathAsPolyline | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Euclidean Allocation | 按直线距离把像元分配给最近源（旧版） | arcpy.sa.EuclideanAllocation | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Euclidean Back Direction | 生成指回来向最近源方向的栅格（旧版） | arcpy.sa.EuclideanBackDirection | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Euclidean Direction | 生成每像元到最近源的方位角栅格（旧版） | arcpy.sa.EuclideanDirection | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Euclidean Distance | 生成每像元到最近源的欧氏距离（旧版） | arcpy.sa.EuclideanDistance | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Path Distance | 计入水平/垂直成本因子的成本距离（旧版） | arcpy.sa.PathDistance | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Path Distance Allocation | 计入水平/垂直因子的成本分配（旧版） | arcpy.sa.PathDistanceAllocation | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |
| Path Distance Back Link | 计入水平/垂直因子的回溯栅格（旧版） | arcpy.sa.PathDistanceBackLink | extension — 旧版工具 | ArcPy GP（官方实现，桥直调） |

### Extraction toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Extract by Attributes | 按属性逻辑查询提取像元子集 | arcpy.sa.ExtractByAttributes | core — 通用栅格提取 | ArcPy GP（官方实现，桥直调） |
| Extract by Circle | 按圆形范围提取像元子集 | arcpy.sa.ExtractByCircle | core — 通用栅格裁剪/提取 | ArcPy GP（官方实现，桥直调） |
| Extract by Mask | 按掩膜栅格或要素范围提取像元子集 | arcpy.sa.ExtractByMask | core — 通用掩膜提取 | ArcPy GP（官方实现，桥直调） |
| Extract by Points | 按点位置提取像元（保留点位像元） | arcpy.sa.ExtractByPoints | core — 通用栅格提取 | ArcPy GP（官方实现，桥直调） |
| Extract by Polygon | 按多边形范围提取像元子集 | arcpy.sa.ExtractByPolygon | core — 通用栅格裁剪/提取 | ArcPy GP（官方实现，桥直调） |
| Extract by Rectangle | 按矩形范围提取像元子集 | arcpy.sa.ExtractByRectangle | core — 通用栅格裁剪/提取 | ArcPy GP（官方实现，桥直调） |
| Extract Multi Values to Points | 把多个栅格在点位的值写入点属性表 | arcpy.sa.ExtractMultiValuesToPoints | core — 通用采样取值 | ArcPy GP（官方实现，桥直调） |
| Extract Values to Points | 把栅格在点位的值写入点属性 | arcpy.sa.ExtractValuesToPoints | core — 通用采样取值 | ArcPy GP（官方实现，桥直调） |
| Sample | 在指定位置生成栅格像元值表或点要素 | arcpy.sa.Sample | core — 通用采样 | ArcPy GP（官方实现，桥直调） |

### Generalization toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Aggregate | 按因子聚合降分辨率并做统计概括 | arcpy.sa.Aggregate | core — 通用重采样/聚合 | ArcPy GP（官方实现，桥直调） |
| Boundary Clean | 清理栅格区域边界（平滑锯齿并按优先级伸缩） | arcpy.sa.BoundaryClean | extension — 区域边界清理为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |
| Expand | 按指定像元数扩张指定值的区域 | arcpy.sa.Expand | core — 通用形态学扩张 | ArcPy GP（官方实现，桥直调） |
| Majority Filter | 用邻域众数替换中心像元以去除噪声 | arcpy.sa.MajorityFilter | core — 通用邻域滤波 | ArcPy GP（官方实现，桥直调） |
| Nibble | 用最近有效值填补被掩膜的 NoData 区域 | arcpy.sa.Nibble | core — 通用 NoData 填补 | ArcPy GP（官方实现，桥直调） |
| Region Group | 给每个连通区域赋唯一编号 | arcpy.sa.RegionGroup | core — 通用连通域标记 | ArcPy GP（官方实现，桥直调） |
| Shrink | 按指定像元数收缩指定值的区域 | arcpy.sa.Shrink | core — 通用形态学收缩 | ArcPy GP（官方实现，桥直调） |
| Thin | 把栅格线状区域细化为单像元宽 | arcpy.sa.Thin | extension — 细化算法为具体实现 | ArcPy GP（官方实现，桥直调） |

### Groundwater toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Darcy Flow | 按达西定律由水头面生成地下水流场与水量平衡栅格 | arcpy.sa.DarcyFlow | extension — 地下水达西流为专业小众模型 | ArcPy GP（官方实现，桥直调） |
| Darcy Velocity | 由水头与孔隙参数计算地下水流速矢量栅格 | arcpy.sa.DarcyVelocity | extension — 地下水专业模型 | ArcPy GP（官方实现，桥直调） |
| Particle Track | 沿流速场追踪粒子路径并输出轨迹与时间 | arcpy.sa.ParticleTrack | extension — 地下水粒子追踪专业模型 | ArcPy GP（官方实现，桥直调） |
| Porous Puff | 模拟溶质在孔隙介质中的对流-弥散羽流 | arcpy.sa.PorousPuff | extension — 地下水溶质运移专业模型 | ArcPy GP（官方实现，桥直调） |

### Hydrology toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Basin | 由流向栅格生成全部汇水盆地 | arcpy.sa.Basin | core — 通用水文分析，DEM 填洼-流向-汇水链共有 | ArcPy GP（官方实现，桥直调） |
| Derive Continuous Flow | 直接由 DEM 生成连续流量累积与河网（无需填洼） | arcpy.sa.DeriveContinuousFlow | extension — 较新的无填洼连续流算法为 ArcGIS 实现 | ArcPy GP（官方实现，桥直调） |
| Derive Stream As Line | 由 DEM 派生河网并输出为线要素 | arcpy.sa.DeriveStreamAsLine | extension — 新一代河网提取实现 | ArcPy GP（官方实现，桥直调） |
| Derive Stream As Raster | 由 DEM 派生河网栅格 | arcpy.sa.DeriveStreamAsRaster | extension — 新一代河网提取实现 | ArcPy GP（官方实现，桥直调） |
| Fill | 填平 DEM 中的洼地 | arcpy.sa.Fill | core — 通用水文预处理 | ArcPy GP（官方实现，桥直调） |
| Flow Accumulation | 由流向栅格计算汇流累积量 | arcpy.sa.FlowAccumulation | core — 通用水文分析 | ArcPy GP（官方实现，桥直调）；ArcGIS Online 栅格分析另有同名托管工具（REST） |
| Flow Direction | 计算每像元流向（D8 等编码） | arcpy.sa.FlowDirection | core — 通用水文分析 | ArcPy GP（官方实现，桥直调） |
| Flow Distance | 计算到出口/河网的水平或垂直流动距离 | arcpy.sa.FlowDistance | core — 通用水文分析 | ArcPy GP（官方实现，桥直调） |
| Flow Length | 计算沿流向到出口的上游/下游流动长度 | arcpy.sa.FlowLength | core — 通用水文分析 | ArcPy GP（官方实现，桥直调） |
| Sink | 识别 DEM 中的洼地区域 | arcpy.sa.Sink | core — 通用水文分析 | ArcPy GP（官方实现，桥直调） |
| Snap Pour Point | 把出水口点吸附到汇流累积最大像元 | arcpy.sa.SnapPourPoint | core — 通用水文分析 | ArcPy GP（官方实现，桥直调） |
| Storage Capacity | 由 DEM 与坝高计算洼地/水库的蓄水容量曲线 | arcpy.sa.StorageCapacity | extension — 蓄水容量计算为较专用的水文工具 | ArcPy GP（官方实现，桥直调） |
| Stream Link | 给河网交汇之间的河段赋唯一编号 | arcpy.sa.StreamLink | core — 通用河网编码 | ArcPy GP（官方实现，桥直调） |
| Stream Order | 按 Strahler/Shreve 方法给河网分级 | arcpy.sa.StreamOrder | core — 通用河网分级 | ArcPy GP（官方实现，桥直调） |
| Stream to Feature | 把河网栅格转为线要素 | arcpy.sa.StreamToFeature | core — 通用栅格转矢量 | ArcPy GP（官方实现，桥直调） |
| Watershed | 由出水口或流向栅格划定汇水区 | arcpy.sa.Watershed | core — 通用分水岭划定 | ArcPy GP（官方实现，桥直调）；ArcGIS Online 栅格分析另有同名托管工具（REST） |

### Interpolation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| IDW | 用反距离加权从采样点插值生成栅格面 | arcpy.sa.IDW | core — 常用插值法，多家共有 | ArcPy GP（官方实现，桥直调） |
| Kriging | 用克里金法从采样点插值并可输出方差面 | arcpy.sa.Kriging | core — 常用插值法，多家共有 | ArcPy GP（官方实现，桥直调） |
| Natural Neighbor | 用自然邻域法从采样点插值生成栅格面 | arcpy.sa.NaturalNeighbor | core — 常用插值法 | ArcPy GP（官方实现，桥直调） |
| Spline | 用最小曲率样条从采样点插值生成平滑面 | arcpy.sa.Spline | core — 常用插值法 | ArcPy GP（官方实现，桥直调） |
| Spline with Barriers | 带障碍线的样条插值 | arcpy.sa.SplineWithBarriers | extension — 带障碍样条为具体实现变体 | ArcPy GP（官方实现，桥直调） |
| Topo to Raster | 由等高线及点线面地形要素插值出水文正确的 DEM | arcpy.sa.TopoToRaster | extension — ANUDEM 算法为 ArcGIS 专属实现 | ArcPy GP（官方实现，桥直调） |
| Topo to Raster by File | 按参数文件批量执行 Topo to Raster 插值 | arcpy.sa.TopoToRasterByFile | extension — 同 Topo to Raster，专属实现 | ArcPy GP（官方实现，桥直调） |
| Trend | 用多项式趋势面拟合采样点生成栅格 | arcpy.sa.Trend | core — 常用趋势面插值 | ArcPy GP（官方实现，桥直调） |

### Local toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Cell Statistics | 逐像元对多个栅格做统计（均值/最大/最小等） | arcpy.sa.CellStatistics | core — 通用逐像元统计 | ArcPy GP（官方实现，桥直调） |
| Combine | 逐像元组合多个栅格的唯一值组合并编号 | arcpy.sa.Combine | core — 通用栅格组合 | ArcPy GP（官方实现，桥直调） |
| Equal to Frequency | 统计逐像元等于指定值的栅格个数 | arcpy.sa.EqualToFrequency | core — 通用频率统计 | ArcPy GP（官方实现，桥直调） |
| Greater Than Frequency | 统计逐像元大于第一个栅格值的栅格个数 | arcpy.sa.GreaterThanFrequency | core — 通用频率统计 | ArcPy GP（官方实现，桥直调） |
| Highest Position | 输出逐像元最大值所在输入栅格的序号 | arcpy.sa.HighestPosition | core — 通用位置统计 | ArcPy GP（官方实现，桥直调） |
| Less Than Frequency | 统计逐像元小于第一个栅格值的栅格个数 | arcpy.sa.LessThanFrequency | core — 通用频率统计 | ArcPy GP（官方实现，桥直调） |
| Lowest Position | 输出逐像元最小值所在输入栅格的序号 | arcpy.sa.LowestPosition | core — 通用位置统计 | ArcPy GP（官方实现，桥直调） |
| Popularity | 输出逐像元第 N 众数所在输入栅格的序号 | arcpy.sa.Popularity | core — 通用位置统计 | ArcPy GP（官方实现，桥直调） |
| Rank | 对多个栅格在逐像元处按指定名次取值 | arcpy.sa.Rank | core — 通用排序取值 | ArcPy GP（官方实现，桥直调） |

### Map Algebra toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Raster Calculator | 用地图代数表达式逐像元计算生成新栅格 | arcpy.sa.RasterCalculator | core — 栅格计算为平台核心能力，多家共有 | ArcPy GP（官方实现，桥直调） |

### Math (general) toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Abs | 逐像元取绝对值 | arcpy.sa.Abs | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Divide | 逐像元两栅格相除 | arcpy.sa.Divide | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Exp | 逐像元计算 e 的幂 | arcpy.sa.Exp | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Exp10 | 逐像元计算 10 的幂 | arcpy.sa.Exp10 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Exp2 | 逐像元计算 2 的幂 | arcpy.sa.Exp2 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Float | 逐像元把值转成浮点数 | arcpy.sa.Float | core — 通用类型转换 | ArcPy GP（官方实现，桥直调） |
| Int | 逐像元截断取整 | arcpy.sa.Int | core — 通用类型转换 | ArcPy GP（官方实现，桥直调） |
| Ln | 逐像元取自然对数 | arcpy.sa.Ln | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Log10 | 逐像元取以 10 为底对数 | arcpy.sa.Log10 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Log2 | 逐像元取以 2 为底对数 | arcpy.sa.Log2 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Minus | 逐像元两栅格相减 | arcpy.sa.Minus | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Mod | 逐像元求除法余数 | arcpy.sa.Mod | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Negate | 逐像元取相反数 | arcpy.sa.Negate | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Plus | 逐像元两栅格相加 | arcpy.sa.Plus | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Power | 逐像元以另一栅格为指数做幂运算 | arcpy.sa.Power | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Round Down | 逐像元向下取整（以浮点表示） | arcpy.sa.RoundDown | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Round Up | 逐像元向上取整（以浮点表示） | arcpy.sa.RoundUp | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Square | 逐像元求平方 | arcpy.sa.Square | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Square Root | 逐像元求平方根 | arcpy.sa.SquareRoot | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Times | 逐像元两栅格相乘 | arcpy.sa.Times | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |

### Math Bitwise toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Bitwise And | 逐像元对两栅格做按位与 | arcpy.sa.BitwiseAnd | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Left Shift | 逐像元做按位左移 | arcpy.sa.BitwiseLeftShift | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Not | 逐像元做按位取反 | arcpy.sa.BitwiseNot | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Or | 逐像元对两栅格做按位或 | arcpy.sa.BitwiseOr | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Right Shift | 逐像元做按位右移 | arcpy.sa.BitwiseRightShift | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise XOr | 逐像元对两栅格做按位异或 | arcpy.sa.BitwiseXOr | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |

### Math Logical toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Boolean And | 逐像元做布尔与（非零为真） | arcpy.sa.BooleanAnd | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Boolean Not | 逐像元做布尔非 | arcpy.sa.BooleanNot | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Boolean Or | 逐像元做布尔或 | arcpy.sa.BooleanOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Boolean XOr | 逐像元做布尔异或 | arcpy.sa.BooleanXOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Combinatorial And | 逐像元组合与：两值皆真时输出唯一组合值 | arcpy.sa.CombinatorialAnd | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Combinatorial Or | 逐像元组合或：任一为真时输出唯一组合值 | arcpy.sa.CombinatorialOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Combinatorial XOr | 逐像元组合异或：恰一为真时输出唯一组合值 | arcpy.sa.CombinatorialXOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Diff | 逐像元比较两栅格，不同则输出第一栅格值、相同输出 0 | arcpy.sa.Diff | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Equal To | 逐像元判断两栅格是否相等（1/0） | arcpy.sa.EqualTo | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Greater Than | 逐像元判断第一栅格是否大于第二栅格（1/0） | arcpy.sa.GreaterThan | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Greater Than Equal | 逐像元判断第一栅格是否大于等于第二栅格（1/0） | arcpy.sa.GreaterThanEqual | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| In List | 逐像元判断值是否出现在其他栅格列表中 | arcpy.sa.InList | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Is Null | 逐像元判断是否为 NoData（1/0） | arcpy.sa.IsNull | core — 通用 NoData 判断 | ArcPy GP（官方实现，桥直调） |
| Less Than | 逐像元判断第一栅格是否小于第二栅格（1/0） | arcpy.sa.LessThan | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Less Than Equal | 逐像元判断第一栅格是否小于等于第二栅格（1/0） | arcpy.sa.LessThanEqual | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Not Equal | 逐像元判断两栅格是否不相等（1/0） | arcpy.sa.NotEqual | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Over | 逐像元以第一栅格非零值覆盖、为零处取第二栅格值 | arcpy.sa.Over | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Test | 逐像元按逻辑表达式求值输出 1/0 | arcpy.sa.Test | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |

### Math Trigonometric toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| ACos | 逐像元计算反余弦 | arcpy.sa.ACos | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ACosH | 逐像元计算反双曲余弦 | arcpy.sa.ACosH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ASin | 逐像元计算反正弦 | arcpy.sa.ASin | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ASinH | 逐像元计算反双曲正弦 | arcpy.sa.ASinH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ATan | 逐像元计算反正切 | arcpy.sa.ATan | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ATan2 | 逐像元由两栅格计算反正切（按官方表：反双曲正切口径以工具页为准） | arcpy.sa.ATan2 | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ATanH | 逐像元计算反双曲正切 | arcpy.sa.ATanH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| Cos | 逐像元计算余弦 | arcpy.sa.Cos | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| CosH | 逐像元计算双曲余弦 | arcpy.sa.CosH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| Sin | 逐像元计算正弦 | arcpy.sa.Sin | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| SinH | 逐像元计算双曲正弦 | arcpy.sa.SinH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| Tan | 逐像元计算正切 | arcpy.sa.Tan | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| TanH | 逐像元计算双曲正切 | arcpy.sa.TanH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |

### Multidimensional Analysis toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Aggregate Multidimensional Raster | 沿维度聚合多维栅格变量生成新的多维栅格 | arcpy.sa.AggregateMultidimensionalRaster | core — 多维栅格聚合为通用科学数据处理 | ArcPy GP（官方实现，桥直调） |
| Dimensional Moving Statistics | 沿指定维度对多维数据做移动窗口统计 | arcpy.sa.DimensionalMovingStatistics | core — 多维栅格统计为通用处理 | ArcPy GP（官方实现，桥直调） |
| Generate Multidimensional Anomaly | 逐切片计算多维栅格距平生成新的多维栅格 | arcpy.sa.GenerateMultidimensionalAnomaly | core — 距平计算为通用处理 | ArcPy GP（官方实现，桥直调） |

### Multivariate toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Band Collection Statistics | 计算多波段栅格的均值/方差/协方差等波段统计 | arcpy.sa.BandCollectionStatistics | core — 通用多波段统计 | ArcPy GP（官方实现，桥直调） |
| Class Probability | 由签名文件计算各类别的概率栅格 | arcpy.sa.ClassProbability | extension — 依赖 ArcGIS 签名文件体系 | ArcPy GP（官方实现，桥直调） |
| Create Signatures | 由样本区与栅格创建类别光谱签名文件 | arcpy.sa.CreateSignatures | extension — 签名文件为 ArcGIS 分类体系专属格式 | ArcPy GP（官方实现，桥直调） |
| Dendrogram | 由签名文件计算类别光谱距离并输出树状图 | arcpy.sa.Dendrogram | extension — 依赖签名文件体系 | ArcPy GP（官方实现，桥直调） |
| Edit Signatures | 编辑签名文件（合并/删除/重命名类别等） | arcpy.sa.EditSignatures | extension — 签名文件专属编辑 | ArcPy GP（官方实现，桥直调） |
| Iso Cluster | 用 ISODATA 聚类生成无监督分类签名 | arcpy.sa.IsoCluster | core — ISODATA 为通用无监督分类算法 | ArcPy GP（官方实现，桥直调） |
| Iso Cluster Unsupervised Classification | 用 Iso Cluster 一步做无监督分类出图 | arcpy.sa.IsoClusterUnsupervisedClassification | core — 通用无监督分类 | ArcPy GP（官方实现，桥直调） |
| Maximum Likelihood Classification | 用最大似然法按签名文件做监督分类 | arcpy.sa.MaximumLikelihoodClassification | core — 最大似然为通用监督分类 | ArcPy GP（官方实现，桥直调） |
| Principal Components | 对多波段栅格做主成分分析降维 | arcpy.sa.PrincipalComponents | core — PCA 为通用降维，多家共有 | ArcPy GP（官方实现，桥直调） |

### Neighborhood toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Block Statistics | 按不重叠分块计算邻域统计并输出块状栅格 | arcpy.sa.BlockStatistics | core — 通用邻域统计 | ArcPy GP（官方实现，桥直调） |
| Filter | 用 3×3 低通/高通核做栅格滤波 | arcpy.sa.Filter | core — 通用栅格滤波 | ArcPy GP（官方实现，桥直调） |
| Focal Flow | 按邻域流向规则生成焦点流栅格（地下水/地表流） | arcpy.sa.FocalFlow | extension — 焦点流为较专用的邻域规则 | ArcPy GP（官方实现，桥直调） |
| Focal Statistics | 在指定邻域内逐像元计算统计量 | arcpy.sa.FocalStatistics | core — 通用邻域统计 | ArcPy GP（官方实现，桥直调） |
| Line Statistics | 在邻域内计算线要素的统计（如密度/长度） | arcpy.sa.LineStatistics | extension — 线邻域统计为具体实现 | ArcPy GP（官方实现，桥直调） |
| Point Statistics | 在邻域内计算点要素的统计（如计数/均值） | arcpy.sa.PointStatistics | extension — 点邻域统计为具体实现 | ArcPy GP（官方实现，桥直调） |

### Overlay toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Fuzzy Membership | 按模糊隶属函数把栅格值转成 0–1 隶属度 | arcpy.sa.FuzzyMembership | extension — 模糊适宜性建模为 ArcGIS 叠加体系 | ArcPy GP（官方实现，桥直调） |
| Fuzzy Overlay | 对多个模糊隶属栅格做模糊逻辑叠加 | arcpy.sa.FuzzyOverlay | extension — 模糊叠加为具体实现 | ArcPy GP（官方实现，桥直调） |
| Locate Regions | 在适宜性结果中按面积/形状规格选出最优区域斑块 | arcpy.sa.LocateRegions | extension — 区域选址规格化为 ArcGIS 叠加工具 | ArcPy GP（官方实现，桥直调） |
| Weighted Overlay | 多栅格按权重与统一量表加权叠加做适宜性评价 | arcpy.sa.WeightedOverlay | core — 加权叠加适宜性为通用建模方法 | ArcPy GP（官方实现，桥直调） |
| Weighted Sum | 多栅格乘权重后逐像元求和 | arcpy.sa.WeightedSum | core — 通用加权求和 | ArcPy GP（官方实现，桥直调） |

### Raster Creation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Constant Raster | 生成全图为常数值的栅格 | arcpy.sa.CreateConstantRaster | core — 通用栅格生成 | ArcPy GP（官方实现，桥直调） |
| Create Normal Raster | 生成服从正态分布的随机值栅格 | arcpy.sa.CreateNormalRaster | core — 通用栅格生成 | ArcPy GP（官方实现，桥直调） |
| Create Random Raster | 生成 0–1 均匀随机值栅格 | arcpy.sa.CreateRandomRaster | core — 通用栅格生成 | ArcPy GP（官方实现，桥直调） |

### Reclass toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Lookup | 按另一栅格的某个属性字段查表赋新值 | arcpy.sa.Lookup | core — 通用查表重分类 | ArcPy GP（官方实现，桥直调） |
| Reclass by ASCII File | 按 ASCII 重映射表文件重分类 | arcpy.sa.ReclassByASCIIFile | core — 通用重分类 | ArcPy GP（官方实现，桥直调） |
| Reclass by Table | 按属性表重映射重分类 | arcpy.sa.ReclassByTable | core — 通用重分类 | ArcPy GP（官方实现，桥直调） |
| Reclassify | 按值区间/单值映射重分类或设 NoData | arcpy.sa.Reclassify | core — 重分类为平台核心能力，多家共有 | ArcPy GP（官方实现，桥直调） |
| Rescale by Function | 用连续函数把值重标定到新量程（如适宜性） | arcpy.sa.RescaleByFunction | extension — 函数重标定为 ArcGIS 适宜性体系 | ArcPy GP（官方实现，桥直调） |
| Slice | 按等间隔/等面积/自然断点把栅格切成若干级 | arcpy.sa.Slice | core — 通用分级切片 | ArcPy GP（官方实现，桥直调） |

### Segmentation and Classification toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Classify Raster | 按分类器定义文件（.ecd）对栅格做分类 | arcpy.sa.ClassifyRaster | extension — 依赖 Esri .ecd 分类器定义格式 | ArcPy GP（官方实现，桥直调） |
| Compute Confusion Matrix | 计算分类结果与参考数据的混淆矩阵及 Kappa 等精度 | arcpy.sa.ComputeConfusionMatrix | core — 精度评价为通用流程 | ArcPy GP（官方实现，桥直调） |
| Compute Segment Attributes | 计算分割影像中各对象的属性 | arcpy.sa.ComputeSegmentAttributes | core — 面向对象分类的通用步骤 | ArcPy GP（官方实现，桥直调） |
| Create Accuracy Assessment Points | 随机生成用于分类精度评价的样本点 | arcpy.sa.CreateAccuracyAssessmentPoints | core — 精度评价为通用流程 | ArcPy GP（官方实现，桥直调） |
| Export Training Data For Deep Learning | 把标注矢量/栅格导出为深度学习训练样本切片 | arcpy.sa.ExportTrainingDataForDeepLearning | defer — 深度学习训练管线前置步骤，单独注记 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Generate Training Samples From Seed Points | 由种子点生成分类训练样本 | arcpy.sa.GenerateTrainingSamplesFromSeedPoints | core — 训练样本生成为通用分类流程 | ArcPy GP（官方实现，桥直调） |
| Inspect Training Samples | 用已有分类结果交叉验证评估单个训练样本精度 | arcpy.sa.InspectTrainingSamples | extension — 依赖 .ecd 训练结果体系 | ArcPy GP（官方实现，桥直调） |
| Linear Spectral Unmixing | 亚像元分解计算各端元在像元中的丰度 | arcpy.sa.LinearSpectralUnmixing | core — 光谱解混为通用遥感方法 | ArcPy GP（官方实现，桥直调） |
| Remove Raster Segment Tiling Artifacts | 修正分割时瓦片边界处对象被切断的伪影 | arcpy.sa.RemoveRasterSegmentTilingArtifacts | extension — 分割瓦片伪影修正为具体实现 | ArcPy GP（官方实现，桥直调） |
| Segment Mean Shift | 用均值漂移把邻近且光谱相似像元聚成对象（分割） | arcpy.sa.SegmentMeanShift | core — 均值漂移分割为通用 OBIA 方法 | ArcPy GP（官方实现，桥直调） |
| Train Iso Cluster Classifier | 训练 Iso Cluster 无监督分类器并输出 .ecd | arcpy.sa.TrainIsoClusterClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Train K-Nearest Neighbor Classifier | 训练 K 近邻分类器并输出 .ecd | arcpy.sa.TrainKNearestNeighborClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Train Maximum Likelihood Classifier | 训练最大似然分类器并输出 .ecd | arcpy.sa.TrainMaximumLikelihoodClassifier | extension — 输出 Esri 专属 .ecd 格式（工具名以完整清单页为准） | ArcPy GP（官方实现，桥直调） |
| Train Random Trees Classifier | 训练随机森林（Random Trees）分类器并输出 .ecd | arcpy.sa.TrainRandomTreesClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Train Support Vector Machine Classifier | 训练支持向量机分类器并输出 .ecd | arcpy.sa.TrainSupportVectorMachineClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Update Accuracy Assessment Points | 更新精度评价点的 Target 字段以与分类图对比 | arcpy.sa.UpdateAccuracyAssessmentPoints | core — 精度评价为通用流程 | ArcPy GP（官方实现，桥直调） |

### Solar Radiation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Area Solar Radiation | 按地形遮挡计算区域逐像元太阳辐射量 | arcpy.sa.AreaSolarRadiation | extension — 太阳辐射地形模型为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |
| Feature Solar Radiation | 为点/线/面要素计算太阳辐射量 | arcpy.sa.FeatureSolarRadiation | extension — 同太阳辐射模型 | ArcPy GP（官方实现，桥直调） |
| Points Solar Radiation | 为指定点位计算太阳辐射量 | arcpy.sa.PointsSolarRadiation | extension — 同太阳辐射模型 | ArcPy GP（官方实现，桥直调） |
| Raster Solar Radiation | 由栅格 DEM 计算太阳辐射（新版） | arcpy.sa.RasterSolarRadiation | extension — 同太阳辐射模型 | ArcPy GP（官方实现，桥直调） |
| Solar Radiation Graphics | 生成天空图/太阳图等辐射计算图形栅格 | arcpy.sa.SolarRadiationGraphics | extension — 辐射模型辅助产物 | ArcPy GP（官方实现，桥直调） |

### Surface toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Surface Information | 把表面（栅格/TIN/地形/LAS）的 Z 值与坡度等写入要素属性 | arcpy.sa.AddSurfaceInformation | core — 通用表面取值 | ArcPy GP（官方实现，桥直调） |
| Aspect | 由 DEM 计算坡向栅格 | arcpy.sa.Aspect | core — 坡向为通用地形分析，多家共有 | ArcPy GP（官方实现，桥直调）；同类能力另有 Esri 托管高程分析服务（ArcGIS REST） |
| Contour | 由 DEM 生成等高线要素 | arcpy.sa.Contour | core — 等高线为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Contour List | 按指定等高距值列表生成等高线 | arcpy.sa.ContourList | core — 通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Contour with Barriers | 带障碍（如悬崖/断层）生成等高线 | arcpy.sa.ContourWithBarriers | extension — 带障碍等高线为具体实现 | ArcPy GP（官方实现，桥直调） |
| Curvature | 计算表面曲率（剖面/平面曲率）栅格 | arcpy.sa.Curvature | core — 曲率为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Cut Fill | 比较两期表面计算挖填方量与净变化 | arcpy.sa.CutFill | core — 挖填方为通用表面差分 | ArcPy GP（官方实现，桥直调） |
| Feature Preserving Smoothing | 保特征平滑 DEM（降噪同时保留地形棱线） | arcpy.sa.FeaturePreservingSmoothing | extension — 保特征平滑为较新的 ArcGIS 算法 | ArcPy GP（官方实现，桥直调） |
| Geomorphon Landforms | 按 Geomorphon 方法识别地貌形态单元 | arcpy.sa.GeomorphonLandforms | extension — 地貌形态分类为具体实现 | ArcPy GP（官方实现，桥直调） |
| Geodesic Viewshed | 考虑地球曲率与折光的大地可视域分析 | arcpy.sa.GeodesicViewshed | core — 可视域为通用表面分析 | ArcPy GP（官方实现，桥直调）；同类能力另有 Esri 托管高程分析服务（ArcGIS REST） |
| Hillshade | 由 DEM 与光源方位生成山体阴影栅格 | arcpy.sa.Hillshade | core — 山影为通用地形渲染/分析 | ArcPy GP（官方实现，桥直调）；同类能力另有 Esri 托管高程分析服务（ArcGIS REST） |
| Interpolate Shape | 把 2D 要素按表面高程转为 3D 要素 | arcpy.sa.InterpolateShape | core — 通用表面赋高 | ArcPy GP（官方实现，桥直调） |
| Multiscale Surface Difference | 多尺度比较两表面差异 | arcpy.sa.MultiscaleSurfaceDifference | extension — 多尺度表面差分为较新实现 | ArcPy GP（官方实现，桥直调） |
| Multiscale Surface Percentile | 多尺度计算表面高程分位数 | arcpy.sa.MultiscaleSurfacePercentile | extension — 多尺度表面统计为较新实现 | ArcPy GP（官方实现，桥直调） |
| Observer Points | 生成能看到指定区域的观察点分布栅格 | arcpy.sa.ObserverPoints | core — 可视域逆向分析为通用表面分析 | ArcPy GP（官方实现，桥直调） |
| Slope | 由 DEM 计算坡度栅格 | arcpy.sa.Slope | core — 坡度为通用地形分析，多家共有 | ArcPy GP（官方实现，桥直调）；同类能力另有 Esri 托管高程分析服务（ArcGIS REST） |
| Surface Parameters | 直接由 DEM 计算坡度/坡向/曲率等表面参数（多尺度） | arcpy.sa.SurfaceParameters | core — 表面参数为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Viewshed | 计算指定观察点的可见/不可见区域 | arcpy.sa.Viewshed | core — 可视域为通用表面分析 | ArcPy GP（官方实现，桥直调）；同类能力另有 Esri 托管高程分析服务（ArcGIS REST） |
| Visibility | 计算观察点可见性并可输出视线方向信息 | arcpy.sa.Visibility | core — 可见性分析为通用表面分析 | ArcPy GP（官方实现，桥直调） |

### Zonal toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Tabulate Area | 交叉统计两栅格/分区与类别的面积表 | arcpy.sa.TabulateArea | core — 通用分区面积统计 | ArcPy GP（官方实现，桥直调） |
| Zonal Characterization | 对每个分区生成地形等特征描述图件 | arcpy.sa.ZonalCharacterization | extension — 分区刻画图件为具体实现 | ArcPy GP（官方实现，桥直调） |
| Zonal Fill | 用分区内像元值的加权平均填充各分区 | arcpy.sa.ZonalFill | extension — 填充分区为具体实现 | ArcPy GP（官方实现，桥直调） |
| Zonal Geometry | 计算每个分区的面积/周长/厚度/质心等几何量 | arcpy.sa.ZonalGeometry | core — 通用分区几何统计 | ArcPy GP（官方实现，桥直调） |
| Zonal Geometry as Table | 把分区几何量输出为表 | arcpy.sa.ZonalGeometryAsTable | core — 通用分区统计 | ArcPy GP（官方实现，桥直调） |
| Zonal Histogram | 生成每个分区内值栅格的直方图统计 | arcpy.sa.ZonalHistogram | core — 通用分区统计 | ArcPy GP（官方实现，桥直调） |
| Zonal Statistics | 按分区统计值栅格（均值/最大/最小等）输出栅格 | arcpy.sa.ZonalStatistics | core — 分区统计为通用栅格分析 | ArcPy GP（官方实现，桥直调） |
| Zonal Statistics as Table | 按分区统计值栅格并输出为表 | arcpy.sa.ZonalStatisticsAsTable | core — 通用分区统计 | ArcPy GP（官方实现，桥直调） |

## 3D Analyst toolbox（arcpy.ddd）

工具集数：11 个一级 toolset（本表展开 24 组）；工具总数：138（去重后）；所需扩展许可：3D Analyst license；官方定位：在栅格、Terrain、TIN 与 LAS 数据集等表面模型及三维矢量数据上做分析、数据管理与格式转换。

### 3D Features toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Enclose Multipatch | 把多面体要素封口生成闭合多面体 | arcpy.ddd.EncloseMultipatch | extension — 多面体为 ArcGIS 3D 数据类型 | ArcPy GP（官方实现，桥直调） |
| Enforce River Monotonicity | 强制河道要素 Z 值沿流向单调递减 | arcpy.ddd.EnforceRiverMonotonicity | extension — 河道高程校正为专用处理 | ArcPy GP（官方实现，桥直调） |
| Is Closed 3D | 判断多面体要素是否闭合 | arcpy.ddd.IsClosed3D | extension — 多面体专属检查 | ArcPy GP（官方实现，桥直调） |
| LAS Building Multipatch | 由 LAS 点云中的建筑点生成建筑多面体 | arcpy.ddd.LASBuildingMultipatch | extension — 点云建楼为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |
| Simplify 3D Line | 按容差简化 3D 线要素的折点 | arcpy.ddd.Simplify3DLine | core — 通用三维线简化 | ArcPy GP（官方实现，桥直调） |

### 3D Features / Conversion toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| ASCII 3D To Feature Class | 把 ASCII 格式的 3D 点/线文件转为要素类 | arcpy.ddd.ASCII3DToFeatureClass | core — 通用格式转换 | ArcPy GP（官方实现，桥直调） |
| Feature Class Z To ASCII | 把带 Z 的要素类导出为 ASCII 文本 | arcpy.ddd.FeatureClassZToASCII | core — 通用格式转换 | ArcPy GP（官方实现，桥直调） |
| Feature To 3D By Attribute | 按属性字段把 2D 要素转为 3D 要素 | arcpy.ddd.FeatureTo3DByAttribute | core — 通用赋高转换 | ArcPy GP（官方实现，桥直调） |
| Features From CityEngine Rules | 用 CityEngine 规则包由 2D 要素程序化生成 3D 要素 | arcpy.ddd.FeaturesFromCityEngineRules | extension — 依赖 CityEngine 规则体系 | ArcPy GP（官方实现，桥直调） |
| Import 3D Files | 导入 COLLADA/SketchUp/OpenFlight 等 3D 模型文件为多面体 | arcpy.ddd.Import3DFiles | extension — 多格式 3D 模型导入为 ArcGIS 实现 | ArcPy GP（官方实现，桥直调） |
| Layer 3D To Feature Class | 把 3D 图层转为要素类 | arcpy.ddd.Layer3DToFeatureClass | core — 通用图层转换 | ArcPy GP（官方实现，桥直调） |

### 3D Features / Extraction toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Extract Multipatch From Mesh | 从集成网格（场景图层）中提取多面体要素 | arcpy.ddd.ExtractMultipatchFromMesh | extension — 集成网格为 ArcGIS 场景数据类型 | ArcPy GP（官方实现，桥直调） |
| Extract Power Lines From Point Cloud | 从点云中提取电力线要素 | arcpy.ddd.ExtractPowerLinesFromPointCloud | extension — 电力线提取为专用算法管线 | ArcPy GP（官方实现，桥直调） |
| Extract Rails From Point Cloud | 从点云中提取铁轨要素 | arcpy.ddd.ExtractRailsFromPointCloud | extension — 铁轨提取为专用算法管线 | ArcPy GP（官方实现，桥直调） |
| Multipatch Footprint | 生成多面体要素的平面占地轮廓 | arcpy.ddd.MultipatchFootprint | core — 通用占地提取 | ArcPy GP（官方实现，桥直调） |
| Regularize Adjacent Building Footprint | 规整相邻建筑轮廓（共边对齐） | arcpy.ddd.RegularizeAdjacentBuildingFootprint | extension — 建筑轮廓规整为具体实现 | ArcPy GP（官方实现，桥直调） |
| Regularize Building Footprint | 把建筑轮廓规整为规则几何形状 | arcpy.ddd.RegularizeBuildingFootprint | extension — 建筑轮廓规整为具体实现 | ArcPy GP（官方实现，桥直调） |

### 3D Features / Interpolation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Interpolate Polygon to Multipatch | 把多边形按表面高程转为多面体 | arcpy.ddd.InterpolatePolygonToMultipatch | extension — 多面体生成为 ArcGIS 数据类型处理 | ArcPy GP（官方实现，桥直调） |
| Interpolate Shape | 把 2D 要素按表面高程转为 3D 要素 | arcpy.ddd.InterpolateShape | core — 通用表面赋高 | ArcPy GP（官方实现，桥直调） |
| Update Feature Z | 用表面高程更新要素的 Z 值 | arcpy.ddd.UpdateFeatureZ | core — 通用表面赋高 | ArcPy GP（官方实现，桥直调） |

### 3D Intersections toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Fence Diagram | 沿剖面线由多层表面生成栅栏图（剖面要素） | arcpy.ddd.FenceDiagram | extension — 栅栏图为地质剖面专用产物 | ArcPy GP（官方实现，桥直调） |
| Intersect 3D | 求两个多面体要素集的 3D 交集体 | arcpy.ddd.Intersect3D | extension — 三维布尔交为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |
| Intersect 3D Line With Multipatch | 求 3D 线与多面体的交点/交段 | arcpy.ddd.Intersect3DLineWithMultipatch | extension — 三维求交为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |
| Intersect 3D Line With Surface | 求 3D 线与表面的交点并按交点打断线 | arcpy.ddd.Intersect3DLineWithSurface | extension — 三维求交为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |
| Intersect 3D Lines | 求 3D 线之间在三维空间中的交点 | arcpy.ddd.Intersect3DLines | extension — 三维求交为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |
| Stack Profile | 沿线采样多个表面生成堆叠剖面图数据 | arcpy.ddd.StackProfile | extension — 堆叠剖面为专用分析产物 | ArcPy GP（官方实现，桥直调） |

### 3D Proximity toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Buffer 3D | 按三维距离生成要素的 3D 缓冲体 | arcpy.ddd.Buffer3D | extension — 三维缓冲为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |
| Generate Clearance Surface | 由障碍要素生成净空（安全高度）表面 | arcpy.ddd.GenerateClearanceSurface | extension — 净空面为航空等专用分析 | ArcPy GP（官方实现，桥直调） |
| Difference 3D | 求两个多面体集的 3D 差集 | arcpy.ddd.Difference3D | extension — 三维布尔差为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |
| Inside 3D | 判断要素是否位于多面体内部并标记 | arcpy.ddd.Inside3D | extension — 三维包含判断为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |
| Locate LAS Points By Proximity | 按与要素的邻近关系定位 LAS 点 | arcpy.ddd.LocateLASPointsByProximity | extension — LAS 邻近查询为具体实现 | ArcPy GP（官方实现，桥直调） |
| Near 3D | 计算三维空间中要素间的最近距离与位置 | arcpy.ddd.Near3D | core — 三维最近邻为通用空间邻近分析 | ArcPy GP（官方实现，桥直调） |
| Union 3D | 合并两个多面体集的 3D 并集 | arcpy.ddd.Union3D | extension — 三维布尔并为 ArcGIS 3D 运算 | ArcPy GP（官方实现，桥直调） |

### Area and Volume toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Cut Fill | 比较两期表面计算挖填方量 | arcpy.ddd.CutFill | core — 挖填方为通用表面差分 | ArcPy GP（官方实现，桥直调） |
| Extrude Between | 在两个 TIN 表面之间挤出多面体体块 | arcpy.ddd.ExtrudeBetween | extension — 表面间挤出为 ArcGIS 3D 处理 | ArcPy GP（官方实现，桥直调） |
| Minimum Bounding Volume | 生成包围要素的最小体积几何（长方体/凸包等） | arcpy.ddd.MinimumBoundingVolume | core — 最小包围体为通用三维几何 | ArcPy GP（官方实现，桥直调） |
| Polygon Volume | 计算多边形范围内表面之上/之下的体积 | arcpy.ddd.PolygonVolume | core — 通用体积计算 | ArcPy GP（官方实现，桥直调） |
| Surface Difference | 求两表面的差值并生成差值多面体/栅格 | arcpy.ddd.SurfaceDifference | core — 通用表面差分 | ArcPy GP（官方实现，桥直调） |
| Surface Volume | 计算表面在参考平面之上/之下的面积与体积 | arcpy.ddd.SurfaceVolume | core — 通用体积计算 | ArcPy GP（官方实现，桥直调） |

### Point Cloud toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Colorize LAS | 用正射影像等栅格给 LAS 点赋 RGB 颜色 | arcpy.ddd.ColorizeLAS | core — 点云赋色为通用 LAS 处理 | ArcPy GP（官方实现，桥直调） |
| Extract LAS | 按范围/类别等条件从 LAS 数据集提取子集 LAS 文件 | arcpy.ddd.ExtractLAS | core — LAS 子集提取为基础处理 | ArcPy GP（官方实现，桥直调） |
| Extract Objects From Point Cloud | 用已训练模型等从点云中提取对象 | arcpy.ddd.ExtractObjectsFromPointCloud | defer — 依赖已训练模型的点云对象提取管线 | ArcPy GP（官方实现，桥直调） |
| Thin LAS | 抽稀 LAS 点生成更均匀的子集 | arcpy.ddd.ThinLAS | core — 点云抽稀为基础处理 | ArcPy GP（官方实现，桥直调） |
| Tile LAS | 把 LAS 数据集切分为规则瓦片文件 | arcpy.ddd.TileLAS | core — LAS 分瓦为基础处理 | ArcPy GP（官方实现，桥直调） |

### Point Cloud / Classification toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Change LAS Class Codes | 批量修改 LAS 点的分类代码 | arcpy.ddd.ChangeLASClassCodes | core — LAS 分类编辑为基础处理 | ArcPy GP（官方实现，桥直调） |
| Classify LAS Building | 自动把屋顶点分类为建筑类 | arcpy.ddd.ClassifyLASBuilding | core — LAS 建筑分类为常用点云处理 | ArcPy GP（官方实现，桥直调） |
| Classify LAS By Height | 按相对地面高度给 LAS 点分类 | arcpy.ddd.ClassifyLASByHeight | core — LAS 按高分类为基础处理 | ArcPy GP（官方实现，桥直调） |
| Classify LAS Ground | 自动识别 LAS 地面点 | arcpy.ddd.ClassifyLASGround | core — LAS 地面点分类为核心点云处理，多家共有 | ArcPy GP（官方实现，桥直调） |
| Classify LAS Noise | 自动识别 LAS 噪声点（低/高异常点） | arcpy.ddd.ClassifyLASNoise | core — LAS 噪声分类为基础处理 | ArcPy GP（官方实现，桥直调） |
| Classify LAS Overlap | 标记重叠航带区域的 LAS 点为重叠类 | arcpy.ddd.ClassifyLASOverlap | core — LAS 重叠标记为基础处理 | ArcPy GP（官方实现，桥直调） |
| Set LAS Class Codes Using Features | 用要素范围给 LAS 点赋分类代码 | arcpy.ddd.SetLASClassCodesUsingFeatures | core — LAS 分类编辑为基础处理 | ArcPy GP（官方实现，桥直调） |
| Set LAS Class Codes Using Raster | 用栅格值给 LAS 点赋分类代码 | arcpy.ddd.SetLASClassCodesUsingRaster | core — LAS 分类编辑为基础处理 | ArcPy GP（官方实现，桥直调） |

### Point Cloud / Classification (Deep Learning) toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Classify Point Cloud Using Trained Model | 用已训练深度学习模型给点云分类 | arcpy.ddd.ClassifyPointCloudUsingTrainedModel | defer — 深度学习点云分类管线，依赖已训练模型 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Evaluate Point Cloud Classification Model | 评估点云分类模型的精度 | arcpy.ddd.EvaluatePointCloudClassificationModel | defer — 深度学习模型评估管线 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Prepare Point Cloud Training Data | 把 LAS 准备为点云深度学习训练数据 | arcpy.ddd.PreparePointCloudTrainingData | defer — 深度学习训练数据准备管线 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Train Point Cloud Classification Model | 训练点云分类深度学习模型 | arcpy.ddd.TrainPointCloudClassificationModel | defer — 深度学习训练管线，单独注记 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |

### Point Cloud / Conversion toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| LAS To Multipoint | 把 LAS 点转为多点要素类 | arcpy.ddd.LASToMultipoint | core — 通用格式转换 | ArcPy GP（官方实现，桥直调） |
| LAS Dataset To TIN | 把 LAS 数据集转为 TIN 表面 | arcpy.ddd.LASDatasetToTIN | core — LAS 转 TIN 为基础表面处理 | ArcPy GP（官方实现，桥直调） |

### Point Cloud / Object Detection (Deep Learning) toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Detect Objects From Point Cloud Using Trained Model | 用已训练模型从点云中检测对象 | arcpy.ddd.DetectObjectsFromPointCloudUsingTrainedModel | defer — 深度学习点云检测管线，依赖已训练模型 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Train Point Cloud Object Detection Model | 训练点云对象检测深度学习模型 | arcpy.ddd.TrainPointCloudObjectDetectionModel | defer — 深度学习训练管线，单独注记 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |

### Raster / Conversion toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Raster Domain | 生成栅格数据范围的多边形轮廓 | arcpy.ddd.RasterDomain | core — 通用栅格范围提取 | ArcPy GP（官方实现，桥直调） |
| Raster to Multipoint | 把栅格像元中心转为多点要素 | arcpy.ddd.RasterToMultipoint | core — 通用栅格转矢量 | ArcPy GP（官方实现，桥直调） |
| Raster to TIN | 把栅格表面转为 TIN | arcpy.ddd.RasterToTIN | core — 栅格转 TIN 为基础表面处理 | ArcPy GP（官方实现，桥直调） |

### Raster / Interpolation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| IDW | 用反距离加权从采样点插值生成栅格面 | arcpy.ddd.IDW | core — 常用插值法（与 Spatial Analyst 同名工具） | ArcPy GP（官方实现，桥直调） |
| Kriging | 用克里金法从采样点插值生成栅格面 | arcpy.ddd.Kriging | core — 常用插值法 | ArcPy GP（官方实现，桥直调） |
| Natural Neighbor | 用自然邻域法从采样点插值生成栅格面 | arcpy.ddd.NaturalNeighbor | core — 常用插值法 | ArcPy GP（官方实现，桥直调） |
| Spline | 用样条法从采样点插值生成平滑面 | arcpy.ddd.Spline | core — 常用插值法 | ArcPy GP（官方实现，桥直调） |
| Spline with Barriers | 带障碍线的样条插值 | arcpy.ddd.SplineWithBarriers | extension — 带障碍样条为具体实现变体 | ArcPy GP（官方实现，桥直调） |
| Topo to Raster | 由地形要素插值出水文正确的 DEM | arcpy.ddd.TopoToRaster | extension — ANUDEM 算法为 ArcGIS 专属实现 | ArcPy GP（官方实现，桥直调） |
| Topo to Raster by File | 按参数文件批量执行 Topo to Raster | arcpy.ddd.TopoToRasterByFile | extension — 同 Topo to Raster，专属实现 | ArcPy GP（官方实现，桥直调） |
| Trend | 用多项式趋势面拟合采样点生成栅格 | arcpy.ddd.Trend | core — 常用趋势面插值 | ArcPy GP（官方实现，桥直调） |

### Raster / Math toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Divide | 逐像元两栅格相除 | arcpy.ddd.Divide | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Float | 逐像元把值转成浮点数 | arcpy.ddd.Float | core — 通用类型转换 | ArcPy GP（官方实现，桥直调） |
| Int | 逐像元截断取整 | arcpy.ddd.Int | core — 通用类型转换 | ArcPy GP（官方实现，桥直调） |
| Minus | 逐像元两栅格相减 | arcpy.ddd.Minus | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Plus | 逐像元两栅格相加 | arcpy.ddd.Plus | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Times | 逐像元两栅格相乘 | arcpy.ddd.Times | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |

### Raster / Reclass toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Lookup | 按另一栅格的属性字段查表赋新值 | arcpy.ddd.Lookup | core — 通用查表重分类 | ArcPy GP（官方实现，桥直调） |
| Reclass by ASCII File | 按 ASCII 重映射表重分类 | arcpy.ddd.ReclassByASCIIFile | core — 通用重分类 | ArcPy GP（官方实现，桥直调） |
| Reclass by Table | 按属性表重映射重分类 | arcpy.ddd.ReclassByTable | core — 通用重分类 | ArcPy GP（官方实现，桥直调） |
| Reclassify | 按映射表重分类栅格值 | arcpy.ddd.Reclassify | core — 重分类为通用栅格处理 | ArcPy GP（官方实现，桥直调） |
| Slice | 把栅格值切成若干等级区间 | arcpy.ddd.Slice | core — 通用分级切片 | ArcPy GP（官方实现，桥直调） |

### Raster / Surface toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Aspect | 由栅格 DEM 计算坡向 | arcpy.ddd.Aspect | core — 坡向为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Contour | 由栅格 DEM 生成等高线 | arcpy.ddd.Contour | core — 等高线为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Contour List | 按指定值列表生成等高线 | arcpy.ddd.ContourList | core — 通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Contour with Barriers | 带障碍生成等高线 | arcpy.ddd.ContourWithBarriers | extension — 带障碍等高线为具体实现 | ArcPy GP（官方实现，桥直调） |
| Curvature | 计算栅格表面曲率 | arcpy.ddd.Curvature | core — 曲率为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Hillshade | 由 DEM 生成山体阴影栅格 | arcpy.ddd.Hillshade | core — 山影为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Slope | 由栅格 DEM 计算坡度 | arcpy.ddd.Slope | core — 坡度为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Surface Parameters | 由 DEM 计算坡度/坡向/曲率等表面参数 | arcpy.ddd.SurfaceParameters | core — 表面参数为通用地形分析 | ArcPy GP（官方实现，桥直调） |

### Statistics toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Surface Information | 把表面 Z 值与坡度等写入要素属性 | arcpy.ddd.AddSurfaceInformation | core — 通用表面取值 | ArcPy GP（官方实现，桥直调） |
| Add Z Information | 计算并写入要素的 Z 相关几何属性（如长度/面积含 Z） | arcpy.ddd.AddZInformation | core — 通用三维几何属性 | ArcPy GP（官方实现，桥直调） |
| LAS Height Metrics | 由 LAS 计算植被/冠层等高度指标栅格 | arcpy.ddd.LASHeightMetrics | extension — LAS 高度指标为林业等专用统计 | ArcPy GP（官方实现，桥直调） |
| LAS Point Statistics By Area | 按区域统计 LAS 点的数量/高程等指标 | arcpy.ddd.LASPointStatisticsByArea | core — 点云分区统计为通用处理 | ArcPy GP（官方实现，桥直调） |
| Point File Information | 汇总点文件（LAS 等）的基本信息与范围 | arcpy.ddd.PointFileInformation | core — 通用元信息汇总 | ArcPy GP（官方实现，桥直调） |

### Terrain Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Feature Class To Terrain | 把要素类加入地形数据集作为数据源 | arcpy.ddd.AddFeatureClassToTerrain | extension — Terrain 为 ArcGIS 专属表面数据结构 | ArcPy GP（官方实现，桥直调） |
| Add Terrain Pyramid Level | 给地形数据集添加金字塔等级 | arcpy.ddd.AddTerrainPyramidLevel | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Append Terrain Points | 向地形数据源追加点 | arcpy.ddd.AppendTerrainPoints | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Build Terrain | 构建/重建地形数据集 | arcpy.ddd.BuildTerrain | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Change Terrain Reference Scale | 修改地形金字塔等级的参考比例尺 | arcpy.ddd.ChangeTerrainReferenceScale | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Change Terrain Resolution Bounds | 修改地形金字塔等级的分辨率范围 | arcpy.ddd.ChangeTerrainResolutionBounds | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Create Terrain | 在地理数据库中创建地形数据集 | arcpy.ddd.CreateTerrain | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Delete Terrain Points | 删除地形数据源中的点 | arcpy.ddd.DeleteTerrainPoints | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Remove Feature Class From Terrain | 从地形数据集移除要素类数据源 | arcpy.ddd.RemoveFeatureClassFromTerrain | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Remove Terrain Pyramid Level | 移除地形数据集的金字塔等级 | arcpy.ddd.RemoveTerrainPyramidLevel | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |
| Replace Terrain Points | 替换地形数据源中的点 | arcpy.ddd.ReplaceTerrainPoints | extension — Terrain 专属管理 | ArcPy GP（官方实现，桥直调） |

### Terrain Dataset / Conversion toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Terrain To Points | 把地形表面转为多点/点要素 | arcpy.ddd.TerrainToPoints | extension — Terrain 专属转换 | ArcPy GP（官方实现，桥直调） |
| Terrain to Raster | 把地形表面转为栅格 DEM | arcpy.ddd.TerrainToRaster | extension — Terrain 专属转换 | ArcPy GP（官方实现，桥直调） |
| Terrain to TIN | 把地形表面转为 TIN | arcpy.ddd.TerrainToTIN | extension — Terrain 专属转换 | ArcPy GP（官方实现，桥直调） |

### TIN Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Copy TIN | 复制 TIN 数据集 | arcpy.ddd.CopyTIN | core — TIN 基础管理 | ArcPy GP（官方实现，桥直调） |
| Create TIN | 由点/线/面要素创建 TIN 表面 | arcpy.ddd.CreateTIN | core — TIN 创建为基础表面处理，多家共有 | ArcPy GP（官方实现，桥直调） |
| Decimate TIN Nodes | 按容差抽稀 TIN 节点生成概化 TIN | arcpy.ddd.DecimateTINNodes | core — TIN 概化为基础处理 | ArcPy GP（官方实现，桥直调） |
| Delineate TIN Data Area | 按边长等规则修剪 TIN 数据区边界 | arcpy.ddd.DelineateTINDataArea | core — TIN 基础处理 | ArcPy GP（官方实现，桥直调） |
| Edit TIN | 向 TIN 添加/替换要素数据 | arcpy.ddd.EditTIN | core — TIN 基础编辑 | ArcPy GP（官方实现，桥直调） |

### TIN Dataset / Conversion toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| LandXML to TIN | 把 LandXML 表面转为 TIN | arcpy.ddd.LandXMLToTIN | core — 通用格式转换 | ArcPy GP（官方实现，桥直调） |
| TIN Domain | 生成 TIN 数据范围多边形 | arcpy.ddd.TINDomain | core — TIN 基础处理 | ArcPy GP（官方实现，桥直调） |
| TIN Edge | 把 TIN 边导出为线要素 | arcpy.ddd.TINEdge | core — TIN 基础导出 | ArcPy GP（官方实现，桥直调） |
| TIN Line | 把 TIN 中的断线导出为线要素 | arcpy.ddd.TINLine | core — TIN 基础导出 | ArcPy GP（官方实现，桥直调） |
| TIN Node | 把 TIN 节点导出为点要素 | arcpy.ddd.TINNode | core — TIN 基础导出 | ArcPy GP（官方实现，桥直调） |
| TIN Polygon Tag | 把 TIN 三角形标签导出为多边形 | arcpy.ddd.TINPolygonTag | core — TIN 基础导出 | ArcPy GP（官方实现，桥直调） |
| TIN To Raster | 把 TIN 按高程转为栅格 DEM | arcpy.ddd.TINToRaster | core — TIN 转栅格为基础表面处理 | ArcPy GP（官方实现，桥直调） |
| TIN Triangle | 把 TIN 三角形导出为多边形要素 | arcpy.ddd.TINTriangle | core — TIN 基础导出 | ArcPy GP（官方实现，桥直调） |

### Triangulated Surface toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Locate Outliers | 在 TIN/地形/LAS 表面中定位高程离群点 | arcpy.ddd.LocateOutliers | extension — 表面离群检测为具体实现 | ArcPy GP（官方实现，桥直调） |
| Surface Aspect | 由 TIN/地形/LAS 表面生成坡向（栅格或多边形） | arcpy.ddd.SurfaceAspect | core — 三角表面坡向为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Surface Contour | 由 TIN/地形/LAS 表面生成等高线 | arcpy.ddd.SurfaceContour | core — 三角表面等高线为通用地形分析 | ArcPy GP（官方实现，桥直调） |
| Surface Slope | 由 TIN/地形/LAS 表面生成坡度（栅格或多边形） | arcpy.ddd.SurfaceSlope | core — 三角表面坡度为通用地形分析 | ArcPy GP（官方实现，桥直调） |

### Visibility toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Construct Sight Lines | 由观察点与目标点构造视线段 | arcpy.ddd.ConstructSightLines | core — 视线构造为通用可见性分析 | ArcPy GP（官方实现，桥直调） |
| Geodesic Viewshed | 考虑地球曲率的大地可视域分析 | arcpy.ddd.GeodesicViewshed | core — 可视域为通用表面分析 | ArcPy GP（官方实现，桥直调）；同类能力另有 Esri 托管高程分析服务（ArcGIS REST） |
| Intervisibility | 判断观察点与目标点之间是否通视并标记 | arcpy.ddd.Intervisibility | core — 通视为通用可见性分析 | ArcPy GP（官方实现，桥直调） |
| Line of Sight | 沿视线采样表面生成通视剖面并判断遮挡 | arcpy.ddd.LineOfSight | core — 视线分析为通用可见性分析 | ArcPy GP（官方实现，桥直调） |
| Skyline | 从观察点生成天际线（可见轮廓）要素 | arcpy.ddd.Skyline | extension — 天际线为 ArcGIS 可见性套件 | ArcPy GP（官方实现，桥直调） |
| Skyline Barrier | 由天际线生成遮挡体多面体 | arcpy.ddd.SkylineBarrier | extension — 天际线衍生处理 | ArcPy GP（官方实现，桥直调） |
| Skyline Graph | 生成观察点可见天空比例的极坐标图数据 | arcpy.ddd.SkylineGraph | extension — 天际线图为具体实现 | ArcPy GP（官方实现，桥直调） |
| Sun Shadow Frequency | 统计一段时间内的日照/阴影频次栅格 | arcpy.ddd.SunShadowFrequency | extension — 日影频次为 ArcGIS 太阳阴影套件 | ArcPy GP（官方实现，桥直调） |
| Sun Shadow Volume | 生成指定时刻建筑等要素的阴影体多面体 | arcpy.ddd.SunShadowVolume | extension — 阴影体为具体实现 | ArcPy GP（官方实现，桥直调） |
| Observer Points | 生成能看到指定区域的观察点分布 | arcpy.ddd.ObserverPoints | core — 可视域逆向分析为通用表面分析 | ArcPy GP（官方实现，桥直调） |
| Viewshed | 计算观察点在表面上的可见区域 | arcpy.ddd.Viewshed | core — 可视域为通用表面分析 | ArcPy GP（官方实现，桥直调）；同类能力另有 Esri 托管高程分析服务（ArcGIS REST） |
| Visibility | 计算观察点可见性并输出视线信息 | arcpy.ddd.Visibility | core — 可见性为通用表面分析 | ArcPy GP（官方实现，桥直调） |

## Geostatistical Analyst toolbox（arcpy.ga）

工具集数：5 个；工具总数：35；所需扩展许可：Geostatistical Analyst license；官方定位：由点测量（或栅格/多边形质心）创建连续表面，用确定性与地统计方法可视化、分析并理解空间现象，并评估插值模型质量。

### Interpolation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Diffusion Interpolation With Barriers | 用基于热方程的核并以栅格/要素障碍重定义距离来插值生成表面 | arcpy.ga.DiffusionInterpolationWithBarriers | extension — 带障碍扩散插值为 ArcGIS 地统计实现 | ArcPy GP（官方实现，桥直调） |
| EBK Regression Prediction | 把经验贝叶斯克里金与解释变量栅格回归结合做预测 | arcpy.ga.EBKRegressionPrediction | defer — EBK 回归预测需模型标定与向导式拟合 | ArcPy GP（官方实现，桥直调） |
| Empirical Bayesian Kriging | 经验贝叶斯克里金：用重复模拟计入半变异函数估计误差做插值 | arcpy.ga.EmpiricalBayesianKriging | defer — EBK 为向导式地统计建模，需交互标定 | ArcPy GP（官方实现，桥直调） |
| Empirical Bayesian Kriging 3D | 用 EBK 方法对三维点插值，输出可按高程切片的 3D 地统计图层 | arcpy.ga.EmpiricalBayesianKriging3D | defer — EBK 3D 为向导式地统计建模 | ArcPy GP（官方实现，桥直调） |
| Global Polynomial Interpolation | 用全局多项式光滑曲面拟合采样点做插值 | arcpy.ga.GlobalPolynomialInterpolation | core — 全局多项式为通用确定性插值 | ArcPy GP（官方实现，桥直调） |
| IDW | 用反距离加权预测未采样位置的值 | arcpy.ga.IDW | core — IDW 为常用插值法，多家共有 | ArcPy GP（官方实现，桥直调） |
| IDW 3D | 用反距离加权对三维点插值并生成体素图层与 .nc 源文件 | arcpy.ga.IDW3D | extension — 3D 体素输出为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |
| Kernel Interpolation With Barriers | 用最短路距离绕过线障碍的移动窗口核插值 | arcpy.ga.KernelInterpolationWithBarriers | extension — 带障碍核插值为 ArcGIS 地统计实现 | ArcPy GP（官方实现，桥直调） |
| Local Polynomial Interpolation | 在重叠邻域内逐区拟合多项式做插值 | arcpy.ga.LocalPolynomialInterpolation | core — 局部多项式为通用确定性插值 | ArcPy GP（官方实现，桥直调） |
| Moving Window Kriging | 在移动小邻域内逐点重算半变异参数（Range/Nugget/Partial Sill）做克里金 | arcpy.ga.MovingWindowKriging | defer — 移动窗口克里金需半变异建模标定 | ArcPy GP（官方实现，桥直调） |
| Nearest Neighbor 3D | 给每个体素赋三维最近邻类别点的类别并生成 netCDF 体素源文件 | arcpy.ga.NearestNeighbor3D | extension — 3D 最近邻体素化为具体实现 | ArcPy GP（官方实现，桥直调） |
| Radial Basis Functions | 用五种径向基函数之一插值出精确通过采样点的表面 | arcpy.ga.RadialBasisFunctions | core — 径向基函数为通用确定性插值 | ArcPy GP（官方实现，桥直调） |

### Sampling Network Design toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Spatially Balanced Points | 按纳入概率生成空间均衡的采样点设计（可用概率栅格偏置选点） | arcpy.ga.CreateSpatiallyBalancedPoints | extension — 空间均衡抽样设计为 ArcGIS 实现 | ArcPy GP（官方实现，桥直调） |
| Densify Sampling Network | 用已拟合的克里金地统计图层决定新增/撤销监测站点 | arcpy.ga.DensifySamplingNetwork | defer — 依赖已标定的克里金模型图层 | ArcPy GP（官方实现，桥直调） |

### Simulation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Extract Values To Table | 按点或面要素把一组栅格的像元值提取成表 | arcpy.ga.ExtractValuesToTable | core — 通用栅格取值制表 | ArcPy GP（官方实现，桥直调） |
| Gaussian Geostatistical Simulations | 基于简单克里金模型做条件/无条件高斯地统计模拟，生成等概率实现栅格 | arcpy.ga.GaussianGeostatisticalSimulations | defer — 地统计模拟需模型标定后批量实现 | ArcPy GP（官方实现，桥直调） |

### Utilities toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Compare Geostatistical Layers | 按交叉验证统计的可定制准则比较并排序多个地统计图层 | arcpy.ga.CompareGeostatisticalLayers | defer — 模型比较属地统计建模标定环节 | ArcPy GP（官方实现，桥直调） |
| Cross Validation | 逐点留一预测并与实测比较以评估模型参数 | arcpy.ga.CrossValidation | core — 交叉验证为通用模型评估 | ArcPy GP（官方实现，桥直调） |
| Directional Trend | 在要素图层上生成指定方向的数据值趋势散点图（3.4 新增） | arcpy.ga.DirectionalTrend | defer — 趋势判读为插值建模前的交互探索；且官方注明需活动地图 | 仅桌面交互（需活动地图）；官方工具页注明不可用于独立脚本，无独立脚本入口 |
| Exploratory Interpolation | 自动生成多种插值结果并按交叉验证准则比较排序 | arcpy.ga.ExploratoryInterpolation | defer — 自动选模属向导式建模标定 | ArcPy GP（官方实现，桥直调） |
| Generate Subset Polygons | 把点集划分为紧凑不重叠子集并生成子集多边形（供 EBK 回归预测分块） | arcpy.ga.GenerateSubsetPolygons | extension — 为 EBK 回归预测配套的专属预处理 | ArcPy GP（官方实现，桥直调） |
| Neighborhood Selection | 按用户定义邻域生成点图层（显示插值邻域） | arcpy.ga.NeighborhoodSelection | extension — 地统计邻域可视化配套工具 | ArcPy GP（官方实现，桥直调） |
| Semivariogram Sensitivity | 在原值百分比范围内变动半变异参数做预测与标准误的敏感性分析 | arcpy.ga.SemivariogramSensitivity | defer — 半变异参数敏感性属模型标定环节 | ArcPy GP（官方实现，桥直调） |
| Subset Features | 把数据集分成建模训练子集与验证子集两部分 | arcpy.ga.SubsetFeatures | core — 训练/验证划分是通用建模流程 | ArcPy GP（官方实现，桥直调） |

### Working with Geostatistical Layers toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Areal Interpolation Layer To Polygons | 把面插值图层的预测重新聚合到一组新多边形上 | arcpy.ga.ArealInterpolationLayerToPolygons | extension — 面插值为 ArcGIS 地统计专属对象体系 | ArcPy GP（官方实现，桥直调） |
| Calculate Z Value | 用地统计图层的插值模型预测单个位置的值 | arcpy.ga.CalculateZValue | extension — 依赖地统计图层对象 | ArcPy GP（官方实现，桥直调） |
| Create Geostatistical Layer | 以已有地统计图层/模型为初值创建新的地统计图层 | arcpy.ga.CreateGeostatisticalLayer | extension — 地统计图层为 ArcGIS 专属对象 | ArcPy GP（桥直调；初始模型可由地统计向导 Geostatistical Wizard 交互生成） |
| GA Layer 3D To Multidimensional Raster | 把 EBK 3D 地统计图层导出为多维 CRF 栅格 | arcpy.ga.GALayer3DToMultidimensionalRaster | extension — 依赖地统计图层与 CRF 格式 | ArcPy GP（官方实现，桥直调） |
| GA Layer 3D To NetCDF | 把一个或多个 EBK 3D 地统计图层导出为 netCDF 以便做体素图层 | arcpy.ga.GALayer3DToNetCDF | extension — 地统计图层专属导出 | ArcPy GP（官方实现，桥直调） |
| GA Layer To Contour | 由地统计图层生成等值线或填充等值面要素 | arcpy.ga.GALayerToContour | extension — 地统计图层专属导出 | ArcPy GP（官方实现，桥直调） |
| GA Layer To Grid | 把地统计图层导出为栅格 | arcpy.ga.GALayerToGrid | extension — 地统计图层专属导出 | ArcPy GP（官方实现，桥直调） |
| GA Layer To Points | 把地统计图层导出为点（可预测未测点或验证已测点） | arcpy.ga.GALayerToPoints | extension — 地统计图层专属导出 | ArcPy GP（官方实现，桥直调） |
| GA Layer To Rasters | 把地统计图层导出为一个或多个栅格 | arcpy.ga.GALayerToRasters | extension — 地统计图层专属导出 | ArcPy GP（官方实现，桥直调） |
| Get Model Parameter | 从已有地统计模型源读取模型参数值（XML） | arcpy.ga.GetModelParameter | extension — 地统计模型参数体系专属 | ArcPy GP（官方实现，桥直调） |
| Set Model Parameter | 在已有地统计模型源中设置模型参数值（XML） | arcpy.ga.SetModelParameter | extension — 地统计模型参数体系专属 | ArcPy GP（官方实现，桥直调） |

## Image Analyst toolbox（arcpy.ia）

工具集数：13 个一级 toolset（本表展开 16 组）；工具总数：119；所需扩展许可：Image Analyst license；官方定位：为影像分析提供工具，覆盖影像分类与模式识别、深度学习、变化检测、SAR 与全动态视频、多维分析等。

### Change Detection toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze Changes Using CCDC | 用 CCDC 连续变化检测算法评估像元值随时间的变化并生成变化分析栅格 | arcpy.ia.AnalyzeChangesUsingCCDC | extension — CCDC 时序算法的 ArcGIS 实现 | ArcPy GP（官方实现，桥直调） |
| Analyze Changes Using LandTrendr | 用 LandTrendr 算法评估像元值随时间的变化并生成变化分析栅格 | arcpy.ia.AnalyzeChangesUsingLandTrendr | extension — LandTrendr 时序算法的 ArcGIS 实现 | ArcPy GP（官方实现，桥直调） |
| Compute Change Raster | 计算两个栅格之间的绝对/相对/类别/光谱差异 | arcpy.ia.ComputeChangeRaster | core — 变化检测为通用遥感处理 | ArcPy GP（官方实现，桥直调） |
| Detect Change Using Change Analysis Raster | 由 CCDC/LandTrendr 的变化分析栅格生成像元变化信息栅格 | arcpy.ia.DetectChangeUsingChangeAnalysisRaster | extension — 依赖 ArcGIS 变化分析栅格产物 | ArcPy GP（官方实现，桥直调） |

### Classification and Pattern Recognition toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Classify Raster | 按 Esri 分类器定义文件（.ecd）对栅格分类 | arcpy.ia.ClassifyRaster | extension — 依赖 .ecd 分类器定义格式 | ArcPy GP（官方实现，桥直调） |
| Compute Confusion Matrix | 计算分类图与参考数据的混淆矩阵、漏分/错分及 Kappa/IoU/总体精度 | arcpy.ia.ComputeConfusionMatrix | core — 精度评价为通用流程 | ArcPy GP（官方实现，桥直调） |
| Compute Segment Attributes | 计算分割影像各对象的属性集 | arcpy.ia.ComputeSegmentAttributes | core — 面向对象分类通用步骤 | ArcPy GP（官方实现，桥直调） |
| Create Accuracy Assessment Points | 随机采样生成分类后精度评价点 | arcpy.ia.CreateAccuracyAssessmentPoints | core — 精度评价为通用流程 | ArcPy GP（官方实现，桥直调） |
| Generate Training Samples From Seed Points | 由种子点（如主题栅格/要素）生成训练样本 | arcpy.ia.GenerateTrainingSamplesFromSeedPoints | core — 训练样本生成为通用分类流程 | ArcPy GP（官方实现，桥直调） |
| Inspect Training Samples | 用 .ecd 分类结果交叉验证评估单个训练样本精度 | arcpy.ia.InspectTrainingSamples | extension — 依赖 .ecd 训练结果体系 | ArcPy GP（官方实现，桥直调） |
| Linear Spectral Unmixing | 亚像元分解计算各端元在像元中的丰度 | arcpy.ia.LinearSpectralUnmixing | core — 光谱解混为通用遥感方法 | ArcPy GP（官方实现，桥直调） |
| Predict Using Regression Model | 用随机森林回归模型输出预测数据值 | arcpy.ia.PredictUsingRegressionModel | extension — 依赖 ArcGIS 回归模型产物 | ArcPy GP（官方实现，桥直调） |
| Remove Raster Segment Tiling Artifacts | 修正分割时瓦片边界对象被切断的伪影 | arcpy.ia.RemoveRasterSegmentTilingArtifacts | extension — 分割瓦片伪影修正为具体实现 | ArcPy GP（官方实现，桥直调） |
| Segment Mean Shift | 用均值漂移把光谱相似邻近像元聚成对象（分割） | arcpy.ia.SegmentMeanShift | core — 均值漂移分割为通用 OBIA 方法 | ArcPy GP（官方实现，桥直调） |
| Train Iso Cluster Classifier | 训练 Iso Cluster 分类器并输出 .ecd | arcpy.ia.TrainIsoClusterClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Train K-Nearest Neighbor Classifier | 训练 K 近邻分类器并输出 .ecd | arcpy.ia.TrainKNearestNeighborClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Train Maximum Likelihood Classifier | 训练最大似然分类器并输出 .ecd | arcpy.ia.TrainMaximumLikelihoodClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Train Random Trees Classifier | 训练随机森林分类器并输出 .ecd | arcpy.ia.TrainRandomTreesClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Train Random Trees Regression Model | 用随机森林建模解释变量与目标数据的回归关系 | arcpy.ia.TrainRandomTreesRegressionModel | extension — ArcGIS 回归建模实现 | ArcPy GP（官方实现，桥直调） |
| Train Support Vector Machine Classifier | 训练支持向量机分类器并输出 .ecd | arcpy.ia.TrainSupportVectorMachineClassifier | extension — 输出 Esri 专属 .ecd 格式 | ArcPy GP（官方实现，桥直调） |
| Update Accuracy Assessment Points | 更新精度评价点 Target 字段以与分类图对比 | arcpy.ia.UpdateAccuracyAssessmentPoints | core — 精度评价为通用流程 | ArcPy GP（官方实现，桥直调） |

### Deep Learning toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Classify Objects Using Deep Learning | 用已训练深度学习模型对栅格及可选对象逐个赋类别标签 | arcpy.ia.ClassifyObjectsUsingDeepLearning | defer — 深度学习推理管线，依赖已训练模型 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Classify Pixels Using Deep Learning | 用已训练深度学习模型逐像元分类生成分类栅格 | arcpy.ia.ClassifyPixelsUsingDeepLearning | defer — 深度学习推理管线，依赖已训练模型 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Compute Accuracy For Object Detection | 把目标检测结果与真值比较计算检测精度 | arcpy.ia.ComputeAccuracyForObjectDetection | defer — 深度学习模型评估管线 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Detect Change Using Deep Learning | 用已训练深度学习模型检测两栅格之间的变化 | arcpy.ia.DetectChangeUsingDeepLearning | defer — 深度学习推理管线，依赖已训练模型 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Detect Objects Using Deep Learning | 用已训练深度学习模型在栅格中检测对象并输出框/面/点要素 | arcpy.ia.DetectObjectsUsingDeepLearning | defer — 深度学习推理管线，依赖已训练模型 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Export Training Data For Deep Learning | 把标注矢量/栅格转为深度学习训练样本切片与元数据 | arcpy.ia.ExportTrainingDataForDeepLearning | defer — 深度学习训练管线前置步骤 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Non Maximum Suppression | 对目标检测输出做非极大值抑制去重 | arcpy.ia.NonMaximumSuppression | defer — 深度学习检测后处理管线 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |
| Train Deep Learning Model | 用导出训练数据训练深度学习模型 | arcpy.ia.TrainDeepLearningModel | defer — 深度学习训练管线，单独注记 | ArcPy GP（官方实现，桥直调；基于 Esri 深度学习框架/模型包） |

### Extraction toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Sample | 在指定位置生成栅格像元值表或点要素 | arcpy.ia.Sample | core — 通用采样取值 | ArcPy GP（官方实现，桥直调） |

### Interpolation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Interpolate From Spatiotemporal Points | 把时空点数据插值成多维栅格 | arcpy.ia.InterpolateFromSpatiotemporalPoints | extension — 时空插值为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |
| Optimal Interpolation | 统计同化多源数据（背景场+观测）生成插值栅格 | arcpy.ia.OptimalInterpolation | extension — 最优同化插值为 ArcGIS 具体实现 | ArcPy GP（官方实现，桥直调） |

### Map Algebra toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Raster Calculator | 用地图代数表达式计算生成输出栅格 | arcpy.ia.RasterCalculator | core — 栅格计算为平台核心能力 | ArcPy GP（官方实现，桥直调） |

### Math (general) toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Abs | 逐像元取绝对值 | arcpy.ia.Abs | core — 通用栅格数学运算（与 SA 同名工具） | ArcPy GP（官方实现，桥直调） |
| Divide | 逐像元两栅格相除 | arcpy.ia.Divide | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Exp | 逐像元计算 e 的幂 | arcpy.ia.Exp | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Exp10 | 逐像元计算 10 的幂 | arcpy.ia.Exp10 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Exp2 | 逐像元计算 2 的幂 | arcpy.ia.Exp2 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Float | 逐像元把值转成浮点数 | arcpy.ia.Float | core — 通用类型转换 | ArcPy GP（官方实现，桥直调） |
| Int | 逐像元截断取整 | arcpy.ia.Int | core — 通用类型转换 | ArcPy GP（官方实现，桥直调） |
| Ln | 逐像元取自然对数 | arcpy.ia.Ln | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Log10 | 逐像元取以 10 为底对数 | arcpy.ia.Log10 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Log2 | 逐像元取以 2 为底对数 | arcpy.ia.Log2 | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Minus | 逐像元两栅格相减 | arcpy.ia.Minus | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Mod | 逐像元求除法余数 | arcpy.ia.Mod | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Negate | 逐像元取相反数 | arcpy.ia.Negate | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Plus | 逐像元两栅格相加 | arcpy.ia.Plus | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Power | 逐像元以另一栅格为指数做幂运算 | arcpy.ia.Power | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Round Down | 逐像元向下取整（以浮点表示） | arcpy.ia.RoundDown | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Round Up | 逐像元向上取整（以浮点表示） | arcpy.ia.RoundUp | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Square | 逐像元求平方 | arcpy.ia.Square | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Square Root | 逐像元求平方根 | arcpy.ia.SquareRoot | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |
| Times | 逐像元两栅格相乘 | arcpy.ia.Times | core — 通用栅格数学运算 | ArcPy GP（官方实现，桥直调） |

### Math Conditional toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Con | 逐像元按条件做 if/else 取值 | arcpy.ia.Con | core — 通用条件运算 | ArcPy GP（官方实现，桥直调） |
| Pick | 按位置栅格从多个输入中逐像元挑选取值 | arcpy.ia.Pick | core — 通用条件运算 | ArcPy GP（官方实现，桥直调） |
| Set Null | 满足条件处设为 NoData、其余保留指定值 | arcpy.ia.SetNull | core — 通用 NoData 处理 | ArcPy GP（官方实现，桥直调） |

### Math Logical toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Bitwise And | 逐像元对两栅格做按位与 | arcpy.ia.BitwiseAnd | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Left Shift | 逐像元做按位左移 | arcpy.ia.BitwiseLeftShift | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Not | 逐像元做按位取反 | arcpy.ia.BitwiseNot | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Or | 逐像元对两栅格做按位或 | arcpy.ia.BitwiseOr | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise Right Shift | 逐像元做按位右移 | arcpy.ia.BitwiseRightShift | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Bitwise XOr | 逐像元对两栅格做按位异或 | arcpy.ia.BitwiseXOr | core — 通用位运算 | ArcPy GP（官方实现，桥直调） |
| Boolean And | 逐像元做布尔与 | arcpy.ia.BooleanAnd | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Boolean Not | 逐像元做布尔非 | arcpy.ia.BooleanNot | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Boolean Or | 逐像元做布尔或 | arcpy.ia.BooleanOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Boolean XOr | 逐像元做布尔异或 | arcpy.ia.BooleanXOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Combinatorial And | 逐像元组合与：两值皆真时输出唯一组合值 | arcpy.ia.CombinatorialAnd | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Combinatorial Or | 逐像元组合或：任一为真时输出唯一组合值 | arcpy.ia.CombinatorialOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Combinatorial XOr | 逐像元组合异或：恰一为真时输出唯一组合值 | arcpy.ia.CombinatorialXOr | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Diff | 逐像元比较两栅格，不同输出第一栅格值、相同输出 0 | arcpy.ia.Diff | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Equal To | 逐像元判断两栅格是否相等（1/0） | arcpy.ia.EqualTo | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Greater Than | 逐像元判断是否大于（1/0） | arcpy.ia.GreaterThan | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Greater Than Equal | 逐像元判断是否大于等于（1/0） | arcpy.ia.GreaterThanEqual | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| InList | 逐像元判断值是否出现在其他栅格列表中 | arcpy.ia.InList | core — 通用逻辑运算（许可页工具名为 InList） | ArcPy GP（官方实现，桥直调） |
| Is Null | 逐像元判断是否为 NoData（1/0） | arcpy.ia.IsNull | core — 通用 NoData 判断 | ArcPy GP（官方实现，桥直调） |
| Less Than | 逐像元判断是否小于（1/0） | arcpy.ia.LessThan | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Less Than Equal | 逐像元判断是否小于等于（1/0） | arcpy.ia.LessThanEqual | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Not Equal | 逐像元判断是否不相等（1/0） | arcpy.ia.NotEqual | core — 通用关系运算 | ArcPy GP（官方实现，桥直调） |
| Over | 逐像元以第一栅格非零值覆盖、为零处取第二栅格值 | arcpy.ia.Over | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |
| Test | 逐像元按逻辑表达式求值输出 1/0 | arcpy.ia.Test | core — 通用逻辑运算 | ArcPy GP（官方实现，桥直调） |

### Math Trigonometric toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| ACos | 逐像元计算反余弦 | arcpy.ia.ACos | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ACosH | 逐像元计算反双曲余弦 | arcpy.ia.ACosH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ASin | 逐像元计算反正弦 | arcpy.ia.ASin | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ASinH | 逐像元计算反双曲正弦 | arcpy.ia.ASinH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ATan | 逐像元计算反正切 | arcpy.ia.ATan | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ATan2 | 逐像元计算反正切类函数（官方完整清单页描述为反双曲正切口径，以工具页为准） | arcpy.ia.ATan2 | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| ATanH | 逐像元计算反双曲正切 | arcpy.ia.ATanH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| Cos | 逐像元计算余弦 | arcpy.ia.Cos | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| CosH | 逐像元计算双曲余弦 | arcpy.ia.CosH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| Sin | 逐像元计算正弦 | arcpy.ia.Sin | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| SinH | 逐像元计算双曲正弦 | arcpy.ia.SinH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| Tan | 逐像元计算正切 | arcpy.ia.Tan | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |
| TanH | 逐像元计算双曲正切 | arcpy.ia.TanH | core — 通用三角运算 | ArcPy GP（官方实现，桥直调） |

### Motion Imagery toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Extract Video Frames To Images | 从 FMV 合规视频流提取帧图像与元数据到目录 | arcpy.ia.ExtractVideoFramesToImages | extension — 全动态视频（FMV）为 Image Analyst 专属工作流 | ArcPy GP（官方实现，桥直调）（FMV 全动态视频工作流） |
| Video Metadata To Feature Class | 提取 FMV 视频的平台/帧中心/帧轮廓等元数据为要素 | arcpy.ia.VideoMetadataToFeatureClass | extension — FMV 专属处理 | ArcPy GP（官方实现，桥直调）（FMV 全动态视频工作流） |
| Video Multiplexer | 把存档视频流与元数据文件按时间戳同步复合成视频文件 | arcpy.ia.VideoMultiplexer | extension — FMV 专属处理 | ArcPy GP（官方实现，桥直调）（FMV 全动态视频工作流） |

### Multidimensional Analysis toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Aggregate Multidimensional Raster | 沿维度组合多维栅格变量生成新的多维栅格 | arcpy.ia.AggregateMultidimensionalRaster | core — 多维栅格聚合为通用处理 | ArcPy GP（官方实现，桥直调） |
| Dimensional Moving Statistics | 沿指定维度对多维数据做移动窗口统计 | arcpy.ia.DimensionalMovingStatistics | core — 多维栅格统计为通用处理 | ArcPy GP（官方实现，桥直调） |
| Find Argument Statistics | 提取多维/多波段栅格中某统计量取得时的维度值或波段序号 | arcpy.ia.FindArgumentStatistics | core — 参数统计为通用多维处理 | ArcPy GP（官方实现，桥直调） |
| Generate Multidimensional Anomaly | 逐切片计算多维栅格距平 | arcpy.ia.GenerateMultidimensionalAnomaly | core — 距平计算为通用处理 | ArcPy GP（官方实现，桥直调） |
| Generate Trend Raster | 沿维度估计每像元的趋势生成趋势栅格 | arcpy.ia.GenerateTrendRaster | core — 趋势估计为通用多维处理 | ArcPy GP（官方实现，桥直调） |
| Multidimensional Principal Components | 对多维栅格做主成分降维以识别时空格局 | arcpy.ia.MultidimensionalPrincipalComponents | core — PCA 为通用降维 | ArcPy GP（官方实现，桥直调） |
| Predict Using Trend Raster | 用趋势栅格计算预测多维栅格 | arcpy.ia.PredictUsingTrendRaster | core — 趋势预测为通用多维处理 | ArcPy GP（官方实现，桥直调） |
| Summarize Categorical Raster | 统计分类栅格每切片中各类别的像元数成表 | arcpy.ia.SummarizeCategoricalRaster | core — 类别统计为通用处理 | ArcPy GP（官方实现，桥直调） |

### Overlay toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Weighted Sum | 多栅格乘权重后逐像元求和 | arcpy.ia.WeightedSum | core — 通用加权叠加 | ArcPy GP（官方实现，桥直调） |

### Statistical toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Cell Statistics | 逐像元对多个栅格做统计 | arcpy.ia.CellStatistics | core — 通用逐像元统计 | ArcPy GP（官方实现，桥直调） |
| Focal Statistics | 在指定邻域内逐像元计算统计量 | arcpy.ia.FocalStatistics | core — 通用邻域统计 | ArcPy GP（官方实现，桥直调） |
| Zonal Statistics | 按分区统计值栅格输出栅格 | arcpy.ia.ZonalStatistics | core — 通用分区统计 | ArcPy GP（官方实现，桥直调） |
| Zonal Statistics as Table | 按分区统计值栅格并输出为表 | arcpy.ia.ZonalStatisticsAsTable | core — 通用分区统计 | ArcPy GP（官方实现，桥直调） |

### Synthetic Aperture Radar toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Apply Geometric Terrain Correction | 用距离-多普勒后向地理编码对 SAR 数据做正射校正 | arcpy.ia.ApplyGeometricTerrainCorrection | extension — SAR 处理链的 ArcGIS 实现（同类链见 SNAP） | ArcPy GP（官方实现，桥直调） |
| Apply Orbit Correction | 用更精确的轨道状态向量文件更新 Sentinel-1 SAR 轨道信息 | arcpy.ia.ApplyOrbitCorrection | extension — Sentinel-1 专属处理链 | ArcPy GP（官方实现，桥直调） |
| Apply Radiometric Calibration | 把 SAR 反射率按参考面归一化为物理后向散射量 | arcpy.ia.ApplyRadiometricCalibration | extension — SAR 处理链的 ArcGIS 实现 | ArcPy GP（官方实现，桥直调） |
| Apply Radiometric Terrain Flattening | 校正地形引起的 SAR 辐射畸变 | arcpy.ia.ApplyRadiometricTerrainFlattening | extension — SAR 处理链的 ArcGIS 实现 | ArcPy GP（官方实现，桥直调） |
| Convert SAR Units | 转换 SAR 数据的标度单位 | arcpy.ia.ConvertSARUnits | extension — SAR 专属处理 | ArcPy GP（官方实现，桥直调） |
| Create Color Composite | 由多波段栅格生成三波段彩色合成栅格 | arcpy.ia.CreateColorComposite | core — 彩色合成为通用栅格处理（许可页列于 SAR 工具集） | ArcPy GP（官方实现，桥直调） |
| Despeckle | 校正 SAR 相干斑噪声（颗粒/椒盐效应） | arcpy.ia.Despeckle | extension — SAR 去斑为 SAR 处理链环节 | ArcPy GP（官方实现，桥直调） |
| Download Orbit File | 下载 Sentinel-1 SAR 的更新轨道文件 | arcpy.ia.DownloadOrbitFile | extension — Sentinel-1 专属配套 | ArcPy GP（官方实现，桥直调） |
| Remove Thermal Noise | 校正 SAR 热噪声引起的后向散射扰动使影像更无缝 | arcpy.ia.RemoveThermalNoise | extension — SAR 处理链环节 | ArcPy GP（官方实现，桥直调） |

### Utilities toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Binary Mask | 由影像及衍生产品生成二值掩膜（预/后处理工具） | arcpy.ia.CreateBinaryMask | extension — 影像预处理配套工具（完整清单页 Utilities 唯一工具） | ArcPy GP（官方实现，桥直调） |

## 普查小结与口径说明

- 工具条数：Spatial Analyst 221 条；3D Analyst 138 条（已去重跨 toolset 重复列名：LAS Building Multipatch 同时列于 3D Features 与 Extraction、Prepare Point Cloud Training Data 同时列于两个点云深度学习分组，各只计一次）；Geostatistical Analyst 35 条；Image Analyst 119 条；**合计 513 条**。其中平台判断为 core 的共 **330 条**。
- 工具集数口径：Spatial Analyst 按 3.4 完整清单的分组行计 25 组（Math 含 general/Bitwise/Logical/Trigonometric 4 个子组、Distance (Legacy) 单列；官方清单页自述为 24 个 toolset、200+ 工具）；3D Analyst 一级 toolset 为 11 个、本表按许可页层级展开为 24 组（含 Point Cloud / Raster / Terrain / TIN 下的子组）；Geostatistical Analyst 为 5 个 toolset；Image Analyst 一级 toolset 为 13 个、本表把 Math 展开为 general/Conditional/Logical/Trigonometric 4 组、共列 16 组。
- Image Analyst 版本口径：本表以许可页工具清单（116 条）为基线，加 Interpolation 总览页的 2 条与 Utilities 的 Create Binary Mask 1 条，共 119 条。官方最新（3.5+）完整清单中另有 Spectral Analysis 工具集、扩展后的 SAR/InSAR 工具（如 Apply Coregistration、Generate Interferogram、Unwrap Phase 等）与新增深度学习工具（如 Train Using AutoDL、Extract Features Using AI Models 等），不属于 3.4 口径，未计入；后续若平台锚点升版，应整箱按新版完整清单重普查。
- 个别工具名注记：Spatial Analyst 的 ATan2 在 IA 官方完整清单页中描述文字与 ATanH 雷同，疑为官方页笔误，本表已注明以工具页为准；Segmentation and Classification 中的 Train Maximum Likelihood 一名在 3.4 清单页显示为截断文本，本表按同箱命名规律与 Image Analyst 同名工具写作 Train Maximum Likelihood Classifier 并已在该行注明。
- 轮子来源总口径：四箱工具均为地理处理工具，官方工具参考逐条给出 ArcPy 语法，默认复用通道即「ArcPy GP 桥直调」；同一 GP 工具可按官方发布流程发布为 ArcGIS Enterprise 地理处理服务（REST），或经 arcgis Python API 调用已发布服务——这两条是平台级的统一备选通道，故不逐行重复标注，只在个别已有 Esri 托管等价服务（如高程分析、ArcGIS Online 水文托管工具）的行内注明。

## 附：Esri 官方智能体 / MCP 入口（单独标出）

- **MCP for ArcGIS Location Services (beta)** — Esri 官方托管的 Model Context Protocol 服务器，官方说明称可让应用与 AI 智能体通过标准化 MCP 工具访问 ArcGIS Location Services（底图样式/静态底图/静态地图、Places、地理编码、路径、GeoEnrichment、Elevation 等），无需直接调用 ArcGIS REST API；需 ArcGIS Location Platform 或 ArcGIS Online 账户。链接：https://developers.arcgis.com/ai/mcp-arcgis-location-services/ 。对本平台的意义：这是 Esri 官方唯一的托管 MCP 入口，可作位置服务类能力的现成轮子；但它覆盖的是 Location Services，不覆盖本表四箱的栅格/表面 GP 工具，栅格侧仍走 ArcPy GP / 自行发布 REST GP 服务。
- **ArcGIS Maps SDK for JavaScript 的 AI 组件（agentic mapping applications）** — 官方 `@arcgis/ai-components` 提供 `arcgis-assistant` 聊天组件与开箱智能体（Navigation agent、Data exploration agent、Help agent、Knowledge agent），支持自然语言驱动地图导航、属性/空间/统计查询与知识图谱探索；属前端 Web 地图智能体，不替代后端 GP。链接：https://developers.arcgis.com/javascript/latest/agentic-apps/ai-introduction/
- **ArcGIS Pro assistant (beta)** — Esri 官方介绍（ArcNews）称该助手可在 ArcGIS Pro 内查文档、生成 ArcPy 代码与 SQL、并以自然语言触发常用动作；当时为 private beta、仅邀约（Early Adopter Community）。它与本平台的桥定位相邻：若后续开放，可评估作为桌面端官方智能体入口而非自研。链接：https://www.esri.com/about/newsroom/arcnews/ai-assistants-in-arcgis-provide-practical-help-and-give-useful-results
- 社区/第三方 MCP（如社区 arcgis-portal-mcp、伙伴 SkyFi MCP Server 等）在官方文档与 Esri 站点亦有出现，但非 Esri 官方实现，未列为官方轮子，仅在此注明存在、采用前需单独审查。

## 官方来源（均为 pro.arcgis.com / developers.arcgis.com / esri.com）

- Spatial Analyst：A complete listing of the Spatial Analyst tools（ArcGIS Pro 3.4）及各 toolset 总览页（An overview of the … toolset）。
- 3D Analyst：An overview of the 3D Analyst toolbox；3D Analyst toolbox licensing（ArcGIS Pro 3.4）。
- Geostatistical Analyst：An overview of the Geostatistical Analyst toolbox 及 Interpolation / Sampling Network Design / Simulation / Utilities / Working with Geostatistical Layers 五个 toolset 总览页；Directional Trend 工具页（ArcGIS Pro 3.4）。
- Image Analyst：An overview of the Image Analyst toolbox（3.3/3.4 线）；Image Analyst toolbox licensing；An overview of the Interpolation toolset (Image Analyst)；List of ArcGIS Image Analyst geoprocessing tools（仅用于核对作用描述与 Utilities 工具，新增工具按版本口径剔除，见上）。
- 智能体/MCP：MCP for ArcGIS Location Services (beta)（developers.arcgis.com）；Intro to building agentic mapping applications（developers.arcgis.com）；AI Assistants in ArcGIS（esri.com ArcNews）。


> GIS 综合平台能力底账 · 分节文件。证据：ArcGIS Pro 3.4 工具参考官方文档（pro.arcgis.com）各工具箱总览页与各 toolset 总览页逐条抄录，2026-11-02 核查；个别 toolset 页官方 3.4 路径未单列时以官方现行（latest/3.3）同名总览页补齐并在节内注明。
> 平台升级原则（鱼鱼定）：全部升级＋不重复造轮子——平台层只做翻译与治理、不自研算法；每条工具的「轮子来源」即官方现成可复用通道。
> 平台判断口径：core＝概念层通用、多家共有，平台应纳为能力；extension＝ArcGIS 专属格式/数据模型/实现，平台只做适配；defer＝依赖门户/在线账号与额度或分布式服务器运维，暂缓落地（概念归属在理由中注明）。
> ArcPy 入口函数名按官方工具名 CamelCase 规则写作 `arcpy.<模块>.<函数>`；模块名经 ArcGIS Pro 3.4《ArcPy modules》官方页核对。

## Network Analyst toolbox（arcpy.na / arcpy.nax）
工具集数：3；工具总数：32；运行前提：桌面扩展——需 ArcGIS Network Analyst 扩展授权，本地网络数据集在桌面运行；分析图层亦可改指 ArcGIS Online 或门户的路径服务作网络数据源，此时 Solve 按 ArcGIS Online credits 计费。官方定位：维护对交通网络建模的网络数据集，并用这些网络执行各类交通网络分析。

### Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Field To Analysis Layer | 给网络分析图层的子图层添加字段 | arcpy.na.AddFieldToAnalysisLayer | extension（NA 分析图层结构专属装配） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Add Locations | 把输入要素/记录装载到网络分析图层的停靠点、障碍等子图层并计算网络位置 | arcpy.na.AddLocations | extension（NA 图层装载机制专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Add Vehicle Routing Problem Breaks | 为 VRP 图层创建休息时段（breaks） | arcpy.na.AddVehicleRoutingProblemBreaks | extension（VRP 图层装配专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Add Vehicle Routing Problem Routes | 为 VRP 或末端配送图层的 Routes 子图层追加车辆路线行 | arcpy.na.AddVehicleRoutingProblemRoutes | extension（VRP 图层装配专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Calculate Locations | 把输入要素定位到网络上并写入网络位置字段，供分析时预计算提速 | arcpy.na.CalculateLocations | extension（网络位置字段为 NA 专属格式） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Copy Network Analysis Layer | 复制网络分析图层及其全部分析设置与数据 | arcpy.na.CopyNetworkAnalysisLayer | extension（NA 图层对象专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Copy Traversed Source Features | 导出求解时实际遍历的边、交汇点与转向为要素类和表 | arcpy.na.CopyTraversedSourceFeatures | extension（NA 求解内部结构专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Delete Network Analysis Layer | 删除网络分析图层及其分析数据 | arcpy.na.DeleteNetworkAnalysisLayer | extension（NA 图层对象专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Directions | 从带路线的分析图层生成逐转向驾驶指引（文本/XML/HTML） | arcpy.na.Directions | core（导航指引为通用能力） | ArcPy GP（arcpy.na）＋arcpy.nax 求解结果对象 |
| Make Closest Facility Analysis Layer | 创建最近设施分析图层并设置其属性，按出行模式找离事件最近的设施 | arcpy.na.MakeClosestFacilityAnalysisLayer | core（最近设施为通用网络分析概念） | ArcPy GP（arcpy.na）＋arcpy.nax；图层可改指 Online/门户路径服务 |
| Make Last Mile Delivery Analysis Layer | 创建末端配送分析图层，用车队优化一组配送路线 | arcpy.na.MakeLastMileDeliveryAnalysisLayer | core（末端配送优化通用） | ArcPy GP（arcpy.na）＋arcpy.nax；图层可改指 Online/门户路径服务 |
| Make Location-Allocation Analysis Layer | 创建选址-分配分析图层，从候选设施中选最优组合分配需求 | arcpy.na.MakeLocationAllocationAnalysisLayer | core（选址分配通用） | ArcPy GP（arcpy.na）＋arcpy.nax；图层可改指 Online/门户路径服务 |
| Make OD Cost Matrix Analysis Layer | 创建 OD 成本矩阵分析图层，表征起点到终点的成本矩阵 | arcpy.na.MakeODCostMatrixAnalysisLayer | core（OD 矩阵通用） | ArcPy GP（arcpy.na）＋arcpy.nax；图层可改指 Online/门户路径服务 |
| Make Route Analysis Layer | 创建路径分析图层，按指定网络成本求一组停靠点之间的最佳路线 | arcpy.na.MakeRouteAnalysisLayer | core（最短/最优路径通用） | ArcPy GP（arcpy.na）＋arcpy.nax；图层可改指 Online/门户路径服务 |
| Make Service Area Analysis Layer | 创建服务区分析图层，求设施在给定成本阈值内的可达范围 | arcpy.na.MakeServiceAreaAnalysisLayer | core（服务区通用） | ArcPy GP（arcpy.na）＋arcpy.nax；图层可改指 Online/门户路径服务 |
| Make Vehicle Routing Problem Analysis Layer | 创建 VRP 分析图层，为车队优化多车辆路线 | arcpy.na.MakeVehicleRoutingProblemAnalysisLayer | core（车辆路径问题通用） | ArcPy GP（arcpy.na）＋arcpy.nax；图层可改指 Online/门户路径服务 |
| Share As Route Layers | 把网络分析结果共享为门户中的 route layer 条目 | arcpy.na.ShareAsRouteLayers | defer（依赖门户托管与共享权限） | ArcPy GP（arcpy.na）＋门户 Route Layer 托管服务 |
| Solve | 按图层的网络位置与属性执行该图层的网络分析求解 | arcpy.na.Solve | core（求解执行为各求解器通用入口；Online 数据源时消耗 credits） | ArcPy GP（arcpy.na）＋arcpy.nax 求解器对象 |

### Network Dataset toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Build Network | 重建网络数据集的连通性与属性信息 | arcpy.na.BuildNetwork | extension（ArcGIS 网络数据集模型专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Create Network Dataset | 在已有要素数据集中创建网络数据集 | arcpy.na.CreateNetworkDataset | extension（ArcGIS 网络数据集模型专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Create Network Dataset From Template | 按 XML 模板文件的模式创建新网络数据集 | arcpy.na.CreateNetworkDatasetFromTemplate | extension（Esri 网络数据集模板格式专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Create Template From Network Dataset | 把已有网络数据集的模式导出为模板文件 | arcpy.na.CreateTemplateFromNetworkDataset | extension（Esri 网络数据集模板格式专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Dissolve Network | 生成线要素最少的等效网络数据集以加速求解与指引生成 | arcpy.na.DissolveNetwork | extension（ArcGIS 网络数据集模型专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Export Network Travel Modes | 把网络数据集的出行模式导出为 .json 文件 | arcpy.na.ExportNetworkTravelModes | extension（Esri 出行模式定义专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Make Network Dataset Layer | 由网络数据集创建网络数据集图层 | arcpy.na.MakeNetworkDatasetLayer | extension（ArcGIS 网络数据集模型专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Replace Network Travel Modes | 用 .json 文件定义的出行模式替换网络数据集的出行模式 | arcpy.na.ReplaceNetworkTravelModes | extension（Esri 出行模式定义专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |

### Turn Feature Class toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Turn Feature Class | 创建存储转向要素的转向要素类，为网络数据集建模转向运动 | arcpy.na.CreateTurnFeatureClass | extension（Esri 转向要素类专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Increase Maximum Edges | 提高转向要素类中每个转向的最大边数 | arcpy.na.IncreaseMaximumEdges | extension（Esri 转向要素类专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Populate Alternate ID Fields | 创建并填充以备用 ID 引用边的字段，维护转向要素完整性 | arcpy.na.PopulateAlternateIDFields | extension（Esri 转向要素类专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Turn Table To Turn Feature Class | 把 ArcView/ArcInfo 转向表转换为 ArcGIS 转向要素类 | arcpy.na.TurnTableToTurnFeatureClass | extension（Esri  legacy 转向格式专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Update By Alternate ID Fields | 用备用 ID 字段更新转向要素类中的全部边引用 | arcpy.na.UpdateByAlternateIDFields | extension（Esri 转向要素类专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |
| Update By Geometry | 用转向要素的几何更新转向要素类中的全部边引用 | arcpy.na.UpdateByGeometry | extension（Esri 转向要素类专属） | ArcPy GP（arcpy.na，官方实现，桥直调） |

## Spatial Statistics toolbox（arcpy.stats）
工具集数：5；工具总数：48；运行前提：桌面本地运行，无扩展/服务器/门户前提（随 ArcGIS Pro 许可级别提供，工具多为 Python 脚本工具、官方开放源码）。官方定位：分析空间分布、模式、过程与关系的统计工具，把空间（邻近、面积、连通性等）直接纳入数学计算。

### Analyzing Patterns toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Average Nearest Neighbor | 按每要素到最近邻要素的平均距离计算最近邻指数 | arcpy.stats.AverageNearestNeighbor | core（最近邻模式判定通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| High/Low Clustering | 用 Getis-Ord General G 统计量度量高值或低值的聚集程度 | arcpy.stats.HighLowClustering | core（全局聚集统计通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Incremental Spatial Autocorrelation | 对一系列距离度量空间自相关并给出 z 分数峰值距离 | arcpy.stats.IncrementalSpatialAutocorrelation | core（尺度选择通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Multi-Distance Spatial Cluster Analysis (Ripley's k-function) | 用 Ripley's K 函数判断多距离上显著聚集或离散 | arcpy.stats.MultiDistanceSpatialClusterAnalysis | core（K 函数通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Spatial Autocorrelation | 用 Global Moran's I 按要素位置与属性值度量空间自相关 | arcpy.stats.SpatialAutocorrelation | core（空间自相关通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |

### Mapping Clusters toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Build Balanced Zones | 用遗传生长算法按指定标准在研究区生成空间连续分区 | arcpy.stats.BuildBalancedZones | core（分区/区域化通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Calculate Composite Index | 把多个数值变量合并为单一综合指数 | arcpy.stats.CalculateCompositeIndex | core（综合指数通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Cluster and Outlier Analysis (Anselin Local Moran's I) | 用 Anselin Local Moran's I 识别显著热点、冷点与空间异常 | arcpy.stats.ClusterAndOutlierAnalysis | core（局部自相关通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Density-based Clustering | 按空间分布在噪声中找点要素簇，可纳入时间找时空簇 | arcpy.stats.DensitybasedClustering | core（密度聚类通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Hot Spot Analysis (Getis-Ord Gi*) | 用 Getis-Ord Gi* 识别显著热点与冷点 | arcpy.stats.HotSpotAnalysis | core（热点分析通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Hot Spot Analysis Comparison | 比较两个热点分析结果图层并度量其相似性与关联 | arcpy.stats.HotSpotAnalysisComparison | core（结果对比通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Multivariate Clustering | 仅按要素属性值找要素的自然簇 | arcpy.stats.MultivariateClustering | core（多变量聚类通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Optimized Hot Spot Analysis | 自动评估输入特征生成最优的 Getis-Ord Gi* 热点/冷点图 | arcpy.stats.OptimizedHotSpotAnalysis | core（热点分析通用，自动选参为其封装） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Optimized Outlier Analysis | 自动评估输入特征生成最优的 Local Moran's I 热点/冷点/异常图 | arcpy.stats.OptimizedOutlierAnalysis | core（局部异常通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Similarity Search | 按属性识别与一个或多个输入要素最相似或最不相似的候选要素 | arcpy.stats.SimilaritySearch | core（相似性检索通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Spatial Outlier Detection | 识别点要素的全局或局部空间异常 | arcpy.stats.SpatialOutlierDetection | core（空间异常检测通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Spatially Constrained Multivariate Clustering | 按属性值与可选簇大小限制找空间连续的要素簇 | arcpy.stats.SpatiallyConstrainedMultivariateClustering | core（空间约束聚类通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |

### Measuring Geographic Distributions toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Central Feature | 识别点/线/面要素类中最居中的要素 | arcpy.stats.CentralFeature | core（中心要素通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Directional Distribution | 创建标准差椭圆/椭球概括中心趋势、离散与方向趋势 | arcpy.stats.DirectionalDistribution | core（方向分布通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Linear Directional Mean | 识别一组线要素的平均方向、长度与地理中心 | arcpy.stats.LinearDirectionalMean | core（线方向均值通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Mean Center | 识别一组要素的地理中心（集中中心） | arcpy.stats.MeanCenter | core（平均中心通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Median Center | 识别使到各要素欧氏距离总和最小的位置 | arcpy.stats.MedianCenter | core（中位中心通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Neighborhood Summary Statistics | 用局部邻域计算一个或多个数值字段的汇总统计 | arcpy.stats.NeighborhoodSummaryStatistics | core（邻域统计通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Standard Distance | 度量要素围绕几何平均中心的集中或离散程度 | arcpy.stats.StandardDistance | core（标准距离通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |

### Modeling Spatial Relationships toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Causal Inference Analysis | 通过近似随机实验并控制混杂变量估计连续暴露对连续结果的因果效应 | arcpy.stats.CausalInferenceAnalysis | core（因果推断通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Colocation Analysis | 用共置商统计量度量两类点要素的局部空间关联 | arcpy.stats.ColocationAnalysis | core（共置分析通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Exploratory Regression | 评估候选解释变量的全部组合，找最能解释因变量的 OLS 模型 | arcpy.stats.ExploratoryRegression | core（探索性回归通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Forest-based and Boosted Classification and Regression | 用随机森林或 XGBoost 做分类与回归建模和预测 | arcpy.stats.ForestBasedAndBoostedClassificationAndRegression | core（树模型学习通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Generalized Linear Regression (GLR) | 用广义线性回归（OLS/逻辑/泊松）建模或预测因变量 | arcpy.stats.GeneralizedLinearRegression | core（GLR 通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Generate Network Spatial Weights | 用网络数据集构建 .swm 空间权重矩阵文件 | arcpy.stats.GenerateNetworkSpatialWeights | extension（.swm 为 Esri 专属权重格式） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Generate Spatial Weights Matrix | 生成表示要素间空间关系的 .swm 空间权重矩阵文件 | arcpy.stats.GenerateSpatialWeightsMatrix | extension（.swm 为 Esri 专属权重格式） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Geographically Weighted Regression (GWR) | 用地理加权回归这一局部线性回归建模空间变化关系 | arcpy.stats.GeographicallyWeightedRegression | core（GWR 通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Local Bivariate Relationships | 用局部熵分析两个变量的显著关系并分类 | arcpy.stats.LocalBivariateRelationships | core（双变量局部关系通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Multiscale Geographically Weighted Regression (MGWR) | 用多尺度地理加权回归建模空间变化关系 | arcpy.stats.MultiscaleGeographicallyWeightedRegression | core（MGWR 通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Ordinary Least Squares (OLS) | 用全局 OLS 线性回归建模或预测因变量 | arcpy.stats.OrdinaryLeastSquares | core（OLS 通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Predict Using Spatial Statistics Model File | 用训练好的空间统计模型文件（.ssm）预测连续或分类值 | arcpy.stats.PredictUsingSpatialStatisticsModelFile | extension（.ssm 为 Esri 专属模型格式） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Presence-only Prediction | 用 MaxEnt 最大熵方法按已知存在位置与解释变量建模存在概率 | arcpy.stats.PresenceonlyPrediction | core（仅存在建模/MaxEnt 通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Spatial Association Between Zones | 度量同一研究区两种区域化（分区）之间的空间关联程度 | arcpy.stats.SpatialAssociationBetweenZones | core（分区关联通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |

### Utilities toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Distance Band from Neighbor Count | 返回到第 N 近邻的最小、最大与平均距离 | arcpy.stats.CalculateDistanceBandFromNeighborCount | core（邻域距离测算通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Calculate Rates | 计算粗率或平滑率（经验贝叶斯等方法） | arcpy.stats.CalculateRates | core（率平滑通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Collect Events | 把事件数据（如犯罪、疾病事件）转换为加权点数据 | arcpy.stats.CollectEvents | core（事件聚合通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Convert Spatial Statistics Popup Charts for Web Display | 把交互式弹窗图表存为要素类附件以供 Web 显示 | arcpy.stats.ConvertSpatialStatisticsPopupChartsForWebDisplay | extension（Esri 弹窗图表机制专属） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Convert Spatial Weights Matrix To Table | 把二进制 .swm 空间权重矩阵文件转换为表 | arcpy.stats.ConvertSpatialWeightsMatrixToTable | extension（.swm 为 Esri 专属权重格式） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Describe Spatial Statistics Model File | 描述空间统计模型文件的内容与诊断信息 | arcpy.stats.DescribeSpatialStatisticsModelFile | extension（.ssm 为 Esri 专属模型格式） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Dimension Reduction | 用 PCA 或降秩 LDA 把连续变量降维为更少成分 | arcpy.stats.DimensionReduction | core（降维通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Export Feature Attributes To ASCII | 把要素坐标与属性值导出为分隔符 ASCII 文本文件 | arcpy.stats.ExportFeatureAttributesToASCII | core（通用导出） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Set Spatial Statistics Model File Properties | 给空间统计模型文件中的变量添加描述与单位 | arcpy.stats.SetSpatialStatisticsModelFileProperties | extension（.ssm 为 Esri 专属模型格式） | ArcPy GP（arcpy.stats，官方实现，桥直调） |
| Time Series Smoothing | 用移动平均或自适应局部线性回归平滑时间序列数值 | arcpy.stats.TimeSeriesSmoothing | core（序列平滑通用） | ArcPy GP（arcpy.stats，官方实现，桥直调） |

## Space Time Pattern Mining toolbox（arcpy.stpm）
工具集数：5；工具总数：18；运行前提：桌面本地运行，无扩展/服务器/门户前提。官方定位：在空间与时间的双重语境中分析数据分布与模式的统计工具，以时空 netCDF 立方体为核心数据结构，含聚类分析、预测与 2D/3D 可视化。

### Space Time Cube Creation toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Space Time Cube By Aggregating Points | 把点集聚合进时空箱汇总为 netCDF 立方体并评估计数与汇总字段趋势 | arcpy.stpm.CreateSpaceTimeCubeByAggregatingPoints | extension（netCDF 时空立方体为 Esri 工作流专属结构） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Create Space Time Cube From Defined Locations | 把面板/站点数据（位置不变、属性随时间变）结构化为 netCDF 立方体 | arcpy.stpm.CreateSpaceTimeCubeFromDefinedLocations | extension（netCDF 时空立方体为 Esri 工作流专属结构） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Create Space Time Cube From Multidimensional Raster Layer | 由多维栅格图层创建时空立方体以便时空分析与可视化 | arcpy.stpm.CreateSpaceTimeCubeFromMultidimensionalRasterLayer | extension（netCDF 时空立方体为 Esri 工作流专属结构） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |

### Space Time Cube Visualization toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Make Space Time Cube Layer | 由 netCDF 立方体创建含全部变量与分析结果副本的时空立方体图层 | arcpy.stpm.MakeSpaceTimeCubeLayer | extension（Esri 立方体图层/ribbon 交互专属） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Visualize Space Time Cube in 2D | 以 2D 形式可视化立方体变量与时空挖掘结果 | arcpy.stpm.VisualizeSpaceTimeCubeIn2D | extension（Esri 立方体可视化专属） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Visualize Space Time Cube in 3D | 以 3D 形式可视化立方体变量与时空挖掘结果 | arcpy.stpm.VisualizeSpaceTimeCubeIn3D | extension（Esri 立方体可视化专属） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |

### Space Time Pattern Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Change Point Detection | 检测立方体每个位置时间序列统计性质发生变化的时间步 | arcpy.stpm.ChangePointDetection | core（变点检测通用；输入为立方体走适配层） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Emerging Hot Spot Analysis | 识别立方体中点密度/值的聚集趋势（新增、持续、增强、减弱等冷热点类别） | arcpy.stpm.EmergingHotSpotAnalysis | core（时空热点趋势通用；输入为立方体走适配层） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Local Outlier Analysis | 在时空语境中识别显著簇与异常（时空版 Anselin Local Moran's I） | arcpy.stpm.LocalOutlierAnalysis | core（时空局部异常通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Time Series Clustering | 按时间序列特征相似性把立方体位置划分为不同簇 | arcpy.stpm.TimeSeriesClustering | core（时间序列聚类通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Time Series Cross Correlation | 计算立方体中两条时间序列在不同时间滞后下的互相关 | arcpy.stpm.TimeSeriesCrossCorrelation | core（互相关通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |

### Time Series Forecasting toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Curve Fit Forecast | 用曲线拟合预测立方体每个位置的未来值 | arcpy.stpm.CurveFitForecast | core（曲线拟合预测通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Evaluate Forecasts by Location | 为立方体每个位置在多个预测结果中选最准确者 | arcpy.stpm.EvaluateForecastsByLocation | core（预测模型评估通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Exponential Smoothing Forecast | 用 Holt-Winters 指数平滑（分解季节与趋势）预测每个位置的值 | arcpy.stpm.ExponentialSmoothingForecast | core（指数平滑通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Forest-based Forecast | 用随机森林改编算法（时间窗训练）预测立方体每个位置的值 | arcpy.stpm.ForestBasedForecast | core（森林预测通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |

### Utilities toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Describe Space Time Cube | 概括立方体的时空范围、变量、已做分析与可用显示主题 | arcpy.stpm.DescribeSpaceTimeCube | extension（netCDF 立方体专属描述） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Fill Missing Values | 用空间邻居、时空邻居、时间序列或全局统计估计值替换缺失值 | arcpy.stpm.FillMissingValues | core（缺失值填补通用） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |
| Subset Space Time Cube | 按空间范围或时间子集化时空立方体 | arcpy.stpm.SubsetSpaceTimeCube | extension（netCDF 立方体专属操作） | ArcPy GP（arcpy.stpm，官方实现，桥直调） |

## GeoAnalytics Desktop toolbox（arcpy.geoanalytics）
工具集数：6；工具总数：31；运行前提：桌面本地运行，需 ArcGIS Pro Advanced 许可（官方许可页：本箱全部工具均为 Advanced 才包含）；用本机 Apache Spark 并行框架，运行时默认占用约 95% 内存与全部 CPU 核，最适合十万至百万级记录。官方定位：在桌面机上以 Spark 并行处理框架做聚合、回归、检测与聚类的分析工具，处理大数据并洞察其模式、趋势与异常。（注：工具集结构以官方现行总览页为准——Data Enrichment 与 Find Locations 已重组为 Analyze Patterns＋Analyze Tracks，Utilities 下含 Multifile Feature Connections 子集。）

### Analyze Patterns toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Density | 计算落在每像元邻域内点要素的量值/单位面积密度 | arcpy.geoanalytics.CalculateDensity | core（密度计算通用；Spark 为实现通道） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Find Hot Spots | 用 Getis-Ord Gi* 为一组要素识别显著热点与冷点 | arcpy.geoanalytics.FindHotSpots | core（热点分析通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Find Point Clusters | 按空间或时空分布在噪声中找点要素簇 | arcpy.geoanalytics.FindPointClusters | core（点聚类通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Find Similar Locations | 按属性识别与输入要素最相似或最不相似的候选要素 | arcpy.geoanalytics.FindSimilarLocations | core（相似性检索通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Forest-based Classification and Regression | 用随机森林改编算法做分类与回归建模和预测 | arcpy.geoanalytics.ForestbasedClassificationAndRegression | core（随机森林通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Generalized Linear Regression | 用 GLR（OLS/逻辑/泊松）建模或预测因变量 | arcpy.geoanalytics.GeneralizedLinearRegression | core（GLR 通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |

### Analyze Tracks toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Motion Statistics | 计算时间启用点要素类的运动统计（速度、加速度、方位等） | arcpy.geoanalytics.CalculateMotionStatistics | core（轨迹运动统计通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Detect Incidents | 创建检测满足给定条件的要素的图层 | arcpy.geoanalytics.DetectIncidents | core（条件事件检测通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Find Dwell Locations | 按时间与距离阈值找移动对象停留（dwell）的位置 | arcpy.geoanalytics.FindDwellLocations | core（停留点检测通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Reconstruct Tracks | 由时间启用输入数据创建线或面轨迹 | arcpy.geoanalytics.ReconstructTracks | core（轨迹重建通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Snap Tracks | 把轨迹点吸附到线要素上（地图匹配 map matching） | arcpy.geoanalytics.SnapTracks | core（地图匹配通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Trace Proximity Events | 追踪在空间与时间上彼此接近的事件 | arcpy.geoanalytics.TraceProximityEvents | core（时空接近事件通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |

### Manage Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Field | 创建带计算字段值的新图层 | arcpy.geoanalytics.CalculateField | core（字段计算通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Clip Layer | 提取指定面范围内的输入要素 | arcpy.geoanalytics.ClipLayer | core（裁剪通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Dissolve Boundaries | 把相交或同字段值的面合并为单一面 | arcpy.geoanalytics.DissolveBoundaries | core（融合通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Overlay Layers | 把多图层几何叠加为单一图层（合并、擦除、修改或更新） | arcpy.geoanalytics.OverlayLayers | core（叠加分析通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |

### Summarize Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Aggregate Points | 把点聚合进面要素或分箱，返回点计数与可选统计 | arcpy.geoanalytics.AggregatePoints | core（点聚合通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Describe Dataset | 把要素概括为字段统计、样本要素与范围边界 | arcpy.geoanalytics.DescribeDataset | core（数据画像通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Join Features | 按空间、时间或属性关系把一图层属性连接至另一图层 | arcpy.geoanalytics.JoinFeatures | core（空间连接通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Summarize Attributes | 计算要素类字段的汇总统计 | arcpy.geoanalytics.SummarizeAttributes | core（属性汇总通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Summarize Center And Dispersion | 找中心要素与方向分布并计算输入的平均与中位位置 | arcpy.geoanalytics.SummarizeCenterAndDispersion | core（中心与离散通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Summarize Within | 在面内汇总另一图层的点数、线长或面面积并计算字段统计 | arcpy.geoanalytics.SummarizeWithin | core（面内汇总通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |

### Use Proximity toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Buffers | 在输入要素周围按指定距离创建缓冲区 | arcpy.geoanalytics.CreateBuffers | core（缓冲通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |
| Group By Proximity | 把空间或时空上彼此接近的要素分组 | arcpy.geoanalytics.GroupByProximity | core（邻近分组通用） | ArcPy GP（arcpy.geoanalytics，Spark 桌面并行，官方实现，桥直调） |

### Utilities toolset（Multifile Feature Connections 子集）
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Copy Dataset From Multifile Feature Connection | 把 MFC 中的一个数据集复制为要素类 | arcpy.geoanalytics.CopyDatasetFromMultifileFeatureConnection | extension（MFC 为 Esri 专属连接格式） | ArcPy GP（arcpy.geoanalytics，官方实现，桥直调） |
| Create Multifile Feature Connection | 创建多文件要素连接文件（.mfc）及其条目 | arcpy.geoanalytics.CreateMultifileFeatureConnection | extension（MFC 为 Esri 专属连接格式） | ArcPy GP（arcpy.geoanalytics，官方实现，桥直调） |
| Duplicate Dataset From Multifile Feature Connection | 创建 MFC 数据集的副本 | arcpy.geoanalytics.DuplicateDatasetFromMultifileFeatureConnection | extension（MFC 为 Esri 专属连接格式） | ArcPy GP（arcpy.geoanalytics，官方实现，桥直调） |
| Preview Dataset From Multifile Feature Connection | 预览 MFC 数据集的前十个要素 | arcpy.geoanalytics.PreviewDatasetFromMultifileFeatureConnection | extension（MFC 为 Esri 专属连接格式） | ArcPy GP（arcpy.geoanalytics，官方实现，桥直调） |
| Refresh Multifile Feature Connection | 刷新已有 MFC 并登记源位置新增的数据集 | arcpy.geoanalytics.RefreshMultifileFeatureConnection | extension（MFC 为 Esri 专属连接格式） | ArcPy GP（arcpy.geoanalytics，官方实现，桥直调） |
| Remove Dataset From Multifile Feature Connection | 从 MFC 中移除一个或多个数据集（不动源数据） | arcpy.geoanalytics.RemoveDatasetFromMultifileFeatureConnection | extension（MFC 为 Esri 专属连接格式） | ArcPy GP（arcpy.geoanalytics，官方实现，桥直调） |
| Update Multifile Feature Connection Dataset Properties | 更新 MFC 数据集的字段、几何、时间与文件设置 | arcpy.geoanalytics.UpdateMultifileFeatureConnectionDatasetProperties | extension（MFC 为 Esri 专属连接格式） | ArcPy GP（arcpy.geoanalytics，官方实现，桥直调） |

## GeoAnalytics Server toolbox（arcpy.gapro）
工具集数：6；工具总数：29；运行前提：服务器＋门户——须登录已配置 GeoAnalytics Server 的 ArcGIS Enterprise 门户（门户设置 Feature Analysis - GeoAnalytics Tools）、具备空间分析权限，Pro 仅作客户端、计算在多台服务器节点分布式执行；官方已标记 Legacy：GeoAnalytics Server 在 ArcGIS Enterprise 中弃用、最终版本为 Enterprise 11.3，本箱工具仅在 11.3 及更早版本可用；活动门户为 ArcGIS Online 时不可用。官方定位：在大数据上做空间分析的强力工具集，由 ArcGIS GeoAnalytics Server 在多服务器节点间分布式处理。

### Analyze Patterns toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Density | 计算落在每像元邻域内点要素的量值/单位面积密度 | arcpy.gapro.CalculateDensity | defer（概念通用，但本箱只能经 GeoAnalytics Server 集群＋门户权限运行且已弃用） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Create Space Time Cube | 把点集聚合进时空箱汇总为 netCDF 立方体并评估趋势 | arcpy.gapro.CreateSpaceTimeCube | defer（同上；且输出为 Esri 立方体结构） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Find Hot Spots | 用 Getis-Ord Gi* 为一组要素识别显著热点与冷点 | arcpy.gapro.FindHotSpots | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Find Point Clusters | 按空间或时空分布在噪声中找点要素簇 | arcpy.gapro.FindPointClusters | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Forest-based Classification and Regression | 用随机森林改编算法做分类与回归建模和预测 | arcpy.gapro.ForestbasedClassificationAndRegression | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Generalized Linear Regression | 用 GLR（OLS/逻辑/泊松）建模或预测因变量 | arcpy.gapro.GeneralizedLinearRegression | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Geographically Weighted Regression | 用 GWR 这一局部线性回归建模空间变化关系 | arcpy.gapro.GeographicallyWeightedRegression | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |

### Data Enrichment toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Motion Statistics | 计算时间启用点要素类的运动统计 | arcpy.gapro.CalculateMotionStatistics | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |

### Find Locations toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Detect Incidents | 创建检测满足给定条件的要素的图层 | arcpy.gapro.DetectIncidents | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Find Dwell Locations | 按时间与距离阈值找移动对象停留的位置 | arcpy.gapro.FindDwellLocations | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Find Similar Locations | 按属性识别与输入要素最相似或最不相似的候选要素 | arcpy.gapro.FindSimilarLocations | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |

### Manage Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Append Data | 把要素追加到已有托管要素图层 | arcpy.gapro.AppendData | defer（绑定门户托管图层与服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Calculate Field | 创建带计算字段值的新图层 | arcpy.gapro.CalculateField | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Clip Layer | 提取指定面范围内的输入要素 | arcpy.gapro.ClipLayer | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Copy To Data Store | 把输入要素复制为门户中的新要素服务 | arcpy.gapro.CopyToDataStore | defer（绑定门户数据存储运维） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Dissolve Boundaries | 把相交或同字段值的面合并为单一面 | arcpy.gapro.DissolveBoundaries | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Merge Layers | 合并要素图层生成单一输出图层 | arcpy.gapro.MergeLayers | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Overlay Layers | 把多图层几何叠加为单一图层（合并、擦除、修改或更新） | arcpy.gapro.OverlayLayers | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |

### Summarize Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Aggregate Points | 把点聚合进面要素或分箱，返回点计数与可选统计 | arcpy.gapro.AggregatePoints | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Describe Dataset | 把要素概括为字段统计、样本要素与范围边界 | arcpy.gapro.DescribeDataset | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Join Features | 按空间、时间或属性关系把一图层属性连接至另一图层 | arcpy.gapro.JoinFeatures | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Reconstruct Tracks | 由时间启用输入数据创建线或面轨迹 | arcpy.gapro.ReconstructTracks | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Summarize Attributes | 计算要素类字段的汇总统计 | arcpy.gapro.SummarizeAttributes | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Summarize Center And Dispersion | 找中心要素与方向分布并计算输入的平均与中位位置 | arcpy.gapro.SummarizeCenterAndDispersion | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Summarize Within | 在面内汇总另一图层的点数、线长或面面积并计算字段统计 | arcpy.gapro.SummarizeWithin | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |

### Use Proximity toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Buffers | 在输入要素周围按指定距离创建缓冲区 | arcpy.gapro.CreateBuffers | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Group By Proximity | 把空间或时空上彼此接近的要素分组 | arcpy.gapro.GroupByProximity | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Snap Tracks | 把轨迹点吸附到线要素上（地图匹配） | arcpy.gapro.SnapTracks | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |
| Trace Proximity Events | 追踪在空间与时间上彼此接近的事件 | arcpy.gapro.TraceProximityEvents | defer（概念通用，通道为已弃用的服务器集群） | 门户 GP 服务（arcpy.gapro 直调 GeoAnalytics Server）；ArcGIS REST Feature Analysis（GeoAnalytics Tools）等价接口 |

## Raster Analysis toolbox（arcpy.ra）
工具集数：9；工具总数：29；运行前提：服务器＋门户——须登录已把 ArcGIS Image Server 配置为 Raster Analysis 的 ArcGIS Enterprise 门户、具备空间分析权限，Pro 仅作客户端、计算在联邦服务器多节点分布式执行、输入输出均为门户图层；活动门户为 ArcGIS Online 时不可用。官方定位：在门户数据上做栅格分析的工具集，由 ArcGIS Image Server 驱动，分布式处理大数据集。

### Analyze Patterns toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Density | 把点/线要素的现象量摊到图面生成密度图（分级区域） | arcpy.ra.CalculateDensity | core（密度制图通用；本箱为门户实现） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Interpolate Points | 按点集测量值预测新位置的值并输出预测栅格 | arcpy.ra.InterpolatePoints | core（点插值通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Analyze Terrain toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Viewshed | 计算观察点在地面上可看见的区域 | arcpy.ra.CreateViewshed | core（可视域通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Surface Parameters | 用测地方法计算表面栅格的坡向、坡度与多种曲率参数 | arcpy.ra.SurfaceParameters | core（地形参数通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Deep Learning toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Classify Objects Using Deep Learning | 在输入栅格（及可选要素类）上运行训练好的深度学习模型给每个对象赋类标 | arcpy.ra.ClassifyObjectsUsingDeepLearning | core（深度学习对象分类推理通用；模型包为 Esri .dlpk 格式走适配） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Classify Pixels Using Deep Learning | 在输入影像上运行深度学习模型生成分类栅格并发布为门户托管影像图层 | arcpy.ra.ClassifyPixelsUsingDeepLearning | core（像元分类推理通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Detect Objects Using Deep Learning | 在输入栅格上运行深度学习模型输出所识别对象的要素类 | arcpy.ra.DetectObjectsUsingDeepLearning | core（目标检测推理通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Generalize toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Nibble | 把栅格中掩膜对应像元替换为最近邻像元值 | arcpy.ra.Nibble | core（栅格 nibble 概化通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Hydrology toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Fill | 填洼：填补表面栅格的汇以去除数据小瑕疵 | arcpy.ra.Fill | core（填洼通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Flow Accumulation | 创建流入每个像元的累积流量栅格 | arcpy.ra.FlowAccumulation | core（汇流累积通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Flow Direction | 用 D8、D-Infinity 或多流向法计算每像元到下坡邻居的流向 | arcpy.ra.FlowDirection | core（流向通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Flow Distance | 沿流路计算每像元到所汇入河道像元的水平/垂直下坡距离分量 | arcpy.ra.FlowDistance | core（流动距离通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Stream Link | 给交汇点之间栅格线性网络的各河段赋唯一值 | arcpy.ra.StreamLink | core（河段链接通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Watershed | 确定栅格中一组像元上方的汇水贡献区 | arcpy.ra.Watershed | core（流域划分通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Manage Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Convert Feature to Raster | 把要素转换为栅格数据集 | arcpy.ra.ConvertFeatureToRaster | core（矢量转栅格通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Convert Raster to Feature | 把栅格转换为点、线或面要素数据集 | arcpy.ra.ConvertRasterToFeature | core（栅格转矢量通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Summarize Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Summarize Raster Within | 计算另一数据集分区内栅格值的统计 | arcpy.ra.SummarizeRasterWithin | core（分区统计通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Zonal Statistics As Table | 计算另一数据集分区内栅格值并把结果报表为表 | arcpy.ra.ZonalStatisticsAsTable | core（分区统计表通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Use Proximity toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Distance Accumulation | 计算每像元到源的累积距离（直线/成本/真实表面距离及纵横成本因子） | arcpy.ra.DistanceAccumulation | core（距离累积通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Distance Allocation | 按直线/成本/表面距离把每像元分配给给定源 | arcpy.ra.DistanceAllocation | core（距离分配通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Optimal Path As Line | 以线形式计算源到目的地的最优路径 | arcpy.ra.OptimalPathAsLine | core（最优路径通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Optimal Path As Raster | 以栅格形式计算源到目的地的最优路径 | arcpy.ra.OptimalPathAsRaster | core（最优路径通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Optimal Region Connections | 计算两个或多个输入区域之间路径的最优连接 | arcpy.ra.OptimalRegionConnections | core（区域最优连接通用） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

### Use Proximity (Legacy) toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Distance | 计算到单一源或一组源的欧氏距离 | arcpy.ra.CalculateDistance | defer（官方已标 Legacy，推荐改用 Use Proximity 新工具） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Calculate Travel Cost | 计算到最小成本源的最小累积成本距离（计表面距离与纵横成本因子） | arcpy.ra.CalculateTravelCost | defer（官方已标 Legacy） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Cost Path As Polyline | 以线要素计算源到目的地的最小成本路径 | arcpy.ra.CostPathAsPolyline | defer（官方已标 Legacy） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Determine Optimum Travel Cost Network | 由一组输入区域计算最优成本网络 | arcpy.ra.DetermineOptimumTravelCostNetwork | defer（官方已标 Legacy） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Determine Travel Cost Path As Polyline | 计算源与目的地之间的最小成本折线路径 | arcpy.ra.DetermineTravelCostPathAsPolyline | defer（官方已标 Legacy） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |
| Determine Travel Cost Paths To Destinations | 计算已知源与已知目的地之间的具体路径 | arcpy.ra.DetermineTravelCostPathsToDestinations | defer（官方已标 Legacy） | 门户 GP 服务（arcpy.ra 直调 Image Server 栅格分析服务）；ArcGIS REST Raster Analysis 服务等价接口 |

## Standard Feature Analysis toolbox（arcpy.sfa）
工具集数：4；工具总数：10；运行前提：服务器＋门户——须登录已把托管服务器配置为 Feature Analysis - Standard Tools 的 ArcGIS Enterprise 门户、具备空间分析权限，Pro 仅作客户端、计算在门户联邦服务器执行、输出为门户图层；活动门户为 ArcGIS Online 时不可用（注：本箱为 Pro 门户工具子集，工具数少于 Web 端标准分析全集）。官方定位：在门户的要素数据上做空间分析的工具集。

### Analyze Patterns toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Calculate Density | 把点/线要素的现象量摊到图面生成由疏到密分级的密度图 | arcpy.sfa.CalculateDensity | core（密度制图通用；本箱为门户实现） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |
| Find Hot Spots | 识别数据中高值（热点）或低值（冷点）的显著空间聚集 | arcpy.sfa.FindHotSpots | core（热点分析通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |
| Interpolate Points | 按点集测量值预测新位置的值并生成按预测值分级的区域 | arcpy.sfa.InterpolatePoints | core（点插值通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |

### Manage Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Dissolve Boundaries | 把重叠或共享边界的面合并为单一面 | arcpy.sfa.DissolveBoundaries | core（融合通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |
| Merge Layers | 把两个图层的全部要素复制到新图层（须同为点/线/面） | arcpy.sfa.MergeLayers | core（图层合并通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |
| Overlay Layers | 把多图层几何叠加为单一图层并带入全部参与属性 | arcpy.sfa.OverlayLayers | core（叠加分析通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |

### Summarize Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Aggregate Points | 按点-面空间关系确定各面内的点并计算其统计赋给该面 | arcpy.sfa.AggregatePoints | core（点聚合通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |
| Summarize Nearby | 找输入图层要素指定距离内的要素 | arcpy.sfa.SummarizeNearby | core（邻近汇总通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |
| Summarize Within | 找位于另一图层面边界内的点/线/面要素（或其部分） | arcpy.sfa.SummarizeWithin | core（面内汇总通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |

### Use Proximity toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Buffers | 创建覆盖点/线/面要素给定距离的面 | arcpy.sfa.CreateBuffers | core（缓冲通用） | 门户 GP 服务（arcpy.sfa 直调托管服务器 Standard Tools）；ArcGIS REST Feature Analysis 服务等价接口 |

## Ready To Use toolbox（arcpy.agolservices）
工具集数：3；工具总数：11；运行前提：在线账号＋额度——工具即 ArcGIS Online 地理处理服务，须登录 ArcGIS Online 组织账号且具相应权限，全部数据与计算由 ArcGIS Online 托管、只需提供少量输入要素；Elevation 与 Hydrology 服务工具现已免费，Network Analysis 服务工具按 credits 计费（如 Find Closest Facilities 0.5 credits/条路线）。官方定位：使用 ArcGIS Online 托管数据与分析能力的即用型服务工具，可解高程、水文与网络分析问题。（注：3.4/3.2 工具箱总览表只单列 Elevation 与 Hydrology 两集，Network Analysis 集未在总览表列行，但其 toolset 总览页仍在现行官方文档中、且总览页正文仍称工具含 routing/directions/service areas，故一并抄录并在此标明。）

### Elevation toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Profile | 返回输入线要素的高程剖面 | arcpy.agolservices.Profile | defer（概念通用，但只能经 ArcGIS Online 托管高程服务运行） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 elevation.arcgis.com |
| Summarize Elevation | 计算每个输入要素的高程汇总统计 | arcpy.agolservices.SummarizeElevation | defer（同上，依赖 Online 权威 DEM 托管数据） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 elevation.arcgis.com |
| Viewshed | 返回给定观察点集合的可见区域面 | arcpy.agolservices.Viewshed | defer（概念通用，通道为 Online 托管服务） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 elevation.arcgis.com |

### Hydrology toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Trace Downstream | 确定水从某位置出发到最远下坡处的路径 | arcpy.agolservices.TraceDownstream | defer（概念通用，通道为 Online 托管服务） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 hydro.arcgis.com |
| Watershed | 确定每个输入点上方的汇水贡献区（流域） | arcpy.agolservices.Watershed | defer（概念通用，通道为 Online 托管服务） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 hydro.arcgis.com |

### Network Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Find Closest Facilities | 按出行时间/距离找离事件最近的一个或多个设施并输出最佳路线与指引 | arcpy.agolservices.FindClosestFacilities | defer（概念与 Network Analyst 箱同源，但本通道为 Online 物流服务且按 credits 计费） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 logistics.arcgis.com |
| Find Routes | 求访问输入停靠点的最短路径并返回指引、停靠信息与路线 | arcpy.agolservices.FindRoutes | defer（同上，Online 服务＋credits） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 logistics.arcgis.com |
| Generate Origin Destination Cost Matrix | 由多起点到多终点生成 OD 成本矩阵（含时间、距离与排序） | arcpy.agolservices.GenerateOriginDestinationCostMatrix | defer（同上，Online 服务＋credits） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 logistics.arcgis.com |
| Generate Service Areas | 求设施周围的网络服务区（给定距离/时间内可达的全部街道范围） | arcpy.agolservices.GenerateServiceAreas | defer（同上，Online 服务＋credits） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 logistics.arcgis.com |
| Solve Location Allocation | 通过把需求点分配给设施使总需求最大、总出行最小来选最佳设施位置 | arcpy.agolservices.SolveLocationAllocation | defer（同上，Online 服务＋credits） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 logistics.arcgis.com |
| Solve Vehicle Routing Problem | 求解车辆路径问题（VRP）为车队找最佳路线 | arcpy.agolservices.SolveVehicleRoutingProblem | defer（同上，Online 服务＋credits） | ArcGIS Online 托管 GP 服务（arcpy.agolservices 直调）；REST 端点 logistics.arcgis.com |

## 附：Esri 官方智能体 / MCP 入口（普查中发现，单列备查）
- **MCP for ArcGIS Location Services（beta）**——Esri 官方托管的 Model Context Protocol 服务器，供应用与 AI 智能体以标准化 MCP 工具访问 ArcGIS Location Services（底图样式、静态底图瓦片、静态地图、Places、地理编码、路径、高程、GeoEnrichment），免直接调用 REST API；需 ArcGIS Location Platform 或 ArcGIS Online 账号。与本节的关系：其 Routing 与 Elevation 能力与 Ready To Use 的网络/高程服务同源，是平台「不造轮子」可直接对接的官方智能体通道。链接：https://developers.arcgis.com/ai/mcp-arcgis-location-services/
- **ArcGIS Pro assistant（beta）**——Esri 官方内置于 ArcGIS Pro 的 AI 助手（Early Adopter 私有 beta）：自然语言查文档、生成 ArcPy/SQL/openCypher 代码、触发应用内动作（如打开缓冲工具）。与本节的关系：官方的「智能体操作 GP 工具」入口，平台做 Agent 编排时应优先评估与其分工而非另起炉灶。链接：https://www.esri.com/about/newsroom/arcnews/ai-assistants-in-arcgis-provide-practical-help-and-give-useful-results ；Early Adopter 页：https://earlyadopter.esri.com/key/ArcGISProAssistants
- 说明：社区/第三方 MCP（如社区 arcgis-portal-mcp、合作伙伴 SkyFi MCP Server）非 Esri 官方出品，按证据纪律不计入本节，仅注记其存在。


> 范围：Editing、Geocoding、Linear Referencing、Location Referencing、Data Interoperability、Data Reviewer、Multidimension 七个工具箱的全部地理处理工具。
> 证据：一级证据仅用 Esri 官方文档（pro.arcgis.com，ArcGIS Pro 3.4 工具参考的各工具箱总览页与各 toolset 总览页，逐条抄录 Tool | Description 表）；工具构成另以同版许可页交叉核对（Geocoding）。
> 平台升级原则（鱼鱼定版）：全部升级＋不重复造轮子——平台层只做翻译与治理、不自研算法；「轮子来源」列写明每条工具可复用的官方现成实现通道。
> 平台判断口径：core＝通用能力、多家共有，宜升为平台通用能力；extension＝ArcGIS 专属数据模型／检查框架／FME 引擎绑定，宜以扩展包形式接入；defer＝依赖地址定位器建设、交互质检会话、第三方引擎许可等前置条件，暂缓。
> 合计：111 条工具，其中 core 44 条、extension 56 条、defer 11 条。

## Editing toolbox（arcpy.edit）

工具集数：2（工具箱顶层＋Conflation）；工具总数：18；前提：官方总览未标注扩展许可，属 ArcGIS Pro 核心工具箱；官方定位：对要素类的全部（或选中）要素做批量编辑，处理数字化精度不足、无捕捉环境造成的面边界不闭合、线过冲／欠冲，以及顶点密度、多源融合等数据质量问题。

### Editing toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Densify | 沿线或面要素添加顶点，并把曲线段（贝塞尔、圆弧、椭圆弧）替换为线段 | `arcpy.edit.Densify` | ArcPy GP（官方实现，桥直调） | core — 顶点加密属批量编辑基础，多家共有 |
| Erase Point | 按操作类型删除落在移除要素内部或外部的输入点 | `arcpy.edit.ErasePoint` | ArcPy GP（官方实现，桥直调） | core — 点批量清理通用能力 |
| Extend Line | 把线段延长至指定距离内首个相交要素，用于清理无捕捉数字化造成的拓扑错误 | `arcpy.edit.ExtendLine` | ArcPy GP（官方实现，桥直调） | core — 线过冲／欠冲清理通用能力 |
| Flip Line | 反转线要素的起止方向 | `arcpy.edit.FlipLine` | ArcPy GP（官方实现，桥直调） | core — 基础几何编辑，多家共有 |
| Generalize | 按最大偏移容差简化输入要素，输出只保留原始顶点子集 | `arcpy.edit.Generalize` | ArcPy GP（官方实现，桥直调） | core — 几何简化通用能力 |
| Simplify By Straight Lines And Circular Arcs | 以更少的线段／边替换连续线段，并可由连续线段生成圆弧 | `arcpy.edit.SimplifyByStraightLinesAndCircularArcs` | ArcPy GP（官方实现，桥直调） | core — 通用简化，圆弧拟合不改变其通用性 |
| Snap | 把点或顶点移动到与其他要素的顶点、边或端点精确重合 | `arcpy.edit.Snap` | ArcPy GP（官方实现，桥直调） | core — 捕捉对齐属编辑基础能力 |
| Trim Line | 去除线越过交点后指定距离内的悬挂部分（dangles） | `arcpy.edit.TrimLine` | ArcPy GP（官方实现，桥直调） | core — 悬挂线清理通用能力 |
| Update COGO | 更新启用 COGO 的线要素的 COGO 属性，使其与线形状几何一致 | `arcpy.edit.UpdateCOGO` | ArcPy GP（官方实现，桥直调） | extension — COGO 是 ArcGIS 测量／宗地专属属性体系 |

### Conflation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Align Features | 在搜索距离内找出输入要素与目标要素不一致的部分并将其对齐到目标 | `arcpy.edit.AlignFeatures` | ArcPy GP（官方实现，桥直调） | core — 多源数据对齐通用需求 |
| Calculate Transformation Errors | 按已知控制点间链接坐标计算残差与均方根误差（RMSE），供空间变换使用 | `arcpy.edit.CalculateTransformationErrors` | ArcPy GP（官方实现，桥直调） | core — 变换精度评估通用能力 |
| Edgematch Features | 按接边匹配链接对输入线做空间调整，使其与相邻数据集的线连接 | `arcpy.edit.EdgematchFeatures` | ArcPy GP（官方实现，桥直调） | core — 接边匹配为通用融合工序 |
| Generate Edgematch Links | 在源数据与相邻数据接边处找出匹配但未连接的线，生成接边匹配链接 | `arcpy.edit.GenerateEdgematchLinks` | ArcPy GP（官方实现，桥直调） | core — 融合链接生成通用能力 |
| Generate Rubbersheet Links | 找出源线与目标线的空间匹配处，生成用于橡皮拉伸的链接线 | `arcpy.edit.GenerateRubbersheetLinks` | ArcPy GP（官方实现，桥直调） | core — 橡皮拉伸链接生成通用能力 |
| Rubbersheet Features | 按橡皮拉伸链接对输入要素做空间调整，使其与目标要素更好对齐 | `arcpy.edit.RubbersheetFeatures` | ArcPy GP（官方实现，桥直调） | core — 橡皮拉伸调整多家共有 |
| Split Line By Match | 按匹配关系分割要素，获得更好的对应线分段 | `arcpy.edit.SplitLineByMatch` | ArcPy GP（官方实现，桥直调） | extension — 依赖 Esri 融合匹配关系模型 |
| Transfer Attributes | 找出源线与目标线的空间匹配处，把指定属性从源要素传到匹配的目标要素 | `arcpy.edit.TransferAttributes` | ArcPy GP（官方实现，桥直调） | core — 属性转移为通用融合工序 |
| Transform Features | 按已知对应控制点间的变换链接，对输入要素坐标做缩放、平移与旋转 | `arcpy.edit.TransformFeatures` | ArcPy GP（官方实现，桥直调） | core — 坐标变换通用能力 |

## Geocoding toolbox（arcpy.geocoding）

工具集数：3（工具箱顶层＋Data Preparation＋Portal）；工具总数：15；前提：3.4 许可页显示顶层与 Data Preparation 工具在 Basic／Standard／Advanced 均可用；Portal 工具要求 ArcGIS Enterprise 账号具备 Perform Analysis 权限；使用 ArcGIS World Geocoding Service 时可能消耗 credits；官方定位：地理编码是把地址中的描述性位置元素与参考资料比对、赋予其位置（通常为坐标值）的过程，本箱覆盖定位器创建维护、地址地理编码与由点取址等任务。注：以工具箱工具为准（arcpy.geocoding 模块另有函数级接口，不计入本表）。

### Geocoding toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Polygon Fields To Locator | 把面图层的自定义输出字段添加给本地存储的已有定位器 | `arcpy.geocoding.AddPolygonFieldsToLocator` | ArcPy GP（官方实现，桥直调） | defer — 依赖已建成的定位器资产 |
| Clip Locator | 按兴趣区或范围裁剪定位器，生成范围与体积更小的定位器 | `arcpy.geocoding.ClipLocator` | ArcPy GP（官方实现，桥直调） | defer — 属定位器建设／维护环节 |
| Create Composite Address Locator | 创建由两个以上单独定位器组成的复合定位器，可用多定位器匹配地址与地点 | `arcpy.geocoding.CreateCompositeAddressLocator` | ArcPy GP（官方实现，桥直调） | defer — 依赖定位器体系建设 |
| Create Feature Locator | 用单字段存唯一名称／值的参考数据创建定位器，可检索水表、地名、信号塔、编码串等 | `arcpy.geocoding.CreateFeatureLocator` | ArcPy GP（官方实现，桥直调） | defer — 属定位器建设环节 |
| Create Locator | 创建可查地址／地点位置、把地址表转为点要素、或由点识别地址的定位器 | `arcpy.geocoding.CreateLocator` | ArcPy GP（官方实现，桥直调） | defer — 平台地理编码的地基，但须先建定位器 |
| Delete Polygon Fields From Locator | 删除已有定位器上由面图层附加的全部自定义输出字段 | `arcpy.geocoding.DeletePolygonFieldsFromLocator` | ArcPy GP（官方实现，桥直调） | defer — 依赖已建成的定位器资产 |
| Geocode Addresses | 把地址表与定位器或复合定位器匹配，每条记录的结果存为新的点要素类 | `arcpy.geocoding.GeocodeAddresses` | ArcPy GP（桥直调）；ArcGIS REST 服务等价接口（World Geocoding Service） | core — 地理编码为通用能力，多家共有 |
| Rebuild Address Locator | 重建地址定位器，使其纳入参考数据的当前几何与属性变更 | `arcpy.geocoding.RebuildAddressLocator` | ArcPy GP（官方实现，桥直调） | defer — 属定位器维护环节 |
| Rematch Addresses | 对已地理编码要素类中的地址重新匹配 | `arcpy.geocoding.RematchAddresses` | ArcPy GP（官方实现，桥直调） | core — 地理编码结果再匹配属通用流程 |
| Reverse Geocode | 由点位置要素类生成地址，查找最近的地址、地点或交叉口 | `arcpy.geocoding.ReverseGeocode` | ArcPy GP（桥直调）；ArcGIS REST 服务等价接口（Geocoding 服务） | core — 逆地理编码为通用能力 |

### Data Preparation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Assign Streets To Points | 综合门牌号、街道名等地址信息与距离，为点找出最佳街道要素候选（地址信息优先于距离） | `arcpy.geocoding.AssignStreetsToPoints` | ArcPy GP（官方实现，桥直调） | defer — 为 Create Locator 建定位器做数据准备 |
| Assign Zones To Streets | 把社区、城市、都市区、邮编等行政区值赋给街道线段的左右两侧 | `arcpy.geocoding.AssignZonesToStreets` | ArcPy GP（官方实现，桥直调） | defer — 为建定位器准备街道参考数据 |
| Split Address Into Components | 把街道地址信息拆成地址组成部分，输出为带独立字段的表或要素类 | `arcpy.geocoding.SplitAddressIntoComponents` | ArcPy GP（官方实现，桥直调） | core — 地址解析／标准化为通用文本处理 |

### Portal toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Geocode File | 把本地大批量地址／地点表转换为点，输出要素类或 CSV／XLS 表，使用门户托管定位器 | `arcpy.geocoding.GeocodeFile` | ArcGIS Enterprise 门户托管工具（REST 分析服务） | defer — 依赖 Enterprise 门户与托管定位器及权限 |
| Geocode Locations From Table | 用门户托管定位器对托管表地理编码，生成含结果的托管要素图层 | `arcpy.geocoding.GeocodeLocationsFromTable` | ArcGIS Enterprise 门户托管工具（REST 分析服务） | defer — 依赖 Enterprise 门户与托管定位器及权限 |

## Linear Referencing toolbox（arcpy.lr）

工具集数：1（无 toolset 分组，工具直列于工具箱）；工具总数：7；前提：核心工具箱，Esri 官方说明核心线性参考工具含于 Basic 许可级别；官方定位：为采集公路、街道、铁路、河流、管线、给排水网络等线状要素数据的组织提供线性参考系统，用已知线要素及其沿线测量值（measure）表达位置，本箱含创建、校准与显示线性参考数据的工具。

### Linear Referencing toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Calibrate Routes | 用校准点重新计算路径的测量值 | `arcpy.lr.CalibrateRoutes` | ArcPy GP（官方实现，桥直调） | core — 线性参考基础能力 |
| Create Routes | 由已有线创建路径，同标识的输入线要素合并为一条路径 | `arcpy.lr.CreateRoutes` | ArcPy GP（官方实现，桥直调） | core — 线性参考基础能力 |
| Dissolve Route Events | 消除事件表冗余信息，或把含多个描述属性的事件表拆为单独的表 | `arcpy.lr.DissolveRouteEvents` | ArcPy GP（官方实现，桥直调） | core — 事件表整理通用能力 |
| Locate Features Along Routes | 计算输入要素（点／线／面）与路径要素的交叠，把路径与测量信息写入新事件表 | `arcpy.lr.LocateFeaturesAlongRoutes` | ArcPy GP（官方实现，桥直调） | core — 动态分段基础能力，多家共有 |
| Make Route Event Layer | 用路径与路径事件创建临时要素图层 | `arcpy.lr.MakeRouteEventLayer` | ArcPy GP（官方实现，桥直调） | core — 事件可视化基础能力 |
| Overlay Route Events | 叠加两个事件表，输出表示其并集或交集的事件表 | `arcpy.lr.OverlayRouteEvents` | ArcPy GP（官方实现，桥直调） | core — 事件叠加为线性参考基础运算 |
| Transform Route Events | 把事件的测量值从一套路径参考转换到另一套，并写入新事件表 | `arcpy.lr.TransformRouteEvents` | ArcPy GP（官方实现，桥直调） | core — 事件参考转换基础能力 |

## Location Referencing toolbox（arcpy.locref）

工具集数：6（工具箱顶层＋Configuration，及其下 LRS、LRS Event、LRS Intersection、LRS Network 四个子集）；工具总数：44；前提：需要 Location Referencing 扩展许可（Roads and Highways／Pipeline Referencing）；官方定位：提供 LRS（线性参考系统）的配置与管理核心工具。补充：该扩展另把线性参考能力以 ArcGIS Server 的 Linear Referencing Service（REST）形式提供（见 Pipeline Referencing 官方入门页），GP 之外多一条服务复用通道。

### Location Referencing toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Append Events | 把表、图层或要素类中的事件记录追加到已有 LRS 事件要素类 | `arcpy.locref.AppendEvents` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件数据模型 |
| Append Routes | 把输入折线追加到 LRS Network 中成为路径 | `arcpy.locref.AppendRoutes` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Apply Event Behaviors | 按所做的路径编辑，更新注册到输入网络的全部事件要素类的事件位置 | `arcpy.locref.ApplyEventBehaviors` | ArcPy GP（官方实现，桥直调） | extension — 事件行为规则为 LRS 专属机制 |
| Calculate Intersecting Route Measures | 生成一张表，列出每个交叉口位置处全部路径及其测量值 | `arcpy.locref.CalculateIntersectingRouteMeasures` | ArcPy GP（官方实现，桥直调） | extension — 依赖 LRS Network 与交叉口模型 |
| Calculate Route Concurrencies | 计算并报告 LRS Network 中的并发路径区段 | `arcpy.locref.CalculateRouteConcurrencies` | ArcPy GP（官方实现，桥直调） | extension — 并发路径为 LRS 专属概念 |
| Delete Routes | 从 LRS Network 删除路径及其关联数据元素 | `arcpy.locref.DeleteRoutes` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Derive Event Measures | 在已配置启用的点／线事件上填充并更新 DerivedRouteID 字段与测量值 | `arcpy.locref.DeriveEventMeasures` | ArcPy GP（官方实现，桥直调） | extension — 派生测量字段为 LRS 专属机制 |
| Generate Calibration Points | 为任意路径形状（含自闭合、自相交、分支等复杂形状）生成校准点 | `arcpy.locref.GenerateCalibrationPoints` | ArcPy GP（官方实现，桥直调） | extension — 服务于 LRS 校准模型 |
| Generate Events | 为注册到 LRS Network 的事件要素重新生成形状 | `arcpy.locref.GenerateEvents` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Generate Intersections | 生成新交叉口并更新已有交叉口 | `arcpy.locref.GenerateIntersections` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口模型 |
| Generate LRS Data Product | 变换 LRS 数据，为 LRS Network 中选定路径生成长度产品（如按县界汇总里程） | `arcpy.locref.GenerateLRSDataProduct` | ArcPy GP（官方实现，桥直调） | extension — LRS 专属数据产品 |
| Generate Routes | 为 LRS Network 中的路径要素重建形状并应用校准变更 | `arcpy.locref.GenerateRoutes` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Overlay Events | 把一个以上线／点事件图层叠加到目标网络，输出表示动态分段结果的要素类或表 | `arcpy.locref.OverlayEvents` | ArcPy GP（官方实现，桥直调） | extension — 虽为动态分段，但实现绑定 LRS Network |
| Remove Overlapping Centerlines | 移除重叠的中心线区段，使中心线几何重叠处只有一条公共中心线 | `arcpy.locref.RemoveOverlappingCenterlines` | ArcPy GP（官方实现，桥直调） | extension — 中心线为 LRS 专属概念 |
| Reverse Line Orders | 反转一条线中全部路径的线顺序 | `arcpy.locref.ReverseLineOrders` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 线／路径模型 |
| Translate Event Measures | 把点或线事件图层的测量值（m 值）从一种线性参考方法（LRM）翻译到另一种 | `arcpy.locref.TranslateEventMeasures` | ArcPy GP（官方实现，桥直调） | extension — LRM 体系为 LRS 专属 |
| Update Measures From LRS | 为 Utility Network 要素（如管道、设备、结点）或非 UN／LRS 要素类填充并更新路径 ID 与测量值 | `arcpy.locref.UpdateMeasuresFromLRS` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 与 Utility Network 模型 |

### Configuration toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Configure Address Feature Classes | 把 Address Data Management 方案的地址范围与站点地址要素类配置为可用于 LRS（配合 Roads and Highways） | `arcpy.locref.ConfigureAddressFeatureClasses` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Esri 方案模板与 LRS 模型 |
| Configure Utility Network Feature Class | 把 Utility Network 管线要素类配置为可用于 LRS | `arcpy.locref.ConfigureUtilityNetworkFeatureClass` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Utility Network 与 LRS 模型 |
| Remove LRS Entity | 从输入地理数据库工作空间移除一个 LRS 实体 | `arcpy.locref.RemoveLRSEntity` | ArcPy GP（官方实现，桥直调） | extension — LRS 实体为专属数据模型对象 |

### Configuration > LRS toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create LRS | 在指定工作空间创建 LRS 及最小模式项 | `arcpy.locref.CreateLRS` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS 信息模型 |
| Create LRS From Existing Dataset | 用已有数据集在指定工作空间创建 LRS | `arcpy.locref.CreateLRSFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS 信息模型 |
| Modify LRS | 修改指定工作空间中已有的 LRS | `arcpy.locref.ModifyLRS` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 信息模型 |

### Configuration > LRS Event toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Configure External Event With LRS | 把存储在外部系统中的事件数据与 LRS 关联 | `arcpy.locref.ConfigureExternalEventWithLRS` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Create LRS Event | 为已有 LRS Network 创建线或点事件 | `arcpy.locref.CreateLRSEvent` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件数据模型 |
| Create LRS Event From Existing Dataset | 把已有要素类注册为 LRS 事件 | `arcpy.locref.CreateLRSEventFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Disable Derived Measure Fields | 禁用存储派生网络路径 ID、路径名与测量值的字段 | `arcpy.locref.DisableDerivedMeasureFields` | ArcPy GP（官方实现，桥直调） | extension — 派生测量字段为 LRS 专属机制 |
| Disable Referent Fields | 禁用已有 LRS 事件要素类／图层的参照字段（不删列，仅从 Lrs_Metadata 表移除其信息） | `arcpy.locref.DisableReferentFields` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 元数据表结构 |
| Disable Stationing Fields | 禁用已注册 LRS 事件的桩号字段 | `arcpy.locref.DisableStationingFields` | ArcPy GP（官方实现，桥直调） | extension — 桩号字段为 LRS 专属机制 |
| Enable Derived Measure Fields | 为指定 LRS 事件要素类启用存储派生路径 ID、派生路径名与派生测量值的字段 | `arcpy.locref.EnableDerivedMeasureFields` | ArcPy GP（官方实现，桥直调） | extension — 派生测量字段为 LRS 专属机制 |
| Enable Referent Fields | 启用或修改参照字段，以便管理已注册 LRS 事件的参照信息 | `arcpy.locref.EnableReferentFields` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Enable Stationing Fields | 启用或修改桩号字段，以便管理已注册 LRS 事件的桩号信息 | `arcpy.locref.EnableStationingFields` | ArcPy GP（官方实现，桥直调） | extension — 桩号字段为 LRS 专属机制 |
| Modify Event Behavior Rules | 修改已注册事件图层或要素类的事件行为规则 | `arcpy.locref.ModifyEventBehaviorRules` | ArcPy GP（官方实现，桥直调） | extension — 事件行为规则为 LRS 专属机制 |
| Modify LRS Event | 修改 LRS 事件的属性 | `arcpy.locref.ModifyLRSEvent` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件数据模型 |

### Configuration > LRS Intersection toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create LRS Intersection | 为已有 LRS Network 创建交叉口要素类 | `arcpy.locref.CreateLRSIntersection` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口模型 |
| Create LRS Intersection From Existing Dataset | 把已有交叉口要素类注册为交叉口 | `arcpy.locref.CreateLRSIntersectionFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口注册模型 |
| Modify LRS Intersection | 修改交叉口要素类的属性，如组成它的字段与相交图层的增删 | `arcpy.locref.ModifyLRSIntersection` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口模型 |

### Configuration > LRS Network toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Configure Lookup Table | 为多字段路径 ID 中使用的一个或多个字段配置查找表 | `arcpy.locref.ConfigureLookupTable` | ArcPy GP（官方实现，桥直调） | extension — 多字段路径 ID 为 LRS 专属机制 |
| Configure Route Dominance Rules | 配置规则集，判定存在并发路径的网络中哪条为主导路径 | `arcpy.locref.ConfigureRouteDominanceRules` | ArcPy GP（官方实现，桥直调） | extension — 路径主导规则为 LRS 专属机制 |
| Create LRS Network | 在 LRS 中创建 LRS Network | `arcpy.locref.CreateLRSNetwork` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS Network 模型 |
| Create LRS Network From Existing Dataset | 用已有折线要素类创建 LRS Network | `arcpy.locref.CreateLRSNetworkFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS Network 模型 |
| Modify LRS Network | 修改 LRS 中的 LRS Network | `arcpy.locref.ModifyLRSNetwork` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Modify Network Calibration Rules | 修改 LRS Network 的网络校准规则 | `arcpy.locref.ModifyNetworkCalibrationRules` | ArcPy GP（官方实现，桥直调） | extension — 网络校准规则为 LRS 专属机制 |
| Modify Route ID Padding | 修改多字段路径 ID 组成字段的填充、空值与长度属性 | `arcpy.locref.ModifyRouteIDPadding` | ArcPy GP（官方实现，桥直调） | extension — 多字段路径 ID 为 LRS 专属机制 |

## Data Interoperability toolbox（arcpy.di）

工具集数：1（无 toolset 分组，工具直列于工具箱）；工具总数：2；前提：需要 Data Interoperability 许可；官方定位：用 Safe Software 的 FME 技术转换广泛的数据格式，FME 套件是空间数据的提取、转换、加载（ETL）工具，可把空间数据格式整合进 GIS 分析并基于内置格式与转换器建模自定义格式。注：用户自建的空间 ETL 工具（由 FME Workbench 工作空间生成）不属官方工具箱工具，不计入本表。

### Data Interoperability toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Quick Export | 把一个或多个输入要素类／要素图层转换为本扩展支持的任意格式 | `arcpy.di.QuickExport` | ArcPy GP（桥直调，底层 Safe Software FME 引擎） | extension — FME 引擎绑定 |
| Quick Import | 把本扩展支持的任意格式的矢量或表格数据转换为要素类或表 | `arcpy.di.QuickImport` | ArcPy GP（桥直调，底层 Safe Software FME 引擎） | extension — FME 引擎绑定 |

## Data Reviewer toolbox（arcpy.reviewer）

工具集数：2（Data Validation＋Result Management）；工具总数：5；前提：需要 Data Reviewer 扩展许可；官方定位：Data Reviewer 扩展为 ArcGIS 加入数据质量控制框架，用批处理作业（batch job）中包含的各类检查（checks）校验数据的空间关系与完整性，并提供纠正校验所发现错误的工具；本箱工具支持创建 Reviewer 会话与执行批处理作业等数据校验工作。注：ArcMap 版工具箱中的 Geodatabase Schema Compare 在 ArcGIS Pro 版两 toolset 总览中无此工具，不计入。

### Data Validation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Execute Reviewer Batch Job | 对工作空间运行 Reviewer 批处理作业并把结果写入 Reviewer 会话；作业含成组的检查，按条件、规则与空间关系校验数据 | `arcpy.reviewer.ExecuteReviewerBatchJob` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Reviewer 检查／批作业框架 |
| Write To Reviewer Table | 把要素类、要素图层、表或表视图写入 Reviewer 工作空间 | `arcpy.reviewer.WriteToReviewerTable` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Reviewer 工作空间结构 |

### Result Management toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create Reviewer Session | 在指定工作空间中新建一个 Reviewer 会话 | `arcpy.reviewer.CreateReviewerSession` | ArcPy GP（官方实现，桥直调） | extension — 会话机制为 Reviewer 框架专属 |
| Delete Reviewer Session | 从 Reviewer 工作空间永久删除一个或多个会话及其全部相关记录 | `arcpy.reviewer.DeleteReviewerSession` | ArcPy GP（官方实现，桥直调） | extension — 会话机制为 Reviewer 框架专属 |
| Enable Data Reviewer | 为已有地理数据库添加使其成为 Reviewer 工作空间所需的数据集与表，以存储 Data Reviewer 结果 | `arcpy.reviewer.EnableDataReviewer` | ArcPy GP（官方实现，桥直调） | extension — Reviewer 工作空间为专属结构 |

## Multidimension toolbox（arcpy.md）

工具集数：2（工具箱顶层＋NetCDF）；工具总数：20；前提：官方说明本工具箱工具不需要额外扩展许可；官方定位：创建与管理 netCDF、GRIB、HDF、OPeNDAP、Esri CRF、多维镶嵌数据集与多维影像服务，可生成多维元数据、创建多维栅格／要素图层或表视图、选取多维数据集的特定切片、或生成多维栅格子集。

### Multidimension toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Build Multidimensional Info | 在镶嵌数据集中生成多维元数据，包括变量与维度信息 | `arcpy.md.BuildMultidimensionalInfo` | ArcPy GP（官方实现，桥直调） | extension — 绑定镶嵌数据集／CRF 多维模型 |
| Build Multidimensional Transpose | 转置多维栅格数据集，沿各维度切分数据以优化跨全部切片取像素值的性能 | `arcpy.md.BuildMultidimensionalTranspose` | ArcPy GP（官方实现，桥直调） | extension — CRF 存储布局优化，Esri 专属 |
| Make Multidimensional Raster Layer | 按定义的变量与维度切片多维栅格数据集或图层，创建栅格图层 | `arcpy.md.MakeMultidimensionalRasterLayer` | ArcPy GP（官方实现，桥直调） | core — 多维栅格切片为通用能力 |
| Make Multidimensional Voxel Layer | 由多维体素数据集创建体素图层 | `arcpy.md.MakeMultidimensionalVoxelLayer` | ArcPy GP（官方实现，桥直调） | extension — 体素图层为 ArcGIS 专属数据模型 |
| Make OPeNDAP Raster Layer | 由 OPeNDAP 服务器上存储的数据创建栅格图层 | `arcpy.md.MakeOPeNDAPRasterLayer` | ArcPy GP（桥直调，数据来自 OPeNDAP 开放服务协议） | core — 基于开放协议，多家共有 |
| Manage Multidimensional Raster | 通过添加或删除变量或维度来编辑多维栅格 | `arcpy.md.ManageMultidimensionalRaster` | ArcPy GP（官方实现，桥直调） | core — 多维数据结构管理通用能力 |
| Merge Multidimensional Rasters | 在空间上或跨变量与维度合并多个多维栅格数据集 | `arcpy.md.MergeMultidimensionalRasters` | ArcPy GP（官方实现，桥直调） | core — 多维栅格合并通用能力 |
| Select By Dimension | 按维度值更新 netCDF 图层显示或 netCDF 表视图 | `arcpy.md.SelectByDimension` | ArcPy GP（官方实现，桥直调） | core — 按维度选片为 netCDF 基础操作 |
| Subset Multidimensional Raster | 按定义的变量与维度切片，创建多维栅格的子集 | `arcpy.md.SubsetMultidimensionalRaster` | ArcPy GP（官方实现，桥直调） | core — 多维子集提取通用能力 |

### NetCDF toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Describe NetCDF File | 描述输入 netCDF 数据集的性质与内容，列出全部变量及其维度与属性 | `arcpy.md.DescribeNetCDFFile` | ArcPy GP（官方实现，桥直调） | core — netCDF 元数据读取基础能力 |
| Feature to NetCDF | 把点要素转换为 netCDF 文件 | `arcpy.md.FeatureToNetCDF` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础写出，多家共有 |
| Make NetCDF Feature Layer | 由 netCDF 文件创建要素图层 | `arcpy.md.MakeNetCDFFeatureLayer` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础读取 |
| Make NetCDF Raster Layer | 由 netCDF 文件创建栅格图层 | `arcpy.md.MakeNetCDFRasterLayer` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础读取 |
| Make NetCDF Table View | 由 netCDF 文件创建表视图 | `arcpy.md.MakeNetCDFTableView` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础读取 |
| NetCDF Points To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的点（离散采样几何 DSG）创建为要素类 | `arcpy.md.NetCDFPointsToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| NetCDF Profiles To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的剖面（DSG）创建为要素类 | `arcpy.md.NetCDFProfilesToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| NetCDF Time Series To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的时间序列（DSG）创建为要素类 | `arcpy.md.NetCDFTimeSeriesToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| NetCDF Trajectories To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的轨迹（DSG）创建为要素类 | `arcpy.md.NetCDFTrajectoriesToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| Raster to NetCDF | 把栅格数据集转换为 netCDF 文件 | `arcpy.md.RasterToNetCDF` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础写出，多家共有 |
| Table to NetCDF | 把表转换为 netCDF 文件 | `arcpy.md.TableToNetCDF` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础写出，多家共有 |

## 附：Esri 官方智能体／MCP 入口（官方文档发现）

七个工具箱的 3.4 工具参考页内未发现各自的智能体／MCP 入口；但在 Esri 官方开发者文档中发现平台级官方 MCP 入口一处，与本文件的 Geocoding 箱直接相关：

- **MCP for ArcGIS Location Services（beta）**——Esri 托管的 Model Context Protocol（MCP）服务器，使应用与 AI 智能体可经标准化 MCP 工具访问 ArcGIS Location Services（含 ArcGIS Geocoding service、Routing、Elevation、Places、底图与静态地图等），无需直接调用 ArcGIS REST API；需 ArcGIS Location Platform 或 ArcGIS Online 账号。官方文档：https://developers.arcgis.com/ai/mcp-arcgis-location-services/ ；官方发布说明（Esri 博客，2026-06-29 起 beta）：https://www.esri.com/arcgis-blog/products/platform/developers/mcp-support-beta-and-arcgis-static-maps-service-in-arcgis-location-platform-release
- 平台含义：地理编码类能力除 ArcPy GP 与 REST 两条复用通道外，新增第三条官方通道——Esri 托管 MCP；平台层可直接把该 MCP 作为 Geocoding 能力的上游轮子接入，只做翻译与治理。


> GIS 综合平台能力底账 · 分片：行业/平台类 21 个工具箱全量地理处理工具清单。
> 证据纪律：仅用 Esri 官方文档（一级证据）——ArcGIS Pro 工具参考（pro.arcgis.com / doc.esri.com 同源文档），逐箱打开总览页与每个 toolset 的 overview 页（Tool | Description 表）逐条抄录，未用论坛/博客，未凭记忆补条。
> 版本口径：任务指定 3.4 版工具参考；实际抓取时各箱官方总览页版本不一（Server、Parcels 历史分片为 3.4；Utility Network 为 3.1；Indoors、Oriented Imagery 为 3.2；Indoor Positioning、Public Transit 为 3.3；其余多为 latest/3.7），各节前提与状态注记以所据页面为准，不宣称全为 3.4。
> 平台判断口径：core＝概念通用、值得升为平台核心能力；extension＝行业数据模型/产品专属，留扩展命名空间；defer＝服务发布/工作流运维/需专门产品与数据，暂缓。
> 轮子来源口径（全部升级＋不重复造轮子）：绝大多数工具的官方现成实现即 ArcPy GP 工具本身，平台层桥直调即可；有 REST/托管等价通道的已在该列单独注明。
> 合计：21 箱、484 个工具，其中 core 50 条。

## GeoAI toolbox（arcpy.geoai）
工具集数：5；工具总数：18；前提：全部工具需另装深度学习框架库（Deep Learning Libraries）；模型可来自 ArcGIS Living Atlas 预训练模型或 arcgis.learn（ArcGIS API for Python）训练。官方定位：使用和训练处理地理空间与表格数据的 AI 模型，以现代机器学习/深度学习技术与 GIS 集成，含 embeddings 工具。

### Embeddings Based Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Extract Embeddings To Fields | 把 BLOB 字段中的向量 embeddings 抽取为新要素类的独立数值字段 | arcpy.geoai.ExtractEmbeddingsToFields | ArcPy GP（官方实现，桥直调） | core（embeddings 通用表示处理） |
| Find Similar Features Using Embeddings | 通过比较 embedding 表示对位置与影像数据做大规模相似检索 | arcpy.geoai.FindSimilarFeaturesUsingEmbeddings | ArcPy GP（官方实现，桥直调） | core（向量相似检索通用能力） |
| Generate Embeddings Using AI Models | 用基础模型为地理空间数据生成语义 embeddings | arcpy.geoai.GenerateEmbeddingsUsingAIModels | ArcPy GP（官方实现，桥直调） | core（基础模型 embedding 生成通用能力） |
| Merge Embeddings | 按重叠面积把 embeddings 合并到目标面（跨行政层级聚合） | arcpy.geoai.MergeEmbeddings | ArcPy GP（官方实现，桥直调） | extension（绑 ArcGIS embeddings 数据结构） |

### Feature and Tabular Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Predict Missing Values Using AI Model | 自动训练 ML/DL 模型估算并替换要素类/表中的缺失数值 | arcpy.geoai.PredictMissingValuesUsingAIModel | ArcPy GP（官方实现，桥直调） | core（通用表格缺失值填补） |
| Predict Using AutoML | 用 Train Using AutoML 产出的 .dlpk 模型对新数据做分类/回归预测 | arcpy.geoai.PredictUsingAutoML | ArcPy GP（官方实现，桥直调） | core（AutoML 推理通用能力） |
| Train Using AutoML | AutoML 自动完成 EDA、特征工程、选模、调参并输出最优模型 .dlpk 与性能指标 | arcpy.geoai.TrainUsingAutoML | ArcPy GP（官方实现，桥直调） | core（AutoML 训练通用能力） |

### Imagery AI toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Extract Features Using AI Models | 在输入栅格上运行一个或多个预训练深度学习模型提取要素并自动后处理推理输出 | arcpy.geoai.ExtractFeaturesUsingAIModels | ArcPy GP（官方实现，桥直调） | core（影像要素自动提取，概念通用） |
| Train Using AutoDL | 自动完成数据增强、选模、调参训练影像深度学习模型并输出 .dlpk | arcpy.geoai.TrainUsingAutoDL | ArcPy GP（官方实现，桥直调） | core（影像深度学习训练通用能力） |

### Text Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Classify Text Using Deep Learning | 用已训练文本分类模型为每条记录赋类别标签及置信度 | arcpy.geoai.ClassifyTextUsingDeepLearning | ArcPy GP（官方实现，桥直调） | core（文本分类通用 NLP 能力） |
| Extract Entities Using Deep Learning | 用 NER 模型从文本提取地址、人名、日期、金额等实体，含地址时可地理编码出要素类 | arcpy.geoai.ExtractEntitiesUsingDeepLearning | ArcPy GP（官方实现，桥直调） | core（实体抽取＋地理编码通用能力） |
| Process Text Using AI Model | 用自定义第三方或已训练模型处理文本（转换/识别/分类/生成/翻译/摘要等） | arcpy.geoai.ProcessTextUsingAIModel | ArcPy GP（官方实现，桥直调） | core（通用文本处理入口） |
| Train Entity Recognition Model | 训练从原始文本抽取预定义实体的 NER 模型 | arcpy.geoai.TrainEntityRecognitionModel | ArcPy GP（官方实现，桥直调） | core（NER 训练通用能力） |
| Train Text Classification Model | 训练单标签或多标签文本分类模型 | arcpy.geoai.TrainTextClassificationModel | ArcPy GP（官方实现，桥直调） | core（文本分类训练通用能力） |
| Train Text Transformation Model | 训练用于转换、翻译或摘要的文本转换模型 | arcpy.geoai.TrainTextTransformationModel | ArcPy GP（官方实现，桥直调） | core（文本转换训练通用能力） |
| Transform Text Using Deep Learning | 用 seq2seq 模型转换/翻译文本字段并写入新字段 | arcpy.geoai.TransformTextUsingDeepLearning | ArcPy GP（官方实现，桥直调） | core（文本转换通用能力） |

### Time Series AI toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Forecast Using Time Series Model | 用已训练深度学习时序模型预测时空立方体各位置的未来值 | arcpy.geoai.ForecastUsingTimeSeriesModel | ArcPy GP（官方实现，桥直调） | core（时空预测通用能力，输入为时空立方体） |
| Train Time Series Forecasting Model | 用时空立方体时序数据训练深度学习预测模型（FCN/LSTM/InceptionTime 等） | arcpy.geoai.TrainTimeSeriesForecastingModel | ArcPy GP（官方实现，桥直调） | core（时序预测训练通用能力） |

## Business Analyst toolbox（arcpy.ba）
工具集数：7；工具总数：47；前提：Business Analyst 许可；Target Marketing 全部工具另需本地含分群数据的 BA 数据集，部分工具消耗 ArcGIS Online credits。官方定位：执行市场分析基础 GIS 操作——人口报告、客户与竞品分布、商圈识别与数据变量可视化。

### Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Calculate Market Penetration | 按区域内客户数与人口等变量计算市场渗透率 | arcpy.ba.CalculateMarketPenetration | ArcPy GP（官方实现，桥直调） | extension（BA 人口数据专属） |
| Color Coded Layer | 按商业/人口/消费/景观变量创建多级尺度依赖分级设色图层 | arcpy.ba.ColorCodedLayer | ArcPy GP（官方实现，桥直调） | extension（BA 数据变量制图专属） |
| Enrich Layer | 为数据位置内部及周边添加人口与景观事实数据 | arcpy.ba.EnrichLayer | ArcPy GP（官方实现，桥直调）；另有 ArcGIS GeoEnrichment REST 服务等价接口 | extension（依赖 BA/GeoEnrichment 数据服务） |
| Find Nearby Locations | 按所选距离类型找出离输入要素最近的位置（可限数量/百分比/距离） | arcpy.ba.FindNearbyLocations | ArcPy GP（官方实现，桥直调） | extension（BA 选址场景包装） |
| Generate Desire Lines | 生成每个客户到关联门店的连线（蜘蛛图），可选风玫瑰报告 | arcpy.ba.GenerateDesireLines | ArcPy GP（官方实现，桥直调） | extension（零售分析专属） |
| Generate Grids and Hexagons | 为给定区域生成方形网格、六边形或 H3 六边形要素 | arcpy.ba.GenerateGridsAndHexagons | ArcPy GP（官方实现，桥直调） | core（网格/六边形生成通用能力） |
| Generate Points from Business Listings | 从商业网点检索生成点要素图层 | arcpy.ba.GeneratePointsFromBusinessListings | ArcPy GP（官方实现，桥直调） | extension（依赖 BA 商业名录数据） |

### Modeling toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Huff Model | 按距离与吸引力因子生成预测区域销售潜力的概率面 | arcpy.ba.HuffModel | ArcPy GP（官方实现，桥直调） | extension（零售引力模型＋BA 数据） |
| Huff Model Calibration | 计算 Huff Model 使用的指数参数值 | arcpy.ba.HuffModelCalibration | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Reports toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Import Business Analyst Report Template | 导入在线报告模板以便用本地 BA 数据集在本地运行 | arcpy.ba.ImportBusinessAnalystReportTemplate | ArcPy GP（官方实现，桥直调） | defer（BA 报告模板运维） |
| Summary Reports | 用标准或自定义模板为边界图层创建信息图与汇总报告 | arcpy.ba.SummaryReports | ArcPy GP（官方实现，桥直调） | defer（BA 报告生成，绑模板与数据） |

### Statistical Data Collections toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate SDCX Index | 为统计数据集合（SDCX）建索引以提升 Enrich 等分析性能 | arcpy.ba.GenerateSDCXIndex | ArcPy GP（官方实现，桥直调） | extension（BA 自定义数据专属） |

### Suitability Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Field Based Suitability Criteria | 添加基于输入图层数值字段的适宜性准则 | arcpy.ba.AddFieldBasedSuitabilityCriteria | ArcPy GP（官方实现，桥直调） | extension（BA 适宜性图层对象专属） |
| Add Point Layer Based Suitability Criteria | 添加基于与指定点图层空间关系的适宜性准则 | arcpy.ba.AddPointLayerBasedSuitabilityCriteria | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Variable Based Suitability Criteria | 添加基于 Enrich Layer 变量值的适宜性准则 | arcpy.ba.AddVariableBasedSuitabilityCriteria | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Calculate Suitability Score | 计算或重算适宜性得分 | arcpy.ba.CalculateSuitabilityScore | ArcPy GP（官方实现，桥直调） | extension（加权多准则概念通用，但实现绑 BA 图层） |
| Make Suitability Analysis Layer | 为输入站点面图层创建适宜性分析组图层 | arcpy.ba.MakeSuitabilityAnalysisLayer | ArcPy GP（官方实现，桥直调） | extension（BA 图层对象专属） |
| Remove Suitability Criteria | 从适宜性分析图层移除准则 | arcpy.ba.RemoveSuitabilityCriteria | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Criteria Properties | 定义准则参数 | arcpy.ba.SetCriteriaProperties | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Target Site | 向适宜性分析组图层添加目标站点 | arcpy.ba.SetTargetSite | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Target Marketing toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Analyze Market Area Gap | 生成显示总客户与期望客户差距的图层 | arcpy.ba.AnalyzeMarketAreaGap | ArcPy GP（官方实现，桥直调） | extension（BA 分群数据专属） |
| Analyze Market Potential | 生成按所选地理级别显示期望客户的图层 | arcpy.ba.AnalyzeMarketPotential | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Target Group | 创建容纳从本地 BA 数据集分群的目标组容器 | arcpy.ba.CreateTargetGroup | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Segmentation Profile | 把分群画像导出为表 | arcpy.ba.ExportSegmentationProfile | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Customer Demographic Profile Report | 用地理边界要素创建客户人口画像报告 | arcpy.ba.GenerateCustomerDemographicProfileReport | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Customer Segmentation Profile | 用已有客户图层创建分群画像 | arcpy.ba.GenerateCustomerSegmentationProfile | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Market Area Segmentation Profile | 汇总输入区域内标准地理边界的分群创建画像 | arcpy.ba.GenerateMarketAreaSegmentationProfile | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Segmentation Profile Report | 创建对比客户分群与研究区基准画像的报告 | arcpy.ba.GenerateSegmentationProfileReport | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Survey Report For Profile | 用消费调查数据显示目标画像的生活方式与偏好特征 | arcpy.ba.GenerateSurveyReportForProfile | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Survey Report For Targets | 显示核心/发展目标组与整体客户画像在各调查类别的头部特征 | arcpy.ba.GenerateSurveyReportForTargets | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Target Group Layer | 生成标识含所选分群地理单元并按目标分类的图层 | arcpy.ba.GenerateTargetGroupLayer | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Target Layer | 创建标识含/不含所选分群地理单元的图层 | arcpy.ba.GenerateTargetLayer | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Target Penetration Layer | 按所选分群渗透百分比生成显示目标分群浓度的图层 | arcpy.ba.GenerateTargetPenetrationLayer | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import Segmentation Profile | 从表生成分群画像 | arcpy.ba.ImportSegmentationProfile | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import Survey Profiles | 导入由调查变量数据组成的分群画像 | arcpy.ba.ImportSurveyProfiles | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Trade Areas toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Assign Customers By Distance | 按所选距离类型把客户分配给最近门店 | arcpy.ba.AssignCustomersByDistance | ArcPy GP（官方实现，桥直调） | extension（零售商圈专属） |
| Generate Approximate Drive Times | 用所选距离类型的可用路径近似已有面的大小形状生成商圈 | arcpy.ba.GenerateApproximateDriveTimes | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Customer Derived Trade Areas | 按每客户数量或量值属性围绕门店创建客户驱动商圈 | arcpy.ba.GenerateCustomerDerivedTradeAreas | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Drive Time Trade Area | 按行驶时间与距离围绕点要素创建商圈要素类 | arcpy.ba.GenerateDriveTimeTradeArea | ArcPy GP（官方实现，桥直调） | extension（驾驶时间商圈，依赖网络服务/数据） |
| Generate Geographies From Overlay | 从与输入有指定空间关系的标准地理级别要素生成商圈 | arcpy.ba.GenerateGeographiesFromOverlay | ArcPy GP（官方实现，桥直调） | extension（BA 标准地理专属） |
| Generate Standard Geography Trade Areas | 按预定义命名统计区域创建商圈（不耗 credits） | arcpy.ba.GenerateStandardGeographyTradeAreas | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Threshold Drive Times | 生成围绕点扩张直到达标的网络距离商圈 | arcpy.ba.GenerateThresholdDriveTimes | ArcPy GP（官方实现，桥直调） | extension（零售商圈专属） |
| Generate Threshold Rings | 生成围绕点扩张直到达阈值的环形商圈 | arcpy.ba.GenerateThresholdRings | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Trade Area Rings | 围绕点位置创建环形商圈 | arcpy.ba.GenerateTradeAreaRings | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Measure Cannibalization | 计算两个以上面的重叠量（相交之外的重叠程度） | arcpy.ba.MeasureCannibalization | ArcPy GP（官方实现，桥直调） | extension（门店蚕食分析专属） |
| Remove Overlap | 移除两个以上区域间的重叠形成相邻边界 | arcpy.ba.RemoveOverlap | ArcPy GP（官方实现，桥直调） | extension（商圈边界处理专属） |
| Remove Overlap (multiple) | 移除多个输入图层中面之间的重叠 | arcpy.ba.RemoveOverlapMultiple | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Crime Analysis and Safety toolbox（arcpy.ca）
工具集数：1 个 toolset＋根层工具；工具总数：13；前提：无单独扩展许可（随 ArcGIS Pro 提供，面向执法/公共安全分析）。官方定位：支持数据管理、案件筛选、战术与战略分析及犯罪模式调查的分析功能。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| 80-20 Analysis | 按关联案件数生成点簇/线/面并算累计百分比，找出案件 disproportionately 集中的地点 | arcpy.ca.EightyTwentyAnalysis | ArcPy GP（官方实现，桥直调） | extension（犯罪分析专属方法） |
| Add Date Attributes | 从日期字段派生星期、月、日、年等日期时间属性字段 | arcpy.ca.AddDateAttributes | ArcPy GP（官方实现，桥直调） | core（通用日期字段派生） |
| Feature To 3D By Time | 用输入要素的日期值创建 3D 要素类（时间作高度） | arcpy.ca.FeatureTo3DByTime | ArcPy GP（官方实现，桥直调） | extension（时空可视化专用） |
| Find Space Time Matches | 按邻近、时间范围或两者找出两个要素类之间的匹配 | arcpy.ca.FindSpaceTimeMatches | ArcPy GP（官方实现，桥直调） | core（通用时空匹配概念） |
| Join Attributes From Polygon | 把面要素属性连接到点要素 | arcpy.ca.JoinAttributesFromPolygon | ArcPy GP（官方实现，桥直调） | extension（通用连接的行业包装，与核心空间连接重复） |
| Select Layer By Date And Time | 按日期/时间范围或日期属性（星期、月、年等）选择记录 | arcpy.ca.SelectLayerByDateAndTime | ArcPy GP（官方实现，桥直调） | core（通用时间选择） |
| Summarize Incident Count | 生成带重合点计数的要素类（线/点按最大距离、面按叠加） | arcpy.ca.SummarizeIncidentCount | ArcPy GP（官方实现，桥直调） | extension（案件计数场景专属） |
| Summarize Percent Change | 计算两个等长对比时段点要素对应的百分比变化 | arcpy.ca.SummarizePercentChange | ArcPy GP（官方实现，桥直调） | extension（案件对比场景专属） |
| Update Features With Incident Records | 按坐标或街道地址把非空间表转点并更新已有数据集 | arcpy.ca.UpdateFeaturesWithIncidentRecords | ArcPy GP（官方实现，桥直调） | extension（案件记录入库专属） |

### Cell Phone Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Cell Phone Records To Feature Class | 导入运营商手机记录并按标识字段关联基站与扇区要素类 | arcpy.ca.CellPhoneRecordsToFeatureClass | ArcPy GP（官方实现，桥直调） | extension（手机取证分析专属） |
| Cell Site Records To Feature Class | 按经纬度、方位角、波束宽度与半径从基站表生成基站点与扇区面 | arcpy.ca.CellSiteRecordsToFeatureClass | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Call Links | 按通话开始时间用基站点/扇区生成表示通话链路的线要素 | arcpy.ca.GenerateCallLinks | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Sector Lines | 生成表示基站天线扇区范围的线要素 | arcpy.ca.GenerateSectorLines | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Defense toolbox（arcpy.defense）
工具集数：4（其中 Gridded Reference Graphic 下含 Number and Letter 子 toolset）；工具总数：23；前提：内置工具箱（源自原 Military Tools），部分工具需 Advanced 许可、3D Analyst 或 Spatial Analyst 许可。官方定位：自动化确定位置、距离、射程与可见性的分析流程（工具参考位于 tool-reference/defense）。

### Conversion toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Coordinate Table To 2-Point Line | 从表中坐标创建两点线要素 | arcpy.defense.CoordinateTableTo2PointLine | ArcPy GP（官方实现，桥直调） | core（表→要素构造与坐标格式互转，概念通用） |
| Coordinate Table To Ellipse | 从表中坐标与输入值创建椭圆要素 | arcpy.defense.CoordinateTableToEllipse | ArcPy GP（官方实现，桥直调） | core（同上） |
| Coordinate Table To Line Of Bearing | 从表中坐标创建方位线 | arcpy.defense.CoordinateTableToLineOfBearing | ArcPy GP（官方实现，桥直调） | core（同上） |
| Coordinate Table To Point | 从表中坐标创建点要素类（支持 DD/DMS/MGRS/USNG/GARS/GEOREF 等格式） | arcpy.defense.CoordinateTableToPoint | ArcPy GP（官方实现，桥直调） | core（同上） |
| Coordinate Table To Polygon | 从表中坐标创建面要素 | arcpy.defense.CoordinateTableToPolygon | ArcPy GP（官方实现，桥直调） | core（同上） |
| Coordinate Table To Polyline | 从表中坐标创建折线要素类 | arcpy.defense.CoordinateTableToPolyline | ArcPy GP（官方实现，桥直调） | core（同上） |
| Generate Coordinate Notations | 把表中源坐标转换为多种坐标表示格式 | arcpy.defense.GenerateCoordinateNotations | ArcPy GP（官方实现，桥直调） | core（坐标表示法互转，概念通用） |

### Distance and Direction toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate Range Fans | 按起止水平角与最小/最大距离从起点创建射程扇面 | arcpy.defense.GenerateRangeFans | ArcPy GP（官方实现，桥直调） | extension（军事射程表达构造） |
| Generate Range Fans From Features | 用点要素类字段属性批量创建射程扇面 | arcpy.defense.GenerateRangeFansFromFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Range Rings | 按环数与间距（或最小/最大距离）从点创建同心距离环 | arcpy.defense.GenerateRangeRings | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Range Rings From Features | 用点要素类字段属性批量创建距离环 | arcpy.defense.GenerateRangeRingsFromFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Gridded Reference Graphic toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate Grid From Area | 在边界多边形范围上按自定义尺寸生成 GRG 格网 | arcpy.defense.GenerateGridFromArea | ArcPy GP（官方实现，桥直调） | extension（GRG 军事参考格网专属） |
| Generate Grid From Point | 以点为中心按自定义尺寸生成 GRG 格网面要素类 | arcpy.defense.GenerateGridFromPoint | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Reference System Grid From Area | 在边界多边形范围上按世界参考系统生成 GRG 格网 | arcpy.defense.GenerateReferenceSystemGridFromArea | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Gridded Reference Graphic > Number and Letter toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Letter Features | 给一组要素的新/已有字段赋顺序字母 | arcpy.defense.LetterFeatures | ArcPy GP（官方实现，桥直调） | core（顺序编号概念通用） |
| Letter Intersections | 识别线要素类交点并给输出点赋顺序字母 | arcpy.defense.LetterIntersections | ArcPy GP（官方实现，桥直调） | extension（绑 GRG 编号场景） |
| Number Features | 给一组输入要素的新/已有字段赋顺序数字 | arcpy.defense.NumberFeatures | ArcPy GP（官方实现，桥直调） | core（顺序编号概念通用） |
| Number Features By Sector | 按要素所属地理分组赋顺序数字 | arcpy.defense.NumberFeaturesBySector | ArcPy GP（官方实现，桥直调） | extension（绑 GRG 分区场景） |

### Visibility toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Find Highest Or Lowest Point | 找定义区域内输入表面的最高或最低点 | arcpy.defense.FindHighestOrLowestPoint | ArcPy GP（官方实现，桥直调） | core（表面极值概念通用） |
| Find Local Peaks Or Valleys | 找定义区域内的局部峰值或谷值 | arcpy.defense.FindLocalPeaksOrValleys | ArcPy GP（官方实现，桥直调） | core（同上） |
| Linear Line Of Sight | 在观察者与目标之间创建通视线 | arcpy.defense.LinearLineOfSight | ArcPy GP（官方实现，桥直调） | core（通视分析概念通用） |
| Radial Line Of Sight | 显示一个或多个观察点可见的区域（视域） | arcpy.defense.RadialLineOfSight | ArcPy GP（官方实现，桥直调） | core（视域分析概念通用） |
| Radial Line Of Sight And Range | 按指定距离与视角显示观察点可见区域 | arcpy.defense.RadialLineOfSightAndRange | ArcPy GP（官方实现，桥直调） | extension（叠加射程约束的军事变体） |

## AllSource toolbox（arcpy.intelligence）
工具集数：3 个一级 toolset（Analysis 下另含 Blind Spot、Suitability 两个子 toolset）；工具总数：18；前提：ArcGIS AllSource 独立产品（情报分析桌面应用，源自 ArcGIS Pro Intelligence 配置）。官方定位：转换和分析情报数据源——批量导入多源数据、分析点轨迹模式、评估机动/着陆区适宜性。

### Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Find Overlaps | 找出要素类中的重叠区域并给出重叠计数 | arcpy.intelligence.FindOverlaps | ArcPy GP（官方实现，桥直调） | extension（通用叠加的情报包装） |

### Blind Spot toolset（Analysis 下）
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate Blind Spot Areas | 按起止时间为 ISR/巡逻可见缓冲生成不可见区（盲区），配合时间滑块探索覆盖缺口 | arcpy.intelligence.GenerateBlindSpotAreas | ArcPy GP（官方实现，桥直调） | extension（ISR/巡逻情报专属） |
| Generate Coverage Areas | 为 ISR/巡逻资产生成邻近缓冲供盲区分析使用 | arcpy.intelligence.GenerateCoverageAreas | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Suitability toolset（Analysis 下）
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| DOF To Obstacle Features | 把 FAA 数字障碍物文件（DOF）转为障碍点与障碍缓冲要素 | arcpy.intelligence.DOFToObstacleFeatures | ArcPy GP（官方实现，桥直调） | extension（航空障碍情报专属） |
| Drop Zone Suitability | 按坡度与植被在指定 AOI 内识别适合空投装备/人员的空投区 | arcpy.intelligence.DropZoneSuitability | ArcPy GP（官方实现，桥直调） | extension（军事空投专属） |
| Generate HLZ Suitability | 由重分类坡度、土地覆盖与障碍缓冲生成直升机着陆区适宜性栅格 | arcpy.intelligence.GenerateHLZSuitability | ArcPy GP（官方实现，桥直调） | extension（军事着陆区专属） |
| Generate Obstacle Features | 把带高度字段的要素转为 3D 障碍要素与障碍限制缓冲 | arcpy.intelligence.GenerateObstacleFeatures | ArcPy GP（官方实现，桥直调） | extension（着陆区评估专属） |
| Least Cost Path | 跨成本面求起点到终点的最短路径 | arcpy.intelligence.LeastCostPath | ArcPy GP（官方实现，桥直调） | extension（成本路径概念通用，实现为情报工具箱包装） |

### Conversion toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Batch Import Data | 把 KML/KMZ/shapefile/Excel/文本表/GeoJSON/GPX 批量导入单个地理数据库要素类 | arcpy.intelligence.BatchImportData | ArcPy GP（官方实现，桥直调） | core（多格式批量导入通用能力） |
| Create Location File From Text File | 从 GeoNames/NGA GNS/USGS GNIS 文本文件创建 LocateXT 位置文件 | arcpy.intelligence.CreateLocationFileFromTextFile | ArcPy GP（官方实现，桥直调） | extension（LocateXT 产品专属） |
| Military Raster To Mosaic Dataset | 把 CADRG/ECRG/CIB/DTED/HRE 军用栅格导入一个或多个镶嵌数据集 | arcpy.intelligence.MilitaryRasterToMosaicDataset | ArcPy GP（官方实现，桥直调） | extension（军用栅格格式专属） |
| Points To Track Segments | 把带时间的点序列（如 GPS 点）转换为一系列路径 | arcpy.intelligence.PointsToTrackSegments | ArcPy GP（官方实现，桥直调） | core（轨迹点转路径通用能力） |

### Movement toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Classify Movement Events | 从点轨迹数据识别转弯、加速事件与速度 | arcpy.intelligence.ClassifyMovementEvents | ArcPy GP（官方实现，桥直调；官方注明借力 GeoAnalytics Desktop 工具箱） | core（轨迹事件分类通用能力；官方注明借力 GeoAnalytics Desktop） |
| Compare Areas | 跨多个已知 AOI 比较移动点轨迹 | arcpy.intelligence.CompareAreas | ArcPy GP（官方实现，桥直调；官方注明借力 GeoAnalytics Desktop 工具箱） | extension（轨迹情报场景） |
| Find Cotravelers | 提取在指定时空间隔内共同移动的唯一标识（同行者） | arcpy.intelligence.FindCotravelers | ArcPy GP（官方实现，桥直调；官方注明借力 GeoAnalytics Desktop 工具箱） | extension（轨迹情报专属） |
| Find Frequented Locations | 按轨迹标识聚合识别轨迹多次停留的常去地点 | arcpy.intelligence.FindFrequentedLocations | ArcPy GP（官方实现，桥直调；官方注明借力 GeoAnalytics Desktop 工具箱） | core（轨迹停留点挖掘通用概念） |
| Find Meeting Locations | 识别多条不同轨迹在定义时段内共同停留的会面地点 | arcpy.intelligence.FindMeetingLocations | ArcPy GP（官方实现，桥直调；官方注明借力 GeoAnalytics Desktop 工具箱） | extension（轨迹情报专属） |
| Select Movement Tracks | 按 AOI 选择移动轨迹 | arcpy.intelligence.SelectMovementTracks | ArcPy GP（官方实现，桥直调；官方注明借力 GeoAnalytics Desktop 工具箱） | extension（轨迹情报场景） |

## Aviation toolbox（arcpy.aviation）
工具集数：2 个一级 toolset（Airports 下 3 个子 toolset、Charting 下 4 个子 toolset）；工具总数：40；前提：Airports 部分需 Aviation Airports 许可、Charting 部分需 Aviation Charting 许可（均需 Standard 级别；LAS 相关另需 3D Analyst）。官方定位：创建、分析和管理航空内容（AIS/Airports 数据模型）。

### Airports > Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Analyze Airport Features | 分析机场周边指定点要素，记录距跑道中心线/最近跑道端距离及最近跑道编号 | arcpy.aviation.AnalyzeAirportFeatures | ArcPy GP（官方实现，桥直调） | extension（机场数据模型专属） |
| Analyze LAS Runway Obstacles | 分析激光雷达数据与 OIS，判断 lidar 点是否穿透障碍物识别面 | arcpy.aviation.AnalyzeLASRunwayObstacles | ArcPy GP（官方实现，桥直调） | extension（航空障碍分析专属） |
| Analyze Runway Obstacles | 分析障碍物数据与 OIS，判断障碍物是否穿透 | arcpy.aviation.AnalyzeRunwayObstacles | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate OIS Obstacle Data | 生成存入 OIS multipatch 的 OBSTACLEJSON，供地形与障碍物剖面布局元素描绘进近面内障碍 | arcpy.aviation.GenerateOISObstacleData | ArcPy GP（官方实现，桥直调） | extension（航空制图布局专属） |
| Generate OIS Profile Data | 生成存入 OIS 的 PROFILEJSON，供剖面布局元素描绘地形、跑道与 OIS | arcpy.aviation.GenerateOISProfileData | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Airports > Data Exchange toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Export 18B Shapefiles | 从含 Airports 模式的地理数据库导出 FAA 18B 合规 shapefile | arcpy.aviation.Export18BShapefiles | ArcPy GP（官方实现，桥直调） | extension（FAA 18B 标准专属） |
| Import 18B Shapefiles | 把 FAA 18B 合规 shapefile 导入含 18B 模式的地理数据库 | arcpy.aviation.Import18BShapefiles | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Airports > Obstruction Identification Surfaces toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create Curved Approach | 按所选规范（如 ICAO Annex 15、FAA 18B）与输入航迹创建弯曲进近 OIS | arcpy.aviation.CreateCurvedApproach | ArcPy GP（官方实现，桥直调） | extension（OIS 规范专属） |
| FAA 13A | 按 FAA AC 150/5300-13A 创建进近/离场障碍物识别面 | arcpy.aviation.FAA13A | ArcPy GP（官方实现，桥直调） | extension（同上） |
| FAA 18B | 按 FAA AC 150/5300-18B 创建 OIS 以识别助航危害与关键进近/离场障碍 | arcpy.aviation.FAA18B | ArcPy GP（官方实现，桥直调） | extension（同上） |
| FAA FAR 77 | 按 FAA Part 77 创建 OIS（影响可通航空域物体的标准） | arcpy.aviation.FAAFAR77 | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate OIS Intersection | 在全部组合面范围内创建最严格（最低）的面 | arcpy.aviation.GenerateOISIntersection | ArcPy GP（官方实现，桥直调） | extension（同上） |
| ICAO Annex 14 | 按 ICAO Annex 14 创建界定机场周边无障碍空域的 OIS | arcpy.aviation.ICAOAnnex14 | ArcPy GP（官方实现，桥直调） | extension（同上） |
| ICAO Annex 15 | 按 ICAO Annex 15（Area 2a/2b/2c）创建 OIS 以定高限或移除危害障碍 | arcpy.aviation.ICAOAnnex15 | ArcPy GP（官方实现，桥直调） | extension（同上） |
| ICAO Annex 4 | 按 ICAO Annex 4 为精密进近地形图创建 OIS | arcpy.aviation.ICAOAnnex4 | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Light Signal Clearance Surface | 按 FAA EB 95 创建 PAPI 障碍物净空面（灯光信号） | arcpy.aviation.LightSignalClearanceSurface | ArcPy GP（官方实现，桥直调） | extension（同上） |
| PAPI Obstacle Clearance Surface | 创建 PAPI 障碍物净空面，穿透者判为垂直障碍物 | arcpy.aviation.PAPIObstacleClearanceSurface | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Unified Facilities Criteria | 按 UFC 3-260-01（MIL-STD 3007）创建美国国防部 OIS | arcpy.aviation.UnifiedFacilitiesCriteria | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Charting > Cartography toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Aviation Line Bypass | 调整与点要素重叠的航线折线要素（绕行） | arcpy.aviation.AddAviationLineBypass | ArcPy GP（官方实现，桥直调） | extension（航空制图专属） |
| Aggregate Obstacles | 在给定半径内聚合点障碍物，以组内最高障碍代表整组 | arcpy.aviation.AggregateObstacles | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Airway Corridors | 简化为指定 ATS 航路创建航路走廊与喇叭口 | arcpy.aviation.GenerateAirwayCorridors | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Rotate Aviation Features | 把要素对齐到格网或页面 | arcpy.aviation.RotateAviationFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Update Aviation Annotation | 批量更新航空专用注记图层以简化航图生产与整饰 | arcpy.aviation.UpdateAviationAnnotation | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Charting > Data Exchange toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Export AIXM 5.1 Message | 把航空数据导出为 AIXM 5.1 消息 | arcpy.aviation.ExportAIXM51Message | ArcPy GP（官方实现，桥直调） | extension（AIXM 标准＋AIS 模型专属） |
| Import AIXM 5.1 Message | 把 AIXM 5.1 数据导入航空地理数据库 | arcpy.aviation.ImportAIXM51Message | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import DCDT Change File | 把 NGA 数字航图数据事务（DCDT）变更文件导入航空地理数据库 | arcpy.aviation.ImportDCDTChangeFile | ArcPy GP（官方实现，桥直调） | extension（NGA 数据专属） |
| Import Digital Obstacle File | 用数字障碍物文件（DOF）增删改输入障碍要素类的障碍点 | arcpy.aviation.ImportDigitalObstacleFile | ArcPy GP（官方实现，桥直调） | extension（DOF 格式专属） |

### Charting > Data Management toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Calculate ATS Route Attributes | 计算 ATS 航路要素的段距离与方位属性（可含 FAA 专用属性） | arcpy.aviation.CalculateATSRouteAttributes | ArcPy GP（官方实现，桥直调） | extension（AIS 模型专属） |
| Generate Airspace Areas | 从 Airspace 要素生成 AirspaceArea 要素 | arcpy.aviation.GenerateAirspaceAreas | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Airspace Lines | 从输入空域面边缘生成 AirspaceLine 线要素 | arcpy.aviation.GenerateAirspaceLines | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Aviation Cartographic Features | 按要素所在 AOI 创建制图要素 | arcpy.aviation.GenerateAviationCartographicFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Changeover Points | 沿由有序 ATSRoute 段组成的航路集合创建转换点 | arcpy.aviation.GenerateChangeoverPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Derived Airspace Geometry | 从导入的 AIXM 5.1 消息为空域要素生成空域几何 | arcpy.aviation.GenerateDerivedAirspaceGeometry | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Procedure Leg Geometry | 从程序航段生成几何，修正缺失正确几何的 AIXM 数据 | arcpy.aviation.GenerateProcedureLegGeometry | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Summary Table Data | 从源制图要素类与 AIS 相关表收集信息输出到独立表 | arcpy.aviation.GenerateSummaryTableData | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Group Route Segments | 从单个段派生航路总距离等累计信息以备制图 | arcpy.aviation.GroupRouteSegments | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Prepare Aviation Data | 按 JSON 脚本把主航空数据属性迁移到制图要素供标注与符号化 | arcpy.aviation.PrepareAviationData | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Process Air Traffic Service Routes | 识别重叠 ATS 航路并计算目标制图航路要素字段以助制图显示 | arcpy.aviation.ProcessAirTrafficServiceRoutes | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Report Aviation Chart Changes | 比较两个企业地理数据库版本的要素类并报告差异（可按 AOI/定义查询过滤受影响航图） | arcpy.aviation.ReportAviationChartChanges | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Charting > Layout toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate Aviation Chart Leads | 在地图框边界与线要素交点处创建文本图形（航图引线） | arcpy.aviation.GenerateAviationChartLeads | ArcPy GP（官方实现，桥直调） | extension（航空布局专属） |

## Bathymetry toolbox（arcpy.bathymetry）
工具集数：3；工具总数：10；前提：Maritime Bathymetry 许可；Smooth Bathymetric TIN 另需 3D Analyst。官方定位：管理测深（水深）数据——创建/管理水深信息系统（BIS）、由 BIS 生成产品与导出、综合水深点与 TIN。

### BIS Data toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| BIS To Mosaic Dataset | 从水深信息系统（BIS）创建镶嵌数据集 | arcpy.bathymetry.BISToMosaicDataset | ArcPy GP（官方实现，桥直调） | extension（BIS 模型专属） |
| Export BIS Points | 从注册到 BIS 的点/多点/shapefile 点/LAS 导出点要素类（可按查询文件过滤排序、去重叠） | arcpy.bathymetry.ExportBISPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Footprints | 把 BisCatalog 的足迹导出到输出要素类 | arcpy.bathymetry.ExportFootprints | ArcPy GP（官方实现，桥直调） | extension（同上） |

### BIS Management toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Data To BIS | 把栅格与要素类数据注册到 BIS | arcpy.bathymetry.AddDataToBIS | ArcPy GP（官方实现，桥直调） | extension（BIS 模型专属） |
| Add Point Data To BIS | 把点云或高程点数据注册到 BIS | arcpy.bathymetry.AddPointDataToBIS | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Analyze BIS | 分析一个水深信息系统（BIS） | arcpy.bathymetry.AnalyzeBIS | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create BIS | 在指定地理数据库工作区创建 BIS | arcpy.bathymetry.CreateBIS | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Remove Data From BIS | 从 BIS 地理数据库移除数据 | arcpy.bathymetry.RemoveDataFromBIS | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Utilities toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Reduce Point Density | 稀疏点或多点要素类的点 | arcpy.bathymetry.ReducePointDensity | ArcPy GP（官方实现，桥直调） | extension（水深点综合专属；与 Maritime 箱同名工具重复） |
| Smooth Bathymetric TIN | 以严格保留浅水偏置的方式平滑 TIN 数据集 | arcpy.bathymetry.SmoothBathymetricTIN | ArcPy GP（官方实现，桥直调） | extension（测深 TIN 专属） |

## Maritime toolbox（arcpy.maritime）
工具集数：2 个 toolset（S-57 下另含 Management、Validation 子 toolset）＋根层工具；工具总数：14；前提：Maritime Charting / Maritime Bathymetry 许可；Generate Depth Areas 另需 3D Analyst。官方定位：管理 S-57、S-100 与测深数据（注：3.1 版总览曾含 Cartography、VPF 两个 toolset，2.9 及以后总览仅列 S-57、S-100，本表以较新总览为准）。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate Depth Areas | 用 TIN 查询深度判断闭合等深线趋势，创建深度区域面要素 | arcpy.maritime.GenerateDepthAreas | ArcPy GP（官方实现，桥直调） | extension（海图深度区专属） |
| Generate Land Areas | 识别海岸线等陆地拓扑要素并排除水域等，创建陆地区域面要素 | arcpy.maritime.GenerateLandAreas | ArcPy GP（官方实现，桥直调） | extension（海图陆地区专属） |
| Reduce Point Density | 稀疏点或多点要素类的点 | arcpy.maritime.ReducePointDensity | ArcPy GP（官方实现，桥直调） | extension（测深点综合专属；与 Bathymetry 箱同名工具重复） |
| Smooth Bathymetric TIN | 以严格保留浅水偏置的方式平滑 TIN | arcpy.maritime.SmoothBathymetricTIN | ArcPy GP（官方实现，桥直调） | extension（测深 TIN 专属） |

### S-57 > Management toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Copy S-57 Features | 把一个或多个图层的要素复制到目标地理数据库 | arcpy.maritime.CopyS57Features | ArcPy GP（官方实现，桥直调） | extension（S-57 模型专属） |
| Create S-57 Exchange Set | 创建 S-57 交换集供 ECDIS 显示电子海图数据集 | arcpy.maritime.CreateS57ExchangeSet | ArcPy GP（官方实现，桥直调） | extension（S-57 产品专属） |
| Export Geodatabase to S-57 | 把 Maritime 地理数据库的水文数据导出为 S-57 文件 | arcpy.maritime.ExportGeodatabaseToS57 | ArcPy GP（官方实现，桥直调） | extension（S-57 标准专属） |
| Import S-57 to Geodatabase | 把 S-57 文件导入 Maritime 地理数据库 | arcpy.maritime.ImportS57ToGeodatabase | ArcPy GP（官方实现，桥直调） | extension（同上） |

### S-57 > Validation toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Repair Nautical Data | 对 Nautical 模式数据库修复未共位结构-设备要素、删除游离记录、处理 LNAM 空/无效/重复值等 | arcpy.maritime.RepairNauticalData | ArcPy GP（官方实现，桥直调） | extension（S-57 数据修复专属） |
| Validate S-57 File | 验证 ENC/IENC/bIENC 文件并生成 .S58 文件与 shapefile 结果 | arcpy.maritime.ValidateS57File | ArcPy GP（官方实现，桥直调） | extension（S-58 验证专属） |

### S-100 toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Convert S-57 to S-101 Cell | 把存储海图数据的 S-57 矢量产品转换为新矢量 S-101 格式 | arcpy.maritime.ConvertS57ToS101Cell | ArcPy GP（官方实现，桥直调） | extension（S-100 系列标准专属） |
| Export S-101 Cell | 把地理数据库的 S-101 水文数据导出为 S-101 文件 | arcpy.maritime.ExportS101Cell | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import S-100 Cell | 把 S-100 水文数据导入由相关 S-100 要素目录创建的地理数据库 | arcpy.maritime.ImportS100Cell | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import S-100 Feature Catalogue | 把 S-100 要素目录（描述数据产品内容的 XML）内容导入已有地理数据库 | arcpy.maritime.ImportS100FeatureCatalogue | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Indoors toolbox（arcpy.indoors）
工具集数：1 个 toolset＋根层工具；工具总数：16；前提：组织需 Indoors 扩展许可。官方定位：向地理数据库添加托管 ArcGIS Indoors 数据所需的数据集、要素类、表与配置（Indoors Information Model）。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create Indoor Dataset | 按 Indoors 信息模型精简模式创建维护楼层平面数据的室内数据集 | arcpy.indoors.CreateIndoorDataset | ArcPy GP（官方实现，桥直调） | extension（Indoors 模型专属） |
| Create Indoor 3D Dataset | 创建含 multipatch 要素类的室内 3D 数据集以备楼层平面 3D 场景 | arcpy.indoors.CreateIndoor3DDataset | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Indoors Database | 创建符合 Indoors 信息模型的地理数据库（楼层制图/路径/空间规划/工位预订） | arcpy.indoors.CreateIndoorsDatabase | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Unit Openings | 生成表示入口位置与物理范围的单元开口线要素 | arcpy.indoors.GenerateUnitOpenings | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import BIM To Indoor Dataset | 把 BIM 文件要素导入室内数据集以备楼层感知地图与室内路径网络 | arcpy.indoors.ImportBIMToIndoorDataset | ArcPy GP（官方实现，桥直调） | extension（BIM→Indoors 模型专属转换） |
| Import CAD To Indoor Dataset | 把 CAD 文件要素导入室内数据集 | arcpy.indoors.ImportCADToIndoorDataset | ArcPy GP（官方实现，桥直调） | extension（CAD→Indoors 模型专属转换） |
| Import IFC To Indoor Dataset | 把 IFC 文件要素导入室内数据集 | arcpy.indoors.ImportIFCToIndoorDataset | ArcPy GP（官方实现，桥直调） | extension（IFC→Indoors 模型专属转换） |
| Import Floorplans To Indoors Geodatabase | 把 CAD 楼层平面导入 Indoors 工作区 | arcpy.indoors.ImportFloorplansToIndoorsGeodatabase | ArcPy GP（官方实现，桥直调） | extension（Indoors 模型专属） |
| Update Occupant Features | 更新符合 Indoors 信息模型的 Occupants 要素类 | arcpy.indoors.UpdateOccupantFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Upgrade Indoors Database | 把已有 Indoors 工作区模式升级到最新信息模型 | arcpy.indoors.UpgradeIndoorsDatabase | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Indoors Network toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Classify Indoor Pathways | 把穿过会议室/服务区等所选单元空间的路径分类为低优先级 | arcpy.indoors.ClassifyIndoorPathways | ArcPy GP（官方实现，桥直调） | extension（室内网络专属） |
| Create Indoor Network Dataset | 创建支持室内可路由网络的室内网络数据集 | arcpy.indoors.CreateIndoorNetworkDataset | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Facility Entryways | 创建或更新表示设施出入口的点 | arcpy.indoors.GenerateFacilityEntryways | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Floor Transitions | 创建或更新垂直连接楼层的过渡线要素 | arcpy.indoors.GenerateFloorTransitions | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Indoor Pathways | 按墙/柱等障碍切割生成初步室内路径 | arcpy.indoors.GenerateIndoorPathways | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Thin Indoor Pathways | 删减路由不需要的初步路径以减小网络并提升求解性能 | arcpy.indoors.ThinIndoorPathways | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Indoor Positioning toolbox（arcpy.indoorpositioning）
工具集数：2；工具总数：8；前提：组织需 ArcGIS IPS 扩展许可，配合 IPS Setup App 采集。官方定位：创建 ArcGIS IPS 信息模型，支持室内调查、调查数据处理与室内定位，并评估部署性能。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create IPS Data Model | 创建含定位数据集/信号/定位点/记录/信标的 IPS 数据模型 | arcpy.indoorpositioning.CreateIPSDataModel | ArcPy GP（官方实现，桥直调） | extension（IPS 模型专属） |
| Generate Indoor Positioning Dataset | 用基于调查或无调查方法为已有 IPS 安装生成室内定位数据集 | arcpy.indoorpositioning.GenerateIndoorPositioningDataset | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Share Indoor Positioning Data Service | 把室内定位数据服务发布到 Enterprise 或 Online 供 Maps SDK 定位 | arcpy.indoorpositioning.ShareIndoorPositioningDataService | ArcPy GP（官方实现，桥直调；动作本质为向门户发布服务） | defer（服务发布，绑 IPS 产品） |

### Classic toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Enable Indoor Positioning | 在已有地理数据库中创建存储 IPS 数据所需的要素类与表（旧模型） | arcpy.indoorpositioning.EnableIndoorPositioning | ArcPy GP（官方实现，桥直调） | extension（IPS 旧模型兼容） |
| Generate Indoor Positioning File | 从 IPS Setup 调查记录生成定位文件 | arcpy.indoorpositioning.GenerateIndoorPositioningFile | ArcPy GP（官方实现，桥直调） | extension（IPS 专属） |
| Generate Indoor Positioning File Without Survey | 模拟蓝牙信号传播，从信标与楼层平面数据无调查生成定位文件 | arcpy.indoorpositioning.GenerateIndoorPositioningFileWithoutSurvey | ArcPy GP（官方实现，桥直调） | extension（IPS 专属） |

### Quality Assessment toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create IPS Quality Dataset | 创建用于评估 IPS 部署质量的数据集 | arcpy.indoorpositioning.CreateIPSQualityDataset | ArcPy GP（官方实现，桥直调） | extension（IPS 质量评估专属） |
| Compute Positioning Quality | 填充 IPS Quality 数据集以计算定位质量 | arcpy.indoorpositioning.ComputePositioningQuality | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Oriented Imagery toolbox（arcpy.oi）
工具集数：2；工具总数：4；前提：无单独扩展（ArcGIS Pro 3.2 起内置的定向影像能力，发布需 Enterprise 11.2/Online）。官方定位：创建、管理和维护定向影像数据集与图层。

### Authoring toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Images To Oriented Imagery Dataset | 从文件/文件夹/表/路径列表/点图层向定向影像数据集添加影像 | arcpy.oi.AddImagesToOrientedImageryDataset | ArcPy GP（官方实现，桥直调） | core（非正射影像纳入 GIS 的通用数据模型概念） |
| Build Oriented Imagery Footprint | 为定向影像数据集构建覆盖足迹要素类 | arcpy.oi.BuildOrientedImageryFootprint | ArcPy GP（官方实现，桥直调） | extension（定向影像数据集专属配套） |
| Create Oriented Imagery Dataset | 在地理数据库中创建空的定向影像数据集 | arcpy.oi.CreateOrientedImageryDataset | ArcPy GP（官方实现，桥直调） | core（通用影像集合数据模型概念） |

### Manage toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Update Oriented Imagery Dataset Properties | 更新或修改定向影像数据集属性 | arcpy.oi.UpdateOrientedImageryDatasetProperties | ArcPy GP（官方实现，桥直调） | extension（定向影像数据集专属维护） |

## Parcels toolbox（arcpy.parcel）
工具集数：1 个 toolset＋根层工具；工具总数：24；前提：Parcel Fabric 数据模型（地籍宗地编织网）；注：Validate Parcel Fabric 已于 3.0 弃用（官方工具箱历史），未计入。官方定位：创建、管理宗地编织网并向其加载数据。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Analyze Parcels By Least Squares Adjustment | 对宗地测量网做最小二乘平差，评估并改进宗地角点坐标精度 | arcpy.parcel.AnalyzeParcelsByLeastSquaresAdjustment | ArcPy GP（官方实现，桥直调） | extension（宗地测量专属） |
| Append Parcels | 把输入宗地编织网的宗地追加到目标编织网 | arcpy.parcel.AppendParcels | ArcPy GP（官方实现，桥直调） | extension（编织网模型专属） |
| Apply Parcel Least Squares Adjustment | 把平差结果（AdjustmentLines/Points）应用到宗地线/连接线/点 | arcpy.parcel.ApplyParcelLeastSquaresAdjustment | ArcPy GP（官方实现，桥直调） | extension（宗地测量专属） |
| Build Parcel Fabric | 从面或线构建宗地（补齐线、点或面，线构建需种子） | arcpy.parcel.BuildParcelFabric | ArcPy GP（官方实现，桥直调） | extension（编织网模型专属） |
| Copy Parcels | 把宗地复制到新要素数据集中的新编织网 | arcpy.parcel.CopyParcels | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Parcel Seeds | 为与指定宗地记录关联的闭合线环创建宗地种子 | arcpy.parcel.CreateParcelSeeds | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Delete Parcels | 删除所选宗地（无选择时删除全部） | arcpy.parcel.DeleteParcels | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Duplicate Parcels | 在同/不同宗地类型中复制宗地，或多次复制生成分层（楼层）宗地 | arcpy.parcel.DuplicateParcels | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Parcel Record Features | 把与所选宗地记录关联的要素导出为单独要素类 | arcpy.parcel.ExportParcelRecordFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Sequenced Parcel Features | 按顺时针序号导出所选宗地要素以便制图与列表 | arcpy.parcel.ExportSequencedParcelFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Find Adjacent Parcel Points | 找出重合或距离小于容差的宗地点 | arcpy.parcel.FindAdjacentParcelPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Find Gaps And Overlaps | 找出宗地图层内/之间的缝隙与重叠并输出为面要素 | arcpy.parcel.FindGapsAndOverlaps | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Parcel Fabric Links | 为指定时段内位置变化的编织网点生成位移链接 | arcpy.parcel.GenerateParcelFabricLinks | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import Parcel Fabric Points | 把源点数据按邻近容差导入编织网点要素类 | arcpy.parcel.ImportParcelFabricPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Merge Collinear Parcel Boundaries | 把相连共线宗地线合并为一条（共享点转为顶点） | arcpy.parcel.MergeCollinearParcelBoundaries | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Select Parcel Features | 选择输入宗地面关联的点与线 | arcpy.parcel.SelectParcelFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Parcel Line Label Position | 设置宗地线 COGO 尺寸标注在左侧/右侧/居中 | arcpy.parcel.SetParcelLineLabelPosition | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Administration toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Parcel Type | 向编织网添加由独立面/线要素类定义的宗地类型 | arcpy.parcel.AddParcelType | ArcPy GP（官方实现，桥直调） | extension（编织网管理专属） |
| Create Parcel Fabric | 在文件/企业/移动地理数据库要素数据集中创建编织网及其数据集 | arcpy.parcel.CreateParcelFabric | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Parcel Records | 按记录名字段或表达式为输入要素创建宗地记录 | arcpy.parcel.CreateParcelRecords | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Disable Parcel Topology | 禁用编织网的地理数据库拓扑并移除系统规则 | arcpy.parcel.DisableParcelTopology | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Enable Parcel Topology | 为编织网启用地理数据库拓扑 | arcpy.parcel.EnableParcelTopology | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Remove Parcel Type | 从编织网移除宗地类型 | arcpy.parcel.RemoveParcelType | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Upgrade ArcMap Parcel Fabric | 把 ArcMap 宗地编织网升级为 ArcGIS Pro 编织网 | arcpy.parcel.UpgradeArcMapParcelFabric | ArcPy GP（官方实现，桥直调） | defer（旧版迁移，一次性） |

## Public Transit toolbox（arcpy.transit）
工具集数：2；工具总数：8；前提：无单独扩展；与 Network Analyst 公交数据模型配合建网需 Network Analyst 许可。官方定位：转换、显示、编辑和分析公共交通数据，多款工具在 GTFS 数据集与要素类/表之间互转，另有工具用公交时刻数据做分析。

### Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Calculate Transit Service Frequency | 计算一个或多个时段内站点/线路/兴趣点/区域可用的班次服务频率 | arcpy.transit.CalculateTransitServiceFrequency | ArcPy GP（官方实现，桥直调） | core（基于开放 GTFS 时刻的通用服务水平分析） |

### Conversion toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Connect Public Transit Data Model To Streets | 把公交站点连接到街道要素，生成 StopsOnStreets 与 StopConnectors 以建公交网络数据集 | arcpy.transit.ConnectPublicTransitDataModelToStreets | ArcPy GP（官方实现，桥直调） | core（GTFS 建网通用环节；输出结构为 NA 公交模型） |
| Features To GTFS Shapes | 按 Generate Shapes 生成的线路表示创建 GTFS shapes.txt | arcpy.transit.FeaturesToGTFSShapes | ArcPy GP（官方实现，桥直调） | core（GTFS 开放标准互转） |
| Features To GTFS Stops | 把要素类转换为 GTFS stops.txt | arcpy.transit.FeaturesToGTFSStops | ArcPy GP（官方实现，桥直调） | core（GTFS 开放标准互转） |
| Generate Shapes Features From GTFS | 估算公交系统车辆行驶路径（可用于生成新 shapes.txt） | arcpy.transit.GenerateShapesFeaturesFromGTFS | ArcPy GP（官方实现，桥直调） | core（GTFS 通用处理） |
| GTFS Shapes To Features | 把 GTFS shapes.txt 转为显示车辆实际路径的折线要素类 | arcpy.transit.GTFSShapesToFeatures | ArcPy GP（官方实现，桥直调） | core（GTFS 开放标准互转） |
| GTFS Stops To Features | 把 GTFS stops.txt 转为公交站点要素类 | arcpy.transit.GTFSStopsToFeatures | ArcPy GP（官方实现，桥直调） | core（GTFS 开放标准互转） |
| GTFS To Public Transit Data Model | 把一个或多个 GTFS 数据集转为 NA 公交数据模型的要素类与表（站点/线路/时刻） | arcpy.transit.GTFSToPublicTransitDataModel | ArcPy GP（官方实现，桥直调） | core（GTFS 开放标准转换；目标模型为 NA 专用） |

## Reality Mapping toolbox（arcpy.rm）
工具集数：0（全部工具位于根层）；工具总数：14；前提：Standard 许可＋ArcGIS Reality for ArcGIS Pro 许可（用户扩展）。官方定位：从无人机与数字航空传感器采集的已平差影像管理和生成真正射、DSM、2.5D/3D 网格与点云产品。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Analyze Control Points | 分析控制点覆盖并指出需补控制点以改进区域网平差的区域 | arcpy.rm.AnalyzeControlPoints | ArcPy GP（官方实现，桥直调） | extension（摄影测量平差流程，绑 Reality 产品） |
| Append Control Points | 把控制点合并到已有控制点表 | arcpy.rm.AppendControlPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Block Adjustment | 用 Compute Block Adjustment 的解算表把地理平差应用到镶嵌数据集项 | arcpy.rm.ApplyBlockAdjustment | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Compute Block Adjustment | 计算镶嵌数据集的平差并生成解算表 | arcpy.rm.ComputeBlockAdjustment | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Compute Camera Model | 从原始影像 EXIF 估算并精化内外方位相机模型并应用到镶嵌数据集 | arcpy.rm.ComputeCameraModel | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Compute Control Points | 在镶嵌数据集与参考影像之间创建控制点 | arcpy.rm.ComputeControlPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Compute Depth Map | 用深度图为每幅影像计算更准的 CenterZ，改进高倾斜影像的像地变换 | arcpy.rm.ComputeDepthMap | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Compute Tie Points | 计算重叠镶嵌数据集项之间的连接点 | arcpy.rm.ComputeTiePoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Detect Control Points | 在镶嵌数据集中检测地面控制点 | arcpy.rm.DetectControlPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Frame And Camera Parameters | 从含框幅影像的镶嵌数据集导出帧与相机参数 | arcpy.rm.ExportFrameAndCameraParameters | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Block Adjustment Report | 区域网平差后生成报告以评估产品质量与精度 | arcpy.rm.GenerateBlockAdjustmentReport | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Match Control Points | 为给定地面控制点与初始连接点在重叠影像中创建匹配连接点 | arcpy.rm.MatchControlPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Reconstruct Surface | 从已平差影像生成 DSM、真正射、DSM 网格、3D 网格、高斯泼溅与点云 | arcpy.rm.ReconstructSurface | ArcPy GP（官方实现，桥直调） | core（摄影测量重建生成 DSM/正射/点云为通用遥感能力概念） |
| Remove Depth Map | 删除 Compute Depth Map 生成的深度图 | arcpy.rm.RemoveDepthMap | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Territory Design toolbox（arcpy.td）
工具集数：2；工具总数：19；前提：Business Analyst 许可（Territory Design 为 BA 扩展的一部分）。官方定位：为点与面数据集构建、编辑、平衡和维护辖区（销售区/服务区/特许经营区等）。

### Analysis toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Level Variables | 在指定层级添加新字段（变量） | arcpy.td.AddLevelVariables | ArcPy GP（官方实现，桥直调） | extension（辖区方案对象专属） |
| Add Territory Barriers | 添加面/线要素以阻止或限制辖区生长 | arcpy.td.AddTerritoryBarriers | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Territory Seed Points | 创建用于确定辖区创建起点的点要素 | arcpy.td.AddTerritorySeedPoints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Balance Variables | 配置平衡过程使用的变量 | arcpy.td.SetBalanceVariables | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Territory Attribute Constraints | 设置求解辖区方案时添加约束的变量 | arcpy.td.SetTerritoryAttributeConstraints | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Territory Distance Parameters | 定义创建辖区使用的距离计算类型或距离约束 | arcpy.td.SetTerritoryDistanceParameters | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Territory Level Options | 设置辖区层级的创建方式选项 | arcpy.td.SetTerritoryLevelOptions | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Solve Territories | 按属性/距离等约束求解辖区方案并平衡辖区 | arcpy.td.SolveTerritories | ArcPy GP（官方实现，桥直调） | extension（分区平衡概念通用，实现绑 BA 方案对象） |
| Validate Territories | 验证辖区方案中是否存在无效辖区 | arcpy.td.ValidateTerritories | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Territory Solution toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Territory Level | 创建表示新层级的空要素类 | arcpy.td.AddTerritoryLevel | ArcPy GP（官方实现，桥直调） | extension（辖区方案对象专属） |
| Copy Territory Solution | 创建辖区方案的副本 | arcpy.td.CopyTerritorySolution | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Territory Level Feature Classes | 为指定辖区层级创建要素类 | arcpy.td.CreateTerritoryLevelFeatureClasses | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Territory Solution | 创建含两层的新辖区方案并把输入要素载入基础层 | arcpy.td.CreateTerritorySolution | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Territory Solution | 把辖区方案导出为要素类（含全部层级记录） | arcpy.td.ExportTerritorySolution | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Territory Report | 创建辖区方案汇总报告或两方案对比报告 | arcpy.td.GenerateTerritoryReport | ArcPy GP（官方实现，桥直调） | defer（报告生成，绑 BA 方案） |
| Import Territory Solution | 创建新方案并从表或图层导入辖区层级 | arcpy.td.ImportTerritorySolution | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Load Territory Records | 为指定层级添加或更新记录（要素） | arcpy.td.LoadTerritoryRecords | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Make Territory Solution Layer | 从已有辖区方案数据集创建表示方案的组图层 | arcpy.td.MakeTerritorySolutionLayer | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Rebuild Territory Solution | 更新辖区方案以反映基础层的变更 | arcpy.td.RebuildTerritorySolution | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Topographic Production toolbox（arcpy.topographic）
一级工具集数：3（Cartography、Data Management、Workflow，含 9 个二级 toolset）；工具总数：55；前提：ArcGIS Topographic Mapping 许可（3.6 起由 Defense Mapping 与 Production Mapping 合并）＋产品数据文件。官方定位：规范驱动的地形图生产工具箱，服务国家/民用/军用测绘机构的制图生产全流程。注：与 Workflow Manager (Classic) 集成的工具已于 Pro 3.5 移除，本节按最新版总览口径。

### Cartography > Banding toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate Elevation Bands | 从 DEM 创建高程分级带要素类 | arcpy.topographic.GenerateElevationBands | ArcPy GP（官方实现，桥直调） | extension（绑图廓整饰要素规范） |
| Generate Elevation Bands From Features | 生成表示地图产品高程级别的带要素（可用规范值或自定义值） | arcpy.topographic.GenerateElevationBandsFromFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Cartography > Cartographic Refinement toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Apply Building Offsets | 按 XML 规范规则对齐/移动/隐藏建筑要素或计算桥梁偏移值 | arcpy.topographic.ApplyBuildingOffsets | ArcPy GP（官方实现，桥直调） | extension（绑产品规范规则文件） |
| Apply Masks From Rules | 按 XML 规则文件对地图图层应用符号掩膜 | arcpy.topographic.ApplyMasksFromRules | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Visual Specification To Map | 按可视化规范数据库把符号与 Arcade 表达式应用到地图图层 | arcpy.topographic.ApplyVisualSpecificationToMap | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Calculate Bridge Offsets | 计算正确显示桥梁所需的偏移量 | arcpy.topographic.CalculateBridgeOffsets | ArcPy GP（官方实现，桥直调） | extension（制图规范专属） |
| Make Masks From Rules | 按颜色规则为要素创建面掩膜 | arcpy.topographic.MakeMasksFromRules | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Thin Spot Heights | 按产品规范对 AOI 内高程点进行综合（稀疏） | arcpy.topographic.ThinSpotHeights | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Cartography > Features toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Apply Element Values | 把图廓整饰要素值应用到目标要素 | arcpy.topographic.ApplyElementValues | ArcPy GP（官方实现，桥直调） | extension（地形图产品专属） |
| Calculate Magnetic Components | 计算给定日期与高度下点位的地磁场分量 | arcpy.topographic.CalculateMagneticComponents | ArcPy GP（官方实现，桥直调） | extension（军用地形图要素） |
| Calculate Max Elevation Figures | 计算面图层每个格网/图幅的最大高程值（MEF） | arcpy.topographic.CalculateMaxElevationFigures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Adjoining Sheets Features | 生成规范驱动地形图接图表所需的要素 | arcpy.topographic.GenerateAdjoiningSheetsFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Elevation Guide Features | 按产品规范生成高程引导图整饰要素所需数据 | arcpy.topographic.GenerateElevationGuideFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Isogonic Lines | 基于世界地磁模型生成等磁偏线 | arcpy.topographic.GenerateIsogonicLines | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Location Diagram Features | 为 JOG/ONC/TPC 图幅生成位置示意图要素 | arcpy.topographic.GenerateLocationDiagramFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Spot Heights | 基于等高线山顶/凹地与 DEM 创建高程点要素 | arcpy.topographic.GenerateSpotHeights | ArcPy GP（官方实现，桥直调） | extension（实现绑产品规范） |
| Generate Topographic Contours | 从输入栅格生成并平滑等高线 | arcpy.topographic.GenerateTopographicContours | ArcPy GP（官方实现，桥直调） | core（等高线生成概念通用） |
| Identify Contours | 识别等高线类型并赋地貌编码 | arcpy.topographic.IdentifyContours | ArcPy GP（官方实现，桥直调） | extension（绑地貌编码体系） |
| Validate Spot Heights | 校验高程点不低于其等高线山顶且无缺失等高线 | arcpy.topographic.ValidateSpotHeights | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Cartography > Layout toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Generate Product Layout | 按标准规范自动生成布局或地图产品 | arcpy.topographic.GenerateProductLayout | ArcPy GP（官方实现，桥直调）；服务端另有 Topographic Production Service 的 generateProduct REST 操作 | extension（绑产品文件与规范） |
| Make Grids And Graticules Layer | 按预定义制图规范创建格网/经纬网/边框要素组图层 | arcpy.topographic.MakeGridsAndGraticulesLayer | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Populate Map Sheet Info | 填充地图布局中图形元素的文本（图幅信息） | arcpy.topographic.PopulateMapSheetInfo | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Data Management > Features toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Apply Feature Level Metadata | 把 FeatureLevelMetadata 表的元数据记录值应用到匹配要素 | arcpy.topographic.ApplyFeatureLevelMetadata | ArcPy GP（官方实现，桥直调） | extension（地形数据模型专属） |
| Calculate Default Values | 用地理数据库默认值替换要素类/表中的空值 | arcpy.topographic.CalculateDefaultValues | ArcPy GP（官方实现，桥直调） | extension（生产库维护） |
| Calculate Metrics | 填充要素的度量属性（长度/宽度/面积/高程） | arcpy.topographic.CalculateMetrics | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Merge Lines By Pseudo Node | 在伪节点处融合（dissolve）要素 | arcpy.topographic.MergeLinesByPseudoNode | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Remove Cutback Vertices | 移除线/面要素中不需要的折返点 | arcpy.topographic.RemoveCutbackVertices | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Repair Self Intersection | 修复自相交的线/面要素（删除或拆分） | arcpy.topographic.RepairSelfIntersection | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Split Features | 用切割要素分割多个目标要素类并在切割要素上插入点 | arcpy.topographic.SplitFeatures | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Update GeoNames | 依据 GeoNames 数据更新输入要素的名称字段 | arcpy.topographic.UpdateGeoNames | ArcPy GP（官方实现，桥直调） | extension（绑 GeoNames 数据模型） |

### Data Management > Generalization toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Eliminate Polygon | 把面要素合并到与其共享最长边界的邻面 | arcpy.topographic.EliminatePolygon | ArcPy GP（官方实现，桥直调） | extension（综合规则绑产品文件） |
| Export Generalized Data | 按 Excel 综合规则把综合后的数据导出到生产 schema | arcpy.topographic.ExportGeneralizedData | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Fill Gaps | 填充参与拓扑的面要素之间的缝隙 | arcpy.topographic.FillGaps | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Identify Narrow Polygons | 按宽度分割面并分类为窄/宽部分 | arcpy.topographic.IdentifyNarrowPolygons | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import Generalization Data | 按 Excel 综合规则把生产 schema 数据导入主题综合库 | arcpy.topographic.ImportGeneralizationData | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Polygon To Centerline | 从面要素创建中心线（常用于小比例尺水系） | arcpy.topographic.PolygonToCenterline | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Remove Small Lines | 移除短于最小长度且一端不连接的线 | arcpy.topographic.RemoveSmallLines | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Set Line Direction | 使线段方向与下层高程的坡向一致 | arcpy.topographic.SetLineDirection | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Thin Hydrology Lines | 生成小比例尺简化的水系线网（保留干流、按层级稀疏） | arcpy.topographic.ThinHydrologyLines | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Data Management > Geodatabase toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create Cross-Reference Geodatabase | 创建供 Load Data 映射源/目标数据的交叉引用地理数据库 | arcpy.topographic.CreateCrossReferenceGeodatabase | ArcPy GP（官方实现，桥直调） | extension（生产数据加载专属） |
| Export MGCP Metadata | 把 MGCP/MUVD 元数据数据集导出为 XML 文件 | arcpy.topographic.ExportMGCPMetadata | ArcPy GP（官方实现，桥直调） | extension（MGCP 数据模型专属） |
| Extract Data By Feature | 把多个输入要素类的要素提取到目标数据库 | arcpy.topographic.ExtractDataByFeature | ArcPy GP（官方实现，桥直调） | extension（生产库维护） |
| Generate Excel From Geodatabase | 从地理数据库内容生成 Excel 文件 | arcpy.topographic.GenerateExcelFromGeodatabase | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Generate Geodatabase From Excel | 从 Excel 文件内容创建地理数据库 | arcpy.topographic.GenerateGeodatabaseFromExcel | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Geodatabase To Shape | 按 defense/generic/MGCP 三种模式把要素类导出为 shapefile | arcpy.topographic.GeodatabaseToShape | ArcPy GP（官方实现，桥直调） | extension（模式绑防御制图数据模型） |
| GeoNames To Geodatabase | 把 GeoNames 数据加载为要素类与表 | arcpy.topographic.GeoNamesToGeodatabase | ArcPy GP（官方实现，桥直调） | extension（绑 GeoNames 数据模型） |
| Import MGCP Metadata | 把 MGCP/MUVD 元数据导入 MGCP/MUVD 数据库 | arcpy.topographic.ImportMGCPMetadata | ArcPy GP（官方实现，桥直调） | extension（MGCP 专属） |
| Load Data | 按交叉引用数据库的映射规则把要素从源加载到目标工作区 | arcpy.topographic.LoadData | ArcPy GP（官方实现，桥直调） | extension（生产数据加载专属） |
| Unzip MGCP Cell And Import | 解压并导入 MGCP 1°×1° 图幅包/MUVD 资源面包到目标地理数据库 | arcpy.topographic.UnzipMGCPCellAndImport | ArcPy GP（官方实现，桥直调） | extension（MGCP 专属） |
| Update Topographic Production Service Database | 更新 Topographic Production Service 实例使用的数据库 | arcpy.topographic.UpdateTopographicProductionServiceDatabase | ArcPy GP（官方实现，桥直调） | defer（服务端运维） |

### Data Management > Topology toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Export Topology | 把地理数据库拓扑导出为 XML 定义文件 | arcpy.topographic.ExportTopology | ArcPy GP（官方实现，桥直调） | extension（拓扑交换概念通用，实现属本箱） |
| Import Topology | 从 XML 定义文件在要素数据集中创建地理数据库拓扑 | arcpy.topographic.ImportTopology | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Data Management > Validation toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| GAIT | 用 GAIT 检查几何、要素编码、属性值/域与元数据（需另装 Cygwin 与 GAIT） | arcpy.topographic.GAIT | ArcPy GP（官方实现，桥直调） | extension（绑 MGCP/TDS 模型与外部程序） |

### Workflow toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Download Job Files | 从地形生产服务器下载并解压最新版作业文件供人工处理 | arcpy.topographic.DownloadJobFiles | ArcPy GP（官方实现，桥直调） | defer（服务端作业流转，需 Workflow Manager 服务配置） |
| Upload Job Files | 把打包的作业文件上传到地形生产服务器继续处理 | arcpy.topographic.UploadJobFiles | ArcPy GP（官方实现，桥直调） | defer（同上） |

## Server toolbox（arcpy.server）
工具集数：4；工具总数：19；前提：无单独扩展，面向 ArcGIS Enterprise/Online/独立 Server 的 Web 图层与服务运维。官方定位：管理 Web 图层与 Web 地图，并简化通过服务器的数据提取。

### Caching toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Convert Map Server Cache Storage Format | 在 exploded 与 compactV2 之间转换地图/影像服务缓存存储格式 | arcpy.server.ConvertMapServerCacheStorageFormat | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Create Map Server Cache | 为地图或影像服务缓存创建切片方案与准备文件夹 | arcpy.server.CreateMapServerCache | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Delete Map Server Cache | 删除地图影像图层缓存及其磁盘文件 | arcpy.server.DeleteMapServerCache | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Export Map Server Cache | 把缓存切片导出为缓存数据集或切片包 | arcpy.server.ExportMapServerCache | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Generate Map Server Cache Tiling Scheme | 生成定义比例尺级别与切片尺寸的自定义切片方案文件 | arcpy.server.GenerateMapServerCacheTilingScheme | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Import Map Server Cache | 把磁盘文件夹中的切片导入地图影像图层缓存 | arcpy.server.ImportMapServerCache | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Manage Map Server Cache Scales | 增删已有缓存的比例尺级别 | arcpy.server.ManageMapServerCacheScales | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Manage Map Server Cache Status | 管理服务器内部记录的缓存切片构建状态数据 | arcpy.server.ManageMapServerCacheStatus | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |
| Manage Map Server Cache Tiles | 创建、更新、替换或删除 Web 切片缓存中的切片 | arcpy.server.ManageMapServerCacheTiles | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务缓存运维） |

### Data Extraction toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Extract Data | 按区域、格式与坐标系提取所选图层并打包为 ZIP | arcpy.server.ExtractData | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（面向 GP 服务的 clip-zip-ship） |
| Extract Data and Email Task | 提取、打包并邮件发送数据，用于搭建数据提取 GP 服务 | arcpy.server.ExtractDataAndEmailTask | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（GP 服务模型工具） |
| Extract Data Task | 按所选格式与坐标系提取图层并返回 ZIP | arcpy.server.ExtractDataTask | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（GP 服务模型工具） |
| Send Email With Zip File Attachment | 通过 SMTP 把 ZIP 文件邮件发送到指定地址 | arcpy.server.SendEmailWithZipFileAttachment | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务配套脚本工具） |

### Printing toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Export Web Map | 按 Web 应用状态返回可打印的页面布局或基础地图 | arcpy.server.ExportWebMap | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（Web 打印服务） |
| Get Layout Templates Info | 以 JSON 返回布局模板（.pagx）的内容信息 | arcpy.server.GetLayoutTemplatesInfo | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（Web 打印服务配套） |
| Get Report Templates Info | 以 JSON 返回报表文件与模板的内容信息 | arcpy.server.GetReportTemplatesInfo | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（Web 打印服务配套） |

### Publishing toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Replace Web Layer | 用另一个 Web 图层的内容替换门户中 Web 图层的内容 | arcpy.server.ReplaceWebLayer | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务发布运维） |
| Stage Service | 把服务定义草稿固化为完整的服务定义文件（.sd） | arcpy.server.StageService | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务发布运维） |
| Upload Service Definition | 上传服务定义并发布为 Web 图层/定位器/Web 工具/服务 | arcpy.server.UploadServiceDefinition | 服务端 GP 工具（随 ArcGIS Server 发布，经 REST GP 服务调用） | defer（服务发布运维） |

## Workflow Manager toolbox（arcpy.wmx）
工具集数：2；工具总数：14；前提：Workflow Manager 许可。官方定位：处理分布式 Workflow Manager (Classic) 仓库并获取作业专属信息（作业版本、数据工作区、AOI 等）。重要状态：Workflow Manager (Classic) 已在 ArcGIS Pro 3.4 退役，本箱工具全部弃用，官方推荐转服务驱动版 Workflow Manager；全箱判 defer。

### Configuration toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Clear Job Replication Information | 删除父仓库复制信息并通知集群内所有子仓库清除 | arcpy.wmx.ClearJobReplicationInformation | ArcPy GP（官方实现，桥直调） | defer（Classic 已退役，仓库运维） |
| Create Workflow Database | 创建 Workflow Manager (Classic) schema 并配置企业地理数据库 | arcpy.wmx.CreateWorkflowDatabase | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Export Job Data | 把仓库配置与全部作业信息导出为 .jxl 文件 | arcpy.wmx.ExportJobData | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Import Job Data | 把配置与作业信息导入目标仓库 | arcpy.wmx.ImportJobData | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Publish Workflow Service | 上传并共享仓库的工作流服务与作业位置地图服务 | arcpy.wmx.PublishWorkflowService | ArcPy GP（官方实现，桥直调） | defer（服务发布＋Classic 已退役） |
| Replicate Job Data | 把父仓库配置复制到各子仓库形成一致副本 | arcpy.wmx.ReplicateJobData | ArcPy GP（官方实现，桥直调） | defer（Classic 已退役，仓库运维） |
| Synchronize Job Data | 双向同步集群内多个仓库的变更 | arcpy.wmx.SynchronizeJobData | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Upgrade Workflow Database | 把已有 Workflow Manager (Classic) 数据库升级到最新 schema | arcpy.wmx.UpgradeWorkflowDatabase | ArcPy GP（官方实现，桥直调） | defer（同上） |

### Jobs toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create New Jobs | 创建一个或多个指定类型作业并指派用户/组，可设优先级与 LOI | arcpy.wmx.CreateJobs | ArcPy GP（官方实现，桥直调）；服务驱动版 Workflow Manager 另有 REST API | defer（Classic 已退役；服务驱动版另有 REST 接口） |
| Get Job AOI | 以要素图层形式获取作业的关注位置（AOI 面或 POI 点） | arcpy.wmx.GetJobAOI | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Get Job Data Workspace | 以企业地理数据库连接文件形式获取作业数据工作区 | arcpy.wmx.GetJobDataWorkspace | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Get Job Parent Version | 以连接文件形式获取作业的父版本 | arcpy.wmx.GetJobParentVersion | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Get Job Version | 以连接文件形式获取作业版本 | arcpy.wmx.GetJobVersion | ArcPy GP（官方实现，桥直调） | defer（同上） |
| Post Job Version | 把当前版本编辑提交到作业的父版本 | arcpy.wmx.PostJobVersion | ArcPy GP（官方实现，桥直调） | defer（同上） |

## Network Diagram toolbox（arcpy.nd）
工具集数：2 个 toolset＋根层工具；工具总数：74；前提：Utility Network 或 Trace Network 数据模型。官方定位：管理网络图（示意图）并配置图模板。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Alter Diagram Properties | 修改已存储网络图的属性 | arcpy.nd.AlterDiagramProperties | ArcPy GP（官方实现，桥直调） | extension（UN/TN 图模型专属） |
| Append to Diagram | 向网络图追加网络元素 | arcpy.nd.AppendToDiagram | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Change Diagrams Owner | 更改已存储网络图的所有者 | arcpy.nd.ChangeDiagramsOwner | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Diagram | 从网络要素/对象或当前追踪位置创建临时网络图 | arcpy.nd.CreateDiagram | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Delete Diagram | 删除一个或多个已存储网络图（可按模板名过滤） | arcpy.nd.DeleteDiagram | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Diagram Content | 以 JSON 导出反映基本连通性的图内容（可选属性/几何等） | arcpy.nd.ExportDiagramContent | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Extend Diagram | 按连通/可遍历/containment/结构附着关联扩展图一级元素 | arcpy.nd.ExtendDiagram | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Make Diagram Layer | 从网络图创建网络图图层 | arcpy.nd.MakeDiagramLayer | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Overwrite Diagram | 用地图中当前所选网络元素覆盖图内容 | arcpy.nd.OverwriteDiagram | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Purge Temporary Diagrams | 清除与给定 UN/TN 相关的临时网络图 | arcpy.nd.PurgeTemporaryDiagrams | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Store Diagram | 把临时图存入数据库并可设访问权与标签 | arcpy.nd.StoreDiagram | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Update Diagram | 更新与给定 UN/TN 相关的一个或多个网络图 | arcpy.nd.UpdateDiagram | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Configuration toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Angle Directed Layout | 把 Angle Directed 布局加入模板自动布局链并预设参数 | arcpy.nd.AddAngleDirectedLayout | ArcPy GP（官方实现，桥直调） | extension（图模板配置专属） |
| Add Collapse Container By Attribute Rule | 加规则：按属性 SQL 折叠容器内容 | arcpy.nd.AddCollapseContainerByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Collapse Container By Category Rule | 加规则：按网络类别折叠容器内容 | arcpy.nd.AddCollapseContainerByCategoryRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Collapse Container Rule | 加规则：折叠全部容器内容 | arcpy.nd.AddCollapseContainerRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Compression Layout | 把 Compression 布局加入模板自动布局链 | arcpy.nd.AddCompressionLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Connectivity Associations Rule | 加规则：在图中表示连通性关联 | arcpy.nd.AddConnectivityAssociationsRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Diagram Feature Capability By Attribute Rule | 加规则：按属性为图要素赋予后续规则用的能力标记 | arcpy.nd.AddDiagramFeatureCapabilityByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Diagram Feature Capability By Category Rule | 加规则：按网络类别为图要素赋予能力标记 | arcpy.nd.AddDiagramFeatureCapabilityByCategoryRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Diagram Feature Selection To Layout | 指定下一个模板布局作用的图要素选择集 | arcpy.nd.AddDiagramFeatureSelectionToLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Diagram Template | 向网络添加新图模板（可导入 .ndbd/.ndld） | arcpy.nd.AddDiagramTemplate | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Expand Container By Attribute Rule | 加规则：按属性展开容器内容 | arcpy.nd.AddExpandContainerByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Expand Container By Category Rule | 加规则：按网络类别展开容器内容 | arcpy.nd.AddExpandContainerByCategoryRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Expand Container Rule | 加规则：展开全部容器内容 | arcpy.nd.AddExpandContainerRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Force Directed Layout | 把 Force Directed 布局加入模板自动布局链 | arcpy.nd.AddForceDirectedLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Grid Layout | 把 Grid 布局加入模板自动布局链 | arcpy.nd.AddGridLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Linear Dispatch Layout | 把 Linear Dispatch 布局加入模板自动布局链 | arcpy.nd.AddLinearDispatchLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Main Ring Layout | 把 Main Ring 布局加入模板自动布局链 | arcpy.nd.AddMainRingLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Mainline Tree Layout | 把 Mainline Tree 布局加入模板自动布局链 | arcpy.nd.AddMainlineTreeLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Partial Overlapping Edges Layout | 把 Partial Overlapping Edges 布局加入模板自动布局链 | arcpy.nd.AddPartialOverlappingEdgesLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Radial Tree Layout | 把 Radial Tree 布局加入模板自动布局链 | arcpy.nd.AddRadialTreeLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Reduce Edge By Attribute Rule | 加规则：按属性归约图边 | arcpy.nd.AddReduceEdgeByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Reduce Junction By Attribute Rule | 加规则：按属性与连接数归约图交点 | arcpy.nd.AddReduceJunctionByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Reduce Junction By Category Rule | 加规则：按网络类别归约图交点 | arcpy.nd.AddReduceJunctionByCategoryRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Reduce Junction Rule | 加规则：按源类与连接数归约图交点 | arcpy.nd.AddReduceJunctionRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Relative Mainline Layout | 把 Relative Mainline 布局加入模板自动布局链 | arcpy.nd.AddRelativeMainlineLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Remove Feature By Attribute Rule | 加规则：按属性移除图要素（可按连通性约束） | arcpy.nd.AddRemoveFeatureByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Remove Feature By Category Rule | 加规则：按网络类别移除图要素 | arcpy.nd.AddRemoveFeatureByCategoryRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Remove Feature Rule | 加规则：按源类移除图要素 | arcpy.nd.AddRemoveFeatureRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Reshape Diagram Edges Layout | 把 Reshape Diagram Edges 布局加入模板自动布局链 | arcpy.nd.AddReshapeDiagramEdgesLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Set Root Junction By Attribute Rule | 加规则：按属性把交点标记为根交点 | arcpy.nd.AddSetRootJunctionByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Set Starting Point By Attribute Rule | 加规则：按属性把图要素设为追踪规则起点 | arcpy.nd.AddSetStartingPointByAttributeRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Smart Tree Layout | 把 Smart Tree 布局加入模板自动布局链 | arcpy.nd.AddSmartTreeLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Spatial Dispatch Layout | 把 Spatial Dispatch 布局加入模板自动布局链 | arcpy.nd.AddSpatialDispatchLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Spatial Query Rule | 加规则：按相对位置向图追加新网络要素 | arcpy.nd.AddSpatialQueryRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Start Iteration Rule | 加规则：标记模板规则序列迭代段的开始 | arcpy.nd.AddStartIterationRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Stop Iteration Rule | 加规则：标记模板规则序列迭代段的结束 | arcpy.nd.AddStopIterationRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Structural Attachment Rule | 加规则：在图中表示结构附着关联 | arcpy.nd.AddStructuralAttachmentRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Add Trace Rule | 加规则：建图时自动对 UN/TN 运行追踪并以结果建图 | arcpy.nd.AddTraceRule | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Alter Diagram Template | 修改图模板的属性 | arcpy.nd.AlterDiagramTemplate | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Diagram Layer Definition | 用当前地图网络图层设置为模板创建图图层定义 | arcpy.nd.CreateDiagramLayerDefinition | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Create Geoprocessing Model From Diagram Template | 从模板生成含配置工具的地理处理模型 | arcpy.nd.CreateGeoprocessingModelFromDiagramTemplate | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Delete Diagram Template | 删除图模板（官方描述为删除按模板过滤的已存储图） | arcpy.nd.DeleteDiagramTemplate | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Diagram Layer Definition | 把图图层定义导出为 .ndld 文件 | arcpy.nd.ExportDiagramLayerDefinition | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Export Diagram Template Definitions | 把规则/布局定义与图层定义导出为 .ndbd/.ndld | arcpy.nd.ExportDiagramTemplateDefinitions | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Get Diagram Templates Names | 返回与某网络相关的全部图模板名 | arcpy.nd.GetDiagramTemplatesNames | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Import Diagram Template Definitions | 向已有模板导入 .ndbd/.ndld 定义文件 | arcpy.nd.ImportDiagramTemplateDefinitions | ArcPy GP（官方实现，桥直调） | extension（同上） |

### Layout toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Apply Angle Directed Layout | 按指定对齐方向移动图的边 | arcpy.nd.ApplyAngleDirectedLayout | ArcPy GP（官方实现，桥直调） | extension（网络图布局专属） |
| Apply Compression Layout | 把图要素向图中心压缩 | arcpy.nd.ApplyCompressionLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Force Directed Layout | 以力导向布局突出图中的环路 | arcpy.nd.ApplyForceDirectedLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Geo Positions Layout | 把图交点/边移到其关联网络要素的地理位置 | arcpy.nd.ApplyGeoPositionsLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Grid Layout | 按预定义磁性网格定位图交点 | arcpy.nd.ApplyGridLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Linear Dispatch Layout | 拉开视觉上过近/重叠/重合的图交点间距 | arcpy.nd.ApplyLinearDispatchLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Main Ring Layout | 把图要素围绕主环排列 | arcpy.nd.ApplyMainRingLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Mainline Tree Layout | 沿主线分层排列图交点与边 | arcpy.nd.ApplyMainlineTreeLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Partial Overlapping Edges Layout | 在缓冲带内错开共线边或边段 | arcpy.nd.ApplyPartialOverlappingEdgesLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Radial Tree Layout | 把图要素分层排成径向树 | arcpy.nd.ApplyRadialTreeLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Relative Mainline Layout | 把图要素沿平行直线排列 | arcpy.nd.ApplyRelativeMainlineLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Rotate Tree Layout | 把与枢轴交点相关的树旋转到指定角度 | arcpy.nd.ApplyRotateTreeLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Smart Tree Layout | 把图要素分层排成智能树 | arcpy.nd.ApplySmartTreeLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Spatial Dispatch Layout | 分开视觉上接近重叠的图交点 | arcpy.nd.ApplySpatialDispatchLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Apply Template Layouts | 对输入图应用模板已配置的布局算法列表 | arcpy.nd.ApplyTemplateLayouts | ArcPy GP（官方实现，桥直调） | extension（同上） |
| Reshape Diagram Edges Layout | 对边上顶点做简单整形操作 | arcpy.nd.ReshapeDiagramEdgesLayout | ArcPy GP（官方实现，桥直调） | extension（同上） |

## Trace Network toolbox（arcpy.tn）
工具集数：0（全部工具位于根层）；工具总数：9；前提：Trace Network 数据模型（简单连通模型，如铁路/水文）。官方定位：创建、配置和使用追踪网络。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Network Attribute | 向追踪网络添加网络属性 | arcpy.tn.AddNetworkAttribute | ArcPy GP（官方实现，桥直调） | extension（TN 模型专属） |
| Convert Geometric Network To Trace Network | 把几何网络转换为追踪网络 | arcpy.tn.ConvertGeometricNetworkToTraceNetwork | ArcPy GP（官方实现，桥直调） | extension（TN 迁移专属） |
| Create Trace Network | 创建追踪网络 | arcpy.tn.CreateTraceNetwork | ArcPy GP（官方实现，桥直调） | extension（TN 模型专属） |
| Disable Network Topology | 禁用已有追踪网络的网络拓扑 | arcpy.tn.DisableNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（TN 模型专属） |
| Enable Network Topology | 启用网络拓扑以支持追踪等分析并发现错误要素 | arcpy.tn.EnableNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（TN 模型专属） |
| Set Flow Direction | 设置追踪网络中要素的流向 | arcpy.tn.SetFlowDirection | ArcPy GP（官方实现，桥直调） | extension（TN 模型专属） |
| Set Network Attribute | 为要素类指定追踪操作使用的网络属性 | arcpy.tn.SetNetworkAttribute | ArcPy GP（官方实现，桥直调） | extension（TN 模型专属） |
| Trace | 按连通性或可遍历性从起点返回所选要素 | arcpy.tn.Trace | ArcPy GP（官方实现，桥直调） | extension（TN 追踪专属；追踪概念本身通用但绑定 TN 模型） |
| Validate Network Topology | 验证追踪网络拓扑（编辑网络属性/几何后必需） | arcpy.tn.ValidateNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（TN 模型专属） |

## Utility Network toolbox（arcpy.un）
工具集数：2 个 toolset＋根层工具；工具总数：37（按所据官方总览页逐条抄录）；前提：Utility Network 数据模型（企业/文件/移动地理数据库），多用户模式需 ArcGIS Enterprise 服务。官方定位：创建、配置和使用公用设施网络（电/气/水/电信等）。

### （根层） toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Trace Locations | 创建用作 Trace 起点与屏障输入的要素类 | arcpy.un.AddTraceLocations | ArcPy GP（官方实现，桥直调） | extension（UN 专属追踪） |
| Export Subnetwork | 把子网导出为 JSON，并可删除已移除控制器的子网行 | arcpy.un.ExportSubnetwork | ArcPy GP（官方实现，桥直调） | extension（UN 子网模型专属） |
| Repair Network Topology | 校验并修复网络拓扑系统表中的不一致 | arcpy.un.RepairNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（UN 拓扑专属） |
| Trace | 按连通性或可遍历性从起点返回公用设施网络要素 | arcpy.un.Trace | ArcPy GP（官方实现，桥直调） | extension（UN 追踪专属） |
| Update Is Connected | 按连通性更新全部网络要素的 IsConnected 属性 | arcpy.un.UpdateIsConnected | ArcPy GP（官方实现，桥直调） | extension（UN 专属） |
| Update Subnetwork | 更新 Subnetworks 表、SubnetLine 与子网系统图中的子网信息 | arcpy.un.UpdateSubnetwork | ArcPy GP（官方实现，桥直调） | extension（UN 子网专属） |
| Validate Network Topology | 编辑后验证公用设施网络拓扑 | arcpy.un.ValidateNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（UN 拓扑专属） |
| Verify Network Topology | 校验拓扑系统表并把不一致写入日志 | arcpy.un.VerifyNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（UN 拓扑专属） |

### Administration toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Domain Network | 向公用设施网络添加域网络 | arcpy.un.AddDomainNetwork | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Add Network Attribute | 向公用设施网络添加网络属性 | arcpy.un.AddNetworkAttribute | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Add Network Category | 向已有公用设施网络添加网络类别 | arcpy.un.AddNetworkCategory | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Add Rule | 向公用设施网络添加网络规则 | arcpy.un.AddRule | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Add Terminal Configuration | 向已有公用设施网络添加终端配置 | arcpy.un.AddTerminalConfiguration | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Add Tier | 为域网络创建新层级（tier） | arcpy.un.AddTier | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Add Tier Group | 向域网络添加层级组 | arcpy.un.AddTierGroup | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Create Utility Network | 在企业/文件/移动地理数据库要素数据集中创建公用设施网络 | arcpy.un.CreateUtilityNetwork | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Delete Network Category | 删除公用设施网络中的网络类别 | arcpy.un.DeleteNetworkCategory | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Delete Rule | 永久删除公用设施网络中的一条规则 | arcpy.un.DeleteRule | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Delete Terminal Configuration | 删除公用设施网络中的终端配置 | arcpy.un.DeleteTerminalConfiguration | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Disable Network Topology | 禁用已有公用设施网络的网络拓扑 | arcpy.un.DisableNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Enable Network Topology | 为公用设施网络启用网络拓扑 | arcpy.un.EnableNetworkTopology | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Export Associations | 把关联导出为 CSV 文件 | arcpy.un.ExportAssociations | ArcPy GP（官方实现，桥直调） | extension（UN 关联模型专属） |
| Export Rules | 把连通/结构附着/ containment 规则导出为 CSV | arcpy.un.ExportRules | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Export Subnetwork Controllers | 把子网控制器导出为 CSV | arcpy.un.ExportSubnetworkControllers | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Import Associations | 从 CSV 向已有公用设施网络导入关联 | arcpy.un.ImportAssociations | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Import Rules | 从 CSV 导入连通/结构附着/containment 规则 | arcpy.un.ImportRules | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Import Subnetwork Controllers | 从 CSV 向公用设施网络导入子网控制器 | arcpy.un.ImportSubnetworkControllers | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Set Association Role | 在资产类型级别更改网络要素类/表的关联角色 | arcpy.un.SetAssociationRole | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Set Edge Connectivity | 定义要素如何连接到给定资产类型的线/边对象 | arcpy.un.SetEdgeConnectivity | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Set Network Attribute | 在资产类型级别为要素类/表指定追踪用网络属性 | arcpy.un.SetNetworkAttribute | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Set Network Category | 在资产类型级别为要素类/表指定追踪用网络类别 | arcpy.un.SetNetworkCategory | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Set Subnetwork Definition | 设置域网络层级的子网属性 | arcpy.un.SetSubnetworkDefinition | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |
| Set Terminal Configuration | 为公用设施网络中的资产类型指定终端配置 | arcpy.un.SetTerminalConfiguration | ArcPy GP（官方实现，桥直调） | extension（UN 模型专属） |

### Trace Configuration toolset
| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Trace Configuration | 在公用设施网络中创建命名追踪配置 | arcpy.un.AddTraceConfiguration | ArcPy GP（官方实现，桥直调） | extension（UN 追踪配置专属） |
| Delete Trace Configuration | 删除一个或多个命名追踪配置 | arcpy.un.DeleteTraceConfiguration | ArcPy GP（官方实现，桥直调） | extension（UN 追踪配置专属） |
| Export Trace Configurations | 把命名追踪配置导出为 JSON | arcpy.un.ExportTraceConfigurations | ArcPy GP（官方实现，桥直调） | extension（UN 追踪配置专属） |
| Import Trace Configurations | 从 JSON 导入命名追踪配置 | arcpy.un.ImportTraceConfigurations | ArcPy GP（官方实现，桥直调） | extension（UN 追踪配置专属） |

## 附：Esri 官方智能体 / MCP 入口（官方文档核实）

- **MCP for ArcGIS Location Services（beta）**——Esri 官方托管的 Model Context Protocol 服务器，AI 智能体可经标准化 MCP 工具调用 ArcGIS Location Services（地理编码/反向地理编码、路径、 高程、静态地图、Places、底图样式与瓦片、GeoEnrichment），无需直调 REST API；需 ArcGIS Location Platform 或 ArcGIS Online 账户。官方文档：https://developers.arcgis.com/ai/mcp-arcgis-location-services/
- **ArcGIS AI assistants（产品内官方助手，非 MCP）**——ArcGIS Online 组织级可开启的官方 AI 助手矩阵，含 ArcGIS Pro assistant（beta）、ArcGIS Business Analyst assistant、ArcGIS Notebooks assistant（beta）、Documentation assistant（beta）等，由组织管理员在 AI 设置页统一开关。官方文档：http://doc.arcgis.com/en/arcgis-online/administer/configure-assistants.htm
- 说明：本轮在 ArcGIS Pro 工具参考内**未发现**面向本地 GP 工具箱的 Esri 官方 MCP server；社区自建的 ArcGIS MCP 项目（如社区发布的 portal MCP）非 Esri 官方出品，按证据纪律未收录。GeoAI 工具箱的模型生态与 arcgis Python API（arcgis.learn）互通，但那是 Python API 而非智能体/MCP 入口。

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

## 6. ArcMap 10.8 对照（差异标注，不另列全集）

口径：ArcMap 10.8 的工具集主体与 Pro 同源（同为 ArcToolbox 体系、同名工具箱/工具集占绝大多数），故不重复列全集，只标三类差异：ArcMap 独有、Pro 独有、结构差异。依据为本节所引的 ArcMap 官方总览页与 Desktop 许可主题（实际查阅，见第 1 节）。

### 6.1 ArcMap 工具箱体系（官方许可主题列名的核心箱＋扩展箱）

核心箱（Desktop "Licensing for geoprocessing tools" 主题列名）：3D Analyst、Analysis、Cartography、Conversion、Coverage、Data Interoperability、Data Management、Geocoding、Geostatistical Analyst、Linear Referencing、Multidimension、Network Analyst、Spatial Analyst、Spatial Statistics。
另有随扩展/产品附带的箱在 ArcMap 中存在：Business Analyst（arcpy.ba，需 ImportToolbox 加载其 .tbx）、Data Reviewer、Editing、Schematics、Server、Tracking Analyst、Workflow Manager 等。

### 6.2 ArcMap 独有（Pro 已移除或被新线取代）

| 对象 | 内容 | 取代者（Pro） | 平台判断 |
| --- | --- | --- | --- |
| Coverage toolbox | 面向 coverage 数据模型的工具箱，含 Analysis（Extract/Overlay/Proximity 等子集）、Conversion（From/To Coverage）、Data Management（Aggregate、Workspace Management 等）三大组；须装 ArcInfo Workstation 才出现 | 无（coverage 模型本身已被 geodatabase 取代） | defer：遗留数据模型，平台不投入 |
| Schematics toolbox | 5 个工具：Create Diagram / Create Schematic Folder / Convert Diagram To Features / Update Diagram / Update Diagrams（建、更新、导出示意图与示意文件夹） | Network Diagram toolbox | extension（存量）：仅 ArcMap 桥可留映射，新能力按 Pro 的 nd 设计 |
| Tracking Analyst toolbox | 时态数据准备：Concatenate Date And Time Fields（合并日期与时间字段）、Make Tracking Layer（建跟踪图层）为其 10.0 总览所载核心工具，后续版本另有 Track Intervals 等增补 | Pro 无同名工具箱（时空分析由 Space Time Pattern Mining 承接一部分） | extension（存量） |
| Data Management 内的遗留工具集 | Distributed Geodatabase（复制/同步）、Geometric Network（几何网络建模与追踪）、Graph（图表文件生成）、File Geodatabase（压缩/解压）、Tile Cache、Photos、General 等——ArcMap 版 DM 共 31 个工具集 | Geometric Network → Utility Network / Trace Network；Graph → arcpy.charts；其余多被 Pro DM 重组或下线 | 按行判断：几何网络线 extension，其余 defer 为主 |

### 6.3 Pro 独有（ArcMap 无对应工具箱）

据 Pro 的 ArcPy 模块总览（45 箱）与 Desktop 侧名单对照，下列为 Pro 线新增、ArcMap 没有的工具箱：GeoAI、GeoAnalytics Desktop、GeoAnalytics Server、Raster Analysis、Standard Feature Analysis、Ready To Use、Reality Mapping、Oriented Imagery、Indoors、Indoor Positioning、Parcels、Public Transit、Territory Design、Topographic Production、Trace Network、Utility Network、Network Diagram、Location Referencing、AllSource、Image Analyst、Defense（其前身 Military Analyst/MOLE 只见于早期 Desktop 许可文档，属遗留）。
结构差异（总览级对比，已逐页证实的一条）：**Analysis 工具箱在 ArcMap 只有 4 个工具集（Extract/Overlay/Proximity/Statistics），Pro 增加 Pairwise Overlay 工具集**，且 Pro 的 Overlay/Statistics 工具集内含 ArcMap 版所无的新工具（如 Count Overlapping Features、Remove Overlap (multiple)、Enrich、Summarize Nearby）——此条为两版总览/工具集页对照结论，逐工具差异未逐页穷举。

### 6.4 ArcPy 与运行环境差异

| 项 | ArcMap 10.8 | ArcGIS Pro 3.4 |
| --- | --- | --- |
| 工程操作模块 | arcpy.mapping（操作 .mxd、数据框 data frame） | arcpy.mp（操作 .aprx、map/layout） |
| Python | Python 2.7（随 Desktop） | Python 3（conda 环境） |
| 地图模型 | 数据框（data frame）即"地图" | Map 与 Layout 分离 |
| 生命周期 | 10.8.x 为最终系列，2026-03-01 退役（Esri Support 官方页） | 持续演进 |

> 对现有两桥的印证：arcmap 桥用 `arcmap_list_dataframes`、arcgis-pro 桥用 `arcgis_list_maps`＋`arcgis_list_layouts`，正是上表地图模型差异的体现；统一入口 v0 已按此做了 kind 标注（dataframe vs map），方向正确。
> 轮子来源注记（ArcMap 存量）：本节所列 ArcMap 独有工具的官方实现均为 **ArcMap 版 ArcPy 地理处理**（随 Desktop 提供，如 Schematics 为 arcpy.schematics、Tracking Analyst 为 arcpy.ta），无 Pro 等价实现、亦无 REST/MCP 通道；按"不重复造轮子"，平台对这批只做存量映射，不新建实现。

---


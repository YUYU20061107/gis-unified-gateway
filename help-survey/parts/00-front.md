# ArcGIS 家族功能普查（GIS 综合平台能力底账）

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

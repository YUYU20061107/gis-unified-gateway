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

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

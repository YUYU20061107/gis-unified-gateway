# ArcGIS Pro 工具普查：Conversion 与 Cartography 工具箱

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

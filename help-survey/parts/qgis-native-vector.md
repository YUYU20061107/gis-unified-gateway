# QGIS 3.40 Processing「QGIS 算法提供者」矢量与通用类分组普查

来源页：https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/index.html（各分组页为其下 24.1.x 子页）｜抓取日期：2026-11-02

判断口径：core＝跨 GIS 软件共有的基础能力；extension＝QGIS 专属或分析型能力；defer＝仅桌面交互、模型内部件或有副作用风险。

## 制图（Cartography）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Angle to nearest feature | 计算点到最近要素的对齐角度 | native:angletonearest | extension |
| Combine style databases | 合并多个样式库为一个 | native:combinestyles | extension |
| Create categorized renderer from styles | 按样式库符号生成分类渲染 | native:categorizeusingstyle | defer |
| Extract style from project | 从工程提取样式对象到样式库 | native:stylefromproject | extension |
| Export atlas layout as image | 将图集布局导出为图片 | native:atlaslayouttoimage | defer |
| Export atlas layout as multiple PDF files | 将图集布局导出为多个PDF | native:atlaslayouttomultiplepdf | defer |
| Export atlas layout as PDF | 将图集布局导出为单个PDF | native:atlaslayouttopdf | defer |
| Export print layout as image | 将打印布局导出为图片 | native:printlayouttoimage | defer |
| Export print layout as PDF | 将打印布局导出为PDF | native:printlayouttopdf | defer |
| Print layout map extent to layer | 布局地图范围导出为面图层 | native:printlayoutmapextenttolayer | extension |
| Set layer style | 给图层套用QML样式文件 | native:setlayerstyle | defer |
| Topological coloring | 为相邻面分配互不相同色号 | qgis:topologicalcoloring | extension |
| Transfer annotations from main annotation layer | 主注记层内容转到新注记层 | native:transferannotationsfrommain | defer |

## 数据库（Database）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Import into PostGIS | 矢量图层导入PostgreSQL库 | qgis:importintopostgis | extension |
| Import into SpatiaLite | 矢量图层导入SpatiaLite库 | qgis:importintospatialite | extension |
| Package layers | 多图层打包进GeoPackage | native:package | extension |
| PostgreSQL execute and load SQL | 对PostgreSQL执行SQL并加载结果 | qgis:postgisexecuteandloadsql | defer |
| PostgreSQL execute SQL | 对PostgreSQL数据库执行SQL | native:postgisexecutesql | defer |
| SpatiaLite execute SQL | 按文件对SpatiaLite执行SQL | native:spatialiteexecutesql | defer |
| SpatiaLite execute SQL (registered) | 对已连接SpatiaLite执行SQL | native:spatialiteexecutesqlregistered | defer |

## 文件工具（File tools）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Download file | 按URL下载文件到本地 | qgis:filedownloader | defer |
| HTTP request | 发起HTTP请求并返回结果 | native:httprequest | defer |
| Open file or URL | 用默认程序打开文件或URL | native:openurl | defer |

## GPS（GPS）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Convert GPS data | 用GPSBabel转GPS文件为GPX | native:convertgpsdata | extension |
| Convert GPX feature type | 转换GPX要素类型 | native:convertgpxfeaturetype | extension |
| Download GPS data | 从GPS设备下载数据为GPX | native:downloadgpsdata | defer |
| Upload GPS data | 将GPX数据上传到GPS设备 | native:uploadgpsdata | defer |

## 图层工具（Layer tools）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Export layers information | 导出图层范围与元信息为面层 | native:exportlayersinformation | extension |
| Export to spreadsheet | 多图层属性导出为电子表格 | native:exporttospreadsheet | extension |

## 建模器工具（Modeler tools）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Calculate expression | 在模型中计算表达式并缓存 | native:calculateexpression | defer |
| Conditional branch | 按表达式给模型加条件分支 | native:condition | defer |
| Create directory | 在文件系统新建目录 | native:createdirectory | defer |
| Feature filter | 模型内按条件分流要素 | native:filter | defer |
| Filter layers by type | 模型内按矢量栅格分流图层 | native:filterlayersbytype | defer |
| Load layer | 把图层加载到当前工程 | native:loadlayer | defer |
| Raise exception | 抛出异常并中止模型执行 | native:raiseexception | defer |
| Raise message | 在日志中记录信息消息 | native:raisemessage | defer |
| Raise warning | 在日志中记录警告消息 | native:raisewarning | defer |
| Rename layer | 在模型中重命名图层 | native:renamelayer | defer |
| Save log | 把模型执行日志存为文件 | native:savelog | defer |
| Set project variable | 设置当前工程的表达式变量 | native:setprojectvariable | defer |
| String concatenation | 在模型中拼接两个字符串 | native:stringconcatenation | defer |
| Variable distance buffer | 按字段值做可变距离缓冲（已弃用） | qgis:variabledistancebuffer | extension |

注：Variable distance buffer 一节位于 Modeler tools 分组页末尾，页内标注 deprecated、建议改用 Buffer。

## 网络分析（Network analysis）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Service area (from layer) | 由点图层生成网络服务区 | qgis:serviceareafromlayer | extension |
| Service area (from point) | 由单点生成网络服务区 | native:serviceareafrompoint | extension |
| Shortest path (layer to point) | 多起点到终点的最短路径 | native:shortestpathlayertopoint | extension |
| Shortest path (point to layer) | 起点到多目标点的最短路径 | native:shortestpathpointtolayer | extension |
| Shortest path (point to point) | 两点间最短或最快路径 | native:shortestpathpointtopoint | extension |

## 图表（Plots）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Bar plot | 按类别字段生成柱状图 | qgis:barplot | extension |
| Box plot | 按类别字段生成箱线图 | qgis:boxplot | extension |
| Mean and standard deviation plot | 生成均值标准差箱线图 | qgis:meanandstandarddeviationplot | extension |
| Polar plot | 按类别与数值生成极坐标图 | qgis:polarplot | extension |
| Raster layer histogram | 生成栅格波段直方图 | qgis:rasterlayerhistogram | extension |
| Vector layer histogram | 生成矢量字段直方图 | qgis:vectorlayerhistogram | extension |
| Vector layer scatterplot | 生成矢量字段散点图 | qgis:vectorlayerscatterplot | extension |
| Vector layer scatterplot (3D) | 生成三维散点图 | qgis:scatter3dplot | extension |

## 矢量分析（Vector analysis）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Basic statistics for fields | 计算单个字段的基础统计 | qgis:basicstatisticsforfields | core |
| Climb along line | 计算线要素的爬升与下降 | qgis:climbalongline | extension |
| Count points in polygon | 统计每个面内的点数量 | native:countpointsinpolygon | core |
| DBSCAN clustering | 对点做DBSCAN密度聚类 | native:dbscanclustering | extension |
| Distance matrix | 计算点间距离矩阵 | qgis:distancematrix | extension |
| Distance to nearest hub (line to hub) | 生成到最近枢纽的连线 | qgis:distancetonearesthublinetohub | extension |
| Distance to nearest hub (points) | 计算点到最近枢纽的距离 | qgis:distancetonearesthubpoints | extension |
| Hub lines | 生成要素到枢纽的连线 | native:hublines | extension |
| K-means clustering | 对点做K均值聚类 | native:kmeansclustering | extension |
| List unique values | 列出字段的唯一值清单 | qgis:listuniquevalues | extension |
| Mean coordinate(s) | 计算图层的平均坐标点 | native:meancoordinates | extension |
| Nearest neighbour analysis | 计算点分布的最近邻指数 | native:nearestneighbouranalysis | extension |
| Overlap analysis | 计算与各图层的重叠面积占比 | native:calculatevectoroverlaps | extension |
| Shortest line between features | 生成要素间的最短连线 | native:shortestline | extension |
| ST-DBSCAN clustering | 考虑时间维的DBSCAN聚类 | native:stdbscanclustering | extension |
| Statistics by categories | 按类别分组计算字段统计 | qgis:statisticsbycategories | core |
| Sum line lengths | 按多边形汇总线长 | native:sumlinelengths | extension |

## 矢量覆盖（Vector coverage）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Coverage dissolve | 对覆盖多边形做优化融合 | native:coverageunion | extension |
| Coverage simplification | 保持拓扑有效的覆盖简化 | native:coveragesimplify | extension |
| Coverage validation | 检测覆盖的边不匹配与缝隙 | native:coveragevalidate | extension |

## 矢量创建（Vector creation）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Array offset lines | 生成线的多重偏移副本 | native:arrayoffsetlines | extension |
| Array translated features | 生成要素的多重平移副本 | native:arraytranslatedfeatures | extension |
| Create grid | 按范围与间距创建格网 | native:creategrid | core |
| Create points layer from table | 按表中坐标字段生成点层 | native:createpointslayerfromtable | core |
| Generate points (pixel centroids) along line | 沿线生成像元中心点 | qgis:generatepointspixelcentroidsalongline | extension |
| Generate points (pixel centroids) inside polygons | 面内生成像元中心点 | native:generatepointspixelcentroidsinsidepolygons | extension |
| Import geotagged photos | 导入带地理标记的照片为点 | native:importphotos | extension |
| Points to path | 按顺序把点连成路径线 | native:pointstopath | extension |
| Random points along line | 沿线随机生成点（旧版） | qgis:qgisrandompointsalongline | extension |
| Random points in extent | 在指定范围内随机生成点 | native:randompointsinextent | extension |
| Random points in layer bounds | 在图层范围内随机生成点 | qgis:randompointsinlayerbounds | extension |
| Random points in polygons | 在面要素内随机生成点 | native:randompointsinpolygons | extension |
| Random points inside polygons | 在面内随机生成点（旧版） | qgis:randompointsinsidepolygons | extension |
| Random points on lines | 在线要素上随机生成点 | native:randompointsonlines | extension |
| Pixels to points | 栅格像元转点 | native:pixelstopoints | extension |
| Pixels to polygons | 栅格像元转面 | native:pixelstopolygons | extension |
| Regular points | 按规则间距生成点阵 | qgis:regularpoints | extension |

## 矢量通用（Vector general）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Assign projection | 只改CRS标注不重投影几何 | native:assignprojection | core |
| Batch Nominatim geocoding | 用Nominatim批量地址编码 | native:batchnominatimgeocoder | defer |
| Create bookmarks from layer | 按要素范围创建空间书签 | native:layertobookmarks | defer |
| Bookmarks to layer | 把空间书签导出为面图层 | native:bookmarkstolayer | defer |
| Create attribute index | 为字段创建属性索引 | native:createattributeindex | extension |
| Create spatial index | 为图层创建空间索引 | native:createspatialindex | extension |
| Define current projection | 就地改写Shapefile投影文件 | qgis:definecurrentprojection | defer |
| Delete duplicate geometries | 删除几何完全相同的要素 | native:deleteduplicategeometries | extension |
| Remove duplicates by attribute | 按字段删除重复行 | native:removeduplicatesbyattribute | extension |
| Detect vector changes | 对比两版本图层找出变化 | native:detectvectorchanges | extension |
| Drop geometries | 删除几何只保留属性表 | native:dropgeometries | extension |
| Execute SQL | 对虚拟层执行SQL查询 | qgis:executesql | defer |
| Export to DXF | 把图层导出为DXF文件 | native:dxfexport | extension |
| Find projection | 猜测缺失投影的正确CRS | qgis:findprojection | extension |
| Flatten relationship | 展平关联关系生成新图层 | native:flattenrelationships | extension |
| Join attributes by field value | 按字段值做表连接 | native:joinattributestable | core |
| Join attributes by location | 按空间关系连接属性 | native:joinattributesbylocation | core |
| Join attributes by location (summary) | 空间连接并汇总统计 | qgis:joinbylocationsummary | core |
| Join to nearest | 连接最近要素的属性 | native:joinbynearest | extension |
| Merge vector layers | 合并多个矢量图层为一层 | native:mergevectorlayers | core |
| Order by expression | 按表达式对要素排序 | native:orderbyexpression | extension |
| Repair Shapefile | 修复损坏的Shapefile | native:repairshapefile | extension |
| Reproject layer | 把图层重投影到目标CRS | native:reprojectlayer | core |
| Save features | 把要素另存为新文件 | native:savefeatures | extension |
| Set layer encoding | 设置图层的数据编码 | native:setlayerencoding | extension |
| Split features by character | 按字段字符拆分要素值 | native:splitfeaturesbycharacter | extension |
| Split vector layer | 按字段把图层拆成多文件 | native:splitvectorlayer | extension |
| Truncate table | 清空图层全部要素 | native:truncatetable | defer |

## 矢量几何（Vector geometry）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Add geometry attributes | 添加面积长度坐标等几何字段 | qgis:exportaddgeometrycolumns | core |
| Affine transform | 对几何做平移缩放旋转变换 | native:affinetransform | extension |
| Aggregate | 按表达式分组聚合要素 | native:aggregate | extension |
| Boundary | 提取线面几何的拓扑边界 | native:boundary | extension |
| Bounding boxes | 计算每个要素的包围盒 | native:boundingboxes | core |
| Buffer | 按固定或字段距离生成缓冲区 | native:buffer | core |
| Centroids | 计算每个要素的质心点 | native:centroids | core |
| Check validity | 检查几何有效性并输出问题 | qgis:checkvalidity | core |
| Collect geometries | 按分组把几何收集为多部件 | native:collect | extension |
| Concave hull | 按阈值生成凹包多边形 | native:concavehull | extension |
| Convert geometry type | 转换几何类型 | qgis:convertgeometrytype | extension |
| Convert to curves | 把直线段几何转换为曲线 | native:converttocurves | extension |
| Convex hull | 生成要素的最小凸包 | native:convexhull | core |
| Create layer from extent | 把范围数值生成为面图层 | native:extenttolayer | extension |
| Create layer from point | 把坐标数值生成为点图层 | native:pointtolayer | extension |
| Create wedge buffers | 按方位角生成楔形缓冲区 | native:wedgebuffers | extension |
| Delaunay triangulation | 对点集做Delaunay三角剖分 | native:delaunaytriangulation | extension |
| Delete holes | 删除面中小于阈值的孔洞 | native:deleteholes | extension |
| Densify by count | 按新增顶点数加密几何 | native:densifygeometries | extension |
| Densify by interval | 按间距加密几何顶点 | native:densifygeometriesgivenaninterval | extension |
| Dissolve | 按字段或整体融合要素 | native:dissolve | core |
| Drape (set Z value from raster) | 从栅格给几何赋Z值 | native:setzfromraster | extension |
| Drop M/Z values | 去除几何的M与Z值 | native:dropmzvalues | extension |
| Eliminate selected polygons | 把选中小面并入邻近大面 | qgis:eliminateselectedpolygons | extension |
| Explode lines | 把线拆为单段线要素 | native:explodelines | extension |
| Extend lines | 按距离延长线两端 | native:extendlines | extension |
| Filter vertices by M value | 按M值范围过滤顶点 | native:filterverticesbym | extension |
| Filter vertices by Z value | 按Z值范围过滤顶点 | native:filterverticesbyz | extension |
| Fix geometries | 修复无效几何使其有效 | native:fixgeometries | core |
| Force right-hand-rule | 强制面环遵循右手定则 | native:forcerhr | extension |
| Split layer at antimeridian | 在反经线处切分几何 | native:antimeridiansplit | extension |
| Geometry by expression | 用表达式逐要素生成新几何 | native:geometrybyexpression | extension |
| Interpolate point on line | 按距起点距离在线上插值取点 | native:interpolatepoint | extension |
| Keep N biggest parts | 只保留最大的N个部件 | qgis:keepnbiggestparts | extension |
| Line substring | 按起止距离截取线段 | native:linesubstring | extension |
| Lines to polygons | 把闭合线转换为面 | qgis:linestopolygons | core |
| Merge lines | 合并相接的线要素 | native:mergelines | extension |
| Minimum bounding geometry | 生成最小包围几何 | qgis:minimumboundinggeometry | extension |
| Minimum enclosing circle | 生成最小外接圆 | native:minimumenclosingcircle | extension |
| Multi-ring buffer (constant distance) | 生成等距多环缓冲区 | native:multiringconstantbuffer | extension |
| Multipart to singleparts | 多部件拆为单部件要素 | native:multiparttosingleparts | core |
| Offset line | 按距离偏移线要素 | native:offsetline | extension |
| Oriented minimum bounding box | 生成有向最小包围盒 | native:orientedminimumboundingbox | extension |
| Orthogonalize | 把几何角度调整为直角 | native:orthogonalize | extension |
| Point on surface | 生成保证落在面上的点 | native:pointonsurface | extension |
| Points along lines | 按间距沿线生成点 | native:pointsalonglines | extension |
| Points displacement | 对重叠点做位移分散 | qgis:pointsdisplacement | extension |
| Pole of inaccessibility | 计算面的不可达极点 | native:poleofinaccessibility | extension |
| Polygonize | 由线网络构建面 | native:polygonize | extension |
| Polygons to lines | 把面轮廓转换为线 | native:polygonstolines | core |
| Project points (Cartesian) | 按距离方位投影点（平面） | native:projectpointcartesian | extension |
| Promote to multipart | 单部件提升为多部件几何 | native:promotetomulti | extension |
| Rectangles, ovals, diamonds | 按范围生成矩形椭圆菱形 | native:rectanglesovalsdiamonds | extension |
| Remove duplicate vertices | 删除几何中的重复顶点 | native:removeduplicatevertices | extension |
| Remove null geometries | 删除空几何要素 | native:removenullgeometries | extension |
| Reverse line direction | 反转线要素方向 | native:reverselinedirection | extension |
| Rotate | 按角度旋转要素几何 | native:rotatefeatures | extension |
| Roundness | 计算面要素的圆度指标 | native:roundness | extension |
| Segmentize by maximum angle | 按最大转角细分几何 | native:segmentizebymaxangle | extension |
| Segmentize by maximum distance | 按最大段长细分几何 | native:segmentizebymaxdistance | extension |
| Set M value | 给几何设置固定M值 | native:setmvalue | extension |
| Set M value from raster | 从栅格给几何赋M值 | native:setmfromraster | extension |
| Set Z value | 给几何设置固定Z值 | native:setzvalue | extension |
| Simplify | 按容差简化几何 | native:simplifygeometries | core |
| Single sided buffer | 生成线的单侧缓冲区 | native:singlesidedbuffer | extension |
| Smooth | 对几何做平滑处理 | native:smoothgeometry | extension |
| Snap geometries to layer | 把几何捕捉到参考图层 | native:snapgeometries | extension |
| Snap points to grid | 把点捕捉到格网交点 | native:snappointstogrid | extension |
| Split lines by maximum length | 按最大长度切分线 | native:splitlinesbylength | extension |
| Subdivide | 把复杂几何细分为小部件 | native:subdivide | extension |
| Swap X and Y coordinates | 交换几何的X与Y坐标 | native:swapxy | extension |
| Tapered buffer | 生成宽度渐变的缓冲区 | native:taperedbuffer | extension |
| Tessellate | 把面几何三角化（3D） | 3d:tessellate | extension |
| Transect | 沿线按间距生成横断线 | native:transect | extension |
| Translate | 按偏移量平移几何 | native:translategeometry | extension |
| Variable width buffer (by M value) | 按M值生成变宽缓冲区 | native:bufferbym | extension |
| Voronoi polygons | 对点集生成泰森多边形 | native:voronoipolygons | extension |

## 矢量叠加（Vector overlay）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Clip | 用面层裁剪矢量图层 | qgis:clip | core |
| Difference | 擦除与叠加层重叠的部分 | qgis:difference | core |
| Difference (multiple layers) | 依次擦除多个叠加层 | qgis:multidifference | extension |
| Intersection | 提取两层重叠部分及双属性 | qgis:intersection | core |
| Intersection (multiple layers) | 提取与多层共同重叠部分 | qgis:multiintersection | extension |
| Line intersections | 提取线交点并附两线属性 | qgis:lineintersections | extension |
| Split with lines | 用另一层线分割要素 | qgis:splitwithlines | extension |
| Symmetrical difference | 提取两层互不重叠的部分 | qgis:symmetricaldifference | core |
| Union | 合并两层并保留全部区域 | qgis:union | core |
| Union (multiple layers) | 合并输入层与多个叠加层 | qgis:multiunion | extension |

## 矢量选择（Vector selection）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Filter by geometry type | 按几何类型分流要素 | native:filterbygeometry | extension |
| Random extract | 随机抽取一部分要素成新层 | native:randomextract | extension |
| Random extract within subsets | 按类别随机抽取要素成新层 | qgis:randomextractwithinsubsets | extension |
| Random selection | 在图层中随机选中要素 | qgis:randomselection | defer |
| Random selection within subsets | 按类别随机选中要素 | qgis:randomselectionwithinsubsets | defer |
| Select by attribute | 按属性条件选中要素 | qgis:selectbyattribute | defer |
| Select by expression | 按表达式选中要素 | qgis:selectbyexpression | defer |
| Select by location | 按空间关系选中要素 | native:selectbylocation | defer |
| Select within distance | 选中指定距离内的要素 | native:selectwithindistance | defer |

## 矢量表（Vector table）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Add autoincremental field | 添加自增序号字段 | native:addautoincrementalfield | extension |
| Add field to attributes table | 给属性表添加新字段 | native:addfieldtoattributestable | core |
| Add unique value index field | 给类别值添加数字索引字段 | native:adduniquevalueindexfield | extension |
| Add X/Y fields to layer | 给点图层添加XY坐标字段 | native:addxyfields | core |
| Advanced Python field calculator | 用Python公式计算新字段 | qgis:advancedpythonfieldcalculator | defer |
| Drop field(s) | 删除指定的属性字段 | native:deletecolumn | core |
| Explode HStore field | 把HStore键值展开为字段 | native:explodehstorefield | extension |
| Field calculator | 用表达式计算新字段 | native:fieldcalculator | core |
| Refactor fields | 重构字段结构与类型映射 | native:refactorfields | extension |
| Rename field | 重命名属性字段 | qgis:renametablefield | extension |
| Retain fields | 只保留指定的属性字段 | native:retainfields | extension |
| Text to float | 把文本字段转换为浮点数 | qgis:texttofloat | extension |

## 矢量瓦片（Vector Tiles）

| 官方名 | 一句话作用 | 算法ID | 判断 |
|---|---|---|---|
| Download vector tiles | 下载矢量瓦片到本地文件 | native:downloadvectortiles | defer |
| Write vector tiles (MBTiles) | 图层写出为MBTiles矢量瓦片 | native:writevectortiles_mbtiles | extension |
| Write vector tiles (XYZ) | 图层写出为XYZ目录矢量瓦片 | native:writevectortiles_xyz | extension |

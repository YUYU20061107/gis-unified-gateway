# 长尾桌面软件与服务端软件功能普查（others-services）

- 普查日期：2026-11-02。证据口径：只用各软件**官方 Help/文档站**（一级证据）；个别功能域的组织方式参考了厂商官方产品页（同为官方源，文中注明）；论坛/博客未用作功能依据。
- 平台判断三档：**core**＝应进平台统一对象模型/统一动词面或平台公共能力；**extension**＝进厂商/软件专属扩展命名空间；**defer**＝暂缓（小众、高风险、与当前路线无关或许可/地域不适配）。
- 现有桥工具面基线：`~/workspace/dsh-skills/gis-agent-bridges/manifest/tools-manifest.json`（离线协议自检级盘点）。统一入口 v0 现状：8 个只读动词、仅覆盖 SuperMap/ArcGIS Pro/ArcMap/QGIS 四家桌面软件；服务端未进统一对象模型（B 阶段刚补数据目录）。

---

# B 组（服务端，功能级）

## 1. PostGIS

### 1) 文档入口与版本口径
- 官方手册（postgis.net 在线版，current 线，2026-11-02 实查）：Chapter 7 PostGIS Reference https://postgis.net/docs/en/reference.html ；Chapter 11 Raster Reference（3.6 版页）https://postgis.net/docs/manual-3.6/en/RT_reference.html ；Chapter 9 Topology（dev 版页）https://postgis.net/docs/manual-dev/en/Topology.html ；Chapter 8 SFCGAL Functions Reference http://postgis.net/docs/manual-dev/reference_sfcgal.html ；TIGER Geocoder 函数页（以 Pagc_Normalize_Address 页为代表）https://postgis.net/docs/manual-3.6/es/Pagc_Normalize_Address.html 。
- 组成（手册 Ch.1 口径）：扩展 `postgis`（矢量核心）、`postgis_raster`、`postgis_topology`、`postgis_sfcgal`、`postgis_tiger_geocoder`＋`address_standardizer`。本节调用入口除注明外均为 **SQL 函数**（geometry/geography/raster 运算符注明「SQL 运算符」）。

### 2) 功能域总览（按官方手册组织）
数据类型与表管理 → 几何构造/访问/编辑/校验 → 坐标系 → 格式输入输出 → 空间运算符 → 空间关系与量测 → 叠加与几何处理 → 覆盖（Coverage）→ 仿射/聚类/包围盒 → 线性参考与轨迹 → 版本与配置；栅格：管理/构造/访问/像元/编辑/统计/输入输出/地图代数/DEM/矢量化/关系；拓扑（SQL-MM）；SFCGAL 三维；TIGER 地理编码（美国专用）。

### 3) 功能清单

#### 7.2 表管理函数
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| AddGeometryColumn | 为已有表添加 geometry 列 | SQL | extension |
| DropGeometryColumn | 移除 geometry 列 | SQL | extension |
| DropGeometryTable | 删表并清除 geometry_columns 引用 | SQL | extension |
| Find_SRID | 返回几何列的 SRID | SQL | extension |
| Populate_Geometry_Columns | 补齐几何列类型修饰/约束定义 | SQL | extension |
| UpdateGeometrySRID | 批量更新整列 SRID 与元数据 | SQL | extension |

#### 7.3 几何构造
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_Collect | 聚合一组几何为集合/多几何 | SQL（聚合） | core |
| ST_LineFromMultiPoint | 由 MultiPoint 连成 LineString | SQL | core |
| ST_MakeEnvelope | 由 min/max 坐标建矩形 Polygon | SQL | core |
| ST_MakeLine | 由点/线串成 LineString | SQL | core |
| ST_MakePoint | 建 2D/3DZ/4D 点 | SQL | core |
| ST_MakePointM | 由 X、Y、M 建点 | SQL | core |
| ST_MakePolygon | 由外壳＋可选洞建 Polygon | SQL | core |
| ST_Point | 建带 SRID 的点 | SQL | core |
| ST_PointZ | 建带 SRID 的 XYZ 点 | SQL | core |
| ST_PointM | 建带 SRID 的 XYM 点 | SQL | core |
| ST_PointZM | 建带 SRID 的 XYZM 点 | SQL | core |
| ST_Polygon | 由 LineString 建 Polygon | SQL | core |
| ST_TileEnvelope | 按 XYZ 瓦片编号建 Web Mercator 范围面 | SQL | core |
| ST_HexagonGrid | 生成铺满范围的六边形网格集 | SQL | extension |
| ST_Hexagon | 按网格坐标生成单个六边形 | SQL | extension |
| ST_SquareGrid | 生成铺满范围的方格网格集 | SQL | extension |
| ST_Square | 按网格坐标生成单个方格 | SQL | extension |
| ST_Letters | 把字母文本渲染为几何 | SQL | defer |

#### 7.4 几何访问器
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| GeometryType | 返回几何类型文本 | SQL | core |
| ST_Boundary | 返回几何边界 | SQL | core |
| ST_BoundingDiagonal | 返回包围盒对角线 | SQL | extension |
| ST_CoordDim | 返回坐标维数 | SQL | core |
| ST_Dimension | 返回拓扑维数 | SQL | core |
| ST_Dump | 把集合拆为 geometry_dump 行集 | SQL | core |
| ST_DumpPoints | 拆出全部坐标点行集 | SQL | core |
| ST_DumpSegments | 拆出全部线段行集 | SQL | extension |
| ST_DumpRings | 拆出面的内外环行集 | SQL | extension |
| ST_EndPoint | 返回线串最后一个点 | SQL | core |
| ST_Envelope | 返回包围盒几何 | SQL | core |
| ST_ExteriorRing | 返回 Polygon 外环 | SQL | core |
| ST_GeometryN | 取集合中第 N 个元素 | SQL | core |
| ST_GeometryType | 返回 SQL-MM 类型名 | SQL | core |
| ST_HasArc | 是否含圆弧 | SQL | extension |
| ST_InteriorRingN | 返回第 N 个内环 | SQL | core |
| ST_NumCurves | 返回复合曲线的曲线段数 | SQL | defer |
| ST_CurveN | 返回第 N 段曲线 | SQL | defer |
| ST_IsClosed | 线串首尾是否重合（闭合） | SQL | core |
| ST_IsCollection | 是否为集合类型 | SQL | core |
| ST_IsEmpty | 是否为空几何 | SQL | core |
| ST_IsPolygonCCW | 外环是否逆时针/内环顺时针 | SQL | extension |
| ST_IsPolygonCW | 外环是否顺时针/内环逆时针 | SQL | extension |
| ST_IsRing | 是否闭合且简单（环） | SQL | core |
| ST_IsSimple | 是否无自交/自切 | SQL | core |
| ST_M | 返回点的 M 坐标 | SQL | extension |
| ST_MemSize | 返回几何占用内存字节数 | SQL | extension |
| ST_NDims | 返回坐标维数（2/3/4） | SQL | core |
| ST_NPoints | 返回全部顶点数 | SQL | core |
| ST_NRings | 返回多边形环数 | SQL | core |
| ST_NumGeometries | 返回集合元素数 | SQL | core |
| ST_NumInteriorRings | 返回内环（洞）数 | SQL | core |
| ST_NumInteriorRing | 同上（别名） | SQL | defer |
| ST_NumPatches | 返回多面体的面片数 | SQL | defer |
| ST_NumPoints | 返回线串顶点数 | SQL | core |
| ST_PatchN | 返回多面体第 N 个面片 | SQL | defer |
| ST_PointN | 返回线串第 N 个顶点 | SQL | core |
| ST_Points | 全部顶点转 MultiPoint | SQL | extension |
| ST_StartPoint | 返回线串第一个点 | SQL | core |
| ST_Summary | 返回几何内容文本摘要 | SQL | core |
| ST_X | 返回点的 X 坐标 | SQL | core |
| ST_Y | 返回点的 Y 坐标 | SQL | core |
| ST_Z | 返回点的 Z 坐标 | SQL | core |
| ST_Zmflag | 返回 ZM 维数标志码 | SQL | extension |
| ST_HasZ | 是否有 Z 维 | SQL | extension |
| ST_HasM | 是否有 M 维 | SQL | extension |

#### 7.5 几何编辑器（均为写变换，进扩展并走确认门）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_AddPoint | 向 LineString 插入点 | SQL | extension |
| ST_CollectionExtract | 从集合按类型抽取元素 | SQL | extension |
| ST_CollectionHomogenize | 集合转最简表示 | SQL | extension |
| ST_CurveToLine | 曲线几何转折线几何 | SQL | extension |
| ST_Scroll | 更换闭合线串的起点 | SQL | defer |
| ST_FlipCoordinates | 交换 X/Y 轴 | SQL | extension |
| ST_Force2D | 强制降为 2D | SQL | extension |
| ST_Force3D / ST_Force3DZ | 强制升为 XYZ | SQL | extension |
| ST_Force3DM | 强制升为 XYM | SQL | extension |
| ST_Force4D | 强制升为 XYZM | SQL | extension |
| ST_ForceCollection | 强制转为 GeometryCollection | SQL | extension |
| ST_ForceCurve | 升格为曲线类型 | SQL | defer |
| ST_ForcePolygonCCW | 强制外环逆时针/内环顺时针 | SQL | extension |
| ST_ForcePolygonCW | 强制外环顺时针/内环逆时针 | SQL | extension |
| ST_ForceSFS | 强制 SFS 1.1 类型 | SQL | extension |
| ST_ForceRHR | 强制右手定则环向 | SQL | extension |
| ST_LineExtend | 线两端按距离延长 | SQL | extension |
| ST_LineToCurve | 折线转曲线 | SQL | defer |
| ST_Multi | 转为 MULTI* 类型 | SQL | extension |
| ST_Normalize | 返回规范形几何 | SQL | extension |
| ST_Project | 由起点＋距离＋方位角投影出新点 | SQL | extension |
| ST_QuantizeCoordinates | 坐标低位置零（量化） | SQL | extension |
| ST_RemovePoint | 删除线串指定点 | SQL | extension |
| ST_RemoveRepeatedPoints | 删除重复顶点 | SQL | extension |
| ST_RemoveIrrelevantPointsForView | 删除对给定视图无关的点 | SQL | extension |
| ST_RemoveSmallParts | 删除小环/小线段部件 | SQL | extension |
| ST_Reverse | 顶点顺序反转 | SQL | extension |
| ST_Segmentize | 按最大段长加密顶点 | SQL | extension |
| ST_SetPoint | 替换线串指定点 | SQL | extension |
| ST_ShiftLongitude | 经度在 -180..180 与 0..360 间平移 | SQL | extension |
| ST_WrapX | 几何绕指定 X 值卷绕 | SQL | extension |
| ST_SnapToGrid | 顶点吸附到规则网格 | SQL | extension |
| ST_Snap | 顶点/线段吸附到参考几何 | SQL | extension |
| ST_SwapOrdinates | 交换指定坐标轴值 | SQL | extension |

#### 7.6 几何校验
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_IsValid | 是否符合 OGC SFS 有效性 | SQL | core |
| ST_IsValidDetail | 返回有效性＋无效原因与位置 | SQL | core |
| ST_IsValidReason | 返回有效性文本说明 | SQL | core |
| ST_MakeValid | 尝试修复无效几何（不丢顶点） | SQL | extension |

#### 7.7 空间参考系
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_SetSRID | 给几何打 SRID 标记 | SQL | core |
| ST_SRID | 读取几何 SRID | SQL | core |
| ST_Transform | 坐标转换到另一 SRS | SQL | core |
| ST_TransformPipeline | 用 PROJ 管线字符串做坐标转换 | SQL | extension |
| ST_InverseTransformPipeline | 用管线的逆做坐标转换 | SQL | extension |
| postgis_srs | 返回指定权威机构/SRID 的 SRS 元数据 | SQL | extension |
| postgis_srs_codes | 返回某权威机构的全部 SRS 代码 | SQL | extension |
| postgis_srs_all | 返回 PROJ 库全部 SRS 元数据 | SQL | extension |
| postgis_srs_search | 按范围查完全覆盖它的投影坐标系 | SQL | extension |

#### 7.8 几何输入
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_GeomFromText | WKT → geometry | SQL | core |
| ST_GeomFromEWKT | EWKT → geometry | SQL | core |
| ST_GeogFromText | WKT/EWKT → geography | SQL | core |
| ST_GeomFromWKB | WKB → geometry | SQL | core |
| ST_GeomFromEWKB | EWKB → geometry | SQL | core |
| ST_GeogFromWKB | WKB/EWKB → geography | SQL | core |
| ST_GeomFromGeoJSON | GeoJSON → geometry | SQL | core |
| ST_GeomFromGML | GML → geometry | SQL | core |
| ST_GeomFromKML | KML → geometry | SQL | core |
| ST_GeomFromTWKB | TWKB → geometry | SQL | extension |
| ST_GeomFromGeoHash | GeoHash → geometry | SQL | extension |
| ST_Box2dFromGeoHash | GeoHash → BOX2D | SQL | extension |
| ST_PointFromGeoHash | GeoHash → 点 | SQL | extension |
| ST_LineFromEncodedPolyline | 编码折线 → LineString | SQL | extension |
| ST_FromFlatGeobuf | 读 FlatGeobuf 数据 | SQL | extension |
| ST_FromFlatGeobufToTable | 按 FlatGeobuf 结构建表 | SQL | extension |
| ST_BdPolyFromText | 由闭合线集 WKT 构面 | SQL | extension |
| ST_BdMPolyFromText | 由闭合线集 WKT 构多面 | SQL | extension |
| ST_GeomCollFromText | WKT → 集合几何 | SQL | extension |
| ST_LineFromText / ST_MLineFromText / ST_MPointFromText / ST_MPolyFromText / ST_PointFromText / ST_PolygonFromText | WKT → 指定类型几何 | SQL | extension |
| ST_LineFromWKB / ST_PointFromWKB | WKB → 指定类型几何 | SQL | extension |
| ST_GeomFromMARC21 | MARC21/XML 地理数据 → geometry | SQL | defer |
| ST_GeometryFromText / ST_WKTToSQL / ST_WKBToSQL / ST_GMLToSQL / ST_GeographyFromText / ST_LinestringFromWKB | 上述函数的别名 | SQL | defer |

#### 7.9 几何输出
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_AsText | geometry → WKT | SQL | core |
| ST_AsEWKT | geometry → 带 SRID 的 EWKT | SQL | core |
| ST_AsBinary | geometry → WKB | SQL | core |
| ST_AsEWKB | geometry → EWKB | SQL | core |
| ST_AsGeoJSON | geometry/要素 → GeoJSON | SQL | core |
| ST_AsGML | geometry → GML 2/3 | SQL | core |
| ST_AsKML | geometry → KML | SQL | core |
| ST_AsMVT | 行集聚合 → Mapbox 矢量瓦片 | SQL（聚合） | core |
| ST_AsMVTGeom | 几何变换到 MVT 瓦片坐标空间 | SQL | core |
| ST_AsSVG | geometry → SVG 路径 | SQL | extension |
| ST_AsTWKB | geometry → TWKB | SQL | extension |
| ST_AsFlatGeobuf | 行集 → FlatGeobuf | SQL | extension |
| ST_AsGeobuf | 行集 → Geobuf | SQL | extension |
| ST_AsHEXEWKB | geometry → HEXEWKB 文本 | SQL | extension |
| ST_AsEncodedPolyline | LineString → 编码折线 | SQL | extension |
| ST_AsLatLonText | 点 → 度分秒文本 | SQL | extension |
| ST_GeoHash | geometry → GeoHash | SQL | extension |
| ST_AsX3D | geometry → X3D XML | SQL | defer |
| ST_AsMARC21 | geometry → MARC21/XML 记录 | SQL | defer |

#### 7.10 运算符（索引谓词与 KNN 距离）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| && | 两几何 2D 包围盒相交（索引过滤） | SQL 运算符 | core |
| &&& | 两几何 n 维包围盒相交 | SQL 运算符 | extension |
| @ | A 的包围盒被 B 包含 | SQL 运算符 | core |
| ~ | A 的包围盒包含 B | SQL 运算符 | core |
| ~= | 两包围盒相同 | SQL 运算符 | extension |
| = | 两几何坐标与顺序全等 | SQL 运算符 | extension |
| &< / &<\| / &> / << / <<\| / >> / \|&> / \|>> | 包围盒相对位置族（左/下/右/上等） | SQL 运算符 | extension |
| <-> | 两几何二维距离（KNN 排序） | SQL 运算符 | core |
| <#> | 两包围盒二维距离（KNN 近似） | SQL 运算符 | core |
| <<->> | n 维距离 | SQL 运算符 | extension |
| \|=\| | 两轨迹最近接近距离 | SQL 运算符 | extension |

#### 7.11 空间关系
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_Intersects | 是否相交 | SQL | core |
| ST_Contains | A 是否包含 B | SQL | core |
| ST_ContainsProperly | A 是否真包含 B（内部） | SQL | core |
| ST_Covers | A 是否覆盖 B | SQL | core |
| ST_CoveredBy | A 是否被 B 覆盖 | SQL | core |
| ST_Within | A 是否在 B 内 | SQL | core |
| ST_Crosses | 是否穿越 | SQL | core |
| ST_Overlaps | 是否部分重叠 | SQL | core |
| ST_Touches | 是否相接（仅边界接触） | SQL | core |
| ST_Disjoint | 是否分离 | SQL | core |
| ST_Equals | 是否表示同一几何 | SQL | core |
| ST_Relate | 计算/检验 DE-9IM 交集矩阵 | SQL | core |
| ST_RelateMatch | DE-9IM 矩阵模式匹配 | SQL | extension |
| ST_LineCrossingDirection | 两线穿越行为判定 | SQL | extension |
| ST_OrderingEquals | 同几何且顶点同序判定 | SQL | extension |
| ST_3DIntersects | 三维相交判定（点/线/面/多面体） | SQL | extension |
| ST_DWithin | 是否在给定距离内 | SQL | core |
| ST_DFullyWithin | 是否整体在给定距离内 | SQL | core |
| ST_3DDWithin | 三维距离内判定 | SQL | extension |
| ST_3DDFullyWithin | 三维整体距离内判定 | SQL | extension |
| ST_PointInsideCircle | 点是否在圆内 | SQL | extension |

#### 7.12 量测
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_Distance | 两几何/geography 间距离 | SQL | core |
| ST_DistanceSphere | 球面模型经纬距离（米） | SQL | core |
| ST_DistanceSpheroid | 椭球模型经纬距离（米） | SQL | core |
| ST_Area | 多边形面积 | SQL | core |
| ST_Length | 线几何二维长度 | SQL | core |
| ST_LengthSpheroid | 椭球模型线长/面周长 | SQL | core |
| ST_Perimeter | 多边形边界长度 | SQL | core |
| ST_Azimuth | 两点北向方位角 | SQL | core |
| ST_ClosestPoint | g1 上距 g2 最近的点 | SQL | core |
| ST_ShortestLine | 两几何间最短线 | SQL | core |
| ST_Angle | 三/四点或两线夹角 | SQL | extension |
| ST_3DClosestPoint | 三维最近点 | SQL | extension |
| ST_3DDistance | 三维笛卡尔距离 | SQL | extension |
| ST_3DLength | 三维线长 | SQL | extension |
| ST_3DPerimeter | 三维面周长 | SQL | extension |
| ST_3DShortestLine | 三维最短线 | SQL | extension |
| ST_3DLongestLine | 三维最长线 | SQL | extension |
| ST_LongestLine | 二维最长线 | SQL | extension |
| ST_MaxDistance | 二维最大距离 | SQL | extension |
| ST_3DMaxDistance | 三维最大距离 | SQL | extension |
| ST_FrechetDistance | Fréchet 距离 | SQL | extension |
| ST_HausdorffDistance | Hausdorff 距离 | SQL | extension |
| ST_MinimumClearance | 最小净距（鲁棒性量度） | SQL | extension |
| ST_MinimumClearanceLine | 跨最小净距的两点线 | SQL | extension |
| ST_Length2D / ST_Perimeter2D | ST_Length / ST_Perimeter 别名 | SQL | defer |

#### 7.13 叠加（布尔运算）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_Intersection | 两几何公共部分 | SQL | core |
| ST_Difference | A 减去与 B 相交部分 | SQL | core |
| ST_SymDifference | 两几何互不相交部分 | SQL | core |
| ST_Union | 一组几何的并集 | SQL（聚合） | core |
| ST_UnaryUnion | 单几何内部构件并集 | SQL | core |
| ST_Split | 用另一几何分割几何 | SQL | core |
| ST_ClipByBox2D | 按矩形裁剪几何 | SQL | core |
| ST_Node | 给线集打断成节点化线集 | SQL | extension |
| ST_Subdivide | 把几何细分为矩形小块集 | SQL | extension |
| ST_MemUnion | 内存友好（较慢）的并集聚合 | SQL（聚合） | extension |

#### 7.14 几何处理（构造类）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_Buffer | 缓冲区 | SQL | core |
| ST_Centroid | 几何中心 | SQL | core |
| ST_PointOnSurface | 保证落在几何上的点 | SQL | core |
| ST_ConvexHull | 凸包 | SQL | core |
| ST_OrientedEnvelope | 最小面积外接矩形 | SQL | core |
| ST_Simplify | Douglas-Peucker 简化 | SQL | core |
| ST_SimplifyPreserveTopology | 保拓扑简化 | SQL | core |
| ST_LineMerge | 多线串缝合为线 | SQL | core |
| ST_ConcaveHull | 凹包 | SQL | extension |
| ST_BuildArea | 由线框架构面 | SQL | extension |
| ST_Polygonize | 由线集多边形化 | SQL | extension |
| ST_DelaunayTriangles | Delaunay 三角剖分 | SQL | extension |
| ST_TriangulatePolygon | 多边形约束 Delaunay 剖分 | SQL | extension |
| ST_VoronoiPolygons | Voronoi 单元面 | SQL | extension |
| ST_VoronoiLines | Voronoi 边界线 | SQL | extension |
| ST_OffsetCurve | 线的平行偏移曲线 | SQL | extension |
| ST_GeneratePoints | 面内生成随机点集 | SQL | extension |
| ST_GeometricMedian | 多点几何中位数 | SQL | extension |
| ST_ChaikinSmoothing | Chaikin 平滑 | SQL | extension |
| ST_MinimumBoundingCircle | 最小外接圆 | SQL | extension |
| ST_MinimumBoundingRadius | 最小外接圆圆心＋半径 | SQL | extension |
| ST_MaximumInscribedCircle | 最大内切圆 | SQL | extension |
| ST_LargestEmptyCircle | 不与几何重叠的最大圆 | SQL | defer |
| ST_ReducePrecision | 按网格容差降精度并修复 | SQL | extension |
| ST_SharedPaths | 两线串的共享路径 | SQL | extension |
| ST_SimplifyVW | Visvalingam-Whyatt 简化 | SQL | extension |
| ST_SimplifyPolygonHull | 多边形保拓扑内外壳简化 | SQL | extension |
| ST_SetEffectiveArea | 按 VW 算法给顶点设有效面积 | SQL | extension |
| ST_FilterByM | 按 M 值过滤顶点 | SQL | defer |

#### 7.15 覆盖（Coverage，窗口函数族）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_CoverageInvalidEdges | 找出不构成有效覆盖的边位置 | SQL（窗口） | extension |
| ST_CoverageSimplify | 简化覆盖的共享边 | SQL（窗口） | extension |
| ST_CoverageUnion | 覆盖并集（去共享边） | SQL | extension |
| ST_CoverageClean | 把非洁净输入整理为边匹配覆盖 | SQL | extension |

#### 7.16 仿射变换
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_Affine | 3D 仿射变换 | SQL | extension |
| ST_Rotate | 绕原点旋转 | SQL | extension |
| ST_RotateX | 绕 X 轴旋转 | SQL | extension |
| ST_RotateY | 绕 Y 轴旋转 | SQL | extension |
| ST_RotateZ | 绕 Z 轴旋转 | SQL | extension |
| ST_Scale | 按因子缩放 | SQL | extension |
| ST_Translate | 按偏移平移 | SQL | extension |
| ST_TransScale | 平移＋缩放复合 | SQL | extension |

#### 7.17 聚类
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_ClusterDBSCAN | DBSCAN 聚类编号 | SQL（窗口） | extension |
| ST_ClusterKMeans | K-means 聚类编号 | SQL（窗口） | extension |
| ST_ClusterWithin | 按间距阈值聚合聚类 | SQL（聚合） | extension |
| ST_ClusterWithinWin | 按间距阈值窗口聚类 | SQL（窗口） | extension |
| ST_ClusterIntersecting | 相交连通集聚合聚类 | SQL（聚合） | extension |
| ST_ClusterIntersectingWin | 相交连通集窗口聚类 | SQL（窗口） | extension |

#### 7.18 包围盒
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| Box2D | 返回几何的 BOX2D 范围 | SQL | core |
| ST_MakeBox2D | 由两点建 BOX2D | SQL | core |
| ST_Extent | 一组几何的包围盒 | SQL（聚合） | core |
| ST_Expand | 扩展包围盒/几何范围 | SQL | core |
| ST_XMin / ST_XMax / ST_YMin / ST_YMax | 包围盒各向极值 | SQL | core |
| Box3D | 返回几何的 BOX3D 范围 | SQL | extension |
| ST_3DMakeBox | 由两点建 BOX3D | SQL | extension |
| ST_3DExtent | 一组几何的三维包围盒 | SQL（聚合） | extension |
| ST_EstimatedExtent | 估算空间表的范围（统计信息） | SQL | extension |
| ST_ZMin / ST_ZMax | 包围盒 Z 极值 | SQL | extension |

#### 7.19 线性参考
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_LineInterpolatePoint | 按比例在线上插值取点 | SQL | extension |
| ST_3DLineInterpolatePoint | 三维线插值取点 | SQL | extension |
| ST_LineInterpolatePoints | 按间隔插值取点集 | SQL | extension |
| ST_LineLocatePoint | 点在线上的比例位置 | SQL | extension |
| ST_LineSubstring | 按比例区间截取子线 | SQL | extension |
| ST_LocateAlong | 按量测值定位点 | SQL | extension |
| ST_LocateBetween | 按量测区间截取 | SQL | extension |
| ST_InterpolatePoint | 点在几何上的插值量测值 | SQL | extension |
| ST_AddMeasure | 沿线插值量测（M） | SQL | extension |
| ST_LocateBetweenElevations | 按高程区间截取 | SQL | defer |

#### 7.20 轨迹
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_IsValidTrajectory | 是否为合法轨迹（M 递增） | SQL | extension |
| ST_ClosestPointOfApproach | 两轨迹最近接近点的量测值 | SQL | extension |
| ST_DistanceCPA | 最近接近距离 | SQL | extension |
| ST_CPAWithin | 最近接近是否在阈值内 | SQL | extension |

#### 7.21 版本与运行时（7.22 GUC 配置族不入动词面）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| PostGIS_Version | PostGIS 版本与编译选项 | SQL | core |
| PostGIS_Full_Version | 完整版本与构建配置（discover 证据） | SQL | core |
| PostGIS_Lib_Version | 库版本号 | SQL | extension |
| PostGIS_GEOS_Version | GEOS 库版本 | SQL | extension |
| PostGIS_PROJ_Version | PROJ 库版本 | SQL | extension |
| PostGIS_Scripts_Installed | 已装脚本版本 | SQL | extension |
| PostGIS_Extensions_Upgrade | 打包/升级各扩展到指定或最新版 | SQL | extension |
| PostGIS_GEOS_Compiled_Version / PostGIS_PROJ_Compiled_Version / PostGIS_Liblwgeom_Version / PostGIS_LibXML_Version / PostGIS_LibJSON_Version / PostGIS_Lib_Build_Date / PostGIS_Scripts_Build_Date / PostGIS_Scripts_Released / PostGIS_Wagyu_Version | 各依赖的编译/构建细节 | SQL | defer |

#### 11.x 栅格（postgis_raster，手册 Chapter 11）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| ST_GDALDrivers | 列出 GDAL 支持的栅格格式（格式能力发现） | SQL | core |
| PostGIS_Raster_Lib_Version | 栅格库版本与构建信息 | SQL | extension |
| PostGIS_GDAL_Version | GDAL 库版本 | SQL | extension |
| AddRasterConstraints | 给栅格表加约束（SR/比例/块/对齐/波段） | SQL | extension |
| DropRasterConstraints | 删除栅格表约束 | SQL | extension |
| AddOverviewConstraints | 标记某栅格列为概览 | SQL | extension |
| DropOverviewConstraints | 取消概览标记 | SQL | defer |
| UpdateRasterSRID | 整列更换 SRID | SQL | extension |
| ST_CreateOverview | 生成降分辨率概览栅格 | SQL | extension |
| ST_FromGDALRaster | GDAL 文件 → raster（入库） | SQL | core |
| ST_Band | 抽取一个/多个波段为新栅格 | SQL | core |
| ST_AddBand | 追加波段 | SQL | extension |
| ST_AsRaster | 几何 → 栅格 | SQL | extension |
| ST_AsRasterAgg | 几何集渲染为栅格（聚合） | SQL（聚合） | extension |
| ST_MakeEmptyRaster | 建空栅格（定尺寸/原点/像元/旋转/SRID） | SQL | extension |
| ST_MakeEmptyCoverage | 空栅格瓦片网格覆盖 | SQL | extension |
| ST_Tile | 栅格按尺寸切分 | SQL | extension |
| ST_Retile | 覆盖重切分为既定瓦片集 | SQL | extension |
| ST_MetaData | 栅格基本元数据（像元大小/旋转/角点） | SQL | core |
| ST_Summary | 栅格内容文本摘要 | SQL | core |
| ST_Width / ST_Height | 栅格宽/高（像元） | SQL | core |
| ST_NumBands | 波段数 | SQL | core |
| ST_PixelWidth / ST_PixelHeight | 像元宽/高（坐标单位） | SQL | core |
| ST_SRID（栅格） | 栅格 SRID | SQL | core |
| ST_GeoReference | 地理参考（GDAL/ESRI 世界文件格式） | SQL | extension |
| ST_RasterToWorldCoord | 行列号 → 世界坐标角点 | SQL | extension |
| ST_WorldToRasterCoord | 世界坐标/点 → 行列号 | SQL | extension |
| ST_ScaleX / ST_ScaleY | 像元 X/Y 尺度 | SQL | extension |
| ST_Rotation / ST_SkewX / ST_SkewY | 旋转/斜切参数 | SQL | extension |
| ST_UpperLeftX / ST_UpperLeftY | 左上角坐标 | SQL | extension |
| ST_RasterToWorldCoordX / ST_RasterToWorldCoordY / ST_WorldToRasterCoordX / ST_WorldToRasterCoordY | 坐标换算分量版 | SQL | defer |
| ST_IsEmpty（栅格） / ST_MemSize（栅格） | 是否空栅格 / 占用字节 | SQL | defer |
| ST_BandMetaData | 指定波段元数据 | SQL | core |
| ST_BandNoDataValue | 波段 NoData 值 | SQL | core |
| ST_BandPixelType | 波段像元类型 | SQL | core |
| ST_BandIsNoData | 波段是否全为 NoData | SQL | extension |
| ST_BandPath | 库外波段文件路径 | SQL | extension |
| ST_HasNoBand | 是否无此波段 | SQL | extension |
| ST_BandFileSize / ST_BandFileTimestamp / ST_MinPossibleValue | 库外文件大小/时间戳 / 像元类型最小值 | SQL | defer |
| ST_Value | 取指定行列/点处像元值 | SQL | core |
| ST_NearestValue | 最近非 NoData 像元值 | SQL | extension |
| ST_Neighborhood | 取像元邻域二维数组 | SQL | extension |
| ST_DumpValues | 整波段值导出为二维数组 | SQL | extension |
| ST_PixelOfValue | 按值反查像元行列 | SQL | extension |
| ST_PixelAsPoint / ST_PixelAsPoints | 像元角点几何 | SQL | extension |
| ST_PixelAsCentroid / ST_PixelAsCentroids | 像元中心点几何 | SQL | extension |
| ST_PixelAsPolygon / ST_PixelAsPolygons | 像元面几何 | SQL | extension |
| ST_SetZ | 用栅格值给几何赋 Z | SQL | extension |
| ST_SetM | 用栅格值给几何赋 M | SQL | extension |
| ST_SetValue / ST_SetValues | 写像元值（写操作） | SQL | extension |
| ST_Resample | 按算法/尺寸/网格重采样 | SQL | core |
| ST_Transform（栅格） | 栅格重投影 | SQL | core |
| ST_Rescale | 仅改像元大小重采样 | SQL | extension |
| ST_SnapToGrid（栅格） | 吸附到网格重采样 | SQL | extension |
| ST_Resize | 改宽高尺寸 | SQL | extension |
| ST_Reskew / ST_SetRotation / ST_SetSkew | 斜切/旋转类调整 | SQL | defer |
| ST_SetGeoReference | 一次设定 6 个地理参考参数 | SQL | extension |
| ST_SetScale / ST_SetUpperLeft / ST_SetSRID（栅格） | 设定像元尺度/左上角/SRID | SQL | extension |
| ST_SetBandNoDataValue | 设定波段 NoData 值 | SQL | extension |
| ST_SetBandPath / ST_SetBandIndex | 更新库外波段路径/编号 | SQL | extension |
| ST_SetBandIsNoData | 设定波段 isnodata 标志 | SQL | defer |
| ST_Count / ST_CountAgg | 波段像元计数 | SQL | core |
| ST_SummaryStats / ST_SummaryStatsAgg | 波段统计（count/sum/mean/stddev/min/max） | SQL | core |
| ST_Histogram | 直方图分箱统计 | SQL | core |
| ST_ValueCount | 指定值像元计数 | SQL | core |
| ST_Quantile | 分位数 | SQL | extension |
| ST_RastFromWKB | WKB → raster | SQL | extension |
| ST_RastFromHexWKB | Hex WKB → raster | SQL | defer |
| ST_AsGDALRaster | raster → 指定 GDAL 格式字节 | SQL | core |
| ST_AsTIFF | raster → TIFF 字节 | SQL | core |
| ST_AsPNG | raster → PNG 字节 | SQL | core |
| ST_AsJPEG | raster → JPEG 字节 | SQL | core |
| ST_AsBinary / ST_AsWKB（栅格） | raster → WKB | SQL | extension |
| ST_AsHexWKB（栅格） | raster → Hex WKB | SQL | defer |
| ST_MapAlgebra（表达式版） | 一/两波段代数表达式生成新波段（波段运算主入口） | SQL | core |
| ST_MapAlgebra（回调版） / ST_MapAlgebraFct / ST_MapAlgebraFctNgb / ST_MapAlgebraExpr | 自定义函数/邻域地图代数 | SQL | extension |
| ST_Reclass | 按规则重分类 | SQL | core |
| ST_ReclassExact | 1:1 精确映射重分类 | SQL | extension |
| ST_Clip | 用几何裁剪栅格 | SQL | core |
| ST_ColorMap | 按色带生成彩色栅格 | SQL | extension |
| ST_Grayscale | RGB 波段合成灰度栅格 | SQL | extension |
| ST_Intersection（栅格） | 两栅格/栅格与几何的交集（值对） | SQL | extension |
| ST_Union（栅格） | 一组栅格瓦片并为单栅格 | SQL（聚合） | extension |
| ST_Distinct4ma | 邻域唯一值计数（回调） | SQL | extension |
| ST_InvDistWeight4ma | 反距离权重插值（回调） | SQL | extension |
| ST_Max4ma / ST_Mean4ma / ST_Min4ma / ST_Range4ma / ST_StdDev4ma / ST_Sum4ma | 邻域最值/均值/极差/标准差/求和（回调） | SQL | extension |
| ST_MinDist4ma | 到最近有值像元的距离（回调） | SQL | extension |
| ST_Slope | DEM 坡度 | SQL | core |
| ST_Aspect | DEM 坡向 | SQL | core |
| ST_HillShade | DEM 山体阴影 | SQL | core |
| ST_Contour | 栅格生成矢量等高线（GDAL 算法） | SQL | core |
| ST_Roughness | DEM 粗糙度 | SQL | extension |
| ST_TPI | 地形位置指数 | SQL | extension |
| ST_TRI | 地形 ruggedness 指数 | SQL | extension |
| ST_InterpolateRaster | 三维点插值成栅格面 | SQL | extension |
| ST_DumpAsPolygons | 波段矢量化为 (geom,val) 行集 | SQL | core |
| ST_Polygon（栅格） | 非 NoData 像元并为 MultiPolygon | SQL | extension |
| ST_Envelope（栅格） | 栅格范围面 | SQL | core |
| ST_ConvexHull（栅格） / ST_MinConvexHull | 栅格凸包 / 去 NoData 凸包 | SQL | extension |
| Box3D（栅格） | 栅格 BOX3D | SQL | defer |
| ST_IntersectionFractions | 几何覆盖各像元的比例 | SQL | extension |
| && / &< / &> / = / @ / ~= / ~（栅格） | 栅格包围盒运算符族 | SQL 运算符 | extension |
| ST_Intersects（栅格） | 两栅格是否相交 | SQL | core |
| ST_Contains / ST_ContainsProperly / ST_Covers / ST_CoveredBy / ST_Within / ST_Overlaps / ST_Touches / ST_Disjoint（栅格） | 栅格间拓扑关系族 | SQL | extension |
| ST_DWithin / ST_DFullyWithin（栅格） | 栅格距离关系 | SQL | extension |
| ST_SameAlignment / ST_NotSameAlignmentReason | 两栅格是否同网格对齐/不对齐原因 | SQL | extension |

#### 拓扑（postgis_topology，手册 Chapter 9，topology schema；全章 40+ 函数，此处列管理/构造/校验/访问主干）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| CreateTopology | 新建拓扑 schema 并注册 | SQL | extension |
| DropTopology | 删除拓扑 schema 及注册 | SQL | extension |
| CopyTopology | 复制整个拓扑 | SQL | extension |
| RenameTopology | 拓扑改名 | SQL | defer |
| TopologySummary | 拓扑对象计数摘要 | SQL | extension |
| ValidateTopology | 校验拓扑并返回错误集（质检） | SQL | extension |
| ValidateTopologyRelation | 校验 relation 记录合法性 | SQL | defer |
| FindTopology | 按层/表/名查拓扑记录 | SQL | extension |
| AddTopoGeometryColumn | 加 TopoGeometry 列并注册为拓扑层 | SQL | extension |
| ST_InitTopoGeo | SQL-MM 版新建空拓扑 | SQL | extension |
| ST_CreateTopoGeo | 向空拓扑批量灌入几何建拓扑 | SQL | extension |
| toTopoGeom | 普通几何 → TopoGeometry | SQL | extension |
| TopoGeo_AddPoint | 向拓扑加点（容差内可劈边） | SQL | extension |
| TopoGeo_AddLineString | 向拓扑加线（可劈边/面） | SQL | extension |
| TopoGeo_AddPolygon | 向拓扑加面（可劈边/面） | SQL | extension |
| ST_AddIsoNode / ST_AddIsoEdge / ST_AddEdgeModFace / ST_AddEdgeNewFaces | 原语级节点/边增改（SQL-MM 编辑族） | SQL | extension |
| ST_ModEdgeSplit / ST_ModEdgeHeal / ST_ChangeEdgeGeom | 边劈分/愈合/改形 | SQL | extension |
| ST_RemoveIsoNode / ST_RemIsoEdgeNewFace / ST_RemIsoEdgeOldFace / ST_MoveIsoNode | 原语级删除/移动 | SQL | extension |
| GetNodeByPoint / GetEdgeByPoint / GetFaceByPoint | 按点定位原语 | SQL | extension |
| ST_GetFaceGeometry | 面原语物化为 Polygon | SQL | extension |
| ST_GetFaceEdges | 取面的有序边列 | SQL | extension |
| GetTopoGeomElements | 取 TopoGeometry 的原语元素集 | SQL | extension |
| asTopoJSON / ST_AsTopoJSON 类输出 | TopoGeometry 序列化输出 | SQL | defer |

#### SFCGAL 三维（postgis_sfcgal，手册 Chapter 8）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| postgis_sfcgal_version | SFCGAL 版本 | SQL | extension |
| postgis_sfcgal_full_version | 含 CGAL/Boost 的完整版本 | SQL | defer |
| ST_Volume / CG_Volume | 三维实体体积 | SQL | extension |
| ST_3DArea / CG_3DArea | 三维表面积 | SQL | extension |
| CG_MakeSolid | 闭合面转实体（不校验） | SQL | extension |
| ST_IsSolid | 是否为实体 | SQL | extension |
| ST_IsPlanar | 表面是否平面 | SQL | defer |
| ST_Orientation | 表面定向 | SQL | defer |
| ST_ForceLHR | 强制左手定向 | SQL | defer |
| ST_3DUnion | 三维并集 | SQL | extension |
| ST_3DIntersection | 三维交集 | SQL | extension |
| ST_3DDifference | 三维差集 | SQL | extension |
| ST_3DConvexHull | 三维凸包 | SQL | extension |
| ST_AlphaShape | Alpha-shape 包裹 | SQL | extension |
| ST_ConstrainedDelaunayTriangles | 约束 Delaunay 三角网 | SQL | extension |
| ST_Tesselate / CG_Tesselate | 表面三角化为 TIN | SQL | extension |
| ST_Extrude / CG_Extrude | 面拉伸成体 | SQL | extension |
| CG_ExtrudeStraightSkeleton | 直骨架拉伸（带屋顶） | SQL | defer |
| ST_StraightSkeleton / CG_StraightSkeleton | 直骨架 | SQL | extension |
| ST_ApproximateMedialAxis | 近似中轴 | SQL | defer |
| ST_MinkowskiSum | Minkowski 和 | SQL | defer |

#### TIGER 地理编码（postgis_tiger_geocoder＋address_standardizer；美国 TIGER 数据专用）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| Normalize_Address | 地址标准化为 norm_addy | SQL | defer |
| Pagc_Normalize_Address | PAGC 版地址标准化（需 address_standardizer） | SQL | defer |
| Geocode | 地址 → 候选点位＋评分 | SQL | defer |
| Geocode_Intersection | 两路交叉口定位 | SQL | defer |
| Reverse_Geocode | 点 → 可能地址与交叉街道 | SQL | defer |
| Pprint_Addy | norm_addy 美化打印 | SQL | defer |
| Get_Geocode_Setting / Set_Geocode_Setting | 编码器设置读写 | SQL | defer |

### 4) 与现有桥的差距
现有桥仅 6 个工具（列空间表、列字段、表摘要、导 GeoJSON、ping、discover），且为只读元数据面：对手册约 530+ 条函数（矢量约 330、栅格约 150、拓扑/SFCGAL/TIGER 约 50），**已接通的分析函数为 0**，工具数覆盖 <2%；PostGIS 是全合集里「官方能力÷桥能力」落差最大的包。

### 5) 对平台升级的头号价值
PostGIS 是平台唯一现成的**服务端计算引擎**：空间关系/量测/叠加/简化/MVT 输出一套 SQL 就能把统一入口从「浏览四家桌面软件」升级为「有服务端分析与矢量瓦片直供」；ST_AsMVT＋ST_TileEnvelope 让平台不依赖任何桌面软件即可对外供瓦片，ST_IsValid 族又正好补上平台的几何质检动词。

---

## 2. GeoServer

### 1) 文档入口与版本口径
- 官方 User Manual（docs.geoserver.org，latest 线对应 2.28 世代，2026-11-02 实查）：总览与标准符合性 https://docs.geoserver.org/main/en/user/introduction/overview.html ；扩展总表 https://docs.geoserver.org/latest/en/user/extensions/index.html ；手册另有 Services（WMS/WFS/WCS/WMTS/WPS）、REST 配置 API、Styling、Data management 等章（REST 章节口径：以 Swagger 2.0 文件描述端点，官方自注该文件自 2017 年手写、未必与配置对象结构完全同步）。
- 版本口径：核心含 WMS 1.3.0/1.1.1、WFS 2.0/1.1.0/1.0.0、WCS 2.0、WMTS 1.0、CSW 2.0.2（实现）、OGC API - Features 1.0（扩展提供）；WPS 1.0 为扩展。

### 2) 功能域总览（按官方手册组织）
OGC 服务（WMS/WFS/WCS/WMTS＋GWC 瓦片缓存）→ 处理服务（WPS）→ 目录服务（CSW）→ OGC API 新族 → 数据管理（workspace/store/layer/style 对象模型、SQL 视图、ImageMosaic）→ REST 配置 API → 样式（SLD/CSS/YSLD/MBStyle）→ 安全（GeoFence、OAuth2、authkey）→ 40+ 扩展（导入、监控、打印、矢量瓦片、NetCDF 等）。

### 3) 功能清单（调用入口：OGC 为 HTTP 服务操作，配置类为 REST 端点）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| WMS GetCapabilities | 地图服务能力文档 | OGC WMS | core |
| WMS GetMap | 按图层/样式/范围出图 | OGC WMS | core |
| WMS GetFeatureInfo | 点查地图要素信息 | OGC WMS | core |
| WMS GetLegendGraphic | 取图例图 | OGC WMS | extension |
| WMS 动态 SLD（sld_body/sld 参数） | 请求级临时样式渲染 | OGC WMS | extension |
| WFS GetCapabilities / DescribeFeatureType | 要素服务能力/类型结构 | OGC WFS | core |
| WFS GetFeature | 按过滤取要素（GML/GeoJSON 等多格式） | OGC WFS | core |
| WFS Transaction（Insert/Update/Delete） | 事务编辑要素（WFS-T） | OGC WFS | extension |
| WFS LockFeature / GetFeatureWithLock | 要素锁定编辑 | OGC WFS | defer |
| WFS 存储查询（Stored Queries） | 预置参数化查询 | OGC WFS | extension |
| WCS GetCapabilities / DescribeCoverage | 覆盖服务能力/覆盖描述 | OGC WCS | core |
| WCS GetCoverage | 取栅格覆盖（子集/重采样/多格式） | OGC WCS | core |
| WMTS GetCapabilities / GetTile | 瓦片服务与取瓦片 | OGC WMTS | core |
| GWC 瓦片缓存与 Seed/Truncate | 预生成/清理瓦片缓存（含 REST 管理） | REST＋WMTS/WMS-C | extension |
| WPS DescribeProcess | 处理过程描述 | OGC WPS（扩展） | extension |
| WPS Execute | 同步/异步执行地理处理（JTS/GeoTools 过程族） | OGC WPS（扩展） | extension |
| WPS Download | 大结果异步下载处理 | OGC WPS（扩展） | extension |
| CSW GetRecords / GetRecordById | 元数据目录检索 | OGC CSW（扩展） | extension |
| OGC API - Features（collections/items） | REST 风格要素访问（GeoJSON/HTML） | OGC API（扩展） | core |
| OGC API - Tiles / Maps / Coverages / Styles / Processes | 新一代 API 族（社区模块、草案状态） | OGC API（社区模块） | extension |
| REST /workspaces（CRUD） | 工作区增删改查 | REST 配置 API | core |
| REST /namespaces（CRUD） | 命名空间管理 | REST 配置 API | extension |
| REST /workspaces/{ws}/datastores（CRUD＋file/url/external 上传） | 矢量存储建置与 Shapefile 等上传发布 | REST 配置 API | core |
| REST /workspaces/{ws}/coveragestores（CRUD＋上传） | 栅格存储建置与 GeoTIFF 等上传发布 | REST 配置 API | core |
| REST /featuretypes（发布/改） | 矢量图层发布与配置 | REST 配置 API | core |
| REST /coverages（发布/改） | 栅格图层发布与配置 | REST 配置 API | core |
| REST /layers（读/改） | 图层总览与默认样式等配置 | REST 配置 API | core |
| REST /layergroups（CRUD） | 图层组管理 | REST 配置 API | extension |
| REST /styles（CRUD，SLD） | 样式上传与管理 | REST 配置 API | core |
| CSS / YSLD / MBStyle 样式 | 替代样式语言 | REST＋样式模块 | extension |
| SQL 视图（虚拟表）图层 | 以参数化 SQL 定义图层数据源 | REST 配置 API | core |
| ImageMosaic 覆盖与颗粒挂载 | 时序/多景影像镶嵌图层与新颗粒接入 | REST 配置 API | extension |
| REST /reload、/reset | 配置重载/缓存重置 | REST 配置 API | extension |
| REST 安全与用户组（/security、/usergroup） | 用户、角色与访问规则 | REST 配置 API | defer |
| Importer 扩展 | 数据导入向导式任务（异步作业） | REST（扩展） | extension |
| Vector Tiles 扩展 | MVT/PBF/TopoJSON/GeoJSON 瓦片输出 | WMS/WMTS（扩展） | extension |
| Printing 扩展（MapFish Print） | 高质量地图打印/出图 | HTTP（扩展） | extension |
| Monitoring 扩展 | 请求审计与监控数据 | REST（扩展） | extension |
| Cross-layer filtering（querylayer） | 跨图层过滤查询 | WFS/WMS（扩展） | extension |
| 输出格式扩展（GeoPackage/Excel/DXF/OGR） | WFS/WPS 额外输出格式 | OGC（扩展） | extension |
| 数据格式扩展（NetCDF、GRIB、JP2K、MongoDB、H2/Oracle/SQLServer/DB2 存储） | 额外数据源接入 | 数据存储（扩展） | extension |
| INSPIRE 扩展 | 欧盟 INSPIRE 合规元数据/下载 | OGC（扩展） | extension |
| OAuth2 OpenID Connect / authkey / CAS | 单点登录与密钥鉴权 | 安全（扩展） | extension |
| GeoFence（插件/内嵌/WPS 集成） | 细粒度地理访问控制 | 安全（扩展） | defer |
| Control Flow | 请求限流与队列控制 | 运维（扩展） | defer |
| MapML / WMTS Multidimensional / GWC S3 BlobStore | 新格式输出/多维瓦片/云端瓦片存储 | 扩展 | defer |

### 4) 与现有桥的差距
现有桥 6 个工具全为只读目录面（列 workspace、列图层、图层信息、capabilities 摘要）：**未调用过任何一条 OGC 服务操作、未用过一个 REST 写端点**；对手册核心 5 类服务＋REST 全配置面＋40 余扩展，桥只摸到「看目录」一层。

### 5) 对平台升级的头号价值
GeoServer 是平台现成的**发布层**：数据目录（B 阶段）里的 Collection 一旦经 REST 发布成图层，WMS/WFS/OGC API 就把平台从「本地编排」抬到「对外供数」；它与 PostGIS 是官方最经典的搭配（PostGIS 存储＋GeoServer 发布），平台服务端对象模型（workspace/store/layer/style）可以直接借它的对象分工落地。

---

## 3. istSOS

### 1) 文档入口与版本口径
- 官方站 https://istsos.org （2026-11-02 实查，现行主线为 **istSOS4**：OGC SensorThings API 1.1 完整实现，Python 编写，GPL；自带 **Traveltime 扩展**做数据版本与时间旅行，支撑科研可复现——项目在 EGU26 摘要中亦以此为卖点 https://meetingorganizer.copernicus.org/EGU26/EGU26-9152.html?pdf ）。
- 遗留线 istSOS2 口径引 OSGeo 官方 OSGeo-Live 概述 http://live.osgeo.org/archive/11.0/ja/overview/istsos_overview.html ：严格实现 SOS 1.0.0（Basic＋Transactional 剖面，通过 OGC CITE 测试）、完整 RESTful API、Web 管理界面。
- 口径衔接：与鱼鱼 GSoC 目标里 istSOS 社区线一致（SensorThings 实体模型是其每日一课的主线）；现有桥按 SensorThings 读面实现，与 istSOS4 同代。

### 2) 功能域总览
STA 传感核心：8 实体（Thing、Location、HistoricalLocation、Datastream、Sensor、ObservedProperty、Observation、FeatureOfInterest）＋OData 查询面（$filter/$expand/$select/$orderby/$top/$skip/$count＋导航属性）＋CRUD 写入＋（标准面）MQTT 订阅；istSOS4 扩展：版本化与 Traveltime；遗留 istSOS2：SOS 1.0 操作面＋REST 管理 API＋数据质量处理。

### 3) 功能清单（调用入口：STA REST，路径形如 /v1.1/Things）
| 官方名 | 作用 | 调用入口 | 平台判断 |
|---|---|---|---|
| 服务根（Landing/Entity Sets 索引） | 列出全部实体集入口 | STA REST GET /v1.1 | core |
| Things 读取 | 传感对象（设备/平台）清单与详情 | STA REST GET | core |
| Locations 读取 | 对象的空间位置（几何） | STA REST GET | extension |
| HistoricalLocations 读取 | 对象位置历史 | STA REST GET | extension |
| Datastreams 读取 | 数据流（对象×传感器×观测属性）清单 | STA REST GET | core |
| Sensors 读取 | 传感器元数据 | STA REST GET | extension |
| ObservedProperties 读取 | 观测属性（量）定义 | STA REST GET | extension |
| Observations 读取 | 观测值与现象时间序列 | STA REST GET | core |
| FeaturesOfInterest 读取 | 被观测的空间要素 | STA REST GET | extension |
| $filter（含空间/时间谓词） | OData 过滤下推 | STA 查询选项 | core |
| $top / $skip / $count | 分页与计数 | STA 查询选项 | core |
| $expand | 关联实体展开（多级导航） | STA 查询选项 | extension |
| $select / $orderby | 字段裁剪与排序 | STA 查询选项 | extension |
| 创建实体（POST，含深插入） | 新建 Thing/Datastream/Observation 等 | STA REST POST | extension |
| 更新实体（PATCH） | 部分更新 | STA REST PATCH | extension |
| 删除实体（DELETE） | 删除实体 | STA REST DELETE | extension |
| 批量请求（Batch Requests） | 多操作打包（STA 扩展面） | STA REST | defer |
| MQTT 订阅 | 实时观测推送订阅（STA 标准面；istSOS4 落地以 REST 为主） | MQTT | defer |
| Traveltime 扩展（istSOS4） | 观测数据版本化/时间旅行：按历史状态引用、查询与抽取 | istSOS4 扩展 API | extension |
| 数据版本审计与持久 URL（istSOS4） | 给某一时刻的数据集状态发持久引用 | istSOS4 扩展 API | extension |
| SOS GetCapabilities / DescribeSensor / GetObservation（istSOS2） | SOS 1.0 核心操作面 | OGC SOS（遗留） | defer |
| SOS RegisterSensor / InsertObservation（istSOS2） | SOS 1.0 事务剖面写入 | OGC SOS（遗留） | defer |
| REST 管理 API（istSOS2） | 服务/程序/观测属性等的管理与数据维护 | REST（遗留） | defer |
| CSV 导入与数据编辑/质量计算（istSOS2） | csv2istsos 导入、管理端数据编辑与质量处理 | 脚本＋Web 管理端（遗留） | defer |

### 4) 与现有桥的差距
现有桥 6 个工具只读覆盖 8 实体中的 3 类（Things、Datastreams、Observations）＋GeoJSON 导出：**实体读覆盖 3/8，$filter 等查询选项无下推证据，写面（POST/PATCH/DELETE）为零**，Traveltime 与版本引用未触及。

### 5) 对平台升级的头号价值
istSOS 是平台唯一的**时序观测域**：它把「传感器/监测数据」这一整类异构数据收敛成一套标准实体模型，正好补平台数据目录缺的观测型 Collection；Traveltime 的版本化引用与鱼鱼的科研可复现纪律同构，是平台对外讲「可审计数据」时现成的差异化能力。

---

# A 组（桌面长尾，域级普查）

## 4. MapGIS（中地数码）

### 1) 文档入口与版本口径
- 官方站产品/开发页（mapgis.com，2026-11-02 实查，当前口径 MapGIS 10.7）：IGServer 产品页 https://www.mapgis.com/index.php?a=shows&catid=7&id=133 ；开发平台口径（桌面组件 MapGIS Objects SDK、桌面插件 MapGIS Desktop SDK、MapGIS Client for JavaScript / 3DClient for WebGL、MapGIS Mobile SDK）见 mapgis.com 开发平台介绍；IGServer 白皮书（司马云开发者社区）http://www.smaryun.com/dev/down/1193_dc2ce7e7f5d72d17a34ea195f5437067 。
- 版本口径：MapGIS 10（桌面端为 MapGIS Desktop「九州」），二次开发分 C++、.NET、Java、Python 多语言资源（Objects SDK 官方简介口径）。

### 2) 功能域总览（按官方产品组织）
全空间数据存储与管理（文件/数据库型地理数据）→ 数据显示与编辑 → 空间查询与分析 → 二三维一体化制图输出 → 三维（地形/模型/M3D 交换格式）→ 服务端 IGServer（服务发布/聚合/管理、二三维服务、分布式裁图与并行渲染）→ 二次开发体系（Objects SDK / Desktop 插件 SDK / WebClient / Mobile SDK）。

### 3) 代表性功能与自动化入口（平台判断＝与统一动词面的映射关系）
| 功能（官方名/域） | 作用 | 自动化入口 | 平台判断 |
|---|---|---|---|
| 数据存储与管理 | 全空间数据存储、管理（文件地理数据库等） | Objects SDK 数据管理类 | core |
| 数据显示与地图浏览 | 二三维一体化显示、图层管理 | Objects SDK / Desktop 插件 | core |
| 数据编辑 | 矢量/属性编辑与拓扑维护 | Objects SDK 编辑类 | extension |
| 空间查询 | 属性/空间条件查询 | Objects SDK 查询类 | core |
| 空间分析 | 叠加、缓冲、统计等分析 | Objects SDK 分析类 | extension |
| 制图输出 | 专题制图与打印输出 | Objects SDK 制图类 | extension |
| 三维与 M3D | 三维数据组织、流式传输与分析渲染（Model 3D Data & SDK） | M3D SDK | defer |
| IGServer 地图/瓦片服务发布 | 发布 MapGIS 二三维地图服务、瓦片服务 | IGServer（服务端） | extension |
| IGServer OGC 服务 | 发布 WMS、WFS、WMTS、CSW 等 OGC 服务 | IGServer（服务端） | extension |
| IGServer 服务聚合 | 聚合第三方/异构平台服务为 MapGIS 标准服务 | IGServer（服务端） | extension |
| IGServer 自定义服务托管 | 自定义服务注册、托管、发现 | IGServer（服务端） | defer |
| WebClient for JavaScript | Web 端地图应用开发（集成 OL/Leaflet/MapboxGL/Cesium） | JS API | defer |

### 4) 与现有桥的差距
现有桥仅 3 个工具（ping、discover、环境探针），**功能动词为 0**：桌面全功能面（数据/编辑/分析/制图）与 IGServer 服务面均未接通，是 A 组里唯一连「工程浏览层」都还没建起来的包。

### 5) 对平台升级的头号价值
MapGIS 是平台国产桌面阵营的缺口位：其余国产家（SuperMap）已有校准级桥，MapGIS 补上后平台的「国产 GIS 全覆盖」叙事才成立；且 IGServer 的 OGC 发布＋异构服务聚合能力，可与 GeoServer 形成国产服务端备选。

---

## 5. ENVI（NV5 Geospatial）

### 1) 文档入口与版本口径
- 官方 Docs Center（nv5geospatialsoftware.com，2026-11-02 实查，ENVI 6.3 口径）：ENVITasks 总页 https://www.nv5geospatialsoftware.com/docs/envitasksmainpage.html ；按类别任务全表 https://www.nv5geospatialsoftware.com/docs/envitasklist.html ；ENVITask 函数页 https://www.nv5geospatialsoftware.com/docs/envitask.html ；深度学习任务表（Deep Learning 4.0）https://www.nv5geospatialsoftware.com/docs/DLENVITaskList.html 。
- 自动化模型（官方口径）：一切处理皆为 **ENVITask**——`ENVITask('任务名')` 取任务、设参数、Execute；任务目录可由 QueryTaskCatalog/QueryTask 在运行时发现与自描述；ENVI Modeler 可编排任务流；任务亦可经 GSF（Geospatial Services Framework）服务端点远程调用。

### 2) 功能域总览（按官方任务类别组织，共 36 类）
大气校正、变化检测、分类（含规则/光谱类分类器族）、作物科学、ENVI Catalog（影像目录）、滤波（自适应/卷积/形态学）、特征提取、地理参考与格网、影像配准、掩膜、镶嵌、点云、预处理（辐射定标等）、雷达、栅格运算、ROI 与矢量、光谱工具、时空分析、拉伸、子集/分片、目标分析、地形、纹理、变换（PCA/MNF/ICA）、植被分析、深度学习（独立模块）等。

### 3) 代表性功能与自动化入口
| 功能（官方名/域） | 作用 | 自动化入口 | 平台判断 |
|---|---|---|---|
| QueryTaskCatalog / QueryTask | 运行时发现任务目录与单任务参数自描述 | ENVITask | core |
| RunTask | 以任务名＋参数字典统一执行任意任务 | ENVITask | core |
| RadiometricCalibration | 辐射定标 | ENVITask | extension |
| FLAASH / QUAC | 大气校正（物理模型/快速） | ENVITask | extension |
| RPCOrthorectification（族） | RPC 正射校正（含 DSM/参考影像变体） | ENVITask | extension |
| ImageToImageRegistration / GenerateTiePointsBy* | 影像配准与连接点生成 | ENVITask | extension |
| MaximumLikelihoodClassification / ISODATAClassification / SpectralAngleMapperClassification 等 | 监督/非监督/光谱分类器族 | ENVITask | extension |
| ClassificationToShapefile / CalculateConfusionMatrixFromRaster | 分类后处理与精度评估（混淆矩阵） | ENVITask | extension |
| ThematicChange / SAMImageDifference / ImageBandDifference | 变化检测族 | ENVITask | extension |
| SpectralIndex / SpectralIndices / QuerySpectralIndices | 光谱指数（如植被/水体指数）计算与查询 | ENVITask | extension |
| LinearSpectralUnmixing / MatchedFilter / RXAnomalyDetection | 光谱解混、目标/异常探测 | ENVITask | extension |
| GramSchmidtPanSharpening / NNDiffusePanSharpening / PCPanSharpening | 全色锐化融合 | ENVITask | extension |
| BuildMosaicRaster | 影像镶嵌 | ENVITask | extension |
| SubsetRaster / DiceRasterBy* / CreateSubrectsFrom* | 空间/波段子集与分片 | ENVITask | core |
| GeneratePointCloudsByDenseImageMatching / PointCloudFeatureExtraction | 密集匹配点云与点云特征提取 | ENVITask | extension |
| TopographicModeling / TopographicFeatures | 地形建模与地形特征 | ENVITask | extension |
| BuildTemporalCube / BuildRasterSeries | 时空立方与影像序列 | ENVITask | extension |
| DeepLearningPixelClassification / TrainDeepLearning*Model（深度学习模块） | 深度学习像素/目标分类与训练 | ENVITask（DL 模块） | extension |
| ExportCatalogToSTAC / QueryCatalog / PopulateCatalog | 影像目录管理与 STAC 导出 | ENVITask | extension |
| RegisterRasterWithGeoServer / RegisterVectorWithGeoServer | 处理结果一键注册到 GeoServer | ENVITask | extension |
| ExportRasterToTIFF / ExportRasterToJPEG2000 等 | 栅格多格式导出族 | ENVITask | extension |

### 4) 与现有桥的差距
现有桥 7 个工具已实现「列任务/描述任务/运行任务」的通用三件套，**机制上可达官方 300+ 任务**，但已逐个验证过的具体任务为 0（仅协议自检）；缺口不在动词面，而在任务级校准与参数样例。

### 5) 对平台升级的头号价值
ENVI 是平台遥感处理深度的天花板：它的任务目录自带「发现—自描述—执行」三段，正是平台统一动词面想要的形状，桥的通用运行器一旦完成几个代表任务的校准，平台的影像预处理/分类/变化检测能力即整域点亮。

---

## 6. GeoScene（易智瑞）

### 1) 文档入口与版本口径
- 官方站（geoscene.cn，2026-11-02 实查）：GeoScene Pro 产品页 https://edutrial.geoscene.cn/geoscene/trial/GeoScenePro.html ；影像解决方案 https://www.geoscene.cn/solution-88.html ；平台介绍（1800+ 地理处理工具口径）https://www.geoscene.cn/information-93.html ；5.1 新特性文（同站）。
- 定位口径（官方）：与 Esri 知识产权转移协议引进吸收的同源平台，GeoScene Pro 为其专业桌面端；自动化面与 ArcGIS Pro 同构——地理处理工具箱＋内置 Python 环境（arcpy）＋Pro SDK for .NET（此三项的同构关系为业界公开事实，官方产品页未逐项展开，标为二级依据）。

### 2) 功能域总览（按官方产品组织）
数据管理与编辑 → 高级制图可视化 → 二三维融合（2D/3D 同步显示与编辑、Multipatch）→ 高级分析（位置理解/空间关系/路径/模式检测/预测）→ 影像处理（镶嵌数据集、150+ 栅格函数、机器/深度学习、OrthoMapping 正射生产）→ 协同共享与服务发布（要素/地图/分析/3D 服务、Web Layer/WebMap/WebScene）→ 扩展模块（3D、地统计、空间分析、网络分析、工作流、数据质检、数据互操作）。

### 3) 代表性功能与自动化入口
| 功能（官方名/域） | 作用 | 自动化入口 | 平台判断 |
|---|---|---|---|
| 工程/地图/图层/布局管理 | 工程内容浏览与组织（与现有桥 13 工具同面） | Pro 应用内桥 / arcpy.mp | core |
| 地理处理工具箱（1800+ 工具） | 全域空间分析与数据处理工具集 | arcpy 地理处理 / 工具箱 | extension |
| 发布要素/地图/分析服务 | 桌面内容发布为 Web 服务 | Pro 共享面 / Enterprise REST | extension |
| 发布 Web Layer / WebMap / WebScene | 与 Portal/Online 协同共享 | Pro 共享面 | extension |
| 空间分析扩展 | 表面/插值/密度/距离等分析工具集 | arcpy.sa | extension |
| 网络分析扩展 | 路径、服务区、最近设施 | arcpy.na | extension |
| 3D 扩展与 Multipatch 编辑 | 三维数据编辑与 3D 分析 | arcpy / Pro 3D 面 | extension |
| 地统计扩展 | 克里金等空间插值与建模 | arcpy.ga | defer |
| 影像：镶嵌数据集管理 | 海量多源影像组织与共享 | arcpy.md / 数据管理工具 | extension |
| 影像：栅格函数（150+）与动态处理 | On-the-fly 实时处理链 | 栅格函数模板 / arcpy.ia | extension |
| 影像：机器学习与深度学习（内置 15 种模型） | 影像分类、对象识别端到端流程 | arcpy.learn / Learn 工具集 | extension |
| OrthoMapping | 正射影像、DSM、DTM 向导式生产 | Pro Ortho Mapping 工作空间 | extension |
| 数据质检扩展 | 数据完整性、空间关系与连接性检查 | 质检工具集 | extension |
| 数据互操作扩展 | 多格式数据读写与转换 | Data Interoperability | extension |
| 知识图谱 | 图数据建模与查询（新能力） | Pro 知识图谱面 | defer |

### 4) 与现有桥的差距
现有桥 13 个工具与 ArcGIS Pro 桥同形，只覆盖工程浏览/视图层：**1800+ 地理处理工具的运行入口为零、服务发布面为零**；且兼容性待实机核验、未实机校准（合集自述口径）。

### 5) 对平台升级的头号价值
GeoScene 是平台的「国产 ArcGIS 等价面」：与 ArcGIS Pro 桥共享动词映射的成本最低，却能独立支撑国产化交付场景；其服务端发布面（要素/分析服务）又能让平台在国产栈里走完「桌面处理→服务发布」闭环。

---

## 7. Global Mapper（Blue Marble Geographics）

### 1) 文档入口与版本口径
- 官方源（bluemarblegeo.com，2026-11-02 实查）：Python 脚本说明 https://www.bluemarblegeo.com/python-scripting-in-global-mapper-pro/ ；Script Editor/脚本语言说明 https://www.bluemarblegeo.com/blog/global-mapper-pros-script-editor-with-syntax-coloring/ ；SDK v25 说明 https://www.bluemarblegeo.com/blog/top-new-features-in-global-mapper-sdk-v25/ ；脚本命令全表在官方 Knowledge Base（Global Mapper Script 命令与参数）。
- 版本口径：桌面 v26 世代 / SDK v25；自动化三通道——原生脚本语言（.gms）、应用内 Python（`import globalmapper`）、SDK（Windows DLL，C++/C#/Python 可调）。

### 2) 功能域总览（按官方产品组织）
多格式数据接入（300+ 格式）与在线数据流 → 矢量编辑与属性处理 → 地形分析（等高线、流域、视域、挖填方、坡度坡向）→ 点云/LiDAR 处理与分类（Pro）→ 影像处理与栅格运算 → 摄影测量 Pixels-to-Points（Pro）→ GPS 实时跟踪 → 制图布局与 3D 显示 → 批量格式转换与导出 → 脚本批处理。

### 3) 代表性功能与自动化入口
| 功能（官方名/域） | 作用 | 自动化入口 | 平台判断 |
|---|---|---|---|
| IMPORT（脚本命令族） | 加载任意支持格式与在线数据源 | GMS 脚本 / SDK GM_LoadLayer、GM_LoadOnlineLayer | core |
| EXPORT（脚本命令族） | 矢量/栅格/高程/网页格式批量导出 | GMS 脚本 / SDK GM_Export* | core |
| GENERATE_CONTOURS | 由高程生成等高线 | GMS 脚本 | extension |
| GENERATE_WATERSHED | 流域/水文分析 | GMS 脚本 | extension |
| GENERATE_ELEVATION_GRID / 栅格运算 | 点/矢量生成高程格网、栅格代数 | GMS 脚本 | extension |
| 地形分析（视域、挖填方、剖面） | Viewshed、Cut-and-Fill、Path Profile | GMS 脚本 / SDK | extension |
| 点云处理与分类（Pro） | LiDAR 显示、编辑、自动分类、特征提取 | Python 模块 / SDK | extension |
| Pixels-to-Points（Pro） | 无人机影像摄影测量建模/正射/点云 | SDK 摄影测量 API | extension |
| EDIT_VECTOR / 属性运算（脚本命令族） | 矢量编辑、属性计算与空间操作 | GMS 脚本 | extension |
| 在线数据（Online Data） | 流式加载地形/影像等在线源（如 NASA DEM） | GM_LoadOnlineLayer | extension |
| UNLOAD_ALL / SAVE_WORKSPACE 等工作区命令 | 批处理工作区生命周期 | GMS 脚本 | extension |
| GPS 跟踪 | 实时 GPS 定位接入 | 桌面功能（脚本面有限） | defer |

### 4) 与现有桥的差距
现有桥 7 个工具只覆盖工作区信息/图层列表/显隐/缩放/导出图：**脚本命令面（数百条命令）与 300+ 格式的转换面均未接通**，桥连它最招牌的「格式枢纽＋地形分析」都还没碰到。

### 5) 对平台升级的头号价值
Global Mapper 是平台最便宜的**格式转换与地形分析外包工**：一个脚本入口同时买到 300+ 格式互转和成套地形分析，正好补平台数据层「异构数据先归一化再入库」的预处理环节，且脚本文件可审计、可复现，符合平台的证据纪律。

---

## 8. FME（Safe Software）

### 1) 文档入口与版本口径
- 官方文档（docs.safe.com，2026-11-02 实查）：Transformer 总表 https://docs.safe.com/fme/html/FME-Form-Documentation/FME-Transformers/transformer-index.htm ；《FME Transformer Reference Guide》2026.2/2026.3 https://docs.safe.com/fme/2026.3/html/FME-Form-Documentation/FME-Transformers/FME-Transformer-Reference-Guide.pdf ；FME Flow REST API 口径引 Safe 官方支持文（V3 已于 Flow 2025.1 弃用、2026.0 移除，现行 V4，端点文档在实例的 /fmeapiv4/docs）https://support.safe.com/s/article/Tips-for-Working-With-the-FME-Server-REST-API-in-FME-Workbench 。
- 版本口径：FME Form（桌面，原 Workbench）2026 世代，转换器 500+、读写格式 350+（厂商文档口径）；FME Flow（服务端）提供作业、自动化与数据服务。

### 2) 功能域总览（按官方 Transformer 类别组织）
属性处理 → 计算器（表达式/统计）→ 制图 → 坐标系 → 数据质量 → 数据库与连接（FeatureReader/Writer、数据库连接器族）→ 过滤与连接 → 格式专属 → 几何处理 → 集成（Web/云连接器族）→ 点云 → 栅格 → 空间分析 → 字符串 → Web → 工作流控制；服务端：Flow 作业提交/调度/Automations/通知/数据流服务。

### 3) 代表性功能与自动化入口
| 功能（官方名/域） | 作用 | 自动化入口 | 平台判断 |
|---|---|---|---|
| 格式读写（Reader/Writer 体系） | 350+ 格式的读、写与互转 | FME workspace / fme 命令行 | core |
| FeatureReader / FeatureWriter | 工作区内任意格式读写节点 | Transformer | core |
| AttributeManager（属性族） | 属性增删改名、条件赋值、表达式 | Transformer | extension |
| FeatureJoiner / FeatureMerger | 按键连接/合并要素属性与几何 | Transformer | extension |
| SpatialFilter / SpatialRelator（空间分析族） | 空间过滤与关系判定 | Transformer | extension |
| InlineQuerier | 对要素流跑 SQL 查询 | Transformer | extension |
| Tester / TestFilter（数据质量族） | 规则校验与分流（质检） | Transformer | extension |
| GeometryValidator 类质检 | 几何合法性检查与修复分流 | Transformer | extension |
| CoordinateSystemSetter / Reprojector（坐标系族） | 坐标系标注与重投影 | Transformer | extension |
| Clipper / Dissolver / Bufferer（几何族示例名按官方类别） | 裁剪、融合、缓冲等几何处理 | Transformer | extension |
| Raster* 栅格族（如 RasterCellValueRounder、ImageRasterizer） | 栅格值处理与矢量栅格化 | Transformer | extension |
| PointCloud* 点云族 | 点云分件、分类与表面建模 | Transformer | extension |
| HTTPCaller / OpenAPICaller | 工作区内调用任意 Web API | Transformer | extension |
| FMEFlowJobSubmitter | 工作区内向 Flow 提交作业 | Transformer | extension |
| Flow 作业提交与状态查询 | 服务端运行 workspace、查作业/日志 | FME Flow REST API V4 | extension |
| Flow Automations / Schedules | 事件/定时触发的自动化数据流水线 | FME Flow（Web/REST） | extension |
| Flow 数据服务（OGC/流式下载等） | workspace 发布为数据分发服务 | FME Flow | defer |

（注：几何族个别转换器名为类别内代表，逐条全表见官方 Transformer 总表。）

### 4) 与现有桥的差距
现有桥 6 个工具覆盖「列 workspace、看信息、运行、看日志尾」：**运行面已通、编排面为零**——500+ 转换器构成的 workspace 内部对平台完全黑盒，平台既不能按需拼装转换链，也不能把单条转换器沉淀为可复用动词。

### 5) 对平台升级的头号价值
FME 是平台的**数据工程重工业**：凡是「脏数据进来、标准数据出去」的脏活（格式、坐标、属性、质检一条龙），它有现成的工业级流水线；平台只需把 Flow 的作业面接成扩展动词，就能给数据目录补上「入库前加工」这一环，而不必自研 ETL。

---

## 附：全表速览（桥工具数 vs 官方能力面）

| 软件 | 现有桥工具 | 官方能力面（本次普查口径） | 桥的层级 |
|---|---|---|---|
| PostGIS | 6 | 约 530+ 函数/运算符（矢量约 330＋栅格约 150＋拓扑/SFCGAL/TIGER 约 50） | 只读元数据 |
| GeoServer | 6 | 核心 5 类 OGC 服务＋OGC API＋REST 全配置面＋40+ 扩展 | 只读目录 |
| istSOS | 6 | STA 8 实体 CRUD＋OData 查询面＋Traveltime | 只读 3/8 实体 |
| MapGIS | 3 | 桌面全功能＋Objects SDK＋IGServer 服务面 | 仅探针 |
| ENVI | 7 | 36 类、300+ ENVITask＋深度学习模块 | 通用运行器（未校准任务） |
| GeoScene | 13 | 1800+ 地理处理工具＋发布面 | 工程浏览层 |
| Global Mapper | 7 | 数百脚本命令＋300+ 格式＋SDK | 工作区浏览层 |
| FME | 6 | 500+ 转换器＋350+ 格式＋Flow 服务面 | 运行面（黑盒） |

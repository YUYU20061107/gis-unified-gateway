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

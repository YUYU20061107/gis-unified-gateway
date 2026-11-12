# ArcGIS Pro 栅格/表面分析四箱工具普查（raster-surface）

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

# ArcGIS Pro 分析服务类工具箱普查（analysis-services）

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

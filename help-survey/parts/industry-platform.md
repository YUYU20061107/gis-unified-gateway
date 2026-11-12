# ArcGIS Pro 行业与平台类工具箱普查（industry-platform）

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

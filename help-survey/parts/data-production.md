# 数据生产与质量类工具箱普查（ArcGIS Pro 3.4 工具参考）

> 范围：Editing、Geocoding、Linear Referencing、Location Referencing、Data Interoperability、Data Reviewer、Multidimension 七个工具箱的全部地理处理工具。
> 证据：一级证据仅用 Esri 官方文档（pro.arcgis.com，ArcGIS Pro 3.4 工具参考的各工具箱总览页与各 toolset 总览页，逐条抄录 Tool | Description 表）；工具构成另以同版许可页交叉核对（Geocoding）。
> 平台升级原则（鱼鱼定版）：全部升级＋不重复造轮子——平台层只做翻译与治理、不自研算法；「轮子来源」列写明每条工具可复用的官方现成实现通道。
> 平台判断口径：core＝通用能力、多家共有，宜升为平台通用能力；extension＝ArcGIS 专属数据模型／检查框架／FME 引擎绑定，宜以扩展包形式接入；defer＝依赖地址定位器建设、交互质检会话、第三方引擎许可等前置条件，暂缓。
> 合计：111 条工具，其中 core 44 条、extension 56 条、defer 11 条。

## Editing toolbox（arcpy.edit）

工具集数：2（工具箱顶层＋Conflation）；工具总数：18；前提：官方总览未标注扩展许可，属 ArcGIS Pro 核心工具箱；官方定位：对要素类的全部（或选中）要素做批量编辑，处理数字化精度不足、无捕捉环境造成的面边界不闭合、线过冲／欠冲，以及顶点密度、多源融合等数据质量问题。

### Editing toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Densify | 沿线或面要素添加顶点，并把曲线段（贝塞尔、圆弧、椭圆弧）替换为线段 | `arcpy.edit.Densify` | ArcPy GP（官方实现，桥直调） | core — 顶点加密属批量编辑基础，多家共有 |
| Erase Point | 按操作类型删除落在移除要素内部或外部的输入点 | `arcpy.edit.ErasePoint` | ArcPy GP（官方实现，桥直调） | core — 点批量清理通用能力 |
| Extend Line | 把线段延长至指定距离内首个相交要素，用于清理无捕捉数字化造成的拓扑错误 | `arcpy.edit.ExtendLine` | ArcPy GP（官方实现，桥直调） | core — 线过冲／欠冲清理通用能力 |
| Flip Line | 反转线要素的起止方向 | `arcpy.edit.FlipLine` | ArcPy GP（官方实现，桥直调） | core — 基础几何编辑，多家共有 |
| Generalize | 按最大偏移容差简化输入要素，输出只保留原始顶点子集 | `arcpy.edit.Generalize` | ArcPy GP（官方实现，桥直调） | core — 几何简化通用能力 |
| Simplify By Straight Lines And Circular Arcs | 以更少的线段／边替换连续线段，并可由连续线段生成圆弧 | `arcpy.edit.SimplifyByStraightLinesAndCircularArcs` | ArcPy GP（官方实现，桥直调） | core — 通用简化，圆弧拟合不改变其通用性 |
| Snap | 把点或顶点移动到与其他要素的顶点、边或端点精确重合 | `arcpy.edit.Snap` | ArcPy GP（官方实现，桥直调） | core — 捕捉对齐属编辑基础能力 |
| Trim Line | 去除线越过交点后指定距离内的悬挂部分（dangles） | `arcpy.edit.TrimLine` | ArcPy GP（官方实现，桥直调） | core — 悬挂线清理通用能力 |
| Update COGO | 更新启用 COGO 的线要素的 COGO 属性，使其与线形状几何一致 | `arcpy.edit.UpdateCOGO` | ArcPy GP（官方实现，桥直调） | extension — COGO 是 ArcGIS 测量／宗地专属属性体系 |

### Conflation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Align Features | 在搜索距离内找出输入要素与目标要素不一致的部分并将其对齐到目标 | `arcpy.edit.AlignFeatures` | ArcPy GP（官方实现，桥直调） | core — 多源数据对齐通用需求 |
| Calculate Transformation Errors | 按已知控制点间链接坐标计算残差与均方根误差（RMSE），供空间变换使用 | `arcpy.edit.CalculateTransformationErrors` | ArcPy GP（官方实现，桥直调） | core — 变换精度评估通用能力 |
| Edgematch Features | 按接边匹配链接对输入线做空间调整，使其与相邻数据集的线连接 | `arcpy.edit.EdgematchFeatures` | ArcPy GP（官方实现，桥直调） | core — 接边匹配为通用融合工序 |
| Generate Edgematch Links | 在源数据与相邻数据接边处找出匹配但未连接的线，生成接边匹配链接 | `arcpy.edit.GenerateEdgematchLinks` | ArcPy GP（官方实现，桥直调） | core — 融合链接生成通用能力 |
| Generate Rubbersheet Links | 找出源线与目标线的空间匹配处，生成用于橡皮拉伸的链接线 | `arcpy.edit.GenerateRubbersheetLinks` | ArcPy GP（官方实现，桥直调） | core — 橡皮拉伸链接生成通用能力 |
| Rubbersheet Features | 按橡皮拉伸链接对输入要素做空间调整，使其与目标要素更好对齐 | `arcpy.edit.RubbersheetFeatures` | ArcPy GP（官方实现，桥直调） | core — 橡皮拉伸调整多家共有 |
| Split Line By Match | 按匹配关系分割要素，获得更好的对应线分段 | `arcpy.edit.SplitLineByMatch` | ArcPy GP（官方实现，桥直调） | extension — 依赖 Esri 融合匹配关系模型 |
| Transfer Attributes | 找出源线与目标线的空间匹配处，把指定属性从源要素传到匹配的目标要素 | `arcpy.edit.TransferAttributes` | ArcPy GP（官方实现，桥直调） | core — 属性转移为通用融合工序 |
| Transform Features | 按已知对应控制点间的变换链接，对输入要素坐标做缩放、平移与旋转 | `arcpy.edit.TransformFeatures` | ArcPy GP（官方实现，桥直调） | core — 坐标变换通用能力 |

## Geocoding toolbox（arcpy.geocoding）

工具集数：3（工具箱顶层＋Data Preparation＋Portal）；工具总数：15；前提：3.4 许可页显示顶层与 Data Preparation 工具在 Basic／Standard／Advanced 均可用；Portal 工具要求 ArcGIS Enterprise 账号具备 Perform Analysis 权限；使用 ArcGIS World Geocoding Service 时可能消耗 credits；官方定位：地理编码是把地址中的描述性位置元素与参考资料比对、赋予其位置（通常为坐标值）的过程，本箱覆盖定位器创建维护、地址地理编码与由点取址等任务。注：以工具箱工具为准（arcpy.geocoding 模块另有函数级接口，不计入本表）。

### Geocoding toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add Polygon Fields To Locator | 把面图层的自定义输出字段添加给本地存储的已有定位器 | `arcpy.geocoding.AddPolygonFieldsToLocator` | ArcPy GP（官方实现，桥直调） | defer — 依赖已建成的定位器资产 |
| Clip Locator | 按兴趣区或范围裁剪定位器，生成范围与体积更小的定位器 | `arcpy.geocoding.ClipLocator` | ArcPy GP（官方实现，桥直调） | defer — 属定位器建设／维护环节 |
| Create Composite Address Locator | 创建由两个以上单独定位器组成的复合定位器，可用多定位器匹配地址与地点 | `arcpy.geocoding.CreateCompositeAddressLocator` | ArcPy GP（官方实现，桥直调） | defer — 依赖定位器体系建设 |
| Create Feature Locator | 用单字段存唯一名称／值的参考数据创建定位器，可检索水表、地名、信号塔、编码串等 | `arcpy.geocoding.CreateFeatureLocator` | ArcPy GP（官方实现，桥直调） | defer — 属定位器建设环节 |
| Create Locator | 创建可查地址／地点位置、把地址表转为点要素、或由点识别地址的定位器 | `arcpy.geocoding.CreateLocator` | ArcPy GP（官方实现，桥直调） | defer — 平台地理编码的地基，但须先建定位器 |
| Delete Polygon Fields From Locator | 删除已有定位器上由面图层附加的全部自定义输出字段 | `arcpy.geocoding.DeletePolygonFieldsFromLocator` | ArcPy GP（官方实现，桥直调） | defer — 依赖已建成的定位器资产 |
| Geocode Addresses | 把地址表与定位器或复合定位器匹配，每条记录的结果存为新的点要素类 | `arcpy.geocoding.GeocodeAddresses` | ArcPy GP（桥直调）；ArcGIS REST 服务等价接口（World Geocoding Service） | core — 地理编码为通用能力，多家共有 |
| Rebuild Address Locator | 重建地址定位器，使其纳入参考数据的当前几何与属性变更 | `arcpy.geocoding.RebuildAddressLocator` | ArcPy GP（官方实现，桥直调） | defer — 属定位器维护环节 |
| Rematch Addresses | 对已地理编码要素类中的地址重新匹配 | `arcpy.geocoding.RematchAddresses` | ArcPy GP（官方实现，桥直调） | core — 地理编码结果再匹配属通用流程 |
| Reverse Geocode | 由点位置要素类生成地址，查找最近的地址、地点或交叉口 | `arcpy.geocoding.ReverseGeocode` | ArcPy GP（桥直调）；ArcGIS REST 服务等价接口（Geocoding 服务） | core — 逆地理编码为通用能力 |

### Data Preparation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Assign Streets To Points | 综合门牌号、街道名等地址信息与距离，为点找出最佳街道要素候选（地址信息优先于距离） | `arcpy.geocoding.AssignStreetsToPoints` | ArcPy GP（官方实现，桥直调） | defer — 为 Create Locator 建定位器做数据准备 |
| Assign Zones To Streets | 把社区、城市、都市区、邮编等行政区值赋给街道线段的左右两侧 | `arcpy.geocoding.AssignZonesToStreets` | ArcPy GP（官方实现，桥直调） | defer — 为建定位器准备街道参考数据 |
| Split Address Into Components | 把街道地址信息拆成地址组成部分，输出为带独立字段的表或要素类 | `arcpy.geocoding.SplitAddressIntoComponents` | ArcPy GP（官方实现，桥直调） | core — 地址解析／标准化为通用文本处理 |

### Portal toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Geocode File | 把本地大批量地址／地点表转换为点，输出要素类或 CSV／XLS 表，使用门户托管定位器 | `arcpy.geocoding.GeocodeFile` | ArcGIS Enterprise 门户托管工具（REST 分析服务） | defer — 依赖 Enterprise 门户与托管定位器及权限 |
| Geocode Locations From Table | 用门户托管定位器对托管表地理编码，生成含结果的托管要素图层 | `arcpy.geocoding.GeocodeLocationsFromTable` | ArcGIS Enterprise 门户托管工具（REST 分析服务） | defer — 依赖 Enterprise 门户与托管定位器及权限 |

## Linear Referencing toolbox（arcpy.lr）

工具集数：1（无 toolset 分组，工具直列于工具箱）；工具总数：7；前提：核心工具箱，Esri 官方说明核心线性参考工具含于 Basic 许可级别；官方定位：为采集公路、街道、铁路、河流、管线、给排水网络等线状要素数据的组织提供线性参考系统，用已知线要素及其沿线测量值（measure）表达位置，本箱含创建、校准与显示线性参考数据的工具。

### Linear Referencing toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Calibrate Routes | 用校准点重新计算路径的测量值 | `arcpy.lr.CalibrateRoutes` | ArcPy GP（官方实现，桥直调） | core — 线性参考基础能力 |
| Create Routes | 由已有线创建路径，同标识的输入线要素合并为一条路径 | `arcpy.lr.CreateRoutes` | ArcPy GP（官方实现，桥直调） | core — 线性参考基础能力 |
| Dissolve Route Events | 消除事件表冗余信息，或把含多个描述属性的事件表拆为单独的表 | `arcpy.lr.DissolveRouteEvents` | ArcPy GP（官方实现，桥直调） | core — 事件表整理通用能力 |
| Locate Features Along Routes | 计算输入要素（点／线／面）与路径要素的交叠，把路径与测量信息写入新事件表 | `arcpy.lr.LocateFeaturesAlongRoutes` | ArcPy GP（官方实现，桥直调） | core — 动态分段基础能力，多家共有 |
| Make Route Event Layer | 用路径与路径事件创建临时要素图层 | `arcpy.lr.MakeRouteEventLayer` | ArcPy GP（官方实现，桥直调） | core — 事件可视化基础能力 |
| Overlay Route Events | 叠加两个事件表，输出表示其并集或交集的事件表 | `arcpy.lr.OverlayRouteEvents` | ArcPy GP（官方实现，桥直调） | core — 事件叠加为线性参考基础运算 |
| Transform Route Events | 把事件的测量值从一套路径参考转换到另一套，并写入新事件表 | `arcpy.lr.TransformRouteEvents` | ArcPy GP（官方实现，桥直调） | core — 事件参考转换基础能力 |

## Location Referencing toolbox（arcpy.locref）

工具集数：6（工具箱顶层＋Configuration，及其下 LRS、LRS Event、LRS Intersection、LRS Network 四个子集）；工具总数：44；前提：需要 Location Referencing 扩展许可（Roads and Highways／Pipeline Referencing）；官方定位：提供 LRS（线性参考系统）的配置与管理核心工具。补充：该扩展另把线性参考能力以 ArcGIS Server 的 Linear Referencing Service（REST）形式提供（见 Pipeline Referencing 官方入门页），GP 之外多一条服务复用通道。

### Location Referencing toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Append Events | 把表、图层或要素类中的事件记录追加到已有 LRS 事件要素类 | `arcpy.locref.AppendEvents` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件数据模型 |
| Append Routes | 把输入折线追加到 LRS Network 中成为路径 | `arcpy.locref.AppendRoutes` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Apply Event Behaviors | 按所做的路径编辑，更新注册到输入网络的全部事件要素类的事件位置 | `arcpy.locref.ApplyEventBehaviors` | ArcPy GP（官方实现，桥直调） | extension — 事件行为规则为 LRS 专属机制 |
| Calculate Intersecting Route Measures | 生成一张表，列出每个交叉口位置处全部路径及其测量值 | `arcpy.locref.CalculateIntersectingRouteMeasures` | ArcPy GP（官方实现，桥直调） | extension — 依赖 LRS Network 与交叉口模型 |
| Calculate Route Concurrencies | 计算并报告 LRS Network 中的并发路径区段 | `arcpy.locref.CalculateRouteConcurrencies` | ArcPy GP（官方实现，桥直调） | extension — 并发路径为 LRS 专属概念 |
| Delete Routes | 从 LRS Network 删除路径及其关联数据元素 | `arcpy.locref.DeleteRoutes` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Derive Event Measures | 在已配置启用的点／线事件上填充并更新 DerivedRouteID 字段与测量值 | `arcpy.locref.DeriveEventMeasures` | ArcPy GP（官方实现，桥直调） | extension — 派生测量字段为 LRS 专属机制 |
| Generate Calibration Points | 为任意路径形状（含自闭合、自相交、分支等复杂形状）生成校准点 | `arcpy.locref.GenerateCalibrationPoints` | ArcPy GP（官方实现，桥直调） | extension — 服务于 LRS 校准模型 |
| Generate Events | 为注册到 LRS Network 的事件要素重新生成形状 | `arcpy.locref.GenerateEvents` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Generate Intersections | 生成新交叉口并更新已有交叉口 | `arcpy.locref.GenerateIntersections` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口模型 |
| Generate LRS Data Product | 变换 LRS 数据，为 LRS Network 中选定路径生成长度产品（如按县界汇总里程） | `arcpy.locref.GenerateLRSDataProduct` | ArcPy GP（官方实现，桥直调） | extension — LRS 专属数据产品 |
| Generate Routes | 为 LRS Network 中的路径要素重建形状并应用校准变更 | `arcpy.locref.GenerateRoutes` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Overlay Events | 把一个以上线／点事件图层叠加到目标网络，输出表示动态分段结果的要素类或表 | `arcpy.locref.OverlayEvents` | ArcPy GP（官方实现，桥直调） | extension — 虽为动态分段，但实现绑定 LRS Network |
| Remove Overlapping Centerlines | 移除重叠的中心线区段，使中心线几何重叠处只有一条公共中心线 | `arcpy.locref.RemoveOverlappingCenterlines` | ArcPy GP（官方实现，桥直调） | extension — 中心线为 LRS 专属概念 |
| Reverse Line Orders | 反转一条线中全部路径的线顺序 | `arcpy.locref.ReverseLineOrders` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 线／路径模型 |
| Translate Event Measures | 把点或线事件图层的测量值（m 值）从一种线性参考方法（LRM）翻译到另一种 | `arcpy.locref.TranslateEventMeasures` | ArcPy GP（官方实现，桥直调） | extension — LRM 体系为 LRS 专属 |
| Update Measures From LRS | 为 Utility Network 要素（如管道、设备、结点）或非 UN／LRS 要素类填充并更新路径 ID 与测量值 | `arcpy.locref.UpdateMeasuresFromLRS` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 与 Utility Network 模型 |

### Configuration toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Configure Address Feature Classes | 把 Address Data Management 方案的地址范围与站点地址要素类配置为可用于 LRS（配合 Roads and Highways） | `arcpy.locref.ConfigureAddressFeatureClasses` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Esri 方案模板与 LRS 模型 |
| Configure Utility Network Feature Class | 把 Utility Network 管线要素类配置为可用于 LRS | `arcpy.locref.ConfigureUtilityNetworkFeatureClass` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Utility Network 与 LRS 模型 |
| Remove LRS Entity | 从输入地理数据库工作空间移除一个 LRS 实体 | `arcpy.locref.RemoveLRSEntity` | ArcPy GP（官方实现，桥直调） | extension — LRS 实体为专属数据模型对象 |

### Configuration > LRS toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create LRS | 在指定工作空间创建 LRS 及最小模式项 | `arcpy.locref.CreateLRS` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS 信息模型 |
| Create LRS From Existing Dataset | 用已有数据集在指定工作空间创建 LRS | `arcpy.locref.CreateLRSFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS 信息模型 |
| Modify LRS | 修改指定工作空间中已有的 LRS | `arcpy.locref.ModifyLRS` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 信息模型 |

### Configuration > LRS Event toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Configure External Event With LRS | 把存储在外部系统中的事件数据与 LRS 关联 | `arcpy.locref.ConfigureExternalEventWithLRS` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Create LRS Event | 为已有 LRS Network 创建线或点事件 | `arcpy.locref.CreateLRSEvent` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件数据模型 |
| Create LRS Event From Existing Dataset | 把已有要素类注册为 LRS 事件 | `arcpy.locref.CreateLRSEventFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Disable Derived Measure Fields | 禁用存储派生网络路径 ID、路径名与测量值的字段 | `arcpy.locref.DisableDerivedMeasureFields` | ArcPy GP（官方实现，桥直调） | extension — 派生测量字段为 LRS 专属机制 |
| Disable Referent Fields | 禁用已有 LRS 事件要素类／图层的参照字段（不删列，仅从 Lrs_Metadata 表移除其信息） | `arcpy.locref.DisableReferentFields` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 元数据表结构 |
| Disable Stationing Fields | 禁用已注册 LRS 事件的桩号字段 | `arcpy.locref.DisableStationingFields` | ArcPy GP（官方实现，桥直调） | extension — 桩号字段为 LRS 专属机制 |
| Enable Derived Measure Fields | 为指定 LRS 事件要素类启用存储派生路径 ID、派生路径名与派生测量值的字段 | `arcpy.locref.EnableDerivedMeasureFields` | ArcPy GP（官方实现，桥直调） | extension — 派生测量字段为 LRS 专属机制 |
| Enable Referent Fields | 启用或修改参照字段，以便管理已注册 LRS 事件的参照信息 | `arcpy.locref.EnableReferentFields` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件注册模型 |
| Enable Stationing Fields | 启用或修改桩号字段，以便管理已注册 LRS 事件的桩号信息 | `arcpy.locref.EnableStationingFields` | ArcPy GP（官方实现，桥直调） | extension — 桩号字段为 LRS 专属机制 |
| Modify Event Behavior Rules | 修改已注册事件图层或要素类的事件行为规则 | `arcpy.locref.ModifyEventBehaviorRules` | ArcPy GP（官方实现，桥直调） | extension — 事件行为规则为 LRS 专属机制 |
| Modify LRS Event | 修改 LRS 事件的属性 | `arcpy.locref.ModifyLRSEvent` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 事件数据模型 |

### Configuration > LRS Intersection toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create LRS Intersection | 为已有 LRS Network 创建交叉口要素类 | `arcpy.locref.CreateLRSIntersection` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口模型 |
| Create LRS Intersection From Existing Dataset | 把已有交叉口要素类注册为交叉口 | `arcpy.locref.CreateLRSIntersectionFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口注册模型 |
| Modify LRS Intersection | 修改交叉口要素类的属性，如组成它的字段与相交图层的增删 | `arcpy.locref.ModifyLRSIntersection` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS 交叉口模型 |

### Configuration > LRS Network toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Configure Lookup Table | 为多字段路径 ID 中使用的一个或多个字段配置查找表 | `arcpy.locref.ConfigureLookupTable` | ArcPy GP（官方实现，桥直调） | extension — 多字段路径 ID 为 LRS 专属机制 |
| Configure Route Dominance Rules | 配置规则集，判定存在并发路径的网络中哪条为主导路径 | `arcpy.locref.ConfigureRouteDominanceRules` | ArcPy GP（官方实现，桥直调） | extension — 路径主导规则为 LRS 专属机制 |
| Create LRS Network | 在 LRS 中创建 LRS Network | `arcpy.locref.CreateLRSNetwork` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS Network 模型 |
| Create LRS Network From Existing Dataset | 用已有折线要素类创建 LRS Network | `arcpy.locref.CreateLRSNetworkFromExistingDataset` | ArcPy GP（官方实现，桥直调） | extension — 创建 ArcGIS 专属 LRS Network 模型 |
| Modify LRS Network | 修改 LRS 中的 LRS Network | `arcpy.locref.ModifyLRSNetwork` | ArcPy GP（官方实现，桥直调） | extension — 绑定 LRS Network 数据模型 |
| Modify Network Calibration Rules | 修改 LRS Network 的网络校准规则 | `arcpy.locref.ModifyNetworkCalibrationRules` | ArcPy GP（官方实现，桥直调） | extension — 网络校准规则为 LRS 专属机制 |
| Modify Route ID Padding | 修改多字段路径 ID 组成字段的填充、空值与长度属性 | `arcpy.locref.ModifyRouteIDPadding` | ArcPy GP（官方实现，桥直调） | extension — 多字段路径 ID 为 LRS 专属机制 |

## Data Interoperability toolbox（arcpy.di）

工具集数：1（无 toolset 分组，工具直列于工具箱）；工具总数：2；前提：需要 Data Interoperability 许可；官方定位：用 Safe Software 的 FME 技术转换广泛的数据格式，FME 套件是空间数据的提取、转换、加载（ETL）工具，可把空间数据格式整合进 GIS 分析并基于内置格式与转换器建模自定义格式。注：用户自建的空间 ETL 工具（由 FME Workbench 工作空间生成）不属官方工具箱工具，不计入本表。

### Data Interoperability toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Quick Export | 把一个或多个输入要素类／要素图层转换为本扩展支持的任意格式 | `arcpy.di.QuickExport` | ArcPy GP（桥直调，底层 Safe Software FME 引擎） | extension — FME 引擎绑定 |
| Quick Import | 把本扩展支持的任意格式的矢量或表格数据转换为要素类或表 | `arcpy.di.QuickImport` | ArcPy GP（桥直调，底层 Safe Software FME 引擎） | extension — FME 引擎绑定 |

## Data Reviewer toolbox（arcpy.reviewer）

工具集数：2（Data Validation＋Result Management）；工具总数：5；前提：需要 Data Reviewer 扩展许可；官方定位：Data Reviewer 扩展为 ArcGIS 加入数据质量控制框架，用批处理作业（batch job）中包含的各类检查（checks）校验数据的空间关系与完整性，并提供纠正校验所发现错误的工具；本箱工具支持创建 Reviewer 会话与执行批处理作业等数据校验工作。注：ArcMap 版工具箱中的 Geodatabase Schema Compare 在 ArcGIS Pro 版两 toolset 总览中无此工具，不计入。

### Data Validation toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Execute Reviewer Batch Job | 对工作空间运行 Reviewer 批处理作业并把结果写入 Reviewer 会话；作业含成组的检查，按条件、规则与空间关系校验数据 | `arcpy.reviewer.ExecuteReviewerBatchJob` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Reviewer 检查／批作业框架 |
| Write To Reviewer Table | 把要素类、要素图层、表或表视图写入 Reviewer 工作空间 | `arcpy.reviewer.WriteToReviewerTable` | ArcPy GP（官方实现，桥直调） | extension — 绑定 Reviewer 工作空间结构 |

### Result Management toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create Reviewer Session | 在指定工作空间中新建一个 Reviewer 会话 | `arcpy.reviewer.CreateReviewerSession` | ArcPy GP（官方实现，桥直调） | extension — 会话机制为 Reviewer 框架专属 |
| Delete Reviewer Session | 从 Reviewer 工作空间永久删除一个或多个会话及其全部相关记录 | `arcpy.reviewer.DeleteReviewerSession` | ArcPy GP（官方实现，桥直调） | extension — 会话机制为 Reviewer 框架专属 |
| Enable Data Reviewer | 为已有地理数据库添加使其成为 Reviewer 工作空间所需的数据集与表，以存储 Data Reviewer 结果 | `arcpy.reviewer.EnableDataReviewer` | ArcPy GP（官方实现，桥直调） | extension — Reviewer 工作空间为专属结构 |

## Multidimension toolbox（arcpy.md）

工具集数：2（工具箱顶层＋NetCDF）；工具总数：20；前提：官方说明本工具箱工具不需要额外扩展许可；官方定位：创建与管理 netCDF、GRIB、HDF、OPeNDAP、Esri CRF、多维镶嵌数据集与多维影像服务，可生成多维元数据、创建多维栅格／要素图层或表视图、选取多维数据集的特定切片、或生成多维栅格子集。

### Multidimension toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Build Multidimensional Info | 在镶嵌数据集中生成多维元数据，包括变量与维度信息 | `arcpy.md.BuildMultidimensionalInfo` | ArcPy GP（官方实现，桥直调） | extension — 绑定镶嵌数据集／CRF 多维模型 |
| Build Multidimensional Transpose | 转置多维栅格数据集，沿各维度切分数据以优化跨全部切片取像素值的性能 | `arcpy.md.BuildMultidimensionalTranspose` | ArcPy GP（官方实现，桥直调） | extension — CRF 存储布局优化，Esri 专属 |
| Make Multidimensional Raster Layer | 按定义的变量与维度切片多维栅格数据集或图层，创建栅格图层 | `arcpy.md.MakeMultidimensionalRasterLayer` | ArcPy GP（官方实现，桥直调） | core — 多维栅格切片为通用能力 |
| Make Multidimensional Voxel Layer | 由多维体素数据集创建体素图层 | `arcpy.md.MakeMultidimensionalVoxelLayer` | ArcPy GP（官方实现，桥直调） | extension — 体素图层为 ArcGIS 专属数据模型 |
| Make OPeNDAP Raster Layer | 由 OPeNDAP 服务器上存储的数据创建栅格图层 | `arcpy.md.MakeOPeNDAPRasterLayer` | ArcPy GP（桥直调，数据来自 OPeNDAP 开放服务协议） | core — 基于开放协议，多家共有 |
| Manage Multidimensional Raster | 通过添加或删除变量或维度来编辑多维栅格 | `arcpy.md.ManageMultidimensionalRaster` | ArcPy GP（官方实现，桥直调） | core — 多维数据结构管理通用能力 |
| Merge Multidimensional Rasters | 在空间上或跨变量与维度合并多个多维栅格数据集 | `arcpy.md.MergeMultidimensionalRasters` | ArcPy GP（官方实现，桥直调） | core — 多维栅格合并通用能力 |
| Select By Dimension | 按维度值更新 netCDF 图层显示或 netCDF 表视图 | `arcpy.md.SelectByDimension` | ArcPy GP（官方实现，桥直调） | core — 按维度选片为 netCDF 基础操作 |
| Subset Multidimensional Raster | 按定义的变量与维度切片，创建多维栅格的子集 | `arcpy.md.SubsetMultidimensionalRaster` | ArcPy GP（官方实现，桥直调） | core — 多维子集提取通用能力 |

### NetCDF toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Describe NetCDF File | 描述输入 netCDF 数据集的性质与内容，列出全部变量及其维度与属性 | `arcpy.md.DescribeNetCDFFile` | ArcPy GP（官方实现，桥直调） | core — netCDF 元数据读取基础能力 |
| Feature to NetCDF | 把点要素转换为 netCDF 文件 | `arcpy.md.FeatureToNetCDF` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础写出，多家共有 |
| Make NetCDF Feature Layer | 由 netCDF 文件创建要素图层 | `arcpy.md.MakeNetCDFFeatureLayer` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础读取 |
| Make NetCDF Raster Layer | 由 netCDF 文件创建栅格图层 | `arcpy.md.MakeNetCDFRasterLayer` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础读取 |
| Make NetCDF Table View | 由 netCDF 文件创建表视图 | `arcpy.md.MakeNetCDFTableView` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础读取 |
| NetCDF Points To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的点（离散采样几何 DSG）创建为要素类 | `arcpy.md.NetCDFPointsToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| NetCDF Profiles To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的剖面（DSG）创建为要素类 | `arcpy.md.NetCDFProfilesToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| NetCDF Time Series To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的时间序列（DSG）创建为要素类 | `arcpy.md.NetCDFTimeSeriesToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| NetCDF Trajectories To Feature Class (Discrete Sampling Geometry) | 按 CF 元数据约定把 netCDF 中的轨迹（DSG）创建为要素类 | `arcpy.md.NetCDFTrajectoriesToFeatureClass` | ArcPy GP（官方实现，桥直调） | core — 基于 CF 开放约定 |
| Raster to NetCDF | 把栅格数据集转换为 netCDF 文件 | `arcpy.md.RasterToNetCDF` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础写出，多家共有 |
| Table to NetCDF | 把表转换为 netCDF 文件 | `arcpy.md.TableToNetCDF` | ArcPy GP（官方实现，桥直调） | core — netCDF 基础写出，多家共有 |

## 附：Esri 官方智能体／MCP 入口（官方文档发现）

七个工具箱的 3.4 工具参考页内未发现各自的智能体／MCP 入口；但在 Esri 官方开发者文档中发现平台级官方 MCP 入口一处，与本文件的 Geocoding 箱直接相关：

- **MCP for ArcGIS Location Services（beta）**——Esri 托管的 Model Context Protocol（MCP）服务器，使应用与 AI 智能体可经标准化 MCP 工具访问 ArcGIS Location Services（含 ArcGIS Geocoding service、Routing、Elevation、Places、底图与静态地图等），无需直接调用 ArcGIS REST API；需 ArcGIS Location Platform 或 ArcGIS Online 账号。官方文档：https://developers.arcgis.com/ai/mcp-arcgis-location-services/ ；官方发布说明（Esri 博客，2026-06-29 起 beta）：https://www.esri.com/arcgis-blog/products/platform/developers/mcp-support-beta-and-arcgis-static-maps-service-in-arcgis-location-platform-release
- 平台含义：地理编码类能力除 ArcPy GP 与 REST 两条复用通道外，新增第三条官方通道——Esri 托管 MCP；平台层可直接把该 MCP 作为 Geocoding 能力的上游轮子接入，只做翻译与治理。

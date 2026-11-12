## Data Management toolbox（arcpy.management）

共 42 个工具集（含子集：顶层 35 个 + 子集 7 个）与 387 个工具。官方定位：该工具箱用于开发、管理与维护要素类、数据集、图层与栅格数据结构（The Data Management toolbox contains tools that are used to develop, manage, and maintain feature classes, datasets, layers, and raster data structures）。来源：ArcGIS Pro 工具参考（pro.arcgis.com）；注：搜索索引实际返回并逐页抓取的是 3.1 文档站，3.4 站未被索引返回，此版本差已在回报中注明，工具集结构以总览页为准。

> 轮子来源口径（主代理总装时补）：本箱 387 条的官方实现均为 ArcPy 地理处理（`arcpy.management.*`），已逐条标入表中。补充：当数据托管在 ArcGIS Online/Enterprise 时，其中一部分数据操作（要素增删改、查询）在服务侧另有 REST（Feature Service applyEdits/query）与 arcgis Python API 通道，属同一官方实现的服务侧等价入口，平台可按数据位置二选一，不逐条重复标注。

### 3D Objects toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add 3D Formats To Multipatch | 将多面体要素类关联一种或多种 3D 模型格式，转换为 3D 对象要素图层 | arcpy.management.Add3DFormatsToMultipatch | extension：3D 对象图层为 ArcGIS 专属存储与纹理优化机制 | ArcPy GP（官方实现） |
| Remove 3D Formats From Multipatch | 移除 3D 对象要素图层引用的 3D 格式 | arcpy.management.Remove3DFormatsFromMultipatch | extension：同上，ArcGIS 专属 | ArcPy GP（官方实现） |

### Archiving toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Disable Archiving | 对地理数据库要素类、表或要素数据集禁用归档 | arcpy.management.DisableArchiving | extension：地理数据库归档为 ArcGIS 专属机制 | ArcPy GP（官方实现） |
| Enable Archiving | 对表、要素类或要素数据集启用归档以记录历史变更 | arcpy.management.EnableArchiving | extension：同上 | ArcPy GP（官方实现） |
| Trim Archive History | 删除非版本化归档数据集中已退役的归档记录 | arcpy.management.TrimArchiveHistory | defer：破坏性删除历史记录，需谨慎与管理员确认 | ArcPy GP（官方实现） |

### Attachments toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Attachments | 按匹配表把文件附件添加到地理数据库要素类或表的记录 | arcpy.management.AddAttachments | extension：地理数据库附件表与关系为 ArcGIS 专属实现 | ArcPy GP（官方实现） |
| Disable Attachments | 禁用附件并删除附件关系类与附件表 | arcpy.management.DisableAttachments | extension：同上，且删除附件结构 | ArcPy GP（官方实现） |
| Downgrade Attachments | 降级要素类或表的附件功能版本 | arcpy.management.DowngradeAttachments | extension：ArcGIS 版本兼容专属操作 | ArcPy GP（官方实现） |
| Enable Attachments | 启用附件并创建附件关系类与附件表 | arcpy.management.EnableAttachments | extension：同上 | ArcPy GP（官方实现） |
| Generate Attachment Match Table | 创建供添加/移除附件工具使用的匹配表 | arcpy.management.GenerateAttachmentMatchTable | extension：为 ArcGIS 附件工作流配套 | ArcPy GP（官方实现） |
| Remove Attachments | 移除地理数据库要素类或表记录的附件 | arcpy.management.RemoveAttachments | extension：同上 | ArcPy GP（官方实现） |
| Upgrade Attachments | 升级数据的附件功能 | arcpy.management.UpgradeAttachments | extension：ArcGIS 版本兼容专属操作 | ArcPy GP（官方实现） |

### Attribute Rules toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Attribute Rule | 向数据集添加一条属性规则 | arcpy.management.AddAttributeRule | extension：地理数据库属性规则（Arcade）为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Alter Attribute Rule | 修改属性规则的属性 | arcpy.management.AlterAttributeRule | extension：同上 | ArcPy GP（官方实现） |
| Delete Attribute Rule | 从数据集删除一条或多条属性规则 | arcpy.management.DeleteAttributeRule | extension：同上 | ArcPy GP（官方实现） |
| Disable Attribute Rules | 禁用数据集的一条或多条属性规则 | arcpy.management.DisableAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Enable Attribute Rules | 启用数据集中的一条或多条属性规则 | arcpy.management.EnableAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Evaluate Rules | 评估地理数据库规则与功能 | arcpy.management.EvaluateRules | extension：同上 | ArcPy GP（官方实现） |
| Export Attribute Rules | 将属性规则导出为 CSV 文件 | arcpy.management.ExportAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Import Attribute Rules | 从 CSV 文件向数据集导入属性规则 | arcpy.management.ImportAttributeRules | extension：同上 | ArcPy GP（官方实现） |
| Reorder Attribute Rule | 调整属性规则的求值顺序 | arcpy.management.ReorderAttributeRule | extension：同上 | ArcPy GP（官方实现） |

### Catalog Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Items To Catalog Dataset | 将工作空间条目与图层（数据集、栅格、要素、镶嵌图层等）加入已有目录数据集 | arcpy.management.AddItemsToCatalogDataset | extension：目录数据集/目录图层为 ArcGIS 新专属概念 | ArcPy GP（官方实现） |
| Add Portal Items To Catalog Dataset | 将门户的要素、地图、影像、场景、切片等服务条目加入目录数据集 | arcpy.management.AddPortalItemsToCatalogDataset | extension：依赖 ArcGIS 门户体系 | ArcPy GP（官方实现） |
| Create Catalog Dataset | 创建可添加图层、栅格、数据集等集合的目录数据集 | arcpy.management.CreateCatalogDataset | extension：同上 | ArcPy GP（官方实现） |

### Contingent Values toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Contingent Value | 向要素类或表的字段组添加一个关联值（条件值） | arcpy.management.AddContingentValue | extension：关联值/字段组为地理数据库专属行为 | ArcPy GP（官方实现） |
| Alter Field Group | 修改字段组的属性 | arcpy.management.AlterFieldGroup | extension：同上 | ArcPy GP（官方实现） |
| Create Field Group | 为要素类或表创建供关联值使用的字段组 | arcpy.management.CreateFieldGroup | extension：同上 | ArcPy GP（官方实现） |
| Delete Field Group | 从表或要素类删除字段组 | arcpy.management.DeleteFieldGroup | extension：同上 | ArcPy GP（官方实现） |
| Export Contingent Values | 将字段组与关联值导出为 CSV 文件 | arcpy.management.ExportContingentValues | extension：同上 | ArcPy GP（官方实现） |
| Import Contingent Values | 从 CSV 文件导入多个关联值与字段组到数据集 | arcpy.management.ImportContingentValues | extension：同上 | ArcPy GP（官方实现） |
| Remove Contingent Value | 从字段组移除一个关联值 | arcpy.management.RemoveContingentValue | extension：同上 | ArcPy GP（官方实现） |

### Data Comparison toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Detect Feature Changes | 匹配更新线与基线线，检测空间/属性变化并输出带变化信息的要素类 | arcpy.management.DetectFeatureChanges | core：数据集变更检测为通用基础能力 | ArcPy GP（官方实现） |
| Feature Compare | 比较两个要素类或图层并返回比较结果 | arcpy.management.FeatureCompare | core：通用数据对比能力 | ArcPy GP（官方实现） |
| File Compare | 比较两个文件并返回比较结果 | arcpy.management.FileCompare | core：通用文件对比能力 | ArcPy GP（官方实现） |
| Raster Compare | 比较两个栅格数据集或镶嵌数据集的属性 | arcpy.management.RasterCompare | core：通用栅格对比能力 | ArcPy GP（官方实现） |
| Table Compare | 比较两个表或表视图并返回比较结果 | arcpy.management.TableCompare | core：通用表格对比能力 | ArcPy GP（官方实现） |
| TIN Compare | 比较两个 TIN 并返回比较结果 | arcpy.management.TINCompare | core：通用表面数据对比能力 | ArcPy GP（官方实现） |

### Distributed Geodatabase toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Compare Replica Schema | 生成描述副本与相对副本之间模式差异的 XML 文件 | arcpy.management.CompareReplicaSchema | extension：企业级地理数据库复制为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Create Replica | 从企业级地理数据库中指定的要素类、图层、数据集与表创建副本 | arcpy.management.CreateReplica | extension：同上 | ArcPy GP（官方实现） |
| Create Replica From Server | 通过 ArcGIS Server 地理数据服务从远程地理数据库创建副本 | arcpy.management.CreateReplicaFromServer | extension：同上，依赖 ArcGIS Server | ArcPy GP（官方实现） |
| Disable Replica Tracking | 禁用数据的副本追踪 | arcpy.management.DisableReplicaTracking | extension：同上 | ArcPy GP（官方实现） |
| Enable Replica Tracking | 启用副本追踪以支持离线地图与分布式协作 | arcpy.management.EnableReplicaTracking | extension：同上 | ArcPy GP（官方实现） |
| Export Acknowledgement Message | 创建确认已接收数据变更消息的确认文件 | arcpy.management.ExportAcknowledgementMessage | extension：同上 | ArcPy GP（官方实现） |
| Export Data Change Message | 创建包含副本更新的增量文件 | arcpy.management.ExportDataChangeMessage | extension：同上 | ArcPy GP（官方实现） |
| Export Replica Schema | 创建一向/双向副本的模式文件 | arcpy.management.ExportReplicaSchema | extension：同上 | ArcPy GP（官方实现） |
| Import Message | 将增量文件的变更或确认消息导入副本地理数据库 | arcpy.management.ImportMessage | extension：同上 | ArcPy GP（官方实现） |
| Import Replica Schema | 用副本地理数据库与 XML 模式文件应用副本模式差异 | arcpy.management.ImportReplicaSchema | extension：同上 | ArcPy GP（官方实现） |
| Re-export Unacknowledged Messages | 创建包含未确认副本更新的增量文件 | arcpy.management.ReexportUnacknowledgedMessages | extension：同上 | ArcPy GP（官方实现） |
| Synchronize Changes | 按指定方向在两个副本地理数据库之间同步更新 | arcpy.management.SynchronizeChanges | extension：同上 | ArcPy GP（官方实现） |
| Unregister Replica | 从企业级地理数据库注销副本 | arcpy.management.UnregisterReplica | extension：同上 | ArcPy GP（官方实现） |

### Domains toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Coded Value To Domain | 向域的编码值列表添加一个值 | arcpy.management.AddCodedValueToDomain | core：值域约束为多家数据库/GIS 通用的数据完整性能力 | ArcPy GP（官方实现） |
| Alter Domain | 修改工作空间中已有属性域的属性 | arcpy.management.AlterDomain | core：同上 | ArcPy GP（官方实现） |
| Assign Domain To Field | 为指定字段（可按子类型）设置域 | arcpy.management.AssignDomainToField | core：同上 | ArcPy GP（官方实现） |
| Create Domain | 在指定工作空间创建属性域 | arcpy.management.CreateDomain | core：同上 | ArcPy GP（官方实现） |
| Delete Coded Value From Domain | 从编码值域中移除一个值 | arcpy.management.DeleteCodedValueFromDomain | core：同上 | ArcPy GP（官方实现） |
| Delete Domain | 从工作空间删除一个域 | arcpy.management.DeleteDomain | core：同上，删除需谨慎但属通用域管理 | ArcPy GP（官方实现） |
| Domain To Table | 从属性域创建表 | arcpy.management.DomainToTable | core：域与表互转为通用能力 | ArcPy GP（官方实现） |
| Remove Domain From Field | 移除要素类或表字段与属性域的关联 | arcpy.management.RemoveDomainFromField | core：同上 | ArcPy GP（官方实现） |
| Set Value For Range Domain | 设置已有范围域的最小值与最大值 | arcpy.management.SetValueForRangeDomain | core：同上 | ArcPy GP（官方实现） |
| Sort Coded Value Domain | 按编码或描述升/降序排序编码值域 | arcpy.management.SortCodedValueDomain | core：同上 | ArcPy GP（官方实现） |
| Table To Domain | 用表中的值创建或更新编码值域 | arcpy.management.TableToDomain | core：同上 | ArcPy GP（官方实现） |

### Feature Binning toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Disable Feature Binning | 对要素类禁用数据库计算的要素分箱 | arcpy.management.DisableFeatureBinning | extension：要素分箱为 ArcGIS 高级可视化专属能力 | ArcPy GP（官方实现） |
| Enable Feature Binning | 对要素类启用数据库计算的要素分箱 | arcpy.management.EnableFeatureBinning | extension：同上 | ArcPy GP（官方实现） |
| Manage Feature Bin Cache | 管理已启用数据库计算分箱数据的分箱缓存 | arcpy.management.ManageFeatureBinCache | extension：同上 | ArcPy GP（官方实现） |

### Feature Class toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Append Annotation Feature Classes | 合并多个注记要素类为单个注记要素类或追加到已有注记要素类 | arcpy.management.AppendAnnotationFeatureClasses | extension：地理数据库注记为 ArcGIS 专属类型 | ArcPy GP（官方实现） |
| Create Feature Class | 在地理数据库中创建空要素类或在文件夹中创建 shapefile | arcpy.management.CreateFeatureClass | core：建要素类为通用基础能力，适合统一动词候选 | ArcPy GP（官方实现） |
| Create Unregistered Feature Class | 在数据库/企业级地理数据库中创建未注册的空要素类 | arcpy.management.CreateUnregisteredFeatureClass | extension：企业级地理数据库注册机制专属 | ArcPy GP（官方实现） |
| Integrate | 将容差内顶点赋予共同坐标并在交点/边附近加顶点，使要素重合对齐 | arcpy.management.Integrate | core：坐标整合/捕捉对齐为通用几何治理能力 | ArcPy GP（官方实现） |
| Recalculate Feature Class Extent | 按要素重算要素类的 XY/Z/M 范围属性 | arcpy.management.RecalculateFeatureClassExtent | core：范围重算为通用元数据维护 | ArcPy GP（官方实现） |
| Set Feature Class Split Model | 定义要素类上分割操作的行为 | arcpy.management.SetFeatureClassSplitModel | extension：ArcGIS 编辑分割模型专属 | ArcPy GP（官方实现） |

### Features toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add XY Coordinates | 添加 POINT_X/POINT_Y（及 Z/M）字段并计算点坐标值 | arcpy.management.AddXYCoordinates | core：坐标提取为通用能力 | ArcPy GP（官方实现） |
| Adjust 3D Z | 修改 3D 要素的 Z 值 | arcpy.management.Adjust3DZ | core：高程值调整为通用能力 | ArcPy GP（官方实现） |
| Bearing Distance To Line | 由表中 XY、方位角与距离字段生成测地/平面线要素 | arcpy.management.BearingDistanceToLine | core：方位距离建线为通用建图能力 | ArcPy GP（官方实现） |
| Calculate Geometry Attributes | 将长度、面积、坐标等几何特征写入属性字段 | arcpy.management.CalculateGeometryAttributes | core：几何属性计算为通用能力 | ArcPy GP（官方实现） |
| Check Geometry | 生成要素类几何问题报告 | arcpy.management.CheckGeometry | core：几何校验为通用能力 | ArcPy GP（官方实现） |
| Copy Features | 将输入要素类/图层要素复制到新要素类 | arcpy.management.CopyFeatures | core：复制要素为通用能力 | ArcPy GP（官方实现） |
| Delete Features | 删除输入中全部或选中的要素子集 | arcpy.management.DeleteFeatures | defer：破坏性批量删除，需确认 | ArcPy GP（官方实现） |
| Dice | 按顶点上限将超大要素切分为较小要素 | arcpy.management.Dice | core：大要素切分为通用性能治理能力 | ArcPy GP（官方实现） |
| Feature Envelope To Polygon | 为每个输入要素生成其包络矩形面 | arcpy.management.FeatureEnvelopeToPolygon | core：包络生成为通用几何转换 | ArcPy GP（官方实现） |
| Feature To Line | 将面边界转线或在交点处分割线/面生成线要素 | arcpy.management.FeatureToLine | core：几何类型转换为通用能力 | ArcPy GP（官方实现） |
| Feature To Point | 由要素质心或内部点生成点要素 | arcpy.management.FeatureToPoint | core：同上 | ArcPy GP（官方实现） |
| Feature To Polygon | 由线/面围成的区域生成面要素 | arcpy.management.FeatureToPolygon | core：同上 | ArcPy GP（官方实现） |
| Feature Vertices To Points | 由要素指定顶点/位置生成点要素 | arcpy.management.FeatureVerticesToPoints | core：同上 | ArcPy GP（官方实现） |
| Geodetic Densify | 用测地线段的加密近似替换要素线段 | arcpy.management.GeodeticDensify | core：测地加密为通用几何处理 | ArcPy GP（官方实现） |
| Minimum Bounding Geometry | 为每个要素或分组生成最小边界几何面 | arcpy.management.MinimumBoundingGeometry | core：最小边界为通用几何派生 | ArcPy GP（官方实现） |
| Multipart To Singlepart | 将多部件要素拆为单部件要素 | arcpy.management.MultipartToSinglepart | core：多部件拆分为通用能力 | ArcPy GP（官方实现） |
| Points To Line | 由点生成线要素 | arcpy.management.PointsToLine | core：点连线为通用能力 | ArcPy GP（官方实现） |
| Polygon To Line | 将面边界转换为线（可考虑邻接面） | arcpy.management.PolygonToLine | core：几何类型转换为通用能力 | ArcPy GP（官方实现） |
| Repair Geometry | 检查并修复要素几何问题 | arcpy.management.RepairGeometry | core：几何修复为通用能力 | ArcPy GP（官方实现） |
| Split Line At Point | 按与点要素的交点/邻近关系分割线要素 | arcpy.management.SplitLineAtPoint | core：按点分割为通用编辑能力 | ArcPy GP（官方实现） |
| Split Line At Vertices | 在顶点处分割线/面生成折线要素类 | arcpy.management.SplitLineAtVertices | core：同上 | ArcPy GP（官方实现） |
| Subdivide Polygon | 将面要素划分为若干等面积/等份部分 | arcpy.management.SubdividePolygon | core：面细分为通用能力 | ArcPy GP（官方实现） |
| Table To Ellipse | 由表中中心、长短轴与方位角字段生成测地/平面椭圆要素 | arcpy.management.TableToEllipse | core：参数化建要素为通用能力 | ArcPy GP（官方实现） |
| Unsplit Line | 聚合端点重合（可选属性相同）的线要素 | arcpy.management.UnsplitLine | core：线合并为通用能力 | ArcPy GP（官方实现） |
| XY Table To Point | 由表中 X/Y/Z 坐标生成点要素类 | arcpy.management.XYTableToPoint | core：坐标表建点为通用能力 | ArcPy GP（官方实现） |
| XY To Line | 由表中起止点坐标字段生成测地/平面线要素 | arcpy.management.XYToLine | core：坐标表建线为通用能力 | ArcPy GP（官方实现） |

### Fields toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Field | 向表、要素类表、图层或带属性表的栅格添加新字段 | arcpy.management.AddField | core：建字段为通用基础能力 | ArcPy GP（官方实现） |
| Add Fields (multiple) | 向表、要素类或栅格一次添加多个新字段 | arcpy.management.AddFields | core：批量建字段为通用能力 | ArcPy GP（官方实现） |
| Add Global IDs | 向地理数据库要素类、表与要素数据集列表添加全局 ID | arcpy.management.AddGlobalIDs | extension：GlobalID 为地理数据库专属标识机制 | ArcPy GP（官方实现） |
| Add GPS Metadata Fields | 向地理数据库要素类添加 GNSS 字段 | arcpy.management.AddGPSMetadataFields | core：GNSS 元数据字段为通用定位数据能力 | ArcPy GP（官方实现） |
| Add Incrementing ID Field | 向企业数据库表/要素类添加数据库维护的自增 ID 字段 | arcpy.management.AddIncrementingIDField | extension：依赖特定企业数据库与要素服务编辑 | ArcPy GP（官方实现） |
| Alter Field | 重命名地理数据库表/要素类的字段或字段别名 | arcpy.management.AlterField | core：字段改名为通用能力 | ArcPy GP（官方实现） |
| Assign Default To Field | 为指定字段创建默认值，新行自动填入 | arcpy.management.AssignDefaultToField | core：字段默认值为通用能力 | ArcPy GP（官方实现） |
| Batch Update Fields | 按定义表模式批量变换表/要素类字段并生成新表/要素类 | arcpy.management.BatchUpdateFields | core：批量字段变换为通用能力 | ArcPy GP（官方实现） |
| Calculate End Time | 基于另一字段的时间值计算要素结束时间 | arcpy.management.CalculateEndTime | core：时间字段计算为通用能力 | ArcPy GP（官方实现） |
| Calculate Field | 计算要素类、图层或栅格某个字段的值 | arcpy.management.CalculateField | core：字段计算为通用基础能力 | ArcPy GP（官方实现） |
| Calculate Fields (multiple) | 计算要素类、图层或栅格两个以上字段的值 | arcpy.management.CalculateFields | core：同上 | ArcPy GP（官方实现） |
| Convert Time Field | 将日期时间字段值转换到另一字段（类型/格式互转） | arcpy.management.ConvertTimeField | core：时间格式转换为通用能力 | ArcPy GP（官方实现） |
| Convert Time Zone | 将日期字段的时间值从一个时区转换到另一个时区 | arcpy.management.ConvertTimeZone | core：时区转换为通用能力 | ArcPy GP（官方实现） |
| Delete Field | 从表、要素类、图层或栅格删除一个或多个字段 | arcpy.management.DeleteField | defer：破坏性删字段，需确认 | ArcPy GP（官方实现） |
| Disable COGO | 对线要素类禁用 COGO 并移除 COGO 字段与标注/符号 | arcpy.management.DisableCOGO | extension：COGO 为 ArcGIS 测量编辑专属 | ArcPy GP（官方实现） |
| Disable Editor Tracking | 对要素类、表、要素数据集或镶嵌数据集禁用编辑追踪 | arcpy.management.DisableEditorTracking | extension：编辑追踪为地理数据库专属机制 | ArcPy GP（官方实现） |
| Enable COGO | 对线要素类启用 COGO 并添加 COGO 字段与标注 | arcpy.management.EnableCOGO | extension：同上 | ArcPy GP（官方实现） |
| Enable Editor Tracking | 对地理数据库要素类、表、要素数据集或关系类启用编辑追踪 | arcpy.management.EnableEditorTracking | extension：同上 | ArcPy GP（官方实现） |
| Encode Field | 将分类值转换为多个数值字段（独热等编码）供数据科学流程使用 | arcpy.management.EncodeField | core：分类编码为通用数据预处理 | ArcPy GP（官方实现） |
| Field Statistics To Table | 为一个或多个字段生成描述统计表 | arcpy.management.FieldStatisticsToTable | core：字段统计为通用能力 | ArcPy GP（官方实现） |
| Reclassify Field | 按手动界限或重分类方法将数值/文本字段值重分为类别 | arcpy.management.ReclassifyField | core：重分类为通用能力 | ArcPy GP（官方实现） |
| Standardize Field | 用 z-score、min-max 等方法将字段值标准化到指定尺度 | arcpy.management.StandardizeField | core：标准化为通用数据预处理 | ArcPy GP（官方实现） |
| Transform Field | 用对数、平方根、Box-Cox 等函数变换连续字段值分布 | arcpy.management.TransformField | core：字段变换为通用数据预处理 | ArcPy GP（官方实现） |
| Transpose Fields | 将字段/列中的数据转置为新表/要素类中的行 | arcpy.management.TransposeFields | core：转置为通用表格操作 | ArcPy GP（官方实现） |

### File Geodatabase toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Compact | 重排文件地理数据库磁盘存储，常可减小体积并提升性能 | arcpy.management.Compact | extension：文件地理数据库为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Compress File Geodatabase Data | 将地理数据库、要素数据集或单个要素类/表压缩为只读格式 | arcpy.management.CompressFileGeodatabaseData | extension：同上 | ArcPy GP（官方实现） |
| Generate File Geodatabase License | 生成用于显示许可文件地理数据库内容的许可文件（.sdlic） | arcpy.management.GenerateFileGeodatabaseLicense | extension：ArcGIS 许可机制专属 | ArcPy GP（官方实现） |
| Generate Licensed File Geodatabase | 生成定义并限制文件地理数据库内容显示的许可定义文件 | arcpy.management.GenerateLicensedFileGeodatabase | extension：同上 | ArcPy GP（官方实现） |
| Recover File Geodatabase | 从已损坏的文件地理数据库中恢复数据 | arcpy.management.RecoverFileGeodatabase | extension：同上 | ArcPy GP（官方实现） |
| Uncompress File Geodatabase Data | 解压地理数据库、要素数据集或单个要素类/表 | arcpy.management.UncompressFileGeodatabaseData | extension：同上 | ArcPy GP（官方实现） |

### General toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Append | 将多个输入数据集追加（可选更新）到已有目标数据集 | arcpy.management.Append | core：追加为通用基础能力，适合统一动词候选 | ArcPy GP（官方实现） |
| Copy | 复制输入数据 | arcpy.management.Copy | core：复制为通用能力 | ArcPy GP（官方实现） |
| Create Database View | 基于 SQL 表达式在数据库中创建视图 | arcpy.management.CreateDatabaseView | core：数据库视图为通用能力 | ArcPy GP（官方实现） |
| Delete | 永久删除数据、工作空间及其包含项 | arcpy.management.Delete | defer：永久破坏性删除，需管理员级确认 | ArcPy GP（官方实现） |
| Delete Identical | 删除一组字段值（可含几何）完全相同的重复记录 | arcpy.management.DeleteIdentical | defer：破坏性批量去重删除，需确认 | ArcPy GP（官方实现） |
| Export Report To PDF | 将 ArcGIS Pro 报表导出为 PDF 文件 | arcpy.management.ExportReportToPDF | defer：依赖桌面报表对象与交互环境 | ArcPy GP（官方实现） |
| Find Identical | 报告字段值完全相同的记录并生成清单表 | arcpy.management.FindIdentical | core：重复检测为通用能力 | ArcPy GP（官方实现） |
| Merge | 将多个输入数据集合并为单个新输出数据集 | arcpy.management.Merge | core：合并为通用基础能力 | ArcPy GP（官方实现） |
| Rename | 更改数据集名称 | arcpy.management.Rename | core：重命名为通用能力 | ArcPy GP（官方实现） |
| Sort | 按一个或多个字段升/降序重排记录并写入新数据集 | arcpy.management.Sort | core：排序为通用能力 | ArcPy GP（官方实现） |
| Transfer Files | 在文件系统与云存储工作空间之间传输文件 | arcpy.management.TransferFiles | core：文件传输为通用能力 | ArcPy GP（官方实现） |

### Generalization toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Dissolve | 按指定属性聚合要素（融合） | arcpy.management.Dissolve | core：融合为通用基础能力 | ArcPy GP（官方实现） |
| Eliminate | 将小面合并到面积最大或共享边界最长的邻接面，消除碎面 | arcpy.management.Eliminate | core：碎面消除为通用综合能力 | ArcPy GP（官方实现） |
| Eliminate Polygon Part | 删除面中指定大小的部件或洞并输出新要素类 | arcpy.management.EliminatePolygonPart | core：同上 | ArcPy GP（官方实现） |

### Geodatabase Administration toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze Datasets | 更新企业级地理数据库基表、增量表、归档表及其索引的数据库统计 | arcpy.management.AnalyzeDatasets | extension：企业级地理数据库运维专属 | ArcPy GP（官方实现） |
| Change Privileges | 设置/更改企业数据库数据集、要素类或表的用户访问权限 | arcpy.management.ChangePrivileges | defer：权限管理需管理员权限 | ArcPy GP（官方实现） |
| Compress | 压缩企业级地理数据库，删除未被版本引用的状态与冗余行 | arcpy.management.Compress | extension：版本状态压缩为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Configure Geodatabase Log File Tables | 更改旧版企业级地理数据库日志文件表类型 | arcpy.management.ConfigureGeodatabaseLogFileTables | extension：同上 | ArcPy GP（官方实现） |
| Create Database Sequence | 在地理数据库中创建数据库序列供自定义应用使用 | arcpy.management.CreateDatabaseSequence | extension：地理数据库专属 | ArcPy GP（官方实现） |
| Create Database User | 创建有足够权限在数据库中建数据的数据库用户 | arcpy.management.CreateDatabaseUser | defer：建用户需管理员权限 | ArcPy GP（官方实现） |
| Create Enterprise Geodatabase | 创建数据库、存储位置与地理数据库管理员用户并建企业级地理数据库 | arcpy.management.CreateEnterpriseGeodatabase | defer：建库需管理员权限且为 ArcGIS 专属部署 | ArcPy GP（官方实现） |
| Create Role | 创建数据库角色以便增删用户 | arcpy.management.CreateRole | defer：角色管理需管理员权限 | ArcPy GP（官方实现） |
| Delete Database Sequence | 从地理数据库删除数据库序列 | arcpy.management.DeleteDatabaseSequence | extension：地理数据库专属 | ArcPy GP（官方实现） |
| Delete Schema Geodatabase | 删除 Oracle 中用户模式下的地理数据库 | arcpy.management.DeleteSchemaGeodatabase | defer：破坏性删库，需管理员确认 | ArcPy GP（官方实现） |
| Diagnose Version Metadata | 识别传统版本与状态系统表的不一致 | arcpy.management.DiagnoseVersionMetadata | extension：版本元数据为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Diagnose Version Tables | 识别传统版本增量（A/D）表的不一致 | arcpy.management.DiagnoseVersionTables | extension：同上 | ArcPy GP（官方实现） |
| Enable Enterprise Geodatabase | 在已有数据库中创建系统表、存储过程等以启用地理数据库功能 | arcpy.management.EnableEnterpriseGeodatabase | defer：启用企业库需管理员权限 | ArcPy GP（官方实现） |
| Export Geodatabase Configuration Keywords | 将企业级地理数据库配置关键字及参数导出为可编辑文件 | arcpy.management.ExportGeodatabaseConfigurationKeywords | extension：配置关键字为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Import Geodatabase Configuration Keywords | 导入配置关键字文件以定义企业级地理数据库存储参数 | arcpy.management.ImportGeodatabaseConfigurationKeywords | extension：同上 | ArcPy GP（官方实现） |
| Migrate Storage | 将 Oracle/SQL Server 地理数据库列数据迁移到另一数据类型的列 | arcpy.management.MigrateStorage | extension：同上 | ArcPy GP（官方实现） |
| Rebuild Indexes | 重建企业级地理数据库的属性/空间索引及版本系统表索引 | arcpy.management.RebuildIndexes | extension：企业库索引重建，虽索引通用但此工具面向 ArcGIS 系统表 | ArcPy GP（官方实现） |
| Register With Geodatabase | 将第三方工具在数据库中创建的要素类、表、视图、栅格注册到地理数据库 | arcpy.management.RegisterWithGeodatabase | extension：地理数据库注册机制专属 | ArcPy GP（官方实现） |
| Repair Version Metadata | 修复传统版本系统表的不一致 | arcpy.management.RepairVersionMetadata | extension：同上 | ArcPy GP（官方实现） |
| Repair Version Tables | 修复传统版本增量（A/D）表的不一致 | arcpy.management.RepairVersionTables | extension：同上 | ArcPy GP（官方实现） |
| Update Enterprise Geodatabase License | 更新企业级地理数据库中的 ArcGIS Server 许可 | arcpy.management.UpdateEnterpriseGeodatabaseLicense | extension：ArcGIS 许可专属 | ArcPy GP（官方实现） |
| Update Portal Dataset Owner | 将数据集的门户所有者更新为另一用户 | arcpy.management.UpdatePortalDatasetOwner | extension：依赖 ArcGIS 门户体系 | ArcPy GP（官方实现） |
| Upgrade Dataset | 将镶嵌、网络、注记、宗地、追踪网络、公用设施网络等数据集模式升级到当前版本 | arcpy.management.UpgradeDataset | extension：ArcGIS 数据集版本升级专属 | ArcPy GP（官方实现） |
| Upgrade Geodatabase | 将地理数据库升级到最新 ArcGIS 版本 | arcpy.management.UpgradeGeodatabase | extension：同上 | ArcPy GP（官方实现） |

### Indexes toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Attribute Index | 向表、要素类、shapefile 或带属性关系类添加属性索引 | arcpy.management.AddAttributeIndex | core：属性索引为通用基础能力 | ArcPy GP（官方实现） |
| Add Spatial Index | 向 shapefile 或各类地理数据库要素类添加/重建空间索引 | arcpy.management.AddSpatialIndex | core：空间索引为通用基础能力 | ArcPy GP（官方实现） |
| Remove Attribute Index | 从表、要素类、shapefile 删除属性索引 | arcpy.management.RemoveAttributeIndex | core：索引管理为通用能力 | ArcPy GP（官方实现） |
| Remove Spatial Index | 从 shapefile 或各类地理数据库要素类删除空间索引 | arcpy.management.RemoveSpatialIndex | core：同上 | ArcPy GP（官方实现） |

### Joins and Relates toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Join | 基于公共字段将图层临时连接到另一图层或表 | arcpy.management.AddJoin | core：连接为通用基础能力 | ArcPy GP（官方实现） |
| Add Relate | 基于字段值将图层与另一图层或表临时关联 | arcpy.management.AddRelate | core：关联为通用能力 | ArcPy GP（官方实现） |
| Add Spatial Join | 基于空间关系将一个要素的属性临时连接到另一要素 | arcpy.management.AddSpatialJoin | core：空间连接为通用基础能力 | ArcPy GP（官方实现） |
| Join Field | 基于公共属性字段将表内容永久连接到另一表 | arcpy.management.JoinField | core：永久字段连接为通用能力 | ArcPy GP（官方实现） |
| Remove Join | 从要素图层或表视图移除连接 | arcpy.management.RemoveJoin | core：同上 | ArcPy GP（官方实现） |
| Remove Relate | 从要素图层或表视图移除关联 | arcpy.management.RemoveRelate | core：同上 | ArcPy GP（官方实现） |
| Validate Join | 验证两图层/表连接的字段名、OID、匹配与一对一/一对多等性质 | arcpy.management.ValidateJoin | core：连接校验为通用能力 | ArcPy GP（官方实现） |

### LAS Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Files To LAS Dataset | 向 LAS 数据集添加 LAS 文件与表面约束要素的引用 | arcpy.management.AddFilesToLASDataset | core：LAS 点云集合管理为多家共有能力（LAS 为开放格式） | ArcPy GP（官方实现） |
| Build LAS Dataset Pyramid | 构建/更新 LAS 数据集显示缓存以优化渲染 | arcpy.management.BuildLASDatasetPyramid | extension：LAS 数据集金字塔为 ArcGIS 数据集实现 | ArcPy GP（官方实现） |
| Create LAS Dataset | 创建引用一个或多个 LAS 文件（可选表面约束）的 LAS 数据集 | arcpy.management.CreateLASDataset | core：创建点云数据集为通用能力 | ArcPy GP（官方实现） |
| LAS Dataset Statistics | 计算/更新 LAS 数据集统计并可生成统计报告 | arcpy.management.LASDatasetStatistics | core：点云统计为通用能力 | ArcPy GP（官方实现） |
| LAS Point Statistics As Raster | 生成像元值反映 LAS 点统计信息的栅格 | arcpy.management.LASPointStatisticsAsRaster | core：点云栅格化统计为通用能力 | ArcPy GP（官方实现） |
| Remove Files From LAS Dataset | 从 LAS 数据集移除 LAS 文件与表面约束要素 | arcpy.management.RemoveFilesFromLASDataset | core：点云集合管理为通用能力 | ArcPy GP（官方实现） |

### Layers and Table Views toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Apply Symbology From Layer | 将指定图层/图层文件的符号系统应用到输入图层 | arcpy.management.ApplySymbologyFromLayer | defer：符号系统依赖桌面图层交互 | ArcPy GP（官方实现） |
| Make Aggregation Query Layer | 创建按时间/范围/属性动态汇总聚合 DBMS 表并连接要素图层的查询图层 | arcpy.management.MakeAggregationQueryLayer | core：动态聚合查询图层为通用能力 | ArcPy GP（官方实现） |
| Make Building Layer | 从 BIM 工作空间或地理数据库数据集创建复合建筑图层 | arcpy.management.MakeBuildingLayer | extension：建筑图层为 ArcGIS BIM 集成专属 | ArcPy GP（官方实现） |
| Make Feature Layer | 从要素类或图层文件创建临时要素图层 | arcpy.management.MakeFeatureLayer | core：建图层为通用基础能力 | ArcPy GP（官方实现） |
| Make Image Server Layer | 从影像服务创建临时栅格图层 | arcpy.management.MakeImageServerLayer | core：服务图层创建为通用能力 | ArcPy GP（官方实现） |
| Make LAS Dataset Layer | 创建可过滤 LAS 点并控制表面约束的 LAS 数据集图层 | arcpy.management.MakeLASDatasetLayer | core：点云图层创建为通用能力 | ArcPy GP（官方实现） |
| Make Mosaic Layer | 从镶嵌数据集或图层文件创建临时镶嵌图层 | arcpy.management.MakeMosaicLayer | extension：镶嵌数据集为 ArcGIS 专属概念 | ArcPy GP（官方实现） |
| Make Query Layer | 基于 SQL 查询从 DBMS 表创建查询图层 | arcpy.management.MakeQueryLayer | core：SQL 查询图层为通用能力 | ArcPy GP（官方实现） |
| Make Query Table | 对数据库执行 SQL 查询并以图层/表视图呈现（可连接多表或取子集） | arcpy.management.MakeQueryTable | core：同上 | ArcPy GP（官方实现） |
| Make Raster Layer | 从栅格数据集或图层文件创建临时栅格图层 | arcpy.management.MakeRasterLayer | core：建栅格图层为通用能力 | ArcPy GP（官方实现） |
| Make Scene Layer | 从场景图层包或场景服务创建场景图层 | arcpy.management.MakeSceneLayer | extension：场景图层/I3S 为 ArcGIS 平台概念 | ArcPy GP（官方实现） |
| Make Table View | 从表或要素类创建临时表视图 | arcpy.management.MakeTableView | core：建表视图为通用能力 | ArcPy GP（官方实现） |
| Make TIN Layer | 从 TIN 数据集或图层文件创建临时 TIN 图层 | arcpy.management.MakeTINLayer | core：建 TIN 图层为通用能力 | ArcPy GP（官方实现） |
| Make WCS Layer | 从 WCS 服务创建临时栅格图层 | arcpy.management.MakeWCSLayer | core：OGC WCS 为开放标准，通用能力 | ArcPy GP（官方实现） |
| Make XY Event Layer | 基于表中 XY（可选 Z）坐标创建临时点要素图层 | arcpy.management.MakeXYEventLayer | core：事件图层为通用能力 | ArcPy GP（官方实现） |
| Match Layer Symbology To A Style | 按字段/表达式匹配样式符号名，为图层创建唯一值符号系统 | arcpy.management.MatchLayerSymbologyToAStyle | defer：符号匹配依赖桌面样式交互 | ArcPy GP（官方实现） |
| Save To Layer File | 将地图图层保存为图层文件（.lyrx，含符号、标注、弹窗等） | arcpy.management.SaveToLayerFile | extension：.lyrx 为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Select Layer By Attribute | 按属性查询添加、更新或移除图层选择集 | arcpy.management.SelectLayerByAttribute | core：属性选择为通用基础能力 | ArcPy GP（官方实现） |
| Select Layer By Location | 按与另一数据集的空间关系选择要素 | arcpy.management.SelectLayerByLocation | core：空间选择为通用基础能力 | ArcPy GP（官方实现） |

### Package toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Consolidate Layer | 将一个或多个图层引用的数据源复制整合到单个文件夹 | arcpy.management.ConsolidateLayer | extension：ArcGIS 工程/图层打包体系专属 | ArcPy GP（官方实现） |
| Consolidate Locator | 将定位器/复合定位器复制整合到单个文件夹 | arcpy.management.ConsolidateLocator | extension：同上 | ArcPy GP（官方实现） |
| Consolidate Map | 将地图及全部引用数据源整合到指定文件夹 | arcpy.management.ConsolidateMap | extension：同上 | ArcPy GP（官方实现） |
| Consolidate Project | 将工程（.aprx）及引用地图与数据整合到指定文件夹 | arcpy.management.ConsolidateProject | extension：同上 | ArcPy GP（官方实现） |
| Consolidate Toolbox | 将一个或多个工具箱整合到指定文件夹 | arcpy.management.ConsolidateToolbox | extension：同上 | ArcPy GP（官方实现） |
| Create Map Tile Package | 由地图生成切片并打包为一个或多个切片包 | arcpy.management.CreateMapTilePackage | extension：ArcGIS 切片包格式专属（概念通用、格式专属） | ArcPy GP（官方实现） |
| Create Mobile Map Package | 将地图、底图及引用数据打包为单个 .mmpk 文件 | arcpy.management.CreateMobileMapPackage | extension：同上 | ArcPy GP（官方实现） |
| Create Mobile Scene Package | 由一个或多个场景创建移动场景包（.mspk） | arcpy.management.CreateMobileScenePackage | extension：同上 | ArcPy GP（官方实现） |
| Create Vector Tile Index | 创建多尺度多边形网格用作矢量切片包的索引面 | arcpy.management.CreateVectorTileIndex | core：矢量切片索引为通用瓦片能力 | ArcPy GP（官方实现） |
| Create Vector Tile Package | 由地图/底图生成矢量切片并打包为 .vtpk 文件 | arcpy.management.CreateVectorTilePackage | extension：.vtpk 为 ArcGIS 格式 | ArcPy GP（官方实现） |
| Extract Package | 将包内容解压到指定文件夹 | arcpy.management.ExtractPackage | extension：ArcGIS 包格式专属 | ArcPy GP（官方实现） |
| Package Layer | 将图层及引用数据打包为单个压缩 .lpkx 文件 | arcpy.management.PackageLayer | extension：同上 | ArcPy GP（官方实现） |
| Package Locator | 将定位器打包为单个压缩 .gcpk 文件 | arcpy.management.PackageLocator | extension：同上 | ArcPy GP（官方实现） |
| Package Map | 将地图及引用数据打包为单个压缩 .mpkx 文件 | arcpy.management.PackageMap | extension：同上 | ArcPy GP（官方实现） |
| Package Project | 将工程及引用地图与数据打包为 .ppkx 文件 | arcpy.management.PackageProject | extension：同上 | ArcPy GP（官方实现） |
| Package Result | 将地理处理结果（含工具与输入输出数据集）打包为 .gpkx 文件 | arcpy.management.PackageResult | extension：同上 | ArcPy GP（官方实现） |
| Share Package | 将包上传分享到 ArcGIS Online 或 Enterprise | arcpy.management.SharePackage | extension：依赖 ArcGIS 门户体系 | ArcPy GP（官方实现） |

### Scene Layers toolset（Package 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create 3D Object Scene Layer Content | 由多面体/3D 对象图层创建场景图层包（.slpk）或 I3S 内容 | arcpy.management.Create3DObjectSceneLayerContent | extension：I3S 场景图层为 ArcGIS 平台专属 | ArcPy GP（官方实现） |
| Create Building Scene Layer Content | 由建筑图层创建场景图层包或 I3S 内容 | arcpy.management.CreateBuildingSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Integrated Mesh Scene Layer Content | 由 OSGB 数据创建集成网格场景图层内容 | arcpy.management.CreateIntegratedMeshSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Point Cloud Scene Layer Content | 由 LAS/zLAS/LAZ 创建点云场景图层包或云端 I3S 内容 | arcpy.management.CreatePointCloudSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Point Scene Layer Content | 由点要素图层创建点场景图层包或 I3S 内容 | arcpy.management.CreatePointSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Create Voxel Scene Layer Content | 由体素图层创建场景图层包 | arcpy.management.CreateVoxelSceneLayerContent | extension：同上 | ArcPy GP（官方实现） |
| Upgrade Scene Layer | 将场景图层包升级到当前 I3S 版本（SLPK 或 i3sREST） | arcpy.management.UpgradeSceneLayer | extension：同上 | ArcPy GP（官方实现） |
| Validate Scene Layer | 在云存储中评估场景图层包是否符合 I3S 规范 | arcpy.management.ValidateSceneLayer | extension：同上 | ArcPy GP（官方实现） |

### Photos toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| GeoTagged Photos To Points | 由地理标记照片元数据中的 XYZ 坐标创建点（可加为附件） | arcpy.management.GeoTaggedPhotosToPoints | core：照片定位建点为通用能力 | ArcPy GP（官方实现） |
| Match Photos To Rows By Time | 按时间戳将照片文件匹配到表/要素类行并可加为附件 | arcpy.management.MatchPhotosToRowsByTime | core：按时间匹配为通用能力 | ArcPy GP（官方实现） |

### Projections and Transformations toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Batch Project | 将一组要素类/要素数据集批量投影到统一坐标系 | arcpy.management.BatchProject | core：批量投影为通用基础能力 | ArcPy GP（官方实现） |
| Convert Coordinate Notation | 将一/两个字段中的坐标表示格式互转 | arcpy.management.ConvertCoordinateNotation | core：坐标表示转换为通用能力 | ArcPy GP（官方实现） |
| Create Custom Geographic Transformation | 创建两个地理坐标系/基准面之间的自定义地理变换方法 | arcpy.management.CreateCustomGeographicTransformation | core：基准变换为通用能力 | ArcPy GP（官方实现） |
| Create Spatial Reference | 创建供 ModelBuilder 使用的空间参考 | arcpy.management.CreateSpatialReference | core：空间参考定义为通用能力 | ArcPy GP（官方实现） |
| Define Projection | 覆写数据集存储的坐标系信息（用于未知/错误坐标系） | arcpy.management.DefineProjection | core：定义投影为通用基础能力 | ArcPy GP（官方实现） |
| Project | 将空间数据从一个坐标系投影到另一个坐标系 | arcpy.management.Project | core：投影为通用基础能力，适合统一动词候选 | ArcPy GP（官方实现） |

### Projections and Transformations — Raster 子集 toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Flip | 沿中心水平轴上下翻转栅格 | arcpy.management.Flip | core：栅格翻转为通用能力 | ArcPy GP（官方实现） |
| Mirror | 沿中心垂直轴左右镜像栅格 | arcpy.management.Mirror | core：栅格镜像为通用能力 | ArcPy GP（官方实现） |
| Project Raster | 将栅格数据集从一个坐标系转换到另一个坐标系 | arcpy.management.ProjectRaster | core：栅格投影为通用基础能力 | ArcPy GP（官方实现） |
| Register Raster | 将栅格自动配准到参考影像或用控制点文件做地理配准（镶嵌数据集逐项处理） | arcpy.management.RegisterRaster | core：影像配准为通用能力 | ArcPy GP（官方实现） |
| Rescale | 按 X/Y 缩放因子调整栅格大小 | arcpy.management.Rescale | core：栅格缩放为通用能力 | ArcPy GP（官方实现） |
| Rotate | 绕指定枢轴点旋转栅格数据集 | arcpy.management.Rotate | core：栅格旋转为通用能力 | ArcPy GP（官方实现） |
| Shift | 按 X/Y 偏移量将栅格平移到新地理位置 | arcpy.management.Shift | core：栅格平移为通用能力 | ArcPy GP（官方实现） |
| Warp | 用源/目标控制点变换栅格数据集（类似地理配准） | arcpy.management.Warp | core：栅格纠正为通用能力 | ArcPy GP（官方实现） |
| Warp From File | 用含源/目标控制点的文本文件变换栅格数据集 | arcpy.management.WarpFromFile | core：同上 | ArcPy GP（官方实现） |

### Raster toolset

Raster 为伞形工具集，无直属工具，其全部 80 个工具分布在以下 5 个子集中：Mosaic Dataset（32）、Ortho Mapping（15）、Raster Dataset（8）、Raster Processing（11）、Raster Properties（14）。

### Raster — Mosaic Dataset toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Rasters To Mosaic Dataset | 从文件、文件夹、表或 Web 服务向镶嵌数据集添加栅格数据集 | arcpy.management.AddRastersToMosaicDataset | extension：镶嵌数据集为 ArcGIS 专属高级影像管理结构 | ArcPy GP（官方实现） |
| Alter Mosaic Dataset Schema | 定义非所有者在企业级地理数据库中编辑镶嵌数据集的操作权限 | arcpy.management.AlterMosaicDatasetSchema | extension：同上 | ArcPy GP（官方实现） |
| Analyze Mosaic Dataset | 检查镶嵌数据集的错误与可改进项 | arcpy.management.AnalyzeMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Build Boundary | 在新增栅格超出原覆盖时更新镶嵌数据集边界范围 | arcpy.management.BuildBoundary | extension：同上 | ArcPy GP（官方实现） |
| Build Footprints | 计算镶嵌数据集中每个栅格的足迹范围 | arcpy.management.BuildFootprints | extension：同上 | ArcPy GP（官方实现） |
| Build Mosaic Dataset Item Cache | 在镶嵌数据集所有函数链末步插入缓存栅格函数 | arcpy.management.BuildMosaicDatasetItemCache | extension：同上 | ArcPy GP（官方实现） |
| Build Overviews | 在镶嵌数据集上定义并生成概视图（金字塔） | arcpy.management.BuildOverviews | extension：同上 | ArcPy GP（官方实现） |
| Build Seamlines | 生成/更新镶嵌数据集的镶嵌线以平滑重叠影像排序 | arcpy.management.BuildSeamlines | extension：同上 | ArcPy GP（官方实现） |
| Calculate Cell Size Ranges | 按空间分辨率计算镶嵌数据集中栅格的可见级别 | arcpy.management.CalculateCellSizeRanges | extension：同上 | ArcPy GP（官方实现） |
| Clear Pixel Cache | 清除与镶嵌数据集关联的像素缓存 | arcpy.management.ClearPixelCache | extension：同上 | ArcPy GP（官方实现） |
| Color Balance Mosaic Dataset | 使相邻影像间过渡无缝的颜色平衡处理 | arcpy.management.ColorBalanceMosaicDataset | extension：同上（色彩平衡概念通用、实现依托镶嵌数据集） | ArcPy GP（官方实现） |
| Compute Dirty Area | 识别镶嵌数据集自某时刻以来发生变化的区域 | arcpy.management.ComputeDirtyArea | extension：同上 | ArcPy GP（官方实现） |
| Compute Mosaic Candidates | 找出最能代表镶嵌区域的影像候选 | arcpy.management.ComputeMosaicCandidates | extension：同上 | ArcPy GP（官方实现） |
| Create Mosaic Dataset | 在地理数据库中创建空镶嵌数据集 | arcpy.management.CreateMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Create Referenced Mosaic Dataset | 从已有镶嵌数据集的条目创建独立的引用镶嵌数据集 | arcpy.management.CreateReferencedMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Define Mosaic Dataset NoData | 指定一个或多个值表示为 NoData | arcpy.management.DefineMosaicDatasetNoData | extension：同上 | ArcPy GP（官方实现） |
| Define Overviews | 设置镶嵌数据集概视图的生成方式（供 Build Overviews 使用） | arcpy.management.DefineOverviews | extension：同上 | ArcPy GP（官方实现） |
| Delete Mosaic Dataset | 删除镶嵌数据集及其概视图与条目缓存 | arcpy.management.DeleteMosaicDataset | defer：破坏性删除镶嵌数据集，需确认（且属 ArcGIS 专属结构） | ArcPy GP（官方实现） |
| Edit Raster Function | 在镶嵌数据集或含栅格函数的图层中添加、替换或移除函数链 | arcpy.management.EditRasterFunction | extension：栅格函数链为 ArcGIS 影像处理专属机制 | ArcPy GP（官方实现） |
| Export Mosaic Dataset Geometry | 创建显示镶嵌数据集足迹、边界、镶嵌线或分辨率的要素类 | arcpy.management.ExportMosaicDatasetGeometry | extension：同上 | ArcPy GP（官方实现） |
| Export Mosaic Dataset Items | 将镶嵌数据集中处理后的影像另存到指定文件夹与格式 | arcpy.management.ExportMosaicDatasetItems | extension：同上 | ArcPy GP（官方实现） |
| Export Mosaic Dataset Paths | 创建镶嵌数据集每条目文件路径的表（可只列损坏路径） | arcpy.management.ExportMosaicDatasetPaths | extension：同上 | ArcPy GP（官方实现） |
| Generate Exclude Area | 按颜色或值域裁剪掩膜像素，供颜色平衡时排除云、水等干扰区 | arcpy.management.GenerateExcludeArea | extension：同上 | ArcPy GP（官方实现） |
| Generate Raster Collection | 对镶嵌数据集中的影像集合逐个或分组批量分析处理 | arcpy.management.GenerateRasterCollection | extension：同上 | ArcPy GP（官方实现） |
| Import Mosaic Dataset Geometry | 按要素类修改镶嵌数据集的足迹、边界或镶嵌线几何 | arcpy.management.ImportMosaicDatasetGeometry | extension：同上 | ArcPy GP（官方实现） |
| Merge Mosaic Dataset Items | 将镶嵌数据集中多个条目合并为一个条目 | arcpy.management.MergeMosaicDatasetItems | extension：同上 | ArcPy GP（官方实现） |
| Mosaic Dataset To Mobile Mosaic Dataset | 将镶嵌数据集转换为兼容 Runtime 的移动镶嵌数据集 | arcpy.management.MosaicDatasetToMobileMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Remove Rasters From Mosaic Dataset | 从镶嵌数据集移除选中的栅格 | arcpy.management.RemoveRastersFromMosaicDataset | extension：同上 | ArcPy GP（官方实现） |
| Repair Mosaic Dataset Paths | 在移动/复制镶嵌数据集后重置源影像路径 | arcpy.management.RepairMosaicDatasetPaths | extension：同上 | ArcPy GP（官方实现） |
| Set Mosaic Dataset Properties | 定义镶嵌数据集显示与发布为影像服务的默认值 | arcpy.management.SetMosaicDatasetProperties | extension：同上 | ArcPy GP（官方实现） |
| Split Mosaic Dataset Items | 拆分先前合并的镶嵌数据集条目 | arcpy.management.SplitMosaicDatasetItems | extension：同上 | ArcPy GP（官方实现） |
| Synchronize Mosaic Dataset | 同步镶嵌数据集保持最新（可更新概视图、缓存、恢复配置、移除路径） | arcpy.management.SynchronizeMosaicDataset | extension：同上 | ArcPy GP（官方实现） |

### Raster — Ortho Mapping toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze Control Points | 分析控制点覆盖并指出需补充控制点以改善区域网平差的区域 | arcpy.management.AnalyzeControlPoints | core：正射校正控制点分析为遥感通用能力 | ArcPy GP（官方实现） |
| Append Control Points | 将控制点合并到已有控制点表 | arcpy.management.AppendControlPoints | core：同上 | ArcPy GP（官方实现） |
| Apply Block Adjustment | 用解算表将地理调整应用到镶嵌数据集条目 | arcpy.management.ApplyBlockAdjustment | core：区域网平差应用为摄影测量通用能力（此处依托镶嵌数据集） | ArcPy GP（官方实现） |
| Build Stereo Model | 基于用户提供的立体像对构建镶嵌数据集立体模型 | arcpy.management.BuildStereoModel | core：立体模型为摄影测量通用能力 | ArcPy GP（官方实现） |
| Compute Block Adjustment | 计算镶嵌数据集的调整量并生成解算表 | arcpy.management.ComputeBlockAdjustment | core：区域网平差为通用能力 | ArcPy GP（官方实现） |
| Compute Camera Model | 由原始影像 EXIF 估计并精化内外方位相机模型，可用 DSM 改善正射 | arcpy.management.ComputeCameraModel | core：相机模型估计为通用能力 | ArcPy GP（官方实现） |
| Compute Control Points | 在镶嵌数据集与参考影像之间创建控制点 | arcpy.management.ComputeControlPoints | core：控制点计算为通用能力 | ArcPy GP（官方实现） |
| Compute Fiducials | 计算镶嵌数据集每幅影像在影像/胶片空间的框标坐标 | arcpy.management.ComputeFiducials | core：框标计算为摄影测量通用能力 | ArcPy GP（官方实现） |
| Compute Tie Points | 计算重叠镶嵌条目之间的连接点 | arcpy.management.ComputeTiePoints | core：连接点计算为通用能力 | ArcPy GP（官方实现） |
| Export Frame and Camera Parameters | 从含框幅影像的镶嵌数据集导出帧与相机参数 | arcpy.management.ExportFrameAndCameraParameters | core：参数导出为通用能力 | ArcPy GP（官方实现） |
| Generate Block Adjustment Report | 生成正射区域网平差报告以评估产品质量与精度 | arcpy.management.GenerateBlockAdjustmentReport | core：平差报告为通用能力 | ArcPy GP（官方实现） |
| Generate Point Cloud | 由立体像对计算 3D 点并输出为 LAS 点云集 | arcpy.management.GeneratePointCloud | core：密集点云生成为通用能力 | ArcPy GP（官方实现） |
| Interpolate From Point Cloud | 由点云内插生成 DTM 或 DSM | arcpy.management.InterpolateFromPointCloud | core：点云内插地形为通用能力 | ArcPy GP（官方实现） |
| Match Control Points | 为给定地面控制点在重叠影像中创建匹配连接点 | arcpy.management.MatchControlPoints | core：控制点匹配为通用能力 | ArcPy GP（官方实现） |
| Update Interior Orientation | 用框标表构建仿射变换精化每幅影像的内定向 | arcpy.management.UpdateInteriorOrientation | core：内定向为摄影测量通用能力 | ArcPy GP（官方实现） |

### Raster — Raster Dataset toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Copy Raster | 保存栅格数据集副本或将镶嵌数据集转为单个栅格数据集 | arcpy.management.CopyRaster | core：栅格复制/转为通用能力 | ArcPy GP（官方实现） |
| Create Random Raster | 按指定分布创建随机值栅格数据集 | arcpy.management.CreateRandomRaster | core：随机栅格为通用能力 | ArcPy GP（官方实现） |
| Create Raster Dataset | 创建空栅格数据集 | arcpy.management.CreateRasterDataset | core：建栅格为通用基础能力 | ArcPy GP（官方实现） |
| Download Rasters | 从影像服务或镶嵌数据集下载源文件 | arcpy.management.DownloadRasters | core：下载栅格为通用能力 | ArcPy GP（官方实现） |
| Generate Raster From Raster Function | 由输入栅格函数/函数链生成栅格数据集 | arcpy.management.GenerateRasterFromRasterFunction | extension：栅格函数链为 ArcGIS 专属机制 | ArcPy GP（官方实现） |
| Mosaic | 将多个已有栅格/镶嵌数据集镶嵌到已有栅格数据集 | arcpy.management.Mosaic | core：栅格镶嵌为通用基础能力 | ArcPy GP（官方实现） |
| Mosaic To New Raster | 将多个栅格数据集镶嵌为新栅格数据集 | arcpy.management.MosaicToNewRaster | core：同上 | ArcPy GP（官方实现） |
| Workspace To Raster Dataset | 将文件夹中全部栅格数据集镶嵌为一个栅格数据集 | arcpy.management.WorkspaceToRasterDataset | core：同上 | ArcPy GP（官方实现） |

### Raster — Raster Processing toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Clip Raster | 裁剪栅格数据集、镶嵌数据集或影像服务图层的一部分 | arcpy.management.ClipRaster | core：栅格裁剪为通用基础能力 | ArcPy GP（官方实现） |
| Composite Bands | 由多个波段创建单个栅格数据集 | arcpy.management.CompositeBands | core：波段合成为通用能力 | ArcPy GP（官方实现） |
| Compute Pansharpen Weights | 为新/自定义传感器计算最优全色锐化权重 | arcpy.management.ComputePansharpenWeights | core：全色锐化为遥感通用能力 | ArcPy GP（官方实现） |
| Create Color Composite | 由多波段栅格创建三波段彩色合成栅格 | arcpy.management.CreateColorComposite | core：彩色合成为通用能力 | ArcPy GP（官方实现） |
| Create Ortho Corrected Raster Dataset | 用高程与 RPC 对卫星数据做正射校正生成栅格 | arcpy.management.CreateOrthoCorrectedRasterDataset | core：正射校正为遥感通用能力 | ArcPy GP（官方实现） |
| Create Pansharpened Raster Dataset | 融合高分辨率全色与低分辨率多波段生成高分辨率多波段栅格 | arcpy.management.CreatePansharpenedRasterDataset | core：全色锐化融合为通用能力 | ArcPy GP（官方实现） |
| Extract Subdataset | 从 HDF 或 NITF 数据集中提取子数据集生成新栅格 | arcpy.management.ExtractSubdataset | core：子数据集提取为通用能力 | ArcPy GP（官方实现） |
| Generate Table From Raster Function | 将栅格函数数据集转换为表或要素类 | arcpy.management.GenerateTableFromRasterFunction | extension：栅格函数为 ArcGIS 专属机制 | ArcPy GP（官方实现） |
| Raster To DTED | 按 DTED 切分结构将栅格拆为独立文件 | arcpy.management.RasterToDTED | core：DTED 为开放军用高程格式，通用能力 | ArcPy GP（官方实现） |
| Resample | 改变栅格空间分辨率并按规则聚合/内插像元值 | arcpy.management.Resample | core：重采样为通用基础能力 | ArcPy GP（官方实现） |
| Split Raster | 按瓦片或面要素将栅格数据集切分为小块 | arcpy.management.SplitRaster | core：栅格切分为通用能力 | ArcPy GP（官方实现） |

### Raster — Raster Properties toolset（Raster 子集）

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Colormap | 向栅格数据集添加新颜色映射表或替换已有颜色映射表 | arcpy.management.AddColormap | core：颜色映射为通用栅格属性 | ArcPy GP（官方实现） |
| Batch Build Pyramids | 为多个栅格数据集批量建金字塔 | arcpy.management.BatchBuildPyramids | core：金字塔为通用栅格能力 | ArcPy GP（官方实现） |
| Batch Calculate Statistics | 为多个栅格数据集批量计算统计 | arcpy.management.BatchCalculateStatistics | core：栅格统计为通用能力 | ArcPy GP（官方实现） |
| Build Pyramids | 为栅格数据集建金字塔 | arcpy.management.BuildPyramids | core：同上 | ArcPy GP（官方实现） |
| Build Pyramids And Statistics | 遍历文件夹为全部栅格建金字塔并计算统计（亦可处理镶嵌条目） | arcpy.management.BuildPyramidsAndStatistics | core：同上 | ArcPy GP（官方实现） |
| Build Raster Attribute Table | 为栅格数据集添加/更新栅格属性表（主要用于离散数据） | arcpy.management.BuildRasterAttributeTable | core：栅格属性表为通用能力 | ArcPy GP（官方实现） |
| Calculate Statistics | 计算栅格或镶嵌数据集的统计 | arcpy.management.CalculateStatistics | core：同上 | ArcPy GP（官方实现） |
| Convert Raster Function Template | 在 rft.xml、json、二进制之间转换栅格函数模板格式 | arcpy.management.ConvertRasterFunctionTemplate | extension：栅格函数模板为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Delete Colormap | 移除栅格数据集关联的颜色映射表 | arcpy.management.DeleteColormap | core：颜色映射管理为通用能力 | ArcPy GP（官方实现） |
| Delete Raster Attribute Table | 移除栅格数据集关联的栅格属性表 | arcpy.management.DeleteRasterAttributeTable | core：同上 | ArcPy GP（官方实现） |
| Export Raster World File | 按像元大小与左上角位置创建世界文件 | arcpy.management.ExportRasterWorldFile | core：世界文件为通用格式 | ArcPy GP（官方实现） |
| Get Cell Value | 按 XY 坐标获取指定像元值 | arcpy.management.GetCellValue | core：像元查询为通用能力 | ArcPy GP（官方实现） |
| Get Raster Properties | 获取栅格数据集的元数据与描述统计信息 | arcpy.management.GetRasterProperties | core：栅格属性读取为通用能力 | ArcPy GP（官方实现） |
| Set Raster Properties | 设置栅格/镶嵌数据集的数据类型、统计与 NoData 值 | arcpy.management.SetRasterProperties | core：同上 | ArcPy GP（官方实现） |

### Relationship Classes toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Rule To Relationship Class | 向关系类添加一条规则 | arcpy.management.AddRuleToRelationshipClass | extension：地理数据库关系类为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Create Relationship Class | 创建存储源表与目标表字段/要素关联的关系类 | arcpy.management.CreateRelationshipClass | extension：同上（关系概念通用、实现专属） | ArcPy GP（官方实现） |
| Migrate Relationship Class | 将基于 ObjectID 的关系类迁移为基于 GlobalID 的关系类 | arcpy.management.MigrateRelationshipClass | extension：同上 | ArcPy GP（官方实现） |
| Remove Rule From Relationship Class | 从关系类移除一条规则 | arcpy.management.RemoveRuleFromRelationshipClass | extension：同上 | ArcPy GP（官方实现） |
| Set Relationship Class Split Policy | 定义关联要素的分割策略 | arcpy.management.SetRelationshipClassSplitPolicy | extension：同上 | ArcPy GP（官方实现） |
| Table To Relationship Class | 由源、目标与关系表创建带属性的关系类 | arcpy.management.TableToRelationshipClass | extension：同上 | ArcPy GP（官方实现） |

### Sampling toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Create Fishnet | 创建矩形格网（渔网），输出折线或面要素 | arcpy.management.CreateFishnet | core：格网生成为通用能力 | ArcPy GP（官方实现） |
| Create Random Points | 创建指定数量的随机点（可在范围、面内、点上或线沿线生成） | arcpy.management.CreateRandomPoints | core：随机采样为通用能力 | ArcPy GP（官方实现） |
| Generate Points Along Lines | 沿线/面边界按固定间隔或长度百分比生成点 | arcpy.management.GeneratePointsAlongLines | core：沿线布点为通用能力 | ArcPy GP（官方实现） |
| Generate Rectangles Along Lines | 沿单个或一组线要素生成系列矩形面 | arcpy.management.GenerateRectanglesAlongLines | core：沿线矩形为通用能力 | ArcPy GP（官方实现） |
| Generate Tessellation | 生成覆盖给定范围的规则多边形镶嵌网格（三角/方/菱/六边形/H3 等） | arcpy.management.GenerateTessellation | core：镶嵌网格为通用能力 | ArcPy GP（官方实现） |
| Generate Transects Along Lines | 沿线按固定间隔生成垂直样线（横断面） | arcpy.management.GenerateTransectsAlongLines | core：样线生成为通用能力 | ArcPy GP（官方实现） |

### Subtypes toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Subtype | 向输入表的子类型集合添加新子类型 | arcpy.management.AddSubtype | extension：子类型为地理数据库专属分组机制 | ArcPy GP（官方实现） |
| Remove Subtype | 按代码从输入表移除子类型 | arcpy.management.RemoveSubtype | extension：同上 | ArcPy GP（官方实现） |
| Set Default Subtype | 设置输入表子类型的默认值/代码 | arcpy.management.SetDefaultSubtype | extension：同上 | ArcPy GP（官方实现） |
| Set Subtype Field | 定义输入表/要素类中存储子类型代码的字段 | arcpy.management.SetSubtypeField | extension：同上 | ArcPy GP（官方实现） |

### Table toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze | 更新业务表、要素表、增量表及其索引的数据库统计 | arcpy.management.Analyze | core：表统计更新为通用数据库能力 | ArcPy GP（官方实现） |
| Copy Rows | 将表的行复制到另一表 | arcpy.management.CopyRows | core：行复制为通用能力 | ArcPy GP（官方实现） |
| Create Table | 创建地理数据库表或 dBASE 表 | arcpy.management.CreateTable | core：建表为通用基础能力 | ArcPy GP（官方实现） |
| Create Unregistered Table | 在数据库/企业级地理数据库中创建未注册的空表 | arcpy.management.CreateUnregisteredTable | extension：企业级地理数据库注册机制专属 | ArcPy GP（官方实现） |
| Delete Rows | 删除输入中全部或选中的行子集 | arcpy.management.DeleteRows | defer：破坏性批量删行，需确认 | ArcPy GP（官方实现） |
| Get Count | 返回表的总行数 | arcpy.management.GetCount | core：计数为通用能力 | ArcPy GP（官方实现） |
| Pivot Table | 对输入表透视以减少记录冗余、扁平化一对多关系 | arcpy.management.PivotTable | core：透视表为通用能力 | ArcPy GP（官方实现） |
| Truncate Table | 用数据库截断方式移除表/要素类的全部行 | arcpy.management.TruncateTable | defer：破坏性清空，需确认 | ArcPy GP（官方实现） |

### Tile Cache toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Export Tile Cache | 将已有切片缓存的切片导出为新缓存或切片包 | arcpy.management.ExportTileCache | core：切片缓存导出为通用瓦片能力（格式含 ArcGIS 包） | ArcPy GP（官方实现） |
| Generate Tile Cache Tiling Scheme | 生成定义切片缓存级别、尺寸等属性的 XML 切片方案文件 | arcpy.management.GenerateTileCacheTilingScheme | core：切片方案为通用瓦片能力 | ArcPy GP（官方实现） |
| Import Tile Cache | 将一个切片缓存的切片导入另一缓存 | arcpy.management.ImportTileCache | core：同上 | ArcPy GP（官方实现） |
| Manage Tile Cache | 在已有切片缓存中创建与更新切片 | arcpy.management.ManageTileCache | core：同上 | ArcPy GP（官方实现） |

### Toolbox toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Analyze Toolbox For Version | 分析工具箱内容并识别与旧版 ArcGIS 的兼容问题 | arcpy.management.AnalyzeToolboxForVersion | extension：ArcGIS 工具箱版本兼容专属 | ArcPy GP（官方实现） |
| Analyze Tools For Pro | 分析 Python 脚本与自定义工具/工具箱中 ArcGIS Pro 不支持的功能 | arcpy.management.AnalyzeToolsForPro | extension：同上 | ArcPy GP（官方实现） |
| Save Toolbox To Version | 分析并将工具箱保存为指定 ArcGIS 版本可用 | arcpy.management.SaveToolboxToVersion | extension：同上 | ArcPy GP（官方实现） |

### Topology toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Feature Class To Topology | 向拓扑添加要素类 | arcpy.management.AddFeatureClassToTopology | extension：地理数据库拓扑为 ArcGIS 专属实现（拓扑概念通用） | ArcPy GP（官方实现） |
| Add Rule To Topology | 向拓扑添加规则 | arcpy.management.AddRuleToTopology | extension：同上 | ArcPy GP（官方实现） |
| Create Topology | 创建不含要素类与规则的空拓扑 | arcpy.management.CreateTopology | extension：同上 | ArcPy GP（官方实现） |
| Export Topology Errors | 将拓扑错误与例外导出到目标地理数据库供任意许可级别使用 | arcpy.management.ExportTopologyErrors | extension：同上 | ArcPy GP（官方实现） |
| Remove Feature Class From Topology | 从拓扑移除要素类 | arcpy.management.RemoveFeatureClassFromTopology | extension：同上 | ArcPy GP（官方实现） |
| Remove Rule From Topology | 从拓扑移除规则 | arcpy.management.RemoveRuleFromTopology | extension：同上 | ArcPy GP（官方实现） |
| Set Cluster Tolerance | 设置拓扑的簇容差 | arcpy.management.SetClusterTolerance | extension：同上 | ArcPy GP（官方实现） |
| Validate Topology | 验证地理数据库拓扑 | arcpy.management.ValidateTopology | extension：同上 | ArcPy GP（官方实现） |

### Trajectory Dataset toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Data To Trajectory Dataset | 向已有轨迹数据集添加轨迹数据 | arcpy.management.AddDataToTrajectoryDataset | extension：轨迹数据集（卫星测高）为 ArcGIS 专属数据类型 | ArcPy GP（官方实现） |
| Create Trajectory Dataset | 在地理数据库中创建空轨迹数据集 | arcpy.management.CreateTrajectoryDataset | extension：同上 | ArcPy GP（官方实现） |
| Repair Trajectory Dataset Paths | 修复轨迹数据集的源数据路径 | arcpy.management.RepairTrajectoryDatasetPaths | extension：同上 | ArcPy GP（官方实现） |

### Versions toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Add Field Conflict Filter | 为地理数据库表/要素类的指定字段添加字段冲突过滤器 | arcpy.management.AddFieldConflictFilter | extension：企业级地理数据库版本为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Alter Version | 修改地理数据库版本属性 | arcpy.management.AlterVersion | extension：同上 | ArcPy GP（官方实现） |
| Change Version | 修改图层/表视图的工作空间以连接指定版本 | arcpy.management.ChangeVersion | extension：同上 | ArcPy GP（官方实现） |
| Create Version | 在指定地理数据库中创建新版本 | arcpy.management.CreateVersion | extension：同上 | ArcPy GP（官方实现） |
| Delete Version | 从企业/工作组/桌面地理数据库删除指定版本 | arcpy.management.DeleteVersion | extension：同上 | ArcPy GP（官方实现） |
| Reconcile Versions | 将一个或多个版本与目标版本协调（reconcile） | arcpy.management.ReconcileVersions | extension：同上 | ArcPy GP（官方实现） |
| Register As Versioned | 将企业级地理数据库数据集注册为版本化 | arcpy.management.RegisterAsVersioned | extension：同上 | ArcPy GP（官方实现） |
| Remove Field Conflict Filter | 移除指定字段的字段冲突过滤器 | arcpy.management.RemoveFieldConflictFilter | extension：同上 | ArcPy GP（官方实现） |
| Unregister As Versioned | 取消企业级地理数据库数据集的版本化注册 | arcpy.management.UnregisterAsVersioned | extension：同上 | ArcPy GP（官方实现） |

### Workspace toolset

| 官方工具名 | 一句话作用 | ArcPy 入口 | 平台判断 | 轮子来源 |
|---|---|---|---|---|
| Clear Workspace Cache | 清除企业级地理数据库工作空间缓存 | arcpy.management.ClearWorkspaceCache | extension：企业级地理数据库缓存专属 | ArcPy GP（官方实现） |
| Create Cloud Storage Connection File | 创建 ArcGIS 支持的云存储连接文件以读写云栅格等数据 | arcpy.management.CreateCloudStorageConnectionFile | core：云存储连接为通用能力 | ArcPy GP（官方实现） |
| Create Database Connection | 创建 ArcGIS 连接数据库/企业级地理数据库的连接文件 | arcpy.management.CreateDatabaseConnection | core：数据库连接为通用能力 | ArcPy GP（官方实现） |
| Create Database Connection String | 创建地理处理工具连接数据库/企业级地理数据库的连接字符串 | arcpy.management.CreateDatabaseConnectionString | core：同上 | ArcPy GP（官方实现） |
| Create Feature Dataset | 在企业/文件/移动地理数据库中创建要素数据集 | arcpy.management.CreateFeatureDataset | extension：要素数据集为地理数据库专属容器 | ArcPy GP（官方实现） |
| Create File Geodatabase | 在文件夹中创建文件地理数据库 | arcpy.management.CreateFileGeodatabase | extension：文件地理数据库为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Create Folder | 在指定位置创建文件夹 | arcpy.management.CreateFolder | core：建文件夹为通用能力 | ArcPy GP（官方实现） |
| Create Mobile Geodatabase | 创建移动地理数据库 | arcpy.management.CreateMobileGeodatabase | extension：移动地理数据库为 ArcGIS 专属格式 | ArcPy GP（官方实现） |
| Create Spatial Type | 向 Oracle/PostgreSQL 数据库添加 ST_Geometry 类型、子类型与函数（或升级） | arcpy.management.CreateSpatialType | core：ST_Geometry 为开放空间类型概念 | ArcPy GP（官方实现） |
| Create SQLite Database | 创建含 ST_Geometry 或 SpatiaLite 空间类型的 GeoPackage/SQLite 数据库 | arcpy.management.CreateSQLiteDatabase | core：GeoPackage/SQLite 为开放格式 | ArcPy GP（官方实现） |
| Export XML Workspace Document | 创建地理数据库内容的可读 XML 文档 | arcpy.management.ExportXMLWorkspaceDocument | extension：地理数据库 XML 工作空间为 ArcGIS 专属 | ArcPy GP（官方实现） |
| Import XML Workspace Document | 将 XML 工作空间文档内容导入已有地理数据库 | arcpy.management.ImportXMLWorkspaceDocument | extension：同上 | ArcPy GP（官方实现） |
| Refresh Excel | 在 ArcGIS Pro 中刷新 Microsoft Excel 文件 | arcpy.management.RefreshExcel | defer：依赖桌面 Excel 交互刷新 | ArcPy GP（官方实现） |
| Update Geodatabase Connection Properties To Branch | 更新企业级地理数据库连接以支持分支版本 | arcpy.management.UpdateGeodatabaseConnectionPropertiesToBranch | extension：分支版本为 ArcGIS 专属 | ArcPy GP（官方实现） |

# SuperMap 功能普查（GIS 综合平台能力底账）

查阅日期：2026-11-02。证据口径：只采信官方一级证据（help.supermap.com 帮助站、iobjectspy.supermap.io 组件文档、supermap.com 官网产品页、support.supermap.com 技术资源中心）。非官方来源（CSDN、前嗅大数据博客等）仅作找官方入口的线索，其内容未采信、未混列。

平台判断标记：**core**＝多家 GIS 共有、可升为平台统一动词的候选；**extension**＝SuperMap 专属或该家实现特色明显、走扩展命名空间；**defer**＝强交互/实时/重人工，不适合现阶段 Agent 操作。

---

## 1. 文档入口与版本口径

实际查阅的官方页面（均为 2026-11-02 当日查阅）：

| 文档 | 入口 | 口径 |
|---|---|---|
| SuperMap 帮助中心总站 | https://help.supermap.com/ | 全产品线帮助聚合（iDesktopX、iServer、iObjects、iMobile、ImageX 等） |
| iDesktopX 帮助（中文，现行版） | https://help.supermap.com/iDesktopX/zh/ | 桌面主线口径；另有 1101/1110/1111/1121/1130 等版本化帮助树，功能组织基本一致 |
| iDesktopX 帮助·数据管理章 | https://help.supermap.com/iDesktopX/zh/tutorial/DataProcessing/DataManagement/DataManagement.html | 数据管理域的官方组织方式来源 |
| iDesktopX 帮助·空间分析章 | https://help.supermap.com/iDesktopx/zh/tutorial/Analyst/Analyst.html | 矢量/栅格分析的官方二级目录来源 |
| iDesktopX 帮助·栅格分析 | https://help.supermap.com/iDesktopX/zh/tutorial/Analyst/Raster/RasterAnalyst.html | 栅格九类功能来源 |
| iDesktopX 帮助·工具箱 | https://help.supermap.com/iDesktopX/zh/Tools/index.html | GPA 工具箱总说明（工具按域分类、每工具带离线帮助） |
| iDesktopX 帮助·网络分析 | https://help.supermap.com/iDesktopX/en/tutorial/Network/Network.html | 交通网络分析六类来源 |
| iDesktopX 帮助·机器学习 | https://help.supermap.com/iDesktopx/zh/SpecialFeatures/MachineLearning/ObjDetect.html 等（工具箱→机器学习→影像分析各工具页） | ML 工具链来源 |
| iDesktopX 帮助·影像处理（ImageX） | https://help.supermap.com/iDesktopx/zh/tutorial/ImageX/ProcessProductiong/ProcessIntroduction.html | DOM/正射等影像生产工作流来源 |
| iDesktopX 帮助·三维剖面/通视等 | https://help.supermap.com/iDesktopX/zh/tutorial/SceneOperation/RealspaceSpatialAnalyst/ProfileAnalyst.html 等 | 三维空间分析来源 |
| iDesktopX 2026 新特性 | https://help.supermap.com/iDesktopX/en/GettingStarted/FeatureNews/what_is_new.html | 2026/2026 Update1 增量（编辑、质检等） |
| iObjects Python（iobjectspy）文档 | https://iobjectspy.supermap.io/（站内版本 12.0.0.0）；API 参考 https://iobjectspy.supermap.io/html_zh/api/iobjectspy.html | 模块结构：data / conversion / analyst / mapping / threeddesigner / ml / enums / env / rpc；analyst 页明列 create_buffer、overlay、clip_raster 等函数 |
| iObjects Java 在线帮助（Javadoc） | https://support.supermap.com/DataWarehouse/WebDocHelp/iObjectsJava/ProgrammingReference/index-all.html | 类级证据，如 com.supermap.analyst.spatialanalyst.BufferAnalyst |
| iObjects Java/.NET 2026（12.1）下载页 | https://www.supermap.com/en-us/html/down.html | 组件现行版本口径 |
| iDesktopX 产品页（官网） | https://www.supermap.com/zh-cn/a/product/gis-iDesktopX-2025.html 、 https://www.supermap.com/zh-cn/a/product/gis-iDesktopX-2026.html | 官方功能总述：工具箱 1200+ 工具、200+ 数据处理功能等（注：2026 版产品页当日直达抓取失败，条目以 2025 版与帮助站新特性页为准） |
| iObjects 产品页（官网） | https://www.supermap.com/en-us/product/?gis-iObjects-java-2024.html（页面内含 iObjects Python 能力清单） | iObjects Python 数据管理/处理/分析能力总述来源 |
| 技术体系页（官网） | https://www.supermap.com/zh-cn/a/product/gis-tec-4-2026.html | iDesktopX CLI 等 2026 自动化新入口来源 |
| iServer 帮助·服务介绍 | https://help.supermap.com/iPortal/Service_introduce/Service_introduce.htm（iServer 服务类型表）及 iServer 产品版本及模块介绍（support.supermap.com） | 发布域服务类型与分析能力来源 |
| iServer 2026 新闻（官网） | https://www.supermap.com/zh-cn/a/news/2_5134.html | iServer 2026 官方 MCP 工具集来源 |

**版本错位提醒（影响差距判断）**：鱼鱼本机是 iDesktop 10i + iobjectspy 10.1.0，桥的 file-fallback 校准（13/13）建立在 10.1.0 上；官方文档现行口径是 iDesktopX 2026 / iobjectspy 12.0.0.0 / iObjects 12.1。下文功能全集按官方现行版计，落地时凡走 iobjectspy 的条目都需在 10.1.0 上逐项验 API 是否存在，不可直接照 12.x 文档写桥。

## 2. 功能域总览（按官方帮助的组织方式）

iDesktopX 帮助的功能组织是「选项卡功能区 + 工具箱（GPA）」双轨：同一功能常同时有功能区入口和工具箱入口（工具箱官方口径 1200+ 工具）。归并为 15 个功能域：

1. **数据管理**（帮助：数据处理→数据管理章）：工作空间/数据源/数据集三级组织、空间索引、金字塔、镶嵌数据集、流数据、数据版本。
2. **数据迁移与格式转换**：80+ 格式导入、导出、类型转换、投影转换、数据配准、服务迁移。
3. **数据编辑**（帮助：数据处理→对象编辑；2026 起独立「数据编辑」选项卡）：绘制、节点编辑、捕捉、追踪、拓扑编辑、模板编辑、AI 辅助采集。
4. **数据处理**（工具箱数据处理类，官方称 200+ 功能）：融合、化简、拓扑检查/处理、空间连接、属性处理等批量处理。
5. **矢量分析**（帮助：空间分析→矢量分析）：缓冲区、叠加、邻近、动态分段。
6. **栅格分析**（帮助：空间分析→栅格分析）：表面分析、栅格统计、矢栅转换、距离栅格、插值、水文、代数运算。
7. **影像处理**（帮助：ImageX 教程，含卫星/无人机影像线）：辐射/几何/正射校正、配准、融合、匀色、镶嵌、DOM 生产工作流。
8. **三维**（帮助：场景操作 + 三维分析选项卡）：场景与图层、三维数据处理（倾斜/S3M/点云）、三维空间分析（通视/可视域/天际线/日照/剖面等）。
9. **网络分析**（帮助：交通分析→网络分析；另含设施网络、三维网络）：最佳路径、TSP、物流配送、最近设施、服务区、选址分区、追踪。
10. **空间统计分析**（帮助：空间统计分析选项卡/工具箱同名类）：度量地理、分析模式、聚类分布、空间关系建模、抽样与推断。
11. **地图制图**（帮助：地图/专题图/布局）：图层风格、六类专题图、布局制图与输出、地图瓦片。
12. **服务发布与在线分析**（iServer 体系 + 桌面端发布流程）：REST 地图/数据/空间分析/交通网络/交通换乘/三维服务、OGC 服务、分布式分析、官方 MCP 工具集。
13. **机器学习与 AI**（帮助：特色功能→机器学习；视图→AI 助理）：深度学习影像解译全流程、图片分析、点云分类、AI 助理。
14. **处理自动化与扩展**：GPA 模型构建、Python 工具、iDesktopX CLI。
15. **特色功能**：视频地图、知识图谱（帮助总述列名，细节目录本次未逐项展开）。

自动化入口的总体格局：**iobjectspy**（Python 组件，桥的现行通道）覆盖数据、转换、分析、制图、三维设计、ML 六大模块；**iObjects Java/.NET** 类库与之同构且更全（分析类在 com.supermap.analyst.* 包下）；**iDesktopX CLI**（2026 新增）把数据导入、制图、处理、分析、三维场景封装为命令行；**iServer REST** 是服务侧入口；纯桌面交互功能标注「仅桌面」。

## 3. 工具/功能级清单

### 3.1 数据管理（16 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 工作空间打开/保存/另存 | 管理 .smwu/.sxwu 工程文件 | iobjectspy.Workspace / WorkspaceConnectionInfo（桥已用） | core |
| 工作空间目录管理 | 组织空间内数据源/地图/布局/场景 | iobjectspy.data（Workspace 类） | core |
| 数据源新建/打开/删除 | 文件/数据库/Web 三类引擎（SDX+）的数据容器 | iobjectspy.data（Datasource、open_datasource） | core |
| 数据源复制/紧缩/排序 | 数据源维护操作 | iObjects Data 包 Datasources 类；iobjectspy 部分支持 | core |
| 新建数据集（16 种类型） | 点/线/面/文本/CAD/模型/属性表/三维/LAS/栅格/影像/镶嵌/视频等 | iobjectspy.data（Datasource.create_dataset） | core |
| 数据集管理 | 复制/重命名/删除/编码方式设置 | iobjectspy.data（Dataset 类族） | core |
| 属性表浏览与 SQL 查询 | 查看属性、按条件检索记录 | iobjectspy.data（Recordset、QueryParameter） | core |
| 空间索引管理 | 四叉树/R 树/图幅/动态索引的建与重建 | iObjects Data 包；iDesktop 桌面 | extension |
| 影像金字塔管理 | 栅格/影像数据集建/删金字塔 | iObjects Data 包；工具箱 | extension |
| 镶嵌数据集管理 | 海量影像的镶嵌数据集创建与维护 | iobjectspy.data（DatasetMosaic 相关） | extension |
| 流数据管理 | 配置流数据服务、收发实时流数据 | iDesktop 桌面；iServer 流数据服务 | defer |
| 数据版本管理 | PostGIS/Yukon 注册版本、多人协同编辑、同步存档 | iDesktop 桌面；iObjects Data 包 | extension |
| 数据库用户与权限管理 | PostGIS/Yukon 建用户/角色并授权 | 仅桌面（iDesktopX 数据管理章） | defer |
| 数据库事务管理 | PostGIS 事务完整性管理 | iObjects Data 包 | extension |
| 云存储影像加载 | 对象存储中影像的查看与加载、瓦片存云 | iDesktop 桌面 | defer |
| iServer 服务器管理 | 连接 iServer、按权限浏览服务目录并加载 | 桌面操作（桥 discover 已有现场探测） | extension |

### 3.2 数据迁移与格式转换（8 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 数据导入（80+ 格式） | SHP/DWG/GeoPackage/GeoJSON/CSV 等导入为 UDBX | iobjectspy.conversion（import_* 系列，如 VCT 导入） | core |
| 数据导出 | 数据集导出为外部格式文件 | iobjectspy.conversion（export_* 系列） | core |
| 类型转换（工具箱） | CAD↔GIS、文本↔点等格式族间转换 | 工具箱（GPA）；iobjectspy.conversion 部分 | core |
| 几何类型转换 | 点/线/面等几何类型互转 | 工具箱；iObjects Data 包 | core |
| 投影转换 | 数据集坐标系转换（11 种方法，含四参数/七参数） | iobjectspy（投影变换接口）；iObjects Data 包 PrjCoordSys | core |
| 数据配准 | 矢量/栅格配准到参考数据 | 工具箱；iDesktop 桌面配准 | extension |
| 数据迁移 | 跨数据库的数据/模式迁移（iXConverter 体系） | iDesktop 桌面迁移模块 | extension |
| 服务迁移 | 其他平台服务迁移发布到 iServer | iDesktopX 帮助·数据迁移→服务迁移页 | extension |

### 3.3 数据编辑（13 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 对象绘制 | 点/线/面/文本/参数化对象采集 | 仅桌面（对象操作选项卡） | defer |
| 节点编辑 | 增删移几何节点改形 | 仅桌面 | defer |
| 对象运算编辑 | 分割/合并/擦除等编辑级对象运算 | 仅桌面（批量同类操作见叠加分析） | defer |
| 端点修整 | 线的修剪/延伸对齐 | 仅桌面 | defer |
| 捕捉设置 | 节点/边/交点等捕捉保证连接精度 | 仅桌面 | defer |
| 追踪矢量化 | 沿线/面或栅格半自动追踪采集 | 仅桌面 | defer |
| 拓扑编辑 | 拓扑边/节点联动编辑（对齐边、修整、编辑节点） | 仅桌面 | defer |
| 模板编辑 | 按要素类别模板快速采编 | 仅桌面 | defer |
| 自动生成面 | 点选闭合区域自动构面（2026 新增） | 仅桌面 | defer |
| AI 辅助绘面 | SAM 点击影像自动提取地物轮廓（2026） | 仅桌面（模型在 iobjectspy.ml 侧有推理接口） | defer |
| 打断相交线 | 选定线对象在交点批量打断（2026） | 工具箱同名处理工具可批量执行 | extension |
| 延续对象 | 从线末端延续编辑 | 仅桌面 | defer |
| FileGDB/GeoPackage 直连编辑 | 不经转换直接编辑开放格式 | 桌面；iObjects Data 包引擎 | extension |

### 3.4 数据处理（16 条，工具箱数据处理类，官方称 200+ 功能，此处列主干）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 融合（Dissolve） | 按属性值合并相邻面 | iobjectspy.analyst；iObjects SpatialAnalyst | core |
| 化简/抽稀 | 线面几何抽稀简化 | 工具箱；iObjects Analyst | core |
| 多边形聚合 | 相邻/近邻面聚合为整体 | iobjectspy.analyst | core |
| 提取中心线 | 面状线状地物（道路/河流）中心线提取 | 工具箱；iObjects Analyst | extension |
| 碎片面消除 | 小碎面并入邻接大面 | 工具箱 | core |
| 建筑物规整化 | 建筑轮廓直角化/规整 | iObjects Python 产品页明列；iDesktop 工具箱 | extension |
| 随机点生成 | 范围内生成随机点 | iobjectspy.analyst | core |
| 点到线垂足 | 计算点到线的垂足 | iObjects Python 产品页明列 | extension |
| 几何平滑 | 线面平滑处理 | iobjectspy.analyst | core |
| 几何重采样 | 按间距/节点数重采样几何 | iobjectspy.analyst | core |
| 数据接边 | 相邻图幅边缘对象接边 | 工具箱 | extension |
| 拓扑检查 | 规则检查（面重叠等）+自定义方案+属性质检（2026 扩规） | 工具箱；iObjects TopologyValidator 类 | core |
| 拓扑处理 | 线拓扑处理、拓扑构面、拓扑构网 | iobjectspy.analyst（拓扑构面明列） | core |
| 空间连接 | 按空间关系连接属性 | 工具箱；iObjects Analyst | core |
| 属性处理 | 字段计算、属性连接、字符串查找/分割/替换、计数器 | 工具箱属性工具；iObjects Recordset | core |
| 渔网创建与标记 | 生成渔网格网并标记（2026 新增） | 工具箱 | extension |


### 3.5 矢量分析（15 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 缓冲区分析 | 点线面按距离/字段生成单重缓冲 | iobjectspy.analyst.create_buffer；iObjects BufferAnalyst；iServer REST | core |
| 多重缓冲区分析 | 多级距离环带缓冲 | iobjectspy.analyst；iObjects BufferAnalyst | core |
| 叠加·裁剪（Clip） | 用面裁取源数据 | iobjectspy.analyst.overlay；iObjects OverlayAnalyst | core |
| 叠加·擦除（Erase） | 擦除与叠加面重叠部分 | 同上 | core |
| 叠加·求交（Intersect） | 取两层交集并综合属性 | 同上 | core |
| 叠加·合并（Union） | 两面层合并重组拓扑 | 同上 | core |
| 叠加·同一（Identity） | 保留源全域叠加求交属性 | 同上 | core |
| 叠加·对称差（XOR） | 取两层非重叠部分 | 同上 | core |
| 叠加·更新（Update） | 用叠加层替换重叠区 | 同上 | core |
| 多层叠加 | 多面层批量合并/求交 | iDesktop 工具箱（叠加工具页明列 9 式含多层两种） | core |
| 泰森多边形 | 由点生成邻近多边形 | iobjectspy.analyst；iObjects 邻近分析 | core |
| 最近距离计算 | 点/线/面间最近距离 | iObjects 邻近分析；iServer REST 空间分析 | core |
| 创建路由 | 由线数据集构建动态分段路由 | iObjects 线性参考（DynamicSegmentation） | extension |
| 路由标定与事件表 | 校准路由、事件表生成与管理 | iObjects 线性参考 | extension |
| 地址匹配（地理编码） | 地址↔坐标匹配 | iObjects Python 产品页明列地址匹配模块 | extension |

### 3.6 栅格分析（23 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 栅格分析环境设置 | 结果范围/分辨率/裁剪范围统一设置 | iObjects TerrainAnalyst 环境参数 | core |
| 提取等值线 | 由栅格表面提取等值线 | iobjectspy.analyst；iObjects SurfaceAnalyst | core |
| 提取等值面 | 由栅格表面提取等值面 | 同上 | core |
| 坡度分析 | 计算像元坡度 | iObjects TerrainAnalyst；iServer REST 地形分析 | core |
| 坡向分析 | 计算像元坡向 | 同上 | core |
| 填挖方 | 两期表面间土方量计算 | iObjects TerrainAnalyst | core |
| 栅格阴影（山体阴影） | 假想光源生成地貌阴影图 | iObjects 表面分析 | extension |
| 栅格统计（基本/邻域） | 像元值统计与邻域统计 | iobjectspy.analyst；iObjects GridAnalyst | core |
| 区域统计 | 按分区统计栅格值 | iobjectspy.analyst | core |
| 栅格直方图 | 像元值分布直方图 | 桌面；iObjects GridAnalyst | extension |
| 栅格矢量化 | 栅格转点/线/面 | iobjectspy.analyst（矢栅转换） | core |
| 矢量栅格化 | 矢量转栅格（含栅格细化） | 同上 | core |
| 栅格裁剪 | 按区域/矩形裁剪栅格影像 | iobjectspy.analyst.clip_raster | core |
| 距离栅格 | 直线/耗费距离与最短表面路径 | iObjects TerrainAnalyst（DistanceAnalyst） | core |
| 插值·距离反比（IDW） | 采样点插值成面 | iobjectspy.analyst（插值分析明列） | core |
| 插值·克里金 | 普通/简单/泛克里金插值 | iobjectspy.analyst；iObjects InterpolationAnalyst | core |
| 插值·样条函数 | 径向基函数/障碍样条插值 | iObjects InterpolationAnalyst | extension |
| 栅格代数运算 | 多栅格四则/函数代数运算 | iobjectspy.analyst（栅格代数明列） | core |
| 重分类 | 像元值按规则重新分级 | iobjectspy.analyst | core |
| 水文·填充伪洼地 | DEM 填洼预处理 | iObjects HydrologyAnalyst | core |
| 水文·流向与累积汇水量 | D8 流向与汇流累积 | 同上 | core |
| 水文·河网与流域提取 | 提取河网、流长、流域分割 | 同上 | core |
| 查询栅格值 | 鼠标点查像元值 | 仅桌面 | defer |

### 3.7 影像处理（13 条，ImageX 线）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 辐射校正 | 辐射定标/校正预处理 | ImageX 工作流步骤（桌面流程） | extension |
| 几何校正 | 控制点几何纠正 | ImageX 几何校正组 | extension |
| 正射校正 | 基于 RPC + DEM 消除畸变生成正射 | ImageX 正射校正生产工作流 | extension |
| 影像配准 | 全色基准配准多光谱 | ImageX 影像配准 | extension |
| 影像融合 | 全色锐化融合全色与多光谱 | ImageX 融合生产工作流 | extension |
| 影像匀色 | 模板/自适应匀色统一色调 | 工具箱影像匀色工具（GPA 进程） | extension |
| 镶嵌线构建 | 自动生成无缝镶嵌线 | ImageX 工作流步骤 | extension |
| 影像镶嵌与输出 | 整幅/标准分幅/矢量裁剪输出 | 工具箱影像镶嵌工具 | extension |
| DOM 生产工作流 | 原始影像到 DOM 的串联自动化生产 | ImageX 流程（可重复执行的工作流） | extension |
| 无人机影像处理 | 无人机数据生成正射影像/DSM | ImageX 无人机数据处理工作流 | extension |
| 影像增强/真彩色输出 | 拉伸增强输出真彩色 | ImageX 工作流步骤 | extension |
| DSM/DEM 镶嵌 | 多幅 DSM/DEM 整合 | ImageX 产品介绍页明列 | extension |
| 镶嵌数据集影像管理 | 海量影像组织与快速显示 | iobjectspy.data | extension |

### 3.8 三维（20 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 场景与图层管理 | 场景新建、图层添加（含天地图/OSM/STK 在线底图） | iobjectspy（场景操作接口有限）；桌面为主 | extension |
| 地形加载与显示 | TIN/栅格地形加载夸张等 | 桌面；iObjects Realspace | extension |
| 地形操作 | TIN 地形裁剪/挖洞/镶嵌/拉伸闭合体 | GPA 三维工具；iobjectspy.threeddesigner | extension |
| 倾斜摄影入库 | OSGB 倾斜数据生成 S3M 瓦片 | GPA 工具（倾斜入库） | extension |
| 倾斜模型操作 | 裁剪/挖洞/镶嵌/压平/单体化查询 | GPA 工具；Hi-Fi 3D SDK | extension |
| S3M 瓦片生成 | 模型/矢量/点云/体数据生成 S3M 3.01 瓦片 | GPA 工具；iobjectspy.threeddesigner | extension |
| 3D Tiles 转 S3M | 3D Tiles 数据格式转换 | GPA 工具 | extension |
| S3M 版本升级与管理 | 瓦片版本升级、MongoDB 存储、属性查询 | GPA 工具；桌面 S3M 瓦片管理 | extension |
| 点云处理 | 点云生成瓦片、外挂模型 | GPA 工具 | extension |
| 三维量算 | 距离/高度/面积量算 | iObjects Realspace；桌面 | extension |
| 通视分析 | 两点/多点间可视性判断 | iObjects Realspace SpatialAnalyst（GPU） | extension |
| 可视域分析 | 观察点可视范围（含动态可视域） | 同上 | extension |
| 天际线分析 | 场景天际线提取 | 同上（产品页明列） | extension |
| 日照/阴影分析 | 日照时长与三维阴影 | 同上 | extension |
| 开敞度分析 | 点位开敞度计算 | Hi-Fi 3D SDK / Realspace | extension |
| 剖面分析 | 沿线地形/模型剖面生成 | 三维分析选项卡（桌面）；结果可存点数据集 | extension |
| 三维缓冲区 | 三维对象缓冲 | iObjects Realspace（BufferAnalyst3DParameter） | extension |
| 三维布尔运算 | 三维集合对象布尔运算 | iServer REST 空间分析；iObjects Realspace | extension |
| 场景飞行 | 自定义飞行路线浏览 | 仅桌面 | defer |
| 视频投放 | 视频投放到三维场景 | Hi-Fi 3D SDK | defer |

### 3.9 网络分析（12 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 构建网络数据集 | 由线数据集拓扑建网络数据集 | iObjects NetworkAnalyst（BuildNetworkDataset） | extension |
| 网络分析环境设置 | 权值字段、结点/弧段标识、转向表等 | iObjects TransportationAnalyst 参数 | extension |
| 最佳路径分析 | 多站点最小阻力路径 + 路径导引 | iObjects TransportationAnalyst；iServer REST 交通网络分析 | core |
| 旅行商分析（TSP） | 单车巡回最优顺序 | 同上 | extension |
| 物流配送（MTSP/VRP） | 多车配送路径优化 | 同上 | extension |
| 最近设施分析 | 事件点找最近设施及路径 | 同上 | core |
| 服务区分析 | 中心点服务范围（网络+面） | 同上 | core |
| 选址分区分析 | 候选点中选最优设施布局 | 同上 | extension |
| 连通性分析 | 网络弧段连通性判断 | iObjects FacilityAnalyst | extension |
| 设施网络追踪 | 上溯/下溯、共同上下游追踪 | iObjects FacilityAnalyst | extension |
| 三维最佳路径 | 三维网络最小阻力路径 | 三维网络分析（桌面/服务） | extension |
| 三维网络上下游追踪 | 三维场景管网追踪 | iServer 三维网络分析 REST 服务 | extension |

### 3.10 空间统计分析（18 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 平均中心 | 要素分布平均中心 | iObjects SpatialStatistics | core |
| 中位数中心 | 抗异常值的中位中心 | 同上 | core |
| 中心要素 | 最居中要素识别 | 同上 | core |
| 方向分布 | 标准差椭圆方向分布 | 同上 | core |
| 线性方向平均值 | 线要素方向趋势 | 同上 | extension |
| 平均最近邻 | 点分布集聚/离散判定 | 同上 | core |
| 空间自相关 | 全局 Moran's I 模式判定 | 同上 | core |
| 高低值聚类 | 全局 G 指数高低值集聚 | 同上 | extension |
| 增量空间自相关 | 多距离自相关峰值探索 | 同上 | extension |
| 热点分析 | 局部 G* 热点/冷点 | 同上 | core |
| 优化的热点分析 | 自动聚合派生参数的热点分析 | 同上 | extension |
| 聚类和异常值分析 | 局部 Moran 热点/冷点/异常值 | 同上 | core |
| 密度聚类 | 基于密度的点聚类 | iobjectspy.analyst（密度聚类明列） | extension |
| 地理探测器 | 空间分异因子探测 | iObjects SpatialStatistics（2023 产品页明列） | extension |
| 普通最小二乘法（OLS） | 全局线性回归建模 | 同上 | extension |
| 地理加权回归（GWR） | 局部加权回归建模 | 同上 | extension |
| 生成空间权重矩阵 | 生成 .swmb 权重文件 | 工具箱空间统计类 | extension |
| 抽样与空间推断 | 随机抽样/B-SHADE 抽样与预测、单点地域估计 | 产品页明列（工具箱） | extension |

### 3.11 地图制图（13 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 图层风格设置 | 符号、颜色、线型面填充设置 | iobjectspy.mapping（Layer 风格）；桥 set_layer_visible 仅显隐 | core |
| 地图属性设置 | 背景、比例尺、色彩模式、抗锯齿、动态投影 | iobjectspy.mapping.Map | core |
| 单值专题图 | 按字段单值分符号渲染 | iobjectspy.mapping（ThemeUnique） | core |
| 分段专题图 | 按字段分段渲染（含栅格分段） | iobjectspy.mapping（ThemeRange） | core |
| 标签专题图 | 字段标注注记（含标签矩阵） | iobjectspy.mapping（ThemeLabel）；桥 make_label_thematic 已覆盖基础版 | core |
| 统计专题图 | 多字段统计图表专题 | iobjectspy.mapping（ThemeGraph） | core |
| 等级符号专题图 | 按值分级符号大小 | iobjectspy.mapping（ThemeGraduatedSymbol） | core |
| 点密度专题图 | 点密度表现数量分布 | iobjectspy.mapping（ThemeDotDensity） | core |
| 统计图表联动 | 图表与地图/属性表联动展示 | 桌面为主 | defer |
| 布局制图 | 布局中放地图、图例、比例尺、指北针、标题 | iObjects Mapping（Layout 类）；桌面为主 | extension |
| 布局输出 | 布局输出图片/PDF | iObjects Mapping；iDesktopX CLI 制图能力 | extension |
| 地图导出图片 | 当前地图出图 PNG 等 | iobjectspy.mapping（桥 export_map_image 已覆盖） | core |
| 地图瓦片生成 | 由地图生成缓存瓦片供服务使用 | 工具箱/桌面切图；iServer 分布式切图 | extension |

### 3.12 服务发布与在线分析（13 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 发布工作空间为服务 | 桌面端一键发布工作空间到 iServer | iDesktopX 桌面发布流程（Publish 章） | extension |
| 地图 REST 服务 | 地图浏览、查询、量算、专题图 | iServer REST（map） | core |
| 数据 REST 服务 | 数据集/要素/字段的查与编辑 | iServer REST（data） | core |
| 空间分析 REST 服务（基础） | 缓冲/叠加/邻近/三维查询/布尔 | iServer REST（spatialAnalyst，datasetBufferResults 等） | core |
| 空间分析 REST 服务（高级） | 表面/插值/密度/栅格代数/地形/日照 | iServer REST（扩展模块） | extension |
| 交通网络分析 REST 服务 | 路径/TSP/配送/最近设施/服务区/选址 | iServer REST（networkAnalyst） | extension |
| 交通换乘分析 REST 服务 | 公交换乘方案与站点查询 | iServer REST（trafficTransferAnalyst） | extension |
| 三维 REST 服务 | 场景/图层/三维数据获取 | iServer REST（realspace3D） | extension |
| 三维网络分析 REST 服务 | 三维上下游追踪等 | iServer REST | extension |
| OGC 标准服务 | WMS/WMTS/WFS/WCS/WPS 发布 | iServer 服务管理 | core |
| 分布式分析服务 | 大数据聚合、密度、区域汇总、插值（Spark） | iServer Distributed Analyst REST（POST 建任务） | extension |
| 地址匹配服务 | 地址解析与匹配（云服务含正逆地理编码） | iServer/Online REST | extension |
| iServer MCP 工具集 | 官方把地图/数据/网络/空间分析/三维封装为智能体工具（2026） | iServer 2026（官方新闻明列） | extension |

### 3.13 机器学习与 AI（15 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 训练数据生成 | 影像+矢量标注切分生成训练样本（六种用途） | 工具箱；iobjectspy.ml | extension |
| 模型训练 | 六类解译任务的模型训练（GPU 单卡/多卡） | 工具箱；iobjectspy.ml | defer |
| 目标检测 | 影像多类目标框检测 | 工具箱；iobjectspy.ml（vision） | extension |
| 二元分类 | 像元级二分类提取 | 同上 | extension |
| 地物分类 | 多类地物语义分类 | 同上 | extension |
| 场景分类 | 影像场景标签分类（网格结果） | 同上 | extension |
| 对象提取 | 特定地物对象提取（如建筑物） | 同上（iobjectspy.ai.recognition.extract_region，旧版命名） | extension |
| 通用变化检测 | 双时相变化提取 | 工具箱；iobjectspy.ml | extension |
| 模型评估 | 检测/分类/变化检测模型精度评估 | 工具箱 | extension |
| 推理后处理 | 推理结果矢量化/清理 | 工具箱（产品页称全流程工具含后处理） | extension |
| 图片分类 | 普通图片的分类/检测（图片分析） | 工具箱图片分析 | extension |
| 点云分类 | 深度学习点云分类（电力场景等，2025 新增） | 工具箱 | extension |
| 影像超分辨率重建 | 低分影像超分 | 工具箱（产品页明列） | extension |
| 预训练模型与大模型 | 林地/耕地/水体/建筑等开箱模型、LIM 大模型、G-SAM 分割 | 工具箱（.sdm 模型文件） | extension |
| AI 助理 | 自然语言智能问答/智能制图/智能建模 | iDesktopX 桌面（视图→AI 助理） | defer |

### 3.14 处理自动化与扩展（4 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| GPA 模型构建 | 工具拖拽连成处理模型批量执行 | iDesktopX 桌面建模器；模型可导出 Python 脚本 | extension |
| 自定义 Python 工具 | 写 Python 工具进工具箱、可入 GPA 流程 | iDesktopX Python 窗口/工具 | extension |
| iDesktopX CLI | 命令行封装探针、三维、导入、制图、处理、分析、流程编排（2026） | CLI 本身即自动化入口 | extension |
| 工具箱统一调用面 | 1200+ GPA 工具的统一参数化执行 | 工具箱进程工厂（Tools/Gtprocessfactory 帮助页体系） | extension |

### 3.15 特色功能（2 条）

| 功能 | 作用 | 自动化入口 | 判断 |
|---|---|---|---|
| 视频地图 | 视频数据集、视频地图、视频目标检测（80 类） | 桌面视频分析选项卡 | defer |
| 知识图谱 | 空间知识图谱构建与应用（帮助总述列名） | 本次未展开其帮助子目录，细节待补查 | defer |

**清单合计：15 个功能域、201 条功能。**

## 4. 差距：现有 SuperMap 桥 vs 官方全集

现有桥（supermap 包，manifest 实测 13 个工具；file-fallback 经 iobjectspy 10.1.0 实机校准 13/13，live 模式未验证）：

- 读（7）：ping、discover、workspace_info、list_datasources、list_datasets、list_maps、list_layers
- 视图（2）：set_layer_visible、zoom_to_dataset
- 写（4，均实验性/带 confirm）：add_dataset_to_map、make_label_thematic、export_map_image、save_workspace

按功能域量化（桥工具映射到官方功能条目约 11 条，占 201 条 ≈ 5%）：

| 功能域 | 官方条数 | 桥已覆盖 | 缺口说明 |
|---|---|---|---|
| 数据管理 | 16 | 约 5（工作空间打开/保存、数据源/数据集/地图/图层列举） | 无新建/删除/复制数据集、无属性查询、无索引/金字塔 |
| 数据迁移与转换 | 8 | 0 | 导入导出、投影转换全缺——数据进出平台的门没开 |
| 数据编辑 | 13 | 0 | 全为交互功能，本就不规划（defer 为主） |
| 数据处理 | 16 | 0 | 融合/拓扑检查等批量处理全缺 |
| 矢量分析 | 15 | 0 | 缓冲/叠加等核心分析全缺（平台最大缺口） |
| 栅格分析 | 23 | 0 | 坡度/代数/重分类/水文全缺 |
| 影像处理 | 13 | 0 | ImageX 工作流全缺 |
| 三维 | 20 | 0（discover 仅探测场景信息） | S3M/倾斜/三维分析全缺 |
| 网络分析 | 12 | 0 | 路径/服务区等全缺 |
| 空间统计 | 18 | 0 | 全缺 |
| 地图制图 | 13 | 约 3（标签专题基础版、导出图片、图层显隐） | 单值/分段/统计等专题图、布局全缺 |
| 服务发布 | 13 | 0 | 发布与 iServer 服务调用全缺 |
| 机器学习 | 15 | 0 | iobjectspy.ml 全缺 |
| 处理自动化 | 4 | 0 | GPA/CLI 未接 |
| 特色功能 | 2 | 0 | 不规划 |

另有**版本缺口**：桥的校准基线是 iobjectspy 10.1.0（iDesktop 10i 时代），官方现行 12.x 的 analyst/ml/threeddesigner 接口与 10.1.0 不完全同名（如对象提取在 10i 为 iobjectspy.ai.recognition），升级功能前须先决定桥的目标版本（继续 10.1.0 本机校准，还是迁 iDesktopX + 12.x）。

## 5. 升级建议（按收益排序，前 8 条）

1. **矢量分析三件套：缓冲区 + 叠加七式 + 泰森多边形**（core）——Agent 最高频的真实干活能力，iobjectspy.analyst 已有 create_buffer/overlay 成熟函数，纯文件模式即可跑、与现有 file-fallback 校准路径同轨，收益/风险比最高。
2. **数据导入/导出 + 投影转换**（core）——平台 B 阶段数据层（STAC/PostGIS/GeoServer 生态）与 SuperMap 互通的门；conversion 模块函数齐备，且是其他一切分析的前置。
3. **栅格基础包：坡度/坡向、栅格代数、重分类、区域统计、栅格裁剪**（core）——鱼鱼遥感主场的刚需，clip_raster 等函数现成；与 MVEO/土地覆盖方向直接复用。
4. **专题图补全：单值 + 分段 + 统计 + 等级符号**（core）——桥已有标签专题的同构实现，mapping 模块扩展成本低，出图能力立刻从"能看"变"能交付"。
5. **数据集写操作与属性查询：新建/复制/删除数据集 + SQL 属性查询 + 字段计算**（core）——把桥从只读查看器升级为工作站；沿用现有 confirm 闸模式即可控风险。
6. **网络分析三件套：最佳路径 + 服务区 + 最近设施**（core 候选、先 extension 落地）——演示与服务类场景价值高；可走 iObjects TransportationAnalyst 或 iServer REST，先在一家跑通再谈统一动词。
7. **机器学习推理三件套：地物分类 + 目标检测 + 变化检测（只推理不训练）**（extension）——与遥感方向、预训练 .sdm 模型结合，是 SuperMap 相对其他家的差异化能力；训练留 defer。
8. **发布与官方 MCP 对接评估：工作空间发布 iServer + iServer 2026 官方 MCP 工具集互通**（extension）——官方已把服务能力封装成智能体工具，平台应先评估复用/互通而非自建发布链，避免重复造轮子；同时关注 iDesktopX CLI 作为新的本机自动化通道（可替代部分 in-app 桥探测）。


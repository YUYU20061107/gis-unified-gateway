# QGIS 能力普查补查：桌面功能域 / PyQGIS Cookbook / GRASS·SAGA 等外部提供者（3.40 英文版）

- 版本口径：QGIS 3.40，英文版官方文档（docs.qgis.org / qgis.org 域名内页面）
- 抓取日期：2026-11-02
- 取源纪律：本文件只依据下文列明的、实际打开的 3.40 官方页面；未在这些页面中出现的内容一律写「3.40 官方用户指南未收录」或「在实际打开的官方页面中未见」，不以记忆或非官方来源补写。
- 总入口（实际打开）：https://docs.qgis.org/3.40/en/docs/index.html

---

## 一、桌面功能域总览（QGIS Desktop User Guide / Manual 3.40）

### 1.1 实际打开的官方页面

| 用途 | URL | 抓取日期 |
|---|---|---|
| 文档总入口 | https://docs.qgis.org/3.40/en/docs/index.html | 2026-11-02 |
| 用户指南目录页（一级/二级章节全表） | https://docs.qgis.org/3.40/en/docs/user_manual/index.html | 2026-11-02 |

该目录页的 27 个一级章为：1. Getting Started；2. Working with Project Files；3. QGIS GUI；4. The Browser panel；5. QGIS Configuration；6. Working with Projections；7. Visualizing Maps；8. General Tools；9. Level up with Expressions；10. The Style Library；11. Managing Data Source；12. Working with Vector Data；13. Working with Raster Data；14. Working with Mesh Data；15. Working with Vector Tiles；16. Working with Point Clouds；17. Working with 3D Tiles；18. Laying out the maps；19. Working with OGC / ISO protocols；20. Working with GPS Data；21. Authentication System；22. GRASS GIS Integration；23. QGIS processing framework；24. Processing providers and algorithms；25. Plugins；26. Appendices；27. Literature and Web References。另在总入口页同一「For Users」组内并列 QGIS Server Guide/Manual (3.40)（独立手册，9 章，见下表最后一行）。

### 1.2 桌面功能域清单（25 行）

格式：域名｜指南对应章节｜主要能力一句话｜自动化入口（PyQGIS / Processing / 仅桌面）。

| # | 域名 | 指南对应章节（含二级节） | 主要能力（一句话） | 自动化入口 |
|---|---|---|---|---|
| 1 | 入门与工程文件 | 1. Getting Started（1.1 安装、1.2 启停、1.3 示例会话加载栅格/矢量）；2. Working with Project Files（2.1 工程介绍、2.2 断链路径处理、2.3 生成输出） | 安装启动、创建/打开/保存工程并处理数据源断链、产生工程输出。 | PyQGIS（Cookbook 2. Loading Projects） |
| 2 | GUI 框架与浏览器面板 | 3. QGIS GUI（3.1 菜单栏、3.2 面板与工具栏、3.3 状态栏）；4. The Browser panel（4.1 可从浏览器打开/运行的资源、4.2 浏览器顶层条目） | 桌面主界面、面板/工具栏/状态栏与资源浏览器（文件、数据库、服务、工程等入口）。 | 仅桌面为主；PyQGIS 可操作界面元素（Cookbook 21. Cheat sheet 的 User Interface / Toolbars / Menus） |
| 3 | 配置与工程属性 | 5. QGIS Configuration（5.1 Options、5.2 User Profiles、5.3 Project Properties、5.4 Customization、5.5 快捷键、5.6 高级设置运行） | 全局选项、用户配置档、工程属性、界面定制与快捷键管理。 | PyQGIS（Cookbook 12. Reading And Storing Settings；21.2 Settings） |
| 4 | 投影与坐标参考系 | 6. Working with Projections（6.1 概览、6.2 图层 CRS、6.3 工程 CRS、6.4 CRS 选择器、6.5 自定义 CRS、6.6 基准变换） | 图层/工程 CRS 设置、自定义 CRS 与基准变换。 | PyQGIS（Cookbook 8. Projections Support） |
| 5 | 地图可视化总览（2D / 3D / 剖面入口） | 7. Visualizing Maps（7.1 2D Map View、7.2 3D Map View、7.3 Elevation Profile View） | 2D 地图视图、3D 地图视图与高程剖面视图的显示与导航入口。 | PyQGIS（Cookbook 9. Using the Map Canvas，含画布嵌入/地图工具；3D 视图本身以桌面操作为据，Cookbook 目录未单列 3D 视图章） |
| 6 | 通用工具 | 8. General Tools（8.1 上下文帮助、8.2 面板、8.3 嵌入外部工程图层、8.4 与要素交互、8.5 保存/分享图层属性、8.6 数据文档化、8.7 变量、8.8 认证、8.9 通用控件） | 要素交互、跨工程嵌入图层、样式/属性的保存分享、变量与数据说明等日常工具集。 | 仅桌面为主；变量/表达式部分可经 PyQGIS |
| 7 | 表达式 | 9. Level up with Expressions（9.1 Expressions、9.2 List of functions） | 用表达式做数据定义覆盖、筛选、计算与标注/样式驱动，附完整函数清单。 | PyQGIS + Processing（Cookbook 11. Expressions, Filtering and Calculating Values；Processing 模型工具含 Calculate expression） |
| 8 | 样式库、符号化与标注 | 10. The Style Library（10.1 Style Manager、10.2 Symbol Selector、10.3 Setting a label、10.4 Creating 3D Symbols）；各数据章的 Properties Dialog 另含本类图层的符号化/标注设置（如 12.1、13.1、14.3、15.3、16.2、17.2） | 符号管理与选择、标注设置、3D 符号创建，以及按图层类型细化的渲染属性。 | PyQGIS（Cookbook 5.2 Renderer、6.8 Appearance (Symbology) of Vector Layers） |
| 9 | 数据源管理 | 11. Managing Data Source（11.1 Opening Data、11.2 Creating Layers、11.3 Georeferencer、11.4 Exploring Data Formats and Fields） | 打开各类数据、新建图层、影像配准（Georeferencer）、探查格式与字段。 | PyQGIS（Cookbook 3. Loading Layers）；配准以仅桌面为主 |
| 10 | 矢量数据：属性表、编辑与连接 | 12. Working with Vector Data（12.1 Vector Properties Dialog、12.2 Working with the Attribute Table、12.3 Editing、12.4 Connecting and Editing Data Across Layers） | 矢量属性对话框、属性表操作、几何/属性编辑与数字化、跨图层连接与联合编辑。 | PyQGIS + Processing（Cookbook 6. Using Vector Layers：迭代、选择、修改、创建、空间索引、符号化） |
| 11 | 栅格数据 | 13. Working with Raster Data（13.1 Raster Properties Dialog、13.2 Raster Analysis） | 栅格渲染/属性设置与栅格分析。 | PyQGIS + Processing（Cookbook 5. Using Raster Layers：详情、渲染器、查值、编辑栅格数据） |
| 12 | 网格数据（Mesh） | 14. Working with Mesh Data（14.1 什么是 mesh、14.2 支持格式、14.3 Mesh Dataset Properties、14.4 Editing a mesh layer、14.5 Mesh Calculator） | 时序/数值模拟类网格数据的显示、编辑与 Mesh Calculator 计算。 | Processing 为主（24.1 QGIS 提供者含 Mesh 一组算法）；Cookbook 目录未单列 Mesh 章 |
| 13 | 矢量瓦片 | 15. Working with Vector Tiles（15.1 什么是 Vector Tiles、15.2 支持格式、15.3 Vector Tiles Dataset Properties） | 矢量瓦片数据的加载、样式与数据集属性。 | Processing（24.1 含 Vector Tiles 一组）；桌面显示为主 |
| 14 | 点云 | 16. Working with Point Clouds（16.1 Introduction to Point Clouds、16.2 Point Clouds Properties、16.3 Virtual point cloud） | 点云加载、分类/渲染等属性设置与虚拟点云（VPC）。 | Processing（24.1 含 Point Cloud Conversion / Data Management / Extraction 三组） |
| 15 | 三维瓦片（3D Tiles） | 17. Working with 3D Tiles（17.1 What are 3D Tiles?、17.2 3D Tiles Properties） | 3D Tiles 数据集的加载与属性/显示设置，主要在 3D 视图中使用。 | Processing（24.1 含 3D Tiles 一组：B3DM↔GLTF 等转换） |
| 16 | 打印布局、图册与报告 | 18. Laying out the maps（18.1 Print Layout 概览、18.2 Layout Items、18.3 Creating an Output、18.4 Creating a Report） | 打印布局编排与导出、按要素批量出图的报告/图册类输出。 | PyQGIS + Processing（Cookbook 10. Map Rendering and Printing，含 10.3 Output using print layout；24.1 Cartography 组含 Export atlas layout as image/PDF、Export print layout as image/PDF 等） |
| 17 | OGC / ISO 协议客户端 | 19. Working with OGC / ISO protocols（19.1 WMS/WMTS Client、19.2 WCS Client、19.3 WFS and WFS-T Client、19.4 SensorThings） | 以客户端身份接入 WMS/WMTS、WCS、WFS/WFS-T 与 SensorThings 服务。 | 仅桌面为主（图层加载可经 PyQGIS 3. Loading Layers 泛化处理） |
| 18 | GPS / GNSS 数据 | 20. Working with GPS Data（20.1 Introducing GNSS/GPS Data、20.2 Live GPS tracking） | GPS 数据导入与实时 GPS 跟踪。 | Processing（24.1 含 GPS 一组：格式转换、设备上下传等） |
| 19 | 认证系统 | 21. Authentication System（21.1 Overview、21.2 User Authentication Workflows）；另见 8.8 Authentication | 受保护服务/数据库的凭据存储与认证工作流。 | PyQGIS（Cookbook 14. Authentication infrastructure） |
| 20 | GRASS GIS 集成（桌面侧） | 22. GRASS GIS Integration（22.1–22.14，详见第三节） | 经 provider 浏览/可视化 GRASS 栅格矢量、经 plugin 建 LOCATION/MAPSET、编辑与用 GRASS 模块分析。 | Processing + 仅桌面（GRASS plugin/Toolbox 为桌面组件；Processing 侧地位见第三节） |
| 21 | Processing 框架 | 23. QGIS processing framework（23.1 Introduction、23.2 Configuring、23.3 Toolbox、23.4 History manager、23.5 Model designer、23.6 Batch processing、23.7 From the console、23.8 From the command line、23.9 Writing new algorithms as Python scripts、23.10 Input/output types、23.11 Configuring external applications） | 统一算法框架：工具箱、历史、模型设计器、批处理、控制台/命令行调用与自写 Python 算法。 | Processing + PyQGIS（即自动化主入口本身） |
| 22 | Processing 提供者与算法参考 | 24. Processing providers and algorithms（24.1 QGIS algorithm provider、24.2 GDAL algorithm provider；仅此两章，核实见第三节） | 逐条记录 QGIS 与 GDAL 两家提供者的算法与参数（界面呈现口径）。 | Processing |
| 23 | 插件体系与 Python 控制台 | 25. Plugins（25.1 QGIS Plugins、25.2 Using QGIS Core Plugins、25.3 QGIS Python console） | 插件管理/使用、核心插件与内置 Python 控制台。 | PyQGIS（Cookbook 16. Developing Python Plugins、17. Writing a Processing plugin、18. Using Plugin Layers） |
| 24 | 附录与参考 | 26. Appendices（26.1 Appendix C: QGIS File Formats、26.2 Appendix D: QGIS R script syntax、26.3 Appendix E: QGIS Application Network Connections）；27. Literature and Web References | 文件格式清单、R 脚本语法（供 Processing R 脚本用）与应用网络连接清单。 | 仅桌面（参考资料性质） |
| 25 | QGIS Server（独立手册，非桌面指南章节） | QGIS Server Guide/Manual (3.40)（总入口页列：1. Introduction、2. Getting Started、3. Services、4. Catalog、5. Plugins、6. Advanced configuration、7. Development Server、8. Containerized deployment、9. Frequently Asked Question） | 以 QGIS 工程对外发布 OGC 等服务的服务端部署与配置；与桌面指南分册。 | PyQGIS（Cookbook 20. QGIS Server and Python：Server API、独立/嵌入运行、Server plugins） |

小结：桌面能力的主自动化入口是 Processing（分析/批处理/模型）与 PyQGIS（工程、图层、画布、布局、插件、Server 扩展）；纯桌面项集中在 GUI/浏览器交互、配准、实时 GPS、3D 视图操作与 GRASS plugin 的 LOCATION/MAPSET 管理。

---

## 二、PyQGIS 开发者手册（PyQGIS Cookbook 3.40）目录

### 2.1 实际打开的官方页面

| 用途 | URL | 抓取日期 |
|---|---|---|
| Cookbook 目录页（21 章及各章二级节全表） | https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html | 2026-11-02 |
| 文档总入口（Cookbook 在「For Developers」组内的定位） | https://docs.qgis.org/3.40/en/docs/index.html | 2026-11-02 |

### 2.2 章节清单（21 行，每章一行）

| # | 章名（官方英文原名） | 能编程式做什么（一句话） |
|---|---|---|
| 1 | 1. Introduction（1.1 Python Console 脚本、1.2 Python Plugins、1.3 启动时运行代码、1.4 Python Applications、1.5 PyQt/SIP 技术注记） | 在 Python 控制台、插件、启动钩子与独立 Python 应用四种形态下运行 PyQGIS 代码。 |
| 2 | 2. Loading Projects（2.1 坏路径处理、2.2 用 flags 提速） | 以代码打开工程、处理失效路径并用标志加速加载。 |
| 3 | 3. Loading Layers（3.1 Vector Layers、3.2 Raster Layers、3.3 QgsProject instance） | 以代码创建/加载矢量与栅格图层并注册进 QgsProject。 |
| 4 | 4. Accessing the Table Of Contents (TOC)（4.1 QgsProject class、4.2 QgsLayerTreeGroup class） | 以代码遍历、分组和管理图层树（TOC）。 |
| 5 | 5. Using Raster Layers（5.1 Layer Details、5.2 Renderer、5.3 Query Values、5.4 Editing raster data） | 读取栅格详情、设置渲染器、查询像元值并编辑栅格数据。 |
| 6 | 6. Using Vector Layers（6.1 属性信息、6.2 迭代要素、6.3 选择要素、6.4 修改图层、6.5 空间索引、6.6 QgsVectorLayerUtils、6.7 创建矢量图层、6.8 符号化、6.9 Further Topics） | 迭代/选择/增删改矢量要素、建空间索引、创建新矢量图层并设置符号化。 |
| 7 | 7. Geometry Handling（7.1 Geometry Construction、7.2 Access to Geometry、7.3 Geometry Predicates and Operations） | 构造与访问几何，执行空间谓词判断与几何运算。 |
| 8 | 8. Projections Support（8.1 Coordinate reference systems、8.2 CRS Transformation） | 以代码定义 CRS 并做坐标转换。 |
| 9 | 9. Using the Map Canvas（9.1 Embedding Map Canvas、9.2 Rubber Bands and Vertex Markers、9.3 Using Map Tools、9.4 Writing Custom Map Tools、9.5 Writing Custom Map Canvas Items） | 嵌入地图画布、画橡皮筋/顶点标记，并编写自定义地图工具与画布图元。 |
| 10 | 10. Map Rendering and Printing（10.1 Simple Rendering、10.2 不同 CRS 图层渲染、10.3 Output using print layout） | 以代码渲染地图并经打印布局输出。 |
| 11 | 11. Expressions, Filtering and Calculating Values（11.1 Parsing Expressions、11.2 Evaluating Expressions、11.3 Handling expression errors） | 解析与求值 QGIS 表达式，用于过滤与字段计算并处理表达式错误。 |
| 12 | 12. Reading And Storing Settings（无二级节列于目录页） | 以代码读写 QGIS 设置项。 |
| 13 | 13. Communicating with the user（13.1 QgsMessageBar 消息、13.2 进度显示、13.3 Logging） | 在界面消息栏提示、显示进度并写日志。 |
| 14 | 14. Authentication infrastructure（14.1 Introduction、14.2 Glossary、14.3 QgsAuthManager、14.4 插件适配认证、14.5 Authentication GUIs） | 经 QgsAuthManager 以代码使用认证库，并让插件接入认证体系。 |
| 15 | 15. Tasks - doing heavy work in the background（15.1 Introduction、15.2 Examples） | 用 QgsTask 等把重活放到后台任务执行。 |
| 16 | 16. Developing Python Plugins（16.1 插件结构、16.2 Code Snippets、16.3 IDE 设置与调试、16.4 Releasing your plugin） | 搭建、调试并发布 Python 插件。 |
| 17 | 17. Writing a Processing plugin（17.1 Creating from scratch、17.2 Updating a plugin、17.3 Implementing custom Processing algorithms） | 编写承载自定义 Processing 算法的插件。 |
| 18 | 18. Using Plugin Layers（18.1 Subclassing QgsPluginLayer） | 继承 QgsPluginLayer 实现自定义图层类型。 |
| 19 | 19. Network analysis library（19.1 General information、19.2 Building a graph、19.3 Graph analysis） | 用 QGIS 网络分析库建图并做路径等图分析。 |
| 20 | 20. QGIS Server and Python（20.1 Introduction、20.2 Server API basics、20.3 Standalone or embedding、20.4 Server plugins） | 以 Python 扩展 QGIS Server：用 Server API、独立/嵌入运行并写 Server 插件。 |
| 21 | 21. Cheat sheet for PyQGIS（21.1 User Interface、21.2 Settings、21.3 Toolbars、21.4 Menus、21.5 Canvas、21.6 Layers、21.7 Table of contents、21.8 Advanced TOC、21.9 Processing algorithms、21.10 Decorators、21.11 Composer、21.12 Sources） | 速查代码片段合集，覆盖界面、画布、图层、TOC、Processing 算法调用与布局（Composer）等高频操作。 |

小结：Cookbook 的编程式覆盖面 = 工程/图层/几何/投影/画布/渲染布局/表达式/设置/认证/后台任务/插件（含 Processing 插件与插件图层）/网络分析/Server；目录中没有单列的 Mesh、Point Clouds、3D Tiles、Vector Tiles 专题章（这些数据类型在 Cookbook 3.40 目录中未单列成章）。

---

## 三、GRASS / SAGA / 其他外部提供者在 3.40 官方文档中的地位

### 3.1 实际打开的官方页面

| 用途 | URL | 抓取日期 |
|---|---|---|
| Processing 算法参考章入口（第 24 章） | https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/index.html | 2026-11-02 |
| QGIS 算法提供者章（24.1） | https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/index.html | 2026-11-02 |
| Configuring external applications（23.11） | https://docs.qgis.org/3.40/en/docs/user_manual/processing/3rdParty.html | 2026-11-02 |
| Configuring the Processing Framework（23.2，含 Providers 块） | https://docs.qgis.org/3.40/en/docs/user_manual/processing/configuration.html | 2026-11-02 |
| Using processing algorithms from the console（23.7，算法 ID 写法出处） | https://docs.qgis.org/3.40/en/docs/user_manual/processing/console.html | 2026-11-02 |
| GRASS GIS Integration（第 22 章） | https://docs.qgis.org/3.40/en/docs/user_manual/grass_integration/grass_integration.html | 2026-11-02 |
| 用户指南目录页（第 22–24 章结构出处） | https://docs.qgis.org/3.40/en/docs/user_manual/index.html | 2026-11-02 |

### 3.2 核实结论①：Processing 算法参考章（第 24 章）不收录 GRASS / SAGA 逐条算法

已核实，任务给定的判断成立：

- 入口页 https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/index.html 全页只列两章：
  - 24.1. QGIS algorithm provider（下含 27 个算法组：3D Tiles、Cartography、Database、File tools、GPS、Interpolation、Layer tools、Mesh、Modeler tools、Network analysis、Plots、Point Cloud Conversion、Point Cloud Data Management、Point Cloud Extraction、Raster analysis、Raster Creation、Raster terrain analysis、Raster tools、Vector analysis、Vector coverage、Vector creation、Vector general、Vector geometry、Vector overlay、Vector selection、Vector table、Vector Tiles）；
  - 24.2. GDAL algorithm provider（下含 8 个算法组：Raster analysis、Raster conversion、Raster extraction、Raster miscellaneous、Raster projections、Vector conversion、Vector geoprocessing、Vector miscellaneous）。
- 用户指南目录页中第 24 章同样只列 24.1 与 24.2 两个二级节，与入口页一致。
- 结论写法：**GRASS 与 SAGA 的逐条算法（名称、参数说明）在 3.40 官方用户指南的 Processing 算法参考章中未收录——3.40 官方用户指南未收录。** 该章只逐条收录 QGIS 与 GDAL 两家提供者；GRASS/SAGA 在用户指南中的存在形式是「配置说明」（23.11、23.2）与 GRASS 的「桌面集成专章」（第 22 章），不是逐条算法参考。

### 3.3 Configuring external applications（23.11）怎么说外部提供者

出处页：https://docs.qgis.org/3.40/en/docs/user_manual/processing/3rdParty.html

总则（该页原文要点）：

- 「The processing framework can be extended using additional applications. Algorithms that rely on external applications are managed by their own algorithm providers. Additional providers can be found as separate plugins, and installed using the QGIS Plugin Manager.」
- 「By default, algorithms that rely on an external application not shipped with QGIS are not enabled. You can enable them in the Processing settings dialog if they are installed on your system.」
- Windows 非高级用户捷径（原文）：「Make sure you install QGIS in your system using the standalone installer. That will automatically install SAGA and GRASS in your system and configure them so they can be run from QGIS. All the algorithms from these providers will be ready to be run without needing any further configuration. If installing with the OSGeo4W application, make sure that you also select SAGA and GRASS for installation.」
- 通用注意：外部软件能打开的文件不等于能被其处理；数据库/冷门格式易出问题；矢量图层会被 QGIS 自动转成外部应用可接受的格式再传入（大图层会增加耗时）；GRASS 栅格图层作为外部算法输入会出问题，故这类图层不出现在可选输入中。

该页在 3.40 版实际包含的小节（按页面出现顺序）：SAGA、R、GRASS、LAStools、Orfeo Toolbox (OTB)。逐家要点：

| 提供者 | 启用/安装条件（官方页原文要点） | 备注（官方页原文要点） |
|---|---|---|
| SAGA | 「SAGA algorithms can be run from QGIS if SAGA is included with the QGIS installation.」Windows 下 standalone 与 OSGeo4W 安装器均包含 SAGA（见上总则：standalone 自动装 SAGA+GRASS）。 | 多输入栅格须同一 grid system，QGIS 调用前会重采样到公共格网（可手动设范围/像元或勾 Use min covering grid system for resampling）；SAGA 不支持多波段图层，须先拆波段（页中举例算法名写作『SAGA/Grid - Tools/Split RGB image』『SAGA/Grid - Tools/Extract band』，为工具箱显示名而非算法 ID）；经命令行接口调用，Log console output / Log execution commands 两项可记录日志。 |
| R | 「To enable R in Processing you need to install the Processing R Provider plugin and configure R for QGIS.」即须另装 Processing R Provider 插件，无预定义算法集（仅示例脚本），自写脚本扩展名为 `.rsx`。 | 与 SAGA 的区别（原文意）：R 没有一套预定义可运行算法，靠用户脚本调用 R 函数；示例脚本可经 QGIS Resource Sharing 插件从官方 R script collection 装入。 |
| GRASS（Processing 侧） | 「Configuring GRASS is not much different from configuring SAGA. First, the path to the GRASS folder has to be defined, but only if you are running Windows.」「GRASS 7 is needed for algorithms to work correctly.」默认框架尝试使用随 QGIS 发布的 GRASS 发行版；Linux 只须保证 GRASS 已正确安装且可在终端运行。 | GRASS 算法用 region 做计算：可手动定义，或勾 Use min covering region 自动取覆盖全部输入图层的最小范围。注意此处说的是 Processing 连接器配置，与第 22 章的 GRASS plugin（桌面 LOCATION/MAPSET）是两套机制，见 3.5。 |
| LAStools | 「you need to download and install LAStools on your computer and install the LAStools plugin (available from the official repository) in QGIS」；在 Processing options 中指定 LAStools folder（Linux 还须 Wine folder）。 | Linux 平台运行部分工具需要 Wine。 |
| Orfeo Toolbox (OTB) | 「Note that OTB is not distributed with QGIS and needs to be installed separately.」须在 Processing 设置中设 OTB folder 与 OTB application folder 后，算法才进 Processing Toolbox。 | 另有 Logger level、Maximum RAM、Geoid file、SRTM tiles folder 等高级设置；自 OTB 6.6.1 起新版与当时最新 QGIS 兼容。 |
| TauDEM | 在实际打开的 23.11 页面全文中未出现 TauDEM 小节（已全文检索该页，无 TauDEM 字样）。 | 写法：TauDEM 在 3.40 用户指南 23.11 中未收录（旧版本文档曾有该节，3.40 该页没有；此对比仅作定位说明，不作为 3.40 结论依据）。 |
| GDAL | 该页未给 GDAL 单独小节；GDAL 的地位由第 24.2 章逐条收录 + 23.2「默认提供者」体现（见 3.4）。 | GDAL 算法无须额外配置的说法在 3.40 实际打开页面中未见于 23.11（旧版有此句，3.40 该页未保留此表述时不引用）。 |

### 3.4 Configuring the Processing Framework（23.2）的 Providers 口径——与 23.11 的年代差

出处页：https://docs.qgis.org/3.40/en/docs/user_manual/processing/configuration.html

- 原文：「By default, QGIS is installed with two algorithm providers: - GDAL whose algorithms you may Activate (or not) in this dialog. - GRASS whose algorithms require the installation of the GRASS GIS Processing Provider from the Plugins Manager.」
- GRASS 的专属设置举例（原文列举）：For raster layers, use r.external (faster) instead of r.in.gdal；For vector layers, use v.external (faster) instead of v.in.ogr；Location of GRASS docs；Log console output；Log execution commands。
- 另有总则：「Installed plugins that provide Processing algorithms may also have their provider listed in this group, with custom settings.」以及第三方提供者相关项：Show algorithms with known issues（默认隐藏已知有问题的算法，一般来自第三方提供者）；CRS 不一致警告「Third-party providers are not concerned.」
- 与 23.11 的关系（普查注记，须并读）：23.2 是 3.40 的现行配置口径——默认提供者只点名 GDAL 与 GRASS，且 GRASS 算法须先从 Plugins Manager 安装 GRASS GIS Processing Provider；SAGA 在 23.2 的 Providers 块中未被点名。23.11 仍保留「standalone 安装器自动安装 SAGA and GRASS、装好即可跑」的旧式表述。两页同属 3.40 用户指南、口径不完全一致，引用时应注明各自出处页，不要把 23.11 的 SAGA 表述当作 3.40 的默认装配结论。

### 3.5 GRASS GIS Integration（第 22 章）：双件套与「400+ 模块」规模说法

出处页：https://docs.qgis.org/3.40/en/docs/user_manual/grass_integration/grass_integration.html ；目录页二级节为 22.1 Demo dataset；22.2 Loading GRASS raster and vector layers；22.3 Importing data into a GRASS LOCATION via drag and drop；22.4 Managing GRASS data in QGIS Browser；22.5 GRASS Options；22.6 Starting the GRASS plugin；22.7 Opening GRASS mapset；22.8 GRASS LOCATION and MAPSET；22.9 Importing data into a GRASS LOCATION；22.10 The GRASS vector data model；22.11 Creating a new GRASS vector layer；22.12 Digitizing and editing a GRASS vector layer；22.13 The GRASS region tool；22.14 The GRASS Toolbox。

- 双件套（原文）：「The integration consists of two parts: provider and plugin. The provider allows to browse, manage and visualize GRASS raster and vector layers. The plugin can be used to create new GRASS locations and mapsets, change GRASS region, create and edit vector layers and analyze GRASS 2-D and 3-D data with more than 400 GRASS modules.」
- 规模说法（原样引用，出处为上页章首段）：**「more than 400 GRASS modules」**——完整原句为 plugin 可「analyze GRASS 2-D and 3-D data with more than 400 GRASS modules」。这是 3.40 官方用户指南给出的唯一 GRASS 规模数字；SAGA 在实际打开的官方页面中未见类似的模块/算法总数说法（3.40 官方用户指南未收录 SAGA 规模数字）。
- 版本支持（原文）：「The provider supports GRASS version 6 and 7, the plugin supports GRASS 6 and 7 (starting from QGIS 2.12). QGIS distribution may contain provider/plugin for either GRASS 6 or GRASS 7 or for both versions at the same time (binaries have different file names). Only one version of the provider/plugin may be loaded on runtime however.」——注意：此段文字在 3.40 页中仍写作 GRASS 6/7；而 23.11 的 Processing 侧配置写作「GRASS 7 is needed」。两处按原文并录，不做调和。
- 使用前提（原文要点）：GRASS plugin 须经 Plugin Manager 加载；必须打开一个 MAPSET 才能用 GRASS Tools（未打开时工具禁用）；数据存于 GISDBASE（常称 grassdata）→ LOCATION → MAPSET 层级，一般须先把数据导入 LOCATION 才能用 GRASS 模块分析（r.external / v.external 可建只读外部链接，页中注明初学者路径不展开）。

### 3.6 算法 ID 前缀：官方页实际给出的写法与未给出的部分

出处页：https://docs.qgis.org/3.40/en/docs/user_manual/processing/console.html （23.7 Using processing algorithms from the console）

- ID 的一般形态（原文要点）：算法的命令行名（unique command-line name）即 alg.id()，形如「提供者:算法名」；可用 `for alg in QgsApplication.processingRegistry().algorithms(): print(alg.id(), "->", alg.displayName())` 列出全部 ID，再用 `processing.run("native:buffer", {...})` 调用。
- 该页实际印出的 ID 示例（原文）：`3d:tessellate`、`gdal:aspect`、`gdal:assignprojection`、`gdal:buffervectors`、`gdal:buildvirtualraster`、`gdal:cliprasterbyextent`、`gdal:cliprasterbymasklayer`、`gdal:clipvectorbyextent`、`gdal:clipvectorbypolygon`、`gdal:colorrelief`、`gdal:contour`、`gdal:convertformat`、`gdal:dissolve` 等；参数帮助示例用 `native:buffer`，并注明「`qgis:buffer` is an alias for `native:buffer`」。
- **GRASS / SAGA 的 ID 前缀：在本节实际打开的 3.40 官方页面（23.7 控制台页全文、23.11、23.2、第 24 章入口页）中，均未出现 `grass:` / `grass7:` / `saga:` / `sagang:` 形式的算法 ID 示例——3.40 官方用户指南在上述页面中未给出 GRASS/SAGA 的算法 ID 前缀写法（未收录）。** 因此本文件不填写 GRASS/SAGA 前缀的「实际写法」；凡需在代码中调用 GRASS/SAGA 算法，应以本机 QGIS 中 `processingRegistry().algorithms()` 的实际输出或算法对话框/帮助中的 ID 为准（这正是 23.7 官方页给出的查 ID 方法），不要凭外部资料写死前缀。
- 顺带核实：SAGA 的新一代提供者名称（NextGen 一类表述）在上述实际打开的 3.40 官方页面中未出现；23.11 仍以笼统的「SAGA」小节表述其配置（见 3.3）。

### 3.7 第三节小结

1. 算法参考收录：3.40 第 24 章 = QGIS（24.1）+ GDAL（24.2）两家逐条收录；GRASS/SAGA 逐条算法未收录。
2. GRASS 的官方地位最厚：既有桌面集成专章（第 22 章，provider + plugin 双件套，官方规模说法「more than 400 GRASS modules」），又是 23.2 点名的默认提供者之一（但其 Processing 算法须另装 GRASS GIS Processing Provider 插件）；Processing 侧配置在 23.11（须 GRASS 7、Windows 设路径、region 规则）。
3. SAGA 的官方地位最薄：仅在 23.11 有配置小节（随安装器包含、格网重采样、多波段限制、命令行调用与日志），23.2 默认提供者名单未点名 SAGA，无专章、无逐条算法、无规模数字。
4. 其他外部提供者：R（须装 Processing R Provider 插件、`.rsx` 脚本、无预定义算法集）、LAStools（下载 + 官方仓插件、Linux 需 Wine）、OTB（不随 QGIS 发布、单独安装并配置双路径）在 23.11 均有小节；TauDEM 在 3.40 的 23.11 中未收录。
5. ID 前缀：官方页只实证了 `native:` / `qgis:`（别名）/ `gdal:` / `3d:` 的写法；GRASS/SAGA 前缀官方页未给出，按未收录处理。

---

## 附：本文件来源页清单（均为 2026-11-02 实际打开的 docs.qgis.org 3.40 英文页）

1. https://docs.qgis.org/3.40/en/docs/index.html
2. https://docs.qgis.org/3.40/en/docs/user_manual/index.html
3. https://docs.qgis.org/3.40/en/docs/pyqgis_developer_cookbook/index.html
4. https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/index.html
5. https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/qgis/index.html
6. https://docs.qgis.org/3.40/en/docs/user_manual/processing/3rdParty.html
7. https://docs.qgis.org/3.40/en/docs/user_manual/processing/configuration.html
8. https://docs.qgis.org/3.40/en/docs/user_manual/processing/console.html
9. https://docs.qgis.org/3.40/en/docs/user_manual/grass_integration/grass_integration.html

注：抓取尾段曾遇文档站限流（HTTP 429），QGIS Server 手册未再单独打开其目录页；本文件中 Server 的 9 章结构引自来源页 1（总入口页）中并列刊出的 Server Guide 目录，属于该页原文。

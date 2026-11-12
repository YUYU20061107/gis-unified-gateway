# QGIS 功能普查（GIS 综合平台能力底账 · QGIS 卷）

- 普查日期：2026-11-02。证据口径：一级证据＝QGIS 官方文档（docs.qgis.org）；本卷未用论坛/博客。
- 版本口径：统一取 **QGIS 文档 3.40 英文版**（现行 LTR 线文档）。注：api.qgis.org 已有 4.3 开发版 API 文档，本卷不取开发版口径。
- 平台判断口径：core＝跨 GIS 软件共有的基础能力，适合升平台统一动词候选；extension＝QGIS 专属或分析型能力，经统一入口以扩展方式暴露；defer＝仅桌面交互、模型内部件或副作用风险大，暂不适合 Agent。
- 「轮子来源」口径（2026-11-02 鱼鱼追加定版）：平台升级原则＝全部升级＋不重复造轮子。算法条目的轮子来源由算法 ID 前缀确定：`native:`/`qgis:`/`3d:`＝QGIS Processing 算法本体，`gdal:`＝GDAL 提供者（QGIS 封装 GDAL 工具），`pdal:`＝PDAL 提供者（QGIS 封装 PDAL ≥2.5.0）。平台层只做统一翻译与治理，不自研算法。
- 分卷底稿：`parts/qgis-native-vector.md`（native 矢量与通用 17 组）、`parts/qgis-raster-gdal.md`（native 栅格/点云/三维 10 组＋GDAL 8 组）、`parts/qgis-desktop-pyqgis-providers.md`（桌面域/PyQGIS/外部提供者，含其实际打开的 9 个官方页面清单）。

## 1. 文档入口与版本口径

| 文档 | 入口（官方） | 本卷用途 |
|---|---|---|
| QGIS 文档总入口（3.40） | https://docs.qgis.org/3.40/en/docs/index.html | 用户指南、Server 手册、PyQGIS Cookbook 三册的总目录 |
| Processing 算法参考（第 24 章） | https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/index.html | 算法普查的纲：24.1 QGIS 提供者 27 组、24.2 GDAL 提供者 8 组（2026-11-02 实际打开核实） |
| Processing 框架（第 23 章） | https://docs.qgis.org/3.40/en/docs/user_manual/processing/index.html | 工具箱、模型、脚本、第三方提供者配置（23.11）、从控制台调用算法（23.7） |
| 从控制台使用算法（23.7） | https://docs.qgis.org/3.40/en/docs/user_manual/processing/console.html | `processing.run()`、`algorithmHelp()`、算法 ID 的官方查法（运行时枚举注册表） |
| GRASS GIS 集成（第 22 章） | docs.qgis.org 3.40 用户指南第 22 章（分卷三实查） | GRASS provider＋plugin 双件套与规模说法 |
| PyQGIS Cookbook（3.40） | 经文档总入口进入（分卷三实查） | 编程自动化面目录（§2.3） |

**已核实的关键事实**：3.40 官方用户指南的 Processing 算法参考章**只收录 QGIS（native）与 GDAL 两个提供者**的逐条算法；GRASS、SAGA 等外部提供者在文档中只有配置说明与集成专章（仅 GRASS），**没有逐条算法目录**（详见 §4.2 真缺口与分卷三）。

## 2. 功能域总览

### 2.1 桌面功能域（用户指南 3.40，25 域）

下表引自用户指南目录普查（分卷三第一节）：「自动化入口」列即该域的轮子来源第一层——有 PyQGIS/Processing 入口的域可借道编程式复用，仅桌面的域没有现成轮子可借（见 §4.2）。

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

### 2.2 Processing 算法域（分析能力主弹药库）

| 提供者 | ID 前缀 | 分组 | 条数（本卷实查） | 启用条件 | 轮子来源 |
|---|---|---|---|---|---|
| QGIS（native） | `native:` / `qgis:` / `3d:` | 27 组 | 317 条（含其中 PDAL 点云条目 17 条） | 随 QGIS 开箱可用，仅用 QGIS API | QGIS Processing 算法本体 |
| GDAL | `gdal:` | 8 组 | 57 条 | 随 QGIS 开箱可用 | GDAL 工具链（QGIS 封装） |
| PDAL（点云，文档组挂在 native 章内） | `pdal:` | 3 组（转换/数据管理/提取） | 17 条（计入 native 总数） | 需 PDAL 库 ≥2.5.0 | PDAL 工具链（QGIS 封装） |
| GRASS | 官方 3.40 页未给出示例写法 | 无逐条目录 | 未收录（官方集成章称 GRASS 插件可达「more than 400 GRASS modules」） | 需另装 GRASS GIS 与 GRASS Processing Provider 插件 | GRASS GIS 本体（外部程序） |
| SAGA | 官方 3.40 页未给出示例写法 | 无逐条目录 | 未收录（无专章、无规模数字） | 随 Windows 独立安装器包含，仍属外部程序 | SAGA 本体（外部程序） |
| 其他外部提供者（OTB / LAStools / R 等） | — | 无逐条目录 | 未收录（23.11 仅配置提及；TauDEM 在 23.11 全文未出现） | 各自外部程序 | 各自本体 |

### 2.3 PyQGIS 自动化面（Cookbook 3.40，21 章）

下表引自 Cookbook 目录普查（分卷三第二节）。这是桌面功能域的编程式轮子：凡 Processing 覆盖不到的工程/画布/布局操作，多经 PyQGIS 对象模型实现。

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

## 3. 功能/算法级清单（共 374 条：core 82 / extension 242 / defer 50）

### 3.1 QGIS（native）提供者 · 矢量与通用（17 组，232 条）

#### 制图（Cartography）（13 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Angle to nearest feature | 计算点到最近要素的对齐角度 | native:angletonearest | QGIS Processing 本体（native） | extension |
| Combine style databases | 合并多个样式库为一个 | native:combinestyles | QGIS Processing 本体（native） | extension |
| Create categorized renderer from styles | 按样式库符号生成分类渲染 | native:categorizeusingstyle | QGIS Processing 本体（native） | defer |
| Extract style from project | 从工程提取样式对象到样式库 | native:stylefromproject | QGIS Processing 本体（native） | extension |
| Export atlas layout as image | 将图集布局导出为图片 | native:atlaslayouttoimage | QGIS Processing 本体（native） | defer |
| Export atlas layout as multiple PDF files | 将图集布局导出为多个PDF | native:atlaslayouttomultiplepdf | QGIS Processing 本体（native） | defer |
| Export atlas layout as PDF | 将图集布局导出为单个PDF | native:atlaslayouttopdf | QGIS Processing 本体（native） | defer |
| Export print layout as image | 将打印布局导出为图片 | native:printlayouttoimage | QGIS Processing 本体（native） | defer |
| Export print layout as PDF | 将打印布局导出为PDF | native:printlayouttopdf | QGIS Processing 本体（native） | defer |
| Print layout map extent to layer | 布局地图范围导出为面图层 | native:printlayoutmapextenttolayer | QGIS Processing 本体（native） | extension |
| Set layer style | 给图层套用QML样式文件 | native:setlayerstyle | QGIS Processing 本体（native） | defer |
| Topological coloring | 为相邻面分配互不相同色号 | qgis:topologicalcoloring | QGIS Processing 本体（qgis Python 算法） | extension |
| Transfer annotations from main annotation layer | 主注记层内容转到新注记层 | native:transferannotationsfrommain | QGIS Processing 本体（native） | defer |

#### 数据库（Database）（7 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Import into PostGIS | 矢量图层导入PostgreSQL库 | qgis:importintopostgis | QGIS Processing 本体（qgis Python 算法） | extension |
| Import into SpatiaLite | 矢量图层导入SpatiaLite库 | qgis:importintospatialite | QGIS Processing 本体（qgis Python 算法） | extension |
| Package layers | 多图层打包进GeoPackage | native:package | QGIS Processing 本体（native） | extension |
| PostgreSQL execute and load SQL | 对PostgreSQL执行SQL并加载结果 | qgis:postgisexecuteandloadsql | QGIS Processing 本体（qgis Python 算法） | defer |
| PostgreSQL execute SQL | 对PostgreSQL数据库执行SQL | native:postgisexecutesql | QGIS Processing 本体（native） | defer |
| SpatiaLite execute SQL | 按文件对SpatiaLite执行SQL | native:spatialiteexecutesql | QGIS Processing 本体（native） | defer |
| SpatiaLite execute SQL (registered) | 对已连接SpatiaLite执行SQL | native:spatialiteexecutesqlregistered | QGIS Processing 本体（native） | defer |

#### 文件工具（File tools）（3 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Download file | 按URL下载文件到本地 | qgis:filedownloader | QGIS Processing 本体（qgis Python 算法） | defer |
| HTTP request | 发起HTTP请求并返回结果 | native:httprequest | QGIS Processing 本体（native） | defer |
| Open file or URL | 用默认程序打开文件或URL | native:openurl | QGIS Processing 本体（native） | defer |

#### GPS（GPS）（4 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Convert GPS data | 用GPSBabel转GPS文件为GPX | native:convertgpsdata | QGIS Processing 本体（native） | extension |
| Convert GPX feature type | 转换GPX要素类型 | native:convertgpxfeaturetype | QGIS Processing 本体（native） | extension |
| Download GPS data | 从GPS设备下载数据为GPX | native:downloadgpsdata | QGIS Processing 本体（native） | defer |
| Upload GPS data | 将GPX数据上传到GPS设备 | native:uploadgpsdata | QGIS Processing 本体（native） | defer |

#### 图层工具（Layer tools）（2 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Export layers information | 导出图层范围与元信息为面层 | native:exportlayersinformation | QGIS Processing 本体（native） | extension |
| Export to spreadsheet | 多图层属性导出为电子表格 | native:exporttospreadsheet | QGIS Processing 本体（native） | extension |

#### 建模器工具（Modeler tools）（14 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Calculate expression | 在模型中计算表达式并缓存 | native:calculateexpression | QGIS Processing 本体（native） | defer |
| Conditional branch | 按表达式给模型加条件分支 | native:condition | QGIS Processing 本体（native） | defer |
| Create directory | 在文件系统新建目录 | native:createdirectory | QGIS Processing 本体（native） | defer |
| Feature filter | 模型内按条件分流要素 | native:filter | QGIS Processing 本体（native） | defer |
| Filter layers by type | 模型内按矢量栅格分流图层 | native:filterlayersbytype | QGIS Processing 本体（native） | defer |
| Load layer | 把图层加载到当前工程 | native:loadlayer | QGIS Processing 本体（native） | defer |
| Raise exception | 抛出异常并中止模型执行 | native:raiseexception | QGIS Processing 本体（native） | defer |
| Raise message | 在日志中记录信息消息 | native:raisemessage | QGIS Processing 本体（native） | defer |
| Raise warning | 在日志中记录警告消息 | native:raisewarning | QGIS Processing 本体（native） | defer |
| Rename layer | 在模型中重命名图层 | native:renamelayer | QGIS Processing 本体（native） | defer |
| Save log | 把模型执行日志存为文件 | native:savelog | QGIS Processing 本体（native） | defer |
| Set project variable | 设置当前工程的表达式变量 | native:setprojectvariable | QGIS Processing 本体（native） | defer |
| String concatenation | 在模型中拼接两个字符串 | native:stringconcatenation | QGIS Processing 本体（native） | defer |
| Variable distance buffer | 按字段值做可变距离缓冲（已弃用） | qgis:variabledistancebuffer | QGIS Processing 本体（qgis Python 算法） | extension |

#### 网络分析（Network analysis）（5 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Service area (from layer) | 由点图层生成网络服务区 | qgis:serviceareafromlayer | QGIS Processing 本体（qgis Python 算法） | extension |
| Service area (from point) | 由单点生成网络服务区 | native:serviceareafrompoint | QGIS Processing 本体（native） | extension |
| Shortest path (layer to point) | 多起点到终点的最短路径 | native:shortestpathlayertopoint | QGIS Processing 本体（native） | extension |
| Shortest path (point to layer) | 起点到多目标点的最短路径 | native:shortestpathpointtolayer | QGIS Processing 本体（native） | extension |
| Shortest path (point to point) | 两点间最短或最快路径 | native:shortestpathpointtopoint | QGIS Processing 本体（native） | extension |

#### 图表（Plots）（8 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Bar plot | 按类别字段生成柱状图 | qgis:barplot | QGIS Processing 本体（qgis Python 算法） | extension |
| Box plot | 按类别字段生成箱线图 | qgis:boxplot | QGIS Processing 本体（qgis Python 算法） | extension |
| Mean and standard deviation plot | 生成均值标准差箱线图 | qgis:meanandstandarddeviationplot | QGIS Processing 本体（qgis Python 算法） | extension |
| Polar plot | 按类别与数值生成极坐标图 | qgis:polarplot | QGIS Processing 本体（qgis Python 算法） | extension |
| Raster layer histogram | 生成栅格波段直方图 | qgis:rasterlayerhistogram | QGIS Processing 本体（qgis Python 算法） | extension |
| Vector layer histogram | 生成矢量字段直方图 | qgis:vectorlayerhistogram | QGIS Processing 本体（qgis Python 算法） | extension |
| Vector layer scatterplot | 生成矢量字段散点图 | qgis:vectorlayerscatterplot | QGIS Processing 本体（qgis Python 算法） | extension |
| Vector layer scatterplot (3D) | 生成三维散点图 | qgis:scatter3dplot | QGIS Processing 本体（qgis Python 算法） | extension |

#### 矢量分析（Vector analysis）（17 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Basic statistics for fields | 计算单个字段的基础统计 | qgis:basicstatisticsforfields | QGIS Processing 本体（qgis Python 算法） | core |
| Climb along line | 计算线要素的爬升与下降 | qgis:climbalongline | QGIS Processing 本体（qgis Python 算法） | extension |
| Count points in polygon | 统计每个面内的点数量 | native:countpointsinpolygon | QGIS Processing 本体（native） | core |
| DBSCAN clustering | 对点做DBSCAN密度聚类 | native:dbscanclustering | QGIS Processing 本体（native） | extension |
| Distance matrix | 计算点间距离矩阵 | qgis:distancematrix | QGIS Processing 本体（qgis Python 算法） | extension |
| Distance to nearest hub (line to hub) | 生成到最近枢纽的连线 | qgis:distancetonearesthublinetohub | QGIS Processing 本体（qgis Python 算法） | extension |
| Distance to nearest hub (points) | 计算点到最近枢纽的距离 | qgis:distancetonearesthubpoints | QGIS Processing 本体（qgis Python 算法） | extension |
| Hub lines | 生成要素到枢纽的连线 | native:hublines | QGIS Processing 本体（native） | extension |
| K-means clustering | 对点做K均值聚类 | native:kmeansclustering | QGIS Processing 本体（native） | extension |
| List unique values | 列出字段的唯一值清单 | qgis:listuniquevalues | QGIS Processing 本体（qgis Python 算法） | extension |
| Mean coordinate(s) | 计算图层的平均坐标点 | native:meancoordinates | QGIS Processing 本体（native） | extension |
| Nearest neighbour analysis | 计算点分布的最近邻指数 | native:nearestneighbouranalysis | QGIS Processing 本体（native） | extension |
| Overlap analysis | 计算与各图层的重叠面积占比 | native:calculatevectoroverlaps | QGIS Processing 本体（native） | extension |
| Shortest line between features | 生成要素间的最短连线 | native:shortestline | QGIS Processing 本体（native） | extension |
| ST-DBSCAN clustering | 考虑时间维的DBSCAN聚类 | native:stdbscanclustering | QGIS Processing 本体（native） | extension |
| Statistics by categories | 按类别分组计算字段统计 | qgis:statisticsbycategories | QGIS Processing 本体（qgis Python 算法） | core |
| Sum line lengths | 按多边形汇总线长 | native:sumlinelengths | QGIS Processing 本体（native） | extension |

#### 矢量覆盖（Vector coverage）（3 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Coverage dissolve | 对覆盖多边形做优化融合 | native:coverageunion | QGIS Processing 本体（native） | extension |
| Coverage simplification | 保持拓扑有效的覆盖简化 | native:coveragesimplify | QGIS Processing 本体（native） | extension |
| Coverage validation | 检测覆盖的边不匹配与缝隙 | native:coveragevalidate | QGIS Processing 本体（native） | extension |

#### 矢量创建（Vector creation）（17 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Array offset lines | 生成线的多重偏移副本 | native:arrayoffsetlines | QGIS Processing 本体（native） | extension |
| Array translated features | 生成要素的多重平移副本 | native:arraytranslatedfeatures | QGIS Processing 本体（native） | extension |
| Create grid | 按范围与间距创建格网 | native:creategrid | QGIS Processing 本体（native） | core |
| Create points layer from table | 按表中坐标字段生成点层 | native:createpointslayerfromtable | QGIS Processing 本体（native） | core |
| Generate points (pixel centroids) along line | 沿线生成像元中心点 | qgis:generatepointspixelcentroidsalongline | QGIS Processing 本体（qgis Python 算法） | extension |
| Generate points (pixel centroids) inside polygons | 面内生成像元中心点 | native:generatepointspixelcentroidsinsidepolygons | QGIS Processing 本体（native） | extension |
| Import geotagged photos | 导入带地理标记的照片为点 | native:importphotos | QGIS Processing 本体（native） | extension |
| Points to path | 按顺序把点连成路径线 | native:pointstopath | QGIS Processing 本体（native） | extension |
| Random points along line | 沿线随机生成点（旧版） | qgis:qgisrandompointsalongline | QGIS Processing 本体（qgis Python 算法） | extension |
| Random points in extent | 在指定范围内随机生成点 | native:randompointsinextent | QGIS Processing 本体（native） | extension |
| Random points in layer bounds | 在图层范围内随机生成点 | qgis:randompointsinlayerbounds | QGIS Processing 本体（qgis Python 算法） | extension |
| Random points in polygons | 在面要素内随机生成点 | native:randompointsinpolygons | QGIS Processing 本体（native） | extension |
| Random points inside polygons | 在面内随机生成点（旧版） | qgis:randompointsinsidepolygons | QGIS Processing 本体（qgis Python 算法） | extension |
| Random points on lines | 在线要素上随机生成点 | native:randompointsonlines | QGIS Processing 本体（native） | extension |
| Pixels to points | 栅格像元转点 | native:pixelstopoints | QGIS Processing 本体（native） | extension |
| Pixels to polygons | 栅格像元转面 | native:pixelstopolygons | QGIS Processing 本体（native） | extension |
| Regular points | 按规则间距生成点阵 | qgis:regularpoints | QGIS Processing 本体（qgis Python 算法） | extension |

#### 矢量通用（Vector general）（28 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Assign projection | 只改CRS标注不重投影几何 | native:assignprojection | QGIS Processing 本体（native） | core |
| Batch Nominatim geocoding | 用Nominatim批量地址编码 | native:batchnominatimgeocoder | QGIS Processing 本体（native） | defer |
| Create bookmarks from layer | 按要素范围创建空间书签 | native:layertobookmarks | QGIS Processing 本体（native） | defer |
| Bookmarks to layer | 把空间书签导出为面图层 | native:bookmarkstolayer | QGIS Processing 本体（native） | defer |
| Create attribute index | 为字段创建属性索引 | native:createattributeindex | QGIS Processing 本体（native） | extension |
| Create spatial index | 为图层创建空间索引 | native:createspatialindex | QGIS Processing 本体（native） | extension |
| Define current projection | 就地改写Shapefile投影文件 | qgis:definecurrentprojection | QGIS Processing 本体（qgis Python 算法） | defer |
| Delete duplicate geometries | 删除几何完全相同的要素 | native:deleteduplicategeometries | QGIS Processing 本体（native） | extension |
| Remove duplicates by attribute | 按字段删除重复行 | native:removeduplicatesbyattribute | QGIS Processing 本体（native） | extension |
| Detect vector changes | 对比两版本图层找出变化 | native:detectvectorchanges | QGIS Processing 本体（native） | extension |
| Drop geometries | 删除几何只保留属性表 | native:dropgeometries | QGIS Processing 本体（native） | extension |
| Execute SQL | 对虚拟层执行SQL查询 | qgis:executesql | QGIS Processing 本体（qgis Python 算法） | defer |
| Export to DXF | 把图层导出为DXF文件 | native:dxfexport | QGIS Processing 本体（native） | extension |
| Find projection | 猜测缺失投影的正确CRS | qgis:findprojection | QGIS Processing 本体（qgis Python 算法） | extension |
| Flatten relationship | 展平关联关系生成新图层 | native:flattenrelationships | QGIS Processing 本体（native） | extension |
| Join attributes by field value | 按字段值做表连接 | native:joinattributestable | QGIS Processing 本体（native） | core |
| Join attributes by location | 按空间关系连接属性 | native:joinattributesbylocation | QGIS Processing 本体（native） | core |
| Join attributes by location (summary) | 空间连接并汇总统计 | qgis:joinbylocationsummary | QGIS Processing 本体（qgis Python 算法） | core |
| Join to nearest | 连接最近要素的属性 | native:joinbynearest | QGIS Processing 本体（native） | extension |
| Merge vector layers | 合并多个矢量图层为一层 | native:mergevectorlayers | QGIS Processing 本体（native） | core |
| Order by expression | 按表达式对要素排序 | native:orderbyexpression | QGIS Processing 本体（native） | extension |
| Repair Shapefile | 修复损坏的Shapefile | native:repairshapefile | QGIS Processing 本体（native） | extension |
| Reproject layer | 把图层重投影到目标CRS | native:reprojectlayer | QGIS Processing 本体（native） | core |
| Save features | 把要素另存为新文件 | native:savefeatures | QGIS Processing 本体（native） | extension |
| Set layer encoding | 设置图层的数据编码 | native:setlayerencoding | QGIS Processing 本体（native） | extension |
| Split features by character | 按字段字符拆分要素值 | native:splitfeaturesbycharacter | QGIS Processing 本体（native） | extension |
| Split vector layer | 按字段把图层拆成多文件 | native:splitvectorlayer | QGIS Processing 本体（native） | extension |
| Truncate table | 清空图层全部要素 | native:truncatetable | QGIS Processing 本体（native） | defer |

#### 矢量几何（Vector geometry）（77 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add geometry attributes | 添加面积长度坐标等几何字段 | qgis:exportaddgeometrycolumns | QGIS Processing 本体（qgis Python 算法） | core |
| Affine transform | 对几何做平移缩放旋转变换 | native:affinetransform | QGIS Processing 本体（native） | extension |
| Aggregate | 按表达式分组聚合要素 | native:aggregate | QGIS Processing 本体（native） | extension |
| Boundary | 提取线面几何的拓扑边界 | native:boundary | QGIS Processing 本体（native） | extension |
| Bounding boxes | 计算每个要素的包围盒 | native:boundingboxes | QGIS Processing 本体（native） | core |
| Buffer | 按固定或字段距离生成缓冲区 | native:buffer | QGIS Processing 本体（native） | core |
| Centroids | 计算每个要素的质心点 | native:centroids | QGIS Processing 本体（native） | core |
| Check validity | 检查几何有效性并输出问题 | qgis:checkvalidity | QGIS Processing 本体（qgis Python 算法） | core |
| Collect geometries | 按分组把几何收集为多部件 | native:collect | QGIS Processing 本体（native） | extension |
| Concave hull | 按阈值生成凹包多边形 | native:concavehull | QGIS Processing 本体（native） | extension |
| Convert geometry type | 转换几何类型 | qgis:convertgeometrytype | QGIS Processing 本体（qgis Python 算法） | extension |
| Convert to curves | 把直线段几何转换为曲线 | native:converttocurves | QGIS Processing 本体（native） | extension |
| Convex hull | 生成要素的最小凸包 | native:convexhull | QGIS Processing 本体（native） | core |
| Create layer from extent | 把范围数值生成为面图层 | native:extenttolayer | QGIS Processing 本体（native） | extension |
| Create layer from point | 把坐标数值生成为点图层 | native:pointtolayer | QGIS Processing 本体（native） | extension |
| Create wedge buffers | 按方位角生成楔形缓冲区 | native:wedgebuffers | QGIS Processing 本体（native） | extension |
| Delaunay triangulation | 对点集做Delaunay三角剖分 | native:delaunaytriangulation | QGIS Processing 本体（native） | extension |
| Delete holes | 删除面中小于阈值的孔洞 | native:deleteholes | QGIS Processing 本体（native） | extension |
| Densify by count | 按新增顶点数加密几何 | native:densifygeometries | QGIS Processing 本体（native） | extension |
| Densify by interval | 按间距加密几何顶点 | native:densifygeometriesgivenaninterval | QGIS Processing 本体（native） | extension |
| Dissolve | 按字段或整体融合要素 | native:dissolve | QGIS Processing 本体（native） | core |
| Drape (set Z value from raster) | 从栅格给几何赋Z值 | native:setzfromraster | QGIS Processing 本体（native） | extension |
| Drop M/Z values | 去除几何的M与Z值 | native:dropmzvalues | QGIS Processing 本体（native） | extension |
| Eliminate selected polygons | 把选中小面并入邻近大面 | qgis:eliminateselectedpolygons | QGIS Processing 本体（qgis Python 算法） | extension |
| Explode lines | 把线拆为单段线要素 | native:explodelines | QGIS Processing 本体（native） | extension |
| Extend lines | 按距离延长线两端 | native:extendlines | QGIS Processing 本体（native） | extension |
| Filter vertices by M value | 按M值范围过滤顶点 | native:filterverticesbym | QGIS Processing 本体（native） | extension |
| Filter vertices by Z value | 按Z值范围过滤顶点 | native:filterverticesbyz | QGIS Processing 本体（native） | extension |
| Fix geometries | 修复无效几何使其有效 | native:fixgeometries | QGIS Processing 本体（native） | core |
| Force right-hand-rule | 强制面环遵循右手定则 | native:forcerhr | QGIS Processing 本体（native） | extension |
| Split layer at antimeridian | 在反经线处切分几何 | native:antimeridiansplit | QGIS Processing 本体（native） | extension |
| Geometry by expression | 用表达式逐要素生成新几何 | native:geometrybyexpression | QGIS Processing 本体（native） | extension |
| Interpolate point on line | 按距起点距离在线上插值取点 | native:interpolatepoint | QGIS Processing 本体（native） | extension |
| Keep N biggest parts | 只保留最大的N个部件 | qgis:keepnbiggestparts | QGIS Processing 本体（qgis Python 算法） | extension |
| Line substring | 按起止距离截取线段 | native:linesubstring | QGIS Processing 本体（native） | extension |
| Lines to polygons | 把闭合线转换为面 | qgis:linestopolygons | QGIS Processing 本体（qgis Python 算法） | core |
| Merge lines | 合并相接的线要素 | native:mergelines | QGIS Processing 本体（native） | extension |
| Minimum bounding geometry | 生成最小包围几何 | qgis:minimumboundinggeometry | QGIS Processing 本体（qgis Python 算法） | extension |
| Minimum enclosing circle | 生成最小外接圆 | native:minimumenclosingcircle | QGIS Processing 本体（native） | extension |
| Multi-ring buffer (constant distance) | 生成等距多环缓冲区 | native:multiringconstantbuffer | QGIS Processing 本体（native） | extension |
| Multipart to singleparts | 多部件拆为单部件要素 | native:multiparttosingleparts | QGIS Processing 本体（native） | core |
| Offset line | 按距离偏移线要素 | native:offsetline | QGIS Processing 本体（native） | extension |
| Oriented minimum bounding box | 生成有向最小包围盒 | native:orientedminimumboundingbox | QGIS Processing 本体（native） | extension |
| Orthogonalize | 把几何角度调整为直角 | native:orthogonalize | QGIS Processing 本体（native） | extension |
| Point on surface | 生成保证落在面上的点 | native:pointonsurface | QGIS Processing 本体（native） | extension |
| Points along lines | 按间距沿线生成点 | native:pointsalonglines | QGIS Processing 本体（native） | extension |
| Points displacement | 对重叠点做位移分散 | qgis:pointsdisplacement | QGIS Processing 本体（qgis Python 算法） | extension |
| Pole of inaccessibility | 计算面的不可达极点 | native:poleofinaccessibility | QGIS Processing 本体（native） | extension |
| Polygonize | 由线网络构建面 | native:polygonize | QGIS Processing 本体（native） | extension |
| Polygons to lines | 把面轮廓转换为线 | native:polygonstolines | QGIS Processing 本体（native） | core |
| Project points (Cartesian) | 按距离方位投影点（平面） | native:projectpointcartesian | QGIS Processing 本体（native） | extension |
| Promote to multipart | 单部件提升为多部件几何 | native:promotetomulti | QGIS Processing 本体（native） | extension |
| Rectangles, ovals, diamonds | 按范围生成矩形椭圆菱形 | native:rectanglesovalsdiamonds | QGIS Processing 本体（native） | extension |
| Remove duplicate vertices | 删除几何中的重复顶点 | native:removeduplicatevertices | QGIS Processing 本体（native） | extension |
| Remove null geometries | 删除空几何要素 | native:removenullgeometries | QGIS Processing 本体（native） | extension |
| Reverse line direction | 反转线要素方向 | native:reverselinedirection | QGIS Processing 本体（native） | extension |
| Rotate | 按角度旋转要素几何 | native:rotatefeatures | QGIS Processing 本体（native） | extension |
| Roundness | 计算面要素的圆度指标 | native:roundness | QGIS Processing 本体（native） | extension |
| Segmentize by maximum angle | 按最大转角细分几何 | native:segmentizebymaxangle | QGIS Processing 本体（native） | extension |
| Segmentize by maximum distance | 按最大段长细分几何 | native:segmentizebymaxdistance | QGIS Processing 本体（native） | extension |
| Set M value | 给几何设置固定M值 | native:setmvalue | QGIS Processing 本体（native） | extension |
| Set M value from raster | 从栅格给几何赋M值 | native:setmfromraster | QGIS Processing 本体（native） | extension |
| Set Z value | 给几何设置固定Z值 | native:setzvalue | QGIS Processing 本体（native） | extension |
| Simplify | 按容差简化几何 | native:simplifygeometries | QGIS Processing 本体（native） | core |
| Single sided buffer | 生成线的单侧缓冲区 | native:singlesidedbuffer | QGIS Processing 本体（native） | extension |
| Smooth | 对几何做平滑处理 | native:smoothgeometry | QGIS Processing 本体（native） | extension |
| Snap geometries to layer | 把几何捕捉到参考图层 | native:snapgeometries | QGIS Processing 本体（native） | extension |
| Snap points to grid | 把点捕捉到格网交点 | native:snappointstogrid | QGIS Processing 本体（native） | extension |
| Split lines by maximum length | 按最大长度切分线 | native:splitlinesbylength | QGIS Processing 本体（native） | extension |
| Subdivide | 把复杂几何细分为小部件 | native:subdivide | QGIS Processing 本体（native） | extension |
| Swap X and Y coordinates | 交换几何的X与Y坐标 | native:swapxy | QGIS Processing 本体（native） | extension |
| Tapered buffer | 生成宽度渐变的缓冲区 | native:taperedbuffer | QGIS Processing 本体（native） | extension |
| Tessellate | 把面几何三角化（3D） | 3d:tessellate | QGIS Processing 本体（3D） | extension |
| Transect | 沿线按间距生成横断线 | native:transect | QGIS Processing 本体（native） | extension |
| Translate | 按偏移量平移几何 | native:translategeometry | QGIS Processing 本体（native） | extension |
| Variable width buffer (by M value) | 按M值生成变宽缓冲区 | native:bufferbym | QGIS Processing 本体（native） | extension |
| Voronoi polygons | 对点集生成泰森多边形 | native:voronoipolygons | QGIS Processing 本体（native） | extension |

#### 矢量叠加（Vector overlay）（10 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Clip | 用面层裁剪矢量图层 | qgis:clip | QGIS Processing 本体（qgis Python 算法） | core |
| Difference | 擦除与叠加层重叠的部分 | qgis:difference | QGIS Processing 本体（qgis Python 算法） | core |
| Difference (multiple layers) | 依次擦除多个叠加层 | qgis:multidifference | QGIS Processing 本体（qgis Python 算法） | extension |
| Intersection | 提取两层重叠部分及双属性 | qgis:intersection | QGIS Processing 本体（qgis Python 算法） | core |
| Intersection (multiple layers) | 提取与多层共同重叠部分 | qgis:multiintersection | QGIS Processing 本体（qgis Python 算法） | extension |
| Line intersections | 提取线交点并附两线属性 | qgis:lineintersections | QGIS Processing 本体（qgis Python 算法） | extension |
| Split with lines | 用另一层线分割要素 | qgis:splitwithlines | QGIS Processing 本体（qgis Python 算法） | extension |
| Symmetrical difference | 提取两层互不重叠的部分 | qgis:symmetricaldifference | QGIS Processing 本体（qgis Python 算法） | core |
| Union | 合并两层并保留全部区域 | qgis:union | QGIS Processing 本体（qgis Python 算法） | core |
| Union (multiple layers) | 合并输入层与多个叠加层 | qgis:multiunion | QGIS Processing 本体（qgis Python 算法） | extension |

#### 矢量选择（Vector selection）（9 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Filter by geometry type | 按几何类型分流要素 | native:filterbygeometry | QGIS Processing 本体（native） | extension |
| Random extract | 随机抽取一部分要素成新层 | native:randomextract | QGIS Processing 本体（native） | extension |
| Random extract within subsets | 按类别随机抽取要素成新层 | qgis:randomextractwithinsubsets | QGIS Processing 本体（qgis Python 算法） | extension |
| Random selection | 在图层中随机选中要素 | qgis:randomselection | QGIS Processing 本体（qgis Python 算法） | defer |
| Random selection within subsets | 按类别随机选中要素 | qgis:randomselectionwithinsubsets | QGIS Processing 本体（qgis Python 算法） | defer |
| Select by attribute | 按属性条件选中要素 | qgis:selectbyattribute | QGIS Processing 本体（qgis Python 算法） | defer |
| Select by expression | 按表达式选中要素 | qgis:selectbyexpression | QGIS Processing 本体（qgis Python 算法） | defer |
| Select by location | 按空间关系选中要素 | native:selectbylocation | QGIS Processing 本体（native） | defer |
| Select within distance | 选中指定距离内的要素 | native:selectwithindistance | QGIS Processing 本体（native） | defer |

#### 矢量表（Vector table）（12 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Add autoincremental field | 添加自增序号字段 | native:addautoincrementalfield | QGIS Processing 本体（native） | extension |
| Add field to attributes table | 给属性表添加新字段 | native:addfieldtoattributestable | QGIS Processing 本体（native） | core |
| Add unique value index field | 给类别值添加数字索引字段 | native:adduniquevalueindexfield | QGIS Processing 本体（native） | extension |
| Add X/Y fields to layer | 给点图层添加XY坐标字段 | native:addxyfields | QGIS Processing 本体（native） | core |
| Advanced Python field calculator | 用Python公式计算新字段 | qgis:advancedpythonfieldcalculator | QGIS Processing 本体（qgis Python 算法） | defer |
| Drop field(s) | 删除指定的属性字段 | native:deletecolumn | QGIS Processing 本体（native） | core |
| Explode HStore field | 把HStore键值展开为字段 | native:explodehstorefield | QGIS Processing 本体（native） | extension |
| Field calculator | 用表达式计算新字段 | native:fieldcalculator | QGIS Processing 本体（native） | core |
| Refactor fields | 重构字段结构与类型映射 | native:refactorfields | QGIS Processing 本体（native） | extension |
| Rename field | 重命名属性字段 | qgis:renametablefield | QGIS Processing 本体（qgis Python 算法） | extension |
| Retain fields | 只保留指定的属性字段 | native:retainfields | QGIS Processing 本体（native） | extension |
| Text to float | 把文本字段转换为浮点数 | qgis:texttofloat | QGIS Processing 本体（qgis Python 算法） | extension |

#### 矢量瓦片（Vector Tiles）（3 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Download vector tiles | 下载矢量瓦片到本地文件 | native:downloadvectortiles | QGIS Processing 本体（native） | defer |
| Write vector tiles (MBTiles) | 图层写出为MBTiles矢量瓦片 | native:writevectortiles_mbtiles | QGIS Processing 本体（native） | extension |
| Write vector tiles (XYZ) | 图层写出为XYZ目录矢量瓦片 | native:writevectortiles_xyz | QGIS Processing 本体（native） | extension |

### 3.2 QGIS（native）提供者 · 栅格 / 点云 / 三维（10 组，85 条，含 PDAL 点云 17 条）

#### 3D Tiles（2 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Convert B3DM to GLTF | 旧B3DM三维瓦片转GLTF/GLB | native:b3dmtogltf | QGIS Processing 本体（native） | extension |
| Convert GLTF to vector features | GLTF/GLB内容转矢量线面要素 | native:gltftovector | QGIS Processing 本体（native） | extension |

#### Interpolation（4 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Heatmap (kernel density estimation) | 点核密度估计生成密度热力栅格 | qgis:heatmapkerneldensityestimation | QGIS Processing 本体（qgis Python 算法） | extension |
| IDW Interpolation | 反距离加权插值点数据成栅格 | qgis:idwinterpolation | QGIS Processing 本体（qgis Python 算法） | core |
| Line Density | 计算邻域内线要素长度密度栅格 | native:linedensity | QGIS Processing 本体（native） | extension |
| TIN Interpolation | TIN三角网插值点数据成栅格 | qgis:tininterpolation | QGIS Processing 本体（qgis Python 算法） | core |

#### Mesh（9 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Export contours | 由网格标量数据集生成等值线和面 | native:meshcontours | QGIS Processing 本体（native） | extension |
| Export cross section dataset values on lines from mesh | 沿线提取网格数据集值导出CSV | native:meshexportcrosssection | QGIS Processing 本体（native） | extension |
| Export mesh edges | 网格边导出为带数据集值的线矢量 | native:exportmeshedges | QGIS Processing 本体（native） | extension |
| Export mesh faces | 网格面导出为带数据集值的面矢量 | native:exportmeshfaces | QGIS Processing 本体（native） | extension |
| Export mesh on grid | 网格数据集采样到规则格网点矢量 | native:exportmeshongrid | QGIS Processing 本体（native） | extension |
| Export mesh vertices | 网格顶点导出为带数据集值的点矢量 | native:exportmeshvertices | QGIS Processing 本体（native） | extension |
| Export time series values from points of a mesh dataset | 在点位提取网格数据集时间序列值 | native:meshexporttimeseries | QGIS Processing 本体（native） | extension |
| Rasterize mesh dataset | 网格数据集栅格化为栅格图层 | native:meshrasterize | QGIS Processing 本体（native） | extension |
| TIN mesh creation | 矢量层经Delaunay三角化建TIN网格 | native:tinmeshcreation | QGIS Processing 本体（native） | extension |

#### Point Cloud Conversion（4 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Convert format | 点云转LAS/LAZ/COPC/VPC等格式，如压成LAZ | pdal:convertformat | PDAL 提供者（QGIS 封装 PDAL） | core |
| Export to raster | 按指定属性把点云栅格化导出TIF | pdal:exportraster | PDAL 提供者（QGIS 封装 PDAL） | core |
| Export raster (using triangulation) | 三角化插值点云生成地形栅格，点稀时建DEM用 | pdal:exportrastertin | PDAL 提供者（QGIS 封装 PDAL） | extension |
| Export to vector | 点云导出为三维点矢量GeoPackage | pdal:exportvector | PDAL 提供者（QGIS 封装 PDAL） | core |

#### Point Cloud Data Management（10 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Assign projection | 给CRS缺失或错误的点云赋予坐标系 | pdal:assignprojection | PDAL 提供者（QGIS 封装 PDAL） | core |
| Build virtual point cloud (VPC) | 多份点云拼成虚拟点云，可选边界统计与概览 | pdal:virtualpointcloud | PDAL 提供者（QGIS 封装 PDAL） | extension |
| Clip | 用面图层裁点云，只留面内点，竞赛按区裁剪用 | pdal:clip | PDAL 提供者（QGIS 封装 PDAL） | core |
| Create COPC | 批量为点云文件生成COPC索引 | pdal:createcopc | PDAL 提供者（QGIS 封装 PDAL） | extension |
| Information | 输出点云元数据：点数、范围、CRS、属性表 | pdal:info | PDAL 提供者（QGIS 封装 PDAL） | core |
| Merge | 多份点云文件合并为一份 | pdal:merge | PDAL 提供者（QGIS 封装 PDAL） | core |
| Reproject | 点云重投影到另一坐标系 | pdal:reproject | PDAL 提供者（QGIS 封装 PDAL） | core |
| Thin (by sampling radius) | 按采样半径抽稀，半径内只留一点，降密度 | pdal:thinbyradius | PDAL 提供者（QGIS 封装 PDAL） | extension |
| Thin (by skipping points) | 每隔N个点保留一个抽稀点云 | pdal:thinbydecimate | PDAL 提供者（QGIS 封装 PDAL） | extension |
| Tile | 点云按边长切分瓦片，大数据分块处理用 | pdal:tile | PDAL 提供者（QGIS 封装 PDAL） | extension |

#### Point Cloud Extraction（3 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Boundary | 提取点云覆盖边界多边形，可含洞 | pdal:boundary | PDAL 提供者（QGIS 封装 PDAL） | extension |
| Density | 每格点数成密度栅格，质检点云疏密空洞 | pdal:density | PDAL 提供者（QGIS 封装 PDAL） | extension |
| Filter | 按PDAL表达式或矩形范围筛点，如按分类码提地面点 | pdal:filter | PDAL 提供者（QGIS 封装 PDAL） | core |

#### Raster analysis（31 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Cell stack percent rank from value | 算给定值在栅格叠栈中的百分位排名 | native:cellstackpercentrankfromvalue | QGIS Processing 本体（native） | extension |
| Cell stack percentile | 栅格叠栈逐像元百分位值计算 | native:cellstackpercentile | QGIS Processing 本体（native） | extension |
| Cell stack percentrank from raster layer | 以一栅格逐像元值算叠栈百分位排名 | native:cellstackpercentrankfromrasterlayer | QGIS Processing 本体（native） | extension |
| Cell statistics | 多栅格逐像元统计，如均值中位数 | native:cellstatistics | QGIS Processing 本体（native） | core |
| Equal to frequency | 统计叠栈中等于给定值的频次 | native:equaltofrequency | QGIS Processing 本体（native） | extension |
| Fuzzify raster (gaussian membership) | 高斯隶属函数把栅格值模糊化到0至1 | native:fuzzifyrastergaussianmembership | QGIS Processing 本体（native） | extension |
| Fuzzify raster (large membership) | 大值隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasterlargemembership | QGIS Processing 本体（native） | extension |
| Fuzzify raster (linear membership) | 线性隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasterlinearmembership | QGIS Processing 本体（native） | extension |
| Fuzzify raster (near membership) | 近值隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasternearmembership | QGIS Processing 本体（native） | extension |
| Fuzzify raster (power membership) | 幂隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasterpowermembership | QGIS Processing 本体（native） | extension |
| Fuzzify raster (small membership) | 小值隶属函数把栅格值模糊化到0至1 | native:fuzzifyrastersmallmembership | QGIS Processing 本体（native） | extension |
| Greater than frequency | 统计叠栈中大于给定值的频次 | native:greaterthanfrequency | QGIS Processing 本体（native） | extension |
| Highest position in raster stack | 找叠栈中最大值所在的层序号 | native:highestpositioninrasterstack | QGIS Processing 本体（native） | extension |
| Less than frequency | 统计叠栈中小于给定值的频次 | native:lessthanfrequency | QGIS Processing 本体（native） | extension |
| Lowest position in raster stack | 找叠栈中最小值所在的层序号 | native:lowestpositioninrasterstack | QGIS Processing 本体（native） | extension |
| Raster boolean AND | 多个栅格逐像元布尔与运算 | native:rasterbooleanand | QGIS Processing 本体（native） | core |
| Raster boolean OR | 多个栅格逐像元布尔或运算 | native:rasterbooleanor | QGIS Processing 本体（native） | core |
| Raster calculator | 表达式逐像元栅格计算 | native:rastercalc | QGIS Processing 本体（native） | core |
| Raster calculator (virtual) | 表达式生成即时计算的虚拟栅格 | native:virtualrastercalc | QGIS Processing 本体（native） | core |
| Raster layer properties | 输出栅格范围、CRS、行列数等属性 | native:rasterlayerproperties | QGIS Processing 本体（native） | extension |
| Raster layer statistics | 计算栅格波段基本统计量 | native:rasterlayerstatistics | QGIS Processing 本体（native） | core |
| Raster layer unique values report | 报告栅格唯一值及各自像元数 | native:rasterlayeruniquevaluesreport | QGIS Processing 本体（native） | extension |
| Raster layer zonal statistics | 按分区统计栅格像元值 | native:rasterlayerzonalstats | QGIS Processing 本体（native） | extension |
| Raster surface volume | 计算栅格表面与基准面间体积 | native:rastersurfacevolume | QGIS Processing 本体（native） | extension |
| Reclassify by layer | 按另一图层的值表重分类栅格 | native:reclassifybylayer | QGIS Processing 本体（native） | core |
| Reclassify by table | 按数值区间表重分类栅格 | native:reclassifybytable | QGIS Processing 本体（native） | core |
| Rescale raster | 栅格值线性拉伸到新数值范围 | native:rescaleraster | QGIS Processing 本体（native） | extension |
| Round raster values | 栅格像元值按指定方式取整 | native:roundrastervalues | QGIS Processing 本体（native） | extension |
| Sample raster values | 在点要素位置采样栅格像元值 | native:rastersampling | QGIS Processing 本体（native） | core |
| Zonal histogram | 分区统计各栅格值的像元数成表 | native:zonalhistogram | QGIS Processing 本体（native） | extension |
| Zonal statistics | 按面分区汇总栅格统计量到属性 | native:zonalstatisticsfb | QGIS Processing 本体（native） | core |

#### Raster Creation（9 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Create constant raster layer | 按范围与像元大小生成常数填充栅格 | native:createconstantrasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (binomial distribution) | 生成二项分布随机值栅格 | native:createrandombinomialrasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (exponential distribution) | 生成指数分布随机值栅格 | native:createrandomexponentialrasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (gamma distribution) | 生成伽马分布随机值栅格 | native:createrandomgammarasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (geometric distribution) | 生成几何分布随机值栅格 | native:createrandomgeometricrasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (negative binomial distribution) | 生成负二项分布随机值栅格 | native:createrandomnegativebinomialrasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (normal distribution) | 生成正态分布随机值栅格 | native:createrandomnormalrasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (poisson distribution) | 生成泊松分布随机值栅格 | native:createrandompoissonrasterlayer | QGIS Processing 本体（native） | extension |
| Create random raster layer (uniform distribution) | 生成均匀分布随机值栅格 | native:createrandomuniformrasterlayer | QGIS Processing 本体（native） | extension |

#### Raster terrain analysis（7 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Aspect | 由DEM计算坡向，0至360度 | qgis:aspect | QGIS Processing 本体（qgis Python 算法） | core |
| DTM filter (slope-based) | 坡度法滤波DEM，分地面与非地面像元 | native:dtmslopebasedfilter | QGIS Processing 本体（native） | extension |
| Hillshade | 按太阳方位高度角生成山体阴影 | qgis:hillshade | QGIS Processing 本体（qgis Python 算法） | core |
| Hypsometric curves | 计算DEM高程面积曲线输出CSV | qgis:hypsometriccurves | QGIS Processing 本体（qgis Python 算法） | extension |
| Relief | 生成分级设色的地貌晕渲栅格 | qgis:relief | QGIS Processing 本体（qgis Python 算法） | extension |
| Ruggedness index | 计算地形粗糙度指数栅格 | qgis:ruggednessindex | QGIS Processing 本体（qgis Python 算法） | extension |
| Slope | 由DEM计算坡度栅格 | qgis:slope | QGIS Processing 本体（qgis Python 算法） | core |

#### Raster tools（6 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Align raster | 单栅格对齐到参考栅格，仅建模器上下文可用 | native:alignsingleraster | QGIS Processing 本体（native） | defer |
| Align rasters | 多栅格重采样重投影对齐到参考栅格 | native:alignrasters | QGIS Processing 本体（native） | core |
| Convert map to raster | 把当前地图画布内容渲染为栅格图 | native:rasterize | QGIS Processing 本体（native） | defer |
| Fill NoData cells | 用指定值填满栅格NoData像元 | native:fillnodata | QGIS Processing 本体（native） | core |
| Generate XYZ tiles (Directory) | 生成XYZ瓦片目录供Web地图用 | native:tilesxyzdirectory | QGIS Processing 本体（native） | extension |
| Generate XYZ tiles (MBTiles) | 生成MBTiles单文件瓦片包 | native:tilesxyzmbtiles | QGIS Processing 本体（native） | extension |

### 3.3 GDAL 提供者（8 组，57 条）

#### Raster analysis（17 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Aspect | 由DEM计算坡向 | gdal:aspect | GDAL 提供者（QGIS 封装 GDAL） | core |
| Color relief | 按色表文件把DEM渲染为彩色地貌图 | gdal:colorrelief | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Fill NoData | 插值填补栅格NoData空洞并平滑 | gdal:fillnodata | GDAL 提供者（QGIS 封装 GDAL） | core |
| Grid (Data metrics) | 点数据按窗口统计格网化，如最小最大值 | gdal:griddatametrics | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Grid (IDW with nearest neighbor searching) | 最近邻搜索的反距离加权点插值格网 | gdal:gridinversedistancenearestneighbor | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Grid (Inverse distance to a power) | 反距离幂点插值格网化 | gdal:gridinversedistance | GDAL 提供者（QGIS 封装 GDAL） | core |
| Grid (Linear) | 线性插值把点数据格网化 | gdal:gridlinear | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Grid (Moving average) | 移动平均把点数据格网化 | gdal:gridaverage | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Grid (Nearest neighbor) | 最近邻把点数据格网化 | gdal:gridnearestneighbor | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Hillshade | 由DEM生成山体阴影 | gdal:hillshade | GDAL 提供者（QGIS 封装 GDAL） | core |
| Near black | 把近黑近白的边缘像元设黑或透明 | gdal:nearblack | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Proximity (raster distance) | 生成到目标像元的距离栅格 | gdal:proximity | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Roughness | 计算地形粗糙度，邻域高程最大差 | gdal:roughness | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Sieve | 筛除小于阈值的零散像元斑块 | gdal:sieve | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Slope | 由DEM计算坡度 | gdal:slope | GDAL 提供者（QGIS 封装 GDAL） | core |
| Terrain Ruggedness Index (TRI) | 计算地形粗糙度指数TRI | gdal:triterrainruggednessindex | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Topographic Position Index (TPI) | 计算地形位置指数TPI | gdal:tpitopographicpositionindex | GDAL 提供者（QGIS 封装 GDAL） | extension |

#### Raster conversion（6 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| gdal2xyz | 栅格导出为XYZ ASCII文本 | gdal:gdal2xyz | GDAL 提供者（QGIS 封装 GDAL） | extension |
| PCT to RGB | 调色板8位影像转24位RGB | gdal:pcttorgb | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Polygonize (raster to vector) | 同值连通像元转面矢量，栅格转矢量 | gdal:polygonize | GDAL 提供者（QGIS 封装 GDAL） | core |
| Rearrange bands | 选取并重排栅格波段生成新栅格 | gdal:rearrange_bands | GDAL 提供者（QGIS 封装 GDAL） | extension |
| RGB to PCT | RGB影像转8位调色板影像 | gdal:rgbtopct | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Translate (convert format) | 栅格格式转换，可改尺寸类型与范围 | gdal:translate | GDAL 提供者（QGIS 封装 GDAL） | core |

#### Raster extraction（4 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Clip raster by extent | 按矩形范围裁剪栅格 | gdal:cliprasterbyextent | GDAL 提供者（QGIS 封装 GDAL） | core |
| Clip raster by mask layer | 按矢量掩膜面裁剪栅格 | gdal:cliprasterbymasklayer | GDAL 提供者（QGIS 封装 GDAL） | core |
| Contour | 由高程栅格提取等高线矢量 | gdal:contour | GDAL 提供者（QGIS 封装 GDAL） | core |
| Contour Polygons | 由高程栅格提取等高线面矢量 | gdal:contour_polygon | GDAL 提供者（QGIS 封装 GDAL） | extension |

#### Raster miscellaneous（10 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Build overviews (pyramids) | 为栅格建金字塔概览加速渲染 | gdal:overviews | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Build virtual raster | 多栅格拼成VRT虚拟镶嵌数据集 | gdal:buildvirtualraster | GDAL 提供者（QGIS 封装 GDAL） | core |
| gdal2tiles | 栅格切成Web瓦片目录并生成查看页 | gdal:gdal2tiles | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Merge | 多个栅格合并镶嵌为一幅 | gdal:merge | GDAL 提供者（QGIS 封装 GDAL） | core |
| Pansharpening | 全色与多光谱影像融合锐化 | gdal:pansharp | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Raster calculator | 用GDAL表达式逐像元栅格计算 | gdal:rastercalculator | GDAL 提供者（QGIS 封装 GDAL） | core |
| Raster information | 输出栅格元信息报告 | gdal:gdalinfo | GDAL 提供者（QGIS 封装 GDAL） | core |
| Retile | 成套瓦片重切分并建金字塔 | gdal:retile | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Tile index | 为栅格集建瓦片索引面矢量 | gdal:tileindex | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Viewshed | 由DEM计算指定观测点可视域 | gdal:viewshed | GDAL 提供者（QGIS 封装 GDAL） | extension |

#### Raster projections（3 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Assign projection | 给栅格数据集赋予坐标系信息 | gdal:assignprojection | GDAL 提供者（QGIS 封装 GDAL） | core |
| Extract projection | 提取栅格投影写成world与prj文件 | gdal:extractprojection | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Warp (reproject) | 栅格重投影到另一坐标系 | gdal:warpreproject | GDAL 提供者（QGIS 封装 GDAL） | core |

#### Vector conversion（4 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Convert format | 矢量图层转任意OGR支持格式 | gdal:convertformat | GDAL 提供者（QGIS 封装 GDAL） | core |
| Rasterize (overwrite with attribute) | 用矢量属性值原地覆写已有栅格像元 | gdal:rasterize_over | GDAL 提供者（QGIS 封装 GDAL） | defer |
| Rasterize (overwrite with fixed value) | 用固定值原地覆写已有栅格像元 | gdal:rasterize_over_fixed_value | GDAL 提供者（QGIS 封装 GDAL） | defer |
| Rasterize (vector to raster) | 矢量点线面按属性或定值栅格化 | gdal:rasterize | GDAL 提供者（QGIS 封装 GDAL） | core |

#### Vector geoprocessing（7 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Buffer vectors | 给矢量要素建指定距离缓冲区 | gdal:buffervectors | GDAL 提供者（QGIS 封装 GDAL） | core |
| Clip vector by extent | 按矩形范围裁剪矢量 | gdal:clipvectorbyextent | GDAL 提供者（QGIS 封装 GDAL） | core |
| Clip vector by mask layer | 按掩膜面图层裁剪矢量 | gdal:clipvectorbypolygon | GDAL 提供者（QGIS 封装 GDAL） | core |
| Dissolve | 按属性值融合合并同值几何 | gdal:dissolve | GDAL 提供者（QGIS 封装 GDAL） | core |
| Offset curve | 线要素按距离平行偏移 | gdal:offsetcurve | GDAL 提供者（QGIS 封装 GDAL） | extension |
| One side buffer | 线要素单侧缓冲区 | gdal:onesidebuffer | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Points along lines | 沿线按间隔生成点 | gdal:pointsalonglines | GDAL 提供者（QGIS 封装 GDAL） | extension |

#### Vector miscellaneous（6 条）

| 官方名 | 一句话作用 | 算法ID | 轮子来源 | 平台判断 |
|---|---|---|---|---|
| Build virtual vector | 多个矢量数据源拼成虚拟矢量VRT | gdal:buildvirtualvector | GDAL 提供者（QGIS 封装 GDAL） | extension |
| Execute SQL | 对矢量图层执行SQL查询生成新图层 | gdal:executesql | GDAL 提供者（QGIS 封装 GDAL） | core |
| Export to PostgreSQL (available connections) | 用已有连接把矢量导入PostgreSQL，可覆写表 | gdal:importvectorintopostgisdatabaseavailableconnections | GDAL 提供者（QGIS 封装 GDAL） | defer |
| Export to PostgreSQL (new connection) | 新建连接把矢量导入PostgreSQL，可覆写表 | gdal:importvectorintopostgisdatabasenewconnection | GDAL 提供者（QGIS 封装 GDAL） | defer |
| Vector Information | 输出矢量图层元信息报告 | gdal:ogrinfo | GDAL 提供者（QGIS 封装 GDAL） | core |
| Vector Information (JSON) | 以JSON输出矢量图层元信息 | gdal:ogrinfojson | GDAL 提供者（QGIS 封装 GDAL） | extension |

## 4. 轮子来源与整域借道

平台原则（鱼鱼定版）：全部升级＋不重复造轮子。平台层只做**统一翻译与治理**，不自研任何已有现成实现的算法。

### 4.1 可整域借道的分析能力（现成轮子，平台零算法开发）

| 域 | 条数 | 借道入口（桥上已有） | 算法 ID 范围 | 接入代价构成 |
|---|---|---|---|---|
| Processing native 全域（矢量几何/叠加/分析、栅格分析/地形、插值、网络、图表等 27 组） | 300 条（`native:` 233＋`qgis:` 66＋`3d:` 1） | qgis 桥 `qgis_run_processing`（单入口，confirm 门）或将来的统一处理动词 | `native:*`、`qgis:*`、`3d:*` | 注册表建账＋参数模式缓存＋治理分级；无算法开发 |
| GDAL 全域（栅格式分析/转换/提取/投影＋矢量转换/地理处理 8 组） | 57 条 | 同上（`processing.run("gdal:...")`）；或合集内独立 gdal 桥（二选一，见建议 5） | `gdal:*` | 同上 |
| PDAL 点云域（转换/数据管理/提取 3 组） | 17 条 | 同上 | `pdal:*` | 同上；另需部署机 PDAL ≥2.5.0 |
| Processing 模型与脚本（Modeler tools 14 条＋模型运行机制） | 含在 native 计数内 | 经 Processing 模型文件运行 | `native:model*` 等 | 模型文件治理（版本、来源）而非算法治理 |

**结论**：平台「分析能力」的 374 条已建账算法，全部是借道题、没有一条需要自研。真正的接入工程量在三件治理物：①算法注册表（本清单即种子数据）；②每条算法的参数模式（可由运行时 `algorithmHelp()`/注册表枚举自动获取，不必人工抄）；③调用治理（confirm 门、defer 名单、输出落盘规则）。

### 4.2 真缺口（无现成轮子可借，或借道前必须先补的账）

1. **GRASS（400+ 模块）与 SAGA 全集——目录缺口**：3.40 官方用户指南没有逐条算法目录，官方页面连 `grass:`/`saga:` 的 ID 写法示例都未给出。在实机上用官方方法枚举 Processing 注册表（`processingRegistry().algorithms()`，见 23.7）建账之前，平台对这两域是「知道有、说不清」——这是全卷最大的未建账面。GRASS 还需外部程序＋专用 Provider 插件，SAGA 需外部程序，均有部署代价。
2. **算法发现与参数自描述——桥侧缺口**：官方运行时本有枚举与 `algorithmHelp()` 能力（轮子在 QGIS 里），但现有 qgis 桥没有暴露它，导致 374 条算法目前「名义可跑、无法建账校验」。这不是算法缺口，是桥的发现面缺口（建议 1）。
3. **桌面交互语义——无算法化轮子**：编辑/数字化会话、标注与符号的可视化编辑、三维视图导航、插件管理等域在官方体系里只有桌面 GUI 与 PyQGIS 对象模型，没有 Processing 入口。平台若要覆盖，只能经 PyQGIS 逐项做视图级动词（桥已有 set_layer_visible/zoom_to_layer 两条实验性先例），或明确 defer；不存在可整域借道的现成实现。
4. **跨软件统一语义翻译——平台唯一该自建的「轮子」**：表达式函数、符号/渲染模型、字段类型等在各 GIS 间无通用现成实现；统一入口要做的是翻译表与口径治理（这正是平台的本职，不是算法自研）。QGIS 表达式引擎规模大（用户指南专设「Level up with Expressions」章），全量翻译不现实，应按统一动词实际需要逐条建映射。
5. **其他外部提供者（OTB/LAStools/R 等）**：官方仅配置提及、无目录、无随装，统一按 defer 处理，等有真实需求再单独立项。

## 5. 差距：现有 qgis 桥 vs 官方全集

现有 qgis 桥共 **12 个工具**（`~/workspace/dsh-skills/gis-agent-bridges/manifest/tools-manifest.json` 实查；桥自述均为实验性/视图级，离线协议自检通过、未实机校准）。逐个对位：

| 桥工具 | 官方对应面 | 状态 |
|---|---|---|
| qgis_ping / qgis_discover | 桥自身协议（对应统一入口 gis_ping/gis_discover） | 已覆盖（平台动词，非 QGIS 功能） |
| qgis_project_info | PyQGIS 工程对象（QgsProject） | 已覆盖只读概览 |
| qgis_list_layers | PyQGIS 图层注册表 | 已覆盖只读 |
| qgis_list_layouts | PyQGIS 布局管理器 | 已覆盖只读（统一入口 v0 未收此动词） |
| qgis_list_fields | PyQGIS 矢量图层字段 | 已覆盖只读（统一入口 v0 未收此动词） |
| qgis_set_layer_visible / qgis_zoom_to_layer | PyQGIS 图层树/画布 | 已覆盖视图级（实验性） |
| qgis_add_layer_from_path | PyQGIS 加载图层（写，confirm 门） | 已覆盖单文件加载 |
| qgis_run_processing | **Processing 全域**（§3 的 374 条＋模型） | 名义全覆盖、无建账：无算法枚举、无参数模式校验、无 defer 拦截 |
| qgis_export_map_image | 画布/布局导出（Processing 亦有 native:printlayouttoimage 等） | 已覆盖（与 Processing 路径功能重叠） |
| qgis_save_project | PyQGIS 工程保存（写，confirm 门） | 已覆盖 |

按域量化：

| 能力域 | 官方全集 | 桥可达 | 可达方式与成色 |
|---|---|---|---|
| 工程/图层/字段/布局只读 | PyQGIS 对象面 | 核心项已达 | 桥原生工具，逐项显式实现 |
| Processing native 分析 | 300 条 | 300 条名义可达 | 经 qgis_run_processing 单入口；未建账、无参数校验 |
| GDAL 分析/转换 | 57 条 | 57 条名义可达 | 同上；另有独立 gdal 桥 7 工具覆盖 info/stats/convert 子集（双口径并存） |
| PDAL 点云 | 17 条 | 17 条名义可达 | 同上（依赖部署机 PDAL 版本，未验） |
| GRASS / SAGA | 官方称 GRASS 400+ 模块；SAGA 未给数 | 0 条建账 | 文档无目录、桥无枚举，完全未建账 |
| 编辑/数字化、标注符号编辑、三维视图、插件 | 桌面＋PyQGIS 面 | 0 | 无 Processing 入口，桥未做 PyQGIS 视图级扩展 |
| 统一入口 v0（平台层） | 8 个只读动词 | QGIS 侧对位 6 个 | QGIS 无「地图（map）」概念，gis_list_maps 在 v0 设计中即已注明不适用；gis_list_datasets 为 SuperMap 扩展，QGIS 走图层数据源字段 |

一句话差距：**桥的「点」已经够用（工程只读＋视图＋保存），Processing 的「面」名义全通但未建账，GRASS/SAGA 与桌面编辑面是空白。** 平台升级的杠杆不在逐条加工具，而在把 Processing 面建账＋治理。

## 6. 升级建议（按收益排序）

1. **先补「算法发现＋算法自描述」两个桥工具**（暴露 Processing 注册表枚举与 `algorithmHelp(id)`）。代价：两个只读工具。收益：374 条已建账算法从「名义可跑」变「可校验、可治理」，是后面所有整域接入的前置；枚举能力同时是 GRASS/SAGA 建账的唯一官方路径。
2. **Processing 整域按「一个执行面＋一张注册表」接入平台**：执行面复用 `qgis_run_processing`（不逐条造工具），平台侧维护算法注册表（本卷清单为种子，参数模式由建议 1 的自描述自动填充）＋按 core/extension 给统一翻译名。代价主要在注册表随 QGIS 版本更新的维护；收益是一次接入 374 条分析能力，且完全符合「不重复造轮子」。
3. **defer 名单做成治理层硬拦截**：本卷 50 条 defer 中，`qgis:executesql`/PostgreSQL·SpatiaLite 执行 SQL 类、原地覆写类（gdal:rasterize_over 等）、批量导出 PDF/图集类，应在网关层默认拒绝或双重确认。代价低（名单制），直接消除 Agent 调用 Processing 的主要副作用风险面。
4. **PDAL 点云域优先升格为平台试点**：17 条与鱼鱼的激光雷达点云竞赛主线（单木分割前处理：裁剪 clip、抽稀 thin、重投影 reproject、密度质检 density、导出栅格/TIN 建 DEM）直接重合；以点云工具组验证「注册表＋治理」模式，跑通后复制到其他域。
5. **GDAL 双口径收敛**：合集内独立 gdal 桥（7 工具）与 Processing 的 `gdal:`（57 条）功能重叠，平台层应定一处为准（建议以 Processing 注册表为准、gdal 桥保留为无 QGIS 环境时的独立部署形态），避免同一能力两套参数口径。
6. **GRASS/SAGA 先枚举、后接入，不凭文档外知识建账**：在装有 GRASS 的机器上跑一次注册表枚举生成清单，GRASS 优先（官方专章＋400+ 规模、且合集已有独立 grass 桥 7 工具可互证），SAGA 视需求后排。在此之前两域在平台注册表中标「未建账」，不许以记忆补条目。
7. **桌面域只借 PyQGIS、不追 GUI 全覆盖**：布局导出等已有 Processing 等价物（native:printlayouttoimage 等）的，不在桥上重复实现；编辑会话、三维导航等无算法入口的域维持 defer，等真实业务需求出现再逐项评估视图级动词。

---

*成文说明：§3 算法条目与 ID 逐字来自 docs.qgis.org 3.40 官方分组页（native 矢量组分卷注：官方名系按算法 ID 与页面简述核对还原，ID 为页面原文；栅格/GDAL 分卷以同站官方 RST 源文本与 HTML 页互证）。本卷与三份分卷底稿同目录存档。*

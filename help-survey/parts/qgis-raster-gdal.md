# QGIS 3.40 Processing 算法普查：native 栅格/点云/三维类分组 + GDAL 提供者全部分组

- 来源页：https://docs.qgis.org/3.40/en/docs/user_manual/processing_algs/index.html（各分组页为其下 qgis/ 与 gdal/ 子页，标题与算法 ID 以官方文档页面及其同站 RST 源文本逐字核对）
- 抓取日期：2026-11-02
- 范围说明：任务清单称 native 为 11 组，但入口页与任务枚举实际均为 10 组（下列 10 组）；GDAL 提供者 8 组全查。
- 判断口径：core=跨 GIS 软件共有的基础能力，适合升平台统一动词候选；extension=专属或分析型能力，经通用 Processing 入口暴露即可；defer=仅桌面交互、需外部专有工具或副作用风险大，暂不适合 Agent；拿不准标 extension。
- 注：点云各组算法在 QGIS 中由 PDAL 库（≥2.5.0）提供，故算法 ID 前缀为 `pdal:`，但分组归属 QGIS（native）提供者文档页。

## QGIS algorithm provider（native）

### 3D Tiles

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Convert B3DM to GLTF | 旧B3DM三维瓦片转GLTF/GLB | native:b3dmtogltf | extension |
| Convert GLTF to vector features | GLTF/GLB内容转矢量线面要素 | native:gltftovector | extension |

### Interpolation

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Heatmap (kernel density estimation) | 点核密度估计生成密度热力栅格 | qgis:heatmapkerneldensityestimation | extension |
| IDW Interpolation | 反距离加权插值点数据成栅格 | qgis:idwinterpolation | core |
| Line Density | 计算邻域内线要素长度密度栅格 | native:linedensity | extension |
| TIN Interpolation | TIN三角网插值点数据成栅格 | qgis:tininterpolation | core |

### Mesh

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Export contours | 由网格标量数据集生成等值线和面 | native:meshcontours | extension |
| Export cross section dataset values on lines from mesh | 沿线提取网格数据集值导出CSV | native:meshexportcrosssection | extension |
| Export mesh edges | 网格边导出为带数据集值的线矢量 | native:exportmeshedges | extension |
| Export mesh faces | 网格面导出为带数据集值的面矢量 | native:exportmeshfaces | extension |
| Export mesh on grid | 网格数据集采样到规则格网点矢量 | native:exportmeshongrid | extension |
| Export mesh vertices | 网格顶点导出为带数据集值的点矢量 | native:exportmeshvertices | extension |
| Export time series values from points of a mesh dataset | 在点位提取网格数据集时间序列值 | native:meshexporttimeseries | extension |
| Rasterize mesh dataset | 网格数据集栅格化为栅格图层 | native:meshrasterize | extension |
| TIN mesh creation | 矢量层经Delaunay三角化建TIN网格 | native:tinmeshcreation | extension |

### Point Cloud Conversion

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Convert format | 点云转LAS/LAZ/COPC/VPC等格式，如压成LAZ | pdal:convertformat | core |
| Export to raster | 按指定属性把点云栅格化导出TIF | pdal:exportraster | core |
| Export raster (using triangulation) | 三角化插值点云生成地形栅格，点稀时建DEM用 | pdal:exportrastertin | extension |
| Export to vector | 点云导出为三维点矢量GeoPackage | pdal:exportvector | core |

### Point Cloud Data Management

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Assign projection | 给CRS缺失或错误的点云赋予坐标系 | pdal:assignprojection | core |
| Build virtual point cloud (VPC) | 多份点云拼成虚拟点云，可选边界统计与概览 | pdal:virtualpointcloud | extension |
| Clip | 用面图层裁点云，只留面内点，竞赛按区裁剪用 | pdal:clip | core |
| Create COPC | 批量为点云文件生成COPC索引 | pdal:createcopc | extension |
| Information | 输出点云元数据：点数、范围、CRS、属性表 | pdal:info | core |
| Merge | 多份点云文件合并为一份 | pdal:merge | core |
| Reproject | 点云重投影到另一坐标系 | pdal:reproject | core |
| Thin (by sampling radius) | 按采样半径抽稀，半径内只留一点，降密度 | pdal:thinbyradius | extension |
| Thin (by skipping points) | 每隔N个点保留一个抽稀点云 | pdal:thinbydecimate | extension |
| Tile | 点云按边长切分瓦片，大数据分块处理用 | pdal:tile | extension |

### Point Cloud Extraction

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Boundary | 提取点云覆盖边界多边形，可含洞 | pdal:boundary | extension |
| Density | 每格点数成密度栅格，质检点云疏密空洞 | pdal:density | extension |
| Filter | 按PDAL表达式或矩形范围筛点，如按分类码提地面点 | pdal:filter | core |

### Raster analysis

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Cell stack percent rank from value | 算给定值在栅格叠栈中的百分位排名 | native:cellstackpercentrankfromvalue | extension |
| Cell stack percentile | 栅格叠栈逐像元百分位值计算 | native:cellstackpercentile | extension |
| Cell stack percentrank from raster layer | 以一栅格逐像元值算叠栈百分位排名 | native:cellstackpercentrankfromrasterlayer | extension |
| Cell statistics | 多栅格逐像元统计，如均值中位数 | native:cellstatistics | core |
| Equal to frequency | 统计叠栈中等于给定值的频次 | native:equaltofrequency | extension |
| Fuzzify raster (gaussian membership) | 高斯隶属函数把栅格值模糊化到0至1 | native:fuzzifyrastergaussianmembership | extension |
| Fuzzify raster (large membership) | 大值隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasterlargemembership | extension |
| Fuzzify raster (linear membership) | 线性隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasterlinearmembership | extension |
| Fuzzify raster (near membership) | 近值隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasternearmembership | extension |
| Fuzzify raster (power membership) | 幂隶属函数把栅格值模糊化到0至1 | native:fuzzifyrasterpowermembership | extension |
| Fuzzify raster (small membership) | 小值隶属函数把栅格值模糊化到0至1 | native:fuzzifyrastersmallmembership | extension |
| Greater than frequency | 统计叠栈中大于给定值的频次 | native:greaterthanfrequency | extension |
| Highest position in raster stack | 找叠栈中最大值所在的层序号 | native:highestpositioninrasterstack | extension |
| Less than frequency | 统计叠栈中小于给定值的频次 | native:lessthanfrequency | extension |
| Lowest position in raster stack | 找叠栈中最小值所在的层序号 | native:lowestpositioninrasterstack | extension |
| Raster boolean AND | 多个栅格逐像元布尔与运算 | native:rasterbooleanand | core |
| Raster boolean OR | 多个栅格逐像元布尔或运算 | native:rasterbooleanor | core |
| Raster calculator | 表达式逐像元栅格计算 | native:rastercalc | core |
| Raster calculator (virtual) | 表达式生成即时计算的虚拟栅格 | native:virtualrastercalc | core |
| Raster layer properties | 输出栅格范围、CRS、行列数等属性 | native:rasterlayerproperties | extension |
| Raster layer statistics | 计算栅格波段基本统计量 | native:rasterlayerstatistics | core |
| Raster layer unique values report | 报告栅格唯一值及各自像元数 | native:rasterlayeruniquevaluesreport | extension |
| Raster layer zonal statistics | 按分区统计栅格像元值 | native:rasterlayerzonalstats | extension |
| Raster surface volume | 计算栅格表面与基准面间体积 | native:rastersurfacevolume | extension |
| Reclassify by layer | 按另一图层的值表重分类栅格 | native:reclassifybylayer | core |
| Reclassify by table | 按数值区间表重分类栅格 | native:reclassifybytable | core |
| Rescale raster | 栅格值线性拉伸到新数值范围 | native:rescaleraster | extension |
| Round raster values | 栅格像元值按指定方式取整 | native:roundrastervalues | extension |
| Sample raster values | 在点要素位置采样栅格像元值 | native:rastersampling | core |
| Zonal histogram | 分区统计各栅格值的像元数成表 | native:zonalhistogram | extension |
| Zonal statistics | 按面分区汇总栅格统计量到属性 | native:zonalstatisticsfb | core |

### Raster Creation

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Create constant raster layer | 按范围与像元大小生成常数填充栅格 | native:createconstantrasterlayer | extension |
| Create random raster layer (binomial distribution) | 生成二项分布随机值栅格 | native:createrandombinomialrasterlayer | extension |
| Create random raster layer (exponential distribution) | 生成指数分布随机值栅格 | native:createrandomexponentialrasterlayer | extension |
| Create random raster layer (gamma distribution) | 生成伽马分布随机值栅格 | native:createrandomgammarasterlayer | extension |
| Create random raster layer (geometric distribution) | 生成几何分布随机值栅格 | native:createrandomgeometricrasterlayer | extension |
| Create random raster layer (negative binomial distribution) | 生成负二项分布随机值栅格 | native:createrandomnegativebinomialrasterlayer | extension |
| Create random raster layer (normal distribution) | 生成正态分布随机值栅格 | native:createrandomnormalrasterlayer | extension |
| Create random raster layer (poisson distribution) | 生成泊松分布随机值栅格 | native:createrandompoissonrasterlayer | extension |
| Create random raster layer (uniform distribution) | 生成均匀分布随机值栅格 | native:createrandomuniformrasterlayer | extension |

### Raster terrain analysis

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Aspect | 由DEM计算坡向，0至360度 | qgis:aspect | core |
| DTM filter (slope-based) | 坡度法滤波DEM，分地面与非地面像元 | native:dtmslopebasedfilter | extension |
| Hillshade | 按太阳方位高度角生成山体阴影 | qgis:hillshade | core |
| Hypsometric curves | 计算DEM高程面积曲线输出CSV | qgis:hypsometriccurves | extension |
| Relief | 生成分级设色的地貌晕渲栅格 | qgis:relief | extension |
| Ruggedness index | 计算地形粗糙度指数栅格 | qgis:ruggednessindex | extension |
| Slope | 由DEM计算坡度栅格 | qgis:slope | core |

### Raster tools

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Align raster | 单栅格对齐到参考栅格，仅建模器上下文可用 | native:alignsingleraster | defer |
| Align rasters | 多栅格重采样重投影对齐到参考栅格 | native:alignrasters | core |
| Convert map to raster | 把当前地图画布内容渲染为栅格图 | native:rasterize | defer |
| Fill NoData cells | 用指定值填满栅格NoData像元 | native:fillnodata | core |
| Generate XYZ tiles (Directory) | 生成XYZ瓦片目录供Web地图用 | native:tilesxyzdirectory | extension |
| Generate XYZ tiles (MBTiles) | 生成MBTiles单文件瓦片包 | native:tilesxyzmbtiles | extension |

## GDAL algorithm provider

### Raster analysis

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Aspect | 由DEM计算坡向 | gdal:aspect | core |
| Color relief | 按色表文件把DEM渲染为彩色地貌图 | gdal:colorrelief | extension |
| Fill NoData | 插值填补栅格NoData空洞并平滑 | gdal:fillnodata | core |
| Grid (Data metrics) | 点数据按窗口统计格网化，如最小最大值 | gdal:griddatametrics | extension |
| Grid (IDW with nearest neighbor searching) | 最近邻搜索的反距离加权点插值格网 | gdal:gridinversedistancenearestneighbor | extension |
| Grid (Inverse distance to a power) | 反距离幂点插值格网化 | gdal:gridinversedistance | core |
| Grid (Linear) | 线性插值把点数据格网化 | gdal:gridlinear | extension |
| Grid (Moving average) | 移动平均把点数据格网化 | gdal:gridaverage | extension |
| Grid (Nearest neighbor) | 最近邻把点数据格网化 | gdal:gridnearestneighbor | extension |
| Hillshade | 由DEM生成山体阴影 | gdal:hillshade | core |
| Near black | 把近黑近白的边缘像元设黑或透明 | gdal:nearblack | extension |
| Proximity (raster distance) | 生成到目标像元的距离栅格 | gdal:proximity | extension |
| Roughness | 计算地形粗糙度，邻域高程最大差 | gdal:roughness | extension |
| Sieve | 筛除小于阈值的零散像元斑块 | gdal:sieve | extension |
| Slope | 由DEM计算坡度 | gdal:slope | core |
| Terrain Ruggedness Index (TRI) | 计算地形粗糙度指数TRI | gdal:triterrainruggednessindex | extension |
| Topographic Position Index (TPI) | 计算地形位置指数TPI | gdal:tpitopographicpositionindex | extension |

### Raster conversion

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| gdal2xyz | 栅格导出为XYZ ASCII文本 | gdal:gdal2xyz | extension |
| PCT to RGB | 调色板8位影像转24位RGB | gdal:pcttorgb | extension |
| Polygonize (raster to vector) | 同值连通像元转面矢量，栅格转矢量 | gdal:polygonize | core |
| Rearrange bands | 选取并重排栅格波段生成新栅格 | gdal:rearrange_bands | extension |
| RGB to PCT | RGB影像转8位调色板影像 | gdal:rgbtopct | extension |
| Translate (convert format) | 栅格格式转换，可改尺寸类型与范围 | gdal:translate | core |

### Raster extraction

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Clip raster by extent | 按矩形范围裁剪栅格 | gdal:cliprasterbyextent | core |
| Clip raster by mask layer | 按矢量掩膜面裁剪栅格 | gdal:cliprasterbymasklayer | core |
| Contour | 由高程栅格提取等高线矢量 | gdal:contour | core |
| Contour Polygons | 由高程栅格提取等高线面矢量 | gdal:contour_polygon | extension |

### Raster miscellaneous

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Build overviews (pyramids) | 为栅格建金字塔概览加速渲染 | gdal:overviews | extension |
| Build virtual raster | 多栅格拼成VRT虚拟镶嵌数据集 | gdal:buildvirtualraster | core |
| gdal2tiles | 栅格切成Web瓦片目录并生成查看页 | gdal:gdal2tiles | extension |
| Merge | 多个栅格合并镶嵌为一幅 | gdal:merge | core |
| Pansharpening | 全色与多光谱影像融合锐化 | gdal:pansharp | extension |
| Raster calculator | 用GDAL表达式逐像元栅格计算 | gdal:rastercalculator | core |
| Raster information | 输出栅格元信息报告 | gdal:gdalinfo | core |
| Retile | 成套瓦片重切分并建金字塔 | gdal:retile | extension |
| Tile index | 为栅格集建瓦片索引面矢量 | gdal:tileindex | extension |
| Viewshed | 由DEM计算指定观测点可视域 | gdal:viewshed | extension |

### Raster projections

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Assign projection | 给栅格数据集赋予坐标系信息 | gdal:assignprojection | core |
| Extract projection | 提取栅格投影写成world与prj文件 | gdal:extractprojection | extension |
| Warp (reproject) | 栅格重投影到另一坐标系 | gdal:warpreproject | core |

### Vector conversion

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Convert format | 矢量图层转任意OGR支持格式 | gdal:convertformat | core |
| Rasterize (overwrite with attribute) | 用矢量属性值原地覆写已有栅格像元 | gdal:rasterize_over | defer |
| Rasterize (overwrite with fixed value) | 用固定值原地覆写已有栅格像元 | gdal:rasterize_over_fixed_value | defer |
| Rasterize (vector to raster) | 矢量点线面按属性或定值栅格化 | gdal:rasterize | core |

### Vector geoprocessing

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Buffer vectors | 给矢量要素建指定距离缓冲区 | gdal:buffervectors | core |
| Clip vector by extent | 按矩形范围裁剪矢量 | gdal:clipvectorbyextent | core |
| Clip vector by mask layer | 按掩膜面图层裁剪矢量 | gdal:clipvectorbypolygon | core |
| Dissolve | 按属性值融合合并同值几何 | gdal:dissolve | core |
| Offset curve | 线要素按距离平行偏移 | gdal:offsetcurve | extension |
| One side buffer | 线要素单侧缓冲区 | gdal:onesidebuffer | extension |
| Points along lines | 沿线按间隔生成点 | gdal:pointsalonglines | extension |

### Vector miscellaneous

| 官方名 | 作用 | 算法ID | 判断 |
|---|---|---|---|
| Build virtual vector | 多个矢量数据源拼成虚拟矢量VRT | gdal:buildvirtualvector | extension |
| Execute SQL | 对矢量图层执行SQL查询生成新图层 | gdal:executesql | core |
| Export to PostgreSQL (available connections) | 用已有连接把矢量导入PostgreSQL，可覆写表 | gdal:importvectorintopostgisdatabaseavailableconnections | defer |
| Export to PostgreSQL (new connection) | 新建连接把矢量导入PostgreSQL，可覆写表 | gdal:importvectorintopostgisdatabasenewconnection | defer |
| Vector Information | 输出矢量图层元信息报告 | gdal:ogrinfo | core |
| Vector Information (JSON) | 以JSON输出矢量图层元信息 | gdal:ogrinfojson | extension |

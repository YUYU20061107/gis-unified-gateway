# PHASE 3 · iServer 评估接入报告

- 日期：2026-11-06
- 状态：**通过（demo-instance-verified，非本机校准）**
- 探针目标：`https://iserver.supermap.io/iserver`（SuperMap 官方公开演示实例）
- 纪律：**只读，只发 GET**；未发任何 POST/PUT/DELETE，未访问管理接口，
  未执行空间分析/写操作。
- 起点：Phase 2 验收提交 `b829322`；Phase 4 经批准先做；本阶段解封后完成。
- 证据目录：`evidence/phase3/`
- 后续：Phase 4B 已完成 PostGIS 隔离本地集群真后端（模板 38/38 + 网关
  21/21），见 `PHASE4-POSTGIS-REPORT.md`；本文的 PostGIS 未做说明是当时快照。

## 1. 目标

先写探针确认 iServer REST 的真实形状（服务目录、地图 REST、数据 REST、
空间分析），再写最小映射；接口证伪的动词记 not_supported，不许凭文档猜。

## 2. 探针过程与真实形状（全部 GET）

### 2.1 服务目录

```
GET /iserver/services.json  → 200, 53,182 bytes, JSON list
```

- 服务总数 **115**。
- 组件计数：MapImpl **56**、DataImpl **29**、SpatialAnalystImpl **5**、
  ImageImpl 7、GeometryComponentImpl 3、TransportationAnalystImpl 2、
  TrafficTransferAnalystImpl 2、VideoHLSComponentImpl 2、componentSetType 2，
  其余 VectorTile/NetworkAnalyst3D/AddressMatch/Realspace/Plot/DataCatalog/
  Webprinting 各 1。
- 条目字段：`componentType`、`interfaceType`、`alias`、`name`、`url`、
  `status`、`additions`、`modifyTime/createTime`。
- 版本：**未确认**（services.json 无版本字段；未找到可用的版本 GET 端点；
  响应头只有 nginx，不透露 iServer 版本）。

### 2.2 地图 REST（已确认）

```
GET /services/map-china/rest/maps.json                    → 200, 2,853 B
GET /services/map-china/rest/maps/China.json              → 200, 4,035 B
GET /services/map-china/rest/maps/China/layers.json       → 200, 491,738 B
```

- `maps.json`：JSON list，4 个地图 `China / China_4326 / ChinaLight / ChinaDark`；
  每项 `resourceConfigID`、`supportedMediaTypes`、`path`、`name`、`resourceType`。
- `China.json`：40 个键；含 `name`、`bounds`、`prjCoordSys`
  （`WGS 84 /Pseudo-Mercator`，EPSG:3857）、`mapCapabilities` 19 项。
- `layers.json`：JSON list，1 个顶层图层 `China`，`subLayers.layers` **13** 个；
  顶层字段含 `name/caption/visible/type/queryable/bounds/fields`。

### 2.3 数据 REST（已确认）

首次按 `data-*/rest/datasets.json` 探得 **404**（路径不匹配），按真实
CatalogList 路径重探：

```
GET /services/data-china/rest.json                                      → 200, 678 B
GET /services/data-china/rest/data/datasources.json                     → 200, 157 B
GET /services/data-china/rest/data/datasources/name/China/datasets.json → 200, 6,156 B
```

- `rest.json`：资源目录 list，含 `data`（CatalogList）、`search` 等。
- `datasources.json`：`{datasourceNames:["China"], datasourceCount:1,
  childUriList:[...]}`。
- `datasets.json`：`{datasetCount:47, datasetNames:[...]}`，前 10 个
  `Province_L, Lake_R, MainRiver_L, MainRiver_R, City_L, County_L, Capital_P,
  GangAo_L, IslandsName_P, City_P`。

### 2.4 空间分析（形状已确认，执行未尝试）

```
GET /services/spatialanalyst-sample/restjsr                    → 200, 209 B
GET /services/spatialanalyst-sample/restjsr/spatialanalyst     → 200, 399 B
GET /services/spatialanalyst-sample/restjsr/spatialanalyst/datasets   → 200, 77,877 B
GET /services/spatialanalyst-sample/restjsr/spatialanalyst/geometry   → 200, 5,683 B
```

- `restjsr`：JSON list，1 个资源 `spatialanalyst`，`path` 指向
  `/restjsr/spatialanalyst`。
- `/spatialanalyst`：资源 `datasets`、`geometry`。
- `/spatialanalyst/datasets`：27 个数据集；首项的 `childResourceInfos` 含
  `buffer`、`densityanalyst`、`extractvector3d`、`georelation`、
  `interpolation`、`isoline`、`isoregion`、`mindistance`、`overlay`、
  `thiessenpolygon` 等。
- `/spatialanalyst/geometry`：25 个几何操作。
- **未执行任何空间分析**：执行需要 POST，违反本次只读规则；只确认了根/
  子资源形状，不把“形状已确认”写成“可执行已验”。

### 2.5 可用性观察

演示实例并非所有服务都稳定：`map-Jingjin-3/rest`、`data-chart2/rest`、
`spatialanalyst-sample/restjsr` 曾在不同批次返回 **502**；`data-*/rest/
datasets.json` 为 **404**（路径不匹配，不是服务缺失）。最终按正确路径
重探，§2.1–§2.4 的 11 个端点全部 **200**。本报告只以最终可复现的 200
结果作为形状证据，并保留原始 502/404 文件作为历史。

## 3. 最小映射（只登记已确认的只读面）

新增第 11 后端 `iserver`，`code/iserver_server.py`（纯标准库，GET-only）：

| 统一面 | 原生工具 | 已确认证据 |
|---|---|---|
| 基础 `gis_ping` | `iserver_ping` | services.json 200 / 115 |
| 基础 `gis_discover` | `iserver_discover` | 组件计数 56/29/5 |
| 基础 `gis_project_info` | `iserver_project_info` | kind=service + 115 |
| 基础 `gis_list_maps` | `iserver_list_maps` | map-china 4 地图 |
| 基础 `gis_list_layers` | `iserver_list_layers` | China 1 顶层/13 子层 |
| 基础 `gis_list_datasets` | `iserver_list_datasets` | data-china/China 47 数据集 |
| V35 `gis_list_services` | `iserver_list_services` | services.json 115 |

- 账本只新增 **V35@iserver 1 叶**（基础动词不计入 leaves-full）：
  `status=ok, kind=native, native=iserver_list_services, bts=existing,
  tier=extended`。
- 总账：207 → **208＝ok 165＋unverified 21＋not_supported 22**；
  existing 22→23；tier core 174／extended 30／exclusive 4；后端 11。
- **未登记**：空间分析执行、写/删/改、发布、导入、任何需要 POST 的动词。
  不是“证伪为 not_supported”，而是“只读规则下未验证”，故不写映射、不写叶子。
- `data` 面只登记只读列表（`gis_list_datasets`）；没有写/编辑映射。

证据标注：**`demo-instance-verified`**（官方公开演示、非本机、版本未确认、
仅 GET）。**不标 calibrated**；本机校准留待后续。

## 4. 真跑验收

`test_iserver_demo.py`：桥 7 项 + 网关 7 项，全部 GET：

```
checks: 14, passed: 14, failed: 0
```

覆盖：桥 ping/discover/project_info/list_maps/list_layers/list_datasets/
list_services；网关 `gis_ping/discover/project_info/list_maps/list_layers/
list_datasets/list_services@iserver`。结果
`evidence/phase3/iserver-demo-results.json`。

其他同步证据：

- `selftest.py` **154/154**（新增 C13 iserver mock discover；A7 覆盖 iServer
  工具；A10 tier core174/ext30/excl4）。
- 生成器干净副本 **6/6** 产物字节一致。
- 全部请求方法均为 GET；桥的 `_get_json` 固定 `method="GET"`，没有写路径。

## 5. 与本机 iServer 实例的差距

| 维度 | 演示实例（本次） | 本机实例（未做） |
|---|---|---|
| 版本 | **未确认**（无版本端点/响应头） | 未知；需本机确认 |
| 部署 | 公网 `iserver.supermap.io`，经本机代理 127.0.0.1:7897 | 本机/内网，网络稳定 |
| 示例数据 | 115 服务；map-china 4 地图/China 13 子层；data-china 47 数据集；spatial 27 数据集/25 几何操作 | 数据源、地图、服务名均可能不同 |
| 权限模型 | services.json 与 GET 端点匿名可读；未见 token/401/403 | 可能需要 token/角色/服务权限；未测 |
| 空间分析 | 仅根/子资源形状；执行未尝试（POST 禁止） | 执行/权限/结果写回均未验 |
| 稳定性 | 部分服务 502、错误路径 404，最终 11/11 200 | 本地应稳定；未测 |
| 校准等级 | `demo-instance-verified` | 未做，不能称 calibrated |

## 6. 账面数字变化对照表

| 项目 | 阶段前 | 阶段后 | 说明 |
|---|---|---|---|
| 后端数 | 10 | **11** | +iServer（官方演示只读） |
| 叶子总数 | 207 | **208** | +V35 iserver |
| ok | 164 | **165** | V35 iserver |
| unverified | 21 | **21** | 不变 |
| not_supported | 22 | **22** | 不变 |
| pending／existing | 21／22 | **21／23** | V35 existing |
| tier core／extended／exclusive | 174／29／4 | **174／30／4** | V35 extended |
| 自检 | 153/153 | **154/154** | C13 iServer mock discover |
| 生成器 | 6/6 | **6/6** | 含 iServer 注册表 |
| iServer 实跑 | 0 | **14/14** | 全部 GET |

## 7. `git diff` 逐项解释

| 文件 | 改动 | 原因 |
|---|---|---|
| `code/iserver_server.py` | 新增 7 工具 GET-only 适配 | iServer 演示只读后端 |
| `probe_iserver_demo.py` | 新增只读探针 | 形状证据可复现 |
| `test_iserver_demo.py` | 新增 14 项验收 | 桥+网关真跑 |
| `code/backends.json` | +iserver，level=demo-instance-verified | 第 11 后端 |
| `code/build_mapping.py` | +ISERVER_TOOLS、基础 TABLE、V35、BACKEND_META | 生成器同账 |
| `code/gateway.py` | list_layers/list_datasets 的 iServer 分支 | 基础动词翻译 |
| `code/mapping.json` / `verbs.json` / `mock_tools.json` | +iServer 映射/工具 | 生成器产出 |
| `code/selftest.py` / `selftest-results.txt` | +C13、A7/A10 调整、154 | 离线自检覆盖 |
| `leaves-full.json` | +V35 iserver 1 叶 | 账本 |
| `code/README.md` / V2 / V1 / G3 / CHANGELOG / PHASE1/2/4/5 | 208/165/21/22、tier 174/30/4、demo 标注 | 文档终对账 |
| `evidence/phase3/*` | 探针 JSON、原始 200/502/404、14/14、154、6/6 | 证据落盘 |

## 8. 未完成与原因

1. **本机 iServer 校准**：本机无实例；演示实例的 `demo-instance-verified`
   不能替代本机校准，不标 calibrated。
2. **版本/权限模型**：演示实例版本未确认；匿名 GET 可用；本机可能需
   token/角色，未测。
3. **空间分析执行**：只确认了根/子资源形状；执行需 POST，按只读规则未做，
   因此没有登记任何空间分析执行映射。
4. **写操作**：iServer 的编辑/发布/导入/删除等一律未映射；本阶段没有写。
5. **演示数据差异**：115 服务/4 地图/47 数据集/27 空间数据集只是演示样本；
   本机实例的示例数据不同。

## 9. 入口/后续

阶段 3 已按“只读演示实例”完成最小接入。后续若拿到本机 iServer：

1. 用同一 `iserver_server.py` 的 GET 工具做本机只读校准（版本/权限/数据）；
2. 空间分析执行另开写阶段，先确认 POST 契约与确认门，再逐项校准；
3. 不得把本次 `demo-instance-verified` 升格为 `calibrated`，除非有本机证据。

## 10. 证据索引

- `evidence/phase3/iserver-demo-probe.json`：最终 11 端点 200 形状
- `evidence/phase3/probe-run.log`：探针运行输出
- `evidence/phase3/services.json`：115 服务原始目录
- `evidence/phase3/probe-*.body`：包括 502/404 历史与最终 200 原始响应
- `evidence/phase3/iserver-demo-results.json`：14/14 逐项
- `evidence/phase3/iserver-demo.log`：14/14 完整输出
- `evidence/phase3/selftest-154.log` / `selftest-results-154.txt`：154/154
- `evidence/phase3/product-compare.txt`：生成器 6/6
- `evidence/phase3/generator-phase3.log`：生成器 stdout
- `evidence/phase3/accounting.txt`：207→208 对照（见 §6）

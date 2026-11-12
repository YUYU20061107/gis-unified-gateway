# 平台数据目录（data-catalog）

GIS 综合平台的数据层（B 阶段）：一份**可登记、可检索、可核许可**的数据集索引，
回答「平台里有什么数据、能不能用、在哪」。它与任何厂商工作空间的现场状态
不是一回事——这里登记的是平台的离线资产（见 `../gateway-v0/PHASE-B-DATA-LAYER.md`
的「先分清两个 datasets」）。

在统一入口里，它是第五个后端 `backend=catalog`（与四家 GIS 桥并列，注册在
`../gateway-v01/backends.json`）：网关的 `gis_discover` 实时调它聚合出
`data_catalog` 一节（计数 + 许可摘要透传），`gis_list_datasets`
（backend=catalog）回核心对象 dataset。对象模型与 STAC 映射见
`../gateway-v01/OBJECT-MODEL-V01.md`。

## 结构

```
data-catalog/
  catalog_server.py   # stdio MCP 服务端（纯标准库）：gis_catalog_list / gis_catalog_describe
  build_catalog.py    # 由 datasets/*/dataset.json 校验后汇总生成 catalog.json
  catalog.json        # 全量索引（生成物，勿手改；改登记后重跑 build_catalog.py）
  datasets/<id>/
    dataset.json      # 登记记录（字段见下）
    README.md         # 人读说明：拿到后怎么用、已知坑
  sources/            # 来源/许可页快照位（见 sources/README.md）
```

**数据本体不进本目录**：dataset.json 只登记 `storage.uri`（上游官方入口 /
本地路径），本目录不下载、不存放任何数据本体。

## 当前登记（9 条，均为 registered）

商用安全底座（许可口径引 MATERIALS-INDEX 第二部分，逐条带 evidence_ref）：
Natural Earth、Copernicus DEM、Sentinel-2、SRTM、AW3D30、ESA WorldCover、
Landsat、HydroSHEDS、OpenStreetMap。类型分布：dem 3 / imagery 2 /
vector 2 / raster 1 / network 1；本批 9 条 commercial_use 均为 true，
但各自的署名等义务仍以每条 `license.attribution` 为准。

## 登记字段（dataset.json）

| 字段 | 说明 |
|---|---|
| `id` | 稳定短 id，如 `natural-earth` |
| `name` | {en, zh} 数据集名 |
| `type` | vector / raster / imagery / dem / poi / network / table |
| `source` | {provider, url, retrieved_at, upstream}——不许只写「网上下载」 |
| `license` | {name, commercial_use: true/false/"unknown", attribution, evidence_ref}——许可要有据可查，查不到标 unknown，不许默认可用 |
| `coverage` | {bbox, crs, temporal_start, temporal_end, region_name} |
| `format` | {name, spec} 本体格式与规格 |
| `update` | {frequency, last_checked, upstream_version} |
| `storage` | {uri, size_bytes, checksum}——本体存放处与校验 |
| `quality_notes` | 已知问题（偏移、坐标系、国界画法红线等）如实写 |
| `status` | registered / verified / deprecated |

状态口径：`registered` = 仅登记、未打开本体验证；`verified` 只给实际打开
验过结构的那条（本批没有）。目录的 calibration 因此如实声明 `uncalibrated`：
**登记 ≠ 验证**。

## 许可闸（写进回包结构，不靠口头约定）

catalog_server 的每条回包记录自带 `license_gate`（许可名、commercial_use、
引用提示）；`commercial_use != true` 的条目另带 `commercial_use_notice`。
网关一侧再把许可摘要（by_license / by_commercial_use）透传进每次
`gis_discover` 的 data_catalog 一节。Agent 不得默认任何数据集可商用；
引用许可结论时带该条的 `license.evidence_ref`。

## 怎么用

```bash
python3 build_catalog.py     # 登记变更后重生 catalog.json（字段/许可/commercial_use 类型校验，缺字段报错退出）
python3 catalog_server.py    # stdio MCP 服务端，一般由网关按 backends.json 拉起
```

直连 catalog_server 的两工具：

- `gis_catalog_list`：列全部登记（可按 `type` / `commercial_use` 过滤），
  回包含 counts（total / by_type / by_license / by_commercial_use）、
  index_updated_at 与逐条 annotate 后的记录；
- `gis_catalog_describe`：按 `id` 返回单条完整记录 + license_gate；
  id 不存在回 `DATASET_NOT_FOUND` 并附 available_ids。

数据源口径：优先读同目录 `catalog.json`；缺失时回退直扫 `datasets/`
（index_updated_at 为 null 并附注）。**catalog.json 与登记文件不一致时，
以重跑 build_catalog.py 为准**，不要手改生成物。

## 新增一条登记

1. 建 `datasets/<id>/`，按上表写 dataset.json：许可字段逐项查证，
   `license.evidence_ref` 指向证据（MATERIALS-INDEX 条目或 sources/ 下的
   许可页快照）；查不到的字段写 unknown / null，**不许编**。
2. 同目录写 README.md：获取方式、怎么用、已知坑，末行标当前 status。
3. 跑 `python3 build_catalog.py` 重生 catalog.json（校验不过先修登记，别改脚本放行）。
4. status 只写 registered；实际下载并打开验过结构后，才可另行改 verified
   并在 quality_notes 里写明验了什么。

## 边界

- 不下载数据本体、不批量爬取数据源站；不做数据加工/切片管线（另立项）。
- 涉中国国界/行政界线的数据（如 Natural Earth）不得直接上架公开展示，
  逐条红线写在各 dataset.json 的 quality_notes 里（源出 MATERIALS-INDEX B0）。
- 本目录的登记内容本版未改动过校验口径：build_catalog.py 的必填字段集与
  catalog_server 的 REQUIRED_FIELDS 保持一致（11 项）。

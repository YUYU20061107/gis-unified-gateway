# PHASE 4B · PostGIS 真后端接入报告

- 日期：2026-11-06
- 状态：**通过（local-instance-verified；生产 DSN 未配置）**
- 目标：把网关的 PostGIS 后端从「离线协议自检」推进到真实 PostgreSQL/PostGIS
  实例上的端到端执行。
- 纪律：不猜本机 5432 实例密码；不改生产数据；使用隔离临时集群。

## 1. 方法（隔离集群，不碰生产实例）

- 用 PostgreSQL 16 自带 `initdb` 建临时集群：
  - `--auth=trust`、`--encoding=UTF8`、`--locale=C`；
  - 随机空闲端口、临时数据目录、测试结束自动 `pg_ctl stop` 并删除；
  - 数据库 `gisplat_test`，扩展 `postgis` + `postgis_raster`。
- 实测版本：**PostgreSQL 16.15 / PostGIS 3.6**（`PostGIS_Version()` 实测）。
- 本机 5432 生产实例未登录、未改任何数据；`production_dsn_untouched=true`
  写入结果 JSON。

## 2. 先纠正一个假通过（重要）

原 `test_templates_live.py` 把 DSN 放在 `psql` 选项前：

```
psql "dbname=..." -X -q -v ON_ERROR_STOP=1 -At -c "<sql>"
```

Windows `psql` 会忽略 DSN 之后的 `-c`，可能进入交互/空跑，旧存档 38/38
因此在方法上不可信。本次改为：

```
psql -d "dbname=..." -X -q -v ON_ERROR_STOP=1 -At -c "<sql>"
```

并在隔离集群上重新建 fixtures、逐条真实执行：**38/38 PASS**（含建表、
矢量/栅格模板、校验修复、MVT、删除回执等）。原始 502/空跑历史不再作为
证据；新证据在 `evidence/phase4-postgis/`。

## 3. PostGIS 适配层

新增 `code/postgis_server.py`（stdio MCP，psycopg2；本机由 QGIS 3.44.15
自带 Python 运行）：

| 工具 | 作用 |
|---|---|
| `postgis_ping` | PostgreSQL/PostGIS 版本、库、用户 |
| `postgis_discover` | 版本 + geometry_columns/raster_columns 计数 |
| `postgis_list_spatial_tables` | 空间表/几何列/类型/SRID（返回 list，供基础动词包装） |
| `postgis_table_summary` | 行数、几何列、extent |
| `postgis_table_columns` | information_schema 列清单 |
| `postgis_exec_template` | 只执行 36 个在册 template_id 的渲染 SQL；值走 psycopg2 绑定；要求 confirm=true |
| `postgis_export_geojson` | 表→GeoJSON 文件（ST_AsGeoJSON + jsonb_agg） |

`backends.json`：
- command 改为 `QGIS Python + {here}/postgis_server.py`；
- `mode=local-instance`；
- `calibration.level=calibrated`，范围明确写为**隔离本地集群**；
- 生产 DSN 通过 `GIS_POSTGIS_DSN` 由用户提供，默认仍指向本机 5432
  的 `gisplat`（未配置密码时不自动升格）。

## 4. 网关 → PostGIS 真跑（21/21）

`test_postgis_live.py`：模板 38/38 + 桥/网关 **21/21 PASS**，覆盖：

- 基础：ping、discover（36 模板 + PostGIS 3.6）、list_datasets、
  project_info（kind=database）；
- V05 建表 `gw_t`、V06 加字段 `extra`、V08 字段计算（表达式模板）；
- V31 量测 distance=1.0；
- V32 几何校验（1 个坏几何）+ 修复（新表 `gw_bad_fixed`）；
- V24 坡度（`gw_slope`）；
- V30 空间过滤（返回行）；
- V16 GeoJSON 导出（3 要素）；
- 查库复核 `gw_t.extra`、`gw_bad_fixed`、`gw_slope` 均存在；
- 导出文件复核 3 要素。

结果：`evidence/phase4-postgis/postgis-live-results.json`（21/21）、
`postgis-live.log`、`postgis-templates.log`、`postgis-test-results.json`。

## 5. 本轮修的两个公共问题

1. **V06 字段参数适配**：统一参数 `field={name,type}` 之前没有映射到
   postgis 模板的 `column/sql_type`；`build_template` 已补，qgis/supermap
   原生路径不受影响。
2. **新桥 UTF-8 stdio**：gdal/qgis-cli/iserver/postgis 四桥统一锁
   UTF-8；否则 Windows 下 stdin 默认 GBK，含中文 target 的请求会被解码
   错乱/卡住（本次 PostGIS GeoJSON 导出的真实根因）。手工测试曾因继承
   `PYTHONUTF8=1` 掩盖该问题，正式测试暴露并修复。

## 6. 账面与校准

| 项目 | 变化 |
|---|---|
| 叶子账本 | **208／ok 165／unverified 21／not_supported 22 不变**（PostGIS 叶原本已计入） |
| tier | 174／30／4 不变 |
| PostGIS 校准 | `protocol_selfcheck_only` → **`calibrated`（仅限隔离本地集群）** |
| 自检 | 154/154（gateway V06 适配与 UTF-8 锁不改变离线断言） |
| 生成器 | 6/6 字节一致（PostGIS 模板/注册表未改内容） |
| 真跑 | 模板 38/38 + 网关 21/21 |

## 7. 未完成与原因

1. **生产 PostGIS 实例**：本机 5432 需要密码，未猜；`GIS_POSTGIS_DSN`
   未配置。`calibrated` 只覆盖隔离集群，不外推到生产。
2. **模板测试旧存档**：根目录 `postgis-test-results.json` 为旧脚本产物，
   方法上不可信；本次修正后的结果在 `evidence/phase4-postgis/`，不再用
   旧存档作为新证据。
3. **psycopg2 运行环境**：桥依赖 QGIS Python 的 psycopg2 2.9.13；标准
   Python 未装。`backends.json` 已写 QGIS Python 路径；换机需同步。
4. **空间分析/写面**：不在本次 PostGIS 范围；PostGIS 模板已覆盖建表/
   加字段/计算等写模板，但删除类只做了模板级测试（隔离库），未对生产。

## 8. 证据索引

- `evidence/phase4-postgis/postgis-live-results.json`：21/21 逐项
- `evidence/phase4-postgis/postgis-live.log`：完整输出（UTF-8）
- `evidence/phase4-postgis/postgis-test-results.json`：修正后模板 38/38
- `evidence/phase4-postgis/postgis-templates.log`：模板测试完整输出
- `evidence/phase4-postgis/postgis-export-debug.log` /
  `gateway-debug.log`：UTF-8/导出路径根因的步骤证据
- `evidence/phase4-postgis/cluster-manual.txt`：手工隔离集群版本记录
- `code/postgis_server.py` / `test_postgis_live.py` /
  `test_templates_live.py`（修正 psql 调用）

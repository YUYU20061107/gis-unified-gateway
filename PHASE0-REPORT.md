# PHASE 0 · 落位与复现报告

- 日期：2026-11-05
- 状态：**通过**（附两条环境适配说明：Windows 测试端 UTF-8、manifest 重建）
- 本地提交：`66ba622`（原件基线）→ `681e9cc`（补发输入）→ 本报告提交
- 环境：Windows 10.0.26300 x64；Python 3.12.9（本机无 `python3` 别名）；Git Bash
- 项目根：`E:/ds工作区/gateway-v03`

## 0. 开工前复述（依据验证报告与四份文档）

### 0.1 当前账面哪些数字是错的

- **叶子映射总账**：文档写 `198 = ok 157 + unverified 19 + not_supported 22`；`leaves-full.json` 实数
  **195 = ok 151 + unverified 22 + not_supported 22**。差额：总数 −3、ok −6、unverified +3。
  G3 已留痕：改前账本为 195 行（ok 151／unverified 19／not_supported 22／空 status 3），
  G3 把 3 条空 status（V32 三叶）补为 unverified，故 unverified 变为 22；**ok 侧少 6 条
  的来路仍未销账**，文档也未同步（`G3-TAGGING-CHANGELOG-20261103.md:33`）。
- **“40/40 每个动词至少一条 ok 映射”**：`verbs.json` 口径成立；`leaves-full.json` 口径为
  **39/40**，唯一缺口是 V32 `gis_validate_geometry`（三后端叶均 unverified，supermap 叶
  not_supported）。两套账本互相矛盾。
- **tier 三级**：实际只有两级在用——core 163／extended 32／**exclusive 0**；V01/V02 的 3 行
  候选暂置 extended，待裁决。说“三级标注已落地”不准确。
- **版本号**：v0.3 只存在于施工单与目录名；`code/gateway.py:51` 仍是
  `SERVER_VERSION = "0.2.0"`，`code/README.md:1` 标题仍是 v0.2。
- **后端 8 个属实**（supermap、arcgis-pro、arcmap、qgis、catalog、postgis、geoserver、
  istsos），但不能据此说“10 个后端”（见 0.3）。

### 0.2 生成器有什么漂移风险

- **最危险项**：`code/postgis_templates.json` 有 7 条模板是 2026-11-03 实机校准定版，
  而 `code/build_mapping.py` 的 `TEMPLATES` 仍是旧版。重跑生成器会把它们静默打回旧版：
  `clip_raster`、`spatial_join`、`mapalgebra`、`hillshade`、`reclass`、`validate_repair`、
  `mvt_tile`。自检 B96–B98 还专门断言 `validate_repair` 的新表形态；重跑后若先落盘再跑自检，
  坏版本已经写回。
- 验证报告的其余 5 个产物（verbs／mapping／gp_registry／processing_registry／mock_tools）
  在本机重跑后**字节级一致**；postgis_templates 是唯一漂移产物（见 §2.4）。
- **本轮新增发现（验证报告未列）**：生成器依赖硬编码 Linux 路径
  `~/workspace/dsh-skills/gis-agent-bridges/manifest/tools-manifest.json`，并依赖
  `gateway-v03/help-survey/`、`data-catalog/`。原件压缩包未带这些输入；补发包补齐了后两者，
  manifest 仍未提供（见 §2.4 与 `evidence/phase0/manifest-reconstruction.txt`）。
  另外在册 JSON 是 LF，Windows 上 Python 文本写入默认转 CRLF，字节级比较需要显式处理换行。

### 0.3 哪些后端只是“已决策未落地”

- **GDAL**：V2 施工单 D3 裁决“接，且升格为正式通用后端 `gdal`”，排批 1；
  `backends.json`、`mapping.json`、`leaves-full.json` 三处均无 `gdal` 后端。
  代码内只见 QGIS Processing 的 `gdal:*` 算法条目与一条 PostGIS 模板名，不是后端落地。
- **iServer**：V2 施工单 D6 裁决“升正式后端”，批 1 只是“评估接入”；
  注册表三处均无 `iserver`。原 V35/supermap 叶仍是 SuperMap 桥内的 not_supported 语境。
- 因此当前准确口径是 **8 个已登记后端；GDAL/iServer 已决策、待批 1 接入**。

## 1. 目标

跑通离线自检 148/148；在副本上重跑 `build_mapping.py`，逐数复现验证报告；
产出本报告。不改语义、不改账本。

## 2. 实际完成（带证据）

### 2.1 落位与基线保护

- 压缩包 `gateway-v03-qoder-pack.zip` 已解压到 `E:/ds工作区/gateway-v03`；
  补发包 `gateway-v03-supplement.zip` 的 `help-survey/` 与 `data-catalog/` 已落位。
- 本地 git 基线提交 `66ba622`（原件原样），补发输入提交 `681e9cc`；
  本阶段未改动任何项目语义文件或账本。
- 证据：`git log --oneline`；`evidence/phase0/supplement-contents.txt`。

### 2.2 自检复现（148/148）

- 补发前：145/148，C11–C13 因缺 `data-catalog/catalog_server.py` 报 `BACKEND_EXITED`。
- 补发后，在干净副本实跑：

```
PYTHONUTF8=1 python code/selftest.py
checks: 148, passed: 148, failed: 0
EXIT=0
```

- 证据：`evidence/phase0/selftest-148.log`。
- **环境适配说明**：不设 `PYTHONUTF8=1` 时，C01 会在 30s 超时。根因是自检的 `McpClient`
  用 `subprocess.Popen(..., text=True)` 未指定 encoding，Windows 父进程按 GBK 解码
  gateway 的 UTF-8 JSON，reader 线程抛 `UnicodeDecodeError`，队列拿不到响应。
  这不是网关逻辑问题；测试端编码修复留到阶段 1（会一并复跑 148/148）。
  证据：`evidence/phase0/selftest-gbk-crash.log`。

### 2.3 验证报告数字逐项复算

复算脚本：`_phase0/audit_phase0.py`（只读）；输出：`evidence/phase0/audit-phase0.txt`。
除“生成器重跑”和“148/148”已在 §2.4／§2.2 单独处理外，验证报告所有主数字均能从在册文件复现：

| 项目 | 验证报告 | 本机复算 | 结论 |
|---|---|---|---|
| 动词 | 40 | 40（verb_order 40） | 一致 |
| 后端 | 8 | 8（三处注册表一致） | 一致 |
| 叶子总数 | 195 | 195 | 一致 |
| ok／unverified／not_supported | 151／22／22 | 151／22／22 | 一致 |
| 桥侧 pending／existing | 21／12 | 21／12 | 一致 |
| GP 总数／core／extension／defer | 1833／803／878／152 | 1833／803／878／152 | 一致 |
| GP 白名单／通道可调／破坏类 | 243／239／28 | 243／239／28 | 一致 |
| Processing 总数／core／extension／defer | 374／82／242／50 | 374／82／242／50 | 一致 |
| Processing 硬拦截 | 51 | 51 | 一致 |
| PostGIS 模板数 | 36 | 36 | 一致 |
| PostGIS 实机用例 | 38/38 PASS | 存档 38 条全 PASS | 存档口径一致，未复跑 |
| tier core／extended／exclusive | 163／32／0 | 163／32／0 | 一致 |
| 每动词至少 1 条 ok | verbs 40/40；leaves 39/40 | 39/40，缺 V32 | 一致 |
| GDAL／iServer 后端 | 不存在 | 三处均不存在 | 一致 |

### 2.4 生成器重跑与字节级比对

在干净副本 `_phase0/gen-full` 上重跑 `build_mapping.py`。生成器输出的 6 个产物与在册文件对比：

| 产物 | 结果 |
|---|---|
| `mapping.json` | **字节级一致** |
| `verbs.json` | **字节级一致** |
| `gp_registry.json` | **字节级一致** |
| `processing_registry.json` | **字节级一致** |
| `mock_tools.json` | **字节级一致** |
| `postgis_templates.json` | **差异**：36 个模板中恰好 7 个不同，其余 29 个一致 |

- 生成器 stdout：`GP: total=1833 core=803 extension=878 defer=152 whitelist_raw=243
  channel_whitelist=239 destructive=28`；`Processing seed: total=374 core=82 extension=242
  defer=50 hard_block=51`；`verbs=40 templates=36 supermap_registry_entries=32`。
- 证据：`evidence/phase0/generator-full.log`、`evidence/phase0/product-compare.txt`。
- **两条复现适配**（均未改项目代码）：
  1. **换行**：在册 JSON 是 LF；Windows 上 Python 文本写入默认 CRLF。重跑用了一层
     `builtins.open` 包装强制 `newline="\n"`，否则 6 个产物全部因换行差异“不等”。
     该修复在阶段 1 正式落进生成器。
  2. **manifest**：原件未随包提供。用本机 `gis-agent-bridges/manifest/tools-manifest.json`
     为底（其 `scope_note` 与在册 `mapping.json` 的 `manifest_scope_note` 逐字一致），
     按 `code/mock_tools.json` 补齐 postgis／geoserver／istsos 及所有被引用的原生工具名，
     作为校验输入。该输入只影响“原生工具名存在性校验”与 `manifest_scope_note`；
     后者已匹配，前者的证据是 5 个产物字节级一致、内容未被改动。
     详见 `evidence/phase0/manifest-reconstruction.txt`。若拿到原件，再跑一次即可复核。

### 2.5 生成器 7 条漂移（逐字段）

生成器 `TEMPLATES` 与在册 `postgis_templates.json` 的差异恰好 7 条，与验证报告一致。
逐字差异见 `evidence/phase0/template-drift.diff`。摘要：

| 模板 | 生成器旧版 | 在册校准版 |
|---|---|---|
| `clip_raster` | `ST_Clip(...)` 三参 | 补 `crop=true`（两形态） |
| `spatial_join` | `a.*, b.*` + `sql` | builder＋显式 `attributes`，别名 `join_<列>`、`join_geom` |
| `mapalgebra` | `ST_MapAlgebra`＋`[rast]` | `ST_MapAlgebraExpr`＋`[rast.val]`＋`pixeltype` |
| `hillshade` | 缺 `pixeltype` | 补 `pixeltype`（默认 32BF） |
| `reclass` | 缺 `pixeltype` | 补 `pixeltype`（默认 32BF） |
| `validate_repair` | 原地 `UPDATE` | 输出新表＋`target` 必填＋`<列>_repaired` |
| `mvt_tile` | `{attr_columns}`＋误标 builder | `{attr_columns:attributes}`，去 builder |

### 2.6 V32 三处矛盾（已坐实）

- `verbs.json`：postgis／arcgis-pro／qgis 的 check 与 repair 均 `ok`；supermap `not_supported`。
- `leaves-full.json`：postgis／arcgis-pro／qgis 三叶均 `unverified`（G3 补正，kind/native 为空）；
  supermap `not_supported`。
- `selftest.py:740/746/753`（B96–B98）：网关实际执行 qgis 校验、postgis repair 的
  `ST_MakeValid` 新表模板，并断言成功/确认门。
- 结论：**账本标未验的映射，运行时在放行**。阶段 1 必须裁决并单向同步。

### 2.7 B1 SuperMap 覆盖层（12 条成果未回灌）

`b1-reconciliation.json` 共 16 条 verdict：`name_verified_function` 10、
`name_verified_class` 2（合计 **12 条已坐实**）、`pending_check` 1（V20/difference）、
`unresolved` 3（V06／V07／V12）。这 12 条仍在覆盖层，`leaves-full.json` 对应叶仍
`unverified`，未回灌。

### 2.8 文档旧数字位置（待阶段 1 同步）

- `code/README.md:19`（198／ok 157）、`:21`（unverified 19）、`:23`（40/40）、`:93`（19 条）。
- `V03-WORKLIST.md:4`、`:38`、`:88`（198／157／19／22）。
- `V03-WORKLIST-V2-GENERALIZED-20261103.md:4`、`:25`（198 叶）。
- `G3-TAGGING-CHANGELOG-20261103.md:33`（差额留痕，待销账）。

### 2.9 e2e 证据边界

- 网关进程级 e2e 只对 mock 后端与真实 data-catalog（只读）跑过；对真实 GIS 后端的端到端
  仍无证据（阶段 4 目标）。
- PostGIS 模板 38/38 PASS 是脱离网关的实机结果（存档口径），本轮未复跑。

## 3. 账面数字变化对照表

本阶段**未改任何账**；变化只在“输入与证据”侧。

| 项目 | 阶段前 | 阶段后 | 变化 |
|---|---|---|---|
| 动词／后端 | 40／8 | 40／8 | 无 |
| 叶子（总数／ok／unv／ns） | 195／151／22／22 | 195／151／22／22 | 无 |
| tier（core／ext／exc） | 163／32／0 | 163／32／0 | 无 |
| 生成器模板漂移 | 7 条 | 7 条（已固化为 diff 证据） | 未修，阶段 1 |
| 自检 | 存档 148/148 | 本机 148/148（UTF-8 模式） | 已复现 |
| 生成器产物一致 | 报告称 5/6 | 本机 5/6 字节一致 | 已复现 |

## 4. 未完成与原因

1. **原始 manifest 未提供**：本机重跑使用“名称补全”的重建 manifest（§2.4）。该输入只影响
   名校验与 `scope_note`，后者已逐字匹配；5 个产物字节一致。严格起见，拿到原件后应再跑一次。
2. **Windows 测试端编码未修**：当前自检需 `PYTHONUTF8=1` 才能 148/148；这是测试 harness 的
   可移植性缺陷，阶段 1 修（不涉网关闭环逻辑）。
3. **生成器换行未正式修**：当前用包装层强制 LF；阶段 1 把 `newline="\n"` 正式落进
   `build_mapping.py` 的输出写入，并用同一条命令复跑。
4. **PostGIS 38/38 未复跑**：本机未起 PostgreSQL/PostGIS 实例；只核对存档 38 条全 PASS。
5. **真实后端 e2e 未做**：按计划留到阶段 4。
6. **阶段 1 未开始**：本报告落盘并提交后才启动。

## 5. 下一阶段入口条件是否满足

**满足。** 阶段 0 的硬门槛已过：

- 自检 148/148（本机，UTF-8 模式）；
- 生成器在副本上重跑，5/6 产物字节级一致，postgis_templates 的差异恰好是 7 条已知漂移；
- 验证报告全部主数字复现；
- 两条环境适配已记录，且不影响账本结论。

阶段 1 入口条件：保持 `leaves-full.json` 现状为基线，先做①总账 195 分项同步、②7 条模板回写
生成器、③V32 裁决、④12 条 B1 回灌；每步跑自检并用 `git diff` 逐项解释。

## 6. 证据索引

- `evidence/phase0/audit-phase0.txt`：全部账面数字复算输出
- `evidence/phase0/product-compare.txt`：6 产物哈希与逐项一致/差异
- `evidence/phase0/generator-full.log`：生成器重跑 stdout（1833/374/40/36）
- `evidence/phase0/template-drift.diff`：7 条模板逐字段差异
- `evidence/phase0/selftest-148.log`：148/148 完整输出
- `evidence/phase0/selftest-gbk-crash.log`：Windows GBK 解码导致 C01 超时
- `evidence/phase0/generator-manifest-missing.log`：manifest 路径缺失（补发前）
- `evidence/phase0/generator-catalog-missing.log`：manifest 补齐后缺 catalog_server.py（补发前）
- `evidence/phase0/manifest-reconstruction.txt`：重建 manifest 的来源、范围与证据边界
- `evidence/phase0/supplement-contents.txt`：补发包文件清单
- 复算脚本：`E:/ds工作区/_phase0/audit_phase0.py`（工作区临时目录，只读）

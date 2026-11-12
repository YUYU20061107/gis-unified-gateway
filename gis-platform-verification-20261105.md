# GIS 平台（统一网关）v0.3 深入验证报告

- 日期：2026-11-05
- 验证方：Muse 子代理（只验证、只提改进，未改任何代码，未做对外发布/推送）
- 验证对象：`~/workspace/gis-platform-integration/gateway-v03/`（其中 `code/` 本体自称 gateway v0.2，v0.3 目前是其上的施工单/设计层，见 §2-S7）
- 证据纪律：每个数字给「账面值／实测值／出处」；README 与施工单的说法一律按自述处理，须实测复现才升为已验证。

---

## 0. 账面数字总核对表

| 项目 | 账面值 | 实测值 | 结论 | 证据出处 |
|---|---|---|---|---|
| 统一动词数 | 40 | **40** | ✅ 一致 | `code/verbs.json`：`verbs` 40 键、`verb_order` 40；`leaves-full.json` 覆盖 40 个动词 |
| 叶子映射总数 | 198（ok 157＋unverified 19＋not_supported 22） | **195**（ok 151＋unverified 22＋not_supported 22） | ❌ 差 3（ok 侧差 6） | 账面：`V03-WORKLIST.md:4`、`code/README.md:19`；实测：`leaves-full.json` 全量计数（本报告脚本实数）；项目自身 `G3-TAGGING-CHANGELOG-20261103.md` 账目差注记已记录此差异，尚未销账 |
| 桥侧 pending 叶 | 21 | **21** | ✅ 一致 | `leaves-full.json` 的 `bts` 字段计数（pending 21／existing 12） |
| 桥侧 existing 叶 | 12 | **12** | ✅ 一致 | 同上 |
| 后端数 | 8 | **8** | ✅ 一致 | `code/backends.json`、`code/mapping.json`：supermap、arcgis-pro、arcmap、qgis、catalog、postgis、geoserver、istsos |
| GDAL 为正式后端 | 「已升格为正式通用后端 `gdal`」 | **注册表无 gdal 后端** | ❌ 只是决策，未落地 | 决策原文：`V03-WORKLIST-V2-GENERALIZED-20261103.md` D3 条（排批 1「GDAL 后端接入」）；`backends.json`/`mapping.json`/`leaves-full.json` 三处均无 gdal；代码内 gdal 仅见于 QGIS Processing 的 `gdal:*` 算法条目与一条 PostGIS 模板名 |
| iServer 为正式后端 | 「升正式后端」 | **注册表无 iserver 后端** | ❌ 只是决策，未落地 | 同上 D6 条（批 1 为「iServer **评估**接入」）；注册表三处均无 iserver |
| GP 注册表 | 1,833（core 803／extension 878／defer 152）；白名单 243→通道可调 239；破坏类 28 | **全部复现** | ✅ 一致 | 在 /tmp 副本实跑 `build_mapping.py`，输出与账面逐数相同；重生成产物与在册文件比对见 §2-S1 |
| Processing 种子账 | 374（82／242／50）；硬拦截 51 | **全部复现** | ✅ 一致 | 同上 |
| PostGIS 模板数 | 36 | **36** | ✅ 数量一致（内容有漂移，见 S1） | `code/postgis_templates.json` 与重生成结果 template_id 集合相同 |
| 离线自检 | 148 项全过 | **148／148 实跑复现** | ✅ 一致 | 本机实跑 `python3 code/selftest.py`，exit 0，尾行 `checks: 148, passed: 148, failed: 0`；与 `code/selftest-results.txt` 一致 |
| 能力三级标注 tier | core／extended／exclusive 三级 | core **163**／extended **32**／exclusive **0** | ⚠️ 实际只有两级在用 | `leaves-full.json` 的 `tier` 字段计数；`G3-TAGGING-CHANGELOG` §2、§4：exclusive 唯一候选（V01/V02 通道叶 3 行）暂置 extended 待裁决 |
| 「每动词至少一条 ok 映射」 | 40／40（`code/README.md:24`） | verbs.json 口径 40／40；**leaves 账本口径 39／40** | ⚠️ 两账本互相矛盾 | `gis_validate_geometry`（V32）在 `leaves-full.json` 中无任何 ok 叶（postgis／arcgis-pro／qgis 均记 unverified、supermap 记 not_supported），但在 `verbs.json` 中三后端均记 ok，详见 S3 |

---

## 1. 已验证成立的结论

1. **动词面属实**：40 个统一动词真实存在于 `verbs.json`，且每个动词在 leaves 中都有叶行覆盖。证据：§0 表。
2. **离线协议自检真实可复现**：`selftest.py` 本机实跑 148/148 全过（A 注册表完整性 7＋B 进程内分发 127＋C 端到端 13＋真实目录对账）。这不是抄存档结果——命令与输出为本次实测。
3. **网关进程本身能跑（对 mock 后端）**：selftest C 段真起 `gateway.py` 子进程、走完整 stdio MCP 协议对 mock 后端与真实 data-catalog（只读）端到端跑通（`selftest.py:12-13` 设计说明＋本次实跑通过）。即「网关本体从未 live 跑过」需修正为：**进程级 live（mock 后端）已验；对真实 GIS 后端的端到端运行无证据**。
4. **注册表生成器可复现**：`build_mapping.py` 在干净副本重跑，GP／Processing 全部计数逐数复现，6 个产物中 5 个与在册文件**字节级一致**（verbs／mapping／gp_registry／processing_registry／mock_tools）。
5. **PostGIS 模板面有真实机证据**（超出「从未 live」的旧口径）：`test_templates_live.py`＋`postgis-test-results.json` 显示 36 个模板在真实 PostgreSQL+PostGIS 实例上执行 **38/38 PASS**（含变体）；模板文件内含 2026-11-03「实机校准定版」修正注记（如 `validate_repair` 改输出新表形态、`hillshade` 补 pixeltype 参数）。
6. **SuperMap 有探针级实机证据，但仅止于原生调用层**：R1–R3 校准探针在 iobjectspy 10.1.0 实机坐实建源全链、V05 建数据集、V06 建字段（创建侧）、V12/V13 追加（`R3-ACCEPTANCE-20261103.md` 本体验收）；B1 对账将 16 条 supermap unverified 叶与实机成员清单逐条对账（10 条 name_verified_function、2 条 name_verified_class、3 条 unresolved、1 条 pending_check，`b1-reconciliation.json`）。**网关 supermap 适配层本身仍未 live**（R3 验收文明示），V07 `remove_field` 疑似静默 no-op、V29 `statistic` 返回 None 两项未验通、已精确定位。
7. **治理（确认门）逻辑经自检覆盖且抽查属实**：破坏性分级与 verbs.json 一致——`gis_delete_dataset`／`gis_delete_field` 为 R3（confirm＋target_echo＋preflight 三件套），`gis_rename_dataset` 为 R2，`gis_copy_dataset` 为 R1；自检 B 段含 DEFER_BLOCKED／DESTRUCTIVE_BLOCKED／CONFIRM_REQUIRED／TARGET_ECHO_MISMATCH／PREFLIGHT_REQUIRED／LICENSE_BLOCKED 等拒绝路径且全过。
8. **证据口径标注整体诚实**：`backends.json` 逐后端自报 calibration 等级（arcmap=calibrated 为 v0.1 冻结存量；postgis/qgis/geoserver/istsos/arcgis-pro/supermap=protocol_selfcheck_only；catalog=uncalibrated），与本次核查所见一致，未发现把自检冒充实机校准的升格。

### 映射质量抽查（随机样本 10 条，种子 20261105，逐条对源核对）

| # | 叶 | 核对结果 |
|---|---|---|
| 1 | V10 gis_rename_dataset@arcgis-pro → `arcpy.management.Rename`（gp_named） | ✅ verbs.json 落名一致；该工具确在 GP 白名单第一批与全量登记中；改名定级 R2 合理 |
| 2 | V36 gis_query_observations@istsos（ObservedProperties）→ `istsos_query_entities` | ⚠️ 映射本身与 verbs.json 一致，但执行工具为桥侧 **pending**——status 记 ok 仅表示「落名」，实机不可用（叶注记已明示，属口径风险，见改进项 6） |
| 3 | V11 gis_delete_dataset@postgis → 模板 `drop_table` | ✅ 模板存在；删除定级 R3＋confirm 必填，破坏性标记正确 |
| 4 | V30 gis_spatial_filter@postgis → 模板 `spatial_filter` | ✅ 模板存在；只读定级 R0 正确 |
| 5 | V08 gis_calculate_field@qgis → `native:fieldcalculator` | ✅ 确在 Processing 种子账中、不在硬拦截名单；verbs.json 落名一致 |
| 6 | V20 gis_overlay@supermap（identity）→ `supermap_overlay` | ✅ 如实标 unverified，注记说明 iobjectspy.analyst.overlay 其余式待验、裁剪走 gis_clip |
| 7 | V31 gis_measure@postgis（length）→ 模板 `measure_length` | ✅ 模板存在 |
| 8 | V32 gis_validate_geometry@supermap → not_supported | ✅ 与 verbs.json 及设计 §2 V32 一致（本波波次决定） |
| 9 | V12 gis_merge_datasets@supermap → `supermap_merge_datasets` | ✅ 如实标 unverified 并注明待验点（B1 二轮后已有类级坐实路径，账本未回灌，见 S5） |
| 10 | V20 gis_overlay@postgis（intersect）→ 模板 `overlay_intersection` | ✅ 模板存在 |

抽查结论：**10/10 语义与源注册表对得上**，状态标注保守（待验/不支持均如实标并附原因），未发现把不存在的轮子写成 ok 的造假；主要风险不在映射真假，而在「ok」的口径（落名≠可执行，21 条 ok 叶骑在 pending 桥侧工具上）与账本同步（§2）。

---

## 2. 对不上的地方（按严重度排序）

- **S1（高）生成器与产物漂移，重跑会静默回退实机修复**：在册 `postgis_templates.json` 与 `build_mapping.py` 重生成结果有 **7 条模板内容不一致**（clip_raster、spatial_join、mapalgebra、hillshade、reclass、validate_repair、mvt_tile）。方向已查明：在册文件更新、含 2026-11-03 实机校准定版（如 `validate_repair` 在册版为「输出新表」SQL，生成器仍产出已被实机证明会失败的「原地 UPDATE」版；`hillshade` 在册版补了 pixeltype 参数，生成器没有）。任何人按 README 指引重跑 `build_mapping.py`，都会把这 7 条实机验过的模板**静默打回已知坏版本**，且自检 B98 还专门断言了新形态——重跑后自检会红，但若先提交产物再跑自检，坏版本已经落盘。
- **S2（高）总账 198 与实数 195 长期未销账**：README 与两份施工单仍挂「198＝ok 157＋unverified 19＋not_supported 22」，实数 195（ok 151／unverified 22／not_supported 22）。项目在 G3 变更日志中已知情并留痕「待批 1 账目刷新时一并核」，但对外引用（如本轮任务背景）仍在用 198。对账差构成：总差 −3、ok 差 −6、unverified 差 +3（G3 将 V32 三条空 status 叶补正为 unverified）。
- **S3（中高）V32 状态三方不一致，且网关在按「未验」映射执行**：`verbs.json`（网关运行时真源）记 V32 于 postgis／arcgis-pro／qgis 三后端为 ok（check/repair 双变体），自检 B96–B98 证明网关确实会执行（qgis:checkvalidity、postgis ST_MakeValid 模板）；`leaves-full.json`（账本）经 G3 补正记三叶为 unverified 并留「待裁决」注记。即：**账本上标着未验的映射，运行时正在放行**，裁决悬置期间两边各自为政。
- **S4（中）「GDAL／iServer 已升为正式后端」与实况不符**：该说法出自 V2 施工单的**决策条目**（D3/D6），落地排在批 1（12 月上旬），且 iServer 在施工单里只是「评估接入」。当前注册表（backends／mapping／leaves）中两个后端均不存在。若对外按「已有 10 个后端」介绍即为超前陈述；准确口径是「已决策升格、待批 1 接入」。
- **S5（中）状态真源三分、B1 成果未回灌**：同一叶子的状态现有三个出处——`verbs.json`（运行时）、`leaves-full.json`（账本）、`b1-reconciliation.json`（覆盖层，G3 明示以覆盖层为准）。B1/B1-R2 已坐实的 supermap 叶（如 V06/V07 类级坐实、V24/V25/V26 名验通）在主账本中仍标 unverified。消费者（人或程序）读哪份文件得到哪种结论，无统一口径。
- **S6（低）tier 三级实际只有两级**：exclusive 为 0，唯一候选 3 叶暂置 extended 待裁决（G3 §4 悬置）。设计本身允许「exclusive 是如实标注」，但「三级标注已落地」的说法应降为「两级已用、第三级待裁决」。
- **S7（低）版本号未落码**：「v0.3」目前只存在于施工单与目录名；`code/gateway.py` 文件头与 SERVER 信息仍自称 **v0.2**，`code/README.md` 标题亦为 v0.2。引用「GIS 平台 v0.3」时须注明是工作线口径，不是代码版本。

---

## 3. 改进清单

| # | 改什么 | 为什么 | 预估工作量 | 风险 |
|---|---|---|---|---|
| 1 | 把 7 条实机校准模板的定版内容**回写进 `build_mapping.py` 的模板源**（或在生成器加「校准覆盖层」合并步骤），重跑后与在册文件 diff 应为零，并把「重跑生成器＋diff 校验」加进自检 A 段 | 消除 S1 的静默回退：现在生成器是坏版本的真源，任何一次例行重跑都会弄丢实机修复 | 0.5–1 天（逐条对 7 个模板，validate_repair 需连参数表一起改） | 低；改完须重跑 148 自检＋PostGIS 实机 38 项复测确认无回退 |
| 2 | **总账刷新并销账**：以 leaves-full 实数（195／ok 151／unverified 22／not_supported 22）更新 README 与施工单账目，或补齐缺失 6 条 ok 叶的抽取并注明去向；在 changelog 中正式关闭 G3 留下的差异注记 | 消除 S2：198 已被多处引用（含本次任务背景），错误基数会污染后续所有批次的增减账 | 0.5 天（纯账目活，先裁决「改账还是补叶」） | 低；注意 pending 21／existing 12 两数与新总账交叉验算 |
| 3 | **裁决 V32 状态并单向同步**：按 G3 §4 的待裁决项拍板（按 verbs.json 的 ok 落名＋模板/算法已实机或种子坐实程度定级），然后让 leaves 与 verbs 只保留一个方向的生成关系（账本由运行时注册表抽取，或反之），禁止手改单边 | 消除 S3：运行时放行与账本定级不一致是治理面最危险的一类账实差——出事时无法回答「这条映射到底验没验」 | 裁决 0.5 小时＋同步改造 0.5 天 | 中；若裁决降级为 unverified，网关行为会变（V32 三后端转 UNVERIFIED_MAPPING 拒绝），须同步改自检 B96–B98 预期 |
| 4 | **对外口径纠正 GDAL／iServer**：所有对外材料改为「已决策升格、批 1 接入中」；在 backends.json 预登记两条 `status: planned` 占位（不计入后端数），使「计划」在注册表内可见、可追踪 | 消除 S4：决策与落地的混淆已进入任务背景口径，继续传播会变成对外承诺 | 1 小时（文档与占位条目） | 低 |
| 5 | **B1 覆盖层回灌主账本**：把 b1-reconciliation（含 R2）的 16 条 verdict 按既定升格流程（名验通→标 name_verified 中间态，不直接升 ok）写回 leaves-full，并注明证据链；此后覆盖层文件冻结为历史档 | 消除 S5：三套真源并存时，任何自动统计都会得出不同结论（本报告 §0 就需要人工对三份文件） | 0.5 天（16 条逐条落，含 V12 合并语义边界注记） | 中；升格口径须守 R3 验收结论——「坐实＝名字存在，不等于可执行」，不得直升 ok |
| 6 | **给「ok」加可执行性子标记**：leaves 增加 `exec_readiness`（ready／bridge_pending／seed_only 三档），21 条 pending 叶与 374 种子账相关叶如实标注；README 的「ok 157」类表述改为双数并列（落名数／今日可执行数） | 抽查样本 #2 暴露的口径风险：ok 叶骑在 pending 工具上，对外报「157 条可用映射」会被误读为今日可执行 | 0.5 天（机械打标，数据源现成：bts 字段＋种子账标记） | 低 |
| 7 | **exclusive 待裁决项关账**：对 V01/V02 通道 3 叶作出裁决（标 exclusive 或维持 extended 并注明理由），使 tier 分布成为终态 | 消除 S6 的长期悬置；三级标注是 v0.3 对外卖点之一，悬置状态不宜跨批 | 0.5 小时（纯裁决） | 低 |
| 8 | **版本号落码**：批 1 首次动代码时把 gateway.py 的 SERVER_VERSION 与 code/README 标题升为 v0.3，并注明与 v0.2 的差异面（tier 字段、账目刷新） | 消除 S7：避免后续验收继续出现「验的是哪一版」的歧义（本报告即须绕注） | 0.5 小时 | 低 |
| 9 | **补一次「生产配置」端到端冒烟**：用在册 backends.json（指向真实桥服务）起网关，对每个后端各跑一条只读动词（ping／discover／list 类），结果落盘为证据文件；ArcGIS Pro 预期失败，如实记为硬阻塞 | 这是当前证据链最大的空白（§4 第 1 条）；做完后「网关从未对真实后端 live」的口径才能关闭或坐实 | 0.5–1 天（桥服务多在用户 Windows 侧，须排期配合） | 中；只读动词、无写操作，风险可控；Pro 无环境一项会失败，屬预期 |

---

## 4. 仍属未验证的结论（不得升格引用）

1. **网关对真实后端的端到端运行**：无证据。已验的只有 mock 后端 e2e（进程级）与 PostGIS 模板脱离网关的实机执行；生产 `backends.json` 指向的 8 个桥服务从未见经网关逐个跑通的记录。
2. **QGIS Processing 执行面**：374 条全为种子账（seed），实机枚举未建账；`gis_run_processing` 的真实执行、参数模式（params_schema）自述均为 pending，自检 B26/B28 亦如实标 pending。
3. **ArcGIS Pro GP 通道**：执行器 `arcgis_run_gp` 为桥侧 pending 工具，无 Pro 环境——这是已坐实的硬阻塞；但「硬阻塞**只有** ArcGIS Pro」不成立：SuperMap 适配层未 live、QGIS 枚举未建账、GeoServer 发布链与 istSOS 通用实体查询工具待实现，都是未通项（性质是未建/未验，非环境阻塞）。
4. **SuperMap 网关适配层**：原生探针级证据不能替代适配层 live；V07 remove_field 静默 no-op 与 V29 statistic 返回 None 两项为已定位的未通点。
5. **GDAL／iServer 两个后端的一切能力**：尚不存在，无从验证（见 S4）。
6. **V33 瓦片真实字节流出口、istSOS 写面、GeoServer 发布回写 catalog**：README 未做清单自述未做，本次未见任何反证，按未做处理。

# PHASE 1 · 销账与防漂移报告

- 日期：2026-11-05
- 状态：**通过**
- 快照说明：本报告是 Phase 1 时点的账（195/152/21/22）。Phase 2 增 GDAL 9 叶、
  Phase 4 增 qgis-cli 3 叶、Phase 3 增 iServer V35 1 叶后，当前终账为
  **208＝ok 165＋unverified 21＋not_supported 22**；见 `PHASE3-REPORT.md`。
- 起点：`d5ac022`（Phase 0 最终证据）→ 本阶段提交
- 环境：Windows 10.0.26300 x64；Python 3.12.9；Git Bash
- 证据目录：`evidence/phase1/`

## 1. 目标

1. 把总账改对（195 及分项），README、现行施工单、账本三处同步；
2. 把 7 条 2026-11-03 实机校准模板回写生成器，使重跑产出与在册文件字节级一致、永不回退；
3. 统一 V32 三处状态，给出裁决理由并留痕；
4. 把 B1 覆盖层的 SuperMap 叶成果回灌主账本。

验收：自检全绿；`git diff` 能逐项解释。

## 2. 实际完成（带证据）

### 2.1 总账销账（195）

**终账：195 = ok 152 + unverified 21 + not_supported 22。**

- 起点实数：195 = ok 151 + unverified 22 + not_supported 22（验证报告基线）。
- 变化：V32@postgis 由 unverified 升 **ok**（+1 ok、−1 unverified）。依据：`postgis_templates.json`
  的 `validate_check` / `validate_repair` 两条模板在真实 PostGIS 上 38/38 PASS
  （`postgis-test-results.json`，2026-11-03 实机）。其余 V32 后端不升。
- 旧文档 `198 = ok 157 + unverified 19 + not_supported 22` 与实数差：
  **ok −5、unverified +2、总数 −3**。旧 157 的 ok 差额中，1 条由 V32@postgis 补齐；
  其余 5 条无对应叶，按实数记账，不伪造补叶。
- 同步位置：
  - `code/README.md`：198/157/19 → 195/152/21；自检 148 → 150；SuperMap 待验 19 → 16。
  - `V03-WORKLIST-V2-GENERALIZED-20261103.md`：终账行、G3 的 198 → 195、B 类标题注明
    “另有 V32 两叶 unverified，合计 21”，末尾新增 Phase 1 执行记录。
  - `leaves-full.json`：195 行不变；V32 四行状态/注记更新；B1 覆盖层字段回灌。
  - `V03-WORKLIST.md`：顶部加“历史文件”横幅，说明 198 已被终账取代；
    历史正文不重写，保留逐叶来源。
  - `G3-TAGGING-CHANGELOG-20261103.md`：末尾新增 §6“Phase 1 销账”，正式关闭 G3 差异注记。
- 证据：`evidence/phase1/accounting.txt`（baseline → current 逐项对照）。

### 2.2 7 条实机校准模板回写生成器（防漂移）

- 在 `code/build_mapping.py` 增加 **`CALIBRATED_TEMPLATES` 校准覆盖层**（7 条：`clip_raster`、
  `spatial_join`、`mapalgebra`、`hillshade`、`reclass`、`validate_repair`、`mvt_tile`），
  在 `TEMPLATE_BY_ID` 之前替换旧定义；内容逐字取自 2026-11-03 在册定版。
- 同步把 `postgis_templates.json` 的写出缩进改为 `indent=1`（在册文件格式），
  并把 6 个产物统一为 `newline="\n"`，消除 Windows CRLF 漂移。
- 干净副本重跑（`_phase0/phase1-verify`）：

```
6 个产物全部 IDENTICAL：
mapping.json / verbs.json / gp_registry.json / processing_registry.json /
postgis_templates.json / mock_tools.json
```

- 新增自检 **A8**：导入 `build_mapping.TEMPLATES`，与在册 `postgis_templates.json`
  36/36 逐对象比较；任何人再把生成器改回旧版，自检立即红。
- 证据：`evidence/phase1/product-compare.txt`、`evidence/phase1/generator-phase1.log`。

### 2.3 V32 裁决（三处统一）

裁决依据（证据优先，不按“落名即 ok”放水）：

| 后端 | 裁决 | 依据 |
|---|---|---|
| postgis | **ok**（check+repair） | `validate_check`/`validate_repair` 模板在真实 PostGIS 38/38 PASS；网关执行器 `postgis_exec_template` 仍 pending，故 ok 仅指映射/模板实机，不是网关端到端 |
| qgis | **unverified** | `qgis:checkvalidity`、`native:fixgeometries` 仅在 Processing 种子账，未实机；`qgis_run_processing` pending |
| arcgis-pro | **unverified** | GP 注册表/白名单在册，但无 Pro 环境、未实机；`arcgis_run_gp` pending |
| supermap | **not_supported**（维持） | 设计 §2 V32 的本波决定；B1/D5 已名验通 `topology_validate`，但无适配实现，不冒充可执行 |

同步结果：

- `code/verbs.json` V32：postgis 保持 ok；qgis/arcgis-pro 降 unverified；supermap 维持
  not_supported（注记写明 B1/D5 名验通）。`code/mapping.json` 的 `supported_verbs` 相应
  移除 qgis/arcgis-pro 的 V32（2 行差异）。
- `leaves-full.json` V32：postgis 升 ok 并补 kind/native/证据注记；qgis/arcgis-pro 补
  kind/native 与 unverified 理由；supermap 补 `b1_*` 字段。
- `selftest.py`：
  - **A9** 新增“verbs 与 leaves 的 V32 状态一致”断言；
  - **B96** 从“qgis 校验成功”改为“qgis 校验回 `UNVERIFIED_MAPPING` 且未发原生调用”；
  - B97/B98（postgis 修复的 confirm 门与新表模板）保持不变并通过。
- 语义冻结：V32 的名称与语义未改；只改后端状态与证据注记；破坏性分级未降。

### 2.4 B1 SuperMap 叶成果回灌

- 将 `b1-reconciliation.json` 的 **16 条 verdict** 写入 `leaves-full.json` 的
  `b1_verdict` / `b1_native` / `b1_ref` / `b1_note` 字段，并在原 `note` 后追加证据说明。
- **12 条名验通**（10 `name_verified_function` + 2 `name_verified_class`）**未升 ok**，
  仍为 unverified；另 1 条 `pending_check`（V20/difference）、3 条 `unresolved`
  （V06/V07/V12）也一并记录，覆盖层不再作为第二真源。
- V32 supermap 另记 D5 的 `topology_validate` 名验通（`b1_ref: B1/D5 (2026-11-03)`）。
- 回灌后 `b1_verdict` 行共 17 行：11 function（10 B1 + 1 D5）、2 class、1 pending、3 unresolved。

### 2.5 自检与 Windows 可移植性

- 自检 **150/150，退出码 0**，且**不再需要 `PYTHONUTF8=1`**。
- 新增 A8/A9 两条断言；B 段 B96 改为拒绝路径；C 段 13 条 e2e 全过。
- 修复：`McpClient` 的 `Popen` 显式 `encoding="utf-8", errors="replace"`；
  `selftest-results.txt` 显式 `newline="\n"`。
- 证据：`evidence/phase1/selftest-150.log`、`evidence/phase1/selftest-results-150.txt`。

## 3. 账面数字变化对照表

| 项目 | 阶段前 | 阶段后 | 变化与理由 |
|---|---|---|---|
| 叶子总数 | 195 | **195** | 不变 |
| ok | 151 | **152** | V32@postgis 模板实机 38/38，升 ok |
| unverified | 22 | **21** | 同上，−1 |
| not_supported | 22 | **22** | 不变（V32@supermap 维持） |
| 每动词至少 1 条 ok | 39/40 | **40/40** | V32@postgis 补齐 |
| pending / existing | 21 / 12 | **21 / 12** | 不变 |
| tier core/extended/exclusive | 163/32/0 | **163/32/0** | 不变；exclusive 仍待阶段 5 裁决 |
| B1 `b1_verdict` 行 | 0 | **17** | 16 条 B1 + 1 条 D5/V32；12 条名验通未升 ok |
| 生成器模板漂移 | 7 条 | **0 条** | 校准覆盖层；6/6 产物字节一致 |
| 自检 | 148/148 | **150/150** | A8/A9 新增；B96 改拒绝路径；Windows 编码修复 |
| 文档总账 | 198/157/19 | **195/152/21** | README 与 V2 施工单同步；v1/G3 加历史/销账注 |

## 4. `git diff` 逐项解释

| 文件 | 改动 | 原因 |
|---|---|---|
| `code/build_mapping.py` | 7 条 `CALIBRATED_TEMPLATES` 覆盖层；V32 三后端状态/注记；`GIS_GATEWAY_MANIFEST` 环境变量；6 产物 `newline="\n"`；模板 JSON `indent=1` | 防 7 模板回退；V32 与生成器同账；Windows 字节级复现 |
| `code/verbs.json` | V32 postgis 注记；qgis/arcgis-pro 降 unverified；supermap 注记 | V32 裁决；由生成器重跑产出，非手改 |
| `code/mapping.json` | qgis/arcgis-pro 的 `supported_verbs` 移除 V32（2 行） | 同上的派生结果 |
| `leaves-full.json` | V32 四行；B1 16 条 + D5 1 条 `b1_*` 字段 | V32 裁决；B1 回灌 |
| `code/selftest.py` | A8/A9；B96 改拒绝；Popen UTF-8；结果文件 LF | 防漂移、三处对账、Windows 可移植 |
| `code/selftest-results.txt` | 148 → 150；新增 A8/A9；B96 文案 | 自检实测输出 |
| `code/README.md` | 195/152/21；150 checks；SuperMap 16 条 | 文档与账本同步 |
| `V03-WORKLIST-V2-GENERALIZED-20261103.md` | 终账行；198→195；B 类标题；Phase 1 执行记录 | 现行施工单同步 |
| `V03-WORKLIST.md` | 顶部历史横幅 | 保留历史，不再作真源 |
| `G3-TAGGING-CHANGELOG-20261103.md` | §6 Phase 1 销账 | 正式关闭 G3 差异注记 |
| `evidence/phase1/*` | 自检、6/6 比对、账面变化、生成器日志 | 阶段证据落盘 |

## 5. 未完成与原因

1. **原始 manifest 未提供**：本阶段生成器重跑沿用 Phase 0 的“名称补全”重建 manifest；
   其 `scope_note` 与在册 `mapping.json` 逐字一致，6/6 产物字节一致。拿到原件后应再跑一次复核。
2. **旧 157 的 ok 差额**：仍有 5 条无对应叶；本阶段按实数 152 记账，不补造叶。
   若后续找到漏抽来源，另开账目并留痕。
3. **qgis / arcgis-pro V32 现在会被拒绝**（UNVERIFIED_MAPPING）：这是证据纪律下的正确行为；
   要恢复可用，需 QGIS 实机校准 / Pro 环境，分别留到阶段 4 与后续。
4. **PostGIS 38/38 未复跑**：本机未起 PostgreSQL/PostGIS 实例；只引用存档结果。
5. **版本号未升 v0.3**：`gateway.py` 仍 `0.2.0`。版本落码与 tier exclusive 裁决留到阶段 5，
   避免本阶段扩散改动面。
6. **真实后端 e2e 未做**：阶段 4 目标。

## 6. 下一阶段入口条件

**满足。** 阶段 2（GDAL 后端接入）可开工。本机入口已实测：

- `C:/Program Files/QGIS 3.44.15/bin/gdalinfo.exe` / `ogrinfo.exe`：GDAL 3.13.3；
- `C:/Program Files/QGIS 3.44.15/apps/Python312/python.exe`：
  `from osgeo import gdal` → 3.13.3。

阶段 2 将按 postgis/qgis 的接入契约实现 `gdal` 适配层，先覆盖栅格/矢量最常用动词；
每条 ok 映射必须有本地 GDAL 实跑证据，跑不通的记 unverified。

## 7. 证据索引

- `evidence/phase1/selftest-150.log`：150/150 完整输出（UTF-8）
- `evidence/phase1/selftest-results-150.txt`：自检结果文件副本
- `evidence/phase1/product-compare.txt`：干净副本 6/6 产物哈希与一致结论
- `evidence/phase1/generator-phase1.log`：生成器重跑 stdout（1833/374/40/36）
- `evidence/phase1/accounting.txt`：195 账目 baseline → current 对照
- `evidence/phase1/v32` 相关证据见 `accounting.txt` 与 `leaves-full.json` diff

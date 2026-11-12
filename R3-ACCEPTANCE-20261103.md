# R3 探针验收（2026-11-03 晚，Muse 按结果本体验收）

结果本体：`calibration-r3-result.json`（75,878 字节，JSON 主体 68,024 字符可解析；首尾 JVM 日志为 2>&1 合并噪声）。执行方 WorkBuddy 回报与本体逐项一致。

## 实机验通（探针级，非网关工具本体）

- 建源全链（set_type/set_server/set_alias → create_datasource）：R2、R3 两轮稳定复现。
- **V05 建数据集**：`DatasetVectorInfo()` + `set_name`/`set_type(DatasetType.POINT)` → `create_dataset(info)`，回读 name/type 一致、`get_dataset` 回环取回 DatasetVector。R2 卡点关闭。附带定论：`create_dataset` 首参为 DatasetVectorInfo（docstring 在档）；`create_vector_dataset(name, type)` 为另一条 docstring 在档的单发路径（未实测）。
- **V06 建字段（创建侧）**：`FieldInfo()` + `set_name`/`set_type(FieldType.DOUBLE|TEXT)`，score/label 均建成。
- 加记录：`get_recordset(False)` → add/set_value/update，记录数 1。
- **V12/V13 追加**：`DatasetVector.append(source)` 返回 True，记录数 1→2。
- 残留之谜关闭：R3 启动自清 R2 残留（prev_scratch_cleanup=removed），坐实 R2 残留系活句柄锁定；R3 收尾 scratch 全删。

## 未验通（留批 1 / R4，均已精确定位）

- **V07 remove_field**：方法存在（DatasetVector 成员表在档），调用无异常但字段数 7→7，疑似 UDB 引擎静默 no-op。R4 须以 field_infos 字段名清单（非计数）复核，并试空数据集/重开后删除；若仍 no-op，注册表标注 UDB 引擎限制。
- **V29 统计**：`Recordset.statistic('score', mode)` 签名为两参（单参 TypeError 在档），调用被接受但返回 None。成员表另有 `DatasetVector.stat`——R4 改走此路，且先回读确认 set_value 真落值。
- **V14 投影赋值**：`set_prj_coordsys(PrjCoordSys())` 调用通过、无回读，暂记调用级；R4 补 prj_coordsys 回读。

## 观察项降级

- JVM `WrapjMObjects.dll` UnsatisfiedLinkError：三轮都在、从未阻断任何步骤，降为背景噪声，不再单列异常。

## 证据口径

以上为 iobjectspy 原生调用级实机证据；网关工具本体（supermap 适配层）仍未 live 跑，注册表状态升格留批 1 按流程办理，不因探针结果自动升格。

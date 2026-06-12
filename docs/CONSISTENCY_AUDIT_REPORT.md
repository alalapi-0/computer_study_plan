# 仓库描述一致性审计报告

> 生成日期：2026-06-12 · 脚本：`python3 scripts/check_user_journey.py`

## 摘要

- 测试用例：20 项，通过 20，失败 0
- 概览 md：22 · 完整实操骨架：22
- 进度已接入：round_00, round_01, round_02, round_03, round_04, round_05, round_06, round_07, round_08, round_09, round_10, round_11, round_12, round_13, round_14, round_15, round_16, round_17, round_18, round_19, round_20, round_21
- 进度闭环（脚本+看板+JSON）：round_00, round_01, round_02, round_03, round_04
- 仅骨架（未接入进度）：无

## 用户旅程测试用例

| ID | 类别 | 标题 | 结果 | 说明 |
|----|------|------|------|------|
| TC-01 | 首次进入 | 确认仓库根目录可识别 | ✅ | OK: 仓库根 |
| TC-02 | 首次进入 | WORKSPACE.md 存在且描述仓库根自检命令 | ✅ | WORKSPACE.md 包含自检说明 |
| TC-03 | 日常使用 | mark_done.sh 无参数可列出任务 | ✅ | 用法：bash mark_done.sh <task-id> [--undo] |
| TC-04 | 日常使用 | progress.json 结构合法（lanes + tasks） | ✅ | tasks=280 |
| TC-05 | 看进度 | progress_data.js 存在且含 PROGRESS_DATA | ✅ | progress_data.js OK |
| TC-06 | 看进度 | progress_rounds.json / .js 与轮次扫描一致 | ✅ | rounds in JSON=22, expected=22 |
| TC-07 | Round 练习 | Round 00 练习脚本语法检查通过 | ✅ | 全部 bash -n 通过 |
| TC-08 | 进度一致性 | progress.json 任务 ID 可映射到 round_id | ✅ | 全部 280 个任务可映射 |
| TC-09 | 看进度 | 看板中已注册任务 ID 均存在于 progress.json | ✅ | 看板任务与 progress.json 对齐 |
| TC-10 | 文档准确 | README 不声称全部 Round 已接入进度看板（若实际未接入） | ✅ | UI=22, scaffold_only=0; 未发现明显夸大表述 |
| TC-11 | Agent 协作 | file_naming_rules 不与实际展开状态矛盾 | ✅ | file_naming_rules 无过时「仅 round_00」表述 |
| TC-12 | 校验脚本 | validate_learning_data.py 通过 | ✅ | Data validation PASSED |
| TC-13 | 校验脚本 | check_protocol_sync.py 通过 | ✅ | Protocol sync check PASSED |
| TC-14 | Agent 协作 | agent_gate --verify 通过 | ✅ | Protocol sync check PASSED |
| TC-15 | 仓库结构 | 工程线 round_00–21 概览 md 与 rounds 目录齐全 | ✅ | md=22, dirs=22 |
| TC-16 | 进度一致性 | progress_store 能正确解析各 round 的 task_id | ✅ | resolve_round_id 抽样通过 |
| TC-17 | 网页学习 | learn_server 健康检查与网页打卡 API | ✅ | health + mark + content OK |
| TC-18 | 网页学习 | 练习向导 API（guide + Python run） | ✅ | guide_steps=4, py_run=True |
| TC-18 | 看进度 | Round 05–21 已接入 progress.json（任务数 ≥ 280） | ✅ | tasks=280, linked_rounds=22 |
| TC-19 | 网页学习 | learn_server 任务 events/feedback 与错题写入 API | ✅ | events=11, note=records/error_notes/engineering/journey_test/2026-06-12-note.md |

## 轮次状态（动态扫描，勿手工维护）

运行 `python3 scripts/round_status.py --markdown` 获取最新表。

```markdown
| 轮次 | 主题 | 层级 | 概览 md | 实操目录 | 进度任务数 | 看板 UI | 备注 |
|------|------|------|---------|----------|------------|---------|------|
| round_00 | Terminal 初见与学习系统搭建 | 进度闭环 | ✅ | ✅ | 21 | ✅ | — |
| round_01 | 文件系统与基础命令 | 进度闭环 | ✅ | ✅ | 12 | ✅ | — |
| round_02 | Shell、管道、Git 最小工作流 | 进度闭环 | ✅ | ✅ | 19 | ✅ | — |
| round_03 | Python 基础补强 + 复杂度直觉 | 进度闭环 | ✅ | ✅ | 12 | ✅ | — |
| round_04 | 核心数据结构 | 进度闭环 | ✅ | ✅ | 12 | ✅ | — |
| round_05 | 高频算法模式 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_06 | Linux 进阶与自动化 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_07 | 面向 AI 项目的综合练习 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_08 | 总复盘与升级路线 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_09 | 仓库规范化与测试入门 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_10 | Python 工程化基础 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_11 | 本地持久化与数据记录 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_12 | 自动化流水线与批处理 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_13 | 环境复现与发布基础 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_14 | HTTP 与 API 设计基础 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_15 | FastAPI 基础 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_16 | API 与数据层结合 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_17 | 服务化收口 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_18 | 数值计算与数据分析前置 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_19 | 机器学习最小闭环 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_20 | PyTorch 入门 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
| round_21 | NLP 前置基础 | 进度已接入 | ✅ | ✅ | 12 | ✅ | progress.json 有任务，练习脚本尚未调用 mark_done.sh |
```

## 修复记录

_本轮修复见对应 commit / PR。_

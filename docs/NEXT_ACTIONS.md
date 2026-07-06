# Next Actions

> 更新日期：2026-07-06
> 本文件只保留当前可执行任务队列。早期 TASK-002 至 TASK-012、旧 Phase 路线和已完成的大量 Round 填充日志已从正文移除；需要追溯时查看 git history。

## 当前推进规则

- 默认直接在 `main` 上修改、验证、commit、push。
- 每轮只做一个明确任务。
- 用户当轮直接指定任务时，以用户指令优先。
- 涉及考试、考纲、院校信息时，必须核验最新官方源。
- 涉及真实 VPS 写操作时，必须先取得用户明确授权。

## TASK-RR-56：治理规则改为直接推 main，并压缩旧路线文档

- 状态：**done**（2026-07-06）
- 背景：用户指出“禁止直接推送 main”的仓库规则不符合当前单人学习仓库协作方式；早期路线图过于陈旧，继续保留长篇旧 Phase/TASK 内容会误导后续 Agent。
- 目标：
  - 将 `AGENTS.md`、`docs/AUTO_ADVANCE_PROTOCOL.md`、治理文档、checklist、prompt 和 `agent_gate` 改为默认直接推 `main`。
  - 将 `docs/CODEX_LONG_TERM_PLAN.md`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md` 从历史日志型文档压缩为当前事实型文档。
  - 同步 README 中与 Git 流程、当前阶段、Web UI 启动端口相关的用户入口说明。
  - 修正 `agent_gate` 任务标题解析，并让 `branch_hint` 输出为 `main`。
- 验收：
  - 当前规则文档不再要求“禁止直接推 main”或“必须独立分支”。
  - `python3 scripts/agent_gate.py --json --no-require-clean` 输出 `branch_hint: "main"`。
  - 标准验证命令通过。
- 是否需要用户介入：否。用户已明确授权直接改规则、直接推送，并说明当前不存在需要保护的真实学习记录。

## 推荐下一步

1. 继续做 Web UI 第三轮用户视角评测：重点检查首屏信息层级、教程/终端/记录的连续性、移动端工作区。
2. 从软考主线开始，把 `plans/soft_exam/` 的启动骨架扩展成可检查产物清单；具体考纲仍以最新官方源为准。
3. 如要启动 VPS 支线，先按 `docs/templates/remote_operation_confirmation.md` 取得授权，再记录真实操作结果。

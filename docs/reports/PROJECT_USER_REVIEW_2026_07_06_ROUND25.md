# Project User Review · Round 25

> 日期：2026-07-06
> 视角：普通学习者 + 后续自动推进 Agent
> 范围：`AGENTS.md`、`docs/AUTO_ADVANCE_PROTOCOL.md`、Cursor UI runbook / prompt、`scripts/agent_gate.py`

## 本轮发现的 5 个问题

1. `AGENTS.md` 的“不破坏最小闭环”仍只保护 Round 00 与旧四件套，遗漏当前 Web UI、`rounds_data.js`、本地 API、动作日志和反馈目录。
2. `docs/AUTO_ADVANCE_PROTOCOL.md` 虽然要求运行 `agent_gate.py --verify`，但协议没有说明涉及 Round 元数据或反馈时还要补跑生成 / 同步命令。
3. 自动推进协议中“修改进度系统”只点名 `mark_done.sh`、`progress.json`、`progress_data.js`，且只要求 `bash mark_done.sh`，不足以覆盖当前 Web UI / 本地 API / 前端脚本。
4. `docs/prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md` 的 UI 任务约束仍把业务闭环缩成 `progress.json` + `mark_done.sh`，会低估 `rounds_data.js`、`progress_ui.js`、本地 API、动作日志和反馈的重要性。
5. `docs/cursor_browser_ui_runbook.md` 还把本仓库描述成“进度看板 / 本地静态页”，并在修改步骤里只泛泛说“不改变业务逻辑”，没有列出当前 Web UI 学习工作区必须保持的闭环。

## 修复摘要

- 将 AGENTS 的最小闭环保护范围扩展到当前 Web UI 进度系统。
- 更新自动推进协议中的验证说明和进度系统修改验证命令。
- 将 `agent_gate.py --verify` 扩展为真实低成本验证基线：`git diff --check`、`node --check progress_ui.js`、协议 / 数据校验、JSON 校验和 CLI 摘要。
- 更新 Cursor UI prompt 和 runbook，把“静态页 / 看板”口径改为本地 Web UI 学习工作区，并明确需要保护的数据 / API / 日志 / 反馈闭环。

## 验证结果

- `python3 scripts/agent_gate.py --verify` 通过，覆盖 `git diff --check`、`node --check progress_ui.js`、协议 / 数据校验、JSON 校验和 CLI 摘要。
- `agent_gate.py --verify` 的 JSON 校验已静默执行，不再把完整 `progress.json` 打到验证输出里。
- `python3 scripts/agent_gate.py --json --no-require-clean` 输出 `branch_hint: "main"`，并列出当前验证基线。
- 文本扫描确认目标旧说法不再残留。
- 浏览器回检通过：默认页显示学习工作区、`读教程`、`记录并完成`；`progress.html?round=round_02` 显示 `终端练习` 并绑定 `~/cli-lab/round2`；390px 移动端无横向溢出。

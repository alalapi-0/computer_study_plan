# Agent 协作说明（Cursor 补充）

> 主协作规则见 [`AGENTS.md`](AGENTS.md)。本文件为 Cursor Agent 的补充入口。

## Cursor Browser UI Workflow

与 `AGENTS.md` 中 **Cursor Browser UI Workflow** 章节一致，要点：

1. 普通前台 Agent；禁止 Multitask 控制浏览器
2. before / after 真实页面检查
3. chrome-devtools / playwright / filesystem / context7 / github 分工
4. 缺工具 → `BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY`

Runbook：`docs/cursor_browser_ui_runbook.md`

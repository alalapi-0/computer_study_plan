# Codex Repository Instructions

本仓库自 2026-05-12 起的总目标是：以**软考中级（默认软件设计师，高分/满分导向）**为短期主线，承接**数学二 / 408 / 0854 跨专业考研**作为中长期主线，同时保留 Linux / Shell / Git / Python / AI 工程实操作为"工程实操线"。

详细路线见 `docs/MASTER_STUDY_ROADMAP.md`。

## 本地工作副本（固定）

- **唯一 Git 仓库根**：`~/PycharmProjects/computer_study_plan`（本机绝对路径 `/Users/alalapi/PycharmProjects/computer_study_plan`）
- Cursor / PyCharm **工作区必须打开该目录**；文档与脚本中的「仓库根」均指此处
- Round 00 终端练习沙盒为 `~/cli-lab/round0`（不进 Git，与仓库根不同）
- 完整约定见 `docs/WORKSPACE.md`；不要在文档中再写 `Desktop/computer_study_plan` 为默认路径

## 每次工作前必须读取

1. `docs/WORKSPACE.md`（路径与工作区，避免改错目录）
2. `docs/MASTER_STUDY_ROADMAP.md`（总目标与四主线）
3. `docs/STAGE_PLAN.md`（Stage 0–7 阶段计划）
4. `docs/CODEX_LONG_TERM_PLAN.md`（长期协作规则，含 2026-05-12 重定向说明）
5. `docs/PROJECT_STATE.md`（仓库当前状态）
6. `docs/NEXT_ACTIONS.md`（下一步任务队列）

> 历史规划（"网页交互式学习系统"Phase 0–7）仍保留作为工程实操线的演进参考，但**不再是最高优先级**。

## 工作原则

- 每轮只做一个明确任务，优先选择 `docs/NEXT_ACTIONS.md` 中最高优先级且不需要用户介入的任务。
- 不破坏 Round 00 已有可运行能力，尤其是 `rounds/round_00/`、`progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh` 的最小闭环。
- 不破坏 `records/` 下任何已写入的用户真实学习记录。
- 不缓存具体考题、考点条目、院校招生数据；涉及考试内容一律以**最新官方信息**为准。
- 不把未来规划写成已完成事实。
- 不一次性大范围重构无关内容。
- 不直接 push `main`。
- 每轮完成后必须运行验证，更新文档，commit，并在 remote 存在时 push 独立分支。

## Git 规则

- 每轮使用独立分支，默认命名：`codex/<task-id>-short-title`。
- 验证通过后再 commit。
- remote 存在时 push 到 GitHub 分支。
- 不直接 push `main`。

## MCP Tools

当前项目运行时需要以下 MCP Servers（通用 5 项由 Cursor Home `~/.cursor/mcp.json` 提供，本项目仅配置 `filesystem`）：

- chrome-devtools（全局）
- context7（全局）
- filesystem（项目级）
- github（全局）
- playwright（全局）
- stitch（全局）

用途：

- **chrome-devtools**：用于浏览器调试、console、network、页面状态检查。
- **context7**：用于查询第三方库和框架文档。
- **filesystem**：用于安全读取和检查当前项目文件。
- **github**：用于仓库、提交、分支、issue、PR 等相关操作。
- **playwright**：用于浏览器自动化、页面操作、E2E 检查。
- **stitch**：用于 UI 设计输入与设计变体参考（需 `STITCH_API_KEY` 环境变量）。

自动推进轮开始前，Agent 必须确认这些 MCP 已加载。

如果某个 MCP 不可用，Agent 需要记录原因，并使用可用替代方案继续推进。

涉及页面、审核台、生成结果、预览、发布流程的任务，必须使用 chrome-devtools 或 playwright 进行真实浏览器检查。

项目级配置位于 `.cursor/mcp.json`（仅 `filesystem`）；通用 server 见 Cursor Home。可运行 `npm run check:mcp` 或 `node scripts/check_mcp_config.js` 验证；CLI 层状态另见 `npm run check:cursor-mcp`。修改后可能需要重启 Cursor 或重新加载窗口。

## Cursor Browser UI Workflow

Cursor 执行 UI 优化（如 `progress.html`）时必须遵守：

1. **必须使用普通前台 Agent**——禁止 Multitask / 后台子 Agent 控制浏览器。
2. **禁止 Multitask 控制浏览器**——子 Agent 通常不继承 Workspace MCP。
3. **每轮 UI 实现必须先检查真实页面**——启动本地服务并打开目标 URL。
4. **每轮 UI 实现必须使用 before / after 浏览器检查**——截图或记录观察结果。
5. **Stitch 用作设计输入**——不得无审查覆盖代码。
6. **chrome-devtools 用作页面调试**——console、network、截图。
7. **playwright 用作回归测试**——稳定 E2E 验证。
8. **filesystem 用作文件真值检查**——仅限当前项目目录。
9. **context7 用作文档查询**——前端库与框架文档。
10. **github 用作提交和远程状态**——token 仅通过环境变量。
11. **当前线程缺工具时必须 BLOCKED**——输出 `BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY`，不要继续假装执行。

详细 runbook：`docs/cursor_browser_ui_runbook.md`  
工具注册排查：`docs/cursor_tool_registry_check.md`  
下一轮 Prompt 模板：`docs/prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md`

## 高风险停止条件

遇到以下情况必须停止并向用户报告：

- git 工作区有用户未提交修改。
- 需要删除或迁移已有学习记录但无法保证安全。
- 需要删除 `records/` 下已写入的真实学习记录。
- 需要引入大型新依赖。
- 需要从 JSON 切换到数据库。
- 需要从静态页面切换到前端框架。
- 需要创建后端服务。
- 需要修改 GitHub remote 或认证。
- 需要把任何院校 / 考试 / 考纲信息写入仓库但无法访问最新官方源。
- push 失败、merge conflict、验证连续失败，或任务边界不清。

## Workspace Tooling Standard

本项目的通用 MCP 工具（chrome-devtools / playwright / context7 / github / stitch）与跨项目分工规则
遵循工作区级标准，详见：
`/Users/alalapi/PycharmProjects/.agent_workspace/docs/AGENT_TOOLING_STANDARD.md`

本项目专属、不可全局化的工具（如有）：见本文件 MCP 配置章节。

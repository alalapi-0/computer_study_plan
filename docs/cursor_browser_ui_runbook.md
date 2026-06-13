# Cursor 浏览器 UI 推进 Runbook

> 本仓库用于学习总控与进度看板；当需要优化 `progress.html` 等本地 Web 页面 UI 时，按本文执行。
> 详细工具注册排查见 [`cursor_tool_registry_check.md`](cursor_tool_registry_check.md)。

---

## 1. Cursor 浏览器任务的基本原则

| 原则 | 说明 |
|---|---|
| **MCP server ready ≠ 当前 Agent 线程可用** | CLI 或 Settings 显示 ready，只代表 server 进程可启动；当前对话线程未必已暴露对应工具。 |
| **Settings 中启用 ≠ 旧对话能调用** | 在 Settings → Tools & MCP 批准或启用后，**已有 Agent 对话**可能仍使用批准前的工具注册表。 |
| **批准 MCP 后需完全退出 Cursor** | 批准后应 **完全退出 Cursor**（不是仅 Reload Window），重新打开本仓库，再新建普通前台 Agent 对话。 |
| **浏览器任务必须用普通前台 Agent** | 涉及页面打开、截图、console、network、Playwright 操作的任务，必须在**普通前台 Agent** 中执行。 |
| **禁止 Multitask / 后台子 Agent** | 禁止用 Multitask 或后台子 Agent 执行浏览器控制；子 Agent 通常**不继承** Workspace MCP 工具。 |
| **开始前检查当前线程实际暴露的工具** | 不要假设 `.cursor/mcp.json` 存在即代表可用；必须在当前对话中确认目标 MCP 工具已暴露。 |
| **缺工具时必须 BLOCKED** | 若当前线程没有目标工具，输出 `BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY` 并停止，**不要假装执行**浏览器操作。 |

---

## 2. 工具选择规则

本仓库（如 `progress.html`、本地静态页）UI 优化优先使用：

| 工具 | 用途 |
|---|---|
| **chrome-devtools** | 检查页面、console、network、截图 |
| **playwright** | E2E 与稳定回归 |
| **filesystem** | 检查代码与产物（仅限当前项目目录） |
| **context7** | 查询前端库 / 框架文档 |
| **github** | commit / push / issue / PR |

### 真实页面 UI 优化（必做检查项）

每次 UI 改造必须执行：

1. 打开页面
2. 截图
3. 检查 console
4. 检查 network
5. 记录 **before** 状态
6. 修改 UI 代码
7. 再打开页面
8. 截图
9. 检查 **after** 状态
10. 修复发现的问题

---

## 3. 标准 UI 优化流程

固定 13 步，每轮只推进一个主要 UI 切片：

1. 读取 `README.md`、`AGENTS.md`、`docs/MASTER_STUDY_ROADMAP.md` 及 `docs/design/`（若存在）
2. 启动项目（如 `python3 -m http.server 8000` 打开 `progress.html`）
3. 用 browser / chrome-devtools / playwright 打开目标页面
4. 保存 **before** screenshot
5. 选择一个 UI 改造切片（每轮一个）
6. 修改代码（不改变业务逻辑）
7. 重新打开页面
8. 检查 console / network
9. 检查响应式（常见 viewport）
10. 运行可用测试（`npm run check:mcp`、`npm run check:cursor-mcp`、相关 Python 校验等）
11. 保存 **after** screenshot
12. 更新相关文档（如 `docs/PROJECT_STATE.md`）
13. commit / push（独立分支，不直接 push main）

---

## 4. 当前线程工具检查

当用户要求使用某个 MCP 时，Agent **必须先确认当前对话线程**是否暴露对应原生工具。

**不要只依赖：**

- `cursor-agent mcp list`
- Settings 中的 ready 状态
- `.cursor/mcp.json` 文件存在

若当前线程没有对应工具，输出：

```
BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY
```

并告知用户：

1. **完全退出 Cursor**（Quit，不是 Reload Window）
2. 重新打开本仓库
3. 在 **Settings → Tools & MCP** 中确认目标 server 为 ready
4. **新建普通前台 Agent 对话**（禁用 Multitask）
5. 重新执行任务

配置层检查命令（**不代表**当前线程已暴露工具）：

```bash
npm run check:cursor-mcp
# 或
bash scripts/check_cursor_mcp_status.sh
npm run check:mcp
```

---

## 5. MCP 批准与用户操作清单

若检查结果显示 MCP **not loaded** 或 **needs approval**：

1. 打开 Cursor **Settings → Tools & MCP**
2. 批准/启用本仓库 `.cursor/mcp.json` 中的 server
3. 为需要的环境变量在本地配置（见 `.env.example`，**不要提交 `.env`**）：
   - `GITHUB_PERSONAL_ACCESS_TOKEN`（github MCP）
4. **完全退出 Cursor 并重新打开项目**
5. 新建**普通前台 Agent** 对话后再执行 UI 任务

---

## 6. 相关文档

| 文档 | 用途 |
|---|---|
| [`cursor_tool_registry_check.md`](cursor_tool_registry_check.md) | 当前线程工具注册排查表 |
| [`prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md`](prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md) | 下一轮 UI 推进可复制 Prompt |
| [`../AGENTS.md`](../AGENTS.md) | Agent 协作硬规则 |
| [`../.cursor/rules/cursor-browser-ui.mdc`](../.cursor/rules/cursor-browser-ui.mdc) | Cursor UI 规则 |
| [`../.cursor/rules/no-multitask-for-browser.mdc`](../.cursor/rules/no-multitask-for-browser.mdc) | 禁止 Multitask 浏览器规则 |

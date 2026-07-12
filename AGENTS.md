# AGENTS.md · 项目级事实与执行契约

本文件适用于仓库根目录及全部子目录。它只记录可由当前仓库代码、配置和现行项目文档核对的事实。事实来源发生冲突时，先停止并核对来源；无法确认的命令或能力统一标记为「待验证」，不得猜测。

仓库根目录固定为：

- `~/PycharmProjects/computer_study_plan`
- `/Users/alalapi/PycharmProjects/computer_study_plan`

开始工作前必须读取：

1. `docs/WORKSPACE.md`
2. `docs/MASTER_STUDY_ROADMAP.md`
3. `docs/STAGE_PLAN.md`
4. `docs/CODEX_LONG_TERM_PLAN.md`
5. `docs/PROJECT_STATE.md`
6. `docs/NEXT_ACTIONS.md`

主要事实来源：`README.md`、`package.json`、`.cursor/mcp.json`、`.cursor/rules/**`、上述六份文档、`docs/PROGRESS_RULES.md`、`docs/governance/**`、`docs/cursor_tool_registry_check.md`、`scripts/**`、`mark_done.sh` 和 `.gitignore`。

## 1. 项目目标

本项目是本地优先的长期计算机学习总控仓库：

- 短期主线：软考中级，默认软件设计师，高分 / 满分导向。
- 中长期主线：数学二、408 兼容基础、0854 跨专业考研准备。
- 工程实操线：Linux、Shell、Git、Python、Web/API、数据与 AI 工程练习。
- Web UI 用于阅读、练习、终端联动、记录、存档和复盘。

进度系统使用四条固定 lane：

| lane | 含义 |
|---|---|
| `engineering` | 工程实操线 |
| `soft_exam` | 软考中级线 |
| `math2` | 数学二线 |
| `cs408` | 408 / 0854 线 |

当前产品边界是不使用数据库、账号系统或云同步；不把前端框架或大型平台建设写成当前已实现事实。

来源：`docs/MASTER_STUDY_ROADMAP.md`、`docs/CODEX_LONG_TERM_PLAN.md`、`docs/PROJECT_STATE.md`、`scripts/progress_lib.py`。

## 2. 技术栈

- 浏览器端：静态 HTML/CSS、原生 JavaScript，入口为 `progress.html` 与 `progress_ui.js`。
- 本地服务与维护脚本：Python 3；`scripts/progress_server.py` 使用 Python 标准库 HTTP 服务。
- 命令行入口：Bash（`mark_done.sh`）。
- 数据与内容：JSON、JSONL、Markdown，以及由 JSON 生成的 JavaScript 数据镜像。
- Node.js / npm：仅作为现有 npm 脚本入口、JavaScript 语法检查和 MCP 配置检查工具。

`package.json` 没有 `dependencies` 或 `devDependencies`。仓库基线未发现 Node lockfile、Python 依赖清单、前端框架配置或数据库配置，因此不得声称项目依赖这些组件。

来源：`package.json`、`progress.html`、`progress_ui.js`、`scripts/progress_server.py`、`scripts/*.py`、`mark_done.sh`。

## 3. 安装与运行前提

- 安装命令：**待验证**。仓库没有可验证的安装脚本或依赖清单；不要猜测执行 `npm install`、`npm ci`、`pip install` 等命令。
- Python、Node.js、npm、Bash 的最低版本：**待验证**。仓库没有固定版本文件或 `engines` 声明。
- 已有命令要求本机能直接调用 `python3`、`node`、`npm` 和 `bash`；这只是运行前提，不等于已固定版本或已提供安装流程。
- 日常 Web UI 需要本机浏览器。练习沙盒位于 `~/cli-lab/roundN`，不在 Git 仓库中。

来源：`package.json`、`docs/WORKSPACE.md`、`README.md`、`scripts/progress_server.py`、`mark_done.sh`。

## 4. 启动命令

在仓库根目录运行以下任一已登记的本地服务入口：

```bash
python3 scripts/progress_server.py
# 或
npm run serve
```

默认页面：`http://127.0.0.1:8777/progress.html`。

服务启动时会从 `progress.json` 同步 `progress_data.js`。直接打开 `progress.html` 或使用普通静态服务器只适合只读布局 / 进度检查，不提供写 API、练习脚本运行、动作日志或浏览器终端能力。

CLI 入口：

```bash
bash mark_done.sh                         # 查看各 lane 的未完成任务
bash mark_done.sh --all                   # 查看全部任务
bash mark_done.sh <task-id>               # 补录完成；会写进度与记录
bash mark_done.sh <task-id> --undo        # 撤销完成；会写进度与记录
```

来源：`package.json`、`README.md`、`docs/WORKSPACE.md`、`scripts/progress_server.py`、`scripts/mark_done_cli.py`、`scripts/progress_lib.py`、`mark_done.sh`。

## 5. lint、类型检查、单元测试、端到端测试

| 类别 | 当前可验证状态 |
|---|---|
| lint | **待验证：仓库未发现已配置的 lint 命令或 ESLint/Ruff 等配置。** |
| 类型检查 | **待验证：仓库未发现已配置的类型检查命令或 `tsconfig`/mypy 等配置。** |
| 单元测试 | **待验证：仓库未发现已配置的单元测试命令、pytest/tox 配置或测试目录。** |
| 端到端测试 | **待验证：仓库未发现已配置的自动化 E2E 命令或 Playwright 测试配置。** |

以下检查不得改称为上述四类测试：

- `node --check progress_ui.js` 仅是 JavaScript 语法检查。
- `git diff --check` 仅检查 diff 中的空白与冲突标记等错误。
- UI 的真实浏览器 before / after、console、network 检查是 UI 验收流程，不是仓库已配置的自动化 E2E 测试套件。

基线还未发现 Makefile、GitHub Actions 工作流或专用测试配置。新增真实工具前，保持上述项目为「待验证」。

来源：`package.json`、`scripts/agent_gate.py`、`.cursor/rules/**`、`docs/cursor_browser_ui_runbook.md`，以及冻结基线的仓库文件扫描。

## 6. 仓库标准验证命令

标准综合验证入口是：

```bash
python3 scripts/agent_gate.py --verify
```

该入口按顺序运行：

```bash
git diff --check
node --check progress_ui.js
python3 scripts/check_protocol_sync.py
python3 scripts/validate_learning_data.py
python3 -m json.tool progress.json
bash mark_done.sh --limit 5
```

这是仓库级综合验证，不是 lint、类型检查、单元测试或 E2E 的替代名称。任务如有更窄的确定性检查，应在标准验证之外追加并记录命令、退出码和关键输出。

涉及生成数据时，按生成关系运行相应生成器后再执行标准验证；UI 变更还必须执行第 11 节规定的真实浏览器检查。

来源：`scripts/agent_gate.py`、`docs/CODEX_LONG_TERM_PLAN.md`。

## 7. 关键目录与文件

| 路径 | 已验证用途 |
|---|---|
| `docs/` | 总路线、阶段计划、当前状态、任务队列、治理与运行说明 |
| `plans/` | `engineering`、`soft_exam`、`math2`、`cs408` 等学习计划入口 |
| `rounds/round_00/` 至 `rounds/round_21/` | 已展开的工程学习 notes、练习脚本和最终材料 |
| `rounds/stage_03_vps_remote_ops/` | VPS 只读学习与授权前准备材料 |
| `scripts/` | 本地服务、进度读写、生成、同步、校验与 Agent gate |
| `progress.json` | 任务完成状态单一事实源 |
| `progress_data.js` | 由 `progress.json` 同步得到的前端镜像 |
| `rounds_data.js` | 由构建脚本生成的 Round / 计划展示数据 |
| `progress.html`、`progress_ui.js` | 本地 Web UI 学习工作区 |
| `mark_done.sh` | CLI 查看、补录完成和撤销入口 |
| `records/` | 学习记录、动作日志、反馈、存档与终端历史目录 |
| `.cursor/` | 项目级 Cursor MCP 配置和 UI 工作规则 |
| `~/cli-lab/roundN` | 仓库外的工程练习沙盒 |

来源：`README.md`、`docs/WORKSPACE.md`、`docs/PROJECT_STATE.md`、`docs/PROGRESS_RULES.md`、对应脚本。

## 8. 允许修改与保护路径

仓库没有可验证的全局宽泛 allow-list。每轮只能修改用户当前请求或已冻结 `TASK_CONTRACT.allowed_paths` 明确列出的路径；路径边界不清时先停止。自动生成文件只能通过第 10 节列出的已验证生成器更新，不得手工编辑。

默认保护以下路径和能力闭环：

- `rounds/round_00/`
- `round_00.md` 至 `round_21.md`
- `progress.json`
- `progress_data.js`
- `rounds_data.js`
- `progress.html`
- `progress_ui.js`
- `scripts/progress_server.py`
- `mark_done.sh`
- `records/action_logs/`
- `records/feedback/`
- 用户后续明确标注为真实学习记录的 `records/` 内容

「保护」表示只有当前任务明确纳入范围且有相应验证时才可修改，不表示永远只读。现行项目文档明确说明：`records/` 整体目前不视为高保护区；不能据此推断未来真实记录已经存在，也不能在用户标注后覆盖这些记录。

任何任务都不得越过当前 allowed paths 修改业务代码、测试、验收条件、Git 配置 / 历史、remote、认证、用户数据、仓库外文件或外部系统。

来源：`docs/PROJECT_STATE.md`、`README.md`、`docs/governance/repo_rules.md`、`docs/governance/file_naming_rules.md`、`docs/PROGRESS_RULES.md`。

## 9. 核心用户旅程

1. 在仓库根启动 `scripts/progress_server.py`，打开默认 8777 Web UI。
2. 在学习工作区确认当前任务、阅读内联教程并按任务练习。工程任务可联动映射到 `~/cli-lab/roundN` 的浏览器终端；可运行练习只允许脚本白名单中的路径。
3. 点击「记录并完成」，在弹窗填写本次记录后保存。实现会更新 `progress.json`、同步 `progress_data.js`、追加动作日志并重新生成任务反馈。
4. 已完成任务可回看记录或撤销；撤销同样会更新进度、镜像、动作日志和反馈。
5. CLI 可查看任务，并按明确 task id 补录完成或撤销。
6. Web UI 可存档与读档；读档前实现会自动在 `records/saves/` 创建恢复点，再恢复进度、动作日志、终端历史和反馈。

来源：`README.md`、`docs/PROGRESS_RULES.md`、`scripts/progress_server.py`、`scripts/progress_lib.py`、`scripts/mark_done_cli.py`。

## 10. 生成资产与运行期记录保存位置

| 触发方式 | 输出 / 写入位置 | 关系 |
|---|---|---|
| `python3 scripts/build_rounds_data.py` 或 `npm run build:rounds` | `rounds_data.js`、`progress.json`、`progress_data.js` | 生成 Round 数据，将缺少的任务合并进进度源，再同步前端镜像 |
| `python3 scripts/sync_progress_data.py` 或 `npm run sync:progress` | `progress_data.js` | 从 `progress.json` 重新生成镜像，不改变任务状态 |
| `python3 scripts/generate_task_feedback.py` | `records/feedback/task_feedback.json` | 从进度与动作日志生成任务反馈 |
| Web UI / CLI 完成或撤销 | `progress.json`、`progress_data.js`、`records/action_logs/events.jsonl`、`records/feedback/task_feedback.json` | 更新状态、镜像、事件和反馈 |
| Web UI 存档 / 读档前恢复点 | `records/saves/*.json` | 本地存档；读档前自动生成恢复点 |
| Web UI 浏览器终端 | `records/terminal/commands.jsonl` | 本地终端命令历史；实际练习目录仍在 `~/cli-lab/roundN` |

`records/saves/*.json` 与 `records/terminal/commands.jsonl` 已被 `.gitignore` 忽略。`progress_data.js`、`rounds_data.js` 和 `records/feedback/task_feedback.json` 不允许手工编辑，应通过对应生成流程维护。

来源：`package.json`、`.gitignore`、`scripts/build_rounds_data.py`、`scripts/sync_progress_data.py`、`scripts/generate_task_feedback.py`、`scripts/progress_lib.py`、`docs/PROGRESS_RULES.md`。

## 11. Definition of Done

一次项目变更只有同时满足以下条件才算完成：

1. 实际 diff 只位于用户请求或冻结 TASK_CONTRACT 的 `allowed_paths`；没有越权修改。
2. 每个新增或修改的事实都能追溯到当前代码、配置、现行文档或独立命令证据；未知项明确标记为「待验证」。
3. 自动生成文件只由对应生成器更新，所有任务相关镜像 / 反馈同步关系保持一致。
4. `python3 scripts/agent_gate.py --verify` 通过；任务相关的额外确定性检查也通过，并记录命令、退出码和关键输出。
5. UI 变更已启动真实页面，完成 before / after 检查，并检查 console 与 network；非 UI 文档任务不强制浏览器检查。
6. 没有泄露密钥，没有破坏保护路径、用户记录、验收条件或现有 Round 00 / Web UI 最小闭环。
7. 独立 Judge 使用第 12 节的候选证据给出 `PASS`。Repair 的自述不构成完成证据。

## 12. Judge 可使用的证据和工具

### 12.1 可接受证据

Judge 只能依据独立、可复现的材料判断：

- 冻结且不可变的 TASK_CONTRACT。
- 分离登记的 `baseline_evidence_id` 与 `candidate_evidence_id`。
- worktree 路径、revision / HEAD 与候选 diff 身份。
- `git status`、`git diff`、`git diff --check`、`git diff --name-only` 等只读结果。
- 实际执行的命令、退出状态和关键输出。
- 相关源文件、配置和现行文档的只读检查。
- UI 任务的 before / after 截图或观察，以及 console / network 结果；本轮若仅修改文档则无需浏览器证据。

Repair 的解释、自信程度、推荐或自测结论不是独立证据。

### 12.2 可用工具及边界

- 本地只读文件检查、`rg`、Git 只读命令和 shell 确定性检查可用于复现证据。
- `filesystem` 只能检查当前项目目录。
- `chrome-devtools` / `playwright` 只在 UI 任务且当前线程实际暴露对应工具时使用。
- `context7` 只用于查询第三方库的官方文档。
- `github` 只用于核对远程仓库、提交、分支、issue / PR 等事实；不得把本地推测当远程事实。
- `stitch` 只提供 UI 设计输入，不能替代代码审查或真实页面验收。
- 工具未在当前线程实际暴露时必须标记「待验证」，不得伪造调用结果。

## 13. Agent / MCP 环境检查

MCP 可用性必须分三层核对；只有配置层、CLI 层和当前线程工具暴露层都通过，才可声称相应 MCP 在当前 Agent 中可用。

1. **项目配置层**：`.cursor/mcp.json` 只声明 `filesystem`，根路径为 `${workspaceFolder}`。
2. **Cursor Home / CLI 配置层**：`scripts/check_mcp_config.js` 期望 Cursor Home 配置提供 `chrome-devtools`、`context7`、`github`、`playwright`、`stitch`。
3. **当前线程层**：必须在每个新线程实际确认工具注册；普通前台 Agent、后台任务和不同产品线程的工具暴露不能互相推定。

检查命令及其证明范围：

```bash
npm run check:mcp          # 只验证静态 MCP 配置，不证明 CLI 或当前线程可调用
npm run check:cursor-mcp   # 只做 Cursor CLI / 配置层诊断，不证明当前线程可调用
```

2026-07-11 冻结基线状态：

- `npm run check:mcp` 通过，只证明静态配置检查通过。
- `npm run check:cursor-mcp` 的包装脚本退出码为 0，但每个 `cursor-agent` 子命令均报告 `SecItemCopyMatching failed -50`；因此 CLI 层不可据此判定可用。
- 当前线程的 Cursor MCP 工具暴露：**待验证**。不得把配置存在、包装脚本退出 0 或 Cursor Home 声明写成线程工具可用。

UI 浏览器任务必须由能实际访问所需工具的普通前台 Agent 执行，不得由后台 Multitask / 子 Agent 控制浏览器。当前线程缺少必需浏览器工具时停止并报告：`BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY`。

来源：`.cursor/mcp.json`、`.cursor/rules/**`、`scripts/check_mcp_config.js`、`scripts/check_cursor_mcp_status.sh`、`docs/cursor_tool_registry_check.md`、`docs/cursor_browser_ui_runbook.md`，以及 2026-07-11 冻结基线命令输出。

## 14. 安全与停止规则

- 每轮只处理一个明确任务；用户当轮明确指定的任务优先于 `docs/NEXT_ACTIONS.md`。
- 不破坏 Round 00 与 Web UI 的现有最小闭环。
- 不缓存具体考题、考点条目或院校招生数据；涉及考试 / 考纲 / 院校信息时必须使用最新官方来源，无法核验则停止。
- `.env`、密钥、token、私钥和认证信息不得写入仓库或命令输出。
- 本文件本身不授权 merge、push、deploy、发布、真实远程 VPS 写操作、数据库迁移、删除用户数据或修改 remote / 认证；这些操作需要当前任务的明确授权并遵守更高层规则。
- 若发现与本轮无关或归属不明的未提交修改，不得覆盖；出现路径边界不清、保护数据风险或冲突修改时停止。
- 需要引入大型依赖、数据库、前端框架、账号系统、云同步、后端架构变化，或需要修改 GitHub remote / 认证时停止并请求用户决定。
- 验证连续失败、push 失败或出现 merge conflict 时停止并报告，不得通过削弱测试或验收条件绕过失败。
- 不把未来规划写成当前已完成功能，不把静态配置存在写成运行时能力可用。

来源：`docs/CODEX_LONG_TERM_PLAN.md`、`docs/PROJECT_STATE.md`、`docs/governance/**`、`.gitignore`、项目级治理约束。

# AGENTS.md · 项目级事实与执行契约

本文件适用于仓库根目录及全部子目录。只记录可由当前仓库代码、配置和现行文档核对的事实。

仓库根目录：

- `~/PycharmProjects/computer_study_plan`
- `/Users/alalapi/PycharmProjects/computer_study_plan`

开始工作前必须读取：

1. `docs/WORKSPACE.md`
2. `docs/PRODUCT_VISION.md`
3. `docs/ROADMAP.md`
4. `docs/MASTER_STUDY_ROADMAP.md`
5. `docs/STAGE_PLAN.md`
6. `docs/CODEX_LONG_TERM_PLAN.md`
7. `docs/PROJECT_STATE.md`
8. `docs/NEXT_ACTIONS.md`

## 1. 项目目标

当前阶段是 **Linux 单课程验证**：

- 唯一正式课程：`linux-foundations`（Linux 基础与工程实践）
- 用这一门课验证：持续学习、任务记录、动作反馈、掌握度/通关感、网页体验
- 平台可保留 course-agnostic 结构，但本阶段不新增第二门课程

长期方向见 `docs/PRODUCT_VISION.md` 与 `docs/ROADMAP.md`。

## 2. 技术栈

- 浏览器端：静态 HTML/CSS、原生 JavaScript（`progress.html`、`progress_ui.js`）
- 本地服务：Python 3（`scripts/progress_server.py`）
- CLI：Bash（`mark_done.sh`）
- 数据：JSON / JSONL / Markdown
- Node.js / npm：仅用于既有检查与脚本入口；`package.json` 无 dependencies

## 3. 启动命令

```bash
python3 scripts/progress_server.py
# 或
npm run serve
```

默认页面：`http://127.0.0.1:8777/progress.html`

CLI：

```bash
bash mark_done.sh
bash mark_done.sh --lane linux-foundations
bash mark_done.sh <task-id>
bash mark_done.sh <task-id> --undo
```

## 4. 标准验证

```bash
python3 scripts/agent_gate.py --verify
```

顺序覆盖：`git diff --check`、`node --check progress_ui.js`、协议检查、学习数据校验、`progress.json`、`mark_done.sh --limit 5`。

涉及生成数据时追加：

```bash
npm run build:rounds
npm run sync:progress
python3 scripts/generate_task_feedback.py
```

UI 变更必须做真实浏览器 before/after，并检查 console / network。

## 5. 关键路径

| 路径 | 用途 |
|---|---|
| `content/courses/linux-foundations/` | 唯一正式课程注册 |
| `rounds/round_00|01|02|06/` | Linux 练习兼容真源 |
| `rounds/stage_03_vps_remote_ops/` | 远程 Linux 支线 |
| `plans/linux/` | 课程路径说明 |
| `progress.json` | 进度单一事实源 |
| `docs/CONTENT_AUDIT.md` / `docs/REMOVAL_MANIFEST.md` | 单课程化审计与删除清单 |

## 6. 保护与边界

- 不得破坏 Round 00 与 Web UI 最小闭环
- 不得把非 Linux 正式课程重新加回当前范围
- 自动生成文件只能通过生成器更新
- 不缓存考题 / 院校招生数据
- 真实远程 VPS 写操作需要明确授权
- 密钥不得写入仓库

## 7. Definition of Done

1. diff 只在当前任务允许路径内
2. 事实可追溯；未知标记「待验证」
3. 生成关系保持一致
4. `python3 scripts/agent_gate.py --verify` 通过
5. UI 变更有真实浏览器证据
6. 未泄露密钥，未破坏保护闭环
7. 独立 Judge 对精确候选给出 `PASS`

## 8. MCP

项目 `.cursor/mcp.json` 仅声明 `filesystem`；Cursor Home 提供 chrome-devtools、context7、github、playwright、stitch。

```bash
npm run check:mcp
```

配置通过 ≠ 当前线程工具可用。UI 浏览器任务缺少工具时报告：`BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY`。

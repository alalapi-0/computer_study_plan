<!-- 当前项目入口：保留业务、权限与验证约束；固定三角色执行链已退役。 -->

# AGENTS.md · 项目级事实与执行契约

本文件适用于仓库根目录及全部子目录。只记录可由当前仓库代码、配置和现行文档核对的事实。

仓库根目录：

- `~/Projects/computer-study-plan`
- `/home/alalapi/Projects/computer-study-plan`

按本次目标读取下列资料中相关的业务状态、范围、保护条件与验收要求；不再整套强制加载。ROADMAP、STAGE_PLAN、NEXT_ACTIONS、PROJECT_STATE 中的旧角色派发和审批条款不是当前执行指令入口；真实质量门、浏览器验证、保护文件及用户接受要求继续有效：

1. `docs/WORKSPACE.md`
2. `docs/PRODUCT_VISION.md`
3. `docs/ROADMAP.md`
4. `docs/MASTER_STUDY_ROADMAP.md`
5. `docs/STAGE_PLAN.md`
6. `docs/CODEX_LONG_TERM_PLAN.md`
7. `docs/PROJECT_STATE.md`
8. `docs/NEXT_ACTIONS.md`

## 1. 项目目标

当前阶段是 **Linux 首版问题驱动实操工作台**（2026-10-13用户请求）：

- 主单位：版本化Scenario / Environment / Attempt，不是课程章节
- 首批小问题跨文件、代码、数据、API子集与媒体产物；用户亲自执行
- `linux-foundations`、80任务、Round00与旧记录保留为历史兼容；不新增其他正式课程
- 提示常开/常关跨刷新持久，完整解答独立入口；检查目标与保护约束
- 任意Shell只能在已验证隔离环境；旧终端allowlist不得放宽；环境缺失拒绝回退
- 原生Windows/macOS、VM/systemd、双节点、真实前端/后台任务/AI能力如实标待实现

长期方向见 `docs/PRODUCT_VISION.md` 与 `docs/ROADMAP.md`。

## 2. 技术栈

- 浏览器端：静态 HTML/CSS、原生 JavaScript（`index.html`、`practice_ui.js`；历史`progress.html`、`progress_ui.js`）
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

默认页面：`http://127.0.0.1:8777/`；历史课程：`/progress.html`

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

顺序覆盖：`git diff --check`、`node --check practice_ui.js`、题包静态门禁、`node --check progress_ui.js`、协议检查、学习数据校验、`progress.json`、`mark_done.sh --limit 5`。

新问题/终端变更追加 `python3 scripts/validate_scenarios.py --runtime`、`python3 -m unittest tests.test_lab_runtime tests.test_scenarios tests.test_workbench_http`。保留进度事务测试。

涉及生成数据时追加：

```bash
npm run build:rounds
npm run sync:progress
python3 scripts/generate_task_feedback.py
```

UI 变更必须做真实浏览器 before/after，并检查 console / network。

Linux UI 回归继续使用 `scripts/external-ui-python` 的固定动作：`--bootstrap`、`--check`、`--ui-test`、`--self-test`。独立 Python3.12 环境与官方 Playwright1.60/Chromium1223 位于 `/home/alalapi/Runtimes/computer-study-plan`；路径、UUID、来源和完整树守卫拒绝回退，仓内不创建 `.venv-ui`。`npm run test:ui` 自动隔离网络、系统IPC和正式数据，只使用现有内存夹具；报告与截图在 `/home/alalapi/Artifacts/computer-study-plan/linux-ui`。历史Mac入口原样保存在 `scripts/external-ui-python-macos`；本机技术回归不代表Phase6或产品整体验收。

## 5. 关键路径

| 路径 | 用途 |
|---|---|
| `content/scenarios/` | 版本化问题真源与发布门禁 |
| `.lab-runtime/` | Git ignored新Attempt与一次性环境；不随旧存档恢复 |
| `content/courses/linux-foundations/` | 历史课程注册 |
| `rounds/round_00|01|02|06/` | Linux 练习兼容真源 |
| `rounds/stage_03_vps_remote_ops/` | 远程 Linux 支线 |
| `plans/linux/` | 课程路径说明 |
| `progress.json` | 历史课程进度单一事实源，旧done不迁成独立解决 |
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
7. 主代理核对实际候选与上述验收证据，明确未验证项；不要求固定角色审批

## 8. MCP

项目 `.cursor/mcp.json` 仅声明 `filesystem`；Cursor Home 提供 chrome-devtools、context7、github、playwright、stitch。

```bash
npm run check:mcp
```

配置通过 ≠ 当前线程工具可用。UI 浏览器任务缺少工具时报告：`BLOCKED: MISSING_FROM_THREAD_TOOL_REGISTRY`。

## PCH 生命周期与公开材料

工作前按本机共享 `~/.agents/pch-project-contract.md` 使用 `pch-project begin --project-id computer-study-plan`；收尾先更新原唯一状态，再带新请求 ID、来源 SHA、context 与原账本 CAS 调用 finish，核对持久终态。登记与状态读取不启动业务 Goal。

原作者工作区的 `docs/PROJECT_STATE.md` 含私人学习过程，仍为原唯一状态；Git 中该文件是经脱敏的公开冻结说明，不是实时状态副本。真实学习日志、原状态及本地恢复历史留在原工作区，不上传其私有提交祖先；克隆不得自行初始化另一套业务状态或恢复旧目标。

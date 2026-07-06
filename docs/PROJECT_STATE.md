# Project State

> 更新日期：2026-07-06
> 本文件只记录当前事实。2026-04/05 的旧状态日志已从正文移除，必要时从 git history 追溯。

## 1. 当前定位

`computer_study_plan` 是本地优先的长期学习总控仓库，服务于：

- 软考中级软件设计师高分 / 满分导向。
- 数学二、408 兼容基础、0854 跨专业考研准备。
- Linux / Shell / Git / Python / Web/API / 数据与 AI 工程实操。

唯一工作副本：

- `~/PycharmProjects/computer_study_plan`
- `/Users/alalapi/PycharmProjects/computer_study_plan`

练习沙盒默认在 `~/cli-lab/roundN`，不进入 Git。

## 2. 当前可运行入口

- Web UI：`progress.html`
- 本地服务：`python3 scripts/progress_server.py`
- 默认地址：`http://127.0.0.1:8777/progress.html`
- CLI：`bash mark_done.sh`
- 数据源：`progress.json`
- 前端镜像：`progress_data.js`、`rounds_data.js`

推荐启动：

```bash
cd ~/PycharmProjects/computer_study_plan
python3 scripts/progress_server.py
open http://127.0.0.1:8777/progress.html
```

## 3. 当前实现事实

- `rounds/round_00` 至 `rounds/round_21` 均已展开为可读 notes、可运行练习脚本和最终验收材料。
- Web UI 已注册 28 个分组、304 个任务，其中 101 个 exercise 任务可通过本地 API 运行。
- 计划入口已接入 Web UI：学习计划总览、软考、数学二、408、Linux、VPS 支线。
- Web UI 已支持：
  - 当前任务聚焦。
  - 内联教程阅读。
  - 浏览器映射终端。
  - 白名单练习脚本运行。
  - 记录 / 完成 / 撤销。
  - 动作日志与任务反馈。
  - 存档与读档。
- 当前仍使用 JSON / JSONL 文件，不使用数据库、账号系统或云同步。

## 4. 保护边界

默认保护：

- `progress.json`
- `progress_data.js`
- `rounds_data.js`
- `progress.html`
- `progress_ui.js`
- `mark_done.sh`
- `rounds/round_00/`
- `round_00.md` 至 `round_21.md`

当前用户已说明 `records/` 下不存在需要保护的真实学习记录；后续若出现真实记录，需要重新标注保护范围。

## 5. 当前问题

- Web UI 仍需要持续以用户视角检查信息密度、教程/终端联动和移动端可用性。
- 软考 / 数学二 / 408 仍主要是计划入口，不含具体题库或官方考纲缓存。
- VPS 支线只提供阅读与授权前准备，不默认执行真实远程操作。
- Cursor MCP CLI 层可能显示 `needs approval`；当前 Codex 线程可用工具和 Cursor 工具注册状态不完全一致。

## 6. 当前协作规则

- 默认直接在 `main` 上完成、验证、commit、push。
- 独立分支和 PR 仅在用户要求审查、实验性大改或 main 推送失败时使用。
- 每轮仍必须运行验证并更新 `docs/PROJECT_STATE.md` 与 `docs/NEXT_ACTIONS.md`。
- 不缓存具体考题、考点条目、院校招生数据；涉及考试信息必须使用最新官方源。

## 7. 2026-07-06 TASK-RR-56 治理规则与旧路线压缩

状态：done

本轮完成：

- 将仓库规则从“禁止直接 push main / 默认独立分支”改为“默认直接 push main”。
- 删除正文中的早期 Phase 0-7 和 TASK-002 至 TASK-012 长篇旧路线，保留当前路线入口。
- 压缩 `PROJECT_STATE` 和 `NEXT_ACTIONS`，避免新 Agent 被历史日志误导。
- 修正 `agent_gate` 输出，使后续自动推进提示 `branch_hint: "main"`，并正确显示任务标题。

风险边界：

- 不删除 Round 00-21 学习内容。
- 不删除进度系统核心文件。
- 不写入未经官方核验的考试或院校信息。

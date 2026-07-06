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

## 8. 2026-07-06 TASK-RR-57 第三轮项目用户视角评测与入口清理

状态：done

本轮评测报告：

- `docs/reports/PROJECT_USER_REVIEW_2026_07_06_ROUND3.md`

本轮发现并修复：

- README 把 MCP / Cursor 工具配置放在学习入口之前，已新增“快速开始”，并把工具配置标注为普通学习可跳过。
- README 对仓库定位、当前目标版本、Round 12–21 展开状态和 Round 数量的描述过期，已同步为当前 Web UI 学习系统事实。
- `docs/STAGE_PLAN.md` Stage 0 / Stage 1 仍像仓库建设未完成，已改为区分“仓库材料已展开”和“用户学习完成状态”。
- Web UI 当前阅读任务缺少“终端练习”入口，已允许 engineering reading 任务绑定浏览器终端。
- 390px 移动端顶部 chrome 推迟学习工作区，已隐藏移动端 `今日学习` 顶栏并压缩侧栏 / 工作区标题区域。

验证摘要：

- 桌面 `progress.html?round=round_02` 当前任务显示 `读教程 / 终端练习 / 记录 / 完成`。
- 点击当前阅读任务的 `终端练习` 后，终端工作目录绑定为 `~/round2`，内联教程仍为 `rounds/round_02/week1/notes.md`。
- 390px 移动端无横向溢出，学习工作区从约 474px 提前到约 265px 开始，内联教程进入首屏。

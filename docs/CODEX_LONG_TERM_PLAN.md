# Codex Long Term Plan

> 更新日期：2026-07-06
> 本文件是给 Codex / Cursor / 编程 AI 的长期协作入口。早期“网页交互式学习系统 Phase 0-7”规划已归档到 git history，不再作为当前推进依据。

## 1. 当前总目标

本仓库的长期目标是维护一个本地优先的计算机学习总控系统：

- 短期主线：软考中级，默认软件设计师，高分 / 满分导向。
- 中长期主线：数学二、408 兼容基础、0854 跨专业考研准备。
- 工程实操线：Linux、Shell、Git、Python、Web/API、数据与 AI 工程练习。
- Web UI：服务于阅读、练习、终端联动、记录、存档和复盘，不再把“做复杂平台”作为最高目标。

路线与阶段以这些文件为准：

- `docs/MASTER_STUDY_ROADMAP.md`
- `docs/STAGE_PLAN.md`
- `docs/PROJECT_STATE.md`
- `docs/NEXT_ACTIONS.md`

## 2. 当前产品边界

保留并维护：

- `progress.html` + `progress_ui.js` 学习工作区。
- `scripts/progress_server.py` 本地 API。
- `progress.json` / `progress_data.js` / `rounds_data.js` 数据文件。
- `mark_done.sh` CLI 兼容能力。
- `rounds/round_00` 至 `rounds/round_21` 工程实操任务。
- `plans/` 下软考、数学二、408、Linux 计划入口。

默认不做：

- 不缓存具体考题、考点条目、院校招生数据。
- 不引入数据库、前端框架、账号系统或云同步。
- 不把真实远程 VPS 操作伪装成自动可执行任务。
- 不为了历史规划继续扩展已经不适合当前路线的 Phase/TASK 文档。

## 3. 自动推进规则

每轮工作按以下顺序执行：

1. 读取 `AGENTS.md`、`docs/WORKSPACE.md`、`docs/MASTER_STUDY_ROADMAP.md`、`docs/STAGE_PLAN.md`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`。
2. 确认工作区状态，避免覆盖用户未说明的并行修改。
3. 从 `docs/NEXT_ACTIONS.md` 选择当前最高优先级任务；用户当轮直接指定任务时，以用户指令优先。
4. 默认在 `main` 上直接修改、验证、commit、push。
5. 只有用户要求审查、实验性大改或 push main 失败时，才使用独立分支和 PR。
6. 每轮完成后更新 `docs/PROJECT_STATE.md` 与 `docs/NEXT_ACTIONS.md`。

## 4. 验证基线

默认验证命令：

```bash
git diff --check
node --check progress_ui.js
python3 scripts/check_protocol_sync.py
python3 scripts/validate_learning_data.py
python3 -m json.tool progress.json
bash mark_done.sh
```

UI 修改还必须启动本地服务并做真实浏览器检查。

## 5. 停止条件

遇到以下情况停止并报告：

- 工作区有用户未说明且与本轮冲突的修改。
- 需要写入考试、考纲、院校信息但无法核验最新官方源。
- 需要修改 GitHub remote 或认证。
- 需要引入大型依赖、数据库、前端框架或后端架构变化。
- 需要执行真实远程 VPS 写操作但未取得用户明确授权。
- 验证连续失败、push 失败或出现 merge conflict。

## 6. 历史归档说明

2026-05-05 至 2026-05-12 的旧 Phase 0-7、TASK-002 至 TASK-012、task registry 原型等内容已被 2026-05-12 路线重定向取代。需要追溯时查看 git history，不再在当前工作文档中保留长篇旧路线。

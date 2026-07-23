# Codex Long Term Plan

> 更新日期：2026-07-18
> 本文件是给 Codex / Cursor / 编程 AI 的长期协作入口。

## 1. 当前总目标

把仓库收敛并打磨成：

**以 `linux-foundations` 为唯一正式课程、以游戏化强反馈学习体验为长期方向的单课程产品原型。**

当前不推进软考、考研、数学二、408，或其他独立工程/AI 课程。

权威文档：

- `docs/PRODUCT_VISION.md`
- `docs/ROADMAP.md`
- `docs/ARCHITECTURE.md`
- `docs/PROJECT_STATE.md`
- `docs/NEXT_ACTIONS.md`
- `docs/CONTENT_AUDIT.md`

## 2. 当前产品边界

保留并维护：

- `progress.html` + `progress_ui.js` 学习工作区
- `scripts/progress_server.py` 本地 API
- `progress.json` / `progress_data.js` / `rounds_data.js`
- `records/action_logs/` 与 `records/feedback/`
- `mark_done.sh`
- Linux 课程内容：Round 00 / 01 / 02 / 06、VPS 支线、`plans/linux/`、`content/courses/linux-foundations/`

默认不做：

- 不新增第二门正式课程
- 不实现完整 XP / 成就 / 反馈引擎（按 ROADMAP 后续 Phase）
- 不引入数据库、账号系统、云同步、前端框架
- 不把真实远程 VPS 写操作伪装成自动可执行任务
- 本轮不做 UI 视觉重设计

## 3. 自动推进规则

1. 读取 `AGENTS.md`、`docs/PRODUCT_VISION.md`、`docs/ROADMAP.md`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`。
2. 确认工作区状态，避免覆盖用户未说明的并行修改。
3. 用户当轮直接指定任务时，以用户指令优先；否则取 `NEXT_ACTIONS` 最高优先级。
4. 大范围重构使用独立分支；日常小修复可在当前协作约定下推进。
5. 每轮完成后更新 `docs/PROJECT_STATE.md` 与 `docs/NEXT_ACTIONS.md`。
6. 涉及删除课程内容时，先更新审计/删除清单，且不得删除 `REVIEW_REQUIRED` 项。

## 4. 验证基线

```bash
python3 scripts/agent_gate.py --verify
```

涉及课程数据时追加：

```bash
npm run build:rounds
npm run sync:progress
python3 scripts/generate_task_feedback.py
```

UI 修改还必须启动本地服务并做真实浏览器检查。

## 5. 停止条件

- 工作区有用户未说明且与本轮冲突的修改
- 出现无法裁定的 `REVIEW_REQUIRED` 删除项
- 需要引入大型依赖、数据库、前端框架或后端架构变化
- 需要执行真实远程 VPS 写操作但未取得明确授权
- 验证连续失败、push 失败或 merge conflict

## 6. 路线索引

详见 `docs/ROADMAP.md` Phase 0–10。当前主线是单课程垂直验证，不是多课程铺开。

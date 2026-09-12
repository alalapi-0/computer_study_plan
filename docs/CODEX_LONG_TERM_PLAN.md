# Codex Long Term Plan

> 更新日期：2026-08-14
> 本文件是给 Codex / Cursor / 编程 AI 的长期协作入口。

## 1. 当前总目标

当前把仓库收敛并打磨成：

**以 `linux-foundations` 为唯一正式课程、以游戏化强反馈学习体验为长期方向的单课程产品原型。**

长期目标是本地优先的通用学习平台，并可在闭环成熟后评估自然语言学习编排；当前不推进软考、考研、数学二、408，或其他独立工程/AI 课程。

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
- `progress_ui.css` 视觉、响应式与动效系统
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
- 不展示未由真实数据支持的 XP、Mastery、成就或复习记录
- 不因视觉重构改变既有任务、进度、终端和存档协议

当前 UI 已实现“今日、学习、路线、复习、手册、成长”六个视图和独立模块检查点，但 2026-08-11 版本只是校准基线。Figma 文件当前可读取到 10 个 Desktop 屏、10 个 Mobile/Mini Program 屏、3 组核心组件和 6 个 Motion/Codex Handoff 页面；六个双端屏幕切片、跨屏任务身份，以及减少动效、直接操控、原子视图切换、终端控件状态和 H04 Home → Learn 共享任务关系现已验证。Home 全局当前项与 Learn 显式任务由不同状态语义承载，注册任务可经 URL / history 恢复；390–920px 的移动入口、聚焦面板与触控约定已统一，并有首个只读 Playwright 回归入口。它们仍不代表 Phase 6 或 Phase 8 整体完成；后续每轮须按真实运行状态重新选择最高价值差距，继续收敛 Components / Motion、局部反馈、跨屏连续性、可重复回归证据与遗留实现，直到整套产品验收。Figma 示例 XP、课程术语或数据文件名不能覆盖仓库事实，未实现的奖励不得展示成真实状态。

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

已安装独立 UI 依赖时，当前最小回归入口为：

```bash
npm run test:ui
```

安装与 fixture 边界见 `tests/ui/README.md`：默认严格只读，完成/撤销测试仅在显式 opt-in 的纯内存模式运行；生产后端事务另在临时仓库测试。它们都不替代真实浏览器视觉检查。

## 5. 停止条件

- 工作区有用户未说明且与本轮冲突的修改
- 出现无法裁定的 `REVIEW_REQUIRED` 删除项
- 需要引入大型依赖、数据库、前端框架或后端架构变化
- 需要执行真实远程 VPS 写操作但未取得明确授权
- 验证连续失败、push 失败或 merge conflict

## 6. 路线索引

详见 `docs/ROADMAP.md` Phase 0–11。当前主线是单课程垂直验证，不是多课程铺开；自然语言入口和第二门课程均是有前置条件的长期评估项。

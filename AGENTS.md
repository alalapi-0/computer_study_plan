# Codex Repository Instructions

本仓库自 2026-05-12 起的总目标是：以**软考中级（默认软件设计师，高分/满分导向）**为短期主线，承接**数学二 / 408 / 0854 跨专业考研**作为中长期主线，同时保留 Linux / Shell / Git / Python / AI 工程实操作为"工程实操线"。

详细路线见 `docs/MASTER_STUDY_ROADMAP.md`。

## 每次工作前必须读取

1. `docs/MASTER_STUDY_ROADMAP.md`（总目标与四主线）
2. `docs/STAGE_PLAN.md`（Stage 0–7 阶段计划）
3. `docs/CODEX_LONG_TERM_PLAN.md`（长期协作规则，含 2026-05-12 重定向说明）
4. `docs/PROJECT_STATE.md`（仓库当前状态）
5. `docs/NEXT_ACTIONS.md`（下一步任务队列）

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

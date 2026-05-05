# Codex Repository Instructions

本仓库的长期目标是把 `computer_study_plan` 从计算机基础学习大纲仓库，逐步推进为本地优先、可版本管理、可网页化部署的交互式学习系统。

## 每次工作前必须读取

1. `docs/CODEX_LONG_TERM_PLAN.md`
2. `docs/PROJECT_STATE.md`
3. `docs/NEXT_ACTIONS.md`

## 工作原则

- 每轮只做一个明确任务，优先选择 `docs/NEXT_ACTIONS.md` 中最高优先级且不需要用户介入的任务。
- 不破坏 Round 00 已有可运行能力，尤其是 `rounds/round_00/`、`progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh` 的最小闭环。
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
- 需要引入大型新依赖。
- 需要从 JSON 切换到数据库。
- 需要从静态页面切换到前端框架。
- 需要创建后端服务。
- 需要修改 GitHub remote 或认证。
- push 失败、merge conflict、验证连续失败，或任务边界不清。

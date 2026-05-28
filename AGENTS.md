# Codex Repository Instructions

本仓库自 2026-05-12 起的总目标是：以**软考中级（默认软件设计师，高分/满分导向）**为短期主线，承接**数学二 / 408 / 0854 跨专业考研**作为中长期主线，同时保留 Linux / Shell / Git / Python / AI 工程实操作为"工程实操线"。

详细路线见 `docs/MASTER_STUDY_ROADMAP.md`。

## 本地工作副本（固定）

- **唯一 Git 仓库根**：`~/PycharmProjects/computer_study_plan`（本机绝对路径 `/Users/alalapi/PycharmProjects/computer_study_plan`）
- Cursor / PyCharm **工作区必须打开该目录**；文档与脚本中的「仓库根」均指此处
- Round 00 终端练习沙盒为 `~/cli-lab/round0`（不进 Git，与仓库根不同）
- 完整约定见 `docs/WORKSPACE.md`；不要在文档中再写 `Desktop/computer_study_plan` 为默认路径

## 每次工作前必须读取

1. `governance/repo_protocol_standard.yaml`（通用治理协议，最高机器规则）
2. `project.yaml`（本仓库身份卡 + 协议版本绑定）
3. `governance/agent_policy.yaml`、`governance/round_state.yaml`、`governance/file_role_map.yaml`（执行边界与本轮状态）
4. `docs/WORKSPACE.md`（路径与工作区，避免改错目录）
5. `docs/MASTER_STUDY_ROADMAP.md`（总目标与四主线）
6. `docs/STAGE_PLAN.md`（Stage 0–7 阶段计划）
7. `docs/CODEX_LONG_TERM_PLAN.md`（长期协作规则，含 2026-05-12 重定向说明）
8. `docs/PROJECT_STATE.md`（仓库当前状态）
9. `docs/NEXT_ACTIONS.md`（下一步任务队列）

> 历史规划（"网页交互式学习系统"Phase 0–7）仍保留作为工程实操线的演进参考，但**不再是最高优先级**。

## 工作原则

- 每轮只做一个明确任务，优先选择 `docs/NEXT_ACTIONS.md` 中最高优先级且不需要用户介入的任务。
- 不破坏 Round 00 已有可运行能力，尤其是 `rounds/round_00/`、`progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh` 的最小闭环。
- 不破坏 `records/` 下任何已写入的用户真实学习记录。
- 不缓存具体考题、考点条目、院校招生数据；涉及考试内容一律以**最新官方信息**为准。
- 不把未来规划写成已完成事实。
- 不一次性大范围重构无关内容。
- 不直接 push `main`。
- 每轮完成后必须运行验证并更新文档；仅在用户明确要求时执行 commit/push。

## 协议同步机制（新增）

- 触发条件：治理规则、阶段结构、关键目录、读取顺序、验证命令发生变化。
- 同步清单：`docs/checklists/protocol_sync_checklist.md`。
- 自动检查：`python3 scripts/check_protocol_sync.py`。
- 同步目标至少包括：`governance/*.yaml`、`project.yaml`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`、`docs/reports/`。

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

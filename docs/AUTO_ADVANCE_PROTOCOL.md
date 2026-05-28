# Auto Advance Protocol

本文档定义 Codex 后续收到“根据长期规划继续推进下一轮”等短指令时的自动推进流程。长期目标以 `docs/CODEX_LONG_TERM_PLAN.md` 为准。

## 1. 自动推进前置条件

开始任何一轮前，Codex 必须确认：

- 已读取 `AGENTS.md`
- 已读取 `governance/repo_protocol_standard.yaml` 与 `project.yaml`
- 已读取 `governance/agent_policy.yaml`、`governance/round_state.yaml`、`governance/file_role_map.yaml`
- 已读取 `docs/CODEX_LONG_TERM_PLAN.md`
- 已读取 `docs/PROJECT_STATE.md`
- 已读取 `docs/NEXT_ACTIONS.md`
- 当前 git 工作区没有用户未提交修改
- 当前任务边界清楚，且只对应一个 `TASK-XXX`
- 该任务不要求删除或不可逆迁移已有学习记录
- 该任务不需要引入大型依赖、数据库、前端框架或后端服务，除非用户已经明确批准

如果前置条件不满足，停止并向用户报告。

## 2. 单轮执行流程

每轮只执行一个明确任务：

1. 从 `docs/NEXT_ACTIONS.md` 选择优先级最高、状态为 `pending`、且不需要用户介入的任务。
2. 创建或切换到独立分支，默认分支名：`codex/<task-id>-short-title`。
3. 将该任务在 `docs/NEXT_ACTIONS.md` 中标记为 `in_progress`。
4. 阅读任务涉及的现有文件，确认真实状态。
5. 做最小必要修改。
6. 运行验证。
7. 将该任务标记为 `done`，并更新后续任务状态。
8. 更新 `docs/PROJECT_STATE.md`。
9. 必要时更新 `docs/DECISIONS.md`、`README.md`、`AGENTS.md` 或长期规划文档。
10. 同步机器协议与文档（含 `docs/reports/` 治理报告）。
11. 仅在用户明确要求时 commit。
12. 仅在用户明确要求且 remote 可用时 push / 创建或更新 PR。

## 3. 验证流程

每轮至少运行：

```bash
git status
git diff --check
```

如果新增或修改 JSON 文件，必须运行：

```bash
python3 -m json.tool <file>
```

如果修改了 `mark_done.sh`、`progress.json`、`progress_data.js` 或进度系统行为，至少运行：

```bash
bash mark_done.sh
```

如果新增脚本或测试工具，应运行对应最小验证命令，并在最终汇报中说明结果。

## 4. Commit 规则（按需）

- 默认不自动 commit，只有用户明确要求时才能 commit。
- 若执行 commit，必须先通过验证，且每次 commit 只对应一个任务。
- commit message 使用格式：

```text
TASK-XXX: short imperative summary
```

- 不把无关格式化、无关重构和任务实现混在同一个 commit。
- 不提交临时文件、缓存文件、运行产物或编辑器私有文件。

## 5. Push 规则（按需）

- 不直接 push `main`。
- 默认不自动 push，只有用户明确要求时才 push 当前独立分支。
- push 失败时停止并报告，不继续做下一轮。
- 不修改 GitHub remote 或认证配置，除非用户明确要求。

## 6. PR 规则

如果 GitHub CLI 可用并已登录：

- 可以为本轮分支创建 PR。
- PR 标题应包含 `TASK-XXX` 和任务摘要。
- PR 描述应说明本轮做了什么、验证了什么、没有做什么。

如果 GitHub CLI 不可用、未登录或 remote 不可访问：

- 不强行创建 PR。
- 在最终汇报中说明原因。

## 7. 停止条件

遇到以下情况必须停止：

- git 工作区有用户未提交修改
- 任务边界不清
- 真实仓库状态与 `docs/PROJECT_STATE.md` 严重不一致
- 需要删除或迁移已有学习记录但无法保证安全
- 需要引入大型新依赖
- 需要从 JSON 切换到数据库
- 需要从静态页面切换到前端框架
- 需要创建后端服务
- 需要修改 GitHub remote 或认证
- push 失败
- merge conflict
- 测试连续两次修复仍失败
- 需要用户确认产品方向

## 8. 最终汇报格式

每轮完成后，最终回复应包含：

```text
## 本轮完成

## 新增/修改文件

## 关键长期目标

## 验证结果

## Git 状态

## 下一轮建议
```

汇报必须说明当前分支、commit hash、push 是否成功，以及 PR 链接是否已创建。

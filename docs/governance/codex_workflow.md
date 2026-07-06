# Codex / Cursor / AI 协作工作流

> 本文件总结编程 AI 在本仓库工作时的标准动作流程。
> 长期目标：未来同样的流程可适用于 `VULTRagent` 这种远程运维辅助工具。

## 1. 关系总览

```
AGENTS.md（强制规则）
   ↓
docs/CODEX_LONG_TERM_PLAN.md（长期目标）
docs/PROJECT_STATE.md（当前状态）
docs/NEXT_ACTIONS.md（下一步队列）
docs/DECISIONS.md（架构决策）
   ↓
docs/AUTO_ADVANCE_PROTOCOL.md（单轮自动推进流程）
docs/governance/repo_rules.md（仓库治理规则）
docs/governance/remote_operation_permissions.md（远程操作权限等级）
docs/governance/file_naming_rules.md（命名规则）
   ↓
单轮任务执行
   ↓
docs/checklists/*（验收检查）
docs/templates/*（高风险操作前的确认模板）
```

## 2. 每轮标准流程

1. 读取 `AGENTS.md` 和三份长期文档（`CODEX_LONG_TERM_PLAN.md`、`PROJECT_STATE.md`、`NEXT_ACTIONS.md`）。
2. 从 `docs/NEXT_ACTIONS.md` 选择优先级最高、状态 `pending`、不需要用户介入的任务。
3. 默认留在 `main` 直接推进；只有用户要求 PR 审查或高风险实验时才创建独立分支。
4. 在 `docs/NEXT_ACTIONS.md` 标记任务为 `in_progress`。
5. 执行**最小必要修改**。
6. 验证：
   - `git status`
   - `git diff --check`
   - 如改动 JSON：`python3 -m json.tool <file>`
   - 如改动进度系统：`bash mark_done.sh`
7. 在 `docs/NEXT_ACTIONS.md` 标记任务为 `done`。
8. 更新 `docs/PROJECT_STATE.md`。
9. 必要时更新 `docs/DECISIONS.md`、`README.md`、`AGENTS.md` 或长期规划文档。
10. commit（一个任务一个 commit）。
11. push 到 remote `main`。
12. 仅在本轮使用独立分支时，创建或更新 PR。

详细见 `docs/AUTO_ADVANCE_PROTOCOL.md`。

## 3. 远程服务器相关任务的额外流程

凡是涉及"在真实 VPS 上执行操作"的任务，必须在标准流程上额外做：

1. 判定本轮的"远程操作权限等级"（参见 `docs/governance/remote_operation_permissions.md`）。
2. 如果等级 ≥ Level 2，**先暂停**，使用 `docs/templates/remote_operation_confirmation.md` 向用户提交确认请求。
3. 等待用户明确授权后再执行。
4. 执行时严格使用占位符示例，避免在文档中留下真实 IP / Key / 私钥。
5. 执行后**留下操作记录**（命令、时间、结果、错误码、回滚方式）到本轮对应的输出物中。

## 4. 仓库治理类任务的额外流程

凡是涉及"删除文件 / 重命名文件 / 合并文档 / 重组目录"的任务，必须在标准流程上额外做：

1. 先扫描仓库，列出拟改文件清单。
2. 使用 `docs/templates/repository_cleanup_confirmation.md` 提交确认。
3. 仅在用户明确授权后才删除或重命名。
4. 删除前确认内容已迁移；保留必要跳转说明。
5. 在 commit message 与变更报告中记录全部变更范围。

## 5. 必须停止并向用户报告的情况

- git 工作区有用户未提交修改且与本轮无关。
- 任务边界不清。
- `docs/PROJECT_STATE.md` 与真实仓库严重不一致。
- 需要删除或迁移已有学习记录但无法保证安全。
- 需要执行 Level 2 及以上远程操作但未取得用户授权。
- 需要执行 Level 5 高风险操作。
- 需要引入大型新依赖、数据库、前端框架、后端服务。
- push 失败、merge conflict、连续两次验证失败。

## 6. 与 `VULTRagent` 的衔接

未来 `VULTRagent` 是独立项目仓库，但其工作流应直接复用本仓库定义的：

- 远程操作权限等级
- 远程操作确认模板
- VPS 安全 checklist
- 操作日志格式

`computer_study_plan` 提供"规则与 SOP"，`VULTRagent` 提供"自动化执行手段"，两者通过文档接口对齐。

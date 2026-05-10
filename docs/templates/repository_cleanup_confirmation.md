# Repository Cleanup Confirmation Template（仓库治理确认模板）

> 任何**删除文件 / 重命名文件 / 合并文档 / 重组目录**操作前，必须以本模板向用户提交确认。
> 与 `docs/checklists/repository_cleanup_checklist.md` 配合使用。

---

## 1. 本轮治理名称

<!-- 一句话说明，例如：Round VPS-01 执行仓库治理与文档合并 -->

## 2. 拟合并文件

| 来源文件 | 目标文件 | 合并策略 | 信息是否已迁移 |
|---|---|---|---|
| `path/to/old_a.md` | `path/to/new.md` | 段落合并 / 去重 / 整章替换 | [ ] 是 / [ ] 否 |
|  |  |  |  |

## 3. 拟删除文件

| 文件 | 类别 | 删除理由 | 内容是否已被吸收 |
|---|---|---|---|
| `path/to/file` | 重复 / 空 / 临时残留 / 命名混乱 / 与项目无关 | ______ | [ ] 是 / [ ] 否 / [ ] 不需要 |
|  |  |  |  |

> 高保护对象（**默认禁止删除**，必须用户单独逐项确认）：
>
> - `progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh`
> - `rounds/round_00/` 下所有文件
> - 任意 `round_XX.md` / `plan_round_XX.txt`
> - `AGENTS.md`、`README.md`、`CONVERSION_PROTOCOL.md`、`docs/CODEX_LONG_TERM_PLAN.md`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`、`docs/DECISIONS.md`、`docs/AUTO_ADVANCE_PROTOCOL.md`

## 4. 拟重命名文件

| 旧路径 | 新路径 | 是否影响外部引用 |
|---|---|---|
| `path/to/old.md` | `path/to/new.md` | [ ] 否 / [ ] 是（已同步引用） |
|  |  |  |

## 5. 删除理由汇总

<!-- 用自然语言一段话说明本轮治理的整体逻辑 -->

## 6. 内容是否已迁移说明

<!-- 对每个被删除 / 被合并的文件，明确说明其内容去向 -->

- `path/to/file` → 内容已迁移至 ______，未丢失。
- `path/to/file` → 内容确为重复，无残留信息可保留。
- `path/to/file` → 内容确为临时残留，不需保留。

## 7. 风险评估

- 是否影响 Round 00 闭环？[ ] 否 / [ ] 需用户确认
- 是否影响主线 Round 概览？[ ] 否 / [ ] 需用户确认
- 是否影响 `progress.json` 数据？[ ] 否 / [ ] 需用户确认
- 是否影响 README 入口？[ ] 否 / [ ] 已同步

## 8. 回滚方式

- 本轮在分支 `codex/<task-id>-short-title` 上执行。
- 如需回滚：`git reset --hard origin/main` 或在 PR 阶段直接关闭。
- 是否已 push 到远端？[ ] 否 / [ ] 是（仅推到独立分支，不影响 main）

## 9. 是否需要用户确认

- [ ] 是（默认必须）
- [ ] 否（仅当所有变更均为新增 / 在独立目录 / 无任何删除时）

## 10. 用户确认记录

- 确认时间：____-__-__ __:__
- 确认范围：[ ] 全部 / [ ] 部分（指明：______）
- 是否允许执行：[ ] 是 / [ ] 否
- 备注：______

## 11. 执行结果（执行完成后填写）

- 实际新增文件：______
- 实际修改文件：______
- 实际删除文件：______
- 实际重命名文件：______
- Round 00 验证：[ ] 通过（`bash mark_done.sh` 可正常运行）
- `progress.json` 校验：[ ] 通过（`python3 -m json.tool progress.json` 通过）
- commit hash：______
- push 状态：[ ] 已 push 到独立分支 / [ ] 未 push（原因：______）

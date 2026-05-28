# Repository Governance Rules（仓库治理规则）

> 本文件是 `computer_study_plan` 仓库的长期治理规则。
> 它不替代 `AGENTS.md`，但补充更细的"如何修改仓库"的边界。

## 1. 仓库定位

`computer_study_plan` 是**长期计算机学习总控仓库**，不是工具仓库、不是项目代码仓库、不是文档站。

它的真实承载内容：

- 长期学习路线（Round 00–21 工程/服务/AI 主线）
- VPS 实操训练支线（stage_03_vps_remote_ops 等）
- 学习进度数据（`progress.json`）与最小展示（`progress.html`）
- 用于 Codex / Cursor / 本地编程 AI 协作的总控文档

它**不承担**：

- 真实项目代码（应放到独立项目仓库）
- 真实 API Key、密码、SSH 私钥
- 真实服务器 IP、域名、token
- 部署生产服务

## 2. 修改仓库的总原则

> 先扫描 → 再判断 → 再提出整理方案 → 再修改仓库 → 再输出变更报告。

每次修改都必须满足：

1. 不破坏 Round 00 的最小可运行闭环：`progress.json` / `progress_data.js` / `progress.html` / `mark_done.sh` / `rounds/round_00/`。
2. 不一次性大范围重构无关内容。
3. 每轮聚焦一个明确任务（参见 `AGENTS.md` 与 `docs/AUTO_ADVANCE_PROTOCOL.md`）。
4. 不直接 push `main`，使用 `codex/<task-id>-short-title` 独立分支。
5. 不把"未来规划"写成"已完成事实"。

## 3. 文件分层（软分层）

仓库中的文件按用途软分为以下层，**不强制目录迁移**，但新增内容应按此层落位：

| 层 | 位置 | 用途 |
|---|---|---|
| 总入口 | `README.md` | 项目介绍、入口指引 |
| Codex/AI 协作规则 | `AGENTS.md`、`docs/AUTO_ADVANCE_PROTOCOL.md`、`docs/governance/codex_workflow.md` | 给 AI 看的工作规则 |
| 长期规划 | `docs/CODEX_LONG_TERM_PLAN.md`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`、`docs/DECISIONS.md` | 项目方向与状态 |
| 治理规则 | `docs/governance/` | 仓库自身的规则 |
| 学习模块总纲 | `docs/modules/` | 每个独立学习模块的主文档 |
| Checklist | `docs/checklists/` | 可勾选的检查清单 |
| 确认模板 | `docs/templates/` | 高风险操作前的确认模板 |
| Round 概览（主线） | `round_00.md` ~ `round_21.md` | 已建立的工程/服务/AI 主线轮次概览 |
| Round 实操（主线） | `rounds/round_XX/` | 主线轮次的可执行展开 |
| 学习计划专题 | `plans/<scope>/` | 软考 / 数学二 / 408 / Linux 等独立学习计划目录 |
| 学习记录 | `records/<scope>/` | 周复盘 / 错题 / 完成任务等用户真实学习记录 |
| Round 实操（支线） | `rounds/stage_*/round_*.md` | 阶段性支线（如 VPS 远程实操） |
| 进度系统 | `progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh` | 任务状态与展示 |
| IDE/系统副产物 | `.idea/`、`.DS_Store` | 不属本仓库内容范围，不主动改 |

> 主线 Round（`round_XX.md`）和阶段性支线 Round（`rounds/stage_*/round_vps_XX.md`）**不混用编号空间**，互相之间不会冲突。

## 4. 删除文件的硬约束

允许删除文件**仅当满足以下任一条件**：

1. 文件明显是重复内容；
2. 文件内容已经被完整合并进其他文档；
3. 文件是空文件；
4. 文件是临时测试残留；
5. 文件命名混乱且内容已经迁移；
6. 文件与当前学习总控完全无关。

删除前必须：

- 先在 PR / 变更报告中列出拟删除文件清单；
- 说明删除理由；
- 如果有内容残值，先确认已迁移；
- 如果是 Round 00 相关文件、`progress.json`、`mark_done.sh`、主线 Round md 文档或用户真实学习记录（`records/` 下已写入的内容），**默认禁止删除**，除非用户明确授权（参见 `docs/templates/repository_cleanup_confirmation.md`）。
- 已删除的对象（不再保护）：`plan_round_XX.txt`（22 份初版提示词文本，于 2026-05-12 经用户授权统一清理，内容已由 `round_XX.md` 完整吸收）。

## 5. 合并文件的硬约束

合并多个文档时必须：

- 保留有效内容，不丢信息；
- 删除重复段落；
- 保留更清晰的结构；
- 在原文件位置保留跳转说明（除非原文件被同时安全删除）；
- 在变更报告中说明合并范围与依据。

## 6. 新增文件的命名规则

详见 `docs/governance/file_naming_rules.md`。要点：

- 文件名小写、单词之间用下划线 `_`。
- 主线 Round 概览：`round_XX.md`，XX 为两位数字。
- 阶段性支线 Round：`round_<scope>_XX.md`，例如 `round_vps_05_first_readonly_check.md`。
- 模块总纲：`docs/modules/<module>.md`。
- 治理规则：`docs/governance/<topic>.md`。
- Checklist：`docs/checklists/<topic>_checklist.md`。
- 模板：`docs/templates/<topic>_template.md` 或 `<topic>.md`（如已是模板自带后缀）。

## 7. 安全边界（与 `docs/governance/remote_operation_permissions.md` 配合）

文档与示例中**绝对禁止**出现：

- 真实服务器 IP；
- 真实 API Key、token、密码；
- 真实 SSH 私钥内容；
- 真实用户名（如不可避免必须使用占位符）。

所有示例统一使用占位符：

- `your_server_ip`
- `your_user`
- `your_repo_url`
- `your_api_key_here`
- `example.com`

允许提交：

- `.env.example`

禁止提交：

- `.env`
- `id_rsa` / `id_ed25519` 等私钥
- 任何含有真实凭证的文件

## 8. Codex / Cursor / AI 协作的额外约束

- 只能在独立分支工作。
- 必须先读取 `AGENTS.md`、`docs/CODEX_LONG_TERM_PLAN.md`、`docs/PROJECT_STATE.md`、`docs/NEXT_ACTIONS.md`。
- 必须遵守 `docs/governance/remote_operation_permissions.md` 定义的权限等级。
- 任何 Level 2 及以上的远程操作，**必须先取得用户明确授权**，并使用 `docs/templates/remote_operation_confirmation.md` 走完确认流程。
- 任何高风险仓库治理（删除、迁移已有学习记录），必须使用 `docs/templates/repository_cleanup_confirmation.md` 走完确认流程。

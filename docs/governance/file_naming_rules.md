# File Naming Rules（文件命名规则）

> 命名规则的目的是让仓库**可被人和 AI 同时一眼识别用途**，避免误改、误删和误合并。

## 1. 通用规则

- 文件名一律使用小写。
- 单词之间用下划线 `_` 分隔，不使用空格、不使用连字符 `-`（除非业内约定）。
- 不使用中文文件名（中文允许出现在文档内容里）。
- 不在文件名里写日期，除非该文件就是按日期归档的运行记录。

## 2. 主线轮次（已存在体系，不改）

- 主线 Round 概览文档：`round_XX.md`，XX 为两位数字（已存在 `round_00.md` ~ `round_21.md`）。
- 主线 Round 实操目录：`rounds/round_XX/`（目前 `rounds/round_00/` 至 `rounds/round_21/` 均已展开）。
- 已废弃命名：`plan_round_XX.txt`（22 份初版提示词文本于 2026-05-12 由用户授权删除，内容已被对应 `round_XX.md` 完整吸收。后续**不再新增**此类文件，新需求直接写 md）。

> 这些命名是项目的"既成事实"，不主动重命名。新增主线 Round 仍延用相同格式。

## 3. 阶段性支线轮次（本次新增）

- 阶段目录：`rounds/stage_<NN>_<scope>/`，例如 `rounds/stage_03_vps_remote_ops/`。
- 支线 Round 文档：`round_<scope>_<XX>_<short_title>.md`，例如：
  - `round_vps_00_repo_scan.md`
  - `round_vps_05_first_readonly_check.md`
- 支线 Round 编号空间与主线**互不冲突**：主线用 `round_00` ~ `round_21`，支线用 `round_vps_00` ~ `round_vps_12` 等。

阶段编号建议（**当前仅作为命名参考，未真实迁移主线**）：

| 阶段编号 | 主题 | 当前是否存在目录 |
|---|---|---|
| stage_01_foundation | 终端 / Shell / Git 基础 | 否（主线 Round 00–02 已覆盖） |
| stage_02_linux_network | Linux 进阶与网络 | 否（主线 Round 06 部分覆盖） |
| stage_03_vps_remote_ops | VPS 远程实操训练 | 是（本次新增） |
| stage_04_project_deployment | 个人项目部署 | 否（未来扩展） |

## 4. docs 目录命名规则

- 模块总纲：`docs/modules/<module>.md`，例如 `docs/modules/vps_remote_ops.md`。
- 治理规则：`docs/governance/<topic>.md`。
- 检查清单：`docs/checklists/<topic>_checklist.md`。
- 操作模板：`docs/templates/<topic>_template.md` 或 `<topic>_confirmation.md`。
- 长期规划与状态：保留现有名字（`CODEX_LONG_TERM_PLAN.md`、`PROJECT_STATE.md`、`NEXT_ACTIONS.md`、`DECISIONS.md`、`AUTO_ADVANCE_PROTOCOL.md`），不重命名。

## 5. 进度系统命名规则（不改）

- `progress.json`：单一事实源，不允许改名。
- `progress_data.js`：自动生成，不手动编辑。
- `progress.html`：静态看板，命名固定。
- `mark_done.sh`：CLI 工具，命名固定。

## 6. 任务 ID 命名规则（与现有 Round 00 保持兼容）

- Round 00 现有：`w1-read`、`w1-ex1`、`fin-comp` 等保持不变。
- 主线 Round 任务 ID 已注册到 `progress.json` / `rounds_data.js`，继续沿用现有 `rNN-*` 规则。
- 支线 VPS 文档已作为阅读入口接入 Web UI；真实远程操作仍需用户授权后再记录。

## 7. 不允许的文件名模式

- 含真实服务器 IP 的文件名。
- 含 API Key 的文件名。
- 含日期且与归档无关的文件名（如 `notes_20260510.md`）。
- 全大写文件名（除少数公认惯例：`README.md`、`AGENTS.md`、`CONVERSION_PROTOCOL.md` 已存在不改）。
- 临时测试残留（如 `test.md`、`tmp.txt`、`untitled.md`）。

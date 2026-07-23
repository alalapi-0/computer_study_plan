# File Naming Rules（文件命名规则）

> 命名规则的目的是让仓库**可被人和 AI 同时一眼识别用途**，避免误改、误删和误合并。

## 1. 通用规则

- 文件名一律使用小写。
- 单词之间用下划线 `_` 分隔，不使用空格、不使用连字符 `-`（除非业内约定）。
- 不使用中文文件名（中文允许出现在文档内容里）。
- 不在文件名里写日期，除非该文件就是按日期归档的运行记录。

## 2. Linux 课程兼容 Round（当前正式范围）

- 课程注册：`content/courses/linux-foundations/`
- 兼容 Round 概览：`round_00.md`、`round_01.md`、`round_02.md`、`round_06.md`
- 兼容实操目录：`rounds/round_00/`、`rounds/round_01/`、`rounds/round_02/`、`rounds/round_06/`
- 已废弃：`plan_round_XX.txt`；非 Linux 正式 Round 03–05、07–21 已移出工作树（见 `docs/REMOVAL_MANIFEST.md`）

> Phase 0/1 仍保留 `round_XX` 命名以兼容现有 Web UI / 进度系统；新增 Linux 模块优先登记到 `course.json`。

## 3. 阶段性支线轮次

- 阶段目录：`rounds/stage_<NN>_<scope>/`，例如 `rounds/stage_03_vps_remote_ops/`。
- 支线 Round 文档：`round_<scope>_<XX>_<short_title>.md`
- 支线编号空间与主线互不冲突：当前正式主线 Round 为 `00/01/02/06`，支线为 `round_vps_00` ~ `round_vps_12`

| 阶段编号 | 主题 | 当前是否存在目录 |
|---|---|---|
| stage_03_vps_remote_ops | VPS 远程实操训练（linux-foundations Module 04） | 是 |

## 4. docs 目录命名规则

- 模块总纲：`docs/modules/<module>.md`，例如 `docs/modules/vps_remote_ops.md`。
- 治理规则：`docs/governance/<topic>.md`。
- 检查清单：`docs/checklists/<topic>_checklist.md`。
- 操作模板：`docs/templates/<topic>_template.md` 或 `<topic>_confirmation.md`。
- 长期规划与状态：保留现有名字（`CODEX_LONG_TERM_PLAN.md`、`PROJECT_STATE.md`、`NEXT_ACTIONS.md`、`DECISIONS.md`、`AUTO_ADVANCE_PROTOCOL.md`），不重命名。

## 5. 进度系统命名规则（不改）

- `progress.json`：单一事实源，不允许改名。
- `progress_data.js`：自动生成，不手动编辑。
- `rounds_data.js`：Round / 计划分组展示数据，自动生成，不手动编辑。
- `progress.html`：Web UI 学习工作区入口，命名固定。
- `progress_ui.js`：Web UI 交互逻辑，命名固定。
- `scripts/progress_server.py`：本地学习服务，命名固定。
- `mark_done.sh`：CLI 兼容工具，命名固定。

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

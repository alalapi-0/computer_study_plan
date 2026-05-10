# Next Actions

本文件是 Codex 后续自动推进的任务队列。每轮只允许选择一个任务推进，并在完成后同步更新本文件与 `docs/PROJECT_STATE.md`。

## TASK-001: 创建长期目标与 Codex 协议文档

- 状态：done
- 背景：仓库已有 Round 00-21 路线文档和 Round 00 最小可运行原型，但缺少 Codex 后续长期推进时必须读取的目标文档、协作规则和任务队列。
- 目标：建立长期目标、自动推进协议、任务队列、决策记录和项目状态同步规则。
- 要修改：`AGENTS.md`、`docs/CODEX_LONG_TERM_PLAN.md`、`docs/AUTO_ADVANCE_PROTOCOL.md`、`docs/NEXT_ACTIONS.md`、`docs/DECISIONS.md`、`docs/PROJECT_STATE.md`。
- 不要修改：不要重构 `progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh` 或 Round 00 脚本。
- 验收标准：Codex 后续能只凭文档理解项目最终目标、当前状态、下一步任务和停止条件。
- 风险：文档把未来规划写成已完成事实。
- 是否需要用户介入：否。

## TASK-002: 设计统一 task registry

- 状态：pending
- 背景：当前任务状态主要写在 `progress.json` 和 `progress.html` 的静态 Round 00 元数据中，Round 01-21 尚未进入统一任务体系。
- 目标：设计一个面向 Round 00-21 的统一 task registry 数据结构和文件位置。
- 要修改：新增或更新设计文档，必要时新增空的 registry 草案文件。
- 不要修改：不要迁移现有进度，不要改 `mark_done.sh` 行为。
- 验收标准：明确 task registry 的文件名、字段、兼容策略、Round 00 迁移方式和后续实现步骤。
- 风险：过早设计过复杂，导致后续实现负担过重。
- 是否需要用户介入：否。

## TASK-003: 实现 task registry 初版

- 状态：pending
- 背景：需要把 Round 00 已有任务先抽成统一 registry，为后续 Round 01-21 纳入系统做底座。
- 目标：实现第一版 task registry，至少完整覆盖 Round 00 现有任务。
- 要修改：新增 task registry 数据文件，必要时新增生成或校验脚本。
- 不要修改：不要改变现有用户进度状态，不要删除 `progress.json` 中旧字段。
- 验收标准：Round 00 现有任务都有稳定 `task_id`，并包含 round、section、标题、类型和来源路径。
- 风险：registry 与 `progress.html` 中现有静态元数据不一致。
- 是否需要用户介入：否。

## TASK-004: 升级 progress 数据结构

- 状态：pending
- 背景：当前 `progress.json` 只保存 Round 00 任务的 `done` 与 `done_at`，无法表达统一任务状态、尝试次数、复习标记或备注。
- 目标：提出并实现兼容旧数据的 progress state 初版。
- 要修改：`progress.json`，必要时新增迁移或兼容脚本。
- 不要修改：不要丢失任何现有任务完成状态。
- 验收标准：旧的 `done` / `done_at` 信息仍可读取，新结构能表达 `status`、`completed_at`、`notes` 等字段。
- 风险：破坏 `mark_done.sh` 和 `progress.html` 对旧结构的读取。
- 是否需要用户介入：否，除非需要不可逆迁移。

## TASK-005: 兼容 Round 00 旧进度

- 状态：pending
- 背景：Round 00 是当前唯一可运行闭环，后续升级必须优先保护它。
- 目标：确保升级后的 task registry 和 progress state 能兼容 Round 00 旧任务 ID。
- 要修改：兼容层、校验脚本或文档说明。
- 不要修改：不要重命名 Round 00 旧 `task_id`，除非提供明确映射并保留兼容。
- 验收标准：`bash mark_done.sh` 仍能显示和操作现有 Round 00 任务。
- 风险：旧任务 ID 改动导致用户已有记录失效。
- 是否需要用户介入：否。

## TASK-006: 升级 mark_done.sh 支持全路线任务

- 状态：pending
- 背景：当前 `mark_done.sh` 只识别 `progress.json` 中已有 Round 00 任务。
- 目标：让 `mark_done.sh` 能基于统一 task registry 显示和标记全路线任务。
- 要修改：`mark_done.sh`，必要时修改或生成 `progress_data.js`。
- 不要修改：不要引入后端服务，不要破坏无参数查看状态的用法。
- 验收标准：无参数可显示按 round 分组的任务；传入 task_id 可标记任务；Round 00 旧任务仍可用。
- 风险：shell 内嵌 Python 逻辑膨胀，需要保持可维护。
- 是否需要用户介入：否。

## TASK-007: 升级 progress_data.js 生成逻辑

- 状态：pending
- 背景：`progress_data.js` 当前只是 `progress.json` 的浏览器镜像，缺少 registry 元数据和全路线展示所需信息。
- 目标：让生成逻辑能输出进度状态和任务元数据，供静态页面读取。
- 要修改：`mark_done.sh` 或新增生成脚本，`progress_data.js`。
- 不要修改：不要手动维护 `progress_data.js` 中的业务状态。
- 验收标准：生成后的 JS 能被 `progress.html` 读取，并包含全路线展示所需最小数据。
- 风险：手动编辑自动生成文件导致状态源混乱。
- 是否需要用户介入：否。

## TASK-008: 升级 progress.html 全路线展示

- 状态：pending
- 背景：当前 `progress.html` 的 `ROUNDS` 静态元数据只覆盖 Round 00。
- 目标：让页面至少能展示 Round 00-21 的轮次级进度和任务列表入口。
- 要修改：`progress.html`，必要时调整 `progress_data.js` 数据消费方式。
- 不要修改：不要引入大型前端框架，不要做复杂网页交互。
- 验收标准：页面能展示全路线进度，Round 00 任务状态仍正确显示。
- 风险：页面逻辑和数据源耦合过深。
- 是否需要用户介入：否。

## TASK-009: 加入 action event log 初版

- 状态：pending
- 背景：当前系统只保存任务最终完成状态，没有结构化动作历史。
- 目标：新增用户动作事件日志，让每次标记、撤销或后续操作都能被记录。
- 要修改：新增 action log 数据文件或目录，升级写入逻辑。
- 不要修改：不要引入数据库，不要做账号系统。
- 验收标准：每次任务操作生成 action_id、task_id、round_id、action_type、timestamp、result 等字段。
- 风险：日志文件持续增长，需要保持格式简单可校验。
- 是否需要用户介入：否。

## TASK-010: 加入 task feedback 原型

- 状态：pending
- 背景：用户最终目标要求每条具体任务有反馈和下一步建议。
- 目标：建立最小 feedback record，并在任务完成后生成简单规则反馈。
- 要修改：新增 feedback 数据结构，必要时更新 `mark_done.sh` 或生成脚本。
- 不要修改：不要引入大模型自动评价，不要做复杂推荐。
- 验收标准：任务完成后能产生可展示的反馈消息和下一步建议。
- 风险：反馈文案过度承诺或误导用户能力状态。
- 是否需要用户介入：否。

## TASK-011: 建立 Round 01 最小骨架

- 状态：pending
- 背景：Round 01 已有根目录大纲文档，但没有 `rounds/round_01/` 可执行展开目录。
- 目标：建立 Round 01 的 notes、exercises 和 final 骨架，并纳入任务注册。
- 要修改：新增 `rounds/round_01/` 目录和最小文件，必要时更新 task registry。
- 不要修改：不要一次性落地 Round 02-21。
- 验收标准：Round 01 有清晰目录、最小练习入口和验证方式。
- 风险：过早生成大量低质量练习。
- 是否需要用户介入：否。

## TASK-012: 建立数据校验脚本

- 状态：pending
- 背景：随着 registry、progress、action log 和 feedback 增加，需要能发现数据损坏。
- 目标：新增最小数据校验脚本。
- 要修改：新增校验脚本和必要说明。
- 不要修改：不要引入重型测试框架。
- 验收标准：能校验 JSON 合法性、必填字段、task_id 引用关系和 Round 00 兼容性。
- 风险：校验规则过早绑定未来未实现结构。
- 是否需要用户介入：否。

---

# VPS 实操支线任务（编号 TASK-VPS-XX）

> 主线 TASK-002 ~ TASK-012 与 VPS 支线 TASK-VPS-00 ~ TASK-VPS-12 **可并行推进**，编号空间互不冲突。
> Level 2 及以上的远程操作必须先走 `docs/templates/remote_operation_confirmation.md`。

## TASK-VPS-00 ~ TASK-VPS-03：文档与治理（Level 0 / Level 1）

- 状态：done（在 2026-05-10 一次性完成 VPS 模块文档与治理体系接入；未来如需调整文档，可重新打开对应 Round）
- 输出：
  - `docs/modules/vps_remote_ops.md`
  - `docs/governance/remote_operation_permissions.md`
  - `docs/governance/repo_rules.md`、`docs/governance/file_naming_rules.md`、`docs/governance/codex_workflow.md`
  - `docs/checklists/*`、`docs/templates/*`
  - `rounds/stage_03_vps_remote_ops/round_vps_00 ~ vps_03`
- 是否需要用户介入：否。

## TASK-VPS-04: SSH 与远程 Linux 基础任务文档化

- 状态：done（文档已写在 `rounds/stage_03_vps_remote_ops/round_vps_04_ssh_basics.md`）
- 备注：实际执行（SSH 登录）属 Level 2 / 3，由 TASK-VPS-05 起接管。

## TASK-VPS-05: 首次远程服务器只读检查（Level 2）

- 状态：pending（**需用户授权后启动**）
- 背景：VPS 模块的"第一次真实操作"。
- 目标：通过 SSH 完成只读检查，输出脱敏的服务器基础信息记录。
- 前置：用户使用 `docs/templates/remote_operation_confirmation.md` 走完确认。
- 验收标准：参见 `rounds/stage_03_vps_remote_ops/round_vps_05_first_readonly_check.md`。
- 风险：误执行写入操作 / 误把真实 IP / 用户名写入仓库。
- 是否需要用户介入：是。

## TASK-VPS-06 ~ TASK-VPS-08: 远程目录 / GitHub 同步 / tmux 训练（Level 3）

- 状态：pending（**需用户授权后启动，且应在 TASK-VPS-05 完成后再进入**）
- 备注：每次执行前都需要用户**单独**授权；不批量预授权。

## TASK-VPS-09: 网络与端口检查（Level 2/3）

- 状态：pending（**需用户授权**）。

## TASK-VPS-10: 远程 API 调用最小实验（Level 3）

- 状态：pending（**需用户授权**）。
- 风险：误把真实 API Key 写入仓库 / commit message。

## TASK-VPS-11: 最小 Web/API 服务部署实验（Level 4）

- 状态：pending（**需用户授权**）。
- 风险：误开放公网端口 / 误绑定域名 / 误启用 systemd。

## TASK-VPS-12: VPS 操作 SOP 与 VULTRagent 需求草案（Level 1）

- 状态：pending（**TASK-VPS-05 ~ TASK-VPS-11 至少完成 1 ~ 2 次真实执行后再做沉淀**，否则 SOP 仅为纸上规划）
- 输出：`rounds/stage_03_vps_remote_ops/outputs/vps_sop.md`、`rounds/stage_03_vps_remote_ops/outputs/vultragent_mvp_requirements.md`
- 是否需要用户介入：否。

---

## 推荐下一步（按优先级）

1. **TASK-002**：设计统一 task registry（主线核心，依然是最高优先级）。
2. **TASK-VPS-05**：当用户希望开始真实远程实操时，由用户主动启动并授权。
3. **TASK-003**：实现 task registry 初版，覆盖 Round 00。

> 主线推进与 VPS 实操推进**互不阻塞**；用户可根据当下心情与可用时间选择当晚要做哪一条。

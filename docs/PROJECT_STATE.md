# Project State

## 1. 项目概览
- **仓库名称**：`computer_study_plan`（基于当前目录名判断）。
- **唯一本地工作副本**：`~/PycharmProjects/computer_study_plan`（绝对路径 `/Users/alalapi/PycharmProjects/computer_study_plan`）。IDE 工作区、文档中的「仓库根」、Git 操作均指此目录；详见 `docs/WORKSPACE.md`。
- **练习沙盒（非仓库）**：Round 00 等终端练习使用 `~/cli-lab/round0`，与 Git 根分离。
- **项目类型判断**：当前以**学习型仓库**为主，附带少量脚本与可视化看板能力（混合了文档 + 轻量 CLI + 静态页面）。
- **当前主入口（基于实际文件）**：
  - `README.md`：总入口与学习路线说明。
  - `progress.html`：进度可视化看板入口（静态页面）。
  - `mark_done.sh`：命令行进度标记工具。
  - `rounds/round_00/week*/exercises.sh`、`rounds/round_00/final/comprehensive_exercise.sh`：Round 00 的练习执行入口。
- **是否已形成可运行项目骨架**：
  - 对“学习进度跟踪 + Round 00 练习”而言，**已形成最小可运行骨架**。
  - 对 README 中描述的 Round 01–21 实操代码能力而言，**尚未形成对应代码骨架**（当前主要是大纲文档）。

## 2. 仓库目录与关键文件

### 2.1 主要目录结构（实际存在）
- 根目录：包含 `round_00.md` 至 `round_21.md`、进度相关文件与脚本。
- `rounds/round_00/`：唯一已展开的轮次目录，含 `week1/week2/week3/final` 子目录及脚本/笔记。
- `docs/`：本次新增，用于沉淀项目状态文档。

> ⚠ 历史记录：根目录原有 `plan_round_00.txt` ~ `plan_round_21.txt`（22 份初版提示词文本），已于 **2026-05-12** 路线重定向时由用户授权删除，内容已被对应 `round_XX.md` 完整吸收。

### 2.2 关键文件与作用
- `README.md`：项目介绍、路线图、目录说明、进度系统说明。
- `CONVERSION_PROTOCOL.md`：Round md 标准结构与进度系统协议（v2.0，已移除 txt 转换流程）。
- `progress.json`：进度状态"单一事实源"（任务完成状态 + 四主线 lanes，v2）。
- `progress_data.js`：由脚本生成，供前端看板读取。
- `progress.html`：可视化展示进度。
- `mark_done.sh`：更新 `progress.json` 并同步生成 `progress_data.js`。
- `round_00.md`~`round_21.md`：21+1 轮学习说明文档（路线重定向后定位为"工程实操线素材库"）。
- `plan_round_00.txt`~`plan_round_21.txt`：已于 2026-05-12 由用户授权删除（仅 git history 可追溯）。

## 3. round00-round21 文档与实际实现对应关系

### 3.1 轮次文件存在性检查
- `round_00.md` 到 `round_21.md`：**全部存在**（22 个）。
- `plan_round_00.txt` 到 `plan_round_21.txt`：**已于 2026-05-12 删除**（路线重定向，用户授权）。

### 3.2 实际代码/脚本落地情况
- **已落地为真实脚本的轮次**：仅确认 `rounds/round_00/`。
  - 包含：`week1/2/3` 的 `notes.md` 与 `exercises.sh`，以及 `final/comprehensive_exercise.sh`。
- **其余轮次（Round 01–21）**：当前仓库未发现对应 `rounds/round_01`~`rounds/round_21` 的展开目录与可执行代码文件；主要为根目录下的路线文档（`.md`）与规划文本（`.txt`）。

### 3.3 文档与实现脱节情况（已确认不一致点）
1. **README 的“项目结构”展示了完整 `rounds/` 展开结构趋势，但当前实际仅有 `rounds/round_00`。**
2. 多个高轮次文档（如 Round 07、Round 09、Round 21）描述了 `ai_prep_tool.py`、`tests/`、PyTorch/NLP 脚本等目标与示例，但仓库中未发现对应真实 `.py` 源文件与目录落地。
3. 路线层面“已规划完整”，实现层面“仅 Round 00 实体化”，当前应按“**规划先行、实现滞后**”认定。

### 3.4 当前代码实现大致对应轮次
- **明确可执行并闭环的部分**：Round 00（终端入门 + 进度打卡系统）。
- **Round 01–21**：目前主要对应“学习大纲/学习说明”阶段，落地实现未确认或尚未实现。

## 4. 当前已实现功能

### 4.1 已实现的核心功能
1. **学习任务进度持久化**：`progress.json` 保存任务完成状态与时间。
2. **进度写入 CLI**：`mark_done.sh` 支持标记完成、撤销、状态查看。
3. **前端进度看板展示**：`progress.html` + `progress_data.js` 实现可视化查看。
4. **Round 00 练习脚本执行链路**：week1~3 与 final 脚本可调用 `mark_done.sh` 自动打卡。

### 4.2 已实现的辅助功能
- 任务 ID 体系（`w1-*`、`w2-*`、`w3-*`、`fin-*`）与状态列表展示。
- 文档生成流程规范（`CONVERSION_PROTOCOL.md`）已建立。

### 4.3 已实现但不完整的功能
- 进度系统目前只覆盖 Round 00 任务集合，未覆盖 Round 01–21。
- 学习路线已覆盖到 Round 21，但对应脚本/项目代码未成体系落地。

### 4.4 当前仅能跑通 demo 的部分
- Round 00 练习更接近教学 demo/手把手任务，而非可复用业务应用。

### 4.5 当前仅有文档、暂无落地代码的部分
- Round 01–21 中涉及的 Python 工程化、测试体系、API、数据库、ML/NLP 训练等内容，当前仓库内未发现同名模块或工程目录落地（按“尚未实现/未确认”记录）。

## 5. 当前可运行能力

### 5.1 启动与使用方式（实际可执行）
1. **CLI 方式**：
   - `bash mark_done.sh`（查看任务）
   - `bash mark_done.sh <task-id>`（标记完成）
   - `bash mark_done.sh <task-id> --undo`（撤销）
2. **静态看板方式**：
   - 直接打开 `progress.html`（手动刷新查看最新状态）
   - 或 `python3 -m http.server 8000` 后访问 `http://localhost:8000/progress.html`
3. **Round 00 脚本方式**：运行 `rounds/round_00/week*/exercises.sh` 与 `rounds/round_00/final/comprehensive_exercise.sh`。

### 5.2 环境与依赖文件检查
- `requirements.txt`：未发现。
- `pyproject.toml`：未发现。
- `Dockerfile` / `docker-compose.yml`：未发现。
- 显式虚拟环境说明：在部分文档示例中出现（例如 Round 09 的示例片段），但仓库未提供统一依赖清单。

### 5.3 入口类型判断
- API 入口：未确认（未发现服务框架代码）。
- CLI 入口：已存在（`mark_done.sh`，以及 Round 00 各练习 shell 脚本）。
- 脚本入口：已存在（Round 00）。
- 测试入口：未确认（未发现 `tests/` 实体目录与测试脚本文件）。

### 5.4 配置、日志、数据库文件现状
- 配置文件：未确认（未发现独立配置模块）。
- 日志文件：仓库未内置运行日志产物；脚本以终端输出为主。
- 数据库文件：未发现（如 `.db`/`.sqlite`）。

### 5.5 最小可运行闭环判断
- **已具备的闭环**：Round 00 学习任务执行 → 调用 `mark_done.sh` 写入状态 → `progress_data.js` 同步 → `progress.html` 展示。
- **未具备的闭环**：Round 01–21 对应的代码执行、数据持久化、测试验证、服务化运行闭环。

## 6. 数据、状态记录与反馈机制现状

### 6.1 当前已有能力
- **数据层**：有基础 JSON 状态存储（`progress.json`）。
- **服务层**：以 shell 脚本形式提供状态更新服务（`mark_done.sh`），无独立服务进程。
- **日志层**：仅终端输出，未形成结构化日志与日志轮转。
- **反馈展示层**：有前端进度看板（`progress.html`）用于可视化反馈。

### 6.2 “根据用户动作进行记录和反馈”机制评估
- 在 **Round 00 学习任务** 范围内：**部分已实现**（用户执行脚本/命令后可记录并反馈）。
- 在 **全项目（Round 01–21）** 范围内：**核心能力缺失**，缺失点如下：
  1. **数据层**：缺少统一的多轮次任务/学习事件数据模型。
  2. **服务层**：无统一应用服务承载多轮次记录逻辑。
  3. **日志层**：无可检索的结构化事件日志。
  4. **事件层**：未建立“用户动作事件”标准（事件类型、payload、时间戳规范）。
  5. **用户状态层**：未看到用户维度状态（仅单份全局进度，且当前只覆盖 Round 00 任务）。
  6. **前后端交互层**：无 API，前端依赖本地文件读取，不支持实时或多端一致状态。
  7. **反馈展示层**：展示层仅聚焦 Round 00，不覆盖全路线。

## 7. 当前存在的关键问题
1. **文档规划与代码落地明显脱节**：Round 01–21 多为路线文档，代码仓库尚未对应展开。
2. **项目入口不统一**：当前同时存在 README 指导、shell 脚本、静态页面，但缺少统一主程序/统一命令入口。
3. **状态记录范围过窄**：进度系统仅覆盖 Round 00，无法支撑全路线持续跟踪。
4. **缺少可验证工程能力**：未发现测试目录、依赖清单、构建/运行标准化配置，难以稳定迭代。
5. **“用户动作→记录→反馈”全链路未成型**：仅在局部脚本层成立，尚未升级为全项目机制。

## 8. 最优先的下一步事项
> 以下仅基于当前现状，按优先级排序（不扩散设计）。

1. **先统一全仓库状态模型**：把 Round 01–21 的任务结构纳入 `progress.json`（或新统一数据结构），解决“只能记录 Round 00”的核心断层。
2. **补齐轮次落地最小骨架**：至少为 Round 01（可再含 Round 02）建立与 Round 00 同级的 `rounds/round_XX/` 目录、notes、exercises 脚本与可执行链路。
3. **建立最小依赖与运行规范**：补充 `requirements.txt` 或 `pyproject.toml`（二选一）及基础运行说明，降低后续迭代不确定性。
4. **补最小测试检查**：至少为状态写入脚本（`mark_done.sh` 相关逻辑）增加基础校验脚本，防止进度文件损坏。
5. **校正文档与现实不一致点**：在 README 明确“已实现轮次 / 规划轮次”，避免将规划误读为已落地功能。

## 9. 本次扫描结论
- 当前仓库的真实状态可概括为：**“完整学习路线文档已铺开到 Round 21，但代码落地主要停留在 Round 00 与进度系统原型。”**
- 因此后续迭代应优先处理“状态模型扩展 + 轮次落地骨架 + 文档对齐”三件事，先把“可持续更新底座”建立起来，再做大规模重构或功能扩展。

## 10. 更新日志
- 2026-04-28 11:24: 基于当前仓库代码完成项目现状扫描并更新文档。

## 11. 2026-05-05 长期推进文档更新

### 11.1 本轮新增内容
- 新增 `AGENTS.md`，作为 Codex 每次进入仓库时的工作入口规则。
- 新增 `docs/CODEX_LONG_TERM_PLAN.md`，明确本仓库的长期目标、阶段路线、数据模型方向、自动推进规则、停止条件和近期优先级。
- 新增 `docs/AUTO_ADVANCE_PROTOCOL.md`，定义后续收到短指令时的单轮自动推进流程、验证流程、commit / push / PR 规则和最终汇报格式。
- 新增 `docs/NEXT_ACTIONS.md`，建立从 TASK-001 到 TASK-012 的下一步任务队列。
- 新增 `docs/DECISIONS.md`，记录当前阶段继续使用 JSON、保留静态页面、保留 `mark_done.sh`、独立分支推进、先做动作记录与反馈原型的 ADR。

### 11.2 当前最终目标
- 当前项目最终目标已明确为：从“计算机基础学习大纲仓库”逐步升级为“网页交互版计算机基础与 AI 工程学习系统”。
- 目标系统应支持 Round 00-21 全路线任务体系、任务状态、用户动作记录、反馈、复盘、总进度与 round 进度展示。
- 该目标是长期方向，不代表当前已经实现完整网页交互系统。

### 11.3 当前仍未实现的关键能力
- 当前仍未实现真正的网页交互操作；`progress.html` 仍主要是静态看板，任务状态更新依赖 `mark_done.sh` 和本地文件刷新。
- 当前仍未实现 action event log；系统尚未保存每次用户动作的结构化历史。
- 当前仍未实现 task feedback 原型；系统尚未为每条任务生成结构化反馈与下一步建议。
- 当前仍未实现 Round 01-21 的统一任务注册和可执行练习目录。
- 当前仍未引入数据库、后端 API、前端框架或测试体系。

### 11.4 下一步最优先事项
1. TASK-002：设计统一 task registry。
2. TASK-003：实现 task registry 初版，优先覆盖 Round 00 现有任务。
3. TASK-004：升级 progress 数据结构，并保证旧进度兼容。
4. TASK-005：验证并保护 Round 00 旧任务 ID 与已有进度。
5. TASK-006：升级 `mark_done.sh` 支持统一任务体系。

### 11.5 更新日志
- 2026-05-05：完成长期目标文档、自动推进协议、任务队列、ADR 和 Codex 仓库入口规则；本轮没有改动进度数据、静态页面、Round 00 脚本或后续功能实现。

## 12. 2026-05-10 VPS 模块接入

### 12.1 本轮新增内容
- 新增治理文档目录：
  - `docs/governance/repo_rules.md`：仓库治理总规则（删除 / 合并 / 命名硬约束）。
  - `docs/governance/file_naming_rules.md`：文件命名规则（主线 vs 支线编号空间、目录约定）。
  - `docs/governance/codex_workflow.md`：Codex / Cursor / 编程 AI 协作工作流总览。
  - `docs/governance/remote_operation_permissions.md`：远程操作 Level 0 ~ Level 5 权限等级，含每级允许 / 禁止 / 命令示例 / 速查表。
- 新增模块文档：`docs/modules/vps_remote_ops.md`（VPS 远程操作模块总纲）。
- 新增检查清单：
  - `docs/checklists/vps_safety_checklist.md`
  - `docs/checklists/remote_operation_checklist.md`
  - `docs/checklists/repository_cleanup_checklist.md`
  - `docs/checklists/project_acceptance_checklist.md`
- 新增确认模板：
  - `docs/templates/remote_operation_confirmation.md`
  - `docs/templates/repository_cleanup_confirmation.md`
- 新增 VPS 实操支线阶段目录与 13 份 Round 文档：
  - `rounds/stage_03_vps_remote_ops/README.md`
  - `rounds/stage_03_vps_remote_ops/round_vps_00_repo_scan.md` ~ `round_vps_12_sop_and_vultragent.md`
- 更新 `README.md`：
  - "项目结构"段落加入 docs 子目录与 stage_03 目录索引。
  - "全局路线图"下新增"实操支线 · VPS 远程操作"段落，含安全约束与入口链接。
- 新增 `.gitignore`：忽略 `.DS_Store`、`.env`、`.venv/`、`*.pem`、`id_rsa*` 等敏感 / 系统副产物。

### 12.2 本轮**未**改动的文件（按硬约束保护）
- `progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh`：Round 00 最小闭环。
- `rounds/round_00/` 下任何文件。
- `round_00.md` ~ `round_21.md`：主线 Round 概览未做内容改动；对应 `plan_round_XX.txt` 计划文本源在 2026-05-12 由用户授权删除。
- `AGENTS.md`、`CONVERSION_PROTOCOL.md`、`docs/CODEX_LONG_TERM_PLAN.md`、`docs/AUTO_ADVANCE_PROTOCOL.md`、`docs/DECISIONS.md`：本轮未触动。
- `.idea/misc.xml`：IDE 自动改动，非本轮范围。

### 12.3 当前 VPS 支线状态
- 文档体系：已建立。
- 实际远程操作：**全部未执行**。本轮没有连接任何 VPS、没有使用任何真实凭证、没有部署任何真实服务。
- 风险：
  - VPS-04 ~ VPS-12 中的命令样例必须由用户在执行时再次审阅。
  - Level 2 及以上操作必须先走 `docs/templates/remote_operation_confirmation.md`。
  - VULTRagent 仅有需求草案接口位置，**未**在本仓库实现。

### 12.4 下一步可推进方向（与 NEXT_ACTIONS.md 同步）
- 主线优先级仍按 TASK-002 ~ TASK-012 推进（task registry / progress / Round 01 骨架等）。
- VPS 支线可按 Round VPS-04 → VPS-05 推进（首次真实只读检查）；执行前需用户授权。
- 仅当用户明确启动时，才进入支线 Level 2/3/4 操作。

### 12.5 更新日志
- 2026-05-10：完成 VPS 模块文档接入、远程操作权限等级、安全 / 部署 / 治理 checklist、确认模板与 13 份 Round 文档；未改动 Round 00 闭环；未连接任何远程服务器。

## 13. 2026-05-12 路线重定向（重大变更）

### 13.1 本轮性质

这是一次**重大方向变更**：仓库总目标从"网页交互式 AI 工程学习系统"升级为"软考中级 → 408/数学二/0854 跨专业考研 + Linux/工程实操"的多目标耦合路线。
本轮经用户明确授权一次性完成"删除 + 治理 + 路线骨架 + 进度系统四主线扩展"，超出常规"一轮一任务"边界，但是受控的、全程可验证的。

### 13.2 本轮删除

- `plan_round_00.txt` ~ `plan_round_21.txt`（22 份初版提示词文本）。用户授权清理；内容已被对应 `round_XX.md` 完整吸收；git history 仍可追溯。

### 13.3 本轮新增（13 份文档 + 7 个目录）

- 路线骨架（8）：`docs/MASTER_STUDY_ROADMAP.md`、`docs/STAGE_PLAN.md`、`docs/KNOWLEDGE_MAPPING.md`、`docs/WEEKLY_EXECUTION_TEMPLATE.md`、`docs/PROGRESS_RULES.md`、`docs/ERROR_REVIEW_SYSTEM.md`、`docs/GRADUATE_SCHOOL_TRACKER.md`（模板，**不含真实院校数据**）、`docs/PROJECT_PORTFOLIO_TRACK.md`。
- 审计报告（1）：`docs/AUDIT_2026_05_12.md`。
- 目录骨架（5）：`plans/README.md`、`plans/linux/README.md`、`plans/soft_exam/README.md`、`plans/math2/README.md`、`plans/408/README.md`、`records/README.md`、`records/weekly_reviews/.gitkeep`、`records/error_notes/.gitkeep`、`records/completed_tasks/.gitkeep`。

### 13.4 本轮修改（含进度系统升级）

- `progress.json`：v1 → v2。新增顶层 `lanes` 字段（4 条主线注册），每个 task 新增 `lane` 字段。Round 00 旧任务全部归 `engineering`，`done` 与 `done_at` 不变。
- `progress_data.js`：自动同步到 v2 结构（仍由 `mark_done.sh` 维护）。
- `mark_done.sh`：升级支持 v2，无参数运行时按 lane 分组输出；v1 数据可自动补 `engineering`。
- `progress.html`：重写为"总进度 + 四主线进度 + 本周任务/倒计时（localStorage）+ Stage 0–7 进度 + 薄弱项面板 + 按 lane 浏览 Round"。Round 00 现有展示完全保留。
- `CONVERSION_PROTOCOL.md`：v1.3 → v2.0。移除"txt → md 转换"全部流程；新增 lanes 数据结构说明；Round 概览表新增"所属主线"列。
- `README.md`：重写为路线总控入口（仓库定位、四主线、当前阶段、文档导航、维护规则）。
- `AGENTS.md`：新增 `MASTER_STUDY_ROADMAP` 与 `STAGE_PLAN` 为必读文档；新增"不缓存考题 / 院校信息"等约束。
- `docs/CODEX_LONG_TERM_PLAN.md`：顶部加 §0 路线重定向说明，§1 ~ §11 旧规划保留作为工程实操线参考。
- `docs/NEXT_ACTIONS.md`：新建 TASK-RR-00 ~ TASK-RR-08 任务队列；旧 TASK-002~012 部分标记为 done/superseded/deferred，全部保留。
- 治理与支线文档清理对 `plan_round_XX.txt` 的引用：`docs/governance/repo_rules.md`、`docs/governance/file_naming_rules.md`、`docs/templates/repository_cleanup_confirmation.md`、`docs/checklists/repository_cleanup_checklist.md`、`rounds/stage_03_vps_remote_ops/round_vps_00_repo_scan.md`、`rounds/stage_03_vps_remote_ops/round_vps_01_repo_cleanup.md`。

### 13.5 本轮**未**改动的高保护对象

- `rounds/round_00/` 下任何文件。
- `round_00.md` ~ `round_21.md`（22 份 md 全部保留）。
- Round 00 旧任务 ID、行为与默认完成状态（done=false）。
- `docs/AUTO_ADVANCE_PROTOCOL.md`、`docs/DECISIONS.md`（未触动）。
- `.idea/misc.xml`（IDE 自动改动，已 stash，不进入本轮 commit）。

### 13.6 验证结果

- `bash mark_done.sh`：可正常运行，按 lane 分组输出 21 条 Round 00 任务，全部 `engineering` lane，全部 `⬜ 未完成`。
- `python3 -m json.tool progress.json`：合法。
- `progress.html` 内嵌 JS 语法（Node 校验）：合法。
- 22 份 `round_XX.md`：完整保留。

### 13.7 当前进度系统状态

- 四主线 lanes 已注册：`engineering` / `soft_exam` / `math2` / `cs408`。
- 任务总数：21（全部在 `engineering` lane）。
- 完成率：0/21。
- 其余三条 lane 暂无注册任务（按真实学习节奏在 plans/ 下推进时再录入）。

### 13.8 下一步可推进方向（与 NEXT_ACTIONS.md 同步）

1. **TASK-RR-01**：Stage 2 软考 3 模块（ds / os / db）笔记骨架建立。
2. **TASK-RR-04**：数学二 limits + la_matrix 启动笔记。
3. **TASK-RR-02**：建立第一周复盘示例。
4. **TASK-RR-03**：Round 02 实操目录展开（可选）。
5. **TASK-RR-05 / 07**：用户提供院校信息 + 考试日期。

### 13.9 更新日志

- 2026-05-12：完成路线重定向（删除 txt + 8 份路线骨架 + plans/records 目录骨架 + 进度系统 v2 + README/AGENTS/长期规划文档对齐 + 治理引用清理）；未破坏 Round 00 闭环；未编造任何考试 / 院校信息；未引入新依赖。

## 14. 2026-05-28 路径统一

- 新增 `docs/WORKSPACE.md` 作为路径单一事实源。
- `README.md` §0、`AGENTS.md`、`docs/governance/repo_rules.md`、`rounds/round_00/README.md`、`mark_done.sh` 错误提示与上述约定对齐。
- 明确区分：**仓库根** `~/PycharmProjects/computer_study_plan` vs **练习沙盒** `~/cli-lab/round0`（Round 文档中的 `~/cli-lab` 保持不变）。

## 15. 2026-05-28 TASK-RR-03 Round 02 实操目录展开

### 15.1 本轮新增

- 新增 `rounds/round_02/README.md`。
- 新增 `rounds/round_02/week1|week2|week3/notes.md` 与 `exercises.sh`。
- 新增 `rounds/round_02/final/comprehensive_exercise.sh` 与 `command_cheatsheet.md`。

### 15.2 本轮修改

- `progress.json`：追加 Round 02 的 `r02-*` 任务，全部归属 `engineering` lane。
- `progress.html`：在 `ROUNDS` 静态元数据中注册 Round 02 任务面板。
- `CONVERSION_PROTOCOL.md`：Round 02 行的“实操目录”状态改为“✅ 已展开”。
- `README.md`：仓库结构与“按 lane / Round 浏览”说明同步到“Round 00 + Round 02”。
- `docs/NEXT_ACTIONS.md`：`TASK-RR-03` 状态更新为 done，并记录产物。

### 15.3 验证

- `python3 scripts/check_protocol_sync.py`。
- `python3 -m json.tool progress.json`。
- `bash mark_done.sh`（确认新增 `r02-*` 任务可识别并按 lane 展示）。

### 15.4 风险边界核对

- 未修改 `rounds/round_00/` 任何文件。
- 未修改 `records/` 下真实学习记录。

## 16. 2026-05-28 校验脚本缺失修复

### 16.1 本轮新增

- 新增 `scripts/check_protocol_sync.py`，用于执行仓库协议同步的基础一致性检查。

### 16.2 触发原因

- 命令 `python3 scripts/check_protocol_sync.py` 报错 `No such file or directory`，定位为仓库缺少该脚本文件与 `scripts/` 目录。

### 16.3 验证

- `python3 scripts/check_protocol_sync.py`：通过（`Protocol sync check PASSED`）。
- `python3 -m json.tool progress.json`：通过。

### 16.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 17. 2026-05-28 TASK-RR-01 软考三模块骨架落地

### 17.1 本轮新增

- 新增 `plans/soft_exam/ds.md`。
- 新增 `plans/soft_exam/os.md`。
- 新增 `plans/soft_exam/db.md`。

### 17.2 内容范围

- 三份文件均仅包含：学习章节骨架、与 408 差异提示、启动节奏建议、启动级易错提醒。
- 每份文件顶部均添加“以官方最新大纲为准”的提示；未写入具体考题与考点原文。

### 17.3 同步更新

- `docs/NEXT_ACTIONS.md`：`TASK-RR-01` 标记为 done，并补充实际产物。

### 17.4 验证

- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 -m json.tool progress.json`：通过。

### 17.5 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 18. 2026-05-28 TASK-RR-04 数学二启动骨架落地

### 18.1 本轮新增

- 新增 `plans/math2/limits.md`。
- 新增 `plans/math2/la_matrix.md`。

### 18.2 内容范围

- 两份文件均仅包含：建议小节标题、低强度启动节奏、启动级易错点示例。
- 文件顶部均保留“以官方最新大纲为准”的提醒，不缓存具体考题与题库内容。

### 18.3 同步更新

- `docs/NEXT_ACTIONS.md`：`TASK-RR-04` 标记为 done，并补充实际产物。

### 18.4 验证

- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 -m json.tool progress.json`：通过。
- `bash mark_done.sh`：通过（Round 00/02 任务识别正常）。

### 18.5 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 19. 2026-05-28 TASK-RR-02 第一周复盘示例落地

### 19.1 本轮新增

- 新增 `records/weekly_reviews/_example.md`。

### 19.2 内容范围

- 文件明确声明为示例骨架，不代表真实周复盘数据。
- 内容采用标准模式模板字段，覆盖“完成项/错题/卡点/下周计划/强度调整”。

### 19.3 同步更新

- `docs/NEXT_ACTIONS.md`：`TASK-RR-02` 标记为 done，并补充实际产物。

### 19.4 验证

- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 -m json.tool progress.json`：通过。
- `bash mark_done.sh`：通过。

### 19.5 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录（仅新增 `_example.md` 示例文件）。

## 20. 2026-05-28 TASK-009 动作事件日志原型

### 20.1 本轮新增

- 新增 `records/action_logs/README.md`（事件字段与使用说明）。

### 20.2 本轮修改

- `mark_done.sh`：在任务标记/撤销后自动追加写入 `records/action_logs/events.jsonl`（JSONL）。

### 20.3 事件字段（v1）

- `action_id`、`task_id`、`round_id`、`lane`、`action_type`、`timestamp`、`result`、`note`、`evidence_path`。

### 20.4 验证

- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 -m json.tool progress.json`：通过。
- `bash mark_done.sh`：通过（状态展示正常）。

### 20.5 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录（仅新增 action log 原型目录说明）。

## 21. 2026-05-28 TASK-010 任务反馈原型

### 21.1 本轮新增

- 新增 `scripts/generate_task_feedback.py`。
- 新增 `records/feedback/README.md`。
- 新增 `records/feedback/task_feedback.json`（原型输出）。

### 21.2 能力说明

- 基于 `progress.json` 与 `records/action_logs/events.jsonl` 生成任务级反馈。
- 当前反馈类型：`completed` / `not_started` / `in_progress`。
- 每个任务输出基础建议（`message` + `next_suggestion`）。

### 21.3 同步更新

- `docs/NEXT_ACTIONS.md`：`TASK-010` 标记为 done 并补齐产物。

### 21.4 验证

- `python3 scripts/generate_task_feedback.py`：通过并生成反馈文件。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 -m json.tool records/feedback/task_feedback.json`：通过。

### 21.5 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录（仅新增反馈原型文件）。

## 22. 2026-05-28 TASK-012 数据一致性校验脚本

### 22.1 本轮新增

- 新增 `scripts/validate_learning_data.py`。

### 22.2 校验范围

- `progress.json`：检查 lanes/tasks 结构、`done`/`done_at`/`lane` 字段。
- `records/action_logs/events.jsonl`：检查 `task_id` 存在性、动作类型、结果枚举、时间戳类型。
- `records/feedback/task_feedback.json`：检查任务 ID 对齐与反馈类型枚举。

### 22.3 同步更新

- `docs/NEXT_ACTIONS.md`：`TASK-012` 标记为 done 并记录产物。

### 22.4 验证

- `python3 scripts/validate_learning_data.py`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 -m json.tool progress.json`：通过。
- `python3 -m json.tool records/feedback/task_feedback.json`：通过。

### 22.5 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 23. 2026-05-28 TASK-011 Round 01 最小骨架

### 23.1 本轮新增

- 新增 `rounds/round_01/README.md`。
- 新增 `rounds/round_01/week1|week2|week3/notes.md`。
- 新增 `rounds/round_01/week1|week2|week3/exercises.sh`。
- 新增 `rounds/round_01/final/comprehensive_exercise.sh`。
- 新增 `rounds/round_01/final/command_cheatsheet.md`。

### 23.2 同步更新

- `CONVERSION_PROTOCOL.md`：Round 01 状态从“未展开”更新为“已展开”。
- `README.md`：已展开 Round 列表同步为 Round 00/01/02。
- `docs/NEXT_ACTIONS.md`：`TASK-011` 标记为 done 并记录产物。
- `progress.json`：新增 Round 01 的 `r01-*` 任务 ID。
- `progress.html`：新增 Round 01 面板与任务元数据展示。
- `rounds/round_01/*/exercises.sh`：接入 `mark_done.sh` 自动打卡。

### 23.3 验证

- `bash -n rounds/round_01/week1/exercises.sh`：通过。
- `bash -n rounds/round_01/week2/exercises.sh`：通过。
- `bash -n rounds/round_01/week3/exercises.sh`：通过。
- `bash -n rounds/round_01/final/comprehensive_exercise.sh`：通过。
- `python3 scripts/generate_task_feedback.py`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。
- `python3 -m json.tool progress.json`：通过。

### 23.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 24. 2026-05-28 Stage 1 可选推进：Round 03 最小骨架

### 24.1 本轮新增

- 新增 `rounds/round_03/README.md`。
- 新增 `rounds/round_03/week1|week2|week3/notes.md`。
- 新增 `rounds/round_03/week1|week2|week3/exercises.sh`。
- 新增 `rounds/round_03/final/comprehensive_exercise.sh`。
- 新增 `rounds/round_03/final/complexity_cheatsheet.md`。

### 24.2 同步更新

- `CONVERSION_PROTOCOL.md`：Round 03 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03。
- `docs/NEXT_ACTIONS.md`：可选下一轮提示从 Round 03 调整为 Round 04。

### 24.3 验证

- `bash -n rounds/round_03/week1/exercises.sh`：通过。
- `bash -n rounds/round_03/week2/exercises.sh`：通过。
- `bash -n rounds/round_03/week3/exercises.sh`：通过。
- `bash -n rounds/round_03/final/comprehensive_exercise.sh`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 24.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 25. 2026-05-28 RR-05 意向院校落库（待官网核验）

### 25.1 本轮修改

- `docs/GRADUATE_SCHOOL_TRACKER.md`：新增“意向院校（待官网核验）”区，记录用户目标院校“中国科学研究院”。
- `docs/NEXT_ACTIONS.md`：
  - `TASK-RR-05` 调整为 `in_progress`（目标已录入，待官网链接回填）。
  - `TASK-RR-06`、`TASK-RR-07`、`TASK-VPS-05` 按用户指示调整为 `deferred`。
  - 推荐下一步队列改为以“无需即时用户输入”的可选推进为主。

### 25.2 规则边界

- 未在主表写入任何未经官网核验的考试字段（专业代码/科目/复试）。
- 考试日期按用户要求暂不处理（两年内不纳入当前日程）。

### 25.3 验证

- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。
- `python3 -m json.tool progress.json`：通过。

### 25.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 26. 2026-05-28 Stage 1 可选推进：Round 04 最小骨架

### 26.1 本轮新增

- 新增 `rounds/round_04/README.md`。
- 新增 `rounds/round_04/week1|week2|week3/notes.md`。
- 新增 `rounds/round_04/week1|week2|week3/exercises.sh`。
- 新增 `rounds/round_04/final/comprehensive_exercise.sh`。
- 新增 `rounds/round_04/final/complexity_cheatsheet.md`。

### 26.2 同步更新

- `CONVERSION_PROTOCOL.md`：Round 04 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03/04。
- `docs/NEXT_ACTIONS.md`：可选下一轮提示从 Round 04 调整为 Round 05。

### 26.3 验证

- `bash -n rounds/round_04/week1/exercises.sh`：通过。
- `bash -n rounds/round_04/week2/exercises.sh`：通过。
- `bash -n rounds/round_04/week3/exercises.sh`：通过。
- `bash -n rounds/round_04/final/comprehensive_exercise.sh`：通过。
- `bash rounds/round_04/week1/exercises.sh`：通过。
- `bash rounds/round_04/week2/exercises.sh`：通过。
- `bash rounds/round_04/week3/exercises.sh`：通过。
- `bash rounds/round_04/final/comprehensive_exercise.sh`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 26.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 27. 2026-05-28 Stage 1 增强：Round 03 接入进度系统

### 27.1 本轮修改

- `progress.json`：新增 Round 03 的 `r03-*` 任务 ID。
- `progress.html`：新增 Round 03 面板与任务元数据展示。
- `rounds/round_03/*/exercises.sh`：接入 `mark_done.sh` 自动打卡。
- `README.md`：按 lane/Round 浏览描述同步到 Round 03。
- `docs/NEXT_ACTIONS.md`：可选项从 Round 03 进度接入更新为 Round 04 进度接入。

### 27.2 验证

- `bash -n rounds/round_03/week1/exercises.sh`：通过。
- `bash -n rounds/round_03/week2/exercises.sh`：通过。
- `bash -n rounds/round_03/week3/exercises.sh`：通过。
- `bash -n rounds/round_03/final/comprehensive_exercise.sh`：通过。
- `python3 scripts/generate_task_feedback.py`：通过（反馈文件已同步）。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。
- `python3 -m json.tool progress.json`：通过。

### 27.3 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 28. 2026-05-28 Stage 1 增强：Round 04 接入进度系统

### 28.1 本轮修改

- `progress.json`：新增 Round 04 的 `r04-*` 任务 ID。
- `progress.html`：新增 Round 04 面板与任务元数据展示。
- `rounds/round_04/*/exercises.sh`：接入 `mark_done.sh` 自动打卡。
- `README.md`：按 lane/Round 浏览描述同步到 Round 04。
- `docs/NEXT_ACTIONS.md`：可选项更新为 Round 05 推进建议。

### 28.2 验证

- `bash -n rounds/round_04/week1/exercises.sh`：通过。
- `bash -n rounds/round_04/week2/exercises.sh`：通过。
- `bash -n rounds/round_04/week3/exercises.sh`：通过。
- `bash -n rounds/round_04/final/comprehensive_exercise.sh`：通过。
- `python3 scripts/generate_task_feedback.py`：通过（反馈文件已同步）。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。
- `python3 -m json.tool progress.json`：通过。

### 28.3 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 29. 2026-05-28 Stage 1 可选推进：Round 05 最小骨架

### 29.1 本轮新增

- 新增 `rounds/round_05/README.md`。
- 新增 `rounds/round_05/week1|week2|week3/notes.md`。
- 新增 `rounds/round_05/week1|week2|week3/exercises.sh`。
- 新增 `rounds/round_05/final/comprehensive_exercise.sh`。
- 新增 `rounds/round_05/final/algorithm_patterns_cheatsheet.md`。

### 29.2 本轮修改

- `CONVERSION_PROTOCOL.md`：Round 05 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03/04/05。
- `docs/NEXT_ACTIONS.md`：新增并完成 `TASK-RR-09`，可选下一轮提示更新到 Round 06 最小骨架。

### 29.3 验证

- `bash -n rounds/round_05/week1/exercises.sh`：通过。
- `bash -n rounds/round_05/week2/exercises.sh`：通过。
- `bash -n rounds/round_05/week3/exercises.sh`：通过。
- `bash -n rounds/round_05/final/comprehensive_exercise.sh`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 29.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 30. 2026-05-28 Stage 1 可选推进：Round 06 最小骨架

### 30.1 本轮新增

- 新增 `rounds/round_06/README.md`。
- 新增 `rounds/round_06/week1|week2|week3/notes.md`。
- 新增 `rounds/round_06/week1|week2|week3/exercises.sh`。
- 新增 `rounds/round_06/final/comprehensive_exercise.sh`。
- 新增 `rounds/round_06/final/linux_automation_cheatsheet.md`。

### 30.2 本轮修改

- `CONVERSION_PROTOCOL.md`：Round 06 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03/04/05/06。
- `docs/NEXT_ACTIONS.md`：新增并完成 `TASK-RR-10`，可选下一轮提示更新到 Round 07 最小骨架。

### 30.3 验证

- `bash -n rounds/round_06/week1/exercises.sh`：通过。
- `bash -n rounds/round_06/week2/exercises.sh`：通过。
- `bash -n rounds/round_06/week3/exercises.sh`：通过。
- `bash -n rounds/round_06/final/comprehensive_exercise.sh`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 30.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 31. 2026-05-29 Stage 1 可选推进：Round 07 最小骨架

### 31.1 本轮新增

- 新增 `rounds/round_07/README.md`。
- 新增 `rounds/round_07/week1|week2|week3/notes.md`。
- 新增 `rounds/round_07/week1|week2|week3/exercises.py`。
- 新增 `rounds/round_07/final/comprehensive_exercise.py`。
- 新增 `rounds/round_07/final/ai_prep_tool_cheatsheet.md`。

### 31.2 本轮修改

- `CONVERSION_PROTOCOL.md`：Round 07 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03/04/05/06/07。
- `docs/NEXT_ACTIONS.md`：新增并完成 `TASK-RR-11`，可选下一轮提示更新到 Round 08 最小骨架。

### 31.3 验证

- `python3 -m py_compile rounds/round_07/week1/exercises.py`：通过。
- `python3 -m py_compile rounds/round_07/week2/exercises.py`：通过。
- `python3 -m py_compile rounds/round_07/week3/exercises.py`：通过。
- `python3 -m py_compile rounds/round_07/final/comprehensive_exercise.py`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 31.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 32. 2026-05-29 Stage 1 可选推进：Round 08 最小骨架

### 32.1 本轮新增

- 新增 `rounds/round_08/README.md`。
- 新增 `rounds/round_08/week1|week2|week3/notes.md`。
- 新增 `rounds/round_08/week1|week2|week3/exercises.py`。
- 新增 `rounds/round_08/final/comprehensive_exercise.py`。
- 新增 `rounds/round_08/final/upgrade_route_cheatsheet.md`。

### 32.2 本轮修改

- `CONVERSION_PROTOCOL.md`：Round 08 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03/04/05/06/07/08。
- `docs/NEXT_ACTIONS.md`：新增并完成 `TASK-RR-12`，可选下一轮提示更新到 Round 09 最小骨架。

### 32.3 验证

- `python3 -m py_compile rounds/round_08/week1/exercises.py`：通过。
- `python3 -m py_compile rounds/round_08/week2/exercises.py`：通过。
- `python3 -m py_compile rounds/round_08/week3/exercises.py`：通过。
- `python3 -m py_compile rounds/round_08/final/comprehensive_exercise.py`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 32.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 33. 2026-05-29 Stage 1 可选推进：Round 09 最小骨架

### 33.1 本轮新增

- 新增 `rounds/round_09/README.md`。
- 新增 `rounds/round_09/week1|week2|week3/notes.md`。
- 新增 `rounds/round_09/week1|week2|week3/exercises.py`。
- 新增 `rounds/round_09/final/comprehensive_exercise.py`。
- 新增 `rounds/round_09/final/repo_testing_cheatsheet.md`。

### 33.2 本轮修改

- `CONVERSION_PROTOCOL.md`：Round 09 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03/04/05/06/07/08/09。
- `docs/NEXT_ACTIONS.md`：新增并完成 `TASK-RR-13`，可选下一轮提示更新到 Round 10 最小骨架。

### 33.3 验证

- `python3 -m py_compile rounds/round_09/week1/exercises.py`：通过。
- `python3 -m py_compile rounds/round_09/week2/exercises.py`：通过。
- `python3 -m py_compile rounds/round_09/week3/exercises.py`：通过。
- `python3 -m py_compile rounds/round_09/final/comprehensive_exercise.py`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 33.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 34. 2026-05-31 agent_gate 与 Round 10 最小骨架

### 34.1 本轮新增

- 新增 `scripts/agent_gate.py`（前置检查 + 自动选取无需用户介入的下一任务）。
- 新增 `rounds/round_10/README.md`。
- 新增 `rounds/round_10/week1|week2|week3/notes.md`。
- 新增 `rounds/round_10/week1|week2|week3/exercises.py`。
- 新增 `rounds/round_10/final/comprehensive_exercise.py`。
- 新增 `rounds/round_10/final/python_engineering_cheatsheet.md`。

### 34.2 本轮修改

- `CONVERSION_PROTOCOL.md`：Round 10 状态更新为“已展开”。
- `README.md`：已展开 Round 列表同步到 Round 00/01/02/03/04/05/06/07/08/09/10。
- `docs/NEXT_ACTIONS.md`：新增并完成 `TASK-RR-14`，可选下一轮提示更新到 Round 11 最小骨架。

### 34.3 验证

- `python3 -m py_compile rounds/round_10/week1/exercises.py`：通过。
- `python3 -m py_compile rounds/round_10/week2/exercises.py`：通过。
- `python3 -m py_compile rounds/round_10/week3/exercises.py`：通过。
- `python3 -m py_compile rounds/round_10/final/comprehensive_exercise.py`：通过。
- `python3 scripts/agent_gate.py --verify`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 34.4 风险边界核对

- 未改动 `rounds/round_00/`。
- 未改动 `records/` 下真实学习记录。

## 35. 2026-05-31 TASK-RR-15 Round 11 最小骨架

### 35.1 本轮新增

- 新增 `rounds/round_11/` 完整最小骨架（README、week1–3、final）。

### 35.2 本轮修改

- `scripts/agent_gate.py`：修正可选 Round 任务 ID 序号映射。
- `CONVERSION_PROTOCOL.md`、`README.md`、`docs/NEXT_ACTIONS.md` 同步 Round 11 已展开状态。

### 35.3 验证

- `python3 -m py_compile rounds/round_11/**/exercises.py`（逐文件）：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。

### 35.4 风险边界核对

- 未改动 `rounds/round_00/` 与 `records/` 真实学习记录。

## 36. 2026-05-31 agent_gate 跳过卡点 + TASK-RR-16 Round 12

### 36.1 agent_gate

- `scripts/agent_gate.py` 新增 `SKIP_TASK_IDS`（RR-05/06/07/08，用户 2026-05-31 永久跳过）。
- `docs/AUTO_ADVANCE_PROTOCOL.md`、`docs/NEXT_ACTIONS.md` 同步 skipped 状态（非已完成核验/决策）。

### 36.2 Round 12

- 新增 `rounds/round_12/` 完整最小骨架。
- `CONVERSION_PROTOCOL.md`、`README.md` 同步 Round 12 已展开。

### 36.3 验证

- `python3 scripts/agent_gate.py --verify`：通过。
- `python3 -m py_compile rounds/round_12/**/exercises.py`（逐文件）：通过。

## 37. 2026-05-31 TASK-RR-17..25 Round 13–21 最小骨架

### 37.1 本轮新增

- 新增 `rounds/round_13/` … `rounds/round_21/` 最小骨架（`scripts/scaffold_round_skeleton.py` 生成）。
- 工程实操线 Round 00–21 概览文档均已对应 `rounds/round_XX/` 目录。

### 37.2 验证

- `python3 scripts/agent_gate.py --verify`：通过。
- Round 13–21 Python 练习脚本 `py_compile`：通过。

## 38. 2026-06-15 TASK-RR-26 Round 05 接入进度系统

### 38.1 本轮修改

- `progress.json`：新增 Round 05 的 `r05-*` 任务 ID（12 项，lane=`engineering`）。
- `progress.html`：新增 Round 05 面板与任务元数据。
- `rounds/round_05/*/exercises.sh` 与 `final/comprehensive_exercise.sh`：接入 `mark_done.sh` 自动打卡。
- `README.md`：区分「实操目录已展开」与「进度看板已接入」范围。

### 38.2 验证

- `bash -n rounds/round_05/**/exercises.sh` 与 `final/comprehensive_exercise.sh`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。
- `bash mark_done.sh`：可识别 `r05-*` 任务。

## 39. 2026-07-04 Web UI 用户闭环测试与修复

### 39.1 本轮新增

- 新增 `docs/reports/WEB_UI_USER_TEST_2026_07_04.md`，记录用户视角 before / after 测试、问题清单、修复项与验证命令。
- 新增 Web UI 事件历史接口：`GET /api/events`。
- 新增 Web UI “继续学习”入口与每任务“记录”入口。

### 39.2 本轮修改

- `progress.html`：从“统计优先”调整为“继续学习优先”；移动端任务行改为可换行网格；浅色工作台视觉替代旧暗色重卡片；关键脚本加版本查询串避免缓存旧逻辑。
- `progress_ui.js`：重写轻量阅读器，支持 Markdown 标题、引用、列表、表格、代码块、链接；支持 `.sh` / `.py` 脚本在页内以代码块阅读；完成 / 撤销按钮只绑定 `data-action`；记录弹窗支持备注与证据路径。
- `scripts/progress_lib.py`：`mark_task()` 写入动作后自动重建 task feedback；新增事件读取、事件分组、反馈生成公共函数。
- `scripts/progress_server.py`：新增事件 API；完成 / 撤销接口支持 JSON body 中的 `note` 与 `evidence_path`。
- `scripts/generate_task_feedback.py`：复用 `progress_lib.py` 的反馈生成逻辑。
- `scripts/build_rounds_data.py`：补齐 Round 02 的真实任务结构，避免 `progress.json` 中存在 UI 不可见任务。
- `progress.json`：删除两个无脚本、无事件、由旧通用生成器留下的冗余 Round 02 任务（`r02-w2-ex2`、`r02-w3-ex3`）。
- `rounds/round_06/*/exercises.sh` 与 `final/comprehensive_exercise.sh`：接入 `mark_done.sh` 自动打卡，完成 TASK-RR-27 的实际落地。

### 39.3 验证

- `npm run check:mcp`：通过。
- `npm run check:cursor-mcp`：CLI 层可列出 chrome-devtools / playwright 等工具；filesystem 在 Cursor 侧仍显示需审批，但当前 Codex 线程使用本地文件与 Playwright/浏览器能力完成验证。
- `python3 scripts/build_rounds_data.py`：通过，`rounds_data.js` 与 `progress.json` 任务集合对齐。
- `python3 scripts/generate_task_feedback.py`：通过。
- `python3 scripts/validate_learning_data.py`：通过。
- `python3 scripts/check_protocol_sync.py`：通过。
- `python3 -m json.tool progress.json`：通过。
- `python3 -m json.tool records/feedback/task_feedback.json`：通过。
- `node --check progress_ui.js`：通过。
- `python3 -m py_compile scripts/progress_lib.py scripts/progress_server.py scripts/generate_task_feedback.py scripts/mark_done_cli.py scripts/sync_progress_data.py scripts/build_rounds_data.py`：通过。
- 真实浏览器测试：桌面端可打开学习资料、练习脚本、记录弹窗；完成 / 撤销链路可写入并恢复；390px 移动端无横向溢出。

### 39.4 风险边界核对

- 本轮 UI 回归测试产生的临时事件已从 `records/action_logs/events.jsonl` 清理。
- 未删除已有 2026-06-15 事件日志。
- 未引入数据库、后端框架或大型新依赖；仍保持本地 JSON + 轻量 Python server。

## 40. 2026-07-04 Web UI Figma 视觉重设计

### 40.1 本轮新增

- 新建 Figma 设计稿：<https://www.figma.com/design/SYls2yaG0D7EEAJGvrcZUd>。
- 在 `docs/reports/WEB_UI_USER_TEST_2026_07_04.md` 追加 Figma 视觉重设计补测记录。

### 40.2 本轮修改

- `progress.html`：按 Figma 稿加入左侧学习导航轨；首屏改为“今日学习”工作区；“继续学习”卡片升级为下一步任务主行动；主线指标、阶段、薄弱项和 Round 清单重新分层；移动端修复整页横向滚动。
- `progress_ui.js`：移除 API 成功横幅里的符号化状态前缀，统一为克制的文字状态。

### 40.3 验证

- 真实浏览器 before / after 检查：桌面端 1280px 和移动端 390px 均无整页横向溢出。
- 真实浏览器交互冒烟：继续学习卡片中的“阅读资料”和“记录”弹窗均可正常打开；当前 URL 无 console error。
- 本轮未点击“完成”按钮，未写入真实学习记录。

### 40.4 风险边界核对

- 未改动 `records/` 下真实学习记录。
- 未引入前端框架、数据库、后端服务或大型新依赖。

## 41. 2026-07-04 Web UI 存档与读档

### 41.1 本轮新增

- `records/saves/README.md`：说明 Web UI 学习进度快照目录。
- `scripts/progress_lib.py`：新增本地快照创建、列表、读档恢复、读档前自动恢复点等公共函数。
- `scripts/progress_server.py`：新增 `GET /api/saves`、`POST /api/saves`、`POST /api/saves/<save_id>/load`。
- `progress.html`：新增“存档与读档”导航入口与操作卡片。

### 41.2 本轮修改

- `README.md`：同步 Web UI 支持存档/读档，并说明读档前自动创建恢复点。
- `docs/reports/WEB_UI_USER_TEST_2026_07_04.md`：追加存档与读档补测记录。

### 41.3 验证

- API 验证：创建测试存档、读档恢复、自动恢复点创建均通过；测试快照含 286 个任务、7 条动作记录。
- 真实浏览器测试：用户可在 Web UI 输入存档备注、点击创建存档、从列表点击读档并确认；读档后恢复点显示正常。
- 桌面端 1280px 与移动端 390px 均无整页横向溢出；当前 URL 无 console error。

### 41.4 风险边界核对

- 本轮 API/UI 测试产生的 `codex-*test-save` 临时快照已删除。
- 未删除 `records/action_logs/events.jsonl` 中已有真实动作记录。
- 未引入数据库、前端框架、后端框架或大型新依赖。

## 42. 2026-07-04 Web UI 练习执行与浏览器终端

### 42.1 本轮新增

- `scripts/progress_lib.py`：新增白名单练习脚本执行、输出摘要、`run_exercise` 动作事件、浏览器终端沙盒命令执行与命令历史记录。
- `scripts/progress_server.py`：新增 `POST /api/tasks/<id>/run`、`GET /api/terminal`、`POST /api/terminal/run`。
- `progress.html`：练习任务新增“运行”按钮；新增“练习终端”卡片与导航入口。
- `progress_ui.js`：新增运行确认、运行结果弹窗、终端输入输出渲染、清屏和回到 `~/cli-lab`。
- `records/terminal/README.md`：说明 Web UI 终端历史记录。

### 42.2 安全边界

- 任务脚本执行只允许 `rounds_data.js` 已登记任务对应的 `rounds/round_XX/weekN|final/(exercises|comprehensive_exercise).sh|py`。
- 任务脚本工作目录固定为 `~/cli-lab/roundN`，超时 20 秒。
- 浏览器终端工作目录限制在 `~/cli-lab` 内，命令白名单 + 危险模式拦截，超时 10 秒。
- 浏览器终端不允许真实远程操作、网络拉取、仓库外绝对路径和 `..` 路径。

### 42.3 验证

- API 验证：`POST /api/tasks/r07-w1-ex1/run` 可运行白名单 Python 练习脚本并返回输出摘要；`POST /api/terminal/run` 可执行 `pwd`、`cd`、管道类命令；`cat /etc/passwd` 被拦截。
- 存档验证：创建临时存档时，摘要包含 `terminal_command_count`；临时存档与测试命令历史已清理。
- 真实浏览器测试：桌面端可见“练习终端”卡片；在 UI 输入 `pwd` 能返回 `/Users/alalapi/cli-lab`；输入 `cat /etc/passwd` 会在 UI 中显示 `terminal_command_blocked`；桌面端无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、`generate_task_feedback.py`、`validate_learning_data.py`、`check_protocol_sync.py`、`agent_gate.py --verify`、`node --check progress_ui.js`、Python 编译、JSON 校验均通过。

### 42.4 风险边界核对

- 未引入数据库、前端框架、后端框架或大型新依赖。
- 未扩大到 VPS / SSH / 远程服务器执行。

## 43. 2026-07-04 TASK-RR-31 Round 01 内容填充与 UI 可完成性

### 43.1 本轮修改

- `rounds/round_01/README.md`：从“最小骨架”更新为 Web UI 可练习说明，明确阅读、运行、自测、最终验收的页面操作路径。
- `rounds/round_01/week1|week2|week3/notes.md`：补齐路径感、文件操作、文本查看与查帮助的可执行学习步骤、自测标准和终端练习边界。
- `rounds/round_01/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh`：移除 `read` 等待与自测 / 小抄 / 验收连带打卡，只自动记录脚本实际完成的练习任务。
- `rounds/round_01/final/command_cheatsheet.md`：补齐删除前检查、常用命令解释和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 01 UI 任务标题从“练习1/2/3”改为用户能理解的动作标题。
- `scripts/progress_lib.py`：浏览器终端允许在 `~/cli-lab` 沙盒内执行普通 `rm <file>`、`less`、`man`；`less/man` 使用捕获输出模式；继续拦截 `rm -r/-f`、通配符、家目录、命令串联符、绝对路径和仓库外路径。

### 43.2 用户视角问题修复

- Round 01 原 UI 任务标题过泛，用户不知道每个练习要做什么。
- Round 01 脚本原先会等待回车并连带标记自测 / 小抄 / 验收，不适合浏览器一键运行。
- Round 01 文件删除练习与浏览器终端全量禁用 `rm` 冲突，导致无法只通过 Web UI 完成练习。
- Round 01 文本查看练习需要 `less` / `man`，但浏览器终端白名单与“按 q 退出”文案不匹配。
- Round 01 笔记过短，缺少“在 Web UI 中怎么完成”的说明。

### 43.3 验证

- `python3 scripts/build_rounds_data.py`：通过，未新增任务，Round 01 标题已同步到 `rounds_data.js`。
- `rg` 检查：Round 01 脚本中不存在 `read` 等待和自测 / 小抄 / 验收连带打卡。
- API / 函数验证：`POST /api/tasks/r01-w2-ex2/run` 返回成功，输出提示用户手动标记自测；浏览器终端允许 `rm round1_api_rm_test/delete_me.txt`、`less`、`man` 捕获输出，拦截 `rm -rf`、`rm *`、`rm ~/x`、`ls; pwd`、`man -P cat ls`、`less +...`、`less -...`、`sh -c` 和 `bash -c`。
- 真实浏览器验证：Round 01 可展开，专用任务标题可见；Week 1 notes 可在弹窗打开，包含 Web UI 步骤、命令块和自测说明；桌面端无横向溢出。
- 静态与数据验证：`generate_task_feedback.py`、`check_protocol_sync.py`、`validate_learning_data.py`、`agent_gate.py --verify`、`bash -n`、`node --check progress_ui.js`、Python 编译、JSON 校验均通过。
- MCP 验证：`npm run check:mcp` 通过；`npm run check:cursor-mcp` 可在 CLI 层列出 chrome-devtools / playwright / context7 / github / stitch 等工具，同时仍提示当前 Cursor 侧 server approval 状态需在 Cursor 设置中处理。

## 44. 2026-07-04 TASK-RR-32 Round 02 内容填充与任务绑定终端

### 44.1 本轮修改

- 新建 Figma 设计稿：<https://www.figma.com/design/gmSFWf3hylozNlXIlHIJAR>，用于“任务区 + 映射终端”工作台布局参考。
- `rounds/round_02/README.md`、`week1|week2|week3/notes.md`、`final/command_cheatsheet.md`：补齐 Web UI 学习路径、重定向 / 管道 / Shell 脚本 / 本地 Git 最小流程、自测标准和安全边界。
- `rounds/round_02/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh`：改为非交互运行，只自动打卡脚本实际完成的练习；自测、小抄和验收仍由用户手动记录。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 02 任务标题改为动作化标题。
- `progress.html` / `progress_ui.js`：终端卡片升级为“当前任务 + 工作目录 + 快捷命令 + 控制台”的浏览器映射工作区；工程实操练习 / 自测 / 产出任务新增“终端”按钮，可一键绑定到对应 `~/cli-lab/roundN`。
- `scripts/progress_lib.py` / `scripts/progress_server.py`：终端命令日志新增 `task_id`；任务脚本“运行”按钮仅允许 `exercise` 类型，防止自测 / 验收被误自动运行。
- `records/terminal/README.md`：同步终端映射边界与 `task_id` 字段说明。

### 44.2 用户视角问题修复

- Round 02 原脚本含 `read` 等待，并会连带标记自测 / 小抄 / 验收，不适合浏览器运行闭环。
- Round 02 自测任务原先因 `.sh` 文件也显示“运行”，会误导用户以为系统能替自己完成自测。
- 终端原先只是页面底部工具，不知道当前任务是谁；用户需要自己判断该进入哪个 `~/cli-lab/roundN`。
- 本地 Git 练习需要在浏览器终端完成，但 UI 没有任务级入口和日志关联。

### 44.3 验证

- Figma：已创建并生成“任务列表 + 映射终端”桌面工作台设计稿。
- API 验证：`/api/terminal?cwd=~/round2` 返回 `~/round2`；`POST /api/terminal/run` 执行 `pwd` 成功，命令日志写入 `task_id=r02-w1-ex1`；`POST /api/tasks/r02-w1-self/run` 返回 `task_not_runnable`。
- 真实浏览器验证：Chrome 前台页面可展开 Round 02；练习任务显示“运行 / 终端 / 记录 / 完成”；点击“终端”后页面滚到练习终端，当前任务绑定为“练习：覆盖与追加”，工作目录显示 `~/round2`；在 UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round2`。
- 静态语义验证：101 个脚本型 `exercise` 任务可显示运行入口；66 个脚本型非 `exercise` 任务不显示运行入口。
- 清理：本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。

### 44.4 风险边界核对

- 未放宽终端沙盒：仍限制在 `~/cli-lab` 内，远程 Git、网络命令、危险删除、命令串联和仓库外路径继续拦截。
- 未引入前端框架、数据库、后端框架或大型新依赖。

## 45. 2026-07-04 TASK-RR-33 Round 03 内容填充与 Python 基础练习

### 45.1 本轮修改

- `rounds/round_03/README.md`：从“最小骨架”更新为 Web UI 可练习说明，明确阅读、运行、自测、最终验收的页面操作路径。
- `rounds/round_03/week1|week2|week3/notes.md`：补齐 Python 基础语法、list/dict、函数拆分与复杂度直觉的学习步骤、自测命令和完成标准。
- `rounds/round_03/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh`：改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动记录。
- `rounds/round_03/final/complexity_cheatsheet.md`：补齐 Python 基础、复杂度判断和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 03 UI 任务标题从“练习1/2/3”改为用户能理解的动作标题。
- `progress.html`：新增 URL 初始路由解析，支持 `?round=round_03`、`?round03=1` 等直达 Round 参数。

### 45.2 用户视角问题修复

- Round 03 原 notes 过短，用户不知道如何只通过 Web UI 完成 Python 文件创建、运行和解释。
- Round 03 原脚本会等待回车并可能连带标记自测 / 小抄 / 验收，不适合浏览器运行闭环。
- Round 03 任务标题过泛，用户无法从 UI 判断每个练习的具体产出。
- 报告或外部链接中的 Round 直达参数原先不会切换 active Round，用户打开后仍落在默认 Round。

### 45.3 验证

- API 验证：`r03-w1-ex1`、`r03-w2-ex2`、`r03-w3-ex3`、`r03-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r03-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round3` 返回 `~/round3`；终端可在任务 `r03-w1-self` 下写入并运行 `hello.py`；`python3 -c` 仍被拦截。
- 真实浏览器验证：`progress.html?round=round_03` 会直接选中 Round 03；自测任务不显示“运行”但显示“终端”；点击“终端”后当前任务绑定为“自测：自己写 square.py”，工作目录为 `~/round3`；UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round3`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、`generate_task_feedback.py`、`check_protocol_sync.py`、`validate_learning_data.py`、`agent_gate.py --verify`、`bash -n`、`node --check progress_ui.js`、Python 编译、JSON 校验、`git diff --check` 均通过。
- MCP 验证：`npm run check:mcp` 通过；`npm run check:cursor-mcp` 可在 CLI 层列出 chrome-devtools / playwright / context7 / github / stitch 等工具，filesystem 仍显示 Cursor 侧需审批。

### 45.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未放宽终端沙盒边界；仍限制在 `~/cli-lab` 内并拦截危险命令。
- 未引入前端框架、数据库、后端框架或大型新依赖。

## 46. 2026-07-04 TASK-RR-34 Round 04 内容填充与核心数据结构练习

### 46.1 本轮修改

- `rounds/round_04/README.md`：从“最小骨架”更新为 Web UI 可练习说明，明确阅读、运行、自测、最终验收的页面操作路径。
- `rounds/round_04/week1|week2|week3/notes.md`：补齐 list、stack/queue、dict/set 的学习步骤、自测命令、场景直觉和完成标准。
- `rounds/round_04/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh`：改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动记录。
- `rounds/round_04/final/complexity_cheatsheet.md`：补齐核心数据结构小抄、选择口诀和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 04 UI 任务标题从“练习1/2/3”改为用户能理解的动作标题。

### 46.2 用户视角问题修复

- Round 04 原 notes 太短，用户不知道如何只通过 Web UI 完成数据结构练习。
- Round 04 原脚本会等待回车并连带标记自测 / 小抄 / 验收，不适合浏览器运行闭环。
- Round 04 原任务标题过泛，用户无法从 UI 判断 list、stack/queue、dict/set 分别要练什么。

### 46.3 验证

- API 验证：`r04-w1-ex1`、`r04-w2-ex2`、`r04-w3-ex3`、`r04-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r04-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round4` 返回 `~/round4`；终端可在任务 `r04-w1-self` 下写入并运行 `scores.py`；`python3 -c` 仍被拦截。
- 真实浏览器验证：`progress.html?round=round_04` 会直接选中 Round 04；自测任务不显示“运行”但显示“终端”；点击“终端”后当前任务绑定为“自测：自己写 scores.py”，工作目录为 `~/round4`；UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round4`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、`generate_task_feedback.py`、`check_protocol_sync.py`、`validate_learning_data.py`、`agent_gate.py --verify`、`bash -n`、`node --check progress_ui.js`、Python 编译、JSON 校验、`git diff --check` 均通过。
- MCP 验证：`npm run check:mcp` 通过；`npm run check:cursor-mcp` 可在 CLI 层列出 chrome-devtools / playwright / context7 / github / stitch 等工具，filesystem 仍显示 Cursor 侧需审批。

### 46.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未放宽终端沙盒边界；仍限制在 `~/cli-lab` 内并拦截危险命令。
- 未引入前端框架、数据库、后端框架或大型新依赖。

## 47. 2026-07-04 TASK-RR-35 Round 05 内容填充与算法模式练习

### 47.1 本轮修改

- `rounds/round_05/README.md`：从“最小骨架 / 已接入进度”更新为 Web UI 可练习说明，明确阅读、运行、自测、最终验收的页面操作路径。
- `rounds/round_05/week1|week2|week3/notes.md`：补齐二分、滑动窗口、双指针、DFS/BFS、回溯、贪心和 DP 的学习步骤、自测命令、场景直觉和完成标准。
- `rounds/round_05/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh`：改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动记录。
- `rounds/round_05/final/algorithm_patterns_cheatsheet.md`：补齐算法模式选择小抄、触发条件和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 05 UI 任务标题从“练习1 / 练习2 / 练习3”改为用户能理解的动作标题。

### 47.2 用户视角问题修复

- Round 05 原 notes 太短，用户不知道如何只通过 Web UI 完成算法模式练习。
- Round 05 原脚本会等待回车并连带标记自测 / 小抄 / 验收，不适合浏览器一键运行。
- Round 05 原任务标题过泛，用户无法从 UI 判断二分、图搜索、贪心和 DP 分别要练什么。
- 算法自测需要用户自己在终端写 Python 文件，已通过浏览器映射终端绑定到 `~/cli-lab/round5`，命令日志带 `task_id`，但不自动等同于任务完成。

### 47.3 验证

- API 验证：`r05-w1-ex1`、`r05-w2-ex2`、`r05-w3-ex3`、`r05-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r05-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round5` 返回 `~/round5`；终端可在任务 `r05-w1-self` 下写入并运行 Python 文件；危险的 `python3 -c` 仍被拦截。
- 真实浏览器验证：`progress.html?round=round_05` 会直接选中 Round 05；自测任务不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 two_sum_sorted.py”，工作目录为 `~/round5`；UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round5`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、`check_protocol_sync.py`、`validate_learning_data.py`、`agent_gate.py --verify`、`bash -n`、`node --check progress_ui.js`、Python 编译、JSON 校验、`git diff --check` 均通过。

### 47.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未放宽终端沙盒边界；仍限制在 `~/cli-lab` 内并拦截危险命令。
- 未引入前端框架、数据库、后端框架或大型新依赖。

## 48. 2026-07-04 TASK-RR-36 Web UI 文档外链跳转

### 48.1 本轮修改

- `progress_ui.js`：Markdown 阅读器的 `inlineMarkdown()` 新增 `[标题](https://...)` 外链渲染支持。
- 外链渲染为新标签页打开，并带 `rel="noreferrer noopener"`。

### 48.2 用户视角问题修复

- 用户在 Web UI 中阅读 `round_05.md` 等总计划文档时，外部学习资源原先只是 Markdown 文本，不便直接跳转。
- 修复后，`Hello Algo`、`VisuAlgo`、Khan Academy 等外部资源可以在阅读弹窗中直接点击打开。

### 48.3 验证

- `node --check progress_ui.js`：通过。
- 真实浏览器验证：打开 `progress.html?round=round_05`，在阅读器中打开 `round_05.md`，确认 `Hello Algo` 链接存在、显示文本正确、`target="_blank"` 且包含 `noreferrer noopener`；页面中共识别到 5 个 `https://` 外部链接。

### 48.4 风险边界核对

- 本轮只修改前端阅读器链接渲染逻辑，未写入任何学习记录。
- 未引入前端框架、数据库、后端框架或大型新依赖。

## 49. 2026-07-04 TASK-RR-37 Round 06 内容填充与 Linux 自动化练习

### 49.1 本轮修改

- `rounds/round_06/README.md`：从“最小实操骨架”更新为 Web UI 可练习说明，明确阅读、运行、自测、最终验收的页面操作路径。
- `rounds/round_06/week1|week2|week3/notes.md`：补齐 find/xargs/sed/awk、进程查看、长任务保活、SSH/rsync/crontab 命令排练的学习步骤、自测命令、场景直觉和完成标准。
- `rounds/round_06/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh`：改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动记录。
- `rounds/round_06/final/linux_automation_cheatsheet.md`：补齐 Linux 自动化命令小抄、Web UI 安全边界和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 06 UI 任务标题从“练习1 / 练习2 / 练习3”改为用户能理解的动作标题。
- `scripts/progress_lib.py` / `records/terminal/README.md`：浏览器终端允许只读 `ps` 进程查看，继续拦截真实远程和网络命令。

### 49.2 用户视角问题修复

- Round 06 原 notes 太短，用户不知道如何只通过 Web UI 完成 Linux 自动化练习。
- Round 06 原脚本会等待回车并连带标记自测 / 小抄 / 验收，不适合浏览器一键运行。
- Round 06 原任务标题过泛，用户无法从 UI 判断 find/xargs、进程查看、远程排练分别要练什么。
- Round 06 涉及 `ssh`、`rsync`、`crontab` 等高风险命令，已改为 Web UI 内命令排练和计划文件，不执行真实远程操作。

### 49.3 验证

- API 验证：`r06-w1-ex1`、`r06-w2-ex2`、`r06-w3-ex3`、`r06-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r06-w2-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round6` 返回 `~/round6`；终端允许在任务 `r06-w2-self` 下执行 `ps aux | grep python | head -1`；`ssh user@host` 返回 `terminal_command_blocked`。
- 真实浏览器验证：`progress.html?round=round_06` 会直接选中 Round 06；自测任务不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 worker_monitor.sh”，工作目录为 `~/round6`；`round_06.md` 中 MIT Missing Semester 外链可在阅读器中点击并新标签页打开。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、`bash -n`、`rg` 残留误打卡检查均通过。

### 49.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未放宽真实远程操作边界；`ssh` / `scp` / `rsync` / 网络命令仍被浏览器终端拦截。
- 未引入前端框架、数据库、后端框架或大型新依赖。

## 50. 2026-07-04 TASK-RR-38 Round 07 内容填充与 AI 数据预处理练习

### 50.1 本轮修改

- `rounds/round_07/README.md`：从“最小实操骨架”更新为 Web UI 可练习说明，明确阅读、自动运行、终端自测、小抄和验收的页面操作路径。
- `rounds/round_07/week1|week2|week3/notes.md`：补齐 pathlib、多格式读写、argparse、logging、去重统计、函数拆分的学习步骤、自测命令和完成标准。
- `rounds/round_07/week1|week2|week3/exercises.py`：改为默认可非交互运行，自动生成演示输入、输出结果和下一步提示，只自动记录对应练习任务。
- `rounds/round_07/final/comprehensive_exercise.py`：改为 Web UI 默认可运行的 AI 数据预处理小工具，支持 `txt/csv/json/jsonl`、`--dedup`、`--keep-duplicates`、日志和 summary 输出，只自动记录 `r07-fin-comp`。
- `rounds/round_07/final/ai_prep_tool_cheatsheet.md`：补齐 Web UI 完成路径、参数、格式读取小抄和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 07 UI 任务标题从“练习1 / 练习2 / 练习3”改为用户能理解的动作标题。

### 50.2 用户视角问题修复

- Round 07 原 notes 太短，用户不知道如何只通过 Web UI 完成 Python 数据预处理练习。
- Week 2 / Final 原脚本默认要求 `--input` 参数，在 Web UI “运行”按钮下会失败。
- Round 07 原任务标题过泛，用户无法从 UI 判断分别要练多格式读取、参数日志还是整合工具。
- 自动脚本现在只标记实际完成的练习任务；自测、小抄和验收仍需用户自己阅读、手写、解释并手动记录。

### 50.3 验证

- API 验证：`r07-w1-ex1`、`r07-w2-ex2`、`r07-w3-ex3`、`r07-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r07-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round7` 返回 `~/round7`；终端可在任务 `r07-w1-self` 下写入并运行 `read_formats.py`；`python3 -c` 仍返回 `terminal_command_blocked`。
- 真实浏览器验证：`progress.html?round=round_07` 会直接选中 Round 07；`r07-w1-ex1` 显示“运行”，`r07-w1-self` 不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 read_formats.py”，工作目录为 `~/round7`。
- 外链验证：在阅读器中打开 `round_07.md`，Python argparse 官方文档链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、Python 语法编译、自动打卡目标检查均通过。

### 50.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未放宽浏览器终端高风险命令边界；`python3 -c` 仍被拦截。
- 未引入前端框架、数据库、后端框架或大型新依赖。

## 51. 2026-07-04 TASK-RR-39 Round 08 内容填充与升级路线收口练习

### 51.1 本轮修改

- `rounds/round_08/README.md`：从“最小实操骨架”更新为 Web UI 可练习说明，明确阅读、自动运行、终端自测、小抄和验收的页面操作路径。
- `rounds/round_08/week1|week2|week3/notes.md`：补齐项目收口、最小测试、sqlite3 运行历史、服务化接口形状的学习步骤、自测命令和完成标准。
- `rounds/round_08/week1|week2|week3/exercises.py`：改为默认可非交互运行，自动生成项目骨架、测试报告、SQLite 数据库、API 合同和下一步提示，只自动记录对应练习任务。
- `rounds/round_08/final/comprehensive_exercise.py`：改为 Web UI 默认可运行的 Round 00-08 收口检查，汇总项目结构、测试、SQLite 和 API 合同结果，只自动记录 `r08-fin-comp`。
- `rounds/round_08/final/upgrade_route_cheatsheet.md`：补齐 Web UI 完成路径、路线 A/B/C 选择标准和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 08 UI 任务标题从“练习1 / 练习2 / 练习3”改为用户能理解的动作标题。

### 51.2 用户视角问题修复

- Round 08 原 notes 太短，用户不知道如何只通过 Web UI 完成项目收口、测试、SQLite 和接口形状排练。
- Round 08 原脚本未接入自动记录，Web UI “运行”后不会推进对应练习状态。
- Round 08 原任务标题过泛，用户无法从 UI 判断分别要练项目收口、sqlite3 还是服务化接口。
- 本轮明确不在仓库中安装 pytest / FastAPI / uvicorn，也不启动真实后端服务；服务化先做标准库接口合同排练。

### 51.3 验证

- API 验证：`r08-w1-ex1`、`r08-w2-ex2`、`r08-w3-ex3`、`r08-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r08-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round8` 返回 `~/round8`；终端可在任务 `r08-w3-self` 下写入并运行 `api_contract.py`；`pip install fastapi` 返回 `terminal_command_not_allowed:pip`。
- 真实浏览器验证：`progress.html?round=round_08` 会直接选中 Round 08；`r08-w1-ex1` 显示“运行”，`r08-w1-self` 不显示“运行”但显示“终端”；点击后当前任务为“自测：自己写 test_basic.py”，工作目录为 `~/round8`。
- 外链验证：在阅读器中打开 `round_08.md`，pytest 官方文档链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、Python 语法编译、自动打卡目标检查均通过。

### 51.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未引入大型新依赖；未创建新的真实后端服务；FastAPI 只作为后续路线说明和接口形状排练。
- 未放宽浏览器终端高风险命令边界。

## 52. 2026-07-04 TASK-RR-40 Round 09 内容填充与仓库测试练习

### 52.1 本轮修改

- `rounds/round_09/README.md`：从“最小实操骨架”更新为 Web UI 可练习说明，明确阅读、自动运行、终端自测、小抄和验收的页面操作路径。
- `rounds/round_09/week1|week2|week3/notes.md`：补齐 README/.gitignore、feature/hotfix 本地分支、纯函数与 pytest 风格测试的学习步骤、自测命令和完成标准。
- `rounds/round_09/week1|week2|week3/exercises.py`：改为默认可非交互运行，自动生成规范化项目、本地 Git 工作流沙盒、测试样例和下一步提示，只自动记录对应练习任务。
- `rounds/round_09/final/comprehensive_exercise.py`：改为 Web UI 默认可运行的 Round 09 收口检查，汇总项目结构、本地 Git 工作流和测试结果，只自动记录 `r09-fin-comp`。
- `rounds/round_09/final/repo_testing_cheatsheet.md`：补齐 Web UI 完成路径、仓库规范化与测试小抄、最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 09 UI 任务标题从“练习1 / 练习2 / 练习3”改为用户能理解的动作标题。

### 52.2 用户视角问题修复

- Round 09 原 notes 太短，用户不知道如何只通过 Web UI 完成仓库结构、README/.gitignore、本地 Git 分支和测试练习。
- Round 09 原脚本只是生成少量文件或打印建议命令，没有形成 Web UI 一键运行后的可检查产物与自动记录。
- Round 09 原任务标题过泛，用户无法从 UI 判断分别要练仓库规范化、本地分支合并还是纯函数测试。
- 本轮明确不安装 pytest、不执行 GitHub remote 操作；Git 练习只在 `~/cli-lab/round9` 本地沙盒仓库内完成。

### 52.3 验证

- API 验证：`r09-w1-ex1`、`r09-w2-ex2`、`r09-w3-ex3`、`r09-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r09-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round9` 返回 `~/round9`；终端 API 可在任务 `r09-w2-self` 下完成本地 `git init`、`git commit`、`git log`；`git push origin main` 返回 `terminal_command_blocked`。
- 真实浏览器验证：`progress.html?round=round_09` 会直接选中 Round 09；`r09-w1-ex1` 显示“运行”，`r09-w1-self` 不显示“运行”但显示“终端”；点击后终端工作目录为 `~/round9`，UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round9`。
- 文档阅读与外链验证：Week 1 notes 可在阅读器中直接阅读；`round_09.md` 中 pytest 官方文档链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、Python 语法编译、自动打卡目标检查均通过。

### 52.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未引入大型新依赖；未安装 pytest；未执行 GitHub 远程 Git 操作。
- 未放宽浏览器终端高风险命令边界；`git push` 仍被拦截。

## 53. 2026-07-04 TASK-RR-41 Round 10 内容填充与 Python 工程化练习

### 53.1 本轮修改

- `rounds/round_10/README.md`：从“最小实操骨架”更新为 Web UI 可练习说明，明确阅读、自动运行、终端自测、小抄和验收的页面操作路径。
- `rounds/round_10/week1|week2|week3/notes.md`：补齐 CLI / core / IO 拆分、config.ini / logging、可控错误与入口规范的学习步骤、自测命令和完成标准。
- `rounds/round_10/week1|week2|week3/exercises.py`：改为默认可非交互运行，自动生成工程化沙盒项目、配置、日志、错误路径报告和下一步提示，只自动记录对应练习任务。
- `rounds/round_10/final/comprehensive_exercise.py`：改为 Web UI 默认可运行的 Round 10 收口检查，生成完整 `ai_prep_tool` 小项目并验证成功路径、缺失输入错误路径、日志和 summary，只自动记录 `r10-fin-comp`。
- `rounds/round_10/final/python_engineering_cheatsheet.md`：补齐 Web UI 完成路径、文件职责表、配置日志口诀、错误处理口诀和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 10 UI 任务标题从“练习1 / 练习2 / 练习3”改为用户能理解的动作标题。

### 53.2 用户视角问题修复

- Round 10 原 notes 太短，用户不知道如何只通过 Web UI 完成模块拆分、配置日志和错误处理练习。
- Round 10 原脚本只是生成骨架或跑内存自检，没有形成 Web UI 一键运行后的可检查产物与自动记录。
- Round 10 原任务标题过泛，用户无法从 UI 判断分别要练 CLI 拆分、配置日志还是入口错误处理。
- 本轮明确不安装第三方依赖、不切换到 `src/` layout、不做打包发布；先把 Python 工程化的最小职责边界跑通。

### 53.3 验证

- API 验证：`r10-w1-ex1`、`r10-w2-ex2`、`r10-w3-ex3`、`r10-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r10-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round10` 返回 `~/round10`；终端 API 可在任务 `r10-w3-self` 下写入入口脚本并看到返回码 2；`python3 -c` 返回 `terminal_command_blocked`。
- 真实浏览器验证：`progress.html?round=round_10` 会直接选中 Round 10；`r10-w1-ex1` 显示“运行”，`r10-w1-self` 不显示“运行”但显示“终端”；点击后终端工作目录为 `~/round10`，UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round10`。
- 文档阅读与外链验证：Week 1 notes 可在阅读器中直接阅读；`round_10.md` 中 Python argparse 官方文档链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、Python 语法编译、自动打卡目标检查均通过。

### 53.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未引入大型新依赖；未安装第三方包；未做打包发布或 layout 迁移。
- 未放宽浏览器终端高风险命令边界；`python3 -c` 仍被拦截。

## 54. 2026-07-04 TASK-RR-42 Round 11 内容填充与 SQLite 持久化练习

### 54.1 本轮修改

- `rounds/round_11/README.md`：从“最小实操骨架”更新为 Web UI 可练习说明，明确阅读、自动运行、终端自测、小抄和验收的页面操作路径。
- `rounds/round_11/week1|week2|week3/notes.md`：补齐 SQLite 建表、参数化插入、`db.py` 查询封装、主工具写入运行历史的学习步骤、自测命令和完成标准。
- `rounds/round_11/week1|week2|week3/exercises.py`：改为默认可非交互运行，自动生成 `runs.db`、查询报告、持久化报告和下一步提示，只自动记录对应练习任务。
- `rounds/round_11/final/comprehensive_exercise.py`：改为 Web UI 默认可运行的 SQLite 运行历史收口检查，生成完整 `ai_prep_tool` 沙盒并验证 2 次运行历史、格式查询、处理总数和 `.gitignore` 边界，只自动记录 `r11-fin-comp`。
- `rounds/round_11/final/sqlite_persistence_cheatsheet.md`：补齐 Web UI 完成路径、表结构、参数化 SQL、`db.py` 职责和最终验收自问。
- `scripts/build_rounds_data.py` / `rounds_data.js`：将 Round 11 UI 任务标题从“练习1 / 练习2 / 练习3”改为用户能理解的动作标题。

### 54.2 用户视角问题修复

- Round 11 原 notes 太短，用户不知道如何只通过 Web UI 完成 SQLite 持久化练习。
- Round 11 原脚本只是生成少量文件或依赖前一周产物，没有形成 Web UI 一键运行后的稳定可检查产物与自动记录。
- Round 11 原任务标题过泛，用户无法从 UI 判断分别要练 `runs` 表、`db.py` 查询封装还是主工具运行历史。
- 本轮明确 `.db` 文件只写入 `~/cli-lab/round11` 沙盒，不把练习数据库提交进仓库；自动脚本只标记练习任务，自测、小抄和验收仍由用户自己阅读、手写、解释并手动记录。

### 54.3 验证

- API 验证：`r11-w1-ex1`、`r11-w2-ex2`、`r11-w3-ex3`、`r11-fin-comp` 均可通过 `/api/tasks/<id>/run` 运行成功；`r11-w1-self/run` 返回 `task_not_runnable`。
- 浏览器终端验证：`/api/terminal?cwd=~/round11` 返回 `~/round11`；终端 API 可在任务 `r11-w1-self` 下写入并运行 SQLite 脚本；`python3 -c` 返回 `terminal_command_blocked`。
- 真实浏览器验证：`progress.html?round=round_11` 会直接选中 Round 11；`r11-w1-ex1` 显示“运行”，`r11-w1-self` 不显示“运行”但显示“终端”；点击后终端工作目录为 `~/round11`，UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round11`。
- 文档阅读与外链验证：Week 1 notes 可在阅读器中直接阅读，包含 Web UI 学习路径；`round_11.md` 中 Python sqlite3 官方文档链接可被定位，`target="_blank"`，`rel` 包含 `noreferrer noopener`。
- 移动端验证：390px 宽度无整页横向溢出。
- 静态与数据验证：`build_rounds_data.py`、Python 语法编译、自动打卡目标检查均通过。

### 54.4 风险边界核对

- 本轮 API/UI 验证产生的进度、动作、反馈和终端历史均已从测试前快照恢复。
- 未引入大型新依赖；只使用 Python 标准库 `sqlite3`。
- 未把练习 `.db` 文件写入仓库；练习产物位于 `~/cli-lab/round11` 沙盒。

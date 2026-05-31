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

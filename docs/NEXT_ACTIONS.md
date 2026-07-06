# Next Actions

本文件是 Codex 后续自动推进的任务队列。每轮只允许选择一个任务推进，并在完成后同步更新本文件与 `docs/PROJECT_STATE.md`。

> **2026-05-12 路线重定向**：当前最高优先级是新建的 TASK-RR-XX 系列（路线重定向后的主任务队列）。
> 旧 TASK-002 ~ TASK-012（任务注册 / action log / 网页交互系统系列）已迁移到本文件末尾"历史任务（已归档 / 暂缓）"，按需重启。
> VPS 实操支线（TASK-VPS-XX）保持不变，可与主任务并行推进。

---

## TASK-RR-53：Web UI 总目标完成审计与计划入口补齐

- 状态：**done**（2026-07-05）
- 背景：用户要求优先确保功能稳定实现，用户可以只通过 Web UI 完成学习推进、记录、文档阅读、外部链接跳转、练习脚本运行、浏览器映射终端、存档读档。
- 目标：用用户视角审计 Web UI 核心闭环，确认 Round 00–21 工程实操线可运行，并把现有学习计划 / 支线文档全部接入页面阅读与记录。
- 实际产物：
  - `scripts/build_rounds_data.py` 新增 `plan_overview`、`plan_linux`、`plan_vps` 等阅读入口，并补齐软考 / 数学二主线 README。
  - `rounds_data.js` 注册 28 个 Web UI 分组、304 个任务，其中 101 个 exercise 任务仍可运行。
  - `progress.json` / `progress_data.js` / `records/feedback/task_feedback.json` 同步新增 18 个阅读任务。
  - 新增 `docs/reports/WEB_UI_COMPLETION_AUDIT_2026_07_05.md` 记录 API、存档读档、浏览器桌面/移动端和计划入口覆盖验证。
- 验收：所有任务文件引用存在；101 个 exercise 任务通过 `/api/tasks/<id>/run` 全量 API 验证；存档读档 API 验证通过；真实浏览器验证计划入口、Round 00、Round 21 和移动端无横向溢出。
- 风险边界：真实考试题目 / 最新大纲 / 院校数据仍必须以后续官方源为准；VPS Level 2+ 真实远程操作仍需用户授权。
- 是否需要用户介入：否。

---

## TASK-RR-54：Web UI 用户视角评测与学习工作区改版

- 状态：**done**（2026-07-06）
- 背景：用户反馈当前 UI 信息堆叠严重，教程弹窗与终端割裂，必须关闭教程才能操作，指引不够明确。
- 目标：按用户视角累计 5 个问题后停止评测、生成报告，并把首屏改成可同时读教程和敲命令的学习工作区。
- 实际产物：
  - `docs/reports/WEB_UI_USER_REVIEW_2026_07_06.md`：记录 5 个问题、修复方向和工具状态。
  - `progress.html`：新增“学习工作区”，把当前任务、内联教程和浏览器终端合并到首屏；配置 / 存档 / 阶段 / 薄弱项默认折叠到管理区。
  - `progress_ui.js`：教程默认在内联阅读器打开；`?round=round_XX` 和 Round 点击会驱动首屏任务；“终端练习”绑定任务后不再打开遮挡教程的弹窗。
  - `README.md`：日常使用说明改为“左侧确认任务 / 中间读教程 / 右侧终端练习 / 最后记录完成”。
- 验收：真实浏览器打开 `progress.html?round=round_02` 后首屏任务聚焦 Round 02；教程内联显示；终端输入框同屏可见；任务行无重复阅读入口；390px 移动端无横向溢出；当前 URL 无 console error。
- 风险边界：未修改 `records/` 下真实学习记录；未引入新依赖；未改变浏览器终端安全命令白名单。
- 是否需要用户介入：否。

---

## TASK-RR-55：Web UI 第二轮用户评测与首屏细节收紧

- 状态：**done**（2026-07-06）
- 背景：第一轮改版后继续评测，发现顶部仍占空间、状态横幅偏重、移动导航裁切、脚本按钮语义不准、终端绑定滚动不够稳定。
- 目标：第二轮累计 5 个新问题后生成报告，并继续修正首屏密度、按钮语义和移动端导航。
- 实际产物：
  - `docs/reports/WEB_UI_USER_REVIEW_2026_07_06_ROUND2.md`：记录第二轮 5 个问题和修复方向。
  - `progress.html`：压缩顶部说明和 API 成功横幅；移动端导航改为换行；学习工作区首屏更紧凑。
  - `progress_ui.js`：按文件类型显示“读教程 / 看脚本 / 打开资料”；终端绑定使用确定性滚动并避免聚焦触发额外滚动。
- 验收：桌面端 `progress.html?round=round_02` 当前任务、内联教程、终端输入框同屏可见；练习脚本任务显示“看脚本”；390px 移动端无横向溢出且导航不裁切。
- 是否需要用户介入：否。

---

## TASK-RR-00：路线重定向 + 治理 + 路线骨架 + 四主线进度

- 状态：**done**（2026-05-12 完成）
- 背景：仓库原目标是"网页交互式 AI 工程学习系统"，与用户实际中长期目标（软考 → 408/数学二/0854）不符。
- 目标：完成一次性的路线重定向 + 治理清理 + 多目标骨架 + 进度系统四主线扩展。
- 实际产物：
  - 删除 22 份 `plan_round_XX.txt`（用户授权清理）。
  - 大幅瘦身 `CONVERSION_PROTOCOL.md`（v1.3 → v2.0，移除 txt 转换流程）。
  - 治理文档清理：`docs/governance/repo_rules.md`、`docs/governance/file_naming_rules.md`、`docs/templates/repository_cleanup_confirmation.md`、`docs/checklists/repository_cleanup_checklist.md`、`rounds/stage_03_vps_remote_ops/round_vps_00/01` 内对 `plan_round_XX.txt` 的引用全部更新。
  - 新增 8 份路线骨架：`docs/MASTER_STUDY_ROADMAP.md` / `STAGE_PLAN.md` / `KNOWLEDGE_MAPPING.md` / `WEEKLY_EXECUTION_TEMPLATE.md` / `PROGRESS_RULES.md` / `ERROR_REVIEW_SYSTEM.md` / `GRADUATE_SCHOOL_TRACKER.md`（模板，无真实院校数据）/ `PROJECT_PORTFOLIO_TRACK.md`。
  - 新增审计报告：`docs/AUDIT_2026_05_12.md`。
  - 新增目录骨架：`plans/{linux,soft_exam,math2,408}/README.md`、`records/{weekly_reviews,error_notes,completed_tasks}/.gitkeep` + `records/README.md`。
  - 进度系统 v2 升级：`progress.json` 新增 `lanes` 顶层字段 + 每个 task 新增 `lane` 字段（Round 00 旧任务自动归 `engineering`）；`mark_done.sh` 兼容并按 lane 分组输出；`progress_data.js` 同步重写；`progress.html` 重写为"总进度 + 四主线 + 个人配置 + 阶段进度 + 薄弱项 + 按 lane 浏览 Round"。
  - 总入口更新：`README.md` 改写为路线总控；`AGENTS.md` 增加新核心文档为必读；`docs/CODEX_LONG_TERM_PLAN.md` 顶部增加 §0 重定向章节。
- 验收：`bash mark_done.sh` 仍可运行；`progress.json` 合法；Round 00 旧任务 ID 与原行为完全保留；progress.html JS 语法校验通过。
- 是否需要用户介入：本轮已由用户授权完成。

---

## TASK-RR-01：Stage 2 软考软件设计师知识体系拆解

- 状态：**done**（2026-05-28）
- 背景：路线重定向完成后，短期主推 lane 是 `soft_exam`。`plans/soft_exam/README.md` 列出了 12 个模块清单，但模块本身没有笔记骨架。
- 目标：为软考软件设计师建立第一份可推进的模块笔记骨架（按用户当前精力，**先做 3 个模块**：数据结构 / 操作系统 / 数据库），每份骨架仅含"章节列表 + 与 408 差异说明 + 引用最新官方大纲的提示"，**不缓存具体考点**。
- 要修改：新增 `plans/soft_exam/ds.md`、`plans/soft_exam/os.md`、`plans/soft_exam/db.md`。
- 不要修改：不要预写具体考题；不要复制教材整段；不要重新规划 Stage Plan。
- 验收标准：3 份文件存在；每份顶部有"⚠ 最新大纲见官方"提示；列出建议章节清单与 408 差异。
- 风险：复制教材内容 / 把"建议章节"误写为"官方考点"。
- 是否需要用户介入：否。
- 实际产物：
  - `plans/soft_exam/ds.md`
  - `plans/soft_exam/os.md`
  - `plans/soft_exam/db.md`

---

## TASK-RR-02：建立第一周复盘示例（节奏起步）

- 状态：**done**（2026-05-28）
- 背景：`docs/WEEKLY_EXECUTION_TEMPLATE.md` 已建立三档强度模板，但用户尚未真实写过一份复盘。需要建一份**示例骨架**（不是用户的真实数据）作为后续模仿对象。
- 目标：新增 `records/weekly_reviews/_example.md`（带下划线前缀，避免被误认为真实周复盘），展示标准模式的填写方式。
- 要修改：新增 `records/weekly_reviews/_example.md`。
- 不要修改：不要直接帮用户写本周复盘（这必须由用户自己写）。
- 验收标准：示例文件存在且明确标注 `_example.md` / "这是示例骨架，不是真实周复盘"。
- 风险：让示例数据被误认为真实进度。
- 是否需要用户介入：否。
- 实际产物：
  - `records/weekly_reviews/_example.md`

---

## TASK-RR-03：Stage 1 工程实操线 · Round 02 实操目录展开

- 状态：**done**（2026-05-28）
- 背景：Stage 1 后续推进需要 Round 02 (Shell / 管道 / Git) 落地实操目录。
- 目标：按 `CONVERSION_PROTOCOL.md` §7 的标准在 `rounds/round_02/` 下建立 README + week1/2/3 + final 骨架（含 notes.md + exercises.sh）。
- 要修改：新增 `rounds/round_02/` 目录及其下文件。
- 不要修改：不要触碰 Round 00 / 不要批量展开 Round 01 / Round 03+。
- 验收标准：目录结构符合 §7；`progress.json` 中追加 Round 02 任务（lane=engineering）；`mark_done.sh` 能识别。
- 风险：一次性展开过多 Round 文件，违反"每轮一个任务"。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_02/README.md`
  - `rounds/round_02/week1/notes.md`、`rounds/round_02/week1/exercises.sh`
  - `rounds/round_02/week2/notes.md`、`rounds/round_02/week2/exercises.sh`
  - `rounds/round_02/week3/notes.md`、`rounds/round_02/week3/exercises.sh`
  - `rounds/round_02/final/comprehensive_exercise.sh`、`rounds/round_02/final/command_cheatsheet.md`
  - `progress.json` 追加 `r02-*` 任务（lane=`engineering`）

---

## TASK-RR-04：Stage 4 数学二保底节奏启动

- 状态：**done**（2026-05-28）
- 背景：数学二必须早启动 + 长期低强度 + 不断线。
- 目标：在 `plans/math2/` 下新增 `limits.md` 与 `la_matrix.md` 两份最小骨架，作为"先动起来"的入口。
- 要修改：新增 `plans/math2/limits.md` 与 `plans/math2/la_matrix.md`。
- 不要修改：不要预写大量例题；不要把骨架变成教材抄袭。
- 验收标准：两份文件存在；每份顶部有官方大纲提示；列出建议小节标题与一个"启动级"易错点示例。
- 风险：把数学二变成"一开始就高强度"，反而崩盘。
- 是否需要用户介入：否。
- 实际产物：
  - `plans/math2/limits.md`
  - `plans/math2/la_matrix.md`

---

## TASK-RR-05：院校跟踪表第一行（需要用户提供 / 联网）

- 状态：**skipped**（2026-05-31 用户要求永久跳过，不阻塞 agent_gate；**非**官网核验完成）
- 背景：`docs/GRADUATE_SCHOOL_TRACKER.md` 模板已建立，但任何院校数据必须以官网为准。
- 目标：填入用户感兴趣的第一所目标院校。
- 要修改：在 `docs/GRADUATE_SCHOOL_TRACKER.md` 末尾"院校列表"追加一行。
- 当前进展：用户已给定目标院校“中国科学研究院”，已写入意向区。
- 前置：补充官网招生目录链接（或允许 Codex 联网采集）后再回填主表正式字段。
- 风险：基于经验贴 / 过期数据填写。
- 是否需要用户介入：**是**。

---

## TASK-RR-06：错题系统第一次走通（需要用户提供 / 联网）

- 状态：**skipped**（2026-05-31 永久跳过，原 deferred；非已走通错题系统）
- 背景：错题系统流程已建立，但需要一道真实做错的题来跑通"记录 → 归类 → 复盘 → 回流"。
- 目标：在 `records/error_notes/<lane>/<module>/` 下记录第一道错题，并在本周复盘中说明回流动作。
- 前置：用户提供一道错题（含题面 + 你的错误答案 + 正确答案）。
- 风险：把示例题误当作真实错题保留在仓库。
- 是否需要用户介入：**是**。

---

## TASK-RR-07：考试日期填入（需要用户提供）

- 状态：**skipped**（2026-05-31 永久跳过，原 deferred；非已填入考试日期）
- 背景：`progress.html` 已支持考试倒计时（localStorage），用户需要在浏览器里录入日期。
- 目标：打开 `progress.html`，在"考试倒计时"卡片填入软考 / 数学二 / 408 的考试日期。
- 前置：用户后续决定启动考试日期管理时再恢复。
- 风险：基于过期年份填错日期。
- 是否需要用户介入：**是**。

---

## TASK-RR-08：作品集第一个项目卡片

- 状态：**skipped**（2026-05-31 用户要求永久跳过决策类卡点；非已追加项目卡片）
- 背景：`docs/PROJECT_PORTFOLIO_TRACK.md` 已建立追踪模板，但还没有任何已启动项目。
- 目标：协助用户挑选第一个项目方向，按 §3 卡片模板在文档末尾追加一份卡片。
- 要修改：`docs/PROJECT_PORTFOLIO_TRACK.md` 追加项目卡片。
- 前置：用户决定第一个想动手的项目方向（推荐方向见 §2）。
- 风险：选择 ROI 低的项目（不能多目标复用）。
- 是否需要用户介入：**是**（决策类）。

---

## TASK-RR-09：Stage 1 可选推进 · Round 05 最小骨架

- 状态：**done**（2026-05-28）
- 背景：`TASK-RR-05`、`TASK-RR-08` 当前都需要用户输入/决策，为保持自动推进节奏，先推进 Stage 1 无需用户介入的可选项。
- 目标：在 `rounds/round_05/` 下建立 README + week1/2/3 + final 的最小实操骨架（含 notes.md + exercises.sh + cheatsheet）。
- 要修改：新增 `rounds/round_05/` 目录与文件；同步 `CONVERSION_PROTOCOL.md`、`README.md`、`docs/PROJECT_STATE.md`。
- 不要修改：不触碰 `rounds/round_00/`；不改 `records/` 真实学习记录；不引入新依赖。
- 验收标准：目录结构符合协议 §7；脚本语法校验通过；协议同步检查与学习数据校验通过。
- 风险：一次性把 Round 05 进度接入也做掉，导致超出“最小骨架”边界。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_05/README.md`
  - `rounds/round_05/week1/notes.md`、`rounds/round_05/week1/exercises.sh`
  - `rounds/round_05/week2/notes.md`、`rounds/round_05/week2/exercises.sh`
  - `rounds/round_05/week3/notes.md`、`rounds/round_05/week3/exercises.sh`
  - `rounds/round_05/final/comprehensive_exercise.sh`
  - `rounds/round_05/final/algorithm_patterns_cheatsheet.md`

---

## TASK-RR-10：Stage 1 可选推进 · Round 06 最小骨架

- 状态：**done**（2026-05-28）
- 背景：在 `TASK-RR-09` 完成后，Stage 1 仍可继续以“最小骨架”方式推进，无需等待用户额外输入。
- 目标：在 `rounds/round_06/` 下建立 README + week1/2/3 + final 的最小实操骨架（含 notes.md + exercises.sh + cheatsheet）。
- 要修改：新增 `rounds/round_06/` 目录与文件；同步 `CONVERSION_PROTOCOL.md`、`README.md`、`docs/PROJECT_STATE.md`。
- 不要修改：不触碰 `rounds/round_00/`；不改 `records/` 真实学习记录；不引入新依赖。
- 验收标准：目录结构符合协议 §7；脚本语法校验通过；协议同步检查与学习数据校验通过。
- 风险：把远程 SSH 实操做成真实连接，触发额外授权边界。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_06/README.md`
  - `rounds/round_06/week1/notes.md`、`rounds/round_06/week1/exercises.sh`
  - `rounds/round_06/week2/notes.md`、`rounds/round_06/week2/exercises.sh`
  - `rounds/round_06/week3/notes.md`、`rounds/round_06/week3/exercises.sh`
  - `rounds/round_06/final/comprehensive_exercise.sh`
  - `rounds/round_06/final/linux_automation_cheatsheet.md`

---

## TASK-RR-11：Stage 1 可选推进 · Round 07 最小骨架

- 状态：**done**（2026-05-29）
- 背景：在 `TASK-RR-10` 完成后，Stage 1 仍可继续以“最小骨架”方式推进，无需等待用户额外输入。
- 目标：在 `rounds/round_07/` 下建立 README + week1/2/3 + final 的最小实操骨架（含 notes.md + exercises.py + cheatsheet）。
- 要修改：新增 `rounds/round_07/` 目录与文件；同步 `CONVERSION_PROTOCOL.md`、`README.md`、`docs/PROJECT_STATE.md`。
- 不要修改：不触碰 `rounds/round_00/`；不改 `records/` 真实学习记录；不引入新依赖。
- 验收标准：目录结构符合协议 §7；Python 脚本语法校验通过；协议同步检查与学习数据校验通过。
- 风险：将 Round 07 与后续工程化路线耦合过深，超出“最小骨架”边界。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_07/README.md`
  - `rounds/round_07/week1/notes.md`、`rounds/round_07/week1/exercises.py`
  - `rounds/round_07/week2/notes.md`、`rounds/round_07/week2/exercises.py`
  - `rounds/round_07/week3/notes.md`、`rounds/round_07/week3/exercises.py`
  - `rounds/round_07/final/comprehensive_exercise.py`
  - `rounds/round_07/final/ai_prep_tool_cheatsheet.md`

---

## TASK-RR-12：Stage 1 可选推进 · Round 08 最小骨架

- 状态：**done**（2026-05-29）
- 背景：在 `TASK-RR-11` 完成后，Stage 1 仍可继续以“最小骨架”方式推进，无需等待用户额外输入。
- 目标：在 `rounds/round_08/` 下建立 README + week1/2/3 + final 的最小实操骨架（含 notes.md + exercises.py + cheatsheet）。
- 要修改：新增 `rounds/round_08/` 目录与文件；同步 `CONVERSION_PROTOCOL.md`、`README.md`、`docs/PROJECT_STATE.md`。
- 不要修改：不触碰 `rounds/round_00/`；不改 `records/` 真实学习记录；不引入新依赖。
- 验收标准：目录结构符合协议 §7；Python 脚本语法校验通过；协议同步检查与学习数据校验通过。
- 风险：将 Round 08 的“路线选择”扩展为真实服务化开发，超出“最小骨架”边界。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_08/README.md`
  - `rounds/round_08/week1/notes.md`、`rounds/round_08/week1/exercises.py`
  - `rounds/round_08/week2/notes.md`、`rounds/round_08/week2/exercises.py`
  - `rounds/round_08/week3/notes.md`、`rounds/round_08/week3/exercises.py`
  - `rounds/round_08/final/comprehensive_exercise.py`
  - `rounds/round_08/final/upgrade_route_cheatsheet.md`

---

## TASK-RR-25：Stage 1 可选推进 · Round 21 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_21/` 最小骨架。

## TASK-RR-24：Stage 1 可选推进 · Round 20 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_20/` 最小骨架。

## TASK-RR-23：Stage 1 可选推进 · Round 19 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_19/` 最小骨架。

## TASK-RR-22：Stage 1 可选推进 · Round 18 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_18/` 最小骨架。

## TASK-RR-21：Stage 1 可选推进 · Round 17 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_17/` 最小骨架。

## TASK-RR-20：Stage 1 可选推进 · Round 16 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_16/` 最小骨架。

## TASK-RR-19：Stage 1 可选推进 · Round 15 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_15/` 最小骨架。

## TASK-RR-18：Stage 1 可选推进 · Round 14 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_14/` 最小骨架。

## TASK-RR-17：Stage 1 可选推进 · Round 13 最小骨架

- 状态：**done**（2026-05-31）
- 是否需要用户介入：否。
- 实际产物：`rounds/round_13/` 最小骨架。

---

## TASK-RR-16：Stage 1 可选推进 · Round 12 最小骨架

- 状态：**done**（2026-05-31）
- 背景：agent_gate 跳过 RR-05/06/07/08 后继续 Stage 1 最小骨架推进。
- 目标：在 `rounds/round_12/` 下建立自动化流水线练习骨架。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_12/README.md`
  - `rounds/round_12/week1|week2|week3/notes.md` 与 `exercises.py`
  - `rounds/round_12/final/comprehensive_exercise.py`
  - `rounds/round_12/final/pipeline_automation_cheatsheet.md`

---

## TASK-RR-15：Stage 1 可选推进 · Round 11 最小骨架

- 状态：**done**（2026-05-31）
- 背景：在 `TASK-RR-14` 完成后继续 Stage 1 最小骨架推进。
- 目标：在 `rounds/round_11/` 下建立 SQLite 持久化练习骨架。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_11/README.md`
  - `rounds/round_11/week1|week2|week3/notes.md` 与 `exercises.py`
  - `rounds/round_11/final/comprehensive_exercise.py`
  - `rounds/round_11/final/sqlite_persistence_cheatsheet.md`

---

## TASK-RR-14：Stage 1 可选推进 · Round 10 最小骨架

- 状态：**done**（2026-05-31）
- 背景：在 `TASK-RR-13` 完成后，Stage 1 仍可继续以“最小骨架”方式推进，无需等待用户额外输入。
- 目标：在 `rounds/round_10/` 下建立 README + week1/2/3 + final 的最小实操骨架（含 notes.md + exercises.py + cheatsheet）。
- 要修改：新增 `rounds/round_10/` 目录与文件；同步 `CONVERSION_PROTOCOL.md`、`README.md`、`docs/PROJECT_STATE.md`；新增 `scripts/agent_gate.py` 作为自动选任务门禁。
- 不要修改：不触碰 `rounds/round_00/`；不改 `records/` 真实学习记录；不引入新依赖。
- 验收标准：目录结构符合协议 §7；Python 脚本语法校验通过；协议同步检查与学习数据校验通过。
- 风险：将 Round 10 扩展为完整 ai_prep_tool 工程化改造，超出“最小骨架”边界。
- 是否需要用户介入：否。
- 实际产物：
  - `scripts/agent_gate.py`
  - `rounds/round_10/README.md`
  - `rounds/round_10/week1/notes.md`、`rounds/round_10/week1/exercises.py`
  - `rounds/round_10/week2/notes.md`、`rounds/round_10/week2/exercises.py`
  - `rounds/round_10/week3/notes.md`、`rounds/round_10/week3/exercises.py`
  - `rounds/round_10/final/comprehensive_exercise.py`
  - `rounds/round_10/final/python_engineering_cheatsheet.md`

---

## TASK-RR-13：Stage 1 可选推进 · Round 09 最小骨架

- 状态：**done**（2026-05-29）
- 背景：在 `TASK-RR-12` 完成后，Stage 1 仍可继续以“最小骨架”方式推进，无需等待用户额外输入。
- 目标：在 `rounds/round_09/` 下建立 README + week1/2/3 + final 的最小实操骨架（含 notes.md + exercises.py + cheatsheet）。
- 要修改：新增 `rounds/round_09/` 目录与文件；同步 `CONVERSION_PROTOCOL.md`、`README.md`、`docs/PROJECT_STATE.md`。
- 不要修改：不触碰 `rounds/round_00/`；不改 `records/` 真实学习记录；不引入新依赖。
- 验收标准：目录结构符合协议 §7；Python 脚本语法校验通过；协议同步检查与学习数据校验通过。
- 风险：将 Round 09 的“仓库规范化与测试”扩展为完整 CI/依赖体系改造，超出“最小骨架”边界。
- 是否需要用户介入：否。
- 实际产物：
  - `rounds/round_09/README.md`
  - `rounds/round_09/week1/notes.md`、`rounds/round_09/week1/exercises.py`
  - `rounds/round_09/week2/notes.md`、`rounds/round_09/week2/exercises.py`
  - `rounds/round_09/week3/notes.md`、`rounds/round_09/week3/exercises.py`
  - `rounds/round_09/final/comprehensive_exercise.py`
  - `rounds/round_09/final/repo_testing_cheatsheet.md`

---

# VPS 实操支线任务（编号 TASK-VPS-XX）

> 主线 TASK-RR-XX 与 VPS 支线 TASK-VPS-XX **可并行推进**，编号空间互不冲突。
> Level 2 及以上的远程操作必须先走 `docs/templates/remote_operation_confirmation.md`。

## TASK-VPS-00 ~ TASK-VPS-03：文档与治理（Level 0 / Level 1）

- 状态：done（在 2026-05-10 一次性完成 VPS 模块文档与治理体系接入）
- 是否需要用户介入：否。

## TASK-VPS-04：SSH 与远程 Linux 基础任务文档化

- 状态：done（文档已写在 `rounds/stage_03_vps_remote_ops/round_vps_04_ssh_basics.md`）
- 备注：实际执行（SSH 登录）属 Level 2 / 3，由 TASK-VPS-05 起接管。

## TASK-VPS-05：首次远程服务器只读检查（Level 2）

- 状态：deferred（用户暂缓授权）
- 详见 `rounds/stage_03_vps_remote_ops/round_vps_05_first_readonly_check.md`。
- 是否需要用户介入：是。

## TASK-VPS-06 ~ TASK-VPS-12

- 状态：pending（每次执行前都需要用户**单独**授权）。

---

# 历史任务（已归档 / 暂缓）

> 这些是 2026-05-05 ~ 2026-05-10 之间面向"网页交互式 AI 工程学习系统"长期规划的旧 TASK，**在 2026-05-12 路线重定向后被暂缓**。
> 它们没有被删除，因为某些子目标（progress.json 升级 / mark_done.sh 升级 / progress.html 升级）已经在 TASK-RR-00 中以"四主线 lanes"方式完成。

## TASK-001 ~ TASK-008：done / 已被 TASK-RR-00 替代

| 编号 | 原标题 | 状态 |
|---|---|---|
| TASK-001 | 创建长期目标与 Codex 协议文档 | done |
| TASK-002 | 设计统一 task registry | **superseded**（被四主线 lanes 替代） |
| TASK-003 | 实现 task registry 初版 | **superseded** |
| TASK-004 | 升级 progress 数据结构 | **done**（已在 TASK-RR-00 完成 v2） |
| TASK-005 | 兼容 Round 00 旧进度 | **done** |
| TASK-006 | 升级 mark_done.sh 支持全路线任务 | **done**（已按 lane 分组） |
| TASK-007 | 升级 progress_data.js 生成逻辑 | **done** |
| TASK-008 | 升级 progress.html 全路线展示 | **done**（已升级为四主线） |

## TASK-009 ~ TASK-012：重启推进（工程实操线）

| 编号 | 原标题 | 状态 |
|---|---|---|
| TASK-009 | 加入 action event log 初版 | **done**（2026-05-28） |
| TASK-010 | 加入 task feedback 原型 | **done**（2026-05-28） |
| TASK-011 | 建立 Round 01 最小骨架 | **done**（2026-05-28） |
| TASK-012 | 建立数据校验脚本 | **done**（2026-05-28） |

TASK-009 实际产物：
- `records/action_logs/README.md`
- `mark_done.sh`（新增动作事件 JSONL 记录）

TASK-010 实际产物：
- `scripts/generate_task_feedback.py`
- `records/feedback/README.md`
- `records/feedback/task_feedback.json`

TASK-012 实际产物：
- `scripts/validate_learning_data.py`

TASK-011 实际产物：
- `rounds/round_01/README.md`
- `rounds/round_01/week1|week2|week3/notes.md`
- `rounds/round_01/week1|week2|week3/exercises.sh`
- `rounds/round_01/final/comprehensive_exercise.sh`
- `rounds/round_01/final/command_cheatsheet.md`

> 这些旧 TASK 不删除，保留作为未来如果决定回到"网页交互式系统"方向时的参考。

---

## TASK-RR-27：Stage 1 增强 · Round 06 接入进度系统

- 状态：**done**（2026-07-04）
- 背景：Round 06 最小骨架已存在，进度系统尚未注册 `r06-*` 任务。
- 目标：将 Round 06 纳入进度闭环（任务注册 + 看板展示 + 练习自动打卡）。
- 要修改：`progress.json`、`progress.html`、`rounds/round_06/` 练习脚本、`README.md`。
- 不要修改：不触碰 `rounds/round_00/`；不改 `records/` 真实学习记录。
- 验收标准：`mark_done.sh` 可识别 `r06-*`；协议与学习数据校验通过。
- 是否需要用户介入：否。
- 实际产物：
  - `progress.json` 注册 `r06-*` 任务（lane=`engineering`）
  - `rounds_data.js` 展示 Round 06 任务
  - `rounds/round_06/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh` 接入 `mark_done.sh`
  - Web UI 可直接阅读 Round 06 notes / scripts 并完成记录

---

## TASK-RR-28：Web UI 后续增强 · 练习执行安全模型

- 状态：**done**（2026-07-04）
- 背景：2026-07-04 已实现“Web UI 阅读资料 / 查看练习脚本 / 写入记录 / 完成或撤销任务”的核心闭环。若后续要求“完全不切终端，并由浏览器直接执行本地练习脚本”，需要额外的命令执行权限模型。
- 目标：设计并实现安全的本地练习执行入口（仅允许白名单脚本、固定 `~/cli-lab` 沙盒、执行前提示影响、执行后记录输出摘要），并补充浏览器内沙盒终端以覆盖终端操作型练习。
- 实际产物：
  - `scripts/progress_lib.py`：新增白名单脚本运行、浏览器终端命令校验、沙盒目录限制、输出摘要和命令历史记录。
  - `scripts/progress_server.py`：新增 `POST /api/tasks/<id>/run`、`GET /api/terminal`、`POST /api/terminal/run`。
  - `progress.html` / `progress_ui.js`：练习任务“运行”按钮、运行结果弹窗、“练习终端”卡片。
  - `records/terminal/README.md`：说明浏览器终端命令记录。
  - `records/action_logs/README.md`、`README.md`、`docs/reports/WEB_UI_USER_TEST_2026_07_04.md` 同步说明。
- 验收标准：浏览器可触发白名单练习脚本；输出可见；失败可记录；浏览器终端可在 `~/cli-lab` 内执行常用练习命令；危险命令会被拦截；安全边界文档明确。
- 是否需要用户介入：否；用户已明确要求终端映射到 Web UI。

---

## TASK-RR-29：Web UI Figma 视觉重设计

- 状态：**done**（2026-07-04）
- 背景：Web UI 核心闭环已成立，但用户反馈界面不够美观，需要调用 Figma 重新设计并按设计稿实现。
- 目标：从用户视角重新审查首屏、主线指标、任务列表和移动端布局；建立 Figma 设计稿；按稿实现视觉与信息架构优化。
- 实际产物：
  - Figma 设计稿：<https://www.figma.com/design/SYls2yaG0D7EEAJGvrcZUd>
  - `progress.html` 工作台式 UI：左侧学习导航轨、今日学习主行动、主线指标卡、状态圆点任务行、移动端局部横向导航。
  - `progress_ui.js` API 横幅文案统一。
  - `docs/reports/WEB_UI_USER_TEST_2026_07_04.md` 追加视觉重设计补测。
- 验收：真实浏览器桌面端与 390px 移动端均无整页横向溢出；继续学习卡片的阅读与记录弹窗可正常打开；未写入真实学习记录。
- 是否需要用户介入：否。

---

## TASK-RR-30：Web UI 存档与读档

- 状态：**done**（2026-07-04）
- 背景：用户要求只通过 Web UI 推进学习并能“存档 / 读档”。原 Web UI 已能阅读、记录、完成/撤销，但没有快照恢复能力。
- 目标：实现本地学习进度快照；快照覆盖进度、动作记录、反馈、本周任务和倒计时；读档前自动创建恢复点。
- 实际产物：
  - `records/saves/README.md`
  - `scripts/progress_lib.py` 存档/读档公共函数
  - `scripts/progress_server.py` 新增 `GET /api/saves`、`POST /api/saves`、`POST /api/saves/<save_id>/load`
  - `progress.html` 新增“存档与读档”卡片与导航入口
  - `README.md`、`docs/PROJECT_STATE.md`、`docs/reports/WEB_UI_USER_TEST_2026_07_04.md` 同步说明与测试记录
- 验收：API 和真实浏览器 UI 均通过；读档确认框正常；读档后自动恢复点出现在列表；桌面端和 390px 移动端无整页横向溢出；测试快照已清理。
- 是否需要用户介入：否。

---

## TASK-RR-31：Stage 1 填充 · Round 01 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：核心 Web UI 已支持阅读、记录、运行练习脚本、浏览器终端、存档 / 读档。下一步开始逐轮把已有学习计划从“骨架”补成可直接学习的内容。Round 01 是最早的终端操作轮次，也是浏览器终端能力的第一轮真实验收。
- 目标：让 Round 01 用户只通过 Web UI 就能阅读、运行、手敲终端练习、完成自测和最终验收记录。
- 实际产物：
  - `rounds/round_01/README.md` 更新为 Web UI 使用说明。
  - `rounds/round_01/week1|week2|week3/notes.md` 补齐学习步骤、自测标准和终端练习说明。
  - `rounds/round_01/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh` 改为非交互运行，只打卡脚本实际完成的练习任务。
  - `rounds/round_01/final/command_cheatsheet.md` 补齐删除安全、命令说明和验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 01 输出清晰任务标题。
  - `scripts/progress_lib.py` 支持沙盒内普通 `rm <file>`、`less`、`man`，继续拦截危险删除和命令串联。
- 验收：Round 01 可通过 Web UI 阅读资料、运行脚本、使用浏览器终端完成文件删除等终端练习；脚本不再卡在输入等待，也不会替用户完成自测 / 小抄 / 验收。
- 是否需要用户介入：否。

---

## TASK-RR-32：Stage 1 填充 · Round 02 Web UI 可完成练习 + 任务绑定终端

- 状态：**done**（2026-07-04）
- 背景：Round 02 是 Shell、管道与本地 Git 最小工作流，终端操作比 Round 01 更密集。用户要求“把终端直接做成浏览器映射，集成到 UI 里面”。
- 目标：让 Round 02 用户只通过 Web UI 就能阅读、运行脚本、使用浏览器映射终端完成手敲练习、自测和最终验收记录；同时修正自测 / 验收任务被误显示“运行”的语义问题。
- 实际产物：
  - Figma 设计稿：<https://www.figma.com/design/gmSFWf3hylozNlXIlHIJAR>
  - `rounds/round_02/README.md` 更新为 Web UI 使用说明。
  - `rounds/round_02/week1|week2|week3/notes.md` 补齐重定向、管道、Shell 脚本、本地 Git 的 Web UI 练习步骤。
  - `rounds/round_02/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh` 改为非交互运行，只打卡脚本实际完成的练习任务。
  - `rounds/round_02/final/command_cheatsheet.md` 补齐命令小抄与最终验收自问。
  - `progress.html` / `progress_ui.js`：练习终端升级为“当前任务 + 工作目录 + 快捷命令 + 控制台”；工程实操练习 / 自测 / 产出任务新增“终端”按钮并自动绑定到 `~/cli-lab/roundN`。
  - `scripts/progress_lib.py` / `scripts/progress_server.py`：终端命令日志新增 `task_id`；“运行”只允许 `exercise` 类型任务。
  - `records/terminal/README.md` 同步终端边界与 `task_id` 字段。
- 验收：真实 Chrome 页面可从 Round 02 任务行点击“终端”绑定到 `~/round2`；UI 输入 `pwd` 输出 `/Users/alalapi/cli-lab/round2`；自测任务不会显示或通过“运行”入口；API、静态语义和数据验证均通过；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-33：Stage 1 填充 · Round 03 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 03 是 Python 基础补强与复杂度直觉，原内容仍偏“最小骨架”，任务标题泛化，脚本会把自动练习和用户自测边界混在一起。
- 目标：让 Round 03 用户只通过 Web UI 就能阅读、运行 Python 练习脚本、在浏览器映射终端中手写自测脚本，并手动记录小抄 / 验收。
- 实际产物：
  - `rounds/round_03/README.md` 更新为 Web UI 使用说明。
  - `rounds/round_03/week1|week2|week3/notes.md` 补齐 Python 语法、list/dict、复杂度观察的页面学习路径与自测命令。
  - `rounds/round_03/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh` 改为非交互运行，只打卡脚本实际完成的练习任务。
  - `rounds/round_03/final/complexity_cheatsheet.md` 补齐 Python 小抄、复杂度小抄与最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 03 输出清晰任务标题。
  - `progress.html` 支持 `?round=round_03`、`?round03=1` 等直达 Round 参数，方便从报告或任务链接直接进入目标轮次。
- 验收：API 可运行 Round 03 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r03-w1-self` 到 `~/round3` 并执行 `pwd`；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-34：Stage 1 填充 · Round 04 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 04 是核心数据结构入门，原内容仍是最小骨架，任务标题泛化，脚本会等待输入并连带标记自测 / 小抄 / 验收。
- 目标：让 Round 04 用户只通过 Web UI 就能阅读 list、stack、queue、dict、set、deque 资料，运行自动练习，在浏览器映射终端中手写自测脚本，并手动记录最终验收。
- 实际产物：
  - `rounds/round_04/README.md` 更新为 Web UI 使用说明。
  - `rounds/round_04/week1|week2|week3/notes.md` 补齐 list、stack/queue、dict/set 的页面学习路径、自测命令和完成标准。
  - `rounds/round_04/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh` 改为非交互运行，只打卡脚本实际完成的练习任务。
  - `rounds/round_04/final/complexity_cheatsheet.md` 补齐数据结构选择口诀和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 04 输出清晰任务标题。
- 验收：API 可运行 Round 04 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r04-w1-self` 到 `~/round4` 并执行 `pwd`；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-35：Stage 1 填充 · Round 05 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 05 是高频算法模式入门，虽然已接入进度系统，但原内容仍偏最小骨架；notes 缺少 Web UI 学习路径，脚本会等待输入并连带标记自测 / 小抄 / 验收，任务标题也不利于用户判断该练什么。
- 目标：让 Round 05 用户只通过 Web UI 就能阅读二分、滑动窗口、双指针、DFS/BFS、回溯、贪心、DP 资料，运行自动练习，在浏览器映射终端中手写自测脚本，并手动记录最终验收。
- 实际产物：
  - `rounds/round_05/README.md` 更新为 Web UI 可练习说明，明确阅读、运行、自测、最终验收的页面操作路径。
  - `rounds/round_05/week1|week2|week3/notes.md` 补齐算法模式触发条件、页面学习路径、自测命令和完成标准。
  - `rounds/round_05/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh` 改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动记录。
  - `rounds/round_05/final/algorithm_patterns_cheatsheet.md` 补齐算法模式选择小抄和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 05 输出清晰任务标题。
- 验收：API 可运行 Round 05 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r05-w1-self` 到 `~/round5` 并执行 `pwd` / 手写 Python 文件；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-36：Web UI 文档阅读器外部链接跳转

- 状态：**done**（2026-07-04）
- 背景：用户明确要求文档学习可以直接在 Web UI 中读，外部链接可以直接跳转。阅读器已支持代码块、表格和尖括号 URL，但主流 Markdown 链接 `[标题](https://...)` 未被渲染为可点击链接。
- 目标：让学习资料中的外部资源链接在阅读弹窗内可点击，并通过新标签页打开。
- 实际产物：
  - `progress_ui.js`：`inlineMarkdown()` 支持 `[标题](https://...)` 外链，渲染为 `target="_blank"` 并带 `rel="noreferrer noopener"`。
- 验收：真实浏览器打开 `progress.html?round=round_05`，在阅读器中打开 `round_05.md` 后，`Hello Algo` 等 5 个外部资料链接均渲染为可点击外链。
- 是否需要用户介入：否。

---

## TASK-RR-37：Stage 1 填充 · Round 06 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 06 已接入进度系统，但仍是最小骨架；notes 缺少 Web UI 学习路径，脚本会等待输入并连带标记自测 / 小抄 / 验收，任务标题过泛；同时本轮涉及 `ssh`、`rsync`、`crontab` 等高风险命令，需要在 Web UI 里明确安全边界。
- 目标：让 Round 06 用户只通过 Web UI 就能阅读 find/xargs/sed/awk、进程查看、长任务保活、远程同步与 cron 排练资料，运行自动练习，在浏览器映射终端中完成安全自测，并手动记录最终验收。
- 实际产物：
  - `rounds/round_06/README.md` 更新为 Web UI 使用说明，明确浏览器终端与远程命令边界。
  - `rounds/round_06/week1|week2|week3/notes.md` 补齐批处理、进程查看、远程排练的页面学习路径、自测命令和完成标准。
  - `rounds/round_06/week1|week2|week3/exercises.sh` 与 `final/comprehensive_exercise.sh` 改为非交互运行，只自动记录脚本实际完成的练习任务；自测、小抄和验收仍由用户手动记录。
  - `rounds/round_06/final/linux_automation_cheatsheet.md` 补齐 Linux 自动化小抄、Web UI 安全边界和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 06 输出清晰任务标题。
  - `scripts/progress_lib.py` / `records/terminal/README.md`：浏览器终端允许只读 `ps` 进程查看，继续拦截 `ssh` / `scp` / `rsync` / 真实网络命令。
- 验收：API 可运行 Round 06 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r06-w2-self` 到 `~/round6` 并执行 `ps`；`ssh user@host` 被拦截；`round_06.md` 外部资料链接可在阅读器新标签页打开；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-38：Stage 1 填充 · Round 07 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 07 已接入进度系统，但仍是最小骨架；notes 缺少 Web UI 学习路径，Week 2 / Final 脚本默认要求 `--input`，会在网页“一键运行”中失败，任务标题也不利于用户判断该练多格式读取、参数日志还是整合工具。
- 目标：让 Round 07 用户只通过 Web UI 就能阅读 pathlib、多格式读写、argparse、logging、去重统计资料，运行自动练习，在浏览器映射终端中完成 Python 文件自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_07/README.md` 更新为 Web UI 使用说明，明确阅读、运行、自测、最终验收边界。
  - `rounds/round_07/week1|week2|week3/notes.md` 补齐页面学习路径、浏览器终端自测命令、格式/参数/日志/函数拆分要点。
  - `rounds/round_07/week1|week2|week3/exercises.py` 与 `final/comprehensive_exercise.py` 改为默认可从 Web UI 非交互运行，自动生成演示输入、输出结果、日志和下一步提示；只自动记录对应练习任务。
  - `rounds/round_07/final/ai_prep_tool_cheatsheet.md` 补齐 Web UI 完成路径、参数、格式读取和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 07 输出清晰任务标题。
- 验收：API 可运行 Round 07 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r07-w1-self` 到 `~/round7` 并运行手写 `read_formats.py`；`python3 -c` 仍被拦截；`round_07.md` 外部资料链接可在阅读器新标签页打开；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-39：Stage 1 填充 · Round 08 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 08 已接入进度系统，但仍是最小骨架；notes 缺少 Web UI 学习路径，脚本未接入自动记录，任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断该做项目收口、sqlite3 还是服务化接口排练。
- 目标：让 Round 08 用户只通过 Web UI 就能阅读项目收口、最小测试、sqlite3 运行历史、服务化接口形状资料，运行自动练习，在浏览器映射终端中完成自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_08/README.md` 更新为 Web UI 使用说明，明确不引入新依赖、不启动真实后端服务的边界。
  - `rounds/round_08/week1|week2|week3/notes.md` 补齐页面学习路径、浏览器终端自测命令、项目收口 / sqlite3 / API 合同要点。
  - `rounds/round_08/week1|week2|week3/exercises.py` 与 `final/comprehensive_exercise.py` 改为默认可从 Web UI 非交互运行，自动生成项目骨架、测试报告、SQLite 数据库、API 合同和收口摘要；只自动记录对应练习任务。
  - `rounds/round_08/final/upgrade_route_cheatsheet.md` 补齐 Web UI 完成路径、三条升级路线选择标准和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 08 输出清晰任务标题。
- 验收：API 可运行 Round 08 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r08-w3-self` 到 `~/round8` 并运行手写 `api_contract.py`；`pip install fastapi` 被拦截；`round_08.md` 外部资料链接可在阅读器新标签页打开；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-40：Stage 1 填充 · Round 09 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 09 已有最小骨架，但 notes 只列目标和自查，脚本未形成完整 Web UI 闭环，任务标题仍偏泛化，用户无法判断 README/.gitignore、本地 Git 分支、纯函数测试分别要完成什么。
- 目标：让 Round 09 用户只通过 Web UI 就能阅读仓库规范化、本地 Git 分支工作流、纯函数与测试资料，运行自动练习，在浏览器映射终端中完成本地 Git / Python 自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_09/README.md` 更新为 Web UI 使用说明，明确不安装 pytest、不做 GitHub 远程操作。
  - `rounds/round_09/week1|week2|week3/notes.md` 补齐页面学习路径、浏览器终端自测命令、README/.gitignore / 本地 Git / pytest 风格测试要点。
  - `rounds/round_09/week1|week2|week3/exercises.py` 与 `final/comprehensive_exercise.py` 改为默认可从 Web UI 非交互运行，自动生成规范化项目、本地 Git 沙盒、测试样例和收口摘要；只自动记录对应练习任务。
  - `rounds/round_09/final/repo_testing_cheatsheet.md` 补齐 Web UI 完成路径、命令小抄和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 09 输出清晰任务标题。
- 验收：API 可运行 Round 09 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r09-w1-self` 到 `~/round9` 并执行 `pwd`；终端 API 可在 `r09-w2-self` 下完成本地 Git init / commit / log，`git push origin main` 被拦截；`round_09.md` 外部资料链接可在阅读器新标签页打开；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-41：Stage 1 填充 · Round 10 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 10 已有最小骨架，但 notes 只列目标和自查，脚本不会自动记录，任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断模块拆分、配置日志、错误处理分别要完成什么。
- 目标：让 Round 10 用户只通过 Web UI 就能阅读 Python 工程化资料，运行自动练习，在浏览器映射终端中完成 CLI / config / error handling 自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_10/README.md` 更新为 Web UI 使用说明，明确不安装第三方依赖、不切 `src/` layout、不做打包发布。
  - `rounds/round_10/week1|week2|week3/notes.md` 补齐页面学习路径、浏览器终端自测命令、CLI / core / IO、config.ini / logging、可控错误与入口规范要点。
  - `rounds/round_10/week1|week2|week3/exercises.py` 与 `final/comprehensive_exercise.py` 改为默认可从 Web UI 非交互运行，自动生成工程化沙盒项目、配置、日志、错误路径报告和收口摘要；只自动记录对应练习任务。
  - `rounds/round_10/final/python_engineering_cheatsheet.md` 补齐文件职责表、配置日志口诀、错误处理口诀和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 10 输出清晰任务标题。
- 验收：API 可运行 Round 10 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r10-w1-self` 到 `~/round10` 并执行 `pwd`；终端 API 可在 `r10-w3-self` 下写入入口脚本并看到返回码 2；`python3 -c` 仍被拦截；`round_10.md` 外部资料链接可在阅读器新标签页打开；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-42：Stage 1 填充 · Round 11 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 11 已有最小骨架，但 notes 只列目标和自查，脚本不会自动记录，任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断 SQLite 建表、查询封装、主工具持久化分别要完成什么。
- 目标：让 Round 11 用户只通过 Web UI 就能阅读 SQLite 持久化资料，运行自动练习，在浏览器映射终端中完成 `sqlite3` / Python 自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_11/README.md` 更新为 Web UI 使用说明，明确 `runs.db` 只写入 `~/cli-lab/round11` 沙盒。
  - `rounds/round_11/week1|week2|week3/notes.md` 补齐页面学习路径、浏览器终端自测命令、`runs` 表、参数化 SQL、`db.py` 封装和主工具接入要点。
  - `rounds/round_11/week1|week2|week3/exercises.py` 与 `final/comprehensive_exercise.py` 改为默认可从 Web UI 非交互运行，自动生成 SQLite 练习沙盒、查询报告、持久化报告和收口摘要；只自动记录对应练习任务。
  - `rounds/round_11/final/sqlite_persistence_cheatsheet.md` 补齐 Web UI 完成路径、表结构、参数化 SQL、安全边界和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 11 输出清晰任务标题。
- 验收：API 可运行 Round 11 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r11-w1-self` 到 `~/round11` 并执行 `pwd` / 手写 SQLite 脚本；`python3 -c` 仍被拦截；`round_11.md` 外部资料链接可在阅读器新标签页打开；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-43：Stage 1 填充 · Round 12 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 12 已有最小骨架，但 notes 只列目标和自查，脚本不会自动记录，任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断批处理、subprocess、归档、日志轮转和定时入口分别要完成什么。
- 目标：让 Round 12 用户只通过 Web UI 就能阅读自动化流水线资料，运行自动练习，在浏览器映射终端中完成批处理 / subprocess / logging 自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_12/README.md` 更新为 Web UI 使用说明，明确 cron / nohup / tmux 只做命令排练，不写系统 crontab、不启动后台任务。
  - `rounds/round_12/week1|week2|week3/notes.md` 补齐页面学习路径、浏览器终端自测命令、批量扫描、失败记录、subprocess、shutil 归档、日志轮转和定时入口要点。
  - `rounds/round_12/week1|week2|week3/exercises.py` 与 `final/comprehensive_exercise.py` 改为默认可从 Web UI 非交互运行，自动生成批处理沙盒、归档报告、轮转日志、定时入口示例和收口摘要；只自动记录对应练习任务。
  - `rounds/round_12/final/pipeline_automation_cheatsheet.md` 补齐 Web UI 完成路径、流水线顺序、文件职责表、安全边界和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 12 输出清晰任务标题。
  - `progress_ui.js` 支持按 `Escape` 关闭阅读弹窗，减少阅读后切换终端的操作阻力。
- 验收：API 可运行 Round 12 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r12-w1-self` 到 `~/round12` 并运行手写 `scan_demo.py`；`crontab -l` 被拦截；`round_12.md` 外部资料链接可在阅读器新标签页打开；阅读器可用 Escape 关闭；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-44：Stage 1 填充 · Round 13 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 13 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker，不会形成 venv / requirements / pyproject / Dockerfile / 发布包等可检查产物；任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断环境复现与发布边界。
- 目标：让 Round 13 用户只通过 Web UI 就能阅读环境复现资料，运行自动练习，在浏览器映射终端中完成 venv / TOML / Dockerfile 自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_13/README.md` 更新为 Web UI 使用说明，明确所有产物写入 `~/cli-lab/round13`，不联网安装依赖、不自动执行 Docker build/run。
  - `rounds/round_13/week1|week2|week3/notes.md` 补齐页面学习路径、浏览器终端自测命令、venv / requirements / pyproject / `.env.example` / Dockerfile / `.dockerignore` 要点。
  - `rounds/round_13/week1|week2|week3/exercises.py` 与 `final/comprehensive_exercise.py` 改为默认可从 Web UI 非交互运行，自动生成演示 venv、requirements、pyproject、配置样例、Dockerfile、发布检查报告和 zip 交付包；只自动记录对应练习任务。
  - `rounds/round_13/final/env_repro_cheatsheet.md` 补齐 Web UI 完成路径、文件职责表、复现流程口诀、Docker 边界和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 13 输出清晰任务标题。
- 验收：API 可运行 Round 13 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r13-w1-self` 到 `~/round13` 并创建无 pip 的 `.venv_self`；`docker build -t demo .` 被拦截；`round_13.md` 外部资料链接可在阅读器新标签页打开；阅读器与运行结果均可用 Escape 关闭；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-45：Stage 1 填充 · Round 14 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 14 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker，任务标题仍是“练习1 / 练习2 / 练习3”；用户无法从 Web UI 判断要练 HTTP 方法、JSON 合同还是 REST 路由。
- 目标：让 Round 14 用户只通过 Web UI 就能阅读 HTTP/API 设计资料，运行自动练习，在浏览器映射终端中完成 JSON / 路由自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_14/README.md` 更新为 Web UI 可练习说明，明确所有产物写入 `~/cli-lab/round14`，不使用 `curl` 访问真实网络，不安装 FastAPI / uvicorn，不启动长期服务。
  - `rounds/round_14/week1|week2|week3/notes.md` 补齐 HTTP 方法与状态码、JSON 请求/响应合同、REST 路由草图的学习步骤、自测命令和完成标准。
  - `rounds/round_14/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成方法矩阵、状态码矩阵、API 合同、mock API、路由测试报告和下一步提示，只自动记录对应练习任务。
  - `rounds/round_14/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的 HTTP API 设计包练习，生成 contract、mock API、client demo、preflight check、OpenAPI 预览和收口摘要，只自动记录 `r14-fin-comp`。
  - `rounds/round_14/final/http_api_cheatsheet.md` 补齐 Web UI 完成路径、方法/状态码/JSON 合同/REST 路由小抄和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 14 输出清晰任务标题。
- 验收：API 可运行 Round 14 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r14-w2-self` 到 `~/round14` 并执行 `pwd`；`curl https://example.com` 被拦截；Week 1 notes 可在阅读器中直接阅读；`round_14.md` 中 MDN HTTP 外链可新标签页打开；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-46：Stage 1 填充 · Round 15 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 15 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker；任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 FastAPI 应用入口、请求体模型还是 `/docs` 示例。
- 目标：让 Round 15 用户只通过 Web UI 就能阅读 FastAPI 基础资料，运行自动练习，在浏览器映射终端中完成 JSON / 路由自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_15/README.md` 更新为 Web UI 可练习说明，明确自动练习生成真实 FastAPI 代码形状，但不要求在 Web UI 里安装依赖或启动 `uvicorn`。
  - `rounds/round_15/week1|week2|week3/notes.md` 补齐应用入口、路径/查询参数、请求体、Pydantic 模型、示例数据和 `/docs` 的学习步骤、自测命令和完成标准。
  - `rounds/round_15/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成 FastAPI 文件、Pydantic 模型、样例 JSON、OpenAPI 预览和静态检查报告，只自动记录对应练习任务。
  - `rounds/round_15/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的 FastAPI 项目骨架练习，生成 `app/main.py`、routers、schemas、`requirements.txt`、`api_contract.json` 和静态验收报告，只自动记录 `r15-fin-comp`。
  - `rounds/round_15/final/fastapi_basics_cheatsheet.md` 补齐 Web UI 完成路径、FastAPI 概念表、运行边界和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 15 输出清晰任务标题。
- 验收：API 可运行 Round 15 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r15-w2-self` 到 `~/round15` 并执行 `pwd`；`pip install fastapi` 和 `uvicorn app.main:app` 被拦截；Week 1 notes 可在阅读器中直接阅读；`round_15.md` 中 FastAPI 官方外链可新标签页打开；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-47：Stage 1 填充 · Round 16 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 16 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker；任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 API 主链、SQLite 读写、上传、错误合同还是 API 测试。
- 目标：让 Round 16 用户只通过 Web UI 就能阅读 API 与数据层结合资料，运行自动练习，在浏览器映射终端中完成 SQLite / 查询 / 错误状态码自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_16/README.md` 更新为 Web UI 可练习说明，明确自动练习只写入 `~/cli-lab/round16`，不要求安装依赖或启动 `uvicorn`。
  - `rounds/round_16/week1|week2|week3/notes.md` 补齐 POST `/run`、SQLite、GET 列表/详情、上传、错误响应和 TestClient 的学习步骤、自测命令和完成标准。
  - `rounds/round_16/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成 FastAPI 形状代码、SQLite demo、上传 route、错误合同和静态检查报告，只自动记录对应练习任务。
  - `rounds/round_16/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的 API/Data Layer 项目包练习，生成完整项目骨架、`api_contract.json`、TestClient 示例和最终验收报告，只自动记录 `r16-fin-comp`。
  - `rounds/round_16/final/api_data_layer_cheatsheet.md` 补齐 Web UI 完成路径、请求主链、接口合同、错误约定和最终验收自问。
  - `round_16.md` 补充 Web UI 使用方式。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 16 输出清晰任务标题，并同步四星难度。
- 验收：API 可运行 Round 16 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r16-w1-self` 到 `~/round16` 并执行 `pwd` / 手写脚本；`curl https://example.com` 被拦截；Week 1 notes 可在阅读器中直接阅读；官方 FastAPI / Python sqlite3 外链可跳转；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-48：Stage 1 填充 · Round 17 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 17 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker；任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 APIRouter 拆分、配置日志、认证/CORS 还是部署检查。
- 目标：让 Round 17 用户只通过 Web UI 就能阅读服务化收口资料，运行自动练习，在浏览器映射终端中完成服务结构 / 配置 / 部署清单自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_17/README.md` 更新为 Web UI 可练习说明，明确自动练习只写入 `~/cli-lab/round17`，不要求安装依赖、运行 Docker 或启动长期服务。
  - `rounds/round_17/week1|week2|week3/notes.md` 补齐 APIRouter、Settings、metadata、logging、Bearer auth、CORS、Dockerfile 和 preflight 的学习步骤、自测命令和完成标准。
  - `rounds/round_17/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成多文件服务结构、配置日志入口、安全部署检查和静态检查报告，只自动记录对应练习任务。
  - `rounds/round_17/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的服务化收口项目包练习，生成 routers、settings、logging、auth、CORS、Dockerfile、contract 和最终验收报告，只自动记录 `r17-fin-comp`。
  - `rounds/round_17/final/service_wrapup_cheatsheet.md` 与 `round_17.md` 补齐 Web UI 完成路径、服务化清单和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 17 输出清晰任务标题，并同步四星难度。
  - `scripts/progress_lib.py` 兼容浏览器终端中的 `~/cli-lab/round17` 与 `~/round17` 两种用户路径写法；`progress.html` 取消顶部卡片 sticky，避免滚动到 Round 清单时遮挡任务区。
- 验收：API 可运行 Round 17 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r17-w1-self` 到 `~/round17` 并执行 `pwd` / 手写脚本；`docker build -t demo .` 被拦截；Week 1 notes 可在阅读器中直接阅读；FastAPI 官方外链可新标签页打开；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-49：Stage 1 填充 · Round 18 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 18 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker；任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 NumPy 数组、pandas CSV 还是完整数据分析流水线。
- 目标：让 Round 18 用户只通过 Web UI 就能阅读数值计算与数据分析资料，运行自动练习，在浏览器映射终端中完成数组 / CSV / 清洗自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_18/README.md` 更新为 Web UI 可练习说明，明确自动产物只写入 `~/cli-lab/round18`，不在 Web UI 中执行 `pip install numpy pandas`。
  - `rounds/round_18/week1|week2|week3/notes.md` 补齐 NumPy 数组、shape/dtype/axis、pandas CSV、DataFrame 筛选统计、数据清洗与分析报告的学习步骤、自测命令和完成标准。
  - `rounds/round_18/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成 NumPy / pandas / 分析流水线示例代码、样例数据、静态检查报告和下一步提示，只自动记录对应练习任务。
  - `rounds/round_18/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的数值数据分析项目包练习，生成 `analysis.py`、样例 CSV、分析合同、标准库预检和最终静态验收报告，只自动记录 `r18-fin-comp`。
  - `rounds/round_18/final/numerics_analytics_cheatsheet.md` 与 `round_18.md` 补齐 Web UI 完成路径、NumPy / pandas / 清洗统计小抄和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 18 输出清晰任务标题，并同步三星难度。
- 验收：API 可运行 Round 18 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r18-w1-self` 到 `~/round18` 并执行 `pwd` / 手写脚本；`pip install numpy pandas` 被拦截；Week 1 notes 可在阅读器中直接阅读；NumPy 官方外链可新标签页打开；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-50：Stage 1 填充 · Round 19 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 19 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker；任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 X/y 切分、分类指标还是 Pipeline 防泄漏。
- 目标：让 Round 19 用户只通过 Web UI 就能阅读机器学习最小闭环资料，运行自动练习，在浏览器映射终端中完成指标 / 切分 / 预处理自测，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_19/README.md` 更新为 Web UI 可练习说明，明确自动产物只写入 `~/cli-lab/round19`，不在 Web UI 中执行 `pip install scikit-learn numpy pandas`。
  - `rounds/round_19/week1|week2|week3/notes.md` 补齐 X/y、train/test split、fit/predict/score、accuracy/precision/recall/F1、过拟合、预处理、Pipeline 与数据泄漏的学习步骤、自测命令和官方外链。
  - `rounds/round_19/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成 scikit-learn 风格示例代码、标准库 smoke check、静态检查报告和下一步提示，只自动记录对应练习任务。
  - `rounds/round_19/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的机器学习最小闭环项目包练习，生成 `training.py`、`metrics.py`、`preprocess.py`、样例 CSV、实验合同、标准库预检和最终静态验收报告，只自动记录 `r19-fin-comp`。
  - `rounds/round_19/final/ml_minimal_loop_cheatsheet.md` 与 `round_19.md` 补齐 Web UI 完成路径、指标/过拟合/防泄漏小抄和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 19 输出清晰任务标题，并同步三星难度。
  - `progress_ui.js` / `progress.html`：阅读器 markdown 请求增加 `no-store` 和 cache-bust，资源版本号同步更新，避免用户看到旧版 notes。
- 验收：API 可运行 Round 19 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r19-w2-self` 到 `~/round19` 并执行 `pwd` / 手写指标脚本；`pip install scikit-learn numpy pandas` 被拦截；Week 1 notes 可在阅读器中直接阅读；scikit-learn 官方外链可新标签页打开；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-51：Stage 1 填充 · Round 20 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 20 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker；任务标题仍是“练习1 / 练习2 / 练习3”，用户无法判断要练 Tensor、DataLoader、训练循环还是 checkpoint。
- 目标：让 Round 20 用户只通过 Web UI 就能阅读 PyTorch 入门资料，运行自动练习，在浏览器映射终端中完成 batch / loss 下降 / checkpoint smoke check，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_20/README.md` 更新为 Web UI 可练习说明，明确自动产物只写入 `~/cli-lab/round20`，不在 Web UI 中执行 `pip install torch torchvision`。
  - `rounds/round_20/week1|week2|week3/notes.md` 补齐 Tensor、Dataset/DataLoader、nn.Module、训练循环、eval/no_grad、state_dict 与 checkpoint 的学习步骤、自测短命令和官方外链。
  - `rounds/round_20/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成 PyTorch 风格示例代码、标准库 smoke check、静态检查报告和下一步提示，只自动记录对应练习任务。
  - `rounds/round_20/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的 PyTorch 入门项目包练习，生成 `dataset.py`、`model.py`、`train.py`、`checkpoint.py`、样例 CSV、工作流合同、标准库预检和最终静态验收报告，只自动记录 `r20-fin-comp`。
  - `rounds/round_20/final/pytorch_intro_cheatsheet.md` 与 `round_20.md` 补齐 Web UI 完成路径、训练循环、评估、保存加载小抄和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 20 输出清晰任务标题，并同步四星难度。
- 验收：API 可运行 Round 20 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r20-w2-self` 到 `~/round20` 并执行 `pwd` / loss 下降 smoke check；`pip install torch torchvision` 被拦截；Week 1 notes 可在阅读器中直接阅读；PyTorch 官方外链可新标签页打开；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-52：Stage 1 填充 · Round 21 Web UI 可完成练习

- 状态：**done**（2026-07-04）
- 背景：Round 21 已有最小骨架，但 notes 只列目标和自查，脚本只写 marker；总览还引导用户直接 `pip install torch transformers scikit-learn`，不符合“只通过 Web UI 稳定推进”的优先级。
- 目标：让 Round 21 用户只通过 Web UI 就能阅读 NLP 前置基础资料，运行自动练习，在浏览器映射终端中完成 tokenizer / embedding / text feature smoke check，并手动记录最终小抄与验收。
- 实际产物：
  - `rounds/round_21/README.md` 更新为 Web UI 可练习说明，明确自动产物只写入 `~/cli-lab/round21`，不在 Web UI 中安装 `torch`、`transformers`、`scikit-learn` 或下载模型。
  - `rounds/round_21/week1|week2|week3/notes.md` 补齐 tokenization、词表编号、embedding、padding、均值池化、传统文本特征、BPE / WordPiece 的学习步骤、自测短命令和官方外链。
  - `rounds/round_21/week1|week2|week3/exercises.py` 改为默认可非交互运行，自动生成 NLP 代码形状、标准库 smoke check、静态检查报告和下一步提示，只自动记录对应练习任务。
  - `rounds/round_21/final/comprehensive_exercise.py` 改为 Web UI 默认可运行的 NLP 前置基础项目包练习，生成 `tokenizer.py`、`dataset.py`、`embedding_model.py`、`traditional_baseline.py`、样例 CSV、流程合同、标准库预检和最终静态验收报告，只自动记录 `r21-fin-comp`。
  - `rounds/round_21/final/nlp_prereq_cheatsheet.md` 与 `round_21.md` 补齐 Web UI 完成路径、tokenization / vocab / embedding / TF-IDF 小抄和最终验收自问。
  - `scripts/build_rounds_data.py` / `rounds_data.js` 为 Round 21 输出清晰任务标题，并同步四星难度。
- 验收：API 可运行 Round 21 四个练习脚本；自测任务拒绝误运行；浏览器终端可绑定 `r21-w2-self` 到 `~/round21` 并执行 `pwd` / `cd` / `python3 stdlib_embedding_smoke.py`；`pip install torch transformers scikit-learn` 被拦截；Week 1 notes 可在阅读器中直接阅读；Hugging Face 官方外链可新标签页打开；运行结果弹窗可见；桌面端和 390px 移动端无横向溢出；测试记录已恢复。
- 是否需要用户介入：否。

---

## TASK-RR-26：Stage 1 增强 · Round 05 接入进度系统

- 状态：**done**（2026-06-15）
- 背景：Round 05 最小骨架已存在，但 `progress.json` / `progress.html` 未注册 `r05-*` 任务，练习脚本未接入 `mark_done.sh`。
- 目标：将 Round 05 纳入进度闭环（任务注册 + 看板展示 + 练习自动打卡）。
- 是否需要用户介入：否。
- 实际产物：
  - `progress.json` 追加 12 个 `r05-*` 任务（lane=`engineering`）
  - `progress.html` 新增 Round 05 面板
  - `rounds/round_05/*/exercises.sh` 与 `final/comprehensive_exercise.sh` 接入 `mark_done.sh`
  - `rounds/round_05/README.md` 更新使用说明

---

## 推荐下一步（按优先级）

1. 运行 `python3 scripts/agent_gate.py --json --no-require-clean` 查看下一项可自动推进任务。
2. （可选）继续逐轮把现有学习计划从“骨架”填充为可检查产物。
3. （可选）用户自行恢复 RR-05 官网核验或 RR-08 作品集决策时，在队列中改回 `pending` 并移出 `SKIP_TASK_IDS`。

> 主线推进、VPS 支线推进、考试日期录入**互不阻塞**；用户可根据当下心情与可用时间选择。

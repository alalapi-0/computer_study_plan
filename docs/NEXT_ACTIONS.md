# Next Actions

本文件是 Codex 后续自动推进的任务队列。每轮只允许选择一个任务推进，并在完成后同步更新本文件与 `docs/PROJECT_STATE.md`。

> **2026-05-12 路线重定向**：当前最高优先级是新建的 TASK-RR-XX 系列（路线重定向后的主任务队列）。
> 旧 TASK-002 ~ TASK-012（任务注册 / action log / 网页交互系统系列）已迁移到本文件末尾"历史任务（已归档 / 暂缓）"，按需重启。
> VPS 实操支线（TASK-VPS-XX）保持不变，可与主任务并行推进。

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

## TASK-RR-26：Stage 2 软考 · 软件工程 + UML + 面向对象 三模块骨架

- 状态：**done**（2026-06-13）
- 背景：`TASK-RR-01` 已完成 ds / os / db 三模块；按 `plans/soft_exam/README.md` §3 推进顺序第 2 步，下一批为软考独有高回报模块。
- 目标：新增 `plans/soft_exam/se.md`、`plans/soft_exam/uml.md`、`plans/soft_exam/oo.md` 三份笔记骨架（章节列表 + 408 差异 + 官方大纲提示），**不缓存具体考点**。
- 要修改：新增上述 3 份文件；同步 `docs/NEXT_ACTIONS.md`、`docs/PROJECT_STATE.md`。
- 不要修改：不要预写具体考题；不要复制教材整段；不要重新规划 Stage Plan。
- 验收标准：3 份文件存在；每份顶部有官方大纲提示；列出建议章节清单与 408 / 软考差异说明。
- 风险：把"建议章节"误写为"官方考点"。
- 是否需要用户介入：否。
- 实际产物：
  - `plans/soft_exam/se.md`
  - `plans/soft_exam/uml.md`
  - `plans/soft_exam/oo.md`

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

## 推荐下一步（按优先级）

1. 运行 `python3 scripts/agent_gate.py --json` 查看下一项可自动推进任务（已跳过 RR-05/06/07/08）。
2. （自动）**TASK-RR-27 候选**：Stage 2 软考 · 计算机网络 + 计算机组成 两模块骨架（`network.md` + `composition.md`），或 Stage 1 Round 05–21 进度系统接入。
3. （可选）用户自行恢复 RR-05 官网核验或 RR-08 作品集决策时，在队列中改回 `pending` 并移出 `SKIP_TASK_IDS`。

> 主线推进、VPS 支线推进、考试日期录入**互不阻塞**；用户可根据当下心情与可用时间选择。

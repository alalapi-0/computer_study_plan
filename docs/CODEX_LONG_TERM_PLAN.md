# Codex Long Term Plan

## 0. 2026-05-12 项目目标重定向（必读）

本文件原是面向"把仓库升级为网页交互式 AI 工程学习系统"的长期规划（Phase 0–7）。

在 2026-05-12 路线重定向中，仓库总目标已升级为**多目标耦合路线**：

| 时段 | 目标 |
|---|---|
| 短期（0–18 个月） | **软考中级软件设计师，高分 / 满分导向** |
| 中期（12–30 个月） | 系统化补齐非科班计算机基础短板 |
| 长期（24–48 个月） | **0854 电子信息**（人工智能 / 计算机技术 / 软件工程）跨专业考研 |
| 长期考试基础 | **数学二** + **408 兼容** |

新总目标的详细说明、四主线（engineering / soft_exam / math2 / cs408）、Stage 0–7 阶段计划、知识点映射表与错题系统已沉淀在以下文档：

- `docs/MASTER_STUDY_ROADMAP.md`（总学习路线）
- `docs/STAGE_PLAN.md`（Stage 0–7 阶段计划）
- `docs/KNOWLEDGE_MAPPING.md`（知识点映射）
- `docs/WEEKLY_EXECUTION_TEMPLATE.md`（周计划三档强度）
- `docs/PROGRESS_RULES.md`（四主线进度规则）
- `docs/ERROR_REVIEW_SYSTEM.md`（错题与复盘系统）
- `docs/GRADUATE_SCHOOL_TRACKER.md`（院校跟踪模板）
- `docs/PROJECT_PORTFOLIO_TRACK.md`（作品集追踪）

下面 §1 ~ §11 的原"网页交互式学习系统"路线**保留作为工程实操线（`engineering` lane）的演进参考**，但**不再是仓库的最高优先级**。

- 仍可参考：Phase 0、Phase 1（任务体系）、Phase 2（动作记录）的数据模型方向。
- **网页交互的可执行拆解**（在 `http://localhost:8000/progress.html` 完成读材料、练习、打卡、错题、复盘）：见 **`docs/PROGRESS_WEB_LEARNING_ROADMAP.md`**（PW-0 ~ PW-6，对应 `TASK-WEB-01` ~ `TASK-WEB-07`）。这是对 §4 Phase 4「网页交互版核心界面」的落地路线图，**计划态，未实现**。
- 新增 Round 实操目录按 Stage 1 需要推进；全路线网页化不阻塞软考 / 数学二主线。

> 短指令"请根据长期规划继续推进下一轮"现在应当按 `docs/NEXT_ACTIONS.md` 中**TASK-RR 系列**、`TASK-WEB`（若用户明确启动网页闭环）或当前 Stage 推进，而不是机械执行 §1 ~ §11 的旧 Phase 顺序。

---

## 1. 项目最终目标（历史规划，保留参考）

这个仓库最终要从“计算机基础学习大纲仓库”升级为一个“网页交互版计算机基础与 AI 工程学习系统”。

最终状态应该具备：

- 网页交互式学习界面
- Round 00-21 全路线任务体系
- 每个 round 有具体任务、练习、文档和状态
- 每条具体任务都能记录用户动作
- 每条具体任务都能给出反馈
- 每个任务能显示状态：未开始、进行中、已完成、需要复习、遇到问题
- 每个任务可以记录完成时间、执行次数、失败次数、备注、复盘
- 每个 round 可以显示整体进度
- 整个项目可以显示总进度
- 支持阶段复盘
- 支持后续逐步扩展到 API、数据库、ML/NLP 项目练习
- 保持对初学者友好
- 保持可长期维护

## 2. 项目核心原则

- 先保证可持续推进，再追求功能完整
- 先做清晰的数据模型，再做复杂交互
- 先保留现有 Round 00 可运行能力，再逐步扩展
- 不把未来规划写成已完成事实
- 不一次性大范围重构无关内容
- 每一轮只做一个明确目标
- 每一轮都必须可验证、可提交、可回滚
- 每一轮完成后都必须更新项目状态文档
- 每一轮完成后都必须更新下一步任务队列
- 网页交互版是最终方向，但早期可以继续使用 JSON + 静态 HTML + shell / Python 脚本
- 只有当 JSON 和静态页面无法支撑需求时，再逐步引入后端、数据库或前端框架

## 3. 目标产品形态

最终产品可以理解为：一个本地优先、GitHub 可版本管理、后续可网页化部署的学习系统。

用户打开网页后，应该能看到：

- 总进度
- 每个 round 的进度
- 每个 round 下的任务列表
- 每个任务的状态
- 每个任务的说明
- 每个任务的操作按钮
- 每个任务的历史记录
- 每个任务的反馈信息
- 当前建议下一步
- 阶段复盘入口

用户执行任务后，系统应该能记录：

- action_id
- task_id
- round_id
- action_type
- timestamp
- result
- note
- evidence_path
- feedback
- next_suggestion

这个产品不追求一次性变成复杂平台。它优先服务一个学习者在本地长期学习、记录、复盘和继续推进的真实流程。

## 4. 长期阶段路线

### Phase 0：项目状态固定与 Codex 协作协议

目标：
建立 Codex 长期协作规则、长期目标文档、当前状态文档和下一步任务队列。

主要产出：

- AGENTS.md
- docs/CODEX_LONG_TERM_PLAN.md
- docs/AUTO_ADVANCE_PROTOCOL.md
- docs/NEXT_ACTIONS.md
- docs/DECISIONS.md
- docs/PROJECT_STATE.md

非目标：

- 不实现网页大改
- 不实现全部 round 的代码
- 不引入数据库
- 不引入前端框架

完成标准：

- Codex 每次可通过文档理解项目目标和当前状态
- 用户之后可以用短指令继续推进项目

### Phase 1：统一任务注册与全路线进度底座

目标：
让 Round 00-21 全部进入统一任务体系，而不是只有 Round 00 能被记录。

主要产出：

- task registry
- progress 数据结构升级
- 旧 progress 兼容
- mark_done.sh 兼容升级
- progress_data.js 生成逻辑升级
- progress.html 能展示全路线

非目标：

- 不落地 Round 01-21 的全部练习代码
- 不做复杂网页交互
- 不引入后端

完成标准：

- Round 00-21 都能被系统识别
- Round 00 原有任务不丢失
- 用户能看到全路线进度
- 每个任务有统一 task_id

### Phase 2：用户动作事件记录机制

目标：
把“任务状态”升级为“任务动作历史”。

主要产出：

- action/event log 数据结构
- 用户每次操作都生成事件
- 事件包含时间、任务、动作、结果、备注
- 支持查询某个任务的动作历史
- 支持从动作历史生成反馈

非目标：

- 不做复杂数据库
- 不做多人账号系统
- 不做云同步

完成标准：

- 每个任务不只有 completed 状态，还能看到历史动作
- 用户执行任务后能保留记录
- 系统能基于记录生成最小反馈

### Phase 3：反馈与复盘系统

目标：
让每个任务有反馈，每个 round 有复盘。

主要产出：

- task feedback 数据结构
- round review 数据结构
- 自动生成简单反馈
- 支持用户备注
- 支持“需要复习”“遇到问题”“已掌握”等状态

非目标：

- 不引入大模型自动评价
- 不做复杂智能推荐

完成标准：

- 用户完成任务后能看到反馈
- 用户能回看某个 round 的复盘
- 系统能给出下一步建议

### Phase 4：网页交互版核心界面

目标：
把现有静态进度页升级为真正可交互的学习看板。

主要产出：

- 任务列表界面
- round 详情界面
- 任务操作按钮
- 任务历史展示
- 反馈展示
- 总进度展示
- 当前建议下一步

非目标：

- 不追求复杂 UI
- 不引入大型前端框架，除非必要
- 不做用户登录

完成标准：

- 用户可以主要通过网页查看和操作学习任务
- 网页能展示任务状态、历史和反馈
- 操作后数据能被保存

### Phase 5：Round 01-21 逐轮落地

目标：
把已有学习大纲逐轮变成真实可执行练习、脚本、笔记和项目骨架。

主要产出：

- rounds/round_01/
- rounds/round_02/
- ...
- 每轮 notes
- 每轮 exercises
- 每轮 final task
- 每轮任务注册
- 每轮验证方式

非目标：

- 不一次性生成 21 个 round 的全部代码
- 不为了数量牺牲质量

完成标准：

- 每个 round 都有目录
- 每个 round 都有可执行或可检查任务
- 每个 round 都能被网页系统追踪

### Phase 6：工程化与测试体系

目标：
让项目本身具备更强的可维护性。

主要产出：

- tests/
- JSON schema 或数据校验脚本
- progress 校验
- task registry 校验
- action log 校验
- README 更新
- 基础 CI，可选

非目标：

- 不过早引入重型测试框架
- 不做复杂部署

完成标准：

- 每次修改后能运行验证命令
- 数据文件损坏能被发现
- 主要功能有最小测试覆盖

### Phase 7：可选服务化/API 化

目标：
当静态网页和本地脚本不够用时，引入最小后端服务。

主要产出：

- FastAPI 或其他轻量 API
- 任务查询接口
- 任务更新接口
- action log 写入接口
- feedback 查询接口

非目标：

- 不做公网生产系统
- 不做复杂账号系统
- 不做高并发架构

完成标准：

- 前端可以通过 API 读写任务状态
- 后端可以持久化用户动作
- 项目架构仍然适合个人维护

## 5. 核心数据模型方向

以下是长期建议的数据模型方向，不代表当前已经实现。后续每轮推进时应按任务边界逐步落地，避免一次性大改。

### task registry

字段建议：

- task_id
- round_id
- round_title
- section_id
- title
- description
- type
- source_doc
- source_path
- implemented
- estimated_minutes
- prerequisites
- acceptance_criteria

用途：
作为全路线任务清单的统一来源，让 Round 00-21 的任务都能被系统识别、展示和追踪。

### progress state

字段建议：

- task_id
- status
- completed
- completed_at
- current_attempt_count
- last_action_at
- review_required
- notes

用途：
记录每个任务当前状态。它应兼容当前 `progress.json` 中 Round 00 的 `done` / `done_at` 信息，迁移时必须保证旧进度不丢失。

### action event

字段建议：

- action_id
- task_id
- round_id
- action_type
- timestamp
- result
- note
- evidence_path
- feedback_generated
- feedback_id

用途：
记录用户每一次动作，而不是只保存最终状态。它是后续反馈、复盘和建议的基础。

### feedback record

字段建议：

- feedback_id
- task_id
- action_id
- feedback_type
- message
- next_suggestion
- created_at

用途：
记录系统对某次动作或某个任务状态的反馈。早期可以先用规则生成短反馈，不需要引入大模型自动评价。

### round review

字段建议：

- round_id
- completed_tasks
- total_tasks
- blockers
- summary
- next_round_ready
- created_at

用途：
记录每个 round 的阶段复盘，帮助用户理解自己是否真的可以进入下一轮。

## 6. Codex 自动推进规则

Codex 后续每一轮都必须按以下流程推进：

1. 读取 AGENTS.md
2. 读取 docs/CODEX_LONG_TERM_PLAN.md
3. 读取 docs/PROJECT_STATE.md
4. 读取 docs/NEXT_ACTIONS.md
5. 选择优先级最高且不需要用户介入的任务
6. 创建或切换到独立分支
7. 执行一个小轮次
8. 运行验证
9. 更新文档
10. commit
11. push 到 GitHub 分支
12. 如可用，创建或更新 PR
13. 继续下一轮，直到遇到必须用户介入的情况

如果用户只说“请根据长期规划继续推进下一轮”，Codex 应按上述流程自动选择任务，不再要求用户重复解释项目背景。

## 7. 每轮任务边界

每轮只允许做一个明确任务。

可以一轮做：

- 统一 task registry
- 或 progress 数据结构迁移
- 或 action log 初版
- 或 progress.html 展示升级
- 或 Round 01 骨架

不可以一轮同时做：

- 数据模型重构
- 前端大改
- 后端 API
- Round 01-05 全部落地
- 测试体系
- 文档全面重写

每轮任务必须能在当前仓库中验证，并且应尽量保持可回滚。

## 8. Git 与 GitHub 推进规则

- 每轮必须在独立分支完成
- 默认分支命名：`codex/<task-id>-short-title`
- 验证通过后 commit
- remote 存在时 push 到 GitHub
- 不直接 push main
- 如 gh CLI 可用并已登录，可创建 PR
- 如果 push 失败，需要停止并报告
- 如果工作区有用户未提交修改，需要停止并报告

提交信息建议使用：

```text
TASK-XXX: short imperative summary
```

## 9. 必须停止并请求用户介入的情况

遇到以下情况必须停止并请求用户介入：

- git 工作区有用户未提交修改
- 需要删除或迁移已有学习记录但无法保证安全
- 需要引入大型新依赖
- 需要从 JSON 切换到数据库
- 需要从静态页面切换到前端框架
- 需要创建后端服务
- 需要修改 GitHub remote 或认证
- push 失败
- merge conflict
- 测试连续两次修复仍失败
- 任务边界不清
- PROJECT_STATE 与真实仓库严重不一致
- 需要用户确认产品方向

## 10. 文档同步规则

每轮结束必须更新：

- docs/PROJECT_STATE.md
- docs/NEXT_ACTIONS.md

必要时更新：

- docs/DECISIONS.md
- docs/CODEX_LONG_TERM_PLAN.md
- docs/AUTO_ADVANCE_PROTOCOL.md
- README.md
- AGENTS.md

不得出现：

- 文档说已实现，但代码没实现
- README 误导用户以为 Round 01-21 已落地
- NEXT_ACTIONS 与当前状态脱节

## 11. 当前近期优先级（已被 2026-05-12 重定向覆盖）

> ⚠️ 本节是 2026-05-05 时的优先级列表，路线重定向后**不再适用**。
> 新优先级请直接看 `docs/NEXT_ACTIONS.md` 的 TASK-RR 系列。

历史优先级（仅供参考）：

1. 创建长期目标和 Codex 协议文档（已完成）
2. 统一 task registry（已弃用 / 改由四主线 lanes 替代）
3. 升级 progress 数据结构（**已在 2026-05-12 完成 v2 升级，新增 lanes 与 tasks[].lane**）
4. 兼容 Round 00（**已在 2026-05-12 完成兼容**）
5. 升级 mark_done.sh（**已在 2026-05-12 完成按 lane 分组输出**）
6. 升级 progress.html（**已在 2026-05-12 完成四主线进度 / 阶段进度 / 倒计时 / 薄弱项**）
7. 加入 action event log（**暂缓**，按新路线非高优先级）
8. 加入 task feedback 原型（**暂缓**，按新路线非高优先级）
9. 建立 Round 01 最小骨架（**保留可选**，仅当 Stage 1 真实推进需要时再做）
10. 建立数据校验脚本（**保留可选**）

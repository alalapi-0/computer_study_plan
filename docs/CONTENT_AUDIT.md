# Content Audit

> 审计日期：2026-07-18
> 工作分支：`codex/linux-single-course-refactor`
> 备份标签：`pre-linux-only-refactor-20260718-1029`
> 契约：`TASK-LINUX-ONLY-BASELINE-20260718` / revision `r2`

## 1. 审计范围

扫描了以下路径与文件类型：

- 根目录：`README.md`、`AGENTS.md`、`CONVERSION_PROTOCOL.md`、`progress.json`、`progress_data.js`、`rounds_data.js`、`progress.html`、`progress_ui.js`、`mark_done.sh`、`round_00.md`–`round_21.md`
- `rounds/`：全部 `round_00`–`round_21` 与 `stage_03_vps_remote_ops/`
- `plans/`：`linux`、`soft_exam`、`math2`、`408`
- `docs/`：路线、状态、治理、模块、模板、检查清单、历史报告
- `scripts/`：进度、构建、校验、本地服务
- `records/`：动作日志、反馈、存档、周复盘骨架（无真实用户学习记录）
- 确认：`plan_round_*.txt` 已不存在于仓库

分类仅使用：`KEEP_PLATFORM` / `KEEP_LINUX` / `REMOVE_NON_LINUX` / `REVIEW_REQUIRED`。

## 2. 当前学习内容总览

| 路线 / 组 | 主要位置 | 原定位 |
|---|---|---|
| 工程实操 Round 00–21 | `round_XX.md` + `rounds/round_XX/` | 混合：Linux + Python + 算法 + Web/API + ML/NLP |
| VPS 远程支线 | `rounds/stage_03_vps_remote_ops/` | Linux 远程操作与授权前准备 |
| Linux 计划入口 | `plans/linux/` | 工程线下 Linux 专项串线 |
| 软考中级 | `plans/soft_exam/` + lane `soft_exam` | 软件设计师等考试主线 |
| 数学二 | `plans/math2/` + lane `math2` | 考研数学线 |
| 408 / 0854 | `plans/408/` + lane `cs408` | 考研计算机基础线 |
| 多主线总控文档 | `docs/MASTER_STUDY_ROADMAP.md` 等 | 软考 → 考研 → 工程实操混合总控 |

`progress.json` 基线：4 条 lane、317 个任务（engineering 296 / soft_exam 13 / math2 3 / cs408 5）。

## 3. 内容分类表

| 路径 | 当前内容 | 分类 | 处理方式 | 原因 |
|---|---|---|---|---|
| `progress.html` / `progress_ui.js` | Web UI 学习工作区 | KEEP_PLATFORM | 保留；仅做单课程 lane 兼容 | 平台基础设施 |
| `scripts/**` | 本地服务、进度、构建、校验 | KEEP_PLATFORM | 保留并收敛为单课程数据模型 | 平台实现代码 |
| `mark_done.sh` | CLI 进度入口 | KEEP_PLATFORM | 保留 | 平台闭环 |
| `progress.json` / `progress_data.js` / `rounds_data.js` | 进度与展示数据 | KEEP_PLATFORM | 重建为 linux-foundations | 平台数据；非课程正文 |
| `records/**`（骨架与空日志） | 动作日志 / 反馈 / 存档目录 | KEEP_PLATFORM | 保留；反馈由生成器重建 | 平台记录机制；无真实用户记录 |
| `.cursor/**` / `package.json` | MCP 与 npm 脚本 | KEEP_PLATFORM | 保留 | 工具与治理 |
| `docs/WORKSPACE.md` | 路径约定 | KEEP_PLATFORM | 保留并轻量同步表述 | 工作区事实 |
| `docs/PROGRESS_RULES.md` | 四主线进度规则 | KEEP_PLATFORM | 重写为单课程进度规则 | 平台规则文档 |
| `docs/DECISIONS.md` | ADR | KEEP_PLATFORM | 追加单课程 ADR | 架构决策 |
| `docs/AUTO_ADVANCE_PROTOCOL.md` | Agent 自动推进 | KEEP_PLATFORM | 重写为单课程目标 | 协作协议 |
| `docs/governance/**` / `docs/checklists/**` / `docs/templates/**` | 仓库治理与 VPS 安全 | KEEP_PLATFORM | 保留；去掉多课程表述处同步 | 平台治理 |
| `docs/modules/vps_remote_ops.md` | VPS 模块总纲 | KEEP_LINUX | 保留 | Linux 远程实践 |
| `docs/cursor_*` / `docs/prompts/**` / `docs/reports/**` | UI/Agent 流程与历史评测 | KEEP_PLATFORM | 保留为历史/流程文档 | 非正式课程内容 |
| `docs/AUDIT_2026_05_12.md` | 历史审计 | KEEP_PLATFORM | 保留 | 历史证据 |
| `rounds/round_00/` + `round_00.md` | Terminal 初见 | KEEP_LINUX | 保留并纳入课程模型 | Linux 核心 |
| `rounds/round_01/` + `round_01.md` | 文件系统与基础命令 | KEEP_LINUX | 保留并纳入课程模型 | Linux 核心 |
| `rounds/round_02/` + `round_02.md` | Shell、管道、Git 最小工作流 | KEEP_LINUX | 保留（Git 为 Linux 邻接） | Shell 核心；Git 是命令行工程实践辅助 |
| `rounds/round_06/` + `round_06.md` | Linux 进阶与自动化 | KEEP_LINUX | 保留并纳入课程模型 | Linux 核心 |
| `rounds/stage_03_vps_remote_ops/` | SSH / 远程目录 / 网络 / 服务排练 | KEEP_LINUX | 保留为课程远程模块 | Linux 远程与系统管理 |
| `plans/linux/` | Linux 专项串线 | KEEP_LINUX | 改写为 linux-foundations 入口 | 正式 Linux 课程入口 |
| `plans/README.md` | 多 lane 计划总览 | KEEP_PLATFORM | 重写为单课程计划说明 | 入口文档 |
| `rounds/round_03/`–`round_05/` + 对应 md | Python / 数据结构 / 算法 | REMOVE_NON_LINUX | 删除 | 独立非 Linux 课程 |
| `rounds/round_07/`–`round_21/` + 对应 md | Python 工程 / API / ML / NLP 等 | REMOVE_NON_LINUX | 删除 | 独立非 Linux 课程 |
| `plans/soft_exam/` | 软考计划 | REMOVE_NON_LINUX | 删除 | 非 Linux 正式课程 |
| `plans/math2/` | 数学二计划 | REMOVE_NON_LINUX | 删除 | 非 Linux 正式课程 |
| `plans/408/` | 408/0854 计划 | REMOVE_NON_LINUX | 删除 | 非 Linux 正式课程 |
| `docs/GRADUATE_SCHOOL_TRACKER.md` | 考研院校跟踪模板 | REMOVE_NON_LINUX | 删除 | 考研正式路线资产 |
| `docs/PROJECT_PORTFOLIO_TRACK.md` | 多目标作品集追踪 | REMOVE_NON_LINUX | 删除 | 服务软考/复试/AI 作品集，非 Linux 单课程 |
| `docs/MASTER_STUDY_ROADMAP.md` | 多主线总路线 | KEEP_PLATFORM | 重写为 Linux 单课程总路线 | 必填协议文件，内容收敛 |
| `docs/STAGE_PLAN.md` | 多 Stage 考试/考研阶段 | KEEP_PLATFORM | 重写为 Linux 单课程阶段 | 必填协议文件，内容收敛 |
| `docs/KNOWLEDGE_MAPPING.md` | 映射到软考/408/数学二 | KEEP_LINUX | 重写为 Linux 模块映射 | 去掉考试映射后可独立服务 Linux |
| `docs/ERROR_REVIEW_SYSTEM.md` | 考试导向错题系统 | KEEP_PLATFORM | 重写为 Linux 练习复盘 | 机制可复用，去除考试 lane |
| `docs/WEEKLY_EXECUTION_TEMPLATE.md` | 多主线周执行模板 | KEEP_PLATFORM | 重写为 Linux 周执行 | 模板保留、范围收敛 |
| `docs/NEXT_ACTIONS.md` / `PROJECT_STATE.md` / `CODEX_LONG_TERM_PLAN.md` | 状态与长期计划 | KEEP_PLATFORM | 重写 | 与单课程定位对齐 |
| `CONVERSION_PROTOCOL.md` | Round 00–21 + 多主线协议 | KEEP_PLATFORM | 重写覆盖范围 | 平台协议 |
| `AGENTS.md` / `README.md` | 多目标 Agent/用户入口 | KEEP_PLATFORM | 重写 | 项目入口事实 |

## 4. Linux 课程内容清单

最终正式课程：`linux-foundations`（Linux 基础与工程实践）

| 模块 | 来源资产 | 说明 |
|---|---|---|
| Module 00 · Terminal 初见 | Round 00 | 终端、pwd/ls/cd/mkdir/touch/cat/man |
| Module 01 · 文件系统与基础命令 | Round 01 | 路径、文件操作、文本查看 |
| Module 02 · Shell、管道与 Git 最小工作流 | Round 02 | 重定向、管道、Shell 脚本；Git 为邻接实践 |
| Module 03 · Linux 进阶与自动化 | Round 06 | find/xargs/sed/awk、进程、SSH/rsync/cron |
| Module 04 · VPS 远程实操（只读优先） | `stage_03_vps_remote_ops` | SSH、远程目录、网络、授权边界 |

内容注册入口：`content/courses/linux-foundations/`（本轮建立课程模型与模块索引；执行材料仍由 `rounds/` 提供以保持 Round 00 兼容）。

## 5. 非 Linux 内容清单

准备删除：

- `round_03.md`–`round_05.md`、`round_07.md`–`round_21.md`
- `rounds/round_03/`–`rounds/round_05/`、`rounds/round_07/`–`rounds/round_21/`
- `plans/soft_exam/`、`plans/math2/`、`plans/408/`
- `docs/GRADUATE_SCHOOL_TRACKER.md`
- `docs/PROJECT_PORTFOLIO_TRACK.md`
- `progress.json` / 镜像中的 soft_exam、math2、cs408 任务与 lane（重建时清除）

## 6. 不确定项

本轮审计后，**无待删除的 `REVIEW_REQUIRED` 项**。

曾疑似不确定、现已裁定：

| 路径 | 裁定 | 理由 |
|---|---|---|
| Round 02 Git 周 | KEEP_LINUX（邻接） | 属于命令行工程最小工作流，不是独立 Git 课程 |
| VPS-10/11 API/服务篇 | KEEP_LINUX（邻接） | 挂在 Linux 远程实操支线，强调远程环境与边界，不是独立后端课程 |
| `docs/ERROR_REVIEW_SYSTEM.md` | KEEP_PLATFORM（重写） | 去除考试 lane 后可作为 Linux 练习复盘机制 |
| `docs/KNOWLEDGE_MAPPING.md` | KEEP_LINUX（重写） | 去除考试映射后保留 Linux 模块覆盖表 |
| `docs/reports/**` | KEEP_PLATFORM | 历史评测报告，不是正式课程内容 |

## 7. 审计结论

当前仓库把 Linux 实操、软考、考研与多条工程/AI 课程混在同一进度系统中，导致产品定位与内容边界不清；本轮必须收敛为唯一正式课程 `linux-foundations`。

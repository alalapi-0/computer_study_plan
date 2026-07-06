# 🧭 computer_study_plan · 长期学习总控仓库

> **定位**：一个面向"在职 + 非科班 + 长期 + 多目标"学习者的本地优先、可版本管理的学习总控仓库。
> 主要服务于「软考中级 → 408/数学二/0854 考研 → 工程实操与作品集」一条连续路线。

---

## 0. 本地路径（唯一工作副本）

| 用途 | 路径 |
|---|---|
| **本仓库 Git 根目录（Cursor / PyCharm 工作区）** | `~/PycharmProjects/computer_study_plan` |
| **本机绝对路径** | `/Users/alalapi/PycharmProjects/computer_study_plan` |
| **Round 00 终端练习沙盒（不进 Git）** | `~/cli-lab/round0` |

完整约定（含如何自检、废弃的 Desktop 副本说明）见 **[`docs/WORKSPACE.md`](docs/WORKSPACE.md)**。  
文档、IDE 左下角路径、终端 `pwd` 应一致指向上表中的**仓库根**，不要维护第二份同名目录。

---

## 快速开始

日常学习优先打开 Web UI：

```bash
cd ~/PycharmProjects/computer_study_plan
python3 scripts/progress_server.py
open http://127.0.0.1:8777/progress.html
```

打开后先看「学习工作区」：

1. 左侧确认当前任务。
2. 中间读教程。
3. 按任务做练习或整理要点；工程任务会自动绑定右侧终端，「终端练习」用于切换或重新聚焦。
4. 点击「记录并完成」，在弹窗里写下本次记录后保存。

需要总览、倒计时、存档或复盘时，再展开「进度、配置、存档与复盘信息」。

---

## Agent / MCP 工具配置（普通学习可跳过）

当前项目需要以下 Workspace MCP Servers：

- chrome-devtools
- context7
- filesystem
- github
- playwright
- stitch

说明：

1. `.cursor/mcp.json` 是当前项目的 Workspace MCP 配置。
2. Cursor 可能需要**重启**或**重新加载窗口**后才能识别新配置；**批准 MCP 后建议完全退出 Cursor 并重开仓库**。
3. GitHub MCP 需要通过环境变量 `GITHUB_PERSONAL_ACCESS_TOKEN` 提供 token，**不允许写进仓库**。
4. Stitch MCP 需要通过环境变量 `STITCH_API_KEY` 提供 key，**不允许写进仓库**（见 `.env.example`）。
5. filesystem MCP 只授权当前项目目录（`.`，即仓库根）。
6. 可运行 `npm run check:mcp` 检查静态配置；`npm run check:cursor-mcp` 检查 CLI 层 MCP 状态（**均不代表当前 Agent 线程已暴露工具**）。

---

## Cursor Browser UI Workflow（开发 Web UI 时使用）

当使用 Cursor Agent 优化本地 Web UI（如 `progress.html`）时：

### 1. 如何检查 MCP

```bash
npm run check:cursor-mcp
# 或
bash scripts/check_cursor_mcp_status.sh
npm run check:mcp
```

### 2. 为什么需要重启 Cursor

- 批准 MCP 后，**旧 Agent 对话**可能仍看不到新工具
- **Multitask 子 Agent** 可能不继承 Workspace MCP
- **新建普通前台 Agent 对话**最稳定

详见 [`docs/cursor_tool_registry_check.md`](docs/cursor_tool_registry_check.md)。

### 3. UI 优化标准流程

1. 启动项目：`python3 scripts/progress_server.py`
2. 打开 `http://127.0.0.1:8777/progress.html` → 截图（before）
3. Stitch 设计输入（可选）
4. 修改代码（每轮一个 UI 切片）
5. 再打开页面 → console / network 检查
6. 截图（after）→ 运行测试
7. commit / push（默认直接推 `main`）

完整 14 步见 [`docs/cursor_browser_ui_runbook.md`](docs/cursor_browser_ui_runbook.md)。

### 4. 微信页面特殊说明

本仓库**不是**微信相关项目。若在其他场景操作微信公众号已登录页面：

- 必须使用 **wechat-chrome-session**
- 不允许用 Playwright 新开页面替代
- 遇到扫码 / 风控时停止，等待用户手动处理

下一轮 UI 推进 Prompt：[`docs/prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md`](docs/prompts/CURSOR_UI_IMPLEMENTATION_PROMPT.md)

---

## 1. 仓库定位

本仓库**不是**：

- ❌ 一个生产业务项目仓库（不放与学习路线无关的业务系统）
- ❌ 一个公网生产项目（不部署真实线上服务）
- ❌ 一个题库（不缓存任何具体考题或考点）
- ❌ 一个院校信息库（不基于经验贴或过期年份填写招生数据）

本仓库**是**：

- ✅ 学习路线的**总控**与本地 Web UI 学习工作区
- ✅ 章节笔记骨架与错题归档系统
- ✅ Codex / Cursor / 编程 AI 协作的工作入口
- ✅ 长期可维护、初学者可读的文档体系

---

## 2. 当前总目标（v2026-07）

| 时段 | 目标 |
|---|---|
| **短期（0–18 个月）** | 软考中级（默认软件设计师），**高分 / 满分导向** |
| **中期（12–30 个月）** | 系统化补齐非科班计算机基础短板 |
| **长期（24–48 个月）** | 0854 电子信息（人工智能 / 计算机技术 / 软件工程）跨专业考研 |
| **长期考试基础** | **数学二** + **408 兼容**（即使部分院校不考 408） |

详细说明见 [`docs/MASTER_STUDY_ROADMAP.md`](docs/MASTER_STUDY_ROADMAP.md)。

---

## 3. 四条主线（lanes）

| lane code | 中文名 | 核心内容 | 当前推进阶段 |
|---|---|---|---|
| `engineering` | 工程实操线 | Linux / Shell / Git / Python / 工程化 / 服务化 / AI 工程 / VPS 实操 | Stage 1（继续） |
| `soft_exam` | 软考中级线 | 软件设计师（默认）+ 备选方向 | Stage 2（启动） |
| `math2` | 数学二线 | 高等数学 + 线性代数（长期低强度） | Stage 4（启动） |
| `cs408` | 408 / 0854 线 | 数据结构 + 计组 + 操作系统 + 计算机网络 | Stage 5（按需启动） |

> 四条主线在 `progress.json` 顶层 `lanes` 字段中注册；每个任务通过 `tasks.<id>.lane` 字段归属。
> 关于 lane 的硬规则见 [`docs/PROGRESS_RULES.md`](docs/PROGRESS_RULES.md)。

---

## 4. 当前阶段

> ✏️ **此区块可手动更新**

- 已完成 **Stage 0 · 仓库治理与学习系统准备**：删除 22 份 `plan_round_XX.txt`，建立路线骨架与四主线进度系统。
- 当前最有效闭环：**Web UI 学习工作区**。Round 00–21 工程实操任务、软考 / 数学二 / 408 / Linux / VPS 计划入口均已接入页面。
- 下一步可选：
  1. 继续做 Web UI / 文档用户视角评测，重点检查入口说明、移动端、首屏信息密度和教程 / 终端 / 记录联动。
  2. 扩展 Stage 2 软考软件设计师计划，把模块骨架变成可检查产物清单（仍以最新官方信息为准）。
  3. 保持 Stage 4 数学二保底节奏，必要时补充更具体的练习记录模板。

---

## 5. 仓库结构

```
~/PycharmProjects/computer_study_plan/   ← 唯一 Git 工作副本（见 docs/WORKSPACE.md）
├─ README.md                       ← 本文件（仓库入口）
├─ docs/WORKSPACE.md               ← ★ 路径与工作区约定（单一事实源）
├─ AGENTS.md                       ← Codex / Cursor / 编程 AI 协作硬规则
├─ CONVERSION_PROTOCOL.md          ← Round md 与进度系统协议（v2.0）
├─ progress.html                   ← Web UI 学习工作区入口（四主线 + 教程 + 终端 + 记录 + 存档/读档）
├─ progress_ui.js                  ← Web UI 交互逻辑（教程、任务、终端、记录、存档、反馈）
├─ progress.json                   ← 进度状态唯一来源（v2 + lanes）
├─ progress_data.js                ← 进度镜像（由同步脚本 / CLI / 本地 API 从 progress.json 生成）
├─ rounds_data.js                  ← Round 与计划任务展示数据（由 scripts/build_rounds_data.py 生成）
├─ mark_done.sh                    ← 进度 CLI（简洁状态 / lane 过滤 / 补录完成）
├─ .gitignore
│
├─ scripts/                        ← 本地服务、数据同步、生成与校验脚本
│  ├─ progress_server.py           ← 本地 Web UI API 服务（默认 8777）
│  ├─ build_rounds_data.py         ← 生成 rounds_data.js
│  ├─ sync_progress_data.py        ← 同步 progress_data.js
│  └─ validate_learning_data.py    ← 校验学习数据结构
│
├─ round_00.md ~ round_21.md       ← 工程实操线 22 份 Round 概览（保留）
│
├─ docs/                           ← 长期规划与治理文档
│  ├─ MASTER_STUDY_ROADMAP.md      ← ★ 总学习路线
│  ├─ STAGE_PLAN.md                ← ★ Stage 0–7 阶段计划
│  ├─ KNOWLEDGE_MAPPING.md         ← ★ 知识点 → 软考/408/数学二 映射表
│  ├─ WEEKLY_EXECUTION_TEMPLATE.md ← ★ 三种强度周计划模板
│  ├─ PROGRESS_RULES.md            ← ★ 四主线进度规则
│  ├─ ERROR_REVIEW_SYSTEM.md       ← ★ 错题与复盘系统
│  ├─ GRADUATE_SCHOOL_TRACKER.md   ← ★ 院校跟踪模板（不含真实数据）
│  ├─ PROJECT_PORTFOLIO_TRACK.md   ← ★ 作品集追踪
│  ├─ CODEX_LONG_TERM_PLAN.md      ← 当前长期协作规则
│  ├─ AUTO_ADVANCE_PROTOCOL.md     ← Codex 单轮自动推进协议
│  ├─ PROJECT_STATE.md             ← 项目当前状态
│  ├─ NEXT_ACTIONS.md              ← 下一步任务队列
│  ├─ DECISIONS.md                 ← 架构决策（ADR）
│  ├─ AUDIT_2026_05_12.md          ← 路线重定向审计报告
│  ├─ modules/                     ← 模块总纲
│  │  └─ vps_remote_ops.md
│  ├─ governance/                  ← 仓库治理硬规则
│  ├─ checklists/                  ← 检查清单
│  └─ templates/                   ← 高风险操作确认模板
│
├─ plans/                          ← 学习计划专题目录（按 lane 组织）
│  ├─ README.md
│  ├─ linux/README.md              ← engineering lane
│  ├─ soft_exam/README.md          ← soft_exam lane
│  ├─ math2/README.md              ← math2 lane
│  └─ 408/README.md                ← cs408 lane
│
├─ records/                        ← 学习记录目录（当前无需保护的真实记录；后续由用户标注）
│  ├─ README.md
│  ├─ weekly_reviews/              ← 每周复盘（YYYY-WW.md）
│  ├─ error_notes/                 ← 错题本（按 lane / module 归档）
│  ├─ action_logs/                 ← Web UI / CLI 动作日志（进度系统产物）
│  ├─ feedback/                    ← 任务反馈 JSON（进度系统产物）
│  ├─ saves/                       ← Web UI 学习进度快照
│  └─ completed_tasks/             ← 完成的练习快照（可选）
│
└─ rounds/                         ← Round 实操目录（仅可执行内容进此）
   ├─ round_00/                    ← 终端入门（已展开并接入 Web UI）
   │  ├─ README.md
   │  ├─ week1/ week2/ week3/ final/
   ├─ round_01/                    ← 文件系统与基础命令（已展开）
   ├─ round_02/                    ← Shell/管道/Git 最小工作流（已展开）
   │  ├─ README.md
   │  ├─ week1/ week2/ week3/ final/
   ├─ round_03/                    ← Python 基础与复杂度入门（已展开）
   ├─ round_04/                    ← 核心数据结构（已展开）
   ├─ round_05/                    ← 高频算法模式（已展开）
   ├─ round_06/                    ← Linux 进阶与自动化（已展开）
   ├─ round_07/                    ← 面向 AI 项目综合练习（已展开）
   ├─ round_08/                    ← 总复盘与升级路线（已展开）
   ├─ round_09/                    ← 仓库规范化与测试入门（已展开）
   ├─ round_10/                    ← Python 工程化基础（已展开）
   ├─ round_11/                    ← 本地持久化与数据记录（已展开）
   ├─ round_12/ … round_21/        ← 工程 / 数据 / AI 轮次（已展开并接入 Web UI）
   └─ stage_03_vps_remote_ops/     ← VPS 远程实操支线（13 份 Round 文档）
      ├─ README.md
      └─ round_vps_00 ~ round_vps_12.md
```

> Round md 文件（`round_00.md` ~ `round_21.md`）作为**工程实操线素材库**全部保留，按需展开到 `rounds/round_XX/`。

---

## 6. 如何使用本仓库

### 6.1 第一次进入仓库

```bash
cd ~/PycharmProjects/computer_study_plan
```

在 Cursor / PyCharm 中打开**同一文件夹**作为工作区根目录。

依序阅读：

1. [`docs/MASTER_STUDY_ROADMAP.md`](docs/MASTER_STUDY_ROADMAP.md) — 总目标
2. [`docs/STAGE_PLAN.md`](docs/STAGE_PLAN.md) — 阶段计划
3. [`docs/KNOWLEDGE_MAPPING.md`](docs/KNOWLEDGE_MAPPING.md) — 知识点映射
4. [`docs/WEEKLY_EXECUTION_TEMPLATE.md`](docs/WEEKLY_EXECUTION_TEMPLATE.md) — 周计划三档强度
5. [`docs/PROGRESS_RULES.md`](docs/PROGRESS_RULES.md) — 进度规则
6. [`docs/ERROR_REVIEW_SYSTEM.md`](docs/ERROR_REVIEW_SYSTEM.md) — 错题系统

### 6.2 日常使用

- 每周选择一种强度（保底 / 标准 / 冲刺），在 `records/weekly_reviews/YYYY-WW.md` 写本周清单。
- 工作日优先打开 Web UI 的「学习工作区」：左侧确认当前任务，中间读教程，按任务做练习或整理要点；工程任务会自动绑定浏览器终端，「终端练习」按钮用于切换或重新聚焦。完成一个最小动作后，点击「记录并完成」，在弹窗里写下本次记录后保存。
- 需要回看整体进度、配置本周任务、存档或读档时，再展开「进度、配置、存档与复盘信息」。
- 错题录入 `records/error_notes/<lane>/<module>/...`。
- 周末写复盘。

### 6.3 打开 Web UI 学习工作区

- **方式一（推荐 · 网页记录）**：
  ```bash
  cd ~/PycharmProjects/computer_study_plan
  python3 scripts/progress_server.py
  # 或：npm run serve
  open http://127.0.0.1:8777/progress.html
  ```
  Web UI 首屏是「学习工作区」：当前任务和教程阅读优先展示；工程任务会额外显示浏览器终端，并自动绑定到对应 `~/cli-lab/roundN` 沙盒。点击「读教程」会在页面中间打开资料；点击「终端练习」可切换或重新聚焦对应任务终端。完成后点击「记录并完成」，在弹窗里写下本次记录后保存；已完成任务可从任务行撤销。存档 / 读档放在折叠的管理区中，读档前会自动创建恢复点。
- **方式二（只读检查）**：双击 `progress.html` 或通过 `python3 -m http.server` 打开，只适合看布局和只读进度；没有写 API、练习脚本运行、动作日志或浏览器终端能力，不作为日常学习入口。

Web UI 包含：

- 学习工作区（当前任务 + 内联教程 + 工程任务终端）
- 总进度与四主线进度（engineering / soft_exam / math2 / cs408）
- 按主线查看任务（工程线为 Round 00–21，考试 / 数学 / 408 为计划任务；Web UI 任务集合已与 `progress.json` 对齐）
- 折叠管理区：本周任务、考试倒计时、存档与读档、Stage 0–7、当前关注项
- 练习脚本运行结果（仅限已登记的 `rounds/round_XX/weekN|final` 白名单脚本）

### 6.4 进度系统 CLI

CLI 适合快速查看 / 补录完成 / 撤销任务；正式学习仍优先用 Web UI，因为网页会把当前任务、教程、记录弹窗和工程终端放在同一条流程里。

在仓库根目录执行：

```bash
cd ~/PycharmProjects/computer_study_plan
bash mark_done.sh                # 简洁查看：每条主线前 8 个未完成任务
bash mark_done.sh --lane soft_exam  # 只看某条主线
bash mark_done.sh --limit 20     # 调整每条主线显示数量
bash mark_done.sh --all          # 查看全部任务
bash mark_done.sh <task-id>      # 记录完成
bash mark_done.sh <task-id> --undo  # 取消完成
```

无参数运行时会显示每条主线前几个未完成任务，格式为 `task-id — 任务标题 / 所属分组`。如果只是想知道现在该做什么，先打开 Web UI；如果已经明确知道任务 id，再用 CLI 快速操作。

---

## 7. 文档导航

| 我想... | 看哪里 |
|---|---|
| 确认本机仓库 / IDE 应打开哪个目录 | `docs/WORKSPACE.md` |
| 看总目标 | `docs/MASTER_STUDY_ROADMAP.md` |
| 看现在该做什么阶段 | `docs/STAGE_PLAN.md` |
| 看某个知识点属于哪条 lane | `docs/KNOWLEDGE_MAPPING.md` |
| 设计本周节奏 | `docs/WEEKLY_EXECUTION_TEMPLATE.md` |
| 理解进度系统规则 | `docs/PROGRESS_RULES.md` + `CONVERSION_PROTOCOL.md` |
| 学错题系统怎么用 | `docs/ERROR_REVIEW_SYSTEM.md` |
| 填院校信息 | `docs/GRADUATE_SCHOOL_TRACKER.md` |
| 看作品集追踪 | `docs/PROJECT_PORTFOLIO_TRACK.md` |
| 看 Codex 的工作规则 | `AGENTS.md` + `docs/CODEX_LONG_TERM_PLAN.md` + `docs/AUTO_ADVANCE_PROTOCOL.md` |
| 看仓库治理规则 | `docs/governance/repo_rules.md` |
| 看 VPS 远程实操支线 | `docs/modules/vps_remote_ops.md` + `rounds/stage_03_vps_remote_ops/README.md` |
| 看本轮变更记录 | `docs/AUDIT_2026_05_12.md` + `docs/PROJECT_STATE.md` |

---

## 8. 维护规则

> 这些是**硬约束**，AI 与人类都需遵守。

- 不随意新增重复文档；任何新计划必须挂到总路线（`docs/MASTER_STUDY_ROADMAP.md`）。
- 所有学习任务必须能对应到某个 Stage（`docs/STAGE_PLAN.md`）。
- 每周至少一次复盘（`records/weekly_reviews/YYYY-WW.md`）。
- 错题归档到 `records/error_notes/<lane>/<module>/`，不写在 `plans/`。
- 不缓存任何具体考题 / 考纲条目 / 院校招生数据；涉及考试一律以**最新官方信息**为准。
- 不删除以下高保护对象（详见 `docs/governance/repo_rules.md`）：
  - `rounds/round_00/`、`round_00.md` ~ `round_21.md`
  - `progress.json`、`progress_data.js`、`rounds_data.js`、`progress.html`、`progress_ui.js`、`scripts/progress_server.py`、`mark_done.sh`
  - `records/action_logs/`、`records/feedback/`（除非本轮明确是生成 / 清理进度系统产物）
  - 用户后续明确标注为真实学习记录的 `records/` 内容
  - 各类长期规划与治理文档
- Codex / Cursor 协作必须遵守 `AGENTS.md` 与 `docs/AUTO_ADVANCE_PROTOCOL.md`。
- Round md 标准结构与命名见 `CONVERSION_PROTOCOL.md`（v2.0）。

---

## 9. 历史变更

- **2026-05-28** · 路径统一：约定唯一工作副本为 `~/PycharmProjects/computer_study_plan`，见 `docs/WORKSPACE.md`。
- **2026-05-12** · 路线重定向：从单一"网页交互式学习系统"升级为"软考 → 408/数学二/0854 多目标耦合"；删除 22 份 `plan_round_XX.txt`；建立四主线 lanes 与 Stage 0–7 阶段计划；进度系统升级到 v2。详情见 `docs/AUDIT_2026_05_12.md`。
- **2026-05-10** · VPS 远程实操支线接入。
- **2026-05-05** · 长期目标与 Codex 协议文档建立。

---

## 10. 现存路线 vs 历史 Round 文档

仓库中 `round_00.md` ~ `round_21.md` 是历史 Round 概览文档（22 份），现在的定位是**工程实操线（`engineering` lane）的素材库**。它们：

- ✅ 全部保留，未被废弃
- ✅ 按需在 `rounds/round_XX/` 展开为可执行实操目录（当前已展开 Round 00–Round 21）
- ✅ 数据结构、算法、网络、Linux 等 Round 内容会作为软考 / 408 模块的辅助素材（参考 `docs/KNOWLEDGE_MAPPING.md`）
- ❌ 不替代 `plans/soft_exam/` 与 `plans/408/` 中的专项考试笔记

---

## 11. 致使用者

- 这条路线长度按年计，节奏需要**长期可持续 > 短期高强度**。
- 错题本是知识体系最重要的指针，而不是炫学习量的工具。
- 数学二每周保底一道题，**永不为 0**。
- 不要把 22 份 Round 概览和实操目录的"已存在"误以为"已经学完"——完成状态以 Web UI / `progress.json` 为准。
- 院校信息**不要凭印象填**，必须查官网。

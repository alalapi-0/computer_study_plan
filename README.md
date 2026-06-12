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

## Workspace MCP Servers

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

## Cursor Browser UI Workflow

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

1. 启动项目（如 `python3 -m http.server 8000`）
2. 打开页面 → 截图（before）
3. Stitch 设计输入（可选）
4. 修改代码（每轮一个 UI 切片）
5. 再打开页面 → console / network 检查
6. 截图（after）→ 运行测试
7. commit / push（独立分支）

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

- ❌ 一个工具仓库（不放业务代码）
- ❌ 一个生产项目（不部署服务）
- ❌ 一个题库（不缓存任何具体考题或考点）
- ❌ 一个院校信息库（不基于经验贴或过期年份填写招生数据）

本仓库**是**：

- ✅ 学习路线的**总控**与**进度看板**
- ✅ 章节笔记骨架与错题归档系统
- ✅ Codex / Cursor / 编程 AI 协作的工作入口
- ✅ 长期可维护、初学者可读的文档体系

---

## 2. 当前总目标（v2026-05）

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

> **勿在此硬编码轮次列表。** 运行 `python3 scripts/round_status.py --summary` 查看概览 md / 实操骨架 / 进度接入的真实数量。  
> Agent 选下一任务：`python3 scripts/agent_gate.py --json`（见 `docs/NEXT_ACTIONS.md`）。

- 已完成 **Stage 0 · 仓库治理与学习系统准备**（路线骨架 + 四主线进度系统 v2）。
- **进度闭环**（`progress.json` + 练习脚本 `mark_done` + 看板任务清单）：以 `scripts/round_status.py` 输出的 `full_loop_rounds` 为准（当前为 Round 00–04）。
- **最小实操骨架**（`rounds/round_XX/` 目录齐全、尚未接入进度）：见 `scaffold_only_rounds`（当前为 Round 05–21）。
- 下一步队列与优先级：见 [`docs/NEXT_ACTIONS.md`](docs/NEXT_ACTIONS.md) 顶部「推荐下一步」。

---

## 5. 仓库结构

```
~/PycharmProjects/computer_study_plan/   ← 唯一 Git 工作副本（见 docs/WORKSPACE.md）
├─ README.md                       ← 本文件（仓库入口）
├─ docs/WORKSPACE.md               ← ★ 路径与工作区约定（单一事实源）
├─ AGENTS.md                       ← Codex / Cursor / 编程 AI 协作硬规则
├─ CONVERSION_PROTOCOL.md          ← Round md 与进度系统协议（v2.0）
├─ progress.html                   ← 进度看板（四主线 + 阶段 + 倒计时）
├─ progress.json                   ← 进度状态唯一来源（v2 + lanes）
├─ progress_data.js                ← 进度镜像（mark_done.sh 自动生成）
├─ mark_done.sh                    ← 进度 CLI（支持按 lane 分组）
├─ .gitignore
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
│  ├─ CODEX_LONG_TERM_PLAN.md      ← 项目长期目标与阶段路线
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
├─ records/                        ← 用户真实学习记录（默认禁止删除）
│  ├─ README.md
│  ├─ weekly_reviews/              ← 每周复盘（YYYY-WW.md）
│  ├─ error_notes/                 ← 错题本（按 lane / module 归档）
│  └─ completed_tasks/             ← 完成的练习快照（可选）
│
└─ rounds/                         ← Round 实操目录（仅可执行内容进此）
   ├─ round_00/ … round_21/        ← 工程线 22 轮（层级见 round_status 扫描）
   └─ stage_03_vps_remote_ops/     ← VPS 远程实操支线（13 份 Round 文档）
```

**轮次三层含义（避免混淆）**

| 层级 | 含义 | 如何查看 |
|------|------|----------|
| 概览文档 | 根目录 `round_XX.md` 大纲 | `ls round_*.md` |
| 实操骨架 | `rounds/round_XX/` 含 week1–3 + final | `python3 scripts/round_status.py` |
| 进度闭环 | 任务在 `progress.json` 且练习可 `mark_done` | 字段 `full_loop_rounds` |

> Round md（`round_00.md` ~ `round_21.md`）是**工程实操线素材库**；「骨架已存在」≠「你已学完」≠「已接入进度看板打卡」。

---

## 6. 如何使用本仓库

### 6.1 第一次进入仓库

```bash
cd ~/PycharmProjects/computer_study_plan   # 或你的克隆路径，见 docs/WORKSPACE.md
test -f progress.json && test -f mark_done.sh && echo "OK: 仓库根"
python3 scripts/check_user_journey.py      # 用户旅程自检（生成审计报告）
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
- 工作日完成任务后：`bash mark_done.sh <task-id>`。
- 错题录入 `records/error_notes/<lane>/<module>/...`。
- 周末写复盘。

### 6.3 看进度

- **方式一（推荐）**：双击 `progress.html`，浏览器打开。完成练习后按 `⌘R` 刷新。
- **方式二（自动刷新）**：
  ```bash
  cd ~/PycharmProjects/computer_study_plan
  python3 -m http.server 8000
  open http://localhost:8000/progress.html
  ```

看板包含：

- 总进度
- 四主线进度（engineering / soft_exam / math2 / cs408）
- 本周任务（localStorage）
- 考试倒计时（localStorage）
- 阶段进度（Stage 0–7）
- 当前薄弱项（自动识别完成率 < 30% 且任务数 ≥ 5 的 lane）
- 按 lane / Round 浏览（元数据来自 `progress_rounds.json`；进度任务仅覆盖已接入轮次，见 `round_status.py`）

### 6.4 进度系统 CLI

在仓库根目录执行：

```bash
cd ~/PycharmProjects/computer_study_plan
bash mark_done.sh                # 查看所有任务（按 lane 分组）
bash mark_done.sh <task-id>      # 标记完成
bash mark_done.sh <task-id> --undo  # 取消完成
```

---

## 7. 文档导航

| 我想... | 看哪里 |
|---|---|
| 确认本机仓库 / IDE 应打开哪个目录 | `docs/WORKSPACE.md` |
| 看总目标 | `docs/MASTER_STUDY_ROADMAP.md` |
| 看现在该做什么阶段 | `docs/STAGE_PLAN.md` |
| 看某个知识点属于哪条 lane | `docs/KNOWLEDGE_MAPPING.md` |
| 设计本周节奏 | `docs/WEEKLY_EXECUTION_TEMPLATE.md` |
| 看进度系统规则 | `docs/PROGRESS_RULES.md` + `CONVERSION_PROTOCOL.md` |
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

- 轮次状态表、README「当前阶段」、看板 Round 列表：**禁止手工维护完整枚举**；以 `scripts/round_status.py` + `scripts/generate_progress_rounds.py` 为准。
- 不随意新增重复文档；任何新计划必须挂到总路线（`docs/MASTER_STUDY_ROADMAP.md`）。
- 所有学习任务必须能对应到某个 Stage（`docs/STAGE_PLAN.md`）。
- 每周至少一次复盘（`records/weekly_reviews/YYYY-WW.md`）。
- 错题归档到 `records/error_notes/<lane>/<module>/`，不写在 `plans/`。
- 不缓存任何具体考题 / 考纲条目 / 院校招生数据；涉及考试一律以**最新官方信息**为准。
- 不删除以下高保护对象（详见 `docs/governance/repo_rules.md`）：
  - `rounds/round_00/`、`round_00.md` ~ `round_21.md`
  - `progress.json`、`progress_data.js`、`progress.html`、`mark_done.sh`
  - `records/` 下任何已写入的真实学习记录
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
- ✅ 可按需在 `rounds/round_XX/` 展开实操目录（当前 22 轮均有最小骨架；进度接入情况运行 `python3 scripts/round_status.py`）
- ✅ 数据结构、算法、网络、Linux 等 Round 内容会作为软考 / 408 模块的辅助素材（参考 `docs/KNOWLEDGE_MAPPING.md`）
- ❌ 不替代 `plans/soft_exam/` 与 `plans/408/` 中的专项考试笔记

---

## 11. 致使用者

- 这条路线长度按年计，节奏需要**长期可持续 > 短期高强度**。
- 错题本是知识体系最重要的指针，而不是炫学习量的工具。
- 数学二每周保底一道题，**永不为 0**。
- 不要把 21 份 Round 概览的"已存在"误以为"已完成"——它们只是大纲。
- 院校信息**不要凭印象填**，必须查官网。

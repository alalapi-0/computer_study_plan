# Round 文档与进度系统协议 v2.1

> **用途**：本文件规定仓库内"Round 概览文档（`round_XX.md`）"与"Round 实操目录（`rounds/round_XX/`）"的标准结构，以及当前进度系统（`progress.json` / `progress_data.js` / `rounds_data.js` / `progress.html` / `progress_ui.js` / `scripts/progress_server.py` / `mark_done.sh` / 动作日志 / 任务反馈）的维护规则。
> 每次新增或修改 Round 时，需严格遵守本协议，并同步更新 `README.md`。

---

## 1. 协议版本说明

| 字段 | 值 |
|------|----|
| **当前版本** | v2.1 |
| **生效日期** | 2026-05-12 |
| **覆盖范围** | 主线 Round 00–21 + 阶段性支线（VPS / 软考 / 408 / 数学二 / 0854 等） |
| **重大变更** | v2.0 移除"txt → md 转换"流程；`plan_round_XX.txt` 已于 2026-05-12 全部删除；本协议改为只面向 md |

> **历史说明**：v1.0 ~ v1.3 时仓库中存在 `plan_round_00.txt` ~ `plan_round_21.txt`（22 份初版提示词文本），用于通过本协议批量生成 `round_XX.md`。这些 txt 在路线重定向时由用户授权统一删除（理由：md 已独立完整、txt 属于历史副本，无独立维护价值）。

---

## 2. 触发条件

以下任一情况发生时，必须执行本协议：

1. 新增 `round_XX.md`（无论是直接写还是由 AI 生成）
2. 修改已有 `round_XX.md` 的结构或主题
3. 在 `rounds/round_XX/` 下新建实操目录或练习脚本
4. 进度系统相关文件需要新增任务 ID

---

## 3. Round 概览文档（`round_XX.md`）标准结构

每个 `round_XX.md` 必须包含以下所有区块，**顺序不可调换**：

### 3.1 文件头

```markdown
# Round XX · [简短主题名]

> **定位**：[一句话说明这轮聚焦什么、解决什么问题]
```

### 3.2 概览表（必填）

```markdown
## 概览

| 项目 | 内容 |
|------|------|
| **主题** | [3-5 个关键技术，用 ` + ` 分隔] |
| **难度** | [⭐ 评级，1-5 颗星] |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | [前置轮次，如：Round XX] |
| **下一轮** | [下一轮编号和名称] |
| **所属主线** | engineering / soft_exam / math2 / cs408（多选用 `+` 分隔） |
```

**难度评级标准：**

| 评级 | 含义 |
|------|------|
| ⭐☆☆☆☆ | 极简入门，零基础可直接上手 |
| ⭐⭐☆☆☆ | 基础，需要前置轮次知识 |
| ⭐⭐⭐☆☆ | 需要练习才能掌握，有一定复杂度 |
| ⭐⭐⭐⭐☆ | 较高复杂度，工程实践为主 |
| ⭐⭐⭐⭐⭐ | 高难度，多系统集成 |

### 3.3 本轮目标（必填）

```markdown
## 本轮目标

完成本轮后，你能做到：

- [ ] [具体、可验证的能力描述，用 "能..."]
```

写作规则：

- 每项以动词开头：能解释 / 能独立完成 / 会用
- 每轮 4–8 条
- 必须可被"验收标准"逐条验证

### 3.4 本轮不学什么（必填）

```markdown
## 本轮不学什么

> 先不碰：[用顿号分隔的技术/主题列表]
```

写作规则：明确排除本轮不涉及但相关的技术，1–2 行。

### 3.5 推荐资源表（必填）

```markdown
## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| [图标] [类型] | [标题]（官方 URL） | [1 句话说明该读什么、为什么有用] |
```

图标约定：

| 图标 | 含义 |
|------|------|
| 📄 | 官方文档/参考手册 |
| 🎬 | 视频教程 |
| 📖 | 教程/指南 |
| 🗺️ | 交互练习/轻量补充 |
| 📚 | 参考书/扩展阅读 |
| 🐳 | Docker/容器相关 |
| 🚀 | 运行时/工具 |
| 📦 | 格式规范/库 |
| 🎓 | 考试大纲/真题 |

写作规则：

- 每轮 3–6 条
- 只放官方文档；不要放可能失效的第三方教程
- "说明"列必须写"读哪部分"或"为什么有用"

### 3.6 3 周学习安排（必填）

```markdown
## 3 周学习安排

### 第 1 周：[子主题名]

**目标**：[一句话单一目标]

**本周主练**：[命令/工具/模块/章节列表]

（可选）**建议安排**：时间分配

（可选）**第 1 周自测**：可独立完成的小任务

---

### 第 2 周：[子主题名]
...

### 第 3 周：[子主题名]
...
```

### 3.7 本轮练习清单（必填）

```markdown
## 本轮练习清单

### 准备工作

\```bash
# 创建练习目录的命令
\```

### 第 1 周练习

**练习 N**：[练习名称]
\```python/bash
# 可直接运行的完整代码
\```

### 第 2 周练习
...

### 第 3 周练习
...

### 综合练习

\```bash/python
# 把本轮所有技能整合的完整演示
\```
```

写作规则（关键）：

- **所有代码必须可直接运行**，不能是伪代码或片段
- 第 1 周练习要有具体的测试数据创建命令
- 每段代码有注释说明"为什么这样写"
- 每个练习 10–40 行，最多不超过 60 行

### 3.8 验收标准（必填）

```markdown
## 验收标准

- [ ] [能力/产出描述，对应"本轮目标"里的每一条]
```

写作规则：与"本轮目标"一一对应；必须可演示或运行验证；4–8 条。

### 3.9 最容易踩的坑（必填）

```markdown
## ⚠️ 最容易踩的坑

1. **[坑的名称]** — [一句话描述正确做法]
```

写作规则：3–4 条，每条 1 行；格式固定：`**粗体描述问题** — 正确做法`。

---

## 4. 可选区块

按需添加，不是所有轮次都必须有：

### 4.1 建议的项目结构

适用于：有实际项目输出的轮次（如 Round 07–17）。

### 4.2 路线说明

适用于：在分叉路线节点上的轮次（如 Round 08）。

### 4.3 速查表

适用于：有多个对比概念的轮次。

### 4.4 考试映射

适用于：与软考 / 408 / 数学二相关的轮次。表格列：本轮内容 / 软考考点 / 408 考点 / 数学二章节。

---

## 5. 新增 Round 的完整流程

```
1. 直接编写 round_XX.md（按本协议 Section 3 结构）
   ↓
2. 创建 rounds/round_XX/ 目录及所有文件（按 Section 7 规范）
   ↓
3. 注册任务与显示元数据
   - 工程 Round 优先更新 `scripts/build_rounds_data.py` 的生成规则，然后运行 `npm run build:rounds`
   - 计划类任务同样通过当前生成脚本或明确的数据维护点注册，不直接改 `progress.html`
   - `progress.json` 中新增任务默认 done: false，必填 lane 字段（engineering / soft_exam / math2 / cs408 之一）
   ↓
4. 同步衍生数据
   - 运行 `npm run build:rounds` 生成 `rounds_data.js` 并合并工程 Round 任务
   - 必要时运行 `npm run sync:progress` 只同步 `progress_data.js`
   - 任务反馈需要更新时运行 `python3 scripts/generate_task_feedback.py`
   ↓
5. 验证 Web UI 与 CLI
   - `bash mark_done.sh --lane engineering --limit 8`
   - `python3 scripts/progress_server.py` 后打开 `http://127.0.0.1:8777/progress.html?round=round_XX`
   ↓
6. 更新本文件（CONVERSION_PROTOCOL.md）：
   - Section 6 当前轮次状态表新增一行
   ↓
7. 更新 README.md：
   - "项目结构"新增 round_XX.md 和 rounds/round_XX/ 目录树
   - "全局路线图"（如有新分支）
   - "核心项目线索表"（如该轮推进了 ai_prep_tool）
```

---

## 6. 当前轮次状态

> 每次新增或修改轮次时更新此表

| 轮次 | 主题 | MD 状态 | 实操目录 | 所属主线 | 备注 |
|------|------|---------|---------|---------|------|
| Round 00 | Terminal 初见 | ✅ 完整 | ✅ 已展开 | engineering | 已展开并接入 Web UI；真实学习完成状态以 `progress.json` 为准 |
| Round 01 | 文件系统与基础命令 | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-28 完成 Round 01 最小目录骨架 |
| Round 02 | Shell、管道、Git | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-28 完成 Round 02 目录骨架 |
| Round 03 | Python 基础 + 复杂度 | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-28 完成 Round 03 最小目录骨架 |
| Round 04 | 核心数据结构 | ✅ 概览 | ✅ 已展开 | engineering + soft_exam + cs408 | 2026-05-28 完成 Round 04 最小目录骨架 |
| Round 05 | 高频算法模式 | ✅ 概览 | ✅ 已展开 | engineering + soft_exam + cs408 | 2026-05-28 完成 Round 05 最小目录骨架 |
| Round 06 | Linux 进阶与自动化 | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-28 完成 Round 06 最小目录骨架 |
| Round 07 | 面向 AI 项目综合练习 | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-29 完成 Round 07 最小目录骨架 |
| Round 08 | 总复盘与升级路线 | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-29 完成 Round 08 最小目录骨架 |
| Round 09 | 仓库规范化与测试（路线 A） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-29 完成 Round 09 最小目录骨架 |
| Round 10 | Python 工程化基础（路线 A） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 10 最小目录骨架 |
| Round 11 | 本地持久化（路线 A） | ✅ 概览 | ✅ 已展开 | engineering + soft_exam | 2026-05-31 完成 Round 11 最小目录骨架 |
| Round 12 | 自动化流水线（路线 A） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 12 最小目录骨架 |
| Round 13 | 环境复现与发布（路线 A） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 13 最小目录骨架 |
| Round 14 | HTTP 与 API 设计（路线 B） | ✅ 概览 | ✅ 已展开 | engineering + soft_exam + cs408 | 2026-05-31 完成 Round 14 最小目录骨架 |
| Round 15 | FastAPI 基础（路线 B） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 15 最小目录骨架 |
| Round 16 | API 与数据层结合（路线 B） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 16 最小目录骨架 |
| Round 17 | 服务化收口（路线 B） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 17 最小目录骨架 |
| Round 18 | 数值计算与数据分析（路线 C） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 18 最小目录骨架 |
| Round 19 | 机器学习最小闭环（路线 C） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 19 最小目录骨架 |
| Round 20 | PyTorch 入门（路线 C） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 20 最小目录骨架 |
| Round 21 | NLP 前置基础（路线 C） | ✅ 概览 | ✅ 已展开 | engineering | 2026-05-31 完成 Round 21 最小目录骨架 |

> "所属主线"是 v2.0 新增字段，用于把现有工程实操内容映射到新增的多目标体系（详见 `docs/KNOWLEDGE_MAPPING.md`）。

---

## 7. `rounds/` 展开目录规范

每个 `rounds/round_XX/` 必须包含以下文件：

### 7.1 标准目录结构

```
rounds/round_XX/
├─ README.md                     ← 目录说明（必须）
├─ week1/
│  ├─ notes.md                   ← 第 1 周学习笔记（必须）
│  └─ exercises.sh 或 .py        ← 第 1 周练习脚本（必须）
├─ week2/
│  ├─ notes.md
│  └─ exercises.sh 或 .py
├─ week3/
│  ├─ notes.md
│  └─ exercises.sh 或 .py
└─ final/
   ├─ comprehensive_exercise.sh 或 .py  ← 综合练习（必须）
   └─ [cheatsheet 或 summary].md        ← 知识小抄或总结（必须）
```

### 7.2 notes.md 写作规则

- 对应该周 `round_XX.md` 中"3 周安排"的该周内容展开
- 必须包含：概念解释表格、命令/函数的参数说明、常见组合示例
- 每节末尾附"本周完成后你应该能回答"复选框列表
- 不写废话，重点放在"怎么用"

### 7.3 exercises.sh / .py 写作规则

- 开头注释说明：Round 编号、周次、主题、用法
- 开头注释列出本脚本对应 `progress.json` 中的任务 ID
- 每个练习前有清晰分隔线和说明
- 脚本可以有提示信息（`echo ">>> ..."`），但核心命令由用户手敲
- 自测部分只提示题目，不直接给出答案命令
- Shell 脚本用 `#!/bin/bash`，Python 脚本用标准 shebang

### 7.4 脚本文件类型选择

| 轮次范围 | 主要语言 | 文件后缀 |
|---------|---------|---------|
| Round 00–06 | Bash | `.sh` |
| Round 07+ | Python | `.py` |
| 混合内容 | 按练习主题决定 | `.sh` 或 `.py` |

---

## 8. 进度系统维护规范

进度系统由数据文件、生成脚本、本地 API 和 Web UI 协同工作：

| 文件 | 作用 |
|------|------|
| `progress.json` | **唯一状态来源**，记录任务状态、时间戳与所属主线（lane） |
| `progress_data.js` | `progress.json` 的 JS 镜像，由工具生成，供前端只读加载和无 API 检查兜底 |
| `rounds_data.js` | Round / 计划分组与任务展示元数据，由 `scripts/build_rounds_data.py` 生成 |
| `scripts/progress_server.py` | 本地学习服务，提供 Web UI 写入、练习脚本运行、存档、动作日志等 API |
| `progress.html` / `progress_ui.js` | 学习工作区：内联教程、工程任务终端、任务清单、记录并完成、存档与复盘 |
| `mark_done.sh` | CLI 兼容工具，用于快速查看、补录完成或撤销任务状态 |
| `records/action_logs/events.jsonl` | Web UI / CLI 动作日志，用于回看与任务反馈 |
| `records/feedback/task_feedback.json` | 任务反馈镜像，由 `scripts/generate_task_feedback.py` 生成 |

> `progress_data.js`、`rounds_data.js` 和 `records/feedback/task_feedback.json` 由工具自动维护，**不可手动编辑**。
> 状态变更优先通过 Web UI 的 `记录并完成` / `撤销完成`，CLI 作为快速查看、补录完成和撤销工具保留。

### 8.1 progress.json 结构（v2 起）

```json
{
  "version": 2,
  "lanes": {
    "engineering": { "title": "工程实操线", "description": "Linux/Shell/Git/Python/工程化/服务化/AI 工程" },
    "soft_exam":   { "title": "软考中级线", "description": "默认软件设计师，高分/满分导向" },
    "math2":       { "title": "数学二线", "description": "高等数学 + 线性代数" },
    "cs408":       { "title": "408/0854 线", "description": "数据结构 + 计组 + 操作系统 + 计算机网络" }
  },
  "tasks": {
    "w1-read": { "done": false, "done_at": null, "lane": "engineering" }
  }
}
```

规则：

- 每次新增 Round，优先通过 `scripts/build_rounds_data.py` 生成或合并任务；只有计划类特殊任务才手动维护 `progress.json`
- `lane` 必填，必须是 `lanes` 中已注册的 key
- `task-id` 全局唯一，建议格式：`rXX-wN-taskShort`（如 `r01-w1-read`）；Round 00 沿用简写（`w1-read` 等）
- `done_at` 由 Web UI 本地 API 或 `mark_done.sh` 自动写入，格式 `YYYY-MM-DD HH:MM`
- 学习备注、证据路径和撤销动作进入 `records/action_logs/events.jsonl`

### 8.2 mark_done.sh 用法

```bash
# 查看紧凑状态
bash mark_done.sh

# 按主线查看前 N 个未完成任务
bash mark_done.sh --lane engineering --limit 8

# 查看完整任务
bash mark_done.sh --all

# 记录完成（CLI 补录）
bash mark_done.sh <task-id>

# 取消完成
bash mark_done.sh <task-id> --undo
```

### 8.3 `rounds_data.js` 展示元数据

Round / 计划任务展示元数据不写在 `progress.html` 内。工程 Round 由 `scripts/build_rounds_data.py` 生成到 `rounds_data.js`；必要时修改生成脚本，而不是手动编辑生成文件。

每个 Round 对象格式：

```js
{
  id: "round_XX",
  title: "Round XX · 主题",
  lane: "engineering",
  difficulty: "⭐⭐☆☆☆",
  duration: "3 周",
  weeks: [
    {
      id: "weekN",
      title: "第 N 周：子主题",
      tasks: [
        {
          id: "task-id",
          type: "reading|exercise|test|output",
          title: "任务描述",
          file: "对应文件路径"
        }
      ]
    }
  ]
}
```

### 8.4 任务类型

| type | 显示标签 | 触发方式 |
|------|---------|---------|
| `reading`  | 阅读 | Web UI 点击 `读教程` 后，通过 `记录并完成` 保存 |
| `exercise` | 练习 | Web UI `运行脚本` 执行白名单脚本；脚本可自动记录练习完成 |
| `test`     | 自测 | Web UI `终端练习` 中完成后，由用户 `记录并完成` |
| `output`   | 产出 | 用户完成小抄、验收或项目产物后 `记录并完成` |

### 8.5 打开 Web UI 学习工作区

**方式一（推荐 · 可写 Web UI）**：

```bash
cd ~/PycharmProjects/computer_study_plan
python3 scripts/progress_server.py
open http://127.0.0.1:8777/progress.html
```

也可以使用：

```bash
npm run serve
```

**方式二（只读检查）**：双击 `progress.html` 或用普通静态服务器打开，只适合看布局和只读进度；没有写 API、练习脚本运行、动作日志和浏览器终端能力，不作为日常学习入口。

---

## 9. 文件命名规范（速查）

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| 主线 Round 概览 | `round_XX.md` | `round_22.md` |
| 主线 Round 实操目录 | `rounds/round_XX/` | `rounds/round_22/` |
| 阶段性支线目录 | `rounds/stage_NN_<scope>/` | `rounds/stage_03_vps_remote_ops/` |
| 阶段性支线 Round | `round_<scope>_XX_<title>.md` | `round_vps_05_first_readonly_check.md` |
| 周学习笔记 | `rounds/round_XX/weekN/notes.md` | `rounds/round_00/week1/notes.md` |
| 周练习脚本 | `rounds/round_XX/weekN/exercises.sh` 或 `.py` | — |
| 综合练习 | `rounds/round_XX/final/comprehensive_exercise.sh` 或 `.py` | — |
| 命令/知识小抄 | `rounds/round_XX/final/command_cheatsheet.md` 或类似 | — |
| 轮次目录说明 | `rounds/round_XX/README.md` | — |
| 学习计划专题目录 | `plans/<scope>/...` | `plans/soft_exam/`、`plans/math2/`、`plans/408/` |
| 学习记录目录 | `records/<scope>/...` | `records/weekly_reviews/`、`records/error_notes/` |

详细规则见 `docs/governance/file_naming_rules.md`。

---

## 10. 路线与轮次关系

仓库目前并行维护以下学习线：

```
工程实操线（engineering）
├─ 主线 Round 00–08：终端 / Python / 数据结构 / 算法 / Linux / 综合
└─ 主线 Round 09–21：工程化 / 服务化 / AI/ML（路线 A / B / C）

软考中级线（soft_exam）
├─ plans/soft_exam/：默认软件设计师
└─ Stage 2 + Stage 3（详见 docs/STAGE_PLAN.md）

数学二线（math2）
└─ plans/math2/：高等数学 + 线性代数（长期低强度推进）

408 / 0854 线（cs408）
├─ plans/408/：数据结构 + 计组 + 操作系统 + 网络
└─ docs/GRADUATE_SCHOOL_TRACKER.md：院校跟踪

支线
└─ rounds/stage_03_vps_remote_ops/：VPS 远程实操（Level 0–5 权限）
```

详细总目标与耦合关系见 `docs/MASTER_STUDY_ROADMAP.md`。

---

## 11. 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-04-11 | 初始版本，覆盖 Round 00–21（基于 txt → md 转换流程） |
| v1.1 | 2026-04-11 | 新增 `rounds/` 展开目录规范、进度系统维护规范、完整新增流程 |
| v1.3 | 2026-04-11 | 新增 `progress_data.js` 作为 JS 镜像，支持 file:// 双击打开 |
| v2.0 | 2026-05-12 | **重大变更**：移除"txt → md 转换"全部流程；删除 22 份 `plan_round_XX.txt`；progress 数据结构升级到 v2（新增 `lanes` 与 `tasks[].lane`）；新增多主线（engineering / soft_exam / math2 / cs408） |
| v2.1 | 2026-07-06 | 将新增 Round 流程、进度系统职责和 Web UI 打开方式同步为当前 `progress_server.py` + Web UI + 生成脚本模型 |

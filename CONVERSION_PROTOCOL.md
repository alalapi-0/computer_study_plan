# Round 文档与进度系统协议 v2.1

> **用途**：本文件规定仓库内"Round 概览文档（`round_XX.md`）"与"Round 实操目录（`rounds/round_XX/`）"的标准结构，以及当前进度系统（`progress.json` / `progress_data.js` / `rounds_data.js` / `progress.html` / `progress_ui.js` / `scripts/progress_server.py` / `mark_done.sh` / 动作日志 / 任务反馈）的维护规则。
> 每次新增或修改 Round 时，需严格遵守本协议，并同步更新 `README.md`。

---

## 1. 协议版本说明

| 字段 | 值 |
|------|----|
| **当前版本** | v2.2 |
| **生效日期** | 2026-07-18（v2.2；v2.1 为 2026-07-06；v2.0 为 2026-05-12） |
| **覆盖范围** | Linux 正式课程兼容 Round：`round_00` / `01` / `02` / `06` + VPS 支线；课程注册见 `content/courses/linux-foundations/` |
| **重大变更** | v2.2 收敛为 `linux-foundations` 单课程；删除非 Linux 正式 Round 与考试计划入口；进度 lane 仅保留 `linux-foundations` |

> **历史说明**：旧版曾覆盖 Round 00–21 与软考/数学二/408 多主线；相关内容已按 `docs/REMOVAL_MANIFEST.md` 移出工作树，可从备份标签恢复。

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
| **所属主线** | `linux-foundations`（当前唯一正式课程 lane） |
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

### 4.4 课程模块映射

适用于：需要标明所属 Linux 模块的轮次。表格列：本轮内容 / Module ID / 关键技能 / 通关验收。

当前正式课程只有 `linux-foundations`；不再维护考试映射表。

---

## 5. 新增 Round 的完整流程

```
1. 确认该 Round 属于 linux-foundations，并更新 content/courses/linux-foundations/course.json
   ↓
2. 直接编写 round_XX.md（按本协议 Section 3 结构）
   ↓
3. 创建 rounds/round_XX/ 目录及所有文件（按 Section 7 规范）
   ↓
4. 注册任务与显示元数据
   - 更新 `scripts/build_rounds_data.py` 的生成规则，然后运行 `npm run build:rounds`
   - `progress.json` 中新增任务默认 done: false，lane 必须为 `linux-foundations`
   ↓
5. 同步衍生数据
   - `npm run build:rounds`
   - 必要时 `npm run sync:progress`
   - 需要时 `python3 scripts/generate_task_feedback.py`
   ↓
6. 验证 Web UI 与 CLI
   - `bash mark_done.sh --lane linux-foundations --limit 8`
   - `python3 scripts/progress_server.py` 后打开 `http://127.0.0.1:8777/progress.html?round=round_XX`
   ↓
7. 更新本文件 Section 6 状态表，并同步 README / PROJECT_STATE
```

---

## 6. 当前轮次状态

> 每次新增或修改轮次时更新此表

| 轮次 | 主题 | MD 状态 | 实操目录 | 所属课程 | 备注 |
|------|------|---------|---------|---------|------|
| Round 00 | Terminal 初见 | ✅ 完整 | ✅ 已展开 | linux-foundations | Module 00；真实完成状态以 `progress.json` 为准 |
| Round 01 | 文件系统与基础命令 | ✅ 完整 | ✅ 已展开 | linux-foundations | Module 01 |
| Round 02 | Shell、管道、Git | ✅ 完整 | ✅ 已展开 | linux-foundations | Module 02；Git 为邻接实践 |
| Round 06 | Linux 进阶与自动化 | ✅ 完整 | ✅ 已展开 | linux-foundations | Module 03 |
| VPS 支线 | 远程实操（只读优先） | ✅ 文档 | ✅ 已展开 | linux-foundations | Module 04；`rounds/stage_03_vps_remote_ops/` |

> Round 03–05、07–21 已从工作树移除，见 `docs/REMOVAL_MANIFEST.md`。
> “所属课程”在单课程阶段固定为 `linux-foundations`（详见 `docs/KNOWLEDGE_MAPPING.md`）。

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
  "active_course_id": "linux-foundations",
  "lanes": {
    "linux-foundations": {
      "title": "Linux 基础与工程实践",
      "description": "当前唯一正式课程",
      "course_id": "linux-foundations"
    }
  },
  "tasks": {
    "w1-read": { "done": false, "done_at": null, "lane": "linux-foundations" }
  }
}
```

规则：

- 每次新增 Round，优先通过 `scripts/build_rounds_data.py` 生成或合并任务
- `lane` 必填，当前只能是 `linux-foundations`
- `task-id` 全局唯一，建议格式：`rXX-wN-taskShort`（如 `r01-w1-read`）；Round 00 沿用简写（`w1-read` 等）
- `done_at` 由 Web UI 本地 API 或 `mark_done.sh` 自动写入，格式 `YYYY-MM-DD HH:MM`
- 学习备注、证据路径和撤销动作进入 `records/action_logs/events.jsonl`

### 8.2 mark_done.sh 用法

```bash
# 查看紧凑状态
bash mark_done.sh

# 按主线查看前 N 个未完成任务
bash mark_done.sh --lane linux-foundations --limit 8

# 查看完整任务
bash mark_done.sh --all

# 记录完成（CLI 补录）
bash mark_done.sh <task-id>

# 取消完成
bash mark_done.sh <task-id> --undo
```

### 8.3 `rounds_data.js` 展示元数据

Round / 计划任务展示元数据不写在 `progress.html` 内。Linux 课程 Round 由 `scripts/build_rounds_data.py` 生成到 `rounds_data.js`；必要时修改生成脚本，而不是手动编辑生成文件。

每个 Round 对象格式：

```js
{
  id: "round_XX",
  title: "Round XX · 主题",
  lane: "linux-foundations",
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
| 学习计划专题目录 | `plans/<scope>/...` | 当前仅 `plans/linux/` |
| 学习记录目录 | `records/<scope>/...` | `records/weekly_reviews/`、`records/error_notes/` |

详细规则见 `docs/governance/file_naming_rules.md`。

---

## 10. 路线与轮次关系

当前只维护一门正式课程：

```
linux-foundations
├─ Module 00 ← Round 00
├─ Module 01 ← Round 01
├─ Module 02 ← Round 02
├─ Module 03 ← Round 06
└─ Module 04 ← rounds/stage_03_vps_remote_ops/
```

课程注册：`content/courses/linux-foundations/course.json`
详细目标见 `docs/MASTER_STUDY_ROADMAP.md` 与 `docs/ROADMAP.md`。

---

## 11. 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-04-11 | 初始版本，覆盖 Round 00–21（基于 txt → md 转换流程） |
| v1.1 | 2026-04-11 | 新增 `rounds/` 展开目录规范、进度系统维护规范、完整新增流程 |
| v1.3 | 2026-04-11 | 新增 `progress_data.js` 作为 JS 镜像，支持 file:// 双击打开 |
| v2.0 | 2026-05-12 | **重大变更**：移除"txt → md 转换"全部流程；删除 22 份 `plan_round_XX.txt`；progress 数据结构升级到 v2（新增 `lanes` 与 `tasks[].lane`）；新增多主线（engineering / soft_exam / math2 / cs408） |
| v2.1 | 2026-07-06 | 将新增 Round 流程、进度系统职责和 Web UI 打开方式同步为当前 `progress_server.py` + Web UI + 生成脚本模型 |
| v2.2 | 2026-07-18 | 收敛为 `linux-foundations` 单课程；移除非 Linux 正式 Round 与考试计划；进度 lane 仅保留 linux-foundations |

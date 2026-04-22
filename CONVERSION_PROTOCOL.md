# Round MD 生成协议 v1.0

> **用途**：本文件是将 `plan_round_XX.txt` 转换为结构化 `round_XX.md` 的操作协议。  
> 每次新增轮次或更新现有轮次时，需严格遵守本协议，并同步更新 `README.md`。

---

## 1. 协议版本说明

| 字段 | 值 |
|------|----|
| **当前版本** | v1.3 |
| **生效日期** | 2026-04-11 |
| **覆盖轮次** | Round 00–21 |
| **维护规则** | 每次新增或大幅修改轮次时，更新本文件的"版本历史"和"当前轮次状态"两节 |

---

## 2. 触发条件

以下任一情况发生时，必须执行本协议：

1. 新增 `plan_round_XX.txt` 文件，需要生成对应 `round_XX.md`
2. 修改已有 `plan_round_XX.txt`，需要同步更新对应 `round_XX.md`
3. 需要向仓库新增不在现有 txt 中的轮次（直接写 md，跳过 txt）

---

## 3. 标准 MD 文件结构

每个 `round_XX.md` 必须包含以下所有区块，**顺序不可调换**：

### 3.1 文件头

```markdown
# Round XX · [简短主题名]

> **定位**（可选的路线标注）：[一句话说明这轮的定位，告诉学习者这轮聚焦什么、解决什么问题]
```

**示例：**
```markdown
# Round 07 · 面向 AI 项目的综合练习

> **定位**：把前面学过的东西真正串起来，做一个能处理真实小数据文件、能从命令行运行、能输出结果和日志的小工具。
```

---

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
```

**难度评级标准：**
| 评级 | 含义 |
|------|------|
| ⭐☆☆☆☆ | 极简入门，零基础可直接上手 |
| ⭐⭐☆☆☆ | 基础，需要前置轮次知识 |
| ⭐⭐⭐☆☆ | 需要练习才能掌握，有一定复杂度 |
| ⭐⭐⭐⭐☆ | 较高复杂度，工程实践为主 |
| ⭐⭐⭐⭐⭐ | 高难度，多系统集成 |

---

### 3.3 本轮目标（必填）

```markdown
## 本轮目标

完成本轮后，你能做到：

- [ ] [具体、可验证的能力描述，用 "能..."]
- [ ] [...]
```

**写作规则：**
- 每项目标必须以动词开头，如"能解释"、"能独立完成"、"会用"
- 每轮 4-8 条
- 必须可以被"验收标准"一节验证

---

### 3.4 本轮不学什么（必填）

```markdown
## 本轮不学什么

> 先不碰：[用顿号或逗号分隔的技术列表]
```

**写作规则：**
- 明确排除本轮不涉及但相关的技术
- 1-2 行，不用展开解释
- 目的是帮助学习者聚焦，防止跑题

---

### 3.5 推荐资源表（必填）

```markdown
## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| [图标] [类型] | [[标题](URL)] | [1句话说明该读什么、为什么有用] |
```

**图标约定：**
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

**写作规则：**
- 每轮 3-6 条资源
- 只放官方文档，不放可能失效的第三方教程
- 说明列必须写"该读哪部分"或"为什么有用"

---

### 3.6 3 周学习安排（必填）

```markdown
## 3 周学习安排

### 第 1 周：[子主题名]

**目标**：[一句话说明这周的单一目标]

**本周主练**：[命令/工具/模块列表]

（可选：**建议安排** 时间分配）

（可选：**第 1 周自测** 可独立完成的小任务）

---

### 第 2 周：[子主题名]

...

### 第 3 周：[子主题名]

...
```

**写作规则：**
- 每周聚焦一个子主题
- "本周主练"是这周的核心工具/命令
- 自测任务是该周结束的检查点，帮助学习者自我评估

---

### 3.7 本轮练习清单（必填）

```markdown
## 本轮练习清单

### 准备工作

\```bash
# 创建练习目录的命令
\```

---

### 第 1 周练习

**练习 N**：[练习名称]
\```python/bash
# 可直接运行的完整代码
# 注释说明代码意图
\```

### 第 2 周练习

...

### 第 3 周练习

...

### 综合练习（推荐包含）

\```bash/python
# 把本轮所有技能整合的完整演示
\```
```

**写作规则（关键）：**
- **所有代码必须可直接运行**，不能是伪代码或片段
- 第 1 周练习要有具体的测试数据创建命令（如 `echo "..." > file.txt`）
- 每段代码有注释说明"为什么这样写"
- 综合练习要把本轮所有能力串起来
- 代码量要适中：每个练习 10-40 行，不要超过 60 行

---

### 3.8 验收标准（必填）

```markdown
## 验收标准

- [ ] [能力/产出描述，对应"本轮目标"里的每一条]
- [ ] [...]
```

**写作规则：**
- 与"本轮目标"一一对应
- 必须是可以"演示"或"运行验证"的，不是"理解了"之类主观描述
- 4-8 条

---

### 3.9 最容易踩的坑（必填）

```markdown
## ⚠️ 最容易踩的坑

1. **[坑的名称]** — [一句话描述正确做法]
2. **[坑的名称]** — [...]
3. ...
```

**写作规则：**
- 3-4 条，每条 1 行
- 格式固定：`**粗体描述问题** — 正确做法`
- 来自 txt 文件中明确提到的常见错误

---

## 4. 可选区块

以下区块按需添加，不是所有轮次都必须有：

### 4.1 建议的项目结构

适用于：有实际项目输出的轮次（如 Round 07-17）

```markdown
## 建议的项目结构

\```
project/
├─ file1.py
├─ file2.py
└─ ...
\```
```

### 4.2 路线说明

适用于：在分叉路线节点上的轮次（如 Round 08）

```markdown
## 后续路线说明

| 路线 | 内容 | 从哪轮开始 |
|------|------|-----------|
| **路线 A** | ... | Round XX |
```

### 4.3 速查表

适用于：有多个对比概念的轮次（如 Round 19 的指标对比）

```markdown
## [主题] 速查

| 操作 | 工具1 | 工具2 |
|------|-------|-------|
```

---

## 5. 从 TXT 转换 MD 的操作步骤

当拿到一个 `plan_round_XX.txt` 时，按以下步骤处理：

### Step 1：读取并识别 txt 结构

txt 文件通常包含：
- **Round 定位段**：第一段，说明这轮做什么、不做什么
- **资源段**：列出推荐阅读材料
- **3 周安排段**：第 1/2/3 周各自的目标和建议
- **练习清单段**：按周组织的具体代码练习
- **验收标准段**：结尾的自测清单
- **最常见坑段**：结尾的注意事项

### Step 2：提取关键内容

| txt 中的内容 | 映射到 md 中的区块 |
|-------------|-----------------|
| 第一段定位说明 | 文件头 `> **定位**` |
| "这轮学什么/不学什么" | 本轮目标 + 本轮不学什么 |
| 推荐资源列表 | 推荐资源表 |
| "第 1/2/3 周..." | 3 周学习安排 |
| 练习 N：... 代码块 | 本轮练习清单 |
| "验收标准" 或 "最终自测清单" | 验收标准 |
| "最容易踩的坑" | ⚠️ 最容易踩的坑 |

### Step 3：补充 md 特有内容

以下内容在 txt 中通常没有，需要从上下文推断：

- **概览表的难度评级**：根据技术栈复杂度判断
- **代码注释**：在练习代码里加注释说明意图
- **综合练习**：从 txt 的"综合演练"或"周末小任务"整合而来

### Step 4：核验 checklist

生成 md 后，按以下列表检查：

- [ ] 文件头有定位说明
- [ ] 概览表包含所有 5 个字段
- [ ] 本轮目标有 4-8 条，动词开头
- [ ] 本轮不学什么有明确列表
- [ ] 推荐资源 3-6 条，有 URL 和说明
- [ ] 3 周安排每周有独立目标
- [ ] 练习清单代码可直接运行
- [ ] 验收标准对应本轮目标
- [ ] 最容易踩的坑 3-4 条

### Step 5：同步更新

生成或更新 md 后，必须同步：

1. **本文件（CONVERSION_PROTOCOL.md）**：
   - 更新"当前轮次状态"表
   - 如有结构变化，更新版本号

2. **README.md**：
   - 更新"项目结构"文件列表
   - 更新"全局路线图"（如有新分支）
   - 更新"核心项目线索：ai_prep_tool"表（如有新轮次推进项目）

---

## 6. 当前轮次状态

> 每次新增或修改轮次时更新此表

| 轮次 | 主题 | MD 状态 | TXT 来源 | 备注 |
|------|------|---------|---------|------|
| Round 00 | Terminal 初见 | ✅ 完整 | plan_round_00.txt | |
| Round 01 | 文件系统与基础命令 | ✅ 完整 | plan_round_01.txt | |
| Round 02 | Shell、管道、Git | ✅ 完整 | plan_round_02.txt | |
| Round 03 | Python 基础 + 复杂度 | ✅ 完整 | plan_round_03.txt | |
| Round 04 | 核心数据结构 | ✅ 完整 | plan_round_04.txt | |
| Round 05 | 高频算法模式 | ✅ 完整 | plan_round_05.txt | |
| Round 06 | Linux 进阶与自动化 | ✅ 完整 | plan_round_06.txt | |
| Round 07 | 面向 AI 项目综合练习 | ✅ 完整 | plan_round_07.txt | 核心工程项目起点 |
| Round 08 | 总复盘与升级路线 | ✅ 完整 | plan_round_08.txt | 三路线分叉点 |
| Round 09 | 仓库规范化与测试（路线 A） | ✅ 完整 | plan_round_09.txt | |
| Round 10 | Python 工程化基础（路线 A） | ✅ 完整 | plan_round_10.txt | |
| Round 11 | 本地持久化（路线 A） | ✅ 完整 | plan_round_11.txt | |
| Round 12 | 自动化流水线（路线 A） | ✅ 完整 | plan_round_12.txt | |
| Round 13 | 环境复现与发布（路线 A） | ✅ 完整 | plan_round_13.txt | |
| Round 14 | HTTP 与 API 设计（路线 B） | ✅ 完整 | plan_round_14.txt | |
| Round 15 | FastAPI 基础（路线 B） | ✅ 完整 | plan_round_15.txt | |
| Round 16 | API 与数据层结合（路线 B） | ✅ 完整 | plan_round_16.txt | |
| Round 17 | 服务化收口（路线 B） | ✅ 完整 | plan_round_17.txt | |
| Round 18 | 数值计算与数据分析（路线 C） | ✅ 完整 | plan_round_18.txt | |
| Round 19 | 机器学习最小闭环（路线 C） | ✅ 完整 | plan_round_19.txt | |
| Round 20 | PyTorch 入门（路线 C） | ✅ 完整 | plan_round_20.txt | |
| Round 21 | NLP 前置基础（路线 C） | ✅ 完整 | plan_round_21.txt | |

---

## 7. 新增轮次流程

当需要新增 Round 22 及以后的轮次时，执行以下流程：

```
1. 将新的学习计划内容放入 plan_round_22.txt（可选，也可直接写 md）
   ↓
2. 按本协议 Section 3 的结构要求生成 round_22.md
   ↓
3. 核验 Section 5 Step 4 的 checklist
   ↓
4. 更新本文件（CONVERSION_PROTOCOL.md）：
   - Section 6 当前轮次状态表新增一行
   - 如有新的路线分支，更新 Section 8
   ↓
5. 更新 README.md：
   - 项目结构文件列表新增 round_22.md 一行
   - 全局路线图（如有新分支或延伸）
   - 核心项目线索表（如该轮推进了 ai_prep_tool）
```

---

## 8. 路线与轮次关系

```
地基层（Round 00-06）
└── 综合应用（Round 07）
    └── 收口与路线选择（Round 08）
        ├── 路线 A：工程化
        │   ├── Round 09：仓库规范化
        │   ├── Round 10：模块拆分
        │   ├── Round 11：SQLite 持久化
        │   ├── Round 12：批处理流水线
        │   └── Round 13：环境复现/Docker
        ├── 路线 B：服务化
        │   ├── Round 14：HTTP 基础
        │   ├── Round 15：FastAPI 基础
        │   ├── Round 16：API + 数据层
        │   └── Round 17：服务化收口
        └── 路线 C：AI/ML
            ├── Round 18：NumPy/pandas
            ├── Round 19：scikit-learn
            ├── Round 20：PyTorch
            └── Round 21：NLP 前置
```

> 建议顺序：A → B → C。先把工程基础站稳，再做服务化，最后上 AI/ML。

---

## 9. 文件命名规范

| 文件类型 | 命名格式 | 示例 |
|---------|---------|------|
| 学习计划原始 txt | `plan_round_XX.txt` | `plan_round_22.txt` |
| 结构化概览文档 | `round_XX.md` | `round_22.md` |
| 展开内容目录 | `rounds/round_XX/` | `rounds/round_22/` |
| 周学习笔记 | `rounds/round_XX/weekN/notes.md` | `rounds/round_00/week1/notes.md` |
| 周练习脚本 | `rounds/round_XX/weekN/exercises.sh` 或 `.py` | — |
| 综合练习 | `rounds/round_XX/final/comprehensive_exercise.sh` 或 `.py` | — |
| 命令/知识小抄 | `rounds/round_XX/final/command_cheatsheet.md` 或类似名 | — |
| 轮次目录说明 | `rounds/round_XX/README.md` | — |
| 本协议文件 | `CONVERSION_PROTOCOL.md` | — |
| 项目说明 | `README.md` | — |
| 进度看板 | `progress.html` | — |

> `XX` 为两位数字，不足两位补零（00, 01, ..., 09, 10, 11, ...）

---

## 10. rounds/ 展开目录规范

每个 `rounds/round_XX/` 必须包含以下文件：

### 10.1 标准目录结构

```
rounds/round_XX/
├─ README.md                     ← 目录说明（必须）
├─ week1/
│  ├─ notes.md                   ← 第1周学习笔记（必须）
│  └─ exercises.sh 或 .py        ← 第1周练习脚本（必须）
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

### 10.2 notes.md 写作规则

- 对应该周 `round_XX.md` 中"3 周安排"的该周内容展开
- 必须包含：概念解释表格、命令/函数的参数说明、常见组合示例
- 每节末尾附"本周完成后你应该能回答"复选框列表
- 不写废话，不写书本式定义，重点放在"怎么用"

### 10.3 exercises.sh / .py 写作规则

- 开头注释说明：Round 编号、周次、主题、用法
- 开头注释列出本脚本对应 progress.json 中的任务 ID
- 每个练习前有清晰分隔线和说明
- 脚本可以有提示信息（`echo ">>> ..."`），但核心命令由用户手敲
- 自测部分只提示题目，不直接给出答案命令
- Shell 脚本用 `#!/bin/bash`，Python 脚本用标准 shebang

### 10.4 脚本文件类型选择

| 轮次范围 | 主要语言 | 文件后缀 |
|---------|---------|---------|
| Round 00-06 | Bash | `.sh` |
| Round 07+ | Python | `.py` |
| 混合内容 | 按练习主题决定 | `.sh` 或 `.py` |

---

## 11. 进度系统维护规范

进度系统由三个文件协同工作：

| 文件 | 作用 |
|------|------|
| `progress.json` | **唯一状态来源**，记录每个任务的完成状态和时间戳 |
| `mark_done.sh` | 在终端标记任务完成，写入 `progress.json` |
| `progress.html` | 读取 `progress.json`，展示进度（需本地服务器，不能直接双击） |

> `progress.html` **不再允许在浏览器里手动勾选**，所有状态变更必须通过 `mark_done.sh` 进行。

### 11.1 progress.json 结构

```json
{
  "version": 1,
  "tasks": {
    "task-id": { "done": false, "done_at": null },
    "task-id": { "done": true,  "done_at": "2026-04-11 10:30" }
  }
}
```

**规则：**
- 每次新增 Round，在 `progress.json` 的 `tasks` 对象里追加该 Round 所有任务（默认 `done: false`）
- `task-id` 全局唯一，建议格式：`rXX-wN-taskShort`（如 `r01-w1-read`），Round 00 使用简写 `w1-read` 等
- `done_at` 由 `mark_done.sh` 自动写入，格式 `YYYY-MM-DD HH:MM`

### 11.2 mark_done.sh 用法

```bash
# 标记完成
bash mark_done.sh <task-id>

# 取消完成
bash mark_done.sh <task-id> --undo

# 查看所有任务状态
bash mark_done.sh
```

### 11.3 exercises.sh 调用约定

每个练习脚本必须：
1. 开头注释列出本脚本对应的所有任务 ID
2. 在对应练习完成后立即调用 `mark <task-id>`（mark 是脚本内定义的 `bash $REPO_ROOT/mark_done.sh` 别名）
3. 阅读类任务（`reading`）不在脚本里自动标记，需用户手动运行 `bash mark_done.sh <id>`

### 11.4 ROUNDS 数组（progress.html 中的静态元数据）

每个 Round 对象格式：

```js
{
  id: "round_XX",
  title: "Round XX · 主题",
  difficulty: "⭐⭐☆☆☆",
  duration: "3 周",
  weeks: [
    {
      id: "weekN",
      title: "第 N 周：子主题",
      tasks: [
        {
          id: "task-id",                                // 与 progress.json 中的 key 一致
          type: "reading|exercise|test|output",
          title: "任务描述",
          cmd: "bash mark_done.sh task-id 或 '自动'",  // 告知用户如何触发
          file: "对应文件路径"
        }
      ]
    }
  ]
}
```

### 11.5 任务类型说明

| type | 显示标签 | 触发方式 |
|------|---------|---------|
| `reading`  | 阅读 | 手动：`bash mark_done.sh <id>` |
| `exercise` | 练习 | 自动：运行 exercises.sh 时标记 |
| `test`     | 自测 | 自动：exercises.sh 中用户确认后标记 |
| `output`   | 产出 | 自动：综合练习脚本中确认后标记 |

### 11.0 进度文件说明

进度系统由四个文件协同工作：

| 文件 | 作用 |
|------|
| `progress.json` | **唯一真实来源**，记录每个任务的完成状态和时间戳，由 `mark_done.sh` 写入 |
| `progress_data.js` | `progress.json` 的 JS 镜像，由 `mark_done.sh` 自动同步生成，供 `progress.html` 在 `file://` 协议下读取 |
| `mark_done.sh` | CLI 工具，标记/取消任务，同时写入以上两个文件 |
| `progress.html` | 只读展示看板，优先 `fetch progress.json`（`http://`），回退读取 `progress_data.js`（`file://`）|

> `progress_data.js` 由工具自动维护，**不可手动编辑**。

### 11.6 打开进度看板

**方式一（推荐，最简单）**：
```bash
# 直接双击 progress.html，浏览器打开
# 完成练习后按 ⌘R 刷新即可
```

**方式二（支持自动刷新）**：
```bash
# 在仓库根目录
python3 -m http.server 8000

# 浏览器打开
open http://localhost:8000/progress.html
```

方式二下，看板每 30 秒自动刷新一次，也可点击「↻ 刷新」按钮。

---

## 12. 新增轮次完整流程（更新版）

```
1. 生成或提供 plan_round_XX.txt
   ↓
2. 生成 round_XX.md（按 Section 3 结构）
   ↓
3. 创建 rounds/round_XX/ 目录及所有文件（按 Section 10 规范）
   ↓
4. 在 progress.json 的 tasks 对象里追加该 Round 所有任务（默认 done: false）
   ↓
5. 运行一次 `bash mark_done.sh`（无参数）使 progress_data.js 同步更新
   ↓
6. 在 progress.html 的 ROUNDS 数组末尾追加该 Round 的静态元数据（按 Section 11.4 格式）
   ↓
6. 更新本文件（CONVERSION_PROTOCOL.md）：
   - Section 6 当前轮次状态表新增一行
   - Section 1 版本号（如结构有变化则升版本）
   ↓
7. 更新 README.md：
   - 项目结构：新增 round_XX.md 和 rounds/round_XX/ 目录树
   - 全局路线图（如有新分支或延伸）
   - 核心项目线索表（如该轮推进了 ai_prep_tool）
```

---

## 13. 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|---------|
| v1.0 | 2026-04-11 | 初始版本，覆盖 Round 00-21 |
| v1.1 | 2026-04-11 | 新增 rounds/ 展开目录规范（Section 10）、progress.html 维护规范（Section 11）、完整新增流程（Section 12） |
| v1.3 | 2026-04-11 | 新增 progress_data.js 作为 JS 镜像，支持 file:// 双击打开 progress.html；mark_done.sh 同步写入两个文件；移除"必须启动本地服务器"限制 |
| v1.3 | 2026-04-11 | 新增 progress_data.js 作为 JS 镜像，支持 file:// 双击打开 progress.html；mark_done.sh 同步写入两个文件；移除"必须启动本地服务器"限制 |

# Stage Plan · 阶段计划（v1.0）

> 本文档把 `docs/MASTER_STUDY_ROADMAP.md` 中的总目标拆成 **Stage 0 – Stage 7** 八个可推进阶段。
> 每个 Stage 列出：目标、产物、所属 lane、与现有 Round 的映射、对应软考 / 408 / 数学二模块、退出标准。
> 这是仓库内**唯一的阶段编号空间**。Round 编号和 Stage 编号是两套独立体系（详见 §11）。

---

## 0. 阅读指南

- Stage 编号代表**主推进序号**，但**多 Stage 可以并行**（特别是 Stage 4 数学二在 Stage 2/3/5 期间持续推进）。
- 阶段之间不是严格线性。每个 Stage 都有"启动条件"和"退出标准"，按你自己的节奏推进。
- 每个 Stage 都有"如果时间不够时优先做什么"的简化版本。

---

## Stage 0：仓库治理与学习系统准备

| 字段 | 内容 |
|---|---|
| 启动条件 | 任何时候 |
| 所属 lane | 跨 lane（治理） |
| 主要时长 | 1–2 周 |
| 现有 Round 映射 | 无（治理阶段） |
| 与考试关系 | 不直接对应任何考试 |

### 目标

- 整理仓库结构（删除 txt、建立 plans/records 目录、四主线进度）
- 明确学习路线（MASTER_STUDY_ROADMAP）
- 建立进度表 / 错题本模板 / 资料索引

### 产物（在路线重定向轮次中已经完成）

- `docs/MASTER_STUDY_ROADMAP.md`
- `docs/STAGE_PLAN.md`（本文件）
- `docs/KNOWLEDGE_MAPPING.md`
- `docs/WEEKLY_EXECUTION_TEMPLATE.md`
- `docs/PROGRESS_RULES.md`
- `docs/ERROR_REVIEW_SYSTEM.md`
- `docs/GRADUATE_SCHOOL_TRACKER.md`
- `docs/PROJECT_PORTFOLIO_TRACK.md`
- `plans/linux/README.md`、`plans/soft_exam/README.md`、`plans/math2/README.md`、`plans/408/README.md`
- `records/weekly_reviews/`、`records/error_notes/`、`records/completed_tasks/`
- progress.json / progress_data.js / mark_done.sh / progress.html 全部升级到四主线

### 退出标准

- [ ] 仓库内 `plan_round_XX.txt` 全部删除
- [ ] 所有路线骨架文档存在并可读
- [ ] `bash mark_done.sh` 仍可运行（Round 00 兼容）
- [ ] `progress.html` 能看到四主线总进度（哪怕目前都是 0%）
- [ ] README 入口已对齐新路线

---

## Stage 1：Linux + Git + Shell + 网络基础（工程地基）

| 字段 | 内容 |
|---|---|
| 启动条件 | Stage 0 退出后 |
| 所属 lane | `engineering` |
| 主要时长 | 2–3 个月（按真实节奏） |
| 现有 Round 映射 | **Round 00–02**（终端 + 文件系统 + Shell + Git）+ **Round 06**（Linux 进阶与自动化）+ **VPS 支线 stage_03_vps_remote_ops** |
| 与考试关系 | 软考"操作系统 / 网络"广度入门；不直接是考点 |

### 目标

- 保留原 Linux 主线
- 让 Linux 学习服务于"软考广度入门 + 工程实操 + 未来 AI 项目"
- 能完成本地与远程服务器的基础操作

### 产物

- Round 00 完成（已存在闭环）
- 至少 Round 01 / Round 02 / Round 06 展开为 `rounds/round_XX/` 实操目录（按需做完）
- VPS 支线至少完成 VPS-04（SSH 文档）+ VPS-05（首次只读检查）
- `plans/linux/` 下补充"软考视角下的操作系统基础对照笔记"

### 对应软考广度

- 操作系统基础（文件、进程、用户、I/O）
- 网络基础（IP/端口/HTTP）

### 对应 408 / 0854

- 软考层级；不达 408 深度。Stage 5 再深化。

### 简化版本（若时间不够）

- 只做 Round 00 + Round 02 + VPS-04，先把 Git 和 SSH 走通

### 退出标准

- [ ] Round 00 全部任务 done
- [ ] 能独立完成"本地仓库 → 推送 GitHub → 远程 VPS 拉取"循环
- [ ] 能列出 Linux 用户 / 权限 / 进程 / 文件系统四大模块的核心命令

---

## Stage 2：软考中级基础核心（默认软件设计师）

| 字段 | 内容 |
|---|---|
| 启动条件 | Stage 1 完成 Round 00、Round 02 或基本掌握命令行后即可启动 |
| 所属 lane | `soft_exam` |
| 主要时长 | 3–6 个月 |
| 现有 Round 映射 | Round 03（Python 基础）、Round 04（数据结构）、Round 05（算法）、Round 11（SQLite）、Round 14（HTTP）等可作为辅助素材；**不替代软考独立学习** |
| 与考试关系 | **本仓库当前阶段主推进方向** |

### 目标

- 以**软件设计师**为默认主线，建立软考知识体系
- 不只刷题，而是补计算机基础
- 高分 / 满分导向，不只追"过线"

### 模块清单（按主流大纲建议 + 待用户对照最新官方大纲确认）

1. 计算机组成基础
2. 操作系统
3. 数据结构
4. 数据库
5. 计算机网络
6. 软件工程
7. UML
8. 面向对象
9. 信息安全
10. 标准化与知识产权
11. 程序设计语言基础（C 为主）

### 产物

- `plans/soft_exam/README.md`：模块清单 + 章节进度表（在 Stage 0 已建空）
- `plans/soft_exam/<module>.md`：每个模块的章节笔记骨架（按需扩展）
- 每个模块至少 1 份"概念地图"笔记
- 错题本进入运转（详见 §Stage 3）

### 简化版本（若时间不够）

- 先做"数据结构 + 操作系统 + 数据库"三模块，跑通错题系统流程
- 其他模块在 Stage 3 真题阶段反推回来

### 退出标准

- [ ] 11 个模块每个都有"是否已建立概念地图"标记
- [ ] 至少做 50 道历年题（任意模块）
- [ ] 错题本运转起来（每周有新增 + 复习）

> **本仓库不缓存任何具体软考考题。** 真题练习以官方题库 / 你购买的教材为准。

---

## Stage 3：软考真题强化与错题系统

| 字段 | 内容 |
|---|---|
| 启动条件 | Stage 2 完成至少 5 个模块的概念地图 |
| 所属 lane | `soft_exam` |
| 主要时长 | 2–4 个月（含模考） |
| 现有 Round 映射 | 无（独立训练阶段） |
| 与考试关系 | **直接对应软考考前冲刺** |

### 目标

- 建立历年真题训练机制
- 建立错题分类
- 建立知识点回流机制
- **以高分 / 满分为目标，而不是只求及格**

### 要求（详见 `docs/ERROR_REVIEW_SYSTEM.md`）

- 每道错题必须归类到知识模块
- 每周生成一次错题复盘
- 高频错误必须回写到学习路线（即调整 Stage 2 的下一步）
- 模考至少 3 次，每次模考都建一份"分项得分表"

### 产物

- `records/error_notes/soft_exam/<module>/YYYY-MM-DD-shortid.md`：每道错题一份
- `records/weekly_reviews/YYYY-WW.md`：每周复盘
- `plans/soft_exam/mock_exams.md`：模考记录与回看

### 简化版本

- 不做模考，只做错题分类与回流

### 退出标准

- [ ] 错题分类清晰，每个模块都有错题
- [ ] 至少 3 次模考记录
- [ ] 模考稳定在自己设定的目标分数之上

---

## Stage 4：数学二长期基础（贯穿 Stage 2/3/5）

| 字段 | 内容 |
|---|---|
| 启动条件 | Stage 0 之后任何时候，建议**与 Stage 2 并行启动**（低强度） |
| 所属 lane | `math2` |
| 主要时长 | 12–24 个月（长期低强度） |
| 现有 Round 映射 | 无 |
| 与考试关系 | 直接对应数学二 |

### 目标

- 启动考研数学二长期计划
- 不追求短期冲刺，先建立稳定学习节奏
- **不被软考挤压到 0**：哪怕每周 1 小时也要保留

### 模块清单（按数学二大纲建议 + 待用户对照最新官方大纲确认）

- 高等数学
  - 函数、极限、连续
  - 一元函数微分
  - 一元函数积分
  - 多元函数微分（按当年大纲）
  - 微分方程
  - 重积分（按当年大纲）
  - 无穷级数（按当年大纲）
- 线性代数
  - 矩阵与行列式
  - 向量
  - 线性方程组
  - 特征值与特征向量
  - 二次型

### 产物

- `plans/math2/README.md`：模块清单 + 进度表
- `plans/math2/<module>.md`：每个模块的核心定义 + 易错点笔记（按需）
- 错题本进入 `records/error_notes/math2/`

### 简化版本

- 保底模式：每周 2 个例题 + 1 次错题复盘

### 退出标准

- [ ] 数学二知识图谱建立
- [ ] 高数与线代两大块每周都有题目积累
- [ ] 错题本至少有 50 道

---

## Stage 5：408 兼容基础（在软考基础上深化）

| 字段 | 内容 |
|---|---|
| 启动条件 | Stage 2 完成 + Stage 3 进入真题阶段（不要求软考已考完） |
| 所属 lane | `cs408` |
| 主要时长 | 4–8 个月 |
| 现有 Round 映射 | Round 04（数据结构）、Round 05（算法）、Round 14（HTTP）可作为入门，**但需要 408 教材深化** |
| 与考试关系 | 直接对应 408 + 0854 部分院校 |

### 目标

- 在软考基础上，进一步提升到考研 408 层级
- 区分清楚**软考广度** vs **408 深度**

### 模块清单

- 数据结构（强化：树 / 图 / 排序综合应用 / KMP / 平衡树 / B+ 树）
- 计算机组成原理（系统从 0 学一遍：数制 / 运算器 / CPU / 存储 / 总线 / I/O）
- 操作系统（强化：进程同步、调度算法计算、内存管理算法、文件分配方式）
- 计算机网络（强化：滑动窗口、拥塞控制、子网与路由计算、HTTP/TCP 细节）

### 产物

- `plans/408/README.md`：4 大模块进度表
- `plans/408/<module>.md`：每个模块的"软考 vs 408 对照"笔记
- 错题本进入 `records/error_notes/cs408/`

### 与软考的关键区别

| 项 | 软考 | 408 |
|---|---|---|
| 数据结构 | 偏概念与代码片段 | 大题（含手写完整算法 + 时间空间分析） |
| 计组 | 简单数制与寻址 | 完整 CPU 设计 + cache 替换计算题 |
| OS | 进程概念 + 简单同步 | 调度算法计算 + 内存管理推导 |
| 网络 | 协议功能 | 滑动窗口数值题 + 子网计算 |

### 退出标准

- [ ] 4 模块每个都有"软考 vs 408 对照"笔记
- [ ] 至少完成 2 套 408 综合题练习
- [ ] 错题本 408 部分超过 50 道

---

## Stage 6：0854 目标院校与方向筛选

| 字段 | 内容 |
|---|---|
| 启动条件 | Stage 5 启动后 |
| 所属 lane | `cs408`（与考研挂钩，但偏行政 / 信息收集） |
| 主要时长 | 持续滚动（每年 9–10 月更新一次最新招生目录） |

### 目标

- 建立目标院校筛选表
- 记录考试科目 / 是否考 408 / 是否考数学二 / 复试要求 / 学校知名度 / 难度

### 产物

- `docs/GRADUATE_SCHOOL_TRACKER.md`：模板已建（Stage 0 完成），后续填写

### 数据来源原则

- **必须以学校研究生院 / 学院官网当年招生目录为准**
- **不能用过期经验贴当最终依据**
- 联网时优先查官方；离线时只建模板与字段，**不编造**

### 退出标准

- [ ] GRADUATE_SCHOOL_TRACKER 中目标院校已经填到至少 5 所
- [ ] 每所院校的关键字段（专业代码 / 是否 408 / 是否数学二 / 复试要求 / 数据来源链接）都已填
- [ ] 每条数据都标注"按 YYYY-MM 官网信息"

---

## Stage 7：项目作品集与复试 / 求职联动

| 字段 | 内容 |
|---|---|
| 启动条件 | Stage 2 启动后**任何时候**，鼓励早动手 |
| 所属 lane | `engineering` + 跨 lane |
| 主要时长 | 长期（每个项目 1–3 个月） |
| 现有 Round 映射 | Round 07 / Round 09–17 / Round 19–21 都可以作为项目素材 |

### 目标

- 把学习内容转化为项目
- 为未来 AI / NLP / 数据质量 / 模型评测方向准备作品集

### 推荐项目方向（每个项目结构详见 `docs/PROJECT_PORTFOLIO_TRACK.md`）

- 标注质量分析系统
- 模型回答质量评测工具
- ASR 转写错误分析工具
- 日中双语文本对齐工具
- AI 小说生成项目的评测模块
- Linux 学习进度可视化页面（已部分存在：`progress.html`）
- 软考错题知识图谱

### 每个项目必须标注

- 对应知识点
- 对应软考模块
- 对应 408 模块
- 对应求职 / 复试价值
- 最小可运行版本
- 后续扩展方向

### 退出标准

- 至少 2 个项目有可运行的最小版本
- 至少 1 个项目能写成 1 页"项目介绍"用于复试

---

## 8. 阶段与 lane 对照表

| Stage | 主 lane | 辅 lane |
|---|---|---|
| 0 | 跨 | 跨 |
| 1 | engineering | — |
| 2 | soft_exam | engineering（共用素材） |
| 3 | soft_exam | — |
| 4 | math2 | — |
| 5 | cs408 | soft_exam（共用知识体系） |
| 6 | cs408 | — |
| 7 | engineering | soft_exam + cs408（项目复用考点） |

---

## 9. 阶段推进节奏建议

> 这是建议节奏，不是死板时间表。具体看 `docs/WEEKLY_EXECUTION_TEMPLATE.md` 的三种强度模板。

```
M1–M2     Stage 0（治理）
M2 起     Stage 1 + Stage 4（开始数学二低强度）
M3–M9     Stage 2 + Stage 4
M8–M12    Stage 3 + Stage 4
≥ M10     Stage 5 + Stage 4 + Stage 7
≥ M14     Stage 6（院校筛选滚动）
```

> M = month。M1 表示从 Stage 0 完成算起的第一个月。
> 软考通常每年 5 月 / 11 月各一次（以官方信息为准），可以提前 4–6 个月进入 Stage 3。

---

## 10. 与本仓库其他资产的连接

| 资产 | Stage 关系 |
|---|---|
| `rounds/round_00/` Round 00 终端入门 | Stage 1 |
| `round_01.md` ~ `round_08.md` 大纲 | Stage 1 + Stage 2（辅助素材） |
| `round_09.md` ~ `round_21.md` 大纲 | Stage 7 项目素材 + Stage 2 / Stage 5 部分章节辅助 |
| `rounds/stage_03_vps_remote_ops/` VPS 支线 | Stage 1（远程操作熟练度） |
| `plans/linux/` | Stage 1 |
| `plans/soft_exam/` | Stage 2 + Stage 3 |
| `plans/math2/` | Stage 4 |
| `plans/408/` | Stage 5 |
| `records/weekly_reviews/` | 全部 Stage |
| `records/error_notes/` | Stage 3 + Stage 4 + Stage 5 + Stage 6 |
| `docs/GRADUATE_SCHOOL_TRACKER.md` | Stage 6 |
| `docs/PROJECT_PORTFOLIO_TRACK.md` | Stage 7 |
| `progress.html` 四主线进度 | 全部 Stage（按 lane 展示） |

---

## 11. Stage 编号空间与 Round 编号空间的关系

- **Stage 编号**：用于"我现在处于学习计划的哪个阶段"。
- **Round 编号**：用于"我已经把哪些章节展开为可执行实操目录"。
- 两者**不冲突**：
  - Stage 1 包含 Round 00–06（已存在）+ Round 06、Round 14 部分 + 未来新增 VPS 支线
  - Stage 2 软考新增内容**不放进 `rounds/round_XX/`**，而是放进 `plans/soft_exam/`
  - Stage 4 数学二同理，放进 `plans/math2/`

> 决策原则：`rounds/round_XX/` 用于"可执行练习目录"；`plans/<scope>/` 用于"知识体系笔记 + 章节学习计划"；`records/<scope>/` 用于"真实发生过的学习记录"。

---

## 12. 风险与停止条件

- 若发现某个 Stage 的真实学习节奏远超预算（比如本来 3 个月却用了 9 个月），**优先停下重新评估总目标**，而不是硬推。
- 若软考改版 / 408 改版 / 数学二大纲变化，必须停下来对照 `docs/MASTER_STUDY_ROADMAP.md` 与本文件同步更新。
- 若进入 Stage 6 后发现目标院校全部不考 408 或不考数学二，Stage 5 / Stage 4 优先级应**重新评估**而不是死撑。

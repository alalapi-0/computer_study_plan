# plans/soft_exam/ · 软考中级线

> 所属 lane：`soft_exam`
> 关联 Stage：Stage 2（基础核心）+ Stage 3（真题强化）
> 默认目标：**软件设计师**，高分 / 满分导向

---

## 1. 重要声明

- 本目录**不缓存**任何具体软考考题、考纲条目或解题方法。
- 具体考试范围、题型、教材必须以**最新官方大纲**为准（中国计算机技术职业资格网 rkb.ruankao.org.cn）。
- 本目录承载的是"模块清单 + 章节笔记骨架 + 学习节奏 + 与 408 / 数学二的耦合关系标注"。

---

## 2. 模块清单（按主流大纲建议，最终以官方大纲为准）

| 模块代码 | 模块名 | 与 408 关系 | 推荐优先级 | 笔记骨架文件 | 当前状态 |
|---|---|---|---|---|---|
| `os` | 操作系统 | 软考广，408 计算题深 | P0 | [os.md](os.md) | 已有启动骨架 |
| `ds` | 数据结构 | 软考广，408 综合题深 | P0 | [ds.md](ds.md) | 已有启动骨架 |
| `db` | 数据库 | 仅软考考 | P0 | [db.md](db.md) | 已有启动骨架 |
| `composition` | 计算机组成基础 | 软考浅，408 深 | P0 | `composition.md` | 待建 |
| `network` | 计算机网络 | 软考广，408 计算题深 | P0 | `network.md` | 待建 |
| `se` | 软件工程 | 仅软考考 | P0 | `se.md` | 待建 |
| `uml` | UML / 设计模式 | 仅软考考 | P0 | `uml.md` | 待建 |
| `oo` | 面向对象 | 仅软考考 | P0 | `oo.md` | 待建 |
| `security` | 信息安全 | 仅软考考 | P0 | `security.md` | 待建 |
| `c_lang` | 程序设计语言（C） | 软考主语言 / 408 表达语言 | P0 | `c_lang.md` | 待建 |
| `standards` | 标准化与知识产权 | 仅软考考 | P1 | `standards.md` | 待建 |
| `english` | 英语阅读理解 | 仅软考考 | P1 | `english.md` | 待建 |

> 当前先维护 [os.md](os.md)、[ds.md](ds.md)、[db.md](db.md) 三个启动骨架。后续按真实学习节奏补 `composition.md`、`network.md`、`se.md` 等，不为了凑文件数提前写空壳。

---

## 3. 推进顺序建议

> 本顺序仅建议；可按 Stage 2 的实际节奏调整。

1. 先做 **数据结构 + 操作系统 + 数据库** 三个模块（与 408 / 工程实操共用率高）
2. 再做 **软件工程 + UML + 面向对象** 三个模块（软考独有，回报高）
3. 然后 **计算机网络 + 计算机组成**（与 408 共用）
4. 最后 **信息安全 + 标准化 + C 语言 + 英语**（补强）
5. 进入 Stage 3 真题阶段 + 错题驱动反推

---

## 4. 完成启动任务的最小产物

读完本总览后，不需要一次补完所有模块。完成当前 Web UI 任务前，只需留下三类可检查产物：

- 选定本周先推进的 1-2 个模块，并写进 Web UI 的本次记录。
- 打开对应模块骨架（优先 [os.md](os.md)、[ds.md](ds.md)、[db.md](db.md)），各写 1 条最容易混淆的概念边界。
- 写清下一步动作，例如“先补操作系统进程/内存概念地图”，不要只写“已阅读”。

---

## 5. 与其他 lane 的共享笔记

| 模块 | 软考侧位置 | 408 侧位置 | 共享原则 |
|---|---|---|---|
| 数据结构 | [plans/soft_exam/ds.md](ds.md) | `plans/408/ds.md` | 概念笔记可互相引用；错题分两份归档 |
| 操作系统 | [plans/soft_exam/os.md](os.md) | `plans/408/os.md` | 同上 |
| 计算机网络 | `plans/soft_exam/network.md` | `plans/408/network.md` | 同上 |
| 计算机组成 | `plans/soft_exam/composition.md` | `plans/408/composition.md` | 同上 |
| C 语言 | `plans/soft_exam/c_lang.md` | `plans/408/...`（按需） | 软考主笔记，408 引用 |

---

## 6. 笔记写作规则

- 每份模块笔记开头必须有"⚠ 注意：最新考试大纲见 [官方链接]" 提示
- 概念按"定义 + 关键性质 + 易混点 + 与 408 区别"四段组织
- **不复制教材整段**；引用必须注明来源
- 错题不写在本目录，归 `records/error_notes/soft_exam/<module>/`
- 章节"调整记录"段（错题驱动回炉）按 `docs/PROGRESS_RULES.md` §5 操作

---

## 6. 配套文件

| 用途 | 文件 |
|---|---|
| 模考记录入口 | `records/weekly_reviews/mock_exams/`（按需建） |
| 错题归档 | `records/error_notes/soft_exam/<module>/` |
| 资料索引 | 本目录 `resources.md`（按需建） |
| 每周复盘 | `records/weekly_reviews/YYYY-WW.md` |

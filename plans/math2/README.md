# plans/math2/ · 数学二线

> 所属 lane：`math2`
> 关联 Stage：Stage 4（长期低强度）

---

## 1. 重要声明

- 本目录**不缓存**任何具体考研数学考点、解题套路或题库内容。
- 数学二大纲、考试范围以**最新考研数学大纲**为准。
- 本目录承载的是"模块清单 + 章节笔记骨架 + 长期节奏"。

---

## 2. 模块清单（按主流大纲建议）

### 高等数学

| 模块代码 | 模块名 | 笔记骨架文件（按需建） |
|---|---|---|
| `limits` | 函数 / 极限 / 连续 | [limits.md](limits.md) |
| `derivatives` | 一元函数微分 | `derivatives.md` |
| `integrals` | 一元函数积分 | `integrals.md` |
| `multi_var` | 多元函数微分（按当年大纲） | `multi_var.md` |
| `double_integrals` | 二重积分（按当年大纲） | `double_integrals.md` |
| `ode` | 微分方程 | `ode.md` |
| `series` | 无穷级数（按当年大纲） | `series.md` |

### 线性代数

| 模块代码 | 模块名 | 笔记骨架文件（按需建） |
|---|---|---|
| `la_matrix` | 矩阵与行列式 | [la_matrix.md](la_matrix.md) |
| `la_vector` | 向量 | `la_vector.md` |
| `la_linear_systems` | 线性方程组 | `la_linear_systems.md` |
| `la_eigen` | 特征值与特征向量 | `la_eigen.md` |
| `la_quadratic_forms` | 二次型 | `la_quadratic_forms.md` |

> 当前已维护 [limits.md](limits.md) 与 [la_matrix.md](la_matrix.md) 两个启动骨架；其他笔记文件按真实学习节奏需要时再建。

---

## 3. 推进原则

- **长期低强度**：哪怕每周 1 道题，也要持续
- **不让软考挤掉数学二**：保底模式下数学二保留每周 1 道题
- **错题积累优先于看视频**

---

## 4. 推进顺序建议

```
M1     启动：极限 + 矩阵入门
M2     一元微分
M3     一元积分
M4     极限/微分/积分 综合滚动
M5     线性代数：向量 + 线性方程组
M6     微分方程
M7     多元微分 / 二重积分（按大纲）
M8     特征值 + 二次型
M9+    真题阶段
```

> M = month。**这是粗略节奏**，实际进度取决于你的精力分配。

---

## 5. 完成启动任务的最小产物

读完本总览后，不需要马上铺开所有数学模块。完成当前 Web UI 任务前，只需留下三类可检查产物：

- 选定本周数学二保底动作，例如“极限 1 道例题 + 矩阵 1 个定义”。
- 打开 [limits.md](limits.md) 或 [la_matrix.md](la_matrix.md)，写下 1 个最容易卡住的概念。
- 在 Web UI 记录中写清下次先算哪一道 / 先补哪个定义，不要只写“已阅读”。

---

## 6. 笔记写作规则

- 每份模块笔记开头必须有"⚠ 注意：最新考试大纲见 [官方链接]" 提示
- 按"定义 → 关键定理 → 易错点 → 例题骨架"四段组织
- **不允许大段抄教材**；保留教材引用 + 个人理解
- 错题归 `records/error_notes/math2/<module>/`

---

## 7. 与其他 lane 的关系

- 数学二**几乎不与软考 / 408 重叠**（408 数据结构 / 计组涉及少量数学但不深）
- 数学二是**独立长期项目**

---

## 8. 配套文件

| 用途 | 文件 |
|---|---|
| 错题归档 | `records/error_notes/math2/<module>/` |
| 真题记录 | `records/weekly_reviews/mock_exams/`（按需建） |
| 资料索引 | 本目录 `resources.md`（按需建） |
| 每周复盘 | `records/weekly_reviews/YYYY-WW.md` |

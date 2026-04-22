# Round 18 · 数值计算与数据分析前置

> **定位**（路线 C 第 1 步）：把后面做机器学习时一定会反复用到的"数据感觉"先打牢。核心工具：NumPy + pandas。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | NumPy ndarray + pandas DataFrame + 基础数据分析 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 17 或 Round 13 |
| **下一轮** | Round 19 · 机器学习最小闭环 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 用 NumPy 处理一维、二维数组，理解 shape、dtype、axis、切片、广播
- [ ] 知道为什么 NumPy 操作比 Python for 循环更适合数值计算
- [ ] 用 pandas 读取 CSV，选列、筛行、做基础统计、`groupby`
- [ ] 建立一个关键项目直觉：模型前的数据准备大多是"读表、筛数据、看分布、查缺失"

---

## 本轮不学什么

> 先不碰：神经网络、PyTorch、Hugging Face、特征工程深水区、复杂可视化、大规模数据管线

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html) | ndarray、形状、轴、常见操作 |
| 📄 文档 2 | [NumPy Absolute Basics](https://numpy.org/doc/stable/user/absolute_beginners.html) | 更适合入门者 |
| 📄 文档 3 | [pandas – Getting started tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html) | 读数据、选子集、统计、groupby |
| 📄 文档 4 | [pandas – User Guide](https://pandas.pydata.org/docs/user_guide/index.html) | 参考用，不用整本读 |

---

## 3 周学习安排

### 第 1 周：NumPy 基础数组操作

**目标**：建立"n 维数组 + 向量化"的直觉。

**关键概念**：
- `ndarray`：同类型元素的多维数组
- `shape`：数组的维度形状，如 `(3, 4)` 表示 3 行 4 列
- `dtype`：数组元素的类型，如 `float64`、`int32`
- `axis`：操作的方向，`axis=0` 沿行方向，`axis=1` 沿列方向
- **广播（broadcasting）**：小数组自动扩展到大数组的形状做运算
- **向量化**：循环发生在 C 层而不是 Python 层，比 for 快很多

---

### 第 2 周：pandas DataFrame 基础

**目标**：把"读表、看数据、筛行选列、做统计"练顺。

**关键操作**：
- `pd.read_csv()` / `df.to_csv()`
- `df.head()` / `df.info()` / `df.describe()`
- `df["列名"]` / `df[["列1", "列2"]]`
- `df[df["列"] > 值]` 筛行
- `df.groupby("列").agg(...)` 分组统计
- `df.isna().sum()` 查缺失值

---

### 第 3 周：综合数据分析

**目标**：用 NumPy + pandas 做一次完整的小数据分析。

---

## 本轮练习清单

### 准备工作

```bash
pip install numpy pandas
mkdir -p ~/cli-lab/round18
cd ~/cli-lab/round18
```

---

### 第 1 周练习

**练习 1**：NumPy 数组基础
```python
# numpy_basics.py
import numpy as np

# 创建数组
a = np.array([1, 2, 3, 4, 5])
b = np.array([[1, 2, 3], [4, 5, 6]])

print(f"a.shape: {a.shape}")    # (5,)
print(f"b.shape: {b.shape}")    # (2, 3)
print(f"b.dtype: {b.dtype}")    # int64
print(f"b.ndim: {b.ndim}")      # 2

# 常用创建方式
zeros = np.zeros((3, 4))
ones = np.ones((2, 3))
range_arr = np.arange(0, 10, 2)
linspace_arr = np.linspace(0, 1, 5)

print(zeros)
print(range_arr)
```

**练习 2**：向量化操作 vs for 循环
```python
# vectorize_demo.py
import numpy as np
import time

data = np.random.randn(1_000_000)

# 方式 1：Python for 循环
start = time.time()
result_loop = []
for x in data:
    result_loop.append(x ** 2)
t_loop = time.time() - start

# 方式 2：NumPy 向量化
start = time.time()
result_np = data ** 2
t_np = time.time() - start

print(f"Loop: {t_loop:.3f}s")
print(f"NumPy: {t_np:.4f}s")
print(f"Speedup: {t_loop / t_np:.0f}x")
```

**练习 3**：切片和广播
```python
# slice_broadcast.py
import numpy as np

m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 切片
print("First row:", m[0])
print("Last column:", m[:, -1])
print("Submatrix:", m[0:2, 1:3])

# 广播示例
row = np.array([1, 2, 3])
print("Original:\n", m)
print("After adding row:\n", m + row)  # row 广播到每一行

# axis 参数
print("Sum all:", m.sum())
print("Sum by column (axis=0):", m.sum(axis=0))  # 每列求和
print("Sum by row (axis=1):", m.sum(axis=1))     # 每行求和
```

---

### 第 2 周练习

**准备测试数据**：
```python
# create_test_data.py
import pandas as pd
import numpy as np

np.random.seed(42)
n = 200

df = pd.DataFrame({
    "id": range(1, n + 1),
    "label": np.random.choice(["ok", "blur", "bad", "good"], n),
    "score": np.random.uniform(0, 1, n).round(3),
    "length": np.random.randint(5, 500, n),
    "source": np.random.choice(["web", "mobile", "api"], n),
})
df.to_csv("sample_data.csv", index=False)
print("Created sample_data.csv")
```

**练习 4**：pandas 基础读取和查看
```python
# pandas_basics.py
import pandas as pd

df = pd.read_csv("sample_data.csv")

# 基本信息
print(df.shape)        # (200, 5)
print(df.head())       # 前 5 行
print(df.dtypes)       # 各列类型
print(df.describe())   # 数值列统计摘要
print(df.info())       # 列信息 + 非空计数
```

**练习 5**：选列和筛行
```python
# select_filter.py
import pandas as pd

df = pd.read_csv("sample_data.csv")

# 选列
scores = df["score"]
subset = df[["label", "score"]]

# 筛行
high_score = df[df["score"] > 0.8]
ok_or_good = df[df["label"].isin(["ok", "good"])]
web_high = df[(df["source"] == "web") & (df["score"] > 0.7)]

print(f"High score rows: {len(high_score)}")
print(f"ok/good rows: {len(ok_or_good)}")
print(f"Web high score: {len(web_high)}")
```

**练习 6**：统计和 groupby
```python
# stats_groupby.py
import pandas as pd

df = pd.read_csv("sample_data.csv")

# 基础统计
print("Score stats:")
print(df["score"].describe())

# groupby
label_stats = df.groupby("label").agg(
    count=("id", "count"),
    avg_score=("score", "mean"),
    avg_length=("length", "mean")
).round(3)
print("\nLabel stats:")
print(label_stats)

# 查缺失值
print("\nMissing values:")
print(df.isna().sum())
```

---

### 第 3 周练习

**综合数据分析脚本**：
```python
# data_analysis.py
"""
用 NumPy + pandas 做一次完整的小数据分析：
1. 读取数据
2. 基本探索
3. 数据清洗
4. 统计分析
5. 导出报告
"""
import pandas as pd
import numpy as np

def load_and_explore(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"=== Data Overview ===")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Missing values:\n{df.isna().sum()}")
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # 删除缺失值行
    df = df.dropna()
    # 过滤异常 score（应在 0-1 之间）
    df = df[(df["score"] >= 0) & (df["score"] <= 1)]
    print(f"\nAfter cleaning: {len(df)} rows")
    return df

def analyze(df: pd.DataFrame) -> dict:
    label_dist = df["label"].value_counts().to_dict()
    score_by_label = df.groupby("label")["score"].mean().round(3).to_dict()
    
    # NumPy 计算
    scores = df["score"].values
    percentiles = np.percentile(scores, [25, 50, 75])
    
    return {
        "total_records": len(df),
        "label_distribution": label_dist,
        "avg_score_by_label": score_by_label,
        "score_percentiles": {
            "p25": round(percentiles[0], 3),
            "p50": round(percentiles[1], 3),
            "p75": round(percentiles[2], 3),
        }
    }

def main():
    df = load_and_explore("sample_data.csv")
    df = clean_data(df)
    report = analyze(df)
    
    print("\n=== Analysis Report ===")
    for key, value in report.items():
        print(f"{key}: {value}")
    
    # 导出干净数据
    df.to_csv("output/clean_data.csv", index=False)
    print("\nCleaned data exported to output/clean_data.csv")

if __name__ == "__main__":
    main()
```

---

## NumPy / pandas 速查

| 操作 | NumPy | pandas |
|------|-------|--------|
| 创建 | `np.array([1,2,3])` | `pd.DataFrame(data)` |
| 形状 | `a.shape` | `df.shape` |
| 切片 | `a[1:3, :]` | `df.iloc[1:3, :]` |
| 条件筛选 | `a[a > 0]` | `df[df["col"] > 0]` |
| 统计 | `a.mean()`, `a.sum()` | `df["col"].describe()` |
| 分组 | - | `df.groupby("col").agg(...)` |
| 缺失值 | `np.isnan(a)` | `df.isna().sum()` |

---

## 验收标准

- [ ] 能用 NumPy 创建、切片、做向量化运算
- [ ] 能解释广播和 `axis` 参数
- [ ] 能用 pandas 读取 CSV，选列、筛行、做统计
- [ ] 完成了综合数据分析脚本，有"读、探、洗、分析、导出"完整流程

---

## ⚠️ 最容易踩的坑

1. **混淆 `axis=0` 和 `axis=1`** — `axis=0` 沿行方向（跨行），`axis=1` 沿列方向（跨列）
2. **pandas 筛行用 `&` 不用 `and`** — `df[(cond1) & (cond2)]`，不能用 Python 的 `and`
3. **修改 DataFrame 的 SettingWithCopyWarning** — 筛选后的 DataFrame 修改要用 `.copy()`

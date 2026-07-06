# Round 18 · Week 2：pandas CSV、选列、筛行与 groupby

## 本周目标

本周把“表格数据”的最小工作流练顺：读 CSV，看列名和类型，选列，按条件筛行，做分组统计，查缺失值。机器学习前的数据准备，大量工作就是这些动作的组合。

## 页面内学习步骤

1. 在 Web UI 打开本文件，先读“CSV 到 DataFrame”的主链。
2. 点击“练习：生成 CSV 读取、筛选与 groupby 示例”。
3. 在运行结果中确认生成 `sample_data.csv`、`pandas_basics.py`、`select_filter.py`、`stats_groupby.py` 和 `static_check_report.json`。
4. 用任务行的“终端练习”完成自测。
5. 在“记录并完成”弹窗里写下你最容易混淆的筛选语法。

## 主链

| 步骤 | pandas 代码形状 | 作用 |
|---|---|---|
| 读表 | `pd.read_csv("sample_data.csv")` | 从 CSV 变成 DataFrame |
| 看结构 | `df.shape` / `df.head()` / `df.dtypes` | 先知道数据长什么样 |
| 选列 | `df["score"]` / `df[["label", "score"]]` | 只拿关心的列 |
| 筛行 | `df[df["score"] > 0.8]` | 只保留符合条件的行 |
| 多条件 | `df[(cond1) & (cond2)]` | pandas 里用 `&`，不用 Python `and` |
| 分组 | `df.groupby("label").agg(...)` | 按类别做统计 |
| 缺失 | `df.isna().sum()` | 看每列缺了多少 |

## 浏览器终端自测

```bash
pwd
printf 'label,score\nok,0.9\nbad,0.2\nok,0.7\ngood,0.8\n' > tiny_scores.csv
printf 'import csv\nrows = list(csv.DictReader(open("tiny_scores.csv")))\nprint(len(rows))\nprint(sum(1 for row in rows if row["label"] == "ok"))\n' > count_labels.py
python3 count_labels.py
```

期望输出：

- 总行数是 `4`。
- `ok` 标签数量是 `2`。

## 外部资料

- [pandas Getting started tutorials](https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html)
- [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)

## 完成标准

- 自动练习任务已运行成功。
- 你能解释 `read_csv`、选列、筛行、`groupby`、`isna().sum()` 分别解决什么问题。
- 自测命令在 Web UI 终端里跑过，并把 `~/cli-lab/round18` 或具体文件路径写入记录。

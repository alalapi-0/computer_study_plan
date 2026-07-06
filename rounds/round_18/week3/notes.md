# Round 18 · Week 3：小数据分析主链

## 本周目标

本周把 NumPy/pandas 的碎片操作收拢成一个完整流程：读取数据、观察结构、清洗异常、做统计、导出报告。这就是后续机器学习之前最常见的数据准备主链。

## 页面内学习步骤

1. 在 Web UI 打开本文件，先读完整分析流程。
2. 点击“练习：生成读、清洗、统计、导出分析流程”。
3. 在运行结果中确认生成 `messy_sample_data.csv`、`data_analysis.py`、`analysis_contract.json` 和 `static_check_report.json`。
4. 用终端完成自测：手写一个不依赖 pandas 的最小清洗统计脚本。
5. 在“记录并完成”弹窗里写下你的分析流程五步：load、explore、clean、analyze、export。

## 分析流程

| 步骤 | 问题 | 代码形状 |
|---|---|---|
| load | 数据从哪里来？ | `pd.read_csv(path)` |
| explore | 数据长什么样？ | `df.shape` / `df.columns` / `df.isna().sum()` |
| clean | 哪些行不能用？ | `df.dropna()` / 条件过滤 |
| analyze | 结果怎么算？ | `value_counts()` / `groupby()` / `np.percentile()` |
| export | 产物留在哪里？ | `to_csv()` / 写 JSON 报告 |

## 浏览器终端自测

```bash
pwd
printf 'label,score\nok,0.9\nbad,-0.1\ngood,0.8\nblur,\nok,1.2\n' > messy.csv
printf 'import csv\nrows = list(csv.DictReader(open("messy.csv")))\nclean = []\nfor row in rows:\n    if row["score"]:\n        score = float(row["score"])\n        if score >= 0 and not score > 1:\n            clean.append(row)\nprint(len(clean))\nprint(sorted(row["label"] for row in clean))\n' > clean_demo.py
python3 clean_demo.py
```

期望输出：

- 干净行数是 `2`。
- 标签是 `good` 和 `ok`。

## 完成标准

- 自动练习任务已运行成功。
- 你能画出或说出数据分析五步。
- 你知道缺失值、异常分数和导出结果分别在哪一步处理。
- 自测命令跑过，并在记录中写下证据路径。

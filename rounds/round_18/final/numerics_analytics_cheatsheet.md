# Round 18 · 数值计算与数据分析小抄

## Web UI 完成顺序

1. Week 1：阅读数组基础，运行 NumPy 形状、axis、广播示例。
2. Week 2：阅读 DataFrame 基础，运行 CSV、筛选、groupby 示例。
3. Week 3：阅读分析主链，运行读、清洗、统计、导出示例。
4. Final：运行综合项目包，打开本文件补充你的理解。
5. 在最终验收任务里记录：你如何从 raw CSV 走到 analysis report。

## 最小口诀

| 主题 | 口诀 |
|---|---|
| NumPy | 先看 `shape`，再想 `axis`，重复计算用向量化 |
| broadcasting | 小数组能不能贴到大数组上，先看维度是否兼容 |
| pandas | 先 `read_csv`，再 `head/shape/dtypes`，不要一上来就分析 |
| 筛行 | pandas 多条件用 `&` 和括号 |
| groupby | “按什么分组”和“算什么指标”分开想 |
| 缺失值 | 先 `isna().sum()` 看问题，再决定 drop 还是填补 |

## 数据分析主链

```text
raw csv
  -> load
  -> explore
  -> clean
  -> analyze
  -> export clean_data + report
```

## 最终验收自问

- 我能解释 `axis=0` 和 `axis=1` 的区别吗？
- 我能解释为什么向量化比 Python for 循环更适合数值计算吗？
- 我能用 pandas 写出选列、筛行、groupby 的代码形状吗？
- 我能说清一个数据分析脚本为什么要分成 load / clean / analyze / export 吗？
- 我知道 Web UI 自动练习为什么不直接安装 NumPy/pandas 吗？

## 通过标准

- `r18-w1-ex1`、`r18-w2-ex2`、`r18-w3-ex3`、`r18-fin-comp` 均运行成功。
- 终端自测至少完成一条，并把证据路径写入记录。
- 最终验收能解释数据从 CSV 到报告的完整链路。

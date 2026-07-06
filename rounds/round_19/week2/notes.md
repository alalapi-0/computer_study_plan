# Round 19 · Week 2 笔记（指标与过拟合直觉）

## 本周目标

本周不追复杂模型，只解决两个问题：

1. 不只盯 accuracy，还能解释 precision、recall、F1。
2. 能用训练分数和测试分数的差距识别过拟合。

## Web UI 学习路径

1. 在 Round 19 面板打开本阅读任务。
2. 点击“练习：生成分类指标与过拟合观察示例”。
3. 查看运行结果中的 `metrics_demo.py`、`overfitting_demo.py`、`stdlib_metrics_demo.py` 和 `static_check_report.json`。
4. 点击“自测：自己写 metrics_from_counts.py”的“终端练习”，完成手写指标计算。
5. 自测通过后点击“记录并完成”保存自测记录。

## 指标速记

| 指标 | 什么时候有用 |
|---|---|
| accuracy | 类别比较均衡时，快速看整体正确率 |
| precision | 预测为正的样本里，有多少真的为正 |
| recall | 真实为正的样本里，有多少被找出来 |
| F1 | precision 和 recall 都重要时，用一个数做折中 |

过拟合的第一眼信号：

- 训练分数很高，测试分数明显低：模型把训练集记住了。
- 训练分数和测试分数都低：模型能力不足或特征不够。
- 测试集被反复拿来调参：测试集会变成“间接训练集”。

## 参考链接

- [scikit-learn Metrics and scoring](https://scikit-learn.org/stable/modules/model_evaluation.html)
- [scikit-learn Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html)

## 浏览器终端自测

在终端任务中输入：

```bash
cat > metrics_from_counts.py
```

输入下面内容，按回车后用 `Ctrl+D` 结束：

```python
tp = 18
fp = 4
fn = 6
tn = 72
accuracy = (tp + tn) * (tp + fp + fn + tn) ** -1
precision = tp * (tp + fp) ** -1
recall = tp * (tp + fn) ** -1
f1 = 2 * precision * recall * (precision + recall) ** -1
print("accuracy:", round(accuracy, 3))
print("precision:", round(precision, 3))
print("recall:", round(recall, 3))
print("f1:", round(f1, 3))
```

运行：

```bash
python3 metrics_from_counts.py
```

如果你能解释为什么 F1 同时受 precision 和 recall 影响，本周自测就过关。

## 完成标准

- 能根据 `tp/fp/fn/tn` 算出四个指标。
- 能解释不平衡数据下 accuracy 为什么可能骗人。
- 能用 train/test 分数差距描述过拟合。

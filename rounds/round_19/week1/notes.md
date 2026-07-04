# Round 19 · Week 1 笔记（X/y、切分、fit/predict/score）

## 本周目标

把最小分类闭环跑通：

1. 准备特征矩阵 `X` 和标签 `y`。
2. 用 `train_test_split` 切出训练集和测试集。
3. 训练一个简单分类器。
4. 对测试集预测。
5. 用 accuracy 记录第一份结果。

## Web UI 学习路径

1. 在 Round 19 面板打开本阅读任务。
2. 点击“练习：生成 X/y 切分与最小分类闭环”，生成 `~/cli-lab/round19/week1_auto/train_test_split`。
3. 打开运行结果，确认看到 `minimal_classifier.py`、`holdout_split_demo.py` 和 `static_check_report.json`。
4. 点击“自测：自己写 train_test_split_demo.py”的“终端”，完成下面的手写自测。
5. 自测通过后手动记录自测任务。

## 概念速记

| 概念 | 解释 |
|---|---|
| `X` | 特征矩阵，每一行是一个样本，每一列是一个特征 |
| `y` | 标签向量，每个样本对应一个目标类别 |
| train set | 用来让模型学习 |
| test set | 用来模拟新数据，评估泛化能力 |
| `random_state` | 固定随机切分，让结果可复现 |
| `fit` | 在训练数据上学习 |
| `predict` | 对新样本预测标签 |
| `score` | 用统一方式返回模型分数 |

## 参考链接

- [scikit-learn Getting Started](https://scikit-learn.org/stable/getting_started.html)
- [train_test_split 官方文档](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html)

## 浏览器终端自测

在终端任务中输入：

```bash
cat > train_test_split_demo.py
```

输入下面内容，按回车后用 `Ctrl+D` 结束：

```python
rows = [
    {"x1": 1.0, "x2": 0.1, "label": "low"},
    {"x1": 1.2, "x2": 0.2, "label": "low"},
    {"x1": 2.0, "x2": 0.8, "label": "mid"},
    {"x1": 2.2, "x2": 0.7, "label": "mid"},
    {"x1": 3.0, "x2": 1.5, "label": "high"},
    {"x1": 3.2, "x2": 1.4, "label": "high"},
]
split_at = 4
train = rows[:split_at]
test = rows[split_at:]
majority = max({row["label"] for row in train}, key=[row["label"] for row in train].count)
print("train:", len(train))
print("test:", len(test))
print("baseline_label:", majority)
```

运行：

```bash
python3 train_test_split_demo.py
```

你应该能看到训练集 4 行、测试集 2 行，并能说出“这个 majority baseline 为什么不是真正聪明的模型”。

## 完成标准

- 能说出 `X` 和 `y` 的区别。
- 能解释为什么不能把全部数据都拿去训练。
- 能复述 `fit -> predict -> evaluate` 的顺序。

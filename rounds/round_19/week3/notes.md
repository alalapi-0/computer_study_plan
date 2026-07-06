# Round 19 · Week 3 笔记（预处理、Pipeline 与数据泄漏）

## 本周目标

建立一个重要规则：

> 任何会“学习数据分布”的预处理步骤，都只能在训练集上 `fit`；测试集只能 `transform`。

这条规则比会背模型名字更重要。因为数据泄漏会让评估分数变漂亮，却不能代表真实泛化能力。

## Web UI 学习路径

1. 在 Round 19 面板打开本阅读任务。
2. 点击“练习：生成预处理、Pipeline 与泄漏检查示例”。
3. 查看运行结果中的 `preprocessing_correct.py`、`pipeline_demo.py`、`leakage_notes.py` 和 `static_check_report.json`。
4. 点击“自测：自己写 scaler_rule_demo.py”的“终端练习”，完成手写预处理规则演示。
5. 自测通过后点击“记录并完成”保存自测记录。

## 关键规则

| 写法 | 结果 |
|---|---|
| `scaler.fit(X_train)` | 正确，只看训练集 |
| `scaler.transform(X_train)` | 正确，转换训练集 |
| `scaler.transform(X_test)` | 正确，测试集只使用训练集学到的参数 |
| `scaler.fit(X)` 后再切分 | 错误，测试集信息已经泄漏 |
| `Pipeline([scaler, model])` | 推荐，把预处理和模型放进同一条训练链 |

## 参考链接

- [scikit-learn Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html)
- [scikit-learn Preprocessing data](https://scikit-learn.org/stable/modules/preprocessing.html)
- [scikit-learn Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline)

## 浏览器终端自测

在终端任务中输入：

```bash
cat > scaler_rule_demo.py
```

输入下面内容，按回车后用 `Ctrl+D` 结束：

```python
train = [10, 12, 14, 16]
test = [30, 32]
mean = sum(train) * len(train) ** -1
variance = sum((value - mean) ** 2 for value in train) * len(train) ** -1
scale = variance ** 0.5
train_scaled = [(value - mean) * scale ** -1 for value in train]
test_scaled = [(value - mean) * scale ** -1 for value in test]
print("train_mean:", round(mean, 2))
print("train_scaled_first:", round(train_scaled[0], 3))
print("test_scaled_first:", round(test_scaled[0], 3))
print("rule:", "fit on train, transform train and test")
```

运行：

```bash
python3 scaler_rule_demo.py
```

## 完成标准

- 能解释为什么测试集不能参与 `fit`。
- 能说出 Pipeline 帮你减少哪类错误。
- 能区分“训练阶段”和“评估阶段”。

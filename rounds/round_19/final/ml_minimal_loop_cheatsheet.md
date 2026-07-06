# Round 19 · 机器学习最小闭环速查

## Web UI 完成顺序

1. Week 1：阅读 X/y、train/test split、fit/predict/score；运行最小分类闭环练习。
2. Week 2：阅读 accuracy / precision / recall / F1；运行指标和过拟合观察练习。
3. Week 3：阅读预处理和 Pipeline；运行泄漏检查练习。
4. Final：运行完整 ML 最小闭环项目包。
5. 点击“记录并完成”保存本小抄和最终验收。

## 最小机器学习链路

```text
raw data
  -> X 特征矩阵 + y 标签
  -> train_test_split
  -> fit on training data
  -> predict on test data
  -> evaluate with metrics
  -> record result and next question
```

## 三条口诀

- **先切分，再训练**：测试集只用来评估。
- **先看 baseline，再看复杂模型**：没有基线，就不知道模型是否真的有用。
- **预处理只在训练集 fit**：测试集不能提前泄漏给训练流程。

## 指标小抄

| 指标 | 一句话 |
|---|---|
| accuracy | 总体答对比例 |
| precision | 预测为正时，有多少是真的正 |
| recall | 真实为正时，有多少被找出来 |
| F1 | precision 和 recall 的折中 |

## 过拟合判断

| 现象 | 解释 |
|---|---|
| train 高、test 低 | 过拟合，模型记住了训练集 |
| train 低、test 低 | 欠拟合，模型或特征不够 |
| test 被反复调参使用 | 测试集不再干净，评估会虚高 |

## 最终验收自问

- 我能说清楚 `X` 和 `y` 分别是什么吗？
- 我能解释 `fit`、`predict`、`score` 的顺序吗？
- 我能用一组 `tp/fp/fn/tn` 算出 precision、recall、F1 吗？
- 我能解释为什么 `scaler.fit(X)` 后再切分是错误的吗？
- 我能说明 Pipeline 如何帮助减少数据泄漏吗？

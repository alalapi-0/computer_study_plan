# Round 19 · 机器学习最小闭环

> **定位**（路线 C 第 2 步）：把一条最小机器学习工作流真正跑通：准备特征 X 和标签 y → 切分数据 → 训练分类器 → 评估 → 理解过拟合。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | scikit-learn 基础 + train/test split + 分类指标 + 过拟合直觉 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 18 |
| **下一轮** | Round 20 · PyTorch 入门 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能用自己的话解释"特征"和"标签"
- [ ] 能用 `train_test_split` 切分数据，知道 `random_state` 的作用
- [ ] 能训练最简单的分类模型并在测试集上评估
- [ ] 知道 accuracy、precision、F1 各适合表达什么
- [ ] 理解"测试集不能拿来反复调参"和"预处理不能先在全数据上 fit"

---

## 本轮不学什么

> 先不碰：神经网络、PyTorch、Transformer、复杂特征工程、超参数搜索深水区、多模型系统比较

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [scikit-learn – Getting Started](https://scikit-learn.org/stable/getting_started.html) | estimator 的 fit/predict/score |
| 📄 文档 2 | [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) | 数据切分 |
| 📄 文档 3 | [Cross-validation](https://scikit-learn.org/stable/modules/cross_validation.html) | 为什么测试集不能反复偷看 |
| 📄 文档 4 | [Metrics and scoring](https://scikit-learn.org/stable/modules/model_evaluation.html) | 选对指标 |
| 📄 文档 5 | [Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) | 数据泄漏和不一致预处理 |
| 📄 文档 6 | [Preprocessing data](https://scikit-learn.org/stable/modules/preprocessing.html) | fit 在训练集上，transform 用到测试集 |

---

## 关键概念速查

| 概念 | 说明 |
|------|------|
| X | 样本的特征矩阵，形状 `(n_samples, n_features)` |
| y | 每个样本对应的目标/标签，形状 `(n_samples,)` |
| fit() | 让模型在训练数据上"学习" |
| predict() | 对新数据做预测 |
| score() | 评估模型在测试集上的表现 |
| train/test split | 把数据分成训练集（学习用）和测试集（评估用） |
| 数据泄漏 | 测试集信息在训练阶段被"偷看"，导致评估结果虚高 |

---

## 3 周学习安排

### 第 1 周：把最小分类闭环跑通

**目标**：准备 X/y → 切分 → 训练 → 在测试集上拿分数。

**最小流程**：
```python
1. 准备 X 和 y
2. train_test_split(X, y, test_size=0.2, random_state=42)
3. 训练一个最简单分类器
4. 在测试集上预测
5. 用 score() 或 accuracy_score() 看结果
```

---

### 第 2 周：评估指标和"泛化"直觉

**目标**：不要只看一个分数，要理解分数代表什么。

**三个指标的区别**：
- `accuracy_score`：总体正确率，最直接
- `precision_score`：预测为正的样本里，有多少真的是正（`tp / (tp + fp)`）
- `f1_score`：precision 和 recall 的调和平均，不平衡数据集常用

**过拟合直觉**：
- 训练集分数高但测试集分数低 → 过拟合
- 两个分数都低 → 欠拟合

---

### 第 3 周：预处理规范 + 最小 Pipeline

**目标**：建立"fit 在训练集上，transform 用到测试集上"的最小规范。

---

## 本轮练习清单

### 准备工作

```bash
pip install scikit-learn numpy pandas
mkdir -p ~/cli-lab/round19
cd ~/cli-lab/round19
```

---

### 第 1 周练习

**练习 1**：用 Iris 数据集跑最小闭环
```python
# iris_demo.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# 1. 加载数据
iris = load_iris()
X = iris.data      # (150, 4) - 4 个特征
y = iris.target    # (150,) - 3 个类别

print(f"X shape: {X.shape}")
print(f"y shape: {y.shape}")
print(f"Classes: {iris.target_names}")

# 2. 切分数据
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"Train: {len(X_train)}, Test: {len(X_test)}")

# 3. 训练
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# 4. 预测
y_pred = clf.predict(X_test)

# 5. 评估
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.3f}")
```

**练习 2**：尝试不同的简单分类器
```python
# compare_classifiers.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

classifiers = {
    "DecisionTree": DecisionTreeClassifier(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=3),
    "LogisticRegression": LogisticRegression(max_iter=200, random_state=42),
}

for name, clf in classifiers.items():
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"{name}: {acc:.3f}")
```

---

### 第 2 周练习

**练习 3**：三种评估指标
```python
# metrics_demo.py
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report
)

# 创建一个不平衡数据集（90% 负样本，10% 正样本）
X, y = make_classification(
    n_samples=1000, n_features=10,
    weights=[0.9, 0.1],  # 不平衡
    random_state=42
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print(f"Accuracy:  {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall:    {recall_score(y_test, y_pred):.3f}")
print(f"F1:        {f1_score(y_test, y_pred):.3f}")

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))
```

**练习 4**：观察过拟合
```python
# overfitting_demo.py
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("=== Effect of max_depth on overfitting ===")
for depth in [1, 2, 3, 5, 10, None]:
    clf = DecisionTreeClassifier(max_depth=depth, random_state=42)
    clf.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, clf.predict(X_train))
    test_acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"max_depth={str(depth):5s}: train={train_acc:.3f}, test={test_acc:.3f}")
```

---

### 第 3 周练习

**练习 5**：正确的预处理方式（防数据泄漏）
```python
# preprocessing_correct.py
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ 正确：只在训练集上 fit，然后 transform 两个集合
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled = scaler.transform(X_test)          # 只 transform，不 fit！

clf = LogisticRegression(random_state=42)
clf.fit(X_train_scaled, y_train)
acc = accuracy_score(y_test, clf.predict(X_test_scaled))
print(f"Accuracy (correct preprocessing): {acc:.3f}")
```

**练习 6**：Pipeline（正确封装预处理 + 模型）
```python
# pipeline_demo.py
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import numpy as np

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Pipeline：自动保证 fit/transform 的正确顺序
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(random_state=42))
])

pipe.fit(X_train, y_train)
print(f"Test accuracy: {pipe.score(X_test, y_test):.3f}")

# 交叉验证（更可靠的评估）
cv_scores = cross_val_score(pipe, X, y, cv=5)
print(f"CV scores: {cv_scores.round(3)}")
print(f"CV mean: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
```

---

## 验收标准

- [ ] 能独立完成 Iris 数据集的完整分类闭环
- [ ] 能解释 accuracy、precision、F1 的区别，知道什么时候 F1 比 accuracy 更有用
- [ ] 能演示"深度太大的决策树会过拟合"
- [ ] 预处理时，`fit` 只在训练集上，`transform` 用在两个集合
- [ ] 知道 `Pipeline` 为什么能防止数据泄漏

---

## ⚠️ 最容易踩的坑

1. **在全数据上 fit 预处理器** — `scaler.fit(X)` 然后 split，导致测试集信息泄漏
2. **只看 accuracy 就决定模型好坏** — 不平衡数据集下 accuracy 会骗人，看 F1
3. **测试集反复调参** — 测试集只用一次，调参用交叉验证

# Round 20 · PyTorch 入门

> **定位**（路线 C 第 3 步）：第一次正式进入深度学习框架，目标是把 PyTorch 的最小训练工作流真正跑通。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | Tensor + Dataset/DataLoader + nn.Module + 训练循环 + 保存加载模型 |
| **难度** | ⭐⭐⭐⭐☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 19 |
| **下一轮** | Round 21 · NLP 前置基础 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能用自己的话解释 tensor 是什么，知道它与 NumPy ndarray 的关系
- [ ] 理解为什么训练通常绕着 `Dataset` 和 `DataLoader` 展开
- [ ] 能自己写一个最小的 `nn.Module`
- [ ] 能写出完整训练循环（loss + optimizer + backward + step）
- [ ] 知道 `model.eval()` 和 `torch.no_grad()` 的作用
- [ ] 能保存和加载模型权重

---

## 本轮不学什么

> 先不碰：CNN 深挖、RNN/Transformer、分布式训练、混合精度、TensorBoard、复杂实验管理

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [PyTorch – Learn the Basics / Intro](https://pytorch.org/tutorials/beginner/basics/intro.html) | 最小工作流全貌 |
| 📄 文档 2 | [PyTorch – Tensors](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html) | tensor、NumPy 关系、初始化方式 |
| 📄 文档 3 | [PyTorch – Datasets & DataLoaders](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html) | 数据如何喂进训练循环 |
| 📄 文档 4 | [PyTorch – Build the Neural Network](https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) | nn.Module、forward、设备选择 |
| 📄 文档 5 | [PyTorch – Optimizing Model Parameters](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) | loss、optimizer、训练/测试循环 |
| 📄 文档 6 | [PyTorch – Save and Load the Model](https://pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html) | 保存权重、加载、model.eval() |

---

## 训练循环核心步骤

```python
# 每个 batch 的训练步骤
for X_batch, y_batch in dataloader:
    # 1. 前向传播
    pred = model(X_batch)
    loss = loss_fn(pred, y_batch)
    
    # 2. 反向传播
    loss.backward()
    
    # 3. 更新参数
    optimizer.step()
    
    # 4. 清零梯度（下一个 batch 之前必须做）
    optimizer.zero_grad()
```

---

## 3 周学习安排

### 第 1 周：Tensor、数据和 DataLoader

**目标**：把 PyTorch 的数据层直觉建立起来。

**Tensor 关键点**：
- Tensor 是一种和数组/矩阵非常相似的专用数据结构
- 和 NumPy 数组经常能共享底层内存
- 对自动微分（autograd）做了优化
- 可以在 GPU 上运行（`.to(device)`）

---

### 第 2 周：nn.Module + 训练循环

**目标**：能自己写一个最小神经网络，并完成一次训练。

**nn.Module 基本结构**：
```python
class MyModel(nn.Module):
    def __init__(self):
        super().__init__()
        # 在 __init__ 里定义层
        
    def forward(self, x):
        # 在 forward 里定义输入如何流过这些层
        return x
```

---

### 第 3 周：eval 模式 + 保存加载

**目标**：养成两个重要习惯：测试时切 `eval()`，只推理时用 `no_grad()`。

---

## 本轮练习清单

### 准备工作

```bash
pip install torch torchvision
mkdir -p ~/cli-lab/round20
cd ~/cli-lab/round20
```

---

### 第 1 周练习

**练习 1**：Tensor 基础
```python
# tensor_basics.py
import torch
import numpy as np

# 创建 tensor
x = torch.tensor([1.0, 2.0, 3.0])
y = torch.zeros(3, 4)
z = torch.ones(2, 3)
r = torch.rand(4, 4)

print(f"x: {x}, dtype: {x.dtype}")
print(f"y shape: {y.shape}")
print(f"r shape: {r.shape}")

# NumPy 互转
arr = np.array([1, 2, 3], dtype=np.float32)
t = torch.from_numpy(arr)      # NumPy → Tensor（共享内存）
back = t.numpy()                # Tensor → NumPy

print(f"arr: {arr}")
print(f"tensor: {t}")

# 设备检查
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
t_device = t.to(device)
```

**练习 2**：Tensor 操作
```python
# tensor_ops.py
import torch

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([[5.0, 6.0], [7.0, 8.0]])

print("加法:", a + b)
print("矩阵乘法:", a @ b)
print("元素乘法:", a * b)
print("转置:", a.T)
print("形状变换:", a.reshape(4))
print("求和:", a.sum(), "按行:", a.sum(dim=1))
```

**练习 3**：自定义 Dataset
```python
# custom_dataset.py
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class SimpleDataset(Dataset):
    """一个最简单的自定义 Dataset"""
    def __init__(self, n_samples=100, n_features=10, random_state=42):
        np.random.seed(random_state)
        self.X = torch.FloatTensor(
            np.random.randn(n_samples, n_features)
        )
        self.y = torch.LongTensor(
            np.random.randint(0, 2, n_samples)
        )
    
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# 使用 DataLoader 按 batch 加载
dataset = SimpleDataset(n_samples=100)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

for batch_idx, (X_batch, y_batch) in enumerate(dataloader):
    print(f"Batch {batch_idx}: X={X_batch.shape}, y={y_batch.shape}")
    if batch_idx >= 2:
        break
```

---

### 第 2 周练习

**练习 4**：最小 nn.Module
```python
# simple_model.py
import torch
import torch.nn as nn

class SimpleClassifier(nn.Module):
    """一个最简单的两层全连接分类网络"""
    def __init__(self, input_size, hidden_size, num_classes):
        super().__init__()
        # 在 __init__ 里定义层
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, num_classes)
    
    def forward(self, x):
        # 在 forward 里定义数据流向
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

# 创建模型
model = SimpleClassifier(input_size=10, hidden_size=64, num_classes=2)
print(model)

# 查看参数
total_params = sum(p.numel() for p in model.parameters())
print(f"Total parameters: {total_params}")

# 前向传播测试
x = torch.rand(4, 10)  # batch_size=4, input_size=10
output = model(x)
print(f"Input shape: {x.shape}")
print(f"Output shape: {output.shape}")
```

**练习 5**：完整训练循环
```python
# train_loop.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from simple_model import SimpleClassifier
from custom_dataset import SimpleDataset

# 准备数据
train_dataset = SimpleDataset(n_samples=800)
test_dataset = SimpleDataset(n_samples=200, random_state=99)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32)

# 模型、损失函数、优化器
device = "cuda" if torch.cuda.is_available() else "cpu"
model = SimpleClassifier(10, 64, 2).to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

def train_epoch(model, dataloader, loss_fn, optimizer, device):
    model.train()  # 设为训练模式
    total_loss = 0
    for X, y in dataloader:
        X, y = X.to(device), y.to(device)
        
        # 前向传播
        pred = model(X)
        loss = loss_fn(pred, y)
        
        # 反向传播 + 更新
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        
        total_loss += loss.item()
    return total_loss / len(dataloader)

def evaluate(model, dataloader, device):
    model.eval()  # 设为评估模式
    correct = 0
    total = 0
    with torch.no_grad():  # 不计算梯度，节省内存
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            correct += (pred.argmax(1) == y).sum().item()
            total += len(y)
    return correct / total

# 训练 10 个 epoch
for epoch in range(10):
    train_loss = train_epoch(model, train_loader, loss_fn, optimizer, device)
    test_acc = evaluate(model, test_loader, device)
    print(f"Epoch {epoch+1:2d}: loss={train_loss:.4f}, test_acc={test_acc:.3f}")
```

---

### 第 3 周练习

**练习 6**：保存和加载模型
```python
# save_load.py
import torch
from simple_model import SimpleClassifier

# 假设 model 已训练
model = SimpleClassifier(10, 64, 2)

# 保存模型权重（推荐方式）
torch.save(model.state_dict(), "model.pth")
print("Model saved to model.pth")

# 加载模型
model_loaded = SimpleClassifier(10, 64, 2)   # 先创建同样结构的模型
model_loaded.load_state_dict(torch.load("model.pth"))
model_loaded.eval()  # ⚠️ 推理前必须切 eval 模式
print("Model loaded and set to eval mode")

# 推理
x = torch.rand(3, 10)
with torch.no_grad():  # 推理时不计算梯度
    output = model_loaded(x)
    pred = output.argmax(1)
print(f"Predictions: {pred}")
```

**练习 7**：用 FashionMNIST 跑完整流程（官方推荐路线）
```python
# fashion_mnist.py
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# 数据
transform = transforms.Compose([transforms.ToTensor()])
train_data = datasets.FashionMNIST("data", train=True, download=True, transform=transform)
test_data = datasets.FashionMNIST("data", train=False, download=True, transform=transform)
train_loader = DataLoader(train_data, batch_size=64, shuffle=True)
test_loader = DataLoader(test_data, batch_size=64)

# 模型：28×28 灰度图 → 10 个类别
class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.net = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )
    
    def forward(self, x):
        return self.net(self.flatten(x))

device = "cuda" if torch.cuda.is_available() else "cpu"
model = NeuralNetwork().to(device)
loss_fn = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)

# 训练 3 个 epoch
for epoch in range(3):
    model.train()
    for X, y in train_loader:
        X, y = X.to(device), y.to(device)
        loss = loss_fn(model(X), y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
    
    model.eval()
    correct = sum((model(X.to(device)).argmax(1) == y.to(device)).sum().item()
                  for X, y in test_loader)
    print(f"Epoch {epoch+1}: Test accuracy = {correct/len(test_data):.3f}")
```

---

## 训练/测试模式区别

| 模式 | 设置方式 | Dropout | BatchNorm | 梯度 |
|------|---------|---------|-----------|------|
| 训练 | `model.train()` | 随机丢弃 | 用 batch 统计 | 计算 |
| 评估/推理 | `model.eval()` | 不丢弃 | 用全局统计 | 不计算（配合 `no_grad`） |

---

## 验收标准

- [ ] 能解释 tensor 和 NumPy array 的关系
- [ ] 能自己写 `Dataset.__len__` 和 `Dataset.__getitem__`
- [ ] 能写一个继承 `nn.Module` 的网络类，有 `__init__` 和 `forward`
- [ ] 训练循环包含：`forward → loss → backward → step → zero_grad`
- [ ] 测试时使用 `model.eval()` + `torch.no_grad()`
- [ ] 能保存 `state_dict` 并重新加载

---

## ⚠️ 最容易踩的坑

1. **忘记 `optimizer.zero_grad()`** — 梯度会累积，下一个 batch 结果错误
2. **推理时忘切 `model.eval()`** — Dropout/BatchNorm 行为不同，结果不稳定
3. **保存整个模型而不是 state_dict** — `torch.save(model.state_dict())` 更推荐，更稳定

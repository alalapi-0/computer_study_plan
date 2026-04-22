# Round 21 · NLP 前置基础

> **定位**（路线 C 第 4 步）：把 PyTorch 最小训练闭环正式接到文本任务，但不直接上 Transformer 微调。先把"文本如何进入模型"这层搞清楚。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 文本预处理 + tokenization + 词表/编号 + embedding 直觉 + 最小文本分类 |
| **难度** | ⭐⭐⭐⭐☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 20 |
| **下一轮** | 自由拓展（Transformer 微调 / Hugging Face 入门） |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能解释为什么模型不能直接吃原始文本，必须先经过 tokenization 和数值化
- [ ] 理解"词表"就是 token ↔ id 的映射
- [ ] 能解释 embedding 为什么被说成"把 token id 变成稠密向量"
- [ ] 做一个最小文本分类任务（哪怕模型很简单）
- [ ] 知道 BPE 和 WordPiece 是两种常见的分词策略

---

## 本轮不学什么

> 先不碰：Transformer 微调、预训练语言模型内部结构、注意力机制细节、命名实体识别、序列标注对齐、长文本建模

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Hugging Face – Tokenizers](https://huggingface.co/learn/nlp-course/chapter2/4) | 文本为什么必须先变成数字 |
| 📄 文档 2 | [Hugging Face – Tokenizers Quicktour](https://huggingface.co/docs/tokenizers/quicktour) | special tokens、词表 |
| 📄 文档 3 | [PyTorch – nn.Embedding](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html) | embedding 层的最小直觉 |
| 📄 文档 4 | [PyTorch – Word Embeddings Tutorial](https://pytorch.org/tutorials/beginner/nlp/word_embeddings_tutorial.html) | 词向量的工程实现 |
| 📄 文档 5 | [scikit-learn – Working With Text Data](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html) | 传统文本分类闭环 |

---

## 两条理解路线

| 路线 | 方法 | 特点 |
|------|------|------|
| **传统** | Bag-of-words / TF-IDF → 线性分类器 | 简单、可解释、适合理解"文本必须数值化" |
| **深度学习** | tokenizer → token ids → embedding → 模型 | 现代 NLP 主流，接 PyTorch 训练闭环 |

> **本轮建议**：两条路线都理解，但主线做深度学习路线，传统路线作为对照理解。

---

## 3 周学习安排

### 第 1 周：文本预处理、tokenization、词表与编号

**目标**：把"文本如何变成数字"讲清楚。

**手动理解最小流程**：
```
一句文本
  ↓ 分词（tokenize）
token 列表
  ↓ 建词表（vocabulary: token → id）
id 列表
  ↓ 转 tensor
模型可处理的输入
```

**两种重要分词策略**：
- **BPE**（Byte-Pair Encoding）：GPT、RoBERTa、BART 等使用
- **WordPiece**：BERT 系列使用，`##` 表示子词

---

### 第 2 周：nn.Embedding + 最小文本分类

**目标**：把"token id → 向量"这一步用 PyTorch 实现，并做一个最小文本分类任务。

**nn.Embedding 本质**：
- 是一个"按索引查向量"的查表层
- 输入：整数索引（token id）
- 输出：对应的稠密向量（embedding）
- 参数：`vocab_size`（词表大小）、`embedding_dim`（向量维度）

---

### 第 3 周：对照传统文本特征 + 完善

**目标**：了解传统路线，理解"文本必须数值化"的本质不变。

---

## 本轮练习清单

### 准备工作

```bash
pip install torch transformers scikit-learn
mkdir -p ~/cli-lab/round21
cd ~/cli-lab/round21
```

---

### 第 1 周练习

**练习 1**：手动实现最朴素 tokenizer
```python
# manual_tokenizer.py
class SimpleTokenizer:
    """最朴素的空格分词 tokenizer"""
    
    def __init__(self):
        self.vocab = {}        # token → id
        self.id_to_token = {}  # id → token
        # 特殊 token
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"
        self._add_special_tokens()
    
    def _add_special_tokens(self):
        for token in [self.pad_token, self.unk_token]:
            idx = len(self.vocab)
            self.vocab[token] = idx
            self.id_to_token[idx] = token
    
    def build_vocab(self, texts: list):
        """从文本列表构建词表"""
        for text in texts:
            for token in text.lower().split():
                if token not in self.vocab:
                    idx = len(self.vocab)
                    self.vocab[token] = idx
                    self.id_to_token[idx] = token
    
    def encode(self, text: str) -> list:
        """文本 → id 列表"""
        unk_id = self.vocab[self.unk_token]
        return [self.vocab.get(t, unk_id) for t in text.lower().split()]
    
    def decode(self, ids: list) -> str:
        """id 列表 → 文本"""
        return " ".join(self.id_to_token.get(i, self.unk_token) for i in ids)

# 测试
corpus = [
    "the cat sat on the mat",
    "the dog ran in the park",
    "cats and dogs are great pets"
]

tokenizer = SimpleTokenizer()
tokenizer.build_vocab(corpus)
print(f"Vocabulary size: {len(tokenizer.vocab)}")
print(f"Vocab: {tokenizer.vocab}")

text = "the cat ran fast"
ids = tokenizer.encode(text)
back = tokenizer.decode(ids)
print(f"\nOriginal: {text}")
print(f"Encoded:  {ids}")
print(f"Decoded:  {back}")
```

**练习 2**：用 Hugging Face tokenizer（现代方式）
```python
# hf_tokenizer_demo.py
from transformers import AutoTokenizer

# 加载预训练 tokenizer（会下载，第一次需要网络）
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

texts = [
    "Hello, how are you?",
    "The quick brown fox jumps over the lazy dog",
    "PyTorch is a deep learning framework",
]

for text in texts:
    encoded = tokenizer(text)
    tokens = tokenizer.convert_ids_to_tokens(encoded["input_ids"])
    print(f"\nText: {text}")
    print(f"Tokens: {tokens}")
    print(f"IDs: {encoded['input_ids']}")
    # [CLS] 和 [SEP] 是 BERT 的 special tokens
```

---

### 第 2 周练习

**练习 3**：nn.Embedding 基础
```python
# embedding_demo.py
import torch
import torch.nn as nn

# 创建 embedding 层
# vocab_size=10（词表10个词），embedding_dim=5（每个词映射成5维向量）
embedding = nn.Embedding(num_embeddings=10, embedding_dim=5)

# 输入：整数索引
token_ids = torch.tensor([1, 3, 5, 2])
embeddings = embedding(token_ids)

print(f"Input ids: {token_ids}")
print(f"Embedding shape: {embeddings.shape}")  # (4, 5)
print(f"Embedding values:\n{embeddings}")

# 关键理解：不同 id 对应不同向量
print(f"\nToken 1: {embedding(torch.tensor([1]))[0]}")
print(f"Token 2: {embedding(torch.tensor([2]))[0]}")
```

**练习 4**：最小文本分类（深度学习路线）
```python
# text_classify_dl.py
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from manual_tokenizer import SimpleTokenizer

# 准备数据：简单情感分类
texts = [
    "great movie love it",
    "terrible waste of time",
    "amazing wonderful film",
    "horrible boring awful",
    "fantastic excellent",
    "disappointing bad bad",
    "really enjoyed this",
    "hated every minute",
    "brilliant masterpiece",
    "total garbage trash",
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]  # 1=正面, 0=负面

# 构建 tokenizer
tokenizer = SimpleTokenizer()
tokenizer.build_vocab(texts)
vocab_size = len(tokenizer.vocab)

# Dataset
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=10):
        self.data = []
        pad_id = tokenizer.vocab["<PAD>"]
        for text, label in zip(texts, labels):
            ids = tokenizer.encode(text)[:max_len]
            # padding 到 max_len
            ids += [pad_id] * (max_len - len(ids))
            self.data.append((torch.tensor(ids), torch.tensor(label)))
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]

# 模型：embedding + 均值池化 + 线性层
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.fc = nn.Linear(embed_dim, num_classes)
    
    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x)     # (batch, seq_len, embed_dim)
        pooled = embedded.mean(dim=1)    # (batch, embed_dim) - 简单均值池化
        return self.fc(pooled)

# 训练
dataset = TextDataset(texts, labels, tokenizer)
loader = DataLoader(dataset, batch_size=4, shuffle=True)

model = TextClassifier(vocab_size=vocab_size, embed_dim=16, num_classes=2)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = nn.CrossEntropyLoss()

for epoch in range(20):
    model.train()
    total_loss = 0
    for X, y in loader:
        pred = model(X)
        loss = loss_fn(pred, y)
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        total_loss += loss.item()
    
    if (epoch + 1) % 5 == 0:
        model.eval()
        with torch.no_grad():
            X_all = torch.stack([d[0] for d in dataset])
            y_all = torch.stack([d[1] for d in dataset])
            acc = (model(X_all).argmax(1) == y_all).float().mean()
        print(f"Epoch {epoch+1}: loss={total_loss/len(loader):.4f}, acc={acc:.3f}")
```

---

### 第 3 周练习

**练习 5**：传统文本分类（对照路线）
```python
# text_classify_traditional.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 数据（和深度学习版本一样）
texts = [
    "great movie love it", "terrible waste of time",
    "amazing wonderful film", "horrible boring awful",
    "fantastic excellent", "disappointing bad bad",
    "really enjoyed this", "hated every minute",
    "brilliant masterpiece", "total garbage trash",
]
labels = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

# TF-IDF 特征提取（传统"数值化"方式）
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

print(f"Feature matrix shape: {X.shape}")
print(f"Vocabulary: {list(vectorizer.vocabulary_.items())[:10]}")

# 训练线性分类器
clf = LogisticRegression()
clf.fit(X, labels)

# 评估
y_pred = clf.predict(X)
print(f"\nAccuracy: {accuracy_score(labels, y_pred):.3f}")
print(classification_report(labels, y_pred, target_names=["negative", "positive"]))

# 新文本预测
new_texts = ["wonderful great movie", "terrible waste"]
X_new = vectorizer.transform(new_texts)
predictions = clf.predict(X_new)
for text, pred in zip(new_texts, predictions):
    sentiment = "positive" if pred == 1 else "negative"
    print(f"'{text}' → {sentiment}")
```

**练习 6**：对比两条路线

```python
# compare_approaches.py
"""
对比传统 NLP 路线 vs 深度学习路线

传统路线：
  文本 → TF-IDF 稀疏向量 → 线性分类器
  优点：简单、可解释、不需要 GPU
  缺点：词序信息丢失、无法捕获语义相似性

深度学习路线：
  文本 → tokenizer → token ids → embedding → 神经网络
  优点：可以学到语义、上下文关系
  缺点：需要更多数据和算力

两条路线的共同点：
  文本都必须先被转成数值表示，模型才能处理
"""

print("传统路线的数值化：")
print("  'great movie' → TF-IDF 稀疏向量 [0, 0.7, 0, 0.4, 0, ...]")
print("  向量维度 = 词表大小（可能几千）")
print("  每个位置 = 该词的 TF-IDF 权重")

print("\n深度学习路线的数值化：")
print("  'great movie' → token ids [3, 8]")
print("  → embedding 向量 [[0.1, -0.3, 0.5, ...], [0.7, 0.2, -0.1, ...]]")
print("  每个 token 对应一个可学习的稠密向量")
```

---

## 验收标准

- [ ] 能解释"为什么模型不能直接吃原始文本"
- [ ] 手动实现了 `SimpleTokenizer`（build_vocab + encode + decode）
- [ ] 理解 `nn.Embedding` 的输入是整数，输出是向量
- [ ] 做出了最小文本分类模型（深度学习路线）
- [ ] 知道传统路线（TF-IDF）和深度学习路线的核心区别

---

## ⚠️ 最容易踩的坑

1. **tokenization ≠ 按空格分词** — BPE/WordPiece 是子词级别的，一个词可能被分成多个 token
2. **embedding 不是固定词典** — embedding 权重是可学习的，会在训练中更新
3. **padding 处理** — 不同长度的序列需要 padding 到同等长度，且 `padding_idx=0` 让 pad token 的梯度为 0

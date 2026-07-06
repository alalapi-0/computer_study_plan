# Round 21 · NLP 前置基础

> **定位**（路线 C 第 4 步）：把 PyTorch 最小训练闭环正式接到文本任务，但不直接上 Transformer 微调。先把“文本如何进入模型”这层搞清楚。

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

## Web UI 完成方式

打开：

```bash
python3 scripts/progress_server.py --host 127.0.0.1 --port 8777
```

然后访问：

```text
http://127.0.0.1:8777/progress.html?round=round_21
```

推荐顺序：

1. 在 Web UI 中展开 Round 21。
2. 点“读教程”直接阅读每周 notes，外部资料链接会新标签页打开。
3. 点“运行脚本”生成本周练习产物，所有输出只写入 `~/cli-lab/round21`。
4. 点“终端练习”在浏览器映射终端中运行短命令 smoke check。
5. 完成自测、小抄和验收后，再用“记录并完成”写入自己的学习记录。

本轮 Web UI 自动练习**不执行** `pip install torch transformers scikit-learn`，也不下载模型。脚本会生成真实 PyTorch / Hugging Face / scikit-learn 风格代码，并用 Python 标准库做可运行 smoke check；以后你想在本机深入运行这些示例时，再自行安装对应依赖。

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能解释为什么模型不能直接吃原始文本，必须先经过 tokenization 和数值化
- [ ] 理解“词表”就是 token 到 id、id 到 token 的双向映射
- [ ] 能解释 embedding 为什么被说成“把 token id 变成稠密向量”
- [ ] 能描述最小文本分类路线：文本 → token ids → padding → embedding → pooling → classifier
- [ ] 知道 Bag-of-words / TF-IDF 与深度学习路线的区别
- [ ] 知道 BPE 和 WordPiece 是两种常见子词分词策略

---

## 本轮不学什么

先不碰：Transformer 微调、预训练语言模型内部结构、注意力机制细节、命名实体识别、序列标注对齐、长文本建模。

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 文档 1 | [Hugging Face – Tokenizers](https://huggingface.co/learn/nlp-course/chapter2/4) | 文本为什么必须先变成 token 和 id |
| 文档 2 | [Hugging Face – Tokenizers Quicktour](https://huggingface.co/docs/tokenizers/quicktour) | special tokens、词表、encode/decode |
| 文档 3 | [PyTorch – nn.Embedding](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html) | embedding 层的最小直觉 |
| 文档 4 | [PyTorch – Word Embeddings Tutorial](https://pytorch.org/tutorials/beginner/nlp/word_embeddings_tutorial.html) | 词向量的工程实现 |
| 文档 5 | [scikit-learn – Working With Text Data](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html) | 传统文本分类闭环 |

---

## 两条理解路线

| 路线 | 方法 | 特点 |
|------|------|------|
| 传统路线 | Bag-of-words / TF-IDF → 线性分类器 | 简单、可解释、适合理解“文本必须数值化” |
| 深度学习路线 | tokenizer → token ids → embedding → 模型 | 现代 NLP 主流，接 Round 20 的 PyTorch 训练闭环 |

本轮建议两条路线都理解，但主线做深度学习路线，传统路线作为对照。

---

## 3 周学习安排

### 第 1 周：文本预处理、tokenization、词表与编号

目标：把“文本如何变成数字”讲清楚。

最小流程：

```text
一句文本
  -> tokenize 得到 token 列表
  -> build_vocab 得到 token_to_id / id_to_token
  -> encode 得到 id 列表
  -> padding / tensor 化
  -> 模型可处理的输入
```

Web UI 运行练习会生成：

- `manual_tokenizer.py`：手写 `SimpleTokenizer`
- `sample_texts.json`：样例语料
- `tokenizer_strategy_notes.json`：BPE / WordPiece 对照
- `stdlib_tokenizer_smoke.py`：标准库 smoke check
- `tokenizer_summary.json`：自测输出
- `static_check_report.json`：静态合同检查

浏览器终端短命令：

```bash
cd ~/cli-lab/round21/week1_auto/tokenizer_vocab
python3 stdlib_tokenizer_smoke.py
cat tokenizer_summary.json
```

### 第 2 周：nn.Embedding + 最小文本分类

目标：把“token id → 向量”这一步用代码结构讲清楚，并做一个最小情感分类模型形状。

核心直觉：

- `nn.Embedding(vocab_size, embedding_dim)` 是一张可学习查表矩阵。
- 输入是整数 token id，输出是每个 token 对应的稠密向量。
- 不同长度文本需要 padding 到同一长度。
- 最小分类器可以先做 embedding，再做均值池化，再接线性分类层。

Web UI 运行练习会生成：

- `embedding_demo.py`：PyTorch `nn.Embedding` 形状示例
- `text_classifier.py`：embedding + mean pooling + classifier 代码形状
- `sample_sentiment.json`：样例情感数据
- `stdlib_embedding_smoke.py`：标准库 embedding 直觉自测
- `embedding_summary.json`：自测输出
- `static_check_report.json`：静态合同检查

浏览器终端短命令：

```bash
cd ~/cli-lab/round21/week2_auto/embedding_classifier
python3 stdlib_embedding_smoke.py
cat embedding_summary.json
```

### 第 3 周：传统文本特征 + 子词策略对照

目标：理解传统 NLP 路线，知道文本数值化不只有 embedding 一条路。

核心对照：

| 主题 | 传统路线 | 深度学习路线 |
|------|----------|--------------|
| 数值化 | Count / TF-IDF 稀疏向量 | token ids + embedding 稠密向量 |
| 模型 | 线性分类器常见 | 神经网络常见 |
| 优点 | 简单、可解释、数据少也能用 | 表达能力强，可接现代 NLP |
| 代价 | 词序和语义弱 | 需要更多数据和训练 |

Web UI 运行练习会生成：

- `traditional_text_features.py`：scikit-learn 风格文本特征示例
- `subword_compare.py`：BPE / WordPiece / whitespace 对照
- `stdlib_text_features_smoke.py`：标准库文本特征自测
- `text_features_summary.json`：自测输出
- `static_check_report.json`：静态合同检查

浏览器终端短命令：

```bash
cd ~/cli-lab/round21/week3_auto/text_features
python3 stdlib_text_features_smoke.py
cat text_features_summary.json
```

---

## 最终验收

点 Web UI 中的“综合练习：完整 NLP 前置基础项目包”后，会生成：

- `tokenizer.py`
- `dataset.py`
- `embedding_model.py`
- `traditional_baseline.py`
- `data/sentiment_samples.csv`
- `pipeline_contract.json`
- `stdlib_smoke.py`
- `final_static_check.py`
- `round21_final_summary.json`

最终你需要能口头解释：

- tokenization 和普通字符串切分有什么区别
- special tokens 为什么要有 `<PAD>` 和 `<UNK>`
- vocab_size、embedding_dim、sequence length 分别是什么意思
- padding 为什么会影响 pooling
- TF-IDF 与 embedding 各自适合什么场景

---

## 最容易踩的坑

1. tokenization 不等于永远按空格分词。BPE / WordPiece 会把词拆成子词。
2. token id 不是语义本身，它只是查 embedding 表的索引。
3. embedding 权重是可学习参数，会随着训练更新。
4. padding 是为了凑齐 batch 形状，不应该被当成真实词贡献语义。
5. Web UI 的浏览器终端是沙盒映射终端，不用于安装大依赖或下载模型。

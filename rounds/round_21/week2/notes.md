# Round 21 · Week 2：Embedding 与最小文本分类

## Web UI 学习路径

1. 先读完本页，确认 Week 1 的 token id 是整数索引。
2. 点“练习：生成 embedding 与文本分类示例”，生成本周代码形状。
3. 点“终端练习”，运行短命令 smoke check。
4. 能解释 `embedding_dim`、`padding_idx`、`mean pooling` 后，点击“记录并完成”保存本周自测记录。

## 本周核心直觉

`nn.Embedding` 可以先理解成一张表：

```text
token id -> embedding table row -> dense vector
```

| 概念 | 解释 |
|------|------|
| `vocab_size` | 表里有多少行，通常等于词表大小 |
| `embedding_dim` | 每个 token 被映射成多少维向量 |
| `padding_idx` | 哪个 id 是 padding，训练时不把它当成真实词 |
| pooling | 把一段 token 向量汇总成一个句子向量 |
| classifier | 用句子向量做分类预测 |

最小文本分类路径：

```text
texts
  -> tokenizer.encode
  -> pad to same length
  -> embedding(ids)
  -> mean pooling
  -> linear classifier
  -> loss / optimizer
```

## 推荐外链

- [PyTorch nn.Embedding](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
- [PyTorch Word Embeddings Tutorial](https://pytorch.org/tutorials/beginner/nlp/word_embeddings_tutorial.html)

## 自动练习产物

点“运行脚本”后会生成：

- `~/cli-lab/round21/week2_auto/embedding_classifier/embedding_demo.py`
- `~/cli-lab/round21/week2_auto/embedding_classifier/text_classifier.py`
- `~/cli-lab/round21/week2_auto/embedding_classifier/sample_sentiment.json`
- `~/cli-lab/round21/week2_auto/embedding_classifier/stdlib_embedding_smoke.py`
- `~/cli-lab/round21/week2_auto/embedding_classifier/embedding_summary.json`
- `~/cli-lab/round21/week2_auto/embedding_classifier/static_check_report.json`

## 浏览器终端自测

在本周练习运行成功后，点击“终端练习”，逐行输入：

```bash
cd ~/cli-lab/round21/week2_auto/embedding_classifier
python3 stdlib_embedding_smoke.py
cat embedding_summary.json
```

看到 `embedding_dim`、`pooled_vector`、`prediction` 后，解释：

- token id 为什么不是语义向量
- embedding 表为什么可以学习
- padding token 为什么不能直接参与平均

## 完成标准

- [ ] 能解释 `nn.Embedding(vocab_size, embedding_dim)`
- [ ] 能解释 padding 与 `padding_idx`
- [ ] 能说清楚 embedding + mean pooling + classifier 的最小结构
- [ ] 知道本周 Web UI 生成的是真实代码形状，但 smoke check 不依赖 PyTorch

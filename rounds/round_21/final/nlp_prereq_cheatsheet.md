# Round 21 · NLP 前置基础速查

## Web UI 完成顺序

1. Week 1：阅读 tokenization / vocab，运行 tokenizer 练习。
2. Week 2：阅读 embedding / classifier，运行最小文本分类练习。
3. Week 3：阅读 TF-IDF / 子词策略，运行传统文本特征练习。
4. Final：运行完整 NLP 前置基础项目包。
5. 在“记录并完成”中写下你自己的解释和证据路径。

## 一句话主线

```text
原始文本 -> token -> token id -> 数值特征 -> 模型
```

## 核心概念表

| 概念 | 速查 |
|------|------|
| tokenization | 把文本切成模型可管理的 token 单位 |
| vocabulary | token 和整数 id 的映射 |
| encode/decode | 文本和 id 列表之间的转换 |
| `<PAD>` | 补齐 batch 长度 |
| `<UNK>` | 处理词表外 token |
| embedding | 用 token id 查可学习稠密向量 |
| mean pooling | 把一段 token 向量汇总成句子向量 |
| TF-IDF | 用词频和逆文档频率表示文本 |
| BPE / WordPiece | 子词分词策略，降低生词压力 |

## 传统路线 vs 深度学习路线

| 路线 | 输入处理 | 常见模型 | 优点 | 注意 |
|------|----------|----------|------|------|
| 传统文本分类 | Count / TF-IDF 稀疏向量 | Logistic Regression / Linear SVM | 简单、可解释 | 词序和语义弱 |
| 深度学习文本分类 | token ids + embedding | embedding + pooling + classifier | 可学习语义表示 | 需要更多数据和训练 |

## 最终自问

- 为什么原始字符串不能直接喂给模型？
- 为什么 token id 不是语义向量？
- `<PAD>` 和 `<UNK>` 分别解决什么问题？
- embedding 表的形状和 `vocab_size`、`embedding_dim` 有什么关系？
- TF-IDF 与 embedding 的差别是什么？
- BPE / WordPiece 为什么比简单空格分词更适合现代 NLP？

## 最小通过标准

- Week 1–3 的自动练习均可通过 Web UI 运行。
- 浏览器终端能运行三段 smoke check 短命令。
- Final 项目包能生成 `round21_final_summary.json`。
- 能对照 `round_21.md` 说明本轮与 Round 20 的关系。

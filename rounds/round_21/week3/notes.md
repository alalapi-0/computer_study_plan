# Round 21 · Week 3：传统文本特征与子词策略

## Web UI 学习路径

1. 先复盘 Week 1 的 token ids 和 Week 2 的 embedding。
2. 点“练习：生成传统文本特征与子词对照示例”，生成本周产物。
3. 点“终端练习”，运行短命令 smoke check。
4. 能比较 TF-IDF 与 embedding 后，点击“记录并完成”保存本周自测记录。

## 本周核心直觉

文本数值化不只有 embedding 一条路。传统机器学习常用：

```text
text -> tokens -> counts / TF-IDF vector -> linear classifier
```

| 对照点 | Bag-of-words / TF-IDF | token ids + embedding |
|--------|-----------------------|-----------------------|
| 向量类型 | 稀疏高维 | 稠密低维 |
| 是否学习词向量 | 通常不学习 | embedding 会学习 |
| 可解释性 | 较强，能看到词权重 | 较弱，需要看模型 |
| 对词序 | 基本弱化 | 可继续接更复杂模型 |

## 子词策略复盘

| 策略 | 示例 | 你要记住的点 |
|------|------|--------------|
| whitespace | `unbelievable movie` -> `["unbelievable", "movie"]` | 简单但遇到生词容易 `<UNK>` |
| BPE | `unbelievable` 可能拆成更小片段 | 高频片段逐步合并 |
| WordPiece | `playing` 可能成 `["play", "##ing"]` | BERT 系常见 `##` 子词标记 |

## 推荐外链

- [scikit-learn Working With Text Data](https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html)
- [Hugging Face Tokenizers Quicktour](https://huggingface.co/docs/tokenizers/quicktour)

## 自动练习产物

点“运行脚本”后会生成：

- `~/cli-lab/round21/week3_auto/text_features/traditional_text_features.py`
- `~/cli-lab/round21/week3_auto/text_features/subword_compare.py`
- `~/cli-lab/round21/week3_auto/text_features/stdlib_text_features_smoke.py`
- `~/cli-lab/round21/week3_auto/text_features/text_features_summary.json`
- `~/cli-lab/round21/week3_auto/text_features/static_check_report.json`

## 浏览器终端自测

在本周练习运行成功后，点击“终端练习”，逐行输入：

```bash
cd ~/cli-lab/round21/week3_auto/text_features
python3 stdlib_text_features_smoke.py
cat text_features_summary.json
```

看到 `vocabulary_size`、`top_features`、`predictions` 后，解释：

- 为什么传统路线也必须先把文本变成数字
- TF-IDF 和 embedding 的输出形态有什么差别
- BPE / WordPiece 为什么能缓解生词问题

## 完成标准

- [ ] 能解释 Bag-of-words / TF-IDF 的作用
- [ ] 能比较传统文本分类和 embedding 分类路线
- [ ] 能解释 BPE / WordPiece 的基本动机
- [ ] 能用 Web UI 终端查看本周 smoke check 输出

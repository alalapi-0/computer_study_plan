# Round 21 · Week 1：Tokenization、词表与编号

## Web UI 学习路径

1. 打开 `http://127.0.0.1:8777/progress.html?round=round_21`，展开 Round 21。
2. 点本任务的“读教程”，先把 tokenization、vocab、encode/decode 的流程看完。
3. 点“练习：生成手写 tokenizer 与词表编号示例”，生成本周产物。
4. 点“终端练习”，运行本页下方短命令，看 `tokenizer_summary.json`。
5. 能解释输出后，再点击“记录并完成”保存“自测：终端运行 tokenizer smoke check”。

## 本周要建立的直觉

原始文本不能直接进入模型。模型能处理的是数字，所以文本要先经历：

```text
text -> tokens -> token ids -> padded ids -> tensor
```

| 名词 | 你需要会说的话 |
|------|----------------|
| tokenization | 把文本切成模型约定的 token 单位 |
| vocabulary | token 到 id 的映射表 |
| encode | 文本转成 token id 列表 |
| decode | token id 列表转回可读 token |
| `<PAD>` | 补齐长度用的特殊 token |
| `<UNK>` | 遇到词表外 token 时的兜底 |

## 三种分词策略

| 策略 | 粗略理解 | 常见位置 |
|------|----------|----------|
| whitespace | 按空格切词，适合入门演示 | 手写 tokenizer |
| BPE | 反复合并高频子串，形成子词词表 | GPT、RoBERTa、BART 等 |
| WordPiece | 也使用子词，BERT 中常见 `##suffix` 形式 | BERT 系列 |

本周手写的 `SimpleTokenizer` 不是现代 tokenizer 的完整实现，它的作用是让你先看清楚 `build_vocab -> encode -> decode` 这条骨架。

## 推荐外链

- [Hugging Face NLP Course：Tokenizers](https://huggingface.co/learn/nlp-course/chapter2/4)
- [Hugging Face Tokenizers Quicktour](https://huggingface.co/docs/tokenizers/quicktour)

## 自动练习产物

点“运行脚本”后会生成：

- `~/cli-lab/round21/week1_auto/tokenizer_vocab/manual_tokenizer.py`
- `~/cli-lab/round21/week1_auto/tokenizer_vocab/sample_texts.json`
- `~/cli-lab/round21/week1_auto/tokenizer_vocab/tokenizer_strategy_notes.json`
- `~/cli-lab/round21/week1_auto/tokenizer_vocab/stdlib_tokenizer_smoke.py`
- `~/cli-lab/round21/week1_auto/tokenizer_vocab/tokenizer_summary.json`
- `~/cli-lab/round21/week1_auto/tokenizer_vocab/static_check_report.json`

## 浏览器终端自测

在本周练习运行成功后，点击“终端练习”，逐行输入：

```bash
cd ~/cli-lab/round21/week1_auto/tokenizer_vocab
python3 stdlib_tokenizer_smoke.py
cat tokenizer_summary.json
```

看到 `vocab_size`、`encoded`、`decoded`、`unknown_token_id` 后，解释：

- 为什么 `fast` 会变成 `<UNK>`
- 为什么 `<PAD>` 的 id 通常固定为 0
- 为什么 encode 的输出是一串整数

## 完成标准

- [ ] 能画出 `text -> tokens -> ids` 流程
- [ ] 能解释 `token_to_id` 和 `id_to_token`
- [ ] 能解释 `<PAD>` 和 `<UNK>`
- [ ] 知道 BPE / WordPiece 不是简单空格分词

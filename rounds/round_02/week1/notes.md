# Round 02 · Week 1 笔记

## 本周目标

- 理解 `>`、`>>`、`|` 的差异。
- 能写出简单的日志筛选流水线。

## 核心概念速查

| 概念 | 作用 | 常见示例 |
|---|---|---|
| 覆盖重定向 `>` | 把输出写入文件，覆盖旧内容 | `echo "a" > a.txt` |
| 追加重定向 `>>` | 把输出追加到文件末尾 | `echo "b" >> a.txt` |
| 管道 `|` | 把左侧输出作为右侧输入 | `cat app.log \| grep error` |
| 计数 `wc -l` | 统计行数 | `grep error app.log \| wc -l` |

## 常用组合

```bash
sort animals.txt | uniq
grep "error" app.log | wc -l
cat app.log | grep "info"
```

## 本周完成后你应该能回答

- [ ] `>` 和 `>>` 的行为区别是什么？
- [ ] 管道为什么能减少中间文件？
- [ ] `grep ... | wc -l` 每一步在做什么？

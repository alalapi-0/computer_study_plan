# Round 00 · Week 3 学习笔记

> **目标**：不会时先查，而不是背参数。学会用 `man` 命令查看任何命令的说明文档。

---

## 本周唯一命令

### `man` — 查命令说明

```bash
man 命令名
```

`man` 是 manual（手册）的缩写。每个 Unix/Linux 命令都有一份 man page。

示例：
```bash
man ls        # 查看 ls 的说明
man mkdir     # 查看 mkdir 的说明
man man       # 查看 man 自己的说明
```

---

## 在 man page 里的操作

进入 man page 后（你会看到一页文字），可以：

| 按键 | 操作 |
|------|------|
| `q` | **退出**（最重要，先记这个） |
| `空格` 或 `f` | 向下翻一页 |
| `b` | 向上翻一页 |
| `↓` / `↑` | 逐行上下移动 |
| `/关键词` + 回车 | 搜索 |
| `n` | 跳到下一个搜索结果 |

**只需要记住两件事**：
1. 进去之后看最上面的 **DESCRIPTION** 部分，了解命令是干什么的
2. 看完了按 **`q`** 退出

---

## man page 的结构

典型的 man page 包含这些节：

| 节名 | 内容 |
|------|------|
| **NAME** | 命令名称和一行简介 |
| **SYNOPSIS** | 命令的使用格式（方括号表示可选） |
| **DESCRIPTION** | 详细说明 |
| **OPTIONS** | 所有参数的说明 |
| **EXAMPLES** | 使用示例（不一定有） |
| **SEE ALSO** | 相关命令 |

你这周只需要能看懂 NAME 和 DESCRIPTION 就够了。

---

## 这就是"不靠死记硬背"的工作方式

命令行的世界里有几百个命令，参数更是数不清。  
没有人会全部背下来。

正确的姿势是：
1. 知道命令的用途（这周学）
2. 用的时候查参数（`man` 命令）
3. 遇到不认识的命令，`man 命令名` 先看一眼

---

## 本周资源

1. **Apple Terminal 入门 - Find the commands you need**  
   https://support.apple.com/guide/terminal/

2. **Linux Journey - Getting Help**  
   https://linuxjourney.com/lesson/help

---

## 本周完成后，你应该能回答

- [ ] `man ls` 进去之后怎么退出？
- [ ] 在 man page 里怎么搜索一个关键词？
- [ ] `man` 的 SYNOPSIS 里，方括号 `[]` 表示什么意思？
- [ ] 为什么不需要背命令参数？

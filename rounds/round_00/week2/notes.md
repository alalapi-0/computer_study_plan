# Round 00 · Week 2 学习笔记

> **目标**：第一次在终端里自己建出目录和文件。掌握 `mkdir`、`touch`、`cat`。

---

## 本周三个命令

### `mkdir` — 创建目录

```bash
mkdir 目录名
```

常用参数：
- `mkdir -p a/b/c`：一次性创建多层嵌套目录（p = parents），目录不存在时自动创建中间层

示例：
```bash
mkdir notes
mkdir -p project/src/utils   # 一次创建多级目录
```

**容易踩的坑**：目录已经存在时，`mkdir` 不加 `-p` 会报错；加了 `-p` 则不会报错。

---

### `touch` — 创建空文件

```bash
touch 文件名
```

示例：
```bash
touch commands.txt
touch notes/questions.txt   # 在 notes 目录下创建（notes 必须已存在）
```

**原理**：`touch` 的本职是"更新文件的时间戳"，当文件不存在时，它会顺手创建一个空文件。

---

### `cat` — 查看文件内容

```bash
cat 文件名
```

适合**短文件**（十几行以内）。

示例：
```bash
cat notes/commands.txt
cat practice/todo.txt
```

**`echo` + `>` 的配合**（本周先"用一下"，不深入）：
```bash
echo "learn terminal" > practice/todo.txt   # 写入内容（会覆盖原有内容）
cat practice/todo.txt                        # 查看写入结果
```

`>` 是**重定向**符号，把左边命令的输出写进右边的文件。这个会在 Round 02 正式学。

---

## 文件和目录的命名建议

| 规范 | 原因 |
|------|------|
| 用小写字母 | 避免大小写混淆（Linux 区分大小写） |
| 用 `-` 或 `_` 代替空格 | 带空格的文件名在命令行里需要转义，麻烦 |
| 避免特殊字符 | `!`、`#`、`&` 等有特殊含义 |

好名字示例：`commands.txt`、`my-notes.md`、`week2_lab`  
不好的名字：`my notes.txt`（有空格）、`data!.csv`（有特殊字符）

---

## 本周资源

1. **Ubuntu 官方教程 - Creating folders and files**  
   https://ubuntu.com/tutorials/command-line-for-beginners#4-creating-folders-and-files

---

## 本周完成后，你应该能回答

- [ ] `mkdir notes` 和 `mkdir -p notes/sub/deep` 有什么区别？
- [ ] `touch` 创建的文件里有内容吗？
- [ ] `cat` 适合看很长的文件吗？为什么？
- [ ] `echo "hello" > file.txt` 做了什么事？

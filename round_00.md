# Round 00 · Terminal 初见与学习系统搭建

> **定位**：这不是正式学 Linux，也不是学编程。只解决一件事：先把学习系统搭起来，第一次对终端产生"我能用它做点事"的感觉。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | Terminal 初见 + 最小命令行实践 |
| **难度** | ⭐☆☆☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | 无 |
| **下一轮** | Round 01 · 文件系统与基础命令 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 知道 Terminal 是应用，shell 是里面接收命令的文本环境
- [ ] 会打开终端（Launchpad 或 `/Applications/Utilities`）
- [ ] 会用 `pwd`、`ls`、`cd`、`mkdir`、`touch`、`cat`、`man`
- [ ] 有一个自己的练习目录 `~/cli-lab/round0`
- [ ] 有一份自己写的命令小抄

---

## 本轮不学什么

> 先不碰：Git、管道和重定向、shell 脚本、权限细节、sudo

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 🎬 主视频 | [MIT Missing Semester – Lecture 1: Shell](https://missing.csail.mit.edu/2020/course-shell/) | 建立整体感觉，只看第一讲 |
| 📄 主文档 | [Apple – Get started with Terminal](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac) | macOS 主文档，直接演示 `ls`、`man` |
| 📖 练习主线 | [Ubuntu – The Linux command line for beginners](https://ubuntu.com/tutorials/command-line-for-beginners) | 零基础友好，难度 1/5 |
| 🗺️ 轻量补充 | [Linux Journey – File System Navigation](https://linuxjourney.com/lesson/the-filesystem) | 分块小、压力低 |

---

## 3 周学习安排

### 第 1 周：先把终端打开，建立感觉

**目标**：不怕黑窗口。

**本周练这些命令**：`pwd` · `ls` · `cd`

**任务**：
1. 看 Missing Semester 第一讲前半段
2. 看 Apple Terminal 入门页前半段
3. 完成下方「第 1 周练习」

**第 1 周自测**（不看命令，独立完成）：
1. 回到 `~/cli-lab/round0`
2. 进入 `notes`
3. 回上一级
4. 进入 `practice`
5. 回到 `~/cli-lab/round0`

---

### 第 2 周：开始自己创建东西

**目标**：第一次在终端里自己建出目录和文件。

**本周练这些命令**：`mkdir` · `touch` · `cat`

**任务**：
1. 跟着 Ubuntu 教程做「Creating folders and files」
2. 完成下方「第 2 周练习」

**第 2 周自测**：
1. 在 `~/cli-lab/round0` 下创建 `week2_test`
2. 在里面创建 `a.txt` 和 `b.txt`
3. 用 `cat` 看其中一个文件
4. 在 `notes/commands.txt` 里手动记下今天学会的命令

---

### 第 3 周：学会自查，不靠死记

**目标**：不会时先查，而不是背参数。

**本周练这些命令**：`man`

**任务**：
1. 查 `man ls`，只做三件事：看简介 → 找一个参数 → 按 `q` 退出
2. 依次查 `man pwd`、`man mkdir`、`man touch`、`man cat`
3. 试试 `man man`

**第 3 周自测**：
1. 打开 `man ls`，找到这页讲什么，退出
2. 打开 `man mkdir`，退出

---

## 本轮练习清单

### 准备工作

打开终端，创建总练习目录：

```bash
mkdir -p ~/cli-lab/round0
cd ~/cli-lab/round0
pwd
ls
```

---

### 第 1 周练习

**练习 1**：认识当前位置
```bash
cd ~/cli-lab/round0
pwd
ls
```

**练习 2**：创建子目录并切换
```bash
mkdir notes
mkdir practice
ls
cd notes
pwd
cd ..
pwd
cd practice
pwd
cd ~/cli-lab/round0
pwd
```

**练习 3**：绝对路径 vs 相对路径
```bash
cd ~/cli-lab/round0/notes
pwd
cd ..
pwd
cd ~/cli-lab/round0/practice
pwd
cd ../notes
pwd
cd ~/cli-lab/round0
pwd
```

---

### 第 2 周练习

**练习 4**：创建更多子目录
```bash
cd ~/cli-lab/round0
mkdir logs
mkdir drafts
mkdir tmp
ls
```

**练习 5**：创建空文件
```bash
touch notes/commands.txt
touch notes/questions.txt
touch practice/todo.txt
ls notes
ls practice
```

**练习 6**：查看空文件
```bash
cat practice/todo.txt
```

**练习 7**：写入内容再查看
```bash
echo "practice pwd ls cd" > practice/todo.txt
cat practice/todo.txt
```

---

### 第 3 周练习

**练习 8**：查 `man ls`
```bash
man ls
# 看最上面的简介，按 q 退出
```

**练习 9**：练习查多个命令
```bash
man pwd
man mkdir
man touch
man cat
```

**练习 10**：查 `man man`
```bash
man man
# 按 q 退出
```

---

### 综合练习

```bash
cd ~/cli-lab/round0
pwd
ls
mkdir week0_lab
cd week0_lab
mkdir notes
mkdir practice
touch notes/commands.txt
touch practice/todo.txt
echo "learn terminal basics" > practice/todo.txt
cat practice/todo.txt
man ls
```

---

## 你的命令小抄模板

在 `~/cli-lab/round0/notes/commands.txt` 里，用最土的话写下每个命令：

```
pwd：看我现在在哪
ls：看这里有什么
cd：切换目录
mkdir：创建目录
touch：创建空文件
cat：把文件内容显示出来
man：查命令说明
```

---

## 验收标准

- [ ] 知道 Terminal 是应用，shell 是里面接收命令的文本环境
- [ ] 会用 `pwd`、`ls`、`cd`
- [ ] 会用 `mkdir`、`touch`、`cat`
- [ ] 会用 `man`
- [ ] 有自己的练习目录和命令小抄

---

## ⚠️ 最容易踩的坑

1. **只看不敲** — Ubuntu 教程和 Apple 指南都是边做边看的设计，一定要手敲
2. **一次看太多** — Missing Semester 自己说课程比较密，这轮只看第一讲就够
3. **急着学高级命令** — 现在把这 7 个命令练顺比扩充命令数量更重要

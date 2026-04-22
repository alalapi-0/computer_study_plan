# Round 02 · Shell、管道、Git 最小工作流

> **定位**：先建立两个直觉：把几个小命令串起来干活；把自己的改动留下一份可追溯的历史。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 重定向 + 管道 + 最小 shell 脚本 + Git 最小闭环 |
| **难度** | ⭐⭐☆☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 01 |
| **下一轮** | Round 03 · Python 基础补强 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能解释 `>`（覆盖写入）、`>>`（追加）、`|`（管道）的区别
- [ ] 能写出 `sort xxx | uniq` 和 `grep "xxx" file | wc -l` 这种简单流水线
- [ ] 能跑一个最简单的 `.sh` 脚本
- [ ] 能完成 Git 最小闭环：`git init` → `git status` → `git add` → `git commit` → `git log`
- [ ] 做出一个小型文本过滤实验 + 一个有 2-3 次提交的小仓库

---

## 本轮命令/工具清单

```
echo  >  >>  |  grep  wc  sort  uniq  bash  
git init  git status  git add  git commit  git log
```

**本轮先不学**：`if/for/while`、`sed/awk`、`find/xargs`、Git 分支冲突、rebase、stash

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 🎬 主视频 1 | [MIT Missing Semester – Lecture 2: Shell Tools and Scripting](https://missing.csail.mit.edu/2020/shell-tools/) | 这轮主线视频，讲 bash 脚本基础和 shell tools |
| 🎬 主视频 2 | [MIT Missing Semester – Lecture 6: Version Control (Git)](https://missing.csail.mit.edu/2020/version-control/) | Git 讲次，先讲数据模型再讲命令 |
| 📄 主文档 1 | [GNU Bash Manual – Redirections/Pipelines](https://www.gnu.org/software/bash/manual/bash.html#Redirections) | 权威定义，当字典查 |
| 📄 主文档 2 | [Pro Git – 第 1、2 章](https://git-scm.com/book/zh/v2) | 官方免费书，前两章是必读 |
| 🛠️ 操作文档 | [GitHub Docs – Set up Git](https://docs.github.com/en/get-started/getting-started-with-git/set-up-git) | 最小起步：安装 + 配置用户名邮箱 |
| 🎮 交互练习 | [Learn Git Branching](https://learngitbranching.js.org/) | 浏览器里的 Git 游戏，反馈快 |

---

## 3 周学习安排

### 第 1 周：重定向和管道

**目标**：理解三件事：`>`、`>>`、`|` 在干什么。

**本周只练这些命令**：`echo`、`cat`、`>`、`>>`、`|`、`grep`、`wc`、`sort`、`uniq`

**第 1 周自测**：能不能独立写出一条「日志统计链」，并自己讲清楚 `cat` 在干什么、`grep` 在干什么、`wc -l` 在干什么。

---

### 第 2 周：最小 shell 脚本

**目标**：脚本就是把你本来要手敲的一串命令，保存成可重复执行的文件。

**本周要跑通三个脚本**：`count_errors.sh`、`count_labels.sh`、`show_args.sh`

**第 2 周自测**：能总结一句：重定向解决什么问题？脚本比手敲命令多了什么价值？

---

### 第 3 周：Git 最小工作流

**目标**：建立一个完整闭环：初始化仓库 → 看状态 → 暂存 → 提交 → 看历史。

**本周关键理解**：Git 记录的不是"最终文件夹长什么样"，而是"一连串可追溯的快照"。

**第 3 周自测**：能独立完成 `git init` → `git add` → `git commit` → `git log --oneline`，并看懂 `git status` 在说什么。

---

## 本轮练习清单

### 准备工作

```bash
mkdir -p ~/cli-lab/round2
cd ~/cli-lab/round2
mkdir week1 week2 week3
```

---

### 第 1 周练习

**练习 1**：认识 `>` 和 `>>`
```bash
cd ~/cli-lab/round2/week1
echo "apple" > fruits.txt
cat fruits.txt
echo "banana" >> fruits.txt
cat fruits.txt
echo "orange" >> fruits.txt
cat fruits.txt
```

**练习 2**：刻意感受覆盖（⚠️ `>` 会静默覆盖原文件）
```bash
echo "new line" > fruits.txt
cat fruits.txt
# 现在只剩一行了
```

**练习 3**：造重复数据
```bash
echo "cat" > animals.txt
echo "dog" >> animals.txt
echo "cat" >> animals.txt
echo "bird" >> animals.txt
echo "dog" >> animals.txt
echo "cat" >> animals.txt
cat animals.txt
```

**练习 4**：练 `sort`、`uniq`、`wc`
```bash
sort animals.txt
sort animals.txt | uniq
sort animals.txt | uniq | wc -l
```

**练习 5**：练 `grep`
```bash
echo "error: login failed" > app.log
echo "info: job started" >> app.log
echo "error: file missing" >> app.log
echo "info: job finished" >> app.log
cat app.log
grep "error" app.log
cat app.log | grep "error"
cat app.log | grep "info" | wc -l
```

---

### 第 2 周练习

**练习 6**：你的第一个脚本
```bash
cd ~/cli-lab/round2/week2
echo "error: login failed" > app.log
echo "info: job started" >> app.log
echo "error: file missing" >> app.log
echo "info: job finished" >> app.log
touch count_errors.sh
```

在 `count_errors.sh` 里写入：
```bash
#!/bin/bash
cat app.log | grep "error" | wc -l > error_count.txt
cat error_count.txt
```

运行：
```bash
bash count_errors.sh
# 如果输出 2，说明你完成了一个最小可重复脚本
```

**练习 7**：标签去重脚本
```bash
echo "ok" > labels.txt
echo "blur" >> labels.txt
echo "ok" >> labels.txt
echo "bad" >> labels.txt
echo "blur" >> labels.txt
echo "ok" >> labels.txt
touch count_labels.sh
```

在 `count_labels.sh` 里写入：
```bash
#!/bin/bash
sort labels.txt | uniq > unique_labels.txt
cat unique_labels.txt
```

运行：
```bash
bash count_labels.sh
```

**练习 8**：传参脚本
```bash
touch show_args.sh
```

在 `show_args.sh` 里写入：
```bash
#!/bin/bash
echo "script name: $0"
echo "first arg: $1"
echo "second arg: $2"
echo "all args: $@"
echo "arg count: $#"
```

运行：
```bash
bash show_args.sh aaa bbb ccc
```

**练习 9**：最简单条件判断
```bash
touch check_file.sh
```

在 `check_file.sh` 里写入：
```bash
#!/bin/bash
if grep "error" app.log > /dev/null 2> /dev/null
then
  echo "has error"
else
  echo "no error"
fi
```

运行：
```bash
bash check_file.sh
```

---

### 第 3 周练习

**准备**：配置 Git 身份（只需做一次）
```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
git config --global user.name
git config --global user.email
```

**练习 10**：初始化仓库
```bash
cd ~/cli-lab/round2/week3
mkdir git_lab
cd git_lab
git init
git status
```

**练习 11**：第一次提交（观察三个状态变化：untracked → staged → committed）
```bash
echo "# round2 git lab" > README.md
git status
git add README.md
git status
git commit -m "init repository"
git log --oneline
```

**练习 12**：第二次提交
```bash
echo "this repo is for round2 practice" >> README.md
git status
git diff
git add README.md
git commit -m "update readme"
git log --oneline
```

**练习 13**：再加一个文件
```bash
echo "pipeline practice notes" > notes.txt
git status
git add notes.txt
git commit -m "add notes"
git log --oneline
```

---

### 综合项目 A：迷你日志统计器

```bash
mkdir -p ~/cli-lab/round2/final_pipeline_lab
cd ~/cli-lab/round2/final_pipeline_lab
echo "error: login failed" > app.log
echo "info: job started" >> app.log
echo "warning: timeout" >> app.log
echo "error: file missing" >> app.log
echo "info: job finished" >> app.log
cat app.log | grep "error" > errors_only.txt
cat app.log | grep "info" > info_only.txt
cat app.log | grep "error" | wc -l > error_count.txt
cat error_count.txt
```

> 意义：你已经开始在做"从原始文本中过滤出我关心的信息"这件事了。

### 综合项目 B：迷你 Git 仓库

```bash
mkdir -p ~/cli-lab/round2/final_git_lab
cd ~/cli-lab/round2/final_git_lab
git init
echo "# final git lab" > README.md
git add README.md
git commit -m "init"
echo "round2 practice repo" >> README.md
git add README.md
git commit -m "add description"
echo "todo: learn git branch later" > todo.txt
git add todo.txt
git commit -m "add todo"
git log --oneline
git status
```

> 意义：你第一次拥有了一个有历史的项目目录。

---

## 验收标准

- [ ] 能解释 `>`、`>>`、`|` 的区别
- [ ] 能独立写一条 `grep | wc -l` 处理链
- [ ] 能写一个最小 `.sh` 文件并用 `bash xxx.sh` 执行
- [ ] 能说出 `$1`、`$@`、`$#` 大概是什么意思
- [ ] 能独立完成 `git init → git add → git commit → git log`
- [ ] 能看懂 `git status` 在说什么

---

## ⚠️ 最容易踩的坑

1. **把 `>` 当成"总是安全的写文件"** — 它会覆盖原文件内容，不是追加
2. **只会手敲命令，不会把命令存成脚本** — 脚本让命令链可以重复执行
3. **太早陷进 Git 高级概念** — 现在先理解"Git 记录快照历史"，把最小工作流跑通，不要学 rebase 和复杂分支

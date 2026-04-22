# Round 01 · 文件系统与基础命令

> **定位**：不是学 Linux 全家桶。只解决一件事：在命令行里不慌，能自己找文件、建目录、看文件、移动文件、删测试文件、查帮助。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 文件系统 + 基础 13 命令 |
| **难度** | ⭐☆☆☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 00 |
| **下一轮** | Round 02 · Shell、管道、Git 最小工作流 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能说清 Terminal 是应用，shell 是文本接口
- [ ] 能独立完成创建目录、创建文件、复制、移动、改名、删除测试文件
- [ ] 能用 `cat`、`less`、`head`、`tail` 看文本文件
- [ ] 知道不会时先查 `man`
- [ ] 已经留下一份自己的命令小抄

---

## 本轮命令清单

```
pwd  ls  cd  mkdir  touch  cp  mv  rm  cat  less  head  tail  man
```

**本轮先不学**：`chmod`、`sudo`、Git、管道、shell 脚本

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 🎬 主视频 | [MIT Missing Semester – Lecture 1: Shell](https://missing.csail.mit.edu/2020/course-shell/) | 建立"为什么还要学命令行"的整体感觉 |
| 📄 主文档 | [Apple – Get started with Terminal](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac) | macOS 主文档，直接演示 `ls`、`man` |
| 📖 练习主线 | [Ubuntu – The Linux command line for beginners](https://ubuntu.com/tutorials/command-line-for-beginners) | 零基础，创建文件/移动文件为主线 |
| 🗺️ 补充 | [Linux Journey – File System Navigation](https://linuxjourney.com/lesson/the-filesystem) | 分块小，专注 `ls`、`cd`、`pwd` |
| 📚 参考 | [jlevy/the-art-of-command-line](https://github.com/jlevy/the-art-of-command-line) | 学完基础后的补充小抄，不是主教材 |

---

## 3 周学习安排

### 第 1 周：路径感

**目标**：搞清楚"我现在在哪、这里有什么、我要怎么去别处"。

**本周主练**：`pwd` · `ls` · `cd`

**建议安排**：
- 2 小时看主视频前半段，建立 shell / terminal / path 的概念
- 2 小时看 Apple Terminal 入门页并跟着敲 `ls`、`man`
- 4 小时做路径切换练习

**本周你要真正分清**：
- 当前目录
- 绝对路径
- 相对路径
- `.` 和 `..`

**第 1 周自测**（不看命令，独立完成）：
1. 回到 `~/cli-lab/round1`
2. 进入 `notes`
3. 回上一级
4. 进入 `practice`
5. 进入 `test`
6. 回到 `~/cli-lab/round1`

---

### 第 2 周：文件操作

**目标**：把"建、看、搬、改、删"练顺。

**本周主练**：`mkdir` · `touch` · `cp` · `mv` · `rm`

**建议安排**：
- 2 小时跟着 Ubuntu 教程做创建和移动文件练习
- 3 小时自己重复做目录与文件操作
- 3 小时做一轮综合整理练习

**第 2 周自测**（不看命令，独立完成）：
1. 在 `~/cli-lab/round1` 下创建 `week2_test`
2. 进入该目录
3. 创建 `input`、`output`、`backup`
4. 创建 `x.txt`、`y.txt`
5. 复制 `x.txt` 到 `backup`
6. 把 `y.txt` 改名成 `result.txt`
7. 删除一个你自己创建的测试文件

---

### 第 3 周：看文件和自查

**目标**：建立"不会就查"的习惯，而不是背参数。

**本周主练**：`cat` · `less` · `head` · `tail` · `man`

**建议安排**：
- 2 小时练短文件和长文件查看
- 2 小时练文件开头和结尾查看
- 4 小时做综合小任务并整理自己的命令小抄

---

## 本轮练习清单

### 准备工作

```bash
mkdir -p ~/cli-lab/round1
cd ~/cli-lab/round1
pwd
ls
```

---

### 第 1 周练习

**练习 1**：认识当前位置
```bash
cd ~/cli-lab/round1
pwd
ls
```

**练习 2**：创建目录并来回切换
```bash
mkdir notes
mkdir practice
mkdir test
ls
cd notes
pwd
cd ..
pwd
cd practice
pwd
cd ../test
pwd
cd ~/cli-lab/round1
pwd
```

**练习 3**：绝对路径 vs 相对路径
```bash
cd ~/cli-lab/round1/notes
pwd
cd ..
pwd
cd ~/cli-lab/round1/practice
pwd
cd ../test
pwd
cd ~/cli-lab/round1
pwd
```

---

### 第 2 周练习

**练习 4**：搭一个小目录结构
```bash
cd ~/cli-lab/round1
mkdir week2
cd week2
mkdir raw_data backup archive
ls
```

**练习 5**：创建测试文件
```bash
touch a.txt
touch b.txt
touch c.txt
ls
```

**练习 6**：复制文件
```bash
cp a.txt backup/
ls
ls backup
# 观察：当前目录里的 a.txt 还在，backup/ 里也多了一份
```

**练习 7**：移动文件
```bash
mv c.txt archive/
ls
ls archive
# 观察：当前目录里的 c.txt 没了，archive/ 里有了 c.txt
```

**练习 8**：改名
```bash
mv b.txt notes.txt
ls
# 观察：b.txt 变成了 notes.txt
```

**练习 9**：复制并改名
```bash
cp notes.txt backup/notes_copy.txt
ls backup
```

**练习 10**：删除测试文件
```bash
touch delete_me.txt
ls
rm delete_me.txt
ls
# 只在练习目录里做，不要碰真实资料文件
```

**练习 11**：删除子目录中的文件
```bash
touch archive/temp.txt
ls archive
rm archive/temp.txt
ls archive
```

---

### 第 3 周练习

**练习 12**：准备一个文本文件
```bash
cd ~/cli-lab/round1
mkdir week3
cd week3
touch study_log.txt
echo "day1 linux practice" >> study_log.txt
echo "day2 learned pwd ls cd" >> study_log.txt
echo "day3 learned mkdir touch" >> study_log.txt
echo "day4 learned cp mv rm" >> study_log.txt
echo "day5 learned cat" >> study_log.txt
echo "day6 learned less" >> study_log.txt
echo "day7 learned head tail" >> study_log.txt
echo "day8 reviewed paths" >> study_log.txt
echo "day9 reviewed files" >> study_log.txt
echo "day10 reviewed commands" >> study_log.txt
```

**练习 13**：用 `cat` 看文件（适合短文件）
```bash
cat study_log.txt
```

**练习 14**：用 `less` 看文件
```bash
less study_log.txt
# 用方向键上下看，按 q 退出
```

**练习 15**：只看开头
```bash
head study_log.txt
head -n 3 study_log.txt
```

**练习 16**：只看结尾
```bash
tail study_log.txt
tail -n 4 study_log.txt
```

**练习 17**：查帮助（每次只做三件事：看简介 → 找一两个参数 → 按 q 退出）
```bash
man ls
man cp
man mv
man rm
man cat
man less
```

---

### 综合练习：迷你文件整理实验室

```bash
# 第一步：创建目录结构
cd ~/cli-lab/round1
mkdir study_files_lab
cd study_files_lab
mkdir input output backup notes
ls

# 第二步：创建测试文件
touch input/raw1.txt
touch input/raw2.txt
touch input/raw3.txt
ls input

# 第三步：复制、移动、改名
cp input/raw1.txt backup/
mv input/raw2.txt output/
mv input/raw3.txt input/final_raw3.txt
ls input
ls output
ls backup

# 第四步：写一份命令笔记
touch notes/round1_notes.txt
echo "pwd: 查看当前路径" >> notes/round1_notes.txt
echo "ls: 查看当前目录内容" >> notes/round1_notes.txt
echo "cd: 切换目录" >> notes/round1_notes.txt
echo "mkdir: 创建目录" >> notes/round1_notes.txt
echo "touch: 创建空文件" >> notes/round1_notes.txt
echo "cp: 复制文件" >> notes/round1_notes.txt
echo "mv: 移动文件或改名" >> notes/round1_notes.txt
echo "rm: 删除文件" >> notes/round1_notes.txt
echo "cat: 查看短文件" >> notes/round1_notes.txt
echo "less: 查看长文件" >> notes/round1_notes.txt
echo "head: 看文件开头" >> notes/round1_notes.txt
echo "tail: 看文件结尾" >> notes/round1_notes.txt
cat notes/round1_notes.txt
```

> 这个目录结构模拟了 AI 项目最常见的组织方式：`input` 放原始数据，`output` 放结果，`backup` 放备份，`notes` 留说明。

---

## 验收标准

- [ ] 能解释什么是当前目录、绝对路径、相对路径
- [ ] 能独立完成创建目录、创建文件、复制、移动、改名、删除测试文件
- [ ] 能用 `cat`、`less`、`head`、`tail` 看文本文件
- [ ] 知道不会时先用 `man`
- [ ] 已经有一份自己的命令小抄

---

## ⚠️ 最容易踩的坑

1. **只看视频不动手** — Missing Semester 自己说课程偏密，视频只能当引导，真正的掌握要靠练
2. **把 `man` 当教材整本读** — Ubuntu 官方说 man page 更适合当快速参考，不是完整学习材料
3. **太早去看命令行大全** — `the-art-of-command-line` 很好，但这轮最多拿来做补充

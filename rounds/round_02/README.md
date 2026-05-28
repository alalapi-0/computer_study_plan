# Round 02 · 学习目录

这个目录是 Round 02（Shell、管道、Git 最小工作流）的展开内容。

> **仓库根**（进度、`mark_done.sh`）：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**（手敲命令）：`~/cli-lab/round2`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_02/
├─ README.md
├─ week1/
│  ├─ notes.md
│  └─ exercises.sh
├─ week2/
│  ├─ notes.md
│  └─ exercises.sh
├─ week3/
│  ├─ notes.md
│  └─ exercises.sh
└─ final/
   ├─ comprehensive_exercise.sh
   └─ command_cheatsheet.md
```

## 使用方式

1. 每周先阅读 `weekN/notes.md`，再执行 `weekN/exercises.sh`。
2. 脚本会自动调用 `mark_done.sh` 标记自动任务。
3. 阅读任务请手动打卡，例如：`bash mark_done.sh r02-w1-read`。

## 进度追踪

```bash
cd ~/PycharmProjects/computer_study_plan
bash mark_done.sh
open progress.html
```

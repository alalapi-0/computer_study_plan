# Round 00 · 学习目录

这个目录是 Round 00（Terminal 初见）的展开内容。

> **仓库根**（进度、`mark_done.sh`）：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**（手敲命令）：`~/cli-lab/round0`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_00/
├─ README.md                    ← 本文件：目录说明
├─ week1/
│  ├─ notes.md                  ← 第1周学习笔记（pwd/ls/cd）
│  └─ exercises.sh              ← 第1周练习脚本
├─ week2/
│  ├─ notes.md                  ← 第2周学习笔记（mkdir/touch/cat）
│  └─ exercises.sh              ← 第2周练习脚本
├─ week3/
│  ├─ notes.md                  ← 第3周学习笔记（man）
│  └─ exercises.sh              ← 第3周练习脚本
└─ final/
   ├─ comprehensive_exercise.sh ← 综合练习脚本
   └─ command_cheatsheet.md     ← 命令小抄模板
```

## 使用方式

1. 每周开始前先阅读 `weekN/notes.md`
2. 再打开 Terminal，对照 `weekN/exercises.sh` 手敲每个命令
3. 完成后在 `progress.html` 里勾选对应任务

## 进度追踪

在仓库根目录打开 `progress.html`：

```bash
cd ~/PycharmProjects/computer_study_plan
open progress.html   # 或：python3 -m http.server 8000 后浏览器访问
```

练习脚本会自动定位仓库根并调用 `mark_done.sh`，无需在 `~/cli-lab` 下执行打卡命令。

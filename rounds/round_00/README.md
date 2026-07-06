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

1. 在仓库根启动本地 Web UI。
2. 打开 Round 00，点击「读教程」阅读 `weekN/notes.md`。
3. 工程任务会自动联动 `~/cli-lab/round0` 终端；按教程手敲命令。
4. 完成一个最小动作后点击「记录并完成」，在弹窗里写下本次记录后保存。

## 进度追踪

在仓库根目录启动本地服务并打开看板：

```bash
cd ~/PycharmProjects/computer_study_plan
python3 scripts/progress_server.py
open http://127.0.0.1:8777/progress.html?round=round_00
```

练习脚本会自动定位仓库根并调用 `mark_done.sh`；阅读、自测、小抄和验收类任务仍以 Web UI 的「记录并完成」为准。

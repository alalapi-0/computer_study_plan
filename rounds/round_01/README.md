# Round 01 · 文件系统与基础命令

这个目录是 Round 01（文件系统与基础命令）的 Web UI 可练习版本。用户可以在 `http://127.0.0.1:8777/progress.html?round=round_01` 中阅读任务、运行练习脚本、使用“终端练习”敲命令，并在完成阅读 / 自测 / 产出后通过页面按钮记录进度。

> **仓库根**（进度、`mark_done.sh`）：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**（手敲命令）：`~/cli-lab/round1`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_01/
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

## Web UI 使用方式

1. 打开本仓库的本地 Web UI，选择 `Round 01 · 文件系统与基础命令`。
2. 先读每周 `notes.md`，确认理解后点击“记录并完成”保存阅读记录。
3. 对练习任务点击页面中的“运行脚本”按钮，脚本会在 `~/cli-lab/round1` 沙盒中准备材料并记录对应练习任务。
4. 对自测任务，使用页面里的“终端练习”手敲命令；确认自己不看提示也能完成后，再点击「记录并完成」。
5. 最终验收里，综合脚本只记录“综合练习”；命令小抄和口头验收仍需要用户理解后点击“记录并完成”保存。

## 终端练习边界

- “终端练习”默认映射到 `~/cli-lab`，Round 01 的主要目录是 `~/cli-lab/round1`。
- 可以练习 `pwd`、`ls`、`cd`、`mkdir`、`touch`、`cp`、`mv`、`rm`、`cat`、`less`、`head`、`tail`、`man` 等基础动作。
- `rm` 只用于删除沙盒内普通测试文件；不要练递归删除、强制删除或删除真实资料。

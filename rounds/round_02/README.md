# Round 02 · 学习目录

这个目录是 Round 02（Shell、管道、Git 最小工作流）的 Web UI 可练习版本。用户可以在 `http://127.0.0.1:8777/progress.html?round=round_02` 中阅读任务、运行受控练习脚本、使用“终端练习”完成管道 / 脚本 / Git 本地练习，并在自测后通过页面按钮记录进度。

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

## Web UI 使用方式

1. 打开本仓库的本地 Web UI，选择 `Round 02 · Shell、管道、Git 最小工作流`。
2. 先读每周 `notes.md`，确认理解后点击“记录并完成”保存阅读记录。
3. 对练习任务点击页面中的“运行脚本”按钮，脚本会在 `~/cli-lab/round2` 下的自动练习目录中准备材料并记录对应练习任务。
4. 对自测任务，使用页面里的“终端练习”手敲命令；确认自己能解释输出后，再点击「记录并完成」。
5. 最终验收里，综合脚本只记录 `r02-fin-comp`；命令小抄和验收项仍需要用户理解后点击“记录并完成”保存。

## 终端练习边界

- “终端练习”默认映射到 `~/cli-lab`，Round 02 的主要目录是 `~/cli-lab/round2`。
- 可以练习 `echo`、`cat`、`grep`、`wc`、`sort`、`uniq`、`bash`、`git init/status/add/commit/log/diff`、重定向和管道。
- 浏览器终端不允许 `;`、`&&`、`||` 这类命令串联；需要把每一步拆成一条命令。
- Git 只练本地仓库，不做 `clone`、`pull`、`push`、`remote` 或任何远程操作。

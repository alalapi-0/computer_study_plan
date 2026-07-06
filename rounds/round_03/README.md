# Round 03 · Python 基础与复杂度入门

这个目录是 Round 03 的 Web UI 可学习版本，聚焦 Python 基础语法、list/dict、函数拆分和复杂度直觉。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round3`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_03/
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
   └─ complexity_cheatsheet.md
```

## 使用方式

1. 用 `python3 scripts/progress_server.py` 启动 Web UI。
2. 打开 `http://127.0.0.1:8777/progress.html?round=round_03`。
3. 每周先点“读教程”阅读 `notes.md`。
4. 对 `exercise` 类型任务点“运行脚本”，脚本会在 `~/cli-lab/round3/*_auto` 生成示例代码并自动记录对应练习任务。
5. 对“自测 / 产出 / 验收”任务点“终端练习”或“记录并完成”，自己在浏览器映射终端中写代码、运行、解释，再点击“记录并完成”。

## 终端边界

- Web UI “终端练习”映射到 `~/cli-lab`，点任务行“终端练习”会自动切到 `~/cli-lab/round3`。
- 可以在终端里运行 `python3 xxx.py`、`cat`、`grep`、`wc`、`ls` 等白名单命令。
- 命令历史会写入 `records/terminal/commands.jsonl`，但“执行过命令”不等于“任务完成”。
- 自测与验收必须由你理解后点击“记录并完成”，脚本不会替你打卡。

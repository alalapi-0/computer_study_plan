# Round 07 · 面向 AI 项目的综合练习

这个目录是 Round 07（pathlib、多格式读写、argparse、logging、小工具整合）的 Web UI 可练习版本。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round7`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_07/
├─ README.md
├─ week1/
│  ├─ notes.md
│  └─ exercises.py
├─ week2/
│  ├─ notes.md
│  └─ exercises.py
├─ week3/
│  ├─ notes.md
│  └─ exercises.py
└─ final/
   ├─ comprehensive_exercise.py
   └─ ai_prep_tool_cheatsheet.md
```

## 使用方式

### 推荐：只通过 Web UI 完成

1. 在仓库根启动本地服务：

   ```bash
   python3 scripts/progress_server.py
   ```

2. 浏览器打开 `http://127.0.0.1:8777/progress.html?round=round_07`。
3. 在 Round 07 任务列表里按顺序完成：
   - 阅读任务：点“读教程”，直接在页面中读 `notes.md`、脚本和 `round_07.md`。
   - 自动练习：点“运行脚本”，脚本会在 `~/cli-lab/round7/*_auto` 生成演示数据、输出结果、写日志并自动记录对应练习完成。
   - 自测任务：点“终端练习”，在浏览器映射终端中自己创建文件、运行脚本；确认理解后再点击“记录并完成”。
   - 小抄与验收：读 `final/ai_prep_tool_cheatsheet.md`，能解释后再点击“记录并完成”保存记录。

### 命令行备用

仍可在仓库根直接运行：

```bash
python3 rounds/round_07/week1/exercises.py
python3 rounds/round_07/week2/exercises.py
python3 rounds/round_07/week3/exercises.py
python3 rounds/round_07/final/comprehensive_exercise.py
```

这些脚本默认生成演示输入，不需要额外参数；你也可以给 Week 2 / Final 脚本传入 `--input`、`--output`、`--format`、`--dedup`。

## 完成边界

- 自动脚本只标记 `r07-w1-ex1`、`r07-w2-ex2`、`r07-w3-ex3`、`r07-fin-comp`。
- `r07-w*-self`、`r07-fin-sheet`、`r07-fin-acc1` 必须由用户通过 Web UI 阅读、手写、自测和点击“记录并完成”保存记录。
- 所有临时数据都在 `~/cli-lab/round7`，不写入仓库、也不污染 `records/` 的真实学习记录。

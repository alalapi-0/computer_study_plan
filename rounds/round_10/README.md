# Round 10 · Python 工程化基础

这个目录是 Round 10（模块拆分、配置、日志、CLI 参数、错误处理）的 Web UI 可练习版本。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round10`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_10/
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
   └─ python_engineering_cheatsheet.md
```

## 使用方式

### 推荐：只通过 Web UI 完成

1. 在仓库根启动本地服务：

   ```bash
   python3 scripts/progress_server.py
   ```

2. 浏览器打开 `http://127.0.0.1:8765/progress.html?round=round_10`。
3. 在 Round 10 任务列表里按顺序完成：
   - 阅读任务：点“打开”，直接在页面中读 `notes.md`、脚本和 `round_10.md`。
   - 自动练习：点“运行”，脚本会在 `~/cli-lab/round10/*_auto` 生成工程化小项目、配置、日志、错误处理报告和收口摘要，并自动记录对应练习完成。
   - 自测任务：点“终端”，在浏览器映射终端中自己写 `cli.py`、`config.py`、`log_utils.py` 或入口脚本；确认理解后再手动点“记录 / 完成”。
   - 小抄与验收：读 `final/python_engineering_cheatsheet.md`，能解释后再手动完成记录。

### 命令行备用

仍可在仓库根直接运行：

```bash
python3 rounds/round_10/week1/exercises.py
python3 rounds/round_10/week2/exercises.py
python3 rounds/round_10/week3/exercises.py
python3 rounds/round_10/final/comprehensive_exercise.py
```

## 完成边界

- 自动脚本只标记 `r10-w1-ex1`、`r10-w2-ex2`、`r10-w3-ex3`、`r10-fin-comp`。
- `r10-w*-self`、`r10-fin-sheet`、`r10-fin-acc1` 必须由用户通过 Web UI 阅读、手写、自测和手动记录。
- 本轮不安装第三方依赖，不切换到 `src/` layout，不做打包发布；先把职责拆分、配置、日志和错误处理跑通。

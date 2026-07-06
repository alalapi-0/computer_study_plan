# Round 12 · 自动化流水线与批处理

这个目录是 Round 12（pathlib 批量遍历、归档、定时入口与日志轮转）的 Web UI 可练习版本。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round12`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 完成路径

1. 启动本地 Web UI：
   ```bash
   python3 scripts/progress_server.py
   ```
2. 打开 `http://127.0.0.1:8777/progress.html?round=round_12`。
3. 每周按顺序完成三件事：
   - 点“读教程”查看 notes。
   - 点“运行脚本”执行对应 `exercises.py`，它会在 `~/cli-lab/round12` 下生成可检查产物。
   - 点“终端练习”进入浏览器映射终端，按 notes 的自测命令自己再写一遍最小脚本。
4. 最终验收：
   - 运行 `final/comprehensive_exercise.py`。
   - 阅读并补全 `final/pipeline_automation_cheatsheet.md`。
   - 用“记录并完成”点击“记录并完成”保存小抄和口头解释类任务。

## 安全边界

- 自动脚本只写入 `~/cli-lab/round12`，不写入仓库练习产物。
- 本轮会生成 `cron` / `nohup` / `tmux` 示例文本，但不会修改系统 crontab，也不会启动真实后台任务。
- 浏览器终端仍然只允许安全白名单命令；`ssh`、`scp`、`rsync`、网络命令和高风险系统操作会被拦截。
- 自动脚本只标记对应练习任务：`r12-w1-ex1`、`r12-w2-ex2`、`r12-w3-ex3`、`r12-fin-comp`。自测、小抄、验收需要用户自己完成后点击“记录并完成”保存记录。

## 目录结构

```
round_12/
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
   └─ pipeline_automation_cheatsheet.md
```

## 每周产物

- Week 1：`week1_auto/batch_pipeline/`，包含输入文件、批处理输出、`failures.log` 和 `batch_report.json`。
- Week 2：`week2_auto/archive_pipeline/`，包含 subprocess 报告和 zip 归档。
- Week 3：`week3_auto/scheduled_pipeline/`，包含 `log_utils.py`、`scripts/run_batch.sh`、cron/nohup/tmux 示例和轮转日志。
- Final：`final_auto/ai_prep_tool/`，包含一个完整的小型批处理流水线、归档和 `round12_summary.json`。

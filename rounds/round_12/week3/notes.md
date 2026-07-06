# Round 12 · Week 3 笔记（日志轮转与定时入口）

## Web UI 学习路径

1. 先阅读本文件，记住本周只做“本地自动化排练”：写脚本、写示例、验证日志轮转，不写系统 crontab。
2. 点“运行脚本”执行 `week3/exercises.py`。脚本会生成 `log_utils.py`、`scripts/run_batch.sh`、`cron_example.txt`、`nohup_tmux_notes.txt` 和轮转日志。
3. 点击“终端练习”，自己写一个小的 logging demo，观察日志文件出现。
4. 用“记录并完成”写下：cron、nohup、tmux 分别解决什么问题。

## 本周目标

- 用 `RotatingFileHandler` 防止日志无限增长。
- 生成一个可被 cron 调用的 `scripts/run_batch.sh`。
- 写出 cron/nohup/tmux 示例，但不真正启用。
- 理解“定时入口”和“长任务保活”的差别。

## 安全边界

- 本仓库非远程部署项目，本周不写入系统 crontab。
- 浏览器终端不允许直接执行 `nohup` / `tmux` / `crontab`；你只需要把示例写进文本文件并能解释。
- 真实启用定时任务前，必须先确认路径、日志、权限和停止方案。

## 浏览器终端自测

在 Round 12 页面点本周自测的“终端练习”，运行：

```bash
mkdir -p log_self
printf 'import logging\nfrom logging.handlers import RotatingFileHandler\nfrom pathlib import Path\nPath("log_self/logs").mkdir(parents=True, exist_ok=True)\nhandler=RotatingFileHandler("log_self/logs/app.log", maxBytes=200, backupCount=2, encoding="utf-8")\nlogger=logging.getLogger("demo")\nlogger.setLevel(logging.INFO)\nlogger.addHandler(handler)\nfor i in range(20):\n    logger.info("line %s %s", i, "x"*20)\nprint("done")\n' > log_self/log_demo.py
python3 log_self/log_demo.py
find log_self/logs -type f | sort
```

看到 `app.log` 和可能的轮转文件后，再手动标记 `r12-w3-self`。

## 本周自查

- [ ] 能说明日志轮转为什么能防止磁盘被单个日志撑爆。
- [ ] 能写出一条 crontab 示例（不必真写入系统 crontab）。
- [ ] 能解释 `nohup` 和 `tmux` 都是保活工具，但使用场景不同。

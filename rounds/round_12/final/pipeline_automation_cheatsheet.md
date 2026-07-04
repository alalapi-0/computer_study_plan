# Round 12 · 自动化流水线速查

## Web UI 完成路径

1. 在 Round 12 页面逐周点“阅读”和“运行”。
2. 每个自测任务点“终端”，自己写最小脚本，而不是只看自动脚本输出。
3. 运行最终综合练习后，查看 `~/cli-lab/round12/final_auto/ai_prep_tool/round12_summary.json`。
4. 在 Web UI 中用“记录”写下本页 5 个自问答案，再手动完成小抄和验收任务。

## 流水线顺序

1. `pathlib` 批量扫描 `input/`。
2. 单文件处理时写独立输出名，避免覆盖。
3. 每个文件单独 try/except，失败写 `failures.log`。
4. `subprocess` 包装批处理入口，记录 returncode/stdout/stderr。
5. `shutil.make_archive()` 把输出打成 zip。
6. `RotatingFileHandler` 控制日志大小。
7. `scripts/run_batch.sh` 作为 cron 可挂接入口。
8. `cron` 负责定时，`nohup` / `tmux` 负责长任务保活。

## 文件职责表

| 文件 / 目录 | 职责 |
|---|---|
| `input/` | 待处理原始文件 |
| `output/` | 当前运行生成的结果 |
| `archive/` | 可长期保存或发送的 zip 证据包 |
| `logs/` | 当前和历史运行日志 |
| `failures.log` | 本次失败文件列表和原因 |
| `batch_summary.json` | 本次批处理摘要 |
| `command_report.json` | subprocess 返回码和输出摘要 |
| `log_utils.py` | 日志轮转配置 |
| `scripts/run_batch.sh` | 定时任务入口脚本 |
| `cron_example.txt` | crontab 示例，只做排练 |
| `nohup_tmux_notes.txt` | 长任务保活命令示例，只做排练 |

## 安全边界

- 不直接写系统 crontab。
- 不在浏览器终端里启动真实 `nohup` / `tmux` 长任务。
- 不把 `output/`、`archive/`、`logs/` 当成源代码提交。
- 真实启用定时任务前，必须确认停止方式和日志位置。

## 最小通过标准

- 沙盒能批量处理多个输入文件并记录失败项。
- 存在可执行的 `run_batch.sh` 与 `log_utils.py`。
- 存在 zip 归档和轮转日志。
- 能说明 cron / nohup / tmux 在本轮中的角色。

## 最终验收自问

1. 批处理为什么要记录失败项，而不是遇到错误就整批退出？
2. `subprocess` 为什么要看 returncode？
3. `output/` 和 `archive/` 的区别是什么？
4. 日志轮转解决了什么风险？
5. cron、nohup、tmux 分别适合什么场景？

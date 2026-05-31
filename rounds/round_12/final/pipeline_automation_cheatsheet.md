# Round 12 · 自动化流水线速查

## 建议顺序

1. `pathlib` 批量扫描 `input/` 并写出 `output/`。
2. `subprocess` + `shutil` 包装批处理并归档摘要。
3. `RotatingFileHandler` + `scripts/run_batch.sh` 定时入口骨架。

## 最小通过标准

- 沙盒能批量处理多个输入文件并记录失败项。
- 存在可执行的 `run_batch.sh` 与 `log_utils.py` 骨架。
- 能说明 cron / nohup / tmux 在本轮中的角色（不必全部实装）。

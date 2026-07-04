# Round 06 · Week 2 笔记（进程管理与长任务）

## 本周目标

- 识别进程状态并完成基础控制。
- 会用 `nohup` 或 `tmux` 保护长任务不中断。

## 在 Web UI 中怎么学

1. 点“练习：进程查看与长任务日志”的“运行”，查看自动生成的 `worker.py`、`worker.log` 和 `process_snapshot.txt`。
2. 点“自测：自己写 worker_monitor.sh”的“终端”，浏览器终端会进入 `~/cli-lab/round6`。
3. 自己写一个长任务观察脚本：

```bash
mkdir week2_self
cd week2_self
printf 'import time\nprint("worker start")\ntime.sleep(2)\nprint("worker done")\n' > worker.py
python3 worker.py > worker.log &
ps aux | grep worker.py | grep -v grep
cat worker.log
```

4. 这个浏览器终端只开放只读 `ps` 查看，不开放 `kill`、真实 `nohup` 或 `tmux` 会话操作。能解释这些命令的用途后，再手动记录自测完成。

## 模式直觉

- `ps`：看到当前系统里有哪些进程。
- 后台任务：命令后加 `&`，当前 shell 很快返回。
- `nohup`：断开终端后继续跑，适合简单长任务。
- `tmux`：保留一个可重新连回去的终端会话，更适合交互式工作。

## 本周自查

- [ ] 能用 `ps` + `grep` 找到目标进程
- [ ] 能解释 `nohup` 与 `tmux` 的使用差异
- [ ] 能区分“后台运行”和“任务保活”

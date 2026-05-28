# Round 06 Linux 自动化小抄

- `find ... -print0 | xargs -0 ...`：安全处理带空格文件名。
- `sed 's/old/new/g'`：适合轻量替换；批量替换前先备份。
- `awk '{print $1}'`：常用于按列提取、统计日志字段。
- `nohup cmd > out.log 2>&1 &`：断开终端后继续运行任务。
- `tmux new -s name` / `tmux attach -t name`：会话级任务保活。
- `rsync -avz src/ dest/`：增量同步优先于重复拷贝。

# Web UI 练习终端记录

`commands.jsonl` 由 Web UI 的“练习终端”自动追加写入，用来保存浏览器沙盒终端中的命令历史。

## 边界

- 工作目录固定在 `~/cli-lab` 及其子目录内。
- 支持学习常用命令、管道、重定向、沙盒内普通文件删除、`less` / `man` 捕获输出、只读 `ps` 进程查看和本地 Git 最小工作流。
- 危险命令、远程命令、网络命令和仓库外路径会被拦截。
- 命令串联符（如 `;`、`&&`、`||`）会被拦截；需要把练习拆成多条命令执行。
- 从任务行点击“终端”后执行的命令会带上 `task_id`，方便回看命令属于哪个学习任务。
- 这些记录只说明“执行过命令”，不等同于任务完成；任务完成仍以 Web UI 的“完成 / 记录”或 `mark_done.sh` 为准。

## 字段

- `command_id`: 命令记录 ID
- `timestamp`: 执行时间
- `cwd`: 执行目录
- `command`: 用户输入的命令
- `task_id`: 关联任务 ID；没有绑定任务时为空字符串
- `result`: `ok` / `failed` / `timeout`
- `returncode`: 进程返回码
- `duration_ms`: 执行耗时
- `stdout_excerpt` / `stderr_excerpt`: 输出摘要

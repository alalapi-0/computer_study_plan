# Round 06 · Linux 进阶与自动化

这个目录是 Round 06（find/xargs、sed/awk、进程查看、长任务排练、SSH/rsync/crontab 命令排练）的 Web UI 可练习版本。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round6`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_06/
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
   └─ linux_automation_cheatsheet.md
```

## Web UI 使用方式

1. 在仓库根启动服务：`python3 scripts/progress_server.py --host 127.0.0.1 --port 8778`。
2. 浏览器打开：`http://127.0.0.1:8778/progress.html?round=round_06`。
3. 先点每周“阅读”任务的“打开”，在页面内读 notes。
4. 再点“练习”任务的“运行”，脚本会在 `~/cli-lab/round6` 下生成安全练习产物，并只标记脚本实际完成的练习任务。
5. 自测任务点“终端”，浏览器终端会绑定到 `~/cli-lab/round6`，命令历史会带上 `task_id`。
6. 自测、小抄和最终验收都需要用户自己理解后，手动点“记录 / 完成”。

## 安全边界

- Web UI 终端允许 `find`、`grep`、`sed`、`awk`、`ps` 等本地沙盒练习命令。
- `ssh`、`scp`、`rsync`、`crontab`、`kill`、真实远程操作和网络命令不会在 Web UI 终端里执行。
- Week 3 会生成远程操作命令排练文件；真实服务器练习需要另开授权边界。

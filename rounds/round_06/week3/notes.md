# Round 06 · Week 3 笔记（SSH/rsync/crontab）

## 本周目标

- 掌握最小远程连接与文件同步流程。
- 理解定时任务语法并能写出基础 cron 条目。

## 在 Web UI 中怎么学

1. 点“练习：远程同步与 cron 命令排练”的“运行脚本”，查看自动生成的 `remote_rehearsal.md` 和 `cron_examples.txt`。
2. 点“自测：自己写 remote_ops_plan.md”的“终端练习”，浏览器终端会进入 `~/cli-lab/round6`。
3. 自己写一份不执行真实远程命令的操作计划：

```bash
mkdir week3_self
cd week3_self
printf '# remote ops rehearsal\n\nssh: ssh user@host\nscp: scp app.log user@host:~/round6/\nrsync: rsync -avz ./ user@host:~/round6/\ncron: */5 * * * * bash ~/round6/healthcheck.sh\n' > remote_ops_plan.md
cat remote_ops_plan.md
```

4. Web UI 终端会拦截 `ssh`、`scp`、`rsync`、`crontab` 等真实远程或系统级命令。能解释命令结构后，再点击“记录并完成”保存自测记录。

## 安全边界

- 这里先学“命令长什么样、参数怎么读、风险在哪里”。
- 不在 Web UI 里连接真实服务器，不写真实 crontab。
- 真实 VPS 操作需要按 `docs/checklists/remote_operation_checklist.md` 另开授权流程。

## 本周自查

- [ ] 能写出一次 `ssh` + `rsync` 的最小操作链路
- [ ] 能解释 cron 的“分 时 日 月 周”五段含义
- [ ] 能说出真实远程操作为什么需要单独授权

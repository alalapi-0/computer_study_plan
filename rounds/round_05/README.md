# Round 05 · 高频算法模式

这个目录是 Round 05（双指针 / 滑动窗口 / 二分 / DFS / BFS / 回溯 / 贪心 / DP）的 Web UI 可完成练习轮。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round5`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 目录结构

```
round_05/
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
   └─ algorithm_patterns_cheatsheet.md
```

## 使用方式

1. 启动本地 Web UI：`python3 scripts/progress_server.py`。
2. 打开 `progress.html?round=round_05`，进入 Round 05。
3. 每周先点“学习资料”阅读 notes，再点练习任务的“运行”生成示例脚本。
4. 自测任务请点“终端”，在浏览器映射终端中进入 `~/cli-lab/round5` 手写 Python 小程序。
5. 能解释“看到什么题型应该优先尝试哪种模式”后，再点“记录 / 完成”。

## 终端边界

- Web UI 终端映射到 `~/cli-lab` 沙盒；Round 05 任务会切到 `~/cli-lab/round5`。
- “运行”按钮只用于自动练习脚本；自测、小抄和验收必须由用户手动确认。
- 命令历史会关联 `task_id`，但执行命令本身不等同于完成任务。

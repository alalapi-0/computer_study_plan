# linux-foundations · Linux 基础与工程实践

当前仓库**唯一正式课程**。

## 课程目标

用这一门 Linux 课程验证：

- 用户是否愿意持续学习
- 每条任务是否可被记录
- 每次学习动作是否能得到反馈
- 是否能形成经验值、掌握度、关卡和通关感
- 网页交互是否有趣、美观、有效
- 是否真正帮助用户坚持并学会 Linux

## 模块顺序

| 顺序 | 模块 | 兼容 Round |
|---|---|---|
| 0 | Terminal 初见 | `round_00` |
| 1 | 文件系统与基础命令 | `round_01` |
| 2 | Shell、管道与 Git 最小工作流 | `round_02` |
| 3 | Linux 进阶与自动化 | `round_06` |
| 4 | VPS 远程实操（只读优先） | `stage_03_vps_remote_ops` |

机器可读注册表：[`course.json`](course.json)

## 学习入口

```bash
python3 scripts/progress_server.py
# 打开 http://127.0.0.1:8777/progress.html?round=round_00
```

## 说明

- 本阶段不新增第二门课程。
- 可执行练习内容仍位于 `rounds/`，以保持 Round 00 现有闭环。
- XP、成就、积分和完整反馈引擎尚未实现；见 `docs/ROADMAP.md`。

# records/ · 用户真实学习记录目录

> 本目录承载真实发生过的学习记录：周复盘、练习问题、动作日志、反馈、存档。
> 它和 `plans/`（计划说明）、`rounds/`（可执行练习）、`content/courses/`（课程注册）分工明确。

---

## 1. 当前约束

- 截至 2026-07-18，本目录下没有需要特殊保护的真实学习记录。
- 后续如果开始写真实周复盘或问题笔记，再由用户明确标注保护范围。
- 不要在本目录写入账号、证件号、真实报名号、cookies、token 或私钥。

---

## 2. 目录结构

```text
records/
├─ weekly_reviews/              ← 每周复盘
│  └─ YYYY-WW.md
├─ error_notes/                 ← 练习问题复盘
│  └─ linux-foundations/
├─ completed_tasks/             ← 可选：完成快照
├─ action_logs/events.jsonl     ← 动作日志
├─ feedback/task_feedback.json  ← 任务反馈（生成器维护）
├─ saves/                       ← 本地存档（通常 gitignore）
└─ terminal/commands.jsonl      ← 浏览器终端历史（通常 gitignore）
```

详细复盘规则见 `docs/ERROR_REVIEW_SYSTEM.md`。

---

## 3. 命名规则

| 类型 | 命名 |
|---|---|
| 周复盘 | `weekly_reviews/YYYY-WW.md` |
| 问题复盘 | `error_notes/linux-foundations/<module>/YYYY-MM-DD-shortid.md` |
| 完成快照 | `completed_tasks/linux-foundations/<module>/YYYY-MM-DD-<shortid>.md` |

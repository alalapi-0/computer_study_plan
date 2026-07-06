# records/ · 用户真实学习记录目录

> 本目录承载**真实发生过的学习记录**：周复盘、错题、完成的练习快照。
> 它和 `plans/`（计划与笔记骨架）、`rounds/`（可执行练习目录）分工明确。

---

## 1. 当前约束

- 截至 2026-07-06，用户已确认本目录下没有需要保护的真实学习记录。
- 后续如果开始写真实周复盘、错题或完成快照，再由用户明确标注保护范围。
- 不要在本目录写入账号、证件号、真实报名号、cookies、token 或私钥。

---

## 2. 目录结构

```
records/
├─ weekly_reviews/         ← 每周复盘
│  └─ YYYY-WW.md           ← 按 ISO 周数命名
├─ error_notes/            ← 错题本（按 lane / module 归档）
│  ├─ soft_exam/
│  ├─ math2/
│  └─ cs408/
└─ completed_tasks/        ← 可选：完成的练习快照
```

详细分类规则见 `docs/ERROR_REVIEW_SYSTEM.md`。

---

## 3. 命名规则

| 类型 | 命名 |
|---|---|
| 周复盘 | `weekly_reviews/YYYY-WW.md`（W 是 ISO 周数，01–53） |
| 错题 | `error_notes/<lane>/<module>/YYYY-MM-DD-shortid.md` |
| 模考记录 | `weekly_reviews/mock_exams/YYYY-MM-DD-<lane>-<name>.md` |
| 完成的练习快照 | `completed_tasks/<lane>/<module>/YYYY-MM-DD-<shortid>.md` |

---

## 4. 写入工作流

1. **周日 / 周一**：选择本周强度（参见 `docs/WEEKLY_EXECUTION_TEMPLATE.md`），创建本周 `weekly_reviews/YYYY-WW.md` 骨架。
2. **工作日 / 周末做题时**：遇到错题 → 当天或次日录入 `error_notes/...`。
3. **周末 / 周一**：完成本周复盘，归档周复盘文件。
4. **每周一次**：根据本周错题判断是否触发回流（详见 `docs/ERROR_REVIEW_SYSTEM.md` §5）。

---

## 5. 与 progress.json 的关系

- 本目录**不进入** `progress.json`。
- `progress.json` 只跟踪"我注册的、显式的任务"是否完成。
- 错题数量、周复盘动作、薄弱项标记都通过本目录的文件表达。

---

## 6. 隐私与安全

- 本目录会随仓库提交到 GitHub（公开 / 私有取决于你的仓库设置）。
- 不要在本目录中写入：
  - 真实身份证号 / 手机号 / 邮箱
  - 真实考试报名号
  - 真实院校官网密码 / cookies
- 错题本可以写题面与解题过程；不要写情绪 / 抱怨内容。

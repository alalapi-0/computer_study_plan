# Architecture

> 更新日期：2026-07-18
> 原则：当前只有一个 active course；底层模型保持 course-agnostic；不为不存在的多课程需求过度设计。

## 1. 当前架构立场

- **Active course**：仅 `linux-foundations`
- **平台层**：任务进度、动作日志、本地 Web UI、CLI、生成与校验脚本
- **内容层**：Linux 课程模块与练习材料
- **本轮不做**：UI 视觉重构、XP 引擎、数据库、账号系统、云同步

## 2. 逻辑分层

```text
content/          课程内容（当前仅 linux-foundations）
platform data/    progress.json / events / feedback（现状仍在仓库根与 records/）
web UI            progress.html + progress_ui.js
local service     scripts/progress_server.py
CLI               mark_done.sh
docs/             愿景、路线、架构、状态
```

目标目录结构（分阶段收敛，不是要求本轮一次性搬迁全部文件）：

```text
computer_study_plan/
├─ content/
│  └─ courses/
│     └─ linux-foundations/
│        ├─ course.json
│        ├─ README.md
│        └─ modules/
│           ├─ module-00-terminal/
│           ├─ module-01-filesystem/
│           ├─ module-02-shell-git/
│           ├─ module-03-automation/
│           └─ module-04-remote-vps/
├─ rounds/                 # Phase 0/1 兼容执行真源（Round 00 闭环）
├─ plans/linux/            # 课程学习路径说明
├─ scripts/                # 平台脚本
├─ records/                # 动作日志、反馈、存档、终端历史
├─ progress.html
├─ progress_ui.js
├─ progress.json
├─ docs/
├─ README.md
└─ AGENTS.md
```

## 3. 数据模型（当前 + 目标）

### 当前已实现

| 概念 | 存储 | 说明 |
|---|---|---|
| Course / Lane | `progress.json.lanes` | 现阶段用 `linux-foundations` 表达唯一课程 |
| Task progress | `progress.json.tasks` | `done` / `done_at` / `lane` |
| Round metadata | `rounds_data.js` | 由 `build_rounds_data.py` 生成 |
| Action events | `records/action_logs/events.jsonl` | mark_done / undo / run_exercise |
| Task feedback | `records/feedback/task_feedback.json` | 生成器输出 |

### 后续目标（未完整实现）

| 概念 | 用途 |
|---|---|
| Course / Module / Lesson / Task | 统一内容模型 |
| Attempt | 单次尝试细节 |
| Action Event | 更细粒度学习动作 |
| XP / Mastery | 成长与通关 |
| Reward | 绑定真实学习证据 |

## 4. 运行时链路

```text
浏览器 progress.html
  → 读取 progress_data.js / rounds_data.js
  → 调用 scripts/progress_server.py API
  → 读写 progress.json
  → 追加 events.jsonl
  → 生成 task_feedback.json
  → 同步 progress_data.js
```

CLI 平行链路：

```text
bash mark_done.sh <task-id>
  → scripts/mark_done_cli.py
  → progress_lib.py
```

## 5. 内容与兼容策略

Phase 0：

- `content/courses/linux-foundations/course.json` 注册唯一课程与模块索引
- 可执行 notes / exercises 仍在 `rounds/round_00|01|02|06` 与 VPS 目录
- 目的：不破坏 Round 00 现有可运行闭环

Phase 1：

- 将任务定义迁入统一模型
- 逐步降低对根目录 `round_XX.md` 散落结构的依赖
- 保持旧入口兼容直到迁移完成

## 6. 明确非目标

- 不为“将来可能有很多课”提前引入复杂多租户架构
- 不在本阶段引入前端框架或数据库
- 不把平台实现用的 Python/JavaScript 误当成课程内容删除
- UI/UX 系统重设计放到 Phase 6

## 7. 相关决策

见 `docs/DECISIONS.md`（JSON 存储、原生 Web UI、CLI 兼容、单课程 active course）。

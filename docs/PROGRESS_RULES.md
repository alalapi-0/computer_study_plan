# Progress Rules · 进度规则（v2.0）

> 更新日期：2026-07-18
> 单课程阶段：只有 `linux-foundations` 一条正式进度 lane。

## 1. 唯一正式课程 / lane

| lane / course_id | 中文名 | 主要内容 |
|---|---|---|
| `linux-foundations` | Linux 基础与工程实践 | 终端、文件系统、Shell、自动化、远程实操 |

进度完成状态由 `progress.json` 持有；Web UI / `mark_done.sh` 写入；`progress_data.js` 是前端镜像；`rounds_data.js` 提供任务展示元数据。

## 2. 完成与撤销

- Web UI：「记录并完成」必须填写本次记录后保存
- CLI：`bash mark_done.sh <task-id>` / `--undo`
- 完成与撤销都会更新进度、镜像、动作日志和任务反馈

## 3. 动作日志与反馈

- 动作日志：`records/action_logs/events.jsonl`
- 任务反馈：`records/feedback/task_feedback.json`（生成器维护，不手工编辑）
- 当前反馈仍是最小实现，不是完整规则引擎

## 4. 生成关系

| 命令 | 输出 |
|---|---|
| `npm run build:rounds` | `rounds_data.js` + 合并/裁剪 `progress.json` + 同步镜像 |
| `npm run sync:progress` | `progress_data.js` |
| `python3 scripts/generate_task_feedback.py` | `task_feedback.json` |

## 5. 禁止事项

- 不手工编辑 `progress_data.js` / `rounds_data.js` / `task_feedback.json`
- 不重新引入 soft_exam / math2 / cs408 作为正式 lane
- 不把“打开页面”当成任务完成

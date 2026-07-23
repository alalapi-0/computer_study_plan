# Action Logs

`records/action_logs/events.jsonl` 用于保存任务动作事件（JSON Lines）。

## 字段说明（v1）

- `action_id`: 事件唯一 ID（UUID）
- `task_id`: 任务 ID（如 `w1-read`、`r02-w1-ex1`）
- `round_id`: 轮次 ID（如 `round_00`、`round_02`）
- `lane`: 课程 lane（当前仅 `linux-foundations`）
- `action_type`: 动作类型（当前支持 `mark_done`、`undo_done`、`run_exercise`）
- `timestamp`: 事件时间（ISO 8601）
- `result`: 动作结果（`ok` / `noop_already_done` / `failed` / `timeout`）
- `note`: 备注（预留）
- `evidence_path`: 证据路径（预留）
- `details`: 可选对象；Web UI 执行练习脚本时会记录脚本路径、沙盒路径、返回码、耗时和输出摘要

## 使用说明

- 该文件由 `mark_done.sh` 和 Web UI 自动追加写入，不建议手工编辑。
- 可配合后续脚本做任务历史查询和反馈生成。

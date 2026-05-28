# Task Feedback Prototype

`records/feedback/task_feedback.json` 是任务反馈原型输出文件。

## 生成方式

在仓库根目录执行：

```bash
python3 scripts/generate_task_feedback.py
```

## 反馈规则（v1）

- `completed`：任务已完成，建议进入复盘或下一任务。
- `not_started`：任务尚无动作，建议先做最小启动动作。
- `in_progress`：已有动作但未完成，建议先收敛当前任务闭环。

## 数据来源

- 状态来源：`progress.json`
- 动作来源：`records/action_logs/events.jsonl`

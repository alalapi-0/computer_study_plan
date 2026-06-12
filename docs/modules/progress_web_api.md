# Progress 网页学习 API（learn_server）

> 服务脚本：`scripts/learn_server.py` · 写入层：`scripts/progress_store.py`  
> 路线图：`docs/PROGRESS_WEB_LEARNING_ROADMAP.md`

## 启动

```bash
cd <仓库根>
python3 scripts/learn_server.py
# 默认 http://127.0.0.1:8000/progress.html
```

## 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/health` | 服务健康检查 |
| GET | `/api/progress` | 读取 `progress.json`（v2） |
| POST | `/api/tasks/<task_id>/done` | 标记完成 |
| POST | `/api/tasks/<task_id>/undo` | 取消完成 |
| GET | `/api/content?path=<rel>&format=json\|html` | 读取白名单内 Markdown（`rounds/`、`plans/`） |
| GET | `/api/exercise/guide?path=<rel>` | 解析练习脚本步骤（Shell 引导 / Python 元数据） |
| POST | `/api/exercise/run` | 运行非交互练习脚本，body: `{"path":"rounds/.../exercises.py"}` |
| GET | `/api/tasks/<task_id>/events` | 读取 `records/action_logs/events.jsonl` 中该任务最近记录 |
| GET | `/api/tasks/<task_id>/feedback` | 读取 `records/feedback/task_feedback.json` 中该任务反馈 |
| POST | `/api/error_notes` | 写入错题笔记，body: `lane`, `module`, `title`, `wrong_answer`, `correct_answer`, `note` |

## 批量接入骨架轮次

```bash
npm run sync:skeleton-progress
# 或 python3 scripts/sync_skeleton_progress.py 5 21
```

为 Round 05–21 生成标准任务并同步 `progress_rounds.json`。

## 安全

- 默认绑定 `127.0.0.1`
- `content` 路径禁止 `..`，仅允许 `.md` / `.txt`
- 无认证（单用户本机）

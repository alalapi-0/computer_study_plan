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

## 安全

- 默认绑定 `127.0.0.1`
- `content` 路径禁止 `..`，仅允许 `.md` / `.txt`
- 无认证（单用户本机）

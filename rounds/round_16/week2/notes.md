# Round 16 · Week 2 笔记（GET 读接口 + 文件上传）

## Web UI 学习路径

1. 在 Round 16 页面阅读本文。
2. 点击“练习：生成 GET /runs 与上传接口”的“运行脚本”按钮。
3. 在运行结果里确认生成了 `app/routers/runs.py`、`app/routers/jobs.py` 和 `round16_week2_query_report.json`。
4. 点击“自测：自己写列表/详情查询”的“终端练习”按钮，手敲下面的自测命令。
5. 能解释列表、详情、格式过滤、上传临时文件清理后，点击“记录并完成”。

## 本周要建立的直觉

写接口不只写 `POST /run`，还要能看历史记录：

| 接口 | 数据来源 | 关键点 |
|---|---|---|
| `GET /runs` | SQLite 多行 | `skip` / `limit` / `format` 是查询参数 |
| `GET /runs/{run_id}` | SQLite 单行 | 找不到返回 404 |
| `POST /run/upload` | 上传文件 | 临时文件用完必须清理 |

上传接口的核心不是“文件怎么传得很大”，而是先建立安全的最小动作：接收 `UploadFile`，写到临时文件，复用同一套处理逻辑，最后在 `finally` 里删掉临时文件。

## 自动练习会做什么

脚本会在 `~/cli-lab/round16/week2_auto/read_upload_api` 下生成：

- `app/routers/runs.py`：从 SQLite 读取列表、详情和格式过滤。
- `app/routers/jobs.py`：`POST /run/upload` 上传入口。
- `app/db.py`：`get_all_runs`、`get_run`、`get_runs_by_format`。
- `seed_and_query.py`：写入两条记录并读取验证。
- `static_check_report.json`：检查读接口、上传代码和 SQLite 查询结果。

## 浏览器终端自测

本周终端自测只模拟“列表/详情/过滤”的数据形状：

```bash
pwd
mkdir round16_w2_self
cd round16_w2_self
printf 'runs = [{"id": 1, "format": "txt"}, {"id": 2, "format": "csv"}]\nprint([r for r in runs if r["format"] == "txt"])\nprint(next(r for r in runs if r["id"] == 2))\n' > mini_queries.py
python3 mini_queries.py
cat mini_queries.py
```

如果你能说明“列表接口返回数组，详情接口返回单个对象，过滤参数只改变集合范围”，Week 2 就过关。

## 外部参考

- [FastAPI Request Files](https://fastapi.tiangolo.com/tutorial/request-files/)
- [FastAPI Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)

# Round 16 · Week 1 笔记（POST /run 接真实逻辑）

## Web UI 学习路径

1. 在 Round 16 页面阅读本文。
2. 点击“练习：生成 POST /run + SQLite 写入链路”的“运行脚本”按钮。
3. 在运行结果里确认生成了 `app/routers/jobs.py`、`app/db.py` 和 `static_check_report.json`。
4. 点击“自测：自己写最小 SQLite 写入脚本”的“终端练习”按钮，手敲下面的自测命令。
5. 能解释“请求 → 读文件 → 核心处理 → 写输出 → 写 SQLite → 返回响应”后，点击“记录并完成”。

## 本周要建立的直觉

Round 15 的 API 还偏 mock；Round 16 开始让 API 调真实逻辑。`POST /run` 的主链应该像流水线：

| 步骤 | 代码位置 | 失败时 |
|---|---|---|
| 校验输入文件存在 | router | `404 input_not_found` |
| 读取 txt/csv | `io_utils.read_records` | `400 read_failed` |
| 清洗和去重 | `core.filter_records` / `core.dedup_records` | 保持纯函数 |
| 写输出文件 | router 或 service | 返回输出路径 |
| 写运行记录 | `db.insert_run` | 后续可查询 |

重点不是一次写成生产级项目，而是先把“路由只负责接请求和翻译错误，核心逻辑和数据层各做自己的事”这个边界分清楚。

## 自动练习会做什么

脚本会在 `~/cli-lab/round16/week1_auto/api_data_layer` 下生成：

- `app/routers/jobs.py`：`POST /run` 的 FastAPI 路由代码。
- `app/db.py`：SQLite 建表和 `insert_run`。
- `app/core.py` / `app/io_utils.py`：清洗、去重、读取文件。
- `run_flow_demo.py`：不用启动 Web 服务，直接跑一遍处理链。
- `static_check_report.json`：检查路由、错误、SQLite 和 demo 输出是否齐全。

## 浏览器终端自测

本周终端自测只练 SQLite 写入，不安装依赖：

```bash
pwd
mkdir round16_w1_self
cd round16_w1_self
printf 'import sqlite3\nconn = sqlite3.connect("runs.db")\nconn.execute("create table if not exists runs (id integer primary key, status text)")\nconn.execute("insert into runs (status) values (?)", ("completed",))\nconn.commit()\nprint(conn.execute("select count(*) from runs").fetchone()[0])\n' > mini_db.py
python3 mini_db.py
ls
```

如果输出 `1`，并且你能说明 `connect / create table / insert / select count` 各自做什么，Week 1 就过关。

## 外部参考

- [FastAPI Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)

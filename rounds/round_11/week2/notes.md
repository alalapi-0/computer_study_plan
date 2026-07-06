# Round 11 · Week 2 笔记（插入与查询）

## 本周目标

- 每次模拟运行后向 `runs` 表插入一条记录。
- 能查询全部记录并按条件过滤。

## Web UI 学习路径

1. 打开本文件，先确认数据库访问不要散落在主程序各处，应该收敛进 `db.py`。
2. 点击 `r11-w2-ex2` 的“运行脚本”。脚本会在 `~/cli-lab/round11/week2_auto/ai_prep_tool` 生成：
   - `db.py`
   - `check_runs.py`
   - `runs.db`
   - `query_report.txt`
3. 运行结果会显示 `all_runs: 3` 和 `txt_runs: 2`。
4. 点击 `r11-w2-self` 的“终端练习”，自己封装一个 `insert_run()` 和 `get_all_runs()`。

## db.py 四个核心函数

- `init_db()`：建表，已经存在就不重复创建。
- `insert_run()`：插入一条运行记录，返回新记录 id。
- `get_all_runs()`：按时间或 id 倒序查询全部运行记录。
- `get_runs_by_format(fmt)`：用 `WHERE format = ?` 按格式筛选。

## 查询也要参数化

插入要参数化，查询也要参数化：

```python
rows = conn.execute(
    "SELECT * FROM runs WHERE format = ? ORDER BY id DESC",
    (fmt,),
).fetchall()
```

单个参数也要写成 `(fmt,)`，后面的逗号不能少。

## 浏览器终端自测命令

在 `r11-w2-self` 的终端里逐条运行：

```bash
mkdir week2_self
cd week2_self
printf 'import sqlite3\n\ndef init_db():\n    conn = sqlite3.connect("runs.db")\n    conn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, format TEXT, processed_count INTEGER)")\n    conn.commit()\n    conn.close()\n\ndef insert_run(fmt, processed_count):\n    conn = sqlite3.connect("runs.db")\n    conn.execute("INSERT INTO runs (format, processed_count) VALUES (?, ?)", (fmt, processed_count))\n    conn.commit()\n    conn.close()\n\ninit_db()\ninsert_run("txt", 3)\nconn = sqlite3.connect("runs.db")\nprint(conn.execute("SELECT COUNT(*) FROM runs WHERE format = ?", ("txt",)).fetchone()[0])\nconn.close()\n' > db_demo.py
python3 db_demo.py
```

看到 `1` 后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能使用 `?` 占位符完成 insert
- [ ] 能执行 `SELECT * FROM runs ORDER BY run_at DESC`
- [ ] 能解释 `sqlite3.Row` 为什么让查询结果更易读

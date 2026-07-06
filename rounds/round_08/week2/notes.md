# Round 08 · Week 2 笔记（sqlite3 最小持久化）

## 本周目标

- 完成 sqlite3 初始化、插入、查询三步闭环。
- 把“处理历史”转成可回看数据，而不是只看终端输出。

## Web UI 学习路径

1. 先点击本文件“读教程”，理解持久化层解决的是“运行历史能回看”。
2. 点击 `r08-w2-ex2` 的“运行脚本”。脚本会在 `~/cli-lab/round8/week2_auto` 生成：
   - `runs.db`
   - `runs_report.txt`
   - `next_steps.txt`
3. 运行输出应看到数据库路径、记录条数和最近一条记录。
4. 点击 `r08-w2-self` 的“终端练习”，自己写一个 `runs_db.py`，完成建表、插入和查询。

## sqlite3 最小闭环

- `sqlite3.connect(path)`：打开或创建数据库文件。
- `CREATE TABLE IF NOT EXISTS`：保证表存在。
- `INSERT ... VALUES (?, ?, ?)`：参数化写入，避免 SQL 拼接风险。
- `SELECT ... ORDER BY id DESC`：按最近运行倒序回看。
- `conn.commit()`：确认写入。
- `conn.close()`：释放连接。

## 浏览器终端自测命令

在 `r08-w2-self` 的终端里逐条运行：

```bash
mkdir week2_self
cd week2_self
printf 'import sqlite3\nfrom datetime import datetime\nconn = sqlite3.connect("runs.db")\nconn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, input_file TEXT, output_file TEXT, original_count INTEGER, processed_count INTEGER, run_time TEXT)")\n' > runs_db.py
printf 'conn.execute("INSERT INTO runs (input_file, output_file, original_count, processed_count, run_time) VALUES (?, ?, ?, ?, ?)", ("input/demo.txt", "output/demo.txt", 4, 3, datetime.now().isoformat(timespec="seconds")))\nconn.commit()\nfor row in conn.execute("SELECT input_file, output_file, original_count, processed_count FROM runs ORDER BY id DESC"):\n    print(row)\nconn.close()\n' >> runs_db.py
python3 runs_db.py
ls
```

能解释参数化 SQL 和 `commit()` 后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能创建 `runs` 表并插入至少一条记录
- [ ] 能说明参数化 SQL 的必要性
- [ ] 能说明数据库文件为什么放在练习沙盒而不是仓库根

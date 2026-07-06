# Round 11 · Week 1 笔记（建表与初始化）

## 本周目标

- 在沙盒中创建 `runs` 表并初始化 SQLite 文件。
- 理解参数化 SQL 的基本写法。

## Web UI 学习路径

1. 在 Round 11 里打开本文件，先看清 `runs` 表的意义：一行记录代表一次工具运行。
2. 点击 `r11-w1-ex1` 的“运行脚本”。脚本会在 `~/cli-lab/round11/week1_auto/ai_prep_tool` 生成：
   - `runs.db`
   - `schema_report.txt`
   - `next_steps.txt`
3. 运行结果会显示 `runs` 表字段和插入后的 `row_count`。
4. 点击 `r11-w1-self` 的“终端练习”，自己写最小 sqlite3 建表和插入脚本。

## runs 表最小字段

- `id`：自增主键。
- `input_file`：本次运行读了哪个输入文件。
- `output_file`：本次运行写到哪个输出文件。
- `format`：输入格式，例如 `txt` / `csv` / `jsonl`。
- `original_count`：处理前记录数。
- `processed_count`：处理后记录数。
- `dedup`：是否去重，通常用 0 / 1。
- `run_at` 或 `run_time`：运行时间。

## 参数化 SQL

永远优先写：

```python
conn.execute(
    "INSERT INTO runs (input_file, output_file, format) VALUES (?, ?, ?)",
    ("input/a.txt", "output/a.txt", "txt"),
)
```

不要把用户输入拼进 SQL 字符串。

## 浏览器终端自测命令

在 `r11-w1-self` 的终端里逐条运行：

```bash
mkdir week1_self
cd week1_self
printf 'import sqlite3\n\nconn = sqlite3.connect("runs.db")\nconn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, input_file TEXT, processed_count INTEGER)")\nconn.execute("INSERT INTO runs (input_file, processed_count) VALUES (?, ?)", ("input/a.txt", 3))\nconn.commit()\nprint(conn.execute("SELECT COUNT(*) FROM runs").fetchone()[0])\nconn.close()\n' > sqlite_demo.py
python3 sqlite_demo.py
```

看到 `1` 后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能写出 `CREATE TABLE runs (...)` 的最小字段集
- [ ] 能说明为什么不要用字符串拼接拼 SQL
- [ ] 能解释为什么写入后需要 `conn.commit()`

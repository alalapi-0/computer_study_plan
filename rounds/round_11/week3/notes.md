# Round 11 · Week 3 笔记（收口与复盘）

## 本周目标

- 把数据库访问封装到 `db.py`。
- 完成 Round 11 沙盒最小收口检查。

## Web UI 学习路径

1. 打开本文件，先确认接入点：工具处理完成后，调用 `insert_run()` 写入一条历史记录。
2. 点击 `r11-w3-ex3` 的“运行脚本”。脚本会在 `~/cli-lab/round11/week3_auto/ai_prep_tool` 生成：
   - `db.py`
   - `ai_prep_tool.py`
   - `check_runs.py`
   - `runs.db`
   - `persistence_report.txt`
3. 运行结果会验证工具运行两次后，`runs.db` 中有两条记录。
4. 点击 `r11-w3-self` 的“终端练习”，自己把 `insert_run()` 接入一个小处理脚本。

## 接入顺序

1. 程序启动时调用 `init_db()`。
2. 读取输入，得到 `original_count`。
3. 处理和写输出，得到 `processed_count`。
4. 调用 `insert_run(...)` 记录输入、输出、格式、计数、是否去重。
5. 查询 `get_all_runs()` 验证刚才那次运行已落库。

## 不要记录什么

- 不把完整原始数据塞进 `runs` 表。
- 不把 `.db` 文件提交进 Git。
- 不为了一个表提前引入 ORM。

## 浏览器终端自测命令

在 `r11-w3-self` 的终端里逐条运行：

```bash
mkdir week3_self
cd week3_self
printf 'import sqlite3\n\ndef init_db():\n    conn = sqlite3.connect("runs.db")\n    conn.execute("CREATE TABLE IF NOT EXISTS runs (id INTEGER PRIMARY KEY AUTOINCREMENT, input_file TEXT, processed_count INTEGER)")\n    conn.commit()\n    conn.close()\n\ndef insert_run(input_file, processed_count):\n    conn = sqlite3.connect("runs.db")\n    conn.execute("INSERT INTO runs (input_file, processed_count) VALUES (?, ?)", (input_file, processed_count))\n    conn.commit()\n    conn.close()\n\ninit_db()\nrecords = ["a", "b", "a"]\nprocessed = list(dict.fromkeys(records))\ninsert_run("demo", len(processed))\nconn = sqlite3.connect("runs.db")\nprint(conn.execute("SELECT processed_count FROM runs").fetchone()[0])\nconn.close()\n' > app_with_db.py
python3 app_with_db.py
```

看到 `2` 后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能在 final 检查中看到 runs 表与 db 模块均存在
- [ ] 能解释 runs 表每条记录代表什么
- [ ] 能说明为什么运行历史记录的是摘要，而不是原始数据全文

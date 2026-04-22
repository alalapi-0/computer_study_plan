# Round 11 · 本地持久化与数据记录

> **定位**（路线 A 第 3 步）：把工具从"处理完就结束"的脚本，推进成"会留下历史、能被查询、能做最小数据管理"的小系统。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | SQLite + Python sqlite3 + 参数化查询 + 历史记录查询 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 10 |
| **下一轮** | Round 12 · 自动化流水线与批处理 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] `ai_prep_tool` 每次运行后，把关键信息写入 SQLite
- [ ] 有一张 `runs` 表（输入文件/输出文件/原始条数/最终条数/运行时间）
- [ ] 能初始化数据库、插入记录、查询全部、按条件查询
- [ ] 永远用参数化写法写 SQL（`?` 占位符）

---

## 本轮不学什么

> 先不碰：ORM、复杂表关系、migration 工具、多表 join 深水区、事务细节深挖、API 接数据库

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Python – sqlite3](https://docs.python.org/3/library/sqlite3.html) | 标准库 DB-API 2.0，含 tutorial + how-to |
| 📄 文档 2 | [SQLite – CREATE TABLE](https://www.sqlite.org/lang_createtable.html) | 建表语法 |
| 📄 文档 3 | [SQLite – INSERT](https://www.sqlite.org/lang_insert.html) | 插入语法 |

---

## 建议的项目结构

```
ai_prep_tool/
├─ cli.py
├─ core.py
├─ io_utils.py
├─ config.py
├─ log_utils.py
├─ db.py             # ← 新增：数据库操作
├─ config.ini
├─ README.md
├─ .gitignore
├─ tests/
├─ input/
├─ output/
├─ logs/
└─ runs.db           # ← 新增：SQLite 数据库文件
```

---

## 3 周学习安排

### 第 1 周：SQLite 基础认知 + 建表 + 插入

**目标**：第一次自己建表、写数据进去、查出来。

**关键理解**：
- `sqlite3.connect("runs.db")` 如果文件不存在会自动创建
- 永远用 `?` 占位符，不要字符串拼 SQL
- `conn.commit()` 才真正写入

---

### 第 2 周：查询 + 条件筛选 + 封装

**目标**：把数据库操作封装成函数，项目可以调用。

**要学会的 4 个动作**：
1. 初始化数据库（建表）
2. 插入一条运行记录
3. 查询全部运行记录
4. 按条件查某一类运行记录

---

### 第 3 周：接入主工具

**目标**：每次运行 `ai_prep_tool.py` 后，自动写一条历史记录。

---

## 本轮练习清单

### 第 1 周练习

**练习 1**：sqlite3 最小操作
```python
# sqlite3_demo.py
import sqlite3

# 连接（文件不存在时自动创建）
conn = sqlite3.connect("demo.db")

# 建表
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        score INTEGER
    )
""")
conn.commit()

# 插入（参数化写法）
conn.execute("INSERT INTO users (name, score) VALUES (?, ?)", ("Alice", 95))
conn.execute("INSERT INTO users (name, score) VALUES (?, ?)", ("Bob", 82))
conn.commit()

# 查询全部
cursor = conn.execute("SELECT * FROM users")
for row in cursor.fetchall():
    print(row)

conn.close()
```

**练习 2**：条件查询
```python
# query_demo.py
import sqlite3

conn = sqlite3.connect("demo.db")

# 按条件查询
cursor = conn.execute("SELECT * FROM users WHERE score > ?", (90,))
print("High scorers:", cursor.fetchall())

# 统计
cursor = conn.execute("SELECT COUNT(*) FROM users")
print("Total users:", cursor.fetchone()[0])

conn.close()
```

---

### 第 2 周练习

**`db.py`**：
```python
# db.py
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = "runs.db"

def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 让结果可以按列名访问
    return conn

def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """初始化数据库，建表（如果不存在）"""
    conn = get_connection(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            input_file TEXT,
            output_file TEXT,
            format     TEXT,
            original_count INTEGER,
            processed_count INTEGER,
            dedup      INTEGER DEFAULT 0,
            run_time   TEXT
        )
    """)
    conn.commit()
    conn.close()
    logger.info(f"Database initialized: {db_path}")

def insert_run(
    input_file: str,
    output_file: str,
    fmt: str,
    original_count: int,
    processed_count: int,
    dedup: bool = False,
    db_path: str = DEFAULT_DB_PATH
) -> int:
    """插入一条运行记录，返回新记录的 id"""
    conn = get_connection(db_path)
    cursor = conn.execute(
        """INSERT INTO runs
           (input_file, output_file, format, original_count, processed_count, dedup, run_time)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (input_file, output_file, fmt, original_count, processed_count,
         int(dedup), datetime.now().isoformat())
    )
    conn.commit()
    run_id = cursor.lastrowid
    conn.close()
    logger.info(f"Inserted run record: id={run_id}")
    return run_id

def get_all_runs(db_path: str = DEFAULT_DB_PATH) -> list:
    """查询全部运行记录"""
    conn = get_connection(db_path)
    cursor = conn.execute("SELECT * FROM runs ORDER BY id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_runs_by_format(fmt: str, db_path: str = DEFAULT_DB_PATH) -> list:
    """按格式筛选运行记录"""
    conn = get_connection(db_path)
    cursor = conn.execute(
        "SELECT * FROM runs WHERE format = ? ORDER BY id DESC", (fmt,)
    )
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows
```

---

### 第 3 周练习

**把 db.py 接入 `ai_prep_tool.py`**：

在 `main()` 函数里加入数据库记录：
```python
# 在 ai_prep_tool.py 的 main() 里加
from db import init_db, insert_run

def main():
    # ... 前面的代码 ...
    
    # 初始化数据库（只在第一次运行时建表）
    init_db()
    
    # ... 处理逻辑 ...
    
    # 写入运行记录
    run_id = insert_run(
        input_file=args.input,
        output_file=args.output,
        fmt=args.format,
        original_count=len(original),
        processed_count=len(records),
        dedup=args.dedup
    )
    logger.info(f"Run saved: id={run_id}")
```

**验证**：
```python
# check_runs.py
from db import get_all_runs, get_runs_by_format

runs = get_all_runs()
print(f"Total runs: {len(runs)}")
for run in runs[:5]:
    print(f"  [{run['id']}] {run['input_file']} → {run['output_file']}")

print("\nTXT format runs:")
for run in get_runs_by_format("txt"):
    print(f"  [{run['id']}] orig={run['original_count']}, processed={run['processed_count']}")
```

---

## 验收标准

- [ ] `db.py` 包含 `init_db`、`insert_run`、`get_all_runs`、`get_runs_by_format` 四个函数
- [ ] 每次运行 `ai_prep_tool.py` 后，`runs.db` 里多一条记录
- [ ] 所有 SQL 都用 `?` 参数化，没有字符串拼接
- [ ] `.gitignore` 里已经加入 `*.db`

---

## ⚠️ 最容易踩的坑

1. **用字符串拼 SQL** — `f"...WHERE id={user_id}"` 是 SQL 注入风险，永远用 `?`
2. **忘记 `conn.commit()`** — 写入操作必须 commit，否则数据不会真正持久化
3. **`runs.db` 提交进 Git** — 在 `.gitignore` 里加 `*.db`

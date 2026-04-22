# Round 08 · 总复盘与升级路线

> **定位**：不再继续加新零件，而是把 Round 00-07 的能力收口成一个稳定可展示的小项目，并明确后续升级路线。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 项目整理 + Git 分支 + pytest 最小测试 + sqlite3 入门 + FastAPI 最小服务 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 07 |
| **下一轮** | Round 09 · 仓库规范化与测试入门（路线 A） |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] `ai_prep_tool` 整理成一个有 README/tests/logs 的像样小仓库
- [ ] 用 Git 分支做小改动，再合并回主分支
- [ ] 写并运行最小的 pytest 测试
- [ ] 给工具加一个本地持久化层（sqlite3）
- [ ] 把工具包装成最小 FastAPI 服务
- [ ] 知道下一阶段该补什么（路线 A/B/C 选择）

---

## 后续路线说明

本轮结束后，你可以选择三条路线深入：

| 路线 | 内容 | 从哪轮开始 |
|------|------|-----------|
| **路线 A** | 工程化深入（测试、结构、发布） | Round 09 |
| **路线 B** | 服务化（HTTP、FastAPI、数据层结合） | Round 14 |
| **路线 C** | AI/ML 核心（NumPy、sklearn、PyTorch、NLP） | Round 18 |

> 建议顺序：A → B → C，确保工程基础站稳后再上 AI 框架。

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Pro Git – Branching](https://git-scm.com/book/zh/v2/Git-分支-分支简介) | Git 分支基础和合并 |
| 📄 文档 2 | [pytest – Get Started](https://docs.pytest.org/en/stable/getting-started.html) | 安装、写第一个测试、运行 |
| 📄 文档 3 | [Python – sqlite3](https://docs.python.org/3/library/sqlite3.html) | 标准库 DB-API 2.0 接口 |
| 📄 文档 4 | [FastAPI – First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) | 最小可运行 API |
| 📄 文档 5 | [MDN – Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) | HTTP 是什么，先建直觉 |

---

## 3 周学习安排

### 第 1 周：总复盘与代码加固

**目标**：把 `ai_prep_tool` 从"能跑"提升到"更稳"。

**任务清单**：
1. 整理项目目录结构（见下方）
2. 补 Git 分支工作流
3. 补 pytest 最小测试

**建议项目结构**：
```
ai_prep_tool/
├─ ai_prep_tool.py
├─ README.md
├─ .gitignore
├─ tests/
│  └─ test_basic.py
├─ input/
├─ output/
└─ logs/
```

---

### 第 2 周：持久化层（sqlite3）

**目标**：让工具开始留历史，而不是处理完就结束。

**建立一张最小的 `runs` 表**：
```sql
CREATE TABLE runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_file TEXT,
    output_file TEXT,
    original_count INTEGER,
    processed_count INTEGER,
    run_time TEXT
);
```

---

### 第 3 周：最小 FastAPI 服务

**目标**：把工具包一层 API，先理解"为什么要做服务化"。

**最小接口**：
```
GET  /health     → 服务存活检查
POST /run        → 触发一次处理任务
GET  /runs       → 查看历史运行记录
```

---

## 本轮练习清单

### 第 1 周练习

**练习 1**：Git 分支基础
```bash
cd ~/cli-lab/round7/ai_prep_tool
git checkout -b feature/add-tests
# 做改动
git add .
git commit -m "add tests"
git checkout main
git merge feature/add-tests
git log --oneline
```

**练习 2**：pytest 最小测试
```python
# tests/test_basic.py
from ai_prep_tool import dedup_records, build_summary

def test_dedup_removes_duplicates():
    records = ["a", "b", "a", "c", "b"]
    result = dedup_records(records)
    assert result == ["a", "b", "c"]

def test_dedup_empty():
    assert dedup_records([]) == []

def test_summary_counts():
    original = ["a", "b", "a"]
    processed = ["a", "b"]
    summary = build_summary(original, processed)
    assert summary["original_count"] == 3
    assert summary["processed_count"] == 2
    assert summary["removed_count"] == 1
```

运行测试：
```bash
pip install pytest
pytest tests/ -v
```

**练习 3**：`.gitignore` 内容
```
# .gitignore
__pycache__/
*.py[cod]
*.log
*.db
output/
logs/
.env
venv/
```

---

### 第 2 周练习

**练习 4**：sqlite3 最小操作
```python
# db_demo.py
import sqlite3
from datetime import datetime

# 初始化数据库
def init_db(db_path="runs.db"):
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_file TEXT,
            output_file TEXT,
            original_count INTEGER,
            processed_count INTEGER,
            run_time TEXT
        )
    """)
    conn.commit()
    return conn

# 插入记录（参数化写法，防 SQL 注入）
def insert_run(conn, input_file, output_file, orig, processed):
    conn.execute(
        "INSERT INTO runs (input_file, output_file, original_count, processed_count, run_time) VALUES (?, ?, ?, ?, ?)",
        (input_file, output_file, orig, processed, datetime.now().isoformat())
    )
    conn.commit()

# 查询全部记录
def get_all_runs(conn):
    cursor = conn.execute("SELECT * FROM runs ORDER BY id DESC")
    return cursor.fetchall()

# 测试
if __name__ == "__main__":
    conn = init_db()
    insert_run(conn, "input/data.txt", "output/result.txt", 100, 85)
    insert_run(conn, "input/labels.csv", "output/clean.csv", 50, 47)
    for row in get_all_runs(conn):
        print(row)
    conn.close()
```

---

### 第 3 周练习

**练习 5**：最小 FastAPI 服务
```python
# api.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Prep Tool API")

class RunRequest(BaseModel):
    input_file: str
    format: str = "txt"
    dedup: bool = False

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/runs")
def list_runs():
    # 这里先返回模拟数据，下一轮接 SQLite
    return {"runs": [], "count": 0}

@app.post("/run")
def trigger_run(req: RunRequest):
    return {
        "status": "accepted",
        "input_file": req.input_file,
        "format": req.format,
        "dedup": req.dedup,
    }
```

启动：
```bash
pip install fastapi uvicorn
uvicorn api:app --reload
# 访问 http://localhost:8000/docs 查看自动文档
```

---

## 验收标准

- [ ] 项目有 README、`.gitignore`、`tests/` 目录
- [ ] 能用 Git 切分支、做改动、合并回主分支
- [ ] pytest 测试能正常运行且通过
- [ ] sqlite3 能完成初始化/插入/查询三个动作
- [ ] FastAPI 服务能启动，`/health` 返回 `{"status": "ok"}`

---

## ⚠️ 最容易踩的坑

1. **太早扑向大模型训练** — 工程基础不稳，很容易在"模型以外的部分"反复卡住
2. **sqlite3 用字符串拼 SQL** — 永远用参数化写法（`?` 占位符），防止 SQL 注入
3. **pytest 测试文件命名** — 文件必须以 `test_` 开头，函数也必须以 `test_` 开头

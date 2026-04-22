# Round 16 · API 与数据层结合

> **定位**（路线 B 第 3 步）：把接口层和数据层真正接起来，让服务不再只返回 mock 数据，而是能接请求、调逻辑、写数据库、返回真实结果。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | FastAPI + SQLite 打通 + 文件上传 + 错误处理 + API 测试 |
| **难度** | ⭐⭐⭐⭐☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 15 |
| **下一轮** | Round 17 · 服务化收口 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] API 能真正调用核心处理逻辑（不再 mock）
- [ ] 每次 API 请求产生的运行结果会写入 SQLite
- [ ] 同时支持两种输入方式：传本地路径 + 上传文件
- [ ] 常见错误给出清楚的 HTTP 错误响应（`HTTPException`）
- [ ] 写了最基础的 API 测试（`TestClient`）

---

## 本轮不学什么

> 先不碰：认证授权、异步任务队列、复杂数据库抽象层、大规模文件流式处理、生产级部署

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [FastAPI – Request Body](https://fastapi.tiangolo.com/tutorial/body/) | 请求体结合核心逻辑 |
| 📄 文档 2 | [FastAPI – Request Files](https://fastapi.tiangolo.com/tutorial/request-files/) | `File`/`UploadFile` 接收上传文件 |
| 📄 文档 3 | [FastAPI – Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) | `HTTPException` 返回错误 |
| 📄 文档 4 | [FastAPI – Testing](https://fastapi.tiangolo.com/tutorial/testing/) | `TestClient` 做最小 API 测试 |
| 📄 文档 5 | [Python – sqlite3](https://docs.python.org/3/library/sqlite3.html) | 数据层（已在 Round 11 学过） |

---

## 推进顺序

```
1. POST /run 接真实逻辑
   ↓
2. 运行记录写入 SQLite
   ↓
3. GET /runs 和 GET /runs/{id} 从 SQLite 读取
   ↓
4. 支持上传文件接口
   ↓
5. 加 API 测试
```

---

## 3 周学习安排

### 第 1 周：POST /run 接真实逻辑 + 写数据库

**目标**：主链打通：接口请求 → 核心逻辑 → 数据库记录 → 响应返回。

---

### 第 2 周：读接口接数据库 + 文件上传

**目标**：GET 接口从真实数据库读，补充文件上传入口。

---

### 第 3 周：错误处理 + API 测试

**目标**：服务更健壮，有基础测试覆盖。

---

## 本轮练习清单

### 第 1 周练习

**`api/routers/jobs.py`（接真实逻辑）**：
```python
# api/routers/jobs.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from fastapi import APIRouter, HTTPException
from pathlib import Path
from schemas import RunRequest, RunResponse
from io_utils import read_records
from core import filter_records, dedup_records
from db import init_db, insert_run

router = APIRouter(prefix="/run", tags=["jobs"])
init_db()

@router.post("", response_model=RunResponse)
def trigger_run(req: RunRequest):
    """提交一次数据处理任务"""
    input_path = Path(req.input_file)
    if not input_path.exists():
        raise HTTPException(status_code=404, detail=f"Input file not found: {req.input_file}")
    
    # 读取
    try:
        records = read_records(req.input_file, req.format)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")
    
    original_count = len(records)
    
    # 处理
    records = filter_records(records)
    if req.dedup:
        records = dedup_records(records)
    
    # 写输出
    output_path = Path("output") / f"{input_path.stem}_result.txt"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w") as f:
        for r in records:
            f.write(r + "\n")
    
    # 写数据库
    run_id = insert_run(
        input_file=req.input_file,
        output_file=str(output_path),
        fmt=req.format,
        original_count=original_count,
        processed_count=len(records),
        dedup=req.dedup
    )
    
    return RunResponse(
        run_id=run_id,
        status="completed",
        input_file=req.input_file,
        processed_count=len(records),
        message=f"Removed {original_count - len(records)} records"
    )
```

---

### 第 2 周练习

**`api/routers/runs.py`（接数据库）**：
```python
# api/routers/runs.py
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from fastapi import APIRouter, HTTPException
from db import get_all_runs, get_runs_by_format

router = APIRouter(prefix="/runs", tags=["runs"])

@router.get("")
def list_runs(skip: int = 0, limit: int = 20, format: str | None = None):
    """查询历史运行记录（从 SQLite 读取）"""
    if format:
        runs = get_runs_by_format(format)
    else:
        runs = get_all_runs()
    return {
        "runs": runs[skip: skip + limit],
        "total": len(runs)
    }

@router.get("/{run_id}")
def get_run(run_id: int):
    """查询某次运行详情"""
    all_runs = get_all_runs()
    for run in all_runs:
        if run["id"] == run_id:
            return run
    raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
```

**文件上传接口**：
```python
# 在 jobs.py 里新增
from fastapi import UploadFile, File
import tempfile

@router.post("/upload", response_model=RunResponse)
async def upload_and_run(
    file: UploadFile = File(...),
    format: str = "txt",
    dedup: bool = False
):
    """上传文件并处理（不需要文件在服务器本地存在）"""
    # 把上传的文件写到临时目录
    with tempfile.NamedTemporaryFile(
        mode="wb",
        suffix=f".{format}",
        delete=False
    ) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        records = read_records(tmp_path, format)
        original_count = len(records)
        records = filter_records(records)
        if dedup:
            records = dedup_records(records)
        
        run_id = insert_run(
            input_file=file.filename or "uploaded",
            output_file="",
            fmt=format,
            original_count=original_count,
            processed_count=len(records),
            dedup=dedup
        )
        
        return RunResponse(
            run_id=run_id,
            status="completed",
            input_file=file.filename or "uploaded",
            processed_count=len(records)
        )
    finally:
        os.unlink(tmp_path)  # 清理临时文件
```

---

### 第 3 周练习

**API 测试（`tests/test_api.py`）**：
```python
# tests/test_api.py
import pytest
import tempfile
import os
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_runs_empty():
    response = client.get("/runs")
    assert response.status_code == 200
    data = response.json()
    assert "runs" in data
    assert "total" in data

def test_get_nonexistent_run():
    response = client.get("/runs/99999")
    assert response.status_code == 404

def test_trigger_run_file_not_found():
    response = client.post("/run", json={
        "input_file": "/nonexistent/file.txt",
        "format": "txt"
    })
    assert response.status_code == 404

def test_trigger_run_success():
    # 创建临时测试文件
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as f:
        f.write("ok\nblur\nok\nbad\n")
        tmp_path = f.name
    
    try:
        response = client.post("/run", json={
            "input_file": tmp_path,
            "format": "txt",
            "dedup": True
        })
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["processed_count"] == 3  # ok, blur, bad（去重后）
    finally:
        os.unlink(tmp_path)
```

运行测试：
```bash
pytest tests/test_api.py -v
```

---

## 验收标准

- [ ] `POST /run` 能真正调用处理逻辑，结果写入 SQLite
- [ ] `GET /runs` 从 SQLite 返回真实历史记录
- [ ] 文件上传接口能接收文件并处理
- [ ] 文件不存在时返回 404，格式错误时返回 400
- [ ] `test_health`、`test_list_runs`、`test_trigger_run` 三个测试全部通过

---

## ⚠️ 最容易踩的坑

1. **没清理临时文件** — 文件上传场景下，临时文件必须用 `try/finally` 确保清理
2. **测试依赖真实文件** — 用 `tempfile.NamedTemporaryFile` 创建测试文件
3. **数据库路径硬编码** — 测试时会修改真实数据库，建议测试用独立的临时 db

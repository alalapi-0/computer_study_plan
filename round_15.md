# Round 15 · FastAPI 基础

> **定位**（路线 B 第 2 步）：把接口真正做成一个能接收路径参数、查询参数、请求体，并且有清晰数据模型和自动文档的最小 API。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | Path Parameters + Query Parameters + Request Body + Pydantic BaseModel |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 14 |
| **下一轮** | Round 16 · API 与数据层结合 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能把 `GET /runs/{id}` 这种路径参数接口写稳
- [ ] 能把 `skip`、`limit`、`keyword` 这类查询参数接进接口
- [ ] 能用请求体接收一次处理任务的参数
- [ ] 能用 Pydantic 模型把输入输出结构固定下来
- [ ] `/docs` 里有更清楚的接口说明和示例数据

---

## 本轮不学什么

> 先不碰：依赖注入深水区、认证授权、数据库会话管理、文件上传、后台任务、复杂错误处理、自定义响应类

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [FastAPI – Path Parameters](https://fastapi.tiangolo.com/tutorial/path-params/) | 路径参数的类型转换和校验 |
| 📄 文档 2 | [FastAPI – Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/) | 非路径参数自动识别为 query param |
| 📄 文档 3 | [FastAPI – Request Body](https://fastapi.tiangolo.com/tutorial/body/) | POST 请求体 + Pydantic 模型 |
| 📄 文档 4 | [FastAPI – Declare Request Example Data](https://fastapi.tiangolo.com/tutorial/schema-extra-example/) | 给 /docs 增加示例数据 |
| 📄 文档 5 | [Pydantic – Models](https://docs.pydantic.dev/latest/) | 类型提示驱动的数据验证 |
| 🚀 运行时 | [Uvicorn](https://www.uvicorn.org/) | 命令行是最简单的启动方式 |

---

## 本轮建议接口集合

```
GET  /health              → 最小可观察性
GET  /runs                → 带 skip/limit 分页
GET  /runs/{run_id}       → run_id 必须是整数
POST /run                 → 接收请求体，调用处理逻辑
```

---

## 3 周学习安排

### 第 1 周：路径参数和查询参数（读接口）

**目标**：把读接口写稳，练两种最常见的参数来源。

**FastAPI 关键规则**：
- 路径参数：声明在路径里，如 `/runs/{run_id}`，会做类型转换和校验
- 查询参数：不在路径里的函数参数，自动识别为 query param
- 两种都有类型提示时会自动校验，非法值返回清楚的错误信息

---

### 第 2 周：请求体和 Pydantic 模型

**目标**：用 Pydantic 定义清晰的输入输出结构。

**Pydantic 关键功能**：
- 自动做类型验证，错误时返回 422 Unprocessable Entity
- 自动生成 JSON Schema，FastAPI 用来生成 `/docs`
- 支持默认值、可选字段、字段校验器

---

### 第 3 周：示例数据和完善文档

**目标**：让 `/docs` 里的文档对别人有实际参考价值。

---

## 本轮练习清单

### 准备工作

```bash
pip install fastapi uvicorn pydantic
```

---

### 第 1 周练习

**练习 1**：路径参数
```python
# api/routers/runs.py
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/runs", tags=["runs"])

# 模拟数据（后续接 SQLite）
FAKE_RUNS = {
    1: {"id": 1, "input_file": "data.txt", "processed_count": 85},
    2: {"id": 2, "input_file": "labels.csv", "processed_count": 42},
}

@router.get("/{run_id}")
def get_run(run_id: int):
    """
    获取某次运行详情。
    - **run_id** 必须是整数，传入非整数时会自动返回 422 错误
    """
    if run_id not in FAKE_RUNS:
        raise HTTPException(status_code=404, detail=f"Run {run_id} not found")
    return FAKE_RUNS[run_id]
```

**练习 2**：查询参数
```python
@router.get("")
def list_runs(
    skip: int = 0,
    limit: int = 20,
    format: str | None = None
):
    """
    查询历史运行记录。
    - **skip**: 跳过前 n 条（分页用）
    - **limit**: 最多返回 n 条（最大 100）
    - **format**: 按输入格式筛选（可选）
    """
    runs = list(FAKE_RUNS.values())
    if format:
        runs = [r for r in runs if r.get("format") == format]
    return {
        "runs": runs[skip: skip + limit],
        "total": len(runs),
        "skip": skip,
        "limit": limit
    }
```

---

### 第 2 周练习

**Pydantic 模型定义**：
```python
# api/schemas.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RunRequest(BaseModel):
    input_file: str = Field(..., description="输入文件路径", example="input/data.txt")
    format: str = Field("txt", description="文件格式", example="txt")
    dedup: bool = Field(False, description="是否去重")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "input_file": "input/labels.txt",
                "format": "txt",
                "dedup": True
            }
        }
    }

class RunResponse(BaseModel):
    run_id: int
    status: str
    input_file: str
    processed_count: Optional[int] = None
    message: Optional[str] = None

class RunRecord(BaseModel):
    id: int
    input_file: str
    output_file: Optional[str] = None
    format: str
    original_count: int
    processed_count: int
    dedup: bool
    run_time: str
```

**POST 接口**：
```python
# api/routers/jobs.py
from fastapi import APIRouter
from schemas import RunRequest, RunResponse

router = APIRouter(prefix="/run", tags=["jobs"])

@router.post("", response_model=RunResponse)
def trigger_run(req: RunRequest):
    """
    提交一次数据处理任务。

    - 传入输入文件路径和处理参数
    - 同步执行并返回结果（后续可改为异步）
    """
    # 这一轮先 mock，下一轮接真实逻辑
    return RunResponse(
        run_id=999,
        status="completed",
        input_file=req.input_file,
        processed_count=100,
        message=f"Processed {req.input_file} with format={req.format}, dedup={req.dedup}"
    )
```

---

### 第 3 周练习

**完整 `api/main.py`**：
```python
# api/main.py
from fastapi import FastAPI
from routers import runs, jobs

app = FastAPI(
    title="AI Prep Tool API",
    description="""
AI 数据预处理工具的 HTTP 接口。

## 功能

* **health** - 服务健康检查
* **runs** - 查询历史运行记录
* **run** - 提交处理任务
""",
    version="0.2.0",
    contact={"name": "AI Prep Tool"},
)

@app.get("/health", tags=["health"])
def health():
    """服务健康检查。返回服务状态和版本。"""
    return {"status": "ok", "version": "0.2.0"}

app.include_router(runs.router)
app.include_router(jobs.router)
```

**启动和测试**：
```bash
uvicorn api.main:app --reload --port 8000

# 测试路径参数
curl http://localhost:8000/runs/1
curl http://localhost:8000/runs/abc   # 应该返回 422

# 测试查询参数
curl "http://localhost:8000/runs?skip=0&limit=5"

# 测试请求体
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"input_file": "input/data.txt", "format": "txt", "dedup": true}'
```

---

## 验收标准

- [ ] `GET /runs/{run_id}` 能正确处理整数参数，传入字符串返回 422
- [ ] `GET /runs` 支持 `skip`、`limit`、`format` 三个查询参数
- [ ] `POST /run` 接收 Pydantic 模型，缺少必填字段时返回 422
- [ ] `/docs` 里能看到每个接口的说明和示例数据
- [ ] 用 `curl` 或 `/docs` 页面能测试所有接口

---

## ⚠️ 最容易踩的坑

1. **路径参数和查询参数混淆** — 在路径里声明 `{id}` 是路径参数；普通函数参数是查询参数
2. **Pydantic 字段不加 `Field(...)`** — `...` 表示必填，不加 `...` 的字段有默认值
3. **`response_model` 漏掉** — 加上 `response_model` FastAPI 才能在文档里展示响应结构

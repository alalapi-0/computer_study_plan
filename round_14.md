# Round 14 · HTTP 与 API 设计基础

> **定位**（路线 B 第 1 步）：先把三件事讲清楚：HTTP 是什么、接口为什么这样设计、FastAPI 最小服务怎么起起来。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | HTTP 基础 + 请求方法 + 状态码 + REST 草图 + FastAPI 最小服务 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 08 或 Round 13 |
| **下一轮** | Round 15 · FastAPI 基础 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 能用自己的话解释 GET/POST/PUT/PATCH/DELETE 各适合什么场景
- [ ] 能看懂一个最小 JSON API 的请求和响应
- [ ] 能给 `ai_prep_tool` 画出第一版接口草图
- [ ] 能用 FastAPI 起一个最小服务，并看到自动生成的交互式文档

---

## 本轮不学什么

> 先不碰：鉴权、OAuth2、复杂数据库模型、异步任务队列、文件上传深水区、部署、反向代理、生产级安全

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [MDN – Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) | HTTP 是什么，客户端服务器模型 |
| 📄 文档 2 | [MDN – HTTP request methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) | GET/POST/PUT/PATCH/DELETE 语义 |
| 📄 文档 3 | [MDN – HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) | 200/201/400/404/500 等常见状态码 |
| 📄 文档 4 | [RFC 9110: HTTP Semantics](https://httpwg.org/specs/rfc9110.html) | 权威语义底座，不用整篇精读 |
| 📄 文档 5 | [FastAPI – First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) | 最小可运行 API + 自动文档 |

---

## 3 周学习安排

### 第 1 周：HTTP 基础和请求/响应直觉

**目标**：把"请求是什么、响应是什么、方法和状态码是什么意思"理顺。

**要建立的判断**（不是背术语）：
- "取状态、取列表、取详情" → 先想 GET
- "提交一次处理任务" → 先想 POST
- "对象不存在" → 404
- "参数不合法" → 4xx
- "服务端自己出错" → 5xx

---

### 第 2 周：REST 风格最小接口设计

**目标**：先为 `ai_prep_tool` 画接口草图，而不是先写代码。

**建议先设计这几类接口**：
```
GET  /health       → 看服务活着没
GET  /runs         → 看历史运行记录
GET  /runs/{id}    → 看某一次运行详情
POST /run          → 提交一次处理任务
```

---

### 第 3 周：FastAPI 最小服务

**目标**：把上周的接口草图落成能跑的最小服务。

---

## 本轮练习清单

### 第 1 周：HTTP 练习（理解为主）

**HTTP 方法速查**：

| 方法 | 语义 | 幂等 | 安全 | 常见用途 |
|------|------|------|------|---------|
| GET | 获取资源 | ✅ | ✅ | 查询、读取 |
| POST | 提交数据，创建资源 | ❌ | ❌ | 创建、提交任务 |
| PUT | 替换整个资源 | ✅ | ❌ | 完整更新 |
| PATCH | 部分修改资源 | ❌ | ❌ | 局部更新 |
| DELETE | 删除资源 | ✅ | ❌ | 删除 |

**状态码速查**：

| 范围 | 含义 | 常见例子 |
|------|------|---------|
| 2xx | 成功 | 200 OK, 201 Created |
| 3xx | 重定向 | 301 Moved Permanently |
| 4xx | 客户端错误 | 400 Bad Request, 404 Not Found |
| 5xx | 服务器错误 | 500 Internal Server Error |

**练习 1**：用 `curl` 理解 HTTP 请求
```bash
# 发送 GET 请求
curl -v https://httpbin.org/get

# 发送 POST 请求（带 JSON 数据）
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "test", "value": 42}'

# 查看响应状态码
curl -o /dev/null -s -w "%{http_code}" https://httpbin.org/status/404
```

---

### 第 2 周：接口草图

**ai_prep_tool 接口设计草图**：

```
# 健康检查
GET /health
Response: {"status": "ok", "version": "0.1.0"}

# 查询所有运行记录
GET /runs?skip=0&limit=20
Response: {"runs": [...], "total": 42}

# 查询某次运行详情
GET /runs/{run_id}
Response: {"id": 1, "input_file": "...", "processed_count": 85, ...}

# 提交一次处理任务
POST /run
Request body: {
  "input_file": "input/data.txt",
  "format": "txt",
  "dedup": true
}
Response: {"run_id": 3, "status": "completed", "processed_count": 85}
```

---

### 第 3 周练习

**安装依赖**：
```bash
pip install fastapi uvicorn
```

**练习 2**：最小 FastAPI 服务
```python
# api.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="AI Prep Tool API",
    description="AI 数据预处理工具的 HTTP 接口",
    version="0.1.0"
)

class RunRequest(BaseModel):
    input_file: str
    format: str = "txt"
    dedup: bool = False

class RunResponse(BaseModel):
    run_id: int
    status: str
    message: str

@app.get("/health")
def health():
    """服务健康检查"""
    return {"status": "ok", "version": "0.1.0"}

@app.get("/runs")
def list_runs(skip: int = 0, limit: int = 20):
    """查询历史运行记录（mock 数据）"""
    return {"runs": [], "total": 0, "skip": skip, "limit": limit}

@app.get("/runs/{run_id}")
def get_run(run_id: int):
    """查询某次运行详情（mock 数据）"""
    return {"id": run_id, "status": "not_found"}

@app.post("/run", response_model=RunResponse)
def trigger_run(req: RunRequest):
    """提交一次处理任务（mock 实现）"""
    return RunResponse(
        run_id=1,
        status="accepted",
        message=f"Will process {req.input_file}"
    )
```

**启动**：
```bash
uvicorn api:app --reload
# 访问 http://localhost:8000/docs 查看交互式文档
# 访问 http://localhost:8000/redoc 查看另一种文档视图
```

**练习 3**：用 `curl` 测试接口
```bash
# 健康检查
curl http://localhost:8000/health

# 查询运行记录
curl "http://localhost:8000/runs?skip=0&limit=5"

# 提交任务
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"input_file": "input/data.txt", "format": "txt", "dedup": true}'
```

---

## 验收标准

- [ ] 能用自己的话解释 GET/POST 的语义区别
- [ ] 能解释 200/201/404/500 各代表什么
- [ ] 已经给 `ai_prep_tool` 画出 4 个接口的草图
- [ ] FastAPI 服务能启动，`/docs` 里能看到接口并测试

---

## ⚠️ 最容易踩的坑

1. **把 POST 当成"万能方法"** — REST 里 GET 用于取数据，POST 用于提交/创建，语义很重要
2. **先写代码再设计接口** — 本轮先画草图，确认接口语义对了再写代码
3. **忽略自动文档** — FastAPI 的 `/docs` 页面非常有用，测试接口必须先用它

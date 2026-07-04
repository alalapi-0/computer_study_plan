# Round 15 · FastAPI 基础速查

## Web UI 完成路径

1. 阅读 Week 1：看懂 `FastAPI(...)`、`@app.get()` 和读接口。
2. 运行 Week 1：生成 `app/main.py`、`route_table.json`、`static_check_report.json`。
3. 阅读 Week 2：看懂请求体和 Pydantic 模型。
4. 运行 Week 2：生成 `schemas.py`、POST `/run` 和样例 JSON。
5. 阅读 Week 3：看懂文档示例、summary、tags、response_model。
6. 运行 Week 3：生成 OpenAPI 预览和文档质量报告。
7. 运行最终综合练习：生成完整 FastAPI 项目骨架。

## 最小概念表

| 概念 | 一句话 |
|---|---|
| `FastAPI(...)` | 创建 API 应用对象 |
| `@app.get("/runs")` | 把函数注册为 GET 路由 |
| 路径参数 | 路径里有 `{run_id}`，函数里写 `run_id: int` |
| 查询参数 | 不在路径里的普通函数参数，如 `skip: int = 0` |
| 请求体 | 函数参数是 Pydantic 模型，如 `req: RunRequest` |
| `response_model` | 固定接口返回结构，也帮助生成 `/docs` |
| `/docs` | FastAPI 自动生成的交互式接口文档 |

## Web UI 边界

- 自动练习生成真实 FastAPI 代码形状，但不要求安装依赖。
- 浏览器终端用于手写小文件、校验 JSON、阅读生成结果。
- 不在 Web UI 里启动 `uvicorn` 长驻进程。

## 最终验收自问

- 我能解释 `GET /runs/{run_id}` 里 `run_id` 为什么是路径参数吗？
- 我能解释 `skip`、`limit` 为什么是查询参数吗？
- 我能解释 `POST /run` 为什么应该接收 `RunRequest` 吗？
- 我能说出 `RunResponse` 对前端或调用者有什么价值吗？
- 我能说明 `/docs` 里的示例数据来自哪里吗？

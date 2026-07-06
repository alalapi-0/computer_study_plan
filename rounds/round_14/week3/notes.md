# Round 14 · Week 3 笔记（REST 路由草图）

## Web UI 学习路径

1. 阅读本文，先理解“方法 + 路径 + 请求体 + 响应体”的路由四件套。
2. 点击 `练习：生成 REST 路由草图与 mock API` 的“运行脚本”按钮。
3. 查看 `routes.json`、`mock_api.py`、`route_test_report.json`。
4. 点击自测任务的“终端练习”，自己写一个很小的路由函数。
5. 自测完成后，点击“记录并完成”记录 `r14-w3-self`。

## 本周边界

Round 14 不安装 FastAPI，也不长期启动服务。你会先用标准库写一个 in-process mock API：把“传进来的 method/path/body”路由到对应响应。这样能先把接口语义练稳，Round 15 再把它迁移成 FastAPI。

## 建议路由草图

| 方法 | 路径 | 含义 | 成功状态 |
|---|---|---|---|
| `GET` | `/health` | 服务健康检查 | `200` |
| `GET` | `/runs` | 查询运行记录列表 | `200` |
| `GET` | `/runs/{run_id}` | 查询单次运行详情 | `200` 或 `404` |
| `POST` | `/run` | 提交一次处理任务 | `201` |

## 自动练习会做什么

脚本会在 `~/cli-lab/round14/week3_auto/rest_routes` 下生成：

- `routes.json`：路由表。
- `mock_api.py`：标准库 mock API，提供 `handle_request(method, path, body)`。
- `route_tests.py`：不启动服务，直接调用函数验证路由。
- `route_test_report.json`：测试结果。

## 终端自测

在浏览器终端绑定 `r14-w3-self` 后执行：

```bash
pwd
mkdir week3_self
cd week3_self
printf 'def route(method, path):\n    if method == "GET" and path == "health":\n        return 200\n    if method == "POST" and path == "run":\n        return 201\n    return 404\nprint(route("GET", "health"))\nprint(route("POST", "run"))\n' > mini_router.py
python3 mini_router.py
cat mini_router.py
```

自测里用 `health` / `run` 代替 `/health` / `/run`，是为了避免浏览器终端安全规则误把字符串中的斜杠当作仓库外路径。自动脚本生成的合同文件会保留真实 HTTP 路径。

## 完成标准

- 能把一个接口描述为“方法 + 路径 + 请求/响应 JSON”。
- 能解释为什么 `/runs/{run_id}` 找不到时应该返回 `404`。
- 能说明 Round 14 的 mock API 和 Round 15 的 FastAPI 服务有什么关系。

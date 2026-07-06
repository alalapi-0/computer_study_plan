# Round 15 · Week 1 笔记（FastAPI 应用入口）

## Web UI 学习路径

1. 在 Round 15 页面阅读本文。
2. 点击“练习：生成 FastAPI 读接口骨架”的“运行脚本”按钮。
3. 在运行结果里确认生成了 `app/main.py`、`route_table.json` 和 `static_check_report.json`。
4. 点击“自测：自己写 mini_api_routes.py”的“终端练习”按钮，手敲下面的自测命令。
5. 自测完成后，点击“记录并完成”记录 `r15-w1-self`。

## 本周要建立的直觉

FastAPI 的最小应用入口通常长这样：

```python
from fastapi import FastAPI

app = FastAPI(title="AI Prep Tool API")

@app.get("/health")
def health():
    return {"status": "ok"}
```

关键点不是先背装饰器，而是先看清 3 层结构：

| 层 | 你要看什么 |
|---|---|
| app | `FastAPI(...)` 代表整个 API 应用 |
| route | `@app.get(...)` / `@app.post(...)` 把函数挂到 URL |
| function | 函数参数来自路径、查询参数或请求体 |

Week 1 只练读接口：

| 接口 | 参数来源 | 重点 |
|---|---|---|
| `GET /health` | 无参数 | 最小可观察性 |
| `GET /runs/{run_id}` | 路径参数 | `run_id: int` 会触发类型校验 |
| `GET /runs?skip=0&limit=20` | 查询参数 | 默认值和分页边界 |

## 自动练习会做什么

脚本会在 `~/cli-lab/round15/week1_auto/fastapi_entry` 下生成：

- `app/main.py`：真实 FastAPI 代码形状。
- `route_table.json`：把路由、参数来源和状态码列成表。
- `static_check.py`：不用安装 FastAPI，只用标准库检查代码结构。
- `static_check_report.json`：检查结果。

## 浏览器终端自测

本轮 Web UI 终端不安装依赖、不启动服务。你只需要手写一个最小路由表：

```bash
pwd
mkdir week1_self
cd week1_self
printf 'routes = [("GET", "health"), ("GET", "runs"), ("GET", "runs_by_id")]\nprint(len(routes))\nprint(routes[0][0], routes[0][1])\n' > mini_api_routes.py
python3 mini_api_routes.py
cat mini_api_routes.py
```

如果能解释“health 是无参数读接口、runs_by_id 需要路径参数”，Week 1 就过关。

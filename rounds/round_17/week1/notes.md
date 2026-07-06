# Round 17 · Week 1 笔记（APIRouter 拆分服务结构）

## Web UI 学习路径

1. 在 Round 17 页面阅读本文。
2. 点击“练习：生成 APIRouter 多文件服务结构”的“运行脚本”按钮。
3. 在运行结果里确认生成了 `api/main.py`、`api/routers/health.py`、`api/routers/runs.py`、`api/routers/jobs.py` 和 `static_check_report.json`。
4. 点击“自测：自己写 route_inventory.json”的“终端练习”按钮，手敲下面的自测命令。
5. 能解释“main 负责组装应用，router 文件按职责拆分”后，点击“记录并完成”。

## 本周要建立的直觉

Round 16 已经把 API 和数据层接起来；Round 17 要把服务整理得像一个可维护项目。第一步是把路由从一个文件拆成多个模块：

| 文件 | 职责 |
|---|---|
| `api/main.py` | 创建 `FastAPI` app，注册中间件和 router |
| `api/routers/health.py` | 健康检查，方便上线后探活 |
| `api/routers/runs.py` | 查询运行历史 |
| `api/routers/jobs.py` | 提交处理任务 |
| `api/schemas.py` | 请求/响应模型 |
| `api/config.py` | 服务配置入口 |

拆分的判断标准很简单：读 `main.py` 时应能一眼看出服务由哪些模块组成，而不是被具体业务逻辑淹没。

## 自动练习会做什么

脚本会在 `~/cli-lab/round17/week1_auto/router_layout` 下生成：

- `api/main.py`：服务入口和 `include_router`。
- `api/routers/*.py`：health / runs / jobs 三个 router。
- `api/config.py` 与 `api/schemas.py`：配置和模型位置。
- `route_inventory.json`：路由表。
- `static_check_report.json`：检查 router 拆分、API 元数据和路由表是否一致。

## 浏览器终端自测

本周终端自测只手写路由表，不安装依赖：

```bash
pwd
mkdir round17_w1_self
cd round17_w1_self
printf '{"routes":[{"method":"GET","path":"/health"},{"method":"GET","path":"/runs"},{"method":"POST","path":"/run"}]}\n' > route_inventory.json
python3 -m json.tool route_inventory.json
cat route_inventory.json
```

如果能说明这三条路由分别属于 health、runs、jobs 三类职责，Week 1 就过关。

## 外部参考

- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [FastAPI Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/)

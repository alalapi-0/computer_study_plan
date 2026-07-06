# Round 17 · Week 3 笔记（最小认证、CORS 与部署检查）

## Web UI 学习路径

1. 在 Round 17 页面阅读本文。
2. 点击“练习：生成认证、CORS 与部署检查”的“运行脚本”按钮。
3. 在运行结果里确认生成了 `api/auth.py`、`api/main.py`、`Dockerfile`、`deployment_checklist.md` 和 `static_check_report.json`。
4. 点击“自测：自己写部署前检查清单”的“终端练习”按钮，手敲下面的自测命令。
5. 能解释 Bearer token、CORS、Dockerfile 和上线前检查的边界后，点击“记录并完成”。

## 本周要建立的直觉

Round 17 的目标不是实现完整登录系统，而是知道服务上线前至少要把这些入口摆正：

| 项 | 最小要求 |
|---|---|
| Bearer token | 知道受保护接口从 `Authorization: Bearer ...` 取 token |
| `401` | token 错误时返回未认证，并带 `WWW-Authenticate: Bearer` |
| CORS | 本地调试可以宽松，生产环境应该列白名单 |
| Dockerfile | 固定工作目录、安装依赖、复制代码、暴露端口、用 uvicorn 启动 |
| Preflight | 上线前有检查表，不靠“我觉得没问题” |

本周 Web UI 终端不运行 Docker，也不启动 `uvicorn`。练习只生成和检查文件。

## 自动练习会做什么

脚本会在 `~/cli-lab/round17/week3_auto/security_deploy` 下生成：

- `api/auth.py`：Bearer token 概念示例。
- `api/main.py`：CORS 中间件配置。
- `api/routers/jobs.py`：受保护的 job route。
- `Dockerfile` 和 `requirements.txt`：部署形状。
- `deployment_checklist.md`：上线前检查表。
- `deployment_preflight_report.json`：标准库预检结果。

## 浏览器终端自测

本周终端自测只写检查清单：

```bash
pwd
mkdir round17_w3_self
cd round17_w3_self
printf 'health=ok\ncors=explicit\ntoken=replaced\ndocker_port=8000\n' > preflight.txt
grep token preflight.txt
cat preflight.txt
```

如果能说明“示例 token 不能进真实生产、CORS 不能长期用通配、Dockerfile 只是运行形状不是部署全部”，Week 3 就过关。

## 外部参考

- [FastAPI Security First Steps](https://fastapi.tiangolo.com/tutorial/security/first-steps/)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [FastAPI Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/)
- [Uvicorn Settings](https://www.uvicorn.org/settings/)
- [Docker Publishing Ports](https://docs.docker.com/network/network-tutorial-host/)

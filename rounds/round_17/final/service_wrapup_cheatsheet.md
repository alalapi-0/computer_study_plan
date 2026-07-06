# Round 17 · 服务化收口速查

## Web UI 完成顺序

1. Week 1：阅读资料，运行“APIRouter 多文件服务结构”。
2. Week 2：阅读资料，运行“配置、元数据与日志入口”。
3. Week 3：阅读资料，运行“认证、CORS 与部署检查”。
4. Final：运行“完整服务化收口项目包”。
5. 每个自测用页面“终端练习”完成后，再点击“记录并完成”记录。

## 服务化收口清单

| 类别 | 最小完成标准 |
|---|---|
| 路由结构 | `api/main.py` 只组装 app，业务路由放到 `api/routers/` |
| 配置 | 服务名、版本、数据库路径、日志级别来自 settings |
| 文档元数据 | `FastAPI(title=..., version=..., description=...)` 清楚 |
| 日志 | 有统一 `setup_logging()` 和 `get_logger()` |
| 认证 | 受保护接口显式依赖 `get_current_user` |
| CORS | 本地/生产策略分开，生产不用无限通配 |
| Docker | `WORKDIR`、依赖安装、`EXPOSE 8000`、`uvicorn api.main:app` |
| 上线前检查 | health、debug、token、CORS、端口、日志路径逐项检查 |

## 一句话边界

```text
Round 17 不是“上线生产”，而是把服务整理到可以被部署、观察和继续加固的形态。
```

## 最小通过标准

- 能在 Web UI 中打开三周笔记和本小抄。
- 四个自动练习都能通过“运行脚本”按钮生成 `static_check_report.json` 或 `round17_final_summary.json`。
- 自测能在浏览器“终端练习”完成，不需要离开页面。
- 能解释 APIRouter、settings、logging、Bearer token、CORS、Dockerfile 各自解决什么问题。

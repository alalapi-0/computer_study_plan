# Round 17 · 服务化收口

这个目录是 Round 17 的 Web UI 可完成版：用户可以在 `progress.html?round=round_17` 中阅读资料、运行服务化收口练习、打开浏览器终端做自测，并记录完成状态。

> 仓库根：`~/PycharmProjects/computer_study_plan`
> 练习沙盒：`~/cli-lab/round17`
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 路径

1. 启动本地学习服务：`python3 scripts/progress_server.py --host 127.0.0.1 --port 8777`。
2. 打开 `http://127.0.0.1:8777/progress.html?round=round_17`。
3. 每周先点击“读教程”阅读，再点击练习任务的“运行脚本”。
4. 自测任务使用页面里的“终端练习”完成，确认能解释自己的输出后点击“记录并完成”。
5. 最终验收运行综合练习，并打开小抄复盘。

## 产出路径

自动练习只写入 `~/cli-lab/round17`，不会修改仓库代码：

| 周次 | 自动产出 |
|---|---|
| Week 1 | `week1_auto/router_layout`：APIRouter 多文件服务结构 |
| Week 2 | `week2_auto/settings_logging`：环境变量配置、API 元数据和日志 |
| Week 3 | `week3_auto/security_deploy`：Bearer token、CORS、Dockerfile 和部署检查 |
| Final | `final_auto/service_wrapup_project`：完整服务化收口项目包 |

## 本轮边界

- 不在 Web UI 里安装 FastAPI / uvicorn / Docker。
- 不启动长期运行服务，不执行 `docker build` 或 `docker run`。
- 练习脚本生成真实服务代码形状，但验证使用 Python 标准库静态检查。
- 外部官方文档通过 Markdown 链接打开；本仓库不缓存第三方文档内容。

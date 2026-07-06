# Round 16 · API 与数据层结合

这个目录是 Round 16 的 Web UI 可完成版：用户可以在 `progress.html?round=round_16` 中阅读资料、运行练习脚本、打开浏览器终端做自测，并记录完成状态。

> 仓库根：`~/PycharmProjects/computer_study_plan`
> 练习沙盒：`~/cli-lab/round16`
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 路径

1. 启动本地学习服务：`python3 scripts/progress_server.py --host 127.0.0.1 --port 8777`。
2. 打开 `http://127.0.0.1:8777/progress.html?round=round_16`。
3. 每周按顺序点击“读教程”阅读，再点击练习任务的“运行脚本”。
4. 自测任务使用页面里的“终端练习”完成，确认能解释自己的输出后点击“记录并完成”。
5. 最终验收运行综合练习，并打开小抄复盘。

## 产出路径

自动练习只写入 `~/cli-lab/round16`，不会修改仓库代码：

| 周次 | 自动产出 |
|---|---|
| Week 1 | `week1_auto/api_data_layer`：POST `/run` + SQLite 写入链路 |
| Week 2 | `week2_auto/read_upload_api`：GET 列表/详情 + 上传入口 |
| Week 3 | `week3_auto/errors_and_tests`：错误合同 + TestClient 示例 |
| Final | `final_auto/api_data_layer_project`：完整 API/Data Layer 项目骨架 |

## 本轮边界

- 不在 Web UI 里安装依赖或启动 FastAPI 服务。
- 练习脚本生成 FastAPI 代码形状，但验证使用 Python 标准库静态检查和 SQLite demo。
- 外部官方文档通过 Markdown 链接打开；本仓库不缓存具体考试题目或第三方资料内容。

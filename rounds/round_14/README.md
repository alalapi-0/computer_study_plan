# Round 14 · HTTP 与 API 设计基础

Round 14 的目标是把“HTTP 请求/响应、方法、状态码、JSON 合同、REST 路由草图”讲清楚，并为下一轮 FastAPI 做准备。用户应当可以只通过 Web UI 完成阅读、运行练习脚本、浏览器终端自测、手动记录小抄和最终验收。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round14`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 完成路径

1. 启动本地服务：`python3 scripts/progress_server.py`。
2. 打开 `progress.html?round=round_14`。
3. 逐周点击“阅读”打开 notes，点击“运行”生成标准沙盒产物。
4. 对自测任务点击“终端”，在浏览器终端中手敲最小命令。
5. 最后运行综合练习，阅读并手动完成 `http_api_cheatsheet.md` 与验收解释。

## 本轮安全边界

- 所有自动脚本只写入 `~/cli-lab/round14`。
- 本轮不联网访问 `httpbin`，不执行 `curl`，不安装 `fastapi` / `uvicorn`。
- Week 3 和 final 会生成标准库 mock API 与合同检查脚本，但不会启动长期后台服务。
- 浏览器终端继续拦截 `curl`、`wget`、`pip install`、真实远程命令和仓库外路径。

## 产物地图

| 阶段 | 自动脚本产物 | 用户自测产物 |
|---|---|---|
| Week 1 | `week1_auto/http_basics/http_report.json`、方法/状态码矩阵 | 自己写 `method_quiz.txt` |
| Week 2 | `week2_auto/json_contract/api_contract.json`、请求/响应样例、合同检查脚本 | 自己写 `request.json` 并用 `python3 -m json.tool` 检查 |
| Week 3 | `week3_auto/rest_routes/mock_api.py`、路由表和 in-process 测试报告 | 自己写 `mini_router.py` |
| Final | `final_auto/ai_prep_api_design/`、接口合同、mock API、client demo、summary | 完成 HTTP/API 小抄和验收解释 |

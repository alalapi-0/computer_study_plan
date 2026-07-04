# Round 15 · FastAPI 基础

这个目录把 Round 15 做成 Web UI 可完成的 FastAPI 入门练习。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round15`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 完成路径

1. 打开 `progress.html?round=round_15`。
2. 按顺序阅读 Week 1、Week 2、Week 3 的资料。
3. 点击每个练习任务的“运行”按钮，脚本会在 `~/cli-lab/round15` 下生成 FastAPI 项目文件和静态检查报告。
4. 点击每个自测任务的“终端”按钮，在浏览器终端里手敲小文件或 JSON 检查命令。
5. 最后阅读 `final/fastapi_basics_cheatsheet.md`，再手动记录最终验收。

## 安全边界

- 本轮不要求在 Web UI 终端里执行 `pip install fastapi uvicorn`。
- 本轮不启动长期运行的 `uvicorn` 服务。
- 自动脚本会生成真实 FastAPI 代码形状，但验证方式是 Python 标准库静态检查和合同检查。
- 真正启动 FastAPI 服务属于后续可选本地实验，不作为 Web UI 完成条件。

## 产物地图

- Week 1：`week1_auto/fastapi_entry`，应用入口、health、runs 读接口。
- Week 2：`week2_auto/pydantic_body`，请求体、响应体、Pydantic 模型。
- Week 3：`week3_auto/docs_examples`，示例数据、OpenAPI 预览、文档质量检查。
- Final：`final_auto/fastapi_project`，完整 FastAPI 项目骨架和静态验收报告。

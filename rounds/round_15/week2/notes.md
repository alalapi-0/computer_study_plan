# Round 15 · Week 2 笔记（请求体与 Pydantic 模型）

## Web UI 学习路径

1. 在 Round 15 页面阅读本文。
2. 点击“练习：生成请求体和响应模型骨架”的“运行”按钮。
3. 在结果里确认生成了 `app/schemas.py`、`app/main.py`、`samples/request_run.json` 和 `model_check_report.json`。
4. 点击“自测：自己写 request_run.json”的“终端”按钮，手敲 JSON 校验命令。
5. 自测完成后，手动点击“完成”记录 `r15-w2-self`。

## 本周要建立的直觉

路径参数和查询参数适合“读”。当用户要提交一次处理任务时，参数会变多，应该放到请求体里。

Pydantic 的作用是把输入输出结构固定下来：

| 模型 | 作用 |
|---|---|
| `RunRequest` | 描述 POST `/run` 接收什么字段 |
| `RunResponse` | 描述 POST `/run` 返回什么字段 |
| `RunRecord` | 描述一条历史运行记录 |

你先记住一条：FastAPI 看到函数参数是 `req: RunRequest`，就会把它当作请求体模型，并自动生成 JSON Schema。

## 自动练习会做什么

脚本会在 `~/cli-lab/round15/week2_auto/pydantic_body` 下生成：

- `app/schemas.py`：Pydantic 模型骨架。
- `app/main.py`：包含 `POST /run` 的接口骨架。
- `samples/request_run.json`：合法请求样例。
- `samples/response_run.json`：响应样例。
- `model_check_report.json`：静态检查报告。

## 浏览器终端自测

```bash
pwd
mkdir week2_self
cd week2_self
printf '{"input_file": "input/labels.txt", "format": "txt", "dedup": true}\n' > request_run.json
python3 -m json.tool request_run.json
cat request_run.json
```

如果你能说出 `input_file` 是必填，`format` 可以有默认值，`dedup` 是布尔开关，Week 2 就过关。

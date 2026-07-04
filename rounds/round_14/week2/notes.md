# Round 14 · Week 2 笔记（JSON 请求/响应合同）

## Web UI 学习路径

1. 阅读本文，先分清“请求体”和“响应体”。
2. 点击 `练习：生成 JSON API 合同` 的“运行”按钮。
3. 查看 `api_contract.json`、`request_run.json`、`responses/*.json` 和 `contract_report.json`。
4. 点击自测任务的“终端”，自己写一个 JSON 文件并用 `python3 -m json.tool` 检查。
5. 自测完成后，手动点击“完成”记录 `r14-w2-self`。

## 你要理解的事

- 请求体是客户端给服务端的输入，例如“我要处理哪个文件，是否去重”。
- 响应体是服务端给客户端的结果，例如“run_id 是多少，当前状态是什么”。
- JSON API 要稳定：字段名、类型、错误格式都要先约定好。
- 错误响应也要有合同，不能只返回一串随意文本。

## 自动练习会做什么

脚本会在 `~/cli-lab/round14/week2_auto/json_contract` 下生成：

- `api_contract.json`：`GET /health`、`GET /runs`、`GET /runs/{run_id}`、`POST /run` 的合同草图。
- `request_run.json`：提交处理任务的请求体样例。
- `responses/*.json`：成功、列表、详情、错误响应样例。
- `validate_contract.py`：用标准库检查字段是否齐全。
- `contract_report.json`：检查结果。

## 终端自测

在浏览器终端绑定 `r14-w2-self` 后执行：

```bash
pwd
mkdir week2_self
cd week2_self
printf '{"input_file": "input.txt", "format": "txt", "dedup": true}\n' > request.json
python3 -m json.tool request.json
printf '{"error": "run_not_found", "message": "Run is missing"}\n' > error.json
python3 -m json.tool error.json
cat request.json
```

本周不要用浏览器终端发真实网络请求。先把 JSON 合同写对，下一轮再进入真实服务。

## 完成标准

- 能说出 `POST /run` 请求体至少需要哪些字段。
- 能说出成功响应和错误响应应该如何区分。
- 能用 `python3 -m json.tool` 检查自己写的 JSON 是否合法。

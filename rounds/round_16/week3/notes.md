# Round 16 · Week 3 笔记（错误响应 + API 测试）

## Web UI 学习路径

1. 在 Round 16 页面阅读本文。
2. 点击“练习：生成错误合同与 TestClient 示例”的“运行”按钮。
3. 在运行结果里确认生成了 `app/routers/jobs.py`、`tests/test_api_contract.py` 和 `static_check_report.json`。
4. 点击“自测：自己写错误状态码映射”的“终端”按钮，手敲下面的自测命令。
5. 能解释 400、404、422 分别是谁的责任后，手动点击“完成”。

## 本周要建立的直觉

API 的错误响应要让调用方能修正输入，而不是只看到一段模糊报错。最小约定：

| 场景 | 状态码 | 说明 |
|---|---:|---|
| 请求 JSON 缺必填字段 | 422 | FastAPI/Pydantic 的请求校验 |
| 输入格式不支持 | 400 | 客户端传了服务不支持的业务值 |
| 本地路径不存在 | 404 | 请求指向的输入资源找不到 |
| 运行记录不存在 | 404 | 查询的 `run_id` 不存在 |

测试也先从合同开始：给固定输入，断言状态码和 `detail.code`。这样即使将来内部实现换了，只要合同不变，调用方就不受影响。

## 自动练习会做什么

脚本会在 `~/cli-lab/round16/week3_auto/errors_and_tests` 下生成：

- `app/routers/jobs.py`：带结构化 `HTTPException` 的路由。
- `tests/test_api_contract.py`：`TestClient` 示例测试。
- `error_contract.json`：错误场景与状态码表。
- `error_simulator.py`：不用安装 FastAPI 的错误合同模拟。
- `static_check_report.json`：检查错误处理和测试断言。

## 浏览器终端自测

本周终端自测只写状态码映射：

```bash
pwd
mkdir round16_w3_self
cd round16_w3_self
printf 'def response_for(error):\n    if error == "missing":\n        return 404\n    if error == "bad_format":\n        return 400\n    return 200\nprint(response_for("missing"))\nprint(response_for("bad_format"))\n' > mini_errors.py
python3 mini_errors.py
cat mini_errors.py
```

如果输出 `404` 和 `400`，并且你能说明“422 是请求体结构校验，400 是业务值不合法，404 是资源不存在”，Week 3 就过关。

## 外部参考

- [FastAPI Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

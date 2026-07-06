# Round 15 · Week 3 笔记（示例数据与 /docs 说明）

## Web UI 学习路径

1. 在 Round 15 页面阅读本文。
2. 点击“练习：生成文档示例与 OpenAPI 预览”的“运行脚本”按钮。
3. 在结果里确认生成了 `openapi_preview.json`、`docs_examples.json` 和 `docs_quality_report.json`。
4. 点击“自测：自己写 docs_example.json”的“终端练习”按钮，手敲 JSON 示例。
5. 自测完成后，点击“记录并完成”记录 `r15-w3-self`。

## 为什么要写示例数据

FastAPI 会自动生成 `/docs`，但“自动有文档”和“文档对人有用”不是一回事。别人打开 `/docs` 时至少要看到：

| 文档信息 | 作用 |
|---|---|
| summary / docstring | 知道接口做什么 |
| request example | 知道 POST 应该传什么 |
| response_model | 知道返回结构 |
| tags | 能按模块整理接口 |

## 自动练习会做什么

脚本会在 `~/cli-lab/round15/week3_auto/docs_examples` 下生成：

- `app/schemas.py`：带 `model_config` 示例的 Pydantic 模型。
- `app/main.py`：带 summary、tags、response_model 的路由。
- `docs_examples.json`：把请求/响应示例集中列出。
- `openapi_preview.json`：不启动服务也能阅读的 OpenAPI 预览。
- `docs_quality_report.json`：检查示例和文档字段是否齐全。

## 浏览器终端自测

```bash
pwd
mkdir week3_self
cd week3_self
printf '{"summary": "Submit one run", "request_example": {"input_file": "input/demo.txt", "format": "txt", "dedup": true}}\n' > docs_example.json
python3 -m json.tool docs_example.json
cat docs_example.json
```

如果你能解释这个例子会出现在 POST `/run` 的文档里，Week 3 就过关。

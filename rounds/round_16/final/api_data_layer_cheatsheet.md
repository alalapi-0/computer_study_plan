# Round 16 · API 与数据层结合速查

## Web UI 完成顺序

1. Week 1：阅读资料，运行“POST /run + SQLite 写入链路”。
2. Week 2：阅读资料，运行“GET /runs 与上传接口”。
3. Week 3：阅读资料，运行“错误合同与 TestClient 示例”。
4. Final：运行“完整 API/Data Layer 项目骨架”。
5. 每个自测用页面终端完成后，再点击“完成”记录。

## 一条请求的主链

```text
HTTP request
  -> router 校验输入并翻译 HTTP 错误
  -> io_utils 读取 txt/csv
  -> core 执行过滤/去重
  -> output 写处理结果
  -> db 写 SQLite 运行记录
  -> response 返回 run_id 和处理数量
```

## 接口最小合同

| 接口 | 用途 | 关键返回 |
|---|---|---|
| `POST /run` | 传本地路径并处理 | `run_id`、`processed_count` |
| `POST /run/upload` | 上传文件并处理 | `run_id`、上传文件名 |
| `GET /runs` | 查询历史运行 | `runs`、`total` |
| `GET /runs/{run_id}` | 查询单次运行 | 单条 run 记录 |

## 错误约定

| 场景 | 状态码 | 建议 `detail.code` |
|---|---:|---|
| 格式不支持 | 400 | `unsupported_format` |
| 文件读取失败 | 400 | `read_failed` |
| 输入文件不存在 | 404 | `input_not_found` |
| 运行记录不存在 | 404 | `run_not_found` |
| 请求体字段缺失或类型不对 | 422 | FastAPI 默认校验错误 |

## 最小通过标准

- 能在 Web UI 中打开三周笔记和本小抄。
- 四个自动练习都能通过“运行”按钮生成 `static_check_report.json` 或 `round16_final_summary.json`。
- 自测能在浏览器终端完成，不需要离开页面。
- 能解释 API 层、核心逻辑层、数据层各自职责。

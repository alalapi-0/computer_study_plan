# Round 17 · Week 2 笔记（配置、元数据与日志）

## Web UI 学习路径

1. 在 Round 17 页面阅读本文。
2. 点击“练习：生成配置、元数据与日志入口”的“运行脚本”按钮。
3. 在运行结果里确认生成了 `api/config.py`、`api/log_utils.py`、`.env.example`、`logs/round17_week2.log` 和 `static_check_report.json`。
4. 点击“自测：自己写 .env.example 与日志 demo”的“终端练习”按钮，手敲下面的自测命令。
5. 能解释“配置不硬编码，日志有统一入口，文档元数据来自 settings”后，点击“记录并完成”。

## 本周要建立的直觉

服务化不是只会写接口，还要让服务能被不同环境配置和观察：

| 能力 | 作用 |
|---|---|
| Settings | 从环境变量 / `.env` 读取服务名、版本、数据库路径、日志级别 |
| Metadata | 让 `/docs` 展示清楚标题、版本和说明 |
| Logging | 统一格式、级别和输出位置，方便定位运行问题 |
| Debug gate | 本地可以打开 docs，生产环境默认关闭调试入口 |

本周仍然不要求安装 `pydantic-settings`。自动练习会生成真实代码形状，再用标准库检查它是否满足结构合同。

## 自动练习会做什么

脚本会在 `~/cli-lab/round17/week2_auto/settings_logging` 下生成：

- `api/config.py`：`Settings(BaseSettings)` 形状。
- `api/log_utils.py`：统一日志入口。
- `api/main.py`：使用 `settings` 填充服务元数据。
- `.env.example`：环境变量样例。
- `logging_demo.py`：标准库日志演示。
- `static_check_report.json`：检查配置字段、日志入口和 demo 输出。

## 浏览器终端自测

本周终端自测只用标准库写 `.env` 和日志：

```bash
pwd
mkdir round17_w2_self
cd round17_w2_self
printf 'APP_NAME=Demo API\nLOG_LEVEL=INFO\n' > env_example.txt
printf 'import logging\nlogging.basicConfig(filename="service.log", level=logging.INFO)\nlogging.info("service started")\nprint("service.log")\n' > log_demo.py
python3 log_demo.py
cat service.log
```

如果能说明为什么服务名、日志级别不应该散落在业务代码里，Week 2 就过关。

## 外部参考

- [FastAPI Settings and Environment Variables](https://fastapi.tiangolo.com/advanced/settings/)
- [Python logging](https://docs.python.org/3/library/logging.html)

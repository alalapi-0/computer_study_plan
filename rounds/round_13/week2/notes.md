# Round 13 · Week 2 笔记（pyproject 与配置样例）

## Web UI 学习路径

1. 阅读本文，先分清 `requirements.txt`、`pyproject.toml` 和 `.env.example` 的职责。
2. 点击 `练习：生成 pyproject 与配置样例` 的“运行脚本”按钮。
3. 查看运行结果里的 `pyproject.toml`、`.env.example`、`ai_prep_tool/settings.py` 和 `config_report.json`。
4. 点击自测任务的“终端练习”，自己读取 TOML 或 `.env.example`。
5. 自测完成后，点击“记录并完成”记录 `r13-w2-self`。

## 文件职责

| 文件 | 解决的问题 |
|---|---|
| `requirements.txt` | “安装哪些第三方包”。适合简单项目、部署环境、复现依赖。 |
| `pyproject.toml` | “这个 Python 项目是什么”。包含构建系统、项目名、版本、入口、工具配置。 |
| `.env.example` | “需要哪些环境变量”。只放示例键名和安全默认值，不放真实密钥。 |
| `.gitignore` | “哪些本地生成物不进 Git”。虚拟环境、缓存、日志、数据库、真实 `.env` 都应忽略。 |

## 自动练习会做什么

脚本会在 `~/cli-lab/round13/week2_auto/project_config` 下生成一个最小项目：

- `pyproject.toml`：用标准 `tomllib` 可解析的现代 Python 项目配置。
- `.env.example`：示例环境变量，不包含真实秘密。
- `ai_prep_tool/settings.py`：只用标准库解析 `.env.example` 的小函数。
- `README.md`：给接手者的启动说明。
- `config_report.json`：自动检查项目名、脚本入口、Python 版本、环境变量键名。

## 终端自测

在浏览器终端绑定 `r13-w2-self` 后执行：

```bash
pwd
mkdir week2_self
cd week2_self
printf '[project]\nname = "demo-tool"\nversion = "0.1.0"\n' > pyproject.toml
cat pyproject.toml
printf 'import tomllib\nfrom pathlib import Path\ncfg = tomllib.loads(Path("pyproject.toml").read_text())\nprint(cfg["project"]["name"])\n' > read_toml.py
python3 read_toml.py
printf 'APP_ENV=dev\nLOG_LEVEL=INFO\n' > .env.example
grep LOG_LEVEL .env.example
```

如果你的 Python 版本不支持 `tomllib`，可以只用 `cat` 和 `grep` 检查文件结构；自动脚本会做一次解析验证。

## 完成标准

- 能说明 `pyproject.toml` 不是拿来写真实密钥的地方。
- 能说明 `.env.example` 和真实 `.env` 的区别。
- 能解释为什么现代 Python 项目常同时存在 `requirements.txt` 与 `pyproject.toml`。

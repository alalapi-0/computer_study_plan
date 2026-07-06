# Round 13 · Week 3 笔记（Dockerfile 与发布前自检）

## Web UI 学习路径

1. 阅读本文，先理解 Dockerfile 的每一行承担什么职责。
2. 点击 `练习：生成 Dockerfile 与发布检查` 的“运行脚本”按钮。
3. 查看 `Dockerfile`、`.dockerignore`、`release_check.py` 和 `release_report.json`。
4. 点击自测任务的“终端练习”，自己写一个最小 Dockerfile 文件并用 `cat` 检查。
5. 自测完成后，点击“记录并完成”记录 `r13-w3-self`。

## 你要理解的事

- Dockerfile 是“如何把项目装进容器镜像”的说明书，不是运行日志。
- `.dockerignore` 会影响 build context，能避免把 `.venv/`、`.git/`、日志、数据库等本地生成物打进镜像。
- `EXPOSE 8000` 只是声明容器内服务端口，真正发布到宿主机还需要 `docker run -p 8000:8000 ...`。
- 当前 Web UI 练习只生成和检查 Dockerfile，不自动构建镜像；这样更稳定，也不会要求本机必须装 Docker。

## 自动练习会做什么

脚本会在 `~/cli-lab/round13/week3_auto/docker_rehearsal` 下生成：

- `Dockerfile`：最小 Python 镜像打包说明。
- `.dockerignore`：忽略虚拟环境、缓存、日志、数据库、Git 目录。
- `requirements.txt`：离线安全的空依赖清单。
- `ai_prep_tool.py`：容器默认命令会调用的最小脚本。
- `release_check.py`：标准库检查脚本，确认 Dockerfile 关键指令和 ignore 规则存在。
- `release_report.json`：检查结果。

## 终端自测

在浏览器终端绑定 `r13-w3-self` 后执行：

```bash
pwd
mkdir week3_self
cd week3_self
printf 'FROM python:3.11-slim\nWORKDIR workspace\nCOPY . .\nCMD ["python3", "app.py"]\n' > Dockerfile
printf '.venv*/\n__pycache__/\n.git/\n' > .dockerignore
cat Dockerfile
cat .dockerignore
```

不要在浏览器终端里执行 `docker build`。当前安全模型会拦截 `docker` 命令；本周重点是读懂和检查发布文件。

## 完成标准

- 能说出 `FROM`、`WORKDIR`、`COPY`、`RUN`、`CMD` 分别做什么。
- 能解释为什么 `.dockerignore` 必须忽略 `.venv/`、`.git/`、日志和数据库。
- 能说明“写好 Dockerfile”和“真正构建镜像”之间还差一个本机 Docker 环境。

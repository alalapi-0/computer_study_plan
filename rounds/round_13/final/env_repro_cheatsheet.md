# Round 13 · 环境复现与发布速查

## Web UI 完成路径

1. 在 Round 13 页面逐周阅读 notes。
2. 运行三周自动练习，确认产物都写入 `~/cli-lab/round13`。
3. 用浏览器终端完成三条自测任务，并手动记录完成。
4. 运行最终综合练习，检查 `final_auto/ai_prep_tool_release` 与 `dist/ai_prep_tool_release.zip`。
5. 对照本小抄完成 `r13-fin-sheet`，再用自己的话解释最终验收。

## 文件职责速查

| 文件 | 一句话说明 | 是否应该提交 |
|---|---|---|
| `requirements.txt` | 简单部署和复现依赖清单 | 是 |
| `pyproject.toml` | 项目元数据、构建系统、脚本入口和工具配置 | 是 |
| `.env.example` | 环境变量示例，不含真实密钥 | 是 |
| `.env` | 本机真实配置，可能含秘密 | 否 |
| `.gitignore` | 避免把本地生成物提交进 Git | 是 |
| `Dockerfile` | 容器镜像构建说明 | 是 |
| `.dockerignore` | 避免把无关文件放进 Docker build context | 是 |
| `README.md` | 接手者最先看的启动说明 | 是 |

## 复现流程口诀

1. 先看 `README.md`，知道项目入口。
2. 看 `requires-python`，确认 Python 版本。
3. 创建虚拟环境，不把 `.venv/` 提交。
4. 用 `requirements.txt` 恢复依赖。
5. 看 `.env.example`，在本机复制成 `.env`，不要提交真实 `.env`。
6. 运行发布检查脚本，再考虑 Docker build。
7. 交付时带上 README、requirements、pyproject、ignore 文件、Dockerfile 和检查清单。

## Docker 边界

本轮 Web UI 自动练习只生成和检查 Dockerfile，不执行 `docker build` / `docker run`。真正构建镜像前要确认：

- 本机 Docker 已安装并运行。
- Dockerfile 没有复制 `.env`、`.venv/`、`.git/`、数据库和日志。
- 镜像默认命令不会误删或覆盖本机文件。
- 如果要发布端口，明确写出 `-p 主机端口:容器端口`。

## 最终验收自问

- 我能否解释 `requirements.txt` 与 `pyproject.toml` 的区别？
- 我能否说出 `.env.example` 为什么可以提交，而 `.env` 为什么不该提交？
- 我能否指出 Dockerfile 中 `FROM`、`WORKDIR`、`COPY`、`RUN`、`CMD` 的作用？
- 我能否把 `~/cli-lab/round13/final_auto/ai_prep_tool_release` 交给另一个人，并说明他最少需要看哪些文件？

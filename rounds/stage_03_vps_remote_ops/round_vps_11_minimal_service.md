# Round VPS-11 · 最小 Web/API 服务部署实验

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 在 VPS 上部署最小 Web/API 服务 |
| 操作权限等级 | **Level 4** |
| 是否需要用户授权 | **是**（必须） |
| 前置 | [VPS-10](round_vps_10_remote_api_minimal.md) |
| 下一轮 | [VPS-12](round_vps_12_sop_and_vultragent.md) |

## 目标

- 部署一个**最小**服务（FastAPI / Flask / Express 任选其一，本文档示例采用 FastAPI）。
- **默认仅监听 `127.0.0.1`**，对公网开放需走单独 Level 4 二次确认。
- 用 tmux 或前台方式运行，systemd 暂不引入（systemd 属 Level 5）。
- 通过 `curl` 自测；记录端口、日志、启停、回滚。

## 用户授权请求范例

```
本轮将进行 Level 4 最小 Web/API 服务部署实验。
计划：
- 在 ~/study/<repo_name> 中部署一个最小 FastAPI 服务。
- 默认仅监听 127.0.0.1:8000。
- 使用 tmux 会话 study_service 管理。
- 用 curl 在 VPS 内部自测。
- 不开放公网端口、不安装 Nginx、不绑定域名、不配置 HTTPS。
请确认是否执行。
如需公网访问，请单独说明，我会再次发起 Level 4 二次确认。
```

## 涉及文件

- 远程：
  - `~/study/<repo_name>/app.py`
  - `~/study/<repo_name>/.env`
  - `~/study/<repo_name>/logs/service.log`
- 本地：`rounds/stage_03_vps_remote_ops/outputs/service_deploy_record_template.md`

## 操作权限等级

- 等级：**Level 4**

## 部署预检（执行前必须确认）

- 使用哪个仓库：`~/study/<repo_name>`
- 部署目录：`~/study/<repo_name>`
- 监听端口：`127.0.0.1:8000`（默认；公网另议）
- 启动命令：`uvicorn app:app --host 127.0.0.1 --port 8000`
- 停止命令：`tmux kill-session -t study_service` 或 `Ctrl+C`
- 回滚方式：`git reset --hard <known_good_commit>` + 重启服务
- 日志路径：`~/study/<repo_name>/logs/service.log`

## 学习内容

- 最小 FastAPI / Flask 服务结构
- ASGI / uvicorn 基础概念
- 监听地址绑定：`127.0.0.1` vs `0.0.0.0`
- `curl` 自测：`curl http://127.0.0.1:8000`
- tmux 管理服务：detach 后服务仍存活
- 日志落盘：服务 stdout 重定向到文件 / Python logging 配置
- 失败处理：端口占用、依赖缺失、import 错误

## 最小 FastAPI 应用骨架（`app.py`，占位）

```python
import logging
from fastapi import FastAPI

app = FastAPI(title="VPS-11 minimal service")

logging.basicConfig(
    filename="logs/service.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


@app.get("/")
def root():
    logging.info("GET /")
    return {"status": "ok", "message": "hello vps"}


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
```

## 命令示例

```bash
ssh your_user@your_server_alias

cd ~/study/<repo_name>
mkdir -p logs

source .venv/bin/activate
pip install fastapi uvicorn

# 在 tmux 中启动
tmux new -s study_service
uvicorn app:app --host 127.0.0.1 --port 8000

# detach: Ctrl+b 然后 d

# 自测（VPS 内部）
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/healthz

# 查看日志
tail -n 20 logs/service.log

# 停止
tmux attach -t study_service
# 在会话内 Ctrl+C
# 或：
tmux kill-session -t study_service

deactivate
exit
```

## 服务部署记录模板（建议字段）

```markdown
# Service Deploy Record · YYYY-MM-DD

- 服务器别名：your_server_alias
- 仓库：~/study/<repo_name>
- 服务名：study_service
- 启动命令：uvicorn app:app --host 127.0.0.1 --port 8000
- 监听地址：127.0.0.1:8000
- 是否对外开放：[ ] 否（默认必勾）
- tmux 会话：study_service
- curl 自测结果：HTTP 200 / 内容（脱敏）______
- 日志路径：~/study/<repo_name>/logs/service.log
- 停止方式：tmux kill-session -t study_service
- 回滚方式：git reset --hard <commit> + 重启
- 异常 / 错误：______
```

## 验收标准

- [ ] 服务能启动并响应 `curl http://127.0.0.1:8000/`。
- [ ] 服务默认仅监听 `127.0.0.1`，未对公网开放。
- [ ] 端口、日志路径、启动命令、停止命令、回滚命令均已记录。
- [ ] tmux 中 detach → attach 不丢失服务。
- [ ] 服务可被稳定停止。
- [ ] 安全 / 远程操作 / 项目验收三份 checklist 已逐项打勾。

## 风险与禁止事项

- **默认不开放公网**。如需开放，必须发起单独 Level 4 二次确认（含具体端口、防火墙规则、回滚方案）。
- 不默认安装 Nginx；不绑定真实域名；不配置 HTTPS（这些属 Level 5）。
- 不设置开机自启（systemd 属 Level 5）。
- 不暴露含真实 Key 的端点。
- 不让服务直接读 `~/.ssh/`、`/etc/` 等敏感目录。

## 输出物

- 一份脱敏后的服务部署记录。
- `~/study/<repo_name>/logs/service.log` 的快照（日志样例，已脱敏）。

## 下一轮接口

VPS-12 将把 VPS-00 ~ VPS-11 的全部经验沉淀成 SOP，并写出 `VULTRagent` 的 MVP 需求草案。

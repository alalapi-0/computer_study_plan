# Round VPS-10 · 远程 API 调用最小实验

## 概览

| 项目 | 内容 |
|---|---|
| 主题 | 在 VPS 上跑通最小 API 调用脚本 |
| 操作权限等级 | **Level 3** |
| 是否需要用户授权 | **是**（必须） |
| 前置 | [VPS-09](round_vps_09_network_check.md) |
| 下一轮 | [VPS-11](round_vps_11_minimal_service.md) |

## 目标

- 在 VPS 的虚拟环境中安装最小依赖（`requests`、`python-dotenv`）。
- 用 `.env` 保存 API Key，但 `.env` **只在服务器**，绝不进 Git。
- 跑通一次 API 调用，处理常见错误码。
- 把请求与响应（脱敏后）写入日志。

## 用户授权请求范例

```
本轮将进行 Level 3 远程 API 调用实验。
计划：
- 在 ~/study/<repo_name> 下创建 venv 并安装 requests / python-dotenv。
- 使用 .env 保存 API Key（仅在 VPS 本地，不进入 Git）。
- 运行最小 API 调用脚本，读取响应并写入日志。
不会安装系统级依赖，不会启动公网服务。
请确认是否执行，并指定要调用的 API 端点（占位 `your_api_endpoint`）。
```

## 涉及文件

- 远程：
  - `~/study/<repo_name>/.venv/`
  - `~/study/<repo_name>/.env`（**不进入 Git**）
  - `~/study/<repo_name>/.env.example`（可进入 Git）
  - `~/study/<repo_name>/scripts/api_test.py`（脚本骨架）
  - `~/study/<repo_name>/logs/api_test_YYYYMMDD.log`
- 本地：`rounds/stage_03_vps_remote_ops/outputs/remote_api_record_template.md`

## 操作权限等级

- 等级：**Level 3**

## 学习内容

- Python venv：`python3 -m venv .venv` 和 `source .venv/bin/activate`
- `python-dotenv`：从 `.env` 读取环境变量，避免在命令行写明文 Key
- HTTP 请求：`requests.get/post`、headers、timeout
- 错误码处理：401 / 403 / 429 / 500 的不同重试策略（429 应退避，500 应记录原因）
- 日志：把请求时间、状态码、耗时、错误信息写文件，**不写真实 Key**

## `.env.example`（仓库可提交版本）

```ini
# .env.example —— 不要写真实 Key
API_BASE_URL=https://example.com
API_KEY=your_api_key_here
API_TIMEOUT=15
```

## 最小 API 调用脚本骨架（`api_test.py`，占位）

```python
import logging
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://example.com")
API_KEY = os.getenv("API_KEY", "your_api_key_here")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "15"))

logging.basicConfig(
    filename="logs/api_test.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def call_api():
    headers = {"Authorization": f"Bearer {API_KEY}"}
    started = time.time()
    try:
        resp = requests.get(API_BASE_URL, headers=headers, timeout=API_TIMEOUT)
        elapsed = round(time.time() - started, 3)
        logging.info("status=%s elapsed=%ss", resp.status_code, elapsed)

        if resp.status_code == 200:
            print("OK")
        elif resp.status_code == 401:
            logging.error("401 Unauthorized: 检查 API_KEY 是否正确")
        elif resp.status_code == 403:
            logging.error("403 Forbidden: 区域 / 权限问题")
        elif resp.status_code == 429:
            logging.error("429 Too Many Requests: 被限流，应退避重试")
        elif resp.status_code >= 500:
            logging.error("5xx: 服务端问题，记录后稍后重试")
        else:
            logging.warning("Unexpected status: %s", resp.status_code)
    except requests.Timeout:
        logging.error("Timeout after %ss", API_TIMEOUT)
    except requests.RequestException as e:
        logging.exception("RequestException: %s", e)


if __name__ == "__main__":
    call_api()
```

## 命令示例

```bash
ssh your_user@your_server_alias

cd ~/study/<repo_name>
mkdir -p logs scripts

# 创建 venv
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install requests python-dotenv

# 复制示例 env，并在 VPS 本地填入真实 Key（不要 commit）
cp .env.example .env
$EDITOR .env

# 运行最小调用
python scripts/api_test.py

# 查看日志
tail -n 20 logs/api_test.log

deactivate
exit
```

## 远程 API 调用记录模板（建议字段）

```markdown
# Remote API Record · YYYY-MM-DD

- 服务器别名：your_server_alias
- 仓库：~/study/<repo_name>
- 依赖：requests / python-dotenv（pip 列表已记录）
- 调用端点（脱敏，仅写域名或别名）：______
- 状态码：200 / 401 / 403 / 429 / 500
- 耗时：__ s
- 错误信息（脱敏）：______
- 是否在仓库内出现真实 Key：[ ] 否（默认必勾）
- 日志路径：~/study/<repo_name>/logs/api_test.log
- 后续是否需要重试 / 排查：______
```

## 验收标准

- [ ] 在 VPS 上能成功跑通最小 API 调用。
- [ ] `.env` 仅存在于 VPS 本地，未被 commit。
- [ ] `.env.example` 在仓库中，且**不含真实 Key**。
- [ ] 至少识别出 401 / 403 / 429 / 500 中的一类（实际命中或文档复述均可）。
- [ ] 日志已落盘，记录中**不含真实 Key**。
- [ ] 安全 / 远程操作两份 checklist 已逐项打勾。

## 风险与禁止事项

- 不在仓库 / 文档 / commit message 中写真实 API Key。
- 不在命令行参数中明文传递 Key。
- 不安装系统级依赖（仅在 venv 中安装）。
- 不启动公网服务。
- 不让脚本默认 `print(API_KEY)`。

## 输出物

- 远程 API 调用记录（脱敏）。
- `.env.example` 与脚本骨架的目录约定。

## 下一轮接口

VPS-11 将基于本轮经验，部署一个最小 Web/API 服务（默认仍只监听 127.0.0.1）。

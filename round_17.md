# Round 17 · 服务化收口

> **定位**（路线 B 第 4 步/收口）：把前面做出来的 API，整理成一个更像正式服务的形态：多文件结构、配置管理、日志规范、最小认证概念、Docker 运行。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | APIRouter + Pydantic Settings + 元数据 + 最小认证概念 + CORS + Uvicorn/Docker |
| **难度** | ⭐⭐⭐⭐☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 16 |
| **下一轮** | Round 18 · 数值计算与数据分析前置（路线 C） |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] FastAPI 服务不再把所有路由都塞在一个文件里，用 `APIRouter` 按模块组织
- [ ] 配置从环境变量读取（`Pydantic Settings`）
- [ ] 日志有统一入口和清晰级别
- [ ] 知道最小认证通常从 Bearer token 模式开始
- [ ] 能用 Uvicorn 和 Docker 跑起服务
- [ ] 有一份"上线前至少检查什么"的清单

---

## 本轮不学什么

> 先不碰：完整 JWT 登录系统、复杂 RBAC、反向代理 HTTPS 证书、生产级多实例集群、监控告警平台

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [FastAPI – Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/) | APIRouter 多文件结构 |
| 📄 文档 2 | [FastAPI – Settings and Env Variables](https://fastapi.tiangolo.com/advanced/settings/) | 从环境变量读取配置 |
| 📄 文档 3 | [FastAPI – Metadata and Docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/) | 自定义文档标题/描述 |
| 📄 文档 4 | [FastAPI – Security First Steps](https://fastapi.tiangolo.com/tutorial/security/first-steps/) | OAuth2 Password + Bearer token |
| 📄 文档 5 | [FastAPI – CORS](https://fastapi.tiangolo.com/tutorial/cors/) | 最小 CORS 配置 |
| 📄 文档 6 | [FastAPI – Deployment Concepts](https://fastapi.tiangolo.com/deployment/concepts/) | HTTPS/启动/重启/进程数 |
| 🚀 运行时 | [Uvicorn – Settings](https://www.uvicorn.org/settings/) | 命令行配置 |
| 🐳 容器 | [Docker – Publishing ports](https://docs.docker.com/network/network-tutorial-host/) | `-p` 端口发布 |

---

## 建议的项目结构

```
ai_prep_tool/
├─ api/
│  ├─ main.py
│  ├─ routers/
│  │  ├─ health.py
│  │  ├─ runs.py
│  │  └─ jobs.py
│  ├─ schemas.py
│  ├─ config.py       # Pydantic Settings
│  └─ log_utils.py
├─ core.py
├─ io_utils.py
├─ db.py
├─ tests/
├─ Dockerfile
├─ requirements.txt
├─ pyproject.toml
└─ README.md
```

---

## 3 周学习安排

### 第 1 周：用 APIRouter 拆分路由

**目标**：把所有路由按职责拆到不同文件里。

**APIRouter 基本用法**：
```python
# api/routers/health.py
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
def health():
    return {"status": "ok"}
```

```python
# api/main.py
from fastapi import FastAPI
from routers import health, runs, jobs

app = FastAPI()
app.include_router(health.router)
app.include_router(runs.router)
app.include_router(jobs.router)
```

---

### 第 2 周：环境变量配置 + 日志 + API 元数据

**目标**：配置不再硬编码，日志统一，文档更专业。

**Pydantic Settings**：
```python
# api/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "AI Prep Tool"
    app_version: str = "0.3.0"
    db_path: str = "runs.db"
    log_level: str = "INFO"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

用法：
```bash
# .env 文件
APP_NAME=AI Prep Tool
LOG_LEVEL=DEBUG
DEBUG=true
```

---

### 第 3 周：最小认证 + CORS + Docker 运行

**目标**：加最小认证概念，服务能在容器里跑。

---

## 本轮练习清单

### 第 1 周练习

**完整路由拆分**：

```python
# api/routers/health.py
from fastapi import APIRouter
from api.config import settings

router = APIRouter(tags=["health"])

@router.get("/health")
def health():
    """服务健康检查"""
    return {"status": "ok", "version": settings.app_version}
```

```python
# api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import health, runs, jobs
from api.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI 数据预处理服务",
    openapi_tags=[
        {"name": "health", "description": "服务状态"},
        {"name": "runs", "description": "查询运行历史"},
        {"name": "jobs", "description": "提交处理任务"},
    ]
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(runs.router)
app.include_router(jobs.router)
```

---

### 第 2 周练习

**最小 Bearer token 认证（概念级）**：
```python
# api/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 这里只是概念演示，不是真实的 token 校验
VALID_TOKENS = {"secret-dev-token"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    if token not in VALID_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "dev-user"}
```

在接口上加认证：
```python
@router.post("", response_model=RunResponse)
def trigger_run(
    req: RunRequest,
    current_user: dict = Depends(get_current_user)  # 加这一行
):
    ...
```

---

### 第 3 周练习

**更新 `Dockerfile`（带端口）**：
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 代码
COPY . .
RUN mkdir -p input output logs

# 端口
EXPOSE 8000

# 以 uvicorn 启动
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**构建和运行**：
```bash
# 构建
docker build -t ai-prep-api:latest .

# 运行（发布端口）
docker run -p 8000:8000 ai-prep-api:latest

# 带环境变量运行
docker run -p 8000:8000 \
  -e LOG_LEVEL=DEBUG \
  -e DEBUG=true \
  ai-prep-api:latest

# 访问 /docs
open http://localhost:8000/docs
```

**上线前检查清单**：

```markdown
## 上线前检查清单

- [ ] 所有接口有错误处理（HTTPException）
- [ ] 日志级别正确（生产用 INFO，不要 DEBUG）
- [ ] `.env` 里的敏感配置不在 Git 里
- [ ] 端口已发布（-p 8000:8000）
- [ ] 容器能正常重启（考虑 --restart=always）
- [ ] /health 接口可以访问
- [ ] API 文档可以访问 /docs
- [ ] 至少有 health 和 run 接口的测试通过
```

---

## 验收标准

- [ ] 路由按 `health.py`/`runs.py`/`jobs.py` 拆分，主文件只做 `include_router`
- [ ] 配置从 `.env` 读取，不硬编码
- [ ] CORS 已配置（debug 模式 allow_origins=["*"]）
- [ ] 能理解 Bearer token 认证的基本原理
- [ ] `docker build` + `docker run -p 8000:8000` 服务能正常跑
- [ ] `/docs` 可以访问，所有接口文档清晰

---

## ⚠️ 最容易踩的坑

1. **项目结构乱再加 APIRouter** — 先把结构整理清楚，再拆路由
2. **把 `.env` 提交进 Git** — `.env` 一定要在 `.gitignore` 里
3. **Docker 忘了 `--host 0.0.0.0`** — 不加这个，容器内部的服务外部无法访问

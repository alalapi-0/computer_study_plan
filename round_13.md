# Round 13 · 环境复现与发布基础

> **定位**（路线 A 第 5 步）：把工具从"只能在你当前机器上跑"的状态，推进到"换一台机器也能较稳定复现"的状态，并学会最小 Docker 打包。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | venv 规范化 + requirements.txt + pyproject.toml + 最小 Dockerfile |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 12 |
| **下一轮** | Round 14 · HTTP 与 API 设计基础（路线 B） |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 规范使用 venv，项目有可重建的依赖清单
- [ ] 知道 `pyproject.toml` 在现代 Python 项目里的角色
- [ ] 能写出最小 Dockerfile，本地 build 并 run
- [ ] 有一份"项目交付给别人时，最少该给哪些文件"的清单

---

## 本轮不学什么

> 先不碰：PyPI 正式发布、多阶段镜像优化、Kubernetes、CI/CD 自动发布、复杂镜像安全加固

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Python – venv](https://docs.python.org/3/library/venv.html) | 创建虚拟环境 |
| 📄 文档 2 | [PyPA – Virtual Environments](https://packaging.python.org/en/latest/tutorials/installing-packages/#creating-virtual-environments) | 创建/激活/使用虚拟环境 |
| 📄 文档 3 | [pip – requirements file](https://pip.pypa.io/en/stable/reference/requirements-file-format/) | 定义可重建的依赖 |
| 📄 文档 4 | [PyPA – pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | 现代 Python 项目配置文件 |
| 📄 文档 5 | [Docker – Dockerfile reference](https://docs.docker.com/engine/reference/builder/) | 构建镜像的指令文件 |
| 📄 文档 6 | [Docker – Publishing ports](https://docs.docker.com/network/network-tutorial-host/) | 容器端口发布 |

---

## 3 周学习安排

### 第 1 周：venv 规范化 + requirements.txt

**目标**：项目有可重建的虚拟环境和依赖清单。

**标准流程**：
```bash
# 创建虚拟环境
python -m venv venv

# 激活（macOS/Linux）
source venv/bin/activate

# 安装依赖
pip install fastapi uvicorn pytest

# 导出依赖清单
pip freeze > requirements.txt

# 验证：在另一个环境里重建
python -m venv venv_test
source venv_test/bin/activate
pip install -r requirements.txt
```

---

### 第 2 周：pyproject.toml 基础认知

**目标**：知道 `pyproject.toml` 是什么，以及为什么现代 Python 项目用它。

**最小 `pyproject.toml`**：
```toml
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "ai-prep-tool"
version = "0.1.0"
description = "AI 数据预处理工具"
requires-python = ">=3.9"
dependencies = [
    "fastapi",
    "uvicorn",
]

[project.scripts]
ai-prep = "ai_prep_tool:main"
```

---

### 第 3 周：最小 Dockerfile + 本地 build/run

**目标**：第一次把项目打包进容器，并本地运行。

---

## 本轮练习清单

### 第 1 周练习

**练习 1**：venv 创建和使用
```bash
cd ~/cli-lab/round7/ai_prep_tool

# 创建虚拟环境
python -m venv venv

# 激活
source venv/bin/activate

# 确认 Python 路径在 venv 里
which python
which pip

# 安装依赖
pip install fastapi uvicorn pytest

# 查看已安装包
pip list

# 导出
pip freeze > requirements.txt
cat requirements.txt

# 退出虚拟环境
deactivate
```

**练习 2**：在新环境里重建
```bash
python -m venv venv_verify
source venv_verify/bin/activate
pip install -r requirements.txt
pip list
python -c "import fastapi; print('OK')"
deactivate
rm -rf venv_verify
```

---

### 第 2 周练习

**练习 3**：创建最小 `pyproject.toml`
```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "ai-prep-tool"
version = "0.1.0"
description = "AI 数据preprocessing tool"
readme = "README.md"
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "pytest-cov"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

---

### 第 3 周练习

**`Dockerfile`**：
```dockerfile
# Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 先复制依赖文件（利用 Docker 缓存层）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 创建必要目录
RUN mkdir -p input output logs

# 声明容器运行时要用的端口（如果有 API）
EXPOSE 8000

# 默认命令
CMD ["python", "ai_prep_tool.py", "--help"]
```

**构建和运行**：
```bash
# 构建镜像
docker build -t ai-prep-tool:latest .

# 查看镜像
docker images | grep ai-prep-tool

# 运行容器（只执行 --help 就退出）
docker run --rm ai-prep-tool:latest

# 挂载本地 input 目录（让容器访问本地文件）
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  ai-prep-tool:latest \
  python ai_prep_tool.py --input input/test.txt --format txt --dedup
```

**`.dockerignore`**：
```
venv/
__pycache__/
*.pyc
*.db
logs/
.git/
.DS_Store
```

---

## 建议的最终项目结构

```
ai_prep_tool/
├─ cli.py
├─ core.py
├─ io_utils.py
├─ config.py
├─ log_utils.py
├─ db.py
├─ pipeline.py
├─ config.ini
├─ requirements.txt
├─ pyproject.toml
├─ Dockerfile
├─ .dockerignore
├─ README.md
├─ .gitignore
├─ tests/
├─ scripts/
├─ input/
├─ output/
├─ archive/
└─ logs/
```

---

## 交付给别人时的最小清单

当你把项目交给另一个人时，至少要提供：

1. 源代码（除了 `venv/`、`output/`、`logs/`）
2. `requirements.txt` 或 `pyproject.toml`
3. `README.md`（怎么安装、怎么运行）
4. `Dockerfile`（可选，但更稳定）

---

## 验收标准

- [ ] 项目有 `venv/`（不进 Git）+ `requirements.txt`（进 Git）
- [ ] 能在全新环境里用 `pip install -r requirements.txt` 重建
- [ ] `pyproject.toml` 存在且格式正确
- [ ] `docker build` 成功，`docker run` 能输出 help 信息

---

## ⚠️ 最容易踩的坑

1. **把 `venv/` 提交进 Git** — 一定要在 `.gitignore` 里排除 `venv/`
2. **`pip freeze` 包含开发环境的系统包** — 用 `pip install --dry-run` 或 `pipreqs` 只导出项目实际依赖
3. **Dockerfile 没用 `.dockerignore`** — 会把 `venv/`、`.git/` 等都复制进镜像，导致镜像非常大

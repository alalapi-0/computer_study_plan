# Round 09 · 仓库规范化与测试入门

> **定位**（路线 A 第 1 步）：不是学新框架，而是把 `ai_prep_tool` 从"能跑的脚本"提升成"更像样的小项目"。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 仓库结构 + README + `.gitignore` + Git 分支 + pytest 测试 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 08 |
| **下一轮** | Round 10 · Python 工程化基础 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 有一个结构清晰的项目目录
- [ ] README 至少说明：项目做什么、怎么运行
- [ ] `.gitignore` 配置正确，不把日志/缓存提交进去
- [ ] 会切功能分支、合并回主分支
- [ ] 会写并运行最小 pytest 测试
- [ ] 核心逻辑变得"可测试"（纯函数，无副作用）

---

## 本轮不学什么

> 先不碰：Git rebase、复杂冲突处理、pytest fixture 深水区、CI/CD、Docker 打包、数据库和 API

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Pro Git – Branches in a Nutshell](https://git-scm.com/book/zh/v2/Git-分支-分支简介) | 分支的意义：偏离主线开发而不影响主线 |
| 📄 文档 2 | [Pro Git – Basic Branching and Merging](https://git-scm.com/book/zh/v2/Git-分支-分支的新建与合并) | 一套真实工作流：新功能 + hotfix + 合并 |
| 📄 文档 3 | [pytest – Get Started](https://docs.pytest.org/en/stable/getting-started.html) | 安装、写第一个测试、断言异常 |
| 📄 文档 4 | [pytest – How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html) | `pytest` 命令会自动发现 `test_*.py` |
| 📄 文档 5 | [GitHub Docs – README](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | README 向别人说明项目用途 |
| 📄 文档 6 | [GitHub Docs – .gitignore](https://docs.github.com/en/get-started/getting-started-with-git/ignoring-files) | 忽略文件，根目录放置共享规则 |

---

## 建议的仓库结构

```
ai_prep_tool/
├─ ai_prep_tool.py      # 主入口（后续会逐步变薄）
├─ README.md
├─ .gitignore
├─ tests/
│  ├─ __init__.py
│  ├─ test_dedup.py
│  └─ test_read.py
├─ input/
├─ output/
└─ logs/
```

---

## 3 周学习安排

### 第 1 周：整理仓库结构和基础文档

**目标**：让项目"能给别人看"。

**任务**：
1. 整理目录结构（按上方模板）
2. 写 README.md（至少含：是什么、怎么安装、怎么运行）
3. 配置 `.gitignore`（日志/缓存/输出/venv 全部排除）
4. 做一次干净的 `git commit`

---

### 第 2 周：Git 分支工作流

**目标**：会切分支做小改动，再合并。

**标准流程**：
```bash
git checkout -b feature/your-feature  # 开新分支
# ... 做改动 ...
git add .
git commit -m "描述改动"
git checkout main
git merge feature/your-feature
git branch -d feature/your-feature   # 清理分支
```

---

### 第 3 周：pytest 测试入门

**目标**：让核心逻辑变得"可测试"，并能运行测试。

**核心原则**：纯函数（无副作用）最容易测试 → 把 I/O 和逻辑分离。

---

## 本轮练习清单

### README.md 模板

```markdown
# AI Prep Tool

一个命令行数据预处理工具，支持 txt/csv/json/jsonl 格式的读取、去重和统计。

## 安装

```bash
# 建议在虚拟环境中运行
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## 使用

```bash
python ai_prep_tool.py --input input/data.txt --format txt --dedup
python ai_prep_tool.py --help
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--input` | 输入文件路径 | 必填 |
| `--output` | 输出文件路径 | `output/result.txt` |
| `--format` | 输入格式 | `txt` |
| `--dedup` | 是否去重 | False |
```

---

### .gitignore 内容

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Virtual environments
venv/
.venv/
env/

# Distribution
dist/
build/
*.egg-info/

# Project specific
output/
logs/
*.log
*.db

# macOS
.DS_Store

# IDE
.vscode/
.idea/
```

---

### 第 2 周练习

**练习 1**：模拟功能分支工作流
```bash
cd ~/cli-lab/round7/ai_prep_tool
git status

# 切新分支做改动
git checkout -b feature/improve-dedup
# ... 修改 dedup 函数 ...
git add ai_prep_tool.py
git commit -m "improve: dedup now case-insensitive"

# 合并回 main
git checkout main
git merge feature/improve-dedup
git branch -d feature/improve-dedup
git log --oneline
```

**练习 2**：模拟 hotfix 场景
```bash
# 假设主线有个 bug 需要紧急修复
git checkout -b hotfix/fix-empty-input
# ... 修复 ...
git add .
git commit -m "fix: handle empty input gracefully"
git checkout main
git merge hotfix/fix-empty-input
git branch -d hotfix/fix-empty-input
```

---

### 第 3 周练习

**练习 3**：把核心逻辑变成纯函数（可测试）

改造前（难以测试）：
```python
# 混合了 I/O 和逻辑
def process(input_path):
    with open(input_path) as f:
        records = f.read().splitlines()
    seen = set()
    result = [r for r in records if r not in seen and not seen.add(r)]
    return result
```

改造后（易于测试）：
```python
# 纯函数：只处理数据，不碰文件
def dedup_records(records: list) -> list:
    seen = set()
    result = []
    for r in records:
        if r not in seen:
            seen.add(r)
            result.append(r)
    return result

# I/O 单独处理
def read_txt(path: str) -> list:
    with open(path) as f:
        return [line.strip() for line in f if line.strip()]
```

**练习 4**：写 pytest 测试

```python
# tests/test_dedup.py
from ai_prep_tool import dedup_records

def test_dedup_basic():
    assert dedup_records(["a", "b", "a"]) == ["a", "b"]

def test_dedup_preserves_order():
    assert dedup_records(["b", "a", "b", "c"]) == ["b", "a", "c"]

def test_dedup_empty():
    assert dedup_records([]) == []

def test_dedup_no_duplicates():
    assert dedup_records(["a", "b", "c"]) == ["a", "b", "c"]

def test_dedup_all_same():
    assert dedup_records(["x", "x", "x"]) == ["x"]
```

```python
# tests/test_read.py
import pytest
from pathlib import Path
from ai_prep_tool import read_records

def test_read_txt(tmp_path):
    """使用 tmp_path fixture 创建临时文件"""
    test_file = tmp_path / "test.txt"
    test_file.write_text("line1\nline2\nline3\n")
    result = read_records(str(test_file), "txt")
    assert result == ["line1", "line2", "line3"]

def test_read_txt_empty_lines(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("line1\n\nline2\n\n")
    result = read_records(str(test_file), "txt")
    assert result == ["line1", "line2"]
```

运行测试：
```bash
pytest tests/ -v
pytest tests/ -v --tb=short   # 失败时显示简短 traceback
pytest tests/test_dedup.py -v  # 只运行指定文件
```

---

## 验收标准

- [ ] 项目有完整的 README、`.gitignore`
- [ ] 能完整演示：切分支 → 改动 → 提交 → 合并 → 删分支
- [ ] pytest 测试文件至少 5 个测试用例，全部通过
- [ ] 核心函数是纯函数，不混合 I/O

---

## ⚠️ 最容易踩的坑

1. **在 main 分支直接改代码** — 养成"新功能=新分支"的习惯
2. **pytest 找不到测试文件** — 文件名必须 `test_*.py` 或 `*_test.py`，函数名必须 `test_`
3. **测试函数依赖真实文件** — 用 `tmp_path` fixture 创建临时文件，测试完自动清理

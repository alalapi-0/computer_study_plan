# Round 10 · Python 工程化基础

> **定位**（路线 A 第 2 步）：把现有"能跑的脚本项目"，往"更像工具、结构更清楚、以后更容易扩展"的方向推进。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 模块拆分 + 配置文件 + 错误处理 + 日志整理 + CLI 参数优化 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 09 |
| **下一轮** | Round 11 · 本地持久化与数据记录 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 项目不再把大部分逻辑堆在一个脚本里，有清晰的职责分层
- [ ] 有一个明确的 CLI 入口（`cli.py`）
- [ ] 可以把运行参数放进配置文件（`config.ini`）
- [ ] 区分"给用户看的输出"和"给排查问题用的日志"
- [ ] 常见错误以更可控的方式暴露出来

---

## 本轮不学什么

> 先不碰：复杂打包发布、CI/CD、数据库、API、Docker、第三方 CLI 框架

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Python – argparse Tutorial](https://docs.python.org/3/howto/argparse.html) | CLI 参数解析，自动生成 help |
| 📄 文档 2 | [Python – Logging HOWTO](https://docs.python.org/3/howto/logging.html) | 什么时候用 logging，日志级别 |
| 📄 文档 3 | [Python – configparser](https://docs.python.org/3/library/configparser.html) | INI 风格配置文件，让用户可调整 |
| 📄 文档 4 | [Python – `__main__`](https://docs.python.org/3/library/__main__.html) | 顶层代码环境和程序入口 |
| 📄 文档 5 | [PyPA – src vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/) | 现在先用 flat，知道为什么 |
| 📄 文档 6 | [pyproject.toml 指南](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) | 现代 Python 项目配置文件 |

---

## 建议的项目结构

```
ai_prep_tool/
├─ ai_prep_tool.py   # 暂时保留，后续可逐步变薄
├─ cli.py            # 参数解析与入口
├─ core.py           # 核心处理流程
├─ io_utils.py       # 文件读写
├─ config.py         # 配置读取
├─ log_utils.py      # 日志初始化
├─ config.ini        # 用户可调整的配置
├─ README.md
├─ .gitignore
├─ tests/
├─ input/
├─ output/
└─ logs/
```

---

## 3 周学习安排

### 第 1 周：拆分入口与核心逻辑

**目标**：把项目从"一个脚本"拆成"入口 + 核心逻辑"。

**任务**：
1. 把参数解析从主脚本拿出来，放进 `cli.py`
2. 把真正的处理逻辑放进 `core.py`
3. 把文件读写放进 `io_utils.py`

---

### 第 2 周：配置文件和日志整理

**目标**：运行参数不再靠硬编码，日志开始有层次。

**任务**：
1. 用 `configparser` 读取 `config.ini`
2. 把 `print()` 换成 `logging.info()/warning()/error()`
3. 写 `log_utils.py` 统一初始化日志

---

### 第 3 周：错误处理与入口规范

**目标**：错误以可控方式暴露，而不是让程序崩溃。

**任务**：
1. 给常见错误加 `try/except`，打日志
2. 用 `if __name__ == "__main__"` 规范入口
3. 考虑是否需要 `pyproject.toml`

---

## 本轮练习清单

### 第 1 周练习

**`cli.py`**：
```python
# cli.py
import argparse

def build_parser():
    parser = argparse.ArgumentParser(
        prog="ai_prep_tool",
        description="AI 数据预处理工具"
    )
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--output", default="output/result.txt", help="输出路径")
    parser.add_argument("--format", choices=["txt", "csv", "json", "jsonl"],
                        default="txt", help="输入格式")
    parser.add_argument("--dedup", action="store_true", help="是否去重")
    parser.add_argument("--config", default="config.ini", help="配置文件路径")
    return parser

def parse_args():
    return build_parser().parse_args()
```

**`core.py`**：
```python
# core.py
import logging

logger = logging.getLogger(__name__)

def filter_records(records: list, min_length: int = 1) -> list:
    """过滤太短的记录"""
    result = [r for r in records if len(r.strip()) >= min_length]
    logger.info(f"filter_records: {len(records)} → {len(result)}")
    return result

def dedup_records(records: list) -> list:
    """去重，保持顺序"""
    seen = set()
    result = []
    for r in records:
        if r not in seen:
            seen.add(r)
            result.append(r)
    logger.info(f"dedup_records: {len(records)} → {len(result)}")
    return result

def build_summary(original: list, processed: list) -> dict:
    return {
        "original_count": len(original),
        "processed_count": len(processed),
        "removed_count": len(original) - len(processed),
    }
```

**`io_utils.py`**：
```python
# io_utils.py
import csv
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def read_records(path: str, fmt: str) -> list:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    
    records = []
    if fmt == "txt":
        with open(p) as f:
            records = [line.strip() for line in f if line.strip()]
    elif fmt == "csv":
        with open(p) as f:
            records = [json.dumps(row) for row in csv.DictReader(f)]
    elif fmt == "json":
        with open(p) as f:
            data = json.load(f)
            records = [json.dumps(item) for item in data] if isinstance(data, list) else []
    elif fmt == "jsonl":
        with open(p) as f:
            records = [line.strip() for line in f if line.strip()]
    
    logger.info(f"read_records: loaded {len(records)} from {path}")
    return records

def write_records(records: list, path: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        for r in records:
            f.write(r + "\n")
    logger.info(f"write_records: wrote {len(records)} to {path}")
```

---

### 第 2 周练习

**`config.ini`**：
```ini
[defaults]
output_dir = output
log_dir = logs
min_length = 1

[filter]
dedup = false
```

**`config.py`**：
```python
# config.py
import configparser
from pathlib import Path

def load_config(config_path: str = "config.ini") -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if Path(config_path).exists():
        config.read(config_path)
    return config

def get_output_dir(config: configparser.ConfigParser) -> str:
    return config.get("defaults", "output_dir", fallback="output")

def get_log_dir(config: configparser.ConfigParser) -> str:
    return config.get("defaults", "log_dir", fallback="logs")

def get_min_length(config: configparser.ConfigParser) -> int:
    return config.getint("defaults", "min_length", fallback=1)
```

**`log_utils.py`**：
```python
# log_utils.py
import logging
from pathlib import Path

def setup_logging(log_dir: str = "logs", level: int = logging.INFO) -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"{log_dir}/app.log")
        ]
    )
```

---

### 第 3 周练习

**重构后的 `ai_prep_tool.py`（入口文件变薄）**：
```python
# ai_prep_tool.py
from cli import parse_args
from config import load_config, get_output_dir, get_log_dir, get_min_length
from log_utils import setup_logging
from io_utils import read_records, write_records
from core import filter_records, dedup_records, build_summary
import logging

def main():
    args = parse_args()
    config = load_config(args.config)
    
    log_dir = get_log_dir(config)
    setup_logging(log_dir)
    logger = logging.getLogger(__name__)
    
    try:
        records = read_records(args.input, args.format)
    except FileNotFoundError as e:
        logger.error(str(e))
        return
    
    original = records[:]
    
    min_length = get_min_length(config)
    records = filter_records(records, min_length)
    
    if args.dedup:
        records = dedup_records(records)
    
    write_records(records, args.output)
    
    summary = build_summary(original, records)
    print("\n=== Summary ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
```

---

## 验收标准

- [ ] 项目逻辑拆分成 `cli.py`、`core.py`、`io_utils.py`、`config.py`、`log_utils.py`
- [ ] `config.ini` 能控制至少一个运行参数
- [ ] 日志用 `logging`，不再混用 `print()`
- [ ] 文件不存在等常见错误被 `try/except` 捕获，打日志后优雅退出
- [ ] `if __name__ == "__main__"` 规范入口

---

## ⚠️ 最容易踩的坑

1. **过早切 src layout** — 先把职责分清，比立刻切 src/ 子目录更有价值
2. **一次性重构所有代码** — 按职责逐步拆，每次拆完跑一遍确认没有引入错误
3. **configparser 不处理缺省值** — 永远用 `config.get(..., fallback=...)` 防止 KeyError

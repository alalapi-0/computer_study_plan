# Round 12 · 自动化流水线与批处理

> **定位**（路线 A 第 4 步）：把 CLI 工具推进成一个能批量跑、能定时跑、能保住长任务、能归档结果的小型自动化流水线。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | pathlib 批量遍历 + shutil + subprocess + crontab + nohup/tmux + 日志轮转 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 11 |
| **下一轮** | Round 13 · 环境复现与发布基础 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 工具能遍历输入目录、批量处理多个文件
- [ ] 把运行摘要归档，失败的文件单独记录
- [ ] 用 `cron` 或 shell 包装脚本定时执行
- [ ] 有基本的日志轮转（防止日志文件无限增长）
- [ ] 长任务可以用 `nohup` 或 `tmux` 保住

---

## 本轮不学什么

> 先不碰：并发队列、Celery、Airflow、复杂 systemd service、云调度平台、复杂重试框架

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Python – pathlib](https://docs.python.org/3/library/pathlib.html) | 目录遍历、路径拼接、创建输出目录 |
| 📄 文档 2 | [Python – shutil](https://docs.python.org/3/library/shutil.html) | 高层文件/目录操作，复制和归档 |
| 📄 文档 3 | [Python – subprocess](https://docs.python.org/3/library/subprocess.html) | 启动子进程，拿返回码 |
| 📄 文档 4 | [Python – logging.handlers](https://docs.python.org/3/library/logging.handlers.html) | `RotatingFileHandler` 做日志轮转 |
| 📄 文档 5 | [crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html) | 定时任务语法 |
| 📄 文档 6 | [GNU nohup](https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html) | 后台不死任务 |

---

## 建议的项目结构

```
ai_prep_tool/
├─ cli.py
├─ core.py
├─ io_utils.py
├─ config.py
├─ log_utils.py
├─ db.py
├─ pipeline.py        # ← 新增：批处理编排
├─ scripts/
│  ├─ run_batch.sh    # ← 新增：定时执行入口
│  └─ archive_reports.sh
├─ input/
├─ output/
├─ archive/           # ← 新增：归档目录
├─ logs/
└─ runs.db
```

---

## 3 周学习安排

### 第 1 周：批量遍历 + 输出命名 + 失败记录

**目标**：工具不再只处理一个文件，而是扫描目录批量处理。

**两个工程直觉**：
1. 批处理要考虑：输入扫描、输出命名、失败记录、日志、归档、可重复运行
2. 每个文件的输出要有唯一命名，不能互相覆盖

---

### 第 2 周：shutil 归档 + subprocess 调用外部命令

**目标**：批处理完成后，自动归档结果；能从脚本里调用外部命令。

---

### 第 3 周：cron 定时 + nohup/tmux 保活 + 日志轮转

**目标**：建立"本地自动化闭环"的完整感觉。

---

## 本轮练习清单

### 第 1 周练习

**`pipeline.py`**：
```python
# pipeline.py
import logging
from pathlib import Path
from datetime import datetime
from io_utils import read_records, write_records
from core import filter_records, dedup_records, build_summary
from db import init_db, insert_run

logger = logging.getLogger(__name__)

def scan_input_dir(input_dir: str, fmt: str) -> list:
    """扫描输入目录，返回匹配格式的文件列表"""
    extensions = {"txt": "*.txt", "csv": "*.csv", "json": "*.json", "jsonl": "*.jsonl"}
    pattern = extensions.get(fmt, f"*.{fmt}")
    files = list(Path(input_dir).glob(pattern))
    logger.info(f"Found {len(files)} {fmt} files in {input_dir}")
    return files

def make_output_path(input_file: Path, output_dir: str) -> Path:
    """根据输入文件名生成唯一输出路径"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = f"{input_file.stem}_{timestamp}.txt"
    return Path(output_dir) / output_name

def run_batch(
    input_dir: str,
    output_dir: str,
    fmt: str,
    dedup: bool = False,
    min_length: int = 1
) -> dict:
    """批量处理入口"""
    init_db()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    files = scan_input_dir(input_dir, fmt)
    results = {"success": [], "failed": [], "total": len(files)}
    
    for file in files:
        try:
            records = read_records(str(file), fmt)
            original = records[:]
            records = filter_records(records, min_length)
            if dedup:
                records = dedup_records(records)
            
            output_path = make_output_path(file, output_dir)
            write_records(records, str(output_path))
            
            insert_run(
                input_file=str(file),
                output_file=str(output_path),
                fmt=fmt,
                original_count=len(original),
                processed_count=len(records),
                dedup=dedup
            )
            results["success"].append(str(file))
            logger.info(f"OK: {file.name}")
        except Exception as e:
            results["failed"].append({"file": str(file), "error": str(e)})
            logger.error(f"FAILED: {file.name} - {e}")
    
    logger.info(f"Batch done: {len(results['success'])} ok, {len(results['failed'])} failed")
    return results
```

---

### 第 2 周练习

**练习 1**：shutil 归档结果
```python
# archive_demo.py
import shutil
from pathlib import Path
from datetime import datetime

def archive_output(output_dir: str, archive_dir: str) -> str:
    """把输出目录打包成 zip 归档"""
    Path(archive_dir).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"{archive_dir}/batch_{timestamp}"
    shutil.make_archive(archive_name, "zip", output_dir)
    return f"{archive_name}.zip"

# 测试
zip_path = archive_output("output", "archive")
print(f"Archived to: {zip_path}")
```

**练习 2**：subprocess 调用外部命令
```python
# subprocess_demo.py
import subprocess
import logging

logger = logging.getLogger(__name__)

def run_command(cmd: list) -> tuple:
    """运行外部命令，返回 (returncode, stdout, stderr)"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error(f"Command failed: {cmd}\n{result.stderr}")
    return result.returncode, result.stdout, result.stderr

# 测试
code, out, err = run_command(["ls", "-la", "."])
print(f"Return code: {code}")
print(out)
```

---

### 第 3 周练习

**日志轮转（`log_utils.py` 升级）**：
```python
# log_utils.py（更新版）
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(
    log_dir: str = "logs",
    level: int = logging.INFO,
    max_bytes: int = 5 * 1024 * 1024,  # 5MB
    backup_count: int = 3
) -> None:
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    file_handler = RotatingFileHandler(
        f"{log_dir}/app.log",
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            file_handler
        ]
    )
```

**`scripts/run_batch.sh`**：
```bash
#!/bin/bash
# run_batch.sh - 批量处理入口脚本

SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_DIR="$SCRIPT_DIR/input"
OUTPUT_DIR="$SCRIPT_DIR/output"
LOG_FILE="$SCRIPT_DIR/logs/batch_$(date +%Y%m%d_%H%M%S).log"

echo "[$(date)] Starting batch run" >> "$LOG_FILE"
cd "$SCRIPT_DIR"
python -c "
from pipeline import run_batch
results = run_batch('$INPUT_DIR', '$OUTPUT_DIR', 'txt', dedup=True)
print(results)
" >> "$LOG_FILE" 2>&1
echo "[$(date)] Done" >> "$LOG_FILE"
```

**设置 crontab**：
```bash
# 编辑 crontab
crontab -e

# 每天凌晨 2 点运行批处理
0 2 * * * /bin/bash ~/cli-lab/round7/ai_prep_tool/scripts/run_batch.sh

# 每小时运行一次（测试）
0 * * * * /bin/bash ~/cli-lab/round7/ai_prep_tool/scripts/run_batch.sh
```

**用 nohup 运行长任务**：
```bash
nohup python -c "
from pipeline import run_batch
run_batch('input', 'output', 'txt', dedup=True)
" > logs/nohup_run.log 2>&1 &
echo "PID: $!"
```

---

## 验收标准

- [ ] `pipeline.py` 能扫描目录、批量处理、记录成功/失败
- [ ] 日志用 `RotatingFileHandler`，有大小限制
- [ ] `run_batch.sh` 能从命令行触发批处理
- [ ] 能设置 crontab 并验证它在运行

---

## ⚠️ 最容易踩的坑

1. **批处理没有跳过已处理文件** — 生产级批处理要记录"已处理"状态，防重复
2. **日志文件无限增长** — 用 `RotatingFileHandler`，不要用普通 `FileHandler`
3. **crontab 的工作目录问题** — crontab 里的命令工作目录是 `$HOME`，用绝对路径

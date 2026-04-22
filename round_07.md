# Round 07 · 面向 AI 项目的综合练习

> **定位**：把前面学过的东西真正串起来，做一个能处理真实小数据文件、能从命令行运行、能输出结果和日志的小工具。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | pathlib + txt/csv/json/jsonl + argparse + logging |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 06 |
| **下一轮** | Round 08 · 总复盘与升级路线 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 用 `pathlib` 遍历目录、操作文件路径
- [ ] 读写 txt / csv / json / jsonl 四种格式
- [ ] 用 `argparse` 做命令行参数解析
- [ ] 用 `logging` 做日志输出（区分 print 和 log）
- [ ] 做出一个完整的"读取 → 筛选 → 去重 → 统计 → 输出"小工具 `ai_prep_tool.py`

---

## 为什么这轮对 AI 项目特别重要

后面不管做数据清洗、提示词样本整理、ASR/TTS 文本预处理、标注结果复查，本质上都逃不开：
- 遍历文件夹
- 识别文件格式，逐条读取记录
- 筛掉不需要的样本，做去重和统计
- 把结果导出为新文件
- 留一份日志，方便以后复现

---

## 本轮不学什么

> 先不碰：pandas、第三方 CLI 框架、Web 服务、数据库、模型 API、多进程并发

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📄 文档 1 | [Python – argparse Tutorial](https://docs.python.org/3/howto/argparse.html) | 标准库推荐的命令行参数解析，自动生成 help |
| 📄 文档 2 | [Python – pathlib](https://docs.python.org/3/library/pathlib.html) | 带 I/O 能力的路径对象，适合目录遍历 |
| 📄 文档 3 | [Python – csv](https://docs.python.org/3/library/csv.html) | 支持 DictReader/DictWriter |
| 📄 文档 4 | [Python – json](https://docs.python.org/3/library/json.html) | JSON 编解码 |
| 📄 文档 5 | [Python – logging HOWTO](https://docs.python.org/3/howto/logging.html) | 区分 print 和 logging 的场景 |
| 📦 格式规范 | [JSON Lines](https://jsonlines.org/) | 每行一条 JSON，适合逐条处理 |

---

## 3 周学习安排

### 第 1 周：pathlib 和多格式读写

**目标**：把"遍历目录 + 识别格式 + 逐条读取"练顺。

**本周主练**：`pathlib.Path`、`open()`、`csv.DictReader`、`json.load`、jsonl 逐行读取

---

### 第 2 周：argparse 和 logging

**目标**：让工具能从命令行调用，有日志可追溯。

**本周主练**：`argparse.ArgumentParser`、`--input`/`--output`/`--format`、`logging.getLogger`、日志级别

---

### 第 3 周：整合成完整工具

**目标**：把前两周的能力组合成一个完整的 `ai_prep_tool.py`。

**本周主练**：函数拆分、去重逻辑、统计报告、日志文件输出

---

## 本轮练习清单

### 准备工作

```bash
mkdir -p ~/cli-lab/round7/ai_prep_tool
cd ~/cli-lab/round7/ai_prep_tool
mkdir input output logs
```

---

### 第 1 周练习

**练习 1**：pathlib 基础
```python
# pathlib_demo.py
from pathlib import Path

# 创建路径对象
p = Path.home() / "cli-lab" / "round7"
print(p)
print(p.exists())

# 列出目录内容
for item in p.iterdir():
    print(f"  {item.name} ({'dir' if item.is_dir() else 'file'})")

# 按类型筛选
txt_files = list(p.glob("**/*.txt"))
print(f"\nFound {len(txt_files)} .txt files")
```

**练习 2**：读写 txt
```python
# txt_rw.py
from pathlib import Path

# 写入
output = Path("input/sample.txt")
output.write_text("line 1\nline 2\nline 3\n")

# 逐行读取
with open(output) as f:
    for i, line in enumerate(f, 1):
        print(f"{i}: {line.rstrip()}")
```

**练习 3**：读写 csv
```python
# csv_rw.py
import csv
from pathlib import Path

# 写入
rows = [
    {"id": "1", "label": "ok", "score": "0.95"},
    {"id": "2", "label": "blur", "score": "0.42"},
    {"id": "3", "label": "ok", "score": "0.88"},
]
with open("input/data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "label", "score"])
    writer.writeheader()
    writer.writerows(rows)

# 读取
with open("input/data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)
```

**练习 4**：读写 json 和 jsonl
```python
# json_rw.py
import json

# json
data = {"records": [{"id": 1, "text": "hello"}, {"id": 2, "text": "world"}]}
with open("input/data.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

with open("input/data.json") as f:
    loaded = json.load(f)
    print(loaded["records"])

# jsonl（每行一条记录）
records = [{"id": 1, "text": "hello"}, {"id": 2, "text": "world"}]
with open("input/data.jsonl", "w") as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

with open("input/data.jsonl") as f:
    for line in f:
        record = json.loads(line.strip())
        print(record)
```

---

### 第 2 周练习

**练习 5**：argparse 基础
```python
# cli_demo.py
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="数据预处理工具"
    )
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--output", default="output/result.txt", help="输出路径")
    parser.add_argument("--format", choices=["txt", "csv", "json", "jsonl"],
                        default="txt", help="输入文件格式")
    parser.add_argument("--dedup", action="store_true", help="是否去重")
    args = parser.parse_args()
    
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Format: {args.format}")
    print(f"Dedup: {args.dedup}")

if __name__ == "__main__":
    main()
```

运行：
```bash
python cli_demo.py --input input/data.csv --format csv --dedup
python cli_demo.py --help
```

**练习 6**：logging 基础
```python
# logging_demo.py
import logging
from pathlib import Path

# 配置日志（同时输出到控制台和文件）
Path("logs").mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log")
    ]
)
logger = logging.getLogger(__name__)

logger.debug("这条不会显示（低于 INFO 级别）")
logger.info("开始处理")
logger.warning("发现空字段")
logger.error("文件不存在")

print("直接 print 的内容，不会进日志文件")
```

---

### 第 3 周练习

**综合项目：`ai_prep_tool.py`**

```python
# ai_prep_tool.py
"""
AI 数据预处理工具
用法：python ai_prep_tool.py --input <path> --format <fmt> [--dedup] [--output <path>]
"""
import argparse
import csv
import json
import logging
from pathlib import Path

# ---- 日志配置 ----
def setup_logging(log_dir="logs"):
    Path(log_dir).mkdir(exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f"{log_dir}/run.log")
        ]
    )

# ---- 读取函数 ----
def read_records(path, fmt):
    """根据格式读取记录，返回 list of str"""
    records = []
    if fmt == "txt":
        with open(path) as f:
            records = [line.strip() for line in f if line.strip()]
    elif fmt == "csv":
        with open(path) as f:
            reader = csv.DictReader(f)
            records = [json.dumps(row, ensure_ascii=False) for row in reader]
    elif fmt == "json":
        with open(path) as f:
            data = json.load(f)
            if isinstance(data, list):
                records = [json.dumps(item, ensure_ascii=False) for item in data]
    elif fmt == "jsonl":
        with open(path) as f:
            records = [line.strip() for line in f if line.strip()]
    return records

# ---- 处理函数 ----
def dedup_records(records):
    seen = set()
    result = []
    for r in records:
        if r not in seen:
            seen.add(r)
            result.append(r)
    return result

def build_summary(original, processed):
    return {
        "original_count": len(original),
        "processed_count": len(processed),
        "removed_count": len(original) - len(processed),
    }

# ---- 主逻辑 ----
def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    parser = argparse.ArgumentParser(description="AI 数据预处理工具")
    parser.add_argument("--input", required=True, help="输入文件路径")
    parser.add_argument("--output", default="output/result.txt", help="输出文件路径")
    parser.add_argument("--format", choices=["txt", "csv", "json", "jsonl"],
                        default="txt", help="输入格式")
    parser.add_argument("--dedup", action="store_true", help="去重")
    args = parser.parse_args()
    
    logger.info(f"Starting: input={args.input}, format={args.format}, dedup={args.dedup}")
    
    records = read_records(args.input, args.format)
    logger.info(f"Loaded {len(records)} records")
    
    if args.dedup:
        records = dedup_records(records)
        logger.info(f"After dedup: {len(records)} records")
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        for r in records:
            f.write(r + "\n")
    logger.info(f"Output written to {args.output}")
    
    summary = build_summary(
        read_records(args.input, args.format),
        records
    )
    print("\n=== Summary ===")
    for k, v in summary.items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
```

运行测试：
```bash
# 先创建测试数据
echo "ok" > input/labels.txt
echo "blur" >> input/labels.txt
echo "ok" >> input/labels.txt
echo "bad" >> input/labels.txt

# 运行工具
python ai_prep_tool.py --input input/labels.txt --format txt --dedup
python ai_prep_tool.py --input input/labels.txt --format txt
```

---

## 验收标准

- [ ] 能用 `pathlib` 遍历目录，找到所有指定格式文件
- [ ] 能读取 txt / csv / json / jsonl 四种格式
- [ ] 能用 `argparse` 做 `--input`、`--output`、`--format`、`--dedup` 等参数
- [ ] 日志写到文件，`print` 和 `logging` 分工明确
- [ ] `ai_prep_tool.py` 能从命令行完整运行，输出处理结果和 summary

---

## ⚠️ 最容易踩的坑

1. **用 `print` 代替 `logging`** — `print` 不会写进文件、没有时间戳级别，不适合生产
2. **路径用字符串拼接** — 用 `pathlib.Path` 代替 `os.path.join`，更安全跨平台
3. **jsonl 整个 `json.load`** — jsonl 必须逐行解析，不能用 `json.load(f)` 整个读

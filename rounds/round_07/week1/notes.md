# Round 07 · Week 1 笔记（pathlib + 多格式读写）

## 本周目标

- 用 `pathlib` 建立跨平台路径操作习惯。
- 能读取 txt/csv/json/jsonl 四种常见格式。

## Web UI 学习路径

1. 在 Round 07 里打开本文件，先读完“四种格式怎么读”的差异。
2. 点击 `r07-w1-ex1` 的“运行”。脚本会在 `~/cli-lab/round7/week1_auto` 生成：
   - `labels.txt`
   - `labels.csv`
   - `labels.json`
   - `labels.jsonl`
   - `next_steps.txt`
3. 看运行输出里的 `formats`、`txt-count`、`csv-labels`、`json-count`、`jsonl-count`，确认四种格式都被读取到了。
4. 点击 `r07-w1-self` 的“终端”，在 `~/cli-lab/round7` 里自己写一个 `read_formats.py`。

## 四种格式的读取直觉

- `txt`：一行一个值，最适合先跑通流程。
- `csv`：表格数据，用 `csv.DictReader` 后每行是一个 dict。
- `json`：整个文件是一个 JSON 对象或数组，适合一次性读入。
- `jsonl`：一行一个 JSON，必须逐行 `json.loads()`，适合大文件和流式处理。

## 浏览器终端自测命令

在 `r07-w1-self` 的终端里逐条运行：

```bash
mkdir week1_self
cd week1_self
printf 'ok\nblur\nok\n' > labels.txt
printf 'id,label\n1,ok\n2,blur\n3,ok\n' > labels.csv
printf '{"records":[{"id":1,"label":"ok"},{"id":2,"label":"blur"}]}\n' > labels.json
printf '{"id":1,"label":"ok"}\n{"id":2,"label":"blur"}\n' > labels.jsonl
printf 'from pathlib import Path\nimport csv\nimport json\nbase = Path(".")\nprint(sorted(p.name for p in base.glob("labels.*")))\nprint(Path("labels.txt").read_text().splitlines())\n' > read_formats.py
printf 'with open("labels.csv", newline="") as f:\n    print([row["label"] for row in csv.DictReader(f)])\n' >> read_formats.py
printf 'print(json.loads(Path("labels.json").read_text())["records"])\nfor line in Path("labels.jsonl").read_text().splitlines():\n    print(json.loads(line)["label"])\n' >> read_formats.py
python3 read_formats.py
```

运行成功后，回到任务行手动点“记录 / 完成”。

## 本周自查

- [ ] 能写出一个遍历目录并筛选扩展名的脚本
- [ ] 能说明 json 与 jsonl 读取方式的差异
- [ ] 能解释为什么 csv 适合表格、jsonl 适合逐条处理

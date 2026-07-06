# Round 07 · Week 3 笔记（整合 ai_prep_tool）

## 本周目标

- 把前两周能力整合到一个可运行脚本。
- 完成“读取 -> 去重 -> 输出 -> 统计”最小闭环。

## Web UI 学习路径

1. 先点击本文件“读教程”，看清最终工具的函数边界。
2. 点击 `r07-w3-ex3` 的“运行脚本”。脚本会在 `~/cli-lab/round7/week3_auto` 生成：
   - `input/records.jsonl`
   - `output/processed.jsonl`
   - `output/summary.json`
   - `next_steps.txt`
3. 运行输出里应能看到 `deduped: 4 -> 3` 和 `label-stats`。
4. 点击 `r07-w3-self` 的“终端练习”，自己写一个 `mini_prep_tool.py`，完成读取、去重、统计、输出。

## 函数拆分建议

- `read_jsonl(path)`：只负责读取，不处理业务。
- `dedup_records(rows)`：只负责按 key 去重。
- `build_stats(rows)`：只负责统计 label。
- `write_jsonl(path, rows)`：只负责输出。
- `main()`：只负责把这些函数串起来。

这种拆法的好处是：后面扩展到 csv/json/txt 时，不会把所有逻辑揉成一团。

## 浏览器终端自测命令

在 `r07-w3-self` 的终端里逐条运行：

```bash
mkdir week3_self
cd week3_self
printf '{"text":"clean","label":"ok"}\n{"text":"blur","label":"blur"}\n{"text":"clean","label":"ok"}\n' > records.jsonl
printf 'import json\nfrom collections import Counter\nfrom pathlib import Path\nrows = [json.loads(line) for line in Path("records.jsonl").read_text().splitlines() if line.strip()]\nseen = set()\nprocessed = []\n' > mini_prep_tool.py
printf 'for row in rows:\n    key = (row["text"], row["label"])\n    if key not in seen:\n        seen.add(key)\n        processed.append(row)\n' >> mini_prep_tool.py
printf 'Path("processed.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\\n" for row in processed))\nstats = Counter(row["label"] for row in processed)\nprint("deduped:", len(rows), "->", len(processed))\nprint(dict(stats))\n' >> mini_prep_tool.py
python3 mini_prep_tool.py
cat processed.jsonl
```

能解释每个函数的输入输出后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能解释脚本中每个函数的输入输出
- [ ] 能独立运行一次带 `--dedup` 的处理流程
- [ ] 能解释“统计基于去重前还是去重后”的差异

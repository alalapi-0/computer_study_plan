# Round 12 · Week 1 笔记（批量遍历与失败记录）

## Web UI 学习路径

1. 在 Round 12 页面打开本文件，先看清楚批处理的 4 个角色：`input/`、`output/`、`failures.log`、`batch_report.json`。
2. 点“运行”执行 `week1/exercises.py`。脚本会在 `~/cli-lab/round12/week1_auto/batch_pipeline` 生成一个小批处理沙盒。
3. 打开“终端”，自己在 `~/round12` 下写一个最小扫描脚本，确认你能不用复制自动脚本也写出目录遍历。
4. 用“记录”写下：成功文件放哪、失败文件怎么记录、为什么输出名不能互相覆盖。

## 本周目标

- 用 `pathlib.Path.glob()` 扫描输入目录。
- 对每个输入文件生成独立输出文件。
- 把失败文件单独写入 `failures.log`，便于后续重跑。
- 用 JSON 报告保存本次批处理的成功数、失败数和输出路径。

## 最小结构

```
batch_pipeline/
├─ input/
├─ output/
├─ failures.log
├─ batch_report.json
└─ next_steps.txt
```

## 核心直觉

- 批处理不是“把 for 循环写完”就结束，还要知道哪些文件成功、哪些失败。
- 输出名要带序号或时间戳，否则多个输入文件容易覆盖同一个输出。
- 失败记录不应该只停留在屏幕输出里，必须落到文件，方便下次重跑。

## 浏览器终端自测

在 Round 12 页面点本周自测的“终端”，运行：

```bash
mkdir -p self_scan/input self_scan/output
printf 'alpha\nbeta\n' > self_scan/input/a.txt
printf 'bad\n' > self_scan/input/b.txt
printf 'from pathlib import Path\nbase=Path("self_scan")\ninput_dir=base.joinpath("input")\noutput_dir=base.joinpath("output")\nfiles=sorted(input_dir.glob("*.txt"))\nfor p in files:\n    output_dir.joinpath(p.name).write_text(p.read_text().upper(), encoding="utf-8")\nprint(len(files))\n' > self_scan/scan_demo.py
python3 self_scan/scan_demo.py
find self_scan -maxdepth 2 -type f | sort
```

看到输出文件后，再手动标记 `r12-w1-self`。

## 本周自查

- [ ] 能列出 `input/` 下待处理文件清单。
- [ ] 能说明输出命名与失败日志应该落在哪。
- [ ] 能解释“脚本成功运行”和“每个文件都处理成功”不是一回事。

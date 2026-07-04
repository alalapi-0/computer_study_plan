# Round 07 · Week 2 笔记（argparse + logging）

## 本周目标

- 让脚本具备命令行参数解析能力。
- 区分 `print` 输出与 `logging` 结构化日志。

## Web UI 学习路径

1. 先点击本文件“阅读”，理解参数和日志分别解决什么问题。
2. 点击 `r07-w2-ex2` 的“运行”。脚本会在 `~/cli-lab/round7/week2_auto` 生成：
   - `input/labels.txt`
   - `output/result.txt`
   - `logs/week2.log`
   - `next_steps.txt`
3. 运行输出里应能看到 `cli-output`、`processed`、`dedup` 和 `log-file`。
4. 点击 `r07-w2-self` 的“终端”，自己写一个带参数和日志的小脚本。

## 参数与日志的分工

- `argparse` 负责“怎么从命令行告诉程序要处理哪个文件、输出到哪里、是否去重”。
- `print` 负责给当前用户看的简短结果，比如 summary。
- `logging` 负责给未来排查看的运行记录，比如输入路径、处理条数、异常信息。
- 自动练习默认开启去重；如果命令行运行脚本，可以用 `--keep-duplicates` 保留重复行。

## 浏览器终端自测命令

在 `r07-w2-self` 的终端里逐条运行：

```bash
mkdir week2_self
cd week2_self
printf 'ok\nblur\nok\nbad\n' > labels.txt
printf 'import argparse\nimport logging\nfrom pathlib import Path\nparser = argparse.ArgumentParser(description="cli logger demo")\nparser.add_argument("--input", default="labels.txt")\nparser.add_argument("--output", default="result.txt")\nargs = parser.parse_args()\n' > cli_logger.py
printf 'Path("logs").mkdir(exist_ok=True)\nlogging.basicConfig(filename="logs/run.log", level=logging.INFO, format="%(levelname)s:%(message)s")\nlines = [line.strip() for line in Path(args.input).read_text().splitlines() if line.strip()]\n' >> cli_logger.py
printf 'Path(args.output).write_text("\\n".join(lines) + "\\n")\nlogging.info("input=%s count=%s", args.input, len(lines))\nprint("count:", len(lines))\n' >> cli_logger.py
python3 cli_logger.py --input labels.txt --output result.txt
cat logs/run.log
python3 cli_logger.py --help
```

能说明 `--input`、`--output`、默认值和日志文件后，回到任务行手动点“记录 / 完成”。

## 本周自查

- [ ] 能使用 `--input`、`--output`、`--format` 参数运行脚本
- [ ] 能把运行日志写入 `logs/` 目录
- [ ] 能说明为什么运行结果不应该只靠 `print`

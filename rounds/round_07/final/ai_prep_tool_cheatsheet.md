# Round 07 · ai_prep_tool 速查

## Web UI 完成路径

1. 点击 `r07-fin-comp` 的“运行脚本”，确认输出出现 `Summary`、`original`、`processed`、`removed`。
2. 打开本文件“读教程”，按下面的小抄检查自己是否真的理解。
3. 能说清楚读取、参数、日志、去重、输出之后，点击“记录并完成”保存 `r07-fin-sheet` 和 `r07-fin-acc1`。

## 最小命令模板

```bash
python3 comprehensive_exercise.py --input input/labels.txt --output output/result.txt --dedup
```

Web UI 自动运行时不需要参数，会默认在 `~/cli-lab/round7/final_auto` 创建演示数据：

```bash
python3 rounds/round_07/final/comprehensive_exercise.py
```

## 参数建议

- `--input`：先从 txt 开始，确保流程可跑通。
- `--output`：默认放到 `output/`，便于版本隔离。
- `--format`：支持 `txt`、`csv`、`json`、`jsonl`；不同格式最终都会转成一行一条记录。
- `--dedup`：默认开启去重；如要观察原始重复数据，可用 `--keep-duplicates`。

## 日志排查

- 日志文件：`logs/round7_final.log`
- 先看 `input` 与 `processed` 数量是否符合预期。

## 格式读取小抄

| 格式 | 读取方式 | 适合场景 |
|---|---|---|
| txt | `Path.read_text().splitlines()` | 一行一个标签或文本 |
| csv | `csv.DictReader` | 表格型标注结果 |
| json | `json.loads()` 一次读入 | 小型结构化配置或记录集合 |
| jsonl | 逐行 `json.loads(line)` | 大量样本、流式处理、训练数据 |

## 最终验收自问

- 输入文件不存在时，我希望脚本怎么报错？
- 去重 key 是整行文本，还是 `(text, label)` 这样的业务字段？
- 日志里应该记录完整数据，还是只记录路径、条数、状态？
- `print` 的 summary 给谁看？`logging` 的日志给谁看？

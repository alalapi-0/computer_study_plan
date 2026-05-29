# Round 07 · ai_prep_tool 速查

## 最小命令模板

```bash
python3 comprehensive_exercise.py --input input/labels.txt --output output/result.txt --dedup
```

## 参数建议

- `--input`：先从 txt 开始，确保流程可跑通。
- `--output`：默认放到 `output/`，便于版本隔离。
- `--dedup`：先关闭观察原始分布，再开启比较差异。

## 日志排查

- 日志文件：`logs/round7_final.log`
- 先看 `input` 与 `processed` 数量是否符合预期。

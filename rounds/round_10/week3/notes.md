# Round 10 · Week 3 笔记（错误处理与收口）

## 本周目标

- 为常见失败路径提供可控错误信息。
- 完成 Round 10 沙盒项目的最小收口检查。

## Web UI 学习路径

1. 打开本文件，先确认“错误处理”的目标不是吞掉错误，而是让用户看到可理解的信息，让日志留下可排查线索。
2. 点击 `r10-w3-ex3` 的“运行脚本”。脚本会在 `~/cli-lab/round10/week3_auto/ai_prep_tool` 生成：
   - `errors.py`
   - `core.py`
   - `ai_prep_tool.py`
   - `pyproject.toml`
   - `error_report.txt`
3. 运行结果会同时验证成功路径和缺失输入文件的错误路径。
4. 点击 `r10-w3-self` 的“终端练习”，自己写一个带返回码的入口脚本。

## 可控错误的最小形状

- 自定义一个领域错误，例如 `PrepToolError`。
- 在底层函数里发现明确错误时抛出它。
- 在入口 `main()` 里捕获它，打印用户可理解的错误，并返回非 0 状态码。
- 不要在核心函数里直接 `sys.exit()`，否则函数难测试。

## 入口规范

```python
def main() -> int:
    ...
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

这样脚本可直接运行，`main()` 也能被测试调用。

## 浏览器终端自测命令

在 `r10-w3-self` 的终端里逐条运行：

```bash
mkdir week3_self
cd week3_self
printf 'class PrepToolError(Exception):\n    pass\n\ndef main():\n    try:\n        raise PrepToolError("demo error")\n    except PrepToolError as exc:\n        print(f"error: {exc}")\n        return 2\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n' > app.py
python3 app.py
```

看到 `error: demo error` 后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能列出至少 2 种应显式处理的输入错误
- [ ] 能运行 final 综合练习并看到检查摘要
- [ ] 能解释为什么入口捕获错误，而核心函数只抛出错误

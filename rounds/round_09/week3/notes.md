# Round 09 · Week 3 笔记（pytest 入门）

## 本周目标

- 将核心逻辑改写为可测试的纯函数。
- 理解最小测试用例集合应覆盖的边界情况。

## Web UI 学习路径

1. 先点击本文件“读教程”，理解“pytest 入门”先学测试思想，不急着安装依赖。
2. 点击 `r09-w3-ex3` 的“运行脚本”。脚本会在 `~/cli-lab/round9/week3_auto` 生成：
   - `ai_prep_tool.py`
   - `tests/test_dedup.py`
   - `run_tests.py`
   - `test_report.txt`
3. 自动练习用标准库执行测试函数；文件命名保持 pytest 风格，后续真正安装 pytest 时可以继续用。
4. 点击 `r09-w3-self` 的“终端练习”，自己写 `test_dedup.py` 并运行。

## 最小测试集

- 普通重复：`["a", "b", "a"]`
- 保持顺序：`["b", "a", "b", "c"]`
- 空输入：`[]`
- 全部相同：`["x", "x", "x"]`
- 无重复：`["a", "b", "c"]`

## 浏览器终端自测命令

在 `r09-w3-self` 的终端里逐条运行：

```bash
mkdir week3_self
cd week3_self
mkdir tests
printf 'def dedup_records(items):\n    seen = set()\n    out = []\n    for item in items:\n        if item not in seen:\n            seen.add(item)\n            out.append(item)\n    return out\n' > ai_prep_tool.py
printf 'from ai_prep_tool import dedup_records\n\ndef test_basic():\n    assert dedup_records(["a", "b", "a"]) == ["a", "b"]\n\ndef test_empty():\n    assert dedup_records([]) == []\n\ndef test_order():\n    assert dedup_records(["b", "a", "b"]) == ["b", "a"]\n' > tests/test_dedup.py
printf 'import importlib.util\nfrom pathlib import Path\nspec = importlib.util.spec_from_file_location("test_dedup", Path("tests/test_dedup.py"))\nmod = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(mod)\nfor name in sorted(n for n in dir(mod) if n.startswith("test_")):\n    getattr(mod, name)()\nprint("tests: ok")\n' > run_tests.py
python3 run_tests.py
```

能解释纯函数为什么更好测后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能写出至少 3 条断言覆盖常见输入
- [ ] 能说明“逻辑与 I/O 分离”为何更易测试
- [ ] 能说明 pytest 风格文件命名与本轮标准库 runner 的关系

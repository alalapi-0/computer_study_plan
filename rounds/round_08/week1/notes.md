# Round 08 · Week 1 笔记（项目收口 + pytest）

## 本周目标

- 把 Round 07 产物整理成更稳定的小项目结构。
- 建立最小测试意识并运行第一组 `pytest` 用例。

## Web UI 学习路径

1. 在 Round 08 里打开本文件，先理解“项目收口”不是继续加功能，而是让已有功能更容易复查。
2. 点击 `r08-w1-ex1` 的“运行”。脚本会在 `~/cli-lab/round8/week1_auto/ai_prep_tool` 生成：
   - `ai_prep_tool.py`
   - `README.md`
   - `.gitignore`
   - `tests/test_basic.py`
   - `run_tests.py`
   - `test_report.txt`
3. 自动练习会用标准库执行 `run_tests.py`，不需要安装 pytest；`tests/test_basic.py` 保持 pytest 兼容风格，后续真正进入工程化路线时再安装 pytest。
4. 点击 `r08-w1-self` 的“终端”，自己写一个最小测试文件并运行。

## 为什么先收口

- README 让未来的你知道项目怎么运行。
- `.gitignore` 防止日志、数据库、输出文件混进仓库。
- `tests/` 让“我改完没坏”有可重复证据。
- `run_tests.py` 是无依赖的保底测试入口；pytest 是下一阶段更专业的入口。

## 浏览器终端自测命令

在 `r08-w1-self` 的终端里逐条运行：

```bash
mkdir week1_self
cd week1_self
printf 'def dedup_records(items):\n    seen = set()\n    out = []\n    for item in items:\n        if item not in seen:\n            seen.add(item)\n            out.append(item)\n    return out\n' > ai_prep_tool.py
mkdir tests
printf 'from ai_prep_tool import dedup_records\n\ndef test_dedup_records():\n    assert dedup_records(["a", "b", "a"]) == ["a", "b"]\n' > tests/test_basic.py
printf 'import importlib.util\nfrom pathlib import Path\nspec = importlib.util.spec_from_file_location("test_basic", Path("tests/test_basic.py"))\nmod = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(mod)\nmod.test_dedup_records()\nprint("tests: ok")\n' > run_tests.py
python3 run_tests.py
```

运行成功后，回到任务行手动点“记录 / 完成”。

## 本周自查

- [ ] 能解释为什么要在升级前先做项目收口
- [ ] 能写出一个最小 `test_*.py` 测试函数
- [ ] 能说明标准库测试入口与 pytest 的关系

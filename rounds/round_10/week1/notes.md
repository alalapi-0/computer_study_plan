# Round 10 · Week 1 笔记（拆分入口与核心逻辑）

## 本周目标

- 把参数解析从主脚本拆到 `cli.py`。
- 把处理流程放到 `core.py`，文件读写放到 `io_utils.py`。

## Web UI 学习路径

1. 在 Round 10 里打开本文件，先看清“拆分”的目的：入口只负责收参数，核心逻辑负责处理，IO 只负责读写。
2. 点击 `r10-w1-ex1` 的“运行脚本”。脚本会在 `~/cli-lab/round10/week1_auto/ai_prep_tool` 生成：
   - `cli.py`
   - `core.py`
   - `io_utils.py`
   - `input/sample.txt`
   - `output/result.txt`
   - `week1_report.txt`
3. 运行结果会验证 `cli.py --input ... --output ... --min-length 2 --dedup` 可以跑通。
4. 点击 `r10-w1-self` 的“终端练习”，自己写一个更小的 `cli.py` 调用核心函数。

## 三个文件各管什么

- `cli.py`：解析参数，决定调用哪些函数，尽量不写业务细节。
- `core.py`：放纯处理逻辑，例如过滤、去重、统计。
- `io_utils.py`：只处理读文件、写文件、创建目录等边界动作。

## 浏览器终端自测命令

在 `r10-w1-self` 的终端里逐条运行：

```bash
mkdir week1_self
cd week1_self
printf 'def upper_text(text):\n    return text.strip().upper()\n' > core.py
printf 'import argparse\nfrom core import upper_text\n\ndef main():\n    parser = argparse.ArgumentParser()\n    parser.add_argument("--text", default="hello")\n    args = parser.parse_args()\n    print(upper_text(args.text))\n\nif __name__ == "__main__":\n    main()\n' > cli.py
python3 cli.py --text round10
```

看到 `ROUND10` 后，回到任务行点击“记录并完成”。

## 本周自查

- [ ] 能说明入口脚本与核心逻辑分离的好处
- [ ] 能在沙盒里找到 `cli.py` / `core.py` / `io_utils.py` 三个文件
- [ ] 能说明为什么 `core.py` 里的函数更适合写测试

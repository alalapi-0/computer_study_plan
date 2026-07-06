# Round 03 · Week 1 笔记（Python 基础语法）

## 本周目标

- 在 Web UI 中跑通 Python 脚本执行链路。
- 熟悉变量、条件、循环、函数的最小用法。
- 能解释“脚本文件、函数定义、函数调用、打印输出”分别在做什么。

## 在 Web UI 中怎么学

1. 点本任务的“读教程”阅读本页。
2. 点“练习：运行第一个 Python 小程序”的“运行脚本”，系统会在 `~/cli-lab/round3/week1_auto` 生成示例文件并运行。
3. 点自测任务的“终端练习”，浏览器终端会进入 `~/cli-lab/round3`。
4. 自己新建一个目录，例如：

```bash
mkdir week1_self
cd week1_self
printf 'def square(x):\n    return x * x\n\nfor i in range(1, 4):\n    print(i, square(i))\n' > square.py
python3 square.py
```

5. 能解释输出后，再在自测任务旁点“记录并完成”。

## 最小语法地图

```python
name = "alice"            # 变量
score = 86                # 数字

if score >= 60:           # 条件分支
    print("pass")

for i in range(3):        # 循环
    print(i)

def greet(name):          # 函数定义
    return f"hello, {name}"

print(greet("alice"))     # 函数调用
```

## 初学者容易卡住的点

- Python 用缩进表示代码块；`if`、`for`、`def` 后面要有冒号。
- `return` 是把结果交回调用者，`print` 是把内容显示出来。
- `python3 app.py` 运行的是文件，不是文件里的某一行。

## 本周自查

- [ ] 能在 Web UI 终端运行 `python3 square.py`。
- [ ] 能写一个 `for` 循环和一个函数。
- [ ] 能说清 `return` 和 `print` 的区别。

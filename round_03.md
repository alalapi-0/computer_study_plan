# Round 03 · Python 基础补强 + 复杂度直觉

> **定位**：把 Python 写顺，至少能独立写出小脚本；对时间复杂度建立够用的工程直觉，能判断代码是不是太笨。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | Python 基础 + 复杂度直觉 |
| **难度** | ⭐⭐☆☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 02 |
| **下一轮** | Round 04 · 核心数据结构 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 会写和读简单 Python 代码
- [ ] 会用 `if`、`for`、`while`、函数、列表、字典
- [ ] 知道单层循环、双层循环、查字典，大致意味着什么成本
- [ ] 能做出一个很小但真实可用的文本处理脚本

---

## 本轮不学什么

> 先不碰：类和面向对象深水区、正则表达式、装饰器、生成器/迭代器细节、动态规划、递归题海、第三方 AI 框架

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 🎬 主视频 | [CS50P – Week 0/1/2](https://cs50.harvard.edu/python/) | Functions/Variables → Conditionals → Loops |
| 📄 主文档 | [Python 官方教程](https://docs.python.org/3/tutorial/) | 对照查，重点看前几章 + 第 5 章数据结构 |
| 📊 复杂度补充 | [Hello Algo – Complexity](https://www.hello-algo.com/chapter_complexity/) | 图解友好的复杂度入门 |
| 🎮 练习平台 | [Exercism – Python Track](https://exercism.org/tracks/python) | 免费，每周做 2-4 个小练习就够 |
| 📈 可视化工具 | [VisuAlgo](https://visualgo.net/en) | 看循环次数变多 = 时间变长 |

---

## 3 周学习安排

### 第 1 周：把 Python 写起来

**目标**：从"会看一点"变成"能自己写一点"。

**主线**：CS50P Week 0 → Python 官方教程前几章
**本周练**：`print`、`input`、变量、字符串、数字、函数、返回值

**本周结束你要能写出**：
- 输入一个名字，输出问候语
- 输入两个数字，输出和
- 写一个 `def` 函数，把一段重复逻辑包起来

**第 1 周参考脚本**：

```python
# hello.py
def greet(name):
    return f"Hello, {name}!"

name = input("Your name: ")
print(greet(name))
```

```python
# add.py
def add(a, b):
    return a + b

x = int(input("First number: "))
y = int(input("Second number: "))
print(add(x, y))
```

---

### 第 2 周：条件、循环、调试直觉

**目标**：从"会写几行"变成"能写一个小逻辑流程"。

**主线**：CS50P Week 1/2 → Python 官方教程条件和循环部分
**本周练**：`if/elif/else`、`for`、`while`、`break`、`continue`、`try/except`

**本周结束你要能写出**：
- 一个猜数字游戏（有循环和条件）
- 一个简单的单词计数脚本
- 遇到错误时不崩溃，而是打印一条友好信息

**第 2 周参考脚本**：

```python
# count_words.py
text = input("Enter a sentence: ")
words = text.split()
print(f"Word count: {len(words)}")

# 统计每个单词出现次数
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
for word, count in counts.items():
    print(f"  {word}: {count}")
```

---

### 第 3 周：列表、字典、集合 + 复杂度直觉

**目标**：建立"用哪种容器、为什么"的判断力。

**主线**：Python 官方教程第 5 章 → Hello Algo 复杂度章节
**本周练**：`list`、`dict`、`set`、常见操作、O(1)/O(n)/O(n²) 直觉

**本周结束你要能判断**：
- 顺序扫一遍列表 → O(n)
- 用字典查一个 key → O(1)
- 两层嵌套循环处理列表 → O(n²)
- 为什么"统计词频"用字典比用列表快

**第 3 周参考脚本**：

```python
# complexity_demo.py
import time

data = list(range(10000))

# O(n) 示例：线性扫描
start = time.time()
for x in data:
    _ = x * 2
print(f"O(n) loop: {time.time() - start:.4f}s")

# O(1) 示例：字典查找
lookup = {x: x * 2 for x in data}
start = time.time()
for _ in range(10000):
    _ = lookup[5000]
print(f"O(1) lookup: {time.time() - start:.6f}s")
```

---

## 本轮练习清单

### 准备工作

```bash
mkdir -p ~/cli-lab/round3
cd ~/cli-lab/round3
```

---

### 第 1 周练习

**练习 1**：变量和类型
```python
# types_demo.py
name = "Alice"
age = 25
height = 1.68
is_student = True
print(type(name), type(age), type(height), type(is_student))
print(f"{name} is {age} years old")
```

**练习 2**：函数基础
```python
# functions.py
def square(n):
    return n * n

def add(a, b):
    return a + b

print(square(5))
print(add(3, 4))
```

---

### 第 2 周练习

**练习 3**：条件判断
```python
# conditions.py
score = int(input("Score (0-100): "))
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
elif score >= 60:
    print("C")
else:
    print("F")
```

**练习 4**：循环操作
```python
# loops.py
# for 循环
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# while 循环 + break
count = 0
while True:
    count += 1
    if count >= 5:
        break
print(f"Loop ran {count} times")
```

**练习 5**：异常处理
```python
# safe_input.py
def get_number():
    try:
        return int(input("Enter a number: "))
    except ValueError:
        print("That's not a valid number!")
        return None

result = get_number()
if result is not None:
    print(f"You entered: {result}")
```

---

### 第 3 周练习

**练习 6**：列表操作
```python
# list_ops.py
nums = [3, 1, 4, 1, 5, 9, 2, 6]
print(f"Length: {len(nums)}")
print(f"Max: {max(nums)}")
print(f"Sum: {sum(nums)}")
nums.append(7)
nums.sort()
print(f"Sorted: {nums}")
```

**练习 7**：字典词频统计
```python
# word_freq.py
text = "the quick brown fox jumps over the lazy dog the fox"
words = text.split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
# 按频率排序
for word, count in sorted(freq.items(), key=lambda x: -x[1]):
    print(f"{word}: {count}")
```

**练习 8**：集合去重
```python
# dedup.py
labels = ["ok", "blur", "ok", "bad", "blur", "ok", "bad"]
unique = set(labels)
print(f"Original: {labels}")
print(f"Unique: {sorted(unique)}")
print(f"Original count: {len(labels)}, Unique count: {len(unique)}")
```

---

### 综合小项目：文本预处理脚本

```python
# text_prep.py
"""
一个最小的文本预处理脚本：
- 读取用户输入的一段文字
- 统计词频
- 输出 top-5 高频词
"""

def tokenize(text):
    """把文本拆成小写单词列表"""
    return text.lower().split()

def count_freq(words):
    """统计词频，返回 dict"""
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq

def top_n(freq, n=5):
    """返回前 n 个高频词"""
    return sorted(freq.items(), key=lambda x: -x[1])[:n]

def main():
    print("Enter text (Ctrl+D to finish):")
    try:
        lines = []
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    text = " ".join(lines)
    words = tokenize(text)
    freq = count_freq(words)
    top = top_n(freq)
    
    print(f"\nTotal words: {len(words)}")
    print(f"Unique words: {len(freq)}")
    print("\nTop 5 words:")
    for word, count in top:
        print(f"  {word}: {count}")

if __name__ == "__main__":
    main()
```

---

## 复杂度速查表

| 操作 | 复杂度 | 例子 |
|------|--------|------|
| 列表末尾 append/pop | O(1) | `lst.append(x)` |
| 列表头部 insert/pop | O(n) | `lst.insert(0, x)` |
| 字典查找/插入 | O(1) | `d[key]` |
| 集合查找 | O(1) | `x in s` |
| 单层 for 循环 | O(n) | 遍历列表 |
| 两层嵌套 for 循环 | O(n²) | 比较所有对 |

---

## 验收标准

- [ ] 能独立写出包含 `if/for/while/def` 的 30 行左右 Python 脚本
- [ ] 知道列表、字典、集合各适合什么场景
- [ ] 能判断代码的大致复杂度（O(1)/O(n)/O(n²)）
- [ ] 完成了一个最小文本处理脚本

---

## ⚠️ 最容易踩的坑

1. **只看视频不写代码** — CS50P 的课程本身就是"写出来才算学会"
2. **急着学 OOP 和高级特性** — 这轮只要把基础语法写顺，OOP 留到后面
3. **把复杂度当考试背** — 只需要建立直觉：嵌套循环慢、字典查找快

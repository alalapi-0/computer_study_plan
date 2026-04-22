# Round 04 · 核心数据结构

> **定位**：不是把所有数据结构一次学完，而是先把 AI 项目最常碰到的那一批打牢：数组/列表、链表、栈、队列、哈希表。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 数组、链表、栈、队列、哈希表 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 03 |
| **下一轮** | Round 05 · 高频算法模式 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 理解"顺序存储"和"链式存储"的本质区别
- [ ] 知道栈（LIFO）和队列（FIFO）各适合什么场景
- [ ] 知道哈希表的 key-value 映射为什么查找快
- [ ] 会用 Python 的 `list`、`dict`、`set`、`collections.deque`
- [ ] 遇到场景时，能大致判断该用哪种结构

---

## 本轮不学什么

> 先不碰：树、堆、图、手写底层实现重心

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📚 主教材 | [Hello Algo – 第 4-6 章](https://www.hello-algo.com/) | 数组与链表、栈与队列、哈希，图解友好 |
| 📈 可视化 | [VisuAlgo](https://visualgo.net/en) | 重点看 linked list、stack/queue、sorting |
| 🎬 视频补充 | [William Fiset – Data Structures](https://www.youtube.com/watch?v=RBSGKlAvoiM) | 挑数组、链表、栈、队列、哈希片段 |
| 📄 Python 文档 | [Python – list/dict/set/deque](https://docs.python.org/3/library/collections.html#collections.deque) | 官方说明，`deque` 两端 O(1) |
| 📦 参考仓库 | [TheAlgorithms/Python](https://github.com/TheAlgorithms/Python) | 学完概念后对照看，不作主教材 |

---

## 3 周学习安排

### 第 1 周：数组、字符串、列表思维（顺序存储）

**目标**：建立"顺序存储"的直觉。

**核心直觉**：
- 顺序扫一遍列表很自然
- 按索引取某个位置很自然
- 在中间频繁插入删除就不那么自然

**Hello Algo 对应**：Chapter 4 – Array and Linked List（先看数组部分）

**本周练习方向**：
1. 顺序遍历列表，求和、找最大值、统计满足条件的元素个数
2. 处理字符串，做字符计数、去空格、简单分词
3. 比较"追加到末尾"和"插到最前面"的使用感

---

### 第 2 周：链表、栈、队列

**目标**：理解节点+引用思维，和 LIFO/FIFO 的场景感。

**Hello Algo 对应**：Chapter 4（链表部分）+ Chapter 5 – Stack and Queue

**本周关键理解**：
- 链表：每个节点存数据+下一个节点的引用，擅长插入/删除
- 栈：后进先出（LIFO），适合"撤销"、函数调用栈
- 队列：先进先出（FIFO），适合"任务排队"
- Python 里：队列优先用 `collections.deque`，不要用 `list` 做队列

---

### 第 3 周：哈希表

**目标**：理解 key-value 映射，知道为什么查找快。

**Hello Algo 对应**：Chapter 6 – Hashing

**本周关键理解**：
- 哈希表通过哈希函数把 key 映射到位置，查找 O(1)
- Python 的 `dict` 和 `set` 都是哈希实现
- 适合：统计词频、去重、快速判断"是否存在"

---

## 本轮练习清单

### 准备工作

```bash
mkdir -p ~/cli-lab/round4
cd ~/cli-lab/round4
```

---

### 第 1 周练习

**练习 1**：列表基本操作
```python
# list_basics.py
nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# 末尾操作（O(1)）
nums.append(7)
popped = nums.pop()

# 头部操作（O(n)，慢）
nums.insert(0, 99)
first = nums.pop(0)

print(f"Sum: {sum(nums)}")
print(f"Max: {max(nums)}")
print(f"Count of 5: {nums.count(5)}")
```

**练习 2**：字符串处理
```python
# string_ops.py
text = "  Hello, World! This is Python.  "

# 基本操作
print(text.strip())
print(text.lower())
print(text.split())

# 字符计数
char_counts = {}
for ch in text.lower():
    if ch.isalpha():
        char_counts[ch] = char_counts.get(ch, 0) + 1
for ch, cnt in sorted(char_counts.items()):
    print(f"  '{ch}': {cnt}")
```

---

### 第 2 周练习

**练习 3**：用列表模拟栈
```python
# stack_demo.py
# Python list 天然可以当栈用（末尾 push/pop 都是 O(1)）
stack = []
stack.append("a")  # push
stack.append("b")
stack.append("c")
print(f"Stack: {stack}")
top = stack.pop()  # pop
print(f"Popped: {top}, Stack now: {stack}")

# 应用：判断括号是否匹配
def is_balanced(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()
    return len(stack) == 0

print(is_balanced("({[]})"))  # True
print(is_balanced("({[})"))   # False
```

**练习 4**：用 `deque` 模拟队列
```python
# queue_demo.py
from collections import deque

queue = deque()
queue.append("task1")   # enqueue（右端入）
queue.append("task2")
queue.append("task3")
print(f"Queue: {queue}")
first = queue.popleft()  # dequeue（左端出）
print(f"Processed: {first}, Queue now: {queue}")
```

---

### 第 3 周练习

**练习 5**：字典的 key-value 映射
```python
# dict_demo.py
# 词频统计：O(n) 扫描，每次查询 O(1)
words = "the quick brown fox jumps over the lazy dog".split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1

# 查找特定词
print(f"'the' appears {freq.get('the', 0)} times")
print(f"'cat' appears {freq.get('cat', 0)} times")
```

**练习 6**：集合去重和成员查询
```python
# set_demo.py
labels = ["ok", "blur", "ok", "bad", "blur", "ok", "bad", "good"]

# 去重
unique = set(labels)
print(f"Unique labels: {sorted(unique)}")

# O(1) 成员查询
valid_labels = {"ok", "blur", "bad", "good"}
test_labels = ["ok", "unknown", "blur", "invalid"]
for label in test_labels:
    if label in valid_labels:
        print(f"  {label}: valid")
    else:
        print(f"  {label}: INVALID")
```

**练习 7**：对比有无哈希的性能差异
```python
# perf_compare.py
import time

data = list(range(100000))
target = 99999

# 列表查找：O(n)
start = time.time()
for _ in range(1000):
    _ = target in data
print(f"List search (1000x): {time.time()-start:.3f}s")

# 集合查找：O(1)
data_set = set(data)
start = time.time()
for _ in range(1000):
    _ = target in data_set
print(f"Set search (1000x): {time.time()-start:.4f}s")
```

---

### 综合小项目：数据处理工具箱

```python
# data_toolkit.py
"""
用本轮学到的数据结构做一个最小数据处理工具：
- 用列表存原始数据
- 用字典统计
- 用集合去重
- 用 deque 处理批次队列
"""
from collections import deque

def process_labels(raw_labels):
    """
    输入：标签列表
    输出：统计信息字典
    """
    # 用字典统计频率
    freq = {}
    for label in raw_labels:
        freq[label] = freq.get(label, 0) + 1
    
    # 用集合去重
    unique = set(raw_labels)
    
    # 用 deque 做批次队列（每批 3 个）
    queue = deque(raw_labels)
    batches = []
    while queue:
        batch = []
        for _ in range(3):
            if queue:
                batch.append(queue.popleft())
        batches.append(batch)
    
    return {
        "total": len(raw_labels),
        "unique_count": len(unique),
        "unique_labels": sorted(unique),
        "freq": freq,
        "batch_count": len(batches)
    }

labels = ["ok", "blur", "ok", "bad", "blur", "ok", "bad", "good", "ok"]
result = process_labels(labels)
for key, value in result.items():
    print(f"{key}: {value}")
```

---

## 数据结构速查表

| 结构 | Python 实现 | 查找 | 插入末尾 | 插入头部 | 适用场景 |
|------|-------------|------|----------|----------|----------|
| 数组/列表 | `list` | O(n) | O(1) | O(n) | 顺序访问、索引访问 |
| 链表 | 手写 | O(n) | O(1)* | O(1)* | 频繁插入删除中间 |
| 栈 | `list`（末尾） | - | O(1) | - | 撤销、函数调用 |
| 队列 | `deque` | - | O(1) | O(1) | 任务排队、BFS |
| 哈希表 | `dict`/`set` | O(1) | O(1) | - | 统计、去重、快速查找 |

---

## 验收标准

- [ ] 能解释顺序存储和链式存储的本质区别
- [ ] 能用 `list` 模拟栈，用 `deque` 模拟队列
- [ ] 能解释 Python `dict` 查找为什么是 O(1)
- [ ] 完成了数据处理工具箱项目
- [ ] 遇到"统计/去重/查找"场景时，第一反应是用 `dict` 或 `set`

---

## ⚠️ 最容易踩的坑

1. **把 list 当队列用** — 用 `list.pop(0)` 做队列头部弹出是 O(n)，用 `deque.popleft()` 才是 O(1)
2. **急着看底层实现** — 这轮先建立直觉，TheAlgorithms/Python 适合学完概念后对照看
3. **跳过可视化** — VisuAlgo 的链表和栈/队列动画，对建立"结构怎么动"很有用

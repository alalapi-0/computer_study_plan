# Round 05 · 高频算法模式

> **定位**：不是把你训练成刷题机器，而是让你形成一种能力：看到题目或小需求时，能先判断"这更像哪一种模式"。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | 双指针、滑动窗口、二分、排序与分治、DFS/BFS/回溯、贪心、DP 入门 |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 04 |
| **下一轮** | Round 06 · Linux 进阶与自动化 |

---

## 本轮目标

完成本轮后，你能建立 6 个判断习惯：

- [ ] 连续区间问题，先想双指针或滑动窗口
- [ ] 有序数据里找位置或边界，先想二分
- [ ] 需要"拆小再合并"，先想分治
- [ ] 图、树、网格、状态扩展，先想 DFS/BFS
- [ ] "试一种选择，不行再撤回"，先想回溯
- [ ] 优化问题里，先区分是贪心能做，还是要上 DP

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 📚 主教材 | [Hello Algo – 第 10/12/13/14/15 章](https://www.hello-algo.com/) | 二分、分治、回溯、DP、贪心 |
| 📈 可视化 | [VisuAlgo – Sorting/DFS/BFS](https://visualgo.net/en) | 直观看算法过程 |
| 🎬 视频补充 | [William Fiset – Graph Theory](https://www.youtube.com/c/WilliamFiset-videos) | DFS、BFS、DP 播放列表 |
| 📖 双指针补充 | [CSES Handbook – Chapter 8](https://cses.fi/book/book.pdf) | Two pointers + Sliding window minimum |
| 🎓 轻量补充 | [Khan Academy – Algorithms](https://www.khanacademy.org/computing/computer-science/algorithms) | 二分和复杂度的轻量解释 |

---

## 3 周学习安排

### 第 1 周：双指针、滑动窗口、二分查找

**目标**：学会认问题，而不是背模板。

**核心判断**：
- 两端往中间夹 → 双指针
- 固定长度或可伸缩区间 → 滑动窗口
- 有序数据，每次把范围减半 → 二分

**Hello Algo 对应**：Chapter 10.1-10.3（Binary Search）

---

### 第 2 周：排序与分治、DFS/BFS/回溯

**目标**：建立"拆小问题"和"状态扩展遍历"的两种思维。

**核心判断**：
- 拆小再合并 → 分治（如归并排序）
- 图/树/网格遍历 → DFS（深度优先）或 BFS（广度优先）
- 试选择、不行撤回 → 回溯

**Hello Algo 对应**：Chapter 12（Divide and Conquer）+ Chapter 13（Backtracking）

---

### 第 3 周：贪心、DP 入门

**目标**：能区分什么时候贪心能做，什么时候需要 DP。

**核心判断**：
- 每步都选局部最优，且不需要回头 → 贪心
- 子问题重叠，需要保存结果避免重复计算 → DP

**Hello Algo 对应**：Chapter 14（Dynamic Programming 引言）+ Chapter 15（Greedy）

---

## 本轮练习清单

### 准备工作

```bash
mkdir -p ~/cli-lab/round5
cd ~/cli-lab/round5
```

---

### 第 1 周练习

**练习 1**：二分查找
```python
# binary_search.py
def binary_search(arr, target):
    """在有序数组中查找 target，返回索引，找不到返回 -1"""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

arr = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(arr, 7))   # 3
print(binary_search(arr, 6))   # -1
```

**练习 2**：双指针（两数之和 - 有序数组）
```python
# two_pointers.py
def two_sum_sorted(arr, target):
    """有序数组中找两数之和等于 target"""
    left, right = 0, len(arr) - 1
    while left < right:
        s = arr[left] + arr[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return []

arr = [1, 2, 4, 6, 8, 10]
print(two_sum_sorted(arr, 10))  # [1, 4] 或 [2, 8]
```

**练习 3**：滑动窗口（最大子数组和 - 定长）
```python
# sliding_window.py
def max_sum_window(arr, k):
    """长度为 k 的子数组的最大和"""
    if len(arr) < k:
        return None
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum

arr = [2, 1, 5, 1, 3, 2]
print(max_sum_window(arr, 3))  # 9 (5+1+3)
```

---

### 第 2 周练习

**练习 4**：归并排序（分治）
```python
# merge_sort.py
def merge_sort(arr):
    """分治：拆成两半，各自排序，再合并"""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

print(merge_sort([3, 1, 4, 1, 5, 9, 2, 6]))
```

**练习 5**：DFS（迷宫路径）
```python
# dfs_demo.py
def dfs(grid, row, col, visited):
    """深度优先搜索：找从起点能到达的所有格子"""
    rows, cols = len(grid), len(grid[0])
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return
    if grid[row][col] == "#" or (row, col) in visited:
        return
    visited.add((row, col))
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        dfs(grid, row+dr, col+dc, visited)

grid = [
    [".", ".", "#", "."],
    ["#", ".", ".", "."],
    [".", ".", "#", "#"],
]
visited = set()
dfs(grid, 0, 0, visited)
print(f"Reachable cells: {len(visited)}")
```

**练习 6**：回溯（全排列）
```python
# backtrack.py
def permutations(nums):
    """回溯：枚举所有排列"""
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i, num in enumerate(remaining):
            path.append(num)
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()  # 撤回
    
    backtrack([], nums)
    return result

print(permutations([1, 2, 3]))
```

---

### 第 3 周练习

**练习 7**：贪心（最少硬币数 - 特定面值）
```python
# greedy_coins.py
def min_coins_greedy(amount, coins):
    """贪心：优先用最大面值（只在某些硬币面值下有效）"""
    coins = sorted(coins, reverse=True)
    count = 0
    for coin in coins:
        while amount >= coin:
            amount -= coin
            count += 1
    return count if amount == 0 else -1

# 对于 [1, 5, 10, 25] 面值，贪心有效
print(min_coins_greedy(41, [1, 5, 10, 25]))  # 4 (25+10+5+1)
```

**练习 8**：DP 入门（爬楼梯）
```python
# dp_stairs.py
def climb_stairs(n):
    """
    DP：每次可以爬1步或2步，爬n级楼梯共有多少种方法？
    子问题：dp[i] = dp[i-1] + dp[i-2]
    """
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2
    for i in range(3, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

for i in range(1, 8):
    print(f"climb_stairs({i}) = {climb_stairs(i)}")
```

---

## 算法模式速查表

| 模式 | 触发信号 | 典型例子 |
|------|---------|--------|
| 双指针 | 有序数组，两端夹逼 | 两数之和、回文判断 |
| 滑动窗口 | 连续子区间 | 最大子数组和、最长不重复子串 |
| 二分查找 | 有序数据，找边界 | 搜索位置、旋转数组 |
| 分治 | 拆成独立子问题再合并 | 归并排序、快速排序 |
| DFS | 图/树深度遍历、路径枚举 | 迷宫、连通性 |
| BFS | 最短路径、按层扩散 | 最短路、网格感染 |
| 回溯 | 枚举所有可能，不行就撤 | 全排列、子集、N 皇后 |
| 贪心 | 局部最优 = 全局最优 | 区间调度、硬币找零 |
| DP | 子问题重叠，需记忆化 | 爬楼梯、背包问题 |

---

## 验收标准

- [ ] 能独立实现二分查找
- [ ] 能识别双指针和滑动窗口的使用场景
- [ ] 能写一个简单的 DFS 遍历
- [ ] 能写最小 DP 问题（爬楼梯）
- [ ] 看到新问题时，能先说"这更像哪种模式"

---

## ⚠️ 最容易踩的坑

1. **盲目刷题** — 这轮重点是建立模式识别，不是追题目数量
2. **把 DP 和贪心混淆** — 贪心每步选局部最优不回头；DP 保存子问题结果避免重复
3. **跳过可视化** — VisuAlgo 的排序和图遍历动画对建立直觉非常有帮助

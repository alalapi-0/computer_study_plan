# Round 05 · Week 1 笔记（双指针 / 滑动窗口 / 二分）

## 本周目标

- 看到“连续区间”时，先想到双指针和滑动窗口。
- 看到“有序 + 查找边界”时，先想到二分。
- 能把“暴力双重循环”改写成一次扫描或二分。

## 在 Web UI 中怎么学

1. 点“练习：二分查找与滑动窗口”的“运行脚本”，查看自动生成的 `binary_window_demo.py`。
2. 点“自测：自己写 two_sum_sorted.py”的“终端练习”，浏览器终端会进入 `~/cli-lab/round5`。
3. 自己写一个有序数组双指针脚本：

```bash
mkdir week1_self
cd week1_self
printf 'def two_sum_sorted(nums, target):\n    left, right = 0, len(nums) - 1\n    while left < right:\n        total = nums[left] + nums[right]\n        if total == target:\n            return (left, right)\n        if total < target:\n            left += 1\n        else:\n            right -= 1\n    return None\n\nprint(two_sum_sorted([1, 2, 4, 7, 11], 9))\nprint(two_sum_sorted([1, 2, 4, 7, 11], 10))\n' > two_sum_sorted.py
python3 two_sum_sorted.py
```

4. 能解释为什么 `left` / `right` 会移动、什么时候该用二分后，再点击“记录并完成”保存自测记录。

## 模式直觉

- 双指针：两个指针一起维护范围或配对，常见于有序数组、去重、左右夹逼。
- 滑动窗口：左右边界维护一个连续区间，常见于“最长 / 最短连续子数组”。
- 二分：每次砍掉一半搜索范围，前提通常是“有序”或“答案具有单调性”。

## 最小代码骨架

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

## 本周自查

- [ ] 能解释双指针和滑动窗口的差异
- [ ] 能写出基础二分查找
- [ ] 能写出有序数组双指针 `two_sum_sorted`

#!/bin/bash
# Round 05 · Week 1 练习：二分查找与滑动窗口（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round5/week1_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > binary_window_demo.py <<'EOF'
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

arr = [1, 3, 5, 7, 9, 11]
print(binary_search(arr, 7))
print(binary_search(arr, 8))

def max_sum_window(nums, k):
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best

print("max-window:", max_sum_window([2, 1, 5, 1, 3, 2], 3))
EOF

python3 binary_window_demo.py

cat > next_steps.txt <<'EOF'
Week 1 自动练习已生成 binary_window_demo.py。

自测请在 Web UI 点 r05-w1-self 的“终端”，进入 ~/cli-lab/round5 后自己完成：
1. 新建 week1_self 目录。
2. 写一个 two_sum_sorted.py，使用左右双指针。
3. 运行 python3 two_sum_sorted.py。
4. 能解释双指针、滑动窗口、二分的触发条件后，手动点“记录 / 完成”。
EOF

mark r05-w1-ex1

echo "Week 1 自动练习完成。请继续手动完成 r05-w1-self。"

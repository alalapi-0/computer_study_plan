#!/bin/bash
# Round 05 · Week 1 练习：双指针 / 滑动窗口 / 二分

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round5/week1
cd ~/cli-lab/round5/week1

cat > binary_search_demo.py <<'EOF'
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
EOF

python3 binary_search_demo.py

echo "请补充一个双指针或滑动窗口练习后按回车继续..."
read
echo "Week 1 完成。"

mark r05-w1-ex1

echo "请手动完成第1周自测后按回车继续..."
read
mark r05-w1-self

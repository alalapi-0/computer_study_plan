#!/bin/bash
# Round 04 · Week 1 练习：list 遍历、过滤与统计（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round4/week1_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > list_demo.py <<'EOF'
nums = [3, 1, 4, 1, 5, 9, 2, 6, 5]
print("sum:", sum(nums))
print("max:", max(nums))
print("count(5):", nums.count(5))

even = []
for x in nums:
    if x % 2 == 0:
        even.append(x)
print("even:", even)

print("first:", nums[0])
print("last:", nums[-1])
EOF

python3 list_demo.py

cat > next_steps.txt <<'EOF'
Week 1 自动练习已生成 list_demo.py。

自测请在 Web UI 点 r04-w1-self 的“终端练习”，进入 ~/cli-lab/round4 后自己完成：
1. 新建 week1_self 目录。
2. 写一个 scores.py，使用 list、for、if、append。
3. 运行 python3 scores.py。
4. 能解释 append、len、索引访问和过滤条件后，点击“记录并完成”。
EOF

mark r04-w1-ex1

echo "Week 1 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r04-w1-self。"

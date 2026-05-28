#!/bin/bash
# Round 04 · Week 1 练习：列表与顺序存储

set -e

mkdir -p ~/cli-lab/round4/week1
cd ~/cli-lab/round4/week1

cat > list_demo.py <<'EOF'
nums = [3, 1, 4, 1, 5, 9, 2, 6, 5]
print("sum:", sum(nums))
print("max:", max(nums))
print("count(5):", nums.count(5))
EOF

python3 list_demo.py
echo "Week 1 完成。"

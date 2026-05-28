#!/bin/bash
# Round 03 · Week 3 练习：复杂度观察

set -e

mkdir -p ~/cli-lab/round3/week3
cd ~/cli-lab/round3/week3

cat > complexity_demo.py <<'EOF'
nums = list(range(100))

count_linear = 0
for _ in nums:
    count_linear += 1

count_quadratic = 0
for _ in nums:
    for _ in nums:
        count_quadratic += 1

print("linear ops:", count_linear)
print("quadratic ops:", count_quadratic)
EOF

python3 complexity_demo.py
echo "Week 3 完成。"

#!/bin/bash
# Round 03 · Week 3 练习：复杂度观察

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

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

mark r03-w3-ex3

echo "请手动完成第3周自测后按回车继续..."
read
mark r03-w3-self

echo "Week 3 完成。"

#!/bin/bash
# Round 05 · Week 3 练习：贪心 / DP 入门

set -e

mkdir -p ~/cli-lab/round5/week3
cd ~/cli-lab/round5/week3

cat > dp_stairs_demo.py <<'EOF'
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

for i in range(1, 8):
    print(i, climb_stairs(i))
EOF

python3 dp_stairs_demo.py

echo "请补充一个贪心反例（证明并非总是最优）后按回车继续..."
read
echo "Week 3 完成。"

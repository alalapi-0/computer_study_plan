#!/bin/bash
# Round 05 · Week 3 练习：贪心选择与 DP 爬楼梯（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round5/week3_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > greedy_dp_demo.py <<'EOF'
def greedy_activity(intervals):
    intervals = sorted(intervals, key=lambda x: x[1])
    chosen = []
    end = -1
    for start, finish in intervals:
        if start >= end:
            chosen.append((start, finish))
            end = finish
    return chosen

print("activities:", greedy_activity([(1, 3), (2, 4), (3, 5), (0, 6), (5, 7)]))

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

python3 greedy_dp_demo.py

cat > next_steps.txt <<'EOF'
Week 3 自动练习已生成 greedy_dp_demo.py。

自测请在 Web UI 点 r05-w3-self 的“终端练习”，进入 ~/cli-lab/round5 后自己完成：
1. 新建 week3_self 目录。
2. 写一个 coin_change_dp.py，使用 dp[x] 表示凑出金额 x 的最少硬币数。
3. 运行 python3 coin_change_dp.py。
4. 能解释贪心和 DP 的判断差异后，点击“记录并完成”。
EOF

mark r05-w3-ex3

echo "Week 3 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r05-w3-self。"

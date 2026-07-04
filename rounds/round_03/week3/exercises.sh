#!/bin/bash
# Round 03 · Week 3 练习：复杂度观察（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round3/week3_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > complexity_demo.py <<'EOF'
for n in [10, 100, 1000]:
    nums = list(range(n))

    count_linear = 0
    for _ in nums:
        count_linear += 1

    count_quadratic = 0
    for _ in nums:
        for _ in nums:
            count_quadratic += 1

    print("n:", n, "linear:", count_linear, "quadratic:", count_quadratic)
EOF

python3 complexity_demo.py

cat > next_steps.txt <<'EOF'
Week 3 自动练习已生成 complexity_demo.py。

自测请在 Web UI 点 r03-w3-self 的“终端”，进入 ~/cli-lab/round3 后自己完成：
1. 新建 week3_self 目录。
2. 写一个 growth.py，打印 n、n、n*n。
3. 运行 python3 growth.py。
4. 能解释 O(n) 与 O(n^2) 后，手动点“记录 / 完成”。
EOF

mark r03-w3-ex3

echo "Week 3 自动练习完成。请继续手动完成 r03-w3-self。"

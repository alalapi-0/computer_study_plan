#!/bin/bash
# Round 03 · Week 1 练习：Python 基础语法（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round3/week1_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > app.py <<'EOF'
def greet(name):
    return f"hello, {name}"

for i in range(3):
    print(greet(f"user{i}"))
EOF

python3 app.py

cat > score_check.py <<'EOF'
def status(score):
    if score >= 60:
        return "pass"
    return "retry"

for score in [42, 60, 88]:
    print(score, status(score))
EOF

python3 score_check.py

cat > next_steps.txt <<'EOF'
Week 1 自动练习已生成 app.py 和 score_check.py。

自测请在 Web UI 点 r03-w1-self 的“终端”，进入 ~/cli-lab/round3 后自己完成：
1. 新建 week1_self 目录。
2. 写一个 square.py，包含函数和 for 循环。
3. 运行 python3 square.py。
4. 能解释 return 与 print 的区别后，手动点“记录 / 完成”。
EOF

mark r03-w1-ex1

echo "Week 1 自动练习完成。请继续手动完成 r03-w1-self。"

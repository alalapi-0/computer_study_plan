#!/bin/bash
# Round 03 · Week 1 练习：Python 基础语法

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round3/week1
cd ~/cli-lab/round3/week1

cat > app.py <<'EOF'
def greet(name):
    return f"hello, {name}"

for i in range(3):
    print(greet(f"user{i}"))
EOF

python3 app.py

mark r03-w1-ex1

echo "请手动完成第1周自测后按回车继续..."
read
mark r03-w1-self

echo "Week 1 完成。"

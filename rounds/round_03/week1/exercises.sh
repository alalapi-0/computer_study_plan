#!/bin/bash
# Round 03 · Week 1 练习：Python 基础语法

set -e

mkdir -p ~/cli-lab/round3/week1
cd ~/cli-lab/round3/week1

cat > app.py <<'EOF'
def greet(name):
    return f"hello, {name}"

for i in range(3):
    print(greet(f"user{i}"))
EOF

python3 app.py
echo "Week 1 完成。"

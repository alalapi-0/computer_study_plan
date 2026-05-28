#!/bin/bash
# Round 04 · Week 3 练习：哈希与去重

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round4/week3
cd ~/cli-lab/round4/week3

cat > hash_demo.py <<'EOF'
labels = ["ok", "blur", "ok", "bad", "blur", "ok"]
freq = {}
for x in labels:
    freq[x] = freq.get(x, 0) + 1
print("freq:", freq)
print("unique:", sorted(set(labels)))
EOF

python3 hash_demo.py

mark r04-w3-ex3

echo "请手动完成第3周自测后按回车继续..."
read
mark r04-w3-self

echo "Week 3 完成。"

#!/bin/bash
# Round 04 · Week 3 练习：哈希与去重

set -e

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
echo "Week 3 完成。"

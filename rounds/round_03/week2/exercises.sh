#!/bin/bash
# Round 03 · Week 2 练习：list/dict 与函数拆分

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round3/week2
cd ~/cli-lab/round3/week2

cat > stats.py <<'EOF'
def count_labels(items):
    result = {}
    for item in items:
        result[item] = result.get(item, 0) + 1
    return result

labels = ["error", "info", "error", "warn", "info"]
print(count_labels(labels))
EOF

python3 stats.py

mark r03-w2-ex2

echo "请手动完成第2周自测后按回车继续..."
read
mark r03-w2-self

echo "Week 2 完成。"

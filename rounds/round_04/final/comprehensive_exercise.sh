#!/bin/bash
# Round 04 · Final 综合练习

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round4/final
cd ~/cli-lab/round4/final

cat > data_toolkit.py <<'EOF'
from collections import deque

def summarize(items):
    freq = {}
    for x in items:
        freq[x] = freq.get(x, 0) + 1
    queue = deque(items)
    batches = []
    while queue:
        batch = []
        for _ in range(3):
            if queue:
                batch.append(queue.popleft())
        batches.append(batch)
    return {"freq": freq, "unique": sorted(set(items)), "batches": batches}

print(summarize(["ok", "ok", "error", "warn", "ok", "error"]))
EOF

python3 data_toolkit.py

mark r04-fin-comp

echo "请检查 rounds/round_04/final/complexity_cheatsheet.md 后按回车..."
read
mark r04-fin-sheet

echo "请确认你能解释 dict/set/deque 的适用场景后按回车..."
read
mark r04-fin-acc1

echo "Final 完成。"

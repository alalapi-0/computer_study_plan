#!/bin/bash
# Round 04 · Final 综合练习

set -e

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
echo "Final 完成。"

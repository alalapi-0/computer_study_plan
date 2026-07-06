#!/bin/bash
# Round 04 · Final 综合练习（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round4/final_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

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

def stack_demo(actions):
    stack = []
    for action in actions:
        stack.append(action)
    return stack.pop(), stack

data = ["ok", "ok", "error", "warn", "ok", "error"]
print("summary:", summarize(data))
print("stack:", stack_demo(["open", "edit", "save"]))
EOF

python3 data_toolkit.py

cat > final_notes.md <<'EOF'
# Round 04 Final 自动练习产物

- data_toolkit.py：综合使用 dict、set、deque、list 和 stack 思路。
- 这只是自动综合练习。
- 小抄 r04-fin-sheet 与验收 r04-fin-acc1 仍需用户自己阅读、解释并在 Web UI 点击“记录并完成”保存记录。
EOF

mark r04-fin-comp

echo "Round 04 Final 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r04-fin-sheet 与 r04-fin-acc1。"

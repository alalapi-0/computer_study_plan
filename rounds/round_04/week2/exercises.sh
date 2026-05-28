#!/bin/bash
# Round 04 · Week 2 练习：栈与队列

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round4/week2
cd ~/cli-lab/round4/week2

cat > stack_queue_demo.py <<'EOF'
from collections import deque

stack = []
stack.append("a")
stack.append("b")
print("stack pop:", stack.pop())

queue = deque()
queue.append("task1")
queue.append("task2")
print("queue popleft:", queue.popleft())
EOF

python3 stack_queue_demo.py

mark r04-w2-ex2

echo "请手动完成第2周自测后按回车继续..."
read
mark r04-w2-self

echo "Week 2 完成。"

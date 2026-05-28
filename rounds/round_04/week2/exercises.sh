#!/bin/bash
# Round 04 · Week 2 练习：栈与队列

set -e

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
echo "Week 2 完成。"

#!/bin/bash
# Round 04 · Week 2 练习：stack 与 queue 出入顺序（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round4/week2_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > stack_queue_demo.py <<'EOF'
from collections import deque

stack = []
stack.append("a")
stack.append("b")
stack.append("c")
print("stack pop:", stack.pop())
print("stack left:", stack)

queue = deque()
queue.append("task1")
queue.append("task2")
queue.append("task3")
print("queue popleft:", queue.popleft())
print("queue left:", list(queue))
EOF

python3 stack_queue_demo.py

cat > next_steps.txt <<'EOF'
Week 2 自动练习已生成 stack_queue_demo.py。

自测请在 Web UI 点 r04-w2-self 的“终端练习”，进入 ~/cli-lab/round4 后自己完成：
1. 新建 week2_self 目录。
2. 写一个 browser_history.py，使用 list 模拟后退栈，用 deque 模拟任务队列。
3. 运行 python3 browser_history.py。
4. 能解释 LIFO 与 FIFO 后，点击“记录并完成”。
EOF

mark r04-w2-ex2

echo "Week 2 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r04-w2-self。"

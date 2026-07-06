#!/bin/bash
# Round 05 · Week 2 练习：DFS、BFS 与回溯最小例子（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round5/week2_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB"
cd "$LAB"

cat > graph_backtracking_demo.py <<'EOF'
from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "D": [],
    "E": []
}

def dfs(node, visited):
    if node in visited:
        return
    visited.add(node)
    print(node)
    for nxt in graph[node]:
        dfs(nxt, visited)

dfs("A", set())

def bfs(start):
    queue = deque([start])
    visited = {start}
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)
    return order

print("bfs:", bfs("A"))

def permutations(items):
    answer = []
    used = [False] * len(items)
    path = []

    def backtrack():
        if len(path) == len(items):
            answer.append(path[:])
            return
        for i, item in enumerate(items):
            if used[i]:
                continue
            used[i] = True
            path.append(item)
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return answer

print("perm:", permutations(["x", "y", "z"]))
EOF

python3 graph_backtracking_demo.py

cat > next_steps.txt <<'EOF'
Week 2 自动练习已生成 graph_backtracking_demo.py。

自测请在 Web UI 点 r05-w2-self 的“终端练习”，进入 ~/cli-lab/round5 后自己完成：
1. 新建 week2_self 目录。
2. 写一个 bfs_levels.py，使用 deque 完成 BFS。
3. 运行 python3 bfs_levels.py。
4. 能解释 DFS、BFS、回溯差异后，点击“记录并完成”。
EOF

mark r05-w2-ex2

echo "Week 2 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r05-w2-self。"

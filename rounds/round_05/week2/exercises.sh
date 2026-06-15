#!/bin/bash
# Round 05 · Week 2 练习：分治 / DFS / BFS / 回溯

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round5/week2
cd ~/cli-lab/round5/week2

cat > dfs_demo.py <<'EOF'
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
EOF

python3 dfs_demo.py

mark r05-w2-ex2

echo "请补充一个回溯或 BFS 练习后按回车继续..."
read
mark r05-w2-self

echo "Week 2 完成。"

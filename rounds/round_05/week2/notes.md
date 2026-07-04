# Round 05 · Week 2 笔记（分治 / DFS / BFS / 回溯）

## 本周目标

- 理解“拆小再合并”的分治思维。
- 识别图、树、网格问题中的 DFS / BFS 场景。
- 理解回溯“试错 + 撤销”的基本流程。

## 在 Web UI 中怎么学

1. 点“练习：DFS、BFS 与回溯最小例子”的“运行”，查看自动生成的 `graph_backtracking_demo.py`。
2. 点“自测：自己写 bfs_levels.py”的“终端”，在 `~/cli-lab/round5` 下完成自测脚本。
3. 推荐自测命令：

```bash
mkdir week2_self
cd week2_self
printf 'from collections import deque\n\ngraph = {\"A\": [\"B\", \"C\"], \"B\": [\"D\"], \"C\": [\"E\"], \"D\": [], \"E\": []}\nqueue = deque([\"A\"])\nvisited = set([\"A\"])\norder = []\nwhile queue:\n    node = queue.popleft()\n    order.append(node)\n    for nxt in graph[node]:\n        if nxt not in visited:\n            visited.add(nxt)\n            queue.append(nxt)\nprint(order)\n' > bfs_levels.py
python3 bfs_levels.py
```

4. 能解释 DFS 和 BFS 的访问顺序差异后，再手动记录自测完成。

## 模式直觉

- 分治：把大问题拆成小问题，分别解决后合并结果。
- DFS：一条路走到底，再回头；适合树、图、路径搜索。
- BFS：一层一层扩展；适合最短步数、层序遍历。
- 回溯：尝试一个选择，继续递归，不合适就撤销选择。

## 回溯骨架

```python
def backtrack(path, choices):
    if finished(path):
        answer.append(path[:])
        return
    for choice in choices:
        path.append(choice)
        backtrack(path, choices)
        path.pop()
```

## 本周自查

- [ ] 能实现一个最小 DFS 或 BFS 遍历
- [ ] 能写出一段简单回溯代码（如全排列）
- [ ] 能解释 BFS 为什么常用于“最短步数”

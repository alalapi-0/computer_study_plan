# Round 04 · Week 2 笔记（栈与队列）

## 本周目标

- 了解栈（LIFO）与队列（FIFO）场景差异。
- 使用 `list` 完成 stack 的 push / pop。
- 使用 `collections.deque` 完成 queue 的 append / popleft。

## 在 Web UI 中怎么学

1. 点“练习：stack 与 queue 出入顺序”的“运行脚本”，查看自动生成的 `stack_queue_demo.py`。
2. 点“自测：自己写 browser_history.py”的“终端练习”，在 `~/cli-lab/round4` 下完成自测脚本。
3. 推荐自测命令：

```bash
mkdir week2_self
cd week2_self
printf 'from collections import deque\n\nback_stack = []\nback_stack.append(\"home\")\nback_stack.append(\"search\")\nback_stack.append(\"detail\")\nprint(\"back\", back_stack.pop())\n\ntasks = deque([\"read\", \"code\", \"review\"])\nprint(\"next\", tasks.popleft())\nprint(\"left\", list(tasks))\n' > browser_history.py
python3 browser_history.py
```

4. 能解释为什么 back 用栈、排队任务用队列后，再点击“记录并完成”保存自测记录。

## 栈与队列的场景

- 栈：后进先出。像撤销、浏览器后退、函数调用栈。
- 队列：先进先出。像排队、任务调度、消息缓冲。
- Python `list.append()` + `list.pop()` 可以模拟栈。
- Python `deque.append()` + `deque.popleft()` 适合模拟队列。

## 最小代码

```python
from collections import deque

stack = []
stack.append("A")
stack.append("B")
print(stack.pop())  # B

queue = deque()
queue.append("A")
queue.append("B")
print(queue.popleft())  # A
```

## 本周自查

- [ ] 能用 `list` 完成 push/pop
- [ ] 能用 `deque` 完成 append/popleft
- [ ] 能给出一个该用栈、一个该用队列的真实例子

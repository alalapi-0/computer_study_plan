# Round 04 · Week 1 笔记（列表与顺序存储）

## 本周目标

- 理解 Python `list` 的顺序存储直觉。
- 熟悉遍历、索引访问、追加、过滤、统计等基础操作。
- 能解释“按位置取元素”和“从头扫描查找”的差别。

## 在 Web UI 中怎么学

1. 点“练习：list 遍历、过滤与统计”的“运行”，查看自动生成的 `list_demo.py`。
2. 点“自测：自己写 scores.py”的“终端”，浏览器终端会进入 `~/cli-lab/round4`。
3. 自己写一个小脚本：

```bash
mkdir week1_self
cd week1_self
printf 'scores = [82, 57, 91, 73, 45]\npassed = []\nfor score in scores:\n    if score >= 60:\n        passed.append(score)\nprint(\"passed\", passed)\nprint(\"count\", len(passed))\nprint(\"first\", scores[0])\n' > scores.py
python3 scores.py
```

4. 能解释 `append`、`len`、索引访问、过滤条件后，再手动记录自测完成。

## list 直觉

- `list` 像一排有顺序的格子，适合保存“第 1 个、第 2 个、第 3 个……”。
- `items[0]` 是按位置访问，通常很快。
- `for x in items` 是从头到尾遍历，数据越多，遍历时间越长。
- 尾部 `append` 通常很方便；头部插入会让后面的元素整体挪动，代价更高。

## 常见操作

```python
items = [3, 1, 4]
items.append(1)
print(items[0])

total = 0
for x in items:
    total += x

big = []
for x in items:
    if x >= 3:
        big.append(x)
```

## 本周自查

- [ ] 能写出 list 遍历和过滤。
- [ ] 能解释索引访问与遍历扫描的区别。
- [ ] 能说明头部插入与尾部追加的差异。

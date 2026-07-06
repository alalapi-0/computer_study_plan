# Round 04 · Week 3 笔记（哈希表）

## 本周目标

- 理解 `dict` / `set` 的查找与去重价值。
- 完成一个最小词频统计脚本。
- 能解释“为什么去重和计数不适合一直用双重循环硬扫”。

## 在 Web UI 中怎么学

1. 点“练习：dict 计数与 set 去重”的“运行脚本”，查看自动生成的 `hash_demo.py`。
2. 点“自测：自己写 tag_report.py”的“终端练习”，在 `~/cli-lab/round4` 下完成自测脚本。
3. 推荐自测命令：

```bash
mkdir week3_self
cd week3_self
printf 'tags = [\"python\", \"linux\", \"python\", \"git\", \"linux\"]\ncounts = {}\nfor tag in tags:\n    counts[tag] = counts.get(tag, 0) + 1\nprint(\"counts\", counts)\nprint(\"unique\", sorted(set(tags)))\nprint(\"has git\", \"git\" in set(tags))\n' > tag_report.py
python3 tag_report.py
```

4. 能解释 `dict.get()`、`set()`、`in` 判断后，再点击“记录并完成”保存自测记录。

## dict / set 直觉

- `dict` 是“键 -> 值”的映射，适合计数、按名字查记录、保存索引。
- `set` 是“不重复集合”，适合去重和快速判断某个值是否出现过。
- 平均情况下，`dict` / `set` 的查找接近 O(1)；但这不是魔法，仍要考虑数据规模和冲突等实现细节。

## 常见写法

```python
counts = {}
for word in ["a", "b", "a"]:
    counts[word] = counts.get(word, 0) + 1

seen = set()
for word in ["a", "b", "a"]:
    seen.add(word)
```

## 本周自查

- [ ] 能用 `dict.get()` 统计频次
- [ ] 能用 `set` 完成去重
- [ ] 能解释 `x in set_items` 和遍历 list 查找的差异

# Round 03 · Week 2 笔记（list/dict 与函数拆分）

## 本周目标

- 用 list 保存一组有顺序的数据。
- 用 dict 保存“键 -> 值”的统计结果。
- 把脚本拆成 2-3 个可复用函数。

## 在 Web UI 中怎么学

1. 点“练习：统计标签出现次数”的“运行”，查看自动生成的 `stats.py` 输出。
2. 点本周自测的“终端”，自己在 `~/cli-lab/round3` 下写一个小脚本。
3. 推荐自测命令：

```bash
mkdir week2_self
cd week2_self
printf 'def count_words(words):\n    result = {}\n    for word in words:\n        result[word] = result.get(word, 0) + 1\n    return result\n\nitems = ["python", "shell", "python", "git"]\nprint(count_words(items))\n' > count_words.py
python3 count_words.py
```

4. 能解释 list、dict、函数拆分后，再手动记录自测完成。

## list / dict 直觉

- list 像一排格子，适合保存“按顺序排列”的数据。
- dict 像查表，适合保存“名字 -> 次数”“用户 -> 分数”。
- `result.get(key, 0)` 的意思是：如果 key 已存在就取已有值，否则先当作 0。

## 函数拆分标准

一个脚本开始变长时，可以按“输入 -> 处理 -> 输出”拆分：

```python
def load_data():
    return ["error", "info", "error"]

def count_labels(items):
    result = {}
    for item in items:
        result[item] = result.get(item, 0) + 1
    return result

def main():
    data = load_data()
    print(count_labels(data))

main()
```

## 本周自查

- [ ] 能写出基础 list/dict 读写。
- [ ] 能解释 `dict.get(key, default)`。
- [ ] 能把脚本拆成 `load_data()`、`process()`、`main()` 这类结构。

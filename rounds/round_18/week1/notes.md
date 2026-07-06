# Round 18 · Week 1：NumPy 数组、shape、axis 与广播

## 本周目标

本周先建立数值计算的核心直觉：数据不只是 Python list，而是有形状、方向和统一类型的数组。后面的 pandas、sklearn、PyTorch 都会反复遇到这些概念。

## 页面内学习步骤

1. 在 Web UI 打开本文件，先读完 `ndarray`、`shape`、`dtype`、`axis`、广播、向量化这 6 个词。
2. 回到任务行，点击“练习：生成 NumPy 数组、axis 与广播示例”。
3. 运行结果里确认生成了 `array_concepts.json` 和 `static_check_report.json`。
4. 点击“终端练习”，在 `~/round18` 下完成下面的自测命令。
5. 打开“记录并完成”弹窗，写下你对 `axis=0` 和 `axis=1` 的一句话解释。

## 必会概念

| 概念 | 你要会说的人话 |
|---|---|
| `ndarray` | NumPy 的多维数组，适合装大量同类型数字 |
| `shape` | 数组长什么样，比如 `(3, 4)` 是 3 行 4 列 |
| `dtype` | 数组元素类型，比如整数、浮点数 |
| `axis=0` | 沿着行往下看，常见结果是“每一列”的统计 |
| `axis=1` | 沿着列横向看，常见结果是“每一行”的统计 |
| broadcasting | 小形状的数据自动对齐到大数组上做运算 |
| vectorization | 不手写 Python for，而让数组一次性完成运算 |

## 浏览器终端自测

```bash
pwd
mkdir -p r18_week1_self
printf 'matrix = [[1, 2, 3], [4, 5, 6]]\nprint([sum(row) for row in matrix])\nprint([sum(col) for col in zip(*matrix)])\n' > axis_demo.py
python3 axis_demo.py
```

期望你能解释：

- `[6, 15]` 是每一行的和。
- `[5, 7, 9]` 是每一列的和。
- 在 NumPy 中，这两个方向通常对应 `axis=1` 和 `axis=0`。

## 外部资料

- [NumPy Quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy Absolute Basics](https://numpy.org/doc/stable/user/absolute_beginners.html)

## 完成标准

- 自动练习任务已运行成功。
- 你能说清 `shape`、`dtype`、`axis` 和 broadcasting。
- 自测命令在 Web UI 终端里运行过，并把证据路径记录到任务记录里。

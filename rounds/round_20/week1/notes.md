# Round 20 · Week 1 笔记（Tensor、Dataset 与 DataLoader）

## Web UI 学习路径

1. 在 Round 20 面板打开本阅读任务。
2. 点击“练习：生成 tensor、Dataset 与 batch 示例”，生成 `~/cli-lab/round20/week1_auto/tensor_dataloader`。
3. 点击“终端练习”，按本页自测命令运行无依赖 batch smoke check。
4. 确认你能解释 tensor 形状、dtype、device、`Dataset` 和 `DataLoader` 的分工。

## 为什么先学 tensor

PyTorch 的数据和参数都围绕 tensor 展开。你可以先把 tensor 理解成“带有深度学习能力的多维数组”：

| 概念 | 要点 |
|---|---|
| shape | 数据有几维，每一维有多少个元素，例如 `(batch_size, features)` |
| dtype | 每个元素的类型，训练常见 `float32`，分类标签常见整数 |
| device | tensor 在 CPU 还是 GPU 上；入门先只用 CPU |
| autograd | PyTorch 能记录计算图并为参数求梯度 |
| NumPy 关系 | tensor 和 ndarray 都像数组，PyTorch tensor 还能参与自动微分和设备迁移 |

## Dataset 和 DataLoader

`Dataset` 负责“单条样本怎么取”，`DataLoader` 负责“如何按 batch、shuffle、多进程方式喂给训练循环”。

一个最小 `Dataset` 通常只需要三个部分：

- `__init__`：准备 `X` 和 `y`。
- `__len__`：告诉外界一共有多少条样本。
- `__getitem__`：按索引返回一条 `(features, label)`。

## 参考链接

- [PyTorch Learn the Basics](https://pytorch.org/tutorials/beginner/basics/intro.html)
- [PyTorch Tensors](https://pytorch.org/tutorials/beginner/basics/tensorqs_tutorial.html)
- [PyTorch Datasets & DataLoaders](https://pytorch.org/tutorials/beginner/basics/data_tutorial.html)

## 浏览器终端自测

先点击本周“运行脚本”按钮生成自动产物，再在 Web UI 终端中依次运行：

```bash
cd ~/round20/week1_auto/tensor_dataloader
python3 stdlib_batch_demo.py
cat batch_summary.json
```

看到 `rows`、`feature_count`、`batch_count` 和 `first_batch`，就说明你已经抓住了 batch 维度。

## 本周自查

- [ ] 能说出 tensor 的 shape / dtype / device 分别表示什么。
- [ ] 能解释 `Dataset` 和 `DataLoader` 谁负责“样本”，谁负责“batch”。
- [ ] 能在浏览器终端中运行 batch smoke check 并解释输出。

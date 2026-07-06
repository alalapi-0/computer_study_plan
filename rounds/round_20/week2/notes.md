# Round 20 · Week 2 笔记（nn.Module 与最小训练循环）

## Web UI 学习路径

1. 先读完本页，弄清 `nn.Module` 和训练循环的职责。
2. 点击“练习：生成 nn.Module 与训练循环示例”，生成 `~/cli-lab/round20/week2_auto/training_loop`。
3. 用浏览器“终端练习”运行标准库梯度下降 smoke check，验证“预测、loss、梯度、更新”的顺序。
4. 点击“记录并完成”保存自测记录：能看着输出说出一轮 batch 更新做了什么。

## nn.Module 的直觉

`nn.Module` 是 PyTorch 模型的基本单位。你在 `__init__` 里声明层，在 `forward` 里写输入如何流过这些层。

```python
class SimpleClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(4, 2)

    def forward(self, x):
        return self.linear(x)
```

入门阶段最重要的是分清：

| 部分 | 作用 |
|---|---|
| model | 负责把输入变成预测 |
| loss_fn | 衡量预测和真实标签差多远 |
| optimizer | 根据梯度更新参数 |
| backward | 从 loss 反向计算梯度 |
| zero_grad | 清掉上一轮梯度，避免累加污染 |

## 训练循环固定顺序

每个 batch 的核心顺序是：

1. `pred = model(X)`
2. `loss = loss_fn(pred, y)`
3. `optimizer.zero_grad()`
4. `loss.backward()`
5. `optimizer.step()`

有些教程把 `zero_grad()` 放在 batch 开头，有些放在 step 后面为下一轮准备。入门时只要记住：每次反向传播前必须清掉上一轮梯度。

## 参考链接

- [PyTorch Build the Neural Network](https://pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html)
- [PyTorch Optimizing Model Parameters](https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html)
- [torch.nn.Module](https://pytorch.org/docs/stable/generated/torch.nn.Module.html)

## 浏览器终端自测

先点击本周“运行脚本”按钮生成自动产物，再在 Web UI 终端中依次运行：

```bash
cd ~/round20/week2_auto/training_loop
python3 stdlib_gradient_demo.py
cat training_summary.json
```

如果 loss 逐步下降，就说明“根据梯度更新参数”这个动作已经跑通。

## 本周自查

- [ ] 能说明 `__init__` 和 `forward` 各写什么。
- [ ] 能按顺序说出训练循环五步。
- [ ] 能解释为什么训练前或每个 batch 中要清梯度。

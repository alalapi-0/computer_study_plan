# Round 20 · Week 3 笔记（eval、no_grad 与 checkpoint）

## Web UI 学习路径

1. 先读本页，理解训练模式和推理模式为什么不同。
2. 点击“练习：生成 eval/no_grad 与 checkpoint 示例”，生成 `~/cli-lab/round20/week3_auto/checkpoint_eval`。
3. 在浏览器终端运行标准库保存/加载权重 smoke check，确认 checkpoint 语义。
4. 点击“记录并完成”保存小抄和验收：能解释保存的是参数，不是训练魔法。

## eval 和 no_grad

训练和推理不是同一种运行状态：

| 写法 | 作用 |
|---|---|
| `model.train()` | 进入训练模式，Dropout / BatchNorm 等层按训练规则工作 |
| `model.eval()` | 进入评估/推理模式，相关层切换到稳定规则 |
| `torch.no_grad()` | 关闭梯度记录，推理更省内存，也避免误改计算图 |

入门时可以记一句：**评估前 `eval()`，只推理时包 `no_grad()`。**

## checkpoint 保存什么

最常见的做法是保存 `state_dict`：

```python
torch.save(model.state_dict(), "model.pt")
model.load_state_dict(torch.load("model.pt"))
model.eval()
```

`state_dict` 保存的是模型参数字典。要正确加载，通常还需要同一份模型结构代码。最终项目里建议把以下信息放进 manifest 或 README：

- 模型类名和输入输出形状。
- checkpoint 文件路径。
- 训练数据版本或样例。
- 评估指标和保存时间。

## 参考链接

- [PyTorch Save and Load the Model](https://pytorch.org/tutorials/beginner/basics/saveloadrun_tutorial.html)
- [PyTorch Autograd](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html)
- [torch.no_grad](https://pytorch.org/docs/stable/generated/torch.no_grad.html)

## 浏览器终端自测

先点击本周“运行脚本”按钮生成自动产物，再在 Web UI 终端中依次运行：

```bash
cd ~/cli-lab/round20/week3_auto/checkpoint_eval
python3 stdlib_checkpoint_demo.py
cat checkpoint_summary.json
```

## 本周自查

- [ ] 能说出 `model.eval()` 和 `torch.no_grad()` 的区别。
- [ ] 能解释为什么保存 `state_dict` 通常还需要保留模型结构代码。
- [ ] 能说明 checkpoint 目录里至少应该包含权重、manifest 和评估摘要。

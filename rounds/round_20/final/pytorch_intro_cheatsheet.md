# Round 20 · PyTorch 入门速查

## Web UI 收口顺序

1. 在 Round 20 面板完成三周阅读。
2. 依次运行三周自动练习，检查 `~/cli-lab/round20/week*_auto` 里的 `static_check_report.json`。
3. 运行最终综合练习，检查 `~/cli-lab/round20/final_auto/pytorch_intro_lab/final_static_check_report.json`。
4. 点击“记录并完成”保存本小抄任务和最终验收任务。

## 一句话主线

PyTorch 入门闭环是：把样本变成 tensor，用 `Dataset` / `DataLoader` 按 batch 喂给 `nn.Module`，在训练循环中计算 loss、反向传播并更新参数，评估时切到 `eval()` 和 `no_grad()`，最后保存 `state_dict` 并保留模型结构代码。

## 核心概念表

| 概念 | 记忆点 |
|---|---|
| Tensor | 多维数组，带 dtype / shape / device，可参与 autograd |
| Dataset | 描述“第 i 条样本怎么取” |
| DataLoader | 描述“如何按 batch / shuffle 喂数据” |
| nn.Module | 模型基类；`__init__` 定义层，`forward` 定义数据流 |
| loss | 衡量预测和标签的差距 |
| optimizer | 按梯度更新参数 |
| backward | 从 loss 反向计算梯度 |
| zero_grad | 清掉旧梯度，避免跨 batch 累加污染 |
| eval | 切换到评估/推理模式 |
| no_grad | 推理时不记录计算图 |
| state_dict | 模型参数字典，常用于保存和加载权重 |

## 最小训练循环

```python
for X_batch, y_batch in loader:
    pred = model(X_batch)
    loss = loss_fn(pred, y_batch)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

## 最小评估与保存

```python
model.eval()
with torch.no_grad():
    pred = model(X_test)

torch.save(model.state_dict(), "model.pt")
model.load_state_dict(torch.load("model.pt", map_location="cpu"))
model.eval()
```

## 依赖边界

- Web UI 自动练习不安装 PyTorch，只生成代码形状并跑标准库 smoke/static check。
- 真正运行 `torch` 示例时，建议在 Web UI 外准备单独虚拟环境。
- checkpoint 不只是一份 `.pt` 文件，还要保留模型结构代码、输入输出形状和评估摘要。

## 最终验收自问

- [ ] 我能解释 tensor 和 NumPy ndarray 的关系。
- [ ] 我能说明 `Dataset`、`DataLoader`、batch shape 的关系。
- [ ] 我能手写一个最小 `nn.Module`。
- [ ] 我能按顺序写出训练循环五步。
- [ ] 我能说明 `eval()`、`no_grad()`、`state_dict` 的作用。

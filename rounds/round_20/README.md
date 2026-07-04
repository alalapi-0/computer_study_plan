# Round 20 · PyTorch 入门

这个目录让 Round 20 可以通过 Web UI 完成：页面内阅读 notes，点击“运行”生成可检查练习产物，再用浏览器内终端完成手写自测。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round20`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## Web UI 完成顺序

1. 打开 `progress.html?round=round_20`。
2. 每周先点“阅读”，在弹窗中读完概念和自测命令。
3. 点“运行”生成自动练习产物。所有产物写入 `~/cli-lab/round20`。
4. 点“终端”完成手写自测，再手动记录自测、小抄和最终验收任务。

## 目录结构

```
round_20/
├─ README.md
├─ week1/ … week3/
└─ final/
```

## 自动练习边界

- 自动练习会生成 PyTorch 风格代码、标准库 smoke check、静态检查报告和最终项目包。
- Web UI 不执行 `pip install torch torchvision`，也不要求本机已有 PyTorch。
- 真实 PyTorch 示例保留在沙盒中，供你在单独准备好环境后手动运行。
- 脚本只自动记录对应“练习”任务；阅读、自测、小抄和验收仍由用户自己完成并在 Web UI 记录。

## 完成标准

- 能解释 tensor shape、dtype、device，以及 tensor 和 NumPy ndarray 的关系。
- 能说明 `Dataset.__len__`、`Dataset.__getitem__` 与 `DataLoader` batch 的关系。
- 能写出训练循环中的 `forward -> loss -> backward -> optimizer.step -> zero_grad`。
- 能说明 `model.eval()`、`torch.no_grad()`、`state_dict`、`torch.save` / `torch.load` 的作用。

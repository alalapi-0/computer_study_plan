# Round 21 · NLP 前置基础

这个目录是 Round 21（NLP 前置基础）的 Web UI 可完成练习内容。

> **仓库根**：`~/PycharmProjects/computer_study_plan`  
> **练习沙盒**：`~/cli-lab/round21`  
> 路径说明见 [`docs/WORKSPACE.md`](../../docs/WORKSPACE.md)。

## 使用方式

1. 启动本地 Web UI：

   ```bash
   python3 scripts/progress_server.py --host 127.0.0.1 --port 8787
   ```

2. 打开 `http://127.0.0.1:8787/progress.html?round=round_21`。
3. 在页面中依次点每周的“阅读”“运行”“终端”“记录 / 完成”。
4. 自动练习只写入 `~/cli-lab/round21`，不会修改仓库里的真实学习记录以外内容。
5. 自测任务使用浏览器映射终端里的短命令完成，最终小抄和验收题需要用户手动记录。

## 产物边界

- Web UI 自动练习会生成 PyTorch / Hugging Face / scikit-learn 风格代码形状。
- Web UI 自动练习不会安装 `torch`、`transformers`、`scikit-learn`，也不会下载预训练模型。
- 每周都会生成标准库 smoke check，确保用户无需额外依赖也能完成自测。
- 外部资料链接保留在 notes 和总览文档中，阅读器会以新标签页跳转。

## 目录结构

```text
round_21/
├─ README.md
├─ week1/
│  ├─ notes.md
│  └─ exercises.py
├─ week2/
│  ├─ notes.md
│  └─ exercises.py
├─ week3/
│  ├─ notes.md
│  └─ exercises.py
└─ final/
   ├─ comprehensive_exercise.py
   └─ nlp_prereq_cheatsheet.md
```

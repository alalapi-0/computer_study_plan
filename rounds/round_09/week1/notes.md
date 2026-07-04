# Round 09 · Week 1 笔记（仓库结构与文档）

## 本周目标

- 按最小可维护原则整理项目目录结构。
- 为项目补齐基础 README 与 `.gitignore` 认知。

## Web UI 学习路径

1. 在 Round 09 里打开本文件，先看清“规范化”的目的：让别人能运行、能看懂、不会把副产物提交进去。
2. 点击 `r09-w1-ex1` 的“运行”。脚本会在 `~/cli-lab/round9/week1_auto/ai_prep_tool` 生成：
   - `README.md`
   - `.gitignore`
   - `ai_prep_tool.py`
   - `tests/test_dedup.py`
   - `input/`、`output/`、`logs/`
   - `layout_report.txt`
3. 运行输出会列出 README 是否包含用途/运行方式、`.gitignore` 是否覆盖缓存/虚拟环境/输出/日志。
4. 点击 `r09-w1-self` 的“终端”，自己写 README 和 `.gitignore` 的最小版本。

## README 最小检查项

- 项目是什么。
- 怎么运行。
- 输入输出在哪里。
- 哪些文件不要提交。

## .gitignore 最小检查项

- Python 缓存：`__pycache__/`、`*.pyc`
- 虚拟环境：`.venv/`、`venv/`
- 输出副产物：`output/`、`logs/`、`*.log`
- 系统/编辑器：`.DS_Store`

## 浏览器终端自测命令

在 `r09-w1-self` 的终端里逐条运行：

```bash
mkdir week1_self
cd week1_self
mkdir tests input output logs
printf '# AI Prep Tool\n\n用于练习仓库规范化。\n\n## 运行\n\npython3 ai_prep_tool.py\n' > README.md
printf '__pycache__/\n*.pyc\n.venv/\nvenv/\noutput/\nlogs/\n*.log\n.DS_Store\n' > .gitignore
printf 'def dedup_records(items):\n    return list(dict.fromkeys(items))\nprint(dedup_records(["a", "b", "a"]))\n' > ai_prep_tool.py
python3 ai_prep_tool.py
ls
```

运行成功后，回到任务行手动点“记录 / 完成”。

## 本周自查

- [ ] 能说明为什么 README 是协作入口
- [ ] 能列出 `.gitignore` 至少 3 类应忽略内容
- [ ] 能说明为什么 `output/` 和 `logs/` 不应该进 Git

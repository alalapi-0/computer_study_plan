# Round 12 · Week 2 笔记（子进程与归档）

## Web UI 学习路径

1. 先阅读本文件，分清 `subprocess` 的返回码、stdout、stderr。
2. 点“运行脚本”执行 `week2/exercises.py`，它会在 `~/cli-lab/round12/week2_auto/archive_pipeline` 生成外部 worker、输出摘要和 zip 归档。
3. 点击“终端练习”，自己写一个 `subprocess_demo.py`，跑一次 `ls` 并打印返回码。
4. 用“记录并完成”写下：为什么自动化脚本不能只看 stdout，必须看 returncode。

## 本周目标

- 用 `subprocess.run(..., capture_output=True, text=True, check=False)` 调用一个批处理 worker。
- 用 returncode 判断外部命令是否成功。
- 用 `shutil.make_archive()` 把输出目录打包成 zip。
- 把命令报告写到 `command_report.json`，让下一步排查有证据。

## 关键区别

| 概念 | 作用 |
|---|---|
| `output/` | 当前这次批处理的可读结果 |
| `archive/` | 用于长期保存或传给别人的压缩归档 |
| `stdout` | 命令正常输出，不等于成功 |
| `returncode` | 命令退出状态，`0` 才是成功 |

## 浏览器终端自测

在 Round 12 页面点本周自测的“终端练习”，运行：

```bash
mkdir -p subprocess_self
printf 'import subprocess\nresult=subprocess.run(["ls","-la","."], capture_output=True, text=True, check=False)\nprint(result.returncode)\nprint(result.stdout.splitlines()[0])\n' > subprocess_self/subprocess_demo.py
python3 subprocess_self/subprocess_demo.py
```

看到返回码 `0` 后，点击“记录并完成”保存 `r12-w2-self` 的本次记录。

## 本周自查

- [ ] 能解释 `subprocess.run(..., check=False)` 与返回码含义。
- [ ] 能说明归档目录与输出目录的区别。
- [ ] 能说出为什么 zip 归档适合做“本次运行证据包”。

# Round 13 · Week 1 笔记（venv 与 requirements）

## Web UI 学习路径

1. 在 Round 13 页面先阅读本文。
2. 点击 `练习：生成 venv 结构与 requirements` 的“运行脚本”按钮。
3. 在运行结果里确认 `env_report.json`、`requirements.txt` 和 `.venv_demo/pyvenv.cfg` 都已生成。
4. 点击 `自测：自己创建 .venv_self` 的“终端练习”按钮，在浏览器终端中手敲下面的自测命令。
5. 自测完成后，点击“记录并完成”记录 `r13-w1-self`。

## 你要理解的事

- `venv` 解决的是“这个项目用哪一个 Python 解释器和哪一组依赖”。
- `requirements.txt` 解决的是“别人如何按同一份清单重建依赖”。
- 本仓库的 Web UI 练习默认不联网安装第三方包；本周先理解结构和复现流程。
- 真项目里可以用 `python3 -m pip freeze > requirements.txt` 导出依赖，但不要把临时环境、缓存和虚拟环境目录提交进仓库。

## 自动练习会做什么

脚本会在 `~/cli-lab/round13/week1_auto/env_basics` 下生成：

- `.venv_demo/`：使用标准库 `venv` 创建的演示环境。
- `requirements.txt`：一份可被 `pip install -r` 读取的依赖清单，本轮为了离线安全保持为空依赖并写清注释。
- `.gitignore`：忽略 `.venv*`、缓存、日志、输出。
- `env_report.json`：记录解释器、venv 配置、requirements 行数和复现建议。
- `next_steps.txt`：提示你自测时该手敲什么。

## 终端自测

在浏览器终端绑定 `r13-w1-self` 后执行：

```bash
pwd
mkdir week1_self
cd week1_self
python3 -m venv --without-pip .venv_self
ls .venv_self
cat .venv_self/pyvenv.cfg
python3 -m pip --version
printf '# no third-party deps yet\n' > requirements.txt
cat requirements.txt
```

不要在浏览器终端里执行 `pip install fastapi` 这类联网安装；当前安全模型会拦截 `pip` 命令，自动脚本也不会替你装依赖。

## 完成标准

- 能解释 `.venv_demo` 和 `requirements.txt` 分别解决什么问题。
- 能说出为什么虚拟环境目录应该被 `.gitignore` 忽略。
- 能在浏览器终端里自己创建一个 `.venv_self`。

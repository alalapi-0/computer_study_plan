# Round 01 · Week 1 笔记（路径感）

## 本周目标

- 分清“我现在在哪”“这里有什么”“我要去哪里”。
- 熟练使用 `pwd`、`ls`、`cd` 在目录间切换。
- 能解释当前目录、绝对路径、相对路径、`.`、`..` 的区别。

## 在 Web UI 里怎么学

1. 在 Round 01 第 1 周阅读本文件。
2. 点击“练习：路径切换实验”的“运行脚本”按钮，脚本会创建 `~/cli-lab/round1/notes`、`practice`、`test`。
3. 打开页面里的“终端练习”，从 `~/cli-lab` 开始手敲下面的命令。
4. 自己能不看提示完成自测后，再点击“记录并完成”保存自测记录。

## 核心概念

- 当前目录：终端命令正在操作的位置，用 `pwd` 查看。
- 绝对路径：从根或家目录开始写清楚位置，例如 `~/cli-lab/round1/notes`。
- 相对路径：从当前目录出发描述位置，例如在 `round1` 里进入 `notes` 只需要 `cd notes`。
- `.`：当前目录。
- `..`：上一级目录。

## 必练命令

```bash
cd ~/cli-lab/round1
pwd
ls
cd notes
pwd
cd ..
cd practice
pwd
cd ../test
pwd
cd ~/cli-lab/round1
pwd
```

## 判断自己是否真的会了

- 看到 `pwd` 的输出，能说出自己在 `round1`、`notes`、`practice` 还是 `test`。
- 不依赖复制粘贴，也能从 `notes` 回到 `round1`，再进入 `practice`。
- 能说出 `cd ../test` 的意思：先回上一级，再进入 `test`。

## 本周自测

不看上面的命令，独立完成：

1. 回到 `~/cli-lab/round1`
2. 进入 `notes`
3. 回上一级
4. 进入 `practice`
5. 进入 `test`
6. 回到 `~/cli-lab/round1`

完成后点击“记录并完成”，保存 `自测：不用提示切换目录` 的本次记录。

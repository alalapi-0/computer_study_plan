# Round 02 · Week 1 笔记（重定向与管道）

## 本周目标

- 理解 `>`、`>>`、`|` 的差异。
- 能写出简单的日志筛选流水线。
- 知道浏览器终端里要把步骤拆开，不用 `;`、`&&`、`||` 串命令。

## 在 Web UI 里怎么学

1. 阅读本文件后，点击“练习：覆盖与追加 / 去重统计 / 日志过滤流水线”的“运行脚本”按钮。
2. 脚本会在 `~/cli-lab/round2/week1/script_lab` 里生成 `fruits.txt`、`animals.txt`、`app.log` 等材料。
3. 自测时打开“终端练习”，进入 `~/cli-lab/round2/week1/self_check`，自己造一个小日志并统计 `error` 行数。
4. 能解释每个命令在流水线里做什么后，再点击“记录并完成”保存自测记录。

## 核心概念速查

| 概念 | 作用 | 常见示例 |
|---|---|---|
| 覆盖重定向 `>` | 把输出写入文件，会覆盖旧内容 | `echo "a" > a.txt` |
| 追加重定向 `>>` | 把输出追加到文件末尾 | `echo "b" >> a.txt` |
| 管道 `|` | 把左侧输出作为右侧输入 | `cat app.log \| grep error` |
| 计数 `wc -l` | 统计行数 | `grep error app.log \| wc -l` |

## 推荐手敲流程

```bash
cd ~/cli-lab/round2/week1/self_check
echo "error: login failed" > app.log
echo "info: job started" >> app.log
echo "error: file missing" >> app.log
cat app.log
grep "error" app.log | wc -l
grep "info" app.log > info_only.txt
cat info_only.txt
```

## 判断自己是否真的会了

- `>` 会覆盖，`>>` 会追加。
- `grep "error" app.log | wc -l` 里，`grep` 先筛出匹配行，`wc -l` 再统计行数。
- 管道能少写中间文件，但如果你想保留结果，就可以把最后一步重定向到文件。

## 本周自测

不看上面的命令，独立完成：

1. 在 `~/cli-lab/round2/week1/self_check` 下创建 `app.log`
2. 写入至少 4 行日志，其中至少 2 行包含 `error`
3. 用一条管道统计 `error` 行数
4. 把 `info` 行保存到 `info_only.txt`
5. 用自己的话解释 `>`、`>>`、`|`

完成后点击“记录并完成”，保存 `自测：独立写日志统计链` 的本次记录。

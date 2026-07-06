# Round 01 · Week 3 笔记（查看文件与查帮助）

## 本周目标

- 了解 `cat`、`less`、`head`、`tail` 的适用场景。
- 形成“不会就先查 `man`”的习惯。
- 能快速查看文件开头、结尾，并退出分页或帮助界面。

## 在 Web UI 里怎么学

1. 阅读本文件后，点击“练习：查看文本与查帮助”的“运行脚本”按钮。
2. 脚本会在 `~/cli-lab/round1/week3` 里创建 `study_log.txt`，并演示 `cat`、`head`、`tail`。
3. `less` 和 `man` 在浏览器终端里会以捕获输出的形式展示；如果以后在真实系统终端里打开分页界面，按 `q` 退出。
4. 自测完成后，点击“记录并完成”保存本次记录。

## 命令分工

- `cat <file>`：一次性输出短文件。
- `less <file>`：分页查看长文件；浏览器终端会直接显示输出，真实终端中按方向键滚动、按 `q` 退出。
- `head <file>`：查看文件开头；`head -n 3 <file>` 只看前 3 行。
- `tail <file>`：查看文件结尾；`tail -n 4 <file>` 只看最后 4 行。
- `man <command>`：查看命令帮助；先看简介，再找一两个参数；真实终端中按 `q` 退出。

## 推荐手敲流程

```bash
cd ~/cli-lab/round1/week3
cat study_log.txt
head study_log.txt
head -n 3 study_log.txt
tail study_log.txt
tail -n 4 study_log.txt
less study_log.txt
man ls
```

在浏览器终端里，`less` / `man` 会直接返回输出；在真实系统终端里，如果打开后不知道怎么返回，按 `q`。

## 本周自测

- 能解释什么时候用 `cat`，什么时候用 `less`。
- 能用 `head -n 3 study_log.txt` 看前三行。
- 能用 `tail -n 4 study_log.txt` 看最后四行。
- 能打开 `man ls`，找到 `-l` 或 `-a` 的含义；知道真实终端里按 `q` 退出。

完成后点击“记录并完成”，保存 `自测：head / tail / man` 的本次记录。

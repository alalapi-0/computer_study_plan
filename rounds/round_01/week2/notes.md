# Round 01 · Week 2 笔记（文件操作）

## 本周目标

- 练熟 `mkdir`、`touch`、`cp`、`mv`、`rm`。
- 形成“先确认路径，再做删除”的操作习惯。
- 能独立完成创建目录、创建文件、复制、移动、改名、删除测试文件。

## 在 Web UI 里怎么学

1. 阅读本文件后，点击“练习：创建 / 复制 / 改名 / 删除”的运行按钮。
2. 脚本会在 `~/cli-lab/round1/week2` 中创建 `input`、`output`、`backup` 并演示复制、改名、删除。
3. 自测时打开“练习终端”，在 `~/cli-lab/round1` 里独立做一遍 `week2_test`。
4. 删除只删自己刚创建的测试文件；练习终端会拦截递归、强制、绝对路径等危险删除。

## 命令分工

- `mkdir <dir>`：创建目录。
- `touch <file>`：创建空文件，适合准备测试文件。
- `cp <src> <dst>`：复制文件，原文件仍然保留。
- `mv <src> <dst>`：移动文件；如果目标是新名字，就是改名。
- `rm <file>`：删除文件；Round 01 只练删除普通测试文件。

## 推荐手敲流程

```bash
cd ~/cli-lab/round1
mkdir week2_test
cd week2_test
mkdir input output backup
touch input/x.txt input/y.txt
cp input/x.txt backup/x_copy.txt
mv input/y.txt output/result.txt
touch delete_me.txt
pwd
ls
rm delete_me.txt
find . -maxdepth 3 -type f | sort
```

## 删除前的固定检查

每次 `rm` 前先做三件事：

1. `pwd`：确认自己在 `~/cli-lab/round1` 或其子目录。
2. `ls`：确认目标文件确实是测试文件。
3. `rm <file>`：只删除明确的单个文件。

本轮不要练 `rm -r`、`rm -f`、`rm *`，也不要删除仓库和真实资料中的文件。

## 本周自测

不看命令，独立完成：

1. 在 `~/cli-lab/round1` 下创建 `week2_test`
2. 进入该目录
3. 创建 `input`、`output`、`backup`
4. 创建 `x.txt`、`y.txt`
5. 复制 `x.txt` 到 `backup`
6. 把 `y.txt` 改名成 `result.txt`
7. 删除一个自己创建的测试文件

完成后在 Web UI 中手动标记 `自测：独立整理 week2_test`。

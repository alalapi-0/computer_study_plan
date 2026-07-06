# Round 02 · Week 2 笔记（最小 Shell 脚本）

## 本周目标

- 理解最小 Shell 脚本的结构。
- 能把重复命令封装成可复用脚本。
- 能在浏览器终端里用 `printf` 写一个很小的 `.sh` 文件并用 `bash` 运行。

## 在 Web UI 里怎么学

1. 阅读本文件后，点击 Week 2 的三个“运行脚本”按钮。
2. 脚本会在 `~/cli-lab/round2/week2/script_lab` 里生成 `count_errors.sh`、`count_labels.sh`、`show_args.sh`。
3. 自测时打开“终端练习”，进入 `~/cli-lab/round2/week2/self_check`，用 `printf` 写一个最小参数脚本。
4. 能解释 `$1`、`$@`、`$#` 的含义后，再在 Web UI 中手动标记自测任务。

## 脚本基础结构

| 组成 | 说明 | 示例 |
|---|---|---|
| shebang | 告诉系统用哪个解释器执行 | `#!/bin/bash` |
| 命令主体 | 平时手敲的命令序列 | `grep ... | wc -l` |
| 参数变量 | 从命令行读取参数 | `$1`, `$2`, `$@`, `$#` |

## 参数速查

| 变量 | 含义 |
|---|---|
| `$0` | 脚本名 |
| `$1` | 第一个参数 |
| `$@` | 全部参数 |
| `$#` | 参数个数 |

## 推荐手敲流程

浏览器终端不是编辑器，所以用 `printf` 快速写小脚本：

```bash
cd ~/cli-lab/round2/week2/self_check
printf '%s\n' '#!/bin/bash' 'echo "first arg: $1"' 'echo "all args: $@"' 'echo "arg count: $#"' > show_args_self.sh
bash show_args_self.sh one two three
```

## 练习节奏

1. 先能写死输入文件的脚本。
2. 再改成接受参数（例如日志文件名）。
3. 每次运行前先 `cat script_name.sh` 看脚本内容，确认自己知道它要做什么。

## 本周完成后你应该能回答

- [ ] 为什么脚本能减少重复劳动？
- [ ] `$@` 与 `$#` 分别在什么场景有用？
- [ ] 什么情况下会把输出重定向到文件而不是直接打印？

## 本周自测

不看上面的命令，独立完成：

1. 在 `~/cli-lab/round2/week2/self_check` 下创建 `show_args_self.sh`
2. 让它至少输出第一个参数和参数个数
3. 用 `bash show_args_self.sh one two` 运行
4. 能解释 `$1`、`$@`、`$#` 的区别

完成后在 Web UI 中手动标记 `自测：运行并解释参数脚本`。

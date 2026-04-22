# Round 06 · Linux 进阶与自动化

> **定位**：不再是"会用几个命令"，而是开始形成真正的工程手感：能批量找文件、能做文本处理、能管理长任务、能远程连机器、能做最基础的定时自动化。

---

## 概览

| 项目 | 内容 |
|------|------|
| **主题** | find/xargs、sed/awk、进程管理、SSH、crontab、tmux |
| **难度** | ⭐⭐⭐☆☆ |
| **周期** | 3 周，每周约 8 小时 |
| **前置** | Round 05 |
| **下一轮** | Round 07 · 面向 AI 项目的综合练习 |

---

## 本轮目标

完成本轮后，你能做到：

- [ ] 用 `find` + `xargs` 批量处理文件
- [ ] 用 `sed` 做简单文本替换，用 `awk` 按列取值
- [ ] 用 `ps`、`top`、`kill` 观察和控制进程
- [ ] 用 `nohup` 或 `tmux` 保住长任务
- [ ] 用 `ssh`、`scp`、`rsync` 做远程连接和文件传输
- [ ] 用 `crontab` 做最小定时任务

---

## 本轮不学什么

> 先不碰：systemd 服务编写、复杂 shell 脚本框架、网络防火墙、Docker 编排、复杂权限模型

---

## 推荐资源

| 类型 | 资源 | 说明 |
|------|------|------|
| 🎬 主视频 | [MIT Missing Semester – Command-line Environment](https://missing.csail.mit.edu/2020/command-line/) | 整体感，讲输入输出流/环境变量/SSH |
| 📄 文档 1 | [GNU Findutils Manual](https://www.gnu.org/software/findutils/manual/html_mono/find.html) | `find`、`xargs` 权威手册 |
| 📄 文档 2 | [GNU sed Manual](https://www.gnu.org/software/sed/manual/sed.html) / [GNU awk](https://www.gnu.org/software/gawk/manual/) | stream editor + 按模式处理 |
| 🖥️ 工具文档 | [tmux Wiki](https://github.com/tmux/tmux/wiki) | 终端复用，支持 detach/reattach |
| 🔐 SSH 文档 | [OpenSSH Manual](https://www.openssh.com/manual.html) | 远程登录核心工具 |
| 📤 传输工具 | [rsync man page](https://linux.die.net/man/1/rsync) | 增量同步，快速高效 |
| ⏰ 定时任务 | [crontab(5)](https://man7.org/linux/man-pages/man5/crontab.5.html) / [nohup](https://www.gnu.org/software/coreutils/manual/html_node/nohup-invocation.html) | 定时执行 + 后台保活 |

---

## 3 周学习安排

### 第 1 周：文件查找与文本处理

**目标**：别再手动翻文件夹，学会批量找和批量筛。

**本周要练的命令**：`find`、`xargs`、`sed`、`awk`

**核心理解**：
- `find`：查找满足条件的文件，可配合 `-exec` 或 `xargs` 执行动作
- `xargs`：把标准输入的参数组装成命令行再执行
- `sed`：stream editor，擅长一趟式文本替换（`s/old/new/g`）
- `awk`：按模式选记录并执行操作，擅长按列取值和统计

---

### 第 2 周：进程管理和长任务保活

**目标**：知道进程在哪、怎么控制它、怎么让任务不因为终端关闭而死掉。

**本周要练的命令**：`ps`、`top`、`kill`、`nohup`、`tmux`

**核心理解**：
- `ps aux`：查看所有运行中的进程
- `kill -9 PID`：强制终止进程
- `nohup`：忽略 hangup 信号，退出登录后命令继续运行
- `tmux`：终端复用，可以 detach 后再 reattach

---

### 第 3 周：远程连接与定时自动化

**目标**：能远程连上服务器，会做最简单的定时任务。

**本周要练的命令**：`ssh`、`scp`、`rsync`、`crontab`

**核心理解**：
- `ssh user@host`：远程登录
- `scp file user@host:path`：安全复制文件
- `rsync -avz src/ dest/`：增量同步，远比 cp 聪明
- `crontab -e`：编辑定时任务，`* * * * *` 是分/时/日/月/周

---

## 本轮练习清单

### 准备工作

```bash
mkdir -p ~/cli-lab/round6
cd ~/cli-lab/round6
mkdir test_files
```

---

### 第 1 周练习

**练习 1**：`find` 基础
```bash
# 在当前目录下找所有 .txt 文件
find ~/cli-lab -name "*.txt"

# 找最近 7 天修改过的文件
find ~/cli-lab -mtime -7

# 找大于 1KB 的文件
find ~/cli-lab -size +1k

# 找到文件后执行动作（查看文件名）
find ~/cli-lab -name "*.txt" -exec echo "Found: {}" \;
```

**练习 2**：`find` + `xargs`
```bash
# 批量统计 .txt 文件的行数
find ~/cli-lab -name "*.txt" | xargs wc -l

# 批量 grep（注意：-0 处理含空格文件名）
find ~/cli-lab -name "*.txt" -print0 | xargs -0 grep -l "error"
```

**练习 3**：`sed` 文本替换
```bash
cd ~/cli-lab/round6/test_files
echo "hello world" > test.txt
echo "world is great" >> test.txt
echo "hello again" >> test.txt

# 替换（不修改文件，只打印）
sed 's/hello/hi/g' test.txt

# 替换并写回（-i 表示 in-place）
sed -i 's/world/earth/g' test.txt
cat test.txt
```

**练习 4**：`awk` 按列处理
```bash
# 创建一个类似 CSV 的文件
echo "alice 85 math" > scores.txt
echo "bob 92 science" >> scores.txt
echo "carol 78 math" >> scores.txt

# 打印第 1 列（姓名）
awk '{print $1}' scores.txt

# 打印姓名和分数
awk '{print $1, $2}' scores.txt

# 统计分数总和
awk '{sum += $2} END {print "Total:", sum}' scores.txt

# 筛选分数 > 80 的行
awk '$2 > 80 {print $1, "passed"}' scores.txt
```

---

### 第 2 周练习

**练习 5**：进程查看
```bash
# 查看所有进程
ps aux

# 找特定进程（比如 Python）
ps aux | grep python

# 查看实时进程状态（按 q 退出）
top
```

**练习 6**：后台运行与 nohup
```bash
# 在后台运行命令（会在终端关闭时死掉）
sleep 100 &

# 查看后台任务
jobs

# nohup 方式（终端关闭后继续运行）
nohup sleep 200 > ~/cli-lab/round6/nohup.log 2>&1 &
ps aux | grep sleep
```

**练习 7**：tmux 基础
```bash
# 启动一个新 session
tmux new -s round6

# 在 session 里启动一个长任务
sleep 300

# 按 Ctrl+b d 脱离（detach）session
# 此时关闭终端也没关系

# 重新连回 session
tmux attach -t round6

# 列出所有 session
tmux ls
```

---

### 第 3 周练习

**练习 8**：SSH 基础（需要有一台 Linux 机器或服务器）
```bash
# 连接远程服务器
ssh username@your-server-ip

# 免密登录配置
ssh-keygen -t ed25519     # 生成密钥对
ssh-copy-id user@host     # 把公钥传到服务器
ssh user@host             # 之后不再需要密码
```

**练习 9**：文件传输
```bash
# scp：简单复制
scp local_file.txt user@host:~/remote_dir/

# rsync：增量同步（只传差异部分）
rsync -avz ~/cli-lab/round6/ user@host:~/remote_round6/

# 从服务器拉取
rsync -avz user@host:~/remote_dir/ ~/local_dir/
```

**练习 10**：crontab 定时任务
```bash
# 编辑 crontab
crontab -e

# crontab 格式：分 时 日 月 周 命令
# 每分钟运行一次（测试用）
* * * * * echo "ping" >> ~/cli-lab/round6/cron.log

# 每天 2 点运行备份脚本
0 2 * * * bash ~/cli-lab/backup.sh >> ~/cli-lab/round6/backup.log 2>&1

# 查看当前 crontab
crontab -l

# 删除所有 crontab
crontab -r
```

---

### 综合小项目：批量文件处理脚本

```bash
#!/bin/bash
# batch_process.sh：批量处理 input 目录下所有 .txt 文件

INPUT_DIR=~/cli-lab/round6/input
OUTPUT_DIR=~/cli-lab/round6/output
LOG_FILE=~/cli-lab/round6/process.log

mkdir -p "$INPUT_DIR" "$OUTPUT_DIR"

echo "[$(date)] Starting batch process" >> "$LOG_FILE"

find "$INPUT_DIR" -name "*.txt" | while read -r file; do
    filename=$(basename "$file")
    output="$OUTPUT_DIR/processed_$filename"
    
    # 去掉空行，转小写
    sed '/^$/d' "$file" | awk '{print tolower($0)}' > "$output"
    
    echo "[$(date)] Processed: $filename" >> "$LOG_FILE"
done

echo "[$(date)] Done. Processed files:" >> "$LOG_FILE"
ls "$OUTPUT_DIR" >> "$LOG_FILE"
```

---

## 常用命令速查

| 命令 | 常见用法 | 说明 |
|------|---------|------|
| `find` | `find . -name "*.py"` | 按条件查文件 |
| `xargs` | `find . -name "*.py" \| xargs grep "def"` | 把输入组装成命令 |
| `sed` | `sed 's/old/new/g' file` | 流式替换 |
| `awk` | `awk '{print $1}' file` | 按列取值 |
| `ps aux` | `ps aux \| grep python` | 查进程 |
| `kill` | `kill -9 PID` | 终止进程 |
| `nohup` | `nohup cmd > log 2>&1 &` | 后台不死任务 |
| `tmux` | `tmux new -s name` | 终端复用 |
| `ssh` | `ssh user@host` | 远程登录 |
| `rsync` | `rsync -avz src/ dest/` | 增量同步 |
| `crontab` | `crontab -e` | 编辑定时任务 |

---

## 验收标准

- [ ] 能用 `find` + `xargs` 批量处理一组文件
- [ ] 能用 `sed` 做简单的文本替换
- [ ] 能用 `awk` 按列过滤和统计
- [ ] 能用 `nohup` 或 `tmux` 保住一个长任务
- [ ] 能用 `crontab` 设置一个每分钟运行的测试任务

---

## ⚠️ 最容易踩的坑

1. **`sed -i` 不备份** — 修改前先 `cp file file.bak`，或用 `sed -i.bak`
2. **`find` + `xargs` 文件名有空格** — 用 `find -print0 | xargs -0` 来安全处理
3. **`journalctl` 是 systemd/Linux 工具** — macOS 本地不能练，适合在 Linux 服务器上用

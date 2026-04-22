#!/bin/bash
# =============================================================
# Round 00 · 综合练习脚本
# 把本轮学到的所有命令串起来做一遍
#
# 本脚本对应 progress.json 中的任务：
#   fin-comp  → 综合练习完成
#   fin-sheet → 命令小抄完成（需手动填写后确认）
#   fin-acc1  → 验收1：能解释 Terminal vs Shell
#   fin-acc2  → 验收2：能用所有7个命令
#   fin-acc3  → 验收3：目录和小抄存在
# =============================================================

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

echo "========================================"
echo "Round 00 综合练习"
echo "本轮学过的命令：pwd / ls / cd / mkdir / touch / cat / man"
echo "========================================"
echo ""

# 步骤1：创建综合练习目录
echo ">>> 步骤1：创建综合练习目录"
cd ~/cli-lab/round0
mkdir -p week0_lab/notes week0_lab/practice
echo "创建完成，结构如下："
ls week0_lab/
echo ""

# 步骤2：进入目录
echo ">>> 步骤2：进入目录"
cd ~/cli-lab/round0/week0_lab
pwd
echo ""

# 步骤3：创建文件
echo ">>> 步骤3：创建文件"
touch notes/commands.txt
touch practice/todo.txt
echo "notes/ 里的文件：$(ls notes/)"
echo "practice/ 里的文件：$(ls practice/)"
echo ""

# 步骤4：写入内容
echo ">>> 步骤4：写入内容"
echo "learn terminal basics" > practice/todo.txt
echo "写入了：$(cat practice/todo.txt)"
echo ""

# 步骤5：查看文件
echo ">>> 步骤5：查看文件内容"
cat practice/todo.txt
echo ""

# 步骤6：查 man 手册
echo ">>> 步骤6：查 man ls（按回车打开，看完按 q 退出）"
read
man ls

echo ""
echo "========================================"
echo "综合练习完成！标记进度..."
echo "========================================"
mark fin-comp

echo ""
echo "接下来请手动填写命令小抄："
echo "  文件：$REPO_ROOT/rounds/round_00/final/command_cheatsheet.md"
echo ""
echo "填好后按回车确认..."
read
mark fin-sheet

echo ""
echo "最终验收（请逐项确认）："
echo ""
echo "验收1：你能解释 Terminal 是应用，Shell 是里面的命令接收程序吗？"
echo "       确认后按回车..."
read
mark fin-acc1

echo ""
echo "验收2：你能不查笔记地使用 pwd / ls / cd / mkdir / touch / cat / man 吗？"
echo "       随便用几个试试，然后按回车确认..."
read
mark fin-acc2

echo ""
echo "验收3：~/cli-lab/round0 目录存在，里面有命令小抄吗？"
ls ~/cli-lab/round0/notes/ 2>/dev/null || echo "(目录不存在，请先完成练习1)"
echo "       确认后按回车..."
read
mark fin-acc3

echo ""
echo "🎉🎉 Round 00 全部完成！"
echo "   打开 progress.html 查看你的进度（需要先启动本地服务器）"
echo "   启动命令：cd '$REPO_ROOT' && python3 -m http.server 8000"
echo "   然后在浏览器打开：http://localhost:8000/progress.html"

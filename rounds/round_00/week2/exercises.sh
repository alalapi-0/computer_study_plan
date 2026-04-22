#!/bin/bash
# =============================================================
# Round 00 · Week 2 练习脚本
# 主题：mkdir / touch / cat
# 用法：把每个练习的命令在终端里手敲一遍，观察输出
#
# 本脚本对应 progress.json 中的任务：
#   w2-read  → 阅读 week2/notes.md（手动运行：bash mark_done.sh w2-read）
#   w2-ex4   → 练习4：创建更多子目录
#   w2-ex5   → 练习5：创建空文件
#   w2-ex6   → 练习6：查看空文件
#   w2-ex7   → 练习7：写入内容再查看
#   w2-self  → 第2周自测
# =============================================================

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

# -------------------------------------------------------------
# 练习 4：创建更多子目录
# -------------------------------------------------------------
echo "========================================"
echo "练习 4：创建更多子目录"
echo "========================================"

cd ~/cli-lab/round0

echo ">>> 创建 logs、drafts、tmp 子目录："
mkdir -p logs drafts tmp
echo ""
echo ">>> 当前 round0 的内容："
ls
echo ""
echo "[ 练习4 完成 ] 你能看到刚才创建的目录吗？"
echo ""
mark w2-ex4

# -------------------------------------------------------------
# 练习 5：创建空文件
# -------------------------------------------------------------
echo "========================================"
echo "练习 5：创建空文件"
echo "========================================"

cd ~/cli-lab/round0

echo ">>> 在 notes/ 下创建 commands.txt 和 questions.txt："
touch notes/commands.txt
touch notes/questions.txt

echo ""
echo ">>> 在 practice/ 下创建 todo.txt："
touch practice/todo.txt

echo ""
echo ">>> 查看 notes/ 的内容："
ls notes

echo ""
echo ">>> 查看 practice/ 的内容："
ls practice

echo ""
echo "[ 练习5 完成 ]"
echo ""
mark w2-ex5

# -------------------------------------------------------------
# 练习 6：查看空文件
# -------------------------------------------------------------
echo "========================================"
echo "练习 6：查看空文件"
echo "========================================"

cd ~/cli-lab/round0

echo ">>> cat practice/todo.txt（文件是空的，不会有输出）："
cat practice/todo.txt
echo "(上面没有输出是正常的，因为文件是空的)"
echo ""
echo "[ 练习6 完成 ]"
echo ""
mark w2-ex6

# -------------------------------------------------------------
# 练习 7：写入内容再查看
# -------------------------------------------------------------
echo "========================================"
echo "练习 7：写入内容再查看"
echo "========================================"

cd ~/cli-lab/round0

echo ">>> 把一行文字写入 practice/todo.txt："
echo "practice pwd ls cd" > practice/todo.txt

echo ""
echo ">>> 用 cat 查看文件内容："
cat practice/todo.txt

echo ""
echo ">>> 再写一行（用 >> 追加，不覆盖）："
echo "practice mkdir touch cat" >> practice/todo.txt
cat practice/todo.txt

echo ""
echo "[ 练习7 完成 ] 注意 > 和 >> 的区别：> 覆盖，>> 追加"
echo ""
mark w2-ex7

# -------------------------------------------------------------
# 第 2 周自测
# -------------------------------------------------------------
echo "========================================"
echo "第 2 周自测"
echo "========================================"
echo "请在终端里独立完成（不看上面的提示）："
echo "  1. 在 ~/cli-lab/round0 下创建 week2_test 目录"
echo "  2. 在里面创建 a.txt 和 b.txt"
echo "  3. 用 cat 查看其中一个文件"
echo "  4. 在 notes/commands.txt 里写下今天学会的命令"
echo "     提示：echo 'mkdir: 创建目录' >> ~/cli-lab/round0/notes/commands.txt"
echo ""
echo "完成后按回车确认，进度将自动记录..."
read
mark w2-self

echo ""
echo "🎉 Week 2 所有练习完成！"
echo "   请阅读 week2/notes.md，然后运行：bash mark_done.sh w2-read"

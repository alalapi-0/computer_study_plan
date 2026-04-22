#!/bin/bash
# =============================================================
# Round 00 · Week 1 练习脚本
# 主题：pwd / ls / cd
# 用法：把每个练习的命令在终端里手敲一遍，观察输出
#       不要只读，一定要自己敲！
#
# 本脚本对应 progress.json 中的任务：
#   w1-read  → 阅读 week1/notes.md（手动运行：bash mark_done.sh w1-read）
#   w1-ex1   → 练习1：认识当前位置
#   w1-ex2   → 练习2：创建子目录并切换
#   w1-ex3   → 练习3：绝对路径 vs 相对路径
#   w1-self  → 第1周自测
# =============================================================

# 仓库根目录（exercises.sh 位于 rounds/round_00/week1/，根目录是 ../../..）
REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

# -------------------------------------------------------------
# 准备工作：先建练习目录（只需执行一次）
# -------------------------------------------------------------
echo ">>> 准备工作：创建 ~/cli-lab/round0"
mkdir -p ~/cli-lab/round0
cd ~/cli-lab/round0
echo "当前位置：$(pwd)"
echo ""

# -------------------------------------------------------------
# 练习 1：认识当前位置
# 目标：体会 pwd 和 ls 的输出
# -------------------------------------------------------------
echo "========================================"
echo "练习 1：认识当前位置"
echo "========================================"

echo ">>> 运行 pwd："
cd ~/cli-lab/round0
pwd

echo ""
echo ">>> 运行 ls（应该是空的，刚创建的目录）："
ls

echo ""
echo "[ 练习1 完成 ] 你看到了什么？记录在 week1/notes.md 里。"
echo ""
mark w1-ex1

# -------------------------------------------------------------
# 练习 2：创建子目录并切换
# 目标：体会 cd 的几种写法
# -------------------------------------------------------------
echo "========================================"
echo "练习 2：创建子目录并切换"
echo "========================================"

echo ">>> 创建 notes 和 practice 子目录："
mkdir -p ~/cli-lab/round0/notes
mkdir -p ~/cli-lab/round0/practice
ls ~/cli-lab/round0

echo ""
echo ">>> 进入 notes，查看位置："
cd ~/cli-lab/round0/notes
pwd

echo ""
echo ">>> 回到上一级（cd ..）："
cd ..
pwd

echo ""
echo ">>> 进入 practice，查看位置："
cd practice
pwd

echo ""
echo ">>> 用绝对路径回到 round0："
cd ~/cli-lab/round0
pwd

echo ""
echo "[ 练习2 完成 ]"
echo ""
mark w1-ex2

# -------------------------------------------------------------
# 练习 3：绝对路径 vs 相对路径
# 目标：分清两种路径写法
# -------------------------------------------------------------
echo "========================================"
echo "练习 3：绝对路径 vs 相对路径"
echo "========================================"

echo ">>> 当前位置："
cd ~/cli-lab/round0
pwd

echo ""
echo ">>> 用绝对路径进入 notes："
cd ~/cli-lab/round0/notes
pwd

echo ""
echo ">>> 用 cd .. 回上级："
cd ..
pwd

echo ""
echo ">>> 用相对路径进入 practice（从 round0 出发）："
cd practice
pwd

echo ""
echo ">>> 用相对路径 ../notes（先回上级，再进 notes）："
cd ../notes
pwd

echo ""
echo ">>> 回到 round0："
cd ~/cli-lab/round0
pwd

echo ""
echo "[ 练习3 完成 ]"
echo ""
mark w1-ex3

# -------------------------------------------------------------
# 第 1 周自测
# 需要你手敲完5步后再确认
# -------------------------------------------------------------
echo "========================================"
echo "第 1 周自测（请自己手敲，不要复制粘贴）"
echo "========================================"
echo "请在终端里依次完成："
echo "  1. 回到 ~/cli-lab/round0"
echo "  2. 进入 notes"
echo "  3. 回上一级"
echo "  4. 进入 practice"
echo "  5. 回到 ~/cli-lab/round0"
echo ""
echo "完成后按回车确认，进度将自动记录..."
read
mark w1-self

echo ""
echo "🎉 Week 1 所有练习完成！"
echo "   请阅读 week1/notes.md，然后运行：bash mark_done.sh w1-read"

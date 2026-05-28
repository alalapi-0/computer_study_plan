#!/bin/bash
# Round 01 · Final 综合练习

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round1/final_lab/{input,output,backup,notes}
cd ~/cli-lab/round1/final_lab

touch input/raw1.txt input/raw2.txt
cp input/raw1.txt backup/
mv input/raw2.txt output/final_raw2.txt

cat > notes/round1_notes.txt <<'EOF'
pwd: 查看当前路径
ls: 查看目录内容
cd: 切换目录
mkdir: 创建目录
touch: 创建文件
cp: 复制文件
mv: 移动或改名
rm: 删除文件
cat/less/head/tail: 查看文本
EOF

mark r01-fin-comp

echo "请检查 rounds/round_01/final/command_cheatsheet.md 后按回车..."
read
mark r01-fin-sheet

echo "请确认你可以解释本轮核心命令后按回车..."
read
mark r01-fin-acc1

echo "综合练习完成，结果如下："
ls -R

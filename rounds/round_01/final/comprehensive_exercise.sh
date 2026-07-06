#!/bin/bash
# Round 01 · Final 综合练习

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round1/study_files_lab/{input,output,backup,notes}
cd ~/cli-lab/round1/study_files_lab

echo "Round 01 Final：迷你文件整理实验室"
echo

touch input/raw1.txt input/raw2.txt input/raw3.txt
cp input/raw1.txt backup/
mv input/raw2.txt output/
mv input/raw3.txt input/final_raw3.txt

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

echo "综合练习完成，结果如下："
find . -maxdepth 3 -type f | sort
echo
echo "脚本已完成综合练习任务 r01-fin-comp。"
echo "下一步：在 Web UI 中检查 command_cheatsheet.md，确认小抄和验收后点击“记录并完成”保存 r01-fin-sheet 与 r01-fin-acc1。"

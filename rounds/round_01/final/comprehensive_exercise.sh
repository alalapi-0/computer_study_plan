#!/bin/bash
# Round 01 · Final 综合练习

set -e

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

echo "综合练习完成，结果如下："
ls -R

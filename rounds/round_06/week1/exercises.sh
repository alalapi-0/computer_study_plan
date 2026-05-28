#!/bin/bash
# Round 06 · Week 1 练习：find / xargs / sed / awk

set -e

mkdir -p ~/cli-lab/round6/week1
cd ~/cli-lab/round6/week1

cat > sample.log <<'EOF'
INFO startup ok
WARN disk usage high
ERROR timeout at api
INFO retry success
EOF

echo "包含 ERROR 的行："
grep "ERROR" sample.log

echo "统一替换 INFO -> LOG："
sed 's/INFO/LOG/g' sample.log

echo "按列提取等级字段："
awk '{print $1}' sample.log

echo "请补充一个 find + xargs 批处理命令后按回车继续..."
read
echo "Week 1 完成。"

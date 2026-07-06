#!/bin/bash
# Round 06 · Week 1 练习：find / xargs / sed / awk（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round6/week1_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB/logs" "$LAB/reports"
cd "$LAB"

cat > logs/app.log <<'EOF'
INFO startup ok
WARN disk usage high
ERROR timeout at api
INFO retry success
EOF

cat > logs/worker.log <<'EOF'
INFO worker boot
ERROR worker retry
INFO worker done
EOF

cat > log_clean_demo.sh <<'EOF'
#!/bin/bash
set -e

echo "error-files:"
find logs -name "*.log" -print0 | xargs -0 grep -l "ERROR" | sort

echo "levels:"
find logs -name "*.log" -print0 | xargs -0 awk '{print $1}' | sort | uniq -c

echo "cleaned:"
sed 's/INFO/LOG/g; s/WARN/ALERT/g' logs/app.log > reports/app.clean.log
cat reports/app.clean.log
EOF

chmod +x log_clean_demo.sh
./log_clean_demo.sh

cat > next_steps.txt <<'EOF'
Week 1 自动练习已生成 log_clean_demo.sh、logs/ 和 reports/。

自测请在 Web UI 点 r06-w1-self 的“终端练习”，进入 ~/cli-lab/round6 后自己完成：
1. 新建 week1_self 目录。
2. 写一个 find_text_report.sh。
3. 使用 find -print0 | xargs -0 grep / wc 批量处理 .log 文件。
4. 能解释 find、xargs、sed、awk 分工后，点击“记录并完成”。
EOF

mark r06-w1-ex1

echo "Week 1 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r06-w1-self。"

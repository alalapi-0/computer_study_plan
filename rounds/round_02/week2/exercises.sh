#!/bin/bash
# =============================================================
# Round 02 · Week 2 练习脚本
# 主题：最小 shell 脚本与参数
# 用法：bash rounds/round_02/week2/exercises.sh
#
# 本脚本对应 progress.json 中的任务：
#   r02-w2-read  → 阅读 week2/notes.md（手动打卡）
#   r02-w2-ex4   → 练习4：count_errors.sh
#   r02-w2-ex5   → 练习5：count_labels.sh
#   r02-w2-ex6   → 练习6：show_args.sh
#   r02-w2-self  → 第2周自测
# =============================================================

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round2/week2
cd ~/cli-lab/round2/week2

echo "========================================"
echo "练习 4：count_errors.sh"
echo "========================================"
cat > app.log <<'EOF'
error: login failed
info: job started
error: file missing
info: job finished
EOF
cat > count_errors.sh <<'EOF'
#!/bin/bash
grep "error" app.log | wc -l > error_count.txt
cat error_count.txt
EOF
bash count_errors.sh
mark r02-w2-ex4

echo "========================================"
echo "练习 5：count_labels.sh"
echo "========================================"
cat > labels.txt <<'EOF'
ok
blur
ok
bad
blur
ok
EOF
cat > count_labels.sh <<'EOF'
#!/bin/bash
sort labels.txt | uniq > unique_labels.txt
cat unique_labels.txt
EOF
bash count_labels.sh
mark r02-w2-ex5

echo "========================================"
echo "练习 6：show_args.sh"
echo "========================================"
cat > show_args.sh <<'EOF'
#!/bin/bash
echo "script name: $0"
echo "first arg: $1"
echo "second arg: $2"
echo "all args: $@"
echo "arg count: $#"
EOF
bash show_args.sh aaa bbb ccc
mark r02-w2-ex6

echo "========================================"
echo "第 2 周自测"
echo "========================================"
echo "请独立运行：bash show_args.sh one two"
echo "完成后按回车继续..."
read
mark r02-w2-self

echo "🎉 Round 02 Week 2 完成。阅读任务请手动打卡：bash mark_done.sh r02-w2-read"

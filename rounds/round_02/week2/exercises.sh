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

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

LAB="$HOME/cli-lab/round2/week2/script_lab"
mkdir -p "$LAB"
cd "$LAB"

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

cat > check_file.sh <<'EOF'
#!/bin/bash
if grep "error" app.log > /dev/null 2> /dev/null
then
  echo "has error"
else
  echo "no error"
fi
EOF
bash check_file.sh

cat > next_steps.txt <<'EOF'
Week 2 下一步：
- 在 Web UI 练习终端中进入 ~/cli-lab/round2/week2/self_check。
- 用 printf 写一个 show_args_self.sh。
- 运行 bash show_args_self.sh one two。
- 确认能解释 $1、$@、$# 后，再手动标记 r02-w2-self。
EOF

echo "脚本已完成 r02-w2-ex4 / r02-w2-ex5 / r02-w2-ex6。"
echo "阅读任务与自测任务请在 Web UI 中确认后手动完成。"

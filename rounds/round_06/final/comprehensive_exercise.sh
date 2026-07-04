#!/bin/bash
# Round 06 · Final 综合练习（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round6/final_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB/input" "$LAB/output"
cd "$LAB"

cat > input/raw.log <<'EOF'
INFO user_login ok
WARN disk_80_percent
ERROR api_timeout
INFO retry_success
EOF

cat > batch_process.sh <<'EOF'
#!/bin/bash
set -e
INPUT_FILE="input/raw.log"
OUTPUT_FILE="output/clean.log"

grep -v "^INFO" "$INPUT_FILE" | sed 's/_/ /g' > "$OUTPUT_FILE"
awk '{print NR ":", $0}' "$OUTPUT_FILE"
EOF

chmod +x batch_process.sh
./batch_process.sh

cat > final_notes.md <<'EOF'
# Round 06 Final 自动练习产物

- batch_process.sh：批量处理 input/raw.log，过滤 INFO，替换下划线，并写入 output/clean.log。
- output/clean.log：清洗后的结果。
- 这只是自动综合练习。
- 小抄 r06-fin-sheet 与验收 r06-fin-acc1 仍需用户自己阅读、解释并在 Web UI 手动记录。
EOF

mark r06-fin-comp

echo "Round 06 Final 自动练习完成。请继续手动完成 r06-fin-sheet 与 r06-fin-acc1。"

#!/bin/bash
# Round 06 · Final 综合练习

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

mkdir -p ~/cli-lab/round6/final/input ~/cli-lab/round6/final/output
cd ~/cli-lab/round6/final

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

mark r06-fin-comp

echo "请确认你能解释该脚本里的 grep/sed/awk 流程后按回车..."
read
mark r06-fin-sheet
mark r06-fin-acc1

echo "Final 完成。"

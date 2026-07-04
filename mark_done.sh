#!/bin/bash
# =============================================================
# mark_done.sh — 标记任务完成，同时写入 progress.json 和 progress_data.js
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -f "$SCRIPT_DIR/progress.json" ]; then
  echo "❌ 找不到 progress.json。请在仓库根目录执行（见 docs/WORKSPACE.md）："
  echo "   cd ~/PycharmProjects/computer_study_plan"
  exit 1
fi

python3 "$SCRIPT_DIR/scripts/mark_done_cli.py" "$@"

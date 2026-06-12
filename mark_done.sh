#!/bin/bash
# =============================================================
# mark_done.sh — 标记任务完成（写入 progress.json / progress_data.js）
#
# 用法：
#   bash mark_done.sh <task-id>           标记完成
#   bash mark_done.sh <task-id> --undo    取消完成
#   bash mark_done.sh                     查看所有任务状态（按 lane 分组）
#
# 写入逻辑与 learn_server API 共用 scripts/progress_store.py
# =============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROGRESS_FILE="$SCRIPT_DIR/progress.json"

if [ ! -f "$PROGRESS_FILE" ]; then
  echo "❌ 找不到 progress.json。请在仓库根目录执行（见 docs/WORKSPACE.md）："
  echo "   cd ~/PycharmProjects/computer_study_plan"
  exit 1
fi

TASK_ID="$1"
MODE="${2:-}"

if [ -z "$TASK_ID" ]; then
  echo "用法：bash mark_done.sh <task-id> [--undo]"
  echo ""
  python3 "$SCRIPT_DIR/scripts/progress_store.py" list
  exit 0
fi

if [ "$MODE" = "--undo" ]; then
  python3 "$SCRIPT_DIR/scripts/progress_store.py" undo "$TASK_ID"
else
  python3 "$SCRIPT_DIR/scripts/progress_store.py" mark "$TASK_ID"
fi

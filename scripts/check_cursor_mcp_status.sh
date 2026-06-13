#!/usr/bin/env bash
# Cursor MCP CLI status check — does NOT prove current Agent thread tool exposure.
# Never prints API keys or tokens.

set -u

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MCP_JSON="${REPO_ROOT}/.cursor/mcp.json"

echo "Cursor MCP Status Check (CLI layer)"
echo "===================================="
echo "Repo root: ${REPO_ROOT}"
echo ""
echo "NOTE: This script checks CLI / config layer only."
echo "      It does NOT guarantee tools are exposed in the current Agent thread."
echo "      See docs/cursor_tool_registry_check.md"
echo ""

if [[ ! -f "${MCP_JSON}" ]]; then
  echo "WARN: .cursor/mcp.json not found"
else
  echo "OK: .cursor/mcp.json exists"
fi
echo ""

if ! command -v cursor-agent >/dev/null 2>&1; then
  echo "SKIP: cursor-agent not found in PATH"
  echo "      Install Cursor CLI or run checks from Cursor integrated terminal."
  echo "      Static config check: npm run check:mcp"
  exit 0
fi

echo "cursor-agent: $(command -v cursor-agent)"
echo ""

echo "--- cursor-agent mcp list ---"
if ! cursor-agent mcp list 2>&1 | sed -E 's/(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{20,})/[REDACTED]/g'; then
  echo "WARN: cursor-agent mcp list failed (server may need approval in Settings)"
fi
echo ""

SERVERS=(
  chrome-devtools
  playwright
  filesystem
  context7
  github
)

for server in "${SERVERS[@]}"; do
  echo "--- cursor-agent mcp list-tools ${server} ---"
  if cursor-agent mcp list-tools "${server}" 2>&1 | sed -E 's/(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{20,})/[REDACTED]/g'; then
    :
  else
    echo "WARN: list-tools failed for ${server} (not loaded / needs approval / name mismatch)"
  fi
  echo ""
done

echo "Done."
echo "If any server shows not loaded or needs approval:"
echo "  1. Cursor Settings → Tools & MCP → approve server"
echo "  2. Fully quit Cursor and reopen this repo"
echo "  3. Start a new ordinary foreground Agent conversation (no Multitask)"

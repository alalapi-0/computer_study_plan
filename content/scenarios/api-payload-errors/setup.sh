#!/bin/bash
set -euo pipefail
mkdir -p /workspace/app
cat > /workspace/app/api_program.py <<'PY'
import json
import sys

try:
    payload = json.loads(sys.stdin.read())
except ValueError:
    print(json.dumps({"status": 400, "error": "invalid JSON"}))
    raise SystemExit(0)
if set(payload) != {"name"} or not isinstance(payload["name"], str) or not payload["name"].strip():
    print(json.dumps({"status": 422, "error": "name is required"}))
else:
    print(json.dumps({"status": 201, "data": {"name": payload["name"].strip()}}))
PY
cat > /workspace/app/client.py <<'PY'
import json
import subprocess
import sys

name = sys.argv[1] if len(sys.argv) > 1 else ""
request = {"username": name}
run = subprocess.run([sys.executable, "/workspace/app/api_program.py"], input=json.dumps(request), text=True, capture_output=True)
response = json.loads(run.stdout)
print(f"saved:{name}")
PY

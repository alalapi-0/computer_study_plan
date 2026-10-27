#!/bin/bash
set -euo pipefail
mkdir -p /workspace/app /workspace/data
printf '{"id":"job-a","value":4}\n{"id":"job-b","value":7}\n' > /workspace/data/requests.jsonl
cat > /workspace/app/worker.py <<'PY'
import json
from pathlib import Path

requests_path = Path("/workspace/data/requests.jsonl")
results_path = Path("/workspace/data/results.json")
results = json.loads(results_path.read_text()) if results_path.exists() else []
for line in requests_path.read_text().splitlines():
    request = json.loads(line)
    results.append({"request_id": request["id"], "result": request["value"] * 2})
results_path.write_text(json.dumps(results, sort_keys=True) + "\n")
print(f"results={len(results)}")
PY
python3 /workspace/app/worker.py >/dev/null
python3 /workspace/app/worker.py >/dev/null

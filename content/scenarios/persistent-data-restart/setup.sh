#!/bin/bash
set -euo pipefail
mkdir -p /workspace/app /workspace/data /workspace/run
printf '{"state_path":"/workspace/run/state.json"}\n' > /workspace/app/config.json
cat > /workspace/app/service.py <<'PY'
import json
import shutil
import sys
from pathlib import Path

config = json.loads(Path("/workspace/app/config.json").read_text())
state_path = Path(config["state_path"])

def load():
    if not state_path.exists():
        return {}
    return json.loads(state_path.read_text())

command = sys.argv[1]
if command == "set":
    state = load()
    state[sys.argv[2]] = sys.argv[3]
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, sort_keys=True) + "\n")
    print("stored")
elif command == "get":
    print(load().get(sys.argv[2], "MISSING"))
elif command == "restart":
    shutil.rmtree("/workspace/run", ignore_errors=True)
    Path("/workspace/run").mkdir()
    print("restarted")
else:
    raise SystemExit("unknown command")
PY
python3 /workspace/app/service.py set theme dark >/dev/null
python3 /workspace/app/service.py restart >/dev/null

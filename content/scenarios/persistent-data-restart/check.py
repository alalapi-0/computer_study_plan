import json
import stat
import subprocess
import sys
from pathlib import Path


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def regular(path, limit):
    try:
        st = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_size <= limit


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
config = Path("/workspace/app/config.json")
if mode == "ready":
    ready = Path("/usr/bin/python3").exists() and config.is_file() and Path("/workspace/app/service.py").is_file()
    emit(ready=ready, passed=False, evidence=["Python and restart simulator available"] if ready else ["platform or setup output missing"])
    raise SystemExit(0)
if not regular(config, 4096):
    emit(ready=True, passed=False, evidence=["config.json must be a bounded regular file"])
    raise SystemExit(0)
try:
    parsed = json.loads(config.read_text())
except (OSError, ValueError):
    emit(ready=True, passed=False, evidence=["config.json is not valid JSON"])
    raise SystemExit(0)
if parsed != {"state_path": "/workspace/data/state.json"}:
    emit(ready=True, passed=False, evidence=["state path is not the scenario persistent-data path"])
    raise SystemExit(0)
commands = [
    ["set", "checker", "survives"],
    ["restart"],
    ["get", "checker"],
    ["get", "theme"],
]
outputs = []
try:
    for args in commands:
        run = subprocess.run(["/usr/bin/python3", "/workspace/app/service.py", *args], text=True, capture_output=True, timeout=3)
        outputs.append((run.returncode, run.stdout.strip()))
except (OSError, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"restart verification failed safely: {type(exc).__name__}"])
    raise SystemExit(0)
state = Path("/workspace/data/state.json")
passed = outputs == [(0, "stored"), (0, "restarted"), (0, "survives"), (0, "dark")] and regular(state, 8192)
emit(ready=True, passed=passed, evidence=[f"command results={outputs!r}", "state survived simulated restart" if passed else "state did not satisfy restart contract"])

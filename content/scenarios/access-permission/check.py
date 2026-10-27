import json
import os
import stat
import subprocess
import sys
from pathlib import Path

EXPECTED = b"mode=training\nport=4310\n"


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def bounded_regular(path, limit):
    try:
        st = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_size <= limit


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
target = Path("/workspace/config/app.conf")
if mode == "ready":
    ready = Path("/usr/bin/python3").exists() and target.exists()
    emit(ready=ready, passed=False, evidence=["unprivileged userland and setup output available"] if ready else ["platform or setup missing"])
    raise SystemExit(0)
if not bounded_regular(target, 1024):
    emit(ready=True, passed=False, evidence=["protected configuration content is missing, linked, oversized, or changed"])
    raise SystemExit(0)
actual_mode = stat.S_IMODE(target.stat().st_mode)
content = target.read_bytes()
if content != EXPECTED:
    emit(ready=True, passed=False, evidence=["protected configuration content changed"])
    raise SystemExit(0)
try:
    run = subprocess.run(["/usr/bin/python3", "/workspace/bin/read_config.py"], text=True, capture_output=True, timeout=3)
except (OSError, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"reader execution failed safely: {type(exc).__name__}"])
    raise SystemExit(0)
passed = actual_mode == 0o600 and run.returncode == 0 and run.stdout == "mode=training port=4310\n"
emit(ready=True, passed=passed, evidence=[f"mode={actual_mode:04o}", f"read/write open exit={run.returncode}", "protected content preserved"])

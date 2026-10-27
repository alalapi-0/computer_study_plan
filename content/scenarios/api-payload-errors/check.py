import json
import stat
import subprocess
import sys
from pathlib import Path

EXPECTED_API = b'''import json\nimport sys\n\ntry:\n    payload = json.loads(sys.stdin.read())\nexcept ValueError:\n    print(json.dumps({"status": 400, "error": "invalid JSON"}))\n    raise SystemExit(0)\nif set(payload) != {"name"} or not isinstance(payload["name"], str) or not payload["name"].strip():\n    print(json.dumps({"status": 422, "error": "name is required"}))\nelse:\n    print(json.dumps({"status": 201, "data": {"name": payload["name"].strip()}}))\n'''


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def regular(path, limit):
    try:
        st = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_size <= limit


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
api = Path("/workspace/app/api_program.py")
client = Path("/workspace/app/client.py")
if mode == "ready":
    ready = Path("/usr/bin/python3").exists() and api.is_file() and client.is_file()
    emit(ready=ready, passed=False, evidence=["local offline API contract program available"] if ready else ["platform or setup output missing"])
    raise SystemExit(0)
if not regular(api, 16_384) or api.read_bytes() != EXPECTED_API:
    emit(ready=True, passed=False, evidence=["protected local API program is missing, linked, oversized, or changed"])
    raise SystemExit(0)
if not regular(client, 24_000):
    emit(ready=True, passed=False, evidence=["client.py must be a bounded regular file"])
    raise SystemExit(0)
try:
    valid = subprocess.run(["/usr/bin/python3", str(client), "Ada"], text=True, capture_output=True, timeout=3)
    varied = subprocess.run(["/usr/bin/python3", str(client), "  Lin  "], text=True, capture_output=True, timeout=3)
    invalid = subprocess.run(["/usr/bin/python3", str(client), ""], text=True, capture_output=True, timeout=3)
except (OSError, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"client contract verification failed safely: {type(exc).__name__}"])
    raise SystemExit(0)
passed = valid.returncode == 0 and valid.stdout == "saved:Ada\n" and varied.returncode == 0 and varied.stdout == "saved:Lin\n" and invalid.returncode != 0 and invalid.stdout == "error: name is required\n"
emit(ready=True, passed=passed, evidence=[f"Ada exit/output={valid.returncode}/{valid.stdout.strip()!r}", f"varied trimmed-name exit/output={varied.returncode}/{varied.stdout.strip()!r}", f"invalid exit/output={invalid.returncode}/{invalid.stdout.strip()!r}", "contract is a local CLI subset, not a browser API"])

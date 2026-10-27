import json
import stat
import subprocess
import sys
from pathlib import Path

EXPECTED_REQUESTS = b'{"id":"job-a","value":4}\n{"id":"job-b","value":7}\n'


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def regular(path, limit):
    try:
        st = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_size <= limit


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
requests = Path("/workspace/data/requests.jsonl")
worker = Path("/workspace/app/worker.py")
if mode == "ready":
    ready = Path("/usr/bin/python3").exists() and requests.is_file() and worker.is_file()
    emit(ready=ready, passed=False, evidence=["Python and retry fixture available"] if ready else ["platform or setup output missing"])
    raise SystemExit(0)
if not regular(requests, 4096) or requests.read_bytes() != EXPECTED_REQUESTS:
    emit(ready=True, passed=False, evidence=["protected request stream is missing, linked, oversized, or changed"])
    raise SystemExit(0)
if not regular(worker, 24_000):
    emit(ready=True, passed=False, evidence=["worker.py must be a bounded regular file"])
    raise SystemExit(0)
results = Path("/workspace/data/results.json")
try:
    first = subprocess.run(["/usr/bin/python3", str(worker)], text=True, capture_output=True, timeout=3)
    second = subprocess.run(["/usr/bin/python3", str(worker)], text=True, capture_output=True, timeout=3)
    records = json.loads(results.read_text()) if regular(results, 16_384) else None
except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"retry verification failed safely: {type(exc).__name__}"])
    raise SystemExit(0)
expected = [{"request_id": "job-a", "result": 8}, {"request_id": "job-b", "result": 14}]
passed = first.returncode == second.returncode == 0 and records == expected
emit(ready=True, passed=passed, evidence=[f"first retry output={first.stdout.strip()!r}", f"second retry output={second.stdout.strip()!r}", f"records={records!r}"])

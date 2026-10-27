import json
import os
import subprocess
import sys
from pathlib import Path

EXPECTED_INPUT = b"alpha\nbeta\ngamma\n"


def regular_bounded(path: Path, limit: int) -> bool:
    try:
        st = path.lstat()
    except OSError:
        return False
    return not path.is_symlink() and path.is_file() and st.st_size <= limit


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
required = [Path("/usr/bin/python3"), Path("/bin/bash")]
workspace = Path("/workspace")
if mode == "ready":
    ready = all(p.exists() for p in required) and (workspace / "app/report.py").is_file()
    emit(ready=ready, passed=False, evidence=["platform tools and scenario files present"] if ready else ["missing platform tool or setup output"])
    raise SystemExit(0)

evidence = []
input_path = workspace / "data/input.txt"
if not regular_bounded(input_path, 1024) or input_path.read_bytes() != EXPECTED_INPUT:
    emit(ready=True, passed=False, evidence=["protected input.txt is missing, linked, oversized, or changed"])
    raise SystemExit(0)
report = workspace / "app/report.py"
if not regular_bounded(report, 16_384):
    emit(ready=True, passed=False, evidence=["report.py must be a bounded regular file"])
    raise SystemExit(0)
result = workspace / "result.txt"
if not regular_bounded(result, 128) or result.read_text() != "records=3\n":
    emit(ready=True, passed=False, evidence=["the learner-produced result.txt is missing, linked, oversized, or incorrect"])
    raise SystemExit(0)
input_path.write_text("delta\nepsilon\n", encoding="utf-8")
result.unlink()
try:
    run = subprocess.run(["/bin/bash", "/workspace/app/run.sh"], cwd="/tmp", text=True, capture_output=True, timeout=4)
except (OSError, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"report execution failed safely: {type(exc).__name__}"])
    raise SystemExit(0)
passed = run.returncode == 0 and run.stdout == "records=2\n" and regular_bounded(result, 128) and result.read_text() == "records=2\n"
evidence.append(f"independent two-record run from /tmp exit={run.returncode}, stdout={run.stdout.strip()!r}")
evidence.append("protected original and learner-produced three-record artifact verified before variation")
emit(ready=True, passed=passed, evidence=evidence)

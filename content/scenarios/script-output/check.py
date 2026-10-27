import json
import stat
import subprocess
import sys
from pathlib import Path

EXPECTED_INPUT = b"north,12\nsouth,8\nwest,15\n"
EXPECTED_REPORT = "rows\ttotal\n3\t35\n"


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def bounded_regular(path, limit):
    try:
        st = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_size <= limit


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
if mode == "ready":
    ready = all(Path(p).exists() for p in ("/bin/bash", "/usr/bin/wc")) and Path("/workspace/bin/generate_report.sh").exists()
    emit(ready=ready, passed=False, evidence=["shell tools and setup output available"] if ready else ["required platform tool or setup output missing"])
    raise SystemExit(0)
source = Path("/workspace/data/sales.csv")
script = Path("/workspace/bin/generate_report.sh")
if not bounded_regular(source, 2048) or source.read_bytes() != EXPECTED_INPUT:
    emit(ready=True, passed=False, evidence=["protected sales.csv is missing, linked, oversized, or changed"])
    raise SystemExit(0)
if not bounded_regular(script, 16_384):
    emit(ready=True, passed=False, evidence=["generator must be a bounded regular file"])
    raise SystemExit(0)
report = Path("/workspace/report.tsv")
if not bounded_regular(report, 1024) or report.read_text() != EXPECTED_REPORT:
    emit(ready=True, passed=False, evidence=["the learner-produced report.tsv is missing, linked, oversized, or incorrect"])
    raise SystemExit(0)
source.write_text("east,2\ncentral,9\n", encoding="utf-8")
report.unlink()
try:
    run = subprocess.run(["/bin/bash", str(script)], text=True, capture_output=True, timeout=3)
except (OSError, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"generator execution failed safely: {type(exc).__name__}"])
    raise SystemExit(0)
varied = "rows\ttotal\n2\t11\n"
passed = run.returncode == 0 and run.stdout == varied and bounded_regular(report, 1024) and report.read_text() == varied
emit(ready=True, passed=passed, evidence=[f"independent varied-input exit={run.returncode}", f"varied report={run.stdout.strip()!r}", "protected original and learner-produced report verified before variation"])

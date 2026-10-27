#!/bin/bash
set -euo pipefail
mkdir -p /workspace/app /workspace/data
printf 'alpha\nbeta\ngamma\n' > /workspace/data/input.txt
cat > /workspace/app/report.py <<'PY'
from pathlib import Path

source = Path("data/input.txt")
lines = source.read_text(encoding="utf-8").splitlines()
Path("/workspace/result.txt").write_text(f"records={len(lines)}\n", encoding="utf-8")
print(f"records={len(lines)}")
PY
cat > /workspace/app/run.sh <<'SH'
#!/bin/bash
set -euo pipefail
cd /workspace/app
python3 report.py
SH
chmod +x /workspace/app/run.sh

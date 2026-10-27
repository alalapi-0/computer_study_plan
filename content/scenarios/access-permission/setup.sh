#!/bin/bash
set -euo pipefail
mkdir -p /workspace/config /workspace/bin
printf 'mode=training\nport=4310\n' > /workspace/config/app.conf
chmod 400 /workspace/config/app.conf
cat > /workspace/bin/read_config.py <<'PY'
from pathlib import Path

path = Path("/workspace/config/app.conf")
with path.open("r+") as stream:
    values = dict(line.split("=", 1) for line in stream.read().splitlines())
print(f"mode={values['mode']} port={values['port']}")
PY

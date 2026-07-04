#!/usr/bin/env python3
"""Round 13 · Week 3: Dockerfile and release preflight rehearsal."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
LAB = Path.home() / "cli-lab" / "round13" / "week3_auto" / "docker_rehearsal"


DOCKERFILE = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p input output logs

EXPOSE 8000

CMD ["python", "ai_prep_tool.py", "--help"]
"""

RELEASE_CHECK = '''#!/usr/bin/env python3
"""Check the Round 13 Docker rehearsal files without running Docker."""

from pathlib import Path
import json

base = Path(__file__).resolve().parent
dockerfile = (base / "Dockerfile").read_text(encoding="utf-8")
dockerignore = (base / ".dockerignore").read_text(encoding="utf-8").splitlines()
required = {
    "FROM": "FROM python:" in dockerfile,
    "WORKDIR": "WORKDIR /app" in dockerfile,
    "COPY_REQUIREMENTS": "COPY requirements.txt ." in dockerfile,
    "PIP_INSTALL": "pip install" in dockerfile,
    "CMD": "CMD [" in dockerfile,
    "IGNORE_VENV": any(".venv" in line or "venv" in line for line in dockerignore),
    "IGNORE_GIT": ".git/" in dockerignore,
    "IGNORE_CACHE": "__pycache__/" in dockerignore,
}
report = {"ok": all(required.values()), "required": required}
(base / "release_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False, sort_keys=True))
raise SystemExit(0 if report["ok"] else 1)
'''


def mark(task_id: str) -> None:
    subprocess.run(["bash", str(REPO_ROOT / "mark_done.sh"), task_id], cwd=REPO_ROOT, check=True)


def reset_lab() -> None:
    if LAB.exists():
        shutil.rmtree(LAB)
    LAB.mkdir(parents=True)


def write_project() -> dict:
    (LAB / "Dockerfile").write_text(DOCKERFILE, encoding="utf-8")
    (LAB / ".dockerignore").write_text(
        ".venv*/\nvenv/\n__pycache__/\n*.pyc\n*.db\nlogs/\noutput/\n.git/\n.DS_Store\n",
        encoding="utf-8",
    )
    (LAB / "requirements.txt").write_text("# offline-safe rehearsal, no third-party packages\n", encoding="utf-8")
    (LAB / "ai_prep_tool.py").write_text(
        "import argparse\n\n"
        "parser = argparse.ArgumentParser(description='Round 13 Docker rehearsal')\n"
        "parser.add_argument('--help-only', action='store_true')\n"
        "args = parser.parse_args()\n"
        "print('ai_prep_tool ready')\n",
        encoding="utf-8",
    )
    check = LAB / "release_check.py"
    check.write_text(RELEASE_CHECK, encoding="utf-8")
    check.chmod(0o755)
    proc = subprocess.run([sys.executable, str(check)], cwd=LAB, capture_output=True, text=True, check=False)
    report = json.loads((LAB / "release_report.json").read_text(encoding="utf-8"))
    report.update({"check_returncode": proc.returncode, "stdout": proc.stdout.strip(), "sandbox": str(LAB)})
    (LAB / "next_steps.txt").write_text(
        "在浏览器终端自己写一个最小 Dockerfile，并手动记录 r13-w3-self；不要执行 docker build。\n",
        encoding="utf-8",
    )
    return report


def main() -> None:
    reset_lab()
    report = write_project()
    if report["check_returncode"] != 0 or not report["ok"]:
        raise RuntimeError(f"Week 3 release preflight failed: {report}")
    print("Round 13 Week 3 Dockerfile 与发布检查")
    print("sandbox:", LAB)
    print("dockerfile:", LAB / "Dockerfile")
    print("dockerignore:", LAB / ".dockerignore")
    print("report:", LAB / "release_report.json")
    print("required_ok:", sorted(k for k, v in report["required"].items() if v))
    mark("r13-w3-ex3")


if __name__ == "__main__":
    main()

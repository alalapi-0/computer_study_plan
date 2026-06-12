#!/usr/bin/env python3
"""Parse and run round exercise scripts for learn_server (PW-3)."""

from __future__ import annotations

import re
import subprocess
import time
from pathlib import Path

EXERCISE_REL_RE = re.compile(
    r"^rounds/round_\d{2}/(week[123]|final)/(exercises\.(sh|py)|comprehensive_exercise\.(sh|py))$"
)

PRACTICE_HEADER_RE = re.compile(r"练习\s*\d+")
MARK_RE = re.compile(r"mark\s+['\"]?([a-zA-Z0-9_-]+)")
ECHO_HINT_RE = re.compile(r"echo\s+\"(.+)\"")
SANDBOX_RE = re.compile(r"~/cli-lab/round(\d+)")


def resolve_exercise_path(repo_root: Path, rel_path: str) -> Path | None:
    rel = rel_path.strip().replace("\\", "/").lstrip("/")
    if not EXERCISE_REL_RE.match(rel):
        return None
    if ".." in rel.split("/"):
        return None
    full = (repo_root / rel).resolve()
    try:
        full.relative_to(repo_root.resolve())
    except ValueError:
        return None
    if not full.is_file():
        return None
    return full


def infer_sandbox(text: str, round_id: str) -> str:
    match = SANDBOX_RE.search(text)
    if match:
        return f"~/cli-lab/round{match.group(1)}"
    num = round_id.replace("round_", "")
    return f"~/cli-lab/round{num}"


def is_section_header(comment: str) -> bool:
    text = comment.strip().lstrip("#").strip()
    if "→" in text:
        return False
    if PRACTICE_HEADER_RE.match(text):
        return True
    if "自测" in text and (text.startswith("第") or "周" in text):
        return True
    return False


def parse_shell_sections(text: str) -> list[dict]:
    lines = text.splitlines()
    headers: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#") and is_section_header(stripped):
            headers.append((i, stripped.lstrip("#").strip()))

    sections: list[dict] = []
    for idx, (start_i, header) in enumerate(headers):
        end_i = headers[idx + 1][0] if idx + 1 < len(headers) else len(lines)
        section: dict = {
            "title": header,
            "hints": [],
            "commands": [],
            "task_id": None,
        }
        for line in lines[start_i:end_i]:
            stripped = line.strip()
            if stripped.startswith("mark "):
                m = MARK_RE.search(stripped)
                if m:
                    section["task_id"] = m.group(1)
            if stripped.startswith("echo "):
                em = ECHO_HINT_RE.search(stripped)
                if em:
                    hint = em.group(1)
                    if hint and not hint.startswith("="):
                        section["hints"].append(hint)
            if not stripped.startswith("#") and stripped:
                if stripped in ("mark()", "}") or stripped.startswith("mark "):
                    continue
                if any(
                    stripped.startswith(p)
                    for p in ("cd ", "mkdir ", "pwd", "ls", "bash ", "python3 ")
                ):
                    section["commands"].append(stripped)
        sections.append(section)
    return sections


def build_guide(repo_root: Path, rel_path: str) -> dict:
    full = resolve_exercise_path(repo_root, rel_path)
    if not full:
        raise ValueError("invalid exercise path")

    text = full.read_text(encoding="utf-8")
    round_m = re.search(r"round_(\d{2})", rel_path)
    round_id = f"round_{round_m.group(1)}" if round_m else "round_00"
    sandbox = infer_sandbox(text, round_id)
    suffix = full.suffix.lower()
    interactive = "read" in text if suffix == ".sh" else False

    if suffix == ".sh":
        steps = parse_shell_sections(text)
        kind = "shell"
        can_run = not interactive
    else:
        steps = [
            {
                "title": "运行 Python 练习脚本",
                "hints": ["点击「运行脚本」在沙盒目录执行 exercises.py"],
                "commands": [f"python3 {rel_path}"],
                "task_id": None,
            }
        ]
        kind = "python"
        can_run = True

    task_ids = [s["task_id"] for s in steps if s.get("task_id")]

    return {
        "ok": True,
        "path": rel_path,
        "round_id": round_id,
        "kind": kind,
        "sandbox": sandbox,
        "can_run": can_run,
        "interactive_shell": interactive,
        "steps": steps,
        "task_ids": task_ids,
    }


def run_exercise(repo_root: Path, rel_path: str, timeout: int = 120) -> dict:
    full = resolve_exercise_path(repo_root, rel_path)
    if not full:
        raise ValueError("invalid exercise path")

    text = full.read_text(encoding="utf-8")
    suffix = full.suffix.lower()

    if suffix == ".sh":
        if "read" in text:
            raise ValueError("interactive shell exercise cannot run via API; use step guide")
        cmd = ["bash", str(full)]
    elif suffix == ".py":
        cmd = ["python3", str(full)]
    else:
        raise ValueError("unsupported exercise type")

    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        elapsed = round(time.time() - start, 2)
        return {
            "ok": proc.returncode == 0,
            "exit_code": proc.returncode,
            "stdout": proc.stdout or "",
            "stderr": proc.stderr or "",
            "elapsed_sec": elapsed,
            "path": rel_path,
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "ok": False,
            "exit_code": -1,
            "stdout": (exc.stdout or "") if exc.stdout else "",
            "stderr": (exc.stderr or "") if exc.stderr else "",
            "elapsed_sec": timeout,
            "path": rel_path,
            "error": "timeout",
        }

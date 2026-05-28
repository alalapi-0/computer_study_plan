#!/usr/bin/env python3
"""Minimal protocol sync checker for computer_study_plan."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = [
    "governance/repo_protocol_standard.yaml",
    "project.yaml",
    "governance/round_state.yaml",
    "governance/agent_policy.yaml",
    "governance/file_role_map.yaml",
    "governance/model_policy.yaml",
    "governance/data_policy.yaml",
    "docs/PROJECT_STATE.md",
    "docs/NEXT_ACTIONS.md",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_version(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.MULTILINE)
    return match.group(1) if match else None


def main() -> int:
    errors: list[str] = []

    for rel in REQUIRED_PATHS:
        abs_path = REPO_ROOT / rel
        if not abs_path.exists():
            errors.append(f"missing_required_path: {rel}")

    protocol_path = REPO_ROOT / "governance/repo_protocol_standard.yaml"
    project_path = REPO_ROOT / "project.yaml"
    agents_path = REPO_ROOT / "AGENTS.md"

    if protocol_path.exists() and project_path.exists():
        protocol_text = read_text(protocol_path)
        project_text = read_text(project_path)
        protocol_version = extract_version(r'^\s*version:\s*"([^"]+)"\s*$', protocol_text)
        project_version = extract_version(
            r'^\s*version:\s*"([^"]+)"\s*$', project_text
        )
        if not protocol_version:
            errors.append("protocol_version_not_found: governance/repo_protocol_standard.yaml")
        if not project_version:
            errors.append("project_protocol_version_not_found: project.yaml")
        if protocol_version and project_version and protocol_version != project_version:
            errors.append(
                "protocol_version_mismatch: "
                f"repo_protocol_standard={protocol_version}, project_yaml={project_version}"
            )

    if agents_path.exists():
        agents_text = read_text(agents_path)
        if "governance/repo_protocol_standard.yaml" not in agents_text:
            errors.append("agents_missing_protocol_reference: AGENTS.md")

    if errors:
        print("Protocol sync check FAILED")
        for item in errors:
            print(f"- {item}")
        return 1

    print("Protocol sync check PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())

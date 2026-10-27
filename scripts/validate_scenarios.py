#!/usr/bin/env python3
"""Validate trusted, repository-local problem scenario packages.

Static validation never runs package code. ``--runtime`` is the publication
gate for this reviewed local catalog and executes it only through LabManager's
Bubblewrap boundary; this is not an arbitrary upload/import facility.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
import uuid
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "content" / "scenarios"
EXPECTED_IDS = {
    "access-permission",
    "api-payload-errors",
    "git-preserve-work",
    "media-wav-quality",
    "path-cwd-input",
    "persistent-data-restart",
    "retry-no-duplicates",
    "script-output",
}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
DESCRIPTOR_KEYS = {
    "id", "version", "title", "summary", "tags", "symptom", "goal",
    "constraints", "environment", "provenance", "hints", "solution",
}
STEP_KEYS = {"node", "shell", "command", "expected", "explanation", "recovery"}
PACKAGE_FILES = {"scenario.json", "setup.sh", "check.py"}
FILE_LIMITS = {"scenario.json": 128_000, "setup.sh": 64_000, "check.py": 64_000}
NEGATIVE_TAMPERS = {
    "path-cwd-input": "printf 'tampered\\n' > /workspace/data/input.txt",
    "access-permission": "chmod 600 /workspace/config/app.conf; printf 'tampered\\n' > /workspace/config/app.conf",
    "script-output": "printf 'tampered,999\\n' > /workspace/data/sales.csv",
    "git-preserve-work": "printf 'lost-draft\\n' > /workspace/repo/settings.ini",
    "persistent-data-restart": "rm /workspace/app/config.json; ln -s /workspace/data/other.json /workspace/app/config.json",
    "retry-no-duplicates": "printf '{\"id\":\"other\",\"value\":1}\\n' > /workspace/data/requests.jsonl",
    "api-payload-errors": "printf 'print(\"fake\")\\n' > /workspace/app/api_program.py",
    "media-wav-quality": "printf '{}\\n' > /workspace/input/spec.json",
}
ALTERNATIVE_SOLUTIONS = {
    "git-preserve-work": "cd /workspace/repo && git branch safety-copy && git show HEAD^:app.py > app.py && python3 app.py",
}
FORGED_OUTPUTS = {
    "git-preserve-work": "cd /workspace/repo && cp app.py /tmp/good-app.py && git checkout --orphan replacement && git rm -rf . >/dev/null && cp /tmp/good-app.py app.py && printf 'color=blue\\n' > settings.ini && git add app.py settings.ini && git -c user.name='Replacement' -c user.email='replacement@example.invalid' commit -qm 'replacement first' && printf 'extra\\n' > extra.txt && git add extra.txt && git -c user.name='Replacement' -c user.email='replacement@example.invalid' commit -qm 'replacement second' && git branch -D main >/dev/null && git reflog expire --expire=now --all && git gc --prune=now && printf 'color=violet\\ndraft_note=keep-me\\n' > settings.ini && python3 app.py",
    "path-cwd-input": "python3 - <<'PY'\nfrom pathlib import Path\nPath('/workspace/app/report.py').write_text('from pathlib import Path\\nPath(\"/workspace/result.txt\").write_text(\"records=3\\\\n\")\\nprint(\"records=3\")\\n')\nPY\n/workspace/app/run.sh",
    "script-output": "python3 - <<'PY'\nfrom pathlib import Path\nPath('/workspace/bin/generate_report.sh').write_text('#!/bin/bash\\nprintf \\'rows\\\\ttotal\\\\n3\\\\t35\\\\n\\' | tee /workspace/report.tsv\\n')\nPY\nchmod +x /workspace/bin/generate_report.sh\n/workspace/bin/generate_report.sh",
    "api-payload-errors": "python3 - <<'PY'\nfrom pathlib import Path\nPath('/workspace/app/client.py').write_text('import sys\\nname=sys.argv[1] if len(sys.argv)>1 else \"\"\\nif name:\\n print(\"saved:Ada\")\\nelse:\\n print(\"error: name is required\")\\n raise SystemExit(2)\\n')\nPY",
    "media-wav-quality": "sed -i 's/FREQUENCY = 440/FREQUENCY = 660/' /workspace/app/generate_tone.py && python3 /workspace/app/generate_tone.py",
}


class ValidationError(ValueError):
    pass


def _nonempty_text(value: Any, label: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{label} must be non-empty text")


def _text_list(value: Any, label: str, *, minimum: int = 1) -> None:
    if not isinstance(value, list) or len(value) < minimum:
        raise ValidationError(f"{label} must be a list with at least {minimum} item(s)")
    for index, item in enumerate(value):
        _nonempty_text(item, f"{label}[{index}]")
    if len(set(value)) != len(value):
        raise ValidationError(f"{label} contains duplicates")


def _step(value: Any, label: str) -> None:
    if not isinstance(value, dict) or set(value) != STEP_KEYS:
        raise ValidationError(f"{label} must contain exactly {sorted(STEP_KEYS)}")
    for key in STEP_KEYS:
        _nonempty_text(value[key], f"{label}.{key}")
    if value["node"] != "lab" or value["shell"] != "bash":
        raise ValidationError(f"{label} targets an unsupported node or shell")
    if len(value["command"].encode("utf-8")) > 32_768:
        raise ValidationError(f"{label}.command is oversized")


def validate_catalog(catalog_root: Path = DEFAULT_CATALOG) -> list[dict[str, Any]]:
    root = Path(catalog_root).absolute()
    if not root.is_dir() or root.is_symlink() or root.resolve() != root:
        raise ValidationError("catalog root must be a real directory")
    descriptors = sorted(root.glob("*/scenario.json"))
    scenarios: list[dict[str, Any]] = []
    seen: set[str] = set()
    for descriptor in descriptors:
        package = descriptor.parent
        if package.is_symlink() or descriptor.is_symlink():
            raise ValidationError("scenario packages may not use symbolic links")
        children = {item.name for item in package.iterdir()}
        if children != PACKAGE_FILES:
            raise ValidationError(f"{package.name} must contain exactly {sorted(PACKAGE_FILES)}")
        for filename, limit in FILE_LIMITS.items():
            target = package / filename
            if target.is_symlink() or not target.is_file() or target.stat().st_size > limit:
                raise ValidationError(f"{package.name}/{filename} is missing, linked, or oversized")
        try:
            value = json.loads(descriptor.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            raise ValidationError(f"{package.name}/scenario.json is invalid: {exc}") from exc
        if not isinstance(value, dict) or set(value) != DESCRIPTOR_KEYS:
            raise ValidationError(f"{package.name} descriptor keys do not match the schema")
        scenario_id = value["id"]
        if not isinstance(scenario_id, str) or not ID_RE.fullmatch(scenario_id) or scenario_id != package.name:
            raise ValidationError(f"{package.name} has an invalid or mismatched id")
        if scenario_id in seen:
            raise ValidationError(f"duplicate scenario id: {scenario_id}")
        seen.add(scenario_id)
        if type(value["version"]) is not int or value["version"] < 1:
            raise ValidationError(f"{scenario_id}.version must be a positive integer")
        for key in ("title", "summary", "symptom", "goal"):
            _nonempty_text(value[key], f"{scenario_id}.{key}")
        _text_list(value["tags"], f"{scenario_id}.tags", minimum=2)
        _text_list(value["constraints"], f"{scenario_id}.constraints", minimum=2)
        environment = value["environment"]
        if not isinstance(environment, dict) or set(environment) != {"adapter", "nodes", "shell", "required_tools"}:
            raise ValidationError(f"{scenario_id}.environment has an invalid shape")
        if environment["adapter"] != "bwrap-userland" or environment["nodes"] != ["lab"] or environment["shell"] != "bash":
            raise ValidationError(f"{scenario_id}.environment requests an unsupported runtime")
        _text_list(environment["required_tools"], f"{scenario_id}.environment.required_tools")
        provenance = value["provenance"]
        if not isinstance(provenance, dict) or set(provenance) != {"type", "source_links", "adaptations"}:
            raise ValidationError(f"{scenario_id}.provenance has an invalid shape")
        if provenance["type"] != "teaching-adaptation":
            raise ValidationError(f"{scenario_id} must be labeled teaching-adaptation")
        _text_list(provenance["source_links"], f"{scenario_id}.provenance.source_links")
        if not all(link.startswith("https://") for link in provenance["source_links"]):
            raise ValidationError(f"{scenario_id} source links must use https")
        _text_list(provenance["adaptations"], f"{scenario_id}.provenance.adaptations")
        hints = value["hints"]
        if not isinstance(hints, list) or len(hints) < 2:
            raise ValidationError(f"{scenario_id}.hints must contain a complete sequence")
        for index, hint in enumerate(hints):
            _step(hint, f"{scenario_id}.hints[{index}]")
        solution = value["solution"]
        if not isinstance(solution, dict) or set(solution) != {"steps", "explanation"}:
            raise ValidationError(f"{scenario_id}.solution has an invalid shape")
        _nonempty_text(solution["explanation"], f"{scenario_id}.solution.explanation")
        if not isinstance(solution["steps"], list) or len(solution["steps"]) < 2:
            raise ValidationError(f"{scenario_id}.solution.steps must be complete")
        for index, step in enumerate(solution["steps"]):
            _step(step, f"{scenario_id}.solution.steps[{index}]")
        checker_source = (package / "check.py").read_text(encoding="utf-8")
        compile(checker_source, str(package / "check.py"), "exec")
        scenarios.append(value)
    if seen != EXPECTED_IDS:
        missing = sorted(EXPECTED_IDS - seen)
        extra = sorted(seen - EXPECTED_IDS)
        raise ValidationError(f"catalog coverage mismatch: missing={missing}, extra={extra}")
    return scenarios


def _latest_check(snapshot: dict[str, Any]) -> dict[str, Any]:
    checks = snapshot["attempt"]["checks"]
    if not checks:
        raise ValidationError("runtime did not record a checker result")
    return checks[-1]


def _send_command(manager: Any, attempt_id: str, command: str, label: str) -> str:
    result = manager.execute(attempt_id, command, f"execute:{label}:{uuid.uuid4().hex}")
    if type(result.get("exit_code")) is not int or not isinstance(result.get("stdout"), str) or not isinstance(result.get("stderr"), str):
        raise ValidationError(f"validation batch result is malformed: {label}")
    return result["stdout"] + result["stderr"]


def _expect_check(manager: Any, attempt_id: str, expected: bool, label: str) -> None:
    snapshot = manager.check(attempt_id, f"check:{label}:{uuid.uuid4().hex}")
    result = _latest_check(snapshot)
    if result.get("status") == "infra_error" or result.get("passed") is not expected:
        raise ValidationError(f"{label}: expected passed={expected}, got {result}")


def _solve_steps(manager: Any, attempt_id: str, steps: list[dict[str, str]], label: str) -> None:
    for index, step in enumerate(steps):
        _send_command(manager, attempt_id, step["command"], f"{label}:step-{index}")


def run_publication_gate(catalog_root: Path = DEFAULT_CATALOG) -> dict[str, Any]:
    scenarios = validate_catalog(catalog_root)
    try:
        from scripts.lab_runtime import LabManager
    except ModuleNotFoundError:  # direct ``python3 scripts/validate_scenarios.py``
        from lab_runtime import LabManager

    evidence: list[str] = []
    with tempfile.TemporaryDirectory(prefix="scenario-publication-") as temp:
        manager = LabManager(Path(catalog_root), Path(temp) / "state", validation_mode=True)
        try:
            capability = manager.capabilities()
            if capability.get("available") is not True:
                raise ValidationError("Bubblewrap publication runtime is unavailable")
            for scenario in scenarios:
                scenario_id = scenario["id"]
                first = manager.start(scenario_id, f"start:{scenario_id}:{uuid.uuid4().hex}")
                first_id = first["attempt"]["id"]
                _expect_check(manager, first_id, False, f"{scenario_id}:initial-fault")
                _solve_steps(manager, first_id, scenario["hints"], f"{scenario_id}:hints")
                _expect_check(manager, first_id, True, f"{scenario_id}:hint-solution")

                reset = manager.reset(first_id, f"reset:{scenario_id}:{uuid.uuid4().hex}")
                reset_id = reset["attempt"]["id"]
                _expect_check(manager, reset_id, False, f"{scenario_id}:reset-fault")
                _solve_steps(manager, reset_id, scenario["solution"]["steps"], f"{scenario_id}:solution")
                _expect_check(manager, reset_id, True, f"{scenario_id}:solution-pass")

                solved_id = reset_id
                if scenario_id in FORGED_OUTPUTS:
                    _send_command(manager, solved_id, FORGED_OUTPUTS[scenario_id], f"{scenario_id}:forged-output")
                    _expect_check(manager, solved_id, False, f"{scenario_id}:forged-output-reject")
                    rebuilt = manager.reset(solved_id, f"negative-reset:{scenario_id}:{uuid.uuid4().hex}")
                    solved_id = rebuilt["attempt"]["id"]
                    _expect_check(manager, solved_id, False, f"{scenario_id}:negative-reset-fault")
                    _solve_steps(manager, solved_id, scenario["solution"]["steps"], f"{scenario_id}:negative-resolve")
                    _expect_check(manager, solved_id, True, f"{scenario_id}:negative-precondition-pass")

                _send_command(manager, solved_id, NEGATIVE_TAMPERS[scenario_id], f"{scenario_id}:protected-tamper")
                _expect_check(manager, solved_id, False, f"{scenario_id}:protected-tamper-reject")

                if scenario_id in ALTERNATIVE_SOLUTIONS:
                    alternative = manager.reset(solved_id, f"alternative-reset:{scenario_id}:{uuid.uuid4().hex}")
                    alternative_id = alternative["attempt"]["id"]
                    _send_command(manager, alternative_id, ALTERNATIVE_SOLUTIONS[scenario_id], f"{scenario_id}:alternative")
                    _expect_check(manager, alternative_id, True, f"{scenario_id}:alternative-pass")
                evidence.append(f"{scenario_id}: initial fail, hints pass, reset fail, solution pass, protected tamper reject" + (", forged-output reject" if scenario_id in FORGED_OUTPUTS else "") + (", alternative pass" if scenario_id in ALTERNATIVE_SOLUTIONS else ""))
            admitted = {
                item["id"]: {"version": item["version"], "content_hash": item["content_hash"]}
                for item in manager.catalog()["scenarios"]
            }
        finally:
            manager.close()
    return {
        "evidence": evidence,
        "receipt": {
            "schema_version": 1,
            "adapter": "bwrap-userland",
            "runtime_versions": capability["versions"],
            "gate": {
                "cycles": 2,
                "negative": True,
                "alternative_scenarios": sorted(ALTERNATIVE_SOLUTIONS),
            },
            "scenarios": admitted,
        },
    }


def write_publication_receipt(catalog_root: Path, receipt: dict[str, Any]) -> Path:
    root = Path(catalog_root).absolute()
    target = root / "publication.json"
    temporary = root / f".publication.{uuid.uuid4().hex}.tmp"
    payload = json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    descriptor_hashes = {item["id"] for item in validate_catalog(root)}
    if descriptor_hashes != set(receipt.get("scenarios", {})):
        raise ValidationError("publication receipt does not cover the exact validated catalog")
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", help="static verification (also the default)")
    parser.add_argument("--runtime", action="store_true", help="run the isolated publication gate for trusted local packages")
    parser.add_argument("--publish", action="store_true", help="write publication.json after a successful runtime gate")
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        if args.publish and not args.runtime:
            raise ValidationError("--publish requires --runtime")
        scenarios = validate_catalog(args.catalog)
        report: dict[str, Any] = {
            "ok": True,
            "mode": "runtime" if args.runtime else "static",
            "scenario_count": len(scenarios),
            "scenario_ids": [item["id"] for item in scenarios],
            "import_boundary": "trusted reviewed repository-local packages only; static validation does not execute package code",
        }
        if args.runtime:
            gate = run_publication_gate(args.catalog)
            report["publication_evidence"] = gate["evidence"]
            if args.publish:
                receipt_path = write_publication_receipt(args.catalog, gate["receipt"])
                report["publication_receipt"] = str(receipt_path)
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    except (ValidationError, OSError, UnicodeError, ValueError, SyntaxError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False, sort_keys=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

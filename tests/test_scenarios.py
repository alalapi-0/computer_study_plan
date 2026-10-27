import json
import tempfile
import unittest
from pathlib import Path

from scripts.lab_runtime import LabManager
from scripts.validate_scenarios import DEFAULT_CATALOG, EXPECTED_IDS, FORGED_OUTPUTS, ValidationError, run_publication_gate, validate_catalog


class ScenarioCatalogTest(unittest.TestCase):
    def test_static_catalog_is_exact_and_complete(self):
        scenarios = validate_catalog()
        self.assertEqual({item["id"] for item in scenarios}, EXPECTED_IDS)
        self.assertEqual(len(scenarios), 8)
        for scenario in scenarios:
            self.assertEqual(scenario["environment"]["nodes"], ["lab"])
            self.assertEqual(scenario["provenance"]["type"], "teaching-adaptation")
            self.assertGreaterEqual(len(scenario["hints"]), 2)

    def test_static_validator_rejects_extra_package_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "catalog"
            root.mkdir()
            for package in DEFAULT_CATALOG.iterdir():
                if not package.is_dir():
                    continue
                target = root / package.name
                target.mkdir()
                for source in package.iterdir():
                    if source.name not in {"scenario.json", "setup.sh", "check.py"}:
                        continue
                    (target / source.name).write_bytes(source.read_bytes())
            (root / "path-cwd-input" / "unreviewed.bin").write_bytes(b"unexpected")
            with self.assertRaisesRegex(ValidationError, "exactly"):
                validate_catalog(root)

    def test_checkers_reject_protected_tamper_and_hints_publish(self):
        with tempfile.TemporaryDirectory() as temp:
            probe = LabManager(DEFAULT_CATALOG, Path(temp) / "probe-state")
            try:
                available = probe.capabilities()["available"]
            finally:
                probe.close()
            if not available:
                self.skipTest("rootless Bubblewrap unavailable")
        result = run_publication_gate()
        evidence = result["evidence"]
        self.assertEqual(len(evidence), 8)
        self.assertTrue(all("tamper reject" in item for item in evidence))
        self.assertTrue(any("alternative pass" in item for item in evidence))
        self.assertEqual(set(result["receipt"]["scenarios"]), EXPECTED_IDS)

    def test_git_checker_requires_original_commit_identities_not_only_count(self):
        with tempfile.TemporaryDirectory() as temp:
            manager = LabManager(DEFAULT_CATALOG, Path(temp) / "state", validation_mode=True)
            try:
                if not manager.capabilities()["available"]:
                    self.skipTest("rootless Bubblewrap unavailable")
                attempt_id = manager.start("git-preserve-work", "git-history-start")["attempt"]["id"]
                manager.execute(attempt_id, "cd /workspace/repo && git restore --source=HEAD^ -- app.py", "git-history-solve")
                passed = manager.check(attempt_id, "git-history-pass")["attempt"]["checks"][-1]
                self.assertTrue(passed["passed"])
                manager.execute(attempt_id, FORGED_OUTPUTS["git-preserve-work"], "git-history-replace")
                count = manager.execute(attempt_id, "cd /workspace/repo && git rev-list --count HEAD && python3 app.py && git status --porcelain=v1", "git-history-count")
                self.assertEqual(count["exit_code"], 0)
                self.assertEqual(count["stdout"].splitlines()[0:2], ["2", "15"])
                self.assertIn("settings.ini", count["stdout"])
                rejected = manager.check(attempt_id, "git-history-reject")["attempt"]["checks"][-1]
                self.assertFalse(rejected["passed"])
                self.assertIn("original commit identities or ancestry changed", rejected["evidence"])
            finally:
                manager.close()


if __name__ == "__main__":
    unittest.main()

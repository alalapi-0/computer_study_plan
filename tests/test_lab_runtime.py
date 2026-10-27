import json
import os
import tempfile
import time
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.lab_runtime import LabManager


SCENARIO = {
    "id": "repair-config",
    "version": 1,
    "title": "Repair the config",
    "summary": "A deterministic userland repair",
    "tags": ["shell"],
    "symptom": "The configured value is wrong.",
    "goal": "Set it to good.",
    "constraints": ["Do not create forbidden."],
    "environment": {"adapter": "bwrap-userland", "nodes": ["lab"], "shell": "bash", "required_tools": ["bash", "python3"]},
    "provenance": {"kind": "test"},
    "hints": [{"node": "lab", "shell": "bash", "command": "cat config", "expected": "bad", "explanation": "Inspect first.", "recovery": "Reset."}],
    "solution": {"steps": [{"node": "lab", "shell": "bash", "command": "printf good > config", "expected": "good", "explanation": "Repair it.", "recovery": "Reset."}], "explanation": "The value is the target state."},
}


CHECKER = r'''import json, pathlib, sys
mode = sys.argv[1]
p = pathlib.Path('/workspace/config')
if mode == 'ready':
    print(json.dumps({'ready': p.exists() and p.read_text() == 'bad', 'evidence': ['initial fault']}))
else:
    passed = p.exists() and p.read_text() == 'good' and not pathlib.Path('/workspace/forbidden').exists()
    print(json.dumps({'ready': not pathlib.Path('/workspace/unready').exists(), 'passed': passed, 'evidence': {'config': p.read_text() if p.exists() else None}, 'details': 'target and protection checked'}))
'''


class LabRuntimeTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.catalog = root / "catalog"
        self.state = root / "state"
        package = self.catalog / "repair-config"
        package.mkdir(parents=True)
        (package / "scenario.json").write_text(json.dumps(SCENARIO), encoding="utf-8")
        (package / "setup.sh").write_text("#!/bin/bash\nset -eu\nprintf bad > /workspace/config\n", encoding="utf-8")
        (package / "check.py").write_text(CHECKER, encoding="utf-8")
        self.manager = LabManager(self.catalog, self.state, validation_mode=True)
        if not self.manager.capabilities()["available"]:
            self.skipTest("rootless Bubblewrap unavailable")

    def tearDown(self):
        self.manager.close()
        self.temp.cleanup()

    def wait_output(self, attempt_id, needle, timeout=5):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            snap = self.manager.snapshot(attempt_id)
            if needle in snap["output"]:
                return snap
            time.sleep(0.05)
        self.fail(f"did not receive expected terminal marker: {needle}")

    def command(self, attempt_id, command, operation):
        self.manager.input(attempt_id, command + "\n", operation)
        return self.wait_output(attempt_id, command.split("echo ")[-1] if command.startswith("echo ") else "lab:")

    def test_real_start_solve_check_reset_and_retry(self):
        first = self.manager.start("repair-config", "start-1")
        attempt_id = first["attempt"]["id"]
        self.assertEqual(first["attempt"]["status"], "active")
        failed = self.manager.check(attempt_id, "check-before")
        self.assertEqual(failed["attempt"]["checks"][-1]["status"], "failed")
        self.manager.input(attempt_id, "printf good > config\n", "solve-1")
        passed = self.manager.check(attempt_id, "check-after")
        self.assertEqual(passed["attempt"]["checks"][-1]["status"], "passed")

        second = self.manager.reset(attempt_id, "reset-1")
        second_id = second["attempt"]["id"]
        self.assertNotEqual(second_id, attempt_id)
        self.assertEqual(self.manager.check(second_id, "check-reset")["attempt"]["checks"][-1]["status"], "failed")
        self.manager.input(second_id, "printf good > config\n", "solve-2")
        self.assertEqual(self.manager.check(second_id, "check-retry")["attempt"]["checks"][-1]["status"], "passed")
        self.assertEqual(len(self.manager.history()["attempts"]), 2)

    def test_validation_batch_is_deterministic_idempotent_and_private(self):
        attempt_id = self.manager.start("repair-config", "start-batch")["attempt"]["id"]
        first = self.manager.execute(attempt_id, "printf good > config; printf batch", "batch-op")
        replay = self.manager.execute(attempt_id, "printf good > config; printf batch", "batch-op")
        self.assertEqual(first, {"exit_code": 0, "stdout": "batch", "stderr": ""})
        self.assertEqual(replay, first)
        self.manager.close()
        normal = LabManager(self.catalog, Path(self.temp.name) / "normal-batch-state")
        with self.assertRaises(RuntimeError):
            normal.execute("missing", "true", "normal-batch")
        normal.close()
        self.manager = LabManager(self.catalog, self.state, validation_mode=True)

    def test_pty_resize_ctrl_c_and_reconnect_cursor(self):
        snap = self.manager.start("repair-config", "start-pty")
        attempt_id = snap["attempt"]["id"]
        self.manager.resize(attempt_id, 123, 37)
        self.manager.input(attempt_id, "stty size; echo RESIZED\n", "size")
        output = self.wait_output(attempt_id, "RESIZED")["output"]
        self.assertIn("37 123", output)
        cursor = self.manager.snapshot(attempt_id)["cursor"]
        self.manager.input(attempt_id, "sleep 30\n", "sleep")
        time.sleep(0.15)
        self.manager.input(attempt_id, "\x03", "ctrl-c")
        self.manager.input(attempt_id, "echo INTERRUPTED\n", "after-interrupt")
        reconnect = self.wait_output(attempt_id, "INTERRUPTED")
        delta = self.manager.snapshot(attempt_id, cursor=cursor)
        self.assertIn("INTERRUPTED", reconnect["output"])
        self.assertIn("INTERRUPTED", delta["output"])
        before_revision = reconnect["revision"]
        self.manager.input(attempt_id, "printf first\\nprintf second\\nprintf MULTI_DONE\\n\n", "multi-line")
        multiline = self.wait_output(attempt_id, "MULTI_DONE")
        self.assertIn("first", multiline["output"])
        self.assertIn("second", multiline["output"])
        self.assertGreater(multiline["revision"], before_revision)
        self.manager.input(
            attempt_id,
            "python3 -c \"import os,time; os.write(1,b'\\xe4'); time.sleep(.05); os.write(1,b'\\xbd\\xa0\\xe5\\xa5\\xbd\\n')\"\n",
            "split-utf8",
        )
        self.assertIn("你好", self.wait_output(attempt_id, "你好")["output"])

    def test_boundary_hides_host_package_environment_and_network(self):
        snap = self.manager.start("repair-config", "start-boundary")
        attempt_id = snap["attempt"]["id"]
        command = (
            "test ! -e /package && test ! -e /home && test ! -e /run && "
            "test \"$(pwd)\" = /workspace && test \"${HOME}\" = /workspace && "
            "python3 -c \"import socket; s=socket.socket(); s.settimeout(.2); "
            "print('NET_OPEN' if s.connect_ex(('1.1.1.1',53)) == 0 else 'NET_BLOCKED')\" && echo BOUNDARY_OK"
        )
        self.manager.input(attempt_id, command + "\n", "boundary")
        output = self.wait_output(attempt_id, "BOUNDARY_OK")["output"]
        self.assertIn("NET_BLOCKED", output)
        self.assertNotIn(str(Path.home()), output)

    def test_operation_replay_does_not_duplicate_input_or_checks(self):
        snap = self.manager.start("repair-config", "start-idem")
        attempt_id = snap["attempt"]["id"]
        command = "echo once >> replay-count"
        self.manager.input(attempt_id, command + "\n", "input-same")
        self.manager.input(attempt_id, command + "\n", "input-same")
        self.manager.input(attempt_id, "wc -l < replay-count; echo COUNTED\n", "count")
        output = self.wait_output(attempt_id, "COUNTED")["output"]
        self.assertIn("\r1\r\n", output)
        self.manager.check(attempt_id, "check-same")
        replay = self.manager.check(attempt_id, "check-same")
        self.assertEqual(len(replay["attempt"]["checks"]), 1)
        with self.assertRaises(ValueError):
            self.manager.input(attempt_id, "echo changed\n", "input-same")

    def test_stop_kills_pid_namespace_descendants(self):
        snap = self.manager.start("repair-config", "start-cleanup")
        attempt_id = snap["attempt"]["id"]
        self.manager.input(attempt_id, "(sleep 1; touch late-file) & echo SPAWNED\n", "spawn")
        self.wait_output(attempt_id, "SPAWNED")
        stopped = self.manager.stop(attempt_id, "stop-cleanup")
        self.assertEqual(stopped["attempt"]["status"], "stopped")
        time.sleep(1.2)
        workspace = self.state / "attempts" / attempt_id / "workspace"
        self.assertFalse(workspace.exists())

    def test_hint_and_solution_events_are_durable_and_once_only(self):
        attempt_id = self.manager.start("repair-config", "start-view")["attempt"]["id"]
        self.manager.view(attempt_id, "hints")
        self.manager.view(attempt_id, "hints")
        snap = self.manager.view(attempt_id, "solution")
        self.assertTrue(snap["attempt"]["hints_viewed"])
        self.assertTrue(snap["attempt"]["solution_viewed"])
        self.assertEqual([event["kind"] for event in snap["attempt"]["view_events"]], ["hints", "solution"])

    def test_checker_exit_zero_with_malformed_json_is_infrastructure_error(self):
        package = self.catalog / "bad-checker"
        bad = dict(SCENARIO, id="bad-checker", title="Bad checker")
        package.mkdir()
        (package / "scenario.json").write_text(json.dumps(bad), encoding="utf-8")
        (package / "setup.sh").write_text("#!/bin/bash\nprintf bad > /workspace/config\n", encoding="utf-8")
        (package / "check.py").write_text(
            "import json,sys\nfrom pathlib import Path\n"
            "print(json.dumps({'ready': True}) if sys.argv[1] == 'ready' else (Path('/workspace/checker-write').write_text('bad') or 'not-json'))\n",
            encoding="utf-8",
        )
        self.manager.close()
        self.manager = LabManager(self.catalog, self.state, validation_mode=True)
        attempt_id = self.manager.start("bad-checker", "start-bad-checker")["attempt"]["id"]
        result = self.manager.check(attempt_id, "check-bad-checker")
        self.assertEqual(result["attempt"]["checks"][-1]["status"], "infra_error")
        self.assertFalse(result["attempt"]["checks"][-1]["passed"])
        workspace = self.state / "attempts" / attempt_id / "workspace"
        self.assertFalse((workspace / "checker-write").exists())

    def test_checker_ready_false_is_infrastructure_error_even_if_passed(self):
        attempt_id = self.manager.start("repair-config", "start-unready")["attempt"]["id"]
        self.manager.execute(attempt_id, "printf good > config; touch unready", "make-unready")
        result = self.manager.check(attempt_id, "check-unready")
        check = result["attempt"]["checks"][-1]
        self.assertEqual(check["status"], "infra_error")
        self.assertFalse(check["passed"])

    def test_restart_marks_unrecoverable_active_attempt_lost(self):
        attempt_id = self.manager.start("repair-config", "start-restart")["attempt"]["id"]
        self.manager.close()
        state_file = self.state / "attempts.json"
        state = json.loads(state_file.read_text(encoding="utf-8"))
        target = next(item for item in state["attempts"] if item["id"] == attempt_id)
        target["status"] = "active"
        target["ended_at"] = None
        target["end_reason"] = None
        state_file.write_text(json.dumps(state), encoding="utf-8")
        self.manager = LabManager(self.catalog, self.state, validation_mode=True)
        snap = self.manager.snapshot(attempt_id)
        self.assertEqual(snap["attempt"]["status"], "lost")
        self.assertIsInstance(snap["output"], str)
        self.assertFalse((self.state / "attempts" / attempt_id).exists())

    def test_single_manager_lock_and_start_replaces_active(self):
        first = self.manager.start("repair-config", "start-first")
        with self.assertRaises(RuntimeError):
            LabManager(self.catalog, self.state, validation_mode=True)
        second = self.manager.start("repair-config", "start-second")
        self.assertEqual(self.manager.snapshot(first["attempt"]["id"])["attempt"]["status"], "stopped")
        self.assertEqual(second["attempt"]["status"], "active")

    def test_short_lived_request_thread_does_not_kill_shell(self):
        result = {}

        def request_thread():
            result["snapshot"] = self.manager.start("repair-config", "thread-start")

        thread = threading.Thread(target=request_thread)
        thread.start()
        thread.join(timeout=10)
        self.assertFalse(thread.is_alive())
        attempt_id = result["snapshot"]["attempt"]["id"]
        time.sleep(0.2)
        self.assertEqual(self.manager.snapshot(attempt_id)["attempt"]["status"], "active")
        self.manager.input(attempt_id, "echo THREAD_ALIVE\n", "thread-input")
        self.assertIn("THREAD_ALIVE", self.wait_output(attempt_id, "THREAD_ALIVE")["output"])

    def test_state_root_symbolic_link_is_rejected(self):
        self.manager.close()
        real = Path(self.temp.name) / "real-state"
        real.mkdir()
        link = Path(self.temp.name) / "linked-state"
        link.symlink_to(real, target_is_directory=True)
        with self.assertRaises(ValueError):
            LabManager(self.catalog, link, validation_mode=True)

    def test_corrupt_traversal_state_is_rejected_without_rewrite(self):
        attempt_id = self.manager.start("repair-config", "start-corrupt")["attempt"]["id"]
        self.manager.close()
        state_file = self.state / "attempts.json"
        state = json.loads(state_file.read_text(encoding="utf-8"))
        next(item for item in state["attempts"] if item["id"] == attempt_id)["workspace_name"] = "../outside"
        state_file.write_text(json.dumps(state), encoding="utf-8")
        before = state_file.read_bytes()
        with self.assertRaises(RuntimeError):
            LabManager(self.catalog, self.state, validation_mode=True)
        self.assertEqual(state_file.read_bytes(), before)
        # The failed constructor released its process lock.
        state_file.unlink()
        recovered = LabManager(self.catalog, self.state, validation_mode=True)
        recovered.close()

    def test_lifetime_and_output_limits_expire_and_cleanup(self):
        first = self.manager.start("repair-config", "start-lifetime")
        first_id = first["attempt"]["id"]
        with patch("scripts.lab_runtime._LIFETIME_SECONDS", 0.05):
            deadline = time.monotonic() + 2
            while time.monotonic() < deadline and self.manager.snapshot(first_id)["attempt"]["status"] == "active":
                time.sleep(0.05)
        self.assertEqual(self.manager.snapshot(first_id)["attempt"]["status"], "expired")
        self.assertFalse((self.state / "attempts" / first_id).exists())

        second_id = self.manager.start("repair-config", "start-output-limit")["attempt"]["id"]
        with patch("scripts.lab_runtime._OUTPUT_LIMIT", 2048):
            self.manager.input(second_id, "python3 -c \"print('x'*10000)\"\n", "flood")
            deadline = time.monotonic() + 3
            while time.monotonic() < deadline and self.manager.snapshot(second_id)["attempt"]["status"] == "active":
                time.sleep(0.05)
        snap = self.manager.snapshot(second_id)
        self.assertEqual(snap["attempt"]["status"], "expired")
        self.assertTrue(snap["attempt"]["output_truncated"])

    def test_workspace_limit_expires_attempt(self):
        attempt_id = self.manager.start("repair-config", "start-workspace-limit")["attempt"]["id"]
        self.manager.input(attempt_id, "python3 -c \"open('large','wb').write(b'x'*4096)\"\n", "large-file")
        with patch("scripts.lab_runtime._WORKSPACE_BYTES", 1024):
            deadline = time.monotonic() + 3
            while time.monotonic() < deadline and self.manager.snapshot(attempt_id)["attempt"]["status"] == "active":
                time.sleep(0.05)
        self.assertEqual(self.manager.snapshot(attempt_id)["attempt"]["status"], "expired")

    def test_publication_receipt_fails_closed_and_matches_exact_runtime(self):
        self.manager.close()
        draft_state = Path(self.temp.name) / "draft-state"
        draft = LabManager(self.catalog, draft_state)
        self.assertFalse(draft.catalog()["scenarios"][0]["playable"])
        with self.assertRaises(RuntimeError):
            draft.start("repair-config", "draft-start")
        versions = draft.capabilities()["versions"]
        draft.close()

        validator = LabManager(self.catalog, Path(self.temp.name) / "validation-state", validation_mode=True)
        scenario = validator.catalog()["scenarios"][0]
        validator.close()
        receipt = {
            "schema_version": 1,
            "adapter": "bwrap-userland",
            "runtime_versions": versions,
            "gate": {"cycles": 2, "negative": True, "alternative_scenarios": []},
            "scenarios": {"repair-config": {"version": 1, "content_hash": scenario["content_hash"]}},
        }
        (self.catalog / "publication.json").write_text(json.dumps(receipt), encoding="utf-8")
        self.manager = LabManager(self.catalog, Path(self.temp.name) / "published-state")
        listed = self.manager.catalog()["scenarios"][0]
        self.assertTrue(listed["playable"])
        self.assertEqual(listed["publication_status"], "published")
        self.assertEqual(self.manager.start("repair-config", "published-start")["attempt"]["status"], "active")


if __name__ == "__main__":
    unittest.main()

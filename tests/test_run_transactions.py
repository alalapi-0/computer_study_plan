from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import mark_done_cli  # noqa: E402
import progress_lib  # noqa: E402
from progress_server import ProgressRequestHandler  # noqa: E402


class RunTransactionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="computer-study-run-test-")
        self.root = Path(self.temp.name) / "repo"
        self.home = Path(self.temp.name) / "home"
        for relative in (
            "progress.json",
            "progress_data.js",
            "rounds_data.js",
            "records/action_logs/events.jsonl",
            "records/feedback/task_feedback.json",
            "rounds/round_00/week1/exercises.sh",
        ):
            source = REPO_ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
        self.sandbox = self.home / "cli-lab" / "round0"
        self.sandbox.mkdir(parents=True)

        data = progress_lib.load_progress(self.root)
        data["revision"] = 0
        for task_id in ("w1-ex1", "w1-ex2", "w1-self", "fin-sheet"):
            data["tasks"][task_id]["done"] = False
            data["tasks"][task_id]["done_at"] = None
        progress_lib.save_progress(data, self.root)
        progress_lib.sync_progress_data_js(data, self.root)
        progress_lib.write_action_events([], self.root)
        progress_lib.write_feedback_payload(data, self.root, events=[])

        self.home_patch = patch.dict(os.environ, {"HOME": str(self.home)})
        self.home_patch.start()

    def tearDown(self) -> None:
        self.home_patch.stop()
        self.temp.cleanup()

    @staticmethod
    def execution(result: str) -> dict:
        if result == "ok":
            returncode, timed_out = 0, False
        elif result == "failed":
            returncode, timed_out = 7, False
        elif result == "timeout":
            returncode, timed_out = None, True
        else:
            raise AssertionError(result)
        return {
            "result": result,
            "execution_ok": result == "ok",
            "returncode": returncode,
            "timed_out": timed_out,
            "duration_ms": 12,
            "script_path": "rounds/round_00/week1/exercises.sh",
            "sandbox_path": "",
            "stdout": f"{result} stdout",
            "stderr": "" if result == "ok" else f"{result} stderr",
        }

    def fake_execution(self, result: str, *, receipt: bool, calls: list[str] | None = None):
        def run(plan: dict, env: dict[str, str]) -> dict:
            if calls is not None:
                calls.append(env["PROGRESS_UI_RUN_TASK_ID"])
            if receipt:
                Path(env["PROGRESS_UI_RUN_RECEIPT"]).write_text(
                    json.dumps(
                        {
                            "token": env["PROGRESS_UI_RUN_TOKEN"],
                            "task_id": env["PROGRESS_UI_RUN_TASK_ID"],
                            "script_path": env["PROGRESS_UI_RUN_SCRIPT"],
                        },
                        separators=(",", ":"),
                    )
                    + "\n",
                    encoding="utf-8",
                )
            execution = self.execution(result)
            execution["script_path"] = plan["file"]
            execution["sandbox_path"] = str(plan["sandbox"])
            return execution

        return run

    def run_task(
        self,
        operation_id: str,
        *,
        task_id: str = "w1-ex1",
        result: str = "ok",
        receipt: bool = True,
        calls: list[str] | None = None,
    ) -> dict:
        with patch.object(
            progress_lib,
            "execute_run_plan",
            side_effect=self.fake_execution(result, receipt=receipt, calls=calls),
        ):
            return progress_lib.run_task_script(task_id, self.root, operation_id=operation_id)

    def assert_single_run_event(self, operation_id: str, result: str) -> dict:
        events = progress_lib.load_action_events(self.root)
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event["operation_id"], operation_id)
        self.assertEqual(event["action_type"], "run_exercise")
        self.assertEqual(event["result"], result)
        return event

    def assert_process_stopped(self, pid_path: Path) -> None:
        self.assertTrue(pid_path.exists(), "background descendant did not publish its pid")
        pid = int(pid_path.read_text(encoding="utf-8"))
        deadline = time.monotonic() + 1.5
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            time.sleep(0.02)
        try:
            os.kill(pid, 9)
        except ProcessLookupError:
            return
        self.fail(f"background descendant {pid} survived execute_run_plan")

    def descendant_plan(self, *, keep_parent_alive: bool) -> tuple[dict, dict[str, str], Path, Path]:
        process_sandbox = Path(self.temp.name) / "process-sandbox"
        process_sandbox.mkdir()
        sentinel = process_sandbox / "descendant-survived"
        pid_path = process_sandbox / "descendant.pid"
        child = (
            "import os,sys,time;"
            "open(sys.argv[2],\"w\").write(str(os.getpid()));"
            "time.sleep(0.7);"
            "open(sys.argv[1],\"w\").write(\"survived\")"
        )
        tail = "; sleep 5" if keep_parent_alive else ""
        shell = (
            '"$RUN_TEST_PYTHON" -c \'%s\' "$RUN_TEST_SENTINEL" "$RUN_TEST_PID" '
            '</dev/null >/dev/null 2>&1 & '
            'while [ ! -s "$RUN_TEST_PID" ]; do sleep 0.01; done%s'
        ) % (child, tail)
        env = os.environ.copy()
        env.update(
            {
                "RUN_TEST_PYTHON": sys.executable,
                "RUN_TEST_SENTINEL": str(sentinel),
                "RUN_TEST_PID": str(pid_path),
            }
        )
        plan = {
            "command": ["/bin/sh", "-c", shell],
            "sandbox": process_sandbox,
            "file": "isolated-process-group-test.sh",
        }
        return plan, env, sentinel, pid_path

    def repository_files(self) -> dict[Path, bytes]:
        return {
            path.relative_to(self.root): path.read_bytes()
            for path in self.root.rglob("*")
            if path.is_file()
        }

    def start_http_server(self) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
        handler = type("TempRunHandler", (ProgressRequestHandler,), {"repo_root": self.root})
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread, f"http://127.0.0.1:{server.server_address[1]}"

    def post_run(self, base: str, task_id: str, payload: object) -> tuple[int, dict]:
        request = Request(
            f"{base}/api/tasks/{task_id}/run",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=2) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            try:
                return error.code, json.loads(error.read().decode("utf-8"))
            finally:
                error.close()

    def test_verified_success_commits_completion_revision_event_and_replays_without_execution(self) -> None:
        calls: list[str] = []
        first = self.run_task("run-success", calls=calls)

        self.assertEqual(first["revision"], 1)
        self.assertTrue(first["tasks"]["w1-ex1"]["done"])
        self.assertTrue(first["execution"]["verification_reached"])
        self.assertTrue(first["execution"]["completion_applied"])
        self.assertFalse(first["execution"]["replayed_operation"])
        event = self.assert_single_run_event("run-success", "ok")
        self.assertTrue(event["details"]["verification_reached"])
        self.assertTrue(event["details"]["completion_applied"])
        ledger = progress_lib.load_run_operations(self.root)
        self.assertEqual(ledger["operations"]["run-success"]["status"], "committed")
        self.assertEqual(calls, ["w1-ex1"])

        replay = self.run_task("run-success", calls=calls)
        self.assertEqual(replay["revision"], 1)
        self.assertTrue(replay["execution"]["replayed_operation"])
        self.assertEqual(replay["execution"]["action_id"], first["execution"]["action_id"])
        self.assertEqual(calls, ["w1-ex1"])
        self.assert_single_run_event("run-success", "ok")

        with self.assertRaisesRegex(ValueError, "operation_id_conflict"):
            self.run_task("run-success", task_id="w1-ex2", calls=calls)
        self.assertEqual(calls, ["w1-ex1"])

    def test_known_outcomes_each_advance_once_but_only_verified_ok_completes(self) -> None:
        cases = (
            ("run-no-receipt", "ok", False, False),
            ("run-failed", "failed", True, True),
            ("run-timeout", "timeout", True, True),
        )
        for expected_revision, (operation_id, result, receipt, expected_verification) in enumerate(cases, 1):
            response = self.run_task(operation_id, result=result, receipt=receipt)
            execution = response["execution"]
            self.assertEqual(response["revision"], expected_revision)
            self.assertEqual(execution["result"], result)
            self.assertEqual(execution["verification_reached"], expected_verification)
            self.assertFalse(execution["completion_applied"])
            self.assertFalse(response["tasks"]["w1-ex1"]["done"])

        events = progress_lib.load_action_events(self.root)
        self.assertEqual([event["result"] for event in events], ["ok", "failed", "timeout"])
        self.assertEqual([event["operation_id"] for event in events], [case[0] for case in cases])
        self.assertTrue(all(not event["details"]["completion_applied"] for event in events))
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 3)

    def test_verified_success_on_already_done_task_records_run_without_recompleting(self) -> None:
        data = progress_lib.load_progress(self.root)
        data["tasks"]["w1-ex1"].update({"done": True, "done_at": "2026-08-14 10:00"})
        progress_lib.save_progress(data, self.root)
        progress_lib.sync_progress_data_js(data, self.root)

        response = self.run_task("run-already-done")
        self.assertEqual(response["revision"], 1)
        self.assertTrue(response["execution"]["verification_reached"])
        self.assertFalse(response["execution"]["completion_applied"])
        self.assertEqual(response["tasks"]["w1-ex1"]["done_at"], "2026-08-14 10:00")
        event = self.assert_single_run_event("run-already-done", "ok")
        self.assertFalse(event["details"]["completion_applied"])

    def test_pending_baseexception_recovers_forward_exactly_once_without_rerun(self) -> None:
        calls: list[str] = []
        with patch.object(
            progress_lib,
            "execute_run_plan",
            side_effect=self.fake_execution("ok", receipt=True, calls=calls),
        ), patch.object(
            progress_lib,
            "_apply_pending_run_operation",
            side_effect=KeyboardInterrupt("prepared-only"),
        ):
            with self.assertRaises(KeyboardInterrupt):
                progress_lib.run_task_script("w1-ex1", self.root, operation_id="run-recover")

        self.assertEqual(calls, ["w1-ex1"])
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 0)
        self.assertEqual(progress_lib.load_action_events(self.root), [])
        self.assertEqual(
            progress_lib.load_run_operations(self.root)["operations"]["run-recover"]["status"],
            "pending",
        )

        with progress_lib.progress_write_lock(self.root):
            progress_lib.recover_pending_operations(self.root)
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 1)
        self.assertTrue(progress_lib.load_progress(self.root)["tasks"]["w1-ex1"]["done"])
        self.assert_single_run_event("run-recover", "ok")
        self.assertEqual(
            progress_lib.load_run_operations(self.root)["operations"]["run-recover"]["status"],
            "committed",
        )

        with progress_lib.progress_write_lock(self.root):
            progress_lib.recover_pending_operations(self.root)
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 1)
        self.assert_single_run_event("run-recover", "ok")
        with patch.object(progress_lib, "execute_run_plan", side_effect=AssertionError("reran")):
            replay = progress_lib.run_task_script("w1-ex1", self.root, operation_id="run-recover")
        self.assertTrue(replay["execution"]["replayed_operation"])
        self.assertEqual(calls, ["w1-ex1"])

    def test_restore_that_removes_event_rejects_ghost_replay(self) -> None:
        calls: list[str] = []
        self.run_task("run-ghost", calls=calls)
        progress_lib.write_action_events([], self.root)

        with patch.object(progress_lib, "execute_run_plan", side_effect=AssertionError("reran")):
            with self.assertRaisesRegex(ValueError, "run_operation_event_not_in_current_history"):
                progress_lib.run_task_script("w1-ex1", self.root, operation_id="run-ghost")
        self.assertEqual(calls, ["w1-ex1"])
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 1)
        self.assertEqual(progress_lib.load_action_events(self.root), [])

    def test_receipt_gate_accepts_only_exact_requested_exercise_without_progress_writes(self) -> None:
        receipt = self.sandbox / "receipt.jsonl"
        receipt.write_text("", encoding="utf-8")
        token = "4c2d2d84-a05e-4607-b16f-9ecad5f45d85"
        env = {
            "HOME": str(self.home),
            "PROGRESS_UI_RUN": "1",
            "PROGRESS_UI_RUN_TASK_ID": "w1-ex1",
            "PROGRESS_UI_RUN_SCRIPT": "rounds/round_00/week1/exercises.sh",
            "PROGRESS_UI_RUN_RECEIPT": str(receipt),
            "PROGRESS_UI_RUN_TOKEN": token,
        }
        progress_before = (self.root / "progress.json").read_bytes()
        events_before = (self.root / "records/action_logs/events.jsonl").read_bytes()

        with patch.dict(os.environ, env, clear=False):
            self.assertEqual(mark_done_cli.record_ui_run_receipt("w1-ex2", False, self.root), 0)
            self.assertEqual(mark_done_cli.record_ui_run_receipt("w1-self", False, self.root), 1)
            self.assertEqual(mark_done_cli.record_ui_run_receipt("fin-sheet", False, self.root), 1)
            self.assertEqual(mark_done_cli.record_ui_run_receipt("w1-ex1", True, self.root), 1)
            self.assertEqual(mark_done_cli.record_ui_run_receipt("w1-ex1", False, self.root), 0)

        rows = [json.loads(line) for line in receipt.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(
            rows,
            [{"token": token, "task_id": "w1-ex1", "script_path": env["PROGRESS_UI_RUN_SCRIPT"]}],
        )
        self.assertEqual((self.root / "progress.json").read_bytes(), progress_before)
        self.assertEqual((self.root / "records/action_logs/events.jsonl").read_bytes(), events_before)

    def test_busy_sandbox_rejects_before_execution_or_ledger_reservation(self) -> None:
        plan = progress_lib.runnable_task_execution_plan("w1-ex1", self.root)
        with progress_lib.run_execution_lock(plan["sandbox"], self.root), patch.object(
            progress_lib,
            "execute_run_plan",
            side_effect=AssertionError("executed while busy"),
        ):
            with self.assertRaisesRegex(progress_lib.RunInProgressError, "run_in_progress"):
                progress_lib.run_task_script("w1-ex1", self.root, operation_id="run-busy")

        self.assertEqual(progress_lib.load_run_operations(self.root)["operations"], {})
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 0)
        self.assertEqual(progress_lib.load_action_events(self.root), [])

    def test_concurrent_same_sandbox_has_one_execution_and_one_busy_result(self) -> None:
        entered = threading.Event()
        release = threading.Event()
        calls: list[str] = []

        def blocking_execution(plan: dict, env: dict[str, str]) -> dict:
            calls.append(env["PROGRESS_UI_RUN_TASK_ID"])
            entered.set()
            self.assertTrue(release.wait(timeout=2))
            return self.fake_execution("ok", receipt=True)(plan, env)

        def first_run() -> dict:
            with patch.object(progress_lib, "execute_run_plan", side_effect=blocking_execution):
                return progress_lib.run_task_script("w1-ex1", self.root, operation_id="run-concurrent-a")

        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(first_run)
            self.assertTrue(entered.wait(timeout=2))
            with self.assertRaisesRegex(progress_lib.RunInProgressError, "run_in_progress"):
                progress_lib.run_task_script("w1-ex2", self.root, operation_id="run-concurrent-b")
            release.set()
            first = future.result(timeout=2)

        self.assertEqual(first["revision"], 1)
        self.assertEqual(calls, ["w1-ex1"])
        self.assertNotIn("run-concurrent-b", progress_lib.load_run_operations(self.root)["operations"])

    def test_execute_run_plan_cleans_background_group_after_normal_parent_exit(self) -> None:
        plan, env, sentinel, pid_path = self.descendant_plan(keep_parent_alive=False)
        result = progress_lib.execute_run_plan(plan, env)

        self.assertEqual(result["result"], "ok")
        self.assertEqual(result["returncode"], 0)
        self.assertFalse(result["timed_out"])
        self.assert_process_stopped(pid_path)
        time.sleep(0.75)
        self.assertFalse(sentinel.exists(), "terminated descendant wrote its delayed sentinel")

    def test_execute_run_plan_timeout_cleans_background_group(self) -> None:
        plan, env, sentinel, pid_path = self.descendant_plan(keep_parent_alive=True)
        with patch.object(progress_lib, "RUN_TIMEOUT_SECONDS", 0.2):
            result = progress_lib.execute_run_plan(plan, env)

        self.assertEqual(result["result"], "timeout")
        self.assertIsNone(result["returncode"])
        self.assertTrue(result["timed_out"])
        self.assert_process_stopped(pid_path)
        time.sleep(0.75)
        self.assertFalse(sentinel.exists(), "timed-out descendant wrote its delayed sentinel")

    def test_invalid_run_ledgers_fail_before_sandbox_creation_execution_or_other_repo_writes(self) -> None:
        shutil.rmtree(self.home / "cli-lab")
        ledger_path = progress_lib.run_operations_path(self.root)
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        invalid_ledgers = {
            "wrong_version": {"version": 2, "operations": {}},
            "missing_version": {"operations": {}},
            "extra_top_level": {"version": 1, "operations": {}, "extra": True},
            "invalid_operation_record": {
                "version": 1,
                "operations": {"broken-run": {"status": "executing"}},
            },
        }

        for name, payload in invalid_ledgers.items():
            with self.subTest(name=name):
                ledger_path.write_text(json.dumps(payload) + "\n", encoding="utf-8")
                before = {
                    path.relative_to(self.root): path.read_bytes()
                    for path in self.root.rglob("*")
                    if path.is_file()
                }
                with patch.object(
                    progress_lib,
                    "execute_run_plan",
                    side_effect=AssertionError("executed before WAL validation"),
                ):
                    with self.assertRaises(ValueError):
                        progress_lib.run_task_script("w1-ex1", self.root, operation_id=f"invalid-{name}")
                after = {
                    path.relative_to(self.root): path.read_bytes()
                    for path in self.root.rglob("*")
                    if path.is_file()
                }
                self.assertEqual(after, before)
                self.assertFalse(self.sandbox.exists())

    def test_http_run_contract_rejections_success_replay_and_conflict(self) -> None:
        shutil.rmtree(self.home / "cli-lab")
        server, thread, base = self.start_http_server()
        try:
            invalid_requests = (
                ({}, "w1-ex1"),
                ({"operation_id": None}, "w1-ex1"),
                ({"operation_id": ""}, "w1-ex1"),
                ({"operation_id": "bad/id"}, "w1-ex1"),
                ({"operation_id": "extra-field", "extra": True}, "w1-ex1"),
                ({"operation_id": "unknown-task"}, "does-not-exist"),
            )
            before = self.repository_files()
            for payload, task_id in invalid_requests:
                with self.subTest(payload=payload, task_id=task_id):
                    status, body = self.post_run(base, task_id, payload)
                    self.assertGreaterEqual(status, 400)
                    self.assertLess(status, 500)
                    self.assertFalse(body["ok"])
                    self.assertEqual(self.repository_files(), before)
                    self.assertFalse(self.sandbox.exists())

            calls: list[str] = []
            fake = self.fake_execution("ok", receipt=True, calls=calls)
            with patch.object(progress_lib, "execute_run_plan", side_effect=fake):
                status, first = self.post_run(base, "w1-ex1", {"operation_id": "http-run"})
                self.assertEqual(status, 200)
                self.assertEqual(set(first), {"ok", "execution", "tasks", "lanes", "feedback", "revision"})
                self.assertTrue(first["ok"])
                self.assertEqual(first["revision"], 1)
                execution = first["execution"]
                self.assertEqual(
                    set(execution),
                    {
                        "result",
                        "execution_ok",
                        "returncode",
                        "timed_out",
                        "duration_ms",
                        "script_path",
                        "sandbox_path",
                        "stdout",
                        "stderr",
                        "verification_reached",
                        "completion_applied",
                        "task_id",
                        "action_id",
                        "event",
                        "operation_id",
                        "replayed_operation",
                        "revision",
                        "total",
                        "done_count",
                    },
                )
                self.assertEqual(execution["operation_id"], "http-run")
                self.assertEqual(execution["revision"], first["revision"])
                self.assertEqual(execution["event"]["operation_id"], "http-run")
                self.assertEqual(execution["event"]["action_id"], execution["action_id"])
                self.assertFalse(execution["replayed_operation"])
                self.assertTrue(execution["completion_applied"])
                self.assertEqual(calls, ["w1-ex1"])

                status, replay = self.post_run(base, "w1-ex1", {"operation_id": "http-run"})
                self.assertEqual(status, 200)
                self.assertEqual(replay["revision"], 1)
                self.assertTrue(replay["execution"]["replayed_operation"])
                self.assertEqual(replay["execution"]["action_id"], execution["action_id"])
                self.assertEqual(calls, ["w1-ex1"])

                committed = self.repository_files()
                status, conflict = self.post_run(base, "w1-ex2", {"operation_id": "http-run"})
                self.assertEqual(status, 400)
                self.assertEqual(conflict["error"], "operation_id_conflict")
                self.assertEqual(self.repository_files(), committed)
                self.assertEqual(calls, ["w1-ex1"])
                self.assertEqual(len(progress_lib.load_action_events(self.root)), 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()

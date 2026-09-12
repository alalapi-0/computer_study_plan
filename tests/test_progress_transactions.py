from __future__ import annotations

import json
import shutil
import sys
import tempfile
import threading
import unittest
from contextlib import ExitStack, contextmanager
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import progress_lib  # noqa: E402
import mark_done_cli  # noqa: E402
from progress_server import ProgressRequestHandler  # noqa: E402


class ProgressTransactionTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="computer-study-progress-test-")
        self.root = Path(self.temp.name)
        for relative in (
            "progress.json",
            "progress_data.js",
            "rounds_data.js",
            "records/action_logs/events.jsonl",
            "records/feedback/task_feedback.json",
            "records/terminal/commands.jsonl",
        ):
            source = REPO_ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.exists():
                shutil.copy2(source, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def state_preimages(self) -> dict[Path, bytes | None]:
        return {
            path: path.read_bytes() if path.exists() else None
            for path in progress_lib.task_transaction_paths(self.root)
        }

    def assert_preimages(self, expected: dict[Path, bytes | None]) -> None:
        self.assertEqual(self.state_preimages(), expected)

    def repository_preimages(self) -> dict[Path, bytes]:
        return self.repository_preimages_for(self.root)

    def repository_preimages_for(self, root: Path) -> dict[Path, bytes]:
        return {
            path.relative_to(root): path.read_bytes()
            for path in root.rglob("*")
            if path.is_file()
        }

    @contextmanager
    def pending_operation_fixture(self):
        """Yield an isolated repo stopped after WAL prepare and before state writes."""
        with tempfile.TemporaryDirectory(prefix="computer-study-pending-wal-test-") as temp:
            root = Path(temp)
            for relative in (
                "progress.json",
                "progress_data.js",
                "rounds_data.js",
                "records/action_logs/events.jsonl",
                "records/feedback/task_feedback.json",
            ):
                source = REPO_ROOT / relative
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
            with patch.object(progress_lib, "save_progress", side_effect=KeyboardInterrupt("prepared_only")):
                with self.assertRaises(KeyboardInterrupt):
                    progress_lib.mark_task(
                        "w1-read",
                        root=root,
                        note="durable note",
                        evidence_path="tmp/evidence",
                        operation_id="wal-validation",
                    )
            self.assertEqual(progress_lib.load_progress(root).get("revision", 0), 0)
            self.assertEqual(progress_lib.load_action_events(root), [])
            yield root

    def invoke_pending_recovery_entrypoint(self, entrypoint: str, root: Path) -> None:
        if entrypoint == "recover":
            progress_lib.recover_pending_task_operations(root)
            return
        if entrypoint == "cli":
            with patch.object(mark_done_cli, "repo_root", return_value=root):
                mark_done_cli.print_status(limit=1)
            return
        if entrypoint == "get":
            handler = object.__new__(ProgressRequestHandler)
            handler.repo_root = root
            handler.path = "/api/progress"
            handler.end_json = Mock()
            handler.do_GET()
            return
        raise AssertionError(f"unknown recovery entrypoint: {entrypoint}")

    def read_events(self) -> list[dict]:
        return progress_lib.load_action_events(self.root)

    def read_progress_mirror(self) -> dict:
        text = (self.root / "progress_data.js").read_text(encoding="utf-8")
        prefix = "window.PROGRESS_DATA = "
        start = text.index(prefix) + len(prefix)
        return json.loads(text[start:].strip().removesuffix(";"))

    def start_http_server(self) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
        handler = type("TempProgressHandler", (ProgressRequestHandler,), {"repo_root": self.root})
        server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        return server, thread, f"http://127.0.0.1:{server.server_address[1]}"

    def post_task_action(self, base: str, task_path: str, action: str, payload: dict) -> tuple[int, dict]:
        request = Request(
            f"{base}/api/tasks/{task_path}/{action}",
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
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

    def test_done_replay_conflict_and_noop_have_stable_revision(self) -> None:
        first = progress_lib.mark_task(
            "w1-read",
            root=self.root,
            note="first note",
            evidence_path="tmp/evidence",
            operation_id="operation-done-1",
        )
        self.assertEqual(first["revision"], 1)
        self.assertTrue(first["done"])
        self.assertEqual(len(self.read_events()), 1)
        committed = self.state_preimages()

        replay = progress_lib.mark_task(
            "w1-read",
            root=self.root,
            note="first note",
            evidence_path="tmp/evidence",
            operation_id="operation-done-1",
        )
        self.assertEqual(replay["result"], "replayed_operation")
        self.assertEqual(replay["revision"], 1)
        self.assertEqual(replay["action_id"], first["action_id"])
        self.assert_preimages(committed)

        with self.assertRaisesRegex(ValueError, "operation_id_conflict"):
            progress_lib.mark_task(
                "w1-read",
                root=self.root,
                note="changed note",
                evidence_path="tmp/evidence",
                operation_id="operation-done-1",
            )
        self.assert_preimages(committed)

        noop = progress_lib.mark_task("w1-read", root=self.root, operation_id="operation-done-2")
        self.assertEqual(noop["result"], "noop_already_done")
        self.assertEqual(noop["revision"], 2)
        undone = progress_lib.mark_task("w1-read", undo=True, root=self.root, operation_id="operation-undo-1")
        self.assertFalse(undone["done"])
        self.assertEqual(undone["revision"], 3)
        undo_noop = progress_lib.mark_task("w1-read", undo=True, root=self.root, operation_id="operation-undo-2")
        self.assertEqual(undo_noop["result"], "noop_already_undone")
        self.assertEqual(undo_noop["revision"], 4)
        self.assertEqual(len(self.read_events()), 4)

    def test_concurrent_different_tasks_and_same_operation_do_not_lose_updates(self) -> None:
        barrier = threading.Barrier(2)

        def mark(task_id: str, operation_id: str) -> dict:
            barrier.wait(timeout=2)
            return progress_lib.mark_task(task_id, root=self.root, operation_id=operation_id)

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda args: mark(*args), [
                ("w1-read", "parallel-a"),
                ("w1-ex1", "parallel-b"),
            ]))
        progress = progress_lib.load_progress(self.root)
        self.assertTrue(progress["tasks"]["w1-read"]["done"])
        self.assertTrue(progress["tasks"]["w1-ex1"]["done"])
        self.assertEqual(progress["revision"], 2)
        self.assertEqual({item["revision"] for item in results}, {1, 2})
        self.assertEqual(len(self.read_events()), 2)

        same_root = self.root
        # Return the fixture to a clean state for the same-id race.
        shutil.copy2(REPO_ROOT / "progress.json", same_root / "progress.json")
        shutil.copy2(REPO_ROOT / "progress_data.js", same_root / "progress_data.js")
        shutil.copy2(REPO_ROOT / "records/feedback/task_feedback.json", same_root / "records/feedback/task_feedback.json")
        (same_root / "records/action_logs/events.jsonl").write_text("", encoding="utf-8")
        (same_root / "records/action_logs/task_operations.json").unlink(missing_ok=True)
        barrier = threading.Barrier(2)

        def same_mark() -> dict:
            barrier.wait(timeout=2)
            return progress_lib.mark_task("w1-read", root=same_root, note="same", operation_id="parallel-same")

        with ThreadPoolExecutor(max_workers=2) as pool:
            same_results = [future.result() for future in [pool.submit(same_mark), pool.submit(same_mark)]]
        self.assertEqual({item["result"] for item in same_results}, {"ok", "replayed_operation"})
        self.assertEqual(progress_lib.load_progress(same_root)["revision"], 1)
        self.assertEqual(len(progress_lib.load_action_events(same_root)), 1)

    def test_each_caught_write_failure_restores_exact_preimage_and_retry_commits_once(self) -> None:
        failure_points = ["sync_progress_data_js", "write_action_events", "write_feedback_payload"]
        for name in failure_points:
            with self.subTest(name=name):
                nested = self.root / name
                nested.mkdir(parents=True)
                for relative in (
                    "progress.json",
                    "progress_data.js",
                    "rounds_data.js",
                    "records/action_logs/events.jsonl",
                    "records/feedback/task_feedback.json",
                ):
                    source = REPO_ROOT / relative
                    target = nested / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)
                paths = progress_lib.task_transaction_paths(nested)
                before = {path: path.read_bytes() if path.exists() else None for path in paths}
                original = getattr(progress_lib, name)

                def fail(*_args, **_kwargs):
                    raise OSError(f"planned_{name}_failure")

                with patch.object(progress_lib, name, side_effect=fail):
                    with self.assertRaisesRegex(OSError, f"planned_{name}_failure"):
                        progress_lib.mark_task("w1-read", root=nested, note="retry me", operation_id=f"fault-{name}")
                after = {path: path.read_bytes() if path.exists() else None for path in paths}
                self.assertEqual(after, before)

                with patch.object(progress_lib, name, wraps=original):
                    result = progress_lib.mark_task("w1-read", root=nested, note="retry me", operation_id=f"fault-{name}")
                self.assertEqual(result["revision"], 1)
                self.assertEqual(len(progress_lib.load_action_events(nested)), 1)

    def test_pending_wal_recovers_after_uncaught_interruption(self) -> None:
        original_sync = progress_lib.sync_progress_data_js
        with patch.object(progress_lib, "sync_progress_data_js", side_effect=KeyboardInterrupt("planned_crash")):
            with self.assertRaises(KeyboardInterrupt):
                progress_lib.mark_task("w1-read", root=self.root, note="durable", operation_id="crash-recovery")

        ledger = progress_lib.load_task_operations(self.root)
        self.assertEqual(ledger["operations"]["crash-recovery"]["status"], "pending")
        with patch.object(progress_lib, "sync_progress_data_js", wraps=original_sync):
            replay = progress_lib.mark_task("w1-read", root=self.root, note="durable", operation_id="crash-recovery")
        self.assertEqual(replay["result"], "replayed_operation")
        self.assertEqual(replay["revision"], 1)
        self.assertEqual(len(self.read_events()), 1)
        self.assertEqual(progress_lib.load_task_operations(self.root)["operations"]["crash-recovery"]["status"], "committed")
        self.assertEqual(self.read_progress_mirror()["revision"], progress_lib.load_progress(self.root)["revision"])

    def test_valid_pending_wal_rolls_forward_once_and_repeated_recovery_is_idempotent(self) -> None:
        with self.pending_operation_fixture() as root:
            progress_lib.recover_pending_task_operations(root)
            committed = self.repository_preimages_for(root)
            self.assertTrue(progress_lib.load_progress(root)["tasks"]["w1-read"]["done"])
            self.assertEqual(progress_lib.load_progress(root)["revision"], 1)
            self.assertEqual(len(progress_lib.load_action_events(root)), 1)
            self.assertEqual(
                progress_lib.load_task_operations(root)["operations"]["wal-validation"]["status"],
                "committed",
            )

            progress_lib.recover_pending_task_operations(root)
            self.assertEqual(self.repository_preimages_for(root), committed)
            self.assertEqual(len(progress_lib.load_action_events(root)), 1)

    def test_tampered_pending_wal_is_rejected_before_any_repository_write(self) -> None:
        def set_request(record: dict, field: str, value) -> None:
            record["request"][field] = value
            record["request_fingerprint"] = progress_lib.task_operation_fingerprint(record["request"])

        def remove_event_action_id(_ledger: dict, record: dict, _root: Path) -> None:
            record["event"].pop("action_id")

        def set_event(field: str, value):
            return lambda _ledger, record, _root: record["event"].__setitem__(field, value)

        def set_request_field(field: str, value):
            return lambda _ledger, record, _root: set_request(record, field, value)

        def set_task_state(field: str, value):
            return lambda _ledger, record, _root: record["task_state"].__setitem__(field, value)

        def set_record(field: str, value):
            return lambda _ledger, record, _root: record.__setitem__(field, value)

        def set_current_snapshot_to_target_without_task_state(
            _ledger: dict,
            record: dict,
            root: Path,
        ) -> None:
            progress = progress_lib.load_progress(root)
            progress["revision"] = record["target_revision"]
            (root / "progress.json").write_text(
                json.dumps(progress, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        def rename_ledger_key(ledger: dict, record: dict, _root: Path) -> None:
            ledger["operations"]["different-valid-key"] = record
            del ledger["operations"]["wal-validation"]

        tamper_cases = (
            ("event_action_id_missing", remove_event_action_id),
            ("event_action_id_empty", set_event("action_id", "")),
            ("event_action_id_invalid", set_event("action_id", "not-a-uuid")),
            ("request_fingerprint", set_record("request_fingerprint", "0" * 64)),
            ("request_task", set_request_field("task_id", "w1-ex1")),
            ("request_action", set_request_field("action", "undo")),
            ("request_note", set_request_field("note", "different request note")),
            ("request_evidence", set_request_field("evidence_path", "different/request/evidence")),
            ("event_task", set_event("task_id", "w1-ex1")),
            ("event_action_type", set_event("action_type", "undo_done")),
            ("event_result", set_event("result", "noop_already_done")),
            ("event_lane", set_event("lane", "different-lane")),
            ("event_operation_id", set_event("operation_id", "different-operation")),
            ("event_note", set_event("note", "different event note")),
            ("event_evidence", set_event("evidence_path", "different/event/evidence")),
            ("task_state_done", set_task_state("done", False)),
            ("task_state_done_at", set_task_state("done_at", None)),
            ("task_state_lane", set_task_state("lane", "different-lane")),
            ("base_revision", set_record("base_revision", 1)),
            ("target_revision", set_record("target_revision", 2)),
            ("current_snapshot", set_current_snapshot_to_target_without_task_state),
            ("ledger_key", rename_ledger_key),
        )

        for case_name, tamper in tamper_cases:
            for entrypoint in ("recover", "cli", "get"):
                with self.subTest(case=case_name, entrypoint=entrypoint):
                    with self.pending_operation_fixture() as root:
                        ledger = progress_lib.load_task_operations(root)
                        record = ledger["operations"]["wal-validation"]
                        tamper(ledger, record, root)
                        # Deliberately bypass the production writer: it now validates
                        # every record before persisting, while this fixture must model
                        # an already-corrupted WAL left on disk by an external fault.
                        progress_lib.task_operations_path(root).write_text(
                            json.dumps(ledger, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8",
                        )
                        before = self.repository_preimages_for(root)

                        with self.assertRaises(ValueError):
                            self.invoke_pending_recovery_entrypoint(entrypoint, root)

                        self.assertEqual(self.repository_preimages_for(root), before)

    def test_cli_status_rolls_pending_wal_forward_before_reading(self) -> None:
        with patch.object(progress_lib, "sync_progress_data_js", side_effect=KeyboardInterrupt("planned_crash")):
            with self.assertRaises(KeyboardInterrupt):
                progress_lib.mark_task("w1-read", root=self.root, note="cli recovery", operation_id="cli-recovery")

        with patch.object(mark_done_cli, "repo_root", return_value=self.root):
            self.assertEqual(mark_done_cli.print_status(limit=1), 0)
        self.assertTrue(progress_lib.load_progress(self.root)["tasks"]["w1-read"]["done"])
        self.assertEqual(len(self.read_events()), 1)
        self.assertEqual(progress_lib.load_task_operations(self.root)["operations"]["cli-recovery"]["status"], "committed")

    def test_restore_advances_revision_and_preserves_idempotency_ledger(self) -> None:
        saved = progress_lib.create_progress_save(root=self.root, label="before action")
        done = progress_lib.mark_task("w1-read", root=self.root, note="later action", operation_id="after-save")
        self.assertEqual(done["revision"], 1)

        restored = progress_lib.load_progress_save(saved["save_id"], root=self.root)
        self.assertEqual(restored["revision"], 2)
        self.assertFalse(restored["tasks"]["w1-read"]["done"])
        self.assertEqual(self.read_events(), [])
        self.assertEqual(self.read_progress_mirror()["revision"], progress_lib.load_progress(self.root)["revision"])
        self.assertEqual(
            progress_lib.load_task_operations(self.root)["operations"]["after-save"]["status"],
            "committed",
        )
        restored_preimage = self.repository_preimages()

        with self.assertRaisesRegex(ValueError, "operation_event_not_in_current_history"):
            progress_lib.mark_task("w1-read", root=self.root, note="later action", operation_id="after-save")

        self.assertEqual(self.repository_preimages(), restored_preimage)
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 2)
        self.assertEqual(self.read_events(), [])
        self.assertEqual(
            progress_lib.load_task_operations(self.root)["operations"]["after-save"]["status"],
            "committed",
        )

    def test_http_rejects_replay_when_restore_removed_operation_event_without_writes(self) -> None:
        saved = progress_lib.create_progress_save(root=self.root, label="before http action")
        done = progress_lib.mark_task(
            "w1-read",
            root=self.root,
            note="later http action",
            operation_id="after-http-save",
        )
        self.assertEqual(done["revision"], 1)

        restored = progress_lib.load_progress_save(saved["save_id"], root=self.root)
        self.assertEqual(restored["revision"], 2)
        self.assertEqual(self.read_events(), [])
        self.assertEqual(
            progress_lib.load_task_operations(self.root)["operations"]["after-http-save"]["status"],
            "committed",
        )
        restored_preimage = self.repository_preimages()

        server, thread, base = self.start_http_server()
        try:
            status, payload = self.post_task_action(
                base,
                "w1-read",
                "done",
                {"operation_id": "after-http-save", "note": "later http action"},
            )
            self.assertEqual(status, 400)
            self.assertEqual(payload["error"], "operation_event_not_in_current_history")
            self.assertIs(payload["ok"], False)
            self.assertNotIn("event", payload)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

        self.assertEqual(self.repository_preimages(), restored_preimage)
        self.assertEqual(progress_lib.load_progress(self.root)["revision"], 2)
        self.assertEqual(self.read_events(), [])
        self.assertEqual(
            progress_lib.load_task_operations(self.root)["operations"]["after-http-save"]["status"],
            "committed",
        )

    def test_restore_rejects_inconsistent_completion_before_any_state_write(self) -> None:
        saved = progress_lib.create_progress_save(root=self.root, label="completion invariant")
        save_path = progress_lib.progress_save_path(saved["save_id"], self.root)
        valid_payload = json.loads(save_path.read_text(encoding="utf-8"))
        progress_lib.mark_task(
            "w1-read",
            root=self.root,
            note="state after save",
            operation_id="after-completion-invariant-save",
        )

        invalid_states = (
            ("incomplete_with_timestamp", False, "2026-08-14T12:00:00"),
            ("complete_with_null_timestamp", True, None),
            ("complete_with_empty_timestamp", True, ""),
        )
        write_entrypoints = (
            "_create_progress_save_unlocked",
            "save_progress",
            "sync_progress_data_js",
            "write_action_events",
            "write_feedback_payload",
            "write_terminal_commands",
        )
        for name, done, done_at in invalid_states:
            with self.subTest(name=name):
                invalid_payload = json.loads(json.dumps(valid_payload))
                invalid_payload["progress"]["tasks"]["w1-ex1"].update(
                    done=done,
                    done_at=done_at,
                )
                save_path.write_text(
                    json.dumps(invalid_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                before_files = self.repository_preimages()
                before_saves = progress_lib.list_progress_saves(self.root)
                before_records = {
                    "events": progress_lib.load_action_events(self.root),
                    "operations": progress_lib.load_task_operations(self.root),
                    "feedback": progress_lib.read_feedback_payload(self.root),
                    "terminal": progress_lib.load_terminal_commands(self.root),
                }

                with ExitStack() as stack:
                    writers = [
                        stack.enter_context(
                            patch.object(progress_lib, entrypoint, wraps=getattr(progress_lib, entrypoint))
                        )
                        for entrypoint in write_entrypoints
                    ]
                    with self.assertRaisesRegex(ValueError, "invalid_task_done_at:w1-ex1"):
                        progress_lib.load_progress_save(saved["save_id"], root=self.root)
                    for writer in writers:
                        writer.assert_not_called()

                self.assertEqual(self.repository_preimages(), before_files)
                self.assertEqual(progress_lib.list_progress_saves(self.root), before_saves)
                self.assertEqual(progress_lib.load_action_events(self.root), before_records["events"])
                self.assertEqual(progress_lib.load_task_operations(self.root), before_records["operations"])
                self.assertEqual(progress_lib.read_feedback_payload(self.root), before_records["feedback"])
                self.assertEqual(progress_lib.load_terminal_commands(self.root), before_records["terminal"])

        save_path.write_text(
            json.dumps(valid_payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        restored = progress_lib.load_progress_save(saved["save_id"], root=self.root)
        self.assertFalse(restored["tasks"]["w1-read"]["done"])
        self.assertFalse(restored["tasks"]["w1-ex1"]["done"])
        self.assertEqual(restored["backup"]["reason"], "auto-before-load")

    def test_http_api_rejects_non_string_and_overlong_operation_ids(self) -> None:
        server, thread, base = self.start_http_server()

        def post(operation_id) -> tuple[int, dict]:
            request = Request(
                f"{base}/api/tasks/w1-read/done",
                data=json.dumps({"operation_id": operation_id, "note": "api"}).encode("utf-8"),
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

        try:
            for invalid in (123, True, None, "", "x" * 121):
                status, payload = post(invalid)
                self.assertEqual(status, 400)
                self.assertIn("operation_id", payload["error"])
            self.assertFalse(progress_lib.load_progress(self.root)["tasks"]["w1-read"]["done"])
            status, payload = post("valid-api-operation")
            self.assertEqual(status, 200)
            self.assertTrue(payload["done"])
            self.assertEqual(payload["revision"], 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_http_task_text_limits_are_code_point_exact_and_rejections_do_not_reserve_operation(self) -> None:
        server, thread, base = self.start_http_server()
        try:
            before = self.state_preimages()
            status, payload = self.post_task_action(
                base,
                "w1-read",
                "done",
                {"operation_id": "note-limit", "note": "a" * 500 + "b"},
            )
            self.assertEqual(status, 400)
            self.assertIn("too_long", payload["error"])
            self.assert_preimages(before)

            status, payload = self.post_task_action(
                base,
                "w1-read",
                "done",
                {"operation_id": "note-limit", "note": "a" * 500},
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload["revision"], 1)
            self.assertEqual(self.read_events()[-1]["note"], "a" * 500)
            self.assertEqual(self.read_progress_mirror()["revision"], 1)

            astral_500 = "\U0001f680" * 500
            committed = self.state_preimages()
            status, payload = self.post_task_action(
                base,
                "w1-ex1",
                "done",
                {"operation_id": "astral-limit", "evidence_path": astral_500 + "\U0001f680"},
            )
            self.assertEqual(status, 400)
            self.assertIn("too_long", payload["error"])
            self.assert_preimages(committed)

            status, payload = self.post_task_action(
                base,
                "w1-ex1",
                "done",
                {"operation_id": "astral-limit", "evidence_path": astral_500},
            )
            self.assertEqual(status, 200)
            self.assertEqual(payload["revision"], 2)
            self.assertEqual(self.read_events()[-1]["evidence_path"], astral_500)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_http_operation_fingerprint_distinguishes_payload_but_normalizes_missing_empty_text(self) -> None:
        server, thread, base = self.start_http_server()
        try:
            status, first = self.post_task_action(
                base,
                "w1-read",
                "done",
                {"operation_id": "fingerprint-conflict", "note": "same-prefix-a"},
            )
            self.assertEqual(status, 200)
            committed = self.state_preimages()
            status, conflict = self.post_task_action(
                base,
                "w1-read",
                "done",
                {"operation_id": "fingerprint-conflict", "note": "same-prefix-b"},
            )
            self.assertEqual(status, 400)
            self.assertEqual(conflict["error"], "operation_id_conflict")
            self.assert_preimages(committed)

            status, empty_first = self.post_task_action(
                base,
                "w1-ex1",
                "done",
                {"operation_id": "missing-empty"},
            )
            self.assertEqual(status, 200)
            empty_committed = self.state_preimages()
            status, replay = self.post_task_action(
                base,
                "w1-ex1",
                "done",
                {"operation_id": "missing-empty", "note": "", "evidence_path": ""},
            )
            self.assertEqual(status, 200)
            self.assertEqual(replay["result"], "replayed_operation")
            self.assertEqual(replay["action_id"], empty_first["action_id"])
            self.assert_preimages(empty_committed)
            self.assertEqual(first["revision"], 1)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)

    def test_http_task_path_rejects_percent_encoded_or_noncanonical_ids_without_mutation(self) -> None:
        server, thread, base = self.start_http_server()
        try:
            before = self.state_preimages()
            for task_path in ("%77%31-read", "w1%2Dread", "w1-read%2Fextra"):
                with self.subTest(task_path=task_path):
                    status, _payload = self.post_task_action(
                        base,
                        task_path,
                        "done",
                        {"operation_id": f"encoded-{len(task_path)}"},
                    )
                    self.assertIn(status, {400, 404})
                    self.assert_preimages(before)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()

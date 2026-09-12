from __future__ import annotations

import json
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import UUID

from playwright.sync_api import Browser, Page, sync_playwright

from tests.ui.fixture_server import FixtureServer


class TaskActionRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.playwright = sync_playwright().start()
        cls.browser: Browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self) -> None:
        self.contexts = []

    def tearDown(self) -> None:
        for context in reversed(self.contexts):
            context.close()

    def open_page(
        self,
        fixture: FixtureServer,
        *,
        viewport: dict[str, int] | None = None,
        task_id: str = "w1-read",
    ) -> tuple[Page, list[str]]:
        context = self.browser.new_context(viewport=viewport or {"width": 1280, "height": 900})
        self.contexts.append(context)
        page = context.new_page()
        runtime_errors: list[str] = []
        page.on("console", lambda message: runtime_errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: runtime_errors.append(str(error)))
        page.on(
            "requestfailed",
            lambda request: runtime_errors.append(f"requestfailed: {request.url} ({request.failure})")
            if "aborted" not in str(request.failure or "").lower()
            else None,
        )
        page.goto(f"{fixture.url}/progress.html?task={task_id}#learn", wait_until="domcontentloaded")
        page.wait_for_function(
            """() => document.body.dataset.activeView === 'learn'
              && typeof learningResourceIsVerified === 'function'
              && learningResourceIsVerified('progress')
              && document.querySelector('.task-complete-open:not(:disabled)')"""
        )
        return page, runtime_errors

    def client_state(self, page: Page) -> dict:
        return page.evaluate(
            """() => ({
              progressData: JSON.parse(JSON.stringify(progressData)),
              lanesData: JSON.parse(JSON.stringify(lanesData)),
              feedbackMap: JSON.parse(JSON.stringify(feedbackMap)),
              eventMap: JSON.parse(JSON.stringify(eventMap)),
              progressRevision,
            })"""
        )

    def assert_canonical_action_id(self, value: str) -> None:
        self.assertIsInstance(value, str)
        self.assertEqual(str(UUID(value)), value)

    def open_record(self, page: Page, *, note: str = "完成本节并验证最小命令") -> None:
        page.locator('.task-complete-open[data-task="w1-read"]').first.click()
        page.wait_for_selector('#readerModal.open .record-panel[data-task="w1-read"]')
        page.locator("#recordNote").fill(note)
        page.locator("#recordEvidence").fill("tests/ui/in-memory-evidence")

    def assert_clean_runtime(self, errors: list[str]) -> None:
        self.assertEqual(errors, [])

    def post_action(self, fixture: FixtureServer, task_id: str, action: str, payload: dict) -> dict:
        status, result = self.post_action_result(fixture, task_id, action, payload)
        self.assertEqual(status, 200)
        return result

    def post_action_result(
        self,
        fixture: FixtureServer,
        task_id: str,
        action: str,
        payload: dict,
    ) -> tuple[int, dict]:
        request = Request(
            f"{fixture.url}/api/tasks/{task_id}/{action}",
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

    def post_path_result(self, fixture: FixtureServer, path: str, payload: dict | None = None) -> tuple[int, dict]:
        request = Request(
            f"{fixture.url}{path}",
            data=json.dumps(payload or {}).encode("utf-8"),
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

    def post_run_result(self, fixture: FixtureServer, task_id: str, operation_id: str) -> tuple[int, dict]:
        return self.post_path_result(
            fixture,
            f"/api/tasks/{task_id}/run",
            {"operation_id": operation_id},
        )

    def test_opt_in_fixture_done_and_undo_return_full_memory_state(self) -> None:
        with FixtureServer(task_actions=True) as fixture:
            done = self.post_action(
                fixture,
                "w1-read",
                "done",
                {"operation_id": "fixture-done", "note": "memory only"},
            )
            undo = self.post_action(
                fixture,
                "w1-read",
                "undo",
                {"operation_id": "fixture-undo"},
            )

            self.assertEqual(len(done["tasks"]), 80)
            self.assertTrue(done["done"])
            self.assertEqual(done["revision"], 1)
            self.assertEqual(done["operation_id"], "fixture-done")
            self.assertEqual(done["event"]["action_id"], done["action_id"])
            self.assert_canonical_action_id(done["action_id"])
            self.assertEqual(done["event"]["operation_id"], "fixture-done")
            self.assertEqual(done["event"]["round_id"], "round_00")
            self.assertFalse(undo["done"])
            self.assertEqual(undo["revision"], 2)
            self.assertEqual(undo["operation_id"], "fixture-undo")
            self.assert_canonical_action_id(undo["action_id"])
            self.assertNotEqual(undo["action_id"], done["action_id"])
            self.assertEqual(fixture.state["post_count"], 2)
            self.assertEqual([event["action_type"] for event in fixture.state["events"]], ["mark_done", "undo_done"])

            run_status, run = self.post_run_result(fixture, "w1-ex1", "fixture-run")
            self.assertEqual(run_status, 200)
            self.assertEqual(run["execution"]["event"]["action_id"], run["execution"]["action_id"])
            self.assert_canonical_action_id(run["execution"]["action_id"])
            self.assertNotIn(run["execution"]["action_id"], {done["action_id"], undo["action_id"]})
            self.assertEqual(run["execution"]["operation_id"], "fixture-run")
            self.assertEqual(run["execution"]["event"]["operation_id"], "fixture-run")

    def test_default_fixture_rejects_task_action_without_mutation(self) -> None:
        with FixtureServer() as fixture:
            status, response = self.post_action_result(
                fixture,
                "w1-read",
                "done",
                {"operation_id": "must-not-write"},
            )

            self.assertEqual(status, 405)
            self.assertEqual(response["error"], "fixture_is_read_only")
            self.assertFalse(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(fixture.state["post_count"], 0)
            self.assertEqual(fixture.state["events"], [])
            for path in ("/api/tasks/w1-ex1/run", "/api/saves/fixture-save/load", "/api/sync"):
                status, response = self.post_path_result(fixture, path)
                self.assertEqual(status, 405)
                self.assertEqual(response["error"], "fixture_is_read_only")
            self.assertEqual(fixture.state["run_post_count"], 0)
            self.assertEqual(fixture.state["save_load_post_count"], 0)

    def test_opt_in_fixture_validates_exact_payload_before_any_memory_mutation(self) -> None:
        with FixtureServer(task_actions=True) as fixture:
            initial_tasks = json.loads(json.dumps(fixture.state["tasks"]))
            invalid_requests = [
                ("w1-read", {"operation_id": 123}),
                ("w1-read", {"operation_id": "too-long-note", "note": "x" * 501}),
                ("w1-read", {"operation_id": "too-long-astral", "evidence_path": "\U0001f680" * 501}),
                ("%77%31-read", {"operation_id": "encoded-task"}),
            ]
            for task_id, payload in invalid_requests:
                with self.subTest(task_id=task_id, operation_id=payload["operation_id"]):
                    status, _response = self.post_action_result(fixture, task_id, "done", payload)
                    self.assertIn(status, {400, 405})
                    self.assertEqual(fixture.state["tasks"], initial_tasks)
                    self.assertEqual(fixture.state["revision"], 0)
                    self.assertEqual(fixture.state["events"], [])
                    self.assertEqual(fixture.state["operations"], {})
                    self.assertEqual(fixture.state["post_count"], 0)

            astral_500 = "\U0001f680" * 500
            accepted = self.post_action(
                fixture,
                "w1-read",
                "done",
                {"operation_id": "accepted-astral", "note": astral_500, "evidence_path": astral_500},
            )
            self.assertEqual(accepted["revision"], 1)
            self.assertEqual(fixture.state["events"][0]["note"], astral_500)
            self.assertEqual(fixture.state["events"][0]["evidence_path"], astral_500)

    def test_opt_in_fixture_replay_requires_exact_payload_and_missing_equals_empty(self) -> None:
        with FixtureServer(task_actions=True) as fixture:
            first = self.post_action(
                fixture,
                "w1-read",
                "done",
                {"operation_id": "exact-fingerprint", "note": "x" * 499 + "a"},
            )
            status, conflict = self.post_action_result(
                fixture,
                "w1-read",
                "done",
                {"operation_id": "exact-fingerprint", "note": "x" * 499 + "b"},
            )
            self.assertEqual(status, 400)
            self.assertEqual(conflict["error"], "operation_id_conflict")
            self.assertEqual(fixture.state["revision"], 1)
            self.assertEqual(len(fixture.state["events"]), 1)

            empty = self.post_action(
                fixture,
                "w1-ex1",
                "done",
                {"operation_id": "missing-empty"},
            )
            replay = self.post_action(
                fixture,
                "w1-ex1",
                "done",
                {"operation_id": "missing-empty", "note": "", "evidence_path": ""},
            )
            self.assertEqual(replay["result"], "replayed_operation")
            self.assertEqual(replay["action_id"], empty["action_id"])
            self.assert_canonical_action_id(replay["action_id"])
            self.assertEqual(fixture.state["revision"], 2)
            self.assertEqual(len(fixture.state["events"]), 2)
            self.assertEqual(first["revision"], 1)

    def test_restored_history_rejects_ledger_only_replay_without_ghost_client_commit(self) -> None:
        original_note = "读档前已提交的记录"
        original_evidence = "tests/ui/in-memory-evidence"
        with FixtureServer(
            task_actions=True,
            save_load_plan=[{
                "kind": "restore_uncompleted_history",
                "task_id": "w1-read",
            }],
        ) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note=original_note)
            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")
            original_operation_id = fixture.state["posts"][0]["payload"]["operation_id"]
            self.assertTrue(page.evaluate("progressData['w1-read'].done"))
            self.assertEqual(page.evaluate("progressRevision"), 1)
            self.assertEqual(len(page.evaluate("eventMap['w1-read'] || []")), 1)

            page.locator("#readerClose").click()
            page.wait_for_function("!document.querySelector('#readerModal').classList.contains('open')")
            page.on("dialog", lambda dialog: dialog.accept())
            page.evaluate("async () => { await loadSave('old-save', '旧存档'); }")
            page.wait_for_function(
                "progressRevision === 2 && progressData['w1-read'].done === false"
            )
            page.wait_for_function("(eventMap['w1-read'] || []).length === 0")
            self.assertEqual(page.evaluate("feedbackMap['w1-read'].feedback_type"), "not_started")
            self.assertFalse(page.locator(".completion-receipt").is_visible())
            self.assertEqual(fixture.state["operations"].keys(), {original_operation_id})
            self.assertEqual(fixture.state["events"], [])

            page.evaluate("openRecordViewer('w1-read', { requireNote: true })")
            page.wait_for_selector('#readerModal.open .record-panel[data-task="w1-read"]')
            page.locator("#recordNote").fill(original_note)
            page.locator("#recordEvidence").fill(original_evidence)
            before_replay = self.client_state(page)
            page.evaluate(
                """async ({ operationId, note, evidencePath }) => {
                  await postTaskAction('w1-read', false, {
                    operation_id: operationId,
                    note,
                    evidence_path: evidencePath,
                  });
                }""",
                {
                    "operationId": original_operation_id,
                    "note": original_note,
                    "evidencePath": original_evidence,
                },
            )
            replay_error = page.locator(".record-transaction-status.is-error")
            replay_error.wait_for()

            self.assertIn("operation_event_not_in_current_history", replay_error.inner_text())
            self.assertEqual(self.client_state(page), before_replay)
            self.assertEqual(page.locator("#recordNote").input_value(), original_note)
            self.assertEqual(page.locator("#recordEvidence").input_value(), original_evidence)
            self.assertFalse(page.locator(".completion-receipt").is_visible())
            self.assertFalse(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(fixture.state["revision"], 2)
            self.assertEqual(fixture.state["events"], [])
            self.assertEqual(len(errors), 1)
            self.assertIn("400", errors[0])
            errors.clear()

            page.locator("#recordSaveDone").click()
            page.wait_for_function("progressData['w1-read'].done === true && progressRevision === 3")
            new_operation_id = fixture.state["posts"][-1]["payload"]["operation_id"]
            self.assertNotEqual(new_operation_id, original_operation_id)
            self.assertEqual(fixture.state["posts"][-1]["payload"]["note"], original_note)
            self.assertEqual(fixture.state["posts"][-1]["payload"]["evidence_path"], original_evidence)
            self.assertTrue(page.evaluate("progressData['w1-read'].done"))
            self.assertEqual(page.evaluate("progressRevision"), 3)
            self.assertEqual(len(page.evaluate("eventMap['w1-read'] || []")), 1)
            self.assertEqual(fixture.state["events"][0]["operation_id"], new_operation_id)
            self.assert_clean_runtime(errors)

    def test_opt_in_fixture_concurrent_same_operation_different_payload_commits_once(self) -> None:
        with FixtureServer(task_actions=True, action_plan=[{"kind": "success", "delay": 0.1}]) as fixture:
            barrier = threading.Barrier(2)

            def post(note: str) -> tuple[int, dict]:
                barrier.wait(timeout=2)
                return self.post_action_result(
                    fixture,
                    "w1-read",
                    "done",
                    {"operation_id": "concurrent-conflict", "note": note},
                )

            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(pool.map(post, ["payload-a", "payload-b"]))

            self.assertEqual(sorted(status for status, _payload in results), [200, 400])
            conflict = next(payload for status, payload in results if status == 400)
            self.assertEqual(conflict["error"], "operation_id_conflict")
            self.assertEqual(fixture.state["revision"], 1)
            self.assertEqual(len(fixture.state["events"]), 1)
            self.assertEqual(len(fixture.state["operations"]), 1)

    def test_delayed_save_is_busy_and_duplicate_activation_posts_once(self) -> None:
        with FixtureServer(task_actions=True, action_plan=[{"kind": "success", "delay": 0.45}]) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page)
            page.evaluate(
                """() => {
                  const button = document.querySelector('#recordSaveDone');
                  button.click();
                  button.click();
                }"""
            )
            page.wait_for_function("document.querySelector('#recordSaveDone')?.getAttribute('aria-busy') === 'true'")
            self.assertTrue(page.locator("#recordSaveDone").is_disabled())
            self.assertTrue(page.locator("#recordNote").is_disabled())
            self.assertIn("正在保存本次记录", page.locator(".record-transaction-status").inner_text())
            page.wait_for_selector("#readerModal.open .completion-receipt")

            self.assertEqual(fixture.state["post_count"], 1)
            self.assertEqual(len(fixture.state["posts"]), 1)
            self.assertTrue(fixture.state["posts"][0]["payload"]["operation_id"])
            self.assertEqual(len(fixture.state["tasks"]), 80)
            self.assertTrue(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(fixture.state["revision"], 1)
            self.assert_clean_runtime(errors)

    def test_success_receipt_uses_saved_event_feedback_and_course_count(self) -> None:
        note = "我读完了 week1 笔记，并验证了 pwd。"
        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note=note)
            page.locator("#recordSaveDone").click()
            receipt = page.locator("#readerModal.open .completion-receipt")
            receipt.wait_for()

            self.assertEqual(page.locator("#readerTitle").inner_text(), "任务完成回执")
            self.assertIn(note, receipt.inner_text())
            self.assertIn("tests/ui/in-memory-evidence", receipt.inner_text())
            self.assertIn("1 / 80", receipt.inner_text())
            self.assertIn("隔离测试内存", receipt.inner_text())
            self.assertEqual(len(fixture.state["events"]), 1)
            self.assertEqual(fixture.state["events"][0]["note"], note)
            self.assertEqual(fixture.state["events"][0]["action_type"], "mark_done")
            self.assertEqual(
                fixture.state["events"][0]["operation_id"],
                fixture.state["posts"][0]["payload"]["operation_id"],
            )
            self.assert_clean_runtime(errors)

    def test_note_preserves_exact_whitespace_in_event_and_receipt(self) -> None:
        note = "  exact note  "
        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note=note)
            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")

            self.assertEqual(fixture.state["posts"][0]["payload"]["note"], note)
            self.assertEqual(fixture.state["events"][0]["note"], note)
            self.assertEqual(page.locator(".completion-receipt .receipt-note strong").text_content(), note)
            self.assert_clean_runtime(errors)

    def test_required_whitespace_only_note_never_posts(self) -> None:
        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note=" \t\n ")
            page.locator("#recordSaveDone").click()
            page.wait_for_timeout(150)

            self.assertEqual(page.locator("#recordNote").input_value(), " \t\n ")
            self.assertEqual(fixture.state["post_count"], 0)
            self.assertEqual(fixture.state["revision"], 0)
            self.assert_clean_runtime(errors)

    def test_http_error_is_inline_preserves_inputs_and_can_retry(self) -> None:
        note = "失败后仍应保留的记录"
        with FixtureServer(
            task_actions=True,
            action_plan=[
                {"kind": "http_error", "status": 503, "error": "测试服务暂不可用"},
                {"kind": "success"},
            ],
        ) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note=note)
            page.locator("#recordSaveDone").click()
            status = page.locator(".record-transaction-status.is-error")
            status.wait_for()

            self.assertIn("测试服务暂不可用", status.inner_text())
            self.assertEqual(page.locator("#recordNote").input_value(), note)
            self.assertEqual(page.locator("#recordEvidence").input_value(), "tests/ui/in-memory-evidence")
            self.assertFalse(page.locator("#recordSaveDone").is_disabled())
            self.assertEqual(page.evaluate("document.activeElement.className"), "record-transaction-status is-error")
            self.assertFalse(fixture.state["tasks"]["w1-read"]["done"])

            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")
            self.assertEqual(fixture.state["post_count"], 2)
            self.assertTrue(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(len(errors), 1)
            self.assertIn("503", errors[0])
            errors.clear()
            self.assert_clean_runtime(errors)

    def test_json_null_400_releases_operation_id_for_identical_retry(self) -> None:
        note = "确定性错误后用同一输入正常重试"
        with FixtureServer(
            task_actions=True,
            action_plan=[
                {"kind": "http_error", "status": 400, "response_body": None},
                {"kind": "success"},
            ],
        ) as fixture:
            page, errors = self.open_page(fixture, viewport={"width": 390, "height": 844})
            self.open_record(page, note=note)
            page.locator("#recordSaveDone").click()
            status = page.locator(".record-transaction-status.is-error")
            status.wait_for()

            self.assertIn("HTTP 400", status.inner_text())
            self.assertEqual(page.locator("#recordNote").input_value(), note)
            self.assertEqual(page.locator("#recordEvidence").input_value(), "tests/ui/in-memory-evidence")
            self.assertEqual(fixture.state["revision"], 0)
            self.assertFalse(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(fixture.state["events"], [])
            first_operation_id = fixture.state["posts"][0]["payload"]["operation_id"]
            self.assert_canonical_action_id(first_operation_id)

            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")
            second_operation_id = fixture.state["posts"][1]["payload"]["operation_id"]
            self.assert_canonical_action_id(second_operation_id)
            self.assertNotEqual(second_operation_id, first_operation_id)
            self.assertEqual(fixture.state["posts"][1]["payload"]["note"], note)
            self.assertEqual(fixture.state["posts"][1]["payload"]["evidence_path"], "tests/ui/in-memory-evidence")
            self.assertEqual(fixture.state["revision"], 1)
            self.assertTrue(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(len(fixture.state["events"]), 1)
            self.assertEqual(fixture.state["events"][0]["operation_id"], second_operation_id)
            self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
            self.assertEqual(len(errors), 1)
            self.assertIn("400", errors[0])
            errors.clear()
            self.assert_clean_runtime(errors)

    def test_timeout_is_inline_preserves_inputs_and_does_not_mutate(self) -> None:
        note = "超时后仍应保留的记录"
        with FixtureServer(
            task_actions=True,
            action_plan=[{"kind": "timeout", "delay": 0.35}],
        ) as fixture:
            page, errors = self.open_page(fixture)
            page.evaluate(
                """() => {
                  const original = fetchTaskAction;
                  fetchTaskAction = (resource, options) => original(resource, options, 120);
                }"""
            )
            self.open_record(page, note=note)
            page.locator("#recordSaveDone").click()
            status = page.locator(".record-transaction-status.is-error")
            status.wait_for()

            self.assertIn("保存超时", status.inner_text())
            self.assertEqual(page.locator("#recordNote").input_value(), note)
            self.assertFalse(page.locator("#recordSaveDone").is_disabled())
            self.assertFalse(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(fixture.state["events"], [])
            self.assertEqual(fixture.state["post_count"], 1)
            self.assert_clean_runtime(errors)

    def test_closing_modal_before_late_success_does_not_reopen_or_steal_focus(self) -> None:
        with FixtureServer(task_actions=True, action_plan=[{"kind": "success", "delay": 0.45}]) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page)
            page.locator("#recordSaveDone").click()
            page.wait_for_function("document.querySelector('#recordSaveDone')?.disabled")
            page.locator("#readerClose").click()
            page.wait_for_function("!document.querySelector('#readerModal').classList.contains('open')")
            page.wait_for_function("progressData?.['w1-read']?.done === true")
            page.wait_for_timeout(150)

            self.assertFalse(page.locator("#readerModal").evaluate("element => element.classList.contains('open')"))
            self.assertEqual(page.evaluate("document.activeElement?.dataset?.task"), "w1-read")
            self.assertFalse(page.evaluate("document.querySelector('#readerModal').contains(document.activeElement)"))
            self.assertEqual(fixture.state["post_count"], 1)
            self.assertTrue(fixture.state["tasks"]["w1-read"]["done"])
            self.assert_clean_runtime(errors)

    def test_retry_operation_id_is_reused_only_for_identical_payload(self) -> None:
        with FixtureServer(
            task_actions=True,
            action_plan=[
                {"kind": "http_error", "status": 503, "error": "first error"},
                {"kind": "http_error", "status": 503, "error": "second error"},
                {"kind": "success"},
            ],
        ) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note="same payload")
            page.locator("#recordSaveDone").click()
            page.locator(".record-transaction-status.is-error").wait_for()
            first_id = fixture.state["posts"][0]["payload"]["operation_id"]

            page.locator("#recordSaveDone").click()
            page.wait_for_function("() => document.querySelector('.record-transaction-status.is-error')?.textContent.includes('second error')")
            second_id = fixture.state["posts"][1]["payload"]["operation_id"]
            self.assertEqual(second_id, first_id)

            page.locator("#recordNote").fill("changed payload")
            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")
            third_id = fixture.state["posts"][2]["payload"]["operation_id"]
            self.assertNotEqual(third_id, first_id)
            self.assertEqual(fixture.state["events"][0]["note"], "changed payload")
            self.assertEqual(len(errors), 2)

    def test_close_reopen_same_task_late_success_reconciles_and_preserves_new_input(self) -> None:
        with FixtureServer(task_actions=True, action_plan=[{"kind": "success", "delay": 0.45}]) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note="first submitted note")
            page.locator("#recordSaveDone").click()
            page.locator("#readerClose").click()
            page.evaluate("openRecordViewer('w1-read', { requireNote: true })")
            page.wait_for_selector('#readerModal.open .record-panel[data-task="w1-read"]')
            page.locator("#recordNote").fill("new unsaved note")
            page.wait_for_function("progressData?.['w1-read']?.done === true")
            page.wait_for_function("() => document.querySelector('.record-transaction-status.is-synced')")

            self.assertIn("当前状态：已完成", page.locator(".record-status").inner_text())
            self.assertEqual(page.locator("#recordNote").input_value(), "new unsaved note")
            self.assertIn("当前输入尚未再次提交", page.locator(".record-transaction-status.is-synced").inner_text())
            self.assertEqual(fixture.state["post_count"], 1)
            self.assert_clean_runtime(errors)

    def test_malformed_action_response_never_partially_commits_client_and_replay_recovers(self) -> None:
        def mutation(name: str):
            def mutate(payload: dict) -> None:
                if name == "done_type":
                    payload["done"] = "false"
                elif name == "lanes_shape":
                    payload["lanes"] = []
                elif name == "task_lane":
                    payload["tasks"]["w1-read"]["lane"] = "other-course"
                elif name == "top_lane":
                    payload["lane"] = "other-course"
                elif name == "top_message":
                    payload["message"] = 1
                elif name == "message_exact":
                    payload["message"] = "done:w1-read"
                elif name == "event_missing":
                    payload.pop("event")
                elif name == "event_shape":
                    payload["event"] = []
                elif name == "event_action_id_missing":
                    payload["event"]["action_id"] = ""
                elif name == "action_id_coordinated_non_uuid":
                    payload["action_id"] = "coordinated-not-a-uuid"
                    payload["event"]["action_id"] = "coordinated-not-a-uuid"
                elif name == "event_action_id_mismatch":
                    payload["event"]["action_id"] = "fixture-action-other"
                elif name == "event_task_id_type":
                    payload["event"]["task_id"] = 1
                elif name == "event_task_id_value":
                    payload["event"]["task_id"] = "w1-ex1"
                elif name == "event_action_type_type":
                    payload["event"]["action_type"] = 1
                elif name == "event_action_type_value":
                    payload["event"]["action_type"] = "undo_done"
                elif name == "event_result_type":
                    payload["event"]["result"] = 1
                elif name == "event_result_value":
                    payload["event"]["result"] = "failed"
                elif name == "event_lane_type":
                    payload["event"]["lane"] = 1
                elif name == "event_lane_value":
                    payload["event"]["lane"] = "other-course"
                elif name == "event_operation_id_type":
                    payload["event"]["operation_id"] = 1
                elif name == "event_operation_id_value":
                    payload["event"]["operation_id"] = "other-operation"
                elif name == "event_note_type":
                    payload["event"]["note"] = 1
                elif name == "event_note_value":
                    payload["event"]["note"] = "different note"
                elif name == "event_evidence_type":
                    payload["event"]["evidence_path"] = []
                elif name == "event_evidence_value":
                    payload["event"]["evidence_path"] = "different/evidence"
                elif name == "event_timestamp_type":
                    payload["event"]["timestamp"] = 1
                elif name == "event_timestamp_value":
                    payload["event"]["timestamp"] = "not-a-timestamp"
                elif name == "event_round_id_type":
                    payload["event"]["round_id"] = 1
                elif name == "event_round_id_value":
                    payload["event"]["round_id"] = "round-02"
                elif name == "done_at_type":
                    payload["done_at"] = 1
                elif name == "done_at_mismatch":
                    payload["done_at"] = "fixture-other-completion"
                elif name == "done_at_null_while_done":
                    payload["done_at"] = None
                    payload["tasks"]["w1-read"]["done_at"] = None
                elif name == "done_result_opposite_direction":
                    payload["result"] = "noop_already_undone"
                elif name == "other_task_done_false_with_done_at":
                    payload["tasks"]["w1-ex1"]["done_at"] = "fixture-forged-completion"
                elif name == "other_task_done_true_without_done_at":
                    payload["tasks"]["w1-ex1"].update(done=True, done_at=None)
                elif name == "feedback_shape":
                    payload["feedback"] = []
                elif name == "feedback_missing":
                    payload["feedback"].pop("w1-ex1")
                elif name == "feedback_extra":
                    payload["feedback"]["not-registered"] = dict(payload["feedback"]["w1-read"])
                elif name == "feedback_task_id":
                    payload["feedback"]["w1-read"]["task_id"] = "w1-ex1"
                elif name == "feedback_lane":
                    payload["feedback"]["w1-read"]["lane"] = "other-course"
                elif name == "feedback_done":
                    payload["feedback"]["w1-read"]["done"] = False
                elif name == "action_count_unsafe":
                    payload["feedback"]["w1-read"]["action_count"] = 9_007_199_254_740_992
                elif name == "action_count_negative":
                    payload["feedback"]["w1-read"]["action_count"] = -1
                elif name == "last_action_type":
                    payload["feedback"]["w1-read"]["last_action_type"] = 1
                elif name == "last_action_at":
                    payload["feedback"]["w1-read"]["last_action_at"] = 1
                elif name == "feedback_type":
                    payload["feedback"]["w1-read"]["feedback_type"] = "invented"
                elif name == "feedback_message":
                    payload["feedback"]["w1-read"]["message"] = 1
                elif name == "next_suggestion":
                    payload["feedback"]["w1-read"]["next_suggestion"] = []
            return mutate

        cases = [
            "done_type", "lanes_shape", "task_lane", "top_lane", "top_message", "message_exact",
            "event_missing", "event_shape", "event_action_id_missing",
            "action_id_coordinated_non_uuid", "event_action_id_mismatch",
            "event_task_id_type", "event_task_id_value", "event_action_type_type",
            "event_action_type_value", "event_result_type", "event_result_value",
            "event_lane_type", "event_lane_value", "event_operation_id_type",
            "event_operation_id_value", "event_note_type", "event_note_value",
            "event_evidence_type", "event_evidence_value", "event_timestamp_type",
            "event_timestamp_value", "event_round_id_type", "event_round_id_value", "done_at_type",
            "done_at_mismatch", "done_at_null_while_done", "done_result_opposite_direction",
            "other_task_done_false_with_done_at", "other_task_done_true_without_done_at",
            "feedback_shape", "feedback_missing",
            "feedback_extra", "feedback_task_id", "feedback_lane", "feedback_done",
            "action_count_unsafe", "action_count_negative", "last_action_type", "last_action_at",
            "feedback_type", "feedback_message", "next_suggestion",
        ]
        for case in cases:
            with self.subTest(case=case):
                with FixtureServer(
                    task_actions=True,
                    action_plan=[{"kind": "success", "response_mutator": mutation(case)}],
                ) as fixture:
                    page, errors = self.open_page(fixture)
                    note = f"malformed response {case}"
                    self.open_record(page, note=note)
                    before = self.client_state(page)
                    page.locator("#recordSaveDone").click()
                    status = page.locator(".record-transaction-status.is-error")
                    status.wait_for()

                    self.assertTrue(fixture.state["tasks"]["w1-read"]["done"])
                    self.assertEqual(fixture.state["revision"], 1)
                    self.assertEqual(self.client_state(page), before)
                    self.assertIn("0 / 80", page.locator("#learnHeaderProgress").inner_text())
                    self.assertEqual(page.locator("#recordNote").input_value(), note)
                    self.assertEqual(page.locator("#recordEvidence").input_value(), "tests/ui/in-memory-evidence")
                    self.assertFalse(page.locator(".completion-receipt").is_visible())

                    page.locator("#recordSaveDone").click()
                    page.wait_for_selector("#readerModal.open .completion-receipt")
                    self.assertEqual(page.evaluate("progressData['w1-read'].done"), True)
                    self.assertEqual(page.evaluate("progressRevision"), 1)
                    self.assertIn("1 / 80", page.locator("#learnHeaderProgress").inner_text())
                    self.assertEqual(fixture.state["post_count"], 2)
                    self.assertEqual(
                        fixture.state["posts"][0]["payload"]["operation_id"],
                        fixture.state["posts"][1]["payload"]["operation_id"],
                    )
                    self.assertEqual(len(fixture.state["events"]), 1)
                    self.assert_clean_runtime(errors)

    def test_undo_result_for_done_direction_is_rejected_atomically(self) -> None:
        def mutate(payload: dict) -> None:
            payload["result"] = "noop_already_done"

        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note="prepare undo direction")
            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")
            with fixture.state["lock"]:
                fixture.state["action_plan"].append({"kind": "success", "response_mutator": mutate})

            before = self.client_state(page)
            page.locator("#receiptRecord").click()
            page.wait_for_selector('#readerModal.open .record-panel[data-task="w1-read"]')
            page.locator("#recordUndoDone").click()
            status = page.locator(".record-transaction-status.is-error")
            status.wait_for()

            self.assertFalse(fixture.state["tasks"]["w1-read"]["done"])
            self.assertEqual(fixture.state["revision"], 2)
            self.assertEqual(self.client_state(page), before)
            self.assertIn("1 / 80", page.locator("#learnHeaderProgress").inner_text())
            self.assertFalse(page.locator(".completion-receipt").is_visible())
            self.assert_clean_runtime(errors)

    def test_astral_text_limit_accepts_500_and_rejects_501_without_post(self) -> None:
        astral_500 = "\U0001f680" * 499 + " "
        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture)
            self.open_record(page, note=astral_500)
            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")
            self.assertEqual(fixture.state["post_count"], 1)
            self.assertEqual(fixture.state["posts"][0]["payload"]["note"], astral_500)
            self.assertEqual(fixture.state["events"][0]["note"], astral_500)
            self.assert_clean_runtime(errors)

        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture)
            astral_501 = "\U0001f680" * 500 + " "
            self.open_record(page, note=astral_501)
            page.locator("#recordSaveDone").click()
            status = page.locator(".record-transaction-status.is-error")
            status.wait_for()
            self.assertIn("不能超过 500 个字符", status.inner_text())
            self.assertEqual(page.locator("#recordNote").input_value(), astral_501)
            self.assertEqual(fixture.state["post_count"], 0)
            self.assertEqual(fixture.state["revision"], 0)
            self.assertEqual(fixture.state["events"], [])
            self.assertEqual(page.evaluate("document.activeElement.className"), "record-transaction-status is-error")
            self.assert_clean_runtime(errors)

    def test_run_operation_commits_once_and_same_id_replays_current_snapshot(self) -> None:
        with FixtureServer(task_actions=True) as fixture:
            first_status, first = self.post_run_result(fixture, "w1-ex1", "run-once")
            replay_status, replay = self.post_run_result(fixture, "w1-ex1", "run-once")

            self.assertEqual((first_status, replay_status), (200, 200))
            self.assertFalse(first["execution"]["replayed_operation"])
            self.assertTrue(replay["execution"]["replayed_operation"])
            self.assertEqual(replay["execution"]["action_id"], first["execution"]["action_id"])
            self.assertEqual(replay["execution"]["event"], first["execution"]["event"])
            self.assertEqual(replay["execution"]["operation_id"], "run-once")
            self.assertEqual(fixture.state["revision"], 1)
            self.assertEqual(len(fixture.state["events"]), 1)
            self.assertEqual(len(fixture.state["run_operations"]), 1)
            self.assertEqual(fixture.state["run_post_count"], 2)
            self.assertEqual(fixture.state["run_execution_count"], 1)
            self.assertTrue(fixture.state["tasks"]["w1-ex1"]["done"])

            conflict_status, conflict = self.post_run_result(fixture, "w2-ex4", "run-once")
            self.assertEqual(conflict_status, 400)
            self.assertEqual(conflict["error"], "operation_id_conflict")
            self.assertEqual(fixture.state["revision"], 1)
            self.assertEqual(len(fixture.state["events"]), 1)

    def test_run_fixture_rejects_non_exact_payload_before_any_memory_mutation(self) -> None:
        invalid_payloads = (
            {},
            {"operation_id": 123},
            {"operation_id": ""},
            {"operation_id": "bad operation"},
            {"operation_id": "has-extra", "extra": True},
        )
        with FixtureServer(task_actions=True) as fixture:
            for payload in invalid_payloads:
                with self.subTest(payload=payload):
                    status, _response = self.post_path_result(
                        fixture,
                        "/api/tasks/w1-ex1/run",
                        payload,
                    )
                    self.assertEqual(status, 400)
                    self.assertEqual(fixture.state["revision"], 0)
                    self.assertEqual(fixture.state["events"], [])
                    self.assertEqual(fixture.state["run_operations"], {})
                    self.assertEqual(fixture.state["run_post_count"], 0)
                    self.assertEqual(fixture.state["run_execution_count"], 0)

    def test_run_5xx_reuses_operation_id_but_deterministic_4xx_releases_it(self) -> None:
        with FixtureServer(
            task_actions=True,
            run_plan=[
                {"kind": "http_error", "status": 503, "error": "run unavailable"},
                {"kind": "success"},
            ],
        ) as fixture:
            page, errors = self.open_page(fixture, task_id="w1-ex1")
            page.on("dialog", lambda dialog: dialog.accept())
            page.evaluate("postTaskRun('w1-ex1')")
            page.wait_for_function("!taskRunPending('w1-ex1')")
            self.assertFalse(page.evaluate("progressData['w1-ex1'].done"))
            self.assertEqual(fixture.state["revision"], 0)

            page.evaluate("postTaskRun('w1-ex1')")
            page.wait_for_function("!taskRunPending('w1-ex1')")
            self.assertTrue(page.evaluate("progressData['w1-ex1'].done"))
            self.assertEqual(fixture.state["revision"], 1)
            self.assertEqual(len(fixture.state["events"]), 1)
            self.assertEqual(
                fixture.state["run_posts"][0]["payload"]["operation_id"],
                fixture.state["run_posts"][1]["payload"]["operation_id"],
            )
            self.assertEqual(len(errors), 1)
            self.assertIn("503", errors[0])
            errors.clear()
            self.assert_clean_runtime(errors)

        with FixtureServer(
            task_actions=True,
            run_plan=[
                {"kind": "http_error", "status": 400, "response_body": None},
                {"kind": "success"},
            ],
        ) as fixture:
            page, errors = self.open_page(fixture, task_id="w1-ex1")
            page.on("dialog", lambda dialog: dialog.accept())
            page.evaluate("postTaskRun('w1-ex1')")
            page.wait_for_function("!taskRunPending('w1-ex1')")
            self.assertEqual(fixture.state["revision"], 0)

            page.evaluate("postTaskRun('w1-ex1')")
            page.wait_for_function("!taskRunPending('w1-ex1')")
            first_id = fixture.state["run_posts"][0]["payload"]["operation_id"]
            second_id = fixture.state["run_posts"][1]["payload"]["operation_id"]
            self.assertNotEqual(first_id, second_id)
            self.assertEqual(fixture.state["events"][0]["operation_id"], second_id)
            self.assertTrue(page.evaluate("progressData['w1-ex1'].done"))
            self.assertEqual(fixture.state["revision"], 1)
            self.assertEqual(len(errors), 1)
            self.assertIn("400", errors[0])
            errors.clear()
            self.assert_clean_runtime(errors)

    def test_run_failure_timeout_and_missing_verification_never_fake_completion(self) -> None:
        cases = (
            ({"kind": "failed", "stderr": "fixture failed"}, "failed", False),
            ({"kind": "timeout", "stderr": "fixture timed out"}, "timeout", False),
            ({"kind": "success", "verification_reached": False}, "ok", False),
        )
        for plan, expected_result, expected_verification in cases:
            with self.subTest(result=expected_result, verification=expected_verification):
                with FixtureServer(task_actions=True, run_plan=[plan]) as fixture:
                    page, errors = self.open_page(fixture, task_id="w1-ex1")
                    page.on("dialog", lambda dialog: dialog.accept())
                    page.evaluate("postTaskRun('w1-ex1')")
                    page.wait_for_function("!taskRunPending('w1-ex1')")
                    page.locator("#readerModal.open .feedback-result").wait_for()

                    execution = fixture.state["run_operations"][
                        fixture.state["run_posts"][0]["payload"]["operation_id"]
                    ]["execution"]
                    self.assertEqual(execution["result"], expected_result)
                    self.assertEqual(execution["verification_reached"], expected_verification)
                    self.assertFalse(execution["completion_applied"])
                    self.assertFalse(fixture.state["tasks"]["w1-ex1"]["done"])
                    self.assertFalse(page.evaluate("progressData['w1-ex1'].done"))
                    self.assertEqual(page.evaluate("progressRevision"), 1)
                    self.assertEqual(fixture.state["revision"], 1)
                    self.assertEqual(len(fixture.state["events"]), 1)
                    self.assertFalse(page.locator(".completion-receipt").is_visible())
                    self.assert_clean_runtime(errors)

    def test_delayed_run_commits_without_reopening_stale_presentation_context(self) -> None:
        cases = ("home", "other_task")
        for destination in cases:
            with self.subTest(destination=destination):
                with FixtureServer(
                    task_actions=True,
                    run_plan=[{"kind": "success", "delay": 0.45}],
                ) as fixture:
                    page, errors = self.open_page(fixture, task_id="w1-ex1")
                    page.on("dialog", lambda dialog: dialog.accept())
                    page.locator('.task-run[data-task="w1-ex1"]').first.click()
                    page.wait_for_function("taskRunPending('w1-ex1') !== null")

                    if destination == "home":
                        page.evaluate("showView('home', { updateHash: true, focus: true })")
                        page.wait_for_function("document.body.dataset.activeView === 'home'")
                    else:
                        page.evaluate("continueToLearningTask('w1-ex2')")
                        page.wait_for_function(
                            "document.body.dataset.activeView === 'learn' && workspaceTaskId === 'w1-ex2'"
                        )

                    page.wait_for_function("!taskRunPending('w1-ex1')")
                    self.assertTrue(fixture.state["tasks"]["w1-ex1"]["done"])
                    self.assertEqual(fixture.state["revision"], 1)
                    self.assertEqual(len(fixture.state["events"]), 1)
                    self.assertTrue(page.evaluate("progressData['w1-ex1'].done"))
                    self.assertEqual(page.evaluate("progressRevision"), 1)
                    self.assertEqual(page.evaluate("(eventMap['w1-ex1'] || []).length"), 1)
                    self.assertFalse(page.locator("#readerModal").evaluate("element => element.classList.contains('open')"))
                    self.assertEqual(
                        page.evaluate("document.body.dataset.activeView"),
                        "home" if destination == "home" else "learn",
                    )
                    if destination == "other_task":
                        self.assertEqual(page.evaluate("workspaceTaskId"), "w1-ex2")
                        self.assertIn("task=w1-ex2", page.url)
                    self.assert_clean_runtime(errors)

    def test_restored_history_rejects_run_ledger_ghost_replay(self) -> None:
        with FixtureServer(
            task_actions=True,
            save_load_plan=[{"kind": "restore_uncompleted_history", "task_id": "w1-ex1"}],
        ) as fixture:
            first_status, first = self.post_run_result(fixture, "w1-ex1", "run-before-restore")
            save_status, _save = self.post_path_result(fixture, "/api/saves/old-save/load")
            replay_status, replay = self.post_run_result(fixture, "w1-ex1", "run-before-restore")

            self.assertEqual(first_status, 200)
            self.assertEqual(save_status, 200)
            self.assertEqual(replay_status, 400)
            self.assertEqual(replay["error"], "run_operation_event_not_in_current_history")
            self.assertEqual(fixture.state["revision"], 2)
            self.assertFalse(fixture.state["tasks"]["w1-ex1"]["done"])
            self.assertEqual(fixture.state["events"], [])
            self.assertEqual(len(fixture.state["run_operations"]), 1)
            self.assertEqual(first["execution"]["operation_id"], "run-before-restore")

    def test_malformed_run_response_is_atomic_and_canonical_memory_run_succeeds(self) -> None:
        def mutation(name: str):
            def mutate(payload: dict) -> None:
                if name == "revision_string":
                    payload["revision"] = "1"
                elif name == "revision_negative":
                    payload["revision"] = -1
                elif name == "lanes":
                    payload["lanes"] = []
                elif name == "task_lane":
                    payload["tasks"]["w1-ex1"]["lane"] = "other-course"
                elif name == "feedback":
                    payload["feedback"].pop("w1-read")
                elif name == "other_task_done_false_with_done_at":
                    payload["tasks"]["w1-read"]["done_at"] = "fixture-forged-completion"
                elif name == "other_task_done_true_without_done_at":
                    payload["tasks"]["w1-read"].update(done=True, done_at=None)
                elif name == "ok_nonzero":
                    payload["execution"]["returncode"] = 1
                elif name == "ok_timed_out":
                    payload["execution"]["timed_out"] = True
                elif name == "failed_zero":
                    payload["execution"].update(result="failed", execution_ok=False, returncode=0)
                elif name == "failed_timed_out":
                    payload["execution"].update(
                        result="failed", execution_ok=False, timed_out=True, returncode=1
                    )
                elif name == "timeout_returncode":
                    payload["execution"].update(
                        result="timeout", execution_ok=False, timed_out=True, returncode=124
                    )
                elif name == "timeout_not_timed_out":
                    payload["execution"].update(
                        result="timeout", execution_ok=False, timed_out=False, returncode=None
                    )
                elif name == "event_missing":
                    payload["execution"].pop("event")
                elif name == "event_shape":
                    payload["execution"]["event"] = []
                elif name == "event_action_id":
                    payload["execution"]["event"]["action_id"] = "fixture-run-other"
                elif name == "action_id_coordinated_non_uuid":
                    payload["execution"]["action_id"] = "coordinated-not-a-uuid"
                    payload["execution"]["event"]["action_id"] = "coordinated-not-a-uuid"
                elif name == "event_task_id":
                    payload["execution"]["event"]["task_id"] = "w1-read"
                elif name == "event_round_id":
                    payload["execution"]["event"]["round_id"] = "round-02"
                elif name == "event_lane":
                    payload["execution"]["event"]["lane"] = "other-course"
                elif name == "event_action_type":
                    payload["execution"]["event"]["action_type"] = "mark_done"
                elif name == "event_result":
                    payload["execution"]["event"]["result"] = "failed"
                elif name == "event_note":
                    payload["execution"]["event"]["note"] = 1
                elif name == "event_evidence":
                    payload["execution"]["event"]["evidence_path"] = 1
                elif name == "event_timestamp":
                    payload["execution"]["event"]["timestamp"] = "not-a-timestamp"
                elif name == "event_operation_id":
                    payload["execution"]["event"]["operation_id"] = "wrong-operation"
                elif name == "event_details":
                    payload["execution"]["event"]["details"]["returncode"] = 1
                elif name == "execution_operation_id":
                    payload["execution"]["operation_id"] = "wrong-operation"
                elif name == "replayed_operation_type":
                    payload["execution"]["replayed_operation"] = "false"
                elif name == "verification_reached_type":
                    payload["execution"]["verification_reached"] = 1
                elif name == "completion_without_verification":
                    payload["execution"]["verification_reached"] = False
                elif name == "event_verification_mismatch":
                    payload["execution"]["event"]["details"]["verification_reached"] = False
                elif name == "event_completion_mismatch":
                    payload["execution"]["event"]["details"]["completion_applied"] = False
            return mutate

        cases = (
            "revision_string", "revision_negative", "lanes", "task_lane", "feedback",
            "other_task_done_false_with_done_at", "other_task_done_true_without_done_at",
            "ok_nonzero", "ok_timed_out", "failed_zero", "failed_timed_out",
            "timeout_returncode", "timeout_not_timed_out",
            "event_missing", "event_shape", "event_action_id",
            "action_id_coordinated_non_uuid", "event_task_id",
            "event_round_id", "event_lane", "event_action_type", "event_result",
            "event_note", "event_evidence", "event_timestamp", "event_operation_id",
            "event_details", "execution_operation_id", "replayed_operation_type",
            "verification_reached_type", "completion_without_verification",
            "event_verification_mismatch", "event_completion_mismatch",
        )
        for case in cases:
            with self.subTest(case=case):
                with FixtureServer(
                    task_actions=True,
                    run_plan=[{"kind": "success", "response_mutator": mutation(case)}],
                ) as fixture:
                    page, errors = self.open_page(fixture, task_id="w1-ex1")
                    before = self.client_state(page)
                    page.on("dialog", lambda dialog: dialog.accept())
                    page.evaluate("postTaskRun('w1-ex1')")
                    page.wait_for_function("!taskRunPending('w1-ex1')")

                    self.assertTrue(fixture.state["tasks"]["w1-ex1"]["done"])
                    self.assertEqual(fixture.state["revision"], 1)
                    self.assertEqual(self.client_state(page), before)
                    self.assertFalse(page.locator(".completion-receipt").is_visible())
                    result = page.locator("#readerModal.open .feedback-result")
                    result.wait_for()
                    self.assertNotIn("FINISHED", result.inner_text())

                    page.evaluate("postTaskRun('w1-ex1')")
                    page.wait_for_function("!taskRunPending('w1-ex1')")
                    recovered = page.locator("#readerModal.open .feedback-result")
                    recovered.wait_for()
                    self.assertIn("FINISHED", recovered.inner_text())
                    self.assertTrue(page.evaluate("progressData['w1-ex1'].done"))
                    self.assertEqual(page.evaluate("progressRevision"), 1)
                    self.assertEqual(fixture.state["run_post_count"], 2)
                    self.assertEqual(len(fixture.state["events"]), 1)
                    self.assertEqual(len(fixture.state["run_operations"]), 1)
                    self.assertEqual(
                        fixture.state["run_posts"][0]["payload"]["operation_id"],
                        fixture.state["run_posts"][1]["payload"]["operation_id"],
                    )
                    self.assert_clean_runtime(errors)

        with FixtureServer(task_actions=True, run_plan=[{"kind": "success"}]) as fixture:
            page, errors = self.open_page(fixture, task_id="w1-ex1")
            page.on("dialog", lambda dialog: dialog.accept())
            page.locator('.task-run[data-task="w1-ex1"]').first.click()
            page.wait_for_function("!taskRunPending('w1-ex1')")
            result = page.locator("#readerModal.open .feedback-result")
            result.wait_for()

            self.assertEqual(fixture.state["run_post_count"], 1)
            self.assertTrue(page.evaluate("progressData['w1-ex1'].done"))
            self.assertEqual(page.evaluate("progressRevision"), 1)
            self.assert_canonical_action_id(fixture.state["events"][0]["action_id"])
            operation_id = fixture.state["run_posts"][0]["payload"]["operation_id"]
            self.assertEqual(fixture.state["events"][0]["operation_id"], operation_id)
            self.assertTrue(fixture.state["events"][0]["details"]["verification_reached"])
            self.assertTrue(fixture.state["events"][0]["details"]["completion_applied"])
            self.assertIn("FINISHED", result.inner_text())
            self.assertIn("fixture run completed", result.inner_text())
            self.assert_clean_runtime(errors)

    def test_malformed_progress_snapshot_preserves_verified_client_state(self) -> None:
        def mutation(name: str):
            def mutate(payload: dict) -> None:
                if name == "revision_string":
                    payload["revision"] = "1"
                elif name == "revision_negative":
                    payload["revision"] = -1
                elif name == "lanes":
                    payload["lanes"] = []
                elif name == "task_lane":
                    payload["tasks"]["w1-read"]["lane"] = "other-course"
                elif name == "other_task_done_false_with_done_at":
                    payload["tasks"]["w1-ex1"]["done_at"] = "fixture-forged-completion"
                elif name == "other_task_done_true_without_done_at":
                    payload["tasks"]["w1-ex1"].update(done=True, done_at=None)
            return mutate

        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture)
            with fixture.state["lock"]:
                fixture.state["tasks"]["w1-read"]["done"] = True
                fixture.state["tasks"]["w1-read"]["done_at"] = "fixture-verified"
                fixture.state["revision"] = 1
                fixture.state["feedback"] = fixture.state["build_feedback"](
                    fixture.state["tasks"], fixture.state["events"]
                )
            page.evaluate("async () => { await Promise.all([loadProgress(), loadFeedbackData()]); render(); }")
            before = self.client_state(page)
            self.assertTrue(before["progressData"]["w1-read"]["done"])
            self.assertEqual(before["progressRevision"], 1)

            cases = (
                "revision_string", "revision_negative", "lanes", "task_lane",
                "other_task_done_false_with_done_at", "other_task_done_true_without_done_at",
            )
            for case in cases:
                with self.subTest(case=case):
                    with fixture.state["lock"]:
                        fixture.state["progress_plan"].append({"response_mutator": mutation(case)})
                    page.evaluate("async () => { await loadProgress(); render(); }")
                    self.assertEqual(self.client_state(page), before)
            self.assert_clean_runtime(errors)

    def test_malformed_save_snapshot_is_rejected_before_any_client_commit(self) -> None:
        def mutation(name: str):
            def mutate(payload: dict) -> None:
                if name == "task_lane":
                    payload["tasks"]["w1-read"]["lane"] = "other-course"
                elif name == "other_task_done_false_with_done_at":
                    payload["tasks"]["w1-ex1"]["done_at"] = "fixture-forged-completion"
                elif name == "other_task_done_true_without_done_at":
                    payload["tasks"]["w1-ex1"].update(done=True, done_at=None)
            return mutate

        cases = (
            "task_lane", "other_task_done_false_with_done_at", "other_task_done_true_without_done_at",
        )
        for case in cases:
            with self.subTest(case=case):
                with FixtureServer(
                    task_actions=True,
                    save_load_plan=[{"kind": "success", "response_mutator": mutation(case)}],
                ) as fixture:
                    page, errors = self.open_page(fixture)
                    before = self.client_state(page)
                    page.on("dialog", lambda dialog: dialog.accept())
                    page.evaluate(
                        """async () => {
                          loadProgress = async () => true;
                          loadFeedbackData = async () => true;
                          loadEventData = async () => true;
                          await loadSave('fixture-save', '隔离内存存档');
                        }"""
                    )

                    self.assertEqual(fixture.state["save_load_post_count"], 1)
                    self.assertEqual(self.client_state(page), before)
                    self.assertFalse(page.locator(".completion-receipt").is_visible())
                    self.assert_clean_runtime(errors)

    def test_390px_record_and_receipt_have_no_overflow_and_44px_controls(self) -> None:
        with FixtureServer(task_actions=True) as fixture:
            page, errors = self.open_page(fixture, viewport={"width": 390, "height": 844})
            self.open_record(page)
            metrics = page.evaluate(
                """() => ({
                  documentWidth: document.documentElement.scrollWidth,
                  modalWidth: document.querySelector('#readerModal .modal-panel').getBoundingClientRect().width,
                  controls: [...document.querySelectorAll('#readerModal.open input, #readerModal.open textarea, #readerModal.open button')]
                    .filter((element) => element.offsetParent !== null)
                    .map((element) => ({
                      height: element.getBoundingClientRect().height,
                      width: element.getBoundingClientRect().width,
                      selector: `${element.tagName.toLowerCase()}#${element.id}.${element.className}`,
                    })),
                })"""
            )
            self.assertLessEqual(metrics["documentWidth"], 391)
            self.assertLessEqual(metrics["modalWidth"], 390)
            for control in metrics["controls"]:
                self.assertGreaterEqual(control["height"], 43.9, control["selector"])

            page.locator("#recordSaveDone").click()
            page.wait_for_selector("#readerModal.open .completion-receipt")
            receipt_metrics = page.evaluate(
                """() => ({
                  documentWidth: document.documentElement.scrollWidth,
                  panelWidth: document.querySelector('#readerModal .modal-panel').getBoundingClientRect().width,
                  buttons: [...document.querySelectorAll('#readerModal.open button')]
                    .filter((element) => element.offsetParent !== null)
                    .map((element) => element.getBoundingClientRect().height),
                })"""
            )
            self.assertLessEqual(receipt_metrics["documentWidth"], 391)
            self.assertLessEqual(receipt_metrics["panelWidth"], 390)
            for height in receipt_metrics["buttons"]:
                self.assertGreaterEqual(height, 43.9)
            self.assert_clean_runtime(errors)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

from playwright.sync_api import sync_playwright

from tests.ui.problem_fixture import ProblemFixture


class ProblemWorkbenchTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = ProblemFixture().__enter__()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.close(); cls.playwright.stop(); cls.fixture.__exit__(None, None, None)

    def setUp(self):
        with self.fixture.state["lock"]:
            self.fixture.state["requests"].clear(); self.fixture.state["attempts"].clear(); self.fixture.state["sequence"] = 0; self.fixture.state["poll_delays"].clear(); self.fixture.state["response_delays"].clear()
        self.fixture.state.update(wav_enabled=False, wav_prepares=0, wav_plan=[])
        self.contexts = []

    def tearDown(self):
        for context in reversed(self.contexts): context.close()

    def open(self, width=920, path="/?scenario=missing-input"):
        context = self.browser.new_context(viewport={"width": width, "height": 900})
        self.contexts.append(context); page = context.new_page(); errors = []
        page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("requestfailed", lambda request: errors.append(f"failed {request.url}: {request.failure}") if "aborted" not in str(request.failure).lower() else None)
        page.goto(self.fixture.url + path, wait_until="domcontentloaded")
        page.wait_for_selector("#startButton:not([disabled])")
        return page, errors

    def start(self, page):
        page.locator("#startButton").click(); page.wait_for_selector('#attemptStatus[data-status="active"]')
        return page.evaluate("new URL(location.href).searchParams.get('attempt')")

    def test_artifact_controls_do_not_fabricate_fixture_exports(self):
        page, errors = self.open()
        self.start(page)
        self.assertTrue(page.locator("#exportWavButton").is_disabled())
        self.assertTrue(page.locator("#downloadWavButton").is_disabled())
        self.assertFalse([r for r in self.fixture.state["requests"] if "export-wav" in r[1]])
        for path in ("/.git/config", "/docs/pch-rebuild-20261020/.source51-inputs/original-task.json", "/scripts/lab_runtime.py"):
            self.assertEqual(page.request.get(self.fixture.url + path).status, 404)
        self.assertEqual(errors, [])

    def eligible_wav(self):
        self.fixture.state["wav_enabled"] = True
        page, errors = self.open(path="/?scenario=media-wav-quality")
        attempt = self.start(page)
        self.assertTrue(page.locator("#exportWavButton").is_disabled())
        with self.fixture.state["lock"]: self.fixture.state["attempts"][attempt]["fixed"] = True
        page.locator("#checkButton").click(); page.wait_for_selector("#exportWavButton:not([disabled])")
        return page, errors

    def test_wav_loading_transient_error_replays_and_readable_facts(self):
        page, errors = self.eligible_wav()
        self.fixture.state["wav_plan"] = [{"status": 503, "delay": .35}, {}]
        page.locator("#exportWavButton").click()
        page.wait_for_selector('#artifactState[data-status="loading"]')
        self.assertTrue(page.locator("#exportWavButton").is_disabled())
        page.wait_for_selector('#artifactState[data-status="error"]')
        page.wait_for_timeout(800)
        self.assertIn("fixture_transient", page.locator("#artifactState").inner_text())
        page.locator("#exportWavButton").click(); page.wait_for_selector('#artifactState[data-status="success"]')
        posts = [r[2] for r in self.fixture.state["requests"] if r[0] == "POST" and r[1].endswith("/export-wav")]
        self.assertEqual(posts[0], posts[1]); self.assertEqual(self.fixture.state["wav_prepares"], 1)
        facts = page.locator("#artifactProvenance").inner_text()
        for value in ("SHA256", "8044", "16000", "4000", "0.25"): self.assertIn(value, facts)
        self.assertNotIn("internal-", facts); self.assertNotIn("attempt_id", facts)

    def test_wav_known_stale_can_prepare_new_operation_and_reset(self):
        page, errors = self.eligible_wav()
        self.fixture.state["wav_plan"] = [{"status": 409}, {}]
        page.locator("#exportWavButton").click(); page.wait_for_selector('#artifactState[data-status="stale"]')
        page.wait_for_timeout(800); self.assertIn("fixture_stale", page.locator("#artifactState").inner_text())
        page.locator("#checkButton").click(); page.wait_for_selector("#exportWavButton:not([disabled])")
        page.locator("#exportWavButton").click(); page.wait_for_selector("#downloadWavButton:not([disabled])")
        posts = [r[2] for r in self.fixture.state["requests"] if r[0] == "POST" and r[1].endswith("/export-wav")]
        self.assertNotEqual(posts[0]["operation_id"], posts[1]["operation_id"])
        self.assertEqual(self.fixture.state["wav_prepares"], 2)
        page.locator("#downloadWavButton").click(); page.wait_for_selector('#artifactState[data-status="stale"]')
        page.wait_for_timeout(800); self.assertIn("410", page.locator("#artifactState").inner_text())
        page.locator("#resetButton").click(); page.locator("#confirmReset").click()
        page.wait_for_function("() => document.querySelector('#artifactState').dataset.status === 'idle'")
        self.assertTrue(page.locator("#downloadWavButton").is_disabled())
        self.assertTrue(page.locator("#exportWavButton").is_disabled())

    def test_hint_preference_survives_reload_and_other_problem(self):
        page, errors = self.open()
        self.start(page); page.locator("#hintToggle").click(); self.assertEqual(page.locator("#hintToggle").get_attribute("aria-pressed"), "true")
        page.reload(wait_until="domcontentloaded"); page.wait_for_selector('#hintToggle[aria-pressed="true"]'); page.wait_for_selector('#attemptStatus[data-status="active"]')
        previous_attempt = page.evaluate("new URL(location.href).searchParams.get('attempt')")
        page.get_by_role("button", name="包已安装，程序仍说找不到", exact=False).click()
        page.once("dialog", lambda dialog: dialog.accept()); page.locator("#startButton").click()
        page.wait_for_function("oldId => new URL(location.href).searchParams.get('scenario') === 'wrong-python' && new URL(location.href).searchParams.get('attempt') !== oldId && document.querySelector('#labPanel').hidden === false", arg=previous_attempt)
        self.assertTrue(page.locator("#hintsPanel").is_visible()); self.assertGreater(page.locator("#hintSteps li").count(), 0)
        self.assertEqual(errors, [])

    def test_check_failure_never_discloses_solution(self):
        page, errors = self.open(); self.start(page)
        page.locator("#checkButton").click(); page.wait_for_selector("#checksList .fail")
        self.assertTrue(page.locator("#solutionPanel").is_hidden())
        self.assertEqual(page.locator("#solutionButton").get_attribute("aria-expanded"), "false")
        page.locator("#solutionButton").click(); page.wait_for_selector("#solutionPanel:not([hidden])")
        self.assertGreater(page.locator("#solutionSteps li").count(), 0); self.assertEqual(errors, [])

    def test_hints_and_solution_are_readable_before_start_and_recorded_after_start(self):
        page, errors = self.open()
        page.locator("#hintToggle").click(); self.assertTrue(page.locator("#hintsPanel").is_visible())
        page.locator("#solutionButton").click(); self.assertTrue(page.locator("#solutionPanel").is_visible())
        with self.fixture.state["lock"]:
            self.assertFalse([entry for entry in self.fixture.state["requests"] if entry[0] == "POST"])
        attempt_id = self.start(page)
        page.wait_for_function("() => document.querySelector('#solutionPanel').hidden === false")
        with self.fixture.state["lock"]:
            attempt = self.fixture.state["attempts"][attempt_id]
            self.assertTrue(attempt["hints_viewed"]); self.assertTrue(attempt["solution_viewed"])
        self.assertEqual(errors, [])

    def test_reset_new_attempt_keeps_assistance_exposure_truth(self):
        page, errors = self.open(); page.locator("#hintToggle").click(); page.locator("#solutionButton").click()
        old_id = self.start(page)
        page.locator("#resetButton").click(); page.locator("#resetDialog button[value=confirm]").click()
        page.wait_for_function("oldId => new URL(location.href).searchParams.get('attempt') !== oldId", arg=old_id)
        page.wait_for_timeout(80); new_id = page.evaluate("new URL(location.href).searchParams.get('attempt')")
        with self.fixture.state["lock"]:
            attempt = self.fixture.state["attempts"][new_id]
            self.assertTrue(attempt["hints_viewed"]); self.assertTrue(attempt["solution_viewed"])
        self.assertEqual(errors, [])

    def test_unpublished_scenario_cannot_start(self):
        page, errors = self.open()
        page.get_by_role("button", name="等待完整复验的草稿题", exact=False).click()
        self.assertTrue(page.locator("#startButton").is_disabled())
        self.assertEqual(page.locator("#startButton").inner_text(), "等待发布验证")
        self.assertIn("awaiting-revalidation", page.locator("#scenarioMeta").inner_text().lower())
        self.assertEqual(errors, [])

    def test_start_refresh_reconnect_and_lost_state_are_truthful(self):
        page, errors = self.open(); attempt_id = self.start(page)
        page.reload(wait_until="domcontentloaded"); page.wait_for_selector('#attemptStatus[data-status="active"]')
        self.assertEqual(page.evaluate("new URL(location.href).searchParams.get('attempt')"), attempt_id)
        self.fixture.lose(attempt_id); page.locator("#reconnectButton").evaluate("button => { button.disabled = false; button.click(); }")
        page.wait_for_selector('#attemptStatus[data-status="lost"]')
        self.assertIn("不会冒充", page.locator("#terminalTarget").inner_text()); self.assertTrue(page.locator("#checkButton").is_disabled())
        self.assertEqual(errors, [])

    def test_quick_terminal_typing_is_fifo_and_drains_before_check(self):
        page, errors = self.open(); self.start(page)
        page.locator("#terminal").click(); page.keyboard.type("printf fix", delay=0)
        page.locator("#checkButton").click(); page.wait_for_selector("#checksList .pass")
        with self.fixture.state["lock"]:
            actions = [(path.rsplit("/", 1)[-1], payload) for method, path, payload in self.fixture.state["requests"] if method == "POST" and "/attempts/" in path]
        input_index = next(index for index, item in enumerate(actions) if item[0] == "input")
        check_index = next(index for index, item in enumerate(actions) if item[0] == "check")
        self.assertLess(input_index, check_index)
        self.assertEqual("".join(item[1]["data"] for item in actions if item[0] == "input"), "printf fix")
        page.wait_for_function("document.querySelector('#attemptHistory').innerText.includes('最近有效检查通过')")
        self.assertEqual(errors, [])

    def test_old_poll_cannot_replace_new_problem_attempt(self):
        page, errors = self.open(); first = self.start(page)
        with self.fixture.state["lock"]: self.fixture.state["poll_delays"].append(.45)
        page.wait_for_timeout(720)
        page.get_by_role("button", name="包已安装，程序仍说找不到", exact=False).click()
        page.once("dialog", lambda dialog: dialog.accept())
        page.locator("#startButton").click(); page.wait_for_function("new URL(location.href).searchParams.get('scenario') === 'wrong-python'")
        page.wait_for_timeout(600)
        second = page.evaluate("new URL(location.href).searchParams.get('attempt')")
        self.assertNotEqual(first, second); self.assertEqual(page.locator("#problemTitle").inner_text(), "包已安装，程序仍说找不到")
        self.assertEqual(errors, [])

    def test_late_quiet_snapshot_cannot_resurrect_stopped_attempt(self):
        page, errors = self.open(); self.start(page)
        with self.fixture.state["lock"]: self.fixture.state["response_delays"]["view"] = [.35]
        page.locator("#solutionButton").click(); page.locator("#stopButton").click()
        page.wait_for_selector('#attemptStatus[data-status="stopped"]'); page.wait_for_timeout(450)
        self.assertEqual(page.locator("#attemptStatus").get_attribute("data-status"), "stopped")
        self.assertTrue(page.locator("#checkButton").is_disabled()); self.assertEqual(errors, [])

    def test_reload_fast_reset_cancels_old_attempt_resize(self):
        page, errors = self.open(); old_id = self.start(page); page.wait_for_timeout(180)
        with self.fixture.state["lock"]: self.fixture.state["requests"].clear()
        page.reload(wait_until="domcontentloaded"); page.wait_for_selector('#attemptStatus[data-status="active"]')
        page.evaluate("() => { document.querySelector('#resetButton').click(); document.querySelector('#confirmReset').click(); }")
        page.wait_for_function("oldId => new URL(location.href).searchParams.get('attempt') !== oldId", arg=old_id); page.wait_for_timeout(220)
        with self.fixture.state["lock"]:
            requests = list(self.fixture.state["requests"])
        self.assertFalse([path for method, path, _payload in requests if method == "POST" and path == f"/api/lab/attempts/{old_id}/resize"])
        self.assertEqual(errors, [])

    def test_reload_fast_stop_and_new_start_cancel_old_resize(self):
        page, errors = self.open(); old_id = self.start(page); page.wait_for_timeout(180)
        with self.fixture.state["lock"]: self.fixture.state["requests"].clear()
        page.reload(wait_until="domcontentloaded"); page.wait_for_selector('#attemptStatus[data-status="active"]')
        page.locator("#stopButton").click(); page.wait_for_selector('#attemptStatus[data-status="stopped"]'); page.wait_for_timeout(180)
        with self.fixture.state["lock"]:
            stop_requests = list(self.fixture.state["requests"])
            self.fixture.state["requests"].clear()
        self.assertFalse([path for method, path, _payload in stop_requests if method == "POST" and path == f"/api/lab/attempts/{old_id}/resize"])
        page.get_by_role("button", name="包已安装，程序仍说找不到", exact=False).click(); page.locator("#startButton").click()
        page.wait_for_function("() => new URL(location.href).searchParams.get('scenario') === 'wrong-python' && document.querySelector('#attemptStatus').dataset.status === 'active'"); page.wait_for_timeout(180)
        with self.fixture.state["lock"]: new_requests = list(self.fixture.state["requests"])
        self.assertFalse([path for method, path, _payload in new_requests if method == "POST" and path == f"/api/lab/attempts/{old_id}/resize"])
        self.assertEqual(errors, [])

    def test_layout_has_no_horizontal_overflow_and_controls_are_touchable(self):
        page, errors = self.open(width=390)
        for width in (390, 430, 720, 920):
            page.set_viewport_size({"width": width, "height": 900}); page.wait_for_timeout(50)
            self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width + 1)
            for selector in ("#hintToggle", "#startButton", "#refreshHistory"):
                box = page.locator(selector).bounding_box(); self.assertGreaterEqual(box["height"], 43.9)
        self.assertEqual(errors, [])

    def test_api_requests_use_token_and_no_external_network(self):
        page, errors = self.open(); self.start(page); page.locator("#checkButton").click(); page.wait_for_selector("#checksList li")
        origins = page.evaluate("performance.getEntriesByType('resource').map(entry => new URL(entry.name).origin)")
        self.assertEqual(set(origins), {self.fixture.url})
        with self.fixture.state["lock"]:
            posts = [entry for entry in self.fixture.state["requests"] if entry[0] == "POST"]
        self.assertTrue(posts)
        for _method, path, payload in posts:
            if not path.endswith(("/resize", "/view")):
                self.assertTrue(payload.get("operation_id"))
        self.assertEqual(errors, [])

    def test_capture_after_desktop_and_mobile(self):
        page, errors = self.open(width=1440); self.start(page)
        page.screenshot(path="/home/alalapi/Caches/computer-study-plan/refactor-after-desktop.png", full_page=True)
        page.set_viewport_size({"width": 390, "height": 844}); page.wait_for_timeout(80)
        page.screenshot(path="/home/alalapi/Caches/computer-study-plan/refactor-after-mobile.png", full_page=True)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

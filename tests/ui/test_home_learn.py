from __future__ import annotations

import unittest

from playwright.sync_api import Page, sync_playwright

from tests.ui.fixture_server import FixtureServer


class HomeLearnRegressionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = FixtureServer()
        cls.fixture.__enter__()
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.browser.close()
        cls.playwright.stop()
        cls.fixture.__exit__(None, None, None)

    def setUp(self) -> None:
        self.contexts = []
        self.fixture.state["requests"].clear()

    def tearDown(self) -> None:
        for context in reversed(self.contexts):
            context.close()

    def open_page(
        self,
        *,
        viewport: dict[str, int],
        reduced_motion: str = "no-preference",
        fixture: FixtureServer | None = None,
        path: str = "/progress.html",
    ) -> tuple[Page, list[str]]:
        context = self.browser.new_context(viewport=viewport, reduced_motion=reduced_motion)
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
        base = (fixture or self.fixture).url
        page.goto(f"{base}{path}", wait_until="domcontentloaded")
        return page, runtime_errors

    def wait_for_home_task(self, page: Page) -> None:
        page.wait_for_function(
            """() => {
              const card = document.querySelector('#homeTaskCard');
              const action = document.querySelector('.home-primary-action');
              return card?.dataset.learningTaskId === 'w1-read'
                && card.getAttribute('aria-disabled') !== 'true'
                && action && !action.disabled
                && typeof learningResourceIsVerified === 'function'
                && learningResourceIsVerified('progress')
                && !document.querySelector('#refreshBtn')?.disabled;
            }"""
        )

    def assert_no_writes_or_runtime_errors(self, errors: list[str], fixture: FixtureServer | None = None) -> None:
        self.assertEqual(errors, [])
        requests = (fixture or self.fixture).state["requests"]
        writes = [entry for entry in requests if entry[0] != "GET"]
        self.assertEqual(writes, [])

    def test_desktop_home_to_learn_is_one_restorable_navigation(self) -> None:
        page, errors = self.open_page(viewport={"width": 1440, "height": 1024})
        self.wait_for_home_task(page)
        initial_history_length = page.evaluate("history.length")
        transition_supported = page.evaluate("typeof document.startViewTransition === 'function'")
        page.evaluate(
            """() => {
              window.__homeTransitionCalls = 0;
              if (typeof document.startViewTransition !== 'function') return;
              const original = document.startViewTransition.bind(document);
              document.startViewTransition = (callback) => {
                window.__homeTransitionCalls += 1;
                return original(callback);
              };
            }"""
        )

        page.get_by_role("button", name="进入当前任务").click()
        page.wait_for_function("document.body.dataset.activeView === 'learn'")
        self.assertTrue(page.url.endswith("/progress.html?task=w1-read#learn"))
        self.assertEqual(page.evaluate("history.state.taskId"), "w1-read")
        self.assertEqual(page.evaluate("history.length"), initial_history_length + 1)
        self.assertEqual(page.evaluate("document.activeElement.id"), "learnHeading")
        self.assertEqual(page.locator("#continueCard h3").inner_text(), "阅读 week1/notes.md")
        self.assertEqual(page.evaluate("window.__homeTransitionCalls"), 1 if transition_supported else 0)
        self.assertEqual(page.locator("#workspaceTabPractice").get_attribute("hidden"), "")
        self.assertEqual(page.locator("#terminal").get_attribute("aria-hidden"), "true")
        self.assertTrue(page.locator("#terminal").evaluate("element => element.inert"))
        for selector in ("#continueCard", "#inlineReaderPanel"):
            self.assertEqual(page.locator(selector).get_attribute("aria-hidden"), "false")
            self.assertFalse(page.locator(selector).evaluate("element => element.inert"))

        page.wait_for_timeout(650)
        self.assertFalse(page.locator("html").evaluate("element => element.classList.contains('home-task-transition')"))
        self.assertEqual(page.locator("#view-learn").evaluate("element => getComputedStyle(element).animationName"), "none")
        page.evaluate(
            """() => {
              window.__viewMutations = [];
              new MutationObserver(() => window.__viewMutations.push(document.body.dataset.activeView))
                .observe(document.body, {attributes: true, attributeFilter: ['data-active-view']});
            }"""
        )
        page.go_back()
        page.wait_for_function("document.body.dataset.activeView === 'home'")
        self.assertNotIn("task=", page.url)
        page.go_forward()
        page.wait_for_function("document.body.dataset.activeView === 'learn'")
        self.assertTrue(page.url.endswith("/progress.html?task=w1-read#learn"))
        self.assertEqual(page.locator("#continueCard h3").inner_text(), "阅读 week1/notes.md")
        self.assertEqual(page.evaluate("window.__viewMutations"), ["home", "learn"])
        self.assert_no_writes_or_runtime_errors(errors)

    def test_rapid_activation_and_back_during_transition_keep_latest_state(self) -> None:
        page, errors = self.open_page(viewport={"width": 1440, "height": 1024})
        self.wait_for_home_task(page)
        initial_history_length = page.evaluate("history.length")
        page.evaluate(
            """() => {
              const action = document.querySelector('.home-primary-action');
              action.click();
              action.click();
            }"""
        )
        page.wait_for_function("document.body.dataset.activeView === 'learn'")
        self.assertEqual(page.evaluate("history.length"), initial_history_length + 1)
        self.assertTrue(page.url.endswith("?task=w1-read#learn"))

        page.go_back()
        page.wait_for_function("document.body.dataset.activeView === 'home'")
        self.assertNotIn("task=", page.url)
        self.assertEqual(page.locator('.app-view:not([hidden])').get_attribute("data-view"), "home")
        page.go_forward()
        page.wait_for_function("document.body.dataset.activeView === 'learn'")
        self.assertTrue(page.url.endswith("?task=w1-read#learn"))
        self.assertEqual(page.locator("#continueCard h3").inner_text(), "阅读 week1/notes.md")
        self.assert_no_writes_or_runtime_errors(errors)

    def test_reduced_motion_uses_atomic_focus_preserving_fallback(self) -> None:
        page, errors = self.open_page(
            viewport={"width": 1440, "height": 1024},
            reduced_motion="reduce",
        )
        self.wait_for_home_task(page)
        page.evaluate(
            """() => {
              window.__homeTransitionCalls = 0;
              if (typeof document.startViewTransition !== 'function') return;
              const original = document.startViewTransition.bind(document);
              document.startViewTransition = (callback) => {
                window.__homeTransitionCalls += 1;
                return original(callback);
              };
            }"""
        )
        page.get_by_role("button", name="进入当前任务").click()
        page.wait_for_function("document.body.dataset.activeView === 'learn'")
        motion = page.locator("#view-learn").evaluate(
            """element => {
              const style = getComputedStyle(element);
              return {name: style.animationName, duration: style.animationDuration};
            }"""
        )
        self.assertEqual(page.evaluate("window.__homeTransitionCalls"), 0)
        self.assertEqual(motion["name"], "reduced-view-enter")
        self.assertLessEqual(float(motion["duration"].removesuffix("s")), 0.16)
        self.assertEqual(page.evaluate("document.activeElement.id"), "learnHeading")
        self.assert_no_writes_or_runtime_errors(errors)

    def test_mobile_home_and_tablet_workspace_keep_touch_contract(self) -> None:
        page, errors = self.open_page(viewport={"width": 390, "height": 844})
        self.wait_for_home_task(page)

        for width in (390, 430, 720, 920):
            page.set_viewport_size({"width": width, "height": 844})
            page.wait_for_timeout(80)
            metrics = page.evaluate(
                """() => {
                  const rect = (element) => {
                    const value = element.getBoundingClientRect();
                    return {left: value.left, top: value.top, right: value.right, bottom: value.bottom, width: value.width, height: value.height};
                  };
                  return {
                    cta: rect(document.querySelector('.home-primary-action')),
                    nav: rect(document.querySelector('.mobile-nav')),
                    targets: [...document.querySelectorAll('.home-brand,.home-progress-link,.home-signals .text-action,.mobile-nav a')].map(rect),
                    scrollWidth: document.documentElement.scrollWidth,
                    innerWidth,
                    innerHeight,
                  };
                }"""
            )
            self.assertGreaterEqual(metrics["cta"]["top"], 0)
            self.assertLessEqual(metrics["cta"]["bottom"], metrics["innerHeight"])
            self.assertLessEqual(metrics["cta"]["bottom"], metrics["nav"]["top"])
            self.assertLessEqual(metrics["scrollWidth"], metrics["innerWidth"] + 1)
            for target in metrics["targets"]:
                self.assertGreaterEqual(target["width"], 43.9)
                self.assertGreaterEqual(target["height"], 43.9)

        for width in (430, 720):
            page.set_viewport_size({"width": width, "height": 844})
            page.goto(f"{self.fixture.url}/progress.html?task=w1-read#learn", wait_until="domcontentloaded")
            page.wait_for_function("document.body.dataset.activeView === 'learn'")
            visible_tabs = page.locator(".workspace-tabs button:not([hidden])")
            self.assertEqual(visible_tabs.count(), 2)
            for index in range(visible_tabs.count()):
                self.assertGreaterEqual(visible_tabs.nth(index).bounding_box()["height"], 43.9)
            visible_panels = page.locator('[data-workspace-panel][aria-hidden="false"]')
            self.assertEqual(visible_panels.count(), 1)
            for panel in page.locator("[data-workspace-panel]").all():
                inactive = panel.get_attribute("aria-hidden") == "true"
                self.assertEqual(panel.evaluate("element => element.inert"), inactive)
            for selector in (".learn-brand", ".learn-progress-link", "#continueCard .task-btn"):
                targets = page.locator(selector)
                self.assertGreater(targets.count(), 0)
                for index in range(targets.count()):
                    box = targets.nth(index).bounding_box()
                    self.assertGreaterEqual(box["width"], 43.9)
                    self.assertGreaterEqual(box["height"], 43.9)
            self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width + 1)

        page.set_viewport_size({"width": 920, "height": 844})
        page.goto(f"{self.fixture.url}/progress.html?task=r06-w1-ex1#learn", wait_until="domcontentloaded")
        page.wait_for_function("document.body.dataset.activeView === 'learn' && document.querySelector('#workspaceTabPractice:not([hidden])')")
        tabs = page.locator(".workspace-tabs button:not([hidden])")
        self.assertEqual(tabs.count(), 3)
        for index in range(tabs.count()):
            self.assertGreaterEqual(tabs.nth(index).bounding_box()["height"], 43.9)
        page.get_by_role("tab", name="练习").click()
        page.wait_for_function("document.querySelector('#terminal').getAttribute('aria-hidden') === 'false'")
        page.wait_for_selector('.terminal-chip[data-command="mkdir -p week1/self_check"]')
        visible_panels = page.locator('[data-workspace-panel][aria-hidden="false"]')
        self.assertEqual(visible_panels.count(), 1)
        for panel in page.locator("[data-workspace-panel]").all():
            inactive = panel.get_attribute("aria-hidden") == "true"
            self.assertEqual(panel.evaluate("element => element.inert"), inactive)
        for selector in (".terminal-chip", "#terminalInput", "#terminalRun", "#terminalReset", "#terminalClear"):
            targets = page.locator(selector)
            self.assertGreater(targets.count(), 0)
            for index in range(targets.count()):
                box = targets.nth(index).bounding_box()
                self.assertGreaterEqual(box["width"], 43.9)
                self.assertGreaterEqual(box["height"], 43.9)
                if selector == ".terminal-chip":
                    self.assertLessEqual(targets.nth(index).evaluate("element => element.scrollWidth"), box["width"] + 1)
        self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 921)
        self.assert_no_writes_or_runtime_errors(errors)

    def test_loading_home_cannot_enter_taskless_learn(self) -> None:
        with FixtureServer(progress_delay=1.0) as delayed:
            page, errors = self.open_page(
                viewport={"width": 430, "height": 844},
                fixture=delayed,
            )
            page.wait_for_selector("#homeTaskCard")
            self.assertEqual(page.locator("#homeTaskCard").get_attribute("aria-disabled"), "true")
            self.assertTrue(page.locator(".home-primary-action").is_disabled())
            page.evaluate(
                """() => {
                  document.querySelector('#homeTaskCard').click();
                  document.querySelector('.home-primary-action').click();
                }"""
            )
            page.wait_for_timeout(80)
            self.assertEqual(page.evaluate("document.body.dataset.activeView"), "home")
            self.assertNotIn("task=", page.url)
            self.wait_for_home_task(page)
            page.get_by_role("button", name="进入当前任务").click()
            page.wait_for_function("document.body.dataset.activeView === 'learn'")
            self.assertTrue(page.url.endswith("?task=w1-read#learn"))
            self.assert_no_writes_or_runtime_errors(errors, delayed)


if __name__ == "__main__":
    unittest.main()

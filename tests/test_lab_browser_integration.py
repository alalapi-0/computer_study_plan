"""Browser-to-production API-to-real PTY validation using disposable Attempts.

Uses the guarded fixed Playwright runtime and headless task-owned browser.
Runs separately because the existing outer UI sandbox denies nested userns.
No formal progress or Attempt store is opened; this is technical proxy validation.
"""
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from lab_runtime import LabManager
from progress_server import ProgressRequestHandler


class LiveLabBrowserTest(unittest.TestCase):
    def test_real_shell_solve_reconnect_reset_and_legacy_read(self):
        with tempfile.TemporaryDirectory(prefix="lab-browser-") as temporary:
            manager = LabManager(ROOT / "content/scenarios", Path(temporary) / "state")
            self.assertTrue(manager.capabilities()["available"], "real isolation is required")
            server = ThreadingHTTPServer(("127.0.0.1", 0), ProgressRequestHandler)
            server.lab_manager = manager
            server.lab_token = "disposable-ui-test-capability"
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch(headless=True)
                    context = browser.new_context(viewport={"width": 1440, "height": 1024})
                    page = context.new_page()
                    errors, requests = [], []
                    page.on("pageerror", lambda error: errors.append(str(error)))
                    page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
                    page.on("requestfailed", lambda request: errors.append(str(request.failure)) if "aborted" not in str(request.failure).lower() else None)
                    page.on("request", lambda request: requests.append((request.method, request.url)))
                    base = f"http://127.0.0.1:{server.server_address[1]}"
                    page.goto(base + "/?scenario=path-cwd-input")
                    page.wait_for_selector("#startButton:not([disabled])")
                    page.locator("#hintToggle").click()
                    page.locator("#startButton").click()
                    try:
                        page.wait_for_selector('#attemptStatus[data-status="active"]', timeout=4000)
                    except Exception:
                        print({"ui_status": page.locator("#attemptStatus").inner_text(), "operation": page.locator("#operationState").inner_text(), "errors": errors, "manager_status": [(a["status"],a.get("end_reason")) for a in manager.history()["attempts"]]})
                        raise
                    first_id = page.evaluate("new URL(location.href).searchParams.get('attempt')")
                    page.locator("#checkButton").click()
                    page.wait_for_selector("#checksList .fail")
                    self.assertTrue(page.locator("#solutionPanel").is_hidden())
                    # Type into the actual xterm textarea; the UI forwards input
                    # to Bash rather than calling the backend directly.
                    for step in next(s for s in manager.catalog()["scenarios"] if s["id"] == "path-cwd-input")["hints"]:
                        textarea = page.locator(".xterm-helper-textarea")
                        textarea.focus()
                        page.keyboard.insert_text(step["command"])
                        page.keyboard.press("Enter")
                        page.wait_for_timeout(250)
                    try:
                        page.wait_for_function("() => document.querySelector('#terminal').innerText.includes('records=3')", timeout=5000)
                    except Exception:
                        print({"terminal_output": manager.snapshot(first_id)["output"], "terminal_notice": page.locator("#terminalMessage").inner_text(), "errors": errors})
                        raise
                    page.locator("#checkButton").click()
                    page.wait_for_selector("#checksList .pass")
                    self.assertTrue(manager.snapshot(first_id)["attempt"]["checks"][-1]["passed"])
                    self.assertIn("终端输出 512 KiB", page.locator("#environmentFacts").inner_text())
                    page.reload()
                    page.wait_for_selector('#attemptStatus[data-status="active"]')
                    self.assertEqual(page.evaluate("new URL(location.href).searchParams.get('attempt')"), first_id)
                    self.assertEqual(page.locator("#hintToggle").get_attribute("aria-pressed"), "true")
                    page.screenshot(path="/home/alalapi/Caches/computer-study-plan/refactor-live-after-desktop.png", full_page=True)
                    page.set_viewport_size({"width": 390, "height": 844})
                    self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), 391)
                    page.screenshot(path="/home/alalapi/Caches/computer-study-plan/refactor-live-after-mobile.png", full_page=True)
                    # Reload creates a fresh 120 ms terminal-fit timer. Reset in
                    # the same browser task so that stale resize cancellation is
                    # verified against the production API, not only the fixture.
                    page.reload(wait_until="domcontentloaded")
                    page.wait_for_selector('#attemptStatus[data-status="active"]')
                    page.evaluate("() => { document.querySelector('#resetButton').click(); document.querySelector('#confirmReset').click(); }")
                    page.wait_for_function("first => new URL(location.href).searchParams.get('attempt') !== first && document.querySelector('#attemptStatus').dataset.status === 'active'", arg=first_id)
                    reset_index = next(index for index, (_method, url) in enumerate(requests) if url.endswith(f"/attempts/{first_id}/reset"))
                    self.assertFalse([url for _method, url in requests[reset_index + 1:] if url.endswith(f"/attempts/{first_id}/resize")])
                    page.locator("#checkButton").click()
                    page.wait_for_selector("#checksList .fail")
                    self.assertEqual(len(manager.history()["attempts"]), 2)
                    page.locator("#stopButton").click()
                    page.wait_for_selector('#attemptStatus[data-status="stopped"]')
                    self.assertTrue(page.locator("#checkButton").is_disabled())
                    self.assertEqual(errors, [])
                    self.assertTrue(any(method == "POST" and url.endswith("/input") for method, url in requests))
                    self.assertTrue(all(url.startswith(base) for _, url in requests))
                    # Original production materials still resolve; no legacy
                    # mutating API is used in this disposable validation.
                    self.assertEqual(context.request.get(base + "/rounds/round_00/week1/notes.md").status, 200)
                    browser.close()
            finally:
                server.shutdown()
                server.server_close()
                thread.join()
                manager.close()

    def test_real_wav_location_check_export_download_and_reset(self):
        import hashlib
        with tempfile.TemporaryDirectory(prefix="wav-browser-") as temporary:
            manager = LabManager(ROOT / "content/scenarios", Path(temporary) / "state")
            server = ThreadingHTTPServer(("127.0.0.1", 0), ProgressRequestHandler)
            server.lab_manager = manager; server.lab_token = "temporary-wav-capability"
            thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
            try:
                self.assertTrue(manager.capabilities()["available"])
                with sync_playwright() as playwright:
                    browser = playwright.chromium.launch(headless=True)
                    context = None
                    try:
                        context = browser.new_context(accept_downloads=True)
                        page = context.new_page(); errors = []; requests = []
                        page.on("pageerror", lambda e: errors.append(str(e)))
                        page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
                        page.on("requestfailed", lambda r: errors.append(str(r.failure)) if "aborted" not in str(r.failure).lower() else None)
                        page.on("request", lambda r: requests.append(r.url))
                        base = f"http://127.0.0.1:{server.server_port}"
                        page.goto(base + "/?scenario=media-wav-quality&locate=1")
                        page.wait_for_selector("#startButton:not([disabled])")
                        self.assertEqual(manager.history()["attempts"], [])
                        self.assertTrue(page.locator("#solutionPanel").is_hidden())
                        page.locator("#startButton").click()
                        page.wait_for_selector('#attemptStatus[data-status="active"]')
                        attempt = page.evaluate("new URL(location.href).searchParams.get('attempt')")
                        page.locator("#checkButton").click(); page.wait_for_selector("#checksList .fail")
                        page.locator(".xterm-helper-textarea").focus()
                        page.keyboard.insert_text("sed -i 's/RATE = 8000/RATE = 16000/; s/AMPLITUDE = 32767/AMPLITUDE = 12000/' app/generate_tone.py && python3 app/generate_tone.py")
                        page.keyboard.press("Enter")
                        page.wait_for_function("() => document.querySelector('#terminal').innerText.includes('wrote 4000 frames at 16000 Hz')")
                        page.locator("#checkButton").click(); page.wait_for_selector("#exportWavButton:not([disabled])")
                        page.locator("#exportWavButton").click(); page.wait_for_selector("#downloadWavButton:not([disabled])")
                        binding = manager.prepare_wav(attempt)
                        with page.expect_download() as event: page.locator("#downloadWavButton").click()
                        data = Path(event.value.path()).read_bytes()
                        self.assertEqual(hashlib.sha256(data).hexdigest(), binding["artifact"]["sha256"])
                        page.locator("#resetButton").click(); page.locator("#confirmReset").click()
                        page.wait_for_function("old => new URL(location.href).searchParams.get('attempt') !== old", arg=attempt)
                        self.assertTrue(page.locator("#downloadWavButton").is_disabled())
                        self.assertEqual(errors, [])
                        self.assertTrue(requests)
                        self.assertTrue(all(url.startswith(base + "/") for url in requests))
                    finally:
                        try:
                            if context is not None: context.close()
                        finally: browser.close()
            finally:
                server.shutdown(); server.server_close(); thread.join(); manager.close()


if __name__ == "__main__":
    unittest.main()

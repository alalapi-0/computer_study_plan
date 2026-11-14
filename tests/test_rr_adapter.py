"""Targeted RR tests: public fixtures only, no production identity or learning state."""
import base64
import contextlib
import copy
import hashlib
import hmac
import http.client
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import uuid
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from rr_adapter import (AGENT, FEEDBACK, Adapter, FeedbackStore, Refused, UnixServer,
                        canonical, digest, multipart, loads, validate_attachment)
from rr_feedback_cli import OwnerClient
from rr_manifest import FrozenApplication, ROOT, PROJECT_ID, ORIGIN
from lab_runtime import LabManager

KEY = b"public-fixture-key-never-a-production-key"
DEVICE = "a" * 64

def exchange(sock, method, path, body=b"", headers=None, *, owner=False):
    connection = http.client.HTTPConnection("rr-owner.local" if owner else "pch-rr.local", timeout=5)
    peer = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    peer.settimeout(5); peer.connect(str(sock)); connection.sock = peer
    try:
        fields = {"Host": "rr-owner.local" if owner else "pch-rr.local", "Content-Length": str(len(body))}
        fields.update(headers or {})
        connection.request(method, path, body, fields)
        response = connection.getresponse()
        return response.status, response.read(), dict(response.getheaders())
    finally:
        connection.close(); peer.close()

def assertion(challenge, method, path, body, device=DEVICE):
    now = int(time.time())
    value = {"v": 1, "challenge": challenge, "device_sha256": device,
             "project_id": PROJECT_ID, "origin": ORIGIN, "method": method, "path": path,
             "body_sha256": digest(body), "nonce": str(uuid.uuid4()), "issued_at": now, "expires": now + 30}
    value["mac"] = hmac.new(KEY, canonical(value), hashlib.sha256).hexdigest()
    return base64.urlsafe_b64encode(canonical(value)).decode().rstrip("=")

def browser_request(sock, method, path, body=b"", content_type=None, device=DEVICE):
    status, raw, _ = exchange(sock, "GET", "/__rr-local/v1/challenge")
    if status != 200:
        return status, raw, {}
    auth = assertion(loads(raw)["challenge"], method, path, body, device)
    headers = {"Origin": ORIGIN, "X-PCH-RR-Auth": auth}
    if content_type:
        headers["Content-Type"] = content_type
    return exchange(sock, method, path, body, headers)

def payload(app, text="Public fixture feedback", *, rid=None, attachment=b"public fixture\n"):
    attachments = [] if attachment is None else [{"attachment_id": "fixture-text",
                    "size": len(attachment), "sha256": digest(attachment)}]
    return {"schema": 1, "client_request_id": rid or str(uuid.uuid4()), "project_id": PROJECT_ID,
            "page_path": "/", "source": app.source,
            "resource": {k: app.resources["/"][k] for k in ("id", "sha256", "mode", "preview_version")},
            "description": text, "expected": "Expected", "actual": "Actual", "steps": "Open page",
            "submitted_at": "2026-10-21T00:00:00Z", "attachments": attachments}

def form(value, attachment=b"public fixture\n", kind="text/plain"):
    boundary = "public_fixture_boundary"
    raw = b"--" + boundary.encode() + b'\r\nContent-Disposition: form-data; name="feedback"; filename="feedback.json"\r\nContent-Type: application/json\r\n\r\n' + canonical(value) + b"\r\n"
    if attachment is not None:
        raw += b"--" + boundary.encode() + b'\r\nContent-Disposition: form-data; name="attachment.0"; filename="../../ignored.txt"\r\nContent-Type: ' + kind.encode() + b"\r\n\r\n" + attachment + b"\r\n"
    raw += b"--" + boundary.encode() + b"--\r\n"
    return raw, "multipart/form-data; boundary=" + boundary

class Fixture:
    def __enter__(self):
        self.temp = tempfile.TemporaryDirectory(prefix="csp-rr-public-")
        self.root = Path(self.temp.name)
        self.manager = LabManager(ROOT / "content/scenarios", self.root / "lab")
        self.app = FrozenApplication()
        self.store = FeedbackStore(self.root / "feedback")
        self.adapter = Adapter(self.manager, self.app, self.store, KEY,
                               gateway_uid=os.getuid(), owner_uid=os.getuid())
        self.browser = self.root / "browser.sock"; self.owner = self.root / "owner.sock"
        self.servers = [UnixServer(self.browser, self.adapter, production=False),
                        UnixServer(self.owner, self.adapter, owner_role=True, production=False)]
        self.threads = [threading.Thread(target=s.serve_forever) for s in self.servers]
        for thread in self.threads: thread.start()
        return self

    def __exit__(self, *_):
        for server in self.servers: server.shutdown()
        for server in self.servers: server.server_close()
        for thread in self.threads: thread.join()
        self.store.close(); self.manager.close(); self.temp.cleanup()

class RRTests(unittest.TestCase):
    def test_manifest_unlisted_runtime_input_closes(self):
        from rr_manifest import catalog_members, SCENARIOS
        with tempfile.TemporaryDirectory(prefix="csp-rr-input-public-") as temp:
            root = Path(temp); catalog = root / "content/scenarios"; catalog.mkdir(parents=True)
            (catalog / "publication.json").write_text("{}")
            for scenario in SCENARIOS:
                directory = catalog / scenario; directory.mkdir()
                for name in ("scenario.json", "setup.sh", "check.py"): (directory / name).write_text("")
            catalog_members(root)
            extra = catalog / SCENARIOS[0] / "unlisted.py"; extra.write_text("")
            with self.assertRaises(ValueError): catalog_members(root)
            extra.unlink(); (catalog / "unlisted-scenario").mkdir()
            with self.assertRaises(ValueError): catalog_members(root)

    def test_nested_public_directory_cannot_inherit_parent_git_identity(self):
        from rr_manifest import SCENARIOS, source_inputs
        scratch = ROOT / ".rr-candidates"
        if scratch.is_symlink():
            raise RuntimeError("preserve unexpected linked fixture parent")
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="nested-public-", dir=scratch) as temporary:
            candidate = Path(temporary)
            catalog = candidate / "content/scenarios"
            catalog.mkdir(parents=True)
            (catalog / "publication.json").write_text("{}")
            for name in SCENARIOS:
                directory = catalog / name
                directory.mkdir()
                for filename in ("scenario.json", "setup.sh", "check.py"):
                    (directory / filename).write_text("")
            with self.assertRaisesRegex(ValueError, "source_git_root_mismatch"):
                source_inputs(candidate)

    def test_generic_fd_public_fixture_and_writable_rejection(self):
        import array
        import fcntl
        from rr_adapter import receive_provider_key
        for readonly in (True, False):
            with tempfile.TemporaryDirectory(prefix="csp-rr-fd-public-") as temp:
                path = Path(temp) / "provider.sock"
                with socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET) as listener:
                    listener.bind(str(path)); listener.listen(1)
                    failures = []
                    def provider():
                        fd = None
                        try:
                            peer, _ = listener.accept()
                            with peer:
                                request = peer.recv(512)
                                assert request == canonical({"project_id": PROJECT_ID, "recipient_uid": 1000, "schema": 1}) + b"\n"
                                fd = os.memfd_create("public-rr-fixture", os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING)
                                os.fchmod(fd, 0o400); os.write(fd, KEY)
                                fcntl.fcntl(fd, fcntl.F_ADD_SEALS, fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL)
                                if readonly:
                                    ro = os.open(f"/proc/self/fd/{fd}", os.O_RDONLY | os.O_CLOEXEC)
                                    os.close(fd); fd = ro
                                peer.sendmsg([canonical({"key_fd": True, "project_id": PROJECT_ID, "schema": 1}) + b"\n"],
                                             [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", [fd]))])
                        except BaseException as error:
                            failures.append(str(error))
                        finally:
                            if fd is not None: os.close(fd)
                    thread = threading.Thread(target=provider); thread.start()
                    try:
                        with socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET) as client:
                            client.settimeout(3); client.connect(str(path))
                            if readonly:
                                self.assertEqual(receive_provider_key(client, os.getuid(), os.getgid()), KEY)
                            else:
                                with self.assertRaises(Refused):
                                    receive_provider_key(client, os.getuid(), os.getgid())
                    finally:
                        thread.join(timeout=5)
                    self.assertFalse(thread.is_alive()); self.assertFalse(failures)

    def test_readonly_shared_manager_and_private_boundaries(self):
        with Fixture() as f:
            with patch.object(f.manager, "history", side_effect=AssertionError("history must not refresh")), \
                 patch.object(f.manager, "snapshot", side_effect=AssertionError("snapshot must not refresh")):
                status, raw, _ = browser_request(f.browser, "GET", "/__rr/v1/workbench")
                data = loads(raw)
                self.assertEqual(status, 200)
                self.assertEqual(data["scenarios"], f.manager.catalog()["scenarios"])
                self.assertEqual(len(data["scenarios"]), 8)
                self.assertNotIn("token", data)
                self.assertNotIn("attempts", data)
            status, raw, _ = browser_request(f.browser, "GET", "/")
            self.assertEqual(status, 200)
            self.assertEqual(raw, (ROOT / "index.html").read_bytes())
            for method, path in [("GET", "/api/lab/bootstrap"), ("GET", "/api/lab/history"),
                                 ("GET", "/api/lab/attempts/anything"), ("POST", "/api/lab/start"),
                                 ("GET", AGENT), ("GET", "/progress.json"),
                                 ("GET", "/.git/config"), ("GET", "/__rr/v1/workbench?x=1")]:
                self.assertEqual(browser_request(f.browser, method, path)[0], 404, (method, path))
            self.assertEqual(exchange(f.browser, "GET", "/__rr/v1/workbench")[0], 403)
            f.adapter.gateway_uid = os.getuid() + 1
            self.assertEqual(exchange(f.browser, "GET", "/__rr-local/v1/challenge")[0], 403)
            f.adapter.gateway_uid = os.getuid()
            from progress_server import ProgressRequestHandler
            from http.server import ThreadingHTTPServer
            local = ThreadingHTTPServer(("127.0.0.1", 0), ProgressRequestHandler)
            local.lab_manager = f.manager; local.lab_token = "public-local-fixture-token"
            thread = threading.Thread(target=local.serve_forever); thread.start()
            try:
                client = http.client.HTTPConnection("127.0.0.1", local.server_port)
                client.request("GET", "/api/lab/bootstrap"); reply = client.getresponse()
                self.assertEqual(loads(reply.read())["token"], "public-local-fixture-token")
                client.close()
            finally:
                local.shutdown(); local.server_close(); thread.join()

    def test_atomic_persistence_idempotency_attachments_and_source(self):
        with Fixture() as f:
            value = payload(f.app); body, kind = form(value)
            status, raw, _ = browser_request(f.browser, "POST", FEEDBACK, body, kind)
            receipt = loads(raw); fid = receipt["feedback_id"]
            self.assertEqual(status, 201)
            self.assertEqual(browser_request(f.browser, "POST", FEEDBACK, body, kind)[0], 200)
            altered = dict(value, description="Different")
            self.assertEqual(browser_request(f.browser, "POST", FEEDBACK, *form(altered))[0], 409)
            stale = copy.deepcopy(value); stale["source"]["build_id"] = "0" * 64
            self.assertEqual(browser_request(f.browser, "POST", FEEDBACK, *form(stale))[0], 409)
            mistyped = copy.deepcopy(value); mistyped["source"]["dirty"] = 1
            self.assertEqual(browser_request(f.browser, "POST", FEEDBACK, *form(mistyped))[0], 409)
            self.assertEqual(browser_request(f.browser, "GET", FEEDBACK + "/by-request/" + value["client_request_id"])[0], 200)
            self.assertEqual(browser_request(f.browser, "GET", FEEDBACK + "/" + fid, device="b"*64)[0], 404)
            self.assertEqual(browser_request(f.browser, "GET", FEEDBACK + "/" + fid + "/attachments/fixture-text")[1], b"public fixture\n")
            with self.assertRaises(Refused): FeedbackStore(f.root / "feedback")
            f.store.close(); f.store = FeedbackStore(f.root / "feedback"); f.adapter.store = f.store
            self.assertEqual(f.store.get(fid)["state"], "pending")
            self.assertEqual(f.store.attachment(fid, "fixture-text")[0], b"public fixture\n")
            linked = f.root / "linked"; linked.symlink_to(f.root / "feedback", target_is_directory=True)
            with self.assertRaises(Refused): FeedbackStore(linked)
            self.assertFalse((f.root / "ignored.txt").exists())
            saved = f.store.directory(fid) / "feedback.json"
            original = saved.read_bytes(); corrupted = loads(original)
            corrupted["payload"]["description"] = "Corrupted fixture"
            saved.write_bytes(canonical(corrupted))
            with self.assertRaises(Refused): f.store.get(fid)
            saved.write_bytes(original)
            with self.assertRaises(Refused): loads(b'{"x":1,"x":2}')
            with self.assertRaises(Refused): loads(b'{"x":1.1}')
            with self.assertRaises(Refused): loads(b'{"x":"\\ud800"}')
            with self.assertRaises(Refused): multipart(b"x" * (2*1024*1024+32769), kind)
            with self.assertRaises(Refused): validate_attachment(b"\xff", "text/plain")
            from PIL import Image
            buffer = io.BytesIO(); Image.new("RGB", (2, 2)).save(buffer, format="PNG")
            validate_attachment(buffer.getvalue(), "image/png")
            with self.assertRaises(Refused): validate_attachment(buffer.getvalue(), "image/jpeg")
            with self.assertRaises(Refused): validate_attachment(b"not an image", "image/png")

    def test_actual_cli_read_ack_result_and_unauthorized_rejection(self):
        with Fixture() as f:
            status, raw, _ = browser_request(f.browser, "POST", FEEDBACK, *form(payload(f.app)))
            fid = loads(raw)["feedback_id"]; cli = OwnerClient(f.owner)
            record, hashes = cli.read(fid)
            incomplete = {"revision": 1, "payload_sha256": record["payload_sha256"],
                          "attachments": hashes, "read_token": "invented"}
            self.assertEqual(exchange(f.owner, "POST", AGENT + "/" + fid + "/ack",
                                      canonical(incomplete), owner=True)[0], 409)
            result = cli.ack(fid)
            self.assertEqual(result["state"], "agent_read")
            self.assertEqual(result["read_receipt"]["attachments"], hashes)
            self.assertEqual(cli.result(fid, "Public fixture handled", ["fixture:check"])["state"], "processed")
            with self.assertRaises(Refused): cli.result(fid, "Different", [])
            command = ("import sys; sys.path.insert(0," + repr(str(ROOT / "scripts")) + ");"
                       "from rr_feedback_cli import main,OwnerClient;"
                       "raise SystemExit(main(['read'," + repr(fid) + "],client=OwnerClient(" + repr(str(f.owner)) + ")))")
            output = subprocess.run([sys.executable, "-B", "-c", command], capture_output=True, text=True)
            self.assertEqual(output.returncode, 0, output.stderr)
            self.assertEqual(json.loads(output.stdout)["state"], "processed")
            self.assertNotIn("read_token", json.loads(output.stdout))
            f.adapter.owner_uid = os.getuid() + 1
            self.assertEqual(exchange(f.owner, "GET", AGENT, owner=True)[0], 403)
            self.assertEqual(browser_request(f.browser, "POST", AGENT + "/" + fid + "/ack", canonical(incomplete))[0], 404)

    def test_auth_replay_and_version_failure_close(self):
        with Fixture() as f:
            _, raw, _ = exchange(f.browser, "GET", "/__rr-local/v1/challenge")
            token = assertion(loads(raw)["challenge"], "GET", "/__rr/v1/manifest", b"")
            headers = {"Origin": ORIGIN, "X-PCH-RR-Auth": token}
            self.assertEqual(exchange(f.browser, "GET", "/__rr/v1/manifest", headers=headers)[0], 200)
            self.assertEqual(exchange(f.browser, "GET", "/__rr/v1/manifest", headers=headers)[0], 403)
            _, raw, _ = exchange(f.browser, "GET", "/__rr-local/v1/challenge")
            token = assertion(loads(raw)["challenge"], "GET", "/__rr/v1/manifest", b"")
            value = loads(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))
            value["project_id"] = "asset-operations-platform"
            unsigned = {k: v for k, v in value.items() if k != "mac"}
            value["mac"] = hmac.new(KEY, canonical(unsigned), hashlib.sha256).hexdigest()
            bad = base64.urlsafe_b64encode(canonical(value)).decode().rstrip("=")
            self.assertEqual(exchange(f.browser, "GET", "/__rr/v1/manifest",
                                     headers={"Origin": ORIGIN, "X-PCH-RR-Auth": bad})[0], 403)
            with patch.object(f.app, "check", side_effect=ValueError("changed")):
                self.assertEqual(exchange(f.browser, "GET", "/__rr-local/v1/challenge")[0], 503)


def browser_checks():
    """Actual headless Chromium + project Unix HTTP, with a public gateway fixture."""
    from playwright.sync_api import sync_playwright
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "/home/alalapi/Runtimes/computer-study-plan/browsers"
    observations = {"classification": "public fixture, actual project handlers/catalog/CLI; gateway substituted",
                    "requests": [], "console": [], "pageerrors": [], "requestfailed": []}
    with Fixture() as f, sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 800})
            drop_next = [False]
            syncing = []
            def gateway(route):
                from urllib.parse import urlsplit
                request = route.request
                parsed = urlsplit(request.url)
                if parsed.scheme + "://" + parsed.netloc != ORIGIN:
                    observations["requestfailed"].append("unexpected_origin")
                    route.abort(); return
                body = request.post_data_buffer or b""
                status, raw, headers = browser_request(f.browser, request.method, parsed.path + ("?" + parsed.query if parsed.query else ""),
                                                       body, request.headers.get("content-type"))
                backend_status = status
                if request.method == "POST" and drop_next[0]:
                    drop_next[0] = False
                    status, raw = 503, canonical({"error": "public_fixture_lost_response"})
                observations["requests"].append({"method": request.method, "path": parsed.path, "status": status, "backend_status": backend_status})
                route.fulfill(status=status, body=raw, headers={"Content-Type": headers.get("Content-Type", "application/json")})
            context.route("**/*", gateway)
            page = context.new_page()
            page.on("console", lambda message: observations["console"].append({"type": message.type, "text": message.text}) if message.type in ("warning", "error") else None)
            page.on("pageerror", lambda error: observations["pageerrors"].append(str(error)))
            page.on("requestfailed", lambda request: observations["requestfailed"].append(request.url))
            page.goto(ORIGIN + "/")
            page.locator("#rrFeedbackMount").wait_for(state="visible")
            assert page.locator("#catalogCount").inner_text() == "8 / 8"
            assert page.locator("#startButton").is_disabled()
            assert page.locator('a[href="progress.html"]').count() == 0
            assert "个人尝试记录" in page.locator("#capabilityNotice").inner_text()
            assert "不开放个人尝试记录" in page.locator("#historyStatus").inner_text()
            page.locator("#hintToggle").click()
            page.locator("#solutionButton").click()
            assert page.locator("#solutionPanel").is_visible()
            page.locator("#solutionButton").click()
            page.locator("#hintToggle").click()
            observations["desktop_overflow"] = page.evaluate("document.documentElement.scrollWidth > innerWidth")
            observations["desktop_image"] = page.context.new_cdp_session(page).send(
                "Page.captureScreenshot", {"format": "jpeg", "quality": 42, "fromSurface": False})["data"]
            page.locator(".rr-feedback-link").click()
            page.locator("#rr-description").fill("公开夹具：只读审核反馈")
            page.locator("#rr-expected").fill("期待清楚说明只读范围")
            page.locator("#rr-actual").fill("已看见真实题库")
            page.locator("#rr-steps").fill("打开页面并阅读题目")
            page.locator("#rr-files").set_input_files({"name": "public-fixture.txt", "mimeType": "text/plain", "buffer": b"public fixture\n"})
            page.locator("#rr-consent").check()
            page.get_by_role("button", name="提交反馈", exact=True).click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('持久保存')")
            fid = page.locator("#rr-query-id").input_value()
            record, hashes = OwnerClient(f.owner).read(fid)
            assert record["payload"]["source"] == f.app.source and len(hashes) == 1
            OwnerClient(f.owner).ack(fid)
            page.get_by_role("button", name="刷新处理状态").click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('Agent 已读')")
            OwnerClient(f.owner).result(fid, "公开夹具处理已完成", ["fixture:ui"])
            page.get_by_role("button", name="刷新处理状态").click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('已处理')")
            assert "公开夹具处理已完成" in page.locator("#rrFeedbackStatus").inner_text()
            observations["clean_console"] = list(observations["console"])
            page.get_by_role("button", name="新建反馈", exact=True).click()
            assert page.locator("#rr-description").evaluate("(e)=>e===document.activeElement")
            page.locator("#rr-description").fill("公开夹具：模拟回执丢失")
            page.locator("#rr-consent").check()
            posts_before = sum(item["method"] == "POST" for item in observations["requests"])
            drop_next[0] = True
            page.get_by_role("button", name="提交反馈", exact=True).click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('失败待核对')")
            page.get_by_role("button", name="核对并继续提交").click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('持久保存')")
            assert sum(item["method"] == "POST" for item in observations["requests"]) == posts_before + 1
            page.locator("#rr-query-id").fill(str(uuid.uuid4()))
            page.get_by_role("button", name="刷新处理状态").click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('失败待核对')")
            page.locator("#rr-query-id").fill(fid)
            page.get_by_role("button", name="刷新处理状态").click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('已处理')")
            page.set_viewport_size({"width": 390, "height": 844})
            page.evaluate("scrollTo(0,0)")
            observations["mobile_overflow"] = page.evaluate("document.documentElement.scrollWidth > innerWidth")
            observations["mobile_image"] = page.context.new_cdp_session(page).send(
                "Page.captureScreenshot", {"format": "jpeg", "quality": 42, "fromSurface": False})["data"]
            page.locator("#rrFeedbackHeading").scroll_into_view_if_needed()
            page.get_by_role("button", name="新建反馈", exact=True).click()
            page.locator("#rrFeedbackHeading").scroll_into_view_if_needed()
            observations["feedback_image"] = page.context.new_cdp_session(page).send(
                "Page.captureScreenshot", {"format": "jpeg", "quality": 42, "fromSurface": False})["data"]
            assert not observations["desktop_overflow"] and not observations["mobile_overflow"]
            assert not observations["pageerrors"] and not observations["requestfailed"]
            assert not observations["clean_console"], observations["clean_console"]
            assert not any(item["path"].startswith(("/api/", "/__rr-agent", "/__rr-local")) for item in observations["requests"])
            observations["source"] = f.app.source
            observations["manifest_sha256"] = digest(canonical(f.app.manifest))
            observations["checks"] = "actual catalog, read-only controls, hints/solution, submit+attachment, CLI read/ack/result, manual status, uncertain-post recovery, stale-state clearing, focus, desktop/mobile"
            page.locator("#rr-description").fill("公开夹具：错误附件修正后重试")
            page.locator("#rr-files").set_input_files({"name": "broken.png", "mimeType": "image/png", "buffer": b"not an image"})
            page.locator("#rr-consent").check()
            page.get_by_role("button", name="提交反馈", exact=True).click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('已保留填写内容')")
            assert page.locator("#rr-description").input_value() == "公开夹具：错误附件修正后重试"
            assert page.locator("#rr-description").is_enabled()
            page.locator("#rr-files").set_input_files({"name": "fixed.txt", "mimeType": "text/plain", "buffer": b"public fixture corrected\n"})
            page.get_by_role("button", name="提交反馈", exact=True).click()
            page.wait_for_function("document.getElementById('rrFeedbackStatus').textContent.includes('持久保存')")
            context.close()
        finally:
            browser.close()
    print(json.dumps(observations, ensure_ascii=False))


class RRLifecycleTests(unittest.TestCase):
    """Only the new lifecycle slice; real signals/identities, isolated public state."""
    def start_child(self, root, *, handoff=False):
        import array
        namespace = root / "namespace"
        namespace.mkdir(mode=0o700, exist_ok=True)
        ready = root / ("ready-" + uuid.uuid4().hex)
        channel, child_channel = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
        script = r'''
import sys,os,pathlib,json,socket,array
ROOT=pathlib.Path(sys.argv[4]).resolve(strict=True)
sys.path[:0]=[str(ROOT/"scripts"),str(ROOT/"tests")]
import lab_runtime,rr_adapter,progress_server,rr_manifest,test_rr_adapter
for module, relative in ((lab_runtime,"scripts/lab_runtime.py"),(rr_adapter,"scripts/rr_adapter.py"),(progress_server,"scripts/progress_server.py"),(rr_manifest,"scripts/rr_manifest.py"),(test_rr_adapter,"tests/test_rr_adapter.py")):
 assert pathlib.Path(module.__file__).resolve() == ROOT/relative, "candidate_module_origin_mismatch"
from test_rr_adapter import KEY
root=pathlib.Path(sys.argv[1]);ready=pathlib.Path(sys.argv[2]);handoff=int(sys.argv[3])
OriginalManager=lab_runtime.LabManager
class PublicManager(OriginalManager):
 def close(self):
  was_closed=getattr(self,"_closed",False)
  super().close()
  if not was_closed: print("PUBLIC_FIXTURE_MANAGER_CLOSED",flush=True)
lab_runtime.LabManager=lambda *_:PublicManager(ROOT/"content/scenarios",root/"lab")
OriginalServer=progress_server.ThreadingHTTPServer
servers=[]
def server_factory(*args,**kwargs):
 value=OriginalServer(*args,**kwargs);servers.append(value);return value
progress_server.ThreadingHTTPServer=server_factory
def rr_factory(manager):
 runner=rr_adapter.RunningAdapter.for_fixture(manager,root/"namespace",root/"feedback",KEY)
 if handoff>=0:
  with socket.socket(fileno=handoff) as peer:
   peer.sendmsg([b"public-fixture-listener"],[(socket.SOL_SOCKET,socket.SCM_RIGHTS,array.array("i",[runner.servers[0].socket.fileno()]))])
 ready.write_text(json.dumps({"pid":os.getpid(),"port":servers[0].server_port}))
 return runner
rr_adapter.RunningAdapter=rr_factory
sys.argv=["progress_server.py","--rr","--port","0"]
raise SystemExit(progress_server.main())
'''
        # Preserve the real class before substituting only main's fixture factory.
        script = script.replace('OriginalManager=lab_runtime.LabManager', 'OriginalRunner=rr_adapter.RunningAdapter\nOriginalManager=lab_runtime.LabManager')
        script = script.replace('runner=rr_adapter.RunningAdapter.for_fixture(', 'runner=OriginalRunner.for_fixture(')
        process = subprocess.Popen([sys.executable, "-B", "-u", "-c", script, str(root), str(ready),
                                    str(child_channel.fileno()) if handoff else "-1", str(ROOT)],
                                   pass_fds=(child_channel.fileno(),) if handoff else (),
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        child_channel.close()
        retained = None
        try:
            deadline = time.monotonic() + 15
            while not ready.exists() and process.poll() is None and time.monotonic() < deadline:
                time.sleep(0.02)
            if not ready.exists():
                output, error = process.communicate(timeout=5)
                channel.close()
                return process, None, None, output + error
            info = json.loads(ready.read_text())
            self.assertEqual(info["pid"], process.pid)
            if handoff:
                channel.settimeout(3)
                _, controls, flags, _ = channel.recvmsg(64, socket.CMSG_SPACE(4), socket.MSG_CMSG_CLOEXEC)
                self.assertFalse(flags & (socket.MSG_TRUNC | socket.MSG_CTRUNC))
                values = array.array("i")
                for level, kind, raw in controls:
                    self.assertEqual((level, kind), (socket.SOL_SOCKET, socket.SCM_RIGHTS))
                    values.frombytes(raw)
                self.assertEqual(len(values), 1)
                retained = socket.socket(fileno=values[0])
            channel.close()
            return process, info, retained, None
        except BaseException:
            if process.poll() is None: process.kill()
            process.communicate(timeout=10)
            if retained is not None: retained.close()
            channel.close()
            raise

    def stop_child(self, process, number):
        process.send_signal(number)
        output, error = process.communicate(timeout=15)
        self.assertEqual(process.returncode, 0, output + error)
        self.assertEqual(output.count("PUBLIC_FIXTURE_MANAGER_CLOSED"), 1, output)
        return output

    def test_normal_sigterm_and_sigint_close_shared_process(self):
        import signal
        import errno
        for number in (signal.SIGTERM, signal.SIGINT):
            with self.subTest(signal=number), tempfile.TemporaryDirectory(prefix="csp-rr-life-public-") as temp:
                root = Path(temp)
                process, info, retained, failure = self.start_child(root)
                self.assertIsNotNone(info, failure)
                try:
                    from rr_adapter import process_identity
                    record = loads((root / "feedback/.instance.json").read_bytes())
                    self.assertEqual(record["owner"], process_identity(process.pid)[0])
                    self.assertEqual(set(record["sockets"]), {"browser", "owner"})
                    self.stop_child(process, number)
                    self.assertFalse((root / "feedback/.instance.json").exists())
                    self.assertFalse((root / "namespace/browser.sock").exists())
                    self.assertFalse((root / "namespace/owner.sock").exists())
                    with socket.socket() as peer:
                        self.assertEqual(peer.connect_ex(("127.0.0.1", info["port"])), errno.ECONNREFUSED)
                finally:
                    if process.poll() is None: process.kill(); process.communicate(timeout=10)

    def test_killed_owner_active_or_changed_socket_refused_then_exact_recovery(self):
        import signal
        with tempfile.TemporaryDirectory(prefix="csp-rr-life-public-") as temp:
            root = Path(temp)
            first, info, retained, failure = self.start_child(root, handoff=True)
            self.assertIsNotNone(info, failure)
            self.assertIsNotNone(retained)
            record_path = root / "feedback/.instance.json"
            before = record_path.read_bytes()
            identities = {role: (root / ("namespace/" + role + ".sock")).lstat().st_ino for role in ("browser", "owner")}
            try:
                first.kill(); first.communicate(timeout=10)
                self.assertEqual(first.returncode, -signal.SIGKILL)
                # The recorded owner is dead, but its real listener FD remains active.
                blocked, ready, _, output = self.start_child(root)
                self.assertIsNone(ready)
                self.assertEqual(blocked.returncode, 78, output)
                self.assertEqual(record_path.read_bytes(), before)
                for role, inode in identities.items():
                    self.assertEqual((root / ("namespace/" + role + ".sock")).lstat().st_ino, inode)
                retained.close(); retained = None
                owner = root / "namespace/owner.sock"
                owner.chmod(0o640)
                blocked, ready, _, output = self.start_child(root)
                self.assertIsNone(ready)
                self.assertEqual(blocked.returncode, 78, output)
                self.assertEqual(record_path.read_bytes(), before)
                self.assertTrue((root / "namespace/browser.sock").exists())
                self.assertEqual(owner.stat().st_mode & 0o777, 0o640)
                owner.chmod(0o600)  # Restore only the test-owned exact metadata.
                recovered, ready, _, output = self.start_child(root)
                self.assertIsNotNone(ready, output)
                try:
                    from rr_adapter import process_identity, socket_metadata
                    record = loads(record_path.read_bytes())
                    self.assertEqual(record["owner"], process_identity(recovered.pid)[0])
                    self.assertNotEqual(record["owner"], loads(before)["owner"])
                    for role, item in record["sockets"].items():
                        self.assertEqual(item, dict(socket_metadata((root / ("namespace/" + role + ".sock")).lstat()),
                                                    path=str(root / ("namespace/" + role + ".sock"))))
                    self.assertEqual(exchange(root / "namespace/browser.sock", "GET", "/__rr-local/v1/challenge")[0], 200)
                    self.stop_child(recovered, signal.SIGTERM)
                    self.assertFalse(record_path.exists())
                    self.assertFalse((root / "namespace/browser.sock").exists())
                    self.assertFalse(owner.exists())
                finally:
                    if recovered.poll() is None: recovered.kill(); recovered.communicate(timeout=10)
            finally:
                if retained is not None: retained.close()
                if first.poll() is None: first.kill(); first.communicate(timeout=10)

    def test_recreated_empty_namespace_starts_new_generation_without_old_unlink(self):
        import signal
        with tempfile.TemporaryDirectory(prefix="csp-rr-life-public-") as temp:
            root = Path(temp)
            first, info, _, output = self.start_child(root)
            self.assertIsNotNone(info, output)
            try:
                first.kill(); first.communicate(timeout=10)
                self.assertEqual(first.returncode, -signal.SIGKILL)
                record_path = root / "feedback/.instance.json"
                before = record_path.read_bytes()
                original = loads(before)
                previous_directory = root / "previous-namespace"
                (root / "namespace").rename(previous_directory)
                new_directory = root / "namespace"; new_directory.mkdir(mode=0o700)
                self.assertNotEqual(new_directory.stat().st_ino, previous_directory.stat().st_ino)
                old_inodes = {p.name: p.lstat().st_ino for p in previous_directory.iterdir()}
                unknown = new_directory / "public-unknown"
                unknown.write_text("public fixture must remain")
                blocked, ready, _, output = self.start_child(root)
                self.assertIsNone(ready)
                self.assertEqual(blocked.returncode, 78, output)
                self.assertEqual(record_path.read_bytes(), before)
                self.assertEqual(unknown.read_text(), "public fixture must remain")
                unknown.unlink()  # Only the test-owned sentinel is removed.
                next_process, ready, _, output = self.start_child(root)
                self.assertIsNotNone(ready, output)
                try:
                    from rr_adapter import process_identity
                    record = loads(record_path.read_bytes())
                    self.assertEqual(record["owner"], process_identity(next_process.pid)[0])
                    self.assertEqual(record["owner"]["boot_id"], original["owner"]["boot_id"])
                    self.assertEqual(record["namespace"]["ino"], new_directory.stat().st_ino)
                    self.assertNotEqual(record["namespace"], original["namespace"])
                    self.assertEqual(old_inodes, {p.name: p.lstat().st_ino for p in previous_directory.iterdir()})
                    self.stop_child(next_process, signal.SIGTERM)
                    self.assertFalse(record_path.exists())
                    self.assertEqual(list(new_directory.iterdir()), [])
                    self.assertEqual(old_inodes, {p.name: p.lstat().st_ino for p in previous_directory.iterdir()})
                finally:
                    if next_process.poll() is None: next_process.kill(); next_process.communicate(timeout=10)
            finally:
                if first.poll() is None: first.kill(); first.communicate(timeout=10)

    def test_unknown_file_and_link_are_preserved(self):
        for kind in ("file", "link"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory(prefix="csp-rr-life-public-") as temp:
                root = Path(temp); namespace = root / "namespace"; namespace.mkdir(mode=0o700)
                target = root / "public-sentinel"; target.write_text("public fixture")
                unknown = namespace / "browser.sock"
                if kind == "file": unknown.write_text("unowned public fixture")
                else: unknown.symlink_to(target)
                inode = unknown.lstat().st_ino
                process, ready, _, output = self.start_child(root)
                self.assertIsNone(ready)
                self.assertEqual(process.returncode, 78, output)
                self.assertEqual(unknown.lstat().st_ino, inode)
                self.assertEqual(target.read_text(), "public fixture")
                self.assertFalse((root / "feedback/.instance.json").exists())



class RRStartupClassificationTests(unittest.TestCase):
    def test_late_provider_retry_and_binding_failure_terminal(self):
        import array
        import fcntl
        from types import SimpleNamespace
        from unittest.mock import Mock
        import rr_adapter
        import progress_server
        import lab_runtime
        def classified(action):
            try:
                action()
            except Exception as error:
                return error
            self.fail("expected startup failure")
        def main_exit(error):
            manager = SimpleNamespace(close=Mock())
            server = SimpleNamespace(server_close=Mock())
            with patch.object(lab_runtime, "LabManager", return_value=manager), \
                 patch.object(progress_server, "ThreadingHTTPServer", return_value=server), \
                 patch.object(rr_adapter, "RunningAdapter", side_effect=error), \
                 patch.object(sys, "argv", ["progress_server.py", "--rr", "--port", "0"]), \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                code = progress_server.main()
            manager.close.assert_called_once(); server.server_close.assert_called_once()
            return code
        with tempfile.TemporaryDirectory(prefix="csp-rr-startup-public-") as temp:
            directory = Path(temp) / "provider"; directory.mkdir(mode=0o750)
            path = directory / "key.sock"
            missing = classified(lambda: rr_adapter._provider_metadata(path, os.getuid(), os.getgid()))
            self.assertIsInstance(missing, rr_adapter.ProviderUnavailable)
            self.assertEqual(main_exit(missing), 75)
            # A later real fixture provider can now supply a sealed read-only FD.
            listener = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            listener.bind(str(path)); path.chmod(0o660); listener.listen(1)
            failures = []
            def public_provider():
                fd = None
                try:
                    peer, _ = listener.accept()
                    with peer:
                        self.assertEqual(peer.recv(512), canonical({"project_id": PROJECT_ID, "recipient_uid": 1000, "schema": 1}) + b"\n")
                        fd = os.memfd_create("public-startup-fixture", os.MFD_CLOEXEC | os.MFD_ALLOW_SEALING)
                        os.fchmod(fd, 0o400); os.write(fd, KEY)
                        fcntl.fcntl(fd, fcntl.F_ADD_SEALS, fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL)
                        ro = os.open(f"/proc/self/fd/{fd}", os.O_RDONLY | os.O_CLOEXEC)
                        os.close(fd); fd = ro
                        peer.sendmsg([canonical({"key_fd": True, "project_id": PROJECT_ID, "schema": 1}) + b"\n"],
                                     [(socket.SOL_SOCKET, socket.SCM_RIGHTS, array.array("i", [fd]))])
                except BaseException as error:
                    failures.append(str(error))
                finally:
                    if fd is not None: os.close(fd)
            thread = threading.Thread(target=public_provider); thread.start()
            try:
                rr_adapter._provider_metadata(path, os.getuid(), os.getgid())
                self.assertEqual(rr_adapter._provider_exchange(path, os.getuid(), os.getgid()), KEY)
            finally:
                listener.close(); thread.join(timeout=5)
            self.assertFalse(thread.is_alive()); self.assertFalse(failures)
            refused = classified(lambda: rr_adapter._provider_exchange(path, os.getuid(), os.getgid()))
            self.assertIsInstance(refused, rr_adapter.ProviderUnavailable)
            self.assertEqual(main_exit(refused), 75)
            # Real local peer identity, deliberately wrong declared binding; no mocked UID/GID.
            left, right = socket.socketpair(socket.AF_UNIX, socket.SOCK_SEQPACKET)
            try:
                wrong_peer = classified(lambda: rr_adapter.receive_provider_key(left, os.getuid() + 1, os.getgid()))
                self.assertIsInstance(wrong_peer, rr_adapter.Refused)
                self.assertNotIsInstance(wrong_peer, rr_adapter.ProviderUnavailable)
                self.assertEqual(main_exit(wrong_peer), 78)
                left.settimeout(0.05)
                timeout = classified(lambda: rr_adapter.receive_provider_key(left, os.getuid(), os.getgid()))
                self.assertIsInstance(timeout, rr_adapter.ProviderUnavailable)
                self.assertEqual(main_exit(timeout), 75)
            finally:
                left.close(); right.close()
            path.chmod(0o600)
            wrong_mode = classified(lambda: rr_adapter._provider_metadata(path, os.getuid(), os.getgid()))
            self.assertNotIsInstance(wrong_mode, rr_adapter.ProviderUnavailable)
            self.assertEqual(main_exit(wrong_mode), 78)
            self.assertEqual(main_exit(ValueError("source_changed")), 78)


if __name__ == "__main__":
    if sys.argv[1:] == ["--ui"]:
        browser_checks()
    else:
        unittest.main()

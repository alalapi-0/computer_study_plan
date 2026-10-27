"""Exercise browser authority and serving boundaries without learner data."""
import http.client
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from progress_server import ProgressRequestHandler


class StubLab:
    def capabilities(self):
        return {"available": False, "label": "test fixture"}

    def catalog(self):
        return {"scenarios": []}

    def history(self):
        return {"attempts": []}

    def start(self, scenario_id, operation_id):
        return {"attempt": {"id": operation_id, "scenario_id": scenario_id}}


class WorkbenchHTTPTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        (root / "index.html").write_text("fixture")
        (root / "progress.html").write_text("legacy")
        (root / "private.json").write_text("private")
        (root / "practice_ui.js").symlink_to(root / "private.json")
        handler = type("PrivateTestHandler", (ProgressRequestHandler,), {"repo_root": root})
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.server.lab_manager = StubLab()
        self.server.lab_token = "test-browser-capability"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self, path, method="GET", body=None, headers=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        conn.request(method, path, body=body, headers=headers or {})
        response = conn.getresponse()
        result = response.status, dict(response.getheaders()), response.read()
        conn.close()
        return result

    def test_dns_rebinding_cross_origin_and_csrf_rejected(self):
        for headers in ({"Host": f"attacker.invalid:{self.port}"},
                        {"Origin": "https://attacker.invalid"},
                        {"Origin": "null"}, {"Sec-Fetch-Site": "cross-site"}):
            self.assertEqual(self.request("/api/lab/bootstrap", headers=headers)[0], 403)
        self.assertEqual(self.request("/api/lab/start", "POST", '{}',
                                      {"Content-Type": "text/plain"})[0], 400)

    def test_local_bootstrap_and_token_api_contract(self):
        status, headers, body = self.request("/api/lab/bootstrap")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["token"], self.server.lab_token)
        self.assertEqual(headers["Cache-Control"], "no-store")
        self.assertEqual(self.request("/api/lab/history")[0], 403)
        token = {"X-Lab-Token": self.server.lab_token}
        self.assertEqual(self.request("/api/lab/history", headers=token)[0], 200)
        headers = {**token, "Content-Type": "application/json"}
        self.assertEqual(self.request("/api/lab/start", "POST",
                                      json.dumps({"scenario_id": "example", "operation_id": "op"}), headers)[0], 200)
        self.assertEqual(self.request("/api/lab/start", "POST", '{}', headers)[0], 400)

    def test_static_scope_and_head_cannot_expose_private_or_symlink(self):
        for method in ("GET", "HEAD"):
            for path in ("/private.json", "/.git/config", "/scripts/progress_server.py",
                         "/.lab-runtime/attempts.json", "/practice_ui.js", "/%2e%2e/private.json"):
                self.assertEqual(self.request(path, method)[0], 404, (method, path))
        status, headers, body = self.request("/")
        self.assertEqual((status, body), (200, b"fixture"))
        self.assertEqual(headers["X-Frame-Options"], "DENY")
        self.assertNotIn("'unsafe-inline'", headers["Content-Security-Policy"].split("script-src")[1].split(";")[0])

    def test_finite_action_routes_keep_existing_token_boundary(self):
        for path in ("/api/lab/locate?scenario=media-wav-quality", "/api/lab/exports/"+'a'*64,
                     "/api/lab/attempts/"+'a'*32+"/wav"):
            self.assertEqual(self.request(path)[0], 403)
        token = {"X-Lab-Token": self.server.lab_token}
        self.assertEqual(self.request("/api/lab/exports/../private", headers=token)[0], 400)
        self.assertEqual(self.request("/api/lab/locate?scenario=a&scenario=b", headers=token)[0], 400)
        self.assertEqual(self.request("/api/lab/attempts/"+'a'*32+"/export-wav", "POST", '{}',
                                     {**token, "Content-Type": "application/json"})[0], 400)


if __name__ == "__main__":
    unittest.main()

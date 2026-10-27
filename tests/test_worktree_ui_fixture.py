"""Selector unit contracts; do not invoke or mutate the installed runtime."""
import os
import http.client
import json
from copy import deepcopy
from urllib.parse import urlparse
from pathlib import Path
from types import SimpleNamespace
import unittest
import tempfile
from unittest.mock import patch
from scripts import worktree_ui_fixture as runner


class SelectorTest(unittest.TestCase):
    def test_isolation_command_mounts_candidate_readonly_at_canonical(self):
        guard = SimpleNamespace(RUNTIME=Path('/runtime/csp'), CACHE=Path('/cache/csp'), TEMP=Path('/temp/csp'), VENV=Path('/runtime/csp/venv'))
        cmd = runner.command(guard)
        i = cmd.index(str(runner.SOURCE)); self.assertEqual(cmd[i-1:i+2], ['--ro-bind', str(runner.SOURCE), str(runner.ROOT)])
        for value in ('--unshare-net', '--unshare-pid', '--die-with-parent', '--remount-ro'): self.assertIn(value, cmd)
        self.assertNotIn('--share-net', cmd)
        self.assertEqual(cmd[-9:], ['unittest', 'discover', '-s', 'tests/ui', '-p', 'test_*.py', '-t', '.', '-v'])

    def test_environment_cannot_select_git_or_python_source(self):
        with patch.dict(os.environ, {'GIT_DIR': '/foreign', 'GIT_WORK_TREE': '/foreign', 'PYTHONPATH': '/foreign'}):
            self.assertFalse(any(k.startswith('GIT_') for k in runner.clean_environment()))
            self.assertNotIn('PYTHONPATH', runner.clean_environment())

    def test_unknown_action_never_loads_guard(self):
        with patch.object(runner, 'load_guard', side_effect=AssertionError('called')):
            self.assertEqual(runner.main(['--bootstrap']), 64)
            self.assertEqual(runner.main(['--ui-test', '/arbitrary']), 64)

    def test_foreign_common_directory_is_rejected(self):
        def require(ok, message):
            if not ok: raise RuntimeError(message)
        guard = SimpleNamespace(path_guard=lambda *a: None, require=require)
        with patch.object(runner.subprocess, 'check_output', return_value='/foreign/.git\n'):
            with self.assertRaisesRegex(RuntimeError, 'common directory'): runner.validate_source(guard)

    def test_gitdir_backlink_and_scope_negative_cases(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary); root = base/'canonical'; source = base/'candidate'
            common = root/'.git'; gitdir = common/'worktrees'/'candidate'
            gitdir.mkdir(parents=True); source.mkdir()
            (gitdir/'gitdir').write_text(str(source/'.git')+'\n')
            (source/'.git').write_text('gitdir: '+str(gitdir)+'\n')
            def require(ok, message):
                if not ok: raise RuntimeError(message)
            def path_guard(path, expected):
                require(not any(p.is_symlink() for p in [path, *path.parents]), 'symlink')
                require(path.resolve(strict=True) == expected, 'physical path')
            guard = SimpleNamespace(require=require, path_guard=path_guard)
            replies = {'common': str(common), 'top': str(source), 'dir': str(gitdir), 'entries': 'worktree '+str(source)+'\0'}
            def git(where, *args):
                if args[0] == 'worktree': return replies['entries']
                if args[-1] == '--git-common-dir': return replies['common']
                if args[-1] == '--show-toplevel': return replies['top']
                return str(common) if where == root else replies['dir']
            with patch.object(runner, 'ROOT', root), patch.object(runner, 'SOURCE', source):
                self.assertEqual(runner.validate_git_identity(guard, git), (common, gitdir))
                for key, bad, reason in [('top', str(root), 'root drift'), ('dir', str(common), 'outside'), ('entries', 'worktree '+str(root), 'unregistered')]:
                    old = replies[key]; replies[key] = bad
                    with self.assertRaisesRegex(RuntimeError, reason): runner.validate_git_identity(guard, git)
                    replies[key] = old
                (gitdir/'gitdir').write_text(str(root/'.git')+'\n')
                with self.assertRaisesRegex(RuntimeError, 'backlink'): runner.validate_git_identity(guard, git)
                (gitdir/'gitdir').write_text(str(source/'.git')+'\n')
                (source/'.git').write_text('gitdir: '+str(common)+'\n')
                with self.assertRaisesRegex(RuntimeError, 'pointer'): runner.validate_git_identity(guard, git)
                (source/'.git').unlink(); (source/'.git').symlink_to(gitdir/'gitdir')
                with self.assertRaisesRegex(RuntimeError, 'symlink'): runner.validate_git_identity(guard, git)

    def test_lock_mismatch_preserves_guard_rejection(self):
        def require(ok, message):
            if not ok: raise RuntimeError(message)
        guard = SimpleNamespace(require=require, path_guard=lambda *args: None)
        def data(path): return b'candidate' if str(path).startswith(str(runner.SOURCE)) else b'canonical'
        with patch.object(runner, 'validate_git_identity', return_value=(runner.ROOT/'.git', runner.ROOT/'.git/worktrees/candidate')), patch.object(Path, 'read_bytes', data):
            with self.assertRaisesRegex(RuntimeError, 'lock drift'): runner.validate_source(guard)


class PublicFixtureHTTPTest(unittest.TestCase):
    """Serve only synthetic temporary public data; no repository progress read."""
    @staticmethod
    def request(fixture, path, method="GET", body=None):
        address = urlparse(fixture.url)
        connection = http.client.HTTPConnection(address.hostname, address.port, timeout=3)
        try:
            connection.request(method, path, body=body)
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally: connection.close()

    def test_default_progress_uses_memory_delay_and_refuses_writes(self):
        from tests.ui import fixture_server
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            progress = {"version": 1, "revision": 7, "tasks": {}, "lanes": {}}
            source = root / "progress.json"; source.write_text(json.dumps(progress))
            with patch.object(fixture_server, "REPO_ROOT", root):
                with fixture_server.FixtureServer(progress_delay=.02) as fixture:
                    before = deepcopy(fixture.state["progress"])
                    # GET must not fall through to static reads, even if the
                    # original file changes after fixture initialization.
                    source.write_text("changed disk data must not be served")
                    disk_before = source.read_bytes()
                    with patch.object(fixture_server.time, "sleep") as delay:
                        status, headers, body = self.request(fixture, "/progress.json?cache=1")
                    self.assertEqual(status, 200)
                    self.assertEqual(json.loads(body), progress)
                    self.assertIn("no-store", headers["Cache-Control"])
                    delay.assert_called_once_with(.02)
                    for method in ("POST", "PUT", "PATCH", "DELETE"):
                        self.assertEqual(self.request(fixture, "/progress.json", method, "{}")[0], 405)
                    self.assertEqual(fixture.state["progress"], before)
                    self.assertEqual(fixture.state["operations"], {})
                    self.assertEqual(fixture.state["events"], [])
                    self.assertEqual(source.read_bytes(), disk_before)

    def test_exact_readme_allowed_private_paths_and_links_denied_for_get_head(self):
        from tests.ui import fixture_server
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root/"progress.json").write_text(json.dumps({"version": 1, "revision": 0, "tasks": {}, "lanes": {}}))
            readme = root/"plans/linux/README.md"; readme.parent.mkdir(parents=True)
            readme.write_text("# Synthetic public Linux plan\n")
            forbidden = [".git/config", "docs/pch-rebuild-20261020/.source51-inputs/original-task.json",
                         "private.json", "plans/linux/other.md"]
            for relative in forbidden:
                path = root/relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("synthetic private")
            with patch.object(fixture_server, "REPO_ROOT", root):
                with fixture_server.FixtureServer() as fixture:
                    self.assertEqual(self.request(fixture, "/plans/linux/README.md?cache=1")[2], readme.read_bytes())
                    for method in ("GET", "HEAD"):
                        self.assertEqual(self.request(fixture, "/plans/linux/README.md", method)[0], 200)
                        for target in ["/"+x for x in forbidden] + ["/plans/", "/plans/linux/", "/plans/linux/../other.md", "/%2e%2e/private.json"]:
                            self.assertEqual(self.request(fixture, target, method)[0], 404, (method, target))
                    readme.unlink(); readme.symlink_to(root/"private.json")
                    for method in ("GET", "HEAD"):
                        self.assertEqual(self.request(fixture, "/plans/linux/README.md", method)[0], 404)

    def test_sixteen_declared_scripts_are_read_only_and_adjacent_files_denied(self):
        from tests.ui import fixture_server
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root/"progress.json").write_text(json.dumps({"version": 1, "revision": 0, "tasks": {}, "lanes": {}}))
            declared = [f"rounds/{round_id}/{leaf}" for round_id in ("round_00", "round_01", "round_02", "round_06")
                        for leaf in ("week1/exercises.sh", "week2/exercises.sh", "week3/exercises.sh", "final/comprehensive_exercise.sh")]
            self.assertEqual(len(declared), 16)
            original = {}
            for relative in declared:
                path = root/relative; path.parent.mkdir(parents=True, exist_ok=True)
                original[relative] = ("# Synthetic public source; reading must not execute: " + relative + "\n").encode()
                path.write_bytes(original[relative])
            forbidden = ["rounds/round_00/week1/adjacent.sh", "rounds/round_06/week1/private.sh",
                         "rounds/round_00/week4/exercises.sh", "rounds/round_03/week1/exercises.sh",
                         "rounds/round_06/final/exercises.sh", "rounds/round_00/week1/exercises.sh.bak",
                         ".git/config", "docs/pch-rebuild-20261020/.source51-inputs/original-task.json"]
            for relative in forbidden:
                path = root/relative; path.parent.mkdir(parents=True, exist_ok=True); path.write_text("synthetic private")
            with patch.object(fixture_server, "REPO_ROOT", root):
                with fixture_server.FixtureServer() as fixture:
                    for relative in declared:
                        for method in ("GET", "HEAD"):
                            status, headers, body = self.request(fixture, "/"+relative+"?cache=1", method)
                            self.assertEqual(status, 200, (method, relative))
                            self.assertEqual(int(headers["Content-Length"]), len(original[relative]))
                            self.assertEqual(body, original[relative] if method == "GET" else b"")
                        self.assertEqual(self.request(fixture, "/"+relative, "POST", "{}")[0], 405)
                        self.assertEqual((root/relative).read_bytes(), original[relative])
                    for method in ("GET", "HEAD"):
                        for target in ["/"+x for x in forbidden] + ["/rounds/round_00/week1/", "/rounds/round_00/week1/../week2/exercises.sh", "/rounds/round_00/week1/%2e%2e/week2/exercises.sh", "/prefix/rounds/round_00/week1/exercises.sh"]:
                            self.assertEqual(self.request(fixture, target, method)[0], 404, (method, target))
                    leaf = root/"rounds/round_00/week1/exercises.sh"
                    leaf.unlink(); leaf.symlink_to(root/forbidden[0])
                    parent = root/"rounds/round_06/week3"
                    parent.rename(parent.with_name("hidden-week3")); parent.symlink_to(parent.with_name("hidden-week3"), target_is_directory=True)
                    for method in ("GET", "HEAD"):
                        for target in ("/rounds/round_00/week1/exercises.sh", "/rounds/round_06/week3/exercises.sh"):
                            self.assertEqual(self.request(fixture, target, method)[0], 404)
                    self.assertEqual(fixture.state["run_execution_count"], 0)
                    self.assertEqual(fixture.state["events"], [])
                    self.assertEqual(fixture.state["operations"], {})
                    self.assertEqual(fixture.state["progress"]["revision"], 0)

    def test_task_action_progress_plan_still_uses_existing_response_semantics(self):
        from tests.ui import fixture_server
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root/"progress.json").write_text(json.dumps({"version": 1, "revision": 7, "tasks": {}, "lanes": {}}))
            with patch.object(fixture_server, "REPO_ROOT", root):
                with fixture_server.FixtureServer(task_actions=True, progress_plan=[{"response_overrides": {"revision": 12}}]) as fixture:
                    first = self.request(fixture, "/progress.json")
                    second = self.request(fixture, "/progress.json")
                    self.assertEqual(first[0], 200); self.assertEqual(second[0], 200)
                    self.assertEqual(json.loads(first[2])["revision"], 12)
                    self.assertEqual(json.loads(second[2])["revision"], 7)
                    self.assertEqual(fixture.state["events"], [])


if __name__ == '__main__': unittest.main()

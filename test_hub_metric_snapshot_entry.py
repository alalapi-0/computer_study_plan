"""The Hub snapshot reader must stay explicit and refuse unsafe roots without any Hub checkout."""
import importlib.util
import unittest
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "scripts/export_hub_metric_snapshot.py"


def load_entry():
    spec = importlib.util.spec_from_file_location("study_hub_export", ENTRY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HubSnapshotEntryTests(unittest.TestCase):
    def test_entry_requires_both_explicit_roots(self):
        module = load_entry()
        for argv in ([], ["--hub-root", str(ENTRY.parent)], ["--project-root", str(ENTRY.parent)]):
            with self.assertRaises(SystemExit) as exit_info:
                module.main(argv)
            self.assertEqual(exit_info.exception.code, 2)

    def test_entry_refuses_symlinked_or_absent_project_root(self):
        module = load_entry()
        hub_root = Path(self._tempdir())
        project = hub_root / "project"
        project.mkdir()
        alias = hub_root / "alias"
        alias.symlink_to(project, target_is_directory=True)
        self.assertEqual(module.main(["--hub-root", str(hub_root), "--project-root", str(alias)]), 2)
        self.assertEqual(
            module.main(["--hub-root", str(hub_root), "--project-root", str(hub_root / "absent")]),
            2,
        )

    def test_missing_hub_root_is_reported_not_guessed(self):
        module = load_entry()
        with self.assertRaises(FileNotFoundError):
            module.main(["--hub-root", "/tmp/study-absent-hub", "--project-root", "/tmp"])

    def _tempdir(self):
        import tempfile
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return temporary.name


# All new fixture data is synthetic. TemporaryDirectory honors the invoking
# process's TMPDIR; no PCH_TEST_TMP, Hub checkout, or real study data is required.
import contextlib
import copy
import hashlib
import io
import json
import os
import tempfile
import types
from unittest import mock

WHEN = "2026-01-02T00:00:00+00:00"
LATER = "2026-01-02T01:00:00+00:00"
CONTEXT = hashlib.sha256(b"synthetic-permission-v1+synthetic-contract-v1").hexdigest()
VISION = """# Product Vision · 真实问题驱动

组织单位是一个实际问题：观察、修复、检查。
Linux是首版运行环境；保留历史课程。
"""
STATE = """# Project State

## 实现事实与阶段
|范围|当前事实|
|---|---|
|P1|PTY、修复、检查、重置|
|P2|状态/证据和提示|
|P2发布|版本化题包|
|R15|小WAV产物；不代表听觉接受|

## 进度核算（冻结前快照）
本轮尚未闭合。旧课程0/80。

## 候选注册与审查
C2已闭合；LOCAL_TECHNICAL_DELIVERED。

## Hub 当前管理映射
Status: active
Objective: Linux问题工作台
Phase: LOCAL_TECHNICAL_DELIVERED
Next action: TASK-PROBLEM-SERVICES待实施

## 私有历史（不可投影）
SYNTHETIC_PRIVATE_SENTINEL
"""


class SourceFixture(unittest.TestCase):
    def setUp(self):
        self.module = load_entry()
        self.assertEqual(Path(self.module.__file__), ENTRY)
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.code = self.root / "candidate"
        self.data = self.root / "metadata"
        for root in (self.code, self.data):
            root.mkdir()
        # A synthetic Git common tree and linked-worktree metadata, no Git calls.
        common = self.data / ".git"
        common.mkdir()
        (common / "HEAD").write_text("a" * 40 + "\n")
        worktree = common / "worktrees" / "candidate"
        worktree.mkdir(parents=True)
        (worktree / "HEAD").write_text("a" * 40 + "\n")
        (worktree / "commondir").write_text("../..\n")
        (worktree / "gitdir").write_text(str(self.code / ".git") + "\n")
        (self.code / ".git").write_text("gitdir: " + str(worktree) + "\n")
        for name, text in (("README.md", "# Synthetic problem workbench\n"),
                           ("docs/PRODUCT_VISION.md", VISION),
                           ("docs/PROJECT_STATE.md", STATE),
                           ("docs/NEXT_ACTIONS.md", "# Queue\nTASK-PROBLEM-SERVICES\n"),
                           ("content/scenarios/publication.json", '{"schema_version":1,"scenarios":{}}\n')):
            path = self.data / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        (self.code / "scripts").mkdir()
        self.entry = self.code / self.module.ENTRY_PATH
        self.entry.write_bytes(ENTRY.read_bytes())
        declaration = ENTRY.parent.parent / "hub.connection.yaml"
        (self.code / "hub.connection.yaml").write_bytes(declaration.read_bytes())
        # The module itself always imports from ENTRY. Only its trusted root
        # binding is substituted for this synthetic filesystem fixture.
        patch = mock.patch.object(self.module, "_ENTRY_FILE", self.entry)
        patch.start()
        self.addCleanup(patch.stop)

    def capture(self, when=WHEN):
        return self.module.capture_source(self.code, self.data, observed_at=when)

    def valid(self, when=WHEN):
        projection = self.capture(when)
        self.assertTrue(projection["available"], projection.get("error"))
        return projection

    def event(self, projection, previous=None):
        return self.module.make_event(projection, expected_previous_version=previous, context=CONTEXT)

    def reduce(self, state, event, previous=None, expected=None, now=LATER, context=CONTEXT):
        if expected is None and isinstance(event, dict):
            expected = event.get("source_version")
        return self.module.reduce_event(state, event, expected_previous_version=previous,
                                        context=context, expected_source_version=expected, now=now)

    def test_actual_five_facts_and_exact_public_provenance(self):
        p = self.valid()
        self.assertEqual(set(p["facts"]), set(self.module.FACT_NAMES))
        facts = p["facts"]
        self.assertIn("Linux", facts["purpose"]["value"])
        self.assertEqual(facts["current_work"]["value"]["phase"], "LOCAL_TECHNICAL_DELIVERED")
        self.assertEqual(facts["next_action"]["value"], "TASK-PROBLEM-SERVICES待实施")
        self.assertIsNone(facts["actor"]["value"])
        self.assertIn("not_published", facts["actor"]["unknown"])
        self.assertIn("small_wav_practice_artifact", facts["outputs"]["value"])
        serialized = json.dumps(p, ensure_ascii=False)
        for private in (str(self.root), "SYNTHETIC_PRIVATE_SENTINEL", "尚未闭合", "0/80"):
            self.assertNotIn(private, serialized)
        for fact in facts.values():
            source = fact["source"]
            self.assertEqual(source["content_sha256"], hashlib.sha256((self.data / source["path"]).read_bytes()).hexdigest())
            self.assertIn("heading", source["locator"])
        self.assertEqual(p["output_semantics"], "documented_types_not_existence_or_acceptance")

    def test_fences_wrong_headings_and_nested_labels_do_not_override(self):
        state = self.data / "docs/PROJECT_STATE.md"
        state.write_text("```md\n## Hub 当前管理映射\nStatus: fake\n```\n" + STATE +
                         "\n## Unrelated\nStatus: fake\n### Hub 当前管理映射\nNext action: fake\n")
        self.assertEqual(self.valid()["facts"]["current_work"]["value"]["status"], "active")
        state.write_text(STATE.replace("Status: active", "### Wrong scope\nStatus: active"))
        self.assertFalse(self.capture()["available"])

    def test_duplicates_missing_ambiguous_and_unclosed_fence_fail(self):
        state = self.data / "docs/PROJECT_STATE.md"
        cases = [STATE.replace("Status: active", "Status: active\nStatus: other"),
                 STATE + "\n## Hub 当前管理映射\nStatus: fake\n",
                 STATE.replace("Next action: TASK-PROBLEM-SERVICES待实施", ""),
                 STATE + "\n```\n", STATE.replace("## 实现事实与阶段", "## Different")]
        for text in cases:
            with self.subTest(text=text[:40]):
                state.write_text(text)
                self.assertFalse(self.capture()["available"])

    def test_missing_invalid_utf8_and_oversize_are_unavailable(self):
        path = self.data / "README.md"
        for data in (b"\xff", b"x" * (self.module.MAX_FILE_BYTES + 1)):
            path.write_bytes(data)
            p = self.capture()
            self.assertFalse(p["available"])
            self.assertIsNone(p["source_version"])
            self.assertNotIn(str(self.root), json.dumps(p))
        path.unlink()
        self.assertFalse(self.capture()["available"])

    def test_no_runtime_reads_no_writes_and_optional_publication(self):
        forbidden = self.data / "progress.json"
        forbidden.write_bytes(b"DO_NOT_READ")
        original = self.module._read
        seen = []
        def traced(fd, relative, **kwargs):
            seen.append(relative)
            self.assertNotIn(relative, ("progress.json", ".hub/status.json", ".lab-runtime/attempts.json"))
            self.assertFalse(relative.startswith("records/"))
            return original(fd, relative, **kwargs)
        before = {str(p.relative_to(self.data)): p.read_bytes() for p in self.data.rglob("*") if p.is_file()}
        with mock.patch.object(self.module, "_read", side_effect=traced):
            self.valid()
        after = {str(p.relative_to(self.data)): p.read_bytes() for p in self.data.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((self.data / ".hub").exists())
        (self.data / self.module.PUBLICATION).unlink()
        p = self.valid()
        entry = next(x for x in p["binding"]["input_manifest"] if x["path"] == self.module.PUBLICATION)
        self.assertEqual(entry["status"], "unknown_optional_missing")
        self.assertIsNone(entry["sha256"])

    def test_symlink_hardlink_parent_alias_and_escape_rejected(self):
        path = self.data / "README.md"
        original = path.read_bytes()
        external = self.root / "external"
        external.write_bytes(original)
        path.unlink()
        path.symlink_to(external)
        self.assertFalse(self.capture()["available"])
        path.unlink()
        os.link(external, path)
        self.assertFalse(self.capture()["available"])
        path.unlink()
        path.write_bytes(original)
        alias = self.root / "alias"
        alias.symlink_to(self.data, target_is_directory=True)
        self.assertFalse(self.module.capture_source(self.code, alias, observed_at=WHEN)["available"])
        self.assertFalse(self.module.capture_source(self.code, str(self.data) + "/../metadata", observed_at=WHEN)["available"])
        docs = self.data / "docs"
        moved = self.root / "moved-docs"
        docs.rename(moved)
        docs.symlink_to(moved, target_is_directory=True)
        self.assertFalse(self.capture()["available"])
        fd, _ = self.module._root(self.data)
        try:
            with self.assertRaises(self.module.SourceUnavailable):
                self.module._read(fd, "../external")
        finally:
            os.close(fd)

    def test_git_common_root_and_code_mismatch(self):
        marker = self.code / ".git"
        marker.unlink()
        marker.mkdir()
        (marker / "HEAD").write_text("a" * 40)
        self.assertFalse(self.capture()["available"])

    def test_code_binding_rejects_changed_import_or_different_root(self):
        self.entry.write_bytes(self.entry.read_bytes() + b"\n# changed\n")
        self.assertEqual(self.capture()["error"], "exporter_code_changed_since_import")
        self.entry.write_bytes(ENTRY.read_bytes())
        with mock.patch.object(self.module, "_ENTRY_FILE", self.root / "wrong.py"):
            self.assertEqual(self.capture()["error"], "exporter_code_path_mismatch")

    def test_double_capture_detects_edit_and_same_bytes_replacement(self):
        original = self.module._capture_once
        calls = []
        def change_after_first(*args):
            result = original(*args)
            calls.append(1)
            if len(calls) == 1:
                path = self.data / "README.md"
                raw = path.read_bytes()
                path.unlink()
                path.write_bytes(raw)
            return result
        with mock.patch.object(self.module, "_capture_once", side_effect=change_after_first):
            self.assertEqual(self.capture()["error"], "double_capture_drift")

    def test_parent_replacement_during_read_is_rejected(self):
        original = self.module.os.read
        changed = []
        def replace_after_read(fd, size):
            raw = original(fd, size)
            if raw.startswith(VISION.encode()) and not changed:
                changed.append(1)
                docs = self.data / "docs"
                docs.rename(self.root / "old-docs")
                docs.mkdir()
            return raw
        with mock.patch.object(self.module.os, "read", side_effect=replace_after_read):
            self.assertFalse(self.capture()["available"])

    def test_same_head_content_declaration_publication_and_code_versions(self):
        p = self.valid()
        version = p["source_version"]
        self.assertEqual(version, self.valid(LATER)["source_version"])
        for path in (self.data / "README.md", self.code / "hub.connection.yaml", self.data / self.module.PUBLICATION):
            original = path.read_bytes()
            path.write_bytes(original + b"\n")
            updated = self.valid()
            self.assertEqual(updated["binding"]["code_head"], p["binding"]["code_head"])
            self.assertNotEqual(updated["source_version"], version)
            path.write_bytes(original)
        original_entry = self.entry.read_bytes()
        changed = original_entry + b"\n# new candidate\n"
        try:
            self.entry.write_bytes(changed)
            with mock.patch.object(self.module, "_LOADED_CODE_SHA", hashlib.sha256(changed).hexdigest()):
                self.assertNotEqual(self.valid()["source_version"], version)
        finally:
            self.entry.write_bytes(original_entry)
        path = self.data / "README.md"
        path.write_bytes(b"line\r\n")
        v1 = self.valid()["source_version"]
        path.write_bytes(b"line\n")
        self.assertNotEqual(v1, self.valid()["source_version"])

    def test_source_only_cli_does_not_import_hub_or_write_snapshot(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            result = self.module.main(["--hub-root", str(self.root), "--project-root", str(self.data), "--source-only"])
        self.assertEqual(result, 0)
        self.assertTrue(json.loads(out.getvalue())["available"])
        self.assertFalse((self.data / ".hub").exists())
        self.assertEqual(Path(self.module.__file__), ENTRY)

    def test_event_new_duplicate_no_reemit_and_once_updated(self):
        first = self.valid()
        event = self.event(first)
        state = self.reduce({}, event)
        self.assertEqual(state["last_result"], "applied")
        self.assertEqual(state["receipt_scope"], "local_source_engineering_only")
        self.assertIsNone(self.event(self.valid(LATER), first["source_version"]))
        duplicate = self.reduce(state, event, previous=first["source_version"])
        self.assertEqual(duplicate["last_result"], "duplicate")
        self.assertEqual(duplicate["observed_at"], WHEN)
        (self.data / "README.md").write_text("semantic revision")
        second = self.valid(LATER)
        updated = self.reduce(state, self.event(second, first["source_version"]), previous=first["source_version"])
        self.assertEqual(updated["last_result"], "applied")
        self.assertEqual(len(updated["seen_versions"]), 2)
        self.assertEqual(state["source_version"], first["source_version"])

    def test_failure_context_cas_payload_and_staleness_retain_last_good(self):
        p = self.valid()
        event = self.event(p)
        good = self.reduce({}, event)
        changed = copy.deepcopy(event)
        changed["payload"]["facts"]["purpose"]["value"] = "forged"
        cases = [(changed, {}), ({"available": False, "error": "read failed"}, {}),
                 (event, {"context": "b" * 64}),
                 (event, {"now": "2025-01-01T00:00:00Z"}),
                 (event, {"now": "2027-01-01T00:00:00Z"}),
                 (event, {"expected": "b" * 64})]
        for bad, kwargs in cases:
            with self.subTest(kwargs=kwargs):
                result = self.reduce(good, bad, previous=p["source_version"], **kwargs)
                self.assertTrue(result["stale"])
                self.assertFalse(result["synced"])
                self.assertEqual(result["value"], good["value"])
        (self.data / "README.md").write_text("next revision")
        newer = self.valid(LATER)
        cas = self.reduce(good, self.event(newer), previous=p["source_version"])
        self.assertEqual(cas["error"], "compare_and_swap_conflict")
        self.assertEqual(cas["value"], good["value"])
        none = self.reduce(good, None, previous=p["source_version"], expected=p["source_version"], now="2027-01-01T00:00:00Z")
        self.assertTrue(none["stale"])

    def test_old_version_cannot_rollback_even_with_new_time(self):
        p = self.valid()
        good = self.reduce({}, self.event(p))
        (self.data / "README.md").write_text("next revision")
        new = self.valid(LATER)
        good2 = self.reduce(good, self.event(new, p["source_version"]), previous=p["source_version"])
        old = copy.deepcopy(p)
        old["observed_at"] = LATER
        rollback = self.reduce(good2, self.event(old, new["source_version"]), previous=new["source_version"])
        self.assertEqual(rollback["error"], "old_version")
        self.assertEqual(rollback["value"], good2["value"])

    def test_unavailable_invalid_time_context_and_tampered_binding(self):
        self.assertFalse(self.capture("timezone missing")["available"])
        p = self.valid()
        self.assertFalse(self.module.make_event(p, expected_previous_version=None, context="unbound")["available"])
        for key in ("content_sha256", "declaration_sha256", "code_sha256"):
            bad = copy.deepcopy(p)
            bad["binding"][key] = "f" * 64
            bad["source_version"] = self.module._digest(bad["binding"])
            self.assertFalse(self.event(bad)["available"])

    def test_declaration_rejects_replaced_fallback_key_with_same_count(self):
        baseline = self.valid()
        declaration = self.code / "hub.connection.yaml"
        original = declaration.read_bytes()
        target = b"  current_work.round:"
        self.assertEqual(original.count(target), 1)
        changed = original.replace(target, b"  arbitrary.extension:", 1)
        for raw in (original, changed):
            fallbacks = raw.split(b"unknown_fields:\n", 1)[1].split(b"validation_entry:\n", 1)[0]
            self.assertEqual(len([line for line in fallbacks.splitlines() if line.startswith(b"  ")]), 21)
        try:
            declaration.write_bytes(changed)
            projection = self.capture()
            self.assertFalse(projection["available"])
            self.assertIsNone(projection["source_version"])
            self.assertEqual(projection["error"], "invalid_unknown_fallbacks")
        finally:
            declaration.write_bytes(original)
        self.assertEqual(self.valid()["source_version"], baseline["source_version"])

    def test_malformed_declaration_and_publication_are_unavailable(self):
        decl = self.code / "hub.connection.yaml"
        original = decl.read_bytes()
        decl.write_bytes(original + b"project_id: ambiguous\n")
        self.assertFalse(self.capture()["available"])
        decl.write_bytes(original)
        publication = self.data / self.module.PUBLICATION
        for raw in (b"{", b'{"schema_version":1,"schema_version":1}', b"[]"):
            publication.write_bytes(raw)
            self.assertFalse(self.capture()["available"])

    def test_source_event_digest_covers_extra_fields_and_provenance(self):
        p = self.valid()
        p["unexpected_raw_text"] = "SYNTHETIC_PRIVATE_SENTINEL"
        self.assertFalse(self.event(p)["available"])
        p = self.valid()
        p["facts"]["purpose"]["source"]["locator"]["unexpected"] = "raw"
        p["binding"]["facts_sha256"] = self.module._digest(p["facts"])
        p["source_version"] = self.module._digest(p["binding"])
        self.assertFalse(self.event(p)["available"])

    def test_git_head_content_change_changes_source_version(self):
        first = self.valid()
        (self.data / ".git/HEAD").write_text("b" * 40 + "\n")
        second = self.valid()
        self.assertEqual(first["binding"]["code_head"], second["binding"]["code_head"])
        self.assertNotEqual(first["binding"]["data_head"], second["binding"]["data_head"])
        self.assertNotEqual(first["source_version"], second["source_version"])

    def test_wrong_schema_and_context_payload_cannot_replace_last_good(self):
        p = self.valid()
        event = self.event(p)
        good = self.reduce({}, event)
        bad = copy.deepcopy(event)
        bad["schema_version"] = "different/2"
        result = self.reduce(good, bad, previous=p["source_version"])
        self.assertTrue(result["stale"])
        self.assertEqual(result["value"], good["value"])
        bad = copy.deepcopy(event)
        bad["context"] = "b" * 64
        bad["event_id"] = self.module._digest({k: v for k, v in bad.items() if k not in ("event_id", "observed_at")})
        self.assertEqual(self.reduce(good, bad, previous=p["source_version"])["error"], "wrong_event_context")


class LegacyExportABITests(unittest.TestCase):
    def test_default_keeps_registered_scope_study_spec_rows_and_single_clock(self):
        module = load_entry()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            project = root / "project"
            project.mkdir()
            old_rows = [{"metric_id": "study_tasks", "completed": 0, "total": 80}]
            spec = {"adapter": "study", "synthetic_spec": "unchanged"}
            management = {"success": True, "synthetic": "management"}
            projects = {module.PROJECT_ID: {"root_path": str(project)}}
            refresh_mock = mock.Mock(return_value=management)
            calls = {}
            class Resolver:
                def __init__(self, given_root, *, clock):
                    self.projects = projects
                    calls["resolver"] = (given_root, clock())
                refresh = refresh_mock
            def export(project_arg, project_id, collectors, **kwargs):
                calls["export"] = (project_arg, project_id, kwargs)
                calls["rows"] = collectors["records"](project_arg, project_id, kwargs["clock"]())
            clock = mock.Mock(return_value=WHEN)
            collector = mock.Mock(return_value=old_rows)
            validate = mock.Mock()
            readers = mock.Mock(return_value=({"projects": {module.PROJECT_ID: spec}}, None))
            modules = {"hub": types.ModuleType("hub")}
            for name, values in {
                "connection_sources": {"SourceResolver": Resolver},
                "metric_collect": {"validate_metric_source_config": validate},
                "metric_documents": {"collect_study": collector},
                "metric_export": {"export_metric_snapshot": export},
                "metric_sources": {"read_structured": readers},
                "metrics": {"utcnow": clock},
            }.items():
                child = types.ModuleType("hub." + name)
                child.__dict__.update(values)
                modules[child.__name__] = child
            with mock.patch.dict("sys.modules", modules), mock.patch.object(module.sys, "path", list(module.sys.path)):
                self.assertEqual(module.main(["--hub-root", str(root), "--project-root", str(project)]), 0)
                clock.assert_called_once_with()
                collector.assert_called_once_with(project, module.PROJECT_ID, WHEN, spec)
                self.assertIs(calls["rows"], old_rows)
                self.assertEqual(calls["resolver"], (root, WHEN))
                kwargs = calls["export"][2]
                self.assertEqual(kwargs["exporter_id"], "computer-study-plan-export")
                self.assertEqual(kwargs["exporter_version"], "1.0")
                self.assertIs(kwargs["management"], management)
                readers.assert_called_once_with(root, "data/connections/metric_sources.yaml")
                validate.assert_called_once_with({"projects": {module.PROJECT_ID: spec}}, projects)
                refresh_mock.assert_called_once_with(module.PROJECT_ID)
                # A caller cannot substitute another root or adapter to widen reads.
                other = root / "other"
                other.mkdir()
                self.assertEqual(module.main(["--hub-root", str(root), "--project-root", str(other)]), 2)
                spec["adapter"] = "other"
                self.assertEqual(module.main(["--hub-root", str(root), "--project-root", str(project)]), 2)
                self.assertEqual(collector.call_count, 1)


class GraphSourceEntryTests(unittest.TestCase):
    def setUp(self):
        self.module = load_entry()
        self.assertEqual(Path(self.module.__file__), ENTRY)
        self.helper = self.module._load_graph_helper()
        self.assertEqual(Path(self.helper.__file__), ENTRY.parent / "study_hub_graph.py")
        self.document = self.helper.native_document(catalog={"scenarios": []}, history={"revision": 0, "attempts": []},
            environments={}, source01_version="a" * 64, native_code_sha256="b" * 64)
        self.context = self.helper.make_context(self.document, exporter_sha256=self.module._LOADED_CODE_SHA,
                                              permission_version="c" * 64, minimum_revision=0)

    def invoke(self, raw):
        stream = io.TextIOWrapper(io.BytesIO(raw), encoding="utf-8")
        with tempfile.TemporaryDirectory() as hub, mock.patch.object(self.module.sys, "stdin", stream), contextlib.redirect_stdout(io.StringIO()) as out:
            code = self.module.main(["--hub-root", hub, "--project-root", str(ENTRY.parent.parent), "--graph-source-only"])
        return code, json.loads(out.getvalue())

    def test_graph_stdin_uses_exact_helper_despite_module_cache(self):
        bundle = {"document": self.document, "context": self.context, "observed_at": WHEN}
        poison = types.ModuleType("study_hub_graph")
        with mock.patch.dict("sys.modules", {"study_hub_graph": poison, "scripts.study_hub_graph": poison}):
            code, result = self.invoke(json.dumps(bundle).encode())
        self.assertEqual(code, 0)
        self.assertTrue(result["available"])
        self.assertEqual(result["graph"]["objects"], [])
        self.assertEqual(result["context"]["helper_sha256"], hashlib.sha256((ENTRY.parent / "study_hub_graph.py").read_bytes()).hexdigest())

    def test_graph_stdin_invalid_private_context_and_limits_rejected(self):
        bundle = {"document": self.document, "context": self.context, "observed_at": WHEN}
        bad = copy.deepcopy(bundle)
        bad["document"]["token"] = "SYNTHETIC_PRIVATE"
        wrong = copy.deepcopy(bundle)
        wrong["context"]["exporter_sha256"] = "0" * 64
        for raw in (b"{", b"\xff", b'{"document":1,"document":2}', b"x" * (self.helper.MAX_DOCUMENT_BYTES + 1),
                    json.dumps(bad).encode(), json.dumps(wrong).encode()):
            code, result = self.invoke(raw)
            self.assertEqual(code, 2)
            self.assertFalse(result["available"])
            self.assertNotIn("SYNTHETIC_PRIVATE", json.dumps(result))

    def test_graph_mode_mutually_exclusive_and_requires_both_roots(self):
        for argv in (["--graph-source-only"], ["--hub-root", str(ENTRY.parent), "--graph-source-only"],
                     ["--hub-root", str(ENTRY.parent), "--project-root", str(ENTRY.parent.parent), "--graph-source-only", "--source-only"]):
            with self.assertRaises(SystemExit) as failure:
                self.module.main(argv)
            self.assertEqual(failure.exception.code, 2)

    def test_graph_loader_detects_code_drift_and_root_mismatch(self):
        original = self.module._read
        def altered(fd, name, **kwargs):
            raw, identity = original(fd, name, **kwargs)
            if name == self.module.ENTRY_PATH:
                raw += b"\n# drift\n"
            return raw, identity
        with mock.patch.object(self.module, "_read", side_effect=altered):
            with self.assertRaises(self.module.SourceUnavailable):
                self.module._load_graph_helper()
        with tempfile.TemporaryDirectory() as elsewhere, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(self.module._graph_source_stdin(Path(elsewhere)), 2)
            self.assertEqual(json.loads(out.getvalue())["error"], "graph_project_root_mismatch")


if __name__ == "__main__":
    unittest.main()

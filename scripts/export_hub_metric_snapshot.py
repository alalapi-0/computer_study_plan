"""Legacy study exporter plus a separate, read-only local SOURCE ABI.

The default CLI still refreshes registered study metrics through the Hub. Explicit
--source-only never imports the Hub or reads progress/records/runtime data. Local
facts/events are NOT declaration 2.0 wire fields, normal Hub adoption, OS isolation,
learning acceptance, or a persistent queue. Roots and event context are trusted
caller inputs, not permission grants. Context is a SHA-256 digest of the caller's
permission AND contract identities; callers must recompute it when either changes.
"""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys

PROJECT_ID = "computer-study-plan"
ADAPTER = "study"
SOURCE_SCHEMA = "computer-study-plan.source/1.2"
CONTRACT_VERSION = "local-source-1.2.0"
ENTRY_PATH = "scripts/export_hub_metric_snapshot.py"
_ENTRY_FILE = Path(__file__).absolute()
_LOADED_CODE_SHA = hashlib.sha256(_ENTRY_FILE.read_bytes()).hexdigest()
MAX_FILE_BYTES = 256 * 1024
MAX_EVENT_BYTES = 64 * 1024
MAX_AGE_SECONDS = 604800
DATA_FILES = ("README.md", "docs/PRODUCT_VISION.md", "docs/PROJECT_STATE.md", "docs/NEXT_ACTIONS.md")
PUBLICATION = "content/scenarios/publication.json"
FACT_NAMES = ("purpose", "outputs", "current_work", "actor", "next_action")
_SHA = re.compile(r"[0-9a-f]{64}\Z")


class SourceUnavailable(ValueError):
    """A public, path-free reason; never include raw source or OS exception text."""


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _digest(value):
    return _sha(_json(value))


def _identity(st):
    return (st.st_dev, st.st_ino, st.st_mode, st.st_nlink, st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def _root(path):
    """Open each ancestor without following links; reject caller aliases."""
    raw = os.fspath(path)
    if not os.path.isabs(raw) or raw != os.path.normpath(raw) or raw.startswith("//"):
        raise SourceUnavailable("root_alias")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    chain = []
    try:
        for part in Path(raw).parts[1:]:
            nxt = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = nxt
            st = os.fstat(fd)
            chain.append((st.st_dev, st.st_ino))
        return fd, tuple(chain)
    except BaseException:
        os.close(fd)
        raise


def _read(fd, relative, *, optional=False, limit=MAX_FILE_BYTES):
    """Bounded descriptor-relative read, parent/leaf recheck, no links or FIFOs."""
    parts = relative.split("/")
    if not parts or any(p in ("", ".", "..") for p in parts):
        raise SourceUnavailable("unsafe_relative_path")
    opened = []
    parent_checks = []
    current = fd
    leaf = None
    try:
        for part in parts[:-1]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            st = os.fstat(child)
            parent_checks.append((current, part, (st.st_dev, st.st_ino)))
            opened.append(child)
            current = child
        leaf = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=current)
        before = os.fstat(leaf)
        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > limit:
            raise SourceUnavailable("unsafe_or_oversize_file")
        chunks, size = [], 0
        while True:
            chunk = os.read(leaf, min(65536, limit + 1 - size))
            if not chunk:
                break
            chunks.append(chunk)
            size += len(chunk)
            if size > limit:
                raise SourceUnavailable("oversize_file")
        raw = b"".join(chunks)
        after = os.fstat(leaf)
        named = os.stat(parts[-1], dir_fd=current, follow_symlinks=False)
        if _identity(before) != _identity(after) or _identity(after) != _identity(named) or len(raw) != after.st_size:
            raise SourceUnavailable("file_drift")
        for parent, name, identity in parent_checks:
            st = os.stat(name, dir_fd=parent, follow_symlinks=False)
            if not stat.S_ISDIR(st.st_mode) or (st.st_dev, st.st_ino) != identity:
                raise SourceUnavailable("parent_drift")
        raw.decode("utf-8", errors="strict")
        return raw, (_identity(after), tuple(x[2] for x in parent_checks))
    except FileNotFoundError:
        if optional:
            return None, None
        raise SourceUnavailable("missing_required_file") from None
    finally:
        if leaf is not None:
            os.close(leaf)
        for child in reversed(opened):
            os.close(child)


def _git(root, fd):
    """Read only Git identity metadata, never spawn git or read object bodies."""
    st = os.stat(".git", dir_fd=fd, follow_symlinks=False)
    signatures = []
    if stat.S_ISDIR(st.st_mode):
        gitdir = Path(root) / ".git"
    else:
        marker, sig = _read(fd, ".git", limit=4096)
        signatures.append((marker, sig))
        text = marker.decode().strip()
        if not text.startswith("gitdir: ") or "\n" in text:
            raise SourceUnavailable("invalid_git_marker")
        gitdir = Path(os.path.normpath(os.path.join(root, text[8:])))
    gfd, gchain = _root(gitdir)
    cfd = None
    try:
        common_raw, sig = _read(gfd, "commondir", optional=True, limit=4096)
        signatures.append((common_raw, sig))
        if common_raw is None:
            common = gitdir
        else:
            common_text = common_raw.decode().strip()
            if not common_text or "\n" in common_text:
                raise SourceUnavailable("invalid_git_common")
            common = Path(os.path.normpath(os.path.join(gitdir, common_text)))
            backlink, backsig = _read(gfd, "gitdir", limit=4096)
            if backlink.decode().strip() != str(Path(root) / ".git"):
                raise SourceUnavailable("git_root_mismatch")
            signatures.append((backlink, backsig))
        cfd, cchain = _root(common)
        head_raw, sig = _read(gfd, "HEAD", limit=4096)
        signatures.append((head_raw, sig))
        head = head_raw.decode().strip()
        if head.startswith("ref: "):
            ref = head[5:]
            if not re.fullmatch(r"refs/heads/[A-Za-z0-9_./-]+", ref) or any(x in ("", ".", "..") for x in ref.split("/")):
                raise SourceUnavailable("invalid_git_ref")
            raw, sig = _read(cfd, ref, optional=True, limit=4096)
            signatures.append((raw, sig))
            if raw is not None:
                head = raw.decode().strip()
            else:
                packed, sig = _read(cfd, "packed-refs", limit=1024 * 1024)
                signatures.append((packed, sig))
                matches = [line.split()[0] for line in packed.decode().splitlines() if len(line.split()) == 2 and line.split()[1] == ref]
                if len(matches) != 1:
                    raise SourceUnavailable("missing_or_ambiguous_git_ref")
                head = matches[0]
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", head):
            raise SourceUnavailable("invalid_git_head")
        # Re-open directory chains to detect substitution while descriptors stay open.
        for path, chain in ((gitdir, gchain), (common, cchain)):
            check, actual = _root(path)
            os.close(check)
            if actual != chain:
                raise SourceUnavailable("git_parent_drift")
        cstat = os.fstat(cfd)
        return head, (cstat.st_dev, cstat.st_ino), (gchain, cchain, signatures)
    finally:
        os.close(gfd)
        if cfd is not None:
            os.close(cfd)


def _capture_once(code_root, data_root):
    cfd, cchain = _root(code_root)
    dfd = None
    try:
        dfd, dchain = _root(data_root)
        code_git, data_git = _git(code_root, cfd), _git(data_root, dfd)
        if code_git[1] != data_git[1]:
            raise SourceUnavailable("git_common_root_mismatch")
        if Path(code_root) / ENTRY_PATH != _ENTRY_FILE:
            raise SourceUnavailable("exporter_code_path_mismatch")
        blobs, identities = {}, {}
        for scope, path, rootfd, optional in (
            *(("data", name, dfd, False) for name in DATA_FILES),
            ("data", PUBLICATION, dfd, True),
            ("code", "hub.connection.yaml", cfd, False),
            ("code", ENTRY_PATH, cfd, False),
        ):
            raw, identity = _read(rootfd, path, optional=optional)
            blobs[(scope, path)] = raw
            identities[(scope, path)] = identity
        if _sha(blobs[("code", ENTRY_PATH)]) != _LOADED_CODE_SHA:
            raise SourceUnavailable("exporter_code_changed_since_import")
        for root, chain in ((code_root, cchain), (data_root, dchain)):
            check, actual = _root(root)
            os.close(check)
            if actual != chain:
                raise SourceUnavailable("root_or_parent_drift")
        if _git(code_root, cfd) != code_git or _git(data_root, dfd) != data_git:
            raise SourceUnavailable("git_identity_drift")
        return blobs, identities, (cchain, dchain, code_git, data_git)
    finally:
        os.close(cfd)
        if dfd is not None:
            os.close(dfd)


def _sections(text, title, level):
    """Exact headings outside fenced/indented code; duplicate sections fail closed."""
    lines, fence, headers = [], None, []
    for number, line in enumerate(text.splitlines(), 1):
        mark = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            if mark and mark[1][0] == fence[0] and len(mark[1]) >= len(fence) and not mark[2].strip():
                fence = None
            continue
        if mark:
            fence = mark[1]
            continue
        if line.startswith(("    ", "\t")):
            continue
        match = re.match(r"^ {0,3}(#{1,6}) +(.+?) *#* *$", line)
        if match:
            headers.append((len(lines), len(match[1]), match[2], number))
        lines.append((number, line))
    if fence:
        raise SourceUnavailable("unclosed_code_fence")
    matches = [h for h in headers if h[1:3] == (level, title)]
    if len(matches) != 1:
        raise SourceUnavailable("missing_or_ambiguous_section")
    start = matches[0]
    end = next((h[0] for h in headers if h[0] > start[0] and h[1] <= level), len(lines))
    # Nested headings are a different scope, never accepted as top-level labels.
    stop = next((h[0] for h in headers if start[0] < h[0] < end), end)
    return lines[start[0] + 1:stop]


def _public(value):
    if len(value) > 2048 or any(ord(c) < 32 for c in value):
        raise SourceUnavailable("invalid_public_value")
    if re.search(r"(?:^|[\s`(])(?:/[^\s]|~[/\\]|[A-Za-z]:[\\/])", value):
        raise SourceUnavailable("nonpublic_path_in_value")
    return value


def _fact(value, path, locator, raw, reason=None):
    return {"value": value, "unknown": reason, "source": {
        "path": path, "locator": locator, "content_sha256": _sha(raw)}}


def _five_facts(blobs):
    vision = blobs[("data", "docs/PRODUCT_VISION.md")]
    state = blobs[("data", "docs/PROJECT_STATE.md")]
    vision_lines = _sections(vision.decode(), "Product Vision · 真实问题驱动", 1)
    selected = []
    for prefix in ("组织单位是", "Linux是"):
        matches = [(n, s) for n, s in vision_lines if s.startswith(prefix)]
        if len(matches) != 1:
            raise SourceUnavailable("missing_or_ambiguous_purpose")
        selected.extend(matches)
    purpose = _fact(" ".join(_public(s) for _, s in selected), "docs/PRODUCT_VISION.md",
                    {"heading": "Product Vision · 真实问题驱动", "lines": [n for n, _ in selected]}, vision)
    capabilities = _sections(state.decode(), "实现事实与阶段", 2)
    types, locations = [], []
    # Types only: never copy table assertions about acceptance or file existence.
    for label, needles in (("versioned_scenario_packages", ("题包",)),
                           ("disposable_problem_workspace", ("PTY", "重置")),
                           ("attempt_checks_and_assistance_records", ("状态/证据", "提示")),
                           ("small_wav_practice_artifact", ("WAV", "产物"))):
        rows = [(n, line) for n, line in capabilities if line.startswith("|") and all(x in line for x in needles)]
        if len(rows) != 1:
            raise SourceUnavailable("missing_or_ambiguous_capability")
        types.append(label)
        locations.append(rows[0][0])
    outputs = _fact(types, "docs/PROJECT_STATE.md", {"heading": "实现事实与阶段", "lines": locations}, state)
    management = _sections(state.decode(), "Hub 当前管理映射", 2)
    labels, locations = {}, {}
    for label in ("Status", "Objective", "Phase", "Next action"):
        matches = [(n, s[len(label) + 1:].strip()) for n, s in management if s.startswith(label + ":")]
        if len(matches) != 1 or not matches[0][1]:
            raise SourceUnavailable("missing_or_duplicate_management_label")
        locations[label], labels[label] = matches[0][0], _public(matches[0][1])
    current = _fact({k: labels[v] for k, v in (("status", "Status"), ("objective", "Objective"), ("phase", "Phase"))},
                    "docs/PROJECT_STATE.md", {"heading": "Hub 当前管理映射", "labels": ["Status", "Objective", "Phase"],
                    "lines": [locations[x] for x in ("Status", "Objective", "Phase")]}, state)
    next_action = _fact(labels["Next action"], "docs/PROJECT_STATE.md",
                        {"heading": "Hub 当前管理映射", "label": "Next action", "lines": [locations["Next action"]]}, state)
    actor = _fact(None, "docs/PROJECT_STATE.md", {"heading": "Hub 当前管理映射", "label": "actor"},
                  state, "actor_not_published; management_active_is_not_native_goal_resume")
    return dict(zip(FACT_NAMES, (purpose, outputs, current, actor, next_action)))


def _validate_declaration(raw):
    """Validate the existing finite 2.0 declaration shape without a YAML loader.

    This local parser intentionally accepts the repository's simple declaration
    subset, not arbitrary YAML aliases/tags/merges or a new wire extension.
    """
    blocks, key = {}, None
    for line in raw.decode("utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"([a-z_]+):(?: (.*))?", line)
        if match:
            key = match[1]
            if key in blocks:
                raise SourceUnavailable("duplicate_declaration_key")
            blocks[key] = [match[2] or "", []]
        elif key is None or "\t" in line:
            raise SourceUnavailable("invalid_declaration")
        else:
            blocks[key][1].append(line)
    expected = {"schema_version", "project_id", "source_refs", "metric_export", "mapping",
                "unknown_fields", "validation_entry", "max_read_age_seconds"}
    if set(blocks) != expected or blocks["schema_version"][0] not in ("'2.0'", '"2.0"', "2.0") or blocks["project_id"][0] != PROJECT_ID:
        raise SourceUnavailable("invalid_declaration_contract")
    if blocks["source_refs"] != ["", ["- id: state", "  path: docs/PROJECT_STATE.md", "  format: markdown", "  role: current_state"]]:
        raise SourceUnavailable("invalid_declaration_source")
    if blocks["metric_export"] != ["", ["  entry: " + ENTRY_PATH, "  snapshot: .hub/status.json"]]:
        raise SourceUnavailable("invalid_declaration_exporter")
    lines = blocks["mapping"][1]
    if blocks["mapping"][0] or len(lines) != 24:
        raise SourceUnavailable("invalid_declaration_mapping")
    seen = set()
    labels = {"status": "Status", "objective": "Objective", "phase": "Phase", "next_action": "Next action"}
    for offset in range(0, len(lines), 6):
        group = lines[offset:offset + 6]
        match = re.fullmatch(r"  current_work\.(status|objective|phase|next_action):", group[0])
        if not match or match[1] in seen:
            raise SourceUnavailable("invalid_declaration_mapping")
        seen.add(match[1])
        if group[1:] != ["    source_ref: state", "    selector:", "      heading: Hub 当前管理映射",
                         "      label: " + labels[match[1]], "    value_map: null"]:
            raise SourceUnavailable("invalid_declaration_selector")
    fallbacks = []
    for line in blocks["unknown_fields"][1]:
        match = re.fullmatch(r"  ([a-z_.]+): (.+)", line)
        if not match:
            raise SourceUnavailable("invalid_unknown_fallback")
        fallbacks.append(match[1])
    expected_fallbacks = frozenset({
        "current_work.objective",
        "current_work.phase",
        "current_work.round",
        "current_work.status",
        "current_work.completed",
        "current_work.accepted",
        "current_work.next_action",
        "current_work.owner_role",
        "progress.completed",
        "progress.total",
        "progress.counting_basis",
        "progress.milestones",
        "blockers",
        "verification.status",
        "verification.evidence_refs",
        "verification.accepted_basis",
        "delivery.status",
        "delivery.remote",
        "delivery.branch",
        "delivery.commit",
        "delivery.receipt_ref",
    })
    if len(fallbacks) != 21 or len(set(fallbacks)) != 21 or frozenset(fallbacks) != expected_fallbacks:
        raise SourceUnavailable("invalid_unknown_fallbacks")


def _validate_publication(raw):
    if raw is None:
        return
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise SourceUnavailable("duplicate_publication_key")
            result[key] = value
        return result
    try:
        value = json.loads(raw, object_pairs_hook=unique)
    except (ValueError, RecursionError):
        raise SourceUnavailable("invalid_publication") from None
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise SourceUnavailable("invalid_publication_schema")


def _time(value):
    if not isinstance(value, str) or len(value) > 40:
        raise SourceUnavailable("invalid_time")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise SourceUnavailable("invalid_time") from None
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise SourceUnavailable("time_requires_timezone")
    return dt.astimezone(timezone.utc)


def capture_source(code_root, data_root, *, observed_at):
    """Capture fixed metadata from explicit roots in the same Git common tree.

    No caller-selected path list, collector, runtime access, publication writes,
    newline normalization, or absolute path disclosure. Failures have no version.
    """
    base = {"schema_version": SOURCE_SCHEMA, "contract_version": CONTRACT_VERSION,
            "project_id": PROJECT_ID, "observed_at": observed_at, "available": False,
            "source_version": None, "facts": {n: {"value": None, "unknown": "source_unavailable", "source": None} for n in FACT_NAMES},
            "scope": "local_source_engineering_only", "output_semantics": "documented_types_not_existence_or_acceptance"}
    try:
        _time(observed_at)
        first = _capture_once(code_root, data_root)
        second = _capture_once(code_root, data_root)
        if first != second:
            raise SourceUnavailable("double_capture_drift")
        blobs, _, roots = second
        manifest = [{"scope": scope, "path": path, "sha256": _sha(raw) if raw is not None else None,
                     "status": "present" if raw is not None else "unknown_optional_missing"}
                    for (scope, path), raw in sorted(blobs.items())]
        _validate_declaration(blobs[("code", "hub.connection.yaml")])
        _validate_publication(blobs[("data", PUBLICATION)])
        facts = _five_facts(blobs)
        binding = {"schema": SOURCE_SCHEMA, "contract": CONTRACT_VERSION,
                   "project_id": PROJECT_ID, "code_head": roots[2][0], "data_head": roots[3][0],
                   "code_sha256": _sha(blobs[("code", ENTRY_PATH)]),
                   "declaration_sha256": _sha(blobs[("code", "hub.connection.yaml")]),
                   "content_sha256": _digest([m for m in manifest if m["scope"] == "data"]),
                   "input_manifest": manifest, "facts_sha256": _digest(facts)}
        base.update(available=True, facts=facts, binding=binding, source_version=_digest(binding))
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        base["error"] = str(exc) if isinstance(exc, SourceUnavailable) else type(exc).__name__
    return base


def _valid_projection(p):
    if not isinstance(p, dict) or len(_json(p)) > MAX_EVENT_BYTES:
        raise SourceUnavailable("invalid_projection")
    if (p.get("project_id"), p.get("schema_version"), p.get("contract_version"), p.get("scope")) != (PROJECT_ID, SOURCE_SCHEMA, CONTRACT_VERSION, "local_source_engineering_only"):
        raise SourceUnavailable("wrong_projection_contract")
    if set(p) != {"schema_version", "contract_version", "project_id", "observed_at", "available",
                  "source_version", "facts", "scope", "output_semantics", "binding"}:
        raise SourceUnavailable("unexpected_projection_fields")
    if p["output_semantics"] != "documented_types_not_existence_or_acceptance":
        raise SourceUnavailable("invalid_output_semantics")
    _time(p.get("observed_at"))
    if p.get("available") is not True:
        raise SourceUnavailable("source_unavailable")
    binding = p.get("binding")
    if not isinstance(binding, dict) or p.get("source_version") != _digest(binding):
        raise SourceUnavailable("invalid_source_binding")
    if (binding.get("project_id"), binding.get("schema"), binding.get("contract"), binding.get("code_sha256")) != (PROJECT_ID, SOURCE_SCHEMA, CONTRACT_VERSION, _LOADED_CODE_SHA):
        raise SourceUnavailable("wrong_code_or_contract")
    if set(p.get("facts", {})) != set(FACT_NAMES) or binding.get("facts_sha256") != _digest(p["facts"]):
        raise SourceUnavailable("invalid_facts_binding")
    if set(binding) != {"schema", "contract", "project_id", "code_head", "data_head", "code_sha256",
                        "declaration_sha256", "content_sha256", "input_manifest", "facts_sha256"}:
        raise SourceUnavailable("unexpected_binding_fields")
    for name in ("code_head", "data_head"):
        if not isinstance(binding[name], str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", binding[name]):
            raise SourceUnavailable("invalid_head_binding")
    manifest = binding.get("input_manifest")
    expected = {("data", p) for p in (*DATA_FILES, PUBLICATION)} | {("code", ENTRY_PATH), ("code", "hub.connection.yaml")}
    if not isinstance(manifest, list) or len(manifest) != len(expected):
        raise SourceUnavailable("invalid_manifest")
    seen = {}
    for m in manifest:
        if not isinstance(m, dict) or set(m) != {"scope", "path", "sha256", "status"}:
            raise SourceUnavailable("invalid_manifest_entry")
        key = (m.get("scope"), m.get("path"))
        if key not in expected or key in seen:
            raise SourceUnavailable("invalid_manifest_path")
        if m.get("status") == "unknown_optional_missing" and key == ("data", PUBLICATION) and m.get("sha256") is None:
            pass
        elif m.get("status") != "present" or not isinstance(m.get("sha256"), str) or not _SHA.fullmatch(m["sha256"]):
            raise SourceUnavailable("invalid_manifest_digest")
        seen[key] = m["sha256"]
    if (binding.get("code_sha256") != seen[("code", ENTRY_PATH)] or
        binding.get("declaration_sha256") != seen[("code", "hub.connection.yaml")] or
        binding.get("content_sha256") != _digest([m for m in manifest if m["scope"] == "data"])):
        raise SourceUnavailable("inconsistent_manifest_binding")
    for name, fact in p["facts"].items():
        if not isinstance(fact, dict) or set(fact) != {"value", "unknown", "source"}:
            raise SourceUnavailable("invalid_fact_fields")
        value = fact["value"]
        if name == "actor":
            if value is not None or fact["unknown"] != "actor_not_published; management_active_is_not_native_goal_resume":
                raise SourceUnavailable("invalid_actor_semantics")
        elif fact["unknown"] is not None:
            raise SourceUnavailable("invalid_fact_unknown")
        elif name == "outputs":
            if value != ["versioned_scenario_packages", "disposable_problem_workspace", "attempt_checks_and_assistance_records", "small_wav_practice_artifact"]:
                raise SourceUnavailable("invalid_output_types")
        elif name == "current_work":
            if not isinstance(value, dict) or set(value) != {"status", "objective", "phase"}:
                raise SourceUnavailable("invalid_current_work")
            for text in value.values():
                if not isinstance(text, str) or not text:
                    raise SourceUnavailable("invalid_current_work_value")
                _public(text)
        else:
            if not isinstance(value, str) or not value:
                raise SourceUnavailable("invalid_fact_value")
            _public(value)
        source = fact.get("source", {})
        if not isinstance(source, dict) or set(source) != {"path", "locator", "content_sha256"}:
            raise SourceUnavailable("invalid_provenance_fields")
        locator = source["locator"]
        if not isinstance(locator, dict) or not set(locator) <= {"heading", "label", "labels", "lines"}:
            raise SourceUnavailable("invalid_locator")
        headings = {"purpose": "Product Vision · 真实问题驱动", "outputs": "实现事实与阶段"}
        if locator.get("heading") != headings.get(name, "Hub 当前管理映射"):
            raise SourceUnavailable("invalid_locator_heading")
        for line in locator.get("lines", []):
            if type(line) is not int or line < 1 or line > 10000:
                raise SourceUnavailable("invalid_locator_line")
        if "labels" in locator and locator["labels"] != ["Status", "Objective", "Phase"]:
            raise SourceUnavailable("invalid_locator_labels")
        if "label" in locator and locator["label"] not in ("actor", "Next action"):
            raise SourceUnavailable("invalid_locator_label")
        if source.get("content_sha256") != seen.get(("data", source.get("path"))) or source.get("path") not in DATA_FILES:
            raise SourceUnavailable("invalid_fact_provenance")


def _context(context):
    if not isinstance(context, str) or not _SHA.fullmatch(context):
        raise SourceUnavailable("context_must_bind_permission_and_contract_digest")
    return context


def _previous(version):
    if version is not None and (not isinstance(version, str) or not _SHA.fullmatch(version)):
        raise SourceUnavailable("invalid_previous_version")


def make_event(projection, *, expected_previous_version, context):
    """Pure local event. Same source with a new observation time emits nothing.

    None means no semantic update. Failure is returned explicitly; it is not a
    success receipt. Receivers independently bind their trusted source version.
    """
    try:
        _valid_projection(projection)
        _context(context)
        _previous(expected_previous_version)
        if projection["source_version"] == expected_previous_version:
            return None
        payload = {k: copy.deepcopy(v) for k, v in projection.items() if k != "observed_at"}
        event = {"schema_version": SOURCE_SCHEMA, "project_id": PROJECT_ID, "context": context,
                 "expected_previous_version": expected_previous_version,
                 "source_version": projection["source_version"], "payload": payload}
        event["event_id"] = _digest(event)
        event["observed_at"] = projection["observed_at"]
        return event
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return {"available": False, "error": str(exc) if isinstance(exc, SourceUnavailable) else "invalid_projection"}


def reduce_event(state, event, *, expected_previous_version, context, expected_source_version, now):
    """Pure CAS reducer; last good value survives all failures, stale/unsynced.

    State is caller-owned in-memory local ABI data, not a business state/queue.
    The caller supplies a fresh trusted expected_source_version. Seen versions
    prevent rollback, including a replay with a newly forged observation time.
    """
    result = copy.deepcopy(state) if isinstance(state, dict) else {}
    def reject(reason):
        result.update(stale=True, synced=False, error=reason, last_result="rejected")
        return result
    try:
        _context(context)
        _previous(expected_previous_version)
        _previous(expected_source_version)
        now_dt = _time(now)
        if result.get("context", context) != context:
            return reject("wrong_state_context")
        if event is None:
            if result.get("source_version") != expected_previous_version:
                return reject("compare_and_swap_conflict")
            observed = result.get("observed_at")
            if (result.get("source_version") != expected_source_version or not observed or
                now_dt < _time(observed) or (now_dt - _time(observed)).total_seconds() > MAX_AGE_SECONDS):
                return reject("stale_or_missing_last_good")
            result["last_result"] = "no_event"
            return result
        if not isinstance(event, dict) or len(_json(event)) > MAX_EVENT_BYTES or event.get("available") is False:
            return reject("invalid_or_unavailable_event")
        if event.get("context") != context or event.get("project_id") != PROJECT_ID or event.get("schema_version") != SOURCE_SCHEMA:
            return reject("wrong_event_context")
        if set(event) != {"schema_version", "project_id", "context", "expected_previous_version", "source_version", "payload", "event_id", "observed_at"}:
            return reject("invalid_event_fields")
        identity = {k: v for k, v in event.items() if k not in ("event_id", "observed_at")}
        if event["event_id"] != _digest(identity):
            return reject("conflicting_event_payload")
        projection = dict(event["payload"], observed_at=event["observed_at"])
        _valid_projection(projection)
        observed = _time(event["observed_at"])
        age = (now_dt - observed).total_seconds()
        if age < 0 or age > MAX_AGE_SECONDS:
            return reject("future_or_stale_event")
        if event["source_version"] != projection["source_version"] or event["source_version"] != expected_source_version:
            return reject("wrong_expected_source_version")
        version = result.get("source_version")
        if version == event["source_version"]:
            if result.get("event_id") != event["event_id"] or result.get("value") != event["payload"]:
                return reject("same_version_conflicting_payload")
            result["last_result"] = "duplicate"
            return result
        if version != expected_previous_version or event["expected_previous_version"] != expected_previous_version:
            return reject("compare_and_swap_conflict")
        if event["source_version"] in result.get("seen_versions", []):
            return reject("old_version")
        if result.get("observed_at") and observed < _time(result["observed_at"]):
            return reject("older_observation")
        seen = list(result.get("seen_versions", []))
        seen.append(event["source_version"])
        return {"context": context, "source_version": event["source_version"], "event_id": event["event_id"],
                "value": copy.deepcopy(event["payload"]), "observed_at": event["observed_at"], "seen_versions": seen,
                "stale": False, "synced": True, "error": None, "last_result": "applied",
                "receipt_scope": "local_source_engineering_only"}
    except (ValueError, TypeError, KeyError, AttributeError) as exc:
        return reject(str(exc) if isinstance(exc, SourceUnavailable) else "invalid_event")



def _load_graph_helper():
    """Execute exact sibling bytes; sys.path/PYTHONPATH/module cache cannot select it."""
    import types
    root = _ENTRY_FILE.parent.parent
    fd, chain = _root(root)
    try:
        first, identity = _read(fd, "scripts/study_hub_graph.py")
        entry, _ = _read(fd, ENTRY_PATH)
        second, after = _read(fd, "scripts/study_hub_graph.py")
        if first != second or identity != after or _sha(entry) != _LOADED_CODE_SHA:
            raise SourceUnavailable("graph_code_drift")
        check, current = _root(root)
        os.close(check)
        if current != chain:
            raise SourceUnavailable("graph_root_drift")
        module = types.ModuleType("_csp_exact_graph_source")
        module.__file__ = str(root / "scripts/study_hub_graph.py")
        module._SOURCE_CODE_SHA256 = _sha(second)
        exec(compile(second, module.__file__, "exec"), module.__dict__)
        return module
    finally:
        os.close(fd)


def _graph_source_stdin(project_root):
    """Explicit bounded sanitized JSON stdin; no source collector or input file."""
    try:
        if project_root != _ENTRY_FILE.parent.parent:
            raise SourceUnavailable("graph_project_root_mismatch")
        helper = _load_graph_helper()
        raw = sys.stdin.buffer.read(helper.MAX_DOCUMENT_BYTES + 1)
        if len(raw) > helper.MAX_DOCUMENT_BYTES:
            raise SourceUnavailable("graph_stdin_limit")
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise SourceUnavailable("duplicate_graph_json_key")
                result[key] = value
            return result
        bundle = json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=unique)
        if type(bundle) is not dict or set(bundle) != {"document", "context", "observed_at"}:
            raise SourceUnavailable("invalid_graph_stdin_bundle")
        if type(bundle["context"]) is not dict or bundle["context"].get("exporter_sha256") != _LOADED_CODE_SHA:
            raise SourceUnavailable("graph_exporter_context_mismatch")
        result = helper.build_study_graph(bundle["document"], context=bundle["context"], observed_at=bundle["observed_at"])
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0 if result["available"] else 2
    except (OSError, ValueError, TypeError, AttributeError, RecursionError, UnicodeError) as exc:
        reason = str(exc) if isinstance(exc, SourceUnavailable) else "graph_source_unavailable"
        print(json.dumps({"available": False, "graph": None, "source_version": None,
                          "error": reason, "scope": "local_source_engineering_only"}))
        return 2


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--hub-root", type=Path, required=True)
    parser.add_argument("--project-root", type=Path, required=True)
    source_modes = parser.add_mutually_exclusive_group()
    source_modes.add_argument("--source-only", action="store_true")
    source_modes.add_argument("--graph-source-only", action="store_true")
    args = parser.parse_args(argv)

    hub_root = args.hub_root.resolve(strict=True)
    project_root = args.project_root.absolute()
    if project_root.is_symlink() or not project_root.is_dir():
        return 2
    # Parent aliases are unsafe too; this does not widen legacy collector scopes.
    try:
        fd, _ = _root(project_root)
        os.close(fd)
    except (OSError, SourceUnavailable):
        return 2
    project_root = project_root.resolve(strict=True)
    if args.graph_source_only:
        return _graph_source_stdin(project_root)
    if args.source_only:
        projection = capture_source(_ENTRY_FILE.parent.parent, project_root,
                                    observed_at=datetime.now(timezone.utc).isoformat())
        print(json.dumps(projection, ensure_ascii=False, sort_keys=True))
        return 0 if projection["available"] else 2
    sys.path.insert(0, str(hub_root / "src"))

    from hub.connection_sources import SourceResolver
    from hub.metric_collect import validate_metric_source_config
    from hub.metric_documents import collect_study
    from hub.metric_export import export_metric_snapshot
    from hub.metric_sources import read_structured
    from hub.metrics import utcnow

    observed_at = utcnow()
    resolver = SourceResolver(hub_root, clock=lambda: observed_at)
    registered = Path(resolver.projects[PROJECT_ID]["root_path"]).expanduser()
    if registered.resolve(strict=True) != project_root:
        return 2
    config, _ = read_structured(hub_root, "data/connections/metric_sources.yaml")
    validate_metric_source_config(config, resolver.projects)
    spec = config["projects"][PROJECT_ID]
    if spec["adapter"] != ADAPTER:
        return 2
    management = resolver.refresh(PROJECT_ID)
    if not management["success"]:
        return 2

    def records(project, project_id, observed):
        return collect_study(project, project_id, observed, spec)

    export_metric_snapshot(
        project_root,
        PROJECT_ID,
        {"records": records},
        exporter_id="computer-study-plan-export",
        exporter_version="1.0",
        management=management,
        clock=lambda: observed_at,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

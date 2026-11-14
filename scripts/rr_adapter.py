#!/usr/bin/env python3
"""Opt-in project-owned RR adapter. Production identity is never a fixture default."""
from __future__ import annotations
import array
import copy
from datetime import datetime, timezone
from email import policy
from email.parser import BytesParser
import fcntl
import hashlib
import hmac
from http.server import BaseHTTPRequestHandler
import io
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import socket
import socketserver
import stat
import struct
import tempfile
import threading
import time
import uuid
from rr_manifest import (ROOT, PROJECT_ID, ORIGIN, BROWSER_SOCKET, OWNER_SOCKET,
                         FrozenApplication, canonical, digest)

MAX_BODY = 2 * 1024 * 1024 + 32 * 1024
MAX_ATTACHMENT = 1024 * 1024
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")
SHA = re.compile(r"[a-f0-9]{64}\Z")
FEEDBACK = "/__rr/v1/feedback"
AGENT = "/__rr-agent/v1/feedback"

class Refused(ValueError):
    def __init__(self, code, status=400):
        super().__init__(code)
        self.status = status
        self.code = code

class ProviderUnavailable(Refused):
    """Only a fixed startup prerequisite is temporarily unavailable."""
    def __init__(self):
        super().__init__("provider_temporarily_unavailable", 503)

def require(condition, code, status=400):
    if not condition:
        raise Refused(code, status)

def exact(value, keys):
    require(type(value) is dict and set(value) == set(keys), "invalid_fields")

def loads(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate_key")
            result[key] = value
        return result
    def no_float(_):
        raise Refused("non_integer_json")
    try:
        result = json.loads(data.decode("utf-8"), object_pairs_hook=pairs,
                            parse_float=no_float, parse_constant=no_float)
        canonical(result)
        return result
    except (UnicodeError, json.JSONDecodeError, TypeError, OverflowError, RecursionError):
        raise Refused("invalid_json") from None

def identity(value):
    require(type(value) is str and ID.fullmatch(value), "invalid_id")
    return value

def uuid_text(value):
    require(type(value) is str, "invalid_uuid")
    try:
        require(str(uuid.UUID(value)) == value, "invalid_uuid")
    except ValueError:
        raise Refused("invalid_uuid") from None
    return value

def checked_text(value, limit=16384):
    require(type(value) is str and len(value.encode("utf-8")) <= limit
            and "\x00" not in value, "invalid_text")
    return value

def private_dir(path):
    path = Path(path).absolute()
    require(not any(q.is_symlink() for q in (path, *path.parents)), "storage_link_refused")
    if not path.exists():
        path.mkdir(mode=0o700)
    st = path.stat()
    require(stat.S_ISDIR(st.st_mode) and st.st_uid == os.getuid()
            and not st.st_mode & 0o077, "storage_untrusted")
    return path

def safe_bytes(path):
    fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as stream:
        st = os.fstat(stream.fileno())
        require(stat.S_ISREG(st.st_mode) and st.st_uid == os.getuid()
                and not st.st_mode & 0o077, "storage_untrusted")
        require(st.st_size <= MAX_BODY + 65536, "storage_invalid")
        return stream.read()

def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)

def write_new(path, data):
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data); stream.flush(); os.fsync(stream.fileno())

def validate_attachment(data, kind):
    require(len(data) <= MAX_ATTACHMENT, "attachment_too_large", 413)
    if kind == "text/plain":
        try:
            text = data.decode("utf-8")
            require("\x00" not in text, "invalid_attachment", 415)
        except UnicodeError:
            raise Refused("invalid_attachment", 415) from None
        return
    expected = {"image/png": "PNG", "image/jpeg": "JPEG", "image/webp": "WEBP"}.get(kind)
    require(expected is not None, "unsupported_attachment", 415)
    try:
        from PIL import Image
        with Image.open(io.BytesIO(data)) as image:
            require(image.format == expected and image.width * image.height <= 4194304
                    and getattr(image, "n_frames", 1) == 1, "invalid_attachment", 415)
            image.verify()
        with Image.open(io.BytesIO(data)) as image:
            image.load()
    except Refused:
        raise
    except Exception:
        raise Refused("invalid_attachment", 415) from None

def multipart(body, content_type):
    require(len(body) <= MAX_BODY, "request_too_large", 413)
    require(content_type.startswith("multipart/form-data;") and "\r" not in content_type
            and "\n" not in content_type and len(content_type) < 256, "multipart_required", 415)
    message = BytesParser(policy=policy.default).parsebytes(
        b"Content-Type: " + content_type.encode("ascii") + b"\r\nMIME-Version: 1.0\r\n\r\n" + body)
    require(message.is_multipart() and not message.defects, "invalid_multipart")
    parts = {}
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        require(part.get_content_disposition() == "form-data" and not part.is_multipart()
                and name in {"feedback", "attachment.0", "attachment.1"} and name not in parts
                and not part.defects and part.get("Content-Transfer-Encoding") is None,
                "invalid_multipart")
        parts[name] = (part.get_payload(decode=True), part.get_content_type())
    require("feedback" in parts and parts["feedback"][1] == "application/json", "invalid_multipart")
    require(len(parts["feedback"][0]) <= 16384, "feedback_too_large", 413)
    payload = loads(parts["feedback"][0])
    files = {name: item for name, item in parts.items() if name != "feedback"}
    return payload, files

class FeedbackStore:
    """One project process owns an atomic record plus its immutable attachments."""
    def __init__(self, root):
        self.root = private_dir(root)
        self.lock_fd = os.open(self.root / ".owner.lock",
                               os.O_RDWR | os.O_CREAT | os.O_CLOEXEC | os.O_NOFOLLOW, 0o600)
        try:
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(self.lock_fd)
            raise Refused("feedback_process_already_running", 503) from None
        self.mutex = threading.RLock()

    def close(self):
        if self.lock_fd is not None:
            os.close(self.lock_fd); self.lock_fd = None

    def directory(self, fid):
        uuid_text(fid)
        path = self.root / fid
        require(path.is_dir() and not path.is_symlink(), "not_found", 404)
        require(path.stat().st_uid == os.getuid() and not path.stat().st_mode & 0o077,
                "storage_untrusted", 503)
        return path

    def get(self, fid, device=None):
        with self.mutex:
            record = loads(safe_bytes(self.directory(fid) / "feedback.json"))
            require(device is None or record["device_sha256"] == device, "not_found", 404)
            require(record["feedback_id"] == fid and record["project_id"] == PROJECT_ID
                    and digest(canonical(record["payload"])) == record["payload_sha256"],
                    "feedback_corrupt", 503)
            return record

    def attachment(self, fid, aid, device=None):
        identity(aid)
        record = self.get(fid, device)
        item = next((a for a in record["attachments"] if a["attachment_id"] == aid), None)
        require(item is not None, "not_found", 404)
        data = safe_bytes(self.directory(fid) / (aid + ".bin"))
        require(len(data) == item["size"] and digest(data) == item["sha256"],
                "attachment_corrupt", 503)
        return data, item

    def receipt(self, record):
        return {key: copy.deepcopy(record[key]) for key in
                ("schema", "project_id", "client_request_id", "feedback_id", "revision",
                 "accepted_at", "payload_sha256", "attachments")}

    def submit(self, payload, files, device, app):
        exact(payload, ("schema", "client_request_id", "project_id", "page_path", "source",
                        "resource", "description", "expected", "actual", "steps",
                        "submitted_at", "attachments"))
        require(type(payload["schema"]) is int and payload["schema"] == 1
                and payload["project_id"] == PROJECT_ID, "project_mismatch")
        uuid_text(payload["client_request_id"])
        require(payload["page_path"] == "/", "page_not_allowed")
        exact(payload["source"], ("commit", "build_id", "dirty"))
        require(type(payload["source"]["dirty"]) is bool and payload["source"] == app.source,
                "source_mismatch", 409)
        resource = payload["resource"]
        exact(resource, ("id", "sha256", "mode", "preview_version"))
        require(resource == {k: app.resources["/"][k] for k in resource}, "resource_mismatch", 409)
        for field in ("description", "expected", "actual", "steps"):
            checked_text(payload[field])
        require(payload["description"].strip(), "description_required")
        checked_text(payload["submitted_at"], 40)
        try:
            stamp = datetime.fromisoformat(payload["submitted_at"].replace("Z", "+00:00"))
            require(stamp.utcoffset() is not None, "invalid_time")
        except ValueError:
            raise Refused("invalid_time") from None
        require(type(payload["attachments"]) is list and len(payload["attachments"]) <= 2,
                "invalid_attachments")
        require(set(files) == {f"attachment.{n}" for n in range(len(payload["attachments"]))},
                "attachment_mismatch")
        attachments, raw = [], {}
        for n, item in enumerate(payload["attachments"]):
            exact(item, ("attachment_id", "size", "sha256"))
            aid = identity(item["attachment_id"])
            require(aid not in raw, "duplicate_attachment")
            data, kind = files[f"attachment.{n}"]
            require(type(item["size"]) is int and item["size"] == len(data)
                    and type(item["sha256"]) is str and SHA.fullmatch(item["sha256"])
                    and item["sha256"] == digest(data), "attachment_mismatch")
            validate_attachment(data, kind)
            attachments.append(dict(item, content_type=kind))
            raw[aid] = data
        payload_sha = digest(canonical(payload))
        fid = str(uuid.uuid5(uuid.NAMESPACE_URL,
                           PROJECT_ID + ":" + device + ":" + payload["client_request_id"]))
        with self.mutex:
            path = self.root / fid
            if path.exists() or path.is_symlink():
                old = self.get(fid, device)
                require(old["payload_sha256"] == payload_sha and old["attachments"] == attachments,
                        "idempotency_conflict", 409)
                return self.receipt(old), 200
            record = dict(self.receipt_fields(payload, fid, payload_sha), payload=payload,
                          device_sha256=device, attachments=attachments, state="pending",
                          read_receipt=None, result=None)
            stage = Path(tempfile.mkdtemp(prefix=".pending-", dir=self.root))
            try:
                for aid, data in raw.items():
                    write_new(stage / (aid + ".bin"), data)
                write_new(stage / "feedback.json", canonical(record))
                sync_dir(stage)
                os.rename(stage, path)
                sync_dir(self.root)
            finally:
                if stage.exists():
                    shutil.rmtree(stage)
            return self.receipt(record), 201

    @staticmethod
    def receipt_fields(payload, fid, payload_sha):
        return {"schema": 1, "project_id": PROJECT_ID,
                "client_request_id": payload["client_request_id"], "feedback_id": fid,
                "revision": 1, "accepted_at": datetime.now(timezone.utc).isoformat(),
                "payload_sha256": payload_sha}

    def by_request(self, request_id, device):
        uuid_text(request_id)
        fid = str(uuid.uuid5(uuid.NAMESPACE_URL, PROJECT_ID + ":" + device + ":" + request_id))
        return self.receipt(self.get(fid, device))

    def list(self, state="pending", limit=20, cursor=""):
        require(state in {"pending", "agent_read", "processed"} and type(limit) is int
                and 1 <= limit <= 100, "invalid_query")
        if cursor:
            uuid_text(cursor)
        records = []
        with self.mutex:
            for path in sorted(self.root.iterdir()):
                if path.name.startswith(".") or (cursor and path.name <= cursor):
                    continue
                record = self.get(path.name)
                if record["state"] == state:
                    records.append({**self.receipt(record), "state": state,
                                    "page_path": record["payload"]["page_path"],
                                    "source": record["payload"]["source"]})
                    if len(records) == limit:
                        break
        return {"feedback": records, "cursor": records[-1]["feedback_id"] if records else None}

    def update(self, fid, record):
        path = self.directory(fid)
        temp = path / (".update-" + secrets.token_hex(16))
        try:
            write_new(temp, canonical(record))
            os.replace(temp, path / "feedback.json")
            sync_dir(path)
        finally:
            if temp.exists():
                temp.unlink()

    def ack(self, fid, payload, uid):
        exact(payload, ("revision", "payload_sha256", "attachments", "read_token"))
        with self.mutex:
            record = self.get(fid)
            expected = [{"attachment_id": a["attachment_id"], "sha256": a["sha256"]}
                        for a in record["attachments"]]
            require(type(payload["revision"]) is int and payload["revision"] == record["revision"]
                    and payload["payload_sha256"] == record["payload_sha256"]
                    and payload["attachments"] == expected, "revision_conflict", 409)
            if record["state"] == "pending":
                record["state"] = "agent_read"
                record["read_receipt"] = {"revision": record["revision"], "uid": uid,
                                          "read_at": datetime.now(timezone.utc).isoformat(),
                                          "payload_sha256": record["payload_sha256"],
                                          "attachments": expected}
                self.update(fid, record)
            return record

    def result(self, fid, payload):
        exact(payload, ("revision", "summary", "references"))
        checked_text(payload["summary"], 8192)
        require(payload["summary"].strip() and type(payload["references"]) is list
                and len(payload["references"]) <= 20, "invalid_result")
        for reference in payload["references"]:
            checked_text(reference, 1024)
        with self.mutex:
            record = self.get(fid)
            require(type(payload["revision"]) is int and payload["revision"] == record["revision"]
                    and record["state"] in {"agent_read", "processed"}, "revision_conflict", 409)
            if record["state"] == "processed":
                require({k: record["result"][k] for k in payload} == payload,
                        "result_conflict", 409)
            else:
                record["state"] = "processed"
                record["result"] = dict(payload, processed_at=datetime.now(timezone.utc).isoformat())
                self.update(fid, record)
            return record

def _provider_metadata(path, provider_uid, provider_gid):
    require(not any(q.is_symlink() for q in (path, *path.parents)), "provider_untrusted", 503)
    try:
        st, parent = path.lstat(), path.parent.lstat()
    except FileNotFoundError:
        raise ProviderUnavailable() from None
    require(stat.S_ISSOCK(st.st_mode) and st.st_uid == provider_uid and st.st_gid == provider_gid
            and stat.S_IMODE(st.st_mode) == 0o660 and parent.st_uid == provider_uid
            and parent.st_gid == provider_gid and stat.S_IMODE(parent.st_mode) == 0o750,
            "provider_untrusted", 503)

def _provider_exchange(path, provider_uid, provider_gid):
    with socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET) as peer:
        peer.settimeout(3)
        try:
            peer.connect(str(path))
        except (FileNotFoundError, ConnectionRefusedError, TimeoutError):
            raise ProviderUnavailable() from None
        return receive_provider_key(peer, provider_uid, provider_gid)

def provider_key():
    """Fixed production binding; only missing/refused/timed-out prerequisites retry."""
    path = Path("/run/rr-project-keys/key.sock")
    require(os.getuid() == 1000, "owner_identity_required", 503)
    _provider_metadata(path, 996, 984)
    return _provider_exchange(path, 996, 984)

def receive_provider_key(peer, provider_uid, provider_gid):
    """Receive a real sealed FD. Tests pass their actual fixture peer, never UID996."""
    fds = []
    try:
        _, uid, gid = struct.unpack("3i", peer.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
        require((uid, gid) == (provider_uid, provider_gid), "provider_peer_refused", 503)
        try:
            peer.sendall(canonical({"project_id": PROJECT_ID, "recipient_uid": 1000, "schema": 1}) + b"\n")
            data, control, flags, _ = peer.recvmsg(512, socket.CMSG_SPACE(16), socket.MSG_CMSG_CLOEXEC)
        except TimeoutError:
            raise ProviderUnavailable() from None
        for level, kind, value in control:
            if level == socket.SOL_SOCKET and kind == socket.SCM_RIGHTS:
                entries = array.array("i")
                entries.frombytes(value[:len(value) - len(value) % entries.itemsize])
                fds.extend(entries)
            else:
                raise Refused("provider_packet_invalid", 503)
        response = {"key_fd": True, "project_id": PROJECT_ID, "schema": 1}
        require(not flags & (socket.MSG_CTRUNC | socket.MSG_TRUNC) and len(fds) == 1
                and data == canonical(response) + b"\n", "provider_packet_invalid", 503)
        fd = fds[0]
        seals = fcntl.F_SEAL_WRITE | fcntl.F_SEAL_GROW | fcntl.F_SEAL_SHRINK | fcntl.F_SEAL_SEAL
        info = os.fstat(fd)
        require(stat.S_ISREG(info.st_mode) and info.st_nlink == 0 and info.st_uid == provider_uid
                and 32 <= info.st_size <= 64 and stat.S_IMODE(info.st_mode) == 0o400
                and fcntl.fcntl(fd, fcntl.F_GET_SEALS) & seals == seals
                and fcntl.fcntl(fd, fcntl.F_GETFL) & os.O_ACCMODE == os.O_RDONLY
                and fcntl.fcntl(fd, fcntl.F_GETFD) & fcntl.FD_CLOEXEC,
                "provider_fd_invalid", 503)
        os.lseek(fd, 0, os.SEEK_SET)
        key = os.read(fd, 65)
        require(len(key) == info.st_size, "provider_fd_invalid", 503)
        return key
    finally:
        for fd in fds:
            os.close(fd)

class Adapter:
    def __init__(self, manager, app, store, key, *, gateway_uid=996, owner_uid=1000):
        require(type(key) is bytes and 32 <= len(key) <= 64, "key_unavailable", 503)
        self.manager, self.app, self.store = manager, app, store
        self.key, self.gateway_uid, self.owner_uid = key, gateway_uid, owner_uid
        self.lock = threading.RLock()
        self.challenges, self.nonces, self.reads = {}, {}, {}

    def challenge(self):
        with self.lock:
            now = time.monotonic()
            self.challenges = {k: v for k, v in self.challenges.items() if v > now}
            require(len(self.challenges) < 256, "challenge_busy", 503)
            value = secrets.token_hex(32)
            self.challenges[value] = now + 30
            return {"challenge": value}

    def authenticate(self, encoded, method, path, body):
        import base64
        require(type(encoded) is str and re.fullmatch(r"[A-Za-z0-9_-]{1,4096}", encoded),
                "browser_auth_required", 403)
        try:
            raw = base64.b64decode(encoded + "=" * (-len(encoded) % 4), altchars=b"-_", validate=True)
            value = loads(raw)
        except (ValueError, TypeError):
            raise Refused("browser_auth_required", 403) from None
        exact(value, ("v", "challenge", "device_sha256", "project_id", "origin",
                      "method", "path", "body_sha256", "nonce", "issued_at", "expires", "mac"))
        require(canonical(value) == raw, "browser_auth_required", 403)
        with self.lock:
            expiry = self.challenges.pop(value["challenge"], 0)
            now = int(time.time())
            self.nonces = {k: v for k, v in self.nonces.items() if v >= now}
            require(expiry > time.monotonic() and type(value["v"]) is int and value["v"] == 1
                    and value["project_id"] == PROJECT_ID and value["origin"] == ORIGIN
                    and value["method"] == method and value["path"] == path
                    and value["body_sha256"] == digest(body)
                    and type(value["device_sha256"]) is str and SHA.fullmatch(value["device_sha256"])
                    and type(value["issued_at"]) is int and type(value["expires"]) is int
                    and now - 30 <= value["issued_at"] <= now
                    and now < value["expires"] <= value["issued_at"] + 30
                    and value["nonce"] not in self.nonces and len(self.nonces) < 4096,
                    "browser_auth_required", 403)
            uuid_text(value["nonce"])
            unsigned = {k: v for k, v in value.items() if k != "mac"}
            require(type(value["mac"]) is str and SHA.fullmatch(value["mac"])
                    and hmac.compare_digest(value["mac"], hmac.new(
                        self.key, canonical(unsigned), hashlib.sha256).hexdigest()),
                    "browser_auth_required", 403)
            self.nonces[value["nonce"]] = value["expires"]
            return value["device_sha256"]

    def public_record(self, record):
        return {k: v for k, v in record.items() if k != "device_sha256"}

    def owner_read(self, fid, uid):
        record = self.store.get(fid)
        with self.lock:
            now = time.monotonic()
            self.reads = {k: v for k, v in self.reads.items() if v["expires"] > now}
            require(len(self.reads) < 128, "read_busy", 503)
            token = secrets.token_urlsafe(32)
            self.reads[token] = {"fid": fid, "uid": uid, "revision": record["revision"],
                                 "payload_sha256": record["payload_sha256"],
                                 "seen": set(), "expires": now + 300}
        return dict(self.public_record(record), read_token=token)

    def ticket(self, token, fid, uid):
        require(type(token) is str, "actual_read_required", 409)
        value = self.reads.get(token)
        require(value and value["expires"] > time.monotonic()
                and value["fid"] == fid and value["uid"] == uid, "actual_read_required", 409)
        return value

    def owner(self, method, path, body, headers, uid):
        from urllib.parse import urlsplit, parse_qs
        require(uid == self.owner_uid and headers.get("Origin") is None,
                "owner_identity_required", 403)
        parsed = urlsplit(path)
        if parsed.path == AGENT and method == "GET":
            values = parse_qs(parsed.query, keep_blank_values=True, strict_parsing=True)
            require(set(values) <= {"state", "limit", "cursor"}
                    and all(len(v) == 1 for v in values.values()), "invalid_query")
            try:
                limit = int(values.get("limit", ["20"])[0])
            except ValueError:
                raise Refused("invalid_query") from None
            return 200, self.store.list(values.get("state", ["pending"])[0], limit,
                                        values.get("cursor", [""])[0]), None
        require(not parsed.query and not parsed.fragment, "not_found", 404)
        match = re.fullmatch(re.escape(AGENT) + r"/([a-f0-9-]{36})(?:/(ack|result|attachments/([A-Za-z0-9_-]+)))?", path)
        require(match is not None, "not_found", 404)
        fid, action, aid = match.groups()
        if action is None and method == "GET":
            return 200, self.owner_read(fid, uid), None
        if aid and method == "GET":
            with self.lock:
                ticket = self.ticket(headers.get("X-RR-Read-Token"), fid, uid)
                data, item = self.store.attachment(fid, aid)
                ticket["seen"].add(aid)
            return 200, data, item["content_type"]
        if action == "ack" and method == "POST":
            payload = loads(body)
            exact(payload, ("revision", "payload_sha256", "attachments", "read_token"))
            with self.lock:
                ticket = self.ticket(payload["read_token"], fid, uid)
                record = self.store.get(fid)
                require(ticket["seen"] == {a["attachment_id"] for a in record["attachments"]}
                        and payload["revision"] == ticket["revision"]
                        and payload["payload_sha256"] == ticket["payload_sha256"],
                        "actual_read_required", 409)
                result = self.store.ack(fid, payload, uid)
                self.reads.pop(payload["read_token"], None)
            return 200, self.public_record(result), None
        if action == "result" and method == "POST":
            return 200, self.public_record(self.store.result(fid, loads(body))), None
        raise Refused("not_found", 404)

    def browser(self, method, path, body, content_type, device):
        require("?" not in path and "#" not in path and "%" not in path
                and "\\" not in path and ".." not in path, "not_found", 404)
        if method == "GET" and path == "/__rr/v1/manifest":
            return 200, self.app.manifest, None
        if method == "GET" and path in self.app.assets:
            return 200, self.app.assets[path], self.app.resources[path]["content_type"]
        if method == "GET" and path == "/__rr/v1/workbench":
            # catalog() is a pure deep-copy. history()/snapshot() refresh and may write:
            # do not expose either, terminal output, Lab token or a host path.
            return 200, {"schema": 1, "project_id": PROJECT_ID, "source": self.app.source,
                         "resource": {k: self.app.resources["/"][k] for k in
                                      ("id", "sha256", "mode", "preview_version")},
                         "review_mode": "readonly", **self.manager.catalog(),
                         "capabilities": {"available": False, "limitations": [
                             "远程只读审核；终端、实验操作及个人尝试记录仅在本机开放。"]}}, None
        if method == "POST" and path == FEEDBACK:
            payload, files = multipart(body, content_type or "")
            receipt, status = self.store.submit(payload, files, device, self.app)
            return status, receipt, None
        match = re.fullmatch(re.escape(FEEDBACK) + r"/by-request/([a-f0-9-]{36})", path)
        if method == "GET" and match:
            return 200, self.store.by_request(match[1], device), None
        match = re.fullmatch(re.escape(FEEDBACK) + r"/([a-f0-9-]{36})(?:/attachments/([A-Za-z0-9_-]+))?", path)
        if method == "GET" and match:
            fid, aid = match.groups()
            if aid:
                data, item = self.store.attachment(fid, aid, device)
                return 200, data, item["content_type"]
            return 200, self.public_record(self.store.get(fid, device)), None
        raise Refused("not_found", 404)

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "CSP-RR"
    sys_version = ""

    def setup(self):
        super().setup()
        self.connection.settimeout(5)

    def log_message(self, *_):
        pass

    def send_value(self, status, value, content_type=None):
        body = value if isinstance(value, bytes) else canonical(value)
        self.close_connection = True
        self.send_response(status)
        self.send_header("Content-Type", content_type or "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-src 'none'; base-uri 'none'")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def handle_request(self):
        try:
            adapter = self.server.adapter
            _, uid, gid = struct.unpack("3i", self.connection.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
            require(sum(len(k) + len(v) for k, v in self.headers.items()) <= 16384,
                    "headers_too_large", 413)
            require(all(len(self.headers.get_all(k)) == 1 for k in self.headers.keys()),
                    "duplicate_header")
            require(not self.headers.get("Transfer-Encoding"), "transfer_encoding_refused")
            length = self.headers.get("Content-Length", "0")
            require(re.fullmatch(r"[0-9]{1,8}", length), "invalid_length")
            length = int(length)
            require(length <= MAX_BODY, "request_too_large", 413)
            require(self.command in {"GET", "POST"} and (self.command != "GET" or length == 0),
                    "method_not_allowed", 405)
            require(self.headers.get("Host") == ("rr-owner.local" if self.server.owner_role else "pch-rr.local"),
                    "invalid_host", 403)
            require(uid == (adapter.owner_uid if self.server.owner_role else adapter.gateway_uid),
                    "peer_refused", 403)
            body = self.rfile.read(length)
            require(len(body) == length, "incomplete_body")
            adapter.app.check()
            if self.server.owner_role:
                result = adapter.owner(self.command, self.path, body, self.headers, uid)
            else:
                if self.path == "/__rr-local/v1/challenge" and self.command == "GET":
                    result = (200, adapter.challenge(), None)
                else:
                    require(self.headers.get("Origin") == ORIGIN, "wrong_origin", 403)
                    device = adapter.authenticate(self.headers.get("X-PCH-RR-Auth"),
                                                  self.command, self.path, body)
                    result = adapter.browser(self.command, self.path, body,
                                              self.headers.get("Content-Type"), device)
            self.send_value(*result)
        except Refused as error:
            self.send_value(error.status, {"error": error.code})
        except (ValueError, KeyError, TypeError, OSError, RecursionError):
            self.send_value(503, {"error": "project_unavailable"})

    do_GET = handle_request
    do_POST = handle_request
    do_HEAD = handle_request

def process_identity(pid=None):
    """Actual Linux identity; never infer death from a missing lock alone."""
    pid = os.getpid() if pid is None else pid
    require(type(pid) is int and pid > 1, "instance_identity_invalid", 503)
    raw = Path(f"/proc/{pid}/stat").read_text()
    fields = raw.rsplit(")", 1)[1].split()
    require(int(raw.split(" ", 1)[0]) == pid, "instance_identity_invalid", 503)
    return {"pid": pid, "start_ticks": int(fields[19]),
            "boot_id": Path("/proc/sys/kernel/random/boot_id").read_text().strip(),
            "pid_namespace": os.stat("/proc/self/ns/pid").st_ino}, fields[0]

def socket_metadata(info):
    return {"dev": info.st_dev, "ino": info.st_ino, "uid": info.st_uid,
            "gid": info.st_gid, "mode": stat.S_IMODE(info.st_mode)}

class SocketInstance:
    """One private, atomic instance record under FeedbackStore's existing flock."""
    NAME = ".instance.json"

    def __init__(self, store, paths, *, production=True):
        self.store, self.state_fd, self.namespace_fd = store, None, None
        self.saved = None
        self.paths = {role: Path(path) for role, path in paths.items()}
        require(set(self.paths) == {"browser", "owner"} and
                self.paths["browser"].parent == self.paths["owner"].parent
                and self.paths["browser"].name == "browser.sock"
                and self.paths["owner"].name == "owner.sock", "instance_namespace_invalid", 503)
        self.directory = self.paths["browser"].parent
        try:
            require(store.lock_fd is not None, "instance_store_not_owned", 503)
            held = os.fstat(store.lock_fd)
            lock = (store.root / ".owner.lock").lstat()
            require((held.st_dev, held.st_ino) == (lock.st_dev, lock.st_ino)
                    and stat.S_ISREG(held.st_mode) and held.st_uid == os.getuid()
                    and stat.S_IMODE(held.st_mode) == 0o600 and held.st_nlink == 1,
                    "instance_store_not_owned", 503)
            fcntl.flock(store.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            require(not any(p.is_symlink() for p in (self.directory, *self.directory.parents)),
                    "socket_directory_untrusted", 503)
            self.namespace_fd = os.open(self.directory, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
            info = os.fstat(self.namespace_fd)
            require(info.st_uid == os.getuid(), "socket_directory_untrusted", 503)
            if production:
                require(os.getuid() == 1000 and info.st_gid == 984
                        and stat.S_IMODE(info.st_mode) == 0o2750
                        and str(self.paths["browser"]) == BROWSER_SOCKET
                        and str(self.paths["owner"]) == OWNER_SOCKET,
                        "socket_directory_untrusted", 503)
            else:
                require(stat.S_IMODE(info.st_mode) == 0o700, "fixture_directory_untrusted", 503)
            self.namespace = dict(socket_metadata(info), path=str(self.directory))
            self.owner, _ = process_identity()
            self.state_fd = os.open(store.root, os.O_RDONLY | os.O_DIRECTORY | os.O_CLOEXEC | os.O_NOFOLLOW)
            self.saved = self._read()
            if self.saved is not None:
                previous = loads(self.saved)
                self._recover(previous)
            else:
                require(all(self._stat(role) is None for role in self.paths),
                        "unrecorded_socket_present", 503)
            self.record = {"schema": 1, "project_id": PROJECT_ID, "owner": self.owner,
                           "namespace": self.namespace, "sockets": {}}
            self._save()
        except BaseException:
            self.release()
            raise

    def _namespace_current(self):
        require(set(os.listdir(self.namespace_fd)) <= {path.name for path in self.paths.values()},
                "instance_namespace_unknown_objects", 503)
        require(self.store.lock_fd is not None, "instance_store_not_owned", 503)
        held = os.fstat(self.store.lock_fd)
        lock = (self.store.root / ".owner.lock").lstat()
        state = self.store.root.lstat()
        require((held.st_dev, held.st_ino) == (lock.st_dev, lock.st_ino)
                and stat.S_ISREG(held.st_mode) and held.st_uid == os.getuid()
                and stat.S_IMODE(held.st_mode) == 0o600 and held.st_nlink == 1
                and (state.st_dev, state.st_ino) == (os.fstat(self.state_fd).st_dev, os.fstat(self.state_fd).st_ino)
                and stat.S_ISDIR(state.st_mode) and state.st_uid == os.getuid()
                and not state.st_mode & 0o077, "instance_store_not_owned", 503)
        fcntl.flock(self.store.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        require(not any(p.is_symlink() for p in (self.directory, *self.directory.parents)),
                "instance_namespace_changed", 503)
        current = self.directory.lstat()
        require(stat.S_ISDIR(current.st_mode) and
                dict(socket_metadata(current), path=str(self.directory)) == self.namespace
                and socket_metadata(os.fstat(self.namespace_fd)) == socket_metadata(current),
                "instance_namespace_changed", 503)

    def _stat(self, role):
        try:
            return os.stat(self.paths[role].name, dir_fd=self.namespace_fd, follow_symlinks=False)
        except FileNotFoundError:
            return None

    def _read(self):
        try:
            fd = os.open(self.NAME, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW, dir_fd=self.state_fd)
        except FileNotFoundError:
            return None
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid()
                    and stat.S_IMODE(info.st_mode) == 0o600 and info.st_nlink == 1
                    and info.st_size <= 8192, "instance_record_untrusted", 503)
            return stream.read()

    def _save(self):
        self._namespace_current()
        require(self._read() == self.saved, "instance_record_changed", 503)
        data = canonical(self.record)
        name = ".instance-" + secrets.token_hex(16)
        try:
            fd = os.open(name, os.O_CREAT | os.O_EXCL | os.O_WRONLY | os.O_CLOEXEC | os.O_NOFOLLOW,
                         0o600, dir_fd=self.state_fd)
            with os.fdopen(fd, "wb") as stream:
                stream.write(data); stream.flush(); os.fsync(stream.fileno())
            os.rename(name, self.NAME, src_dir_fd=self.state_fd, dst_dir_fd=self.state_fd)
            os.fsync(self.state_fd)
            self.saved = data
        finally:
            try: os.unlink(name, dir_fd=self.state_fd)
            except FileNotFoundError: pass

    def _recover(self, previous):
        exact(previous, ("schema", "project_id", "owner", "namespace", "sockets"))
        require(type(previous["schema"]) is int and previous["schema"] == 1
                and previous["project_id"] == PROJECT_ID, "instance_record_invalid", 503)
        namespace = previous["namespace"]
        exact(namespace, ("path", "dev", "ino", "uid", "gid", "mode"))
        require(namespace["path"] == str(self.directory)
                and all(type(namespace[k]) is int for k in ("dev", "ino", "uid", "gid", "mode"))
                and namespace["dev"] >= 0 and namespace["ino"] > 0
                and all(namespace[k] == self.namespace[k] for k in ("uid", "gid", "mode")),
                "instance_record_invalid", 503)
        owner = previous["owner"]
        exact(owner, ("pid", "start_ticks", "boot_id", "pid_namespace"))
        require(type(owner["pid"]) is int and owner["pid"] > 1
                and type(owner["start_ticks"]) is int and owner["start_ticks"] > 0
                and type(owner["pid_namespace"]) is int and owner["pid_namespace"] > 0,
                "instance_identity_invalid", 503)
        uuid_text(owner["boot_id"])
        same_boot = owner["boot_id"] == self.owner["boot_id"]
        if same_boot:
            require(owner["pid_namespace"] == self.owner["pid_namespace"],
                    "instance_identity_unverifiable", 503)
            try:
                actual, state = process_identity(owner["pid"])
                require(actual != owner or state in {"Z", "X"}, "instance_still_alive", 503)
            except FileNotFoundError as error:
                require(error.filename == f"/proc/{owner['pid']}/stat"
                        and process_identity()[0] == self.owner, "instance_identity_unverifiable", 503)
        # A different real boot ID proves the old process cannot be this boot's PID.
        sockets = previous["sockets"]
        require(type(sockets) is dict and set(sockets) <= set(self.paths), "instance_record_invalid", 503)
        for role, item in sockets.items():
            exact(item, ("path", "dev", "ino", "uid", "gid", "mode"))
            require(item["path"] == str(self.paths[role])
                    and all(type(item[k]) is int for k in ("dev", "ino", "uid", "gid", "mode"))
                    and item["dev"] >= 0 and item["ino"] > 0 and item["uid"] == os.getuid()
                    and item["gid"] == namespace["gid"]
                    and item["mode"] == (0o600 if role == "owner" else 0o660),
                    "instance_record_invalid", 503)
        entries = set(os.listdir(self.namespace_fd))
        require(entries <= {path.name for path in self.paths.values()},
                "instance_namespace_unknown_objects", 503)
        if namespace != self.namespace or not same_boot:
            # No object is unlinked across generations. The new fixed namespace
            # must be genuinely empty and already pass the unchanged native guards.
            require(not entries, "instance_namespace_changed", 503)
            self._namespace_current()
            require(self._read() == self.saved, "instance_record_changed", 503)
            return
        reclaim = []
        for role in self.paths:
            info = self._stat(role)
            if role not in sockets:
                require(info is None, "unrecorded_socket_present", 503)
                continue
            item = sockets[role]
            if info is None:
                continue
            require(stat.S_ISSOCK(info.st_mode) and dict(socket_metadata(info), path=str(self.paths[role])) == item,
                    "instance_socket_changed", 503)
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as peer:
                    peer.settimeout(0.5)
                    peer.connect(f"/proc/self/fd/{self.namespace_fd}/{self.paths[role].name}")
            except ConnectionRefusedError:
                reclaim.append((role, item))
            except OSError:
                raise Refused("instance_socket_unverifiable", 503) from None
            else:
                raise Refused("instance_listener_active", 503)
        # Validate the whole pair before removing any recorded binding.
        self._namespace_current()
        require(self._read() == self.saved, "instance_record_changed", 503)
        for role, item in reclaim:
            info = self._stat(role)
            require(info is not None and stat.S_ISSOCK(info.st_mode)
                    and dict(socket_metadata(info), path=str(self.paths[role])) == item,
                    "instance_socket_changed", 503)
        for role, item in reclaim:
            self._namespace_current()
            require(self._read() == self.saved, "instance_record_changed", 503)
            info = self._stat(role)
            require(info is not None and stat.S_ISSOCK(info.st_mode)
                    and dict(socket_metadata(info), path=str(self.paths[role])) == item,
                    "instance_socket_changed", 503)
            os.unlink(self.paths[role].name, dir_fd=self.namespace_fd)
        if reclaim:
            os.fsync(self.namespace_fd)

    def created(self, role, info):
        require(stat.S_ISSOCK(info.st_mode) and info.st_uid == os.getuid()
                and info.st_gid == self.namespace["gid"]
                and stat.S_IMODE(info.st_mode) == (0o600 if role == "owner" else 0o660),
                "instance_socket_changed", 503)
        self.record["sockets"][role] = dict(socket_metadata(info), path=str(self.paths[role]))
        self._save()

    def unlink_created(self, role, expected):
        try:
            self._namespace_current()
            require(self._read() == self.saved and self.record["owner"] == process_identity()[0],
                    "instance_record_changed", 503)
            info = self._stat(role)
            if info is None:
                return
            require(stat.S_ISSOCK(info.st_mode) and socket_metadata(info) == expected,
                    "instance_socket_changed", 503)
            os.unlink(self.paths[role].name, dir_fd=self.namespace_fd)
            os.fsync(self.namespace_fd)
        except (Refused, OSError):
            pass  # Leave changed/unknown objects and the record for explicit recovery.

    def finish(self):
        try:
            self._namespace_current()
            require(self._read() == self.saved and self.record["owner"] == process_identity()[0]
                    and all(self._stat(role) is None for role in self.paths),
                    "instance_cleanup_incomplete", 503)
            os.unlink(self.NAME, dir_fd=self.state_fd); os.fsync(self.state_fd)
        except (Refused, OSError):
            pass
        finally:
            self.release()

    def release(self):
        for name in ("state_fd", "namespace_fd"):
            fd = getattr(self, name, None)
            if fd is not None:
                os.close(fd); setattr(self, name, None)

class UnixServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = False
    block_on_close = True
    request_queue_size = 8

    def __init__(self, path, adapter, *, owner_role=False, production=True, instance=None):
        path = Path(path)
        require(not os.path.lexists(path), "socket_already_exists", 503)
        require(not any(p.is_symlink() for p in (path.parent, *path.parent.parents)),
                "socket_directory_untrusted", 503)
        info = path.parent.stat()
        require(info.st_uid == os.getuid() and stat.S_ISDIR(info.st_mode), "socket_directory_untrusted", 503)
        if production:
            require(os.getuid() == 1000 and info.st_gid == 984
                    and stat.S_IMODE(info.st_mode) == 0o2750
                    and str(path) == (OWNER_SOCKET if owner_role else BROWSER_SOCKET),
                    "socket_directory_untrusted", 503)
        else:
            require(not info.st_mode & 0o077, "fixture_directory_untrusted", 503)
        self.adapter, self.owner_role, self.path = adapter, owner_role, path
        self.created_identity = None
        self.instance = instance
        self.role = 'owner' if owner_role else 'browser'
        self.created_metadata = None
        super().__init__(str(path), Handler)
        os.chmod(path, 0o600 if owner_role else 0o660)
        current = path.stat()
        self.created_identity = current.st_dev, current.st_ino
        self.created_metadata = socket_metadata(current)
        if self.instance is not None:
            try:
                self.instance.created(self.role, current)
            except BaseException:
                self.server_close()
                raise

    def server_close(self):
        super().server_close()
        if self.created_identity and self.instance is not None:
            self.instance.unlink_created(self.role, self.created_metadata)
            self.created_identity = None
        if self.created_identity:
            try:
                current = self.path.lstat()
                if (current.st_dev, current.st_ino) == self.created_identity:
                    self.path.unlink()
            except FileNotFoundError:
                pass
            self.created_identity = None

class RunningAdapter:
    def __init__(self, manager):
        self._start(manager, FrozenApplication(ROOT), ROOT / ".rr-feedback", provider_key,
                    {"browser": Path(BROWSER_SOCKET), "owner": Path(OWNER_SOCKET)}, production=True)

    @classmethod
    def for_fixture(cls, manager, directory, store_root, key):
        """Isolated public fixture with actual local UID/GID and no production FD."""
        result = cls.__new__(cls)
        directory = Path(directory)
        result._start(manager, FrozenApplication(ROOT), store_root, lambda: key,
                      {"browser": directory / "browser.sock", "owner": directory / "owner.sock"},
                      production=False)
        return result

    def _start(self, manager, app, store_root, key_source, paths, *, production):
        self.store, self.instance, self.servers, self.threads = None, None, [], []
        try:
            self.store = FeedbackStore(store_root)
            adapter = Adapter(manager, app, self.store, key_source(),
                              gateway_uid=996 if production else os.getuid(),
                              owner_uid=1000 if production else os.getuid())
            self.instance = SocketInstance(self.store, paths, production=production)
            for role, path in paths.items():
                self.servers.append(UnixServer(path, adapter, owner_role=role == "owner",
                                               production=production, instance=self.instance))
            for server in self.servers:
                thread = threading.Thread(target=server.serve_forever, name="csp-rr")
                thread.start(); self.threads.append(thread)
        except BaseException:
            self.close()
            raise

    def close(self):
        errors = []
        for server, thread in zip(self.servers, self.threads):
            try: server.shutdown()
            except Exception as error: errors.append(error)
        for server in self.servers:
            try: server.server_close()
            except Exception as error: errors.append(error)
        for thread in self.threads:
            try: thread.join()
            except Exception as error: errors.append(error)
        if self.instance is not None:
            try: self.instance.finish()
            except Exception as error: errors.append(error)
            self.instance = None
        if self.store is not None:
            try: self.store.close()
            except Exception as error: errors.append(error)
            self.store = None
        if errors:
            raise errors[0]

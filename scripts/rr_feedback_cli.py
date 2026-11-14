#!/usr/bin/env python3
"""Owner-only RR feedback CLI; ack always reads and hashes actual bytes first."""
from __future__ import annotations
import argparse
import http.client
import json
import os
from pathlib import Path
import socket
import stat
import struct
from rr_adapter import (AGENT, MAX_BODY, Refused, canonical, digest, loads, require, uuid_text)
from rr_manifest import OWNER_SOCKET

class OwnerClient:
    def __init__(self, path=OWNER_SOCKET):
        self.path = Path(path)

    def request(self, method, path, payload=None, token=None):
        require(os.getuid() == 1000, "owner_identity_required", 403)
        require(not any(p.is_symlink() for p in (self.path, *self.path.parents)),
                "owner_socket_untrusted", 403)
        st = self.path.stat()
        require(stat.S_ISSOCK(st.st_mode) and st.st_uid == os.getuid()
                and stat.S_IMODE(st.st_mode) == 0o600, "owner_socket_untrusted", 403)
        connection = http.client.HTTPConnection("rr-owner.local", timeout=5)
        peer = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            peer.settimeout(5); peer.connect(str(self.path))
            _, uid, _ = struct.unpack("3i", peer.getsockopt(socket.SOL_SOCKET, socket.SO_PEERCRED, 12))
            require(uid == os.getuid(), "owner_peer_refused", 403)
            connection.sock = peer
            body = b"" if payload is None else canonical(payload)
            headers = {"Host": "rr-owner.local", "Content-Length": str(len(body))}
            if token:
                headers["X-RR-Read-Token"] = token
            if payload is not None:
                headers["Content-Type"] = "application/json"
            connection.request(method, path, body=body, headers=headers)
            response = connection.getresponse()
            require(response.getheader("Transfer-Encoding") is None, "owner_response_invalid", 503)
            length = response.getheader("Content-Length", "")
            require(length.isdigit() and int(length) <= MAX_BODY, "owner_response_invalid", 503)
            raw = response.read(int(length) + 1)
            require(len(raw) == int(length), "owner_response_invalid", 503)
            require(response.status == 200, "owner_request_refused", response.status)
            return raw
        finally:
            connection.close(); peer.close()

    def read(self, fid):
        uuid_text(fid)
        record = loads(self.request("GET", AGENT + "/" + fid))
        require(record["feedback_id"] == fid and digest(canonical(record["payload"])) == record["payload_sha256"],
                "feedback_digest_mismatch", 409)
        hashes = []
        for item in record["attachments"]:
            raw = self.request("GET", AGENT + "/" + fid + "/attachments/" + item["attachment_id"],
                               token=record["read_token"])
            require(len(raw) == item["size"] and digest(raw) == item["sha256"],
                    "attachment_digest_mismatch", 409)
            hashes.append({"attachment_id": item["attachment_id"], "sha256": digest(raw)})
        return record, hashes

    def ack(self, fid):
        record, hashes = self.read(fid)
        return loads(self.request("POST", AGENT + "/" + fid + "/ack",
                                  {"revision": record["revision"],
                                   "payload_sha256": digest(canonical(record["payload"])),
                                   "attachments": hashes, "read_token": record["read_token"]}))

    def result(self, fid, summary, references):
        record, _ = self.read(fid)
        return loads(self.request("POST", AGENT + "/" + fid + "/result",
                                  {"revision": record["revision"], "summary": summary,
                                   "references": references}))

def main(argv=None, *, client=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list")
    listing.add_argument("--state", choices=("pending", "agent_read", "processed"), default="pending")
    listing.add_argument("--limit", type=int, default=20)
    listing.add_argument("--cursor", default="")
    for command in ("read", "ack", "result"):
        sub = commands.add_parser(command)
        sub.add_argument("feedback_id")
        if command == "result":
            sub.add_argument("--summary", required=True)
            sub.add_argument("--reference", action="append", default=[])
    args = parser.parse_args(argv)
    client = client or OwnerClient()
    try:
        if args.command == "list":
            require(1 <= args.limit <= 100, "invalid_query")
            if args.cursor:
                uuid_text(args.cursor)
            query = "?state=" + args.state + "&limit=" + str(args.limit)
            if args.cursor:
                query += "&cursor=" + args.cursor
            result = loads(client.request("GET", AGENT + query))
        elif args.command == "read":
            result, _ = client.read(args.feedback_id)
            result.pop("read_token", None)
        elif args.command == "ack":
            result = client.ack(args.feedback_id)
        else:
            result = client.result(args.feedback_id, args.summary, args.reference)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except (Refused, OSError, KeyError, ValueError):
        print(json.dumps({"error": "feedback_cli_failed"}))
        return 1

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Safe repository content paths for learn_server (notes / plans)."""

from __future__ import annotations

import re
from pathlib import Path

ALLOWED_PREFIXES = ("rounds/", "plans/")
ALLOWED_SUFFIXES = (".md", ".txt")

ROUND_NOTES_RE = re.compile(
    r"^rounds/round_\d{2}/(week[123]|final)/notes\.md$"
)


def resolve_content_path(repo_root: Path, rel_path: str) -> Path | None:
    """Return absolute path if rel_path is allowed, else None."""
    rel = rel_path.strip().replace("\\", "/").lstrip("/")
    if not rel or ".." in rel.split("/"):
        return None
    if not any(rel.startswith(p) for p in ALLOWED_PREFIXES):
        return None
    if not any(rel.endswith(s) for s in ALLOWED_SUFFIXES):
        return None

    full = (repo_root / rel).resolve()
    try:
        full.relative_to(repo_root.resolve())
    except ValueError:
        return None
    if not full.is_file():
        return None
    return full


def markdown_to_html(text: str) -> str:
    """Minimal Markdown → HTML (no external deps)."""
    lines = text.splitlines()
    out: list[str] = []
    in_code = False
    in_ul = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            close_ul()
            if in_code:
                out.append("</code></pre>")
                in_code = False
            else:
                out.append("<pre><code>")
                in_code = True
            continue
        if in_code:
            out.append(line)
            continue

        if line.startswith("# "):
            close_ul()
            out.append(f"<h1>{inline_format(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            close_ul()
            out.append(f"<h2>{inline_format(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            close_ul()
            out.append(f"<h3>{inline_format(line[4:].strip())}</h3>")
        elif line.startswith("- ") or line.startswith("* "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_format(line[2:].strip())}</li>")
        elif re.match(r"^\d+\.\s", line):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            content = re.sub(r"^\d+\.\s", "", line)
            out.append(f"<li>{inline_format(content.strip())}</li>")
        elif not line.strip():
            close_ul()
            out.append("<br>")
        else:
            close_ul()
            out.append(f"<p>{inline_format(line)}</p>")

    close_ul()
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def inline_format(text: str) -> str:
    text = escape_html(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )

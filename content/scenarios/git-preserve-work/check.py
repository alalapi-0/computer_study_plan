import json
import os
import stat
import subprocess
import sys
from pathlib import Path

GOOD_APP = b"def total(values):\n    return sum(values)\n\nprint(total([4, 5, 6]))\n"
DRAFT = b"color=violet\ndraft_note=keep-me\n"
EXPECTED_HEAD = "b97793c2931dd3bcffb091769bb70c6a7228c406"
EXPECTED_PARENT = "dfd20b96cecfbe04a08b0e8b78a34f873e283eb5"


def emit(**payload):
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def regular(path, limit):
    try:
        st = path.lstat()
    except OSError:
        return False
    return stat.S_ISREG(st.st_mode) and not path.is_symlink() and st.st_size <= limit


mode = sys.argv[1] if len(sys.argv) > 1 else "check"
repo = Path("/workspace/repo")
if mode == "ready":
    ready = Path("/usr/bin/git").exists() and (repo / ".git").is_dir() and (repo / "app.py").exists()
    emit(ready=ready, passed=False, evidence=["Git and disposable repository available"] if ready else ["Git platform or setup repository missing"])
    raise SystemExit(0)
app = repo / "app.py"
draft = repo / "settings.ini"
if not regular(app, 16_384) or not regular(draft, 4096):
    emit(ready=True, passed=False, evidence=["solution files must remain bounded regular files"])
    raise SystemExit(0)
try:
    git_env = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")
    run = subprocess.run(["/usr/bin/python3", "app.py"], cwd=repo, text=True, capture_output=True, timeout=3)
    status = subprocess.run(["/usr/bin/git", "status", "--porcelain=v1"], cwd=repo, env=git_env, text=True, capture_output=True, timeout=3)
    identities = subprocess.run(["/usr/bin/git", "rev-parse", "HEAD", "HEAD^"], cwd=repo, env=git_env, text=True, capture_output=True, timeout=3)
    ancestry = subprocess.run(["/usr/bin/git", "rev-list", "HEAD"], cwd=repo, env=git_env, text=True, capture_output=True, timeout=3)
    replace_refs = subprocess.run(["/usr/bin/git", "for-each-ref", "--format=%(refname) %(objectname)", "refs/replace"], cwd=repo, env=git_env, text=True, capture_output=True, timeout=3)
    object_format = subprocess.run(["/usr/bin/git", "rev-parse", "--show-object-format"], cwd=repo, env=git_env, text=True, capture_output=True, timeout=3)
except (OSError, subprocess.TimeoutExpired) as exc:
    emit(ready=True, passed=False, evidence=[f"repository verification failed safely: {type(exc).__name__}"])
    raise SystemExit(0)
lines = status.stdout.splitlines()
draft_preserved = draft.read_bytes() == DRAFT and any(line.endswith(" settings.ini") for line in lines)
identity_lines = identities.stdout.splitlines()
ancestry_lines = ancestry.stdout.splitlines()
replace_ref_lines = replace_refs.stdout.splitlines()
metadata_safe = not (repo / ".git/shallow").exists() and not (repo / ".git/info/grafts").exists()
history_exact = (
    identities.returncode == ancestry.returncode == replace_refs.returncode == object_format.returncode == 0
    and identity_lines == [EXPECTED_HEAD, EXPECTED_PARENT]
    and ancestry_lines == [EXPECTED_HEAD, EXPECTED_PARENT]
    and replace_ref_lines == []
    and object_format.stdout.strip() == "sha1"
    and metadata_safe
)
passed = app.read_bytes() == GOOD_APP and draft_preserved and run.returncode == 0 and run.stdout == "15\n" and history_exact
emit(ready=True, passed=passed, evidence=[f"program output={run.stdout.strip()!r}", f"status={lines!r}", f"HEAD/parent={identity_lines!r}", "exact original two-commit ancestry preserved" if history_exact else "original commit identities or ancestry changed"])

#!/bin/bash
set -euo pipefail
mkdir -p /workspace/repo
cd /workspace/repo
git init -q -b main --object-format=sha1
git config user.name 'Scenario Builder'
git config user.email 'scenario@example.invalid'
git config commit.gpgsign false
git config core.autocrlf false
git config core.filemode true
export GIT_AUTHOR_NAME='Scenario Builder'
export GIT_AUTHOR_EMAIL='scenario@example.invalid'
export GIT_COMMITTER_NAME='Scenario Builder'
export GIT_COMMITTER_EMAIL='scenario@example.invalid'
cat > app.py <<'PY'
def total(values):
    return sum(values)

print(total([4, 5, 6]))
PY
printf 'color=blue\n' > settings.ini
git add app.py settings.ini
export GIT_AUTHOR_DATE='2026-01-01T00:00:00+0000'
export GIT_COMMITTER_DATE='2026-01-01T00:00:00+0000'
git commit -qm 'known good calculator'
cat > app.py <<'PY'
def total(values):
    return len(values)

print(total([4, 5, 6]))
PY
git add app.py
export GIT_AUTHOR_DATE='2026-01-02T00:00:00+0000'
export GIT_COMMITTER_DATE='2026-01-02T00:00:00+0000'
git commit -qm 'regression in calculator'
printf 'color=violet\ndraft_note=keep-me\n' > settings.ini

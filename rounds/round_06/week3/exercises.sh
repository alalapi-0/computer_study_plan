#!/bin/bash
# Round 06 · Week 3 练习：SSH / rsync / crontab 命令排练（Web UI 可运行）

set -e

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
LAB="$HOME/cli-lab/round6/week3_auto"

mark() {
  bash "$REPO_ROOT/mark_done.sh" "$1"
}

rm -rf "$LAB"
mkdir -p "$LAB/local_files"
cd "$LAB"

cat > local_files/sync_demo.txt <<'EOF'
This file is used for rsync/scp command rehearsal.
EOF

cat > remote_rehearsal.md <<'EOF'
# Remote Ops Rehearsal

These commands are examples only. The Web UI terminal blocks real remote/network commands.

```bash
ssh user@host
scp local_files/sync_demo.txt user@host:~/round6/
rsync -avz local_files/ user@host:~/round6/
```
EOF

cat > cron_examples.txt <<'EOF'
# Every five minutes:
*/5 * * * * bash ~/round6/healthcheck.sh >> ~/round6/healthcheck.log 2>&1

# Every day at 02:00:
0 2 * * * bash ~/round6/backup.sh >> ~/round6/backup.log 2>&1
EOF

cat > local_sync_plan.sh <<'EOF'
#!/bin/bash
set -e
mkdir -p dry_run_remote
cp local_files/sync_demo.txt dry_run_remote/sync_demo.txt
find dry_run_remote -type f -print
EOF

chmod +x local_sync_plan.sh
./local_sync_plan.sh

echo "remote-rehearsal:"
cat remote_rehearsal.md

echo "cron-examples:"
cat cron_examples.txt

mark r06-w3-ex3

echo "Week 3 自动练习完成。请继续在 Web UI 点击“记录并完成”保存 r06-w3-self。"

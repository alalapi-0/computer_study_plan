#!/bin/bash
set -euo pipefail
mkdir -p /workspace/data /workspace/bin
printf 'north,12\nsouth,8\nwest,15\n' > /workspace/data/sales.csv
cat > /workspace/bin/generate_report.sh <<'SH'
#!/bin/bash
set -euo pipefail
input=/workspace/data/sales.csv
output=/workspace/report.tsv
rows=$(wc -c < "$input")
total=0
while IFS=, read -r region amount; do
  total=$((total + amount))
done < "$input"
printf 'rows\ttotal\n%s\t%s\n' "$rows" "$total" > "$output"
cat "$output"
SH
chmod +x /workspace/bin/generate_report.sh
/workspace/bin/generate_report.sh >/dev/null

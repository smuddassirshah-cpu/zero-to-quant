#!/usr/bin/env bash
# Runs the commands given on stdin, one per line, from app/ (docs/CI.md). Each command: its output is cut to the last 40 lines, its exit code
# is kept (pipefail), its wall clock is printed. A failing command does not stop the rest; the exit code is 1 if any failed, with a table at the end.
# Blank lines and lines starting with # are skipped.
#   bash tools/ci-run.sh <<'EOF'
#   node tools/test-capstone.mjs
#   node tools/test-check-first.mjs --mobile
#   EOF
set -o pipefail
fails=()
rows=()
while IFS= read -r line; do
  case "$line" in ''|'#'*) continue ;; esac
  echo "::group::$line"
  t0=$(date +%s)
  bash -c "set -o pipefail; $line 2>&1 | tail -40"
  code=$?
  secs=$(( $(date +%s) - t0 ))
  echo "::endgroup::"
  if [ "$code" -ne 0 ]; then
    echo "::error::FAILED ($code, ${secs} s): $line"
    fails+=("$line")
    rows+=("FAIL ${secs}s  $line")
  else
    rows+=("ok   ${secs}s  $line")
  fi
done
printf '%s\n' "${rows[@]}"
if [ "${#fails[@]}" -gt 0 ]; then
  echo "ci-run: ${#fails[@]} of ${#rows[@]} commands failed"
  exit 1
fi
echo "ci-run: all ${#rows[@]} commands passed"

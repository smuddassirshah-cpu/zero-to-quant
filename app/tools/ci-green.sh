#!/usr/bin/env bash
# Helpers for the green-hash cache in .github/workflows/acceptance.yml (docs/CI.md, "The green-hash cache"). Run from app/.
#   PT_ARGS="--all --shard 3/16 --no-routes --mobile" bash tools/ci-green.sh select <label> [cache-file]
#       Runs `node tools/playthrough.mjs $PT_ARGS --changed --list --cache <file>` (no browser, about a second), prints the line it reports
#       ("changed: K of N items ..."), and records it for the job:
#         - $GITHUB_OUTPUT: k, n, before (the sha1 of the cache file now, or "none")
#         - $ZQ_CHANGED_FILE (default $RUNNER_TEMP/changed.txt): "<label>: changed K of N", which the job uploads and the acceptance job prints
#   bash tools/ci-green.sh dirty <before> [cache-file]
#       Writes dirty=true to $GITHUB_OUTPUT when the cache file exists and is not what it was after the restore (the job recorded a green), else dirty=false.
# Locally: PT_ARGS="--lesson number-sense/l1-what-a-fraction-measures --no-routes" bash tools/ci-green.sh select local /tmp/some-cache.json
set -o pipefail
cmd="${1:-}"; label="${2:-}"
sum() { if [ -f "$1" ]; then sha1sum "$1" | cut -d' ' -f1; else echo none; fi; }
out() { if [ -n "${GITHUB_OUTPUT:-}" ]; then echo "$1" >> "$GITHUB_OUTPUT"; else echo "output: $1"; fi; }
case "$cmd" in
  select)
    file="${3:-tools/.green-cache.json}"
    [ -n "$label" ] || { echo "ci-green: select needs a label" >&2; exit 2; }
    err=$(mktemp)
    # word splitting of $PT_ARGS is intended: it is a list of flags
    node tools/playthrough.mjs $PT_ARGS --changed --list --cache "$file" > /dev/null 2> "$err"
    code=$?
    line=$(grep '^changed:' "$err" | tail -1)
    if [ "$code" -ne 0 ] || [ -z "$line" ]; then echo "::error::the --changed --list selection failed (exit $code)"; tail -20 "$err"; exit 1; fi
    k=$(echo "$line" | sed -n 's/^changed: \([0-9][0-9]*\) of \([0-9][0-9]*\) items.*/\1/p')
    n=$(echo "$line" | sed -n 's/^changed: \([0-9][0-9]*\) of \([0-9][0-9]*\) items.*/\2/p')
    [ -n "$k" ] && [ -n "$n" ] || { echo "::error::cannot read K and N from: $line"; exit 1; }
    echo "$line"
    out "k=$k"; out "n=$n"; out "before=$(sum "$file")"
    echo "$label: changed $k of $n" > "${ZQ_CHANGED_FILE:-${RUNNER_TEMP:-/tmp}/changed.txt}"
    ;;
  dirty)
    file="${3:-tools/.green-cache.json}"
    now=$(sum "$file")
    if [ "$now" != none ] && [ -n "$label" ] && [ "$now" != "$label" ]; then out dirty=true; else out dirty=false; fi
    ;;
  *) echo "usage: ci-green.sh select <label> [file] | dirty <before> [file]" >&2; exit 2 ;;
esac

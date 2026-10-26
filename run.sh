#!/usr/bin/env bash
# Session loop: runs one fresh Claude Code session per iteration from NEXT_PROMPT.md
# until a file named DONE exists at the repo root. Uses the project's own
# permission settings (.claude/settings.json if present); adds no bypass flags.
cd "$(dirname "$0")"
touch loop.log
i=0
while [ ! -f DONE ]; do
  i=$((i + 1))
  if [ ! -f NEXT_PROMPT.md ]; then
    echo "$(date -u +%FT%TZ) iteration $i: NEXT_PROMPT.md missing, stopping" | tee -a loop.log
    exit 1
  fi
  echo "$(date -u +%FT%TZ) iteration $i: start" >> loop.log
  claude -p "$(cat NEXT_PROMPT.md)"
  status=$?
  echo "$(date -u +%FT%TZ) iteration $i: exit $status" >> loop.log
  if [ $status -ne 0 ]; then
    echo "iteration $i exited $status; pausing 60 s before retrying" | tee -a loop.log
    sleep 60
  fi
done
echo "$(date -u +%FT%TZ) DONE found after $i iterations" | tee -a loop.log

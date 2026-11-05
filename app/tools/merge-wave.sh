#!/usr/bin/env bash
# merge-wave.sh: merge parallel worktree branches into the current branch by rule.
#
# Usage (from the repo root, on the branch to merge into):
#   app/tools/merge-wave.sh <branch> [<branch>...]
#
# Per branch: git merge --no-ff --no-commit, then resolve conflicts by rule:
#   app/content/drills/index.json   union by id (ours first, then theirs' new ids)
#   docs/BACKLOG-INBOX.md           keep both sides (ours, then theirs)
#   app/content/courses/*/review-*.json   side whose last commit on the file is newer
#   PROGRESS.md, docs/reports/*.md, docs/reviews/*.md   keep both sides
#   anything else                   abort that merge, print UNRESOLVED, go on
# Then: conflict-marker scan of the lines the merge adds, `node tools/validate.mjs`
# from app/ (manifest.json is staged), commit "Merge <branch> (merge-wave)".
# Output: verbose log in ${TMPDIR:-/tmp}/merge-wave.log; the last lines are one
# status per branch (merged, unresolved, invalid), "validator: N errors", OK or FAIL.
# Exit 0 only if every branch merged. The working tree must be clean.
set -u
[ $# -ge 1 ] || { echo "usage: $0 <branch> [<branch>...]" >&2; exit 2; }
ROOT=$(git rev-parse --show-toplevel) || exit 2
cd "$ROOT" || exit 2
LOG="${TMPDIR:-/tmp}/merge-wave.log"; : > "$LOG"
if ! git diff --quiet HEAD; then echo "working tree not clean" >&2; exit 2; fi

summary=(); fail=0; verr=0

join_json() { # union by id: node script; args: ours theirs out
  node -e '
const fs=require("fs");
const [o,t,out]=process.argv.slice(1).map(String);
const A=JSON.parse(fs.readFileSync(o,"utf8")),B=JSON.parse(fs.readFileSync(t,"utf8"));
const pick=x=>Array.isArray(x)?x:Object.keys(x).find(k=>Array.isArray(x[k]));
const la=Array.isArray(A)?A:A[pick(A)], lb=Array.isArray(B)?B:B[pick(B)];
const seen=new Set(la.map(e=>e.id));
for(const e of lb){ if(!seen.has(e.id)){seen.add(e.id);la.push(e);} }
fs.writeFileSync(out,JSON.stringify(A,null,2)+"\n");
' "$1" "$2" "$3"
}

resolve_file() { # path branch ; returns 0 if resolved
  local f=$1 br=$2 d
  d=$(mktemp -d)
  case "$f" in
    app/content/drills/index.json)
      git show ":2:$f" > "$d/o" 2>/dev/null && git show ":3:$f" > "$d/t" 2>/dev/null || return 1
      join_json "$d/o" "$d/t" "$f" >>"$LOG" 2>&1 || return 1 ;;
    docs/BACKLOG-INBOX.md|PROGRESS.md|docs/reports/*.md|docs/reviews/*.md)
      git show ":2:$f" > "$d/o" 2>/dev/null && git show ":3:$f" > "$d/t" 2>/dev/null || return 1
      git show ":1:$f" > "$d/b" 2>/dev/null || : > "$d/b"
      cp "$d/o" "$f"
      git merge-file --union "$f" "$d/b" "$d/t" >>"$LOG" 2>&1
      [ $? -lt 128 ] || return 1 ;;
    app/content/courses/*/review-*.json)
      local ho bo
      ho=$(git log -1 --format=%ct HEAD -- "$f"); bo=$(git log -1 --format=%ct "$br" -- "$f")
      if [ "${bo:-0}" -gt "${ho:-0}" ]; then git checkout --theirs -- "$f" || return 1
      else git checkout --ours -- "$f" || return 1; fi ;;
    *) return 1 ;;
  esac
  git add -- "$f"
}

for br in "$@"; do
  echo "== $br" >>"$LOG"
  if ! git rev-parse -q --verify "$br^{commit}" >/dev/null; then
    summary+=("invalid $br: no such branch"); fail=1; continue
  fi
  git merge --no-ff --no-commit "$br" >>"$LOG" 2>&1
  if ! git rev-parse -q --verify MERGE_HEAD >/dev/null; then
    if git diff --quiet HEAD && git merge-base --is-ancestor "$br" HEAD; then
      summary+=("merged $br (already up to date)"); continue
    fi
    git merge --abort >/dev/null 2>&1
    summary+=("invalid $br: merge refused"); fail=1; continue
  fi
  conflicted=$(git diff --name-only --diff-filter=U)
  bad=""
  for f in $conflicted; do resolve_file "$f" "$br" || bad="$bad $f"; done
  if [ -n "$bad" ]; then
    git merge --abort >/dev/null 2>&1
    echo "UNRESOLVED $br:$bad" | tee -a "$LOG"
    summary+=("unresolved $br:$bad"); fail=1; continue
  fi
  git add -A -- . >/dev/null 2>&1
  # markers newly added by the merge (diff against HEAD, added lines only)
  if git diff --cached -U0 HEAD | grep -E '^\+(<<<<<<< |>>>>>>> |=======$)' >>"$LOG"; then
    git merge --abort >/dev/null 2>&1
    summary+=("invalid $br: conflict markers remain"); fail=1; continue
  fi
  out=$(cd app && node tools/validate.mjs 2>&1); echo "$out" | tail -40 >>"$LOG"
  n=$(echo "$out" | grep -Eo '^[0-9]+ errors?' | tail -1 | grep -Eo '^[0-9]+')
  if [ -z "$n" ] || [ "$n" -gt 0 ]; then
    verr=${n:-999}
    git merge --abort >/dev/null 2>&1
    summary+=("invalid $br: validator ${n:-failed} errors"); fail=1; continue
  fi
  verr=0
  git add -A -- app/content/manifest.json >/dev/null 2>&1
  if git commit -q -m "Merge $br (merge-wave)" >>"$LOG" 2>&1; then
    summary+=("merged $br")
  else
    git merge --abort >/dev/null 2>&1
    summary+=("invalid $br: commit failed"); fail=1
  fi
done

echo "log: $LOG"
for s in "${summary[@]}"; do echo "$s"; done
echo "validator: $verr errors"
if [ $fail -eq 0 ]; then echo OK; else echo FAIL; fi
exit $fail

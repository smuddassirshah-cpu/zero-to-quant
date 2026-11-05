#!/usr/bin/env bash
# test-merge-wave.sh: clone the repo, make two branches that conflict in
# drills/index.json, BACKLOG-INBOX.md and one review file, merge them with
# merge-wave.sh and assert the result. Prints PASS or FAIL (last line).
set -u
SRC=$(git rev-parse --show-toplevel); T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
git clone -q "$SRC" "$T/r" 2>/dev/null || { echo "FAIL: clone"; exit 1; }
cd "$T/r"; git config user.email t@t; git config user.name t
cp "$SRC/app/tools/merge-wave.sh" app/tools/merge-wave.sh   # the script under test may be uncommitted
git add -A; git commit -q -m "base" ; BASE=$(git rev-parse --abbrev-ref HEAD)
# drill ids that have a file but no index entry (the validator needs a real file)
FREE=($(for f in app/content/drills/*.json; do i=$(basename "$f" .json); [ "$i" = index ] || grep -q "\"$i\"" app/content/drills/index.json || echo "$i"; done | head -3))
[ ${#FREE[@]} -eq 3 ] || { echo "FAIL: need 3 unlisted drill files"; exit 1; }
REV=$(ls app/content/courses/*/review-*.json | head -1)
edit() { # branch tag date
  git checkout -q -b "$1" "$BASE"
  node -e '
const fs=require("fs"),[tag,rev,...fa]=process.argv.slice(1);
const i="app/content/drills/index.json",d=JSON.parse(fs.readFileSync(i));
for(const id of [fa[tag==="a"?0:1],fa[2]])d.push({id,name:"Test "+id,course:"py-found",difficulty:1});
fs.writeFileSync(i,JSON.stringify(d,null,2)+"\n");
const r=JSON.parse(fs.readFileSync(rev));r.items[0].prose="side-"+tag+" "+r.items[0].prose;
fs.writeFileSync(rev,JSON.stringify(r,null,2)+"\n");' "$2" "$REV" "${FREE[@]}"
  echo "inbox line $2" >> docs/BACKLOG-INBOX.md
  git add -A; GIT_COMMITTER_DATE="$3" git commit -q -m "branch $2"
}
edit wave-a a "2026-01-01T00:00:00Z"
edit wave-b b "2026-01-02T00:00:00Z"
git checkout -q "$BASE"
OUT=$(app/tools/merge-wave.sh wave-a wave-b 2>&1); RC=$?
echo "$OUT" | tail -6
fail=""
[ $RC -eq 0 ] || fail="$fail exit=$RC"
git grep -n -E '^(<<<<<<< |>>>>>>> )' -- app docs >/dev/null && fail="$fail markers"
for id in "${FREE[@]}"; do [ "$(grep -c "\"id\": \"$id\"" app/content/drills/index.json)" = 1 ] || fail="$fail drill-$id"; done
grep -q "inbox line a" docs/BACKLOG-INBOX.md && grep -q "inbox line b" docs/BACKLOG-INBOX.md || fail="$fail inbox"
grep -q "side-b" "$REV" && ! grep -q "side-a" "$REV" || fail="$fail review-newer"
(cd app && node tools/validate.mjs 2>&1 | grep -q '^0 errors') || fail="$fail validator"
[ -z "$(git status --porcelain)" ] || fail="$fail dirty"
[ -z "$fail" ] && echo "PASS merge-wave" || { echo "FAIL merge-wave:$fail"; exit 1; }

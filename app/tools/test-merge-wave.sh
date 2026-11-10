#!/usr/bin/env bash
# test-merge-wave.sh: clone the repo, make two branches that conflict in
# drills/index.json, BACKLOG-INBOX.md, one review file, the generated manifest.json (ours is taken, the validator regenerates it), docs/briefs/README.md and two
# adjacent rows of docs/readiness.md (session V), one branch also leaves content/readiness.json
# stale; merge them with merge-wave.sh and assert the result, including the readiness
# regeneration. Prints PASS or FAIL (last line).
set -u
SRC=$(git rev-parse --show-toplevel); T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
# A fresh repository holding a snapshot of the working tree (a clone fails in a shallow checkout: merges need history).
mkdir "$T/r" && cd "$T/r" && git init -q || { echo "FAIL: init"; exit 1; }
git config user.email t@t; git config user.name t
cp -r "$SRC/app" "$SRC/docs" "$SRC/PROGRESS.md" . 2>/dev/null || { echo "FAIL: copy"; exit 1; }
rm -rf app/node_modules
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
// a row must equal its drill file on name, course and difficulty (validator, ENGINE-BACKLOG 859), so copy them from the file
const row=(id,src)=>{const f=JSON.parse(fs.readFileSync("app/content/drills/"+src+".json"));return {id,name:f.name,course:f.course,difficulty:f.difficulty};};
for(const id of [fa[tag==="a"?0:1],fa[2]])d.push(row(id,id));
d.push(row("zz-"+tag,fa[0]));   // the new zz drill file below is a non-sample file, so it needs a row too
fs.writeFileSync(i,JSON.stringify(d,null,2)+"\n");
const r=JSON.parse(fs.readFileSync(rev));r.items[0].prose="side-"+tag+" "+r.items[0].prose;
fs.writeFileSync(rev,JSON.stringify(r,null,2)+"\n");' "$2" "$REV" "${FREE[@]}"
  # a new drill file on each side: the manifest lists it, so the two regenerated manifests collide on adjacent lines
  sed "s/\"id\": *\"${FREE[0]}\"/\"id\": \"zz-$2\"/" "app/content/drills/${FREE[0]}.json" > "app/content/drills/zz-$2.json"
  (cd app && node tools/validate.mjs >/dev/null 2>&1)
  echo "inbox line $2" >> docs/BACKLOG-INBOX.md
  echo "brief line $2" >> docs/briefs/README.md
  node -e '
const fs=require("fs"),tag=process.argv[1],k=tag==="a"?"algebra":"algo-think";
const t=fs.readFileSync("docs/readiness.md","utf8").split("\n").map(l=>l.startsWith("| `"+k+"` |")?l.replace(/\| [^|]* \|$/,"| reason-"+tag+" |"):l);
fs.writeFileSync("docs/readiness.md",t.join("\n"));
if(tag==="b"){const j=JSON.parse(fs.readFileSync("app/content/readiness.json"));j.zzStale=1;fs.writeFileSync("app/content/readiness.json",JSON.stringify(j,null,2)+"\n");}' "$2"
  git add -A; GIT_COMMITTER_DATE="$3" git commit -q -m "branch $2"
}
edit wave-a a "2026-01-01T00:00:00Z"
edit wave-b b "2026-01-02T00:00:00Z"
git checkout -q "$BASE"
OUT=$(app/tools/merge-wave.sh wave-a wave-b 2>&1); RC=$?
echo "$OUT" | tail -7
fail=""
[ $RC -eq 0 ] || fail="$fail exit=$RC"
git grep -n -E '^(<<<<<<< |>>>>>>> )' -- app docs >/dev/null && fail="$fail markers"
for id in "${FREE[@]}"; do [ "$(grep -c "\"id\": \"$id\"" app/content/drills/index.json)" = 1 ] || fail="$fail drill-$id"; done
grep -q "inbox line a" docs/BACKLOG-INBOX.md && grep -q "inbox line b" docs/BACKLOG-INBOX.md || fail="$fail inbox"
grep -q "side-b" "$REV" && ! grep -q "side-a" "$REV" || fail="$fail review-newer"
(cd app && node tools/validate.mjs 2>&1 | grep -q '^0 errors') || fail="$fail validator"
grep -q "drills/zz-a.json" app/content/manifest.json && grep -q "drills/zz-b.json" app/content/manifest.json || fail="$fail manifest-regenerated"
grep -q "brief line a" docs/briefs/README.md && grep -q "brief line b" docs/briefs/README.md || fail="$fail briefs"
NA=$(git show "$BASE:docs/readiness.md" | grep -c '^| `algebra` |')   # one row in each of the six role tables
[ "$(grep -c '^| `algebra` |.*reason-a |$' docs/readiness.md)" = "$NA" ] || fail="$fail readiness-row-ours"
[ "$(grep -c '^| `algo-think` |.*reason-b |$' docs/readiness.md)" = "$NA" ] || fail="$fail readiness-row-theirs"
[ "$(grep -c '^| `algebra` |' docs/readiness.md)" = "$(git show "$BASE:docs/readiness.md" | grep -c '^| `algebra` |')" ] || fail="$fail readiness-dup-rows"
grep -q zzStale app/content/readiness.json && fail="$fail readiness-json-stale"
(cd app && node tools/readiness-sums.mjs 2>&1 | grep -q '^OK') || fail="$fail readiness-check"
echo "$OUT" | grep -q '^readiness: regenerated' || fail="$fail readiness-status"
[ -z "$(git status --porcelain)" ] || fail="$fail dirty"
[ -z "$fail" ] && echo "PASS merge-wave" || { echo "FAIL merge-wave:$fail"; exit 1; }

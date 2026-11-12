#!/bin/sh
# Regenerates docs/reviews/triage-bands-ab.md.
# Usage: regen.sh <pkgs folder> [scratch dir] [commit the content was read at]
# Each step runs in under two minutes. Nothing here edits content or engine files.
# validate.mjs rewrites app/content/manifest.json: do not commit it.
set -e
PKGS="$1"; TMP="${2:-/tmp}"; HERE="$(cd "$(dirname "$0")" && pwd)"; APP="$HERE/../../../app"
SHA="${3:-$(cd "$HERE" && git rev-parse --short HEAD)}"
(cd "$APP" && node tools/validate.mjs > "$TMP/triage-validate.txt" 2>&1 || true)
(cd "$APP" && node tools/grade-regression.mjs --local-cdn "$PKGS" --out "$TMP/triage-gr.json" | tail -1)
cd "$HERE"
node dossier-bands.mjs "$TMP/triage-validate.txt" --local-cdn "$PKGS"
node dossier-selfgrade.mjs "$TMP/triage-gr.json" --local-cdn "$PKGS"
node fluency-selfgrade.mjs --local-cdn "$PKGS" --seeds 40
N1=$(grep -c '\[tight-band\]' "$TMP/triage-validate.txt")
N2=$(grep -c '\[wide-wrong-band\]' "$TMP/triage-validate.txt")
N3=$(node -e 'console.log(JSON.parse(require("fs").readFileSync("out/pile3.json")).length)')
node classify.mjs --local-cdn "$PKGS" --commit "$SHA" --counts "$N1,$N2,$N3"

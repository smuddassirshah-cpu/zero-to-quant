#!/usr/bin/env bash
# Build a local copy of what the app loads from cdn.jsdelivr.net, for
#   node tools/playthrough.mjs --local-cdn <dir>
# Needs github.com release downloads and registry.npmjs.org. Idempotent: anything already in place is skipped.
# Usage: app/tools/fetch-local-cdn.sh <dir>
set -euo pipefail

DIR="${1:-${ZQ_LOCAL_CDN:-}}"
[ -n "$DIR" ] || { echo "usage: $0 <dir>" >&2; exit 2; }
mkdir -p "$DIR"
DIR="$(cd "$DIR" && pwd)"

PYODIDE_VER=0.27.7
NPM_PKGS=(
  "mathlive@0.105.0"
  "@cortex-js/compute-engine@0.30.2"
  "@yowasp/clang@21.1.4-3"
)

# Pyodide: the full release distribution (core files plus every package wheel).
PY_OUT="$DIR/pyodide-$PYODIDE_VER/package"
if [ -f "$PY_OUT/pyodide.js" ] && [ -f "$PY_OUT/pyodide-lock.json" ]; then
  echo "skip pyodide $PYODIDE_VER (present)"
else
  echo "fetch pyodide $PYODIDE_VER"
  tmp="$(mktemp -d "$DIR/.tmp-pyodide.XXXXXX")"
  trap 'rm -rf "$tmp"' EXIT
  curl -fsSL --retry 3 -o "$tmp/pyodide.tar.bz2" \
    "https://github.com/pyodide/pyodide/releases/download/$PYODIDE_VER/pyodide-$PYODIDE_VER.tar.bz2"
  mkdir "$tmp/x"
  tar -xjf "$tmp/pyodide.tar.bz2" -C "$tmp/x"
  rm -f "$tmp/pyodide.tar.bz2"
  rm -rf "$DIR/pyodide-$PYODIDE_VER"
  mkdir -p "$DIR/pyodide-$PYODIDE_VER"
  # The archive holds a single top-level "pyodide/" folder.
  mv "$tmp/x/pyodide" "$PY_OUT"
  rm -rf "$tmp"; trap - EXIT
fi

# npm packages: the registry tarball unpacks to "package/".
for spec in "${NPM_PKGS[@]}"; do
  name="${spec%@*}"; ver="${spec##*@}"
  folder="$(printf '%s' "$name" | sed 's/^@//; s#/#-#')-$ver"
  if [ -f "$DIR/$folder/package/package.json" ]; then
    echo "skip $spec (present)"; continue
  fi
  echo "fetch $spec"
  tmp="$(mktemp -d "$DIR/.tmp-npm.XXXXXX")"
  trap 'rm -rf "$tmp"' EXIT
  base="${name##*/}"
  curl -fsSL --retry 3 -o "$tmp/pkg.tgz" "https://registry.npmjs.org/$name/-/$base-$ver.tgz"
  rm -rf "$DIR/$folder"; mkdir -p "$DIR/$folder"
  tar -xzf "$tmp/pkg.tgz" -C "$DIR/$folder"
  rm -rf "$tmp"; trap - EXIT
done

echo "done: $DIR"
du -sh "$DIR"

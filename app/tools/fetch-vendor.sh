#!/usr/bin/env bash
# Populate the self-hosting fallback folders the app reads when cdn.jsdelivr.net is unreachable:
#   <dir>/pyodide/         js/engine/widgets/code.js and js/screens/drill.js pass it to drill-worker.js (pyodide.mjs, wasm, lock file, wheels)
#   <dir>/mathlive/        js/engine/grade.js: mathlive.min.js with its fonts/ and sounds/ next to it
#   <dir>/compute-engine/  js/engine/grade.js: compute-engine.min.umd.js
#   <dir>/yowasp-clang/    js/screens/cpp-worker.js: the package's gen/ folder, directly in it
# Same sources and versions as tools/fetch-local-cdn.sh (Pyodide release tarball from github.com, npm tarballs from registry.npmjs.org).
# Every download is checked: npm tarballs against the registry's sha512 integrity, Pyodide files against the sha256 in its own pyodide-lock.json.
# Idempotent: a folder that is already complete is skipped. The downloaded folders are ignored by version control (root .gitignore); KaTeX stays tracked.
# Usage: app/tools/fetch-vendor.sh [--core] [<dir>]      <dir> defaults to app/vendor
#   --core  Pyodide core only (the npm package: about 12 MB, no wheels). Python that imports numpy, pandas, SciPy, scikit-learn,
#           statsmodels or matplotlib then fails offline. Without it the full release is fetched: 389 MB to download, 762 MB on disk.
set -euo pipefail

CORE=0
if [ "${1:-}" = "--core" ]; then CORE=1; shift; fi
DIR="${1:-$(cd "$(dirname "$0")/.." && pwd)/vendor}"
mkdir -p "$DIR"
DIR="$(cd "$DIR" && pwd)"

PYODIDE_VER=0.27.7
tmp="$(mktemp -d "$DIR/.tmp-vendor.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

# npm_fetch <name> <version> <outdir>: download, verify the registry's integrity, unpack to <outdir>/ (the tarball's "package/" folder)
npm_fetch() {
  local name="$1" ver="$2" out="$3" base="${1##*/}"
  curl -fsSL --retry 3 -o "$tmp/pkg.tgz" "https://registry.npmjs.org/$name/-/$base-$ver.tgz"
  local want got
  want="$(curl -fsSL --retry 3 "https://registry.npmjs.org/$name/$ver" | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).dist.integrity))')"
  got="sha512-$(openssl dgst -sha512 -binary "$tmp/pkg.tgz" | base64 -w0)"
  [ "$want" = "$got" ] || { echo "integrity mismatch for $name@$ver: registry $want, downloaded $got" >&2; exit 1; }
  rm -rf "$out"; mkdir -p "$out"
  tar -xzf "$tmp/pkg.tgz" -C "$out" --strip-components=1
  rm -f "$tmp/pkg.tgz"
}

# Pyodide
if [ -f "$DIR/pyodide/.complete" ] && [ "$(cat "$DIR/pyodide/.complete")" = "$PYODIDE_VER $CORE" ]; then
  echo "skip pyodide $PYODIDE_VER (present)"
else
  rm -rf "$DIR/pyodide"
  if [ "$CORE" = 1 ]; then
    echo "fetch pyodide $PYODIDE_VER (core only)"
    npm_fetch pyodide "$PYODIDE_VER" "$DIR/pyodide"
  else
    echo "fetch pyodide $PYODIDE_VER (full release, 389 MB)"
    curl -fsSL --retry 3 -o "$tmp/pyodide.tar.bz2" "https://github.com/pyodide/pyodide/releases/download/$PYODIDE_VER/pyodide-$PYODIDE_VER.tar.bz2"
    mkdir "$tmp/x"; tar -xjf "$tmp/pyodide.tar.bz2" -C "$tmp/x"; rm -f "$tmp/pyodide.tar.bz2"
    mv "$tmp/x/pyodide" "$DIR/pyodide"
    echo "verify pyodide files against pyodide-lock.json"
    node -e '
      const fs=require("fs"),c=require("crypto"),d=process.argv[1];
      const lock=JSON.parse(fs.readFileSync(d+"/pyodide-lock.json","utf8"));
      let n=0;
      for(const p of Object.values(lock.packages)){
        const h=c.createHash("sha256").update(fs.readFileSync(d+"/"+p.file_name)).digest("hex");
        if(h!==p.sha256){console.error("sha256 mismatch: "+p.file_name);process.exit(1);} n++;
      }
      for(const f of ["pyodide.mjs","pyodide.asm.wasm","python_stdlib.zip"]) if(!fs.existsSync(d+"/"+f)){console.error("missing "+f);process.exit(1);}
      console.log("  "+n+" packages match");' "$DIR/pyodide"
  fi
  [ -f "$DIR/pyodide/pyodide.mjs" ] || { echo "pyodide.mjs missing after unpack" >&2; exit 1; }
  echo "$PYODIDE_VER $CORE" > "$DIR/pyodide/.complete"
fi

# MathLive: the script finds fonts/ and sounds/ next to itself
if [ -f "$DIR/mathlive/mathlive.min.js" ] && [ -d "$DIR/mathlive/fonts" ]; then
  echo "skip mathlive (present)"
else
  echo "fetch mathlive@0.105.0"
  npm_fetch mathlive 0.105.0 "$tmp/ml"
  rm -rf "$DIR/mathlive"; mkdir -p "$DIR/mathlive"
  cp -r "$tmp/ml/mathlive.min.js" "$tmp/ml/fonts" "$tmp/ml/sounds" "$tmp/ml/mathlive-fonts.css" "$tmp/ml/LICENSE.txt" "$DIR/mathlive/"
  rm -rf "$tmp/ml"
fi

# Compute Engine
if [ -f "$DIR/compute-engine/compute-engine.min.umd.js" ]; then
  echo "skip compute-engine (present)"
else
  echo "fetch @cortex-js/compute-engine@0.30.2"
  npm_fetch @cortex-js/compute-engine 0.30.2 "$tmp/ce"
  rm -rf "$DIR/compute-engine"; mkdir -p "$DIR/compute-engine"
  cp "$tmp/ce/dist/compute-engine.min.umd.js" "$tmp/ce/LICENSE" "$DIR/compute-engine/"
  rm -rf "$tmp/ce"
fi

# YoWASP Clang: the package's gen/ folder, directly in the folder
if [ -f "$DIR/yowasp-clang/bundle.js" ]; then
  echo "skip yowasp-clang (present)"
else
  echo "fetch @yowasp/clang@21.1.4-3"
  npm_fetch @yowasp/clang 21.1.4-3 "$tmp/clang"
  rm -rf "$DIR/yowasp-clang"; mkdir -p "$DIR/yowasp-clang"
  cp "$tmp/clang/gen/"* "$DIR/yowasp-clang/"
  rm -rf "$tmp/clang"
fi

echo "done: $DIR"
du -sh "$DIR/pyodide" "$DIR/mathlive" "$DIR/compute-engine" "$DIR/yowasp-clang"

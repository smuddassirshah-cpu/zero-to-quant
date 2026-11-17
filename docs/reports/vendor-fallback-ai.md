# Vendor fallback (self-hosting) report

**Changed.** Pyodide: `code.js` and `drill.js` now pass the absolute `vendor/pyodide/` address as `indexURL`; `drill-worker.js` still tries the CDN first. MathLive and Compute Engine: `grade.js` `maths()` tries the CDN script (6 s), then `vendor/mathlive/mathlive.min.js` and `vendor/compute-engine/compute-engine.min.umd.js` (4 s); overall budget 10 s (was 6 s). `playthrough.mjs` ignores a failed HEAD probe of `vendor/` (Chromium reports a finished HEAD as aborted); `--local-cdn` still intercepts only jsDelivr.

**Added.** `app/tools/fetch-vendor.sh [--core] [<dir>]` (npm sha512 integrity, Pyodide sha256 from `pyodide-lock.json`; full release 389 MB download, 762 MB on disk; `--core` 14 MB, stdlib only). `app/tools/test-vendor-fallback.mjs --vendor <dir> [--absent]`. Root `.gitignore` covers the four folders. CI: added to the `python` leg of `tests-browser` (fetches from github.com and npm; `ci-coverage` passes). README and `docs/CI.md` updated.

**MathLive.** Its fonts and sounds resolve next to its script; fonts are skipped because KaTeX is already loaded, so only sounds load (on a key press).

**Results.** With the CDN blocked, `first-python/l1-calculator`, `cpp-pricing/l1-doubles` and `algebra/l1-symmetries` pass from vendor; `--absent` fails as expected (no local copy; the maths box degrades). Playthrough of the three, desktop and mobile, and the touched tests pass; validator 0 errors.

**Not done.** The Python lesson uses no wheel, so a NumPy load from vendor is not tested.

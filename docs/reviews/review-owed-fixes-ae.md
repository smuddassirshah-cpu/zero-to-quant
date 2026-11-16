# Owed fixes, session AE

Three small content fixes, one commit each.

## 1. ci-rebuild-from-orders: larger hidden test

Added hidden test 13 (all 12 earlier tests kept; `how` now says 13). Input: 99,980 ids, a left spine of 380 nodes over a balanced tree of 99,600 (height about 397, inside the 400 limit), compared with the expected tree built a second way.

Mechanism: an operation count, not time. The slicing solution (correct, `pre[1:i + 1]`, `ino[:i]`, `ino.index`) takes 2.35 s in Pyodide on this input, well inside the 5 s limit, so a time split is not reliable. The call passes `pre` and `ino` as a list subclass that counts elements copied by slices and scanned by `index`, and raises past 3,000,000 (30 per id). The dict solution does neither.

Timings in Pyodide 0.27.7 (whole test, build included): reference passes in 0.24 s; starter fails in 0.13 s; slicing solution stops with a RuntimeError in 0.09 s. Without the counter the slicing solution takes 2.35 s against 0.06 s for the reference.

Also: `docs/reports/drills-ci-4-check.py` now runs a case's `setup` line (it ignored it); it exits 0 on this drill. Page runtime: `planted-check` 0 failures, playthrough green with and without `--mobile`.

## 2. anticlockwise

14 vector-calc files: "counterclockwise" became "anticlockwise" in prose and option text, with "a" becoming "an". No id, key or answer string changed (options answer by id). Validator 0 errors, voice scan 0 and 0, `l5-divergence-and-curl` playthrough green both ways.

## 3. stage-2 build.py

`build.py` now reproduces the committed `stage-2.json` exactly (empty diff, data files unchanged). Drift found and brought into the script: item `a-spline-columns`, `"required": true` on five items (`a-walk-forward-ridge`, `b-eg-pair`, `c-three-pricers`, `c-kkt-code`, `d-signal-report`), and the `sign` wrong answer with its feedback on `b-yule-walker` and `b-df-hand`. `check_numbers.py`: 790 of 790.

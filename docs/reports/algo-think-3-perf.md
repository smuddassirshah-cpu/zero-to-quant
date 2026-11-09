# algo-think level 3: performance task

`homework-3.json`, `h-ring-search`, item 9 of 9 (added). Kind `code` (Python).

Matched objective: l9-halving "Implement binary search and handle its edge cases."

Task: find a sequence number in a ring buffer, a sorted list turned once (rotated-array search). New to the course.

Tests: 13 hidden, 1 example. Nine planted slips fail: `<` in the in-order test (5), `while lo < hi` (7), strict range at `lo` (9) or `hi` (8), two-step with `seq > ring[0]` (9), no check that `seq` is there (4, 10), unguarded empty ring (2), pivot search assuming a turn (3), sorted place (1). Test 13 sweeps every turn of lists of 0 to 12 numbers. A linear scan passes (graded on answers, as `how` says): slowest case 0.07 s in Pyodide 0.27.7 (Node).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/algo-think python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/algo-think-3-perf-numbers.py`: exit 0, failures 0.
4. `node tools/playthrough.mjs --set algo-think/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed; no wide display.

Freshness grep: ring, turned, rotated, oldest, slot, `find_trade`; `fresh-check --file`: no hit on the new item.

Overlapping screens: l9-halving screens[3] (`binary_search`), [5] (`first_at_least`) and [9]; new: the turn, the in-order half test, an unturned ring.

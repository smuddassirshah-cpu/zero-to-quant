# Engine pass AB (session AB): deep recursion, the 440 px feedback bar, the near-miss rule

Items 917, 914, 918, 919 of `docs/ENGINE-BACKLOG.md`. No file under `app/content/` was edited.

## Item 1 (917, 919): deep recursion on the Python code surfaces

### Reproduced first

A bare module worker on the app page (`drill-worker.js`, Pyodide 0.27.7, Chromium): an `lru_cache` recursion with two arguments 500 calls deep ends with the worker error `Maximum call stack size exceeded`; Pyodide is then "already fatally failed" and the page reads the run as a crash. A dict recursion with a generator in each call dies at about 450. A plain or dict recursion with no C code in the call passes at 900 and, with `sys.setrecursionlimit(100000)`, at 50,000. So the cause is the browser stack, not Python's limit: it is used up by C code at each call (the C `lru_cache` wrapper, a generator expression under `min`, `sorted` with a key, `map`). All surfaces share the one worker (`drill.js` and `code.js` both start `js/screens/drill-worker.js`; nothing else loads Pyodide), so one fix covers the drill page, lesson `code` screens, exams and the bank.

### The fix (`app/js/screens/drill-worker.js`)

1. `functools.lru_cache` and `functools.cache` are the pure-Python implementation (the stdlib's own, re-executed with the C wrapper hidden): they add no browser stack. About four times slower (160,000 states: 0.38 s against about 0.07 s).
2. `sys.setrecursionlimit(3000)` at the start of every run (one `lru_cache` call costs two Python frames). A learner's own `setrecursionlimit` still works and the next run starts again at 3,000.
3. A run that still overflows the stack (a generator in every call, say) no longer kills the grading: the overflowing test is reported as `RecursionError: maximum recursion depth exceeded. This recursion went too deep for the Python in this page ...`, a fresh Pyodide is loaded in the same worker (the page's 5-second clock is held with `pkgs` messages while it loads), and the tests after it run and are graded. An overflow while the code loads is a load error with the same message. A crash that is not a stack overflow keeps the old reporting ("Python stopped").
4. `ZQDrill.results()` carries `error` and `crash` (the test hook; no learner-facing change).

Measured safe depths (Chromium on this machine; docs in `docs/AUTHORING.md` section 5, "Deep recursion", and in the `code` section):

| Form | Safe to | Fails at |
| --- | --- | --- |
| plain or dict-remembered recursion | 2,900 (limit 3,000); 50,000 with the limit raised to 100,000 | the limit: a plain `RecursionError` |
| `lru_cache` or `cache`, any number of arguments | 1,400 (two frames a call) | the limit |
| generator expression in `min`, `max`, `sum`; `sorted` key; `map` | `min`: 400 passes, 450 fails; `sorted` key: 300 passes, 400 fails; `sum` and `map`: 500 to 700 pass | the browser stack: reported per test as above |
| list comprehension | at least 1,400 (inlined by Python 3.12) | the limit |

The documented number is "about 300".

### Tests

`app/tools/test-drill-recursion.mjs` (committed, needs `--local-cdn` off a connected machine): source checks (one runner), worker cases (lru 800 and 1,400 deep, a plain recursion 2,800 deep, `functools.cache`, a dict 50,000 deep, a plain recursion past the limit, a generator that overflows with the tests after it graded, an overflow at load), and the drill page played with `app/tools/fixtures/drill-recursion/drill-ab-recursion.json` (the deep test is an error naming `RecursionError`, the other four pass, no crash, Python ready again). Against the old worker the worker cases failed with the crash above.

### The old sizes of the six pack 7 drills

For the report only, no content edited: with the fix the old sizes of the six resized pack 7 drills are safe. The three `lru_cache` ones (`ci-merged-tape`, `ci-priced-edits`, `ci-tolerant-common`, 600 calls deep) and `ci-long-mirrors` (500 deep, `lru_cache`) are far inside 1,400. `ci-mirror-pieces` (400 letters, a generator in each call) passes at 400 and fails at 440; a 200 by 200 floor with a generator in each call (`ci-drop-point-routes`, 400 deep) passes (250 by 250 also passes). So the two generator cases sit near the edge (400 of about 440) and a larger test would not be safe.

### The drills at risk (`app/tools/drill-recursion.mjs`)

Static, from the data: for each Python drill (235, samples left out) the size of every hidden test's arguments and the upper bounds of the machine `constraints` objects, against 2,900, 1,400 and 300. Depth is estimated as a natural linear recursion would have it (a string or list is its length, sequence arguments add, a grid is rows + columns, a whole number up to 100,000 is its value; an upper estimate, it overcounts a two-feed recursion). Only drills whose natural method is recursive are listed (a `dp`, `backtracking`, `trees` or `graphs` pattern, a `dp-` tag, or a brief, hint, note or model that says recursion, memo, top-down, dfs or `lru_cache`): **63 at risk**, 61 by a hidden test and 2 only by the constraints; 10 of the 63 already warn the learner about recursion in their text; a further 128 drills whose natural method is a loop (heaps, windows, sorting, prefix sums) are counted, not listed. 175 drills have prose-only constraints, so only their tests were measured.

Reading the list: the 46 in the first group have inputs of thousands to millions: no recursion of any form passes them, so each one's brief should say "use a loop or your own stack" (53 of the 63 do not say anything about recursion). Before this pass the first group failed with a silent stop on the page for an `lru_cache` solution; now a recursive solution fails that test with a `RecursionError` message and the later tests are graded. The 15 in the third group need a generator or a sorted key inside each call to fail. The estimates are not proofs: a drill is listed when the data allow a recursion that deep, not when one exists.

### Past 2,900 calls (every recursive form fails; an iterative method is the only one): 46

- `ci-best-route-value`: tests 200000, constraints prose only, text warns
- `ci-best-session`: tests 100000, constraints 100000
- `ci-broken-steps`: tests 100000, constraints 100000
- `ci-capped-trips`: tests 9998, constraints 10000
- `ci-cell-formula`: tests 599990, constraints prose only, text warns
- `ci-change-ways`: tests 544453, constraints 800000
- `ci-cheapest-route`: tests 5001, constraints 10003, grid cells 30000
- `ci-cooldown-trades`: tests 100000, constraints 100000
- `ci-downward-path-sums`: tests 200000, constraints prose only, text warns
- `ci-ferry-timetable`: tests 100000, constraints 3000000
- `ci-fewest-tokens`: tests 20000, constraints 20000
- `ci-first-circular-rule`: tests 20002, constraints 20002, grid cells 40000
- `ci-half-fare-route`: tests 25001, constraints 30003, grid cells 90000
- `ci-handoff-distances`: tests 40000, constraints prose only, grid cells 40000
- `ci-level-totals`: tests 1288890, constraints prose only, text warns
- `ci-line-from-pairs`: tests 100001, constraints 100002, grid cells 200000
- `ci-longest-rising`: tests 100000, constraints 100000
- `ci-loop-cables`: tests 250001, constraints 250002, grid cells 500000
- `ci-mirror-pieces`: tests 150, constraints 20000
- `ci-nested-crates`: tests 100002, constraints 100002, grid cells 200000
- `ci-paving-ways`: tests 20000, constraints 60002, grid cells 120000
- `ci-read-preorder`: tests 532065, constraints prose only
- `ci-rebuild-from-orders`: tests 131070, constraints prose only
- `ci-reclaimed-land`: tests 100002, constraints 100002, grid cells 200000
- `ci-ring-bonuses`: tests 100000, constraints 100000, text warns
- `ci-ring-stalls`: tests 100000, constraints 100000
- `ci-shift-picks`: tests 100000, constraints 100000
- `ci-stop-cascade`: tests 60002, constraints 1500000
- `ci-stuck-jobs`: tests 250000, constraints 250002, text warns, grid cells 500000
- `ci-tape-decodes`: tests 200000, constraints 300000
- `ci-two-shift-rota`: tests 200002, constraints 250002, text warns, grid cells 500000
- `ci-word-split`: tests 25000, constraints 25000, grid cells 100000
- `dsa-closest-level`: tests 20003, constraints prose only
- `dsa-common-manager`: tests 65537, constraints prose only
- `dsa-feed-passes`: tests 1977774, constraints prose only
- `dsa-forced-order`: tests 399999, constraints prose only, grid cells 799994
- `dsa-kiosk-change`: tests 200001, constraints prose only
- `dsa-loop-depots`: tests 400000, constraints prose only
- `dsa-route-order`: tests 200002, constraints prose only, grid cells 400000
- `dsa-shared-tail`: tests 1288890, constraints prose only
- `dsa-shift-pay`: tests 1199999, constraints prose only
- `dsa-spare-cables`: tests 200002, constraints prose only, text warns, grid cells 400000
- `dsa-stamp-gaps`: tests 50000, constraints prose only
- `dsa-upstream-stations`: tests 200002, constraints prose only, grid cells 400000
- `oa-critical-path`: tests 200001, constraints prose only, grid cells 200000
- `oa-decodings`: tests 200000, constraints prose only

### Past 1,400 (lru_cache fails; plain and dict-remembered pass): 2

- `ci-product-stretch`: tests 2000, constraints 2000
- `ci-spaced-picks`: tests 2000, constraints 2000

### Past 300 (fails only when each call holds a generator expression, a sorted key or a map): 15

- `ci-checkpoint-route`: tests 302, constraints 100000
- `ci-flood-reach`: tests 800, constraints 800, text warns, grid cells 160000
- `ci-hold-limit`: tests 400, constraints 400
- `ci-invoice-matches`: tests 1000, constraints 20000
- `ci-island-shapes`: tests 600, constraints 600, text warns, grid cells 90000
- `ci-long-mirrors`: tests 300, constraints 1000
- `ci-merged-tape`: tests 600, constraints 600
- `ci-nearest-depot`: tests 600, constraints 600, grid cells 90000
- `ci-priced-edits`: tests 301, constraints 20000
- `ci-safest-walk`: tests 500, constraints 500, grid cells 62500
- `ci-smooth-orderings`: tests 1000, constraints 1000
- `ci-wall-break-route`: tests 600, constraints 600, grid cells 90000
- `dsa-climb-limit`: tests 600, constraints prose only, grid cells 90000
- `dsa-free-desk-square`: tests 1000, constraints prose only, grid cells 250000
- `dsa-split-prices`: tests 1000, constraints prose only

### Model solutions on the page

`node tools/playthrough.mjs --drills --local-cdn <pkgs>`: every drill (Python and C++) and the sample session pass, the starters fail: All passed, 0 relaunches. The pure `lru_cache` did not push any model past its limit.

## Item 2 (914): the feedback bar over the last answer box at 440 px

Reproduced with a new playthrough assertion (`--problems <set> --mobile`, at 440 x 956 after each checked part of the first attempt: the part's answer box must end above the feedback bar). On `exp-log/problems-1` it failed on 4 of 4 problems (134, 94, 98 and 81 px covered). Fix in `runSet` (`app/js/engine/player.js`, `clearBar`): after the verdict the checked part is scrolled so its answer box ends 12 px above the bar, never past its own top; repeated on the next frame and at 250 ms (the verdict's maths grows the bar) and on resize. `exp-log/problems-1` and `series/problems-1` pass; `--problems all --mobile`: All passed (every set, with the 440 px assertion).

## Item 3 (918): the near-miss rule

What the reviews describe (`review-drills-ci-3-4.md` findings 2 to 8, `-5.md` 1 to 9, `-6.md` 1 to 9): in every case a solution one step short of the target passes every hidden test. Four kinds: the ruled-out slower method kept alive by the test data (the tails scanned without a binary search, relaxing every crossing until nothing changes, a per-rule search run backwards, a sorted list with `insort`); a greedy that lacks the exchange case (richest free day first, three days); an off-by-one in the table or window (a check one column short, a first token only); and the brief's own allowed case never tested (two roads between the same towns, `src` equal to `dst`, equal case mixed). The authors had planted the slow or obvious wrong solution, never the nearly right one.

The smallest rule that catches them: every `ci-` and `dsa-` drill carries a planted solution marked `"nearMiss": true`. It is a plant like any other, so `planted-check` already requires it to fail at least one hidden test; what is new is that its presence is required and its kind is named.

- Validator (`validate.mjs`): `[near-miss]` warning on each non-sample `ci-` or `dsa-` drill with no planted entry marked `nearMiss: true`; `nearMiss` that is not a boolean is an error; `nearMiss` is a known planted field.
- `planted-check.mjs --near-miss`: fails a drill with no marked plant; a near-miss that passes every hidden test is named "near-miss planted[i] passes all N hidden tests" (the `playthrough.mjs --planted` line).
- Docs: `docs/AUTHORING.md` section 5, "The near-miss".
- Scratch cases: `app/tools/test-validate-near-miss.mjs` (9 checks).
- **Count: 190 drills warn** on current content (190 non-sample `ci-` and `dsa-` drills, none carries the mark): 120 of them already have planted solutions (one may qualify; the author marks it or adds one), 70 have none.

Not done (left in the inbox): the stronger form "the slow plant must fail at least two large tests of different shape".

## Results

- `node tools/validate.mjs`: 0 errors (4,854 warnings, 190 of them `[near-miss]`).
- Every `app/tools/test-*` file passes (44 files: 42 `.mjs` including the new `test-drill-recursion.mjs` and `test-validate-near-miss.mjs`, `test-numbers-lib.py` and `test-merge-wave.sh`). Three `test-validate-*` files (`fluency`, `problems`, `session-v-b`) timed out at my first 280-second limit on a loaded machine and passed when rerun with a longer one.
- `node tools/playthrough.mjs --drills --local-cdn <pkgs>`: All passed.
- `node tools/playthrough.mjs --problems all --mobile --local-cdn <pkgs>`: All passed (every set, with the 440 px assertion).

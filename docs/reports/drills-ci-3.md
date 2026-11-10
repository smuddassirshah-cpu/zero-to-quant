# Drills pack `ci`, pack 3 (stacks-queues, binary-search)

Brief: `docs/briefs/drills-ci-packs.md` row "Pack 3", on top of `docs/briefs/drills-1.8.md`. 15 Python drills, `"pack": "ci"`, `"course": "coding-int"`, skills from the `coding-int` lessons (`ci-patterns`, `ci-timed`, `ci-strings`, `ci-design`), tags `pack-3` first, rows appended to `app/content/drills/index.json`.

| id | pattern | difficulty | pace (s) | stdin | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- |
| `ci-log-compactor` | stacks-queues | 2 | 900 | no | 13 | 2 |
| `ci-ring-waits` | stacks-queues | 3 | 1500 | no | 13 | 2 |
| `ci-cell-formula` | stacks-queues | 3 | 1500 | no | 13 | 3 |
| `ci-tray-queue` | stacks-queues | 3 | 1500 | yes | 13 | 2 |
| `ci-van-convoys` | stacks-queues | 3 | 1500 | no | 13 | 3 |
| `ci-wide-bars` | stacks-queues | 4 | 1800 | no | 13 | 2 |
| `ci-visible-masts` | stacks-queues | 4 | 1800 | no | 13 | 2 |
| `ci-price-ramp` | stacks-queues | 4 | 1800 | no | 13 | 2 |
| `ci-free-block` | stacks-queues | 5 | 2700 | no | 13 | 2 |
| `ci-tick-ranges` | binary-search | 2 | 1080 | yes | 12 | 2 |
| `ci-ring-lookup` | binary-search | 2 | 1200 | no | 12 | 2 |
| `ci-clear-rate` | binary-search | 3 | 1500 | no | 13 | 2 |
| `ci-relay-masts` | binary-search | 4 | 1800 | no | 13 | 2 |
| `ci-ready-blocks` | binary-search | 4 | 1800 | no | 13 | 2 |
| `ci-kth-gap` | binary-search | 5 | 2400 | no | 13 | 2 |

Mix: three at 2, five at 3, five at 4, two at 5; two stdin drills. Ideas of the row: circular next-greater (`ring-waits`), monotonic spans (`visible-masts`, `price-ramp`), expression evaluation (`cell-formula`, nested functions, not the taught infix calculator), largest rectangle (`wide-bars` with widths, `free-block` on a grid), a queue from two stacks under load (`tray-queue`, the move count is the test), rotated search (`ring-lookup`), first and last position (`tick-ranges`), search on the answer (`clear-rate`, `relay-masts`, `ready-blocks`, `kth-gap`). At 4 and 5 the `how` line names the step from the obvious method to the target, and the obvious method runs past 8 s in CPython on a large hidden test.

## Checks

1. `docs/reports/drills-ci-3-check.py` (scratchpad venv): exit 0, 15 drills, 0 errors. Model solution and an independent method on every example and test (brute force when small; on large inputs a sparse table with binary lifting, a sort-and-sweep, insertion into a sorted list, numpy row pairs or `searchsorted`, union-find over days, a heap exact greedy, or a closed form worked in a comment). A random cross-check of 400 small cases per drill family: 0 disagreements. Starter fails every drill. Every planted solution is wrong on a test and finishes all tests within 1.5 s; each slow obvious method in `drills-ci-3-obvious.json` runs past 8 s or fails.
2. `node tools/validate.mjs`: 0 errors. Two warnings on my files: pace 2,400 and 2,700 on the difficulty-5 drills, which the brief allows.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: 15 ok, All passed; with `--mobile`: 15 ok, All passed. Screenshots looked at (desktop and 440 px): no overflow or clipping.
4. Voice: `voice-scan.py 35` on the 15 files (planted code removed): 0 sentences over 35 words, 0 explanations over three sentences. No exclamation marks or em-dashes in prose.
5. This report; three inbox bullets under "Raised later (drills ci 3)".
6. `node tools/planted-check.mjs --drill <15 ids> --require --local-cdn <pkgs>`: 15 drills, 32 planted solutions, 0 failures.

## Planted solutions

First CPython run: 2 of 45 passed every test. `visible-masts` planted[2] was in fact correct (on distinct heights the push test is always true), so it was replaced by a real slip: counting every mast up to the first taller one. `free-block`'s row-pair method ran under 8 s on 400 by 400, so the grid limit went to 600 and the three large tests to 600 by 600. No other test was added.

Then the stock planted-check failed 13 drills. Every one was the engine fault in the first inbox bullet: after a planted run timed out, later submits read stale results. Fix applied on a scratch copy only: 45 planted, 0 failures. In the repo, the 13 slow methods moved from `planted` to `drills-ci-3-obvious.json`, run by the check script. Two compactor and relay slips (a run-count reset, all relays in the longest gap) were added so each drill keeps two.

## Freshness

`node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15. At `--min-run 8 --min-share 0` the only hits are the shared constraint lines ("is too slow. All the tests in a run share one 5-second limit in the browser") and name rows in `index.json`: stock phrasing, kept. Setups judged against taught ones: `ds` l10 (linear next greater; largest rectangle only as a choice item), `coding-int` l7 `calculate` (infix with precedence, and bracket decoding), `ds` homework-3 `stock_span`, `algo-think` homework-3 `min_capacity`, and the `dsa` drills `depth-block` (sum of block minima), `kiosk-spacing` (widest spacing), `net-tape` and `bracket-partners`. Each pack 3 task differs in its question and its key step.

`app/content/manifest.json` was rewritten by the validator and is left out of the commit.

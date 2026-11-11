# Delta read: the four fix passes on drills `ci`, packs 5 to 8

Scope: only what the four fix passes changed, read at commit 80caffb. No drill file of the four packs has changed since its fix pass (`diff_fields.py`).

- Pack 5: `git diff e2b921a^ e2b921a -- app/content/drills/`. 12 drill files and two `index.json` rows. Record: `review-drills-ci-5.md`, "Fix pass".
- Pack 6: `399c637`. 13 drill files and four `index.json` rows. Record: `review-drills-ci-6.md`, "Fix pass".
- Pack 7: `4160e9d`. 11 drill files, no `index.json` row. Record: `review-drills-ci-7.md`, "Fix pass".
- Pack 8: `a6b3b02`. 13 drill files and two `index.json` rows. Record: `review-drills-ci-8.md`, "Fix pass".

Method. Each changed drill was read whole as it now stands, against the finding above its fix. For every drill whose tests, examples, model or sizes changed (39 drills) I wrote my own solution from the brief, by a method other than the model's wherever one exists (`mine_5.py` to `mine_8.py`), and ran model, mine, starter and every planted solution on every example and hidden test (`run.py`). For 28 of them (packs 6 to 8) I also wrote a plain brute force and ran it on every example and test small enough for it, then against the model on 300 to 1,500 random small inputs a drill (`extra_6.py`, `extra_7.py`, `extra_8.py`); for the one drill whose task changed, `ci-half-fare-route`, a brute force over every simple route ran against model and mine on 4,000 random networks (`extra_5.py`). Second methods used: a Dijkstra keyed on the route itself, a queue-based label correcting search, a topological order kept up as rules arrive, two plain searches with the voucher tried on every road, member lists with the smaller rewritten, a parity union-find, a search over (cell, knocked), prefix sums with suffix maxima, Fenwick trees over ranks, a cell-by-cell paving window, a trie search, a cheapest path on the edit grid, counts over what is left of each size, difference constraints solved as a longest path (`ci-double-checks`), a bit-by-bit count with no binomials, a sliding minimum, sorted lists in place of heaps. To see whether a fix pass let anything through, I ran every candidate of the first readers' own files on each drill as it stood before its fix pass and as it stands now (`old_drills.py`, `regress.py`: 222 candidates on drills with changed tests). For the six resized drills of pack 7 I wrote natural top-down solutions and counted calls on the stack for every test (`depth_7.py`). Authors' scripts, the validator and the voice scan were run. No browser was used: page behaviour is quoted from the first reviews, and one timing question was settled in Pyodide 0.27.7 under node through the authors' own `--pyodide` mode.

Scripts: `docs/reviews/review-delta-drills-ci-5-8-scripts/`, run from the repo root with `python3` (the scratchpad venv has no NumPy, which two authors' scripts need): `run.py <pack>`; `extra_5.py` to `extra_8.py` (with `brute_lib.py`); `depth_7.py`; `old_drills.py <pack> <dir>` then `regress.py <pack> <dir>`; `weak_78.py`; `proposed.py`; `diff_fields.py` and `show.py` print what changed and a drill for reading.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = a statement reads two ways, or the tests now let through a wrong solution that they caught before the fix pass (the first reviews' `weak`); `minor` = otherwise.

## Tool results

- `run.py`: all 60 models pass, all 60 starters fail, my 39 solutions agree with every `expect` (11, 10, 10 and 8 by pack), every `how` count matches its `tests` array, every `index.json` row matches its file, and the mix is 3 / 5 / 5 / 2 in each pack. **No `expect` is wrong, in any of the four packs.** Every planted solution fails a test or runs past 5 seconds natively, except `ci-word-split` planted[3] (1.9 s natively; 14.8 s in Pyodide, so it does fail on the page).
- Brute forces: 0 disagreements with any `expect` they could reach and 0 with the model on 42,800 random inputs (38,800 in packs 6 to 8, 4,000 networks in pack 5).
- `regress.py`: of 222 first-reader candidates on drills with changed tests, 40 verdicts moved. 37 moved the right way (every candidate of the `weak` findings is now caught or too slow). One is timing noise on a right solution. **Two moved the wrong way: caught before the fix pass, accepted now** (findings 7 and 9). One planted solution is now caught only by a large generated test (finding 1).
- `depth_7.py`: my top-down solutions agree with every `expect`; deepest tests are 301, 300 and 300 calls (`ci-merged-tape`, `ci-priced-edits`, `ci-tolerant-common`) and 151 to 159 calls for the other three (finding 8).
- Authors' scripts: `drills-ci-5-check.py` exit 0 (`15 drills, 0 errors`); `drills-ci-7-check.py` exit 0 (`15 drills, 0 errors`, 40 stated numbers); `drills-ci-8-check.py` exit 0 (`15 drills, 0 errors`). **`drills-ci-6-check.py` exits 1 on this machine** (`15 drills, 1 errors`, finding 3).
- Pyodide under node, authors' `--pyodide` mode: `ci-word-split` model 0.115 s, planted[3] 14.769 s; `ci-first-circular-rule` model 0.46 s, planted[2] and [3] cut off at 12 s (the backward search takes 5.4 s natively here).
- `node tools/validate.mjs`: 0 errors; `manifest.json` came out unchanged. `voice-scan.py 35` on `app/content/drills`: 0 and 0. No em-dash, exclamation mark or American spelling in the prose of the 60 drills.

## Fix pass 1: pack 5

| Finding of `review-drills-ci-5.md` | Verdict |
| --- | --- |
| 1 to 4 (large tests for the ruled-out methods) | fixed; each new `expect` agrees with mine; each new slow plant is slow |
| 5 (`ci-island-shapes`, three tests, constraints sentence) | fixed; the sentence it adds is finding 2 below |
| 6 to 8 | fixed |
| 9, 13, 14 (`ci-half-fare-route`, task changed) | fixed; brief, hint, both examples, notes, `how`, all 15 tests and the five plants agree with the new rule; model, mine and brute force agree on 4,000 networks |
| 10, 11 (brief sentences) | fixed |
| 12 (`ci-flood-reach` wording) | fixed |
| 15 (two near-sample tests) | ferry fixed; cables fixed, and the swap introduced a new fault (finding 1) |
| 16 (constraints objects) | no change, as agreed |
| 17, 18 | fixed |
| 19 (difficulty and pace) | fixed; rows in step |

1. `minor` (new fault from fix 15) | `app/content/drills/ci-loop-cables.json` | `tests[2]`, `planted[0]`.
   Before the fix pass planted[0] (rack `a` pointed at the other root, not its own root) first failed tests[2], the triangle `loop_cables(3, [[0, 1], [0, 2], [1, 2]])`: expected `[2]`, it returned `[]`. On the replacement `loop_cables(4, [[3, 1], [0, 3], [1, 0], [2, 0]])` it returns `[2]`, the right answer. It now fails tests[11] only, where the learner sees `(9755, 88463)` against `(100001, 8756)`, which says nothing about the slip. The first reader's own proposed replacement has the same effect. Add `{"call": "loop_cables(4, [[1, 3], [1, 0], [3, 0], [2, 3]])", "expect": "[2]", "compare": "equal"}` (model and mine `[2]`, planted[0] `[]`; it is not a rotation of the triangle) and set `how` to 13 hidden tests.
2. `minor` | `app/content/drills/ci-island-shapes.json` | `constraints[1]`.
   The sentence added for finding 5, "One slick can hold every cell, too deep for Python recursion.", is the claim finding 12 of the same review corrected in `ci-flood-reach` in the same pass. Planted[5], the recursive fill, with `sys.setrecursionlimit(1000000)` added passes all 15 tests natively, 90,000 calls deep (the first reader saw the same on the page for `ci-flood-reach`, 160,000 deep). Suggested: "One slick can hold every cell, too deep for Python recursion unless the limit is raised." The planted slip could say "at the default limit" as the other drill's now does.

## Fix pass 2: pack 6

| Finding of `review-drills-ci-6.md` | Verdict |
| --- | --- |
| 1 to 9 (tests and plants) | fixed; all twelve candidates are caught or too slow; each new `expect` agrees with mine and with a brute force where one reaches |
| 10, 11 (brief sentences) | fixed |
| 12, 13, 14 (notes and constraints wording) | fixed |
| 15 (`ci-capped-trips`) | applied exactly as the reader wrote it (sentence, difficulty 4, pace 2,100, swap with `ci-long-stairwell`); task kept: my view is finding 4 |
| 16 (`ci-longest-rising`, `ci-paving-ways`) | applied as written; paving at difficulty 4 has its obvious method named in `how`, planted and too slow; rising kept: finding 5 |
| 17 (`how` sentences) | fixed; the two reworded ones match the code |
| 18 (near samples) | fixed; `216` has 3 readings |
| 19 | no change, as agreed |
| 20 (`ci-best-session` model) | fixed; the changed model agrees with a brute force on 1,500 inputs and with my prefix-sum method on all 15 cases |
| 21 | fixed |

3. `minor` | `docs/reports/drills-ci-6-check.py` | `SOFT_SLOW`, line 680.
   The gate "it must exit 0" does not hold here: `ERROR ci-word-split: planted[3] is meant to be too slow but finished ({'failed': None, 's': 2.27})`. The script asks that plant to take 3.5 s natively; the fix pass measured about 4.7 s, this machine (CPython 3.13) takes 1.9 to 2.3 s. The content is sound: in Pyodide the plant takes 14.8 s, three times the page's limit. The native floor is a machine-dependent stand-in for the Pyodide figure. Either drop the native floor for `SOFT_SLOW` plants and leave the verdict to `--pyodide`, or lower it to a figure that only says "much slower than the model". The same kind of plant in pack 5 (`ci-first-circular-rule` planted[3], 5.4 s natively here against a 3 s floor) passes with less room than its author had.
4. `minor` (judgement asked for) | `app/content/drills/ci-capped-trips.json` | whole drill.
   I side with the reader on substance and with the fix pass on what the reader literally asked. Evidence: the model of `contests` homework-4 `max_profit_k`, renamed and with `- fee` added to one line, passes all 2 examples and 15 hidden tests of this drill (checked). The fix record's basis, "the fee removes the large-`k` shortcut", describes a shortcut the homework model does not have; the homework table needs nothing else changed. So for a learner who did that homework this is a repeat with five characters added, labelled difficulty 4 on 35 minutes. Against that: the three new tests do separate the fee slips, `how` now says plainly what the drill is, and the reader's own exact fix was the sentence and the relabel, both applied. The brief's rule bars "a `contests` task under a new story"; whether one added term escapes it is a policy call, not a fault in the file. My recommendation: keep it for this release, since nothing in it is wrong, and record the policy in DECISIONS (a cross-course near-repeat is allowed when `how` names its source, or it is not). If it is not, the task needs a change that alters the table and not one term of it, with every `expect` recomputed twice.
5. `minor` (judgement asked for) | `app/content/drills/ci-longest-rising.json` | difficulty, `how`.
   Keep it. The changed return value is small but real: planted[1] shows the slip it invites, and the brief's no-repeat list does not name the `oa-` pack. Two loose ends remain. The model of `oa-rising-run`, with its return line changed to `[len(tails), tails[-1]]`, passes every example and test here (checked), yet `oa-rising-run` is labelled difficulty 4 and pace 1,800 while this drill, which asks for strictly more, is now 3 and 1,500. And `how` does not name the earlier drill, as `ci-loop-starts` now names `dsa-loop-depots`. Suggested: end `how` with "This is the drill `oa-rising-run` with the smallest end added.", using that drill's display name, and bring the two labels into line (the `oa` drill to 3, or this one to 4 with the mix rebalanced).

## Fix pass 3: pack 7

| Finding of `review-drills-ci-7.md` | Verdict |
| --- | --- |
| 1 to 4 (sizes halved in four drills) | fixed; prose constraints, `constraints` objects, tests, slips and `how` all carry the new sizes and nothing still states an old one; the room left is finding 8 |
| same fault found by the fix pass in `ci-long-mirrors` | fixed; statement, object and tests agree at 300 letters |
| same fault found by the fix pass in `ci-drop-point-routes` | sizes agree at 80 by 80; the resize introduced a new fault (finding 7) |
| 5 (brief sentence) | fixed |
| 6 to 8 (tests and plants) | fixed; all four candidates are caught or too slow; $11! - 2 \times 10! = 32{,}659{,}200$ agrees with mine |
| 9, 10 (small tests) | fixed; the dropped length-mismatch test loses nothing I can find |
| 11, 12 | fixed; tests[11] of `ci-trace-count` is 20 rows by 19 columns and a 60-letter word, inside the constraints |
| 13 (`ci-hold-limit` samples) | values fixed; the reworded example note is false (finding 6) |
| 14, 15, 16 | fixed |

6. `wrong` (fix 13, fixed wrongly) | `app/content/drills/ci-hold-limit.json` | `examples[1].note`.
   The note the fix pass wrote reads: "The limit of 3 crates does not bind: only the crates of 4 and 3 tonnes fit together within 9 tonnes, and they earn £65." For weights `[4, 3, 6]` and `cap = 9` the crates of 3 and 6 tonnes also fit together, at exactly 9 tonnes, and earn £60 (`extra_7.py`: sets within 9 tonnes are `[4, 3]` at £65 and `[3, 6]` at £60). The answer 65 is right. The note is not, and it teaches that a load of exactly `cap` does not fit, against the brief's "at most `cap` tonnes". The fix record rejected the reader's wording as false and put another false sentence in its place. Suggested: "The limit of 3 crates does not bind, because all three weigh 13 tonnes. Of the pairs that fit, 4 and 3 tonnes earn £65 and 3 and 6 tonnes earn £60."
7. `unclear` (new fault from the resize) | `app/content/drills/ci-drop-point-routes.json` | `tests[11]` to `tests[13]`.
   The hint says to count every route, count the routes that meet no drop point, and subtract. A learner who reduces both counts and returns `every[-1] - clear[-1]` without a last `% MOD` returns a negative number whenever the first residue is the smaller. The 200 by 200 tests caught that: the first reader's `drop_mod_of_difference_missing` failed old tests[11] and [13]. On the three 80 by 80 tests that replaced them no difference is negative, so the plain slip now passes all 3 examples and 14 hidden tests (`weak_78.py`, `regress.py 7`). Add `{"call": "drop_point_routes(['.' * 18] * 2 + ['.' * 2 + 'P' + '.' * 15] + ['.' * 18] * 15)", "expect": "930705120", "compare": "equal"}` (model and mine 930705120, the slip returns -69294887; 18 by 18, 36 calls deep) and set `how` to 15 hidden tests. It is worth planting, with the slip "Reducing both counts but not their difference returns a negative number when the first residue is the smaller."
8. `minor` (not confirmed on the page) | `ci-merged-tape.json`, `ci-priced-edits.json`, `ci-tolerant-common.json` | `tests[11]`, `tests[10]`, `tests[10]`.
   The halved sizes are the reader's own, and they do what was asked for the form the reader tested: a remembered recursion with plain calls goes 301, 300 and 300 calls deep, inside the 450 the reader saw pass. The reader's second band was a recursion holding a generator expression in each call: 200 passed, 250 stopped Python. A learner who writes `return sum(go(i2, j2) for i2, j2 in moves) % MOD` in `ci-merged-tape`, or `min(... for ...)` over the three edits, is 300 deep in that form, past the failing depth. I could not run the page, so this is a risk and not a finding of fact. `ci-mirror-pieces` (151 calls, each with a generator) and `ci-drop-point-routes` (159) are inside both bands. The engine item already raised ([Must] under `Raised later (fix drills ci 7):`) removes the question; until it lands, about 90 letters a side would clear both bands in these three drills.

## Fix pass 4: pack 8

| Finding of `review-drills-ci-8.md` | Verdict |
| --- | --- |
| 1 (`ci-first-fit-slot`, two tests) | both tests added and both candidates caught; folding out old tests[5] introduced a new fault (finding 9) |
| 2 to 4, 6 (tests swapped or added) | fixed; the replaced tests lose no candidate; each new `expect` agrees with mine and a brute force |
| 5 (`ci-switch-panel`) | fixed; folding out old tests[13] loses nothing (tests[12] and examples[0] hold the same tie) |
| 7 (`ci-ring-bonuses` recursion sentence) | fixed by wording, sizes kept, as the reader proposed |
| 8 (`ci-k-bit-count`, 400 queries) | fixed; prose "1 to 400", object `[1, 400]`, tests[11] with 400 queries and tests[12] with 301 agree; both `expect`s agree with my bit-by-bit count |
| 9, 11, 12 (brief and constraint wording) | fixed |
| 10, 13 (`bisect` and recursion wording) | fixed; one event does fire 20,000 stops in tests[14] |
| 14 | fixed; the name matches `dsa-loop-depots` |
| 15, 16 | fixed; every test sits inside the newly stated ranges |
| 17 (`ci-room-numbers` example) | fixed; brief, example and note agree, and `[0, 1, 1, 0]` agrees with mine and a room-by-room scan |
| 18 (difficulty swap) | fixed; rows in step; the new slow plant of `ci-double-checks` is slow |

9. `unclear` (new fault from fix 1) | `app/content/drills/ci-first-fit-slot.json` | `tests` (old `tests[5]` removed).
   To stay at 15 tests the fix pass removed `first_fit([[0, 3], [3, 6], [10, 12]], 20, 4)`, calling it "covered by the empty list and test 3". It was the only test with bookings present and `start` past the end of the last one. The first reader's own candidate `fit_past_end_forgets_start` (no gap found, so the job goes at the last booking's end) failed that test and now passes all 2 examples and 15 hidden tests (`regress.py 8`, `weak_78.py`). On the removed test it returns `[12, [[0, 6], [10, 16]]]` against `[20, [[0, 6], [10, 12], [20, 24]]]`; on `first_fit([[2, 4]], 9, 1)` it returns `[4, [[2, 5]]]` against `[9, [[2, 4], [9, 10]]]`. The fix record's "still fail every planted and every further wrong solution" holds for the author's file of 83 but the first reader's candidates were not rerun. Put the removed test back in place of one of tests[0] to [12]: replacing any one of those loses no planted solution and none of the first reader's five candidates (`proposed.py`; tests[13] and [14] must stay). Rerun `drills-ci-8-check.py` after the swap, since the author's 83 may lean on the test that goes.

## Resized drills of pack 7: do statement, constraints and tests agree?

Yes in all six. `ci-merged-tape`: prose 150, 150 and 300, objects `[0, 150]`, `[0, 150]`, `[0, 300]`, largest tests 150 + 150 letters, slip "well over eighty digits" ($\binom{300}{150}$ has 89). `ci-mirror-pieces`: prose 1 to 150 letters and 3,000 in all, largest tape 150, largest text 1,725 letters. `ci-priced-edits`: prose 1 to 150, largest codes 150, products at most 90,000 a text against the 100,000 stated. `ci-tolerant-common`: prose and objects 150, tests 150 and 140. `ci-long-mirrors`: prose and object 300, tests 300; `k` keeps its range to 1,000, which the prose covers ("`k` may be longer than the tape"). `ci-drop-point-routes`: prose and object 80, tests 80 by 80. No brief, hint, note, slip or `how` in the six still names an old size. The only faults the resize left are findings 7 and 8.

## Counts

| Pack | `wrong` | `unclear` | `minor` |
| --- | --- | --- | --- |
| 5 | 0 | 0 | 2 (findings 1, 2) |
| 6 | 0 | 0 | 3 (findings 3, 4, 5) |
| 7 | 1 (finding 6) | 1 (finding 7) | 1 (finding 8) |
| 8 | 0 | 1 (finding 9) | 0 |

Of the 74 findings in the four first reviews: 67 fixed, 2 left unchanged as agreed, 1 fixed wrongly (pack 7 finding 13), 2 applied as written with the task kept (pack 6 findings 15 and 16), and 2 fixed with a new fault of the fix's own (pack 5 finding 15, pack 8 finding 1). A third new fault came from the pack 7 resize of `ci-drop-point-routes`, which went beyond the review.

## For the main session

- One finding class, three sightings in this delta (findings 1, 7 and 9): a fix pass that swaps, removes or resizes a test did not rerun the first reader's candidates, and a slip the old test caught went through. SESSION PROTOCOL 6 makes that a script. `regress.py` with `old_drills.py` is that script in rough form; I have not added an inbox bullet, since this task writes only the review.
- A decision on `ci-capped-trips` (finding 4): record whether a cross-course near-repeat with an honest `how` is allowed.
- A small fix pass covers the rest: one note (finding 6), three tests (findings 1, 7, 9), two wordings (findings 2, 5), one script threshold (finding 3). Each proposed `expect` was computed by the model and by my own solution (`proposed.py`).

## Fix pass

Candidates rerun (rule of this pass): every first-reader candidate of `review-drills-ci-5.md` to `-8.md` for the three drills whose tests changed, on the tests before and after (`verify.py`, scratchpad: 5 + 7 + 5 = 17 candidates, 4 of them right solutions, plus all 12 planted solutions). Result: 0 candidates that failed before pass now, 0 planted solutions pass. Three that passed on the old tests are now caught: `fit_past_end_forgets_start` (test 7), `drop_mod_of_difference_missing` (test 14), and planted[0] of `ci-loop-cables` now also fails the small test 12. The delta reader's `regress.py` classes were covered: `ci-hold-limit`, `ci-island-shapes`, `ci-longest-rising`, `ci-word-split` have no test change. Every `expect` agrees between the model and the delta reader's own solution (`proposed.py`).

1. `ci-loop-cables` (finding 1): fixed. Added tests[12] `loop_cables(4, [[1, 3], [1, 0], [3, 0], [2, 3]])`, expect `[2]` (model and mine `[2]`; planted[0] returns `[]`, fails it; every other candidate unchanged). `how` now says 13 hidden tests. Tests changed: one added, none swapped. Graded values changed: none.
2. `ci-island-shapes` (finding 2): fixed. `constraints[1]` now ends "too deep for Python recursion unless the limit is raised."; planted[5] slip says "at the default limit". No test change.
3. `drills-ci-6-check.py` (finding 3): fixed. `SOFT_SLOW` plants now need only `SOFT_FLOOR = 1.5` s natively (the model takes about 0.1 s) in place of 3.5 s; the Pyodide check (plant over 5 s) is untouched and still the gate. `WANT_DIFF` updated for finding 5. All four check scripts exit 0 (15 drills, 0 errors each).
4. `ci-capped-trips` (finding 4): no change, kept by decision of the main session.
5. `ci-longest-rising` (finding 5): fixed. Difficulty 4 and pace 1,800 to match `oa-rising-run` (4, 1,800); `how` ends "This is the drill `oa-rising-run` (Longest rising subsequence) with the smallest end added." To keep the mix 3 / 5 / 5 / 2, `ci-word-split` (the plain fewest-codes table over a dictionary, with an obvious method and slow plants intact) goes to difficulty 3, pace 1,500. `index.json` rows in step. No test change.
6. `ci-hold-limit` (finding 6): fixed. Recomputed: sets within 9 tonnes are `[4, 3]` at £65 and `[3, 6]` at £60 (`[4, 6]` is 10); the three crates weigh 13. `examples[1].note` now reads "The limit of 3 crates does not bind, because all three weigh 13 tonnes. Of the pairs that fit, 4 and 3 tonnes earn £65 and 3 and 6 tonnes earn £60." Graded answer 65 unchanged.
7. `ci-drop-point-routes` (finding 7): fixed. Added tests[14] `drop_point_routes(['.' * 18] * 2 + ['.' * 2 + 'P' + '.' * 15] + ['.' * 18] * 15)`, expect `930705120` (model and mine agree; the slip returns -69294887, 18 by 18, under the sizes of pack 7). `how` says 15 hidden tests. New planted[3]: both counts reduced, difference not (fails tests[14] only, as intended). Tests changed: one added, none swapped.
8. Pack 7 recursion depth (finding 8): deferred. Not confirmed on the page; no limit raised and no test resized; the engine item already stands.
9. `ci-first-fit-slot` (finding 9): fixed. The removed test is back in place of old tests[7] `first_fit([[10, 20], [25, 30]], 12, 5)` (expect `[20, [[10, 30]]]`, a touch-both-sides case also held by examples[0] and tests[4] and [10]); the new tests[7] is `first_fit([[0, 3], [3, 6], [10, 12]], 20, 4)`, expect `[20, [[0, 6], [10, 12], [20, 24]]]`. Rerun after the swap: all five first-reader candidates are caught (`fit_past_end_forgets_start` now at test 7) and all five planted solutions still fail (tests 1, 2, 8, 13, 14 among others); `drills-ci-8-check.py` exit 0. The empty-list test[0] and tests[13], [14] are kept.

Changed tests, all: `ci-loop-cables` +1 (`loop_cables(4, [[1, 3], [1, 0], [3, 0], [2, 3]])`), `ci-drop-point-routes` +1 (the 18 by 18 grid above), `ci-first-fit-slot` tests[7] replaced. No other graded value changed.

Gates: all four `drills-ci-<5..8>-check.py` exit 0; `validate.mjs` 0 errors; `planted-check` on the seven changed drills 0 failures; playthrough (`--local-cdn`) of the seven changed drills with and without `--mobile`, all passed; voice scan `35` on the drills folder 0 and 0.

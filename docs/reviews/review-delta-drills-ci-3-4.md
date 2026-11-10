# Delta read: fix pass on drills `ci`, packs 3 and 4

Scope: only what the fix pass in `review-drills-ci-3-4.md` changed, at commit 4e2b3e0. `git diff 6038127 4e2b3e0 -- app/content/drills/` touches 22 drill files and `index.json`; the two check scripts and `drills-ci-3-obvious.json` changed with them.

Method. Each of the 22 drills was read whole as it now stands (brief, constraints, examples, notes, `how`, `hint`, solution, `slip` sentences, tests), not only its changed lines. I wrote my own solution to all 22, by a second method wherever one exists (`mine.py`: a Fenwick tree for the median, a prefix set for the board, an un-turned copy for the ring, a merge for the tick log, exact fractions for the convoys, a sort for the ramp, the rota rule read literally, each level checked against every level above it, and so on), and ran model, mine, starter and every planted solution on every example and hidden test in CPython. Every changed or added test was checked against the drill's own constraints by script. I wrote three candidates the fixer did not plant and timed them, with the marginal planted ones, in Pyodide 0.27.7 under node (V8). The three too-slow planted solutions, and then all 22 drills, were run through `planted-check --require` in the app runtime.

Scripts: `docs/reviews/delta-drills-ci-3-4-scripts/`, run from the repo root with the scratchpad venv Python: `run.py [ids]`, `extra.py`, `make_proposed.py` (writes `proposed_tests.json`), `gen_times.py` (see its header), `dump.py <id>`, with `mine.py` and `extra_cands.py`.

Tags: `wrong` = a learner is marked wrongly or told something false; `weak` = the tests miss a real wrong or too-slow solution, or the statement is ambiguous; `minor` = otherwise.

## Tool results

- `run.py`: model and mine agree on every example and hidden test of all 22 drills. No `expect` is wrong. `how` counts match the `tests` arrays. The starter fails in all 22. All 62 planted solutions fail a hidden test in CPython except `ci-live-median` planted[3], which is right and takes 8.6 s there (the app is the test for it, below).
- Every planted solution the fixer added fails for the reason its sentence names: `ci-ring-lookup` [0] (10 tests, the next id for a present one) and [1] (tests[4], the ring not turned); `ci-tick-ranges` [0] (9 tests, one too far) and [1] (4 tests, a larger time reported as found); `ci-cell-formula` [3] (only tests[13] and [14], clipped at $\pm 10^9$); `ci-first-misplaced` [3] (only tests[13], returns 15 for 12); `ci-log-compactor` [2], `ci-stock-by-prefix` [3] and `ci-live-median` [3] on time only.
- The three `SLOW_PLANTED` solutions, from `app/`, foreground: `node tools/planted-check.mjs --drill <id> --require --local-cdn <pkgs>` gives "1 drill checked, 4 planted solutions, 0 failures" for `ci-live-median`, the same for `ci-stock-by-prefix`, and "3 planted solutions, 0 failures" for `ci-log-compactor`. All 22 changed drills in one run: "22 drills checked, 62 planted solutions, 0 failures".
- `ci-live-median` in Pyodide: model 1.6 s over all tests (tests[10] 1.1 s); the planted sorted list 16.9 s (tests[10] alone 15.2 s), three times the limit. The same list held in `array('i')` takes 19.1 s. The open case of the first review is settled in the app, not only in CPython.
- `ci-board-words` tests[12] holds 3,602 distinct words on a 12 by 12 board, inside the constraints. In Pyodide the model takes 0.04 s; the per-word search takes 12.4 s, and 12.2 s with the letter-count check first. tests[11] is unchanged and still yields 30 distinct words; nothing in the drill claims more, and tests[12] now does that job.
- `drills-ci-3-check.py`: "15 drills ..., 34 planted, 0 errors" (181 s). `drills-ci-4-check.py`: "15 drills, 0 errors" (96 s). `node tools/validate.mjs`: 0 errors.
- `index.json`: the 30 pack-3 and pack-4 rows equal their files in `name`, `course` and `difficulty`. Both packs keep the mix 3 / 5 / 5 / 2 and two stdin drills.
- `voice-scan.py 35` on `app/content/drills/`: 1 sentence over the gate, made by this fix pass (finding 3).
- I did not run the playthrough with `--mobile`.

## Findings

1. `weak` | `ci-ring-lookup` | tests.
   Finding 9 of the review was that the drill needs no search. It still needs none. A dict of positions, with an absent id walked up one id at a time (`while t not in where: t += 1`, after one check against the largest id), passes all 12 hidden tests: 0.08 s in CPython and 0.09 s in Pyodide, against 0.85 s for the model (`extra_cands.py`, `find_in_ring__dict_probe`). In the two large tests neighbouring ids differ by 1 and by 2, so the walk is one step. Constraints[1] now says "a lookup by exact value cannot answer for an id that is absent"; against these tests it can. The id, name and tag are still honest for the new task, and the statement is complete (the empty ring, no turn, a target below every id and above every id are all stated or shown).
   Fix: replace tests[9] with `{"call": "find_in_ring([1000000000, -1000000000], [-1000000000, 1000000000, -999999999, 0])", "expect": "[1, 0, 0, 0]", "compare": "equal"}` and add `{"call": "(lambda r: (len(r), sum(r), r.count(-1)))(find_in_ring([10000 * ((i + 61729) % 100000) for i in range(100000)], [(i * 104729) % 1000000000 for i in range(100000)]))", "expect": "(100000, 5053688078, 1)", "compare": "equal"}`. `how`: 13 hidden tests. Model and mine agree on both; the model takes 0.54 s on the large one in Pyodide; the walk does not finish either inside 6 s natively (2 thousand million steps on the small one). Plant the walk last in `planted`, with slip "A dict answers ids that are present, but an absent id is walked up one at a time, which takes as many steps as the gap to the next id.", and add `("ci-ring-lookup", 2)` to `SLOW_PLANTED` in `drills-ci-3-check.py`.

2. `weak` | `ci-tick-ranges` | tests.
   The same, for finding 10. Two dicts of first and last position, with an absent time walked up one millisecond at a time to the next tick, pass all 12 hidden tests (0.17 s in CPython, 0.34 s in Pyodide, level with the model; `solve_tick_ranges__dict_probe`). The longest such walk in any test is 5 steps. tests[6] stops a walk down (from 999999999999 to 0) but not a walk up.
   Fix: replace tests[6] with `{"call": "solve_tick_ranges('4 4\\n0 0 1000000000000 1000000000000\\n0 1000000000000 999999999999 1\\n')", "expect": "'0 1\\n2 3\\n-1 2\\n-1 2'", "compare": "equal"}` (the added query 1 is a million million steps below the next tick) and add `{"call": "(lambda r: (r.count('\\n'), sum(map(int, r.split()))))(solve_tick_ranges('100000 100000\\n' + ' '.join(str(10000000 * (i // 2)) for i in range(100000)) + '\\n' + ' '.join(str(i * 7919) for i in range(100000)) + '\\n'))", "expect": "(99999, 7919120)", "compare": "equal"}`. `how`: 13 hidden tests. Model and mine agree; the model takes 0.18 s on the large one in Pyodide; the walk finishes neither inside 6 s. Plant it last, slip "Dicts answer times that are present, but an absent time is walked up one millisecond at a time to the next tick.", and add `("ci-tick-ranges", 2)` to `SLOW_PLANTED`.

3. `minor` | `ci-tick-ranges` | brief.
   The fix lengthened one sentence to 43 words: "Write `solve_tick_ranges(text)`, which returns one line per query ... where `c` is the number of ticks before that time." The gate is 35 (drills brief step 4, SESSION PROTOCOL 4). It is the only sentence over the gate in the drills folder.
   Fix: "Write `solve_tick_ranges(text)`, which returns one line per query, joined by `"\n"`. A line holds the first and last position (counting from 0), separated by a space. When the time is not in the log the line is `-1 c`, where `c` is the number of ticks before that time."

4. `minor` | `ci-live-median` | tests[10] (new), tests[11] (as before).
   The new test holds size 0 twice (`+ 0` at event 0, `- 0` at event 300,000). Constraints[0] says sizes run from 1 to $10^9$. This is the class of findings 16 and 17, brought in by the fix for finding 3. tests[11], untouched, holds 201 zeros.
   Fix: add 1 to every size. tests[10]: `'+ %d' % (i * 7919 % 1000003 + 1)` and `'- %d' % ((i - 300000) * 3 * 7919 % 1000003 + 1)`, expect `(400000, 0, 199838746874, ['499938', '499938', '499935'])`. tests[11]: `'- %d' % ((i - 2) * 37 % 1000 + 1)` and `'+ %d' % (i * 37 % 1000 + 1)`, expect `(200000, 0, 99934787, ['500', '500', '500'])`. Model and mine agree on both. The data only shifts by 1, so the sorted list stays as slow.

5. `minor` | `ci-ready-blocks`, `ci-price-ramp`, `ci-right-edge-view`, `ci-funded-projects` | brief, examples, tests.
   Findings 11 and 12 asked for the author's own data. None of the 12 drills still holds a value the review named, and eight now carry data that is their own. Four carry the site's sample with the values renamed (site samples recalled from memory, as in the first review; `extra.py` part 3 compares order patterns):
   - `ci-ready-blocks`: `[2, 8, 5, 8, 3]` is `[1, 10, 3, 10, 2]` with 1, 2, 3, 10 renamed 2, 3, 5, 8, under the same three `(k, m)` calls. Every answer is the old one renamed.
   - `ci-price-ramp` tests[6]: `[7, 6, 2, 1, 2, 8, 3, 1, 3, 2]` is `[9, 8, 1, 0, 1, 9, 4, 0, 4, 1]` entry by entry (9 to 7, 8 to 6, 4 to 3, 1 to 2, 0 to 1; the second 9 to 8). Same length, same answer 7. The brief's example is new enough.
   - `ci-right-edge-view`: `(6, (3, None, (8, None, None)), (5, None, None))` is the old tree, the same four nodes in the same places, renamed.
   - `ci-funded-projects`: `(2, 2, [[2, 3], [3, 1], [3, 5]])` is the old case with 2 added to the fund and to every need; the story (one project open, then the larger of two) is the site's.
   Fix (every value below computed by the model and by mine, `proposed_tests.json`):
   - `ci-ready-blocks`, examples 0 to 2 and tests[2] to [4]: `earliest_ready_day([7, 2, 9, 4, 4, 6], 1, 3)` gives 4, `(..., 2, 2)` gives 7, `(..., 2, 4)` gives -1. Brief: "For `ready = [7, 2, 9, 4, 4, 6]`, `k = 1` and `m = 3` three servers are up by day 4. With `k = 2` and `m = 2`, day 6 gives one pair among servers 3 to 5, and day 7 adds servers 0 and 1, so that answer is 7." Notes: "Single servers: three are up on day 4."; "Day 6 has only one pair; day 7 brings up server 0 beside server 1."; "Four pairs need eight servers, and the rack has six."
   - `ci-price-ramp` tests[6]: `widest_ramp([8, 8, 7, 2, 8, 5, 1, 4, 2])`, expect 5 (both planted solutions fail it, with 4 and 2).
   - `ci-right-edge-view`, example 0 and tests[3]: `right_edge_view((4, (9, (2, None, (7, None, None)), None), (1, None, None)))`, expect `[4, 1, 2, 7]`. Brief: "In `(4, (9, (2, None, (7, None, None)), None), (1, None, None))` the rows are 4, then 9 and 1, then 2, then 7. The camera sees 4, 1, 2 and 7, so the answer is `[4, 1, 2, 7]`. The 2 and the 7 show although they hang on the left side." Note: "The 2 and the 7 are alone on their rows, so the camera sees them."
   - `ci-funded-projects`, example 0 and tests[2]: `funded_projects(1, 2, [[4, 6], [1, 2], [0, 3], [3, 1]])`, expect 10. Brief: "For `capital = 1`, `k = 2` and `projects = [[4, 6], [1, 2], [0, 3], [3, 1]]`, two projects are open at the start, and the profit of 3 takes the fund to 4. That opens `[4, 6]`, so the answer is `10`." Note: "Taking the profit of 3 first opens the project that needs 4."

6. `minor` | `docs/reports/drills-ci-4-check.py`, `docs/briefs/drills-ci-packs.md`, fix-pass note 2 | scripts and limits.
   - Note 2 says the per-word search "is a slow method in the check script and times out on it". The script stops a slow method at its first timeout, and prints "slow methods time out at [10]" for `ci-board-words`: the method without the letter-count check dies on tests[10], as it did before the fix, and never reaches tests[12]. No script in the repo shows that tests[12] stops a per-word search; only my timing above does. Fix: add the count-first search (`board_words__per_word_counts` in `drills-ci-3-4-scripts/wrong.py`) to `SLOW["ci-board-words"]` and assert that it times out at index 12.
   - The widened limits are sound: the validator caps a drill at 15 tests, and `ci-cell-formula` sits at 15. But the packs brief still says "two or three wrong solutions", and four drills now hold four (`ci-cell-formula`, `ci-first-misplaced`, `ci-live-median`, `ci-stock-by-prefix`). Fix: one line in the brief, "a fix pass may add a fourth, and a too-slow one goes last".
   - `SLOW_PLANTED` in pack 4 asserts a timeout at 5 s in CPython; the sorted list takes 8.6 s here, a margin of 1.7. A machine twice as fast fails the script while the app (16.9 s) is fine. No content change; raise the test or accept the note. `planted-check` is the real gate and is green.

7. `minor` | `ci-relay-masts` tests[12], `ci-cell-formula` tests[11], `ci-price-ramp` tests[11] | outside the delta, same class as findings 16 and 17.
   Found by the constraint script while checking the changed tests; none was changed by the fix pass, and the first review missed them. `ci-relay-masts` tests[12] puts marks up to about $10^{11}$ against a stated $10^9$ (the fixer corrected tests[7] of this file for the same fault). `ci-cell-formula` tests[11] is 600,002 characters against 600,000. `ci-price-ramp` tests[11] is 200,001 days against 200,000.
   Fix: `min_longest_gap([0] + [(i * i * 31) % 9973 + 10000 * i for i in range(1, 100000)], 5000000)`, expect 199; `formula_value('SUM(2,MAX(' * 49999 + '-3' + '))' * 49999)`, expect 99995; `widest_ramp(list(range(199999, 0, -1)) + [100000])`, expect 100000 as now. Model and mine agree on all three. Engine item, already named in the first review: a script that holds every test to the drill's constraints (`extra.py` part 2 is a start).

## The 18 findings of the review

- Resolved, verified: 1, 4, 5, 6, 7, 8, 13, 14, 15, 16, 17, 18.
- 2: resolved in the app (12.2 s for the per-word search with the count check); the check script does not hold it (finding 6).
- 3: resolved in the app (16.9 s against a 5-second limit); the new test breaks the size constraint (finding 4).
- 9 and 10: the tasks changed as proposed and every `expect`, example, note, hint and planted solution agrees with the new task; the tests still pass a solution with no search (findings 1 and 2), and one new sentence is over the voice gate (finding 3).
- 11 and 12: resolved in eight drills, renamed only in four (finding 5).

The fix pass introduced nothing `wrong`. What it introduced: the 43-word sentence, the two sizes of 0, and a note that claims more than the script shows.

## Counts

- `wrong`: 0.
- `weak`: 2 (findings 1 and 2).
- `minor`: 5 (findings 3 to 7).

## Verdict

Returns to the fixer, for findings 1 to 5: two drills whose tests still pass a method the constraints rule out, one sentence over the voice gate, one new test outside its constraint, and four samples renamed where the review asked for new data. Findings 6 and 7 can ride with the same pass.

Verified clean (read whole, mine agrees on every case, new planted solutions fail for the named reason, tests inside the constraints, no stale sentence): `ci-board-words`, `ci-busiest-links`, `ci-cheapest-pairs`, `ci-clear-rate`, `ci-downward-path-sums`, `ci-first-misplaced`, `ci-log-compactor`, `ci-no-repeat-rota`, `ci-rebuild-from-orders`, `ci-stock-by-prefix`, `ci-tray-queue`, `ci-van-convoys`, `ci-visible-masts`. Clean but for a finding above: `ci-ring-lookup` (1), `ci-tick-ranges` (2, 3), `ci-live-median` (4), `ci-ready-blocks`, `ci-right-edge-view`, `ci-funded-projects` (5), `ci-price-ramp` (5, 7), `ci-relay-masts`, `ci-cell-formula` (7, not from the fix pass).

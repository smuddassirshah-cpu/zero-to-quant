# Delta read, session AA: three fix passes

Scope: only what the three fix passes changed, read at commit 6bd4d57. No file of the three has changed since its fix pass.

- Fix pass 1 (drills `cpp`): `git diff d71960f^ d71960f -- app/content/drills/`. 21 `cpp-` drill files and one `index.json` row. Record: `review-drills-cpp.md`, "Fix pass".
- Fix pass 2 (drills `py`): `git diff 7fde608^ 7fde608 -- app/content/drills/`. 22 `py-` drill files and four `index.json` rows. Record: `review-drills-py.md`, "Fix pass".
- Fix pass 3 (problem sets): `git diff 58e5d81^ 58e5d81 -- app/content/courses/`. Six files, eleven items: `limits-thm/problems-4`, `markov/problems-4` and `-5`, `random-vars/problems-2`, `-4` and `-5`. Record: `review-problems-1.5-d.md`, "Fix pass".

Method. Each changed item and drill was read whole as it now stands, not only its changed lines. Every changed problem answer, tolerance and `wrong` value was recomputed in exact fractions and then by a second route: an eigenvector for the five acceptance rules of the supplier walk, a 20,000-hour simulation of the taxi rank, first-step equations for the two pattern waits, enumeration of the 210 hands and the 10,000 ordered draws, a series for the retry time, a double integral for the fault gap. For the drills I wrote my own solution to each drill whose tests or starter changed (9 Python, 17 C++), by another method wherever one exists, and ran model, mine, starter and every planted solution on every example and hidden test: Python in CPython under the first reader's copy of the page's comparison, C++ natively with g++ 13.3 and clang++ 18.1 and then in the app's own runtime (clang 21 to wasm32) on a copy of `app/`. Every new or changed `expect` was also recomputed apart from any solution (fractions, whole numbers, mpmath, counting). For each planted solution the C++ fix pass added, the new tests were taken out again on the copy to see that they, and only they, catch it in the app. Authors' scripts, `planted-check`, the validator, the voice scan and the playthrough were run.

Scripts: `docs/reviews/delta-session-aa-scripts/`, run from the repo root with the scratchpad venv Python: `problems.py`; `py_run.py` with `mine_py.py`; `py_extra.py`; `cpp_run.py [fuzz]` with `mine_cpp.py` (`ZQ_TMP=<scratch>`, `CXX=clang++` for the second compiler); `cpp_extra.py`; `app_probe.py <copy> <pkgs> mine|probes|newonly`; `expr_probe.mjs <pkgs>` and `expr_scale_scan.mjs <pkgs>`; `voice.py`; `show.py`, `drill_text.py` and `drill_fields.py` print an item or drill for reading.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` / `weak` = a statement reads two ways, or the tests miss a rule the fix pass wrote; `minor` = otherwise.

## Tool results

- `drills-cpp-check.py`: `25 drills, 354 cases compared`, `errors: 0`. `drills-py-a-check.py`: `18 drills, 62 planted, errors: 0`. `drills-py-b-check.py`: `12 drills, 43 planted, 0 errors`.
- `problems-random-vars-numbers.py` 1,333 checks, `problems-limits-thm-numbers.py` 1,539, `problems-markov-numbers.py` 1,815: 0 failures each.
- `problems.py`: 42 checks, 0 failures. No changed answer, tolerance or `wrong` value is wrong; no two bands meet in the six files; every `wrong` id has its `byKey` line.
- `py_run.py`: 30 models pass, 30 starters fail, my 9 solutions pass every example and test, all 105 planted solutions fail a test, every `how` count and index row agrees with its file, mix 9 / 12 / 9. `py_extra.py`: 11 checks pass, 2 fail (finding 8).
- `cpp_run.py fuzz`, g++: 25 models pass, 25 starters fail, my 17 solutions pass, all 89 planted solutions fail a test, `how` counts and index rows agree. Under clang++ the only difference is the planted `cpp-high-water` [1], the undefined read the first review already recorded. 400 random texts: model and mine agree with the brief of `cpp-fill-csv` read as a regular expression.
- `cpp_extra.py`: every new or changed `expect` agrees with my value; two checks record findings 4 and 5.
- `planted-check --require` in the app: 21 `cpp` drills, 77 planted, 0 failures; 22 `py` drills, 81 planted, 0 failures.
- `app_probe.py mine`: my 17 C++ solutions pass every hidden test in the app. `newonly`: with the fix pass's new tests removed, each of its 14 new C++ planted solutions passes every remaining test in the app, so the new tests are what catch them. `probes`: finding 2.
- `playthrough --mobile --drill` on the 21 and the 22 changed drills: all passed. `playthrough --problems` on the six sets, with and without `--mobile`: all passed.
- `node tools/validate.mjs`: 0 errors. `voice-scan.py 35` on the drills and the three courses: 0 and 0. `voice.py`: no em-dash and no exclamation mark in prose.
- No drill `expect` is wrong.

## Findings: fix pass 1 (drills `cpp`)

1. `unclear` | `cpp-crossings.json` | `constraints[0]`, `notes[0]`.
   The fix added a hidden type `Px` and a twelfth test, and `how` now says the tests also use "a type that has only `<`". `constraints[0]` still reads "The tests call the template with `int`, `long long` and `double`", and `notes[0]` "One template serves all three types". A learner whose version is right by its results but uses `>` or `==` now fails all 12 tests on a compile error that names `Px`, a type no line of the brief or the constraints mentions (`cpp_run.py`, probe "right results, uses > and ==": 12 of 12 fail, in the app too).
   Fix: `constraints[0]`: "$0 \le n \le 10^5$ values. The tests call the template with `int`, `long long`, `double` and a small struct that has only `<`." `notes[0]`: "One template serves every type the tests use; the compiler writes a version for each `T`."

2. `weak` | `cpp-fill-csv.json` | brief, `tests`.
   The fix pass wrote a new rule into the brief, "Drop one `\r` at the end of a line; a `\r` anywhere else is another character and makes the row bad", and tested the second half only. No test has two carriage returns at a line end, so a reader that strips every trailing `\r` passes all 15 tests, natively and in the app (`app_probe.py probes`: "passes all 15 hidden tests"). It is the fault class the first review was about: a sentence the tests do not hold.
   Fix: replace `tests[14]` (`"1\r2,5\n3,4\n"`, 12) with `{"call": "fills_value", "args": ["1\r2,5\n3,4\r\r\n6,1\n"], "types": ["std::string"], "expect": 6, "compare": "equal"}`. Model and mine give 6, the strip-all version 18, and planted [4] still fails with 78 (`cpp_run.py`, last lines). The count stays 15.

3. `minor` | pack, `docs/reports/drills-cpp-check.py` | difficulty mix.
   The brief asks for eight, ten and seven at difficulties 1, 2 and 3 (`docs/briefs/drills-1.1-1.9.md` line 8). Moving `cpp-drop-small` to 1 leaves 9 / 9 / 7, and the fix pass changed `want_mix` in the check script from 6 / 7 / 4 to 7 / 6 / 4 so that the script passes. The `py` fix pass kept its pack on the brief's 9 / 12 / 9.
   Fix: set `cpp-clip-returns` to difficulty 2, pace 540: with the starter cut to a comment the learner must now choose both reference parameters unaided. Change its index row, put `want_mix` back to 6 / 7 / 4 and update the mix line of `drills-cpp.md`. Or record 9 / 9 / 7 in DECISIONS.

4. `minor` | `cpp-prob-between.json` | `constraints[0]`.
   Review finding 10 said the model leaves its own tolerance inside the stated constraints. The new bound, 5 standard deviations, closes the cases the review named and all 10 tests keep to it. A narrow band high in the tail is still inside it and still off: `prob_between(0, 1, 4.99, 5)` gives 1.524489057e-08 against a true 1.524489064e-08, a relative error of 4.6e-9 (`cpp_extra.py`, mpmath at 40 digits). At 4.9 to 5 the error is 1.1e-10. No test goes there.
   Fix: add to `constraints[0]`: "In the tests `b - a` is at least half a standard deviation, or the band is empty."

5. `minor` | `cpp-running-stats.json` | `constraints[0]` against the brief's new third paragraph.
   The fix pass put Welford's update and the merge formula in the brief. `constraints[0]` promises more than they give: "Values may sit near $10^9$ with a spread of a few units, and the variance must still be within a relative 1e-9." On 500 random values near $10^9$ the brief's own method is out by up to 2.5e-8, and merged with 300 more by up to 3.4e-7 (five seeds, against exact fractions). The four tests near $10^9$ hold at most five whole numbers each, where the method is exact, so no learner is marked wrongly. The constraint predates the fix pass; the brief now makes the gap visible.
   Fix: "Up to $10^6$ values. Values may sit near $10^9$ with a spread of a few units, where a plain sum of squares is wrong in its first digit. The tests there use short lists of whole numbers, on which the running method is exact."

## Findings: fix pass 2 (drills `py`)

6. `unclear` | `py-excess-vs-benchmark.json` | brief, second paragraph.
   The sentence added for review finding 6 reads "A share that misses a date still meets the index's one-day return that day, so its excess then sets a two-day return against a one-day one". "That day" is the missed date, on which the share has no return and no excess. The mismatch falls on the share's next date. The sentence also uses "excess" one sentence before the brief defines it. The rule itself and the new test are right (GAP 100 to 103 across the gap, index flat on the 8th, 300 basis points; the per-share-dates version gives 200).
   Fix: move it after the definition and reword: "The excess return of a share on a date is its return less the index's. After a date the share misses, its next return spans two days while the index's still spans one; real code would flag it."

7. `minor` | three drills | `hint`, `where`.
   Text left out of step with an edit of the same pass. (a) `py-fx-to-pounds`: the hint and `notes[0]` say `r.reshape(len(r), 1)`, but the starter no longer makes `r` (the `np.asarray` lines were cut for finding 13), and a plain `rates` list has no `reshape`. (b) `py-growth-curve`: the hint still says "append `last * (1 + r)` for each return in turn", which raises `TypeError` on the new `None` days. (c) `py-day-fills`: `where` still says "`groupby` with named aggregations", the form the new hint was written to avoid.
   Fix: (a) hint: "Make `r = np.asarray(rates, dtype=float)`. A 1-D array of rates lines up with the last axis, the shares. Turn it into a column, `r.reshape(len(r), 1)` (`r[:, None]` is the short form), so it stretches across each row instead." (b) hint: "Start the list with `start`. For each return append `last * (1 + r)`, or `last` again when the return is `None`." (c) `where`: "Draws on numpy-pandas lesson l12-split-apply-combine: sums and a count inside each group."

8. `minor` | `docs/reports/drills-py-a.md`, `docs/reports/drills-py-b.md` | tables.
   The difficulty and pace cells were brought up to date; the hidden-test and planted counts were not. Seven rows are stale: `py-cross-up-days`, `py-split-pence`, `py-batches`, `py-cost-basis`, `py-growth-curve` and `py-month-grid` in A, `py-excess-vs-benchmark` in B (`py_extra.py`, last two lines; for example `py-growth-curve` still shows 10 tests and 3 planted, now 12 and 4). The `cpp` report was updated in full. This is session Z's finding 10 again.
   Fix: update the rows, or add under each table: "Counts as authored; see `docs/reviews/review-drills-py.md`, Fix pass, for later changes."

9. `minor` | `py-carry-forward-limit.json`, `py-combined-desk-pnl.json`, `py-day-fills.json`, `py-gap-aware-returns.json` | `starter`.
   Finding 13 named eight `numpy-pandas` starters and all eight are now blank. The other four keep a stub: `out = close.copy()` (which is the answer to the limit 0 case the hint points at), `m = ...` with `return a + b`, `df = fills.copy()` with `out = ...`, and `ret = ...`. The pack now has two starter styles in one course. The first review did not name these four, so this is not an omission of the fixer.
   Fix: the house form for all four: imports, the signature, `# your code here` and a failing return (`return close`, `return a`, `return fills`, `return close`). Rerun the starter check of `drills-py-b-check.py`.

## Findings: fix pass 3 (problem sets 1.5 d)

10. `minor` | `random-vars/problems-4.json` | `p-courier-vans` | part 4, question.
    The sentence added for finding A11 reads "Part 3 showed the rows differ, so each has its own mean." Part 3 showed one cell that differs from the product of its margins. Dependent variables can have equal conditional means, so the "so" teaches a rule that is false in general. It is true of this table (0.5 against 0.9).
    Fix: "Part 3 showed the number of vans changes the chances of late parcels. Using the two-van row, ..."

11. `minor` | `limits-thm/problems-4.json` | line 723.
    The edit left the closing brace of `byKey` on the end of the `one` line, after twelve spaces. The file parses and nothing shows to a learner.
    Fix: put the brace back on its own line.

12. `minor` | engine | review finding A8, left as an inbox bullet.
    The fixer was right not to add the two root-spelt slips, though not for the reason recorded. On the real `grade.js`, `\frac{4}{\sqrt{1-2s}}` grades equal to `\frac{1}{\sqrt{1-2s}}`, so the proposed slips `one-root` and `added-root` would have shadowed each other (`expr_probe.mjs`). The cause is wider than a sampling range: the grader reads only the real part of a value, so two expressions that are pure imaginary at every sample point compare equal whatever their size. `\sqrt{x-5}` equals `3\sqrt{x-5}`, and `\sqrt{1-2s}` equals `\frac{1}{\sqrt{1-2s}}`. No present item is marked wrongly by it: of 497 `expression` answers in `app/content`, none grades equal to twice itself (`expr_scale_scan.mjs`).
    Fix: extend the inbox bullet under `Raised later (problems fix pass d):` with "The grader also reads only the real part: at a point where both sides are complex it should compare both parts, or skip the point, and it should not pass a pair with no real point checked."

## Was each review finding resolved

Fix pass 1, review findings 1 to 19: all resolved. The entries marked "in part" (14 and 16) each take an option the review offered, and in 6 the correct but slow `mean_ranks` is rightly left unplanted. Checked in particular: finding 1 (`pounds_to_pence(30000000.01)` is 3,000,000,001, and `std::lround`, which the review could not run, now fails that test in the app's 32-bit `long`); finding 6 (the quadratic count fails the 100,000-score test on time, natively and in the app; the `<=` comparator fails both new tests); finding 7 (the 60 tied symbols are exactly tied as doubles, so `constraints[1]` holds); finding 11 (the version with other operators no longer compiles); finding 15 (my solutions were written from the brief and the cut starters alone, and each brief gives every type and signature needed). New faults: findings 1 to 3. Left short of the review's aim: finding 4.

Fix pass 2, review findings 1 to 18: all resolved, 14 (b) and (c) accepted as the review allowed. Checked in particular: finding 1 (the 10,000 keys of `tests[10]` are distinct real dates in rising order, and my date-parsing solution passes); finding 8 (no test text is `'nan'` or `'inf'`, and `' 4.80 '` and `'1,200.00'` behave as the brief now says); finding 9 (no weekend date in any call); finding 15 (one-day table right, square table wrong without an error, 2 by 3 raises); finding 18 (9 / 12 / 9, index rows equal the files). New faults: findings 6 to 9.

Fix pass 3, findings A1 to A13 and B1: all resolved; A8 left to the engine with reason (finding 12), A13 accepted. Checked in particular: A1 (uniform under the keyed rule only; the old option $\tfrac{1}{\deg(j)}$ was uniform too; $\tfrac{1}{\deg(i)}$ gives shares proportional to the squared degrees, H at $\tfrac{16}{26}$, the same law as the `flipped` option, whose `why` agrees); A2 (hourly losses have variance 2.5 times their mean in simulation, so "not a Poisson stream" is true); A10 (the band 3.3577 to 3.3647 takes 3.3584, 3.3640 and the unrounded 3.3639); A12 (1,152 and 1,153 both pass, and the slips at 952.38 and 866.67 stay clear); B1 (43.7245 inside 43.72 with `tol` 0.005). New faults: findings 10 and 11.

## Verdict

- Fix pass 1 (drills `cpp`): **closed for answers and tests; one short follow-up**. `wrong` 0, `unclear` / `weak` 2, `minor` 3. Findings 1 and 2 are two sentences and one test; 3 needs a decision; 4 and 5 are one constraint line each.
- Fix pass 2 (drills `py`): **closed for answers and tests; one short follow-up**. `wrong` 0, `unclear` 1, `minor` 3. Finding 6 is one sentence of a brief; 7 is three lines; 8 and 9 can ride with the next pass on the pack.
- Fix pass 3 (problem sets): **closed**. `wrong` 0, `unclear` 0, `minor` 3. Nothing returns to the fixer; findings 10 and 11 can ride with the next problems pass, and 12 is an engine note.

## Verified clean

Problem sets, changed graded values (each recomputed twice, with the item read whole):

| item, part | now | check |
|---|---|---|
| `p-supplier-survey` 3, option `inverse` | $\tfrac{1}{\deg(i)}$, still wrong | stationary law $(\tfrac{8}{13}, \tfrac{2}{13}, \tfrac{2}{13}, \tfrac{1}{26}, \tfrac{1}{26})$ by balance and by eigenvector; exactly one option is uniform |
| `p-file-retry` 2, `carried-both` | 1, `tol` 0.0005 | $m = 0.5 + 0.5m$; clear of 4.2, 3, 2.1, 2 and 1.4 |
| `p-startup-rounds` 3, `count-squared` | 3.3612, `tol` 0.0035 | $16 \times 0.2099 = 3.3584$; with the count term 3.3640; answer 0.8452 untouched |
| `p-two-loss-cut` 5 | 1152.38, `tol` 1 | $\tfrac{1}{0.3} + \tfrac{1}{0.063} = 19.2063$ by the pattern rule and by first-step equations; $60 \times 19.21 = 1152.6$ |
| `p-token-draw` 5, `carried-half` | 43.72, `tol` 0.005 | $38 + 15(0.3483 + \tfrac{1}{30}) = 43.7245$; 0.3483 by formula and by 10,000 ordered draws |

Also clean: `p-taxi-rank` parts 4 and 5 (11.8154, 7.2796, 4.5358; simulated loss rate 11.86); `p-regime-sampler` part 5 ($\tfrac{50}{77}$ by balance and by a matrix power; Mid is over-weighted, as the new sentence says); `p-part-errors` part 3 ("finite near 0"); `p-machine-faults` part 4 ($e^{-2}$, by a double integral over the wedge; part 5 restates what it needs); `p-ticket-stages` part 3 `rates` (the slip is named, and the stored slip still routes: `expr_probe.mjs`); `p-courier-vans` part 5 ($0.38 + 2 \times 0.14 = 0.66$, £3.96).

Drills `cpp`, tests the fix pass added or replaced (each `expect` by my own value and by my C++ solution; "catches" is what the new planted solution returns):

| drill, test | expect | catches |
|---|---|---|
| `cpp-cash-split` [1] | 3000000001 | `int` round: 2147483647 |
| `cpp-fill-csv` [13], [14] | 10, 12 | one reader for both fields: -20; every `\r` dropped: 72 |
| `cpp-compound-df` [10], [11] | 0.9854695516134061, 0.9566303671497992 | whole periods: 1 and 0.9709 |
| `cpp-session-time` [12], [13] | true, false | raw counts: false and true |
| `cpp-tick-log` [11] | [1, 0, 1, 0] | `int` times: [1, 1, 2, 1294967297] |
| `cpp-mean-ranks` [11], [12] | [50.5, 91950.5, 8150.5], [1500.5, 1500.5] | `<=` comparator: crash; quadratic count: out of time |
| `cpp-movers` [12], [13] | `["H"]`, 60 symbols in three tied groups | divide first: `[]`; no tie-break: out of order |
| `cpp-fee-pence` [12] | 999900000000 | `double` ceiling: 999899999999 |
| `cpp-high-water` [9], `cpp-range-out` [12] | [0.1, 0.3, 0.3], [1, 0.1, 0.7] | `float`: 0.10000000149 |
| `cpp-trimmed-mean` [12] | 100000002.33333333 | `float` sum: 100000000 |
| `cpp-scaled-payoff` [10] | 0.09999999999999432 | `float` strike: 0.0999985 |
| `cpp-crossings` [11] | 3 | other operators: does not compile |
| `cpp-fee-tier` [7] to [9] | by bisect | (test count; one asks at $10^{13}$, one has twenty tiers) |
| `cpp-take-all` [8], [9] | `run_take(5, 1)`, `run_take(1, 5)` | (test count) |

Drills `cpp` clean in full (statement, examples, notes, tests, planted, starter): `cpp-cash-split`, `cpp-compound-df`, `cpp-session-time`, `cpp-tick-log`, `cpp-mean-ranks`, `cpp-movers`, `cpp-fee-pence`, `cpp-high-water`, `cpp-range-out`, `cpp-trimmed-mean`, `cpp-scaled-payoff`, `cpp-fee-tier`, `cpp-take-all`, `cpp-clip-returns`, `cpp-drop-small`, `cpp-tick-round`, `cpp-bermudan-put`. Each of the five cut starters fails every value test, and its brief names every type the learner must write. `docs/reports/drills-cpp.md` carries the file's difficulty, pace, test and planted counts in all 25 rows.

Drills `py`, tests added or changed (model, the check scripts' second method and mine agree):

| drill, test | expect | catches |
|---|---|---|
| `py-paired-returns` [10] | unchanged | (keys are now real dates) |
| `py-cross-up-days` [12], [13] | `[]`, `[]` | each mixed-day form: `[1]` |
| `py-split-pence` [12] | `[55, 55]` | `math.ceil`: `[56, 55]` |
| `py-batches` [13] | `['a', 'b', 'c']` | read-ahead: `RuntimeError` |
| `py-cost-basis` [13], [14] | `(10, 2.0, 0.0)`, `'ValueError'` | zero-only check: `(6, -2.67, 0.0)`; check after: `(6, 2.0, 0.0)` |
| `py-excess-vs-benchmark` [10] | `[300.0000000000003]` | per-share dates: 200 |
| `py-month-grid` [14] | `[[-1.0]]` | truth test: `[[None]]` |
| `py-growth-curve` [10], [11] | carries over on `None` | `None` as a total loss: 0.0 |
| `py-day-fills` [5] to [10] | unchanged | (helper renamed `make_fills`) |

Drills `py` clean in full: `py-batches`, `py-best-desk-each-day`, `py-big-move-days`, `py-cost-basis`, `py-cross-up-days`, `py-format-pence`, `py-guarded-returns`, `py-month-grid`, `py-month-hit-rate`, `py-paired-returns`, `py-prior-zscore`, `py-split-pence`, `py-volume-surge`, `py-weekly-range`, `py-wide-to-long` (both readers give the same rows on all 14 test texts). The two examples added to briefs are right: `np.argmax` of `[[1, 5, 5], [7, 2, 3]]` along `axis=1` is `[1, 0]`; `f'{1234567:,}'` is `'1,234,567'` and `f'{5:02d}'` is `'05'`.

## Counts

| fix pass | wrong | unclear / weak | minor | verdict |
|---|---|---|---|---|
| 1, drills `cpp` | 0 | 2 | 3 | closed, short follow-up |
| 2, drills `py` | 0 | 1 | 3 | closed, short follow-up |
| 3, problem sets 1.5 d | 0 | 0 | 3 | closed |

Finding classes (SESSION PROTOCOL 6). "A pack report left behind by a fix pass" is now seen twice (session Z finding 10, finding 8 here). "A check script's target moved to fit the content" (finding 3) is new. "A rule the fix pass wrote into a brief without a test" (finding 2) is the class of the three drill reviews, now seen in a fix pass: a fixer who adds a sentence to a brief should add or adapt a test for it in the same pass.

## Fix pass

1. Fixed: `cpp-crossings` `constraints[0]` now names the small struct that has only `<`; `notes[0]` says "every type the tests use".
2. Fixed: `cpp-fill-csv` `tests[14]` replaced by `"1\r2,5\n3,4\r\r\n6,1\n"`, expect 6 (the row `3,4\r` is bad after one `\r` is dropped; strip-all would add 12 and give 18). Planted-check: 5 planted, 0 failures.
3. Fixed: `cpp-clip-returns` to difficulty 2, pace 540 (file and index row); `want_mix` back to 6 / 7 / 4; `drills-cpp.md` row and mix line updated (8 / 10 / 7 in all, the brief's mix). The check script passes.
4. Fixed: `cpp-prob-between` `constraints[0]` adds that `b - a` is at least half a standard deviation, or the band is empty.
5. Fixed: `cpp-running-stats` `constraints[0]` reworded as the reader gave it (no promise beyond the running method on whole-number tests).
6. Fixed: `py-excess-vs-benchmark` brief: definition first, then "After a date the share misses, its next return spans two days while the index's still spans one; real code would flag it."
7. Fixed: (a) `py-fx-to-pounds` hint makes `r = np.asarray(rates, dtype=float)` first (`notes[0]` left, it only describes the reshape); (b) `py-growth-curve` hint handles `None`; (c) `py-day-fills` `where` reworded.
8. Fixed: the seven stale rows of `drills-py-a.md` and `drills-py-b.md` now carry the file's test and planted counts (cross-up-days 14/5, split-pence 13/4, batches 14/4, cost-basis 15/5, growth-curve 12/4, month-grid 15/4, excess-vs-benchmark 11/5).
9. Fixed: the four starters (`py-carry-forward-limit`, `py-combined-desk-pnl`, `py-day-fills`, `py-gap-aware-returns`) now use the house form: signature, `# your code here`, failing return. Starter check passes in planted-check and `drills-py-b-check.py`.
10. Fixed: `random-vars/problems-4` `p-courier-vans` part 4 question now says part 3 showed the number of vans changes the chances of late parcels.
11. Fixed: `limits-thm/problems-4` closing brace of `byKey` back on its own line.
12. Fixed: bullet added to `docs/BACKLOG-INBOX.md` under `Raised later (delta session AA):` (the reader's wording; the pass-d bullet is about sampling, so a new section was used).

Graded answers and test `expect` changed: one test `expect`, `cpp-fill-csv` `tests[14]` (12 to 6, with its input), no graded problem answer.

Gates: validator 0 errors; voice scan 0 and 0 on drills, limits-thm, random-vars; `planted-check --require` on the 12 changed drills 0 failures; `drills-cpp-check.py` 354 cases, 0 errors; `drills-py-b-check.py` 0 errors; `playthrough --drill` on the 12, desktop and `--mobile`, all passed; `--problems` on random-vars/problems-4 and limits-thm/problems-4, both widths, all passed; numbers scripts random-vars 1333 and limits-thm 1539 checks, 0 failures.

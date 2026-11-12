# Delta read AC-2: three fix passes that changed graded content and were never re-read

Scope: the last `## Fix pass` section of three reviews, each changed item read as the files stand now.

- a. `review-delta-bank-2.md` (commit 6392a67), `app/content/bank/`: four keys, six slip values, two added `wrong` entries, one choice set, one code line (`pf-types-round-half-even`), one prose fix (`es-mle-waits-between-trades`); six hidden tests swapped (`ds-pointers-merge-ticks` 9, `edge-case-list-to-pence` 5, `pf-idioms-count-above-mean` 5, `edge-case-list-second-largest` 4, `at-search-count-in-range` 10, `pf-collections-top-symbols` 10).
- b. `review-delta-holes.md` (commit 60d52d1): three keys (`p-lawn-pond` part 3, `e-odds-update`, `e-diameter-ends`), one added `wrong` entry (`p-windy-ride` part 4), two question or line edits (`p-disk-failures` part 5, `p-hall-tiles` part 2), and the `let`, `where` and `wrong` of two Fluency families (`two-by-two`, `poisson-ratio-test`), one prompt (`wilks-df`).
- c. `review-delta-drills-ci-5-8.md` (commit 3eb5b96): `ci-loop-cables` tests[12] added, `ci-drop-point-routes` tests[14] added, `ci-first-fit-slot` tests[7] swapped.

Not in scope: the behavioural models, freshness of the re-authored items, the drills whose text only changed.

Method. Keys, bands and `wrong` values: `recompute.py` recomputes each from the item's prose by two routes (fractions against floats, a matrix inverse, a bisection, an integral, a count-up, sympy, a simulation for the Sharpe claim), checks each stored value against its band, each slip against the key band, every pair of bands, the id-to-line map both ways, and the sentences that print the numbers. `grade.mjs` puts about 200 typed strings through the engine's `numGrade` and `exprGrade` (local Compute Engine, no browser): other right forms, each slip rounded and unrounded, the old keys, neighbours either side of each band. The two Fluency families are checked over every draw, not a sample (`fluency_all.py`: 13,845,841 tables and 3,120 Poisson draws, the `let` strings read from the files). Hidden tests, under the binding rule of session AB: `bank_code.py` and `drills_code.py` run the model, the starter, a solution of my own by a different method, and every candidate of both earlier readers, on the tests before the pass and now; drills are run in three states (before the pack's first fix pass, before 3eb5b96, now) with every planted solution of every state. Each changed `expect` is recomputed by my solution and by a brute route; drills also against a brute force on 3,000 random small inputs each. Inputs are checked against the typed `constraints` objects. C++: none of the changed items is C++.

Scripts: `docs/reviews/review-delta-ac-2-scripts/`, run from the repo root with the scratchpad venv Python: `recompute.py`; `fluency_all.py`; `bank_code.py [id ...]` (give the two slow tasks, `at-search-count-in-range` and `pf-collections-top-symbols`, one a command); `drills_code.py [id ...]`; `loop_side.py`; `proposed_code.py`; `node grade.mjs --local-cdn <pkgs> [--show]`; reading aids `show_code.py`, `show_item.py`, `show_part.py`.

Tags: `wrong` = a learner is marked wrongly or told something false about the subject; `unclear` = a line reads wrongly for a second way of reaching it; `minor` = otherwise.

## Tool results

- `recompute.py`: 138 checks, 0 failures, 3 FINDING rows (findings 1 and 4). Every changed key, slip value and printed number agrees by two routes; no figure of an old version is left in a re-authored item.
- `grade.mjs`: 345 checks, 0 failures, 6 FINDING rows (finding 4). Every stored answer and `accept` form grades correct, every `wrong` value lands on its own id and has a line, no band meets another or the key band, every old key is refused.
- `fluency_all.py`: 0 failures, 0 FINDING rows. `two-by-two` keeps 3,659,984 of 13,845,841 tables (26.4%); `poisson-ratio-test` keeps 1,299 of 3,120 draws (41.6%).
- `bank_code.py`: exit 0. 131 candidates run on the six tasks (44 of the first reader, 67 of the delta reader, 20 of mine). None that failed before the pass passes now. Passing every test now: `index-method` (known, stopped in the page), and three of mine (findings 2 and 3, and a note).
- `drills_code.py`: exit 0. 40 candidates and planted solutions over the three drills, three states each; 0 pass now, 0 regressed; every planted solution of the files as they stand fails. `loop_side.py`: exit 0.
- Earlier readers' scripts rerun: `review-delta-bank-2-scripts/code_run.py` on the six tasks, tried 67, passing 1 (`index-method`), exit 0; `proposed.py` 21 of 21; `review-delta-bank-2-fix-scripts/grade_new.mjs` 113 checks, 0 failures; `pyo_time.mjs` (Pyodide 0.27.7 under node): models at most 0.15 s a case, `slice-len` 8.51 s and `index-method` 8.65 s and `first-seen-list` 23.5 s on their slow test, all over the 5 s limit.
- `node tools/validate.mjs`: 0 errors, 5,020 warnings. `manifest.json` unchanged.
- No browser and no `playthrough.mjs` run, as asked.

## Findings

| id | file # item | tag | what is wrong | proposed fix |
| --- | --- | --- | --- | --- |
| 1 | `bank/coding-1.json` # `pf-types-round-half-even` `feedback.byKey.half-up`, `.half-away` | `unclear` | The new four-term line lets two slips reach each of -11 and -13, and each line names only one. -11 is "rounded each half up" (-1, -1, -4, -5) and also `-9 // 2` taken as -4 with everything else right (-1, -2, -4, -4). -13 is "half away from zero" (-1, -2, -5, -5) and also `int(-1.5)` taken as -2 (-2, -2, -4, -5). The learner who cut `//` towards zero, the commonest slip on this line, is told "You rounded each half up, to -1 and -4", which they did not. The Python facts in both lines are true (`recompute.py`, "one term misread"). | `byKey.half-up`: "That is one too high. You rounded a half up, taking `round(-1.5)` as -1, or you cut `-9 // 2` to -4. Python 3 sends an exact half to the even neighbour, -2, and `//` rounds down, to -5." `byKey.half-away`: "That is one too low. You rounded `round(-4.5)` away from zero, to -5, or you took `int(-1.5)` down to -2. Python 3 sends an exact half to the even neighbour, -4, and `int` cuts towards zero, to -1." Ids, values and bands stay. |
| 2 | `bank/coding-2.json` # `ds-pointers-merge-ticks` `tests` | `minor` | The swap of test 9 moved the "neither list is changed" check from feeds with no shared time to feeds with one, so the check no longer runs on the case with no shared time. No recorded candidate regressed. A solution of mine that changes a list only when no time is shared (`out = a; out += b` on that branch) failed the old test 9 and passes all 10 now (`bank_code.py` `x-sort-into-b`, `proposed_code.py` `alias-when-no-shared-time`). | Add the old test back as an eleventh, keep the new one: `{"setup": "a = [(1, 1.0), (3, 1.0)]; b = [(2, 2.0)]", "call": "(merge_ticks(a, b), a, b)", "expect": "([(1, 1.0), (2, 2.0), (3, 1.0)], [(1, 1.0), (3, 1.0)], [(2, 2.0)])", "compare": "equal"}`; `how`: "Submit runs 11 hidden tests. Each result must equal the expected value." Model, my solution and the three right alternatives pass it; the candidate fails it (`proposed_code.py`). An added test cannot let a caught candidate through. |
| 3 | `bank/coding-2.json` # `edge-case-list-second-largest` `tests` | `minor` | Not caused by the swap, seen while rerunning it: no hidden test has 0 as the second value, so `return top - second if second else None` passes all 9 tests and returns `None` for `[7, 0, 7]` (`bank_code.py` `x-falsy-second`). The item is tagged `edge-case-list`, and a zero read as "missing" is that kind of slip. | Add a tenth test: `{"call": "runner_up_gap([7, 0, 7])", "expect": "7", "compare": "equal"}`; `how`: "Submit runs 10 hidden tests. Each result must equal the expected value." Model, my solution and `two-max` pass it; the candidate returns `None` (`proposed_code.py`). |
| 4 | `exams/topic-2.1.json` # `e-odds-update` `widget.wrong[3]` (`decimal`) | `minor` | The pass widened the `decimal` band from the 0.00002 proposed to 0.0005 to quiet the validator's `[wrong-band]` advisory. With unit `%` a typed `0.201` is read as 0.00201 and `0.12` as 0.0012, and both now fall in 0.00167 ± 0.0005. So a learner who stops at the odds (0.201) or multiplies the probability (0.12) and types a decimal is told "That is the probability as a fraction of 1. Type it as a percentage: 16.7." That is not what they typed, and it hands them the key. `0.2`, `0.2008`, `0.1205` and `0.15` do the same (`grade.mjs`, 6 rows). | `widget.wrong[3].tol.abs`: 0.00006. It still takes `0.166`, `0.167`, `0.1672`, `0.16722`, `0.168` and `0.17`, and leaves `0.2`, `0.201`, `0.2008`, `0.12`, `0.1205` and `0.15` to the generic line (`grade.mjs` PROPOSED rows, `recompute.py`). The validator will print one `[wrong-band]` advisory for it: the rule assumes the slip is typed at the asked rounding, and this slip is the answer in another unit, so the advisory does not apply. |

## Notes, not findings

- `at-search-count-in-range` test 10: `slice-len` and `index-method` give right answers and are stopped only for time, at 8.5 s and 8.65 s against a 5 s limit under node on this machine. A machine twice as fast lets them through. The prose asks for $O(\log n)$ and the model takes 0.04 s, so no right solution is at risk; no change proposed.
- `edge-case-list-to-pence`: a solution that strips only the left side passes all 10 tests before and after the swap (it returns 305 for `" £3.5 "`). Rare in practice; a test `to_pence(" £3.5 ")`, expect `350`, would catch it if the item is touched again.
- `ci-loop-cables`: the new tests[12] is aimed at rack `a` hung under the other root. The mirror slip (rack `b`) was already caught by the small tests 6 and 8 (`loop_side.py`).
- `ci-first-fit-slot`: the test taken out in the swap, `first_fit([[10, 20], [25, 30]], 12, 5)`, had `start` inside a booking and a gap filled exactly, joined on both sides. Test 6 still holds an exact fit joined on both sides, and test 9 a push from inside a booking. No candidate or planted solution of any state was caught by the removed test alone (`drills_code.py`, columns `mid` and `now`).
- `e-odds-update` key band: 0.167 ± 0.0015 accepts 16.6 and 16.8. Working with the printed 0.667 and 0.30 gives 16.67, so the width is needed.

## For the main session

- The rerun of the first reader's candidates recorded by fix pass a ("tried 175, passing 0") was empty for two of the six tasks. `edge-case-list-second-largest` and `pf-collections-top-symbols` were restated under new function names by the earlier fix pass, so all 16 first-reader candidates for them raise `NameError` on every test and count as "caught". `bank_code.py` wraps them under the new names (`ADAPT`) and prints `VACUOUS` for any candidate that fails every test by `NameError`; under the wrappers all 16 are caught by a wrong answer or for time. A rule for the rerun: a candidate whose every failure is a `NameError` or a load error is not a rerun.
- Two first-reader "alt" solutions (`stable-sort` for `merge_ticks`, `alphabetical-then-stable` for the top symbols) were written for the statements before the restating and give wrong answers under the present ones. They are not right solutions refused.

## Verified

Fix pass a, bank part 2:
- `collinear-features-inflation-factor`: key 4/3 by $1/(1 - r^2)$ and by the inverse correlation matrix; band 0.005 takes 1.33, 1.333 and 4/3; `one-minus-r` 2 and `standard-error-factor` 1.1547 (stored 1.15, takes 1.15 and 1.155) land on their ids; 1.5625, 2.5 and 1.25 of the old version are refused; "a third larger" is 4/3 - 1.
- `weak-signal-daily-edge`: $\sqrt{1{,}225} = 35$, standard error 0.04%, t = 7/4 two ways; `no-root` 0.05 and `annual-sharpe` 0.7937 (stored 0.79) land on their ids; 4,900 days is the first length with t = 3.5.
- `ht-pvalue-z-two-and-a-half`: one tail 0.02018 by three routes, two-sided 0.0404; one key; 0.020, 0.025 (the tail beyond 1.96) and 0.050 each match their `why`; "significant at 5% but not at 1%" holds; no option is named by place.
- `sample-size-for-signal-sharpe-years`: $T = 900/121 = 7.438$ by algebra and by bisection; a simulation of daily returns at Sharpe 1.1 gives a mean t of 2.99 over that record; band 0.05 takes 7.4 and 7.44 and refuses 7.3 and 7.5; slips 2.727 and 3.306 land on their ids.
- `op-payoff-short-strangle-loss`: -3 two ways; `3`, `£3` and `3.00` land on `unsigned`; `-3`, `-£3` and `£-3` are accepted.
- `pf-types-round-half-even`: the line returns -12 (terms -1, -2, -4, -5) by running it and by `decimal`; the three slips are -10, -11 and -13 as stored; `accept`, `correct`, `generic` and `explain` agree with the four terms. Finding 1 is about two lines only.
- `es-mle-waits-between-trades`: six gaps listed, total 30, estimate 0.2 by the closed form and by a grid on the log-likelihood.
- Six swapped tests: each `expect` agrees with my solution and with a brute route (closed form for the 3,000-call sum, a per-symbol sum for the 20,000 symbols); the changed test is exactly the one the pass lists in each task; each model passes, each starter fails, each `how` count matches. All 111 recorded candidates of the two earlier readers still fail, the seven that passed before the pass included, except `index-method`, which the page stops. Prose sizes match the tests (50,000 ticks; 100,000 trades in 20,000 symbols).

Fix pass b, holes:
- `p-lawn-pond` part 3: 134.37 ÷ 12 = 11.1975, 12 tins by ceiling and by count-up; `rounded-down` 11 and `whole-courtyard` 13 land on their ids; 11.20, 132 and 144 are as printed; the removed `circumference-carried` slip does give the key, so removing it was right.
- `e-odds-update`: 0.16722 by the odds and by the logistic of the log-odds; `prob-times` 0.1205, `odds-as-prob` 0.2008, `sign` 0.6888 and `decimal` land on their ids; 0.667, 0.301, 0.201 and 16.7 are as printed; no word or figure of the leverage version is left.
- `e-diameter-ends`: centre (1, 6); $r^2 = 289$ from $C$ to $A$ and from half of $AB$ (34); both ends satisfy the key; the `accept` form expands from the key; 13 typed forms of the right circle are accepted, the three slips land on their ids, the old 169 and -132 forms are refused, an expression with no `=` is refused.
- `p-windy-ride` part 4: the ratio is $9v/(16(v - 2))$ by sympy; `72`, `9\cdot8` and `9\times 8` land on the new `number` line; part 3 does give $v = 8$ and part 5 does put it in.
- `p-disk-failures` part 5: 200 is the smallest $n$ with $(n - 2)/n \ge 0.99$, by search and by algebra; 198 and 0.95 land on their ids. `p-hall-tiles` part 2: 120 has 16 factors; the generic line names 120.
- `two-by-two`, every kept table: `key`, `obs` and `g` agree with a cell-by-cell second route; the key to 2 places is accepted; working with expected counts kept to 2 places is accepted (worst miss 0.033 against a band of 0.05), so the prompt's promise holds; the solution's printed figures are accepted (worst miss 0.013); each of the four slips to 2 places is refused and gets its own line, never another's.
- `poisson-ratio-test`, every kept draw: key and `score` agree with a second route (twice the gap between the two log-likelihoods); a logarithm kept to 4 places is accepted (worst miss 0.031), so the reworded prompt's promise holds; each of the three slips is refused and gets its own line.
- `wilks-df`: the prompt gives `p` and `p - r` free, and the answer `r` is their difference; `r < p` keeps at least one free.

Fix pass c, drills ci packs 5 to 8:
- `ci-loop-cables` tests[12]: `[2]` by the model, by my group-label solution and by a search per cable; inputs inside the constraints; `how` says 13; planted[0] fails tests 12 and 13 (1-based), all three planted solutions fail, all five first-reader candidates fail in all three states.
- `ci-drop-point-routes` tests[14]: 930705120 by the model and by my exact whole-number count taken from the end cell; 18 by 18, inside the constraints, 35 calls deep at most for a recursion; `how` says 15; `drop_mod_of_difference_missing`, the delta reader's `DROP` and the new planted[3] passed before the pass and fail test 15 now; the two right recursive solutions of the first reader still pass.
- `ci-first-fit-slot` tests[7]: `[20, [[0, 6], [10, 12], [20, 24]]]` by the model, by my bisect solution and by a minute-by-minute brute force; inputs sorted, disjoint and inside the constraints; `how` says 15. Across the three states no candidate that failed earlier passes now: `fit_past_end_forgets_start` and the delta reader's `FIT` (passed before the pass) fail test 8; `fit_gap_size_only` and `fit_gap_must_begin_after_start` (passed in the original file) still fail tests 15 and 14; all five planted solutions fail; the two first-reader solutions found right still pass.
- Model, my solution and a brute force agree on 3,000 random small inputs for each of the three drills.

## Counts

| Fix pass | wrong | unclear | minor |
| --- | --- | --- | --- |
| a. bank part 2 | 0 | 1 | 2 |
| b. holes | 0 | 0 | 1 |
| c. drills ci 5 to 8 | 0 | 0 | 0 |

## Not checked

- Timing in the page itself: the 5 s limit was checked with Pyodide 0.27.7 under node only (the delta reader's `pyo_time.mjs`), and drills natively with a 10 s limit for a whole run.
- The four `bank-2-s<n>-numbers.py` author scripts and the four `drills-ci-<n>-check.py` scripts were not rerun (`s3` takes about seven minutes, over the two-minute limit of this read).
- Validator warnings were not listed by file; only the totals were read (0 errors).
- Freshness of the four re-authored statistics items and of the two re-authored exam items against the courses was not re-read.

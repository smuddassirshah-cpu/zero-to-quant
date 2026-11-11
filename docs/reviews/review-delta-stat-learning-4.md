# Delta read: fix pass of stat-learning level 4

Scope: only what the fix pass changed (commits "Fix pass: stat-learning L4", 4e94e04 to 06ca8d6; `git diff 4e94e04^ 06ca8d6 -- app/content`), read at 4a436a3. Seven files in `app/content/courses/stat-learning/`: `l15-widest-street` (screens 0, 1, 3, 4), `l16-groups-nobody-labelled` (screens 1, 2, 4, 5, 7, 10, summary, quiz q1), `l17-a-small-network` (screens 0, 4, 8, 9, quiz q2), `l18-bending-the-line` (screens 3, 10, quiz q2, q3), `l19-which-learner` (screens 0 to 5, 7, 8, summary), `review-4` (`r-few-rows`), `homework-4` (`h-kmeans`, new `h-pick-learner`). Record: `docs/reviews/review-stat-learning-4.md`, 34 findings and "Fix pass".

Method. Each changed screen and item was read whole as it now stands. `recompute.py` recomputes every changed number by two routes and puts a run behind each reworded sentence; `code_tests.py` runs the six new hidden tests and `h-kmeans` under the engine's comparison rule; both files run unchanged in CPython (scratchpad venv, scikit-learn 1.6.1) and, through `pyo.mjs`, in the local Pyodide 0.27.7 build, and the two outputs were compared line by line. `grade.mjs` puts typed strings through the engine's numeric grader. `few_rows.py` tests `r-few-rows` at its own sizes. The diff showed me the key of `h-pick-learner` (1.21) before I had solved it; I then solved it from the prose by two routes and tried six other readings.

Scripts: `docs/reviews/delta-stat-learning-4-scripts/`, run from the repo root: `<venv python> recompute.py`; `<venv python> code_tests.py`; `node pyo.mjs <pkgs> recompute.py` and `node pyo.mjs <pkgs> code_tests.py`; `node grade.mjs`; `<venv python> few_rows.py`.

Tags: `wrong` = a wrong number, a false statement or wrong grading; `unclear` = teaching that misleads, or is true only of the lesson's data; `minor` = wording, coverage, freshness, test strength.

## Tool results

- `recompute.py`: CPython 55 of 55 checks, Pyodide 50 of 50 (the long searches are shortened there); 5 FINDING rows (findings 2, 3, 5, 7 and 9 below). Every changed stored value is right by both routes.
- `code_tests.py`: 0 BAD rows in CPython and in Pyodide. The two outputs differ only where a network score differs (below) and for a solution with no `random_state`.
- `grade.mjs`: 66 checks, 0 failures; 4 FINDING rows (findings 5 and 11). Every answer grades correct, every `wrong` entry lands on its own id and has its line, the old values 12 and "11, 29" no longer fire.
- Author scripts: `stat-learning-L4-numbers.py` exit 0, 457 of 457; `stat-learning-4-perf-numbers.py` exit 0, 0 failures, ten planted slips each failing at least one test.
- First reader's `run-code.py`: exit 0; the only unexpected passes left are the l17 scaler on all rows and the l18 scaler.
- Validator: 0 errors; 51 warnings on the level's files (17 long sentences, 34 hint or canvas advisories), the count the fix pass reports. `manifest.json` unchanged.
- Voice scan (`voice-scan.py 35`): 0 and 0. `fresh-check --file` on `homework-4`: 0 hits. `perf-reports.mjs`: 0 missing parts.
- Playthrough with `--local-cdn`, one at a time: l15 to l19, `review-4`, `homework-4`, with and without `--mobile`: 14 runs, all "All passed."; `homework-4` shows "1 performance starter fail".
- Not done: no screenshot was read for `showZero` (finding 30); I read `bars.js` line 221 instead, where a 0 is printed only if `showZero !== false`.

## The 34 findings

Fixed as recorded, checked here: 1 to 28, 30 to 33. Deferred as the first read allows: 29 (the line is in `docs/reports/stat-learning-4.md`). Open: 34, see "Rulings asked for". Partly fixed: 13 (finding 1 below: the same phrase survives on two screens the pass edited), 20 (finding 3), 21 (finding 11), 27 (finding 9).

## Reworded sentences (reader's source or run)

- $C$ against budget (l15 s4): true. ISLP 9.2.2, equation 9.15, has $\sum \epsilon_i \le C$, "a budget", and the margin widens as $C$ grows; ISLP lab 9.6.1 says of scikit-learn's `C` that a small cost gives wide margins. Run: widths 2.78, 1.07, 0.80 at $C$ = 0.01, 1, 100, by `coef_` and by `dual_coef_ @ support_vectors_`.
- "anywhere beyond their own edge" (l15 s1): true as a rule. 300 random moves of the three other loans beyond their edges move the hard-margin fit by at most 0.0008 (solver rounding); a default moved beyond the repaid edge moves it.
- k-means starts (l16 s5): the fixer is right, the first reader was not. `KMeans(3, n_init=10, random_state=0)` and `n_init=50` both stop at 842.33 (purity 0.75); `n_init=200` reaches 842.15 (purity 44/60). My own loop from 3,000 random starts has 842.15 as its lowest stop (46 starts), 842.33 as a local stop (665), and no single share moved to another group lowers 842.15. So "more starts", not "fifty starts". See finding 7 for the seed.
- "The best inertia never rises" (l16): true (ISLP 12.4.1). Exhaustive search over every grouping of the six shares: 790, 64, 10, 4, 2, 0.
- "Only heights mean anything" (l16 s7): ISLP 12.4.2, on reading a dendrogram: closeness is read from the height of the fusion, not from position along the axis. See finding 12.
- Pyodide against CPython (l17 s9): the table is Pyodide's exactly (175/167, 181/150, 195/149 rows of 300). CPython gives test rows 170, 146, 149: moves of 3, 4 and 0, so "up to four rows" is true of this table and this pair. Not true as a bound: finding 2.
- l17 s9 key, "two rows in 300 above the 0.55 base rate": 167 against 165. True of the table shown.
- Accuracy has no exact split (l19 s5): true. ISLP 2.2.2, equation 2.7, is for squared error; ISLP 2.2.3 says the trade-off carries over to classification "with only some modifications" and gives no sum. Level 1 holds l3, so "Level 1 split a squared error" is right.
- Fresh estimators (l19 s7): true. scikit-learn's glossary entry for `fit`: a second call discards the earlier fit unless `warm_start` is set. Run: a reused pipeline gives the same 20 deterministic cells; a street model kept and then fitted to the rings is the same object and scores 0.05 on the street.
- "Few rows" as an average (l19 s3, summary): the fixer's 40 pairs rerun: means 0.9182, 0.8588, 0.9065, 0.9090, 0.9283; nearest neighbours strictly last in 35, below logistic regression in 40. My own 40 pairs (seeds 5000 on): 0.9215, 0.8653, 0.9118, 0.9066, 0.9323; last in 35 again. The first 10 pairs give the same 50 scores in Pyodide and CPython. As a rule: ISLP 3.5, the curse of dimensionality for nearest neighbours.
- Ridge on a spline (l18 q3): true. 0.8868 by pipeline and by the normal equations. Penalty 1 on 40 knots: the curve's sd falls from 16.4 to 13.3, its squared second differences halve, and it reads 12.3 and 61.0 at 1% and 40% against the 5-knot fit's 9.8 and 62.5. Penalty $10^6$: a constant 46.50, the mean of $y$; the same limit on a hinge basis. Penalty 0.001: at most 0.33 bp on a curve from 4 to 74 bp (the fix record says 0.06; that depends on the grid, and the content states neither). Smoothing spline, ISLP 7.5.1: with a curvature penalty of $10^8$ SciPy's `make_smoothing_spline` is the least-squares line to 0.05 bp.
- `r-few-rows` (review): the softened key holds. At the item's sizes (80 rows, 25 features, 40 seed pairs) logistic regression averages 0.927, the 64-unit network 0.920, the 10-knot additive model 0.900 and nearest neighbours 0.863.

## New hidden tests

Model solution passes, starter fails every test, the wrong solution each test was written for fails that test, my own solutions pass. Same rows in both runtimes.

| test | wrong solution it catches | reader's correct solutions that pass |
|---|---|---|
| l16 s4 `tests[9]` | Manhattan assignment: fails only this test | loops with `np.linalg.norm` (plain length, not squared) |
| l17 s8 `tests[5]` | `random_state=0` whatever the seed: fails only this test | a closure with `accuracy_score` and a list for the sizes; a positional width with a dict of scores |
| l17 s8 `tests[6]` | default `alpha`: fails only this test | as above |
| l19 s7 `tests[5]` | one model per learner, refitted: fails only this test | a comprehension with accuracy by hand; a row of models built first and fitted afterwards (2 builds) |
| l19 s8 `tests[5]` | validation on rows already fitted: fails only this test | a dict of scores with `max`; an array of scores with a stable sort |
| `h-kmeans` (reworded) | a stop straight after the last assignment fails tests 3 and 5; one more assignment after the loop and `max_iter + 1` rounds fail test 3 | a `while` loop that counts rounds; an update before the repeat test, with plain Euclidean length |

- Stability: three units on seeds 0 to 7 score 0.82, 0.9733, 0.7767, 0.7967, 0.8067, 0.7833, 0.9733, 0.7833 in both runtimes, so the two new bands hold in both: 0.9733 sits 0.017 under the top of 0.93 to 0.99 and 0.043 above its floor, and 0.7833 is 0.067 under 0.85. Default `alpha` at seed 5 scores 0.9633 in both. The two `l19` tests have no network in them.
- The `counted` helper (l19 s7): a solution that builds a model per cell in any order passes (count 2). A solution that makes one template per learner and fits a fresh `sklearn.base.clone` of it per cell has independent cells and the right table, and is refused (count 1). So is one that builds an extra model per learner to inspect it (count 3). Both depart from the starter's comment, "build each learner fresh with `learners[name]()`", and `clone` is not taught in the course, so I do not count either as a correct solution refused. See finding 8.
- `h-kmeans`: one reading. A round is defined; the labels are "of the last assignment"; `max_iter=1` therefore returns the first assignment and the centres after its update, 25.6 and 587.2. Ten tests, ten planted slips, prose, `how`, `stat-learning-4-perf.md` and `stat-learning-4-perf-numbers.py` agree.
- The two wrong solutions that still pass. l17 s8, a scaler fitted on training and test rows: passes all 7 tests in both runtimes (0.80 against 0.82 at three units). The text does not claim to catch it: `how` says the two new runs "check that your seed and penalty are used" and "The bands cannot check everything else". l18 s7, a scaler before the splines: passes; `how` lists the five cases and makes no claim about scaling. Neither lesson overstates its tests.

## `h-pick-learner`

Solved from the prose: validation 0.61, 0.61, 0.60, 0.59, 0.58, tie to the first; its test accuracy 0.59; $t = 0.03/\sqrt{0.56 \times 0.44/400} = 1.2087$, and $t^2 = 225/154$ exactly. Key 1.21 right. The four `wrong` values are right by floats: 2.4175, 1.6116, 3.6000, 2.0146. No two bands meet; each has its line. The formula is the level's own (l19 summary, l14). Fresh: `fresh-check` 0 hits, and no other item in `stat-learning`, `validation` or exam `topic-2.1` joins a validation pick to a $t$ statistic. It is the third item to use 400 test rows (`review-3` `r-hit-t`, `review-4` `r-t-edge`); the numbers differ. Findings 4, 5 and 6.

## Findings

Format: `N. file | screen or item | tag | what is wrong | fix`.

1. `l17-a-small-network.json` screens[8] `how`; `l19-which-learner.json` screens[7] `how` | unclear | Both still say "a network's score moves in the third place between runtimes", the phrase finding 13 removed from l17 s9. It is true of the rings (one row, 0.97 against 0.9733). It is not a rule: the next screen now says four rows in 300, and l19's own noise cell is 0.5367 in Pyodide and 0.5633 in CPython, eight rows. The fix pass edited both strings and kept the clause. | Both: "because a network's score differs a little between runtimes".
2. `l17-a-small-network.json` | screens[9] explain | unclear | "On another runtime the test scores move by up to four rows in 300" states one measured gap (3, 4, 0 rows, confirmed) as a bound for any runtime. The same 8-unit network on the same noise rows behind a scaler, l19's cell, moves eight rows between the same two runtimes. | "On another runtime the test scores move by a few rows in 300; the conclusion does not."
3. `l18-bending-the-line.json` | quiz[1] explain | unclear | "a **natural spline** goes further and is forced to be linear beyond its boundary knots" names no difference. The spline on this screen, with `extrapolation="linear"`, is already exactly linear beyond its boundary knots (second differences 0 from 51 to 55), and option a calls it "the linear tail". What a natural spline adds (ISLP 7.4.3) is the constraint at the boundary: no curvature there, so fewer coefficients and a steadier curve near the edges. The lesson's spline has curvature at its upper boundary. | Second sentence: "The spline's linear tail is closer to the truth, 85.13 against 74.16, by luck of shape; a **natural spline** builds that straight tail into the fit, with no curvature at its boundary knots." (33 words; the explanation stays at three sentences.)
4. `homework-4.json` | `h-pick-learner` prose | unclear | "Five learners ... are fitted to 600 training rows. Their validation accuracies, on 200 rows held out of the training rows" reads as fitted to all 600 and then scored on 200 of them. That is the leak l19 screen 8 teaches against and its new test catches. | "Five learners, listed simplest first, are each fitted to 400 of 600 training rows. Their accuracies on the other 200, the validation rows, are 0.61, 0.61, 0.60, 0.59 and 0.58."
5. `homework-4.json` | `h-pick-learner` widget.tol | minor | The band is 1.21 ± 0.005. A learner who rounds the standard error to 0.025, as `r-t-edge`'s own feedback line does, types 1.20; one who takes the standard error from the learner's own 0.59 types 1.22. Both get the generic line, which names neither. The sibling items (`r-hit-t`, `r-t-edge`, l14 screen 10) use 0.01. | `"tol": {"abs": 0.015}`: the nearest `wrong` value is 1.61.
6. `homework-4.json` | `h-pick-learner` `valscore` | minor | 2.01 is also the $t$ of the fifth learner's test accuracy, 0.61. A learner who picks the most flexible learner is told "You used the validation score, 0.61". | In the prose make the fifth test accuracy 0.57: its $t$, 0.40, meets no band, and 0.62 stays the best test score.
7. `l16-groups-nobody-labelled.json` | screens[5] prose | minor | The screen's call is `KMeans(3, n_init=10)`, with no `random_state`. With ten starts 7 of 40 seeds already reach 842.15 and show 73%, not the question's 75%; 31 stop at 842.33 and 2 at 842.96 (both 75%). The new `why`, "from 842.33 to 842.15", is the seed-0 run. | Prose: `KMeans(3, n_init=10, random_state=0)`.
8. `l19-which-learner.json` screens[7]; `l17` screens[8]; `l19` screens[8]; `l16` screens[4] | minor | Each new test is the only one its slip fails, and none has a line. A learner whose table is right but who reuses a model reads "5 of 6 tests passed. The first failure is test 6." and a row calling `counted` and `BUILDS`, names from the hidden prelude, "Expected 2, got 1". The engine takes `byKey["test-N"]` (`code.js` line 576, `player.js` line 111). | l19 s7 `"test-6": "Your table is right, but one model served more than one cell. Build a fresh one for each cell with `learners[name]()`."` l19 s8 `"test-6": "A learner that memorises its rows won your validation. Fit on `X[:-n_val]` only, then score on the last `n_val` rows."` l17 s8 `"test-6": "Seed 1 should reach 0.93 with three units. Pass `random_state=seed`."` and `"test-7": "Seed 5 should stay under 0.85 with three units. Pass `alpha=0.01`."` l16 s4 `"test-10": "Use squared distance, summed over the columns, not summed absolute gaps."`
9. `l19-which-learner.json` | screens[5] explain | minor | "Bias wins where the truth is simple or the rows are few" now sits beside screen 3's "logistic regression's lead here is this sample's". Over 80 seed pairs the table's additive model beats logistic regression on the wide row by 0.0105 ($t = 5.0$). The sentence is right as a rule (ISLP 2.2.2; `few_rows.py`: a 10-knot additive model trails by 0.027 at 80 rows), but the table's wide row is not its evidence. | "Simple learners hold up where the truth is simple or the rows are few; flexibility wins where the truth is curved and the rows are many."
10. `l16-groups-nobody-labelled.json` | screens[5] options[2].why and feedback.byKey.c | minor | "purity" appears here for the first time, before the explanation defines it; the prose says "land with their own planted group". | `why`: "...only from 842.33 to 842.15, and then 73% of shares land with their own group, not 75%." `byKey.c`: "...dominated by volatility, and the match with the planted groups falls to 73%."
11. `l18-bending-the-line.json` | screens[3] question | minor | The question still asks two things and takes one number: "3, 7" does not parse. The new `interior` entry catches the learner who types 3 alone. | "...among its 5. How many basis functions does it build? Count the interior knots first."
12. `l16-groups-nobody-labelled.json` | screens[7] explain | minor | "Only heights mean anything" overreaches: which leaves join also means something, and B1 and B2, side by side here, are close. ISLP's point is narrower. | "Read closeness from the height at which two leaves join, not from their order along the axis."
13. `l15-widest-street.json` | screens[0] prose | minor | "Three defaulted ... Logistic regression with its default penalty": two senses of "default" in one paragraph about loans. | "Logistic regression with its usual penalty would pick yet another line."

## Counts

- wrong: 0
- unclear: 4 (1, 2, 3, 4)
- minor: 9 (5 to 13)

No changed number, key, `wrong` value or test is wrong. The fixer's two departures from the first reader on numbers (7 and 27) both stand on my reruns.

## Rulings asked for

1. Finding 34 of the first read is still open: `DECISIONS.md` has no line saying that level 4's performance task proves l16's objective while the validator's verb rule matches l17's. The fix pass left it to the main session.
2. l19 screen 7, test 6: a count of factory calls refuses a solution that fits a fresh `clone` per cell. I read the starter's comment as the specification and do not call that a correct solution refused. If the main session reads it the other way, the test should count distinct fitted objects instead.

## Verdict by file

| file | verdict |
|---|---|
| `l15-widest-street.json` | Fixed. One wording note (13). |
| `l16-groups-nobody-labelled.json` | Fixed; the starts claim is right as rewritten. Three minor (7, 10, 12). |
| `l17-a-small-network.json` | Dead entry fixed, new bands stable. The runtime claim is half fixed (1, 2). |
| `l18-bending-the-line.json` | Ridge explanation right. The natural spline sentence needs its real difference (3); one minor (11). |
| `l19-which-learner.json` | The three false sentences are gone and both new tests bite. Minor (8, 9) and the shared phrase of finding 1. |
| `review-4.json` | Fixed; the key holds on a run. |
| `homework-4.json` | `h-kmeans` has one reading. `h-pick-learner` is right; its prose can be read as the leak (4), and two minor (5, 6). |

# Topic 2.1 exam: machine learning

File: `app/content/exams/topic-2.1.json` (id `topic-2.1`, 90 minutes, pass 0.7).
Generator and checks: `scratchpad/exam-2.1/` (`gen.py` builds the file from `d2.py`, `d3.py` and `d4.py`; `codeitems.py` holds the code items' preludes, starters, solutions, wrong versions and tests; `build_specs.py` writes `specs.json`; `codecheck.mjs` grades any source against a widget spec in the app's own runtime; `calc1.py`, `calc2.py`, `calc18.py`, `t14.py` to `t28.py` and `pyo_check.py` recompute the numbers; `pyo.mjs` runs a Python file in Pyodide 0.27.7 under Node; `lint.py` checks the voice rules). A scikit-learn 1.6.1 venv in the same folder gave CPython values.

Minutes: topic 2.1 has 200 hours, so `examMinutes` gives 90. Pass mark 0.7, as in the pattern exams.

## Shape

30 items, interleaving stat-learning (sl), validation (vl), ensembles (en) and fin-ml (fm), ordered by difficulty with the courses alternating inside each band.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 6 | 20% | 20% |
| 3 | 15 | 50% | 50% |
| 4 | 6 | 20% | 20% |
| 5 | 3 | 10% | 10% |

Widgets: 10 numeric, 5 code (Python), 4 choice (2 with a table canvas, 1 with a series canvas), 4 table, 3 tap-regions (grid, table rows, console lines), 2 multi, 1 order, 1 longform (10 points).

| # | id | d | skills | widget / canvas |
|---|---|---|---|---|
| 1 | e-gap-reading | 2 | sl-setup, sl-tradeoff | choice, table |
| 2 | e-gini-node | 2 | en-trees | numeric |
| 3 | e-first-touch | 2 | fm-labels | choice, series with barrier lines |
| 4 | e-walk-first-test | 2 | vl-time, vl-cv | tap-regions, grid time line |
| 5 | e-kelly-odds | 2 | fm-sizing | numeric |
| 6 | e-fit-count | 2 | vl-cv, vl-overfit | numeric |
| 7 | e-bias-var-table | 3 | sl-tradeoff | table |
| 8 | e-leak-rows | 3 | vl-leakage, vl-time | tap-regions, table rows |
| 9 | e-boost-residuals | 3 | en-boosting | table |
| 10 | e-frac-diff | 3 | fm-features | choice, table |
| 11 | e-ridge-shrink | 3 | sl-regularise | numeric |
| 12 | e-oob-overlap | 3 | en-bagging, vl-time | choice |
| 13 | e-break-even-cost | 3 | fm-eval | numeric |
| 14 | e-odds-update | 3 | sl-classify | numeric |
| 15 | e-code-gbm-stop | 3 | en-boosting, en-trees, vl-time | code |
| 16 | e-lookahead-lines | 3 | fm-features, vl-leakage | tap-regions, console |
| 17 | e-lasso-raw-units | 3 | sl-regularise, sl-linear | multi |
| 18 | e-importance-claims | 3 | en-interpret, en-bagging | multi |
| 19 | e-interaction-slope | 3 | sl-linear | numeric |
| 20 | e-rf-variance | 3 | en-bagging, en-trees | numeric |
| 21 | e-precision-recall | 3 | sl-classify | table, table |
| 22 | e-code-ridge-inter | 4 | sl-linear, sl-regularise, sl-setup | code |
| 23 | e-best-of-n | 4 | vl-overfit, fm-eval | numeric, console (research log) |
| 24 | e-code-meta-short | 4 | fm-labels | code |
| 25 | e-boost-recipe | 4 | en-boosting, fm-labels, fm-features, vl-time, fm-eval | order |
| 26 | e-code-purged-roll | 4 | vl-time, vl-leakage | code |
| 27 | e-kelly-wrong | 4 | fm-sizing, sl-classify | numeric |
| 28 | e-code-honest-report | 5 | sl-setup, sl-classify, sl-regularise, vl-cv, vl-time, vl-leakage | code |
| 29 | e-honest-t | 5 | fm-labels, fm-eval, sl-classify | table |
| 30 | e-explain-note | 5 | sl-tradeoff, sl-regularise, vl-leakage, vl-time, vl-overfit, en-boosting | longform |

Skills: all 17 of the topic are covered (the `skills` map is the union of the four course.json maps). Item counts per skill: sl-setup 3, sl-tradeoff 3, sl-linear 4, sl-regularise 5, sl-classify 5; vl-cv 4, vl-time 8, vl-leakage 5, vl-overfit 4; en-trees 4, en-bagging 4, en-boosting 5, en-interpret 1; fm-labels 5, fm-features 3, fm-sizing 3, fm-eval 5. en-interpret has one item plus the longform's boosted-model reading; the lessons teach it in one lesson (l8) and as part of l1, l4 and l12.

Exit line. "One tabular prediction problem done end to end with time-ordered cross-validation" is item 28 (time split, scaler inside the pipeline, penalty tuned by `TimeSeriesSplit`, one test score against a base rate), with item 25 (the order of an honest boosted-tree study), item 26 (purged, rolling walk-forward folds) and item 15 (early stopping on a later block). "Explain leakage, regularisation and the bias-variance trade-off without notes" is item 30, a written reply to a flawed model note (a 10-point rubric and full model answer), backed by items 1, 7, 8, 11, 16 and 17.

Quant framing: spread snapshots, a triple-barrier trade, monthly walk-forward folds, Kelly stakes, grid-search fits, noise and bias in volatility forecasts, month-end features, impact trades under boosting, fractionally differenced prices, ridge slopes on momentum, a forest on 10-day returns, trading costs and no-trade bands, loan default odds, a feature script, a lasso on raw units, importance with a ticker id, an interaction of momentum and volatility, a crash detector, a research log, a long-and-short crossover desk, a miscalibrated edge, overlapping labels, and a reply to a junior analyst's note.

Fresh against the courses. Each item is a new problem on a taught idea. For example: a 12-month `TimeSeriesSplit(4, test_size=2)` (the lessons use 1,000 rows); a depth-1 stump on six trades with a shrunk first round; the Gini of 6 defaults in 20 loans; a fractional-differencing choice at seed 17 (the lesson used seed 5); a rolling window with a purge in one splitter; a long-and-short meta-label with a 2σ target and a 1σ stop; a research log of 8 trials against the lesson's 3.

## Code items (app runtime, `codecheck.mjs`: Chromium, local CDN, Pyodide 0.27.7, scikit-learn 1.6.1)

| item | tests | solution | starter | wrong versions (each fails, first failing test) |
|---|---|---|---|---|
| e-code-gbm-stop | 5 | 5/5 | 0/5 | shuffled split (1), zero-based round (1), training MSE (1), fit on all rows (1) |
| e-code-ridge-inter | 5 | 5/5 | 0/5 | no interaction (1), scaler on all rows (1), product of z-scores (1), shuffled split (1) |
| e-code-purged-roll | 10 (2 raise) | 10/10 | 0/10 | gap = h (1), no purge (2), window ignored (3), window counted before the purge (3), no error (8) |
| e-code-meta-short | 11 | 11/11 | 0/11 | one width for both sides (3), shorts read as longs (4), time-out by final return (2), yesterday's volatility (1), strict barrier crossing (6) |
| e-code-honest-report | 7 | 7/7 | 0/7 | shuffled split (1), scaler on all rows (1), `C` chosen on the test block (3), base rate from the test block (1), ties keep the later `C` (7), shuffled folds for `C` (1) |

All 33 runs came out as expected. The same run caught three faults I then fixed: a seed whose scikit-learn value differs between CPython and Pyodide (see below), a wrong version that passed every test (a strict `>` on barriers, now caught by tests with a close exactly on a barrier), and a "ties keep the later `C`" version that no test separated (test 7 uses `C = [1e-4, 1e-5]`, which tie). Every `how` on a scikit-learn screen says the first run takes 20 to 40 seconds. The first scikit-learn load took 7 to 9 s from the local CDN in the app; a real network will be slower, so those items carry a `budget`. Longest case: `honest_report` at about 0.7 s once loaded. Tests that return floats use `isclose` with a relative tolerance of 1e-6; rounded outputs sit at 4 places.

Pyodide against CPython. Four of five seeds for `early_stop_round` matched to 4 places. The fifth (seed 8, learning rate 0.05, 200 training rows) gave 14.9285 in CPython and 14.9527 in Pyodide (a tie in a split changes one tree), so the exam uses seed 11 instead, where both give (69, 12.8732). Every expected value in the file was produced by the solution in CPython and then graded in Pyodide by `codecheck.mjs` and by the playthrough.

## Numbers computed twice

Each number was computed in CPython (NumPy 2.5.3, SciPy, scikit-learn 1.6.1) and in Pyodide 0.27.7 under Node (NumPy 2.0.2). `pyo_check.py` ran in both, and the outputs agreed except for dtype names and a last-digit difference of 1e-16.

- Item 1: polynomial fits on 24 training and 500 test points, seed 4, true curve 1 + 0.8x − 1.2x², noise sd 0.4. Training MSE 0.25, 0.13, 0.10, 0.09 and test MSE 0.32, 0.18, 0.49, 2.57 at degrees 1, 2, 6, 10, in both interpreters. Seed 4 was chosen from a search of seeds for a clean U shape.
- Item 2: Gini $1 - 0.09 - 0.49 = 0.42$ by arithmetic and by `Fraction`; the $p(1-p) = 0.21$ distractor.
- Item 3: barriers $50 \times 1.03 = 51.50$ and $50 \times 0.97 = 48.50$ by arithmetic and Python; the path first closes below the stop on day 4 (48.40) and above the upper barrier only on day 7.
- Item 4: `TimeSeriesSplit(4, test_size=2)` on 12 rows gives test rows 4 and 5 (May and June) in scikit-learn, in CPython and Pyodide, and by $12 - 4 \times 2 = 4$.
- Item 5: $0.5 - 0.5/1.5 = 0.16667$ by float and by `Fraction`; the edge $0.5 \times 1.5 - 0.5 = 0.25$.
- Item 6: $6 \times 5 + 1 = 31$.
- Item 7: $4 + 0.49 + 5.51 = 10.00$, $4 + 1.44 + 2.06 = 7.50$, $4 + 5.76 + 0.34 = 10.10$; the unsquared slip gives 7.26.
- Item 9: scikit-learn's depth-1 tree splits at 3.5 with leaf means 3 and 9 in CPython and Pyodide; shrunk predictions 1.5 and 4.5; residuals 0.5, 2.5, 1.5, 3.5, 4.5, 5.5; sum of squares 71.5; no-model sum 274 by hand and by NumPy.
- Item 10: fractional differencing (weights cut at $10^{-4}$) of the seed-17 log price, 1,500 days: variance ratio 0.263, 0.202, 0.166, 0.139, 0.049 and correlation with the level 0.95, 0.89, 0.85, 0.79, 0.04 at $d$ = 0.3, 0.4, 0.45, 0.5, 1. Same in both interpreters (the code is the l6 `ffd_weights`, `frac_diff` and `vr`).
- Item 11: `Ridge(alpha=100)` on exactly orthogonal columns with sum of squares 250 gives 0.428571 in both interpreters, and $0.6 \times 250/350$ by hand. The subtract slip is 0.6 − 100/250 = 0.2; the other slip is 0.6/101 = 0.0059.
- Item 13: $3.3/0.30 = 11$ and $3.6/0.45 = 8$ by arithmetic and Python.
- Item 14: odds $0.1/0.9 = 0.1111$, times $e^{0.9} = 2.4596$ gives 0.27329 and probability 0.21463, by float and by `Fraction` for the odds; the slips 24.6% and 27.3%.
- Item 19: $0.5 + 0.6 \times 1.5 = 1.4$.
- Item 20: $\rho\sigma^2 + (1-\rho)\sigma^2/B = 2.25 + 0.03375 = 2.28375$, and the same from the variance of the mean of 200 equicorrelated variables, $w^T \Sigma w$ with $\Sigma$ built explicitly (2.28375 both ways).
- Item 21: precision 10/40, recall 10/25, accuracy 955/1,000 and 975/1,000 by arithmetic and Python.
- Item 23: 8 distinct trials among `look` and `fit` lines (six fitted, two chart-only), 4 kept, 17 lines, 6 fitted; bars $\sqrt{2\ln N}/\sqrt 4$ = 1.0197 (N = 8), 0.8326 (4), 1.1902 (17), 0.9465 (6); left after the bar 0.1303, 0.3174, −0.0402, 0.2035.
- Item 27: full Kelly $2 \times 0.58 - 1 = 0.16$; growth at $p = 0.52$ is $-0.006511223$ in float and with 40-digit `Decimal` logarithms (−0.00651122316799). At the model's 0.58 the same stake gives +0.01286; the true Kelly stake 0.04 gives +0.00080.
- Item 29: $\sqrt{0.57 \times 0.43/1000} = 0.015656$; effective $n = 1000/10 = 100$; $\sqrt{0.2451/100} = 0.049508$; $z = 0.05/0.049508 = 1.0099$ (naive 3.1937); for $z = 2$: $0.2451/0.025^2 = 392.16$ effective, so 3,921.6 labels. Tolerance on the last cell is ±40.
- Items 15, 22, 24, 26 and 28: every expected value from the solution in CPython and checked in Pyodide through the app. Item 26's folds also equal scikit-learn's `TimeSeriesSplit(n_splits, test_size, gap=h-1, max_train_size=window)` for nine parameter sets, and `ValueError` where scikit-learn raises. Item 24's 971 labels and sum 329 for the seeded series (seed 21, sides flipping every 7 days) match the lesson's `rolling_vol` and barrier convention; hand-made cases were traced by hand.

Items 8, 12, 16, 17, 18, 25 and 30 carry no stated computation; their keys follow the lessons' rules (known-at dates, out-of-bag against overlapping labels, `groupby` windows, units under a penalty, importance methods, the purge-before-tune order).

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors overall, no message for this file. The manifest lists `exams/topic-2.1.json`.
- Voice lint (`lint.py`): no `!`, no em or en dash, no American spelling from a list, every sentence under 20 words and every explanation at most three sentences in the prompts, options, feedback and rubric. Three sentences in the model answer sit at 20 or 21 words once a bold label is counted.
- `playthrough.mjs --exam topic-2.1 --local-cdn <pkgs>`: 30 of 30, passed, desktop and `--mobile` (15 to 53 s).
- Screenshots reviewed (`scratchpad/exam-2.1/shots`, `shots2`). Fixes made after looking: the feature names in item 8 wrapped mid-word, so they are shorter (`surprise`, `in_index`); item 16's and item 23's console lines were cut at 390 px, so they now wrap; the 12-month grid is no longer `compact`; item 30's quoted note printed a literal `>`, so it is italic; every code docstring is wrapped to 50 characters so the starter shows whole in the editor.

## Engine notes (also in `docs/BACKLOG-INBOX.md`)

- A Markdown blockquote prints `>` literally in a longform prompt.
- A 12-column one-row `grid` is tiny on a phone.
- scikit-learn values can drift between CPython and Pyodide on a tie (the seed-8 case above).
- Table cells' own `wrong[]` ids still cannot be `byKey` keys.
- The exam `--why` result screenshot is 30,000 px tall and cannot be read as an image.

## Time

The paper has 30 items, 5 code items and a longform. My estimate is 85 to 105 minutes for a slow learner and about 60 for a fast one, so 90 minutes from `examMinutes` is tight but fair. The first scikit-learn load (20 to 40 s) is paid once, on item 15, which is the first code item.

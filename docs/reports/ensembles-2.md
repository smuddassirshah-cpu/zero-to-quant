# Report: ensembles level 2 (Averaging trees)

## Files written

All in `app/content/courses/ensembles/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l5-bagging.json` | 12 screens, 4 quiz | `bootstrap_indices` + `fraction_unique` (exact), `bagged_predict` (stand-in models and real bootstrap trees), `bagging_test_acc` (`BaggingClassifier`) | en-bagging, en-trees |
| `l6-random-forest.json` | 11 screens, 4 quiz | `average_variance`, `rf_test_acc_by_m`, `rf_vote_fraction` | en-bagging |
| `l7-out-of-bag.json` | 11 screens, 4 quiz | `oob_mask` (exact, own sampler), `oob_error_by_hand` (depth-3 trees on own bootstrap indices), `rf_oob_vs_cv` | en-bagging |
| `l8-which-features.json` | 11 screens, 4 quiz | `permutation_importance_by_hand`, `impurity_importance`, `importance_rank_change` (exact) | en-interpret, en-bagging |
| `review-2.json` | 8 items, difficulty 2 to 4, two per lesson | | |
| `homework-2.json` | 8 items, difficulty 3 to 5 (three at 5) | `scratch_forest` (5: own sampler, depth-2 trees, OOB accuracy, permutation importance per feature, returns `(oob_acc, top_feature)`), `honest_forest` (5: issue-order split, m and depth chosen by OOB on train, test accuracy against a logistic baseline) | |

The homework also has an `order` item (deriving $B^* = (1 - \rho)/\rho$ from the correlated-variance formula), numeric items (rows with no OOB tree at B = 10; trees needed to come within 5% of the floor, 162), two choice items (training-set permutation; bagged stumps) and a `longform` item (a colleague's forest: 2,000 trees, `max_features=None`, OOB on 5-day labels, impurity importance read as causal) with a 10-point rubric and a full model answer.

Lesson shapes. l5: two depth-2 bootstrap trees that disagree on one loan (a `pair` of `tree` canvases), test error against B on `series` with a slider, B = 1 (one bootstrap tree, 0.2965 against the plain tree's 0.2595), a `boxes` resample of 10 loans where the learner taps the loans never drawn, the 63.2% argument as an `order` derive, three code screens, bagged stumps against deep trees (`bars`), trap, the $\sigma^2/B$ generalise, fifty analysts as transfer. l6: the bagged trees' root splits (all leverage) beside a forest's, the floor $\rho\sigma^2$ on a `plane` with a $\rho$ slider, the derivation of $\rho\sigma^2 + (1 - \rho)\sigma^2/B$ as an `order` derive, measured $\rho$ and $\sigma^2$, the 2-of-8 candidate chance (0.25, and 25 of 100 roots did use leverage), error against m, the vote fraction as an uncalibrated probability (trap), a 30-feature credit book as transfer. l7: tap the out-of-bag cells of a 6-loan, 4-tree table, a `table` widget for the OOB predictions and error (2/6), OOB and test error against B, rows with no OOB tree, OOB against 5-fold CV (`bars`), OOB on 10-day labels (trap), the OOB recipe as an `order` derive, a desk tuning by OOB and still walking forward as transfer. l8: impurity importance from a tree's Gini drops, impurity against permutation importance as a stacked `pair` of `bars` (tap loan_id), permutation importance by hand, the correlated pair and its ablation, permuting on training data (trap), partial dependence on a `plane`, the formula and the constant column, a research note with a ticker id on top as transfer.

Traps: more trees overfit (l5; bagged stumps as a ladder), the vote share as a calibrated probability (l6; m = p is bagging in the quiz), OOB on overlapping time-ordered labels (l7; too few trees on screen and in the quiz), permutation on the training set (l8; impurity importance read as predictive value on the explore screen and in the transfer). Edge cases: B = 1 and identical trees (l5), m = 1 and p = 2 (l6), rows in every bootstrap and B large enough to cover every row (l7), a constant column with zero importance under both methods and an interaction-only feature (l8).

`random_state=0` is fixed everywhere. Every `how` on a scikit-learn screen says the first load takes 10 to 30 seconds. Links by name: *Resampling your own data* (estimation), *Averages settle down* (limits-thm), *Probabilities you can trust* (stat-learning l13), *Why shuffling a time series lies* and *Purging and embargo* (validation).

## Validator

`node app/tools/validate.mjs`: 0 errors overall, and no warnings on any level 2 file.

## Playthrough

`node app/tools/playthrough.mjs --lesson ensembles/l5-bagging --lesson ensembles/l6-random-forest --lesson ensembles/l7-out-of-bag --lesson ensembles/l8-which-features --set ensembles/review-2 --set ensembles/homework-2 --local-cdn <scratchpad>/pkgs --shots ... --mobile`, no console errors:

- l5-bagging: ok, 16 checks, quiz 4/4
- l6-random-forest: ok, 15 checks, quiz 4/4
- l7-out-of-bag: ok, 15 checks, quiz 4/4
- l8-which-features: ok, 15 checks, quiz 4/4
- review-2: ok, 8 of 8 recorded
- homework-2: ok, 8 of 8 marked right, 37 of 37 marks

I read the screenshots at 1280 and 390 px wide and fixed what they showed: the boxes cards were tiny and filled bottom-up, a trap marker label overlapped the series end label, the partial dependence y axis sat at x = 0, and the l8 tree's root pill was clipped on a phone. After the fixes, l5 and l8 were played again and passed.

## Numbers

Every code expectation was computed in CPython (scikit-learn 1.6.1, NumPy 2.1, in a scratchpad venv) and again by running each widget's solution against its tests in Pyodide 0.27.7 under node. All tests pass in both. Canvas numbers (error curves, root splits, calibration bins, importances, ablation, partial dependence) come from the CPython runs of the same generators; the Pyodide reruns of the code tests agree with CPython digit for digit. The tree correlations $\rho$ (0.11 bagged, 0.04 at m = 2) and variances come from a simulation: 200 fresh books, two trees per book, on 300 fixed query loans.

Longest test case in Pyodide: 3.0 s (`permutation_importance_by_hand` against scikit-learn with 15 repeats, including the fit in `setup`); the next longest are 1.8 s. Heavy screens carry a `budget` of 10 to 20 s.

## Dataset generators (all `np.random.default_rng(seed)`, defined in the code preludes)

- `make_loans(seed, n=400)`: 8 standard normal z-score features (leverage, cover, margin, vol, short, drawdown, size, age); default with probability $\text{logistic}(-0.3 + 2.5\,\text{lev} + 0.7(-\text{cover} - \text{margin} + \text{vol} + \text{short} + \text{drawdown}))$; size and age carry no signal. Books used: 1 (l5), 9 (l6, l7; chosen because its error-against-m curve has the typical shape: best m = 2 beats bagging by 1.6 points, against a 0.7-point average over 12 books, which the lesson states), 2 (2,000-loan test set), 3 to 8 for tests.
- `make_book(seed, n=400)` (l8, homework): leverage, cover and cover_ttm (two noisy measures of one cover, correlation 0.92), secured (binary, small effect), loan_id (uniform, unique per loan, noise), odd_day (binary noise), currency (constant 1); default logit $-0.3 + 1.8\,\text{lev} - 1.2\,\text{cov} - 0.5\,\text{secured}$.
- `make_days(seed, n=500)` (l7 trap; the numbers are on screen, it is not in a widget): iid daily returns N(0.0003, 0.01); features are the 5, 20 and 60-day mean returns and 20-day vol; label is the sign of the next 10 days' return. Book 8: OOB 0.767 against an expanding walk-forward 0.495; label autocorrelation 0.73.

## Proposed change to course.json

None.

## Notes for other levels

- scikit-learn 1.6.1 does not put NaN in `oob_decision_function_` for rows with no OOB tree. It warns "Some inputs do not have OOB scores", fills those rows with zeros and scores them as class 0. l7 teaches that behaviour rather than NaN (36 of 400 rows at B = 5).
- `RandomForestRegressor` defaults to `max_features=1.0` (bagging), not p/3; review-2 has an item on it. The l6 summary gives √p and p/3 as the usual choices.
- A forest's inner trees predict encoded class indices, not labels, so `tree.predict` on a single-class book returns 0 for label 1. I removed that test from `rf_vote_fraction`. Level 3 may meet the same thing with boosted trees' staged outputs.
- On these books, logistic regression beats the forest (the true log-odds are linear). `honest_forest` in the homework makes that the point.

## Engine or canvas limitations

See `docs/BACKLOG-INBOX.md`, "Raised later (ensembles level 2)": four bullets (plane decision-region map, tree node annotations, series numeric x, per-case `tol` in the code widget).

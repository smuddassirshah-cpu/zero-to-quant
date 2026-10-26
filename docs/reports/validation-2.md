# Report: validation level 2 (Time)

## Files written

All in `app/content/courses/validation/`. Build scripts (the source of each JSON file) and every generator are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/validation-2/build/`.

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l5-shuffling-lies.json` | 11 screens, 4 quiz | `autocorr`, `shuffled_vs_ordered`, `future_in_train` | vl-time, vl-cv, vl-leakage |
| `l6-walking-forward.json` | 11 screens, 4 quiz | `walk_forward_indices`, `walk_forward_mse`, `rolling_vs_expanding` | vl-time, vl-cv |
| `l7-purging.json` | 11 screens, 4 quiz | `forward_label`, `purged_train_idx`, `purged_cv_mse` | vl-time, vl-leakage, vl-cv |
| `l8-regime-shift.json` | 12 screens, 4 quiz | `fold_scores`, `coef_by_fold`, `first_bad_fold` | vl-time, vl-cv, vl-overfit |
| `review-2.json` | 8 items, difficulty 2 to 4, every lesson | | |
| `homework-2.json` | 8 items, difficulty 3 to 5 (two at 5) | `purged_kfold_splits` (4), `honest_walk_forward` (5) | |

Homework also has a `table` item (TimeSeriesSplit boundaries with `test_size` and `gap`), two numeric items, a choice item, an `order` item (the steps of purged walk-forward validation, label and features interchangeable) and a `longform` item (a colleague's note: boosted trees, moving-average features, 20-day labels, shuffled `KFold`, mean fold R² 0.18 and hit rate 64%, no base rate) with a 10-point rubric and a full model answer. López de Prado's book is named once in l7 (generalise screen) and once in the homework.

Canvases: grid as a day time line (shuffled fold numbers; a fold slider whose `derive` reshades the test fold and counts sandwiched days; blocked folds; six `TimeSeriesSplit` blocks with fold and expanding/rolling sliders), series (the 1,000-day volatility path with the last 200 days shaded; rolling against expanding fold MSEs with a rule-change marker; block slopes crossing zero, tap the first negative), bars (shuffled against ordered MSE; per-fold MSE, tap the least trustworthy; unequal calendar folds; purged against unpurged; fold hit rates against a base-rate line, tap the break; ten folds for the alarm rule), plane (the overlap picture: a dot per row, a bar per label window, the test labels' days shaded; tap the leaking rows before and after a block), number-line (train, gap and test of one fold), table widget.

## Validator

`node app/tools/validate.mjs`: 0 errors in my files (the full run showed 7 errors for a few minutes from another agent's half-written `random-vars/course.json`; the final run is 0 errors). Level 2 warnings are only "a ladder screen usually reuses the previous canvas kind", where a ladder moves between a chart and a code or time-line canvas.

## Playthrough

`node app/tools/playthrough.mjs --local-cdn .../scratchpad/pkgs` (Pyodide 0.27.7, scikit-learn 1.6.1), final run after the last edit, with `--mobile`:

| File | Result |
|---|---|
| l5 | 15 checks, quiz 4/4 |
| l6 | 15 checks, quiz 4/4 |
| l7 | 15 checks, quiz 4/4 |
| l8 | 16 checks, quiz 4/4 |
| review-2 | 8 of 8 recorded |
| homework-2 | 8 of 8 right, 37 of 37 marks |

Screenshots (1280 and 390 px, plus Why sheets from an earlier `--why` run) are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/validation-2/shots`. Fixed after looking: an l6 explore caption that read "test days 668 to 668" (operator precedence in a derive template), number-line intervals stacked off the axis, label bars touching the shaded band in the l7 overlap picture, an l7 edge-case screen whose bars did not match its caption. Sliders were also driven by a probe script (`probe.mjs`) to check the derived shading at other fold values. Every sentence in the six files was then cut to 20 words or fewer.

## Numbers: computed twice

- Every code test's expected value came from running the widget's solution in CPython 3.13 with scikit-learn 1.6.1 (installed into the scratchpad) and NumPy 2.5; the playthrough then ran every solution against every test in Pyodide 0.27.7 (NumPy 2.0.2, scikit-learn 1.6.1) in the browser, all passing at rel 1e-9.
- Every number stated in prose, captions, charts and options (31 groups in `facts.json`, plus the neighbour statistics, the full-sample slope and the tiny-window MSE) was recomputed in Pyodide under node (`pyrun.mjs`, `pyo_facts.py`): identical to every place shown. Arithmetic items (pooled MSEs, standard errors, row counts, z-scores) were done by hand and in Python.
- Pure-Python widgets (`future_in_train`, `walk_forward_indices`, `purged_train_idx`, `first_bad_fold`, `purged_kfold_splits`) are tested against independent references: `TimeSeriesSplit` and `KFold` output, and set arithmetic.

## Dataset generators (seeded; in hidden preludes)

- `make_vol(seed=7, n=1000, h=1, phi=0.98)` (l5, l7): a share's daily volatility in % a year, `v = 20 + 5 m + N(0, 1)`, `m` AR(1) with φ = 0.98 and innovation sd 0.2 (unit variance). Features: 5-, 20- and 60-day averages up to day t; label: mean of `v` over t+1 to t+h. 1,000 rows from a fixed 1,100-day path, so every h shares the same series. Lag-1 autocorrelation 0.952.
  - l5 gap (5-neighbour regressor): shuffled 5-fold CV MSE 3.3135 against 7.2578 on the last 200 days, 2.19 times; across 16 seeds 1.2 to 3.4 times, never below 1. In shuffled CV the nearest training row is the day before or after for 69% of test days; in the ordered split a median 272 days away (the last 200 days also average 22.4% against 15.2%). With φ = 0 the gap vanishes (2.5595 against 2.6159). Ridge: 3.2057 against 3.4977. Unshuffled `KFold`: mean 7.1022. Direction classifier: 58.1% shuffled, 52.5% ordered, base rate 51.0%.
  - l7 gap (5-neighbour regressor, 50 blocked folds of 20 rows, h = 5): 5.8928 without purge, 7.0581 purged, 7.0351 purged with embargo 5, a 19.4% rise; h = 20: 10.3097 against 14.467 (40%); h = 1: identical 4.9685. Ridge barely moves (3.36 against 3.3755).
- `make_signals(seed=0, n=1500, p=20, brk=1000)` (l6): tomorrow's volume surprise from 20 standard-normal signals, unit-norm coefficients, half of them flipping sign at day 1,000, noise sd 1. First 1,000 days, `TimeSeriesSplit(5)`: fold MSEs 1.42, 1.08, 1.00, 0.89, 0.93 (fold 1 trains on 170 rows). All 1,500 days, `TimeSeriesSplit(10)`: joined MSE expanding 1.7351, rolling 250 1.3935, rolling 100 1.571, rolling 500 1.4928, rolling 15 3.2993; refit once 2.2447. Rolling 250 wins 3 of 10 folds and the joined score; with no break expanding wins.
- `make_flip(seed=6, n=1500, brk=1000, b=0.25, drift=0.03)` (l8): signal `x ~ N(0, 1)`, next-day return `r = 0.03 + β x + N(0, 1)`, β = +0.25 before day 1,000 and −0.25 after. Logistic walk-forward, 5 folds: 0.616, 0.6, 0.564, 0.452, 0.424 against a base rate of 0.506; mean 0.5312 hides the break. 150-day block slopes cross zero between blocks 7 and 8; the full-history fit stays at +0.15.
- `make_hw(seed=0, n=1200, h=5)` (homework): daily returns with an AR(1) drift (φ = 0.99, sd 0.15) plus N(0, 1) noise; 5- and 20-day average-return features; 5-day forward-return label. Honest walk-forward (10 splits, gap 9): hit rate 54.9% against a base rate of 59.1%, MSE 5.5583.

The leak sizes are honest rather than tuned to look dramatic: in blocked folds the purge matters only near block edges, so l7 uses monthly blocks and says the leak grows as h nears the block length. A flexible model (nearest neighbours, which stat-learning l4 taught) is used in l5 and l7 because ridge cannot copy neighbours; both lessons show the small ridge gap as a quiz item.

## course.json

No change needed. l8 also tags `vl-overfit` (the stopped-working against never-worked screen and quiz lean on selection); this is a course skill, so no proposal.

## Engine and canvas limitations

Five bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (validation level 2):".

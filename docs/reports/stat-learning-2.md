# Report: stat-learning level 2 (Linear models)

## Files written

All in `app/content/courses/stat-learning/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l5-linear-as-learner.json` | 10 screens, 4 quiz | `fit_predict_mse`, `baseline_mse`, `normal_eq_coef` | sl-linear, sl-tradeoff |
| `l6-making-features.json` | 11 screens, 4 quiz | `add_interactions`, `poly_test_mse`, `one_hot` | sl-linear |
| `l7-shrinking.json` | 11 screens, 4 quiz | `ridge_coef`, `best_alpha`, `ridge_path` (transfer, 50-factor model) | sl-regularise, sl-tradeoff |
| `l8-setting-to-zero.json` | 11 screens, 3 quiz | `soft_threshold`, `lasso_support`, `first_to_zero` | sl-regularise |
| `l9-scale-first.json` | 11 screens, 3 quiz | `standardise_train_test`, `scaled_lasso_support`, `pipeline_test_mse` | sl-regularise |
| `review-2.json` | 9 items, difficulty 2 to 4, every lesson | | |
| `homework-2.json` | 8 items, difficulty 3 to 5 (two at 5) | `test_r2` (3), `count_survivors` (4), `end_to_end` (5) | |

Homework also has an `order` item (the leak-free workflow), two numeric items, one choice item and a `longform` item (reviewing a colleague's 60-feature model: scaled on all rows, random split, λ chosen on test, R² against the test mean, a forecast-month volume feature), with a 10-point rubric and a full model answer.

Canvases used: series (train and test MSE against features used, with a slider-driven marker pair; test MSE against polynomial degree), plane (interaction slopes with a slider; one-feature ridge line with a λ slider, slope `Σxy/(Σx² + λ)` in `derive`; ridge and lasso coefficient paths with a slider and a derived vertical line; expected test MSE against λ with a draggable point on the curve; error ellipses against the lasso diamond and the ridge circle, tap the touching corner), bars (signed lasso coefficients following an α slider; a stacked pair of raw against standardised lasso effects, tap the one that changed most), table (feature lists, tap the leaking row; fill-in tables), console, matrix.

## Validator

`node app/tools/validate.mjs`: 0 errors. Level 2 files carry only "a ladder screen usually reuses the previous canvas kind" warnings (l5 screen 4, l7 screens 5 and 6, l8 screen 4), where a ladder moves to a code screen on a different canvas.

## Playthrough

`node app/tools/playthrough.mjs` passed every lesson and both sets:

| File | Result |
|---|---|
| l5 | 14 checks, quiz 4/4 |
| l6 | 15 checks, quiz 4/4 |
| l7 | 15 checks, quiz 4/4 |
| l8 | 14 checks, quiz 3/3 |
| l9 | 14 checks, quiz 3/3 |
| review-2 | 9 of 9 recorded |
| homework-2 | 8 of 8 right, 36 of 36 marks |

Run with `--local-cdn .../scratchpad/pkgs` (Pyodide 0.27.7, scikit-learn 1.6.1). Screenshots of every screen are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/stat-learning-2/shots` and `shots2`; I looked at all lesson screens and fixed overlapping curve labels (l6 screen 1, l7 screens 1, 2 and 4), signed paths running over the x-axis ticks (l7, l8: now plotted as |β̂_j|), and an unreadable side-by-side bar pair (l9: stacked).

## Numbers: computed twice

- Every code test's expected value was computed in CPython (NumPy 2.5: closed-form OLS and ridge, my own coordinate-descent lasso with tolerance 1e-13, NumPy polynomial expansion), then every widget's solution was run against its tests in Pyodide 0.27.7 with scikit-learn 1.6.1 under node (`checkcode.mjs` in the scratchpad folder): all pass, and the playthrough runs them again in the browser. NumPy's `default_rng` streams agree between CPython and Pyodide.
- Every number stated in prose, tables and charts was recomputed with scikit-learn in Pyodide (`xcheck.py`, `sk5.py`, `sk7b.py`, `sk9.py`, `skq.py`): the l5 feature-count curve, train and test scores, more-features-than-rows fits; the l6 degree curve and leak table; the l7 50-factor model, ridge on 30 rows, the 1,000-panel selection-bias simulation (reported 9.15 against fresh 9.38); the l8 correlated pair (seeds 5 and 9) and 200-signal screen; the l9 raw against scaled lasso, the scaler's treatment of constant and dummy columns, duplicate columns under ridge and lasso. All agree to the places shown.
- Constrained optima in the l8 diamond picture were found by grid search and checked with SciPy's SLSQP.
- Every `how` on a screen that imports scikit-learn says the first run takes 10 to 30 seconds. Lasso calls use `max_iter=10000`, and l8 says why.

## Dataset generators (all seeded, all in hidden preludes or in the lesson's own numbers)

- `make_panel(seed, n=400, p=10)` (l5, l7, l8): `X` standard normal (z-scored features: mom, value, vol and seven others), rows in month order, `y = 0.5 + 0.6 x0 + 0.4 x1 − 0.3 x2 + 3.0 ε`, next-month return in %. Seven features are pure noise.
- l5 hook: seed 4, 60 training and 2,000 test rows, 40 candidate features, true coefficients 1.5, 1.0, −0.8 on the first three, noise sd 3; test MSE is lowest at three features (8.81). l5 transfer: seed 6, five features, true 0.6, 0.4, −0.3, 0, 0, noise sd 8; test R² 1.91%.
- `make_curved(seed, n=400)` (l6): three z-scored features, `y = 0.3 + 0.5 mom − 0.3 vol + 0.6 mom·vol + 1.5 ε`. The degree chart uses seed 3 with 120 training and 2,000 test rows. Leak table: seed 5, with February buying volume built as 0.6 × the standardised return plus noise.
- Uncorrelated six-feature panel (l7, l8 canvases): 200 rows, columns centred and scaled so XᵀX = 200 I, OLS coefficients fixed at 0.6, 0.4, −0.3, 0.12, −0.08, 0.05 (mom, value, vol, size, turnover, beta), true coefficients 0.5, 0.35, −0.25, 0, 0, 0, noise variance 4. So ridge is `b · 200/(200 + λ)`, the lasso is soft thresholding, and expected test MSE is `4 + Σ(c_j − β_j)²` (minimum at λ ≈ 46).
- One-feature ridge (l7): 20 centred points, seed 21, Σx² = 29.2772, Σxy = 23.0276.
- `make_factors(seed, months=120, k=50)` (l7 transfer): factors `0.8 × common + 0.6 × noise`, fund holds 0.4, 0.3, 0.2, −0.2, 0.1 of the first five, noise sd 1.
- l8 trap: seeds 5 and 9, mom6 and mom12 with correlation 0.97, each truly 0.3, noise sd 2. l8 transfer: seed 3, 200 pure-noise signals on 240 + 120 months.
- `make_raw(seed, n=400)` (l9): mom (%, sd 8), vol (%, mean 30, sd 10), size (£m, lognormal around £3,000m), turnover (fraction of shares a day, gamma, mean 0.006), value (book-to-price, mean 0.6, sd 0.3); `y = 0.5 + 0.06 mom − 0.02 (vol − 30) − 120 (turnover − 0.006) + 0.8 (value − 0.6) + 3 ε`. Size has no effect. Seed 2 at α = 0.1: the raw lasso keeps size and drops turnover and value; the scaled lasso does the reverse.
- `make_signals(seed, n=400)` (homework): `make_raw`'s five features plus seven pure-noise signals in units from 0.01 to 2,000.

## course.json

No change proposed. All ids, names and objectives are used as given; `sl-tradeoff` is added to l5 and l7, where they lean on level 1.

## Engine and canvas limitations

Five bullets are filed in `docs/BACKLOG-INBOX.md` under "Raised later (stat-learning level 2):":

1. Plane x-axis is always at y = 0.
2. The validator rejects the documented plane `contour` family.
3. The series x axis is index-only, with no real x values for λ grids.
4. `derive` has no linear solve, so there are no live multi-feature ridge paths.
5. A side-by-side bars pair is unreadable at column width.

Notes:
- Level 1 and level 3 files appeared while I worked. I did not edit them, and level 2 refers to level 1 only in general terms (the U-shape, k-NN distances).
- The validator rewrote `content/manifest.json`, as expected.

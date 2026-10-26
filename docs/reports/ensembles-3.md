# Report: ensembles level 3 (Boosting)

## Files written

All in `app/content/courses/ensembles/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l9-fixing-mistakes.json` | 10 screens, 4 quiz | `boost_stumps` (by hand, `DecisionTreeRegressor(max_depth=1)`, ν = 1, from 0), `residuals_after` (SSE per round; constant target gives zeros), `ensemble_predict` (sum of trees; empty list gives 0) | en-boosting, en-bagging |
| `l10-small-steps.json` | 10 screens, 4 quiz | `val_loss_curve` (`staged_predict`), `best_stage` (first argmin, 1-based), `stumps_vs_depth2_on_interaction` | en-boosting |
| `l11-gradient-boosting.json` | 10 screens, 4 quiz | `gradient_of_logloss` (exact), `hgb_early_stopped` (`n_iter_`, final validation log loss), `hgb_time_ordered_stop` (`GradientBoostingClassifier` + `staged_predict_proba` on a later block), `monotone_vs_free` | en-boosting |
| `l12-trees-on-returns.json` | 12 screens, 4 quiz | `make_threshold_features` (exact alignment), `walk_forward_models` (logistic, forest, time-stopped boosting; `TimeSeriesSplit(5, test_size=50, gap=1)`), `edge_t_stat`, `pnl_after_costs` | en-interpret, en-boosting |
| `review-3.json` | 8 items, difficulty 2 to 3, two per lesson | | |
| `homework-3.json` | 8 items, difficulty 3 to 5 (three at 5) | `boost_with_stopping` (5: from-scratch squared-error boosting with stumps, ν and a validation stopping rule, returns rounds and validation MSE), `full_study` (5: the l12 study as one function, returns three hit rates, the base rate and the best model's t) | |

Homework also has an `order` item (the honest study from features to the results table), numeric items ($t$ of 58% on 120 days = 1.75; $F_0 = \ln 0.25 = -1.3863$), two choice items (a contradicted monotone constraint; quoting a grid winner) and the `longform` colleague (3,000 depth-6 trees, ν = 0.3, random validation split, 58% on 120 days, best of five) with a 10-point rubric and a full model answer.

Canvases used: `table` widget for the 6-trade residual table and the second stump (l9), `tree` stumps, `plane` with a stage slider over 1, 5, 20, 100 stumps (curves from the fitted trees, checked against `GradientBoostingRegressor(init="zero").staged_predict`), `bars` of SSE per round, `series` of test MSE for stumps against depth 4, `series` of validation MSE for ν = 1, 0.1, 0.01 with a slider and minimum markers, `pair` of `plane` heat maps (depth 1 against depth 2 on an interaction), `grid` of learning rate by depth (tap the best cell), `plane` log-loss curve with a draggable point and tangent (l11), `bars` of up-day shares by regime and `series` of cumulative P&L after 10 bp for the three models (l12).

Traps: deep trees in boosting (l9), keeping the number of trees when ν changes (l10), early stopping on a random fraction of overlapping daily data (l11), shuffled folds on the returns study (l12). Edge cases: one round = a plain stump and residuals already zero (l9), ν = 0.01 still falling at 200 trees and depth 1 on an interaction (l10), early stopping that never triggers and a constraint the data contradict (l11), a purely linear signal and no signal (l12). Links by name: *Features that know the answer*, *Walking forward*, *Purging and embargo*, *Trying too many models* (validation), *Predicting tomorrow’s direction* (stat-learning l14).

## Validator

`node app/tools/validate.mjs`: 0 errors on every level 3 file (the run currently shows 4 errors, all in another agent's `backtest/l5` and `l6`). Two warnings on `l10`: a ladder screen moves from the `series` to an `array` (best_stage) and a `table` (subsampling).

## Playthrough

`node app/tools/playthrough.mjs --lesson ensembles/l9-fixing-mistakes --lesson ensembles/l10-small-steps --lesson ensembles/l11-gradient-boosting --lesson ensembles/l12-trees-on-returns --set ensembles/review-3 --set ensembles/homework-3 --local-cdn <scratchpad>/pkgs --shots <scratchpad>/ensembles-3/final --mobile`, no console errors:

- l9: ok, 14 checks, quiz 4/4
- l10: ok, 14 checks, quiz 4/4
- l11: ok, 14 checks, quiz 4/4
- l12: ok, 16 checks, quiz 4/4
- review-3: ok, 8 of 8
- homework-3: ok, 8 of 8, 38 of 38 marks

Every code test's `expect` was produced by running the solution in CPython (scikit-learn 1.6.1 in a scratchpad venv) and is then checked in Pyodide 0.27.7 by the playthrough; all matched exactly. Screenshots (desktop and 390 px, with Why sheets) were reviewed; fixes made: a dropped bar label, a console line that scrolled, a numeric answer shown on its own bar, the stage caption's plural, ν typeset as KaTeX.

Longest case in Pyodide: `walk_forward_models` on one 980-row study (15 fits), 1.2 s under node's Pyodide; those screens carry `budget: 60000`. Other scikit-learn cases are under 0.5 s in CPython.

## Proposed change to course.json

None.

## Dataset generators (all seeded with `np.random.default_rng`)

- l9 `make_trades(seed, n=40)`: size uniform 0.2 to 10 (% of daily volume), impact = 8√size + N(0, 3²) bp; train seed 7, test seed 107 (400 trades). Stumps at ν = 1: test MSE 17.28, 10.59, 10.20, 11.34 after 1, 5, 20, 100; best 9.86 at 15; depth 4 settles at 15.1. Six-trade example x = 1..6, y = 3, 3, 6, 6, 7, 11: SSE 14, 2, 0.8, 0.32.
- l10 `make_vol(11)`: five z-score features, y = 20 + 4x₁ + 3 tanh(2x₂) + 2.5x₁x₃ + N(0, 3²); 300 train, 300 validation. Depth 2: ν = 1 best 16.91 at 26 trees, ν = 0.1 12.75 at 55, ν = 0.01 14.63 at 200 (12.67 at 571 of 1,000). Grid best: depth 3, ν = 0.03, 11.54 at 160. `make_regime(3)`: y = 2x₁ sign(x₂) + N(0, 1); stumps 5.65, depth 2 1.85, mean 4.61.
- l11 `make_credit(seed, n)`: leverage, cover, size, two noise columns; logit = −4.2 + 4 lev + 1.2·[lev > 0.7] − 0.6 ln cover − 0.3 size. Seed 1: HGB early stopping 24 trees, final validation log loss 0.3776 (best 0.3582 at 14); learning rate 0.01 hits max_iter 100; monotone 0.3259, free 0.3267, reversed 0.4570, base 0.4400. `make_daily(4)`: pure-noise returns, 20-day and 5-day features, 10-day forward labels; random validation fraction stops at 24 with 0.6629 but tests at 0.8038 (base 0.6654); a later block picks 2 trees and tests at 0.6697.
- l12 `make_returns(seed, n=1000, kind)`: AR(1) log-volatility (0.98, sd 0.12 around ln 1%), slow mean drift (AR 0.995, sd 0.00003); kind "threshold": when the trailing 20-day vol exceeds 1.2%, a move above 1.5% is followed by +0.6σ, a smaller one by −0.48σ; "linear": −0.3 × yesterday; "none". `make_study(seed)` adds three noise columns (seed + 1000). Seed 4 out of sample (rows 730 to 979, 250 days, up share 0.484, base 0.516): **logistic 0.476, forest 0.568, boosting 0.532**; t −1.27, 1.65, 0.51; AUC 0.456, 0.572, 0.536; P&L after 10 bp on £1m −£204k, +£80k, +£102k. Shuffled KFold: 0.450, 0.567 (t 3.39), 0.579 (t 4.09). Linear seed 8: 0.644, 0.628, 0.612; none seed 7: 0.516, 0.460, 0.512 against 0.512. Over 15 seeds the threshold design averages logistic 0.494, forest 0.534, boosting 0.537 against a mean best-constant base of 0.525 (walk-forward), and 0.543 and 0.549 for the trees under shuffled folds, so the lesson's reading holds in expectation; seed 4 was chosen as a representative draw, and the lesson says so only implicitly (it is a simulation with a planted signal).

## Engine and canvas limits

Four bullets in `docs/BACKLOG-INBOX.md` under "Raised later (ensembles level 3):": the validator rejects plane `heat` functions in params (worked round via `state.functions`); heat maps are one-colour, so a signed surface needs two layers and very long expressions, and expressions cannot index a data grid; controls have no list of stops (the 1, 5, 20, 100 stage slider reads 0 to 3); bars drop colliding category labels silently.

Sandbox note: in this container scikit-learn's `HistGradientBoostingClassifier` hangs in CPython unless `OMP_NUM_THREADS=1`.

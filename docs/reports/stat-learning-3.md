# Report: stat-learning level 3 (Classification)

## Files written

All in `app/content/courses/stat-learning/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l10-predicting-a-probability.json` | 11 screens, 4 quiz | `sigmoid` / `odds_from_prob` / `prob_from_odds`, `log_loss` (matches `sklearn.metrics.log_loss`), `fit_logistic_proba` (scikit-learn, `C=1.0`) | sl-classify, sl-setup |
| `l11-the-boundary.json` | 10 screens, 4 quiz | `predict_at` + `confusion_counts`, `best_threshold` | sl-classify, sl-setup |
| `l12-accuracy-not-enough.json` | 11 screens, 4 quiz | `precision_recall`, `roc_points`, `auc_by_ranks` (matches `roc_auc_score`) | sl-classify |
| `l13-calibration.json` | 11 screens, 4 quiz | `calibrated_knn` (`CalibratedClassifierCV`, isotonic, `cv=5`), `reliability_bins`, `brier` + `expected_calibration_error` | sl-classify, sl-setup |
| `l14-up-or-down.json` | 11 screens, 4 quiz | `make_features` (alignment tested exactly), `direction_hit_rate` (scaler + logistic Pipeline), `hit_rate_t` + `pnl_after_costs` | sl-classify, sl-setup, sl-regularise |
| `review-3.json` | 10 items, difficulty 2 to 4, two per lesson | | |
| `homework-3.json` | 9 items, difficulty 3 to 5 (two at 5: the code pipeline and the longform) | `direction_report` (5: features, time split, Pipeline, hit rate, base rate, t, AUC), `calibration_report` (4: Brier, ECE, AUC by ranks) | |

Homework also has two `order` derivations (the sigmoid from linear log-odds; the steps of an honest classifier evaluation), four numeric items (cost threshold, odds over 3 units, days needed for a 2-point edge, Kelly growth when overconfident) and a `longform` item (a colleague's "72% accurate crash predictor" on 3% crash days) with a 10-point rubric and full model answer.

Traps, one per lesson: coefficient read as a change in probability (l10), threshold tuned on the test set (l11, with 0.5-as-law in screens and quiz), two models compared at different thresholds (l12, with accuracy on unbalanced classes as the hook), good AUC read as good calibration via a cubed model with identical AUC (l13), hit rate compared with 0.5 instead of the base rate (l14). Edge cases: zero-effect feature (odds ratio 1.023) and perfect separation (quiz) in l10; t = 0 and t = 1 in l11's cost table; threshold 0 giving recall 1 and precision at the base rate, and a perfect classifier (quiz) in l12; a constant base-rate forecast and a two-observation bin (quiz) in l13; always-up and zero drift in l14.

Canvases: plane (OLS line on 0/1 data; sigmoid with a log-odds slider and live odds caption; decision boundary moving with a threshold slider, captions reading precomputed count arrays; 1-NN boundary from marching squares against the logistic line; ROC curve with a threshold-step slider moving a point along the precomputed curve; PR curve with base-rate line; reliability diagram switching models; expected profit and Kelly growth curves), number-line (`log-odds` scale), bars (odds coefficients, grouped predicted vs observed per bin, returns), table (confusion counts, costs, bins, precision/recall filled by the learner), series (price path with test window; cumulative P&L of signal before and after costs, coin, always long, with a reveal slider), distribution (hit rate under the base rate with observed markers), console.

## Validator

`node app/tools/validate.mjs`: 0 errors overall. Level 3 files carry only two warnings (l10 screens 3 and 4: a ladder changes canvas kind, number-line to plane to bars).

## Playthrough

`node app/tools/playthrough.mjs --local-cdn .../scratchpad/pkgs` (Pyodide 0.27.7, scikit-learn 1.6.1):

| File | Result |
|---|---|
| l10 | 15 checks, quiz 4/4 |
| l11 | 14 checks, quiz 4/4 |
| l12 | 15 checks, quiz 4/4 |
| l13 | 15 checks, quiz 4/4 |
| l14 | 15 checks, quiz 4/4 |
| review-3 | 10 of 10 recorded |
| homework-3 | 9 of 9 right, 41 of 41 marks |

Screenshots of every screen: `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/stat-learning-3/shots` and `shots-sets`. Fixed after looking: ROC planes with `equal: true` rendered with oversized fonts (dropped `equal`); the k-NN screen's line label sat under the dots (label removed, caption names it); l11 table screens pushed the table below the fold (`maxHeight`, slider dropped on the cost screen); l14 feature table had no canvas (bars of the seven returns added).

## Numbers computed twice

Every expected value and stated number was computed in CPython 3.13 with scikit-learn 1.6.1 (a scratch venv) by the generators, which assert the numbers typed into the prose; the code tests then ran the solutions in Pyodide through the playthrough and matched. Generators: `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/stat-learning-3/build_l10.py` to `build_l14.py`, `build_sets.py`, data in `data.py`.

## Datasets (all `np.random.default_rng(seed)`, described in prose in a market setting)

- **Loans, l10 and l11** (seed 5, 400 loans in origination order, train first 300, test last 100): leverage U(0.5, 7.5), interest cover gamma(3, 1.3) clipped to [0.2, 12], loan size N(0, 1) with no effect; true log-odds −2.0 + 0.6 lev − 0.55 cover. Fitted (C = 1): −1.960, 0.601, −0.536, 0.023 (three features); −1.966, 0.602, −0.534 (two). 28 test defaults; costs £50,000 a missed default, £2,000 a wrong refusal.
- **Rare defaults, l12** (seed 3, 2,000 firms, train 1,000, test 1,000 with exactly 50 defaults): two standardised features, true log-odds −4.4 + 1.5 x1 − 1.0 x2; scores from the fitted −3.703, 1.210, −0.765; test AUC 0.828.
- **Loans, l13 and homework** (seed 21, 2,000 loans, same generator as l10, train 1,000, test 1,000): logistic fitted −2.161, 0.647, −0.605 (Brier 0.134, AUC 0.818); k-NN k = 3 overconfident (says 1 on 48 loans, 33 default); cubed logistic same AUC, Brier 0.177; isotonic-calibrated k-NN 5 Brier 0.149.
- **Returns, l14 and homework** (seed 27 main, seed 6 second; 1,000 days): r_t = 0.0004 − 0.05 r_{t−1} − 0.03 (r_{t−5} + … + r_{t−1}) + 0.01 ε_t. 980 feature rows, train 730, test 250: hit rate 0.56 against a base rate of 0.54 (t = 0.63; 1.90 against 0.5), AUC 0.577; on £1m, P&L £156k before costs, £31k after 10 bp per unit traded (63 position changes), always long £251k, a seeded coin (seed 99) −£348k.

## course.json

No change proposed. l14 lists `sl-regularise` because its Pipeline leans on lesson 9's scaling before a penalised fit.

## Engine and canvas limitations

Six bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (stat-learning level 3):".

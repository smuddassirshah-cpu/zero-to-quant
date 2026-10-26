# Report: validation level 3 (Leakage)

## Files written

All in `app/content/courses/validation/` (no other file touched except this report and `docs/BACKLOG-INBOX.md`; the validator rewrote `content/manifest.json`):

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l9-knows-the-answer.json` | 10 screens, 4 quiz | `known_at`, `centred_vs_trailing` (pandas `rolling(w, center=True)`), `leak_score_gap` (scikit-learn) | vl-leakage, vl-time |
| `l10-scaling-with-future.json` | 10 screens, 4 quiz | `scale_leak_gap`, `pipeline_cv` (`Pipeline` + `TimeSeriesSplit`), `select_then_cv_vs_cv_then_select` (all scikit-learn) | vl-leakage, vl-cv, vl-time |
| `l11-dead-companies.json` | 10 screens, 4 quiz | `survivor_bias`, `dropna_kills` (pandas), `universe_as_of` (pure Python) | vl-leakage |
| `l12-too-many-models.json` | 10 screens, 4 quiz | `expected_max_sharpe` (NumPy), `haircut`, `trials_log_count` | vl-overfit |
| `review-3.json` | 9 items, difficulty 2 to 4, two or more per lesson | | |
| `homework-3.json` | 9 items, difficulty 3 to 5 (two at 5) | `pit_value` (point-in-time lookup, d4); `leak_audit` (target leak, future-fitted transform, survivorship reasons, trial count; 8 planted cases, d5) | |

Homework also has an `order` item (leak-free procedure, universe to reported score), five numeric items (centred window, target-encoding hit rate via the arcsine formula, zero-delisting bias, Bonferroni bar 1.70, years for the rule of thumb to fall to 0.5) and a `longform` review of a colleague's note with one of each leak plus a best-of-30 (10-point rubric, full model answer with direction and size of each leak and a rerun plan).

Lesson shapes (hook, explore, name, ladder, trap, generalise or derive, transfer):
- l9: too-good hook (bars: one feature at 85% importance, 67% monthly hit rate); explore slider on a number-line (feature window end against the label window; noise hit rate 49.9% at 0 days overlap, 51.6% at 1, 61.6% at 7); tap the two leaking rows of an 8-feature `table` with known days; `known_at`; "lagged by name only" centred window; point-in-time EPS table (tap the versions known on 1 March 2020); `leak_score_gap`; trap: groupby target mean over all months with a time split (55.0% from noise); rule known(x_j) ≤ t; transfer: research note, 64% daily hit rate, the desk's 60% rule. Edge cases: 1-day overlap and a harmless future-noise feature (quiz).
- l10: hook `array` (tap the test days that entered the scaler's mean, 28.5 against 23.0); explore drag a test day (mean moves 1.9); `scale_leak_gap` (honest: under 1%, sign varies by seed); `graph` pipeline, tap the misplaced median fill (log is the no-fit edge case); `pipeline_cv`; bars of inflation by step; trap: select 10 of 500 on all rows then CV (0.403 against −0.005); `select_then_cv...` on 5 seeds; rule "every fit inside the fold"; transfer: feature-store recipes (cross-sectional z-score safe, full-history z-score and full-panel clipping leak). Quiz: `fit_transform` on test, why OLS is immune to scaling, scaling the target, which score to trust.
- l11: hook (today's 45, £100 to £367.24); explore slider through both indices (gap £160.24 at month 120); `survivor_bias`; `dropna_kills`; `universe_as_of` with look-ahead in "today's top 100"; edge case table (no deaths, random exits: no bias); trap: delisting return set to 0 (1.42 of 5.77 points remain); `order` survivorship-free backtest; gap formula from conditional `l25-survivorship` (fund database 0.30 × 4 = 1.2 points; 1 to 2% stated as an order of magnitude); transfer: today's FTSE 100 from 2005. Quiz: `dropna()` on rows keeps 31 months, death on the last day (~0.1 point), fund premium, a strategy wiki's survivorship.
- l12: hook bars of 40 noise lookbacks (best 1.05); explore series of the exact mean best against N over 3 years with the rule of thumb (crosses 1.0 at N = 15); `expected_max_sharpe` reproduces testing's 1.12 (best of 100, 5 years); `haircut` (1.3 from 40 on 3 years keeps 0.05); bars sim of 40 correlated tries (mean best 0.39, effective N); trap "we only tried three" (N = 30: noise best 1.18); `trials_log_count` (looks count, refits and drops do not); rule √(2 ln N)/√T with the alternatives (locked test, nested CV, Bonferroni) and the deflated Sharpe ratio pointed to fin-ml l11; derive (`order`) of the rule; transfer: 1.3 from 40 lookbacks, believe about 0.05. Quiz: N = 1, best fold, locked test set, forking paths.

£ is the only currency. Every `how` on a scikit-learn screen says the first load takes 10 to 30 seconds; pandas and NumPy screens say a few seconds.

## Validator

`node app/tools/validate.mjs`: 0 errors. Two warnings in my files, both accepted: l10 screens 3 and 4 change canvas kind between ladder screens (graph of the pipeline, then a console of `Pipeline` code).

## Playthrough

`node app/tools/playthrough.mjs --lesson validation/l9-... --lesson ... --set validation/review-3 --set validation/homework-3 --local-cdn <scratchpad>/pkgs`, all passed:

- l9-knows-the-answer: 14 checks, quiz 4/4
- l10-scaling-with-future: 14 checks, quiz 4/4
- l11-dead-companies: 14 checks, quiz 4/4
- l12-too-many-models: 14 checks, quiz 4/4
- review-3: 9 of 9; homework-3: 9 of 9, 41 of 41 marks

Screenshots (every screen, and with `--why` the explanation sheets) are in the scratchpad folder `validation-3` (`shots`, `shots2`) and were reviewed. Fixed after review: a doubled £ marker label overlapping the series label (l11), illustrative table numbers replaced with the panel's real values (l11), a wrong "46 firms in the final month" (it is 45), zero-height bars with no visible value (caption added), cramped pipeline graph (wider spacing, numbered steps), long code and console lines wrapped, the l12 trap plane (rule-of-thumb curve with simulated dots that did not lie on it) replaced by the exact series.

## Proposed change to course.json

None. Lessons use the names, ids and first objectives as given; each lesson adds a second objective. l10 also names `vl-cv` and `vl-time`, l9 `vl-time`.

One content deviation from the brief: on the seeded data the PCA leak is not larger than the scaling leak. Unsupervised steps (scaling, PCA) inflated 5-fold CV R² by 0.00 on average over 20 seeds; supervised ones were large (target encoding 0.45, selecting 10 of 500 noise columns 0.74). The lesson teaches that split honestly: steps that read y leak a lot.

## Dataset generators and key numbers

All NumPy `default_rng(seed)`, generator functions shipped in the preludes; scripts in the scratchpad `validation-3` (`gen_l9.py`, `l9_gap.py`, `l9_cvt.py`, `te.py`, `l10_final.py`, `l10_bars.py`, `l11_final.py`, `l12_final.py`, `hc.py`, builders `build_*.py`).

- l9 overlap: seed 9, 20,000 share-months of iid daily returns (2%), label days 1 to 21, feature 20-day return ending day k; simulated hit rates match ½ + arcsin(k/√420)/π to 0.004 (k = 1: 51.6%, 7: 61.6%, 10: 66.7%).
- l9 `make_leak(seed, n=600)`: y = 0.5·mom + 0.3·value + 21 daily shocks (6%/√21); leaky feature = days −9 to 10. Seed 3: test R² 0.023 clean against 0.221 leaky (seeds 1 to 5: 0.16 to 0.27 leaky).
- l9 target encoding: seed 2, 1,000 shares × 36 months of noise, train 24 / test 12: hit 55.0% (exact 55.3%) against 49.9% with a training-only encoding.
- l10 `make_shift(seed, n=200, p=6)`: second half ×2 and +1.5; Ridge(α = 10): leaky against clean test MSE, seed 2: 4.1647 against 4.19 (seeds 1, 4, 5 go the other way). `pipeline_cv` seed 1, 4 walk-forward folds: 5.8329. `make_noise(seed)` 100 × 500: select-then-CV 0.403 against −0.005 (seed 1). Inflation bars: mean over 20 seeds of 5-fold CV R² gaps.
- l11 `make_panel(seed=5)`: 60 firms, 120 months, drift N(0.7%, 0.6%) a month, vol 9%; delisted the month after the price closes below 40% of start, delisting return −50%. 15 die (months 30 to 114). Survivors 13.17% a year, all firms 7.40% (bias 5.77 points), delisting 0: 8.82%; index £367.24 against £207.00; dead firms averaged −17.7% a year while listed; `dropna(axis=1)` removes 15 (19 with 5 late listers); `dropna()` keeps 31 months.
- l12: noise Sharpe over n daily returns drawn directly as N(0, 252/n), following testing l11's model; `expected_max_sharpe(100, 1260, s, 20000)` = 1.12 for seeds 0, 1, 7 (exact 2.5076/√5 = 1.121). Exact E[max] by numerical integration (SciPy) for N = 1 to 100. Best of 40 over 3 years 1.25, of 30 1.18 (matches testing l11's 1.18), correlated (ρ = 0.9) 0.39 by simulation and formula.

Every stated number was computed twice: CPython (NumPy 2.5, pandas) and Pyodide 0.27.7 under Node gave identical outputs for every generator. CPython in this sandbox has no scikit-learn (pip could not install it), so each scikit-learn figure was reproduced in CPython by a NumPy reimplementation (OLS and ridge closed forms, population-sd scaling, `TimeSeriesSplit` and `KFold` splits, F-statistic ranking) and matched Pyodide's scikit-learn to every printed digit; the playthrough confirmed every code screen's expected values in the browser.

## Engine or canvas limitations

Appended to `docs/BACKLOG-INBOX.md` under "Raised later (validation level 3):" (5 bullets): no list `max` in sim outcomes (no slider on N for a best-of-N simulation); Compute Engine reads `N` as its numeric-evaluation function, so expressions in N fail to grade; zero-height bars show no value label; graph edges between close rect nodes lose their arrowheads; near-equal number-line points overlap.

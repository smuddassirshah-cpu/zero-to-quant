# Report: garch level 3 (Using forecasts)

## Files

All in `app/content/courses/garch/`. `l9-forecasting-vol.json` was kept as triaged and not edited.

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l9-forecasting-vol.json` (kept) | 12 screens, 4 quiz | `garch_forecast` + `horizon_vol`, `forecast_from_series` + `annual_vol_forecast` | gv-forecast |
| `l10-value-at-risk.json` | 12 screens, 4 quiz | `var_normal` + `var_t` (11 tests), `garch_var_series` + `expected_shortfall_normal` (12 tests) | gv-risk |
| `l11-checking-var.json` | 12 screens, 4 quiz | `count_breaches` + `kupiec_lr` (11 tests), `traffic_light` + `backtest_var` (8 tests) | gv-risk |
| `l12-vol-targeting.json` | 12 screens, 4 quiz | `target_weights` + `turnover_cost` (10 tests), `vol_target_backtest` (7 tests) | gv-forecast, gv-risk |
| `review-3.json` | 10 items, difficulty 2 to 4, l9 to l12 interleaved | | all four level 3 objectives |
| `homework-3.json` | 8 items, difficulty 3 to 5 (two at 5) | `banded_backtest` (4, 7 tests), `risk_pipeline` (5, 11 tests) | gv-forecast, gv-risk |

Homework also has an `order` item (the steps of an honest VaR backtest), numerics (a $t_5$ VaR, Kupiec at 9 of 250, a capped fund's vol), a choice (clustered breaches that pass Kupiec) and a `longform` (the March breaches note) with a 10-point rubric and a full model answer.

Lesson shapes:

- l10: hook drags the 1% cut on tomorrow's normal P&L (`distribution` with `drag: true`, choice: £21,359); explore slides the forecast and the cut follows (derive caption); name VaR on the stormiest test day (£33,648); VaR table at 95%, 99%, 99.9%; Student-$t_5$ with the √(3/5) rescaling (£23,931, the unscaled £30,894 as a keyed wrong answer); code `var_normal`, `var_t`; trap: the 250-day sd in the storm of day 1,403 (£28,356 against GARCH's £60,855; 7 against 2 breaches in days 1,380 to 1,479, 1 expected); expected shortfall (£24,470); 10-day VaR by summed variances against √10 (£187,439 against £192,440); generalise with the short position as edge case (right tail) and the two-asset sentence; code `garch_var_series`, `expected_shortfall_normal`; transfer: a prop desk's £25,000 VaR limit with VaR and ES side by side, Basel's 99% and 10-day convention in one sentence.
- l11: hook on `limits-thm` l7's 41 of 2,520 (3.2 sds); explore: tap the breaches among the eight largest losses of days 2,290 to 2,429 (three; day 2,313 is a large loss but not a breach); name the hit sequence and Binomial(1,000, 0.01), sd 3.15; exact one-sided binomial p 0.00222; Kupiec LR 8.412 by hand; the U-shaped LR curve for n = 1,000 (accepts 5 to 16: too few is a rejection); code `count_breaches`, `kupiec_lr` with x = 0 and x = n; the out-of-sample bars (GARCH normal 11, $t_5$ 8, constant vol 4 rejected for too few, true parameters 9); trap: model X with 11 breaches in two runs (9 of 11 follow a breach; Christoffersen named, GARCH's hits p = 0.62); Basel traffic light with GARCH's four test years (2, 3, 2, 4) and the zero-breach edge case (LR 5.025, p = 0.025); code `traffic_light`, `backtest_var`; transfer: the "3 breaches in a year" interview question with power (a 2% model passes 75.7% of the time over 250 days).
- l12: hook: weight for a 20% forecast against a 10% target; explore: the weight curve with target and cap controls (cap binds below 5%); name volatility targeting on the calmest test day (w = 1.0294); 63-day rolling realised vol of B, the GARCH fund and a 250-day-sized fund; turnover by hand on six days (3.58 a year; 5.099 on the whole test, 0.25% at 5 bp); code `target_weights`, `turnover_cost`; trap: look-ahead sizing with a 20-day window that ends on the sized day (10.12% looks better; shifted honestly it gives 10.71%); EWMA and a 0.1 band in a table (saving 0.159% a year); derive the rule as an `order`; edge case: a target at the long-run 14.96% (mean weight 1.0406, leverage, `markets` l13); code `vol_target_backtest`; transfer: managed-volatility and risk-parity funds, CTAs, and the Sharpe interview question answered as an empirical regularity that B cannot show.

## Validator

`node tools/validate.mjs` from `app/`: 0 errors across the repository at the final run (an earlier run showed 4 errors in `contests/l2-limits-to-complexity.json`, another agent's file mid-write). The level 3 files carry 8 warnings: ladder screens that change canvas kind (deliberate: a chart, then a table or code of the same numbers) and one point hint without a highlight.

## Playthrough

Final run, after the last edit: `node tools/playthrough.mjs --lesson garch/l9-forecasting-vol --lesson garch/l10-value-at-risk --lesson garch/l11-checking-var --lesson garch/l12-vol-targeting --set garch/review-3 --set garch/homework-3 --local-cdn <scratchpad>/pkgs`:

| File | Result |
|---|---|
| l9-forecasting-vol | 16 checks, quiz 4/4 |
| l10-value-at-risk | 16 checks, quiz 4/4 |
| l11-checking-var | 16 checks, quiz 4/4 |
| l12-vol-targeting | 16 checks, quiz 4/4 |
| review-3 | 10 of 10 recorded |
| homework-3 | 8 of 8 right, 36 of 36 marks |

No console errors. One earlier sets run failed ("0 items", then a timeout on the retry) while the level 2 agent was writing `review-2.json`; the same two sets passed alone straight after and in every later run, and a separate browser loaded all 10 items at that moment (backlog bullet 4).

Screenshots at 1280 and 390 px are in `<scratchpad>/garch-3/shots`. Fixed after looking: the x-axis title of l12's weight curve, drawn below the ticks, ran into the caption and the question (shorter label); the 3.841 line label on l11's LR curves met the axis title (`xLabelPos: "below"`); the short-position screen shaded both tails and summed them to 0.02 (now the right tail only); crowded point labels on l11's code screen; the long-run line on l12's hook crossed the series (removed).

## Numbers and their sources

Every number was computed in CPython (NumPy 2.5.3, SciPy 1.18.1) by `facts*.py` and again inside each builder (`build_l10.py` to `build_l12.py`, `build_sets.py`), which assert every figure in the prose against a fresh computation before writing the file. Code test expectations come from running each reference solution in CPython (`common.mk_tests`); `harness.py` confirms every solution passes and every starter fails in CPython, and the playthrough runs every solution's tests in Pyodide 0.27.7 (NumPy 2.0.2, SciPy 1.14.1), so both platforms agree on every tested value.

The brief's figures, all reproduced: fit (0.0121, 0.0629, 0.9235) in 15 iterations; day 2,000 forecast 0.9181%; normal VaR £21,358.88; $t_5$ quantile −2.6065, VaR £23,930.71 (unscaled −3.3649); 41 of 2,520: binomial p 0.00222, Kupiec 8.412, p 0.0037; sd 3.15 over 1,000 days; GARCH normal 11 breaches (LR 0.0978, p 0.7544), $t_5$ 8 (0.4337, 0.5102), constant vol 4 (4.706, 0.0301) on days 2,093, 2,360, 2,577 and 2,897, true parameters 9; 0 of 250: LR 5.0252, p 0.025; out-of-sample vol 14.98%; targeted 10.21%, mean weight 0.6955, largest 1.0294, turnover 5.099, cost 0.25%.

Values the brief left open:
- l10: 95% VaR £15,101.88, 99.9% £28,372.33; $t_5$ at 95% £14,330.62 (below the normal: the order flips); ES £24,470.12 (2.6652 sds); storm evening of day 1,403: GARCH £60,854.72, 250-day sd 1.2189% gives £28,355.78, true σ £63,916.63; 10-day from the storm: summed variances 64.919 %², vol 8.0572%, VaR £187,439.37 against √10's £192,439.53; from day 1,999 the two differ by £107; test-period VaR from £14,236 to £33,648 (day 2,900), mean £21,605; on the 11 breach days the loss averaged £23,608; the worst test day, 2,360, lost £33,999 against a VaR of £21,840.
- l11: Kupiec at n = 1,000 accepts 5 to 16 breaches (LR(4) = 4.706, LR(17) = 4.091); GARCH breaches per test year 2, 3, 2, 4 (all green); no two GARCH breaches on consecutive days, Christoffersen LR 0.245, p 0.62; planted model X (days 2,400 to 2,405 and 2,700 to 2,704): 9 of 11 follow a breach, Christoffersen p 1.5e−19; 95% VaR tested at 99%: 45 breaches, LR 66.6 (at 95% it passes, LR 0.54); a 2% model passes Kupiec 75.7% of the time over 250 days and 21.8% over 1,000; under the null 90.5% over 250 days.
- l12: forecasts 9.71% (day 2,417) to 22.96% (day 2,900); 63-day realised vol: GARCH fund 8.33% to 11.88%, unscaled 9.72% to 19.59%, 250-day-sized fund 6.35% to 13.43% (overall 10.37%); at the storm ending day 2,265: 19.59%, 11.37% and 12.55%; EWMA λ = 0.94: 10.34%, mean weight 0.7028, turnover 5.118; the 0.1 band (compare with the weight held): 10.05%, 1.922 a year, 63 trades, saving 0.159% a year; look-ahead 20-day window: 10.12% (shifted one day: 10.71%, turnover 7.20); target 14.96%: mean weight 1.0406, largest 1.5403, vol 15.27%; target 20%: cap binds, 20.41%; true parameters: 10.09%; the weight passed 1 on 3 test days. The strategy's own return over the test is −2.17% a year (B has zero mean), so l12 compares the 0.25% cost with "a 5% annual return" instead of the path's return, and says why B cannot show a Sharpe gain.
- Homework: planted $t_3$ series (`simulate_garch_t`, B's true parameters, shocks $t_3 \times \sqrt{1/3}$, seeds 20, 27, 31): seed 27 fits (0.0172, 0.0800, 0.8821) and its normal VaR fails (20 breaches, p 0.0051) while the $t_5$ passes (13, p 0.3621); seed 20 keeps the normal (7, p 0.3136, against $t_5$ 5, p 0.0786); seed 31 rejects both (22 and 18; p 0.001 and 0.0223). Banded backtest: band 0.05 gives (0.1006, 2.6728); 9 of 250: LR 10.229, p 0.0014, log-likelihoods −43.869 and −38.754.

## Deviations from the brief, stated honestly

- Conventions follow l9 exactly: the fitted parameters are held at full precision in every prelude (not rounded to 4 places), and `s2f = garch_variance(params, rp3)` starts at the variance of all 3,000 days. Starting at the training variance instead changes no test-day value at all (difference 0.0 after 2,000 days).
- l10's "drag the cut" hook grades a choice beside the drag, because no widget grades a distribution bound; the $t_5$ screen draws the raw $t_5$ beside a same-variance normal, since the canvas has no scaled t. Both are backlog bullets.
- l11's trap computes the share of breaches that follow a breach (9 of 11) and names Christoffersen's test in one sentence; the test itself is not coded. The "too few" second trap is a ladder screen with a keyed misconception, not a second `trap` screen (one per lesson).
- l12's "trade only when |w_t − w_{t−1}| > 0.1" is implemented, and stated, as a band around the weight actually held; comparing with yesterday's target weight would rarely trade, since daily changes are small.
- l12 has no `generalise` screen; its rule is derived in an `order` screen instead. l10 has a `generalise` screen with a confirmation item (the short position).

## Conventions

- Data: `r3, s3 = simulate_garch(2e-6, 0.08, 0.90, 3000, 7)`, `rp3 = 100 * r3`; days 0 to 1,999 train, 2,000 to 2,999 test; the l9 prelude (generator, filter, data, `params`, `s2f`) is copied verbatim into every code screen.
- Units: returns and vols in % in code (`rp3`, `s2f`), as fractions in the `var_*` functions' `sigma`, money in £ on a £1m position unless stated. A breach is `r / 100 * position < -VaR` (strict). Annualising by √252. Realised vol uses the sample sd (ddof 1).
- Kupiec: a term with a zero count in front is 0, LR is floored at 0, p from `chi2.sf(LR, 1)`.

## course.json

No change needed.

## Engine and canvas limitations

Four bullets in `docs/BACKLOG-INBOX.md` under "Raised later (garch level 3):".

Scratch files: `/tmp/claude-0/-home-user-zero-to-quant/3e0ee4d9-5633-56bc-b89e-00d7263b2d42/scratchpad/garch-3/` (`base.py`, `common.py`, `facts*.py`, `t3.py`, `build_l10.py`, `build_l11.py`, `build_l12.py`, `build_sets.py`, `harness.py`, `harness_sets.py`, `voice.py`, `shots/`).

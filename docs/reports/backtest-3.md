# backtest level 3 (Metrics): report

## Files written

All in `app/content/courses/backtest/`:

| File | Screens / items | Quiz | Skills |
|---|---|---|---|
| `l9-sharpe.json` | 12 screens (3 code) | 4 | bt-metrics |
| `l10-drawdown-calmar.json` | 12 screens (3 code) | 4 | bt-metrics |
| `l11-turnover.json` | 12 screens (2 code) | 4 | bt-metrics, bt-execution |
| `l12-benchmark.json` | 12 screens (3 code, one matplotlib) | 4 | bt-metrics |
| `review-3.json` | 9 items, difficulty 2 to 4, every lesson | | bt-metrics, bt-execution |
| `homework-3.json` | 8 items, difficulty 3 to 5 (two at 5): 1 order, 2 code (d4 `drawdown_table`, d5 `tear_sheet`), 1 longform (10-point rubric, full model answer), 4 numeric/choice | | bt-metrics, bt-execution |

Every lesson: hook, explore with a real interactive canvas (leverage slider on bars; a "today" marker slid along the equity curve with a derived running peak; a point dragged along a net-Sharpe-against-cost line; a slope slider minimising squared residuals on a scatter), ladder, trap, generalise or derive, code screens, transfer. Each has an edge case (flat or one-value series; a curve that only rises and one that starts at its peak; a rule that never trades and buy and hold; a strategy flat every day).

## Validator

`node app/tools/validate.mjs`: 0 errors overall. One warning in my files: `l12-benchmark.json screens[3].hints[1]` has no highlight (the only sensible target is the scatter's `fit` line, which the validator rejects as an id; level 4 raised the same bug).

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set backtest/review-3 --set backtest/homework-3 --local-cdn <scratchpad>/pkgs`, last run after the final edits:

- l9-sharpe ok, 16 checks, quiz 4/4
- l10-drawdown-calmar ok, 16 checks, quiz 4/4
- l11-turnover ok, 16 checks, quiz 4/4
- l12-benchmark ok, 16 checks, quiz 4/4
- review-3 ok, 9 of 9
- homework-3 ok, 8 of 8, 37 of 37 marks

Screenshots (desktop, 390 px mobile and Why? sheets) are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/backtest-3/shots`. I looked at every lesson screen and fixed: duplicated year ticks (now `%b %Y`), the trap plane's label colliding with the 252 line, a "1 years" caption, overlapping marker labels in l10's hook, a duplicate "peak" label, a trap distractor (0.48) that was numerically the same as another (0.49), a hyphen-minus in prose, and a rounding that showed −39.8% for a −39.75% drawdown.

Every code widget's solution was also run against its tests outside the browser, in CPython (NumPy 2.5.3, pandas 3.0.5) and in Pyodide 0.27.7 under node (`pyrun.mjs`): 0 failures in both. Expected values were generated in CPython and confirmed identical in Pyodide. Package load under node: numpy + pandas + matplotlib about 7 to 19 s; the heaviest screen (plot_tearsheet) about 7 s of first-run time for matplotlib's font cache.

## Engine pieces and preludes

Levels 1 and 2 were not written when I started; I first used the Level 1 section's signatures. They now exist, so every prelude in my files carries `make_bars` (verbatim, with `import numpy as np` and `import pandas as pd` on their own lines) and the level 1 and 2 solutions exactly as written: `momentum_signal`, `target_positions`, `orders_from_targets` (l3), `Portfolio` (l4), `fill_at_next_open`, `backtest` (l5), `trade_cost` (l6), `slippage_bp` (l7). Regenerating with their code changed no expected value.

Level 3 functions (names and signatures as the brief lists; additions are keyword arguments with defaults, so the listed calls still work):

- l9: `sharpe(returns, periods=252)`; `sharpe_se(sr_annual, n_years, periods=252)` (added `periods`); `rolling_sharpe(returns, window, periods=252)` (added `periods`).
- l10: `drawdown(equity)`, `max_drawdown(equity)`, `cagr(equity, periods=252)`, `calmar(equity, periods=252)`, `longest_underwater(equity)`.
- l11: `turnover(positions)`, `cost_drag(turnover_per_day, cost_bp, periods=252)`, `capacity_table(bars, lookback, book_sizes, c=1.0, half_spread_bp=2.0, sigma=0.012)` (added the last two).
- l12: `buy_and_hold(bars, cash0)`, `beta_alpha(strat_returns, bench_returns, periods=252)`, `metrics(equity, positions, bench_equity)`, `plot_tearsheet(equity, bench)`.
- homework: `drawdown_table(equity, k)`, `tear_sheet(bars, lookback, cash0=1_000_000, half_spread_bp=2.0, c=1.0, adv=2_000_000, sigma=0.012)`.

Conventions, for level 4:
- Sharpe: $\sqrt{252}$ × mean / sample sd (`ddof = 1`), NaN dropped, 0.0 for fewer than two values or sd below `1e-12` (pandas leaves about 1e-19 of noise on a constant 252-value series, so `== 0` is not enough).
- Standard error (Lo 2002, iid): per-period $\sqrt{(1 + SR_p^2/2)/T}$ annualised by $\sqrt{\text{periods}}$; with daily data about $1/\sqrt{\text{years}}$. The brief's $\sqrt{(1 + SR^2/2)/n}$ in yearly units is the `periods=1` case; I teach both and say which applies.
- Drawdown negative fractions; `max_drawdown` 0.0 for a curve that never falls; CAGR uses $n$ = number of returns (len − 1); Calmar `math.inf` when the maximum drawdown is 0 (stated on the l10 edge screen); full-sample Calmar, one sentence on the classic 36 months.
- Turnover: two-sided, positions as fractions of equity, mean over all $n$ days with the position before day 1 equal to 0 (so buy and hold over 1,260 days has 1/1260). This matches fin-ml l10's cost bill; fin-ml's `turnover` helper averaged over the $n − 1$ changes instead, and l11 says so.
- `metrics`: inputs line up by position; `positions[t]` is the exposure held over day `t` (for the engine: shares × close / equity at the previous close); hit rate over days with a non-zero position, `nan` with none; beta from `beta_alpha`; every value rounded to 4.
- Buy and hold: `int(cash0 // open[0])` shares at the first open, paying `trade_cost` once; cash may dip a few pounds below zero, as the strategy's 10,000 shares at £100+ already do.
- "Rule A" throughout the level is `backtest(bars, target_positions(momentum_signal(bars["close"], 1), 10_000), costs=trade_cost)` on `make_bars()`.

Deviation from the brief: `capacity_table` uses the vectorised path (unit positions decided at close t − 1, held open to open, cost per unit traded = half spread + $c\sigma\sqrt{Q/V}$ with $V$ the previous 20 days' mean volume) rather than l7's `backtest_with_impact`. The event-loop engine holds a fixed share count, so at large books its equity goes negative and the Sharpe of `pct_change` becomes meaningless (I measured sign flips between book sizes). Related finding for level 4: with the course's $c = 1$ and a 2m-share ADV, lookback 1's equity falls below zero by 2023 (minimum −£512k); the engine has no margin stop. The homework `tear_sheet` tests therefore use $c$ = 0, 0.25 and lookback 20 at $c = 1$, and its feedback says to check for negative equity before trusting a metric. Level 4's `sanity_flags` could add a "negative equity" flag.

## Numbers stated, with source

All from my scratchpad scripts (`common.py`, `data.py`, `gen_l*.py`, `gen_sets.py` in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/backtest-3`), confirmed in Pyodide through the tests.

- `make_bars()` first row: open 100.0463, close 99.5909, volume 2,424,184 (matches the brief).
- Rule A (lookback 1, 10,000 shares, net): final £1,160,461; daily mean 0.0166%, sd 0.978%; Sharpe 0.2692; annual vol 15.5%; maximum drawdown −0.2311 from 4 Jul 2022 (£1,397,068) to 28 Aug 2023 (£1,074,214), not recovered; last-day drawdown −0.1694; CAGR 0.0302; Calmar 0.1308; longest underwater 346 bars; beta 0.0138; alpha 4.17% a year; hit rate 0.5004; information ratio 0.134; `metrics` turnover 1.0351 (equity-based exposure drifts, so above the vectorised 0.97); last 252-day rolling Sharpe as in the l9 code feedback. Gross (no costs) Sharpe 0.6582.
- Rule B (lookback 2, 6,000 shares, net): final £1,160,378; daily mean 0.0139%, sd 0.652%; Sharpe 0.3392; vol 10.4%; maximum drawdown −0.1448.
- Global range trap: lowest £875,774 (7 Nov 2019) before highest £1,397,068: 1 − min/max = 0.3731.
- Buy and hold from £1m: 9,995 shares, final £947,384; Sharpe 0.0456 (positive arithmetic, negative CAGR −0.0098); maximum drawdown −0.3975; beta 1.
- Long-or-flat variant: full-sample beta 0.5136; on the plotted 2020 window (returns 253 to 502) 0.4847.
- Vectorised path (open to open): lookback 1 turnover 0.9698, gross 3.335 bp a day, gross Sharpe 0.566, break-even 3.44 bp, trades on 48.5% of days; lookback 2 gross 3.54 bp, turnover 0.61, break-even 5.78 bp; lookback 5 turnover 0.409, gross Sharpe −0.660; lookback 20 turnover 0.198 (brief: about 0.97 and 0.20), gross Sharpe −0.160. Net Sharpe is linear in cost to 3 decimals (checked at 5 bp).
- Capacity, lookback 2, books £10k/£100k/£1m/£10m/£100m: $c = 1$: 0.278, 0.026, −0.766, −3.125, −7.635; $c = 0.25$: 0.365, 0.302, 0.103, −0.524, −2.439; spread only 0.394.
- Homework `tear_sheet(bars, 1, c=0.25)` strategy Sharpe −0.204.
- Hand examples (exact): ten returns mean 0.15%, sample sd 0.4552%, daily Sharpe 0.3295; monthly 0.8/3.5 × √12 = 0.792; flat half the year 0.897 against 1.270; 0.05 × √252 = 0.794; SE one year 1.001 (daily), 1.225 (one yearly observation); factsheet 1.4 over 18 months: SE 0.849; 4 years for a 2.3% tail; Y's drawdown 0.98^5 − 1 = −0.0961; hook D/M net Sharpe 0.16 and 0.958; daily flip drag 12.6%; buy-and-hold drag 0.5 bp a year; review and homework items as stated in their explanations.

## Proposed change to course.json

None.

## Backlog

Six bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (backtest level 3)".

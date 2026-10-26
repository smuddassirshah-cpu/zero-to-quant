# alpha level 4 ("From signal to strategy"): report

## Files written

Everything is in `app/content/courses/alpha/`. Lesson ids, names, objectives and skills follow `course.json`: `al-portfolio` for l13; `al-costs` for l14; `al-costs` and `al-portfolio` for l15; `al-ic` and `al-costs` for l16. Money is in £.

Python generators are in the scratchpad folder `alpha-4/gen`:
- `src.py` holds every function's source text.
- `data4.py` computes every panel number into `facts.json`.
- `gen13.py` to `gen16.py` and `gen_sets.py` write the JSON.
- Every code test's `expect` is computed by running the solution at generation time.

### `l13-long-short.json` (11 screens, 4 quiz items)
- Screens, in order:
  - Hook: net and gross exposure of a £1m/£1m quintile book.
  - Explore: a `bars` canvas of eight shares' rank weights. A slider moves H's momentum and a derive recomputes the ranks, so H's weight stops at 0.2188 at +180%.
  - Rank weights named: a `table` widget.
  - Ladder 1: the quintile book against the rank book.
  - Ladder 2: dollar neutral is not beta neutral.
  - Ladder 3 (edge case): S010 dies while shorted.
  - Trap: same-day returns.
  - Generalise: the book-return formula.
  - Two code screens.
  - Transfer: prime-broker borrow cost, 25 bp of gross.
- Code: `long_short_weights(signal, min_names=10)`.
  - I added the `min_names` keyword argument; the brief's signature still works.
  - Cash on rows with fewer than 10 names or with equal signals. NaN shares get weight 0.
- Code: `portfolio_returns(weights, ret, rebalance="M")`.
  - It uses a prelude helper, `rebalance_dates(index, rebalance)`: the last day of each "D", "W" or "M" period in the index.
  - Tests include an alignment spy: flipping weights from a rebalance date on must not move any return on or before that date.

### `l14-turnover-and-costs.json` (12 screens, 4 quiz items)
- Screens, in order:
  - Hook: reversal rebalanced daily, weekly or monthly. Which has the best net Sharpe?
  - Explore: a `plane` of net Sharpe against a flat cost. Three straight lines, a control on the cost, and a derive caption.
  - Turnover named.
  - Ladders: autocorrelation predicts turnover; the cost of one trade with square-root impact; break-even cost.
  - Trap: costs charged on the book held instead of the trade.
  - Edge case: the first rebalance from cash. The exit from a dead share is also charged.
  - Generalise.
  - Two code screens.
  - Transfer: a capacity `bars` canvas with an `hlines` at half the gross Sharpe. The learner taps £300m.
- Code: `turnover(weights)` and `trade_costs(weights, half_spread_bp, adv_gbp, sigma, book_gbp, c=1.0)`. `sigma` may be a Series or a frame.
- Code: `net_returns(weights, ret, half_spread_bp, rebalance="M")`.
  - I added the `rebalance` keyword argument.
  - It charges the spread only, on the day after each rebalance, through a prelude helper `charge_next_day(cost, index)`.

### `l15-sharpe-after-costs.json` (12 screens, 4 quiz items)
- Screens, in order:
  - Hook: the held-out year is locked; then, is a net Sharpe of 0.9 better than 0.6?
  - Explore: a `distribution` with a years slider and a derived sigma. Answer: 5 years.
  - Lo's interval for our net Sharpe.
  - Ladders: daily against monthly returns (only years matter); a block bootstrap against Lo; counting N = 37 from the trial log; E[max] for N = 37.
  - Trap: the best variant quoted alone.
  - Generalise.
  - Two code screens.
  - Transfer: opening the held-out year, on a `series` with the held-out part shaded.
- Quiz edge cases: a Sharpe of exactly 0 (interval ±1.96), and N = 1.
- Code: `sharpe` and `sharpe_ci`.
- Code: `block_bootstrap_ci` and `deflated_sharpe_check(sr, n_trials, sr_sd, n_obs, periods=252)`.
  - I added the `periods` keyword argument.
  - Returns `(expected_max_sr, passes)`. E[max] uses fin-ml l11's formula, and `passes` means DSR ≥ 0.95.
  - `sr` and `sr_sd` are annual. In the study, `sr_sd` is the no-skill spread, √(252/(n − 1)).

### `l16-research-note.json` (12 screens, 3 quiz items)
- Screens, in order:
  - Hook: a tap on a `pair` of two note consoles.
  - `order` the ten headings.
  - Tap the pipeline `graph` stages that feed the Costs section.
  - Measurement: t and IR in a table.
  - Costs: break-even and net return.
  - Results: the honest sentence.
  - What failed: `multi`, four of six lines.
  - Trap: "nothing failed" with research-only results.
  - Generalise: the template as a code block, plus KaTeX.
  - Two code screens.
  - Transfer: the real-data table. The step free data cannot do well is a point-in-time universe with delisted shares.
- Quiz: the edge case of a held-out year better than research; an interviewer's questions; the README.
- Code: `run_research(p, config)` with four gaps.
  - The prelude builds `P = make_panel()` once.
  - Seven tests on the full panel; `budget` 20000.
- Code: `research_note(results, n_variants, failures)`.
  - Tests check the heading list in order, the IC, turnover and both intervals, N with the deflated check, the bullets, and `ValueError("a research note must say what failed")`.

### `review-4.json` (8 items, difficulty 2 to 4)
Items, mixing all four lessons:
- rank weights;
- why the same-day bug barely moves monthly momentum (1.82 to 1.81);
- turnover;
- the cost of a trade (£6,600);
- break-even (112 bp);
- Lo's lower end for a Sharpe of 1.0 over 504 days (−0.39);
- counting N;
- a What failed line.

### `homework-4.json` (8 items, difficulty 3 to 5)
- `hw-capacity`: code, difficulty 5. `capacity_curve(weights, ret, half_spread_bp, adv_gbp, sigma, books, rebalance="M")` returns `(net Sharpes, first book at or below half the gross)`. It returns None when that never happens or when the gross Sharpe is not positive.
- `hw-band`: code, difficulty 4. `cost_aware_rebalance(target, current, half_spread_bp, band)` returns `(new, cost)`.
- `hw-order`: order, difficulty 3. The eight steps from locking the held-out year to the note.
- Hedge the book's beta: +£5.8m of futures.
- Costs at a £400m book: 294.2 bp (impact grows with √4).
- E[max] for N = 10: 0.79.
- Why a held-out year cannot be reused.
- `hw-note`: longform, difficulty 5. The research note, with a 10-point rubric (2+2+2+1+2+1) and a full model answer filled from the run.

## Validator

`node app/tools/validate.mjs`: 0 errors overall. No errors or warnings for any level 4 file.

## Playthrough

Command: `node app/tools/playthrough.mjs --lesson … ×4 --set alpha/review-4 --set alpha/homework-4 --local-cdn …/scratchpad/pkgs --shots …`. All passed:

| File | Result |
|---|---|
| l13 | 15 checks, quiz 4/4 |
| l14 | 16 checks, quiz 4/4 |
| l15 | 16 checks, quiz 4/4 |
| l16 | 15 checks, quiz 3/3 |
| review-4 | 8 of 8 recorded |
| homework-4 | 8 of 8 right, 37 of 37 marks |

- l16 was replayed after a final alignment tweak and passed again.
- Screenshots are in the scratchpad folder `alpha-4/shots`. I looked at them and fixed what I saw: hyphen minus signs in prose are now U+2212, and I removed a cluttered mean marker on the l15 explore.
- Every untouched starter fails its tests (net_returns passes 2 of 6 trivial ones).

## Numbers and their sources

All panel numbers come from `make_panel()` with seed 2310.
- Research period: the first 1,008 days (2 Jan 2019 to 11 Nov 2022). Held-out year: the last 252 days (14 Nov 2022 to 31 Oct 2023).
- Universe: level 1's `universe_mask` (listed, 60-day £ volume ≥ £5m).
- Signals: level 2's `momentum_12_1` and `reversal_5d`.
- Book: rank weights, gross 1.
- Costs: half spread plus impact c·σ·√(Q/V), with c = 1, σ = 60-day trailing sd (`min_periods=20`, forward-filled), V = `adv_gbp`, and a £100m book unless stated.

How the numbers were checked twice:
- `data4.py` ran in CPython (NumPy 2.5).
- The same script ran in Pyodide 0.27.7 through `pyrun.mjs` (scratchpad `alpha-4/pyo_facts.py`). All 37 fact groups agree to 1e-9.
- Every code-test expectation was computed in CPython and confirmed in Pyodide by the browser playthrough.

### Monthly 12−1 momentum, research period, rank book (`run_research` output, identical in Pyodide)
- IC: mean 0.0377, sd 0.0971, t 2.30, IR 1.35, hit rate 63%, over 35 month ends.
- Quintiles: 0.22%, 0.81%, 0.75%, 0.83% and 1.52% a month (not monotone).
- Gross: Sharpe 1.82, return 5.24% a year, volatility 2.87%.
- Turnover: 2.34 a year.
- Costs: 165.4 bp a year at £100m (36.6 bp spread, 128.8 bp impact). Break-even 112 bp per £ traded.
- Net Sharpe: 1.23, with 95% interval 0.10 to 2.35.
  - Over 36 monthly returns: 1.27 (0.10 to 2.44).
  - Block bootstrap, 21-day blocks, seed 0: 0.13 to 2.36. One-day blocks: 0.10 to 2.36.
  - Lag-1 autocorrelation of the daily net returns: −0.015.
- Maximum drawdown: −3.6%.
- Held-out year: net −0.49 (−2.45 to 1.47), gross −0.01.
- Beta:
  - On 2020-03-31: long side 0.957, short side 1.073, book −0.058.
  - Regression beta on the equal-weighted index: −0.01.
- Capacity (net Sharpe by book): £10m 1.55, £50m 1.36, £100m 1.23, £200m 1.03, £250m 0.95, £300m 0.88, £500m 0.65, £1bn 0.25. Half the gross is 0.91.

### Quintile book against rank book
| | Quintile book | Rank book |
|---|---|---|
| Names held | 69 | 170 |
| Gross return a year | 7.23% | 5.24% |
| Volatility a year | 3.72% | 2.87% |
| Gross Sharpe | 1.94 | 1.82 |
| Turnover a year | 2.86 | 2.34 |
| Net Sharpe at £100m | 0.94 | 1.23 |

### Reversal (5-day)
| | Daily | Weekly | Monthly |
|---|---|---|---|
| Gross Sharpe | 3.42 | 2.35 | 1.17 |
| Net, spread only | −0.96 | 0.39 | 0.73 |
| Turnover a year | 74.9 | 34.3 | 7.8 |

- Flat-cost slopes: 0.567, 0.253 and 0.0564 Sharpe per bp. Monthly beats weekly above 6.0 bp.
- Daily rebalancing:
  - Break-even 6.0 bp; the median half spread is 7.31 bp.
  - Net at £100m: −18.8, with costs of 59.3% a year.
  - With same-day returns (the trap): −76.25.
- Rank autocorrelation, using level 2's `signal_autocorr` on the universe-masked signals:
  - momentum, 21-day lag: 0.907;
  - reversal, 1-day lag: 0.771;
  - reversal, 5-day lag: −0.027.

### Spread cost of monthly momentum
- 36.6 bp a year on each £ traded.
- 92.7 bp if charged on the book held.
- 18.3 bp if only one side is charged.

### 50/50 combination (monthly)
- Gross Sharpe 2.15, net −0.00 at £100m.
- Turnover 6.12 a year.

### Trial log, N = 37
- 6 signals (12−1 and 12−0 momentum; reversal over 1, 5 and 21 days; the combination) × 2 neutralisations (none or sector-demeaned) × 3 rebalances, all rank books, plus the l13 quintile book.
- Best net Sharpe: 12−0 momentum, monthly, at 1.24 (0.13 to 2.35).
- No-skill sd: √(252/769) = 0.572. E[max] for 37 is 1.236 (Φ⁻¹ values 1.9264 and 2.3285).
- DSR 0.49, so the check fails. With N = 1 the DSR is 0.98.

### Hand-made examples (exact arithmetic)
- Trade cost £1,411; review trade £6,600.
- Borrow cost 25 bp.
- Interval of 0.9 ± 0.89 over five monthly years; five years before the lower end clears 0.
- £400m costs 294.2 bp; hedge £5.8m.

## Conventions and departures

- **Earlier levels' code.** The preludes copy the level 1 and 2 solutions exactly: `daily_volume_gbp`/`universe_mask`, `forward_returns`, `momentum_12_1`, `reversal_5d`, `cs_zscore` and `demean_by_group`, as written in the course files.
- **Level 3 code.** Level 3 was being written at the same time. My preludes define `rank_ic` (vectorised, minimum of 10 shares), `ic_summary`, `quantile_returns` (rank then equal-count buckets) and `combine` from the Level 1 signatures.
- **Small panels.** Tests use `make_panel(30, 300, 5)`, `(40, 400, 5)` and `(60, 500, 5)`.
- **Prelude imports.** Every prelude puts `import numpy as np` and `import pandas as pd` on separate lines, as level 1's backlog note asks.
- **Added keyword arguments.** `min_names=10`, `rebalance="M"` (on `net_returns`) and `periods=252`. The old signatures still work.
- **New helpers in preludes.** `rebalance_dates`, `charge_next_day` and `max_drawdown`.
- **`run_research` results dict.** It carries `cost_bp`, `break_even_bp`, `max_drawdown`, `n_obs` and the held-out `n_obs` beyond the brief's keys.
- **Simplifications, stated in the lessons.**
  - Weights are held constant between rebalances.
  - The first rebalance from cash counts in full.
  - A dead share's exit is charged as a trade.
  - Borrow costs are excluded.
- **Run times.**
  - Package load (numpy and pandas) under node Pyodide: 5.2 s from local disk.
  - In Pyodide, `make_panel()` takes 0.43 s and `run_research` about 0.45 s per call.
  - l16's code screen checked in about 30 s within the playthrough.

## Proposed change to course.json

None.

# Report: backtest level 2 (Execution)

## Files written

All in `app/content/courses/backtest/`. Each was generated from a Python script in the scratchpad folder `backtest-2` (`gen_l5.py` to `gen_l8.py`, `gen_sets.py`, shared preludes in `common.py`).

| File | Screens or items | Code screens | Quiz |
|---|---|---|---|
| `l5-next-open.json` | 10 screens (problem, explore, problem, 2 ladders, 2 code problems, trap, generalise, transfer) | `fill_at_next_open`, `backtest` | 4 |
| `l6-commissions-and-spread.json` | 11 screens (hook, explore, name, 2 ladders, trap, 2 code, generalise, 2 transfers) | `trade_cost`, `net_sharpe_table` | 4 |
| `l7-slippage.json` | 11 screens (hook, name, explore, 2 ladders, trap, derive (order), 2 code, 2 transfers) | `slippage_bp` + `capped_qty`, `backtest_with_impact` | 4 |
| `l8-catching-look-ahead.json` | 10 screens (hook, explore, name, ladder, code, ladder (edge case), trap, pytest code, generalise, transfer) | `lookahead_check`, pytest tests | 3 |
| `review-2.json` | 9 items, difficulty 2 to 4, all four lessons interleaved | – | – |
| `homework-2.json` | 9 items, difficulty 3 to 5 (two at 5): `execution_report` (code, 5), `leaky_or_not` (code, 4), an `order` item, a `longform` (10-point rubric, full model answer), 5 others | 2 | – |

Skills: `bt-execution` for l5 to l7; `bt-bias` and `bt-execution` for l8. Money in £ throughout.

## Validator

`node app/tools/validate.mjs`: 0 errors in these six files. The remaining warnings on them are "a point hint usually highlights the canvas" on choice screens whose point hint refers to the prose. At the time of the last run the whole tree showed 51 errors, all in `cpp` and `cpp-pricing` (other agents' work in progress); none in `backtest` level 2.

## Playthrough

`node app/tools/playthrough.mjs --local-cdn <scratchpad>/pkgs --no-routes --lesson ... --set backtest/review-2 --set backtest/homework-2 --shots ... --why`: all passed.

- l5: 14 checks, quiz 4/4. l6: 15 checks, quiz 4/4. l7: 15 checks, quiz 4/4. l8: 13 checks, quiz 3/3.
- review-2: 9 of 9 recorded. homework-2: 9 of 9 right, 40 of 40 marks.
- Screenshots (with Why? sheets) are in the scratchpad folder `backtest-2/shots`. Fixed after looking: duplicate "2019" year ticks on the two date series (now `%b %y`), a bar label clipped at the bottom of l6's grouped bars (`yMin` −1.5), a longform item whose question repeated its prompt.

Every code widget was also run outside the browser by `mkverify.py` / `verify_run.py` (the app's compare rules: `equal` on `tolist()`, `isclose` rel 1e-9) in CPython (NumPy 2.5.3, pandas 3.0.5) and in Pyodide 0.27.7 under node (NumPy 2.0.2, pandas 2.2.3, pytest 8.1.1): 0 mismatches in both. Package load under node: numpy, pandas and pytest about 5 to 8 s; the whole verification run about 8 to 18 s.

## Level 1 functions in the preludes

Level 1 was not written when I started; it appeared during the work. The preludes now carry `momentum_signal`, `target_positions`, `orders_from_targets` and `Portfolio` copied verbatim from `l3-signal-to-position.json` and `l4-accounting.json`, and `sharpe` copied from `l9-sharpe.json` (with its `sd < 1e-12` guard). All expected values were recomputed after the swap and are unchanged. Signatures used are exactly the brief's: `fill_at_next_open(orders, bars)`, `backtest(bars, targets, cash0=1_000_000, costs=None)`, `trade_cost(qty, price, per_share=0.005, minimum=1.0, half_spread_bp=2.0)`, `slippage_bp(qty, adv_shares, sigma, c=1.0)`, `capped_qty(qty, volume, max_participation=0.1)`, `lookahead_check(run, bars, cut)`. Level 3 and 4 preludes already use a `backtest` with the same semantics.

Conventions I fixed (later levels should keep them):

- `backtest` returns columns `shares`, `cash`, `equity`; `costs` is a callable `(qty, price) -> £`.
- `fill_at_next_open` returns fills only for non-zero orders, indexed by the fill date; the last row's order is dropped.
- `backtest_with_impact(bars, targets, cash0, book_scale, sigma=0.012, c=1.0)`: targets and cash scaled by `book_scale`; impact uses the **signal day's** volume (`volume[t-1]`, known at its close); a buy fills at `open * (1 + b/1e4)`, a sale at `open * (1 - b/1e4)`; fees are `trade_cost(q, moved_price)`. No participation cap inside it (the cap is taught as `capped_qty`).
- The engine holds a fixed number of shares, so engine Sharpes use daily equity change over the starting cash: `sharpe(equity.diff().dropna() / cash0)`. (With `pct_change`, the 10 bp run's equity nears zero and the Sharpe is meaningless.)
- A look-ahead `run(bars)` returns a DataFrame with `target` plus `shares`, `cash`, `equity`. The target column is required: with next-open fills a `shift(-1)` leak at the cut changes only the target on row cut−1, never shares or equity before the cut.
- `noise_after(bars, cut, seed=0)`: every price after the cut multiplied by `exp(0.02 * N(0,1))` from `np.random.default_rng(0)`.
- Hand frame `hand_bars()`: six bars from Mon 4 March 2024, opens 100, 101, 99.5, 102, 103, 101.5; closes 100.5, 100, 101.5, 102.5, 102, 103; volumes 1m, 2m, 0.5m, 1m, 4m, 1m.
- Planted engines in l8 and homework: `honest_engine` (lookback 1, 10,000 shares), `peek_engine` (`close.shift(-1)`), `scaled_engine` (positions × 0.005 / full-sample `pct_change().std()`), `centred_engine` (5-day centred mean), `late_engine` (honest until row 300, then peeks), and `_with_costs` variants.
- The l8 pytest screen copies the `pytest` l5 postlude verbatim; its prelude writes `engine_lib.py` (engine, check, planted engines, `engine = honest_engine`, `engine_with_costs = honest_engine_with_costs`) and the learner's test file imports from it, so `outcome(engine=planted)` swaps work.

## Numbers and their sources

All from `make_bars()` (seed 2301, verbatim from the brief), computed in CPython and Pyodide with identical output (`numbers_check.py`, outputs `cpy.txt`, `pyo.txt`).

- Same-bar rule `sign(r_t) r_t`: Sharpe 20.3828 (matches the brief); £100 grows to £17,953,880.72. Close-to-close honest `sign(r_t) r_{t+1}`: 0.8228 (matches); £100 ends at £221.11.
- Next-open fill, vectorised (decide at close t, hold open t+1 to open t+2): 0.5656 over all 1,260 days (0.7727 over the first 1,008, matching the brief's "about 0.77").
- l5 explore sweep, `make_bars` rebuilt with the overnight share f in `gap = f*r + 0.002*noise` (closes unchanged): next-open Sharpe at f = 0, 0.1, ..., 1.0: 0.9378, 0.9104, 0.864, 0.7925, 0.6922, 0.5656, 0.4223, 0.2762, 0.1395, 0.019, −0.0833.
- Engine, lookback 1, 10,000 shares, £1m: gross P&L £495,327.10, 612 fills, £1,368,580,545.42 traded, commission £61,150.00, so £136,858.05 per bp of half spread and a break-even half spread of 3.1725 bp (3.62 bp ignoring commission).
- Engine Sharpes (P&L over £1m), gross then with commission at 1, 2.5, 5, 10 bp half spread: lookback 1: 0.604, 0.362, 0.112, −0.304, −1.129; lookback 2: 0.507, 0.374, 0.236, 0.007, −0.449.
- `make_bars(250)`, lookback 1, 10,000 shares: total costs at the default tariff £62,274.03.
- `net_sharpe_table(make_bars(500), [1, 2], [0, 2.5, 10])`: [[0.082, −0.352, −1.645], [0.349, 0.132, −0.518]].
- Capacity, lookback 2 with `backtest_with_impact`, book £10k, £30k, £100k, £300k, £1m, £10m: fees only 0.28 at every size; with impact 0.17, 0.09, −0.07, −0.33, −0.83, −3.05. Lookback 1: fees only 0.20; with impact −0.01, −0.16, −0.45, −0.92, −1.81, −5.64.
- `backtest_with_impact(make_bars(250), lookback-1 targets, £1m)`: final equity £77,672.56 at book 0.1 and £572,005.40 at book 1.
- l8: honest engine and full-sample-scaled engine both Sharpe 0.604 (final equity £1,495,327.10 and £1,203,381.31); `shift(-1)` engine 9.781. Full-sample vol 0.012177 (scale 0.4106, 4,106 shares); first-600-row vol 0.012284 (4,070 shares). The cut-at-600 tables come from these runs.
- `execution_report(make_bars(250), lookback-1, £1m, 0.005, 2 bp, c = 1)`: gross −£66,322.37, commission £12,650.00, spread £49,624.12, impact £299,398.10, net −£427,994.60.
- Hand-computed (exact): £10.00 over the mid for 500 at £100.02; £12.50 and £3.00 tickets; £25 round trip; 6,000-share walk average £100.0317 and slippage 1.17 bp; 12 bp at 1% of volume and σ = 1.2%; 120 bp at 100%; 53.7 bp at 20%; pre-trade £6,708 (£2m of £40m, σ 1.5%); 316 bp and 63 bp in the longform (£50m of £20m, σ 2%); £2,900.48 flip cost; 5,000-share capacity at a 6 bp edge.

## Interpretations of the brief

- l5's three fills are "same bar (the bug)", "at the signal's close" (0.8228) and "at the next open" (0.5656). A fill at the *next* close would be lag 2 and carry almost no edge, so I read the brief's "next close" as the signal's own close. The trap is `signal * r` without `.shift(1)` (0.82 to 20.38). The explore is a bars chart with the overnight-share slider rather than three equity lines, because the leak line dwarfs the honest ones on any shared axis; the hook shows the leak against the honest line on a log scale.
- l6's code screen "backtest extended to take costs" became: l5's `backtest` already takes `costs`, l6's `trade_cost` tests include one hand trade's cash and the £62,274.03 total through the engine, and a second screen writes `net_sharpe_table`.
- l8's hook engines report the same Sharpe (0.60) and similar curves rather than identical curves.

## Proposed course.json change

None.

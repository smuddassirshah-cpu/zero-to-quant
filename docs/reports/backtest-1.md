# backtest level 1 (Design): report

## Files written

All in `app/content/courses/backtest/`. Ids, names and skills as in `course.json`; every lesson uses `bt-design`.

| File | Screens / items | Quiz | Code screens | Shape |
|---|---|---|---|---|
| `l1-one-bar-at-a-time.json` | 11 screens | 4 | 2 (`run_loop`, `vector_targets`) | title, problem, explore, problem, ladder, problem, ladder, trap, generalise, derive, transfer |
| `l2-data-layer.json` | 10 screens | 4 | 3 (`cached_fetch`, `validate_bars`, dated `cached_fetch`) | problem, explore, problem, ladder, ladder, problem, trap, generalise, problem, transfer |
| `l3-signal-to-position.json` | 10 screens | 4 | 3 (`momentum_signal`, `target_positions`, `orders_from_targets`) | problem, explore, problem, ladder ×4, trap, generalise, transfer |
| `l4-accounting.json` | 10 screens | 4 | 1 (`Portfolio`) | problem, explore, problem, ladder ×3, problem, trap, derive, transfer |
| `review-1.json` | 9 items, difficulty 2 to 4 | | | two or more per lesson, interleaved |
| `homework-1.json` | 8 items, difficulty 3 to 5 | | 2 (`run_loop_with_portfolio` at 5, `validate_and_repair` at 4) | plus 1 `order`, 1 `longform` (10-point rubric, full model answer) at 5, 2 numeric, 1 multi, 1 choice |

Trap per lesson: l1 `rolling(5, center=True)` (tap the window: the trailing-window pick is the byKey misconception); l2 a cache keyed by ticker only serving a stale 2019 to 2021 file; l3 sending the target as the order (the runaway holding); l4 marking at the fill price, or charging the fee twice. Edge case per lesson: l1 the first `lookback` bars (target 0, never NaN); l2 an empty download is never cached; l3 a NaN signal gives target 0 and an unchanged target gives order 0; l4 a position closed to exactly 0 shares and a zero-quantity fill.

Reference texts: Chan, *Quantitative Trading*, chapter 3 (l1 transfer explanation); López de Prado, *Advances in Financial Machine Learning*, chapters 11 to 12 (l1 title screen).

## Validator

`node app/tools/validate.mjs`: 0 errors in my six files. Three warnings remain, all "a ladder screen usually reuses the previous canvas kind" (l1 screens 4 and 6, l3 screen 3): each of these ladders follows a code screen, whose canvas is a `console`. Errors in the validator output belong to other levels' files (l5 to l7, l13), which I did not touch.

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set backtest/review-1 --set backtest/homework-1 --local-cdn .../scratchpad/pkgs --shots ... --why --mobile`:

- l1-one-bar-at-a-time: ok, 14 checks, quiz 4/4
- l2-data-layer: ok, 14 checks, quiz 4/4
- l3-signal-to-position: ok, 14 checks, quiz 4/4
- l4-accounting: ok, 14 checks, quiz 4/4
- review-1: ok, 9 of 9 recorded
- homework-1: ok, 8 of 8 right, 36 of 36 marks

l1, l3 and l4 were replayed after the last layout fixes (all ok). Screenshots, including the Why sheets and the 390 px versions, are in `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/backtest-1/shots` and `shots2`. Fixed after looking at them: pipeline graph nodes touching (now two rows of three, with arrows), wrapping trade text in the l4 ledgers, a "1 rows" caption, and uneven number widths in the array cells.

Every code widget's `solution` also passes its tests in CPython (`check_code.py`), and every starter fails at least one test.

## Numbers and their sources

Everything from `make_bars` was computed in CPython (NumPy 2.5.3, pandas 3.0.5) and in Pyodide 0.27.7 (`node pyrun.mjs nums.py`); the two agree to every digit shown.

| Number | Where used | Value |
|---|---|---|
| First row of `make_bars()` | l1 hook table (rounded to 2) | open 100.0463, high 100.2093, low 98.7023, close 99.5909, volume 2,424,184 |
| Same-bar leak Sharpe, `sign(r_t) r_t` | not used in level 1 (check only) | 20.3828 |
| Honest close-to-close Sharpe | not used in level 1 (check only) | 0.8228 |
| Last date of `make_bars()` | l2 dates (2019-01-02 to 2023-10-31) | 2023-10-31, 1,260 bars |
| Bars from 2019-01-02 to 2021-12-31 | l2 trap ("bars: 783") | 783 |
| `momentum_signal(make_bars(40).close, 3)` | l3 code test | `[0, 0, 0, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1]` |
| `run_loop_with_portfolio(make_bars(60), 100 × 3-day momentum, 10,000)` final equity | homework | £10,495.02 with no fee, £10,481.02 with a £1 fee (14 trades, so exactly £14 apart) |

Hand numbers, each recomputed by a script: l1 bar 7 history 8 rows, lookback-5 warm-up bars 0 to 4, centred window bars 5 to 9. l2: 1 download of 40; busday count 6 to 20 March 2020 = 10. l3: day 9 order 1,500; −0.5 signal gives order −7,500; table orders 0, 4,000, 0, 6,000, −20,000, 0, 10,000; 10 days of target-as-order gives 40,000; 5% of 2,000,000 = 100,000 against a target of 200,000. l4 ledger (cash, shares, equity at the close): day 1 4,989 / 100 / 10,029; day 2 4,989 / 100 / 9,969; day 3 2,503 / 150 / 10,033; day 4 10,092 / 0 / 10,092; day 5 14,171 / −80 / 10,067; day 6 +£40 to 10,107. The break-even close is £50.11. The reconciliation story: £61,240 = 3,062 × £20. Review: 1 + ... + 250 = 31,375; the short gives £12,118.50. Homework: ledger £25,316 (cash £33,436, −200 shares); shares traded 20,000.

Package load measured with `node pyrun.mjs`: Pyodide plus NumPy and pandas from the local CDN took 3.2 to 6.0 s to load, and a run of the 7 `run_loop` tests took 3.1 s. In the browser playthrough a lesson with code screens takes 17 to 84 s, the first numpy/pandas import included. Every `how` that imports them says "takes about 15 seconds".

## Seeds and conventions

- `make_bars()` is copied verbatim from `docs/briefs/backtest.md` into every prelude that needs data, preceded by two extra lines, `import numpy` and `import pandas` (see the backlog: the widget's import scan misses `pandas` in `import numpy as np, pandas as pd`). Later levels should copy the preludes from these files, with those two lines.
- Hidden helpers, defined in the preludes: `hand_bars()` (5 bars, 4 to 8 March 2024, closes 100, 102, 101, 99, 103), `up_day(history)`, `decide_mom(history, lookback)`, `Spy` (records `len(history)` and the last date of each call), `counting_fetch(calls, empty=())` (30 bars from `make_bars(30, seed=sum(map(ord, ticker)))`), `ranged_fetch(calls)` (slices `make_bars()` by dates), `planted(*kinds)` (one planted problem per code on `make_bars(30)`), `run_ledger(cls)`, `conservation(cls, n=200, seed=7)` (`random.Random(7)`), `identity_holds(...)` and `messy(*kinds)`.
- File-system tests use `tempfile.mkdtemp()` per case, because cases in one run share a working directory.
- Signs: targets and orders are in shares, and sales are negative.

## Engine functions as written (for levels 2 to 4)

- `run_loop(bars, decide)`: a list of targets; `decide(bars.iloc[: t + 1])`.
- `vector_targets(close, lookback)` and `momentum_signal(close, lookback)`: `np.sign(close.pct_change(lookback)).fillna(0)`, a float Series indexed like `close`.
- `cached_fetch(ticker, fetch, cache_dir="cache", start=None, end=None)`: CSV, read back with `index_col=0, parse_dates=True`; an empty frame is never written.
- `validate_bars(df)`: a sorted list of the seven codes; a gap means `np.busday_count > 5`.
- `target_positions(signal, max_units)`: an int Series; NaN becomes 0; clipped to ±1 before scaling; `np.round`.
- `orders_from_targets(targets)`: `t.diff()` with day 0 equal to the first target (floats).
- `Portfolio(cash)`: `.cash` (float), `.shares` (int), `fill(qty, price, cost=0.0)` (a zero quantity changes nothing, cost included), `equity(price)`.

## Proposed change to course.json and the function list

No change to `course.json`. One signature extension, kept backward compatible: `cached_fetch(ticker, fetch, cache_dir="cache", start=None, end=None)`. With `start` or `end` given, the file is `{ticker}_{start}_{end}.csv` and the call is `fetch(ticker, start, end)`. Without them it behaves exactly as the brief's signature (`{ticker}.csv`, `fetch(ticker)`). I made this change because the brief's trap (a key of ticker only) needs a fix the learner can write. The l4 real-data swap should then use `fetch = lambda t, s, e: yf.download(t, start=s, end=e, auto_adjust=False)`.

Suggested course-level change (not made): put `backtest` on the code track in the curriculum data, so a generalise screen may state its rule as a fenced code block. As things stand, the validator demands KaTeX (see the backlog).

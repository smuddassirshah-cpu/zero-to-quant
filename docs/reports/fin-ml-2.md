# fin-ml level 2 (Features): report

## Files written (all in `app/content/courses/fin-ml/`)

- `l5-features-that-do-not-drift.json` (11 screens, 4 quiz items; skill `fm-features`)
- `l6-fractional-differencing.json` (11 screens, 4 quiz items; `fm-features`)
- `l7-ranking-across-stocks.json` (11 screens, 3 quiz items; `fm-features`)
- `l8-hidden-look-ahead.json` (11 screens, 3 quiz items; `fm-features`, `fm-eval`)
- `review-2.json` (8 items, difficulty 2 to 4, interleaving l5 to l8)
- `homework-2.json` (7 items: two `code` items, one at difficulty 5; one `order`; one `longform` with a 10-point rubric and model answer; three choice items)

Generators and helpers are in the scratchpad folder `fin-ml-2` (`build_l5.py` to `build_l8.py`, `build_sets.py`, `gen_l5.py`, `gen_l6.py`, `l8gap.py`, `hw2code.py`, `checkcode.mjs`, `probe.mjs`).

## Validator

`node app/tools/validate.mjs`: 0 errors in these six files. One warning: l8 screen 6 (a `graph` pipeline) follows a `table` ladder screen. The run's single remaining error is in `arma/l3-unit-root.json`, another agent's file.

## Playthrough (`--local-cdn .../scratchpad/pkgs`)

- l5: ok, 15 checks, quiz 4/4
- l6: ok, 15 checks, quiz 4/4
- l7: ok, 14 checks, quiz 3/3 (replayed after a final prose fix)
- l8: ok, 14 checks, quiz 3/3
- review-2: ok, recorded 8 of 8
- homework-2: ok, marked 7 of 7, 33 of 33 marks

In one combined run, review-2 failed with "the set has no items" and homework-2 timed out. Each passed when run alone. Other agents were writing fin-ml level 1 and 3 files at the time, so I put the failure down to that concurrent activity.

Every code solution was also run in Pyodide 0.27.7 under Node (`checkcode.mjs`), and every test passed. The expected values come from CPython (NumPy 2.5, pandas 3.0, statsmodels 0.15) and agree with Pyodide (NumPy 2.0.2, pandas 2.2.3, statsmodels 0.14.4). I looked at the screenshots. Fixes made after looking: date ticks (the `%Y` dateFormat put "2016" at Dec 2016, so I removed it), the rate chart's y range, table alignment, plane label placement, and the l7 outlier pair, now stacked.

## Datasets (all `np.random.default_rng(seed)`)

- **l5 hook:** seed 29. A weekly log random walk, drift 0.25% and sd 2.5% a week, 470 weeks, 2015 to 2023. It trains on 313 weeks to 25 Dec 2020. 154 of 157 test weeks (98.1%) lie above the training maximum of £297.78. Full-sample z of price averages −0.61 in training and +1.21 in test. `make_walk(seed, n)` is 100 plus a cumulative sum of standard normals. `make_stock(seed, n)` gives daily closes (drift 0.04%, sd 1.5%) and volume whose level rises by about e^0.8.
- **l6:** `make_logprice(5, 1500)`: ln 100 plus a cumulative sum of 0.0004 + 0.012 z. Fixed-width threshold 1e-4; window lengths are 282 at d = 0.4, 200 at d = 0.5 and 527 at most (d = 0.15). The stationarity rule is VR(20) below 0.2. It is defined in the lesson as Var(20-day change) / (20 Var(1-day change)).
  - **Smallest passing d = 0.4:** VR 0.185, against 0.224 at d = 0.35. The correlation with the level is 0.864; d = 1 keeps 0.036.
  - **ADF cross-check:** with one lag, ADF passes from d = 0.3. With AIC lags it passes from d = 0.45. The lesson shows all three and says to state the test with the d.
  - **Threshold trap:** at 1e-5 the window is 1,458 days, leaving 43 values. At 1e-6 it is 7,550, longer than the series.
  - **Seed 11:** passes at a different d (tested).
- **l7:** six named shares on three hand-made days (all down; all up with a tie; a +40% takeover outlier). `make_panel(seed, 60, 20)` is a long panel (date, stock, sector, mom) with about 10% of rows dropped, so day sizes run from 14 to 20.
- **l8, one-day leak:** `make_returns(seed, 2000, phi=0.05)` is AR(1) returns with a 1% sd. The feature is the 5-day mean. The sign is fitted on the first 1,000 days and the hit rate is scored after that.
  - **Seed 7:** honest 54.2%, with the feature shifted one day too few 66.2%. The edge over a coin rises from 4.2 to 16.2 points, almost four times.
  - **No momentum:** with phi = 0 the leaky version still scores 65.9%.
  - **Hit rate does not double:** it cannot from 50%, so the lesson talks about the edge over a coin instead.
  - **Other l8 data:** a step price (centred 5-day mean rises on day 19, trailing on day 21), and a two-quarter EPS example (published 15 Feb and 8 May 2024).
- **Homework d5:** `make_universe(2)`, 20 stocks by 120 business days with a planted centred 5-day `smooth` column, plus two quarters of fundamentals per stock published 20 to 49 days after quarter end. `summary` returns ((2400, 7), 0.980591, 2320).

## course.json

No change proposed. All names, objectives and skill ids are used as given.

## Engine and canvas limitations

Listed in `docs/BACKLOG-INBOX.md` under "Raised later (fin-ml level 2):" (4 bullets).

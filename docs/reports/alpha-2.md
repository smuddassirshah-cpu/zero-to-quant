# alpha level 2 (Signals): report

## Files written (all in `app/content/courses/alpha/`)

- `l5-momentum-signal.json`: 10 screens, 4 quiz items, skill `al-signal`. It has one `code` screen, `momentum_12_1(ret, lookback=252, skip=21, min_periods=200)`, with 8 hidden tests.
- `l6-reversal-signal.json`: 10 screens, 4 quiz items. It has two `code` screens: `reversal_5d(ret)` with 6 tests, and `signal_autocorr(signal, lag)` with 6 tests.
- `l7-ranks-and-z.json`: 10 screens, 4 quiz items. It has two `code` screens: `cs_rank(signal)` with 6 tests, and `cs_zscore(signal, clip=3.0)` with 6 tests.
- `l8-neutralising.json`: 10 screens, 4 quiz items. It has two `code` screens: `demean_by_group(signal, sector)` with 6 tests, and `neutralise(signal, beta, sector)` with 8 tests.
- `review-2.json`: 9 items at difficulty 2 to 4. They mix all four lessons.
- `homework-2.json`: 7 items at difficulty 3 to 5:
  - `code` at difficulty 5: `rolling_beta` + `neutral_momentum`, with 9 tests
  - `code` at difficulty 4: `winsorise`, with 6 tests
  - one `order` item
  - one `longform` item with a 10-point rubric and a model answer: a reversal signal built from raw closes and z-scored over time, reported with an IC of 0.15
  - two choice items and one numeric item.

Generators live in the scratchpad folder `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/alpha-2/`:

- `common.py`, `l5.py` to `l8.py` and `sets.py` build the content.
- `data.py` builds the canvas data.
- `fill.py` runs every code widget's solution and tests in CPython and in Pyodide, then writes Pyodide's values into `expect`.
- `hl.py` adds the hint highlights.
- `verify.py` and `verify_all.py` recompute the panel numbers.
- `make.sh` rebuilds everything.

## Validator

`node app/tools/validate.mjs`: 0 errors overall. There are 0 errors and 4 warnings in these six files:

- l8 screens 4 and 5: the point hints have no highlight. These are scatter and pair canvases; the validator rejects `fit` as a hint id on a scatter.
- l8 screen 7: a bars canvas follows a code screen's table.
- l8 screen 1: `explain.canvas` contains `params`. This is a false positive. On a bars canvas `state.params.k` is the slider's value, and the Why? sheet renders correctly (screenshot checked).

## Playthrough (`--local-cdn .../scratchpad/pkgs`)

| file | result |
|---|---|
| l5 | ok, 14 checks, quiz 4/4 |
| l6 | ok, 14 checks, quiz 4/4 |
| l7 | ok, 14 checks, quiz 4/4 |
| l8 | ok, 14 checks, quiz 4/4 |
| review-2 | ok, recorded 9 of 9 |
| homework-2 | ok, marked 7 of 7, 33 of 33 marks |

In the first combined run, review-2 reported "no items" and homework-2 timed out. Both passed when run alone, and in two later combined runs. The level 1, 3 and 4 agents were rewriting `manifest.json` at the same time.

I looked at the desktop, 390 px and Why? screenshots. Fixes made after looking:

- series ticks every 63 days, so they run −252 to 0 instead of ending at −2
- number-line interval labels moved apart (one was overlapping)
- axis labels added to the half-life plane
- sector colours named in the l8 prose
- the homework beta formula moved from a cramped table into the prose

## Seeds, generators, conventions

- **Data generator.** `make_panel(n_stocks=200, n_days=1260, seed=2310)` is copied verbatim from the brief. I checked that it is identical to the copy in level 1's `l4-returns-panel` prelude. Tests use `make_panel(30, 300, 5)`, and the homework uses `make_panel(30, 600, 5)`.
- **Prelude imports.** Every prelude puts `import numpy` and `import pandas` on their own lines above the generator. The widget's import scan reads `import numpy as np, pandas as pd` as numpy only; this was already in the backlog from the backtest course.
- **Level 1 functions.** The level 2 preludes do not need any. The signals take `ret` directly, and every test builds its data with `make_panel`. Level 1's `forward_returns` matches the convention the lessons describe.
- **Later functions in preludes.** Later screens' preludes load earlier level 2 functions with these exact names: `momentum_12_1` in l6, l7, l8 and the homework, `reversal_5d` in l6, and `neutralise` in the homework.
- **`momentum_12_1`** has the signature `momentum_12_1(ret, lookback=252, skip=21, min_periods=200)`. The keyword arguments are an addition, as the brief allows; the defaults keep the brief's signature. It computes `log1p(ret).rolling(lookback - skip, min_periods).sum().shift(skip)`, then `.where(ret.notna())`. That last step means a share not listed on the date has NaN.
- **`reversal_5d`** is `-log1p(ret).rolling(5, min_periods=5).sum()`.
- **`signal_autocorr(signal, lag)`** is the mean over dates of the row-wise Pearson correlation of ranks. It uses only shares present on both dates and skips dates with fewer than 3 such shares. The result is rounded to 4 places.
- **`cs_rank`** is $(\text{rank} - 1)/(n - 1) - 0.5$: fin-ml l7's percentile rank, centred. Ties are averaged, NaN shares are excluded, and a date with one share scores 0.
- **`cs_zscore`** uses `ddof=1`, gives NaN for a date with one share or with all values equal, and clips at ±3.
- **`neutralise`** fits `np.linalg.lstsq` on a constant, beta and sector dummies. A date whose share count is 0, or not above the rank of X, is left NaN.
- **Homework `rolling_beta(ret, market, window=252, min_periods=126)`.** The market is the equal-weighted mean of `ret` across shares. The masked rolling means give covariance divided by variance, using only the days each share has a return.

## Numbers stated, with source

Every number was computed in CPython (NumPy 2.5.3, pandas 3.0.5) and in Pyodide 0.27.7 (NumPy 2.0.2, pandas 2.2.3) with `verify_all.py`. The two agreed to every digit shown. Panel ICs use the Level 1 check's definitions:

- the forward return is `L[::-1].rolling(h).sum()[::-1].shift(-1)`, with `L = log1p(ret)`
- monthly dates are 252, 273, ... up to 1,238 (47 dates)
- weekly dates are 5, 10, ... (250 dates; 247 for the 21-day reversal)

**Momentum (l5)**

- 12-1 momentum: mean IC 0.0325, t 2.64, 47 dates. This reproduces the brief's check.
- 12-minus-0, i.e. without the skip: 0.0296, t 2.34.
- One month only: 0.0008.
- The `shift(-21)` look-ahead version: 0.2985, t 24.52.
- Explore share `S019` at the last date: 12-1 return +34.2%, whole year +15.6%, last month −13.9%.
- Hook series: hand-made, seed 7. Inside the window A rose 26.79% and B fell 0.35%.

**Reversal (l6)**

- Mean IC against the next week: 1-day 0.0142 (t 2.91), 5-day 0.0243 (t 4.52), 21-day 0.0174 (t 3.12).
- Half-life: $\ln 0.5/\ln 0.8 = 3.106$ days. This follows from the generator's parameter, not from data.

**Signal autocorrelation (l6), full panel**

| signal | lag 1 | lag 5 | lag 21 |
|---|---|---|---|
| momentum | 0.9944 | 0.9757 | 0.9090 |
| reversal | 0.7706 | −0.0263 | 0.0006 |

**Normalising (l7)**

- The rank IC of `cs_rank(mom)` and of `cs_zscore(mom)` is 0.0325, the same as the raw signal.
- Clipping touches 690 of 191,497 values.
- Rank-weighted book, share of the long side held by the top share: 43.75% with 8 shares. With 200 shares it is $0.5/(5000/199) = 1.99\%$.

**Neutralising (l8)**

- Correlation of momentum with beta across shares on month-ends: min −0.223, max 0.196.
- On 2023-07-06 it is 0.196, with 182 shares, after the equal-weighted market rose 31.1% over the window.
- Mean IC: sector-demeaned 0.0252 (t 2.50); neutralised for beta and sector 0.0255 (t 2.52).
- The neutral and raw signals have a mean rank correlation of 0.928.

**Homework**

- On `make_panel(30, 600, 5)`, on the last date, estimated and true betas correlate 0.83, with a mean absolute error of 0.0993.
- On the full panel the correlation is 0.89.

**Code tests.** Every `expect` value was produced by `fill.py` in Pyodide, and CPython gave the same value. Hand-checked items:

- review: $\ln(52/40) = 0.2624$, half-life 1.943, $(n - 1)/\sqrt n$ bound of 11 shares
- homework: residual 0.02, first score 220 days
- l7 quiz: $7/\sqrt 8 = 2.4749$
- l6 example: −Σ log1p = 0.0810

**Load and run times.** Pyodide under node took 3.2 to 6.3 s to load numpy and pandas from the local CDN. Each widget's solution and tests took under 2 s.

## Proposed course.json change

None.

## Notes for later levels

- **For level 3.** The 5-day reversal IC is 0.0243. Neutralising costs about a fifth of momentum's IC.
- **For level 4.** Reversal's ranking is close to new each week (lag-5 autocorrelation −0.03), so its turnover will be high.
- **Interface for neutralising.** `neutralise` takes a fixed beta Series. The homework shows the per-date pattern for time-varying betas: `neutralise(mom.loc[[d]], beta_t.loc[d], sector)`.

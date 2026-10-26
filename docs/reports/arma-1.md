# Report: arma (Stationarity and ARMA, topic 2.2), level 1 "Stationarity"

## Files written

All in `app/content/courses/arma/` (nothing else edited except this report and `docs/BACKLOG-INBOX.md`; the validator rewrote `content/manifest.json`):

| File | Screens / items | Quiz | Code screens |
|---|---|---|---|
| `l1-returns-not-prices.json` | 12 screens | 4 | 4: `summary_stats_by_block`, `log_returns`, `lag_slope`, `level_vs_return_fit` |
| `l2-what-stays-the-same.json` | 11 screens | 3 | 3: `rolling_mean_sd`, `is_roughly_stationary`, `simulate_ar1` + `variance_of_ar1` (one screen) |
| `l3-unit-root.json` | 12 screens | 3 | 4: `df_t_stat`, `df_null_quantile`, `adf_decision` (statsmodels), `adf_power` |
| `l4-differencing.json` | 12 screens | 3 | 4: `difference`, `integration_order` (statsmodels), `detrend_linear`, `seasonal_difference` |
| `review-1.json` | 8 items, difficulty 2 to 4, two per lesson | | |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5) | | 2: `df_quantiles` (d4), `classify_series` (d5, statsmodels); plus 2 `order` derivations and a 10-point `longform` |

All lessons use skill `ts-stationary` and the names and objectives from `course.json`. Money is £ throughout. Generators and helpers: `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/arma-1/` (`data.py`, `lib.py`, `gen_l1.py` to `gen_l4.py`, `gen_sets.py`, `checkcode.mjs`).

## Validator

`node app/tools/validate.mjs`: 0 errors in arma files. Two arma warnings ("a point hint usually highlights the canvas", l1 screen 7 and l3 screen 12, where no valid id fits). At the time of the last run, errors elsewhere were from other agents' files only (ensembles l10).

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set arma/review-1 --set arma/homework-1 --local-cdn .../scratchpad/pkgs --mobile`: all passed.

- l1: 16 checks, quiz 4/4. l2: 14 checks, quiz 3/3. l3: 15 checks, quiz 3/3. l4: 15 checks, quiz 3/3.
- review-1: recorded 8 of 8. homework-1: marked 8 of 8, 37 of 37 marks.
- Screenshots (desktop and 390 px) in `.../scratchpad/arma-1/final/`, earlier rounds with Why? sheets in `shots`, `shots2`, `shots34`. Fixes made from them: misleading `%Y` date ticks dropped, scatter pair stacked, overlapping "par" label removed, series C rescaled, hyphen-minus replaced by − in prose.
- Every code solution was also run in Pyodide 0.27.7 under node (`checkcode.mjs`): 132 of 132 cases pass; each untouched starter fails at least the value tests.
- One console error during setup came from `random-vars/course.json` (another agent's file).

## statsmodels load time

Measured in Chromium from a local copy of Pyodide 0.27.7: Python boot 6.0 s, fetching and installing statsmodels with NumPy, SciPy, pandas and patsy 5.2 s (local disk, no network), `import` plus the first `adfuller` 9.2 s. Under node the same import took about 40 s (SciPy 22 s, statsmodels 18 s). The three statsmodels screens carry `budget: 90000` and their `how` says the first run takes 20 to 40 seconds. adfuller results in Pyodide (statsmodels 0.14.4, NumPy 2.0.2) matched CPython (statsmodels 0.15.0, NumPy 2.5.3) to about 1e-14, so no tolerances had to be widened.

## Seeds and generators

Prelude functions, identical in the generators and the widgets: `make_price(seed, n=2000)` (log random walk, drift 0.03%, sd 1.2% a day, from £100), `make_ar1(phi, n, seed, c=0)` (x₀ = ε₀), `make_walk(seed, n=500, drift=0)`, all on `np.random.default_rng(seed)`. Dates: 2,000 business days from 2016-01-04 to 2023-09-01.

- l1: price seed 12 (training = first 750 days, to 2018-11-16); seeds 6, 9, 3, 7 in tests; bond near par `100 + 0.25 * make_ar1(0.9, 500, 5)`; volatility regime seed 8 (sd 0.7 then 2.2); walk explore seed 21.
- l2: hook seeds 31 to 34; explore shocks seed 41; block table seeds 4 to 8; trap AR(1) φ = 0.95 seed 161 against walk seed 1161 (250 days); break seeds 51, 52; transfer seeds 61, 62.
- l3: walk seed 71, AR(1) φ = 0.9 seed 72, φ = 0.8 seed 73, borderline spread φ = 0.97 seed 114; Dickey-Fuller null simulation seed 2024 (2,000 walks of 250 days); power seed 7 (2,000 paths of 250 days per φ), seed 3 for 1,000 days.
- l4: shocks seed 81, AR(1) seed 82, volume seed 91, spread seed 95. Homework planted series via `make_planted(kind, seed)`, seeds 101 to 112.

## Numbers stated, with sources

Each was computed by the generator in CPython and either re-run in Pyodide (code tests) or recomputed in a separate script (`nums1.py`, `explore*.py`).

- l1 (seed 12): training closes £98.82 to £161.42; 2023 closes £217.58 to £255.95; return sd 1.19% in training and 1.29% in 2023; price block means £116, £148, £206, £228; lag slope 0.9988 (log price 0.9987, return 0.0161); R² 0.9977 against 0.00026 for returns; Desk A fit p = 0.563 + 0.9961 p₋₁, implied mean £144.48; one-day MSE (Desk A, Desk B) seed 12: 6.5228, 6.4738; seed 6: 10.8531, 6.3305 (71% worse). Short table series 100, 102, 99, 97, 96, 94 has slope 0.9912.
- l2: AR(1) variance 1/(1 − 0.25) = 1.333, simulated 1.353 over 20,000 days; trap ranges 18.6 (AR) and 10.4 (walk); shock half-life at φ = 0.95: 13.5 days; calm and stormy sds 0.60% and 1.96%.
- l3: Dickey-Fuller t of the φ = 0.9 series −5.05 (equal to `adfuller(maxlag=0, regression="c")`); 45.25% of 2,000 null walks below −1.645; simulated quantiles −3.43, −2.89, −2.59 against MacKinnon's large-sample −3.43, −2.86, −2.57; power at φ = 0.8, 0.9, 0.95, 0.98, 1.0: 1.00, 0.97, 0.46, 0.12, 0.05, and 0.85 at φ = 0.98 with 1,000 days; ADF: walk −2.0002 (p 0.2865), φ = 0.8 −7.03, lesson 1 price p 0.7203, its returns −43.96, spread −2.70 (p 0.0735); KPSS p ≤ 0.01 (walk), ≥ 0.10 (φ = 0.8).
- l4: differenced straight trend: lag-1 correlation −0.49, variance 2.02; detrended walk residual ADF p 0.46; walk p 0.52 ("c") and 0.77 ("ct"); trend plus noise p 0.97 ("c") and below 0.0001 ("ct").
- Homework: simulated n = 100 quantiles (−3.48, −2.89, −2.58); classifier misclassified 3 of 40 seeded walks in a trial run (the tests avoid those seeds).

## Deviations from the brief

- l2's hook trio uses a trend, a variance change and a change in memory (smooth AR(0.9) then white noise of the same variance), not a seasonal pattern. A deterministic seasonal pattern breaks the constant-mean promise, not the autocovariance one, so matching it to the third condition would have taught something false. Seasonality appears in l2's generalise screen and in l4's seasonal-difference screen.
- l2 puts `simulate_ar1` and `variance_of_ar1` on one code screen, to stay within 12 screens.
- l1's `level_vs_return_fit` scores both desks on one-day price forecasts (MSE in £²). The one-day errors are close on a trending path, and the lesson says so honestly. The strong contrast is the long-horizon pull to a/(1 − b) (screen 10) and the flat-training seed 6.
- fin-ml l6 (fractional differencing) is not written yet; l4 refers to it in one sentence by course and lesson number.

## Proposed course.json change

None.

## Engine and canvas limitations

Seven bullets under "Raised later (arma level 1):" in `docs/BACKLOG-INBOX.md`: validator id patterns for walk and scatter, slider-chosen series data, year-aligned date ticks, more than two stacked panels, an AR(1) walk model, a share beyond a bars cut, and shared lesson data.

# Topic 2.2 exam: time series

File: `app/content/exams/topic-2.2.json` (id `topic-2.2`, 45 minutes, pass 0.7).
Generator and checks: `scratchpad/exam-2.2/` (`gen.py` builds the file; `code_ar.py`, `code_garch.py`, `code_pair.py`, `code_items.py` hold the code items; `runner.py`, `pycheck.mjs`, `variants.py` grade solutions, starters and wrong versions in CPython and in Pyodide; `verify.py` recomputes the stated numbers by other methods; `pyfacts.py` compares CPython and Pyodide; `lint.py` checks voice; `ptool/pt.mjs` is a copy of the playthrough with a tall viewport for screenshots).

Minutes: topic 2.2 has 60 hours, and `examMinutes` gives 45 for 60 hours or fewer. Pass mark 0.7 as in the pattern exams (backlog bullet: 45 minutes is tight with three code items).

## Shape

22 items, interleaving `arma` (8), `garch` (6) and `coint` (7), plus one longform that spans the exit line.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 4 | 18% | 20% |
| 3 | 11 | 50% | 50% |
| 4 | 5 | 23% | 20% |
| 5 | 2 | 9% | 10% |

Widgets: 5 choice, 5 numeric, 3 table, 3 code, 2 tap-regions (bars, series markers), 2 multi, 1 order, 1 longform (10 points). Canvases: console x2, bars x4 (one grouped), pair of bars, series x4, table.

| # | id | d | course | skills | widget |
|---|---|---|---|---|---|
| 1 | e-adf-read | 2 | arma | ts-stationary | choice, console (ADF on closes and returns) |
| 2 | e-garch-step | 2 | garch | gv-models | numeric (one GARCH step) |
| 3 | e-spurious-fit | 2 | coint | co-spurious | choice, series (two walks, t = -32) |
| 4 | e-band-lags | 2 | arma | ts-acf | tap-regions on bars (lags outside the band, one chance bar) |
| 5 | e-ar1-table | 3 | arma | ts-models, ts-acf | table, bars (AR(1), phi = -0.7) |
| 6 | e-clusters-multi | 3 | garch | gv-clustering, ts-acf | multi, grouped bars |
| 7 | e-eg-critical | 3 | coint | co-test | choice, console (ADF p against `coint`) |
| 8 | e-ma-identify | 3 | arma | ts-models, ts-acf | choice, pair of bars (ACF and PACF) |
| 9 | e-breach-days | 3 | garch | gv-risk | tap-regions on series markers |
| 10 | e-hedge-flip | 3 | coint | co-spread | numeric (reverse regression) |
| 11 | e-unit-root-steps | 3 | arma | ts-stationary, ts-models | order |
| 12 | e-vol-ahead | 3 | garch | gv-forecast, gv-models | numeric |
| 13 | e-pair-positions | 3 | coint | co-pairs | table, series (z-score rule with a stop) |
| 14 | e-aic-bic | 3 | arma | ts-models | table (AIC and BIC from log-likelihoods) |
| 15 | e-fan-width | 3 | arma | ts-forecast | numeric (AR(1) interval at h = 3) |
| 16 | e-code-ar-fan | 4 | arma | ts-forecast, ts-models | code |
| 17 | e-kupiec | 4 | garch | gv-risk | numeric |
| 18 | e-johansen-rank | 4 | coint | co-test | choice, table (trace table, a trap row) |
| 19 | e-code-garch-report | 4 | garch | gv-models, gv-forecast, gv-risk | code (hand fit, SLSQP) |
| 20 | e-lookahead-multi | 4 | coint | co-pairs | multi |
| 21 | e-code-pair-verdict | 5 | coint | co-test, co-spread, co-pairs, co-spurious | code |
| 22 | e-returns-note | 5 | all | ts-stationary, co-spurious, co-test | longform |

Skills: all 12 are covered (`skills` map is the union of the three course.json maps): ts-stationary 3, ts-acf 4, ts-models 5, ts-forecast 2, gv-clustering 1, gv-models 3, gv-forecast 2, gv-risk 3, co-spurious 3, co-test 4, co-spread 2, co-pairs 3.

Exit line: items 7, 18 and 21 test a pair for cointegration (the right critical values, the trace-table rank, and a full verdict function with the I(1) check first). Items 1, 11 and 22 test why models are fitted to returns and not prices. Item 22 asks for both in one note on a seeded pair.

Fresh against the courses: every dataset has a seed that the lessons do not use (price seed 80, walks 213, `make_arma` seeds 43, 63 and 64, GARCH seeds 31 and 57, `make_pair` seeds 3 with 400 days, 12, 14 and 117's own three-series system). Code items are new problems: an AR(1) forecast fan with a horizon-dependent interval, a GARCH fit that also returns tomorrow's VaR, and a pair verdict that chains the I(1) check, Engle-Granger and a half-life screen. Traps reused from the lessons are applied to new numbers: the ADF table against Engle-Granger, the largest loss that is no breach, a trace row that exceeds its value after a non-rejection.

## Code items (Pyodide 0.27.7 under Node, `pycheck.mjs`; CPython 3.13 with statsmodels 0.15.0 in `cpy_check.py`)

| item | tests | solution | starter | wrong versions (each fails, first failing test) |
|---|---|---|---|---|
| e-code-ar-fan | 8 | 8/8 | 0/8 (stops with an error) | no reversion (1), sqrt-k width (2), divisor n-3 (2), variance sum from j = 1 (2), 1.645 (2), sample mean for mu (1), fixed width (2) |
| e-code-garch-report | 9 | 9/9 | 0/9 | today's variance for tomorrow (7), 365 days (4), 95% z (7), persistence = alpha (1), sample sd (4), VaR in % (7) |
| e-code-pair-verdict | 9 | 9/9 | 0/9 | no I(1) check (5), y leg only (6), ADF on the residual (3), no half-life (7), half-life from levels (1), alpha ignored (9) |

Dropping the stationarity constraint from the fit passes (the constraint is inactive on these series), so it is not a planted bug. Tests use tolerances: AR fan 2e-5 absolute on values rounded to 6 places; GARCH persistence 0.002 absolute, volatility and VaR 1% relative. Pyodide and CPython pass the same tests. Slowest case in Pyodide: 0.47 s (a 3,000-day pair). `how` on the statsmodels item says 20 to 40 seconds for the first run, with `budget` 90,000. Starters and docstrings are wrapped to 54 characters or fewer.

## Numbers computed twice

First computation in `gen.py` (CPython), with an assertion for each stated number; second in `verify.py` by a different method (45 checks, all pass); Pyodide agreement in `pyfacts.py` (14 result lines identical to the printed places).

- Item 1: ADF statistic -1.4365, p 0.5647 (lag 0) and returns -17.4129 (one lag), by `adfuller` and by a hand regression with MacKinnon's p.
- Item 2: 0.02 + 0.07 x 5.76 + 0.91 x 1.6 = 1.8792, root 1.37084; wrong values 1.28 and 1.25 by hand.
- Item 3: slope -0.3778, R² 0.6728, t -32.00, residual lag-1 correlation 0.952, daily-changes R² 0.00078, by OLS and by covariance formulas.
- Item 4: ACF by `acf` and by hand: 0.5193, 0.2407 and 0.1251 at lags 1, 2 and 9; band 0.098.
- Item 5: -0.7, 0.49, -0.343 and 4/0.51 = 7.8431 (simulated variance of a 400,000-day path 7.82).
- Item 6: the ACF of r (largest 0.041), |r| and r² (0.14 to 0.22); Ljung-Box p 0.306 and below 1e-4, by `acorr_ljungbox` and by Q = n(n+2) sum rho²/(n-k).
- Item 7: Engle-Granger -3.1282, p 0.0828, critical values -3.9241, -3.3515, -3.0551, and ADF on the residual -3.1241, p 0.0248, by `coint`, by a hand Dickey-Fuller regression (no constant, AIC lag 0) with MacKinnon's tables; identical in Pyodide (statsmodels 0.14.4).
- Item 8: ACF -0.485 at lag 1 (band 0.088) and PACF -0.485, -0.281, -0.181, -0.104, by `pacf` and a Durbin-Levinson recursion.
- Item 9: the eight largest losses, their VaRs and the margins 0.22, 0.20 and 0.38, by `simulate_garch` and a second variance recursion written out again.
- Item 10: slopes 0.8626, 0.9359 (x on y), R² 0.8073 and the hedge 1.0685, by OLS and by covariance; wrong values 1.159 and 0.696.
- Item 12: 1 + 0.97^10 x 1.5 = 2.1061, root 1.4513, by the closed form and by iterating the recursion ten times; the off-by-one value 1.4398.
- Item 13: positions 0, -1, -1, -1, 0, 0, +1, 0, +1 by two differently written state machines.
- Item 14: log-likelihoods -571.34, -560.97, -554.25, -552.63, -552.51 by `ARIMA` and by the exact Gaussian likelihood from the autocovariance matrix; AIC 1114.49 and 1113.02, BIC 1126.47 and 1128.98; gaps 1.47 and 2.51.
- Item 15: 24.096, half-width 8.418, upper end 32.514, by the closed form and by 400,000 simulated paths (mean 24.093, 97.5% point 32.52).
- Item 17: LR 3.9136 by the log-likelihood formula, by `xlogy` and by `binom.logpmf`; z 2.25 and z² 5.05; chi-squared 5% point 3.8415.
- Item 18: trace 64.22, 12.91, 4.43 with 95% values 29.80, 15.49, 3.84, by `coint_johansen` and by a hand Johansen procedure (reduced-rank eigenvalues).
- Item 22: ADF p 0.47 and 0.46 (prices), below 1e-4 (changes), beta 1.4532, R² 0.9482, t 117.0, Engle-Granger -3.605 with p 0.0241 and values -3.911, -3.344, -3.050, residual ADF p 0.0057, half-life 19.57 days, return correlation 0.88; AR(1) coefficient of the price 0.9906 by `ARIMA` (maximum likelihood; OLS gives 0.9914, and both are about 0.99).
- Code items: expected values come from the reference solutions in CPython and agree in Pyodide; the ratio test (VaR scales with the position) is exact.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no message for this file; the manifest lists `exams/topic-2.2.json`.
- Voice lint (`lint.py`): no `!`, no em-dash, no sentence of 20 words or more outside code, explanations of at most three sentences, no American spellings. Minus signs in prose are the real minus.
- `playthrough.mjs --exam topic-2.2 --local-cdn <pkgs>`: 22 of 22, passed (19 to 51 s over several runs, desktop and `--mobile`).
- Screenshots reviewed (tall viewport copy of the playthrough). Fixes made from them: bars axis titles ("Count" replaced by ACF and PACF); the band label that sat on the bars removed; the breach chart moved to a window where the eight dots are spread out and the largest loss is no breach; the AIC and BIC table reduced to three columns so it fits 390 px; code docstrings rewrapped to 54 characters.

## Engine notes (also in `docs/BACKLOG-INBOX.md`)

Six bullets under "Raised later (topic 2.2 exam)": the 45-minute allowance, table overflow on a phone, the default "Count" axis title on grouped bars, the code editor's lack of soft wrap, the unreadable `--why` result page, and crowded markers on a phone.

## Proposed course.json change

None.

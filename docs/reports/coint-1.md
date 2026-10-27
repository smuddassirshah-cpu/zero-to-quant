# Report: coint (Cointegration, topic 2.2), level 1 "Spurious relationships"

## Files written

All in `app/content/courses/coint/` (nothing else edited except this report and `docs/BACKLOG-INBOX.md`; the validator rewrote `content/manifest.json`). `l1-two-walks.json` was triaged green on 27 October and is unchanged; the other files build on its seeds, numbers and voice.

| File | Screens / items | Quiz | Code screens |
|---|---|---|---|
| `l1-two-walks.json` (unchanged) | 12 screens | 4 | 3: `levels_regression`, `differences_regression`, `spurious_rate` |
| `l2-not-correlation.json` | 12 screens | 4 | 2: `return_correlation` + `drift_apart` (one screen), `classify_pair` (statsmodels) |
| `l3-stays-put.json` | 12 screens | 4 | 3: `spread` + `adf_pvalue` (one screen), `best_beta_by_adf`, `is_i1` (all statsmodels) |
| `l4-engle-granger.json` | 12 screens | 3 | 2: `engle_granger_by_hand`, `eg_decision` + `wrong_decision` (one screen) (statsmodels) |
| `review-1.json` | 8 items, difficulty 2 to 4, two per lesson | | |
| `homework-1.json` | 9 items, difficulty 3 to 5 (two at 5) | | 2: `ar_pair` + `spurious_share` (d4, NumPy), `is_i1` + `screen_pairs` (d5, statsmodels); plus an `order` item, an `expression` derivation and a 10-point `longform` |

Skills: l2 `co-spurious`, `co-test`; l3 and l4 `co-test`; review and homework items name `co-spurious` and `co-test`. Names and first objectives are those in `course.json`. Money is £ throughout. Generators and helpers are in `/tmp/claude-0/-home-user-zero-to-quant/3e0ee4d9-5633-56bc-b89e-00d7263b2d42/scratchpad/coint-1/` (`lib.py`, `mk.py`, `gen_l2.py`, `gen_l3.py`, `gen_l4.py`, `gen_sets.py`, the fact scripts `facts2.py` to `facts4.py`, `hw.py`, `ar.py`, `pyfacts.py`, and the checkers `harness.py`, `mkpc.py`, `pyrun.mjs`, `voice.py`).

## Validator

`node tools/validate.mjs`: 0 errors overall at the last run, and no errors or warnings in any coint file. The only coint line is the expected "not yet written: 8 of 12 lessons" for levels 2 and 3.

## Playthrough

`node tools/playthrough.mjs --lesson coint/l1-two-walks --lesson coint/l2-not-correlation --lesson coint/l3-stays-put --lesson coint/l4-engle-granger --set coint/review-1 --set coint/homework-1 --local-cdn .../scratchpad/pkgs --shots .../coint-1/final --mobile`: all passed.

- l1: 16 checks, quiz 4/4. l2: 16 checks, quiz 4/4. l3: 16 checks, quiz 4/4. l4: 15 checks, quiz 3/3 (replayed alone after a last table fix, passed).
- review-1: recorded 8 of 8. homework-1: marked 9 of 9 right, 41 of 41 marks.
- One failure on the way: l3's drag-point screen failed with key `P` while its target was `{ on: "f", x: 1.47 }` on a polyline (backlog bullet 1); it now uses a plain target and passes.

Each code solution was also run against its hidden tests in CPython (statsmodels 0.15.0, NumPy 2.5.3) with `harness.py` and in Pyodide 0.27.7 (statsmodels 0.14.4, NumPy 2.0.2) under node with `mkpc.py` and `pyrun.mjs`: every solution passes every case in both, and every untouched starter fails every case in both (l2: 17 cases, l3: 22, l4: 15, homework: 16).

Screenshots, desktop and 390 px, are in `.../coint-1/final/`; earlier rounds with Why? sheets in `shots2`, `shots3`, `shots4` and `shotsS`. Fixes made from them: l3's plane charts moved the x axis to the bottom (`xAxis: "bottom"`) because the axis title collided with the point label at y = 0; l4's number lines were narrowed to −4.2 to −2.6 (and −5.6 to −2.6 where pair C's −5.13 appears) because −2.86 and −2.91 overlapped on a −6 to 0 axis; the ADF point was given its own colour; l3's transfer lost a distractor (a share against its own price a year ago) whose gap is in fact stationary.

## statsmodels load time

Under node, Pyodide 0.27.7 from the local copy took 5.2 to 7.7 s to fetch and install NumPy, SciPy, pandas, patsy and statsmodels from local disk, and the first statsmodels import plus first call about 2.0 to 2.5 s more. The arma level 1 report measured 9.2 s for import and first `adfuller` in Chromium. Every statsmodels screen carries `budget: 60000` on top of the engine's 30 s heavy-import allowance, and each `how` says the first run takes 20 to 40 seconds. The slowest hidden cases in Pyodide: `screen_pairs` on the eight-series universe (about 3 s), the 40-pair counting tests in l4 (about 2 s each).

## Seeds and generators

Every code prelude holds the course generators from `docs/briefs/coint.md` verbatim (`make_two_walks`, `make_pair`, `make_broken_pair`). Two helpers are added where screens need them:

- `make_case(name, n=1000)`: lesson 2's four pairs exactly as the brief defines them. A: `default_rng(1)`, x = cumsum(e₀), y = cumsum(0.8e₀ + 0.6e₁). B: `default_rng(2)`, x = cumsum(e₀), u₀ = 3e₀₁, u_t = 0.5u_{t−1} + 3e_{t1}, y = x + u. C: `make_pair(3, 1000)`. D: `make_two_walks(4, 1000)`.
- `make_ar1(seed, n=500, phi=0.5)` (l3 `is_i1` tests) and `make_universe(seed=31, extra=False)` (homework `screen_pairs`): `make_pair(seed)` as bank_a/bank_b, `make_pair(seed + 1, alpha=2.0, beta=0.8, phi=0.9, x0=60.0)` as miner_a/miner_b, and from `default_rng(seed + 2)` a correlated-only oil pair 30·exp(cumsum(0.015e₀)) and 45·exp(cumsum(0.012e₀ + 0.009e₁)); with `extra=True` also a utility share 50·exp(cumsum(0.01e₂)) and a stationary fund NAV 20 + AR(1) with φ = 0.7 from `default_rng(seed + 3)`. Universes 31, 51 and 21 were chosen because no cross pair rejects at 5% (seed 41 was rejected: four spurious cross-pair rejections).
- l3 screen 6's legs: x = 20 + AR(1) φ = 0.5 from `default_rng(6)`; y = 50 + walk from `default_rng(5)`. Homework `ar_pair(seed, n, phi)`: columns of `default_rng(seed).standard_normal((n, 2))`, a₀ = z₀; this reproduces l1's 74.3% and 82.0%.
- The Engle-Granger null in l4: seeds 0 to 999 of `make_two_walks(seed)`, OLS of the second walk on the first, `adfuller(res, maxlag=0, regression="n", autolag=None)[0]`.

## Numbers stated, with sources

All were computed in CPython by the generator scripts and recomputed in a separate script; every statsmodels value was rerun in Pyodide with `pyfacts.py` and agreed to every stated place (22 quantities compared; only the 16th significant figure of two tiny p-values differed).

- l2: daily return correlations A 0.7867, B 0.2984, C 0.9319, D 0.0057; `coint(y, x)` p-values A 0.80 (statistic −1.3926), B 0.0000 (−10.4247), C 0.0001 (−5.1315), D 0.4722 (−2.1079). B's gap: long-run sd 3/√0.75 = 3.46 (sample 3.27 with ddof 0), Var(Δu) = 2 × 12 × 0.5 = 12 (sample 12.00), design correlation 1/√13 = 0.277 (sample 0.298). 20-day rolling correlation: C 0.73 to 0.99, A 0.26 to 0.91. `drift_apart`: A with β = 0.8 (2.0406, 5.4086), C with β = 1.5 (1.4646, 1.7070), B with β = 1 (3.4084, 3.1585). A's gap: Var 0.36t, sd 18.97 at t = 1,000, range −19.3 to 5.0. Pairs: 500 × 499/2 = 124,750; 2,000 × 0.05 = 100; 300 × 299/2 = 44,850; sd at t = 400 is 0.6 × 20 = 12.
- l3 (`make_pair(3, 1000)`): ADF p-values (AIC, constant) x 0.9401, y 0.9039, y − 1.5x − 5 3.3·10⁻⁵ (statistic −4.9152); ADF statistic of y − βx: −0.436 at β = 0, −1.09 at 1, −5.011 at 1.45, −5.131 at 1.47 (the minimum on a 0.01 grid), −4.915 at 1.5, −2.98 at 1.6; below −2.86 only for β between about 1.33 and 1.61. Gap sd (ddof 1): £24.0 at β = 0, £1.59 at 1.47, £1.64 at 1.5. `best_beta_by_adf`: 1.0 on [0, 1, 2, 3], 1.5 on [1.6, 1.4, 1.5], 1.45 on the 0.05 grid from 1 to 2, 1.47 on the 0.01 grid, 1.52 for `make_pair(5, 1000)`, 0.85 for `make_pair(7, 1000, beta=0.8)`. Pair A: level gap y − 0.8x p 0.5136; Δy − 0.8Δx statistic −11.93. `adf_pvalue`: pair D gap 0.3711, seed 103's first walk 0.3131; u[999] = −0.5473. `is_i1` series: walk seed 5 level p 0.4514, AR(1) seed 6 and white noise seed 7 reject on levels, walk of a walk seed 9 p 0.95 and 0.08.
- l4: seed 103 residual: `adfuller(res)` −2.9059, p 0.0447, 5% value −2.867; by hand (no lags, no constant) −2.9091, with a constant −2.9059; `coint` −2.9091, p 0.1334, critical values −3.9185, −3.3484, −3.0530; slope −1.9236, intercept −1.1571. Pair C: β̂ 1.4744, α̂ 6.4908, residual statistic −5.1315 (−5.1289 with a constant), `adfuller(res)` p 1.2·10⁻⁵, `coint` p 9.4·10⁻⁵ (0.0001), critical values −3.9074, −3.3423, −3.0487, `coint(x, y)` −5.109; residual on day 500 from the rounded closes £46.96 and £76.81: 1.08 (exact 1.0878), residual sd £1.59. Null: 14.6% of 1,000 statistics below −2.86, 12.9% at or below seed 103's, 5.0% below −3.35, empirical 5% quantile −3.347. Decisions on seeds 0 to 39: `coint` rejects 1, the trap 7; on 0 to 199: 10 and 35. Pair A by hand −1.7312, pair B −19.7271. Broken pair: p 0.0001 on days 0 to 999, 0.9914 on 1,500; gap falls to −£48 by day 1,499. Power at 250 days: 29 of 100 seeds (`make_pair(seed, 250)`, seeds 0 to 99); at 1,000 days, 100 of 100.
- Review: 0.3√(248/0.91) = 4.95; 0.8√100 = 8; 6/3 = 2; 2,000 × (0.146 − 0.050) = 192.
- Homework: −0.114 residual; Var(u) = 4/0.36 = 11.11, Var(Δu) = 4.44, correlation 3/7 = 0.429; Var(y − rx) = (1 − r²)t; `spurious_share` 0.743 (φ = 0.98), 0.82 (φ = 1, 500 seeds), 0.505 (0.9), 0.135 (0.5), 0.05 (0), 0.123 beyond |t| = 10 at φ = 0.98, 0.75 on 100 seeds (example); `ar_pair(0, 3, 0.5)` first column 0.1257, 0.7033, −0.1840; `screen_pairs`: universe 31 gives bank (β̂ 1.5915, p 0.0004) and miner (0.8208, 0.0000), oil correlation 0.82 with p 0.77; universe 51 with extras the same two pairs, the fund NAV passing against both banks with p 0.0000 if the leg check is skipped; universe 21 bank p 0.034, so only the miners survive at 1%.

## Deviations from the brief

- l2's explore steps through the four pairs' gaps (y − 0.8x, y − x, y − 1.5x − 5, y − x) on one axis, beside a bars panel of daily correlations, instead of levels and a changes scatter: a frames control cannot change the series axis, and pair C's prices sit on a different scale from the three walks (backlog). The hook shows A's and B's gaps; the 2 × 2 table the learner fills is screen 3, right after the explore.
- l2 puts `return_correlation` and `drift_apart` on one code screen, l3 `spread` and `adf_pvalue`, and l4 `eg_decision` and `wrong_decision`, to stay within 12 screens.
- l3's valley plots the ADF statistic, not the p-value: the p-value is 0.0000 across the whole floor, so the valley would be flat.
- l4's `wrong_decision` reads `adfuller`'s own p-value on the residual (AIC lags, constant). It gives True on seed 103 (p 0.0447), as the brief asks, and it is the exact habit the trap targets.
- l4's short-sample edge case (29 of 100 at 250 days) is a quiz item, not a ladder screen; the broken-pair edge case is screen 10.
- For the level 2 author: on seed 103 the reverse test `coint(x, y)` gives −3.5291, p 0.0299, a false rejection in one direction only. The lessons quote the direction comparison for pair C only (−5.1315 against −5.109).
- l3 and l4 name the Markets course's cost of carry and lesson 8 (Johansen), lesson 5 (direction) and lesson 11 (breaks) by name only; none of those exists yet.

## Proposed course.json change

None.

## Engine and canvas limitations

Four bullets under "Raised later (coint level 1):" in `docs/BACKLOG-INBOX.md`: drag-point `{ on, x }` targets on a plane polyline, a series axis a frame cannot change, a scatter cloud a frame cannot swap, and `cut` as a bars highlight id.

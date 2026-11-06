# stat-models level 3 (Without the assumptions): author report

Session T, content wave 1. Brief: `docs/briefs/stat-models.md`, preamble and `## Level 3`.

## Files written

| File | Screens / items | Quiz | Notes |
|---|---|---|---|
| `l10-rank-tests.json` | 10 | 3 | 24 returns on a `number-line`; a draggable big day whose rank is a sum of comparisons; $U$ table; $P(A > B)$; median trap with a counter-example; signed ranks; D6 again; ties and $2/20$; code `rank_sum_u` + `mw_exact_p` (dynamic programme) |
| `l11-permutation-tests.json` | 11 | 3 | live permutation null (`bars` `sim`, `shuffle(pooled)`, seed 11, bins aligned so the cut at 0.562 is an edge); 184,756 splits; $+1$ rule; null SD and its derivation; skewed planted case; persistent-signal trap; $1/(B + 1)$ floor; sign flips and the bootstrap; code `perm_test` + `sign_flip_test` (vectorised) |
| `l12-kernel-density.json` | 10 | 3 | histogram with a `binWidth` control; 60-term kernel curve over the bars with $h$ on a slider and a derive caption for $\hat f(0)$; Silverman; quantiles with a normal overlay; `bw_method` trap; spreads KDE on a `plane` with an `area` below 0; code `kde`, `silverman_h`, `kde_quantile` |
| `l13-robust-estimates.json` | 11 | 3 | draggable big month with live mean, median and trimmed mean; breakdown; trimmed mean, MAD; live bootstrap of the mean (seed 13); beta `scatter` with OLS live and the bisquare line, day 40 draggable; deletion trap; Theil-Sen; code `mad_scale`, `trimmed_mean`, `bisquare_fit`; statsmodels `RLM` screen (budget 60000) |
| `review-3.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | | interleaves all four lessons; `r3-paired` recalls level 2's paired design |
| `homework-3.json` | 7 items, difficulty 3 to 5 (two at 5) | | `h-block-perm` code (difficulty 5, `performance: "code"`: `naive_perm_test` and `shift_test`, planted dependent and real-edge cases), `h-u-moments` order derivation, `h-beta-var` longform |

All lessons use `sm-nonpar`. l11's objective starts with "Build", so the level is rule-matched; `h-block-perm` is its one performance task.

## Gates

1. Validator: **0 errors**.
2. Voice scan over the course folder: **0 and 0**.
3. Numbers: `python3 docs/reports/stat-models-L3-numbers.py`: **157 of 157 passed**, exit 0 (about 20 s: it enumerates 184,756 splits and 4,096 sign patterns).
4. Playthrough: four lessons, `--set stat-models/review-3`, `--set stat-models/homework-3`, `--mobile --tablet --local-cdn <pkgs>`: **all passed**.

## Numbers and their sources

All planner values were reproduced in Pyodide (SciPy 1.14.1, statsmodels 0.14.4), and the seeded datasets match local NumPy: 0.185, 0.423, $-0.4276$, 0.677, 195, 117, 27, 0.00829, 2,704,156, 0.0102, 0.8125, 70, 8, 0.0122, 4,096, 0.233, 0.461, 0.00484, 0.1, 0.562, 0.104, 184,756, 0.2088, 1.3129, 0.2057, 0.4361, $-0.0037$, 0.8965, 0.985, 2.84, 0.2724, 0.3132, 0.2917, 0.4688, 0.4190, 0.3953, 0.4187, $-3.406$, $-2.089$, $-2.766$, 0.3356, 13.1%, 3.389, 0.722, 0.857, 0.4448, 8.130, 0.3464, 0.3897, 0.1949, 0.0568, 2.555, $(0.382529, 1.583828)$, 0.4175, 0.4700, $(0.005175, 1.142954)$, 0.88977, 1.167936, 0.0503, 1.234554, 1,764, 1.278, 1.404, 1.854, 1.151052; day 40 sits 27.0 scale units from the bisquare line.

Differences and choices:
- Monte Carlo $p$: my seeded 100,000 shuffles (seed 1) give 20,916, so $p = 0.2092$ (planner 0.2095 with another seed); the lesson states 0.2092.
- Huber's location for the fund months: 0.93 with $k = 1.345$ and the MAD scale fixed (statsmodels' joint `huber` fails to converge in Pyodide); the planner had 0.94.
- $60^{-1/5} = 0.4409$ (an early draft had 0.4407; fixed, the $h$ values were unaffected).
- The bisquare scale uses `norm.ppf(0.75)` for 0.6745: with the rounded 0.6745 the intercept moves by $8.5 \times 10^{-7}$; the code test allows $10^{-5}$ for that reason.
- Homework longform: the stock's normal-fit 99% VaR from these data is 7.78% (the 25% day inflates the SD to 3.506%), not the brief's illustrative 2.1%, so the prompt says 7.8%. KDE 1% quantile $-3.36$% at Silverman's $h = 0.5745$, empirical $-2.81$%.
- Planted cases (computed and reported): skewed 5 against 5, exact permutation $p = 0.0556$ (14 of 252) against Welch 0.261; persistent signal on an AR(1), seed 3, naive shuffle $p = 0.0002$ against lag shift 0.277; sign flips on the signal days $p = 0.269$ against $t$ 0.258. The homework's planted cases use an irregular signal (runs 15 to 40 days) because a 25-on, 25-off signal repeats under circular shifts: AR(1) seed 6 gives naive 0.0002, shift 0.24; the real edge (seed 4) gives 0.0002 and 0.0005.
- Canvas counts after 1,000 trials (engine streams, confirmed by running `js/engine/sim.js` in Node and on screen): permutation `sim` (seed 11) **101 of 1,000** at or beyond 0.562 (0.101; exact 0.1044); bootstrap `sim` (seed 13) **342 of 1,000** resamples without the 25% month (exact 0.3464), mean of the 1,000 resample means 3.397, SD 2.459 (plug-in 2.555).
- KDE redraw time on a slider move: not measured (no tool reports it); the 60-term curve redraws without visible lag in the playthrough's screenshots.

## Runtime

One statsmodels screen (l13 `rlm_fits`, budget 60000, `how` states 20 to 40 s). Everything else uses NumPy and SciPy. Monte Carlo tests carry a tolerance of 0.02 on $p$; exact cases are enumerated or planted.

## Proposed course.json change

None.

## Backlog

Four bullets under `Raised later (stat-models level 3):` (bars `cut` counts whole bins; no `median` in the sim language; long generated curve formulas and no redraw timing; `fitLabel` placement).

# Problem sets: arma levels 1 to 3 (brief `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/arma/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-arma-numbers.py` (577 of 577 checks, exit 0). The first author was stopped by a restart; the second author judged its drafts, kept the problems and rewrote the weak parts (below), then ran every gate.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-airport-anomaly | 5 (4 / 1) | l3, l2 | 4 |
| problems-1 | p-ppp-screen | 5 (4 / 1) | l3, l4 | 5 |
| problems-1 | p-gdp-trend | 4 (3 / 1) | l4, l2, l1 | 4 |
| problems-1 | p-gold-drift | 4 (3 / 1) | l1, l4 | 3 |
| problems-2 | p-etf-flows | 4 (4 / 0) | l5, l6, l7 | 3 |
| problems-2 | p-vol-index-order | 4 (3 / 1) | l6, l8 | 4 |
| problems-2 | p-peg-fridays | 4 (4 / 0) | l7, l6, l5 | 4 |
| problems-2 | p-freight-ar2 | 4 (3 / 1) | l6, l8 | 5 |
| problems-3 | p-smoothed-fund | 4 (4 / 0) | l9, l11 | 4 |
| problems-3 | p-inflation-arma | 4 (4 / 0) | l10, l11 | 4 |
| problems-3 | p-inventory-half-life | 4 (4 / 0) | l12, l11 | 4 |
| problems-3 | p-dual-listing | 5 (4 / 1) | l10, l12 | 5 |

Typed parts: 14 of 18, 14 of 16, 16 of 17. Every lesson of each level appears; every problem draws on two or more. Skills are the level lessons' own (`ts-stationary`; `ts-acf`, `ts-models`; `ts-models`, `ts-forecast`).

## Gates

1. Number script: 577 of 577, exit 0. Keys exact (fractions) and by a second route (seeded simulation, statsmodels `ArmaProcess`, SciPy tails, least squares, brute search); every `wrong` value recomputed from its slip and shown outside the key band; stated rates of p-ppp-screen re-simulated on 360 months.
2. Validator: 0 errors; 4571 warnings before and after (no warning on these files).
3. Playthrough `--problems arma/problems-<n> --local-cdn <pkgs>`: green desktop and `--mobile`, all three. 440 px part shots read: no overflow.
4. Voice scan 35 on `app/content/courses/arma`: 0 and 0.
5. `grade-all --file` each set: 0 failures (51 widgets).
6. `fresh-check --file` each set: 0 hits (errors); advisories judged below.

## Changes made in this pass

- p-vol-index-order: 600 days became 680 (l7 screens[10] has 600 days and band 0.080). Part 3 was "at least one of 18 bars strays", a retelling of homework-2 items[0]; it now asks for exactly one stray (0.376) against none (0.397).
- Feedback, `why` and `explain` lines rewritten where a word-overlap scan matched course lines: l3 screens[1] (flip, sign, "far enough from 0"), l3 screens[3] and [10] (normal cut-off rejects half the walks), l3 screens[8] (non-rejection), l4 screens[9] (over-differencing), review-1 items[5], l1 screens[3] (telescope), l4 summary, review-2 items[2] generic (Ljung-Box recipe), l8 screens[4] generic, l8 screens[2] (relay), l9 screens[4], review-3 items[5] generic, l10 screens[2], l11 screens[11], l12 screens[2] (flip, word for word), homework-3 items[2].
- Level 3 title "ARMA".

## Freshness: closest course items per problem

| problem | closest lesson screen | closest review | closest homework | why it is not a walk through them |
|---|---|---|---|---|
| p-airport-anomaly | l3 screens[1]: $t$ from a coefficient table | review-1 items[4]: AR(1) variance, $\phi = 0.9$ | homework-1 items[2]: $t$ from $\hat\gamma$ and se | Here $\hat\gamma$ and its se come from raw sums, and the fitted $\phi$ feeds a variance and a normal tail count of days. No item runs sums, test, variance, tail. Weather story new. |
| p-ppp-screen | l3 screens[3] and [8]: 45% of walks below −1.645; power 12% | review-1 items[6]: power 32% and 86% | homework-1 items[6]: difference or not | Those give one test's size or power. This turns size and power into the share of rejections and non-rejections that revert over a 48-series screen, then the cost of differencing the misses. |
| p-gdp-trend | l4 screens[4]: line plus noise, differenced | review-1 items[7]: detrend or difference by ADF | homework-1 items[4]: detrended FTSE residual | Rejects the trend model by comparing its implied growth sd ($\sqrt 2 \times 3.5\%$) with the data, then finds the horizon where the walk's sd passes the trend model's. Neither step is in the course. |
| p-gold-drift | l1 screens[3]: log returns telescope | review-1 items[0]: sum of two log returns | homework-1 items[3]: which series are stationary | Estimates a drift from two closes, tests it, and finds the sample needed for $t = 2$. The lesson checks the identity only. |
| p-etf-flows | l5 screens[2]: $\hat\rho_1 = 15/28$ by hand | review-2 items[2]: $Q(2)$, $n = 50$ | homework-2 items[1]: AR(1) moments function | One-step uses of each, chained to the implied $\rho_2$ against the sample and the one-week forecast-error sd from $\gamma_0$. |
| p-vol-index-order | l8 screens[7]: stray PACF bar at lag 3, AIC and BIC | review-2 items[7]: AIC by order | homework-2 items[0]: at least one of 10 bars | Exactly one stray of 18 (binomial) instead of at least one; BIC gap from two log-likelihoods; 680 days. |
| p-peg-fridays | l7 screens[9]: $\rho_k = \phi^k$ | review-2 items[4]: AR(1) mean | homework-2 items[5]: days for 0.05 to clear the band | Sampling an AR(1) every fifth day: weekly $\phi$, weekly shock variance and the last weekly lag above the band. Not in the course. |
| p-freight-ar2 | l6 screens[3]: $Q(5)$ against $\chi^2_5$; l8 screens[2]: $\rho_2$ against $\rho_1^2$ | review-2 items[2]: $Q(2)$ | homework-2 items[3]: identify, then residual check | The residual degrees of freedom decide the verdict (10.69 between 9.49 and 11.07), then the 2 by 2 Yule-Walker equations are solved by hand for $b_2$ and $b_1$. |
| p-smoothed-fund | l9 screens[10]: overlapping 2-day returns, $\rho_1 = 0.5$ | review-3 items[1]: $\theta$ from $\rho_1 = 0.4$ | homework-3 items[3]: 5-day windows | Unequal appraisal weights, then the conditional half-width once $r_n$ is published and the 12-month sum with covariances. The l9 items stop at $\rho_1$. |
| p-inflation-arma | l11 screens[7]: MA(1) half-width from the last shock | review-3 items[5]: AR(1) 3-day forecast | homework-3 items[8]: ARMA(1, 1) error variance derived | Recovers the shock as last month's miss, applies the MA term once, then the horizon within 0.05 of the mean. Homework-3 derives variances with $\phi = 0.8$, $\theta = -0.4$; the shared formula is the model's standard equation. |
| p-inventory-half-life | l12 screens[2]: half-life at $\phi = 0.8$; l11 screens[11]: 10-day half-width | review-3 items[6]: half-life at 0.7 | homework-3 items[7]: ten-day hold | A dealer's inventory: expected position, its 15-minute half-width and the first minute below 5. Each is a standard task with its own setting; no item chains them. |
| p-dual-listing | l10 screens[6]: BIC of an ARMA(1, 1) | review-3 items[2]: AIC of ARMA(2, 1) | homework-3 items[2]: BIC gap; items[8]: weights $\phi + \theta$ | The impulse path $1.13 \times 0.88^{h-1}$ and its half-life from 1.13 instead of 1 appear nowhere; the BIC step is one standard task. |

Fresh-check advisories (no errors), judged: problems-1 item 2 shares 1.645, 45, 2.87 with l3 screens[3] and review-1 items[2] (the normal and Dickey-Fuller points and l3's taught rate, used as given constants), and 48, 36, 0.98 with two exam items of other topics (unrelated). Problems-2 shares 0.05 and 95 (the band) and 400 with l7 quiz[3] (one sample size). Problems-3 shares the ARMA(1, 1) equation with homework-3 items[8] and constants 0.25, 0.05 with quizzes (stock). Grep of every story noun (airport, gold, GDP, exchange rate, ETF, stablecoin, freight, appraisal, inflation, inventory, dual-listed) across the course folder: none.

## Engine

Two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems arma):`.

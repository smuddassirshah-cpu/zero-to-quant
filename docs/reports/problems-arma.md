# Problem sets: arma levels 1 to 3 (brief `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/arma/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-arma-numbers.py` (605 of 605 checks after the session AF re-author and fix pass, exit 0; 577 before). The first author was stopped by a restart; the second author judged its drafts, kept the problems and rewrote the weak parts (below), then ran every gate.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-airport-anomaly | 5 (4 / 1) | l3, l2 | 4 |
| problems-1 | p-ppp-screen | 5 (4 / 1) | l3, l4 | 5 |
| problems-1 | p-gdp-trend | 4 (3 / 1) | l4, l2, l1 | 4 |
| problems-1 | p-gold-drift | 4 (3 / 1) | l1, l4 | 3 |
| problems-2 | p-etf-flows | 4 (4 / 0) | l5, l6, l7 | 3 |
| problems-2 | p-trust-discount (AF, replaces p-vol-index-order) | 4 (3 / 1) | l8, l7 | 4 |
| problems-2 | p-peg-fridays | 4 (4 / 0) | l7, l6, l5 | 4 |
| problems-2 | p-satellite-stocks (AF, replaces p-freight-ar2) | 4 (4 / 0) | l5, l6, l7 | 5 |
| problems-3 | p-smoothed-fund | 4 (4 / 0) | l9, l11 | 4 |
| problems-3 | p-inflation-arma | 4 (4 / 0) | l10, l11 | 4 |
| problems-3 | p-swap-spread-hold (AF, replaces p-inventory-half-life) | 4 (4 / 0) | l12, l11 | 4 |
| problems-3 | p-dual-listing | 5 (4 / 1) | l10, l12 | 5 |

Typed parts: 14 of 18, 15 of 16, 16 of 17. Every lesson of each level appears; every problem draws on two or more. Skills are the level lessons' own (`ts-stationary`; `ts-acf`, `ts-models`; `ts-models`, `ts-forecast`).

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
| p-peg-fridays | l7 screens[9]: $\rho_k = \phi^k$ | review-2 items[4]: AR(1) mean | homework-2 items[5]: days for 0.05 to clear the band | Sampling an AR(1) every fifth day: weekly $\phi$, weekly shock variance and the last weekly lag above the band. Not in the course. |
| p-smoothed-fund | l9 screens[10]: overlapping 2-day returns, $\rho_1 = 0.5$ | review-3 items[1]: $\theta$ from $\rho_1 = 0.4$ | homework-3 items[3]: 5-day windows | Unequal appraisal weights, then the conditional half-width once $r_n$ is published and the 12-month sum with covariances. The l9 items stop at $\rho_1$. |
| p-inflation-arma | l11 screens[7]: MA(1) half-width from the last shock | review-3 items[5]: AR(1) 3-day forecast | homework-3 items[8]: ARMA(1, 1) error variance derived | Recovers the shock as last month's miss, applies the MA term once, then the horizon within 0.05 of the mean. Homework-3 derives variances with $\phi = 0.8$, $\theta = -0.4$; the shared formula is the model's standard equation. |
| p-dual-listing | l10 screens[6]: BIC of an ARMA(1, 1) | review-3 items[2]: AIC of ARMA(2, 1) | homework-3 items[2]: BIC gap; items[8]: weights $\phi + \theta$ | The impulse path $1.13 \times 0.88^{h-1}$ and its half-life from 1.13 instead of 1 appear nowhere; the BIC step is one standard task. |

Fresh-check advisories (no errors), judged: problems-1 item 2 shares 1.645, 45, 2.87 with l3 screens[3] and review-1 items[2] (the normal and Dickey-Fuller points and l3's taught rate, used as given constants), and 48, 36, 0.98 with two exam items of other topics (unrelated). Problems-2 shares 0.05 and 95 (the band) and 400 with l7 quiz[3] (one sample size). Problems-3 shares the ARMA(1, 1) equation with homework-3 items[8] and constants 0.25, 0.05 with quizzes (stock). Grep of every story noun (airport, gold, GDP, exchange rate, ETF, stablecoin, freight, appraisal, inflation, inventory, dual-listed) across the course folder: none.

## Engine

Two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems arma):`.

## Session AF: re-author and fix pass (`docs/reviews/review-problems-arma-1-3.md`)

Three problems re-authored (findings 8, 11, 14) and thirteen findings applied with the reader's exact text, each number recomputed first; none disputed or deferred. Rows for the removed problems are gone from the freshness table above; the new ones are below.

| problem | closest lesson screens and quiz | closest review, homework | closest exam items | why it is not a walk |
|---|---|---|---|---|
| p-trust-discount | l8 screens[1] (regression rows, newest coefficient), screens[4] and [10] (order from the PACF); l7 quiz[0] ($c/(1 - \phi)$) | review-2 items[4] (AR(1) mean), items[5] (one-step forecast from `const`); homework-2 items[3] (identify an AR) | topic-2.2 items[8] (read ACF and PACF); stage-2 parts[1].items[4] not used | The PACF is read off four regression rows with a trap (week 3's 0.10 in the four-lag row is not the PACF), then an AR(2) mean from its constant, a two-lag one-step forecast and its gap to the one-lag forecast. No item takes an AR(2) mean or forecast, or compares two fits' forecasts. No band, binomial, BIC or Yule-Walker step. |
| p-satellite-stocks | l5 screens[11] (noise on a walk, lag-1 of changes); l6 screens[2] (white noise); l7 screens[9] ($\rho_k = \phi^k$); l9 quiz[3] (booked P&L, level 3) | review-2 items[4]; homework-2 items[1] (AR(1) moments) | topic-2.2 items[5] (AR(1) ACF table); stage-2 parts[1].items[1] (long-run sd) | An AR(1) observed with independent white error, in levels: the estimates' variance, their lag-1 and lag-4 autocorrelations (every lag scaled by $36/48.25$), then $\phi$ recovered from $\hat\rho_4/\hat\rho_1$ by a cube root. No item adds noise to a stationary series or recovers $\phi$ from a ratio of lags. No $Q$ is computed. |
| p-swap-spread-hold | l12 screens[2] (half-life), screens[11] (horizon against half-life); l11 screens[5], [6] (variance sum and its limit), screens[11] (10-day half-width); l7 screens[11] (gap after $h$ days) | review-3 items[4], [6]; homework-3 items[7] (share closed in ten days) | topic-2.2 items[15] (upper end at three days), items[16] | The vendor quotes a half-life and a long-run sd, not $\phi$: the gap is $9 \times 0.5^{20/12}$, the error variance $36(1 - \phi^{40})$ with $\phi^{20}$ from part 1, then the chance a short position is losing at exit and its floor $P(Z > 1.5)$ as the hold grows. No item asks a chance of loss or uses the half-life in place of $\phi$. No $\phi = 0.915$, no shock sd 2.4. |

Coverage after the pass: level 2, l5 (p-etf-flows, p-peg-fridays, p-satellite-stocks), l6 (the same three), l7 (all four), l8 (p-trust-discount); level 3, l12 (p-dual-listing, p-swap-spread-hold). Each problem draws on two or more lessons.

Gates, each edited set: validator 0 errors, 4582 warnings in all; three warnings on the sets, each on a reader's exact replacement (`[key-length]` on p-ppp-screen part 5, `[O2-long-sentence]` on two p-dual-listing lines). Voice scan 35: 0 and 0. `fresh-check --file`: 0 hits on each set (4, 1 and 7 advisories, read: stock constants, the ARMA(1, 1) equation, and 0.05 and 0.08 against l7 screens[10] by chance). `grade-all --file`: 0 failures (18, 16 and 17 widgets). Playthrough `--problems arma/problems-<n> --local-cdn`: green on desktop and `--mobile` for all three; 440 px shots of sets 2 and 3 read, and a stray `\'` in two lines fixed after them. Number scripts: author 605 checks, 0 failures; reader 473 checks, 0 failing (blocks of the three removed problems and the freight exam pairing removed, other checks moved to the new values).

# Report: ito (Brownian Motion and Itô, topic 3.2), level 1 "Brownian motion"

## Files written

All in `app/content/courses/ito/` (nothing else edited except this report and `docs/BACKLOG-INBOX.md`; the validator rewrote `content/manifest.json`). Lesson ids, names, objectives and skills are those of `course.json` (it-bm on all four, it-calculus also on l3).

| File | Screens / items | Quiz | Code screens |
|---|---|---|---|
| `l1-walk-to-bm.json` | 10 screens | 4 | 1: `scaled_walk` + `var_at_one` |
| `l2-normal-increments.json` | 11 screens | 4 | 1: `bm_path` + `increment_cov` (prelude `many_paths`) |
| `l3-quadratic-variation.json` | 11 screens | 4 | 1: `quadratic_variation`, `total_variation`, `qv_table` (prelude: the reference path `W`) |
| `l4-gbm.json` | 11 screens | 4 | 2: `gbm_path` + `prob_below`; `gbm_terminal` |
| `review-1.json` | 9 items, difficulty 2 to 4, two or three per lesson | | |
| `homework-1.json` | 9 items, difficulty 3 to 5 (three at 5) | | 2: `qv_convergence` (d5), `brownian_bridge` (d4); plus an `order` derivation, a `multi`, an `expression` and a 10-point `longform` |

Shape per lesson: hook, explore (a real interactive canvas: `walk` with a `steps` control and `derive` on `step`; `scatter` sim with a `t` control; `series` with a frames control over m; lognormal density with a σ control), name, ladder, trap, derive (`order` with distractors) or generalise, edge case, code, transfer. l1's first screen says topic 3.2 is optional and for derivatives and desk quant roles; Shreve (Stochastic Calculus for Finance II, section 3.2) is named once, in l1. Money is £ throughout.

Interview-style material (as asked): review has $E[W_t^4] = 3t^2$ (expression), $\operatorname{Var}(W_1 + W_2 + W_3) = 14$, $\operatorname{Var}(\int_0^2 W_t\,dt) = 8/3$, "which is a martingale" ($W_t^2 - t$), $\operatorname{Var}(S_1)$ for GBM; homework has the derivation $\operatorname{Var}(\int_0^T W\,dt) = T^3/3$ (`order`), "select every martingale" including $W_t^3 - 3tW_t$ and $e^{W_t - t/2}$ against $W_t^3$, $tW_t$, $e^{W_t}$ (per the interview-plan note for L2), $P(W_1 > 0, W_2 > 0) = 3/8$, $E[W_s^2W_t^2] = 2s^2 + st$ (expression). Each has a worked solution in its explanation (a chain of equalities) and per-distractor lines.

## Validator

PENDING

## Playthrough

PENDING

## Seeds and generators

Generators and helpers in `/tmp/claude-0/-home-user-zero-to-quant/9fb26fd5-8508-5986-8a3a-66bc5f67acde/scratchpad/ito-1/`: `lib.py`, `gen_l1.py` to `gen_l4.py`, `gen_sets.py` (they compute every number in the files with NumPy and write the JSON), `ref.py`, `nums.py`, `nums2.py` (independent checks), `checkcode.mjs` (runs every code widget in Pyodide 0.27.7 under node: the solution must pass every case, the untouched starter must fail at least one), `voice.py` (sentence length, punctuation, spelling scan). The brief's reference script (`.../d67d8e29-.../stage3-briefs/ito.py`) does not exist in this sandbox, so every reference value was recomputed from the brief's definitions; all matched the brief to the stated places.

- Reference path: `np.random.default_rng(3).standard_normal(4096) * sqrt(1/4096)`, cumulated from 0 (l2 code, l3 throughout).
- l1: walk canvases engine seeds 3 and 5 (mulberry32, no number read from them); bars sim seed 21; code `integers(0, 2, n)` on seeds 0 to 5.
- l2: walk seed 6, scatter sims seeds 4 and 9; code `many_paths(10000, 100, 1.0, 7)`.
- l3: transfer uses the first 126 returns of l4's path.
- l4: path `gbm_path(100, 0.08, 0.2, 1, 252, 4)`; trap paths `default_rng(7)` (20 weekly paths, σ = 60%); `gbm_terminal` seed 6.
- Homework: `qv_convergence` seeds 1 (2,000 paths, m = 16 to 1,024) and 7 (3,000 paths); bridge seeds 11, 5, 3 and 0 to 1,999.

## Numbers stated, with sources

Every value below was computed twice: by hand or closed form, and by code (CPython NumPy 2.5.3 in the generators, and Pyodide NumPy via `checkcode.mjs` and the playthrough, which agreed to every stated place); simulated claims were also checked by an independent seeded Monte Carlo (`nums.py`, `nums2.py`).

- l1: endpoint variance $16 \times \frac1{16} = 1$; $c = 1/\sqrt{400} = 0.05$; sd of $W_{0.25}$ = 0.5; $P(W_1 > 1) = 1 - \Phi(1) = 0.1587$; drift edge case $p = 0.525$, mean end $400 \times 0.05 \times 0.05 = 1$; 10-day VaR £2.0m × √10 = £6.32m (6.3246). Code: `scaled_walk(8, 0)` = [0, 0.353553, 0.707107, 1.06066, 0.707107, 0.353553, 0, −0.353553, −0.707107]; `var_at_one(100, 10000, 1)` = 1.005356 (se 0.014), 0.994419 (n = 400, seed 2). Quiz: sd 1; $P(W_4 > 2) = 0.1587$; $n^{0.2}$.
- l2: $\operatorname{Var}(W_3 - W_1) = 2$; $\operatorname{Cov}(W_1, W_3) = 1$; Corr = $1/\sqrt3$ = 0.5774; $\operatorname{Var}(2W_1 - W_2) = 2$ (MC 1.9993); sd of $W_2$ = 1.4142; $\Delta W/\Delta t$ sds 10, 100, 1,000; $X_t = \sqrt t Z$: $\operatorname{Var}(X_2 - X_1) = (\sqrt2 - 1)^2 = 0.17$, $\operatorname{Cov}(X_1, X_2) = \sqrt2$; Corr(5-day, 10-day) = 0.7071. Code: $W_1$ = 0.541651, $W$[10] = −0.017606; covariance at 0.3, 0.7 on seed 7 = 0.3114 (se 0.0055), at 0.5, 1 = 0.5131; small array 1.666667. Quiz: 3, 5, 2, $2W_{t/4}$.
- l3: four-step increments 0.5561, 0.4810, −0.2647, −0.2307, sum of squares 0.6639 (0.6640 unrounded); QV at m = 16, 64, 256, 1,024, 4,096: 0.590845, 0.886817, 0.971822, 1.007951, 1.004400; TV 2.6091, 6.1166, 12.6051, 25.7785, 51.3601 (ratio 1.9924; $\sqrt{2m/\pi}$ = 51.06); sd of QV at 4,096 = $\sqrt{2/4096}$ = 0.0221, at 16 = 0.354; $f = t^2$, m = 100: 1,333,300/10⁸ = 0.0133 (formula $m(2m-1)(2m+1)/3$); $[0.3W]_2 = 0.18$; transfer: first 126 daily log returns of the l4 path, $\sum r^2$ = 0.02036, $\hat\sigma = \sqrt{0.02036/0.5}$ = 0.2018; full year $\sqrt{\sum r^2}$ = 0.1996. Seed-5 check path QV 1.975431. Quiz: 12; cubes; 0.08; $9\,dt$.
- l4: $100e^{0.06}$ = 106.18; $100e^{0.08}$ = 108.33 (108.3287); $100e^{0.1}$ = 110.52 (distractor); $\Phi(-0.3)$ = 0.3821; $\Phi(-0.4)$ = 0.3446; $\Phi(0.1667)$ = 0.5662; $\Phi(-0.1333)$ = 0.4470; median at σ = 10% and 60%: 107.79, 90.48; σ = 0 median 108.33; exact step $100e^{-1.14}$ = 31.98 against Euler −£12; mode $100e^{0.02}$ = 102.02. Code: path end £129.6833, realised volatility (sample sd × √252) 0.1994; `gbm_terminal` seed 6: mean 108.4114, median 106.1293, se 0.2209 (0.37 se from 108.3287). Quiz: 55.81, 61.07, 4.5%.
- Review: $E[W_t^4] = 3t^2$ (MC at t = 2: 11.96 vs 12); VaR 25 days £7.5m; Var sum 14 (MC 13.98); Corr($W_4$, $W_9$) = 0.6667; QV sd 0.1; $P(S_1 > 120) = 1 - \Phi(0.6116)$ = 0.2704 (MC 0.2704); $\operatorname{Var}(S_1) = 12{,}214.03 - 11{,}735.11$ = 478.92 (two closed forms agree; MC 479.1); $\operatorname{Var}(\int_0^2 W\,dt) = 8/3$ = 2.6667 (MC 2.658, 10,000 paths of 400 steps).
- Homework: `qv_convergence` seed 1 sds 0.3456, 0.1750, 0.0864, 0.0438 against $\sqrt{2/m}$ 0.3536, 0.1768, 0.0884, 0.0442; bridge midpoint variance over 2,000 seeds 0.2449 (vs 0.25); $P(W_1 > 0, W_2 > 0) = 3/8$ (MC 0.3754); $E[W_s^2W_t^2] = 2s^2 + st$ (MC at 0.7, 1.9: 2.322 vs 2.31); $P(X_4 < 0) = \Phi(-1) = 0.1587$ (MC 0.1585); realised volatility $\sqrt{0.0144/0.25} = 0.24$; martingale classification checked by regressing the simulated change on $W_s$ (zero for the three martingales, $3W_s$ for $W^3$, $W_s$ for $tW_t$).

## Deviations from the brief

- The brief's reference script was missing (see above); values recomputed.
- Realised volatility: l4 states 0.1994 (sample sd of daily log returns × √252, as the brief). l3's transfer uses the quadratic-variation estimator $\sqrt{\sum r^2 / T}$, which gives 0.1996 for the full year (stated) and 0.2018 for the first half year (the question), so that the $T$ matters.
- l1 and l2 combine the two code functions of each lesson on one screen, and l3 combines three, to stay within 12 screens. l2's `increment_cov` takes an array of paths (one per row) with a provided `many_paths` prelude.
- l4's lognormal pictures use a `plane` with the density formula instead of `distribution` (whose mean marker reads "μ = 108.329", which clashes with the drift μ; backlog bullet).
- Homework `order` item: the brief offers the QV mean and variance or Cov = min(s, t), both already derived in l3 and l2, so the homework derives $\operatorname{Var}(\int_0^T W\,dt) = T^3/3$, which uses Cov = min(s, t) as a step (interview-requested "variance of an integral").
- l3's quiz and review use $(3\,dW + 2\,dt)^2 = 9\,dt$ and the martingale check by independent increments; Itô's lemma itself is left to level 2.

## Proposed course.json changes

None.

# Report: ito (Brownian Motion and Itô, topic 3.2), level 2 "Itô calculus"

## Files written

All in `app/content/courses/ito/`. Ids, names, objectives and skills are those of `course.json` (`it-calculus` on l5 to l7, `it-martingale` and `it-calculus` on l8).

| File | Screens / items | Quiz | Code screens |
|---|---|---|---|
| `l5-integrating-noise.json` | 11 screens | 4 | 2: `ito_sum`, `mid_sum`, `right_sum`; `isometry_check` |
| `l6-ito-lemma.json` | 11 screens | 4 | 1: `ito_drift`, `check_d_s2` |
| `l7-solving-gbm.json` | 11 screens | 4 | 2: `euler_gbm`, `exact_gbm`; `euler_error` |
| `l8-fair-games.json` | 11 screens | 4 | 1: `sample_mean_change`, `exp_martingale_mean` |
| `review-2.json` | 10 items, difficulty 2 to 4 (l5 2, l6 3, l7 2, l8 3) | | |
| `homework-2.json` | 8 items (one with 2 parts), difficulty 3 to 5 (two at 5) | | `ito_vs_strat` (d5), `apply_ito` (d4); `order` + numeric in `h-moment-order`; an `expression`; a 10-point `longform` |

l5 names Shreve once (transfer screen) and opens with the one-sentence note that topic 3.2 is optional. The brief-check items R1 to R4 were applied (see below).

## Validator and playthrough

- `node tools/validate.mjs`: 0 errors; no warnings in the level 2 files.
- Playthrough with `--local-cdn`, desktop and `--mobile` (390 px): l5, l6, l7, l8 (15 checks each, quiz 4/4), `review-2` (recorded 10 of 10) and `homework-2` (marked 8 of 8 right, 39 of 39 marks): all passed. Screenshots checked in the scratchpad `ito-2/fD`, `fM` and earlier folders; faults fixed: an empty `bars` chart on opening (now opens with 1,000 paths), answers leaked by `area` labels (removed), a `walk` y range squashed by 200 steps (fixed range), a wrong KaTeX comma in captions, long starter lines (wrapped to 54 columns).
- `checkcode.mjs` (Pyodide 0.27.7 under node, own folder): every code widget's solution passes all its tests and examples and every untouched starter fails (l5 8/8 and 4/4, l6 8/8, l7 8/8 and 4/4, l8 8/8, homework `ito_vs_strat` 5/5 and `apply_ito` 5/5). Pyodide NumPy matched CPython NumPy 2.5.3 to every stated place.
- Voice: `voice-scan.py` reports 0 sentences over 20 words and 0 explanations over three sentences in the level 2 files (the two over-length sentences it still lists are in level 1).

## Numbers stated, with sources (each computed twice)

Seeded path = `default_rng(3).standard_normal(4096) * sqrt(1/4096)`; GBM path = `default_rng(4).standard_normal(252)`.

- l5: four-step left sum $-0.1853$ (hand 0 + 0.2675 − 0.2745 − 0.1782; code −0.185297); right 0.4787; midpoint $W_1^2/2$ = 0.146693; at 4,096 steps left −0.355507, mid 0.146693, right 0.648893 (= left + 1.004400, checked as `W` identity to 1e-12); Itô $(W_1^2 - 1)/2 = -0.353307$ ($W_1 = 0.541651$); midpoint minus left 0.5022; $E[(\int W\,dW)^2] = 1/2$ (hand $\int t\,dt$, and $\tfrac14\operatorname{Var}(Z^2) = \tfrac12$; simulation 0.4788, se 0.0124, n = 100, 20,000 paths, seed 5; exact at n steps $\tfrac12(1 - 1/n)$); $\operatorname{Var}\int_0^1 t\,dW = 1/3$; midpoint sum squares 0.728 (se 0.017). Quiz: −1, 0.98, 2, 36.
- l6: $W_1^2 - 2\cdot$left = 1.004400; $d(S^2)$ drift at £100 = 2000; $E[S_1^2] = 10^4e^{0.2} = 12{,}214.03$ (also lognormal $e^{2m + 2s^2}$ and simulation 12,210.23, se 16.10, seed 6, 100,000 draws); $d(\ln S)$ drift 0.06; $\sum\Delta S/S$ = 0.2799, $\ln(S_T/S_0)$ = 0.2599 ($S_T$ = 129.6833), gap 0.019935 against 0.02 (also $\tfrac12\sum x^2$ = 0.019929); gamma 0.018762 ($\varphi(0.35)/20$ and finite differences of Black-Scholes, 0.018762017) so $\tfrac12\sigma^2S^2\Gamma$ = 3.7524 a year, 0.0149 a day. Quiz: 24, 0.055, 4465.1, 4.
- l7: $W_1$ = 0.9996, $S_1$ = 129.6833; Euler 129.690755 (gap 0.007491), ordinary-calculus guess 132.3030 (gap 2.6198); Euler end gaps at m = 4, 12, 36, 252: 0.8196, 0.7520, 0.1109, 0.0075; $z$ = 1.0118, $P(S_1 > 130)$ = 0.1558; overstatement $e^{0.02} - 1$ = 2.02%; $\int_0^1(0.1 + 0.2t)^2dt$ = 0.04333; `euler_error` seed 1, 500 paths: 0.1533, 0.0744, 0.0391 at 252, 1,008, 4,032 steps (2,000-path script: ratios 1.98, 1.96); $\Phi(-1.8)$ = 0.0359. Quiz: 0.11, 0.4243, 61.38, 9.42%.
- l8: drift of $W^3$ at $W = 2$ is 6, $e^{W}$ 3.6945; $E[e^{0.5W_2}] = e^{0.25}$ = 1.2840; $E[W_1^3 \mid W_{0.5} = 1]$ = 2.5; $(\mu - r)S$ = 3; stopping at +7 before −3: 0.3 (ruin formula 3/10); forward $100e^{0.05}$ = 105.13; seed 3 changes: $W^2$ 0.9981 (se 0.0045), $W^2 - t$ −0.0019, $e^{W - t/2}$ −0.0005, $e^{W}$ 0.6480 (exact 0.6487); `exp_martingale_mean(0.5, 2, 100000, 7)` = 0.9977 (se 0.0025). Quiz: −3, 6, 2.7183, 0.2.
- review-2: left sum −0.25; $\operatorname{Var}\int_0^3(2 + t)dW$ = 39; −8; $E[S_{1.5}^2]$ = 8166.6; $S_{0.5}$ = £175.62; $P(S_1 < 80)$ = 0.0784; drift 7; stopping 0.25.
- homework-2: `ito_vs_strat(3, [16, 256, 4096])` gaps 0.295422, 0.485911, 0.502200 (half the squared sums); $E[S^3] = 10^6e^{0.36}$ = 1,433,329 (two routes agree); $\operatorname{Var}\int W^2dW$ = 1; $E[W_3^3 \mid W_1 = 2]$ = 20.

## Brief-check items applied

- R1: l5's `bars` screen simulates a path of 256 steps per trial (`sample(m, n(0, 1 / sqrt(m)))`) and uses the telescoping identity, with a switch $c$ from the left sum to the midpoint sum.
- R2: l5's code screen carries a `plane` with the left-point integrand as a `steps` function (15 breakpoints, 16 heights from the seed-3 path) over the path as a polyline function.
- R3: the brief's $d(W^3) = 3W\,dW + 3W\,dt$ is wrong ($3W^2\,dW + 3W\,dt$); l6 asks the $dt$ coefficient of $d(e^{W})$ as an `expression` keyed `\frac{1}{2}e^{w}` (the `e^{...}` form, no `\exp` in the key or the hints). It will grade correctly once the engine fix for P32-expr-exp is in; the playthrough passes it today because it enters the key.
- R4: l8's classification is a `table` with a numeric $dt$-coefficient column at $W_t = 2$ and a text yes or no column (`byKey` keys are cell ids `r{i}c{j}`).

## Departures from the brief

- l5: the right sum is shown in the explore captions and the code tests, and the numeric "right − left" screen was dropped to keep within 12 screens; the transfer asks midpoint minus left (0.5022).
- l6: no `expression` screen for $d(W^3)$ (the brief had a formula error); $d(W^3)$ appears in l8's table. The transfer uses Black-Scholes gamma 0.018762 with the course option.
- l7: the Euler convergence is shown on one seeded path (gaps 0.82 down to 0.0075) and on 500 paths in code, since a single path need not be monotone; a screen shows that Euler already holds the drag through the squared steps.
- l8: the local martingale is named in one sentence without naming Shreve a second time.
- Review has 10 items (brief: 6 to 10); the brief's "at least two code items" for homework is met by `ito_vs_strat` and `apply_ito`.

## Proposed changes outside this level

- `course.json`: the course card line "Needed for strats and desk quant interviews (banks), rarely for trading firms" (not added; l5 states it in the optional-topic sentence).
- Prerequisites beyond `requires` (`ito/L1`, `taylor/L2`, `random-vars/L4`): l5 relies on `integrals` l1 and l2 (Riemann sums); l8 uses `markov` l10 (gambler's ruin and the stopping barriers) and l5 uses `random-vars` l15 (expectation given information, in l8's conditional means). If those lessons sit above `taylor/L2` or `random-vars/L4` in their courses, add them for the mapping agent.

## Seeds and conventions

Generators and checks in the scratchpad `ito-2/` (`lib.py`, `gen_l5.py` to `gen_l8.py`, `gen_sets.py`, `gen_sets2.py`, `nums*.py`, `checkcode.mjs`). Canvas simulations use the engine's seeds (bars seed 3; walks 5, 8, 21), whose values are never typed by the learner. Code: l5 isometry seeds 5, 1, 2, 3; l6 `check_d_s2` seed 6; l7 `euler_error` seeds 1 to 3; l8 seeds 3, 7, 5, 2.

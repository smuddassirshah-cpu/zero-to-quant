# stat-models level 4 (Bayesian models): author report

Session T, content wave 3. Brief: `docs/briefs/stat-models.md`, preamble and `## Level 4`. Base 72e22c8.

## Files written

| File | Screens / items | Quiz | Notes |
|---|---|---|---|
| `l14-conjugate-priors.json` | 11 | 4 | `distribution` beta with controls on fills and prior strength (`derive` on `params.a`, `params.b`), prior overlay, MLE `observed`; drag-the-shade $P(p > 0.25)$; Gamma `plane` stepped by year (`cum[yrs]`); generalise; Gamma-Poisson `order` with the rate distractor; normal-normal with overlays; scale-or-rate trap (each wrong option draws its curve); flat-prior edge case; code `beta_update`, `gamma_update`, `normal_update`, `credible_interval`; daily-update transfer (prior counted twice as a distractor) |
| `l15-posterior-predictive.json` | 10 | 4 | plug-in Binomial(10, $p$) bars on a control against fixed beta-binomial `exact` lines; grouped bars; pmf table; negative binomial; capital-model trap; D3 predictive check (replicate zero-day histogram, `cut` at 28); a check that cannot fail; generalise; code `beta_binomial_pmf`, `predictive_tail`, `ppc_pvalue`; quiet-days transfer |
| `l16-fitting-by-mcmc.json` | 12 | 3 | Beta(15, 35) `plane` with draggable current and proposal points and a live ratio caption; four hand steps in a `table` widget; only ratios matter; log-posterior `order`; MLE against grid; step size; accepted-only trap (console); log densities; code `metropolis` (prescribed stream) and `log_post_logistic` + `fit_bayes_logistic`; plug-in PD; thin-segment transfer |
| `l17-has-it-converged.json` | 11 | 3 | four Gibbs AR(1) chains on a `series` redrawn by `derive` (`ar1`, `rolling` in a `let`) with live $\hat R$; $\hat R$ by hand (`table` widget); AR(1) `order` derivation; ESS; centring console; one-start trend trap with split $\hat R$; one long chain; code `rhat`, `split_rhat`, `ess_ar1`; exit screen `four_chains` + `converged` on centred D1s; validator transfer |
| `l18-hierarchical-models.json` | 11 | 3 | twelve hit rates on a `plane`, raw to shrunk arrows driven by a $\kappa$ control; weight; empirical Bayes; MSE; fund alphas with a $\tau$ control; top-fund trap; one-factor trap; shrinkage-factor `order`; $\hat\tau = 0$ edge case with the full Bayesian version; code `eb_beta_binomial`, `shrink_alphas`; multi-manager transfer (ridge link) |
| `review-4.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | | all five lessons; `r4-boot` recalls level 3's bootstrap against a posterior |
| `homework-4.json` | 8 items, difficulty 3 to 5 (two at 5) | | `h-exit-mcmc` code (difficulty 5, `performance: "code"`, the exit task: `bayes_logistic_with_checks`), `h-nb-derive` order derivation, `h-analyst-errors` longform (10-point rubric, full model answer) |

Skills: l14, l15 `sm-bayes`; l16 `sm-mcmc` + `sm-bayes`; l17 `sm-mcmc`; l18 `sm-hier` + `sm-bayes`. No level-4 objective starts with a verb of the rule, so the level is not rule-matched and the performance task is practice only (it is the topic exit task, so it is marked).

## Gates

1. Validator: **0 errors** (no warnings for L4 files beyond "point hint usually highlights" and "ladder usually reuses the canvas kind", both common in L1 to L3).
2. Voice scan (`VOICE_BASE` the course folder): **0 explanations over three sentences, 0 sentences over 20 words**.
3. Numbers: `python3 docs/reports/stat-models-L4-numbers.py` exits 0: **271 of 271** path checks, 88 two-way agreements, **89 `wrong[]` values outside their answer bands** (rule 581 checked by hand: $|w - a| > \text{tol}_a + \text{tol}_w$), **8 code widgets: every solution passes and every starter fails every hidden test** (local harness mirroring `code.js`).
4. Playthrough: all five lessons, `--set stat-models/review-4`, `--set stat-models/homework-4`, `--mobile --tablet --local-cdn <pkgs>`: see the end of this report.

## Numbers and their sources

Every planner figure was recomputed twice (scipy closed form against two million seeded draws or a grid; two optimisers; a formula against an enumeration). Seeded streams match between CPython NumPy 2.5.3 and Pyodide's NumPy 2.0.2: the 20,000-step D1s chain gave the same means to 1e-12 in both, and the l17 exit test's exact $\hat R$ (1.0007, 1.0004) passed in Pyodide.

- l14: Beta(15, 35), 0.30, 0.325, 0.8, sd 0.0642, mode 0.2917, $(0.1825, 0.4326)$, $P(p > 0.25) = 0.7747$ (draws 0.7753), prior 0.3003; Gamma(17, 6), 2.8333, 0.6872, $(1.6505, 4.3305)$, $5/6$; $N(1.2, 1.7889^2)$, $B = 0.8$, $(-2.306, 4.706)$, 0.7488 (grid 0.7488); 102 and 23 for the wrong scipy calls; flat prior $1/42 = 0.0238$, $P(p > 0.05) = 0.12$; Tuesday Beta(21, 59), 0.2625, double-counted 0.2556.
- l15: pmf as in the brief (formula and `betabinom` agree to 1e-12); mean 3, variance 2.4706, $P(\ge 5) = 0.1702$ (draws 0.1702); plug-in 2.1 and 0.1503; NB mean 2.8333, variance 3.3056, $P(\ge 6) = 0.0829$ (my draws 0.0831, planner 0.0827), Poisson 0.0681; D3 sum 881, Gamma(882, 200.1), mean 4.4078; expected zero days $200(200.1/201.1)^{882} = 2.463$, simulation 2.457; **the largest of 200,000 replicates (seed 3) is 13**, not 14 as the brief allows; no replicate's variance reaches D3's 17.1.
- l16: hand ratios 32.19, 0.4205, 2.2807, 0.01362, chain ends at 0.29 (density, power form and log form agree); 33 defaults; MLE $(-8.048126, 12.828742)$ by IRLS and BFGS; standard errors shown as 1.7795 and 2.7886 (statsmodels' 1.779488 and 2.788630 use the last IRLS weights; the Hessian at the MLE gives 1.779489 and 2.788632); grid posterior mean $(-7.861, 12.537)$, sd $(1.591, 2.492)$, correlation $-0.971$ on two meshes (1,101 by 1,361 and 1,601 by 1,601); chain (seed 1, step 1, 20,000 steps, burn 2,000) $(-7.869, 12.545)$; acceptance on D1s (start $(-8, 12.8)$, seed 1): 0.952, 0.579, 0.351, 0.24, 0.053 for steps 0.05, 0.5, 1.0, 1.5, 5 (**0.952, not the brief's 0.94**: seed-dependent); $(2/\pi)\arctan(2/s)$ 0.4423, 0.7048, 0.2422, my seeded run 0.4439 (planner 0.4408); PD at $L = 0.5$: grid 0.1794, chain 0.1789, plug-in 0.1633. Accepted-only trap (standard normal, step 5, seed 1): sd 1.002 against 1.122, share beyond $\pm 2$ 0.0460 against 0.0698. The log-likelihood at the MLE is about $-22$; **the trap uses $e^{-22}$ and $e^{-2200}$ for 10,000 firms**.
- l17: hand case $W = 5/3$, $B = 8$, 3.25, 1.3964, total-variance check 2.5714; ESS 105.3, 667, 61; inflation 19.5 from 4,000 simulated chains (finite-$n$ exact 18.91; planner 18.7); independent chains (seed 5) 0.999802, shifted 1.305087; trend case (`linspace(0, 3, 1000)` plus noise, seed 3; the brief gave no construction) plain 0.9996, **split 1.2362** (brief 1.1170 from an unstated case); centred grid correlation $-0.750$ (two meshes), MLE $-0.976 \to -0.776$, $\bar L = 0.4534$.
- l18: wins as in the brief; $\hat a = 23.31$, $\hat b = 19.72$ (Nelder-Mead and L-BFGS-B agree to 0.002), 43.02, 0.5417, pooled 0.5501; the twelve shrunk rates as in the brief; weights 0.317 to 0.903; MSE 0.00558 and 0.00272; $\hat\mu = 2.2478$, $\hat\tau = 1.6943$ (Nelder-Mead and a profile over 100,001 values of $\tau$); $B$ from 0.4394 to 0.8970; 3.28 and 3.84; MSE 10.58 and 4.88; seed 101: $\hat\tau \to 0$, $\hat\mu = -0.80$ (equal to the precision-weighted mean).
- Review and homework: each figure is in the script (for example $E[p^3] = 0.03077$ against draws, $\hat R = 1.0607$ from summaries, 94 trades).

Monte Carlo tolerances: l16 rate within 0.02 (about four standard errors at 20,000 steps) and mean within 0.1 (about seven); D1s means within 0.25 (Monte Carlo standard errors near 0.09 and 0.17 from my run's ESS); centred means within 0.25 of $(-2.237, 12.848)$ (MCSE about 0.07 for $\beta_1$); ESS test within 15% of $n/19$.

## Choices and brief errors

- The l17 exit and homework run on **centred** D1s, whose posterior differs from the uncentred one because the $N(0, 10^2)$ prior now sits on the centred intercept: grid means $(-2.237, 12.848)$, not a re-expression of $(-7.861, 12.537)$. The tests compare with the centred grid.
- An isotropic step on the centred posterior (sd 0.58 and 2.60) mixes no better for $\beta_1$ than the uncentred chain (ESS 275 against 240). The lesson therefore uses per-coordinate steps $(0.8, 3.5)$ on the centred model (the sampler's `step * z` takes a vector): ESS 1,264 and 1,255 against 273 and 195 uncentred, split $\hat R$ 1.0020 against 1.0141.
- The l17 `series` caption at $w = 100$: $\hat R = 1.0050$ at $\rho = 0.3$ and **1.2231 at $\rho = 0.97$**; at $w = 200$, 0.9998 and 1.0624 (engine rng, confirmed on the Why? screenshot).
- The l15 hook asks for a plug-in tail with one control, not dragged bars (inbox bullet).
- 20,000-step sampler in Pyodide: **1.6 s** under Node (2.5 s with load); each exit case of four chains of 5,000 is about 2 s. Code cases that run a chain carry `budget: 10000`.

## Proposed course.json change

None.

## Backlog

Six bullets under `Raised later (stat-models level 4):` in `docs/BACKLOG-INBOX.md`.

## Playthrough

One run on the final files covers desktop (1280), `--mobile` (440) and `--tablet` (1032, 1376), with `--local-cdn` set to the scratchpad `pkgs`. **All passed**, no sideways scroll, browser relaunches 0:

- l14 15 checks, quiz 4/4; l15 14 checks, quiz 4/4; l16 15 checks, quiz 3/3; l17 14 checks, quiz 3/3; l18 14 checks, quiz 3/3.
- review-4: 9 of 9 recorded. homework-4: 8 of 8 right, 37 of 37 marks; the performance starter fails; the longform was marked through the button.

I looked at the screenshots and fixed these layout faults:
- a plane x label over the caption (l14);
- spoiler labels on the hand-table canvas, and a six-column table that scrolled at 440 (l16);
- a normal-update display formula wider than the phone column (l14);
- captions that gave away the answer on two l18 screens and on the l14 Gamma ladder;
- a flat replicate histogram (l15, now `yMax`).

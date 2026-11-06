# numerics level 4 (One option, three ways): report

Author: content agent, session T wave 1, 6 Nov 2026. Brief: `docs/briefs/numerics.md` section "Level 4".

## Files

| File | Screens or items | Canvases and widgets of note |
|---|---|---|
| `l13-finite-differences.json` | 10 screens, quiz 3 | `grid` lattice mesh with ordered `tap-regions` (the three nodes an explicit update reads); `plane` with the Black-Scholes curve (`Phi`, param `tau`) and the grid's V(S) as `points` polylines in a `frames` control through τ; one explicit step by hand in a `table` widget; error-across-S curves for ΔS = 2 and 1; stability `frames` through N = 250, 300, 330, 500; trap M = 200, N = 500; code `explicit_bs` + `stable`; transfer on trusting a grid |
| `l14-implicit-and-crank-nicolson.json` | 11 screens, quiz 3 | amplification factors as live curves of ω with a `stops` control on ν and `hlines` at ±1; θ-scheme named; `grid` taps for the three unknowns of an implicit row; Thomas elimination on a 4 by 4 `matrix` driven by `manipulate` (refused row swap and early back-substitution); `order` of the algorithm with a pivoting distractor; implicit and CN error table; gamma ringing trap with `frames` (CN, implicit, two implicit steps first); `expression` derive of CN's factor; code `thomas`; code `theta_bs`; gamma transfer |
| `l15-monte-carlo-error.json` | 10 screens, quiz 3 | `walk` of 2,000 log-price paths (`drawn` 30, `stopAt` 50, overlay `pay`, `showStopped`, derive caption of `stoppedPay` and `stoppedPaySE`); log-log `plane` of s/√n with a `table` widget; slope; cost of a penny; tenfold trap; 95% band with two seeds; monitoring bias table (barrier, Broadie-Glasserman); dimension generalise; code `mc_call` + `paths_for_error`; structurer transfer |
| `l16-control-variates.json` | 12 screens, quiz 3 | three `series` sims (plain, antithetic, control) on a log axis with ±2 SE bands and `hlines` at £10.4506; b* numeric; `order` derivation of b* and Var(Y)(1 − ρ²) with the b = 1 distractor; `expression` for 1/(1 − ρ²); factor 6.88; seeded run; antithetic pairs; geometric Asian control; straddle trap; code `mc_control` + `vrf` + `mc_antithetic`; code `asian_geometric_cv`; machine-time transfer |
| `l17-three-ways.json` | 10 screens, quiz 3 | `console` of the learner's five pricers with a `table` widget for three errors (Gauss-Legendre's is given in the question, so the table fits a phone); `place` matching each method to its error; grid refinement prediction; Monte Carlo band; the tree as a fourth check; the half-year 95 put; strike-off-node trap; validation generalise; code `three_prices`; validation-note `multi` transfer |
| `review-4.json` | 10 items, difficulty 2 to 4, `pass` 0.8 | all five lessons plus `r4-implicit-euler` recalling l12 (tagged `nm-stability`); skills `nm-fd`, `nm-stability`, `nm-mc`, `nm-quadrature` |
| `homework-4.json` | 8 items, difficulty 3 to 5 | numeric weight; `order` derivation of the explicit safe step; `expression` θ-scheme factor; control paths; Broadie-Glasserman shift; Gauss degree; code `price_report` (difficulty 5, `performance: "code"`); longform validation note (10-point rubric, full model) |

Performance task: `h4-price-report` carries `performance: "code"`. The level is not rule-matched (objectives start Replace, Compare, Estimate, Cut, Price), so it is practice only and never gates met.

## Gates (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warning on any level 4 file.
2. Voice scan, `VOICE_BASE=app/content/courses/numerics/`: 0 sentences over 20 words, 0 explanations over three sentences (all four levels).
3. `python3 docs/reports/numerics-L4-numbers.py`: exits 0: 213 of 213 numbers_lib checks at their JSON paths, and 0 failures among the second-method checks. It also runs every code widget's hidden tests in CPython: all 8 solutions pass, all 8 starters fail one.
4. Playthrough with `--local-cdn`: all seven files pass on desktop and with `--mobile --tablet`. Lessons 13, 14, 13, 15 and 13 checks, quizzes all right; review 10 of 10; homework 8 of 8 (37 of 37 marks), the performance starter fails, the longform marked by the button.

SciPy: no level 4 code imports SciPy; every solver is pure NumPy, as the brief prefers. Measured for the record in node Pyodide: `import scipy.linalg, scipy.stats` takes 3.8 s after the wheels are fetched. Times in node Pyodide: `theta_bs` 0.13 s at M = 400, N = 200 and 0.72 s at M = 800, N = 400; `three_prices` 0.29 s; `price_report` on the put 0.55 s.

## Numbers and their sources

Every option price is computed twice: by the closed form (Black-Scholes by `math.erf`, checked against `quad` over the density) and by the method. Seeded values were computed in node Pyodide 0.27.7 (NumPy 2.0.2) and in CPython (NumPy 2.5.3); they agree to 1e-14. The numbers script recomputes them in CPython.

- Standard call £10.450584 (10.450583572186), d1 = 0.35, gamma 0.018762.
- l13: a = 0.0975, 1 + b = 0.7999, c = 0.1025, V50 = 0.2050 (weights sum 0.9999); explicit £10.442791 (−0.0078); ΔS = 1, N = 1,700: £10.4487 (−0.0019, ratio 4.2); bound N ≥ 401 (400.05); N = 300: 379,169; N = 250: 4.5 × 10^30; N = 330: £10.4439 with grid maximum 7.5 × 10^14; M = 200, N = 500: 4.1 × 10^277, bound 1,601; M = 300: 3,601; M = 50: 101; share (K = 0) exact; forward error 2.4 × 10^-4, halving with N.
- l14: ν = 20 CN factor −0.951; ν = 80 −0.9876 (88% left after ten steps); implicit errors −0.0519, −0.0309, −0.0204 and CN −0.00950, −0.00980, −0.00987 (M = 100, N = 25, 50, 100); CN −0.00246, −0.000616 (ratio 4.0); implicit less space error −0.042, −0.021, −0.0105; M = 400, N = 10: CN £10.2767, gamma 1.2526 (66.8 times 0.018762); implicit £10.3457, gamma 0.01957; two implicit steps £10.4324 (10.432399), gamma 0.01904; ν ≤ 0.4 prices 10.4428, 10.4386, 10.4407; pivots 2, 1.5, 1.33, 1.25. Implicit and CN are recomputed by `scipy.linalg.solve_banded` against the lessons' Thomas.
- l15: s = 14.7194 by closed form and by `quad`; SEs 1.472, 0.465, 0.147, 0.0465; 2,166,609 paths for £0.01; plain seed 0 £10.4362 (SE 0.0465, −0.31 SE), seed 1 £10.3578 (SE 0.0464, −2.00 SE, its interval misses); lower end 10.3450; down-and-out £8.6655 (closed form and `quad` over the killed density); monitored 9.572, 9.152, 8.936 (SE 0.033, 200,000 paths, seed 0), shifted 9.580, 9.174, 8.914; walk caption SE about £0.324 (seed 5, by a Python copy of walk.js's mulberry32 stream).
- l16: Var(Y) 216.66, Var(X) 408.11, Cov 274.91 (closed forms and `quad`), ρ = 0.92450, b* = 0.6736, b̂ = 0.67307 (seed 0), factor 6.88, 315,000 paths, residual 31.48 (b = 1 gives 74.95); seeded control £10.4484 (SE 0.0178), ratio squared 6.86; antithetic correlation −0.501, 54.06 against 108.33, seed 0 £10.4721 (SE 0.0329), both 30.67; geometric Asian £5.9402 (closed form, and the simulated geometric mean within 3 SE); control £6.1561 (SE 0.00075), plain £6.1722 (SE 0.0269), seed 1 £6.1558 (SE 0.00074), factor 1,281 (about 1,300); straddle £16.0241, correlation +0.645, 144.0 against 87.6, efficiency 0.61; put b̂ = −0.292.
- l17: CN £10.449920 (−6.6 × 10^-4), Gauss-Legendre £10.450583572185 (−2.6 × 10^-13), Monte Carlo £10.4484 (SE 0.0178, −0.12 SE; seed 1 £10.4275, −1.30 SE), tree 500 £10.446585 (−0.0040), 1,000 −0.0020, 1,001 +0.0018, 2,000 −0.0010; CN refinement −2.65 × 10^-3, −6.64 × 10^-4, −1.66 × 10^-4, −4.15 × 10^-5; put £5.170209, CN £5.169608, Gauss £5.170208971851, Monte Carlo £5.1672 (SE 0.0181, −0.17 SE), tree 1,000 £5.170502; off-node strike (S_max = 300) M = 390 −1.51 × 10^-3, 400 +9.1 × 10^-4, 420 −1.31 × 10^-3.
- Review and homework: N ≥ 901 at M = 150; ΔS = 0.5 predicted −0.00049, grid −0.00045 at N = 6,401; CN factor −0.980 at ν = 50; 640,000 paths; factor 10.26 at ρ = 0.95; implicit Euler 0.0244; centre weight 0.4879 at j = 80 (0.2158 at j = 99, 0.0198 at N = 400, negative below N = 393); 39,600 paths at ρ = 0.98; shifted daily barrier £89.34; degree 63; `price_report` on the put: grid M = 320, error −9.4 × 10^-4 with an honest estimate, 16 nodes, 2,560,000 paths, SE £0.0036.

Tolerances in code tests: grid prices 1e-6, quadrature 1e-10 against Black-Scholes, seeded Monte Carlo 1e-8 (exact stream), Thomas against `np.linalg.solve` 1e-10, Asian control SE below £0.002 and within 3 SE of £6.156 for seeds 0 and 1 (not pinned to one path layout), `price_report` within tol (3 SE for Monte Carlo).

## Brief errors and choices that differ from the brief

- Forward edge case: the explicit grid does not reproduce a forward exactly. Its space error is 0, but the Euler time step leaves 2.4 × 10^-4, halving with N. The share (a call struck at 0) is exact, so it is the edge case and a hidden test; the forward is stated with its time error.
- "Each coefficient must be non-negative": a_1 = ½Δτ(σ² − r) is negative at j = 1 for σ = 20%, r = 5%, at any step. The lessons state the condition on the centre weight 1 + b_j, with j = M as a safe bound (N ≥ 401). The homework derivation notes that a_1 multiplies V_0 = 0. The exact interior limit (j = M − 1) is N ≥ 393, stated once in a homework explanation.
- `paths_for_error(14.7194, 0.01)` is 2,166,608. The brief's 2,166,609 comes from the unrounded s = 14.719404; the lesson states 2,166,609 for the unrounded s and the hidden test expects 2,166,608 for 14.7194.
- Off-node strike: doubling M from 400 keeps the strike a third of the way between nodes, and the error ratio stays near 4. The broken pattern shows across neighbouring M instead (390, 400, 420), which is what the trap uses.
- Barrier figures 9.572 and 9.152 reproduce only when the normals are drawn step by step (shape steps by paths); the Asian figures use shape paths by steps, as the code screen does. Neither is a test.
- The brief uses θ for both the frequency and the scheme weight. The lessons write the frequency as ω.
- The Asian factor: 1/(1 − 0.9996²) = 1,250; the SEs give 1,281. Both are "about 1,300".
- Homework `price_report`: with S_max = 2K, the 120 call's S0 is off the grid and the refinement estimate understated the error (0.0011 against 0.0044). The settings are S_max = 2·S0 from M = 40, N = 20, so S0 and both test strikes are nodes; the estimate is the last difference over 3.
- The walk explore asks for the caption's standard error with a tolerance of £0.03 around £0.33 (the stream gives £0.324).
- Ladder counts: l16 has four ladders and 12 screens.
- Layout fixes from the phone screenshots: l14's Thomas states show short pivot formulas (a sentence overflowed at 440 px), l14's explore opens at ν = 0.6 so the curve labels sit on their curves, and l17's hook table lost its Gauss row.

## Dependence on odes level 4 (recheck after merge)

- l13's transfer says the grid is trusted once it reproduces the closed form, "the habit of `odes` l18". Recheck that wording against the merged odes L4 text.
- Stability factors and stiffness are cited from this course's l12, not from odes, so nothing else assumes odes L4 lesson text.

## Proposed course.json change

None.

## Seeds and conventions

NumPy `default_rng(seed)`, every normal in one call. Seed 0 is the headline run and seed 1 the second check. Engine canvases: walk seed 5, series seed 11 (the engine stream, captions quote limits only). Generators and helpers are in the scratchpad folder `numerics-4`.

# numerics level 3 (Integrals and time steps): report

Author: content agent, 6 Nov 2026. Brief: `docs/briefs/numerics.md` section "Level 3".

## Files

| File | Screens or items | Canvases and widgets of note |
|---|---|---|
| `l9-quadrature.json` | 10 screens, quiz 3 | `riemann` trapezium with a `stops` control on `riemann.n` and a live `sum` caption; ratio and order table; Simpson parabolas as one `floor` curve formula with a live caption; error-formula prediction; Richardson as an `expression` derive; log10 plot of both rules; kink trap on the payoff × density; cubic edge case; code `trapezium` + `simpson` + `observed_order` + `richardson`; strike-grid transfer |
| `l10-gaussian-quadrature.json` | 10 screens, quiz 3 | two mirrored nodes dragged until x² is exact (`drag-point`, derived mirror and caption); x⁴ and x⁶ checks; `order` change of interval with a distractor; split call price and the tail at z = 8; unsplit-kink trap; polynomial edge case; code `gl_integrate` + `gl_call_price` + `gl_put_price`; quadrature-pricing transfer |
| `l11-step-size.json` | 10 screens, quiz 3 | CIR B(5) errors on a log10 plot (slope table); local against global error; explore with a slider on n and the predicted error against a 10^-8 line; Richardson error estimate; adaptive controller's 38 accepted steps drawn on y = 1/(1 − t); `expression` for the step update; budgeting trap; code `steps_for_tol` + `adaptive_rk4` (prelude gives `rk4` and `euler`); logging transfer |
| `l12-stiff-equations.json` | 10 screens, quiz 3 | two-speed rate model with Euler's path as an exact formula and a `stops` control on h; stability limit; implicit Euler path; stability regions as `implicit` curves (RK4 boundary expanded by hand) with a draggable hλ and four live factors, graded by a `multi`; trapezoidal ringing trap; h = 0.02 edge case; code `implicit_euler_linear` + `trapezoidal_linear`; code `compare_solvers` with `solve_ivp`; finite-difference stiffness transfer |
| `review-3.json` | 10 items, difficulty 2 to 4 | all four lessons, plus `r3-tiny-step` recalling level 1's rounding floor (tagged `nm-float`) |
| `homework-3.json` | 8 items, difficulty 3 to 5 | code `price_by_quadrature` (difficulty 5: call, put, call spread, digital, forward, a kink beyond z = 8); `expression` derivation of 1/(1 − hλ); `order` proof that Simpson is exact for cubics; longform on the stiff Euler run (10-point rubric, full model) |

No performance task: the objectives start with Integrate, Price, Measure and See, so the verb rule does not match.

## Gates (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warning on any level 3 file.
2. Voice scan with `VOICE_BASE` on the course folder: 0 sentences over 20 words, 0 explanations over three sentences (all three levels).
3. `python3 docs/reports/numerics-L3-numbers.py`: exits 0. Every code widget's solution passes its tests in CPython, and every starter fails one.
4. Playthrough with `--local-cdn`: all six files pass without flags and with `--mobile --tablet`. The lessons have 13, 12, 12 and 12 checks, with quizzes all right. Review 10 of 10; homework 8 of 8 (38 of 38 marks), with the longform marked by the button.

SciPy: only `compare_solvers` (l12) imports SciPy. In node Pyodide, after the wheels were fetched, `import scipy.integrate` took 2.1 s. The `how` says about 2 s once downloaded. In the desktop playthrough the whole l12 lesson took 10.6 s.

`closure.mjs --target pdes/L3` now reaches numerics only at level 4. odes (levels 1 to 4) and complex (level 1) are written elsewhere in this wave.

## Numbers and their sources

Each figure was computed in CPython, then recomputed in the numbers script by a second route. The rules were checked against `quad` and mpmath, the CIR closed form against `solve_ivp` at rtol 1e-12, and the two-speed model against `expm` and step loops.

- l9: trapezium errors 0.0357, 0.00894, 0.00224, 0.000559 (ratios 3.99 to 4.00); Simpson 5.79e-4, 3.70e-5, 2.33e-6, 1.46e-7 (ratios 15.6, 15.9, 16.0; log-log slope −3.98); predicted 0.00895; (4T8 − T4)/3 = S8 = 1.7182841547; z* = −0.15; Simpson with the kink 0.600, 0.116, 0.0108, −0.00644 (n = 16 to 128); split 9.26e-3, 5.10e-4, 3.10e-5, 1.93e-6; quiz S4 = 1.7183188, n = 64 for 10^-9.
- l10: 1/√3 = 0.57735; x⁴ by two nodes 0.2222 against 0.4; √0.6 = 0.774597, weights 8/9 and 5/9; x⁶ by three nodes 0.24 against 2/7; Gauss split errors −1.32e-3, −2.0e-9, −2.6e-13 (8, 16, 32 nodes); tail beyond z = 8 is 2.5e-13 (mpmath); unsplit 3.90, 0.927, 0.120, −0.036; truncation in S −0.0483, −9.2e-6, −1.8e-9 for tops 200, 300, 400, the same at 64 and 128 nodes; polynomial payoff 10/3; put £5.573526; K = 200 call £0.004799.
- l11: γ = 0.519615, B(5) = 1.812959, A(5) = 0.881920, price £79.1020; Euler errors 0.0964, 0.0493, 0.0247, 0.0124 (slope −0.99); RK4 3.49e-4, 1.75e-5, 9.84e-7, 5.83e-8 (slope −4.18); C = 2.81e-4, h = 0.0773, n = 65, error 8.2e-9; Richardson (y10 − y20)/15 = −1.10e-6 against the true −9.84e-7. The brief's "at n = 20" is read as the estimate for the n = 20 value from runs at 10 and 20. Adaptive: 38 accepted, 1 rejected, 468 evaluations, first accepted step 0.069 (the brief said 0.070), smallest 0.0022 (the brief said 0.0021; the value is 0.002152), final relative error 2.4e-8. This needs the controller to keep the extrapolated value y(h/2) + (y(h/2) − y(h))/15, as the lesson states. Without extrapolation the end error is 2.0e-6. Fixed RK4 at 400 steps: 7.0e-8. RK45 at rtol 1e-8 took 320 evaluations and 29 steps in Pyodide's SciPy 1.14.1, and the same in CPython's 1.18.1. The brief quoted 296 and 49; no lesson states this count.
- l12: A = 0.020202, B = −0.030202, r(1) = 5.2253% (matches `expm`); Euler r(1) 5.2238% (h = 0.01), 5.2222% (0.02), 8.24% (0.04), −10,038% (0.05), −3,166,906% (0.1); limit h < 0.04; implicit Euler path 5.5720%, 5.5796%, 5.4176%, 5.2611%, fast factor 1/13.5 = 0.0741; trapezoidal factor −0.7241, path 7.9696%, 3.9891%, 6.5346%, 4.3941% against 5.7828%, 5.5733%, 5.3885%, 5.2253%; trapezoidal r(1) at h = 0.05 is 0.0522528; factors at z = −2.5: Euler 1.5, implicit 0.286, trapezoidal 0.111, RK4 0.648; RK4 limit −2.7853; solve_ivp evaluations RK45 1,172, Radau 422, BDF 226 (Pyodide and CPython agree).
- Review and homework: RK4 halving 3.2e-6 to 2e-7; 32 steps for C = 1e-3, tol 1e-9; Euler limit 0.02 for λ = −100; trapezoidal factor −0.905 at hλ = −40; trapezium n = 128 for 10^-4 from 0.02 at n = 8; 4 Gauss nodes for degree 7; RK4 limit 0.0557 at λ = −50; step update 0.0045; spread £4.410495, digital £0.532325, forward £4.877058; 1.5^20 ≈ 3,300.

Tolerances in code tests: quadrature tables 1e-12, the split call 2e-6, Gauss prices 1e-8 (a forward on one long piece needs 48 nodes; 24 left 5.6e-6), steps exact, adaptive value 1e-6 relative with 30 to 45 accepted steps, implicit steppers 1e-6, `solve_ivp` answers 1e-6 with only a ratio test on evaluation counts.

## Choices that differ from the brief

- The log-log pictures plot log10 values on linear axes (level 1 Backlog).
- Euler, implicit Euler and trapezoidal paths are exact curve formulas per mode. The implicit and trapezoidal paths join grid values linearly; Euler's uses its own step slope.
- The homework longform uses steps of 0.05 years, which give −100.38. Weekly steps (h = 1/52) are stable here, so the brief's "weekly" would not blow up.

## Proposed course.json change

None.

## Seeds and conventions

No random numbers. Rates in per cent on canvases and as decimals in code. Generators are in the scratchpad folder `numerics-L3`.

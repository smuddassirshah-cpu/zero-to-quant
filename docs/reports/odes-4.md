# odes level 4: Transforms and numerical solution

Author: content agent, session T wave 1. Brief: `docs/briefs/odes.md` `## Level 4` (binding). Base commit 37c0724.

## Files

| file | screens / items | quiz | notes |
|---|---|---|---|
| `l14-laplace-transform.json` | 11 screens | 4 | perpetuity area with a rate slider (`area` + `values.A` caption); $\mathcal{L}\{e^{at}\}$, $\mathcal{L}\{t\}$ by parts, table widget for $t^2$, $\sin 3t$, $\cos 2t$; Gordon trap with a rate slider into divergence; $e^{t^2}$ edge case; $\mathcal{L}\{f'\}$ as an `order` derivation with a distractor; transform table and shift rule; `code` `laplace_numeric` (trapezium written out) and `pv_growing` (raises `ValueError`); default-claim transfer £33.33 |
| `l15-solving-with-laplace.json` | 10 screens | 4 | `manipulate` hook with refused steps and a slope field; Vasicek drift by Laplace; cover-up table on the $s$-plane poles; complex poles $-1 \pm 2i$; trap: dropping starting values gives $y = 0$; repeated pole $te^{-t}$; `code` `residues` and `inverse_laplace`; floating-leg transfer $R(0.05) = £0.8364$ |
| `l16-euler-method.json` | 10 screens | 4 | hand steps in a table; closed-form Euler polygon with a step slider; monthly compounding; log-log error chart; Vasicek quarterly and monthly; Euler round the centre (polyline); stiff trap on a `series`; stability rule $h < 2/\lambda$; `code` `euler` and `observed_order`; loan-schedule transfer |
| `l17-runge-kutta.json` | 12 screens | 4 | midpoint hook with segments; RK4 and Euler polygons with a step slider; four slopes by hand; order chart ($\log_{10}$ error); cost chart; RK4 round the centre; trap: tap the `k1`-for-`k2` line in a console; RK4 stability limit; `code` `rk4_step`/`rk4`; `code` `solve_ivp` against the closed form; scheme-choice transfer |
| `l18-four-decimal-places.json` | 12 screens | 4 | bond price as the area under $r$; closed form; Euler $D_n$ by formula with an $n$ slider; search for 163; RK4 table; coarse-luck chart; monthly-Euler trap; convexity edge case with a draggable $\sigma$; convergence check as an `order`; `code` bond functions and `steps_to_4dp` (`rk4`, `discount_euler` in a prelude); `code` `solve_ivp`; desk-habit transfer |
| `review-4.json` | 10 items | | `pass: 0.8`; difficulty 2 to 4; two items per lesson; `r-system-step` recalls level 3 (eigen l14's matrix, fastest eigenvalue limits Euler's step) |
| `homework-4.json` | 8 items | | difficulty 3 to 5; `h-match-4dp` is the performance task (`code`, difficulty 5, 7 tests, 1 example: `rk4` and `match_to_4dp`); `h-solve-order` order derivation; `h-monthly-note` longform, 10-point rubric, full model |

Performance task: rule-matched (l17's objective starts "Implement"), so `h-match-4dp` carries `"performance": "code"`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warning on any level 4 file.
2. Voice scan, `VOICE_BASE=app/content/courses/odes`: 0 explanations over three sentences, 0 sentences over 20 words.
3. `python3 docs/reports/odes-L4-numbers.py`: 291 of 291 numbers_lib checks, 0 route disagreements, exit 0.
4. Playthrough with `--local-cdn`: all five lessons, review-4 and homework-4 green on desktop and with `--mobile --tablet` (440, 1032, 1376); l16 and l18 replayed green with and without `--mobile` after a last caption and wrap fix. Screenshots at every width were looked at; fixes made: pole labels off the axis, explicit curve colours, $\log_{10}$ error charts with the x axis at the bottom. Homework: "1 performance starter fail". Every code solution passes its tests and every starter fails in CPython too (`codecheck.py` in the scratchpad).

## Numbers

All from the script (route 1 closed form or exact arithmetic; route 2 SciPy `quad`/`solve_ivp`, a brute-force step loop, `np.roots`, or RK4 as the matrix polynomial $P(h\mathbf{A})$). The brief's planner values all reproduced: £25, 0.25, 2, 0.3, 0.2, £125, £33.33, 1.7293, 0.399576, residues 1, $-2$, 1 and $0.5 \mp 0.25i$, 0.014164, 0.052131, 1.051162, 1.051271, 0.124539, 0.064984, 0.013468, 1.92, 0.964, 5.1724%, 5.2001%, 1.3681, 5.0625, 2.714081, 0.004201, 1.1051708333, 2.7182797, $2.084 \times 10^{-6}$, 15.35, $1.36 \times 10^{-5}$, 0.9999996, 1.375, 0.6484, 2.7853, 7 RK4 steps, 1.835830, 0.236717, 0.789215, 0.788402, 0.789134, 0.789207, 163, 0.789229, 0.00062 and 0.00196, 0.789080, 0.789581. Computed and reported: buggy RK4 ($k_1$ in $k_3$) order 1.98, value 2.71613; RK4 10-step bond error $2.6 \times 10^{-7}$; `steps_to_4dp` gives 4 (RK4) and 256 (Euler, doubling); `match_to_4dp` gives 8 (bond as $(r, D)$), 16 (oscillator), 16 ($y' = y$); Euler needs 16,019 steps on the oscillator; noisy price £0.0367 higher; loan schedule £93,832.22 against £93,816.35.

Pyodide against CPython: Pyodide 0.27.7 (NumPy 2.0.2, SciPy 1.14.1) gave the same trapezium values (0.5000000104, 0.2499999948, 0.2999999844) and the bond `solve_ivp` error $1.78 \times 10^{-12}$ as CPython (NumPy 2.5.3, SciPy 1.18.1). The oscillator `solve_ivp` error is $7.7 \times 10^{-12}$ in Pyodide against $7 \times 10^{-14}$ in CPython; tests use `abs` 1e-8. SciPy load, measured by loading Pyodide from the local CDN folder in Node: NumPy 0.6 s, SciPy 1.5 s; the `how` lines say about 2 s from a local cache, 5 to 20 s over a home connection.

## Brief errors found

- "The moment generating function of `random-vars`": `random-vars` has no MGF lesson; it is `limits-thm` l19 (generating functions). l14 cites that.
- l16 transfer: the monthly schedule for lesson 1's loan differs from l3's formula by £15.87 after a year, not "in the pennies". Stated as £15.87.
- Homework: "RK4 needs 7" holds for the closed form alone; a doubling check that also needs two runs to agree stops at 16. The item says so.
- The critical-damping claim is not used; level 4 does not refer to damping.

## For numerics (L3 requires odes/L4)

Taught plainly: Euler $y_{n+1} = y_n + hf(t_n, y_n)$, global error proportional to $h$; on $y' = -\lambda y$ the factor $1 - h\lambda$, stable for $h < 2/\lambda$ ($h = 1/\lambda$ jumps to 0); "stiff" is only named, with a pointer to numerics l12; for a system the fastest eigenvalue limits $h$. Midpoint method (second order). RK4 with $k_1..k_4$, fourth order (ratio 15.35), four evaluations a step, stability on the real axis $h\lambda < 2.7853$. `solve_ivp` (RK45, `rtol`, `atol`) used only as a checked tool; adaptive step control is left to numerics l11. Four decimals means $|err| < 5 \times 10^{-5}$; convergence is checked by doubling until two runs agree and match a closed form. Python names: `euler(f, t0, y0, h, n)` and `rk4(f, t0, y0, h, n)` return arrays `t`, `y`; `rk4_step(f, t, y, h)`, `observed_order(errors, hs)`. Laplace: definition, table, shift and derivative rules, partial fractions by cover-up and by $\text{num}(p)/\text{den}'(p)$.

## Proposed course.json change

None. Note: AUTHORING section 11 advises 12 or more review items for a level others require (numerics L3 requires odes/L4), so a 6-item test-out repeats; the binding brief caps the review at 10.

## Backlog

Six bullets in `docs/BACKLOG-INBOX.md` under "Raised later (odes level 4)".

## Conventions

No seeds or data files. Scratch generators and checks in the scratchpad folder `odes-4`.

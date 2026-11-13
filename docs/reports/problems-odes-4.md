# Problem set: odes, level 4 (brief `docs/briefs/chained.md`)

File: `app/content/courses/odes/problems-4.json` (3 problems, 15 parts, 40 minutes). Levels 1 to 3 belong to another agent, whose report is `problems-odes.md`; this report and `docs/reports/problems-odes-4-numbers.py` cover level 4 only.

## Set

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-test-rig | 5 (2 / 3 / 0) | l14 (transform of $8e^{-3t}$ by table and definition), l15 (transform the IVP, cover-up, invert) | 4 |
| problems-4 | p-skydiver-check | 5 (4 / 1 / 0) | l15 (closed form by Laplace), l16 (Euler), l17 (one RK4 step, order 4), l18 (four-decimal match as $n$ doubles) | 5 |
| problems-4 | p-dose-simulator | 5 (5 / 0 / 0) | l16 (Euler factor and stability limit), l17 (RK4 limit, cost of four slopes a step) | 4 |

Typed parts 15 of 15; no choice part. Every numeric part states its form (whole number, exact value, exact fraction or decimal to 4 places, 2 or 4 decimal places, two numbers separated by a comma).

Chains. Rig: $\mathcal{L}\{8e^{-3t}\} = \tfrac{8}{s + 3}$, $Y = \tfrac{8}{(s + 2)(s + 3)(s + 4)}$, residue $-8$ at $-3$, $y = 4e^{-2t} - 8e^{-3t} + 4e^{-4t} = 4e^{-2t}(1 - e^{-t})^2$, peak 0.25 cm at $t = \ln 2$. Skydiver: $V = \tfrac{9.8}{s(s + 0.2)}$, $v(2) = 49(1 - e^{-0.4}) = 16.1543$, Euler $h = 1$ gives 17.64, one RK4 step gives 16.1504 (error 0.0039), first $n$ in 1, 2, 4, 8 predicted inside $5 \times 10^{-5}$ is 4 (run: errors 0.000207 and 0.0000119, so 4 again). Dose: eigenvalues $-6$ and $-0.5$, Euler factor $-2$ at $h = 0.5$, Euler limit $\tfrac13$ h, RK4 limit 0.4642 h, cheapest stable run over 24 h is Euler with 73 slope readings (RK4 needs 52 steps, 208 readings). Each later part restates the value it uses.

Slips with lines (each checked in the script): forcing sign and the dropped 8; the carried $\tfrac{8}{s - 3}$; roots of $s^2 + 6s + 8$ with the wrong signs; residue sign and another pole's residue; $-p$ in the exponent; $\tfrac1{16}$ without the 4, the peak time, $y(1)$; the constant 9.8 not transformed, drag sign, cover-up not divided by 0.2, the two carried closed forms; one slope for both Euler steps; RK4 as a plain mean and without $h$; first-order halving (128) and the $5 \times 10^{-4}$ band (2); positive eigenvalues, $|{-2}|$, the slow mode's factor and limits, $6h < 1$, Euler's limit for RK4, $n = 72$ at the edge, RK4's 208 readings and its 52 steps.

Judgement calls a reader may question:
- `p-test-rig` part 5 asks for a maximum, found by calculus with $u = e^{-t}$ (a prerequisite, not a level-4 idea); the question names the substitution.
- `p-skydiver-check` part 5 asks for a prediction from the order, as review-4 does; the feedback also gives the true errors, which pick the same $n$.
- `p-dose-simulator` part 1 (eigenvalues of a triangular matrix) is level-3 work used as the first step. Part 5 concludes that Euler is cheaper when only stability matters; the explanation says RK4 earns its cost on accuracy.

## Checks

1. `docs/reports/problems-odes-4-numbers.py` with the scratchpad venv: exit 0, 104 checks, 0 failures. Route 1 exact (sympy `laplace_transform`, `apart`, `limit` for residues, `dsolve` with the starting values, exact Euler and RK4 slopes as fractions, exact stability limit); route 2 another method (quadrature of the transform, `solve_ivp`, a grid search for the peak, direct Euler and RK4 stepping, a scan of $|R(z)| < 1$ for the RK4 edge 2.7853, the fast mode's growth over 24 h for each step count). Every `wrong` value rebuilt from its slip and shown outside the key band; all 15 stored keys read back from the JSON.
2. Validator: 0 errors, no warning on the file (one `[wrong-band]` fixed by asking for the exact factor in `p-dose-simulator` part 2).
3. Playthrough `--problems odes/problems-4 --local-cdn <pkgs>`: green on desktop and with `--mobile`. Shots at 440 px read: the fractions in Laplace parts and the RK4 slopes set cleanly, no overflow.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all.mjs --file problems-4.json --local-cdn`: 15 widgets, 0 failures. `fresh-check --file`: 0 hits, no advisory.

## Freshness

Level 4 settings read first (l14 to l18, review-4, homework-4) and avoided: perpetuities and the Gordon model, a default claim, the Vasicek drift and bond, the loan schedule, Euler as compounding, $y' = y$ and $y' = -10y$, the centre $x' = y$, $y' = -x$, the oscillator $y'' + 2y' + 5y$, $y' + 2y = 4$, $y'' + 3y' + 2y = 2$, a fast-reverting spread, a two-factor rate model, eigen lesson 14's matrix.

Grep per problem (course folder, then `app/content`):
- `p-test-rig`: $y'' + 6y' + 8y$ is nowhere; `review-3` has $y'' + 4y' + 3y$ (a companion-matrix item), which an earlier draft used and I replaced; $e^{-4t}$ occurs in l9 and review-3 as a decay term of other equations; "test rig" only in `brainteasers` (egg drop).
- `p-skydiver-check`: "skydiver", "balloon", "air resistance", $9.8 - 0.2v$, 16.1543, 16.1504, 17.64 not found; 9.8 only inside 9.8521 in homework-3.
- `p-dose-simulator`: "tablet", "gut", "clinic", "drug" not found in `odes`, `numerics`, `eigen` or the exams; 0.4642 not found; 2.7853 is RK4's stock limit, stated in l17 and review-4.

Backlog: no engine limit met; no bullet added under "Raised later (problems odes 4):".

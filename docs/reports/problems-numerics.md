# Problem sets: numerics levels 1 to 3 (brief `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/numerics/problems-1.json` to `problems-3.json`. Level 4 is left to a later author. Numbers: `docs/reports/problems-numerics-numbers.py` (675 of 675 checks, exits 0). Level 1 was written by the first agent; this pass kept its one later edit (an explain split so it no longer chains two equals signs) and authored or finished levels 2 and 3.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-float32-overnight | 4 (4 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-moment-recurrence | 5 (4 / 1) | l1, l4 | 5 |
| problems-1 | p-netting-sum | 4 (4 / 0) | l3, l4 | 4 |
| problems-2 | p-project-irr | 5 (5 / 0) | l5, l6 | 4 |
| problems-2 | p-spread-spline | 5 (5 / 0) | l8, l5 | 4 |
| problems-2 | p-survival-crossing | 5 (5 / 0) | l7, l5 | 5 |
| problems-3 | p-normal-cdf-quadrature | 4 (4 / 0) | l9, l10 | 3 |
| problems-3 | p-stiff-credit-trapezoid | 4 (4 / 0) | l9, l11, l12 | 5 |
| problems-3 | p-rate-path-euler | 5 (5 / 0) | l9, l11 | 4 |

Every lesson of each level appears; every problem draws on two or more. Each numeric part names its form. Each later part restates the value it uses.

## Level 2 changes to the draft

- `p-project-irr` part 4: tolerance moved from $10^{-10}$ to $10^{-12}$ (the `bisect` slip becomes 38 halvings), so it no longer echoes l5's transfer screen (Newton against 31 halvings to $10^{-10}$).
- `p-project-irr` part 5: `unit: "%"` with the key as a fraction (0.088963), so "8.90" and "8.90%" are both read.

## Checks (all green at the level 3 commit)

1. Number script: 675 of 675, exit 0. Two methods per key (fractions, sympy or mpmath, then floats, NumPy, SciPy `CubicSpline`, `brentq`, `quad`, `leggauss`, `ndtr`, or a direct ODE run); each `wrong` value is recomputed from its slip and checked clear of the key band; stated figures are checked as text.
2. Validator: 0 errors; no warning on the three sets.
3. Playthrough `--problems numerics/problems-n --local-cdn <pkgs>`: green on desktop and `--mobile` for 1, 2 and 3 (`--why` routes 25 slips on set 2, 28 on set 3). Part screenshots at 440 px read: no overflow.
4. Voice scan 35: 0 and 0.
5. `fresh-check --file`: 0 hits on each set (advisories only: $u = 2^{-53}$ in set 1; $e_{k+1} \approx Ce_k^2$ and the figures 120, 150 in set 2).
6. `grade-all --file`: 0 failures (13, 15, 13 widgets).

## Closest course material per problem (hand check against every lesson screen, review and homework item, levels 1 to 4)

| problem | closest lesson screen | closest review | closest homework | why it is not a walk through it |
|---|---|---|---|---|
| p-float32-overnight | l1 transfer (float32 index level at 20,000, gap $2^{k-23}$); l2 problem on the quadratic root | r1-float32-notional | h1-float32-int | Those ask one gap. Here the gap feeds a forward-rate subtraction, its relative error, the amplification (matched to $\kappa$ of a subtraction) and the forward in bp: a chain no screen holds. |
| p-moment-recurrence | l4 opening ($e^{-20}$ by series) and the backward-stable screen | r1-discount | h1-forward-backward | The course shows growth through series terms; this is a recurrence whose error grows as $n!$, then fixed by running it backwards from a guess. Neither the integral nor the backward run is in the course. |
| p-netting-sum | l4 "forward error ≲ κ × backward error" | r1-kappa-shift | h1-stats-code (Kahan) | The course states the bound; here $\kappa$ of a sum is computed from gross and net flows, then loop and pairwise bounds are priced in pounds. |
| p-project-irr | l6 problem (Newton step outside the bracket: take the midpoint); l5 bond-yield ladder | r2-safeguard | h2-ytm-book (code) | l6 and r2 ask what the solver does; here the step is computed, the fallback point evaluated, Newton resumed, steps counted from $Ce_k^2$ and the IRR read. Markets' hw1-irr-quadratic solves a 2-year IRR by the quadratic formula: other numbers and method. |
| p-spread-spline | l8 problem (right side of the 5-year row) and ladder (check $4M_2 + M_3$) | r2-spline-global | h2-spline-m (one unknown, 3 points) | The lesson gives the $M_k$ and reads forwards; here a 2 by 2 system is solved by hand, the piece evaluated and differentiated, and Newton inverts the spline for a target spread. |
| p-survival-crossing | l7 error-formula screen (node product at 0.95); l5 secant explore | r2-lebesgue | h2-tick-vol (ΔV / vega) | The course bounds data error by a Lebesgue constant; here a quadratic is built from divided differences, its root found by secant then Newton, and the interpolation bound turned into days through the slope. |
| p-normal-cdf-quadrature | l9 quiz q-richardson-num ($(4T_4 - T_2)/3$ for $e^x$); l10 two-node problem on $x^4$ and quiz q-interval | r3-richardson | h3-gauss-n | Course items apply one rule each to $e^x$ or monomials. Here one integrand runs through trapezium, Richardson and a mapped two-node rule, and the result is $\Phi(1)$ with its error. |
| p-stiff-credit-trapezoid | l12 trap (trapezoidal factor $-0.7241$ at $h = 0.25$, ringing path); l11 explore ($C$ from one run, $n$ for a tolerance) | r3-ring ($h\lambda = -40$, choice) | h3-rk4-limit | l12 asks whether an unconditionally stable rule is safe at any step; here the step is chosen for accuracy from a measured order, and the leftover fast mode after the run, $0.9747^{80} \approx 0.129$, is computed against the tolerance. Level 4's l14 Crank-Nicolson factor near $-1$ (ν = 80) is the PDE form; this is an ODE with two modes. |
| p-rate-path-euler | l11 ladder (error of the $n = 20$ RK4 value from two runs); l9 derive (Richardson) | r3-richardson | none close (h3-trap-n is a doubling count) | The order is read from three runs with no exact value (gaps, not errors), the estimate feeds an extrapolation and a step budget, and the closing part shows one trapezium strip is exact for a linear rate. No course item uses an ODE whose answer is a quadrature. |

No reuse was found; the reader should rule on p-stiff-credit-trapezoid against the l12 trap screen, the closest pairing.

## Open

- `problems-1` p-float32-overnight part 2 asks for a percentage with the key in per cent and no `unit`, so "0.060%" is read as 0.0006 and refused. Fix: `unit: "%"`, key 0.000596, tol 0.000005, `wrong` 0.000298 and 0.001192 (and the number script's `num` call for it). Not changed here, as level 1 was outside this pass's levels.

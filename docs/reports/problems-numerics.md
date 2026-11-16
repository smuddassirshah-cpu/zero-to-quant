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

# Level 4 (second author, appended): `problems-4.json`, "One option, three ways"

Written by a second author; sets 1 to 3 and the sections above are untouched. Numbers: the level 4 block appended to `docs/reports/problems-numerics-numbers.py` (the only change above it is `LEVELS` now listing 4); the script runs 1,010 of 1,010 checks and exits 0.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-hand-implicit-put | 4 (4 / 0) | l13, l14 | 4 |
| problems-4 | p-pilot-control | 4 (4 / 0) | l15, l16 | 4 |
| problems-4 | p-grid-node-budget | 5 (5 / 0) | l13, l14, l17 | 5 |
| problems-4 | p-digital-pairs | 5 (5 / 0) | l15, l16 | 5 |

Every lesson of level 4 appears; each problem draws on two or more. Each numeric part names its form; each later part restates the value it uses. No part asks for a percentage, so no `unit: "%"` is needed.

## Methods in the script

Each key two ways: fractions (the matrix rebuilt from $\sigma$, $r$, $\Delta\tau$; Thomas by hand in exact arithmetic; bounds as fractions with an exact ceiling; the pair's 2 by 2 joint table) against floats (numpy `solve`, scipy `lu`, `brentq`, brute searches over $n$, $N$ and $M$, a real explicit and Crank-Nicolson put grid run against Black-Scholes). Every `wrong` value is recomputed from its named slip and checked clear of the key band; stated figures in feedback and `explain` are checked as text. The grid run confirms the prose: $-0.0219$ at $M = 69$, $-0.00243$ at $M = 207$ (over target), $-0.00137$ at $M = 276$, Crank-Nicolson at 100 steps $-0.0015$, and the hand step's put at £9.96 against the formula's £10.00.

## Checks (all green at the level 4 commit)

1. Number script: 1,010 of 1,010, exit 0.
2. Validator: 0 errors; no warning on `problems-4.json` (the `negative-key` warning was fixed with a `sign` slip; three long questions split).
3. Playthrough `--problems numerics/problems-4 --local-cdn <pkgs>`: green on desktop (`--why`, 51 typed slips routed) and `--mobile`. Part screenshots at 440 px read: the 3 by 3 system fits, no overflow.
4. Voice scan 35: 0 and 0.
5. `fresh-check --file`: 0 hits (no `retold`, no `rate`).
6. `grade-all --file`: 0 failures (18 numeric widgets).

## Closest course material per problem (hand check against every lesson screen, quiz, review and homework item of levels 1 to 4, sets 1 to 3, and the numerics items of `exams/topic-2.5.json`, `stage-2.json` and `mock-superday-strats.json`)

| problem | closest lesson screen | closest review / homework | closest exam item | why it is not a walk through it |
|---|---|---|---|---|
| p-hand-implicit-put | l13 ladder "One step by hand" (explicit coefficients at $j = 50$, one step of the call); l14 problem "Solving a tridiagonal system" (4 by 4, all-ones answer) | r4-thomas (cost, choice); h4-weight (centre weight at $j = 80$) | topic-2.5 e-explicit-step (the bound, $\Delta\tau$ and $M$) | No course item takes an implicit step by hand. Here a put on a five-node grid first fails the explicit weight test (one part), then the learner runs the Thomas sweep on its own matrix (pivot, last row, back substitution) to a price checked against the formula. The l14 system is a bare matrix with no option behind it. |
| p-pilot-control | l16 problem "A control with a known mean" ($b^* = 274.91/408.11$) and ladder "For our call" (factor 6.88, 315,000 paths); l16 transfer "Machine time" (10 hours to 36 s) | r4-vrf; h4-control-paths (1,000,000 times $1 - \rho^2$) | topic-2.5 e-control-variate ($b^*$ then the factor); r5-mc-error in the mock (half-width two SE, 810,000 paths) | $b$ is given, not asked. The chain is new: the residual variance at a pilot-fixed $b$, the paths for a 95% half-width of £0.02, the machine-time gain once a controlled path costs 1.3 plain ones, and the break-even cost 13.59. No course item prices a control's extra cost per path. |
| p-grid-node-budget | l17 trap "The strike between nodes"; l13 ladder "Too long a step" (smallest $N$ at $M = 100$, $T = 1$); l17 ladder "The grid's error" (quarter per refinement) | r4-limit-150; r4-predict-ds ($-0.0078/16$) | topic-2.5 e-explicit-step ($\Delta\tau$ from $S_{\max}/\Delta S$, largest $M$ for $N = 2{,}500$); stage-2 c-error-rates | The course reads node placement from a table and applies the bound with $T = 1$. Here the learner chooses $M$ so both $S_0$ and $K$ sit on nodes, scales the bound by $T$, picks the first whole refinement $k$ that meets £0.002 with nodes kept, recomputes $N$, and prices explicit against Crank-Nicolson work. The design chain is in no item. |
| p-digital-pairs | l16 ladder "Antithetic pairs" (call, $\rho = -0.501$ given, efficiency 2.0); l16 trap "When pairs hurt" (straddle); l15 problem "The rate" | r4-anti (digital named as helped, choice); r4-paths | topic-2.5 e-mc-error (SE from 40,000 paths) | The course gives the pair correlation from simulation. Here it is derived exactly from a 0 or 1 payoff ($\rho = -p/(1 - p)$, a pair never pays twice), then turned into efficiency 4/3 and a pair count, with plain and payoff counts checked against it. 25,600 paths, not the exam's 40,000. |

Second hand pass on feedback lines: five `byKey` lines that echoed lesson or exam slips ("You rounded ... down. ... just over the bound", "You divided by $n$. The error falls like ...", "A 95% interval reaches 1.96 ...", "You used $M$ for $M^2$ ...") were rewritten in other words before the commit. No sentence, number set, matrix or story is shared with sets 1 to 3.

## Open (level 4)

- None in content. One inbox bullet: the same-course check does not load the topic exam.

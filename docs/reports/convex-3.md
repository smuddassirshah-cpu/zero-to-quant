# convex level 3 (Duality and KKT): report

## Files (app/content/courses/convex/)

| file | screens or items | quiz | canvases and widgets |
|---|---|---|---|
| l9-lagrangian-dual.json | 11 screens | 4 | `pair` of planes ($L(x, \lambda)$ with a price control, $g(\lambda)$ with a riding point); graded `slider` to the best price; `space` saddle; weak-duality `order` with a convexity distractor; lower-envelope plane; portfolio $g(\nu)$ with a draggable point; reversed-constraint trap; lot-size gap with a `\min` expression; `code` (NumPy) |
| l10-kkt.json | 12 screens | 4 | `plane` contours, half-plane polygon, draggable $P$ with a live $-\nabla f$ plane vector; `vectors` normal cone (chain $2\mathbf{a}_1$ then $2\mathbf{a}_2$, `angles` arc); active-set `order`; four-case `table`; sign-convention `table` canvas; Slater edge case; `code` (NumPy) |
| l11-mean-variance-kkt.json | 12 screens | 4 | `plane` of $V(w_1)$ on the 10% line with the long-only part, a riding drag point and the tangent at the wall; `bars` of weights; multiplier `table`; clip-and-rescale trap; weight-formula `order`; `code` (NumPy) |
| l12-long-only.json | 12 screens | 4 | `console` solver output (hook, four-asset book, `linprog` status 2, the `ineq` sign trap, tiny zeros, 35% cap); `space` variance bowl with the target line drawn on it as a curve; KKT `table` for the four-asset book; tracking `table`; `code` (SciPy) |
| l13-shadow-prices.json | 11 screens | 3 | `pair`: desk region (hidden vertices moved by `derive`) beside $v(R)$; draggable $v(B)$; frontier planes with tangents at 8% and 10%; wall plane; trap plane with $v$ hidden until Show why; degenerate-corner `multi`; `code` (SciPy) |
| review-3.json | 10 items, `pass` 0.8 | | difficulty 2 to 4, all five lessons and one level 2 recall (an LP dual) |
| homework-3.json | 8 items | | difficulty 4 to 5 (three at 5); weak-duality `order` for the general problem; two vector `expression` KKT items; `code` `frontier` (difficulty 5); `longform` exit task with the 45% cap, 10-point rubric |

No performance task: the level's lesson objectives start with Form, State, Solve, Solve and Read, so the verb rule does not match (AUTHORING section 5). The longform is ordinary homework.

## Gates

- Validator: 0 errors; no warnings on level 3 files (the only convex warnings are the unwritten level 4 and the L1 and L2 number scripts, see the inbox).
- Voice scan (`VOICE_BASE=app/content/courses/convex/`): 0 over 20 words and 0 explanations over three sentences.
- Numbers: `docs/reports/convex-L3-numbers.py` exits 0: 410 of 410 `numbers_lib` checks and 0 two-route failures. It runs all 6 code widgets in CPython: every solution passes all its tests, every starter passes none.
- Playthrough with `--local-cdn` (this session's pkgs): see the table below.

| file | desktop | `--mobile --tablet` (440, 1032, 1376) |
|---|---|---|
| l9-lagrangian-dual | ok, 15 checks, quiz 4/4 | ok |
| l10-kkt | ok, 16 checks, quiz 4/4 | ok (replayed after the table fix) |
| l11-mean-variance-kkt | ok, 16 checks, quiz 4/4 | ok (replayed after the trap canvas fix) |
| l12-long-only | ok, 16 checks, quiz 4/4 (SciPy code green in Pyodide) | ok |
| l13-shadow-prices | ok, 14 checks, quiz 3/3 (SciPy code green) | ok |
| review-3 | ok, 10 of 10 recorded | ok |
| homework-3 | ok, 8 of 8 right, 40 of 40 marks, longform marked by the button | ok |

Screenshots read at every width; fixes made: l9 caption no longer gives the hook's answer, lines relabelled, saddle camera and $z$ range (no clipped staircase); l10 line label off the axis, `angles` moved to state so the cone arc draws, four-case table narrowed for a phone; l11 trap shows the clipped weights (the KKT weights appear in Show why); l12 bowl camera turned so the target line is seen side on; l13 overlapping labels moved, the trap hides $v(R)$ until Show why so the £500k is not on screen.

## Numbers and sources

Every value is computed twice in the script: exact fractions (KKT systems on an active set solved by Gauss-Jordan elimination, closed forms, vertex enumeration) against a solver (SLSQP at `ftol` 1e-15, HiGHS, `numpy.linalg`). Every dual value and multiplier is computed by the hand formula and recovered from the solver's weights by `np.linalg.lstsq` on the stationarity rows of the free assets (never `res.multipliers`).

Reproduced from the brief: $g(\lambda) = \lambda - \lambda^2/4$ with $g(1) = g(3) = 0.75$, $g(4) = 0$, peak 1 at 2; $s = \tfrac{1525}{36}$, $\nu^* = \tfrac{72}{1525}$, $d^* = \tfrac{36}{1525}$, $g(0.03) \approx 0.020469$; reversed $g = -\lambda - \lambda^2/4$ with bound 0; lot-size gap $p^* = 2$, $d^* = 1$; $(2.5, 1.5)$, 4.5, $\lambda = 3$; $(2, 2)$, 5, $\boldsymbol{\lambda} = (2, 2)$; $(3, 1)$ with $(4, -2)$; all running-portfolio weights, variances, volatilities and multipliers; $V(w_1)$ and $\tfrac{7}{75}$; clip numbers 0.4615, 0.5385, 9.615%, 1.0833; the four-asset book's weights, $\tfrac{27923}{450000}$, 24.910%, $\lambda$, $\mu$, $\nu_1$, $\eta_4$, eigenvalues and 8.6% (HiGHS status 2 at 9%); the SLSQP sign flip $(0.5902, 0.2623, 0.1475)$ at 6.672%; $v(R)$, 490, 500, ranges 10 to 20 and 8 to 18; 0.002571 against 0.002765, 18.684%; 0.005111 against 0.005389, 0.0865, 29.411%; 0.000933 against 0.000877, 0.080234; 3.586; the degenerate duals $(30, 10, 0, 0)$ and $(20, 0, 0, 20)$ with 479.9 and 480 either side of $R = 18$; $\eta_3 = \tfrac{1}{375}$, 0.049844 against 0.049841, 22.3259% against 22.3252%.

Computed and reported ("compute and report" in the brief):
- 8% target with a 35% cap on the four-asset book: $\mathbf{w} = (\tfrac{9}{1442}, \tfrac{4897}{14420}, \tfrac{2193}{7210}, 0.35) \approx (0.006241, 0.339598, 0.304161, 0.35)$, variance $\tfrac{1836207}{36050000} \approx 0.050935$, $\mu = \tfrac{15693}{7210}$, $\eta_4 = \tfrac{9147}{450625}$; the bond is a free asset.
- Index tracking: benchmark $(0.10, 0.30, 0.30, 0.30)$ with the 40% book excluded gives $\mathbf{w} = (\tfrac{9961}{45085}, \tfrac{4965}{18034}, \tfrac{45423}{90170}, 0) \approx (0.2209, 0.2753, 0.5037, 0)$, tracking variance $\tfrac{299916}{28178125} \approx 0.010644$ (10.317% a year).
- 10% shorting multiplier $\lambda = -\tfrac{151}{900}$ (brief gives only $\mu = \tfrac{29}{9}$).
- Long-only frontier switch: the free optimum's $w_1$ reaches 0 at $r = \tfrac{163}{1700} \approx 9.588\%$ (used in l13's long-only frontier plot).
- Frontier without bounds: $V^*(r) = \tfrac{3050r^2 - 407r}{63} + \tfrac{3013}{12600}$, so $dV^*/dr = \tfrac97$ at 8%.
- 2 by 2 correlated test case ($\sigma_{12} = 0.012$): $s = \tfrac{6625}{216}$, $d^* = \tfrac{216}{6625} \approx 0.032604$, $g(0.03) \approx 0.023099$.
- Review and homework: $g(0.06) = \tfrac{7}{320}$; projection $(1.2, 0.4)$ with $\lambda = 1.6$; $\nu_1 = \tfrac{29}{250}$ at 10.1%; 9.05% best return under a 45% cap; £540k at a £12m budget; LP dual 11 at $(2, 1)$; $g = 2\lambda - \lambda^2/2$; gap 3 for lots $\{0, 4\}$; $(2.4, 0.8, 1.2)$; $(0.5, 1.5, 3, 2)$; $\mu = \tfrac{142}{63}$ at 9%; the strictly feasible point $(0.11, 0.445, 0.445)$ (9.005%) used for Slater in the model answer.

**Brief errors and corrections.** None in the brief's figures. One slip of my own was caught by the script: a homework `wrong` value for "dropped the 2 in the gradient" was 1.785714; the true slip value is $\tfrac{158}{99} \approx 1.59596$, now used.

## Runtime

SciPy loads in Pyodide and SLSQP, `linprog` (HiGHS) and `np.linalg.lstsq` give the same values as CPython's SciPy 1.18.1 at the tolerances used (absolute 1e-6 for solver weights and finite-difference prices, 1e-4 and 1e-3 for the portfolio shadow prices, 1e-8 for a solver variance, 1e-9 for closed forms). No value differed. `res.multipliers` is never used; multipliers come from the stationarity rows (l11's method) or from re-solving with a moved constraint (l13's `shadow_price`). The SciPy load time could not be measured (no per-item timing in the playthrough; already in the inbox from level 1), so each `how` says "a few seconds from cache, longer on a first visit".

## Canvases

- l9 `space` saddle: surface $z = x^2 + \lambda(1 - x)$ over $x \in [-1, 3]$, $\lambda \in [0, 4]$, $n = 22$ (484 cells), opacity 0.65, $z$ range $[-0.5, 9.5]$ so nothing is clipped (a clamped top drew a staircase); camera az −70, el 42; the curve of minimisers $(t/2, t, t - t^2/4)$ bold, the slice at the slider's $\lambda$, and the point $(1, 2, 1)$.
- l12 `space` variance bowl over $(w_1, w_2)$ with $w_3 = 1 - w_1 - w_2$, $n = 22$ (484 cells), $z$ range $[0, 0.33]$ (no clipping), camera az 25, el 28 so the target line is seen from the side; the line is a curve on the surface (no vertical plane, item 440) with its long-only part bold and a point riding it at the slider's $w_1$.
- l13 desk region: five hidden vertices driven by `derive` with a `let` for the budget-risk corner; the region and the best plan follow the risk control from 0 to 30.

## Notes

- Scratchpad: this session's `19ed1109...` folder, subfolder `convex-3` (the brief's `a8ff8d32...` paths are stale).
- Screens: l10, l11 and l12 have 12 screens, the brief's maximum.
- No `course.json` change proposed.
- Inbox: 4 bullets under "Raised later (convex level 3)".

# Problem sets: convex (levels 1 to 3)

Level 4 (`problems-4.json`) is left to a later author. Numbers: `docs/reports/problems-convex-numbers.py` (595 own checks, numbers_lib failures 0, exit 0).

## Sets

| Set | Item | Parts | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| 1 | p-shortfall-and-fee | 5 | l1, l2, l3 | 4 |
| 1 | p-worst-scenario | 5 | l1, l2, l3, l4 | 4 |
| 1 | p-two-futures-hedge | 5 | l1, l2, l3, l4 | 5 |
| 2 | p-parking-cash | 5 | l5, l6, l7 | 4 |
| 2 | p-whole-blocks | 4 | l5, l6 | 4 |
| 2 | p-three-strategies | 5 | l5, l6, l8 | 5 |
| 3 | p-capital-price | 5 | l9, l10, l13 | 5 |
| 3 | p-no-borrowing | 5 | l10, l11, l12, l13 | 4 |
| 3 | p-variance-limit | 5 | l10, l11, l13 | 4 |

Set 1: 15 parts. Set 2: 14 parts (1 choice). Set 3: 15 parts (1 choice).

## Gates

- Validator: 0 errors, no warnings on the three sets beyond advisory `O2-long-sentence`.
- Voice scan 35 on the course folder: 0 and 0.
- Number script: exit 0. Every key twice (exact fractions or sympy, then linprog, SLSQP, a grid, vertex enumeration or a finite difference); every `wrong` value recomputed from its slip and shown outside the key band.
- `fresh-check.mjs --file`: 0 hits on each set. Advisories on set 3 (shared single parameters 0.01, 0.04, 0.005 with l17 and an exam of topic 1.10) judged coincidental: different roles, no shared set or story.
- `grade-all.mjs --file`: 0 failures on sets 2 and 3 (set 1 run by the first agent).
- Playthrough `--problems` desktop and `--mobile`: green for sets 2 and 3; shots at 440 px read, no layout faults. Set 1 was played by the first agent at its commit and is unchanged.

## Changes to the level 2 draft

The draft's minimax line fit walked the same chain as set 1's p-worst-scenario (trial value, active rows, equalised rows, value), so it was replaced by p-whole-blocks. p-parking-cash parts 4 and 5 (complementary slackness, then +1 unit of the budget) retold homework-2 h2-do-nothing and l13 screen 0; they now ask for a notes floor re-solve and the largest feasible floor. Lines in p-three-strategies that echoed l8 screen 6 and l6 screen 1 were rewritten. After the topic exam was read, p-whole-blocks changed rows: the first version shared $3x + 2y \le 12$ and an $x + 2y$ row with exam item e-lp-corner.

## Closest course material per problem (verdict clean)

- p-shortfall-and-fee: l2 screen 9 (trade-splitting impact cost), review r1-gap (chord gap of $x^2 + 2x$), homework h1-valley; topic exam e-hessian-threshold. A kinked cost $2(x-3)^2 + 5|x|$, convex by the sum rule, minimised by calculus on one side and then under a cap; no screen has a kink plus a cap.
- p-worst-scenario: l4 screen 3 (epigraph trick), review r1-epi, homework h1-sublevel; exam e-local-global-proof. Scenario losses built from fund returns, then a sublevel set length, then the LP; the course items are a bare max of two lines or a proof.
- p-two-futures-hedge: l2 screen 4 (Hessian of $x^2 + bxy + y^2$), review r1-hessian, homework h1-largest-a; exam e-hessian-threshold. The quadratic comes from a hedge's covariances and ends with a sign limit solved on its edge.
- p-parking-cash: l5 screens 0 to 4 (desk LP), l7 screen 1 (`-c`, `-res.fun`), review r2-cut and r2-status, homework h2-do-nothing; exam e-lp-corner. An equality removed by substitution, a constant outside `c`, a floor re-solve and the largest feasible floor; no dual and no shadow-price step.
- p-whole-blocks: l6 screens 1 and 2 (corner enumeration), l9 screen 9 (lots and a duality gap), review r2-vertex, homework h2-hedge (fractional contracts allowed); exam e-lp-corner. The course never rounds an LP to whole units or uses the LP value as a bound on whole plans.
- p-three-strategies: l8 screens 1, 2 and 5 (dual corners, rows from columns, complementary slackness), review r2-cs, homework h2-range; exam e-duality-sandwich. The course goes primal then dual; here a three-variable primal is solved through its two-variable dual and recovered by slackness, then an entry threshold read from dual prices.
- p-capital-price: l9 screens 0 to 2 ($x^2$ with $x \ge 1$), l13 screen 2, review r3-bound and r3-shadow, homework h3-dual-fn; exam e-dual-function and e-solver-certificate. A maximisation (prices give upper bounds), two desks responding to a transfer price, $g' = 6 -$ asks, then a capital estimate.
- p-no-borrowing: l11 screens 3 to 5 and 7 (KKT rows, $w_1 = 0$, clip and rescale), l12 screen 4, review r3-nu, homework h3-cap-kkt; exam e-long-only-kkt. Risk-aversion objective, correlated 2 by 2 matrix, a cash asset whose bound is a borrowing ban and $\nu_c = \lambda - r_f$; no return target.
- p-variance-limit: l4 screen 2 (standard form of max return under a variance limit), l1 screen 5 (risk budget set), l13 screen 3 ($\mu$ as a slope), review r3-gap, homework h1-sublevel; exam e-slsqp-sign. Solved here: a quadratic limit by its roots, $\mu = R'/V'$, Slater and a basis-point estimate.

No `feedback`, `explain` or `why` line was copied or paraphrased from these items; each was compared by hand.

## Engine

One bullet in `docs/BACKLOG-INBOX.md` (fresh-check `rate` false positive).

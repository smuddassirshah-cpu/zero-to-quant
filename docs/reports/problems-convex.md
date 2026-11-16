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

# Level 4 (`problems-4.json`, added by the level 4 author)

| Set | Item | Parts | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| 4 | p-curve-fit-log | 5 | l14, l15 | 4 |
| 4 | p-sale-horizon | 4 | l14, l16 | 4 |
| 4 | p-variance-log | 4 | l14, l15, l17 | 5 |

13 parts, 12 typed (numeric), 1 choice. Skills `cv-descent`, `cv-duality`.

## Gates (level 4)

- Validator: 0 errors; on `problems-4.json` only advisory `O2-long-sentence` (4).
- Voice scan 35 on the course folder: 0 and 0.
- Number script: level 4 section appended (`level4()`, 178 checks; SETS now loads 1 to 4). Whole script 773 of 773, numbers_lib failures 0, exit 0. Method 2 per key: a simulated descent or Newton run in floats, a bounded scalar search, numpy eigenvalues, a counting loop, Aitken's delta-squared formula.
- `fresh-check.mjs --file`: 0 hits. Hand greps of 30.8, 0.9481, 0.0649, 1.7375, 1.5145, 8.0793, 200.4096, 0.2401, 0.765625, 199.95, 0.2901, "yield-curve" and "block of shares" over the course and `exams/topic-2.5.json`: none outside the set.
- `grade-all.mjs --file`: 13 widgets, 0 failures.
- Playthrough `--problems convex/problems-4`, desktop and `--mobile`: green; 440 px shots read, no layout faults.

## Closest course material per problem (level 4, verdict clean)

- p-curve-fit-log. Lesson: l14 screens 0 and 4 (factors $1 - s$, $1 - 10s$ of a given bowl; best step $\tfrac{2}{11}$), l15 screen 1. Quiz: l14 q1 (factor at $s = 1/\lambda_{\max}$). Review: r4-factor ($y$ factor $-0.2$ from a given curvature). Homework: h4-rho (eigenvalues 8 and 2 to $\rho = 0.6$). Exam: e-rate-from-kappa (eigenvalues to $\rho$ to a count), e-step-limit. Not a walk: the course goes curvature to factor; here two logged factors are inverted to curvatures (0.8, 30), then the retuned step, its factor and the steps saved over the current run, with a $10^4$ target the course never uses.
- p-sale-horizon. Lesson: l14 screen 7 ($s < 2/L$ for the logistic loss), l16 screens 0, 3 and 9 ($x - \ln x$, 44 descent steps against 5, far start). Quiz: l16 q0 ($e^x - 2x$). Review: r4-newton ($x^2 - 2\ln x$). Homework: h4-newton-iter (simplify a Newton map). Exam: e-newton-minimise ($e^x - 3x$, error ratio $f'''/2f''$). Not a walk: a cost $8/T + 2T$ on $T \ge 1$, $L$ read on a region, descent at $1/L$ and Newton landing on the same first point, then the extra cost in pounds of stopping early; no step count, no error-ratio or far-start step.
- p-variance-log. Lesson: l15 screens 1 and 5 ($\rho$ and the log slope of a run), l17 screens 0 to 4 (feasibility, lstsq residual, dual bound, excess) and 11 (tolerances fixed in advance). Quiz: l15 q2 ($\rho = 0.9$ to $\kappa$), l17 q2 (bracket 470 to 490). Review: r4-backout (errors 1, 0.6, 0.36 to $\kappa$). Homework: h4-bound (0.0650 against 0.0641). Exam: e-solver-certificate ($g(5.9)$, gap, what it certifies), e-richardson-three (an extrapolation that cancels a power of $h$, not a geometric tail). Not a walk: logged objective values give $\rho^2$ through the drops, an extrapolated $V^*$, the steps left to a tolerance, and a sign-off line that separates the estimate from the certified bracket; no residual fit, no dual function evaluated.

No `feedback`, `explain` or `why` line was copied or paraphrased from these items; each was compared by hand. Three draft lines that echoed l14 screens 4 and 7 and l15 screen 3 ("makes the two factors equal in size", "below which step does descent always settle", "no fixed step does better") were reworded before the first check.

## Engine (level 4)

No new limits; no inbox bullets.

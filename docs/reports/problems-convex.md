# Problem sets: convex (levels 1 to 3)

Level 4 (`problems-4.json`) is left to a later author. Numbers: `docs/reports/problems-convex-numbers.py` (595 own checks, numbers_lib failures 0, exit 0; 792 after the session AF re-author pass, levels 1 to 4).

## Sets

| Set | Item | Parts | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| 1 | p-shortfall-and-fee | 5 | l1, l2, l3 | 4 |
| 1 | p-account-target | 5 | l1, l2, l3, l4 | 4 |
| 1 | p-two-futures-hedge | 5 | l1, l2, l3, l4 | 5 |
| 2 | p-parking-cash | 5 | l5, l6, l7 | 4 |
| 2 | p-whole-blocks | 4 | l5, l6 | 4 |
| 2 | p-three-strategies | 5 | l5, l6, l8 | 5 |
| 3 | p-capital-price | 5 | l9, l10, l13 | 5 |
| 3 | p-style-fit | 5 | l10, l11, l12 | 4 |
| 3 | p-variance-limit | 5 | l10, l11, l13 | 4 |

Set 1: 15 parts (3 choice, 2 expression). Set 2: 14 parts (1 choice). Set 3: 15 parts (2 choice).

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
- p-worst-scenario: re-authored in session AF as p-account-target (review finding 4); see below.
- p-two-futures-hedge: l2 screen 4 (Hessian of $x^2 + bxy + y^2$), review r1-hessian, homework h1-largest-a; exam e-hessian-threshold. The quadratic comes from a hedge's covariances and ends with a sign limit solved on its edge.
- p-parking-cash: l5 screens 0 to 4 (desk LP), l7 screen 1 (`-c`, `-res.fun`), review r2-cut and r2-status, homework h2-do-nothing; exam e-lp-corner. An equality removed by substitution, a constant outside `c`, a floor re-solve and the largest feasible floor; no dual and no shadow-price step.
- p-whole-blocks: l6 screens 1 and 2 (corner enumeration), l9 screen 9 (lots and a duality gap), review r2-vertex, homework h2-hedge (fractional contracts allowed); exam e-lp-corner. The course never rounds an LP to whole units or uses the LP value as a bound on whole plans.
- p-three-strategies: l8 screens 1, 2 and 5 (dual corners, rows from columns, complementary slackness), review r2-cs, homework h2-range; exam e-duality-sandwich. The course goes primal then dual; here a three-variable primal is solved through its two-variable dual and recovered by slackness, then an entry threshold read from dual prices.
- p-capital-price: l9 screens 0 to 2 ($x^2$ with $x \ge 1$), l13 screen 2, review r3-bound and r3-shadow, homework h3-dual-fn; exam e-dual-function and e-solver-certificate. A maximisation (prices give upper bounds), two desks responding to a transfer price, $g' = 6 -$ asks, then a capital estimate.
- p-no-borrowing: re-authored in session AF as p-style-fit (main-session ruling, review findings 16, 17, 20); see below.
- p-variance-limit: l4 screen 2 (standard form of max return under a variance limit), l1 screen 5 (risk budget set), l13 screen 3 ($\mu$ as a slope), review r3-gap, homework h1-sublevel; exam e-slsqp-sign. Solved here: a quadratic limit by its roots, $\mu = R'/V'$, Slater and a basis-point estimate.

No `feedback`, `explain` or `why` line was copied or paraphrased from these items; each was compared by hand.

## Engine

One bullet in `docs/BACKLOG-INBOX.md` (fresh-check `rate` false positive).

## Session AF: re-author and fix pass (second read `docs/reviews/review-problems-convex-1-3.md`)

Two problems re-authored, ids changed (the sets are new this session): `p-worst-scenario` became `p-account-target` (set 1) and `p-no-borrowing` became `p-style-fit` (set 3). The reader's replacement lines for findings 1 to 3, 6 to 15, 18 and 19 were applied as written (46 lines), after recomputing their numbers; findings 5, 16 and 17 fell with the re-authored problems. `p-three-strategies` stays, with the reader's lines (findings 11, 12, 13).

| Set | Item | Parts | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| 1 | p-account-target | 5 (2 expression, 2 numeric, 1 choice) | l1, l2, l3, l4 | 4 |
| 3 | p-style-fit | 5 (4 numeric, 1 choice) | l10, l11, l12 | 4 |

Closest course material per new problem (verdict clean, every feedback, explain and why line compared by hand):

- p-account-target. Lesson: l4 screen 1 (standard form, a $\ge$ moved across), l4 screen 4 (logs turn $xy \ge 1$ into a convex limit), l2 screen 3 ($f'' \ge 0$ on $-\ln x$), l1 screen 6 (volatility at least 28% is not convex), l3 screen 5 (a stationary point of a convex function is global). Quiz: q4-disguise ($x/y \le 3$), q2-max. Review: r1-floor (a volatility floor and a midpoint), r1-compose (the rules). Homework: h1-sublevel, h1-sharpe (a ratio rewritten). Exam: stage-2 c-convex-functions ($-\ln x$ convex), topic-2.5 e-convex-sets. Not a walk: an at-least limit on a concave function shown convex through part 1's second derivative, a square-root change of variables to a bowl and a half-plane, the best plan by substitution along the active limit, and the cost curve $T^2/45$. No epigraph, no rows below $t$, no lines set equal, no sublevel length, no scenarios (finding 4's list).
- p-style-fit. Lesson: l12 screen 2 ($\mathbf{Q} = 2\boldsymbol{\Sigma}$, $\mathbf{q} = \mathbf{0}$), l12 screen 9 (a tracking QP with bounds), l11 screen 0 (a quadratic along the target line), l10 screen 2 (the four KKT conditions), l11 screen 9 (a floor that does not bind). Quiz: q12-qp ($\mathbf{Q}$, $\mathbf{q}$ of $\mathbf{w}^T\boldsymbol{\Sigma}\mathbf{w} - 2\mathbf{m}^T\mathbf{w}$), q10-slack. Review: r3-kkt. Homework: h3-frontier, h3-cap-kkt. Exam: stage-2 c-kkt-hand (two weights summing to 1), topic-2.5 e-long-only-kkt and e-slsqp-sign. Not a walk: a QP built from regression sums (returns-based style analysis, new to the course), the budget fit by substitution, the bounds settled by complementary slackness with no multiplier solved or sign-checked, then the fit's residual and its root-mean-square monthly miss. No bound is broken, nothing is held at 0, no row is subtracted to cancel $\lambda$, and the problem ends on a fit figure, not a shadow price (finding 20). It grades two l12 ideas: $\mathbf{Q}$ from the objective (part 1) and the long-only solver's answer (part 3).

Numbers: `problems-convex-numbers.py` replaces the two old blocks (method 2 for p-account-target: a central second difference, SLSQP in the original variables at targets 12, 30 and 60; for p-style-fit: 12 months of synthetic data with exactly the stated sums, built from the Cholesky factor of their Gram matrix, then $2\mathbf{X}^T\mathbf{X}$ and SLSQP with bounds on the data). 792 of 792, numbers_lib failures 0, exit 0. The reader's script: its blocks for the two removed problems are removed with a comment (FINDING lines 1, 2, 4 and 7 went with them); its continuity regex now also takes a capital "Part"; 683 checks, 0 FINDING lines, exit 0. Grep of the new keys and nouns (`{45}`, 0.957, $6\sqrt{x}$, podcast, search ads, style weights, value index, growth index) over `app/content`: no match in this course or its exams; the other hits are unrelated ($\sqrt{45}$, $\tfrac{45}{41.76}$).

Gates (session AF): validator 0 errors; on these sets only the three `O2-long-sentence` warnings the reader judged keeps. Voice scan 35: 0 and 0. `fresh-check --file`: 0 hits on each set; set 3 the same two advisories as before (p-variance-limit). `grade-all --file`: 15, 14 and 15 widgets, 0 failures. Playthrough `--problems` sets 1 to 3, desktop and `--mobile`: green; 440 px shots of the new problems read, no layout faults.

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

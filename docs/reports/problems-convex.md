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
# Level 4 (`problems-4.json`, added by the level 4 author; re-author and fix pass after `review-problems-convex-4.md`)

| Set | Item | Parts | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| 4 | p-curve-fit-backtrack | 5 | l14, l15 | 5 |
| 4 | p-sale-horizon | 4 | l14, l16 | 4 |
| 4 | p-variance-log | 4 | l14, l15, l17 | 5 |

13 parts, 12 typed (numeric), 1 choice. Skills `cv-descent`, `cv-duality`.

## Re-author and fix pass (level 4)

`p-curve-fit-log` was ruled `re-author` (its parts 3 to 5 ran l14 screen 4 and both parts of `e-rate-from-kappa`). It is replaced by `p-curve-fit-backtrack`: parts 1 and 2 (two logged factors turned back into curvatures 0.8 and 30) are kept with findings 1 and 2 applied; parts 3 to 5 are new. A logged gradient $(0.4, 0.06)$ at step 4 gives errors 0.5 and 0.002; the Armijo test then accepts $s = 0.5$, 7.5 times the fixed-step limit $2/30$, because the gradient lies along the gentle direction (part 3). The level error is multiplied by $-14$, the gradient turns to the steep direction, and the next accepted step is $0.03125$ (part 4). The two steps take the excess from 0.10006 to 0.0343, which the fixed step 0.05 needs 14 steps to match (part 5, the excess shrinking by $0.96^2 = 0.9216$ a step). Findings 6 to 13 and 15 were applied as the reader wrote them, after recomputing; findings 3, 4, 5 and 14(a) fell away with the replaced parts. Keys unchanged outside the new parts.

## Gates (level 4)

- Validator: 0 errors. On `problems-4.json`: `O2-long-sentence` once (`p-sale-horizon` part 4, judged by the reader to stand) and `[wrong-band]` twice, on the slip bands the review narrowed (0.075 at 0.0005, 0.0793 at 0.005). Both slips are values in other units from a key asked as a whole number; the band the rule asks for (0.5) is the one finding 2 and 10 showed takes unrelated answers. Kept; inbox bullet.
- Voice scan 35 on the course folder: 0 and 0.
- Number script: `level4()` rewritten for the new problem and the fixed lines; whole script 799 of 799, numbers_lib failures 0, exit 0. Method 1 for parts 3 and 4: the Armijo test on a quadratic holds exactly for $s \le \lVert g\rVert^2/g^T\mathbf{H}g$ (0.693, then 0.036), in fractions; method 2: the trial steps run on $f$ in floats. Part 5: first $k$ in fractions and a float loop of the fixed run. The two narrowed bands are asserted.
- Reader's script `problems-convex-4-numbers-read.py`: checks A3 to A5 and the reuse rows of findings 3 and 4 removed with the parts they read (said so in the script); A2 band and B4 thousands band tightened to the new values; 118 checks, 0 failed, no FINDING line, exit 0.
- `fresh-check.mjs --file`: 0 hits, 2 advisories judged: 0.05 and 0.06 shared with l11 screen 5 (returns there, a step and a gradient here); the Armijo test of l14 screen 8, which the stem must state.
- `grade-all.mjs --file`: 13 widgets, 0 failures.
- Playthrough `--problems convex/problems-4`, desktop and `--mobile`: green; 440 px shots of the new parts read, no layout faults.
- Hand greps of 0.10006, 0.0343, 0.9216, 0.7632, 0.1636, 0.04776 and 0.03125 over the course and every exam with convex items: only 0.03125, in `topic-1.6` and `topic-1.7` in unrelated roles. "Backtrack" and "Armijo" occur in the course only in l14 screen 8 and quiz 2.

## Closest course material per problem (level 4)

- p-curve-fit-backtrack. Lesson: l14 screens 0 and 2 (factor $1 - s\lambda$, limit $2/\lambda_{\max}$), l14 screen 8 (backtracking steps in order), l15 screen 2 (counts from a rate). Quiz: l14 q2 (backtracking on $2x^2$ at $x = 1$ accepts 0.25). Review: r4-factor, r4-count ($\rho = 0.8$ to $10^6$). Homework: h4-rho. Exam: `e-rate-from-kappa`, `e-step-limit` (topic 2.5). Verdict clean: the course runs backtracking once in one variable and teaches that the test holds once $s \le 1/L$. Here the test runs twice in two variables, accepts a step far past the fixed-step limit and then a sixteenth of it, and the result is how many fixed steps two such steps are worth. No balanced step, no $\rho$ from $\kappa$, no count to a power of ten. Slip lines were written against l14 screen 8's `d1`, `d2` and line 6 `why`, and l14 screen 2's `one` line, and share no sentence.
- p-sale-horizon. Lesson: l14 screen 7, l16 screens 0, 3, 6, 9 and 11. Quiz: l16 q0. Review: r4-newton. Homework: h4-newton-iter, h4-kelly-even. Exam: e-newton-minimise. Slip lines now the reader's (findings 6 to 8).
- p-variance-log. Lesson: l15 screens 1 and 5, l17 screens 3, 4 and 11. Quiz: l15 q1 and q2, l17 q2. Review: r4-backout. Homework: h4-bound, h4-stuck. Exam: e-rate-from-kappa, e-solver-certificate. Part 4 rewritten line by line (findings 13 and 15); slip lines of parts 1 and 3 the reader's (11, 12).

## Engine (level 4)

One inbox bullet under `Raised later (re-author and fix pass problems convex 4):` (`[wrong-band]` on a slip in other units).

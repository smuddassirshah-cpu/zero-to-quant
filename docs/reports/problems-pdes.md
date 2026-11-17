# Problem sets: pdes (session AG, Wave C)

Author report for `app/content/courses/pdes/problems-1.json` to `problems-3.json`. Number script `docs/reports/problems-pdes-numbers.py` (exit 0).

## Sets

| Set | Item | Parts | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| 1 | p-tick-spread | 4 numeric | l2, l3 | 3 |
| 1 | p-two-level-bar | 5 numeric | l3, l4 | 5 |
| 1 | p-grid-rod | 4 numeric | l4, l2 | 3 |
| 1 | p-drift-walk | 4 numeric | l1, l2, l3 | 4 |
| 2 | p-tent-rod | 4 numeric | l5, l6, l8 | 3 |
| 2 | p-exp-series | 5 numeric | l6, l7 | 5 |
| 2 | p-grid-modes | 4 numeric | l8, l5 | 4 |

Level 1: 4 problems, 17 parts, all typed. Every lesson of the level appears (l1 in p-drift-walk; l2 in three; l3 in three; l4 in two). Skill `pe-heat` throughout (the only skill of the level's lessons).

Level 2: 3 problems, 13 parts, all typed (one percentage part with unit "%"). l5 in two problems, l6 in two, l7 in one, l8 in two. Skills `pe-fourier` and `pe-heat`.

## Closest course items, per problem

Reuse scope: the level's lessons, quizzes, review and homework, every other set of the course, and the `pe-` items of `exams/topic-3.2.json` (no other exam file carries a `pe-` skill).

### Level 1

- **p-tick-spread** (D from ticks, spread over a minute, two-tailed chance, time to a spread of 24 pence).
  - Lesson: l2 screen 9 ($D$ from $\Delta x = 0.2$, $\Delta t = 0.01$) and screen 10 (log-price sd over three months). Here the walk is a mid price in ticks, and the chain goes on to a tail chance and an inverted $\sqrt{t}$ law.
  - Quiz: l3 quiz 1 (kernel width $\sqrt{2Dt}$ from $D$, $t$). One step; ours uses the width for a two-sided tail.
  - Review: review-1 items 2 and 3 ($D$ from a walk, then the sd at $t = 2$). Two steps in common; ours adds the tail chance and the time to a given spread, and has its own numbers and story.
  - Homework: homework-1 item 6 (longform, a walk with $\Delta x = \Delta t$ that does not diffuse). Ours is a well-posed walk, typed parts.
  - Exam: e-kernel-peak (peak height of a point source). Ours never uses the peak height.
- **p-two-level-bar** (two-level start scaled from the unit step, a value with a table $\Phi$, the position and the time of the level 75 by the quantile, the steady value on a finite bar).
  - Lesson: l3 screen 3 ($u(1, 0.5)$ for the unit step). Ours scales the step, then inverts it for a position and a time.
  - Quiz: l3 quiz 3 ($u(2, 2)$ with $D = \tfrac12$). Forward value only.
  - Review: review-1 item 5 ($u(-1, 1)$, unit step). Forward value only.
  - Homework: homework-1 item 2 (Gaussian start, $u(0, t)$). Different start and no inversion.
  - Exam: e-slab-heat (box start, $u(0, 0.75)$). Different start, forward only.
- **p-grid-rod** (stable step count, the explicit step at $\lambda = \tfrac12$ as the neighbour mean, three steps by hand, the off-centre steady value).
  - Lesson: l4 screen 8 (the explicit step in code) and screen 0 (rod 20 to 50, middle settles at 35). Ours runs three steps by hand with held non-zero ends and asks an off-centre steady value.
  - Quiz: l4 quiz 1 (stays between the end values). Ours asks values, not bounds.
  - Review: review-1 item 7 (insulated rod settles at the mean). Ours has held ends and a line.
  - Homework: homework-1 item 4 ($\lambda = 0.6$, zero ends, two steps, a negative entry). Ours is the stable $\lambda = \tfrac12$ with non-zero ends.
  - Exam: e-heat-grid-steps (fewest stable steps for heat time 0.03675, $\Delta x = 0.04$) and e-explicit-code (code). Ours has its own numbers and goes on to the grid values and the steady state.
- **p-drift-walk** (drift speed from a biased walk, a residual test with a cancelling drift, a moving-kernel tail, the time the left tail falls to 1%).
  - Lesson: l2 screen 7 ($c$ for $q = 0.55$) and l1 screen 3 (which candidate has zero residual for $u_t = u_{xx}$). Ours finds the decay rate of a drifting candidate in the drift-diffusion equation.
  - Quiz: l1 quiz 0 (residual of $(1 - t)\sin x$). Heat equation only, one number.
  - Review: review-1 item 1 ($c$ in $e^{-ct}\sin 3x$). No drift term.
  - Homework: homework-1 item 1 (derivation that $u(x - ct, t)$ solves the drift equation). Ours uses the moving kernel numerically, no derivation.
  - Exam: none closer than e-kernel-peak.

### Level 2

- **p-tent-rod** (decay rate of the slowest mode on a rod of length 2, $b_1$ of a tent by integration, the centre from two terms, the time the centre falls to 1).
  - Lesson: l8 screen 0 (rod at 100, read the time the centre reaches 50 off a slider) and l5 screen 9 (rate of $\sin 2x$ with $D = 2$). Ours computes the coefficient of a tent and solves for the time by logs.
  - Quiz: l8 quiz 0 (centre with the $k = 1$ and $k = 3$ terms of the 100-degree rod). Same standard step with a new start, coefficients the learner derives, and the sign of $\sin(3\pi/2)$ as the trap.
  - Review: review-2 item 0 ($\lambda_2$ for $L = 3$) and item 7 (start 40 by scaling). One step each.
  - Homework: homework-2 item 2 (ends 10 and 70, sum $k = 1$ and 3). Different start and no time inversion.
  - Exam: e-rod-centre (length 3, start given as two modes). Ours derives the modes from a tent.
- **p-exp-series** ($b_1$ of $e^x$ by parts, $b_3$ from the general form, the decay slope, the midpoint $\cosh\pi$ at the jump, and the sum $\sum 1/(1 + k^2)$ read off the midpoint).
  - Lesson: l6 screens 3 and 5 (square-wave $b_k$, $a_3$ of $|x|$), l7 screen 2 (slopes $-1$ and $-2$), l7 screen 7 ($f = x$ at $x = \pi$ gives 0). Ours works on $e^x$, whose jump midpoint is not 0, and turns the midpoint into a series sum.
  - Quiz: l7 quiz 1 (midpoint of 2 and 8) and l6 quiz 1 (Leibniz sum from $f = x$ at $\pi/2$). Ours sums $\sum 1/(1 + k^2)$, a series no course item sums.
  - Review: review-2 item 4 (coefficients like $1/k^2$ mean a kink) and item 5 (Parseval for $|x|$). Ours reads the slope from a formula and uses the pointwise value, not Parseval.
  - Homework: homework-2 item 3 (statements on the square wave from $-3$ to 3). Choice only.
  - Exam: e-jump-gibbs (midpoint and Gibbs peak of a jump from 1 to 7). A first draft ended on the Gibbs peak, which walked through this exam item; it now ends on the series sum instead, so only the midpoint step is shared.
- **p-grid-modes** ($\lambda$ on a 12-interval rod, the grid factor of the smooth mode, its size after 50 steps, the percentage it lags the exact $e^{-1.5}$).
  - Lesson: l8 screen 4 ($\Delta t_{\max}$ as an expression) and screen 5 (top-mode factor at $\lambda = 0.6$, unstable). Ours takes the smooth mode at a stable $\lambda$ and measures its accuracy, not its growth.
  - Quiz: l8 quiz 1 and quiz 2 (largest stable step for $N = 10$; the $-1.34$ factor). A first draft opened with the largest stable step; it was dropped to keep clear of these and review-2 item 6.
  - Review: review-2 item 6 (largest stable step, $N = 20$, $D = 0.5$). Not asked here.
  - Homework: homework-2 item 5 (step count of `rod_explicit`). Different question.
  - Exam: e-explicit-code (code). Different task.

## Fresh-check

- problems-1: 0 hits, 4 advisory: the explicit-step formula (shared with l4 screen 8 and homework-1 item 4), the drift formula $c = (2q - 1)\Delta x/\Delta t$ (l2 screen 7, restated as the model, not a retold chain), and the parameter pair 0.25 and 0.02 also in l2 screen 10 (a different story: $D = 0.02$ there, $\Delta t = 0.02$ here). Judged clean.
- problems-2: 0 hits, 2 advisory: $\cos k\pi = (-1)^k$ (l6 screen 3, a stock identity) and the grid factor $1 - 4\lambda\sin^2(k\Delta x/2)$ (l8 screen 4, the model the problem uses). A first draft drew one `rate` error: the Gibbs fraction 8.95% against 0.0895 in l7 screen 1, with 1.179 in both (a slip line quoted 1.179). That part was replaced by the series sum, so the constant no longer appears.

## Gates

| Set | Validator | Voice 35 | fresh-check | Numbers | grade-all | Playthrough | `--mobile --why` |
|---|---|---|---|---|---|---|---|
| 1 | 0 errors, no pass-8 warnings (one advisory O2) | 0 and 0 | 0 errors | exit 0 | 0 failures (17 widgets) | green | green, 34 slips routed |
| 2 | 0 errors, no pass-8 warnings (two advisory O2) | 0 and 0 | 0 errors | exit 0 | 0 failures (13 widgets) | green | green |

Screenshots at 440 px read: no overflow, maths wraps inside the column.

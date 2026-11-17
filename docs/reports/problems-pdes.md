# Problem sets: pdes (session AG, Wave C)

Author report for `app/content/courses/pdes/problems-1.json` to `problems-3.json`. Number script `docs/reports/problems-pdes-numbers.py` (exit 0).

## Sets

| Set | Item | Parts | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| 1 | p-tick-spread | 4 numeric | l2, l3 | 3 |
| 1 | p-two-level-bar | 5 numeric | l3, l4 | 5 |
| 1 | p-grid-rod | 4 numeric | l4, l2 | 3 |
| 1 | p-drift-walk | 4 numeric | l1, l2, l3 | 4 |

Level 1: 4 problems, 17 parts, all typed. Every lesson of the level appears (l1 in p-drift-walk; l2 in three; l3 in three; l4 in two). Skill `pe-heat` throughout (the only skill of the level's lessons).

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

## Fresh-check

- problems-1: 0 hits, 4 advisory: the explicit-step formula (shared with l4 screen 8 and homework-1 item 4), the drift formula $c = (2q - 1)\Delta x/\Delta t$ (l2 screen 7, restated as the model, not a retold chain), and the parameter pair 0.25 and 0.02 also in l2 screen 10 (a different story: $D = 0.02$ there, $\Delta t = 0.02$ here). Judged clean.

## Gates

| Set | Validator | Voice 35 | fresh-check | Numbers | grade-all | Playthrough | `--mobile --why` |
|---|---|---|---|---|---|---|---|
| 1 | 0 errors, no pass-8 warnings (one advisory O2) | 0 and 0 | 0 errors | exit 0 | 0 failures (17 widgets) | green | green, 34 slips routed |

Screenshots at 440 px read: no overflow, maths wraps inside the column.

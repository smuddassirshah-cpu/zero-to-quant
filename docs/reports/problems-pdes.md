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
| 3 | p-call-heat | 4 numeric | l9, l10 | 4 |
| 3 | p-fk-claim | 5 numeric | l9, l11, l10 | 5 |
| 3 | p-grid-no-formula | 4 numeric | l12, l10 | 4 |

Level 1: 4 problems, 17 parts, all typed. Every lesson of the level appears (l1 in p-drift-walk; l2 in three; l3 in three; l4 in two). Skill `pe-heat` throughout (the only skill of the level's lessons).

Level 2: 3 problems, 13 parts, all typed (one percentage part with unit "%"). l5 in two problems, l6 in two, l7 in one, l8 in two. Skills `pe-fourier` and `pe-heat`.

Level 3: 3 problems, 13 parts, all typed. l9 in two problems, l10 in three, l11 in one, l12 in one. Skills `pe-bs`, `pe-heat`, `pe-fk`, `pe-fd`. The Crank-Nicolson prices of p-grid-no-formula come from the lesson 12 scheme (heat variables on $[-1, 1]$, $n_t = n_x/5$, zero left edge, exact right edge); the number script's own solver reproduces the lesson's £10.4427214 and £10.4486123 and the three stated prices to $5 \times 10^{-8}$.

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

### Level 3

- **p-call-heat** (heat time today, $k$, the lemma argument $d_1$ from $x$, $a$ and $\tau$, the price with given $\Phi$ values; $S = 80$, $K = 75$, $r = 4\%$, $\sigma = 25\%$, $T = 0.8$).
  - Lesson: l10 screen 4 (the $S = 110$ price with $d_1$, $d_2$ and $\Phi$ given). Ours builds $d_1$ from the heat variables first, for an off-the-money strike.
  - Quiz: l9 quiz 0 ($\tau$ for a two-year 30% option) and l10 quiz 0 (lemma argument for $x = 0.1$, $\tau = 0.02$, $a = 1.75$). One step each; ours chains them to the price.
  - Review: review-3 items 0 to 2 ($k$, $\beta$, kernel sd for $r = 4\%$, $\sigma = 30\%$, $T = 0.5$). Ours shares the $k$ step only, then goes to $d_1$ and the price.
  - Homework: homework-3 item 1 (order the change of variables). No numbers.
  - Exam: e-heat-change ($\alpha$, $\beta$ for $r = 6\%$, $\sigma = 25\%$). Ours asks neither.
- **p-fk-claim** (heat time of a Feynman-Kac equation, the variance of $X_T$ as $2\tau$, $E[e^{X_T}]$, the discounted value, and a simulation run in standard errors).
  - Lesson: l11 screen 1 ($E[(x + W_t)^2]$), screen 3 (read $\mu$ and $\sigma$ off the equation), screen 4 (standard error of a batch of 2,000). Ours has a drifted process, an exponential payoff and the link to heat time.
  - Quiz: l11 quiz 0 ($E[(x + W_t)^3]$). One step, no discount.
  - Review: review-3 item 5 (standard error from sd £14.70 and 20,000 paths). Ours asks how far a run sits from the value, in standard errors.
  - Homework: homework-3 item 4 (Vasicek bond). Different model.
  - Exam: e-fk-square ($dX = 0.5\,dt + 1.2\,dW$, payoff $x^2$, $r = 10\%$) and e-fk-reverting (mean-reverting drift, payoff $x$). Same standard task, Feynman-Kac for a Gaussian process; ours has its own drift, volatility, rate and an exponential payoff, and adds the heat-time and simulation steps.
- **p-grid-no-formula** (observed order from three grids without the formula, the shortfall of the finest grid, the extrapolated price, the put by parity).
  - Lesson: l12 screen 3 (errors against the formula, times $10^6$) and screen 4 (Richardson on 100 and 200 intervals). Ours never uses the formula: the order comes from differences, and the shortfall is estimated, not measured.
  - Quiz: l12 quiz 0 (order from two errors). Ours uses two differences of prices instead.
  - Review: review-3 item 7 (Richardson on 200 and 400 for $S = K = 100$, $r = 3\%$, $\sigma = 25\%$) and item 3 (put by parity). Separate items in the review; ours chains them through the order and the shortfall, on its own option.
  - Homework: homework-3 item 6 (smallest grid with error below $5 \times 10^{-5}$). Not asked here.
  - Exam: e-explicit-code and e-heat-grid-steps (explicit scheme). Different scheme and task.

## Fresh-check

- problems-1: 0 hits, 4 advisory: the explicit-step formula (shared with l4 screen 8 and homework-1 item 4), the drift formula $c = (2q - 1)\Delta x/\Delta t$ (l2 screen 7, restated as the model, not a retold chain), and the parameter pair 0.25 and 0.02 also in l2 screen 10 (a different story: $D = 0.02$ there, $\Delta t = 0.02$ here). Judged clean.
- problems-2: 0 hits, 2 advisory: $\cos k\pi = (-1)^k$ (l6 screen 3, a stock identity) and the grid factor $1 - 4\lambda\sin^2(k\Delta x/2)$ (l8 screen 4, the model the problem uses). A first draft drew one `rate` error: the Gibbs fraction 8.95% against 0.0895 in l7 screen 1, with 1.179 in both (a slip line quoted 1.179). That part was replaced by the series sum, so the constant no longer appears.
- problems-3: 0 hits, 6 advisory: $k = 2r/\sigma^2$ (homework-3 item 1, review-3 item 0, exam e-heat-change), the Black-Scholes formula (l10 quiz 3), and $n_t = n_x/5$ (l12 screen 3, homework-3 item 6). All are the course's notation for the model, restated so each problem stands alone. Judged clean.
- Second check by grep: the stories (tick walk, two-level bar, tent rod, $e^x$ series, exponential claim, convergence without a formula), the option parameters (80, 75, 4%, 25%, 0.8; 50, 50, 3%, 24%, 0.5) and each key number were grepped in `app/content/courses/pdes/` and `exams/topic-3.2.json`: no match beyond the advisories above.

## Gates

| Set | Validator | Voice 35 | fresh-check | Numbers | grade-all | Playthrough | `--mobile --why` |
|---|---|---|---|---|---|---|---|
| 1 | 0 errors, no pass-8 warnings (one advisory O2) | 0 and 0 | 0 errors | exit 0 | 0 failures (17 widgets) | green | green, 34 slips routed |
| 2 | 0 errors, no pass-8 warnings (two advisory O2) | 0 and 0 | 0 errors | exit 0 | 0 failures (13 widgets) | green | green |
| 3 | 0 errors, no pass-8 warnings | 0 and 0 | 0 errors | exit 0 | 0 failures (13 widgets) | green | green |

Number script: 571 checks, 0 failures (two methods per value, every slip recomputed, stated figures matched as text, `check_wrongs` per set, set shape).

## Inbox

Two bullets under `Raised later (problems pdes):` in `docs/BACKLOG-INBOX.md`: the `rate` check on a universal constant, and the playthrough's message when the manifest lacks a new set.

## Course map

No `course.json` change proposed.

Screenshots at 440 px read: no overflow, maths wraps inside the column.

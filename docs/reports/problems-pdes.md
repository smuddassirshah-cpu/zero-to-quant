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
| 3 | p-straddle-vol | 1 expression, 3 numeric | l9, l10 | 4 |
| 3 | p-log-contract | 1 expression, 3 numeric | l9, l11 | 5 |
| 3 | p-grid-budget | 4 numeric | l12, l11 | 4 |

Level 1: 4 problems, 17 parts, all typed. Every lesson of the level appears (l1 in p-drift-walk; l2 in three; l3 in three; l4 in two). Skill `pe-heat` throughout (the only skill of the level's lessons).

Level 2: 3 problems, 13 parts, all typed (one percentage part with unit "%"). l5 in two problems, l6 in two, l7 in one, l8 in two. Skills `pe-fourier` and `pe-heat`.

Level 3 (re-authored in session AF, review findings 6 to 8): 3 problems, 12 parts, all typed (two `expression`, two percentage parts with unit "%"). l9 in two problems, l10 in one, l11 in two, l12 in one; no lesson is in all three. Skills `pe-bs`, `pe-heat`, `pe-fk`, `pe-fd`. The Crank-Nicolson prices of p-grid-budget come from the lesson 12 scheme (heat variables on $[-1, 1]$, $n_t = n_x/5$, zero left edge, exact right edge); the number script's solver reproduces the lesson's £10.4427214 and £10.4486123 and the three stated prices to $5 \times 10^{-8}$, and the reader's dense solver agrees to $5 \times 10^{-7}$.

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
- **p-grid-rod** (stable step count, the explicit step at $\lambda = \tfrac12$ as the neighbour mean, three steps by hand, how far the grid still sits above the off-centre steady value).
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
- **p-grid-modes** ($\lambda$ on a 12-interval rod with $D = 0.75$ and $\Delta t = 0.04$, the grid factor of the smooth mode, its size after 40 steps, the percentage it lags the exact $e^{-1.2}$; renumbered in session AF, review finding 9).
  - Lesson: l8 screen 4 ($\Delta t_{\max}$ as an expression) and screen 5 (top-mode factor at $\lambda = 0.6$, unstable). Ours takes the smooth mode at a stable $\lambda$ and measures its accuracy, not its growth.
  - Quiz: l8 quiz 1 and quiz 2 (largest stable step for $N = 10$; the $-1.34$ factor). A first draft opened with the largest stable step; it was dropped to keep clear of these and review-2 item 6.
  - Review: review-2 item 6 (largest stable step, $N = 20$, $D = 0.5$). Not asked here.
  - Homework: homework-2 item 5 (step count of `rod_explicit`). Different question.
  - Exam: e-explicit-code (code). Different task.

### Level 3

Re-authored in session AF. The review ruled all three first-draft problems a walk of course items in the lessons' own order (findings 6 to 8); the new problems share no setting, number set or chain with them or with any course item.

- **p-straddle-vol** ($r = 0$, $S = K = 80$, nine months, a straddle at £9.60: the lemma argument as an expression, $\Phi$ from the quote, the heat time by $\Phi^{-1}$, the implied volatility 17.38%).
  - Lesson: l9 screen 8 ($r = 0$ edge case: equal heat time gives an equal price) and l10 screen 2 (the lemma arguments at $x = 0$, $\tau = 0.02$, as numbers). Ours simplifies the argument symbolically, then runs the route backwards from a market quote to $\tau$ and $\sigma$.
  - Quiz: l10 `q-arg` (argument for $x = 0.1$, $\tau = 0.02$, $a = 1.75$, forward). Ours asks the form $\sqrt{\tau/2}$ and later inverts it.
  - Review: `r-put` (put by parity). Ours uses parity only to split a straddle at $r = 0$ into equal legs; no put price is asked.
  - Homework: `h-r0-sigma` ($r = 0$, matching total variance between two options). Ours reads the volatility from one price through $\Phi^{-1}$.
  - Exam: `e-heat-grid-steps` part 1 ($\tau$ forward from $\sigma$ and $T$). Ours inverts $\tau$ to $\sigma$; no step count.
- **p-log-contract** (a claim paying £1,000 $\ln(S_T/K)$, $K = S_0 = 64$, $\sigma = 28\%$, $r = 2\%$, $T = 1.5$: the constant $c = k - 1$ of a trial solution of the scaled equation, the value $-$£27.95, the break-even rise 2.92%, the chance 0.4665 of a positive payoff).
  - Lesson: l9 screens 3 and 4 ($k$ and the $v_x$ coefficient $k - 1$) and l11 screen 3 (read $\mu$ and $\sigma$ off the equation). Ours puts a trial solution into the scaled equation, then reads it in heat time as a drifted normal.
  - Quiz: l9 `q-coeff` (the $v_x$ coefficient as a number). Ours asks $c$ symbolically; $k - 1$ appears as a number only inside $(k - 1)\tau$.
  - Review: `r-k`, `r-sd`. Ours never asks $k$ or the kernel's spread on their own.
  - Homework: `h-vasicek`, `h-drift-sim`. Different claims and tasks.
  - Exam: `e-fk-reverting` and `e-fk-square` (read a process off a Feynman-Kac equation, take the mean or second moment, discount). Ours gets the value from the trial solution in one step, with no read-mean-discount chain; Feynman-Kac enters only in part 4, for a probability. The first draft's mean-then-discount split was merged for this reason. A mock item in another course (`mock-superday-strats` `log-contract`, skills `it-`) prices $\ln S_T$ by Itô's lemma; ours works in the heat variables and asks other quantities.
- **p-grid-budget** ($S = K = 120$, $r = 4.5\%$, $\sigma = 18\%$, $T = 1.25$: the order from two differences, the 400 grid's shortfall, the shortfall on 16 times the work, and the 256 times the paths a simulation needs for the same cut).
  - Lesson: l12 screen 3 (errors against the formula, times $10^6$) and l11 screen 4 (standard error rescaled from 100,000 to 2,000 paths). Ours never uses the formula and compares how work buys accuracy on the grid and by simulation.
  - Quiz: l12 `q-order` (order from two errors). Ours uses two differences of prices.
  - Review: `r-rich` (Richardson) and `r-se` (standard error from $s$ and $n$). Ours computes neither an extrapolated price nor a standard error from data.
  - Homework: `h-sequence` (smallest halving grid under a tolerance). Ours fixes the budget and predicts the shortfall; no tolerance search.
  - Exam: `e-heat-grid-steps` and `e-explicit-code` (explicit scheme). A numerics exam item outside the course, `topic-2.5` `e-error-budget`, chains Richardson, the grid error and the paths for a standard error from a payoff sd; ours asks no extrapolated price, no payoff sd and no path count, so the chains differ (found by grep: `fresh-check` reads only the course's own exams).

## Fresh-check

- problems-1: 0 hits, 4 advisory: the explicit-step formula (shared with l4 screen 8 and homework-1 item 4), the drift formula $c = (2q - 1)\Delta x/\Delta t$ (l2 screen 7, restated as the model, not a retold chain), and the parameter pair 0.25 and 0.02 also in l2 screen 10 (a different story: $D = 0.02$ there, $\Delta t = 0.02$ here). Judged clean.
- problems-2: 0 hits, 2 advisory: $\cos k\pi = (-1)^k$ (l6 screen 3, a stock identity) and the grid factor $1 - 4\lambda\sin^2(k\Delta x/2)$ (l8 screen 4, the model the problem uses). A first draft drew one `rate` error: the Gibbs fraction 8.95% against 0.0895 in l7 screen 1, with 1.179 in both (a slip line quoted 1.179). That part was replaced by the series sum, so the constant no longer appears.
- problems-3 (session AF): 0 hits, 6 advisory: $k = 2r/\sigma^2$ (homework-3 item 1, review-3 item 0, exam e-heat-change), $n_t = n_x/5$ (l12 screen 3, homework-3 item 6), and the parameters 120, 1.25, 400 shared with a SQL table in `exams/stage-1.json` (chance). Judged clean.
- Second check by grep: the stories (tick walk, two-level bar, tent rod, $e^x$ series, straddle, log claim, grid against simulation), the level 3 parameters (80, 9.60, 0.75; 64, 28%, 2%, 1.5; 120, 4.5%, 18%, 1.25) and each key number (0.07527, 0.01133, 17.38, 27.95, 0.0288, 2.92, 0.4665, 557.6, 34.85) were grepped in `app/content/courses/pdes/` and `exams/topic-3.2.json`: no match beyond the advisories above. Across `app/content/`, "straddle" and "log contract" stories exist only in other courses (named above).

## Gates

| Set | Validator | Voice 35 | fresh-check | Numbers | grade-all | Playthrough | `--mobile --why` |
|---|---|---|---|---|---|---|---|
| 1 | 0 errors, no pass-8 warnings (two advisory O2, one from the reader's text) | 0 and 0 | 0 errors | exit 0 | 0 failures (17 widgets) | green | green |
| 2 | 0 errors, no pass-8 warnings (two advisory O2) | 0 and 0 | 0 errors | exit 0 | 0 failures (13 widgets) | green | green, 28 slips routed |
| 3 | 0 errors, no warnings | 0 and 0 | 0 errors | exit 0 | 0 failures (12 widgets: 2 expression, 10 numeric) | green | green, 30 slips routed |

Gates rerun in session AF after the fix pass. Number script: 637 checks, 0 failures (two methods per value, every slip recomputed, stated figures matched as text and, for level 3, printed products and quotients recomputed at full precision and rounded with `shown`, `check_wrongs` per set, set shape). The reader's script: 716 checks, 0 `FINDING` lines; its checks of the three replaced problems were removed and its solver check retargeted to p-grid-budget.

## Inbox

Two bullets under `Raised later (problems pdes):` in `docs/BACKLOG-INBOX.md`: the `rate` check on a universal constant, and the playthrough's message when the manifest lacks a new set. Session AF adds one under `Raised later (problems pdes, session AF):`: `fresh-check` does not read other courses' exams, where a chain walk (`e-error-budget`) was found only by grep.

## Course map

No `course.json` change proposed.

Screenshots at 440 px read: no overflow, maths wraps inside the column.

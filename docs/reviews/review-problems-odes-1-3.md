# Problem sets 1.11, odes levels 1 to 3: second-reader findings

Scope: `app/content/courses/odes/problems-1.json`, `-2`, `-3`: 9 problems, 40 parts (27 numeric, 10 `expression`, 3 choice), 82 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Author rules, Reader). Pattern: `review-problems-analysis-1-3.md`. `problems-4.json` belongs to another reader and was not read.

Method. The author's script was run first. Every equation was then typed from the item's prose into `docs/reports/problems-odes-numbers-read.py`, which imports nothing from the author's script. Route 1 is sympy: `dsolve` on each of the eight equations (the logistic-type equation, the moving-target and pension linear equations, the three second-order equations with their starts, the trend equation with a free slope), each solution put back into its equation, the matrix exponential for the yield system, `solve` and `jacobian` for the nonlinear system. Route 2 is `scipy.solve_ivp` (rtol 1e-11) on every equation: the time membership reaches 5 by `brentq` on the path, the trough of the rate by a bounded minimiser, the hedge's first peak as the first zero of the computed velocity and as the highest point of the path, the buffer at $\tfrac{\pi}{2}$, the gap at 0.5, the ratio $y/x$ at $t = 6$, and the turn time of the nonlinear path near $(2, 4)$ from successive crossings of $x = 2$. Each stability and phase-plane class is read from $\tau$ and $\Delta$ by the reader's `classify`, checked against `numpy` eigenvalues, and for the two nonlinear claims against the integrated path (a near start and a far start both end at $(2, 4)$; starts either side of $m = 2$ and $m = 6$ go where the test says). Every `wrong` value is rebuilt from the slip its line names; every number printed in a question, feedback, `why` or `explain` string is formatted from the reader's value and looked for in the string. `review-problems-odes-1-3-scripts/grade-probe.mjs` then runs every typed part through the real widget files, as `grade-all.mjs` boots them: key, each `accept`, each `wrong` on its own line, and 246 strings of my own (the asked rounding and the next coarser, fractions, other forms of each expression, a letter and `=`, a set in either order, matrices both ways). Reuse was read by eye with `fresh.py` (numbers, functions and nouns of each problem across the course and `app/content`), `mats.py` (every 2 by 2 numeric matrix of the course against the three of level 3, up to a scalar, a transpose and a swap of coordinates, and by trace and determinant) and `fresh-check.mjs --file` with and without `--cross-numbers`; the three scratch scripts are in the scratchpad `read-odes` folder.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-odes-numbers.py` 547 of 547, exit 0 |
| `problems-odes-numbers-read.py` (reader's keys, slips, printed numbers, set shape, bands) | 518 checks, 4 failures, exit 1: findings 1, 2, 3 and 4 (each check fails on the content as it stands and passes once fixed); 1 CLAIM line (finding 3) |
| `grade-probe.mjs` (real widgets, 37 typed parts) | 456 of 456 as expected, 246 reader rows, exit 0 |
| `grade-all.mjs --file`, three sets | 13, 13 and 14 widgets, 0 failures |
| validator | 0 errors, 4532 warnings, none on the three files; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file` (same-course mode), three sets | 0 hits, 0 `[same-course-reuse]` lines; 0, 0 and 4 advisories, read below |
| `fresh-check.mjs --file --cross-numbers` | 0 hits; 1, 4 and 0 further advisories, read below |
| browser, `playthrough.mjs` | not run (reader rule) |

Result. All 37 typed keys and the 3 choice keys agree with mine, by both routes, and so does every one of the 82 `wrong` values and every printed number. No learner is marked wrongly: no `wrong`-severity finding. Every band takes the asked rounding of its key and of each slip, no slip band touches a key band or another slip band. Three lines say something that is not quite true or carry a stray letter (findings 1 to 3), two are wording against the course (4, 5) and three later parts restate less than they use (6 to 8). The five near-reuses the author changed are all clear, and no new reuse was found.

## Findings

Format: `N. file | JSON path | severity | problem | evidence | exact fix`.

1. `odes/problems-1.json` | `items[0].parts[2].explain.text` (`p-lending-members` part 3) | misleading | The two integrals are written in $dq$; the variable is $m$. A leftover of the first version of the item (a venue's depth). | "$\int \tfrac{dq}{m - 2} = \ln|m - 2|$ and $\int \tfrac{dq}{6 - m} = -\ln|6 - m|$": no $q$ exists in the item. | `explain.text`: "$\int \tfrac{dm}{m - 2} = \ln|m - 2|$ and $\int \tfrac{dm}{6 - m} = -\ln|6 - m|$. So $\tfrac14\ln\left|\tfrac{m - 2}{6 - m}\right| = t + C$. Multiply by 4 and take exponentials: $k = 4$."

2. `odes/problems-1.json` | `items[0].parts[1].explain.text` (`p-lending-members` part 2) | misleading | "a small gap $u$ obeys $u' = f'(m^*)u$" states the linear law as exact. | With $u = m - 6$ the gap obeys $u' = -4u - u^2$ exactly (checked in the script), so the linear law holds only near the equilibrium. l4's summary says "a small gap nearly obeys $u' = f'(y^*)u$". | `explain.text`: "Near an equilibrium a small gap $u$ nearly obeys $u' = f'(m^*)u$. $f'(6) = -4$ shrinks it and $f'(2) = 4$ grows it. Membership that starts at 2.5 therefore heads for 6."

3. `odes/problems-2.json` | `items[2].parts[3].explain.text` (`p-tracking-gap` part 4) | misleading | "the gap never crosses zero, as critical damping promises". Critical damping promises no oscillation, not no crossing: $(c_1 + c_2t)e^{-5t}$ crosses zero once when $c_2 < 0$. | $c_2 = x'(0) + 10$, so from $x(0) = 2$ any start steeper than $x'(0) = -10$ crosses. The script integrates $x'(0) = -12$: $x = (2 - 2t)e^{-5t}$ is negative after $t = 1$. l9's "never overshoots" is said of the step response from rest. This path does stay positive ($2 + 6t > 0$), so only the reason is wrong. | `explain.text`: "$2 + 6 \times 0.5 = 5$ and $e^{-2.5} = 0.082085$, so $x(0.5) = 0.4104$. Since $2 + 6t > 0$ for $t \ge 0$, this gap never crosses zero. A start steeper than $x'(0) = -10$ would make $c_2$ negative and cross once."

4. `odes/problems-2.json` | `items[0].parts[0].explain.text` (`p-hedge-overshoot` part 1) | voice | "underdamped" against the course's "under-damped". | l9, l12 and review-3 all hyphenate; no lesson has the closed form. | Last sentence of `explain.text`: "Complex roots with a negative real part mean the hedge is under-damped."

5. `odes/problems-2.json` | `items[0].parts[4].explain.text` (`p-hedge-overshoot` part 5) | voice | "That is the damping rule ..." names a rule the course never names, and $\zeta$ appears without its source. | l9 teaches "The first peak overshoots by $e^{-\zeta\pi/\sqrt{1 - \zeta^2}}$" with $\zeta = \tfrac{b}{2\omega_0}$; "damping rule" occurs nowhere in the course. Here $\zeta = \tfrac{4}{2\sqrt{29}} = \tfrac{2}{\sqrt{29}} = 0.3714$ and $\zeta/\sqrt{1 - \zeta^2} = \tfrac25$, so the formula gives $e^{-2\pi/5}$ (checked). | Last sentence of `explain.text`: "That is lesson 9's overshoot $e^{-\zeta\pi/\sqrt{1 - \zeta^2}}$ with $\zeta = \tfrac{b}{2\omega_0} = \tfrac{2}{\sqrt{29}}$."

6. `odes/problems-2.json` | `items[1].parts[3].question` (`p-cash-buffer` part 4) | continuity | The part restates $c_1$ and $c_2$ but not the solution they go into; $x_p$ and the form are only in part 3's question. | Brief: "each later part restates the value it needs". The other two problems of the set do it ("Using $x(t) = 2 - e^{-2t}(2\cos 5t + 0.8\sin 5t)$", "Using $x = (2 + 6t)e^{-5t}$"). | `question`: "Using $c_1 = -1.25$ and $c_2 = -3.75$ from part 3, $x = e^{-2t}(-1.25\cos t - 3.75\sin t) + 1.25\cos t + 1.25\sin t$. Find the buffer $x\left(\tfrac{\pi}{2}\right)$ in £ million. Give your answer to 3 decimal places." Key and lines unchanged ($x(\tfrac{\pi}{2}) = -3.75e^{-\pi} + 1.25 = 1.087948$).

7. `odes/problems-3.json` | `items[0].parts[1].question` (`p-yield-gaps` part 2) | continuity | "Using $\tau = -6$ and $\Delta = 5$ from part 1": part 1 asks only for $\Delta$; $\tau$ is met in part 1's `explain`, which a learner who was right may not open. | The value is given, so nobody is blocked; the attribution is off. | `question`: "Using $\Delta = 5$ from part 1 and the trace $\tau = -7 + 1 = -6$, find the eigenvalues of $\mathbf{A}$. Give both, separated by a comma."

8. `odes/problems-3.json` | `items[2].parts[2].question` (`p-trend-signal` part 3) | continuity | "Using $\tau = -4$ and $\Delta = -5$ from part 2": part 2 asks only for $\Delta$, and $\tau$ appears there only in the `trace` slip line. | As finding 7. | `question`: "Using $\Delta = -5$ from part 2 and the trace $\tau = 0 + (-4) = -4$, find the eigenvalues of $\mathbf{A}$. Give both, separated by a comma."

## Same-course reuse, read by eye

The five changes the author lists, each confirmed clear:

| change | now | check |
|---|---|---|
| `p-lending-members`: a trading venue (l4 screen 9, market share) | a peer-to-peer lending platform | "lending", "peer" occur nowhere else in `app/content`; $-m^2 + 8m - 12$, $(m - 2)(m - 6)$, $\ln 21$, 0.761 nowhere in the course |
| `p-cash-buffer`: a market maker's inventory (l6 screen 9) | a fund's cash buffer driven by subscriptions | "buffer", "subscription" nowhere else in `app/content`; $x'' + 4x' + 5x$, $r^2 + 4r + 5$, $-2 \pm i$, $10\cos t$, 3.75 as a constant nowhere in the course |
| `p-hedge-overshoot`: roots $-2 \pm 3i$ (l15's poles) | $-2 \pm 5i$ | no $-2 \pm 5i$, no 29, 58 or 11.6 as a coefficient in the course; l15 keeps $-2 \pm 3i$; review-3's $-2 \pm 0.5i$ is another pair |
| `p-liquidity-arbitrage`: equilibrium $(2, 3)$ (l13's swapped distractor) | $(2, 4)$ | $(2, 4)$ and $(6, 0)$ occur nowhere in the course; $x(6 - x - y)$, $y(x - 2)$, $\sqrt7$, 2.375 nowhere |
| `p-yield-gaps`: $\begin{pmatrix}0&-3\\1&-4\end{pmatrix}$ (transpose of review-3's) and a start near l10's $(5, 2)$ | $\begin{pmatrix}-7&2\\-6&1\end{pmatrix}$, start $(4, 2)$ | `mats.py`: of the 38 numeric 2 by 2 matrices of the course none equals it up to a scalar, a transpose or a swap of coordinates; $(4, 2)$ and the eigenvector $(1, 3)$ occur nowhere in the course |

Read and ruled to stand (DECISIONS session AB "same standard task, own setting and numbers"; session AC rulings):

- `p-lending-members` against l4 screen 7 ($y' = y^2 - 4$, equilibria $\pm 2$, $f' = \mp 4$): both have roots 4 apart, so both tests give $\pm 4$. The functions, the equilibria (2 and 6) and the stable one (the upper, not the lower) differ. Any quadratic with roots 4 apart shares this; not a shifted copy a learner would see.
- `p-moving-target` against l3 screen 6 (a ramp-forced linear equation with solution $\tfrac{x}{2} - 0.25 + 1.25e^{-2x}$): same standard task; the only shared figure is 1.25, a constant there and the speed here.
- `p-hedge-overshoot` against l9's step response ($\omega = 2$, $\zeta = 0.25$, 44%) and review-2: same standard task with its own $\omega_0^2 = 29$ and $\zeta = 2/\sqrt{29}$.
- `p-yield-gaps` against l10 screen 1: the `mats.py` hit of equal trace and determinant, $\begin{pmatrix}0&1\\-5&-6\end{pmatrix}$, is a wrong option there (the swapped companion of $y'' + 5y' + 6y$), not a worked matrix.
- `p-liquidity-arbitrage` against review-3 item 6 ($x' = x(1 - x) - xy$, $y' = y(x - 0.5)$, a stable spiral) and l13 screen 6 (crowded prey): the same model family, as l13 teaches it. The Jacobians $\begin{pmatrix}-0.5&-0.5\\0.5&0\end{pmatrix}$ and $\begin{pmatrix}-0.5&-1.5\\0.25&0\end{pmatrix}$ are not multiples of $\begin{pmatrix}-2&-2\\4&0\end{pmatrix}$, and the story (liquidity providers, arbitrage firms) is new. l4 screen 9 has the word "liquidity" in a venue story; no shared sentence.
- `p-trend-signal` part 4 against l11 quiz "Which start heads into the origin?": same standard task, another matrix.
- Fluency families: `fluency-l7` draws $\alpha \pm \beta i$ with $\alpha$ from $-4$ to 4 and $\beta$ from 1 to 5, and real roots from $-6$ to 6, so a draw can land on $-2 \pm 5i$, $-2 \pm i$ or the pairs $-1, -5$ and $1, -5$. A family that spans every small integer cannot be avoided; task shape, not an instance.

`fresh-check` advisories. Same-course mode, `problems-3`: `c_1=-1` against l7 screen 1 and against `problems-2` (a constant of a fitted solution, by chance, and the second is a prefix of $c_1 = -1.25$); $\tau^2 - 4\Delta$ against l12 screen 2 and homework-3 (the taught formula). `--cross-numbers`: `p-lending-members` against `mock-oa-trader-3` (2.5, 0.125, 3.5: a sum of reciprocals), `p-hedge-overshoot` against `eigen/problems-3` (a rank-1 fit of a sales table) and `mental` l12, `p-cash-buffer` against `convex` l16 and `testing` l18 (1.25, 2.5, 3.75: quarter multiples). All coincidence; no shared task.

Stories across `app/content`: "pension" (series review-3, ratio problems-1, markets, options: other courses, other tasks), "hedging rule" (testing homework-2 and review-2, a paired test), "liquidity providers" (micro l8), "trend-following" (garch l12), "bond yields" (markets l6, taylor problems-1, exp-log l10). No shared numbers or sentences.

## Verified

- Level 1. Equilibria 2 and 6, $f'(2) = 4$, $f'(6) = -4$; the integrated path from 2.5, 5.9 and 7.5 ends at 6 and from 1.99 leaves 2. `dsolve` gives $\tfrac{m - 2}{6 - m} = \tfrac17e^{4t}$; $m = 5$ at $\tfrac{\ln 21}{4} = 0.761131$ (path: same to 1e-8). $r = 2.52 + 0.6t + 2.48e^{-1.25t}$ is the `dsolve` solution; half-life 0.554518; trough at 1.313782 (minimiser on the path agrees), 2.37 half-lives, $r = \theta = 3.79$ there. $B = 100000(e^{0.04t} - e^{0.02t})$, $B(10) = 27042.19$; flat fund 24591.23 (`dsolve`), payments 22140.28 (`quad`); the differences £2,451 and £4,902 as printed.
- Level 2. Roots $-2 \pm 5i$, $x_p = 2$, $c_1 = -2$, $c_2 = -0.8$; $x' = 11.6e^{-2t}\sin 5t$ exactly; first peak $\tfrac{\pi}{5}$ is the highest point of the path; overshoot $e^{-2\pi/5} = 0.284610$, equal to l9's formula. Roots $-2 \pm i$, $A = B = 1.25$, $c_1 = -1.25$, $c_2 = -3.75$, $x(\tfrac{\pi}{2}) = 1.087948$. $b = 10$ (9 oscillates, 11 has a slower mode), root $-5$, $x = (2 + 6t)e^{-5t}$, $x(0.5) = 0.410425$.
- Level 3. $\begin{pmatrix}-7&2\\-6&1\end{pmatrix}$: $\tau = -6$, $\Delta = 5$, $\tau^2 - 4\Delta = 16$, eigenvalues $-1, -5$, stable node; eigenvectors $(1, 3)$ and $(1, 1)$; $c = (-1, 5)$; the matrix exponential equals the printed solution; $y/x \to 3$. Equilibrium $(2, 4)$, $\mathbf{J} = \begin{pmatrix}-2&-2\\4&0\end{pmatrix}$ (also by central differences), $\tau = -2$, $\Delta = 8$, $-28$, stable spiral, turn $\tfrac{2\pi}{\sqrt7} = 2.374821$; the nonlinear path from $(2.001, 4)$ turns in 2.375 and a start at $(5, 1)$ also ends at $(2, 4)$. $\begin{pmatrix}0&1\\5&-4\end{pmatrix}$: $\Delta = -5$, saddle, eigenvalues $1, -5$; the growing mode vanishes only at $s'(0) = -5$; slopes $-4.9$, 1 and 5 blow up.
- Shape. 3 items a set, 13, 13 and 14 parts, difficulties 3, 4 and 5 in each set, skills `de-first`, `de-second`, `de-systems` as `course.json` gives them, typed parts 12 of 13, 13 of 13, 12 of 14. Lessons drawn on: l1 to l5, l6 to l9, l10 to l13, each at least once. Nothing beyond the level: integration by parts (integrals L3), complex roots (complex L1) and eigenvectors (eigen L4) are the levels' stated prerequisites.
- Judgement calls of the author's report. `p-moving-target` part 4 uses part 2, not part 3: stands (parts 3 and 4 both read the solution of part 2, the explain ties them, and the trough is the result the prose promises). `p-lending-members` part 3 gives the partial fractions: stands, as level 1's logistic screen does. `p-hedge-overshoot` part 4 gives $x'$: stands and is correct. `p-liquidity-arbitrage` part 5 gives the eigenvalues: stands.

## Counts

| severity | count | findings |
|---|---|---|
| wrong | 0 | |
| misleading | 3 | 1, 2, 3 |
| reuse | 0 | |
| voice | 2 | 4, 5 |
| continuity | 3 | 6, 7, 8 |

## Engine

1. A numeric field drops a letter and `=` before a value (`k = 4`, `b = 10`, `r = -5`, `x_p = 2`, `c_1 = -1` all pass in the probe) but not a derivative label: `s'(0) = -5` on `p-trend-signal` part 4 is refused on the generic line, though the question asks for "$s'(0)$".
2. Finding 1 is a letter left behind when an item's story changed ($q$ for depth, now $m$). A validator advisory could list a differential `d<letter>` in an integral whose letter occurs nowhere else in the item.

Both are inbox bullets under `Raised later (review problems odes):`.

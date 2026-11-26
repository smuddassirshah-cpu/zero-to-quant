# Concept audit: multivar levels 1 to 3 (round 1)

Auditor: blind Fable reader, session 13. Commit read: ee5d8292. Stage 1 course, full ledger.

Scope: `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l1-two-inputs`, `fluency-l2-slicing`, `fluency-l3-second-partials` in `app/content/courses/multivar/`.

Outputs: this file, the ledger `docs/reports/audit-multivar-1-3-ledger.md`, the script `docs/reports/multivar-L1-3-concepts.py`.

Sources: Apostol, *Calculus* vol. II (2nd ed.), ch. 8 and 9; Marsden and Tromba, *Vector Calculus*, ch. 2 and 3; Boyd and Vandenberghe, *Convex Optimization*, sections 4.4, 5.6 and 9.3; Hull, *Options, Futures and Other Derivatives*, ch. 19.

## Verdict

The mathematics taught is sound. Every graded key is right, every slip value is the value of the mistake its feedback names, and no wrong option is correct under a convention the item states. I found no wrong definition, formula or number.

The findings are of three kinds. Two results are stated without the condition that makes them true, in places where the watch list asked me to look: the gradient formula for directional derivatives (differentiability) and the Lagrange recipe (an extremum must exist, and $\nabla g \neq \mathbf 0$). Several lines say "always" where "usually" is true. Three code feedback lines name a mistake that fails a different test first.

Ledger: 2,877 rows; 2,843 correct, 3 wrong, 29 imprecise, 2 misleading, 0 unverified.

Findings: 15. By severity: wrong 3, imprecise 11, misleading 1. Serious 2, minor 13.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l6-any-direction.json` | `quiz[3]` (q-stationary): `prose`, the key `options[0]`, `options[1].why`, `explain`; also `screens[6].prose`, `summary.formula` | imprecise, serious | The item says that $D_{\mathbf u} f = 0$ along $(1, 0)$ and $(0, 1)$ forces every directional derivative to be 0, and marks "Only those two directions are level; others may not be" as wrong. That is true only for a differentiable $f$. Nothing in levels 1 to 3 says so, and the rejected option is the correct statement for a general function. A learner carries away "the two partials fix every slope", the classic false theorem. | Take $f = \frac{x^2 y}{x^2 + y^2}$ with $f(0, 0) = 0$. Then $f_x(0,0) = f_y(0,0) = 0$, but along $(1, 1)/\sqrt 2$ the slope is $\sqrt 2 / 4 \approx 0.354$ (script check [F1]). Apostol II 8.10 and 8.11: $f'(a; u) = \nabla f(a) \cdot u$ is proved for differentiable $f$, and partials alone do not give it. Marsden and Tromba 2.6. | Paste-ready. `screens[6].prose`: "Each time, you weighted the partials by the arrow's components. That sum is the **dot product** $\nabla f \cdot \mathbf u$: $$D_{\mathbf u} f = \nabla f \cdot \mathbf u = f_x u_1 + f_y u_2, \qquad |\mathbf u| = 1.$$ It holds for a smooth $f$, one whose partial derivatives are continuous. Every function in this course is smooth." `quiz[3].prose`: "At a point Q of a smooth function $f$, you find $D_{\mathbf u} f = 0$ for $\mathbf u = (1, 0)$ and for $\mathbf u = (0, 1)$." `quiz[3].widget.options[1].why`: "Those two slopes are $f_x$ and $f_y$. Both zero makes $\nabla f = (0, 0)$, and for a smooth $f$ every slope is $\nabla f \cdot \mathbf u = 0$." `summary.formula.note`: "$\mathbf u$ must have length 1: divide an arrow by its length first. $f$ must be smooth."

2. `l4-chain-two-inputs.json` | `summary.formula`, `screens[7].widget.lines[2].text`, `screens[7].explain`; `l7-tangent-planes.json` | `screens[2].prose` | imprecise, minor | The chain rule and the tangent plane are stated for any function with partial derivatives. Both need $f$ differentiable. The derivation line "each bracket moves one input only: a partial times its step" uses $f_x$ at $(x, y + \Delta y)$, not at $(x, y)$, so it needs $f_x$ continuous. This is where the convention first matters, so it should be said here once. | Same $f = \frac{x^2 y}{x^2 + y^2}$ on the path $(t, t)$: $f = t/2$, so $\frac{df}{dt} = \frac12$, while $f_x x' + f_y y' = 0$ at $t = 0$ (script check [F2]). Apostol II 8.15 (chain rule for differentiable fields) and 8.13 (continuous partials are sufficient); Marsden and Tromba 2.5. | `l4 summary.formula.note`: "Each partial is paired with its own rate, then the two products add. It needs a smooth $f$, one with continuous partial derivatives." `l4 screens[7].widget.lines[2].text`: "$\approx f_x\,\Delta x + f_y\,\Delta y$, each bracket moves one input only: a partial times its step, for a smooth $f$". `l7 screens[2].prose`, last sentence: "This is the **tangent plane** to the surface at (2, 1): a flat surface touching it there, with the same slopes in $x$ and in $y$. Every smooth surface has one."

3. `l11-on-a-constraint.json` | `screens[6].prose`, `summary.ideas[1]` | imprecise, serious | The rule reads: to find the largest or smallest $f$ on $g = c$, solve the conditions, "then compare $f$ at every solution". That works only when a largest and a smallest value exist. The lesson's own first example has neither property: $xy$ on $x + y = 10$ has one solution, $(5, 5)$, and no smallest value. A learner asked for the smallest $xy$ on that line would follow the rule and answer 25. No graded item falls into this, because each asks for the extreme that exists, but the method as stated is wrong on unbounded curves. | On the line $xy = 10x - x^2 \to -\infty$ (script check [F3]). The conditions are necessary, not sufficient: Marsden and Tromba 3.4 Theorem 8. Existence needs a closed bounded set: Apostol II 9.16 (extreme-value theorem). | `screens[6].prose`: "To find the largest or smallest $f$ on the curve $g(x, y) = c$, solve $$\nabla f = \lambda \nabla g, \qquad g(x, y) = c.$$ That is $f_x = \lambda g_x$, $f_y = \lambda g_y$ and $g = c$. Then compare $f$ at every solution. On a closed curve such as a circle, the largest and smallest values are both among them. On a line, one of them may not exist: $xy$ has no smallest value on $x + y = 10$." `summary.ideas[1]`: "There the gradients line up: $\nabla f = \lambda \nabla g$. Solve this with $g = c$, then compare $f$ at every solution. On a line, check that the largest or smallest value exists."

4. `l11-on-a-constraint.json` | `summary.formula`, `screens[6].prose` | imprecise, minor | The condition $\nabla g \neq \mathbf 0$ appears only in quiz item q11-condition. The rule and the summary omit it. Every constraint in levels 1 to 3 satisfies it, so no answer is affected. | Smallest $x$ on $y^2 = x^3$ is at the cusp $(0, 0)$, where $\nabla g = \mathbf 0$; the Lagrange system has no solution at all (script check [F4]). Marsden and Tromba 3.4 Theorem 8; Apostol II 9.14. | `summary.formula.note`: "Three equations in $x$, $y$ and $\lambda$. They assume $\nabla g \neq \mathbf{0}$ on the curve."

5. `l5-steepest-climb.json` | `screens[0].explain.text`, `screens[0].hints[2].text`, `screens[0].feedback.byKey.C` | imprecise, minor | "Per unit step, arrow A climbs about 5.7, B about 5.4, D 4 and C nothing." These are the slopes at P. The four arrows drawn have length 1.4, and over them the map shows something else: arrow C ends at $(1.01, 1.99)$ where $f = 8.94$, a climb of 2.94, well off the contour through P. A learner who counts contours on the map sees the text contradicted. | Gains per unit of length over the drawn arrows: A 7.76, B 7.05, D 6.80, C 2.10 (script check [F5]). The key is unaffected: A is largest either way. A straight step along the tangent gains $\tfrac12 \mathbf u^T \mathbf H \mathbf u\, L^2 = 1.5L^2$ (Apostol II 9.10). | `explain.text`: "At P the slope along arrow A is about 5.7, along B about 5.4, along D 4 and along C 0. A is the one at right angles to the contour through P. Slanting across the contours wastes part of every step." `hints[2].text`: "Arrow C starts out along the curve, so at P it gains nothing. Arrow A leaves the curve at a right angle." `feedback.byKey.C`: "You set off along the contour through P. In that direction the slope at P is 0."

6. `l5-steepest-climb.json` | `summary.trap` | imprecise, minor | "The gradient does not point at the peak" is stated as a rule. On round contours it does: lesson 1's own $x^2 + y^2$ has a radial gradient. | For $20 - x^2 - y^2$ at $(2, 1)$, $\nabla = (-4, -2)$, parallel to the direction of the peak (script check [F6]). | "The gradient need not point at the peak, and it never runs along a contour. It crosses the contour through your point at right angles."

7. `l5-steepest-climb.json` | `screens[9].explain.text` | imprecise, minor | "Variance rises fastest by adding asset 1." In a lesson whose point is that the fastest rise is along the gradient, this names an axis direction instead. The gradient is $(0.05, 0.02)$, a mix of both assets. | Slope along $(1, 0)$ is 0.05; along the gradient it is $\sqrt{0.05^2 + 0.02^2} = 0.0539$ (script check [F7]). The next sentence, on shifting weight from 1 to 2, is right: $-0.05 + 0.02 < 0$. | Replace the second sentence: "Per unit of weight, adding asset 1 raises variance more than adding asset 2: 0.05 against 0.02."

8. `l8-walking-downhill.json` | `screens[7].widget.options[2].why` (option "Only $s = \tfrac16$") | wrong, minor | "Other steps settle too, just more slowly." False: on $3x^2 + y^2$ the step $s = \tfrac14$ settles faster than $\tfrac16$. At $\tfrac16$ the factors are 0 and $\tfrac23$; at $\tfrac14$ they are $-\tfrac12$ and $\tfrac12$. Homework 2 (h-best-step) teaches exactly this balance, so the course contradicts itself. | Distance from the bottom after 20 steps from $(4, 3)$: $9.0 \times 10^{-4}$ at $s = \tfrac16$, $4.8 \times 10^{-6}$ at $s = \tfrac14$ (script check [F8]). Boyd and Vandenberghe 9.3: the rate is set by the worst factor. | "At $\tfrac16$ the $x$ factor is 0, a perfect $x$ step. Other steps settle too, and $s = \tfrac14$ settles faster overall."

9. `l9-peaks-pits-saddles.json` | `quiz[2]` (q9-cross): key, `explain`, `options[1].why`, `options[2].why`; `summary.ideas[1]`; `screens[4].explain.text` | imprecise, minor | "Two level curves cross at a stationary point, so it is a saddle" holds at non-degenerate points only. The same lesson already shows a degenerate case (the flat valley), so the exception is in reach. | $f = x^2 y^2$: the level set $f = 0$ is the two axes, which cross at the origin, and the origin is a lowest point (script check [F9]). Apostol II 9.9 to 9.11: the classification by crossing level curves comes from a non-degenerate quadratic part. | `quiz[2].prose`: "On a contour map, two level curves cross at a stationary point P. The ground is higher than P between one pair of arms and lower between the other." `summary.ideas[1]`: "Contours close into rings round a peak or a pit, and usually cross at a saddle."

10. `l12-min-variance.json` | `screens[6].widget.options[2].why` | imprecise, minor | "Zero risk needs $\rho = -1$." The screen before it says that with $\rho = 1$ and a short sale, $w_1 = -1$ "would hedge the risk away entirely". Screen 6 does not ban short sales. (Quiz q12-never says the same, but there no short sales is stated, so it is right.) | $\rho = 1$, $w_1 = -1$, $w_2 = 2$: $\sigma_p = |-0.2 + 0.2| = 0$ (script check [F10]). | "Zero risk needs $\rho = -1$, or $\rho = 1$ with a short sale. Uncorrelated assets cannot cancel exactly."

11. `l8-walking-downhill.json` | `screens[8].feedback.byKey.test-2` and `test-1` | wrong, minor | The test-2 line says "Update $a$ and $b$ together: if $a$ changes first, $b$ sees new residuals." That mistake changes the answer after one step, so it fails test 1 first. The learner then reads the test-1 line, which tells them to check $2/m$ and the sign, both of which they have right. | Under the page's Pyodide 0.27.7 (sweep below): three natural codings of the sequential update fail tests 1 and 2, first failure test 1. The coding that passes test 1 and fails test 2 first is "residuals computed once, outside the loop". | `test-1`: "Test 1 is one step from (0, 0), expecting (0.0733, 0.252). Check the factor $2/m$, the sign, and that $b$ uses the same residuals as $a$." `test-2`: "Test 2 is three steps. Rebuild the residuals inside the loop, from the current $a$ and $b$, on every pass."

12. `l8-walking-downhill.json` | `screens[8].feedback.byKey.test-4` | wrong, minor | "If the numbers blow up, check the sign of each step." A wrong sign fails test 1 first, so this line is never shown for it. | Sweep: uphill and flipped-residual codings fail test 1 first. The natural coding that fails test 4 first is stopping early on a tolerance (fails 4, 5, 6 only). | "Test 4 runs 3,000 steps and expects the least-squares line. Take all `n` steps: do not stop early or round the result."

13. `l8-walking-downhill.json` | `screens[3].feedback.byKey.error`; `homework-2.json` | `items[4].feedback.byKey.error` | misleading, minor | Both lines explain an unpacking mistake ("`grad(x, y)` returns two numbers: unpack them"). An unpacking mistake raises inside the first test, and the engine reports that as `test-1`, so the learner sees the test-1 line instead. Key `error` is given only when the code fails to load, for example on a `SyntaxError`, where unpacking is not the problem. (`screens[8]`'s error line, about `pass` and indentation, is right: comments with no body give an `IndentationError` and key `error`.) | Pyodide runs: `g = grad(x, y); x - step * g` gives key `test-1`; a missing colon gives key `error`. | `l8 screens[3]` error line: "Your code did not run. Check the colons and the indentation of the loop." `l8 screens[3]` test-1 line: "Test 1 expects (3.2, 1.8) after one step. Subtract `step * gx`, not add it, and unpack with `gx, gy = grad(x, y)`." `homework-2 items[4]` error line: "Your code did not run. Replace `pass` and check the indentation." Engine note in the inbox.

14. `l2-slicing.json` | `screens[1].feedback.correct` | imprecise, minor | "The slope at $x = 1$ is $2y_0$: double the slice height." The height of the slice at $x = 1$ is $f(1, y_0) = 4y_0$. The slope is double $y_0$. | $f(1, y_0) = y_0 + 3y_0 = 4y_0$; $f_x(1, y_0) = 2y_0$. | "The slope at $x = 1$ is $2y_0$: double the value $y$ is held at."

15. `l8-walking-downhill.json` | `quiz[2].widget.options[3].why` | imprecise, minor | "The start does not matter: a factor of size above 1 grows from anywhere." From a start on the $x$-axis $y$ stays 0 and the run settles. | $y_k = y_0(-1.4)^k = 0$ when $y_0 = 0$. | "The start hardly matters: a factor of size above 1 grows from any start with $y \neq 0$."

## Checked and found correct (the watch list)

- Partials against differentiability: see findings 1 and 2. Lesson 3 does state "for smooth functions" for Clairaut's theorem, and the script confirms the hypothesis is needed.
- Gradient direction and magnitude: `l5`, `l6`, `review-2`, `problems-2` all correct. The perpendicularity derivation in `l5 screens[8]` handles the vertical case.
- Directional derivative needs a unit vector: stated on first use (`l6 screens[1]`), drilled in `l6 screens[5]`, in the summary formula note and in every later item. The P&L item `l6 screens[8]` correctly does not normalise, and says why.
- Chain rule: every numeric item agrees with direct substitution (script).
- Second-derivative test: the statement in `l10 screens[6]` is the standard one. $D = 0$ is given as "no verdict" with examples of both outcomes. All 18 classified points agree with the Hessian eigenvalues (script). The test uses $D$ and $f_{xx}$; the trace is not used, which is fine in two variables.
- Lagrange multipliers: the sign convention $\nabla f = \lambda \nabla g$ with $g = c$ is used throughout, and under it $\lambda = dM/dc$ in every item (script, four problems). "Shadow price" is used correctly. Maximum against minimum is handled by comparing values in every circle item. See findings 3 and 4 for the missing conditions.
- Local against global: `l9 screens[8]` proves a global minimum by completing the square; `problems-3` part 5 says its pit is not the lowest value overall; `homework-3` h3-quartic argues the global minimum from growth at infinity. Correct.
- Portfolio: covariance terms, $\nabla V = 2\boldsymbol\Sigma\mathbf w$, the minimum variance weight, $\lambda = 2\sigma_p^2$, the long-only clip and the $\rho \ge \sigma_B/\sigma_A$ corner all check, including by Monte Carlo (400,000 draws). No item annualises or mixes horizons; volatilities are given as plain percentages throughout, so no convention is at risk. Units (£m sizes, £k profit, vol points against decimals) are consistent in every item.

## Code widget sweep

Run under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs` (scratch `sweep.mjs`, 46 submissions). First failing test for each natural coding:

| Widget | Line | Codings tried, first failing test | Line correct? |
|---|---|---|---|
| `l8 screens[3]` descend | test-1 (sign) | add both: 1; add $x$ only: 1 | yes |
| | test-2 (recompute) | gradient once before the loop: 2; gradient at the start point: 2; one jump of $n \times$ step: 2 | yes |
| | test-4 (0 steps) | `range(max(n, 1))`: 4; do-while: 4 | yes |
| | error (unpack) | no unpack: test-1, not error | no, finding 13 |
| `l8 screens[8]` fit_line | test-1 ($2/m$, sign) | $1/m$: 1; no $1/m$: 1; uphill: 1; residual sign flipped: 1 | yes |
| | test-2 (update together) | $a$ first with rebuilt list: 1; $a$ first inline: 1; $b$ first: 1 | no, finding 11 |
| | test-4 (blow up, sign) | uphill: 1; early stop on tolerance: 4 | no, finding 12 |
| | error (`pass`, indent) | comments only: error; body not indented: error | yes |
| `homework-2` steps_needed | test-1 (check first, count from 0) | returns $k + 1$: 1; squared length: 1 | yes |
| | test-4 (start at minimum) | step then check: 4 | yes |
| | test-5 (cap) | returns `None`: 5; returns $-1$: 5; uncapped `while`: 5 | yes; the uncapped loop fails by the time limit, so that case is timing-dependent |
| | error (unpack) | no unpack: test-1 | no, finding 13 |

Hidden tests reject the obvious wrong programs: closed-form least squares in `fit_line` fails tests 1 to 3; coordinate-wise descent fails `descend` test 6; component-wise and sum-of-sizes stopping rules fail `steps_needed` test 7. Programs that pass every test and differ from the solution (`<= tol`, testing the stale gradient after stepping, `range(max_steps + 1)`) return the same values as the solution on all inputs away from an exact tie, so none is a finding. Both starters fail.

## Run results

- Validator: `node tools/validate.mjs`: 0 errors.
- Number scripts: `node tools/run-number-scripts.mjs --only multivar`: 2 of 436 scripts, 2 passed, 0 new failures.
- `node tools/grade-all.mjs --file <each of the 24 files>`: 0 failures each. `--code` on `l8-walking-downhill.json` and `homework-2.json`: 0 failures.
- `docs/reports/multivar-L1-3-concepts.py` (venv Python, sympy and numpy newer than CI's pins; no figure depends on the version): 95 checks, 85 pass, 10 fail, exit 1. The 10 failures are findings 1 to 10, tagged [F1] to [F10] in the output. It exits 0 once those are fixed in content and the matching checks are retired or inverted.
- No playthrough, per the common rules.

## Overlap with earlier reads

Read after the ledger and findings were written: `docs/reviews/review-1.3.md` (multivar section and its fix pass), `docs/reviews/review-problems-1.3-b.md` and `docs/reviews/review-delta-problems-1.3-ab.md` (multivar problems 1 to 3), `docs/reports/problems-multivar.md`, `docs/reports/fluency-multivar.md`. No earlier `audit-multivar*` or `gap-multivar*` file exists at this commit.

Conceptual findings of the earlier reads in this scope (style, sentence length, typography and freshness left out):

| Earlier finding | Kind | Status at ee5d8292 | Found by me? |
|---|---|---|---|
| `review-1.json` r1-pnl-zero: feedback said both prices move together on a diagonal where they move oppositely | false claim | fixed; I read the corrected line and marked it correct | no (already fixed) |
| `l4-chain-two-inputs.json` S9: "ignoring time decay" unstated | unstated hypothesis | fixed; the phrase is present | no (already fixed) |
| `l8-walking-downhill.json` S6: "grows by 1.2" for a factor | wording | fixed | no (already fixed) |
| `problems-3.json` p-min-variance-pair part 4: "treat the weights 0.25 and 0.75 as free" | wording | fixed | no (already fixed) |

| | Count |
|---|---|
| Conceptual findings found by this audit only | 15 |
| Found by the earlier reads only | 4 (all fixed before this commit) |
| Found by both | 0 |

New `wrong` verdicts not in any earlier read: 3 (findings 8, 11, 12). Both serious findings (1 and 3) are new. The earlier reads checked numbers, slips and grading, and found none of the missing hypotheses: the miss rate of a single arithmetic-led read on conditions of theorems was complete here.

## Inbox

Three bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (audit multivar):": the `error` key reaches only load errors; `mutants` per named mistake for `test-N` lines; a standing-convention field and the advisory universal-claim pass.

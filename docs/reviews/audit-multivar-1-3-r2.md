# Blind concept audit, round 2: multivar levels 1 to 3 (`multivar-1-3-r2`)

Commit read: `beaf4205`. Stage 1, full ledger. Files: lessons `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l1`, `fluency-l2`, `fluency-l3` (24 files).

Read blind. The ledger, the findings and the concepts script were written before any earlier read on this course was opened. The earlier reads were opened only for the overlap table.

Sources: Apostol, *Calculus* vol. II (2nd ed.), chapters 8 and 9; Marsden and Tromba, *Vector Calculus*, chapters 2 and 3; Boyd and Vandenberghe, *Convex Optimization*, 4.4.1, 5.6.3, 9.3; Hull, *Options, Futures and Other Derivatives*, ch. 19.

## Verdict

Ledger: 3,563 rows in `docs/reports/audit-multivar-1-3-r2-ledger.md`. Correct 3,548, imprecise 13, wrong 2, misleading 0, unverified 0. The 15 rows that are not correct belong to 7 findings.

Findings: 1 wrong (minor), 6 imprecise (1 serious, 5 minor), 0 misleading. Serious 1, minor 6.

New `wrong` that no earlier read found: 1 (finding 2, a slip value). That is within the convergence rule's limit of one per three levels.

Every graded key is right. Every choice item has exactly one true option under its stated premises, with one reservation (finding 4). The three round 1 repairs named in the brief hold, with one reservation: the new definition of "smooth" in `l3` is too weak for the theorem it is attached to (finding 1).

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l3-second-partials.json` | `screens[7].explain.text`; same defect in `summary.ideas[2]` and the "Every time" of `screens[7].prose` | imprecise, serious | The explanation defines smooth functions as "those whose partial derivatives are continuous" and says Clairaut's theorem holds for them. Read plainly, that is continuity of $f_x$ and $f_y$. Lessons 4 and 6 use the same words for exactly that (the chain rule and $D_{\mathbf u} f = \nabla f \cdot \mathbf u$, where first partials are what is needed). Continuous first partials do not give $f_{xy} = f_{yx}$. The theorem needs the mixed second partials to be continuous. | $f = xy(x^2 - y^2)/(x^2 + y^2)$, $f(0, 0) = 0$, has continuous first partials everywhere, yet $f_{xy}(0, 0) = -1$ and $f_{yx}(0, 0) = +1$. The concepts script confirms both (two `support` checks). Apostol II 8.23, Theorem 8.12; Marsden and Tromba 3.1, Theorem 1 (stated for $C^2$). | Replace the last sentence of `screens[7].explain.text` with: "For smooth functions in general, those whose first and second partial derivatives are continuous, this is **Clairaut's theorem**." Replace the first sentence of `summary.ideas[2]` with: "For functions with continuous second partials, $f_{xy} = f_{yx}$." The lesson 4 and lesson 6 wording can stay: continuous first partials are enough there.

2. `homework-2.json` | `items[6].widget.wrong[0]` (`signs`, value 810) and `items[6].feedback.byKey.signs` | wrong, minor | The feedback names the mistake: "A short position gains when its price falls: $(-300)(-0.5) = +150$." A learner who makes it books B's term as $-150$ and enters $960 - 150 + 300 = 1110$. The slip is stored as 810, which that mistake does not give. 810 needs the C term to be lost as well ($960 - 150$). So the line never fires for the mistake it names, and the common wrong answer 1110 gets the generic line. | $800 \times 1.2 = 960$, $150 \times 2 = 300$; $960 - 150 + 300 = 1110$. Failing check in the concepts script. | Set `wrong[0].value` to `1110`. Keep the feedback line as it is.

3. `l7-tangent-planes.json` | `summary.ideas[2]`; same defect in `objectives[1]` and `quiz[1].widget.options[3].why` | imprecise, minor | "The error shrinks with the square of the step" is given as a property of every tangent plane. Screen 3 says a smooth $f$ has a tangent plane at every point, and smooth there means continuous first partials. For such an $f$ the error is only small compared with the step. The square law needs continuous second partials. Every function in the lesson has them, so no key is affected. | $|x|^{1.5}$ has a continuous derivative; its tangent error at 0 is $h^{1.5}$, so halving the step divides it by 2.83, not 4 (script `support` check). Marsden and Tromba 3.2, Theorem 2; Apostol II 9.10. | `summary.ideas[2]`: "When the second partials are continuous, the error shrinks with the square of the step: ten times closer, a hundred times smaller."

4. `review-3.json` | `items[8]`: `question`, key `options[0]`, `feedback.correct`, `explain.text` | imprecise, minor | "For which $k$ is the origin a pit?" has the key $-2 < k < 2$. At $k = \pm 2$, $f = (x \pm y)^2 \ge 0 = f(0, 0)$, so the origin is still a lowest point. Lesson 10 screen 7 says of exactly this function that "each point is a pit" is true. Under the lesson's own usage the full answer is $-2 \le k \le 2$, which no option offers. The key is the best of the four, and it is right for a strict pit. | $x^2 + 2xy + y^2 = (x + y)^2 \ge 0$. Monte Carlo sample of the disc round the origin in the concepts script (printed as a note). Apostol II 9.9 separates relative minima from strict ones. | `question`: "For which $k$ does the second derivative test show the origin is a pit?" Last sentence of `explain.text`: "At $|k| = 2$ the test is silent: $f = (x \pm y)^2$ is a valley, lowest along a whole line."

5. `l10-second-derivative-test.json` | `screens[6].prose`; same defect in `summary.ideas[1]` | imprecise, minor | The test is stated for any stationary point, with no condition on $f$. It needs the second partials to be continuous near the point. The derivation on screen 8 uses the second-order Taylor formula, which needs the same. All functions used are polynomials, so no key is affected, but this is the theorem a learner will quote. | Apostol II 9.11 to 9.12, Theorem 9.7; Marsden and Tromba 3.3, Theorem 6. | Start `screens[6].prose` with: "Let $f$ have continuous second partials. At a stationary point, let $D = \det \mathbf{H} = f_{xx} f_{yy} - f_{xy}^2$."

6. `l11-on-a-constraint.json` | `quiz[1].prose` | imprecise, minor | "P is the largest value of $f$ on the curve" and then "at P": P is used as a value and as a point. | Wording only; the key and the three `why` lines are right once P is a point. Marsden and Tromba 3.4, Theorem 8. | "On the curve $g(x, y) = c$, $f$ is largest at the point P, and $\nabla g \neq \mathbf{0}$ at P."

7. `l3-second-partials.json` | `screens[1].feedback.correct` | imprecise, minor | "The slope goes 2, 4, 6 as $y_0$ goes 1, 2, 3." The slider stops at $y_0 = 2.5$, so the learner cannot see the slope 6. The arithmetic is right. | Slider `max` is 2.5 in the screen's controls; $f_x(1, y_0) = 2y_0$. | "The slope goes 2, 3, 4 as $y_0$ goes 1, 1.5, 2: up 2 per unit."

## Checked and found correct (the watch list)

- Partials against differentiability. Lessons 4, 6 and 7 now carry "smooth, with continuous partial derivatives" where the chain rule, $\nabla f \cdot \mathbf u$ and the tangent plane need it (Apostol II 8.13, 8.15). `l6` `quiz[3]` states "smooth" in its premise, so its key is forced. The one gap is in lesson 3 (finding 1).
- Gradient and directional derivative. Unit arrows are required every time a slope is asked for; `l6` screen 9 says why the P&L does not divide by the length. A Monte Carlo over 200,000 directions finds the largest slope along $\nabla f / |\nabla f|$ with value $|\nabla f|$.
- Chain rule. Every stated rate was recomputed by differentiating the substituted function.
- Hessian test. Twenty stationary points were checked three ways: gradient, $D$ with the sign of $f_{xx}$, and a Monte Carlo sample of $f$ on a small disc. All agree with the content. The inconclusive case is taught with both outcomes ($x^4 + y^4$, $x^4 - y^4$, $(x - y)^2$).
- Lagrange multipliers. The rule in `l11` screen 7 now conditions on existence and on $\nabla g \neq \mathbf 0$, and both are right as worded. Every constrained answer was found again by brute force along the curve. $xy$ on $x + y = 10$ has no smallest value (checked). The sign and size of $\lambda$ as a shadow price hold for maxima and minima alike: 300 random constrained quadratics, $\lambda$ equal to the slope of the best value in $c$.
- Local against global. `l9` screen 9 proves a global minimum by completing the square; `l10` says "nearby"; `problems-3` says the pit at $(1, 1)$ is local only; `homework-3` item 7 justifies its global minimum by growth at infinity. All right.
- Portfolio. The two-asset formula, the multiplier $\lambda = 2\sigma_p^2$, clipping to $[0, 1]$, "all in the calmer asset exactly when $\rho \ge \sigma_B / \sigma_A$", "never more of the riskier asset" and "never riskier than the calmer asset alone" were all confirmed on 100,000 random pairs. The option tables in `l2` and `l3` are Black-Scholes values at zero rate.

## Code widget sweep

All runs in Pyodide 0.27.7 from the local CDN through `app/tools/code-runner.mjs` (the page's grader), 51 submissions. The number is the first failing test.

| Widget | Line | Codings tried, first failing test | Line correct? |
|---|---|---|---|
| `l8 screens[3]` `descend` | test-1 (unpack, subtract) | adds the step: 1; adds, two statements: 1; no unpack: 1 | yes |
| | test-2 (recompute the gradient) | gradient once before the loop: 2; gradient at the start point each pass: 2; one jump of `n * step`: 2; one step, no loop: 2 | yes |
| | test-4 (0 steps) | do-while: 4; `range(max(n, 1))`: 4; `range(n + 1)`: 1 | yes (the last is a different mistake) |
| | error | missing colon: error | yes |
| `l8 screens[8]` `fit_line` | test-1 ($2/m$, sign, same residuals) | $1/m$: 1; no $1/m$: 1; adds: 1; residual sign flipped: 1; $a$ first then $b$: 1; $b$'s sum without $x_i$: 1 | yes |
| | test-2 (rebuild residuals each pass) | residuals once before the loop: 2; one jump: 2; residuals from $a = b = 0$ each pass: 2 | yes |
| | test-4 (take all `n` steps) | stop at 1e-6 on both partials: 4; at 1e-8 on the length: 4; at 1e-4: 4; at 1e-12: passes; cap of 1,000 steps: passes | yes (three of five; the two that pass return the right line) |
| | error | undefined name in the loop: test-1, since the engine reports a run-time error as the test it happens in; the line speaks of `pass` and indentation, which is the load-time case | yes |
| `homework-2 items[4]` `steps_needed` | test-1 (unpack, check first, count from 0) | returns $k + 1$: 1; `hypot(g)`: 1; check after the step, return $k$: 1; old gradient tested after the step: 1 | yes |
| | test-4 (start at the minimum) | step, then check, return $k + 1$: 4; `while` version of the same: 4; divide by the gradient length: 4 | yes |
| | test-5 (cap) | uncapped `while`: 5 (by the time limit, so timing-dependent); returns `None`: 5; returns $-1$: 5; returns the last $k$: 5 | yes |
| | error | missing colon: error | yes |

Wrong programs against the hidden tests: a hard-coded gradient fails test 5 of `descend`; closed-form least squares fails test 1 of `fit_line`; the L1 norm and the max norm in `steps_needed` fail test 7 only; the squared length and the distance to the origin fail test 1. Nothing wrong passed. Three harmless variants pass and should: a list in place of a tuple, `<=` in place of `<`, and one extra check after the last step. Solutions pass and starters fail in all three. The declared `mutants` (4, 11 and 4) each first fail their named test under `grade-all --code`.

## Run results

- Validator: 0 errors.
- `run-number-scripts.mjs --only multivar`: 2 of 2 passed.
- `grade-all.mjs --file` on all 24 files with `--code`: 338 widgets and 10 Fluency templates, 3 Python widgets, 0 failures.
- `docs/reports/multivar-L1-3-concepts-r2.py`: 107 checks, 1 failing, exit 1. The failing check is finding 2 and stays failing until the slip value is fixed. It prints one note, for finding 4. Run with NumPy 2 and SciPy from the session venv; no figure depends on the version.
- No playthrough, as the brief says.

## Overlap with earlier reads

Read after the findings were written: `docs/reviews/audit-multivar-1-3.md` (round 1, 15 findings, all marked fixed), `docs/reviews/review-1.3.md`, the three `review-problems-1.3-*` files and their delta, `docs/reports/multivar-5.md`, `problems-multivar.md`, `fluency-multivar.md`.

| | Count |
|---|---|
| Conceptual findings found by this audit only | 7 |
| Found by the earlier reads only | 19 (15 in round 1 and 4 before it; all fixed at this commit, and I marked each corrected line correct) |
| Found by both | 0 |

New `wrong` found by this audit only: 1 (finding 2). Finding 1 sits in text that the round 1 fix pass wrote (its fix for round 1 finding 1 added the definition of "smooth" to `l3`); it is `imprecise`, so it does not count as a `wrong` towards convergence. That round 1 fix pass has no fix-pass read recorded in its audit file.

## Inbox

One bullet added to `docs/BACKLOG-INBOX.md` under "Raised later (audit multivar):" (slip values against the arithmetic their feedback shows).

## Fix pass

Opus fixer, from commit `7703cf96`. Own checks in the scratch script `fix-mv13r2/own.py` (SymPy and NumPy), written before the auditor's script was rerun.

1. Fixed differently. Basis: for $xy(x^2 - y^2)/(x^2 + y^2)$ I get $f_x(0, y) = -y$ and $f_y(x, 0) = x$, so $f_{xy}(0, 0) = -1$ and $f_{yx}(0, 0) = 1$, while $f_x / r$ stays bounded in polar form, so $f_x$ is continuous at the origin; Apostol II 8.23 needs the mixed second partials continuous. Rather than redefine "smooth" (lessons 4, 6 and 7 gloss it as continuous first partials, which is all they need), the second-order condition is stated where it is used. `l3` `screens[7].explain`: "For any function whose second partial derivatives are continuous, the two orders agree too: this is **Clairaut's theorem**." `summary.ideas[2]`: "When the second partials are continuous, $f_{xy} = f_{yx}$." `screens[7].prose`: "In every example so far, $f_{xy} = f_{yx}$." The quadratic-error claim (finding 3) and the Hessian test (finding 5) now carry the same condition.
2. Fixed. Basis: $800(1.2) = 960$, $(-300)(-0.5) = 150$, $150(2) = 300$; booking B as $-150$ gives $960 - 150 + 300 = 1110$, and again as the key minus twice B's term, $1410 - 300 = 1110$. `wrong[0].value` is now 1110: 300 from the key 1410 and 150 from the `noB` slip 1260, both far outside the 0.5 bands.
3. Fixed. Basis: Taylor's formula with second-order remainder (Apostol II, ch. 9) gives error $\tfrac12 Q(h) + o(|h|^2)$ given continuous second partials, and not in general without them; $|x|^{1.5}$ is $C^1$ with tangent error $h^{1.5}$, ratio 2.83 on halving. `l7` `summary.ideas[2]`, `objectives[1]`, `quiz[1].prose` ("Take an $f$ with continuous second partials.") and `quiz[1]` option `eighth` `why` now state the condition. Key unchanged.
4. Fixed (question reworded; key unchanged). Basis: $D = 4 - k^2$ with $f_{xx} = 2$, so the test says pit exactly when $|k| < 2$, is silent at $|k| = 2$ and says saddle beyond; at $k = \pm 2$, $f = (x \pm y)^2 \ge 0$ is a non-strict lowest point, which `l10` screen 6 calls a pit. `question`: "For which $k$ does the second derivative test show the origin is a pit?" so the key $-2 < k < 2$ is exactly what the test gives. `explain.text` last sentence: "At $|k| = 2$ the test is silent, yet $f = (x \pm y)^2 \geq 0$ is still lowest at the origin, along a whole line." The concepts script's note for this item was re-pointed to the old question wording (said in its docstring); no check changed.
5. Fixed. Basis: the second-derivative test in Apostol II, ch. 9, assumes continuous second partials near the point, as does the second-order Taylor step on screen 7. `l10` `screens[6].prose` now starts "Let $f$ have continuous second partials."; `summary.ideas[1]` starts "If the second partials are continuous, then at a stationary point".
6. Fixed. Basis: Lagrange's condition is about a point; P must name one. `l11` `quiz[1].prose`: "On the curve $g(x, y) = c$, $f$ is largest at the point P, and $\nabla g \neq \mathbf{0}$ at P."
7. Fixed. Basis: slider `min` 0.5, `max` 2.5, `step` 0.5; slope at $x = 1$ is $2y_0$, so 2, 3, 4 at 1, 1.5, 2. `l3` `screens[1].feedback.correct`: "The slope goes 2, 3, 4 as $y_0$ goes 1, 1.5, 2: up 2 per unit."

Gates: validator 0 errors; voice scan 35 on the six edited files, 0 and 0; `multivar-L1-3-concepts-r2.py` 107 checks, 0 failing, no notes, exit 0; `multivar-L1-3-concepts.py` 95 of 95, exit 0; `run-number-scripts --only multivar` 2 of 2; `grade-all --file` 0 failures on each edited file; playthrough green desktop and `--mobile` for `l3`, `l7`, `l10`, `l11`, `review-3`, `homework-2`. Keys: none changed. Slips: `homework-2` `items[6]` `signs` 810 to 1110. Tests: none added.

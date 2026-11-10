# Concept audit: odes, levels 1 to 3 (round 3)

Blind third concept audit (brief: `docs/briefs/concept-audit.md`) of `app/content/courses/odes/` levels 1 to 3: l1 to l13, review-1 to review-3, homework-1 to homework-3, as they stand after the two earlier fix passes. Claim ledger: `docs/reports/audit-odes-1-3-r3-ledger.md` (184 rows: correct 178, imprecise 5, misleading 1, wrong 0, unverified 0). Checks: `docs/reports/odes-L1-concepts-r3.py`, `odes-L2-concepts-r3.py`, `odes-L3-concepts-r3.py`. The ledger, the scripts and the findings below were written and committed (da0fe403 and the commit after it) before any earlier review, audit, ledger, concepts script or author report for this course was opened.

Every screen, quiz item, hint, explain, why, feedback and wrong-option line was read, with chart and canvas expressions where a curve makes a claim. All 16 code tasks were run in CPython: every solution passes all of its hidden tests and every starter passes none. Console lines were also run in Pyodide 0.27.7 (NumPy 2.0.2) under node, since two claims are about that runtime.

Findings are `N. file | JSON path | severity | problem | evidence and basis | exact fix`. Severities: `wrong` (false as stated), `imprecise` (true under an unstated hypothesis), `misleading` (true, but teaches a wrong habit). Each is also tagged `serious` (a learner would carry away a wrong definition, theorem, method, convention or graded answer) or `minor`. There are 6 findings: 0 `wrong`, 5 `imprecise`, 1 `misleading`. All 6 are minor; the serious count is 0. No graded key is wrong, no accepted answer is wrong, and no theorem or method is stated falsely.

## Level 1

1. l2-separable.json | quiz[1].feedback.correct | misleading, minor | "$t + y$ is a sum, not a product, so it cannot be split." The conclusion is right. The reason given is not a test: being written as a sum does not stop a right side from separating. The course's own homework-1 items[6] separates $y' = 1 + y^2$, a sum, and $t + ty = t(1 + y)$ separates too. A learner who keeps the line as a rule will call both non-separable. | A right side $F(t, y)$ separates exactly when it equals some product $g(t)h(y)$ (Boyce and DiPrima 2.2; Tenenbaum and Pollard lesson 6). For $F \ne 0$ that is $F\,F_{ty} = F_tF_y$: for $t + y$ it reads $0 = 1$, so no such product exists; for $1 + y^2$ and $t + ty$ it holds. `odes-L1-concepts-r3.py` `t+y_not_separable` passes and `FINDING_1` is the EXPECTED_FAIL. | quiz[1].feedback.correct: "No product $g(t)h(y)$ equals $t + y$, so it cannot be split."

2. l2-separable.json | screens[9].prose (second sentence); screens[9].explain.text (first sentence) | imprecise, minor | "An analyst fits $1000e^{0.8t}$ to the first few months, where the two curves agree" and "Early on $P \approx P_0e^{kt}$ because $1 - P/K \approx 1$." With $P_0 = 1{,}000$ and $K = 10{,}000$ the factor $1 - P/K$ starts at 0.9, not near 1. The logistic starts growing at 0.72 a year, not 0.8, and after three months it is already 2.2% below the exponential. The approximation needs $P_0$ much smaller than $K$, which the screen does not say. The key (£11,023m) and the lesson drawn from it are unaffected. | Boyce and DiPrima 2.5: for $y \ll K$ the logistic is close to $y' = ry$. Here $0.8(1 - 0.1) = 0.72$; $P(0.25) = 1{,}194.9$ against $1000e^{0.2} = 1{,}221.4$. `odes-L1-concepts-r3.py` `FINDING_2` (EXPECTED_FAIL) and `quarter_year_gap_is_2pc`. | screens[9].prose, second sentence: "An analyst fits $1000e^{0.8t}$ to the first few months, where the two curves are still close." screens[9].explain.text, first sentence: "Early on $1 - P/K$ is close to 1, here 0.9, so $P$ grows almost as $P_0e^{kt}$."

## Level 2

3. l6-second-order.json | screens[4].explain.text (second sentence) | imprecise, minor | "Superposition is why two independent solutions are enough." Superposition says that every sum $c_1y_1 + c_2y_2$ is a solution. It does not say that every solution is such a sum. That second half needs the existence and uniqueness theorem and a non-zero Wronskian, which the lesson gives on screen 8. As written, the learner is handed half the argument as the whole. | Boyce and DiPrima 3.2: Theorem 3.2.2 (superposition) against Theorems 3.2.1 and 3.2.4 (a fundamental set gives every solution because the initial value problem has one solution and $W \ne 0$). | screens[4].explain.text, second sentence, replaced by two: "Superposition makes every such sum a solution. Screen 8 says when two solutions give all of them."

4. l7-characteristic-equation.json | screens[9].prose (first sentence) | imprecise, minor | "A perpetual American put has no expiry, so its value $V(S)$ obeys $\tfrac12\sigma^2S^2V'' + rSV' - rV = 0$." The equation holds only while the option is held, for $S$ above the exercise level $S^*$. At and below $S^*$ the value is $K - S$, which gives $-rK$ on the left, not 0. The explain and quiz[2] do use the right region ("for $S \ge S^*$"), so only the prose drops the condition. | Hull, *Options, Futures, and Other Derivatives*, perpetual American options; Shreve, *Stochastic Calculus for Finance II*, 8.3. `odes-L2-concepts-r3.py` `put_power_solutions` and `put_smooth_pasting` pass; `FINDING_4` (EXPECTED_FAIL) shows $K - S$ fails the equation. | screens[9].prose, first sentence: "A perpetual American put has no expiry, so while it is held its value $V(S)$ obeys $\tfrac12\sigma^2S^2V'' + rSV' - rV = 0$."

## Level 3

5. l10-first-order-systems.json | screens[10].prose (first sentence) | imprecise, minor | "Two-factor short-rate models have one fast factor and one slow one." This is stated of every such model. It is true of most fitted ones, not of the class: the two mean-reversion speeds are free parameters and nothing forces them apart. The next sentence ("In ours ...") is fine. | Brigo and Mercurio, *Interest Rate Models*, ch. 4 (G2++, speeds $a$ and $b$ fitted freely); Hull, two-factor Hull-White. | screens[10].prose, first sentence: "Two-factor short-rate models are often fitted with one fast factor and one slow one."

6. l13-linearising.json | screens[7].widget.options[2].why | imprecise, minor | The question is "What does the linearisation tell us about the origin?" Option 3 is "A line of equilibria, as in lesson 11", and its why says "Only the origin is still: at $(1, 0)$, $x' = 1$." The linearised system is $x' = 0$, $y' = -y$, which is lesson 11's system exactly and does have a line of equilibria. The why answers about the true system without saying so, so a learner who read the linear picture correctly is told a thing that is false of it. The key is still the best answer. | $\mathbf{J}(0, 0) = \begin{pmatrix}0&0\\0&-1\end{pmatrix}$ has null vector $(1, 0)$ (l11 screens[7]); Strogatz 6.3 on non-hyperbolic points. `odes-L3-concepts-r3.py` `FINDING_6` (EXPECTED_FAIL). | screens[7].widget.options[2].why: "The linear system has that line, but the true system does not: at $(1, 0)$, $x' = 1$."

## Noted, not conceptual

Printed values met while running the code. They change no meaning and are not counted as findings.

- l4-slope-fields.json screens[8].canvas.params.lines[3] shows `array([-0.+1.j, -0.-1.j])`. Pyodide 0.27.7 and CPython both print `array([-0.+1.j,  0.-1.j])`.
- l2-separable.json screens[8].canvas.params.lines[3] shows `2.7465307216702745`. `np.log(9) / 0.8` prints `2.746530721670274` in Pyodide and CPython.
- l3-integrating-factor.json screens[8].canvas.params.lines[1] shows `15569.310496803077`. The solution's `linear_const(0.05, 1200, 0, 10)` returns `15569.310496803075`.
- NumPy 2 prints scalars as `np.float64(...)`. Five console lines show a bare number where Pyodide prints that wrapper: l2 screens[8] lines[3], l5 screens[8] lines[3], l7 screens[8] lines[3], l9 screens[9] lines[3] and l12 screens[8] lines[2]. This looks like a house simplification.
- l3-integrating-factor.json screens[0].canvas.state.points[0].y is 5303.4 at $x = 4$; the curve gives 5,313.67. The point is bound to the curve, so the engine should redraw it there.
- l10-first-order-systems.json screens[9] console `array([-2. , -0.5])` is right for Pyodide's NumPy 2.0.2. NumPy 2.5 returns a complex array; the solution's `np.real` covers both.

## Checked and clean

Every probe named in the brief came back clean after the two fix passes. In brief:

- Dropped hypotheses. Uniqueness carries its condition (l1 screens[9], summary; homework-1 items[3]). Lost constant solutions are taught and tested (l2 screens[7]). Intervals of validity are stated (l2 screens[5], homework-1 items[5] and items[6]). homework-2 items[6] states continuity of $p$, $q$, $g$.
- Integrating factor: $e^{\int p}$, both sides multiplied, the $a = 0$ case, and the two trap curves all check.
- Characteristic-equation cases, the modification rule (including $t^2$ at a double root) and the singular $2 \times 2$ system at resonance all check by sympy.
- Damping: $b = 0$ is named undamped and the code's convention is stated in its docstring. The settling table, the 2.8% and 44.43% overshoots, the envelope $1.0328e^{-0.5t}$, the damped peak at $2\sqrt{1 - 2\zeta^2}$ and "critical is fastest with no overshoot" all reproduce.
- Phase plane: the turning rule (sign of the bottom-left entry) holds for 5,000 random matrices with complex eigenvalues. The trace-determinant map agrees with the eigenvalues for 20,000 random matrices. The parabola and $\Delta = 0$ are handled as edges.
- Stability: a centre is called stable but not asymptotically stable (l12 screens[7]); semi-stable is called unstable in the strict sense (l4 quiz[0]); continuous and discrete tests are kept apart.
- Linearisation: trusted for a saddle, node or spiral, with the equal-eigenvalue caveat; silent for a centre and for a zero eigenvalue unless the other is positive. Each case has a worked check in `odes-L3-concepts-r3.py`.
- Wrong options and slips: every `wrong[]` value and every option `why` was recomputed. Only finding 6 has a why that is false of what the option says.
- Financial readings: half-lives halve the gap, the Vasicek mean follows the ODE (Monte Carlo, 200,000 paths), the perpetuity's $c/r$ is an unstable level, and the perpetual put's numbers reproduce.
- Lesson against review and homework: every reused matrix, equation and number agrees with its lesson.

## Overlap with the earlier reads

Filled after the ledger, scripts and findings above were committed (da0fe403 `Concept audit: odes L1 to L3 round 3, ledger and concepts scripts` and dace047a `Concept audit: odes L1 to L3 round 3, findings (blind, before overlap)`). Only then were `docs/reviews/review-odes-1-3.md`, `docs/reviews/audit-odes-1-3.md` and `docs/reviews/audit-odes-1-3-r2.md` opened, with their `## Fix pass` sections. The earlier ledgers and the author reports were not opened. The earlier concepts scripts were run for their exit codes only.

The earlier reads hold 32 conceptual findings: 9 in the second-reader review (as counted by the round-1 audit), 14 in the round-1 audit and 9 in the round-2 audit. All 32 were applied before this round read the content, so none could be found again.

| | count | which |
|---|---|---|
| Conceptual findings found by this round only | 6 | findings 1 to 6 above (0 wrong, 5 imprecise, 1 misleading; 0 serious) |
| Conceptual findings found by earlier reads only | 32 | review-odes-1-3: 9; audit-odes-1-3: 14 (2 wrong, 4 serious); audit-odes-1-3-r2: 9 (2 wrong, 0 serious). All fixed in the text read here |
| Found by both | 0 | none |

Where each finding of this round sits (`git log -S` on the quoted words names one commit each, the author's level commit):

| finding | in fix-pass text? | note |
|---|---|---|
| 1 (l2 "a sum, not a product") | no | original text, commit 4ce4b470; no fix pass touched l2 |
| 2 (l2 "where the two curves agree") | no | original text, commit 4ce4b470 |
| 3 (l6 "Superposition is why ...") | no | original text, commit 47136824; no fix pass touched l6 |
| 4 (l7 put equation with no region) | no | original text, commit 47136824; the fix passes changed l7 screens[4] and screens[5] only |
| 5 (l10 "Two-factor short-rate models have ...") | no | original text, commit a1b867b9 |
| 6 (l13 screens[7] option why) | no | original text, commit a1b867b9; the fix passes changed other screens of l13 |

None of the six sits in text a fix pass wrote, against three of nine in round 2.

The 32 corrected lines were each read here as they now stand, and they hold. Among them, each with its own check in this round's scripts or runs: the uniqueness hypothesis (l1 screens[9], homework-1 items[3]); the linear-drift reason for the Vasicek mean; the envelopes $\tfrac{\sqrt5}{2}e^{-t}$ and $1.0328e^{-0.5t}$; the term-by-term modification rule with $t^2$ at a double root; the smoother feedback equation with its 100; the float example $0.2^2 - 4(0.5)(0.02)$, which does print `6.938893903907228e-18` in Pyodide; undamped named apart from under-damped; "its first swing"; the semi-stable point called unstable in the strict sense; asymptotic against Lyapunov stability in l12; the $\Delta > 0$ condition in l12 screens[2]; the parabola caveat; the cubic centre that spirals in; the equal-eigenvalue caveat; and "nor does a zero eigenvalue, unless the other eigenvalue is positive". No fix of either pass introduced a new error that this round could find.

Four of the notes under "Noted, not conceptual" repeat notes of round 2 that are still in the content (the l3 canvas point, the l4 console line, the bare floats and their last digits). They were notes there too, and the round-2 fix pass left them alone.

Counts for the convergence rule. New `wrong` findings that no earlier read found: 0. The rule closes a course at "at most one new `wrong` per three levels", so on this count the course closes at round 3. The trend across rounds is 2 `wrong` and 4 serious, then 2 `wrong` and 0 serious, then 0 `wrong` and 0 serious. The six findings left are wording and precision; the fixes above are one sentence each.

## Gate results

Run in this worktree on the content as read. No content file, engine file or `course.json` was changed.

- `node tools/validate.mjs 2>&1 | tail -5` (from `app/`): `0 errors, 4116 warnings`. `content/manifest.json` unchanged (`git status` shows only this round's files).
- `python3 docs/reports/odes-L1-concepts-r3.py`: exit 0 (43 passed, 2 EXPECTED_FAIL: findings 1 and 2). `odes-L2-concepts-r3.py`: exit 0 (40 passed, 1 EXPECTED_FAIL: finding 4). `odes-L3-concepts-r3.py`: exit 0 (39 passed, 1 EXPECTED_FAIL: finding 6). Findings 3 and 5 are a gap in an argument and a claim about practice; neither has a check that could fail, and the true statements beside them are checked. Each EXPECTED_FAIL has its corrected assert in the comment below it.
- `python3 docs/reports/odes-L1-numbers.py`: exit 0. `odes-L2-numbers.py`: exit 0. `odes-L3-numbers.py`: exit 0.
- Earlier concepts scripts, run only after the overlap table was filled: `odes-L{1,2,3}-concepts.py` exit 0, 0, 0; `odes-L{1,2,3}-concepts-r2.py` exit 0, 0, 0.
- Code tasks (scratch harness, not committed): 16 tasks, every solution passes all hidden tests in CPython 3.13 with NumPy 2.5.3, every starter passes none.
- Pyodide runs (scratch script, not committed; Pyodide 0.27.7, NumPy 2.0.2, under node with the local package folder): a singular `np.linalg.solve` returns `array([nan, nan])`; `np.linalg.eig([[-2, 2], [0, -0.5]])` gives `array([-2. , -0.5])`; `0.2**2 - 4*0.5*0.02` is `6.938893903907228e-18`; `np.roots([1, 0, 1])` is `array([-0.+1.j,  0.-1.j])`.
- Playthrough: not run. This round changed no content, so there are no changed files to play through.

Proposed fixes obey the voice rules: British English, no exclamation marks, no em-dashes, every sentence under 35 words, explanations of at most three sentences (finding 2's explain stays at three, finding 3's goes from two to three).

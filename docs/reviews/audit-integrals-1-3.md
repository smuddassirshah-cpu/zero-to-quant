# Blind concept audit: integrals levels 1 to 3 (round 1)

Commit 43e99544, branch `worktree-agent-a472cf3ef3e935a9c`. Scope: `app/content/courses/integrals/` lessons l1 to l13, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, and the fluency sets for l6, l7, l9 and l10 (26 files). Stage 1, full ledger. Level 4 (l14 to l17 and its sets) was not read.

Ledger: `docs/reports/audit-integrals-1-3-ledger.md`, 3,934 rows. Blind verdicts: 3,918 correct, 12 imprecise, 3 wrong, 1 misleading, 0 unverified (13 findings; some cover two rows). Two more rows turned `imprecise` in the addendum at the end.
Script: `docs/reports/integrals-L1-3-concepts.py`, 359 checks, 4 failing (findings 1, 2, 7 and 9 below), exit 1. Run with the scratchpad venv (NumPy 2, SciPy and SymPy newer than CI's pins; no figure depends on the version).

## What was checked

- Every key, every slip value against the mistake its feedback names, and every figure printed in prose, hints, feedback, explanations, captions, models and rubrics, recomputed with SymPy (closed forms, limits, antiderivatives by differentiation) and `scipy.integrate.quad` (definite values, areas as $\int |f|$).
- Riemann sums: left, right and midpoint values; the closed forms $R_n$ and $L_n$ for $x^2$, $x^3$, $x$, $12 - 3x^2$ and $9 - x^2$ on their intervals (symbolic in $n$); the gap $|f(b) - f(a)|\tfrac{b - a}{n}$; which sum overestimates on a rising and on a falling curve. The limit statement is given for continuous $f$ (Spivak ch. 13, Thm 3), which is the right hypothesis.
- Signed integral against area: every item that asks for one was checked for the other as a slip; reversed, equal and split limits.
- Fundamental theorem: the first form is stated for continuous $f$ in l5 (prose, summary, quiz, homework-2 models). The second form drops the hypothesis (finding 3). The $1/x^2$ counterexample on $[-1, 1]$ is right, and so is the constant argument ($F - A$ has zero derivative on an interval).
- Antiderivatives: every formula differentiated back; $\ln|x|$ on each side of 0; the constant fixed by a starting value.
- Substitution: limits moved to $u$ in every definite item, and the kept-limits slip reproduced each time. Parts: sign of $\int v\,du$ in every item and every fluency family (symbolic for all parameter values); the looped $e^x \sin x$ derivation; the homework-3 derivation with its hypotheses.
- Improper integrals: defined as the limit of $\int_a^b$; the p-test with $p = 1$ and $p < 1$ diverging; $\int_1^\infty \ln x / x$ diverges; the perpetuity $1/r$, growing perpetuity $1/(r - g)$, $1/r^2$ and the duration $1/r$; the limit $b\,e^{-rb} \to 0$ is justified by a bound in both models.
- Trapezium rule: $T_n$ values, the exact error $1/(6n^2)$ for $x^2$, the empirical order 2 for smooth integrands (run), over and under-estimates against convexity. Simpson's rule is not taught in these levels. In problems-3, the predicted errors from one $h^2$ extrapolation were compared with the true ones: 0.00173 against a predicted 0.0017 for $\ln x$ at $n = 8$, and true errors 0.1185, 0.0294, 0.0073 for the signal at $n = 4, 8, 16$, so the keyed $n = 16$ is also the true answer.
- Densities and expectations: every density integrates to 1 ($\tfrac{1}{20}$ on [90, 110], the triangle, $x/2$, $3x^2$, $e^{-t}$, $x e^{-x}$, $2x/(1 + x^2)^2$); means, tails, the median and the 1% size; $E[g(X)]$ against $g(E[X])$ with the direction of Jensen's inequality for $e^{-x}$ and $\ln x$. All confirmed by Monte Carlo (2,000,000 seeded draws; tolerances at least four standard errors and far below the gap to each named slip).
- Units and conventions: shares per minute times minutes, £k per hour, pound-hours for TWAP; actual/365 is stated where it is used; the continuous rate is stated from l7 on but not at its first use in l2 (finding 8).
- Tools: validator 0 errors; `run-number-scripts.mjs --only integrals` 5 of 5 passed; `grade-all.mjs --file` 0 failures on each of the 26 files. No playthrough.

## Code sweep (rule 6)

Three Python widgets: l12 `screens[3]` (`trapezium`), l12 `screens[8]` (`phi`, `prob_within`), homework-3 `items[4]` (`trapezium`, `n_needed`). No C++. Each line was tested by submitting natural codings of its mistake through `app/tools/code-runner.mjs` (the page's grader in Pyodide 0.27.7 from the local CDN; scripts `docs/reports/integrals-L1-3-test-line-sweep.mjs` and `-sweep-2.mjs`, run as `node <script> $PWD <pkgs>` from `app/`). None is timing-dependent.

| widget | line | codings submitted | first failing key | verdict |
|---|---|---|---|---|
| l12 s3 | test-1 | `range(n + 1)`, `range(n - 1)`, `range(1, n)`, left sum, midpoint, Jo's `range(n)` points | test-1 (all six) | correct |
| l12 s3 | test-3 | early return for `n < 2`; ends added inside a `range(1, n)` loop | test-3 (both) | correct |
| l12 s3 | test-6 | `left = i * h`; `abs(a) + i * h`; `h = b / n` | test-6, test-6, test-5 | correct (the third gets the generic line) |
| l12 s3 | error | bad indent | error | correct |
| l12 s8 | test-1 | no square root; $\sqrt{\pi}$; $\sqrt2\,\pi$ | test-1 (all three) | correct |
| l12 s8 | test-4 | 0 to `z`; $-10$ to `z`; twice 0 to `z` | test-4 (all three) | correct |
| l12 s8 | error | `trapezium(phi(), ...)`; `trapezium(phi(x), ...)`; unclosed bracket | test-4, test-4, error | finding 10 |
| hw3 i4 | test-1 | `range(n + 1)`; left sum | test-1 (both) | correct |
| hw3 i4 | test-3 | return the previous `n`; stop at $4\,\text{tol}$; `n += 1` | test-3 (all three) | correct |
| hw3 i4 | test-4 | start at `n = 2`; double before testing | test-4 (both) | correct |
| hw3 i4 | error | generic line, true as stated | | correct |

Obvious wrong programs: left, right-open and midpoint sums fail test 1 in both `trapezium` widgets; a signed error without `abs` fails test 6 of homework-3; $e^{-x^2}$ without the half fails test 2 of l12 s8. One wrong program passes every test of homework-3 (finding 9). Starters fail and solutions pass in all three.

## Findings

1. `l3-signed-area.json` | `screens[7].explain.text` | wrong, serious | "A negative result says $f$ spends more of $[2, 5]$ below the axis than above it." The sign of an integral compares areas, not lengths of interval. | Take $f = -10$ on $[2, 2.5)$ and $f = 1$ on $[2.5, 5]$: the integral is $-2.5$, yet $f$ is above the axis for five sixths of the interval (script, FINDING 1). The lesson's own screen 1 says "signed area measures the balance, not the size". Stewart 5.2: the integral is the net area $A_1 - A_2$. | Replace the last sentence with: "A negative result says the area below the axis on $[2, 5]$ outweighs the area above it."

2. `l8-between-curves.json` | `screens[8].prose` | wrong, minor | "So the area between the rate curves is the gap between the equity curves." By this lesson's definition (screen 6, $\int |f - g|$) the area is 74; the gap is the signed integral, $-24$, which is the keyed answer. | Script FINDING 2: $\int_0^{12} |10 - 2t|\,dt = 74$, $\int_0^{12} (10 - 2t)\,dt = -24$. The explanation on the same screen says the opposite of the prose ("the enclosed area, 74, would count losses as gains"), so the screen contradicts itself. Minor because the explanation corrects it. | Replace the sentence with: "So the integral of $f - b$ is the gap between the equity curves."

3. `l7-evaluating.json` | `screens[2].prose`, and `summary.formula.tex` | imprecise, minor | The second form is stated as "If $F' = f$ on $[a, b]$, then $\int_a^b f = F(b) - F(a)$" with no hypothesis on $f$. | Stewart 5.3 requires $f$ continuous; Spivak ch. 14 Thm 2 requires $f$ integrable. A derivative need not be integrable (Volterra's function; Spivak ch. 14, problems). The proof on screen 8 uses $A' = f$, which l5 proved for continuous $f$ only, so the proof given does not cover the statement given. | Prose: "This is the fundamental theorem, second form. If $f$ is continuous on $[a, b]$ and $F' = f$ there, then $$\int_a^b f(x)\,dx = F(b) - F(a) = \Big[F(x)\Big]_a^b.$$" Summary formula: `\int_a^b f(x)\,dx = F(b) - F(a), \quad F' = f \text{ continuous on } [a, b]`

4. `l9-undo-chain.json` | `screens[5].feedback.correct`, and `summary.formula.note` | imprecise, minor | "Substitution needs the inside's derivative to be present, up to a constant" and "It needs $g'(x)$ in the integral, up to a constant factor" are true of this direct pattern only. | $u = x + 1$ turns $\int_0^3 x\sqrt{x + 1}\,dx$ into $\int_1^4 (u - 1)\sqrt{u}\,du$ with no such factor present (script check; the rule of Stewart 5.5 applied with $g(x) = x + 1$), and the model of homework-3 `items[9]` in this same level substitutes $x = e^s$. Level 4 teaches trigonometric substitutions. A learner would carry "no $g'$, no substitution" into those. | Feedback: "Here substitution needs the inside's derivative to be present, up to a constant. It is not." Summary note: "Used this way, it needs $g'(x)$ in the integral, up to a constant factor."

5. `l12-no-formula.json` | `screens[6].prose`, and `summary.ideas[2]` | imprecise, minor | "Its error shrinks like $h^2$" with no condition on $f$. | Stewart 7.7: $|E_T| \le K(b - a)^3 / (12n^2)$ needs $|f''| \le K$. For $\sqrt{x}$ on $[0, 1]$ the measured order is 1.5 (script, FINDING 5 line). Every integrand in these levels is smooth, so no key is affected. | Prose, last sentence: "For a smooth $f$, one whose second derivative stays bounded, its error shrinks like $h^2$." Summary idea: "For a smooth $f$ the error shrinks like $h^2$: doubling $n$ cuts it by about 4."

6. `l11-to-infinity.json` | `screens[1].feedback.byKey.power-up` | wrong, minor | "You raised the power to $-3$." The slip $\tfrac13 - \tfrac{1}{3b^3}$ comes from $\tfrac{x^{-3}}{-3}$, which lowers the power from $-2$ to $-3$. The next sentence then says, correctly, that integrating raises it. | $-3 < -2$. The fluency set for l7 words the same slip as "You lowered the power to $-3$". | "You lowered the power to $-3$. Integrating $x^{-2}$ raises it by one, to $x^{-1}$."

7. `l4-accumulating-a-rate.json` | `screens[8].explain.text` | imprecise, minor | "$30 \times 1{,}095.89 = £32{,}876.71$ and $60 \times 1{,}232.88 = £73{,}972.60$" are not true as printed: the products are 32,876.70 and 73,972.80. | The stated totals come from the unrounded daily rates (script, FINDING 7). The key 106,849.32 is right and its £1 band takes both routes. | "Thirty days at 4% hold $10{,}000{,}000 \times 0.04 \times \tfrac{30}{365} = \text{£}32{,}876.71$, and sixty days at 4.5% hold £73,972.60: about £106,849 in all. A bond's accrued interest is the area under its accrual rate. When the rate moves every day, the integral does the adding."

8. `l2-thinner.json` | `screens[8].prose` | imprecise, minor | "At a 5% discount rate, £1 due at time $t$ is worth $D(t) = e^{-0.05t}$ today" uses continuous compounding without saying so, at the convention's first use in the course. | With annual compounding the factor is $1.05^{-t}$ (Hull, 4.2). l7, l10 and l11 all say "continuous rate"; l2 comes first and does not. | "At a 5% discount rate, compounded continuously, £1 due at time $t$ is worth $D(t) = e^{-0.05t}$ today."

9. `homework-3.json` | `items[4].widget.tests` | imprecise, minor | A program that ignores `exact` and stops when two successive estimates agree, `abs(trapezium(f, a, b, 2 * n) - trapezium(f, a, b, n)) < tol`, passes all 7 hidden tests. It answers a different question from the one set. | Run under Pyodide with code-runner (key `null`). For an $h^2$ error, $|T_{2n} - T_n| = \tfrac34 |T_n - \text{exact}|$, so the two rules differ only when the error at some doubling lies in $[\text{tol}, \tfrac43\text{tol})$, and no test lands there. | Add an eighth test: `{"call": "n_needed(lambda x: x**2, 0, 1, 1/3, 1.5e-4)", "expect": 64, "compare": "equal"}` (solution returns 64, the other program 32; both run under Pyodide), change "7 hidden tests" to "8 hidden tests" in `how`, and add `byKey.test-8`: "Test 8 expects 64. Compare each estimate with `exact`, not with the estimate before it."

10. `l12-no-formula.json` | `screens[8].feedback.byKey.error` (with `byKey.test-4`) | misleading, minor | The `error` line says "Pass `phi` without brackets", but that mistake never shows this line. `trapezium(phi(), -z, z, n)` and `trapezium(phi(x), -z, z, n)` raise inside test 4 and get key `test-4`, whose line names a different mistake ("not from 0 to `z`"). Key `error` fires only when the code does not load, where the bracket advice is beside the point. | code-runner under Pyodide: both codings give key `test-4`; an unclosed bracket gives key `error`. | `error`: "Your code did not load. Read the last line of the message under the editor: a bracket or an indent is often the cause." `test-4`: "Test 4 expects 0.950004. Integrate `phi` from `-z` to `z`, not from 0 to `z`, and pass `phi` itself, without brackets."

11. `problems-3.json` | `items[2].parts[3].explain.text` | imprecise, minor | "With independent years, compounded wealth tends to shrink even though each year's mean gross return is 1." The typical path shrinks; the mean does not. | Monte Carlo, 200,000 paths of 50 years: median wealth 0.107, 85% of paths below 1, mean wealth 1.00 (by independence $E[\prod X_i] = 1$). | Last sentence: "With independent years, the typical path of compounded wealth shrinks, although its mean stays at 1."

12. `l5-area-undoes-slope.json` | `screens[6].prose` and `screens[6].widget.lines[3].text` | imprecise, minor | The proof takes $h > 0$ only and concludes $A'(x) = f(x)$. That is the right-hand derivative. | Spivak ch. 14, Thm 1 treats $h < 0$ too; the models of homework-2 `items[8]` and `items[9]` do, and the rubric of `items[9]` requires it. The lesson proof should at least say so. | Prose: replace "Take $h > 0$." with "Take $h > 0$; for $h < 0$ the same steps run on the strip $[x + h, x]$."

13. `l1-thin-rectangles.json` | `screens[9].explain.text` | imprecise, minor | "Risk systems compute such chances with sums like this, using far more strips." The numbers on the screen are right; the practice claim could not be established and is doubtful. | Normal probabilities are computed from rational and series approximations to erf (Abramowitz and Stegun 7.1.26; Cody 1969), not from Riemann sums. | Last sentence: "Computers find such chances numerically too, with far finer rules than four strips."

Three findings are `wrong` (1 serious, 2 minor), nine `imprecise` (all minor) and one `misleading` (minor). No graded key is wrong, and no wrong option or slip is right under another valid convention.

## Notes that are not findings

- l2 `screens[6]` gives the gap formula "if $f$ only rises or only falls". The identity $R_n - L_n = (f(b) - f(a))\tfrac{b - a}{n}$ holds for every $f$; monotonicity is what makes the two sums trap the area. True as stated.
- l6 writes $\int \tfrac1x\,dx = \ln|x| + C$ with one constant, as Stewart does. The constant may differ on each side of 0; nothing in these levels integrates across 0 except the $1/x^2$ screen, which is handled.
- l10 `quiz[1]` calls the $u = x^3$ split "harder"; it brings back three times the same integral, as the homework-3 model says of its own analogue. Fair wording.
- l12 `screens[8]`: twice the integral from 0 to `z` with `n` strips fails test 4 although it is a valid estimate. The question fixes "`n` strips on $[-z, z]$", so the test is within its rights.
- problems-3 `items[2].parts[2]` and `items[3].parts[4]` extrapolate an $h^2$ law from $n = 2$. Both predictions agree with the true errors at the precision asked (see above).

## Overlap with earlier reads

Read after the ledger and the findings above were written: `docs/reviews/review-1.3.md` (integrals sections and fix pass), `review-problems-1.3-a.md`, `review-delta-problems-1.3-ab.md`, `review-perf-retrofit-10.md` (the three integrals derivation items). Most of their findings are voice, rendering, tolerance bands, rubric rows and freshness; those are not counted. Conceptual findings only:

| | count | which |
|---|---|---|
| this audit only | 13 | findings 1 to 13 |
| earlier reads only | 5 | review-1.3: homework-1 "U shape" claim against the bars; l4 `quiz[3]` actual/365 unlabelled. perf-retrofit-10: IN3-2 (the other split "leaves a harder integral"), IN2-3 (continuity used three times, not twice), IN2-4 ("No formula exists" for an antiderivative of $\varphi$) |
| both | 0 | |

All five earlier findings are fixed in the text read here, so they could not be found again. New `wrong` that no earlier read found: 3 (findings 1, 2 and 6), over three levels. That is above the convergence limit of one per three levels, so the course needs another blind round after the fix pass.

### Addendum after the earlier reads (not blind, not in the counts above)

14. `l12-no-formula.json` | `screens[8].prose`; `homework-3.json` | `items[8].prose` | imprecise, minor | "As in lesson 9, no formula exists" and "$\int_0^1 e^{-x^2}\,dx$ has no formula". The earlier read (IN2-4) corrected this wording in homework-2 to "no elementary formula"; the same wording survives in these two places, and the blind read passed it. | The antiderivative is a named function, $\tfrac{\sqrt{\pi}}{2}\operatorname{erf}(x)$; what does not exist is an elementary formula (Liouville's theorem; l5 `quiz[1]` and l9 `screens[5]` say it correctly). | l12: "As in lesson 9, no elementary formula exists." homework-3: "$\displaystyle\int_0^1 e^{-x^2}\,dx$ has no elementary formula."

The ledger marks these two rows `imprecise` with the addendum named in the basis: with them it reads 3,916 correct, 14 imprecise, 3 wrong, 1 misleading.

## Engine notes sent to the inbox

Two bullets under "Raised later (audit integrals):" in `docs/BACKLOG-INBOX.md`: the Python `byKey.error` key (ENGINE-BACKLOG 1036 seen again, finding 10), and a check for printed products of rounded figures (finding 7).

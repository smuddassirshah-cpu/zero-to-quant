# Concept audit: integrals level 4, round 1

Blind read at commit `20c509c0`. Scope: lessons l14 to l17, review-4, homework-4, problems-4, fluency-l14-splitting-fractions (levels 1 to 3 are closed). Sources: Stewart, *Calculus* (8e) chapters 6.2, 6.3, 7.2, 7.3, 7.4, 7.7, 7.8, 8.1, 8.3, 9.4; Spivak, *Calculus* (4e) chapters 14, 15, 19; Casella and Berger (2e) examples 2.1.7 and 2.2.4; Feller, *An Introduction to Probability Theory*, volume 1, chapter III.4.

- Ledger: `docs/reports/audit-integrals-4-ledger.md`, 1122 rows: correct 1101, wrong 4, imprecise 15, misleading 2, unverified 0.
- Concepts script: `docs/reports/integrals-L4-concepts.py`, 476 checks, 4 failing. Each failing check is a finding below (1 to 4), so the script exits 1 until the content is fixed.
- Code-widget sweep: `docs/reports/integrals-L4-test-line-sweep.mjs`, 14 submissions to l16 `screens[4]` under the page's Pyodide 0.27.7.

## Verdict

No wrong key, no wrong slip value and no accept figure that its own tolerance refuses. All 62 numeric keys and 142 numeric slip values were recomputed from the named mistake with `scipy.integrate.quad` or by hand, and the three expression keys were differentiated with SymPy. The four printed tables (trapezium on the quarter circle, Cauchy partial means, midpoint on $\frac{1}{\sqrt{x}}$, the $p$-test table) are right to the last digit. The improper-integral teaching is sound: limits are taken one end at a time, the $p$-test is stated with the right side at 0 and at infinity, the comparison test is used only for positive integrands, and the Cauchy mean is shown to be undefined, not 0.

Fourteen findings, all minor. Four are `wrong` as stated: a summary sentence the lesson itself contradicts, a wrong-option reason that gives another option's value, and two printed check figures. The rest are unstated hypotheses or loose wording.

| severity | serious | minor |
|---|---|---|
| wrong | 0 | 4 |
| imprecise | 0 | 9 |
| misleading | 0 | 1 |

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l14-splitting-fractions.json` | `summary.ideas[0]` | wrong, minor | "Each piece integrates to a logarithm or an arctangent." A repeated factor's piece does neither. | `screens[4]` of the same lesson writes $\frac{1}{x^2(x+1)} = -\frac1x + \frac{1}{x^2} + \frac{1}{x+1}$, and $\int \frac{dx}{x^2} = -\frac1x$. Stewart 7.4, case II: a rational function integrates to rational functions, logarithms and arctangents. Concepts script, check "l14 summary.ideas[0]". | `"A rational function splits along the factors of its bottom. Each piece integrates to a logarithm, an arctangent or a power such as $-\\frac{1}{x}$."`

2. `review-4.json` | `items[5].widget.options[2].why` | wrong, minor | The reason given for the option "It equals $\ln 2$" is "You evaluated $\ln|x|$ at 1 and at $-1$". That evaluation gives $0 - 0 = 0$, as the item's own prose shows. It is the route to option B, not to $\ln 2$. | $\ln|1| - \ln|-1| = 0$ (concepts script, check "review-4 items[5]"). $\ln 2$ comes from taking the logarithm of the width $1 - (-1)$. | `"You took $\\ln$ of the interval's width, $1 - (-1) = 2$. The antiderivative is read at each end, and here the curve blows up at 0, inside the interval."`

3. `homework-4.json` | `items[5].explain.text` | wrong, minor | "A numerical check with 16 trapezium strips gives 0.6427." It gives 0.6425. | $T_{16} = 0.642536$, $T_{32} = 0.642658$, exact $\frac{\pi}{8} + \frac14 = 0.642699$ (concepts script). The trapezium error is $\frac{h^2}{12}\left(f'(1) - f'(0)\right) = -0.00016$ at $n = 16$ (Stewart 7.7). A learner who runs l12's `trapezium` sees 0.6425 and doubts the key. | Last sentence: `"A numerical check with 32 trapezium strips gives 0.6427."`

4. `l17-solids-of-revolution.json` | `screens[1].explain.text` | wrong, minor | "Three discs gave 3.0543, 12 would give 3.13". Twelve midpoint discs give 3.1361, which is 3.14 to two places. | $\pi \sum$ of the 12 midpoint discs $= 3.136138$ (concepts script); the midpoint error is $\pi \cdot \frac{h^2}{36} = 0.0055$ at $h = \frac14$. | `"The integral gives exactly the cone formula, $\\pi$. Three discs gave 3.0543, 12 would give 3.136, and the limit is $\\pi$."`

5. `l16-infinite-height.json` | `screens[3].prose`, `screens[3].explain.text`; `l17-solids-of-revolution.json` | `screens[7].explain.text` | imprecise, minor | "Some integrals have no formula", and three sentences later "The exact value is $\sqrt{\pi}\,\text{erf}(1)$". The value has a formula; what is missing is an elementary antiderivative. erf is not defined here or anywhere else in the course. l17 repeats "many have no formula at all". | l12 says "no elementary formula" once; these lines drop the word. $\int_0^1 \frac{e^{-x}}{\sqrt{x}}\,dx = \sqrt{\pi}\,\text{erf}(1) = 1.493648$ (concepts script). Stewart 7.5, "Can we integrate all continuous functions?". | l16 `screens[3].prose` first sentence: `"Some integrands have no elementary antiderivative (l12)."` l16 `screens[3].explain.text` second sentence: `"The exact value is $\\sqrt{\\pi}\\,\\text{erf}(1) \\approx 1.4936$, where erf is the error function, a named integral of $e^{-t^2}$ that is not elementary."` l17 `screens[7].explain.text` last sentence: `"Arc-length integrals often need substitution, and many have no elementary antiderivative, which is where the trapezium rule returns."`

6. `homework-4.json` | `items[8].model` part (a); `l15-circles-and-powers.json` | `screens[10].prose` | imprecise, minor | The integral over the whole line is first met in l15 as $\left[\arctan x\right]_{-\infty}^{\infty}$, and the model answer evaluates it as $\lim_{b \to \infty}\left[\arctan x\right]_{-b}^{b}$. That symmetric limit is right here only because $f > 0$. Part (b) of the same model forbids the same move for $x f(x)$, where it would give 0. The course never says that a two-sided improper integral is two separate limits. | Stewart 7.8, definition 1(c): $\int_{-\infty}^{\infty} f = \int_{-\infty}^{a} f + \int_a^{\infty} f$, both convergent. l11 and l13 have no two-sided integral (searched). | l15 `screens[10].prose`, add as the last sentence: `"An integral over the whole line is two improper integrals, one for each half, and both must converge."` homework-4 `items[8].model` part (a), replace the display by `$$\\begin{aligned} \\int_{-\\infty}^{\\infty} f(x)\\,dx \\\\ &= \\frac{1}{\\pi}\\Big(\\lim_{b \\to \\infty}\\arctan b - \\lim_{a \\to -\\infty}\\arctan a\\Big) \\\\ &= \\frac{1}{\\pi}\\left(\\frac{\\pi}{2} + \\frac{\\pi}{2}\\right) = 1. \\end{aligned}$$` and follow it with `"Each half converges, so the two limits may be taken separately. $f$ is positive, so it is a density."`

7. `l15-circles-and-powers.json` | `screens[10].feedback.byKey.normal-habit`, `screens[10].explain.text`; `homework-4.json` | `items[8].model` part (d) | misleading, minor | "The Cauchy has fatter tails, so less mass sits near the centre" and "against 68% for a normal, which shows the fat tails". The 68% is for one standard deviation. The Cauchy has no standard deviation, and its unit is the half interquartile range. A normal with the same quartiles also puts exactly 50% within $\pm 1$, so 50% against 68% shows a choice of unit, not a tail. | Concepts script: normal with quartiles $\pm 1$ has $\sigma = 1.4826$ and $P(|X| \le 1) = 0.5$; $P(|X| > 5)$ is 0.126 for the Cauchy and 0.00075 for that normal. Casella and Berger example 2.2.4 (no moments). | `normal-habit`: `"That is a standard normal's chance of landing within one standard deviation. This density is Cauchy, so integrate it from $-1$ to 1."` `screens[10].explain.text`: `"Half the probability sits within $\\pm 1$, so $\\pm 1$ are the quartiles. A normal with the same quartiles puts under 0.1% beyond $\\pm 5$. The Cauchy puts 12.6% there, because $f(x)$ falls only like $\\frac{1}{x^2}$."` homework-4 `items[8].model` part (d), last sentence: `"Half of all days fall within $\\pm 1$ unit. A normal with the same quartiles puts under 0.1% of days beyond $\\pm 5$ units and the Cauchy puts 12.6% there, which shows the fat tails."`

8. `l16-infinite-height.json` | `screens[11].prose` | imprecise, minor | "The share $X$ of time a fair game's P&L is positive has the arcsine density". The arcsine law is the limit for a long game (exact for Brownian motion). For a short game the chance is visibly larger. | Feller volume 1, III.4, theorem 2 and its limit. Monte Carlo, 20,000 paths of a fair $\pm 1$ game (concepts script): $P(\text{share} \le 0.1) = 0.27$ for 20 steps and 0.205 for 2,000 steps, against the arcsine 0.2048. | First sentence: `"Over a long fair game, the share $X$ of time the P&L is positive has, very nearly, the arcsine density $\\frac{1}{\\pi\\sqrt{x(1 - x)}}$ on $(0, 1)$."`

9. `l17-solids-of-revolution.json` | `screens[11].explain.text` | imprecise, minor | "the joint density $\frac{1}{\pi}e^{-(x^2 + y^2)}$ of two independent shocks". Elsewhere in the level a "shock" is standard normal (l16 `screens[10]`). This density belongs to two independent normals of variance $\frac12$; the standard pair has $\frac{1}{2\pi}e^{-(x^2 + y^2)/2}$. | $\int x^2 \frac{e^{-x^2}}{\sqrt{\pi}}\,dx = \frac12$ and the double integral is 1 (concepts script). Casella and Berger 4.2 (independent normals). | `"The volume is $\\pi$, so $\\frac{1}{\\pi}e^{-(x^2 + y^2)}$ has total probability 1. It is the joint density of two independent normal shocks, each of variance $\\frac12$. Shells and polar coordinates are the same slicing: $2\\pi r\\,dr$ is the area of a thin ring."`

10. `l17-solids-of-revolution.json` | `screens[4].feedback.byKey.discs-in-x`, `screens[8].prose`, `summary.ideas[1]`, `summary.formula.note` | imprecise, minor | "About the $y$-axis the slices are shells, not discs" and "Pick the formula from the axis of the turn". The axis decides only once the strips are taken in $x$. The same solid about the $y$-axis is also a stack of washers in $y$. | Stewart 6.2 and 6.3: the method follows from whether the strip is perpendicular (disc, washer) or parallel (shell) to the axis. For `screens[4]`, washers in $y$ give $\pi\int_0^1 (1 - y)\,dy = \frac{\pi}{2}$, the same volume (concepts script). | `discs-in-x`: `"You used $\\pi\\int_0^1 (x^2)^2\\,dx = \\frac{\\pi}{5}$. That spins the region about the $x$-axis. About the $y$-axis a strip at $x$ sweeps a shell, not a disc."` `screens[8].prose` first sentence: `"With strips taken at each $x$, pick the formula from the axis of the turn."` `summary.ideas[1]` first sentence: `"About the $y$-axis a strip at $x$ sweeps a shell of volume $2\\pi x\\,f(x)\\,dx$."` `summary.formula.note`: `"For strips at each $x$: discs for a turn about the $x$-axis, shells about the $y$-axis."`

11. `l15-circles-and-powers.json` | `screens[8].canvas.params.rows` and `canvas.state.caption` | imprecise, minor | The table gives $\sqrt{a^2 - x^2} = a\cos\theta$, $\sqrt{a^2 + x^2} = a\sec\theta$ and $\sqrt{x^2 - a^2} = a\tan\theta$ with no range for $\theta$. Each holds only where the trigonometric term is positive. For $x \le -a$ the secant row gives $-a\tan\theta$ on the usual range. | Stewart 7.3, table of trigonometric substitutions, which prints the three ranges. The lesson states the range only in `screens[9]` (tangent) and homework-4 `items[1]` (sine). | Caption: `"Pick the substitution that makes the root a single trigonometric term. Take $\\theta$ where that term is positive: between $\\pm\\frac{\\pi}{2}$ for sine and tangent, and $0 \\le \\theta < \\frac{\\pi}{2}$ for secant with $x \\ge a$."`

12. `l16-infinite-height.json` | `quiz[1].widget.options[3].why` | imprecise, minor | "With $p = 0.9$ the area grows like $a^{0.1}$." In this lesson $a$ is the lower cut-off that tends to 0, where $a^{0.1}$ shrinks. The upper limit is $b$ in l11. | $\int_1^b x^{-0.9}\,dx = 10\left(b^{0.1} - 1\right)$. | `"This trouble is at infinity, where $p$ must exceed 1. With $p = 0.9$ the area up to $b$ grows like $b^{0.1}$."`

13. `l16-infinite-height.json` | `screens[4].feedback.byKey.test-6` | imprecise, minor | "If you evaluate at an end of a strip, the first call divides by zero." Every natural coding of that mistake fails test 1 first, so the learner who makes it never sees this line. | Sweep under Pyodide: left-endpoint, right-endpoint, trapezium and Simpson codings all return key `test-1` (values 0.21875, 0.46875, 0.34375, 0.33333 against 0.328125). No coding in the sweep failed test 6 first. The line is true of its test. | Move the diagnosis to the line that is shown. `test-1`: `"Test 1 expects 0.328125 for $x^2$ on $[0, 1]$ with 4 strips: the centres are 0.125, 0.375, 0.625, 0.875. A result of 0.21875, 0.46875 or 0.34375 means you used strip ends."` `test-6`: `"Test 6 is $\\frac{1}{\\sqrt{x}}$ with 10 strips, where the first centre is 0.05. Check that no call reaches $x = 0$."`

14. `l16-infinite-height.json` | `screens[4].canvas.params.lines` | imprecise, minor | The console is titled "Your trapezium from l12" and shows `line 5, in trapezium` with no frame for the lambda. l12's solution raises on its line 7, inside the lambda, so the real traceback has one more frame. The error message itself is right. | CPython 3.13 run of l12 `screens[3]` solution: frames `<module>`, `line 7, in trapezium`, `line 1, in <lambda>`, then `ZeroDivisionError: 0.0 cannot be raised to a negative power`. Pyodide 0.27.7 is CPython 3.12, same message. | Lines 4 and 5 become three lines: `"  File \"<stdin>\", line 7, in trapezium"`, `"  File \"<stdin>\", line 1, in <lambda>"`, `"ZeroDivisionError: 0.0 cannot be raised to a negative power"`, with `canvas.state.tone` `{"l6": "err"}`.

## Checked and found sound (the watch list)

- Improper integrals and convergence. l16 defines $\int_0^1 f = \lim_{a \to 0^+}\int_a^1 f$, splits at an interior blow-up before any antiderivative, and gets every $p$-test case right, including $p = 1$ at both ends. The comparison test is stated for positive integrands each time. problems-4 keeps the bound, the substitution and the limit as separate parts and each chains.
- Densities and expectations. The Cauchy density integrates to 1; the mean is shown undefined with a limit for each half, and the option "$E[X] = 0$ by symmetry" is refused for the right reason. Monte Carlo (20,000 samples of the mean of 10 and of 1,000 draws): $P(|\bar{X}| \le 1) = 0.50$ at both sizes, so the mean of $n$ draws is again Cauchy, as homework-4 says. The chi-square(1) density and $P(X \le 1) = 0.6827$ agree with `scipy.stats.chi2`.
- Numerical integration error. The trapezium table for the quarter circle (ratio 2.8 per doubling), the midpoint table for $\frac{1}{\sqrt{x}}$ (ratio $\sqrt{10}$ per tenfold $n$; first strip carries 97% of the error) and the $h^2$ rate for $\cos x$ all recompute. The constant "about $\frac{0.59}{\sqrt{n}}$" is the first strip alone; the whole error is $\frac{0.605}{\sqrt{n}}$, within the stated "about".
- Finance applications. The logit as $\int \frac{dp}{p(1-p)}$, the logistic share times ($\frac{\ln 9}{0.5}$, $\frac{2\ln 19}{0.8}$) and the impact kernel ($2\ln\frac32$, $2\ln 2$, share 0.585) are right, with every slip value matching its named mistake.
- Earlier band findings on problems-4 (review-problems-1.3-c 6, 7, 9; review-delta-problems-aa-2 1; review-delta-ac-3 4.1) are fixed at this commit: every printed accept figure is accepted by its own tolerance (concepts script).

## Code-widget sweep (l16 `screens[4]`, `midpoint`)

Run with `node docs/reports/integrals-L4-test-line-sweep.mjs <app> <pkgs>` under the page's Pyodide.

| submission | key | rows (tests 1 to 7) |
|---|---|---|
| solution | pass | PPPPPPP |
| starter | test-1 | FFFFFFF |
| left endpoint | test-1 | FFPFFEE |
| right endpoint | test-1 | FFPFFFF |
| trapezium | test-1 | FPPFFEE |
| Simpson | test-1 | FPPFFEE |
| `range(1, n + 1)` with $i + 0.5$ | test-1 | FFPFFFF |
| `range(1, n + 1)` with $i - 0.5$ | pass | PPPPPPP (correct) |
| centre as mean of the two edges | pass | PPPPPPP (correct) |
| ignores `a` | test-5 | PPPPFPP |
| returns `total` without `h` | test-1 | FFFFPFF |
| `//` for `h` | test-1 | FPFFPEE |
| left endpoint with a guard at 0 | test-1 | FFPFFFF |
| syntax error | error | load error |

- `test-1` line: describes its test and is true. Correct.
- `test-6` line: names "evaluate at an end of a strip"; all four codings of it fail test 1 first. Finding 13.
- `error` line: shown for a load error only. Correct.
- No wrong program passes every test. No line is timing-dependent.

## Overlap with earlier reads

Read after the ledger and findings were written: `docs/reports/integrals-4.md` (author report), `docs/reports/problems-integrals.md`, `docs/reports/fluency-integrals.md`, `docs/reviews/review-problems-1.3-c.md` (findings 6 to 9 on problems-4), `review-delta-problems-aa-2.md` (finding 1), `review-delta-ac-3.md` (4.1), `review-delta-ae-1.md`, `review-perf-retrofit-8.md` (voice notes). `review-1.3.md` predates level 4 and does not cover it. No second read of the four lessons, review-4 or homework-4 was found.

| conceptual findings | count |
|---|---|
| this audit only | 14 |
| earlier reads only | 1 (review-problems-1.3-c finding 8, a slip line naming a number the learner did not type; fixed) |
| both | 0 |

The five other earlier findings on problems-4 are grading-band and accept-line findings, all fixed. New `wrong` not found by any earlier read: 4, all minor.

## Gates

- Validator: 0 errors, 4623 warnings.
- `node tools/run-number-scripts.mjs --only integrals`: 5 of 436 scripts, 5 passed, 0 new failures.
- `node tools/grade-all.mjs --file` on each of the 8 files: 0 failures each.
- `docs/reports/integrals-L4-concepts.py` (venv Python 3.13, NumPy, SciPy, SymPy; no figure depends on a version): 476 checks, 4 failed, exit 1. The four failures are findings 1 to 4.
- No playthrough, as the brief sets.

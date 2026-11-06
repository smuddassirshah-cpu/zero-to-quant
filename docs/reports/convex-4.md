# convex level 4 (Algorithms): report

## Files (app/content/courses/convex/)

| file | screens or items | quiz | canvases and widgets |
|---|---|---|---|
| l14-gradient-descent.json | 12 screens | 4 | `plane` contours of $\tfrac12(x^2 + 10y^2)$ with the ten-step descent path from $(10, 1)$ (11 points, 10 segments) and a live step control; logistic-curvature plane; weights `bars`; `expression` $2/L$; backtracking `order` with distractors; `code` (NumPy) |
| l15-convergence-rates.json | 11 screens | 4 | log-error `plane` ($\kappa = 2$ against 100) with a step control and riding vline; table widget of counts beside a log plane; rate `order` derivation; correlated-pair contours with fast and slow vectors; round-bowl rescale; $x^4$ table; `code` (NumPy) |
| l16-newton-for-minimising.json | 12 screens | 4 | `plane` of $x - \ln x$ with the quadratic model at $x_k$ (control) and its minimum marked; error and cost tables; Kelly growth plane; Newton-step `order`; root-finder trap plane with tangents; model at 2.5 for the edge case; `code` (NumPy) |
| l17-checking-a-solver.json | 12 screens | 4 | `console` solver output (colleague, `linprog`, the flipped sign); KKT `table`s; checklist; dual-feasibility screen; procedure `order`; degenerate optimum `bars`; two `code` screens (NumPy; NumPy and SciPy SLSQP) |
| review-4.json | 10 items, `pass` 0.8 | | difficulty 2 to 4; all four lessons; one level 3 recall (KKT sign of $\lambda$ in Boyd's form) and one level 2 LP certificate |
| homework-4.json | 8 items | | difficulty 3 to 5 (two at 5); step-limit `order` proof; Newton-map `expression`; `code` `compare_methods` (difficulty 5); `longform` "stuck after 200 steps" with a 10-point rubric |

No performance task: the lesson objectives start with Run, Link, Minimise and Check, so the verb rule does not match.

## Gates

- Validator (`node tools/validate.mjs`): 0 errors; no warnings on level 4 files.
- Voice scan (`VOICE_BASE=app/content/courses/convex/`): 0 sentences over 20 words, 0 explanations over three sentences.
- Numbers: `docs/reports/convex-L4-numbers.py` exits 0: 397 of 397 `numbers_lib` checks, 0 two-route failures, 0 wrong values inside an answer band (rule 581 checked by hand in the script: every numeric and table `wrong` satisfies $|w - a| >$ tolA + tolW). It runs all 6 code widgets in CPython: every solution passes all its tests, every starter passes none.
- Playthrough with `--local-cdn` (this session's pkgs):

| file | desktop | `--mobile --tablet` (440, 1032, 1376) |
|---|---|---|
| l14-gradient-descent | ok, 16 checks, quiz 4/4 | ok |
| l15-convergence-rates | ok, 15 checks, quiz 4/4 | ok |
| l16-newton-for-minimising | ok, 16 checks, quiz 4/4 | ok (replayed after the last edit) |
| l17-checking-a-solver | ok, 16 checks, quiz 4/4 (SciPy SLSQP green in Pyodide) | ok |
| review-4 | ok, 10 of 10 recorded | ok |
| homework-4 | ok, 8 of 8 right, 38 of 38 marks, longform marked by the button | ok |

Screenshots read at all widths. Fixes made: l14 optimum label moved off the origin tick, trap opens at $s = 0.1$ so the caption does not show the answer; l15 counts ladder given a log plane; l16 boundary line removed from the hook (it sat on the left edge), trap tangent slope corrected to 0.40938.

## Numbers and sources

Each value is computed twice in the script: a closed form or exact fractions against the algorithm itself (fixed-step descent, Newton, backtracking, SLSQP, HiGHS, `numpy.linalg`).

Reproduced from the brief: step limits 0.2, 0.5, 2.5; factors 0.9, 0, $\pm\tfrac{9}{11}$, $-1$, $-1.1$; 3.4868; $(1.3443, 0.1344)$; 2.5937; $(0.25, 0.1778, 0.1375)$; counts 13, 28, 69, 270, 691 and 20, 49, 132, 532, 1,375 (formula and simulation); 0.078, 0.002, $\kappa = 39$ and 4; $\tfrac{9}{11}$ fitted by `polyfit`; Newton iterates and errors of $x - \ln x$; $-1.25$ and 0; the factor $\tfrac23$ on $x^4$; Kelly 0.090909, 0.099951, 0.0999999987 and growth 0.009712; $(0.01, 0.3133, 0.6767)$ with return 10.0001%, variance 0.082106, residual $(0.0174, -0.0349, 0.0174)$ (fitted $\lambda = -0.1964$, $\mu = 3.5957$) and gap 0.000995; LP gap 0; bound 0.077222 and 0.004884; rounded output 0.081162 and 10.001%; the flipped-sign run (SLSQP success, $(0.5902, 0.2623, 0.1475)$, 6.672%).

Computed and reported ("compute and report" in the brief):
- Descent on $x - \ln x$ with $s = 0.25$: 44 steps to within $10^{-6}$; Newton 5 (errors $1.53 \times 10^{-5}$ after 4, $2.3 \times 10^{-10}$ after 5).
- `newton_minimise` with stop $\lVert\nabla f\rVert \le 10^{-12}$: $x - \ln x$ from 0.5 in 6 steps, Kelly from 0 in 4, the three-asset quadratic in 1; `newton_damped` (halve until $f(x - td) \le f(x)$): from 2.5 in 6 steps (one halving, first damped point 0.625, $f$ 1.584 to 1.095), from 2 in 1, from 0.5 in 6.
- `check_portfolio` signature `(Sigma, m, target, w, cap=None, tol=1e-6)`, returning `feasible`, `lam`, `mu`, `nu`, `eta`, `stationarity`, `signs_ok`, `gap`; the four-asset book passes with $\nu_1 = 0.018889$, $\eta_4 = 0.0308$ and gap $< 10^{-17}$.
- `compare_methods` counts: $\kappa = 39$ pair with $\mathbf{q} = (0.06, 0.02)$ from 0: 306 against 1; Kelly 9 against 3; bowl $\operatorname{diag}(1, 10)$ from $(10, 1)$ at tol $10^{-6}$: 83 against 1 (at $10^{-8}$ the count sits at 104.997, too close to an integer, so not used); $x - \ln x$: 60 against 5.
- Added: $\kappa = 1000$ needs 6,908; shrinking the pair halfway gives correlation 0.475, $\kappa \approx 2.81$, 19 steps; ridge example eigenvalues 3 and 1, limit 0.5 with $\lambda = 0.5$ ($\tfrac23$ without); logistic $L = \tfrac14$ so $s < 8$; $x^4$ descent at $s = \tfrac1{12}$: $f = 0.01234$, 0.000204, $2.2 \times 10^{-6}$ after 10, 100, 1,000; sublinear bound 500,000 steps; cost ratio $n/3 = 100$ at 300 assets; risk parity Newton 1.8519, 2.9064, 3.4687, 3.5349 to $\sqrt{12.5}$, weights $(\tfrac23, \tfrac13)$; degenerate optimum at $\tfrac{163}{1700}$: $(0, \tfrac{8}{17}, \tfrac{9}{17})$, $\lambda = -\tfrac{12}{85}$, $\mu = \tfrac{48}{17}$, $\nu_1 = 0$; invalid dual point $(-0.1, 2.5, (0, 0, -0.1))$ gives $g = 0.109527 > 0.081111$; review and homework figures (62, 118, 9, 4, 0.8, 870, 2, 0.6, 35, 0.005008, 0.0009, $\tfrac{2x}{2x^2 + 1}$).

**Brief errors and corrections.**
- l17 edge case: "the multipliers from `lstsq` are not unique" does not hold for the natural example. At the 9.588% target, $w_1 = 0$ and $\nu_1 = 0$, but $\lambda$ and $\mu$ are unique. What is ambiguous is the active set (asset 1 free or at 0 both pass KKT); the screen teaches that.
- l14: $\tfrac{2}{11}$ has the best worst-case factor, but it is not the step that ends nearest the optimum after ten steps from $(10, 1)$ ($s = 0.19$ ends at distance 1.2648, against 1.3510). The lesson says "smallest worst factor", never "closest after ten steps".
- l15: the $1/\lambda_{\max}$ counts (20 to 1,375) hold for a start along the slow direction; from $(1, 1)$ they are 20, 47, 128, 519, 1,341. The table says "from a start along the slow direction".
- l15: on $x^4$ the observed $f$ falls like $1/k^2$; the $1/k$ is the guarantee for convex $L$-smooth $f$. The screen states the guarantee and calls the $x^4$ run sublinear.
- l16: "5 or 6 iterations" depends on the stop: 5 to within $10^{-6}$, 6 with the $10^{-12}$ gradient stop the code uses.
- Homework: `compare_methods(f, grad, hess, x0, tol)` needs no `f`; the signature is `(grad, hess, x0, tol=1e-8)`.
- Every general rule carries its hypotheses (positive definite Hessian for the step limit, the rate and one-step Newton; convex with curvature at most $L$ for $2/L$ and the $1/k$ bound; $f'' > 0$ for Newton's minimising step and quadratic convergence; dual feasibility for weak duality; convexity for KKT to certify a global optimum).

## Runtime

NumPy in l14 to l16; SciPy SLSQP in l17's second code screen, green in Pyodide. Tests compare numbers only, at absolute $10^{-9}$ (closed forms), $10^{-6}$ (solver weights and fitted values) and $10^{-12}$ (Newton points); step counts exactly. No value differed between Pyodide and CPython 1.18.1 at these tolerances. `res.multipliers` is never used; multipliers come from `lstsq` on the free rows. SciPy load time could not be measured separately (no per-item timing; raised in level 1); l17 took 46.8 s across three widths against 43.6 s for l16, so the local load is a few seconds. Each `how` says "a few seconds from cache, longer on a first visit".

## Canvases

- Descent path (l14): 11 points $p_0$ to $p_{10}$ joined by 10 segments. For this diagonal quadratic each point is a closed form in `derive` ($x_k = 10(1 - s)^k$, $y_k = (1 - 10s)^k$), equivalent to the brief's `let` chain and cheaper. A control on $s$ (0.02 to 0.25, step 0.001) and a caption with the distance after ten steps.
- Error plots (l15) use `yScale: "log"`; the hook's vline rides a control on $k$ and the caption scales the error by $10^6$.
- Newton model (l16): the model $q$ is a plane function of the param $a = x_k$; `derive` places $x_k$ and the model's minimum $(2a - a^2, a - \ln a - \tfrac12(a - 1)^2)$.

## Notes

- Scratchpad: this session's `19ed1109...` folder, subfolder `convex-4` (the brief's `a8ff8d32...` paths are stale; the brief also says not to run git, and the orchestrator asked for one commit, which I followed).
- `numerics` l5-bisection-and-newton is now written, so l16 cites it beside `taylor` l3.
- No `course.json` change proposed.
- Inbox: 3 bullets under "Raised later (convex level 4)".

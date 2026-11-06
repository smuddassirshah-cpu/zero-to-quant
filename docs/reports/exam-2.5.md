# Topic 2.5 exam: numerical methods and optimisation

File: `app/content/exams/topic-2.5.json` (110 minutes, pass 0.7, 30 items, all eleven skills of `convex` and `numerics`). Scripts: `docs/briefs/exam-2.5-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Result

- Ramp 6, 15, 6, 3 at difficulties 2 to 5; pace 5,280 s (88 min).
- By course and level: convex L1 3, L2 3, L3 4, L4 4; numerics L1 6, L2 3, L3 3, L4 4.
- Coverage: every level has an auto-graded item on a skill first met there. `cv-duality` first appears in convex l8, so L2 is covered by `e-duality-sandwich` and L3 by `cv-qp` items. `check_numbers.py` derives this from `course.json` and the lesson files.
- Kinds: 14 parts, 8 numeric, 4 choice, 1 multi, 1 expression (Richardson for an order-3 rule), 1 order (a local minimum of a convex function is global, two flawed lines) and 1 Python `code` item (`log_sum_exp`, 9 hidden tests). No longform: every skill and level is on an auto item.
- Hypotheses are stated wherever they matter: convexity and Slater for strong duality and KKT sufficiency, affine limits, a bounded polygon for the LP corner, a positive definite quadratic and the stated step for descent rates, $f'' > 0$ near the minimum for Newton, continuity with a sign change for bisection, and the test equation for every stability factor.

## Gates

- Validator: 0 errors, no topic-2.5 warnings.
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice25/`): 0 sentences over 20 words, 0 explanations over three sentences, 744 sentences. No exclamation marks, em-dashes or en-dashes outside maths.
- `check_numbers.py`: 315 of 315, exit 0. Route B uses vertex enumeration and a grid search for the LP, descent and Newton run step by step, projected gradient for the KKT items, a brute-force simplex search for the long-only portfolio, NumPy's `spacing`, `polyfit` and Gauss-Legendre nodes, a general natural-spline solver, 40- and 50-digit decimals for the floating-point items, exact Fractions, and seeded simulations for the Monte Carlo and control-variate items. The code solution passes all 9 cases in CPython and the starter fails 5 (overflow, a log of 0, a subnormal sum). A final pass reads every number in every learner-visible string.
- Playthrough with `--local-cdn`: green with and without `--mobile` (30 of 30, the code item run in Pyodide); screenshots at 1280 and 440 px checked.

## Freshness

Superseded in part (session U fix pass): 13 items were rewritten for freshness and 16 keys changed; `docs/reviews/review-exam-2.5.md` `## Fix pass` is the current list. The list below is the author's pre-review state.

Clashes found before the first build were replaced: the LP limits $x + y \le 4$ (convex l10, review-3) became $x + 2y \le 8$ and $3x + 2y \le 12$; the projection $(x - 3)^2 + (y - 2)^2$ with $x + y \le 2$ (convex homework-3) and $x + 2y \le 2$ (convex review-3) became $(x - 4)^2 + (y - 1)^2$ with $x + 2y \le 3$; $e^x - 2x$ (convex l3, l16) became $e^x - 3x$; eigenvalues 0.5 and 8 (convex l14) became 0.4 and 10; $\kappa(\mathbf A) = 3 \times 10^5$ (numerics homework-1) became $2 \times 10^6$; $\rho = 0.9$ with factor 5.2632 (numerics l16) became $\rho = 0.95$; the return-floor `w @ m - 0.07` (convex l12) became a variance cap; `safe_newton` (numerics l6) was dropped as the code item for `log_sum_exp`. After the first build `fresh.py` caught `exp(1e-10) - 1` (numerics l2, homework-1), so that item became `math.log(1 + 3e-12)`. Remaining hits are unrelated numbers in other courses and the weight vector $(0, 0.5, 0.5)$, which convex homework-1 uses in a different setting.

# Topic 1.11 exam: complex numbers, vector calculus and differential equations

File: `app/content/exams/topic-1.11.json` (100 minutes, pass 0.7, 30 items, all fourteen skills of `complex`, `vector-calc` and `odes`). Scripts: `docs/briefs/exam-1.11-scripts/` (`build.py` route A, `check_numbers.py` route B, `fresh.py`).

## Result

- Ramp 6, 15, 6, 3 at difficulties 2 to 5; pace 4,920 s (82 min).
- By course and level: complex L1 3, L2 2, L3 6; vector-calc L1 2, L2 2, L3 3; odes L1 2, L2 3, L3 3, L4 4.
- Coverage: every level has an auto-graded item on a skill first met there, except odes L3. That level adds no new skill (`de-systems` first appears in l4-slope-fields), so it is covered by three `de-systems` items pitched at l10 to l13. `check_numbers.py` derives this from `course.json` and the lesson files.
- Kinds: 12 parts, 10 numeric, 3 choice, 1 multi, 3 expression (one complex, one harmonic conjugate, one transform) and 1 order. There are two order derivations, each with two flawed lines: the semicircle lemma, and a Laplace solution inside a parts item. 30 items cover all 14 skills and 10 levels, so no longform was needed.
- Hypotheses are stated wherever a theorem is used: analytic on and inside the path, degree gap 2 and no real zeros, Green, Stokes and divergence with continuous derivatives on the region, simply connected for the potential, Euler and RK4 stability on the test equation, a hyperbolic equilibrium for linearising. No item claims that critical damping settles fastest; `e-damping-rate` says only that the slow mode decays more slowly past critical, which the script checks over $b$ from 0.5 to 20.

## Gates

- Validator: 0 errors, no topic-1.11 warnings.
- Voice scan on a copy (`VOICE_BASE=<scratch>/voice111/`): 0 sentences over 20 words, 0 explanations over three sentences, 684 sentences. No exclamation marks, em-dashes or en-dashes (the script checks this outside maths).
- `check_numbers.py`: 288 of 288, exit 0. Route B uses Fractions, trapezoid contour integrals, Simpson line and real integrals, face-by-face surface flux, RK4 for every ODE value, a series matrix exponential, numerical Laplace transforms and a Carr-Madan integral against Black-Scholes at two values of $\alpha$. Expression forms are evaluated from their LaTeX; wrong forms must differ, and the harmonic-conjugate forms are tested by finite-difference Cauchy-Riemann. A final pass reads every number in every learner-visible string.
- Playthrough with `--local-cdn`: green with and without `--mobile` (30 of 30); screenshots at 1280 and 440 px checked, including both order lists and the three-part items.

## Freshness

Clashes found before the first build were replaced: the cube roots of $\pm 8i$ (complex l4) became the fifth roots of $-32$; $u = x^3 - 3xy^2 + y$ (complex homework-2) became $e^x\cos y + 2xy$; $y'' - y' - 6y$ (odes review-2) became $y'' + 2y' - 8y$ with forcing $12e^{2t}$; $y' + 3y$ (odes l3) became $y' + 4y = 9e^{-t}$; $y'' + 4y' + 3y$ (odes review-3) and $y'' + 5y' + 4y$ (odes l9) became $y'' + 6y' + 5y$; $\begin{pmatrix}1&2\\2&1\end{pmatrix}$ (odes l11, l12) became $\begin{pmatrix}1&4\\1&1\end{pmatrix}$; $x' = x(2 - y)$, $y' = y(x - 1)$ (odes l13) became the crowded $x(4 - x - 2y)$, $y(x - 2)$; the rate gap 0.06 to 0.02 (odes l5) became 0.045 from 0.07. After the first build `fresh.py` caught two more: the tangent pair $(1, 0, 2), (0, 1, 3)$ is a vector-calc l9 key, so the patch became $(u, v, 3u - v)$; $\lambda = 50$ with RK4 limit 0.0557 is numerics homework-3, so the stiff item uses $\lambda = 80$. Remaining hits are unrelated numbers in other courses, the Carr-Madan damping notation, and the theorem hypothesis $\deg q \ge \deg p + 2$. Complex l11 orders the semicircle argument for $\tfrac{1}{1 + x^2}$; this exam proves the general lemma with different flawed lines.

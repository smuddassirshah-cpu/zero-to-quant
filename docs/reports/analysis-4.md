# Report: analysis level 4 (Continuity and the derivative)

Course `analysis` (topic 1.10, strand pure), level 4, from `## Level 4` of `docs/briefs/analysis.md`. Lesson ids, names, objectives and skills are as in course.json. l15, l17 use `an-continuity`; l16 uses `an-continuity`, `an-reals`; l18 uses `an-calculus`; l19 uses `an-continuity`, `an-sequences`.

Brief errors found: (1) the l15 hook's largest δ is √4.1 − 2 ≈ 0.024846, not 0.025158; (2) the brief's `\min(\frac{a}{2}, \frac{a^2\varepsilon}{2})` expression answer cannot be graded, as `\frac{a}{2}` alone passes. Both are worked around (see Departures).

## Files written (app/content/courses/analysis/)
| file | screens / items | quiz | canvases |
|---|---|---|---|
| l15-epsilon-delta.json | 12 | 5 | plane ε-δ box (slider; ε and δ controls), plane cap picture, plane sin(1/x), plane 1/x boxes, table (quiz) |
| l16-intermediate-value.json | 12 | 4 | number-line with a table bound to its points, number-line final interval, plane proof pictures, plane 1/x jump, plane sin(1/x), console, plane Black-Scholes price against volatility |
| l17-extreme-value.json | 11 | 4 | plane with a four-frame "Picture" control, plane bound to a table, plane on [−2, 2], number-line (1/n in (0, 1]), plane trap and stress test |
| l18-mean-value-proved.json | 12 | 5 | plane with draggable P on abs(x) and on a hump (live quotient caption), plane chord and g, plane x³ with tangent, table (quiz) |
| l19-uniform-convergence.json | 12 | 4 | plane x^n with an n control and a band, bump with a derived peak, x/n, M-test partial sums with an N control, smoothed digital with a step function, console |
| review-4.json | 8 items, difficulty 2 to 4 | | 3 numeric, 5 choice; covers every lesson |
| homework-4.json | 9 items, difficulty 3 to 5 (three at 5) | | expression, choice ×2, order ×2, numeric ×2, code (d5), longform (d5) |

- **Longform rubric:** 1+2+2+2+1+2 = 10, with a full model answer.
- **Generators:** gen_l15.py to gen_l19.py, gen_review4.py, gen_homework4.py and common.py.
- **Checks:** calc.py and calc_hw.py hold the numbers; codecheck.py runs each solution and starter against the tests in CPython.
- **Grader probe:** exprcheck.mjs runs ZQ.grade.exprEqual in Chromium with the local Compute Engine.
- **Location:** all of these are in the scratchpad folder `analysis-4`.

Lesson shapes:
- **l15:** slider hook, explore (names continuity), derive 3x+1, ladder ×2 (factorise, cap), derive ε/5, order proof, trap δ = ε, order (sequential criterion), generalise (sin(1/x) by a sequence), edge case 1/x, transfer.
- **l16:** bisection table hook, ladder (width), generalise IVT, three derive steps of the sup proof, order (whole proof), order (bisection proof), trap (no continuity), converse fails, code, transfer (implied volatility).
- **l17:** place hook (which hypothesis fails), candidate table, ladder multi, generalise EVT, three derive steps of the bounded part, order (bounded), order (attained), trap (f' = 0), transfer (stress test).
- **l18:** abs(x) quotients ×2, generalise, order (differentiable implies continuous), ladder ×2 (quotient signs at a maximum), order (interior extremum), order (Rolle), multi (hypotheses used), expression g, trap x³, transfer (call spread).
- **l19:** explore x^n, sup gap 1, generalise uniform, ladder ×3 (0.9^n, bump, x/n), order (ε/3), choice (why n before δ), M-test, trap, code, transfer (smoothed digital).

Edge cases:
- **l15:** 1/x at a = 0.1, where δ shrinks as a → 0.
- **l16:** the converse fails (sin(1/x)).
- **l17:** constant function (quiz).
- **l18:** x² sin(1/x) (quiz).
- **l19:** triangles of area 1 (quiz).

## The ε-δ box
It could be drawn and driven as the brief describes.
- **Box:** a `polygons` entry on four hidden points, whose corners `derive` from params `eps` and `delta`.
- **Band and window:** the band f(a) ± ε is an `area` between two dashed functions. The window edges are `vlines` with derived x.
- **Curve over the window:** a second function `x^2` with domain `["2 - delta", "2 + delta"]`.
- **Caption:** a derive caption reads "stays in the box" or "leaves the box" through a ternary.
- **Driving it:** the hook grades a `slider` bound to `delta`, and the explore screen has controls on `eps` and `delta`.

## Departures from the brief
- **l15 hook numbers.** The right end binds: (2 + δ)² < 4.1 needs δ ≤ √4.1 − 2 = 0.024846. The figure 2 − √3.9 = 0.025158 is only the left end's limit.
  - At δ = 0.025, 2.025² = 4.100625 > 4.1.
  - The slider steps 0.001 from 0.001. It accepts 0.001 to 0.024 (answer 0.0125, tol 0.01151).
  - 0.025 has its own wrong range, "edge", and 0.026 to 0.06 is "wide". So 0.02 passes and both 0.025 and 0.03 fail.
- **l15 edge case, an expression grading hole.** In Chromium, `\min(\frac{a}{2}, \frac{a^2\varepsilon}{2})` graded equal to `\frac{a}{2}` alone, and to `\min(\frac{a}{2}, a^2\varepsilon)`. None of the six seeded points has aε < 1.
  - The screen now asks for the second bound `\frac{a^2\varepsilon}{2}`, with the cap a/2 given in the prose.
  - The explanation gives the whole min, and quiz numeric 0.0005 checks the combined value. This is backlog bullet 1.
- **Grading checks in the browser.**
  - The `\epsilon` and `\varepsilon` forms both grade (ε/3, ε/5, ε/7 and a²ε/2), and `ε/3` as plain text grades too.
  - `(x-1)(x-3)` grades as `x^2 - 4x + 3`.
- **Where items moved.**
  - The flawed-line spot for "δ depends on x" is l15 quiz 3, on a static table.
  - The "flat at the top" flawed-line spot is l18 quiz 5. It is also a distractor in the l18 order proof.
  - The converse direction of the sequential criterion is homework order h-sequential-converse (d5).
- **l16 transfer.** It asks for the number of halvings (11). The implied volatility 20.09% is in the feedback and the explanation.
- **l17 hook.** It is one `place` item over a four-frame picture control, not four choice screens (backlog bullet 2).

## Validator
- 0 errors overall.
- Warnings on these files: l18 screens[8], "a problem screen without a canvas before the ladder ends" (the multi on the hypotheses of Rolle).
- Every point hint now names a highlight.

## Playthrough (--local-cdn pkgs --mobile; --why used while developing)
- l15: ok, 17 checks, quiz 5/5.
- l16: ok, 16 checks, quiz 4/4.
- l17: ok, 15 checks, quiz 4/4.
- l18: ok, 17 checks, quiz 5/5.
- l19: ok, 16 checks, quiz 4/4.
- review-4: recorded 8 of 8.
- homework-4: 9 of 9 right, 42 of 42 marks.

Code: every solution passes its hidden tests in Pyodide and in CPython, and every starter passes 0.
- l16: 13 of 13.
- l19: 12 of 12.
- homework: 11 of 11.

Layout faults fixed:
- **l15 quiz table:** a line overflowed at 390 px, so it is split in two.
- **sin(1/x) plots:** labels moved off the axis ticks.
- **l16:** the number-line "root" label was moved below. The c label was moved off the tick, and the 1/x branches use one colour.
- **l17:** curve labels moved off the axis, and the stress-test x label was shortened.
- **l18:** g's plot uses `xAxis: "bottom"`.
- **l19:** `xAxis: "bottom"` keeps the band off the tick labels, and the smooth digital curve is now blue.
- **Summary formulas:** shortened so they no longer scroll at 390 px.
- **Lower parts of long screens:** checked with a scratch scroll-and-capture script (peek.mjs) and montages.

## Numbers (each by two routes)

**l15**
- √4.1 − 2 = 0.024846 and 2 − √3.9 = 0.025158, by float and 40-digit Decimal.
- 2.025² = 4.100625, 2.024² = 4.096576, and 2.09² = 4.3681 (exact Fraction), so the gap is 0.3681.
- min(1, 0.1/5) = 0.02, and the ε/7 bound at a = 3.
- 1/x at a = 0.1: δ = 0.0005, by float and Fraction 1/2000. The worst gap is 1/0.0995 − 10 = 0.050251 (Fraction route too).
- Boxes at ε = 1: ±0.125 at a = 0.5 and ±0.02 at a = 0.2.
- Transfer: 0.03/0.6 = 0.05 (also as Fraction 1/20).

**l16**
- Midpoints and f values: 1.5 (0.875), 1.25 (−0.296875), 1.375 (0.224609), 1.3125 (−0.051514), 1.34375 (0.082611), all exact in Fraction.
- After 10 steps the interval is [1.32421875, 1.3251953125], width 1/1024.
- The root is 1.324718, by Newton and by float bisection.
- steps_needed: 20 for 10⁻⁶ (2¹⁹ < 10⁶ < 2²⁰).
- Black-Scholes prices 3.9878, 7.9656 and 11.9235, by erfc and statistics.NormalDist.
- Implied volatility 0.200867, by bisection and by Newton with vega. 11 halvings: 0.2/2¹¹ = 9.77e-5 and 0.2/2¹⁰ = 1.95e-4.
- Code test values come from the solution and from Newton (√2, and cos x = x at 0.7390851332).
- Quiz: 10 halvings for 0.001.

**l17**
- x³ − 3x at −2, −1, 0, 1, 2 gives −2, 2, 0, −2, 2.
- f'(2) = 9.

**l18**
- Quotients of abs(x) are ±1.
- g(x) = x² − 4x + 3 = (x − 1)(x − 3), with c = 2.
- x³ on [0, 3]: chord slope 9 and c = √3 = 1.732. The midpoint gives f'(1.5) = 6.75.
- Call spread: 8.00 − 2.50 = 5.50 against a bound of 5, so at least £0.50.

**l19**
- 0.9⁴³ = 0.01078 and 0.9⁴⁴ = 0.00970, also as Fraction comparisons with 1/100. ln 0.01/ln 0.9 = 43.7.
- The bump peak is ½ (AM-GM, and the code run).
- sup_gap_bump: 0.5 for n = 1, 2, 10, 100, 1000 with m = 10000.
- Coarse grids: (3, 10) = 90/181, (7, 10) = 35/74, (4, 10) = 30/61, (2, 3) = 12/25, (3, 100) = 9900/19801 and (6, 100) = 2550/5101, by Fraction and float.
- Digital at n = 10 and S = 100.1: error 100/(1 + e) = £26.89, also as 100 − 100σ(1). The smooth value is £73.11.
- Triangle area ½ · (2/n) · n = 1.
- M-test tail below 1/N.

**review-4**
- x² + x at 1, ε = 0.2: δ = 0.05, giving a gap below 0.1525. The largest δ is 0.0652 (quadratic formula, both ends).
- x² − 2 bisection: 0.25 and −0.4375.
- 1/x on [1, 4]: c = 2.
- Σ_{k≥6} 2^−k = 1/32, by closed form and sum.

**homework-4**
- 18 halvings for 10⁻⁶ on [0.1, 0.3] (2¹⁷ = 131,072 and 2¹⁸ = 262,144).
- sup of x⁴(1 − x) = 256/3125 = 0.08192, exact and by a grid of 10⁶ points.
- bs_call values 7.965567, 3.441215, 21.441372 and 4.594047, by erf and NormalDist.
- implied_vol values 0.200867, 0.1, 0.3, 0.309534, 0.271562, 0.630881 and 0.355424, by bisection and Newton, agreeing to 1e-10.
- 36 halvings to reach 1e-10 from width 5.
- Longform: 0.1/7 = 0.014286 against √9.1 − 3 = 0.016621 (86%) and 3 − √8.9 = 0.016713.

Main-session spot check (a third route, CPython): √4.1 − 2, 2 − √3.9, 0.9⁴³ and 0.9⁴⁴, 256/3125, 100/(1 + e), the three Black-Scholes prices at 10%, 20% and 30%, and the root 1.324718 all agree.

## Proof steps and their widgets
| proof | steps graded by |
|---|---|
| Continuity of 3x + 1 (l15) | expression ε/3 |
| x² at 2 | choice (factorisation), choice (why cap δ ≤ 1), expression ε/5, order with 2 distractors; numeric 0.02 and expression ε/7 in the quiz |
| δ = ε fails (trap) | numeric 0.3681 |
| δ depending on x | flawed-line choice on a table (quiz) |
| Sequential criterion | order with 2 distractors (continuity implies sequential); homework order, d5 (converse, by contrapositive) |
| sin(1/x) discontinuous; x sin(1/x) continuous | choice (generalise screen); choice (quiz) |
| 1/x edge case | expression a²ε/2 (cap in prose); numeric 0.0005 (quiz) |
| IVT by sup (l16) | choice (sup exists), choice (case f(c) < 0), choice (case f(c) > 0), order with `same` and 1 distractor |
| IVT by bisection | table bound to the number-line, numeric width, order with 1 distractor, code |
| EVT bounded (l17) | choice ×3 (pick x_n, Bolzano-Weierstrass, c ∈ [a, b]), order with 2 distractors |
| EVT attained | order with 1 distractor |
| Differentiable implies continuous (l18) | order with 1 distractor; numeric ±1 for the quotients of abs(x) |
| Interior extremum | choice ×2 (signs), order with `same` and 2 distractors (picture; converse) |
| Rolle | order with 1 distractor, multi (hypotheses used) |
| Mean value theorem | expression g(x) = x² − 4x + 3, numeric √3 (quiz); homework order with `same` and 2 distractors |
| Uniform limit continuous (l19) | order with 1 distractor, choice (why n before δ) |
| Pointwise limit "proof" | homework flawed-line choice |
| Whole proof | homework longform: x² continuous at every a with δ = min(1, ε/(2abs(a) + 1)) |

## Proposed course.json changes
None.

## Conventions
- Abbott's n ≥ N form; `\varepsilon` and `\delta` in KaTeX; £ for money.
- Code uses pure Python with math only, and `isclose` with a stated `tol` on every case.
- No random seeds.
- Proofs cite earlier results by lesson: completeness and nested intervals (l3), Bolzano-Weierstrass (l9), limit laws (l7), l15 to l17 within this level.

## Engine limits
Three bullets in `docs/BACKLOG-INBOX.md` under "Raised later (analysis level 4):":
- **Expression seeded points:** with two free symbols they never fall where aε < 1, so a two-symbol `\min` cannot be graded. Needed: author-set sample points or ranges.
- **No small multiples:** a 2 by 2 set of plane panels does not exist; `pair` holds only two. Workaround: a frames control.
- **Unlabelled bound points:** a table cell bound to a number-line point creates an unlabelled dot.

The bullet "playthrough --mobile screenshots only the viewport" was already raised at level 3 and is not repeated.

The main session saved this report from the agent's returned text (user decision, 29 Oct; see KNOWN_ISSUES).

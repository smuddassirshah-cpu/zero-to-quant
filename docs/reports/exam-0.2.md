# Topic 0.2 exam: algebra

File: `app/content/exams/topic-0.2.json` (id `topic-0.2`, 90 minutes from the topic's 180 hours by `examMinutes` in `learn.js`, pass 0.7).
Generator and checks: `scratchpad/exam-0.1-0.2/` (`gen02.py` builds the file, `check02.py` recomputes every answer by a second method, `lint.py` checks the ramp, skills and copy rules).

## Shape

26 items, interleaving the three courses (equations, functions, quadratics). Pitched at GCSE Higher; the formula item allows a calculator.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 5 | 19% | 20% |
| 3 | 13 | 50% | 50% |
| 4 | 5 | 19% | 20% |
| 5 | 3 | 12% | 10% |

Widgets: 8 numeric, 4 expression, 4 choice, 2 multi, 2 drag-point (plane), 2 table, 1 manipulate, 1 tap-regions (number line), 1 order, 1 longform (10-point rubric, full model answer).

| # | id | d | skills | widget / canvas |
|---|---|---|---|---|
| 1 | e-expand-two | 2 | eq-expressions | expression |
| 2 | e-bracket-equation | 2 | eq-linear | numeric |
| 3 | e-gradient | 2 | fn-lines | numeric |
| 4 | e-evaluate | 2 | fn-rules | numeric |
| 5 | e-factorise | 2 | quad-factor | choice |
| 6 | e-clear-fractions | 3 | eq-linear | manipulate |
| 7 | e-whole-numbers | 3 | eq-inequalities | tap-regions on number-line |
| 8 | e-option-prices | 3 | eq-simultaneous, eq-forming | numeric |
| 9 | e-subject | 3 | eq-forming | expression |
| 10 | e-cubic-line | 3 | fn-graphs | choice on plane |
| 11 | e-shifted-peak | 3 | fn-transform | drag-point on plane |
| 12 | e-composite | 3 | fn-compose | expression |
| 13 | e-inverse | 3 | fn-compose | choice |
| 14 | e-two-roots | 3 | quad-solve, quad-factor | multi |
| 15 | e-complete-table | 3 | quad-square | table |
| 16 | e-vertex | 3 | quad-graph, quad-square | drag-point on plane |
| 17 | e-one-root | 3 | quad-solve | numeric |
| 18 | e-floor-area | 3 | quad-model, eq-forming | numeric |
| 19 | e-perpendicular | 4 | fn-lines | expression |
| 20 | e-formula | 4 | quad-solve | numeric |
| 21 | e-quad-inequality | 4 | quad-graph, eq-inequalities | choice |
| 22 | e-fg-equation | 4 | fn-compose, fn-rules, quad-solve | multi |
| 23 | e-odd-squares | 4 | eq-expressions, quad-factor | order |
| 24 | e-tangent-line | 5 | eq-simultaneous, quad-solve | table |
| 25 | e-lattice-region | 5 | fn-graphs, eq-inequalities, quad-graph | numeric on plane |
| 26 | e-spread-model | 5 | quad-model, quad-square, eq-forming | longform |

Skills: all 15 of the topic are covered: eq-expressions 2, eq-linear 2, eq-inequalities 3, eq-simultaneous 2, eq-forming 4, fn-rules 2, fn-lines 2, fn-graphs 2, fn-transform 1, fn-compose 3, quad-factor 3, quad-solve 5, quad-square 3, quad-graph 3, quad-model 2.

Quant framing: call and put prices from two orders, the average price after a second buy, a trading floor's width, a market maker's spread and daily profit.

Fresh against the courses: searched as for 0.1. Replaced near copies: $x^2 - 2x - 15$ (factorised in quadratics l2) became $x^2 - 4x - 21$; $x^2 - x - 12 > 0$ (quadratics review 3) became $x^2 + 2x - 15 < 0$; $f(x + 4)$ (functions l14) became $f(x + 3) - 2$; making $r$ the subject of $I = Prt$ (equations l13) became making $q$ the subject of an average price. The stage exam's items ($f(g(3))$, $f^{-1}(7)$, $b$ in a completed square) are not reused.

## Numbers computed twice

`gen02.py` computes with `Fraction` and the quadratic formula; `check02.py` recomputes by other means: bisection (10.5), a 0.1 grid search (2.8), brute force over pence (call £6), scans over whole numbers and quarters ($n$ from −3 to 3; $k = 8$; width 8 m; $k = -5.25$), grid maximum and minimum searches (peak $(-1, 3)$, turning point $(-1, -9)$, spread 7.5p with profit £25 and break-even at 5p and 10p), the trigonometric form of the cubic (roots −1.532, −0.347, 1.879, so 3 solutions), Newton's method (2.7656, which rounds to 2.77), evaluation at six sample points for every expression answer and identity, a column count for the lattice region (8 points; 2 with strict signs), and $(2n + 3)^2 - (2n + 1)^2 \bmod 8 = 0$ for 1,000 values of $n$. Checks quoted in explanations were recomputed: £100 to £115, $f(2) = \tfrac{2}{5}$, $g(f(1)) = 6$, $7^2 - 5^2 = 24$, the other root −1.27. No numeric wrong value lies within tolerance of its answer.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors and no warnings for this file.
- Copy lint (`lint.py`): no `!`, no dashes, no sentence of 20 words or more (four long sentences were split), no American spellings.
- `playthrough.mjs --exam topic-0.2 --local-cdn <pkgs>`: 26 of 26, passed, desktop and `--mobile` (the expression items need the local MathLive and Compute Engine).
- Screenshots reviewed (`scratchpad/exam-0.1-0.2/shots`). Fixes made from them: the cubic's label moved from above the frame to the left branch (`labelAt: -2.1`); the whole-number line narrowed from −6..6 to −5..5 so its dots are larger on a phone; multi options use `\dfrac`.

## Engine notes

- The number line's dots stay small on a 390 px phone (item 7, 11 tappable dots), so the tap targets are tight. Workaround: the shortest range that still holds the trap values −4 and 4.
- On item 25, `labelSide: "below"` with `labelAt` did not move the straight line's label off the parabola; it still touches the curve, but it is legible.

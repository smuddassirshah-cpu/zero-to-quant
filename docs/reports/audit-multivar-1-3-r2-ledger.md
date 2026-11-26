# Claim ledger: multivar levels 1 to 3, round 2 (multivar-1-3-r2)

Blind read at commit beaf4205. One row per definition, rule, key, option, slip, hint, feedback line, explanation, summary line, model paragraph, rubric line, code test and mutant. Rows: 3563. Verdicts: correct 3548, imprecise 13, wrong 2. No row is `unverified`.

Sources: Apostol, *Calculus* vol. II (2nd ed.), chapters 8 and 9; Marsden and Tromba, *Vector Calculus*, chapters 2 and 3; Boyd and Vandenberghe, *Convex Optimization*, 4.4.1, 5.6.3, 9.3, A.4.1; Hull, *Options, Futures and Other Derivatives*, ch. 19. "concepts-r2 script" is `docs/reports/multivar-L1-3-concepts-r2.py`. Canvas-only strings (captions, plotted expressions) were read with their screens and carry no separate row unless they state a value used in grading.

## Basis key

Rows with verdict `correct` cite one of these; other rows give their basis in full.

- **B1**: Apostol II 8.1-8.2 and Marsden-Tromba 2.1 (scalar fields, level sets); arithmetic redone by hand and in concepts-r2 script (l1 checks)
- **B2**: derivation: x^2+y^2=c solved for y; circle of radius sqrt(c) (Marsden-Tromba 2.1)
- **B3**: derivation: 300 dA + 200 dB = 0 gives dB = -1.5 dA; concepts-r2 script l1 s8
- **B4**: Apostol II 8.6 (partial derivatives as one-variable derivatives) and Marsden-Tromba 2.3; finite-difference check in concepts-r2 script (l2 checks)
- **B5**: limit definition, Apostol II 8.6; algebra redone
- **B6**: Hull ch. 19 (delta, vega); table reproduced by Black-Scholes at r = 0 in concepts-r2 script
- **B7**: Apostol II 8.23 and Marsden-Tromba 3.1 (second and mixed partials); finite-difference Hessians in concepts-r2 script (l3 checks)
- **B8**: power rule on x^m y^n, derivation redone; Clairaut hypothesis per Apostol II Theorem 8.12 (8.23) and Marsden-Tromba 3.1 Theorem 1
- **B9**: Hull ch. 19 (gamma); vanna = d delta/d sigma; delta table reproduced by Black-Scholes at r = 0 in concepts-r2 script
- **B10**: Apostol II 8.15 and Marsden-Tromba 2.5 (chain rule along a path, f with continuous partials); values redone in concepts-r2 script (l4 checks)
- **B11**: standard two-step proof of the chain rule, Apostol II 8.15 (needs differentiability; continuity of partials is sufficient, 8.13)
- **B12**: dV/dt = delta dS/dt + vega dsigma/dt (Hull ch. 19), theta ignored as stated; arithmetic in concepts-r2 script
- **B13**: template algebra checked symbolically by hand: key, each slip and its `where`/`when` guard; grade-all draws at 2 seeds
- **B14**: template algebra checked by hand (power, chain and log rules, Apostol II 8.6); grade-all draws at 2 seeds
- **B15**: template algebra checked by hand (second and mixed partials of monomials); grade-all draws at 2 seeds
- **B16**: level 1 results (Apostol II 8.6, 8.15, 8.23); values recomputed in concepts-r2 script
- **B17**: level 1 results (Apostol II 8.6, 8.15, 8.23); values and the long-form model recomputed in concepts-r2 script
- **B18**: level 1 results (Apostol II 8.6, 8.15, 8.23); each part recomputed in concepts-r2 script
- **B19**: Apostol II 8.10 and 8.17, Marsden-Tromba 2.6 (gradient, steepest ascent, normal to level sets); concepts-r2 script l5 checks and Monte Carlo over 200,000 directions
- **B20**: derivation from the chain rule on a level curve, Apostol II 8.17
- **B21**: gradient of w^T Sigma w is 2 Sigma w (Boyd-Vandenberghe A.4.1); numbers in concepts-r2 script
- **B22**: Apostol II 8.6 and 8.10 (directional derivative = grad f . u for differentiable f), Marsden-Tromba 2.6 Theorem 12-13; concepts-r2 script l6 checks
- **B23**: cos(theta - alpha) identity; Cauchy-Schwarz, Marsden-Tromba 2.6 Theorem 13
- **B24**: Apostol II 8.11 and 8.17, Marsden-Tromba 2.3 (tangent plane, linear approximation), 3.2 (Taylor remainder); concepts-r2 script l7 checks
- **B25**: Boyd-Vandenberghe 9.3 (gradient method, fixed step on a quadratic: factors 1 - s*lambda_i); step-size sweeps and exact runs in concepts-r2 script; code lines swept in Pyodide (audit, code sweep)
- **B26**: run in Pyodide 0.27.7 through grade-all --code and the audit sweep; expected values recomputed in concepts-r2 script
- **B27**: audit code sweep: natural codings of the named mistake submitted in Pyodide 0.27.7 (see the table in the audit)
- **B28**: least squares by gradient descent on the mean squared error, Boyd-Vandenberghe 9.3; 3,000-step results compared with numpy.polyfit in concepts-r2 script; mistakes submitted in Pyodide 0.27.7 (audit, code sweep)
- **B29**: level 2 results (Apostol II 8.10, 8.17; Boyd-Vandenberghe 9.3); values recomputed in concepts-r2 script
- **B30**: level 2 results (Apostol II 8.10; Boyd-Vandenberghe 9.3); values recomputed in concepts-r2 script; code item swept in Pyodide (audit, code sweep)
- **B31**: level 2 results (Apostol II 8.10, 8.17; Boyd-Vandenberghe 9.3); each part recomputed in concepts-r2 script
- **B32**: Apostol II 9.9 and Marsden-Tromba 3.3 (stationary points; first-derivative condition); every point checked by finite-difference gradient in concepts-r2 script
- **B33**: completing the square; global minimum shown directly
- **B34**: Apostol II 9.10-9.12 (Theorem 9.7, second-derivative test with continuous second partials) and Marsden-Tromba 3.3 Theorem 6; every stated D and type checked by Hessian and by Monte Carlo sampling of f in concepts-r2 script
- **B35**: second-order Taylor formula (Apostol II 9.10) and completing the square, as in Marsden-Tromba 3.3
- **B36**: Apostol II 9.14 and Marsden-Tromba 3.4 Theorem 8 (Lagrange multiplier, needs grad g != 0), Apostol II 9.16 (extreme values on compact sets), Boyd-Vandenberghe 5.6.3 (multiplier as sensitivity); brute force on the constraint curve in concepts-r2 script
- **B37**: Boyd-Vandenberghe 4.4.1 (Markowitz portfolio, variance w^T Sigma w) and two-asset derivation redone; all figures and the general claims by Monte Carlo over 100,000 pairs in concepts-r2 script
- **B38**: level 3 results (Apostol II 9.9-9.14; Boyd-Vandenberghe 4.4.1); values recomputed in concepts-r2 script
- **B39**: level 3 results (Apostol II 9.12, 9.14; Boyd-Vandenberghe 4.4.1); values and the long-form model recomputed in concepts-r2 script
- **B40**: level 3 results (Apostol II 9.12, 9.14; Boyd-Vandenberghe 4.4.1, 5.6.3); each part recomputed in concepts-r2 script

## l1-two-inputs

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Read a function of two variables as a surface and as a contour map. | correct | B1 |
| `objectives[1]` | Explain why close contours mean a steep surface | correct | B1 |
| `screens[0].prose` | Until now a function took one number. This one takes two: $f(x, y) = x^2 + y^2$. Each cell is one input pair $(x, y)$. Tap a cell to see its value;... | correct | B1 |
| `screens[0].question` | Shade every cell where $f$ takes its largest value. | correct | B1 |
| `screens[0].widget.answer` | r1c1, r1c5, r5c1, r5c5 | correct | B1 |
| `screens[0].hints[0]` | Which inputs make $x^2$ as big as it can be in this table? | correct | B1 |
| `screens[0].hints[1]` | The largest $x^2$ comes from $x = 2$ or $x = -2$. The same goes for $y$. | correct | B1 |
| `screens[0].hints[2]` | Both inputs must be $\pm 2$. That is four corners, each giving $4 + 4 = 8$. | correct | B1 |
| `screens[0].feedback.correct` | All four corners give $4 + 4 = 8$. | correct | B1 |
| `screens[0].feedback.generic` | Not quite right. Work out $x^2 + y^2$ for the corners and the middle, and compare. | correct | B1 |
| `screens[0].feedback.byKey.one-corner` | $(2, 2)$ gives 8, but so does $(-2, -2)$. Squaring wipes out the sign, so all four corners give 8. | correct | B1 |
| `screens[0].feedback.byKey.r3c3` | The centre $(0, 0)$ gives $0 + 0 = 0$, the smallest value, not the largest. | correct | B1 |
| `screens[0].explain.text` | You needed both $x^2$ and $y^2$ as large as possible, so both inputs are $\pm 2$. That happens at the four corners, where $f = 8$. A function of tw... | correct | B1 |
| `screens[1].prose` | Same function, $f(x, y) = x^2 + y^2$. Now look for one value that appears in many places. | correct | B1 |
| `screens[1].question` | Shade every cell where $f(x, y) = 5$. | correct | B1 |
| `screens[1].widget.answer` | r1c2, r1c4, r2c1, r2c5, r4c1, r4c5, r5c2, r5c4 | correct | B1 |
| `screens[1].hints[0]` | Which two squares add to 5? | correct | B1 |
| `screens[1].hints[1]` | $5 = 1 + 4$. So one input is $\pm 1$ and the other is $\pm 2$. | correct | B1 |
| `screens[1].hints[2]` | Try $x = \pm 1$ with $y = \pm 2$, then $x = \pm 2$ with $y = \pm 1$. That gives eight cells. | correct | B1 |
| `screens[1].feedback.correct` | Eight cells, and they form a ring round the centre. | correct | B1 |
| `screens[1].feedback.generic` | Not quite right. You need $x^2 + y^2 = 5$, so the squares are 1 and 4 in some order. | correct | B1 |
| `screens[1].feedback.byKey.positive-only` | You found $(1, 2)$ and $(2, 1)$. Negative inputs square to the same values, so $(-1, 2)$, $(1, -2)$ and the rest count too. | correct | B1 |
| `screens[1].feedback.byKey.half` | You stopped at the top half. Negative $y$ squares to the same values, so the bottom rows hold four more. | correct | B1 |
| `screens[1].explain.text` | You shaded eight cells, from $(1, 2)$ round to $(2, -1)$ and back. They sit on a ring about the centre, at distance $\sqrt{5}$ from it. Every input... | correct | B1 |
| `screens[2].prose` | The table only showed whole-number inputs. Here every point of the plane is an input $(x, y)$. The blue curve marks every input with $x^2 + y^2 = c... | correct | B1 |
| `screens[2].question` | Set $c = 4$. The curve is a circle centred on $(0, 0)$. What is its radius? | correct | B1 |
| `screens[2].widget.options[0]` | option two (key): 2 | correct | B1 |
| `screens[2].widget.options[1]` | option four: 4 | correct | B1 |
| `screens[2].widget.options[1].why` | You read the level $c$ as the radius. Points on the circle have $x^2 + y^2 = 4$, so the radius is $\sqrt{4} = 2$. | correct | B1 |
| `screens[2].widget.options[2]` | option sixteen: 16 | correct | B1 |
| `screens[2].widget.options[2].why` | You squared the level. The radius $r$ satisfies $r^2 = c$, so $r = \sqrt{c}$. | correct | B1 |
| `screens[2].hints[0]` | Where does the circle cross the positive $x$-axis when $c = 4$? | correct | B1 |
| `screens[2].feedback.correct` | The circle passes through $(2, 0)$, so its radius is 2. | correct | B1 |
| `screens[2].feedback.generic` | Not quite right. Find where the curve crosses the $x$-axis, where $y = 0$. | correct | B1 |
| `screens[2].explain.text` | At $c = 4$ the curve passes through $(2, 0)$, since $2^2 + 0^2 = 4$. Every point on it is at distance $\sqrt{4} = 2$ from the origin. Raising $c$ g... | correct | B1 |
| `screens[3].prose` | Each curve where $f$ takes one value is a **contour**. Drawing several gives a **contour map**, like height lines on a hiking map. Here are the con... | correct | B1 |
| `screens[3].question` | You walk from A $= (2, 0)$ to B $= (3, 0)$. By how much does $f$ rise? | correct | B1 |
| `screens[3].widget.answer` | 5 | correct | B1 |
| `screens[3].widget.accept` | 5: from the contour $f = 4$ to the contour $f = 9$. | correct | B1 |
| `screens[3].widget.wrong[0]` | slip distance = 1 | correct | B1 |
| `screens[3].widget.wrong[1]` | slip end-value = 9 | correct | B1 |
| `screens[3].widget.wrong[2]` | slip start-value = 4 | correct | B1 |
| `screens[3].hints[0]` | Which contour passes through A, and which through B? | correct | B1 |
| `screens[3].hints[1]` | A is on the contour labelled 4. B is on the contour labelled 9. | correct | B1 |
| `screens[3].hints[2]` | The rise is the change in the contour labels: $9 - 4$. | correct | B1 |
| `screens[3].feedback.correct` | From the contour 4 to the contour 9: a rise of 5. | correct | B1 |
| `screens[3].feedback.generic` | Not quite right. Read the label of the contour through each point, then subtract. | correct | B1 |
| `screens[3].feedback.byKey.distance` | 1 is the distance from A to B across the page. The rise is the change in the output: $9 - 4$. | correct | B1 |
| `screens[3].feedback.byKey.end-value` | 9 is the value at B. The rise is the value at B minus the value at A. | correct | B1 |
| `screens[3].feedback.byKey.start-value` | 4 is the value at A. Subtract it from the value at B. | correct | B1 |
| `screens[3].explain.text` | A sits on the contour $f = 4$ and B on the contour $f = 9$. So $f$ rises by 5 over a walk of length 1. Earlier, from $(1, 0)$ to $(2, 0)$, it rose ... | correct | B1 |
| `screens[4].prose` | This map shows nine contours of $f(x, y) = x^2 + y^2$: $f = 1, 2, 3, \ldots, 9$ from the centre out. Two walkers each step 0.5 to the right, one fr... | correct | B1 |
| `screens[4].question` | Tap the walker whose step makes $f$ rise more. | correct | B1 |
| `screens[4].widget.answer` | B | correct | B1 |
| `screens[4].hints[0]` | Count the contours each arrow crosses. Each crossing is a rise of 1. | correct | B1 |
| `screens[4].hints[1]` | A's arrow crosses one contour. Count B's. | correct | B1 |
| `screens[4].hints[2]` | B's arrow crosses the contours 7, 8 and 9. A's crosses only the contour 1. | correct | B1 |
| `screens[4].feedback.correct` | B's step crosses three contours; A's crosses one. | correct | B1 |
| `screens[4].feedback.generic` | Not quite right. Count how many contours each arrow crosses. | correct | B1 |
| `screens[4].feedback.byKey.A` | Near A the contours are far apart, so the step crosses just one. Wide gaps mean the surface is gentle there. | correct | B1 |
| `screens[4].explain.text` | A's step takes $f$ from 0.25 to 1, a rise of 0.75. B's takes it from 6.25 to 9, a rise of 2.75. Where contours crowd together, $f$ changes fast: th... | correct | B1 |
| `screens[5].prose` | A new function, $f(x, y) = y - x^2$. Its contours are the curves $y = x^2 + c$. Three walks are drawn: A goes up, B goes right, and C follows a curve. | correct | B1 |
| `screens[5].question` | Along which walk does $f$ stay the same? | correct | B1 |
| `screens[5].widget.options[0]` | option a: Walk A | correct | B1 |
| `screens[5].widget.options[0].why` | Walk A crosses the contours 0, 1 and 2, so $f$ rises from 0 to 2. | correct | B1 |
| `screens[5].widget.options[1]` | option b: Walk B | correct | B1 |
| `screens[5].widget.options[1].why` | Walk B starts on the contour 1 and ends below the contour $-1$: $f(1.5, 1) = 1 - 2.25 = -1.25$. | correct | B1 |
| `screens[5].widget.options[2]` | option c (key): Walk C | correct | B1 |
| `screens[5].hints[0]` | A walk keeps $f$ fixed only if it never crosses a contour. | correct | B1 |
| `screens[5].hints[1]` | Walk C hugs one curve. Which contour is it next to? | correct | B1 |
| `screens[5].hints[2]` | Walk C runs along $y = x^2 + 1$, the contour $f = 1$, so $f$ stays 1. | correct | B1 |
| `screens[5].feedback.correct` | Walk C runs along the contour $f = 1$ and never crosses another. | correct | B1 |
| `screens[5].feedback.generic` | Not quite right. Look for the walk that crosses no contour. | correct | B1 |
| `screens[5].explain.text` | Walk C follows the contour $f = 1$, so $f$ never changes on it. Walks A and B cut across contours, so $f$ changes. Moving along a contour is the on... | correct | B1 |
| `screens[6].prose` | Same map of $f(x, y) = y - x^2$. The point P $= (1, 1)$ sits on the curve labelled $f = 0$. | correct | B1 |
| `screens[6].question` | What is $f$ at P? | correct | B1 |
| `screens[6].widget.options[0]` | option zero (key): 0 | correct | B1 |
| `screens[6].widget.options[1]` | option height: 1 | correct | B1 |
| `screens[6].widget.options[1].why` | You read the curve as the graph $y = x^2$ and took its height at $x = 1$. On a contour map the height on the page is the input $y$. The output is t... | correct | B1 |
| `screens[6].widget.options[2]` | option sum: 2 | correct | B1 |
| `screens[6].widget.options[2].why` | You added the coordinates. Put them into the formula: $f(1, 1) = 1 - 1^2$. | correct | B1 |
| `screens[6].hints[0]` | On a contour map, what does the vertical position of a point tell you? | correct | B1 |
| `screens[6].hints[1]` | The curve through P carries a label. That label is the output. | correct | B1 |
| `screens[6].hints[2]` | Check with the formula: $f(1, 1) = 1 - 1^2 = 0$. | correct | B1 |
| `screens[6].feedback.correct` | P is on the contour $f = 0$, and $1 - 1^2 = 0$. | correct | B1 |
| `screens[6].feedback.generic` | Not quite right. The output is the contour's label, not a height on the page. | correct | B1 |
| `screens[6].feedback.byKey.height` | You read the curve as a graph of $y$ against $x$. Its height at P is the input $y = 1$. The output is the label: $f = 0$. | correct | B1 |
| `screens[6].explain.text` | Both axes of a contour map are inputs, so P's height on the page is $y = 1$. The output lives in the label: P is on the contour $f = 0$. The formul... | correct | B1 |
| `screens[7].prose` | A function of two variables takes a pair $(x, y)$ to one number $f(x, y)$. Its contour at level $c$ is every input with $f(x, y) = c$. For $f = x^2... | correct | B2 |
| `screens[7].question` | Put the lines in order. | correct | B2 |
| `screens[7].widget.lines[0]` | line set: $x^2 + y^2 = c$, the contour: every input whose output is $c$ | correct | B2 |
| `screens[7].widget.lines[1]` | line sub: $y^2 = c - x^2$, subtract $x^2$ from both sides | correct | B2 |
| `screens[7].widget.lines[2]` | line root: $y = \pm\sqrt{c - x^2}$, square roots: one half above the $x$-axis, one below | correct | B2 |
| `screens[7].widget.lines[3]` | line range: $-\sqrt{c} \le x \le \sqrt{c}$, the root needs $c - x^2 \ge 0$, so the radius is $\sqrt{c}$ | correct | B2 |
| `screens[7].widget.answer` | set, sub, root, range | correct | B2 |
| `screens[7].hints[0]` | Start from the equation that defines the contour. | correct | B2 |
| `screens[7].hints[1]` | Make $y^2$ the subject before taking any square root. | correct | B2 |
| `screens[7].hints[2]` | Contour, subtract $x^2$, take square roots, then ask where the root exists. | correct | B2 |
| `screens[7].feedback.correct` | Two halves, $y = \pm\sqrt{c - x^2}$, joined at $x = \pm\sqrt{c}$. | correct | B2 |
| `screens[7].feedback.generic` | Not quite right. Begin with $x^2 + y^2 = c$ and solve it for $y$ one step at a time. | correct | B2 |
| `screens[7].feedback.byKey.root` | You can take the square root only once $y^2$ is alone on one side. | correct | B2 |
| `screens[7].feedback.byKey.range` | The limit on $x$ comes from the square root, so it comes last. | correct | B2 |
| `screens[7].explain.text` | Solving $x^2 + y^2 = c$ for $y$ gives two halves, $\pm\sqrt{c - x^2}$. They exist only for $\|x\| \le \sqrt{c}$, and meet at the ends. That is the ... | correct | B2 |
| `screens[8].prose` | You hold 300 shares of A and 200 shares of B. If A moves by $\Delta A$ and B by $\Delta B$ pounds, your P&L is $300\,\Delta A + 200\,\Delta B$. The... | correct | B3 |
| `screens[8].question` | A rises by £2.00. What change in B's price keeps your P&L at exactly £0? | correct | B3 |
| `screens[8].widget.answer` | -3 | correct | B3 |
| `screens[8].widget.accept` | $-3$: B must fall £3.00, since $300 \times 2 + 200 \times (-3) = 0$. | correct | B3 |
| `screens[8].widget.wrong[0]` | slip same = -2 | correct | B3 |
| `screens[8].widget.wrong[1]` | slip ratio-flipped = -1.3333 | correct | B3 |
| `screens[8].widget.wrong[2]` | slip sign = 3 | correct | B3 |
| `screens[8].widget.wrong[3]` | slip pnl-of-a = -600 | correct | B3 |
| `screens[8].hints[0]` | Stay on the £0 contour. Where does it cross $\Delta A = 2$? | correct | B3 |
| `screens[8].hints[1]` | On the £0 line, $300\,\Delta A + 200\,\Delta B = 0$. | correct | B3 |
| `screens[8].hints[2]` | $600 + 200\,\Delta B = 0$, so $\Delta B = -3$. | correct | B3 |
| `screens[8].feedback.correct` | B must fall £3.00: $600 - 600 = 0$. | correct | B3 |
| `screens[8].feedback.generic` | Not quite right. Stay on the £0 contour: solve $300 \times 2 + 200\,\Delta B = 0$. | correct | B3 |
| `screens[8].feedback.byKey.same` | A fall of £2.00 in B loses only £400, against A's £600 gain. You hold fewer B shares, so B must move further. | correct | B3 |
| `screens[8].feedback.byKey.ratio-flipped` | You flipped the ratio. Each £1 in B is worth 200, each £1 in A is worth 300, so $\Delta B = -\tfrac{300}{200} \times 2$. | correct | B3 |
| `screens[8].feedback.byKey.sign` | A rise in B would add to the gain. To cancel A's £600, B must fall. | correct | B3 |
| `screens[8].feedback.byKey.pnl-of-a` | £600 is the gain on A. The question asks for B's price change, in pounds per share. | correct | B3 |
| `screens[8].explain.text` | Along the £0 contour, $300\,\Delta A + 200\,\Delta B = 0$, so $\Delta B = -1.5\,\Delta A$. With $\Delta A = 2$ that is $-3$. Every point on that li... | correct | B3 |
| `summary.ideas[0]` | A function of two variables takes a pair $(x, y)$ to one number $f(x, y)$. Think of it as a height above each point of the plane. | correct | B1 |
| `summary.ideas[1]` | A contour is every input with the same output. On a contour map both axes are inputs and the labels are outputs. | correct | B1 |
| `summary.ideas[2]` | Walking along a contour keeps $f$ fixed. Where contours crowd together, $f$ changes fast: the surface is steep. | correct | B1 |
| `summary.formula.name` | Contour at level $c$ | correct | B1 |
| `summary.formula.tex` | \{(x, y) : f(x, y) = c\} | correct | B1 |
| `summary.formula.note` | A set of inputs, not a graph of $y$ against $x$. | correct | B1 |
| `summary.trap` | A contour can look like the graph $y = x^2$. Its height on the page is the input $y$; the output is its label. | correct | B1 |
| `quiz[0].prose` | Take $f(x, y) = x^2 + y^2$ again. | correct | B1 |
| `quiz[0].question` | What does the contour $f = -1$ look like? | correct | B1 |
| `quiz[0].widget.options[0]` | option empty (key): It has no points at all | correct | B1 |
| `quiz[0].widget.options[1]` | option circle: A circle of radius 1 | correct | B1 |
| `quiz[0].widget.options[1].why` | You dropped the minus sign. $x^2 + y^2$ is never negative, so no input gives $-1$. | correct | B1 |
| `quiz[0].widget.options[2]` | option origin: The single point $(0, 0)$ | correct | B1 |
| `quiz[0].widget.options[2].why` | That is the contour $f = 0$, the lowest level $f$ reaches. | correct | B1 |
| `quiz[0].feedback.correct` | A sum of squares is never negative, so nothing reaches $-1$. | correct | B1 |
| `quiz[0].feedback.generic` | Not quite right. Can $x^2 + y^2$ ever be negative? | correct | B1 |
| `quiz[0].explain.text` | Squares are at least 0, so $x^2 + y^2 \ge 0$ for every input. The contour $f = 0$ is the single point $(0, 0)$, and every negative level is empty. | correct | B1 |
| `quiz[1].prose` | Take $f(x, y) = x^2 + y^2$. | correct | B1 |
| `quiz[1].question` | Which level $c$ is the contour that passes through $(3, 4)$? | correct | B1 |
| `quiz[1].widget.answer` | 25 | correct | B1 |
| `quiz[1].widget.accept` | 25, since $3^2 + 4^2 = 25$. | correct | B1 |
| `quiz[1].widget.wrong[0]` | slip sum = 7 | correct | B1 |
| `quiz[1].widget.wrong[1]` | slip radius = 5 | correct | B1 |
| `quiz[1].feedback.correct` | $9 + 16 = 25$. | correct | B1 |
| `quiz[1].feedback.generic` | Not quite right. The level is the output at that point: $f(3, 4)$. | correct | B1 |
| `quiz[1].feedback.byKey.sum` | You added the inputs. Square each one first: $9 + 16$. | correct | B1 |
| `quiz[1].feedback.byKey.radius` | 5 is the radius of that circle. The level is $5^2 = 25$. | correct | B1 |
| `quiz[1].explain.text` | The contour through a point is the one whose level equals the output there. $f(3, 4) = 9 + 16 = 25$. It is the circle of radius $\sqrt{25} = 5$. | correct | B1 |
| `quiz[2].prose` | Take $f(x, y) = 2x - y$. | correct | B1 |
| `quiz[2].question` | Which point lies on the contour $f = 3$? | correct | B1 |
| `quiz[2].widget.options[0]` | option a (key): $(2, 1)$ | correct | B1 |
| `quiz[2].widget.options[1]` | option swap: $(1, 2)$ | correct | B1 |
| `quiz[2].widget.options[1].why` | You swapped the inputs. $(1, 2)$ gives $2 - 2 = 0$. | correct | B1 |
| `quiz[2].widget.options[2]` | option x-only: $(3, 0)$ | correct | B1 |
| `quiz[2].widget.options[2].why` | You used $x = 3$ alone. $f(3, 0) = 6$. | correct | B1 |
| `quiz[2].widget.options[3]` | option sum: $(0, 3)$ | correct | B1 |
| `quiz[2].widget.options[3].why` | You looked for $x + y = 3$. $f(0, 3) = -3$. | correct | B1 |
| `quiz[2].feedback.correct` | $2 \times 2 - 1 = 3$. | correct | B1 |
| `quiz[2].feedback.generic` | Not quite right. Work out $2x - y$ for each point. | correct | B1 |
| `quiz[2].explain.text` | A point is on the contour $f = 3$ when its output is 3. $f(2, 1) = 4 - 1 = 3$. The others give 0, 6 and $-3$. | correct | B1 |
| `quiz[3].prose` | A contour map of a book's P&L, against two share prices, has a line every £100. In region R the lines are 2 mm apart. In region S they are 8 mm apart. | correct | B1 |
| `quiz[3].question` | Where does the P&L change faster as prices move? | correct | B1 |
| `quiz[3].widget.options[0]` | option r (key): In R, where the lines are close | correct | B1 |
| `quiz[3].widget.options[1]` | option s: In S, where the lines are far apart | correct | B1 |
| `quiz[3].widget.options[1].why` | You read wide gaps as big changes. Each gap is the same £100, so a wide gap means a slow change. | correct | B1 |
| `quiz[3].widget.options[2]` | option same: The same everywhere, since every gap is £100 | correct | B1 |
| `quiz[3].widget.options[2].why` | Each gap is £100, but the distance differs. In R you cross four lines in 8 mm; in S, one. | correct | B1 |
| `quiz[3].feedback.correct` | Close contours mean £100 changes over short moves. | correct | B1 |
| `quiz[3].feedback.generic` | Not quite right. Count how many £100 lines a short move crosses in each region. | correct | B1 |
| `quiz[3].explain.text` | In 8 mm you cross four £100 lines in R and only one in S. So the P&L changes four times as fast in R. Crowded contours mean steep. | correct | B1 |

## l2-slicing

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Compute partial derivatives by holding one variable fixed. | correct | B4 |
| `objectives[1]` | Read a partial derivative as the slope of a slice | correct | B4 |
| `screens[0].prose` | Take $f(x, y) = x^2 y + 3y$. Fix $y = 2$ and walk along that line. The height you meet is $f(x, 2) = 2x^2 + 6$, an ordinary function of $x$. The bo... | correct | B4 |
| `screens[0].question` | What is the slope of the slice $f(x, 2)$ at $x = 1$? | correct | B4 |
| `screens[0].widget.answer` | 4 | correct | B4 |
| `screens[0].widget.accept` | 4: the derivative of $2x^2 + 6$ is $4x$, which is 4 at $x = 1$. | correct | B4 |
| `screens[0].widget.wrong[0]` | slip height = 8 | correct | B4 |
| `screens[0].widget.wrong[1]` | slip lost-factor = 2 | correct | B4 |
| `screens[0].widget.wrong[2]` | slip kept-6 = 10 | correct | B4 |
| `screens[0].hints[0]` | The slice is a function of $x$ alone. Differentiate it as you always have. | correct | B4 |
| `screens[0].hints[1]` | Differentiate $2x^2 + 6$ term by term. What does the 6 contribute? | correct | B4 |
| `screens[0].hints[2]` | $\frac{d}{dx}(2x^2 + 6) = 4x$. Put in $x = 1$. | correct | B4 |
| `screens[0].feedback.correct` | $\frac{d}{dx}(2x^2 + 6) = 4x$, which is 4 at $x = 1$. | correct | B4 |
| `screens[0].feedback.generic` | Not quite right. Differentiate $2x^2 + 6$ with respect to $x$, then put in $x = 1$. | correct | B4 |
| `screens[0].feedback.byKey.height` | 8 is the height of the slice at $x = 1$: $2 + 6$. The slope is its derivative. | correct | B4 |
| `screens[0].feedback.byKey.lost-factor` | You differentiated $x^2$ to $2x$ but lost the factor 2 in front. The slice is $2x^2$, so the slope is $4x$. | correct | B4 |
| `screens[0].feedback.byKey.kept-6` | You kept the 6. It is a constant, so its slope is 0. | correct | B4 |
| `screens[0].explain.text` | Once $y$ is fixed at 2, $f$ is the one-variable function $2x^2 + 6$. Its derivative is $4x$, so the slope at $x = 1$ is 4. The 6 came from $3y$ and... | correct | B4 |
| `screens[1].prose` | Same $f(x, y) = x^2 y + 3y$. The slider moves the slice to $y = y_0$. The bottom graph shows $f$ along it, with the tangent at $x = 1$ and its slope. | correct | B4 |
| `screens[1].question` | How does the slope at $x = 1$ depend on $y_0$? | correct | B4 |
| `screens[1].widget.options[0]` | option twice (key): It equals $2y_0$ | correct | B4 |
| `screens[1].widget.options[1]` | option fixed: It stays at 2 whatever $y_0$ is | correct | B4 |
| `screens[1].widget.options[1].why` | Watch the slope label, not the curve's shape. At $y_0 = 2$ it reads 4, at $y_0 = 0.5$ it reads 1. | correct | B4 |
| `screens[1].widget.options[2]` | option plus-three: It equals $2y_0 + 3$ | correct | B4 |
| `screens[1].widget.options[2].why` | The $3y$ term lifts the whole slice by $3y_0$ but does not tilt it. At $y_0 = 1$ the slope is 2, not 5. | correct | B4 |
| `screens[1].widget.options[3]` | option square: It equals $y_0^2$ | correct | B4 |
| `screens[1].widget.options[3].why` | Check $y_0 = 1$ and $y_0 = 2$: the slope goes from 2 to 4, doubling, not from 1 to 4. | correct | B4 |
| `screens[1].hints[0]` | Read the slope at $y_0 = 0.5$, 1 and 2. What do you multiply $y_0$ by? | correct | B4 |
| `screens[1].feedback.correct` | The slope at $x = 1$ is $2y_0$: double the value of $y$ on the slice. | correct | B4 |
| `screens[1].feedback.generic` | Not quite right. Set $y_0$ to 0.5, 1 and 2, and compare each slope with $y_0$. | correct | B4 |
| `screens[1].explain.text` | At $y_0 = 0.5$, 1 and 2 the slope reads 1, 2 and 4. So the slope at $x = 1$ is $2y_0$, and at a general $x$ it is $2xy_0$. The $3y_0$ never tilts t... | correct | B4 |
| `screens[2].prose` | You held $y$ fixed and differentiated in $x$. That is the **partial derivative** of $f$ with respect to $x$, written $\dfrac{\partial f}{\partial x... | correct | B4 |
| `screens[2].question` | Write $f_x$ for $f(x, y) = x^2 y + 3y$. | correct | B4 |
| `screens[2].widget.answer` | 2xy | correct | B4 |
| `screens[2].widget.accept` | 2xy, 2*x*y, 2yx, 2*y*x, 2 x y | correct | B4 |
| `screens[2].widget.wrong[0]` | slip kept-3 = 2xy+3 | correct | B4 |
| `screens[2].widget.wrong[1]` | slip dropped-y = 2x | correct | B4 |
| `screens[2].widget.wrong[2]` | slip wrong-variable = x^2+3 | correct | B4 |
| `screens[2].hints[0]` | Pretend $y$ is a number, say 5. Differentiate $5x^2 + 15$. | correct | B4 |
| `screens[2].hints[1]` | With $y$ as a constant, $x^2 y$ is a constant times $x^2$, and $3y$ is a constant. | correct | B4 |
| `screens[2].hints[2]` | $\frac{\partial}{\partial x}(x^2 y) = 2x \cdot y$ and $\frac{\partial}{\partial x}(3y) = 0$. | correct | B4 |
| `screens[2].feedback.correct` | $f_x = 2xy$. At $x = 1$ that is $2y$, the slope you saw. | correct | B4 |
| `screens[2].feedback.generic` | Not quite right. Treat $y$ as a fixed number and differentiate in $x$. | correct | B4 |
| `screens[2].feedback.byKey.kept-3` | The $3y$ has no $x$ in it, so with $y$ fixed it is a constant. Its slope is 0. | correct | B4 |
| `screens[2].feedback.byKey.dropped-y` | You differentiated $x^2$ but lost its factor $y$. A constant factor stays: $2x \cdot y$. | correct | B4 |
| `screens[2].feedback.byKey.wrong-variable` | That is $f_y$: you differentiated with respect to $y$. Here $x$ moves and $y$ is held. | correct | B4 |
| `screens[2].explain.text` | With $y$ held fixed, $x^2 y$ is a constant times $x^2$, giving $2xy$. The $3y$ is a constant, giving 0. So $f_x = 2xy$, which at $x = 1$ is the $2y... | correct | B4 |
| `screens[3].prose` | Now hold $x$ fixed at 2 and let $y$ move. The slice runs up the page on the contour map. Along it, $f(2, y) = 4y + 3y$, a function of $y$ alone. | correct | B4 |
| `screens[3].question` | What is $\dfrac{\partial f}{\partial y}$ at $(2, 2)$, for $f = x^2 y + 3y$? | correct | B4 |
| `screens[3].widget.answer` | 7 | correct | B4 |
| `screens[3].widget.accept` | 7: $f_y = x^2 + 3$, which is $4 + 3$ at $x = 2$. | correct | B4 |
| `screens[3].widget.wrong[0]` | slip dropped-3 = 4 | correct | B4 |
| `screens[3].widget.wrong[1]` | slip f-x = 8 | correct | B4 |
| `screens[3].widget.wrong[2]` | slip height = 14 | correct | B4 |
| `screens[3].hints[0]` | Now $x$ is the constant. What is $f_y$ as a formula? | correct | B4 |
| `screens[3].hints[1]` | $x^2 y$ is the constant $x^2$ times $y$, and $3y$ has slope 3. | correct | B4 |
| `screens[3].hints[2]` | $f_y = x^2 + 3$. At $x = 2$ that is 7, the slope of the line $7y$. | correct | B4 |
| `screens[3].feedback.correct` | $f_y = x^2 + 3 = 7$ at $x = 2$, whatever $y$ is. | correct | B4 |
| `screens[3].feedback.generic` | Not quite right. Hold $x$ at 2 and differentiate $f$ in $y$. | correct | B4 |
| `screens[3].feedback.byKey.dropped-3` | You differentiated $x^2 y$ to $x^2 = 4$ but dropped the $3y$. Now $y$ moves, so $3y$ has slope 3. | correct | B4 |
| `screens[3].feedback.byKey.f-x` | 8 is $f_x = 2xy$ at $(2, 2)$: the slope across the page. Here the slice runs up the page. | correct | B4 |
| `screens[3].feedback.byKey.height` | 14 is the height $f(2, 2)$. The partial derivative is the slope of the slice. | correct | B4 |
| `screens[3].explain.text` | Holding $x = 2$ makes $f = 4y + 3y = 7y$, a straight line in $y$. Its slope is 7 everywhere along the slice. In general $f_y = x^2 + 3$. | correct | B4 |
| `screens[4].prose` | Take $f(x, y) = e^{xy}$. The graph is its slice at $y = \tfrac12$, which is $e^{x/2}$, with the tangent at $x = 0$. | correct | B4 |
| `screens[4].question` | Find $\dfrac{\partial f}{\partial x}$ for $f(x, y) = e^{xy}$. | correct | B4 |
| `screens[4].widget.answer` | ye^{xy} | correct | B4 |
| `screens[4].widget.accept` | y*e^(x*y), y*e^(xy), ye^(xy), e^(xy)*y, e^(x*y)*y, y*exp(x*y), e^{xy}y | correct | B4 |
| `screens[4].widget.wrong[0]` | slip no-chain = e^{xy} | correct | B4 |
| `screens[4].widget.wrong[1]` | slip wrong-variable = xe^{xy} | correct | B4 |
| `screens[4].widget.wrong[2]` | slip power-rule = xye^{xy-1} | correct | B4 |
| `screens[4].hints[0]` | With $y$ fixed, $e^{xy}$ is like $e^{5x}$. What is the derivative of $e^{5x}$? | correct | B4 |
| `screens[4].hints[1]` | The chain rule brings down the derivative of the exponent $xy$ with respect to $x$. | correct | B4 |
| `screens[4].hints[2]` | $\frac{\partial}{\partial x}(xy) = y$, so $f_x = y\,e^{xy}$. At $y = \tfrac12$, $x = 0$ that is $\tfrac12$, the slope drawn. | correct | B4 |
| `screens[4].feedback.correct` | $f_x = y e^{xy}$. At $(0, \tfrac12)$ it is $\tfrac12$, the slope on the graph. | correct | B4 |
| `screens[4].feedback.generic` | Not quite right. Treat $y$ as a constant $k$: the derivative of $e^{kx}$ is $k e^{kx}$. | correct | B4 |
| `screens[4].feedback.byKey.no-chain` | You left out the chain rule. The exponent $xy$ changes at rate $y$ as $x$ moves, so a factor $y$ comes down. | correct | B4 |
| `screens[4].feedback.byKey.wrong-variable` | That is $f_y$: the factor $x$ comes from moving $y$. Here $x$ moves, so the factor is $y$. | correct | B4 |
| `screens[4].feedback.byKey.power-rule` | The power rule is for $x^n$ with a fixed power. Here the variable is in the exponent: use $\frac{d}{dx} e^{kx} = k e^{kx}$. | correct | B4 |
| `screens[4].explain.text` | With $y$ held, $e^{xy}$ is $e^{kx}$ with $k = y$, whose derivative is $k e^{kx}$. So $f_x = y e^{xy}$. At $y = \tfrac12$ and $x = 0$ that gives $\t... | correct | B4 |
| `screens[5].prose` | Take $f(x, y) = \ln(x^2 + y^2)$. Its contours are circles about the origin, where $f$ is not defined. P is the point $(1, 2)$. | correct | B4 |
| `screens[5].question` | What is $\dfrac{\partial f}{\partial y}$ at $(1, 2)$? | correct | B4 |
| `screens[5].widget.answer` | 0.8 | correct | B4 |
| `screens[5].widget.accept` | 0.8: $f_y = \dfrac{2y}{x^2 + y^2} = \dfrac{4}{5}$. | correct | B4 |
| `screens[5].widget.wrong[0]` | slip f-x = 0.4 | correct | B4 |
| `screens[5].widget.wrong[1]` | slip no-chain = 0.2 | correct | B4 |
| `screens[5].widget.wrong[2]` | slip no-denominator = 4 | correct | B4 |
| `screens[5].widget.wrong[3]` | slip value = 1.6094 | correct | B4 |
| `screens[5].hints[0]` | Hold $x$ fixed. The outer function is $\ln$, the inner is $x^2 + y^2$. | correct | B4 |
| `screens[5].hints[1]` | The derivative of $\ln u$ is $\frac{u'}{u}$. Here $u'$ is the $y$-derivative of $x^2 + y^2$. | correct | B4 |
| `screens[5].hints[2]` | $f_y = \frac{2y}{x^2 + y^2}$. At $(1, 2)$: $\frac{4}{5}$. | correct | B4 |
| `screens[5].feedback.correct` | $f_y = \frac{2y}{x^2 + y^2} = \frac{4}{5} = 0.8$. | correct | B4 |
| `screens[5].feedback.generic` | Not quite right. Use $\frac{d}{dy}\ln u = \frac{1}{u}\frac{\partial u}{\partial y}$ with $u = x^2 + y^2$. | correct | B4 |
| `screens[5].feedback.byKey.f-x` | 0.4 is $f_x = \frac{2x}{x^2 + y^2}$. You moved $x$; here $y$ moves, so the top is $2y$. | correct | B4 |
| `screens[5].feedback.byKey.no-chain` | You stopped at $\frac{1}{x^2 + y^2}$. The chain rule multiplies by the $y$-derivative of the inside, $2y$. | correct | B4 |
| `screens[5].feedback.byKey.no-denominator` | You kept the $2y$ but lost the $\frac{1}{x^2 + y^2}$ from differentiating $\ln$. | correct | B4 |
| `screens[5].feedback.byKey.value` | 1.609 is $\ln 5$, the value of $f$ at P. The question asks for its slope in $y$. | correct | B4 |
| `screens[5].explain.text` | Holding $x$ fixed, the chain rule gives $f_y = \frac{2y}{x^2 + y^2}$. At $(1, 2)$ that is $\frac{4}{5} = 0.8$. By symmetry $f_x = \frac{2x}{x^2 + y... | correct | B4 |
| `screens[6].prose` | Take $f(x, y) = xy$. The graph is its slice at $y = 3$, the line $f(x, 3) = 3x$. | correct | B4 |
| `screens[6].question` | What is $\dfrac{\partial}{\partial x}(xy)$? | correct | B4 |
| `screens[6].widget.options[0]` | option y (key): $y$ | correct | B4 |
| `screens[6].widget.options[1]` | option one: $1$ | correct | B4 |
| `screens[6].widget.options[1].why` | You differentiated $x$ to 1 and dropped $y$. But $y$ is a fixed number here, like the 3 in $3x$, whose slope is 3. | correct | B4 |
| `screens[6].widget.options[2]` | option sum: $x + y$ | correct | B4 |
| `screens[6].widget.options[2].why` | You used the product rule as if $y$ moved with $x$. With $y$ held fixed its derivative is 0, so only $y$ is left. | correct | B4 |
| `screens[6].widget.options[3]` | option zero: $0$ | correct | B4 |
| `screens[6].widget.options[3].why` | You treated the whole term as a constant because it contains $y$. It also contains $x$, which moves. | correct | B4 |
| `screens[6].hints[0]` | Replace $y$ by the number 3. What is the derivative of $3x$? | correct | B4 |
| `screens[6].hints[1]` | The slice at $y = 3$ is the line $3x$. Read its slope. | correct | B4 |
| `screens[6].hints[2]` | $\frac{d}{dx}(3x) = 3$. With a general fixed $y$, $\frac{\partial}{\partial x}(xy) = y$. | correct | B4 |
| `screens[6].feedback.correct` | A fixed $y$ is a constant factor, so the slope is $y$. | correct | B4 |
| `screens[6].feedback.generic` | Not quite right. Put a number in for $y$ and differentiate. | correct | B4 |
| `screens[6].feedback.byKey.one` | You differentiated $x$ to 1 and dropped $y$. But $y$ is a fixed number, like the 3 in $3x$, whose slope is 3, not 1. | correct | B4 |
| `screens[6].feedback.byKey.sum` | You used the product rule as if $y$ changed with $x$. Held fixed, $y$ has derivative 0, leaving only $y$. | correct | B4 |
| `screens[6].explain.text` | At $y = 3$ the slice is $3x$, with slope 3. At $y = -1$ it would be $-x$, with slope $-1$. The slope is always the fixed $y$: $\frac{\partial}{\par... | correct | B4 |
| `screens[7].prose` | Formally, $f_x(a, b) = \displaystyle\lim_{h \to 0} \frac{f(a + h, b) - f(a, b)}{h}$: nudge $x$ alone, keep $y = b$. Use it to confirm $\frac{\parti... | correct | B5 |
| `screens[7].question` | Put the lines in order. | correct | B5 |
| `screens[7].widget.lines[0]` | line def: $f_x(a, b) = \displaystyle\lim_{h \to 0} \frac{f(a + h, b) - f(a, b)}{h}$, move $x$ by $h$ and hold $y = b$ | correct | B5 |
| `screens[7].widget.lines[1]` | line sub: $= \displaystyle\lim_{h \to 0} \frac{(a + h)b - ab}{h}$, put in $f(x, y) = xy$ | correct | B5 |
| `screens[7].widget.lines[2]` | line expand: $= \displaystyle\lim_{h \to 0} \frac{hb}{h}$, expand: the $ab$ terms cancel | correct | B5 |
| `screens[7].widget.lines[3]` | line cancel: $= b$, cancel $h \neq 0$; nothing depends on $h$ any more | correct | B5 |
| `screens[7].widget.answer` | def, sub, expand, cancel | correct | B5 |
| `screens[7].hints[0]` | Start from the definition, then put in the function. | correct | B5 |
| `screens[7].hints[1]` | Expand $(a + h)b$ before cancelling anything. | correct | B5 |
| `screens[7].hints[2]` | Definition, substitute $xy$, expand so $ab$ cancels, then cancel $h$. | correct | B5 |
| `screens[7].feedback.correct` | $f_x(a, b) = b$: the slope in $x$ is the fixed value of $y$. | correct | B5 |
| `screens[7].feedback.generic` | Not quite right. Begin with the limit definition and simplify one step per line. | correct | B5 |
| `screens[7].feedback.byKey.cancel` | You can cancel $h$ only once the top has become $hb$. | correct | B5 |
| `screens[7].explain.text` | Only $x$ moved, by $h$, so the top became $(a + h)b - ab = hb$. Cancelling $h$ leaves $b$, the value $y$ was held at. Every partial derivative is t... | correct | B5 |
| `screens[8].prose` | An option's value $V$ depends on the share price $S$ and the volatility $\sigma$. **Delta** is $\dfrac{\partial V}{\partial S}$ and **vega** is $\d... | correct | B6 |
| `screens[8].question` | Estimate delta at $S = \text{£}100$, $\sigma = 0.20$, in pounds of option value per £1 of share price. | correct | B6 |
| `screens[8].widget.answer` | 0.53 | correct | B6 |
| `screens[8].widget.accept` | 0.53, from $\frac{6.18 - 5.12}{2}$; a one-sided 0.52 or 0.54 is also accepted. | correct | B6 |
| `screens[8].widget.wrong[0]` | slip diagonal = 0.81 | correct | B6 |
| `screens[8].widget.wrong[1]` | slip no-halve = 1.06 | correct | B6 |
| `screens[8].widget.wrong[2]` | slip vega = 0.28 | correct | B6 |
| `screens[8].hints[0]` | Delta holds $\sigma$ fixed. Which column do you stay in? | correct | B6 |
| `screens[8].hints[1]` | Stay in the $\sigma = 0.20$ column and compare $S = 99$ with $S = 101$. | correct | B6 |
| `screens[8].hints[2]` | $\frac{6.18 - 5.12}{101 - 99} = \frac{1.06}{2}$. | correct | B6 |
| `screens[8].feedback.correct` | $\frac{6.18 - 5.12}{2} = 0.53$: the option gains about 53p per £1 on the share. | correct | B6 |
| `screens[8].feedback.generic` | Not quite right. Hold $\sigma$ at 0.20, and divide the change in $V$ by the change in $S$. | correct | B6 |
| `screens[8].feedback.byKey.diagonal` | You moved along the diagonal, so $\sigma$ changed as well as $S$. Delta holds $\sigma$ fixed: stay in one column. | correct | B6 |
| `screens[8].feedback.byKey.no-halve` | 1.06 is the change in $V$ over a £2 move in $S$. Divide by 2 for the change per £1. | correct | B6 |
| `screens[8].feedback.byKey.vega` | 0.28 is vega: you moved along a row, changing $\sigma$ with $S$ fixed. | correct | B6 |
| `screens[8].explain.text` | Holding $\sigma = 0.20$ is a slice down one column. Across £2 of share price $V$ rises £1.06, so delta is about 0.53. Along the $S = 100$ row, vega... | correct | B6 |
| `summary.ideas[0]` | Fix $y$ and $f$ becomes a function of $x$ alone: a slice of the surface. | correct | B4 |
| `summary.ideas[1]` | The slope of that slice is the partial derivative $f_x$. Differentiate in $x$ and treat every $y$ as a constant number. | correct | B4 |
| `summary.ideas[2]` | $f_y$ is the same with the roles swapped. Delta and vega are the partials of an option's value in $S$ and $\sigma$. | correct | B4 |
| `summary.formula.name` | Partial derivative | correct | B4 |
| `summary.formula.tex` | f_x(a, b) = \lim_{h \to 0} \frac{f(a + h, b) - f(a, b)}{h} | correct | B4 |
| `summary.formula.note` | Only $x$ moves; $y$ stays at $b$. | correct | B4 |
| `summary.trap` | A held $y$ is a constant factor, not a variable: $\frac{\partial}{\partial x}(xy) = y$, not 1. | correct | B4 |
| `quiz[0].prose` | Take $f(x, y) = 3x^2 y^3$. | correct | B4 |
| `quiz[0].question` | Find $\dfrac{\partial f}{\partial y}$. | correct | B4 |
| `quiz[0].widget.answer` | 9x^2y^2 | correct | B4 |
| `quiz[0].widget.accept` | 9x^2y^2, 9*x^2*y^2, 9y^2x^2, 9*y^2*x^2 | correct | B4 |
| `quiz[0].widget.wrong[0]` | slip f-x = 6xy^3 | correct | B4 |
| `quiz[0].widget.wrong[1]` | slip dropped-x = 9y^2 | correct | B4 |
| `quiz[0].widget.wrong[2]` | slip no-power = 3x^2y^2 | correct | B4 |
| `quiz[0].feedback.correct` | $3x^2$ is a constant factor, and $\frac{d}{dy}y^3 = 3y^2$. | correct | B4 |
| `quiz[0].feedback.generic` | Not quite right. Treat $3x^2$ as a constant and differentiate $y^3$. | correct | B4 |
| `quiz[0].feedback.byKey.f-x` | That is $f_x$: you moved $x$. Hold $x$ fixed and differentiate in $y$. | correct | B4 |
| `quiz[0].feedback.byKey.dropped-x` | The factor $x^2$ is a constant, so it stays in the answer. | correct | B4 |
| `quiz[0].feedback.byKey.no-power` | You lowered the power but did not bring the 3 down: $\frac{d}{dy}y^3 = 3y^2$. | correct | B4 |
| `quiz[0].explain.text` | With $x$ fixed, $3x^2$ is a constant factor. The power rule gives $\frac{d}{dy}y^3 = 3y^2$. So $f_y = 3x^2 \cdot 3y^2 = 9x^2y^2$. | correct | B4 |
| `quiz[1].prose` | Take $f(x, y) = y^2 + 5$. It is a function of two variables whose formula happens to contain no $x$. | correct | B4 |
| `quiz[1].question` | What is $\dfrac{\partial f}{\partial x}$? | correct | B4 |
| `quiz[1].widget.options[0]` | option zero (key): $0$ | correct | B4 |
| `quiz[1].widget.options[1]` | option two-y: $2y$ | correct | B4 |
| `quiz[1].widget.options[1].why` | That is $f_y$. Moving $x$ with $y$ fixed leaves $y^2 + 5$ unchanged. | correct | B4 |
| `quiz[1].widget.options[2]` | option undefined: It is undefined, since $f$ has no $x$ | correct | B4 |
| `quiz[1].widget.options[2].why` | $f$ still has a value at every $(x, y)$. It just does not change as $x$ moves, so the slope is 0. | correct | B4 |
| `quiz[1].feedback.correct` | Every slice in $x$ is flat, so $f_x = 0$. | correct | B4 |
| `quiz[1].feedback.generic` | Not quite right. Fix $y$ and ask how $f$ changes as $x$ moves. | correct | B4 |
| `quiz[1].explain.text` | Fix $y$, say $y = 2$: then $f = 9$ for every $x$. Each slice in $x$ is flat, so $f_x = 0$ everywhere. The contours are horizontal lines. | correct | B4 |
| `quiz[2].prose` | Take $f(x, y) = \dfrac{x}{y}$. | correct | B4 |
| `quiz[2].question` | What is $\dfrac{\partial f}{\partial y}$ at $(2, 4)$? | correct | B4 |
| `quiz[2].widget.answer` | -0.125 | correct | B4 |
| `quiz[2].widget.accept` | $-0.125$: $f_y = -\dfrac{x}{y^2} = -\dfrac{2}{16}$. | correct | B4 |
| `quiz[2].widget.wrong[0]` | slip f-x = 0.25 | correct | B4 |
| `quiz[2].widget.wrong[1]` | slip sign = 0.125 | correct | B4 |
| `quiz[2].widget.wrong[2]` | slip no-square = -0.5 | correct | B4 |
| `quiz[2].feedback.correct` | $f_y = -\frac{x}{y^2} = -\frac{2}{16} = -0.125$. | correct | B4 |
| `quiz[2].feedback.generic` | Not quite right. Write $f = x\,y^{-1}$ and differentiate in $y$ with $x$ fixed. | correct | B4 |
| `quiz[2].feedback.byKey.f-x` | 0.25 is $f_x = \frac{1}{y}$. Here $y$ moves. | correct | B4 |
| `quiz[2].feedback.byKey.sign` | $\frac{d}{dy}y^{-1} = -y^{-2}$: raising $y$ lowers $\frac{x}{y}$, so the sign is negative. | correct | B4 |
| `quiz[2].feedback.byKey.no-square` | $\frac{d}{dy}y^{-1} = -y^{-2}$, so you divide by $y^2 = 16$, not by $y$. | correct | B4 |
| `quiz[2].explain.text` | With $x$ fixed, $f = x\,y^{-1}$, so $f_y = -x\,y^{-2}$. At $(2, 4)$ that is $-\frac{2}{16} = -0.125$. Raising $y$ shrinks the ratio. | correct | B4 |
| `quiz[3].prose` | A book holds two zero-coupon bonds. Its value is $V = 500{,}000\,e^{-2y_1} + 300{,}000\,e^{-10y_2}$ pounds, where $y_1 = 0.03$ is the 2-year yield ... | correct | B4 |
| `quiz[3].question` | About how much does $V$ fall, in pounds, if $y_2$ rises by one basis point (0.0001) and $y_1$ is fixed? | correct | B4 |
| `quiz[3].widget.answer` | 201.1 | correct | B4 |
| `quiz[3].widget.accept` | About £201.10: $\frac{\partial V}{\partial y_2} = -3{,}000{,}000\,e^{-0.4} \approx -2{,}010{,}960$, times 0.0001. | correct | B4 |
| `quiz[3].widget.wrong[0]` | slip no-discount = 300 | correct | B4 |
| `quiz[3].widget.wrong[1]` | slip no-chain = 20.11 | correct | B4 |
| `quiz[3].widget.wrong[2]` | slip short-bond = 94.18 | correct | B4 |
| `quiz[3].feedback.correct` | $3{,}000{,}000 \times e^{-0.4} \times 0.0001 \approx \text{£}201.10$. | correct | B4 |
| `quiz[3].feedback.generic` | Not quite right. Differentiate $V$ in $y_2$ with $y_1$ fixed, then multiply by 0.0001. | correct | B4 |
| `quiz[3].feedback.byKey.no-discount` | You dropped the factor $e^{-0.4} \approx 0.670$. The derivative of $e^{-10y_2}$ keeps $e^{-10y_2}$. | correct | B4 |
| `quiz[3].feedback.byKey.no-chain` | You left out the chain factor $-10$ from the exponent $-10y_2$. | correct | B4 |
| `quiz[3].feedback.byKey.short-bond` | That is the 2-year bond's sensitivity, $\frac{\partial V}{\partial y_1}$. Here $y_1$ is fixed. | correct | B4 |
| `quiz[3].explain.text` | Holding $y_1$, the first term is a constant. $\frac{\partial V}{\partial y_2} = -10 \times 300{,}000\,e^{-10y_2} \approx -2{,}010{,}960$ at $y_2 = ... | correct | B4 |

## l3-second-partials

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Compute second and mixed partial derivatives. | correct | B7 |
| `objectives[1]` | Read $f_{xx}$ as bending along $x$ and $f_{xy}$ as how the $x$-slope changes with $y$ | correct | B7 |
| `screens[0].prose` | Take $f(x, y) = x^2 y$. The curve is its slice at $y = 1.5$, which is $1.5x^2$. Drag P along it: the label reads the slope there. | correct | B7 |
| `screens[0].question` | Drag P from $x = 2$ to $x = 3$. By how much does the slope rise per unit of $x$? | correct | B7 |
| `screens[0].widget.answer` | 3 | correct | B7 |
| `screens[0].widget.accept` | 3: the slope goes from 6 at $x = 2$ to 9 at $x = 3$. | correct | B7 |
| `screens[0].widget.wrong[0]` | slip end-slope = 9 | correct | B7 |
| `screens[0].widget.wrong[1]` | slip height-change = 7.5 | correct | B7 |
| `screens[0].widget.wrong[2]` | slip start-slope = 6 | correct | B7 |
| `screens[0].hints[0]` | Read the slope label at $x = 2$, then at $x = 3$. | correct | B7 |
| `screens[0].hints[1]` | The slope is 6 at $x = 2$. What does the label say at $x = 3$? | correct | B7 |
| `screens[0].hints[2]` | From 6 to 9 over one unit of $x$: a rise of 3. | correct | B7 |
| `screens[0].feedback.correct` | From 6 to 9 over one unit: the slope rises 3 per unit of $x$. | correct | B7 |
| `screens[0].feedback.generic` | Not quite right. Subtract the slope at $x = 2$ from the slope at $x = 3$. | correct | B7 |
| `screens[0].feedback.byKey.end-slope` | 9 is the slope at $x = 3$. The question asks how much it rose from $x = 2$. | correct | B7 |
| `screens[0].feedback.byKey.start-slope` | 6 is the slope at $x = 2$. Drag on to $x = 3$ and subtract. | correct | B7 |
| `screens[0].feedback.byKey.height-change` | 7.5 is the rise in height, $13.5 - 6$. Compare the slopes, not the heights. | correct | B7 |
| `screens[0].explain.text` | The slope of $1.5x^2$ is $3x$: 6 at $x = 2$ and 9 at $x = 3$. It rises 3 per unit, so the slice bends upward. That rate is the second derivative of... | correct | B7 |
| `screens[1].prose` | Same $f(x, y) = x^2 y$. Its $x$-slope is $f_x = 2xy$. Now keep $x = 1$ and move the slice with the slider. Watch the slope at P. | correct | B7 |
| `screens[1].question` | Each step of 1 in $y_0$ changes the slope at $x = 1$ by how much? | correct | B7 |
| `screens[1].widget.answer` | 2 | correct | B7 |
| `screens[1].widget.accept` | 2: the slope at $x = 1$ is $2y_0$. | correct | B7 |
| `screens[1].widget.wrong[0]` | slip read-slope = 4 | correct | B7 |
| `screens[1].widget.wrong[1]` | slip read-step = 1 | correct | B7 |
| `screens[1].hints[0]` | Read the slope at $y_0 = 1$ and at $y_0 = 2$, then subtract. | correct | B7 |
| `screens[1].feedback.correct` | The slope goes 2, 4, 6 as $y_0$ goes 1, 2, 3: up 2 per unit. | imprecise | finding 7: the slider stops at y0 = 2.5, so the slope 6 at y0 = 3 is never shown; the arithmetic is right |
| `screens[1].feedback.generic` | Not quite right. Compare the slope at $y_0 = 1$ with the slope at $y_0 = 2$. | correct | B7 |
| `screens[1].feedback.byKey.read-slope` | 4 is the slope at $y_0 = 2$. The question asks how much it changes per unit of $y_0$. | correct | B7 |
| `screens[1].feedback.byKey.read-step` | 1 is the change in $y_0$. Look at how far the slope moves over that step. | correct | B7 |
| `screens[1].explain.text` | At $x = 1$ the slope is $f_x = 2y_0$, so it climbs 2 for each unit of $y_0$. That is the derivative of $f_x$ with respect to $y$: $\frac{\partial}{... | correct | B7 |
| `screens[2].prose` | Differentiating a partial again gives a **second partial**. $f_{xx} = \frac{\partial^2 f}{\partial x^2}$ is the bend along $x$. The **mixed partial... | correct | B7 |
| `screens[2].question` | Still with $f = x^2 y$, what is $f_{yy}$ at $(3, 1)$? | correct | B7 |
| `screens[2].widget.answer` | 0 | correct | B7 |
| `screens[2].widget.accept` | 0: $f_y = x^2$ has no $y$ in it, so $f_{yy} = 0$. | correct | B7 |
| `screens[2].widget.wrong[0]` | slip stopped = 9 | correct | B7 |
| `screens[2].widget.wrong[1]` | slip mixed = 6 | correct | B7 |
| `screens[2].widget.wrong[2]` | slip f-xx = 2 | correct | B7 |
| `screens[2].hints[0]` | Find $f_y$ first, then differentiate it in $y$ again. | correct | B7 |
| `screens[2].hints[1]` | $f_y = x^2$. Does it change when $y$ moves? | correct | B7 |
| `screens[2].hints[2]` | $x^2$ is a constant when $x$ is held, so its $y$-derivative is 0. The slice $9y$ is straight. | correct | B7 |
| `screens[2].feedback.correct` | $f_y = x^2$ does not depend on $y$, so $f_{yy} = 0$. | correct | B7 |
| `screens[2].feedback.generic` | Not quite right. Differentiate in $y$ twice, holding $x$ each time. | correct | B7 |
| `screens[2].feedback.byKey.stopped` | 9 is $f_y = x^2$ at $x = 3$. Differentiate once more in $y$. | correct | B7 |
| `screens[2].feedback.byKey.mixed` | 6 is $f_{xy} = 2x$ at $x = 3$. Here both derivatives are in $y$. | correct | B7 |
| `screens[2].feedback.byKey.f-xx` | 2 is $f_{xx} = 2y$ at $y = 1$. Here both derivatives are in $y$. | correct | B7 |
| `screens[2].explain.text` | Holding $x = 3$ makes the slice $9y$, a straight line. Its slope never changes, so $f_{yy} = 0$. A zero second partial means no bend in that direct... | correct | B7 |
| `screens[3].prose` | Take $f(x, y) = x^3 y^2$. Its first partials are $f_x = 3x^2y^2$ and $f_y = 2x^3y$. Differentiate each again, and evaluate at $(1, 3)$. | correct | B7 |
| `screens[3].question` | Fill in the four second partials at $(1, 3)$. | correct | B7 |
| `screens[3].widget.columns` | Partial, How, At $(1, 3)$ | correct | B7 |
| `screens[3].widget.rows[0]` | $f_x$, $3x^2y^2$, 27 | correct | B7 |
| `screens[3].widget.rows[1]` | $f_y$, $2x^3y$, 6 | correct | B7 |
| `screens[3].widget.rows[2]` | $f_{xx}$, $f_x$, then $x$ again, {"edit": true, "answer": 54, "tol": {"abs": 0.001}} | correct | B7 |
| `screens[3].widget.rows[3]` | $f_{xy}$, $f_x$, then $y$, {"edit": true, "answer": 18, "tol": {"abs": 0.001}} | correct | B7 |
| `screens[3].widget.rows[4]` | $f_{yx}$, $f_y$, then $x$, {"edit": true, "answer": 18, "tol": {"abs": 0.001}} | correct | B7 |
| `screens[3].widget.rows[5]` | $f_{yy}$, $f_y$, then $y$ again, {"edit": true, "answer": 2, "tol": {"abs": 0.001}} | correct | B7 |
| `screens[3].hints[0]` | Differentiate the formula in the How column, then put in $x = 1$, $y = 3$. | correct | B7 |
| `screens[3].hints[1]` | $f_{xx}$: differentiate $3x^2y^2$ in $x$ to get $6xy^2$. | correct | B7 |
| `screens[3].hints[2]` | $f_{xx} = 6xy^2 = 54$, $f_{xy} = 6x^2y = 18$, $f_{yx} = 6x^2y = 18$, $f_{yy} = 2x^3 = 2$. | correct | B7 |
| `screens[3].feedback.correct` | 54, 18, 18 and 2. The two mixed partials agree. | correct | B7 |
| `screens[3].feedback.generic` | Not quite right. Differentiate each first partial once more, then evaluate at $(1, 3)$. | correct | B7 |
| `screens[3].feedback.byKey.r2c2` | For $f_{xx}$, differentiate $3x^2y^2$ in $x$: $6xy^2$, which is 54 at $(1, 3)$. | correct | B7 |
| `screens[3].feedback.byKey.r3c2` | For $f_{xy}$, differentiate $3x^2y^2$ in $y$, holding $x$: $6x^2y$, which is 18. | correct | B7 |
| `screens[3].feedback.byKey.r4c2` | For $f_{yx}$, differentiate $2x^3y$ in $x$, holding $y$: $6x^2y$, which is 18. | correct | B7 |
| `screens[3].feedback.byKey.r5c2` | For $f_{yy}$, differentiate $2x^3y$ in $y$: the $y$ goes, leaving $2x^3 = 2$. | correct | B7 |
| `screens[3].explain.text` | You found $f_{xx} = 6xy^2$, $f_{yy} = 2x^3$, and both mixed partials equal to $6x^2y$. Differentiating in $x$ then $y$ gave the same as $y$ then $x... | correct | B7 |
| `screens[4].prose` | Check the pattern on $f(x, y) = e^{xy}$. You found $f_x = y\,e^{xy}$. By symmetry, $f_y = x\,e^{xy}$. | correct | B7 |
| `screens[4].question` | Find $f_{xy}$, the $y$-derivative of $f_x = y\,e^{xy}$. | correct | B7 |
| `screens[4].widget.answer` | (1+xy)e^{xy} | correct | B7 |
| `screens[4].widget.accept` | e^{xy}+xye^{xy}, (1+xy)e^(xy), (1+x*y)*e^(x*y), e^(xy)+xy*e^(xy), e^(x*y)+x*y*e^(x*y), e^(xy)(1+xy), e^(x*y)*(1+x*y) | correct | B7 |
| `screens[4].widget.wrong[0]` | slip no-product = xye^{xy} | correct | B7 |
| `screens[4].widget.wrong[1]` | slip first-only = e^{xy} | correct | B7 |
| `screens[4].widget.wrong[2]` | slip f-xx = y^2e^{xy} | correct | B7 |
| `screens[4].hints[0]` | $f_x = y\,e^{xy}$ is a product of two factors that both contain $y$. | correct | B7 |
| `screens[4].hints[1]` | Use the product rule in $y$: $\frac{\partial}{\partial y}(y) = 1$ and $\frac{\partial}{\partial y}e^{xy} = x\,e^{xy}$. | correct | B7 |
| `screens[4].hints[2]` | $1 \cdot e^{xy} + y \cdot x\,e^{xy} = (1 + xy)\,e^{xy}$. | correct | B7 |
| `screens[4].feedback.correct` | $(1 + xy)\,e^{xy}$, and $f_{yx}$ gives the same. | correct | B7 |
| `screens[4].feedback.generic` | Not quite right. Use the product rule on $y \cdot e^{xy}$, differentiating in $y$. | correct | B7 |
| `screens[4].feedback.byKey.no-product` | You differentiated only $e^{xy}$. The factor $y$ also moves with $y$, adding $1 \cdot e^{xy}$. | correct | B7 |
| `screens[4].feedback.byKey.first-only` | You differentiated the factor $y$ but held $e^{xy}$ fixed. It changes with $y$ too. | correct | B7 |
| `screens[4].feedback.byKey.f-xx` | That is $f_{xx}$: you differentiated $f_x$ in $x$ again. | correct | B7 |
| `screens[4].explain.text` | The product rule in $y$ gives $e^{xy} + xy\,e^{xy} = (1 + xy)e^{xy}$. Starting from $f_y = x\,e^{xy}$ and differentiating in $x$ gives the same. Ag... | correct | B7 |
| `screens[5].prose` | Take $f(x, y) = x^2 - y^2$. At the origin $f_x = f_y = 0$: it is flat. The bottom graph shows the slice along the $x$-axis, $t^2$, and along the $y... | correct | B7 |
| `screens[5].question` | At the origin, what are the signs of $f_{xx}$ and $f_{yy}$? | correct | B7 |
| `screens[5].widget.options[0]` | option right (key): $f_{xx} > 0$ and $f_{yy} < 0$ | correct | B7 |
| `screens[5].widget.options[1]` | option both-up: Both positive | correct | B7 |
| `screens[5].widget.options[1].why` | You read the $x$ slice only. The $y$ slice, $-t^2$, bends down, so $f_{yy} = -2$. | correct | B7 |
| `screens[5].widget.options[2]` | option flat: Both zero, since the origin is flat | correct | B7 |
| `screens[5].widget.options[2].why` | Flat means the first partials are 0. The second partials measure bending: $2$ and $-2$. | correct | B7 |
| `screens[5].widget.options[3]` | option swapped: $f_{xx} < 0$ and $f_{yy} > 0$ | correct | B7 |
| `screens[5].widget.options[3].why` | You swapped the slices. Along $x$ the slice is $t^2$, a cup. | correct | B7 |
| `screens[5].hints[0]` | Which slice is a cup and which is a cap? | correct | B7 |
| `screens[5].hints[1]` | Along the $x$-axis, $f = t^2$. Along the $y$-axis, $f = -t^2$. | correct | B7 |
| `screens[5].hints[2]` | $f_{xx} = 2$ and $f_{yy} = -2$. | correct | B7 |
| `screens[5].feedback.correct` | $f_{xx} = 2 > 0$ and $f_{yy} = -2 < 0$. | correct | B7 |
| `screens[5].feedback.generic` | Not quite right. Read each slice's bend: a cup has positive second derivative, a cap negative. | correct | B7 |
| `screens[5].explain.text` | Along $x$ the surface is a cup, so $f_{xx} = 2$. Along $y$ it is a cap, so $f_{yy} = -2$. A point that is a valley one way and a ridge the other is... | correct | B7 |
| `screens[6].prose` | Take $f(x, y) = x^2 y^3$. Its first partials are in the table. | correct | B7 |
| `screens[6].question` | What is the mixed partial $f_{xy}$? | correct | B7 |
| `screens[6].widget.options[0]` | option right (key): $6xy^2$ | correct | B7 |
| `screens[6].widget.options[1]` | option product: $6x^3y^5$ | correct | B7 |
| `screens[6].widget.options[1].why` | You multiplied $f_x$ by $f_y$. $f_{xy}$ means differentiate $f_x$ again, in $y$. | correct | B7 |
| `screens[6].widget.options[2]` | option f-xx: $2y^3$ | correct | B7 |
| `screens[6].widget.options[2].why` | That is $f_{xx}$: you differentiated $f_x$ in $x$ again. Differentiate it in $y$. | correct | B7 |
| `screens[6].widget.options[3]` | option f-yy: $6x^2y$ | correct | B7 |
| `screens[6].widget.options[3].why` | That is $f_{yy}$: you differentiated $f_y$ in $y$ again. Mixed means one of each. | correct | B7 |
| `screens[6].hints[0]` | $f_{xy}$ is two derivatives in a row, not a product of two. | correct | B7 |
| `screens[6].hints[1]` | Start from $f_x = 2xy^3$ and hold $x$ fixed. | correct | B7 |
| `screens[6].hints[2]` | $\frac{\partial}{\partial y}(2xy^3) = 2x \cdot 3y^2 = 6xy^2$. | correct | B7 |
| `screens[6].feedback.correct` | $\frac{\partial}{\partial y}(2xy^3) = 6xy^2$. From $f_y$ in $x$: also $6xy^2$. | correct | B7 |
| `screens[6].feedback.generic` | Not quite right. Differentiate $f_x$ with respect to $y$. | correct | B7 |
| `screens[6].feedback.byKey.product` | You multiplied $f_x$ by $f_y$. The subscripts mean differentiate twice: $f_x$ first, then in $y$. | correct | B7 |
| `screens[6].explain.text` | The subscripts in $f_{xy}$ are a recipe: differentiate in $x$, then in $y$. From $2xy^3$ that gives $6xy^2$. The product $f_x f_y = 6x^3y^5$ is a d... | correct | B7 |
| `screens[7].prose` | Every time, $f_{xy} = f_{yx}$. Here is why for any polynomial. Each term is a constant times $x^m y^n$, so it is enough to check one such term. | imprecise | finding 1 (same defect): "Every time" holds for the polynomials shown; the general hypothesis is given wrongly in the explanation |
| `screens[7].question` | Put the lines in order. | correct | B8 |
| `screens[7].widget.lines[0]` | line term: $f = x^m y^n$, one term of a polynomial | correct | B8 |
| `screens[7].widget.lines[1]` | line fx: $f_x = m\,x^{m-1} y^n$, power rule in $x$; $y^n$ is a constant factor | correct | B8 |
| `screens[7].widget.lines[2]` | line fxy: $f_{xy} = mn\,x^{m-1} y^{n-1}$, power rule in $y$; $m\,x^{m-1}$ is a constant factor | correct | B8 |
| `screens[7].widget.lines[3]` | line fyx: $f_{yx} = nm\,x^{m-1} y^{n-1}$, the other order: $f_y = n\,x^m y^{n-1}$, then the power rule in $x$ | correct | B8 |
| `screens[7].widget.lines[4]` | line equal: $f_{xy} = f_{yx}$, since $mn = nm$; a sum of terms agrees term by term | correct | B8 |
| `screens[7].widget.answer` | term, fx, fxy, fyx, equal | correct | B8 |
| `screens[7].hints[0]` | Begin with one term, then take the $x$-first route. | correct | B8 |
| `screens[7].hints[1]` | After $f_x$ comes its $y$-derivative. The other order comes next. | correct | B8 |
| `screens[7].hints[2]` | Term, $f_x$, $f_{xy}$, then $f_{yx}$, then compare. | correct | B8 |
| `screens[7].feedback.correct` | Both orders give $mn\,x^{m-1}y^{n-1}$. | correct | B8 |
| `screens[7].feedback.generic` | Not quite right. Follow one route to $f_{xy}$, then the other route, then compare. | correct | B8 |
| `screens[7].feedback.byKey.equal` | The comparison needs both mixed partials first, so it comes last. | correct | B8 |
| `screens[7].feedback.byKey.fxy` | $f_{xy}$ needs $f_x$ first: differentiate in $x$ before $y$. | correct | B8 |
| `screens[7].explain.text` | Each route applies the power rule once in $x$ and once in $y$. The two factors $m$ and $n$ come down either way, so the results match. For smooth f... | imprecise | finding 1: "partial derivatives are continuous" reads as the first partials; Clairaut needs the mixed second partials continuous (Apostol II 8.23; Marsden-Tromba 3.1). Counter-example xy(x^2-y^2)/(x^2+y^2) in concepts-r2 script |
| `screens[8].prose` | For an option value $V(S, \sigma)$, **gamma** is $\frac{\partial^2 V}{\partial S^2}$: how fast delta moves with the share price. **Vanna** is the m... | correct | B9 |
| `screens[8].question` | Estimate vanna at $S = \text{£}105$, $\sigma = 0.20$, per unit of $\sigma$. | correct | B9 |
| `screens[8].widget.answer` | -0.54 | correct | B9 |
| `screens[8].widget.accept` | $-0.54$: $\frac{0.642 - 0.696}{0.25 - 0.15}$. | correct | B9 |
| `screens[8].widget.wrong[0]` | slip sign = 0.54 | correct | B9 |
| `screens[8].widget.wrong[1]` | slip no-divide = -0.054 | correct | B9 |
| `screens[8].widget.wrong[2]` | slip gamma = 0.0276 | correct | B9 |
| `screens[8].widget.wrong[3]` | slip half-step = -0.27 | correct | B9 |
| `screens[8].hints[0]` | Vanna is the change in delta as $\sigma$ moves, with $S$ held. Which row do you stay in? | correct | B9 |
| `screens[8].hints[1]` | Stay in the $S = 105$ row and compare $\sigma = 0.15$ with $\sigma = 0.25$. | correct | B9 |
| `screens[8].hints[2]` | $\frac{0.642 - 0.696}{0.10} = \frac{-0.054}{0.10}$. | correct | B9 |
| `screens[8].feedback.correct` | $\frac{-0.054}{0.10} = -0.54$: more volatility pulls this in-the-money delta down. | correct | B9 |
| `screens[8].feedback.generic` | Not quite right. In the $S = 105$ row, divide the change in delta by the change in $\sigma$. | correct | B9 |
| `screens[8].feedback.byKey.sign` | Delta falls from 0.696 to 0.642 as $\sigma$ rises, so vanna is negative here. | correct | B9 |
| `screens[8].feedback.byKey.no-divide` | $-0.054$ is the change in delta over a $\sigma$ step of 0.10. Divide by 0.10 for the rate per unit. | correct | B9 |
| `screens[8].feedback.byKey.gamma` | That is gamma: you moved down a column. Vanna moves along a row. | correct | B9 |
| `screens[8].feedback.byKey.half-step` | The step from $\sigma = 0.15$ to $0.25$ is 0.10, not 0.20. | correct | B9 |
| `screens[8].explain.text` | Holding $S = 105$, delta falls by 0.054 as $\sigma$ rises by 0.10, so vanna is about $-0.54$. That is $-0.0054$ per vol point. At $S = 95$ the same... | correct | B9 |
| `summary.ideas[0]` | $f_{xx}$ is the bend of the slice along $x$: positive for a cup, negative for a cap. $f_{yy}$ is the same along $y$. | correct | B7 |
| `summary.ideas[1]` | The mixed partial $f_{xy}$ differentiates $f_x$ in $y$: how the $x$-slope changes as $y$ moves. | correct | B7 |
| `summary.ideas[2]` | For smooth functions $f_{xy} = f_{yx}$. Gamma is $V_{SS}$ and vanna is $V_{S\sigma}$ for an option value $V(S, \sigma)$. | imprecise | finding 1 (same defect): "smooth" as defined in screen 8 does not give f_xy = f_yx |
| `summary.formula.name` | Mixed partial | correct | B7 |
| `summary.formula.tex` | f_{xy} = \frac{\partial}{\partial y}\left(\frac{\partial f}{\partial x}\right) = f_{yx} | correct | B7 |
| `summary.formula.note` | Two derivatives in a row, never the product $f_x f_y$. | correct | B7 |
| `summary.trap` | $f_{xy}$ is not $f_x \times f_y$. For $x^2y^3$ it is $6xy^2$, not $6x^3y^5$. | correct | B7 |
| `quiz[0].prose` | Take $f(x, y) = x^4 + x^2y^2 + y^3$. | correct | B7 |
| `quiz[0].question` | Find $f_{xx}$. | correct | B7 |
| `quiz[0].widget.answer` | 12x^2+2y^2 | correct | B7 |
| `quiz[0].widget.accept` | 12x^2+2y^2, 12*x^2+2*y^2, 2y^2+12x^2, 2*y^2+12*x^2 | correct | B7 |
| `quiz[0].widget.wrong[0]` | slip f-x = 4x^3+2xy^2 | correct | B7 |
| `quiz[0].widget.wrong[1]` | slip dropped = 12x^2 | correct | B7 |
| `quiz[0].widget.wrong[2]` | slip f-yy = 2x^2+6y | correct | B7 |
| `quiz[0].feedback.correct` | $f_x = 4x^3 + 2xy^2$, then $f_{xx} = 12x^2 + 2y^2$. | correct | B7 |
| `quiz[0].feedback.generic` | Not quite right. Differentiate in $x$ twice, holding $y$ fixed both times. | correct | B7 |
| `quiz[0].feedback.byKey.f-x` | That is $f_x$. Differentiate it once more in $x$. | correct | B7 |
| `quiz[0].feedback.byKey.dropped` | The middle term $x^2y^2$ gives $2y^2$ after two $x$-derivatives. Only $y^3$ vanishes. | correct | B7 |
| `quiz[0].feedback.byKey.f-yy` | That is $f_{yy}$: both derivatives were in $y$. | correct | B7 |
| `quiz[0].explain.text` | In $x$: $f_x = 4x^3 + 2xy^2$, since $y^3$ is a constant. Again in $x$: $f_{xx} = 12x^2 + 2y^2$. | correct | B7 |
| `quiz[1].prose` | For an option value $V(S, \sigma)$, delta is $\frac{\partial V}{\partial S}$ and vega is $\frac{\partial V}{\partial \sigma}$. Vanna measures how m... | correct | B7 |
| `quiz[1].question` | Which expression is vanna? | correct | B7 |
| `quiz[1].widget.options[0]` | option mixed (key): $\dfrac{\partial^2 V}{\partial \sigma\,\partial S}$ | correct | B7 |
| `quiz[1].widget.options[1]` | option gamma: $\dfrac{\partial^2 V}{\partial S^2}$ | correct | B7 |
| `quiz[1].widget.options[1].why` | That is gamma: how delta changes with $S$, not with $\sigma$. | correct | B7 |
| `quiz[1].widget.options[2]` | option product: $\dfrac{\partial V}{\partial S} \cdot \dfrac{\partial V}{\partial \sigma}$ | correct | B7 |
| `quiz[1].widget.options[2].why` | You multiplied delta by vega. Vanna differentiates delta again, in $\sigma$. | correct | B7 |
| `quiz[1].widget.options[3]` | option volga: $\dfrac{\partial^2 V}{\partial \sigma^2}$ | correct | B7 |
| `quiz[1].widget.options[3].why` | That is how vega changes with $\sigma$, often called volga. Vanna mixes $S$ and $\sigma$. | correct | B7 |
| `quiz[1].feedback.correct` | Differentiate delta, $\frac{\partial V}{\partial S}$, with respect to $\sigma$. | correct | B7 |
| `quiz[1].feedback.generic` | Not quite right. Start from delta and ask which variable vanna moves. | correct | B7 |
| `quiz[1].explain.text` | Vanna is the $\sigma$-derivative of delta: $\frac{\partial}{\partial \sigma}\frac{\partial V}{\partial S}$. Because mixed partials agree, it is als... | correct | B7 |
| `quiz[2].prose` | Take $f(x, y) = x \sin y$. | correct | B7 |
| `quiz[2].question` | What is $f_{xy}$ at $(2, 0)$? | correct | B7 |
| `quiz[2].widget.answer` | 1 | correct | B7 |
| `quiz[2].widget.accept` | 1: $f_x = \sin y$, so $f_{xy} = \cos y = 1$ at $y = 0$. | correct | B7 |
| `quiz[2].widget.wrong[0]` | slip pure = 0 | correct | B7 |
| `quiz[2].widget.wrong[1]` | slip f-y = 2 | correct | B7 |
| `quiz[2].feedback.correct` | $f_x = \sin y$, then $f_{xy} = \cos y$, which is 1 at $y = 0$. | correct | B7 |
| `quiz[2].feedback.generic` | Not quite right. Find $f_x$, then differentiate it in $y$. | correct | B7 |
| `quiz[2].feedback.byKey.pure` | 0 is $f_{xx}$ (and $f_{yy}$) at $(2, 0)$. Mixed means $x$ then $y$. | correct | B7 |
| `quiz[2].feedback.byKey.f-y` | 2 is $f_y = x\cos y$ at $(2, 0)$. Differentiate $f_x$, not $f$. | correct | B7 |
| `quiz[2].explain.text` | With $y$ held, $x\sin y$ has $x$-slope $\sin y$. Its $y$-derivative is $\cos y$, which is 1 at $y = 0$. From $f_y = x\cos y$ in $x$: also $\cos y$. | correct | B7 |
| `quiz[3].prose` | Take $f(x, y) = 3y^2 - x^2$. | correct | B7 |
| `quiz[3].question` | What shape does the surface have at the origin? | correct | B7 |
| `quiz[3].widget.options[0]` | option saddle (key): A saddle: a cap along $x$ and a cup along $y$ | correct | B7 |
| `quiz[3].widget.options[1]` | option valley: A valley: a cup in both directions | correct | B7 |
| `quiz[3].widget.options[1].why` | $f_{xx} = -2 < 0$, so the slice along $x$ is a cap, not a cup. | correct | B7 |
| `quiz[3].widget.options[2]` | option peak: A peak: a cap in both directions | correct | B7 |
| `quiz[3].widget.options[2].why` | $f_{yy} = 6 > 0$, so the slice along $y$ is a cup. | correct | B7 |
| `quiz[3].widget.options[3]` | option reversed: A saddle: a cup along $x$ and a cap along $y$ | correct | B7 |
| `quiz[3].widget.options[3].why` | You swapped the directions: the $-x^2$ term makes the $x$ slice a cap. | correct | B7 |
| `quiz[3].feedback.correct` | $f_{xx} = -2$ and $f_{yy} = 6$: opposite signs, a saddle. | correct | B7 |
| `quiz[3].feedback.generic` | Not quite right. Work out $f_{xx}$ and $f_{yy}$ and read their signs. | correct | B7 |
| `quiz[3].explain.text` | $f_{xx} = -2$ makes the $x$ slice a cap; $f_{yy} = 6$ makes the $y$ slice a cup. Opposite bends in two directions make a saddle. | correct | B7 |

## l4-chain-two-inputs

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Apply the multivariable chain rule along a path. | correct | B10 |
| `objectives[1]` | Split the rate of change of $f$ into a part from each input | correct | B10 |
| `screens[0].prose` | The circles are contours of $f(x, y) = x^2 + y^2$, labelled by level. At time $t$ the point P is at $(2 - t,\ t)$, moving along the dashed path. Sl... | correct | B10 |
| `screens[0].question` | As $t$ runs from 0 to 2.5, what does $f$ at P do? | correct | B10 |
| `screens[0].widget.options[0]` | option dip (key): Falls, then rises | correct | B10 |
| `screens[0].widget.options[1]` | option rise: Rises all the way | correct | B10 |
| `screens[0].widget.options[1].why` | You watched $y$ grow. At first P also moves left, towards the centre, so $f$ falls before it rises. | correct | B10 |
| `screens[0].widget.options[2]` | option fall: Falls all the way | correct | B10 |
| `screens[0].widget.options[2].why` | Watch past $t = 1$: P starts crossing contours outward and $f$ climbs back up. | correct | B10 |
| `screens[0].widget.options[3]` | option same: Stays the same | correct | B10 |
| `screens[0].widget.options[3].why` | Only a walk along a contour keeps $f$ fixed. This path cuts across the circles. | correct | B10 |
| `screens[0].hints[0]` | Watch the value of $f$ in the caption at $t = 0$, 1 and 2. | correct | B10 |
| `screens[0].feedback.correct` | $f$ falls from 4 to 2 at $t = 1$, then rises. | correct | B10 |
| `screens[0].feedback.generic` | Not quite right. Read $f$ in the caption at $t = 0$, $t = 1$ and $t = 2.5$. | correct | B10 |
| `screens[0].explain.text` | From $(2, 0)$ the path heads inward, so $f$ falls from 4. At $t = 1$, P is at $(1, 1)$ and the path just touches the contour 2. After that P moves ... | correct | B10 |
| `screens[1].prose` | Along the path, $f$ is a function of $t$ alone: $f(2 - t,\ t) = (2 - t)^2 + t^2$. At $t = 0.5$, P is at $(1.5, 0.5)$. | correct | B10 |
| `screens[1].question` | At $t = 0.5$, at what rate is $f$ changing? A negative rate means falling. | correct | B10 |
| `screens[1].widget.answer` | -2 | correct | B10 |
| `screens[1].widget.accept` | $-2$: $\frac{d}{dt}\big[(2 - t)^2 + t^2\big] = 4t - 4$. | correct | B10 |
| `screens[1].widget.wrong[0]` | slip sign = 2 | correct | B10 |
| `screens[1].widget.wrong[1]` | slip value = 2.5 | correct | B10 |
| `screens[1].widget.wrong[2]` | slip start = -4 | correct | B10 |
| `screens[1].hints[0]` | Differentiate $(2 - t)^2 + t^2$ with respect to $t$. | correct | B10 |
| `screens[1].hints[1]` | The chain rule gives $\frac{d}{dt}(2 - t)^2 = -2(2 - t)$. | correct | B10 |
| `screens[1].hints[2]` | $-2(2 - t) + 2t = 4t - 4$. Put in $t = 0.5$. | correct | B10 |
| `screens[1].feedback.correct` | $4t - 4 = -2$ at $t = 0.5$: $f$ is falling at 2 per unit of time. | correct | B10 |
| `screens[1].feedback.generic` | Not quite right. Differentiate $(2 - t)^2 + t^2$ in $t$, then put in $t = 0.5$. | correct | B10 |
| `screens[1].feedback.byKey.sign` | $\frac{d}{dt}(2 - t)^2 = -2(2 - t)$: the inner $-t$ brings a minus sign. P is still heading inward, so $f$ falls. | correct | B10 |
| `screens[1].feedback.byKey.value` | 2.5 is the value $f(1.5, 0.5)$. The question asks for its rate of change. | correct | B10 |
| `screens[1].explain.text` | Substituting the path made $f$ a one-variable function, $(2 - t)^2 + t^2$. Its derivative is $4t - 4$, which is $-2$ at $t = 0.5$. Next we split th... | correct | B10 |
| `screens[2].prose` | At $t = 0.5$, P moves left at $x'(t) = -1$ and up at $y'(t) = +1$. Freeze $y$ for an instant and let only $x$ move. At P, $f_x = 2x = 3$. | correct | B10 |
| `screens[2].question` | At what rate does that $x$-motion alone change $f$? | correct | B10 |
| `screens[2].widget.answer` | -3 | correct | B10 |
| `screens[2].widget.accept` | $-3$: $f_x \cdot x'(t) = 3 \times (-1)$. | correct | B10 |
| `screens[2].widget.wrong[0]` | slip sign = 3 | correct | B10 |
| `screens[2].widget.wrong[1]` | slip rate-only = -1 | correct | B10 |
| `screens[2].hints[0]` | $f$ changes at $f_x$ per unit of $x$, and $x$ changes at $x'(t)$ per unit of time. | correct | B10 |
| `screens[2].hints[1]` | Multiply the slope in $x$ by the speed in $x$. | correct | B10 |
| `screens[2].hints[2]` | $f_x \cdot x'(t) = 3 \times (-1)$. | correct | B10 |
| `screens[2].feedback.correct` | $3 \times (-1) = -3$: moving left pulls $f$ down at rate 3. | correct | B10 |
| `screens[2].feedback.generic` | Not quite right. Multiply $f_x = 3$ by $x'(t) = -1$. | correct | B10 |
| `screens[2].feedback.byKey.sign` | P moves left, towards smaller $x$, where $f$ is lower. So this part is negative. | correct | B10 |
| `screens[2].feedback.byKey.rate-only` | $-1$ is how fast $x$ moves. Each unit of $x$ is worth $f_x = 3$ units of $f$. | correct | B10 |
| `screens[2].explain.text` | Each unit of $x$ changes $f$ by $f_x = 3$, and $x$ falls 1 unit per unit of time. So the $x$-motion alone changes $f$ at $3 \times (-1) = -3$. | correct | B10 |
| `screens[3].prose` | Now freeze $x$ and let only $y$ move, at $y'(t) = +1$. At P $= (1.5, 0.5)$, $f_y = 2y$. | correct | B10 |
| `screens[3].question` | At what rate does the $y$-motion alone change $f$? | correct | B10 |
| `screens[3].widget.answer` | 1 | correct | B10 |
| `screens[3].widget.accept` | 1: $f_y \cdot y'(t) = 2(0.5) \times 1$. | correct | B10 |
| `screens[3].widget.wrong[0]` | slip sign = -1 | correct | B10 |
| `screens[3].widget.wrong[1]` | slip formula = 2 | correct | B10 |
| `screens[3].widget.wrong[2]` | slip y-value = 0.5 | correct | B10 |
| `screens[3].hints[0]` | Find $f_y$ at P first. | correct | B10 |
| `screens[3].hints[1]` | $f_y = 2y = 2 \times 0.5 = 1$. | correct | B10 |
| `screens[3].hints[2]` | Multiply by $y'(t) = 1$. | correct | B10 |
| `screens[3].feedback.correct` | $1 \times 1 = 1$. And $-3 + 1 = -2$, the rate you found by substitution. | correct | B10 |
| `screens[3].feedback.generic` | Not quite right. Multiply $f_y$ at P by $y'(t) = 1$. | correct | B10 |
| `screens[3].feedback.byKey.sign` | P moves up, away from the centre in $y$, so this part raises $f$. | correct | B10 |
| `screens[3].feedback.byKey.formula` | $f_y = 2y$, and at P, $y = 0.5$. So $f_y = 1$, not 2. | correct | B10 |
| `screens[3].feedback.byKey.y-value` | 0.5 is the $y$-coordinate of P. Use $f_y = 2y$. | correct | B10 |
| `screens[3].explain.text` | The $y$-motion adds $f_y\,y'(t) = 1 \times 1 = 1$. Together $-3 + 1 = -2$, the rate you found by substituting. This is the **chain rule with two in... | correct | B10 |
| `screens[4].prose` | Now $f(x, y) = x^2 y$, with contours $y = \frac{c}{x^2}$. A point moves along $x = 1 + 2t$, $y = 2 + 3t$. At $t = 0$ it is at $(1, 2)$. | correct | B10 |
| `screens[4].question` | At $t = 0$, at what rate is $f$ changing? | correct | B10 |
| `screens[4].widget.answer` | 11 | correct | B10 |
| `screens[4].widget.accept` | 11: $f_x x' + f_y y' = 4 \times 2 + 1 \times 3$. | correct | B10 |
| `screens[4].widget.wrong[0]` | slip x-only = 8 | correct | B10 |
| `screens[4].widget.wrong[1]` | slip y-only = 3 | correct | B10 |
| `screens[4].widget.wrong[2]` | slip no-weights = 5 | correct | B10 |
| `screens[4].widget.wrong[3]` | slip product = 24 | correct | B10 |
| `screens[4].hints[0]` | Find $f_x$ and $f_y$ at $(1, 2)$, and $x'$ and $y'$. | correct | B10 |
| `screens[4].hints[1]` | $f_x = 2xy = 4$, $f_y = x^2 = 1$, $x' = 2$, $y' = 3$. | correct | B10 |
| `screens[4].hints[2]` | $4 \times 2 + 1 \times 3$. | correct | B10 |
| `screens[4].feedback.correct` | $4 \times 2 + 1 \times 3 = 11$. | correct | B10 |
| `screens[4].feedback.generic` | Not quite right. Pair each partial with its own rate: $f_x x' + f_y y'$. | correct | B10 |
| `screens[4].feedback.byKey.x-only` | 8 is the $x$ part alone. $y$ is moving too, adding $f_y\,y' = 3$. | correct | B10 |
| `screens[4].feedback.byKey.y-only` | 3 is the $y$ part alone. $x$ is moving too, adding $f_x\,x' = 8$. | correct | B10 |
| `screens[4].feedback.byKey.no-weights` | 5 adds numbers without pairing each partial with its rate. Here $x' + y'$ and $f_x + f_y$ both give 5. | correct | B10 |
| `screens[4].feedback.byKey.product` | You multiplied the two parts. The parts add: $8 + 3$. | correct | B10 |
| `screens[4].explain.text` | At $(1, 2)$, $f_x = 4$ and $f_y = 1$, while $x' = 2$ and $y' = 3$. So $\frac{df}{dt} = 8 + 3 = 11$. Substituting $f = (1 + 2t)^2(2 + 3t)$ and diffe... | correct | B10 |
| `screens[5].prose` | Back to $f = x^2 + y^2$. Now P circles round the contour $f = 4$: $x = 2\cos t$, $y = 2\sin t$. At this moment P $= (1.2, 1.6)$, with $x' = -1.6$ a... | correct | B10 |
| `screens[5].question` | What is $\dfrac{df}{dt}$ at this moment? | correct | B10 |
| `screens[5].widget.answer` | 0 | correct | B10 |
| `screens[5].widget.accept` | 0: $2.4 \times (-1.6) + 3.2 \times 1.2 = -3.84 + 3.84$. | correct | B10 |
| `screens[5].widget.wrong[0]` | slip x-only = -3.84 | correct | B10 |
| `screens[5].widget.wrong[1]` | slip y-only = 3.84 | correct | B10 |
| `screens[5].widget.wrong[2]` | slip rates = -0.4 | correct | B10 |
| `screens[5].hints[0]` | Work out $f_x$ and $f_y$ at P first. | correct | B10 |
| `screens[5].hints[1]` | $f_x = 2.4$ and $f_y = 3.2$ at P. | correct | B10 |
| `screens[5].hints[2]` | $2.4 \times (-1.6) + 3.2 \times 1.2$. | correct | B10 |
| `screens[5].feedback.correct` | The two parts, $-3.84$ and $+3.84$, cancel exactly. | correct | B10 |
| `screens[5].feedback.generic` | Not quite right. Compute both parts, $f_x x'$ and $f_y y'$, then add. | correct | B10 |
| `screens[5].feedback.byKey.x-only` | $-3.84$ is the $x$ part alone. The $y$ part is $3.2 \times 1.2 = 3.84$. | correct | B10 |
| `screens[5].feedback.byKey.y-only` | $3.84$ is the $y$ part alone. The $x$ part is $2.4 \times (-1.6) = -3.84$. | correct | B10 |
| `screens[5].feedback.byKey.rates` | You added $x' + y'$. Each rate must be weighted by its partial derivative. | correct | B10 |
| `screens[5].explain.text` | The two parts cancel: $-3.84 + 3.84 = 0$. That had to happen, since P never leaves the contour $f = 4$. Moving along a contour, $\frac{df}{dt} = 0$... | correct | B10 |
| `screens[6].prose` | Same $f = x^2 + y^2$. A new path: $x = 1 + t^2$, $y = 2 + t$. At $t = 0$, P is at $(1, 2)$ with $x'(0) = 0$ and $y'(0) = 1$. | correct | B10 |
| `screens[6].question` | What is $\dfrac{df}{dt}$ at $t = 0$? | correct | B10 |
| `screens[6].widget.options[0]` | option right (key): 4 | correct | B10 |
| `screens[6].widget.options[1]` | option x-only: 0 | correct | B10 |
| `screens[6].widget.options[1].why` | You used only the $x$ term, and $x' = 0$ there. But $y$ is moving, carrying P across contours. | correct | B10 |
| `screens[6].widget.options[2]` | option rates: 1 | correct | B10 |
| `screens[6].widget.options[2].why` | You added $x' + y' = 0 + 1$ without the partials. Each rate is weighted by its slope: $f_y = 4$. | correct | B10 |
| `screens[6].widget.options[3]` | option partials: 6 | correct | B10 |
| `screens[6].widget.options[3].why` | You added $f_x + f_y = 2 + 4$. Each partial must be multiplied by its own rate. | correct | B10 |
| `screens[6].hints[0]` | Is P really standing still? Look at the arrow. | correct | B10 |
| `screens[6].hints[1]` | $x$ is momentarily still, but $y$ moves at rate 1. $f_y = 2y = 4$ at P. | correct | B10 |
| `screens[6].hints[2]` | $f_x x' + f_y y' = 2 \times 0 + 4 \times 1$. | correct | B10 |
| `screens[6].feedback.correct` | $2 \times 0 + 4 \times 1 = 4$. All the change comes from $y$. | correct | B10 |
| `screens[6].feedback.generic` | Not quite right. Use both terms: $f_x x' + f_y y'$. | correct | B10 |
| `screens[6].feedback.byKey.x-only` | You used only $f_x x'$, which is 0 here. $y$ is moving, so $f_y y' = 4$ must be added. | correct | B10 |
| `screens[6].feedback.byKey.rates` | You added the rates $x' + y'$ without their partials. The $y$ rate counts 4 times over, since $f_y = 4$. | correct | B10 |
| `screens[6].explain.text` | At $t = 0$ the path is vertical, so $x' = 0$ and the $x$ term vanishes. The $y$ term is $f_y\,y' = 4 \times 1 = 4$. The arrow crosses contours outw... | correct | B10 |
| `screens[7].prose` | In a short time $\Delta t$, P moves by $\Delta x$ and $\Delta y$. We split the change in $f$ into a step in $x$ and a step in $y$. You did the same... | correct | B11 |
| `screens[7].question` | Put the lines in order. | correct | B11 |
| `screens[7].widget.lines[0]` | line total: $\Delta f = f(x + \Delta x,\ y + \Delta y) - f(x, y)$, the change over the short time | correct | B11 |
| `screens[7].widget.lines[1]` | line split: $= \big[f(x + \Delta x,\ y + \Delta y) - f(x,\ y + \Delta y)\big] + \big[f(x,\ y + \Delta y) - f(x, y)\big]$, add and subtract $f(x, y ... | correct | B11 |
| `screens[7].widget.lines[2]` | line partials: $\approx f_x\,\Delta x + f_y\,\Delta y$, each bracket moves one input only: a partial times its step, for a smooth $f$ | correct | B11 |
| `screens[7].widget.lines[3]` | line divide: $\dfrac{\Delta f}{\Delta t} \approx f_x\dfrac{\Delta x}{\Delta t} + f_y\dfrac{\Delta y}{\Delta t}$, divide by $\Delta t$ | correct | B11 |
| `screens[7].widget.lines[4]` | line limit: $\dfrac{df}{dt} = f_x\,x'(t) + f_y\,y'(t)$, let $\Delta t \to 0$: the ratios become $x'$ and $y'$ | correct | B11 |
| `screens[7].widget.answer` | total, split, partials, divide, limit | correct | B11 |
| `screens[7].hints[0]` | Start with the whole change in $f$. | correct | B11 |
| `screens[7].hints[1]` | The trick line adds and subtracts the same value, so each bracket moves one input. | correct | B11 |
| `screens[7].hints[2]` | Total change, split, partials times steps, divide by $\Delta t$, then take the limit. | correct | B11 |
| `screens[7].feedback.correct` | Two one-input steps, each a partial times its rate. | correct | B11 |
| `screens[7].feedback.generic` | Not quite right. Write the total change, split it into two one-input steps, then divide and take a limit. | correct | B11 |
| `screens[7].feedback.byKey.partials` | The partials appear only once each bracket moves a single input. Split first. | correct | B11 |
| `screens[7].feedback.byKey.limit` | The limit comes last, after dividing by $\Delta t$. | correct | B11 |
| `screens[7].explain.text` | The split makes each bracket a one-input change: in the first only $x$ moves, in the second only $y$. Each is a partial derivative times its step. ... | correct | B11 |
| `screens[8].prose` | You are long 1,000 calls. Each call's value is $V(S, \sigma)$. Right now the share is rising and implied volatility is falling. The pricer and the ... | correct | B12 |
| `screens[8].question` | At what rate is the whole position's value changing, in pounds per hour? | correct | B12 |
| `screens[8].widget.answer` | 140 | correct | B12 |
| `screens[8].widget.accept` | £140 per hour: $1000 \times (0.56 \times 0.50 + 0.28 \times (-0.5))$. | correct | B12 |
| `screens[8].widget.wrong[0]` | slip delta-only = 280 | correct | B12 |
| `screens[8].widget.wrong[1]` | slip vega-only = -140 | correct | B12 |
| `screens[8].widget.wrong[2]` | slip sign = 420 | correct | B12 |
| `screens[8].widget.wrong[3]` | slip rates = 0 | correct | B12 |
| `screens[8].widget.wrong[4]` | slip per-option = 0.14 | correct | B12 |
| `screens[8].hints[0]` | Per call, $\frac{dV}{dt} = \frac{\partial V}{\partial S}\frac{dS}{dt} + \frac{\partial V}{\partial \sigma}\frac{d\sigma}{dt}$. | correct | B12 |
| `screens[8].hints[1]` | The share part is $0.56 \times 0.50$. The vol part is $0.28 \times (-0.5)$. | correct | B12 |
| `screens[8].hints[2]` | $0.28 - 0.14 = 0.14$ per call, times 1,000. | correct | B12 |
| `screens[8].feedback.correct` | $0.28 - 0.14 = 0.14$ per call: £140 per hour on 1,000 calls. | correct | B12 |
| `screens[8].feedback.generic` | Not quite right. Use $\Delta \frac{dS}{dt} + \mathcal{V}\frac{d\sigma}{dt}$ per call, then multiply by 1,000. | correct | B12 |
| `screens[8].feedback.byKey.delta-only` | £280 counts the share move alone. Falling volatility costs $0.28 \times 0.5 = 0.14$ per call. | correct | B12 |
| `screens[8].feedback.byKey.vega-only` | $-\text{£}140$ counts the volatility move alone. The rising share adds £280. | correct | B12 |
| `screens[8].feedback.byKey.sign` | Volatility is falling and the calls are long vega, so that term loses money. Subtract it. | correct | B12 |
| `screens[8].feedback.byKey.rates` | You added the two rates, $0.50 + (-0.5)$. Each must be weighted by delta or vega first. | correct | B12 |
| `screens[8].feedback.byKey.per-option` | £0.14 is the rate for one call. You hold 1,000. | correct | B12 |
| `screens[8].explain.text` | Per call, ignoring time decay, $\frac{dV}{dt} = 0.56 \times 0.50 + 0.28 \times (-0.5) = 0.28 - 0.14 = 0.14$. Over 1,000 calls that is £140 per hour... | correct | B12 |
| `summary.ideas[0]` | Along a path $(x(t), y(t))$, $f$ becomes a function of $t$ alone. | correct | B10 |
| `summary.ideas[1]` | Its rate of change has one part per input: $f_x\,x'(t)$ from moving $x$ and $f_y\,y'(t)$ from moving $y$. The parts add. | correct | B10 |
| `summary.ideas[2]` | Along a contour the two parts cancel, so $\frac{df}{dt} = 0$. For an option, $\frac{dV}{dt} = \Delta\,\frac{dS}{dt} + \mathcal{V}\,\frac{d\sigma}{d... | correct | B10 |
| `summary.formula.name` | Chain rule along a path | correct | B10 |
| `summary.formula.tex` | \frac{d}{dt} f(x(t), y(t)) = f_x\,x'(t) + f_y\,y'(t) | correct | B10 |
| `summary.formula.note` | Each partial is paired with its own rate, then the two products add. It needs a smooth $f$, one with continuous partial derivatives. | correct | B10 |
| `summary.trap` | Keep both terms, and keep each rate paired with its partial. $x' + y'$ alone, or one term alone, is wrong. | correct | B10 |
| `quiz[0].prose` | Take $f(x, y) = xy$ along $x = t^2$, $y = t^3$. | correct | B10 |
| `quiz[0].question` | What is $\dfrac{df}{dt}$ at $t = 2$? | correct | B10 |
| `quiz[0].widget.answer` | 80 | correct | B10 |
| `quiz[0].widget.accept` | 80: $y\,x' + x\,y' = 8 \times 4 + 4 \times 12$. | correct | B10 |
| `quiz[0].widget.wrong[0]` | slip x-only = 32 | correct | B10 |
| `quiz[0].widget.wrong[1]` | slip y-only = 48 | correct | B10 |
| `quiz[0].widget.wrong[2]` | slip rates = 16 | correct | B10 |
| `quiz[0].widget.wrong[3]` | slip partials = 12 | correct | B10 |
| `quiz[0].feedback.correct` | $8 \times 4 + 4 \times 12 = 80$. Check: $f = t^5$, and $5t^4 = 80$. | correct | B10 |
| `quiz[0].feedback.generic` | Not quite right. At $t = 2$: $x = 4$, $y = 8$, $x' = 4$, $y' = 12$. Use $f_x x' + f_y y'$. | correct | B10 |
| `quiz[0].feedback.byKey.x-only` | 32 is the $x$ part, $f_x x' = 8 \times 4$. Add the $y$ part. | correct | B10 |
| `quiz[0].feedback.byKey.y-only` | 48 is the $y$ part, $f_y y' = 4 \times 12$. Add the $x$ part. | correct | B10 |
| `quiz[0].feedback.byKey.rates` | 16 is $x' + y'$, with no partials. Weight each rate by its partial. | correct | B10 |
| `quiz[0].feedback.byKey.partials` | 12 is $f_x + f_y$. Multiply each by its own rate. | correct | B10 |
| `quiz[0].explain.text` | At $t = 2$: $f_x = y = 8$, $f_y = x = 4$, $x' = 2t = 4$, $y' = 3t^2 = 12$. So $\frac{df}{dt} = 32 + 48 = 80$. Substituting gives $f = t^5$, with $5... | correct | B10 |
| `quiz[1].prose` | A point moves along a path $(x(t), y(t))$ across the contours of $f(x, y)$. | correct | B10 |
| `quiz[1].question` | Which expression is $\dfrac{d}{dt} f(x(t), y(t))$? | correct | B10 |
| `quiz[1].widget.options[0]` | option right (key): $f_x\,x'(t) + f_y\,y'(t)$ | correct | B10 |
| `quiz[1].widget.options[1]` | option one: $f_x\,x'(t)$ | correct | B10 |
| `quiz[1].widget.options[1].why` | That counts only the motion in $x$. When $y$ moves too, it changes $f$ as well. | correct | B10 |
| `quiz[1].widget.options[2]` | option rates: $x'(t) + y'(t)$ | correct | B10 |
| `quiz[1].widget.options[2].why` | That adds the speeds with no slopes. A fast move across a flat region barely changes $f$. | correct | B10 |
| `quiz[1].widget.options[3]` | option all: $f_x\,f_y\,x'(t)\,y'(t)$ | correct | B10 |
| `quiz[1].widget.options[3].why` | That multiplies everything. The two contributions add: one from $x$, one from $y$. | correct | B10 |
| `quiz[1].feedback.correct` | Each input contributes its partial times its rate, and the parts add. | correct | B10 |
| `quiz[1].feedback.generic` | Not quite right. Think of two parts: one from moving $x$, one from moving $y$. | correct | B10 |
| `quiz[1].explain.text` | Moving $x$ changes $f$ at $f_x\,x'$ and moving $y$ changes it at $f_y\,y'$. Over a short time the two changes add. So $\frac{df}{dt} = f_x x' + f_y... | correct | B10 |
| `quiz[2].prose` | A book is long 200 shares of A and short 500 shares of B, so its P&L is $200\,\Delta A - 500\,\Delta B$. A is rising at £0.30 an hour and B at £0.1... | correct | B10 |
| `quiz[2].question` | At what rate is the book's P&L changing, in pounds per hour? | correct | B10 |
| `quiz[2].widget.answer` | 10 | correct | B10 |
| `quiz[2].widget.accept` | £10 per hour: $200 \times 0.30 - 500 \times 0.10$. | correct | B10 |
| `quiz[2].widget.wrong[0]` | slip a-only = 60 | correct | B10 |
| `quiz[2].widget.wrong[1]` | slip short-sign = 110 | correct | B10 |
| `quiz[2].widget.wrong[2]` | slip b-only = -50 | correct | B10 |
| `quiz[2].feedback.correct` | $60 - 50 = \text{£}10$ per hour. | correct | B10 |
| `quiz[2].feedback.generic` | Not quite right. The partials are 200 and $-500$. Multiply each by its price's rate and add. | correct | B10 |
| `quiz[2].feedback.byKey.a-only` | £60 is the gain on A alone. The short B position loses £50 an hour as B rises. | correct | B10 |
| `quiz[2].feedback.byKey.short-sign` | You added the B term. Short 500 means the partial in B is $-500$: a rising B costs money. | correct | B10 |
| `quiz[2].feedback.byKey.b-only` | $-\text{£}50$ is the B leg alone. Add the £60 from A. | correct | B10 |
| `quiz[2].explain.text` | The P&L has partials 200 in A and $-500$ in B. So $\frac{d}{dt}\text{P\&L} = 200 \times 0.30 + (-500) \times 0.10 = 60 - 50 = 10$ pounds per hour. | correct | B10 |

## fluency-l1-two-inputs

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0].skill` | find the level of the contour through a point | correct | B13 |
| `families[0].let.t1` | a*p^2 | correct | B13 |
| `families[0].let.t2` | b*p*q | correct | B13 |
| `families[0].let.t3` | e*q^2 | correct | B13 |
| `families[0].let.key` | a*p^2 + b*p*q + e*q^2 | correct | B13 |
| `families[0].let.neg` | a*sign(p)*p^2 + b*p*q + e*sign(q)*q^2 | correct | B13 |
| `families[0].let.sw` | a*q^2 + b*q*p + e*p^2 | correct | B13 |
| `families[0].where` | p < 0 or q < 0, neg != key, sw != key, sw != neg | correct | B13 |
| `families[0].prompt` | Take $f(x, y) = {a:c}x^2{b:+c}xy{e:+c}y^2$. Which level $c$ is the contour that passes through $({p}, {q})$? | correct | B13 |
| `families[0].widget.answer` | {key} | correct | B13 |
| `families[0].widget.accept` | {key}, since $f({p}, {q}) = {key}$ | correct | B13 |
| `families[0].wrong[0]` | slip negative-square = {neg} | correct | B13 |
| `families[0].wrong[1]` | slip swapped = {sw} | correct | B13 |
| `families[0].solution[0]` | Put $x = {p}$ and $y = {q}$ in: the three terms are ${t1}$, ${t2}$ and ${t3}$. | correct | B13 |
| `families[0].solution[1]` | So $f({p}, {q}) = {key}$, and the contour through the point is $c = {key}$. | correct | B13 |
| `families[1].skill` | keep a linear function on its contour | correct | B13 |
| `families[1].let.ad` | a*d | correct | B13 |
| `families[1].let.r` | -a*d/b | correct | B13 |
| `families[1].let.sl` | a*d/b | correct | B13 |
| `families[1].let.ud` | -b*d/a | correct | B13 |
| `families[1].where` | abs(a) != abs(b) | correct | B13 |
| `families[1].prompt` | Take $f(x, y) = {a:c}x{b:+c}y$. Along a contour, $x$ rises by {d}. What is the change in $y$? Give a fraction or a decimal. | correct | B13 |
| `families[1].widget.answer` | {r} | correct | B13 |
| `families[1].widget.accept` | ${r:frac}$, or a decimal within 0.0005 | correct | B13 |
| `families[1].wrong[0]` | slip sign-lost = {sl} | correct | B13 |
| `families[1].wrong[1]` | slip upside-down = {ud} | correct | B13 |
| `families[1].solution[0]` | Moving $x$ up by {d} changes ${a:c}x$ by ${ad}$. On a contour $f$ stays the same. | correct | B13 |
| `families[1].solution[1]` | So the $y$ term must change by ${-ad}$: the change in $y$ is ${-ad} \div {b:()} = {r:frac}$. | correct | B13 |
| `families[2].skill` | find the missing coordinate of a point on a contour | correct | B13 |
| `families[2].let.t1` | aa*p^2 | correct | B13 |
| `families[2].let.t2` | bb*p | correct | B13 |
| `families[2].let.key` | k - aa*p^2 - bb*p | correct | B13 |
| `families[2].let.ms` | k + aa*p^2 + bb*p | correct | B13 |
| `families[2].let.dx` | k - aa*p^2 | correct | B13 |
| `families[2].where` | aa*p^2 + bb*p != 0, 2*aa*p^2 + bb*p != 0 | correct | B13 |
| `families[2].prompt` | Take $f(x, y) = y{aa:+c}x^2{bb:+c}x$. Find $y$ so that $({p}, y)$ lies on the contour $f = {k}$. | correct | B13 |
| `families[2].widget.answer` | {key} | correct | B13 |
| `families[2].wrong[0]` | slip signs-not-changed = {ms} | correct | B13 |
| `families[2].wrong[1]` | slip one-term-moved = {dx} | correct | B13 |
| `families[2].solution[0]` | At $x = {p}$ the $x$ terms are ${t1}$ and ${t2}$, so $y{t1:+}{t2:+} = {k}$. | correct | B13 |
| `families[2].solution[1]` | So $y = {key}$. | correct | B13 |

## fluency-l2-slicing

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0].skill` | find a partial derivative in x | correct | B14 |
| `families[0].let.cm` | c*m | correct | B14 |
| `families[0].let.bp` | b*p | correct | B14 |
| `families[0].prompt` | Take $f(x, y) = {c:c}{xm}{mono(y; 1, n)}{b:+c}x^{{{p}}}{e:+c}{mono(y; 1, q)}$. Find $f_x$. | correct | B14 |
| `families[0].widget.answer` | {cm:c}{xm1}{mono(y; 1, n)}{bp:+}{mono(x; 1, p - 1)} | correct | B14 |
| `families[0].wrong[0]` | slip y-term-kept = {cm:c}{xm1}{mono(y; 1, n)}{bp:+}{mono(x; 1, p - 1)}{e:+c}{mono(y; 1, q)} | correct | B14 |
| `families[0].wrong[1]` | slip y-dropped = {mono(x; cm, m - 1)}{bp:+}{mono(x; 1, p - 1)} | correct | B14 |
| `families[0].solution[0]` | Hold $y$ fixed: in ${c:c}{xm}{mono(y; 1, n)}$ the factor ${mono(y; 1, n)}$ is a constant, and ${mono(y; e, q)}$ is a constant with $x$-derivative 0. | correct | B14 |
| `families[0].solution[1]` | Differentiate the powers of $x$: $f_x = {cm:c}{xm1}{mono(y; 1, n)}{bp:+}{mono(x; 1, p - 1)}$. | correct | B14 |
| `families[1].skill` | find a partial derivative in y at a point | correct | B14 |
| `families[1].let.cn` | c*n | correct | B14 |
| `families[1].let.eq` | e*q | correct | B14 |
| `families[1].let.key` | c*n*x0^m*y0^(n - 1) + e*q*y0^(q - 1) | correct | B14 |
| `families[1].let.fx` | c*m*x0^(m - 1)*y0^n + b*p*x0^(p - 1) | correct | B14 |
| `families[1].let.fv` | c*x0^m*y0^n + b*x0^p + e*y0^q | correct | B14 |
| `families[1].where` | fx != fv | correct | B14 |
| `families[1].prompt` | Take $f(x, y) = {c:c}{mono(x; 1, m)}{mono(y; 1, n)}{b:+c}{mono(x; 1, p)}{e:+c}{mono(y; 1, q)}$. What is $\dfrac{{\partial f}}{{\partial y}}$ at $({... | correct | B14 |
| `families[1].widget.answer` | {key} | correct | B14 |
| `families[1].wrong[0]` | slip f-x = {fx} | correct | B14 |
| `families[1].wrong[1]` | slip height = {fv} | correct | B14 |
| `families[1].solution[0]` | Hold $x$ fixed: ${mono(x; b, p)}$ is a constant, so $f_y = {cn:c}{mono(x; 1, m)}{yn1}{eq:+}{yq1}$. | correct | B14 |
| `families[1].solution[1]` | At $({x0}, {y0})$ this is $f_y = {key}$. | correct | B14 |
| `families[2].skill` | find a partial derivative of an exponential | correct | B14 |
| `families[2].let.km` | k*m | correct | B14 |
| `families[2].let.ckm` | c*k*m | correct | B14 |
| `families[2].let.ckn` | c*k*n | correct | B14 |
| `families[2].prompt` | Take $f(x, y) = {c:c}e^{{{k:c}{xm}{yn}}}$. Find $f_x$. | correct | B14 |
| `families[2].widget.answer` | {ckm:c}{xm1}{yn}e^{{{k:c}{xm}{yn}}} | correct | B14 |
| `families[2].wrong[0]` | slip no-chain = {c:c}e^{{{k:c}{xm}{yn}}} | correct | B14 |
| `families[2].wrong[1]` | slip wrong-variable = {ckn:c}{xm}{yn1}e^{{{k:c}{xm}{yn}}} | correct | B14 |
| `families[2].solution[0]` | Hold $y$ fixed: the power ${k:c}{xm}{yn}$ has $x$-derivative ${km:c}{xm1}{yn}$. | correct | B14 |
| `families[2].solution[1]` | By the chain rule, $f_x = {ckm:c}{xm1}{yn}e^{{{k:c}{xm}{yn}}}$. | correct | B14 |
| `families[3].skill` | find a partial derivative of a logarithm at a point | correct | B14 |
| `families[3].let.den` | a*x0^2 + b*y0^2 | correct | B14 |
| `families[3].let.b2` | 2*b | correct | B14 |
| `families[3].let.top` | 2*b*y0 | correct | B14 |
| `families[3].let.key` | 2*b*y0/(a*x0^2 + b*y0^2) | correct | B14 |
| `families[3].let.fxv` | 2*a*x0/(a*x0^2 + b*y0^2) | correct | B14 |
| `families[3].let.nochain` | 1/(a*x0^2 + b*y0^2) | correct | B14 |
| `families[3].where` | abs(fxv - nochain) > 0.001 | correct | B14 |
| `families[3].prompt` | Take $f(x, y) = \ln({a:c}x^2+{b:c}y^2)$. What is $\dfrac{{\partial f}}{{\partial y}}$ at $({x0}, {y0})$? Give a fraction or a decimal. | correct | B14 |
| `families[3].widget.answer` | {key} | correct | B14 |
| `families[3].widget.accept` | ${key:frac}$, or a decimal within 0.0005 | correct | B14 |
| `families[3].wrong[0]` | slip f-x = {fxv} | correct | B14 |
| `families[3].wrong[1]` | slip no-chain = {nochain} | correct | B14 |
| `families[3].solution[0]` | Hold $x$ fixed and use the chain rule: $f_y = \dfrac{{{b2}y}}{{{a:c}x^2+{b:c}y^2}}$. | correct | B14 |
| `families[3].solution[1]` | At $({x0}, {y0})$ the top is {top} and the bottom is {den}, so $f_y = {key:frac}$. | correct | B14 |

## fluency-l3-second-partials

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0].skill` | find a first partial derivative | correct | B15 |
| `families[0].let.cn` | c*n | correct | B15 |
| `families[0].let.bp` | b*p | correct | B15 |
| `families[0].let.eq` | e*q | correct | B15 |
| `families[0].where` | n != q | correct | B15 |
| `families[0].prompt` | Take $f(x, y) = {c:c}x^{{{m}}}y^{{{n}}}{b:+c}x^{{{p}}}{e:+c}y^{{{q}}}$. Find $f_y$. | correct | B15 |
| `families[0].widget.answer` | {cn}x^{{{m}}}{mono(y; 1, n - 1)}{eq:+}{mono(y; 1, q - 1)} | correct | B15 |
| `families[0].wrong[0]` | slip x-term-differentiated = {cn}x^{{{m}}}{mono(y; 1, n - 1)}{bp:+}{mono(x; 1, p - 1)}{eq:+}{mono(y; 1, q - 1)} | correct | B15 |
| `families[0].wrong[1]` | slip x-factor-dropped = {mono(y; cn, n - 1)}{eq:+}{mono(y; 1, q - 1)} | correct | B15 |
| `families[0].solution[0]` | Hold $x$ fixed: $x^{{{m}}}$ is a constant factor and ${b:c}x^{{{p}}}$ is a constant, with $y$-derivative 0. | correct | B15 |
| `families[0].solution[1]` | Differentiate the powers of $y$: $f_y = {cn}x^{{{m}}}{mono(y; 1, n - 1)}{eq:+}{mono(y; 1, q - 1)}$. | correct | B15 |
| `families[1].skill` | evaluate a second partial at a point | correct | B15 |
| `families[1].let.c3` | 3*c | correct | B15 |
| `families[1].let.b4` | 4*b | correct | B15 |
| `families[1].let.c6` | 6*c | correct | B15 |
| `families[1].let.b12` | 12*b | correct | B15 |
| `families[1].let.t1` | 6*c*x0*y0^n | correct | B15 |
| `families[1].let.t2` | 12*b*x0^2 | correct | B15 |
| `families[1].let.key` | 6*c*x0*y0^n + 12*b*x0^2 | correct | B15 |
| `families[1].let.fx` | 3*c*x0^2*y0^n + 4*b*x0^3 | correct | B15 |
| `families[1].let.fxy` | 3*c*n*x0^2*y0^(n-1) | correct | B15 |
| `families[1].where` | key != fx, key != fxy, fx != fxy | correct | B15 |
| `families[1].prompt` | Take $f(x, y) = {c:c}x^3y^{{{n}}}{b:+c}x^4{e:+c}y^{{{q}}}$. What is $f_{{xx}}$ at $({x0}, {y0})$? | correct | B15 |
| `families[1].widget.answer` | {key} | correct | B15 |
| `families[1].wrong[0]` | slip stopped-at-first = {fx} | correct | B15 |
| `families[1].wrong[1]` | slip mixed-instead = {fxy} | correct | B15 |
| `families[1].solution[0]` | $f_x = {c3}x^2y^{{{n}}}{b4:+}x^3$, since ${e:c}y^{{{q}}}$ is a constant in $x$. | correct | B15 |
| `families[1].solution[1]` | $f_{{xx}} = {c6}xy^{{{n}}}{b12:+}x^2$. | correct | B15 |
| `families[1].solution[2]` | At $({x0}, {y0})$ the two terms are ${t1}$ and ${t2}$, so $f_{{xx}} = {key}$. | correct | B15 |
| `families[2].skill` | find a mixed partial derivative | correct | B15 |
| `families[2].let.cm` | c*m | correct | B15 |
| `families[2].let.cn` | c*n | correct | B15 |
| `families[2].let.bp` | b*p | correct | B15 |
| `families[2].let.eq` | e*q | correct | B15 |
| `families[2].let.cmn` | c*m*n | correct | B15 |
| `families[2].prompt` | Take $f(x, y) = {c:c}x^{{{m}}}y^{{{n}}}{b:+c}x^{{{p}}}{e:+c}y^{{{q}}}$. Find the mixed partial $f_{{xy}}$. | correct | B15 |
| `families[2].widget.answer` | {cmn}{mono(x; 1, m - 1)}{mono(y; 1, n - 1)} | correct | B15 |
| `families[2].wrong[0]` | slip product-of-partials = ({cm}{mono(x; 1, m - 1)}y^{{{n}}}{bp:+}{mono(x; 1, p - 1)})({cn}x^{{{m}}}{mono(y; 1, n - 1)}{eq:+}{mono(y; 1, q - 1)}) | correct | B15 |
| `families[2].wrong[1]` | slip pure-term-kept = {cmn}{mono(x; 1, m - 1)}{mono(y; 1, n - 1)}{bp:+}{mono(x; 1, p - 1)} | correct | B15 |
| `families[2].wrong[2]` | slip power-not-lowered = {cmn}{mono(x; 1, m - 1)}y^{{{n}}} | correct | B15 |
| `families[2].solution[0]` | $f_x = {cm}{mono(x; 1, m - 1)}y^{{{n}}}{bp:+}{mono(x; 1, p - 1)}$. | correct | B15 |
| `families[2].solution[1]` | Differentiate in $y$: the second term has no $y$, so $f_{{xy}} = {cmn}{mono(x; 1, m - 1)}{mono(y; 1, n - 1)}$. | correct | B15 |

## review-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | A book's P&L is $100\,\Delta A + 50\,\Delta B$ pounds, where $\Delta A$ and $\Delta B$ are the moves in two share prices. Each cell is one pair of ... | correct | B16 |
| `items[0].question` | Shade every cell on the £0 contour. | correct | B16 |
| `items[0].widget.answer` | r1c2, r3c3, r5c4 | correct | B16 |
| `items[0].feedback.correct` | Three cells, on a line through the centre: $\Delta B = -2\,\Delta A$. | correct | B16 |
| `items[0].feedback.generic` | Not quite right. A cell is on the £0 contour when $100\,\Delta A + 50\,\Delta B = 0$. | correct | B16 |
| `items[0].feedback.byKey.centre-only` | No move at all gives £0. So do pairs that cancel, such as A down £1 with B up £2. | correct | B16 |
| `items[0].feedback.byKey.wrong-diagonal` | On that diagonal B moves opposite to A by the same amount. A's move is worth twice as much, so those corners show −£100 and £100. | correct | B16 |
| `items[0].explain.text` | $100\,\Delta A + 50\,\Delta B = 0$ means $\Delta B = -2\,\Delta A$. On the grid that is $(-1, 2)$, $(0, 0)$ and $(1, -2)$. They lie on one straight... | correct | B16 |
| `items[1].prose` | Take $f(x, y) = x^2 + 4y^2$. | correct | B16 |
| `items[1].question` | The contour $f = 4$ crosses the positive $y$-axis at which $y$? | correct | B16 |
| `items[1].widget.answer` | 1 | correct | B16 |
| `items[1].widget.accept` | 1: on the axis $x = 0$, so $4y^2 = 4$. | correct | B16 |
| `items[1].widget.wrong[0]` | slip circle = 2 | correct | B16 |
| `items[1].widget.wrong[1]` | slip level = 4 | correct | B16 |
| `items[1].widget.wrong[2]` | slip quarter = 0.5 | correct | B16 |
| `items[1].feedback.correct` | $4y^2 = 4$ gives $y = 1$. | correct | B16 |
| `items[1].feedback.generic` | Not quite right. Put $x = 0$ and solve $4y^2 = 4$. | correct | B16 |
| `items[1].feedback.byKey.circle` | 2 is where it crosses the $x$-axis. Along $y$ the factor 4 squeezes the contour. | correct | B16 |
| `items[1].feedback.byKey.quarter` | You solved $4y = 2$. The equation is $4y^2 = 4$, so $y^2 = 1$. | correct | B16 |
| `items[1].explain.text` | On the $y$-axis $x = 0$, so the contour needs $4y^2 = 4$, giving $y = 1$. On the $x$-axis it needs $x^2 = 4$, giving $x = 2$. The contour is an ell... | correct | B16 |
| `items[2].prose` | Take $f(x, y) = x^3 + xy^2 + y$. | correct | B16 |
| `items[2].question` | Find $\dfrac{\partial f}{\partial y}$. | correct | B16 |
| `items[2].widget.answer` | 2xy+1 | correct | B16 |
| `items[2].widget.accept` | 2xy+1, 2*x*y+1, 1+2xy, 2yx+1, 1+2*x*y | correct | B16 |
| `items[2].widget.wrong[0]` | slip dropped-y = 2xy | correct | B16 |
| `items[2].widget.wrong[1]` | slip f-x = 3x^2+y^2 | correct | B16 |
| `items[2].widget.wrong[2]` | slip dropped-x = 2y+1 | correct | B16 |
| `items[2].feedback.correct` | $0 + 2xy + 1$. | correct | B16 |
| `items[2].feedback.generic` | Not quite right. Hold $x$ fixed: $x^3$ is a constant, $xy^2$ is $x$ times $y^2$. | correct | B16 |
| `items[2].feedback.byKey.dropped-y` | The last term $y$ has slope 1 in $y$. | correct | B16 |
| `items[2].feedback.byKey.f-x` | That is $f_x$. Here $y$ moves. | correct | B16 |
| `items[2].feedback.byKey.dropped-x` | $x$ is a constant factor in $xy^2$, so it stays: $2xy$. | correct | B16 |
| `items[2].explain.text` | With $x$ fixed, $x^3$ is a constant (slope 0), $xy^2$ has slope $2xy$, and $y$ has slope 1. So $f_y = 2xy + 1$. | correct | B16 |
| `items[3].prose` | Vega is $\frac{\partial V}{\partial \sigma}$, the option value's sensitivity to volatility. | correct | B16 |
| `items[3].question` | Tap the two cells you would use to estimate vega at $S = \text{£}100$, $\sigma = 0.20$. | correct | B16 |
| `items[3].widget.answer` | r1c1, r1c3 | correct | B16 |
| `items[3].feedback.correct` | Stay in the $S = 100$ row: $\frac{5.92 - 5.36}{0.02} = 28$ per unit of $\sigma$, or £0.28 per vol point. | correct | B16 |
| `items[3].feedback.generic` | Not quite right. Vega holds $S$ fixed and moves $\sigma$. | correct | B16 |
| `items[3].feedback.byKey.delta` | Those cells hold $\sigma$ and move $S$: that estimates delta. | correct | B16 |
| `items[3].feedback.byKey.diagonal` | Along the diagonal $S$ and $\sigma$ both move, mixing delta and vega. | correct | B16 |
| `items[3].explain.text` | A partial in $\sigma$ holds $S$ fixed, so both cells sit in the $S = 100$ row, either side of 0.20. Vega $\approx \frac{5.92 - 5.36}{0.21 - 0.19} =... | correct | B16 |
| `items[4].prose` | Take $f(x, y) = x^3 e^{2y}$. | correct | B16 |
| `items[4].question` | What is $f_{xy}$ at $(2, 0)$? | correct | B16 |
| `items[4].widget.answer` | 24 | correct | B16 |
| `items[4].widget.accept` | 24: $f_{xy} = 6x^2 e^{2y}$. | correct | B16 |
| `items[4].widget.wrong[0]` | slip product = 192 | correct | B16 |
| `items[4].widget.wrong[1]` | slip first = 12 | correct | B16 |
| `items[4].widget.wrong[2]` | slip f-yy = 32 | correct | B16 |
| `items[4].feedback.correct` | $f_x = 3x^2 e^{2y}$, then $f_{xy} = 6x^2 e^{2y} = 24$ at $(2, 0)$. | correct | B16 |
| `items[4].feedback.generic` | Not quite right. Find $f_x$, then differentiate it in $y$. | correct | B16 |
| `items[4].feedback.byKey.product` | 192 is $f_x \times f_y = 12 \times 16$. $f_{xy}$ differentiates $f_x$ again, in $y$. | correct | B16 |
| `items[4].feedback.byKey.first` | 12 is $f_x$ (and $f_{xx}$) at $(2, 0)$. Differentiate $f_x$ in $y$. | correct | B16 |
| `items[4].feedback.byKey.f-yy` | 32 is $f_{yy} = 4x^3 e^{2y}$. Mixed means one derivative in each. | correct | B16 |
| `items[4].explain.text` | $f_x = 3x^2 e^{2y}$. Its $y$-derivative brings down a 2 from the exponent: $6x^2 e^{2y}$, which is 24 at $(2, 0)$. From $f_y = 2x^3 e^{2y}$ in $x$:... | correct | B16 |
| `items[5].prose` | At some point, a function has $f_{xy} = 3$. | correct | B16 |
| `items[5].question` | Which statement follows? | correct | B16 |
| `items[5].widget.options[0]` | option right (key): If $y$ rises by 0.1, the slope in $x$ rises by about 0.3 | correct | B16 |
| `items[5].widget.options[1]` | option value: If $x$ and $y$ both rise by 1, $f$ rises by about 3 | correct | B16 |
| `items[5].widget.options[1].why` | That reads $f_{xy}$ as a change in $f$. It is a change in a slope. | correct | B16 |
| `items[5].widget.options[2]` | option product: $f_x \times f_y = 3$ there | correct | B16 |
| `items[5].widget.options[2].why` | $f_{xy}$ is a second derivative, not the product of the first partials. | correct | B16 |
| `items[5].widget.options[3]` | option pure: If $y$ rises by 0.1, the slope in $y$ rises by about 0.3 | correct | B16 |
| `items[5].widget.options[3].why` | That is $f_{yy}$: how the $y$-slope changes with $y$. | correct | B16 |
| `items[5].feedback.correct` | $f_{xy}$ is the rate the $x$-slope changes as $y$ moves. | correct | B16 |
| `items[5].feedback.generic` | Not quite right. $f_{xy}$ differentiates $f_x$ with respect to $y$. | correct | B16 |
| `items[5].explain.text` | $f_{xy} = \frac{\partial}{\partial y} f_x$, so $f_x$ changes by about $3 \times 0.1 = 0.3$ when $y$ rises by 0.1. Since $f_{yx} = f_{xy}$, the $y$-... | correct | B16 |
| `items[6].prose` | Take $f(x, y) = x e^{y}$ along $x = 2 + t$, $y = 3t$. | correct | B16 |
| `items[6].question` | What is $\dfrac{df}{dt}$ at $t = 0$? | correct | B16 |
| `items[6].widget.answer` | 7 | correct | B16 |
| `items[6].widget.accept` | 7: $e^0 \times 1 + 2e^0 \times 3$. | correct | B16 |
| `items[6].widget.wrong[0]` | slip x-only = 1 | correct | B16 |
| `items[6].widget.wrong[1]` | slip y-only = 6 | correct | B16 |
| `items[6].widget.wrong[2]` | slip rates = 4 | correct | B16 |
| `items[6].widget.wrong[3]` | slip partials = 3 | correct | B16 |
| `items[6].feedback.correct` | $f_x x' + f_y y' = 1 \times 1 + 2 \times 3 = 7$. | correct | B16 |
| `items[6].feedback.generic` | Not quite right. At $t = 0$, $(x, y) = (2, 0)$, $f_x = e^y = 1$, $f_y = xe^y = 2$, $x' = 1$, $y' = 3$. | correct | B16 |
| `items[6].feedback.byKey.x-only` | 1 is the $x$ part. $y$ moves at rate 3 as well. | correct | B16 |
| `items[6].feedback.byKey.y-only` | 6 is the $y$ part. Add the $x$ part, 1. | correct | B16 |
| `items[6].feedback.byKey.rates` | 4 is $x' + y'$. Weight each rate by its partial. | correct | B16 |
| `items[6].feedback.byKey.partials` | 3 is $f_x + f_y$. Multiply each by its rate. | correct | B16 |
| `items[6].explain.text` | At $(2, 0)$: $f_x = 1$ and $f_y = 2$, with $x' = 1$ and $y' = 3$. So $\frac{df}{dt} = 1 + 6 = 7$. Substituting, $(2 + t)e^{3t}$ has derivative $1 +... | correct | B16 |
| `items[7].prose` | A point moves along a path that stays on one contour of $f(x, y)$ the whole time. | correct | B16 |
| `items[7].question` | Which must be true at every instant? | correct | B16 |
| `items[7].widget.options[0]` | option right (key): $f_x\,x'(t) + f_y\,y'(t) = 0$ | correct | B16 |
| `items[7].widget.options[1]` | option still: $x'(t) = y'(t) = 0$ | correct | B16 |
| `items[7].widget.options[1].why` | The point is moving, so its rates are not both 0. It is $f$ that stays fixed. | correct | B16 |
| `items[7].widget.options[2]` | option flat: $f_x = f_y = 0$ | correct | B16 |
| `items[7].widget.options[2].why` | The surface need not be flat. On a circle of $x^2 + y^2$ the partials are not 0, yet the two parts cancel. | correct | B16 |
| `items[7].widget.options[3]` | option rates: $x'(t) + y'(t) = 0$ | correct | B16 |
| `items[7].widget.options[3].why` | The rates need not cancel each other. The weighted parts $f_x x'$ and $f_y y'$ cancel. | correct | B16 |
| `items[7].feedback.correct` | $f$ is constant along the path, so $\frac{df}{dt} = 0$, and the chain rule spells that out. | correct | B16 |
| `items[7].feedback.generic` | Not quite right. What is $\frac{df}{dt}$ when $f$ never changes? | correct | B16 |
| `items[7].explain.text` | On one contour $f$ never changes, so $\frac{df}{dt} = 0$. By the chain rule that is $f_x x' + f_y y' = 0$. The two parts cancel, as at $(1.2, 1.6)$... | correct | B16 |
| `items[8].prose` | A bond book is worth $V = 500{,}000\,e^{-2y_1} + 300{,}000\,e^{-10y_2}$ pounds, with $y_1 = 0.03$ and $y_2 = 0.04$. Today the 2-year yield $y_1$ ri... | correct | B16 |
| `items[8].question` | At what rate is $V$ changing, in pounds per day? | correct | B16 |
| `items[8].widget.answer` | 12.74 | correct | B16 |
| `items[8].widget.accept` | About £12.74 per day: $-941{,}765 \times 0.0002 + (-2{,}010{,}960) \times (-0.0001)$. | correct | B16 |
| `items[8].widget.wrong[0]` | slip y1-only = -188.35 | correct | B16 |
| `items[8].widget.wrong[1]` | slip y2-only = 201.1 | correct | B16 |
| `items[8].widget.wrong[2]` | slip sign = -389.45 | correct | B16 |
| `items[8].feedback.correct` | $-188.35 + 201.10 \approx \text{£}12.74$ per day. | correct | B16 |
| `items[8].feedback.generic` | Not quite right. Find both partials, then use $V_{y_1}\,y_1' + V_{y_2}\,y_2'$ with rates in decimals. | correct | B16 |
| `items[8].feedback.byKey.y1-only` | $-\text{£}188.35$ is the 2-year part alone. The falling 10-year yield adds value. | correct | B16 |
| `items[8].feedback.byKey.y2-only` | £201.10 is the 10-year part alone. The rising 2-year yield costs £188.35. | correct | B16 |
| `items[8].feedback.byKey.sign` | $y_2$ is falling, so $y_2' = -0.0001$, and $V_{y_2}$ is negative: that part is a gain. | correct | B16 |
| `items[8].explain.text` | $V_{y_1} = -1{,}000{,}000\,e^{-0.06} \approx -941{,}765$ and $V_{y_2} = -3{,}000{,}000\,e^{-0.4} \approx -2{,}010{,}960$. With $y_1' = 0.0002$ and ... | correct | B16 |

## homework-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Take $f(x, y) = \ln(xy^2)$ for $x > 0$ and $y > 0$. | correct | B17 |
| `items[0].question` | Find $\dfrac{\partial f}{\partial y}$ in its simplest form. | correct | B17 |
| `items[0].widget.answer` | \frac{2}{y} | correct | B17 |
| `items[0].widget.accept` | 2/y, 2y^(-1), 2*y^(-1), 2/(y) | correct | B17 |
| `items[0].widget.wrong[0]` | slip no-chain = \frac{1}{xy^2} | correct | B17 |
| `items[0].widget.wrong[1]` | slip no-power = \frac{1}{y} | correct | B17 |
| `items[0].widget.wrong[2]` | slip f-x = \frac{1}{x} | correct | B17 |
| `items[0].feedback.correct` | $\frac{2xy}{xy^2} = \frac{2}{y}$, or from $\ln x + 2\ln y$ directly. | correct | B17 |
| `items[0].feedback.generic` | Not quite right. Write $\ln(xy^2) = \ln x + 2\ln y$ first. | correct | B17 |
| `items[0].feedback.byKey.no-chain` | You stopped at $\frac{1}{u}$ with $u = xy^2$. Multiply by $\frac{\partial u}{\partial y} = 2xy$. | correct | B17 |
| `items[0].feedback.byKey.no-power` | The square on $y$ gives $2\ln y$, so the slope is $\frac{2}{y}$. | correct | B17 |
| `items[0].feedback.byKey.f-x` | That is $f_x$. Here $y$ moves. | correct | B17 |
| `items[0].explain.text` | $\ln(xy^2) = \ln x + 2\ln y$. With $x$ fixed, $\ln x$ is a constant, so $f_y = \frac{2}{y}$. The value of $x$ does not affect this slope at all. | correct | B17 |
| `items[1].prose` | Find $f_x(a, b)$ for $f(x, y) = x^2 y$ straight from the definition. | correct | B17 |
| `items[1].question` | Put the lines in order. | correct | B17 |
| `items[1].widget.lines[0]` | line def: $f_x(a, b) = \displaystyle\lim_{h \to 0} \frac{f(a + h, b) - f(a, b)}{h}$, move $x$ only | correct | B17 |
| `items[1].widget.lines[1]` | line sub: $= \displaystyle\lim_{h \to 0} \frac{(a + h)^2 b - a^2 b}{h}$, put in $f = x^2 y$ with $y = b$ | correct | B17 |
| `items[1].widget.lines[2]` | line expand: $= \displaystyle\lim_{h \to 0} \frac{(2ah + h^2)\,b}{h}$, expand $(a + h)^2$: the $a^2 b$ terms cancel | correct | B17 |
| `items[1].widget.lines[3]` | line cancel: $= \displaystyle\lim_{h \to 0} (2a + h)\,b$, divide by $h \neq 0$ | correct | B17 |
| `items[1].widget.lines[4]` | line limit: $= 2ab$, let $h \to 0$ | correct | B17 |
| `items[1].widget.answer` | def, sub, expand, cancel, limit | correct | B17 |
| `items[1].feedback.correct` | $f_x(a, b) = 2ab$, matching the rule $\frac{\partial}{\partial x}(x^2 y) = 2xy$. | correct | B17 |
| `items[1].feedback.generic` | Not quite right. Definition, substitute, expand, cancel $h$, then the limit. | correct | B17 |
| `items[1].feedback.byKey.cancel` | You can divide by $h$ only once every term on top carries an $h$. | correct | B17 |
| `items[1].feedback.byKey.limit` | The limit is last, when no $h$ is left on the bottom. | correct | B17 |
| `items[1].explain.text` | Only $x$ moved, so $b$ rode along as a constant factor. Expanding left $(2ah + h^2)b$, and cancelling $h$ left $(2a + h)b \to 2ab$. The shortcut $2... | correct | B17 |
| `items[2].prose` | Take $f(x, y) = x\,e^{xy}$. | correct | B17 |
| `items[2].question` | Find the mixed partial $f_{xy}$. | correct | B17 |
| `items[2].widget.answer` | (2x+x^2y)e^{xy} | correct | B17 |
| `items[2].widget.accept` | 2xe^{xy}+x^2ye^{xy}, x(2+xy)e^{xy}, (2x+x^2y)e^(xy), (2*x+x^2*y)*e^(x*y), 2x*e^(xy)+x^2*y*e^(xy), x(2+xy)e^(xy), e^(xy)(2x+x^2y) | correct | B17 |
| `items[2].widget.wrong[0]` | slip f-x = (1+xy)e^{xy} | correct | B17 |
| `items[2].widget.wrong[1]` | slip f-y = x^2e^{xy} | correct | B17 |
| `items[2].widget.wrong[2]` | slip f-xx = (2y+xy^2)e^{xy} | correct | B17 |
| `items[2].widget.wrong[3]` | slip no-product = x^2ye^{xy} | correct | B17 |
| `items[2].feedback.correct` | $f_x = (1 + xy)e^{xy}$, then $f_{xy} = (2x + x^2y)e^{xy}$. From $f_y = x^2 e^{xy}$ in $x$: the same. | correct | B17 |
| `items[2].feedback.generic` | Not quite right. Find $f_x$ with the product rule, then differentiate it in $y$ with the product rule again. | correct | B17 |
| `items[2].feedback.byKey.f-x` | That is $f_x$. Differentiate it once more, in $y$. | correct | B17 |
| `items[2].feedback.byKey.f-y` | That is $f_y$. Differentiate it once more, in $x$, to check the mixed partial. | correct | B17 |
| `items[2].feedback.byKey.f-xx` | That is $f_{xx}$: both derivatives were in $x$. | correct | B17 |
| `items[2].feedback.byKey.no-product` | You differentiated only $e^{xy}$ in the last step. The factor $(1 + xy)$ moves with $y$ too. | correct | B17 |
| `items[2].explain.text` | $f_x = e^{xy} + xy\,e^{xy} = (1 + xy)e^{xy}$. In $y$: $x\,e^{xy} + (1 + xy)\,x\,e^{xy} = (2x + x^2y)e^{xy}$. The other order, from $f_y = x^2 e^{xy... | correct | B17 |
| `items[3].prose` | Two assets have volatilities $\sigma_1 = 0.2$ and $\sigma_2 = 0.3$ and correlation $\rho = 0.5$. With weights $w_1$, $w_2$ the portfolio variance i... | correct | B17 |
| `items[3].question` | At $w_1 = w_2 = 0.5$, what is $\dfrac{\partial V}{\partial w_2}$? | correct | B17 |
| `items[3].widget.answer` | 0.12 | correct | B17 |
| `items[3].widget.accept` | 0.12: $2(0.5)(0.09) + 2(0.5)(0.5)(0.2)(0.3) = 0.09 + 0.03$. | correct | B17 |
| `items[3].widget.wrong[0]` | slip no-cross = 0.09 | correct | B17 |
| `items[3].widget.wrong[1]` | slip w1 = 0.07 | correct | B17 |
| `items[3].widget.wrong[2]` | slip half-cross = 0.105 | correct | B17 |
| `items[3].widget.wrong[3]` | slip variance = 0.0475 | correct | B17 |
| `items[3].feedback.correct` | $0.09 + 0.03 = 0.12$. | correct | B17 |
| `items[3].feedback.generic` | Not quite right. Hold $w_1$ fixed: differentiate $w_2^2\sigma_2^2$ and the cross term $2w_1w_2\rho\sigma_1\sigma_2$. | correct | B17 |
| `items[3].feedback.byKey.no-cross` | You dropped the cross term. It contains $w_2$, adding $2w_1\rho\sigma_1\sigma_2 = 0.03$. | correct | B17 |
| `items[3].feedback.byKey.w1` | 0.07 is $\frac{\partial V}{\partial w_1}$. Here $w_2$ moves. | correct | B17 |
| `items[3].feedback.byKey.half-cross` | The cross term's slope in $w_2$ is $2w_1\rho\sigma_1\sigma_2$: keep the 2. | correct | B17 |
| `items[3].feedback.byKey.variance` | 0.0475 is the variance $V$ itself. The question asks for its slope in $w_2$. | correct | B17 |
| `items[3].explain.text` | With $w_1$ held, $\frac{\partial V}{\partial w_2} = 2w_2\sigma_2^2 + 2w_1\rho\sigma_1\sigma_2 = 0.09 + 0.03 = 0.12$. The same for $w_1$ gives $0.04... | correct | B17 |
| `items[4].prose` | Take $f(x, y) = xy^2$ along $x = e^t$, $y = t$. | correct | B17 |
| `items[4].question` | Write $\dfrac{df}{dt}$ as a function of $t$. | correct | B17 |
| `items[4].widget.answer` | (t^2+2t)e^t | correct | B17 |
| `items[4].widget.accept` | t^2e^t+2te^t, e^t(t^2+2t), te^t(t+2), (t^2+2t)e^t, (t^2+2*t)*e^t, t^2*e^t+2*t*e^t, e^t*(t^2+2*t), t*e^t*(t+2), (t^2+2t)exp(t) | correct | B17 |
| `items[4].widget.wrong[0]` | slip x-only = t^2e^t | correct | B17 |
| `items[4].widget.wrong[1]` | slip y-only = 2te^t | correct | B17 |
| `items[4].widget.wrong[2]` | slip product = 2t^3e^{2t} | correct | B17 |
| `items[4].feedback.correct` | $y^2 e^t + 2xy \cdot 1 = t^2 e^t + 2t\,e^t$. | correct | B17 |
| `items[4].feedback.generic` | Not quite right. Use $f_x x' + f_y y'$ with $f_x = y^2$, $f_y = 2xy$, $x' = e^t$, $y' = 1$. | correct | B17 |
| `items[4].feedback.byKey.x-only` | That is only the $x$ part, $y^2 e^t$. $y$ moves at rate 1 too. | correct | B17 |
| `items[4].feedback.byKey.y-only` | That is only the $y$ part, $2xy$. Add $y^2 x'$. | correct | B17 |
| `items[4].feedback.byKey.product` | You multiplied the two parts. They add. | correct | B17 |
| `items[4].explain.text` | $f_x x' = t^2 \cdot e^t$ and $f_y y' = 2e^t t \cdot 1$. So $\frac{df}{dt} = (t^2 + 2t)e^t$. Check: $f = t^2 e^t$, and the product rule gives the same. | correct | B17 |
| `items[5].prose` | Take $f(x, y) = e^{-(x^2 + y^2)}$, a bump with its top at the origin. | correct | B17 |
| `items[5].question` | Which contour has no points at all? | correct | B17 |
| `items[5].widget.options[0]` | option two (key): $f = 2$ | correct | B17 |
| `items[5].widget.options[1]` | option one: $f = 1$ | correct | B17 |
| `items[5].widget.options[1].why` | $f = 1$ at the origin, where $x^2 + y^2 = 0$. That contour is a single point. | correct | B17 |
| `items[5].widget.options[2]` | option half: $f = 0.5$ | correct | B17 |
| `items[5].widget.options[2].why` | $x^2 + y^2 = \ln 2$ is a circle of radius about 0.83. | correct | B17 |
| `items[5].widget.options[3]` | option small: $f = 0.01$ | correct | B17 |
| `items[5].widget.options[3].why` | $x^2 + y^2 = \ln 100$ is a circle of radius about 2.15. Small levels are far out, not missing. | correct | B17 |
| `items[5].feedback.correct` | $f \le e^0 = 1$ everywhere, so no input reaches 2. | correct | B17 |
| `items[5].feedback.generic` | Not quite right. What is the largest value $f$ ever takes? | correct | B17 |
| `items[5].explain.text` | The exponent $-(x^2 + y^2)$ is at most 0, so $f \le 1$. The contour $f = 1$ is the origin alone, and any level above 1 is empty. Levels between 0 a... | correct | B17 |
| `items[6].prose` | Take $f(x, y) = x^2 y - y^3$ along the unit circle $x = \cos t$, $y = \sin t$. | correct | B17 |
| `items[6].question` | What is $\dfrac{df}{dt}$ at $t = \dfrac{\pi}{4}$? Give 3 decimal places. | correct | B17 |
| `items[6].widget.answer` | -1.4142 | correct | B17 |
| `items[6].widget.accept` | $-\sqrt{2} \approx -1.414$: $1 \times (-\tfrac{\sqrt2}{2}) + (-1) \times \tfrac{\sqrt2}{2}$. | correct | B17 |
| `items[6].widget.wrong[0]` | slip x-only = -0.7071 | correct | B17 |
| `items[6].widget.wrong[1]` | slip y-only-sign = 0.7071 | correct | B17 |
| `items[6].widget.wrong[2]` | slip sign = 1.4142 | correct | B17 |
| `items[6].feedback.correct` | $f_x = 1$, $f_y = -1$, $x' = -\tfrac{\sqrt2}{2}$, $y' = \tfrac{\sqrt2}{2}$: total $-\sqrt{2}$. | correct | B17 |
| `items[6].feedback.generic` | Not quite right. At $t = \frac{\pi}{4}$, $x = y = \frac{\sqrt2}{2}$. Find $f_x = 2xy$ and $f_y = x^2 - 3y^2$ there. | correct | B17 |
| `items[6].feedback.byKey.x-only` | That is only the $x$ part. The $y$ part, $f_y\,y' = (-1)(0.707)$, adds the same again. | correct | B17 |
| `items[6].feedback.byKey.y-only-sign` | Check $f_y = x^2 - 3y^2 = 0.5 - 1.5 = -1$: it is negative. | correct | B17 |
| `items[6].feedback.byKey.sign` | $x' = -\sin t$ is negative here, and so is $f_y$. Both parts are negative. | correct | B17 |
| `items[6].explain.text` | At $t = \frac{\pi}{4}$, $x = y = \frac{\sqrt2}{2}$, so $f_x = 2xy = 1$ and $f_y = x^2 - 3y^2 = -1$. With $x' = -\frac{\sqrt2}{2}$ and $y' = \frac{\... | correct | B17 |
| `items[7].prompt` | Near spot £100 and volatility 0.20, a desk models its option book as $$\begin{aligned} V(S, \sigma) = 1000\big[&0.5(S - 100) \\ &+ 0.02(S - 100)^2 ... | correct | B17 |
| `items[7].model#1` | **(a) First partials.** Holding $\sigma$ fixed and differentiating in $S$: | correct | B17 |
| `items[7].model#2` | Holding $S$ fixed and differentiating in $\sigma$: | correct | B17 |
| `items[7].model#3` | At $S = 100$, $\sigma = 0.2$: $\Delta = 500$ pounds per £1 of spot, and $\mathcal{V} = 30{,}000$ per unit of $\sigma$, which is £300 per vol point. | correct | B17 |
| `items[7].model#4` | **(b) Second partials.** $V_{SS} = \frac{\partial}{\partial S}\Delta = 1000 \times 0.04 = 40$. $V_{\sigma\sigma} = \frac{\partial}{\partial \sigma}... | correct | B17 |
| `items[7].model#5` | **(c) Chain rule.** Along the scenario $S'(t) = 2$ and $\sigma'(t) = -0.01$, so | correct | B17 |
| `items[7].model#6` | At $t = 0$: $500 \times 2 + 30{,}000 \times (-0.01) = 1000 - 300 = 700$ pounds per day. | correct | B17 |
| `items[7].model#7` | At $t = 1$: $S = 102$, $\sigma = 0.19$. Then $\Delta = 1000[0.5 + 0.08 + 0.02] = 600$ and $\mathcal{V} = 1000[30 - 4] = 26{,}000$. So $\frac{dV}{dt... | correct | B17 |
| `items[7].model#8` | **(d) Substitution.** Put $S - 100 = 2t$ and $\sigma - 0.2 = -0.01t$: | correct | B17 |
| `items[7].model#9` | So $V'(t) = 700 + 240t$: 700 at $t = 0$ and 940 at $t = 1$, matching (c). | correct | B17 |
| `items[7].model#10` | **(e) Meaning of vanna.** Vanna is $-2000$: each unit rise in $\sigma$ lowers delta by 2000, so one vol point lowers delta by 20 pounds per £1 of s... | correct | B17 |
| `items[7].rubric[0]` | (1) Finds $\Delta = 1000[0.5 + 0.04(S - 100) - 2(\sigma - 0.2)]$ by holding $\sigma$ fixed. | correct | B17 |
| `items[7].rubric[1]` | (1) Finds $\mathcal{V} = 1000[30 - 2(S - 100)]$ and evaluates $\Delta = 500$, $\mathcal{V} = 30{,}000$ at the base point. | correct | B17 |
| `items[7].rubric[2]` | (1) Finds gamma $= 40$ and $V_{\sigma\sigma} = 0$. | correct | B17 |
| `items[7].rubric[3]` | (2) Computes vanna in both orders, gets $-2000$ each time, and notes they agree. | correct | B17 |
| `items[7].rubric[4]` | (1) Writes the chain rule $\frac{dV}{dt} = \Delta S' + \mathcal{V}\sigma'$ with $S' = 2$ and $\sigma' = -0.01$. | correct | B17 |
| `items[7].rubric[5]` | (1) Gets 700 at $t = 0$. | correct | B17 |
| `items[7].rubric[6]` | (1) Recomputes $\Delta = 600$ and $\mathcal{V} = 26{,}000$ at $t = 1$ and gets 940. | correct | B17 |
| `items[7].rubric[7]` | (1) Substitutes to get $V(t) = 1000(0.7t + 0.12t^2)$ and confirms both rates. | correct | B17 |
| `items[7].rubric[8]` | (1) Explains that negative vanna means delta falls as volatility rises. | correct | B17 |

## problems-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Take the stretched bowl $f(x, y) = 9x^2 + y^2$. Its contours are ellipses about the origin, and we follow the one through $(1, 3)$. | correct | B18 |
| `items[0].parts[0].question` | Which contour passes through $(1, 3)$? Give the level $c$ with $f(1, 3) = c$. | correct | B18 |
| `items[0].parts[0].widget.answer` | 18 | correct | B18 |
| `items[0].parts[0].widget.wrong[0]` | slip no-square-y = 12 | correct | B18 |
| `items[0].parts[0].widget.wrong[1]` | slip swapped = 82 | correct | B18 |
| `items[0].parts[0].feedback.correct` | $f(1, 3) = 9 + 3^2 = 18$, so the point sits on the contour $f = 18$. | correct | B18 |
| `items[0].parts[0].feedback.generic` | Not quite. Put $x = 1$ and $y = 3$ into $9x^2 + y^2$. | correct | B18 |
| `items[0].parts[0].feedback.byKey.no-square-y` | You added $y = 3$ without squaring it. The term is $y^2 = 9$. | correct | B18 |
| `items[0].parts[0].feedback.byKey.swapped` | You put the 9 on $y^2$. Here the 9 multiplies $x^2$, so $f(1, 3) = 9 + 9$. | correct | B18 |
| `items[0].parts[0].explain.text` | A contour is every input with the same output. $f(1, 3) = 9 + 9 = 18$, so $(1, 3)$ lies on $f = 18$. | correct | B18 |
| `items[0].parts[1].question` | Find the two partial derivatives at $(1, 3)$. Give $(f_x, f_y)$ as a pair. | correct | B18 |
| `items[0].parts[1].widget.answer` | (18, 6) | correct | B18 |
| `items[0].parts[1].widget.accept` | (18,6) | correct | B18 |
| `items[0].parts[1].widget.wrong[0]` | slip no-power = (9, 3) | correct | B18 |
| `items[0].parts[1].widget.wrong[1]` | slip swapped = (6, 18) | correct | B18 |
| `items[0].parts[1].feedback.correct` | $f_x = 18x$ and $f_y = 2y$, so at $(1, 3)$ the pair is $(18, 6)$. | correct | B18 |
| `items[0].parts[1].feedback.generic` | Not quite. Hold $y$ fixed to find $f_x$, then hold $x$ fixed to find $f_y$. | correct | B18 |
| `items[0].parts[1].feedback.byKey.no-power` | You dropped the factor from each power. $\frac{\partial}{\partial x}(9x^2) = 18x$ and $\frac{\partial}{\partial y}(y^2) = 2y$. | correct | B18 |
| `items[0].parts[1].feedback.byKey.swapped` | You swapped the two. $f_x$ comes from $9x^2$, which gives 18 at $x = 1$. | correct | B18 |
| `items[0].parts[1].feedback.byKey.length` | Give two numbers in brackets: $f_x$ first, then $f_y$. | correct | B18 |
| `items[0].parts[1].explain.text` | Holding $y$ fixed, $9x^2$ gives $f_x = 18x = 18$. Holding $x$ fixed, $y^2$ gives $f_y = 2y = 6$. | correct | B18 |
| `items[0].parts[2].question` | A point moves along the contour $f = 18$ from $(1, 3)$, so $f$ stays fixed. Using $f_x = 18$ and $f_y = 6$ there, $x$ rises by 0.01. About how much... | correct | B18 |
| `items[0].parts[2].widget.answer` | -0.03 | correct | B18 |
| `items[0].parts[2].widget.accept` | -0.03 (the exact change, -0.0303, is accepted too) | correct | B18 |
| `items[0].parts[2].widget.wrong[0]` | slip sign = 0.03 | correct | B18 |
| `items[0].parts[2].widget.wrong[1]` | slip inverted = -0.0033 | correct | B18 |
| `items[0].parts[2].widget.wrong[2]` | slip rise-in-f = 0.18 | correct | B18 |
| `items[0].parts[2].feedback.correct` | Along a contour $f_x\,\Delta x + f_y\,\Delta y = 0$. So $0.18 + 6\,\Delta y = 0$, and $\Delta y = -0.03$. | correct | B18 |
| `items[0].parts[2].feedback.generic` | Not quite. On a contour the change from $x$ and the change from $y$ must cancel. | correct | B18 |
| `items[0].parts[2].feedback.byKey.sign` | The size is right but the sign is wrong. As $x$ rises $f$ rises, so $y$ must fall to keep $f = 18$. | correct | B18 |
| `items[0].parts[2].feedback.byKey.inverted` | You divided the wrong way round. Solve $18 \times 0.01 + 6\,\Delta y = 0$ for $\Delta y$. | correct | B18 |
| `items[0].parts[2].feedback.byKey.rise-in-f` | That is how much $f$ would rise with $y$ held fixed. On the contour, $y$ moves to cancel it. | correct | B18 |
| `items[0].parts[2].explain.text` | Along a contour $\frac{df}{dt} = f_x x'(t) + f_y y'(t) = 0$, so the two parts cancel. With $\Delta x = 0.01$, $6\,\Delta y = -0.18$ and $\Delta y =... | correct | B18 |
| `items[0].parts[3].question` | Now find the exact change. Using $f = 18$ from part 1, find the $y > 0$ with $9(1.01)^2 + y^2 = 18$, then subtract 3. Give a decimal to 4 places. | correct | B18 |
| `items[0].parts[3].widget.answer` | -0.0303 | correct | B18 |
| `items[0].parts[3].widget.wrong[0]` | slip linear = -0.03 | correct | B18 |
| `items[0].parts[3].widget.wrong[1]` | slip no-square = -0.015 | correct | B18 |
| `items[0].parts[3].widget.wrong[2]` | slip no-subtract = 2.9697 | correct | B18 |
| `items[0].parts[3].widget.wrong[3]` | slip sign = 0.0303 | correct | B18 |
| `items[0].parts[3].feedback.correct` | $y^2 = 18 - 9.1809 = 8.8191$, so $y \approx 2.9697$ and the change is $-0.0303$. Part 3's estimate of $-0.03$ was close. | correct | B18 |
| `items[0].parts[3].feedback.generic` | Not quite. Square 1.01 first, then solve for $y$ and compare it with 3. | correct | B18 |
| `items[0].parts[3].feedback.byKey.linear` | That is part 3's estimate. The contour bends a little, so the exact change is $-0.0303$. | correct | B18 |
| `items[0].parts[3].feedback.byKey.no-square` | You used $9 \times 1.01$. The term is $9x^2$, so square 1.01 first: $9 \times 1.0201 = 9.1809$. | correct | B18 |
| `items[0].parts[3].feedback.byKey.no-subtract` | That is the new $y$. The question asks for the change, $2.9697 - 3$. | correct | B18 |
| `items[0].parts[3].feedback.byKey.sign` | y falls from 3 to 2.9697, so the change is 2.9697 − 3, which is negative. A positive 0.0303 takes 3 − 2.9697, the wrong way round. | correct | B18 |
| `items[0].parts[3].explain.text` | $y = \sqrt{18 - 9.1809} = \sqrt{8.8191} \approx 2.9697$, a change of $-0.0303$. The slope estimate missed by only 0.0003, because the step was small. | correct | B18 |
| `items[1].prose` | Take $f(x, y) = x^3 y - 2xy^2$. We find its mixed partial both ways, then use it to predict a slope. | correct | B18 |
| `items[1].parts[0].question` | Find $f_x$. | correct | B18 |
| `items[1].parts[0].widget.answer` | 3x^2y-2y^2 | correct | B18 |
| `items[1].parts[0].widget.accept` | y(3x^2-2y) | correct | B18 |
| `items[1].parts[0].widget.wrong[0]` | slip wrong-variable = x^3-4xy | correct | B18 |
| `items[1].parts[0].widget.wrong[1]` | slip both = 3x^2y+x^3-2y^2-4xy | correct | B18 |
| `items[1].parts[0].feedback.correct` | Holding $y$ fixed, $x^3 y$ gives $3x^2 y$ and $2xy^2$ gives $2y^2$. So $f_x = 3x^2 y - 2y^2$. | correct | B18 |
| `items[1].parts[0].feedback.generic` | Not quite. Treat $y$ as a constant number and differentiate each term in $x$. | correct | B18 |
| `items[1].parts[0].feedback.byKey.wrong-variable` | That is $f_y$: you differentiated in $y$. For $f_x$, hold $y$ fixed. | correct | B18 |
| `items[1].parts[0].feedback.byKey.both` | You let $y$ move as well. For $f_x$ every $y$ is a constant, so $x^3 y$ gives only $3x^2 y$. | correct | B18 |
| `items[1].parts[0].explain.text` | Each $y$ is a constant: $\frac{\partial}{\partial x}(x^3 y) = 3x^2 y$ and $\frac{\partial}{\partial x}(2xy^2) = 2y^2$. So $f_x = 3x^2 y - 2y^2$. | correct | B18 |
| `items[1].parts[1].question` | Using $f_x = 3x^2 y - 2y^2$ from part 1, find the mixed partial $f_{xy}$. | correct | B18 |
| `items[1].parts[1].widget.answer` | 3x^2-4y | correct | B18 |
| `items[1].parts[1].widget.accept` | 3x^2-4y, -4y+3x^2 | correct | B18 |
| `items[1].parts[1].widget.wrong[0]` | slip xx = 6xy | correct | B18 |
| `items[1].parts[1].widget.wrong[1]` | slip carried-both = 3x^2-4y-4x | correct | B18 |
| `items[1].parts[1].feedback.correct` | Differentiate $f_x$ in $y$: $3x^2 y$ gives $3x^2$ and $2y^2$ gives $4y$. So $f_{xy} = 3x^2 - 4y$. | correct | B18 |
| `items[1].parts[1].feedback.generic` | Not quite. Now hold $x$ fixed and differentiate $f_x$ in $y$. | correct | B18 |
| `items[1].parts[1].feedback.byKey.xx` | That is $f_{xx}$: you differentiated in $x$ again. The mixed partial differentiates $f_x$ in $y$. | correct | B18 |
| `items[1].parts[1].feedback.byKey.carried-both` | You started from part 1's slip, which kept the terms $x^3 - 4xy$. From $f_x = 3x^2 y - 2y^2$ you get $3x^2 - 4y$. | correct | B18 |
| `items[1].parts[1].explain.text` | $f_{xy} = \frac{\partial}{\partial y}(3x^2 y - 2y^2) = 3x^2 - 4y$. It says how the $x$-slope changes as $y$ moves. | correct | B18 |
| `items[1].parts[2].question` | Now go the other way. Find $f_y$, differentiate it in $x$, and evaluate $f_{yx}$ at $(2, 1)$. | correct | B18 |
| `items[1].parts[2].widget.answer` | 8 | correct | B18 |
| `items[1].parts[2].widget.wrong[0]` | slip xx = 12 | correct | B18 |
| `items[1].parts[2].widget.wrong[1]` | slip yy = -8 | correct | B18 |
| `items[1].parts[2].widget.wrong[2]` | slip sign = 16 | correct | B18 |
| `items[1].parts[2].feedback.correct` | $f_y = x^3 - 4xy$, so $f_{yx} = 3x^2 - 4y$, which is $12 - 4 = 8$ at $(2, 1)$. It matches $f_{xy}$, as it must for a polynomial. | correct | B18 |
| `items[1].parts[2].feedback.generic` | Not quite. Find $f_y$ first, then differentiate that in $x$. | correct | B18 |
| `items[1].parts[2].feedback.byKey.xx` | That is $f_{xx} = 6xy$ at $(2, 1)$. The question wants $f_y$ differentiated in $x$. | correct | B18 |
| `items[1].parts[2].feedback.byKey.yy` | That is $f_{yy} = -4x$ at $(2, 1)$. Differentiate $f_y$ in $x$, not in $y$. | correct | B18 |
| `items[1].parts[2].feedback.byKey.sign` | You added the $4y$. The $x$-derivative of $x^3 - 4xy$ is $3x^2 - 4y$, so $12 - 4$. | correct | B18 |
| `items[1].parts[2].explain.text` | $f_y = x^3 - 4xy$ and $f_{yx} = 3x^2 - 4y$, the same as part 2's $f_{xy}$. At $(2, 1)$ both give 8. | correct | B18 |
| `items[1].parts[3].question` | Using $f_x = 3x^2 y - 2y^2$ from part 1, what is the $x$-slope $f_x$ at $(2, 1)$? | correct | B18 |
| `items[1].parts[3].widget.answer` | 10 | correct | B18 |
| `items[1].parts[3].widget.wrong[0]` | slip sign = 14 | correct | B18 |
| `items[1].parts[3].widget.wrong[1]` | slip f-y = 0 | correct | B18 |
| `items[1].parts[3].feedback.correct` | $f_x(2, 1) = 3 \times 4 \times 1 - 2 \times 1 = 12 - 2 = 10$. | correct | B18 |
| `items[1].parts[3].feedback.generic` | Not quite. Put $x = 2$ and $y = 1$ into $3x^2 y - 2y^2$. | correct | B18 |
| `items[1].parts[3].feedback.byKey.sign` | You added the $2y^2$. It is subtracted: $12 - 2 = 10$. | correct | B18 |
| `items[1].parts[3].feedback.byKey.f-y` | That is $f_y(2, 1) = 8 - 8$. The $x$-slope is $f_x$. | correct | B18 |
| `items[1].parts[3].explain.text` | $f_x(2, 1) = 12 - 2 = 10$. It is the slope of the slice $y = 1$ at $x = 2$. | correct | B18 |
| `items[1].parts[4].question` | Using $f_x(2, 1) = 10$ and $f_{xy}(2, 1) = 8$, estimate the $x$-slope $f_x$ at $(2, 1.1)$. Give one decimal place. | correct | B18 |
| `items[1].parts[4].widget.answer` | 10.8 | correct | B18 |
| `items[1].parts[4].widget.accept` | 10.8 (the exact value 10.78 rounds to it) | correct | B18 |
| `items[1].parts[4].widget.wrong[0]` | slip used-xx = 11.2 | correct | B18 |
| `items[1].parts[4].widget.wrong[1]` | slip used-yy = 9.2 | correct | B18 |
| `items[1].parts[4].widget.wrong[2]` | slip change-only = 0.8 | correct | B18 |
| `items[1].parts[4].feedback.correct` | $f_{xy} = 8$ means the $x$-slope rises 8 per unit of $y$. So $f_x \approx 10 + 8 \times 0.1 = 10.8$, and the exact value is 10.78. | correct | B18 |
| `items[1].parts[4].feedback.generic` | Not quite. Start from the slope 10 and add the mixed partial times the step in $y$. | correct | B18 |
| `items[1].parts[4].feedback.byKey.used-xx` | You used $f_{xx} = 12$, which says how the slope changes with $x$. Here $y$ moves, so use $f_{xy} = 8$. | correct | B18 |
| `items[1].parts[4].feedback.byKey.used-yy` | You used $f_{yy} = -8$. The change in the $x$-slope as $y$ moves is $f_{xy}$. | correct | B18 |
| `items[1].parts[4].feedback.byKey.change-only` | That is the change in the slope. Add it to the slope 10 at $(2, 1)$. | correct | B18 |
| `items[1].parts[4].explain.text` | $f_x(2, 1.1) \approx f_x(2, 1) + f_{xy}(2, 1) \times 0.1 = 10 + 0.8 = 10.8$. The exact value is $13.2 - 2.42 = 10.78$. | correct | B18 |
| `items[2].prose` | A UK fund holds 2,000 shares of a US stock. At a price of $P$ dollars and an exchange rate of $X$ dollars per pound, the holding is worth $V(P, X) ... | correct | B18 |
| `items[2].parts[0].question` | What is $V_P$ at today's point, in pounds per dollar rise in the price? | correct | B18 |
| `items[2].parts[0].widget.answer` | 1600 | correct | B18 |
| `items[2].parts[0].widget.wrong[0]` | slip times-x = 2500 | correct | B18 |
| `items[2].parts[0].widget.wrong[1]` | slip no-x = 2000 | correct | B18 |
| `items[2].parts[0].feedback.correct` | Holding $X$ fixed, $V_P = \frac{2000}{X}$. At $X = 1.25$ that is £1,600 per dollar. | correct | B18 |
| `items[2].parts[0].feedback.generic` | Not quite. Hold $X$ fixed: $V$ is then a constant times $P$. | correct | B18 |
| `items[2].parts[0].feedback.byKey.times-x` | You multiplied by $X$. Holding $X$ fixed, $V = \frac{2000}{X}P$, so divide 2,000 by 1.25. | correct | B18 |
| `items[2].parts[0].feedback.byKey.no-x` | You left out the exchange rate. Each dollar of price is worth $\frac{1}{1.25}$ pounds, so $V_P = 1{,}600$. | correct | B18 |
| `items[2].parts[0].explain.text` | With $X$ fixed, $V$ is $\frac{2000}{X}$ times $P$. So $V_P = \frac{2000}{1.25} = 1{,}600$ pounds per dollar. | correct | B18 |
| `items[2].parts[1].question` | What is $V_X$ at today's point, in pounds per unit rise in $X$? | correct | B18 |
| `items[2].parts[1].widget.answer` | -64000 | correct | B18 |
| `items[2].parts[1].widget.wrong[0]` | slip sign = 64000 | correct | B18 |
| `items[2].parts[1].widget.wrong[1]` | slip no-square = -80000 | correct | B18 |
| `items[2].parts[1].feedback.correct` | $V_X = -\frac{2000P}{X^2}$. At today's point that is $-\frac{100{,}000}{1.5625} = -64{,}000$. | correct | B18 |
| `items[2].parts[1].feedback.generic` | Not quite. Hold $P$ fixed and differentiate $\frac{1}{X}$, which gives $-\frac{1}{X^2}$. | correct | B18 |
| `items[2].parts[1].feedback.byKey.sign` | The size is right, but a stronger pound lowers the sterling value. $\frac{d}{dX}\frac{1}{X} = -\frac{1}{X^2}$. | correct | B18 |
| `items[2].parts[1].feedback.byKey.no-square` | You divided by $X$ once. The derivative of $\frac{1}{X}$ is $-\frac{1}{X^2}$, so divide by $1.25^2 = 1.5625$. | correct | B18 |
| `items[2].parts[1].explain.text` | Holding $P = 50$ fixed, $V = \frac{100{,}000}{X}$. So $V_X = -\frac{100{,}000}{X^2} = -64{,}000$ at $X = 1.25$. | correct | B18 |
| `items[2].parts[2].question` | The price is rising at 0.50 dollars a day and $X$ at 0.01 a day. Using $V_P = 1{,}600$ and $V_X = -64{,}000$, at what rate is $V$ changing, in poun... | correct | B18 |
| `items[2].parts[2].widget.answer` | 160 | correct | B18 |
| `items[2].parts[2].widget.wrong[0]` | slip sign = 1440 | correct | B18 |
| `items[2].parts[2].widget.wrong[1]` | slip price-only = 800 | correct | B18 |
| `items[2].parts[2].widget.wrong[2]` | slip carried = 0 | correct | B18 |
| `items[2].parts[2].feedback.correct` | $\frac{dV}{dt} = V_P P'(t) + V_X X'(t) = 1{,}600 \times 0.5 - 64{,}000 \times 0.01 = 800 - 640 = 160$ pounds a day. | correct | B18 |
| `items[2].parts[2].feedback.generic` | Not quite. Add one part per input: $V_P$ times the price's rate, plus $V_X$ times the rate at which $X$ moves. | correct | B18 |
| `items[2].parts[2].feedback.byKey.sign` | You added the currency part. $V_X$ is negative, so the stronger pound takes £640 a day off. | correct | B18 |
| `items[2].parts[2].feedback.byKey.price-only` | That is the price part alone. The currency part, $-64{,}000 \times 0.01 = -640$, counts too. | correct | B18 |
| `items[2].parts[2].feedback.byKey.carried` | You used $V_X = -80{,}000$, which divides by $X$ once. With $-64{,}000$ the currency part is $-640$. | correct | B18 |
| `items[2].parts[2].explain.text` | Each input adds a part: the price adds £800 a day and the pound takes off £640. So the value grows at £160 a day. | correct | B18 |
| `items[2].parts[3].question` | The sterling delta $V_P = \frac{2000}{X}$ moves too. Find the mixed partial $V_{PX}$ as an expression in $X$. | correct | B18 |
| `items[2].parts[3].widget.answer` | -\frac{2000}{X^2} | correct | B18 |
| `items[2].parts[3].widget.accept` | -2000X^{-2} | correct | B18 |
| `items[2].parts[3].widget.wrong[0]` | slip sign = \frac{2000}{X^2} | correct | B18 |
| `items[2].parts[3].widget.wrong[1]` | slip gave-vx = -\frac{2000P}{X^2} | correct | B18 |
| `items[2].parts[3].feedback.correct` | $V_{PX} = \frac{\partial}{\partial X}\left(\frac{2000}{X}\right) = -\frac{2000}{X^2}$, the same as $V_{XP}$. | correct | B18 |
| `items[2].parts[3].feedback.generic` | Not quite. Differentiate $V_P = \frac{2000}{X}$ in $X$. | correct | B18 |
| `items[2].parts[3].feedback.byKey.sign` | Check the sign: $\frac{2000}{X}$ falls as $X$ rises, so its derivative is negative. | correct | B18 |
| `items[2].parts[3].feedback.byKey.gave-vx` | That is $V_X$, the $X$-slope of $V$ itself. Differentiate $V_P = \frac{2000}{X}$ instead. | correct | B18 |
| `items[2].parts[3].explain.text` | Differentiating $V_P = \frac{2000}{X}$ in $X$ gives $-\frac{2000}{X^2}$. At $X = 1.25$ it is $-1{,}280$. | correct | B18 |
| `items[2].parts[4].question` | Apply the chain rule to $V_P(P, X)$ along the day's path, with $P' = 0.5$ and $X' = 0.01$ as in part 3. Using $V_{PX} = -1{,}280$ at today's point,... | correct | B18 |
| `items[2].parts[4].widget.answer` | -12.8 | correct | B18 |
| `items[2].parts[4].widget.wrong[0]` | slip sign = 12.8 | correct | B18 |
| `items[2].parts[4].widget.wrong[1]` | slip no-rate = -1280 | correct | B18 |
| `items[2].parts[4].widget.wrong[2]` | slip used-vx = -640 | correct | B18 |
| `items[2].parts[4].feedback.correct` | $\frac{dV_P}{dt} = V_{PP} P' + V_{PX} X' = 0 \times 0.5 - 1{,}280 \times 0.01 = -12.8$. $V_P = \frac{2000}{X}$ has no $P$ in it, so $V_{PP} = 0$. | correct | B18 |
| `items[2].parts[4].feedback.generic` | Not quite. $V_P$ has a part from each input: $V_{PP} P'$ plus $V_{PX} X'$. | correct | B18 |
| `items[2].parts[4].feedback.byKey.sign` | The delta falls: a stronger pound shrinks it, so the rate is negative. | correct | B18 |
| `items[2].parts[4].feedback.byKey.no-rate` | That is $V_{PX}$ itself. Multiply it by $X' = 0.01$ a day. | correct | B18 |
| `items[2].parts[4].feedback.byKey.used-vx` | You used $V_X = -64{,}000$. The delta's rate needs the mixed partial $V_{PX} = -1{,}280$. | correct | B18 |
| `items[2].parts[4].explain.text` | $V_P = \frac{2000}{X}$ does not depend on $P$, so $V_{PP} = 0$ and only the currency part is left. It is $-1{,}280 \times 0.01 = -12.8$ pounds per ... | correct | B18 |

## l5-steepest-climb

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Compute the gradient and see it point uphill, across the contours. | correct | B19 |
| `objectives[1]` | Read the gradient's length as the slope of the steepest climb. | correct | B19 |
| `screens[0].prose` | Here is a contour map of $f(x, y) = x^2 + 2y^2$. Each curve joins points of equal height, and the height rises by 4 from one curve to the next. You... | correct | B19 |
| `screens[0].question` | Tap the arrow tip that climbs fastest. | correct | B19 |
| `screens[0].widget.answer` | A | correct | B19 |
| `screens[0].hints[0]` | Every curve is 4 units higher than the last. Which arrow reaches the next curve soonest? | correct | B19 |
| `screens[0].hints[1]` | The arrow that crosses the curve at P squarely, not at a slant, gains height in the least distance. | correct | B19 |
| `screens[0].hints[2]` | Arrow C starts out along the curve, so at P it gains nothing. Arrow A leaves the curve at a right angle. | correct | B19 |
| `screens[0].feedback.correct` | Arrow A crosses the contours at right angles, so it gains height fastest. | correct | B19 |
| `screens[0].feedback.generic` | Not quite right. Look for the arrow that reaches the next contour in the shortest distance. | correct | B19 |
| `screens[0].feedback.byKey.B` | You pointed straight away from the bottom at (0, 0). The contours are squashed, so that line crosses them at a slant. | correct | B19 |
| `screens[0].feedback.byKey.C` | You set off along the contour through P. In that direction the slope at P is 0. | correct | B19 |
| `screens[0].feedback.byKey.D` | You went straight up in $y$ because $2y^2$ has the bigger coefficient. Arrow A crosses the curves more squarely. | correct | B19 |
| `screens[0].explain.text` | At P the slope along arrow A is about 5.7, along B about 5.4, along D 4 and along C 0. A is the one at right angles to the contour through P. Slant... | correct | B19 |
| `screens[1].prose` | Now the steepest-climb arrow is drawn for you, at one fifth of its true size. Drag the blue point P anywhere on the map and watch the arrow. | correct | B19 |
| `screens[1].question` | Drag P from (1, 0) out along the $x$-axis to (4, 0). The arrow grows. What do the contours do along the way? | correct | B19 |
| `screens[1].widget.options[0]` | option closer (key): They get closer together | correct | B19 |
| `screens[1].widget.options[1]` | option apart: They spread further apart | correct | B19 |
| `screens[1].widget.options[1].why` | You may have read the gaps near the middle. Compare the gap at $x = 1$ with the gap at $x = 4$. | correct | B19 |
| `screens[1].widget.options[2]` | option same: They stay evenly spaced | correct | B19 |
| `screens[1].widget.options[2].why` | The heights are evenly spaced, but the curves are not. Near $x = 4$ two curves sit about 0.5 apart, near $x = 2$ about 1 apart. | correct | B19 |
| `screens[1].hints[0]` | Count how many curves P crosses between $x = 3$ and $x = 4$. | correct | B19 |
| `screens[1].hints[1]` | Near the middle the curves are far apart. Near the edge they bunch up. | correct | B19 |
| `screens[1].feedback.correct` | Closer contours mean a steeper climb, and a longer arrow. | correct | B19 |
| `screens[1].feedback.generic` | Not quite right. Watch the gaps between curves as P moves outwards. | correct | B19 |
| `screens[1].feedback.byKey.apart` | You may have read the gaps near the middle. Compare the gap at $x = 1$ with the gap at $x = 4$. | correct | B19 |
| `screens[1].feedback.byKey.same` | The heights are evenly spaced, but the curves are not. Near $x = 4$ two curves sit about 0.5 apart, near $x = 2$ about 1 apart. | correct | B19 |
| `screens[1].explain.text` | Each gap is a rise of 4. Where the gaps are narrow, 4 units of height come in a short distance, so the climb is steep. The arrow's length tracks th... | correct | B19 |
| `screens[2].prose` | The arrow's two components are the partial derivatives: $\nabla f = (f_x, f_y)$, read **grad f**. This arrow is the **gradient**. For $f = x^2 + 2y... | correct | B19 |
| `screens[2].question` | What is $\nabla f$ at Q = (3, 1)? | correct | B19 |
| `screens[2].widget.options[0]` | option swap: $(4, 6)$ | correct | B19 |
| `screens[2].widget.options[0].why` | You swapped the components. The first is $f_x = 2x = 6$, the second $f_y = 4y = 4$. | correct | B19 |
| `screens[2].widget.options[1]` | option right (key): $(6, 4)$ | correct | B19 |
| `screens[2].widget.options[2]` | option half: $(6, 2)$ | correct | B19 |
| `screens[2].widget.options[2].why` | You differentiated $2y^2$ as $2y$. The power rule brings the 2 down: $2 \times 2y = 4y$. | correct | B19 |
| `screens[2].widget.options[3]` | option point: $(3, 1)$ | correct | B19 |
| `screens[2].widget.options[3].why` | That is the point Q itself. The gradient is built from the slopes at Q. | correct | B19 |
| `screens[2].widget.options[4]` | option values: $(9, 2)$ | correct | B19 |
| `screens[2].widget.options[4].why` | You put Q into $x^2$ and $2y^2$, the terms of $f$. The gradient uses their derivatives. | correct | B19 |
| `screens[2].hints[0]` | Put $x = 3$ into $f_x$ and $y = 1$ into $f_y$. | correct | B19 |
| `screens[2].hints[1]` | $f_x = 2x$ and $f_y = 4y$, in that order. | correct | B19 |
| `screens[2].hints[2]` | $f_x(3, 1) = 6$ and $f_y(3, 1) = 4$. | correct | B19 |
| `screens[2].feedback.correct` | $\nabla f(3, 1) = (6, 4)$. | correct | B19 |
| `screens[2].feedback.generic` | Not quite right. Evaluate each partial derivative at (3, 1). | correct | B19 |
| `screens[2].explain.text` | The first component is $f_x(3, 1) = 2 \times 3 = 6$ and the second is $f_y(3, 1) = 4 \times 1 = 4$. Drawn at one fifth size, the arrow crosses the ... | correct | B19 |
| `screens[3].prose` | The length $\|\nabla f\| = \sqrt{f_x^2 + f_y^2}$ is the slope of the steepest climb: the rise in $f$ per unit step along the arrow. Back at P = (2,... | correct | B19 |
| `screens[3].question` | How steep is the steepest climb from P? | correct | B19 |
| `screens[3].widget.answer` | 5.657 | correct | B19 |
| `screens[3].widget.accept` | $\sqrt{4^2 + 4^2} = \sqrt{32} \approx 5.66$ | correct | B19 |
| `screens[3].widget.wrong[0]` | slip added = 8 | correct | B19 |
| `screens[3].widget.wrong[1]` | slip squared = 32 | correct | B19 |
| `screens[3].widget.wrong[2]` | slip one = 4 | correct | B19 |
| `screens[3].hints[0]` | Use Pythagoras on the two components. | correct | B19 |
| `screens[3].hints[1]` | $\|\nabla f\| = \sqrt{4^2 + 4^2}$. | correct | B19 |
| `screens[3].hints[2]` | $\sqrt{32} \approx 5.66$. | correct | B19 |
| `screens[3].feedback.correct` | About 5.66 units of height per unit step, the 5.7 you saw for arrow A. | correct | B19 |
| `screens[3].feedback.generic` | Not quite right. Square both components, add, then take the square root. | correct | B19 |
| `screens[3].feedback.byKey.added` | You added the components. They are at right angles, so combine them with Pythagoras. | correct | B19 |
| `screens[3].feedback.byKey.squared` | You stopped at $4^2 + 4^2 = 32$. Take the square root. | correct | B19 |
| `screens[3].feedback.byKey.one` | 4 is the slope along $x$ alone. The gradient direction does better. | correct | B19 |
| `screens[3].explain.text` | You combined the two slopes with Pythagoras: $\sqrt{16 + 16} \approx 5.66$. That matches the 5.66 per unit step of arrow A in the first screen. | correct | B19 |
| `screens[4].prose` | Points A $= (\sqrt{10}, 0)$ and B $= (0, \sqrt 5)$ both sit on the contour $f = 10$. Look at the gaps between curves near each one. | correct | B19 |
| `screens[4].question` | Tap the point where the steepest climb is steeper. | correct | B19 |
| `screens[4].widget.answer` | B | correct | B19 |
| `screens[4].hints[0]` | Narrow gaps between contours mean a steep climb. | correct | B19 |
| `screens[4].hints[1]` | Compare the gaps just outside A and just outside B. | correct | B19 |
| `screens[4].hints[2]` | $\|\nabla f\|$ at A is $2\sqrt{10} \approx 6.32$; at B it is $4\sqrt 5 \approx 8.94$. | correct | B19 |
| `screens[4].feedback.correct` | B: the contours are packed tighter along the $y$-axis. | correct | B19 |
| `screens[4].feedback.generic` | Not quite right. Compare the gaps between curves near each point. | correct | B19 |
| `screens[4].feedback.byKey.A` | A is further from the bottom, but distance is not height. The curves are closer together near B. | correct | B19 |
| `screens[4].explain.text` | At A, $\nabla f \approx (6.32, 0)$. At B, $\nabla f \approx (0, 8.94)$. Same height, but the curves bunch more tightly near B, so the arrow there i... | correct | B19 |
| `screens[5].prose` | Now stand at the very bottom of the bowl, O = (0, 0), where $f = 0$. | correct | B19 |
| `screens[5].question` | What is $\nabla f$ at O, and what does it tell you? | correct | B19 |
| `screens[5].widget.options[0]` | option zero (key): $(0, 0)$: no direction starts out steeper than another | correct | B19 |
| `screens[5].widget.options[1]` | option flat: $(0, 0)$: $f$ cannot rise from here | correct | B19 |
| `screens[5].widget.options[1].why` | You read a zero gradient as a flat floor. $f$ rises in every direction from O; only the slope at O itself is zero. | correct | B19 |
| `screens[5].widget.options[2]` | option coef: $(2, 4)$: climb in the direction $(2, 4)$ | correct | B19 |
| `screens[5].widget.options[2].why` | You read off the coefficients of $2x$ and $4y$. Put $x = 0$ and $y = 0$ into them. | correct | B19 |
| `screens[5].widget.options[3]` | option yaxis: $(0, 0)$, but along $y$ is steepest because the curves are closer | correct | B19 |
| `screens[5].widget.options[3].why` | The curves are closer along $y$, but that matters a step away from O. At O itself every slope is zero. | correct | B19 |
| `screens[5].hints[0]` | Put $x = 0$ and $y = 0$ into $2x$ and $4y$. | correct | B19 |
| `screens[5].hints[1]` | An arrow of length 0 has no direction to point in. | correct | B19 |
| `screens[5].hints[2]` | $\nabla f(0, 0) = (0, 0)$, so the steepest slope at O is 0. | correct | B19 |
| `screens[5].feedback.correct` | The gradient vanishes at the bottom: no direction of steepest climb. | correct | B19 |
| `screens[5].feedback.generic` | Not quite right. Evaluate both partials at O, then think about an arrow of length zero. | correct | B19 |
| `screens[5].explain.text` | Both partials are zero at O, so $\nabla f = (0, 0)$. Every direction has slope 0 at the exact bottom, even though $f$ grows once you step away. Poi... | correct | B19 |
| `screens[6].prose` | A different function, a hill: $g(x, y) = 20 - x^2 - 4y^2$, with its peak at the origin. You stand at P = (2, 1). A friend says the fastest way up i... | correct | B19 |
| `screens[6].question` | In which direction does $\nabla g$ point at P? | correct | B19 |
| `screens[6].widget.options[0]` | option peak: $(-2, -1)$, straight at the peak | correct | B19 |
| `screens[6].widget.options[0].why` | You aimed at the summit. The contours are long ellipses, so that line crosses them at a slant. | correct | B19 |
| `screens[6].widget.options[1]` | option right (key): $(-4, -8)$ | correct | B19 |
| `screens[6].widget.options[2]` | option down: $(4, 8)$ | correct | B19 |
| `screens[6].widget.options[2].why` | You dropped the minus signs: the derivative of $-x^2$ is $-2x$. Your arrow points downhill. | correct | B19 |
| `screens[6].widget.options[3]` | option along: $(8, -4)$ | correct | B19 |
| `screens[6].widget.options[3].why` | That arrow runs along the contour through P, where $g$ does not change. | correct | B19 |
| `screens[6].hints[0]` | Compute $g_x$ and $g_y$ and put in P. | correct | B19 |
| `screens[6].hints[1]` | $g_x = -2x$ and $g_y = -8y$. | correct | B19 |
| `screens[6].hints[2]` | At (2, 1): $g_x = -4$, $g_y = -8$. | correct | B19 |
| `screens[6].feedback.correct` | $\nabla g = (-4, -8)$: steeply towards the near side of the ridge, not at the peak. | correct | B19 |
| `screens[6].feedback.generic` | Not quite right. Compute both partial derivatives of $g$ at P. | correct | B19 |
| `screens[6].feedback.byKey.peak` | You aimed at the summit. The contours are long ellipses, so that line crosses them at a slant. | correct | B19 |
| `screens[6].feedback.byKey.down` | You dropped the minus signs: the derivative of $-x^2$ is $-2x$. Your arrow points downhill. | correct | B19 |
| `screens[6].feedback.byKey.along` | That arrow runs along the contour through P, where $g$ does not change. | correct | B19 |
| `screens[6].explain.text` | $\nabla g(2, 1) = (-4, -8)$, which leans much more towards the $x$-axis than the peak does. The hill is steepest across its narrow side, so the bes... | correct | B19 |
| `screens[7].prose` | Every time, the arrow was built from the partials, crossed the contours at right angles and pointed uphill: $$\nabla f = (f_x, f_y), \qquad \|\nabl... | correct | B19 |
| `screens[7].question` | At some point $\nabla f = (3, -4)$. Which statement is right? | correct | B19 |
| `screens[7].widget.options[0]` | option right (key): The steepest climb has slope 5, in the direction $(3, -4)$ | correct | B19 |
| `screens[7].widget.options[1]` | option added: The steepest climb has slope 7, in the direction $(3, -4)$ | correct | B19 |
| `screens[7].widget.options[1].why` | You added the components. They meet at right angles, so the length is $\sqrt{9 + 16} = 5$. | correct | B19 |
| `screens[7].widget.options[2]` | option contour: The steepest climb has slope 5, in the direction $(4, 3)$ | correct | B19 |
| `screens[7].widget.options[2].why` | $(4, 3)$ is at right angles to the gradient: it runs along the contour. | correct | B19 |
| `screens[7].widget.options[3]` | option neg: The slope is $-1$, because $3 - 4 = -1$ | correct | B19 |
| `screens[7].widget.options[3].why` | You added the components with their signs. The length of an arrow is never negative. | correct | B19 |
| `screens[7].feedback.correct` | Length $\sqrt{3^2 + 4^2} = 5$, pointing along $(3, -4)$. | correct | B19 |
| `screens[7].feedback.generic` | Not quite right. The gradient gives both the direction and, through its length, the slope. | correct | B19 |
| `screens[7].explain.text` | The gradient is itself the direction of steepest climb, and its length is the slope that way: $\sqrt{9 + 16} = 5$. | correct | B19 |
| `screens[8].prose` | Why does $\nabla f$ cross the contours at right angles? Walk along a contour on a path $(x(t), y(t))$ and use the chain rule from level 1. | correct | B20 |
| `screens[8].question` | Put the lines of the argument in order. | correct | B20 |
| `screens[8].widget.lines[0]` | line walk: $f(x(t), y(t)) = c$ for every $t$: the path stays on the contour | correct | B20 |
| `screens[8].widget.lines[1]` | line chain: $f_x\,x'(t) + f_y\,y'(t) = 0$: chain rule, and a constant has derivative 0 | correct | B20 |
| `screens[8].widget.lines[2]` | line slope: $\dfrac{y'}{x'} = -\dfrac{f_x}{f_y}$: rearrange for the slope of the contour | correct | B20 |
| `screens[8].widget.lines[3]` | line perp: $-\dfrac{f_x}{f_y} \times \dfrac{f_y}{f_x} = -1$: the gradient has slope $\tfrac{f_y}{f_x}$, and slopes multiplying to $-1$ are perpendi... | correct | B20 |
| `screens[8].widget.answer` | walk, chain, slope, perp | correct | B20 |
| `screens[8].hints[0]` | Start from what it means to stay on a contour. | correct | B20 |
| `screens[8].hints[1]` | Differentiate the first line with respect to $t$; the right side is a constant. | correct | B20 |
| `screens[8].hints[2]` | Then turn the equation into the contour's slope, and compare it with the gradient's slope $f_y / f_x$. | correct | B20 |
| `screens[8].feedback.correct` | Along the contour $f$ is constant, and that forces the right angle. | correct | B20 |
| `screens[8].feedback.generic` | Not quite right. Begin with the path on the contour, then differentiate, then compare slopes. | correct | B20 |
| `screens[8].feedback.byKey.chain` | The chain rule needs something to differentiate first: the line saying $f$ stays at $c$. | correct | B20 |
| `screens[8].feedback.byKey.perp` | The right angle is the conclusion. It needs the contour's slope first. | correct | B20 |
| `screens[8].explain.text` | Staying on a contour means $f$ never changes, so its rate of change along the path is 0. The chain rule writes that rate with the partials, which f... | correct | B20 |
| `screens[9].prose` | A two-asset portfolio holds weights $w_1, w_2$. Asset 1 has volatility 20%, asset 2 has 10%, correlation 0.5. Its variance is $$V = 0.04w_1^2 + 0.0... | correct | B21 |
| `screens[9].question` | What is $\dfrac{\partial V}{\partial w_1}$ at $\mathbf{w} = (0.5, 0.5)$? | correct | B21 |
| `screens[9].widget.answer` | 0.05 | correct | B21 |
| `screens[9].widget.accept` | $0.08w_1 + 0.02w_2 = 0.04 + 0.01 = 0.05$ | correct | B21 |
| `screens[9].widget.wrong[0]` | slip no-cross = 0.04 | correct | B21 |
| `screens[9].widget.wrong[1]` | slip no-two = 0.025 | correct | B21 |
| `screens[9].widget.wrong[2]` | slip w2 = 0.02 | correct | B21 |
| `screens[9].hints[0]` | Differentiate $V$ with $w_2$ held fixed. | correct | B21 |
| `screens[9].hints[1]` | $\dfrac{\partial V}{\partial w_1} = 0.08w_1 + 0.02w_2$; the cross term counts. | correct | B21 |
| `screens[9].hints[2]` | $0.08 \times 0.5 + 0.02 \times 0.5 = 0.05$. | correct | B21 |
| `screens[9].feedback.correct` | 0.05. With $\partial V / \partial w_2 = 0.02$, $\nabla V = (0.05, 0.02) = 2\boldsymbol{\Sigma}\mathbf{w}$. | correct | B21 |
| `screens[9].feedback.generic` | Not quite right. Differentiate each term of $V$ with respect to $w_1$, then put in the weights. | correct | B21 |
| `screens[9].feedback.byKey.no-cross` | You dropped the cross term $0.02w_1w_2$. Its $w_1$-derivative is $0.02w_2 = 0.01$. | correct | B21 |
| `screens[9].feedback.byKey.no-two` | That is row 1 of $\boldsymbol{\Sigma}\mathbf{w}$. Differentiating $w_1^2$ brings down a 2, so the gradient is $2\boldsymbol{\Sigma}\mathbf{w}$. | correct | B21 |
| `screens[9].feedback.byKey.w2` | 0.02 is $\partial V / \partial w_2 = 0.02w_1 + 0.02w_2$. You want the $w_1$ partial. | correct | B21 |
| `screens[9].explain.text` | $\nabla V = (0.08w_1 + 0.02w_2,\ 0.02w_1 + 0.02w_2) = 2\boldsymbol{\Sigma}\mathbf{w} = (0.05, 0.02)$. Per unit of weight, adding asset 1 raises var... | correct | B21 |
| `summary.ideas[0]` | The gradient $\nabla f = (f_x, f_y)$ points in the direction of steepest climb. | correct | B19 |
| `summary.ideas[1]` | It crosses the contours at right angles, and its length $\|\nabla f\|$ is the steepest slope: closer contours, longer arrow. | correct | B19 |
| `summary.ideas[2]` | Where $\nabla f = (0, 0)$ no direction starts out steeper than another, as at the bottom of a bowl. | correct | B19 |
| `summary.formula.name` | Gradient | correct | B19 |
| `summary.formula.tex` | \nabla f = (f_x, f_y), \quad \|\nabla f\| = \sqrt{f_x^2 + f_y^2} | correct | B19 |
| `summary.formula.note` | Evaluate the partials at the point you stand on. | correct | B19 |
| `summary.trap` | The gradient need not point at the peak, and it never runs along a contour. It crosses the contour through your point at right angles. | correct | B19 |
| `quiz[0].prose` | Let $f(x, y) = x^2y + 3y$. | correct | B19 |
| `quiz[0].question` | What is $\nabla f$ at (2, 1)? | correct | B19 |
| `quiz[0].widget.options[0]` | option right (key): $(4, 7)$ | correct | B19 |
| `quiz[0].widget.options[1]` | option nothree: $(4, 4)$ | correct | B19 |
| `quiz[0].widget.options[1].why` | You lost the $3y$ term. Its $y$-derivative is 3, so $f_y = x^2 + 3 = 7$. | correct | B19 |
| `quiz[0].widget.options[2]` | option swap: $(7, 4)$ | correct | B19 |
| `quiz[0].widget.options[2].why` | You swapped the components. $f_x$ comes first. | correct | B19 |
| `quiz[0].widget.options[3]` | option fx: $(2, 7)$ | correct | B19 |
| `quiz[0].widget.options[3].why` | You treated $x^2y$ as $x^2$ when differentiating in $x$. Keep the $y$: $f_x = 2xy = 4$. | correct | B19 |
| `quiz[0].feedback.correct` | $f_x = 2xy = 4$ and $f_y = x^2 + 3 = 7$. | correct | B19 |
| `quiz[0].feedback.generic` | Not quite right. Find each partial derivative, then put in (2, 1). | correct | B19 |
| `quiz[0].explain.text` | Holding $y$ fixed, $f_x = 2xy = 4$. Holding $x$ fixed, $f_y = x^2 + 3 = 7$. So $\nabla f(2, 1) = (4, 7)$. | correct | B19 |
| `quiz[1].prose` | At a point on a map, $\nabla f = (-6, 8)$. | correct | B19 |
| `quiz[1].question` | What is the slope of the steepest climb there? | correct | B19 |
| `quiz[1].widget.answer` | 10 | correct | B19 |
| `quiz[1].widget.accept` | $\sqrt{36 + 64} = 10$ | correct | B19 |
| `quiz[1].widget.wrong[0]` | slip added = 2 | correct | B19 |
| `quiz[1].widget.wrong[1]` | slip abs = 14 | correct | B19 |
| `quiz[1].widget.wrong[2]` | slip sq = 100 | correct | B19 |
| `quiz[1].feedback.correct` | $\sqrt{(-6)^2 + 8^2} = 10$. | correct | B19 |
| `quiz[1].feedback.generic` | Not quite right. Square, add, take the square root. | correct | B19 |
| `quiz[1].feedback.byKey.added` | You added $-6$ and 8. The length uses squares, so the sign of $-6$ does not reduce it. | correct | B19 |
| `quiz[1].feedback.byKey.abs` | You added the sizes 6 and 8. Combine them with Pythagoras. | correct | B19 |
| `quiz[1].feedback.byKey.sq` | 100 is the squared length. Take the square root. | correct | B19 |
| `quiz[1].explain.text` | The steepest slope is the gradient's length, $\sqrt{36 + 64} = 10$, in the direction $(-6, 8)$. | correct | B19 |
| `quiz[2].prose` | For $f = x^2 + 2y^2$, the point (1, 1) lies on the contour $f = 3$. | correct | B19 |
| `quiz[2].question` | Which arrow points along the contour at (1, 1)? | correct | B19 |
| `quiz[2].widget.options[0]` | option grad: $(2, 4)$ | correct | B19 |
| `quiz[2].widget.options[0].why` | That is $\nabla f(1, 1)$, which crosses the contour at right angles. | correct | B19 |
| `quiz[2].widget.options[1]` | option right (key): $(2, -1)$ | correct | B19 |
| `quiz[2].widget.options[2]` | option radial: $(1, 1)$ | correct | B19 |
| `quiz[2].widget.options[2].why` | That points straight away from the origin. On a squashed contour it is not tangent. | correct | B19 |
| `quiz[2].widget.options[3]` | option neg: $(-2, -4)$ | correct | B19 |
| `quiz[2].widget.options[3].why` | That is $-\nabla f$, straight downhill, still at right angles to the contour. | correct | B19 |
| `quiz[2].feedback.correct` | $(2, -1)$: its slope $-\tfrac12$ times the gradient's slope 2 is $-1$. | correct | B19 |
| `quiz[2].feedback.generic` | Not quite right. Find $\nabla f(1, 1)$, then an arrow at right angles to it. | correct | B19 |
| `quiz[2].explain.text` | $\nabla f(1, 1) = (2, 4)$ has slope 2. A tangent to the contour must be perpendicular to it, with slope $-\tfrac12$, such as $(2, -1)$. | correct | B19 |
| `quiz[3].prose` | A contour map has levels 10 apart. Near point A the contours are 0.5 apart; near point B they are 2 apart. | correct | B19 |
| `quiz[3].question` | Where is $\|\nabla f\|$ larger, and roughly how large? | correct | B19 |
| `quiz[3].widget.options[0]` | option right (key): At A, about 20 | correct | B19 |
| `quiz[3].widget.options[1]` | option b: At B, about 20 | correct | B19 |
| `quiz[3].widget.options[1].why` | You picked the wider gaps. Wide gaps mean the height changes slowly. | correct | B19 |
| `quiz[3].widget.options[2]` | option a5: At A, about 5 | correct | B19 |
| `quiz[3].widget.options[2].why` | 5 is the slope at B: 10 over 2. At A the rise of 10 comes in 0.5. | correct | B19 |
| `quiz[3].widget.options[3]` | option same: The same at both, because the levels are 10 apart everywhere | correct | B19 |
| `quiz[3].widget.options[3].why` | Equal steps in height do not mean equal steepness. The distance between curves sets the slope. | correct | B19 |
| `quiz[3].feedback.correct` | A rise of 10 over a distance of 0.5 is a slope of about 20. | correct | B19 |
| `quiz[3].feedback.generic` | Not quite right. Steepness is rise over distance, measured across the contours. | correct | B19 |
| `quiz[3].explain.text` | Across the contours, the slope is about rise over gap: $10 / 0.5 = 20$ at A and $10 / 2 = 5$ at B. Closer contours, longer gradient. | correct | B19 |

## l6-any-direction

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Compute a directional derivative from the gradient. | correct | B22 |
| `objectives[1]` | Explain why it is largest along the gradient and zero along a contour. | correct | B22 |
| `screens[0].prose` | Back on the bowl $f = x^2 + 2y^2$ at P = (2, 1). The blue arrow has length 1. Turn it with the slider; the caption reads how fast $f$ changes per u... | correct | B22 |
| `screens[0].question` | Turn the arrow all the way round. Where is the slope largest? | correct | B22 |
| `screens[0].widget.options[0]` | option right (key): At $45^\circ$, about 5.66 | correct | B22 |
| `screens[0].widget.options[1]` | option zero: At $0^\circ$, exactly 4 | correct | B22 |
| `screens[0].widget.options[1].why` | At $0^\circ$ you read $f_x$ alone. Keep turning: the slope climbs past 4. | correct | B22 |
| `screens[0].widget.options[2]` | option ninety: At $90^\circ$, exactly 4 | correct | B22 |
| `screens[0].widget.options[2].why` | At $90^\circ$ you read $f_y$ alone. Somewhere between $0^\circ$ and $90^\circ$ it beats both. | correct | B22 |
| `screens[0].widget.options[3]` | option down: At $225^\circ$, about $-5.66$ | correct | B22 |
| `screens[0].widget.options[3].why` | That is where the slope is most negative: the steepest way down, not up. | correct | B22 |
| `screens[0].hints[0]` | Watch the caption as you pass $0^\circ$, $45^\circ$ and $90^\circ$. | correct | B22 |
| `screens[0].hints[1]` | The largest reading sits between the $x$ direction and the $y$ direction. | correct | B22 |
| `screens[0].feedback.correct` | The largest slope, 5.66, comes at $45^\circ$: the gradient's direction from lesson 5. | correct | B22 |
| `screens[0].feedback.generic` | Not quite right. Turn slowly and note the largest number in the caption. | correct | B22 |
| `screens[0].explain.text` | The slope peaks at 5.66 when the arrow points along $\nabla f = (4, 4)$, at $45^\circ$. It is 0 at $135^\circ$ and $315^\circ$, along the contour, ... | correct | B22 |
| `screens[1].prose` | How does the caption get its number? Walk from P at unit speed along $\mathbf u = (0.6, 0.8)$, a unit arrow since $0.6^2 + 0.8^2 = 1$. Your positio... | correct | B22 |
| `screens[1].question` | Use the chain rule: what is $\dfrac{df}{dt}$ at $t = 0$? | correct | B22 |
| `screens[1].widget.answer` | 5.6 | correct | B22 |
| `screens[1].widget.accept` | $f_x \cdot 0.6 + f_y \cdot 0.8 = 2.4 + 3.2 = 5.6$ | correct | B22 |
| `screens[1].widget.wrong[0]` | slip sum = 8 | correct | B22 |
| `screens[1].widget.wrong[1]` | slip fx = 4 | correct | B22 |
| `screens[1].widget.wrong[2]` | slip speeds = 1.4 | correct | B22 |
| `screens[1].hints[0]` | The chain rule from level 1: $\dfrac{df}{dt} = f_x \dfrac{dx}{dt} + f_y \dfrac{dy}{dt}$. | correct | B22 |
| `screens[1].hints[1]` | Here $\dfrac{dx}{dt} = 0.6$ and $\dfrac{dy}{dt} = 0.8$. | correct | B22 |
| `screens[1].hints[2]` | $4 \times 0.6 + 4 \times 0.8 = 5.6$. | correct | B22 |
| `screens[1].feedback.correct` | 5.6, the same number the caption shows for this arrow. | correct | B22 |
| `screens[1].feedback.generic` | Not quite right. Multiply each partial by how fast that coordinate changes, then add. | correct | B22 |
| `screens[1].feedback.byKey.sum` | You added $f_x$ and $f_y$. Each must be weighted by how fast $x$ and $y$ change: 0.6 and 0.8. | correct | B22 |
| `screens[1].feedback.byKey.fx` | 4 is the slope along $x$ alone. The walk also climbs in $y$. | correct | B22 |
| `screens[1].feedback.byKey.speeds` | You added the speeds 0.6 and 0.8. Each speed multiplies a partial derivative. | correct | B22 |
| `screens[1].explain.text` | The rate you found is the **directional derivative** of $f$ along $\mathbf u$, written $D_{\mathbf u} f$. It weights each partial by the arrow's co... | correct | B22 |
| `screens[2].prose` | Still at P = (2, 1), where $\nabla f = (4, 4)$. Use $D_{\mathbf u} f = f_x u_1 + f_y u_2$, or turn the arrow to check. | correct | B22 |
| `screens[2].question` | Along which unit arrow is $D_{\mathbf u} f = 0$? | correct | B22 |
| `screens[2].widget.options[0]` | option grad: $(0.707, 0.707)$ | correct | B22 |
| `screens[2].widget.options[0].why` | That is the gradient's direction: $4(0.707) + 4(0.707) \approx 5.66$, the largest slope. | correct | B22 |
| `screens[2].widget.options[1]` | option right (key): $(-0.707, 0.707)$ | correct | B22 |
| `screens[2].widget.options[2]` | option half: $(0.6, -0.8)$ | correct | B22 |
| `screens[2].widget.options[2].why` | That gives $2.4 - 3.2 = -0.8$: gently downhill, not level. | correct | B22 |
| `screens[2].widget.options[3]` | option x: $(1, 0)$ | correct | B22 |
| `screens[2].widget.options[3].why` | That is the $x$ direction, with slope $f_x = 4$. | correct | B22 |
| `screens[2].hints[0]` | You need $4u_1 + 4u_2 = 0$. | correct | B22 |
| `screens[2].hints[1]` | So $u_2 = -u_1$: the components cancel. | correct | B22 |
| `screens[2].hints[2]` | $(-0.707, 0.707)$ has length 1 and gives $-2.83 + 2.83 = 0$. That is $135^\circ$. | correct | B22 |
| `screens[2].feedback.correct` | $135^\circ$: along the contour through P, where $f$ does not change. | correct | B22 |
| `screens[2].feedback.generic` | Not quite right. Find the arrow whose two products cancel. | correct | B22 |
| `screens[2].explain.text` | $4(-0.707) + 4(0.707) = 0$. That arrow runs along the contour through P, at right angles to $\nabla f$. Along a contour $f$ is level, so the slope ... | correct | B22 |
| `screens[3].prose` | Now point the arrow straight against the gradient: $\mathbf u = (-0.707, -0.707)$, at $225^\circ$. | correct | B22 |
| `screens[3].question` | What is $D_{\mathbf u} f$ at P? | correct | B22 |
| `screens[3].widget.answer` | -5.657 | correct | B22 |
| `screens[3].widget.accept` | $4(-0.707) + 4(-0.707) \approx -5.66$ | correct | B22 |
| `screens[3].widget.wrong[0]` | slip sign = 5.657 | correct | B22 |
| `screens[3].widget.wrong[1]` | slip zero = 0 | correct | B22 |
| `screens[3].widget.wrong[2]` | slip unscaled = -8 | correct | B22 |
| `screens[3].hints[0]` | Both components of $\mathbf u$ are negative. | correct | B22 |
| `screens[3].hints[1]` | $D_{\mathbf u} f = 4(-0.707) + 4(-0.707)$. | correct | B22 |
| `screens[3].hints[2]` | That is $-2 \times 2.83 \approx -5.66$. | correct | B22 |
| `screens[3].feedback.correct` | $-5.66$: the steepest way down, as steep as the steepest way up. | correct | B22 |
| `screens[3].feedback.generic` | Not quite right. Multiply each partial by the matching component, signs included. | correct | B22 |
| `screens[3].feedback.byKey.sign` | You dropped the minus signs. This arrow points downhill, so $f$ falls. | correct | B22 |
| `screens[3].feedback.byKey.zero` | 0 is the slope along the contour. This arrow points straight downhill. | correct | B22 |
| `screens[3].feedback.byKey.unscaled` | You used $(-1, -1)$, which has length $\sqrt 2$. Use the unit arrow $(-0.707, -0.707)$. | correct | B22 |
| `screens[3].explain.text` | $D_{\mathbf u} f = -2.83 - 2.83 \approx -5.66 = -\|\nabla f\|$. The steepest descent is exactly opposite the steepest climb, and just as steep. | correct | B22 |
| `screens[4].prose` | Move to the bottom of the bowl, O = (0, 0). Turn the arrow again and watch the caption. | correct | B22 |
| `screens[4].question` | What is $D_{\mathbf u} f$ at O? | correct | B22 |
| `screens[4].widget.options[0]` | option right (key): 0 in every direction | correct | B22 |
| `screens[4].widget.options[1]` | option y: 0, except along the $y$-axis where the curves are closer | correct | B22 |
| `screens[4].widget.options[1].why` | The curves are closer along $y$, but that shows a step away from O. At O, $f_y = 4 \times 0 = 0$. | correct | B22 |
| `screens[4].widget.options[2]` | option grad: Largest along $\nabla f$, as always | correct | B22 |
| `screens[4].widget.options[2].why` | $\nabla f(0, 0) = (0, 0)$, so $(0, 0) \cdot \mathbf u = 0$ for every $\mathbf u$. No direction is largest. | correct | B22 |
| `screens[4].widget.options[3]` | option undef: Not defined, because $\nabla f$ has no direction | correct | B22 |
| `screens[4].widget.options[3].why` | Only the steepest direction is undefined. The slope itself is $0 \cdot u_1 + 0 \cdot u_2 = 0$. | correct | B22 |
| `screens[4].hints[0]` | Find $f_x$ and $f_y$ at (0, 0). | correct | B22 |
| `screens[4].hints[1]` | Both partials are 0 at O. | correct | B22 |
| `screens[4].hints[2]` | $D_{\mathbf u} f = 0 \cdot u_1 + 0 \cdot u_2 = 0$, whatever $\mathbf u$ is. | correct | B22 |
| `screens[4].feedback.correct` | At a stationary point every directional derivative is 0. | correct | B22 |
| `screens[4].feedback.generic` | Not quite right. Evaluate the gradient at O first. | correct | B22 |
| `screens[4].explain.text` | At O the gradient is $(0, 0)$, so every directional derivative is 0. A point like this, where $f$ is level in every direction, is called a **statio... | correct | B22 |
| `screens[5].prose` | From P = (2, 1) a friend asks how steeply $f$ changes heading towards T = (−1, 5). The arrow from P to T is $(-3, 4)$. Recall $\nabla f(2, 1) = (4,... | correct | B22 |
| `screens[5].question` | What is the slope of $f$ at P in the direction of T? | correct | B22 |
| `screens[5].widget.answer` | 0.8 | correct | B22 |
| `screens[5].widget.accept` | $\mathbf u = (-0.6, 0.8)$, so $4(-0.6) + 4(0.8) = 0.8$ | correct | B22 |
| `screens[5].widget.wrong[0]` | slip raw = 4 | correct | B22 |
| `screens[5].widget.wrong[1]` | slip nosign = 5.6 | correct | B22 |
| `screens[5].widget.wrong[2]` | slip sqrt = 2.828 | correct | B22 |
| `screens[5].hints[0]` | Is $(-3, 4)$ a unit arrow? | correct | B22 |
| `screens[5].hints[1]` | Its length is $\sqrt{9 + 16} = 5$. Divide by 5 first. | correct | B22 |
| `screens[5].hints[2]` | $\mathbf u = (-0.6, 0.8)$, then $D_{\mathbf u} f = -2.4 + 3.2 = 0.8$. | correct | B22 |
| `screens[5].feedback.correct` | 0.8: a gentle climb, since T's direction runs close to the contour. | correct | B22 |
| `screens[5].feedback.generic` | Not quite right. Turn the arrow to T into a unit arrow before you use it. | correct | B22 |
| `screens[5].feedback.byKey.raw` | You used $(-3, 4)$ as it stands. It has length 5, so you got the change over 5 units of distance. Divide by 5. | correct | B22 |
| `screens[5].feedback.byKey.nosign` | You dropped the minus sign on $-3$. The walk to T goes left, so $u_1 = -0.6$. | correct | B22 |
| `screens[5].feedback.byKey.sqrt` | You divided by $\sqrt 2$, as for $(1, 1)$. The length of $(-3, 4)$ is 5. | correct | B22 |
| `screens[5].explain.text` | A slope is a change per unit step, so the arrow must have length 1. Divide $(-3, 4)$ by its length 5 to get $\mathbf u = (-0.6, 0.8)$. Then $D_{\ma... | correct | B22 |
| `screens[6].prose` | Each time, you weighted the partials by the arrow's components. That sum is the **dot product** $\nabla f \cdot \mathbf u$: $$D_{\mathbf u} f = \na... | correct | B22 |
| `screens[6].question` | At a point $\nabla f = (2, -1)$. What is $D_{\mathbf u} f$ for $\mathbf u = (0.8, 0.6)$? | correct | B22 |
| `screens[6].widget.options[0]` | option right (key): $1$ | correct | B22 |
| `screens[6].widget.options[1]` | option abs: $2.2$ | correct | B22 |
| `screens[6].widget.options[1].why` | You added $1.6$ and $0.6$. The second product is $(-1)(0.6) = -0.6$. | correct | B22 |
| `screens[6].widget.options[2]` | option fx: $1.6$ | correct | B22 |
| `screens[6].widget.options[2].why` | That is $f_x u_1$ alone. Add $f_y u_2 = -0.6$. | correct | B22 |
| `screens[6].widget.options[3]` | option swap: $0.4$ | correct | B22 |
| `screens[6].widget.options[3].why` | You paired $f_x$ with $u_2$: $2(0.6) + (-1)(0.8)$. Match first component with first, second with second. | correct | B22 |
| `screens[6].feedback.correct` | $2(0.8) + (-1)(0.6) = 1$. | correct | B22 |
| `screens[6].feedback.generic` | Not quite right. Multiply matching components, then add. | correct | B22 |
| `screens[6].explain.text` | $\nabla f \cdot \mathbf u = 2(0.8) + (-1)(0.6) = 1.6 - 0.6 = 1$. | correct | B22 |
| `screens[7].prose` | Why was the largest slope exactly $\|\nabla f\|$, along $\nabla f$? Write the unit arrow as $\mathbf u = (\cos\theta, \sin\theta)$ and the gradient... | correct | B23 |
| `screens[7].question` | Put the lines in order. | correct | B23 |
| `screens[7].widget.lines[0]` | line dot: $D_{\mathbf u} f = f_x\cos\theta + f_y\sin\theta$: the dot product with $\mathbf u = (\cos\theta, \sin\theta)$ | correct | B23 |
| `screens[7].widget.lines[1]` | line polar: $= \|\nabla f\|(\cos\alpha\cos\theta + \sin\alpha\sin\theta)$: put in $f_x = \|\nabla f\|\cos\alpha$, $f_y = \|\nabla f\|\sin\alpha$ | correct | B23 |
| `screens[7].widget.lines[2]` | line trig: $= \|\nabla f\|\cos(\theta - \alpha)$: the cosine of a difference | correct | B23 |
| `screens[7].widget.lines[3]` | line read: Largest, $\|\nabla f\|$, at $\theta = \alpha$; zero at $\theta = \alpha \pm 90^\circ$; smallest, $-\|\nabla f\|$, at $\theta = \alpha + ... | correct | B23 |
| `screens[7].widget.answer` | dot, polar, trig, read | correct | B23 |
| `screens[7].hints[0]` | Start from the formula you used on every screen. | correct | B23 |
| `screens[7].hints[1]` | Before any trigonometry, write the gradient's components using its length and angle. | correct | B23 |
| `screens[7].hints[2]` | Then $\cos\alpha\cos\theta + \sin\alpha\sin\theta = \cos(\theta - \alpha)$, and cosine runs from $-1$ to 1. | correct | B23 |
| `screens[7].feedback.correct` | The slope is $\|\nabla f\|$ times the cosine of the angle between $\mathbf u$ and $\nabla f$. | correct | B23 |
| `screens[7].feedback.generic` | Not quite right. Start from the dot product, rewrite the gradient, then use the identity. | correct | B23 |
| `screens[7].feedback.byKey.trig` | The identity needs the bracket $\cos\alpha\cos\theta + \sin\alpha\sin\theta$ first. | correct | B23 |
| `screens[7].feedback.byKey.read` | The conclusion comes last: it reads off where $\cos(\theta - \alpha)$ is 1, 0 and $-1$. | correct | B23 |
| `screens[7].explain.text` | $D_{\mathbf u} f = \|\nabla f\|\cos(\theta - \alpha)$, and cosine is at most 1. At P, $\alpha = 45^\circ$ and $\|\nabla f\| = 5.66$: the slider sho... | correct | B23 |
| `screens[8].prose` | A book is long 1,200 shares of A and short 500 shares of B. So its value changes by £1,200 per £1 rise in A and by −£500 per £1 rise in B. Overnigh... | correct | B22 |
| `screens[8].question` | Approximately what is the book's P&L? | correct | B22 |
| `screens[8].widget.answer` | 210 | correct | B22 |
| `screens[8].widget.accept` | $1200(0.80) + (-500)(1.50) = 960 - 750 = 210$ | correct | B22 |
| `screens[8].widget.wrong[0]` | slip nosign = 1710 | correct | B22 |
| `screens[8].widget.wrong[1]` | slip unit = 123.5 | correct | B22 |
| `screens[8].widget.wrong[2]` | slip flip = -210 | correct | B22 |
| `screens[8].hints[0]` | P&L is a dot product: sensitivities with the move. | correct | B22 |
| `screens[8].hints[1]` | A adds $1200 \times 0.80$; B adds $-500 \times 1.50$. | correct | B22 |
| `screens[8].hints[2]` | $960 - 750 = 210$. | correct | B22 |
| `screens[8].feedback.correct` | £210: the gain on A outweighs the loss on the short B. | correct | B22 |
| `screens[8].feedback.generic` | Not quite right. Multiply each sensitivity by its price move, signs included, then add. | correct | B22 |
| `screens[8].feedback.byKey.nosign` | You treated the short as long. A rise in B costs a short £500 per £1. | correct | B22 |
| `screens[8].feedback.byKey.flip` | You flipped the sign: the book makes money, because A's gain is larger. | correct | B22 |
| `screens[8].explain.text` | P&L $\approx \nabla V \cdot \Delta = 1200(0.80) - 500(1.50) = 210$, so about £210. Here we want the total change, not a slope, so the move is not d... | correct | B22 |
| `summary.ideas[0]` | The slope of $f$ along a unit arrow $\mathbf u$ is the directional derivative $D_{\mathbf u} f = f_x u_1 + f_y u_2$. | correct | B22 |
| `summary.ideas[1]` | It equals $\|\nabla f\|\cos(\text{angle to } \nabla f)$: largest along $\nabla f$, zero along the contour, most negative opposite. | correct | B22 |
| `summary.ideas[2]` | At a stationary point $\nabla f = (0, 0)$, so every directional derivative is zero. | correct | B22 |
| `summary.formula.name` | Directional derivative | correct | B22 |
| `summary.formula.tex` | D_{\mathbf u} f = \nabla f \cdot \mathbf u = f_x u_1 + f_y u_2 | correct | B22 |
| `summary.formula.note` | $\mathbf u$ must have length 1: divide an arrow by its length first. The formula needs a smooth $f$. | correct | B22 |
| `summary.trap` | Using an arrow like $(-3, 4)$ without dividing by its length 5 makes the slope five times too big. | correct | B22 |
| `quiz[0].prose` | Let $f(x, y) = xy^2$ and $\mathbf u = (0.6, -0.8)$. | correct | B22 |
| `quiz[0].question` | What is $D_{\mathbf u} f$ at (1, 2)? | correct | B22 |
| `quiz[0].widget.answer` | -0.8 | correct | B22 |
| `quiz[0].widget.accept` | $\nabla f(1, 2) = (4, 4)$, so $2.4 - 3.2 = -0.8$ | correct | B22 |
| `quiz[0].widget.wrong[0]` | slip nosign = 5.6 | correct | B22 |
| `quiz[0].widget.wrong[1]` | slip fy = 2.4 | correct | B22 |
| `quiz[0].widget.wrong[2]` | slip sign = 0.8 | correct | B22 |
| `quiz[0].feedback.correct` | $-0.8$: a gentle descent. | correct | B22 |
| `quiz[0].feedback.generic` | Not quite right. Find $\nabla f(1, 2)$, then take the dot product with $\mathbf u$. | correct | B22 |
| `quiz[0].feedback.byKey.nosign` | You dropped the minus sign on $-0.8$ in $\mathbf u$. | correct | B22 |
| `quiz[0].feedback.byKey.fy` | You kept only $f_x u_1 = 2.4$. Add $f_y u_2 = -3.2$. | correct | B22 |
| `quiz[0].feedback.byKey.sign` | 4(0.6) + 4(−0.8) is 2.4 − 3.2, which is below zero. A positive 0.8 takes 3.2 − 2.4, the wrong way round. | correct | B22 |
| `quiz[0].explain.text` | $f_x = y^2 = 4$ and $f_y = 2xy = 4$. Then $D_{\mathbf u} f = 4(0.6) + 4(-0.8) = -0.8$. | correct | B22 |
| `quiz[1].prose` | Let $f(x, y) = 3x + 4y$. | correct | B22 |
| `quiz[1].question` | What is the slope of $f$ in the direction of the arrow $(1, 1)$? | correct | B22 |
| `quiz[1].widget.answer` | 4.95 | correct | B22 |
| `quiz[1].widget.accept` | $\mathbf u = (1, 1)/\sqrt 2$, so $7/\sqrt 2 \approx 4.95$ | correct | B22 |
| `quiz[1].widget.wrong[0]` | slip raw = 7 | correct | B22 |
| `quiz[1].widget.wrong[1]` | slip grad = 5 | correct | B22 |
| `quiz[1].feedback.correct` | $7 / \sqrt 2 \approx 4.95$. | correct | B22 |
| `quiz[1].feedback.generic` | Not quite right. Make the arrow a unit arrow first. | correct | B22 |
| `quiz[1].feedback.byKey.raw` | You used $(1, 1)$ as it stands. Its length is $\sqrt 2$, so divide by it. | correct | B22 |
| `quiz[1].feedback.byKey.grad` | 5 is $\|\nabla f\|$, the largest slope. $(1, 1)$ is not the gradient's direction. | correct | B22 |
| `quiz[1].explain.text` | $\nabla f = (3, 4)$ and $\mathbf u = (1, 1)/\sqrt 2$. So $D_{\mathbf u} f = (3 + 4)/\sqrt 2 \approx 4.95$, a little under the maximum of 5. | correct | B22 |
| `quiz[2].prose` | At a point, $\nabla f = (5, 12)$. | correct | B22 |
| `quiz[2].question` | What is the largest directional derivative there, and along which unit arrow? | correct | B22 |
| `quiz[2].widget.options[0]` | option right (key): 13, along $(5/13, 12/13)$ | correct | B22 |
| `quiz[2].widget.options[1]` | option sum: 17, along $(5, 12)$ | correct | B22 |
| `quiz[2].widget.options[1].why` | You added 5 and 12. The length is $\sqrt{25 + 144} = 13$, and the arrow must be a unit arrow. | correct | B22 |
| `quiz[2].widget.options[2]` | option y: 12, along $(0, 1)$ | correct | B22 |
| `quiz[2].widget.options[2].why` | 12 is the slope along $y$ alone. Leaning towards $x$ as well does better. | correct | B22 |
| `quiz[2].widget.options[3]` | option perp: 13, along $(12/13, -5/13)$ | correct | B22 |
| `quiz[2].widget.options[3].why` | That arrow is at right angles to $\nabla f$, where the slope is 0. | correct | B22 |
| `quiz[2].feedback.correct` | The maximum is $\|\nabla f\| = 13$, along $\nabla f / 13$. | correct | B22 |
| `quiz[2].feedback.generic` | Not quite right. The largest slope is the gradient's length, along the gradient. | correct | B22 |
| `quiz[2].explain.text` | $D_{\mathbf u} f = \|\nabla f\|\cos(\text{angle})$ is largest when $\mathbf u$ points along $\nabla f$. Then it equals $\sqrt{5^2 + 12^2} = 13$. | correct | B22 |
| `quiz[3].prose` | At a point Q of a smooth function $f$, you find $D_{\mathbf u} f = 0$ for $\mathbf u = (1, 0)$ and for $\mathbf u = (0, 1)$. | correct | B22 |
| `quiz[3].question` | What follows? | correct | B22 |
| `quiz[3].widget.options[0]` | option right (key): $\nabla f(Q) = (0, 0)$, so every directional derivative at Q is 0 | correct | B22 |
| `quiz[3].widget.options[1]` | option two: Only those two directions are level; others may not be | correct | B22 |
| `quiz[3].widget.options[1].why` | Those two slopes are $f_x$ and $f_y$. Both zero makes $\nabla f = (0, 0)$, and for a smooth $f$ every slope is $\nabla f \cdot \mathbf u = 0$. | correct | B22 |
| `quiz[3].widget.options[2]` | option min: Q must be a minimum | correct | B22 |
| `quiz[3].widget.options[2].why` | Level in every direction does not mean lowest. Q could be a maximum or a saddle. | correct | B22 |
| `quiz[3].widget.options[3]` | option contour: Q lies on a contour where $f = 0$ | correct | B22 |
| `quiz[3].widget.options[3].why` | A zero slope says nothing about the value of $f$ at Q. | correct | B22 |
| `quiz[3].feedback.correct` | Q is a stationary point. | correct | B22 |
| `quiz[3].feedback.generic` | Not quite right. What are $f_x$ and $f_y$ at Q? | correct | B22 |
| `quiz[3].explain.text` | Along $(1, 0)$ the slope is $f_x$; along $(0, 1)$ it is $f_y$. Both are 0, so $\nabla f = (0, 0)$ and $D_{\mathbf u} f = 0$ for every $\mathbf u$. | correct | B22 |

## l7-tangent-planes

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Approximate a surface near a point with its tangent plane. | correct | B24 |
| `objectives[1]` | See the approximation error shrink with the square of the step. | imprecise | finding 3 (same defect) |
| `screens[0].prose` | Take $f(x, y) = x^2 + 2y^2$ near (2, 1), where $f = 6$. Each slice through (2, 1) has a tangent line of slope 4. No calculator: we want $f(2.1, 1.0... | correct | B24 |
| `screens[0].question` | Use the two tangent slopes to estimate $f(2.1, 1.05)$. | correct | B24 |
| `screens[0].widget.answer` | 6.6 | correct | B24 |
| `screens[0].widget.accept` | $6 + 4(0.1) + 4(0.05) = 6.6$; the true value is 6.615 | correct | B24 |
| `screens[0].widget.wrong[0]` | slip xonly = 6.4 | correct | B24 |
| `screens[0].widget.wrong[1]` | slip yonly = 6.2 | correct | B24 |
| `screens[0].widget.wrong[2]` | slip same = 6.8 | correct | B24 |
| `screens[0].widget.wrong[3]` | slip exact = 6.615 | correct | B24 |
| `screens[0].hints[0]` | Moving 0.1 in $x$ along a slope of 4 adds about $4 \times 0.1$. | correct | B24 |
| `screens[0].hints[1]` | The $y$ step is 0.05, along its own slope of 4. | correct | B24 |
| `screens[0].hints[2]` | $6 + 0.4 + 0.2 = 6.6$. | correct | B24 |
| `screens[0].feedback.correct` | 6.6, against a true value of 6.615. | correct | B24 |
| `screens[0].feedback.generic` | Not quite right. Add the change from each step to $f(2, 1) = 6$. | correct | B24 |
| `screens[0].feedback.byKey.xonly` | You used only the $x$ step. The $y$ step of 0.05 adds $4 \times 0.05 = 0.2$ more. | correct | B24 |
| `screens[0].feedback.byKey.yonly` | You used only the $y$ step. The $x$ step of 0.1 adds $4 \times 0.1 = 0.4$ more. | correct | B24 |
| `screens[0].feedback.byKey.same` | You stepped 0.1 in $y$ too. The $y$ step is 0.05. | correct | B24 |
| `screens[0].feedback.byKey.exact` | That is the exact value, worked out in full. Here we want the tangent estimate. | correct | B24 |
| `screens[0].explain.text` | You added two straight-line changes to the known height: $6 + 4(0.1) + 4(0.05) = 6.6$. The true value is 6.615, so the estimate is off by only 0.01... | correct | B24 |
| `screens[1].prose` | How good is a tangent estimate? On the slice $y = 1$, drag the blue point Q along the curve towards $x = 2$. The orange segment is the gap between ... | correct | B24 |
| `screens[1].question` | Halve the step from 1 to 0.5. What happens to the gap? | correct | B24 |
| `screens[1].widget.options[0]` | option right (key): It drops to a quarter, from 1 to 0.25 | correct | B24 |
| `screens[1].widget.options[1]` | option half: It halves, from 1 to 0.5 | correct | B24 |
| `screens[1].widget.options[1].why` | Read the caption at step 0.5: the gap is 0.25, not 0.5. | correct | B24 |
| `screens[1].widget.options[2]` | option same: It stays about the same | correct | B24 |
| `screens[1].widget.options[2].why` | Drag Q from $x = 3$ to $x = 2.5$ and compare the two gaps in the caption. | correct | B24 |
| `screens[1].hints[0]` | Read the gap at $x = 3$, then at $x = 2.5$. | correct | B24 |
| `screens[1].hints[1]` | The gap is 1 at step 1. | correct | B24 |
| `screens[1].feedback.correct` | Half the step, a quarter of the gap: the gap is the step squared. | correct | B24 |
| `screens[1].feedback.generic` | Not quite right. Compare the caption at steps 1 and 0.5. | correct | B24 |
| `screens[1].explain.text` | On this slice the gap is exactly $(x - 2)^2$, the step squared. So the tangent's error shrinks much faster than the step. Near the point, the strai... | correct | B24 |
| `screens[2].prose` | Your estimate added both slice changes to $f(2, 1)$: $$z = 6 + 4(x - 2) + 4(y - 1).$$ This is the **tangent plane** to the surface at (2, 1): a fla... | correct | B24 |
| `screens[2].question` | Multiply out the tangent plane: $z = \;?$ | correct | B24 |
| `screens[2].widget.answer` | 4x+4y-6 | correct | B24 |
| `screens[2].widget.accept` | 6+4(x-2)+4(y-1), 4y+4x-6, 2(2x+2y-3) | correct | B24 |
| `screens[2].widget.wrong[0]` | slip lost6 = 4x+4y-12 | correct | B24 |
| `screens[2].widget.wrong[1]` | slip sign = 4x+4y+6 | correct | B24 |
| `screens[2].hints[0]` | Expand $4(x - 2)$ and $4(y - 1)$. | correct | B24 |
| `screens[2].hints[1]` | $4(x - 2) = 4x - 8$ and $4(y - 1) = 4y - 4$. | correct | B24 |
| `screens[2].hints[2]` | $6 + 4x - 8 + 4y - 4 = 4x + 4y - 6$. | correct | B24 |
| `screens[2].feedback.correct` | $z = 4x + 4y - 6$. Check: at (2, 1) it gives 6. | correct | B24 |
| `screens[2].feedback.generic` | Not quite right. Expand both brackets and collect the numbers. | correct | B24 |
| `screens[2].feedback.byKey.lost6` | You dropped the starting height 6. Without it the plane misses the point (2, 1, 6). | correct | B24 |
| `screens[2].feedback.byKey.sign` | Check the numbers: $6 - 8 - 4 = -6$. | correct | B24 |
| `screens[2].explain.text` | $6 + 4x - 8 + 4y - 4 = 4x + 4y - 6$. At (2.1, 1.05) it gives $8.4 + 4.2 - 6 = 6.6$, your estimate. The plane touches the surface at (2, 1, 6) and l... | correct | B24 |
| `screens[3].prose` | Step from (2, 1) to $(2 + h, 1 + h)$ and compare the plane with the truth. The table shows the error $f - z$. | correct | B24 |
| `screens[3].question` | What is the error when $h = 0.01$? | correct | B24 |
| `screens[3].widget.answer` | 0.0003 | correct | B24 |
| `screens[3].widget.accept` | $3h^2 = 3(0.01)^2 = 0.0003$ | correct | B24 |
| `screens[3].widget.wrong[0]` | slip linear = 0.003 | correct | B24 |
| `screens[3].widget.wrong[1]` | slip h2 = 0.0001 | correct | B24 |
| `screens[3].hints[0]` | Each time $h$ halves, what does the error do? | correct | B24 |
| `screens[3].hints[1]` | From $h = 0.1$ to $0.05$ the error goes from 0.03 to 0.0075: a quarter. | correct | B24 |
| `screens[3].hints[2]` | The error is $3h^2$: $3 \times 0.0001 = 0.0003$. | correct | B24 |
| `screens[3].feedback.correct` | 0.0003. Ten times closer, a hundred times smaller error. | correct | B24 |
| `screens[3].feedback.generic` | Not quite right. Look at how the error scales with $h$ down the table. | correct | B24 |
| `screens[3].feedback.byKey.linear` | You scaled the error by 10, like $h$. It scales with $h^2$, so by 100. | correct | B24 |
| `screens[3].feedback.byKey.h2` | That is $h^2$. Read off the multiplier from the table: 0.03 at $h = 0.1$ is $3h^2$. | correct | B24 |
| `screens[3].explain.text` | Here the error is exactly $h^2 + 2h^2 = 3h^2$. It shrinks with the square of the step, so it is **quadratic** in $h$. Close in by 10 and the error ... | correct | B24 |
| `screens[4].prose` | The steps can have different signs. Use $z = 6 + 4(x - 2) + 4(y - 1)$. | correct | B24 |
| `screens[4].question` | Estimate $f(1.98, 1.03)$ with the tangent plane. | correct | B24 |
| `screens[4].widget.answer` | 6.04 | correct | B24 |
| `screens[4].widget.accept` | $6 + 4(-0.02) + 4(0.03) = 6.04$; the true value is 6.0422 | correct | B24 |
| `screens[4].widget.wrong[0]` | slip nosign = 6.2 | correct | B24 |
| `screens[4].widget.wrong[1]` | slip exact = 6.0422 | correct | B24 |
| `screens[4].hints[0]` | $x - 2 = -0.02$: the $x$ step is backwards. | correct | B24 |
| `screens[4].hints[1]` | $4(-0.02) = -0.08$ and $4(0.03) = 0.12$. | correct | B24 |
| `screens[4].hints[2]` | $6 - 0.08 + 0.12 = 6.04$. | correct | B24 |
| `screens[4].feedback.correct` | 6.04. The true value is 6.0422. | correct | B24 |
| `screens[4].feedback.generic` | Not quite right. Find each step with its sign, multiply by 4, add to 6. | correct | B24 |
| `screens[4].feedback.byKey.nosign` | You took the $x$ step as $+0.02$. From 2 to 1.98 is $-0.02$. | correct | B24 |
| `screens[4].feedback.byKey.exact` | That is the true value. The plane's estimate is 6.04. | correct | B24 |
| `screens[4].explain.text` | The $x$ step lowers $f$ by 0.08 and the $y$ step raises it by 0.12. The plane gives 6.04, against a true 6.0422. | correct | B24 |
| `screens[5].prose` | Jo estimates $f(2.5, 1.5)$ from (2, 1) like this: $$6 + f_x(2.5, 1.5)(0.5) + f_y(2.5, 1.5)(0.5) = 6 + 5(0.5) + 6(0.5).$$ | correct | B24 |
| `screens[5].question` | What does the tangent plane at (2, 1) actually give for $f(2.5, 1.5)$? | correct | B24 |
| `screens[5].widget.options[0]` | option jo: 11.5 | correct | B24 |
| `screens[5].widget.options[0].why` | That is Jo's sum. Jo took the slopes at the new point, (2.5, 1.5). The plane at (2, 1) uses the slopes at (2, 1). | correct | B24 |
| `screens[5].widget.options[1]` | option right (key): 10 | correct | B24 |
| `screens[5].widget.options[2]` | option true: 10.75 | correct | B24 |
| `screens[5].widget.options[2].why` | That is the true value, $6.25 + 4.5$. The plane's estimate is a different number. | correct | B24 |
| `screens[5].widget.options[3]` | option half: 8 | correct | B24 |
| `screens[5].widget.options[3].why` | You took half of each step. The steps are 0.5 in full: $4 \times 0.5 = 2$ each. | correct | B24 |
| `screens[5].hints[0]` | Which slopes do you actually know when you stand at (2, 1)? | correct | B24 |
| `screens[5].hints[1]` | The plane uses $f_x(2, 1) = 4$ and $f_y(2, 1) = 4$. | correct | B24 |
| `screens[5].hints[2]` | $6 + 4(0.5) + 4(0.5) = 10$. | correct | B24 |
| `screens[5].feedback.correct` | $6 + 4(0.5) + 4(0.5) = 10$. | correct | B24 |
| `screens[5].feedback.generic` | Not quite right. Use the slopes at the point you start from, (2, 1). | correct | B24 |
| `screens[5].feedback.byKey.jo` | That is Jo's sum. Jo took the slopes at the new point, (2.5, 1.5). The plane at (2, 1) uses the slopes at (2, 1). | correct | B24 |
| `screens[5].feedback.byKey.true` | That is the true value, $6.25 + 4.5$. The plane's estimate is a different number. | correct | B24 |
| `screens[5].feedback.byKey.half` | You took half of each step. The steps are 0.5 in full: $4 \times 0.5 = 2$ each. | correct | B24 |
| `screens[5].explain.text` | The tangent plane uses only what we know at (2, 1): the height 6 and the slopes 4 and 4. Jo's slopes come from the point we are trying to estimate,... | correct | B24 |
| `screens[6].prose` | Every time, you started from the height at $(a, b)$. Then you added one straight-line change per direction, with slopes taken at $(a, b)$: $$z = f(... | correct | B24 |
| `screens[6].question` | Which is the tangent plane of $g(x, y) = xy$ at (3, 2)? | correct | B24 |
| `screens[6].widget.options[0]` | option right (key): $z = 6 + 2(x - 3) + 3(y - 2)$ | correct | B24 |
| `screens[6].widget.options[1]` | option swap: $z = 6 + 3(x - 3) + 2(y - 2)$ | correct | B24 |
| `screens[6].widget.options[1].why` | You swapped the slopes. $g_x = y = 2$ and $g_y = x = 3$. | correct | B24 |
| `screens[6].widget.options[2]` | option vars: $z = 6 + y(x - 3) + x(y - 2)$ | correct | B24 |
| `screens[6].widget.options[2].why` | You left $g_x = y$ and $g_y = x$ unevaluated. Put in (3, 2), or the result is not flat. | correct | B24 |
| `screens[6].widget.options[3]` | option nobase: $z = 2(x - 3) + 3(y - 2)$ | correct | B24 |
| `screens[6].widget.options[3].why` | You dropped $g(3, 2) = 6$. The plane must pass through the surface's height there. | correct | B24 |
| `screens[6].feedback.correct` | $g = 6$, $g_x = 2$ and $g_y = 3$ at (3, 2). | correct | B24 |
| `screens[6].feedback.generic` | Not quite right. Evaluate $g$, $g_x$ and $g_y$ at (3, 2). | correct | B24 |
| `screens[6].explain.text` | $g(3, 2) = 6$, $g_x = y = 2$ and $g_y = x = 3$, all at (3, 2). Each slope multiplies its own step. | correct | B24 |
| `screens[7].prose` | Find the tangent plane of $f(x, y) = x^2y$ at (1, 3). The working so far: $$f(1, 3) = 3, \quad f_x = 2xy = 6, \quad f_y = x^2 = 1,$$ $$z = 3 + 6(x ... | correct | B24 |
| `screens[7].question` | Simplify the last line: $z = \;?$ | correct | B24 |
| `screens[7].widget.answer` | 6x+y-6 | correct | B24 |
| `screens[7].widget.accept` | 3+6(x-1)+(y-3), y+6x-6 | correct | B24 |
| `screens[7].widget.wrong[0]` | slip lost = 6x+y-3 | correct | B24 |
| `screens[7].widget.wrong[1]` | slip fy3 = 6x+3y-12 | correct | B24 |
| `screens[7].hints[0]` | Expand $6(x - 1)$. | correct | B24 |
| `screens[7].hints[1]` | $3 + 6x - 6 + y - 3$. | correct | B24 |
| `screens[7].hints[2]` | Collect the numbers: $3 - 6 - 3 = -6$. | correct | B24 |
| `screens[7].feedback.correct` | $z = 6x + y - 6$; at (1, 3) it gives 3, as it must. | correct | B24 |
| `screens[7].feedback.generic` | Not quite right. Expand, then collect the constant terms. | correct | B24 |
| `screens[7].feedback.byKey.lost` | You dropped one of the constants. $3 - 6 - 3 = -6$. | correct | B24 |
| `screens[7].feedback.byKey.fy3` | You used $f_y = 3$. At (1, 3), $f_y = x^2 = 1$. | correct | B24 |
| `screens[7].explain.text` | $3 + 6x - 6 + y - 3 = 6x + y - 6$. Check at (1, 3): $6 + 3 - 6 = 3 = f(1, 3)$. | correct | B24 |
| `screens[8].prose` | A call option on a £100 share is a function $V(S, \sigma)$ of the share price and its volatility. It has delta 0.6 (per £1 of share price) and vega... | correct | B24 |
| `screens[8].question` | Use the tangent plane: by how much does the option's value change? | correct | B24 |
| `screens[8].widget.answer` | 0.825 | correct | B24 |
| `screens[8].widget.accept` | $0.6(2) + 0.25(-1.5) = 1.2 - 0.375 = 0.825$ | correct | B24 |
| `screens[8].widget.wrong[0]` | slip nosign = 1.575 | correct | B24 |
| `screens[8].widget.wrong[1]` | slip delta = 1.2 | correct | B24 |
| `screens[8].widget.wrong[2]` | slip decimal = 1.196 | correct | B24 |
| `screens[8].hints[0]` | This is $\Delta V \approx \delta\,\Delta S + \mathcal V\,\Delta\sigma$: the tangent plane in $(S, \sigma)$. | correct | B24 |
| `screens[8].hints[1]` | $\Delta S = 2$ and $\Delta\sigma = -1.5$ points. | correct | B24 |
| `screens[8].hints[2]` | $1.2 - 0.375 = 0.825$. | correct | B24 |
| `screens[8].feedback.correct` | About £0.83: the share's rise outweighs the fall in volatility. | correct | B24 |
| `screens[8].feedback.generic` | Not quite right. Multiply each sensitivity by its move, signs included, and add. | correct | B24 |
| `screens[8].feedback.byKey.nosign` | Volatility fell, so the vega term is negative: $-0.375$. | correct | B24 |
| `screens[8].feedback.byKey.delta` | That is the delta term alone. The fall in volatility costs $0.25 \times 1.5 = 0.375$. | correct | B24 |
| `screens[8].feedback.byKey.decimal` | You wrote the volatility move as $-0.015$. Vega is quoted per point, so use $-1.5$. | correct | B24 |
| `screens[8].explain.text` | $\Delta V \approx \delta\,\Delta S + \mathcal V\,\Delta\sigma = 0.6(2) + 0.25(-1.5) = 0.825$, about £0.83. This is the tangent plane at today's $(S... | correct | B24 |
| `summary.ideas[0]` | Near $(a, b)$, $f$ is close to its tangent plane: the height there plus one straight-line change per direction. | correct | B24 |
| `summary.ideas[1]` | Every number in the plane is evaluated at $(a, b)$: the height and both slopes. | correct | B24 |
| `summary.ideas[2]` | The error shrinks with the square of the step: ten times closer, a hundred times smaller. | imprecise | finding 3: quadratic error needs continuous second partials (Marsden-Tromba 3.2 Theorem 2; Apostol II 9.10); for a merely "smooth" (C1) f the error is only o(step). Example |x|^1.5 in concepts-r2 script |
| `summary.formula.name` | Tangent plane | correct | B24 |
| `summary.formula.tex` | z = f(a, b) + f_x(a, b)(x - a) + f_y(a, b)(y - b) | correct | B24 |
| `summary.formula.note` | In finance: $\Delta V \approx \delta\,\Delta S + \mathcal V\,\Delta\sigma$. | correct | B24 |
| `summary.trap` | Taking the slopes at the new point $(x, y)$ instead of at $(a, b)$. You do not know those slopes, and the result is not a plane. | correct | B24 |
| `quiz[0].prose` | Let $f(x, y) = x^2 + y^2$. At (1, 2), $f = 5$, $f_x = 2$ and $f_y = 4$. | correct | B24 |
| `quiz[0].question` | What does the tangent plane at (1, 2) give for $f(1.1, 1.9)$? | correct | B24 |
| `quiz[0].widget.answer` | 4.8 | correct | B24 |
| `quiz[0].widget.accept` | $5 + 2(0.1) + 4(-0.1) = 4.8$ | correct | B24 |
| `quiz[0].widget.wrong[0]` | slip nosign = 5.6 | correct | B24 |
| `quiz[0].widget.wrong[1]` | slip exact = 4.82 | correct | B24 |
| `quiz[0].feedback.correct` | 4.8; the true value is 4.82. | correct | B24 |
| `quiz[0].feedback.generic` | Not quite right. Add each slope times its step, with signs, to 5. | correct | B24 |
| `quiz[0].feedback.byKey.nosign` | The $y$ step is $1.9 - 2 = -0.1$, so the $y$ term is $-0.4$. | correct | B24 |
| `quiz[0].feedback.byKey.exact` | That is the exact value. The plane's estimate is 4.8. | correct | B24 |
| `quiz[0].explain.text` | $z = 5 + 2(0.1) + 4(-0.1) = 4.8$. The exact value is $1.21 + 3.61 = 4.82$. | correct | B24 |
| `quiz[1].prose` | A tangent plane's error is 0.04 at a step of 0.2 from the point. | correct | B24 |
| `quiz[1].question` | Roughly what is the error at a step of 0.1 in the same direction? | correct | B24 |
| `quiz[1].widget.options[0]` | option right (key): 0.01 | correct | B24 |
| `quiz[1].widget.options[1]` | option half: 0.02 | correct | B24 |
| `quiz[1].widget.options[1].why` | You halved the error with the step. It scales with the step squared. | correct | B24 |
| `quiz[1].widget.options[2]` | option same: 0.04 | correct | B24 |
| `quiz[1].widget.options[2].why` | The error depends on the step: closer points are approximated better. | correct | B24 |
| `quiz[1].widget.options[3]` | option eighth: 0.005 | correct | B24 |
| `quiz[1].widget.options[3].why` | That scales with the step cubed. The tangent plane's error is quadratic. | imprecise | finding 3 (same defect): "the tangent plane's error is quadratic" stated without the hypothesis |
| `quiz[1].feedback.correct` | Half the step, a quarter of the error. | correct | B24 |
| `quiz[1].feedback.generic` | Not quite right. How does the error scale with the step? | correct | B24 |
| `quiz[1].explain.text` | The error is roughly proportional to the step squared. Halving the step divides it by 4: $0.04 / 4 = 0.01$. | correct | B24 |
| `quiz[2].prose` | Let $f(x, y) = x^2 + 2y^2$. | correct | B24 |
| `quiz[2].question` | What is the tangent plane at (0, 0)? | correct | B24 |
| `quiz[2].widget.options[0]` | option right (key): $z = 0$ | correct | B24 |
| `quiz[2].widget.options[1]` | option coef: $z = 2x + 4y$ | correct | B24 |
| `quiz[2].widget.options[1].why` | You used $f_x = 2x$ and $f_y = 4y$ without putting in (0, 0). Both are 0 there. | correct | B24 |
| `quiz[2].widget.options[2]` | option f: $z = x^2 + 2y^2$ | correct | B24 |
| `quiz[2].widget.options[2].why` | That is $f$ itself. A tangent plane is flat: no squares. | correct | B24 |
| `quiz[2].widget.options[3]` | option one: $z = 1$ | correct | B24 |
| `quiz[2].widget.options[3].why` | The plane passes through $f(0, 0) = 0$, not 1. | correct | B24 |
| `quiz[2].feedback.correct` | At a stationary point the tangent plane is flat. | correct | B24 |
| `quiz[2].feedback.generic` | Not quite right. Evaluate $f$, $f_x$ and $f_y$ at (0, 0). | correct | B24 |
| `quiz[2].explain.text` | $f(0, 0) = 0$ and both partials are 0, so $z = 0 + 0(x) + 0(y) = 0$. The plane sits flat on the bottom of the bowl. | correct | B24 |
| `quiz[3].prose` | An option has delta 0.45 and vega £0.12 per volatility point. The share rises £1 and volatility rises 2 points. | correct | B24 |
| `quiz[3].question` | Estimate the change in the option's value. | correct | B24 |
| `quiz[3].widget.answer` | 0.69 | correct | B24 |
| `quiz[3].widget.accept` | $0.45(1) + 0.12(2) = 0.69$ | correct | B24 |
| `quiz[3].widget.wrong[0]` | slip delta = 0.45 | correct | B24 |
| `quiz[3].widget.wrong[1]` | slip vega1 = 0.57 | correct | B24 |
| `quiz[3].feedback.correct` | About £0.69. | correct | B24 |
| `quiz[3].feedback.generic` | Not quite right. Add delta times the price move and vega times the volatility move. | correct | B24 |
| `quiz[3].feedback.byKey.delta` | That is delta alone. Volatility also rose, adding $0.12 \times 2 = 0.24$. | correct | B24 |
| `quiz[3].feedback.byKey.vega1` | You used one volatility point. The move is 2 points. | correct | B24 |
| `quiz[3].explain.text` | $\Delta V \approx 0.45(1) + 0.12(2) = 0.45 + 0.24 = 0.69$, so about £0.69. | correct | B24 |

## l8-walking-downhill

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Minimise a function with gradient descent in code, and choose a step size. | correct | B25 |
| `objectives[1]` | Explain why a step that is too big zigzags or diverges. | correct | B25 |
| `screens[0].prose` | On the bowl $f = x^2 + 2y^2$ you start at S = (4, 3), where $\nabla f = (8, 12)$. The orange arrow is $\nabla f / 10$, pointing uphill. To go down,... | correct | B25 |
| `screens[0].question` | Drag the blue point to where one step lands. | correct | B25 |
| `screens[0].hints[0]` | Work out $0.1 \times (8, 12)$ first. | correct | B25 |
| `screens[0].hints[1]` | Subtract $(0.8, 1.2)$ from (4, 3): the opposite way to the orange arrow. | correct | B25 |
| `screens[0].hints[2]` | $(4 - 0.8, 3 - 1.2) = (3.2, 1.8)$. | correct | B25 |
| `screens[0].feedback.correct` | (3.2, 1.8): $f$ falls from 34 to 16.72 in one step. | correct | B25 |
| `screens[0].feedback.generic` | Not quite right. Subtract $0.1 \times (8, 12)$ from (4, 3). | correct | B25 |
| `screens[0].feedback.byKey.uphill` | You added the step, so you climbed. Go against the gradient. | correct | B25 |
| `screens[0].feedback.byKey.xonly` | You moved only in $x$. The $y$ coordinate also changes, by $-1.2$. | correct | B25 |
| `screens[0].feedback.byKey.yonly` | You moved only in $y$. The $x$ coordinate also changes, by $-0.8$. | correct | B25 |
| `screens[0].explain.text` | $(4, 3) - 0.1(8, 12) = (3.2, 1.8)$, where $f = 10.24 + 6.48 = 16.72$. One step against the gradient more than halved $f$. | correct | B25 |
| `screens[1].prose` | Repeat the step ten times: at each new point, find $\nabla f$ and move by $-s\,\nabla f$. The slider sets the step size $s$. Watch the path and the... | correct | B25 |
| `screens[1].question` | Try $s = 0.05$, $0.3$ and $0.45$. Which statement fits what you see? | correct | B25 |
| `screens[1].widget.options[0]` | option right (key): 0.05 crawls, 0.3 lands almost at the bottom, 0.45 zigzags across the valley | correct | B25 |
| `screens[1].widget.options[1]` | option bigger: The bigger the step, the closer the path ends to the bottom | correct | B25 |
| `screens[1].widget.options[1].why` | Compare 0.3 with 0.45: the larger step bounces across the valley and ends further away. | correct | B25 |
| `screens[1].widget.options[2]` | option small: 0.05 ends closest, because small steps are the most accurate | correct | B25 |
| `screens[1].widget.options[2].why` | After 10 steps at 0.05 the path is still at about (1.4, 0.3). Small steps are safe but slow. | correct | B25 |
| `screens[1].hints[0]` | Read $f$ in the caption at each of the three settings. | correct | B25 |
| `screens[1].hints[1]` | At 0.45 the path jumps from one side of the $x$-axis to the other. | correct | B25 |
| `screens[1].feedback.correct` | Too small crawls, too big bounces; in between works best. | correct | B25 |
| `screens[1].feedback.generic` | Not quite right. Set each of the three step sizes and read $f$ after 10 steps. | correct | B25 |
| `screens[1].explain.text` | At 0.05 the path ends near (1.39, 0.32), $f \approx 2.15$. At 0.3 it ends almost at (0, 0). At 0.45 each $y$ step overshoots the valley floor, so t... | correct | B25 |
| `screens[2].prose` | This is **gradient descent**: from a point $\mathbf x_k$, step to $\mathbf x_{k+1} = \mathbf x_k - s\,\nabla f(\mathbf x_k)$, and repeat. With $s =... | correct | B25 |
| `screens[2].question` | Where does step 2 land? | correct | B25 |
| `screens[2].widget.options[0]` | option right (key): (2.56, 1.08) | correct | B25 |
| `screens[2].widget.options[1]` | option old: (2.4, 0.6) | correct | B25 |
| `screens[2].widget.options[1].why` | You reused $\nabla f(4, 3) = (8, 12)$. Recompute the gradient at (3.2, 1.8): it is (6.4, 7.2). | correct | B25 |
| `screens[2].widget.options[2]` | option up: (3.84, 2.52) | correct | B25 |
| `screens[2].widget.options[2].why` | You added $0.1\,\nabla f$, which climbs. Subtract it. | correct | B25 |
| `screens[2].widget.options[3]` | option noscale: (−3.2, −5.4) | correct | B25 |
| `screens[2].widget.options[3].why` | You subtracted the whole gradient. Scale it by the step size 0.1 first. | correct | B25 |
| `screens[2].hints[0]` | Find $\nabla f$ at (3.2, 1.8). | correct | B25 |
| `screens[2].hints[1]` | $\nabla f(3.2, 1.8) = (6.4, 7.2)$. | correct | B25 |
| `screens[2].hints[2]` | $(3.2, 1.8) - 0.1(6.4, 7.2) = (2.56, 1.08)$. | correct | B25 |
| `screens[2].feedback.correct` | (2.56, 1.08), the third dot on the path. | correct | B25 |
| `screens[2].feedback.generic` | Not quite right. Recompute the gradient at the new point, then step against it. | correct | B25 |
| `screens[2].explain.text` | At (3.2, 1.8) the gradient is $(2 \times 3.2, 4 \times 1.8) = (6.4, 7.2)$. Subtracting 0.1 of it gives (2.56, 1.08). The gradient is fresh at every... | correct | B25 |
| `screens[3].prose` | Now in Python. `descend(grad, x0, y0, step, n)` starts at `(x0, y0)` and takes `n` steps. `grad(x, y)` returns the pair `(f_x, f_y)`. Return the fi... | correct | B25 |
| `screens[3].question` | Complete `descend`. | correct | B25 |
| `screens[3].widget.solution` | def descend(grad, x0, y0, step, n): x, y = x0, y0 for _ in range(n): gx, gy = grad(x, y) x, y = x - step * gx, y - step * gy return x, y  | correct | B25 |
| `screens[3].widget.examples[0]` | descend(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 1) -> (3.2, 1.8) | correct | B26 |
| `screens[3].widget.examples[1]` | descend(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 2) -> (2.56, 1.08) | correct | B26 |
| `screens[3].widget.tests[0]` | descend(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 1) -> (3.2, 1.8) | correct | B26 |
| `screens[3].widget.tests[1]` | descend(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 2) -> (2.56, 1.08) | correct | B26 |
| `screens[3].widget.tests[2]` | descend(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 10) -> (0.4294967296000001, 0.018139852799999988) | correct | B26 |
| `screens[3].widget.tests[3]` | descend(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 0) -> (4, 3) | correct | B26 |
| `screens[3].widget.tests[4]` | descend(lambda x, y: (2 * (x - 1), 2 * (y + 2)), 0, 0, 0.25, 20) -> (0.9999990463256836, -1.9999980926513672) | correct | B26 |
| `screens[3].widget.tests[5]` | descend(lambda x, y: (2 * (x - y), -2 * (x - y) + 2 * y), 1, 1, 0.1, 5) -> (0.7827200000000001, 0.49312) | correct | B26 |
| `screens[3].widget.tests[6]` | descend(lambda x, y: (2 * x, 4 * y), 4, 3, 0.6, 10) -> (4.09599999999999e-07, 86.77639649279996) | correct | B26 |
| `screens[3].widget.how` | Check runs 7 hidden tests on three different functions, including 0 steps and a step that is too big. Each coordinate is accepted when `math.isclos... | correct | B25 |
| `screens[3].widget.mutants[0]` | mutant first fails test 1: adds `step * gx` and `step * gy`: walks uphill | correct | B26 |
| `screens[3].widget.mutants[1]` | mutant first fails test 1: `g = grad(x, y)` not unpacked: `step * g` raises a TypeError in test 1 | correct | B26 |
| `screens[3].widget.mutants[2]` | mutant first fails test 1: `gx = grad(x, y)` keeps the pair: `step * gx` raises a TypeError in test 1 | correct | B26 |
| `screens[3].widget.mutants[3]` | mutant first fails test 1: `(x, y) - step * grad(x, y)` on tuples raises a TypeError in test 1 | correct | B26 |
| `screens[3].hints[0]` | Loop `n` times with `for _ in range(n):`. | correct | B25 |
| `screens[3].hints[1]` | Inside the loop, call `grad(x, y)` at the current point. | correct | B25 |
| `screens[3].hints[2]` | `gx, gy = grad(x, y)` then `x, y = x - step * gx, y - step * gy`. | correct | B25 |
| `screens[3].feedback.correct` | Ten steps of 0.1 take you to about (0.43, 0.018). | correct | B25 |
| `screens[3].feedback.generic` | Not quite right. Read the first failing test. | correct | B25 |
| `screens[3].feedback.byKey.test-1` | Test 1 expects (3.2, 1.8) after one step. Unpack with `gx, gy = grad(x, y)`, then subtract `step * gx`, not add it. | correct | B27 |
| `screens[3].feedback.byKey.test-2` | Test 2 needs the gradient recomputed at the new point on every pass of the loop. | correct | B27 |
| `screens[3].feedback.byKey.test-4` | Test 4 takes 0 steps: the start point should come back unchanged. | correct | B27 |
| `screens[3].feedback.byKey.error` | Your code did not run. Check the colon after `for` and the indentation of the loop body. | correct | B27 |
| `screens[3].explain.text` | The gradient call sits inside the loop, so each step uses the slope where you stand. Test 7 uses step 0.6: $x$ settles but $y$ grows to about 86.8.... | correct | B25 |
| `screens[4].prose` | Back to the path. Below some step size the zigzag in $y$ dies away; above it the zigzag grows. Slide to find the boundary. | correct | B25 |
| `screens[4].question` | Set the step where the $y$ zigzag neither grows nor shrinks. | correct | B25 |
| `screens[4].widget.answer` | 0.5 | correct | B25 |
| `screens[4].hints[0]` | A zigzag of constant size flips the sign of $y$ but keeps its size. | correct | B25 |
| `screens[4].hints[1]` | Watch the dots near the $x$-axis: once $s$ passes 0.25, their $y$ values flip sign each step. | correct | B25 |
| `screens[4].hints[2]` | $s = 0.5$: $y$ goes 3, $-3$, 3, $-3$, ... | correct | B25 |
| `screens[4].feedback.correct` | At $s = 0.5$, $y$ flips between 3 and $-3$ for ever. | correct | B25 |
| `screens[4].feedback.generic` | Not quite right. Find the step where each $y$ step lands at minus the old $y$. | correct | B25 |
| `screens[4].feedback.byKey.onset` | Near 0.25 the zigzag starts, since $1 - 4s$ turns negative. It still shrinks there. | correct | B25 |
| `screens[4].feedback.byKey.past` | There the zigzag already grows: $\|1 - 4s\| > 1$. Come back down a little. | correct | B25 |
| `screens[4].explain.text` | At $s = 0.5$ the factor is $1 - 4(0.5) = -1$: $y$ bounces between 3 and $-3$. Above 0.5 the factor's size passes 1 and the path flies off. That is ... | correct | B25 |
| `screens[5].prose` | Sam's version returns a point far from the bottom, and more steps make it worse. | correct | B25 |
| `screens[5].question` | Tap the line with the bug. | correct | B25 |
| `screens[5].widget.answer` | l5 | correct | B25 |
| `screens[5].hints[0]` | Is the path going up or down? $f$ at the end is huge. | correct | B25 |
| `screens[5].hints[1]` | The direction of each step is set on one line. | correct | B25 |
| `screens[5].hints[2]` | Line 5 adds `step * gx`. Descent subtracts it. | correct | B25 |
| `screens[5].feedback.correct` | Line 5 steps along $+\nabla f$: uphill. | correct | B25 |
| `screens[5].feedback.generic` | Not quite right. Find the line that decides which way each step goes. | correct | B25 |
| `screens[5].feedback.byKey.l4` | Line 4 is fine: it finds the gradient at the current point. The trouble is what is done with it. | correct | B25 |
| `screens[5].feedback.byKey.l3` | The loop runs `n` times, as it should. Look at the update inside it. | correct | B25 |
| `screens[5].feedback.byKey.l2` | Starting at `(x0, y0)` is right. Look at how each step moves the point. | correct | B25 |
| `screens[5].feedback.byKey.l6` | Returning the point is right. The point is wrong before it gets here. | correct | B25 |
| `screens[5].explain.text` | Line 5 climbs along $+\nabla f$, so $x$ is multiplied by 1.2 and $y$ by 1.4 each step. The fix is `x - step * gx, y - step * gy`. A growing $f$ in ... | correct | B25 |
| `screens[6].prose` | Why does the limit sit at 0.5? Follow $y$ alone. The $y$ part of the gradient is $f_y = 4y$, so one step gives $$y_{\text{new}} = y - s(4y).$$ | correct | B25 |
| `screens[6].question` | Factor out $y$: $y_{\text{new}} = (\;?\;)\,y$. Enter the factor. | correct | B25 |
| `screens[6].widget.answer` | 1-4s | correct | B25 |
| `screens[6].widget.accept` | -4s+1, 1-4*s | correct | B25 |
| `screens[6].widget.wrong[0]` | slip x = 1-2s | correct | B25 |
| `screens[6].widget.wrong[1]` | slip sign = 1+4s | correct | B25 |
| `screens[6].hints[0]` | $y - 4sy = y(\;\cdot\;)$. | correct | B25 |
| `screens[6].hints[1]` | Take $y$ out of both terms. | correct | B25 |
| `screens[6].hints[2]` | $y - 4sy = (1 - 4s)\,y$. | correct | B25 |
| `screens[6].feedback.correct` | $(1 - 4s)$: each step multiplies $y$ by it, so $y_k = 3(1 - 4s)^k$. | correct | B25 |
| `screens[6].feedback.generic` | Not quite right. Take $y$ out of both terms of $y - 4sy$. | correct | B25 |
| `screens[6].feedback.byKey.x` | $1 - 2s$ is the factor for $x$, from $f_x = 2x$. For $y$ the slope is $4y$. | correct | B25 |
| `screens[6].feedback.byKey.sign` | Descent subtracts the step, so the factor is $1 - 4s$. | correct | B25 |
| `screens[6].explain.text` | $y_k = 3(1 - 4s)^k$ shrinks only if $\|1 - 4s\| < 1$, that is $0 < s < 0.5$. The factor is negative once $s > 0.25$, which is the zigzag. For $x$ t... | correct | B25 |
| `screens[7].prose` | Gradient descent repeats $\mathbf x_{k+1} = \mathbf x_k - s\,\nabla f(\mathbf x_k)$. On a bowl $ax^2 + by^2$ each coordinate is multiplied by $1 - ... | correct | B25 |
| `screens[7].question` | For $f = 3x^2 + y^2$, which steps make gradient descent settle? | correct | B25 |
| `screens[7].widget.options[0]` | option right (key): $0 < s < \tfrac13$ | correct | B25 |
| `screens[7].widget.options[1]` | option y: $0 < s < 1$ | correct | B25 |
| `screens[7].widget.options[1].why` | That is the limit for $y$, factor $1 - 2s$. The $x$ factor $1 - 6s$ fails first. | correct | B25 |
| `screens[7].widget.options[2]` | option best: Only $s = \tfrac16$ | correct | B25 |
| `screens[7].widget.options[2].why` | At $\tfrac16$ the $x$ factor is 0, but the $y$ factor is $\tfrac23$. Every $s$ below $\tfrac13$ settles, and $s = \tfrac14$ is faster: both factors... | correct | B25 |
| `screens[7].widget.options[3]` | option any: Any $s > 0$, because each step goes downhill | correct | B25 |
| `screens[7].widget.options[3].why` | Each direction is downhill, but a long step overshoots the valley floor and lands higher. | correct | B25 |
| `screens[7].feedback.correct` | $\|1 - 6s\| < 1$ needs $s < \tfrac13$, and that also keeps $\|1 - 2s\| < 1$. | correct | B25 |
| `screens[7].feedback.generic` | Not quite right. Write each coordinate's factor and require both to lie between $-1$ and 1. | correct | B25 |
| `screens[7].explain.text` | $f_x = 6x$ gives the factor $1 - 6s$ and $f_y = 2y$ gives $1 - 2s$. Both lie in $(-1, 1)$ only when $0 < s < \tfrac13$. | correct | B25 |
| `screens[8].prose` | Six days of returns, in %: the market `xs` and a stock `ys`. We fit $y \approx a + bx$ by gradient descent on the mean squared error $$L(a, b) = \f... | correct | B28 |
| `screens[8].question` | Complete `fit_line(xs, ys, step, n)`, starting from $a = b = 0$ and returning `(a, b)`. | correct | B28 |
| `screens[8].widget.solution` | def fit_line(xs, ys, step, n): a, b = 0.0, 0.0 m = len(xs) for _ in range(n): r = [a + b * x - y for x, y in zip(xs, ys)] ga = 2 / m * sum(r) gb = ... | correct | B28 |
| `screens[8].widget.examples[0]` | fit_line([-1.2, 0.4, 1.0, -0.6, 1.8, 0.2], [-1.5, 0.7, 1.1, -0.4, 2.3, 0.0], 0.1, 1) -> (0.07333333333333333, 0.252) | correct | B26 |
| `screens[8].widget.tests[0]` | fit_line([-1.2, 0.4, 1.0, -0.6, 1.8, 0.2], [-1.5, 0.7, 1.1, -0.4, 2.3, 0.0], 0.1, 1) -> (0.07333333333333333, 0.252) | correct | B26 |
| `screens[8].widget.tests[1]` | fit_line([-1.2, 0.4, 1.0, -0.6, 1.8, 0.2], [-1.5, 0.7, 1.1, -0.4, 2.3, 0.0], 0.1, 3) -> (0.14430544592592592, 0.600233728) | correct | B26 |
| `screens[8].widget.tests[2]` | fit_line([-1.2, 0.4, 1.0, -0.6, 1.8, 0.2], [-1.5, 0.7, 1.1, -0.4, 2.3, 0.0], 0.1, 0) -> (0.0, 0.0) | correct | B26 |
| `screens[8].widget.tests[3]` | fit_line([-1.2, 0.4, 1.0, -0.6, 1.8, 0.2], [-1.5, 0.7, 1.1, -0.4, 2.3, 0.0], 0.1, 3000) -> (0.04678899082568805, 1.1995412844036697) | correct | B26 |
| `screens[8].widget.tests[4]` | fit_line([0, 1, 2, 3], [0.5, 2.5, 4.5, 6.5], 0.05, 3000) -> (0.5, 2.0) | correct | B26 |
| `screens[8].widget.tests[5]` | fit_line([-2.0, -1.0, 0.5, 1.5, 2.5], [1.1, 0.4, -0.2, -0.5, -1.4], 0.05, 3000) -> (0.03270676691729324, -0.5090225563909774) | correct | B26 |
| `screens[8].widget.how` | Check runs 6 hidden tests. Three check 0, 1 and 3 steps exactly. Three run 3,000 steps and compare with the exact least-squares line, which the des... | correct | B28 |
| `screens[8].widget.mutants[0]` | mutant first fails test 1: $a$ updated first, so $b$ sees new residuals | correct | B26 |
| `screens[8].widget.mutants[1]` | mutant first fails test 1: $b$ updated first, so $a$ sees new residuals | correct | B26 |
| `screens[8].widget.mutants[2]` | mutant first fails test 1: residuals rebuilt between the $a$ and $b$ updates | correct | B26 |
| `screens[8].widget.mutants[3]` | mutant first fails test 1: factor $1/m$ in place of $2/m$ | correct | B26 |
| `screens[8].widget.mutants[4]` | mutant first fails test 1: steps with the gradient, uphill | correct | B26 |
| `screens[8].widget.mutants[5]` | mutant first fails test 2: residuals built once, before the loop | correct | B26 |
| `screens[8].widget.mutants[6]` | mutant first fails test 2: gradient computed once, before the loop | correct | B26 |
| `screens[8].widget.mutants[7]` | mutant first fails test 2: one jump of `n * step` along the starting gradient | correct | B26 |
| `screens[8].widget.mutants[8]` | mutant first fails test 4: stops when both partials are below 1e-6 | correct | B26 |
| `screens[8].widget.mutants[9]` | mutant first fails test 4: stops when the gradient length is below 1e-8 | correct | B26 |
| `screens[8].widget.mutants[10]` | mutant first fails test 4: stops when a step moves $a$ and $b$ by under 1e-7 | correct | B26 |
| `screens[8].hints[0]` | Build the list of residuals at the top of each pass. | correct | B28 |
| `screens[8].hints[1]` | `ga = 2 / m * sum(r)` and `gb = 2 / m * sum(ri * x for ri, x in zip(r, xs))`. | correct | B28 |
| `screens[8].hints[2]` | Then `a, b = a - step * ga, b - step * gb`, both from the same residuals. | correct | B28 |
| `screens[8].feedback.correct` | Beta about 1.20, alpha about 0.047% a day. | correct | B28 |
| `screens[8].feedback.generic` | Not quite right. Read the first failing test. | correct | B28 |
| `screens[8].feedback.byKey.test-1` | Test 1 is one step from (0, 0), expecting (0.0733, 0.252). Check the factor $2/m$, the sign, and that $b$ uses the same residuals as $a$. | correct | B27 |
| `screens[8].feedback.byKey.test-2` | Test 2 is three steps. Rebuild the residuals inside the loop, from the current $a$ and $b$, on every pass. | correct | B27 |
| `screens[8].feedback.byKey.test-4` | Test 4 runs 3,000 steps and expects the least-squares line. Take all `n` steps: do not stop early when the gradient gets small. | correct | B27 |
| `screens[8].feedback.byKey.error` | Your code stopped with an error. Replace `pass` with the update, and keep the loop body indented. | correct | B27 |
| `screens[8].explain.text` | After 3,000 steps the line is $y \approx 0.047 + 1.200x$: the stock moves about 1.2% for each 1% of the market. Regression has a formula for this c... | correct | B28 |
| `summary.ideas[0]` | Gradient descent steps against the gradient, recomputed at every point: $\mathbf x_{k+1} = \mathbf x_k - s\,\nabla f(\mathbf x_k)$. | correct | B25 |
| `summary.ideas[1]` | Too small a step crawls; too big a step zigzags across the valley or flies off. | correct | B25 |
| `summary.ideas[2]` | On a bowl each coordinate is multiplied by $1 - 2as$ per step, so the steepest direction caps the step size. | correct | B25 |
| `summary.formula.name` | Gradient descent | correct | B25 |
| `summary.formula.tex` | \mathbf x_{k+1} = \mathbf x_k - s\,\nabla f(\mathbf x_k) | correct | B25 |
| `summary.formula.note` | For $x^2 + 2y^2$ it settles only for $0 < s < 0.5$. | correct | B25 |
| `summary.trap` | Writing `x + step * gx` walks uphill. Descent subtracts the gradient. | correct | B25 |
| `quiz[0].prose` | Let $f(x, y) = (x - 1)^2 + y^2$. You start at (3, 2) with step size 0.25. | correct | B25 |
| `quiz[0].question` | Where does one step of gradient descent land? | correct | B25 |
| `quiz[0].widget.options[0]` | option right (key): (2, 1) | correct | B25 |
| `quiz[0].widget.options[1]` | option up: (4, 3) | correct | B25 |
| `quiz[0].widget.options[1].why` | You added the step. Descent subtracts $s\,\nabla f$. | correct | B25 |
| `quiz[0].widget.options[2]` | option noscale: (−1, −2) | correct | B25 |
| `quiz[0].widget.options[2].why` | You subtracted the whole gradient (4, 4). Scale it by 0.25 first. | correct | B25 |
| `quiz[0].widget.options[3]` | option grad: (2.5, 1.5) | correct | B25 |
| `quiz[0].widget.options[3].why` | You used $\nabla f = (2, 2)$. With $f_x = 2(x - 1)$ and $f_y = 2y$, at (3, 2) it is (4, 4). | correct | B25 |
| `quiz[0].feedback.correct` | $(3, 2) - 0.25(4, 4) = (2, 1)$. | correct | B25 |
| `quiz[0].feedback.generic` | Not quite right. Compute $\nabla f(3, 2)$, scale by 0.25, subtract. | correct | B25 |
| `quiz[0].explain.text` | $\nabla f = (2(x - 1), 2y) = (4, 4)$ at (3, 2). One step: $(3, 2) - 0.25(4, 4) = (2, 1)$. | correct | B25 |
| `quiz[1].prose` | Gradient descent on $f = x^2 + 2y^2$ with step $s = 0.3$. | correct | B25 |
| `quiz[1].question` | What happens to $y$ over the steps? | correct | B25 |
| `quiz[1].widget.options[0]` | option right (key): It flips sign each step and shrinks to 0 | correct | B25 |
| `quiz[1].widget.options[1]` | option smooth: It shrinks smoothly without changing sign | correct | B25 |
| `quiz[1].widget.options[1].why` | The factor is $1 - 4(0.3) = -0.2$. A negative factor flips the sign. | correct | B25 |
| `quiz[1].widget.options[2]` | option grow: It flips sign and grows | correct | B25 |
| `quiz[1].widget.options[2].why` | The factor $-0.2$ has size below 1, so the flips shrink. | correct | B25 |
| `quiz[1].widget.options[3]` | option stuck: It stays at its starting value | correct | B25 |
| `quiz[1].widget.options[3].why` | Only a factor of 1 would keep it. Here it is $-0.2$. | correct | B25 |
| `quiz[1].feedback.correct` | Factor $-0.2$: a shrinking zigzag. | correct | B25 |
| `quiz[1].feedback.generic` | Not quite right. Compute the factor $1 - 4s$. | correct | B25 |
| `quiz[1].explain.text` | Each step multiplies $y$ by $1 - 4(0.3) = -0.2$. The sign flips and the size falls by a factor of 5. | correct | B25 |
| `quiz[2].prose` | Gradient descent on $f = x^2 + 2y^2$ from (4, 3) with step 0.6 ends, after 10 steps, near $(0, 86.8)$. | correct | B25 |
| `quiz[2].question` | What went wrong? | correct | B25 |
| `quiz[2].widget.options[0]` | option right (key): The step is too big: $y$ is multiplied by $-1.4$ each time | correct | B25 |
| `quiz[2].widget.options[1]` | option sign: The code steps uphill | correct | B25 |
| `quiz[2].widget.options[1].why` | Then $x$ would grow too, but $x$ went to 0. The $y$ step is too long. | correct | B25 |
| `quiz[2].widget.options[2]` | option few: Ten steps are too few | correct | B25 |
| `quiz[2].widget.options[2].why` | More steps make it worse: $\|{-1.4}\|^k$ grows. | correct | B25 |
| `quiz[2].widget.options[3]` | option start: The start (4, 3) is too far from the bottom | correct | B25 |
| `quiz[2].widget.options[3].why` | The start hardly matters: a factor of size above 1 grows from any start with $y \neq 0$. | correct | B25 |
| `quiz[2].feedback.correct` | $\|1 - 4(0.6)\| = 1.4 > 1$. | correct | B25 |
| `quiz[2].feedback.generic` | Not quite right. Compute the factor for $y$, $1 - 4s$. | correct | B25 |
| `quiz[2].explain.text` | $x$ shrinks by $1 - 1.2 = -0.2$ each step, but $y$ is multiplied by $1 - 2.4 = -1.4$. So $y$ grows to $3 \times 1.4^{10} \approx 86.8$. | correct | B25 |

## review-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Let $f(x, y) = 3x^2 - xy + y^2$. | correct | B29 |
| `items[0].question` | What is $\nabla f$ at (1, 2), and how steep is the steepest climb there? | correct | B29 |
| `items[0].widget.options[0]` | option right (key): $(4, 3)$, slope 5 | correct | B29 |
| `items[0].widget.options[1]` | option noxy: $(6, 4)$, slope 7.2 | correct | B29 |
| `items[0].widget.options[1].why` | You dropped the $-xy$ term. Its partials are $-y$ and $-x$. | correct | B29 |
| `items[0].widget.options[2]` | option sum: $(4, 3)$, slope 7 | correct | B29 |
| `items[0].widget.options[2].why` | You added the components. The steepest slope is the length, $\sqrt{16 + 9} = 5$. | correct | B29 |
| `items[0].widget.options[3]` | option swap: $(3, 4)$, slope 5 | correct | B29 |
| `items[0].widget.options[3].why` | You swapped the components: $f_x = 6x - y = 4$ comes first. | correct | B29 |
| `items[0].feedback.correct` | $f_x = 6x - y = 4$, $f_y = -x + 2y = 3$, length 5. | correct | B29 |
| `items[0].feedback.generic` | Not quite right. Find each partial, put in (1, 2), then take the length. | correct | B29 |
| `items[0].explain.text` | $f_x = 6x - y = 6 - 2 = 4$ and $f_y = -x + 2y = -1 + 4 = 3$. The steepest climb is along (4, 3) with slope $\sqrt{4^2 + 3^2} = 5$. | correct | B29 |
| `items[1].prose` | Let $f(x, y) = x^2 + y^2$. You stand at (3, 4). | correct | B29 |
| `items[1].question` | What is the slope of $f$ in the direction of the origin? | correct | B29 |
| `items[1].widget.answer` | -10 | correct | B29 |
| `items[1].widget.accept` | $\nabla f = (6, 8)$, $\mathbf u = (-0.6, -0.8)$: $-3.6 - 6.4 = -10$ | correct | B29 |
| `items[1].widget.wrong[0]` | slip sign = 10 | correct | B29 |
| `items[1].widget.wrong[1]` | slip raw = -50 | correct | B29 |
| `items[1].feedback.correct` | $-10$: straight downhill, as steep as it gets. | correct | B29 |
| `items[1].feedback.generic` | Not quite right. Make the arrow to the origin a unit arrow, then take the dot product with $\nabla f$. | correct | B29 |
| `items[1].feedback.byKey.sign` | Heading to the origin lowers $f$, so the slope is negative. | correct | B29 |
| `items[1].feedback.byKey.raw` | You used $(-3, -4)$ without dividing by its length 5. | correct | B29 |
| `items[1].explain.text` | The arrow to the origin is $(-3, -4)$, of length 5, so $\mathbf u = (-0.6, -0.8)$. Then $D_{\mathbf u} f = 6(-0.6) + 8(-0.8) = -10 = -\|\nabla f\|$... | correct | B29 |
| `items[2].prose` | Let $f(x, y) = xy^2$. At (2, 1), $f = 2$, $f_x = y^2 = 1$ and $f_y = 2xy = 4$. | correct | B29 |
| `items[2].question` | Use the tangent plane at (2, 1) to estimate $f(2.1, 0.9)$. | correct | B29 |
| `items[2].widget.answer` | 1.7 | correct | B29 |
| `items[2].widget.accept` | $2 + 1(0.1) + 4(-0.1) = 1.7$; the true value is 1.701 | correct | B29 |
| `items[2].widget.wrong[0]` | slip nosign = 2.5 | correct | B29 |
| `items[2].widget.wrong[1]` | slip exact = 1.701 | correct | B29 |
| `items[2].feedback.correct` | 1.7, against a true 1.701. | correct | B29 |
| `items[2].feedback.generic` | Not quite right. Add each slope times its signed step to 2. | correct | B29 |
| `items[2].feedback.byKey.nosign` | The $y$ step is $0.9 - 1 = -0.1$, so its term is $-0.4$. | correct | B29 |
| `items[2].feedback.byKey.exact` | That is the exact value. The plane gives 1.7. | correct | B29 |
| `items[2].explain.text` | $z = 2 + 1(0.1) + 4(-0.1) = 1.7$. The true value is $2.1 \times 0.81 = 1.701$. | correct | B29 |
| `items[3].prose` | Gradient descent on $f(x, y) = x^2 + 4y^2$ with step 0.1 starts at (2, 1). | correct | B29 |
| `items[3].question` | Where is the point after one step? | correct | B29 |
| `items[3].widget.options[0]` | option right (key): (1.6, 0.2) | correct | B29 |
| `items[3].widget.options[1]` | option up: (2.4, 1.8) | correct | B29 |
| `items[3].widget.options[1].why` | You added $0.1\,\nabla f$, which climbs. | correct | B29 |
| `items[3].widget.options[2]` | option half: (1.6, 0.6) | correct | B29 |
| `items[3].widget.options[2].why` | You used $f_y = 4y$. For $4y^2$ the derivative is $8y = 8$. | correct | B29 |
| `items[3].widget.options[3]` | option noscale: (−2, −7) | correct | B29 |
| `items[3].widget.options[3].why` | You subtracted the whole gradient. Scale by 0.1 first. | correct | B29 |
| `items[3].feedback.correct` | $(2, 1) - 0.1(4, 8) = (1.6, 0.2)$. | correct | B29 |
| `items[3].feedback.generic` | Not quite right. Find $\nabla f(2, 1)$, scale by 0.1 and subtract. | correct | B29 |
| `items[3].explain.text` | $\nabla f = (2x, 8y) = (4, 8)$ at (2, 1). One step gives $(2 - 0.4, 1 - 0.8) = (1.6, 0.2)$. | correct | B29 |
| `items[4].prose` | Let $f(x, y) = x^2 - y^2$. The point (2, 1) is on the contour $f = 3$. | correct | B29 |
| `items[4].question` | Which arrow points along that contour at (2, 1)? | correct | B29 |
| `items[4].widget.options[0]` | option grad: $(4, -2)$ | correct | B29 |
| `items[4].widget.options[0].why` | That is $\nabla f(2, 1)$, at right angles to the contour. | correct | B29 |
| `items[4].widget.options[1]` | option right (key): $(1, 2)$ | correct | B29 |
| `items[4].widget.options[2]` | option radial: $(2, 1)$ | correct | B29 |
| `items[4].widget.options[2].why` | That points away from the origin. It is not perpendicular to $\nabla f$: $4(2) - 2(1) = 6 \ne 0$. | correct | B29 |
| `items[4].widget.options[3]` | option signs: $(1, -2)$ | correct | B29 |
| `items[4].widget.options[3].why` | Check: $4(1) + (-2)(-2) = 8$, not 0. That arrow is not perpendicular to $\nabla f$. | correct | B29 |
| `items[4].feedback.correct` | $(4, -2) \cdot (1, 2) = 0$: along the contour. | correct | B29 |
| `items[4].feedback.generic` | Not quite right. Find $\nabla f(2, 1)$, then an arrow whose dot product with it is 0. | correct | B29 |
| `items[4].explain.text` | $\nabla f(2, 1) = (4, -2)$. A tangent to the contour is perpendicular to it: $(1, 2)$ gives $4 - 4 = 0$. | correct | B29 |
| `items[5].prose` | At a point, $\nabla f = (3, 4)$. | correct | B29 |
| `items[5].question` | Along which unit arrows is $D_{\mathbf u} f = 0$? Select all that apply. | correct | B29 |
| `items[5].widget.options[0]` | option a (key): $(0.8, -0.6)$ | correct | B29 |
| `items[5].widget.options[1]` | option b (key): $(-0.8, 0.6)$ | correct | B29 |
| `items[5].widget.options[2]` | option c: $(4, -3)$ | correct | B29 |
| `items[5].widget.options[2].why` | It is level, but its length is 5. A direction $\mathbf u$ must have length 1. | correct | B29 |
| `items[5].widget.options[3]` | option d: $(0.6, 0.8)$ | correct | B29 |
| `items[5].widget.options[3].why` | That is the gradient's own direction, where the slope is largest: 5. | correct | B29 |
| `items[5].feedback.correct` | Both run along the contour, one each way. | correct | B29 |
| `items[5].feedback.generic` | Not quite right. You need $3u_1 + 4u_2 = 0$ and length 1. | correct | B29 |
| `items[5].explain.text` | $3u_1 + 4u_2 = 0$ means $\mathbf u$ is a multiple of $(4, -3)$. The unit arrows are $\pm(0.8, -0.6)$: the two ways along the contour. | correct | B29 |
| `items[6].prose` | Gradient descent on $f(x, y) = 2x^2 + 5y^2$ with a fixed step $s$. | correct | B29 |
| `items[6].question` | Above what step size does it fail to settle? | correct | B29 |
| `items[6].widget.answer` | 0.2 | correct | B29 |
| `items[6].widget.accept` | $f_y = 10y$ gives the factor $1 - 10s$; $\|1 - 10s\| < 1$ needs $s < 0.2$ | correct | B29 |
| `items[6].widget.wrong[0]` | slip x = 0.5 | correct | B29 |
| `items[6].widget.wrong[1]` | slip best = 0.1 | correct | B29 |
| `items[6].feedback.correct` | 0.2: the steep $y$ direction sets the limit. | correct | B29 |
| `items[6].feedback.generic` | Not quite right. Write each coordinate's factor and require its size below 1. | correct | B29 |
| `items[6].feedback.byKey.x` | 0.5 is the limit for $x$, factor $1 - 4s$. The $y$ factor $1 - 10s$ fails first. | correct | B29 |
| `items[6].feedback.byKey.best` | At 0.1 the $y$ factor is 0: a perfect $y$ step, not the limit. | correct | B29 |
| `items[6].explain.text` | $x$ is multiplied by $1 - 4s$ and $y$ by $1 - 10s$. Both stay inside $(-1, 1)$ only for $0 < s < 0.2$. | correct | B29 |
| `items[7].prose` | A call on a £100 share has delta 0.55 and vega £0.18 per volatility point. The share falls £3 and volatility rises 4 points. | correct | B29 |
| `items[7].question` | Estimate the change in the option's value. | correct | B29 |
| `items[7].widget.answer` | -0.93 | correct | B29 |
| `items[7].widget.accept` | $0.55(-3) + 0.18(4) = -1.65 + 0.72 = -0.93$ | correct | B29 |
| `items[7].widget.wrong[0]` | slip nosign = 2.37 | correct | B29 |
| `items[7].widget.wrong[1]` | slip delta = -1.65 | correct | B29 |
| `items[7].widget.wrong[2]` | slip sign = 0.93 | correct | B29 |
| `items[7].feedback.correct` | About −£0.93: the price fall outweighs the volatility rise. | correct | B29 |
| `items[7].feedback.generic` | Not quite right. Add delta times the price move and vega times the volatility move, signs included. | correct | B29 |
| `items[7].feedback.byKey.nosign` | The share fell, so the delta term is $-1.65$. | correct | B29 |
| `items[7].feedback.byKey.delta` | That is the delta term alone. The volatility rise adds $0.18 \times 4 = 0.72$. | correct | B29 |
| `items[7].feedback.byKey.sign` | The delta term is 0.55 × (−3) = −1.65, and vega adds back only 0.72, so the sum is below zero. A positive 0.93 books the loss as a gain. | correct | B29 |
| `items[7].explain.text` | $\Delta V \approx \delta\,\Delta S + \mathcal V\,\Delta\sigma = 0.55(-3) + 0.18(4) = -0.93$. The option loses about 93p. | correct | B29 |

## homework-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Two assets have volatilities 30% and 15% and correlation $-0.2$. So $\boldsymbol\Sigma = \begin{pmatrix} 0.09 & -0.009 \\ -0.009 & 0.0225 \end{pmat... | correct | B30 |
| `items[0].question` | What is $\dfrac{\partial V}{\partial w_1}$? | correct | B30 |
| `items[0].widget.answer` | 0.1008 | correct | B30 |
| `items[0].widget.accept` | $2(0.09 \times 0.6 - 0.009 \times 0.4) = 2(0.0504) = 0.1008$ | correct | B30 |
| `items[0].widget.wrong[0]` | slip half = 0.0504 | correct | B30 |
| `items[0].widget.wrong[1]` | slip nocov = 0.108 | correct | B30 |
| `items[0].feedback.correct` | 0.1008. With $\partial V / \partial w_2 = 0.0072$, adding asset 1 raises risk far faster. | correct | B30 |
| `items[0].feedback.generic` | Not quite right. Use $\nabla V = 2\boldsymbol\Sigma\mathbf w$ and take its first component. | correct | B30 |
| `items[0].feedback.byKey.half` | That is $(\boldsymbol\Sigma\mathbf w)_1$. The gradient of $\mathbf w^T\boldsymbol\Sigma\mathbf w$ is twice it. | correct | B30 |
| `items[0].feedback.byKey.nocov` | You dropped the covariance term $-0.009 w_2$. | correct | B30 |
| `items[0].explain.text` | Row 1 of $\boldsymbol\Sigma\mathbf w$ is $0.09(0.6) - 0.009(0.4) = 0.0504$, so $\partial V / \partial w_1 = 0.1008$. Row 2 gives $\partial V / \par... | correct | B30 |
| `items[1].prose` | Let $f(x, y) = x^3 - 3xy$. | correct | B30 |
| `items[1].question` | What is the slope of $f$ at (1, 2) in the direction of the arrow (2, 1)? | correct | B30 |
| `items[1].widget.answer` | -4.025 | correct | B30 |
| `items[1].widget.accept` | $\nabla f = (-3, -3)$, $\mathbf u = (2, 1)/\sqrt 5$: $-9/\sqrt 5 \approx -4.025$ | correct | B30 |
| `items[1].widget.wrong[0]` | slip raw = -9 | correct | B30 |
| `items[1].widget.wrong[1]` | slip grad = 4.243 | correct | B30 |
| `items[1].widget.wrong[2]` | slip sign = 4.025 | correct | B30 |
| `items[1].feedback.correct` | $-9/\sqrt5 \approx -4.02$. | correct | B30 |
| `items[1].feedback.generic` | Not quite right. Find $\nabla f(1, 2)$, divide the arrow by its length, then take the dot product. | correct | B30 |
| `items[1].feedback.byKey.raw` | You used (2, 1) without dividing by its length $\sqrt5$. | correct | B30 |
| `items[1].feedback.byKey.grad` | That is $\|\nabla f\|$, the steepest slope. (2, 1) is not the gradient's direction. | correct | B30 |
| `items[1].feedback.byKey.sign` | Both components of the gradient are −3, so (−6 − 3)/√5 is negative. A positive 4.025 drops the minus signs of the gradient. | correct | B30 |
| `items[1].explain.text` | $f_x = 3x^2 - 3y = -3$ and $f_y = -3x = -3$ at (1, 2). With $\mathbf u = (2, 1)/\sqrt5$, $D_{\mathbf u} f = (-6 - 3)/\sqrt5 \approx -4.025$. | correct | B30 |
| `items[2].prose` | Let $f(x, y) = x^2y - y^3$. | correct | B30 |
| `items[2].question` | Find the tangent plane at (2, 1). Enter $z$ in terms of $x$ and $y$. | correct | B30 |
| `items[2].widget.answer` | 4x+y-6 | correct | B30 |
| `items[2].widget.accept` | 3+4(x-2)+(y-1), y+4x-6 | correct | B30 |
| `items[2].widget.wrong[0]` | slip fy = 4x+7y-12 | correct | B30 |
| `items[2].widget.wrong[1]` | slip nobase = 4x+y-9 | correct | B30 |
| `items[2].feedback.correct` | $z = 4x + y - 6$. | correct | B30 |
| `items[2].feedback.generic` | Not quite right. Find $f$, $f_x$ and $f_y$ at (2, 1), build the plane, then simplify. | correct | B30 |
| `items[2].feedback.byKey.fy` | You used $f_y = x^2 + 3y^2 = 7$. The derivative of $-y^3$ is $-3y^2$. | correct | B30 |
| `items[2].feedback.byKey.nobase` | You dropped $f(2, 1) = 3$. | correct | B30 |
| `items[2].explain.text` | $f(2, 1) = 4 - 1 = 3$, $f_x = 2xy = 4$ and $f_y = x^2 - 3y^2 = 1$. So $z = 3 + 4(x - 2) + (y - 1) = 4x + y - 6$. | correct | B30 |
| `items[3].prose` | Show that $\nabla(\mathbf w^T\boldsymbol\Sigma\mathbf w) = 2\boldsymbol\Sigma\mathbf w$ for two assets, where $\boldsymbol\Sigma = \begin{pmatrix} ... | correct | B30 |
| `items[3].question` | Put the lines in order. | correct | B30 |
| `items[3].widget.lines[0]` | line expand: $V = \sigma_{11}w_1^2 + 2\sigma_{12}w_1w_2 + \sigma_{22}w_2^2$: multiply out, using $\boldsymbol\Sigma$ symmetric | correct | B30 |
| `items[3].widget.lines[1]` | line d1: $\dfrac{\partial V}{\partial w_1} = 2\sigma_{11}w_1 + 2\sigma_{12}w_2$: hold $w_2$ fixed | correct | B30 |
| `items[3].widget.lines[2]` | line d2: $\dfrac{\partial V}{\partial w_2} = 2\sigma_{12}w_1 + 2\sigma_{22}w_2$: the same steps with the roles swapped | correct | B30 |
| `items[3].widget.lines[3]` | line collect: $\nabla V = 2(\sigma_{11}w_1 + \sigma_{12}w_2,\ \sigma_{12}w_1 + \sigma_{22}w_2) = 2\boldsymbol\Sigma\mathbf w$: the bracket is $\bol... | correct | B30 |
| `items[3].widget.answer` | expand, d1, d2, collect | correct | B30 |
| `items[3].feedback.correct` | Expand, differentiate each weight, recognise $\boldsymbol\Sigma\mathbf w$. | correct | B30 |
| `items[3].feedback.generic` | Not quite right. Start by multiplying out $V$; the matrix form comes last. | correct | B30 |
| `items[3].feedback.byKey.d2` | The roles can only be swapped after the first partial is done. | correct | B30 |
| `items[3].feedback.byKey.collect` | The gradient needs both partials first. | correct | B30 |
| `items[3].explain.text` | Multiplying out gives a quadratic in $w_1, w_2$ with the cross term twice. Each partial brings down a 2. The two partials are exactly twice the row... | correct | B30 |
| `items[4].prose` | How long does descent take? Write `steps_needed(grad, x0, y0, step, tol, max_steps)`. It runs gradient descent from `(x0, y0)`. It returns the firs... | correct | B30 |
| `items[4].question` | Write `steps_needed`. | correct | B30 |
| `items[4].widget.solution` | import math def steps_needed(grad, x0, y0, step, tol, max_steps): x, y = x0, y0 for k in range(max_steps): gx, gy = grad(x, y) if math.hypot(gx, gy... | correct | B30 |
| `items[4].widget.examples[0]` | steps_needed(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 1e-3, 1000) -> 41 | correct | B26 |
| `items[4].widget.tests[0]` | steps_needed(lambda x, y: (2 * x, 4 * y), 4, 3, 0.1, 1e-3, 1000) -> 41 | correct | B26 |
| `items[4].widget.tests[1]` | steps_needed(lambda x, y: (2 * x, 4 * y), 4, 3, 0.3, 1e-3, 1000) -> 10 | correct | B26 |
| `items[4].widget.tests[2]` | steps_needed(lambda x, y: (2 * x, 4 * y), 4, 3, 0.01, 1e-3, 10000) -> 445 | correct | B26 |
| `items[4].widget.tests[3]` | steps_needed(lambda x, y: (2 * x, 4 * y), 0, 0, 0.1, 1e-3, 100) -> 0 | correct | B26 |
| `items[4].widget.tests[4]` | steps_needed(lambda x, y: (2 * x, 4 * y), 4, 3, 0.6, 1e-3, 50) -> 50 | correct | B26 |
| `items[4].widget.tests[5]` | steps_needed(lambda x, y: (2 * x, 4 * y), 4, 3, 0.5, 1e-3, 200) -> 200 | correct | B26 |
| `items[4].widget.tests[6]` | steps_needed(lambda x, y: (2 * x, 18 * y), 9, 1, 0.1, 1e-6, 1000) -> 77 | correct | B26 |
| `items[4].widget.how` | Check runs 7 hidden tests on $x^2 + 2y^2$ and $x^2 + 9y^2$. They cover good steps, a tiny step, a start at the minimum, and steps that never settle... | correct | B30 |
| `items[4].widget.mutants[0]` | mutant first fails test 1: `math.hypot(g)` on the pair raises a TypeError in test 1 | correct | B26 |
| `items[4].widget.mutants[1]` | mutant first fails test 1: `abs(g)` on the pair raises a TypeError in test 1 | correct | B26 |
| `items[4].widget.mutants[2]` | mutant first fails test 1: `step * g` on the pair raises a TypeError in test 1 | correct | B26 |
| `items[4].widget.mutants[3]` | mutant first fails test 1: returns $k + 1$: counts from 1 | correct | B26 |
| `items[4].feedback.correct` | Step 0.3 needs 10 steps where 0.1 needs 41 and 0.01 needs 445. | correct | B30 |
| `items[4].feedback.generic` | Not quite right. Read the first failing test. | correct | B30 |
| `items[4].feedback.byKey.test-1` | Test 1 expects 41. Unpack with `gx, gy = grad(x, y)`, check `math.hypot(gx, gy)` before each step, and count from 0. | correct | B27 |
| `items[4].feedback.byKey.test-4` | Test 4 starts at the minimum, where the gradient is already 0: return 0. | correct | B27 |
| `items[4].feedback.byKey.test-5` | Test 5 never settles. Stop after `max_steps` steps and return `max_steps`. | correct | B27 |
| `items[4].feedback.byKey.error` | Your code did not run. Check the colons and the indentation, and give the function a body in place of `pass`. | correct | B27 |
| `items[4].explain.text` | Test before stepping, so a start at the minimum returns 0. Step 0.3 is close to the best step $\tfrac13$, so it needs only 10 steps; 0.01 crawls th... | correct | B30 |
| `items[5].prose` | On $f = x^2 + 2y^2$, a step $s$ multiplies $x$ by $1 - 2s$ and $y$ by $1 - 4s$. The slower coordinate shrinks by $\max(\|1 - 2s\|, \|1 - 4s\|)$ per... | correct | B30 |
| `items[5].question` | Which step size makes that slower factor as small as possible? | correct | B30 |
| `items[5].widget.answer` | 0.3333 | correct | B30 |
| `items[5].widget.accept` | $1 - 2s = 4s - 1$ gives $s = \tfrac13$, factor $\tfrac13$ | correct | B30 |
| `items[5].widget.wrong[0]` | slip y = 0.25 | correct | B30 |
| `items[5].widget.wrong[1]` | slip x = 0.5 | correct | B30 |
| `items[5].feedback.correct` | $s = \tfrac13$: both factors have size $\tfrac13$. | correct | B30 |
| `items[5].feedback.generic` | Not quite right. The best step balances the two sizes: $\|1 - 2s\| = \|1 - 4s\|$. | correct | B30 |
| `items[5].feedback.byKey.y` | At 0.25 the $y$ factor is 0, but $x$ still shrinks only by 0.5 per step. | correct | B30 |
| `items[5].feedback.byKey.x` | At 0.5 the $y$ factor is $-1$: $y$ never settles. | correct | B30 |
| `items[5].explain.text` | For small $s$ the $x$ factor $1 - 2s$ is the larger. Past $\tfrac14$ the $y$ factor $4s - 1$ grows. They meet where $1 - 2s = 4s - 1$, at $s = \tfr... | correct | B30 |
| `items[6].prose` | A book's value changes by £800, −£300 and £150 per £1 rise in stocks A, B and C. Today A rises £1.20, B falls £0.50 and C rises £2.00. | correct | B30 |
| `items[6].question` | Estimate the book's P&L. | correct | B30 |
| `items[6].widget.answer` | 1410 | correct | B30 |
| `items[6].widget.accept` | $800(1.2) + (-300)(-0.5) + 150(2) = 960 + 150 + 300 = 1410$ | correct | B30 |
| `items[6].widget.wrong[0]` | slip signs = 810 | wrong | finding 2: the named mistake (B term taken as -150) gives 960 - 150 + 300 = 1110, not 810; failing check in concepts-r2 script |
| `items[6].widget.wrong[1]` | slip noB = 1260 | correct | B30 |
| `items[6].feedback.correct` | £1,410: every position gained, the short B included. | correct | B30 |
| `items[6].feedback.generic` | Not quite right. Take the dot product of sensitivities with moves, signs included. | correct | B30 |
| `items[6].feedback.byKey.signs` | A short position gains when its price falls: $(-300)(-0.5) = +150$. | wrong | finding 2: this line fires on 810, which the mistake it names does not produce (it produces 1110) |
| `items[6].feedback.byKey.noB` | You left out B. Its term is $(-300)(-0.5) = +150$. | correct | B30 |
| `items[6].explain.text` | The P&L is the dot product $800(1.2) + (-300)(-0.5) + 150(2) = 1410$. The short in B gains when B falls. | correct | B30 |
| `items[7].prompt` | We minimise $f(x, y) = x^2 + 9y^2$ by gradient descent with a fixed step $s$, starting at (9, 1). (a) Show that each step multiplies $x$ by $1 - 2s... | correct | B30 |
| `items[7].model#1` | **(a)** $\nabla f = (2x, 18y)$. One step gives $x_{\text{new}} = x - s(2x) = (1 - 2s)x$ and $y_{\text{new}} = y - s(18y) = (1 - 18s)y$. | correct | B30 |
| `items[7].model#2` | **(b)** $x_k = 9(1 - 2s)^k$ and $y_k = (1 - 18s)^k$ tend to 0 exactly when both factors have size below 1. $\|1 - 2s\| < 1$ needs $0 < s < 1$, and ... | correct | B30 |
| `items[7].model#3` | **(c)** The slower factor is $\max(\|1 - 2s\|, \|1 - 18s\|)$. The first falls as $s$ grows, and the second rises once $s > \tfrac1{18}$. They balan... | correct | B30 |
| `items[7].model#4` | **(d)** $\|x_k\| = 9(0.8)^k < 10^{-3}$ means $k > \dfrac{\ln 9000}{\ln 1.25} \approx 40.8$, so 41 steps. Check: $9(0.8)^{40} \approx 0.0012$ and $9... | correct | B30 |
| `items[7].model#5` | **(e)** The contours are ellipses three times wider in $x$ than in $y$. The gradient crosses each contour at right angles, so away from the axes it... | correct | B30 |
| `items[7].rubric[0]` | (2) Computes $\nabla f = (2x, 18y)$ and derives both factors $1 - 2s$ and $1 - 18s$. | correct | B30 |
| `items[7].rubric[1]` | (2) States convergence needs both factors of size below 1 and concludes $0 < s < \tfrac19$. | correct | B30 |
| `items[7].rubric[2]` | (2) Balances $1 - 2s = 18s - 1$ to get $s = 0.1$ with factor 0.8. | correct | B30 |
| `items[7].rubric[3]` | (2) Solves $9(0.8)^k < 10^{-3}$ with logarithms and gets 41 steps. | correct | B30 |
| `items[7].rubric[4]` | (2) Explains the zigzag with the gradient perpendicular to elongated contours, contrasts circles, and links it to rescaling parameters. | correct | B30 |

## problems-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Take $f(x, y) = x^2 y$ and stand at P $= (3, 2)$, where $f = 18$. We find the slope of $f$ in several directions from P. | correct | B31 |
| `items[0].parts[0].question` | What is $\nabla f$ at P? Give it as a pair. | correct | B31 |
| `items[0].parts[0].widget.answer` | (12, 9) | correct | B31 |
| `items[0].parts[0].widget.accept` | (12,9) | correct | B31 |
| `items[0].parts[0].widget.wrong[0]` | slip swapped = (9, 12) | correct | B31 |
| `items[0].parts[0].widget.wrong[1]` | slip no-two = (6, 9) | correct | B31 |
| `items[0].parts[0].feedback.correct` | $f_x = 2xy = 12$ and $f_y = x^2 = 9$ at $(3, 2)$, so $\nabla f = (12, 9)$. | correct | B31 |
| `items[0].parts[0].feedback.generic` | Not quite. The gradient is $(f_x, f_y)$: find each partial, then put in $x = 3$ and $y = 2$. | correct | B31 |
| `items[0].parts[0].feedback.byKey.swapped` | You put $f_y$ first. The gradient is $(f_x, f_y) = (12, 9)$. | correct | B31 |
| `items[0].parts[0].feedback.byKey.no-two` | You dropped the 2 from $x^2$. $f_x = 2xy$, which is 12 at P. | correct | B31 |
| `items[0].parts[0].feedback.byKey.length` | Give two numbers in brackets: $f_x$ first, then $f_y$. | correct | B31 |
| `items[0].parts[0].explain.text` | $\nabla f = (2xy, x^2)$. At $(3, 2)$ that is $(12, 9)$. | correct | B31 |
| `items[0].parts[1].question` | Using $\nabla f = (12, 9)$, how steep is the steepest climb from P? | correct | B31 |
| `items[0].parts[1].widget.answer` | 15 | correct | B31 |
| `items[0].parts[1].widget.wrong[0]` | slip added = 21 | correct | B31 |
| `items[0].parts[1].widget.wrong[1]` | slip no-root = 225 | correct | B31 |
| `items[0].parts[1].feedback.correct` | $\|\nabla f\| = \sqrt{12^2 + 9^2} = \sqrt{225} = 15$. | correct | B31 |
| `items[0].parts[1].feedback.generic` | Not quite. The steepest slope is the length of the gradient. | correct | B31 |
| `items[0].parts[1].feedback.byKey.added` | You added the components. The length is $\sqrt{12^2 + 9^2}$, not $12 + 9$. | correct | B31 |
| `items[0].parts[1].feedback.byKey.no-root` | That is $\|\nabla f\|^2$. Take the square root: 15. | correct | B31 |
| `items[0].parts[1].explain.text` | The steepest climb runs along $\nabla f$, with slope $\|\nabla f\| = \sqrt{144 + 81} = 15$. | correct | B31 |
| `items[0].parts[2].question` | A friend walks from P straight towards $(-1, 5)$. Using $\nabla f = (12, 9)$, what is the slope of $f$ in that direction? Give the exact decimal. | correct | B31 |
| `items[0].parts[2].widget.answer` | -4.2 | correct | B31 |
| `items[0].parts[2].widget.wrong[0]` | slip not-unit = -21 | correct | B31 |
| `items[0].parts[2].widget.wrong[1]` | slip reversed = 4.2 | correct | B31 |
| `items[0].parts[2].feedback.correct` | The arrow is $(-4, 3)$, of length 5, so $\mathbf u = (-0.8, 0.6)$. Then $D_{\mathbf u} f = -9.6 + 5.4 = -4.2$. | correct | B31 |
| `items[0].parts[2].feedback.generic` | Not quite. Make the arrow from P to $(-1, 5)$ a unit arrow first, then take its dot product with $\nabla f$. | correct | B31 |
| `items[0].parts[2].feedback.byKey.not-unit` | You used the arrow $(-4, 3)$ without making it unit length. Divide by its length 5 first. | correct | B31 |
| `items[0].parts[2].feedback.byKey.reversed` | You used the arrow from $(-1, 5)$ back to P. Towards $(-1, 5)$ the arrow is $(-4, 3)$, so the slope is negative. | correct | B31 |
| `items[0].parts[2].explain.text` | $\mathbf u = \tfrac{1}{5}(-4, 3) = (-0.8, 0.6)$, and $D_{\mathbf u} f = \nabla f \cdot \mathbf u = -4.2$. The friend heads slightly downhill. | correct | B31 |
| `items[0].parts[3].question` | Using $\nabla f = (12, 9)$, which unit arrow points along the contour through P? Give the one with a positive first component. | correct | B31 |
| `items[0].parts[3].widget.answer` | (0.6, -0.8) | correct | B31 |
| `items[0].parts[3].widget.accept` | (\frac{3}{5}, -\frac{4}{5}) | correct | B31 |
| `items[0].parts[3].widget.wrong[0]` | slip gradient-dir = (0.8, 0.6) | correct | B31 |
| `items[0].parts[3].widget.wrong[1]` | slip other-way = (-0.6, 0.8) | correct | B31 |
| `items[0].parts[3].widget.wrong[2]` | slip not-unit = (9, -12) | correct | B31 |
| `items[0].parts[3].feedback.correct` | A contour arrow has $D_{\mathbf u} f = 0$: $7.2 - 7.2 = 0$, and $0.6^2 + 0.8^2 = 1$. | correct | B31 |
| `items[0].parts[3].feedback.generic` | Not quite. Look for a unit arrow whose dot product with $(12, 9)$ is zero. | correct | B31 |
| `items[0].parts[3].feedback.byKey.gradient-dir` | That arrow points along $\nabla f$, the steepest climb. The contour crosses it at right angles. | correct | B31 |
| `items[0].parts[3].feedback.byKey.other-way` | That arrow is along the contour too, but its first component is negative. Reverse it. | correct | B31 |
| `items[0].parts[3].feedback.byKey.not-unit` | That arrow is along the contour, but its length is 15. Divide by 15. | correct | B31 |
| `items[0].parts[3].feedback.byKey.length` | Give two numbers in brackets, the arrow's two components. | correct | B31 |
| `items[0].parts[3].explain.text` | The contour crosses $\nabla f$ at right angles, so swap the components and change one sign: $(9, -12)$. Dividing by its length 15 gives $(0.6, -0.8)$. | correct | B31 |
| `items[0].parts[4].question` | Using $\|\nabla f\| = 15$ from part 2, at what angle to $\nabla f$ must a unit arrow point for the slope to be 7.5? Give the angle in degrees, betw... | correct | B31 |
| `items[0].parts[4].widget.answer` | 60 | correct | B31 |
| `items[0].parts[4].widget.wrong[0]` | slip sine = 30 | correct | B31 |
| `items[0].parts[4].widget.wrong[1]` | slip obtuse = 120 | correct | B31 |
| `items[0].parts[4].feedback.correct` | $D_{\mathbf u} f = \|\nabla f\|\cos\theta$, so $15\cos\theta = 7.5$ and $\cos\theta = 0.5$. That gives $\theta = 60^\circ$. | correct | B31 |
| `items[0].parts[4].feedback.generic` | Not quite. The slope along $\mathbf u$ is $\|\nabla f\|$ times the cosine of the angle to $\nabla f$. | correct | B31 |
| `items[0].parts[4].feedback.byKey.sine` | You solved $\sin\theta = 0.5$. The slope uses the cosine: $15\cos\theta = 7.5$. | correct | B31 |
| `items[0].parts[4].feedback.byKey.obtuse` | At $120^\circ$ the cosine is $-0.5$, a slope of $-7.5$. A slope of $+7.5$ needs $60^\circ$. | correct | B31 |
| `items[0].parts[4].explain.text` | Writing $D_{\mathbf u} f = \|\nabla f\|\cos\theta$, we need $\cos\theta = \tfrac{7.5}{15} = 0.5$, so $\theta = 60^\circ$. Half the steepest slope l... | correct | B31 |
| `items[1].prose` | A desk runs two uncorrelated books with daily risk $x$ and $y$, in £k. The desk's daily risk is $\sigma(x, y) = \sqrt{x^2 + y^2}$, which is £5k tod... | correct | B31 |
| `items[1].parts[0].question` | What is $\nabla\sigma$ at $(3, 4)$? Give it as a pair of exact decimals. | correct | B31 |
| `items[1].parts[0].widget.answer` | (0.6, 0.8) | correct | B31 |
| `items[1].parts[0].widget.accept` | (\frac{3}{5}, \frac{4}{5}) | correct | B31 |
| `items[1].parts[0].widget.wrong[0]` | slip no-root = (6, 8) | correct | B31 |
| `items[1].parts[0].widget.wrong[1]` | slip half = (0.3, 0.4) | correct | B31 |
| `items[1].parts[0].feedback.correct` | $\sigma_x = \frac{x}{\sqrt{x^2 + y^2}} = \tfrac{3}{5}$ and $\sigma_y = \tfrac{4}{5}$, so $\nabla\sigma = (0.6, 0.8)$. | correct | B31 |
| `items[1].parts[0].feedback.generic` | Not quite. Use the chain rule on the square root: $\sigma_x = \frac{2x}{2\sqrt{x^2 + y^2}}$. | correct | B31 |
| `items[1].parts[0].feedback.byKey.no-root` | That is the gradient of $x^2 + y^2$. Divide by $2\sigma = 10$ for the square root. | correct | B31 |
| `items[1].parts[0].feedback.byKey.half` | You halved once too often. The 2 from $x^2$ cancels the $\tfrac12$ from the root, so $\sigma_x = \tfrac{x}{\sigma}$. | correct | B31 |
| `items[1].parts[0].feedback.byKey.length` | Give two numbers in brackets: $\sigma_x$ first, then $\sigma_y$. | correct | B31 |
| `items[1].parts[0].explain.text` | The chain rule gives $\sigma_x = \tfrac{x}{\sigma}$ and $\sigma_y = \tfrac{y}{\sigma}$. With $\sigma = 5$ that is $(0.6, 0.8)$. | correct | B31 |
| `items[1].parts[1].question` | Using $\nabla\sigma = (0.6, 0.8)$ and $\sigma = 5$ at $(3, 4)$, write the tangent plane $z$ in terms of $x$ and $y$. | correct | B31 |
| `items[1].parts[1].widget.answer` | 0.6x+0.8y | correct | B31 |
| `items[1].parts[1].widget.accept` | 5+0.6(x-3)+0.8(y-4), \frac{3x+4y}{5} | correct | B31 |
| `items[1].parts[1].widget.wrong[0]` | slip no-shift = 5+0.6x+0.8y | correct | B31 |
| `items[1].parts[1].widget.wrong[1]` | slip carried = 6x+8y-45 | correct | B31 |
| `items[1].parts[1].feedback.correct` | $z = 5 + 0.6(x - 3) + 0.8(y - 4) = 0.6x + 0.8y$. The constants cancel: $5 - 1.8 - 3.2 = 0$. | correct | B31 |
| `items[1].parts[1].feedback.generic` | Not quite. Start from $\sigma(3, 4) = 5$ and add one straight-line change per direction, measured from $(3, 4)$. | correct | B31 |
| `items[1].parts[1].feedback.byKey.no-shift` | You used $x$ and $y$ in place of $x - 3$ and $y - 4$. The changes are measured from the point $(3, 4)$. | correct | B31 |
| `items[1].parts[1].feedback.byKey.carried` | You used slopes 6 and 8, the gradient of $x^2 + y^2$. The slopes of $\sigma$ are 0.6 and 0.8. | correct | B31 |
| `items[1].parts[1].explain.text` | $z = \sigma(3, 4) + \sigma_x(x - 3) + \sigma_y(y - 4) = 5 + 0.6(x - 3) + 0.8(y - 4)$. Multiplied out, $z = 0.6x + 0.8y$. | correct | B31 |
| `items[1].parts[2].question` | Tomorrow the books' risks move to $x = 3.2$ and $y = 3.7$. Using the plane $z = 0.6x + 0.8y$, estimate the desk's risk in £k. Give 2 decimal places. | correct | B31 |
| `items[1].parts[2].widget.answer` | 4.88 | correct | B31 |
| `items[1].parts[2].widget.wrong[0]` | slip exact = 4.89 | correct | B31 |
| `items[1].parts[2].widget.wrong[1]` | slip no-shift = 9.88 | correct | B31 |
| `items[1].parts[2].widget.wrong[2]` | slip unit-slopes = 4.9 | correct | B31 |
| `items[1].parts[2].widget.wrong[3]` | slip carried = 3.8 | correct | B31 |
| `items[1].parts[2].feedback.correct` | $z = 0.6 \times 3.2 + 0.8 \times 3.7 = 1.92 + 2.96 = 4.88$, so about £4.88k. | correct | B31 |
| `items[1].parts[2].feedback.generic` | Not quite. Put $x = 3.2$ and $y = 3.7$ into $0.6x + 0.8y$. | correct | B31 |
| `items[1].parts[2].feedback.byKey.exact` | That is the true risk, $\sqrt{3.2^2 + 3.7^2}$. The question asks for the plane's estimate. | correct | B31 |
| `items[1].parts[2].feedback.byKey.no-shift` | You kept part 2's extra 5. The plane $0.6x + 0.8y$ already holds the height at $(3, 4)$. | correct | B31 |
| `items[1].parts[2].feedback.byKey.unit-slopes` | You added the two moves, $+0.2$ and $-0.3$, to 5 without their slopes. Weight them by 0.6 and 0.8. | correct | B31 |
| `items[1].parts[2].feedback.byKey.carried` | That comes from the plane $6x + 8y - 45$, built with the slopes of $x^2 + y^2$. | correct | B31 |
| `items[1].parts[2].explain.text` | The plane gives $1.92 + 2.96 = 4.88$. The fall in $y$ counts for more, because its slope is 0.8. | correct | B31 |
| `items[1].parts[3].question` | The true risk is $\sqrt{3.2^2 + 3.7^2}$. Using the plane's estimate 4.88, what is the error, the true value minus the estimate? Give 4 decimal places. | correct | B31 |
| `items[1].parts[3].widget.answer` | 0.0118 | correct | B31 |
| `items[1].parts[3].widget.wrong[0]` | slip sign = -0.0118 | correct | B31 |
| `items[1].parts[3].widget.wrong[1]` | slip squares = 0.1156 | correct | B31 |
| `items[1].parts[3].feedback.correct` | $\sqrt{3.2^2 + 3.7^2} = \sqrt{23.93} \approx 4.8918$, so the error is $4.8918 - 4.88 = 0.0118$. | correct | B31 |
| `items[1].parts[3].feedback.generic` | Not quite. Work out $\sqrt{3.2^2 + 3.7^2}$, then subtract 4.88. | correct | B31 |
| `items[1].parts[3].feedback.byKey.sign` | You took the estimate minus the true value. The plane lies below this surface, so true minus estimate is positive. | correct | B31 |
| `items[1].parts[3].feedback.byKey.squares` | You compared the squares, $23.93 - 4.88^2$. Take the square root first, then subtract. | correct | B31 |
| `items[1].parts[3].explain.text` | The true risk is $\sqrt{23.93} \approx 4.8918$, so the error is 0.0118. It is positive: the surface $\sigma$ curves up away from its tangent plane. | correct | B31 |
| `items[1].parts[4].question` | Halve the move: $x = 3.1$ and $y = 3.85$. The error 0.0118 from part 4 shrinks with the square of the step. Predict the new error. Give 4 decimal p... | correct | B31 |
| `items[1].parts[4].widget.answer` | 0.003 | correct | B31 |
| `items[1].parts[4].widget.accept` | 0.0030 (the true error, 0.0029, is accepted too) | correct | B31 |
| `items[1].parts[4].widget.wrong[0]` | slip halved = 0.0059 | correct | B31 |
| `items[1].parts[4].widget.wrong[1]` | slip same = 0.0118 | correct | B31 |
| `items[1].parts[4].widget.wrong[2]` | slip cube = 0.0015 | correct | B31 |
| `items[1].parts[4].feedback.correct` | Half the step gives a quarter of the error: $0.0118 / 4 \approx 0.0030$. The true error is $4.9429 - 4.94 = 0.0029$. | correct | B31 |
| `items[1].parts[4].feedback.generic` | Not quite. The error shrinks with the square of the step. | correct | B31 |
| `items[1].parts[4].feedback.byKey.halved` | You halved the error. It shrinks with the square of the step, so halving the step divides it by 4. | correct | B31 |
| `items[1].parts[4].feedback.byKey.same` | The error does shrink. Halving the step divides it by about $2^2 = 4$. | correct | B31 |
| `items[1].parts[4].feedback.byKey.cube` | You divided by 8. The tangent plane's error goes with the square of the step, so divide by 4. | correct | B31 |
| `items[1].parts[4].explain.text` | The plane's error shrinks with the square of the step. Halving the move divides 0.0118 by 4, about 0.0030, and the true error is 0.0029. | correct | B31 |
| `items[2].prose` | A model fits two parameters by gradient descent on the loss $L(a, b) = 4(a - 1)^2 + (b + 2)^2$, which is lowest at $(1, -2)$. Descent starts at $(0... | correct | B31 |
| `items[2].parts[0].question` | What is $\nabla L$ at $(0, 0)$? Give it as a pair. | correct | B31 |
| `items[2].parts[0].widget.answer` | (-8, 4) | correct | B31 |
| `items[2].parts[0].widget.accept` | (-8,4) | correct | B31 |
| `items[2].parts[0].widget.wrong[0]` | slip sign = (8, -4) | correct | B31 |
| `items[2].parts[0].widget.wrong[1]` | slip no-two = (-4, 2) | correct | B31 |
| `items[2].parts[0].feedback.correct` | $L_a = 8(a - 1)$ and $L_b = 2(b + 2)$. At $(0, 0)$, $\nabla L = (-8, 4)$. | correct | B31 |
| `items[2].parts[0].feedback.generic` | Not quite. Differentiate each bracket with the chain rule, then put in $a = 0$ and $b = 0$. | correct | B31 |
| `items[2].parts[0].feedback.byKey.sign` | The signs are flipped. At $a = 0$, $8(a - 1) = -8$, and at $b = 0$, $2(b + 2) = 4$. | correct | B31 |
| `items[2].parts[0].feedback.byKey.no-two` | You dropped the 2 from each square. $\frac{\partial}{\partial a} 4(a - 1)^2 = 8(a - 1)$. | correct | B31 |
| `items[2].parts[0].feedback.byKey.length` | Give two numbers in brackets: $L_a$ first, then $L_b$. | correct | B31 |
| `items[2].parts[0].explain.text` | $\nabla L = (8(a - 1), 2(b + 2))$, which is $(-8, 4)$ at the start. It points uphill, away from $(1, -2)$. | correct | B31 |
| `items[2].parts[1].question` | Using $\nabla L = (-8, 4)$, where does one step with $s = 0.1$ land? Give the point as a pair. | correct | B31 |
| `items[2].parts[1].widget.answer` | (0.8, -0.4) | correct | B31 |
| `items[2].parts[1].widget.accept` | (0.8,-0.4), (\frac{4}{5}, -\frac{2}{5}) | correct | B31 |
| `items[2].parts[1].widget.wrong[0]` | slip uphill = (-0.8, 0.4) | correct | B31 |
| `items[2].parts[1].widget.wrong[1]` | slip carried = (0.4, -0.2) | correct | B31 |
| `items[2].parts[1].widget.wrong[2]` | slip no-scale = (8, -4) | correct | B31 |
| `items[2].parts[1].feedback.correct` | $(0, 0) - 0.1(-8, 4) = (0.8, -0.4)$, closer to $(1, -2)$ in both coordinates. | correct | B31 |
| `items[2].parts[1].feedback.generic` | Not quite. Step against the gradient: subtract $0.1\,\nabla L$. | correct | B31 |
| `items[2].parts[1].feedback.byKey.uphill` | You stepped along the gradient, uphill. Descent subtracts $s\,\nabla L$. | correct | B31 |
| `items[2].parts[1].feedback.byKey.carried` | That uses the gradient $(-4, 2)$ from dropping the 2. With $(-8, 4)$ the step lands at $(0.8, -0.4)$. | correct | B31 |
| `items[2].parts[1].feedback.byKey.no-scale` | You left out the step size. The move is $-0.1\,\nabla L$, not $-\nabla L$. | correct | B31 |
| `items[2].parts[1].feedback.byKey.length` | Give the point as two numbers in brackets, $a$ first. | correct | B31 |
| `items[2].parts[1].explain.text` | $\mathbf x_1 = \mathbf x_0 - s\,\nabla L(\mathbf x_0) = (0, 0) - 0.1(-8, 4) = (0.8, -0.4)$. | correct | B31 |
| `items[2].parts[2].question` | Each step multiplies $b + 2$ by $1 - 2s$. Using $b = -0.4$ after step 1, where is $b$ after step 2? Give the exact decimal. | correct | B31 |
| `items[2].parts[2].widget.answer` | -0.72 | correct | B31 |
| `items[2].parts[2].widget.wrong[0]` | slip linear = -0.8 | correct | B31 |
| `items[2].parts[2].widget.wrong[1]` | slip plus-two = 1.28 | correct | B31 |
| `items[2].parts[2].widget.wrong[2]` | slip sign = 0.72 | correct | B31 |
| `items[2].parts[2].feedback.correct` | $b + 2 = 1.6$ becomes $0.8 \times 1.6 = 1.28$, so $b = -0.72$. The gradient is recomputed: $L_b = 3.2$ now, not 4. | correct | B31 |
| `items[2].parts[2].feedback.generic` | Not quite. Multiply $b + 2 = 1.6$ by $1 - 2(0.1) = 0.8$, then subtract 2. | correct | B31 |
| `items[2].parts[2].feedback.byKey.linear` | You reused the first gradient, 4. At $b = -0.4$ it is $2(1.6) = 3.2$, so the step is shorter. | correct | B31 |
| `items[2].parts[2].feedback.byKey.plus-two` | That is $b + 2$ after step 2. Subtract 2 to get $b$. | correct | B31 |
| `items[2].parts[2].feedback.byKey.sign` | b₂ + 2 = 1.28, so b₂ = 1.28 − 2, which is below zero. A positive 0.72 takes 2 − 1.28, the wrong way round. | correct | B31 |
| `items[2].parts[2].explain.text` | $b_2 + 2 = 0.8 \times 1.6 = 1.28$, so $b_2 = -0.72$. Each step closes a fifth of the gap to $-2$. | correct | B31 |
| `items[2].parts[3].question` | Each step also multiplies $a - 1$ by $1 - 8s$. Descent settles only when both factors lie strictly between $-1$ and 1. It settles for every $s$ fro... | correct | B31 |
| `items[2].parts[3].widget.answer` | 0.25 | correct | B31 |
| `items[2].parts[3].widget.wrong[0]` | slip b-only = 1 | correct | B31 |
| `items[2].parts[3].widget.wrong[1]` | slip no-zigzag = 0.125 | correct | B31 |
| `items[2].parts[3].feedback.correct` | $\|1 - 8s\| < 1$ needs $0 < s < 0.25$, and $\|1 - 2s\| < 1$ needs $0 < s < 1$. The stricter limit is 0.25. | correct | B31 |
| `items[2].parts[3].feedback.generic` | Not quite. Solve $-1 < 1 - 8s < 1$ and $-1 < 1 - 2s < 1$, then take the stricter. | correct | B31 |
| `items[2].parts[3].feedback.byKey.b-only` | That is the limit for $b$ alone. The steeper $a$ direction caps the step at 0.25. | correct | B31 |
| `items[2].parts[3].feedback.byKey.no-zigzag` | Below 0.125 the $a$ factor stays positive, so there is no zigzag. Between 0.125 and 0.25 it zigzags but still shrinks. | correct | B31 |
| `items[2].parts[3].explain.text` | The steepest direction caps the step: $\|1 - 8s\| < 1$ gives $s < 0.25$. The $b$ factor alone would allow steps up to 1. | correct | B31 |
| `items[2].parts[4].question` | Back to $s = 0.1$. Then $a - 1$ starts at $-1$ and is multiplied by 0.2 each step, and $b + 2$ starts at 2 and is multiplied by 0.8. After how many... | correct | B31 |
| `items[2].parts[4].widget.answer` | 24 | correct | B31 |
| `items[2].parts[4].widget.wrong[0]` | slip used-a = 3 | correct | B31 |
| `items[2].parts[4].widget.wrong[1]` | slip one-short = 23 | correct | B31 |
| `items[2].parts[4].widget.wrong[2]` | slip start-one = 21 | correct | B31 |
| `items[2].parts[4].feedback.correct` | $2 \times 0.8^{k} < 0.01$ needs $0.8^{k} < 0.005$. Since $0.8^{23} \approx 0.0059$ and $0.8^{24} \approx 0.0047$, it takes 24 steps; $a$ was close ... | correct | B31 |
| `items[2].parts[4].feedback.generic` | Not quite. The slow coordinate decides. Find the first $k$ with $2 \times 0.8^{k} < 0.01$. | correct | B31 |
| `items[2].parts[4].feedback.byKey.used-a` | That is when $a$ arrives. The slow coordinate is $b$, which shrinks by only 0.8 a step. | correct | B31 |
| `items[2].parts[4].feedback.byKey.one-short` | After 23 steps $b + 2 \approx 0.0118$, still above 0.01. It takes one more. | correct | B31 |
| `items[2].parts[4].feedback.byKey.start-one` | You started $b + 2$ at 1. It starts at 2, so solve $2 \times 0.8^{k} < 0.01$. | correct | B31 |
| `items[2].parts[4].explain.text` | The slow factor 0.8 sets the pace: $2 \times 0.8^{24} \approx 0.0094$, below 0.01, but $2 \times 0.8^{23} \approx 0.0118$. So it takes 24 steps, wh... | correct | B31 |

## l9-peaks-pits-saddles

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Find the stationary points of a function of two variables. | correct | B32 |
| `objectives[1]` | Recognise a peak, a pit and a saddle on a contour map. | correct | B32 |
| `screens[0].prose` | A contour map of hilly ground. Each curve joins points of equal height. Blue curves are above sea level, amber curves below it, and purple is sea l... | correct | B32 |
| `screens[0].question` | Tap every lettered point where the ground is level in every direction. | correct | B32 |
| `screens[0].widget.answer` | A, C, F, G | correct | B32 |
| `screens[0].hints[0]` | Where could you take a small step any way without climbing or dropping? | correct | B32 |
| `screens[0].hints[1]` | Look where the curves close into small rings, and where two curves cross. | correct | B32 |
| `screens[0].hints[2]` | C and F sit inside closed rings: a summit and a hollow. A and G sit where the sea-level curves cross: two passes. | correct | B32 |
| `screens[0].feedback.correct` | A summit, a hollow and two passes. | correct | B32 |
| `screens[0].feedback.generic` | Not quite right. Level points sit inside the smallest rings or where two curves cross. | correct | B32 |
| `screens[0].feedback.byKey.rings-only` | You found the summit and the hollow. At A and G two curves cross: those are passes, and a pass is level too. | correct | B32 |
| `screens[0].feedback.byKey.A` | You left out A, where two sea-level curves cross. Walking through A, one way climbs and one way falls, but A itself is level. | correct | B32 |
| `screens[0].feedback.byKey.G` | You left out G, where two sea-level curves cross. G is a pass between two hills, and the ground there is level. | correct | B32 |
| `screens[0].feedback.byKey.B` | B sits between rings, on a slope. Walking east from B you climb towards the summit at C. | correct | B32 |
| `screens[0].feedback.byKey.D` | D is on the sea-level curve, but the ground still slopes there. Being on a contour does not make a point level. | correct | B32 |
| `screens[0].feedback.byKey.E` | E is on the side of the hill round C. Walking west from E you climb. | correct | B32 |
| `screens[0].explain.text` | You picked the points with no slope at all. Rings close round the summit C and the hollow F. At the passes A and G two contours cross, so the groun... | correct | B32 |
| `screens[1].prose` | The map is $f(x, y) = \sin x + \sin y$. The arrow at P is the gradient $\nabla f = (\cos x, \cos y)$, drawn at half length. Drag P around. | correct | B32 |
| `screens[1].question` | Drag P onto the summit, the hollow and each pass. What is true of $\nabla f$ at all of them? | correct | B32 |
| `screens[1].widget.options[0]` | option zero (key): Both components are 0, so the arrow vanishes | correct | B32 |
| `screens[1].widget.options[1]` | option one: One component is 0 and the other is not | correct | B32 |
| `screens[1].widget.options[1].why` | That happens along a whole line, such as $x = \tfrac{\pi}{2}$. At the four level points both read 0 together. | correct | B32 |
| `screens[1].widget.options[2]` | option uphill: It points straight up the steepest slope | correct | B32 |
| `screens[1].widget.options[2].why` | That is true on a slope. At the summit there is no uphill direction left, so the arrow has nothing to point at. | correct | B32 |
| `screens[1].widget.options[3]` | option along: It points along the contour | correct | B32 |
| `screens[1].widget.options[3].why` | On a slope the gradient crosses the contours at right angles. At the level points it has shrunk to nothing. | correct | B32 |
| `screens[1].hints[0]` | Drag P onto C and read the caption. | correct | B32 |
| `screens[1].hints[1]` | The summit and the passes all sit at $x = \pm\tfrac{\pi}{2}$, $y = \pm\tfrac{\pi}{2}$, where cosine is 0. | correct | B32 |
| `screens[1].feedback.correct` | At every level point the gradient is the zero vector. | correct | B32 |
| `screens[1].feedback.generic` | Not quite right. Drag P onto the summit and read both numbers in the caption. | correct | B32 |
| `screens[1].explain.text` | You saw the arrow shrink to nothing at the summit, the hollow and both passes. There $\cos x = 0$ and $\cos y = 0$, so $\nabla f = (0, 0)$. Points ... | correct | B32 |
| `screens[2].prose` | A stationary point is where $\nabla f = \mathbf{0}$, so $f_x = 0$ and $f_y = 0$ at once. Take $$f(x, y) = x^2 + y^2 - 2x + 4y.$$ Solve both equatio... | correct | B32 |
| `screens[2].question` | Drag P to the stationary point. | correct | B32 |
| `screens[2].hints[0]` | Differentiate with respect to $x$, holding $y$ fixed. Then the other way round. | correct | B32 |
| `screens[2].hints[1]` | $f_x = 2x - 2$ and $f_y = 2y + 4$. The caption shows both at P. | correct | B32 |
| `screens[2].hints[2]` | $2x - 2 = 0$ gives $x = 1$. $2y + 4 = 0$ gives $y = -2$. Drag P to $(1, -2)$. | correct | B32 |
| `screens[2].feedback.correct` | $(1, -2)$, the centre of the rings. | correct | B32 |
| `screens[2].feedback.generic` | Not quite right. Solve $2x - 2 = 0$ and $2y + 4 = 0$, then place P there. | correct | B32 |
| `screens[2].feedback.byKey.sign-y` | You placed P at $y = 2$. From $2y + 4 = 0$, $y = -2$: the sign flips when the 4 moves across. | correct | B32 |
| `screens[2].feedback.byKey.sign-x` | You placed P at $x = -1$. From $2x - 2 = 0$, $x = +1$. | correct | B32 |
| `screens[2].feedback.byKey.both-signs` | Both signs flipped. $2x - 2 = 0$ gives $x = 1$, and $2y + 4 = 0$ gives $y = -2$. | correct | B32 |
| `screens[2].explain.text` | You solved $2x - 2 = 0$ and $2y + 4 = 0$ together and got $(1, -2)$. Both partials read 0 there, and the rings close round it. Each equation alone ... | correct | B32 |
| `screens[3].prose` | Now take $$f(x, y) = x^3 - 3x + y^2.$$ Find every solution of $f_x = 0$ and $f_y = 0$. The map shows its contours, with the level $f = 2$ in purple. | correct | B32 |
| `screens[3].question` | Select all that apply: tap every stationary point. | correct | B32 |
| `screens[3].widget.answer` | A, B | correct | B32 |
| `screens[3].hints[0]` | Write down $f_x$ and $f_y$ first. | correct | B32 |
| `screens[3].hints[1]` | $f_x = 3x^2 - 3$ and $f_y = 2y$. Points with $y \neq 0$ fail the second equation. | correct | B32 |
| `screens[3].hints[2]` | $2y = 0$ gives $y = 0$. Then $3x^2 = 3$ gives $x = 1$ or $x = -1$. So $(1, 0)$ and $(-1, 0)$. | correct | B32 |
| `screens[3].feedback.correct` | $(1, 0)$ and $(-1, 0)$. | correct | B32 |
| `screens[3].feedback.generic` | Not quite right. Solve $2y = 0$ and $3x^2 - 3 = 0$ together. | correct | B32 |
| `screens[3].feedback.byKey.plus-only` | You took only $x = 1$. The equation $x^2 = 1$ has two roots, so $(-1, 0)$ is stationary too. | correct | B32 |
| `screens[3].feedback.byKey.one-partial` | D and E make $f_x = 0$, but $f_y = 2y$ is not 0 there. Both partials must vanish. | correct | B32 |
| `screens[3].feedback.byKey.D` | At D, $f_x = 0$ but $f_y = 2$. The ground still slopes in the $y$ direction. | correct | B32 |
| `screens[3].feedback.byKey.E` | At E, $f_x = 0$ but $f_y = -2$. The ground still slopes in the $y$ direction. | correct | B32 |
| `screens[3].feedback.byKey.C` | C is where $f = 0$, not where the slope is 0. There $f_x = -3$. | correct | B32 |
| `screens[3].feedback.byKey.F` | F is where $f = 0$ on the $x$-axis. There $f_x = 3(3) - 3 = 6$, so it slopes. | correct | B32 |
| `screens[3].explain.text` | You solved $2y = 0$ first, then $3x^2 = 3$, which has two roots. Rings close round A, so A is a pit. The purple contours cross at B, so B is a saddle. | correct | B32 |
| `screens[4].prose` | Take $f(x, y) = x^2 - y^2$. Here $f_x = 2x$ and $f_y = -2y$, so the only stationary point is $(0, 0)$. Blue contours have $f > 0$, amber $f < 0$, a... | correct | B32 |
| `screens[4].question` | What does the ground do at $(0, 0)$? | correct | B32 |
| `screens[4].widget.options[0]` | option saddle (key): It rises along the $x$-axis and falls along the $y$-axis | correct | B32 |
| `screens[4].widget.options[1]` | option pit: It is a pit, since $f = x^2$ rises either side along the $x$-axis | correct | B32 |
| `screens[4].widget.options[1].why` | You walked along the $x$-axis only. Along the $y$-axis $f = -y^2$, which falls either side. | correct | B32 |
| `screens[4].widget.options[2]` | option peak: It is a peak, since $f = -y^2$ falls either side along the $y$-axis | correct | B32 |
| `screens[4].widget.options[2].why` | You walked along the $y$-axis only. Along the $x$-axis $f = x^2$ rises. | correct | B32 |
| `screens[4].widget.options[3]` | option none: It is not level, because $f$ takes negative values nearby | correct | B32 |
| `screens[4].widget.options[3].why` | Negative heights do not make a slope. $\nabla f = (2x, -2y)$ is $(0, 0)$ at the origin. | correct | B32 |
| `screens[4].hints[0]` | Walk along the $x$-axis through the origin, then along the $y$-axis. | correct | B32 |
| `screens[4].hints[1]` | On the $x$-axis $f = x^2$. On the $y$-axis $f = -y^2$. | correct | B32 |
| `screens[4].hints[2]` | One walk climbs either side, the other falls either side. The contours $f = 0$ cross at the origin. | correct | B32 |
| `screens[4].feedback.correct` | Up one way, down the other: a saddle. | correct | B32 |
| `screens[4].feedback.generic` | Not quite right. Compare the walk along the $x$-axis with the walk along the $y$-axis. | correct | B32 |
| `screens[4].explain.text` | You compared two walks through the origin: one climbs, the other falls. A stationary point like that is a **saddle**, shaped like a horse's saddle ... | correct | B32 |
| `screens[5].prose` | Find the stationary point of $$f(x, y) = x^2 - 2xy + 2y^2 - 2y.$$ Here $f_x = 2x - 2y$ and $f_y = 4y - 2x - 2$. The green line is where $f_x = 0$. | correct | B32 |
| `screens[5].question` | Where is the stationary point? | correct | B32 |
| `screens[5].widget.options[0]` | option right (key): $(1, 1)$ | correct | B32 |
| `screens[5].widget.options[1]` | option origin: $(0, 0)$ | correct | B32 |
| `screens[5].widget.options[1].why` | You solved $f_x = 0$, got $x = y$, and picked $(0, 0)$ on that line. There $f_y = -2$, so the ground still slopes. | correct | B32 |
| `screens[5].widget.options[2]` | option line: Every point on $y = x$ | correct | B32 |
| `screens[5].widget.options[2].why` | You set only $f_x$ to zero, which leaves a whole line. $f_y = 0$ must hold too, and its line cuts $y = x$ once. | correct | B32 |
| `screens[5].widget.options[3]` | option half: $(0, 0.5)$ | correct | B32 |
| `screens[5].widget.options[3].why` | You set $x = 0$ and solved $f_y = 0$ for $y$. But $f_x = -1$ at $(0, 0.5)$. | correct | B32 |
| `screens[5].hints[0]` | The point must lie on the green line and also satisfy $f_y = 0$. | correct | B32 |
| `screens[5].hints[1]` | On the green line $x = y$. Put that into $f_y = 0$. | correct | B32 |
| `screens[5].hints[2]` | $4y - 2y - 2 = 0$ gives $y = 1$, and then $x = 1$. | correct | B32 |
| `screens[5].feedback.correct` | $(1, 1)$, where the two lines cross. | correct | B32 |
| `screens[5].feedback.generic` | Not quite right. Use $x = y$ from $f_x = 0$ inside $f_y = 0$. | correct | B32 |
| `screens[5].feedback.byKey.line` | You stopped after $f_x = 0$. That equation alone gives the whole line $y = x$; the second equation picks one point on it. | correct | B32 |
| `screens[5].feedback.byKey.origin` | $(0, 0)$ satisfies $f_x = 0$ only. A stationary point needs both partials to be zero. | correct | B32 |
| `screens[5].explain.text` | You substituted $x = y$ from the first equation into the second, giving $y = 1$. Each equation alone is a line of points. The stationary point is w... | correct | B32 |
| `screens[6].prose` | Take $f(x, y) = (x - y)^2$. Its contours are straight lines parallel to $y = x$. Work out $f_x$ and $f_y$ with the chain rule. | correct | B32 |
| `screens[6].question` | How many stationary points does $f$ have? | correct | B32 |
| `screens[6].widget.options[0]` | option one: One, at $(0, 0)$ | correct | B32 |
| `screens[6].widget.options[0].why` | You found one solution of $x - y = 0$ and stopped. $(2, 2)$ and $(-1, -1)$ make both partials 0 as well. | correct | B32 |
| `screens[6].widget.options[1]` | option none: None: there is no single lowest point | correct | B32 |
| `screens[6].widget.options[1].why` | You looked for one isolated point. The lowest value, 0, is reached all along $y = x$, and the ground is level there. | correct | B32 |
| `screens[6].widget.options[2]` | option inf (key): Infinitely many: every point on $y = x$ | correct | B32 |
| `screens[6].widget.options[3]` | option two: Two, one from each partial | correct | B32 |
| `screens[6].widget.options[3].why` | Each partial gives an equation, not a point. Here both equations say the same thing: $x = y$. | correct | B32 |
| `screens[6].hints[0]` | Differentiate $(x - y)^2$ with respect to $x$, then with respect to $y$. | correct | B32 |
| `screens[6].hints[1]` | $f_x = 2(x - y)$ and $f_y = -2(x - y)$. | correct | B32 |
| `screens[6].hints[2]` | Both are zero exactly when $x = y$. That is a whole line of points. | correct | B32 |
| `screens[6].feedback.correct` | The whole line $y = x$. | correct | B32 |
| `screens[6].feedback.generic` | Not quite right. Solve $2(x - y) = 0$ and $-2(x - y) = 0$ and count the solutions. | correct | B32 |
| `screens[6].explain.text` | You found that both partials are multiples of $x - y$. So both vanish at every point of $y = x$: a valley with a flat floor. Stationary points need... | correct | B32 |
| `screens[7].prose` | Each time you solved two equations together. For a function of two variables, $$\nabla f = \mathbf{0} \iff f_x(x, y) = 0 \text{ and } f_y(x, y) = 0... | correct | B32 |
| `screens[7].question` | Which system gives the stationary points of $f = x^2 + xy + y^2$? | correct | B32 |
| `screens[7].widget.options[0]` | option right (key): $2x + y = 0$ and $x + 2y = 0$ | correct | B32 |
| `screens[7].widget.options[1]` | option one: $2x + y = 0$ alone | correct | B32 |
| `screens[7].widget.options[1].why` | That is $f_x = 0$ only. It is a line; $f_y = 0$ cuts it down to points. | correct | B32 |
| `screens[7].widget.options[2]` | option drop: $2x = 0$ and $2y = 0$ | correct | B32 |
| `screens[7].widget.options[2].why` | You dropped the $xy$ term. Its $x$-partial is $y$ and its $y$-partial is $x$. | correct | B32 |
| `screens[7].widget.options[3]` | option f0: $x^2 + xy + y^2 = 0$ | correct | B32 |
| `screens[7].widget.options[3].why` | That sets the height to zero. Stationary means the slope is zero. | correct | B32 |
| `screens[7].hints[0]` | Differentiate each term, including $xy$. | correct | B32 |
| `screens[7].feedback.correct` | Both partials, set to zero together. | correct | B32 |
| `screens[7].feedback.generic` | Not quite right. Write $f_x$ and $f_y$, keeping the $xy$ term. | correct | B32 |
| `screens[7].explain.text` | The $xy$ term gives $y$ in $f_x$ and $x$ in $f_y$. The system $2x + y = 0$, $x + 2y = 0$ has the single solution $(0, 0)$. | correct | B32 |
| `screens[8].prose` | We found $(1, -2)$ for $f = x^2 + y^2 - 2x + 4y$. Completing the square shows it is the lowest point, not just a level one. | correct | B33 |
| `screens[8].question` | Put the lines of the derivation in order. | correct | B33 |
| `screens[8].widget.lines[0]` | line group: $f = (x^2 - 2x) + (y^2 + 4y)$, group the $x$ terms and the $y$ terms | correct | B33 |
| `screens[8].widget.lines[1]` | line square: $= (x - 1)^2 - 1 + (y + 2)^2 - 4$, complete each square | correct | B33 |
| `screens[8].widget.lines[2]` | line collect: $= (x - 1)^2 + (y + 2)^2 - 5$, collect the constants | correct | B33 |
| `screens[8].widget.lines[3]` | line bound: $\geq -5$, since squares are never negative, with equality only at $(1, -2)$ | correct | B33 |
| `screens[8].widget.answer` | group, square, collect, bound | correct | B33 |
| `screens[8].hints[0]` | Start by sorting the terms by variable. | correct | B33 |
| `screens[8].hints[1]` | $(x - 1)^2 = x^2 - 2x + 1$, so $x^2 - 2x = (x - 1)^2 - 1$. | correct | B33 |
| `screens[8].hints[2]` | Group, complete both squares, collect $-1 - 4 = -5$, then use that squares are at least 0. | correct | B33 |
| `screens[8].feedback.correct` | So $f \geq -5$, with the minimum at $(1, -2)$. | correct | B33 |
| `screens[8].feedback.generic` | Not quite right. Group by variable before completing the squares. | correct | B33 |
| `screens[8].feedback.byKey.bound` | The inequality needs the squares on show, so it comes last. | correct | B33 |
| `screens[8].feedback.byKey.square` | Group the terms by variable before you complete each square. | correct | B33 |
| `screens[8].explain.text` | Grouping, then completing both squares, writes $f$ as $(x - 1)^2 + (y + 2)^2 - 5$. Each square is zero only at $(1, -2)$. The contours $f = c$ are ... | correct | B33 |
| `screens[9].prose` | A desk runs two strategies at sizes $x$ and $y$, in £m. Their trades overlap, so expected daily P&L, in £k, is $$P = 10x + 8y - x^2 - y^2 - xy.$$ | correct | B32 |
| `screens[9].question` | At which sizes are both partial derivatives of $P$ zero? | correct | B32 |
| `screens[9].widget.options[0]` | option right (key): $x = 4$, $y = 2$ | correct | B32 |
| `screens[9].widget.options[1]` | option drop: $x = 5$, $y = 4$ | correct | B32 |
| `screens[9].widget.options[1].why` | You dropped the $-xy$ term: $10 - 2x = 0$ and $8 - 2y = 0$. The overlap pulls both sizes down. | correct | B32 |
| `screens[9].widget.options[2]` | option swap: $x = 2$, $y = 4$ | correct | B32 |
| `screens[9].widget.options[2].why` | You swapped the two answers. Check $P_x = 10 - 2x - y$ at $(2, 4)$: it is 2, not 0. | correct | B32 |
| `screens[9].widget.options[3]` | option one: $x = 5$, $y = 0$ | correct | B32 |
| `screens[9].widget.options[3].why` | You solved $P_x = 0$ with $y = 0$ and ignored $P_y$. There $P_y = 8 - 0 - 5 = 3$. | correct | B32 |
| `screens[9].hints[0]` | Write $P_x$ and $P_y$, keeping the $-xy$ term. | correct | B32 |
| `screens[9].hints[1]` | $P_x = 10 - 2x - y$ and $P_y = 8 - 2y - x$. From the first, $y = 10 - 2x$. Then $8 - 2(10 - 2x) - x = 0$ gives $3x = 12$, so $x = 4$ and $y = 2$. | correct | B32 |
| `screens[9].feedback.correct` | £4m and £2m, for an expected £28k a day. | correct | B32 |
| `screens[9].feedback.generic` | Not quite right. Solve $10 - 2x - y = 0$ and $8 - 2y - x = 0$ together. | correct | B32 |
| `screens[9].explain.text` | You solved the two linear equations together and got $(4, 2)$. There $P = 40 + 16 - 16 - 4 - 8 = 28$, so £28k a day. The rings close round it: whet... | correct | B32 |
| `summary.ideas[0]` | A stationary point is where $\nabla f = \mathbf{0}$: both partial derivatives vanish at once. | correct | B32 |
| `summary.ideas[1]` | Contours close into rings round a peak or a pit, and usually cross at a saddle. | correct | B32 |
| `summary.ideas[2]` | Solve $f_x = 0$ and $f_y = 0$ as one system. The answer can be one point, several, or a whole line. | correct | B32 |
| `summary.formula.name` | Stationary points | correct | B32 |
| `summary.formula.tex` | \nabla f = \mathbf{0} \iff f_x = 0 \text{ and } f_y = 0 | correct | B32 |
| `summary.formula.note` | Two equations in two unknowns, solved together. | correct | B32 |
| `summary.trap` | Setting only $f_x = 0$ gives a curve of points, not a point. The stationary points are where it meets $f_y = 0$. | correct | B32 |
| `quiz[0].prose` | Take $f(x, y) = x^2 + 6x + y^2 - 8y$. | correct | B32 |
| `quiz[0].question` | Where is its stationary point? | correct | B32 |
| `quiz[0].widget.options[0]` | option right (key): $(-3, 4)$ | correct | B32 |
| `quiz[0].widget.options[1]` | option signs: $(3, -4)$ | correct | B32 |
| `quiz[0].widget.options[1].why` | You flipped both signs. $2x + 6 = 0$ gives $x = -3$. | correct | B32 |
| `quiz[0].widget.options[2]` | option nohalf: $(-6, 8)$ | correct | B32 |
| `quiz[0].widget.options[2].why` | You set $x + 6 = 0$, forgetting the 2 in $2x$. | correct | B32 |
| `quiz[0].widget.options[3]` | option origin: $(0, 0)$ | correct | B32 |
| `quiz[0].widget.options[3].why` | At the origin $f_x = 6$ and $f_y = -8$, so the ground slopes. | correct | B32 |
| `quiz[0].feedback.correct` | $2x + 6 = 0$ and $2y - 8 = 0$. | correct | B32 |
| `quiz[0].feedback.generic` | Not quite right. Set $f_x = 2x + 6$ and $f_y = 2y - 8$ to zero. | correct | B32 |
| `quiz[0].explain.text` | $f_x = 2x + 6 = 0$ gives $x = -3$, and $f_y = 2y - 8 = 0$ gives $y = 4$. So the stationary point is $(-3, 4)$. | correct | B32 |
| `quiz[1].prose` | Take $f(x, y) = x^2 - y^3 + 3y$. | correct | B32 |
| `quiz[1].question` | How many stationary points does $f$ have? | correct | B32 |
| `quiz[1].widget.answer` | 2 | correct | B32 |
| `quiz[1].widget.accept` | 2: the points $(0, 1)$ and $(0, -1)$. | correct | B32 |
| `quiz[1].widget.wrong[0]` | slip one = 1 | correct | B32 |
| `quiz[1].widget.wrong[1]` | slip four = 4 | correct | B32 |
| `quiz[1].feedback.correct` | $(0, 1)$ and $(0, -1)$. | correct | B32 |
| `quiz[1].feedback.generic` | Not quite right. Solve $2x = 0$ and $3 - 3y^2 = 0$. | correct | B32 |
| `quiz[1].feedback.byKey.one` | You took only $y = 1$. $y^2 = 1$ has two roots. | correct | B32 |
| `quiz[1].feedback.byKey.four` | $x$ has only one value, $x = 0$, so there are $1 \times 2$ points. | correct | B32 |
| `quiz[1].explain.text` | $f_x = 2x = 0$ forces $x = 0$. $f_y = -3y^2 + 3 = 0$ gives $y = \pm 1$. That is two points. | correct | B32 |
| `quiz[2].prose` | On a contour map, two level curves cross at a stationary point P. The ground is higher than P between one pair of arms and lower between the other. | correct | B32 |
| `quiz[2].question` | What kind of stationary point is P? | correct | B32 |
| `quiz[2].widget.options[0]` | option saddle (key): A saddle | correct | B32 |
| `quiz[2].widget.options[1]` | option peak: A peak | correct | B32 |
| `quiz[2].widget.options[1].why` | At a peak the ground is lower on every side. Here it is higher between two of the arms. | correct | B32 |
| `quiz[2].widget.options[2]` | option pit: A pit | correct | B32 |
| `quiz[2].widget.options[2].why` | At a pit the ground is higher on every side. Here it is lower between two of the arms. | correct | B32 |
| `quiz[2].feedback.correct` | Up one way and down the other marks a saddle. | correct | B32 |
| `quiz[2].feedback.generic` | Not quite right. Think of $x^2 - y^2$ at the origin. | correct | B32 |
| `quiz[2].explain.text` | Higher ground one way and lower ground the other is a saddle, as for $x^2 - y^2$ at the origin. Crossing contours usually mean this. On $x^2y^2$ th... | correct | B32 |
| `quiz[3].prose` | Take $f(x, y) = (x + 2y)^2$. | correct | B32 |
| `quiz[3].question` | Which describes its stationary points? | correct | B32 |
| `quiz[3].widget.options[0]` | option right (key): Every point on the line $x + 2y = 0$ | correct | B32 |
| `quiz[3].widget.options[1]` | option origin: Only $(0, 0)$ | correct | B32 |
| `quiz[3].widget.options[1].why` | $(2, -1)$ also gives $x + 2y = 0$, so both partials vanish there too. | correct | B32 |
| `quiz[3].widget.options[2]` | option none: There are none | correct | B32 |
| `quiz[3].widget.options[2].why` | Both partials are multiples of $x + 2y$, which is zero along a whole line. | correct | B32 |
| `quiz[3].widget.options[3]` | option yx: Every point on the line $y = x$ | correct | B32 |
| `quiz[3].widget.options[3].why` | That was the valley of $(x - y)^2$. Here the bracket is $x + 2y$. | correct | B32 |
| `quiz[3].feedback.correct` | A whole line of stationary points. | correct | B32 |
| `quiz[3].feedback.generic` | Not quite right. Find $f_x$ and $f_y$ with the chain rule. | correct | B32 |
| `quiz[3].explain.text` | $f_x = 2(x + 2y)$ and $f_y = 4(x + 2y)$. Both vanish exactly when $x + 2y = 0$, a whole line. | correct | B32 |

## l10-second-derivative-test

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Classify stationary points with the Hessian. | correct | B34 |
| `objectives[1]` | Explain why the mixed partial can turn a point into a saddle. | correct | B34 |
| `screens[0].prose` | Last lesson, $f(x, y) = x^3 - 3x + y^2$ had two stationary points, A at $(1, 0)$ and B at $(-1, 0)$. The purple contour is $f = 2$; the innermost r... | correct | B34 |
| `screens[0].question` | What kind of point is each one? | correct | B34 |
| `screens[0].widget.options[0]` | option right (key): A is a pit and B is a saddle | correct | B34 |
| `screens[0].widget.options[1]` | option swap: A is a saddle and B is a pit | correct | B34 |
| `screens[0].widget.options[1].why` | You swapped them. Rings close round A, and the purple contours cross at B. | correct | B34 |
| `screens[0].widget.options[2]` | option peak: A is a peak and B is a saddle | correct | B34 |
| `screens[0].widget.options[2].why` | Rings close round a peak too, but here the heights fall towards A. The inner ring is $-1.5$ and $f(1, 0) = -2$. | correct | B34 |
| `screens[0].widget.options[3]` | option both: Both are pits | correct | B34 |
| `screens[0].widget.options[3].why` | Along the $x$-axis through B, $f = x^3 - 3x$ peaks at $x = -1$. Along the $y$-axis it rises. Up one way, down the other. | correct | B34 |
| `screens[0].hints[0]` | Do the contours close round the point, or cross at it? | correct | B34 |
| `screens[0].hints[1]` | The purple contours cross at B. | correct | B34 |
| `screens[0].hints[2]` | Rings close round A and the values fall towards it, so A is a pit. Crossing contours make B a saddle. | correct | B34 |
| `screens[0].feedback.correct` | A pit at A, a saddle at B. | correct | B34 |
| `screens[0].feedback.generic` | Not quite right. Rings mean a peak or a pit; crossing contours mean a saddle. | correct | B34 |
| `screens[0].explain.text` | You read the shapes: closing rings with falling values round A, crossing contours at B. That needed the picture. This lesson gets the same answer f... | correct | B34 |
| `screens[1].prose` | Take $f(x, y) = ax^2 + y^2$, with a stationary point at the origin. Here $f_{xx} = 2a$ and $f_{yy} = 2$. Slide $a$ and watch the contours. Blue has... | correct | B34 |
| `screens[1].question` | For which values of $a$ do the contours cross at the origin, making it a saddle? | correct | B34 |
| `screens[1].widget.options[0]` | option neg (key): $a < 0$, when $f_{xx}$ and $f_{yy}$ have opposite signs | correct | B34 |
| `screens[1].widget.options[1]` | option pos: $a > 0$ | correct | B34 |
| `screens[1].widget.options[1].why` | With $a > 0$ the contours close into ellipses: a pit. Slide $a$ below 0. | correct | B34 |
| `screens[1].widget.options[2]` | option zero: Only $a = 0$ | correct | B34 |
| `screens[1].widget.options[2].why` | At $a = 0$ the contours are parallel lines, a valley with a flat floor. Slide a little below 0. | correct | B34 |
| `screens[1].widget.options[3]` | option all: Every $a$ | correct | B34 |
| `screens[1].widget.options[3].why` | Set $a = 1$: the contours are circles round the origin, so it is a pit. | correct | B34 |
| `screens[1].hints[0]` | Try $a = 1$, then $a = -1$. | correct | B34 |
| `screens[1].hints[1]` | Watch the sign of the product in the caption. | correct | B34 |
| `screens[1].feedback.correct` | Opposite curvatures make a saddle. | correct | B34 |
| `screens[1].feedback.generic` | Not quite right. Slide $a$ to $-1$ and look at the origin. | correct | B34 |
| `screens[1].explain.text` | You saw circles and ellipses for $a > 0$, and crossing contours for $a < 0$. With no $xy$ term, the sign of $f_{xx} f_{yy}$ decides it. At $a = 0$ ... | correct | B34 |
| `screens[2].prose` | Collect the second partials of $f = x^3 - 3x + y^2$ in a grid: $f_{xx}$ and $f_{xy}$ on top, $f_{yx}$ and $f_{yy}$ below. This matrix is the **Hess... | correct | B34 |
| `screens[2].question` | What is $f_{xx} f_{yy} - f_{xy}^2$ at A, the determinant of $\mathbf{H}(1, 0)$? | correct | B34 |
| `screens[2].widget.answer` | 12 | correct | B34 |
| `screens[2].widget.accept` | 12, from $6 \times 2 - 0^2$. | correct | B34 |
| `screens[2].widget.wrong[0]` | slip trace = 8 | correct | B34 |
| `screens[2].widget.wrong[1]` | slip b = -12 | correct | B34 |
| `screens[2].widget.wrong[2]` | slip fxx = 6 | correct | B34 |
| `screens[2].hints[0]` | Multiply the diagonal, then subtract the square of the off-diagonal entry. | correct | B34 |
| `screens[2].hints[1]` | The diagonal of $\mathbf{H}(1, 0)$ is 6 and 2. The off-diagonal is 0. | correct | B34 |
| `screens[2].hints[2]` | $6 \times 2 - 0^2 = 12$. | correct | B34 |
| `screens[2].feedback.correct` | 12. | correct | B34 |
| `screens[2].feedback.generic` | Not quite right. Compute $6 \times 2 - 0^2$. | correct | B34 |
| `screens[2].feedback.byKey.trace` | You added the diagonal. The determinant multiplies it: $6 \times 2$. | correct | B34 |
| `screens[2].feedback.byKey.b` | That is the value at B, where $f_{xx} = 6(-1) = -6$. At A, $x = 1$. | correct | B34 |
| `screens[2].feedback.byKey.fxx` | That is $f_{xx}$ alone. Multiply by $f_{yy} = 2$ and subtract $f_{xy}^2$. | correct | B34 |
| `screens[2].explain.text` | You multiplied the diagonal and subtracted the off-diagonal squared. We call this number $D = \det \mathbf{H} = f_{xx} f_{yy} - f_{xy}^2$. Since $f... | correct | B34 |
| `screens[3].prose` | Here are the stationary points from last lesson, with their types from the contour maps. The functions are $f_1 = x^2 + y^2 - 2x + 4y$, $f_2 = x^3 ... | correct | B34 |
| `screens[3].question` | Fill in $D$ for each point. | correct | B34 |
| `screens[3].widget.columns` | Point, $f_{xx}$, $f_{yy}$, $f_{xy}$, $D$, Type | correct | B34 |
| `screens[3].widget.rows[0]` | $f_1$ at $(1, -2)$, 2, 2, 0, {"edit": true, "answer": 4, "tol": {"abs": 0}}, pit | correct | B34 |
| `screens[3].widget.rows[1]` | $f_2$ at $(1, 0)$, 6, 2, 0, {"edit": true, "answer": 12, "tol": {"abs": 0}}, pit | correct | B34 |
| `screens[3].widget.rows[2]` | $f_2$ at $(-1, 0)$, −6, 2, 0, {"edit": true, "answer": -12, "tol": {"abs": 0}}, saddle | correct | B34 |
| `screens[3].widget.rows[3]` | $f_3$ at $(0, 0)$, 2, −2, 0, {"edit": true, "answer": -4, "tol": {"abs": 0}}, saddle | correct | B34 |
| `screens[3].hints[0]` | Each row: multiply $f_{xx}$ by $f_{yy}$, then subtract $f_{xy}^2$. | correct | B34 |
| `screens[3].hints[1]` | Every $f_{xy}$ here is 0, so $D$ is just $f_{xx} f_{yy}$. | correct | B34 |
| `screens[3].hints[2]` | $2 \times 2 = 4$, $6 \times 2 = 12$, $-6 \times 2 = -12$, $2 \times (-2) = -4$. | correct | B34 |
| `screens[3].feedback.correct` | 4, 12, $-12$ and $-4$. | correct | B34 |
| `screens[3].feedback.generic` | Not quite right. Multiply $f_{xx}$ by $f_{yy}$ in each row; every $f_{xy}$ is 0. | correct | B34 |
| `screens[3].feedback.byKey.r2c4` | In the third row $f_{xx} = -6$, so $D = (-6)(2) = -12$. Keep the sign. | correct | B34 |
| `screens[3].feedback.byKey.r3c4` | In the last row $f_{yy} = -2$, so $D = (2)(-2) = -4$. | correct | B34 |
| `screens[3].explain.text` | You found $D > 0$ at both pits and $D < 0$ at both saddles. That pattern is the start of the test. Next we check what tells a pit from a peak. | correct | B34 |
| `screens[4].prose` | Take $f = 6x - x^2 + xy - y^2$. Its only stationary point is $(4, 2)$, where its Hessian is shown. So $D = (-2)(-2) - 1^2 = 3 > 0$. | correct | B34 |
| `screens[4].question` | What kind of point is $(4, 2)$? | correct | B34 |
| `screens[4].widget.options[0]` | option peak (key): A peak | correct | B34 |
| `screens[4].widget.options[1]` | option pit: A pit | correct | B34 |
| `screens[4].widget.options[1].why` | $D > 0$ says peak or pit, and you chose pit. But $f_{xx} = -2 < 0$: the slice along $x$ bends down. | correct | B34 |
| `screens[4].widget.options[2]` | option saddle: A saddle | correct | B34 |
| `screens[4].widget.options[2].why` | You took the mixed term as a sign of a saddle. It is small here: $D = 4 - 1 = 3 > 0$. | correct | B34 |
| `screens[4].widget.options[3]` | option none: No verdict | correct | B34 |
| `screens[4].widget.options[3].why` | The test is silent only when $D = 0$. Here $D = 3$. | correct | B34 |
| `screens[4].hints[0]` | $D > 0$ narrows it to two types. Which entry tells them apart? | correct | B34 |
| `screens[4].hints[1]` | Look at $f_{xx}$, the top-left entry. | correct | B34 |
| `screens[4].hints[2]` | $f_{xx} = -2 < 0$, so $f$ bends down along $x$. With $D > 0$ it bends down in every direction: a peak. | correct | B34 |
| `screens[4].feedback.correct` | $D > 0$ and $f_{xx} < 0$: a peak. | correct | B34 |
| `screens[4].feedback.generic` | Not quite right. With $D > 0$, the sign of $f_{xx}$ decides. | correct | B34 |
| `screens[4].explain.text` | You used $D > 0$ to rule out a saddle, then the sign of $f_{xx}$. When $D > 0$, $f_{xx}$ and $f_{yy}$ must share a sign, so either one decides. Bot... | correct | B34 |
| `screens[5].prose` | Take $f = x^2 + 4xy + y^2$, stationary at the origin. Along the $x$-axis $f = x^2$, and along the $y$-axis $f = y^2$. So $f_{xx} = 2 > 0$ and $f_{y... | correct | B34 |
| `screens[5].question` | What kind of point is the origin? | correct | B34 |
| `screens[5].widget.options[0]` | option pit: A pit: $f$ curves up along both axes | correct | B34 |
| `screens[5].widget.options[0].why` | You read $f_{xx} > 0$ and $f_{yy} > 0$ and stopped. Along $y = -x$, $f = x^2 - 4x^2 + x^2 = -2x^2$, which falls. | correct | B34 |
| `screens[5].widget.options[1]` | option saddle (key): A saddle | correct | B34 |
| `screens[5].widget.options[2]` | option peak: A peak | correct | B34 |
| `screens[5].widget.options[2].why` | $f$ rises along both axes, so the origin cannot be the top. | correct | B34 |
| `screens[5].widget.options[3]` | option none: The test gives no verdict | correct | B34 |
| `screens[5].widget.options[3].why` | $D = 2 \times 2 - 4^2 = -12$. The test is silent only when $D = 0$. | correct | B34 |
| `screens[5].hints[0]` | Compute $f_{xy}$ before deciding. | correct | B34 |
| `screens[5].hints[1]` | $f_{xy} = 4$, so $D = 2 \times 2 - 4^2$. | correct | B34 |
| `screens[5].hints[2]` | $D = 4 - 16 = -12 < 0$: a saddle. Walk along $y = -x$ to see $f$ fall. | correct | B34 |
| `screens[5].feedback.correct` | $D = -12 < 0$: a saddle. | correct | B34 |
| `screens[5].feedback.generic` | Not quite right. Include $f_{xy} = 4$ in $D$. | correct | B34 |
| `screens[5].feedback.byKey.pit` | You classified from $f_{xx}$ and $f_{yy}$ alone. The mixed term $4xy$ is negative when $x$ and $y$ have opposite signs, and it wins along $y = -x$. | correct | B34 |
| `screens[5].explain.text` | The two axis slices both curve up, but the diagonal slice $f = -2t^2$ curves down. $D = 4 - 16 = -12$ catches this: the mixed term outweighs the pu... | correct | B34 |
| `screens[6].prose` | At a stationary point, let $D = \det \mathbf{H} = f_{xx} f_{yy} - f_{xy}^2$. $$\begin{aligned} D > 0,\ f_{xx} > 0 &: \text{pit} \\ D > 0,\ f_{xx} <... | imprecise | finding 5: the test is stated with no hypothesis; it needs continuous second partials near the point (Apostol II Theorem 9.7; Marsden-Tromba 3.3 Theorem 6) |
| `screens[6].question` | For $f = (x - y)^2$, $D = 2 \times 2 - (-2)^2 = 0$ at every point of $y = x$. What does the test say? | correct | B34 |
| `screens[6].widget.options[0]` | option none (key): Nothing: we must look at $f$ another way | correct | B34 |
| `screens[6].widget.options[1]` | option saddle: Each point is a saddle | correct | B34 |
| `screens[6].widget.options[1].why` | $D = 0$ is not negative. And $f \geq 0$ everywhere, so $f$ never falls below these points. | correct | B34 |
| `screens[6].widget.options[2]` | option pit: Each point is a pit | correct | B34 |
| `screens[6].widget.options[2].why` | That is true here, but the test did not say so. $x^4 - y^4$ also has $D = 0$ at the origin, and it is a saddle. | correct | B34 |
| `screens[6].hints[0]` | Which row of the test has $D = 0$? | correct | B34 |
| `screens[6].feedback.correct` | $D = 0$ gives no verdict. | correct | B34 |
| `screens[6].feedback.generic` | Not quite right. Read the last row of the test. | correct | B34 |
| `screens[6].explain.text` | When $D = 0$ the quadratic part of $f$ is flat in some direction, so higher terms decide. Here $f = (x - y)^2 \geq 0$ shows each point is a lowest ... | correct | B34 |
| `screens[7].prose` | Write $A = f_{xx}$, $B = f_{xy}$, $C = f_{yy}$ at the stationary point, so $D = AC - B^2$. Step away by $(h, k)$. | correct | B35 |
| `screens[7].question` | Put the lines of the derivation in order. | correct | B35 |
| `screens[7].widget.lines[0]` | line taylor: $f(x_0 + h, y_0 + k) - f(x_0, y_0) \approx \tfrac{1}{2}(Ah^2 + 2Bhk + Ck^2)$, second-order Taylor; the linear part is 0 since $\nabla ... | correct | B35 |
| `screens[7].widget.lines[1]` | line square: $Ah^2 + 2Bhk + Ck^2 = A\left(h + \tfrac{B}{A}k\right)^2 + \left(C - \tfrac{B^2}{A}\right)k^2$, complete the square in $h$ (with $A \ne... | correct | B35 |
| `screens[7].widget.lines[2]` | line dee: $= A\left(h + \tfrac{B}{A}k\right)^2 + \tfrac{D}{A}k^2$, since $C - \tfrac{B^2}{A} = \tfrac{AC - B^2}{A}$ | correct | B35 |
| `screens[7].widget.lines[3]` | line verdict: So if $D > 0$ both terms have the sign of $A$; if $D < 0$ they have opposite signs | correct | B35 |
| `screens[7].widget.answer` | taylor, square, dee, verdict | correct | B35 |
| `screens[7].hints[0]` | Start from what $f$ looks like near the point. | correct | B35 |
| `screens[7].hints[1]` | The square has to be completed before $D$ can appear. | correct | B35 |
| `screens[7].hints[2]` | Taylor, then complete the square, then spot $D/A$, then read off the signs. | correct | B35 |
| `screens[7].feedback.correct` | The signs of $A$ and $D/A$ decide everything. | correct | B35 |
| `screens[7].feedback.generic` | Not quite right. $D$ appears only after completing the square. | correct | B35 |
| `screens[7].feedback.byKey.dee` | The fraction $D/A$ comes from the coefficient $C - B^2/A$, so complete the square first. | correct | B35 |
| `screens[7].feedback.byKey.verdict` | The verdict reads the two coefficients, so it comes last. | correct | B35 |
| `screens[7].explain.text` | Completing the square splits the change in $f$ into two squares with coefficients $A$ and $D/A$. With $D > 0$ they share a sign: a pit if $A > 0$, ... | correct | B35 |
| `screens[8].prose` | A researcher tunes two parameters of a strategy: lookback and entry threshold. Near the best pair found, the backtest Sharpe ratio has zero gradien... | correct | B34 |
| `screens[8].question` | Is this pair a local best for the Sharpe ratio? | correct | B34 |
| `screens[8].widget.options[0]` | option saddle (key): No: it is a saddle | correct | B34 |
| `screens[8].widget.options[1]` | option peak: Yes: it is a peak, since both diagonal entries are negative | correct | B34 |
| `screens[8].widget.options[1].why` | You classified from the diagonal alone. $D = (-0.8)(-0.2) - 0.5^2 = 0.16 - 0.25 = -0.09 < 0$. | correct | B34 |
| `screens[8].widget.options[2]` | option pit: No: it is a pit | correct | B34 |
| `screens[8].widget.options[2].why` | A pit needs $D > 0$ and $f_{xx} > 0$. Here $f_{xx} = -0.8$. | correct | B34 |
| `screens[8].widget.options[3]` | option none: The test cannot tell | correct | B34 |
| `screens[8].widget.options[3].why` | The test is silent only when $D = 0$. Here $D = -0.09$. | correct | B34 |
| `screens[8].hints[0]` | Compute $D$ before looking at signs. | correct | B34 |
| `screens[8].hints[1]` | $D = (-0.8)(-0.2) - 0.5^2$. | correct | B34 |
| `screens[8].hints[2]` | $0.16 - 0.25 = -0.09 < 0$, so it is a saddle. | correct | B34 |
| `screens[8].feedback.correct` | A saddle: the Sharpe ratio still rises in some direction. | correct | B34 |
| `screens[8].feedback.generic` | Not quite right. Include the off-diagonal $0.5$ in $D$. | correct | B34 |
| `screens[8].explain.text` | You found $D = 0.16 - 0.25 = -0.09$. Moving both parameters together in the right proportion still raises the Sharpe ratio. The search stopped at a... | correct | B34 |
| `summary.ideas[0]` | The Hessian collects the second partials: $\mathbf{H} = \begin{pmatrix} f_{xx} & f_{xy} \\ f_{xy} & f_{yy} \end{pmatrix}$, and $D = \det \mathbf{H}$. | correct | B34 |
| `summary.ideas[1]` | At a stationary point, $D < 0$ means a saddle. $D > 0$ means a pit if $f_{xx} > 0$ and a peak if $f_{xx} < 0$. | imprecise | finding 5 (same defect) |
| `summary.ideas[2]` | $D = 0$ gives no verdict: $x^4 + y^4$ is a pit and $x^4 - y^4$ a saddle, both with $D = 0$. | correct | B34 |
| `summary.formula.name` | Second derivative test | correct | B34 |
| `summary.formula.tex` | D = f_{xx} f_{yy} - f_{xy}^2 | correct | B34 |
| `summary.formula.note` | $D > 0$: the sign of $f_{xx}$ picks pit or peak. $D < 0$: saddle. $D = 0$: no verdict. | correct | B34 |
| `summary.trap` | Two positive pure second partials do not make a pit: $x^2 + 4xy + y^2$ has $D = -12$ and is a saddle. | correct | B34 |
| `quiz[0].prose` | At a stationary point the Hessian is $\begin{pmatrix} 4 & 2 \\ 2 & 3 \end{pmatrix}$. | correct | B34 |
| `quiz[0].question` | What is $D$? | correct | B34 |
| `quiz[0].widget.answer` | 8 | correct | B34 |
| `quiz[0].widget.accept` | 8, from $4 \times 3 - 2^2$. | correct | B34 |
| `quiz[0].widget.wrong[0]` | slip plus = 16 | correct | B34 |
| `quiz[0].widget.wrong[1]` | slip nosq = 10 | correct | B34 |
| `quiz[0].feedback.correct` | $12 - 4 = 8$. | correct | B34 |
| `quiz[0].feedback.generic` | Not quite right. Multiply the diagonal and subtract the off-diagonal squared. | correct | B34 |
| `quiz[0].feedback.byKey.plus` | You added $f_{xy}^2$. The determinant subtracts it. | correct | B34 |
| `quiz[0].feedback.byKey.nosq` | You subtracted 2, not $2^2 = 4$. | correct | B34 |
| `quiz[0].explain.text` | $D = 4 \times 3 - 2^2 = 12 - 4 = 8$. With $f_{xx} = 4 > 0$ the point is a pit. | correct | B34 |
| `quiz[1].prose` | Take $f = x^2 + 3xy + y^2$, stationary at the origin. | correct | B34 |
| `quiz[1].question` | What kind of point is the origin? | correct | B34 |
| `quiz[1].widget.options[0]` | option saddle (key): A saddle | correct | B34 |
| `quiz[1].widget.options[1]` | option pit: A pit | correct | B34 |
| `quiz[1].widget.options[1].why` | You used $f_{xx} = f_{yy} = 2 > 0$ only. With $f_{xy} = 3$, $D = 4 - 9 = -5$. | correct | B34 |
| `quiz[1].widget.options[2]` | option peak: A peak | correct | B34 |
| `quiz[1].widget.options[2].why` | $f_{xx} = 2 > 0$, so it cannot be a peak. | correct | B34 |
| `quiz[1].widget.options[3]` | option none: No verdict | correct | B34 |
| `quiz[1].widget.options[3].why` | $D = -5$, not 0. | correct | B34 |
| `quiz[1].feedback.correct` | $D = 4 - 9 = -5 < 0$. | correct | B34 |
| `quiz[1].feedback.generic` | Not quite right. Compute $D$ with $f_{xy} = 3$. | correct | B34 |
| `quiz[1].explain.text` | $f_{xx} = 2$, $f_{yy} = 2$, $f_{xy} = 3$, so $D = 4 - 9 = -5 < 0$. The mixed term wins, and the origin is a saddle. | correct | B34 |
| `quiz[2].prose` | Take $f = x^4 + y^4$. At the origin every second partial is 0, so $D = 0$. | correct | B34 |
| `quiz[2].question` | What is the origin? | correct | B34 |
| `quiz[2].widget.options[0]` | option right (key): A pit: the test is silent, but $f \geq 0 = f(0, 0)$ | correct | B34 |
| `quiz[2].widget.options[1]` | option saddle: A saddle, because $D$ is not positive | correct | B34 |
| `quiz[2].widget.options[1].why` | A saddle needs $D < 0$. Here $D = 0$, and $f$ is never below $f(0, 0) = 0$. | correct | B34 |
| `quiz[2].widget.options[2]` | option notstat: Not a stationary point | correct | B34 |
| `quiz[2].widget.options[2].why` | $f_x = 4x^3$ and $f_y = 4y^3$ are both 0 at the origin. | correct | B34 |
| `quiz[2].feedback.correct` | The test is silent, but $f$ itself shows a pit. | correct | B34 |
| `quiz[2].feedback.generic` | Not quite right. With $D = 0$, look at $f$ directly. | correct | B34 |
| `quiz[2].explain.text` | $D = 0$ gives no verdict. But $x^4 + y^4 \geq 0$ with equality only at the origin, so it is the lowest point. This is the edge case where the test ... | correct | B34 |
| `quiz[3].prose` | Last lesson a desk's P&L was $P = 10x + 8y - x^2 - y^2 - xy$, stationary at $(4, 2)$. | correct | B34 |
| `quiz[3].question` | What kind of point is it? | correct | B34 |
| `quiz[3].widget.options[0]` | option peak (key): A peak | correct | B34 |
| `quiz[3].widget.options[1]` | option pit: A pit | correct | B34 |
| `quiz[3].widget.options[1].why` | $D = 3 > 0$, but $P_{xx} = -2 < 0$, so $P$ bends down. | correct | B34 |
| `quiz[3].widget.options[2]` | option saddle: A saddle | correct | B34 |
| `quiz[3].widget.options[2].why` | $D = (-2)(-2) - (-1)^2 = 3 > 0$, so not a saddle. | correct | B34 |
| `quiz[3].widget.options[3]` | option none: No verdict | correct | B34 |
| `quiz[3].widget.options[3].why` | $D = 3$, not 0. | correct | B34 |
| `quiz[3].feedback.correct` | $D = 3 > 0$ and $P_{xx} < 0$: the best sizes nearby. | correct | B34 |
| `quiz[3].feedback.generic` | Not quite right. $P_{xx} = -2$, $P_{yy} = -2$, $P_{xy} = -1$. | correct | B34 |
| `quiz[3].explain.text` | $D = (-2)(-2) - (-1)^2 = 3 > 0$ and $P_{xx} = -2 < 0$. So $(4, 2)$ is a peak: £28k a day is the best the desk can expect nearby. | correct | B34 |

## l11-on-a-constraint

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Use a Lagrange multiplier to optimise along a constraint curve. | correct | B36 |
| `objectives[1]` | Interpret the multiplier as the value of relaxing the constraint. | correct | B36 |
| `screens[0].prose` | The blue curves are contours of $f(x, y) = xy$. Point P must stay on the orange line $x + y = 10$. Drag P along it and watch the value of $f$. | correct | B36 |
| `screens[0].question` | What is the largest value of $f$ you can reach on the line? | correct | B36 |
| `screens[0].widget.answer` | 25 | correct | B36 |
| `screens[0].widget.accept` | 25, at $(5, 5)$. | correct | B36 |
| `screens[0].widget.wrong[0]` | slip free = 100 | correct | B36 |
| `screens[0].widget.wrong[1]` | slip near = 24.75 | correct | B36 |
| `screens[0].hints[0]` | Watch the caption as P slides. Where does it stop rising? | correct | B36 |
| `screens[0].hints[1]` | Look for the contour that only touches the line. | correct | B36 |
| `screens[0].hints[2]` | At $(5, 5)$, $f = 25$. Either side of it, $f$ falls. | correct | B36 |
| `screens[0].feedback.correct` | 25, at $(5, 5)$. | correct | B36 |
| `screens[0].feedback.generic` | Not quite right. Slide P until the caption stops rising. | correct | B36 |
| `screens[0].feedback.byKey.free` | That would need both $x$ and $y$ at 10, off the line. P must keep $x + y = 10$. | correct | B36 |
| `screens[0].feedback.byKey.near` | $(4.5, 5.5)$ gives 24.75. Slide half a step more, to $(5, 5)$. | correct | B36 |
| `screens[0].explain.text` | You slid P until $f$ stopped rising, at $(5, 5)$ with $f = 25$. There the contour $xy = 25$ touches the line without crossing it. Any higher contou... | correct | B36 |
| `screens[1].prose` | At P $= (5, 5)$, $\nabla f = (y, x) = (5, 5)$, drawn at 0.4 scale. The constraint is $g(x, y) = x + y = 10$, with $\nabla g = (1, 1)$. At Q $= (2, ... | correct | B36 |
| `screens[1].question` | What number $\lambda$ makes $\nabla f = \lambda \nabla g$ at P? | correct | B36 |
| `screens[1].widget.answer` | 5 | correct | B36 |
| `screens[1].widget.accept` | 5: $(5, 5) = 5 \times (1, 1)$. | correct | B36 |
| `screens[1].widget.wrong[0]` | slip one = 1 | correct | B36 |
| `screens[1].widget.wrong[1]` | slip inv = 0.2 | correct | B36 |
| `screens[1].widget.wrong[2]` | slip fval = 25 | correct | B36 |
| `screens[1].hints[0]` | Which multiple of $(1, 1)$ is $(5, 5)$? | correct | B36 |
| `screens[1].hints[1]` | Compare the arrows at P. | correct | B36 |
| `screens[1].hints[2]` | $(5, 5) = 5 \times (1, 1)$, so $\lambda = 5$. | correct | B36 |
| `screens[1].feedback.correct` | $\lambda = 5$. | correct | B36 |
| `screens[1].feedback.generic` | Not quite right. Find the number that scales $(1, 1)$ to $(5, 5)$. | correct | B36 |
| `screens[1].feedback.byKey.one` | With $\lambda = 1$ you would need $\nabla f = (1, 1)$. Here $\nabla f = (5, 5)$: same direction, five times longer. | correct | B36 |
| `screens[1].feedback.byKey.inv` | You divided the wrong way. $\lambda$ multiplies $\nabla g$ to give $\nabla f$. | correct | B36 |
| `screens[1].feedback.byKey.fval` | 25 is the value of $f$, not the scale between the gradients. | correct | B36 |
| `screens[1].explain.text` | At Q, $\nabla f$ leans along the line, so sliding P raises $f$. At the best point it has no part along the line, so it lines up with $\nabla g$: $\... | correct | B36 |
| `screens[2].prose` | Maximise $f = x + 2y$ on the circle $g = x^2 + y^2 = 5$. Blue lines are contours of $f$. Solve $\nabla f = \lambda \nabla g$ together with $x^2 + y... | correct | B36 |
| `screens[2].question` | Tap the point where $f$ is largest on the circle. | correct | B36 |
| `screens[2].widget.answer` | A | correct | B36 |
| `screens[2].hints[0]` | Write $\nabla f = (1, 2)$ and $\nabla g = (2x, 2y)$. | correct | B36 |
| `screens[2].hints[1]` | $1 = 2\lambda x$ and $2 = 2\lambda y$, so $y = 2x$. | correct | B36 |
| `screens[2].hints[2]` | Put $y = 2x$ into $x^2 + y^2 = 5$: $5x^2 = 5$, so $x = \pm 1$. $f(1, 2) = 5$ and $f(-1, -2) = -5$. | correct | B36 |
| `screens[2].feedback.correct` | $(1, 2)$, where $f = 5$. | correct | B36 |
| `screens[2].feedback.generic` | Not quite right. From $y = 2x$ and $x^2 + y^2 = 5$, find both solutions and compare $f$. | correct | B36 |
| `screens[2].feedback.byKey.B` | B solves the equations too, but $f(-1, -2) = -5$. That is the minimum. | correct | B36 |
| `screens[2].feedback.byKey.C` | At C, $f = 2 + 2 = 4$. You swapped $x$ and $y$: the condition gives $y = 2x$. | correct | B36 |
| `screens[2].feedback.byKey.D` | D solves $\nabla f = \nabla g$ with no $\lambda$. It is inside the circle, so it breaks the constraint. | correct | B36 |
| `screens[2].feedback.byKey.E` | At E, $f = 2 \times 2.236 = 4.47$. The contour through E crosses the circle, so $f$ can still rise. | correct | B36 |
| `screens[2].explain.text` | You solved $y = 2x$ with the circle and got two points. The contour $f = 5$ touches the circle at A, and $f = -5$ touches at B. The system finds bo... | correct | B36 |
| `screens[3].prose` | Minimise $f = (x - 1)^2 + (y - 1)^2$ on the line $x + y = 2$. Here $\nabla f = (2(x - 1), 2(y - 1))$ and $\nabla g = (1, 1)$. | correct | B36 |
| `screens[3].question` | Solve the system. What is $\lambda$ at the minimum? | correct | B36 |
| `screens[3].widget.answer` | 0 | correct | B36 |
| `screens[3].widget.accept` | 0: the minimum is $(1, 1)$, where $\nabla f = (0, 0)$. | correct | B36 |
| `screens[3].widget.wrong[0]` | slip one = 1 | correct | B36 |
| `screens[3].widget.wrong[1]` | slip two = 2 | correct | B36 |
| `screens[3].hints[0]` | The two equations give $2(x - 1) = \lambda$ and $2(y - 1) = \lambda$. | correct | B36 |
| `screens[3].hints[1]` | So $x = y$. With $x + y = 2$ that is the point $(1, 1)$. | correct | B36 |
| `screens[3].hints[2]` | At $(1, 1)$, $2(x - 1) = 0$, so $\lambda = 0$. | correct | B36 |
| `screens[3].feedback.correct` | $\lambda = 0$. | correct | B36 |
| `screens[3].feedback.generic` | Not quite right. Find the point first, then $\lambda = 2(x - 1)$ there. | correct | B36 |
| `screens[3].feedback.byKey.one` | You may have taken $\lambda = 1$ to match $\nabla f = \nabla g$. At $(1, 1)$, $\nabla f = (0, 0) = 0 \times (1, 1)$. | correct | B36 |
| `screens[3].feedback.byKey.two` | 2 is the constant in the constraint, not the multiplier. At $(1, 1)$, $\nabla f = (0, 0)$. | correct | B36 |
| `screens[3].explain.text` | The line passes through the centre of the rings, the free minimum. There $\nabla f = \mathbf{0}$, so $\lambda = 0$. A zero multiplier says the cons... | correct | B36 |
| `screens[4].prose` | Back to $xy$ on $x + y = 10$: the best value is 25, with $\lambda = 5$. Now the line moves out a little, to $x + y = 10.2$. | correct | B36 |
| `screens[4].question` | Use $\lambda$ to estimate the best value of $xy$ on $x + y = 10.2$. | correct | B36 |
| `screens[4].widget.answer` | 26 | correct | B36 |
| `screens[4].widget.accept` | 26 from $25 + 5 \times 0.2$; the exact value is $5.1^2 = 26.01$. | correct | B36 |
| `screens[4].widget.wrong[0]` | slip budget = 25.2 | correct | B36 |
| `screens[4].widget.wrong[1]` | slip same = 25 | correct | B36 |
| `screens[4].hints[0]` | $\lambda$ is the rate the best value changes as the constant 10 changes. | correct | B36 |
| `screens[4].hints[1]` | The constant rises by 0.2. | correct | B36 |
| `screens[4].hints[2]` | $25 + 5 \times 0.2 = 26$. The exact best is $5.1 \times 5.1 = 26.01$. | correct | B36 |
| `screens[4].feedback.correct` | About 26; exactly $5.1^2 = 26.01$. | correct | B36 |
| `screens[4].feedback.generic` | Not quite right. Add $\lambda$ times the change in the constant. | correct | B36 |
| `screens[4].feedback.byKey.budget` | You added the 0.2 itself. Each unit of extra budget is worth $\lambda = 5$ units of $f$. | correct | B36 |
| `screens[4].feedback.byKey.same` | The best value does change: a longer line reaches a higher contour. | correct | B36 |
| `screens[4].explain.text` | The best value on $x + y = c$ is $c^2/4$, whose slope at $c = 10$ is 5: exactly $\lambda$. So $\lambda$ is the price of the constraint, the gain pe... | correct | B36 |
| `screens[5].prose` | Maximise $f = x + y$ on the circle $x^2 + y^2 = 8$. Here $\nabla f = (1, 1)$ and $\nabla g = (2x, 2y)$. | correct | B36 |
| `screens[5].question` | Where is the maximum, and what is it? | correct | B36 |
| `screens[5].widget.options[0]` | option right (key): $f = 4$, at $(2, 2)$ | correct | B36 |
| `screens[5].widget.options[1]` | option nolambda: $f = 1$, at $(0.5, 0.5)$ | correct | B36 |
| `screens[5].widget.options[1].why` | You set $\nabla f = \nabla g$ with no $\lambda$: $1 = 2x$ and $1 = 2y$. That point is not on the circle, since $0.25 + 0.25 \neq 8$. | correct | B36 |
| `screens[5].widget.options[2]` | option noconstraint: Every point on the line $y = x$ | correct | B36 |
| `screens[5].widget.options[2].why` | You matched the gradients, got $x = y$, then stopped. The constraint $x^2 + y^2 = 8$ still has to hold: it picks two points. | correct | B36 |
| `screens[5].widget.options[3]` | option min: $f = -4$, at $(-2, -2)$ | correct | B36 |
| `screens[5].widget.options[3].why` | That point solves the system too, but it gives the smallest value of $f$ on the circle. | correct | B36 |
| `screens[5].hints[0]` | Write all three equations: two from the gradients, one from the circle. | correct | B36 |
| `screens[5].hints[1]` | $1 = 2\lambda x$ and $1 = 2\lambda y$ give $x = y$. | correct | B36 |
| `screens[5].hints[2]` | Then $2x^2 = 8$, so $x = \pm 2$. $f(2, 2) = 4$ is the larger. | correct | B36 |
| `screens[5].feedback.correct` | $f = 4$ at $(2, 2)$, with $\lambda = \tfrac{1}{4}$. | correct | B36 |
| `screens[5].feedback.generic` | Not quite right. Use $\nabla f = \lambda \nabla g$ and the circle equation together. | correct | B36 |
| `screens[5].feedback.byKey.nolambda` | You dropped $\lambda$. The gradients need only point the same way; their lengths may differ. | correct | B36 |
| `screens[5].feedback.byKey.noconstraint` | You forgot the constraint equation. Without it, two equations cannot fix three unknowns. | correct | B36 |
| `screens[5].explain.text` | The gradient equations give $x = y$, and only the circle equation turns that into points: $(2, 2)$ and $(-2, -2)$. At $(2, 2)$, $1 = 2\lambda \time... | correct | B36 |
| `screens[6].prose` | To find the largest or smallest $f$ on the curve $g(x, y) = c$, solve $$\nabla f = \lambda \nabla g, \qquad g(x, y) = c.$$ That is $f_x = \lambda g... | correct | B36 |
| `screens[6].question` | How many unknowns does this system solve for? | correct | B36 |
| `screens[6].widget.options[0]` | option three (key): Three: $x$, $y$ and $\lambda$ | correct | B36 |
| `screens[6].widget.options[1]` | option two: Two: $x$ and $y$ | correct | B36 |
| `screens[6].widget.options[1].why` | $\lambda$ is unknown too. That is why the constraint equation is needed as a third equation. | correct | B36 |
| `screens[6].widget.options[2]` | option one: One: $\lambda$ | correct | B36 |
| `screens[6].widget.options[2].why` | The point $(x, y)$ is what we are after. $\lambda$ is found along the way. | correct | B36 |
| `screens[6].hints[0]` | Count the letters that are not known in advance. | correct | B36 |
| `screens[6].feedback.correct` | Three equations, three unknowns. | correct | B36 |
| `screens[6].feedback.generic` | Not quite right. Count $x$, $y$ and $\lambda$. | correct | B36 |
| `screens[6].explain.text` | Two gradient equations and the constraint make three equations in $x$, $y$ and $\lambda$. Drop any one and the system no longer pins down the points. | correct | B36 |
| `screens[7].prose` | Maximise $f = xy$ on $x + y = 10$ with the Lagrange conditions. | correct | B36 |
| `screens[7].question` | Put the lines of the solution in order. | correct | B36 |
| `screens[7].widget.lines[0]` | line grads: $\nabla f = (y, x)$ and $\nabla g = (1, 1)$, the partials of $xy$ and of $x + y$ | correct | B36 |
| `screens[7].widget.lines[1]` | line match: $y = \lambda$ and $x = \lambda$, matching components of $\nabla f = \lambda \nabla g$ | correct | B36 |
| `screens[7].widget.lines[2]` | line equal: So $x = y$, since both equal $\lambda$ | correct | B36 |
| `screens[7].widget.lines[3]` | line sub: $2x = 10$, so $x = y = 5$, substituting into $x + y = 10$ | correct | B36 |
| `screens[7].widget.lines[4]` | line value: $f = 25$ and $\lambda = 5$ | correct | B36 |
| `screens[7].widget.answer` | grads, match, equal, sub, value | correct | B36 |
| `screens[7].hints[0]` | Gradients first, then the equations they give. | correct | B36 |
| `screens[7].hints[1]` | The constraint is used only after $x = y$ is known. | correct | B36 |
| `screens[7].hints[2]` | Gradients, match components, $x = y$, substitute, read off $f$ and $\lambda$. | correct | B36 |
| `screens[7].feedback.correct` | The same $(5, 5)$ you found by dragging. | correct | B36 |
| `screens[7].feedback.generic` | Not quite right. You need the gradients before you can match them. | correct | B36 |
| `screens[7].feedback.byKey.sub` | Substituting needs $x = y$ first, which comes from matching the components. | correct | B36 |
| `screens[7].feedback.byKey.value` | The values come last, once the point is known. | correct | B36 |
| `screens[7].explain.text` | Matching components gave $x = y = \lambda$. The constraint then fixed $x = y = 5$. So the best value is 25, with $\lambda = 5$, as the drag and the... | correct | B36 |
| `screens[8].prose` | A fund puts $a$ and $b$, in £m, into two uncorrelated strategies of equal volatility. Expected profit is $3a + 4b$, in £k. The risk limit is $a^2 +... | correct | B36 |
| `screens[8].question` | What is the largest expected profit, in £k, within the risk limit? | correct | B36 |
| `screens[8].widget.answer` | 25 | correct | B36 |
| `screens[8].widget.accept` | 25, from $a = 3$, $b = 4$. | correct | B36 |
| `screens[8].widget.wrong[0]` | slip allb = 20 | correct | B36 |
| `screens[8].widget.wrong[1]` | slip alla = 15 | correct | B36 |
| `screens[8].widget.wrong[2]` | slip half = 24.75 | correct | B36 |
| `screens[8].widget.wrong[3]` | slip square = 35 | correct | B36 |
| `screens[8].hints[0]` | Solve $(3, 4) = \lambda (2a, 2b)$ with $a^2 + b^2 = 25$. | correct | B36 |
| `screens[8].hints[1]` | The equations give $b/a = 4/3$. | correct | B36 |
| `screens[8].hints[2]` | $b = \tfrac{4}{3}a$ and $a^2 + \tfrac{16}{9}a^2 = 25$ give $a = 3$, $b = 4$. Profit $= 9 + 16 = 25$. | correct | B36 |
| `screens[8].feedback.correct` | £25k, from £3m and £4m. | correct | B36 |
| `screens[8].feedback.generic` | Not quite right. Use $\nabla f = \lambda \nabla g$ with the risk limit. | correct | B36 |
| `screens[8].feedback.byKey.allb` | You put the whole budget into the better strategy: $b = 5$ gives £20k. Splitting does better, because risk adds in squares. | correct | B36 |
| `screens[8].feedback.byKey.alla` | All in $a$ gives only £15k. The strategy with the higher return deserves more, not all. | correct | B36 |
| `screens[8].feedback.byKey.half` | An equal split, $a = b = 3.54$, gives about £24.7k. The better strategy deserves a larger share. | correct | B36 |
| `screens[8].feedback.byKey.square` | $a = b = 5$ gives £35k, but $25 + 25 = 50$ breaks the risk limit of 25. | correct | B36 |
| `screens[8].explain.text` | The conditions gave $3 = 2\lambda a$ and $4 = 2\lambda b$, so sizes in proportion to returns: $a = 3$, $b = 4$, $\lambda = 0.5$. The £25k contour t... | correct | B36 |
| `summary.ideas[0]` | On a constraint, the best point is where a contour of $f$ touches the constraint curve without crossing it. | correct | B36 |
| `summary.ideas[1]` | There the gradients line up: $\nabla f = \lambda \nabla g$. Solve this with $g = c$, then compare $f$ at every solution. That finds the largest or ... | correct | B36 |
| `summary.ideas[2]` | $\lambda$ is the gain in the best value per unit the constraint is relaxed. $\lambda = 0$ means the constraint is not binding. | correct | B36 |
| `summary.formula.name` | Lagrange conditions | correct | B36 |
| `summary.formula.tex` | \nabla f = \lambda \nabla g, \quad g(x, y) = c | correct | B36 |
| `summary.formula.note` | Three equations in $x$, $y$ and $\lambda$. They assume $\nabla g \neq \mathbf{0}$ on the curve. | correct | B36 |
| `summary.trap` | Setting $\nabla f = \nabla g$ without $\lambda$ gives a point off the curve. Dropping $g = c$ leaves a whole curve of candidates. | correct | B36 |
| `quiz[0].prose` | Maximise $xy$ on the line $x + y = 6$. | correct | B36 |
| `quiz[0].question` | What is the largest value? | correct | B36 |
| `quiz[0].widget.answer` | 9 | correct | B36 |
| `quiz[0].widget.accept` | 9, at $(3, 3)$. | correct | B36 |
| `quiz[0].widget.wrong[0]` | slip free = 36 | correct | B36 |
| `quiz[0].widget.wrong[1]` | slip off = 8 | correct | B36 |
| `quiz[0].feedback.correct` | 9, at $(3, 3)$. | correct | B36 |
| `quiz[0].feedback.generic` | Not quite right. The conditions give $x = y$; then use $x + y = 6$. | correct | B36 |
| `quiz[0].feedback.byKey.free` | $x = y = 6$ is off the line. On $x + y = 6$ the conditions give $x = y = 3$. | correct | B36 |
| `quiz[0].feedback.byKey.off` | $(2, 4)$ gives 8, but $(3, 3)$ does better. | correct | B36 |
| `quiz[0].explain.text` | $\nabla f = (y, x) = \lambda (1, 1)$ gives $x = y$. With $x + y = 6$ that is $(3, 3)$, so the maximum is 9. | correct | B36 |
| `quiz[1].prose` | P is the largest value of $f$ on the curve $g(x, y) = c$, and $\nabla g \neq \mathbf{0}$ at P. | imprecise | finding 6: "P is the largest value" but P is then used as the point; and the rule also needs f and g smooth |
| `quiz[1].question` | What must be true at P? | correct | B36 |
| `quiz[1].widget.options[0]` | option par (key): $\nabla f$ is parallel to $\nabla g$ | correct | B36 |
| `quiz[1].widget.options[1]` | option zero: $\nabla f = \mathbf{0}$ | correct | B36 |
| `quiz[1].widget.options[1].why` | That is the condition without a constraint. On a curve, $\nabla f$ can be large as long as it points across the curve. | correct | B36 |
| `quiz[1].widget.options[2]` | option perp: $\nabla f$ is perpendicular to $\nabla g$ | correct | B36 |
| `quiz[1].widget.options[2].why` | Then $\nabla f$ would point along the curve, and sliding along it would raise $f$. | correct | B36 |
| `quiz[1].widget.options[3]` | option fg: $f = g$ at P | correct | B36 |
| `quiz[1].widget.options[3].why` | $f$ and $g$ measure different things. The condition is on their gradients. | correct | B36 |
| `quiz[1].feedback.correct` | $\nabla f = \lambda \nabla g$. | correct | B36 |
| `quiz[1].feedback.generic` | Not quite right. Think about which way $\nabla f$ must point at the best point. | correct | B36 |
| `quiz[1].explain.text` | If $\nabla f$ had any part along the curve, moving that way would raise $f$. So at the best point it points straight across the curve, like $\nabla... | correct | B36 |
| `quiz[2].prose` | Minimise $x^2 + y^2$ on the line $x + y = 4$. | correct | B36 |
| `quiz[2].question` | What is the smallest value? | correct | B36 |
| `quiz[2].widget.answer` | 8 | correct | B36 |
| `quiz[2].widget.accept` | 8, at $(2, 2)$. | correct | B36 |
| `quiz[2].widget.wrong[0]` | slip end = 16 | correct | B36 |
| `quiz[2].widget.wrong[1]` | slip dist = 2.83 | correct | B36 |
| `quiz[2].feedback.correct` | 8, at $(2, 2)$. | correct | B36 |
| `quiz[2].feedback.generic` | Not quite right. $(2x, 2y) = \lambda(1, 1)$ gives $x = y$. | correct | B36 |
| `quiz[2].feedback.byKey.end` | $(4, 0)$ gives 16, but $(2, 2)$ is lower. | correct | B36 |
| `quiz[2].feedback.byKey.dist` | That is the distance $\sqrt{8}$. The question asks for $x^2 + y^2$ itself. | correct | B36 |
| `quiz[2].explain.text` | $2x = \lambda$ and $2y = \lambda$ give $x = y = 2$, so the minimum is $4 + 4 = 8$. It is the squared distance from the origin to the line. | correct | B36 |
| `quiz[3].prose` | The fund from the lesson made £25k at risk limit 25, with $\lambda = 0.5$. The limit rises to 27. | correct | B36 |
| `quiz[3].question` | Estimate the new largest expected profit, in £k. | correct | B36 |
| `quiz[3].widget.answer` | 26 | correct | B36 |
| `quiz[3].widget.accept` | 26, from $25 + 0.5 \times 2$; exactly $5\sqrt{27} \approx 25.98$. | correct | B36 |
| `quiz[3].widget.wrong[0]` | slip budget = 27 | correct | B36 |
| `quiz[3].widget.wrong[1]` | slip same = 25 | correct | B36 |
| `quiz[3].feedback.correct` | About £26k. | correct | B36 |
| `quiz[3].feedback.generic` | Not quite right. Add $\lambda$ times the rise in the limit. | correct | B36 |
| `quiz[3].feedback.byKey.budget` | You added the whole rise of 2. Each unit is worth $\lambda = 0.5$, so the gain is about 1. | correct | B36 |
| `quiz[3].feedback.byKey.same` | A looser limit lets the fund reach a higher contour. | correct | B36 |
| `quiz[3].explain.text` | The limit rises by 2 and each unit is worth $\lambda = 0.5$, so profit rises by about 1, to £26k. The exact best is $5\sqrt{27} \approx 25.98$. | correct | B36 |

## l12-min-variance

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `objectives[0]` | Find the minimum variance two-asset portfolio with a Lagrange multiplier. | correct | B37 |
| `objectives[1]` | Check the answer by substitution and see how correlation moves it. | correct | B37 |
| `screens[0].prose` | Asset A has volatility 20% and asset B 10%. Their returns have correlation 0.3. You put a fraction $w_1$ of your money in A and the rest in B. The ... | correct | B37 |
| `screens[0].question` | Set $w_1$ to the mix with the lowest volatility. | correct | B37 |
| `screens[0].widget.answer` | 0.105 | correct | B37 |
| `screens[0].hints[0]` | Watch the volatility in the caption as you slide towards 0. | correct | B37 |
| `screens[0].hints[1]` | Near $w_1 = 0$ the curve dips just below the B-alone line. | correct | B37 |
| `screens[0].hints[2]` | The lowest volatility, 9.79%, comes at about 10.5% in A. | correct | B37 |
| `screens[0].feedback.correct` | About 10.5% in A, for a volatility of 9.79%. | correct | B37 |
| `screens[0].feedback.generic` | Not quite right. Slide towards 0 and watch for the lowest volatility in the caption. | correct | B37 |
| `screens[0].feedback.byKey.all-b` | You put everything, or nearly everything, in B. A little of A lowers the risk: at 10.5% in A it is 9.79%. | correct | B37 |
| `screens[0].feedback.byKey.half` | Half and half gives 12.45%. The risk keeps falling as you move towards B, until about 10.5% in A. | correct | B37 |
| `screens[0].feedback.byKey.all-a` | A alone has 20% volatility, the riskiest choice here. | correct | B37 |
| `screens[0].explain.text` | You found the lowest point at about 10.5% in A, with volatility 9.79%. That is below B alone, though A is twice as volatile. Because the two do not... | correct | B37 |
| `screens[1].prose` | Same two assets, but now you set the correlation $\rho$. The marked point is the lowest point of the curve with $w_1$ between 0 and 1. | correct | B37 |
| `screens[1].question` | Set $\rho = -1$. What is the lowest volatility you can reach? | correct | B37 |
| `screens[1].widget.answer` | 0 | correct | B37 |
| `screens[1].widget.accept` | 0%, with a third of the money in A. | correct | B37 |
| `screens[1].widget.wrong[0]` | slip b = 0.1 | correct | B37 |
| `screens[1].widget.wrong[1]` | slip base = 0.0979 | correct | B37 |
| `screens[1].hints[0]` | Drag the $\rho$ slider all the way to the left. | correct | B37 |
| `screens[1].hints[1]` | Watch where the marked point lands. | correct | B37 |
| `screens[1].feedback.correct` | Zero: the two assets cancel exactly. | correct | B37 |
| `screens[1].feedback.generic` | Not quite right. Set $\rho = -1$ and read the caption. | correct | B37 |
| `screens[1].feedback.byKey.b` | That is B alone. With $\rho = -1$ the curve drops all the way to the axis. | correct | B37 |
| `screens[1].feedback.byKey.base` | That is the lowest point at $\rho = 0.3$. Move the slider to $-1$ first. | correct | B37 |
| `screens[1].explain.text` | At $\rho = -1$ the assets move exactly opposite. With a third in A, $\tfrac{1}{3} \times 20\% = \tfrac{2}{3} \times 10\%$, so their swings cancel a... | correct | B37 |
| `screens[2].prose` | The least risky mix is the **minimum variance portfolio**. The variance is $$\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\rho\sigma_1\s... | correct | B37 |
| `screens[2].question` | What is the coefficient $a$? | correct | B37 |
| `screens[2].widget.answer` | 0.038 | correct | B37 |
| `screens[2].widget.accept` | 0.038, from $0.04 + 0.01 - 0.012$. | correct | B37 |
| `screens[2].widget.wrong[0]` | slip nocross = 0.05 | correct | B37 |
| `screens[2].widget.wrong[1]` | slip sign = 0.062 | correct | B37 |
| `screens[2].widget.wrong[2]` | slip first = 0.04 | correct | B37 |
| `screens[2].hints[0]` | Collect the $w_1^2$ terms from all three parts. | correct | B37 |
| `screens[2].hints[1]` | $(1 - w_1)^2$ gives $+w_1^2$, and $w_1(1 - w_1)$ gives $-w_1^2$. | correct | B37 |
| `screens[2].hints[2]` | $0.04 + 0.01 - 2(0.3)(0.2)(0.1) = 0.04 + 0.01 - 0.012 = 0.038$. | correct | B37 |
| `screens[2].feedback.correct` | $a = 0.038$. | correct | B37 |
| `screens[2].feedback.generic` | Not quite right. Each of the three terms contributes to $w_1^2$. | correct | B37 |
| `screens[2].feedback.byKey.nocross` | You took $0.04 + 0.01$ but left out the cross term. $2w_1(1 - w_1)(0.006)$ contributes $-0.012w_1^2$. | correct | B37 |
| `screens[2].feedback.byKey.sign` | The cross term gives $-0.012w_1^2$, not $+0.012w_1^2$: $w_1(1 - w_1) = w_1 - w_1^2$. | correct | B37 |
| `screens[2].feedback.byKey.first` | $(1 - w_1)^2\sigma_2^2$ also contributes $0.01w_1^2$, and the cross term $-0.012w_1^2$. | correct | B37 |
| `screens[2].explain.text` | Expanding gives $0.04w_1^2 + 0.01(1 - 2w_1 + w_1^2) + 0.012(w_1 - w_1^2)$. Collecting terms: $\sigma_p^2 = 0.038w_1^2 - 0.008w_1 + 0.01$. A parabol... | correct | B37 |
| `screens[3].prose` | So $\sigma_p^2 = 0.038w_1^2 - 0.008w_1 + 0.01$. Its lowest point is where the derivative is zero. | correct | B37 |
| `screens[3].question` | Solve $\dfrac{d\sigma_p^2}{dw_1} = 0$. What is $w_1$? Give four decimal places. | correct | B37 |
| `screens[3].widget.answer` | 0.10526 | correct | B37 |
| `screens[3].widget.accept` | $\tfrac{0.008}{0.076} = 0.1053$, about 10.5% in A. | correct | B37 |
| `screens[3].widget.wrong[0]` | slip notwo = 0.2105 | correct | B37 |
| `screens[3].widget.wrong[1]` | slip zero = 0 | correct | B37 |
| `screens[3].widget.wrong[2]` | slip ratio = 0.25 | correct | B37 |
| `screens[3].hints[0]` | Differentiate: $\tfrac{d}{dw_1}(aw_1^2 + bw_1 + c) = 2aw_1 + b$. | correct | B37 |
| `screens[3].hints[1]` | Drag the point until the tangent is flat. | correct | B37 |
| `screens[3].hints[2]` | $0.076w_1 - 0.008 = 0$ gives $w_1 = 0.008 / 0.076 = 0.1053$. | correct | B37 |
| `screens[3].feedback.correct` | $w_1 = 0.1053$. | correct | B37 |
| `screens[3].feedback.generic` | Not quite right. Solve $0.076w_1 - 0.008 = 0$. | correct | B37 |
| `screens[3].feedback.byKey.notwo` | You solved $0.038w_1 = 0.008$. The derivative of $0.038w_1^2$ is $0.076w_1$. | correct | B37 |
| `screens[3].feedback.byKey.zero` | At $w_1 = 0$ the slope is $-0.008$, so the variance still falls as you add A. | correct | B37 |
| `screens[3].feedback.byKey.ratio` | That is $\sigma_2^2 / \sigma_1^2$, which ignores the correlation. Solve the derivative instead. | correct | B37 |
| `screens[3].explain.text` | The derivative $0.076w_1 - 0.008$ is zero at $w_1 = 0.10526$. There $\sigma_p^2 = 0.0095789$, so $\sigma_p = 0.09787$: 9.79%. The tangent is flat a... | correct | B37 |
| `screens[4].prose` | Treat $w_1$ and $w_2$ as free, with the budget $w_1 + w_2 = 1$ as a constraint. The ellipses are contours of $\sigma_p^2$. Here $$\nabla \sigma_p^2... | correct | B37 |
| `screens[4].question` | Solve $\nabla \sigma_p^2 = \lambda (1, 1)$ with $w_1 + w_2 = 1$. What is $w_2$? Give four decimal places. | correct | B37 |
| `screens[4].widget.answer` | 0.89474 | correct | B37 |
| `screens[4].widget.accept` | $w_2 = 8.5w_1$, so $w_2 = 8.5 / 9.5 = 0.8947$. | correct | B37 |
| `screens[4].widget.wrong[0]` | slip w1 = 0.10526 | correct | B37 |
| `screens[4].widget.wrong[1]` | slip half = 0.5 | correct | B37 |
| `screens[4].widget.wrong[2]` | slip ratio = 8.5 | correct | B37 |
| `screens[4].hints[0]` | Both components equal $\lambda$, so set them equal to each other. | correct | B37 |
| `screens[4].hints[1]` | $0.08w_1 + 0.012w_2 = 0.02w_2 + 0.012w_1$ gives $0.068w_1 = 0.008w_2$. | correct | B37 |
| `screens[4].hints[2]` | So $w_2 = 8.5w_1$. With $w_1 + w_2 = 1$: $9.5w_1 = 1$, $w_1 = 0.1053$, $w_2 = 0.8947$. | correct | B37 |
| `screens[4].feedback.correct` | $w_2 = 0.8947$, so $w_1 = 0.1053$ as before. | correct | B37 |
| `screens[4].feedback.generic` | Not quite right. Equate the two components, then use $w_1 + w_2 = 1$. | correct | B37 |
| `screens[4].feedback.byKey.w1` | That is $w_1$, the weight in A. The question asks for $w_2$, the weight in B. | correct | B37 |
| `screens[4].feedback.byKey.half` | Equal weights ignore the gradient equations. They give $w_2 = 8.5w_1$. | correct | B37 |
| `screens[4].feedback.byKey.ratio` | 8.5 is the ratio $w_2 / w_1$. Use the budget $w_1 + w_2 = 1$ to turn it into weights. | correct | B37 |
| `screens[4].explain.text` | Equating the components gave $w_2 = 8.5w_1$, and the budget gave $w_1 = 0.1053$, $w_2 = 0.8947$: the same as substitution. The purple ellipse touch... | correct | B37 |
| `screens[5].prose` | Now let $\rho = 1$, with no short sales, so $0 \le w_1 \le 1$. Then $\sigma_p = w_1\sigma_1 + w_2\sigma_2$ exactly: a straight line from 10% to 20%. | correct | B37 |
| `screens[5].question` | Which mix has the lowest volatility? | correct | B37 |
| `screens[5].widget.options[0]` | option corner (key): All in B, $w_1 = 0$ | correct | B37 |
| `screens[5].widget.options[1]` | option formula: $w_1 = -1$, from the formula | correct | B37 |
| `screens[5].widget.options[1].why` | The formula gives $(0.01 - 0.02)/(0.04 + 0.01 - 0.04) = -1$: a short sale of A. With $0 \le w_1 \le 1$, the line's lowest point is its end. | correct | B37 |
| `screens[5].widget.options[2]` | option half: Half in each | correct | B37 |
| `screens[5].widget.options[2].why` | On a straight line there is no dip in the middle. Half in each gives 15%. | correct | B37 |
| `screens[5].widget.options[3]` | option same: Every mix is equally risky | correct | B37 |
| `screens[5].widget.options[3].why` | The volatility still changes with the mix: it climbs from 10% to 20% along the line. | correct | B37 |
| `screens[5].hints[0]` | Where is a rising straight line lowest? | correct | B37 |
| `screens[5].hints[1]` | The line starts at B alone. | correct | B37 |
| `screens[5].hints[2]` | With $\rho = 1$ there is no dip: the lowest volatility, 10%, is at $w_1 = 0$. | correct | B37 |
| `screens[5].feedback.correct` | All in B: with $\rho = 1$ mixing gives no benefit. | correct | B37 |
| `screens[5].feedback.generic` | Not quite right. With $\rho = 1$ the volatility is a straight line in $w_1$. | correct | B37 |
| `screens[5].explain.text` | With $\rho = 1$ the assets move in lockstep, so mixing only averages their volatilities. The best long-only mix is a corner, all in B. With short s... | correct | B37 |
| `screens[6].prose` | Asset A has volatility 30% and asset B 15%, uncorrelated. A colleague says the safest portfolio is all in B, the calmer asset. | correct | B37 |
| `screens[6].question` | What is the lowest volatility you can reach? | correct | B37 |
| `screens[6].widget.options[0]` | option right (key): 13.4%, with 20% in A | correct | B37 |
| `screens[6].widget.options[1]` | option allb: 15%, all in B | correct | B37 |
| `screens[6].widget.options[1].why` | You held only the calmer asset. With $\rho = 0$, adding some A lowers the risk: 20% in A gives 13.4%. | correct | B37 |
| `screens[6].widget.options[2]` | option zero: 0%, with a third in A | correct | B37 |
| `screens[6].widget.options[2].why` | Zero risk needs $\rho = -1$, or $\rho = 1$ with a short sale. Uncorrelated assets cannot cancel exactly. | correct | B37 |
| `screens[6].widget.options[3]` | option avg: 22.5%, half in each | correct | B37 |
| `screens[6].widget.options[3].why` | You averaged the volatilities. Half and half gives $\sqrt{0.25 \times 0.09 + 0.25 \times 0.0225} = 16.8\%$, and less A does better. | correct | B37 |
| `screens[6].hints[0]` | Use $w_1^* = \dfrac{\sigma_2^2 - \rho\sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2}$ with $\rho = 0$. | correct | B37 |
| `screens[6].hints[1]` | $w_1^* = 0.0225 / (0.09 + 0.0225) = 0.2$. | correct | B37 |
| `screens[6].hints[2]` | $\sigma_p^2 = 0.04 \times 0.09 + 0.64 \times 0.0225 = 0.018$, so $\sigma_p = 0.134$. | correct | B37 |
| `screens[6].feedback.correct` | 13.4%, below B's 15%. | correct | B37 |
| `screens[6].feedback.generic` | Not quite right. Find $w_1^*$ with $\rho = 0$, then the volatility there. | correct | B37 |
| `screens[6].feedback.byKey.allb` | You assumed the least risky asset is the least risky portfolio. Unless $\rho$ is high, a slice of the riskier asset diversifies. | correct | B37 |
| `screens[6].explain.text` | With $\rho = 0$, $w_1^* = 0.0225 / 0.1125 = 0.2$ and $\sigma_p^2 = 0.0036 + 0.0144 = 0.018$, so $\sigma_p = 13.4\%$. The curve dips below B alone. ... | correct | B37 |
| `screens[7].prose` | Solving either way, for any $\sigma_1$, $\sigma_2$ and $\rho$: $$w_1^* = \frac{\sigma_2^2 - \rho\sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\rho\s... | correct | B37 |
| `screens[7].question` | Check it on the first pair: $\sigma_1 = 0.2$, $\sigma_2 = 0.1$, $\rho = 0.3$. What is the numerator? | correct | B37 |
| `screens[7].widget.answer` | 0.004 | correct | B37 |
| `screens[7].widget.accept` | $0.01 - 0.006 = 0.004$; then $0.004 / 0.038 = 0.1053$. | correct | B37 |
| `screens[7].widget.wrong[0]` | slip s1 = 0.034 | correct | B37 |
| `screens[7].widget.wrong[1]` | slip nor = 0.01 | correct | B37 |
| `screens[7].hints[0]` | $\sigma_2^2 = 0.01$ and $\rho\sigma_1\sigma_2 = 0.3 \times 0.2 \times 0.1$. | correct | B37 |
| `screens[7].feedback.correct` | $0.004 / 0.038 = 0.1053$, as before. | correct | B37 |
| `screens[7].feedback.generic` | Not quite right. Compute $0.1^2 - 0.3 \times 0.2 \times 0.1$. | correct | B37 |
| `screens[7].feedback.byKey.s1` | You used $\sigma_1^2 = 0.04$. The numerator for $w_1$ uses the other asset's variance, $\sigma_2^2$. | correct | B37 |
| `screens[7].feedback.byKey.nor` | You left out $-\rho\sigma_1\sigma_2 = -0.006$. | correct | B37 |
| `screens[7].explain.text` | The numerator is $0.01 - 0.006 = 0.004$ and the denominator $0.038$, so $w_1^* = 0.1053$. Notice the numerator uses the *other* asset's variance: t... | correct | B37 |
| `screens[8].prose` | We minimise $\sigma_p^2$ over $w_1$, with $w_2 = 1 - w_1$. Write $\sigma_1, \sigma_2, \rho$ as letters throughout. | correct | B37 |
| `screens[8].question` | Put the lines of the derivation in order. | correct | B37 |
| `screens[8].widget.lines[0]` | line sub: $\sigma_p^2 = w_1^2\sigma_1^2 + (1 - w_1)^2\sigma_2^2 + 2w_1(1 - w_1)\rho\sigma_1\sigma_2$, substitute $w_2 = 1 - w_1$ | correct | B37 |
| `screens[8].widget.lines[1]` | line diff: $\dfrac{d\sigma_p^2}{dw_1} = 2w_1\sigma_1^2 - 2(1 - w_1)\sigma_2^2 + 2(1 - 2w_1)\rho\sigma_1\sigma_2$, chain rule and product rule | correct | B37 |
| `screens[8].widget.lines[2]` | line zero: $0 = w_1\sigma_1^2 - \sigma_2^2 + w_1\sigma_2^2 + \rho\sigma_1\sigma_2 - 2w_1\rho\sigma_1\sigma_2$, set it to zero, halve and expand | correct | B37 |
| `screens[8].widget.lines[3]` | line collect: $w_1(\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2) = \sigma_2^2 - \rho\sigma_1\sigma_2$, collect the $w_1$ terms | correct | B37 |
| `screens[8].widget.lines[4]` | line divide: $w_1^* = \dfrac{\sigma_2^2 - \rho\sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2}$, divide; the bracket is $\text{Va... | correct | B37 |
| `screens[8].widget.answer` | sub, diff, zero, collect, divide | correct | B37 |
| `screens[8].hints[0]` | Substitute first, then differentiate. | correct | B37 |
| `screens[8].hints[1]` | Collecting the $w_1$ terms needs the expanded equation. | correct | B37 |
| `screens[8].hints[2]` | Substitute, differentiate, set to zero and expand, collect, divide. | correct | B37 |
| `screens[8].feedback.correct` | The formula, from one derivative. | correct | B37 |
| `screens[8].feedback.generic` | Not quite right. You must substitute $w_2 = 1 - w_1$ before differentiating in $w_1$. | correct | B37 |
| `screens[8].feedback.byKey.collect` | Collecting needs the expanded form, so the zero line comes first. | correct | B37 |
| `screens[8].feedback.byKey.divide` | Dividing is the last step, once all $w_1$ terms are on one side. | correct | B37 |
| `screens[8].explain.text` | One derivative, set to zero, gives a linear equation in $w_1$. The bracket we divide by is $\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2$, the v... | correct | B37 |
| `screens[9].prose` | A fund holds two equity books: A with volatility 15%, B with 25%, correlation 0.8. The formula gives $w_1^* = 1.3$: 130% in A and −30% in B. The fu... | correct | B37 |
| `screens[9].question` | Which weight $w_1$ should the fund hold? | correct | B37 |
| `screens[9].widget.answer` | 1 | correct | B37 |
| `screens[9].widget.accept` | 1: all in A, the allowed weight nearest 1.3. | correct | B37 |
| `screens[9].widget.wrong[0]` | slip ignore = 1.3 | correct | B37 |
| `screens[9].widget.wrong[1]` | slip zero = 0 | correct | B37 |
| `screens[9].widget.wrong[2]` | slip half = 0.5 | correct | B37 |
| `screens[9].hints[0]` | The allowed weights lie between the two dashed lines. | correct | B37 |
| `screens[9].hints[1]` | Between 0 and 1, the curve falls all the way to the right-hand line. | correct | B37 |
| `screens[9].hints[2]` | The variance is a parabola with its lowest point at 1.3. On $[0, 1]$ it is lowest at the end nearest 1.3: $w_1 = 1$. | correct | B37 |
| `screens[9].feedback.correct` | All in A, with volatility 15%. | correct | B37 |
| `screens[9].feedback.generic` | Not quite right. Find the lowest point of the curve between 0 and 1. | correct | B37 |
| `screens[9].feedback.byKey.ignore` | 1.3 breaks the mandate: it needs a short position of 30% in B. | correct | B37 |
| `screens[9].feedback.byKey.zero` | All in B is the riskiest allowed choice here, at 25%. | correct | B37 |
| `screens[9].feedback.byKey.half` | Half in each gives about 19%. The curve keeps falling towards $w_1 = 1$. | correct | B37 |
| `screens[9].explain.text` | The variance is a parabola in $w_1$ with its lowest point at 1.3. Restricted to $[0, 1]$, it is lowest at $w_1 = 1$: all in A, volatility 15%. Clip... | correct | B37 |
| `summary.ideas[0]` | With $w_2 = 1 - w_1$ the portfolio variance is a parabola in $w_1$. Its lowest point is the minimum variance portfolio. | correct | B37 |
| `summary.ideas[1]` | A multiplier on $w_1 + w_2 = 1$ gives the same weights, with $\lambda = 2\sigma_p^2$ at the minimum. | correct | B37 |
| `summary.ideas[2]` | Lower correlation means a deeper dip: at $\rho = -1$ risk can reach zero, at $\rho = 1$ there is no dip. A ban on short sales clips $w_1$ to $[0, 1]$. | correct | B37 |
| `summary.formula.name` | Minimum variance weight | correct | B37 |
| `summary.formula.tex` | w_1^* = \dfrac{\sigma_2^2 - \rho\sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2} | correct | B37 |
| `summary.formula.note` | The bottom is $\text{Var}(R_1 - R_2) > 0$. For 20%, 10% and $\rho = 0.3$: $w_1^* = 0.1053$, $\sigma_p = 9.79\%$. | correct | B37 |
| `summary.trap` | The least volatile asset alone is not the least volatile portfolio. Unless correlation is high, a slice of the riskier asset lowers risk. | correct | B37 |
| `quiz[0].prose` | Two assets both have volatility 20%, with correlation 0.5. | correct | B37 |
| `quiz[0].question` | What weight $w_1$ gives the minimum variance portfolio? | correct | B37 |
| `quiz[0].widget.answer` | 0.5 | correct | B37 |
| `quiz[0].widget.accept` | 0.5, by symmetry or from the formula. | correct | B37 |
| `quiz[0].widget.wrong[0]` | slip zero = 0 | correct | B37 |
| `quiz[0].widget.wrong[1]` | slip one = 1 | correct | B37 |
| `quiz[0].feedback.correct` | Half in each. | correct | B37 |
| `quiz[0].feedback.generic` | Not quite right. With equal volatilities the formula's top is half its bottom. | correct | B37 |
| `quiz[0].feedback.byKey.zero` | Neither asset is calmer, so neither corner wins. Splitting evenly diversifies. | correct | B37 |
| `quiz[0].feedback.byKey.one` | Neither asset is calmer, so neither corner wins. Splitting evenly diversifies. | correct | B37 |
| `quiz[0].explain.text` | $w_1^* = (0.04 - 0.02)/(0.04 + 0.04 - 0.04) = 0.02/0.04 = 0.5$. Identical volatilities make the assets interchangeable, so the best split is even. | correct | B37 |
| `quiz[1].prose` | Asset A has volatility 20% and B 10%, with correlation $-1$. | correct | B37 |
| `quiz[1].question` | Which weight in A makes the portfolio riskless? | correct | B37 |
| `quiz[1].widget.options[0]` | option third (key): $w_1 = \tfrac{1}{3}$ | correct | B37 |
| `quiz[1].widget.options[1]` | option half: $w_1 = \tfrac{1}{2}$ | correct | B37 |
| `quiz[1].widget.options[1].why` | Half and half leaves A's larger swings uncancelled: $0.5 \times 20\% - 0.5 \times 10\% = 5\%$. | correct | B37 |
| `quiz[1].widget.options[2]` | option twothirds: $w_1 = \tfrac{2}{3}$ | correct | B37 |
| `quiz[1].widget.options[2].why` | You gave the larger weight to the riskier asset. A needs the smaller weight. | correct | B37 |
| `quiz[1].widget.options[3]` | option none: No mix is riskless | correct | B37 |
| `quiz[1].widget.options[3].why` | With $\rho = -1$ the swings can cancel exactly. | correct | B37 |
| `quiz[1].feedback.correct` | $\tfrac{1}{3} \times 20\% = \tfrac{2}{3} \times 10\%$. | correct | B37 |
| `quiz[1].feedback.generic` | Not quite right. With $\rho = -1$, $\sigma_p = \|w_1\sigma_1 - w_2\sigma_2\|$. | correct | B37 |
| `quiz[1].explain.text` | With $\rho = -1$, $\sigma_p = \|0.2w_1 - 0.1(1 - w_1)\|$, which is zero when $0.3w_1 = 0.1$. So $w_1 = \tfrac{1}{3}$, matching the formula: $0.03 /... | correct | B37 |
| `quiz[2].prose` | Take $\sigma_1 = 0.2$, $\sigma_2 = 0.1$, $\rho = 0.3$ again. | correct | B37 |
| `quiz[2].question` | What is $\sigma_p^2$ for half in each asset? | correct | B37 |
| `quiz[2].widget.answer` | 0.0155 | correct | B37 |
| `quiz[2].widget.accept` | 0.0155, from $0.01 + 0.0025 + 0.003$. | correct | B37 |
| `quiz[2].widget.wrong[0]` | slip nocross = 0.0125 | correct | B37 |
| `quiz[2].widget.wrong[1]` | slip avg = 0.025 | correct | B37 |
| `quiz[2].feedback.correct` | 0.0155, a volatility of 12.45%. | correct | B37 |
| `quiz[2].feedback.generic` | Not quite right. Each weight is 0.5, so each squared weight is 0.25. | correct | B37 |
| `quiz[2].feedback.byKey.nocross` | You dropped the covariance term, $2 \times 0.25 \times 0.006 = 0.003$. | correct | B37 |
| `quiz[2].feedback.byKey.avg` | You averaged the variances. The weights enter squared: $0.25 \times 0.04 + 0.25 \times 0.01 + 0.003$. | correct | B37 |
| `quiz[2].explain.text` | $0.25 \times 0.04 + 0.25 \times 0.01 + 2 \times 0.25 \times 0.006 = 0.01 + 0.0025 + 0.003 = 0.0155$. That is above the minimum, 0.0096. | correct | B37 |
| `quiz[3].prose` | Two assets, no short sales. B is the less volatile of the two. | correct | B37 |
| `quiz[3].question` | Which statement is always true? | correct | B37 |
| `quiz[3].widget.options[0]` | option right (key): The minimum variance portfolio is never riskier than B alone | correct | B37 |
| `quiz[3].widget.options[1]` | option allb: The minimum variance portfolio is all in B | correct | B37 |
| `quiz[3].widget.options[1].why` | Only when $\rho \ge \sigma_B / \sigma_A$. Otherwise some A lowers the risk further. | correct | B37 |
| `quiz[3].widget.options[2]` | option zero: The minimum variance portfolio has zero risk | correct | B37 |
| `quiz[3].widget.options[2].why` | Zero risk needs $\rho = -1$. | correct | B37 |
| `quiz[3].widget.options[3]` | option half: The minimum variance portfolio holds more of A than of B | correct | B37 |
| `quiz[3].widget.options[3].why` | The calmer asset gets the larger weight: the numerator of $w_A$ uses $\sigma_B^2$. | correct | B37 |
| `quiz[3].feedback.correct` | All in B is one of the choices, so the best can only match or beat it. | correct | B37 |
| `quiz[3].feedback.generic` | Not quite right. Ask which choices the minimum is taken over. | correct | B37 |
| `quiz[3].explain.text` | All in B is an allowed portfolio, so the lowest variance over all allowed mixes is at most B's variance. It equals it when $\rho \ge \sigma_B / \si... | correct | B37 |

## review-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Take $f(x, y) = x^2 + 2y^2 - 4x + 4y$. | correct | B38 |
| `items[0].question` | Where is its stationary point? | correct | B38 |
| `items[0].widget.options[0]` | option right (key): $(2, -1)$ | correct | B38 |
| `items[0].widget.options[1]` | option signs: $(-2, 1)$ | correct | B38 |
| `items[0].widget.options[1].why` | You flipped both signs. $2x - 4 = 0$ gives $x = +2$. | correct | B38 |
| `items[0].widget.options[2]` | option coef: $(4, -4)$ | correct | B38 |
| `items[0].widget.options[2].why` | You dropped the coefficients: $f_x = 2x - 4$ and $f_y = 4y + 4$, not $x - 4$ and $y + 4$. | correct | B38 |
| `items[0].widget.options[3]` | option half: $(2, -2)$ | correct | B38 |
| `items[0].widget.options[3].why` | From $4y + 4 = 0$, $y = -1$. You divided 4 by 2 instead of by 4. | correct | B38 |
| `items[0].feedback.correct` | $2x - 4 = 0$ and $4y + 4 = 0$. | correct | B38 |
| `items[0].feedback.generic` | Not quite right. Set $f_x = 2x - 4$ and $f_y = 4y + 4$ to zero. | correct | B38 |
| `items[0].explain.text` | $f_x = 2x - 4 = 0$ gives $x = 2$, and $f_y = 4y + 4 = 0$ gives $y = -1$. Both must hold, so the point is $(2, -1)$. | correct | B38 |
| `items[1].prose` | The same $f = x^2 + 2y^2 - 4x + 4y$, at its stationary point $(2, -1)$. | correct | B38 |
| `items[1].question` | What kind of point is it? | correct | B38 |
| `items[1].widget.options[0]` | option pit (key): A pit | correct | B38 |
| `items[1].widget.options[1]` | option peak: A peak | correct | B38 |
| `items[1].widget.options[1].why` | $f_{xx} = 2 > 0$, so $f$ curves up along $x$. A peak needs $f_{xx} < 0$. | correct | B38 |
| `items[1].widget.options[2]` | option saddle: A saddle | correct | B38 |
| `items[1].widget.options[2].why` | A saddle needs $D < 0$. Here $D = 2 \times 4 - 0 = 8$. | correct | B38 |
| `items[1].widget.options[3]` | option none: No verdict | correct | B38 |
| `items[1].widget.options[3].why` | $D = 8$, not 0, so the test decides. | correct | B38 |
| `items[1].feedback.correct` | $D = 8 > 0$ and $f_{xx} = 2 > 0$. | correct | B38 |
| `items[1].feedback.generic` | Not quite right. Compute $D = f_{xx} f_{yy} - f_{xy}^2$. | correct | B38 |
| `items[1].explain.text` | $f_{xx} = 2$, $f_{yy} = 4$ and $f_{xy} = 0$, so $D = 8 > 0$ with $f_{xx} > 0$: a pit. Completing the square agrees: $f = (x - 2)^2 + 2(y + 1)^2 - 6$. | correct | B38 |
| `items[2].prose` | Take $f(x, y) = x^3 + y^3 - 3x - 12y$. | correct | B38 |
| `items[2].question` | How many stationary points does $f$ have? | correct | B38 |
| `items[2].widget.answer` | 4 | correct | B38 |
| `items[2].widget.accept` | 4: $x = \pm 1$ with $y = \pm 2$. | correct | B38 |
| `items[2].widget.wrong[0]` | slip two = 2 | correct | B38 |
| `items[2].widget.wrong[1]` | slip one = 1 | correct | B38 |
| `items[2].feedback.correct` | Four: every pairing of $x = \pm 1$ with $y = \pm 2$. | correct | B38 |
| `items[2].feedback.generic` | Not quite right. Solve $3x^2 - 3 = 0$ and $3y^2 - 12 = 0$ separately. | correct | B38 |
| `items[2].feedback.byKey.two` | Each equation has two roots, and any root for $x$ pairs with any root for $y$: $2 \times 2 = 4$. | correct | B38 |
| `items[2].feedback.byKey.one` | You took only the positive roots. $x^2 = 1$ and $y^2 = 4$ each have two. | correct | B38 |
| `items[2].explain.text` | $f_x = 3x^2 - 3 = 0$ gives $x = \pm 1$, and $f_y = 3y^2 - 12 = 0$ gives $y = \pm 2$. The equations do not share a variable, so all four pairs work. | correct | B38 |
| `items[3].prose` | The same $f = x^3 + y^3 - 3x - 12y$. Here $f_{xx} = 6x$, $f_{yy} = 6y$ and $f_{xy} = 0$. | correct | B38 |
| `items[3].question` | Which stationary point is a peak? | correct | B38 |
| `items[3].widget.options[0]` | option mm (key): $(-1, -2)$ | correct | B38 |
| `items[3].widget.options[1]` | option pp: $(1, 2)$ | correct | B38 |
| `items[3].widget.options[1].why` | There $f_{xx} = 6 > 0$ and $D = 72 > 0$: a pit. | correct | B38 |
| `items[3].widget.options[2]` | option pm: $(1, -2)$ | correct | B38 |
| `items[3].widget.options[2].why` | There $D = 6 \times (-12) = -72 < 0$: a saddle. | correct | B38 |
| `items[3].widget.options[3]` | option mp: $(-1, 2)$ | correct | B38 |
| `items[3].widget.options[3].why` | There $D = (-6)(12) = -72 < 0$: a saddle. | correct | B38 |
| `items[3].feedback.correct` | $D = 72 > 0$ and $f_{xx} = -6 < 0$. | correct | B38 |
| `items[3].feedback.generic` | Not quite right. A peak needs $D > 0$ and $f_{xx} < 0$. | correct | B38 |
| `items[3].explain.text` | At $(-1, -2)$, $f_{xx} = -6$ and $f_{yy} = -12$, so $D = 72 > 0$ with $f_{xx} < 0$: a peak. The mixed pairs have $D < 0$ and are saddles. | correct | B38 |
| `items[4].prose` | Maximise $f = xy$ on the line $2x + y = 12$. | correct | B38 |
| `items[4].question` | What is the largest value? | correct | B38 |
| `items[4].widget.answer` | 18 | correct | B38 |
| `items[4].widget.accept` | 18, at $(3, 6)$. | correct | B38 |
| `items[4].widget.wrong[0]` | slip equal = 16 | correct | B38 |
| `items[4].widget.wrong[1]` | slip free = 36 | correct | B38 |
| `items[4].feedback.correct` | 18, at $(3, 6)$. | correct | B38 |
| `items[4].feedback.generic` | Not quite right. $(y, x) = \lambda(2, 1)$ gives $y = 2x$. | correct | B38 |
| `items[4].feedback.byKey.equal` | You set $x = y$, as for $x + y = c$. Here $\nabla g = (2, 1)$, so $y = 2x$. | correct | B38 |
| `items[4].feedback.byKey.free` | $(6, 6)$ is off the line: $2 \times 6 + 6 = 18$, not 12. | correct | B38 |
| `items[4].explain.text` | $y = 2\lambda$ and $x = \lambda$ give $y = 2x$. Then $2x + 2x = 12$, so $x = 3$, $y = 6$, and the maximum is 18. | correct | B38 |
| `items[5].prose` | Maximise $f = 2x + y$ on the circle $x^2 + y^2 = 5$. | correct | B38 |
| `items[5].question` | What is the largest value? | correct | B38 |
| `items[5].widget.answer` | 5 | correct | B38 |
| `items[5].widget.accept` | 5, at $(2, 1)$. | correct | B38 |
| `items[5].widget.wrong[0]` | slip nolambda = 2.5 | correct | B38 |
| `items[5].widget.wrong[1]` | slip min = -5 | correct | B38 |
| `items[5].feedback.correct` | 5, at $(2, 1)$. | correct | B38 |
| `items[5].feedback.generic` | Not quite right. Solve $(2, 1) = \lambda(2x, 2y)$ with $x^2 + y^2 = 5$. | correct | B38 |
| `items[5].feedback.byKey.nolambda` | You set $\nabla f = \nabla g$ with no $\lambda$, giving $(1, 0.5)$. That point is not on the circle. | correct | B38 |
| `items[5].explain.text` | $2 = 2\lambda x$ and $1 = 2\lambda y$ give $x = 2y$. Then $5y^2 = 5$, so $y = \pm 1$. The larger value is $f(2, 1) = 5$. | correct | B38 |
| `items[6].prose` | Asset A has volatility 10% and asset B 20%, uncorrelated. | correct | B38 |
| `items[6].question` | What weight $w_1$ in A gives the minimum variance portfolio? | correct | B38 |
| `items[6].widget.answer` | 0.8 | correct | B38 |
| `items[6].widget.accept` | 0.8, from $0.04 / (0.01 + 0.04)$. | correct | B38 |
| `items[6].widget.wrong[0]` | slip swap = 0.2 | correct | B38 |
| `items[6].widget.wrong[1]` | slip half = 0.5 | correct | B38 |
| `items[6].widget.wrong[2]` | slip vol = 0.6667 | correct | B38 |
| `items[6].feedback.correct` | 80% in the calmer asset. | correct | B38 |
| `items[6].feedback.generic` | Not quite right. With $\rho = 0$, $w_1^* = \sigma_2^2 / (\sigma_1^2 + \sigma_2^2)$. | correct | B38 |
| `items[6].feedback.byKey.swap` | You used A's variance on top. The weight in A uses B's variance, $\sigma_2^2 = 0.04$. | correct | B38 |
| `items[6].feedback.byKey.half` | Equal weights ignore that A is calmer. | correct | B38 |
| `items[6].feedback.byKey.vol` | You used volatilities, not variances: $0.2 / 0.3$. Square them first. | correct | B38 |
| `items[6].explain.text` | With $\rho = 0$, $w_1^* = 0.04 / (0.01 + 0.04) = 0.8$. The calmer asset gets the larger share, in proportion to the other asset's variance. | correct | B38 |
| `items[7].prose` | Two assets both have volatility 20%, and are uncorrelated. You hold the minimum variance portfolio. | correct | B38 |
| `items[7].question` | What is its volatility? | correct | B38 |
| `items[7].widget.answer` | 0.1414 | correct | B38 |
| `items[7].widget.accept` | 14.14%, which is $0.2 / \sqrt{2}$. | correct | B38 |
| `items[7].widget.wrong[0]` | slip same = 0.2 | correct | B38 |
| `items[7].widget.wrong[1]` | slip halved = 0.1 | correct | B38 |
| `items[7].feedback.correct` | $0.2 / \sqrt{2} = 14.14\%$. | correct | B38 |
| `items[7].feedback.generic` | Not quite right. Find $\sigma_p^2$ at half in each, then take the square root. | correct | B38 |
| `items[7].feedback.byKey.same` | Mixing uncorrelated assets lowers risk. Half in each gives a variance of 0.02, not 0.04. | correct | B38 |
| `items[7].feedback.byKey.halved` | The weights enter squared: $0.25 \times 0.04 \times 2 = 0.02$, and $\sqrt{0.02} = 0.1414$. | correct | B38 |
| `items[7].explain.text` | The weights are $\tfrac{1}{2}$ each, so $\sigma_p^2 = 0.25 \times 0.04 + 0.25 \times 0.04 = 0.02$. The volatility is $\sqrt{0.02} = 0.1414$, or 14.... | correct | B38 |
| `items[8].prose` | Take $f = x^2 + kxy + y^2$, stationary at the origin for every $k$. | correct | B38 |
| `items[8].question` | For which $k$ is the origin a pit? | imprecise | finding 4: at k = +-2, f = (x +- y)^2 >= 0, so the origin is a lowest point, which l10 screen 7 calls a pit; the key is right only for a strict (isolated) pit. Monte Carlo note in concepts-r2 script |
| `items[8].widget.options[0]` | option right (key): $-2 < k < 2$ | correct | B38 |
| `items[8].widget.options[1]` | option all: Every $k$, since $f_{xx}$ and $f_{yy}$ are positive | correct | B38 |
| `items[8].widget.options[1].why` | You classified from the pure partials alone. With $k = 4$, $D = 4 - 16 < 0$: a saddle. | correct | B38 |
| `items[8].widget.options[2]` | option pos: $k > 0$ | correct | B38 |
| `items[8].widget.options[2].why` | The sign of $k$ does not matter, only its size: $D = 4 - k^2$. | correct | B38 |
| `items[8].widget.options[3]` | option below: $k < 2$ | correct | B38 |
| `items[8].widget.options[3].why` | $k = -4$ also gives $D = 4 - 16 < 0$. The bound applies to $\|k\|$. | correct | B38 |
| `items[8].feedback.correct` | $D = 4 - k^2 > 0$ exactly when $\|k\| < 2$. | imprecise | finding 4: at k = +-2, f = (x +- y)^2 >= 0, so the origin is a lowest point, which l10 screen 7 calls a pit; the key is right only for a strict (isolated) pit. Monte Carlo note in concepts-r2 script |
| `items[8].feedback.generic` | Not quite right. $f_{xy} = k$, so $D = 4 - k^2$. | correct | B38 |
| `items[8].explain.text` | $f_{xx} = f_{yy} = 2$ and $f_{xy} = k$, so $D = 4 - k^2$. That is positive when $\|k\| < 2$, and then $f_{xx} > 0$ makes it a pit. At $\|k\| = 2$ t... | imprecise | finding 4: at k = +-2, f = (x +- y)^2 >= 0, so the origin is a lowest point, which l10 screen 7 calls a pit; the key is right only for a strict (isolated) pit. Monte Carlo note in concepts-r2 script |

## homework-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Take $f(x, y) = x^3 + y^3 - 3xy$. | correct | B39 |
| `items[0].question` | Write $D(x, y) = f_{xx} f_{yy} - f_{xy}^2$ as an expression in $x$ and $y$. | correct | B39 |
| `items[0].widget.answer` | 36xy-9 | correct | B39 |
| `items[0].widget.accept` | 36xy-9, 36*x*y-9, -9+36xy, 36yx-9, 9(4xy-1) | correct | B39 |
| `items[0].widget.wrong[0]` | slip plus = 36xy+9 | correct | B39 |
| `items[0].widget.wrong[1]` | slip nosq = 36xy+3 | correct | B39 |
| `items[0].widget.wrong[2]` | slip unsq = 36xy-3 | correct | B39 |
| `items[0].feedback.correct` | $D = 36xy - 9$. | correct | B39 |
| `items[0].feedback.generic` | Not quite right. Find $f_{xx} = 6x$, $f_{yy} = 6y$ and $f_{xy} = -3$ first. | correct | B39 |
| `items[0].feedback.byKey.plus` | $f_{xy}^2 = 9$ is subtracted, not added. | correct | B39 |
| `items[0].feedback.byKey.nosq` | You subtracted $f_{xy} = -3$ itself. The test uses its square, 9. | correct | B39 |
| `items[0].feedback.byKey.unsq` | You subtracted 3, not $(-3)^2 = 9$. | correct | B39 |
| `items[0].explain.text` | $f_x = 3x^2 - 3y$ and $f_y = 3y^2 - 3x$. So $f_{xx} = 6x$, $f_{yy} = 6y$, $f_{xy} = -3$, and $D = 36xy - 9$. | correct | B39 |
| `items[1].prose` | The same $f = x^3 + y^3 - 3xy$, with $f_x = 3x^2 - 3y$ and $f_y = 3y^2 - 3x$. | correct | B39 |
| `items[1].question` | Select all that apply: which are stationary points? | correct | B39 |
| `items[1].widget.options[0]` | option o (key): $(0, 0)$ | correct | B39 |
| `items[1].widget.options[1]` | option a (key): $(1, 1)$ | correct | B39 |
| `items[1].widget.options[2]` | option b: $(-1, 1)$ | correct | B39 |
| `items[1].widget.options[2].why` | There $f_x = 3 - 3 = 0$, but $f_y = 3 + 3 = 6$. Only one partial vanishes. | correct | B39 |
| `items[1].widget.options[3]` | option c: $(1, -1)$ | correct | B39 |
| `items[1].widget.options[3].why` | There $f_y = 3 - 3 = 0$, but $f_x = 3 + 3 = 6$. Only one partial vanishes. | correct | B39 |
| `items[1].widget.options[4]` | option d: $(-1, -1)$ | correct | B39 |
| `items[1].widget.options[4].why` | There $f_x = 3 + 3 = 6$. Substituting $y = x^2$ into $x = y^2$ gives $x = x^4$, whose real roots are 0 and 1. | correct | B39 |
| `items[1].feedback.correct` | $(0, 0)$ and $(1, 1)$. | correct | B39 |
| `items[1].feedback.generic` | Not quite right. From $f_x = 0$, $y = x^2$; from $f_y = 0$, $x = y^2$. | correct | B39 |
| `items[1].explain.text` | $f_x = 0$ gives $y = x^2$ and $f_y = 0$ gives $x = y^2$. So $x = x^4$, that is $x(x^3 - 1) = 0$, with real roots $x = 0$ and $x = 1$. The points ar... | correct | B39 |
| `items[2].prose` | Use $D = 36xy - 9$ for $f = x^3 + y^3 - 3xy$ at its stationary points $(0, 0)$ and $(1, 1)$. | correct | B39 |
| `items[2].question` | How are they classified? | correct | B39 |
| `items[2].widget.options[0]` | option right (key): $(0, 0)$ is a saddle and $(1, 1)$ is a pit | correct | B39 |
| `items[2].widget.options[1]` | option swap: $(0, 0)$ is a pit and $(1, 1)$ is a saddle | correct | B39 |
| `items[2].widget.options[1].why` | At the origin $D = -9 < 0$, a saddle. At $(1, 1)$, $D = 27 > 0$. | correct | B39 |
| `items[2].widget.options[2]` | option peak: $(0, 0)$ is a saddle and $(1, 1)$ is a peak | correct | B39 |
| `items[2].widget.options[2].why` | $D = 27 > 0$ at $(1, 1)$, but $f_{xx} = 6 > 0$, so it is a pit. | correct | B39 |
| `items[2].widget.options[3]` | option none: $(0, 0)$ gives no verdict, since $f_{xx} = f_{yy} = 0$ there | correct | B39 |
| `items[2].widget.options[3].why` | The test reads $D$, not the pure partials. $D = 0 - 9 = -9 \neq 0$. | correct | B39 |
| `items[2].feedback.correct` | $D(0, 0) = -9$ and $D(1, 1) = 27$ with $f_{xx} = 6$. | correct | B39 |
| `items[2].feedback.generic` | Not quite right. Evaluate $D$ at each point, then $f_{xx}$ where $D > 0$. | correct | B39 |
| `items[2].explain.text` | $D(0, 0) = -9 < 0$, so the origin is a saddle. $D(1, 1) = 27 > 0$ and $f_{xx}(1, 1) = 6 > 0$, so $(1, 1)$ is a pit, with $f = -1$. | correct | B39 |
| `items[3].prose` | Minimise $\sigma_p^2 = w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2w_1w_2\rho\sigma_1\sigma_2$ subject to $w_1 + w_2 = 1$, with a Lagrange multiplier. | correct | B39 |
| `items[3].question` | Put the lines of the derivation in order. | correct | B39 |
| `items[3].widget.lines[0]` | line c1: $2w_1\sigma_1^2 + 2w_2\rho\sigma_1\sigma_2 = \lambda$, the first component of $\nabla \sigma_p^2 = \lambda \nabla g$, with $\nabla g = (1,... | correct | B39 |
| `items[3].widget.lines[1]` | line c2: $2w_2\sigma_2^2 + 2w_1\rho\sigma_1\sigma_2 = \lambda$, the second component | correct | B39 |
| `items[3].widget.lines[2]` | line eq: $w_1(\sigma_1^2 - \rho\sigma_1\sigma_2) = w_2(\sigma_2^2 - \rho\sigma_1\sigma_2)$, equate the two expressions for $\lambda$ and halve | correct | B39 |
| `items[3].widget.lines[3]` | line con: $w_1(\sigma_1^2 - \rho\sigma_1\sigma_2) = (1 - w_1)(\sigma_2^2 - \rho\sigma_1\sigma_2)$, use the constraint $w_2 = 1 - w_1$ | correct | B39 |
| `items[3].widget.lines[4]` | line sol: $w_1 = \dfrac{\sigma_2^2 - \rho\sigma_1\sigma_2}{\sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2}$, collect the $w_1$ terms and divide | correct | B39 |
| `items[3].widget.answer` | c1, c2, eq, con, sol | correct | B39 |
| `items[3].feedback.correct` | The same formula as by substitution. | correct | B39 |
| `items[3].feedback.generic` | Not quite right. Both gradient equations come first; the constraint is used after $\lambda$ is eliminated. | correct | B39 |
| `items[3].feedback.byKey.eq` | Equating needs both component equations written first. | correct | B39 |
| `items[3].feedback.byKey.con` | Use the constraint after eliminating $\lambda$, so both weights are still visible. | correct | B39 |
| `items[3].feedback.byKey.sol` | Solving for $w_1$ is the last step. | correct | B39 |
| `items[3].explain.text` | Each component of $\nabla \sigma_p^2$ equals $\lambda$, so they equal each other, which removes $\lambda$. The constraint then leaves one equation ... | correct | B39 |
| `items[4].prose` | Minimise $f = x^2 + y^2$ on the line $x + 2y = 10$. | correct | B39 |
| `items[4].question` | What is the smallest value? | correct | B39 |
| `items[4].widget.answer` | 20 | correct | B39 |
| `items[4].widget.accept` | 20, at $(2, 4)$. | correct | B39 |
| `items[4].widget.wrong[0]` | slip equal = 22.2222 | correct | B39 |
| `items[4].widget.wrong[1]` | slip axis = 25 | correct | B39 |
| `items[4].widget.wrong[2]` | slip xaxis = 100 | correct | B39 |
| `items[4].feedback.correct` | 20, at $(2, 4)$. | correct | B39 |
| `items[4].feedback.generic` | Not quite right. $(2x, 2y) = \lambda(1, 2)$ gives $y = 2x$. | correct | B39 |
| `items[4].feedback.byKey.equal` | You set $x = y$. Here $\nabla g = (1, 2)$, so $y = 2x$. | correct | B39 |
| `items[4].feedback.byKey.axis` | $(0, 5)$ is on the line, but $(2, 4)$ is closer to the origin. | correct | B39 |
| `items[4].feedback.byKey.xaxis` | $(10, 0)$ is on the line, but far from the origin. | correct | B39 |
| `items[4].explain.text` | $2x = \lambda$ and $2y = 2\lambda$ give $y = 2x$. Then $x + 4x = 10$, so $(2, 4)$ and $f = 4 + 16 = 20$. It is the squared distance from the origin... | correct | B39 |
| `items[5].prose` | Asset A has volatility 25% and asset B 15%, with correlation 0.2. | correct | B39 |
| `items[5].question` | What weight $w_1$ in A gives the minimum variance portfolio? Give four decimal places. | correct | B39 |
| `items[5].widget.answer` | 0.21429 | correct | B39 |
| `items[5].widget.accept` | $0.015 / 0.07 = 0.2143$. | correct | B39 |
| `items[5].widget.wrong[0]` | slip norho = 0.26471 | correct | B39 |
| `items[5].widget.wrong[1]` | slip w2 = 0.78571 | correct | B39 |
| `items[5].feedback.correct` | $w_1 = 0.2143$, so 21.4% in A. | correct | B39 |
| `items[5].feedback.generic` | Not quite right. Numerator $0.0225 - 0.0075$; denominator $0.0625 + 0.0225 - 0.015$. | correct | B39 |
| `items[5].feedback.byKey.norho` | You left out the correlation terms. They take 0.0075 from the top and 0.015 from the bottom. | correct | B39 |
| `items[5].feedback.byKey.w2` | That is the weight in B. The formula's numerator uses B's variance to give A's weight. | correct | B39 |
| `items[5].explain.text` | $\rho\sigma_1\sigma_2 = 0.2 \times 0.25 \times 0.15 = 0.0075$. So $w_1^* = (0.0225 - 0.0075)/(0.0625 + 0.0225 - 0.015) = 0.015 / 0.07 = 0.2143$. | correct | B39 |
| `items[6].prose` | Take $f(x, y) = x^4 + y^4 - 4xy$. | correct | B39 |
| `items[6].question` | Select all that apply. | correct | B39 |
| `items[6].widget.options[0]` | option saddle (key): The origin is a saddle | correct | B39 |
| `items[6].widget.options[1]` | option pits (key): $(1, 1)$ and $(-1, -1)$ are pits | correct | B39 |
| `items[6].widget.options[2]` | option min (key): The smallest value of $f$ is $-2$ | correct | B39 |
| `items[6].widget.options[3]` | option mixed: $(1, -1)$ is a stationary point | correct | B39 |
| `items[6].widget.options[3].why` | There $f_x = 4 + 4 = 8$. From $y = x^3$ and $x = y^3$, $x = x^9$, so $x \in \{0, 1, -1\}$ with $y = x^3$. | correct | B39 |
| `items[6].widget.options[4]` | option silent: The test is silent at the origin, because $f_{xx} = 0$ there | correct | B39 |
| `items[6].widget.options[4].why` | The test reads $D = 0 \times 0 - (-4)^2 = -16$, which is not 0. | correct | B39 |
| `items[6].feedback.correct` | A saddle at the origin, two pits at $f = -2$. | correct | B39 |
| `items[6].feedback.generic` | Not quite right. Solve $x^3 = y$ and $y^3 = x$, then use $D = 144x^2y^2 - 16$. | correct | B39 |
| `items[6].explain.text` | $f_x = 4x^3 - 4y$ and $f_y = 4y^3 - 4x$ give $y = x^3$ and $x = x^9$: $(0, 0)$, $(1, 1)$, $(-1, -1)$. $D = 144x^2y^2 - 16$ is $-16$ at the origin (... | correct | B39 |
| `items[7].prose` | A fund maximises expected profit $3a + 4b$, in £k, subject to the risk limit $a^2 + b^2 = R$. For $R = 25$ the best is £25k, at $a = 3$, $b = 4$. | correct | B39 |
| `items[7].question` | Find the best expected profit, in £k, when the limit is $R = 36$. Work it out for general $R$ first. | correct | B39 |
| `items[7].widget.answer` | 30 | correct | B39 |
| `items[7].widget.accept` | 30: the best profit is $5\sqrt{R}$, and $5\sqrt{36} = 30$. | correct | B39 |
| `items[7].widget.wrong[0]` | slip linear = 36 | correct | B39 |
| `items[7].widget.wrong[1]` | slip lambda = 30.5 | correct | B39 |
| `items[7].widget.wrong[2]` | slip seven = 42 | correct | B39 |
| `items[7].widget.wrong[3]` | slip nosqrt = 180 | correct | B39 |
| `items[7].feedback.correct` | £30k: the best profit is $5\sqrt{R}$. | correct | B39 |
| `items[7].feedback.generic` | Not quite right. Solve $3 = 2\lambda a$, $4 = 2\lambda b$ with $a^2 + b^2 = R$, then substitute. | correct | B39 |
| `items[7].feedback.byKey.linear` | You scaled the profit with $R$ itself. Doubling the risk limit does not double the profit: the sizes grow like $\sqrt{R}$. | correct | B39 |
| `items[7].feedback.byKey.lambda` | You used $25 + \lambda \times 11 = 30.5$. That linear estimate drifts as $\lambda$ falls; solve exactly for general $R$. | correct | B39 |
| `items[7].feedback.byKey.seven` | You used $7\sqrt{R}$, adding the returns $3 + 4$. The best direction is $(3, 4)/5$, which gives $\sqrt{3^2 + 4^2} = 5$. | correct | B39 |
| `items[7].feedback.byKey.nosqrt` | $5R$ gives 125 at $R = 25$, not 25. The sizes grow like $\sqrt{R}$. | correct | B39 |
| `items[7].explain.text` | $a = \tfrac{3}{2\lambda}$ and $b = \tfrac{4}{2\lambda}$, so $a^2 + b^2 = \tfrac{25}{4\lambda^2} = R$ and $\lambda = \tfrac{5}{2\sqrt{R}}$. Profit $... | correct | B39 |
| `items[8].prompt` | Asset A has volatility 30% and asset B 20%, with correlation 0.4. (a) Use a Lagrange multiplier to find the minimum variance weights $w_1$ and $w_2... | correct | B39 |
| `items[8].model#1` | **(a) Lagrange.** With $\sigma_1^2 = 0.09$, $\sigma_2^2 = 0.04$ and $\rho\sigma_1\sigma_2 = 0.4 \times 0.3 \times 0.2 = 0.024$, | correct | B39 |
| `items[8].model#2` | $\nabla \sigma_p^2 = \lambda \nabla g$ gives two equations, since $\nabla g = (1, 1)$: | correct | B39 |
| `items[8].model#3` | Equating them: $0.132w_1 = 0.032w_2$, so $w_2 = 4.125w_1$. The constraint gives $5.125w_1 = 1$, so $w_1 = 0.1951$ and $w_2 = 0.8049$. | correct | B39 |
| `items[8].model#4` | **(b) Substitution.** With $w_2 = 1 - w_1$, | correct | B39 |
| `items[8].model#5` | The derivative $0.164w_1 - 0.032$ is zero at $w_1 = 0.032 / 0.164 = 0.1951$. The two methods agree. The formula agrees too: $(0.04 - 0.024) / (0.09... | correct | B39 |
| `items[8].model#6` | **(c) Risk and the multiplier.** $\sigma_p^2 = 0.04 - 0.032^2 / (4 \times 0.082) = 0.04 - 0.003122 = 0.036878$, so $\sigma_p = 0.1920$, or 19.20%. ... | correct | B39 |
| `items[8].model#7` | **(d) Changing the correlation.** At $\rho = -1$: $w_1 = (0.04 + 0.06) / (0.13 + 0.12) = 0.4$, and $\sigma_p = \|0.4 \times 0.3 - 0.6 \times 0.2\| ... | correct | B39 |
| `items[8].rubric[0]` | (1) Writes $\sigma_p^2$ with the covariance term $2 \times 0.024 = 0.048$ and the constraint $w_1 + w_2 = 1$. | correct | B39 |
| `items[8].rubric[1]` | (1) Writes both Lagrange equations, $0.18w_1 + 0.048w_2 = \lambda$ and $0.08w_2 + 0.048w_1 = \lambda$. | correct | B39 |
| `items[8].rubric[2]` | (1) Eliminates $\lambda$ to get $w_2 = 4.125w_1$ and solves $w_1 = 0.1951$, $w_2 = 0.8049$. | correct | B39 |
| `items[8].rubric[3]` | (1) Substitutes $w_2 = 1 - w_1$ and expands to $0.082w_1^2 - 0.032w_1 + 0.04$. | correct | B39 |
| `items[8].rubric[4]` | (1) Differentiates, solves $w_1 = 0.1951$ and states that the methods agree. | correct | B39 |
| `items[8].rubric[5]` | (1) Finds $\sigma_p^2 = 0.0369$ and $\sigma_p = 19.2\%$, below B alone. | correct | B39 |
| `items[8].rubric[6]` | (1) Finds $\lambda = 0.0738$ and notes it equals $2\sigma_p^2$. | correct | B39 |
| `items[8].rubric[7]` | (1) At $\rho = -1$ finds $w_1 = 0.4$ and zero volatility. | correct | B39 |
| `items[8].rubric[8]` | (1) At $\rho = 0.9$ finds the formula gives a negative weight, $w_1 = -0.64$. | correct | B39 |
| `items[8].rubric[9]` | (1) Concludes that with no short sales the fund holds B alone, explaining why the clipped end is the minimum. | correct | B39 |
| `items[8].feedback.correct` | Your self-mark is 7 or more out of 10. | correct | B39 |
| `items[8].feedback.generic` | Compare your working with the model answer, line by line. | correct | B39 |

## problems-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Take $f(x, y) = 2x^3 - 6xy + 3y^2$. We find where its surface is level and what kind of point each one is. | correct | B40 |
| `items[0].parts[0].question` | Solve $f_x = 0$ and $f_y = 0$ together. Which values of $x$ give stationary points? Give every value, separated by commas. | correct | B40 |
| `items[0].parts[0].widget.answers` | 0, 1 | correct | B40 |
| `items[0].parts[0].widget.wrong[0]` | slip sign = 0, -1 | correct | B40 |
| `items[0].parts[0].feedback.correct` | $f_y = 6y - 6x = 0$ gives $y = x$. Then $f_x = 6x^2 - 6y = 6x(x - 1) = 0$, so $x = 0$ or $x = 1$. | correct | B40 |
| `items[0].parts[0].feedback.generic` | Not quite. Use $f_y = 0$ to write $y$ in terms of $x$, then put that into $f_x = 0$. | correct | B40 |
| `items[0].parts[0].feedback.byKey.count` | This needs 2 values. If you divided $6x^2 - 6x = 0$ by $x$, you lost the root $x = 0$. | correct | B40 |
| `items[0].parts[0].feedback.byKey.sign` | Check the factorising: $6x^2 - 6x = 6x(x - 1)$, so the roots are 0 and 1. | correct | B40 |
| `items[0].parts[0].explain.text` | $f_x = 6x^2 - 6y$ and $f_y = 6y - 6x$. The second forces $y = x$, so $6x(x - 1) = 0$ and the stationary points are $(0, 0)$ and $(1, 1)$. | correct | B40 |
| `items[0].parts[1].question` | Find $D = f_{xx} f_{yy} - f_{xy}^2$ as an expression in $x$. | correct | B40 |
| `items[0].parts[1].widget.answer` | 72x-36 | correct | B40 |
| `items[0].parts[1].widget.accept` | 36(2x-1) | correct | B40 |
| `items[0].parts[1].widget.wrong[0]` | slip plus = 72x+36 | correct | B40 |
| `items[0].parts[1].widget.wrong[1]` | slip no-mixed = 72x | correct | B40 |
| `items[0].parts[1].widget.wrong[2]` | slip no-square = 72x+6 | correct | B40 |
| `items[0].parts[1].feedback.correct` | $f_{xx} = 12x$, $f_{yy} = 6$ and $f_{xy} = -6$. So $D = 72x - 36$. | correct | B40 |
| `items[0].parts[1].feedback.generic` | Not quite. Find the three second partials, then form $f_{xx} f_{yy} - f_{xy}^2$. | correct | B40 |
| `items[0].parts[1].feedback.byKey.plus` | You added $f_{xy}^2$. The determinant subtracts it: $72x - 36$. | correct | B40 |
| `items[0].parts[1].feedback.byKey.no-mixed` | You left out the mixed partial. $f_{xy} = -6$, so subtract 36. | correct | B40 |
| `items[0].parts[1].feedback.byKey.no-square` | You subtracted $f_{xy} = -6$ without squaring it. Subtract $(-6)^2 = 36$. | correct | B40 |
| `items[0].parts[1].explain.text` | From $f_x = 6x^2 - 6y$ we get $f_{xx} = 12x$ and $f_{xy} = -6$. With $f_{yy} = 6$, $D = 72x - 36$. | correct | B40 |
| `items[0].parts[2].question` | Using $D = 72x - 36$, what is $D$ at the stationary point $(0, 0)$? | correct | B40 |
| `items[0].parts[2].widget.answer` | -36 | correct | B40 |
| `items[0].parts[2].widget.wrong[0]` | slip plus = 36 | correct | B40 |
| `items[0].parts[2].widget.wrong[1]` | slip no-mixed = 0 | correct | B40 |
| `items[0].parts[2].widget.wrong[2]` | slip no-square = 6 | correct | B40 |
| `items[0].parts[2].feedback.correct` | $D(0, 0) = -36 < 0$, so $(0, 0)$ is a saddle. | correct | B40 |
| `items[0].parts[2].feedback.generic` | Not quite. Put $x = 0$ into $72x - 36$. | correct | B40 |
| `items[0].parts[2].feedback.byKey.plus` | That comes from adding $f_{xy}^2$. With $D = 72x - 36$, $D(0, 0) = -36$. | correct | B40 |
| `items[0].parts[2].feedback.byKey.no-mixed` | That comes from leaving out $f_{xy}$. The mixed partial makes $D(0, 0) = -36$. | correct | B40 |
| `items[0].parts[2].feedback.byKey.no-square` | That comes from not squaring $f_{xy}$. Squared, it gives $D(0, 0) = -36$. | correct | B40 |
| `items[0].parts[2].explain.text` | $D(0, 0) = -36$. A negative $D$ means a saddle: the contours cross at $(0, 0)$. | correct | B40 |
| `items[0].parts[3].question` | Using $D = 72x - 36$ and $f_{xx} = 12x$, what kind of point is $(1, 1)$? | correct | B40 |
| `items[0].parts[3].widget.options[0]` | option pit (key): A pit | correct | B40 |
| `items[0].parts[3].widget.options[1]` | option peak: A peak | correct | B40 |
| `items[0].parts[3].widget.options[1].why` | You read $D > 0$ as a peak. That needs $f_{xx} < 0$, and here $f_{xx} = 12$. | correct | B40 |
| `items[0].parts[3].widget.options[2]` | option saddle: A saddle | correct | B40 |
| `items[0].parts[3].widget.options[2].why` | A saddle needs $D < 0$. At $(1, 1)$, $D = 72 - 36 = 36$. | correct | B40 |
| `items[0].parts[3].widget.options[3]` | option none: No verdict | correct | B40 |
| `items[0].parts[3].widget.options[3].why` | The test is silent only when $D = 0$. Here $D = 36$. | correct | B40 |
| `items[0].parts[3].feedback.correct` | $D(1, 1) = 36 > 0$ and $f_{xx} = 12 > 0$, so $(1, 1)$ is a pit. | correct | B40 |
| `items[0].parts[3].feedback.generic` | Not quite. Find $D$ and the sign of $f_{xx}$ at $(1, 1)$. | correct | B40 |
| `items[0].parts[3].explain.text` | At $(1, 1)$, $D = 36 > 0$, so it is a peak or a pit. $f_{xx} = 12 > 0$ makes the slices bend up: a pit. | correct | B40 |
| `items[0].parts[4].question` | Using part 4, what is $f$ at the bottom of the pit $(1, 1)$? | correct | B40 |
| `items[0].parts[4].widget.answer` | -1 | correct | B40 |
| `items[0].parts[4].widget.wrong[0]` | slip plus-xy = 11 | correct | B40 |
| `items[0].parts[4].widget.wrong[1]` | slip origin = 0 | correct | B40 |
| `items[0].parts[4].widget.wrong[2]` | slip sign = 1 | correct | B40 |
| `items[0].parts[4].feedback.correct` | $f(1, 1) = 2 - 6 + 3 = -1$. | correct | B40 |
| `items[0].parts[4].feedback.generic` | Not quite. Put $x = 1$ and $y = 1$ into $2x^3 - 6xy + 3y^2$. | correct | B40 |
| `items[0].parts[4].feedback.byKey.plus-xy` | You added the $6xy$ term. It is subtracted: $2 - 6 + 3 = -1$. | correct | B40 |
| `items[0].parts[4].feedback.byKey.origin` | That is $f$ at the saddle $(0, 0)$. The pit is at $(1, 1)$. | correct | B40 |
| `items[0].parts[4].feedback.byKey.sign` | f(1, 1) = 2 − 6 + 3, and the 6 outweighs the 5, so the value is −1. A positive 1 takes 6 − 5, the wrong way round. | correct | B40 |
| `items[0].parts[4].explain.text` | $f(1, 1) = 2 - 6 + 3 = -1$, the bottom of a local pit. It is not the lowest value overall: $2x^3$ falls without limit as $x$ becomes very negative. | correct | B40 |
| `items[1].prose` | A fund sizes two signals: $x$ in momentum and $y$ in carry, in £m. Its model puts expected yearly profit, in £k, at $P(x, y) = 14x + 6y - x^2 - y^2$. | correct | B40 |
| `items[1].parts[0].question` | Where is $P$ stationary, with no limit on capital? Give the point as a pair $(x, y)$. | correct | B40 |
| `items[1].parts[0].widget.answer` | (7, 3) | correct | B40 |
| `items[1].parts[0].widget.accept` | (7,3) | correct | B40 |
| `items[1].parts[0].widget.wrong[0]` | slip no-half = (14, 6) | correct | B40 |
| `items[1].parts[0].widget.wrong[1]` | slip swapped = (3, 7) | correct | B40 |
| `items[1].parts[0].feedback.correct` | $P_x = 14 - 2x = 0$ and $P_y = 6 - 2y = 0$ give $(7, 3)$. | correct | B40 |
| `items[1].parts[0].feedback.generic` | Not quite. Set both partial derivatives to zero and solve. | correct | B40 |
| `items[1].parts[0].feedback.byKey.no-half` | You set $14 - x = 0$. The derivative of $x^2$ is $2x$, so $x = 7$. | correct | B40 |
| `items[1].parts[0].feedback.byKey.swapped` | You swapped the sizes. $P_x = 0$ gives $x = 7$ and $P_y = 0$ gives $y = 3$. | correct | B40 |
| `items[1].parts[0].feedback.byKey.length` | Give the point as two numbers in brackets, $x$ first. | correct | B40 |
| `items[1].parts[0].explain.text` | $\nabla P = (14 - 2x, 6 - 2y)$ is zero at $(7, 3)$, which uses £10m in all. | correct | B40 |
| `items[1].parts[1].question` | At $(7, 3)$, $P_{xx} = P_{yy} = -2$ and $P_{xy} = 0$. What kind of point is it? | correct | B40 |
| `items[1].parts[1].widget.options[0]` | option peak (key): A peak | correct | B40 |
| `items[1].parts[1].widget.options[1]` | option pit: A pit | correct | B40 |
| `items[1].parts[1].widget.options[1].why` | You read $D > 0$ as a pit. With $P_{xx} = -2 < 0$ the slices bend down. | correct | B40 |
| `items[1].parts[1].widget.options[2]` | option saddle: A saddle | correct | B40 |
| `items[1].parts[1].widget.options[2].why` | A saddle needs $D < 0$. Here $D = (-2)(-2) - 0 = 4$. | correct | B40 |
| `items[1].parts[1].widget.options[3]` | option none: No verdict | correct | B40 |
| `items[1].parts[1].widget.options[3].why` | The test is silent only when $D = 0$. Here $D = 4$. | correct | B40 |
| `items[1].parts[1].feedback.correct` | $D = 4 > 0$ and $P_{xx} = -2 < 0$, so $(7, 3)$ is a peak, with $P = 58$. | correct | B40 |
| `items[1].parts[1].feedback.generic` | Not quite. Work out $D = P_{xx}P_{yy} - P_{xy}^2$ and the sign of $P_{xx}$. | correct | B40 |
| `items[1].parts[1].explain.text` | $D = 4 > 0$ with $P_{xx} < 0$: a peak. With no limit, the fund would put £10m to work for £58k. | correct | B40 |
| `items[1].parts[2].question` | The fund has only £6m, so $x + y = 6$, and the peak's £10m is out of reach. Using $\nabla P = \lambda \nabla g$ with $g = x + y$, what is $x$ at th... | correct | B40 |
| `items[1].parts[2].widget.answer` | 5 | correct | B40 |
| `items[1].parts[2].widget.wrong[0]` | slip scaled = 4.2 | correct | B40 |
| `items[1].parts[2].widget.wrong[1]` | slip even = 3 | correct | B40 |
| `items[1].parts[2].widget.wrong[2]` | slip free = 7 | correct | B40 |
| `items[1].parts[2].feedback.correct` | $14 - 2x = \lambda$ and $6 - 2y = \lambda$ give $x - y = 4$. With $x + y = 6$, $x = 5$ and $y = 1$. | correct | B40 |
| `items[1].parts[2].feedback.generic` | Not quite. Set $14 - 2x$ and $6 - 2y$ both equal to $\lambda$, then use $x + y = 6$. | correct | B40 |
| `items[1].parts[2].feedback.byKey.scaled` | You scaled $(7, 3)$ down to fit £6m. The best point is where a contour touches the line, at $x = 5$. | correct | B40 |
| `items[1].parts[2].feedback.byKey.even` | An even split ignores that momentum pays more. The Lagrange conditions give $x - y = 4$. | correct | B40 |
| `items[1].parts[2].feedback.byKey.free` | That is the free peak, which needs £10m. On $x + y = 6$ the best is $x = 5$. | correct | B40 |
| `items[1].parts[2].explain.text` | Equal multipliers give $14 - 2x = 6 - 2y$, so $x = y + 4$. With $x + y = 6$ that is $(5, 1)$, where $P = 50$. | correct | B40 |
| `items[1].parts[3].question` | Using $x = 5$ and $y = 1$, what is the multiplier $\lambda$? | correct | B40 |
| `items[1].parts[3].widget.answer` | 4 | correct | B40 |
| `items[1].parts[3].widget.wrong[0]` | slip sign = -4 | correct | B40 |
| `items[1].parts[3].widget.wrong[1]` | slip value = 50 | correct | B40 |
| `items[1].parts[3].feedback.correct` | $\lambda = 14 - 2(5) = 6 - 2(1) = 4$. | correct | B40 |
| `items[1].parts[3].feedback.generic` | Not quite. Put the point into $P_x = \lambda g_x$ or $P_y = \lambda g_y$, with $g_x = g_y = 1$. | correct | B40 |
| `items[1].parts[3].feedback.byKey.sign` | Check the sign: $P_x = 14 - 2x = 4$ at $x = 5$, and $g_x = 1$. | correct | B40 |
| `items[1].parts[3].feedback.byKey.value` | That is the best profit, £50k. The multiplier is $P_x / g_x = 4$. | correct | B40 |
| `items[1].parts[3].explain.text` | $\lambda = P_x / g_x = 14 - 10 = 4$, and $P_y / g_y$ agrees. Each extra £1m of capital is worth about £4k a year. | correct | B40 |
| `items[1].parts[4].question` | At £6m the best profit is £50k. Using $\lambda = 4$, estimate the best profit, in £k, if capital rises to £6.5m. | correct | B40 |
| `items[1].parts[4].widget.answer` | 52 | correct | B40 |
| `items[1].parts[4].widget.accept` | 52 (the exact best, 51.875, is accepted too) | correct | B40 |
| `items[1].parts[4].widget.wrong[0]` | slip full-lambda = 54 | correct | B40 |
| `items[1].parts[4].widget.wrong[1]` | slip no-lambda = 50.5 | correct | B40 |
| `items[1].parts[4].widget.wrong[2]` | slip sign = 48 | correct | B40 |
| `items[1].parts[4].feedback.correct` | $50 + 4 \times 0.5 = 52$, so about £52k. Solving again on $x + y = 6.5$ gives the exact £51.875k. | correct | B40 |
| `items[1].parts[4].feedback.generic` | Not quite. $\lambda$ is the gain in best profit per extra £1m, so multiply it by 0.5. | correct | B40 |
| `items[1].parts[4].feedback.byKey.full-lambda` | You added a whole $\lambda$. The limit rises by 0.5, so the gain is $4 \times 0.5 = 2$. | correct | B40 |
| `items[1].parts[4].feedback.byKey.no-lambda` | You added the £0.5m itself. Each £1m is worth $\lambda = 4$, so add $4 \times 0.5$. | correct | B40 |
| `items[1].parts[4].feedback.byKey.sign` | You took $\lambda \times 0.5$ off. More capital helps here, so the best profit rises. | correct | B40 |
| `items[1].parts[4].explain.text` | The best value moves by about $\lambda$ per unit of relaxed limit: $50 + 4(0.5) = 52$. The exact best, at $(5.25, 1.25)$, is 51.875. | correct | B40 |
| `items[2].prose` | Asset A has volatility 40% and asset B 25%, with correlation 0.3. A portfolio holds the share $w$ in A and $1 - w$ in B, so $\sigma_p^2 = 0.16w^2 +... | correct | B40 |
| `items[2].parts[0].question` | Expand $\sigma_p^2$ as a quadratic in $w$. | correct | B40 |
| `items[2].parts[0].widget.answer` | 0.1625w^2-0.065w+0.0625 | correct | B40 |
| `items[2].parts[0].widget.accept` | \frac{13w^2}{80}-\frac{13w}{200}+\frac{1}{16} | correct | B40 |
| `items[2].parts[0].widget.wrong[0]` | slip no-cross = 0.2225w^2-0.125w+0.0625 | correct | B40 |
| `items[2].parts[0].widget.wrong[1]` | slip half-cross = 0.1925w^2-0.095w+0.0625 | correct | B40 |
| `items[2].parts[0].feedback.correct` | $0.16w^2 + 0.0625(1 - 2w + w^2) + 0.06(w - w^2) = 0.1625w^2 - 0.065w + 0.0625$. | correct | B40 |
| `items[2].parts[0].feedback.generic` | Not quite. Expand $(1 - w)^2$ and $w(1 - w)$, then collect the $w^2$, $w$ and constant terms. | correct | B40 |
| `items[2].parts[0].feedback.byKey.no-cross` | You dropped the correlation term $0.06w(1 - w)$. It adds $0.06w - 0.06w^2$. | correct | B40 |
| `items[2].parts[0].feedback.byKey.half-cross` | You halved the correlation term. It is $2 \times 0.3 \times 0.4 \times 0.25 = 0.06$ times $w(1 - w)$. | correct | B40 |
| `items[2].parts[0].explain.text` | The $w^2$ terms are $0.16 + 0.0625 - 0.06 = 0.1625$ and the $w$ terms are $-0.125 + 0.06 = -0.065$. The constant is 0.0625. | correct | B40 |
| `items[2].parts[1].question` | Using $\sigma_p^2 = 0.1625w^2 - 0.065w + 0.0625$, which $w$ gives the minimum variance portfolio? Give the exact decimal. | correct | B40 |
| `items[2].parts[1].widget.answer` | 0.2 | correct | B40 |
| `items[2].parts[1].widget.wrong[0]` | slip no-two = 0.4 | correct | B40 |
| `items[2].parts[1].widget.wrong[1]` | slip gave-b = 0.8 | correct | B40 |
| `items[2].parts[1].widget.wrong[2]` | slip carried = 0.2809 | correct | B40 |
| `items[2].parts[1].feedback.correct` | $\frac{d\sigma_p^2}{dw} = 0.325w - 0.065 = 0$ gives $w = 0.2$: 20% in A and 80% in B. | correct | B40 |
| `items[2].parts[1].feedback.generic` | Not quite. Set the derivative $0.325w - 0.065$ to zero. | correct | B40 |
| `items[2].parts[1].feedback.byKey.no-two` | You solved $0.1625w - 0.065 = 0$. The derivative of $0.1625w^2$ is $0.325w$. | correct | B40 |
| `items[2].parts[1].feedback.byKey.gave-b` | That is the weight in B. The weight in A is $w = 0.2$. | correct | B40 |
| `items[2].parts[1].feedback.byKey.carried` | That comes from the quadratic without the correlation term. With $0.1625w^2 - 0.065w + 0.0625$ the minimum is at $w = 0.2$. | correct | B40 |
| `items[2].parts[1].explain.text` | The parabola $0.1625w^2 - 0.065w + 0.0625$ is lowest where $0.325w = 0.065$, at $w = 0.2$. More money goes in B, the calmer asset. | correct | B40 |
| `items[2].parts[2].question` | Using $w = 0.2$, what is the portfolio's volatility $\sigma_p$? Give a decimal to 4 places. | correct | B40 |
| `items[2].parts[2].widget.answer` | 0.2366 | correct | B40 |
| `items[2].parts[2].widget.wrong[0]` | slip variance = 0.056 | correct | B40 |
| `items[2].parts[2].widget.wrong[1]` | slip weighted = 0.28 | correct | B40 |
| `items[2].parts[2].widget.wrong[2]` | slip carried-half = 0.25 | correct | B40 |
| `items[2].parts[2].feedback.correct` | $\sigma_p^2 = 0.0065 - 0.013 + 0.0625 = 0.056$, so $\sigma_p = \sqrt{0.056} \approx 0.2366$, or 23.66%. | correct | B40 |
| `items[2].parts[2].feedback.generic` | Not quite. Put $w = 0.2$ into the quadratic, then take the square root. | correct | B40 |
| `items[2].parts[2].feedback.byKey.variance` | That is the variance. The volatility is its square root. | correct | B40 |
| `items[2].parts[2].feedback.byKey.weighted` | That is the weighted average of the volatilities, which holds only when $\rho = 1$. With $\rho = 0.3$ the risk is lower. | correct | B40 |
| `items[2].parts[2].feedback.byKey.carried-half` | That is the volatility at $w = 0.4$, from solving $0.1625w = 0.065$. At $w = 0.2$ it is 0.2366. | correct | B40 |
| `items[2].parts[2].explain.text` | The variance at $w = 0.2$ is 0.056, so $\sigma_p \approx 0.2366$. That is below B's 25%, though A is the riskier asset. | correct | B40 |
| `items[2].parts[3].question` | Now treat both weights as free, $w_1$ in A and $w_2$ in B, with the budget $w_1 + w_2 = 1$. The minimum is at $w_1 = 0.2$, $w_2 = 0.8$. Here $\frac... | correct | B40 |
| `items[2].parts[3].widget.answer` | 0.112 | correct | B40 |
| `items[2].parts[3].widget.wrong[0]` | slip variance = 0.056 | correct | B40 |
| `items[2].parts[3].widget.wrong[1]` | slip no-cross = 0.064 | correct | B40 |
| `items[2].parts[3].feedback.correct` | $\lambda = 0.064 + 0.048 = 0.112$, which is $2\sigma_p^2 = 2 \times 0.056$. | correct | B40 |
| `items[2].parts[3].feedback.generic` | Not quite. Put $w_1 = 0.2$ and $w_2 = 0.8$ into $0.32w_1 + 0.06w_2$. | correct | B40 |
| `items[2].parts[3].feedback.byKey.variance` | That is $\sigma_p^2$ itself. The multiplier is twice it: 0.112. | correct | B40 |
| `items[2].parts[3].feedback.byKey.no-cross` | You left out $0.06w_2$, the correlation term. It adds 0.048. | correct | B40 |
| `items[2].parts[3].explain.text` | $\lambda = 0.32(0.2) + 0.06(0.8) = 0.112$, and $\frac{\partial \sigma_p^2}{\partial w_2} = 0.1 + 0.012$ agrees. It equals $2\sigma_p^2$, as the les... | correct | B40 |
| `items[2].parts[4].question` | The fund must now place 102% of its capital, so $w_1 + w_2 = 1.02$. Using $\sigma_p^2 = 0.056$ and $\lambda = 0.112$ at a budget of 1, estimate the... | correct | B40 |
| `items[2].parts[4].widget.answer` | 0.05824 | correct | B40 |
| `items[2].parts[4].widget.wrong[0]` | slip sigma-lambda = 0.05712 | correct | B40 |
| `items[2].parts[4].widget.wrong[1]` | slip no-change = 0.056 | correct | B40 |
| `items[2].parts[4].widget.wrong[2]` | slip whole-lambda = 0.168 | correct | B40 |
| `items[2].parts[4].widget.accept` | 0.05824, from $0.056 + 0.112 \times 0.02$ (0.0582 and the exact value, 0.0583, are accepted too) | correct | B40 |
| `items[2].parts[4].feedback.correct` | $0.056 + 0.112 \times 0.02 = 0.056 + 0.00224 = 0.05824$. Scaling both weights by 1.02 gives the exact value, $0.056 \times 1.0404 \approx 0.05826$. | correct | B40 |
| `items[2].parts[4].feedback.generic` | Not quite. The smallest variance moves by about $\lambda$ per unit of budget, so add $\lambda \times 0.02$. | correct | B40 |
| `items[2].parts[4].feedback.byKey.sigma-lambda` | You used $\lambda = 0.056$, the variance itself. The multiplier is $2\sigma_p^2 = 0.112$. | correct | B40 |
| `items[2].parts[4].feedback.byKey.no-change` | The budget grew, so the smallest variance grows too, by about $\lambda \times 0.02$. | correct | B40 |
| `items[2].parts[4].feedback.byKey.whole-lambda` | You added a whole $\lambda$. The budget rises by 0.02, so add $0.112 \times 0.02$. | correct | B40 |
| `items[2].parts[4].explain.text` | $\lambda$ is the change in the best value per unit of budget, so the variance rises by about $0.112 \times 0.02 = 0.00224$ to 0.05824. Placing 2% m... | correct | B40 |

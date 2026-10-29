# Report: linear-maps level 3, "Duality and inner products"

Course `linear-maps` (topic 1.10, strand pure), level 3, from `## Level 3` of `docs/briefs/linear-maps.md`. Lesson ids, names, objectives and skills are those of `app/content/courses/linear-maps/course.json`: l10 uses `lx-dual`, l11 to l14 use `lx-inner`; review and homework items carry their own skill. Notation follows the brief and levels 1 and 2: bold vectors, plain polynomials, $V'$, $\varphi_j$, $T'$, $\langle \mathbf{u}, \mathbf{v} \rangle$, $\|\mathbf{v}\|$, $U^\perp$, $P_U$, $\mathrm{Var}$ and $\mathrm{Cov}$ in `\mathrm`, the $\tfrac1n$ covariance convention of `eigen` l7, £ for money, proofs ending with $\blacksquare$, every `choice` shuffled. Cited unwritten or other-course lessons: `proof` l13-induction (l13), `analysis` l15-epsilon-delta (l11 quiz), `vectors` l3, `least-squares` l3, l4, l6, l12, `eigen` l7.

## Files written

All in `app/content/courses/linear-maps/`.

| File | Screens | Quiz / items | Canvases | Contents |
|---|---:|---:|---|---|
| `l10-dual-space.json` | 12 | 4 | vectors, matrix, plane, code | P&L rule $\varphi_1 = \tfrac{x + y}{2}$ (`expression`), drag $\mathbf{u}$ and read its $\mathbf{v}_1$-coordinate (explore), dual basis named with $\varphi_2 = \tfrac{x - y}{2}$, rows of $\mathbf{B}^{-1}$ (`expression`, `pmatrix`), Lagrange $\ell_1 = 2x - x^2$ (plane), $D'\varphi$ values $0, 1, 2, 3$ (`table`), trap $x$ against $x - y$, $\dim V' = \dim V$ (`choice`), independence (`order`), transpose (`order`), `dual_basis` code, exposures $(2, 4)$ in a new basis |
| `l11-inner-products.json` | 11 | 4 | vectors, table, matrix | three products on $(0, 1)$ (`table`: 1, $-1$, 0), drag $\mathbf{v}$ (explore), axioms and norm (positivity), $\langle \mathbf{e}_1, \mathbf{e}_2 \rangle_{\mathbf{A}} = 1$, positive weights, the complex bar (positivity), covariance on raw returns trap (definiteness, distractor positivity), $\|\lambda\mathbf{v}\| = |\lambda|\,\|\mathbf{v}\|$ (`order`), Pythagoras (`order`), max norm fails the parallelogram law (2 against 4), uncorrelated books £5,000 |
| `l12-cauchy-schwarz.json` | 11 | 4 | space, vectors, plane, table, number-line | 1.03 hook with $11 \le 15$ (`table`), equality on the line (explore), $c = 0.44$, the $\|\mathbf{w}\|^2 \ge 0$ step (`choice`), discriminant proof (`order`), divide-by-zero flaw (tap rows), triangle inequality (`order`), perpendicular trap, $\rho \in [-1, 1]$ (number-line), main proof (`order`), $\sqrt{37}$ diversification (£6,082.76) |
| `l13-gram-schmidt-proved.json` | 12 | 5 | matrix, vectors, space, plane, code | $\beta = 1$, leftover orthogonal (explore), residual $(1, 1, -1, -1)$, $\mathbf{f}_2$, $\|\mathbf{f}_2\|^2 = 1.5$, $\mathbf{f}_3$, Legendre $x^2 - \tfrac13$, projections-onto-$\mathbf{v}$s trap ($-0.5$), why $\mathbf{f}_k \ne \mathbf{0}$ (`choice`), inductive step (`order`), `gram_schmidt` code with the QR sign note, order of orthogonalisation (`choice`) |
| `l14-orthogonal-complements.json` | 12 | 5 | vectors (`lockTo`), space (slider on $t$), plane (slider on $c$, `integral` caption), code, matrix | nearest point $(2, 1)$ (`drag-point`), residual orthogonal (explore), $U^\perp$ a subspace (`order`), $\dim U^\perp = 2$, $P_U\mathbf{v} = (1, 1, 1)$, residual $(2, -1, -1)$, best constant $\tfrac13$, single-projections trap, Axler 6.49 (`order`), minimisation (`order`), `project` and `complement_basis` code, hedge variance 1 |
| `review-3.json` | | 9 | matrix | difficulties 3, 2, 2, 4, 3, 3, 3, 2, 3; lessons l10, l11, l12, l12, l13, l14, l12, l11, l10 |
| `homework-3.json` | | 9 | table | difficulties 4, 3, 3, 4, 4, 5, 5, 3, 3: $(U^\perp)^\perp = U$ (`order`), $\ell_2$ (`expression`), a dual map, $\|x - \tfrac12\|^2 = \tfrac1{12}$, best line $x - \tfrac16$ on $[0, 1]$, `residual_factors` code, Cauchy-Schwarz and the 1.03 bug (`longform`, 10 points), covariance flaw (tap rows), $0.98 \to 1.0316$ |

Generators and checks are in `/tmp/claude-0/-home-user-zero-to-quant/9fb26fd5-8508-5986-8a3a-66bc5f67acde/scratchpad/linear-maps-3/`: `common.py`, `gen_l10.py` to `gen_l14.py`, `gen_sets.py`, `voice.py` (sentence length, dashes, exclamation marks, explanation length), `codecheck.py` (every code solution and starter against its hidden tests, in CPython and in Pyodide 0.27.7 under node from the local CDN), `checks.py` (second pass on the numbers) and `pyo.mjs`. Edit the generators and rerun them rather than the JSON.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 367 warnings, none in a level 3 file. The only linear-maps line is the course's "not yet written" warning for level 4.

## Playthrough

All with `--local-cdn /tmp/claude-0/-home-user-zero-to-quant/9fb26fd5-8508-5986-8a3a-66bc5f67acde/scratchpad/pkgs`, with `--shots --mobile --why` while authoring. I looked at the screenshots at 1280 px and 390 px.

| Target | Result |
|---|---|
| `--lesson linear-maps/l10-dual-space` | ok, 16 checks, quiz 4/4 |
| `--lesson linear-maps/l11-inner-products` | ok, 15 checks, quiz 4/4 |
| `--lesson linear-maps/l12-cauchy-schwarz` | ok, 15 checks, quiz 4/4 |
| `--lesson linear-maps/l13-gram-schmidt-proved` | ok, 17 checks, quiz 5/5 |
| `--lesson linear-maps/l14-orthogonal-complements` | ok, 17 checks, quiz 5/5 |
| `--set linear-maps/review-3` | ok, 9 of 9 recorded |
| `--set linear-maps/homework-3` | ok, 9 of 9 right, 39 of 39 marks |

No run flaked. Fixes made after the screenshots:
- l10 trap: the dashed "old $\mathbf{v}_2$" was in `params.segments` and did not draw; moved to `state.segments` (already in the inbox from level 1). The $\mathbf{v}_1$ label sat on the tick "1.0"; now a mid label.
- l11: the axioms table clipped the additivity row at 390 px; the row now reads "... is ..." with words between two short formulas, and the header is shorter. Vector labels on the axes sat on tick labels (parallelogram and transfer); now mid labels on the side away from the ticks.
- l12: the space view crowded $\mathbf{u}$, $c\mathbf{v}$ and $\mathbf{w}$; the camera now looks along the normal of $\operatorname{span}(\mathbf{u}, \mathbf{v})$ (az $-166$, el 36, from $\mathbf{u} \times \mathbf{v} = (8, 2, -6)$), and $\mathbf{w}$ has a mid label. The $q(t)$ label floated above the plot; the range and `labelAt` changed.
- l13: $\mathbf{f}_2$ and $\mathbf{f}_3$ overlapped near the $z$-axis; camera az $-100$.
- Homework: a raw-string slip printed `\"proves\"`; now 'proves'.

## Proofs and the widget that grades each step

| Proof | Where | Widget |
|---|---|---|
| The dual basis is independent | l10 derive | `order`, 4 lines; distractor "each $\varphi_j$ is non-zero" |
| Independent of length $n$ gives a basis of $V'$ | l10 quiz | `choice` (l4) |
| $\dim V' = \dim V$ | l10 generalise | `choice` ($n \cdot 1$, l9) |
| Matrix of $T'$ is $\mathbf{A}^T$ (Axler 3.114) | l10 derive | `order`, 4 lines, `same` on the two evaluations; distractor $\mathbf{A}^{-1}$ |
| Which axiom fails (four non-examples) | l11 | `choice` each: $x_1y_1 - x_2y_2$, weights, no bar, covariance on raw returns; quiz $x_1y_1$ and the spike function |
| $\|\lambda\mathbf{v}\| = |\lambda|\,\|\mathbf{v}\|$ | l11 generalise | `order`, 4 lines; distractor $\lambda^2$ |
| Pythagoras | l11 derive | `order`, 4 lines; distractor adding lengths; quiz `choice` for the cross terms |
| Cauchy-Schwarz (Axler 6.14) | l12 derive | `order`, 5 lines; distractor $\mathbf{u} \perp \mathbf{v}$; inequality step `choice` ($\|\mathbf{w}\|^2 \ge 0$) |
| Cauchy-Schwarz over $\mathbb{R}$ by the discriminant | l12, review | `order`, 5 lines; distractor two roots; review `choice` for the discriminant step |
| Missing $\mathbf{v} = \mathbf{0}$ case | l12 | tap the flawed row |
| Triangle inequality (Axler 6.17) | l12 | `order`, 4 lines; distractor dropping the cross term; quiz `choice` for $\operatorname{Re} \le |\cdot| \le \|\mathbf{u}\|\,\|\mathbf{v}\|$ |
| An orthonormal list is independent | l13 quiz | `order`, 3 lines; distractor "no two are multiples" |
| Gram-Schmidt (Axler 6.32), inductive step | l13 derive | `order`, 6 lines, `same` on the two span inclusions; distractor $\mathbf{v}_k \perp \mathbf{e}_j$; `choice` for $\mathbf{f}_k \ne \mathbf{0}$ (generalise), `choice` for $\langle \mathbf{f}_k, \mathbf{e}_j \rangle = 0$ (quiz) |
| Orthonormal list extends to an orthonormal basis | l13 quiz | `choice` |
| $U^\perp$ is a subspace | l14 | `order`, 4 lines, `same` on the three checks; distractor from the picture |
| $V = U \oplus U^\perp$ (Axler 6.49) | l14 generalise | `order`, 5 lines; distractor "orthogonal to $\mathbf{e}_1$"; quiz `choice` definiteness (distractor positivity) |
| Minimisation (Axler 6.61) | l14 derive | `order`, 5 lines; distractor $\mathbf{v} \perp \mathbf{u}$; quiz `choice` for why the pieces are orthogonal |
| $(U^\perp)^\perp = U$ | l14 quiz, homework | `choice`; homework `order`, 4 lines, circular distractor |
| Covariance is an inner product on all of $\mathbb{R}^n$ (false) | homework | tap the flawed row |
| Cauchy-Schwarz, $|\rho| \le 1$ and the divisor bug | homework | `longform`, rubric 1 + 2 + 1 + 1 + 1 + 1 + 1 + 1 + 1 = 10, full model answer |

## Numbers, each computed twice

First pass: exact fractions and NumPy while writing the generators. Second pass: `checks.py`, 74 checks by independent numerical routes (inverse matrices, `vander`, QR with signs fixed, trapezoid quadrature on 200,001 points, grid search for minima). All agree.

- l10: $\varphi_1 = \tfrac{x + y}{2}$, $\varphi_2 = \tfrac{x - y}{2}$ (values 1, 0 and 0, 1 on the basis); $\mathbf{B}^{-1} = \begin{pmatrix}0.5&0.5\\0.5&-0.5\end{pmatrix}$; trap basis $(1, 0), (1, 1)$ gives $\mathbf{B}^{-1}$ rows $(1, -1), (0, 1)$, so $\varphi_1 = x - y$; Lagrange $\ell_0 = 1 - 1.5x + 0.5x^2$, $\ell_1 = 2x - x^2$, $\ell_2 = -0.5x + 0.5x^2$ (columns of the inverse Vandermonde, and evaluation at 0, 1, 2); $(1, 1, 1)[D] = (0, 1, 2, 3)$; transfer $(3, -1)\mathbf{P} = (2, 4)$, wrong $(3, -1)\mathbf{P}^{-1} = (1, 2)$, coordinates of $(3, 1)$ are $(2, 1)$ and both P&Ls are 8 (£8k); quiz $[T']$ is $2 \times 3$.
- l10 code, "compute and report": the $3 \times 3$ basis with columns $(2, 1, 0), (0, 1, 1), (1, 0, 1)$ has inverse $\tfrac13\begin{pmatrix}1&1&-1\\-1&2&1\\1&-2&2\end{pmatrix}$, rounded `[[0.333333, 0.333333, -0.333333], [-0.333333, 0.666667, 0.333333], [0.333333, -0.666667, 0.666667]]`.
- l11: $\langle (0, 1), (0, 1) \rangle$ = 1, $-1$, 0; $\mathbf{A} = \begin{pmatrix}2&1\\1&2\end{pmatrix}$ has eigenvalues 1 and 3, $\langle \mathbf{e}_1, \mathbf{e}_2 \rangle_{\mathbf{A}} = 1$, $\|\mathbf{e}_1\|_{\mathbf{A}} = \sqrt2$; $i \cdot i = -1$, $i\bar{i} = 1$, $(1 + i)^2 = 2i$, $|1 + i|^2 = 2$; max norm $1 + 1 = 2$ against $2(1 + 1) = 4$; $\sqrt{9 + 16} = 5$, £5,000; quiz $\int_0^1 x = 0.5$.
- l12: $\langle \mathbf{u}, \mathbf{v} \rangle = 11$, $\|\mathbf{u}\| = 3$, $\|\mathbf{v}\| = 5$, 15; $c = 0.44$, $c\mathbf{v} = (1.32, 0, 1.76)$, $\mathbf{w} = (-0.32, 2, 0.24)$, $\langle \mathbf{w}, \mathbf{v} \rangle = 0$, $\|\mathbf{w}\|^2 = 4.16$, $4.84 + 4.16 = 9$; $q(t) = 9 - 22t + 25t^2$, minimum 4.16 at 0.44, discriminant $-416$; $\|\mathbf{u} + \mathbf{v}\| = \sqrt{56} \approx 7.483 \le 8$; perpendicular pair $(2, 1), (-1, 2)$ gives 0 against 5, $2\mathbf{u}$ gives 10 and 10; transfer $\sqrt{37} \approx 6.08276$, £6,082.76 (the $\sigma_Y$ arrow at 60 degrees is $(2, 3.4641)$); quiz: eigenvalues $2.2$ and $-0.2$, $(1, -1)$ variance $-0.4$; $0.25 \le \tfrac13$; $\langle \mathbf{u}, 2\mathbf{u} \rangle = 18 = 3 \times 6$.
- l13: $\langle \mathbf{f}, \mathbf{m} \rangle = \langle \mathbf{m}, \mathbf{m} \rangle = 10$, $\beta = 1$ (covariance 2.5 over variance 2.5), residual $(1, 1, -1, -1)$; $\mathbf{f}_2 = (0.5, -0.5, 1)$, $\|\mathbf{f}_2\|^2 = 1.5$, $\mathbf{e}_2 = \tfrac1{\sqrt6}(1, -1, 2)$; $\mathbf{f}_3 = (-\tfrac23, \tfrac23, \tfrac23)$, $\|\mathbf{f}_3\| = \tfrac2{\sqrt3} \approx 1.1547$; trap $\mathbf{g} = (-1, 0.5, 0.5)$, $\langle \mathbf{g}, \mathbf{v}_1 \rangle = -0.5$; `np.linalg.qr` returns $-\mathbf{e}_1$ first (the other two columns agree); Legendre $\|1\|^2 = 2$, $\|x\|^2 = \langle x^2, 1 \rangle = \tfrac23$, $\langle x^2, x \rangle = 0$, $\|x^2 - \tfrac13\|^2 = \tfrac8{45}$, $\sqrt{45/8} \approx 2.3717$; transfer $\mathbf{m} - \tfrac{10}{14}\mathbf{f} = (-\tfrac37, -1, \tfrac97, \tfrac17)$.
- l13 code, "compute and report": the market and factor matrix gives $\mathbf{Q}$ `[[0.316228, 0.5], [-0.316228, 0.5], [0.632456, -0.5], [-0.632456, -0.5]]` ($\mathbf{m}/\sqrt{10}$ and the residual over 2). The orthonormality and span checks use the $5 \times 3$ matrix `[[1, 0, 2], [1, 1, 0], [0, 1, 1], [2, 0, 1], [1, 3, 0]]` (rank 3).
- l14: hook $\tfrac55(2, 1) = (2, 1)$, residual $(-1, 2)$, $\sqrt5 \approx 2.236$; $\dim U^\perp = 2$; $P_U(3, 0, 0) = (1, 1, 1)$, residual $(2, -1, -1)$, $\sqrt6 \approx 2.449$; $\|x^2 - c\|^2 = \tfrac25 - \tfrac43c + 2c^2$, minimum $\tfrac8{45} \approx 0.1778$ at $c = \tfrac13$, distance $\approx 0.4216$; trap $(1, 1, 0)$ at distance 1, sum $(2, 1, 0)$ at $\sqrt2 \approx 1.414$; transfer hedged variance $\tfrac44 = 1$ against $\tfrac{14}4 = 3.5$ unhedged.
- Review: $\begin{pmatrix}2&1\\1&1\end{pmatrix}^{-1} = \begin{pmatrix}1&-1\\-1&2\end{pmatrix}$, $\varphi_2 = 2y - x$; $\sqrt{14}\sqrt5 = \sqrt{70} \approx 8.367$ against 5; $|\mathrm{Cov}| \le 2 \times 3 = 6$; $(2, 1, 0) - (1, 0, 1) = (1, 1, -1)$; $(1, 2, 3)$ to $\operatorname{span}\{(1, 1, 1)\}$: residual $(-1, 0, 1)$, $\sqrt2$; $\|(1, 1)\|_{\mathbf{A}}^2 = 6$; $p'(0) = 3$ for $1 + 3x + 5x^2$.
- Homework: $\ell_2 = \tfrac{x(x - 1)}{2}$; $(2, -1)\begin{pmatrix}1&2\\0&3\end{pmatrix} = (2, 1)$, so $T'\psi = 2x + y$; $\int_0^1 (x - \tfrac12)^2 = \tfrac1{12} \approx 0.0833$; normal equations $a + \tfrac b2 = \tfrac13$, $\tfrac a2 + \tfrac b3 = \tfrac14$ give $x - \tfrac16$, and so does $\tfrac13 + \tfrac{\sqrt3}6 \cdot 2\sqrt3(x - \tfrac12)$; $0.98 \times \tfrac{20}{19} \approx 1.0316$; $1.03 \times \tfrac{19}{20} = 0.9785$. The seeded case was confirmed in Pyodide's NumPy 2.0.2 and in CPython's NumPy 2.5.3: `default_rng(7)`, true $\rho \approx 0.974916$, buggy ratio $\approx 1.026227$, ratio $1.052632 = \tfrac{20}{19}$.
- Homework code, "compute and report": the planted case is $\mathbf{m} + 0.5$ and $\mathbf{f} + 0.2$, giving `[[0.632456, 1.0], [-0.632456, 1.0], [1.264911, -1.0], [-1.264911, -1.0]]` (by the loop and by QR with signs fixed, scaled by $\sqrt n$). The three-factor case `[[1, 2, 0], [2, 0, 1], [-1, 1, 3], [0, -2, 1], [3, 1, -1]]` gives `[[0.0, 1.206045, -1.154701], [0.707107, -0.452267, 1.443376], [-1.414214, 0.753778, 0.866025], [-0.707107, -1.658312, -0.866025], [1.414214, 0.150756, -0.288675]]`, the same both ways.

### Code tests

Each imports NumPy, decides rank by `np.linalg.matrix_rank`, and returns lists rounded to 6 with `+ 0.0`. `codecheck.py` ran every solution and every starter in CPython and in Pyodide; every solution passes all its tests and every starter fails all of them.

- l10 `dual_basis(B)` (5 tests): the two bases, the $3 \times 3$ basis, `dual @ B` is the identity (boolean), a singular $\mathbf{B}$ raises `ValueError`. The starter returns $\mathbf{B}^T$: 0 of 5. No orthonormal basis is tested, since $\mathbf{B}^T$ would pass it.
- l13 `gram_schmidt(V)` (5 tests): the $3 \times 3$ example exactly, the market and factor, $\mathbf{Q}^T\mathbf{Q} = \mathbf{I}$, the span check $\mathbf{Q}\mathbf{Q}^T\mathbf{V} = \mathbf{V}$, a dependent input raises. The starter rescales columns: 0 of 5. `np.linalg.qr(V)[0]` fails test 1 (it has a `byKey` line). The brief's span check `matrix_rank(hstack([V, Q])) == k` would pass the starter, whose columns span the same space, so the span is checked by $\mathbf{Q}\mathbf{Q}^T\mathbf{V} = \mathbf{V}$, which also needs orthonormality.
- l14 `project(v, A)` and `complement_basis(A)` (6 tests): the trap's plane, a rank-deficient $\mathbf{A}$, a residual orthogonal to the columns, $|$complement$|$ of the trap's plane is $(0, 0, 1)$, dimensions add to 3 for the rank-1 matrix, an orthonormal complement orthogonal to a $4 \times 2$ $\mathbf{A}$. The starter adds single projections and returns an empty complement: 0 of 6. The one-column examples of the brief are left out of the hidden tests, since adding single projections is right for one column; one is the visible example.
- Homework `residual_factors(R)` (6 tests): the planted case, the three-factor case, $\tfrac1n\mathbf{Q}^T\mathbf{Q} = \mathbf{I}$, zero column means, a span check against the demeaned $\mathbf{R}$, and a cash column (constant) that raises. The starter is plain QR: 0 of 6.

## Departures from the brief

- l10: one `expression` per $\ell_k$ as asked, but spread out: $\ell_1$ on the lesson screen, $\ell_0$ in the quiz, $\ell_2$ in the homework. The independence-to-basis step is a quiz `choice`; the edge case $\{\mathbf{0}\}' = \{0\}$ is a quiz item.
- l11: the hook's "which could measure length" is the explore screen. The integral product $\int_0^1 fg$ appears in the generalise list, a quiz value and the quiz edge case; the "why the cross terms vanish" `choice` is a quiz item.
- l12: the triangle-inequality `choice` and the matrix with eigenvalue $-0.2$ are quiz items; the number-line carries the correlation bound on the generalise screen.
- l13: $\|\mathbf{f}_3\|$, the "why $\langle \mathbf{f}_k, \mathbf{e}_j \rangle = 0$" `choice`, independence of an orthonormal list, the dependent input and the extension corollary are quiz items. $\mathbf{Q}$ is a `matrix` canvas on the code screen.
- l14: "why the intersection is zero", "why the pieces are orthogonal", $(U^\perp)^\perp = U$, the trap's $\sqrt2$ and the extreme cases are quiz items. $P_U^2 = P_U$, kernel and image are stated on the code screen and in the summary, not graded. The space canvas shows the line $U$ as a one-vector span; the residual is drawn from the point $t(1, 1, 1)$ and follows the slider.
- Homework: the `order` item proves $(U^\perp)^\perp = U$, because the lessons' derive screens already order the Gram-Schmidt step and the minimisation proof. The longform asks for the true correlation behind 1.03 (0.9785) as well as the factor $\tfrac{n}{n-1}$.
- Ladder steps whose canvas kind changes are typed `problem`, as in level 2.
- No `course.json` change is proposed.

## Seeds and data conventions

One seed: `np.random.default_rng(7)` in the longform model answer only (not graded). Returns are demeaned daily percentages; covariance uses $\tfrac1n$; money in £; matrices are lists of rows, and a basis or factor set in code is given by its columns.

## Backlog

Three bullets under "Raised later (linear-maps level 3):" in `docs/BACKLOG-INBOX.md`: `vectors` labels on axis-aligned arrows land on the tick labels; `space` end labels of two arrows that end at one point overlap; and `vectors` `angles` and `lines`, like `segments`, are read from state only. Seen again but not raised: `vectors` `params.segments` ignored (level 1), the `table` widget cell `wrong[]` ids refused by the validator, and `space` cameras chosen by hand to avoid edge-on planes (level 1).

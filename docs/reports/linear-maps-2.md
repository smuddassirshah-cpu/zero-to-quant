# Report: linear-maps level 2, "Linear maps"

Course `linear-maps` (topic 1.10, strand pure), level 2, from `## Level 2` of `docs/briefs/linear-maps.md`. Lesson ids, names and objectives are those of `app/content/courses/linear-maps/course.json`; every lesson and item uses the skill `lx-maps`. Notation follows the brief and level 1: field $\mathbb{F}$, bold vectors, $\mathcal{L}(V, W)$, $\ker T$ and $\operatorname{im} T$ (with one sentence in l6 that Axler writes null and range, and that they are `elimination`'s $N(\mathbf{A})$ and $C(\mathbf{A})$), $[T]_{\mathcal{B}}^{\mathcal{C}}$, $[T]_{\mathcal{B}}$, $[\mathbf{v}]_{\mathcal{B}}$, matrices bold capitals, £ for money, proofs ending with $\blacksquare$. I read level 1's generators and report, `eigen` l13 for $\mathbf{A}$ and $\mathbf{X}$, and the `proof` course list: l6 cites `proof` l9-one-to-one-onto (written) for injective. No `analysis` lesson is cited at this level.

## Files written

All in `app/content/courses/linear-maps/`.

| File | Screens | Quiz / items | Canvases | Contents |
|---|---:|---:|---|---|
| `l5-linear-maps.json` | 11 | 4 | vectors (with `state.matrix`), table, plane | $T(2, 0) = (4, 6)$ (`expression`), drag $\mathbf{u}, \mathbf{v}$ under $[[2, 1], [3, -2]]$ with a caption from `image.u`, `image.v` (explore), the two rules and $\mathcal{L}(V, W)$ with $T(3, 1) = (7, 7)$, which maps are linear (`multi`, 8 maps), $T\mathbf{0} = \mathbf{0}$ (`order`), why the lemma's formula is well defined (`choice`), $2x + 3$ trap (`choice`, plane), uniqueness in the lemma (`order`), $D$ from basis values with zero map and identity as distractors, $T(0, 1) = (1, -2)$ (`generalise`), £30 value change (`numeric`) |
| `l6-kernel-and-image.json` | 12 | 4 | matrix (live cells, sliders), space, plane, table | zero-exposure book $(-1, 1, -1)$ (`expression`), $y = 2$ book (explore), $\dim \ker E = 1$, kernel is a subspace (`order` with `same`), image step (`choice`), kernel of $(x + y, y + z)$ with the coset line (`expression`, space), $\ker D$ and $\operatorname{im} D$ (`choice`), kernel-in-$W$ trap (`choice`, space), Axler 3.15 forward and backward (`order` each), circular proof (tap rows), two books with one exposure (`choice`) |
| `l7-rank-nullity.json` | 12 | 4 | table, vectors (matrix sliders), matrix | dimension table $(4, 1, 3)$, $(3, 1, 2)$, $(2, 2, 0)$ (`table`), squash the plane (explore), $\mathbb{R}^5 \to \mathbb{R}^3$ never injective, extension reason (`choice`), spanning (`order`), independence (`order`), full proof, 8 lines (`order`), images of any basis (tap rows), $\dim \ker \mathbf{F} = 2$, $\mathbf{B}$ nullity trap (wrong 1 and 2), `rank_nullity` and `kernel_basis` code, factor-neutral portfolios (`choice`) |
| `l8-maps-as-matrices.json` | 11 | 4 | table, vectors (matrix sliders, `state.matrix`, `state.basis`), plane, matrix | $[D]$ filled column by column (`table`, 12 cells), column $k$ is $T\mathbf{e}_k$ (explore), $[S]$ (`expression`, `pmatrix`), $[S](3, 2, 1) = (6, 4, 1)$, $[D \circ S] = [D][S]$ (`choice`), rows give the transpose (trap), $[T\mathbf{v}]_{\mathcal{C}} = [T][\mathbf{v}]_{\mathcal{B}}$ (`order`), $\mathbf{X}^{-1}\mathbf{A}\mathbf{X} = \operatorname{diag}(5, 2)$ (`expression`), $[(5, 1)] = (3, 2)$ in the skewed grid, `coords` and `matrix_in_basis` code, market variance 8 (`numeric`) |
| `l9-invertible-and-isomorphic.json` | 12 | 4 | matrix (live cells, sliders), table, space, plane | bootstrap $(0.97, 0.94, 0.91)$ (`table`), the doubled bond leaves $d_3$ free (explore), unique inverse (`order`), inverse is linear (`order`), injective and surjective give an inverse (`choice`), Axler 3.59 forward (`order`, `same`) and backward (`order`, `same`), injective is enough when dimensions match (`choice`), $(x, y, 0)$ trap (space), multiplication by $x$ on $\mathcal{P}(\mathbb{R})$ (`choice`), `invert_if_iso` code against the determinant test, a line of consistent curves (`numeric`) |
| `review-2.json` | | 9 | | difficulties 2, 2, 3, 2, 2, 3, 3, 4, 3; lessons l5, l6, l7, l8, l9, l5, l8, l6/l9, l7 (linearity check, kernel vector in $\mathbb{R}^4$, nullity of a $4 \times 6$ rank 3 with the $m - r$ trap, column 3 of $xp'$, isomorphic pair, $T(1, 0)$ from a basis, change of basis $\mathbf{P}^{-1}\mathbf{A}\mathbf{P}$ with $\mathbf{P}\mathbf{A}\mathbf{P}^{-1}$ as a distractor, injective test, no solution) |
| `homework-2.json` | | 9 | matrix, table | difficulties 4, 4, 4, 3, 4, 3, 5, 3, 5; injective gives surjective when dimensions match (`order`), $[D]$ in $(1, 1 + x, 1 + x + x^2)$ (`expression`), `solution_set` code, planted system (`numeric`), "every map is an isomorphism" flaw (tap rows), kernel of the trace, $\dim\{T : T(1, 1, 1) = \mathbf{0}\} = 4$, $\operatorname{diag}(3, -1)$, rank-nullity `longform` (10 one-point rubric lines, full model answer) |

Generators and checks are in `/tmp/claude-0/-home-user-zero-to-quant/7b2c22fa-9eb5-56f2-a434-3e990ba10710/scratchpad/linear-maps-2/` (`common.py`, `gen_l5.py` to `gen_l9.py`, `gen_sets.py`, `checks.py`, `checks2.py`, `voice.py`). Edit the generators and rerun them rather than the JSON. The shared helper now shuffles `choice` options by default; ordered option lists pass `shuffle=False`.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 364 warnings, none in a level 2 file (the only linear-maps line is the course's "not yet written: 10 of 19 lessons" warning for levels 3 and 4). No `analysis` errors were reported in any run.

## Playthrough

All with `--local-cdn /tmp/claude-0/-home-user-zero-to-quant/7b2c22fa-9eb5-56f2-a434-3e990ba10710/scratchpad/pkgs`, with `--shots --mobile --why` while authoring. I looked at the screenshots at 1280 px and 390 px.

| Target | Result |
|---|---|
| `--lesson linear-maps/l5-linear-maps` | ok, 15 checks, quiz 4/4 |
| `--lesson linear-maps/l6-kernel-and-image` | ok, 16 checks, quiz 4/4 |
| `--lesson linear-maps/l7-rank-nullity` | ok, 16 checks, quiz 4/4 (code solution passes 12 tests in Pyodide) |
| `--lesson linear-maps/l8-maps-as-matrices` | ok, 15 checks, quiz 4/4 (code solution passes 8 tests in Pyodide) |
| `--lesson linear-maps/l9-invertible-and-isomorphic` | ok, 16 checks, quiz 4/4 (code solution passes 6 tests in Pyodide) |
| `--set linear-maps/review-2` | ok, 9 of 9 recorded |
| `--set linear-maps/homework-2` | ok, 9 of 9 right, 40 of 40 marks (code passes 8 tests in Pyodide) |

No run flaked. Fixes made after the screenshots:
- l5: the matrix overlay's basis arrows were labelled $\mathbf{b}_1$, $\mathbf{b}_2$; now $T\mathbf{e}_1$, $T\mathbf{e}_2$ through `basisLabels`, and the hook's Why? names the image grid. Trap labels moved off the left edge and off the dashed line.
- l6: the kernel and coset lines sat almost on top of each other, and the kernel vector's label gave away the answer; camera az 50 el 35, label $\mathbf{k}$.
- l7: order cards ran past the 390 px column because of long inline sums; the proof lines now use $\sum$ notation. The hook gained a table canvas recalling each kernel and image.
- l8: the curve label $(x + 1)^2$ was cut at the left edge; raw `pmatrix` LaTeX showed on the Accepted line (now plain `[[...]]` forms).
- l9: the bootstrap table's input column was cut at 390 px; the table is now two columns. Plane and space labels moved apart.
- Every `choice` now shuffles, so the correct option is no longer always first.

## Proofs and the widget that grades each step

| Proof | Where | Widget |
|---|---|---|
| $T\mathbf{0} = \mathbf{0}$ | l5 | `order`, 4 lines; distractor "$T$ is a matrix" |
| Linear map lemma, existence (well defined) | l5 | `choice` (unique coordinates, l4; distractors independent targets, circular linearity, finite dimension) |
| Linear map lemma, uniqueness | l5 derive | `order`, 5 lines; distractor "the $\mathbf{w}_k$ are a basis" |
| $f(x) = 2x + 3$ is not linear | l5 trap | `choice` on a plane |
| $\ker T$ is a subspace | l6 | `order`, 4 lines, three checks in `same`; distractor $\mathbf{0}_W \in \ker T$ |
| $\operatorname{im} T$ is a subspace | l6, l6 quiz | `choice` for the sum step; quiz `choice` for $\mathbf{0} = T\mathbf{0}$ |
| Axler 3.15, injective gives $\ker T = \{\mathbf{0}\}$ | l6 | `order`, 4 lines; distractor "the kernel is empty" |
| Axler 3.15, $\ker T = \{\mathbf{0}\}$ gives injective | l6 derive | `order`, 4 lines; distractor "both in $\ker T$"; then tap the circular row of a table |
| Rank-nullity step 2 (extension) | l7 | `choice` (Axler 2.31) |
| Rank-nullity step 4 (spanning) | l7 | `order`, 5 lines; circular distractor; quiz `choice` for why $T\mathbf{u}_i = \mathbf{0}$ |
| Rank-nullity step 5 (independence) | l7 | `order`, 6 lines; distractor "$T$ is injective" |
| Rank-nullity, whole skeleton | l7 derive | `order`, 8 lines; distractor "non-zero vectors are independent" |
| Images of any basis form a basis (false) | l7 | tap the flawed row of a table |
| Consequences of rank-nullity | l7, l7 quiz | `choice` (smaller codomain: not injective); quiz `choice` (larger codomain: not surjective) |
| $[T\mathbf{v}]_{\mathcal{C}} = [T][\mathbf{v}]_{\mathcal{B}}$ | l8 derive | `order`, 4 lines; distractor with the vector on the left |
| Matrix of a composition | l8 | `choice` |
| Inverse is unique | l9 | `order`, 4 lines; distractor "agree on a basis" |
| Inverse is linear | l9 | `order`, 4 lines; distractor "inverse matrix" |
| Invertible gives injective | l9 quiz | `order`, 3 lines, circular distractor |
| Injective and surjective give an inverse | l9 | `choice` |
| Axler 3.59 forward | l9 | `order`, 4 lines, `same` on the two facts; distractor counting vectors |
| Axler 3.59 backward | l9 derive | `order`, 5 lines, `same` on the two properties; distractor "$T$ keeps independence"; quiz `choice` for the injectivity reason |
| Equal dimension: injective is enough | l9, homework | `choice` in l9; homework `order`, 5 lines, distractor "injective is always surjective" |
| Every map between equal dimensions is an isomorphism (false) | homework | tap the flawed row |
| Rank-nullity | homework | `longform`, 10 one-point rubric lines (kernel basis 2, extension with reason 2, spanning 2, independence 3, count 1) and full model answer |

## Numbers, each computed twice

First pass: `checks.py`, exact fractions and integer rank by NumPy (92 checks, all OK; two of my own hand values in the checker were wrong and were corrected against the computation: $E(-1, 1, 1) = (-0.8, 0.4)$, and $S(1 + x + x^2) = 3 + 3x + x^2$, coordinates $(0, 2, 1)$ in $(1, 1 + x, 1 + x + x^2)$; neither number appears in the content). Second pass: `checks2.py` reads the written JSON back, lists every graded answer for a by-hand recheck, and runs each code solution and starter against its hidden tests in CPython; the playthrough ran them again in Pyodide. No stated number failed its double check.

- l5: $T(x, y) = (2x + y, 3x - 2y)$; $T(1, 1) = (3, 1)$, $T(1, -1) = (1, 5)$; $T(2, 0) = (4, 6)$ and $T(3, 1) = 2(3, 1) + (1, 5) = (7, 7)$, both also by the matrix; $T(0, 1) = \tfrac12(3, 1) - \tfrac12(1, 5) = (1, -2)$. Distractors $(6, 2)$, $(2, 10)$, $(10, 8)$, $(2, -4)$. $f(1 + 1) = 7$, $f(1) + f(1) = 10$. Transfer: $100 \times 12 + 50 \times 30 = £2,700$; $100(0.40) + 50(-0.20) = £30$; distractors £2,730, £50, 0.2. Quiz: $T(4, -1) = (7, 14)$; $S(3 + 2x + x^2) = 6 + 4x + x^2$.
- l6: $E = \begin{pmatrix}1 & 0.6 & -0.4\\ 0 & 0.2 & 0.2\end{pmatrix}$, rank 2, $E(-1, 1, -1) = E(-2, 2, -2) = (0, 0)$; distractors $E(-1, 1, 1) = (-0.8, 0.4)$, $E(1, 1, 1) = (1.2, 0.4)$. $(x + y, y + z)$: kernel $(1, -1, 1)$, rank 2, every $(1 + t, -t, t) \mapsto (1, 0)$. $E(10, 2, 3) = E(5, 7, -2) = (10, 1)$, difference $5(-1, 1, -1)$. $E(1, 0, 0) + E(0, 1, 0) = (1.6, 0.2)$. Quiz: kernel of $(x - 2y, 2x - 4y)$ is spanned by $(2, 1)$.
- l7: $(4, 1, 3)$, $(3, 1, 2)$, $(2, 2, 0)$. $\mathbf{F}$ rank 3, nullity 2; $\mathbf{B}$ rank 2 (row 3 = row 1 + row 2), nullity 3, distractors $m - r = 1$, $n - m = 2$; $D$'s $3 \times 4$ matrix rank 3, nullity 1. Explore: rows $(1, 2), (1, 2)$ send $(2, -1)$ to $\mathbf{0}$. Quiz: $p \mapsto (p(0), p(1))$ on $\mathcal{P}_4$ has kernel dimension $5 - 2 = 3$ (basis $x - x^2, x - x^3, x - x^4$); an injective map $\mathbb{R}^3 \to \mathbb{R}^5$ has rank 3.
- l8: $[D] = \begin{pmatrix}0&1&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$; $[S] = \begin{pmatrix}1&1&1\\0&1&2\\0&0&1\end{pmatrix}$ (columns checked against $S1$, $Sx$, $Sx^2$); $[S](3, 2, 1) = (6, 4, 1)$, transpose distractor $(3, 5, 8)$; $[D][S] = \begin{pmatrix}0&1&2\\0&0&2\end{pmatrix}$ (columns checked against $D(S x^k)$); $\mathbf{X}^{-1}\mathbf{A}\mathbf{X} = \operatorname{diag}(5, 2)$, $\mathbf{A}(1, 1) = (5, 5)$, $\mathbf{A}(1, -2) = (2, -4)$; $[(5, 1)] = (3, 2)$; $\mathbf{P}^{-1}\boldsymbol{\Sigma}\mathbf{P} = \operatorname{diag}(4, 2)$, $\mathbf{P}^T\boldsymbol{\Sigma}\mathbf{P} = \operatorname{diag}(8, 4)$, market variance 8, distractors 4 and 6. Quiz: $[(x + 2y, 3y)] = \begin{pmatrix}1&2\\0&3\end{pmatrix}$; $[D]$ from $\mathcal{P}_2$ to $\mathcal{P}_1$ is $\begin{pmatrix}0&1&0\\0&0&2\end{pmatrix}$.
- l8 code, "compute and report": the shift in the basis $(1, 1 + x, 1 + x + x^2)$ is $\begin{pmatrix}1&1&0\\0&1&2\\0&0&1\end{pmatrix}$. The basis $(1, x - 1, (x - 1)^2)$ would give the standard matrix back, because the shift commutes with translation, so it cannot be a test (the starter returning `A` would pass it).
- l9: $d_1 = 101.85/105 = 0.97$; $105d_2 = 103.55 - 4.85 = 98.70$, $d_2 = 0.94$; $105d_3 = 105.10 - 4.85 - 4.70 = 95.55$, $d_3 = 0.91$ (exact fractions). Distractors $103.55/105 = 0.9862$, $105.10/105 = 1.001$. The bond $(10, 210, 0)$ is twice bond 2 and prices at $9.70 + 197.40 = £207.10$; $\mathbf{C}'$ has rank 2 and nullity 1, kernel $(0, 0, 1)$. $0.1\mathbf{I}_{10}$: determinant $10^{-10}$ (NumPy: 9.999999999999996e-11), condition number 1, `matrix_rank` 10. $\dim \mathcal{L}(\mathbb{R}^3, \mathbb{R}^2) = 6$. $\mathbf{C}^{-1}$ rounded: rows $(0.009524, 0, 0)$, $(-0.000454, 0.009524, 0)$, $(-0.000432, -0.000454, 0.009524)$.
- Review: $T(1, -1, 2, -2) = (0, 0)$, $T(1, -1, 2, 2) = (0, 4)$; nullity $6 - 3 = 3$; $T x^2 = 2x^2$ for $Tp = xp'$; $\dim \mathcal{P}_5 = \dim \mathbb{R}^{2 \times 3} = 6$; $T(1, 0) = (1, 0, 1) - 2(0, 1, 1) = (1, -2, -1)$; $\mathbf{P}^{-1}\mathbf{A}\mathbf{P} = \begin{pmatrix}2&0\\1&3\end{pmatrix}$ and $\mathbf{P}\mathbf{A}\mathbf{P}^{-1} = \begin{pmatrix}2&0\\-1&3\end{pmatrix}$ for $\mathbf{A} = \operatorname{diag}(2, 3)$, $\mathbf{P} = \begin{pmatrix}1&0\\1&1\end{pmatrix}$; $(x - z, y + z, x + y)$ has kernel $(1, -1, 1)$ and rank 2.
- Homework (compute and report): $[D]_{\mathcal{B}}$ in $\mathcal{B} = (1, 1 + x, 1 + x + x^2)$ is $\begin{pmatrix}0&1&-1\\0&0&2\\0&0&0\end{pmatrix}$, since $1 + 2x = -1 + 2(1 + x)$. Planted $\mathbf{H} = \begin{pmatrix}1&2&0&1\\0&0&1&1\\1&2&1&2\end{pmatrix}$ has rank 2; $\mathbf{b} = (3, 2, 5)$ is consistent with $\mathbf{x}_p = (3, 0, 2, 0)$, solutions of dimension 2; $(3, 2, 4)$ raises the augmented rank to 3. Trace kernel $4 - 1 = 3$. $\{T \in \mathcal{L}(\mathbb{R}^3, \mathbb{R}^2) : T(1, 1, 1) = \mathbf{0}\}$ has dimension $6 - 2 = 4$. $\begin{pmatrix}1&2\\2&1\end{pmatrix}$ in $(1, 1), (1, -1)$ is $\operatorname{diag}(3, -1)$.

### Code tests, with expected values

Each imports NumPy and decides rank by `np.linalg.matrix_rank`, never a determinant. Results are Python lists, `int`s and booleans.

- l7 `rank_nullity(A)` and `kernel_basis(A)` (12 tests): $\mathbf{B} \to [2, 3]$, $\mathbf{F} \to [3, 2]$, $D \to [3, 1]$, $\mathbf{0}_{2 \times 3} \to [0, 3]$, $\mathbf{I}_4 \to [4, 0]$ with a $4 \times 0$ kernel; kernel shapes $[5, 3]$, $[5, 2]$, $[4, 1]$, $[3, 3]$; $\mathbf{A}\mathbf{K} = \mathbf{0}$ for $\mathbf{B}$, $\mathbf{F}$, $D$; $\operatorname{rank} \mathbf{K} = 3$ for $\mathbf{B}$. The starter returns rows minus rank and `kernel_basis` returns `None`: it fails all 12.
- l8 `coords(v, B)` and `matrix_in_basis(A, B)` (8 tests): `eigen` l13 pair $\to$ `[[5, 0], [0, 2]]`; $\boldsymbol{\Sigma}$ with market and spread $\to$ `[[4, 0], [0, 2]]`; $\mathbf{A}$ with $(1, 1), (1, -1)$ $\to$ `[[5, 1], [0, 2]]`; the shift in $(1, 1 + x, 1 + x + x^2)$ $\to$ `[[1, 1, 0], [0, 1, 2], [0, 0, 1]]`; `coords([5, 1], ...)` $\to$ `[3, 2]`; `coords([3, 3, 1], Bb)` $\to$ `[0, 2, 1]`; two singular bases raise `ValueError`. The starter returns `v` and `A`: it fails all 8.
- l9 `invert_if_iso(A)` (6 tests): $\mathbf{C}$ gives its rounded inverse (`isclose`, absolute 0.000001); $\mathbf{C}'$, a $2 \times 3$ and $\begin{pmatrix}1&2\\2&4\end{pmatrix}$ give `None`; $0.1\mathbf{I}_{10}$ gives $10\mathbf{I}_{10}$; $\begin{pmatrix}2&1\\1&1\end{pmatrix}$ gives `[[1, -1], [-1, 2]]`. The starter is the brief's determinant test: it fails the $2 \times 3$ case (no determinant) and $0.1\mathbf{I}$, and passes the other 4.
- Homework `solution_set(A, b)` (8 tests): $\mathbf{H}\mathbf{x}_p = (3, 2, 5)$, kernel shape $[4, 2]$, $\mathbf{H}\mathbf{K} = \mathbf{0}$ with rank 2, $(3, 2, 4)$ gives `None`; $\mathbf{F}$ with $(1, 1, 1)$: solved, kernel $[5, 2]$; $\mathbf{B}$ with $(1, 1, 2)$: solved, kernel $[5, 3]$; $\mathbf{B}$ with $(1, 1, 1)$ gives `None`; $\mathbf{C}$ with the bond prices gives $(0.97, 0.94, 0.91)$ and a $3 \times 0$ kernel. The starter returns zeros and an empty kernel: it fails all 8.

## Departures from the brief

- Ladder steps are typed `problem` where the canvas kind changes, to avoid the validator's "ladder reuses the previous canvas kind" warning; the lesson shape is unchanged.
- l5 has 11 screens; the edge case (zero map, identity, $D$ with no matrix) is one `choice` screen.
- l6: the image-is-a-subspace proof grades the sum step on the screen and the zero step in the quiz; scaling is in the explanation. $\ker D$ and $\operatorname{im} D$ are one `choice`, with surjective named in its explanation.
- l7: the "why $T\mathbf{u}_i = \mathbf{0}$" `choice` and "a map into a larger space is not surjective" are quiz items. The transfer is a `choice` (rank fell, nullity rose to 3) rather than a second nullity number, since the trap already asks for $\mathbf{B}$'s nullity. The brief fixed only `rank_nullity`'s starter; `kernel_basis` starts as `None`, so every test fails on the starter.
- l8: $\mathbf{P}\mathbf{A}\mathbf{P}^{-1}$ against $\mathbf{P}^{-1}\mathbf{A}\mathbf{P}$ and the identity with two bases are quiz items; the trap screen is the rows-give-the-transpose `choice`. The `coords` starter returns `v` as well as `matrix_in_basis` returning `A`.
- l9: the order for "invertible gives injective" is a quiz item and the lesson grades the converse by `choice`. In the backward direction of Axler 3.59 the reasons sit in the `order` lines; the injectivity reason is also a quiz `choice`, and the surjectivity reason is not graded separately. $\dim \mathcal{L}(\mathbb{R}^3, \mathbb{R}^2) = 6$ is a quiz `numeric`. The determinant discussion is the code screen's prose. As the brief asks, the starter uses the determinant test, so it passes 4 of the 6 hidden tests; this departs from the general rule that every hidden test fails on the starter.
- Homework: the inverse-is-linear `order` is in l9, so the homework `order` item proves "injective gives surjective when $\dim V = \dim W$". Review has 9 items and homework 9.
- No `course.json` change is proposed.

## Seeds and data conventions

No randomness. Money in £; covariance in $\%^2$; vectors are Python lists, matrices lists of rows, and a basis `B` in code is given by its columns. Matrix answers are `pmatrix` with a plain `[[...]]` accept form.

## Backlog

Three bullets under "Raised later (linear-maps level 2):" in `docs/BACKLOG-INBOX.md`: the matrix overlay of `vectors` cannot be hidden, matrix `accept` examples print raw LaTeX, and `space` line spans ignore `labelAt`. Seen again but not raised (already in the inbox): long inline maths in `order` cards runs past the 390 px column (proof level 3); worked around with $\sum$ notation.

# Report: linear-maps level 1, "Vector spaces"

Course `linear-maps` (topic 1.10, strand pure), level 1, from `## Level 1` of `docs/briefs/linear-maps.md`. Lesson ids, names and objectives are those of `app/content/courses/linear-maps/course.json`; every lesson and item uses the skill `lx-spaces`. Notation follows the brief: field $\mathbb{F}$, bold vectors, lists in brackets, $\mathcal{P}_m(\mathbb{F})$, $\mathbb{R}^{S}$, $\operatorname{span}$, $\dim$, $[\mathbf{v}]_{\mathcal{B}}$; scalars are $\lambda, \mu$; proofs end with $\blacksquare$ as in the `proof` course. I read `proof` l10 to l12 (the generators of `docs/reports/proof-3.md`) for voice and the order-widget pattern, and `elimination` l5, l7 and l12 for shared numbers. `analysis` l15-epsilon-delta is not written: l2 cites it by id only, for "sums and multiples of continuous functions are continuous". The `proof` course is now written, so homework-1 cites `proof` l12-contradiction by id for the contradiction method.

## Files written

All in `app/content/courses/linear-maps/`.

| File | Screens | Quiz / items | Canvases | Contents |
|---|---:|---:|---|---|
| `l1-axioms.json` | 12 | 4 | vectors, table, plane | fully invested sum (0.9, 1.1) (`expression`), drag both heads on $x + y = 1$ (explore), the eight conditions and why addition must map into $V$, $\mathcal{P}_2$ against degree exactly 2 (`table` of yes/no), $(f + g)(0.5)$ in $\mathbb{R}^{[0,1]}$ and P&L as $\mathbb{R}^{252}$, $\lambda(a, b) = (\lambda a, 0)$ fails $1\mathbf{v} = \mathbf{v}$, fully invested line trap (`multi`), positive reals with zero vector 1, unique zero (`order`), $0\mathbf{v} = \mathbf{0}$ (`order`), its line-2 reason (`choice`), quant sets transfer (`multi`) |
| `l2-subspaces-and-sums.json` | 12 | 4 | vectors, table, space, plane | union of the axes (`drag-point` with `lockTo`, then explore), the subspace test, plane $x_1 + 2x_2 + 3x_3 = 0$ (`order` with `same`), function subspaces (`multi`), $U + W$ as the smallest subspace (`choice`), Axler 1.45 (`order`), Axler 1.46 (`order`), three-subspace trap (`choice`) and its third piece $(0, -1, -1)$ (`expression`), even part of $e^x$ (`expression`), market and zero-sum split (`expression`) |
| `l3-span-and-independence.json` | 12 | 4 | matrix (live cells and sliders), space | zero-return weights $(1, -1, -1)$, scaled $(2, -2, -2)$ (explore), (A, B, C) independent, dependence lemma (`order`), the exchange (`manipulate` on column matrices, refused steps), Axler 2.22 (`order`, 6 lines), why a $\mathbf{w}$ goes (`choice`), consequences (`multi`), no-parallel-pair trap, $\mathcal{P}(\mathbb{F})$ edge case, `first_dependent` code, 500 stocks over 252 days |
| `l4-bases-and-dimension.json` | 12 | 4 | plane (sliders), matrix, table | coordinates $(6, 4, 1)$ (`expression`), uniqueness by sliders (explore), coordinates unique (`order`), Axler 2.34 (`order` with `same`), why we may swap (`choice`), dimensions 4, 4, 6, 3, 0 (`table`), extension keep/skip (`table`), independent list of length $n$ (`choice`), $\dim(U + W) = 3$ (`generalise`), rank-2 trap (`numeric`, wrong 3), `dim_span` and `extend_to_basis` code, yield-curve rank 2 |
| `review-1.json` | | 8 | | difficulties 3, 2, 2, 4, 2, 3, 3, 3; order l1, l2, l3, l4, l1, l2, l3, l4 (axiom that fails, subspace check, first dependent vector, dimension count, positive reals, direct sum, exchange justification, coordinate vector) |
| `homework-1.json` | | 9 | table | difficulties 4, 5, 3, 4, 4, 3, 3, 4, 5; spanning list of length $\dim V$ (`order`), union of subspaces by contradiction (`order` with `same`), function subspaces (`multi`), `basis_of_span` code, $\dim(U \cap W) = 1$, $[(2, 3, 4)]_{\mathcal{B}} = (-1, 4, 3)$, which law $(xy)^{\lambda} = x^{\lambda}y^{\lambda}$ is, flawed direct-sum proof (tap rows), $\dim(U + W)$ `longform` (10 one-point rubric lines, full model answer) |

Generators and checks are in the scratchpad folder `/tmp/claude-0/-home-user-zero-to-quant/7b2c22fa-9eb5-56f2-a434-3e990ba10710/scratchpad/linear-maps-1/` (`common.py`, `gen_l1.py` to `gen_l4.py`, `gen_sets.py`, `checks.py`, `checks2.py`, `voice.py`). Edit the generators and rerun them rather than the JSON.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 364 warnings, none in a linear-maps file (the only linear-maps line is the course's "not yet written: 15 of 19 lessons" warning for levels 2 to 4). No analysis errors were reported in any run.

## Playthrough

All with `--local-cdn /tmp/claude-0/-home-user-zero-to-quant/7b2c22fa-9eb5-56f2-a434-3e990ba10710/scratchpad/pkgs`, with `--shots --mobile --why` while authoring. I looked at the screenshots of every screen at 1280 px and 390 px, and at every set item.

| Target | Result |
|---|---|
| `--lesson linear-maps/l1-axioms` | ok, 16 checks, quiz 4/4 |
| `--lesson linear-maps/l2-subspaces-and-sums` | ok, 16 checks, quiz 4/4 |
| `--lesson linear-maps/l3-span-and-independence` | ok, 16 checks, quiz 4/4 (code solution passes 8 tests in Pyodide) |
| `--lesson linear-maps/l4-bases-and-dimension` | ok, 16 checks, quiz 4/4 (code solution passes 10 tests in Pyodide) |
| `--set linear-maps/review-1` | ok, 8 of 8 recorded |
| `--set linear-maps/homework-1` | ok, 9 of 9 right, 40 of 40 marks (code passes 8 tests in Pyodide) |

No run flaked. Fixes made after the screenshots:
- l1 hook, explore and trap: the dashed line $x + y = 1$ was missing because `segments` were in `params`; the `vectors` canvas reads them from `state` only (backlog bullet).
- l1 eight-conditions table scrolled sideways at 390 px; shorter statements, a "Statement" header and `compact`.
- l1 function plane and odd-scaling arrow: labels sat on tick labels; moved with `labelAt`, `labelSide` and `labelPos: "mid"`.
- l2 plane $x_1 + 2x_2 + 3x_3 = 0$ and l2 transfer plane $W$ were edge-on at the opening camera; l3 span(A, B) was face-on, then straight down an axis. Cameras now az 30 el 30, az -20 el 25 and az 150 el 25 (backlog bullet).
- l4 hook: the long curve label crossed the line $x = 1$; the curves are labelled $p$ and $q$ and the prose names $q$.
- l4 dimension screen: a canvas table and a widget table repeated the same column; merged into one widget table with a basis column, and the canvas now plots $x - 1$, $x^2 - 1$, $x^3 - 1$ through $(1, 0)$.
- l4 code starter: comment lines over 54 characters were wrapped.

## Proofs and the widget that grades each step

| Proof | Where | Widget |
|---|---|---|
| The additive identity is unique | l1 | `order`, 3 lines; distractor "both are $(0, \dots, 0)$" |
| $0\mathbf{v} = \mathbf{0}$ | l1 | `order`, 4 lines, distractor "zero times anything is zero"; then `choice` for line 2 (distributive; distractors commutativity and $0 + 0 = 0$ in $\mathbb{F}$) |
| $(-1)\mathbf{v} = -\mathbf{v}$ | l1 quiz | `order`, 4 lines, distractor from number arithmetic |
| Which condition fails ($\lambda(a, b) = (\lambda a, 0)$; $\lambda(a, b) = (\lambda a, b)$) | l1, review | `choice` |
| Degree exactly 2 is not a space | l1 | `table` of yes/no cells (cell-keyed `byKey`) |
| $x_1 + 2x_2 + 3x_3 = 0$ is a subspace | l2 | `order` with the three checks in `same`, distractor "one pair passes" |
| Why the other conditions come free | l2 | `choice` |
| $x_1 + 2x_2 + 3x_3 = 4$ fails at $\mathbf{0}$ | l2 quiz | `choice` |
| Direct exactly when $\mathbf{0}$ is written one way (Axler 1.45, hard direction) | l2 | `order`, 5 lines, distractor "one way only" |
| $U \cap W = \{\mathbf{0}\}$ gives a direct sum (Axler 1.46) | l2 | `order`, 4 lines, sign-slip distractor; reason $-\mathbf{w} \in W$ as a quiz `choice` |
| Pairwise zero intersections are not enough | l2 trap, homework | `choice`, then `expression` $(0, -1, -1)$; homework: tap the flawed row of a `table` |
| Union of subspaces | l2 quiz, homework | quiz `choice`; homework `order` (6 lines, the two cases in `same`, distractor "in both") |
| Linear dependence lemma (Axler 2.19) | l3 | `order`, 5 lines, distractor "smallest index" |
| The exchange | l3 | `manipulate` with refused steps (remove $\mathbf{u}_1$, $\mathbf{u}_2$, $\mathbf{e}_1$, $\mathbf{e}_3$ too early) |
| Independent never longer than spanning (Axler 2.22) | l3 | `order`, 6 lines, distractor "remove $\mathbf{u}_k$ again"; `choice` for "the removed vector is a $\mathbf{w}$" |
| Why the list still spans after a removal | review | `choice` |
| Coordinates are unique | l4 | `order`, 4 lines, distractor "spanning kills the weights" |
| Every basis has the same length (Axler 2.34) | l4 | `order` with `same`, distractor "both span"; `choice` for why we may swap |
| Independent of length $n$ is a basis | l4 | `choice` with its justification |
| Spanning of length $\dim V$ is a basis | homework | `order`, 5 lines, distractor "spanning lists are independent" |
| $\dim(U + W)$ formula | homework | `longform`, 10-point rubric (set-up 3, spanning 2, independence 3, count 2) and full model answer |

## Numbers, each computed twice

First pass: `checks.py`, exact fractions and integer rank by NumPy (45 checks, all OK). Second pass: `checks2.py` reads the written JSON back, lists every graded answer for a by-hand recheck, and runs each code solution and starter against its hidden tests in CPython; the playthrough ran them again in Pyodide. No number failed its double check.

- l1: $(0.6, 0.4) + (0.3, 0.7) = (0.9, 1.1)$, total 2. $(x^2 + x) + (-x^2 + 1) = x + 1$. $(f + g)(0.5) = 0.25 + 0.5 = 0.75$ for $f = x^2$, $g = 1 - x$. $1(2, 3) = (2, 0)$ under $\lambda(a, b) = (\lambda a, 0)$; the other three scaling conditions hold on a grid of vectors and scalars. Positive reals: $2 \oplus 3 = 6$, $3 \odot 2 = 8$, $0.5 \odot 4 = 2$, zero vector 1, inverse of 2 is $\tfrac12$.
- l2: $(1, 1, -1)$, $(3, 0, -1)$ and their sum $(4, 1, -2)$ satisfy $x_1 + 2x_2 + 3x_3 = 0$. $U_1, U_2, U_3$: pairwise intersections 0 by rank, sum of rank 3, dimensions $2 + 1 + 1 = 4$; $(0, 1, 0) + (0, 0, 1) + (0, -1, -1) = \mathbf{0}$. Split $(0.03, -0.01, 0.01) = (0.01, 0.01, 0.01) + (0.02, -0.02, 0)$, the second summing to 0. $\cosh x + \sinh x = e^x$ at nine points. $(p + q)(0) = 2$ for $p = 1 + x/2$, $q = 1 - x^2$.
- l3: A + B $-$ C $-$ D $= \mathbf{0}$ for A $= (1, 0, 2)$, B $= (0, 1, 1)$, C $= (1, 1, 0)$, D $= (0, 0, 3)$, so weights $(1, -1, -1)$, scaled $(2, -2, -2)$, portfolio $(1, 1, -1, -1)$; with $b = c = d = 0$ the portfolio column reads $(1, 0, 2)$. (A, B, C) has rank 3; D $=$ A + B $-$ C. Exchange: $\mathbf{e}_2 = \mathbf{u}_1 - \mathbf{e}_1$; $\mathbf{u}_2 \notin \operatorname{span}(\mathbf{u}_1)$, $\mathbf{e}_1 \notin \operatorname{span}(\mathbf{u}_1, \mathbf{u}_2)$; $\mathbf{e}_3 = -\mathbf{u}_1 + \mathbf{u}_2 + \mathbf{e}_1$. $(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 1)$ has rank 3. Transfer: $\boldsymbol{\Sigma} = \tfrac{1}{251}\mathbf{X}^T\mathbf{X}$ for 252 days.
- l4: $6 + 4(x - 1) + (x - 1)^2 = x^2 + 2x + 3$; the starting sliders $(3, 2, 1)$ draw $x^2 + 2 = p - 1$. $(x - 1, x^2 - 1, x^3 - 1)$ has rank 3 and each vanishes at 1. Extension in $\mathbb{R}^4$ keeps $\mathbf{e}_1, \mathbf{e}_2$; in $\mathbb{R}^3$ it keeps $\mathbf{e}_1$ only. $U \cap W = \operatorname{span}\{(1, 1, 1, 1)\}$, $\dim(U + W) = 2 + 2 - 1 = 3$. The trap list has rank 2. Quiz: $[(3, 5)] = (4, -1)$ in $((1, 1), (1, -1))$; $\dim \mathbb{R}^{3 \times 4} = 12$.
- l4 transfer (compute and report): level $L = (1, 1, 1, 1)$, slope $S = (-3, -1, 1, 3)$, daily weights $(a, b)$ = (2, 1), (−1, 2), (3, 0), (0, −1), (1, 1), (2, −1). The six moves in basis points at 2y, 5y, 10y, 30y are (−1, 1, 3, 5), (−7, −3, 1, 5), (3, 3, 3, 3), (3, 1, −1, −3), (−2, 0, 2, 4), (5, 3, 1, −1). Rank 2 (asserted in the generator and in `checks.py`).
- Review: $\lambda(a, b) = (\lambda a, b)$ fails $(\lambda + \mu)\mathbf{v} = \lambda\mathbf{v} + \mu\mathbf{v}$; $\dim\{p \in \mathcal{P}_4 : p(0) = p(1) = 0\} = 5 - 2 = 3$; $3 \odot (2 \oplus 5) = 10^3 = 1000 = 8 \times 125$; $U = \{(x, y, 0)\}$ and $\operatorname{span}\{(1, 1, 1)\}$ meet in $\mathbf{0}$; $[x^2] = (1, 2, 1)$ in $(1, x - 1, (x - 1)^2)$.
- Homework: $U = \operatorname{span}(\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3)$, $W = \operatorname{span}\{(1, 1, 1, 1), (0, 0, 0, 1)\}$: $\dim(U \cap W) = 1$ (spanned by $(1, 1, 1, 0)$), $U + W = \mathbb{R}^4$; $[(2, 3, 4)] = (-1, 4, 3)$ in $((1, 1, 0), (0, 1, 1), (1, 0, 0))$; $f = 1 - x$, $g = x$ have $f(0)f(1) = g(0)g(1) = 0$ but $(f + g)(0)(f + g)(1) = 1$.

### Code tests, with expected values

Each imports NumPy and decides dependence by `np.linalg.matrix_rank`, never a determinant. Results are Python lists and `int`s compared with `compare: "equal"`.

- l3 `first_dependent(vectors)` (0-based): the four returns → 3; $[\mathbf{u}_1, \mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3]$ → 2; $[\mathbf{u}_1, \mathbf{u}_2, \mathbf{e}_1, \mathbf{e}_3]$ → 3; $[\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3]$ → `None`; $[\mathbf{0}, (1, 2, 3)]$ → 0; $[(1, 2), (2, 4)]$ → 1; a 4-D list → 2; the trap list → 3. The starter returns `None`, as the brief asks, so it passes test 4 only.
- l4 `extend_to_basis(vectors, n)` and `dim_span(vectors)`: the $\mathbb{R}^3$ and $\mathbb{R}^4$ cases as exact lists; $((1, 1), (1, -1))$ unchanged; `[]` with $n = 3$ → the identity's rows; $[(0, 0, 1)]$ → $[(0, 0, 1), \mathbf{e}_1, \mathbf{e}_2]$; $[(1, 2), (2, 4)]$ and $[\mathbf{0}]$ raise `ValueError`; `dim_span` gives 2, 3 and 0. The starter returns `None` from both functions and fails all 10.
- Homework `basis_of_span(vectors)`: the four returns → A, B, C; $[(1, 0), (2, 0), (0, 1)]$ → $[(1, 0), (0, 1)]$; $[\mathbf{0}, \mathbf{e}_1]$ → $[\mathbf{e}_1]$; the l4 trap list → its first two; $[\mathbf{u}_1, \mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3]$ → $[\mathbf{u}_1, \mathbf{e}_1, \mathbf{e}_3]$; two zero vectors → `[]`; the six yield days → days 1 and 2; $[L, S, L + S, L - S]$ → $[L, S]$. The starter keeps every vector and fails all 8.

## Departures from the brief

- l1: $(-1)\mathbf{v} = -\mathbf{v}$ is a quiz `order`, the inverse of 2 and the zero space $\{\mathbf{0}\}$ are quiz items, and P&L as $\mathbb{R}^{252}$ is in the function screen's prose and a quiz item, to keep 12 screens. The $\mathcal{P}_2$ screen grades the sum by a yes/no `table` beside the plane, not a separate `expression`.
- l2: the "first check that fails is $\mathbf{0}$" `choice`, the reason $-\mathbf{w} \in W$ and the union edge case are quiz items. The trap uses one `expression` for the third piece, $(0, -1, -1)$, with the first two pieces drawn and given, not three `expression` screens. The transfer asks for the market part; the zero-sum part $(0.02, -0.02, 0)$ is a quiz `expression`.
- l3: the transfer is a `choice` on why $\boldsymbol{\Sigma}$ is singular, with the $(1, 1, -1, -1)$ portfolio in the prose. The code screen has the brief's five tests plus three (a 2-D, a 4-D and the trap list).
- l4: the basis $(x - 1, x^2 - 1, x^3 - 1)$ `choice` is a quiz item, after the dimension table; $\dim\{\mathbf{0}\} = 0$ is a row of that table and $\mathcal{P}(\mathbb{F})$ a quiz item. The code starter returns `None` rather than its input, so every hidden test fails (a starter that returns its input passes "a basis comes back unchanged").
- Review has 8 items and homework 9. No course.json change is proposed.

## Seeds and data conventions

No randomness. Returns are in percent on canvases (l2 transfer drawn as $(3, -1, 1)$ for $(0.03, -0.01, 0.01)$); yield moves are whole basis points. Indices in code are 0-based; vectors are Python lists of rows.

# Problem set linear-maps level 4 (Operators): second-reader findings

Scope: `app/content/courses/linear-maps/problems-4.json`: 3 problems, 15 parts (10 `expression`, 5 numeric of which 2 are sets, 0 choice), 29 `wrong` entries. Rules: `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md` (Author, Reader). Pattern: `review-problems-analysis-1-3.md`.

Method. The author's script was run first. Every part was then solved by hand from its text and again in `docs/reports/problems-linear-maps-4-numbers-read.py`, which imports nothing from the author's script and types $\mathbf{S}$, $\mathbf{K}$ and $T$ from the prose. Route 1 is exact sympy: `solve` for $(a, b)$, `eigenvals`, `nullspace`, `charpoly`, `jordan_form`, `LUsolve`. Route 2 is another method: Cayley-Hamilton (trace and determinant) for $(a, b)$, numpy `eigvalsh`, `eigh` and `solve`, the cross product against two equations, the spectral sum against elimination, $T$ applied to polynomials by differentiation against powers of its matrix for $t = 1$ to 8, block sizes from ranks of $N^k$ against sympy's own Jordan form and against the change of basis $(6x, x^3, 2, x^2)$ the explanation names. Claims read for their hypotheses: $\mathbf{S}^* = \mathbf{S}$ and $\mathbf{K}^T = \mathbf{K}$ checked; $\mathbf{v}$, $\mathbf{S}\mathbf{v}$ independent, so $(a, b)$ is unique and $p$ is the characteristic polynomial; real eigenvalues; perpendicular eigenvectors with the conjugate in the second slot; $\mathbf{S} = 7\mathbf{q}_1\mathbf{q}_1^* + \mathbf{q}_2\mathbf{q}_2^*$ rebuilt exactly; $\mathbf{Q}^T\mathbf{K}\mathbf{Q} = \operatorname{diag}(4, 1, 7)$; $J_3(1) \oplus J_1(1)$ has $d = (2, 3)$ as its slip line says; $T$ not diagonalisable; $J_2(\lambda)^t$ has top-right entry $t\lambda^{t-1}$. Every `wrong` value was rebuilt from the slip its line names. Each typed part then went through the engine's graders (`review-problems-linear-maps-4-scripts/grade-probe.mjs`, 122 strings of my own in `rows.json`). Reuse: `mats.py` (scratch) parsed 977 square matrices in `app/content` and compared entries and eigenvalues up to scale with $\mathbf{S}$ and $\mathbf{K}$; key numbers and nouns were grepped in the course and stories across `app/content`; l15 to l19, `review-4` and `homework-4` were searched for each idea the set uses.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-linear-maps-numbers.py` exit 0, 0 failures |
| reader's script | `problems-linear-maps-4-numbers-read.py` 193 checks, 0 failures, exit 0 |
| `grade-probe.mjs` (engine graders, 15 typed parts) | 218 checks, 122 reader rows, 0 failures, exit 0; 3 rows held to be engine limits (Engine 1, 2) |
| validator | 0 errors; no warning names `linear-maps/problems-4` |
| `grade-all.mjs --file` | 15 widgets, 0 failures |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --file` (same-course mode) | 0 hits, 2 advisories, both stand (below) |

Every key, every `wrong` value and every printed number is right. No finding of severity wrong. Three low findings.

## Findings

1. `problems-4.json` | `items[0].parts[0].question` | reuse (low) | The sentence that sets up the step is l15 `screens[1].prose` with $\mathbb{R}$ changed to $\mathbb{C}$ and $\mathbf{A}$ to $\mathbf{S}$. Parts 1 to 3 follow l15 screens 0 to 2 step for step, from the same $\mathbf{v} = (1, 0)$, to the same second factor $\mathbf{S} - \mathbf{I}$. | l15: "Three vectors in $\mathbb{R}^2$ are dependent (level 1 l3). So $\mathbf{A}^2\mathbf{v} = a\mathbf{A}\mathbf{v} + b\mathbf{v}$ for some $a, b$." Here: "Three vectors in $\mathbb{C}^2$ are dependent, so $\mathbf{S}^2\mathbf{v} = a\mathbf{S}\mathbf{v} + b\mathbf{v}$ for some $a, b$." The matrix, the numbers $(8, -7)$, the roots and the complex setting are the set's own (l15 has $\begin{pmatrix}2&1\\1&2\end{pmatrix}$, $(4, -3)$, roots 3 and 1), so the task stands as the same standard task. Only the sentence is shared. | Question becomes: "Here $\mathbf{S}\mathbf{v} = (6, 2 - i)$. The list $\mathbf{v}, \mathbf{S}\mathbf{v}, \mathbf{S}^2\mathbf{v}$ has three entries and $\dim\mathbb{C}^2 = 2$, so $\mathbf{S}^2\mathbf{v} = a\mathbf{S}\mathbf{v} + b\mathbf{v}$ for some numbers $a$ and $b$. Find them. Give them as $(a, b)$." No key changes.

2. `problems-4.json` | `items[2].prose`, `items[2].parts[1].feedback.generic`, `.feedback.correct`, `.explain.text` | misleading (low) | "Cubic" is used for every member of $\mathcal{P}_3(\mathbb{R})$. The generic line then asks "which cubics have $p'' = 0$", and no polynomial of degree 3 has. l6 says "a cubic has degree 3". | `feedback.correct` answers with $p = a + bx$, which is not a cubic; `explain` says "Every non-zero cubic is a generalised eigenvector". | Prose: "... be $Tp = p + p''$, which adds to a polynomial of degree at most 3 its own second derivative." Generic: "Not quite. Find which $p$ in $\mathcal{P}_3(\mathbb{R})$ have $p'' = 0$, then which have $p'''' = 0$." Correct: "$Np = p''$ is zero exactly for $p = a + bx$, so $d_1 = 2$. $N^2p = p''''$ is zero for every $p$ in $\mathcal{P}_3(\mathbb{R})$, so $d_2 = 4$." Explain, first sentence: "Every non-zero $p$ in $\mathcal{P}_3(\mathbb{R})$ is a generalised eigenvector for 1, since $N^2 = 0$." No key changes.

3. `problems-4.json` | `items[2].parts[4].question` (and `items[2].parts[3]`) | continuity (low) | The chain breaks after part 3. Part 4's key $(4, 2)$ is part 2's key $(2, 4)$ reversed, since $g = d_1$ and $a = d_2$ here; its own `swapped` slip is part 2's key. Part 5 then leans on part 2, not on part 3 or 4. | Part 5 opens "Using $N^2 = 0$ from part 2". Nothing after part 4 uses $(4, 2)$. | Part 4 stands: it reads the multiplicities off the form, which l19 teaches. Tie part 5 to the form. Question becomes: "Using the blocks $J_2(1) \oplus J_2(1)$ from part 3, no block is longer than 2, so $N = T - I$ has $N^2 = 0$. Find $T^t(x^3)$ for a whole number $t \ge 1$. Give it in terms of $x$ and $t$." Key $x^3 + 6tx$ unchanged (checked for $t = 1$ to 8 two ways).

## Read and held to stand

- `p-footbridge-modes` part 5 states $\mathbf{S} = 7\mathbf{q}_1\mathbf{q}_1^* + \mathbf{q}_2\mathbf{q}_2^*$. l17 gives $\mathbf{A} = \mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^T$; the sum of $\lambda\mathbf{q}\mathbf{q}^T$ is in `eigen` l5 (level 4 requires `eigen/L2`) and the star is l16's. The part states the formula and asks one entry. Stands.
- `p-spring-linkage` part 2 can be passed from the kernel alone; part 1's eigenvector serves the `plane-only` slip and the check. Part 5 can be done by elimination. Both are second routes, not a printed target.
- $\mathbf{S}$ has eigenvalues 1 and 7, both positive, as a matrix of powers needs. $\mathbf{K}$ has 1, 4, 7. No matrix in `app/content` shares their entries up to scale; `eigen` l5 has other $2 \times 2$ matrices with eigenvalues 1 and 7, another course and another matrix.
- $(1, 2, 2)$ is l12's $\mathbf{u}$ in a Cauchy-Schwarz example and a $d$ list in l19: a single vector in another role. Stands.
- `fresh-check` advisories: `items[2]` shares the formula $(1, x, x^2, x^3)$ with l4 `quiz[0]` and l5 `screens[8]`. It is the standard basis of $\mathcal{P}_3$, a notation, not a setting. $p + p''$ is nowhere in the course; l18 and l19 use the shift $p(x + 1)$ on $\mathcal{P}_2$. Stands.
- Stories: "footbridge" and "accelerometer" occur nowhere else; "linkage" only in `stat-learning` clustering; "stiffness" in `numerics` and `odes/homework-4` as stiff equations and a spring constant, not a stiffness matrix.
- Level cover: l15 (item 1), l16 (items 1, 2), l17 (items 1, 2), l18 and l19 (item 3). Each problem draws on at least two lessons. Skills are the level's. Difficulty 5, 4, 4.

## Engine

1. A tuple typed after the letters the question names, `(a, b) = (8, -7)` or `(d_1, d_2) = (2, 4)`, is refused (key `length`). Already in the inbox under "review problems linear-maps 1-3"; two more rows of evidence.
2. `p-curvature-operator` part 5: the question's own left side typed before the answer, `T^t(x^3) = x^3+6tx`, is refused on the generic line. `dropLabel` reads `y =` and `f^{-1}(x) =` but not an operator power applied to an argument.

Inbox: one bullet under `Raised later (review problems linear-maps 4):`.

# Problem sets 1.10, linear-maps levels 1 to 3: second-reader findings

Scope: `app/content/courses/linear-maps/problems-1.json`, `-2`, `-3`: 9 problems, 41 parts (10 numeric, 27 `expression` of which 3 ask for a matrix, 4 choice), 81 `wrong` entries and 12 wrong options. Rules: `docs/briefs/chained.md`, DECISIONS session AB (reuse). Pattern: `review-problems-1.4-c.md`.

Method. The author's script was run first. Each problem was then read whole as a learner would (`show.py` prints a set), with the level's lessons searched for every idea, word and symbol a part leans on (`ctx.py`). Every part was solved by hand from its text and again in `mine.py`, which imports nothing from the author's script and types every vector, matrix and polynomial from the prose. Route 1 is exact (sympy and fractions: `rank`, `nullspace`, `solve`, `LUsolve`, exact inverses, the eight axioms of the shifted space checked symbolically). Route 2 is another method: NumPy `matrix_rank`, `solve`, `lstsq`, `inv`, `eigvals`, `cov`, `corrcoef`, `qr`, the normal equations, a grid search over $U$ for the least distance, and direct substitution. Every rank, kernel, image, coordinate, change of basis and dual-basis claim is checked exactly. Every `wrong` value was rebuilt from the slip its line names, and every number printed in a `feedback`, `byKey`, `why` or `explain` string was recomputed. Every typed part then went through the engine's own graders in node (`grade-probe.mjs`, `rows.json`): the key and each `accept` form, each `wrong` entry on its own key, each wrong matrix typed whole in the `[[a, b], [c, d]]` form, and 268 strings of my own (other spellings of the key, honest roundings, slips, answers one step short, wrong lengths). `try-fix.mjs` tries the two `wrong` entries proposed below on in-memory copies. Freshness: `matrices.py` types the 33 matrices the sets print or hold and searches the course's lessons, reviews and homework, `exams/topic-1.10.json` and the `eigen`, `vectors` and `elimination` courses (110 files, 1,484 matrices) up to a scalar, a transpose and any reordering of rows and columns, then all of `app/content` with `--all`; settings and nouns were read against the lessons by hand.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, uses a term the level does not teach, or refuses a defensible entry; `minor` = loose chain, missing restatement, slip with no line, loose wording or freshness.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-linear-maps-numbers.py` 0 failures, exit 0 |
| `mine.py` (reader's own keys, slips, stated numbers, set shape) | 576 checks, 0 failures, exit 0; 3 CLAIM lines (findings 1, 2, 6) |
| `grade-probe.mjs` (engine graders, 37 typed parts) | 553 checks, 268 reader rows, 0 failures; 6 rows held to be faults (engine note) |
| `grade-probe.mjs`, matrix parts | 3 parts, 7 wrong matrices: each typed whole as `[[...]]` lands on its own line; a matrix of the wrong shape gets the engine's shape line |
| `try-fix.mjs` (the `wrong` entries of findings 8 and 11) | 16 checks, 0 failures |
| `matrices.py` (course, topic exam, `eigen`, `vectors`, `elimination`) | 4 of 33 matrices matched, 0 of 20 vectors; all 4 judged chance (see Verified) |
| `matrices.py --all` (2,461 files, 3,977 matrices) | the same 4 matrices; 4 vectors matched in unrelated drills and lessons, judged chance |
| `grade-all.mjs --local-cdn`, three files | 15, 13 and 13 widgets, 0 failures each |
| validator | 0 errors; no warning on the three files; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0; no exclamation mark, no em-dash, British spelling, £ where money appears |
| `fresh-check.mjs --file`, three sets | 0 hits; advisories on `problems-3` only (the dual-basis definition against l10 and `topic-1.10`; 26, 6.5, 2.5 against a mock paper), read and judged stock and chance |

Result. All 41 keys agree with mine, and so does every one of the 81 `wrong` values. Two printed statements are false (findings 1 and 2); neither changes a mark. `problems-2` writes the kernel and image in a notation the level's lessons never use (finding 4), and one choice part marks a valid argument wrong (finding 5). Two problems of `problems-3` retell the setting of a lesson hook with new numbers (findings 9 and 10). The rest is minor. No band is wide enough to pass a wrong method, and every numeric part states its form.

Counts: `problems-1` 2 wrong, 0 unclear, 1 minor; `problems-2` 0 wrong, 2 unclear, 3 minor; `problems-3` 0 wrong, 0 unclear, 4 minor.

## A. `problems-1`

1. `wrong` | `linear-maps/problems-1.json` | `p-hedge-baskets` | `items[0].parts[1].explain.text` | a stated parameter value does not give the stated vector.
   The `correct` line sets $w_4 = s$, $w_2 = t$, so $\mathbf{w} = (2s, t, -3s - t, s)$. The explanation says $(s, t) = (1, 0)$ gives $(2, -1, -2, 1)$; it gives $(2, 0, -3, 1)$. The vector $(2, -1, -2, 1)$, which part 3 uses as $\mathbf{b}_1$, is $(s, t) = (1, -1)$ (`mine.py` CLAIM). It is in $U$ and the pair is a basis, so no key changes.
   Fix: "Setting $(s, t) = (1, -1)$ and $(0, 1)$ gives $(2, -1, -2, 1)$ and $(0, 1, -1, 0)$. They are independent and span $U$, so they are a basis of length 2."

2. `wrong` | `linear-maps/problems-1.json` | `p-scenario-space` | `items[2].parts[2].feedback.byKey.usual-negative` | wrong number.
   "$\mathbf{u} \oplus (-4, -30) = (-3, -50)$". With $\mathbf{u} = (4, 30)$ and $\mathbf{c} = (3, 40)$, $\mathbf{u} \oplus (-4, -30) = (0, 0) - (3, 40) = (-3, -40)$ (`mine.py` CLAIM).
   Fix: "That is $-\mathbf{u}$ in the usual sense. Here $\mathbf{u} \oplus (-4, -30) = (-3, -40)$, not the zero vector $(3, 40)$."

3. `minor` | `linear-maps/problems-1.json` | `p-scenario-space` | `items[2].parts[3].explain.text` | the list of subspaces leaves one out.
   "Here that means a line or plane of moves through $\mathbf{c}$." The set $\{\mathbf{c}\}$ is a subspace too, and the only plane is the whole space.
   Fix (second sentence only): "Here that means $\mathbf{c}$ alone, a line through $\mathbf{c}$ or the whole plane."

## B. `problems-2`

4. `unclear` | `linear-maps/problems-2.json` | `p-curve-report`, `p-slope-adjusted` | 13 strings in `items[0].parts[2]`, `items[0].parts[4]`, `items[2].parts[1]`, `items[2].parts[2]` | notation the level does not teach.
   The set writes $\operatorname{null} T$ (8 times), $\operatorname{range} T$ (5), "null space" (6) and "range". Lessons l5 to l9, `review-2` and `homework-2` never use any of them: they write $\ker$ (146 times), $\operatorname{im}$ (94), "kernel" and "image" (l6 is titled "Kernel and image"). A learner meets $\dim \operatorname{null} T$ in a graded question with no definition. "Null space" is known for a matrix from `elimination`; "range" of a map is not used in the course.
   Fix, in every string of those four parts (ids stay, `wrong` id `null` stays): `\operatorname{null} T` becomes `\ker T`; `\operatorname{range} T` becomes `\operatorname{im} T`; "null space" becomes "kernel"; "the range" and "The range" become "the image" and "The image". "Rank-nullity" stays (l7's name). No sentence grows.

5. `unclear` | `linear-maps/problems-2.json` | `p-slope-adjusted` | `items[2].parts[1].widget.options[3]` | a valid argument is marked wrong.
   Option d, "$T$ is onto, so its null space is $\{0\}$", is a true implication for an operator on a finite-dimensional space (rank-nullity, l7 and l9). A learner who sees from part 1's explanation that $1$, $x - 1$ and $x^2 - 2x$ span $\mathcal{P}_2$ has a complete proof this way. The `why` calls it circular only because of the order the item chose. The key is also the longest option by 18 characters (69 against 51, 45, 42).
   Fix: `text`: "$T$ maps $\mathcal{P}_2(\mathbb{R})$ to itself, so its kernel is $\{0\}$." `why`: "A map from a space to itself can still send non-zero vectors to 0. $p \mapsto p'$ maps $\mathcal{P}_2(\mathbb{R})$ to itself and sends 1 to 0."

6. `minor` | `linear-maps/problems-2.json` | `p-curve-report` | `items[0].parts[4].explain.text` | the count of conditions is off.
   "The solutions are $p_0$ plus the null space, a plane, so one more condition picks one curve of degree 2." On a plane one condition leaves a line: with $p(0) = 7$ the solutions in $\mathcal{P}_3$ still have one free parameter (`mine.py` CLAIM). One curve is left only among curves of degree at most 2, which is the family the question names.
   Fix (second sentence only): "Among curves of degree at most 2 the solutions are $p_0 + \lambda(t - 2)^2$, a line, so one more condition picks one curve."

7. `minor` | `linear-maps/problems-2.json` | `p-curve-report` | `items[0].parts[3].question` | the part uses no earlier answer.
   Part 4 starts afresh; parts 2 and 3 feed nothing until part 5.
   Fix: "Using the first two columns of the matrix from part 2, $T(a + bt) = (a + 2b, b)$. Find the polynomial $p$ of degree at most 1 with $T(p) = (5, 3)$. Give it in terms of $t$."

8. `minor` | `linear-maps/problems-2.json` | `p-futures-exposure` | `items[1].parts[3].widget.wrong` | one of part 3's two stored slips has no carried line.
   The `sign` slip of part 3 is carried ($(\tfrac{17}{3}, \tfrac{20}{3})$); the `entrywise` slip gives $[T^{-1}]_{\mathcal{B}}(7, 2) = (\tfrac{17}{6}, 1)$ and the position $(\tfrac{29}{6}, \tfrac{35}{6})$, which gets the generic line.
   Fix: add `{ "id": "carried-entrywise", "tex": "(\\frac{29}{6}, \\frac{35}{6})" }` and `byKey.carried-entrywise`: "That uses the inverse with $\tfrac14$ in the corner. With $-\tfrac23$ the $\mathcal{B}$-coordinates are $(1, 1)$, giving $(3, 4)$." (`try-fix.mjs`: it lands, typed as `(29/6, 35/6)` too.)

## C. `problems-3`

9. `minor` | `linear-maps/problems-3.json` | `p-currency-duals` | `items[0]` | the setting is l10's (reuse ruling, session AB: own setting and numbers).
   l10 screen "A P&L rule from two scenarios": a book's P&L is linear in two returns $(x, y)$ in %, two scenarios $\mathbf{v}_1, \mathbf{v}_2$ span every move, and $\varphi_1$ pays 1 on $\mathbf{v}_1$ and 0 on $\mathbf{v}_2$. l10 screen "Exposures in a new basis": P&L in £k $\varphi = 3x - y$, the risk system quotes moves in the scenarios, and the dual-basis coefficients are the P&L of each scenario. Parts 1, 2 and 4 retell both with a fund, two currencies, a risk team and $\psi = 3x + 5y$ in £ thousands. The numbers are fresh (`matrices.py`: no match for the basis, the dual rows or $T$).
   Fix, a new setting with every number kept (8 strings):
   - `prose`: "A gauge on a robot arm reads a voltage that depends linearly on the displacements $(x, y)$, in mm, of two joints. Its engineers describe displacements with two test moves, $\mathbf{v}_1 = (5, 1)$ and $\mathbf{v}_2 = (4, 1)$, a basis of $\mathbb{R}^2$. The dual basis $(\varphi_1, \varphi_2)$ has $\varphi_j(\mathbf{v}_k) = 1$ when $j = k$ and 0 otherwise."
   - `parts[0].explain.text`, first sentence: "$\varphi_1$ reads off the $\mathbf{v}_1$-coordinate of a displacement."
   - `parts[1].feedback.correct`, last sentence: "Check: $\varphi_1 + \varphi_2 = y$, which is 1 on both test moves."
   - `parts[2].question`: "The reading is $\psi(x, y) = 3x + 5y$, in mV. A gearbox changes the displacements by $T(x, y) = (2x - y, x + 3y)$, and the geared reading is the dual map $T'\psi = \psi \circ T$. Find $T'\psi(x, y)$. Give it in terms of $x$ and $y$."
   - `parts[3].feedback.byKey.standard`, last sentence: "In the dual basis the coefficients are the values on the test moves."
   - `parts[3].feedback.byKey.carried`, last sentence: "With $11x + 12y$, the values on the test moves are 67 and 56."
   - `parts[3].explain.text`, last sentence: "The geared gauge reads 67 mV on test move 1 and 56 mV on test move 2."
   - `parts[4].question`, first sentence: "The engineers' inner product on displacements is $\langle \mathbf{u}, \mathbf{w} \rangle = 2u_1w_1 + u_2w_2$."
   No file of the course or of `topic-1.10` has a gauge, a gearbox or a robot arm.

10. `minor` | `linear-maps/problems-3.json` | `p-index-beta` | `items[1]` | the setting is l13's hook (same ruling).
   l13 opens with four days of demeaned returns, the market $\mathbf{m}$ and a factor $\mathbf{f}$, $\beta = \langle \mathbf{f}, \mathbf{m} \rangle / \langle \mathbf{m}, \mathbf{m} \rangle$, and the residual $\mathbf{f} - \beta\mathbf{m}$ by Gram-Schmidt in the covariance inner product; l14 "Hedging by least squares" returns to it. The problem is five days of an index and a stock, the same $\beta$ and the same residual. Parts 2 and 4 (correlation, share explained) are new work, and the numbers are fresh.
   Fix, a new setting with every number kept (6 strings):
   - `prose`, first sentence: "Over five days the noon temperature differed from its mean by $\mathbf{a} = (1, -1, 0, 1, -1)$, in °C, and a kiosk's takings by $\mathbf{b} = (3, 0, -2, 2, -3)$, in £ hundreds." (the second sentence stays)
   - `parts[0].explain.text`, last sentence: "The temperature and the takings move together."
   - `parts[2].explain.text`, last sentence: "$\beta = 2$ is the slope of takings on temperature, £200 a degree."
   - `parts[3].question`: "the stock's variance $\|\mathbf{b}\|^2$ does the index explain" becomes "the takings' variance $\|\mathbf{b}\|^2$ does the temperature explain".
   - `parts[3].feedback.byKey.residual-share`, last sentence: "The temperature explains the rest."
   - `parts[3].explain.text`: "so the index explains $4$ of the $6.5$" becomes "so the temperature explains $4$ of the $6.5$".
   No file of the course or of `topic-1.10` has a kiosk or a temperature.

11. `minor` | `linear-maps/problems-3.json` | `p-currency-duals` | `items[0].parts[3].widget.wrong` | one of part 3's two stored slips has no carried line.
   `not-transpose` ($x + 18y$) is carried as $(23, 22)$. `dropped-three` ($11x + 2y$) gives $(55 + 2, 44 + 2) = (57, 46)$ and the generic line.
   Fix: add `{ "id": "carried-three", "tex": "(57, 46)" }` and `byKey.carried-three`: "That uses $11x + 2y$ from the slip in part 3. With $11x + 12y$, the values are 67 and 56." (`try-fix.mjs`: it lands.)

12. `minor` | `linear-maps/problems-3.json` | `p-index-beta` | `items[1].parts[2].question` | the value used is not restated.
   "Using part 1, find the residual": every other later part of the three sets restates the value it needs.
   Fix: "Gram-Schmidt removes from $\mathbf{b}$ its part along $\mathbf{a}$. Using $\langle \mathbf{a}, \mathbf{b} \rangle = 2$ from part 1, find the residual $\mathbf{r} = \mathbf{b} - \beta\mathbf{a}$ that is orthogonal to $\mathbf{a}$. Give it as $(r_1, r_2, r_3, r_4, r_5)$."

## Engine

- A pair typed with the letters the question names is refused with the generic line: `a=2, b=5` for "Give them as $(a, b)$", `x=3, y=4`, `c1=67, c2=56` (6 rows of `grade-probe.mjs`, 17 tuple parts in the three sets). A single labelled value (`k = -1`) is read. Appended to `docs/BACKLOG-INBOX.md`. Every such part states the form and shows it in the placeholder, so no content change is asked.
- The fault recorded in earlier reads (a wrong matrix typed whole does not reach its line) does not show here: all 7 wrong matrices reach their lines in `[[...]]` form.

## Verified

- Keys: 41 of 41 by two routes. `wrong` values: 81 of 81 rebuilt from their named slips; each differs from its key and has a `byKey` line; the 12 wrong options each have a `why` whose counter-example was recomputed.
- Exact claims: $\dim U = 2$, $\dim W = 2$, $U \cap W$ a line, $\dim(U + W) = 3$; $\operatorname{span}(p_1, p_2, p_3)$ of dimension 2 and which of four polynomials extend $(p_2, p_3)$; the eight axioms for $\oplus$, $\odot$ about $\mathbf{c} = (3, 40)$; rank 2 and nullity 2 of the $2 \times 4$ matrix with kernel basis $((t - 2)^2, t(t - 2)^2)$; $[T]_{\mathcal{B}} = \mathbf{P}^{-1}\mathbf{A}\mathbf{P}$, its inverse and $[(11, 13)]_{\mathcal{B}} = (7, 2)$; $p \mapsto p - p'$ invertible with $T^{-1}q = q + q' + q''$; the dual basis as rows of the inverse; $T'\psi$ by composition and by the transpose; the representer under $\operatorname{diag}(2, 1)$; covariance, correlation, $\beta$, residual and the Pythagoras split; Gram-Schmidt, $P_U\mathbf{v}$ against the normal equations and `lstsq`, the residual in $U^\perp$ and the distance against a grid search.
- Bands: the three 3-place parts (0.784, 0.615, 3.873) take the exact value and more places and refuse a 2-place rounding, which the question's "to 3 places" covers; `8/13` is taken for 0.615. No band reaches a `wrong` value.
- Chain: each later part restates what it uses, except finding 12. Several chains are trees, not lines (`p-hedge-baskets` part 4, `p-currency-duals` parts 3 and 5, `p-index-beta` part 3, `p-two-signal-fit` part 4 use a part other than the one before); only finding 7 uses nothing earlier. A learner who carried a stored slip meets a carried line in 3 parts and the generic line in 2 (findings 8 and 11). In `p-index-beta` a learner who used the plain dot product throughout still reaches the keys of parts 2 and 4, which is right.
- Level: dimension of a sum (l4), dependence lemma (l3), extension to a basis (l4), rank-nullity (l7), matrix in a basis and $\mathbf{P}^{-1}\mathbf{A}\mathbf{P}$ (l8), invertibility (l9), dual basis, dual map and transpose (l10), weighted and covariance inner products (l11), Cauchy-Schwarz and correlation (l12), Gram-Schmidt (l13), projection and least distance (l14). `p-currency-duals` part 5 names no theorem and is solved from the definition of the inner product, as the author says. Each lesson of each level is drawn on. Every `skills` id is in `course.json`.
- Shape: 3 problems a set, 4 or 5 parts each, typed parts 12 of 15, 12 of 13 and 13 of 13, one difficulty 5 in each set, explanations at most three sentences.
- Freshness, matrices: $\begin{pmatrix}1&2\\0&1\end{pmatrix}$ ($T$ on lines in `p-curve-report`, never printed) and $\operatorname{diag}(2, 1)$ (the weights, never printed as a matrix) are stock; the Gram matrix $\begin{pmatrix}3&6\\6&15\end{pmatrix}$ of `p-two-signal-fit` is never printed and is 3 times a matrix in `eigen` l9 and `vectors` l10; $\mathbf{P} = \begin{pmatrix}1&2\\1&3\end{pmatrix}$ of `p-futures-exposure` matches `vectors/problems-3` `p-engraver-dial` $\begin{pmatrix}3&1\\2&1\end{pmatrix}$ only after a transpose and a swap, and two distractors of `topic-1.10` item 19 after a swap, in other roles. None is a reuse. $\mathbf{A}$, $[T]_{\mathcal{B}}$, the $2 \times 4$ matrix, the dual basis, $T$ of `p-currency-duals` and every data matrix match nothing in 3,977 matrices.
- Freshness, settings: `p-hedge-baskets`, `p-hedge-curves`, `p-scenario-space`, `p-curve-report`, `p-futures-exposure`, `p-slope-adjusted` and `p-two-signal-fit` share no setting with a lesson, review, homework or exam item (l7's factor-neutral portfolios, l6's option book and l14's hedge are other stories). $T(x^2) = x^2 - 2x$ in `p-slope-adjusted` equals $q_1$ of `homework-1`'s last item by chance, in another role.

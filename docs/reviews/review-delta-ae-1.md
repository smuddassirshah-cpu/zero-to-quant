# Delta read AE-1: six waived-reuse fix passes, hidden test 13, and the 28 new-shape hits

Counts. Part A: `wrong` 0, `weak` 3, `nit` 4. Part B (28 hits): `reuse` 1, `stands` 14, `rule too loose` 13.

Scope, at commit 30d621c. Part A: the six problems re-keyed or re-worded by the `## Fix pass (session AE, waived reuse)` sections, and hidden test 13 of drill `ci-rebuild-from-orders`. Part B: the 28 `warn` lines of `node tools/same-course-reuse.mjs --all`.

Method. Each item was read whole and solved from its text before its key was read. No browser, no `playthrough.mjs`, no content or engine edit.

- `docs/reports/delta-ae-1-numbers.py` (scratchpad venv Python): every key, `wrong` value and printed number of the six items by a second route (numpy `eigh`, `svd`, `pinv` and `lstsq`; a polar area integral and a search for the farthest edge point; `np.linalg.solve`; day-by-day sums; a brute k-means loop; the greedy rule run for 200,000 terms; the eta function for the series sum). Each key band takes the rounding its feedback prints, refuses each `wrong` value, and no two bands overlap; each later part restates the value it needs. It also checks the relations and proposals quoted below.
- Reuse: every `pmatrix` and `[[..]]` matrix of each course compared up to a scalar, a transpose and row or column swaps; greps of the course for each key number, vector and formula with any letter; greps of `app/content` for each story noun.
- Test 13: the drill's 13 tests run in CPython against ten solutions written for this read (scratch `delta-ae-1/t13.py`).

## Tool results

- `delta-ae-1-numbers.py`: 386 checks, 1 failure, the FINDING row of finding 2. Exit 1 until finding 2 is fixed.
- `grade-all.mjs --file`: 0 failures on each of the six files (15, 18, 19, 15, 19 and 17 widgets).
- `fresh-check.mjs --file`: 0 hits on each of the six files. Advisories: eigen/problems-4 3, analysis/problems-3 2, stat-learning/problems-4 2, series/problems-2 1, none on a fixed item's new content (formulas of other items, and `p-track-laps` 33 and 22 against `homework-4`, where 22 is not in the item).
- Validator: 0 errors; `manifest.json` restored. Voice scan 35: 0 for eigen, vectors, analysis, stat-learning and series.

## Part A findings

Verified with no finding: `eigen/problems-4` `p-track-laps` (all keys, six `wrong` values, $\boldsymbol{\beta}^+ = (1, 4)$ by `pinv` and `lstsq`, both rival fits equally good and longer); `vectors/problems-3` `p-goat-feed` (matrix, determinant, inverse, blend, ten `wrong` values; no matrix of the course matches $\mathbf{A}$ or $\mathbf{A}^{-1}$ up to scalar, transpose or swaps); `series/problems-2` `p-app-users` (all keys and seven `wrong` values; 12500 in `l7-shifted-copy` is $500/0.04$, unrelated); `stat-learning/problems-4` `p-order-sizes` (wording only; all 15 `wrong` values recomputed; no tie at any assignment). Stories ("pond", "goat", "pellet", "messaging app", runner's laps, cube roots) appear nowhere else in `app/content` in these roles.

1. `app/content/courses/eigen/problems-2.json` | `items[p-oval-pond]`, prose and parts 2 to 5 | weak | The new matrix is the worked matrix of `l5-perpendicular-eigenvectors` scaled and shifted: $\mathbf{A} = 10\boldsymbol{\Sigma} - 2\mathbf{I}$ with $\boldsymbol{\Sigma} = \begin{pmatrix}1.1&0.3\\0.3&1.9\end{pmatrix}$ (l5 `screens[9]`). So the eigenvectors are l5's pair: l5 gives $(1, 3)$ and asks for the perpendicular $(3, -1)$; part 3 asks for $(3, b)$ and its explain names $(1, 3)$. The matrix check (scalar, transpose) cannot see a shift by $\mathbf{I}$; the fix pass grepped $\mathbf{A}$, $\mathbf{A} - 8\mathbf{I}$ and $\mathbf{A} - 18\mathbf{I}$ only. Eigenvalues (8, 18 against 1, 2), task and story differ, so this is for the main session to rule under "a worked example shifted and scaled" (session AD). | If renumbered, one checked option: $40x^2 + 12xy + 45y^2 = 1764$, $\mathbf{A} = \begin{pmatrix}40&6\\6&45\end{pmatrix}$, eigenvalues 36 and 49, long axis $(3, -2)$, half-axes 7 and 6, area $42\pi = 131.95$. No matrix of the eigen course matches it or $\begin{pmatrix}4&6\\6&9\end{pmatrix}$ up to scalar and transpose; $(2, 3)$ appears in l3, l6, l9, l16 and `homework-1` and those screens must be read first.
2. `app/content/courses/analysis/problems-3.json` | `items[p-cube-root-greedy].parts[1].question` | weak | The re-wording dropped which unused term is taken: "add the positive term not yet used" (many are unused). The old text and l14 say "the next unused positive term", and the `skipped` entry of part 4 marks the learner who takes $\tfrac{1}{\sqrt[3]{5}}$. Part 3's generic line still says "next". | "While the running total sits at or below $T$, add the first positive term not yet used. Once it rises above $T$, add the first negative term not yet used." (No 12-word run with `review-3` `r-greedy-second`.)
3. `app/content/drills/ci-rebuild-from-orders.json` | `tests[12]`, `constraints[1]` | weak | Test 13 refuses a correct solution the constraints do not rule out: the dict-free recursion with a bounded search, `ino.index(root, lo, hi)`. It costs $O(nh)$, which "height at most 400" invites, and the constraint calls $O(n)$ only "the target". On test 13 it scans 37.8 million ids (under half a second) and is stopped by `RuntimeError: scanned more than 30 ids per id` at count 3,098,915. Run in CPython: reference, `deque.popleft`, `iter` and `next`, one reversed copy with `pop()` (count 99,980), a stop-value recursion and an iterative stack all pass with count 0 or one copy; the slicing solution is stopped as intended. So an index variable with a dict is certain to pass: integer `pre[pos]`, `enumerate(ino)` and `len` never reach the counter. | State the gate: `constraints[1]` "$O(n)$ time is required: one hidden test counts the ids copied by slices and scanned by `index`, and stops past 30 per id."
4. `app/content/drills/ci-rebuild-from-orders.json` | `tests[12].setup` | nit | The counter is left by one copy. A helper that slices plain lists after `go(list(pre), list(ino))` passes all 13 tests (count 0, 1.96 s in CPython, about the 2.35 s the fix pass measured). `pre.pop(0)` with a dict is also uncounted and takes 10.9 s in CPython, so only the clock stops it. | None needed; note it in `docs/reviews/review-owed-fixes-ae.md`.
5. `app/content/courses/series/problems-2.json` | `items[p-app-users].parts[1].widget.wrong[0].id`, `parts[3].widget.wrong[1].id` | nit | Stale ids after the re-key: `no-halve` now divides by 4, and `nine` has value 7. Learners never see ids. | Rename `no-halve` to `no-divide-4` and `nine` to `day-before`, with their `byKey` keys.
6. `app/content/courses/eigen/problems-2.json`, `problems-4.json` | `p-oval-pond` part 2, `p-track-laps` parts 1 and 2 | nit | The two new matrices share 9, 144 and 153: the pond prints "$\det\mathbf{A} = 153 - 9 = 144$", the laps item has entries 9 and 144 and the eigenvalue 153. Different sets and tasks; `homework-3`'s 153.09 is unrelated. | Goes away if finding 1 is renumbered; otherwise leave.
7. `app/content/courses/stat-learning/problems-4.json` | `items[p-order-sizes].parts[0..2].question` | nit | Not from this fix: parts 1 to 3 state no form (brief: every numeric part states its form). The `percent-sign` entries cover the likeliest slip. | Add "Give a whole number." to parts 1 to 3.

## Part B: the 28 hits

Rulings used: DECISIONS session AC (a single common value stands; a matrix doubled, a number scaled, a shifted series are reuse) and session AD (function with interval and region with integrand are app-wide; a worked example shifted and scaled is reuse; a quadratic with small whole roots shared with another topic stands; a taught definition stands).

| # | set, item | kind | source | verdict | basis |
|---|---|---|---|---|---|
| 1 | analysis/problems-5 `p-root-sums` | function | integrals/l16 `quiz[2]` | rule too loose (R1) | The lesson integrates $\tfrac{1}{\sqrt{x}}$ on $[0, 9]$ (improper, value 6); the problem's function is $\sqrt{x}$. The denominator was read as the function. |
| 2 | counting/problems-1 `p-team-photo` | pair | counting/l2 `screens[8]` | stands | Stock value: $7! = 5040$ and $6! = 720$, the factorial table. |
| 3 | counting/problems-1 `p-team-photo` | pair | counting/review-2 `items[5]` | stands | Stock value, as row 2; a round table against a captain in the middle. |
| 4 | integrals/problems-3 `p-order-size-tail` | transform | integrals/l9 `quiz[2]` | rule too loose (R2) | $3(1 + x^2)^3$ is the denominator of the `power-down` wrong entry, not the problem's content. The integrands differ: $\tfrac{2x}{(1 + x^2)^2}$ against $2x(x^2 + 1)^2$. |
| 5 | limits-thm/problems-2 `p-quote-life` | function | ito/review-4 `items[5]` | stands | Small whole roots, another topic (AD): $(3 - t)^2$ is a tail function here and an Itô integrand there. |
| 6 | markov/problems-4 `p-regime-sampler` | pair | markov/l13 `screens[2]` | rule too loose (R3) | 0.6 and 0.3 with 0.5 in the sentence; a birth and death ratio, not this sampler. |
| 7 | same | pair | markov/l2 `screens[3]` | rule too loose (R3) | A row of a weather matrix: 0.6, 0.3, 0.1. |
| 8 | same | pair | markov/l7 `screens[8]` | rule too loose (R3) | Queue chances 0.6, 0.3, 0.1. |
| 9 | same | pair | markov/l8 `screens[8]` | rule too loose (R3) | The same queue sentence. |
| 10 | same | pair | markov/problems-2 `items[1]` | rule too loose (R3) | $h = 0.3 + 0.5h$; 0.5 is in the sentence. |
| 11 | multivar/problems-5 `p-triangle-field` | function | limits-thm/l17 `screens[6]` | stands | Small whole roots, another topic (AD): $u(1 - u)^3$ is an inner integral in an explain here, an order-statistic density there. |
| 12 | multivar/problems-5 `p-triangle-field` | region | vector-calc/homework-3 `items[1]` | rule too loose (R4) | The homework has a plane with intercepts 4, 2, 4 and a cross product; its shadow triangle is never drawn or integrated over. The integrands share nothing ($xy^2$ against $dS$). |
| 13 | quadratics/problems-4 `p-storage-crate` | function | quadratics/review-4 `items[6]` | reuse | $V(x) = x^3 + 4x^2 + x - 6 = -R(-x)$ for the review's $R(x) = x^3 - 4x^2 + x + 6$: the same cubic reflected, same level, same task (factor theorem, divide, factorise fully). Ruling AD, shifted and scaled. Fix below. |
| 14 | same, part 3 | function | quadratics/l17 `screens[5]` | rule too loose (R2) | $x^3 - 7x - 6$ is the `signs` wrong entry $(x + 2)(x - 3)(x + 1)$, not the problem's cubic. |
| 15 | same, part 4 | function | quadratics/l1 `screens[1]` | stands | Small whole roots: $x^2 + 5x + 6$ is the course's stock quadratic. Goes with the fix of row 13. |
| 16 | same, part 4 | function | quadratics/l15 `screens[1]` | stands | As row 15. l15 also cancels it in a fraction; the fix of row 13 removes it. |
| 17 | same, part 4 | function | quadratics/l3 `screens[5]` | stands | As row 15. |
| 18 | same, part 4 | function | quadratics/l5 `screens[3]` | stands | As row 15 (l5 has $x^2 - 5x + 6$). |
| 19 | regression/problems-3 `p-power-price` | pair | regression/homework-1 `items[7]` | rule too loose (R3) | "$r^2 = 2 \times 0.3 = 0.6$" in a unit keyed 2; here $\delta = 0.30$ and $r = 0.60$. |
| 20 | same | pair | regression/review-3 `items[0]` | rule too loose (R3) | $\delta = -0.3$ and "0.5 − 0.6"; 0.5 is in the sentence and the unit is keyed $-0.1$. |
| 21 | taylor/problems-3 `p-tail-bound` | function | taylor/l7 `screens[9]` | stands | Standard series: $T_3$ of $e^x$. Note: both price £1 under continuous compounding (5% for a year there, 8% for five years here); numbers and parts 2 to 5 are new. |
| 22 | same | function | exams/topic-1.3 `items[10]` | stands | Standard series. |
| 23 | taylor/problems-3 `p-big-gain` | function | taylor/l7 `screens[5]` | stands | Standard series: $\ln(1 + x)$. |
| 24 | trig/problems-2 `p-two-buoys` | pair | trig/l9 `screens[4]` | stands | Stock values (the 3/8 ruling, AC): two plain halves, peak times in seconds here, a range of heights there. |
| 25 | vector-calc/problems-2 `p-cycloid-arch` | function | vector-calc/l12 `screens[5]` | stands | Standard integral: $\cos^2 t$ over a full turn is $\pi$, one term of $(1 - \cos t)^2$ here. |
| 26 | same | function | vector-calc/l3 `quiz[2]` | stands | As row 25. |
| 27 | vector-calc/problems-3 `p-can-curl` | function | vector-calc/l10 `screens[8]` | rule too loose (R5) | "$x^2 + y^2$ on $[0, 2]$" is the left side of a cylinder's equation with the range of $z$. Radii differ: 4 against 1.5. |
| 28 | same | function | vector-calc/review-3 `items[2]` | rule too loose (R5) | As row 27; radius 1 there. |

Row 13, what to change. Renumber the crate on $V(x) = x^3 + 6x^2 + 3x - 10$, $x > 1$ (0 hits in `app/content` for this cubic or its reflection, any letter, expanded or factorised; checked in the script):

- part 1: $V(-2) = -8 + 24 - 6 - 10 = 0$, key 0.
- part 2: quotient $x^2 + 4x - 5$ ($x^2(x + 2)$ leaves $4x^2 + 3x - 10$; $4x(x + 2)$ leaves $-5x - 10 = -5(x + 2)$).
- part 3: $(x + 2)(x + 5)(x - 1)$ (product $-5$, sum 4: 5 and $-1$); `signs` $(x + 2)(x - 5)(x + 1)$, `one-root-sign` $(x + 2)(x + 5)(x + 1)$.
- part 4: base $x^2 + 7x + 10 = (x + 2)(x + 5)$, height $x - 1$ (neither quadratic is in the quadratics course).
- part 5: $x = 3.5$, $V = 5.5 \times 8.5 \times 2.5 = 116.875$ m³.

Other `wrong` values follow from these and need the fixer's script.

Rule changes for the 13 `rule too loose` hits (each keeps the eight true positives of `test-fresh-check-same-course-ae.mjs`, to be confirmed on its fixtures):

- R1 (row 1): a function under a fraction bar is keyed on the whole quotient, so $\tfrac{1}{\sqrt{x}}$ is not $\sqrt{x}$.
- R2 (rows 4, 14): take no shape from a `wrong` entry or an incorrect option; a slip's formula is not the problem's.
- R3 (rows 6 to 10, 19, 20): a pair sentence may hold no decimal other than the two keys, stock decimals included (0.5 and 0.1 count against it), and one of the two values must be a key of the source unit. The true positive keeps both: l23 is keyed 0.3 and reads "$r = 1 - 0.7 = 0.3$".
- R4 (row 12): the projected-intercept form of `region` runs in the same course only; plain corner sets stay app-wide. `p-triangle-flux` still hits both ways (corners against multivar, projection against its own course's homework).
- R5 (rows 27, 28): a function with an interval needs the interval's variable in the function when the variable is named ($0 \le z \le 2$ does not bound $x^2 + y^2$), and a level set keeps its right-hand side.

## Engine

- Five bullets R1 to R5 and one miss (finding 1: a symmetric matrix equal to another after $a\mathbf{M} + b\mathbf{I}$) are in `docs/BACKLOG-INBOX.md` under `Raised later (delta AE-1):`.

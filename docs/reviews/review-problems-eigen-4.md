# Problem set eigen level 4: second-reader findings

Scope: `app/content/courses/eigen/problems-4.json`: 4 problems, 18 parts (11 numeric, 2 numeric sets, 4 `expression`, 1 choice), 45 `wrong` entries, lessons l13 to l17. Rules: `docs/briefs/chained.md`. Pattern: `review-problems-1.4-c.md`. Extra task: `## Near-miss sample` at the end.

Method. The author's script was run first. The five lessons were skimmed screen by screen with `review-4` and `homework-4` (`review-problems-1.4-a-scripts/taught.py`), for what the level teaches and for reused settings and numbers. Every part was solved by hand from its text (`review-problems-1.4-c-scripts/show.py 4` prints the set) and again in `mine.py`, which imports nothing from the author's script and types every matrix, vector and data column from the prose. Route 1 is exact (sympy: similarity, eigenvalues, `LUsolve`, `cholesky`, nullspace, exact matrix exponential). Route 2 is another method: NumPy `eigvals`, `eigvalsh`, `cholesky`, `solve`, `pinv` and `lstsq`, the lagoon system stepped by RK4, 2,000,000 simulated turbine hours for the tail chance, 400,000 simulated runs of the two-state machine, and a scan in $t$ for the 0.01 time. Every `wrong` value was rebuilt from the slip its line names, and every number printed in a `feedback`, `byKey`, `why` or `explain` string was recomputed while reading. Every typed part then went through the engine's own graders in node with the local Compute Engine (`grade-probe.mjs`: the key with more places, a letter and `=`, a true minus sign and its unit; each `accept`; each `wrong` on its own key; 202 strings of my own). `proposed.py` proves the two reuses from the lesson files and computes the numbers of the fixes twice. `fresh.py` greps every matrix, key number and story noun across `app/content` and checks the `skills` ids.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question reads two ways, does not say the form wanted, or refuses a sensible entry; `minor` = loose `wrong` entry, missing restatement, wording or freshness.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-eigen-numbers.py` 2,182 checks, 0 failures, exit 0 |
| `mine.py` (reader's own keys, slips, stated numbers, bands, set shape) | 345 checks, 0 failures, exit 0; 4 CLAIM lines (band notes, finding 4) |
| `grade-probe.mjs` (engine graders, 17 typed parts) | 353 checks, 202 reader rows, 0 failures; 2 rows held to be a fault (finding 4) |
| `proposed.py` (reuse shown from the lesson files; numbers of fixes 1 and 2) | 40 checks, 0 failures, exit 0 |
| `fresh.py` | exit 0; hits read by hand (findings 1 and 2); every `skills` id is carried by a level 4 lesson |
| `grade-all.mjs --file` | 18 widgets (numeric 13, expression 4, choice 1), 0 failures |
| validator | 0 errors; no warning on the file; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0; no exclamation mark, no em-dash, British spelling, no money in the set |
| `fresh-check.mjs --file` | 0 hits; 2 advisories ($u_1 + u_2$ with l14, $e^{-d^2/2}$ with l16), both the taught tools |

Result. All 18 keys agree with mine, and so do all 45 `wrong` values and every number in a feedback or explanation string. Every `wrong` entry lands on its own key and has a line; no two bands touch. No part marks a right answer wrong, and no statement of theory is false. Each later typed part restates what it needs; the one choice part does not (finding 3). The set covers l13 to l17, each problem draws on two lessons, one problem is difficulty 5, and 17 of 18 parts are typed. Findings: 0 `wrong`, 0 `unclear`, 4 `minor`. Two are reuse that `fresh-check` cannot see, and the author's report says of them "No matrix of the course is reused", which is not so.

## Findings

1. `minor` | `eigen/problems-4.json` | `p-linked-lagoons` | `items[0].prose`, parts 1 to 4 | freshness: the change of grid is l13's own.
   $\mathbf{M} = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ and $\mathbf{M}^{-1} = \begin{pmatrix} 1 & -1 \\ 0 & 1 \end{pmatrix}$ are the pair of l13 screens 0, 1 and 5. There too $\mathbf{B}$ comes out lower triangular, and its eigenvalues are 5 and 2 with trace 7 and determinant 10. The item has $-5$ and $-2$, trace $-7$, determinant 10 (`proposed.py`). The learner multiplies by the same two matrices as in the lesson the item draws on. DECISIONS session AB: an item may not share numbers with a lesson.
   Fix (all keys stay; `proposed.py` checks each value):
   - `prose`: "... to $\mathbf{u} = \mathbf{M}\mathbf{w}$ with $\mathbf{M} = \begin{pmatrix} 1 & 0 \\ 1 & 1 \end{pmatrix}$, so $w_2 = u_2 - u_1$ is the difference between the lagoons."
   - part 1 `question`: "Find the bottom-right entry of $\mathbf{B} = \mathbf{M}^{-1}\mathbf{A}\mathbf{M}$, where $\mathbf{M}^{-1} = \begin{pmatrix} 1 & 0 \\ -1 & 1 \end{pmatrix}$. Give a whole number." Key $-5$ stays. `wrong`: `sign` 5 stays, `unchanged` $-3$, `reversed` $-1$.
   - part 1 `correct`: "$\mathbf{A}\mathbf{M} = \begin{pmatrix} -2 & 2 \\ -2 & -3 \end{pmatrix}$, and row 2 of $\mathbf{M}^{-1}$ takes row 2 minus row 1 of it: $-3 - 2 = -5$."
   - part 1 `sign`: "The entry is negative. Row 2 minus row 1 of $\mathbf{A}\mathbf{M}$ ends with $-3 - 2 = -5$." `unchanged`: "That is the bottom-right entry of $\mathbf{A}$. The change of grid moves the entries: $\mathbf{M}^{-1}\mathbf{A}\mathbf{M}$ has $-3 - 2 = -5$ there." `reversed`: "That is the bottom-right entry of $\mathbf{M}\mathbf{A}\mathbf{M}^{-1}$. With $\mathbf{u} = \mathbf{M}\mathbf{w}$ the new matrix is $\mathbf{M}^{-1}\mathbf{A}\mathbf{M}$, with $\mathbf{M}$ on the right."
   - part 1 `explain`: "In full, $\mathbf{B} = \begin{pmatrix} -2 & 2 \\ 0 & -5 \end{pmatrix}$. Its bottom row says $w_2' = -5w_2$: the difference between the lagoons decays on its own."
   - part 2 `question`: "Using part 1, $\mathbf{B} = \begin{pmatrix} -2 & 2 \\ 0 & -5 \end{pmatrix}$. Find both eigenvalues of $\mathbf{A}$. Type them separated by a comma." `correct`: write $(-2 - \lambda)(-5 - \lambda)$; the rest stands.
   - part 3 `question`: "Using $\mathbf{B}$ from part 1, $\mathbf{y} = (2, -3)$ is an eigenvector of $\mathbf{B}$ for $-5$. Find the eigenvector of $\mathbf{A}$ it stands for, $\mathbf{x} = \mathbf{M}\mathbf{y}$. Give it as $(a, b)$." Key $(2, -1)$ stays. `wrong`: `inverse` `(2, -5)`, `unmoved` `(2, -3)`.
   - part 3 `correct`: "$\mathbf{M}\mathbf{y} = (2, 2 - 3) = (2, -1)$. Check: $\mathbf{A}(2, -1) = (-10, 5) = -5(2, -1)$." `generic`: "Not quite. Multiply $\mathbf{M}$ by $(2, -3)$: coordinates in the new grid go back to the standard grid through $\mathbf{M}$."
   - part 4 `wrong` `w-coords`: `(5, -3)`; its line stands.
   A changed `wrong` value is not a changed key, but the fixer should rerun `grade-all` and the author's script (its lagoon block types $\mathbf{M}$).

2. `minor` | `eigen/problems-4.json` | `p-machine-stops` | `items[3]`, all five parts | freshness: the generator is twice l14's.
   l14 screens 9 and 10 use the credit generator $\begin{pmatrix} -0.1 & 0.3 \\ 0.1 & -0.3 \end{pmatrix}$: eigenvalues 0 and $-0.4$, eigenvectors $(3, 1)$ and $(1, -1)$, steady state $(0.75, 0.25)$, curves $0.75 + 0.25e^{-0.4t}$ and $0.75 - 0.75e^{-0.4t}$. The item's $\mathbf{Q}$ is exactly twice that matrix (`proposed.py`). So it has the same steady state, the same eigenvectors and the same coefficients 0.75 and 0.25; only the rate in the exponent differs. A learner who remembers the lesson's hint has parts 2 to 4.
   Fix: the machine stops at rate 0.1 an hour and restarts at rate 0.4 an hour, and part 4 asks for 5 hours. Every value below is computed twice in `proposed.py`; no eigen file holds the new generator or $(0.8, 0.2)$. Sentences stand with the numbers swapped.
   - `prose`: rates 0.1 and 0.4; $\mathbf{Q} = \begin{pmatrix} -0.1 & 0.4 \\ 0.1 & -0.4 \end{pmatrix}$.
   - part 1: `answers` `[0, -0.5]`; `wrong` `sign` "0, 0.5", `diagonal` "-0.1, -0.4". Lines: $\det\mathbf{Q} = 0.04 - 0.04 = 0$; trace $-0.1 - 0.4 = -0.5$; `explain` $\lambda^2 + 0.5\lambda = \lambda(\lambda + 0.5)$.
   - part 2: `answer` `(0.8, 0.2)`; `accept` `(0.8,0.2)`, `[0.8, 0.2]`, `(\frac{4}{5}, \frac{1}{5})`, `(4/5, 1/5)`, `0.2(4, 1)`, `\frac{1}{5}(4, 1)`; `wrong` `swapped` `(0.2, 0.8)`, `unscaled` `(4, 1)`. `correct`: "$-0.1a + 0.4b = 0$ gives $a = 4b$, and $a + b = 1$ then gives $(0.8, 0.2)$. The machine runs four fifths of the time." `explain`: flows $0.1 \times 0.8 = 0.08$ and $0.4 \times 0.2 = 0.08$; $\mathbf{Q}(0.8, 0.2) = \mathbf{0}$.
   - part 3: in the options, the `why` lines, `correct` and `explain`: $-0.8$ becomes $-0.5$, 0.8 becomes 0.5, $(0.25, 0.75)$ becomes $(0.2, 0.8)$, $(0.75, 0.25)$ becomes $(0.8, 0.2)$; $\mathbf{Q}' = \begin{pmatrix} -0.4 & 0.1 \\ 0.4 & -0.1 \end{pmatrix}$ with trace $-0.5$.
   - part 4: eigenvalue $-0.5$, steady state $(0.2, 0.8)$, "5 hours later". `answer` 0.266. `wrong`: `running-chance` 0.816, `no-steady` 0.066, `restart-rate` 0.308, `one-hour` 0.685. `correct`: "$(1, 0) = (0.2, 0.8) + 0.8(1, -1)$, and the second part decays as $e^{-0.5t}$. So the chance is $0.2 + 0.8e^{-2.5} = 0.2 + 0.8 \times 0.0821 = 0.266$." Lines: $0.8 + 0.2e^{-2.5}$; $0.8e^{-2.5}$ and the steady share 0.2; restart rate 0.4 against the eigenvalue $-0.5$; $0.2 + 0.8e^{-0.5}$ and the exponent $-2.5$ after 5 hours. `explain`: "... a multiple of $e^{-0.5t}$. This one is 0.266 at $t = 5$, and $0.2 + 0.8 = 1$ at $t = 0$, as it must be."
   - part 5: "Using the chance $0.2 + 0.8e^{-0.5t}$ from part 4, after how many hours is it within 0.01 of the steady share 0.2?" `answer` 8.76. `wrong`: `running-start` 5.99, `no-coefficient` 9.21, `restart-rate` 10.96, `multiplied` 2.19. `correct`: "$0.8e^{-0.5t} = 0.01$ gives $e^{-0.5t} = 1/80$, so $t = \ln 80 / 0.5 = 4.382 / 0.5 = 8.76$ hours." Lines: $\ln 20 / 0.5$ for the coefficient 0.2; drops the 0.8; restart rate 0.4 against decay rate 0.5; multiplies $\ln 80$ by 0.5. `explain`: "After about 8.8 hours ... eigenvalue $-0.5$, minus the sum of the two rates."
   This changes five graded answers, so it needs a delta read (DECISIONS session AA) and a fresh run of the author's script, `grade-all` and `fresh-check`.

3. `minor` | `eigen/problems-4.json` | `p-machine-stops` | `items[3].parts[2].question` | the part does not restate what it needs.
   "Using parts 1 and 2, what does the team find?" names the parts but not their values. A learner who typed $(0.25, 0.75)$ in part 2 reasons correctly from it to the `same-vector` option and is marked wrong a second time. `chained.md`: each later part restates the value it needs.
   Fix, last sentence of the question: "Part 1 gave the eigenvalues 0 and $-0.8$, and part 2 the steady state $(0.75, 0.25)$ with Running first. What does the team find?" (With fix 2: $-0.5$ and $(0.8, 0.2)$.)

4. `minor` | `eigen/problems-4.json` | `p-wind-pair` | `items[1].parts[1].feedback.byKey.carried` | the line names one slip, the band holds two.
   The band is $-1.029 \pm 0.5$, as the validator's wrong-band rule asks for a whole-number part. It also holds $-6/9 = -0.667$, the answer carried from the `no-root` slip of part 1 ($L_{22} = 9$). That learner is told "That divides by $\sqrt{34}$ in place of $L_{22}$" (`grade-probe.mjs`, 2 rows). The part restates $\mathbf{L}$, so few will arrive this way.
   Fix: "That divides by a wrong $L_{22}$, such as $\sqrt{34}$ or 9. With $L_{22} = 3$, $w_2 = (4 - 10)/3 = -2$."

## Verified

- Keys: all 18 by two routes (`mine.py`). `p-linked-lagoons`: $-5$; $-5, -2$; $(2, -1)$; $(3, 1)$; $6e^{-2} + e^{-5} = 0.8188$, and RK4 on $\mathbf{u}' = \mathbf{A}\mathbf{u}$ from $(5, 2)$ gives the same total. `p-wind-pair`: 3; $-2$; $\sqrt8 = 2.828$ with $\mathbf{x}^T\boldsymbol{\Sigma}^{-1}\mathbf{x} = 8$ exactly; $e^{-4} = 0.0183$, simulated tail 0.0183. `p-track-laps`: 0; 45; $(1, 2)$ by the formula, `pinv` and `lstsq`; 15. `p-machine-stops`: $0, -0.8$; $(0.75, 0.25)$; option `moved`; $0.25 + 0.75e^{-2.4} = 0.3180$, the exact entry of $e^{3\mathbf{Q}'}$ and a simulation agree; $\ln 75 / 0.8 = 5.397$.
- `wrong` values: all 45 rebuilt from the slip named and equal to the file. The `carried` entries follow from the slips they name: $(1, 3)$ gives 0.291; $\sqrt{34}$ gives $-1.029$; $w_2 = -12$ gives 12.166; $d = 2.114$ gives 0.1070; a running start gives 4.02.
- Stated numbers: $\mathbf{A}\mathbf{M}$, $\mathbf{B}$, trace $-7$, determinant 10, $\mathbf{A}(2, -1) = (-10, 5)$, 0.1353, 0.0067, the factor $(4, 0; 5, 3)$, "$+10$ for turbine 2", "2 sd short", "one hour in 55", $(45, 90)$, $\mathbf{u}_1 \cdot \mathbf{y} = 15$, $\sqrt5\sqrt{45} = 15$, lengths 5 and $\sqrt5$, flows 0.15, $\mathbf{Q}'$, 0.0907, 4.317.
- Bands: every key takes the value its own feedback line prints (0.8185 from the printed constants is accepted, and so is 0.818; 5.396 from $4.317/0.8$ is accepted). Each key band refuses every `wrong` value. The three $\pm 0.5$ slip bands (`p-wind-pair` parts 1 and 2, `p-track-laps` part 1) are the validator's wrong-band rule at work: the slip rounded to a whole number as asked (6, 4, $-1$, 1) reaches its line. Read and accepted, but for finding 4.
- Forms: every numeric part says the form it wants. Vector parts take `(a,b)`, a column `pmatrix` and decimals; part 2 of `p-machine-stops` takes fractions and `\frac{1}{4}(3,1)`. Number sets take either order, "and", and $-4/5$.
- Chain: each later part uses the result before it and restates it, but for finding 3. `p-track-laps` part 4 is kind to a carried slip by design: $(5, 0)$ and $(0, 2.5)$ also predict 15.
- Claims read and held true: similar matrices share eigenvalues and eigenvectors move by $\mathbf{M}$ (l13 screen 5 states the mirror, $\mathbf{M}^{-1}\mathbf{x}$); a zero Cholesky pivot means positive semidefinite only; the tail chance $e^{-d^2/2}$ in two dimensions (l16 screen 4); every best fit predicts the same for a row in the row space; a generator always has eigenvalue 0; column convention as in l14 screen 10.
- Level: nothing used that l13 to l17 or earlier levels do not teach. "Grid", "mode", "un-mix", "Mahalanobis distance", "generator", "shortest best fit" are the lessons' own words. The rank-one form $\mathbf{X}^+ = \mathbf{v}_1\mathbf{u}_1^T/\sigma_1$ is given in the part.
- Voice: 0 sentences over 35 words, 0 explanations over three sentences, British spelling, no exclamation mark, no em-dash.
- Freshness (`fresh.py`): the nouns lagoon, hydrologist, turbine, laps per km, maintenance team and every data matrix but $\mathbf{M}$ stand nowhere else in `app/content`. Findings 1 and 2 are the two reuses. Read and accepted: `p-wind-pair` runs the chain of l16 screens 2 to 4 on its own numbers; `p-track-laps` part 3 has the answer $(1, 2)$ of `homework-4` `h-pinv1` ($\mathbf{A} = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$, $\mathbf{b} = (5, 10)$), with another matrix, other data and another route, so only the answer vector meets; `r-chol` in `review-4` also has $L_{22} = 3$, from other entries; "MWh" is a unit in four unrelated files; "packaging" is a Python lesson title.

## Counts

| set | parts | `wrong` | `unclear` | `minor` |
|---|---|---|---|---|
| `problems-4` | 18 | 0 | 0 | 4 |

Finding classes: reuse that `fresh-check` cannot see (findings 1 and 2; the fifth review of topic 1.4 to see it, already an engine note in `review-problems-1.4-c.md`); a later part that does not restate what it needs (finding 3); a slip band whose line names one slip of two (finding 4).

## Near-miss sample

Sample: 12 `ci-` drills drawn at random (seed 20261112, `review-problems-eigen-4-scripts/nearmiss-sample.py`) from the 118 whose `nearMiss` plant was an existing plant (`docs/reports/near-miss-1.md`, `near-miss-2.md`). In all 12 the file marks the plant the report names. For each I read the statement, `constraints`, hint, model solution, the marked plant and the slips of the other plants.

| drill | plant | verdict | reason |
|---|---|---|---|
| `ci-checkpoint-route` | 1 | true | Two searches as the model does, but the marks are not cleared, so it fails only when the legs must share cells, the case the brief stresses. |
| `ci-excused-outages` | 2 | true | A window that restarts at today where the model shrinks from the left: the sliding window one step short. |
| `ci-first-misplaced` | 2 | true | The in-order check, a right test for "is it in order", answers the wrong question for "first in preorder". |
| `ci-line-from-pairs` | 2 | true, borderline | The model's walk with the start taken as the smallest name, not the smallest end; right whenever that name is an end. |
| `ci-loop-starts` | 0 | true | The textbook skip-ahead greedy finds one start where the brief asks for every start. |
| `ci-paired-signals` | 3 | true | The monotone deque with `if` for `while` on the stale end: a window slip that shows only when several signals expire at once. |
| `ci-rest-days` | 0 | true, borderline | The model with the rest counted from the work day, a fencepost on "whole days"; plant 3, the day-by-day wait the constraints rule out, is as near. |
| `ci-spiral-cells` | 2 | not true | Height and width swapped under a complete $O(\log)$ method is a transposition slip. The constraints name ring-by-ring skipping as the method to beat, and that is plant 4. |
| `ci-stop-cascade` | 0 | true | Fires the stops ready before the trades and misses those the trades set off, the cascade the drill is named for. |
| `ci-target-blocks` | 0 | true | Every rectangle from a prefix table, $O(R^2C^2)$: the slower order the constraints rule out by name. |
| `ci-tick-ranges` | 1 | true | Lower bound without the test that the time found is the time asked: the absent-time case missed. |
| `ci-van-pairs` | 2 | true | Strict `<` refuses a pair weighing exactly `cap`: the tie case missed. |

Judged not a true near-miss: 1 of 12 (`ci-spiral-cells`; move the mark to plant 4, which is time-based, as `ci-target-blocks` plant 0 is). Two more are true but borderline (`ci-line-from-pairs`, `ci-rest-days`). No sign of plants marked only to quiet the validator: 11 of 12 are the target method short by one case or one order.

## Fix pass

- Finding 1 fixed: `p-linked-lagoons` now uses M = (1 0; 1 1), M^-1 = (1 0; -1 1), w2 = u2 - u1; B = (-2 2; 0 -5) (AM = (-2 2; -2 -3)). Recomputed by sympy and by `solve`. Keys unchanged (-5; -5, -2; (2, -1); (3, 1); 0.819). Wrong values changed: part 1 `unchanged` -4 to -3, `reversed` -3 to -1 (`sign` 5 stays); part 3 `inverse` (4, -1) to (2, -5), `unmoved` (3, -1) to (2, -3); part 4 `w-coords` (3, 2) to (5, -3). Part 3's y is now (2, -3). No other eigen file holds the new B.
- Finding 2 fixed: stop rate 0.1, restart rate 0.4, Q = (-0.1 0.4; 0.1 -0.4), part 4 at 5 hours. Graded keys changed: part 1 {0, -0.8} to {0, -0.5}; part 2 (0.75, 0.25) to (0.8, 0.2) (accept list rebuilt); part 4 0.318 to 0.266; part 5 5.40 to 8.76. Wrong values: part 1 "0, 0.8" to "0, 0.5", "-0.2, -0.6" to "-0.1, -0.4"; part 2 (0.25, 0.75) to (0.2, 0.8), (3, 1) to (4, 1); part 4 0.773/0.068/0.374/0.587 to 0.816/0.066/0.308/0.685; part 5 4.02/5.76/7.20/3.45 to 5.99/9.21/10.96/2.19. Part 3 choice: same option stays correct, text and `why` lines renumbered. Verified by exact matrix exponential, a scan in t, and the reader's numbers in `proposed.py`.
- Finding 3 fixed: part 3 question now restates the eigenvalues 0 and -0.5 and the steady state (0.8, 0.2) with Running first.
- Finding 4 fixed: `carried` line of `p-wind-pair` part 2 now says "a wrong $L_{22}$, such as $\sqrt{34}$ or 9". No value changed.
- Near-miss sample: `nearMiss` moved from plant 2 to plant 4 in `app/content/drills/ci-spiral-cells.json`; `planted-check --near-miss`: 1 drill, 6 planted solutions, 0 failures.
- Scripts: `docs/reports/problems-eigen-numbers.py` updated (new matrices, keys, slips, vocab 8.8) and exits 0 (2,189 checks, 0 failures); `mine.py` and `proposed.py` updated to the new values and exit 0 (the latter excludes problems-4 itself from its freshness grep).
- Gates: validator 0 errors, no warning on the eigen file; `grade-all --file` 18 widgets, 0 failures; voice scan 0 and 0; playthrough `--problems eigen/problems-4` desktop and `--mobile` both All passed; `manifest.json` restored.

# Problem sets 1.4 (c), eigen levels 1 to 3: second-reader findings

Scope: `app/content/courses/eigen/problems-1.json`, `-2`, `-3`: 10 problems, 47 parts (31 numeric, 4 numeric sets, 11 `expression`, 1 choice), 115 `wrong` entries. Rules: `docs/briefs/chained.md`. Pattern: `review-problems-1.4-b.md`.

Method. The author's script was run first. The 12 lessons were then skimmed screen by screen with the three reviews and three homework sets (`review-problems-1.4-a-scripts/taught.py`), for what each level teaches and for reused settings and numbers. Every part was solved by hand from its text (`review-problems-1.4-c-scripts/show.py` prints a set for reading) and again in `mine.py`, which imports nothing from the author's script and types every matrix, vector and data column from the prose. Route 1 is exact (sympy, fractions: eigenvalues, nullspaces, `LUsolve`, exact powers, symbolic determinants). Route 2 is another method: NumPy `eigvals`, `eigvalsh`, `eigh`, `svd`, `matrix_power`, `np.cov`, the paving recurrence iterated and checked against a count of the pavings, the bike chain stepped night by night, a scan of the pond's edge, and a real demeaned 31 by 4 matrix with the stated singular values. Every `wrong` value and `wrong[].tex` was rebuilt from the slip its line names, and each number printed in a `feedback`, `byKey`, `why` or `explain` string was recomputed while reading. Every typed part then went through the engine's own graders in node with the local Compute Engine (`grade-probe.mjs`: `numGrade`, `numSetGrade` and `exprGrade`, the calls `numeric.js` and `expression.js` make): the key, with more places, a letter and `=`, a true minus sign and its unit; each `accept` form; each `wrong` entry on its own key; for each of the 10 bracketed vector answers eleven other ways to type it; and 455 strings of my own (fraction against decimal, a percentage, the value the working prints after its stated rounding, a non-zero multiple of an eigenvector, a number in front of a vector, the answer one step short, the commonest slip). `try-fix.mjs` tries the content fixes below on in-memory copies with the same grader, and `proposed.py` computes their numbers. `pyodide-eigh.mjs` runs one NumPy call in the app's own Pyodide. Freshness was read by hand, helped by `fresh.py`: every matrix and vector of each problem searched in the eigen course, the three other 1.4 courses with their problem sets, exam `topic-1.4`, the stage exams and the mock papers, then every matrix again up to a transpose, a swap of rows or columns and a common factor, then the key numbers and story nouns across all of `app/content`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not say the form wanted, or refuses a sensible entry; `minor` = weak part, loose chain, loose `wrong` entry, missing restatement, wording or freshness.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-eigen-numbers.py` 1,536 checks, 0 failures, exit 0 |
| `mine.py` (reader's own keys, slips, stated numbers, set shape) | 724 checks, 0 failures; 3 CLAIM lines (findings 2, 11, 12) |
| `grade-probe.mjs` (engine graders, 46 typed parts) | 956 checks, 455 reader rows, 0 failures; 8 rows held to be faults (findings 3, 11, 14 and the engine notes); 0 form results against the reader |
| `grade-probe.mjs`, matrix parts | 0: no part asks for a matrix |
| `try-fix.mjs` (fixes of findings 3, 4, 8, 9, 10, 11, 14, 15 on in-memory copies) | 98 checks, 0 failures |
| `proposed.py` (numbers of the fixes of findings 2, 5, 6, 8, 10, 11) | 27 checks, 0 failures |
| `pyodide-eigh.mjs` (Pyodide 0.27.7, NumPy 2.0.2) | `vecs = [[-0.8, 0.6], [0.6, 0.8]]` for the crab matrix (finding 12) |
| `skills.py` | every `skills` id of each set is carried by a lesson of its level |
| validator | 0 errors; no warning on the three files; `manifest.json` unchanged |
| playthrough `--problems`, three sets, `--local-cdn` | all passed, desktop and `--mobile` |
| voice scan 35, course folder | 0 and 0; no exclamation mark, no em-dash, British spelling, no money in the sets |
| `fresh-check.mjs --file`, three sets | 0 hits; 3 advisories on `problems-3` (crab measurements against number sequences in three mock papers), read and judged chance, as the author says |

Result. All 47 keys agree with mine, and so does every one of the 115 `wrong` values and every number in a feedback or explanation string but one quotient (finding 11). Every `wrong` entry lands on its own key and has a line; no two bands touch and none is wide enough to pass a wrong method. One part refuses the value its own feedback line leads to (finding 11). No statement of theory is false in its setting; two `diagonal` lines are loose as general statements (findings 2 and 6), and one line about what `eigh` returns is not what NumPy returns (finding 12). The rest is minor: four missing restatements, two right answers refused in the form the item itself prints, three slips with no line and two reuses that `fresh-check` cannot see.

Known engine fault (a wrong matrix typed whole does not reach its `wrong` line): it touches 0 parts. No part of the three sets asks for a matrix.

## A. `problems-1`

1. `minor` | `eigen/problems-1.json` | `p-sketch-warp` | `items[0].parts[2].feedback.byKey.trace-sign`.
   The stored slip is 3 and its line says "The trace is $4 + (-1) = 3$, not $4 + 1$." But 3 is also the trace itself, the answer one step short (the learner stops before taking off $\lambda = 2$). That learner had the trace right and is told they added $4 + 1$. `p-hill-bikes` part 2 has the same slip under its own name (`trace`, 1.55).
   Fix (value and id stay): "That is the trace itself, $4 + (-1) = 3$, or $5 - 2$ with the trace taken as $4 + 1$. The two eigenvalues add to 3, so take the 2 off it."

2. `minor` | `eigen/problems-1.json` | `p-garden-path` | `items[1].parts[0].feedback.byKey.diagonal` | a general statement that holds for 2 by 2 only.
   "Only a triangular matrix shows its eigenvalues there." $\begin{pmatrix}5&1&1\\1&2&0\\-1&0&2\end{pmatrix}$ is not triangular and has eigenvalues 5, 2 and 2, its diagonal (`mine.py`, `proposed.py`). l2 screen 4 says only "A triangular matrix always shows its eigenvalues on its diagonal".
   Fix: "Those are the diagonal entries. A triangular matrix shows its eigenvalues there, but $\mathbf{A}$ is not triangular."

3. `minor` | `eigen/problems-1.json` | `p-sketch-warp` | `items[0].parts[4].widget` | the form of the part's own `correct` line is refused.
   `16(3,1)+(2,1)`, the line "$2^4(3, 1) + 1^4(2, 1)$" typed as it stands, is refused with the engine's line "That is a single value. The answer has 2 components." The learner typed two vectors of two components. Engine class of `review-problems-1.4-a.md` finding 6 and `-b` findings 5, 8 and 13.
   Fix (`try-fix.mjs`): `accept` gains `"16(3, 1) + (2, 1)"` and `"(48, 16) + (2, 1)"`. Then `16(3,1)+(2,1)`, `2^4(3,1)+1^4(2,1)` and `(48,16)+(2,1)` are accepted, `8(3,1)+4(2,1)` is still refused, and `one-warp`, `times-four` and `carried` keep their keys.

4. `minor` | `eigen/problems-1.json` | `p-lazy-frog` | `items[3].parts[3].widget.wrong` | the two right values in the other order have no line.
   The part asks for the eigenvalue of $(1, -2, 1)$ first. `(0.5, 0)` gets the generic line ("Apply $\mathbf{L}$ ... to each vector"), which is what the learner did.
   Fix (`try-fix.mjs`, lands on the new key, no other entry moves): add `{ "id": "order", "tex": "(0.5, 0)" }` and `byKey.order`: "Those are the two eigenvalues in the other order. Type the one for $(1, -2, 1)$ first."

5. `minor` | `eigen/problems-1.json` | `p-garden-path` | `items[1].parts[3].question` | missing restatement.
   Part 4 restates $c_1$ and $c_2$ but not the eigenvalues 3 and $-2$ or the eigenvectors, which stand only in parts 1 to 3. (The recurrence alone also gives the key in nine additions, $1, 1, 7, 13, 55, 133, 463, 1261, 4039, 11605, 35839$, so the chain is not forced; the explanation uses that as its check. Accept.)
   Fix: "Using $c_1 = \tfrac35$ and $c_2 = \tfrac25$ from part 3, with eigenvalue 3 for $(3, 1)$ and $-2$ for $(-2, 1)$, find $t_{10}$, the number of ways to pave a path 10 metres long. Give a whole number."

## B. `problems-2`

6. `minor` | `eigen/problems-2.json` | `p-oval-pond` | `items[0].parts[1].feedback.byKey.diagonal` | a general statement without its hypothesis.
   "$\mathbf{A}$ is not diagonal, so its eigenvalues differ from them." True here because $\mathbf{A}$ is symmetric: $\det(\mathbf{A} - \lambda\mathbf{I}) - (a - \lambda)(d - \lambda) = -b^2$. Without symmetry it fails: $\begin{pmatrix}5&2\\0&8\end{pmatrix}$ has eigenvalues 5 and 8 (`proposed.py`), and l2 has just taught that case.
   Fix: "Those are the diagonal entries. $\mathbf{A}$ is symmetric and not diagonal, so its eigenvalues differ from them."

7. `minor` | `eigen/problems-2.json` | `p-oval-pond` | `items[0].parts[3].question` | missing restatement.
   Part 4 restates the direction $(2, -1)$ but not its eigenvalue, 4, which the `generic` line and the explanation both use.
   Fix: "Along the direction $(2, -1)$ from part 3, the eigenvector for 4, how far is the edge from the centre? Give metres as a whole number."

8. `minor` | `eigen/problems-2.json` | `p-river-gauges` | `items[1].prose`, part 5 | freshness; the author's report is wrong on this point.
   `homework-4` `h-long-psd` ("A covariance matrix that will not factor") is the same setup in the same course: three series with correlations 0.9, 0.9 and a stated 0.2, a mix with variance $-0.2$, the lowest correlation that data could give (0.62), and the conclusion that no data give the matrix. Here: 0.8, 0.8 and a reported 0.2, a mix with variance $-0.16$, the bound 0.28, the same conclusion. Both bounds are $\rho^2 - (1 - \rho^2)$. `docs/reports/problems-eigen.md` says the eigen course does not treat three-series correlation limits. The homework is level 4 and by Cholesky, the problem is level 2 and by leading determinants and a null vector, so the learner meets the problem first: accept the setup, but the two should not share the reported value. `fresh-check` lists nothing.
   Fix (`proposed.py`, `try-fix.mjs`): the report claims $r = 0.15$ (prose and part 5 question). Parts 1 to 4 do not change. Part 5: key $-0.26$ ($2 \times 0.15 - 0.56$); `dropped-sign` 0.26; `bound` 0; `no-double` 2.15 ($4.56 - 2.41$). `correct`: "... $= 2r - 0.56$. At $r = 0.15$ that is $-0.26$, a negative variance." `dropped-sign`: "... which at $r = 0.15$ is $0.3 - 0.56 = -0.26$." `bound`: "... The report's $r = 0.15$ gives $2(0.15) - 0.56 = -0.26$." `no-double`: "... Double them: $4.56 + 2(-2.41) = -0.26$." Explain: "So $-0.26$ shows that $r = 0.15$ cannot be right."

9. `minor` | `eigen/problems-2.json` | `p-river-gauges` | `items[1].parts[3].widget.wrong` | the answer one step short has no line.
   $-1.28$ ($0.8a = -1.28$, not yet divided by 0.8) gets the generic line, "Write row 1 ... and set it to 0", which is what the learner did.
   Fix (`try-fix.mjs`): add `{ "id": "no-divide", "value": -1.28, "tol": { "abs": 0.0005 } }` and the line "That is $0.8a$. Row 1 gives $0.8a = -1.28$, so divide by 0.8."

10. `minor` | `eigen/problems-2.json` | `p-tank-thermometers` | `items[2].parts[4]` | freshness.
    The weights $(0.5, 0.3, 0.2)$ are the weights of exam `topic-1.4` `a-portfolio-dot`, of `vectors/l4` screen 8 and of `vectors/problems-1` `p-active-bets` (and of three files outside 1.4). The task differs each time; only the vector is shared.
    Fix (`proposed.py`, `try-fix.mjs`; $(0.6, 0.25, 0.15)$ is in no content file): $\mathbf{w} = (0.6, 0.25, 0.15)$. Key 1.89. `correct`: "$\mathbf{d} = (\tfrac{4}{15}, -\tfrac{1}{12}, -\tfrac{11}{60})$, with $|\mathbf{d}|^2 = \tfrac{67}{600} = 0.1117$. So $\mathbf{w}^T\mathbf{S}\mathbf{w} = \tfrac53 + 2 \times 0.1117 = 1.89$." `no-eigenvalue` 1.78 ($\tfrac53 + 0.1117 = 1.7783$), line "... adds $2|\mathbf{d}|^2 = 2 \times 0.1117 = 0.223$."; `d-only` 0.22; `no-cov` 1.335 with the same band of 0.005, so that 1.33 and 1.34 both land, line "... The off-diagonal 1s add $2(0.15 + 0.09 + 0.0375) = 0.555$." Explain: "Directly: $3(0.445) + 2(0.2775) = 1.89$."

## C. `problems-3`

11. `wrong` | `eigen/problems-3.json` | `p-crab-sizes` | `items[1].parts[4]` | the part refuses the value its own feedback line leads to.
    `correct`: "$\sqrt{250} = 15.81$, so crab 1 is $20/15.81 \approx 1.26$". But $20/15.81 = 1.265022$, which is 1.27 to the 2 places asked for. The exact value is $1.264911$, a hair under the rounding edge, so a learner who rounds $\sqrt{250}$ to 15.81 as the line does types 1.27 and is refused on no line (`grade-probe.mjs`). The `variance` line prints 15.81 too.
    Fix (`proposed.py`, `try-fix.mjs`): ask for 3 places, where every route agrees: exact $1.264911$, by 15.81 $1.265022$, by 15.811 $1.264942$, all 1.265. Question: "... Give 3 decimal places." `answer` 1.265, `tol` 0.0005. `wrong`: `variance` 0.08, `total` 1.131 ($20/\sqrt{312.5} = 1.13137$), `pc2-sd` 2.53 ($20/\sqrt{62.5} = 2.52982$), each with `tol` 0.0005. `correct`: "The standard deviation of the scores is $\sqrt{250} = 15.811$, so crab 1 is $20/15.811 \approx 1.265$ standard deviations above average." `variance`: "... Divide by the standard deviation, $\sqrt{250} = 15.811$." Explain: "So $20/\sqrt{250} \approx 1.265$." Then 1.265, 1.2649 and 1.26502 are accepted, 1.26, 1.27, 1.264 and 1.266 are refused, and each slip lands on its key.

12. `minor` | `eigen/problems-3.json` | `p-crab-sizes` | `items[1].parts[2].question` | a line about code that is not what the code does.
    "`vals, vecs = np.linalg.eigh(S)` returns `vals = [62.5, 250.]` and `vecs = [[0.8, -0.6], [-0.6, -0.8]]`". For this matrix NumPy returns `vecs = [[-0.8, 0.6], [0.6, 0.8]]`, in the app's own Pyodide (`pyodide-eigh.mjs`, NumPy 2.0.2) and in the venv (2.5.3): both columns have the other sign, and PC1 needs no flip. The printed columns are valid eigenvectors and l12 says a library may return either sign, so no key is affected; the sentence should not state it as what this call returns.
    Fix: "A colleague's run of `vals, vecs = np.linalg.eigh(S)` gave `vals = [62.5, 250.]` and `vecs = [[0.8, -0.6], [-0.6, -0.8]]`, with eigenvectors as columns. A library may return either sign. Using the eigenvalues from part 2, ..." The rest stays.

13. `minor` | `eigen/problems-3.json` | `p-site-anomalies` | `items[2].parts[2].question`, `parts[3].question` | missing restatement.
    Part 3 says "Using part 2" without the 0.962. Part 4 says "the number of components from part 3" without the 3, so a slip in part 3 carries into part 4 (the `rank-two` line catches one case only).
    Fix: part 3: "The service keeps the fewest components that explain at least 99% of the variance. Two explain 0.962, from part 2. How many does it keep? Give a whole number." Part 4: "Part 3 keeps 3 components, which gives the best rank-3 approximation `Xk`. What is the energy of the error `Xc - Xk`, the sum of its squared entries? Give a whole number."

14. `minor` | `eigen/problems-3.json` | `p-branch-sales` | `items[0].parts[3].widget` | a number times a vector.
    `5(0.8,0.6,0)`, the form of the part's own `carried` line ("the column is $5\mathbf{u}_1$"), is refused with "That is a single value. The answer has 3 components." Part 3 of the same problem accepts `0.1(8,6,0)`, because its `accept` list holds a form of that shape.
    Fix (`try-fix.mjs`): `accept` gains `"5(0.8, 0.6, 0)"`. Then `5(0.8,0.6,0)`, `\sqrt{25}(0.8,0.6,0)` and `0.5(8,6,0)` are accepted, `5(8,6,0)` is still refused, and `u-only` and `carried` keep their keys.

15. `minor` | `eigen/problems-3.json` | `p-site-anomalies` | `items[2].parts[3].widget.wrong` | a likely slip has no line.
    Parts 1 to 3 all divide by $n - 1 = 30$. A learner who keeps doing so types 0.3, the variance of PC4, and gets the generic line.
    Fix (`try-fix.mjs`): add `{ "id": "variance", "value": 0.3, "tol": { "abs": 0.0005 } }` and the line "That is PC4's variance, $s_4^2/30$. Energy is the plain sum of squares, with no division by $n - 1$."

## Per set

- Coverage: every lesson of each level is drawn on and each problem draws on at least two. Level 1: sketch warp l1 to l3; garden path l2, l3; hill bikes l2, l4; lazy frog l1, l3, l4. Level 2: oval pond l5, l6, l8; river gauges l6, l7; tank thermometers l5, l7. Level 3: branch sales l9, l10; crab sizes l11, l12; site anomalies l10 to l12.
- Only taught ideas. Three things from outside the level are given, not asked: the paving recurrence and its matrix (prose of `p-garden-path`), the area $\pi ab$ (`p-oval-pond` part 5), and $\mathbf{L} = \tfrac12(\mathbf{I} + \mathbf{M})$, whose eigenvalues follow from l1's definition in one line. Level 2 divides covariances by $n$ and level 3 by $n - 1$, as l7 and l11 do; no level 2 part computes a covariance from data.
- Hypotheses: each general statement carries what it needs, but for findings 2 and 6. Powers by eigenvectors say "the eigenvalues differ, so the eigenvectors are independent" (`p-garden-path` 4); perpendicular axes and the repeated eigenvalue say "symmetric" (`p-oval-pond` 3, `p-tank-thermometers` 3 and 5); the leading-determinant test is stated for this symmetric $\mathbf{C}$ with "exactly when"; "every Markov matrix has eigenvalue 1" is true for columns adding to 1; the settling rule says "every eigenvalue other than 1 is below 1 in size", and the frog's start does have a part along $(1, -2, 1)$ (coefficient $\tfrac14$, restated in part 5); PCA variances $s_i^2/(n - 1)$ are for the demeaned `Xc`. No part uses power iteration.
- Chains: all 10 are real chains with one right answer a part. Every eigenvector part fixes its scale ("second entry 1", "as $(2, b)$", "entries adding to 1", the given $\mathbf{v}_1$, the sign rule), and the grader refuses other multiples (`(4,2)`, `(-2,1)` for $(2,-1)$, `(-0.8,-0.6,0)`). Every part's result is used later. Loose ends: findings 5, 7 and 13, and `p-tank-thermometers` part 2, which names part 1's vector only to note a perpendicularity it does not use (the author's report says so; accept, since part 3 needs both results).
- Typed parts: 17 of 18, 15 of 15, 14 of 14. The one choice part is a judgement; its key is the longest option (100 characters against 33 to 68), which a fix pass could even out.
- Grader, numeric parts (31): every key grades correct with more places, a letter and `=`, a true minus sign, its unit and, where not whole, as a fraction (`3/10`, `11/20`, `5/16`, `5/3`, `25/29`, `25/26`, `-8/5`) or a percentage (`30%`, `31.25%`, `86.2%`, `96.2%`). Every part that asks for places refuses the value one place short or truncated (`0.313`, `1.67`, `1.666`, `18.84`, `0.86`, `0.961`), and every part refuses each slip. Slips rounded as the question asks land (`35020`, `182`, `440`, `38`, `113.10`, `75.40`).
- Grader, sets (4): read in either order, as `3, -2`, `(3, -2)`, `3 and -2` and `x = 3, x = -2`; one value or three gets the count line.
- Grader, vectors (10) and the polynomial: accepted in all nine bracket and layout forms, a row where a column is meant included, with entries as fractions or decimals, and as a number in front or underneath where `accept` holds such a form (`(3,2)/5`, `(1,2,1)/4`, `(8,6,0)/10`, `(3,4)/5`); refused reversed or one entry short, on the right line. $\det\mathbf{C}$ is accepted expanded, factored either way, unexpanded from the cofactor line and with fractions; the negated polynomial, which has the same roots, is refused.
- `wrong` lines: none names a number the learner did not type, but for finding 1's second reading of 3. Banded slips (0.075, 181.5, 440.25, 35019.8, 37.74, 1.8, 0.09) have lines that name the method, not the figure.
- Freshness: no matrix of the sets stands in the 1.4 courses, exam `topic-1.4`, the stage exams or the mock papers, also up to a transpose, a swap or a common factor (`fresh.py`). Findings 8 and 10 are the two reuses. Read and accepted: `p-hill-bikes` part 4 is l4 screen 3's "smallest $k$" on new numbers (the author's call); `p-lazy-frog` part 3 is l4 screen 4's question on a three-state chain; `p-tank-thermometers` part 1 uses the row-sum argument that l10 screen 9 and `homework-3` `h-factor` use a level later; paving a path with slabs is the story of two coding drills outside 1.4 (`dsa-footpath-slabs`, `ci-paving-ways`), with other shapes and a coding task.
- Voice: British English, no exclamation marks, no em-dashes, no explanation over three sentences.

## Counts

| tag | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| wrong | 0 | 0 | 1 |
| unclear | 0 | 0 | 0 |
| minor | 5 | 5 | 4 |

Clean problems (no finding): `p-hill-bikes`.

Finding classes seen three times or more: a later part that does not restate what it needs (4 parts, findings 5, 7, 13); a right answer or a slip typed as a number times a vector, or a sum of such, met with "That is a single value" (3 parts here, findings 3 and 14 and the engine note; third review of topic 1.4 to see it); a slip one step short, in the other order or carried from the parts before with no line (3 parts, findings 4, 9, 15). Seen twice: a general statement without its hypothesis (findings 2, 6); reuse that `fresh-check` cannot see (findings 8, 10; fourth 1.4 review to see it).

## Engine

- A number times a vector is read only when an `accept` form has that shape (findings 3, 14). A slip typed that way never reaches its line: `0.2(-3,-4)` on `p-crab-sizes` part 3 gets "That is a single value", not `no-flip`.
- Not read as a number, so Check stays unavailable: `r>0.28` on `p-river-gauges` part 3, whose question asks "above what value of $r$"; `1.26 standard deviations` on `p-crab-sizes` part 5; `λ = 3, λ = -2` in a set field. `18.85 m^2` on `p-oval-pond` part 5 is the author's own inbox bullet.
- A feedback quotient that rounds the other way from its printed operands passed the author's script (finding 11): a rule for `numbers_lib.py`.
- `fresh-check.mjs` misses a setup met again with other numbers in a later level of the same course (finding 8) and a weights vector shared with the topic exam (finding 10).
- The known matrix fault is not raised again: 0 parts.

## Fix pass

Every changed number was recomputed by two routes before it was written, and sits in `docs/reports/problems-eigen-numbers.py` (exact sympy, then NumPy: `eigh`, `svd`, `det` at three values of `c`, a regression of C on A and B, `np.cov`): 1,613 checks, 0 failures, exit 0 with the scratchpad venv. The script's new checks: a sum of a number times a vector and a vector is parsed (finding 3); the crab feedback quotient is 1.265 by 15.811, by 15.81 and exactly, and part 3 is worded as a colleague's run because this NumPy (2.5.3) and the app's Pyodide (NumPy 2.0.2, `pyodide-eigh.mjs`: `vecs = [[-0.8, 0.6], [0.6, 0.8]]`) both return the other sign; a stale-value check over the re-authored gauges item (no 0.8, 0.28, 1.28, 1.6, 0.16, 0.36, 0.64, 0.72, correlation or standardis left), over the tank part 5 (no 0.0467, 0.093, 0.62, 0.38, 0.31, 1.76) and over crab part 5 (no 15.81, 1.26 or 1.13 left).

Real grader (`numGrade`, `exprGrade` with the local Compute Engine, scratch `check-real.mjs`): 178 rows over the 13 touched parts; every key, every `accept` form and every `wrong` entry lands on its own id; the 4 rows that differ are my own wrong guesses about the grader, all sensible: `253/200` (= 1.265) accepted, `12.5%` accepted for 0.125, `25%` lands on `unexplained`, and `(-0.125,-0.25)` gets the length line. Reader's scripts: `try-fix.mjs` 101 checks, its 4 fails are the "as it stands" rows now accepted (findings 3 and 14 closed) and the old gauges part 4; `grade-probe.mjs` 979 checks, 56 fails, all strings typed from old values of the re-authored gauges, the tank part 5 and the crab part 5, or findings now closed (`(0.5,0)` now lands on `order`, `0.3` on `variance`, `1.27` is refused as it should be for 3 places); `proposed.py` 27 checks, 0 failures. `mine.py` types the old prose and stops on the new accept form and the new item, so it was not rerun.

Status: fixed 15 findings, disputed 0, deferred 0 (the engine notes stay in the inbox: no content change).

1. warp part 3, fixed: `byKey.trace-sign` reads as proposed. Value 3 and id stay.
2. garden part 1, fixed: `byKey.diagonal` reads as proposed (basis: the 3 by 3 matrix with rows (5, 1, 1), (1, 2, 0), (-1, 0, 2) has eigenvalues 5, 2, 2 and is not triangular, so "only" was false).
3. warp part 5, fixed: `accept` gains `16(3, 1) + (2, 1)` and `(48, 16) + (2, 1)`. Graded accepted: `16(3,1)+(2,1)`, `2^4(3,1)+1^4(2,1)`, `(48,16)+(2,1)`; `8(3,1)+4(2,1)` still refused on the length line; `one-warp`, `times-four`, `carried` keep their ids.
4. frog part 4, fixed: `wrong` gains `order` `(0.5, 0)` and `byKey.order`; graded on `order`, the key and the other three unchanged.
5. garden part 4, fixed: the question restates eigenvalues 3 and -2 and their eigenvectors, as two sentences (the first draft gave a long-sentence warning).
6. oval pond part 2, fixed: `byKey.diagonal` says "symmetric and not diagonal" (basis: for symmetric $\mathbf{A}$, $\det(\mathbf{A} - \lambda\mathbf{I}) - (a - \lambda)(d - \lambda) = -b^2$).
7. oval pond part 4, fixed: the question restates "the eigenvector for 4".
8. river gauges, fixed, re-authored (id and `skills` kept; progress keys on the id): the setting is now three strain gauges on a bridge cable with $\mathbf{K} = \begin{pmatrix}4&2&1\\2&3&1\\1&1&c\end{pmatrix}$ and a planned $c = 0.5$. Parts: 1 second pivot (key 2; `multiplier-one` 1, `multiplier-two` -1); 2 third pivot $c - d$, $d$ (key 0.375, band 0.0005; `one-step` 0.25, `big-multiplier` 0.5, `added` 0.125); 3 null vector at $c = 0.375$ typed $(a, b, 1)$ (key $(-0.125, -0.25, 1)$ with 6 `accept` forms; `sign` $(0.125, 0.25, 1)$, `swapped` $(-0.25, -0.125, 1)$, `no-b` $(-0.25, -0.25, 1)$); 4 $\mathbf{w}^T\mathbf{K}\mathbf{w}$ at $c = 0.5$ (key 0.125; `c-only` 0.5, `sign` 1.625, `boundary` 0.375); 5 the share of C's variance that A and B explain (key 0.75; `unexplained` 0.25, `not-scaled` 0.875). Every number by two routes: pivots by exact elimination and by $\det\mathbf{K}/$corner; null vector by exact nullspace and the last right singular vector; part 4 by $\mathbf{K}\mathbf{w} = (0, 0, 0.125)$ and NumPy; part 5 by $1 - 0.125/0.5$ and the $R^2$ of a NumPy regression of C on A and B ($\beta = (0.125, 0.25)$). Skeleton differs from `h-long-psd` (no correlations, no 0.2, no 0.9, no Cholesky, no negative variance): pivots, a null mix, then variance left. Lessons drawn on: l6 (pivots) and l7 (zero variance, redundant asset).
   Freshness grep over all of `app/content` (whitespace-normalised, `fresh2.py` also tries every row and column permutation, the transpose and a wildcard for $c$ over the 126 three-by-three matrices): the matrix rows `4&2&1`, `2&3&1`, the vector `(-0.125,-0.25,1)` and `(-1/8,-1/4,1)`, `8c-3`, `c-0.375`, "strain gauge", "bridge cable" and "0.125A" occur only in `courses/eigen/problems-2.json`; no other matrix matches. The bare numbers 0.375 and 1.625 occur in about 150 and 20 unrelated files (sums of eighths, an AR coefficient, a decimal), none with this setting; read and judged chance. `fresh-check.mjs --file`: 0 hits.
9. gauges part 4, closed by the re-authoring: the slip of one step short is now a line in each new part (`one-step`, `no-b`, `not-scaled`, `boundary`).
10. tank part 5, fixed: $\mathbf{w} = (0.6, 0.25, 0.15)$, key 1.89 (exact 189/100 = 5/3 + 2 x 67/600), `no-eigenvalue` 1.78, `d-only` 0.22, `no-cov` 1.335 (band 0.005 as before, so 1.33 and 1.34 land), and `correct`, three `byKey` lines and `explain` follow as proposed. (0.6, 0.25, 0.15) stands in no other file.
11. crab part 5, fixed: asks 3 decimal places; key 1.265, tol 0.0005; `variance` 0.08, `total` 1.131, `pc2-sd` 2.53, each tol 0.0005; `correct`, `byKey.variance` and `explain` print 15.811 and 1.265. Graded accepted: 1.265, 1.2649, 1.26502, 1.26494; refused: 1.26, 1.27, 1.266, 1.264; each slip on its id. 20/15.811 = 1.264942, 20/15.81 = 1.265022, exact 1.264911: all 1.265.
12. crab part 3, fixed: "A colleague's run of ... gave ... A library may return either sign." The printed columns are valid eigenvectors; the real call returns the opposite sign in both columns (Pyodide NumPy 2.0.2 and the venv), so no sign is claimed for the call. Key and `wrong` unchanged.
13. site anomalies parts 3 and 4, fixed: part 3 restates "Two explain 0.962, from part 2"; part 4 restates "Part 3 keeps 3 components, which gives the best rank-3 approximation".
14. branch sales part 4, fixed: `accept` gains `5(0.8, 0.6, 0)`. Graded accepted: `5(0.8,0.6,0)`, `\sqrt{25}(0.8,0.6,0)`, `0.5(8,6,0)`; `5(8,6,0)` refused on the length line; `u-only` and `carried` keep their ids.
15. site anomalies part 4, fixed: `wrong` gains `variance` 0.3 and `byKey.variance`, as proposed. Its question now ends "Give the exact value." in place of "Give a whole number": a band of 0.0005 on 0.3 trips the validator's rounding rule against a whole-number question, and a band of 0.5 trips the wide-band rule; the key 9 is unchanged.

Graded answers, bands, `accept` forms and items that changed:
- `problems-1` `p-sketch-warp`: part 3 line text only; part 5 `accept` +2. `p-garden-path`: part 1 line text, part 4 question. `p-lazy-frog`: part 4 `wrong` +1 (`order`).
- `problems-2` `p-oval-pond`: part 2 line text, part 4 question. `p-river-gauges`: whole item re-authored (prose, 5 parts, all keys, bands, `accept` forms and `wrong`). `p-tank-thermometers`: part 5 question, key 1.76 to 1.89, `no-eigenvalue` 1.71 to 1.78, `d-only` 0.09 to 0.22, `no-cov` 1.14 to 1.335, `correct`, two `byKey` lines, `explain`.
- `problems-3` `p-branch-sales`: part 4 `accept` +1. `p-crab-sizes`: part 3 question; part 5 question, key 1.26 to 1.265, tol 0.005 to 0.0005, `variance` 0.08, `total` 1.13 to 1.131, `pc2-sd` 2.53, tols 0.0005, `correct`, `byKey.variance`, `explain`. `p-site-anomalies`: part 3 and part 4 questions, part 4 `wrong` +1 (`variance`).

Gates (from `app/`): validator 0 errors, 4,853 warnings, none on the three files (the same total as before the pass); `manifest.json` not committed. Voice scan 35: 0 and 0 on the repo and on the eigen folder. `playthrough --problems eigen/problems-1`, `-2`, `-3`, each with and without `--mobile` and `--local-cdn`: all six passed.

# Problem sets 1.4 (a), vectors levels 1 to 3: second-reader findings

Scope: `app/content/courses/vectors/problems-1.json`, `problems-2.json` and `problems-3.json`: 12 problems, 53 parts (28 numeric, 22 `expression`, 3 choice). Patterns: `review-problems-1.5-a.md`, `review-holes-1.6-2.1.md`, `review-delta-holes.md`.

Method. The author's script was run first. The twelve lessons l1 to l12 were skimmed screen by screen, with the three reviews and three homework sets (`taught.py`), for what each level teaches and for reused settings and numbers. Every part was solved from its text before its answer was read, by hand and again in `review-problems-1.4-a-scripts/mine.py`, which imports nothing from the author's script and types every vector and matrix from the prose (NumPy, `np.linalg.solve`, `inv`, `det` and `matrix_rank`, sympy for the two matrices in $k$, the drone's whole flight checked as vectors). Every `wrong` value and every `wrong[].tex` was re-derived from the slip its line names, and each number printed in a `feedback` or `explain` string recomputed. Every typed part then went through the engine's own graders in node with the local Compute Engine (`grade-probe.mjs`: `numGrade` for the 28 numeric parts, `exprGrade`, the call `expression.js` makes, for the 22 expression parts): the stored answer, each `accept` form, each `wrong` entry on its own key, typed strings of my own, and for every vector or matrix answer a fixed list of other ways to type it (round, square and angle brackets, MathLive's `\left\lbrack` spelling, a column, a row, no brackets, semicolons, entries reversed, the transpose, a flat row). Because nine parts ask for a matrix typed whole, `matrix-forms.mjs` retyped each of their `wrong` matrices in the form the question asks for, and `mathlive-typed.mjs` typed 16 answers key by key into the app's real math field (MathLive 0.105.0 in headless Chromium) and graded the LaTeX the field holds.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways or does not say the form wanted; `minor` = weak part, loose `wrong` entry, missing hypothesis, label or freshness.

## Tool results

| check | result |
|---|---|
| author's script `problems-vectors-numbers.py` (scratchpad venv) | 820 checks, 0 failures, exit 0 |
| `mine.py` (reader's own keys, slips, stated numbers, set shape) | 472 checks, 0 failures; 1 note read (finding 3) |
| `grade-probe.mjs` (engine graders, 50 typed parts) | 969 checks, 0 failures; 33 rows held to be faults (findings 1 to 7) and 36 form results against the reader (finding 1) |
| `matrix-forms.mjs` (the 20 `wrong` matrices retyped four ways; 31 right matrices with an entry written another way) | 0 of 80 land on their own key; 5 of 31 right matrices refused (findings 1, 2) |
| `mathlive-typed.mjs` (16 answers typed into the real math field) | the field holds `\left\lbrack\left\lbrack1,0\right\rbrack,\left\lbrack0.25,1\right\rbrack\right\rbrack`; findings 1 and 2 reproduce |
| `try-fix.mjs` (the content fixes of findings 1 and 2 on in-memory copies) | 40 of 40 wrong matrices land on their key; 5 of 5 factorised typings accepted |
| `proposed.py` (numbers of the fixes below) | 11 checks pass |
| `fresh.py` (story nouns, vectors and matrices against the course and exams `topic-1.4`, `stage-1`) | read by hand; finding 8 |
| validator | 0 errors; no warning on the three files; `manifest.json` unchanged |
| playthrough `--problems` 1, 2, 3 with `--local-cdn` | all passed, desktop and `--mobile` (the hook sets the stored `pmatrix`, so it cannot see finding 1) |
| voice scan 35, `vectors` | 0 and 0 |
| `fresh-check.mjs --file` 1, 2, 3 | 0 hits; 8 advisories on `problems-1` (shared small returns), none on the others |

Result. All 53 keys agree with mine, and so does every one of the 121 `wrong` values and every number in a feedback or explanation string; no statement of theory is false. The faults are in grading. On all nine matrix parts a wrong matrix typed as the question asks is told something untrue and never reaches the line written for it (finding 1), and one right matrix is refused (finding 2). Two questions can be read two ways (findings 3, 4).

## Findings

1. `wrong` | `vectors/problems-2.json`, `problems-3.json` | all nine matrix parts | no `wrong` line can fire, and the line shown is false.
   Parts: `p-italic-letters` 1 and 3, `p-site-plan` 1 and 2, `p-goat-feed` 1 and 3, `p-colour-sensor` 2, `p-engraver-dial` 1 and 4. Each says "Type it row by row, as `[[a, b], [c, d]]`" and stores its answer and its `wrong[].tex` as `\begin{pmatrix}...\end{pmatrix}`, with the bracket form only in `accept`. The grader reads `[[a, b], [c, d]]` as a list of lists, not as a matrix: it matches the `accept` form list against list, never matches a `pmatrix`, and then takes its shape to be "a single value". So every wrong matrix typed in the asked form gets the key `length` and the engine's line "That is a single value. The answer has 2 rows and 2 columns." The learner typed a 2 by 2 matrix, and the slip line is never shown.
   Evidence: `matrix-forms.mjs`: the 20 `wrong` matrices, each typed as asked, as MathLive spells it, with bare `\lbrack` and with round brackets: 0 of 80 land on their key. `mathlive-typed.mjs`: typing `[[1,0],[0.25,1]]` (the `rows` slip of `p-italic-letters` part 1) into the real field gives the line above; so do `[[1.5,0.25],[0,1]]` (`order`), `[[0.8,0.6],[-0.6,0.8]]` (`clockwise`), `[[0.3,-0.1],[-0.2,0.4]]` (`no-divide`) and `[[7,3k+1],[5,2k+1]]` (`order`). A wrong matrix no entry names (`[[4, -1], [-2, 3]]`) gets the same line. Round brackets, `((3, -1), (-2, 4))`, get "Your answer has 2 components. The answer has 2 rows and 2 columns." The author's routing check and the playthrough both pass because they feed the stored `pmatrix`, which no learner can type.
   Fix (content, works today, `try-fix.mjs` 40 of 40): store each of the 20 `wrong[].tex` in the asked form, for example `"[[1, 0], [0.25, 1]]"` for `rows`, `"[[7, 3k+1], [5, 2k+1]]"` for `order`; and give each of the nine parts a `byKey.length` line so that an unnamed wrong matrix is not told it is a single value: the part's `generic` line followed by "Type 2 rows of 2 entries, as `[[a, b], [c, d]]`." The 20 entries: italic 1 `rows`; italic 3 `order`, `entrywise`; site 1 `clockwise`, `swapped`; site 2 `square`, `entrywise`; goat 1 `transposed`; goat 3 `no-divide`, `no-negate`, `transposed`, `times-det`; sensor 2 `no-divide`, `times-det`, `no-negate`; engraver 1 `order`, `entrywise`; engraver 4 `no-negate`, `unswapped`, `order`.
   Fix (engine, the real one): read a list of equal-length lists as a matrix in `grade.js` `itemsOf`, so the bracket form is compared entry by entry with a `pmatrix` and has a shape. Raised in `docs/BACKLOG-INBOX.md`.

2. `wrong` | `vectors/problems-3.json` | `p-engraver-dial` | part 1.
   For the same reason the bracket form is compared with `accept` as a whole list, not entry by entry at seeded points. A right matrix with an entry arranged another way is refused: `[[2(k+3), k+2], [5, 2]]` and `[[2(3+k), 2+k], [5, 2]]` get "That is a single value. The answer has 2 rows and 2 columns." (typed into the real field too). The same matrix as a `pmatrix` is accepted. `[[2k+6, k+2], [5, 2]]` and `[[6+k\cdot2, 2+k], [5, 2]]` pass. The same fault refuses `[[1.5, 1.5\times0.25], [0, 1]]` in `p-italic-letters` part 3 and `[[\frac{0.3}{0.1}, -1], [-2, 4]]` in `p-goat-feed` part 3, which are less likely to be typed.
   Fix (content): add `"[[2(k+3), 2+k], [5, 2]]"` to `accept` of part 1 (`try-fix.mjs`: the five factorised typings are then accepted and both slips still refused). The engine fix of finding 1 removes the cause.

3. `unclear` | `vectors/problems-2.json` | `p-site-plan` | part 4.
   "What angle does the pipe make with the ground $x$-axis?" A pipe is a line with no direction, and the angle between a line and an axis is usually given as the acute one: $180° - 126.9° = 53.1°$. That value is the stored `clockwise` slip, so a learner who turns the step correctly to $(-6, 8)$ and gives the acute angle is marked wrong and told "That turns the step the wrong way, with $\mathbf{R}^T$."
   Fix: question "A straight pipe runs from the borehole, at plan point $(10, -5)$ from part 3, to a well at plan point $(10, 5)$. What angle does the step from the borehole to the well make with the ground direction $(1, 0)$? Give degrees between 0 and 180, to 1 decimal place." `byKey.clockwise`: "That is the angle of $(6, 8)$: the step turned the wrong way, with $\mathbf{R}^T$, or the smaller angle between the pipe's line and the axis. From borehole to well the step is $\mathbf{R}(0, 10) = (-6, 8)$, at $126.9°$ from $(1, 0)$."

4. `unclear` | `vectors/problems-2.json` | `p-factor-risk` | part 3.
   "find $\mathbf{F}\mathbf{e}$. Give it as $(x, y)$." The entries are 0.02415 and 0.00472, the question asks for no rounding, and an `expression` answer is compared exactly. `(0.0242, 0.0047)` is refused with the generic line "Dot each row of $\mathbf{F}$ with $\mathbf{e}$", which the learner did. Part 4 does state its form ("to 5 places").
   Fix: question ends "Give it as $(x, y)$, with each entry to 5 decimal places."

5. `minor` | five "Give a percentage" parts | the decimal the working gives is refused with a line about the method.
   `problems-1` `p-active-bets` 2, `p-stress-hedge` 1, 3 and 4; `problems-2` `p-factor-risk` 5. The prose gives returns as decimals (0.02, $-0.12$), so the working ends in a decimal, and each `feedback.correct` prints it ("$= -0.0055$"). Typed as $-0.0055$ in a `unit: "%"` field it is read as $-0.0055\%$ and refused with the generic line ("Multiply each active weight by its market's return, then add."). The same class was raised for `regression` problem sets.
   Fix: end each of the five `generic` lines with "If your working ends in a decimal such as 0.012, type it in per cent: 1.2."

6. `minor` | three parts | the answer as a number times a vector or matrix is refused.
   `problems-1` `p-drone-crosswind` 1: `\frac{1}{5}(3,4)` gets the key `length`. `problems-3` `p-goat-feed` 3: `10[[0.3, -0.1], [-0.2, 0.4]]`, and `p-colour-sensor` 2: `2[[0.7, -0.3], [-0.2, 0.8]]`, get the generic line "Swap the diagonal, negate the other two entries, then divide", which is what the learner has written.
   Fix: goat 3 and sensor 2, add to the question "Work out the four entries." Drone 1, add "with both entries worked out". The engine limit is raised in the inbox.

7. `minor` | `vectors/problems-3.json` | `p-engraver-dial` | part 3.
   The `added` slip is $-\tfrac{22}{9} = -2.444$ with a band of 0.5, wide so that $-2$ lands on it. But $k = -2$ is also the plain sign slip (solving $2 + k = 0$), and that learner is told "That solves $22 + 9k = 0$, from adding the products."
   Fix: `byKey.added`: "That solves $22 + 9k = 0$, from adding the products, or $2 + k = 0$, a sign slip. The determinant is $2 - k$, which is 0 at $k = 2$."

8. `minor` | freshness, three items.
   - `problems-1` `p-charging-robot`: $\mathbf{u} = (3, 1)$ and $\mathbf{v} = (1, 2)$ are the two arrows of l3 screen 4 ("Use $\cos\theta$ ... on $\mathbf{u} = (1, 2)$ and $\mathbf{v} = (3, 1)$", answer $45°$, with $\mathbf{u} \cdot \mathbf{v} = 5$). Part 3 asks the angle between $2\mathbf{u}$ and $3\mathbf{v}$: the same $45°$. Part 1 is l1 screens 0 and 3 (weights that reach a target) with l1's own $\mathbf{v} = (1, 2)$. `fresh-check` lists nothing. Fix: new arrows, $\mathbf{u} = (4, 1)$, $\mathbf{v} = (1, 3)$, charger at $(11, 11)$ (no screen or item of the course holds that pair). Then part 1 is still $(2, 3)$; part 2 is 42 (slips 7, 14, 21); part 3 is $58°$ ($\cos\theta = \tfrac{42}{\sqrt{68 \times 90}}$, $57.53°$; slips 1.004 rad and $90°$); part 4 is $\sqrt{68 + 84 + 90} = \sqrt{242} \approx 15.56$ m (slips 12.57, 17.73, 8.60, 242).
   - `problems-2` `p-factor-risk`: the setting, a table of stocks' loadings on a market factor and a second factor, is the course's standing one (l5 screen 8, `review-2` `r-factor-day`, `homework-2` `h-three-assets`), and $\mathbf{w}^T\boldsymbol{\Sigma}\mathbf{w}$ is l8 screen 8 and `review-2` `r-vol`. The task, $\mathbf{B}^T\mathbf{w}$ then $\mathbf{e}^T\mathbf{F}\mathbf{e}$, is new. Accept.
   - `problems-3` `p-colour-sensor`: $\mathbf{M} = \begin{pmatrix}0.8&0.3\\0.2&0.7\end{pmatrix}$ is the regime matrix of an item in exam `topic-1.4` (another story), and part 3 is the l12 screen 4 trap (`A * x`) with a new array. Accept.

9. `minor` | results that nothing uses.
   `problems-1` `p-charging-robot` part 3 ($45°$) is not used by part 4, and part 4 can be read off the charger alone ($\sqrt{9^2 + 8^2}$), as its own explanation says, so the chain is optional there. `problems-3` `p-paint-tints` part 2 (the rank) is used by no later part; it is the item's link to l12.
   Fix: robot part 4, ask for what the chain gives and the charger does not: "How much shorter is the straight line than the two-leg path? Give metres to 2 decimal places." ($\sqrt{40} + \sqrt{45} - \sqrt{145} = 0.99$ with the present arrows; $17.73 - 15.56 = 2.18$ with those of finding 8, unrounded $17.733 - 15.556 = 2.177$.) Paint: accept.

10. `minor` | `vectors/problems-3.json` | `p-colour-sensor` | part 4.
    "The fix should be `Minv @ r`." l12 teaches the opposite habit (its objective is "prefer solving to inverting", and `review-3` `r-solve-inv` asks for it).
    Fix: "The line should use `@`: `Minv @ r`, or better `np.linalg.solve(M, r)`. Using $\mathbf{M}^{-1}$ from part 2, ..."

## Per set

- Coverage: every lesson of each level is drawn on and each problem draws on at least two (level 1: robot l1 to l3, active bets l2 to l4, drone l2, l3, stress hedge l1, l2, l4; level 2: italic l5 to l7, site plan l6 to l8, factor risk l5, l7, l8, bakery l5, l8; level 3: goat feed l9, l10, paint l9, l11, l12, sensor l10 to l12, engraver l10, l11 with l7's product).
- Only taught ideas: `matrix_rank` and `*` against `@` are in l12, the area reading of the determinant in l11, $(\mathbf{AB})^T$ and the identity in l8. The variance $\mathbf{e}^T\mathbf{F}\mathbf{e}$ is given, with the hypothesis that the factors drive every return.
- Chains: all twelve are real chains and each later part restates what it needs; finding 9 lists the two results nothing uses.
- Typed parts: 17 of 17, 16 of 18, 17 of 18. The three `choice` parts are judgements (which product, how many solutions).
- Grader, vectors typed whole (12 parts): accepted with round or square brackets, MathLive's spellings, angle brackets, as a column or a row, with no brackets and with any spacing; refused with the entries reversed or one short, on the right line. Decimal entries are accepted as fractions.
- Grader, numeric parts: every answer grades correct with more places, a unit (`m`, `km/h`, `°`, `minutes`, `£`), a letter and `=`, a true minus sign and a % sign on the percentage parts; every part refuses the value one place short and each slip. All 72 numeric `wrong` values land on their own keys and no two bands touch; the 29 `wrong` vectors and expressions land on theirs however they are bracketed (the 20 `wrong` matrices are finding 1).
- Voice: British English, no exclamation marks, no em-dashes, £ for money, no explanation over three sentences.

## Counts

| tag | count |
|---|---|
| wrong | 2 |
| unclear | 2 |
| minor | 6 |

Clean problems (no finding): `p-bakery-costs`. Clean but for the percentage hint of finding 5: `p-active-bets`, `p-stress-hedge`. Every problem of `problems-3` and two of `problems-2` hold a matrix part and so finding 1.

## Engine

- `[[a, b], [c, d]]` is not read as a matrix (findings 1, 2): the cause of both `wrong` findings and of the line "That is a single value".
- A number in front of a vector or matrix is not multiplied in (finding 6).
- The problem-set playthrough and `grade-regression.mjs` test a matrix part only with its stored `pmatrix`; neither types the form the question asks for (finding 1).
- `fresh-check.mjs` cannot see two arrows reused under other names (finding 8).

## Fix pass

Counts: 10 findings; 9 fixed, 1 waits for the engine (finding 1), 0 disputed. Every changed number was recomputed twice (`docs/reports/problems-vectors-numbers.py`, 935 checks, exit 0 with `<scratchpad>/venv/bin/python`). Files: `app/content/courses/vectors/problems-1.json`, `-2`, `-3` only.

1. The nine matrix parts (`wrong` | no `wrong` line can fire): waits for the engine fix, as directed. The engine reads `[[a, b], [c, d]]` as a list, not a matrix. Content left as it is: every `wrong[].tex` stays a `pmatrix`, and no `byKey.length` line was added (it has the same cause). Parts that wait for engine: `p-italic-letters` 1 and 3; `p-site-plan` 1 and 2; `p-goat-feed` 1 and 3; `p-colour-sensor` 2 (this part no longer exists, see finding 8: the re-authored item has two matrix parts of the same class, its parts 1 and 3); `p-engraver-dial` 1 and 4. The reader's `grade-probe.mjs` still shows 20 "never reaches its `wrong` line" rows for them, as expected.
2. `p-engraver-dial` part 1 (a right matrix refused): fixed with `accept` forms, which AUTHORING documents for `expression` and which work in the real grader. Added `[[2(k+3), 2+k], [5, 2]]` and `[[2(3+k), 2+k], [5, 2]]`. Checked with `numGrade`/`exprGrade`: both are accepted, `[[6+2k,2+k],[5,2]]` still accepted, and the order slip `[[7,3k+1],[5,2k+1]]` is still refused (it returns `length`, finding 1).
3. `p-site-plan` part 4 (`unclear`): fixed as proposed. The question asks for the angle of the step from borehole to well with the ground direction $(1, 0)$, in degrees between 0 and 180, and the `clockwise` line now also names the acute angle of the pipe's line. Key 126.9 and all bands unchanged. Checked: $\mathbf{R}^T(0, 10) = (6, 8)$ gives 53.13 and $\mathbf{R}(0, 10) = (-6, 8)$ gives 126.87.
4. `p-factor-risk` part 3 (no form stated): closed by finding 8. The part no longer exists. The new item asks for its two vector parts "exactly" ("Give them exactly, as $(e_1, e_2)$"), since the entries 1.105, 0.2 and 0.04875 are exact.
5. Five per cent parts (`unit: "%"` refuses the decimal the working prints): fixed in `p-active-bets` 2 and `p-stress-hedge` 1, 3 and 4, and built into the new `p-factor-risk` part 5 (the old part 5 was replaced). Each `feedback.correct` now ends its working in per cent ("$= -0.0055 = -0.55\%$"). Each part has a `decimal` wrong entry with its own line ("That is the decimal, $-0.0055$. The part asks for per cent: $-0.0055 = -0.55\%$, so type $-0.55$."), not a line about the method. The `decimal` value is the decimal slip at the asked rounding, with a band that takes the typed decimal (the validator's `[wrong-band]` and `[wide-wrong-band]` both pass): `p-active-bets` 2 value $-0.0001$ (band 0.000049) takes $-0.0055$, $-0.006$, $-0.01$; `p-stress-hedge` 3 and 4 the same; `p-stress-hedge` 1 value $-0.0002$ (band 0.00005) takes $-0.022$ and $-0.02$. Real grader: $-0.55$ and $-0.55\%$ accepted, $-0.0055$ returns `decimal`, 0.0055 (the sign slip's decimal) stays generic. To make the decimal slip expressible, `p-stress-hedge` part 1 now asks for 2 decimal places instead of 1 (same key $-0.022$, same band 0.0005; at one place the slip $-0.00022$ cannot meet both band rules). New `p-factor-risk` part 5: 80.3, 80.31 accepted; 0.803 and 0.8031 return `decimal`.
6. A number times a vector or matrix (class e): fixed with `accept` forms, which work. `p-drone-crosswind` 1: `\frac{1}{5}(3,4)` and `\frac{1}{20}(12,16)`; `p-goat-feed` 3: `10[[0.3, -0.1], [-0.2, 0.4]]` and `\frac{1}{0.1}[[0.3, -0.1], [-0.2, 0.4]]`; the re-authored sensor part 3: `1.25[[0.6, -0.4], [-0.1, 1.4]]` and `\frac{1}{0.8}[[0.6, -0.4], [-0.1, 1.4]]`. Checked: each typed form, `\frac15(3,4)`, `0.05(12,16)` and `\frac{1}{20}\left(12,16\right)` are accepted; `\frac{1}{4}(3,4)`, `5(3,4)` and `5[[0.3, -0.1], [-0.2, 0.4]]` are refused. The question rewording was not needed. A number in front of a typed `pmatrix` is still refused (engine, in the inbox), but the question asks for the bracket form.
7. `p-engraver-dial` part 3: fixed with the reviewer's line, which names both causes ("or $2 + k = 0$, a sign slip"). Key and band unchanged. The numbers script checks $k = -2$ solves $2 + k = 0$ and sits 0.444 from $-2.444$, inside the band of 0.5.
8. Freshness: `p-charging-robot`, `p-factor-risk` and `p-colour-sensor` were re-authored with a different task structure and new numbers, as directed. Robot: $\mathbf{u} = (4, 1)$, $\mathbf{v} = (1, 3)$, charger $(11, 11)$ (v appears in `review-1` with another second arrow, and (4, 1) is a target in l1: shared small vectors, judged fresh); $(a, b) = (2, 3)$; $(2\mathbf{u}) \cdot (3\mathbf{v}) = 42$ (slips 7, 14, 21); angle $57.5°$ to 58 (slips 1.004 rad and 90°); the straight line $\sqrt{242} = 15.56$ m is 2.18 m shorter than the legs $\sqrt{68} + \sqrt{90} = 17.73$ m (slips 15.56, 17.73, 5.16). Factor risk: weights $(0.4, 0.35, 0.25)$, $\mathbf{B}$ with rows $(1.1, 0.3)$, $(0.9, -0.2)$, $(1.4, 0.6)$, $\mathbf{F} = \begin{pmatrix}0.0144&0.003\\0.003&0.0049\end{pmatrix}$ and a future loading $(1, 0.25)$: exposures $(1.105, 0.2)$, the units to sell to cut the market exposure to 0.5 ($x = 0.605$), the hedged exposures $(0.5, 0.04875)$, the hedged variance $0.00376$ and the cut in variance, 80.3% (unhedged 0.01910). Colour sensor: a leak $\mathbf{M}$ then a gain $\mathbf{D} = \mathrm{diag}(2, 1)$: $\mathbf{C} = \mathbf{D}\mathbf{M} = \begin{pmatrix}1.4&0.4\\0.1&0.6\end{pmatrix}$, its area factor 0.8, $\mathbf{C}^{-1} = \begin{pmatrix}0.75&-0.5\\-0.125&1.75\end{pmatrix}$, the true colour $(120, 80)$ from the reading $(200, 60)$, and a choice that the amplifier is undone first. The numbers script has a stale-value check on each (none of the old figures, 45°, 12.04, 145, 0.0263, 0.02415, (140, 60) and the rest, remains). `fresh-check --file`: 0 hits, no advisory on `problems-2` or `problems-3`, and none on the robot.
9. `p-charging-robot` part 4: fixed as proposed, now "how much shorter is the straight line than the two-leg path" (2.18 m), which the charger alone cannot give. Key and band: 2.18, band 0.015 (so the rounded route $17.73 - 15.56 = 2.17$ and $8.25 + 9.49 - 15.56 = 2.18$ both land). `p-paint-tints` part 2: accepted as proposed.
10. `p-colour-sensor` part 4 (the `Minv @ r` habit): closed by finding 8. The re-authored item has no code line, so it no longer contradicts l12's "prefer solving to inverting".

Gates. Validator 0 errors, no warning on the three files. Voice scan 35 on `vectors`: 0 and 0. Playthrough `--problems vectors/problems-1`, `-2`, `-3` with `--local-cdn`, desktop and `--mobile`: all passed. Reader's scripts: `mine.py` fails only on the `decimal` entries (unknown to its list of re-derived slips; checked in the numbers script) and on the three re-authored items (written for the old numbers); `grade-probe.mjs` leaves only the class (a) rows, the engraver typing `[[6+2k, 2+k], [3+2, 1+1]]` (an entry as a sum, the engine's list reading), the `decimal` rows (now refused with their own line, by design), site plan `53.1` (now refused with the line that names it) and engraver `-2` (the line now names it). A grader sweep of every numeric and expression part of the three sets (each key, each `accept` form, each wrong typed as stored): 0 anomalies.

Changed graded answers, bands and items (complete):
- Keys changed on kept items: none. `p-stress-hedge` part 1 asks for 2 places instead of 1 (key $-0.022$ and band 0.0005 unchanged).
- New `wrong` entries: `decimal` in `p-active-bets` 2 ($-0.0001$, 0.000049), `p-stress-hedge` 1 ($-0.0002$, 0.00005), 3 and 4 ($-0.0001$, 0.000049), and in the new `p-factor-risk` part 5 (0.008, 0.0005).
- New `accept` forms: `p-drone-crosswind` 1 (2), `p-goat-feed` 3 (2), `p-engraver-dial` 1 (2), new `p-colour-sensor` part 3 (2).
- `p-site-plan` part 4: wording and `clockwise` line only (key 126.9, band 0.05, 53.1 slip unchanged). `p-engraver-dial` part 3: `added` line only.
- Items re-authored, every key new: `p-charging-robot` ($(2, 3)$ unchanged in value; 42; 58; 2.18), `p-factor-risk` ($(1.105, 0.2)$; 0.605; $(0.5, 0.04875)$; 0.00376; 80.3%; its choice part is gone), `p-colour-sensor` ($\mathbf{C}$; 0.8; $\mathbf{C}^{-1}$; $(120, 80)$; choice `gain-first`).

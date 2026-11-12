# Problem sets 1.4 (b), elimination and least-squares levels 1 to 3: second-reader findings

Scope: `app/content/courses/elimination/problems-1.json`, `-2`, `-3` and `app/content/courses/least-squares/problems-1.json`, `-2`, `-3`: 22 problems, 97 parts (45 numeric, 49 `expression`, 3 choice). Rules: `docs/briefs/chained.md`. Patterns: `review-problems-1.4-a.md`, `review-problems-1.6-a.md`.

Method. The two authors' scripts were run first. The 24 lessons were then skimmed screen by screen with the six reviews and six homework sets (`review-problems-1.4-a-scripts/taught.py`), for what each level teaches and for reused settings and numbers. Every part was solved by hand from its text before its key was read, and again in `review-problems-1.4-b-scripts/mine.py`, which imports nothing from the authors' scripts and types every matrix and vector from the prose (sympy exact: my own LU, forward and back substitution, nullspaces, Gram-Schmidt, normal equations; NumPy as a second route: `solve`, the SVD, `det`, `lstsq`, `polyfit`, `corrcoef`, and an enumeration of every way to pay 370p in ten coins). Every `wrong` value and `wrong[].tex` was rebuilt from the slip its line names, and each number printed in a `feedback`, `byKey`, `why` or `explain` string was recomputed while reading. Every typed part then went through the engine's own graders in node with the local Compute Engine (`grade-probe.mjs`: `numGrade` for the 45 numeric parts, `exprGrade`, the call `expression.js` makes, for the 49 expression parts): the key, with more places, a letter and `=`, a true minus sign and its unit; each `accept` form; each `wrong` entry on its own key; for each of the 46 vector answers eleven other ways to type it (round, square and angle brackets, MathLive's `\left\lbrack` spelling, a column, a row, no brackets, semicolons, reversed, one entry short); and 517 strings of my own (fraction against decimal, the value the working prints after its stated rounding, the answer one step short, the commonest slip). `try-fix.mjs` tries the content fixes below on in-memory copies with the same grader, and `proposed.py` computes their numbers. Freshness was read by hand, helped by `fresh.py` (every vector and matrix row of each problem searched in both courses, every `vectors` file, the `regression` problem sets and exams `topic-1.4` and `stage-1`).

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not say the form wanted, or refuses a sensible entry; `minor` = weak part, loose chain, loose `wrong` entry, missing restatement, wording or freshness.

## Tool results

| check | result |
|---|---|
| authors' scripts (scratchpad venv) | `problems-elimination-numbers.py` 1,201 checks, 0 failures; `problems-least-squares-numbers.py` 1,391 checks, 0 failures; both exit 0 |
| `mine.py` (reader's own keys, slips, stated numbers, set shape) | 1,105 checks, 0 failures; 5 CLAIM lines (findings 7, 9, 11, 15) |
| `grade-probe.mjs` (engine graders, 94 typed parts) | 1,721 checks, 517 reader rows, 0 failures; 13 rows held to be faults (findings 5, 8, 9, 12, 13); 0 form results against the reader |
| `grade-probe.mjs`, matrix parts | 3 parts, 6 `wrong` matrices retyped as the question asks: 0 on their own key (the known engine fault) |
| `try-fix.mjs` (fixes of findings 5, 8, 9, 12, 13 on in-memory copies) | 62 checks, 0 failures |
| `proposed.py` (numbers of the fixes of findings 1, 2, 3, 9, 12, 14) | 32 checks, 0 failures |
| `skills.py` | every `skills` id of each set is carried by a lesson of its level |
| validator | 0 errors; no warning on the six files; `manifest.json` unchanged |
| playthrough `--problems`, six sets, `--local-cdn` | all passed, desktop and `--mobile` |
| voice scan 35, both course folders | 0 and 0 each; no exclamation mark, no em-dash, British spelling, £ throughout |
| `fresh-check.mjs --file`, six sets | 0 hits; 2 advisories ($2y + z = 7$ with `elimination/l2` quiz 3; $\mathbf{q}_1 \cdot \mathbf{a}_2$ with `least-squares/l8` screen 1), both read and judged chance or taught notation |

Result. All 97 keys agree with mine, and so does every one of the 193 `wrong` values and every number in a feedback or explanation string. Every `wrong` entry lands on its own key and has a line; no two bands touch. One feedback line states something false (finding 7). The grader refuses one right answer typed in the item's own notation (finding 8). The rest is minor: five reuses that `fresh-check` cannot see, loose slip entries and two loose chains. Elimination is clean but for freshness.

Known engine fault (a wrong matrix typed whole does not reach its `wrong` line): it touches 3 parts, all in `elimination/problems-1` (`p-three-lines` part 1, `p-courier-rounds` parts 1 and 2; 6 `wrong` matrices). No least-squares part asks for a matrix.

## A. Elimination

1. `minor` | `elimination/problems-1.json` | `p-courier-rounds` | `items[2].prose`, parts 1 to 4 | freshness.
   $\mathbf{A} = \begin{pmatrix}0&3&1\\2&1&2\\0&6&5\end{pmatrix}$ and part 1 ("Which single swap of two rows fixes it?") are `review-1` `r-which-swap`: $\begin{pmatrix}0&3&1\\2&1&4\\0&5&2\end{pmatrix}$, "What is the first step?", answer "Swap rows 1 and 2". Row 1 and column 1 are the same, and the part's one slip, `swap-1-3` ("Row 3 also starts with 0"), is the review's second option with the same reason. `fresh-check` lists nothing.
   Fix (`proposed.py`; no row of the new matrix is in the course): prose "Round 1 had 3 large and 2 signed-for drops. Round 2 had 4 small, 1 large and 1 signed-for. Round 3 had 6 large and 7 signed-for.", $\mathbf{A} = \begin{pmatrix}0&3&2\\4&1&1\\0&6&7\end{pmatrix}$, $\mathbf{b} = (18, 15, 45)$. Part 1 and its key stay. Part 2: key stays ($\ell_{32} = 6/3 = 2$); explain "$\mathbf{PA}$ has rows $(4, 1, 1)$, $(0, 3, 2)$, $(0, 6, 7)$". Part 3: $\mathbf{P}\mathbf{b} = (15, 18, 45)$, key $(15, 18, 9)$ from $45 - 2 \times 18$; `unswapped` $(18, 15, 15)$; `signs` $(15, 18, 81)$. Part 4: $\mathbf{U} = \begin{pmatrix}4&1&1\\0&3&2\\0&0&3\end{pmatrix}$, restated $\mathbf{c} = (15, 18, 9)$, key $(2, 4, 3)$ unchanged: $z = 9/3 = 3$, $y = (18 - 6)/3 = 4$, $x = (15 - 4 - 3)/4 = 2$; `no-divide` $(6, 0, 9)$; `reversed` unchanged. Part 5 unchanged (30; `reversed` 31).

2. `minor` | `elimination/problems-3.json` | `p-vinyl-cutter` | `items[0].parts[0]` | freshness.
   At $k = 1$ the matrix is $\begin{pmatrix}3&1\\2&4\end{pmatrix}$, the matrix of `review-3` `r-area` ("acts on a triangle of area 2. What is the area of the image?") and of exam `topic-1.4` `a-det-area`, with the same task and the same determinant, 10. `fresh-check` cannot see it because the problem writes the entry as $k$. Parts 2 to 4 follow l11 screens 0 to 2 (slide an entry until the square is flat, where the images land, the input with a fixed first entry sent to zero) and the dial is the device of `vectors/problems-3` `p-engraver-dial`; the numbers there are new, accept.
   Fix: part 1 "With $k = 2$, ..." ($\begin{pmatrix}3&2\\2&4\end{pmatrix}$ is in no file). Key 40; `plus` 80; `diagonal` 60 (unchanged). `correct`: "$\det \mathbf{T} = 3 \times 4 - 2 \times 2 = 8$, so the area is $5 \times 8 = 40$ cm²." `plus`: "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$." `diagonal`: "That uses only $ad = 12$. Take off $bc = 2 \times 2$ too." Explain: "$\det \mathbf{T} = ad - bc = 12 - 4 = 8$. The determinant scales every area, so the logo becomes $5 \times 8 = 40$ cm²."

3. `minor` | `elimination/problems-2.json` | `p-tilted-gantry` part 3, `p-futures-packages` part 3 | freshness.
   Both ask "for which $c$ is the target in the column space", the level's stock task, on a target the course has already used for it. The gantry's $(3, 1, c)$ is the first item of `homework-2` ("$\mathbf{b} = (3, 1, c)$. Which $c$ puts $\mathbf{b}$ in $C(\mathbf{A})$?"). The futures' $(4, -1, c)$ is l5 screen 4 ("The target is $\mathbf{b} = (4, -1, c)$"), whose answer, 3, is the stored `sign` slip here, so a learner who recalls the lesson is told about a sign.
   Fix (`proposed.py`; neither new target is in the course, and $(5, 2, c)$ is l5's, so it is avoided). Gantry: target $(6, 2, c)$. Part 3 key 8 ($x_2 = 2$, $x_1 = 4$, $c = 2 \times 4 = 8$); `half-step` 12 ("That stops at $c - 12 = 0$ ... Adding $2R_2$ also adds $2 \times 2$: $c - 8 = 0$."); keep $-4$ as the tilt slip. Part 4 restates $(6, 2, 8)$; base $(4, 2, 0)$; key $(6, 0, 1)$; `no-motor-3` $(4, 2, 0)$; `sign` $(2, 4, 1)$. Futures: target $(5, -2, c)$. Part 3 key $-3$ unchanged (steps give $(5, 3, c + 3)$); `sign` 3 ("the entries sum to $5 - 2 + 3 = 6$"); `stale-rhs` 2 ("You added the old $-2$ to row 3. Row 2 had become $-2 + 5 = 3$"). Part 4 key $(5, 3, 0)$; `sign` $(5, -3, 0)$, "That gives June $-5 - 3 = -8$. You need $-x_1 + x_2 = -2$". Part 5 key $(3, 5, 2)$; `sign` $(7, 1, 2)$, which gives $(9, -10, 1)$; `nullspace-only` $(-2, 2, 2)$ unchanged.

4. `minor` | results that nothing uses.
   `problems-3` `p-vinyl-cutter` part 1 (50 cm²) feeds nothing: part 2 hands over $\det \mathbf{T} = 12 - 2k$ itself. `p-deformed-part` part 2 (the third pivot $\tfrac{13}{6}$) is a check that no later part uses. In `problems-2`, `p-coin-hopper` part 3 does not use part 2 and `p-futures-packages` part 3 does not use part 2; each pair is joined by the last part, as the author's report says. Accept those two.
   Fix: vinyl part 2 opens "Part 1 used $\det \mathbf{T} = 12 - 2k$ at $k = 1$, where it is 10." (with finding 2: "at $k = 2$, where it is 8."). Deformed part 3: "Parts 1 and 2 agree that $\det \mathbf{D} = 13$. A part of volume 15 cm³ is deformed. ..."

5. `minor` | `elimination/problems-2.json` | `p-burning-ethanol` | `items[0].parts[2].widget` | a number times a vector.
   `\frac{1}{3}(1,3,2,3)` and `(1,3,2,3)/3` are refused with the engine's line "That is a single value. The answer has 4 components." The learner typed four components. The class of `review-problems-1.4-a.md` finding 6.
   Fix (`try-fix.mjs`): add `"\\frac{1}{3}(1, 3, 2, 3)"` and `"(1, 3, 2, 3)/3"` to `accept`. Both typings are then accepted; `(1,3,2,3)` still lands on `scaled` and `no-minus` on its key.

## B. Least squares

6. `minor` | `least-squares/problems-1.json` | `p-crystal-cell` | `items[2].parts[3].explain` | an idea outside the level.
   "The determinant of the three edges is 27 too." Level 1 requires `elimination/L2` only (`course.json`); determinants are `elimination` level 3. The number is right ($\det = 27$).
   Fix: drop the sentence, or "If you have met determinants: the determinant of the three edges is 27 too."

7. `wrong` | `least-squares/problems-1.json` | `p-station-codes` | `items[1].parts[0].feedback.byKey.c1-only`.
   "That is $\mathbf{c}_2$ itself, which passes the test against $\mathbf{c}_1$ only. Its dot product with $\mathbf{c}_2$ is 4." False: $\mathbf{c}_2 \cdot \mathbf{c}_3 = 1 - 1 - 1 + 1 = 0$, so it passes against $\mathbf{c}_1$ and $\mathbf{c}_3$ and fails only against itself (`mine.py`).
   Fix: "That is $\mathbf{c}_2$ itself. It is orthogonal to $\mathbf{c}_1$ and $\mathbf{c}_3$, but its dot product with $\mathbf{c}_2$ is 4, not 0." The id can stay or become `c2-itself`.

8. `unclear` | `least-squares/problems-2.json` | `p-dye-mix` | `items[3].parts[1].widget`.
   The item writes its unit vectors as a fraction in front: $\mathbf{q}_1 = \tfrac17(2, 3, 6)$ in part 1, $\mathbf{q}_2 = \tfrac17(6, 2, -3)$ in part 2's own `correct` line and part 3's question. Typed that way, `\frac17(6,2,-3)`, `\frac{1}{7}\left(6,2,-3\right)` and `(6,2,-3)/7` are refused with "That is a single value. The answer has 3 components." The question does say "with exact fractions as entries", but the line shown is false and the entry is the item's own notation.
   Fix (`try-fix.mjs`): add `"\\frac{1}{7}(6, 2, -3)"` and `"(6, 2, -3)/7"` to `accept`. The three typings are then accepted; `(6,2,-3)` still lands on `not-normalised`, `7(6,2,-3)` and `\frac17(6,2,3)` are still refused.

9. `minor` | `least-squares/problems-1.json` | `p-hall-drone` | `items[0].parts[1].widget.wrong` `added`.
   The line says "You added 4 and 6", and the stored value is 10. A learner who adds and then solves $4 + 6 + c = 0$ types $-10$, which gets the generic line ("A reachable point is orthogonal to $\mathbf{y}$"), the test they applied.
   Fix (`try-fix.mjs`): add `{ "id": "added-solved", "value": -10, "tol": { "abs": 0 } }` with the same line as `added`.

10. `minor` | `least-squares/problems-1.json` | `p-hall-drone` | parts 1 to 3 | one letter for two numbers.
    Part 1 asks for $\mathbf{y} = (1, b, c)$ and finds $c = 1$. Part 2 asks "for which height $c$" and finds $c = 2$; part 3 opens "With $c = 2$". A learner reading part 2 with part 1's feedback still on screen sees $c = 1$ and $c = 2$ side by side.
    Fix: call the height $h$ in parts 2 and 3: "$(4, 6, h)$", "$4 - 6 + h$", "$h = 2$", "$h = -2$" in part 2's question, `correct`, `sign`, `added` and explain, and "With $h = 2$ the target is $(4, 6, 2)$." in part 3.

11. `minor` | `least-squares/problems-1.json` | `p-rotor-changes` | `items[3].parts[3].question` | missing restatement.
    Part 4 restates the coefficient $-2$ but not $\mathbf{e}_2$, $\mathbf{s}_1$ or $\mathbf{d}$, all three of which it needs; they stand only in parts 1 to 3.
    Fix: "Using the coefficient $-2$ on $\mathbf{e}_2 = (-1, 1, -1, 1)$ from part 3, the computer keeps only the safe part of $\mathbf{d} = (4, 0, 2, -2)$: its terms along $\mathbf{s}_1 = (-1, 0, 1, 0)$ and $\mathbf{e}_2$. Find that safe change."

12. `minor` | `least-squares/problems-1.json` | `p-crystal-cell` parts 1 and 3, `p-rotor-changes` part 2 | the unit vector has no line.
    l4 always divides by the length straight after subtracting ($\mathbf{e}_k$, then $\mathbf{q}_k$). A learner who does so here types $(\tfrac23, -\tfrac23, -\tfrac13)$, $(\tfrac13, \tfrac23, -\tfrac23)$ or $(-\tfrac12, \tfrac12, -\tfrac12, \tfrac12)$ and gets the generic line ("Subtract from $\mathbf{a}_2$ its projection ...", "Take off ..."), which is what they did.
    Fix (`try-fix.mjs`, each lands on the new key and no other entry moves): add `{ "id": "normalised", "tex": "(2/3, -2/3, -1/3)" }` to crystal part 1, "That is $\mathbf{q}_2 = \mathbf{e}_2/|\mathbf{e}_2|$, the unit vector. This part asks for $\mathbf{e}_2$ before dividing by its length, 3."; `"(1/3, 2/3, -2/3)"` to crystal part 3, "That is $\mathbf{e}_3$ divided by its length, 3. This part asks for $\mathbf{e}_3$ itself."; `"(-1/2, 1/2, -1/2, 1/2)"` to rotor part 2, "That is $\mathbf{e}_2$ divided by its length, 2. This part asks for $\mathbf{e}_2$ itself."

13. `minor` | a number times a vector, three more parts.
    `problems-3` `p-ramp-ball` part 2: `0.1(5,-8,3)`, the form of its own `correct` line ("$\mathbf{e} = 0.1\mathbf{y}$"). `problems-2` `p-solar-drone` part 2: `2(-2,-1,1)` ("$\mathbf{e} = 2\mathbf{n}$"). `problems-1` `p-hall-drone` part 4: `\frac12(7,-1,2)`. Each is refused with "That is a single value. The answer has 3 components."
    Fix (`try-fix.mjs`): `accept` gains `"0.1(5, -8, 3)"` and `"\\frac{1}{10}(5, -8, 3)"`; `"2(-2, -1, 1)"`; `"\\frac{1}{2}(7, -1, 2)"` and `"0.5(7, -1, 2)"`. All typings are then accepted, the bare vectors `(5,-8,3)`, `(-2,-1,1)` and `(7,-1,2)` stay refused, and every `wrong` entry keeps its key.

14. `minor` | `least-squares/problems-3.json` | `p-gas-hubs` | `items[2].prose`, parts 1 to 3 | freshness.
    The regressor, five days of $t = (-1, 0, 1, 2, 3)$, is the market series of exam `topic-1.4` `a-beta` ("Five days of returns, in %: the market $\mathbf{m} = (-1, 0, 1, 2, 3)$ ... Fit $s = \alpha + \beta m$ by least squares"), so $\mathbf{A}^T\mathbf{A} = \begin{pmatrix}5&5\\5&15\end{pmatrix}$ is the exam's too. The setting, gas regressed on temperature, is `regression/problems-1` `p-gas-demand`; the task there differs, accept the story.
    Fix (`proposed.py`; $(0, 1, 2, 3, 4)$ is in no file): $t = (0, 1, 2, 3, 4)$, both $\mathbf{y}$ series unchanged. Part 1: key 30; `sum` 10; `sum-squared` 100; add `count` 5 (see finding 15). Part 2: `A.T @ A` is `[[5, 10], [10, 30]]`, `A.T @ yN` is `[-5, -30]`; key $(3, -2)$ ($5\hat\alpha + 10\hat\beta = -5$, $10\hat\alpha + 30\hat\beta = -30$; twice the first off the second gives $10\hat\beta = -20$); `diagonal` $(-1, -1)$; `swapped` $(-2, 3)$; `no-sign` $(3, 2)$. Part 3: `A.T @ yS` is `[-5, -25]`; key $(2, -1.5)$; `diagonal` $(-1, -5/6)$; `no-sign` $(2, 1.5)$. Part 4: key $(1, -0.5)$; `added` $(5, -3.5)$; `reversed` $(-1, 0.5)$. Part 5: fitted spread $1 - 0.5t = (1, 0.5, 0, -0.5, -1)$, residuals, $\sum e_i^2 = 5$, 7.5 and every key and slip unchanged (0.333; 0.667; 0.6; 0.964).

15. `minor` | `least-squares/problems-3.json` | `p-gas-hubs` | part 1 `byKey.sum`; parts 2 and 3 questions.
    (a) The slip value 5 is also entry `[0, 0]`, the count, which is what a learner who counts from 1 reads for `[1, 1]`. The line names only "$\sum t_i$, the off-diagonal entry". (b) "`A.T @ A` prints `[[5, 5], [5, 15]]`" and "`A.T @ yN` prints `[-5, -25]`": `np.ones` makes a float array, so NumPy prints `[[ 5.  5.]` `[ 5. 15.]]` and `[ -5. -25.]` (`mine.py`).
    Fix: (a) `sum`: "That is entry `[0, 0]`, the count, or an off-diagonal entry, $\sum t_i$: both are 5. NumPy counts from 0, so `[1, 1]` is the column $t$ dotted with itself." (with finding 14 they differ: `count` 5, "That is entry `[0, 0]`, the count. NumPy counts from 0, so `[1, 1]` is the bottom-right entry."; `sum` 10 keeps its line). (b) "holds" for "prints" in both questions, or "prints, as whole numbers,".

16. `minor` | freshness inside the course's own sets.
    - One route three times: find a vector orthogonal to both columns, project $\mathbf{b}$ on it, subtract. `problems-1` `p-hall-drone` parts 1 and 2, `problems-2` `p-solar-drone` parts 1 to 3 and `problems-3` `p-ramp-ball` parts 1 to 3; the last two are the same three steps. `p-hall-drone` part 1 is also `homework-1` `h-complement` ("spanned by $(1, 0, -1)$ and $(0, 1, 2)$ ... a vector $(1, a, b)$. Find $a$ and $b$"), with $(1, 0, -1)$ in both. Each use is apt to its level; accept the route.
    - Three drones in one course (`p-hall-drone`, `p-rotor-changes`, `p-solar-drone`) and a fourth in `vectors/problems-1` `p-drone-crosswind`.
    Fix: `p-solar-drone`: keep the id, change the story noun in the prose and in part 4's question and `straight-down` line ("A survey prism hangs at $\mathbf{b} = (-2, 1, 9)$", "where its plumb line should meet the panel", "the spot straight below the prism").

## Per set

- Coverage: every lesson of each level is drawn on and each problem draws on at least two. Elimination: florist l1, l2; lines l1 to l3; courier l2 to l4; roaster l1, l2, l4; ethanol l4, l6, l8; gantry l5 to l7; futures l5 to l8; coins l6, l8; vinyl l9, l11; deformed l9, l10; draw bet l10 to l12. Least squares: hall drone l1 to l3; codes l1 to l3; crystal l1, l4; rotor l2 to l4; pixel l6, l7; power line l5, l7; solar l5 to l7; dye l7, l8; runner l10, l11; ramp l9, l10; gas hubs l10 to l12.
- Only taught ideas, but for finding 6. The volume rule of `p-crystal-cell` and the linearity used in `p-three-lines` part 4 are given or come from a `requires`.
- Hypotheses: each general statement carries what it needs. Orthogonal expansions say the vectors are orthogonal (`p-hall-drone` 3, `p-station-codes` 2 and 4, `p-rotor-changes` 3); $\hat{\mathbf{x}} = (\mathbf{A}^T\mathbf{A})^{-1}\mathbf{A}^T\mathbf{y}$ is used with independent columns ($\det = 50$); "the line passes through $(\bar{x}, \bar{y})$" says "with an intercept"; $N(\mathbf{A}^T)$ is "a line since $\mathbf{A}$ has rank 2"; the third pivot is asked "with no row swaps"; `p-draw-bet` counts redundant bets as "bets minus rank", the lesson's count (by l12's other wording, "a combination of the others", all four bets qualify, since $\text{H} - \text{Y} + \text{X} - \text{D} = \mathbf{0}$ has no zero weight).
- Chains: all 22 are real chains with one right answer a part (each "which swap", special solution, copy and plan is pinned by a stated entry or by invertibility; one way to pay 370p in ten coins, by enumeration). Findings 4 and 11 list the loose ends.
- Typed parts: elimination 18 of 19, 16 of 17, 14 of 14; least squares 16 of 16, 17 of 17, 13 of 14. The three choice parts are judgements.
- Grader, numeric parts (45): every key grades correct with more places, a letter and `=`, a true minus sign, its unit (£, minutes, km) and, where the answer is not whole, as a fraction (`3/2`, `13/6`, `7/5`, `1/3`); every part that asks for places refuses the value one place short (`2.17`, `0.7`, `0.33`), and every part refuses each slip. `p-hall-drone` part 2 has no `unit`, so "2 m" is not read as a number and Check stays unavailable (inbox, known class).
- Grader, vectors (46): accepted in all nine bracket and layout forms, a row where a column is meant included, and with entries as fractions or decimals; refused reversed or one entry short, on the right line. Parts with non-whole entries say "exact", and rounded decimals get the generic line.
- Voice: British English, no exclamation marks, no em-dashes, £ for money, no explanation over three sentences.

## Counts

| tag | elimination | least squares |
|---|---|---|
| wrong | 0 | 1 |
| unclear | 0 | 1 |
| minor | 5 | 9 |

Clean problems (no finding): `p-florist-prices`, `p-three-lines`, `p-roaster-beans`, `p-deformed-part` but for its unused check, `p-draw-bet`; `p-grey-pixel`, `p-power-line`, `p-runner-heart`.

Finding classes seen three times or more: a number in front of a vector refused with "That is a single value" (5 parts here, findings 5, 8, 13; 3 parts in 1.4 a); numbers or a setup reused from the course or its exam that `fresh-check` cannot see (5 items, findings 1, 2, 3, 14); the unit vector as a slip with no line (3 parts, finding 12).

## Engine

- A number in front of a vector is read as a single value (findings 5, 8, 13): same bullet as 1.4 a, five more parts.
- A unit after a vector, `(-3.6, 4.8) km`, gets the same false line; `(£6, £8, £5)` gets the generic line.
- `fresh-check.mjs` misses a matrix that equals a course matrix at the part's own parameter value (finding 2), a regressor shared with an exam item under another letter (finding 14) and a target with a letter entry, `(3, 1, c)` (finding 3).
- The known matrix fault is not raised again: 3 parts, as counted above.

## Fix pass

I recomputed every changed number before writing it, by two routes in the two number scripts (sympy exact; NumPy `solve`, `lstsq`, `polyfit`, SVD, or enumeration), and each agrees with the reader's `proposed.py` (32 checks, 0 failures). The real graders (`check-real.mjs` in the fix scratch folder: `numGrade` and `exprGrade` with the local Compute Engine) were run on the content as it now stands: 424 checks, 0 failures. They cover every typed part of the six sets (the key and every `accept` form grade correct, every `wrong` lands on its own id), the five `accept` additions with strings that must still be refused, the three `normalised` lines, `-10` on `added-solved`, and the renamed `c2-itself`. The reader's `try-fix.mjs` still passes (65 checks, 0 failures). The reader's `grade-probe.mjs` fails 30 rows and prints 1 finding line, all on strings typed from the old numbers of re-authored items (gas hubs, gantry, futures, vinyl) or on the closed findings 7 and 9; its other 1,700 checks pass, including all 11 ways to type each of the 46 vector answers. `mine.py` types the old prose and stops on the new accept forms, so it was not rerun.

Status: fixed 16 findings (all but the engine fault, which waits for the engine), disputed 0, deferred 0. Waits for engine: the known matrix fault (3 parts of `elimination/problems-1`, 6 `wrong` matrices), and the three engine bullets under "Engine". No content change for them.

1. courier, fixed. Prose (rounds 1 to 3), $\mathbf{A}$ and $\mathbf{b}$ are now $\begin{pmatrix}0&3&2\\4&1&1\\0&6&7\end{pmatrix}$ and $(18, 15, 45)$, as proposed. $\mathbf{A}(2, 4, 3)^T = (18, 15, 45)$ both ways. Part 2 explain, part 3 (key, accepts, `unswapped`, `signs`, all strings), part 4 ($\mathbf{U}$, restated $\mathbf{c}$, `no-divide`, strings) follow. Parts 1, 2 and 5 keys unchanged. The setting stays: the review reused only the matrix.
2. vinyl cutter, fixed. Part 1 at $k = 2$: $\det = 12 - 4 = 8$, area 40, `plus` 80, `diagonal` 60 unchanged, every string follows. Part 2 opens "Part 1 used ... at $k = 2$, where it is 8."
3. gantry and futures, fixed. Gantry target $(6, 2, c)$: part 3 key 8, `half-step` 12, `sign` $-4$ kept; part 4 key $(6, 0, 1)$, `no-motor-3` $(4, 2, 0)$, `sign` $(2, 4, 1)$. Futures target $(5, -2, c)$: part 3 key $-3$ and `sign` 3 unchanged, `stale-rhs` 2; part 4 key $(5, 3, 0)$, `sign` $(5, -3, 0)$ (June $-8$); part 5 key $(3, 5, 2)$, `sign` $(7, 1, 2)$ (gives $(9, -10, 1)$), `nullspace-only` unchanged. Restatements and strings follow.
4. unused results, fixed. Vinyl part 2 and deformed part 3 open as proposed (`p-deformed-part` part 3: "Parts 1 and 2 agree that $\det \mathbf{D} = 13$."). The two coin-hopper and futures pairs accepted, as the review says.
5. ethanol part 3, fixed: `accept` gains `\frac{1}{3}(1, 3, 2, 3)` and `(1, 3, 2, 3)/3`; both graded accepted, `(1,3,2,3)` still lands on `scaled`.
6. crystal part 4, fixed: the determinant sentence is dropped (the explanation is two sentences).
7. station codes, fixed. $\mathbf{c}_2 \cdot \mathbf{c}_1 = 1 - 1 + 1 - 1 = 0$, $\mathbf{c}_2 \cdot \mathbf{c}_3 = 1 - 1 - 1 + 1 = 0$, $\mathbf{c}_2 \cdot \mathbf{c}_2 = 4$. The line now says it is orthogonal to $\mathbf{c}_1$ and $\mathbf{c}_3$ and has dot product 4 with itself; the `wrong` id is now `c2-itself` (same value $(1, -1, 1, -1)$).
8. dye mix part 2, fixed: `accept` gains `\frac{1}{7}(6, 2, -3)` and `(6, 2, -3)/7`; graded accepted in three typings; `(6,2,-3)` still `not-normalised`, `7(6,2,-3)` and `\frac17(6,2,3)` refused.
9. hall drone part 2, fixed: `added-solved` $-10$ (from $4 + 6 + h = 0$) with the `added` line; graded on that id, `10` still on `added`.
10. hall drone parts 2 and 3, fixed: the height is $h$ in both (question, `correct`, `sign`, `added`, explain, and "With $h = 2$" in part 3).
11. rotor part 4, fixed: the question restates $\mathbf{e}_2$, $\mathbf{d}$ and $\mathbf{s}_1$.
12. unit vectors, fixed: `normalised` on crystal part 1 $(\tfrac23, -\tfrac23, -\tfrac13)$, crystal part 3 $(\tfrac13, \tfrac23, -\tfrac23)$, rotor part 2 $(-\tfrac12, \tfrac12, -\tfrac12, \tfrac12)$, each with the proposed line; lengths 3, 3, 2 checked by two routes; each lands on its id and no other entry moves.
13. number times a vector, fixed: `accept` gains `0.1(5, -8, 3)` and `\frac{1}{10}(5, -8, 3)` (ramp ball 2), `2(-2, -1, 1)` (solar drone 2), `\frac{1}{2}(7, -1, 2)` and `0.5(7, -1, 2)` (hall drone 4); the bare vectors stay refused, every `wrong` keeps its id.
14. gas hubs, fixed: $t = (0, 1, 2, 3, 4)$. Part 1 key 30, `sum` 10, `sum-squared` 100; part 2 key $(3, -2)$, `diagonal` $(-1, -1)$, `swapped` $(-2, 3)$, `no-sign` $(3, 2)$; part 3 key $(2, -1.5)$, `diagonal` $(-1, -5/6)$, `no-sign` $(2, 1.5)$; part 4 key $(1, -0.5)$, `added` $(5, -3.5)$, `reversed` $(-1, 0.5)$; part 5 unchanged ($R^2$ 0.333 and every slip), fitted spread $1 - 0.5t$. Normal equations were re-solved: twice the first off the second, as in the review; `np.polyfit` agrees.
15. gas hubs part 1, fixed: `count` 5 with the proposed line, `sum` keeps its line with "= 10"; parts 2 and 3 say "holds" for "prints".
16. solar drone, fixed: a survey prism hangs at $\mathbf{b}$ (prose, part 3 and part 4 questions, `straight-down` line); id kept. The shared route and the homework overlap are accepted, as the review says.

Graded answers, bands, `accept` forms and items that changed:
- `elimination/problems-1` `p-courier-rounds`: prose and matrix. Part 3 key $(14, 15, 9)$ to $(15, 18, 9)$ with its two accept forms; `unswapped` $(15, 14, 11)$ to $(18, 15, 15)$; `signs` $(14, 15, 69)$ to $(15, 18, 81)$. Part 4 key unchanged $(2, 4, 3)$; `no-divide` $(-10, 6, 9)$ to $(6, 0, 9)$. Parts 1, 2, 5: none.
- `elimination/problems-2` `p-tilted-gantry`: part 3 key 4 to 8, `half-step` 6 to 12; part 4 key $(4, -1, 1)$ to $(6, 0, 1)$ with its two accept forms, `no-motor-3` $(2, 1, 0)$ to $(4, 2, 0)$, `sign` $(0, 3, 1)$ to $(2, 4, 1)$. `p-futures-packages`: part 3 `stale-rhs` 1 to 2; part 4 key $(4, 3, 0)$ to $(5, 3, 0)$ with accepts, `sign` $(4, -3, 0)$ to $(5, -3, 0)$; part 5 key $(2, 5, 2)$ to $(3, 5, 2)$ with accepts, `sign` $(6, 1, 2)$ to $(7, 1, 2)$. `p-burning-ethanol` part 3: 2 `accept` forms added.
- `elimination/problems-3` `p-vinyl-cutter` part 1: key 50 to 40, `plus` 70 to 80. `p-deformed-part` part 3: question wording only.
- `least-squares/problems-1`: `p-hall-drone` part 2 `wrong` `added-solved` ($-10$) added, wording $c$ to $h$; part 4 2 `accept` forms added. `p-station-codes` part 1 `wrong` id `c1-only` to `c2-itself` (value unchanged). `p-crystal-cell` parts 1 and 3 `wrong` `normalised` added; part 4 explain shortened. `p-rotor-changes` part 2 `wrong` `normalised` added; part 4 question restated.
- `least-squares/problems-2`: `p-dye-mix` part 2 2 `accept` forms added; `p-solar-drone` part 2 1 `accept` form added, story noun changed (prose, parts 3 and 4).
- `least-squares/problems-3`: `p-ramp-ball` part 2 2 `accept` forms added. `p-gas-hubs`: prose $t$; part 1 key 15 to 30, `sum` 5 to 10, `sum-squared` 25 to 100, `count` 5 added; part 2 key $(1, -2)$ to $(3, -2)$ with accepts, `diagonal` $(-1, -5/3)$ to $(-1, -1)$, `swapped` $(-2, 1)$ to $(-2, 3)$, `no-sign` $(1, 2)$ to $(3, 2)$; part 3 key $(0.5, -1.5)$ to $(2, -1.5)$ with accepts, `diagonal` $(-1, -4/3)$ to $(-1, -5/6)$, `no-sign` $(0.5, 1.5)$ to $(2, 1.5)$; part 4 key $(0.5, -0.5)$ to $(1, -0.5)$ with accepts, `added` $(1.5, -3.5)$ to $(5, -3.5)$, `reversed` $(-0.5, 0.5)$ to $(-1, 0.5)$; part 5 none.

Gate results. `problems-elimination-numbers.py` 1,269 checks, exit 0; `problems-least-squares-numbers.py` 1,471 checks, exit 0 (each with a stale-value check on every re-authored item). Validator 0 errors, no warning on the six files, `manifest.json` untouched. Playthrough `--problems`, six sets, `--local-cdn`: all passed, desktop and `--mobile`. `fresh-check.mjs --file` on the six sets: 0 hits; the same two advisories as the reader (chance or taught notation). The new rows and targets appear in no other content file (searched). Voice scan 35 on both course folders: 0 and 0.

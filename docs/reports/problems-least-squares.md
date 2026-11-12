# Problem sets: least-squares (brief `docs/briefs/chained.md`)

Files: `app/content/courses/least-squares/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-least-squares-numbers.py` (exit 0, 1,391 checks, 0 failures). Commits: 84dc378 (level 1), af49ab0 (level 2), 22f1292 (level 3), then a small fix commit with this report.

Read first: every screen and quiz of l1 to l12, review-1 to 3, homework-1 to 3 and the l11 Fluency set, for settings to avoid. The course's standing settings are finance: market-neutral books and beta vectors (l1, l2, homework-1), exposure matrices and trades that change no exposure (l2, homework-1), principal components of two stocks (l3), orthogonalising a value factor against the market (l4, review-1, homework-1), a stock's beta and idiosyncratic part (l5, review-2, homework-2), the hat matrix and residuals of a market regression (l6, l7), alpha and beta by QR (l8), trends through closes (l9, l10), price impact against order size (l11), volume against spread (l11), a signal against next-day return (review-3), hedge ratios and a rates desk (homework-3). None is used. One draft was dropped: a level 3 van whose lost fuel reading is recovered from the fitted line through the means was the task of `regression/problems-1` item 3 (another course, a courier with a smudged figure) step for step, so it was replaced by `p-runner-heart`, which asks what a new point at $\bar{x}$ does to the slope and the intercept.

Answer kinds. Vectors are typed whole in one `expression` widget, as `(a, b, c)`, with `[a, b, c]` and the fraction forms in `accept`. No part asks for a matrix, so the open matrix grading fault (inbox, "review problems testing, vectors") touches nothing here; a matrix a part needs is printed as NumPy prints it or shown as a display after the sentence. Every vector part with a non-whole entry says "exact entries", "exact decimals" or "exact fractions", because a vector is compared exactly.

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-hall-drone | 4 (1 / 3 / 0) | l1, l2, l3 | 3 |
| problems-1 | p-station-codes | 4 (2 / 2 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-crystal-cell | 4 (2 / 2 / 0) | l1, l4 | 4 |
| problems-1 | p-rotor-changes | 4 (1 / 3 / 0) | l2, l3, l4 | 5 |
| problems-2 | p-grey-pixel | 4 (0 / 4 / 0) | l6, l7 | 3 |
| problems-2 | p-power-line | 4 (3 / 1 / 0) | l5, l7 | 3 |
| problems-2 | p-solar-drone | 4 (0 / 4 / 0) | l5, l6, l7 | 4 |
| problems-2 | p-dye-mix | 5 (2 / 3 / 0) | l7, l8 | 5 |
| problems-3 | p-runner-heart | 5 (4 / 0 / 1) | l10, l11 | 3 |
| problems-3 | p-ramp-ball | 4 (2 / 2 / 0) | l9, l10 | 4 |
| problems-3 | p-gas-hubs | 5 (2 / 3 / 0) | l10, l11, l12 | 5 |

Typed parts: level 1 16 of 16, level 2 17 of 17, level 3 13 of 14. The one choice part is a judgement: what a sixth run at $\bar{x}$ does to the slope (`p-runner-heart` 4).

Chains. Level 1: $\mathbf{y} = (1, -1, 1)$ spanning $N(\mathbf{A}^T)$, the reachable height $c = 2$, the plan $(3, 1)$ by orthogonal coordinates, then the three-direction plan $(3.5, -0.5, 1)$; the fourth code $(1, -1, -1, 1)$, station 4's reading 2, all four readings, the power rise 60 by Pythagoras; $\mathbf{e}_2 = (2, -2, -1)$, the face area 9, $\mathbf{e}_3 = (1, 2, -2)$, the volume 27 (the determinant agrees); the special solution $(-2, 1, 0, 1)$, its straightened $\mathbf{e}_2 = (-1, 1, -1, 1)$, the coefficient $-2$ of $\mathbf{d}$ on $\mathbf{e}_2$ in the orthogonal basis of rows and safe changes, then the safe part $(3, -2, 1, -2)$. Level 2: the grey part $(140, 140, 140)$, the colour part $(60, 0, -60)$, one pass of $\mathbf{F} = \mathbf{P} + \tfrac12(\mathbf{I} - \mathbf{P})$, two passes $(155, 140, 125)$; $\hat{x} = 1.4$, $\mathbf{e} = (-3.6, 4.8)$, 6 km, 0.71 km extra to the pylon by Pythagoras; the normal $(-2, -1, 1)$, $\mathbf{e} = (-4, -2, 2)$ by projecting on it, $\mathbf{p} = \mathbf{b} - \mathbf{e}$, the panel coordinates $(2, 3)$; $r_{12} = 7$, $\mathbf{q}_2 = \tfrac17(6, 2, -3)$, $\mathbf{Q}^T\mathbf{b} = (21, 7)$, $\hat{\mathbf{x}} = (2, 1)$ by back substitution, the miss 7. Level 3: the cross sum 59, $\hat\beta = 5.9$, $\hat\alpha = 81$, the slope unchanged by a run at $\bar{x}$, the new intercept 82; $\mathbf{y} = (5, -8, 3)$, the error $(0.5, -0.8, 0.3)$ as the projection of $\mathbf{b}$ on $N(\mathbf{A}^T)$, $\hat{\mathbf{x}} = (1, 5)$ from $\mathbf{b} - \mathbf{e}$, the prediction 126 cm; `(A.T @ A)[1, 1]` $= 15$, hub N's fit $(1, -2)$, hub S's $(0.5, -1.5)$ with the same `A.T @ A`, the spread's fit $(0.5, -0.5)$ as the difference, its $R^2 = 0.333$. Each later part restates the value it uses, and where a slip can carry, its `wrong` list holds what the commonest slip before it gives (`carried` in eight parts).

Judgement calls a reader may question:
- `p-crystal-cell` states in its prose that straightening keeps the volume, so the volume is $|\mathbf{a}_1|\,|\mathbf{e}_2|\,|\mathbf{e}_3|$. Level 1 does not teach it; it is given, and the determinant (elimination, a prerequisite course) is named only as a check.
- `p-rotor-changes` part 3 states that the two rows of $\mathbf{A}$, $\mathbf{s}_1$ and $\mathbf{e}_2$ are orthogonal; the explain gives the reason (row space orthogonal to $N(\mathbf{A})$, l2). Its part 4 then adds two coordinate terms, which is a projection onto $N(\mathbf{A})$ done with l3's coordinates; level 2's projection matrix is not needed.
- `p-hall-drone` part 4 can be done from scratch or from part 3's plan plus the plan for the extra $(0, 0, 3)$; the explain shows both, so part 3 feeds it.
- `p-solar-drone` projects onto a plane by projecting onto its normal line and subtracting ($\mathbf{I} - \mathbf{P}_n$), on purpose a different route from l6 screen 7 and `homework-2` item 3, which give $(\mathbf{A}^T\mathbf{A})^{-1}$ and multiply. The last part's explain checks it against the normal equations.
- `p-ramp-ball` fits $d = C + Dt^2$, a model linear in its unknowns but not a straight line in $t$; the explain says so. Its error comes from $N(\mathbf{A}^T)$ (a line, since $\mathbf{A}$ is 3 by 2 of rank 2), which part 1 builds.
- `p-gas-hubs` draws on l12 through NumPy: `A = np.column_stack([np.ones(5), t])`, an entry of `A.T @ A`, printed `A.T @ y` arrays, and one `np.linalg.solve(A.T @ A, A.T @ Y)` for both hubs (l12 screen 9). No part is code: problem sets refuse `code` parts.

Form. Every numeric part names its form ("Give a whole number", "Give a decimal", "Give km to 2 decimal places", "Give 3 decimal places"). `p-power-line` parts 3 and 4 carry `unit` "km". Bands: keys asked to 2 or 3 places have tol 0.005 or 0.0005; every `wrong` on a part asking a whole number has a band of 0.5 when its value is not whole, so the slip as a learner rounds it lands (validator `[wrong-band]` caught four on the first draft of level 1).

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (1,391 checks in all) |
| validator | 0 errors; no warning on the file (total 4,856, as before) | same | same |
| playthrough `--local-cdn` | green (16 parts) | green (17 parts) | green (14 parts) |
| playthrough `--mobile` | green; 440 px shots read | green; shots read | green; shots read |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

The numbers script: route 1 is exact sympy (dot products, nullspace, Gram-Schmidt by hand, normal equations), route 2 NumPy by another method (`lstsq`, Householder `qr` with signs fixed, the SVD for null spaces, `det`, `cross`, `polyfit`, `corrcoef`, a grid search for one reading). Beyond keys: every `wrong` value is rebuilt from its named slip and shown outside the key's band, no two bands overlap, every expression `wrong` is rebuilt and differs from the key and the others; `arith` evaluates every chain $a = b = c$ of plain arithmetic in every learner-facing string (tuples, fractions, square roots and squares included) and `vocab` fails any printed number that is neither given nor computed. A self-test plants one fault of each kind; a second planted run on a scratch copy (a false sum in `p-runner-heart` part 1, two false steps in the dropped van draft) failed as it should.

Routing, through the real grader: `tools/grade-regression.mjs --content` on a scratch folder holding only these three files. All 106 keys and `accept` forms grade correct, and all 106 `wrong` entries grade wrong and land on their own key.

Layout: the first draft of `p-station-codes` put the three 4-entry codes on one display line, which widened the page past 440 px and cut the prose off at the right in the `-440` shot, while the playthrough stayed green (inbox). It is now an `aligned` block of two lines.

## Fresh-check

At the gate: 0 hits on all three sets. Advisories: `problems-1` had one, the Gram-Schmidt formula for $\mathbf{e}_3$ shared with l4 screen 4, where the same step was given with its $\mathbf{q}$s; the part was rewritten to ask "straighten $\mathbf{a}_3$ against $\mathbf{a}_1$ and $\mathbf{e}_2$" with no formula, and the advisory is gone. `problems-2` has one, $\mathbf{q}_1 \cdot \mathbf{a}_2$ shared with l8 screen 1: the definition of $r_{12}$, a taught idea; kept. At `--min-run 8 --min-share 0`: 0, 1 and 8 hits, all form sentences ("give a whole number using # from part", "give a decimal using # from part") in other courses' sets. The same loose run on the van draft listed "least squares line with an intercept passes through" in `regression/problems-1`, which led to reading that item and dropping the draft.

## Engine limits

Three bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems least-squares)". None blocked a problem.

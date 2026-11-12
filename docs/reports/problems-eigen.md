# Problem sets: eigen, levels 1 to 3 (brief `docs/briefs/chained.md`)

Files: `app/content/courses/eigen/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-eigen-numbers.py` (exit 0, 1,536 checks, 0 failures). Commits: c790bf1 (level 1), b9e7efb (level 2), 056da8d (level 3), then one commit with a unit fix on `problems-2` and this report.

Read first: every screen and quiz of l1 to l12, review-1 to 3, homework-1 to 3 and exam `topic-1.4` (its eigen items), for settings to avoid. The course's own settings are finance throughout: market share and brokers (l1, l4), credit and bond ratings (l3, l4), regimes, order flow and a two-sector economy (homework-1), covariance of bank shares and hedged pairs (l2, l5, l7), hedges with futures (l6, homework-2), risk ellipses (l8), desks under shocks (l9), five-bank correlation (l10), stock PCA and takeovers (l11), gilt curves (l12, homework-3). None is used: the sets use a drawing app, a paved path, a bike scheme, a frog, a pond, river gauges, thermometers, branch sales, crabs and weather sites. No matrix of the course is reused, and every task structure differs from the screen it draws on (below).

Answer kinds. No part asks for a matrix (the open matrix grading fault is not touched). Vectors are typed whole in one `expression` widget; every eigenvector part fixes the scaling it wants ("second entry 1, as $(a, 1)$", "as $(2, b)$", "shares adding to 1", "unit vector by the sign rule"), and every vector part with a non-whole entry says "exact decimals" or "exact fractions". Where a learner may write a number in front of a vector, `accept` holds that form (`\frac{1}{5}(3, 2)`, `0.2(3, 2)`, `0.25(1, 2, 1)`, `\frac{1}{10}(8, 6, 0)`, `0.2(3, 4)` and others).

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-sketch-warp | 5 (3 / 2 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-garden-path | 4 (2 / 2 / 0) | l2, l3 | 4 |
| problems-1 | p-hill-bikes | 4 (4 / 0 / 0) | l2, l4 | 3 |
| problems-1 | p-lazy-frog | 5 (2 / 2 / 1) | l1, l3, l4 | 5 |
| problems-2 | p-oval-pond | 5 (4 / 1 / 0) | l5, l6, l8 | 3 |
| problems-2 | p-river-gauges | 5 (4 / 1 / 0) | l6, l7 | 5 |
| problems-2 | p-tank-thermometers | 5 (5 / 0 / 0) | l5, l7 | 4 |
| problems-3 | p-branch-sales | 5 (3 / 2 / 0) | l9, l10 | 4 |
| problems-3 | p-crab-sizes | 5 (4 / 1 / 0) | l11, l12 | 5 |
| problems-3 | p-site-anomalies | 4 (4 / 0 / 0) | l10, l11, l12 | 4 |

Numeric counts include the three `answers` sets (eigenvalues typed as a pair). Typed parts: level 1 17 of 18, level 2 15 of 15, level 3 14 of 14. The one choice part is a judgement: whether the frog's chain settles, given the eigenvalue $-1$.

Chains. Level 1: $\lambda = 2$ from the row of ${\bf A}{\bf v}$ free of $b$, then $b = -6$, the other eigenvalue 1 by the trace, its eigenvector $(2, 1)$, then ${\bf A}^4{\bf w} = (50, 17)$; eigenvalues 3 and $-2$ of the paving recurrence, the eigenvector $(3, 1)$, the start's eigen-coordinates $(\tfrac35, \tfrac25)$, then $t_{10} = 35839$; the $p = 0.3$ that puts 200 bikes at Hill in the long run, $\lambda_2 = 0.55$ by the trace, 321 bikes after two nights, then night 5 as the first below 230; the frog's steady state $(0.25, 0.5, 0.25)$, the eigenvalue $-1$ of $(1, -2, 1)$, the judgement that it never settles, the lazy chain's eigenvalues $(0, 0.5)$, then 0.3125 on pad 1 after 3 minutes. Level 2: the off-diagonal 2, eigenvalues 4 and 9, the long axis $(2, -1)$, the half-axis 3 m, then the area $6\pi = 18.85$ m²; the corner determinant 0.36, $\det{\bf C} = -r^2 + 1.28r - 0.28$, the bound $r > 0.28$, the null vector $(1, -1.6, 1)$, then the variance $-0.16$ that rules out the reported $r = 0.2$; eigenvalues 5, 2 and 2 of the thermometer covariance, the average's variance $\tfrac53$, then 1.76 for other weights by splitting along the eigenvectors. Level 3: $({\bf A}^T{\bf A})_{12} = 21$, eigenvalues 50 and 8, ${\bf u}_1 = (0.8, 0.6, 0)$, the first column $(4, 3, 0)$ of ${\bf A}_1$, then the energy share 0.862; the covariance 90, eigenvalues 250 and 62.5, PC1 $(0.6, 0.8)$ from a printed `eigh` result with the sign rule, crab 1's score 20, then 1.26 standard deviations; total variance 39 from the singular values, the share 0.962 of two components, 3 components for 99%, then the rank-3 error energy 9. Each later part restates the value it uses, and where a slip can carry, its `wrong` list holds what the commonest slip before it gives (`carried` in ten parts).

Judgement calls a reader may question:
- `p-garden-path` gives the recurrence and ${\bf A}$ in the prose: building a state matrix from a recurrence is not taught in level 1, so it is given, and the parts test eigenvalues, eigenvectors, coordinates and powers (l2, l3). The explain states the hypothesis (distinct eigenvalues, so independent eigenvectors).
- `p-lazy-frog` part 4 uses ${\bf L} = \tfrac12({\bf I} + {\bf M})$: that ${\bf L}$ keeps the eigenvectors of ${\bf M}$ follows from l1's definition in one line, and the explain shows ${\bf L}$ applied to each vector directly.
- `p-hill-bikes` part 4 is l4's "first $k$ below a threshold", on purpose: parts 1 to 3 are new (an inverse problem for $p$, $\lambda_2$ by the trace, a two-night count) and the last part is the result the operator wants.
- `p-river-gauges` uses the leading-determinant test for positive definiteness (l6) on a correlation matrix and reads the result through l7 (no real data give a negative variance). Another course (`research-int/l2-correlation-limits`) treats three-asset correlation limits; the eigen course and exam `topic-1.4` do not, and the structure here (polynomial determinant, null vector, the variance of that mix) is the item's own.
- `p-oval-pond` part 5 gives the ellipse area formula $\pi ab$; it is not taught in level 2, and the explain checks it against $36\pi/\sqrt{\det{\bf A}}$.
- `p-crab-sizes` part 3 prints an `eigh` result (signs as NumPy may return them; the script checks the printed columns are eigenvectors of the covariance) and asks for PC1 by l12's sign rule. No part is code: problem sets refuse `code` parts.
- `p-tank-thermometers` part 2 restates part 1's vector only to note the perpendicularity; parts 3 to 5 each use the parts before.

Form. Every numeric part names its form ("Give a whole number", "Give a decimal", "Give a decimal to 3 places", "Give 2 decimal places", "Give an exact decimal", "Give metres as a whole number", "Give square metres to 2 decimal places"). `p-oval-pond` parts 4 and 5 carry `unit` "m" and "m²", so "3 m" and "18.85 m²" are read. Negative keys ($b = -6$, eigenvalue $-1$, $a = -1.6$, variance $-0.16$, the set $\{3, -2\}$) each have a dropped-sign `wrong`. Whole-number parts have bands of 0.5 on non-whole slips (181.5, 440.25, 35019.8, 37.74, 1.8), so the slip rounded as asked lands.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (1,536 checks in all) |
| validator | 0 errors; no warning on the file (total 4,853, as before) | same | same |
| playthrough `--local-cdn` | green (18 parts) | green (15 parts) | green (14 parts) |
| playthrough `--mobile` | green; 440 px shots read | green; shots read | green; shots read |
| voice scan 35 (`VOICE_BASE` the course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

The numbers script: route 1 is exact sympy (characteristic roots, exact nullspaces, `LUsolve`, exact powers and chain steps, symbolic determinants), route 2 a different method in floating point (NumPy `eig`, `eigvals`, `eigh`, `svd`, `matrix_power`, `np.cov`, the recurrence iterated, a bisection on NumPy's steady state for $p$, a bisection on the smallest eigenvalue for the bound on $r$, and for `p-site-anomalies` a real demeaned 31 by 4 matrix built with the stated singular values). Beyond keys: every `wrong` value is rebuilt from its named slip and shown outside the key's band, no two bands overlap, every expression and set `wrong` is rebuilt and differs from the key; `arith` evaluates every chain of plain arithmetic in every learner-facing string and `vocab` fails any printed number that is neither given nor computed. A self-test plants one fault of each kind, and a planted run on `problems-3` (15.3 for 15.2 in a working line, 38.6 for 38.7) failed four checks as it should.

Routing, through the real grader: `tools/grade-regression.mjs --content` on a scratch folder holding only these three files. All 204 keys, `answers` sets and `accept` forms grade correct, and every `wrong` entry grades wrong and lands on its own key.

## Fresh-check

At the gate: 0 hits on all three sets. Advisories: none on `problems-1` and `problems-2`; three on `problems-3`, each "3 shared parameters" between the crab measurements and a number-sequence puzzle in `mock-oa-trader`, `-2` and `-3` (74, 46, 52 and similar): chance, not reuse (inbox). At `--min-run 8 --min-share 0`: 2, 5 and 1 hits, all form sentences ("give a whole number using # from part", "find both eigenvalues of # type them separated by a comma") shared with other sets.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems eigen)". None blocked a problem.

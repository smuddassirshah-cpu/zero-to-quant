# Problem sets: stat-learning (brief `docs/briefs/chained.md`)

Files: `app/content/courses/stat-learning/problems-4.json`. Numbers: `docs/reports/problems-stat-learning-numbers.py` (exits 0, 286 checks). Levels 1 to 3 have no set yet.

## Level 4: `problems-4.json` (margins, clusters, networks and splines)

Lessons read first: l15 support vector machines, l16 k-means and linkage, l17 a one-layer network and a gradient step, l18 splines, l19 choosing a learner. The three reviews of the level were read too, so that no wrong finding is repeated: the set uses scikit-learn's sense of the margin only through $w$ and $b$ (no $C$), counts spline coefficients by knots (not `SplineTransformer` columns), splits no accuracy into bias and variance, and says nothing about a best inertia. Settings new to the course: a spam filter, a desk's order sizes, a delivery-time network, a subscription firm's renewals.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-spam-filter | 5 (3 / 2) | l15, l19 | 3 |
| problems-4 | p-order-sizes | 5 (5 / 0) | l16, l18 | 4 |
| problems-4 | p-one-unit | 5 (5 / 0) | l17, l18 | 5 |
| problems-4 | p-renewals | 4 (3 / 1) | l17, l19 | 4 |

Typed parts 16 of 19. The three choice parts are judgements: where an email sits in the street, which of two tied learners to keep, and which learner to take to the test rows. Every lesson of the level appears in at least one problem, and every problem draws on at least two.

Chains. The margin 0.4 from $\lVert w \rVert = 2.5$, an email's distance 0.08, its place inside the street, the tie broken towards the linear filter, then that filter's $t = 2.24$ against a 90% base rate. Two rounds of k-means on six order sizes (centre 18, then 22), the inertia 40, a knot halfway between the settled centres at 13, the spline's prediction 38.4 bp at 20%, and the 12.4 bp that splitting the order saves. A forward pass $\hat y = 7$, the loss 4.5, the slope $-48$ for $w_1$, the step to $w_1 = 0.98$, and the unit's knot moving from 2 to $\tfrac{1}{0.98} \approx 1.020$, which ties a ReLU unit to a hinge. A 6–16–1 network's 129 parameters, the tie broken towards logistic regression's 7, its $t = 1.95$ against a 70% base rate, and the 1,182 test rows a $t$ of 3 would need. Each later part restates the value it uses, and its `wrong` list holds the value that follows from the commonest slip in the part before (`carried`).

Form. Every non-whole numeric part says "Give a decimal." or "Give n decimal places.". The validator's `[tight-band]` rule flagged the first draft of the last part, whose working ended on 1181.25 before the rounded key 1,182; the working now ends "round up to $n = 1182$".

## Checks

| check | problems-4 |
|---|---|
| numbers script | 0 failures (286 checks; two routes a part: sympy against NumPy projection, scikit-learn `KMeans` from the stated centres, hinge columns in NumPy, a finite-difference slope, a scan for the knot, statsmodels' `proportions_ztest` with the null variance, brute search over $n$) |
| validator | 0 errors, 0 warnings on the file (eight `O2-long-sentence`, two `[tight-band]` and one `[shown-arithmetic]` on first draft, all rewritten) |
| playthrough `--local-cdn` | green (19 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

## Fresh-check

`node tools/fresh-check.mjs --file content/courses/stat-learning/problems-4.json`: 0 hits and no advisory lines. The lesson stories (six loans, six shares' volatilities, the corner network, the impact curve, the five-learner table) are not reused.

## Engine limits

None found; nothing raised for this set.

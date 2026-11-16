# Problem sets: stat-learning (brief `docs/briefs/chained.md`)

Files: `app/content/courses/stat-learning/problems-1.json` to `problems-4.json`. Numbers: `docs/reports/problems-stat-learning-numbers.py` (exits 0; one block per set, every path from `__file__`).

## Level 1: `problems-1.json` (prediction, overfitting, bias and variance)

Lessons read first: l1 to l4, review-1 and homework-1, with their numbers and stories noted (futures and stock returns, spreads by hour, the 20 resampled fits, the 3-NN grid, the £ and per cent features). Settings new to the course: a ferry's passengers, a bakery's loaves, a broker's commissions, a district heating firm's demand.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-ferry-passengers | 5 (4 / 1) | l1, l2 | 3 |
| problems-1 | p-loaves-k | 5 (4 / 1) | l3, l4 | 4 |
| problems-1 | p-broker-clients | 5 (5 / 0) | l1, l4 | 4 |
| problems-1 | p-heat-demand | 5 (5 / 0) | l2, l3 | 5 |

Typed parts 18 of 20; the two choice parts are judgements (which forecast to keep, which $k$ to use). Chains: the best constant 7, its training MSE 5.667, its test MSE 9, the degree-5 interpolant, and the constant kept against the interpolant's 31.4. Bias squared 9 for $k = 20$, its error 13.4, $k = 1$ at 10.4, $k = 5$ at 5.8, and $k = 5$ chosen. A raw distance 5.39, a scaled one 0.54, the scaled 2-NN forecast 7.5, its test MSE 0.5, and the training mean's 1.833. Degree 2 kept by test MSE, 0.60 above the noise, squared bias 0.24, 1.476 at 400 days, and degree 6 at 1.358, so more data moves the best degree up. Each later part restates the value it uses; `carried` wrongs hold the commonest slip of the part before.

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

| check | problems-1 | problems-4 |
|---|---|---|
| numbers script | 0 failures (two routes a part: sympy or fractions against NumPy, calculus against a scan for the best constant, `np.polyfit` for the interpolant, a simulated average of five noises, scikit-learn `KNeighborsRegressor`, the $1/n$ rule written with $n$) | 0 failures (286 checks; two routes a part: sympy against NumPy projection, scikit-learn `KMeans` from the stated centres, hinge columns in NumPy, a finite-difference slope, a scan for the knot, statsmodels' `proportions_ztest` with the null variance, brute search over $n$) |
| validator | 0 errors, 0 warnings on the file (eight `O2-long-sentence` and five `O2-explain-answer` on first draft, rewritten) | 0 errors, 0 warnings on the file (eight `O2-long-sentence`, two `[tight-band]` and one `[shown-arithmetic]` on first draft, all rewritten) |
| playthrough `--local-cdn` | green (20 parts) | green (19 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault | green; 440 px shots read, no fault |
| `grade-all --file` | 0 failures (20 widgets) | not run |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 |

## Fresh-check

`problems-1.json`: first run gave one advisory, `items[1]` sharing the parameters 22 and 21 with `l18-bending-the-line.json` screens[0] (the $k = 1$ forecasts held 22 and 21). The forecasts were changed to 23, 18, 19, 17, 23 (variance 6.4, error 10.4); the rerun gives 0 hits, 0 warnings, 0 advisories. Second check by grep: the key numbers, each variable letter and each noun (ferry, passengers, loaves, bakery, broker, commission, heat demand) across `app/content/courses/stat-learning/`, and each story across `app/content/`. The first draft's gas demand from the temperature matched `regression/problems-1.json`, so that problem became a district heating firm's heat demand (no match). Bakeries and ferries appear in other courses with unrelated stories (break-even trays, a berth map).

`node tools/fresh-check.mjs --file content/courses/stat-learning/problems-4.json`: 0 hits and no advisory lines. The lesson stories (six loans, six shares' volatilities, the corner network, the impact curve, the five-learner table) are not reused.

## Engine limits

None found; nothing raised for this set.

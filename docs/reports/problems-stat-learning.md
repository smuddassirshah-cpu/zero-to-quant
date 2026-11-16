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

## Level 2: `problems-2.json` (linear models, features and penalties)

Lessons read first: l5 to l9, review-2 and homework-2 (the 40-feature share panel, mom times vol, $\sum xy = 23.0276$, the six uncorrelated coefficients, size in £ millions, the built two-feature market with $\lambda = 25$). Settings new to the course: an ice-cream van's cones, a letting agent's rents against mortgage rates, a futures model's five signals, a built three-feature market (both re-authored in session AF: a power futures desk's three signals, and a market maker's two correlated volume signals).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-2 | p-ice-cream-van | 5 (5 / 0) | l5, l6 | 3 |
| problems-2 | p-rent-ridge | 5 (5 / 0) | l7, l9 | 4 |
| problems-2 | p-futures-lasso | 4 (4 / 0) | l5, l8 | 4 |
| problems-2 | p-built-ridge | 4 (4 / 0) | l5, l7 | 5 |

Typed parts 18 of 18 (no step here is a judgement between named options). Chains: the weekend slope 2.0, the Saturday forecast 52, the test MSE 4.5, the training-mean baseline 75.75, test $R^2$ 0.941. OLS 0.9, ridge 0.75, the same $\lambda$ in percentage points keeping 0.045 of an OLS 90, the standardised slope 1.0 per standard deviation, and 0.5 per basis point in either unit. The OLS forecast 1.4, the lasso forecast 0.9 at $\alpha = 0.2$ (a fall of 2.5 per unit), the first zero at $\alpha = 0.8$ after demand leaves at 0.5, and the forecast $-0.1$ at the chosen $\alpha = 1.0$. OLS coefficients 2.0 and $-1.0$ from the 2 by 2 normal equations, ridge's 1.2 and $-0.3$ at $\lambda = 10$, ridge's test MSE 0.355 on four held-out hours, and its test $R^2$ 0.897 against a baseline of 3.4525.

## Level 3: `problems-3.json` (probabilities, thresholds and honest scores)

Lessons read first: l10 to l14, review-3 and homework-3 (the 400 business loans with leverage and cover, the £50,000 and £2,000 costs, the 1,000 firms with 50 defaults, the reliability table, the cubed model, the Kelly bets, the 1,000 simulated days with 135 up of 250). Settings new to the course: a limit order's fill, a lender's missed payments, euro against sterling calls, a power desk's price spikes.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-3 | p-order-fill | 5 (5 / 0) | l10, l11 | 4 |
| problems-3 | p-payment-misses | 5 (5 / 0) | l12, l13 | 3 |
| problems-3 | p-sterling-calls | 5 (5 / 0) | l12, l14 | 4 |
| problems-3 | p-price-spikes | 5 (5 / 0) | l10, l11, l13 | 5 |

Typed parts 20 of 20. Chains: a fill chance of 0.525, the odds ratio 0.407 a basis point, 0.310 one point further out by the odds, the cost threshold 0.8, and the boundary at $d = 0.571$. Precision 0.24, recall 0.6, accuracy 0.885 under the 0.95 of flagging nobody, the flagged bin overconfident by 0.16, and an ECE of 0.035. Up-call precision 0.66, a hit rate of 0.635, $t = 2.75$ against the 0.55 base rate, £42,000 of flips, and £8,000 after costs. A spike chance of 0.269, the hedge threshold 0.25, 0.18 observed where the model said 0.29, £4,920 expected for a hedge, and £168,000 saved over 100 days by not following the overconfident model.

Bands. Part 3 of `p-sterling-calls` asks for $t$ from the printed 0.635 (2.7549, so 2.75) and takes 2.739 to 2.761, so the unrounded route from $165/260$ (2.742, printed 2.74) is accepted too; the script checks both.

## Level 4: `problems-4.json` (margins, clusters, networks and splines)

Lessons read first: l15 support vector machines, l16 k-means and linkage, l17 a one-layer network and a gradient step, l18 splines, l19 choosing a learner. The three reviews of the level were read too, so that no wrong finding is repeated: the set uses scikit-learn's sense of the margin only through $w$ and $b$ (no $C$), counts spline coefficients by knots (not `SplineTransformer` columns), splits no accuracy into bias and variance, and says nothing about a best inertia. Settings new to the course: a spam filter, a desk's order sizes, a delivery-time network, a subscription firm's renewals.

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-spam-filter | 5 (3 / 2) | l15, l19 | 3 |
| problems-4 | p-order-sizes | 5 (5 / 0) | l16, l18 | 4 |
| problems-4 | p-one-unit | 5 (5 / 0) | l17, l18 | 5 |
| problems-4 | p-renewals | 4 (3 / 1) | l17, l19 | 4 |

Typed parts 16 of 19. The three choice parts are judgements: where an email sits in the street, which of two tied learners to keep, and which learner to take to the test rows on validation scores. Every lesson of the level appears in at least one problem, and every problem draws on at least two.

Chains. The margin 0.4 from $\lVert w \rVert = 2.5$, an email's distance 0.08, its place inside the street, the tie broken towards the linear filter, then that filter's $t = 2.24$ against a 90% base rate. Two rounds of k-means on six order sizes (centre 18, then 22), the inertia 40, a knot halfway between the settled centres at 13, the spline's prediction 38.4 bp at 20%, and the 12.4 bp that splitting the order saves. A forward pass $\hat y = 7$, the loss 4.5, the slope $-48$ for $w_1$, the step to $w_1 = 0.98$, and the unit's knot moving from 2 to $\tfrac{1}{0.98} \approx 1.020$, which ties a ReLU unit to a hinge. A 6–16–1 network's 129 parameters, logistic regression taken on the best validation score (0.78; the network's 129 parameters on 320 rows fall from 0.96 to 0.75), its $t = 1.95$ against a 70% base rate, and the 1,182 test rows a $t$ of 3 would need. Each later part restates the value it uses, and its `wrong` list holds the value that follows from the commonest slip in the part before (`carried`).

Form. Every non-whole numeric part says "Give a decimal." or "Give n decimal places.". The validator's `[tight-band]` rule flagged the first draft of the last part, whose working ended on 1181.25 before the rounded key 1,182; the working now ends "round up to $n = 1182$".

## Checks

| check | problems-1 | problems-2 | problems-3 | problems-4 |
|---|---|---|---|---|
| numbers script | 0 failures (two routes a part: sympy or fractions against NumPy, calculus against a scan for the best constant, `np.polyfit` for the interpolant, a simulated average of five noises, scikit-learn `KNeighborsRegressor`, the $1/n$ rule written with $n$) | 0 failures (built data with the stated sums fitted by scikit-learn `LinearRegression`, `Ridge` and `Lasso`, an orthogonal design for soft thresholding and the ridge factor, `mean_squared_error`) | 0 failures (sympy against SciPy `expit` and `brentq`, a scan of expected costs for each threshold, label arrays scored by scikit-learn's precision, recall and accuracy, binned ECE in NumPy, statsmodels' `proportions_ztest`, a position path for the flips, a simulation of spikes) | 0 failures (286 checks; two routes a part: sympy against NumPy projection, scikit-learn `KMeans` from the stated centres, hinge columns in NumPy, a finite-difference slope, a scan for the knot, statsmodels' `proportions_ztest` with the null variance, brute search over $n$) |
| validator | 0 errors, 0 warnings on the file (eight `O2-long-sentence` and five `O2-explain-answer` on first draft, rewritten) | 0 errors, 0 warnings (two `[percent-form]`, one `O2-explain-answer` on first draft, rewritten) | 0 errors, 0 warnings (six `O2-long-sentence` on first draft, rewritten) | 0 errors, 0 warnings on the file (eight `O2-long-sentence`, two `[tight-band]` and one `[shown-arithmetic]` on first draft, all rewritten) |
| playthrough `--local-cdn` | green (20 parts) | green (20 parts) | green (20 parts) | green (19 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault | green; 440 px shots read, no fault | green; 440 px shots read, no fault | green; 440 px shots read, no fault |
| `grade-all --file` | 0 failures (20 widgets) | 0 failures (20 widgets) | 0 failures (20 widgets) | not run |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 | 0 and 0 |

## Fresh-check

`problems-1.json`: first run gave one advisory, `items[1]` sharing the parameters 22 and 21 with `l18-bending-the-line.json` screens[0] (the $k = 1$ forecasts held 22 and 21). The forecasts were changed to 23, 18, 19, 17, 23 (variance 6.4, error 10.4); the rerun gives 0 hits, 0 warnings, 0 advisories. Second check by grep: the key numbers, each variable letter and each noun (ferry, passengers, loaves, bakery, broker, commission, heat demand) across `app/content/courses/stat-learning/`, and each story across `app/content/`. The first draft's gas demand from the temperature matched `regression/problems-1.json`, so that problem became a district heating firm's heat demand (no match). Bakeries and ferries appear in other courses with unrelated stories (break-even trays, a berth map).

`problems-2.json`: first run gave one advisory, `items[3]` sharing 300 and 0.15 with `l11-the-boundary.json` screens[5]; the built market moved to $n = 500$, $\lambda = 125$ and 500, and a third OLS estimate of 0.14 (also clear of review-2's $n = 400$, $\lambda = 100$). The grep of `app/content/` found the first draft's freight rate against diesel close to `regression/problems-2.json` (a freight index on ship fuel), so that problem became rents against mortgage rates. Rerun: 0 hits, 0 warnings, 0 advisories.

`problems-3.json`: first run gave one `[same-course-reuse]` pair warning (the spike item's consecutive keys 0.2 and 0.15 sat together in a review-2 line) and one advisory (0.27 and 0.15 shared with `problems-2.json` items[2]). The spike item moved to costs of £6,000 and £18,000 (threshold 0.25), 100 past days averaging 0.29 with 18 spikes; the rerun gives 0 hits, 0 warnings, 0 advisories. The grep of `app/content/` found an order filling in `conditional/problems-1.json` (a router sending orders to three venues, a different story and model) and a price spike in `fin-ml/l2-triple-barrier.json` (a barrier walk-through); neither is reused. After the third set was written, `problems-1.json` and `problems-2.json` were rerun against it: 0 hits each.

`node tools/fresh-check.mjs --file content/courses/stat-learning/problems-4.json`: 0 hits and no advisory lines. The lesson stories (six loans, six shares' volatilities, the corner network, the impact curve, the five-learner table) are not reused.

## Re-author, session AF

The reuse triage (`docs/reviews/review-reuse-af-hits.md`) ruled three pieces re-author. Ids kept: `p-futures-lasso` is still a futures desk (power futures), and `p-built-ridge` now builds a ridge fit by hand from the normal equations. Detail and gates: `docs/reviews/review-reuse-af-hits-reauthor-stat-learning.md`.

- `problems-2` `p-futures-lasso`: the OLS forecast of a power futures desk, then the lasso forecast as $\alpha$ grows (0.9 at 0.2), the $\alpha$ where it first reaches 0 (0.8, after demand leaves at 0.5), and the forecast at the chosen $\alpha = 1.0$ ($-0.1$). Closest: `l8-setting-to-zero.json` screens[1] and quiz[2] (one coefficient after the penalty), screens[6] and [8] (who leaves first, the empty model), `review-2.json` items[3] (count survivors), `l5-linear-as-learner.json` screens[9] (a test $R^2$ from a fitted model). None of them follows a forecast along $\alpha$, finds where it changes sign, or reads the slope change when a coefficient reaches 0; no part counts survivors, asks one coefficient, asks the emptying $\alpha$ or standardises a raw value.
- `problems-2` `p-built-ridge`: two correlated z-scored signals ($\sum x_1x_2 = 40$ of 50), OLS by the 2 by 2 normal equations ($-1.0$ on quote updates), ridge at $\lambda = 10$ by $(\mathbf{X}^T\mathbf{X} + \lambda\mathbf{I})$ ($-0.3$), its test MSE on four held-out hours (0.355) and test $R^2$ (0.897). Closest: `homework-2.json` items[4] and `l7-shrinking.json` screens[3] and [4] (uncorrelated built market, the factor $n/(n + \lambda)$, expected test MSE), quiz[3] and `review-2.json` items[6] (the factor), `l7` screens[5] and `homework-2.json` items[8] (the matrix formula in code), `l8` quiz[1] (ridge splits a copied column). This item has correlated features, so the factor is a named slip; it solves the equations by hand, scores real held-out rows and uses no expected test MSE, no true coefficients and no noise variance.
- `problems-4` `p-renewals` part 2: the learner is chosen on unequal validation scores; the network's 129 parameters on 320 fitting rows fall from 0.96 to 0.75. Closest: `l19-which-learner.json` quiz[1], `review-4.json` items[5] and `homework-4.json` items[9] (tie-breaks), `l17-a-small-network.json` screens[11] (training accuracy of a large network). No tie: the part ranks by validation, not by fitting rows, and reads the fitting-to-validation drop as variance.

Checks after the re-author: numbers script 0 failures (1269 checks; the lasso by scikit-learn on an orthogonal design and bisection for the zero, the ridge by scikit-learn on data built with the stated sums), reader script 0 failures (2197 checks, blocks retargeted), validator 0 errors with no warning on the new parts, voice 0 and 0, fresh-check 0 hits on both sets, `same-course-reuse --all` no error for the course, `grade-all --file` 0 failures on both sets, playthrough green with and without `--mobile` on both sets.

## Engine limits

None found for any of the four sets; nothing raised to `docs/BACKLOG-INBOX.md`.

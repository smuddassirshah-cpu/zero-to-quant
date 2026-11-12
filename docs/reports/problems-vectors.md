# Problem sets: vectors (brief `docs/briefs/chained.md`)

Files: `app/content/courses/vectors/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-vectors-numbers.py` (exit 0, 935 checks, 0 failures after the fix pass). Commits: 90dad0e (level 1), b7bbdce (level 2), f960ba9 (level 3), then this report.

Read first: every screen and quiz of l1 to l12, review-1 to 3, homework-1 to 3 and the four Fluency sets, for settings to avoid (factor exposures of a long-short book, two-fund factor targets, correlation and beta as cosine and projection, two-asset portfolio variance, the options desk's delta and vega hedge, minimum-variance weights, bond discount factors).

Answer kinds. AUTHORING section 3 ("Vectors and matrices") says one `expression` widget takes a vector, `(a, b)` or `[a, b]`, and a matrix, `pmatrix` or `[[a, b], [c, d]]`, entry by entry. So vector and matrix results are typed whole; every matrix part says "Type it row by row, as `[[a, b], [c, d]]`." and lists that form in `accept`.

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-charging-robot | 4 (3 / 1 / 0) | l1, l2, l3 | 3 |
| problems-1 | p-active-bets | 4 (3 / 1 / 0) | l1, l2, l3, l4 | 4 |
| problems-1 | p-drone-crosswind | 5 (4 / 1 / 0) | l1, l2, l3 | 5 |
| problems-1 | p-stress-hedge | 4 (4 / 0 / 0) | l1, l2, l4 | 4 |
| problems-2 | p-italic-letters | 4 (1 / 3 / 0) | l5, l6, l7 | 3 |
| problems-2 | p-site-plan | 4 (1 / 3 / 0) | l5, l6, l7, l8 | 4 |
| problems-2 | p-factor-risk | 5 (3 / 2 / 0) | l5, l7, l8 | 5 |
| problems-2 | p-bakery-costs | 5 (3 / 1 / 1) | l5, l7, l8 | 4 |
| problems-3 | p-goat-feed | 4 (1 / 3 / 0) | l9, l10, l11 | 3 |
| problems-3 | p-paint-tints | 5 (3 / 1 / 1) | l9, l10, l11, l12 | 4 |
| problems-3 | p-colour-sensor | 5 (1 / 3 / 1) | l8, l10, l11 | 4 |
| problems-3 | p-engraver-dial | 5 (1 / 4 / 0) | l7, l10, l11 | 5 |

Typed parts: level 1 17 of 17, level 2 17 of 18, level 3 17 of 19 (after the fix pass below). The three choice parts are judgements on sizes and transposes (which product is the exposure column, which is the cost per item) or on solvability (no mix reaches an off-line colour).

Chains. Level 1: weights $(2, 3)$ to the legs' dot product 30, the 45° turn, then the straight line $\sqrt{145}$ from the expanded square; active weights to the active return $-0.55\%$, their length 0.1871 and the 130° angle with March's returns; the route's unit vector to the headwind $-4$, the 7 km/h crosswind, the 24 km/h left along the route and the 60-minute flight; a crash return of $-2.2\%$ to the switch $h = 0.11$ that zeroes it, its cost in a rate rise and the central case. Level 2: a slant matrix to an image, the product $\mathbf{DS}$ and the final point; a turn $\mathbf{R}$ to $\mathbf{R}^T\mathbf{R} = \mathbf{I}$, ground to plan with $\mathbf{R}^T$ and a pipe's ground angle; $\mathbf{B}^T\mathbf{w}$ to $\mathbf{F}\mathbf{e}$, $\mathbf{e}^T\mathbf{F}\mathbf{e}$ and 16.2% volatility; ingredients $\mathbf{Q}\mathbf{x}$ to the bill, $\mathbf{c} = \mathbf{Q}^T\mathbf{p}$ and next week's bill. Level 3: a feed system to its determinant, inverse and blend; a tint matrix's singular $k$, its rank in NumPy, an unreachable colour, a reachable one, then a fixed $k$; a sensor's area factor to $\mathbf{M}^{-1}$, the `*` slip and the true colour; a two-step engraver $\mathbf{C}_k$ to its determinant $2 - k$, the dead dial setting, $\mathbf{C}_1^{-1}$ and a design point. Each later part restates the value it uses, and its `wrong` list holds the value the commonest slip before it gives (`swapped`, `transposed`, `order`, `diagonal`, `unswapped`).

Judgement calls a reader may question: `p-site-plan` part 4 uses part 3 through the borehole's plan point (the pipe's plan step is $(10, 5) - (10, -5)$); `p-paint-tints` part 4 rests on part 3's conclusion (blue is a quarter of red), not on a number; `p-paint-tints` part 2 and `p-colour-sensor` part 3 are the set's two uses of l12, since a problem set has no code part.

Form. Every non-whole numeric part names its form; every whole-number part says "Give a whole number" (or minutes, degrees). Angles carry `unit` "°", speeds "km/h", distances "m", time "minutes", money "£", returns "%". Each `wrong` value on a rounded part carries a band at the asked rounding (`[wrong-band]` clean).

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (820 checks in all) |
| validator | 0 errors; no warning on the file | same | same |
| playthrough `--local-cdn` | green (17 parts) | green (18 parts) | green (18 parts) |
| playthrough `--mobile` | green; 440 px shots read, no layout fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

Extra check: `tools/grade-regression.mjs` run on a scratch copy holding only these three files (`--content`): every key and accept form grades correct, and all 121 `wrong` entries grade wrong and land on their own key through the real grader, the matrix in $k$ included.

## Fresh-check

At the gate: 0 hits on all three sets. Advisories: shared small returns (0.01 to 0.05) with l4, l8 and three exams (number coincidences, different settings). One advisory on level 2 led to a change: the factor covariance first used 0.04 and 0.01, the variances of l8's covariance screen, so $\mathbf{F}$ became 0.0225, 0.003, 0.0064. At `--min-run 8 --min-share 0`: 15, 1 and 4 hits, all form sentences ("give a decimal to # places using # from part", "type it row by row as"). The settings (a warehouse robot, active weights against a benchmark, a drone in a crosswind, a stress-test hedge, an italic font tool, a site plan's turned axes, a two-factor risk model, bakery costs, goat feed, paint tints, a leaky colour sensor, a two-step engraver) are new to the course.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems vectors)". None blocked a problem.

## Fix pass (review-problems-1.4-a, problems-1 to 3)

`p-charging-robot` (new arrows $(4, 1)$ and $(1, 3)$, charger $(11, 11)$, and a last part that needs the whole chain: how much shorter the straight line is than the two legs), `p-factor-risk` (hedge the market exposure with a future, then the hedged variance and the cut in it) and `p-colour-sensor` (a leak then a gain: the single matrix, its area factor, its inverse, the true colour and the order that undoes the stages) were re-authored with a new task structure and new numbers (finding 8). The other changes are the per cent decimal lines (finding 5), the accept forms for a number times a vector or matrix and for the factorised engraver matrix (findings 2 and 6), the site-plan angle wording (finding 3) and the engraver sign-slip line (finding 7). The nine matrix parts that wait for the engine fix (finding 1) are listed in the review. Numbers script: 935 checks, 0 failures, a stale-value check on each re-authored item. Fresh-check: 0 hits; no advisory on `problems-2` or `problems-3`.

# Widget catalogue: probability, statistics and time series

Blueprint work file, Stage 2 Phase 1. Draft 1, 6 October 2026.

**Scope.** Every interactive widget needed to teach curriculum items 1.5 Probability (250 h), 1.6 Statistics (120 h) and 2.2 Time series (60 h), Brilliant-style (act before you read, the diagram explains, direct manipulation, one idea per screen) and at the depth of a top quant programme: Stat 110 and Blitzstein and Hwang for 1.5, DeGroot and Schervish for 1.6, Hyndman's Forecasting: Principles and Practice (Pythonic edition) and Tsay for 2.2, with Mosteller, Zhou (the green book) and Jane Street's probability guide for interview-style problems.

**Read for this file.** `docs/curriculum.md`; `docs/design-research.md` sections 2, 4, 5, 8, 9 and 10; the Stage 1 prototype (`css/tokens.css`, `js/screens/lesson.js`, `drill.js`, `drill-worker.js`); the sibling work files `widgets-stage0.md` and `widgets-calc-linalg.md`; the owner's lesson-creator, maths-teaching and project-forge skills; the Artifact `sample` and `db` contracts (version 0.2.69).

**How to read it.** Section 1 walks every lesson and names what the learner must manipulate, see, build or predict. Every widget below exists because a row in section 1 needs it. Section 2 states what this cluster adds to the shared widget contract. Sections 3 to 8 specify the widgets. Sections 9 to 13 cover generators, the misconception register, rejected alternatives, the full widget table and cross-cluster needs.

**Numbering.** Course and lesson numbers (1.5.1 to 1.5.9, 1.6.1 to 1.6.6, 2.2.1 to 2.2.5, and L1, L2 inside them) are this catalogue's working outline, written to test coverage. The course-architecture blueprint owns the final outline; renumbering it changes no widget.

**Evidence tags**, as in the design research: [our choice] for decisions without Brilliant evidence, [unverified] for facts not yet measured, [inferred] for deductions, [sourced] for facts from a cited source.

---

## 0. Summary and decisions

- **40 new widgets:** 3 primitives and 37 composites. 25 are P0 (all of 1.5), 9 are P1 (1.6) and 6 are P2 (2.2). Section 12 lists them all.
- **45 widgets from the sibling catalogues are reused with a change:** 31 composites and inputs gain a mode this cluster needs (section 5), and 14 shared primitives gain additions (section 4). Reuse comes first: nothing here rebuilds `outcome-grid`, `tree-diagram`, `trial-simulator`, `counting-slots`, `venn-diagram`, `pascal-triangle`, `path-simulator`, `linear-dynamics`, `least-squares-fit` or `filtration-tree`.
- **Generators.** All 37 composites need seeded generators for practice, homework and exams (section 9). The 3 primitives do not.
- **Build waves inside P0:** D0 (cluster primitives and the statistics core), D1 (counting and conditional probability), D2 (discrete random variables), D3 (continuous, joint, conditional expectation, limit theorems), D4 (Markov chains, random walks, interview patterns). P1 is wave E (1.6), P2 is wave F (2.2). The calc-linalg catalogue calls the whole of probability wave D; D0 to D4 subdivide it.

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Reuse | Extend sibling widgets with modes (section 5); build a new composite only where no sibling widget can carry the idea | A self-contained probability widget set | Two copies of a dice grid or a Galton histogram means two sets of defects. The Stage 1 lesson's 23 defects were mostly machinery |
| 2 | New primitives | `mass-editor`, `node-graph`, `chance-object` | Composite-private code for sum-to-one editing, state diagrams and dice art | Each is needed by four or more composites here and by other clusters (portfolio weights, algorithm graphs, interview games) |
| 3 | What simulations grade | Never the random estimate. Checks grade exact values, predictions made before running, or computations on fixed item data | Grading a simulated proportion within a tolerance | A tolerance on a random estimate either fails honest learners on unlucky seeds or is too wide to teach anything |
| 4 | Discrete probability arithmetic | Exact BigInt rationals for every discrete probability the learner computes or the screen shows as a fraction; floats for densities and simulation | Floats everywhere | $\frac{1}{11}$ must never show as 0.0909090909; exact equality also makes equation-system and stationary-distribution checks exact |
| 5 | Statistics core | Our own `stats-core` module that bundles selected stdlib-js distribution and special-function packages (Apache-2.0) with our own tests layer; MacKinnon response-surface tables ported from statsmodels (BSD-3-Clause) with attribution | jStat; Pyodide statsmodels in the browser for widget numbers; writing every special function from scratch | stdlib-js packages are ports of established numerical libraries and import one function at a time. Pyodide is about 13 MB and cannot run in the Artifact. Bundle size is [unverified] |
| 6 | Accuracy proof | CI generates golden fixtures with CPython, SciPy and statsmodels pinned to the versions Pyodide ships, and every JS statistic is tested against them | Trusting the JS ports | The 1.6 exit test is literally "match statsmodels" |
| 7 | Data shared between a widget and a code drill | The item's data travel to Python as a literal list or a CSV file. A pure-Python port of the engine RNG ships as a drill prelude for drills that generate their own data | Regenerating with `numpy.random.default_rng` | NumPy's PCG64 cannot reproduce the engine's streams, so the learner's numbers would not match the picture they explored |
| 8 | Colour roles | Theory in slot 3 (aqua), empirical in slot 2 (orange), comparison or prior in slot 6 (violet, dashed), learner-controlled in `--manip` (section 2.4) | Free choice per widget | Learners meet the same three roles in 40 widgets; "orange is what happened, aqua is what theory says" becomes a reading habit |
| 9 | Tutor access to hidden truths | Widgets expose a `secret()` block (true parameters, exact answers, optimal policies). The engine passes it to Bertie only in lesson and explore modes, under a never-reveal instruction | Stage 0's rule (describe never includes hidden values); calc-linalg's "hidden from learner" line inside `describe` | Without the true $\mu$ Bertie cannot aim a hint about a confidence-interval ladder. Keeping it out of `describe` keeps screen-reader text clean |
| 10 | statsmodels summary | Recomputed in JS for `summary-table`; real statsmodels only in web code drills; the Artifact shows fixture values precomputed in CI | Requiring Pyodide for the exit lesson | The explanation must work on a phone in the Artifact; the code drill that proves the learner can match it is web-only |
| 11 | Market data for 2.2 | Seeded synthetic series by default; learner-supplied CSV on the web; no bundled market data | Bundling Yahoo or exchange data | Redistribution rights for free price data are unclear. Synthetic data also let items know the truth |
| 12 | GARCH code drills | The likelihood written by the learner and optimised with `scipy.optimize.minimize` | The `arch` package | `arch` is not on the platform's confirmed Pyodide package list [unverified whether Pyodide ships it] |
| 13 | Geometric distribution convention | Blitzstein and Hwang's convention (failures before the first success, support $0, 1, 2, \dots$) by default; the "trials until first success" form is a labelled config option | Silent switching between books | The exit test is two Stat 110 finals; the green book uses the other convention, so the label is always shown |
| 14 | Discrete CDF drawing | Right-continuous steps: filled dot at the top of each jump, hollow dot at the bottom | Plain steps | The $\le$ against $<$ distinction is the commonest discrete-CDF error and the dots carry it |

### 0.2 Finding: the exit tests examine more than the cover lists

The same pattern the Stage 0 catalogue found holds here.

- **1.5.** The exit test is two Stat 110 past finals at 70%. Those finals routinely examine moment generating functions, order statistics, Beta and Gamma distributions, Poisson processes, transformations and convolutions, the multinomial and multivariate normal, and the Markov, Chebyshev and Jensen inequalities [inferred from the Stat 110 syllabus and the Blitzstein and Hwang chapter list]. The cover list names none of them. This catalogue covers them.
- **1.6.** The exit test asks the learner to explain every number in a statsmodels OLS summary. That table includes Omnibus, Jarque-Bera, Durbin-Watson, skew, kurtosis, log-likelihood, AIC, BIC and the condition number, none of which the cover list names. `summary-table` covers every field.
- **2.2.** Forecasting: Principles and Practice spends most of its length on decomposition, exponential smoothing and forecast evaluation, which the cover list omits. This catalogue covers them at a lighter depth (`series-lab` decomposition, `forecast-lab`), because the 2.1 exit test also needs time-ordered validation.

**Owner decision needed (curriculum, not widgets):** none. The lessons fit the stated hours; the cover lists could name these topics so the course map and the exit test agree.

### 0.3 Names against the sibling catalogues

The two sibling catalogues were written in parallel and name some shared primitives differently. This file uses the first name in each row; the engine blueprint picks the final names, and the mapping is mechanical.

| Used here | Stage 0 file | Calc-linalg file | Notes |
|---|---|---|---|
| `plot-axes` | `plot-axes` | `plot-2d` | |
| `marks` | `curve-layer`, `geo-layer`, `bar-layer` | `marks` | One primitive with many mark types keeps the primitive count small. Section 4.1 adds the mark types this cluster needs |
| `draggable-point` | `draggable-point` | `drag-point` | |
| `slider`, `stepper`, `token-tray`, `number-line` | same | same | |
| `region-selector` | `region-selector` | `region-select` | Calc-linalg's bracket mode is required here |
| `data-table` | `data-table` | `value-table` | |
| `tex-terms` | `tex-terms` | `live-formula` | Addressable, live-updating KaTeX |
| `sim-runner` | (the `seeded-rng` service inside `trial-simulator`) | `sim-runner` | Section 5 asks for `trial-simulator` to be rebuilt on `sim-runner` |
| `sketch-pad`, `matrix`, `plot-3d` | not specified | same | |
| `code-cell` | `code-surface` plus the `python-runner` service | `code-cell` | |
| `choice-cards`, `numeric-entry`, `expression-entry`, `card-sort`, `free-response` | same | `choice`, `numeric-input`, `expression-input` | |
| `derivation` | `derivation` | `derivation-steps` | |
| Element ids `kind:name` | `kind-name` | `kind:name` | |

---

## 1. Lesson map: what the learner does to get each idea

Each row is one lesson idea in depth-first order. "Act" is the hook: what the learner manipulates, builds or predicts before any rule is named. A lesson's Explore screen uses the same widget in `explore` mode with no check. Every lesson also uses the general inputs (`choice-cards`, `numeric-entry`, `expression-entry`, `derivation`, `free-response`); they are listed only where they carry the idea.

### 1.1 Probability (1.5, 250 h; Blitzstein and Hwang, Stat 110)

**1.5.1 Counting and the naive definition** (B&H chapter 1)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Sample spaces and events as sets | Tap the outcomes of three coin flips that make "at least two heads"; combine events with $\cup$, $\cap$ and complement chips | `outcome-grid` (list layout, event chips), `venn-diagram` |
| 2 | The naive definition and when it fails | Predict $P(\text{sum} = 7)$ treating the 11 sums as equally likely, then shade the 36-cell grid | `outcome-grid` (display sum), `choice-cards` (Trap) |
| 3 | The multiplication rule | Fill slots for a number plate; grow a tree and count its leaves | `counting-slots`, `tree-diagram` (count) |
| 4 | Four sampling schemes | Sort eight situations into ordered or unordered, with or without replacement; enumerate each scheme for $n = 4$, $k = 2$ | `card-sort` (bins), `counting-slots` (enumerate), `derivation` |
| 5 | Adjusting for overcounting | Collapse ordered committees into stacks of $k!$; handshakes; seats round a table | `counting-slots` (collapse, circular) |
| 6 | Binomial coefficients and story proofs | Count "committee with a chair" two ways and watch the two lists match; build Vandermonde's identity from two groups; hockey stick | `counting-slots` (procedure comparison), `pascal-triangle`, `derivation` (justify) |
| 7 | Stars and bars, and its probability trap | Drop dividers between stars; then see that the configurations are not equally likely when balls are placed one at a time | `counting-slots` (stars and bars, probability toggle) |
| 8 | Multinomial coefficients | Arrange the letters of MISSISSIPPI; divide by the repeats | `counting-slots` |
| 9 | The birthday problem | Predict the group size that gives 50%; plot $P(\text{no match})$ against $n$; count the $\binom{n}{2}$ pairs; simulate | `graph-explorer` (integer $n$), `trial-simulator` (birthday), `indicator-board` (pairs) |
| 10 | Axioms and their consequences | Edit the masses of the four atoms of a two-set diagram; derive $P(A^c)$, monotonicity and $P(A \cup B)$ | `venn-diagram` (probability mode), `prob-square` (events), `derivation` |
| 11 | Inclusion-exclusion | Count the regions of three sets, then do it with probabilities | `venn-diagram` (3 sets) |
| 12 | De Montmort's matching problem | Shuffle letters into envelopes; the inclusion-exclusion sum approaches $1 - e^{-1}$ | `trial-simulator` (permutation), `indicator-board` (fixed points), `derivation` |
| 13 | "At least one" by complements | Two routes to de Méré's "at least one six in four rolls" | `counting-slots`, `trial-simulator` |
| 14 | Symmetry arguments | Is the first ace more likely above or below the first king? Tap where the special card lands | `indicator-board` (card positions), `choice-cards` |

**1.5.2 Conditional probability and Bayes' rule** (B&H chapter 2)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Conditioning shrinks the sample space (the Stage 1 reference lesson) | Apply "at least one 5"; count what is left | `outcome-grid` (condition, shrink) |
| 2 | Conditional probability as an area ratio | Condition on $B$ in the unit square; $B$'s pieces stretch to fill it | `prob-square` (condition) |
| 3 | The multiplication rule and trees | Multiply along branches; match each leaf to a rectangle | `tree-diagram`, `prob-square` (events) |
| 4 | Law of total probability | Split the square into a partition; drag widths and heights; $P(B)$ is the width-weighted mean height | `prob-square` (partition), `tree-diagram` |
| 5 | Bayes' rule with natural frequencies | Filter 1,000 people to the positive tests and count | `icon-array` (bayes), `prob-square` (bayes) |
| 6 | Base-rate neglect (Trap) | Predict the chance of disease after a positive from a "99% accurate" test at 1% prevalence | `icon-array`, `choice-cards` |
| 7 | Flipping the tree | Rebuild the tree split by test result first; the leaves keep their probabilities | `tree-diagram` (flip) |
| 8 | Odds form and sequential evidence | Drag evidence cards onto the log-odds line; reorder them and see the same end point | `odds-ledger` |
| 9 | Conditional probabilities are probabilities; conditioning twice | Apply a second piece of evidence to the posterior square | `prob-square` (bayes, evidence sequence), `derivation` |
| 10 | Independence; independent is not disjoint | Make $A$ and $B$ independent by aligning the splits; then try to make them disjoint and independent | `prob-square` (events), `outcome-grid` (row proportions) |
| 11 | Pairwise against mutual independence | Two fair coins and "the coins match": check each pair, then all three | `outcome-grid` (event chips), `contingency-table` |
| 12 | Conditional independence and its failure | Two tests independent given disease become dependent once disease is unknown | `prob-square` (nested), `icon-array` |
| 13 | Monty Hall | Play ten rounds; simulate "always switch"; then an ignorant host | `game-lab` (Monty Hall), `tree-diagram` |
| 14 | First-step analysis: gambler's ruin | Write one equation per state, solve, simulate | `first-step-solver`, `path-simulator` (barrier) |
| 15 | Simpson's paradox | Combine two strata and watch the comparison flip; resize strata until it does not | `contingency-table` (strata), `icon-array` (simpson) |
| 16 | Prosecutor's fallacy: $P(A \mid B)$ against $P(B \mid A)$ | A one-in-a-million DNA match in a city of 5 million | `icon-array` (fallacy), `odds-ledger` |
| 17 | Bayes in quant settings | Fair coin or two-headed coin; is the trader skilled after 8 winning months out of 10 | `odds-ledger`, `prob-square` (bayes, 3 to 5 hypotheses) |

**1.5.3 Discrete random variables and expectation** (B&H chapters 3 and 4)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | A random variable is a function | Assign a number to each outcome; tap a value to see its preimage | `rv-mapper` |
| 2 | PMFs | Pour each outcome's mass into its value; spot the invalid PMF | `rv-mapper`, `mass-editor` |
| 3 | CDFs: steps, jumps and $\le$ against $<$ | Shade $P(2 < X \le 5)$ on both panels; toggle the endpoints; sketch a CDF from a PMF | `dist-explorer`, `sketch-pad` |
| 4 | Bernoulli and binomial: the story | Steer a ball through a Galton board; count the paths to each bin | `galton-board`, `pascal-triangle`, `binomial-expander` (probability mode) |
| 5 | Hypergeometric against binomial | Draw from an urn with and without replacement; capture-recapture; Fisher's tea taster | `trial-simulator` (urn), `dist-explorer` (compare) |
| 6 | Functions of a random variable | Push $X$ uniform on $\{-2, \dots, 2\}$ through $g(x) = x^2$; values merge | `rv-mapper` (g stage) |
| 7 | Independent variables and their sums | Sum two dice along the anti-diagonals of the grid | `convolver` (discrete grid), `outcome-grid` |
| 8 | Expectation as a balance point | Slide a fulcrum under a PMF until it balances, then compute | `dist-explorer` (fulcrum), `mass-editor` |
| 9 | Linearity of expectation | Predict the expected number of fixed points of a shuffle for $n = 3, 10, 52$; light the indicators | `indicator-board` (fixed points) |
| 10 | Indicators and the fundamental bridge | Derive the binomial and hypergeometric means from indicators | `indicator-board`, `derivation` |
| 11 | Geometric and negative binomial; waiting times | Flip until the first head; histogram of waits; the two conventions | `trial-strip`, `dist-explorer` |
| 12 | Memorylessness | Condition on five failures; the remaining wait has the same histogram | `trial-strip` (condition) |
| 13 | Pattern waiting times | Predict whether HH or HT takes longer; race them; Penney's game | `trial-strip` (pattern race), `first-step-solver` (pattern automaton), `game-lab` (Penney) |
| 14 | LOTUS | Compute $E[X^2]$ through the outcomes and through the values | `rv-mapper` (lotus), `dist-explorer` |
| 15 | Variance and standard deviation | Drag mass outwards; deviation squares grow; $\mathrm{Var}(aX + b)$ | `dist-explorer` (deviation squares), `mass-editor` |
| 16 | Variance of a sum of indicators | The number of fixed points has variance 1; read the covariance grid | `indicator-board` (covariances) |
| 17 | Poisson as the law of rare events | Raise $n$ with $np$ fixed; the binomial and Poisson bars merge | `dist-explorer` (compare), `trial-strip` (discretised) |
| 18 | Poisson approximation in practice | Matching birthdays among 100 people; rare defaults in a loan book | `indicator-board` (pairs), `dist-explorer` |
| 19 | St Petersburg paradox | Play; the running average never settles; expectation against utility | `game-lab` (St Petersburg) |
| 20 | Coupon collector | Sum geometric waits to get $nH_n$ | `indicator-board` (coupons), `trial-strip`, `derivation` |

**1.5.4 Continuous random variables and the named distributions** (B&H chapters 5, 6 and 8)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | From histograms to densities | Narrow the bins as the sample grows; heights become density | `sampling-lab` (population view), `stat-chart` (frequency density) |
| 2 | PDF and CDF; probability is area; $P(X = x) = 0$ | Drag bracket ends; area and $F(b) - F(a)$ agree; meet a density above 1 | `dist-explorer`, `accumulator` |
| 3 | Universality of the uniform | Drop uniform dots through the CDF to build any distribution; run it backwards | `dist-explorer` (inverse transform, PIT) |
| 4 | The normal: standardising, 68-95-99.7 | Shift, then scale, to $Z$; read $\Phi$ | `dist-explorer` (standardise) |
| 5 | Exponential and memorylessness | Wait at a bus stop that has no memory | `dist-explorer`, `trial-strip` (Poisson) |
| 6 | Poisson processes | Count arrivals in windows; gaps; merge two streams; thin one | `trial-strip` (Poisson) |
| 7 | Gamma and Beta | Gamma as a sum of exponential waits; Beta as an order statistic | `convolver` (repeat), `order-statistics`, `dist-explorer` |
| 8 | Lognormal, Cauchy, $t$ and $\chi^2$ | Explore shapes; watch a Cauchy running mean refuse to settle | `dist-explorer`, `sampling-lab` (Cauchy) |
| 9 | Mean, median and mode as loss minimisers | Drag a guess $c$; $E[(X - c)^2]$ bottoms out at the mean, $E\lvert X - c \rvert$ at the median | `dist-explorer` (loss) |
| 10 | Moments, skewness and kurtosis | Compare readouts across families | `dist-explorer`, `sampling-lab` |
| 11 | MGFs: moments from derivatives | Drag $t$ near 0; the slope of $M(t)$ is $E[X]$ | `generating-function`, `taylor-builder` |
| 12 | MGFs of sums; uniqueness | Multiply two MGF curves; match an MGF to its distribution | `generating-function` (product, match) |
| 13 | PGFs and branching processes | Iterate $s \mapsto G(s)$ to the extinction probability | `generating-function` (PGF, cobweb), `iteration-cobweb` |
| 14 | Change of variables | Squeeze an interval through $g$; the density rescales by $1/\lvert g' \rvert$ | `function-mapping` (density mode) |
| 15 | Convolution of densities | Slide the flipped density; trace the sum of two uniforms | `convolver` (flip and slide) |
| 16 | Order statistics | Predict the expected maximum of $n$ uniforms; histogram of $U_{(k)}$ | `order-statistics` |
| 17 | Symmetry of iid continuous variables; records | Light the record indicators; $P(\text{record at } j) = 1/j$ | `indicator-board` (records) |

**1.5.5 Joint distributions, covariance and the multivariate normal** (B&H chapters 7 and 8)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Joint PMF tables, marginals, conditionals | Sum rows and columns; normalise one row | `contingency-table` (joint), `joint-density` (table) |
| 2 | Joint PDFs; marginals by integrating out | Squash the heatmap onto each axis | `joint-density` |
| 3 | Conditional densities as renormalised slices | Drag the slice; compare raw heights with the renormalised curve | `joint-density` |
| 4 | Independence of continuous variables | Are all the slices the same shape? | `joint-density` |
| 5 | Regions and 2D LOTUS | $P(X < Y)$; $E\lvert X - Y \rvert$ for two uniforms | `joint-density`, `region-bounds`, `geo-prob` |
| 6 | Covariance as average signed area | Drag points; their rectangles flip sign | `covariance-lab` |
| 7 | Correlation; uncorrelated but dependent | Guess the correlation; build $Y = X^2$ with zero correlation | `covariance-lab` |
| 8 | Variance of sums; the two-asset portfolio | Set $\rho$; find the minimum-variance weight | `gaussian-2d` (combination, portfolio), `covariance-lab` (sum) |
| 9 | Multinomial | Count arrangements; sample from an urn with three colours | `counting-slots`, `trial-simulator` (urn) |
| 10 | Bivariate normal; regression to the mean | Shape the ellipse; slice it; the conditional mean line is not the major axis | `gaussian-2d` |
| 11 | Linear combinations; Cholesky construction | Build correlated normals from independent ones | `gaussian-2d` (Cholesky), `transform-grid` |
| 12 | Normal marginals, zero correlation, still dependent (Trap) | Flip a random sign; the cloud is an X | `gaussian-2d` (show-why), `joint-density` |
| 13 | 2D change of variables; Box-Muller | Map polar coordinates to two normals | `transform-grid`, `joint-density` |

**1.5.6 Conditional expectation** (B&H chapter 9)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | $E[Y \mid X = x]$ as slice means | Drag one prediction per slice to make the squared error as small as possible | `cond-expectation` |
| 2 | $E[Y \mid X]$ is a random variable | Collapse every point to its slice mean | `cond-expectation` (collapse) |
| 3 | Adam's law (the tower property) | Average the collapsed points; average atoms of a coin-toss tree | `cond-expectation`, `filtration-tree` (conditional expectation, tower) |
| 4 | Eve's law | Build the variance bar from "within slices" and "between slice means" | `cond-expectation` (Eve bar) |
| 5 | Random sums and hierarchical models | $E[S_N] = E[N]E[X]$ from grouped data | `cond-expectation` (groups), `trial-simulator` |
| 6 | Best predictor; the linear special case | Compare the slice-mean curve with the best straight line | `cond-expectation` (MSE), `gaussian-2d` (regression line) |
| 7 | Conditioning as a problem-solving tool | $E[\text{tosses until HH}]$ by conditioning on the first tosses | `first-step-solver` |
| 8 | Conditional expectation as a projection | See the residual orthogonal to every function of $X$ | `cond-expectation` (projection view), `least-squares-fit` |

**1.5.7 Inequalities and limit theorems** (B&H chapter 10)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Markov and Chebyshev | Drag a threshold; compare each bound with the exact tail; build the distribution that makes Markov tight | `dist-explorer` (bounds), `mass-editor` |
| 2 | Chernoff (preview) | Watch the exponential bound beat Chebyshev in the tail | `dist-explorer` (bounds) |
| 3 | Jensen's inequality | A random point on a chord: $E[g(X)]$ against $g(E[X])$ | `convexity-chord` (random-variable mode), `rv-mapper` |
| 4 | Cauchy-Schwarz and $\lvert \rho \rvert \le 1$ | Try to push a sample correlation past 1 | `covariance-lab`, `derivation` |
| 5 | Weak law of large numbers, proved from Chebyshev | Run trials; the proportion's funnel narrows like $1/\sqrt{n}$ | `trial-simulator` (funnel), `sampling-lab` (LLN), `derivation` |
| 6 | Gambler's fallacy: proportions converge, counts do not | Watch $\lvert S_n - n/2 \rvert$ grow while $S_n/n$ settles | `trial-simulator` (count-deviation trace) |
| 7 | When the law fails: Cauchy | Running mean of Cauchy draws | `sampling-lab` (LLN, Cauchy) |
| 8 | Central limit theorem | Predict the shape of the mean of 2, 5 and 30 skewed draws | `sampling-lab` (CLT), `galton-board`, `convolver` (repeat) |
| 9 | Normal approximation and continuity correction | Overlay the normal on binomial bars; shade with and without the half-unit | `dist-explorer` (compare, continuity) |
| 10 | Student $t$ and $\chi^2$ as sampling distributions | Standardise small-sample means with $s$; the tails fatten | `sampling-lab` (t statistic), `dist-explorer` |
| 11 | Delta method (preview) | Linearise $g(\bar X)$; compare spreads | `taylor-builder` (delta method), `sampling-lab` |

**1.5.8 Markov chains** (B&H chapter 11)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | The Markov property; diagram and matrix | Walk a token; read each row as "where next" | `markov-chain` (diagram, matrix, walker) |
| 2 | $n$-step transitions | Step a population vector; compare with $P^n$; two-step paths as sums | `markov-chain` (population), `matrix-multiply` |
| 3 | Classification of states | Group states into communicating classes; mark recurrent and transient | `markov-chain` (classes) |
| 4 | Stationary distributions | Enter $\pi$ and test $\pi P$; compare with long-run visit frequencies | `markov-chain`, `eigen-finder`, `linear-dynamics` (Markov mode) |
| 5 | Convergence and periodicity | A periodic chain oscillates for ever | `markov-chain` |
| 6 | Reversibility and detailed balance | Balance the flows on each edge | `markov-chain` (flows) |
| 7 | Random walks on graphs; PageRank | Stationary mass proportional to degree; add teleporting | `markov-chain` (graph walk, PageRank) |
| 8 | Absorbing chains | Expected visits from $(I - Q)^{-1}$; absorption probabilities | `markov-chain` (absorbing), `first-step-solver` |
| 9 | Transfer: credit-rating migration | Default probability over five years from a rating matrix | `markov-chain` (ratings preset) |

**1.5.9 Random walks and interview patterns** (B&H chapters 2, 11 and 13; Mosteller; Zhou chapter 4)

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Simple random walk paths and counts | Build paths step by step; count paths to an endpoint | `lattice-walk` (build, count), `pascal-triangle` |
| 2 | Reflection principle; ballot theorem | Reflect the path before its first touch | `lattice-walk` (reflect, ballot) |
| 3 | Catalan numbers | Count paths that never go below zero | `lattice-walk` (Catalan) |
| 4 | Gambler's ruin with drift; expected duration | Solve by first-step analysis; check by simulation | `first-step-solver`, `path-simulator` (barrier) |
| 5 | First passage, maximum, return to the origin | Histogram of the running maximum | `lattice-walk` (max), `path-simulator` |
| 6 | Scaled walks towards Brownian motion (preview of 3.2) | Shrink steps as $1/\sqrt{n}$ | `path-simulator` (scaled walk) |
| 7 | Geometric probability: the meeting problem | Drag the point $(X, Y)$; build $\lvert X - Y \rvert < w$ | `geo-prob` (meeting) |
| 8 | Broken stick | Drag the two cuts; light the triangle region | `geo-prob` (broken stick) |
| 9 | Buffon's needle; Bertrand's paradox | Three ways to draw a "random chord" give three answers | `geo-prob` (Buffon, Bertrand) |
| 10 | Optimal stopping: dice games | Fill the value table from the last roll backwards | `game-lab` (dice stop, induction) |
| 11 | The secretary problem | Slide the look-only fraction; find $1/e$ | `game-lab` (secretary) |
| 12 | Two-envelope paradox | Find the step in the switching argument that fails | `game-lab` (two envelopes) |
| 13 | Betting and Kelly (preview; full treatment in 3.3) | Bet a fraction of wealth on a favourable coin | `game-lab` (Kelly, P2 mode) |
| 14 | Martingale intuition: fair games and stopping | No stopping rule beats a fair game with bounded play | `path-simulator`, `filtration-tree` |

### 1.2 Statistics (1.6, 120 h; DeGroot and Schervish; OpenIntro first if needed)

**1.6.1 Sampling and estimation**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Statistics are random variables | Draw samples; each sample mean drops into a second histogram | `sampling-lab` |
| 2 | Standard error $\sigma/\sqrt{n}$ | Predict the spread of the sample mean, then draw 1,000 samples | `sampling-lab` (prediction bracket) |
| 3 | Bias, variance and mean squared error | Race two estimators; read $\text{MSE} = \text{bias}^2 + \text{variance}$ | `estimator-compare` |
| 4 | Why $n - 1$ | Drag a centre $c$ away from $\bar x$; the sum of squares grows; compare divisors $n - 1$, $n$ and $n + 1$ | `dot-plot-stats` (movable centre), `estimator-compare` |
| 5 | Consistency | Raise $n$; the sampling distributions close in on $\theta$ | `estimator-compare` (MSE against $n$) |
| 6 | Method of moments | Match the mean and variance of a family to data | `dist-explorer` (match moments), `estimator-compare` |
| 7 | The German tank problem | Estimate the number of tanks from serial numbers | `estimator-compare` |
| 8 | Efficiency: mean against median | Normal data, then heavy-tailed data | `estimator-compare` |
| 9 | Cramér-Rao bound (after 1.6.2) | See no unbiased estimator's variance cross the bound line | `estimator-compare` (bound line) |
| 10 | Sufficiency (optional) | The likelihood depends on the data only through $T$ | `likelihood-lab` |

**1.6.2 Likelihood and maximum likelihood**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Likelihood is a function of the parameter | Drag $\theta$; each data point's density height changes; their product is $L(\theta)$ | `likelihood-lab` |
| 2 | Log-likelihood and the score equation | Switch to logs; set the derivative to zero | `likelihood-lab`, `derivation` |
| 3 | MLEs for Bernoulli, Poisson, exponential, normal | Find each peak by dragging, then by algebra | `likelihood-lab` |
| 4 | A boundary MLE: uniform on $[0, \theta]$ (Trap) | Slide $\theta$ below the largest observation; $L$ falls to zero | `likelihood-lab` (show-why) |
| 5 | Two parameters | Find the peak of the $(\mu, \sigma)$ log-likelihood contour | `likelihood-lab` (contours), `surface-explorer` |
| 6 | Fisher information and standard errors | Fit a parabola at the peak; curvature gives the standard error | `likelihood-lab` (curvature), `sampling-lab` (MLE spread) |
| 7 | Asymptotic normality, invariance, delta method | Sample the MLE many times; transform it | `sampling-lab`, `taylor-builder` (delta method) |
| 8 | Least squares is maximum likelihood under normal errors | Overlay the two objectives | `likelihood-lab` (regression), `regression-lab` |

**1.6.3 Confidence intervals**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | What "95%" describes | Run 100 intervals; count the ones that miss $\mu$ | `ci-ladder` |
| 2 | One realised interval (Trap) | Is there a 95% chance $\mu$ is inside this interval? | `ci-ladder` (your interval), `choice-cards` |
| 3 | Pivots; $z$ and $t$ intervals | Use $s$ instead of $\sigma$ at $n = 5$; coverage drops until $t$ replaces $z$ | `ci-ladder`, `dist-explorer`, `derivation` |
| 4 | Proportions: Wald fails near 0 and 1 | Read the exact coverage curve; switch to Wilson | `ci-ladder` (coverage curve) |
| 5 | Sample size and margin of error | Halve the width: what happens to $n$? | `ci-ladder` (width against $n$) |
| 6 | Bootstrap intervals | Resample the data with replacement | `sampling-lab` (bootstrap), `ci-ladder` (bootstrap method) |
| 7 | Likelihood intervals (preview) | Cut the log-likelihood 1.92 below its peak | `likelihood-lab` (cut) |

**1.6.4 Hypothesis tests and p-values**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | The logic of a test | Drag the critical value; shade $\alpha$ | `test-lab` |
| 2 | p-values as tail areas | Place the observed statistic; shade beyond it | `test-lab` |
| 3 | What a p-value is not | 1,000 studies, 10% real effects: what share of "significant" ones are real? | `icon-array` (FDR), `test-lab`, `odds-ledger` |
| 4 | Type I and II errors, power | Move the effect size and $n$; watch $\beta$ shrink | `test-lab` |
| 5 | Power curves and sample size | Find the $n$ that gives 80% power | `test-lab` (power curve) |
| 6 | p-values are uniform under the null | Histogram 10,000 null p-values, then alternative ones | `sampling-lab` (p-values) |
| 7 | $t$-tests: one-sample, Welch, paired | Choose the right test for three data sets | `test-lab`, `sampling-lab` |
| 8 | Permutation tests | Shuffle the group labels; build the null distribution | `sampling-lab` (permutation) |
| 9 | $\chi^2$ tests: goodness of fit and independence | Compare observed with expected counts cell by cell | `contingency-table` (expected), `test-lab` ($\chi^2$) |
| 10 | Neyman-Pearson; likelihood-ratio tests | Order outcomes by likelihood ratio to build the best region | `test-lab`, `likelihood-lab` |
| 11 | Tests and intervals are duals | The interval holds the null values the test keeps | `test-lab`, `ci-ladder` |
| 12 | Multiple testing: family-wise error | 20 tests at 5%: chance of at least one false alarm | `multiple-testing` (FWER) |
| 13 | Bonferroni, Holm, Benjamini-Hochberg | Drag the BH line through the sorted p-values | `multiple-testing` (corrections) |
| 14 | p-hacking and forking paths | Choose the best of $k$ analyses per study | `multiple-testing` (forking) |
| 15 | Backtest overfitting | Pick the best of 200 noise strategies; see its out-of-sample Sharpe | `multiple-testing` (strategy zoo) |

**1.6.5 Linear regression**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Least squares by hand | Drag a line to shrink the squares | `least-squares-fit`, `scatter-fit` |
| 2 | Normal equations; the projection picture | Derive $X^\top X \hat\beta = X^\top y$ | `least-squares-fit`, `derivation` |
| 3 | Reading slope and intercept; regression to the mean | Fathers' and sons' heights | `regression-lab`, `gaussian-2d` |
| 4 | Residuals; $SST = SSR + SSE$; $R^2$ | Build the decomposition bars | `regression-lab` (decomposition) |
| 5 | Sampling distribution of $\hat\beta$; standard errors; $t$ | Refit on new samples; the slope histogram builds | `regression-lab` (refits) |
| 6 | Confidence and prediction bands | Why the prediction band never shrinks to zero | `regression-lab` |
| 7 | Assumptions and what breaks | Bend the truth, fan the errors, correlate them, fatten their tails; watch the 95% slope interval's coverage fall | `regression-lab` (violations), `ci-ladder` (coverage), `qq-plot` |
| 8 | Diagnostics | Read residual, QQ, scale-location and influence plots; match each to a violation | `regression-lab` (diagnostics), `qq-plot`, `card-sort` |
| 9 | Multiple regression; Frisch-Waugh-Lovell | Fit a plane; regress residuals on residuals | `regression-lab` (two predictors), `plot-3d` |
| 10 | Omitted-variable bias | Drop $x_2$; the slope on $x_1$ moves by $\beta_2 \delta$ | `regression-lab` (OVB) |
| 11 | Collinearity and variance inflation | Correlate the predictors; the coefficient ellipse stretches | `regression-lab` (collinear), `quadratic-form` |
| 12 | Categorical predictors, interactions, transformations | Add a dummy; fit log of $y$ | `regression-lab` |
| 13 | Gauss-Markov | Compare OLS with another linear unbiased estimator | `estimator-compare`, `derivation` |
| 14 | $F$-tests and nested models | Test two coefficients at once | `test-lab` ($F$), `regression-lab` |
| 15 | Heteroscedasticity-consistent standard errors | Switch the covariance type; standard errors change, coefficients do not | `regression-lab`, `summary-table` |
| 16 | Exit: the statsmodels summary, number by number | Tap each number; predict the blanked ones; then match it in NumPy | `summary-table`, `code-cell` |

**1.6.6 Bayesian updating**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Updating on a grid | Shape a prior; flip coins; multiply and renormalise | `posterior-lab` (grid) |
| 2 | Beta-binomial conjugacy | Read $\alpha$ and $\beta$ as pseudo-counts | `posterior-lab` |
| 3 | Sequential updating equals batch updating | Update flip by flip, then all at once | `posterior-lab`, `odds-ledger` |
| 4 | Credible against confidence intervals | Same data, two intervals, two meanings | `posterior-lab`, `ci-ladder` |
| 5 | Posterior predictive | Probability the next flip is heads | `posterior-lab` |
| 6 | Prior sensitivity | Two analysts, two priors, growing data | `posterior-lab` |
| 7 | Normal-normal: precision weighting | Combine a prior view with noisy data | `posterior-lab` (normal) |
| 8 | Shrinkage across many groups | Shrink 20 managers' noisy alphas towards the pool | `posterior-lab` (groups) |
| 9 | Bayes factors | Compare two models as odds | `odds-ledger` |

### 1.3 Time series (2.2, 60 h; FPP Pythonic edition; Tsay)

**2.2.1 Prices, returns and stationarity**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Prices wander, returns hover | Apply "difference" and "log" chips to a price series | `series-lab` |
| 2 | Simple against log returns; aggregation | Add log returns across days; try it with simple returns | `series-lab` |
| 3 | Weak stationarity | Drag two windows; compare their histograms | `series-lab` (split windows) |
| 4 | Trend, seasonality, random walks; differencing | Classify six series; pick the transform that makes each stationary | `series-lab`, `choice-cards` |
| 5 | Decomposition | Pull trend and season out of a series | `series-lab` (decompose) |
| 6 | Unit roots | Slide $\varphi$ to 1 and past it | `arma-lab` |
| 7 | Dickey-Fuller: the null distribution is not $t$ | Simulate the statistic under a unit root | `test-lab` (simulated null) |
| 8 | ADF and KPSS in practice | Opposite nulls; read both | `test-lab`, `series-lab`, `code-cell` |
| 9 | Spurious regression | Regress one random walk on an independent one | `coint-lab` (spurious), `regression-lab` |

**2.2.2 Autocorrelation**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Lag plots and the ACF | Slide the lag; each scatter's correlation becomes a bar | `acf-lab` |
| 2 | White-noise bands; the 1-in-20 trap | Count bars outside the band for pure noise | `acf-lab` |
| 3 | PACF | Remove the intermediate lags, then correlate | `acf-lab` (PACF) |
| 4 | Ljung-Box | Test many lags at once | `acf-lab`, `test-lab` ($\chi^2$) |
| 5 | Returns against squared returns | Flat ACF for returns, long ACF for squares | `acf-lab` (squares) |

**2.2.3 ARMA models**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | AR(1): mean reversion and half-life | Slide $\varphi$ with the same shocks | `arma-lab` |
| 2 | MA(1) and MA($q$) | Finite memory; the ACF cuts off | `arma-lab` |
| 3 | AR(2): the stationarity triangle; cycles | Drag $(\varphi_1, \varphi_2)$ into the complex-root zone | `arma-lab` (triangle, roots), `complex-plane` |
| 4 | Invertibility | Move an MA root inside the unit circle | `arma-lab` (roots) |
| 5 | Identification from ACF and PACF | Match correlograms to models | `acf-lab`, `card-sort` (match) |
| 6 | Estimation; AIC and BIC | Tap the best cell of a $(p, q)$ grid; see over-fitting | `arma-lab` (fit grid) |
| 7 | Forecasts and their intervals | Stationary fans saturate; random-walk fans grow like $\sqrt{h}$ | `forecast-lab` |
| 8 | Evaluation: rolling origin; leakage | Compare time-ordered with shuffled cross-validation | `forecast-lab` |
| 9 | Exponential smoothing | Slide $\alpha$; weights decay geometrically | `forecast-lab` (SES) |

**2.2.4 Volatility**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Stylised facts: fat tails and clustering | QQ against the normal; ACF of absolute returns | `series-lab` (facts), `qq-plot`, `acf-lab` |
| 2 | EWMA volatility | Slide $\lambda$; read the weights | `garch-lab` (EWMA) |
| 3 | ARCH(1) | One shock, then the next day's variance | `garch-lab` |
| 4 | GARCH(1,1): persistence, long-run variance | Slide $\alpha$ and $\beta$ with fixed shocks | `garch-lab` |
| 5 | Volatility forecasts | The term structure decays at rate $(\alpha + \beta)^h$ | `garch-lab` |
| 6 | Fitting GARCH by maximum likelihood | Drag $(\alpha, \beta)$ on the log-likelihood map | `garch-lab` (fit), `code-cell` |
| 7 | VaR and exceedances | Count days below the 1% line | `garch-lab` (VaR) |

**2.2.5 Cointegration**

| L | Lesson idea | Act | Widgets |
|---|---|---|---|
| 1 | Common stochastic trends | Drag the hedge ratio until the spread stops wandering | `coint-lab` |
| 2 | Correlation is not cointegration (Trap) | Two pairs: high return correlation with no cointegration, and the reverse | `coint-lab` |
| 3 | Engle-Granger in two steps | Regress, then test the residuals against the right critical values | `coint-lab`, `test-lab` |
| 4 | Error correction and half-life | Read the speed of adjustment | `coint-lab` (ECM), `sde-stepper` (OU) |
| 5 | Pairs trading and look-ahead | Trade z-score bands; estimate $\beta$ without peeking | `coint-lab` (trading) |
| 6 | Exit: test a pair; explain returns against prices | Run the test in Python; write the explanation | `coint-lab`, `code-cell`, `free-response` |

---

## 2. What this cluster adds to the shared contract

The shared widget contract is proposed in `widgets-stage0.md` section 1 and `widgets-calc-linalg.md` section 2: a module with `mount`, serialisable state, `answer()`, `lock`, grading marks, `showWhy`, `reveal`, `describe`, element ids, highlight and annotate, `on('change' | 'commit')`, and `destroy`. This file assumes that contract. Where the two drafts differ, the engine blueprint decides; this section states only what probability, statistics and time series add.

### 2.1 Answer and check additions

```ts
// Additions to the sibling Answer and Check unions
type Answer =
  | { type: 'distribution'; support: (number | string)[]; masses: string[] }   // masses as exact 'a/b' or decimals
  | { type: 'policy'; params: Record<string, number> };                        // thresholds in game-lab

type Check =
  | { kind: 'probability'; value: Entry; tol?: Tolerance;
      forms?: ('fraction' | 'decimal' | 'percent' | 'odds')[] }               // numeric, specialised to [0, 1]
  | { kind: 'distribution'; target: Entry[]; metric: 'exact' | 'tv' | 'max-abs'; tol?: number;
      requireValid?: boolean }                                                 // tv: total variation distance
  | { kind: 'policy'; game: string; optimalValue: Entry; tol: number };       // the policy's exact value, not a simulated one
```

- **Probability entry** accepts $\frac{a}{b}$, decimals and percentages, and odds $a:b$ only where the screen asks for odds. A value outside $[0, 1]$ gets a parse-level nudge ("A probability lies between 0 and 1") before Check, so it costs no attempt, following Stage 0's parse-preview rule.
- **Accepted-answer rule** shown after grading, for example "Accepted: $\frac{10}{109}$, or 0.092 ± 0.005".
- **Predicates** this cluster registers (pure, unit-tested, named in content, never supplied as code):

| Predicate | Tests | Used by |
|---|---|---|
| `independent-events` | $\lvert P(A \cap B) - P(A)P(B) \rvert \le$ tol | `prob-square`, `outcome-grid` |
| `disjoint-events` | $P(A \cap B) = 0$ | `prob-square`, `venn-diagram` |
| `valid-pmf` | masses non-negative and summing to 1 exactly (rationals) or within $10^{-9}$ | `mass-editor`, `rv-mapper` |
| `row-stochastic` | every row valid as a PMF | `markov-chain` |
| `is-stationary` | $\lVert \pi P - \pi \rVert_\infty \le$ tol and $\pi$ valid | `markov-chain` |
| `detailed-balance` | $\pi_i P_{ij} = \pi_j P_{ji}$ for all pairs | `markov-chain` |
| `class-partition` | learner's groups equal the communicating classes | `markov-chain` |
| `system-equivalent` | learner's first-step equations have the same solution set as the true system, by exact row reduction of both | `first-step-solver` |
| `region-equals` | area of the symmetric difference of two polygons below $10^{-6}$ | `geo-prob` |
| `path-property` | a lattice path satisfies a named property (stays positive, touches level $k$, ends at $k$) | `lattice-walk` |
| `matches-moments` | mean and variance within tolerance of targets | `dist-explorer` |
| `corr-near` | sample correlation within tolerance of a target | `covariance-lab` |
| `slice-means-fit` | every slice prediction within tolerance of the slice mean | `cond-expectation` |
| `in-region` | a parameter point lies in a named region (stationarity triangle, $\alpha + \beta < 1$) | `arma-lab`, `garch-lab` |
| `transform-sequence` | the applied transforms equal one of the accepted sequences | `series-lab` |
| `hedge-ratio-near` | learner's $\beta$ within tolerance of the true or OLS ratio | `coint-lab` |

### 2.2 Randomness, seeds and grading

1. **Never grade a random estimate.** A check grades an exact value, a prediction made before running, or a computation on fixed item data. Simulation exists to confirm a prediction, never to be the answer.
2. **Fixed item data.** Data the learner computes from are fixed by the item's seed and shown in a table, so two learners with the same item see the same numbers.
3. **Streams.** Each widget asks `ctx.rng(stream)` with labels `data` (item data, fixed), `explore` (changed by "New seed") and `sim:<widget-id>`. "New seed" changes only `explore` and `sim` streams.
4. **Exact discrete arithmetic.** Discrete probabilities use BigInt rationals end to end and display as a fraction with a decimal beside it.
5. **Cross-device determinism.** Integer-based draws (Bernoulli by integer threshold, dice, permutations) are identical on every device. Continuous draws pass through `Math.log` and `Math.cos`, which ECMAScript lets engines approximate differently in the last bit, so a histogram may differ by one count between browsers [inferred from the specification's "implementation-approximated" wording]. Rule 1 makes this harmless.
6. **Two-way verification of every generated answer** in CI: an exact or closed-form solver, and a seeded simulation of at least $10^6$ draws that must land within 4 standard errors. Because the CI seed is fixed, the test cannot flake.
7. **Drills that share data with a widget** receive it as a literal or a CSV file (decision 7). Drills that generate their own data import `zq_rng`, a pure-Python port of the engine generator that uses only 32-bit integer arithmetic, so it runs unchanged on CPython, Pyodide and MicroPython.

### 2.3 Example screen as data

A Problem screen from 1.5.2 L5. The widget, the check, the misconception and its show-why are all data; no lesson code exists.

```json
{
  "id": "1.5.2.L5.s3",
  "type": "problem",
  "prose": "One in 100 people has the condition. The test catches 90% of cases and wrongly flags 9% of everyone else. You test positive.",
  "widgets": [{
    "type": "prob-square", "id": "sq", "label": "Everyone, as a square",
    "mode": "bayes",
    "labels": { "hyps": ["Has it", "Does not"], "evidence": "Positive" },
    "init": { "priors": ["1/100", "99/100"], "likelihoods": ["9/10", "9/100"] },
    "editable": [], "show": { "areas": "percent", "formula": false, "braces": true }
  }],
  "answer": { "type": "numeric-entry", "id": "post",
              "fields": [{ "id": "p", "label": "Chance you have it" }] },
  "check": { "kind": "probability", "value": "10/109", "tol": { "abs": 0.005 },
             "forms": ["fraction", "decimal", "percent"] },
  "misconceptions": [{
    "when": { "kind": "probability", "value": "9/10", "tol": { "abs": 0.005 } },
    "id": "transposed-conditional",
    "line": "That is the chance of a positive if you have it. You need the reverse.",
    "showWhy": { "key": "renormalise" } }]
}
```

### 2.4 Visual roles for this cluster

All tokens are from `prototype/css/tokens.css`. Following the calc-linalg rule, slot 1 (#2A78D6) is skipped in any plot that has a handle, because it sits too close in hue to `--manip` (#2F6BFF); nearly every widget here has a handle, so slot 1 rarely appears.

| Role | Style | Examples |
|---|---|---|
| Learner-controlled | `--manip` handles (20px disc, 2px white ring, 1px ink outline), `--manip-wash` regions, `--manip` 2.5px learner curves and brushes | bracket ends, predictions, split handles, hedge ratio, learner-built regions |
| Theory | `--s3` (aqua), 2.5px lines or stems with 6px heads; fills at 20 to 25% | PMFs and PDFs, exact sampling distributions, posterior, null distribution, stationary distribution |
| Empirical | `--s2` (orange), fills at 35% with a 1px edge; dots | simulation histograms, sample dots, data-derived series, likelihood, residuals of interest |
| Comparison | `--s6` (violet), 2px dashed lines, fills at 20% | approximating distribution, prior, alternative hypothesis, second estimator |
| Third series | `--s4` with a direct label and at least a 2px stroke | third estimator, third forecast method |
| Given data and primary series | ink | data points, price series, observed statistic |
| Truth, exact values, targets | 1.5px dashed ink, 6 on and 4 off, with a label | $\mu$ in a CI ladder, the exact probability line on a trace |
| Signed contributions | positive in `--s3` with a "+" glyph, negative in `--s2` with a "−" glyph | covariance rectangles, Eve's law parts |
| Densities over a plane | `--seq-1` to `--seq-6` | joint PDFs, log-likelihood maps |
| Signed heatmaps | `--div-neg`, `--div-mid`, `--div-pos`, always with + and − glyphs | covariance of indicators |
| Conditioned away, ruled out | `--out` (opacity 0.25 light, 0.3 dark) | cells outside a condition, non-evidence parts of a square |
| $\alpha$ and $\beta$ regions | fill plus pattern: diagonal hatch for $\alpha$ and rejection, dot pattern for $\beta$, cross-hatch for the p-value tail | `test-lab` |
| Chance devices | flat fills, 2px ink outlines, letters on faces | coins show H or T, balls carry a letter as well as a colour |

Grading recolours answer objects only (the chosen card, the learner's region, the placed token, the entered field). Theory, empirical and given marks never change colour on grading. A reveal uses a 2px `--hint` outline so it never reads as success.

### 2.5 Motion and show-why

- **Direct manipulation is never tweened.** Dragged handles and everything derived from them redraw on the same frame.
- **Data arriving is content.** Simulation histograms fill in `requestAnimationFrame` chunks, at most 1.1s per batch, as in the prototype.
- **Consequence animations** play the result of a learner action and only start from one: pouring mass along arrows (`rv-mapper`), renormalising (`prob-square`, `posterior-lab`, `joint-density`), sorting (`icon-array`, `multiple-testing`), collapsing to slice means (`cond-expectation`), reflecting a path (`lattice-walk`), shuffling (`indicator-board`). They run 300 to 600ms with `--ease-morph` and a tap skips to the end.
- **Chance devices** animate (flip, roll, spin, draw) for the first 10 trials of a run only; after that, values arrive in batches.
- **Show-why** uses the declarative recipe in calc-linalg section 2.6: tween non-answer variables, highlight, annotate, 480 to 800ms. Each widget below lists its keys.
- **Reduced motion.** Batches show their final state; consequence animations and show-why become a before-and-after pair with a Play button; chance devices show their value with a 120ms cross-fade; springs land at once.

### 2.6 Accessibility additions

- **Simulations announce once per batch**, never per frame: "1,000 runs. Switched and won 0.668. Exact two thirds."
- **Probabilities are spoken as fractions and decimals**: "one sixth, 0.167".
- **Every chart has a table view.** Distributions list $x$, $P(X = x)$ and $F(x)$; continuous ones list quantiles at 5% steps plus the shaded probability.
- **Dense marks are summarised.** Glyph arrays, path bundles and scatter clouds are described by counts and summary statistics, and their table view holds the counts, not one row per glyph.
- **Graphs** (`node-graph`) offer an adjacency list and a matrix as tables, and arrow-key navigation between nodes by direction.
- **Patterns as well as colour** mark $\alpha$, $\beta$ and conditioned-away regions.
- **Long series** (time series, simulation traces) are described by window summaries; the table view shows 200 rows and offers a CSV download through the `downloads` capability in the Artifact or a Blob link on the web.

### 2.7 Tutor hooks for Brainy Bertie

- **`describe('brief')`** at most 300 characters; **`describe('full')`** at most 1,500 characters. Simulation state always includes the seed, the run count and summary values, and never more than 20 raw values.
- **`secret()`** returns hidden truths: true parameters, exact answers, which hypotheses are really non-null, the optimal policy. The engine includes it only in lesson and explore modes, under an instruction never to reveal it (decision 9). The tutor is off in practice, quiz, homework and exam modes anyway.
- **Element ids** use `kind:name` (`split:a`, `bar:3`, `node:B`, `edge:A-B`, `cell:2,3`). Ids are stable across sessions, so authored hints and Bertie's references use the same names.
- **Suggestion chips** that Bertie may propose for the learner to tap: "Run 1,000 more", "Try $n = 100$", "Condition on $B$", "Show the slice means". Bertie never changes answer state.
- **Computed numbers.** On complex-tier calls the engine may give Bertie three small tools so that any number it quotes is computed, not recalled: `dist_eval(family, params, op, x)`, `exact_solve(equations)` and `enumerate(space, event)` for spaces up to 10,000 outcomes. Results are under 1 KB each, in line with the `sample` advice to keep tools few and results small.

### 2.8 Performance

| Budget | Value |
|---|---|
| Work per pointer frame on the reference phone (state, derived values, redraw) | 8ms for a composite, of which script at most 4ms |
| Main-thread simulation per frame | 4ms; above that the work moves to the shared simulation worker |
| Mount | 100ms, excluding lazy dependencies |
| SVG nodes per screen | 1,500; above that the dense layer moves to Canvas 2D under an SVG layer of focusable handles |
| Canvas thresholds | glyph arrays above 400, scatter above 1,500 points, path bundles above 20 paths, every heatmap |
| Histograms | incremental binning into `Uint32Array` counts; redraw only when counts change, at most once per frame |
| Time series | min-and-max decimation per pixel column; prefix sums so a dragged window's statistics cost $O(1)$ per frame |
| Exact arithmetic | BigInt rational operations cost about a microsecond [unverified]; systems up to 30 unknowns |

The reference phone is the engine blueprint's; the sibling files name a Galaxy A53 or a Pixel 4a class device.

### 2.9 Artifact and web

| Concern | Artifact | Web |
|---|---|---|
| Simulation worker | from a published own file or a `blob:` URL | own file |
| Statistics core | `stats-core.js` published as an own file | vendored, cached by the service worker |
| 1.5 code drills (pure Python simulation with `zq_rng`) | MicroPython if the WebAssembly probe passes [unverified]; otherwise a handoff to the web app | Pyodide |
| 1.6 drills | pure-Python and ulab drills in MicroPython [unverified]; drills needing `scipy.stats` or `statsmodels` hand off | Pyodide with SciPy and statsmodels |
| 2.2 drills | all hand off (they need statsmodels) | Pyodide |
| Exporting simulated data | `downloads` capability | Blob link |
| Learner CSV upload (2.2) | file input; whether the Artifact sandbox allows it is [unverified] | file input |
| Tutor transport | `sample` capability | proxy |

### 2.10 Services this cluster needs (not widgets)

These are requirements on the engine's shared modules, written as acceptance tests. The engine blueprint owns their design.

| Module | Must provide | Accuracy acceptance | Used by |
|---|---|---|---|
| `rational` | BigInt fractions; exact linear solve; $\binom{n}{k}$ and $n!$ up to $n = 1{,}000$; exact sums of products | exact | every discrete widget |
| `special` | log-gamma, digamma, regularised incomplete gamma and beta and their inverses, erf and erfc | against SciPy: absolute error at most $10^{-12}$ on $[10^{-10}, 1 - 10^{-10}]$; relative error at most $10^{-8}$ for tails down to $10^{-15}$ | `dist` |
| `dist` | Bernoulli, binomial, hypergeometric, geometric (both conventions), negative binomial, Poisson, discrete uniform, multinomial, uniform, normal, exponential, gamma, beta, $\chi^2$, Student $t$, $F$, lognormal, Cauchy, Laplace, Pareto, two-component mixtures, and custom PMFs; each with PMF or PDF, CDF, survival function, quantile, mean, variance, skewness, kurtosis, MGF where it exists, and seeded sampling | as `special`; sample moments of $10^6$ seeded draws within 4 standard errors | most widgets |
| `rng` | the engine generator (sfc32 or the counter-based proposal) plus normals, gammas (Marsaglia-Tsang), betas, Poisson, binomial, hypergeometric, permutations (Fisher-Yates), multivariate normal (Cholesky); a portable Python port `zq_rng` | Python port reproduces the integer stream bit for bit; continuous values to $10^{-12}$ relative | `sim-runner`, generators, drills |
| `tests` | $z$, one-sample, Welch and paired $t$, $\chi^2$ goodness of fit and independence, $F$, exact binomial, Jarque-Bera, D'Agostino $K^2$ omnibus, Durbin-Watson, Ljung-Box, ADF with AIC lag selection and MacKinnon p-values, KPSS with statsmodels' table p-values, Engle-Granger cointegration with MacKinnon (2010) critical values, Bonferroni, Holm and Benjamini-Hochberg | statistics to $10^{-8}$ relative and p-values to $10^{-6}$ absolute against statsmodels and SciPy fixtures | `test-lab`, `summary-table`, `acf-lab`, `coint-lab`, `multiple-testing` |
| `ols` | QR-based fit; coefficients, standard errors, $t$, p, intervals, $R^2$, adjusted $R^2$, $F$, log-likelihood, AIC, BIC, HC0 to HC3 covariances, hat values, Cook's distance, the condition number as statsmodels reports it | every field of the summary to its printed precision, and to $10^{-9}$ relative internally, on 30 fixture data sets | `regression-lab`, `summary-table`, `coint-lab` |
| `ts` | sample ACF and PACF (the method statsmodels uses by default, [unverified] which it is in the pinned version), theoretical ARMA ACF and PACF, ARMA simulation with supplied shocks, ARMA fit by exact Gaussian likelihood (innovations algorithm, Nelder-Mead from a Hannan-Rissanen start) for $p, q \le 3$, GARCH(1,1) filter and likelihood, EWMA, classical decomposition, simple exponential smoothing, forecasts with intervals | ACF and PACF to $10^{-10}$; ARMA parameters within 0.002 absolute of statsmodels ARIMA on fixtures [our choice, to be confirmed] | `acf-lab`, `arma-lab`, `forecast-lab`, `garch-lab` |
| `geom` | half-plane arrangement of up to 10 lines in a box, exact polygon areas, Sutherland-Hodgman clipping, symmetric-difference areas | exact to $10^{-12}$ | `geo-prob` |
| `expr` additions | functions `binom`, `fact`, `perm`, `gamma`, `lgamma`, `beta`, `Phi`, `Phiinv`, `phi`, `erf`, `tcdf`, `tinv`, `chi2cdf`, `chi2inv`, indicator `ind(cond)`, `sum` and `prod` over integer ranges | as `dist` | widgets whose configs carry formulas |

**Fixture pipeline.** A CI job runs CPython with SciPy and statsmodels pinned to the versions the Pyodide release ships [unverified which versions], writes golden JSON fixtures, and fails the JavaScript tests on any mismatch. The same fixtures feed the Artifact's precomputed statsmodels values (decision 10).

---

## 3. New primitives

Each is cluster-neutral and is proposed for the engine's primitive set. All three are P0, wave D0.

### 3.1 `mass-editor`: Mass editor

**Primitive (handle) · P0 · D0.** Edit a list of non-negative masses that must sum to a fixed total, usually 1.

- **Purpose.** Build and reshape PMFs, priors, Markov transition rows, spinner sectors and mixture weights by hand, with the sum constraint made visible rather than enforced by an error message.
- **Serves.** 1.5.1 L10; 1.5.3 L2, L8, L15; 1.5.7 L1; 1.5.8 L1 to L6; 1.6.6 L1. Hosts: `rv-mapper`, `dist-explorer`, `markov-chain`, `venn-diagram` (probability mode), `contingency-table`, `posterior-lab`, `galton-board` (prediction).
- **Uses.** `plot-axes` and `marks` (bars), `draggable-point` (bar tops and dividers, axis-constrained).
- **Layouts.**
  - `bars`: one vertical bar per support value, each with a top handle.
  - `stack`: one 100% bar split by draggable dividers; moving a divider trades mass between its two neighbours only, so the total never changes.
  - `spinner`: a circle split into sectors by draggable boundaries; the same trading rule.
- **Constraint policies** for `bars`:
  - `free`: bars move independently; a total readout shows the shortfall or excess, and a Normalise button rescales all bars. Use it when making the PMF valid is the task.
  - `pool`: a hatched grey "unassigned" bar holds the slack; no bar can take more than the pool holds.
  - `proportional`: dragging one bar rescales the others in proportion, so the total stays fixed.
- **Interactions.**
  - Pointer: drag a bar's top handle or a divider; tap a bar's value label to type an exact value; tap Normalise.
  - Keyboard: each bar or divider is a slider; arrows step one unit; Shift + arrow steps ten; Home sets 0; E opens the exact editor (accepts `5/36`); N normalises.
- **State.** `{ units: number[]; denom: number }` when the step is rational, so masses are stored as integers over a common denominator and never drift; `{ masses: number[] }` when the step is continuous.
- **Answers.** `distribution`; `numeric` (one mass); `state` (predicate `valid-pmf`).
- **Config.**

```ts
interface MassEditorConfig {
  id: string;
  support: { id: string; label: string; tex?: string; x?: number }[];
  masses: Entry[];                         // initial masses
  total?: Entry;                           // default 1
  layout: 'bars' | 'stack' | 'spinner';
  policy?: 'free' | 'pool' | 'proportional';    // bars only
  step?: Entry;                            // e.g. '1/36', 0.01; rational steps store exactly
  locked?: string[];                       // support ids that cannot change
  show?: { values: 'fraction' | 'decimal' | 'percent' | 'none'; total: boolean };
  role: 'answer' | 'control';
}
```

- **Visual.**
  - Bars: `--manip-wash` fill, a 24 × 6 px `--manip` pill handle on top with a 44px hit area, value labels above in the caption token with tabular figures.
  - The pool bar: `--bg-sunken` with a 45° hatch in `--text-muted`, labelled "unassigned".
  - The total readout reads "Total $\frac{35}{36}$, needs 1" in `--text-2` with an info icon. It does not turn amber: grading colours are reserved for Check.
  - Stack and spinner dividers are `--manip` handles on the boundary lines; sectors take series slots in order with direct labels.
- **Motion.** Dragging is direct; in `proportional` the other bars redraw on the same frame. Normalise is a consequence animation, 300ms `--ease-standard`. Snap on release with `--spring-snap`.
- **Reduced motion.** Normalise and snaps are instant.
- **Accessibility.** A group named by the host ("Distribution of X, total 1"). Each bar is a slider with `aria-valuetext` such as "P of X equals 3: five thirty-sixths". The total is announced on commit.
- **Tutor hooks.** Describe: "Masses on 0..4: 1/16, 4/16, 6/16, 4/16, 0; total 15/16 (needs 1)." Ids: `mass:<id>`, `divider:<i>`, `total`, `normalise`.
- **Performance.** SVG up to 60 bars; a drag updates at most 60 rects per frame, well under 1ms.
- **Artifact and web.** No difference.
- **Generators.** None of its own; hosts generate.
- **Cross-cluster.** Portfolio weights (1.7, 2.3), class probabilities (2.1), bet allocation (3.3).

### 3.2 `node-graph`: Node graph

**Primitive (host) · P0 · D0.** Nodes and edges, directed or not, with weights, labels, values and moving tokens.

- **Purpose.** Draw and edit state diagrams and mappings: Markov chains, first-step analysis, pattern automata, random walks on graphs, PageRank, and the bipartite outcome-to-value map of a random variable.
- **Serves.** 1.5.2 L14; 1.5.3 L1, L13; 1.5.6 L7; 1.5.8 all; 1.5.9 L4. Hosts: `markov-chain`, `first-step-solver`, `rv-mapper`.
- **Uses.** `marks` (labels), `mass-editor` (outgoing weights popover), `numeric-entry` (single weights).
- **Layouts.** `given` coordinates; `circle`; `layered` (left to right, for automata and absorbing chains); `bipartite` (two columns); `grid`; `force-once`, a deterministic seeded force layout computed once at mount and never animated, so the diagram does not jitter.
- **Interactions.**
  - Pointer: tap a node or edge to select it; drag a node to rearrange (layout only, never answer state); drag from a node's edge handle to another node to add an edge when editing is on; tap an edge label to edit its weight; tap a node with `weights: 'mass-editor'` to open its outgoing-row editor.
  - Keyboard: Tab enters the graph; arrows move focus to the nearest node in that direction; Enter selects; E edits the focused node's outgoing weights; A starts add-edge mode (arrows choose the target, Enter confirms); Delete removes a learner-added edge; L reads the adjacency list.
- **State.** `{ positions: Record<Id, Vec2>; selected: Id[]; edges?: { from: Id; to: Id; w: Entry }[]; walkers?: { id: Id; at: Id; t: number }[] }`.
- **Answers.** `set` (nodes or edges), `state` (structure and weights), `mapping` (bipartite edges).
- **Config.**

```ts
interface NodeGraphConfig {
  id: string;
  nodes: { id: string; label: string; tex?: string; x?: number; y?: number;
           kind?: 'state' | 'absorbing' | 'start' }[];
  edges: { from: string; to: string; w?: Entry; label?: string; editable?: boolean }[];
  directed: boolean;
  layout: 'given' | 'circle' | 'layered' | 'bipartite' | 'grid' | 'force-once';
  nodeValues?: { values: Record<string, number>; show: 'fill' | 'bar' | 'label' | 'all' };
  editable?: { addEdges?: boolean; weights?: 'none' | 'field' | 'mass-editor' };
  walkers?: { count: number; display: 'tokens' | 'counts' };
  selectable?: 'nodes' | 'edges' | 'both' | 'none';
}
```

- **Visual.**
  - Nodes are 44px circles with a 2px ink outline on `--bg-surface`, or filled from `--seq-1` to `--seq-6` by value with ink or white labels chosen for contrast. Absorbing nodes have a double outline; the start node has a short ink arrow into it.
  - Edges are 1.5px ink with 8px arrowheads. A pair of opposite edges curves apart; self-loops sit outside the node, away from the graph's centre.
  - Edge labels are KaTeX in the caption size on a `--bg-surface` pill, so they stay legible over lines.
  - Selected nodes and edges are 3px `--manip`; learner-added edges are `--manip` until graded.
  - Walkers are 10px `--s2` discs with an ink outline.
- **Motion.** Walkers move along their edge in 240ms `--ease-standard` (a demonstration started by Step or Play). Node fills step over 320ms on Step. Node drags are direct.
- **Reduced motion.** Walkers jump; fills change at once.
- **Accessibility.** `role="group"` with `aria-roledescription="state diagram"`. Each node is a button named in full: "State B, probability 0.30, goes to A with one half, to C with one half". Table views: the adjacency list and the weight matrix. Walker moves are announced on Step, not during Play.
- **Tutor hooks.** Describe: "Directed graph, 3 nodes. A→A 1/2, A→B 1/2, B→C 1, C→A 1. Walker at B." Ids: `node:<id>`, `edge:<from>-<to>`, `walker:<i>`.
- **Performance.** SVG up to 30 nodes and 120 edges; edge routing recomputed only when the layout changes. Up to 50 walker tokens drawn; above that, `counts` mode shows counts on nodes.
- **Artifact and web.** No difference.
- **Generators.** None of its own.
- **Cross-cluster.** 1.8 graph algorithms (BFS, DFS, Dijkstra, topological sort), 1.2 Git commit graphs, 2.1 computation graphs (calc-linalg's `dependency-graph` could sit on it).

### 3.3 `chance-object`: Chance devices

**Primitive (display and light input) · P0 · D0.** Code-drawn coins, dice, cards, spinners, urns, doors, envelopes and hats.

- **Purpose.** Show the physical story behind a random experiment, and let the learner act on it: flip, roll, draw a ball, open a door, pick an envelope.
- **Serves.** `trial-simulator` (rebuilt), `game-lab`, `indicator-board`, `trial-strip`, `sampling-lab` (bootstrap draws), `posterior-lab` (coin flips), `galton-board` balls.
- **Uses.** None.
- **Kinds.** `coin`; `die` (4, 6, 8, 10, 12 and 20 sides; 6 uses pips, others numerals); `card` (rank and suit, or a back); `spinner` (sectors with given probabilities); `urn` (up to 60 balls in up to 3 colours); `door` (closed, open with prize, open empty); `envelope` (amount hidden or shown); `hat` (owner letter).
- **Interactions.**
  - Pointer: when `interactive` is `tap`, tap selects (choose a door or a card); when `draw`, drag a ball out of the urn, or tap the urn to draw one.
  - Keyboard: interactive objects are buttons; Space or Enter activates.
- **State.** `{ value: unknown; faceUp: boolean; selected: boolean }`. Values come from the host's seeded stream; the object never draws its own randomness.
- **Answers.** `choice` (the selected object), through the host.
- **Config.**

```ts
interface ChanceObjectConfig {
  id: string;
  kind: 'coin' | 'die' | 'card' | 'spinner' | 'urn' | 'door' | 'envelope' | 'hat';
  sides?: 4 | 6 | 8 | 10 | 12 | 20;
  sectors?: { label: string; p: Entry }[];
  balls?: { colour: 1 | 2 | 3; letter: string; count: number }[];
  value?: unknown;                 // set by the host
  interactive?: 'none' | 'tap' | 'draw';
  size?: 'sm' | 'md' | 'lg';       // 24, 48, 96px
  label?: string;
}
```

- **Visual.** Flat fills from the neutral and series ramps, 2px ink outlines and rounded corners, in the code-drawn style of design research section 3. Coins show a letter, H or T. Dice show ink pips. Card suits use their glyphs, with red suits in `--prob-deep` and black in ink, so the glyph carries the suit. Urn balls use slots 2, 3 and 6 and carry a letter (R, B, G), so colour is never the only cue. Doors are numbered.
- **Motion.** Flip: two horizontal squashes, 300ms. Roll: four seeded intermediate faces at 60ms, landing on `--spring-snap`. Spin: rotate to the final angle with `--ease-exit` reversed (fast start, slow end), 600ms. Draw: the ball rises and moves to the tally, 300ms. Only the first 10 trials of a run animate.
- **Reduced motion.** The value appears with a 120ms cross-fade.
- **Accessibility.** Non-interactive objects are `role="img"` ("Die showing 5"). Interactive ones are buttons ("Door 2, closed"). The host announces results.
- **Tutor hooks.** Describe: "Urn: 3 red, 2 blue. Drawn without replacement: R, B." Ids: `coin:<i>`, `die:<i>`, `card:<i>`, `door:<i>`, `ball:<i>`, `urn`.
- **Performance.** SVG, one group per object; at most 60 objects drawn, beyond which hosts show counts.
- **Artifact and web.** No difference.
- **Generators.** None.
- **Cross-cluster.** GCSE probability (Stage 0 `trial-simulator`), 3.3 betting and market-making games with cards.

---

## 4. Additions to shared primitives

These primitives are specified in the sibling catalogues. This cluster needs the additions below; without them the named lessons cannot be built.

### 4.1 `marks`: new mark types

| Type | Draws | Notes | First needed |
|---|---|---|---|
| `stems` | PMF lollipops: a vertical line from 0 to $p_x$ with a 6px head | One SVG path for all stems above 60 support points | 1.5.3 L2 |
| `step` | Right-continuous step function | Filled dot at the top of each jump, hollow dot at the bottom; horizontal runs 2.5px | 1.5.3 L3 |
| `hist` | Histogram bound to a counts buffer | Edges fixed at creation; reads a `Uint32Array` stream from `sim-runner`; `scale: 'count' \| 'proportion' \| 'density'` | 1.5.4 L1 |
| `glyphs` | A grid of up to 10,000 small glyphs (person, square, dot) with per-glyph fill, marker and opacity | Canvas; SVG overlay only for group outlines and focus | 1.5.2 L5 |
| `intervals` | Horizontal interval segments with centre dots, stacked as a ladder | Per-interval style (covering or missing) | 1.6.3 L1 |
| `rug` | Small ticks along an axis for raw data | | 1.5.4 L1 |
| `fan` | Nested quantile bands around a central path | 80% band at 30% and 95% band at 15% opacity of the series colour | 2.2.3 L7 |
| `rect-signed` | Rectangles from a centre to each point, signed | + and − glyphs in a corner | 1.5.5 L6 |
| `connector` | A line from an element in one host to an element in another | Used for outcome-to-value arrows when two hosts sit side by side | 1.5.3 L1 |
| fill patterns | `hatch-diagonal`, `hatch-dots`, `hatch-cross` on any filled mark | SVG `<pattern>` in light and dark variants | 1.5.2 L2, 1.6.4 L1 |

### 4.2 Other primitives

| Primitive | Addition | First needed |
|---|---|---|
| `plot-axes` | Stacked panels sharing one $x$ axis (`link: { group, axis: 'x' }`), including a sideways panel for marginal histograms | 1.5.4 L1 (`sampling-lab`), 1.5.5 L2 (`joint-density`) |
| `plot-axes` | Time axis with date or trading-day ticks | 2.2.1 L1 (P2) |
| `number-line` | Dual-labelled scale: log-odds positions with probability ticks below (0.01, 0.1, 0.5, 0.9, 0.99) | 1.5.2 L8 (`odds-ledger`) |
| `region-selector` | Bracket mode on a time axis with two independent brushes (A and B) | 2.2.1 L3 |
| `region-selector` | Half-plane arrangement cells with exact areas from `geom` | 1.5.9 L7 (`geo-prob`) |
| `slider` | Discrete value lists such as $n \in \{1, 2, 5, 10, 30, 100, 1000\}$; a hidden-value mode whose label reads "hidden" in quiz mode | 1.5.7 L8 |
| `numeric-entry` | Probability forms (fraction, decimal, percent; odds $a:b$ where asked) and the $[0, 1]$ parse nudge (section 2.1) | 1.5.1 L2 |
| `expression-entry` | A probability keyboard layer: $P(\cdot \mid \cdot)$, $E[\cdot]$, $\mathrm{Var}$, $\binom{n}{k}$, $!$, $\Sigma$, and the variables $p, q, n, k, \lambda, \mu, \sigma, \rho, \theta, \alpha, \beta, \varphi$ | 1.5.1 L4 |
| `sim-runner` | Models for this cluster: `bernoulli-seq`, `urn`, `permutation`, `birthday`, `coupon`, `pattern`, `poisson-process`, `galton`, `sample-statistic` (population, $n$, statistic), `bootstrap`, `permutation-test`, `ci`, `policy` (game-lab), `markov-walk`, `lattice-walk`, `arma`, `garch`, `pair`; streams of statistics into `hist` marks; up to $10^7$ draws per run in the worker; pauses when the tab is hidden | 1.5.1 L9 |
| `data-table` | Margins computed from cells; a conditional view (row or column normalised); CSV export through the platform adapter | 1.5.5 L1 |
| `matrix` | Row-stochastic editing: a row's cells edit through a `mass-editor` popover so the row always sums to 1 | 1.5.8 L1 |
| `token-tray` | Term chips that carry a coefficient and a variable (`first-step-solver`); evidence cards that carry a likelihood ratio (`odds-ledger`) | 1.5.2 L8 |
| `sketch-pad` | Step-function features for sketching CDFs: `jump` (at $x$, of height $h$) and `flat` (on an interval) | 1.5.3 L3 |
| `choice-cards` | Options holding a read-only mini plot (also requested by calc-linalg): match a correlogram, pick the residual plot that shows a fan | 1.5.4 L12 |
| `code-cell` | Python helpers for this cluster: `zq_rng` (section 2.2), `assert_mc_close(value, exact, se, k=4)`, `assert_tv_close(p, q, tol)`, `assert_fixture(name, values, rtol)` against CI-generated statsmodels fixtures; data passed as literals or CSV | 1.5.1 L9 (P0); fixtures at 1.6.5 L16 (P1) |

---

## 5. Extensions to widgets owned by the sibling catalogues

Each row is a mode or change this cluster needs from a widget specified elsewhere. The owning catalogue keeps the full spec; the more demanding configuration wins, as the Stage 0 file already says for its probability composites.

| Widget (owner) | What this cluster needs | Priority, wave | Lessons |
|---|---|---|---|
| `outcome-grid` (Stage 0) | Non-uniform cell weights; event chips defined by `expr` predicates over row and column with $\cup$, $\cap$, complement and difference; a random-variable display (each cell shows $X(\omega)$, coloured by value, linked to `rv-mapper`); a list layout for 1D and three-stage spaces up to 64 outcomes; a layered mode for three dice (216 outcomes, one $6 \times 6$ layer per value of the third die, chosen by a slider); renormalised cell labels under a condition; row-proportion bars for independence | P0, D1 | 1.5.1 L1, L2; 1.5.2 L1, L10, L11; 1.5.3 L7 |
| `tree-diagram` (Stage 0) | `flip` mode: build the reversed tree; leaves keep their ids and joint probabilities, with link lines showing which leaf is which; natural-frequency labels (1,000, then 10, then 9); depth 4 with collapse; loop leaves marked "back to start" that hand over to `first-step-solver`; tap the leaves of $B$, then of $A \cap B$, to form a ratio | P0, D1 | 1.5.2 L3, L4, L7, L13 |
| `trial-simulator` (Stage 0) | Rebuilt on `sim-runner` and `chance-object`; experiment kinds `urn` (with replacement, without, and Pólya with $+c$ balls), `permutation` (fixed points, cycles), `birthday`, `coupon`, `pattern`; displays: proportion trace with a $\pm 2$ standard-error funnel, the count-deviation trace $\lvert S_n - np \rvert$, and a histogram of a numeric per-trial outcome; $10^6$ trials in the worker; Pólya's limiting proportion histogram against its Beta density | P0, D1 | 1.5.1 L9, L12, L13; 1.5.3 L5; 1.5.7 L5, L6 |
| `counting-slots` (Stage 0) | Procedure comparison: two procedures enumerate the same set side by side with linked rows, for story proofs; multinomial mode; a probability toggle in stars-and-bars mode showing each configuration's real probability under ball-by-ball placement | P0, D1 | 1.5.1 L4 to L8 |
| `venn-diagram` (Stage 0) | Probability mode: atom masses edited through `mass-editor`; non-negative atoms enforced; an inclusion-exclusion term builder linked to the formula, for 2 and 3 sets | P0, D1 | 1.5.1 L10, L11 |
| `pascal-triangle` (Stage 0) | Row-to-PMF view: row $n$ divided by $2^n$, or weighted entries $\binom{n}{k}p^k q^{n-k}$; peg links to `galton-board`; Catalan highlight shared with `lattice-walk` | P0, D2 | 1.5.3 L4; 1.5.9 L1, L3 |
| `binomial-expander` (Stage 0) | Probability mode: the terms of $(p + q)^n$ are binomial probabilities | P0, D2 | 1.5.3 L4 |
| `graph-explorer` (Stage 0) | Integer-domain functions drawn as stems (birthday curve) | P0, D1 | 1.5.1 L9 |
| `iteration-cobweb` (Stage 0) | Cobweb for $s \mapsto G(s)$ on $[0, 1]$, hosted by `generating-function` | P0, D3 | 1.5.4 L13 |
| `stat-chart` (Stage 0) | Histogram with a bin-width slider and density scaling | P0, D3 | 1.5.4 L1 |
| `dot-plot-stats` (Stage 0) | A movable centre $c$ with a sum-of-squares readout (minimum at $\bar x$); divisor chips $n - 1$, $n$, $n + 1$ | P1, E | 1.6.1 L4 |
| `scatter-fit` (Stage 0) | $R^2$ and residual plot (already flagged P1 there) | P1, E | 1.6.5 L1 |
| `complex-plane` (Stage 0) | Roots of an AR or MA characteristic polynomial against the unit circle | P2, F | 2.2.3 L3, L4 |
| `function-mapping` (calc-linalg) | Density mode: an interval $[x, x + dx]$ maps to its image; mass is conserved, so bar heights rescale by $1/\lvert g'(x) \rvert$; non-monotone $g$ sums the branches | P0, D3 | 1.5.4 L14 |
| `accumulator` (calc-linalg) | PDF-to-CDF mode using the `dist` service, matching `dist-explorer` | P0, D3 | 1.5.4 L2 |
| `region-bounds` (calc-linalg) | A joint density as the integrand over a chosen region | P0, D3 | 1.5.5 L5 |
| `convexity-chord` (calc-linalg) | Random-variable mode: $X$ takes two (or three) values; a handle on the chord sits at $E[X]$; the Jensen gap is labelled | P0, D3 | 1.5.7 L3 |
| `taylor-builder` (calc-linalg) | MGF series (coefficients are $E[X^k]/k!$) at P0; delta-method mode at P1 | P0, D3; P1, E | 1.5.4 L11; 1.5.7 L11; 1.6.2 L7 |
| `quadratic-form` (calc-linalg) | Covariance ellipses and Mahalanobis distance at P0; coefficient confidence ellipse at P1 | P0, D3; P1, E | 1.5.5 L10; 1.6.5 L11 |
| `transform-grid` (calc-linalg) | Cholesky ($Z \mapsto LZ$) and Box-Muller polar presets | P0, D3 | 1.5.5 L11, L13 |
| `filtration-tree` (calc-linalg) | Promote the conditional-expectation and tower modes from P2 to P0 | P0, D3 | 1.5.6 L3; 1.5.9 L14 |
| `linear-dynamics` (calc-linalg) | Markov mode linked from `markov-chain` | P0, D4 | 1.5.8 L4 |
| `eigen-finder` (calc-linalg) | Left eigenvector for $\lambda = 1$ as the stationary distribution | P0, D4 | 1.5.8 L4 |
| `matrix-multiply` (calc-linalg) | Two-step transition entries shown as sums over intermediate states | P0, D4 | 1.5.8 L2 |
| `path-simulator` (calc-linalg) | Walk and barrier modes are already P0; add drift $p \ne \frac{1}{2}$ with the ruin formula, a running-maximum histogram, and a link to `lattice-walk` | P0, D4 | 1.5.2 L14; 1.5.9 L4 to L6 |
| `least-squares-fit` (calc-linalg) | Linked from `regression-lab`; already declared shared with 1.6 | P1, E | 1.6.5 L1, L2 |
| `surface-explorer` (calc-linalg) | Log-likelihood surfaces over two parameters | P1, E | 1.6.2 L5 |
| `sde-stepper` (calc-linalg) | Ornstein-Uhlenbeck spread with its half-life; already declared for 2.2 | P2, F | 2.2.5 L4 |
| `card-sort` (Stage 0) | Bins for the four sampling schemes (P0); match mode with mini-plot cards for correlograms and residual plots | P0, D1; P1, E; P2, F | 1.5.1 L4; 1.6.5 L8; 2.2.3 L5 |
| `derivation` (Stage 0) | Probability notation lines; no other change | P0, D1 | throughout |
| `free-response` (Stage 0) | Explanation items with rubrics, including both exit-test explanations | P1, E; P2, F | 1.6.5 L16; 2.2.5 L6 |

**Three extensions carry most of the weight** and get a short spec here.

- **`trial-simulator` on `sim-runner`.** State becomes `{ seed, runs, counts, trace }` held by the runner, with the composite keeping only display choices. The `predictFirst` gate stays. The count-deviation trace is the gambler's-fallacy Trap: $S_n/n$ settles while $\lvert S_n - n/2 \rvert$ wanders upward like $\sqrt{n}$. Show-why `funnel` draws the $\pm 2\sqrt{p(1-p)/n}$ envelope over 600ms. Tutor describe adds the funnel width at the current $n$.
- **`tree-diagram` flip.** The learner builds the second tree; Check passes when every reversed branch probability equals the exact conditional (exact rational check per branch through `multi`). Show-why `flip` moves each leaf from its old position to its new one over 600ms, keeping its label, so the learner sees that the joint probabilities did not change; only the order of splitting did.
- **`outcome-grid` random-variable display.** Each cell shows $X(\omega)$; cells sharing a value share a slot colour and a value label (never colour alone). Tapping a value in the legend highlights its preimage. This is the bridge from 1.5.2 to `rv-mapper`.

---

## 6. Probability composites (1.5)

All 22 are P0. Fields that follow the shared contract unchanged are stated briefly.

### 6.1 Events, conditioning and Bayes

#### 6.1.1 `prob-square`: Probability square

**Composite · P0 · D1.** Probability as area in a unit square: two events, partitions, conditioning and Bayes' rule.

- **Purpose.** Make $P(A \cap B) = P(A)\,P(B \mid A)$ a rectangle the learner can resize. Column widths are $P(A)$ and $P(A^c)$ (or the priors of a partition); the shaded height inside each column is the conditional probability of $B$. Independence is visible as one straight split line across all columns; conditioning is visible as the surviving pieces stretching to fill the square.
- **Modes.**
  - `events`: one vertical split for $A$; one horizontal split inside each column for $B \mid A$ and $B \mid A^c$.
  - `condition`: tap a region (or a chip) to condition on it; everything else dims; Renormalise stretches what remains.
  - `bayes`: 2 to 5 hypothesis columns (widths are priors, edited as a `mass-editor` stack); one evidence height per column (the likelihood); Observe removes the non-evidence parts; Renormalise gives posterior widths. An evidence sequence makes the posterior the next prior.
  - `partition`: $k$ columns; a dashed level line at the width-weighted mean height is $P(B)$ (law of total probability).
  - `nested`: inside each column, a second event split perpendicular to the first, so two tests are independent given the column (conditional independence) while their aggregate is not.
- **Serves.** 1.5.1 L10; 1.5.2 L2, L3, L4, L5, L9, L10, L12, L17.
- **Uses.** `plot-axes` (unit square, equal aspect), `draggable-point` (split handles, axis-constrained), `mass-editor` (stack layout for priors), `region-selector` (shapes mode for the rectangles), `marks` (rectangles, braces, labels, hatch patterns), `tex-terms` (live $P(A \cap B) = P(A)P(B \mid A)$ with numbers), `stepper` (evidence sequence).
- **Interactions.**
  - Pointer: drag the column divider on the top edge; drag each height handle at its column's centre; tap a rectangle to select it (for "shade the event" tasks); tap Condition on a region chip; tap Observe and Renormalise in `bayes`.
  - Keyboard: every handle is a slider (arrows step by the snap, Shift ten steps, E types an exact value); Tab moves through handles, then regions; Space selects a region; C conditions on the focused region; R renormalises.
- **State.** `{ widths: Entry[]; heights: Entry[]; nested?: Entry[]; selected: Id[]; conditionedOn: Id | null; stage: 'prior' | 'observed' | 'posterior'; step: number }`.
- **Answers and checks.** `numeric` and `probability` (any area or ratio); `set` (the regions that make up an event); `state` with predicates `independent-events`, `disjoint-events`, or target widths and heights within the snap.
- **Config.**

```ts
interface ProbSquareConfig {
  mode: 'events' | 'condition' | 'bayes' | 'partition' | 'nested';
  labels: { A?: string; B?: string; C?: string; hyps?: string[]; evidence?: string };
  init: { widths?: Entry[]; heights?: Entry[]; nested?: Entry[]; priors?: Entry[]; likelihoods?: Entry[] };
  editable: ('widths' | 'heights' | 'nested' | 'priors' | 'likelihoods')[];
  snap?: Entry;                                   // e.g. '1/20', 0.01
  show: { areas: 'none' | 'fraction' | 'decimal' | 'percent'; formula: boolean; braces: boolean };
  evidenceSequence?: { label: string; likelihoods: Entry[] }[];
  task?: 'shade' | 'compute' | 'make-independent' | 'make-disjoint' | 'posterior';
}
```

- **Visual.** The square is 2px ink, at most 320px on mobile. Column dividers are 1.5px ink. $B$'s parts are `--s2` at 25% with a diagonal hatch; selected regions `--manip-wash` with a 2px `--manip` edge. Braces above the columns carry widths; in `bayes` the prior braces are `--s6`, likelihood labels `--s2`, posterior braces `--s3` (the Bayes colour triple used across the cluster). Conditioned-away parts take `--out`. The formula line below uses `tex-terms` with terms tinted to match.
- **Motion.** Drags are direct. Renormalise is a consequence animation: surviving rectangles slide together and stretch to fill the square, 600ms `--ease-morph`. Show-why keys: `renormalise`; `aligned-splits` (a dashed ink line runs across the columns to show independence or its absence, 480ms); `transposed` (highlights the two different denominators of $P(A \mid B)$ and $P(B \mid A)$ in turn); `double-count` (flashes the overlap twice at 150ms).
- **Reduced motion.** Renormalise and show-why become before-and-after with Play; flashes become a static highlight.
- **Accessibility.** Rectangles are buttons named with their event and area ("A and B, 0.12"). Handles are sliders ("Probability of B given A, 0.40"). Table view: the joint $2 \times 2$ (or $k \times 2$) table with margins, read-only `contingency-table`. Areas are announced on commit.
- **Tutor hooks.** Describe: "Square: P(A) = 0.30; P(B|A) = 0.40, P(B|not A) = 0.40 (splits aligned). Conditioned on: none." Ids: `split:a`, `split:b|a`, `split:b|not-a`, `region:a-b`, `region:a-notb`, `region:nota-b`, `region:nota-notb`, `col:<i>`, `prior:<i>`, `lik:<i>`, `formula`. Secret: target posterior and the exact areas the task asks for.
- **Performance.** SVG under 60 nodes; a drag updates at most 10 rectangles per frame.
- **Artifact and web.** No difference.
- **Generators.** Two-event tables with denominators of 20 or less; Bayes items built from priors in $\{\frac{1}{100}, \frac{1}{50}, \frac{1}{20}, \frac{1}{10}, \frac{1}{4}\}$ and likelihoods in tenths and hundredths, accepted only when the posterior denominator is 200 or less; independence and disjointness construction tasks.
- **Misconceptions.** `transposed-conditional`, `independent-means-disjoint`, `base-rate-neglect`, `lotp-unweighted-average`, `conditioning-keeps-denominator`.

#### 6.1.2 `icon-array`: Natural-frequency icon array

**Composite · P0 · D1 (FDR mode P1, E).** A population of 100, 1,000 or 10,000 glyphs, marked by attributes, filtered and sorted.

- **Purpose.** Natural frequencies make conditional probability countable: "Of 1,000 people, 10 have it; 9 of those test positive; 89 of the 990 without it also test positive." The learner filters to positives and counts. Also carries the prosecutor's fallacy, Simpson's paradox, and in 1.6 the false-discovery picture (1,000 studies, a share with real effects).
- **Modes.** `bayes` (base rate, sensitivity, specificity), `fallacy` (match probability against population size), `simpson` (two strata), `fdr` (P1: share of true effects, power, $\alpha$), `repeat-test` (second test on the positives).
- **Serves.** 1.5.2 L5, L6, L12, L15, L16; 1.6.4 L3.
- **Uses.** `marks` (`glyphs`, block outlines, labels), `slider` (rates), `region-selector` (filter chips, block selection), `contingency-table` (linked counts), `tex-terms`.
- **Interactions.**
  - Pointer: rate sliders; filter chips ("Has it", "Tests positive", their complements); Sort arranges glyphs into labelled blocks; tap a block to select it.
  - Keyboard: chips are toggle buttons; sliders are native; blocks are focusable groups (never individual glyphs); S sorts.
- **State.** `{ rates: Record<string, Entry>; filter: string[]; sorted: boolean; selectedBlocks: Id[] }`.
- **Answers and checks.** `numeric` (a count or a proportion), `probability`, `set` (blocks), `choice`.
- **Config.**

```ts
interface IconArrayConfig {
  n: 100 | 1000 | 10000;
  mode: 'bayes' | 'fallacy' | 'simpson' | 'fdr' | 'repeat-test';
  attributes: { id: string; label: string; rate?: Entry;
                given?: { attr: string; rateIf: Entry; rateIfNot: Entry } }[];
  editable?: string[];                  // which rates have sliders
  glyph?: 'person' | 'square' | 'dot';  // 'square' is forced at n = 10000
  layout?: 'scattered' | 'blocks';      // 'scattered' uses the item seed for positions
  strata?: { label: string; n: number; rates: Record<string, Entry> }[];
}
```

- **Visual.** First attribute: glyph filled `--s2`, otherwise outlined. Second attribute: a small ink plus or minus marker, or a hatch at $n = 10{,}000$. Filtered-out glyphs take `--out`. Blocks have 1.5px ink outlines with count labels ("9 of 98"). Colour is never alone: fill and marker shape both carry meaning.
- **Motion.** Sort is a consequence animation: glyphs travel to block positions over 480ms with a column stagger of 10ms. Filter dims over 200ms.
- **Reduced motion.** Instant.
- **Accessibility.** Group named "1,000 people"; the table view is the $2 \times 2$ count table; the filter result is announced ("Showing 98 people who test positive; 9 have the condition").
- **Tutor hooks.** Describe: "1,000 people: 10 with condition, 9 of them positive; 89 of 990 without it positive. Filter: positive (98 shown). Sorted: yes." Ids: `block:<attr-combination>` (such as `block:cond-pos`), `chip:<filter>`, `slider:<rate>`. Secret: the requested count.
- **Performance.** Canvas for glyphs; at $n = 1{,}000$ a redraw takes under 2ms on the reference phone [unverified]; at $n = 10{,}000$ squares of 4px. SVG only for block outlines and focus.
- **Artifact and web.** No difference.
- **Generators.** Screening scenarios with integer counts by construction ($n$ and rates chosen so every cell is whole); fallacy items; Simpson items (shared generator with `contingency-table`); FDR items (P1).
- **Misconceptions.** `base-rate-neglect`, `sensitivity-is-ppv`, `prosecutors-fallacy`, `p-value-is-p-null` (P1).

#### 6.1.3 `contingency-table`: Two-way table

**Composite · P0 · D1 (expected counts P1, E).** Counts or probabilities in a two-way table with margins, conditioning, strata and expected counts.

- **Purpose.** Joint, marginal and conditional distributions of two categorical variables; independence as "every row has the same shape"; Simpson's paradox as strata that disagree with their sum; in 1.6, expected counts and $\chi^2$ contributions; in 2.1 (cross-cluster), confusion matrices; in 1.6.4, the truth-against-decision table of multiple testing.
- **Serves.** 1.5.2 L11, L15; 1.5.5 L1; 1.6.4 L9, L12 to L13.
- **Uses.** `data-table` (cells and margins), `mass-editor` (probability mode keeps the grand total at 1), `marks` (mosaic thumbnail and stratum rate bars), `slider` (stratum sizes), `tex-terms`.
- **Interactions.**
  - Pointer: edit cells (keypad on touch); tap a row or column header to condition on it; display chips (counts, joint, row conditional, column conditional, expected); in `simpson`, stratum tabs, Combine, and stratum-size sliders.
  - Keyboard: the `data-table` grid; C conditions on the focused row or column; D cycles the display.
- **State.** `{ cells: Entry[][]; display: 'counts' | 'joint' | 'row' | 'col' | 'expected'; conditioned: { row?: number; col?: number } | null; strata?: Entry[][][]; combined: boolean }`.
- **Answers and checks.** `numeric` and `probability` (any cell, margin or conditional); `state` (table equals a target; predicate `independent-events` applied to the table); `choice`.
- **Config.**

```ts
interface ContingencyTableConfig {
  rows: { title: string; labels: string[] };
  cols: { title: string; labels: string[] };
  cells?: Entry[][];
  editable?: 'none' | 'cells' | 'margins' | 'all';
  display?: 'counts' | 'joint' | 'row' | 'col' | 'expected';
  strata?: { label: string; cells: Entry[][] }[];
  mosaic?: boolean;
  chi2?: boolean;                      // P1: (O - E)^2 / E per cell
}
```

- **Visual.** Margins in weight 600; the conditioned row in `--manip-wash` and the rest at `--out`; the mosaic thumbnail beside the table on desktop and below it on mobile, drawn with `prob-square` geometry; in `simpson`, per-stratum rate bars with direct labels and the aggregate bar, with an ink arrow marking the reversal.
- **Motion.** Conditioning morphs values to percentages over 300ms. Combine slides the stratum tables together and sums them over 480ms.
- **Reduced motion.** Instant.
- **Accessibility.** A native table with scoped headers; conditional displays announce their denominator ("Row: smokers, 120 people").
- **Tutor hooks.** Describe: "2 × 2 counts. Treated: 81/87 and 192/263; Control: 234/270 and 55/80. Display: row conditional. Combined: no." Ids: `cell:<r>,<c>`, `row:<r>`, `col:<c>`, `margin:row:<r>`, `margin:col:<c>`, `stratum:<i>`, `mosaic`.
- **Performance.** Tables up to $6 \times 6$; trivial.
- **Artifact and web.** No difference.
- **Generators.** Integer tables with tidy conditionals; Simpson instances whose reversal is verified by exact arithmetic; independence and dependence pairs; $\chi^2$ items (P1).
- **Misconceptions.** `simpson-aggregate-trusted`, `pairwise-means-mutual`, `joint-vs-conditional`.

#### 6.1.4 `odds-ledger`: Odds ledger

**Composite · P0 · D1 (Bayes factors P1, E).** Bayes' rule in odds form, with evidence that adds on a log scale.

- **Purpose.** $\text{posterior odds} = \text{prior odds} \times \text{likelihood ratio}$. On the log-odds line every piece of independent evidence is a jump of $\ln \text{LR}$, so evidence accumulates by addition and in any order.
- **Serves.** 1.5.2 L8, L16, L17; 1.6.4 L3; 1.6.6 L3, L9.
- **Uses.** `number-line` (dual-labelled log-odds scale), `token-tray` (evidence cards into a ledger zone), `slider` (prior), `draggable-point` (prediction marker), `tex-terms` (the product chain).
- **Interactions.**
  - Pointer: drag evidence cards into the ledger (or tap a card then the ledger); reorder or remove them; set the prior with the slider; in predict mode drag a marker to where the posterior will land, then Apply.
  - Keyboard: `token-tray` keys for cards; the prior and the prediction marker are sliders.
- **State.** `{ priorLogOdds: number; applied: Id[]; prediction?: number }`.
- **Answers and checks.** `probability` and `numeric` (posterior probability or odds), `point` (prediction on the line, tolerance in log-odds units), `choice`.
- **Config.**

```ts
interface OddsLedgerConfig {
  hypotheses: [string, string];
  prior: Entry | { odds: [number, number] };
  evidence: { id: string; label: string; lr?: Entry; pIfH1?: Entry; pIfH2?: Entry }[];
  scale?: 'ln' | 'log10' | 'log2';
  show: ('odds' | 'prob' | 'logodds')[];
  predict?: boolean;
}
```

- **Visual.** The line is 1.5px `--axis` with log-odds ticks above and probability ticks below. Prior marker `--s6`, posterior marker `--s3`, evidence jumps as `--s2` arcs labelled "× 9". The prediction marker is `--manip`. Cards are `lip-token` chips showing their ratio.
- **Motion.** Applying a card sends the marker along an arc, 300ms `--ease-standard`. Show-why `commute`: replays the cards in reverse order to the same end point.
- **Reduced motion.** The marker jumps.
- **Accessibility.** The line is a slider-like readout with `aria-valuetext` "odds 18 to 99, probability 0.154". The ledger is a list.
- **Tutor hooks.** Describe: "Prior odds 1:99 (P = 0.01). Applied: positive test (× 10). Posterior odds 10:99 (P = 0.092)." Ids: `card:<id>`, `marker:prior`, `marker:posterior`, `marker:prediction`, `slider:prior`, `ledger`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Evidence sequences with integer likelihood ratios and tidy posterior odds; fair-against-two-headed coin items; Bayes-factor items (P1).
- **Misconceptions.** `add-probabilities`, `evidence-order-matters`, `lr-is-posterior`.

### 6.2 Random variables and distributions

#### 6.2.1 `rv-mapper`: Random-variable mapper

**Composite · P0 · D2.** A random variable drawn as what it is: a function from outcomes to numbers.

- **Purpose.** Assign numbers to outcomes, then pour each outcome's probability along its arrow into a stem over its value: the PMF appears as the sum of preimage masses. A second stage $g$ merges values, giving the distribution of $g(X)$. LOTUS appears as two routes to the same $E[g(X)]$: averaging over outcomes, and averaging $g$ over the values of $X$ weighted by the PMF.
- **Serves.** 1.5.3 L1, L2, L6, L14; 1.5.7 L3.
- **Uses.** `outcome-grid` (left panel, grid or list), `node-graph` (bipartite layout for list spaces) or `marks` `connector` between two hosts for grids, `number-line` (value axis), `marks` (`stems`), `token-tray` (value tokens dropped on outcomes), `tex-terms`, `stepper` (the pouring demonstration).
- **Interactions.**
  - Pointer: tap an outcome then a value on the axis (two-tap), or drag a value token onto an outcome; apply a rule chip (sum, maximum, number of heads, indicator of an event) to fill every outcome; tap Collect to pour; tap a value to light its preimage; add a $g$ stage and assign its outputs the same way.
  - Keyboard: roving grid over outcomes; V opens a value picker for the focused outcome; P lights the preimage of the focused value; Enter collects.
- **State.** `{ assignment: Record<OutcomeId, number>; g?: Record<string, number>; collected: boolean; highlightValue?: number }`.
- **Answers and checks.** `mapping` (outcome to value), `distribution` (the PMF of $X$ or $g(X)$), `probability` ($P(X = x)$), `numeric` ($E[X]$, $E[g(X)]$), `set` (a preimage).
- **Config.**

```ts
interface RvMapperConfig {
  space: OutcomeGridConfig | { list: { id: string; label: string; p: Entry }[] };
  rule?: string;                         // expr over outcome fields, e.g. 'r + c', 'max(r, c)'
  ruleChips?: { label: string; rule: string }[];
  editable: boolean;
  axis: { min: number; max: number };
  g?: { rule?: string; editable?: boolean };
  show: { pmf: boolean; expectation: boolean; lotus: boolean };
  task: 'assign' | 'preimage' | 'pmf' | 'g' | 'lotus';
}
```

- **Visual.** Outcomes on the left and a vertical value axis on the right on desktop; on mobile the grid sits above and the axis runs horizontally below. Connectors are 1px `--text-muted`; a lit preimage's connectors are 2px `--s2`. PMF stems are `--s3`. Learner-assigned value tokens are `--manip` until graded. The two LOTUS sums sit side by side under the panels with matching tints.
- **Motion.** Collect is a demonstration: each outcome's mass, a disc sized by its probability, travels along its connector and stacks on its stem; staggered 30ms, at most 1.2s in total, skippable by tap. Preimage lighting is instant.
- **Reduced motion.** Stems fill at once; connectors light without travel.
- **Accessibility.** Table view: outcome, probability, $X$ value, $g(X)$ value; a second table for the PMF. Assignments are announced ("Outcome (2, 5) assigned 7").
- **Tutor hooks.** Describe: "Two dice, X = sum. Assigned 36 of 36. Collected: yes. P(X = 7) = 6/36 shown. Lit: preimage of 7." Ids: `outcome:<id>`, `value:<x>`, `stem:<x>`, `connector:<outcome>`, `g:<y>`, `rule:<id>`. Secret: the target PMF.
- **Performance.** Up to 64 outcomes animate individually; for 216 outcomes the pour is aggregated per value. SVG under 600 nodes.
- **Artifact and web.** No difference.
- **Generators.** Random variables on dice, coin and card spaces with tidy PMFs; $g$ items with merging values; LOTUS items.
- **Misconceptions.** `rv-is-an-outcome`, `pmf-counts-values-not-outcomes`, `g-of-mean` ($E[g(X)] = g(E[X])$).

#### 6.2.2 `dist-explorer`: Distribution explorer

**Composite · P0 · D2 to D3.** The named-distribution workbench: density or mass linked with the CDF, intervals, quantiles, moments, comparisons and transforms.

- **Purpose.** One place to learn every named distribution by its story and its shape; to read $P(a < X \le b)$ as an area and as $F(b) - F(a)$; to find quantiles; to see the mean as a balance point and the SD as a spread; to compare an exact distribution with its approximation; and to see why $F^{-1}(U)$ has distribution $F$.
- **Families.** Every family in the `dist` service (section 2.10), plus `custom` built in a `mass-editor`.
- **Modes.**
  - `explore`: parameters, bracket, quantile handle, overlays.
  - `standardise`: shift by $\mu$ then scale by $\sigma$ to $Z$.
  - `inverse-transform`: uniform dots on the CDF's vertical axis travel across to the CDF and down to the $x$ axis, building a histogram.
  - `pit`: the reverse: draws of $X$ go up through $F$ and land uniform.
  - `loss`: a guess $c$ with curves of $E[(X - c)^2]$ and $E\lvert X - c \rvert$ against $c$.
  - `bounds`: a threshold $a$ with the exact tail, Markov's $E[X]/a$, Chebyshev's $\sigma^2/(a - \mu)^2$ and Chernoff's bound.
  - `fit-moments`: parameter sliders to match a data set's mean and variance (1.6.1 L6).
- **Serves.** 1.5.3 L3, L5, L8, L11, L14, L15, L17, L18; 1.5.4 L2 to L5, L7 to L10; 1.5.7 L1, L2, L9, L10; 1.6.1 L6; 1.6.3 L3; and the distribution panels inside `test-lab`, `ci-ladder` and `trial-strip`.
- **Uses.** `plot-axes` twice with a linked $x$ axis, `marks` (`stems`, `curve`, `step`, `region`, `band`, `hist`, hatch fills), `draggable-point` (bracket ends, quantile handle on the CDF's vertical axis, guess $c$, threshold $a$), `slider` (parameters), `mass-editor` (custom), `choice-cards` (family picker), `sim-runner` (sample overlay and the dot streams), `sketch-pad` (sketch-the-CDF tasks), `tex-terms` (the PMF or PDF with live parameters, and $F(b) - F(a)$).
- **Interactions.**
  - Pointer: drag parameter sliders; drag bracket ends on either panel; tap a bracket end to toggle it open or closed (discrete only); drag the quantile handle up the CDF's vertical axis; tap Sample 100 or 1,000 to overlay a histogram; tap Compare to add a second distribution.
  - Keyboard: sliders; bracket ends are sliders (step 1 for discrete, 0.01 of the range for continuous); O toggles the focused end; Q focuses the quantile handle; E types an exact value anywhere.
- **State.** `{ family; params; compare?: { family; params }; bracket?: { a; b; aClosed; bClosed }; q?: number; guess?: number; threshold?: number; sample?: { seed; n }; mode }`.
- **Answers and checks.** `probability` (bracket areas, tails), `numeric` (quantiles, moments, parameter values), `interval` (the bracket as the answer: "the middle 95%"), `point` (quantile handle), `curve` (a sketched CDF, through `sketch-pad` with step features), `choice` (which family tells this story), `state` (predicate `matches-moments`).
- **Config.**

```ts
interface DistExplorerConfig {
  family: Family | 'custom';
  params: Record<string, number>;
  editableParams?: string[];
  ranges?: Record<string, [min: number, max: number, step: number]>;
  panels: ('density' | 'cdf')[];
  compare?: { family: Family; params: Record<string, number>; label: string };
  bracket?: { a: number; b: number; aClosed: boolean; bClosed: boolean; editable: boolean };
  quantile?: boolean;
  overlays?: ('mean' | 'sd-band' | 'fulcrum' | 'median' | 'mode' | 'deviation-squares'
            | 'continuity' | 'markov' | 'chebyshev' | 'chernoff')[];
  mode?: 'explore' | 'standardise' | 'inverse-transform' | 'pit' | 'loss' | 'bounds' | 'fit-moments';
  sample?: { sizes: number[]; seed: number };
  geometricConvention?: 'failures' | 'trials';
  show: { formula: boolean; story: boolean };
}
```

- **Visual.** Discrete mass as `--s3` stems; continuous density as a 2.5px `--s3` curve. The bracket region is `--s3` at 25%, its edges solid ink when closed and dashed when open. The CDF panel draws discrete CDFs with the filled-top, hollow-bottom dots (decision 14) and continuous CDFs as a curve; the bracket shows on the CDF as a vertical brace on the $y$ axis labelled $F(b) - F(a)$. Comparisons are `--s6` dashed; sample histograms `--s2` at 35%. The mean is an ink fulcrum triangle under the axis; the SD band is a `--text-muted` bracket; deviation squares are `--s2` at 15%. Handles are `--manip`.
- **Motion.** Parameter changes and drags redraw directly. Show-why keys: `standardise` (shift 400ms, then scale 400ms, with axis relabelling, `--ease-morph`); `inverse-transform` (50 dots, 400ms each, staggered 20ms); `endpoint` (flashes the stem at a closed or open end twice); `area-not-height` (fills the bracket, then shows that one tall point has zero area).
- **Reduced motion.** Show-why becomes before-and-after with Play; the dot stream lands as a finished histogram.
- **Accessibility.** Table view: for discrete, $x$, $P(X = x)$ and $F(x)$ for up to 60 rows; for continuous, quantiles at 5% steps and the bracket probability. Sliders say their parameter ("lambda, 3.5"). Bracket changes are announced on commit ("P of 2 less than X, at most 5: 0.537").
- **Tutor hooks.** Describe: "Binomial(n = 10, p = 0.3). Bracket 2 ≤ X ≤ 4: 0.5372. Mean 3, SD 1.449. Compare: none. Mode: explore." Ids: `family`, `slider:<param>`, `stem:<x>`, `curve:density`, `curve:cdf`, `bracket:a`, `bracket:b`, `region:bracket`, `handle:quantile`, `marker:mean`, `band:sd`, `curve:compare`, `hist:sample`, `handle:guess`, `handle:threshold`. Secret: target probability, quantile or parameters.
- **Performance.** Up to 200 stems as SVG, then one path; curves at 400 samples; one CDF evaluation under 0.05ms [unverified]; a slider frame recomputes in under 2ms. The dot stream draws at most 200 moving dots.
- **Artifact and web.** No difference.
- **Generators.** Per family: interval probabilities with tidy exact answers (binomial and hypergeometric as fractions, normal at table $z$ values, Poisson with small $\lambda$); quantile items; approximation items with and without continuity correction; story-to-family choice items; bound items.
- **Misconceptions.** `pdf-is-probability`, `discrete-endpoint`, `geometric-convention`, `sd-vs-variance`, `no-continuity-correction`, `markov-is-an-estimate`, `median-equals-mean`.

#### 6.2.3 `galton-board`: Galton board

**Composite · P0 · D2.** Balls bounce left or right at each peg: binomial counts, path counting and the normal shape.

- **Purpose.** One ball's path is $n$ Bernoulli trials and also a random walk; the bins count successes; the number of paths into bin $k$ is $\binom{n}{k}$; tilting the board sets $p$; with many rows the shape approaches the normal.
- **Serves.** 1.5.3 L4; 1.5.7 L8.
- **Uses.** `plot-axes`, `marks` (pegs, ball paths, `hist`, `stems`, `curve`), `slider` ($n$, $p$), `sim-runner` (`galton` model), `pascal-triangle` (path counts on the pegs), `mass-editor` (predicted bin heights), `stepper` (a steered ball).
- **Interactions.**
  - Pointer: Drop 1, 10, 100 or 1,000; in steer mode tap Left or Right at each peg; slide $n$ (1 to 20 drawn, up to 100 in histogram-only view) and $p$ (the tilt); toggle overlays (binomial, normal, Pascal counts); in predict mode set bin heights before dropping.
  - Keyboard: buttons; Left and Right arrows steer; sliders; the `mass-editor` keys for predictions.
- **State.** `{ n; p; seed; counts: number[]; steered?: ('L' | 'R')[]; prediction?: number[] }`.
- **Answers and checks.** `probability` (bin $k$), `numeric` (path counts, expected count in a bin), `distribution` (predicted shape, total-variation tolerance), `choice`.
- **Config.**

```ts
interface GaltonBoardConfig {
  n: number; p: number;
  editable: ('n' | 'p')[];
  mode: 'drop' | 'steer' | 'paths';
  overlays?: ('binomial' | 'normal' | 'pascal')[];
  maxBalls?: number;
  predictFirst?: boolean;
}
```

- **Visual.** Pegs are 4px ink dots in a triangular lattice; balls are `--s2` discs; a steered path is a `--manip` polyline; bins fill as an `--s2` histogram at 35%; binomial stems `--s3`; normal curve `--s6` dashed; Pascal counts in the caption token above each peg.
- **Motion.** The first 20 balls bounce peg to peg at 60ms per row with an ease-in, as data arriving; later balls land directly in the histogram in batches. The steered ball moves one row per tap, 120ms.
- **Reduced motion.** No bouncing; counts increment.
- **Accessibility.** Table view: bin, count, expected count. Steering uses named buttons. After each batch: "500 balls, 12 rows, p = 0.5. Most in bin 6 (113)."
- **Tutor hooks.** Describe: "12 rows, p = 0.5. 500 balls dropped; counts 0, 2, 9, 28, 61, 97, 113, 95, ... Overlays: binomial." Ids: `peg:<row>,<k>`, `bin:<k>`, `slider:n`, `slider:p`, `path:steered`, `overlay:normal`, `overlay:binomial`.
- **Performance.** At most 20 animated balls in SVG; bins up to 101; $10^5$ balls are binomial draws in the worker, never per-peg simulation.
- **Artifact and web.** No difference.
- **Generators.** Path-count and bin-probability items with exact fractions; tilt items ($p \ne \frac{1}{2}$).
- **Misconceptions.** `bins-equally-likely`, `one-path-per-bin`.

#### 6.2.4 `convolver`: Convolver

**Composite · P0 · D2 to D3.** The distribution of $X + Y$ for independent $X$ and $Y$, discrete and continuous, and repeated sums.

- **Purpose.** Discrete: $P(X + Y = s)$ is the sum along one anti-diagonal of the joint grid. Continuous: $f_{X+Y}(s) = \int f_X(t) f_Y(s - t)\,dt$, seen as flipping $f_Y$, sliding it to $s$, and measuring the overlap of the product. Repeated self-convolution of a skewed shape heads to the normal, a mechanical view of the CLT.
- **Serves.** 1.5.3 L7; 1.5.4 L7, L15; 1.5.7 L8.
- **Uses.** `plot-axes` (two or three panels), `marks` (`stems`, `curve`, `region`, `hist`), `draggable-point` (the shift $s$ on the axis), `slider` ($n$ in repeat mode), `outcome-grid` (discrete joint grid, diagonal display), `tex-terms`.
- **Interactions.**
  - Pointer: drag $s$ along the axis; tap an anti-diagonal to sum it; in trace mode sweep $s$ and watch the result curve drawn behind the handle; tap Convolve again to add one more copy.
  - Keyboard: $s$ is a slider; diagonals are a roving list; N convolves again.
- **State.** `{ mode; s: number; n: number; traced: [number, number][] }`.
- **Answers and checks.** `probability` and `numeric` ($P(X + Y = s)$, $f(s)$), `curve` (sketch the result: support, peak, symmetry features), `choice` (shape), `expression` (the density of a sum of two uniforms piecewise).
- **Config.**

```ts
interface ConvolverConfig {
  mode: 'discrete-grid' | 'flip-slide' | 'repeat';
  X: DistSpec; Y?: DistSpec;            // Y defaults to X
  range: [number, number];
  nMax?: number;                        // repeat mode, at most 50
  standardise?: boolean;                // repeat mode: rescale each sum to mean 0, SD 1
  trace?: boolean;
}
```

- **Visual.** $f_X$ in `--s3`; flipped and shifted $f_Y$ in `--s6` dashed; the product shaded `--s3` at 30%; the traced result in 2px ink; the $s$ handle `--manip`. In repeat mode the standardised sum is `--s3` against a dashed `--s6` normal.
- **Motion.** The sweep is direct. Repeat morphs from $n$ to $n + 1$ over 480ms (a demonstration on tap).
- **Reduced motion.** Jumps.
- **Accessibility.** Table view of $s$ against $P(X + Y = s)$ or $f(s)$ on a grid; the overlap value announced on commit.
- **Tutor hooks.** Describe: "Flip and slide: X, Y uniform(0, 1). s = 1.4: overlap 0.6. Traced from 0 to 1.4." Ids: `handle:s`, `curve:fx`, `curve:fy-flipped`, `region:overlap`, `curve:result`, `diag:<s>`, `slider:n`.
- **Performance.** Discrete convolution of up to 400 support points directly; continuous densities on a 512-point grid with the overlap integral by the trapezoid rule each frame (512 products); repeat mode precomputes up to 50 convolutions on a 1,024-point grid by FFT in the worker at mount.
- **Artifact and web.** No difference.
- **Generators.** Sums of small discrete variables with exact fractions; continuous sum densities at chosen points; shape items.
- **Misconceptions.** `sum-of-uniforms-uniform`, `add-the-densities`, `add-the-pmfs`.

#### 6.2.5 `indicator-board`: Indicator board

**Composite · P0 · D2.** Linearity of expectation made visible: one lamp per indicator, lit when its event happens.

- **Purpose.** $X = \sum_j I_j$, so $E[X] = \sum_j P(A_j)$, whether or not the events are independent. The learner computes one $P(A_j)$ by symmetry, multiplies by $n$, and then watches the running average of the lit count settle on it. Variance mode adds the covariance grid: $\mathrm{Var}(X) = \sum_j \mathrm{Var}(I_j) + \sum_{i \ne j} \mathrm{Cov}(I_i, I_j)$.
- **Scenarios** (registered modules): fixed points of a shuffle (hat check), records in a random sequence, distinct coupons after $m$ draws and coupon waiting times, pairs sharing a birthday, runs and pattern occurrences in coin flips, cards above the first ace, empty boxes when balls are thrown into boxes, local maxima of a random permutation.
- **Serves.** 1.5.1 L9, L12, L14; 1.5.3 L9, L10, L16, L18, L20; 1.5.4 L17.
- **Uses.** `chance-object` (cards, hats, coins), `marks` (lamp row, `hist`, trace, signed heatmap), `sim-runner`, `slider` ($n$), `tex-terms` (the sum of indicators with live values), `numeric-entry`, `data-table`.
- **Interactions.**
  - Pointer: New instance (one seeded draw shown on the objects); Run 100 or 10,000 instances; tap a lamp to see its event and enter $P(I_j = 1)$; slide $n$; toggle the covariance grid.
  - Keyboard: buttons; lamps are a roving list (Enter opens the event card); slider.
- **State.** `{ scenario; n; seed; instances: number; runningMean: number; selectedLamp?: number; entered?: Record<string, string> }`.
- **Answers and checks.** `probability` ($P(I_j = 1)$), `numeric` ($E[X]$, $\mathrm{Var}(X)$), `expression` ($E[X]$ as a function of $n$, such as $n\left(1 - (1 - \frac{1}{n})^m\right)$), `choice`.
- **Config.**

```ts
interface IndicatorBoardConfig {
  scenario: 'fixed-points' | 'records' | 'coupons' | 'birthday-pairs' | 'runs' | 'pattern-count'
          | 'above-first-ace' | 'empty-boxes' | 'local-maxima';
  n: number;
  params?: Record<string, number>;      // m draws, d days, pattern
  editable?: ('n')[];
  show: { runningMean: boolean; covariances?: boolean; exactLine?: 'after-check' | 'always' | 'never' };
  predictFirst?: boolean;
}
```

- **Visual.** Objects in a row with a lamp under each: lit is a filled `--s2` circle with "1", unlit an outline with "0". The count readout uses the stat token. The running-mean trace is `--s2` with the exact value as a dashed ink line. The covariance grid uses the diverging ramp with + and − glyphs.
- **Motion.** New instance shuffles the objects (300ms, a consequence) and lights lamps staggered 40ms.
- **Reduced motion.** Instant.
- **Accessibility.** Each position reads "Position 3: card 3, a match, 1". Table view of instance counts. Batches announce the running mean and the exact value when shown.
- **Tutor hooks.** Describe: "Fixed points, n = 10. 1,000 instances: mean count 1.004. Exact line hidden. Lamp 3 open: P(card 3 in place) entered 1/10." Ids: `object:<j>`, `lamp:<j>`, `count`, `trace:mean`, `line:exact`, `cov:<i>,<j>`, `slider:n`. Secret: $E[X]$ and $\mathrm{Var}(X)$.
- **Performance.** $n \le 52$ objects in SVG; $10^5$ instances in the worker.
- **Artifact and web.** No difference.
- **Generators.** Scenario and $n$ pairs with exact expectations (fixed points 1; records $H_n$; coupons $n H_n$; birthday pairs $\binom{n}{2}/d$); expression items for general $n$; variance items.
- **Misconceptions.** `linearity-needs-independence`, `find-the-distribution-first`, `indicator-expectation-is-count`.

#### 6.2.6 `trial-strip`: Trial strip and Poisson process

**Composite · P0 · D2 to D3.** Sequences of trials and arrivals on a line: waiting times, patterns, memorylessness, and the Poisson process.

- **Purpose.** Discrete: a strip of coin flips shows the wait to the first head (geometric), to the $r$th head (negative binomial), to a pattern such as HH or HT, and runs. Memorylessness: condition on no success in the first $k$ cells; the remaining wait has the same histogram. Continuous: arrivals at rate $\lambda$ on a time line; counts in a window are Poisson; gaps are exponential; two streams superpose; thinning keeps each arrival with probability $p$. The discretised mode splits time into $n$ slots with probability $\lambda/n$ each and lets $n$ grow, so the Bernoulli strip becomes the Poisson process.
- **Serves.** 1.5.3 L11, L12, L13, L17, L20; 1.5.4 L5, L6.
- **Uses.** `chance-object` (coin faces at small size), `marks` (strip cells, arrival ticks, `hist`, `stems`), `region-selector` (bracket windows on the line), `slider` ($p$, $\lambda$, $n$), `token-tray` (pattern builder), `sim-runner` (`bernoulli-seq`, `pattern`, `poisson-process`), `dist-explorer` (theoretical overlay).
- **Interactions.**
  - Pointer: Flip 1; Run until the pattern; Run 1,000 sequences; build a pattern from H and T tokens; drag a window bracket on the time line to count arrivals; sliders; toggle Condition on no success in the first $k$.
  - Keyboard: buttons; H and T keys append flips in hand mode; bracket ends are sliders; sliders.
- **State.** `{ seed; mode; p?; lambda?; n?; strip: string; arrivals?: number[]; pattern?: string; waits: number[]; window?: [number, number]; conditioned?: number }`. The strip keeps the last 400 cells.
- **Answers and checks.** `numeric` (expected waits, window probabilities), `probability`, `choice` (which pattern comes sooner; which race wins), `distribution` (predicted wait histogram).
- **Config.**

```ts
interface TrialStripConfig {
  mode: 'bernoulli' | 'poisson' | 'discretised';
  p?: number; lambda?: number; n?: number;
  pattern?: string | { race: [string, string] };
  displays: ('strip' | 'waits-hist' | 'window-count-hist' | 'gap-hist')[];
  condition?: { noSuccessFirst: number };
  streams?: { label: string; lambda: number }[];      // superposition
  thinning?: number;
  predictFirst?: CheckSpec;
}
```

- **Visual.** Cells are 20px squares: H filled `--s2` with the letter H, T outlined with the letter T. A detected pattern gets an ink bracket. Arrival ticks are 2px `--s2`; superposed streams use `--s2` and `--s6` with labels and different tick heights. The window bracket is `--manip`. Histograms are `--s2` with `--s3` theory stems or curves.
- **Motion.** In hand and flip modes cells appear at 40ms each (data arriving). Batches fill histograms.
- **Reduced motion.** Cells and histograms appear at once.
- **Accessibility.** The strip reads as text ("H T T H H"); the window announces its count ("3 arrivals between 2.0 and 4.5"). Table views for every histogram.
- **Tutor hooks.** Describe: "Pattern race HH against HT, fair coin. 1,000 sequences: mean wait HH 5.96, HT 4.02. Exact hidden." Ids: `cell:<i>`, `pattern:<id>`, `window`, `tick:<i>`, `hist:waits`, `hist:window`, `slider:p`, `slider:lambda`, `slider:n`. Secret: exact expected waits.
- **Performance.** At most 400 visible cells, virtualised beyond; $10^5$ sequences in the worker; arrival lines up to 2,000 ticks in one path.
- **Artifact and web.** No difference.
- **Generators.** Waiting-time and pattern-race problems over coins and dice; exact answers from the pattern automaton solved by `first-step-solver`'s exact engine; Poisson window and gap items.
- **Misconceptions.** `hh-equals-ht`, `due-for-a-success`, `poisson-windows-not-additive`, `geometric-convention`.

#### 6.2.7 `generating-function`: Generating functions

**Composite · P0 · D3.** PGFs and MGFs as curves whose derivatives at 0 hold the moments.

- **Purpose.** $M_X(t) = E[e^{tX}]$: the slope at $t = 0$ is $E[X]$ and the second derivative is $E[X^2]$; the Taylor coefficients are $E[X^k]/k!$. For independent variables $M_{X+Y} = M_X M_Y$, which is why sums of Poissons are Poisson. For discrete variables $G(s) = E[s^X]$ holds the PMF in its coefficients, and a branching process dies out with probability equal to the smallest fixed point of $G$.
- **Serves.** 1.5.4 L11, L12, L13.
- **Uses.** `plot-axes`, `marks` (`curve`, tangent, osculating parabola, labels), `draggable-point` ($t$ on the curve), `slider` (parameters), `tex-terms`, `taylor-builder` (series view), `iteration-cobweb` (extinction), `choice-cards` (match the MGF).
- **Interactions.**
  - Pointer: drag $t$ along the curve; toggle the tangent at 0 and the osculating parabola; choose a second distribution to multiply; in branching mode iterate $s_{k+1} = G(s_k)$ by tapping Next.
  - Keyboard: $t$ is a slider; toggles; N iterates.
- **State.** `{ kind: 'mgf' | 'pgf'; family; params; t: number; combineWith?: DistSpec; iterates?: number[] }`.
- **Answers and checks.** `numeric` (moments, extinction probability), `expression` (the MGF of a sum, a moment from an MGF), `choice` (which distribution has this MGF).
- **Config.**

```ts
interface GeneratingFunctionConfig {
  kind: 'mgf' | 'pgf';
  family: Family | 'custom'; params: Record<string, number>;
  show: ('tangent' | 'curvature' | 'series' | 'product' | 'cobweb')[];
  combine?: DistSpec;
  tRange?: [number, number];
  offspring?: Entry[];                  // PGF branching: P(k children)
}
```

- **Visual.** $M(t)$ in `--s3`; the tangent at 0 in `--s6` with its slope labelled; the product curve ink; the $t$ handle `--manip`; the cobweb in ink with iterates as `--s2` dots.
- **Motion.** Direct. Cobweb steps over 300ms on tap.
- **Reduced motion.** Steps jump.
- **Accessibility.** Table of $t$ against $M(t)$; readouts announce "slope at zero 2, so E of X is 2".
- **Tutor hooks.** Describe: "MGF of Poisson(2). Tangent at 0: slope 2.00. Curvature toggle on." Ids: `curve:m`, `handle:t`, `tangent`, `parabola`, `term:<k>`, `curve:product`, `cobweb`, `iterate:<k>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** MGF recognition items; moments from MGFs; sums of independent variables; extinction probabilities with rational fixed points.
- **Misconceptions.** `mgf-is-a-probability`, `mgf-of-sum-is-sum`, `extinction-is-largest-root`.

### 6.3 Continuous, joint and limiting behaviour

#### 6.3.1 `order-statistics`: Order statistics

**Composite · P0 · D3.** Sort a sample; follow the $k$th smallest; see Beta distributions and spacings.

- **Purpose.** For $n$ uniforms, the sorted values cut $[0, 1]$ into $n + 1$ pieces of equal expected length, so $E[U_{(k)}] = \frac{k}{n+1}$ and $U_{(k)} \sim \text{Beta}(k, n - k + 1)$. For a general $F$, $P(\max \le x) = F(x)^n$ and $P(\min > x) = (1 - F(x))^n$. For exponentials, spacings are exponential with rates $n, n - 1, \dots$, a memorylessness argument interviewers like.
- **Serves.** 1.5.4 L7, L16; 1.5.9 L8 (broken stick, with `geo-prob`).
- **Uses.** `number-line`, `sim-runner`, `marks` (dots, spacing braces, `hist`, `curve`), `slider` ($n$, $k$), `draggable-point` (prediction marker), `choice-cards` (base distribution).
- **Interactions.**
  - Pointer: Draw a sample (dots fall onto the line); Sort labels them $U_{(1)}$ to $U_{(n)}$; slide $k$; Run 1,000 samples to build the histogram of $U_{(k)}$; drag the prediction marker before running; switch the base distribution.
  - Keyboard: buttons; sliders; the marker is a slider.
- **State.** `{ base: DistSpec; n; k; seed; sample: number[]; hist: Uint32Array; prediction?: number }`.
- **Answers and checks.** `numeric` ($E[U_{(k)}]$, $P(\max \le x)$), `point` (prediction), `expression` (the CDF of the maximum), `choice`.
- **Config.**

```ts
interface OrderStatisticsConfig {
  base: DistSpec;                    // uniform, exponential, normal
  n: number; k: number;
  editable: ('n' | 'k' | 'base')[];
  show: ('beta' | 'spacings' | 'cdf-max' | 'cdf-min')[];
  predictFirst?: CheckSpec;
}
```

- **Visual.** Sample dots `--s2` on the line; the $k$th gets an ink ring and label; spacing braces `--text-muted`; the histogram `--s2`; the Beta density `--s3`; the prediction marker `--manip`.
- **Motion.** Sort lifts each dot and attaches its label over 300ms (a consequence). Batches fill.
- **Reduced motion.** Instant.
- **Accessibility.** The sample is listed in sorted order; histogram table view; "1,000 samples of 5: mean of the maximum 0.834, Beta(5, 1) mean 0.833".
- **Tutor hooks.** Describe: "Uniform, n = 5, k = 5. Last sample sorted: 0.11, 0.38, 0.52, 0.70, 0.93. 1,000 samples: mean of U(5) 0.834." Ids: `dot:<i>`, `kth`, `spacing:<i>`, `hist`, `curve:beta`, `slider:n`, `slider:k`, `marker:prediction`.
- **Performance.** Trivial in SVG; $10^5$ samples with $n \le 50$ sorted in the worker.
- **Artifact and web.** No difference.
- **Generators.** Expected order statistics; max and min CDF items; exponential spacing items.
- **Misconceptions.** `max-of-uniforms-is-one`, `order-stats-independent`.

#### 6.3.2 `sampling-lab`: Sampling lab

**Composite · P0 for sampling, LLN, CLT and $t$ modes (D3); P1 for bootstrap, permutation and p-value modes (E).** Population, one sample, and the sampling distribution of a statistic, stacked.

- **Purpose.** The picture under all of statistics. The top panel is the population (a distribution, or a data set treated as one). The middle panel is one sample of size $n$, as dots. The bottom panel collects one dot per sample: the statistic's sampling distribution. LLN mode runs one growing sample with a running statistic. CLT mode standardises the bottom panel and overlays $N(0, 1)$. Bootstrap mode makes the observed data the population. Permutation mode shuffles group labels to build a null distribution. p-value mode collects p-values, uniform under the null.
- **Serves.** 1.5.4 L1, L8, L10; 1.5.7 L5, L7, L8, L10, L11; 1.6.1 L1, L2; 1.6.2 L6, L7; 1.6.3 L6; 1.6.4 L6, L7, L8.
- **Uses.** `plot-axes` three times, linked on $x$ for the top two, `marks` (`curve`, `hist`, `rug`, dots, `band`), `sim-runner` (`sample-statistic`, `bootstrap`, `permutation-test`), `slider` ($n$), `choice-cards` (population shape and statistic), `chance-object` (token draws for the first bootstrap resamples), `mass-editor` (custom population), `draggable-point` (prediction bracket), `qq-plot` (P1 companion).
- **Interactions.**
  - Pointer: Draw 1 sample (dots fall from the population to the sample row, the statistic drops to the bottom panel); Draw 10, 100, 1,000 or 10,000; slide $n$ (clears the bottom panel); choose the statistic; toggle Standardise and the normal or $t$ overlay; drag the prediction bracket (centre and one-SD width) before drawing; in LLN mode, Play.
  - Keyboard: buttons; slider; chips; the bracket's centre and edge are sliders.
- **State.** `{ population: PopulationSpec; n; statistic; seed; drawn: number; lastSample: number[]; statHist: Uint32Array; edges: Float64Array; mode; prediction?: { centre?: number; sd?: number } }`.
- **Answers and checks.** `numeric` (standard errors, CLT probabilities), `point` (prediction centre), `interval` (bootstrap percentile interval, P1; or a predicted one-SD band), `choice` (shape), `state` (at least $N$ samples drawn, for exploration screens).
- **Config.**

```ts
interface SamplingLabConfig {
  mode: 'sampling' | 'lln' | 'clt' | 't-stat' | 'bootstrap' | 'permutation' | 'pvalues';
  population: { dist: DistSpec } | { data: number[] } | { custom: Entry[]; support: number[] };
  n: number | { values: number[] };
  statistic: 'mean' | 'sum' | 'median' | 'proportion' | 'var-n' | 'var-n-1' | 'max' | 'min'
           | 't' | 'z' | 'mle' | 'p-value' | 'diff-means';
  batches: number[];
  overlays?: ('normal' | 't' | 'truth-line' | 'se-bracket')[];
  standardise?: boolean;
  groups?: { a: number[]; b: number[] };       // permutation
  test?: TestSpec;                             // p-value mode
  predictFirst?: CheckSpec;
}
```

- **Visual.** Population curve `--s3` (or a `--s3` histogram for data); sample dots `--s2` on a rug row; the statistic histogram `--s2` at 35%; theoretical sampling distribution `--s6` dashed; truth line dashed ink labelled $\mu$; the prediction bracket `--manip`. Panel titles in the label token: "Population", "One sample, n = 30", "1,000 sample means".
- **Motion.** Draw 1 is a short demonstration: dots fall 300ms with a 15ms stagger, then the statistic dot drops 300ms. Batches fill in chunks within 1.1s. Bootstrap's first three resamples show `chance-object` tokens drawn from a bag of the data with replacement.
- **Reduced motion.** Results appear at once.
- **Accessibility.** "Population exponential, mean 1. n = 30. 1,000 sample means: mean 1.003, SD 0.181; theory 0.183." Table views for each panel's histogram.
- **Tutor hooks.** Describe: "Mode CLT. Population: exponential(1). n = 5. 1,000 means drawn; standardised; normal overlay on. Prediction bracket SD 0.40." Ids: `panel:population`, `panel:sample`, `panel:stat`, `dot:<i>`, `stat:last`, `hist:stat`, `curve:normal`, `curve:t`, `line:truth`, `bracket:prediction`, `slider:n`, `chip:<statistic>`. Secret: the exact standard error and the truth.
- **Performance.** Up to $10^4$ samples of $n \le 1{,}000$ ($10^7$ draws) in the worker, about 100ms [unverified]; histograms stream in chunks; at most 200 bins drawn in SVG and 200 sample dots.
- **Artifact and web.** No difference.
- **Generators.** Seeds and populations for prediction items ($\sigma/\sqrt{n}$; CLT tail probabilities; required $n$); bootstrap data sets (P1).
- **Misconceptions.** `clt-makes-data-normal`, `law-of-small-numbers`, `se-vs-sd`, `cauchy-obeys-lln`, `bootstrap-creates-information` (P1), `p-values-cluster-near-005` (P1).

#### 6.3.3 `joint-density`: Joint distribution explorer

**Composite · P0 · D3.** Joint PMFs and PDFs with marginals as projections and conditionals as renormalised slices.

- **Purpose.** Integrate out to get a marginal (the heatmap squashes onto an axis); slice at $X = x$ and renormalise to get $f_{Y \mid X}(y \mid x)$; test independence by asking whether every slice has the same shape; compute region probabilities such as $P(X < Y)$.
- **Serves.** 1.5.5 L1 to L5, L12, L13; 1.5.6 (data source for `cond-expectation`).
- **Uses.** `plot-axes` (main panel plus marginal panels sharing axes), `plot-3d` (optional surface), `marks` (heatmap, contours, `stems` for discrete, `curve`, `region`), `draggable-point` (slice handle), `region-selector` (preset regions; rectangle by two corners), `slider` (parameters), `region-bounds` (integral set-up), `contingency-table` (discrete table view).
- **Interactions.**
  - Pointer: drag the slice line ($x = x_0$ or $y = y_0$); tap Marginal to squash; tap a region chip or set a rectangle's corners; toggle 3D and orbit.
  - Keyboard: the slice is a slider; region chips are buttons; the rectangle corners are 2D handles; 3D keys as in `plot-3d`.
- **State.** `{ joint: JointSpec; slice?: { axis: 'x' | 'y'; at: number }; region?: RegionSpec; view: '2d' | '3d'; marginals: boolean }`.
- **Answers and checks.** `probability` (region probabilities, conditional probabilities), `numeric` (marginal density values, $E[Y \mid X = x]$), `choice` (independent or not), `curve` (sketch a marginal or a conditional), `expression` (a marginal density), `set` (the support).
- **Config.**

```ts
interface JointDensityConfig {
  joint: { kind: 'table'; xs: number[]; ys: number[]; p: Entry[][] }
       | { kind: 'density'; expr: string; support: [number, number][] | 'rect';
           box: { x: [number, number]; y: [number, number] } }
       | { kind: 'bvn'; mu: [number, number]; sigma: [number, number]; rho: number };
  show: ('heat' | 'contours' | 'marginals' | 'slices' | '3d' | 'ellipse')[];
  slice?: { axis: 'x' | 'y'; at: number; editable: boolean };
  regions?: { id: string; label: string; polygon?: [number, number][]; expr?: string }[];
  task?: 'marginal' | 'conditional' | 'independence' | 'region';
}
```

- **Visual.** Heat on `--seq-1` to `--seq-6`; contours 1px ink with inline labels; support outline 2px ink; slice line 2px `--manip` with its handle; the slice panel shows the raw slice heights dashed `--s6` and the renormalised conditional solid `--s3`, so renormalisation is visible; marginals `--s3` in the side panels; a learner region `--manip-wash`, a given region `--s2` hatch.
- **Motion.** The slice is direct. Marginal squashes the heatmap into the side panel over 600ms `--ease-morph`. Show-why `renormalise` stretches the raw slice to the conditional over 400ms.
- **Reduced motion.** Before-and-after.
- **Accessibility.** Discrete: the table view is a `contingency-table`. Continuous: a description of the support, the mode and the correlation, a values table on a $9 \times 9$ grid, and a slice table.
- **Tutor hooks.** Describe: "Density f(x, y) = x + y on the unit square. Slice at x = 0.25: conditional density (0.25 + y)/0.75. Region X < Y: 0.5 shown." Ids: `heat`, `contours`, `slice`, `panel:conditional`, `panel:marginal-x`, `panel:marginal-y`, `region:<id>`, `support`. Secret: region probabilities and marginal formulas.
- **Performance.** The heatmap is a $64 \times 64$ grid computed on parameter change only (about 0.4ms with a compiled expression [unverified]); contours by marching squares on parameter change only; the slice evaluates 400 points per frame.
- **Artifact and web.** No difference.
- **Generators.** Joint tables with tidy marginals and conditionals; polynomial densities on squares and triangles with exact region probabilities (verified by `quad` in CI); independence pairs.
- **Misconceptions.** `slice-is-conditional-without-renormalising`, `marginals-determine-joint`, `zero-correlation-means-independent`.

#### 6.3.4 `covariance-lab`: Covariance lab

**Composite · P0 · D3 (Anscombe preset P1).** Covariance as the average signed area of rectangles from the mean point.

- **Purpose.** For each point, the rectangle from $(\bar x, \bar y)$ to the point has signed area $(x_i - \bar x)(y_i - \bar y)$; covariance is their average. Standardising the axes turns covariance into correlation. The learner drags points and watches rectangles flip sign, guesses correlations, builds zero correlation with obvious dependence ($Y = X^2$), and sees one outlier swing $r$. Sum mode shows $\mathrm{Var}(X + Y) = \mathrm{Var}(X) + \mathrm{Var}(Y) + 2\,\mathrm{Cov}(X, Y)$.
- **Serves.** 1.5.5 L6, L7, L8; 1.5.7 L4; 1.6.5 (Anscombe, P1).
- **Uses.** `plot-axes`, `marks` (scatter, `rect-signed`, mean lines), `draggable-point` (data points), `slider` ($\rho$ and $n$ for generated data), `numeric-entry` (guesses), `sim-runner` (generated samples).
- **Interactions.**
  - Pointer: drag points; toggle rectangles and standardised axes; Add point; in the guessing game enter $r$ (or use its slider) then Reveal; generate data at a chosen $\rho$ and shape.
  - Keyboard: points are 2D handles (arrows move by the grid step); T toggles rectangles; S standardises.
- **State.** `{ points: Vec2[]; showRects: boolean; standardised: boolean; guess?: number }`.
- **Answers and checks.** `numeric` (covariance, $r$; guesses within $\pm 0.1$), `choice` (sign; which set has the larger $r$), `state` (predicate `corr-near`, or zero covariance with a nonlinear pattern).
- **Config.**

```ts
interface CovarianceLabConfig {
  data: Vec2[] | { generate: { n: number; rho: number;
                   shape: 'linear' | 'quadratic' | 'circle' | 'clusters' | 'anscombe-1' | 'anscombe-2'
                        | 'anscombe-3' | 'anscombe-4'; seed: number } };
  movable: boolean;
  show: ('rects' | 'means' | 'r' | 'cov' | 'fit' | 'sum')[];
  task?: 'guess' | 'make-r' | 'zero-cov-dependent' | 'compute';
}
```

- **Visual.** Points are 6px ink, `--manip` when movable. Positive rectangles `--s3` at 15% with a + glyph; negative `--s2` at 15% with a − glyph. Mean lines dashed `--text-muted`. Readouts with tabular figures.
- **Motion.** Direct.
- **Reduced motion.** Not applicable.
- **Accessibility.** Table view with columns $x$, $y$, deviations and their product; "n = 20, covariance 1.8, r = 0.62; 14 positive rectangles, 6 negative".
- **Tutor hooks.** Describe: "20 points. Covariance 1.80, r 0.62. Rectangles on. Guess entered: none." Ids: `point:<i>`, `rect:<i>`, `mean:x`, `mean:y`, `readout:r`, `readout:cov`. Secret: the target $r$ in the guessing game.
- **Performance.** SVG up to 200 points; rectangles drawn for $n \le 60$, above which the four quadrant totals are shown instead.
- **Artifact and web.** No difference.
- **Generators.** Data sets with an exact target sample correlation (generate, then adjust the standardised residual by a 2 × 2 Cholesky step so $r$ hits the target exactly); guess-the-correlation sets; nonlinear zero-correlation sets.
- **Misconceptions.** `zero-correlation-means-independent`, `r-measures-slope`, `outlier-cannot-matter`.

#### 6.3.5 `gaussian-2d`: Bivariate normal

**Composite · P0 · D3.** The bivariate normal shaped by hand: ellipses, conditionals, linear combinations and portfolios.

- **Purpose.** Set $\sigma_X$, $\sigma_Y$ and $\rho$ and see the 1- and 2-standard-deviation ellipses. Slice at $X = x$: the conditional mean lies on the regression line $\mu_Y + \rho\frac{\sigma_Y}{\sigma_X}(x - \mu_X)$, which is not the ellipse's major axis, and the conditional SD is $\sigma_Y\sqrt{1 - \rho^2}$. Point a direction $\mathbf{w}$: the shadow of the cloud on it has variance $\mathbf{w}^\top \Sigma \mathbf{w}$. Portfolio mode fixes $w_1 + w_2 = 1$ and plots $\sigma_p$ against the weight, with its minimum. Cholesky mode builds the cloud from two independent normals. A Trap shows normal marginals with zero correlation that are still dependent (a random sign flip).
- **Serves.** 1.5.5 L8, L10, L11, L12; 1.5.6 L6; 1.6.5 L3.
- **Uses.** `plot-axes`, `marks` (`ellipse`, scatter, line, `band`, `curve`, `hist`), `draggable-point` (ellipse handles, slice handle, direction handle on a circle), `slider` ($\rho$, weight), `matrix` ($\Sigma$ live), `quadratic-form` and `transform-grid` (linked views), `sim-runner` (samples).
- **Interactions.**
  - Pointer: drag the ellipse's $x$ and $y$ extent handles and its tilt handle (or the sliders); drag the slice line; drag the direction handle round the unit circle; drag the portfolio weight; Sample 500.
  - Keyboard: every handle is a slider with its parameter in the value text; E edits exactly.
- **State.** `{ mu: Vec2; sx: number; sy: number; rho: number; x0?: number; w?: Vec2; weight?: number; seed: number }`.
- **Answers and checks.** `numeric` (conditional mean and SD, combination variance, minimum-variance weight, correlation), `point` (predicted conditional mean on the slice), `choice` (which line is the regression line).
- **Config.**

```ts
interface Gaussian2DConfig {
  mu: [number, number]; sigma: [number, number]; rho: number;
  editable: ('sx' | 'sy' | 'rho' | 'mu')[];
  mode: 'shape' | 'conditional' | 'combination' | 'portfolio' | 'cholesky' | 'mahalanobis' | 'sign-flip';
  samples?: { n: number; seed: number };
  assetLabels?: [string, string];
}
```

- **Visual.** Ellipses 1.5px ink labelled with their mass (39% and 86%); samples `--s2` at 50%; the regression line `--s3`; the major axis dashed `--text-muted` and labelled, so the two are never confused; the conditional band `--s3` at 20%; the direction vector a `--manip` arrow; its shadow an `--s6` segment with a small histogram; the portfolio curve `--s3` with its minimum marked.
- **Motion.** Direct. Show-why `regression-not-major-axis` pulses each line with its label, 600ms. Show-why `sign-flip` reflects half the points across the $y$ axis to form an X, 600ms.
- **Reduced motion.** Static highlights; before-and-after for the flip.
- **Accessibility.** Table of $\Sigma$, conditional parameters and portfolio points; "Correlation 0.6. At x = 1, Y has mean 0.6 and SD 0.8."
- **Tutor hooks.** Describe: "σx 1, σy 1, ρ 0.6. Slice at x = 1.5: conditional mean 0.9, SD 0.8. Mode: conditional." Ids: `handle:sx`, `handle:sy`, `handle:rho`, `ellipse:1`, `ellipse:2`, `line:regression`, `line:major-axis`, `slice`, `band:conditional`, `handle:w`, `shadow`, `curve:portfolio`, `point:min-var`.
- **Performance.** Ellipses analytic; samples in canvas above 1,500 points.
- **Artifact and web.** No difference.
- **Generators.** Conditional-normal items; combination variances; minimum-variance weights with tidy answers; correlation from a picture.
- **Misconceptions.** `regression-line-is-major-axis`, `correlated-variances-add`, `sds-add`, `normal-marginals-uncorrelated-independent`.

#### 6.3.6 `cond-expectation`: Conditional expectation

**Composite · P0 · D3.** $E[Y \mid X]$ as slice means, as a random variable, and as the best predictor; Adam's and Eve's laws.

- **Purpose.** Group $Y$ by slices of $X$ and average each: that function of $X$ is $E[Y \mid X]$. Collapse every point to its slice mean and the result is a random variable whose average is $E[Y]$ (Adam's law). The variance of $Y$ splits into the average within-slice variance and the variance of the slice means (Eve's law). Among all functions of $X$, the slice means minimise squared error; the learner tries to beat them and cannot.
- **Serves.** 1.5.6 L1 to L6, L8.
- **Uses.** `plot-axes`, `marks` (scatter, slice boundaries, step function, stacked bars), `region-selector` (slices), `draggable-point` (one prediction handle per slice), `stepper` (collapse), `filtration-tree` (linked discrete version), `tex-terms`.
- **Interactions.**
  - Pointer: drag each slice's prediction handle; readout of mean squared error; Show slice means; Collapse; bin-width slider for continuous $X$; Build Eve bar.
  - Keyboard: prediction handles are sliders; buttons; slider.
- **State.** `{ bins: number[]; predictions: number[]; collapsed: boolean; showMeans: boolean; eve: boolean }`.
- **Answers and checks.** `numeric` ($E[Y \mid X = x]$, $E[Y]$, Eve components), `state` (predicate `slice-means-fit`), `expression` ($E[Y \mid X]$ for a given joint), `choice`.
- **Config.**

```ts
interface CondExpectationConfig {
  data: Vec2[] | { joint: JointSpec; n: number; seed: number }
      | { groups: { label: string; values: number[] }[] };
  bins?: number | number[];
  show: ('slice-means' | 'collapse' | 'eve' | 'mse' | 'linear-fit' | 'projection')[];
  task?: 'predict' | 'compute' | 'adam' | 'eve';
}
```

- **Visual.** Points 4px ink; slice boundaries `--line`; slice means `--s3` segments; prediction handles `--manip`; collapsed points `--s3`; the Eve bar stacks "within" in `--s2` and "between" in `--s3` with labels and values; the linear fit dashed `--s6`.
- **Motion.** Collapse slides each point vertically to its slice mean over 600ms `--ease-morph` (a consequence of the tap). The Eve bar grows over 400ms.
- **Reduced motion.** Before-and-after.
- **Accessibility.** Table view: slice range, count, mean, variance; "Your predictions: mean squared error 2.41; slice means give 2.07".
- **Tutor hooks.** Describe: "8 slices. Predictions set: 8 of 8. MSE 2.41 (slice means 2.07). Collapsed: no." Ids: `slice:<k>`, `handle:pred:<k>`, `mean:<k>`, `point:<i>`, `bar:within`, `bar:between`, `readout:mse`. Secret: the slice means.
- **Performance.** Canvas above 1,500 points; at most 20 slices.
- **Artifact and web.** No difference.
- **Generators.** Discrete joint tables with conditional expectations; random-sum and two-stage items (Poisson number of claims with random sizes); Eve's law numeric items.
- **Misconceptions.** `cond-exp-is-a-number`, `average-of-averages-unweighted`, `variance-of-means-is-total`.

### 6.4 Chains, walks and interview patterns

#### 6.4.1 `geo-prob`: Geometric probability

**Composite · P0 · D4.** Uniform points in an interval, a square, a disc or a needle's configuration space; events as regions; probability as area.

- **Purpose.** Two independent uniforms are one uniform point in the unit square, so any event about them is a region and its probability is its area. The learner drags the point $(X, Y)$ and sees the story move with it: two arrival times on a clock for the meeting problem, two cut marks on a stick for the broken stick. They build the event from inequality chips, get the exact area, and confirm with darts. Buffon's needle uses the (distance, angle) rectangle with a sine boundary. Bertrand's paradox shows three chord-drawing mechanisms giving $\frac{1}{3}$, $\frac{1}{2}$ and $\frac{1}{4}$.
- **Serves.** 1.5.5 L5; 1.5.9 L7, L8, L9.
- **Uses.** `plot-axes` (equal aspect), `region-selector` (half-plane cells), `draggable-point` (the sample point; parameter handles such as the meeting window $w$), `marks` (`region`, scatter, `curve`, labels), `slider`, `sim-runner` (darts), `expression-entry` (typed constraints), `numeric-entry`.
- **Interactions.**
  - Pointer: drag the sample point and watch the story inset; add a constraint from the palette or type one ("abs(x - y) < 0.25"); tap cells of the arrangement to include or exclude them; drag $w$; Throw 1,000 darts; in Bertrand mode switch between the three methods.
  - Keyboard: the sample point is a 2D handle; cells are a roving grid toggled with Space; constraint chips are buttons; sliders.
- **State.** `{ constraints: string[]; selectedCells: Id[]; point: Vec2; params: Record<string, number>; darts: { seed: number; n: number; inside: number } }`.
- **Answers and checks.** `probability` (area), `set` (cells), `expression` (probability as a function of $w$, such as $1 - (1 - w)^2$), `state` (predicate `region-equals`).
- **Config.**

```ts
interface GeoProbConfig {
  space: 'unit-interval' | 'unit-square' | 'disc' | 'buffon' | 'bertrand';
  story?: 'meeting' | 'broken-stick' | 'buffon' | 'bertrand' | 'none';
  constraints?: string[];               // given constraints; learner adds more when editable
  editable: 'none' | 'chips' | 'typed' | 'cells';
  params?: Record<string, [min: number, max: number, step: number, value: number]>;
  darts?: number[];
  task?: 'build-region' | 'area' | 'formula';
}
```

- **Visual.** The space outlined in 2px ink; boundaries 1.5px ink labelled with their equations; a learner-built region `--manip-wash` with a 2px `--manip` edge; given regions `--s3` at 25%; darts inside `--s3` filled and outside `--text-muted` hollow, so shape also separates them; the sample point `--manip`; the story inset (clock or stick) beside the square on desktop and above it on mobile, linked live to the point.
- **Motion.** Dragging the point moves the inset on the same frame. Darts fill in batches.
- **Reduced motion.** Darts appear at once.
- **Accessibility.** The region is described as inequalities with its area; the point announces both views ("X 0.30, Y 0.70: pieces 0.30, 0.40, 0.30, a triangle"); darts summarised as counts.
- **Tutor hooks.** Describe: "Broken stick. Point (0.30, 0.70): triangle yes. Region built: x < 0.5, y > 0.5, y - x < 0.5 (area 0.125). Darts: none." Ids: `region`, `constraint:<i>`, `boundary:<i>`, `point:sample`, `inset`, `darts`, `slider:<param>`, `cell:<id>`. Secret: target region and area.
- **Performance.** Clipping up to 10 constraints is trivial; curved boundaries sampled at 200 points; up to $10^5$ darts on canvas.
- **Artifact and web.** No difference.
- **Generators.** Meeting-problem variants (window, unequal intervals, one person waits longer); threshold events on $\max$, $\min$ and sums; broken-stick variants (triangle, longest piece under a half); all with exact rational areas from `geom`.
- **Misconceptions.** `forget-the-other-order`, `bertrand-has-one-answer`, `area-on-wrong-space`.

#### 6.4.2 `game-lab`: Game lab

**Composite · P0 · D4 (Kelly mode P2, F).** Play a probability game by hand, then simulate a policy, then compute its exact value.

- **Purpose.** Interview games teach expectation, conditioning and optimal stopping better than any formula sheet. Each game is a registered module with its round logic, the decisions offered, the policy parameters, an exact value (closed form or backward induction) and a seeded policy simulator.
- **Games.**
  - `monty-hall`: standard; ignorant host; $n$ doors with $k$ opened.
  - `dice-stop`: roll up to $m$ times and keep the last roll; thresholds per stage; values by backward induction ($3.5$, then $4.25$, then $4\frac{2}{3}$ for a six-sided die).
  - `secretary`: $n$ candidates in random order; look at the first $r$, then take the first better one; optimum near $r = n/e$.
  - `two-envelopes`: where the "always switch" argument breaks.
  - `st-petersburg`: the running average never settles.
  - `penney`: choose a pattern after the opponent; linked to `trial-strip`.
  - `kelly-coin` (P2): bet a fraction $f$ of wealth on a favourable coin; log-wealth growth; over-betting ruin.
- **Serves.** 1.5.2 L13; 1.5.3 L13, L19; 1.5.9 L10 to L13; 3.3 betting games (P2, cross-cluster).
- **Uses.** `chance-object` (doors, dice, cards, envelopes, coins), `sim-runner` (`policy`), `stepper` (backward induction stages), `slider` (thresholds, look-only fraction, Kelly fraction), `data-table` (value table), `marks` (running-average trace, wealth paths), `choice-cards` (decisions in hand play).
- **Interactions.**
  - Pointer: in hand play, tap a door, Stick or Switch, Roll again or Stop; in policy mode set thresholds and Run 100 or 10,000 rounds; in induction mode fill each stage's value starting from the last.
  - Keyboard: decisions are buttons; sliders; the stepper keys; value cells are numeric fields.
- **State.** `{ game; params; hand: RoundRecord[]; policy: Record<string, number | string>; simulated: { rounds: number; total: number; mean: number }; values?: Record<string, string> }`.
- **Answers and checks.** `numeric` and `probability` (exact values, win chances, thresholds), `choice` (stick or switch; which policy), `policy` (the policy's exact value within tolerance of the optimum), `ordering` (rank policies by value).
- **Config.**

```ts
interface GameLabConfig {
  game: 'monty-hall' | 'dice-stop' | 'secretary' | 'two-envelopes' | 'st-petersburg' | 'penney' | 'kelly-coin';
  params: Record<string, unknown>;          // doors, rolls, die size, n candidates, edge
  modes: ('hand' | 'policy' | 'induction')[];
  rounds: number[];
  predictFirst?: CheckSpec;
}
```

- **Visual.** Game objects from `chance-object` at the top; decisions as secondary pills, never styled as Check; tallies with tabular figures; policy sliders `--manip`; the simulated mean trace `--s2` with the exact value as dashed ink; the induction table with one column per stage, filled cells `--manip` until graded; Kelly wealth paths on canvas, ink at 25% with the median path `--s2`.
- **Motion.** `chance-object` animations in hand play; policy batches fill the trace.
- **Reduced motion.** Instant.
- **Accessibility.** Every decision is a button; "Monty Hall, 3 doors, host knows. Hand play: 7 rounds; switched 4 times and won 3; stuck 3 times and won 1. Policy always switch: 10,000 rounds, won 0.668; exact two thirds."
- **Tutor hooks.** Describe as above. Ids: `door:<i>`, `die`, `decision:<id>`, `slider:<policy>`, `trace`, `line:exact`, `value:<stage>`, `path:median`. Secret: exact values and the optimal policy.
- **Performance.** Policy runs of $10^5$ rounds in the worker; Kelly paths up to 200 drawn.
- **Artifact and web.** No difference.
- **Generators.** Dice-stopping variants (die size, number of rolls, a cost per roll); Monty variants; secretary values of $n$ with the optimum by dynamic programming; Kelly items (P2).
- **Misconceptions.** `monty-fifty-fifty`, `ignorant-host-same-as-informed`, `envelopes-always-switch`, `expectation-is-enough`, `bet-more-win-more` (P2).

#### 6.4.3 `first-step-solver`: First-step solver

**Composite · P0 · D4.** First-step analysis as a method: one unknown per state, one equation per state, solved exactly and checked by simulation.

- **Purpose.** Most interview probability questions with "until" or "first" in them are first-step problems. The learner gives each state an unknown (probability of reaching a target first, or expected steps), builds each state's equation by tapping its outgoing edges (each tap adds $p_e x_{\text{target}}$; a "+1" chip adds a step for expected-time problems), fixes boundary values at absorbing states, solves, and verifies with walkers. Pattern problems generate their automaton from the pattern, including the overlap rule (after HH, a T in HHT's automaton falls back correctly).
- **Problems.** Gambler's ruin with any $p$; expected tosses to HH, HT, HHT, or any pattern over a coin or a die; alternating turns ("first to roll a six"); tennis from deuce; two wins in a row; expected rolls until the sum reaches $n$; drunkard near a cliff.
- **Serves.** 1.5.2 L14; 1.5.3 L13; 1.5.6 L7; 1.5.8 L8; 1.5.9 L4.
- **Uses.** `node-graph`, `token-tray` (term chips), `expression-entry` (typed equations as an alternative), `matrix` (the system and its solution), `sim-runner` (`markov-walk`), `tex-terms`, `stepper` (substitution steps after Solve).
- **Interactions.**
  - Pointer: tap a state to open its equation row; tap an outgoing edge to add its term; tap "+1"; set a boundary value on an absorbing state; Solve (enabled once every state has an equation); Simulate 10,000 walks.
  - Keyboard: graph navigation from `node-graph`; Enter opens the focused state's equation; its outgoing edges appear as buttons in the equation editor; T switches to typed entry.
- **State.** `{ equations: Record<StateId, { terms: { coef: Entry; target: StateId | 'one' }[] }>; boundary: Record<StateId, Entry>; solved?: Record<StateId, string>; sim?: { seed: number; walks: number; mean: number } }`.
- **Answers and checks.** `state` (predicate `system-equivalent`), `numeric` and `probability` (the start state's value), `expression` (a general formula in $p$ and $N$), `choice`.
- **Config.**

```ts
interface FirstStepSolverConfig {
  chain: NodeGraphConfig
       | { pattern: string; alphabet: { symbol: string; p: Entry }[] }
       | { preset: 'gamblers-ruin'; N: number; p: Entry; start: number }
       | { preset: 'alternating'; pWin: Entry[] };
  unknown: 'hit-prob' | 'expected-time' | 'expected-reward';
  target?: string[];
  start: string;
  editable: 'equations' | 'diagram-and-equations' | 'none';
  simulate?: boolean;
}
```

- **Visual.** The `node-graph` with each state's unknown ($x_A$) in KaTeX inside the node; absorbing states double-outlined with their boundary value; the equation panel with one row per state and term chips in `lip-token` style, `--manip` until graded; after Solve, values appear in the nodes in `--s3`; walkers `--s2`.
- **Motion.** Tapping an edge sends its term chip from the edge to the equation row (200ms, a consequence). Solve can play its substitution steps through the stepper.
- **Reduced motion.** Chips appear in place.
- **Accessibility.** Equations as text ("x zero equals 1 plus one half x H plus one half x zero"); states as buttons; walker results announced after each batch.
- **Tutor hooks.** Describe: "States 0, H, HH (absorbing). Unknown: expected tosses. x0 = 1 + ½xH + ½x0 entered; xH missing; boundary xHH = 0 set." Ids: `node:<id>`, `edge:<a>-<b>`, `eq:<id>`, `term:<id>:<k>`, `chip:one`, `solve`, `sim`. Secret: the solution vector.
- **Performance.** Exact BigInt elimination for up to 30 unknowns; pattern automata up to 10 states; walkers in the worker.
- **Artifact and web.** No difference.
- **Generators.** Patterns of length 2 to 4 over coins and dice; gambler's ruin parameters; alternating-turn games; each answer from the exact solver and cross-checked by simulation in CI.
- **Misconceptions.** `forget-the-plus-one`, `restart-from-zero-after-partial-match`, `missing-boundary`.

#### 6.4.4 `markov-chain`: Markov chain lab

**Composite · P0 · D4 (Metropolis mode P2).** Diagram and matrix together, with a walker, a population, classification and stationary distributions.

- **Purpose.** Every row of $P$ is "where next from here". One walker's long-run visit frequencies and a whole population's distribution $\pi_0 P^n$ approach the same stationary $\pi$ (for an irreducible, aperiodic chain), and $\pi P = \pi$ can be checked state by state. Classification: communicating classes, recurrent and transient states, period. Detailed balance as flows that cancel edge by edge. Random walks on graphs (stationary mass proportional to degree), PageRank with teleporting, absorbing chains with the fundamental matrix $(I - Q)^{-1}$, and a credit-rating migration preset. Metropolis (P2) designs a chain for a target distribution.
- **Serves.** 1.5.8 L1 to L9.
- **Uses.** `node-graph`, `matrix` (row-stochastic editing), `mass-editor` (row popover, initial distribution), `sim-runner` (`markov-walk`), `marks` (bars per state, visit-frequency bars), `stepper` ($n$ steps), `region-selector` (class selection over nodes), `linear-dynamics` and `eigen-finder` (linked views), `first-step-solver` (absorbing link).
- **Interactions.**
  - Pointer: edit a row through its node's popover or the matrix; Step and Play the walker; drag the initial distribution bars and Step the population; select states into classes and label each class recurrent or transient; enter $\pi$ and tap Test to see $\pi P$ against $\pi$ per state; toggle flows; slide the PageRank teleport probability $\alpha$.
  - Keyboard: `node-graph` and `matrix` keys; S steps; P plays and pauses; G groups the selected states into a class.
- **State.** `{ P: Entry[][]; pi0: Entry[]; n: number; walker: { at: Id; recent: Id[]; visits: number[]; steps: number }; classes?: Id[][]; enteredPi?: string[]; alpha?: number }`.
- **Answers and checks.** `matrix` (transition matrix equals a target; `row-stochastic`), `numeric` and `probability` ($P^n$ entries, stationary probabilities, expected visits, absorption probabilities), `state` (predicates `is-stationary`, `detailed-balance`, `class-partition`), `choice` (recurrent, transient, periodic).
- **Config.**

```ts
interface MarkovChainConfig {
  states: { id: string; label: string }[];
  P: Entry[][] | { preset: 'weather' | 'ehrenfest' | 'ratings' | 'graph-walk' | 'pagerank' | 'gamblers-ruin';
                   params?: Record<string, unknown> };
  editable: ('P' | 'pi0')[];
  views: ('diagram' | 'matrix' | 'population' | 'walker' | 'flows' | 'eigen')[];
  nMax: number;
  alpha?: number;
  task?: 'step' | 'classify' | 'stationary' | 'absorb' | 'design';
}
```

- **Visual.** Nodes filled by $\pi_n$ on `--seq-1` to `--seq-6` with value labels; the walker an `--s2` token; long-run visit frequencies as `--s2` bars beside stationary `--s3` stems (empirical against theory); the matrix shows row sums; learner-selected classes get a dashed `--manip` hull; in flows view each edge's width is proportional to $\pi_i P_{ij}$ and balanced pairs are marked with an equals glyph.
- **Motion.** Walker steps 240ms; population steps 320ms; Play runs at four steps a second. All are demonstrations started by the learner.
- **Reduced motion.** Jumps; Play steps without interpolation.
- **Accessibility.** The matrix is the table view; each state is described with its outgoing row and current probability; "Walker at B after 57 steps; visits A 40, B 9, C 8".
- **Tutor hooks.** Describe: "3 states. P rows: A (0.9, 0.1, 0), B (0.5, 0, 0.5), C (0, 0.5, 0.5). π10 = (0.71, 0.14, 0.15). Walker at B after 57 steps." Ids: `node:<id>`, `edge:<a>-<b>`, `cell:<i>,<j>`, `row:<i>`, `walker`, `bar:<id>`, `class:<k>`, `pi:<id>`, `slider:alpha`, `step`. Secret: $\pi$ and the classes.
- **Performance.** Diagrams up to 12 states; matrix powers trivial; $10^6$ walker steps in the worker for long-run frequencies.
- **Artifact and web.** No difference.
- **Generators.** Chains with rational stationary distributions built by detailed balance (choose $\pi$ and symmetric edge weights, then normalise rows); classification puzzles with known classes; absorbing chains with tidy fundamental matrices; small PageRank graphs.
- **Misconceptions.** `stationary-means-stopped`, `rows-or-columns`, `periodic-chain-converges`, `irreducible-means-aperiodic`.

#### 6.4.5 `lattice-walk`: Lattice walk

**Composite · P0 · D4.** Simple random walk paths on the (time, position) lattice: counting, reflection, ballots and Catalan numbers.

- **Purpose.** A path of $n$ steps ending at $k$ is a choice of which $\frac{n+k}{2}$ steps go up, so there are $\binom{n}{(n+k)/2}$ of them. Reflecting the part of a path before its first touch of a barrier gives a bijection that counts touching paths, which proves the ballot theorem, counts Catalan paths, and gives the distribution of the running maximum. Simulation adds return-to-origin rates and the arcsine law for time spent positive.
- **Serves.** 1.5.9 L1, L2, L3, L5.
- **Uses.** `plot-axes` (integer lattice), `marks` (lattice dots, paths, barrier line, labels), `draggable-point` (endpoint, barrier level), `stepper` (reflection), `sim-runner` (`lattice-walk`), `pascal-triangle` (counts), `path-simulator` (scaling link).
- **Interactions.**
  - Pointer: build a path with Up and Down buttons; drag the endpoint to $(n, k)$ for its count; drag the barrier; tap Reflect at first touch; Enumerate all paths for $n \le 12$; Run 10,000 walks.
  - Keyboard: Up and Down arrows add steps; Backspace removes one; endpoint and barrier are sliders; R reflects.
- **State.** `{ path: (1 | -1)[]; endpoint: [number, number]; barrier?: number; reflected: boolean; sim?: { seed: number; runs: number } }`.
- **Answers and checks.** `numeric` (path counts, probabilities), `expression` (count formulas), `state` (predicate `path-property`), `choice`.
- **Config.**

```ts
interface LatticeWalkConfig {
  n: number; start: number;
  endpoint?: [number, number];
  barrier?: { level: number; editable: boolean };
  mode: 'build' | 'count' | 'reflect' | 'ballot' | 'catalan' | 'max' | 'arcsine';
  simulate?: boolean;
}
```

- **Visual.** Lattice dots `--line`; the learner's path 2.5px `--manip`; enumerated paths ink at low opacity; the reflected part `--s6` dashed; the barrier dashed ink with its level; the first touch marked by an ink ring.
- **Motion.** Reflect mirrors the pre-touch segment over 600ms `--ease-morph`.
- **Reduced motion.** Before-and-after.
- **Accessibility.** The path reads as "up, up, down, up"; counts table; "Paths from 0 to 2 in 6 steps: 15; touching minus 1: 6".
- **Tutor hooks.** Describe: "n = 6, start 0, endpoint (6, 2). Barrier at −1. Learner path U U D U D U touches the barrier: no." Ids: `path`, `step:<i>`, `endpoint`, `barrier`, `touch`, `path:reflected`, `count`. Secret: counts asked for.
- **Performance.** Up to 4,096 enumerated paths drawn as one canvas bundle; simulation in the worker.
- **Artifact and web.** No difference.
- **Generators.** Path counts with and without barriers; ballot items; Catalan items; first-passage probabilities; all exact.
- **Misconceptions.** `reflect-the-wrong-part`, `all-endpoints-equally-likely`.

---

## 7. Statistics composites (1.6)

All 9 are P1, wave E, unless a mode says otherwise.

### 7.1 `estimator-compare`: Estimator race

**Composite · P1 · E.** Two or three estimators of the same parameter, compared by their sampling distributions.

- **Purpose.** Bias is where a sampling distribution centres relative to $\theta$; variance is its spread; $\text{MSE} = \text{bias}^2 + \text{variance}$. The learner sees that unbiased is not the same as best (dividing a sum of squares by $n + 1$ beats $n - 1$ on MSE for normal data), that the median beats the mean on heavy tails, that consistency is concentration as $n$ grows, and that no unbiased estimator crosses the Cramér-Rao line. The German tank problem compares $\max$-based and mean-based estimators of a population size.
- **Serves.** 1.6.1 L3 to L9; 1.6.5 L13.
- **Uses.** `sampling-lab` engine (shared worker model), `sim-runner`, `marks` (overlaid `hist`, truth line, stacked MSE bars, MSE curves), `slider` ($n$, $\theta$, shrinkage factor $c$), `choice-cards` (estimator chips), `draggable-point` (predicted bias and spread markers), `tex-terms`.
- **Interactions.**
  - Pointer: choose up to three estimators; set $\theta$ (hidden in quizzes); slide $n$; Run 1,000 samples; drag predicted centre markers before running; switch to the MSE-against-$n$ or MSE-against-$c$ view.
  - Keyboard: chips; sliders; markers are sliders.
- **State.** `{ theta: number; n: number; estimators: Id[]; seed: number; results: Record<Id, { mean: number; variance: number; mse: number }>; predictions?: Record<Id, number> }`.
- **Answers and checks.** `numeric` (exact bias, variance, MSE from formulas, never from the simulation), `expression` (bias formulas such as $-\frac{\theta}{n+1}$), `choice` (which estimator wins and why), `point` (predictions).
- **Config.**

```ts
interface EstimatorCompareConfig {
  model: { dist: DistSpec; param: string };
  thetaRange: [number, number];
  estimators: ('mean' | 'median' | 'max' | 'max-adjusted' | 'two-mean' | 'mom' | 'mle'
             | 'var-n' | 'var-n-1' | 'var-n+1' | 'shrink' | 'ols' | 'other-linear')[];
  n: number;
  show: ('hist' | 'mse-bars' | 'mse-vs-n' | 'mse-vs-c' | 'crlb')[];
  hideTruth?: boolean;
}
```

- **Visual.** Estimator histograms in `--s2`, `--s6` and `--s4` with direct labels; the truth as dashed ink labelled $\theta$; MSE bars stacked: bias squared hatched, variance solid, in the estimator's colour; the Cramér-Rao bound as a dashed ink curve.
- **Motion.** Batches fill.
- **Reduced motion.** Instant.
- **Accessibility.** Table view: estimator, mean, bias, variance, MSE (simulated and exact side by side).
- **Tutor hooks.** Describe: "θ = 100 (hidden), n = 5. Max-adjusted: mean 100.2, SD 15.1. Two-mean: mean 99.8, SD 25.6. 1,000 samples." Ids: `est:<id>`, `hist:<id>`, `line:truth`, `bar:<id>:bias`, `bar:<id>:var`, `curve:mse`, `curve:crlb`, `slider:n`, `slider:theta`. Secret: $\theta$ and exact MSEs.
- **Performance.** $10^4$ samples with $n \le 500$ in the worker.
- **Artifact and web.** No difference.
- **Generators.** Bias and variance formula items; German tank items with given serials; divisor items.
- **Misconceptions.** `unbiased-is-best`, `n-minus-one-is-magic`, `consistent-means-unbiased`.

### 7.2 `likelihood-lab`: Likelihood lab

**Composite · P1 · E.** The likelihood as a function of the parameter, built from the data's density heights.

- **Purpose.** Fix the data and move $\theta$: the model density slides over the data, each point's density height changes, and their product (or the sum of their logs) is $L(\theta)$, plotted in a second panel. The peak is the MLE. Curvature at the peak gives the standard error through the observed information. A uniform model shows a boundary maximum where the derivative is not zero. Two parameters give a contour map. A horizontal cut 1.92 below the peak gives a likelihood interval and the likelihood-ratio test.
- **Serves.** 1.6.1 L10; 1.6.2 L1 to L8; 1.6.3 L7; 1.6.4 L10.
- **Uses.** `plot-axes` twice (data with the model; parameter axis with $\ell(\theta)$), `marks` (`rug`, `curve`, `stems` from each point to the curve, contours, cut line), `draggable-point` ($\theta$ handle; the $(\mu, \sigma)$ point on the contour map), `slider`, `surface-explorer` (two-parameter view), `tex-terms` ($\ell(\theta) = \sum_i \ln f(x_i; \theta)$ live), `derivation`.
- **Interactions.**
  - Pointer: drag $\theta$ on the parameter axis (or the model directly); toggle $L$ and $\ln L$; toggle the curvature parabola; drag the cut; in two-parameter mode drag the point on the contour map; drag data points in explore mode.
  - Keyboard: handles are sliders; toggles.
- **State.** `{ theta: number[]; logScale: boolean; data: number[]; showCurvature: boolean; cut?: number }`.
- **Answers and checks.** `numeric` (MLE, standard error, likelihood ratio), `point` (the handle at the MLE within tolerance), `expression` (the MLE formula: $\frac{k}{n}$, $\bar x$, $\max_i x_i$), `interval` (a likelihood interval), `choice`.
- **Config.**

```ts
interface LikelihoodLabConfig {
  model: 'bernoulli' | 'binomial' | 'poisson' | 'exponential' | 'normal-mu' | 'normal-mu-sigma'
       | 'uniform-theta' | 'regression';
  data: number[] | { generate: { n: number; theta: number[]; seed: number } };
  params: { name: string; range: [number, number]; step: number }[];
  show: ('point-densities' | 'product' | 'log' | 'curvature' | 'contours' | 'lr-cut')[];
  task?: 'find-mle' | 'se' | 'interval' | 'lr-test';
}
```

- **Visual.** Data as an ink rug; the model density `--s3`; each point's height as an `--s2` stem; the log-likelihood `--s3` on the parameter panel with the current $\theta$ marked; the $\theta$ handle `--manip`; the parabola `--s6` dashed; the cut dashed ink; the MLE marker revealed after Check.
- **Motion.** Direct. Show-why `boundary` slides $\theta$ below the largest observation, where that point's stem drops to zero and $L$ collapses, 600ms. Show-why `curvature` draws the parabola, 480ms.
- **Reduced motion.** Before-and-after.
- **Accessibility.** Table view of $\theta$ on a grid against $\ell(\theta)$; data list; "theta 0.4: log-likelihood −6.73".
- **Tutor hooks.** Describe: "Bernoulli, 7 heads in 10. θ = 0.55: log-likelihood −6.27. Log scale on." Ids: `handle:theta`, `curve:loglik`, `curve:model`, `stem:<i>`, `readout:loglik`, `parabola`, `cut`, `contour`. Secret: the MLE.
- **Performance.** $\ell$ on a 400-point grid recomputed only when the data change; a $\theta$ drag costs $O(n)$.
- **Artifact and web.** No difference.
- **Generators.** Data with tidy MLEs; information and standard-error items; likelihood-ratio items.
- **Misconceptions.** `likelihood-is-probability-of-theta`, `mle-is-unbiased`, `derivative-is-always-zero-at-mle`, `why-logs` (product underflow).

### 7.3 `ci-ladder`: Confidence interval ladder

**Composite · P1 · E.** Many intervals from many samples, stacked, with the ones that miss the truth counted.

- **Purpose.** "95%" describes the method: about 95 of 100 intervals built this way cover $\mu$. The learner watches coverage hold for a $t$ interval, fail when $z$ is used with $s$ at small $n$, fail for Wald intervals for a proportion near 0 or 1 (exact coverage curve), and recover with Wilson. Your-interval mode asks the Trap question about one realised interval.
- **Serves.** 1.6.3 L1 to L6; 1.6.4 L11; 1.6.5 L7 (coverage under violated assumptions, fed from `regression-lab`).
- **Uses.** `sim-runner` (`ci`), `marks` (`intervals`, truth line, coverage curve), `slider` ($n$, level, truth), `choice-cards` (method), `number-line` (one realised interval), `dist-explorer` (critical values), `tex-terms`.
- **Interactions.**
  - Pointer: Run 1, 20, 100 or 1,000 intervals; the ladder shows the latest 100; switch method; slide $n$ and the level; show the exact coverage curve for proportions; predict coverage before running.
  - Keyboard: buttons; sliders; chips.
- **State.** `{ method; n; level; truth; seed; latest: { lo: number; hi: number; covers: boolean }[]; hits: number; total: number }`.
- **Answers and checks.** `numeric` (an interval's endpoints from given data, margin of error, required $n$, predicted coverage), `interval` (the learner's computed interval), `choice` (interpretations).
- **Config.**

```ts
interface CiLadderConfig {
  model: 'normal-mean' | 'proportion' | 'exponential-mean' | 'difference-means' | 'regression-slope';
  methods: ('z-known' | 'z-with-s' | 't' | 'wald' | 'wilson' | 'agresti-coull' | 'bootstrap-percentile')[];
  n: number; level: number; truth: number;
  hideTruth?: boolean;
  show: ('ladder' | 'coverage-curve' | 'your-interval' | 'width-vs-n')[];
  predictFirst?: CheckSpec;
}
```

- **Visual.** Covering intervals 1.5px ink; missing intervals 2.5px `--s2` with a cross glyph at the right end; centre dots; the truth dashed ink; the coverage counter beside a nominal-level line; the coverage curve `--s3` against a dashed nominal line.
- **Motion.** New intervals enter at the top and the ladder scrolls within 200ms per batch frame.
- **Reduced motion.** The ladder updates at once.
- **Accessibility.** Table of the latest intervals; "100 intervals, 95% t, n = 10: 94 cover the truth".
- **Tutor hooks.** Describe: "Normal mean, t at 95%, n = 10. 100 run, 94 cover. Truth hidden." Ids: `interval:<i>`, `line:truth`, `counter`, `curve:coverage`, `slider:n`, `slider:level`, `method:<id>`. Secret: the truth.
- **Performance.** 100 intervals in SVG; $10^5$ simulated in the worker; the proportion coverage curve computed exactly by summing binomial probabilities over 200 values of $p$.
- **Artifact and web.** No difference.
- **Generators.** Interval computations from small data sets with table critical values; sample-size items; interpretation items.
- **Misconceptions.** `ci-is-probability-for-this-interval`, `z-at-small-n`, `wald-near-boundary`, `wider-is-worse`.

### 7.4 `test-lab`: Test lab

**Composite · P1 · E (simulated Dickey-Fuller null P2, F).** Null and alternative distributions, critical regions, error rates, power and p-values on one canvas.

- **Purpose.** A test is a rule: reject when the statistic lands in a region chosen to have probability $\alpha$ under the null. Dragging the critical value trades $\alpha$ against $\beta$; moving the effect size or $n$ moves the alternative and changes power. A p-value is the null tail area beyond the observed statistic. The Neyman-Pearson view orders outcomes by likelihood ratio. Tests and intervals are duals. Simulated nulls handle statistics without a textbook distribution (Dickey-Fuller, permutation).
- **Tests.** $z$ (mean, proportion), one-sample, Welch and paired $t$, $\chi^2$ (variance, goodness of fit, independence through `contingency-table`), $F$ (regression), exact binomial, and simulated nulls: permutation (P1) and Dickey-Fuller (P2).
- **Serves.** 1.6.4 L1 to L5, L7, L9 to L11; 1.6.5 L14; 2.2.1 L7, L8; 2.2.2 L4; 2.2.5 L3.
- **Uses.** `plot-axes`, `marks` (`curve`, `region` with hatch fills, labels), `draggable-point` (critical handles; observed-statistic marker in predict tasks), `slider` (effect, $n$, $\alpha$, $\sigma$), `choice-cards` (test, sidedness), `dist-explorer` (shared distribution code), `sim-runner` (simulated nulls and simulated power), `tex-terms` (the statistic with the data substituted).
- **Interactions.**
  - Pointer: drag a critical value ($\alpha$ follows) or set $\alpha$ (the critical value follows); slide effect size and $n$; switch one- or two-sided; place the observed statistic from data or generate a sample; toggle the p-value shading; open the power-curve panel.
  - Keyboard: handles and sliders; chips; P toggles the p-value region.
- **State.** `{ test; alpha; sided; effect; n; critical: number[]; observed?: number; showP: boolean; powerCurve: boolean }`.
- **Answers and checks.** `numeric` (statistic, p-value, critical value, power, required $n$), `interval` (the rejection region), `point` (critical handle for a given $\alpha$), `choice` (reject or not; which error).
- **Config.**

```ts
interface TestLabConfig {
  test: 'z-mean' | 'z-prop' | 't-one' | 't-welch' | 't-paired' | 'chi2-var' | 'chi2-gof' | 'chi2-indep'
      | 'f-nested' | 'binom-exact' | 'simulated';
  null: Record<string, number>;
  alt?: Record<string, number>;
  alpha: number;
  sided: 'two' | 'left' | 'right';
  editable: ('alpha' | 'critical' | 'effect' | 'n' | 'sided')[];
  data?: number[] | { generate: { n: number; params: Record<string, number>; seed: number } };
  show: ('null' | 'alt' | 'alpha' | 'beta' | 'power' | 'p' | 'power-curve')[];
  simulatedNull?: { model: string; statistic: string; reps: number };
}
```

- **Visual.** Null curve `--s3` with a 20% fill; alternative `--s6` with a 20% fill; $\alpha$ regions `--s3` at 45% with diagonal hatch; $\beta$ region `--s6` at 35% with dots; critical lines `--manip` with handles; the observed statistic a solid ink line labelled ("t = 2.31"); the p-value tail cross-hatched in ink; labels "α 0.05", "β 0.29", "power 0.71".
- **Motion.** Direct. Show-why `p-is-not-posterior` hands over to an `icon-array` screen state; show-why `two-sided` mirrors the tail, 480ms.
- **Reduced motion.** Before-and-after.
- **Accessibility.** "Two-sided z test at 0.05: reject when the absolute value of z exceeds 1.96. Effect 0.5, n 25: power 0.71. Observed z 2.31, p 0.021."
- **Tutor hooks.** Ids: `curve:null`, `curve:alt`, `region:alpha`, `region:beta`, `handle:crit-left`, `handle:crit-right`, `marker:observed`, `region:p`, `curve:power`, `slider:<id>`. Secret: the p-value and decision asked for.
- **Performance.** Closed forms are trivial; simulated nulls in the worker ($10^4$ Dickey-Fuller regressions on $T = 100$ in well under a second [unverified]).
- **Artifact and web.** No difference.
- **Generators.** Test items with small data sets ($t$, $z$, $\chi^2$ tables); power and sample-size items; decision items.
- **Misconceptions.** `p-is-probability-null-true`, `fail-to-reject-means-accept`, `alpha-equals-p`, `significant-means-large`, `one-sided-after-looking`.

### 7.5 `multiple-testing`: Multiple testing

**Composite · P1 · E (strategy-zoo mode also serves 3.1 at P2).** Many tests at once: family-wise error, corrections, false discovery rate, forking paths and backtest overfitting.

- **Purpose.** Run $m$ tests at 5% and some will reject by chance: $P(\text{at least one}) = 1 - 0.95^m$. Bonferroni and Holm control the family-wise rate; Benjamini-Hochberg controls the false discovery rate by comparing sorted p-values with the line $\frac{i}{m}q$. Forking paths (choosing the best of $k$ analyses) inflate false positives. In the strategy zoo, the best in-sample Sharpe ratio of many noise strategies looks like skill and vanishes out of sample. Harvey, Liu and Zhu's argument for a $t$ hurdle near 3 for new factors follows.
- **Serves.** 1.6.4 L3, L12 to L15; 3.1 (P2, cross-cluster).
- **Uses.** `icon-array` (test cells), `marks` (sorted p-value `stems`, BH and Bonferroni lines, in-sample against out-of-sample scatter), `draggable-point` (BH line slope $q$), `slider` ($m$, share of real effects, effect size, $k$, number of strategies), `contingency-table` (truth against decision), `sim-runner`.
- **Interactions.**
  - Pointer: Run a batch of studies; choose a correction; drag the BH line; tap cells to mark which hypotheses BH rejects (a task); Reveal truth fills the outcome table; slide $k$ for forking paths; in the zoo, run $N$ strategies, tap the best in-sample one, then Reveal its out-of-sample result.
  - Keyboard: buttons; sliders; the cell grid is roving with Space to mark.
- **State.** `{ m; pi1; effect; seed; method; q?: number; alpha?: number; marked: Id[]; revealed: boolean; k?: number; N?: number; picked?: Id }`.
- **Answers and checks.** `numeric` (FWER, expected false positives, number of BH discoveries), `set` (exactly the hypotheses a procedure rejects), `choice`.
- **Config.**

```ts
interface MultipleTestingConfig {
  m: number; pi1: number; effect: number; alpha: number;
  methods: ('none' | 'bonferroni' | 'holm' | 'bh')[];
  mode: 'fwer' | 'corrections' | 'forking' | 'zoo';
  pValues?: number[];                    // fixed list for set tasks
  zoo?: { N: number; T: number; seed: number };
  hideTruth?: boolean;
}
```

- **Visual.** Cells outlined in ink; a rejected test carries a filled `--s2` dot; after Reveal, truly non-null cells are hatched `--s3`; the sorted p-value plot uses `--s2` stems, the BH line `--manip`, the Bonferroni line dashed ink; the zoo scatter puts in-sample Sharpe on $x$ and out-of-sample on $y$ with the picked strategy ringed.
- **Motion.** Sorting moves cells into p-value order over 480ms (a consequence of tapping Sort). Batches fill.
- **Reduced motion.** Instant.
- **Accessibility.** Sorted p-value table with each method's decision; "20 tests, none real: 1 rejected at 5% with no correction".
- **Tutor hooks.** Describe: "m = 100, 10 real, BH at q = 0.1: 12 discoveries. Truth hidden." Ids: `cell:<i>`, `line:bh`, `line:bonferroni`, `stem:<rank>`, `table:outcomes`, `point:best`, `slider:<id>`. Secret: which hypotheses are real.
- **Performance.** Up to 1,000 cells on canvas; the lowest 200 p-values drawn as stems; zoo of up to 1,000 strategies of 1,000 days in the worker.
- **Artifact and web.** No difference.
- **Generators.** BH and Holm set tasks on fixed p-value lists with exact decisions; FWER items; zoo items whose expected best Sharpe is stated by simulation in the explanation only, never graded.
- **Misconceptions.** `bonferroni-controls-fdr`, `best-backtest-is-skill`, `p-hacking-is-harmless`, `more-tests-same-error`.

### 7.6 `regression-lab`: Regression lab

**Composite · P1 · E (autocorrelated errors and HAC P2).** Fit, read, resample, break and diagnose linear regression.

- **Purpose.** Everything about OLS that a summary table hides: residuals and the $SST = SSR + SSE$ decomposition behind $R^2$; the sampling distribution of $\hat\beta$ that standard errors describe; confidence against prediction bands; what each assumption buys and what breaks when it fails (nonlinearity, heteroscedasticity, correlated errors, heavy tails), measured as the true coverage of a nominal 95% interval; diagnostics; two predictors with a fitted plane, Frisch-Waugh-Lovell, omitted-variable bias and collinearity; influence of single points.
- **Serves.** 1.6.5 L3 to L15; 2.2.1 L9 (spurious regression, with `coint-lab`).
- **Uses.** `plot-axes` (scatter, residual and diagnostic panels), `marks` (scatter, line, residual segments, squares, decomposition bars, `band`, `ellipse`, `stems` for Cook's distance), `draggable-point` (data points), `slider` (noise, $n$, curvature, fan, error correlation, predictor correlation), `sim-runner` (refits), `plot-3d` (plane), `matrix` ($X^\top X$, $\widehat{\mathrm{Cov}}(\hat\beta)$), `least-squares-fit` (geometry link), `qq-plot`, `ci-ladder` (coverage), `summary-table` (link), `tex-terms`.
- **Interactions.**
  - Pointer: drag points; toggle fitted line, residuals, squares and decomposition bars; New sample refits and adds the slope to a histogram; violation sliders; diagnostics tabs (residuals against fitted, QQ, scale-location, hat values and Cook's distance); two-predictor mode with an orbiting plane and an added-variable plot; drop or add $x_2$; switch standard errors between classical and HC types.
  - Keyboard: points are 2D handles; tabs; sliders; R refits.
- **State.** `{ data: { X: number[][]; y: number[] }; predictors: Id[]; shown: string[]; violations: Record<string, number>; seed: number; slopes: number[]; tab: string; cov: 'classical' | 'HC0' | 'HC1' | 'HC2' | 'HC3' }`.
- **Answers and checks.** `numeric` (coefficients, standard errors, $t$, $R^2$, fitted values, residuals, hat values), `interval` (a slope interval), `choice` (which assumption a plot shows broken; generated), `state` (place a point with high influence), `code` (via `summary-table`'s drill).
- **Config.**

```ts
interface RegressionLabConfig {
  data: { X: number[][]; y: number[]; names: string[] }
      | { generate: { n: number; beta: number[]; sigma: number; x: 'uniform' | 'normal' | 'correlated';
                      rho12?: number; violations?: { curve?: number; fan?: number; ar1?: number; tails?: number };
                      seed: number } };
  predictors: string[];
  show: ('fit' | 'residuals' | 'squares' | 'decomposition' | 'ci-band' | 'pi-band' | 'refits' | 'plane' | 'avplot')[];
  diagnostics?: ('resid-fitted' | 'qq' | 'scale-location' | 'influence')[];
  editable: ('points' | 'violations' | 'model' | 'cov')[];
  task?: string;
}
```

- **Visual.** Data ink (`--manip` when movable); fitted line `--s3`; residuals `--text-muted`; squares `--s2` at 15%; decomposition bars $SSR$ `--s3` and $SSE$ `--s2` summing to $SST$ in ink outline; confidence band `--s3` at 20%, prediction band `--s3` at 10% with dashed edges; the slope histogram `--s2` with the theoretical sampling density `--s6` dashed; reference lines dashed ink in diagnostics; Cook's distance stems with the $4/n$ line.
- **Motion.** Direct. Show-why keys: `omitted-variable` (the fitted line rotates as $x_2$ is dropped, 600ms); `fan` (highlights the widening residual spread); `influence` (a point drags the line with it).
- **Reduced motion.** Before-and-after.
- **Accessibility.** Table view of data, fitted values, residuals and hat values; "y on x, n = 50: intercept 1.02, slope 2.98, R squared 0.81, slope standard error 0.14".
- **Tutor hooks.** Ids: `point:<i>`, `line:fit`, `residual:<i>`, `bar:sst`, `bar:ssr`, `bar:sse`, `band:ci`, `band:pi`, `panel:<tab>`, `slider:<id>`, `hist:slopes`, `plane`. Secret: the true coefficients of generated data.
- **Performance.** OLS by QR from the `ols` service; one predictor uses closed forms during drags, $O(n)$ per frame; $10^4$ refits with $n \le 200$ in the worker.
- **Artifact and web.** No difference.
- **Generators.** Data with exact round coefficients by construction (residuals projected out of the column space, as `least-squares-fit` does); generated residual plots each with one named violation; omitted-variable items.
- **Misconceptions.** `r2-measures-truth`, `correlation-is-causation`, `significant-slope-means-good-model`, `x-must-be-normal`, `extrapolation-is-safe`, `regress-prices-not-returns`, `always-delete-outliers`.

### 7.7 `summary-table`: Regression summary explainer

**Composite · P1 · E.** The statsmodels OLS summary, with every number a button that explains itself on this data.

- **Purpose.** The 1.6 exit test: fit a regression in NumPy, match statsmodels, and explain every number. The widget reproduces the text layout of `print(results.summary())` for the pinned statsmodels version [unverified which version Pyodide ships]. Tapping a number opens a card with a one-sentence definition, the formula with this data's values substituted, and a linked picture: residuals for $SSE$, the $t$ tail for $P > \lvert t \rvert$, the coefficient's sampling distribution for its standard error, the residual histogram for skew, kurtosis, Omnibus and Jarque-Bera, a lag-1 residual scatter for Durbin-Watson, and singular values for the condition number. "Break it" toggles show which numbers move.
- **Fields.** Dep. Variable, Model, Method, Date, Time (both fixed in fixtures), No. Observations, Df Residuals, Df Model, Covariance Type; R-squared, Adj. R-squared, F-statistic, Prob (F-statistic), Log-Likelihood, AIC, BIC; per coefficient: coef, std err, t, $P > \lvert t \rvert$, [0.025, 0.975]; Omnibus, Prob(Omnibus), Skew, Kurtosis, Durbin-Watson, Jarque-Bera (JB), Prob(JB), Cond. No.; the numbered notes.
- **Serves.** 1.6.5 L15, L16.
- **Uses.** `data-table` (layout), `tex-terms` (substituted formulas), `regression-lab` (linked plots), `dist-explorer` ($t$ and $F$ tails), `qq-plot` and `marks` (residual histogram, lag scatter), `numeric-entry` (blanked cells), `free-response` (explain a number), `code-cell` (the drill).
- **Interactions.**
  - Pointer: tap any value to open its card; in predict mode, blanked values are fields; toggles: add a pure-noise predictor ($R^2$ rises, adjusted $R^2$ falls), heteroscedastic errors (switch covariance type to see standard errors move and coefficients stay), collinear predictors (condition number and standard errors jump, the note appears), autocorrelated errors (Durbin-Watson falls).
  - Keyboard: a roving grid over values; Enter opens the card; Escape closes it; Tab moves into fields.
- **State.** `{ selected?: CellId; entries: Record<CellId, string>; toggles: Record<string, boolean>; cov: string }`.
- **Answers and checks.** `numeric` per cell through `multi` (part marks per cell), `choice` (interpretations), `free-text` (explain a number against a rubric; self-marked, with an optional tutor draft), `code` (the learner's NumPy values against CI fixtures).
- **Config.**

```ts
interface SummaryTableConfig {
  data: { X: number[][]; y: number[]; names: string[]; depName: string } | { fixture: string };
  covType: 'classical' | 'HC0' | 'HC1' | 'HC2' | 'HC3';   // 'classical' prints as statsmodels' default label
  hidden?: string[];                 // cell ids the learner computes
  toggles?: ('noise-predictor' | 'hetero' | 'collinear' | 'autocorr')[];
  fixture?: string;                  // statsmodels reference values precomputed in CI
}
```

- **Visual.** The table in Source Code Pro on `--bg-sunken`, laid out like statsmodels' text so the learner recognises it on a terminal later; each value a button with a focus ring; the selected value `--manip-wash`; the card as a bottom sheet on mobile and a side panel on desktop; linked plot elements highlighted with the pear focus wash.
- **Motion.** The card enters over 280ms (`--d-sheet`); values changed by a toggle get a 150ms focus wash.
- **Reduced motion.** Instant.
- **Accessibility.** A real table with headers; each value a button named "R-squared, 0.812"; cards are regions with headings.
- **Tutor hooks.** Describe: "OLS, y on x1 and x2, n = 50. Selected: std err of x1 (0.141). Blanked: t of x1, Adj. R-squared. Toggles: none." Ids: `cell:<field>` (for example `cell:r-squared`, `cell:coef:x1`, `cell:se:x1`, `cell:dw`), `card`, `plot:<id>`. Secret: blanked values.
- **Performance.** All values computed once per data or toggle change: QR for $n \le 1{,}000$ and $p \le 10$ plus the normality and autocorrelation statistics in under 3ms [unverified].
- **Accuracy.** Every value must match statsmodels to its printed digits on all 30 fixtures (section 2.10).
- **Artifact and web.** Web: the drill runs real statsmodels in Pyodide and compares. Artifact: the widget shows fixture values; the learner computes in MicroPython with ulab or pure Python if available [unverified]; the "match statsmodels" step is web-only and offers the handoff link.
- **Generators.** Data sets for predict-the-number items ($R^2$ from $SSE$ and $SST$; $t$ from coefficient and standard error; degrees of freedom; adjusted $R^2$; $F$ from $R^2$; AIC from the log-likelihood).
- **Misconceptions.** `p-of-coef-is-probability-it-is-zero`, `higher-r2-is-better-model`, `condition-number-is-an-error`, `durbin-watson-two-is-bad`.

### 7.8 `qq-plot`: Quantile-quantile plot

**Composite · P1 · E (also used at P2 in 2.2).** Sorted data against theoretical quantiles, built by hand and read for shape.

- **Purpose.** A QQ plot pairs the $i$th smallest observation with the reference quantile at plotting position $p_i$. A straight line means the shapes agree; an S shape means heavier tails; a bow means skew. Building one by hand for $n \le 10$ makes the pairing concrete.
- **Serves.** 1.6.5 L7, L8; 2.2.4 L1; optional in 1.5.7 L8.
- **Uses.** `plot-axes`, `marks` (scatter, reference line, envelope band), `token-tray` (pairing in build mode), `dist-explorer` (quantile positions), `slider` (tail weight through $t$ degrees of freedom; skew), `sim-runner` (envelope).
- **Interactions.**
  - Pointer: in build mode tap a sorted observation then its quantile slot; in explore mode choose a data shape and a reference; toggle the simulation envelope.
  - Keyboard: `token-tray` keys in build mode; chips and sliders.
- **State.** `{ data: number[]; reference: DistSpec; pairs?: [number, number][]; envelope: boolean }`.
- **Answers and checks.** `choice` (shape diagnosis), `mapping` (pairing), `numeric` (a plotting position or reference quantile).
- **Config.**

```ts
interface QqPlotConfig {
  data: number[] | { generate: { shape: 'normal' | 't3' | 't5' | 'exponential' | 'uniform' | 'lognormal'; n: number; seed: number } };
  reference: DistSpec;
  mode: 'build' | 'explore' | 'diagnose';
  positions: 'hazen' | 'blom' | 'filliben';    // (i - 0.5)/n, (i - 3/8)/(n + 1/4), Filliben's medians
  envelope?: boolean;
}
```

- **Visual.** Points `--s2`; the reference line dashed ink; the envelope `--s3` at 20%; build slots dashed `--manip`.
- **Motion.** In build mode a paired point flies to its position over 300ms.
- **Reduced motion.** Instant.
- **Accessibility.** Table: rank, observation, plotting position, reference quantile; a sentence describing departures ("points rise above the line at the right end: heavier right tail").
- **Tutor hooks.** Ids: `point:<i>`, `line:reference`, `band:envelope`, `slot:<i>`. Describe gives the shape summary and the positions convention.
- **Performance.** Canvas above 1,500 points.
- **Artifact and web.** No difference.
- **Generators.** Diagnose-the-shape items from seeded samples large enough to be unambiguous ($n \ge 200$).
- **Misconceptions.** `qq-axes-swapped`, `any-wiggle-means-non-normal`.

### 7.9 `posterior-lab`: Posterior lab

**Composite · P1 · E.** Prior times likelihood, renormalised: on a grid, with conjugate families, and across many groups.

- **Purpose.** Shape a prior over $\theta$ (bars on a grid, or a Beta curve), observe data, multiply by the likelihood point by point and renormalise. Conjugacy makes $\text{Beta}(\alpha, \beta)$ become $\text{Beta}(\alpha + k, \beta + n - k)$, read as pseudo-counts. Sequential updating equals batch updating. Credible intervals contain $\theta$ with stated posterior probability; confidence intervals do not make that claim. The posterior predictive gives the next observation's chance. Normal-normal updating is precision weighting. Many groups shrink towards the pooled mean, which is how noisy fund alphas should be read.
- **Serves.** 1.6.6 L1 to L8; 1.6.3 L4 (contrast).
- **Uses.** `plot-axes`, `mass-editor` (grid prior), `marks` (bars, `curve`, `stems`, `intervals`), `slider` ($\alpha$, $\beta$, prior mean and SD, prior strength), `chance-object` (coin flips), `sim-runner` (data and predictive draws), `number-line` (credible interval), `tex-terms`.
- **Interactions.**
  - Pointer: drag prior bars or the $\alpha$ and $\beta$ sliders; Flip or enter $k$ of $n$; step through Prior, Likelihood, Posterior; toggle sequential or batch; drag the credible bracket to hold 95% (equal-tailed or highest-density); in groups mode slide the prior strength and watch estimates move towards the pool.
  - Keyboard: `mass-editor` keys; sliders; buttons; the bracket ends are sliders.
- **State.** `{ prior: { grid: Entry[] } | { alpha: number; beta: number } | { mu0: number; tau0: number }; data: { k: number; n: number } | { xs: number[] }; stage: 'prior' | 'likelihood' | 'posterior'; interval?: [number, number]; groups?: { k: number; n: number }[]; strength?: number }`.
- **Answers and checks.** `numeric` (posterior mean, MAP, predictive probability, updated parameters), `interval` (credible interval), `distribution` (grid posterior, total-variation tolerance), `expression` ($\alpha' = \alpha + k$), `choice` (sensitivity and interpretation).
- **Config.**

```ts
interface PosteriorLabConfig {
  model: 'grid-binomial' | 'beta-binomial' | 'normal-normal' | 'gamma-poisson' | 'groups';
  prior: { grid: Entry[]; thetas: number[] } | { alpha: number; beta: number } | { mu0: number; tau0: number };
  data?: { k: number; n: number } | { xs: number[]; sigma: number };
  editable: ('prior' | 'data')[];
  show: ('prior' | 'likelihood' | 'posterior' | 'predictive' | 'interval' | 'mle')[];
  groups?: { label: string; k: number; n: number }[];
  task?: string;
}
```

- **Visual.** The Bayes triple: prior `--s6` dashed (or outlined bars), likelihood `--s2` labelled "likelihood, rescaled", posterior `--s3` filled at 25%; the MLE as an ink marker; the credible bracket `--manip`; in groups mode raw estimates as `--s2` dots and shrunk estimates as `--s3` dots joined by arrows towards the pooled line.
- **Motion.** Multiply then renormalise plays per stage over 600ms (a consequence of Next); sequential flips update after each flip.
- **Reduced motion.** Stages swap without interpolation.
- **Accessibility.** Grid table: $\theta$, prior, likelihood, posterior; "Posterior Beta(9, 5): mean 0.643; 95% interval 0.39 to 0.86".
- **Tutor hooks.** Ids: `curve:prior`, `curve:likelihood`, `curve:posterior`, `bar:<theta>`, `bracket:interval`, `slider:alpha`, `slider:beta`, `flip`, `group:<i>`, `slider:strength`. Secret: requested posterior quantities.
- **Performance.** Grids up to 201 points; Beta quantiles from `dist`.
- **Artifact and web.** No difference.
- **Generators.** Conjugate update items with tidy parameters; grid items; predictive items; shrinkage items.
- **Misconceptions.** `credible-equals-confidence`, `flat-prior-is-neutral`, `order-of-data-matters`, `prior-irrelevant-at-small-n`.

---

## 8. Time-series composites (2.2)

All 6 are P2, wave F. Default data are seeded synthetic series (decision 11); a series spec names a generator and its parameters, or a CSV file and a column.

```ts
type SeriesSpec =
  | { gen: 'random-walk'; drift?: number; sigma: number; T: number; seed: number; start?: number; log?: boolean }
  | { gen: 'arma'; phi: number[]; theta: number[]; sigma: number; T: number; seed: number; mean?: number }
  | { gen: 'garch'; omega: number; alpha: number; beta: number; innov: 'normal' | 't'; df?: number; T: number; seed: number }
  | { gen: 'trend-season'; slope: number; period: number; amp: number; sigma: number; T: number; seed: number }
  | { gen: 'pair'; kind: 'cointegrated' | 'independent' | 'correlated-returns'; beta: number; kappa: number; T: number; seed: number }
  | { csv: string; column: string; dateColumn?: string };
```

### 8.1 `series-lab`: Series lab

**Composite · P2 · F.** A time-series workbench: transforms, rolling statistics, two-window comparison, decomposition and stylised facts.

- **Purpose.** Prices wander and returns hover. The learner applies transform chips (log, difference, log-difference, percentage change, standardise) and watches a non-stationary series become stationary. Two draggable windows compare their histograms: for a random walk they disagree, for returns they agree; that comparison is the working meaning of weak stationarity. Rolling mean and SD use a window slider. Decomposition pulls out trend and season. Facts mode shows kurtosis, the histogram against the normal and the clustering of large moves.
- **Serves.** 2.2.1 L1 to L5; 2.2.4 L1; 1.1 exit (log returns, annualised volatility) as a cross-cluster bonus.
- **Uses.** `plot-axes` (time axis; stacked linked panels), `marks` (paths, `hist`, `band`, `rug`), `region-selector` (two brushes on the time axis), `slider` (window, period), `choice-cards` (transform chips), `sim-runner` (`arma`, `garch`, `pair` and walk generators), `data-table`, `acf-lab` (link).
- **Interactions.**
  - Pointer: choose a series; tap transform chips in order (they stack and can be removed); drag brushes A and B; slide the rolling window; toggle decomposition; classify a generated series.
  - Keyboard: chips; brush ends are sliders; slider.
- **State.** `{ source: SeriesSpec; transforms: string[]; brushes: { a: [number, number]; b: [number, number] }; window: number; decomposition: boolean }`.
- **Answers and checks.** `choice` (stationary or not; which transform), `numeric` (a log return over a period; annualised volatility), `state` (predicate `transform-sequence`).
- **Config.**

```ts
interface SeriesLabConfig {
  source: SeriesSpec;
  transforms?: ('log' | 'diff' | 'logdiff' | 'pct' | 'standardise' | 'seasonal-diff')[];
  editable: ('transforms' | 'brushes' | 'window' | 'source')[];
  panels: ('level' | 'transformed' | 'rolling' | 'split-hist' | 'decompose' | 'facts')[];
}
```

- **Visual.** Level series 1.5px ink; transformed series `--s2`; rolling mean `--s3` with the rolling SD band `--s3` at 20%; brushes `--manip-wash` rectangles with `--manip` handles; window histograms A in `--s2` and B in `--s6`, overlaid with labels.
- **Motion.** Direct.
- **Reduced motion.** Not applicable.
- **Accessibility.** Window summaries ("Window A: mean 101.2, SD 3.1. Window B: mean 87.6, SD 4.0"); table view of the first 200 rows with CSV export.
- **Tutor hooks.** Describe: "Random walk, T = 500. Transforms: log, diff. Window A days 50 to 150, B days 350 to 450: means 0.0004 and 0.0001, SDs 0.010 and 0.010." Ids: `series:level`, `series:transformed`, `brush:a`, `brush:b`, `hist:a`, `hist:b`, `band:rolling`, `chip:<transform>`, `slider:window`. Secret: the generator.
- **Performance.** Up to 10,000 points on canvas with min-and-max decimation; window statistics from prefix sums in $O(1)$ per frame.
- **Artifact and web.** Synthetic data on both; CSV upload on the web; in the Artifact a file input [unverified] or the item's published CSV.
- **Generators.** Stationarity classification series (walks, AR, trend, seasonal, GARCH); transform items.
- **Misconceptions.** `prices-are-stationary`, `trend-or-random-walk`, `simple-returns-add`.

### 8.2 `acf-lab`: Autocorrelation lab

**Composite · P2 · F.** From lag scatter to correlogram, partial autocorrelation and the Ljung-Box test.

- **Purpose.** At lag $k$, plot $x_t$ against $x_{t-k}$; its correlation is the bar $r_k$ of the correlogram. Bands at $\pm 1.96/\sqrt{T}$ mark what white noise produces, and about one bar in twenty crosses them by chance. The PACF removes the intermediate lags first. Ljung-Box tests many lags at once. Returns show almost no autocorrelation while squared returns show a long one: volatility clustering.
- **Serves.** 2.2.2 L1 to L5; 2.2.3 L5; 2.2.4 L1.
- **Uses.** `plot-axes` (series, lag scatter, correlogram), `marks` (scatter, line, `stems`, `band`), `slider` (lag $k$, Ljung-Box $m$), `draggable-point` (predicted bar heights), `test-lab` ($\chi^2$ link), `regression-lab` (partial residual view), `series-lab` (source).
- **Interactions.**
  - Pointer: slide the lag; tap Build to sweep $k$ from 1 to the maximum; switch to PACF; toggle absolute or squared values; predict bars for a stated model by dragging stem heads before reveal; slide $m$.
  - Keyboard: sliders; stem heads are sliders; toggles.
- **State.** `{ source: SeriesSpec; k: number; mode: 'acf' | 'pacf'; transform: 'none' | 'abs' | 'square'; predictions?: number[]; m: number }`.
- **Answers and checks.** `numeric` ($r_k$, $Q$, its p-value), `distribution` (predicted ACF stems within tolerance), `choice` (white noise or not; which model).
- **Config.**

```ts
interface AcfLabConfig {
  source: SeriesSpec;
  maxLag: number;
  mode: 'acf' | 'pacf';
  show: ('lag-scatter' | 'correlogram' | 'bands' | 'pacf' | 'ljung-box' | 'theory')[];
  theory?: { phi: number[]; theta: number[] };
  predict?: boolean;
}
```

- **Visual.** Lag scatter `--s2` dots with an `--s3` fit line and $r$ label; sample correlogram stems `--s2`; theory stems `--s3` dashed; bands dashed `--text-muted` with labels; the current lag's stem gets the pear focus wash; predicted stems `--manip`.
- **Motion.** Build sweeps one lag per 150ms (a demonstration).
- **Reduced motion.** The full correlogram appears.
- **Accessibility.** Table: lag, $r_k$, outside band or not; "Lag 1: 0.62, outside the band. Ljung-Box over 10 lags: Q 210, p below 0.001".
- **Tutor hooks.** Ids: `slider:lag`, `scatter:lag`, `stem:<k>`, `band`, `pacf:<k>`, `readout:q`. Secret: the generating model.
- **Performance.** Direct sums $O(TK)$ for $T \le 5{,}000$ and $K \le 40$; PACF by Durbin-Levinson.
- **Artifact and web.** No difference.
- **Generators.** Identification items from AR(1), AR(2), MA(1), MA(2), white noise and random walks, with $T \ge 500$ and parameters chosen so the signature is clear; the generator rejects any series whose sample pattern contradicts its model.
- **Misconceptions.** `one-bar-out-means-dependence`, `ar-acf-cuts-off`, `uncorrelated-returns-are-independent`.

### 8.3 `arma-lab`: ARMA lab

**Composite · P2 · F.** Build AR, MA and ARMA models by hand, with the same shocks, and see paths, correlograms, roots and fits.

- **Purpose.** AR(1) with $\varphi$ is mean reversion with half-life $\frac{\ln 0.5}{\ln \varphi}$; at $\varphi = 1$ the series is a random walk. MA($q$) has memory of $q$ steps. AR(2) is stationary inside a triangle in the $(\varphi_1, \varphi_2)$ plane, and below the parabola $\varphi_1^2 + 4\varphi_2 = 0$ its roots are complex and the series cycles. Invertibility puts MA roots outside the unit circle. Fitting compares AIC and BIC over a $(p, q)$ grid. Shocks are fixed by the seed, so every parameter change shows its effect on the same noise.
- **Serves.** 2.2.1 L6; 2.2.3 L1 to L4, L6.
- **Uses.** `plot-axes` (path, triangle, ACF, impulse response), `complex-plane` (roots against the unit circle), `marks`, `slider` ($\varphi_1$, $\varphi_2$, $\theta_1$, $\theta_2$, $\sigma$), `draggable-point` (the $(\varphi_1, \varphi_2)$ point; roots), `sim-runner` (`arma` with supplied shocks), `acf-lab` (theory against sample), `data-table` (AIC grid).
- **Interactions.**
  - Pointer: drag sliders or the triangle point; drag roots directly; toggle panels; in fit mode tap a grid cell to fit that order and compare.
  - Keyboard: sliders; the triangle point is a 2D handle; grid cells are a roving grid.
- **State.** `{ phi: number[]; theta: number[]; sigma: number; seed: number; T: number; fit?: { p: number; q: number; aic: number[][] } }`.
- **Answers and checks.** `numeric` (half-life, theoretical $\rho_k$, unconditional variance), `point` (a parameter point inside a named region, predicate `in-region`), `choice` (stationary, invertible, which model).
- **Config.**

```ts
interface ArmaLabConfig {
  p: 0 | 1 | 2; q: 0 | 1 | 2;
  init: { phi: number[]; theta: number[]; sigma: number };
  editable: ('phi' | 'theta' | 'sigma')[];
  show: ('path' | 'triangle' | 'roots' | 'acf' | 'pacf' | 'irf' | 'fit-grid')[];
  T: number; seed: number;
}
```

- **Visual.** The path in ink; the triangle's stationary area `--s3` at 15%, the complex-root zone hatched; the parameter point `--manip`; roots as `--s2` crosses against the ink unit circle; theory ACF `--s3`, sample ACF `--s2`; impulse response as stems.
- **Motion.** Direct.
- **Reduced motion.** Not applicable.
- **Accessibility.** "AR(2) with phi 1 = 0.5 and phi 2 = 0.3: stationary, real roots; ACF decays without cycles." Tables for ACF and impulse response.
- **Tutor hooks.** Ids: `point:phi`, `triangle`, `root:<i>`, `unit-circle`, `path`, `irf:<k>`, `cell:<p>,<q>`, `slider:<param>`.
- **Performance.** A path of $T \le 2{,}000$ recomputed per frame in $O(T)$; fits in the worker (about 50ms per order [unverified]).
- **Artifact and web.** No difference.
- **Generators.** Half-life items; stationarity and invertibility classification; theoretical ACF values.
- **Misconceptions.** `phi-one-reverts`, `ma-has-long-memory`, `lowest-aic-is-truth`.

### 8.4 `forecast-lab`: Forecast lab

**Composite · P2 · F.** Forecasts, their intervals, and honest evaluation over time.

- **Purpose.** Forecasts from a stationary model revert to the mean and their intervals saturate; random-walk forecasts are flat and their intervals grow like $\sqrt{h}$. Methods: naive (random walk), mean, drift, seasonal naive, AR($p$), simple exponential smoothing. Evaluation: a train and test split, then rolling-origin evaluation with an expanding window, scored by MAE, RMSE and MASE. The leakage Trap compares shuffled K-fold cross-validation with time-ordered validation on the same series.
- **Serves.** 2.2.3 L7, L8, L9; 2.1 exit (time-ordered cross-validation), cross-cluster.
- **Uses.** `plot-axes`, `marks` (path, `fan`, error bars), `region-selector` (split brush), `slider` ($h$, $\alpha$, origin), `choice-cards` (methods), `sim-runner`, `data-table` (scores).
- **Interactions.**
  - Pointer: drag the split; choose up to three methods; slide $h$ and $\alpha$; Play the rolling origin; toggle the shuffled-CV comparison.
  - Keyboard: the split is a slider; chips; sliders; P plays.
- **State.** `{ source: SeriesSpec; split: number; methods: string[]; h: number; alpha?: number; origin?: number; cv: 'rolling' | 'shuffled' }`.
- **Answers and checks.** `numeric` (a forecast value, an interval width at $h$, an error metric), `choice` (which method wins; why shuffled CV flatters), `ordering` (rank methods by RMSE).
- **Config.**

```ts
interface ForecastLabConfig {
  source: SeriesSpec;
  methods: ('naive' | 'mean' | 'drift' | 'snaive' | 'ar' | 'ses')[];
  h: number; split: number;
  show: ('fan' | 'actuals' | 'errors' | 'rolling-origin' | 'shuffled-cv')[];
}
```

- **Visual.** History in ink; each method's forecast in `--s2`, `--s3` or `--s6` with a direct label and its `fan` bands; test-period actuals dashed ink; the split line `--manip`.
- **Motion.** Rolling-origin play advances one origin per 200ms (a demonstration).
- **Reduced motion.** Steps without interpolation.
- **Accessibility.** Score table; "AR(1) RMSE 1.02 against naive 1.31 over 50 origins".
- **Tutor hooks.** Ids: `split`, `method:<id>`, `fan:<id>`, `slider:h`, `origin`, `errors`, `table:scores`.
- **Performance.** Forecasts are closed form; up to 1,000 origins evaluated in the worker.
- **Artifact and web.** No difference.
- **Generators.** Forecast and interval items for AR(1) and random walks; method-ranking items.
- **Misconceptions.** `shuffled-cv-is-fine`, `narrow-intervals-are-better`, `in-sample-fit-is-skill`.

### 8.5 `garch-lab`: Volatility lab

**Composite · P2 · F.** EWMA, ARCH and GARCH(1,1) driven by the same shocks; forecasts, likelihood and VaR.

- **Purpose.** $\sigma_t^2 = \omega + \alpha r_{t-1}^2 + \beta \sigma_{t-1}^2$: a shock raises tomorrow's variance and the effect decays at rate $\alpha + \beta$. Long-run variance is $\frac{\omega}{1 - \alpha - \beta}$; half-life of a volatility shock is $\frac{\ln 0.5}{\ln(\alpha + \beta)}$; forecasts of $\sigma^2_{t+h}$ converge to the long-run level. EWMA is the case $\omega = 0$, $\alpha + \beta = 1$. Fitting means finding the peak of the log-likelihood over $(\alpha, \beta)$ inside $\alpha + \beta < 1$. VaR mode counts exceedances of a 1% band.
- **Serves.** 2.2.4 L2 to L7.
- **Uses.** `plot-axes` (returns, $\sigma_t$, term structure, news impact curve, likelihood map), `marks` (paths, `band`, heatmap, contours, `curve`), `slider` ($\omega$, $\alpha$, $\beta$, $\lambda$), `draggable-point` ($(\alpha, \beta)$ on the map, constrained to the triangle), `sim-runner` (`garch` with supplied shocks), `acf-lab` (squared returns), `qq-plot` (standardised residuals), `dist-explorer` ($t$ innovations).
- **Interactions.**
  - Pointer: sliders; switch EWMA, ARCH(1), GARCH(1,1); drag $(\alpha, \beta)$ on the log-likelihood map; toggle the term structure and news impact panels; in VaR mode slide the level and count exceedances.
  - Keyboard: sliders; the map point is a 2D handle.
- **State.** `{ omega: number; alpha: number; beta: number; lambda?: number; seed: number; T: number; mode: string; mapPoint?: Vec2 }`.
- **Answers and checks.** `numeric` (long-run variance, persistence, half-life, next-day forecast, expected exceedances), `point` (the MLE on the map within tolerance), `choice` (which series is GARCH), `state` (predicate `in-region`).
- **Config.**

```ts
interface GarchLabConfig {
  mode: 'ewma' | 'arch1' | 'garch11' | 'fit' | 'var';
  params: { omega?: number; alpha?: number; beta?: number; lambda?: number };
  innovations: 'normal' | 't'; df?: number;
  source?: SeriesSpec;                   // fit mode on given returns
  show: ('returns' | 'sigma' | 'term' | 'nic' | 'map' | 'squared-acf' | 'var')[];
  T: number; seed: number;
}
```

- **Visual.** Returns in ink; the $\pm 2\sigma_t$ band `--s3` at 20%; the EWMA line `--s6`; the map on `--seq-1` to `--seq-6` with contours; the $(\alpha, \beta)$ handle `--manip`; the boundary $\alpha + \beta = 1$ dashed ink; the VaR line `--s2` with exceedances marked by ink crosses.
- **Motion.** Direct.
- **Reduced motion.** Not applicable.
- **Accessibility.** "GARCH(1,1), omega 0.02, alpha 0.08, beta 0.90: persistence 0.98, long-run daily SD 1.0%, half-life 34 days."
- **Tutor hooks.** Ids: `slider:<param>`, `series:returns`, `band:sigma`, `map:loglik`, `handle:ab`, `boundary`, `curve:term`, `curve:nic`, `exceed:<i>`. Secret: the true parameters and the MLE.
- **Performance.** The recursion over $T \le 5{,}000$ costs well under 1ms per frame; the $48 \times 48$ likelihood map over $T = 2{,}000$ (about 4.6 million updates) runs in the worker when the data change.
- **Artifact and web.** No difference. The fitting drill (web) uses `scipy.optimize.minimize` on the learner's likelihood (decision 12).
- **Generators.** Persistence, long-run variance and half-life items; forecast items; exceedance items.
- **Misconceptions.** `volatility-is-constant`, `alpha-plus-beta-one-is-fine`, `garch-predicts-direction`.

### 8.6 `coint-lab`: Cointegration lab

**Composite · P2 · F.** Two price series, a hedge ratio, a spread, and the Engle-Granger test done in two visible steps.

- **Purpose.** Two non-stationary prices that share a stochastic trend have a stationary combination $y_t - \beta x_t$. Only the right $\beta$ makes the spread stop wandering. Engle-Granger estimates $\beta$ by regression, then tests the residuals for a unit root against Engle-Granger critical values, which are more negative than Dickey-Fuller's because $\beta$ was fitted. Spurious regression shows independent walks giving huge $t$-statistics. Return correlation and cointegration are different properties. The error-correction model reads the speed of adjustment and the half-life. Trading mode puts z-score bands on the spread and warns about estimating $\beta$ on data the strategy then trades.
- **Serves.** 2.2.1 L9; 2.2.5 L1 to L6; 3.1 pairs replication (Gatev, Goetzmann and Rouwenhorst), cross-cluster.
- **Uses.** `plot-axes` (both prices, levels scatter, spread, z-score, a small null-distribution panel), `marks`, `slider` (hedge ratio, mean-reversion speed, noise), `draggable-point` (the hedge-ratio handle on the scatter's line; entry and exit bands), `sim-runner` (`pair`), `test-lab` (ADF on the spread with Engle-Granger critical values), `regression-lab` (spurious readouts), `sde-stepper` (Ornstein-Uhlenbeck link), `code-cell` (statsmodels drill), `free-response` (exit explanation).
- **Interactions.**
  - Pointer: generate a pair (cointegrated, independent walks, or correlated returns without cointegration); drag $\beta$ and watch the spread and its ADF statistic update live against the critical line; Estimate $\beta$ (step 1) and Test residuals (step 2); open the ECM panel; in trading mode drag entry and exit bands and move the in-sample and out-of-sample split.
  - Keyboard: handles and sliders; buttons.
- **State.** `{ pair: SeriesSpec; beta: number; step: 0 | 1 | 2; entry?: number; exit?: number; split?: number }`.
- **Answers and checks.** `numeric` ($\hat\beta$, the ADF statistic, half-life), `choice` (cointegrated or not; which critical values apply), `state` (predicate `hedge-ratio-near`), `code` (web drill: `statsmodels.tsa.stattools.coint` and `adfuller` on the item's pair, compared with fixtures), `free-text` (why models are fitted to returns, not prices).
- **Config.**

```ts
interface CointLabConfig {
  pair: Extract<SeriesSpec, { gen: 'pair' }> | { csv: string; columns: [string, string] };
  steps: ('levels' | 'scatter' | 'spread' | 'adf' | 'ecm' | 'trading' | 'spurious')[];
  editable: ('beta' | 'bands' | 'split')[];
  task?: string;
}
```

- **Visual.** Series $y$ in ink and $x$ in `--s2` on a shared scale; the levels scatter `--s2` with the $\beta$ line `--manip`; the spread `--s3` with its mean line; entry and exit bands as `--manip` dashed lines; the ADF readout beside a small null-distribution panel with the observed statistic and the critical value.
- **Motion.** Direct.
- **Reduced motion.** Not applicable.
- **Accessibility.** "Your beta 1.40: spread ADF −2.1; Engle-Granger 5% critical value −3.37: unit root not rejected." Table view of both series with CSV export.
- **Tutor hooks.** Describe: "Pair: cointegrated (hidden). β = 1.40. Step 1 done (OLS β 1.52). Spread ADF −2.1." Ids: `series:y`, `series:x`, `scatter`, `handle:beta`, `spread`, `band:entry`, `band:exit`, `readout:adf`, `line:critical`, `panel:ecm`, `split`. Secret: the pair's kind and true $\beta$.
- **Performance.** The spread and its ADF regression recompute per frame in under 1ms for $T \le 1{,}000$ and up to 5 lags.
- **Artifact and web.** The statsmodels drill is web-only; the Artifact shows fixture values.
- **Generators.** Cointegrated and non-cointegrated pairs; the generator rejects any pair whose Engle-Granger statistic lies within 1.0 of the 5% critical value, so the classification is never borderline.
- **Misconceptions.** `correlation-is-cointegration`, `df-critical-values-for-residuals`, `high-r2-means-a-relationship`, `full-sample-beta-in-backtest`.

---

## 9. Generators

Practice, quizzes, homework and exams need many instances of each item. This cluster follows the sibling rule (calc-linalg section 2.12): a generator is a pure function `make(seed, difficulty)` returning a widget config, a check, a worked solution and the misconceptions its distractors encode. Each ships with a property test over 1,000 seeds.

**Rules this cluster adds** [our choice]:

1. **Two-way verification.** Every generated answer is computed by an exact or closed-form solver and confirmed in CI by a seeded simulation of at least $10^6$ draws within 4 standard errors, or by numerical integration for continuous answers.
2. **Tidy numbers by construction.** Choose the answer's shape first and build the item around it: integer counts in icon arrays, rational stationary distributions by detailed balance, regression coefficients by projecting residuals out of the column space, exact sample correlations by a Cholesky adjustment.
3. **No borderline classifications.** Items that ask "stationary?", "cointegrated?" or "which model?" reject instances whose statistics sit near the decision boundary.
4. **Fixed data are shown.** Every number the learner computes from appears on screen or in a table; nothing depends on an unseen simulation.
5. **Interview-style variety.** Each generator varies the story as well as the numbers (dice, cards, coins, defaults, trades, arrivals), so practice tests the idea, not the wording.

| Widget | Generator ids | What varies | Answer computed by | Difficulty |
|---|---|---|---|---|
| `prob-square` | `two-event`, `bayes-k`, `make-independent` | event rates; 2 to 5 hypotheses; evidence sequences | exact rationals | 1 to 4 |
| `icon-array` | `screening`, `fallacy`, `simpson`, `fdr` (P1) | prevalence, sensitivity, specificity, $n$; strata | exact integer counts | 1 to 3 |
| `contingency-table` | `joint`, `conditional`, `simpson`, `independence`, `chi2` (P1) | counts and labels | exact; reversal verified | 1 to 4 |
| `odds-ledger` | `sequential`, `coin-two-headed`, `bayes-factor` (P1) | priors and likelihood ratios | exact odds | 2 to 4 |
| `rv-mapper` | `assign`, `pmf`, `g-merge`, `lotus` | space, rule, $g$ | exact rationals | 1 to 3 |
| `dist-explorer` | per family: `interval`, `quantile`, `moments`, `approx`, `story`, `bounds` | family, parameters, interval ends | `dist` service; exact for discrete | 1 to 5 |
| `galton-board` | `paths`, `bin-prob`, `tilt` | $n$, $k$, $p$ | exact | 1 to 3 |
| `convolver` | `discrete-sum`, `density-at`, `shape` | two distributions | exact or `quad` | 2 to 4 |
| `indicator-board` | one per scenario, plus `expression`, `variance` | $n$, $m$, $d$, pattern | closed forms; simulation check | 2 to 5 |
| `trial-strip` | `wait`, `pattern-race`, `poisson-window`, `memoryless` | $p$, $\lambda$, patterns, windows | exact automaton solve | 2 to 5 |
| `generating-function` | `recognise`, `moment`, `sum`, `extinction` | family, offspring law | symbolic and exact | 2 to 5 |
| `order-statistics` | `expected-kth`, `cdf-max-min`, `spacings` | base, $n$, $k$ | closed forms | 2 to 5 |
| `sampling-lab` | `predict-se`, `clt-prob`, `required-n`, `bootstrap` (P1) | population, $n$ | closed forms | 2 to 4 |
| `joint-density` | `table`, `region`, `marginal`, `conditional`, `independence` | joint law, region | exact or `quad` | 2 to 5 |
| `covariance-lab` | `guess-r`, `make-r`, `zero-cov` | $n$, $\rho$, shape | exact sample statistics | 1 to 3 |
| `gaussian-2d` | `conditional`, `combination`, `min-var` | $\sigma$s, $\rho$, weights | closed forms | 2 to 4 |
| `cond-expectation` | `slice-means`, `adam`, `eve`, `random-sum` | joint law or groups | exact | 2 to 5 |
| `geo-prob` | `meeting`, `threshold`, `broken-stick`, `custom-region` | windows, thresholds | exact polygon areas | 2 to 5 |
| `game-lab` | `monty`, `dice-stop`, `secretary`, `kelly` (P2) | doors, rolls, die, $n$, edge | closed form or dynamic programming | 2 to 5 |
| `first-step-solver` | `pattern`, `ruin`, `alternating`, `custom-chain` | patterns, $p$, $N$ | exact BigInt elimination | 3 to 5 |
| `markov-chain` | `n-step`, `stationary`, `classify`, `absorb`, `pagerank` | chain structure and weights | exact | 2 to 5 |
| `lattice-walk` | `count`, `ballot`, `catalan`, `first-passage` | $n$, endpoint, barrier | exact | 2 to 5 |
| `estimator-compare` | `bias-var`, `german-tank`, `divisor` | model, $n$ | closed forms | 3 to 5 |
| `likelihood-lab` | `mle`, `se`, `lr` | model, data | closed forms | 2 to 5 |
| `ci-ladder` | `compute`, `sample-size`, `interpret` | data, level | closed forms with table critical values | 2 to 4 |
| `test-lab` | `t`, `z`, `chi2`, `power`, `decide` | data, $\alpha$, effect | `tests` service | 2 to 5 |
| `multiple-testing` | `bh-set`, `holm-set`, `fwer` | p-value lists, $m$ | exact procedures | 2 to 4 |
| `regression-lab` | `coef`, `diagnose`, `ovb`, `interval` | design, violations | `ols` service | 2 to 5 |
| `summary-table` | `predict-cell` | data set, blanked cells | `ols`, checked against fixtures | 3 to 5 |
| `qq-plot` | `diagnose` | shape, $n$ | generator label | 2 to 3 |
| `posterior-lab` | `conjugate`, `grid`, `predictive`, `shrink` | prior, data | exact | 2 to 4 |
| `series-lab` | `classify`, `transform`, `log-return` | generator, parameters | generator label | 1 to 3 |
| `acf-lab` | `identify`, `theory-acf`, `ljung-box` | model, $T$ | `ts` service | 2 to 4 |
| `arma-lab` | `half-life`, `region`, `theory` | parameters | closed forms | 2 to 4 |
| `forecast-lab` | `forecast`, `interval`, `rank` | model, $h$ | closed forms | 2 to 4 |
| `garch-lab` | `persistence`, `long-run`, `forecast`, `exceed` | parameters | closed forms | 2 to 4 |
| `coint-lab` | `classify-pair`, `half-life`, `hedge` | pair kind, $\beta$, $\kappa$ | `tests` service, margin rule | 3 to 5 |

**Extensions to sibling generators** (section 5): `outcome-grid` gains weighted-dice and three-dice items; `tree-diagram` gains flip items; `trial-simulator` gains urn, permutation, birthday, coupon and Pólya prediction items; `counting-slots` gains story-proof and multinomial items; `venn-diagram` gains probability-mode atom items; `pascal-triangle` gains weighted-row items.

---

## 10. Misconception register

Every id below is a distractor or a misconception rule that some screen uses. The line is what the verdict chip says (at most 20 words, referring to the learner's own action where possible). Show-why keys are in each widget's entry.

| Id | Verdict-chip line | Widgets |
|---|---|---|
| `transposed-conditional` | That is the chance of the evidence given the cause. The question asks the reverse. | `prob-square`, `icon-array`, `odds-ledger` |
| `base-rate-neglect` | The test is good, but almost nobody has the condition. Look at how many false alarms there are. | `prob-square`, `icon-array` |
| `sensitivity-is-ppv` | 90% of the sick test positive. That is not the share of positives who are sick. | `icon-array` |
| `prosecutors-fallacy` | A one-in-a-million match still leaves several matching people in a big city. | `icon-array`, `odds-ledger` |
| `independent-means-disjoint` | Disjoint events cannot both happen, so one tells you everything about the other. | `prob-square` |
| `lotp-unweighted-average` | You averaged the heights equally. Wider columns count for more. | `prob-square`, `tree-diagram` |
| `conditioning-keeps-denominator` | After conditioning, the whole of $B$ is the new 1. Divide by its area. | `prob-square`, `outcome-grid` |
| `simpson-aggregate-trusted` | Each group favours the treatment, but the groups are different sizes. Compare within groups. | `contingency-table`, `icon-array` |
| `pairwise-means-mutual` | Each pair is independent, but all three together are not. Check the triple. | `contingency-table`, `outcome-grid` |
| `joint-vs-conditional` | That cell is a share of everyone. The question asks for a share of one row. | `contingency-table` |
| `add-probabilities` | Evidence multiplies the odds; it does not add to the probability. | `odds-ledger` |
| `evidence-order-matters` | Reorder the cards: you land in the same place. | `odds-ledger`, `posterior-lab` |
| `lr-is-posterior` | The likelihood ratio says how much to update, not where you end up. | `odds-ledger` |
| `rv-is-an-outcome` | $X$ is the rule that turns outcomes into numbers, not one of the outcomes. | `rv-mapper` |
| `pmf-counts-values-not-outcomes` | Value 7 comes from six outcomes. Add their probabilities. | `rv-mapper` |
| `g-of-mean` | Squaring the average is not the average of the squares. | `rv-mapper`, `convexity-chord` |
| `pdf-is-probability` | A density can exceed 1. Probability is the area, not the height. | `dist-explorer` |
| `discrete-endpoint` | For a discrete variable, including the endpoint changes the answer. | `dist-explorer` |
| `geometric-convention` | This geometric counts failures before the first success. Check the support. | `dist-explorer`, `trial-strip` |
| `sd-vs-variance` | You used the variance where the standard deviation belongs. | `dist-explorer` |
| `no-continuity-correction` | The bars have width. Shade from half a unit before to half a unit after. | `dist-explorer` |
| `markov-is-an-estimate` | Markov's inequality is a bound, often far above the true tail. | `dist-explorer` |
| `median-equals-mean` | This shape is skewed, so its median and mean differ. | `dist-explorer` |
| `bins-equally-likely` | More paths lead to the middle bins. | `galton-board` |
| `one-path-per-bin` | Count the paths: there are $\binom{n}{k}$ ways to reach bin $k$. | `galton-board`, `pascal-triangle` |
| `sum-of-uniforms-uniform` | Middle totals can be made in more ways than extreme ones. | `convolver`, `outcome-grid` |
| `add-the-densities` | You added the two curves. A sum's density comes from sliding one past the other. | `convolver` |
| `add-the-pmfs` | You added the bars. Sum along each diagonal of the grid instead. | `convolver` |
| `linearity-needs-independence` | Expectations add even when the events depend on each other. | `indicator-board` |
| `find-the-distribution-first` | You do not need the full distribution. Add the indicator probabilities. | `indicator-board` |
| `indicator-expectation-is-count` | An expected count need not be a whole number. | `indicator-board` |
| `hh-equals-ht` | After one H, a T sends HH back to the start but leaves HT halfway there. | `trial-strip`, `first-step-solver` |
| `due-for-a-success` | The coin has no memory. Five tails do not make a head more likely. | `trial-strip`, `trial-simulator` |
| `poisson-windows-not-additive` | Counts in separate windows are independent and their rates add. | `trial-strip` |
| `mgf-is-a-probability` | $M(t)$ is an expectation of $e^{tX}$, not a probability. | `generating-function` |
| `mgf-of-sum-is-sum` | For independent variables, MGFs multiply. | `generating-function` |
| `extinction-is-largest-root` | Extinction probability is the smallest fixed point in $[0, 1]$. | `generating-function` |
| `max-of-uniforms-is-one` | The maximum of five uniforms averages $\frac{5}{6}$, not 1. | `order-statistics` |
| `order-stats-independent` | Sorted values depend on each other: the second smallest is above the smallest. | `order-statistics` |
| `clt-makes-data-normal` | The data keep their shape. The sample mean becomes normal. | `sampling-lab` |
| `law-of-small-numbers` | Small samples swing widely. The law of large numbers needs large $n$. | `sampling-lab`, `trial-simulator` |
| `se-vs-sd` | The spread of the mean is $\sigma/\sqrt{n}$, not $\sigma$. | `sampling-lab` |
| `cauchy-obeys-lln` | The Cauchy has no mean, so the running average never settles. | `sampling-lab` |
| `bootstrap-creates-information` | Resampling shows variability; it cannot add data you do not have. | `sampling-lab` |
| `p-values-cluster-near-005` | Under the null, every p-value from 0 to 1 is equally likely. | `sampling-lab` |
| `slice-is-conditional-without-renormalising` | The slice's heights need dividing by its total area to become a density. | `joint-density` |
| `marginals-determine-joint` | Different joints share these marginals. The dependence is extra information. | `joint-density` |
| `zero-correlation-means-independent` | Correlation only measures straight-line association. This pattern is curved. | `covariance-lab`, `joint-density` |
| `r-measures-slope` | A steep cloud can have a weak correlation, and a flat one a strong one. | `covariance-lab` |
| `outlier-cannot-matter` | One far point dominates the rectangles. Look at its area. | `covariance-lab`, `regression-lab` |
| `regression-line-is-major-axis` | The conditional mean line is flatter than the ellipse's long axis. | `gaussian-2d` |
| `correlated-variances-add` | With correlation, $\mathrm{Var}(X + Y)$ gains $2\,\mathrm{Cov}(X, Y)$. | `gaussian-2d`, `covariance-lab` |
| `sds-add` | Variances add for independent variables; standard deviations do not. | `gaussian-2d`, `dist-explorer` |
| `normal-marginals-uncorrelated-independent` | Each marginal is normal and the correlation is 0, yet $\lvert Y \rvert = \lvert X \rvert$. | `gaussian-2d` |
| `cond-exp-is-a-number` | $E[Y \mid X]$ changes with $X$: it is a random variable. | `cond-expectation` |
| `average-of-averages-unweighted` | Big slices count for more when you average the slice means. | `cond-expectation` |
| `variance-of-means-is-total` | You left out the spread inside each slice. | `cond-expectation` |
| `forget-the-other-order` | Either person can arrive first. Your region covers only one of the cases. | `geo-prob` |
| `bertrand-has-one-answer` | "Random chord" is not defined until you say how it is drawn. | `geo-prob` |
| `area-on-wrong-space` | The point is uniform on the square, not on the line you drew. | `geo-prob` |
| `monty-fifty-fifty` | The host's choice was not random. Your first pick wins only one time in three. | `game-lab` |
| `ignorant-host-same-as-informed` | A host who might reveal the prize gives different information. | `game-lab` |
| `envelopes-always-switch` | The argument treats one amount as fixed and as random at once. | `game-lab` |
| `expectation-is-enough` | The expected payout is infinite, yet nobody pays much to play. | `game-lab` |
| `bet-more-win-more` | Betting too large a fraction shrinks long-run wealth. | `game-lab` (P2) |
| `forget-the-plus-one` | Every move costs one step before you reach the next state. | `first-step-solver` |
| `restart-from-zero-after-partial-match` | After HH then H, you still have HH. You do not start again. | `first-step-solver`, `trial-strip` |
| `missing-boundary` | The absorbing state needs its own value. | `first-step-solver` |
| `stationary-means-stopped` | Walkers keep moving; only the distribution stays still. | `markov-chain` |
| `rows-or-columns` | Rows are "from", columns are "to". Each row sums to 1. | `markov-chain` |
| `periodic-chain-converges` | This chain alternates for ever. Its distribution does not settle. | `markov-chain` |
| `irreducible-means-aperiodic` | Every state reaches every other, but only in even numbers of steps. | `markov-chain` |
| `reflect-the-wrong-part` | Reflect the part before the first touch, not after it. | `lattice-walk` |
| `all-endpoints-equally-likely` | Central endpoints have many more paths. | `lattice-walk`, `galton-board` |
| `unbiased-is-best` | This biased estimator has the smaller mean squared error. | `estimator-compare` |
| `n-minus-one-is-magic` | $n - 1$ removes bias, but $n + 1$ gives a smaller error for normal data. | `estimator-compare` |
| `consistent-means-unbiased` | This estimator is biased at every $n$, yet it closes in on $\theta$. | `estimator-compare` |
| `likelihood-is-probability-of-theta` | The likelihood need not integrate to 1 over $\theta$. | `likelihood-lab` |
| `mle-is-unbiased` | The MLE of the variance divides by $n$, so it runs low. | `likelihood-lab`, `estimator-compare` |
| `derivative-is-always-zero-at-mle` | Here the peak is at the boundary, where the slope is not zero. | `likelihood-lab` |
| `why-logs` | A product of many small numbers underflows. Logs turn it into a sum. | `likelihood-lab` |
| `ci-is-probability-for-this-interval` | This interval either contains $\mu$ or not. 95% describes the method. | `ci-ladder` |
| `z-at-small-n` | With $s$ in place of $\sigma$ at small $n$, use $t$. | `ci-ladder`, `test-lab` |
| `wald-near-boundary` | Near 0 or 1 the Wald interval undercovers. Read the coverage curve. | `ci-ladder` |
| `wider-is-worse` | A wider interval that keeps its promise beats a narrow one that does not. | `ci-ladder` |
| `p-is-probability-null-true` | The p-value assumes the null is true. It cannot give its probability. | `test-lab`, `icon-array` |
| `fail-to-reject-means-accept` | Not enough evidence against the null is not evidence for it. | `test-lab` |
| `alpha-equals-p` | $\alpha$ is fixed before the data; p comes from the data. | `test-lab` |
| `significant-means-large` | With large $n$, a tiny effect is significant. Look at its size. | `test-lab` |
| `one-sided-after-looking` | Choosing the side after seeing the data doubles the false-alarm rate. | `test-lab` |
| `bonferroni-controls-fdr` | Bonferroni controls the chance of any false alarm, a stricter target. | `multiple-testing` |
| `best-backtest-is-skill` | The best of 200 noise strategies always looks good in sample. | `multiple-testing` |
| `p-hacking-is-harmless` | Trying several analyses and reporting the best inflates false positives. | `multiple-testing` |
| `more-tests-same-error` | Each extra test adds another chance of a false alarm. | `multiple-testing` |
| `r2-measures-truth` | A wrong model can have a high $R^2$. Check the residuals. | `regression-lab` |
| `correlation-is-causation` | The slope describes association in these data, not what happens if you intervene. | `regression-lab` |
| `significant-slope-means-good-model` | The slope is significant, but the residuals curve. The model is wrong. | `regression-lab` |
| `x-must-be-normal` | OLS assumptions concern the errors, not the predictors. | `regression-lab` |
| `extrapolation-is-safe` | Outside the data's range the line is a guess. | `regression-lab` |
| `regress-prices-not-returns` | Prices wander, so their regressions look strong by accident. Use returns or test for cointegration. | `regression-lab`, `coint-lab` |
| `always-delete-outliers` | Find out why the point is far away before removing it. | `regression-lab` |
| `p-of-coef-is-probability-it-is-zero` | $P > \lvert t \rvert$ assumes the coefficient is zero; it does not estimate that chance. | `summary-table` |
| `higher-r2-is-better-model` | Adding noise raised $R^2$. Adjusted $R^2$ fell. | `summary-table` |
| `condition-number-is-an-error` | A large condition number warns of collinearity; the fit still ran. | `summary-table` |
| `durbin-watson-two-is-bad` | Near 2 means no first-order autocorrelation in the residuals. That is good. | `summary-table` |
| `qq-axes-swapped` | Theoretical quantiles are on $x$ here, so an upward bend means a heavy right tail. | `qq-plot` |
| `any-wiggle-means-non-normal` | Small samples wiggle. Compare with the envelope. | `qq-plot` |
| `credible-equals-confidence` | The credible interval is a posterior probability statement. The confidence interval is not. | `posterior-lab`, `ci-ladder` |
| `flat-prior-is-neutral` | Flat in $p$ is not flat in the odds. Every prior says something. | `posterior-lab` |
| `order-of-data-matters` | Updating flip by flip or all at once gives the same posterior. | `posterior-lab` |
| `prior-irrelevant-at-small-n` | With ten flips, the prior still moves the posterior a lot. | `posterior-lab` |
| `prices-are-stationary` | Two windows of this price series have different means. | `series-lab` |
| `trend-or-random-walk` | A random walk can look trended. Differencing, not detrending, fixes it. | `series-lab` |
| `simple-returns-add` | Log returns add across days; simple returns compound. | `series-lab` |
| `one-bar-out-means-dependence` | With 20 lags, about one bar crosses the band by chance. | `acf-lab` |
| `ar-acf-cuts-off` | An AR model's ACF decays; its PACF cuts off. | `acf-lab` |
| `uncorrelated-returns-are-independent` | Returns are uncorrelated, but their squares are not. | `acf-lab`, `garch-lab` |
| `phi-one-reverts` | At $\varphi = 1$ shocks never fade: this is a random walk. | `arma-lab` |
| `ma-has-long-memory` | An MA(1) forgets after one step. Its ACF is zero beyond lag 1. | `arma-lab` |
| `lowest-aic-is-truth` | AIC picks a good forecaster, not necessarily the true model. | `arma-lab` |
| `shuffled-cv-is-fine` | Shuffling lets the model see the future. Validate in time order. | `forecast-lab` |
| `narrow-intervals-are-better` | These intervals cover far less than they claim. | `forecast-lab` |
| `in-sample-fit-is-skill` | It fits the past well and forecasts badly. | `forecast-lab` |
| `volatility-is-constant` | Large moves cluster. Today's variance depends on yesterday's shock. | `garch-lab` |
| `alpha-plus-beta-one-is-fine` | At $\alpha + \beta = 1$ there is no long-run variance to return to. | `garch-lab` |
| `garch-predicts-direction` | GARCH forecasts the size of moves, not their sign. | `garch-lab` |
| `correlation-is-cointegration` | These returns move together, yet the spread wanders. | `coint-lab` |
| `df-critical-values-for-residuals` | You fitted $\beta$ first, so the residual test needs Engle-Granger critical values. | `coint-lab` |
| `high-r2-means-a-relationship` | Two independent random walks: $R^2$ 0.7 and a huge $t$. This is spurious. | `coint-lab`, `regression-lab` |
| `full-sample-beta-in-backtest` | The hedge ratio used data the strategy then traded. That is look-ahead. | `coint-lab` |

---

## 11. Rejected alternatives and open questions

### 11.1 Rejected

| Rejected | Chosen instead | Reason |
|---|---|---|
| A charting library (Plotly, Vega-Lite, Chart.js) for statistics plots | `plot-axes` and `marks` | Plotly alone is several megabytes; none gives handle-level focus, ARIA, hit areas or the grading recolour rule |
| Running statsmodels in the browser for widget numbers | JS `ols` and `tests` checked against fixtures | Pyodide is about 13 MB and cannot run in the Artifact; widgets must answer within a frame |
| jStat for distributions | stdlib-js packages bundled into `stats-core` | stdlib-js ports established numerical libraries and is modular; jStat's tail accuracy is weaker [unverified, to confirm with the fixture tests before final choice] |
| Compiling Cephes or Boost.Math to WebAssembly | Pure JS ports | WebAssembly in the Artifact is unconfirmed [unverified] |
| A physics engine (for example matter.js) for the Galton board | Binomial draws with scripted bounce paths | A physics engine is heavy, nondeterministic across devices, and teaches nothing extra |
| A learner-programmable experiment builder in JS | Registered experiment modules configured by data; custom simulation lives in Python drills | Content must never ship code (calc-linalg 2.4); Python drills already teach simulation |
| Separate Monty Hall, Bayes box, secretary and St Petersburg widgets | `game-lab` modules and `prob-square`'s Bayes mode | One machinery for rounds, policies and exact values instead of four |
| Area-proportional three-set Venn diagrams | Labelled atom masses in `venn-diagram`; areas in `prob-square` | Three circles cannot show arbitrary atom areas exactly |
| WebGL for large point clouds | Canvas 2D with decimation | At most $10^5$ points are drawn; Canvas meets the budget and avoids a second rendering model |
| Grading simulated estimates within a tolerance | Exact values and predictions (section 2.2) | Unlucky seeds would fail correct learners |
| Bundling market data for 2.2 | Synthetic seeded series; learner CSV on the web | Redistribution rights are unclear; synthetic data know the truth |
| The `arch` package in GARCH drills | SciPy optimisation of the learner's likelihood | Availability in Pyodide is unconfirmed, and writing the likelihood is the point of the drill |

### 11.2 Open questions

1. **WebAssembly in the Artifact** decides whether 1.5 and simple 1.6 drills run there under MicroPython [unverified; the probe is running].
2. **Bundle size of `stats-core`** with the stdlib-js functions this cluster needs [unverified; estimated at 100 to 200 KB minified].
3. **Pinned statsmodels and SciPy versions in Pyodide**, which fix the summary layout and the fixture values [unverified].
4. **PACF default method** in the pinned statsmodels, which `ts` must match [unverified].
5. **File input inside the Artifact sandbox** for learner CSVs [unverified].
6. **MCMC.** Blitzstein and Hwang chapter 12 (Metropolis-Hastings, Gibbs) is outside the 1.5 cover list. `markov-chain` has a P2 Metropolis mode in case 2.1 or 3.1 needs it.
7. **Brand review** of `chance-object` art and `icon-array` person glyphs, to keep them generic and distinct from Brilliant's illustration style.

---

## 12. All widgets

### 12.1 New in this catalogue

| # | Id | Kind | Priority | Wave | Curriculum items |
|---|---|---|---|---|---|
| 1 | `mass-editor` | primitive (handle) | P0 | D0 | 1.5.1, 1.5.3, 1.5.7, 1.5.8, 1.6.6; cross-cluster 1.7, 2.1, 2.3, 3.3 |
| 2 | `node-graph` | primitive (host) | P0 | D0 | 1.5.2, 1.5.3, 1.5.6, 1.5.8, 1.5.9; cross-cluster 1.2, 1.8, 2.1 |
| 3 | `chance-object` | primitive (display) | P0 | D0 | 1.5 throughout, 1.6.3, 1.6.6; cross-cluster Stage 0, 3.3 |
| 4 | `prob-square` | composite | P0 | D1 | 1.5.1, 1.5.2 |
| 5 | `icon-array` | composite | P0 (FDR mode P1) | D1 | 1.5.2, 1.6.4 |
| 6 | `contingency-table` | composite | P0 ($\chi^2$ mode P1) | D1 | 1.5.2, 1.5.5, 1.6.4; cross-cluster 2.1 |
| 7 | `odds-ledger` | composite | P0 (Bayes factors P1) | D1 | 1.5.2, 1.6.4, 1.6.6 |
| 8 | `rv-mapper` | composite | P0 | D2 | 1.5.3, 1.5.7 |
| 9 | `dist-explorer` | composite | P0 | D2 | 1.5.3, 1.5.4, 1.5.7, 1.6.1, 1.6.3 |
| 10 | `galton-board` | composite | P0 | D2 | 1.5.3, 1.5.7 |
| 11 | `convolver` | composite | P0 | D2 | 1.5.3, 1.5.4, 1.5.7 |
| 12 | `indicator-board` | composite | P0 | D2 | 1.5.1, 1.5.3, 1.5.4 |
| 13 | `trial-strip` | composite | P0 | D2 | 1.5.3, 1.5.4 |
| 14 | `generating-function` | composite | P0 | D3 | 1.5.4 |
| 15 | `order-statistics` | composite | P0 | D3 | 1.5.4, 1.5.9 |
| 16 | `sampling-lab` | composite | P0 (bootstrap, permutation, p-value modes P1) | D3 | 1.5.4, 1.5.7, 1.6.1 to 1.6.4 |
| 17 | `joint-density` | composite | P0 | D3 | 1.5.5, 1.5.6 |
| 18 | `covariance-lab` | composite | P0 (Anscombe P1) | D3 | 1.5.5, 1.5.7, 1.6.5 |
| 19 | `gaussian-2d` | composite | P0 | D3 | 1.5.5, 1.5.6, 1.6.5 |
| 20 | `cond-expectation` | composite | P0 | D3 | 1.5.6 |
| 21 | `geo-prob` | composite | P0 | D4 | 1.5.5, 1.5.9 |
| 22 | `game-lab` | composite | P0 (Kelly mode P2) | D4 | 1.5.2, 1.5.3, 1.5.9; cross-cluster 3.3 |
| 23 | `first-step-solver` | composite | P0 | D4 | 1.5.2, 1.5.3, 1.5.6, 1.5.8, 1.5.9 |
| 24 | `markov-chain` | composite | P0 (Metropolis P2) | D4 | 1.5.8 |
| 25 | `lattice-walk` | composite | P0 | D4 | 1.5.9 |
| 26 | `estimator-compare` | composite | P1 | E | 1.6.1, 1.6.5 |
| 27 | `likelihood-lab` | composite | P1 | E | 1.6.1 to 1.6.4 |
| 28 | `ci-ladder` | composite | P1 | E | 1.6.3, 1.6.4, 1.6.5 |
| 29 | `test-lab` | composite | P1 (simulated Dickey-Fuller P2) | E | 1.6.4, 1.6.5, 2.2.1, 2.2.2, 2.2.5 |
| 30 | `multiple-testing` | composite | P1 | E | 1.6.4; cross-cluster 3.1 |
| 31 | `regression-lab` | composite | P1 (autocorrelated errors P2) | E | 1.6.5, 2.2.1 |
| 32 | `summary-table` | composite | P1 | E | 1.6.5 (exit) |
| 33 | `qq-plot` | composite | P1 | E | 1.6.5, 2.2.4 |
| 34 | `posterior-lab` | composite | P1 | E | 1.6.3, 1.6.6 |
| 35 | `series-lab` | composite | P2 | F | 2.2.1, 2.2.4 |
| 36 | `acf-lab` | composite | P2 | F | 2.2.2, 2.2.3, 2.2.4 |
| 37 | `arma-lab` | composite | P2 | F | 2.2.1, 2.2.3 |
| 38 | `forecast-lab` | composite | P2 | F | 2.2.3; cross-cluster 2.1 |
| 39 | `garch-lab` | composite | P2 | F | 2.2.4 |
| 40 | `coint-lab` | composite | P2 | F | 2.2.1, 2.2.5 (exit); cross-cluster 3.1 |

**Count:** 40 widgets: 3 primitives and 37 composites. 25 are P0, 9 are P1 and 6 are P2. All 37 composites need generators.

**Build order inside P0.** D0: `stats-core` and the `dist` service, `chance-object`, `mass-editor`, `node-graph`, then the section 4 additions to shared primitives. D1: `prob-square`, `contingency-table`, `icon-array`, `odds-ledger`, with the `outcome-grid`, `tree-diagram`, `trial-simulator`, `counting-slots` and `venn-diagram` extensions. D2: `rv-mapper`, `dist-explorer`, `galton-board`, `indicator-board`, `trial-strip`, `convolver`. D3: `sampling-lab`, `generating-function`, `order-statistics`, `joint-density`, `covariance-lab`, `gaussian-2d`, `cond-expectation`, with the calc-linalg extensions. D4: `geo-prob`, `first-step-solver`, `markov-chain`, `lattice-walk`, `game-lab`.

### 12.2 Reused from the sibling catalogues with a change for this cluster

45 widgets in all.

- **31 composites and inputs with a new mode** (section 5). From Stage 0: `outcome-grid`, `tree-diagram`, `trial-simulator`, `counting-slots`, `venn-diagram`, `pascal-triangle`, `binomial-expander`, `graph-explorer`, `iteration-cobweb`, `stat-chart`, `dot-plot-stats`, `scatter-fit`, `complex-plane`, `card-sort`, `derivation`, `free-response`. From calc-linalg: `function-mapping`, `accumulator`, `region-bounds`, `convexity-chord`, `taylor-builder`, `quadratic-form`, `transform-grid`, `filtration-tree`, `linear-dynamics`, `eigen-finder`, `matrix-multiply`, `path-simulator`, `least-squares-fit`, `surface-explorer`, `sde-stepper`.
- **14 shared primitives with additions** (section 4): `marks`, `plot-axes`, `number-line`, `region-selector`, `slider`, `numeric-entry`, `expression-entry`, `sim-runner`, `data-table`, `matrix`, `token-tray`, `sketch-pad`, `choice-cards`, `code-cell`.
- **One priority change:** `filtration-tree`'s conditional-expectation and tower modes move from P2 to P0.

---

## 13. Cross-cluster needs

### 13.1 Primitives other clusters will need

1. **`mass-editor`**: portfolio weights and allocations (1.7, 2.3), class probabilities and softmax outputs (2.1), bet allocation in betting games (3.3).
2. **`node-graph`**: graph algorithms (1.8: BFS, DFS, Dijkstra, topological sort), Git commit graphs (1.2), computation graphs and network diagrams (2.1); calc-linalg's `dependency-graph` could be built on it.
3. **`chance-object`**: Stage 0 probability (`trial-simulator`), 3.3 betting and market-making games with cards and dice.
4. **`sim-runner` with this cluster's models**: Monte Carlo pricing (1.7), noisy training (2.1), backtests with seeded noise (2.3), stochastic calculus (3.2).
5. **The new `marks` types** (`hist`, `fan`, `intervals`, `glyphs`, `stems`, `step`, fill patterns): price-path fans (1.7), calibration and error bars (2.1), equity curves and drawdowns (2.3).
6. **`region-selector` time brushes**: date ranges in data work (1.1), train and test splits (2.1), backtest windows (2.3).
7. **The `stats-core`, `tests`, `ols` and `ts` services**: Sharpe ratios, information coefficients and factor regressions (2.3, 3.1), logistic and penalised regression diagnostics (2.1).

### 13.2 Composites from this catalogue other clusters should reuse

| Composite | Other uses |
|---|---|
| `contingency-table` | 2.1 confusion matrices, precision and recall |
| `icon-array` | 2.1 base rates and precision; 3.1 false discoveries in factor research |
| `regression-lab`, `summary-table` | 2.1 linear models; 3.1 factor regressions (Fama and French) |
| `forecast-lab` (rolling origin) | 2.1 exit test: time-ordered cross-validation and leakage |
| `coint-lab` | 3.1 pairs-trading replication (Gatev, Goetzmann and Rouwenhorst) |
| `multiple-testing` (strategy zoo) | 2.3 backtest overfitting; 3.1 Harvey, Liu and Zhu |
| `game-lab` | 3.3 betting games and Kelly sizing; a market-making module is a natural P2 addition there |
| `dist-explorer` | 1.7 lognormal prices and $N(d_1)$; 2.1 probabilistic outputs |
| `gaussian-2d` | 1.7 two-asset portfolios; 2.1 Gaussian discriminant analysis |
| `garch-lab` | 2.3 options dashboard (volatility forecasts) |
| `sampling-lab` (bootstrap) | 2.1 bootstrap and bagging |
| `posterior-lab` | 2.1 regularisation as a prior; naive Bayes |

### 13.3 What this catalogue needs from other clusters

| Need | Expected owner | Used in |
|---|---|---|
| `plot-axes` with linked panels, log axes and time axes | engine (both sibling drafts) | nearly every widget here |
| `code-cell` with the helpers in section 4.2 and the fixture pipeline | programming (1.1) and engine | all code drills; both exit tests |
| `expression-entry` probability keyboard layer | engine | 1.5 expression answers |
| `matrix` with row-stochastic editing | linear algebra (calc-linalg) | `markov-chain`, `first-step-solver` |
| `sketch-pad` with step features | calc-linalg | 1.5.3 L3 |
| The shared RNG with a portable Python port | engine | every simulation and drill |
| Bertie's face and pointer beside annotated elements, and the `secret()` channel in the tutor prompt | engine and tutor blueprint | every `annotate` call; section 2.7 |

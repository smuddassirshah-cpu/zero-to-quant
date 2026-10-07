# Widget catalogue: calculus, linear algebra and stochastic calculus

Working paper for the Stage 2 Blueprint, 6 October 2026. Scope: curriculum items 1.3 Calculus, 1.4 Linear algebra and 3.2 Stochastic calculus. Input to `docs/PLAN.md` (component tree, interfaces and execution stages for the widget library).

**How to read it.**

- Section 1 walks every lesson in the three topics and names what the learner must manipulate, see, build or predict. Every widget below exists because a row in section 1 needs it.
- Section 2 is the shared contract that every widget follows. Per-widget entries only state what differs from it, so read section 2 first.
- Sections 3 to 7 specify the widgets: primitives first, then composites by topic.
- Sections 8 to 10 cover screens that need no composite, generators, and rejected alternatives with open questions. The document ends with the full widget table (section 11) and cross-cluster needs (section 12).

**Numbering.** Course and lesson numbers (1.3.1 to 1.3.8, 1.4.1 to 1.4.7, 3.2.1 to 3.2.4, and L1, L2 inside them) are this catalogue's working outline, written to test coverage. The course-architecture blueprint owns the final outline; renumbering it changes no widget.

**Evidence tags** follow the design research: [our choice] for decisions without Brilliant evidence, [unverified] for facts not yet measured, [inferred] for deductions. Untagged design values come from `docs/design-research.md` or the Stage 1 prototype.

---

## 0. Decisions in brief

1. **76 widgets: 58 composites on 18 primitives.** A composite is configuration plus a small amount of widget-specific logic (state derivation, check functions, show-why recipes). A composite may not draw anything a mark cannot draw: a new drawing need becomes a new mark type, so every widget gains it.
2. **Expressions are data, compiled without `eval`.** Widget configs carry maths as restricted ASCII expressions (`x^2*sin(1/x)`), compiled by a shared `expr` module into closures. The same module differentiates symbolically and computes Taylor coefficients by truncated power-series arithmetic, so authors never hand-write a derivative. This sidesteps any Artifact CSP question about `unsafe-eval` [our choice].
3. **Exact arithmetic where the learner computes by hand.** Elimination, RREF, inverses and determinants use BigInt fractions, so $\tfrac{1}{3}$ never shows as 0.3333. Floats are used for eigen-solvers, SVD, quadrature and simulation [our choice].
4. **SVG by default, Canvas 2D for heavy layers, no WebGL.** Path bundles, heatmaps, dense scatter and 3D meshes go to canvas; everything a learner can focus or a screen reader can name stays in SVG or DOM. 3D uses a hand-written projection with painter's sorting. Three.js is rejected (section 10) [our choice].
5. **Learner-controlled objects are manipulable blue; derived series start at slot 2.** In any plot with a handle, series slot 1 (#2A78D6) is skipped because it is too close in hue to manipulable blue (#2F6BFF). This needs design sign-off [our choice].
6. **Show-why is declarative.** Each misconception maps to a recipe of variable tweens, highlights and annotations, played on non-answer state and undone on Try again. Authors write recipes, not animation code [our choice].
7. **Every drag has a typed path.** Pressing E (or double-tapping) on any handle opens an exact-value editor. This is the keyboard and screen-reader route, and the precision route for everyone [our choice].
8. **The tutor reads `describe()` and points with element ids.** Bertie's reply is one JSON object (what to say, which ids to highlight, which to annotate). Highlights ride in the reply, not as tool calls, so a hint costs one model round. The tutor can never change answer state; it can offer a "Try this" chip the learner taps [our choice].
9. **Counter-based random numbers and refinable Brownian paths.** Any random draw is addressable by (seed, stream, index), so adding paths never changes existing ones. Brownian paths are built by midpoint (bridge) refinement, so refining a partition keeps the coarse path fixed. Quadratic variation and Itô sums depend on this [our choice].
10. **Priority.** Every widget that a 1.3 or 1.4 lesson needs is P0, because the depth-first build runs through 1.5. Two widgets are P1: `binomial-tree` (first needed in 1.7) and `condition-number` (first needed in 1.6; it is outside 1.4's cover list). Ten stochastic-calculus widgets are P2. `path-simulator` is P0 for its random-walk modes, which 1.5 needs. Some P0 widgets carry later modes, marked in their entries.

---

## 1. Lesson map: what the learner does to get each idea

Each row is one lesson. "Act" is the hook: the action taken before any rule is read. "Check" is the main answer type.

### 1.1 Calculus (1.3, 200 h; MIT 18.01, the 18.02 units on partials and Lagrange multipliers, Stewart or OpenStax)

**1.3.1 Limits and continuity**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Approaching a value | Drag two handles towards $x=2$ on $f(x)=\frac{x^2-4}{x-2}$ and predict the height they approach before the hole is shown | limit-explorer | numeric |
| 2 | One-sided limits, jumps, holes, asymptotes | On four graphs, approach from each side and record both one-sided limits; say where the limit exists | limit-explorer | multi (numeric with DNE), choice |
| 3 | Limits at infinity and growth rates | Push $x$ to $10^6$ on a log axis; order $\ln x$, $x^3$, $e^x$, $x!$ by who wins | limit-explorer (infinity), token-tray | ordering |
| 4 | Squeeze theorem; $\frac{\sin x}{x}$ | Shrink an angle on the unit circle and watch triangle, sector and triangle squeeze the ratio | unit-circle (0.3 cluster), limit-explorer (bounds) | numeric |
| 5 | Sequences; $e$ from compounding | Raise the compounding frequency $n$; predict where $(1+\frac1n)^n$ settles | limit-explorer (sequence) | numeric |
| 6 | Continuity and the intermediate value theorem | Halve a bracket until a root is pinned to 3 decimals; pick the function where the theorem fails | root-finder (bisection), choice | numeric, choice |
| 7 | The $\varepsilon$-$\delta$ definition | Beat the adversary: for each $\varepsilon$ it picks, choose a $\delta$ that keeps the graph in the box; then write $\delta(\varepsilon)$ | epsilon-delta | predicate, expression |

**1.3.2 The derivative**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Average to instantaneous rate | Slide $Q$ towards $P$; predict the slope the secants approach | secant-tangent | numeric |
| 2 | Local linearity | Zoom on $x^2$, $\lvert x\rvert$ and $x\sin\frac1x$: which turn into straight lines? | local-zoom | choice |
| 3 | The derivative as a function | Trace the slope while dragging along $f$; then sketch $f'$ for a new $f$ before tracing | derivative-tracer | curve |
| 4 | Power rule | Grow a square and a cube by $dx$; label the new pieces; watch $dx^2$ vanish | growth-rectangle, derivation-steps | set, expression |
| 5 | Product and quotient rules | Grow an $f$ by $g$ rectangle; which strips survive as $dx \to 0$? | growth-rectangle, expression-input | set, expression |
| 6 | Chain rule | Nudge $x$ and follow the stretch through $g$, then $f$; predict the overall stretch | function-mapping (chain) | numeric, expression |
| 7 | $e^x$ and $\ln x$ | Find the base $b$ whose graph has slope equal to its height; then invert the map | derivative-tracer (base slider), function-mapping (inverse) | numeric |
| 8 | Trigonometric derivatives | Drag $\theta$ round the unit circle; the point's vertical speed is $\cos\theta$ | unit-circle (0.3 cluster), derivative-tracer | curve, expression |
| 9 | Implicit, inverse and parametric derivatives | Drag a point round a circle and read the tangent slope; predict $-x/y$ | secant-tangent (implicit, parametric) | numeric, expression |
| 10 | Related rates | Pull a ladder's foot at 0.5 m/s; how fast does the top fall when the foot is 3 m out? | rates-scene | numeric |
| 11 | Linear approximation; Newton's method | Estimate $\sqrt{4.1}$ with a tangent line; iterate tangents to a root, including a start that cycles | local-zoom (tangent), root-finder (Newton) | numeric, point, choice |
| 12 | Mean value theorem | Find where the tangent is parallel to the chord | secant-tangent (mvt) | point |
| 13 | L'Hôpital's rule | Zoom in where $f$ and $g$ both vanish: their ratio becomes a ratio of slopes | local-zoom (ratio) | numeric |

**1.3.3 Shape and optimisation**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Increasing, decreasing, critical points | Mark where $f'$ changes sign; deduce peaks and troughs | sign-chart, derivative-tracer | set |
| 2 | Concavity, inflection, second-derivative test | Mark where the curve bends up or down; predict the signs of $f''$ | derivative-tracer ($f''$), sign-chart | set, choice |
| 3 | Curve sketching | Sketch $\frac{x}{1+x^2}$ from its sign charts and end behaviour | sketch-pad on plot-2d | curve with features |
| 4 | Optimisation in geometry | Cut squares from a sheet to make the biggest open box; then prove it with $V'(x)=0$ | objective-explorer | point, expression |
| 5 | Optimisation in finance | Choose a bet fraction that maximises log growth (Kelly); a weight that minimises two-asset variance | objective-explorer (presets) | numeric |
| 6 | Convexity and Jensen's inequality | Drag a chord along a convex curve; then show $E[f(X)] \ge f(E[X])$ with a two-point $X$ | convexity-chord | choice, numeric |

**1.3.4 Integration**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Area by rectangles | Predict over or under; raise $n$ until the error is below 0.01 | riemann-sum | choice, numeric |
| 2 | The definite integral; signed area | Integrate across a root: why does the sum shrink? | riemann-sum (signed), accumulator | numeric |
| 3 | Accumulation and the fundamental theorem | Drag $x$: the slope of $A$ at $x$ equals the height of $f$ at $x$ | accumulator (ftc) | numeric, curve |
| 4 | Antiderivatives, $+C$, slope fields | Move the start point $a$: the whole $A$ curve lifts; fit a curve to a slope field | accumulator, slope-field | curve, expression |
| 5 | Substitution | Watch a $dx$ strip become a $du$ strip with the same area | function-mapping (substitution), expression-input | expression |
| 6 | Integration by parts | Split the $uv$ rectangle under a parametric curve into two areas | primitive screen (section 8), derivation-steps | expression |
| 7 | Partial fractions, trigonometric substitution | Complete the missing line of each derivation | derivation-steps | expression, ordering |
| 8 | Improper integrals | Push the upper limit to infinity for $x^{-p}$; which $p$ converge? | accumulator (improper) | choice, numeric |
| 9 | Area between curves; average value; arc length | Find the level whose rectangle has the same area as $f$ | riemann-sum (two curves, average), primitive screen | numeric |
| 10 | Volumes of revolution | Sweep a region round an axis; choose discs or shells | solid-of-revolution | numeric, expression |
| 11 | Numerical integration and its error | Double $n$: by what factor does the midpoint error shrink? Simpson's? | riemann-sum (error inset) | numeric |
| 12 | Differential equations; Euler's method; continuous compounding | Step Euler with $h=0.5$ and $h=0.1$; predict the next point | slope-field | point, numeric |
| 13 | Densities: area as probability | Shade $P(1<X<2)$ under a density and watch the CDF trace | accumulator (density) | numeric |

**1.3.5 Series and Taylor**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Partial sums; geometric series | Halve a square forever; predict the total | series-explorer (geometric picture) | numeric |
| 2 | Divergence; harmonic series; integral test | The terms go to zero, so does it converge? Push $N$ to $10^6$ | series-explorer | choice |
| 3 | Comparison, ratio and alternating tests | Read the ratio $a_{n+1}/a_n$ settling; bound an alternating tail | series-explorer | choice, numeric |
| 4 | Power series; radius of convergence | Move $x$ and watch partial sums settle or explode; mark the interval | series-explorer (power) | interval |
| 5 | Taylor polynomials by matching derivatives | Set four coefficients by hand so a cubic hugs $e^x$ at 0 | taylor-builder (match) | numeric |
| 6 | Taylor's theorem and the remainder | Where does the degree-3 polynomial first miss by more than 0.01? | taylor-builder (remainder) | point, numeric |
| 7 | The standard series | Build $\sin x$, $\ln(1+x)$ and $(1+x)^\alpha$; spot each radius | taylor-builder | expression |
| 8 | Euler's formula | Add the terms of $e^{i\theta}$ as arrows; they spiral onto the unit circle | series-explorer (complex) | point |
| 9 | Duration, convexity, delta and gamma | Approximate a bond's price change with a line, then a parabola | taylor-builder (bond, option presets) | numeric |

**1.3.6 Functions of several variables**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Surfaces and contour maps | Find the summit using only the contour map, then check in 3D | surface-explorer | point |
| 2 | Partial derivatives | Slice the surface along $x$ and along $y$; read both slopes | surface-explorer (slices) | numeric |
| 3 | Tangent planes; linear approximation | Toggle the tangent plane; estimate $f$ near the point | surface-explorer | numeric |
| 4 | Multivariable chain rule | Build the dependency tree; add one product per path | dependency-graph | set, expression |
| 5 | Directional derivative and gradient | Turn a needle to find the steepest way up; notice it crosses the contour at a right angle | gradient-compass | angle, numeric |
| 6 | Gradient descent | Pick the learning rate that converges fastest without blowing up | descent-lab | numeric, choice |
| 7 | Critical points; second-derivative test | Morph a quadratic between bowl, saddle and ridge; classify Hessians | quadratic-form (hessian), surface-explorer | choice |
| 8 | Least squares as minimisation | Find the bottom of the error bowl over (intercept, slope) | least-squares-fit (error map) | point |

**1.3.7 Multiple integrals**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Volume by columns | Refine the grid; predict the limiting volume | volume-slicer (columns) | numeric |
| 2 | Iterated integrals by slicing | Sweep a slice and plot its area $A(x)$; the volume is the area under $A$ | volume-slicer (slices) | expression, numeric |
| 3 | Setting up bounds; swapping the order | Slide a strip across the region and write where it starts and stops; then turn the strip | region-bounds | predicate, expression |
| 4 | Polar coordinates; the Gaussian integral | Build $\iint e^{-(x^2+y^2)}\,dA$ from rings; take the square root | volume-slicer (shells), region-bounds (polar), derivation-steps | numeric |
| 5 | Change of variables; the Jacobian | Map a tiny square through $(r,\theta)\mapsto(x,y)$ and measure its area factor | transform-grid (nonlinear) | numeric |
| 6 | Probability over regions | Integrate a joint density over $x+y<1$ | region-bounds (density) | numeric |
| 7 | Triple integrals | Stack a solid's $z$-bounds over its shadow region | region-bounds (3D) | predicate |

**1.3.8 Constrained optimisation**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Optimising along a constraint | Walk along a circle and watch $f$ rise and fall | lagrange-explorer (profile) | point |
| 2 | Tangency and parallel gradients | At the best point the contour just touches the constraint; draw both gradients | lagrange-explorer | choice, expression |
| 3 | The multiplier as a shadow price | Loosen the constraint by 0.1; predict the change in the optimum | lagrange-explorer (shadow price) | numeric |
| 4 | Three variables | Find the point on a plane closest to the origin | lagrange-explorer (3D), derivation-steps | numeric |
| 5 | Minimum-variance portfolio | Move weights on a triangle of portfolios; find the least risky one | lagrange-explorer (simplex) | point, numeric |

KKT conditions for inequality constraints are not in the curriculum's cover list or exit; `lagrange-explorer` can show a binding or slack inequality as an extension in 2.1 (section 10).

### 1.2 Linear algebra (1.4, 150 h; Strang, MIT 18.06)

**1.4.1 Vectors**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Linear combinations | Reach the target with $c\mathbf v + d\mathbf w$ | vector-combo | numeric |
| 2 | Span | Which targets can never be reached? Paint everything reachable, in 2D then 3D | vector-combo (span) | choice, predicate |
| 3 | Length, dot product, angle | Rotate $\mathbf b$ round $\mathbf a$; watch $\mathbf a\cdot\mathbf b$ change sign at $90^\circ$ | projection-lab (dot) | choice, numeric |
| 4 | $A\mathbf x$ as a combination of columns | Compute $A\mathbf x$ by stacking columns, not rows | vector-combo (columns), matrix-multiply (column view) | matrix |

**1.4.2 Solving linear equations**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Row and column pictures | Find the solution where the lines meet, then as weights on the columns | row-column-picture | numeric |
| 2 | Elimination | Choose multipliers that clear below each pivot | elimination-lab | matrix, numeric |
| 3 | Breakdown: exchanges and singular systems | Hit a zero pivot and swap; then meet a system with no pivot left | elimination-lab, row-column-picture | choice |
| 4 | Matrix multiplication four ways | Fill $AB$ by entries, by columns, by rows, by outer products | matrix-multiply | matrix |
| 5 | $A = LU$ | Record each multiplier and watch $L$ fill itself | elimination-lab (LU) | matrix |
| 6 | Inverses by Gauss-Jordan | Reduce $[A\;I]$ to $[I\;A^{-1}]$ | elimination-lab (inverse) | matrix |
| 7 | Transposes, permutations, symmetric matrices | Predict where $P$ sends each row of $A$ | matrix-multiply, choice | matrix |
| 8 | Matrices as transformations | Drag where $\mathbf e_1$ and $\mathbf e_2$ land so the grid's F matches the target | transform-grid | matrix |

**1.4.3 Vector spaces and rank**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Subspaces | Break closure: find two vectors in the set whose sum escapes | subspace-tester | predicate, choice |
| 2 | Column space and nullspace | Squash the plane; which inputs land on $\mathbf 0$? | transform-grid (singular), solution-set | choice |
| 3 | $A\mathbf x=\mathbf 0$: RREF, pivots, free variables | Reduce, circle pivots, set each free variable to 1 in turn | elimination-lab (RREF), solution-set | set, matrix |
| 4 | Rank and the complete solution | Move free-variable sliders: the solutions form a shifted line or plane | solution-set | expression, choice |
| 5 | Independence, basis, dimension | Drag three vectors until their box flattens | vector-combo (3D independence) | choice |
| 6 | The four fundamental subspaces | Sort vectors into the four boxes; fill in $r$, $n-r$, $r$, $m-r$ | four-subspaces | set, numeric |
| 7 | Change of basis | Read a point's coordinates on a skewed grid | basis-change | numeric |
| 8 | Linear maps beyond arrows | Write $\frac{d}{dx}$ on cubics as a $4\times4$ matrix | primitive screen (section 8) | matrix |

**1.4.4 Orthogonality**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Orthogonal subspaces | Show the nullspace is perpendicular to every row | four-subspaces (geometric), projection-lab | choice |
| 2 | Projection onto a line | Drop $\mathbf b$ onto $\mathbf a$: predict where it lands | projection-lab (predict) | point |
| 3 | Projection onto a plane | Drop $\mathbf b$ onto the plane of two columns; $\mathbf e$ meets both at right angles | projection-lab (plane) | point, matrix |
| 4 | Least squares | Drag a line to make the squares on the residuals as small as possible | least-squares-fit | point, numeric |
| 5 | Normal equations; the picture in $\mathbb R^m$ | With three data points, see $\mathbf b$, $\mathbf p$ and $\mathbf e$ in $\mathbb R^3$ | least-squares-fit (r3), projection-lab | matrix |
| 6 | Orthonormal bases; Gram-Schmidt; QR | Predict each new orthogonal vector before it is drawn | gram-schmidt | point, matrix |
| 7 | CAPM beta | Regress a stock's returns on the market's, then code it | least-squares-fit (capm), code-cell | numeric, code |

**1.4.5 Determinants**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Area and volume | Drag the columns: the parallelogram's signed area is $\det A$ | determinant-lab, transform-grid | numeric |
| 2 | Properties through row operations | Shear, swap, scale: predict each change in area | determinant-lab (properties) | choice |
| 3 | Cofactors, Cramer's rule, the inverse formula | Expand along the row with most zeros | determinant-lab (cofactor, cramer) | numeric |

**1.4.6 Eigenvalues**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Directions that do not turn | Spin $\mathbf x$ until $A\mathbf x$ lies on the same line | eigen-finder | angle, numeric |
| 2 | $\det(A-\lambda I)=0$ | Slide $\lambda$ until the circle's image collapses to a segment | eigen-finder (lambda-shift) | numeric, expression |
| 3 | Trace, determinant, complex eigenvalues | A rotation: no direction survives; read $\lambda$ from trace and determinant | eigen-finder | choice |
| 4 | Diagonalisation and powers | Split $\mathbf x_0$ along the eigenvectors; predict $\mathbf x_{10}$ | linear-dynamics, basis-change (diagonalise) | numeric |
| 5 | Markov matrices | Iterate a population until it stops changing | linear-dynamics (markov) | point |
| 6 | $\frac{d\mathbf u}{dt}=A\mathbf u$ | Drop starting points into the flow; classify the origin | linear-dynamics (continuous) | choice |
| 7 | Symmetric matrices; spectral theorem | Turn a circle into an ellipse whose axes are perpendicular eigenvectors | svd-stepper (spectral), quadratic-form | angle |

**1.4.7 Positive definite matrices, SVD and PCA**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Tests for positive definiteness | Push the off-diagonal entry until the bowl becomes a saddle | quadratic-form | choice, set |
| 2 | Valid covariance and correlation matrices | Given two correlations, find the range the third can take | quadratic-form (correlation-3) | numeric |
| 3 | Cholesky | Factor $A=LL^\top$ and use $L$ to make correlated noise | quadratic-form, path-simulator (2D) | matrix |
| 4 | SVD geometry | Rotate, stretch, rotate: build $A$ from the ellipse it makes | svd-stepper | numeric, angle |
| 5 | Low-rank approximation | Keep $k$ layers; how many for 90% of the energy? | low-rank-approx | numeric |
| 6 | Pseudoinverse | Map back from the column space | svd-stepper (pseudoinverse) | matrix |
| 7 | Principal component analysis | Spin a line to catch the most variance | pca-lab | angle, numeric |
| 8 | PCA on yield-curve changes | Name the three loading shapes, then code PCA in NumPy | pca-lab (loadings), code-cell | set, code |

### 1.3 Stochastic calculus (3.2, optional; Shreve volumes I and II)

**3.2.1 Discrete time**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | One-period model; replication; no arbitrage | Build a stock-and-bond portfolio that copies the option in both states | binomial-tree (replicate) | numeric |
| 2 | Multi-period pricing | Fill the tree backwards | binomial-tree (price) | numeric per node |
| 3 | Risk-neutral probabilities | Choose $q$ so the discounted stock is a fair game | measure-change (discrete), binomial-tree | numeric |
| 4 | Information and conditional expectation | Average over the outcomes you cannot yet tell apart | filtration-tree | numeric per atom |
| 5 | Martingales and Markov processes | Test whether a process is fair at every node | filtration-tree (martingale) | choice |
| 6 | Stopping times; American options | Mark early-exercise nodes; is "first time above 8" a stopping time? | binomial-tree (american), filtration-tree | set, choice |
| 7 | Random walk: first passage and reflection | Reflect a path after it first touches $m$ | reflection-principle (walk), path-simulator | numeric |

**3.2.2 Brownian motion**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | From random walks to Brownian motion | Shrink steps and time together; what must the step size be? | path-simulator (scaled) | choice, numeric |
| 2 | Properties; nowhere differentiable | Zoom into a Brownian path: it never straightens | path-simulator, local-zoom (Brownian) | choice |
| 3 | Quadratic variation | Refine the partition; predict $\sum(\Delta W)^2$ | quadratic-variation | numeric |
| 4 | Reflection and the running maximum | Predict $P(\max_{t\le1} W_t \ge 1)$, then tally | reflection-principle | numeric |
| 5 | Correlated Brownian motions | Use the Cholesky factor to correlate two paths | path-simulator (2D), quadratic-form | numeric |

**3.2.3 Itô calculus**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | The Itô integral | Compare left, average and right sums of $W\,dW$ as the partition refines | ito-sum | numeric |
| 2 | Itô isometry; martingale property | Average the left sums over many paths | ito-sum | numeric |
| 3 | Itô's lemma | Predict whether $E[W_t^2]$ rises; fill the $dW\cdot dW$ table | ito-lemma-lab, derivation-steps | choice, expression |
| 4 | Geometric Brownian motion; volatility drag | Predict the median path for $\mu=5\%$, $\sigma=40\%$ | gbm-lab | choice, numeric |
| 5 | SDEs; mean reversion | Step an Ornstein-Uhlenbeck process; read its half-life | sde-stepper | numeric |

**3.2.4 Pricing**

| L | Idea | Act | Widgets | Check |
|---|---|---|---|---|
| 1 | Black-Scholes-Merton by delta hedging | Rebalance more often; how fast does the hedge error shrink? | hedging-sim | numeric |
| 2 | Risk-neutral measure; Girsanov | Reweight paths until the discounted price is a martingale | measure-change | numeric |
| 3 | Feynman-Kac; the heat equation | Predict the price curve a month before expiry from the payoff | heat-diffusion | curve |
| 4 | Monte Carlo for exotic payoffs | Price an Asian option; watch the confidence interval shrink like $1/\sqrt N$ | gbm-lab (price) | numeric |
| 5 | Short-rate models | Simulate Vasicek and CIR; when can CIR reach zero? | sde-stepper | choice |

Text-led lessons without a dedicated widget, by decision: measure-theoretic foundations (Shreve II chapter 1), change of numéraire, the martingale representation theorem and Heath-Jarrow-Morton. They use `derivation-steps` and the engine's free-text items (section 10).

---
## 2. Shared contract

Every widget in sections 3 to 7 follows this section. A per-widget field that says "base" means this section applies unchanged.

### 2.1 Taxonomy

| Kind | What it is | Members |
|---|---|---|
| Host | Owns a coordinate space, its transforms, hit testing and table view | `plot-2d`, `plot-3d`, `number-line`, `matrix` |
| Mark | Passive, declarative layer inside a host, with a stable id | `marks` (one primitive, many mark types) |
| Handle | A learner-moved element inside a host | `drag-point`, `sketch-pad`, `region-select` |
| Control | An input outside the canvas | `slider`, `stepper`, `token-tray`, `value-table`, `choice`, `numeric-input`, `expression-input`, `code-cell` |
| Runner | Produces data over time from a seed | `sim-runner` |
| Display | Typeset maths bound to live values | `live-formula` |
| Composite | Primitives plus widget-specific state derivation, checks and show-why recipes | sections 4 to 7 |

Rules [our choice]:

- A composite never draws pixels itself. If it needs a new shape, the shape becomes a mark type in `marks`.
- A composite owns no pointer handling beyond what its handles provide. Gestures live in primitives so keyboard paths, hit areas and reduced motion are solved once.
- A composite is a module exporting `type`, a config validator, `create()`, its named check functions, its show-why recipes and its generators.
- Lesson content is data: a screen lists widget configs and a check. No lesson ships its own JavaScript. This is the response to the Stage 1 finding that a hand-built 12-minute lesson took 1,316 lines and still had 23 defects, mostly in machinery.

### 2.2 Lifecycle interface

```ts
type Id = string;

interface Widget<C extends BaseConfig, S> {
  readonly type: string;                 // 'riemann-sum'
  mount(el: HTMLElement, cfg: C, ctx: WidgetContext): void;
  getState(): S;                         // JSON-serialisable; saved for resume
  setState(s: Partial<S>, how?: 'instant' | 'spring' | 'explain'): void;
  reset(): void;                         // "Start over"
  lock(on: boolean): void;               // evaluating and graded states (design 5.4)
  answer(): AnswerPayload | null;        // null keeps Check disabled (idle state)
  showGrade(g: GradeResult): void;       // recolours answer objects, runs show-why
  clearGrade(): void;                    // Try again: frame neutral, input kept
  reveal(): Promise<void>;               // Show solution: morph to solved state, indigo outlines
  describe(level: 'brief' | 'full'): string;
  ids(): Array<{ id: Id; name: string }>;  // every element the tutor or a hint may point at
  highlight(ids: Id[], style: 'point' | 'dim-others'): () => void;  // returns an undo
  annotate(id: Id, text: string): { anchor: DOMRect; remove(): void };
  snapshot?(): Promise<Blob>;            // PNG for image-capable tutor calls only
  destroy(): void;
  on(ev: 'engage' | 'change' | 'commit', fn: (s: S) => void): () => void;
}

interface WidgetContext {
  target: 'artifact' | 'web';
  rng(stream: string): Rng;              // counter-based, seeded from the screen seed
  reducedMotion(): boolean;
  announce(text: string, opts?: { on: 'commit' | 'now'; throttleMs?: number }): void;
  tex(src: string, display?: boolean): string;   // KaTeX, shared cache
  expr: ExprCore;                        // section 2.13
  linalg: LinalgCore;
  worker(name: string): WorkerHandle;    // own-file worker, both targets
  tokens(): DesignTokens;                // read at draw time; re-read on theme change
}
```

`engage` fires on the first learner change and moves the Check button from idle to engaged. `commit` fires on pointer up, key up, or a value typed and confirmed; announcements and saves happen on commit, never per frame.

### 2.3 Base config and expressions

```ts
type Expr = string;   // restricted ASCII maths, compiled by ctx.expr, never passed to eval
type Vec2 = [number, number];
type Entry = number | string;   // string: exact rational '3/4', symbol 'a', or an Expr

interface BaseConfig {
  id: Id;                         // instance id, unique on the screen
  label: string;                  // accessible name; also how the tutor names the widget
  seed?: number;                  // set by generators; default derives from the screen id
  vars?: Record<string, number>;  // initial widget variables that Exprs may reference
  check?: CheckSpec;              // absent: explore-only, Continue without Check
  readonly?: boolean;             // Demonstrate screens, quiz review
  hints?: Array<{ rung: 'nudge' | 'point' | 'step'; text: string; highlight?: Id[] }>;
  showWhy?: Record<MisconceptionId, ShowWhy>;
  tutor?: { focus?: Id[]; notes?: string };   // authored context for Bertie
  a11y?: { summary?: string };    // overrides describe('brief') where the computed text is weak
}
```

**Expression grammar** [our choice]: decimal and scientific numbers; identifiers; `+ - * / ^`, unary minus and parentheses. Multiplication is explicit (`2*x`), because implicit multiplication makes `xy` ambiguous. Functions: `sin cos tan asin acos atan atan2 sinh cosh tanh exp ln log10 sqrt cbrt abs sign floor ceil min max if(cond, a, b) Phi phi erf`, plus `sum(k, lo, hi, term)` for finite sums. Constants `pi` and `e`. Comparisons `< <= > >= ==` only inside `if`. Undefined points (division by zero, logarithm of a non-positive number) evaluate to `NaN`, and curve samplers treat `NaN` as a break: that is how holes and asymptotes are drawn.

### 2.4 Answer and check types

```ts
type CheckSpec =
  | { kind: 'choice'; correct: Id | Id[]; misconceptions?: Record<Id, MisconceptionId> }
  | { kind: 'numeric'; value: number | Expr; tol: Tolerance; specials?: Array<'DNE' | 'inf' | '-inf'> }
  | { kind: 'expression'; equals: string; vars: string[];
      mode?: 'equal' | 'antiderivative' | 'equal-up-to-constant';
      form?: 'any' | 'factored' | 'expanded' | 'single-fraction';
      domain?: Record<string, [number, number]> }
  | { kind: 'set'; correct: Id[]; partial?: boolean }
  | { kind: 'interval'; correct: Array<{ a: number; b: number; openA: boolean; openB: boolean }>; tol: number }
  | { kind: 'ordering'; correct: Id[]; marks: 'all-or-nothing' | 'per-position' }
  | { kind: 'point'; target: number[] | number[][]; tol: number;
      metric: 'euclid' | 'x' | 'y' | 'angle' | 'angle-mod-pi' }       // number[][]: any of several
  | { kind: 'curve'; target: Expr; band: number; coverage: number; features?: Feature[] }
  | { kind: 'matrix'; equals: Entry[][]; tol?: number;
      relation: 'equal' | 'echelon-row-equivalent' | 'rref' | 'columns-up-to-scale' | 'orthonormal-columns' }
  | { kind: 'predicate'; name: PredicateName; args?: Record<string, unknown> }
  | { kind: 'code'; suite: Id; compare: 'isclose' | 'allclose' | 'exact' | 'allclose-up-to-sign' }
  | { kind: 'free-text'; rubric: Array<{ point: string; marks: number }>; model: string;
      marking: 'self' | 'tutor-draft' }
  | { kind: 'multi'; parts: Record<string, CheckSpec> };

type Tolerance = { abs?: number; rel?: number };

type Feature =
  | { kind: 'zero'; x: number; tol: number }
  | { kind: 'sign'; on: [number, number]; sign: 1 | -1 }
  | { kind: 'extremum'; x: number; type: 'max' | 'min'; tol: number }
  | { kind: 'concavity'; on: [number, number]; sign: 1 | -1 }
  | { kind: 'monotone'; on: [number, number]; dir: 1 | -1 }
  | { kind: 'asymptote'; x?: number; y?: number };

interface GradeResult {
  ok: boolean;
  parts?: Record<string, boolean>;       // multi-part: green parts lock, amber parts reopen
  misconception?: MisconceptionId;       // selects the show-why recipe and verdict line
  accepted: string;                      // the accepted-answer rule shown after grading
  answerObjects: Id[];                   // the only elements grading may recolour
}
```

How each type maps to the task's list:

| Task type | Kinds | Notes |
|---|---|---|
| choice | `choice` | Each distractor names one misconception (design 5.6) |
| numeric with tolerance | `numeric` | `specials` adds DNE, $\infty$, $-\infty$ keys for limits; the accepted range is shown after grading |
| expression | `expression` | CAS equivalence (Compute Engine), cross-checked by numeric sampling at 8 seeded points with our `expr`; disagreement between the two is logged as a content bug. `antiderivative` differentiates the learner's answer and compares with the integrand; `equal-up-to-constant` ignores $+C$ |
| set or region | `set`, `interval`, `predicate` | Regions defined geometrically are checked by `predicate` (rasterised symmetric difference) |
| ordering | `ordering` | Per-line marks after grading (design 5.3 item 15) |
| point or curve within tolerance | `point`, `curve` | `angle-mod-pi` treats $\mathbf x$ and $-\mathbf x$ as the same direction (eigenvectors, principal components). `curve` passes when the sketch stays inside the band over `coverage` of the domain and every feature holds |
| matrix | `matrix` | Exact rational equality by default; `echelon-row-equivalent` accepts any correct echelon form |
| code tests | `code` | Runs in `code-cell`; `allclose-up-to-sign` for eigenvectors and principal components |
| free text | `free-text` | Self-marked against a model answer and rubric; `tutor-draft` lets Bertie propose a mark the learner confirms |

**Predicates** are named, pure, unit-tested functions in a registry. Content can name them and pass arguments; content can never supply code. The predicates this cluster needs: `delta-works`, `delta-formula-works`, `outside-span`, `closure-counterexample`, `bounds-describe-region`, `same-affine-set`, `is-echelon-row-equivalent`, `is-eigenvector`, `arbitrage-profitable`, `is-stopping-time`, `mvt-point`.

### 2.5 Visual rules for this cluster

- **Roles by colour** [our choice, needs design sign-off]:
  - Given objects (the function, the data, fixed vectors): ink, 2px.
  - Learner-controlled objects (handles, the learner's line, strip, direction or sketch): manipulable blue `--manip`, handles with a 2px white ring and 1px ink outline.
  - Derived objects (tangent, secant, $f'$, projection, approximation): series slots in the order s2, s3, s4, s6. In any plot that has a handle, s1 is skipped: #2A78D6 sits too close in hue to `--manip` #2F6BFF. Plots without handles use s1 first, as section 2.6 of the design research says.
  - Slots s4 and s5 appear only with a direct label and at least a 2px stroke or 20% fill, and never as the only cue.
- **Targets and ghosts:** dashed ink, 1.5px, 6 on and 4 off.
- **Fills:** at most 25% opacity, so gridlines read through.
- **Show-why highlights:** the focus wash (pear-200 at 60%) plus a 2px ink ring. They never use green or amber.
- **Grading recolours answer objects only.** Each widget names its answer objects. Correct: #15B441 stroke, #F4FCF7 fill, check badge. Not yet: #F9D25C stroke, amber wash, cross badge. Reveal: `--hint` outline, so a reveal never reads as success. Given and derived objects never change colour on grading.
- **Labels:** KaTeX, placed directly on the object; numbers in tabular figures; units always.
- **Sizes:** canvases between 4:3 and 1:1 on mobile, at least 240px tall. Two-panel composites stack vertically below 768px and sit side by side from 1024px.
- **3D:** surfaces shaded with the sequential ramp `--seq-1` to `--seq-6`; planes translucent at 0.3 to 0.4 alpha with intersection lines drawn in ink on top.
- **Dark mode:** canvas layers read CSS variables at draw time and redraw on theme change; SVG layers use `currentColor` and variables directly.

### 2.6 Motion and show-why

Base rules (design research 4.1, 4.4, 4.5):

- **Direct manipulation is never tweened.** Dragged geometry and everything derived from it redraw on the same animation frame as the pointer.
- **Springs only on release:** snapping to a grid, a curve point or a slot uses spring-snap (300ms).
- **Stepper transitions and Play** use ease-morph over 480 to 800ms. They are demonstrations started by the learner.
- **Show-why** plays after a not-yet verdict, from a recipe:

```ts
interface ShowWhy {
  line: string;                               // verdict-chip diagnosis, at most 20 words
  steps: Array<{
    set?: Record<string, number | string>;    // non-answer variables to tween (ease-morph)
    highlight?: Id[];                         // focus wash plus ink ring, pulses twice
    annotate?: Array<{ id: Id; text: string }>;
    ms?: number;                              // 480 to 800
  }>;
}
```

- Show-why never edits answer state. Variables it tweens (zoom, $n$, the time cursor) are restored on Try again.
- Every show-why belongs to one grade. Try again, Start over, Show solution and leaving the screen cancel it, using the generation counter the prototype introduced (`showGen` in `lesson.js`).

### 2.7 Reduced motion

Triggered by `prefers-reduced-motion: reduce` or the in-app Motion setting (design 4.9):

- Snaps place instantly.
- Stepper morphs and show-why become a before-and-after pair with a Play button that steps without interpolation.
- Path reveals, histogram fills and count-ups show their final state.
- Pulsing highlights become a static ring.
- Direct manipulation is unchanged: it is the learner's own motion.

Per-widget entries list only additions.

### 2.8 Accessibility

**Keyboard map (all widgets)** [our choice]:

| Key | Action |
|---|---|
| Tab, Shift+Tab | Move between handles and controls in authored order |
| Arrow keys on a handle | Move one step along its constraint (on a curve: Left and Right move along the curve) |
| Shift+Arrow, Alt+Arrow | Ten steps; one tenth of a step |
| Home, End | Ends of the constraint |
| PageUp, PageDown | Ten steps on sliders |
| E (or double-tap) | Exact-value editor for the focused handle; accepts Exprs such as `pi/4` |
| Space | Toggle a region or cell; lift and drop a token |
| Escape | Cancel the drag in progress (handle returns to where it started); close popovers |
| Enter | Check, or Continue (engine) |
| Canvas focused (3D) | Arrows orbit $5^\circ$, Shift+Arrows $15^\circ$, + and − zoom, 0 resets the view |

**Semantics:**

- Handles are `role="slider"` with `aria-roledescription="draggable point"` and `aria-valuetext` giving every coordinate ("x 1.50, y 2.25"). Sliders wrap a native `<input type="range">`.
- Grids (`matrix`, `region-select` cells, `value-table`) use grid semantics with a roving tab stop, as the prototype dice grid does.
- Each widget's `describe('brief')` is the canvas's accessible description. Every chart has a Table toggle that opens a `value-table` with the plotted data.
- One polite live region per screen (engine). Widgets announce on commit only, throttled to one message per 600ms, in the form "Slope 2.31".
- Colour is never the only cue: graded objects carry a check or cross badge, signed regions carry + and − glyphs, early-exercise nodes carry a flag glyph.
- Tap targets are at least 44px. Only handles set `touch-action: none`, so one-finger drags on empty canvas still scroll the page on phones.
- Freehand sketching has no keyboard equivalent, so every sketch item also accepts control-point mode (section 3.11).

### 2.9 Tutor hooks (Brainy Bertie)

The tutor is Bertie on both targets: the Artifact calls the `sample` capability on the viewer's account; the web app calls the proxy. Widgets expose the same hooks to both.

- **`describe('full')`** returns at most 1,500 characters in this shape:

```text
Widget: riemann-sum "Area under x^2"
Given: f(x) = x^2 on [0, 2]; exact area 8/3 (hidden from learner)
Learner state: rule = left, n = 4; sum = 1.75; answer field "2.5" (not yet checked)
Attempts: 1 not yet (misconception: left-sum-always-over)
Elements: handle:a, handle:b, slider:n, bar:1..4, curve:f, readout:sum
```

  The "hidden from learner" line lets Bertie aim hints without revealing the answer; the engine's instruction forbids revealing it, and Show solution exists anyway after two attempts.
- **`ids()`** lists every element Bertie may point at, with a human name. Ids follow `kind:name` or `kind:index` (`handle:a`, `bar:3`, `cell:2,3`, `term:dx`) and are stable across sessions, so hints authored in content and Bertie's references use the same names.
- **Reply contract** [our choice]: Bertie answers with one JSON object, `{ "say": string, "highlight": Id[], "annotate": [{ "id": Id, "text": string }], "suggest": [{ "control": Id, "value": number, "label": string }] }`. The engine validates every id against `ids()` and drops unknown ids. One model round per hint; no tool calls needed for pointing.
- **No answer edits.** The tutor cannot call `setState`. A `suggest` entry appears as a "Try this" chip ("Try $n = 50$"); the learner taps it to apply.
- **Verified arithmetic.** On complex-tier questions the engine may give Bertie maths-core tools (`evaluate`, `differentiate`, `integrate`, `rref`, `eig`, `svd`), so numbers it quotes are computed, not recalled. Widgets need nothing extra for this.
- **`snapshot()`** renders the canvas to PNG for image-capable calls, used only when the learner asks Bertie about the picture itself.

### 2.10 Performance budgets and rendering

**Reference device** [our choice]: a 2021 mid-range Android phone (Pixel 4a or Moto G Power class) in Chrome; in CI, desktop Chrome with 4× CPU throttling as its proxy.

| Budget | Value |
|---|---|
| Widget work per pointer frame (state, derived values, redraw), P95 | 8 ms for composites, 2 ms for a primitive's own overhead |
| First render after mount | 100 ms (heavy precomputation goes to a worker or the content build) |
| Main-thread task during simulation | 4 ms; above that, the work moves to a worker |
| Memory per widget | 30 MB, including typed arrays for paths |
| Widget library download | Lazy-loaded per screen; each composite under 25 KB minified [our choice, to be measured] |

**Rendering choice:**

- SVG for anything focusable, nameable or under about 1,500 nodes.
- Canvas 2D for path bundles above 20 paths, heatmaps, scatter above 1,500 points and 3D meshes. Canvas device-pixel ratio is capped at 2 on phones.
- Heatmaps compute a coarse grid (64 by 64) into an `ImageData` and scale it with smoothing. Per-pixel evaluation is banned, as the maths-teaching skill says.
- Pointer events are coalesced to one update per animation frame. Layout is read before it is written, never interleaved.
- KaTeX renders a formula once; live numbers patch text nodes inside it (section 3.14).
- Derived data is cached by dependency: each compiled Expr knows its free variables, so dragging a point does not recompute a contour map that does not depend on it.

### 2.11 Artifact and web differences

Almost every widget is plain JavaScript with SVG and Canvas, so most entries say "no difference". The differences are:

| Concern | Artifact | Web app |
|---|---|---|
| Tutor transport | `sample` capability (viewer's account); `quick` tier for hints, `default` for explanations | Proxy holding `ANTHROPIC_API_KEY` |
| Python in `code-cell` | MicroPython with ulab if the WebAssembly probe passes [unverified]; otherwise a link to the same drill in the web app | Pyodide with NumPy, pandas, SciPy, statsmodels, scikit-learn |
| Workers | From the Artifact's own published files (allowed) or `blob:` URLs | Own files |
| Exporting data or a plot | `downloads` capability | Blob URL |
| KaTeX and MathLive styles and fonts | Must ship as the Artifact's own files, because stylesheets load only from own files or Google Fonts [inferred from the CSP facts] | Vendored |
| Saving mid-screen widget state | `db` capability (engine) | IndexedDB (engine) |

### 2.12 Generators

Practice, quizzes, homework and exams need many instances of the same item. A generator is a pure function:

```ts
interface Generator<C> {
  id: string;                                  // 'elimination-lab/integer-lu'
  difficulty: [1 | 2 | 3 | 4 | 5, 1 | 2 | 3 | 4 | 5];   // range it can produce
  make(seed: number, difficulty: number): { config: C; check: CheckSpec; solution: SolutionSteps };
}
```

Rules [our choice]:

- Deterministic: the same seed gives the same item on every device.
- Nice numbers by construction, not by rejection loops where avoidable. For example, integer $LU$ factors are chosen first and multiplied.
- Every generator ships with a property test over 1,000 seeds: the stored answer equals an independent solver's answer, the answer is unique where the item says so, and every number sits inside the stated bounds.
- A set never repeats an instance; the engine passes consecutive seeds.
- Each generator states the misconceptions its distractors encode.

Section 9 lists which widgets need generators.

### 2.13 What these widgets need from the maths core

These are requirements on the engine's shared modules. The engine blueprint owns their design; this list is the acceptance test from the widget side.

| Module | Must provide | Used by |
|---|---|---|
| `expr` | Parse the grammar in 2.3; compile to closures with no `eval` or `Function`; symbolic $\frac{d}{dx}$ with light simplification; Taylor coefficients to order 12 by truncated power-series arithmetic; LaTeX output; free-variable lists for caching | every calculus widget |
| `sample` | Adaptive curve sampling (at most 400 points per curve) that breaks at `NaN` and jumps; marching squares for implicit curves and contours on a 96 by 96 grid | `marks` |
| `quad` | Adaptive Simpson and Gauss-Kronrod (7, 15); cumulative integral on a 512-point grid | `accumulator`, `riemann-sum`, `volume-slicer` |
| `ode` | RK4 fixed step; Dormand-Prince adaptive | `slope-field`, `linear-dynamics` |
| `roots` | Brent's method; safeguarded Newton; projection of a point onto an implicit curve | `drag-point`, `root-finder`, `lagrange-explorer` |
| `rational` | BigInt fractions; exact RREF, $PA=LU$, determinant, inverse, rank, nullspace basis for matrices up to 6 by 7 | `elimination-lab`, `solution-set`, `four-subspaces`, `determinant-lab` |
| `linalg` | Closed-form eigen and SVD for 2 by 2; 3 by 3 eigen; Jacobi symmetric eigensolver and one-sided Jacobi SVD up to 64 by 64 and 500 by 10; Householder QR; Cholesky; least squares by QR | linear algebra widgets |
| `rng` | Counter-based uniforms addressable by (seed, stream, index); normals by Box-Muller; Brownian paths by midpoint bridge refinement to $2^{14}$ steps; Poisson | `sim-runner` and every stochastic widget |
| `stats` | $\Phi$, $\varphi$, $\Phi^{-1}$, quantiles, histogram binning | stochastic widgets, `taylor-builder` (option preset) |

### 2.14 Testing per widget

Each widget ships with four kinds of test [our choice]:

1. Unit tests for its pure parts: state derivation, check functions, show-why selection.
2. Property tests for each generator (2.12).
3. An accessibility test (axe) on a fixture page, plus a scripted keyboard-only run that completes the widget's canonical item.
4. A performance fixture: a scripted drag under 4× CPU throttling in Playwright, failing the build when the P95 frame exceeds the budget in 2.10.

### 2.15 Example screen as data

A Problem screen from 1.3.4 L1, showing how content names a widget, its check and its show-why:

```json
{
  "id": "1.3.4.L1.s4",
  "type": "problem",
  "prose": "The rectangles use the left edge of each strip. Will their total be too big or too small?",
  "widgets": [{
    "type": "riemann-sum", "id": "rs", "label": "Area under x squared",
    "f": "x^2", "a": 0, "b": 2, "movableEnds": false,
    "n": 4, "rules": ["left"], "showExact": "after-check"
  }],
  "answer": { "type": "choice", "id": "dir", "options": [
    { "id": "under", "tex": "Too small" },
    { "id": "over", "tex": "Too big" },
    { "id": "exact", "tex": "Exactly right" } ] },
  "check": { "kind": "choice", "correct": "under",
    "misconceptions": { "over": "left-sum-always-over", "exact": "rectangles-are-exact" } },
  "showWhy": {
    "left-sum-always-over": {
      "line": "Each bar takes its height from the left edge, where x squared is smallest.",
      "steps": [ { "highlight": ["gap:1", "gap:2", "gap:3", "gap:4"], "ms": 600 } ] }
  }
}
```

---
## 3. Primitives

Build waves used below: **A** Stage 0, 1.1 and 1.2; **B** single-variable calculus (1.3.1 to 1.3.5); **C** multivariable calculus and linear algebra (1.3.6 to 1.4.7); **D** probability (1.5). Section 11 has the full ordering.

### 3.1 `plot-2d`: Plot axes

Primitive (host). P0, wave A. First needed in 0.2 (graphs).

- **Purpose.** A coordinate plane that hosts marks and handles. It owns the world-to-screen transform, axes, grid, ticks, clipping, zoom, linking between sibling plots, coordinate systems and the table view.
- **Serves.** Every 1.3 and 1.4 composite except `matrix-multiply`, `four-subspaces` and `dependency-graph`; every 3.2 composite.
- **Interactions.** Pointer: no pan by default, so one-finger drags on empty space scroll the page. When `zoom` is on: pinch, Ctrl or Cmd with the wheel, and on-canvas +, − and reset buttons. Double-tap on empty space resets the view. Keyboard: the canvas takes focus only when zoom or pan is on; then arrows pan, + and − zoom, 0 resets.
- **State.** `{ view: { x: [number, number]; y: [number, number] } }`. No answer state.
- **Checks.** None of its own.
- **Config.**

```ts
interface Plot2DConfig extends BaseConfig {
  view: { x: [number, number]; y: [number, number] };
  aspect?: 'equal' | 'free' | number;          // 'equal' for geometry and linear algebra
  coords?: 'cartesian' | 'polar' | 'ternary';  // polar grid; ternary for weights summing to 1
  axes?: { x?: AxisSpec; y?: AxisSpec } | false;
  grid?: 'none' | 'major' | 'minor' | 'integer';
  zoom?: { min: number; max: number; pinch: boolean; buttons: boolean } | false;
  pan?: boolean;
  link?: { group: string; axis: 'x' | 'y' | 'both' };   // shared view with sibling plots
  layers: Array<MarkSpec | HandleSpec>;                 // drawn in order
  table?: 'auto' | TableSpec | false;
}
interface AxisSpec {
  label?: string;                                   // LaTeX
  ticks?: 'auto' | number[] | { step: number };
  scale?: 'linear' | 'log';
  format?: 'decimal' | 'pi' | 'percent' | 'fraction' | 'integer';
  position?: 'zero' | 'edge';
}
```

- **Visual.** `bg-surface`; gridlines 1px `--grid`; axes 1.5px `--axis` with no arrowheads; tick labels in caption type (13/18, tabular); axis labels in KaTeX at the positive ends. Ternary mode draws the triangle with its three edges labelled by weight.
- **Motion.** Zoom buttons animate the view over 200ms (ease-standard); pinch is direct. Linked plots update on the same frame.
- **Reduced motion.** Zoom buttons jump.
- **Accessibility.** `role="group"` named by `label`. With no handles, the SVG is `role="img"` with `describe('brief')` as its description. The Table toggle lists the data of every mark marked `table: true`. Tick text is hidden from assistive technology; the axis ranges are in the description.
- **Tutor hooks.** Describes ranges and lists its marks. Ids: `axis:x`, `axis:y`, `grid`, plus the ids of its marks and handles.
- **Performance.** Host overhead under 1 ms per frame. Transforms cached; resizing through `ResizeObserver`. A layer marked `heavy` renders on a canvas beneath the SVG overlay.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.2 `plot-3d`: Lightweight 3D scene

Primitive (host). P0, wave C. First needed in 1.3.6; possibly 0.3 if the precalculus cluster uses 3D vectors.

- **Purpose.** Show surfaces, planes, vectors, points, curves, columns and solids in 3D with an orbit camera, linked to 2D views.
- **Serves.** 1.3.4 L10; 1.3.6; 1.3.7; 1.3.8 L4; 1.4.1 L2; 1.4.2 L1; 1.4.3 L4 and L5; 1.4.4 L3 and L5; 1.4.5 L1; 1.4.7 L1, L2 and L4; 3.2.4 L3.
- **Interactions.** Pointer: drag on empty space orbits (azimuth free, elevation clamped to $\pm85^\circ$); pinch zooms; view buttons for top, front, side and isometric. 3D handles move in a constraint plane (default: horizontal through the point), with a side slider for height, because a 2D pointer cannot pick depth. Keyboard: the canvas orbits as in 2.8; handles open a three-field exact editor on E.
- **State.** `{ camera: { azimuth: number; elevation: number; zoom: number } }`.
- **Checks.** None of its own.
- **Config.**

```ts
interface Plot3DConfig extends BaseConfig {
  box: { x: [number, number]; y: [number, number]; z: [number, number] };
  camera?: { azimuth: number; elevation: number; zoom?: number;
             projection?: 'orthographic' | 'perspective' };
  axes?: boolean | { labels: [string, string, string] };
  floor?: 'grid' | 'contours' | 'none';
  orbit?: boolean;
  presets?: Array<'top' | 'front' | 'side' | 'iso'>;
  layers: Array<Mark3DSpec | Handle3DSpec>;
  mesh?: { phone: number; desktop: number };   // cells per side; default 32 and 64
  link?: { group: string };                    // share a point or slice with a plot-2d
}
// Mark3DSpec types: surface (z = f(x, y) or parametric), plane (normal and offset, or span),
// vector, point, curve3d, polyline, polygon, parallelepiped (three edge vectors), columns, slicePlane.
```

- **Visual.** Surfaces flat-shaded with the sequential ramp by height, 0.5px ink mesh lines. Planes translucent in series colours with ink intersection lines. Axes in `--axis`, labelled in KaTeX. Handles in `--manip`. Far edges drawn lighter as a depth cue.
- **Motion.** Orbit is direct. Preset views move over 280ms (ease-standard). Nothing rotates on its own.
- **Reduced motion.** Presets jump.
- **Accessibility.** A 3D view cannot carry meaning alone: every scene has a 2D companion (contour map, slice panel or coordinates table) and a description that states the geometry ("Two planes meet in a line through (1, 0, 2) with direction (1, 1, 0)").
- **Tutor hooks.** Describes the camera and objects. Ids: `surface:<id>`, `plane:<id>`, `vec:<id>`, `point:<id>`, `slice:<axis>`, `column:<i>,<j>`.
- **Performance.** Canvas 2D for meshes and planes, with painter's sorting by quad centroid depth: at most 1,024 quads on phones, 4,096 on desktop. SVG overlay for handles, vectors and labels (under 50 nodes, reprojected each frame). Budget 8 ms per orbit frame; if two frames in a row exceed it, the mesh draws as wireframe until the pointer is released. Intersecting planes cannot be sorted correctly by painter's algorithm, so planes stay translucent and their intersection lines are computed analytically and drawn on top.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.3 `number-line`: Number line

Primitive (host). P0, wave A. First needed in 0.1 (negatives); cross-cluster.

- **Purpose.** A 1D axis for points, intervals, sign tables, mapping diagrams and convergence intervals.
- **Serves.** 1.3.1 L1; 1.3.3 L1 and L2; 1.3.5 L4; `function-mapping`, `sign-chart`, `series-explorer`.
- **Interactions.** Pointer: tap to place a point (when `placeable`), drag points, tap an interval end to toggle open or closed. Keyboard: arrows move the focused point by `step`; O toggles open or closed; Delete removes a placed point.
- **State.** `{ points: Array<{ id: Id; x: number }>; intervals: Array<{ id: Id; a: number; b: number; openA: boolean; openB: boolean }> }`.
- **Checks.** `point` (metric `x`), `interval`, `ordering` (of points).
- **Config.**

```ts
interface NumberLineConfig extends BaseConfig {
  range: [number, number];
  ticks?: AxisSpec['ticks']; scale?: 'linear' | 'log'; format?: AxisSpec['format'];
  orientation?: 'horizontal' | 'vertical';
  points?: Array<{ id: Id; x: number; movable?: boolean; label?: string }>;
  intervals?: Array<{ id: Id; a: number; b: number; openA: boolean; openB: boolean; editable?: boolean }>;
  placeable?: { max: number; snap?: number };
}
```

- **Visual.** 1.5px `--axis` line with ticks. Fixed points are 6px ink dots; learner points are `--manip` handles. Intervals are 6px bands, `--manip` when learner-set and s2 when given; open ends hollow, closed ends filled.
- **Motion.** Snap on release (spring-snap).
- **Reduced motion.** Base.
- **Accessibility.** Points are sliders; each interval end is a slider with an adjacent toggle button (`aria-pressed` for closed).
- **Tutor hooks.** Ids: `point:<id>`, `interval:<id>`, `end:<id>:a`, `end:<id>:b`.
- **Performance.** Trivial SVG.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.4 `matrix`: Matrix view and editor

Primitive (host). P0, wave C. First needed in 1.4.1; column vectors may appear in 0.3.

- **Purpose.** Show and edit matrices and vectors with exact entries; select rows, columns and cells; carry the row-operation gestures; mark pivots; draw augmented bars and partitions; colour entries in heatmap mode.
- **Serves.** All of 1.4; 1.3.6 L7 (Hessian); 1.3.7 L5 (Jacobian); 3.2.2 L5 (covariance); linked panels in most linear algebra composites.
- **Interactions.** Pointer: tap a cell to edit (numeric keypad with a fraction key, or a small MathLive field when symbols are allowed); tap a row's gutter handle to select the row; drag a row handle onto another row to swap them. Keyboard: arrows move between cells (roving tab stop); Enter or F2 edits; Escape cancels the edit; Space selects the focused row in row mode; Alt+Up and Alt+Down move the selected row (swap).
- **State.** `{ entries: Entry[][]; selected: { rows: number[]; cols: number[]; cells: Array<[number, number]> } }`.
- **Checks.** `matrix` (all relations), `numeric` per cell through `multi` (per-cell marks), `set` (pivot positions as selected cells).
- **Config.**

```ts
interface MatrixConfig extends BaseConfig {
  rows: number; cols: number;
  entries: Entry[][];
  editable?: boolean | Array<[number, number]>;
  augmentAfterCol?: number;                     // draws the bar of [A | b] or [A | I]
  partition?: { rows?: number[]; cols?: number[] };
  number?: 'exact' | 'decimal'; decimals?: number;
  select?: 'none' | 'cell' | 'row' | 'col' | 'multi';
  rowGestures?: boolean;                        // drag-to-swap, used by elimination-lab
  heat?: { ramp: 'sequential' | 'diverging'; range?: [number, number] };
  labels?: { name?: string; rows?: string[]; cols?: string[] };   // LaTeX
  bracket?: 'square' | 'round' | 'bar';         // 'bar' for determinants
}
```

- **Visual.** Brackets drawn in SVG (not KaTeX, so cells stay interactive). Entries in KaTeX for fractions and symbols, tabular figures otherwise. Editable cells carry a `--manip` dashed underline; a selected row takes a `--manip-wash` band; pivots get a 2px ink circle. Heatmap cells take the ramp colour with ink or white text chosen by contrast. Grading badges sit at each cell's top right. Answer objects: the editable cells.
- **Motion.** Row swaps slide over 200ms (spring-snap) after the drop; entries changed by an operation cross-fade over 150ms with a brief focus wash, so the learner sees what changed.
- **Reduced motion.** No slide; the wash still marks changed entries.
- **Accessibility.** `role="grid"` with row and column counts; each cell named "row 2, column 3, five halves". Row operations are announced with the resulting row ("Row 2 minus 3 times row 1. Row 2 is now 0, 2, minus 1").
- **Tutor hooks.** Describes the matrix as a LaTeX `bmatrix` string plus the selection. Ids: `cell:<i>,<j>`, `row:<i>`, `col:<j>`, `pivot:<k>`.
- **Performance.** DOM grid up to 8 by 8 editable; heatmap mode up to 64 by 64 on a canvas.
- **Artifact and web.** No difference.
- **Generators.** None of its own.

### 3.5 `marks`: Passive drawing layers

Primitive (mark family). P0, wave A.

- **Purpose.** Declarative layers inside a host, each with a stable id, whose coordinates may be Exprs over widget variables. Marks never animate by themselves; they redraw from variables.
- **Mark types.**

| Type | Draws | Notes |
|---|---|---|
| `curve` | $y=f(x)$ | Adaptive sampling; breaks at `NaN` and jumps; `holes` drawn as hollow circles; open or closed ends |
| `param-curve` | $(x(t), y(t))$ | Also used for implicit circles in parametric form |
| `polar-curve` | $r(\theta)$ | |
| `implicit` | $F(x,y)=c$ | Marching squares, 96 by 96 |
| `contours` | Level sets of $f(x,y)$ | Levels by list or count; inline labels; optional filled bands |
| `heatmap` | Colour field of $f(x,y)$ | 64 by 64 canvas, sequential or diverging ramp |
| `field` | Slope or vector field | One SVG path for all segments; optional normalised length |
| `point`, `segment`, `line`, `ray` | Basic geometry | `line` through two points or point and slope |
| `vector` | Arrow from tail to head | 8px head; label at the tip |
| `polygon`, `region` | Filled shapes | `region` fills under $f$ or between $f$ and $g$ on $[a,b]$, with signed colouring |
| `bars` | Rectangles from arrays | Riemann sums, histograms, singular values |
| `scatter` | Points from arrays | Tap or hover to inspect |
| `paths` | Bundle of polylines | Canvas when heavy; one path can be emphasised |
| `band` | Horizontal or vertical strip | $\varepsilon$ bands, confidence bands |
| `angle` | Arc or right-angle marker | |
| `ellipse` | Image of the unit circle under a $2\times2$ matrix, or a covariance ellipse | |
| `tangent` | Tangent line to a curve at $x$ | Slope from the symbolic derivative |
| `brace` | Dimension brace with a label | $\Delta x$, $\Delta y$, $dx$ |
| `label` | KaTeX label at a world point | Picks one of 8 positions to avoid overlap |
| `ghost` | Any of the above as a dashed target | 1.5px ink, 6 on and 4 off |

- **Serves.** Every composite.
- **Interactions.** None, except tap, hover or keyboard focus on `scatter`, `bars` and `paths` items, which shows an inspection chip and emits a `select` event a composite may use (choosing a path to reflect, a singular-value layer to show). Selectable items join the tab order only when a composite subscribes to `select`.
- **State.** None; derived from variables.
- **Checks.** None directly. A mark can be an answer object that a composite recolours.
- **Config.** `type MarkSpec = { id: Id; type: MarkType; style?: Style; table?: boolean; visibleWhen?: Expr } & TypeFields;` with `Style = { stroke?: 'ink' | 's1' | 's2' | 's3' | 's4' | 's5' | 's6' | 'manip' | 'muted'; width?: 1 | 1.5 | 2 | 2.5 | 3; dash?: boolean; fill?: Style['stroke']; opacity?: number }`. Example: `{ "id": "curve:f", "type": "curve", "expr": "x^2*sin(1/x)", "domain": [-1, 1] }`.
- **Visual.** Section 2.5 roles.
- **Motion.** None of their own; `explain` transitions tween the variables marks depend on.
- **Reduced motion.** Not applicable.
- **Accessibility.** Each mark contributes a phrase to `describe()` and, when `table: true`, rows to the table view.
- **Tutor hooks.** The declared ids.
- **Performance.** At most 400 sample points per curve; recompute only when a free variable of the mark's Exprs changes.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.6 `drag-point`: Draggable point

Primitive (handle). P0, wave A.

- **Purpose.** The universal handle: a point the learner moves under a constraint, with snapping. Also the head of a draggable vector, the end of an interval, and an angle handle on a circle.
- **Serves.** Nearly every composite.
- **Interactions.** Pointer: press within 22px (a 44px target), drag with pointer capture; the point follows on every frame; on release it snaps (spring-snap) to the grid, a snap target or the nearest allowed point; Escape during a drag returns it to its start. Keyboard: base map; on a curve, Left and Right move along the curve's parameter; E opens the exact editor.
- **Constraints.** `free`, `grid`, `axis` (x or y locked), `on-curve` (curve id; the handle tracks $x$ and sits on the curve), `on-implicit` (projects to the nearest point of $F=c$ by Newton steps), `on-segment`, `on-circle` (centre, radius: angle handles), `in-region` (clamped to a polygon or box), `custom` (a named projection in the registry).
- **State.** `{ at: number[]; t?: number; dragging: boolean }`.
- **Checks.** `point` (all metrics), `predicate`, and `numeric` on a value derived from the point.
- **Config.**

```ts
interface DragPointConfig {
  id: Id;
  at: number[] | { t: number };
  constraint?:
    | { kind: 'free' } | { kind: 'grid'; step: number }
    | { kind: 'axis'; axis: 'x' | 'y'; value: number }
    | { kind: 'on-curve'; curve: Id } | { kind: 'on-implicit'; expr: Expr; level: number | string }
    | { kind: 'on-segment'; from: number[]; to: number[] }
    | { kind: 'on-circle'; centre: number[] | Id; radius: number }
    | { kind: 'in-region'; polygon: number[][] } | { kind: 'custom'; name: string };
  snap?: { grid?: number; to?: number[][]; radius?: number };
  bind?: { x?: string; y?: string; z?: string; t?: string; angle?: string };   // writes widget vars
  shape?: 'dot' | 'arrowhead' | 'bar-end' | 'ring';
  tail?: number[] | Id;                       // vector mode: arrow drawn from the tail
  readout?: 'none' | 'coords' | 'x' | 'y' | Expr;
  label?: string;                             // LaTeX
}
```

- **Visual.** A 20px `--manip` disc with a 2px white ring and 1px ink outline (design 2.6); arrowhead variant for vectors. While dragging, a caption chip above the point shows the readout. Focus ring 2px `--focus` with 2px offset. Answer object when the point is the answer.
- **Motion.** Never tweened while dragged; spring-snap on release.
- **Reduced motion.** Snap is instant.
- **Accessibility.** Slider semantics with every coordinate in `aria-valuetext`; announced on release.
- **Tutor hooks.** Ids: `handle:<id>`. Describes position and constraint ("P at x = 1.50 on curve f").
- **Performance.** Distance-based hit testing, no per-pixel DOM; under 0.5 ms per frame.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.7 `slider`: Parameter slider

Primitive (control). P0, wave A.

- **Purpose.** Set a scalar: continuous, stepped, logarithmic, integer, or from a discrete list.
- **Serves.** Most composites.
- **Interactions.** Pointer: drag the thumb or tap the track. Keyboard: base map; E opens an exact field. Optional Play for time-like parameters, which advances the value linearly.
- **State.** `{ value: number; playing?: boolean }`.
- **Checks.** `numeric` (the value itself is the answer), `predicate`.
- **Config.**

```ts
interface SliderConfig {
  id: Id; bind: string;
  min: number; max: number; step?: number;
  scale?: 'linear' | 'log';
  values?: number[];                // discrete list, e.g. [1, 2, 4, 8, 16, ..., 1024]
  label: string;                    // LaTeX, e.g. 'n'
  format?: 'decimal' | 'integer' | 'pi' | 'percent'; decimals?: number; units?: string;
  ticks?: number[];
  play?: { perSecond: number; loop?: boolean };
  orientation?: 'horizontal' | 'vertical';
}
```

- **Visual.** Design 5.3 item 5: 4px track in `--line`, filled part `--manip`, 24px `--manip` thumb, 44px hit area; label to the left in KaTeX ($n = 16$); value above the thumb while dragging. Answer object when the value is the answer.
- **Motion.** Direct; Play is linear.
- **Reduced motion.** Play steps without interpolation, four steps per second.
- **Accessibility.** Native `<input type="range">` underneath with `aria-valuetext` including units.
- **Tutor hooks.** Ids: `slider:<id>`. Bertie's "Try this" chips target sliders most often.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.8 `stepper`: Diagram stepper

Primitive (control). P0, wave A.

- **Purpose.** Walk through a fixed sequence of states: Demonstrate screens, algorithm traces (Newton iterations, elimination history, Gram-Schmidt, SVD stages, backward induction).
- **Serves.** `root-finder`, `elimination-lab`, `gram-schmidt`, `svd-stepper`, `determinant-lab`, `binomial-tree`, `dependency-graph`, `linear-dynamics`, `filtration-tree`, `derivation-steps`.
- **Interactions.** Previous, next and play buttons; tap a dot to jump. Keyboard: Left and Right when the stepper is focused; Space plays and pauses. **Predict mode:** Next stays locked until the learner answers a small prediction (a drag or a choice). This keeps "act before you read" inside demonstrations [our choice].
- **State.** `{ index: number; playing: boolean; predictions: Record<number, unknown> }`.
- **Checks.** None of its own; predict mode embeds a sub-check per step.
- **Config.** `{ id: Id; steps: Array<{ state: Record<string, unknown>; caption?: string; highlight?: Id[]; predict?: { prompt: string; check: CheckSpec } }>; autoplayMs?: number; loop?: boolean }`. Captions are at most 20 words.
- **Visual.** Dots as in quiz progress (8px, `--line`, current in ink), small secondary pill buttons, caption below the canvas.
- **Motion.** Step transitions tween state over 480 to 800ms (ease-morph).
- **Reduced motion.** Cross-fade of 120ms.
- **Accessibility.** Buttons named "Step 2 of 5"; the caption is announced on each step.
- **Tutor hooks.** Ids: `step:<i>`. Describes the current step and its caption.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.9 `region-select`: Region selector

Primitive (handle). P0, wave A. The prototype's dice grid is an instance.

- **Purpose.** Choose regions: cells of a grid, parts of a diagram, intervals of a sign table, atoms of a partition; or bracket an interval $[a,b]$ on an axis with two handles.
- **Serves.** `sign-chart`, `filtration-tree`, `binomial-tree` (early-exercise nodes), `region-bounds` (strip), `elimination-lab` (pivot marking).
- **Interactions.** Pointer: tap toggles a region or cycles its states (for example blank, +, −); drag across cells paints them with the first cell's new state. Keyboard: arrows move between regions in spatial order; Space toggles or cycles. Bracket mode uses two `drag-point`s on the axis.
- **State.** `{ selected: Record<Id, string> }`.
- **Checks.** `set` (with optional partial marks), `interval` (bracket mode).
- **Config.** `{ id: Id; regions: Array<{ id: Id; shape: number[][] | { cell: [number, number] } | { interval: [number, number] } | { mark: Id }; label?: string }>; states?: string[]; maxSelected?: number; bracket?: { axis: 'x' | 'y'; range: [number, number] }; showCount?: boolean }`.
- **Visual.** Unselected regions transparent with a 1px `--line` edge; selected regions `--manip-wash` with a 2px `--manip` edge; sign states show an ink glyph. Answer objects: the selected regions.
- **Motion.** None beyond grading.
- **Reduced motion.** Base.
- **Accessibility.** Each region is a toggle button with `aria-pressed` (or a named state for cycles); the running count is announced.
- **Tutor hooks.** Ids: `region:<id>`.
- **Performance.** Trivial up to 200 regions.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.10 `token-tray`: Token tray

Primitive (control). P0, wave A.

- **Purpose.** Drag tokens (terms, labels, steps, vectors, values) into slots: ordering, fill the blank, matching, building an expression, filling a table, sorting into bins.
- **Serves.** `growth-rectangle` (labelling strips), `dependency-graph`, `four-subspaces`, `derivation-steps`, `matrix-multiply` (shape matching), growth-rate ordering (1.3.1 L3), `pca-lab` (naming loadings), the $dW\cdot dW$ table (3.2.3 L3).
- **Interactions.** Pointer: drag, or tap a token then tap a slot (the two-tap path suits touch and motor impairments). Keyboard: Space lifts, arrows move between slots, Space drops, Escape cancels. A token dropped outside any slot returns to the tray.
- **State.** `{ placement: Record<SlotId, TokenId | null> }`.
- **Checks.** `ordering`, `set` (bin membership), `expression` (the assembled expression).
- **Config.** `{ id: Id; tokens: Array<{ id: Id; content: string; copies?: number }>; slots: Array<{ id: Id; accepts?: Id[]; label?: string; group?: string }>; layout: 'sequence' | 'bins' | 'grid' | 'inline'; reuse?: boolean }`.
- **Visual.** Lip-token chips (2px border plus a 4px bottom edge); a lifted token scales to 1.03 with the e2 shadow and drops its lip; slots have a dashed `--line-control` outline. Answer objects: the placed tokens.
- **Motion.** Siblings slide aside over 200ms; drops snap (spring-snap). Design 5.3 item 7.
- **Reduced motion.** Instant placement.
- **Accessibility.** Announces each move ("Moved dW times dW to row 2, column 2").
- **Tutor hooks.** Ids: `token:<id>`, `slot:<id>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.11 `sketch-pad`: Curve sketcher

Primitive (handle). P0, wave A. First needed in 0.2 (sketching graphs), if the algebra cluster uses it.

- **Purpose.** The learner draws a curve on a `plot-2d`, freehand or by moving control points; graded against a target by values and by features.
- **Serves.** `derivative-tracer` (sketch $f'$ or $f$), 1.3.3 L3 (curve sketching), `accumulator` (sketch $A$), `slope-field` (sketch a solution), `heat-diffusion` (predict the price curve).
- **Interactions.** Freehand: draw with a finger or mouse; the stroke is resampled as a function of $x$, and a later stroke overwrites the $x$-range it covers; an eraser clears ranges. Points mode: $k$ knots joined by a monotone cubic spline (Fritsch-Carlson, so the curve never overshoots its knots); tap the curve to add a knot, long-press a knot to remove it. Keyboard: points mode only (Tab between knots, arrows move, Insert adds a knot after the focused one, Delete removes). Every sketch item offers points mode, so no item depends on freehand drawing.
- **State.** `{ samples: Array<number | null>; knots: Vec2[]; mode: 'freehand' | 'points' }` with samples on a 101-point grid over the domain.
- **Checks.** `curve`: inside the band over `coverage` of the domain, plus every listed feature (zeros, signs, extrema, concavity, monotone pieces, asymptotes). Each feature gets its own verdict, so the show-why can point at the failing part.
- **Config.** `{ id: Id; plot: Id; domain: [number, number]; mode: 'freehand' | 'points' | 'either'; knots?: number; anchor?: Vec2 }` with the check in `CheckSpec` (`kind: 'curve'`).
- **Visual.** The learner's stroke is 3px `--manip`. After grading, the target appears as a ghost and failing features get an amber marker with a cross; the stroke is the answer object.
- **Motion.** Show-why draws the target on (stroke dash offset) over 600ms, then pulses the failing interval.
- **Reduced motion.** The target appears at once.
- **Accessibility.** Points mode; `describe()` turns the sketch into words ("decreasing from x = −2 to 0, increasing after; crosses zero near x = 1.1").
- **Tutor hooks.** Ids: `stroke`, `knot:<i>`, `feature:<i>`.
- **Performance.** Raw pointer samples while drawing; resampling on pointer up only.
- **Artifact and web.** No difference.
- **Generators.** None of its own.

### 3.12 `sim-runner`: Seeded simulation driver

Primitive (runner). P0, wave A if Stage 0 probability uses it, otherwise wave D; cross-cluster with probability.

- **Purpose.** Reproducible random simulation: run batches, play, pause and step; stream results into marks; offload heavy work to a worker.
- **Serves.** `path-simulator` and every 3.2 composite; `least-squares-fit` and `pca-lab` (seeded data); `condition-number`.
- **Interactions.** Buttons Run 1, 10, 100, 1,000 (and 10,000 where allowed), Reset, play and pause, a speed slider. Keyboard: native buttons.
- **State.** `{ seed: number; runs: number; summary: Record<string, number>; playing: boolean }`.
- **Checks.** None of its own. Simulation screens grade a prediction made before running (the prototype's "predict first" rule), never the simulated estimate.
- **Config.** `{ id: Id; seed: number; model: 'walk' | 'scaled-walk' | 'brownian' | 'brownian-2d' | 'gbm' | 'sde' | 'poisson' | 'gaussian-cloud' | string; params: Record<string, number | string>; batches: number[]; maxSamples: number; worker?: 'auto' | 'never'; feeds: Id[] }`.
- **Randomness.** Counter-based: every draw is a hash of (seed, stream, index), so path 37 is the same whether 50 or 500 paths exist. Brownian paths are built by midpoint bridge refinement on dyadic grids up to $2^{14}$ steps, so a finer partition keeps every coarser point.
- **Visual.** Secondary pill buttons; tabular run counter; histograms fill as data arrives.
- **Motion.** Data-driven filling is content, not decoration.
- **Reduced motion.** Each batch shows its final state at once.
- **Accessibility.** After each batch: "1,000 runs. Mean 0.02. 68% within one standard deviation."
- **Tutor hooks.** Ids: `run:<n>`, `reset`. Describes runs and summary statistics.
- **Performance.** In-thread while a frame's share stays under 4 ms; otherwise a worker posts `Float32Array`s as transferables. At most 200 paths are drawn; the rest only feed summaries.
- **Artifact and web.** Worker from an own published file on both targets.
- **Generators.** Supplies seeds to generators of other widgets.

### 3.13 `value-table`: Live table of values

Primitive (control). P0, wave A.

- **Purpose.** A live table: $x$ and $f(x)$ approaching a limit, partial sums, iterates, data points, residuals. Editable cells for data entry. It is also the table view of every chart.
- **Serves.** `limit-explorer`, `secant-tangent`, `root-finder`, `riemann-sum`, `series-explorer`, `least-squares-fit`, `linear-dynamics`, `binomial-tree` (accessible view), every chart's Table toggle.
- **Interactions.** Hovering or focusing a row highlights its linked mark and the reverse; editable numeric cells; optional add and remove rows; optional sort. Keyboard: grid navigation.
- **State.** `{ rows: Array<Record<string, number>>; focusRow?: number }`.
- **Checks.** `numeric` per cell through `multi`.
- **Config.** `{ id: Id; columns: Array<{ key: string; label: string; expr?: Expr; decimals?: number; editable?: boolean }>; rows: Array<Record<string, number>> | { from: Id }; maxRows?: number; linkMarks?: boolean }`.
- **Visual.** Tabular figures; caption-weight headers in KaTeX; the row linked to the dragged handle tinted `--manip-wash`.
- **Motion.** None.
- **Reduced motion.** Not applicable.
- **Accessibility.** A native `<table>` with a caption and scoped headers. It is the accessible fallback for charts, so it must be complete.
- **Tutor hooks.** Ids: `row:<i>`, `cell:<i>,<key>`.
- **Performance.** Virtualised beyond 200 rows.
- **Artifact and web.** No difference.
- **Generators.** None.

### 3.14 `live-formula`: Live typeset formula

Primitive (display). P0, wave A.

- **Purpose.** A KaTeX formula whose numbers update from widget variables, with terms linked to marks: focus a term and its mark lights up, and the reverse. It also renders Generalise-screen formula cards.
- **Serves.** Nearly every composite.
- **Interactions.** Hover or focus a linked term to highlight its mark (focus wash); tap a term to toggle its mark when `toggles` is set. Keyboard: Tab through linked terms.
- **State.** None; derived.
- **Checks.** None.
- **Config.** `{ id: Id; tex: string; slots: Record<string, { expr: Expr; decimals?: number; format?: 'decimal' | 'fraction' | 'percent' }>; links?: Record<Id, Id>; toggles?: boolean }`, where `tex` contains `\htmlId{slot-name}{0}` placeholders, for example `\frac{f(x+h)-f(x)}{h} = \htmlId{slope}{0}`.
- **Visual.** Display maths at 1.15em. Numbers that depend on something the learner is moving render in `--manip`; other numbers in ink. This shows cause and effect [our choice].
- **Motion.** Numbers change immediately, never count up during a drag.
- **Reduced motion.** Not applicable.
- **Accessibility.** KaTeX outputs MathML alongside HTML; the engine announces key values on commit.
- **Tutor hooks.** Ids: `term:<id>`. Describes the formula in LaTeX with current numbers.
- **Performance.** KaTeX renders the skeleton once (with `trust` limited to `\htmlId`); slots are patched through `textContent`. Under 0.5 ms per frame.
- **Artifact and web.** KaTeX styles and fonts as own files in the Artifact (2.11).
- **Generators.** None.

### 3.15 `choice`: Option cards

Primitive (control, engine-level). P0, wave A. Specified by the engine (design 5.3 items 1 and 2); this cluster needs one addition.

- **Addition needed here.** An option's content may be a small read-only `plot-2d` thumbnail, for "which graph is $f'$?" and "which field matches $y'=y(1-y)$?". Thumbnails render at 120 by 90 with no axis labels and a KaTeX caption below.
- **Checks.** `choice`, with one misconception per distractor.
- **Tutor hooks.** Ids: `option:<id>`.
- **Everything else.** Base and engine.

### 3.16 `numeric-input`: Numeric entry

Primitive (control, engine-level). P0, wave A. Specified by the engine (design 5.3 item 3); this cluster needs three additions.

- **Special keys** for limits and convergence: DNE, $\infty$, $-\infty$, enabled per item through `specials`.
- **Exact entry:** fractions, $\pi$, $e$ and square roots parsed by `expr`, so $\frac{8}{3}$ and 2.6667 are both accepted within tolerance.
- **Vector entry** is not done here: vectors and matrices use the `matrix` primitive with editable cells.
- **Tutor hooks.** Ids: `field:<id>`.

### 3.17 `expression-input`: Expression entry

Primitive (control, engine-level). P0, wave A. Specified by the engine (design 5.3 item 4: MathLive and Compute Engine); this cluster needs:

- `mode: 'antiderivative'` and `'equal-up-to-constant'` (2.4).
- Variables beyond $x$: $t$, $\theta$, $\lambda$, $\varepsilon$, $\delta$, $\sigma$, $\mu$, $W_t$ and subscripted names, typed from the Greek layer of the maths keyboard.
- `form` checks for factored and single-fraction answers (partial fractions).
- Numeric cross-checking with our `expr` at seeded sample points, avoiding singular points listed in the item's `domain`.
- Compute Engine is used to parse, simplify and test equality only, never its `compile()`, which builds JavaScript functions from strings and could meet the Artifact's script policy [inferred].
- **Tutor hooks.** Ids: `field:<id>`.

### 3.18 `code-cell`: Python cell with tests

Primitive (control). P0, wave A (1.1). Owned by the programming cluster; this cluster needs:

- NumPy linear algebra in tests (least squares and PCA "from the matrix operations", the 1.4 exit test).
- Comparison helpers: `allclose`, `allclose_up_to_sign` (eigenvectors and principal components have arbitrary sign) and a subspace comparison for bases.
- A fixed seed for generated data, shared with the matching widget, so the learner can check their code against the picture they explored.
- **Artifact.** MicroPython with ulab covers pure-Python drills and simple arrays if the WebAssembly probe passes [unverified]. ulab's `linalg` is understood to include `dot`, `inv`, `det`, `cholesky` and a symmetric-only `eig`, which would cover least squares by normal equations and PCA from a covariance matrix; it is not understood to include SVD [unverified, check at build]. Any drill that needs more links to the web app.

---
## 4. Shared composite

### 4.1 `derivation-steps`: Derivation builder

Composite. P0, wave A. Cross-cluster: every topic with Derive screens uses it. Uses: `token-tray`, `expression-input`, `live-formula`, `stepper`, `choice`.

- **Purpose.** Derive screens (design 5.2): a derivation shown as aligned lines where some lines are blank (type them), shuffled (order them) or missing a justification (pick it from a tray). Linked to a canvas so each line can point at the picture it describes.
- **Serves.** 1.3.2 L4 and L5 (power and product rules); 1.3.4 L6 and L7 (parts, partial fractions); 1.3.5 L5 (Taylor coefficients); 1.3.7 L4 (Gaussian integral); 1.3.8 L4; 1.4.4 L5 (normal equations); 3.2.3 L3 (Itô's lemma with the $dt$, $dW$ multiplication table); 3.2.4 L1 (the Black-Scholes PDE).
- **Interactions.** Pointer: tap a blank line to type it; drag lines to reorder (token-tray sequence layout); drag justification chips ("binomial expansion", "$dW\cdot dW = dt$", "terms of order $dt^{3/2}$ vanish") onto lines. Keyboard: token-tray and expression-input paths; Up and Down move between lines.
- **State.** `{ order: Id[]; entries: Record<Id, string>; justifications: Record<Id, Id> }`.
- **Checks.** `multi` combining `ordering` (per-line marks), `expression` per blank line, and `set` for justifications. Green lines lock and amber lines reopen (design 5.4).
- **Config.**

```ts
interface DerivationStepsConfig extends BaseConfig {
  lines: Array<{
    id: Id;
    tex: string;                                   // the line, LaTeX inside aligned
    blank?: { check: CheckSpec };                  // learner types this line
    justification?: Id;                            // correct chip id
    links?: Id[];                                  // canvas elements this line describes
  }>;
  shuffle?: boolean;                               // order-the-steps variant
  chips?: Array<{ id: Id; tex: string }>;          // justification tray, with distractors
  grid?: { rows: string[]; cols: string[]; cells: Record<string, Id> };   // e.g. the dt, dW table
  canvas?: Id;                                     // a sibling widget whose ids `links` refers to
}
```

- **Visual.** KaTeX `aligned`, justifications in the right margin on desktop and below each line on mobile (design 9.4). Blank lines have a `--manip` dashed outline. Answer objects: the learner's lines and chips.
- **Motion.** Show-why highlights the linked canvas elements of the first wrong line.
- **Reduced motion.** Base.
- **Accessibility.** Lines form an ordered list; each blank is a labelled field; chips use token-tray semantics.
- **Tutor hooks.** Describes the derivation with the learner's entries and which lines are wrong. Ids: `line:<id>`, `chip:<id>`, `cell:<row>,<col>`.
- **Performance.** KaTeX renders each line once; re-render only the edited line.
- **Artifact and web.** No difference.
- **Generators.** Template derivations with seeded constants (for example $\frac{d}{dx}x^n$ with seeded $n$; partial fractions with seeded roots).

---

## 5. Calculus composites (1.3)

### 5.1 `limit-explorer`: Limit explorer

Composite. P0, wave B. Uses: `plot-2d`, `marks`, `drag-point`, `slider`, `value-table`, `numeric-input`, `live-formula`.

- **Purpose.** Approach a point from each side and read what the function approaches. Holes, jumps, vertical asymptotes, oscillation, limits at infinity and limits of sequences.
- **Serves.** 1.3.1 L1 to L5; 0.3 (sequences); 1.3.4 L8 (intuition for improper integrals).
- **Interactions.** Pointer: drag the left handle (always below $a$) and the right handle (always above $a$) along the $x$-axis; their curve points show dashed guides to the $y$-axis with values. The closeness slider moves both together, $h$ from 1 down to $10^{-6}$ on a log scale, and the view zooms around $(a, L)$ so both stay visible (half-width $5h$). Sequence mode: an $n$ slider on a log scale, dots for $a_n$. Infinity mode: a far handle at $x = 10^k$. Keyboard: handles and slider as base.
- **State.** `{ xLeft: number; xRight: number; h: number; zoom: number }`.
- **Checks.** `numeric` with specials (the limit, or DNE, $\infty$, $-\infty$); `multi` for left limit, right limit, value and limit; `choice` (exists, continuous).
- **Config.**

```ts
interface LimitExplorerConfig extends BaseConfig {
  f?: Expr;
  pieces?: Array<{ expr: Expr; domain: [number, number]; closed?: [boolean, boolean] }>;
  a: number | 'inf' | '-inf';
  mode: 'function' | 'sequence';
  valueAt?: number | null;           // f(a) when it differs from the limit; null: undefined (hole)
  view: { x: [number, number]; y: [number, number] };
  closeness?: { min: number; max: number };
  autoZoom?: boolean;
  sides?: 'both' | 'left' | 'right';
  bounds?: Array<{ id: Id; expr: Expr; label: string }>;   // squeeze theorem
  table?: boolean;
}
```

- **Visual.** $f$ in ink; holes as 7px hollow ink circles; $f(a)$ as a filled dot where defined; handles `--manip` with dashed guides; squeeze bounds in s2 and s3 with labels. After grading, the limit $L$ appears as a ghost horizontal line. Answer objects: the answer field and, in multi items, each one-sided reading.
- **Motion.** Zoom follows the slider directly. Show-why for "limit equals $f(a)$": the filled dot pulses, then both guides converge on $L$, not on the dot. For "DNE" on a two-sided limit that exists: both handles approach from their sides to the same height (600ms).
- **Reduced motion.** Base.
- **Accessibility.** The value table is the primary alternative; handle text reads "x = 1.99, f(x) = 3.99".
- **Tutor hooks.** Describe: "f(x) = (x^2 − 4)/(x − 2), a = 2, hole at x = 2. Left handle x = 1.9 (f = 3.9), right handle x = 2.1 (f = 4.1). Answer field: DNE." Ids: `handle:left`, `handle:right`, `slider:h`, `hole`, `dot:value`, `guide:left`, `guide:right`, `curve:f`, `bound:<id>`, `row:<i>`.
- **Performance.** SVG; adaptive curve; table at most 12 rows; under 1 ms.
- **Artifact and web.** No difference.
- **Generators.** Rational functions with a removable discontinuity ($\frac{(x-r)(x-s)}{x-r}$); piecewise jumps with integer values; vertical asymptotes; sequences (rational in $n$, $(1+\frac kn)^n$). Distractors: $f(a)$, one one-sided limit, DNE.

### 5.2 `epsilon-delta`: Epsilon-delta game

Composite. P0, wave B. Uses: `plot-2d`, `marks` (bands, curve), `drag-point`, `slider`, `live-formula`, `expression-input`.

- **Purpose.** Make the formal definition a game. For a given $\varepsilon$ band around $L$, find a $\delta$ such that the graph over $(a-\delta, a+\delta)$ stays inside the band. Then state $\delta$ as a function of $\varepsilon$. Sequence version: find $N$ for $\varepsilon$.
- **Serves.** 1.3.1 L7; 1.3.5 L2 (formal convergence).
- **Interactions.** Pointer: drag the $\delta$ handle on the $x$-axis (the strip is symmetric about $a$). Adversary mode: the widget plays the adversary, shrinking $\varepsilon$ each round (0.5, 0.1, 0.01); the learner answers each, then types $\delta(\varepsilon)$. Keyboard: base.
- **State.** `{ delta: number; eps: number; round: number; formula?: string }`.
- **Checks.** `predicate: delta-works` (the supremum of $\lvert f-L\rvert$ over the strip is below $\varepsilon$, by 400-point sampling refined by bisection); `predicate: delta-formula-works` (the typed $\delta(\varepsilon)$ is positive and works for a seeded sample of $\varepsilon$ values); `choice`.
- **Config.**

```ts
interface EpsilonDeltaConfig extends BaseConfig {
  f: Expr; a: number; L: number;
  mode: 'function' | 'sequence';
  eps: number | number[];            // fixed, or adversary rounds
  deltaRange: [number, number];
  liveEscape: boolean;               // Explore screens: show escaping arcs while dragging
  askFormula?: boolean;
}
```

- **Visual.** $\varepsilon$ band: dashed ink lines at $L\pm\varepsilon$ with a `--bg-sunken` wash. $\delta$ strip: `--manip-wash` (learner-controlled). Their intersection is the box. Arcs that leave the box turn amber only after Check on Problem screens (live on Explore screens). Answer objects: the $\delta$ strip and the escaping arcs.
- **Motion.** Show-why for a $\delta$ that is too large: zoom to the first escape point, mark it with a cross, show its coordinates.
- **Reduced motion.** Base.
- **Accessibility.** Describes escape points: "With δ = 0.3, f leaves the band at x = 2.27, where f = 5.15, above L + ε = 5.1."
- **Tutor hooks.** Ids: `handle:delta`, `band:eps`, `strip:delta`, `escape:<i>`, `field:formula`.
- **Performance.** Escape search under 0.5 ms per frame.
- **Artifact and web.** No difference.
- **Generators.** Linear $f$ (answer $\delta=\varepsilon/\lvert m\rvert$); $x^2$ near 2 (answer $\delta=\min(1,\varepsilon/5)$, from $\lvert x^2-4\rvert < 5\lvert x-2\rvert$ when $\lvert x-2\rvert<1$); sequences $\frac1n$ and $\frac{n+1}{n}$ (answer $N=\lceil 1/\varepsilon\rceil$).

### 5.3 `local-zoom`: Local zoom

Composite. P0, wave B (Brownian mode P2). Uses: `plot-2d` (main and inset), `drag-point`, `slider`, `marks`, `live-formula`.

- **Purpose.** Zoom into a point on a curve until it looks straight (differentiable), or does not (corner, cusp, oscillation, Brownian path). Measure the slope at high magnification. Compare two functions near a common zero (L'Hôpital).
- **Serves.** 1.3.2 L2, L11, L13; 3.2.2 L2.
- **Interactions.** Pointer: drag the zoom centre along the curve; magnification slider from 1 to $10^6$ on a log scale, or pinch on the inset. Measure mode: two points a fixed screen distance apart on the inset give rise over run. Ratio mode: $f$ and $g$ both in the inset, with $f(x)/g(x)$ read out as the centre approaches $a$. Keyboard: base.
- **State.** `{ x0: number; mag: number }`.
- **Checks.** `numeric` (slope at $x_0$, limit of the ratio); `choice` (differentiable here? if not, why: corner, cusp, vertical tangent, oscillation).
- **Config.**

```ts
interface LocalZoomConfig extends BaseConfig {
  f: Expr; g?: Expr;
  x0: number; movable: boolean;
  magRange: [number, number];
  showTangent: 'never' | 'after-check' | 'toggle';
  measure?: boolean;
  path?: { model: 'brownian'; seed: number };    // zoom into a sampled path
}
```

- **Visual.** Inset framed with 2px `--line`, radius r-md, with a "×1,000" chip; the zoom rectangle on the main plot in `--manip` because it follows the handle. Tangent (when shown) in s2. Answer objects: the answer field.
- **Motion.** Zoom follows the slider. Show-why for a corner: the inset splits into a left tangent (s2) and a right tangent (s3) with their different slopes labelled.
- **Reduced motion.** Base.
- **Accessibility.** "At ×1,000 around x = 0, |x| still shows a corner: slope −1 on the left, +1 on the right."
- **Tutor hooks.** Ids: `handle:centre`, `slider:mag`, `inset`, `tangent`, `slope:left`, `slope:right`, `curve:f`, `curve:g`.
- **Performance.** The inset resamples per frame with view-dependent adaptive sampling. Magnification is capped at $10^6$, because float64 round-off becomes visible beyond about $10^7$ for typical functions. Brownian mode refines the path by bridge sampling as magnification grows, deterministic by seed.
- **Artifact and web.** No difference.
- **Generators.** Pick from a catalogue ($x^2$, $\lvert x\rvert$, $x^{2/3}$, $x\sin\frac1x$, $x^2\sin\frac1x$, $\sqrt[3]{x}$) with seeded centres; L'Hôpital pairs with integer limits.

### 5.4 `secant-tangent`: Secant to tangent

Composite. P0, wave B. Uses: `plot-2d`, `marks`, `drag-point`, `slider`, `value-table`, `live-formula`, `numeric-input`, `expression-input`.

- **Purpose.** Average rate of change becomes instantaneous: the slope of secant $PQ$ as $Q\to P$. Also tangents to implicit and parametric curves, and the mean value theorem.
- **Serves.** 1.3.2 L1, L9, L12; 0.2 (gradient between two points).
- **Interactions.** Pointer: drag $P$ and $Q$ along the curve, or move $Q=P+h$ with a signed log slider so $Q$ can approach from either side. MVT mode: endpoints $A$ and $B$, and a third handle $C$ whose tangent the learner makes parallel to $AB$. Keyboard: base.
- **State.** `{ xP: number; xQ: number; xC?: number }` (or curve parameters for parametric and implicit curves).
- **Checks.** `numeric` (slope); `expression` ($f'(x)$ after the table); `predicate: mvt-point` (any $c$ where $f'(c)$ equals the chord slope, within tolerance); `choice`.
- **Config.**

```ts
interface SecantTangentConfig extends BaseConfig {
  curve: { y: Expr } | { implicit: Expr; level: number } | { param: [Expr, Expr]; t: [number, number] };
  P: number; Q?: number;
  h?: { range: [number, number]; signed: boolean };
  mode: 'secant' | 'tangent' | 'mvt';
  showTangent: 'never' | 'after-check' | 'limit';
  braces?: boolean; table?: boolean;
}
```

- **Visual.** Curve in ink; secant line in s2, extended across the plot; tangent in s3, dashed until confirmed; rise and run braces labelled $\Delta x$ and $\Delta y$. Answer objects: the answer field, or $C$ in MVT items.
- **Motion.** The secant rotates directly as $Q$ moves. Show-why for a wrong slope: the braces pulse with the learner's numbers against the real rise and run (catches swapped rise and run).
- **Reduced motion.** Base.
- **Accessibility.** Table of $h$ against slope; "Secant through P(1, 1) and Q(1.5, 2.25): slope 2.5."
- **Tutor hooks.** Ids: `handle:P`, `handle:Q`, `handle:C`, `slider:h`, `line:secant`, `line:tangent`, `brace:rise`, `brace:run`, `row:<i>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Polynomials of degree up to 3 with integer coefficients and points giving round slopes; circles and ellipses for implicit items; MVT on cubics with rational $c$.

### 5.5 `derivative-tracer`: Derivative tracer

Composite. P0, wave B. Uses: `plot-2d` (two or three, linked on $x$), `marks`, `drag-point`, `sketch-pad`, `slider`, `live-formula`, `choice`.

- **Purpose.** Link $f$, $f'$ and $f''$. Dragging along $f$ plots the tangent slope on the panel below, leaving a trace, so the learner builds the derivative graph. Sketch $f'$ from $f$, or $f$ from $f'$. Concavity. Find $e$ as the base whose slope equals its height.
- **Serves.** 1.3.2 L3, L7, L8; 1.3.3 L1 to L3; 1.3.4 L4.
- **Interactions.** Pointer: drag $x$ along $f$; dots accumulate on the lower panel; a "Reveal $f'$" toggle where allowed. Sketch modes put a `sketch-pad` on the lower panel (or the upper one, anchored at a given point, for antiderivatives). Base slider for $b^x$. Keyboard: base; sketch through points mode.
- **State.** `{ x: number; trace: number[]; sketch?: SketchState; params?: Record<string, number> }`.
- **Checks.** `curve` (sketch in band with features: zeros of $f'$ at extrema of $f$, signs on each interval); `point` (the $x$ where the slope equals a target); `choice` (which graph is $f'$, with thumbnail options); `expression` ($f'(x)$).
- **Config.**

```ts
interface DerivativeTracerConfig extends BaseConfig {
  f: Expr; domain: [number, number];
  params?: SliderConfig[];
  panels: Array<'f' | 'df' | 'd2f'>;
  mode: 'trace' | 'sketch-derivative' | 'sketch-antiderivative' | 'match';
  reveal: 'never' | 'after-check' | 'toggle';
  anchor?: Vec2;                     // antiderivative sketches pass through this point
  concavityBands?: boolean;
}
```

- **Visual.** $f$ in ink; tangent segment in s2 (fixed length, 30% of the width, centred on the point); trace dots in s2; revealed $f'$ in s2 and $f''$ in s3; a dashed vertical crosshair across panels. Concavity bands: s3 and s5 washes at 10% with the direct labels "concave up" and "concave down". Answer objects: the sketch or the answer field.
- **Motion.** Direct. Show-why for a wrong sketch: the true $f'$ draws on; intervals with the wrong sign flash twice (150ms).
- **Reduced motion.** Base.
- **Accessibility.** Table of $x$, $f(x)$, $f'(x)$ at sample points; sketches described in words.
- **Tutor hooks.** Ids: `handle:x`, `tangent`, `trace`, `curve:f`, `curve:df`, `curve:d2f`, `sketch`, `feature:<i>`, `band:<i>`, `slider:<param>`.
- **Performance.** $f'$ and $f''$ come from symbolic differentiation at mount, never finite differences; under 1 ms per frame.
- **Artifact and web.** No difference.
- **Generators.** Cubics and quartics with integer critical points; trigonometric and exponential families; "which is $f'$" option sets whose distractors are $f''$, $-f'$, a shifted $f'$ and an antiderivative.

### 5.6 `growth-rectangle`: Growing square, cube and rectangle

Composite. P0, wave B. Uses: `plot-2d` (geometry, equal aspect), `plot-3d` (cube), `drag-point`, `slider`, `marks`, `token-tray`, `live-formula`.

- **Purpose.** Derive derivative rules from growth. A square of side $x$ grows by $2x\,dx + dx^2$; a cube by $3x^2\,dx$ plus smaller pieces; a rectangle $f\cdot g$ by the strips $f\,dg$ and $g\,df$ plus the corner $df\,dg$. As $dx\to0$ the corner pieces vanish faster than the strips.
- **Serves.** 1.3.2 L4, L5; 0.2 (area model for expanding brackets), cross-cluster.
- **Interactions.** Pointer: drag the corner to grow the shape; a $dx$ slider on a log scale shrinks the growth; drag term tokens onto the strips to label them. Keyboard: base.
- **State.** `{ x: number; dx: number; labels: Record<Id, Id> }`.
- **Checks.** `set` (labels match pieces); `numeric` ($\Delta A$ for given numbers); `expression` (the rule), usually through `derivation-steps`.
- **Config.** `{ shape: 'square' | 'cube' | 'rectangle'; f?: Expr; g?: Expr; x: number; dxRange: [number, number]; labelTokens?: boolean; ratioReadout?: boolean }`.
- **Visual.** The original shape with an ink outline and `--bg-sunken` fill; strips in s2 and s3 at 25%, each with a direct label ($x\,dx$); the corner in s5 with a label. The cube shows three slabs, three rods and a small cube. Answer objects: the placed labels.
- **Motion.** Direct. Show-why when the corner is labelled first-order: $dx$ tweens down over 800ms while a readout shows the corner's share of the growth falling to zero.
- **Reduced motion.** A three-row table ($dx = 0.5$, $0.05$, $0.005$) replaces the tween.
- **Accessibility.** Areas described numerically, for example "strips 2 × 3 × 0.1 = 0.6, corner 0.01".
- **Tutor hooks.** Ids: `handle:corner`, `slider:dx`, `strip:1`, `strip:2`, `corner`, `slot:<i>`, `readout:ratio`.
- **Performance.** Trivial; the cube uses a small `plot-3d` scene.
- **Artifact and web.** No difference.
- **Generators.** Integer $x$ and $dx$ for numeric items; product pairs ($x\cdot\sin x$, $x\cdot e^x$).

### 5.7 `function-mapping`: Mapping diagram

Composite. P0, wave A. Cross-cluster (0.2 functions; 1.5 transformations of random variables). Uses: `number-line` (two or three, parallel), `marks`, `drag-point`, `slider`, `live-formula`.

- **Purpose.** Functions as maps between number lines. A small interval $[x, x+dx]$ maps to an interval whose length is stretched by $g'(x)$; composition multiplies stretches (chain rule); an inverse divides them; substitution in integrals rescales strip widths.
- **Serves.** 0.2 (composition, inverses); 1.3.2 L6, L7, L9; 1.3.4 L5; 1.5 (density of $g(X)$ scales by $1/\lvert g'\rvert$).
- **Interactions.** Pointer: drag $x$ on the top line; the $dx$ band and its images move; a $dx$ slider. Grid mode: evenly spaced points on line 1 land unevenly on line 2, showing where the map stretches and squeezes. Substitution mode: a strip of width $dx$ under the integrand maps to a strip of width $du$ of equal area. Keyboard: base.
- **State.** `{ x: number; dx: number }`.
- **Checks.** `numeric` (stretch factor; the composite derivative at $x$); `expression` (chain-rule result, substituted integral); `choice`.
- **Config.**

```ts
interface FunctionMappingConfig extends BaseConfig {
  maps: Array<{ name: string; expr: Expr; from: string; to: string }>;   // a chain of maps
  lines: Array<{ variable: string; range: [number, number] }>;
  mode: 'map' | 'chain' | 'inverse' | 'substitution';
  x: number; dxRange: [number, number];
  gridPoints?: number;
  integrand?: Expr;                  // substitution mode
}
```

- **Visual.** Horizontal number lines 72px apart; connectors 1px `--text-muted`; the $dx$ band in `--manip`, its images in s2 and s3; stretch chips ("×2.4") between lines. Answer objects: the answer field.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** "x = 1.2 → u = 1.44 → y = 0.99. A step dx = 0.01 becomes du = 0.024 (×2.4), then dy = 0.0041 (×0.17). Overall ×0.41, the derivative."
- **Tutor hooks.** Ids: `handle:x`, `slider:dx`, `band:<variable>`, `factor:<map>`, `line:<variable>`.
- **Performance.** Trivial SVG.
- **Artifact and web.** No difference.
- **Generators.** Compositions of polynomial, exponential and trigonometric maps at points with tidy values; substitution integrals with integer bounds.

### 5.8 `root-finder`: Root finder

Composite. P0, wave B. Uses: `plot-2d`, `marks`, `drag-point`, `stepper`, `value-table`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** Algorithms that find zeros. Bisection (the intermediate value theorem made constructive), Newton's method (iterate tangent lines), the secant method; convergence speed; failure modes.
- **Serves.** 1.3.1 L6; 1.3.2 L11; 1.1 and 1.8 (bisection in code), cross-cluster; 1.7 (implied volatility by Newton), P1 transfer.
- **Interactions.** Pointer: drag $x_0$ or the bracket ends; Step applies one iteration. Predict mode: before each step the learner drags a marker to where $x_{n+1}$ will land. Keyboard: base.
- **State.** `{ x0: number; bracket?: [number, number]; iterates: number[]; prediction?: number }`.
- **Checks.** `point` (predicted next iterate, metric `x`); `numeric` (root to $k$ decimals; steps needed); `choice` (why Newton failed here: flat tangent, cycle, jump to another root).
- **Config.** `{ f: Expr; method: 'bisection' | 'newton' | 'secant'; x0?: number; bracket?: [number, number]; maxSteps: number; predict?: boolean; errorPlot?: boolean }`.
- **Visual.** Iterates as numbered ink dots on the axis ($x_0$, $x_1$, ...); tangent segments in s2 from $(x_n, f(x_n))$ to the axis; the learner's bracket as a `--manip-wash` band, with later brackets nested in s2. An optional error panel plots digits of accuracy against $n$ (Newton's roughly double each step). Answer objects: the prediction marker or the answer field.
- **Motion.** Each step slides the tangent down to the axis (480ms, ease-morph); this is a demonstration of the algorithm.
- **Reduced motion.** Steps appear at once.
- **Accessibility.** The table ($n$, $x_n$, $f(x_n)$, error) is primary.
- **Tutor hooks.** Ids: `handle:x0`, `handle:lo`, `handle:hi`, `iterate:<n>`, `tangent:<n>`, `bracket:<n>`, `row:<n>`, `marker:predict`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Polynomials with an irrational root in an integer bracket; designed failures, such as $f(x)=x^3-2x+2$ from $x_0=0$, which cycles between 0 and 1.

### 5.9 `rates-scene`: Related rates scene

Composite. P0, wave B. Uses: `plot-2d` (scene coordinates), `marks` (polygons with Expr vertices, rate arrows), `drag-point`, `slider` (time, with Play), `live-formula`, `numeric-input`, `expression-input`.

- **Purpose.** Related rates in a physical scene: a ladder sliding down a wall, a cone filling, a ripple spreading, two cars, a lengthening shadow. One quantity is driven; the rates of the others appear as arrows.
- **Serves.** 1.3.2 L10.
- **Interactions.** Pointer: drag the driven quantity, or play time at the stated rate; freeze at the asked instant. Keyboard: base; time slider.
- **State.** `{ t: number }` (or the driven variable).
- **Checks.** `numeric` (a rate at an instant, with units); `expression` (the differentiated relation); `choice` (sign of a rate).
- **Config.** `{ vars: Record<string, Expr>; relation: Expr; scene: MarkSpec[]; driver: { var: string; rate: number; units: string }; rates: Array<{ var: string; units: string; arrowAt: Expr[] }>; askAt?: number }`.
- **Visual.** Scene in ink outlines with `--bg-sunken` fills; driver handle in `--manip`; rate arrows in s2 with labels such as $\dot y = -0.8$ m/s. Answer objects: the answer field.
- **Motion.** Play is linear time; dragging is direct.
- **Reduced motion.** Play steps at four frames per second.
- **Accessibility.** The scene described with numbers and units.
- **Tutor hooks.** Ids: `handle:driver`, `slider:t`, `arrow:<var>`, `shape:<id>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Ladder lengths from Pythagorean triples; cone dimensions and fill rates with tidy answers.

### 5.10 `objective-explorer`: Optimisation explorer

Composite. P0, wave B. Uses: `plot-2d` (scene and objective), `marks`, `drag-point`, `slider`, `live-formula`, `numeric-input`, `expression-input`; optionally `sign-chart`.

- **Purpose.** Optimise one variable in context. A scene (box from a sheet, fence, can, bet fraction, portfolio weight, price) is linked to the objective curve $f(x)$. The learner searches by hand first, then derives $f'(x)=0$ and confirms with the second derivative or a sign chart.
- **Serves.** 1.3.3 L4, L5; 1.5 and 1.7 (Kelly growth, two-asset variance), cross-cluster.
- **Interactions.** Pointer: drag $x$ in the scene or on the curve (the two are synchronised). A best-so-far marker records the learner's best attempt. Keyboard: base.
- **State.** `{ x: number; best: { x: number; value: number } }`.
- **Checks.** `point` or `numeric` (the optimiser within tolerance, the optimal value); `expression` (the model $f(x)$ the learner writes; $f'(x)$); `choice` (interior optimum or endpoint).
- **Config.** `{ scene: MarkSpec[]; x: { var: string; range: [number, number]; init: number }; objective: { expr: Expr; label: string; units?: string }; showCurve: 'always' | 'after-explore' | 'never'; preset?: 'box' | 'fence' | 'can' | 'kelly' | 'min-variance' | 'price' }`.
- **Presets.** Kelly: $g(f)=p\ln(1+bf)+(1-p)\ln(1-f)$, maximised at $f^*=p-\frac{1-p}{b}$. Minimum variance: $w^*=\frac{\sigma_2^2-\rho\sigma_1\sigma_2}{\sigma_1^2+\sigma_2^2-2\rho\sigma_1\sigma_2}$.
- **Visual.** Scene left (top on mobile), objective right (below on mobile); the current point in `--manip` on both; best-so-far as a ghost; objective curve in ink. Answer objects: the learner's chosen point or field.
- **Motion.** Direct. Show-why for an endpoint answer: the curve near the boundary is highlighted and the interior maximum pulses.
- **Reduced motion.** Base.
- **Accessibility.** Table of $x$ against the objective.
- **Tutor hooks.** Ids: `handle:x`, `scene:<shape>`, `curve:objective`, `marker:best`, `point:optimum`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Sheet sizes with a tidy optimal cut; Kelly with $(p, b)$ giving round fractions; two-asset $(\sigma_1, \sigma_2, \rho)$ giving round weights.

### 5.11 `sign-chart`: Sign table

Composite. P0, wave A. Cross-cluster (0.2 inequalities). Uses: `number-line`, `region-select` (cycling states), `drag-point`, `marks`, `choice`; optionally a linked `plot-2d`.

- **Purpose.** Sign analysis on a number line: factors of an expression for inequalities, $f'$ for monotonicity, $f''$ for concavity, linked to a graph.
- **Serves.** 0.2 (quadratic and rational inequalities); 1.3.3 L1 to L3.
- **Interactions.** Pointer: place critical points (tap the line, drag to adjust, or type); tap each interval cell to cycle blank, +, −. Multi-row tables have one row per factor and a product row; the last row shows increasing or decreasing arrows. Keyboard: grid navigation; Space cycles.
- **State.** `{ points: number[]; signs: Record<RowId, Array<'+' | '-' | ''>> }`.
- **Checks.** `set` (critical points within tolerance); `set` (signs per interval, partial marks per cell); `choice` (maximum, minimum or neither at each point).
- **Config.** `{ range: [number, number]; rows: Array<{ id: Id; label: string; expr?: Expr }>; points: 'given' | 'place'; truePoints: number[]; linkPlot?: Id; derivedRow?: 'product' | 'monotonicity' | 'concavity' }`.
- **Visual.** Table grid in `--line`; signs in ink 700 weight; learner-set cells in `--manip-wash` until Check. Answer objects: the learner's cells and points.
- **Motion.** None beyond grading.
- **Reduced motion.** Base.
- **Accessibility.** Grid semantics; each cell named "row x minus 1, interval 1 to 3".
- **Tutor hooks.** Ids: `point:<i>`, `cell:<row>:<interval>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Factored polynomials and rationals with integer roots and poles.

### 5.12 `convexity-chord`: Convexity and Jensen

Composite. P0, wave B. Uses: `plot-2d`, `marks`, `drag-point`, `slider`, `live-formula`, `choice`.

- **Purpose.** Convex and concave functions through chords and tangents; Jensen's inequality, $E[f(X)]\ge f(E[X])$ for convex $f$; the start of the intuition behind volatility drag and option convexity.
- **Serves.** 1.3.3 L6; 1.5 (Jensen), cross-cluster; 1.7 (convex payoffs), P1; 3.2.3 (Itô drift), P2.
- **Interactions.** Pointer: drag two points on the curve; drag $\lambda$ along the chord to compare $\lambda f(x_1)+(1-\lambda)f(x_2)$ with $f(\lambda x_1+(1-\lambda)x_2)$. Distribution mode: up to four atoms on the $x$-axis with probability handles (bars below the axis); $E[X]$ and $E[f(X)]$ are marked and the gap is labelled. Keyboard: base.
- **State.** `{ xs: number[]; ws: number[]; lambda: number }`.
- **Checks.** `choice` (convex, concave or neither on an interval); `numeric` (the Jensen gap); `predicate` (two points whose chord dips below the curve, proving non-convexity).
- **Config.** `{ f: Expr; domain: [number, number]; mode: 'chord' | 'tangent' | 'jensen'; points: number[]; weights?: number[] }`.
- **Visual.** Chord in s2; tangent in s3; the gap as an ink brace with a label; atom handles in `--manip`. Answer objects: the answer field, or the learner's point pair.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** "The chord lies above the curve everywhere between 1 and 3; at λ = 0.5 the gap is 0.25."
- **Tutor hooks.** Ids: `handle:x1`, `handle:x2`, `handle:lambda`, `chord`, `tangent`, `gap`, `atom:<i>`, `point:Ef`, `point:fE`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** $x^2$, $e^x$, $\ln x$, $\sqrt x$, $\lvert x\rvert$ and $x^3$ (neither) on seeded intervals; two-point distributions with rational weights.

### 5.13 `riemann-sum`: Riemann sums

Composite. P0, wave B. Uses: `plot-2d` (plus an error inset), `marks` (curve, bars, regions), `drag-point`, `slider`, `choice` (rule switch), `value-table`, `live-formula`.

- **Purpose.** Area by rectangles: left, right, midpoint, upper and lower sums, trapezoids and Simpson's rule; signed area; area between curves; average value; error against $n$.
- **Serves.** 1.3.4 L1, L2, L9, L11; 1.5 (probability as area, numerically), cross-cluster.
- **Interactions.** Pointer: drag $a$ and $b$; the $n$ slider (1 to 1,000 on a log list); the rule switch; tap a bar to see height times width. Average mode: drag a horizontal level line until the area above $f$ equals the area below. Keyboard: base.
- **State.** `{ a: number; b: number; n: number; rule: Rule; level?: number }`.
- **Checks.** `numeric` (the sum, the exact area, the smallest $n$ for an error below a tolerance, the error ratio when $n$ doubles); `choice` (over or under); `point` (the average level, metric `y`).
- **Config.**

```ts
interface RiemannSumConfig extends BaseConfig {
  f: Expr; g?: Expr;                     // g: lower curve for area between curves
  a: number; b: number; movableEnds: boolean;
  n: number; nValues?: number[];
  rules: Array<'left' | 'right' | 'mid' | 'trap' | 'upper' | 'lower' | 'simpson'>;
  showExact: 'never' | 'after-check' | 'always';
  errorInset?: boolean; signed?: boolean; averageMode?: boolean;
}
```

- **Visual.** $f$ in ink. Bars filled s2 at 20% with s2 outlines; in signed mode, positive parts in s3 and negative parts in s2, each with a + or − glyph. The slivers between bar tops and the curve (`gap:<i>`) are drawn but unfilled until a show-why highlights them. The error inset is a log-log plot in ink with slope labels. Answer objects: the answer field or the level line.
- **Motion.** $n$ changes redraw at once. Show-why for over or under: the gaps highlight with the focus wash.
- **Reduced motion.** Base.
- **Accessibility.** Table of $i$, $x_i^*$, $f(x_i^*)$, area of bar $i$, and the total.
- **Tutor hooks.** Ids: `handle:a`, `handle:b`, `slider:n`, `rule:<r>`, `bar:<i>`, `gap:<i>`, `curve:f`, `readout:sum`, `inset:error`, `handle:level`.
- **Performance.** SVG up to 200 bars; above that, all bar outlines go into one path; recompute under 1 ms.
- **Artifact and web.** No difference.
- **Generators.** Polynomials with integer coefficients on integer intervals (exact areas rational); seeded rule and $n$; distractors encode "left always overestimates" and "more rectangles always means smaller error for every rule at the same rate".

### 5.14 `accumulator`: Accumulation function

Composite. P0, wave B. Uses: `plot-2d` (two, linked on $x$), `marks`, `drag-point`, `slider`, `sketch-pad`, `live-formula`, `numeric-input`, `expression-input`.

- **Purpose.** The accumulation function $A(x)=\int_a^x f(t)\,dt$ linked to $f$: area so far, the fundamental theorem ($A'=f$), families of antiderivatives ($+C$), improper integrals by pushing the upper limit to infinity, densities and CDFs.
- **Serves.** 1.3.4 L2, L3, L4, L8, L13; 1.5 (density to CDF), cross-cluster.
- **Interactions.** Pointer: drag $x$; the region from $a$ to $x$ shades and the $A(x)$ dot moves below, leaving a trace; toggle the tangent to $A$ at $x$ (slope equals $f(x)$); drag $a$ and the whole $A$ curve shifts vertically. Improper mode: $x$ on a compressed axis ($x=10^k$) with a running value and a convergence panel. Sketch mode: sketch $A$ before revealing it. Keyboard: base.
- **State.** `{ a: number; x: number; trace: number[]; sketch?: SketchState }`.
- **Checks.** `numeric` ($A(x)$; the improper integral or DNE); `curve` (sketch of $A$); `choice` (converges or diverges); `expression` (`mode: 'antiderivative'`).
- **Config.** `{ f: Expr; a: number; movableA: boolean; x: number; domain: [number, number]; mode: 'accumulate' | 'ftc' | 'improper' | 'density'; reveal: 'never' | 'after-check' | 'toggle'; closedForm?: Expr }`.
- **Visual.** $f$ in ink; the region in s3 (positive) and s2 (negative) at 20% with + and − glyphs; $A$ in s2 with the direct label $A(x)$; tangent to $A$ in s3; a dashed crosshair across both panels. Answer objects: the answer field or sketch.
- **Motion.** Direct. Show-why for sign confusion: the region below the axis flashes with its − glyph while $A$'s falling stretch highlights.
- **Reduced motion.** Base.
- **Accessibility.** Table of $x$ against $A(x)$.
- **Tutor hooks.** Ids: `handle:x`, `handle:a`, `region`, `curve:f`, `curve:A`, `tangent:A`, `panel:convergence`.
- **Performance.** $A$ is precomputed by cumulative adaptive quadrature on a 512-point grid (cached per $a$), with local refinement per frame; under 0.5 ms.
- **Artifact and web.** No difference.
- **Generators.** Polynomial and exponential integrands; improper items with $x^{-p}$ for $p$ in $\{0.5, 1, 1.5, 2, 3\}$; densities (exponential, triangular, uniform) with tidy probabilities.

### 5.15 `slope-field`: Slope field and Euler's method

Composite. P0, wave B. Uses: `plot-2d`, `marks` (field, curves, polyline), `drag-point`, `slider`, `stepper`, `value-table`, `sketch-pad`, `choice`.

- **Purpose.** First-order differential equations $y'=F(x,y)$: direction fields, solution curves through chosen points, Euler's method and its error, equilibria. Exponential growth, decay, logistic growth and continuous compounding.
- **Serves.** 1.3.4 L4, L12.
- **Interactions.** Pointer: drag the initial point; its solution curve follows. Euler mode: choose $h$, step through, and predict each next point before it is drawn. Sketch mode: sketch the solution through a given point. Parameter sliders (for example the rate $r$). Keyboard: base.
- **State.** `{ ic: Vec2; h: number; steps: number; prediction?: Vec2 }`.
- **Checks.** `point` (the next Euler point); `numeric` ($y(T)$ by Euler with a given $h$; the error ratio when $h$ halves); `curve` (sketched solution against the RK4 solution); `choice` (which equation matches the field, with thumbnail options); `expression` (separable solution).
- **Config.** `{ F: Expr; view: Plot2DConfig['view']; arrowsPerSide: number; ic?: Vec2; movableIc: boolean; euler?: { h: number; steps: number; predict?: boolean }; exact?: Expr; params?: SliderConfig[] }`.
- **Visual.** Field segments 1px `--text-muted` at 70% of cell length; solution in s3, 2px; Euler polyline in s2 with dots. Answer objects: the prediction marker, the sketch or the field.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** Qualitative description computed from the field: equilibria and their stability ("y = 0 unstable, y = 1 stable").
- **Tutor hooks.** Ids: `handle:ic`, `solution`, `euler:<k>`, `field`, `slider:h`, `marker:predict`.
- **Performance.** At most 625 field segments in one SVG path; RK4 with 400 steps per frame under 1 ms.
- **Artifact and web.** No difference.
- **Generators.** $y'=ky$, logistic $y'=ry(1-y)$, $y'=x+y$ and cooling laws with seeded parameters; Euler items with tidy $h$.

### 5.16 `solid-of-revolution`: Solid of revolution

Composite. P0, wave C. Uses: `plot-2d` (profile), `plot-3d`, `drag-point`, `slider`, `choice`, `marks`, `live-formula`.

- **Purpose.** Volumes of revolution by discs, washers and shells.
- **Serves.** 1.3.4 L10 (in the 18.01 exit exam).
- **Interactions.** Pointer: a sweep slider (0 to $2\pi$) builds the solid; drag $x$ on the profile to show its representative disc or shell in 3D; an $n$ slider stacks discs to approximate the volume; choose the axis ($x$-axis, $y$-axis or a line $y=k$). Keyboard: base; 3D orbit.
- **State.** `{ sweep: number; x: number; n: number; method: 'disc' | 'washer' | 'shell'; axis: Axis }`.
- **Checks.** `numeric` (volume); `expression` (the integral set up); `choice` (which method is easier).
- **Config.** `{ f: Expr; g?: Expr; a: number; b: number; axis: { kind: 'x' | 'y'; at: number }; methods: Array<'disc' | 'washer' | 'shell'>; n: number }`.
- **Visual.** Profile region in s3 at 25%; solid shaded with the sequential ramp; the representative slice in s2. Answer objects: the answer fields.
- **Motion.** Sweep is direct. Show-why for a wrong method: the slice morphs between perpendicular (disc) and parallel (shell) orientations to show which one the learner's integrand describes.
- **Reduced motion.** Base.
- **Accessibility.** The solid described in words; table of slice volumes.
- **Tutor hooks.** Ids: `slider:sweep`, `handle:x`, `slice`, `profile`, `solid`, `axis`.
- **Performance.** Solid mesh 32 by 24 on phones.
- **Artifact and web.** No difference.
- **Generators.** Polynomial and root profiles on integer bounds with tidy volumes.

### 5.17 `series-explorer`: Series explorer

Composite. P0, wave A (0.3 geometric series). Uses: `plot-2d`, `marks`, `slider`, `number-line`, `drag-point`, `value-table`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** Series as partial sums: convergence and divergence; geometric series; the integral, comparison, ratio and alternating tests; power series at a chosen $x$ and the radius of convergence; partial sums of $e^{i\theta}$ in the complex plane.
- **Serves.** 0.3 (sequences and series); 1.3.5 L1 to L4, L8; 1.7 (annuities and perpetuities), P1 transfer; 1.5 (geometric expectation), cross-cluster.
- **Interactions.** Pointer: the $N$ slider (log scale to $10^6$); a tail bracket shows the remainder; integral-test overlay toggle; power mode: drag $x$ on a number line strip and watch the partial sums settle or explode, then mark the interval; geometric picture mode: a unit square subdivided by the ratio. Complex mode: terms drawn head to tail as arrows; the term is given as a pair of Exprs (real part, imaginary part), so `expr` needs no complex arithmetic. Keyboard: base.
- **State.** `{ N: number; x?: number; interval?: IntervalState }`.
- **Checks.** `numeric` (the sum; $N$ for error below $\varepsilon$); `choice` (converges or diverges, and by which test); `interval` (interval of convergence with endpoint openness); `point` (complex mode: where the partial sums settle).
- **Config.** `{ term: Expr | [Expr, Expr]; start: number; mode: 'partial-sums' | 'geometric-picture' | 'integral-test' | 'ratio' | 'alternating' | 'power' | 'complex'; NRange: [number, number]; x?: { range: [number, number]; init: number }; limit?: number | 'diverges'; compareTo?: Expr }`.
- **Visual.** Term bars in s2; partial sums as ink dots joined by a thin line; the limit as a ghost; the alternating error band in `--bg-sunken` labelled "error at most the next term". Answer objects: the answer field or the marked interval.
- **Motion.** Direct. Show-why for "the terms go to zero, so it converges": $N$ tweens to $10^6$ on a log axis while partial sums keep climbing beside an overlaid $\ln N$ curve.
- **Reduced motion.** Base.
- **Accessibility.** Table of $N$ and partial sums.
- **Tutor hooks.** Ids: `slider:N`, `bar:<n>`, `sum:<N>`, `limit`, `tail`, `handle:x`, `interval`, `overlay:integral`.
- **Performance.** Partial sums to $10^6$ with Kahan summation, plotted at no more than 400 points on a log-$N$ axis.
- **Artifact and web.** No difference.
- **Generators.** Geometric series with rational ratios; $p$-series; telescoping series; power series with integer radii and mixed endpoint behaviour.

### 5.18 `taylor-builder`: Taylor builder

Composite. P0, wave B. Uses: `plot-2d`, `drag-point`, `slider`, `marks`, `live-formula`, `value-table`, `numeric-input`, `expression-input`.

- **Purpose.** Build Taylor polynomials by matching value, slope and curvature at a centre; see the error and the remainder bound; find the radius of convergence; apply it to bonds (duration and convexity) and options (delta and gamma).
- **Serves.** 1.3.5 L5 to L7, L9; 1.7 (bond duration and convexity; delta-gamma), P1 transfer; 1.6 (the delta method), cross-cluster.
- **Interactions.** Pointer: drag the centre $a$ along the axis; the degree slider (0 to 10); match mode: coefficient sliders $c_0$ to $c_4$ with readouts of the value, slope and curvature mismatch at $a$. Transfer presets: drag the yield change $\Delta y$ (or the price move $\Delta S$) and compare the true change with the linear and quadratic approximations. Keyboard: base.
- **State.** `{ a: number; degree: number; coefficients?: number[]; delta?: number }`.
- **Checks.** `numeric` (each coefficient; an approximation; an error bound); `expression` (the polynomial); `point` (where the error first exceeds a tolerance, metric `x`); `choice`.
- **Config.** `{ f: Expr; centre: number; movableCentre: boolean; degree: number; maxDegree: number; mode: 'overlay' | 'match-coefficients' | 'remainder' | 'transfer'; coefficientRanges?: Array<[number, number]>; errorBand?: boolean; radius?: number | null; preset?: 'bond-price' | 'option-delta-gamma' }`.
- **Visual.** $f$ in ink; $T_n$ in s2; the error between them in s2 at 15%; the remainder bound as a `--bg-sunken` band; the radius of convergence as a bracket on the axis. Answer objects: the coefficient sliders in match mode, otherwise the fields.
- **Motion.** Direct. Show-why for a sign error in a coefficient: the polynomial with the corrected sign appears as a ghost bending the other way.
- **Reduced motion.** Base.
- **Accessibility.** Table of $x$, $f(x)$, $T_n(x)$ and error; the polynomial read as text.
- **Tutor hooks.** Ids: `handle:centre`, `slider:degree`, `coef:<k>`, `curve:f`, `curve:T`, `error`, `radius`, `handle:delta`.
- **Performance.** Coefficients from truncated power-series arithmetic in `expr` (no expression swell), recomputed per frame while the centre moves; under 1 ms to degree 10.
- **Artifact and web.** No difference.
- **Generators.** $e^x$, $\sin x$, $\cos x$, $\ln(1+x)$, $\frac{1}{1-x}$, $\sqrt{1+x}$, $\arctan x$ at seeded centres and degrees; bonds with seeded coupons and maturities.

### 5.19 `surface-explorer`: Surface and contour explorer

Composite. P0, wave C. Uses: `plot-3d`, `plot-2d` (contour map and two slice panels), `marks`, `drag-point`, `slider`, `live-formula`, `numeric-input`, `expression-input`.

- **Purpose.** Functions of two variables as surfaces and contour maps; partial derivatives as slopes of slices; tangent planes and linear approximation.
- **Serves.** 1.3.6 L1 to L3, L7; 1.6 (likelihood surfaces), cross-cluster; 2.1 (loss surfaces), cross-cluster.
- **Interactions.** Pointer: drag the point on the contour map; the 3D view shows it on the surface with slice planes $x=x_0$ and $y=y_0$; the side panels show the slice curves with tangent lines whose slopes are $f_x$ and $f_y$; toggle the tangent plane. Walk mode: arrow keys move the point like walking on a hill. Keyboard: base; 3D orbit.
- **State.** `{ point: Vec2; camera: Camera; toggles: Record<string, boolean> }`.
- **Checks.** `numeric` ($f_x$, $f_y$, the linear estimate); `choice` (signs of the partials read from the contour map); `point` (find a point where $f_x=0$ and $f_y>0$; find the summit); `expression` (a partial derivative).
- **Config.** `{ f: Expr; box: Plot3DConfig['box']; contours: { levels: number[] | number; labels: boolean }; point: Vec2; show: { surface: boolean; contour: boolean; slices: boolean; tangentPlane: 'never' | 'toggle' | 'after-check' }; layout: 'side-by-side' | 'stacked' | 'contour-only' }`.
- **Visual.** Surface shaded with the sequential ramp; contours in ink, 1px, with level labels; slice planes translucent in s2 and s3; the matching slice curves in s2 and s3 in their panels; the point in `--manip`. Answer objects: the point (in locate items) or the fields.
- **Motion.** Direct; camera presets over 280ms.
- **Reduced motion.** Base.
- **Accessibility.** The contour map is the accessible view; "At (1, 2), f = 5. Moving in +x, f rises 2 per unit; moving in +y, f falls 1 per unit." An optional coarse 7 by 7 value table.
- **Tutor hooks.** Ids: `handle:point`, `slice:x`, `slice:y`, `panel:x`, `panel:y`, `contour:<level>`, `plane:tangent`, `surface`.
- **Performance.** Contours by marching squares on 64 by 64, computed once per function (dragging the point does not recompute them); surface mesh 32 by 32 on phones; slice curves 200 points each per frame.
- **Artifact and web.** No difference.
- **Generators.** Quadratics, products, Gaussian bumps and saddles with seeded coefficients; points chosen so the partials are integers.

### 5.20 `gradient-compass`: Gradient compass

Composite. P0, wave C. Uses: `plot-2d` (contour map, and a second plot of slope against angle), `drag-point` (point; direction handle on a circle), `marks`, `live-formula`.

- **Purpose.** Directional derivatives and the gradient: which way is steepest, why the gradient crosses contours at right angles, and $D_{\mathbf u}f=\nabla f\cdot\mathbf u=\lvert\nabla f\rvert\cos\theta$.
- **Serves.** 1.3.6 L5; 2.1 (gradients), cross-cluster.
- **Interactions.** Pointer: drag the point; drag the direction handle round a dial centred on it; the directional derivative shows as a signed bar and as a dot on the angle plot, which traces a cosine as the needle turns. Keyboard: base (the direction handle steps in degrees).
- **State.** `{ point: Vec2; theta: number }`.
- **Checks.** `point` with metric `angle` (steepest ascent within $\pm5^\circ$; a direction of zero change); `numeric` ($\lvert\nabla f\rvert$, $D_{\mathbf u}f$); `expression` (the components of $\nabla f$); `choice`.
- **Config.** `{ f: Expr; point: Vec2; movablePoint: boolean; theta: number; revealGradient: 'never' | 'after-check' | 'toggle'; anglePlot: boolean }`.
- **Visual.** Dial ring in 1.5px `--line`, radius 48px; the needle in `--manip`; the gradient (after reveal) in s2 labelled $\nabla f$; the contour through the point in ink, 2px. Answer objects: the needle.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** The direction handle reports degrees; "Heading 30°: f rises at 1.73 per unit; steepest rise 2.0 at 0°."
- **Tutor hooks.** Ids: `handle:point`, `handle:direction`, `vector:grad`, `contour:through-point`, `plot:angle`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Linear and quadratic functions with integer gradients at seeded points.

### 5.21 `descent-lab`: Gradient descent lab

Composite. P0, wave C (momentum and stochastic modes P2; Newton mode P1). Uses: `plot-2d` (contour map and loss curve), `drag-point`, `slider`, `stepper`, `marks`, `value-table`, `numeric-input`, `choice`.

- **Purpose.** Gradient descent on a contour map: the learning rate, divergence, zig-zagging in narrow valleys, and the link between convergence and the eigenvalues of the Hessian.
- **Serves.** 1.3.6 L6; 1.4.6 and 1.4.7 (conditioning seen through eigenvalues); 2.1 (training), cross-cluster.
- **Interactions.** Pointer: drag the start point; the learning-rate slider (log scale); Step or Run; predict the next iterate by dragging a marker. Keyboard: base.
- **State.** `{ start: Vec2; eta: number; iterates: Vec2[]; prediction?: Vec2 }`.
- **Checks.** `numeric` (the divergence threshold: for $f=\frac12\mathbf x^\top A\mathbf x$, descent diverges when $\eta>2/\lambda_{\max}$; iterations to a tolerance); `choice` (why it zig-zags: elongated contours from a large ratio of eigenvalues); `point` (predicted next iterate).
- **Config.** `{ f: Expr; start: Vec2; movableStart: boolean; eta: number; etaRange: [number, number]; method: 'gd' | 'momentum' | 'newton' | 'sgd'; steps: number; showLoss: boolean; noise?: { seed: number; scale: number } }`.
- **Visual.** Contours in ink, 1px; the iterate path in s2 with dots; the start handle in `--manip`; the loss plot on a log $y$-axis in ink. Answer objects: the prediction marker or the field.
- **Motion.** Run reveals iterates at 8 per second (a demonstration started by the learner).
- **Reduced motion.** Run shows all iterates at once.
- **Accessibility.** Table of $k$, $\mathbf x_k$ and $f(\mathbf x_k)$.
- **Tutor hooks.** Ids: `handle:start`, `slider:eta`, `iterate:<k>`, `path`, `plot:loss`, `marker:predict`.
- **Performance.** Contours computed once; up to 500 iterates per run.
- **Artifact and web.** No difference.
- **Generators.** Rotated quadratic bowls with eigenvalue ratios 1, 4 and 25; the Rosenbrock function at difficulty 5.

### 5.22 `quadratic-form`: Quadratic forms and definiteness

Composite. P0, wave C. Shared by 1.3 and 1.4. Uses: `matrix`, `slider`, `plot-3d`, `plot-2d`, `drag-point`, `marks`, `live-formula`, `choice`.

- **Purpose.** $q(\mathbf x)=\mathbf x^\top A\mathbf x$ for symmetric $A$: bowl, saddle or ridge; eigenvectors as principal axes; the tests for positive definiteness; the second-derivative test through the Hessian; covariance ellipses; Cholesky; which correlation matrices are possible.
- **Serves.** 1.3.6 L7; 1.4.6 L7; 1.4.7 L1 to L3; 1.5 (bivariate normal), cross-cluster; 1.6 (covariance), cross-cluster; 3.2.2 L5.
- **Interactions.** Pointer: sliders for $a$, $b$, $c$ in $\begin{bmatrix}a&b\\b&c\end{bmatrix}$ (or edit the matrix cells; the two off-diagonal cells are linked); the surface morphs between bowl and saddle; drag a point on the level-set plot to read $q(\mathbf x)$ and the gradient $2A\mathbf x$. A tests panel lights each test (pivots, eigenvalues, leading minors); on Check items it stays hidden until graded. Correlation mode: sliders for $\rho_{12}$, $\rho_{13}$, $\rho_{23}$; the feasible region (the elliptope) in 3D with the current point; the smallest eigenvalue read out. Keyboard: base.
- **State.** `{ a: number; b: number; c: number }` or `{ r12: number; r13: number; r23: number }`, plus `{ point: Vec2 }`.
- **Checks.** `choice` (positive definite, semidefinite, indefinite, negative definite; minimum, maximum or saddle); `set` (which tests pass); `numeric` (eigenvalues; the bounds for $\rho_{13}$, which are $\rho_{12}\rho_{23}\pm\sqrt{(1-\rho_{12}^2)(1-\rho_{23}^2)}$, so $[0.4585, 0.9815]$ for $\rho_{12}=0.9$, $\rho_{23}=0.8$); `matrix` (the Cholesky factor, exact for integer cases).
- **Config.** `{ A: [[Entry, Entry], [Entry, Entry]]; editable: Array<'a' | 'b' | 'c'>; ranges: Partial<Record<'a' | 'b' | 'c', [number, number]>>; views: Array<'surface' | 'levels' | 'tests' | 'eigen'>; mode: 'quadratic' | 'hessian' | 'covariance' | 'correlation-3'; f?: Expr; at?: Vec2 }` (Hessian mode takes $f$'s Hessian at a point).
- **Visual.** Surface with the sequential ramp; level curves in ink; eigen-axes in s2 and s3 labelled with $\lambda$; the negative region of an indefinite form in the focus wash during show-why; test rows with check or cross icons after grading. Answer objects: the answer fields and, in correlation mode, the learner's bound handles.
- **Motion.** The sliders are direct manipulation, so the surface follows on every frame. Show-why for "positive diagonal entries mean positive definite": $b$ tweens up until the bowl becomes a saddle, and the direction where $q<0$ highlights.
- **Reduced motion.** Base.
- **Accessibility.** "q = 2x² + 6xy + 2y²: eigenvalues 5 and −1, indefinite (a saddle). Along (1, −1)/√2, q is negative."
- **Tutor hooks.** Ids: `slider:a`, `slider:b`, `slider:c`, `slider:r12`, `slider:r13`, `slider:r23`, `cell:<i>,<j>`, `axis:1`, `axis:2`, `test:pivots`, `test:eigenvalues`, `test:minors`, `region:negative`, `elliptope`.
- **Performance.** Closed-form 2 by 2 eigenvalues; surface 32 by 32; the elliptope boundary ($1+2xyz-x^2-y^2-z^2=0$) precomputed as a 48 by 48 parametric mesh.
- **Artifact and web.** No difference.
- **Generators.** Integer symmetric matrices of each definiteness; Hessians of polynomials at their critical points; correlation triples with tidy bounds.

### 5.23 `dependency-graph`: Dependency tree

Composite. P0, wave C (backpropagation mode P2). Uses: `marks` (nodes and edges), `token-tray`, `region-select` (each path is a selectable region), `live-formula`, `expression-input`, `stepper`.

- **Purpose.** The multivariable chain rule as a sum over paths of products of partial derivatives; computational graphs; backpropagation as accumulating derivatives in reverse.
- **Serves.** 1.3.6 L4; 1.3.2 L6 (one-variable chains); 2.1 (backpropagation), cross-cluster.
- **Interactions.** Pointer: drag variable tokens into node slots and partial-derivative tokens onto edges; tap a path from the output to an input to add its product to the formula, which assembles from the learner's taps. Numeric mode: values on nodes, local derivatives on edges; the stepper runs the forward pass and then the backward pass (P2). Keyboard: Tab through nodes and edges; Space selects a path at its leaf.
- **State.** `{ placements: Record<Id, Id>; paths: Id[]; step: number }`.
- **Checks.** `set` (edge labels; the chosen paths equal all paths); `expression` (the final formula); `numeric` (the derivative at a point).
- **Config.** `{ nodes: Array<{ id: Id; label: string; layer: number }>; edges: Array<{ from: Id; to: Id; partial: string }>; build: 'given' | 'place-nodes' | 'label-edges'; target: { from: Id; to: Id }; values?: Record<Id, number>; mode: 'chain-rule' | 'backprop' }`.
- **Visual.** Nodes as lipped chips layered from output (top) to inputs (bottom), as in Stewart's tree diagrams; edges 1.5px ink; selected paths 3px `--manip`. Answer objects: placed tokens and selected paths.
- **Motion.** Path selection is immediate; the backward pass moves values along edges (320ms per layer).
- **Reduced motion.** Base.
- **Accessibility.** The tree as a nested list of paths.
- **Tutor hooks.** Ids: `node:<id>`, `edge:<from>-<to>`, `path:<leaf>`, `term:<path>`.
- **Performance.** Trivial (at most 20 nodes).
- **Artifact and web.** No difference.
- **Generators.** $z=f(x,y)$ with $x=g(s,t)$, $y=h(s,t)$ from seeded forms; numeric values at tidy points.

### 5.24 `region-bounds`: Integration region and bounds

Composite. P0, wave C. Uses: `plot-2d`, `marks`, `drag-point`, `choice`, `expression-input` (four bounds), `live-formula`; `plot-3d` for triple integrals.

- **Purpose.** Set up double and triple integrals: describe a region by bounds, with vertical or horizontal strips; swap the order of integration; polar regions; probability over regions.
- **Serves.** 1.3.7 L3, L4, L6, L7; 1.5 (for example $P(X+Y<1)$, joint densities), cross-cluster.
- **Interactions.** Pointer: drag the representative strip across the region; its ends light up the boundary curves they touch; toggle the strip's orientation; type the bounds into the integral template. The widget draws the region the learner's bounds describe as a ghost over the true region. Keyboard: the bound fields are native; the strip is a handle.
- **State.** `{ orientation: 'vertical' | 'horizontal'; strip: number; bounds: { outer: [string, string]; inner: [string, string]; z?: [string, string] } }`.
- **Checks.** `predicate: bounds-describe-region` (the outer bounds are constants and the region they describe matches the target: symmetric difference below 0.5% of the area on a 200 by 200 raster); `expression` per bound; `numeric` (the integral's value); `choice` (which order is easier).
- **Config.** `{ boundaries: Array<{ id: Id; expr: Expr; kind: 'y=f(x)' | 'x=g(y)' | 'r=f(theta)' }>; target: RegionDef; coords: 'cartesian' | 'polar'; askOrder?: 'dy dx' | 'dx dy' | 'either'; integrand?: Expr; density?: boolean; dims?: 2 | 3; zBounds?: [Expr, Expr] }`.
- **Visual.** Region in s3 at 20% with ink boundaries labelled ($y=x^2$); the strip in `--manip-wash` with `--manip` edges; the learner's described region as a ghost. Answer objects: the bound fields and the learner's ghost region, which grading recolours.
- **Motion.** Direct. Show-why: the mismatched area between the learner's region and the true one flashes twice.
- **Reduced motion.** Base.
- **Accessibility.** Boundaries and their intersection points described; bound fields fully keyboard-driven.
- **Tutor hooks.** Ids: `boundary:<id>`, `strip`, `bound:outer-lo`, `bound:outer-hi`, `bound:inner-lo`, `bound:inner-hi`, `bound:z-lo`, `bound:z-hi`, `mismatch`.
- **Performance.** Rasterised comparison only on Check, under 10 ms.
- **Artifact and web.** No difference.
- **Generators.** Regions bounded by lines and parabolas with integer intersections; triangles; polar sectors and annuli; order-swap items.

### 5.25 `volume-slicer`: Volume by columns and slices

Composite. P0, wave C. Uses: `plot-3d`, `plot-2d` (region and $A(x)$ panel), `slider`, `drag-point`, `marks`, `live-formula`, `numeric-input`.

- **Purpose.** A double integral as the volume under a surface: Riemann columns; slicing into cross-sections with area $A(x)=\int f(x,y)\,dy$; iterated integrals; polar wedges and cylindrical shells, including the Gaussian integral.
- **Serves.** 1.3.7 L1, L2, L4; 1.5 (a joint density has volume 1), cross-cluster.
- **Interactions.** Pointer: grid slider for columns, with a running volume; slice mode: drag $x_0$, see the cross-section shaded in its plane and its area plotted as a point on the $A(x)$ panel, so sweeping builds the $A(x)$ curve whose area is the volume; polar wedge mode; shell mode for $\iint e^{-(x^2+y^2)}\,dA$ (the shell at radius $r$ has volume $2\pi re^{-r^2}\,dr$, total $\pi$). Keyboard: base; 3D orbit.
- **State.** `{ n: number; x0: number; mode: Mode }`.
- **Checks.** `numeric` (volume, $A(x_0)$); `expression` ($A(x)$); `choice`.
- **Config.** `{ f: Expr; region: RegionDef; mode: 'columns' | 'slices' | 'polar-wedges' | 'shells'; n?: number; sliceAxis?: 'x' | 'y' }`.
- **Visual.** Columns in s2 at 60% with ink edges; the slice plane in `--manip-wash` (learner-controlled); the cross-section in s3; the surface translucent when columns show. Answer objects: the fields.
- **Motion.** Direct; the camera moves to a side view when slicing starts (280ms).
- **Reduced motion.** Base.
- **Accessibility.** Volume estimate and slices described; table of $A(x)$.
- **Tutor hooks.** Ids: `column:<i>,<j>`, `slice`, `area:slice`, `plot:A`, `shell:<k>`.
- **Performance.** Three visible faces per column: $n\le16$ per side on phones (768 quads), 24 on desktop.
- **Artifact and web.** No difference.
- **Generators.** Polynomial surfaces over rectangles and triangles with tidy volumes.

### 5.26 `lagrange-explorer`: Lagrange multipliers

Composite. P0, wave C (three-variable mode late in wave C). Uses: `plot-2d` (contour map with constraint, and a profile plot), `plot-3d` (three-variable mode), `drag-point` (on the constraint), `slider`, `marks`, `live-formula`, `numeric-input`, `expression-input`, `choice`.

- **Purpose.** Constrained optimisation: walk along a constraint and watch $f$; at the optimum the level curve is tangent to the constraint and $\nabla f=\lambda\nabla g$; $\lambda$ is the shadow price; portfolio weights on a simplex.
- **Serves.** 1.3.8 L1 to L5; 1.7 and 2.3 (Markowitz), cross-cluster.
- **Interactions.** Pointer: drag the point along the constraint curve; the profile panel plots $f$ against position along the curve; toggle both gradient arrows; the $c$ slider moves the constraint $g=c$ so the learner can read the change in the optimum. Simplex mode: weights on a ternary plot whose interior is shaded by portfolio variance. Three-variable mode: a level surface and a constraint plane in 3D. Keyboard: base.
- **State.** `{ point: number[]; c: number }`.
- **Checks.** `point` (the optimum on the constraint); `numeric` ($\lambda$; the change in the optimum for $\Delta c$); `expression` (the Lagrange system); `choice` (maximum or minimum among candidates).
- **Config.** `{ f: Expr; g: Expr; c: number; cRange?: [number, number]; start: number[]; show: { contours: boolean; gradients: 'never' | 'toggle' | 'after-check'; profile: boolean }; coords: 'cartesian' | 'ternary'; vars: 2 | 3 }`.
- **Visual.** Contours of $f$ in ink, 1px, labelled; the constraint in s2, 2px; the point in `--manip`; $\nabla g$ in s2 (matching its curve) and $\nabla f$ in s3. Answer objects: the point or the fields.
- **Motion.** Direct. Show-why at a non-optimal point: the two gradients highlight with the angle between them labelled, and the contour through the point is seen crossing, not touching, the constraint.
- **Reduced motion.** Base.
- **Accessibility.** "On the circle at 40°: f = 3.2. The gradients differ by 25°, so moving along the circle still changes f."
- **Tutor hooks.** Ids: `handle:point`, `curve:constraint`, `vector:gradf`, `vector:gradg`, `contour:<level>`, `plot:profile`, `slider:c`.
- **Performance.** The constraint is recomputed by marching squares only when $c$ changes (about 1 to 2 ms on a 96 by 96 grid); the point is projected onto $g=c$ by Newton steps.
- **Artifact and web.** No difference.
- **Generators.** Linear or quadratic $f$ on circles, ellipses and lines with tidy optima; three-asset variance problems with tidy weights.

---
## 6. Linear algebra composites (1.4)

### 6.1 `vector-combo`: Linear combinations and span

Composite. P0, wave A (2D, for 0.3 vectors) and wave C (3D). Uses: `plot-2d`, `plot-3d`, `drag-point` (vector tips, combination point), `slider`, `marks`, `live-formula`, `matrix`, `numeric-input`.

- **Purpose.** Vectors as arrows; linear combinations $c\mathbf v+d\mathbf w$; reaching a target; span as a line, a plane or everything; independence; $A\mathbf x$ as a combination of columns.
- **Serves.** 0.3 (vectors), cross-cluster; 1.4.1 L1, L2, L4; 1.4.3 L5.
- **Interactions.** Pointer: drag the tips of $\mathbf v$ and $\mathbf w$; set $c$ and $d$ with sliders, or drag the combination point and read the $c$ and $d$ the widget solves for live (when the vectors are dependent and the point is off their line, it shows the nearest reachable point). Span mode paints every combination (an integer lattice plus a shaded line or plane). 3D mode adds $\mathbf u$ and shows the parallelepiped's volume falling to zero as the three become coplanar. Integer game: reach $\mathbf b$ with integer weights. Keyboard: base.
- **State.** `{ vectors: Record<string, number[]>; coeffs: Record<string, number> }`.
- **Checks.** `numeric` ($c$, $d$); `point` (the combination reaches the target); `choice` (the span is a line, a plane or the whole space); `predicate: outside-span` (find a vector outside the span); `matrix` (a column vector).
- **Config.** `{ dims: 2 | 3; vectors: Array<{ id: string; at: number[]; movable: boolean; label: string }>; coeffs?: Array<{ for: string; range: [number, number]; step?: number }>; target?: number[]; mode: 'combine' | 'solve' | 'span' | 'independence' | 'columns-of-A'; lattice?: boolean; snap?: number }`.
- **Visual.** Movable vectors in `--manip` with KaTeX labels; fixed vectors in ink; scaled copies dashed in s2 and s3 forming the parallelogram; the result in ink, 2.5px; the span in s3 at 15%; the target as a ghost ring. Answer objects: the coefficient sliders, the combination point, or the learner's vector in `outside-span` items.
- **Motion.** Direct. Show-why for an unreachable target: the span line paints in and the target pulses off it.
- **Reduced motion.** Base.
- **Accessibility.** "v = (2, 1), w = (1, 3). 1.5v − 0.5w = (2.5, 0). The target (3, 4) needs c = 1, d = 1."
- **Tutor hooks.** Ids: `vec:<id>`, `handle:<id>`, `handle:combo`, `slider:c`, `slider:d`, `span`, `target`, `volume`.
- **Performance.** Trivial in 2D; 3D through `plot-3d`.
- **Artifact and web.** No difference.
- **Generators.** Integer vectors with integer solutions; dependent pairs; coplanar triples in 3D.

### 6.2 `projection-lab`: Dot products and projections

Composite. P0, wave A (2D dot product, for 0.3) and wave C. Uses: `plot-2d`, `plot-3d`, `drag-point`, `marks`, `live-formula`, `matrix`, `numeric-input`.

- **Purpose.** Lengths, dot products and angles; the projection of $\mathbf b$ onto a line and onto a plane; the error vector perpendicular to what it was projected onto; projection matrices; the cross product in 3D.
- **Serves.** 0.3 (scalar product), cross-cluster; 1.4.1 L3; 1.4.4 L1 to L3, L5; 1.3.6 (normal vectors to planes); 1.6 (regression geometry), cross-cluster.
- **Interactions.** Pointer: drag $\mathbf a$ and $\mathbf b$; the projection updates. Predict mode: drag a marker along the line through $\mathbf a$ to where $\mathbf p$ should land. Dot mode shades the half-planes where $\mathbf a\cdot\mathbf b$ is positive or negative. Plane mode in 3D: $\mathbf b$ above the plane of two columns, with $\mathbf p$ and $\mathbf e$. Cross mode: $\mathbf a\times\mathbf b$ with the parallelogram whose area is its length. Keyboard: base (3D handles use the height field).
- **State.** `{ a: number[]; b: number[]; prediction?: number[] }`.
- **Checks.** `point` (the projection); `numeric` ($\mathbf a\cdot\mathbf b$, $\lvert\mathbf p\rvert$, $\cos\theta$); `matrix` ($P=\frac{\mathbf a\mathbf a^\top}{\mathbf a^\top\mathbf a}$ or $A(A^\top A)^{-1}A^\top$); `choice` (sign of the dot product).
- **Config.** `{ dims: 2 | 3; a?: number[]; A?: number[][]; b: number[]; movable: Array<'a' | 'b'>; mode: 'dot' | 'onto-line' | 'onto-plane' | 'predict' | 'cross'; showMatrix?: boolean }`.
- **Visual.** $\mathbf a$ and $\mathbf b$ in `--manip`; $\mathbf p$ in s2, 2.5px; $\mathbf e$ dashed in ink with a right-angle marker; the plane in s3 at 15%. Answer objects: the prediction marker and the fields.
- **Motion.** Direct. Show-why when the learner drops $\mathbf b$ straight down instead of perpendicular to $\mathbf a$: both drops drawn, with the angle of the wrong one marked.
- **Reduced motion.** Base.
- **Accessibility.** "a = (3, 1), b = (2, 2). a · b = 8. p = 0.8a = (2.4, 0.8); e = (−0.4, 1.2), at 90° to a."
- **Tutor hooks.** Ids: `vec:a`, `vec:b`, `vec:p`, `vec:e`, `angle:right`, `plane`, `marker:predict`, `region:positive`, `region:negative`, `vec:cross`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Integer vectors with rational projection coefficients; planes from integer columns.

### 6.3 `row-column-picture`: Row and column pictures

Composite. P0, wave A (2D, for 0.2 simultaneous equations) and wave C (3D). Uses: `plot-2d` or `plot-3d` (two, side by side), `matrix`, `drag-point`, `slider`, `marks`, `live-formula`.

- **Purpose.** $A\mathbf x=\mathbf b$ two ways: rows as lines (or planes) meeting at the solution; columns combining to reach $\mathbf b$. Singular systems: parallel lines, coincident lines, planes without a common point.
- **Serves.** 0.2 (simultaneous equations), cross-cluster; 1.4.2 L1, L3; 1.4.3 L2.
- **Interactions.** Pointer: edit $A$ and $\mathbf b$ in the matrix; drag $\mathbf b$ in the column picture and watch the row-picture lines shift in parallel (only their intercepts change); weight sliders in the column picture. Keyboard: matrix cells and handles.
- **State.** `{ A: Entry[][]; b: Entry[]; weights?: number[] }`.
- **Checks.** `matrix` or `numeric` (the solution); `choice` (no solution, one, infinitely many); `point` (the intersection).
- **Config.** `{ A: Entry[][]; b: Entry[]; editable: { A?: boolean | Array<[number, number]>; b?: boolean }; views: Array<'row' | 'column'>; dims: 2 | 3 }`.
- **Visual.** Row lines (or planes) in s2, s3 and s4 with equation labels; the intersection as an ink dot (or line); columns as ink arrows with dashed scaled copies; $\mathbf b$ as a `--manip` handle in the column picture. Answer objects: the fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** "Row picture: 2x − y = 0 and −x + 2y = 3 meet at (1, 2). Column picture: 1·(2, −1) + 2·(−1, 2) = (0, 3)."
- **Tutor hooks.** Ids: `line:<i>`, `plane:<i>`, `point:solution`, `col:<j>`, `vec:b`, `cell:<i>,<j>`, `slider:x<j>`.
- **Performance.** Trivial; three translucent planes in 3D.
- **Artifact and web.** No difference.
- **Generators.** Integer systems with integer solutions; singular systems (parallel and coincident).

### 6.4 `elimination-lab`: Elimination lab

Composite. P0, wave C. Uses: `matrix` (augmented, row gestures), `numeric-input`, `stepper` (history), `marks`, `live-formula`; optionally a linked `row-column-picture`.

- **Purpose.** Gaussian elimination by hand in exact arithmetic: pivots, multipliers, row operations and exchanges; reaching $U$; back substitution; Gauss-Jordan to RREF and the inverse; elimination matrices assembling $L$ in $A=LU$ and $P$ in $PA=LU$.
- **Serves.** 1.4.2 L2, L3, L5, L6; 1.4.3 L3, L4; 1.4.5 L2 (the determinant as the product of pivots).
- **Interactions.** An operation builder: choose the target row, the source row and the multiplier $\ell$, then Apply ($R_i \leftarrow R_i-\ell R_j$); swap and scale operations; Undo. Gestures are shortcuts: drag a row onto another to swap. In Explore screens an "auto $\ell$" button fills the multiplier; in Problem screens the learner supplies it. LU mode: each operation writes its $\ell$ into a growing $L$ beside the matrix. Back-substitution mode: solve from the bottom row with numeric fields. Keyboard: the builder is a native form, fully keyboard-driven.
- **State.** `{ M: Rational[][]; history: RowOp[]; L?: Rational[][]; P?: number[] }`.
- **Checks.** `matrix` (`echelon-row-equivalent`, `rref`, or exact $L$, $U$, $P$, $A^{-1}$); `numeric` (a multiplier; the determinant from pivots); `set` (pivot positions).
- **Config.** `{ A: Entry[][]; b?: Entry[] | Entry[][]; goal: 'U' | 'RREF' | 'LU' | 'PA=LU' | 'inverse' | 'solve'; allowed: Array<'add-multiple' | 'swap' | 'scale'>; autoMultiplier?: boolean; showRowPicture?: boolean; maxOps?: number }`.
- **Visual.** As `matrix`; pivots circled; entries the learner has just zeroed take a brief focus wash (state feedback, not a verdict); the history list in caption type with KaTeX operations; $L$ cells filling in as ghosts. Answer objects: the final matrix (and $L$, $P$ where asked).
- **Motion.** Changed entries cross-fade over 150ms; swaps slide over 200ms.
- **Reduced motion.** Base.
- **Accessibility.** Each operation announced with its resulting row; the matrix is a grid.
- **Tutor hooks.** Describes the current matrix, the history and the next pivot position (not the next move). Ids: `row:<i>`, `cell:<i>,<j>`, `pivot:<k>`, `op:<n>`, `L:<i>,<j>`, `builder:target`, `builder:source`, `builder:multiplier`.
- **Performance.** BigInt fractions on matrices up to 6 by 7; trivial.
- **Artifact and web.** No difference.
- **Generators.** $A=LU$ built from a unit lower-triangular $L$ with small integer multipliers and an upper-triangular $U$ with nonzero integer pivots; versions where a zero pivot forces an exchange; rank-deficient matrices; RREF with free columns; unimodular matrices (determinant $\pm1$) for integer inverses.

### 6.5 `matrix-multiply`: Matrix multiplication four ways

Composite. P0, wave C. Uses: `matrix` (three), `marks`, `choice`, `numeric-input`, `stepper`, `token-tray`.

- **Purpose.** $AB$ by entries (row times column), by columns (combinations of $A$'s columns), by rows, and as a sum of outer products; shape rules; non-commutativity; permutation and elimination matrices acting on rows; transpose rules.
- **Serves.** 1.4.1 L4; 1.4.2 L4, L5, L7; 1.4.7 L5 (outer products behind the SVD).
- **Interactions.** Pointer: tap a cell of $C$ to see its row and column highlighted with the dot product written out; switch view; fill $C$'s cells; outer-product mode steps in layers, column $k$ of $A$ times row $k$ of $B$. Shape puzzle: drag shapes so the product is defined. Keyboard: grid navigation; stepper keys.
- **State.** `{ C: Entry[][]; view: View; layer: number }`.
- **Checks.** `matrix` ($C$); `numeric` per cell; `choice` (does $AB=BA$?); `set` (compatible shapes).
- **Config.** `{ A: Entry[][]; B: Entry[][]; view: 'entry' | 'column' | 'row' | 'outer'; fill?: 'none' | 'cells' | 'all'; shapes?: Array<[number, number]> }`.
- **Visual.** $A$'s row band in an s2 wash, $B$'s column band in an s3 wash, $C$'s cell ringed in ink; learner cells with a `--manip` underline. Answer objects: the learner's cells.
- **Motion.** Highlights are immediate; layers add over 320ms in outer-product mode.
- **Reduced motion.** Base.
- **Accessibility.** "C row 2, column 1 = row 2 of A dot column 1 of B = 3·1 + 0·2 = 3."
- **Tutor hooks.** Ids: `A:row:<i>`, `B:col:<j>`, `C:cell:<i>,<j>`, `layer:<k>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Small integer matrices; permutation and elimination matrices; non-commuting pairs.

### 6.6 `transform-grid`: Linear (and nonlinear) maps of the plane

Composite. P0, wave C. Shared by 1.3.7 and 1.4. Uses: `plot-2d`, `plot-3d`, `drag-point` (column tips; a probe point), `slider` (morph $t$), `matrix`, `marks`, `live-formula`.

- **Purpose.** A matrix as a transformation: the images of $\mathbf e_1$ and $\mathbf e_2$ are its columns; composition is multiplication; the inverse undoes; the determinant is the signed area factor; a singular matrix squashes the plane onto a line. Nonlinear maps are locally linear, with the Jacobian as the local matrix, which explains change of variables.
- **Serves.** 1.4.2 L8; 1.4.3 L2; 1.4.5 L1; 1.4.6 L1 (eigen-directions stay on their lines); 1.3.7 L5.
- **Interactions.** Pointer: drag the column tips; the morph slider (0 to 1) deforms the grid from the identity to $A$. Compose mode: apply $B$, then $A$, and compare with $AB$. Inverse mode: build the matrix that returns the F to its start. Nonlinear mode: a map $(u,v)\mapsto(x,y)$ (polar to Cartesian by default), a probe point carrying a tiny square, its image parallelogram, an inset showing local linearity, and $\lvert\det J\rvert$ read out. 3D mode: the unit cube to a parallelepiped. Keyboard: base; matrix cells.
- **State.** `{ A: Entry[][]; t: number; B?: Entry[][]; probe?: Vec2 }`.
- **Checks.** `matrix` (the $A$ that produces the target image; an inverse); `numeric` ($\det A$; the Jacobian determinant at the probe); `choice` (orientation reversed?); `point` (where a given vector lands).
- **Config.** `{ dims: 2 | 3; A: Entry[][]; movableColumns: boolean; target?: Entry[][]; mode: 'transform' | 'compose' | 'inverse' | 'determinant' | 'nonlinear'; B?: Entry[][]; map?: { x: Expr; y: Expr; domain: [[number, number], [number, number]] }; glyph?: 'F' | 'square' | 'circle' | 'none'; snap?: number }`.
- **Visual.** The original grid in faint `--grid`; the transformed grid in ink at 40%; the unit square's image in s3 at 25% with an asymmetric F glyph so orientation shows; column vectors in `--manip` labelled $A\mathbf e_1$, $A\mathbf e_2$; the target F as a ghost. Answer objects: the column handles or the matrix cells.
- **Motion.** Column drags and the morph slider are direct. Play runs the morph over 800ms (ease-morph). Show-why for a wrong matrix: the learner's F and the target F morph side by side.
- **Reduced motion.** Play becomes a before-and-after pair.
- **Accessibility.** "A = [[2, 1], [0, 1]]: e1 goes to (2, 0), e2 to (1, 1). Areas double; orientation is kept."
- **Tutor hooks.** Ids: `handle:col1`, `handle:col2`, `handle:col3`, `glyph`, `square`, `grid`, `slider:t`, `probe`, `inset`, `cell:<i>,<j>`.
- **Performance.** At most 21 grid lines each way as two SVG paths; nonlinear grids as 21 by 21 polylines with 32 samples each; under 1 ms.
- **Artifact and web.** No difference.
- **Generators.** Integer 2 by 2 matrices with target glyphs; rotations, reflections, shears and projections; unimodular matrices for inverse puzzles.

### 6.7 `subspace-tester`: Subspace tester

Composite. P0, wave C. Uses: `plot-2d`, `plot-3d`, `drag-point` (two vectors constrained to the set), `slider` (scalar), `marks`, `choice`.

- **Purpose.** What makes a subspace: it contains $\mathbf 0$ and is closed under addition and scalar multiplication. Building a counterexample.
- **Serves.** 1.4.3 L1, L5.
- **Interactions.** Pointer: drag $\mathbf u$ and $\mathbf w$ within the set; their sum and $c\,\mathbf u$ are drawn; in Explore screens, results outside the set highlight live; in Problem screens the learner submits a counterexample pair or claims the set is closed. Keyboard: base.
- **State.** `{ u: number[]; w: number[]; c: number }`.
- **Checks.** `choice` (subspace or not; which rule fails); `predicate: closure-counterexample`.
- **Config.** `{ dims: 2 | 3; set: { kind: 'line' | 'plane' | 'quadrant' | 'union-of-lines' | 'half-plane' | 'curve' | 'point'; def: Expr | number[][] }; allowCounterexample: boolean }`.
- **Visual.** The set in s3; $\mathbf u$ and $\mathbf w$ in `--manip`; $\mathbf u+\mathbf w$ in s2; $c\,\mathbf u$ dashed in s2. Answer objects: the pair, or the choice.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** Membership tests described numerically ("u + w = (−1, 2) is not in the first quadrant").
- **Tutor hooks.** Ids: `handle:u`, `handle:w`, `vec:sum`, `vec:scaled`, `slider:c`, `set`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Sets from a catalogue with seeded parameters.

### 6.8 `four-subspaces`: The four fundamental subspaces

Composite. P0, wave C. Uses: `marks` (the big-picture diagram), `token-tray`, `matrix`, `numeric-input`, `plot-3d`, `drag-point`, `live-formula`.

- **Purpose.** Strang's big picture: row space and nullspace in $\mathbb R^n$, column space and left nullspace in $\mathbb R^m$, with dimensions $r$, $n-r$, $r$, $m-r$; orthogonal complements; $A$ maps the row space one-to-one onto the column space and the nullspace to $\mathbf 0$.
- **Serves.** 1.4.3 L6; 1.4.4 L1; 1.4.7 L4 and L6 (SVD bases, the pseudoinverse).
- **Interactions.** Pointer: fill the four dimensions; drag basis-vector tokens into the four boxes. Geometric mode (3 by 3, rank 1 or 2): drag $\mathbf x$ in $\mathbb R^3$, see its row-space and nullspace parts, and watch only the row-space part decide $A\mathbf x$. Keyboard: token-tray and fields.
- **State.** `{ dims: Record<Box, number>; placements: Record<TokenId, Box>; x?: number[] }`.
- **Checks.** `numeric` (dimensions); `set` (tokens to boxes); `choice`.
- **Config.** `{ A: Entry[][]; tokens: Array<{ id: Id; vector: Entry[] }>; ask: Array<'dims' | 'sort' | 'geometric'> }`.
- **Visual.** Two rounded rectangles ($\mathbb R^n$ left, $\mathbb R^m$ right), each split into two boxes with a right-angle marker; arrows from row space to column space and from nullspace to $\mathbf 0$. Answer objects: the placed tokens and dimension fields.
- **Motion.** Token placement as `token-tray`.
- **Reduced motion.** Base.
- **Accessibility.** The diagram described as four labelled lists.
- **Tutor hooks.** Ids: `box:row`, `box:null`, `box:col`, `box:leftnull`, `token:<id>`, `dim:<box>`, `handle:x`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Integer matrices of chosen rank built as $A=CR$ (an $m\times r$ times an $r\times n$ integer matrix); vectors from each subspace computed exactly, plus distractors.

### 6.9 `solution-set`: Complete solution of $A\mathbf x=\mathbf b$

Composite. P0, wave C. Uses: `matrix`, `slider` (free variables), `plot-3d`, `marks`, `expression-input`, `choice`.

- **Purpose.** The complete solution $\mathbf x=\mathbf x_p+\mathbf x_n$: free variables as parameters; a point, line or plane offset from the origin, parallel to the nullspace; the rank cases.
- **Serves.** 1.4.3 L3, L4.
- **Interactions.** Pointer: move the free-variable sliders and watch the solution point travel along its line or plane, with the nullspace drawn through the origin; when $\mathbf b$ is editable, make the system inconsistent and see the contradictory row "0 = 1" highlighted. Keyboard: base.
- **State.** `{ free: Record<string, number>; b: Entry[] }`.
- **Checks.** `matrix` (special solutions); `predicate: same-affine-set` (the learner's parametric form describes the same set); `numeric` (rank); `choice` (the rank case and the number of solutions).
- **Config.** `{ A: Entry[][]; b: Entry[]; editableB?: boolean; showRref?: boolean; view3d?: boolean }`.
- **Visual.** The solution set in s2 (a 2.5px line or a 20% plane); the nullspace in s3 through the origin; the current point in `--manip`. Answer objects: the fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** The set read as a parametric equation.
- **Tutor hooks.** Ids: `slider:<free>`, `set:solution`, `set:null`, `pivot:<k>`, `row:<i>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Integer matrices of rank 1 to 3 in 3 or 4 unknowns with integer particular and special solutions.

### 6.10 `basis-change`: Change of basis

Composite. P0, wave C. Uses: `plot-2d` (two grids), `drag-point`, `matrix`, `marks`, `numeric-input`.

- **Purpose.** Coordinates relative to a basis; change-of-basis matrices; the same transformation written in another basis (similar matrices); diagonalisation as switching to the eigenbasis.
- **Serves.** 1.4.3 L7; 1.4.6 L4; 1.4.7 L4.
- **Interactions.** Pointer: drag the basis vectors and the point $\mathbf x$; read its coordinates on both grids. Transformation mode: $T$ acts on the plane; on the eigenbasis grid it is a pure stretch along each grid direction. Keyboard: base.
- **State.** `{ basis: [number[], number[]]; x: number[] }`.
- **Checks.** `numeric` (coordinates in the new basis); `matrix` ($P$, $P^{-1}$, or the matrix of $T$ in the new basis); `choice`.
- **Config.** `{ basis: [number[], number[]]; movableBasis: boolean; x: number[]; T?: Entry[][]; mode: 'coordinates' | 'matrix-of-T' | 'diagonalise' }`.
- **Visual.** The standard grid in `--grid`; the basis grid in s2 at 50%; $\mathbf x$ in `--manip`; coordinate labels in both systems. Answer objects: the fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** Both coordinate pairs described.
- **Tutor hooks.** Ids: `handle:b1`, `handle:b2`, `handle:x`, `grid:standard`, `grid:basis`, `cell:<i>,<j>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Integer bases with determinant $\pm1$ or small; diagonalisable $T$ with integer eigenvectors.

### 6.11 `least-squares-fit`: Least squares

Composite. P0, wave C. Shared by 1.3.6 L8, 1.4.4 and 1.6. Uses: `plot-2d` (data and the error map), `drag-point`, `marks`, `value-table`, `matrix`, `live-formula`, `sim-runner` (seeded data), `code-cell`; links to `projection-lab` for the $\mathbb R^3$ picture.

- **Purpose.** Fitting a line or polynomial by least squares: residuals and the sum of squared errors; the error bowl over (intercept, slope); the normal equations $A^\top A\hat{\mathbf x}=A^\top\mathbf b$; the picture in $\mathbb R^m$; sensitivity to an outlier; a CAPM beta.
- **Serves.** 1.4.4 L4, L5, L7; 1.3.6 L8; 1.6 (linear regression), cross-cluster; 2.1 (linear models), cross-cluster.
- **Interactions.** Pointer: drag the learner's line by two handles to make the squares as small as possible (live total and squares area); drag data points (when movable) to see the fit respond after the reveal; outlier mode drags one point far away; a degree switch (1, 2, 3) shows the design-matrix columns $1, t, t^2$. With exactly three points, a linked $\mathbb R^3$ view shows $\mathbf b$, the column-space plane, $\mathbf p$ and $\mathbf e$. Keyboard: base.
- **State.** `{ points: Vec2[]; line: { C: number; D: number }; degree: 1 | 2 | 3 }`.
- **Checks.** `numeric` ($C$ and $D$ against the least-squares values; the minimum sum of squares); `point` (the learner's $(C, D)$ on the error map); `matrix` ($A^\top A$, $A^\top\mathbf b$); `choice` (effect of the outlier); `code` (NumPy implementation, compared with `allclose`).
- **Config.** `{ points: Vec2[] | { generate: { n: number; slope: number; intercept: number; noise: number; seed: number } }; movablePoints: boolean; degree: 1 | 2 | 3; line?: { C: number; D: number }; show: { residuals: boolean; squares: boolean; errorMap: boolean; matrices: boolean; r3?: boolean }; preset?: 'capm' }`.
- **Visual.** Data as ink dots; the learner's line in `--manip` with two handles; residuals in s2; squares on the residuals in s2 at 15%; the least-squares line as a ghost after Check. The error map shows ellipses in ink, the learner's point in `--manip`, the optimum after Check. Answer objects: the learner's line and its point on the error map.
- **Motion.** Direct. Show-why: the learner's line moves to the least-squares line over 800ms while the squares shrink and the total falls.
- **Reduced motion.** Before and after.
- **Accessibility.** Table of data, fitted values and residuals; "Your line y = 1.2 + 0.8x has a total of 4.31; the smallest possible is 3.95."
- **Tutor hooks.** Ids: `handle:line-1`, `handle:line-2`, `point:<i>`, `residual:<i>`, `square:<i>`, `map:error`, `point:learner-cd`, `point:optimum`, `cell:<i>,<j>`.
- **Performance.** The error map is a quadratic in $(C, D)$, so its level sets are drawn as exact ellipses from a 2 by 2 matrix, with no contouring.
- **Artifact and web.** The `code-cell` exit drill runs Pyodide on the web; in the Artifact it runs MicroPython with ulab if the probe passes, otherwise it links out (section 3.18).
- **Generators.** Data whose least-squares coefficients are round numbers by construction: choose $C$ and $D$, draw a seeded residual vector, project out the column space of $A$, scale it to the stated noise, and add it. CAPM returns with a seeded beta.

### 6.12 `gram-schmidt`: Gram-Schmidt

Composite. P0, wave C. Uses: `plot-2d`, `plot-3d`, `stepper` (predict mode), `drag-point`, `marks`, `matrix`, `live-formula`.

- **Purpose.** Turn a basis into an orthonormal basis step by step; assemble $A=QR$.
- **Serves.** 1.4.4 L6.
- **Interactions.** Stepper: normalise $\mathbf a$; project $\mathbf b$ onto $\mathbf q_1$ and subtract (the learner first drags where the result will point); repeat in 3D for $\mathbf c$. $Q$ and $R$ fill in beside the picture. Keyboard: stepper keys and handles.
- **State.** `{ step: number; predictions: Record<number, number[]> }`.
- **Checks.** `point` (the predicted orthogonal vector, by direction); `matrix` ($Q$ with `orthonormal-columns`; $R$ within tolerance); `numeric` ($r_{ij}$).
- **Config.** `{ dims: 2 | 3; vectors: number[][]; movable: boolean; predict: boolean; showQR: boolean }`.
- **Visual.** Inputs in ink; projections being removed dashed in s2; outputs $\mathbf q_k$ in s3, 2.5px, with right-angle markers. Answer objects: the prediction handles and the fields.
- **Motion.** Each subtraction shrinks the projection away over 600ms (a demonstration).
- **Reduced motion.** Before and after per step.
- **Accessibility.** Each step described numerically.
- **Tutor hooks.** Ids: `vec:a`, `vec:b`, `vec:c`, `proj:<k>`, `q:<k>`, `step:<k>`, `R:<i>,<j>`, `handle:predict`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Integer vectors chosen so the norms are whole numbers (Pythagorean triples and quadruples).

### 6.13 `determinant-lab`: Determinant lab

Composite. P0, wave C. Uses: `plot-2d`, `plot-3d`, `drag-point`, `matrix` (bar brackets), `marks`, `stepper`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** The determinant as signed area or volume; its three defining properties seen through row operations (a shear keeps the area, a swap flips the sign, scaling a row scales the area); $\det(AB)=\det A\det B$; cofactor expansion; Cramer's rule; the inverse formula.
- **Serves.** 1.4.5 L1 to L3; 1.3.7 L5.
- **Interactions.** Pointer: drag the parallelogram's edge vectors; apply shear, swap or scale with buttons and watch the area; cofactor mode steps through an expansion (highlight a row, cross out to show each minor, apply the sign pattern); Cramer mode replaces a column with $\mathbf b$ and compares areas. Keyboard: base; stepper keys.
- **State.** `{ A: Entry[][]; step: number }`.
- **Checks.** `numeric` (the determinant; cofactors); `choice` (the effect of an operation); `predicate` where a construction is asked for (a matrix with a given determinant).
- **Config.** `{ dims: 2 | 3; A: Entry[][]; movable: boolean; mode: 'area' | 'properties' | 'cofactor' | 'cramer' | 'product' }`.
- **Visual.** Parallelogram in s3 at 25% with the F glyph for orientation and a signed label; minors shown by crossing out a row and column in `--bg-sunken`; a checkerboard of signs. Answer objects: the fields, or the edge handles in construction items.
- **Motion.** Each shear slides the top edge along itself over 480ms, keeping base and height, so equal area is visible.
- **Reduced motion.** Before and after.
- **Accessibility.** Area and sign described; expansions read as sums.
- **Tutor hooks.** Ids: `shape`, `handle:col1`, `handle:col2`, `handle:col3`, `cell:<i>,<j>`, `minor:<i>,<j>`, `op:<k>`, `step:<k>`.
- **Performance.** Trivial.
- **Artifact and web.** No difference.
- **Generators.** Integer matrices with small determinants; 3 by 3 matrices with a row or column rich in zeros, so choosing the expansion line matters.

### 6.14 `eigen-finder`: Eigenvector finder

Composite. P0, wave C. Uses: `plot-2d` (circle and the characteristic polynomial), `drag-point` (on a circle), `matrix`, `slider` ($\lambda$), `marks` (vectors, ellipse), `live-formula`, `numeric-input`, `choice`.

- **Purpose.** Eigenvectors as directions that do not turn; eigenvalues as stretch factors; finding them through $\det(A-\lambda I)=0$; trace and determinant; complex eigenvalues (a rotation leaves no real direction); repeated and defective cases; the symmetric case.
- **Serves.** 1.4.6 L1 to L3; 1.4.7 L4; 1.5 (stationary vectors of Markov matrices), cross-cluster.
- **Interactions.** Pointer: drag $\mathbf x$ round the unit circle; $A\mathbf x$ is drawn from the origin and the ellipse it traces builds up; in Explore screens the angle between $\mathbf x$ and $A\mathbf x$ reads out live; "Mark it" pins a found direction. Lambda-shift mode: slide $\lambda$ and watch $(A-\lambda I)$ act on the circle; at an eigenvalue the image collapses to a segment while the dot on the characteristic-polynomial plot crosses zero. Keyboard: base (the handle steps in degrees).
- **State.** `{ theta: number; pinned: number[]; lambda: number }`.
- **Checks.** `point` with metric `angle-mod-pi` (an eigen-direction within $\pm2^\circ$); `predicate: is-eigenvector` (for typed vectors); `numeric` ($\lambda$ values; trace and determinant relations); `choice` (number of real eigen-directions); `expression` (the characteristic polynomial).
- **Config.** `{ A: Entry[][]; editable?: boolean; mode: 'find-directions' | 'lambda-shift' | 'trace-det' | 'classify'; showEllipse?: boolean; showAngle: 'live' | 'after-check' }`.
- **Visual.** Unit circle in `--line`; $\mathbf x$ in `--manip`; $A\mathbf x$ in s2; the traced ellipse in s2 at 40%; pinned eigen-lines dashed in ink with $\lambda$ labels; the polynomial in ink with its $\lambda$ dot in `--manip`. Answer objects: the pinned directions and the fields.
- **Motion.** Direct. Show-why for a pinned direction that is not an eigenvector: the wedge between $\mathbf x$ and $A\mathbf x$ highlights with its angle.
- **Reduced motion.** Base.
- **Accessibility.** "x at 30°: Ax = (2.1, 1.3), pointing at 31.8°, 1.8° away; it is 2.5 times as long."
- **Tutor hooks.** Ids: `handle:x`, `vec:Ax`, `ellipse`, `eigenline:<k>`, `slider:lambda`, `plot:charpoly`, `root:<k>`, `cell:<i>,<j>`.
- **Performance.** Closed-form 2 by 2 eigenvalues; trivial.
- **Artifact and web.** No difference.
- **Generators.** $A=X\Lambda X^{-1}$ with unimodular integer $X$ and integer $\Lambda$; rotation-scaling matrices $\begin{bmatrix}a&-b\\b&a\end{bmatrix}$ for complex pairs; shears for the defective case; symmetric matrices.

### 6.15 `linear-dynamics`: Powers, Markov chains and linear systems

Composite. P0, wave C (Markov mode reused in wave D). Uses: `plot-2d`, `drag-point`, `stepper`, `slider`, `marks` (trajectories, eigen-lines, flow field), `matrix`, `value-table`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** Powers $A^k$ through the eigen-decomposition; long-run behaviour; Markov matrices and steady states; Fibonacci growth; continuous systems $\frac{d\mathbf u}{dt}=A\mathbf u$, their stability and phase portraits.
- **Serves.** 1.4.6 L4 to L6; 1.5 (Markov chains), cross-cluster; 2.2 (stability of vector autoregressions), cross-cluster, P2.
- **Interactions.** Pointer: drag $\mathbf x_0$; step $k$; a decomposition toggle splits $\mathbf x_0$ into eigen-components and shows each scaled by $\lambda_i^k$. Continuous mode: a flow field, with trajectories from any dropped starting point. Markov mode: a two-state population as bars plus its point on the line $x_1+x_2=1$. Keyboard: base.
- **State.** `{ x0: number[]; k: number; trajectories: number[][] }`.
- **Checks.** `numeric` ($\mathbf x_k$; the growth ratio); `point` (the steady state); `choice` (node, saddle, spiral or centre; stable or unstable).
- **Config.** `{ A: Entry[][]; mode: 'discrete' | 'markov' | 'continuous'; x0: number[]; kMax: number; showDecomposition: boolean; field?: boolean }`.
- **Visual.** Trajectory as s2 dots; eigen-lines dashed in ink labelled with $\lambda$; $\mathbf x_0$ in `--manip`; the field in `--text-muted`. Answer objects: the fields or the learner's steady-state point.
- **Motion.** Each step moves the point over 320ms (a demonstration).
- **Reduced motion.** Steps jump.
- **Accessibility.** Table of $k$ and $\mathbf x_k$; the portrait described by type and eigenvalues.
- **Tutor hooks.** Ids: `handle:x0`, `iterate:<k>`, `eigenline:<k>`, `component:<k>`, `field`, `trajectory:<i>`, `slider:k`.
- **Performance.** RK4 trajectories, 400 steps each, at most 12 at once.
- **Artifact and web.** No difference.
- **Generators.** 2 by 2 Markov matrices with rational steady states; integer eigen-systems; one item per phase-portrait type.

### 6.16 `svd-stepper`: SVD geometry

Composite. P0, wave C (3D mode P1). Uses: `plot-2d`, `stepper`, `slider`, `matrix`, `drag-point`, `marks`, `live-formula`.

- **Purpose.** $A=U\Sigma V^\top$ as rotate, stretch, rotate; singular values as the ellipse's semi-axes; singular vectors; rank; the pseudoinverse; the symmetric case $A=Q\Lambda Q^\top$ (the spectral theorem).
- **Serves.** 1.4.6 L7; 1.4.7 L4, L6; 2.1, cross-cluster.
- **Interactions.** Stepper through the stages, each with a morph slider. Build mode: drag the image ellipse's axes to set $\sigma_1$, $\sigma_2$ and the angles, and read off $A$. A rank-one case collapses the ellipse to a segment. Pseudoinverse mode maps the column space back to the row space. Keyboard: stepper keys and handles.
- **State.** `{ stage: 0 | 1 | 2 | 3; t: number; A: Entry[][] }`.
- **Checks.** `numeric` ($\sigma_i$); `point` with metric `angle-mod-pi` (singular-vector directions); `matrix` ($\Sigma$; $A^+$); `choice` (rank).
- **Config.** `{ A: Entry[][]; mode: 'svd' | 'spectral' | 'pseudoinverse' | 'build'; dims: 2 | 3; editable?: boolean }`.
- **Visual.** The unit circle in ink; each stage's image in s3 at 15%; $\mathbf v_i$ in s2 and $\mathbf u_i$ in s3; $\sigma$ labels on the semi-axes. Answer objects: the build handles and the fields.
- **Motion.** Stage morphs over 600ms each, driven by the stepper.
- **Reduced motion.** Stepped stages.
- **Accessibility.** Stages described numerically ("Stretch: 3 along the first axis, 1 along the second").
- **Tutor hooks.** Ids: `stage:<k>`, `vec:v1`, `vec:v2`, `vec:u1`, `vec:u2`, `ellipse`, `sigma:<k>`, `handle:axis1`, `handle:axis2`.
- **Performance.** Closed-form 2 by 2 SVD; Jacobi for 3 by 3.
- **Artifact and web.** No difference.
- **Generators.** $A=U\Sigma V^\top$ with rotations at tidy angles and integer singular values.

### 6.17 `low-rank-approx`: Low-rank approximation

Composite. P0, wave C. Uses: `marks` (heatmaps, bars), `slider`, `plot-2d`, `stepper`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** A rank-$k$ approximation as a sum of rank-one layers $\sigma_i\mathbf u_i\mathbf v_i^\top$; the Eckart-Young theorem; the singular-value spectrum; compression and denoising; factor structure in a returns matrix.
- **Serves.** 1.4.7 L5, L7; 2.1 and 3.1 (factor models), cross-cluster.
- **Interactions.** Pointer: the $k$ slider; tap a layer to see its outer product as its own heatmap; a noise slider adds noise to a low-rank matrix so the learner sees how many singular values stand above the noise floor. Keyboard: base.
- **State.** `{ k: number; noise: number }`.
- **Checks.** `numeric` (the $k$ needed for 90% of the energy; the error $\lVert A-A_k\rVert_F^2=\sum_{i>k}\sigma_i^2$); `choice`.
- **Config.** `{ source: { image: 'glyph-64' | 'stripes' | 'returns' } | { matrix: number[][] } | { generate: { m: number; n: number; rank: number; noise: number; seed: number } }; kMax: number; showLayers: boolean }`.
- **Visual.** Heatmaps on the sequential ramp (images) or diverging ramp (returns); $\sigma$ bars in s2 with the cumulative energy line in ink (no handle in this plot, so s1 is allowed, but s2 keeps colours consistent across the widget). Answer objects: the fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** "k = 5 keeps 92% of the energy; the error is 0.08." Table of singular values.
- **Tutor hooks.** Ids: `slider:k`, `bar:<i>`, `layer:<i>`, `heatmap:A`, `heatmap:Ak`, `heatmap:residual`, `slider:noise`.
- **Performance.** SVD of a 64 by 64 matrix by one-sided Jacobi in a worker at mount (estimated 20 to 50 ms on the reference phone [unverified]); authored images are decomposed in the content build instead. Each $k$ change costs $64\cdot64\cdot k$ multiply-adds.
- **Artifact and web.** No difference.
- **Generators.** Seeded low-rank plus noise matrices of chosen rank and noise level.

### 6.18 `pca-lab`: Principal component analysis

Composite. P0, wave C. Uses: `plot-2d`, `plot-3d`, `drag-point` (angle handle), `marks` (points, projections, ellipse, loadings), `sim-runner` (seeded data), `slider`, `value-table`, `token-tray`, `code-cell`.

- **Purpose.** PCA as finding the direction of greatest variance: projections onto a line; covariance and its top eigenvector; centring and scaling; explained variance; reconstruction; PCA of yield-curve changes (level, slope, curvature).
- **Serves.** 1.4.7 L7, L8; 2.1, cross-cluster; 3.1, cross-cluster.
- **Interactions.** Pointer: spin a line through the centroid by its angle handle; every point drops a perpendicular onto the line and the variance of the projected coordinates shows as a live bar; maximise it. Toggles: centre the data (to show the error of not centring), standardise (multiply one axis by 100 and watch PCA chase units). 3D mode: a cloud in $\mathbb R^3$ and its best plane. Loadings mode: three loading curves across maturities to name with tokens. Scree mode: explained-variance bars. Keyboard: base.
- **State.** `{ angle: number; centred: boolean; standardised: boolean; labels?: Record<Id, Id> }`.
- **Checks.** `point` with metric `angle-mod-pi` (the first principal direction within $\pm3^\circ$); `numeric` (variance along it; the explained ratio); `choice` (the effect of not centring or of rescaling); `set` (loading names); `code` (NumPy PCA, compared with `allclose-up-to-sign`).
- **Config.** `{ data: { generate: { n: number; cov: [[number, number], [number, number]]; mean: Vec2; seed: number } } | { points: Vec2[] } | { preset: 'yield-curve-changes' | 'two-stocks' }; dims: 2 | 3; mode: 'find-direction' | 'variance' | 'reconstruct' | 'loadings' | 'scree'; centre: 'auto' | 'toggle' | 'off'; standardise?: 'toggle' | 'off'; angle?: number }`.
- **Yield-curve preset.** Synthetic daily changes at maturities 1, 2, 3, 5, 7, 10, 20 and 30 years, generated from three factors with level, slope and curvature loadings plus noise, tuned to explain about 85%, 10% and 3% of variance, in line with the pattern Litterman and Scheinkman (1991) reported. The data are synthetic, so there are no licence questions.
- **Visual.** Points in ink at 70% opacity; the learner's line in `--manip` with its handle; projection segments in s2, thin; projected points in s2 on the line; the variance bar in s2; after reveal, the covariance ellipse dashed in s3 and the principal axes in s3. Answer objects: the line, or the fields and tokens.
- **Motion.** Direct. Show-why: the learner's line turns to the first principal direction over 800ms while the variance bar grows.
- **Reduced motion.** Before and after.
- **Accessibility.** "Your line at 20° captures variance 3.1; the most possible is 4.4 at 35°." Table of points and projections.
- **Tutor hooks.** Ids: `handle:angle`, `line:direction`, `proj:<i>`, `point:<i>`, `bar:variance`, `ellipse:cov`, `pc:<k>`, `loading:<k>`, `toggle:centre`, `toggle:standardise`.
- **Performance.** At most 500 points (projection segments in one path); 3D at most 300 points.
- **Artifact and web.** As 6.11 for the `code-cell` drill.
- **Generators.** Covariance matrices with seeded principal angle and variance ratio; seeded yield-curve factor data.

### 6.19 `condition-number`: Conditioning

Composite. P1. Uses: `plot-2d` (two: $\mathbf b$-space and $\mathbf x$-space), `drag-point`, `slider`, `sim-runner`, `marks`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** How sensitive $A\mathbf x=\mathbf b$ is to small changes in $\mathbf b$: a small disc of perturbations maps to a long ellipse of solutions; $\kappa=\sigma_{\max}/\sigma_{\min}$; near-singular systems; why Markowitz weights from an inverted covariance matrix jump around. Also vector-norm unit balls ($L_1$, $L_2$, $L_\infty$) as a mode, for regularisation in 2.1.
- **Serves.** 1.6 (collinearity), cross-cluster; 2.1 (regularisation), cross-cluster; an optional extension of 1.4.7. Not in 1.4's cover list or the 18.06 final, hence P1.
- **Interactions.** Pointer: drag $\mathbf b$; a perturbation-size slider; a near-singularity slider $\varepsilon$; Run samples random perturbations into a cloud of solutions. Keyboard: base.
- **State.** `{ b: number[]; delta: number; eps: number; samples: number }`.
- **Checks.** `numeric` ($\kappa$; the amplification); `choice`.
- **Config.** `{ A: Entry[][] | { family: 'near-singular'; eps: number }; b: number[]; delta: number; samples: number; mode: 'sensitivity' | 'norm-balls' }`.
- **Visual.** The perturbation disc in `--manip-wash`; the solution cloud in s2; its bounding ellipse in s3. Answer objects: the fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** "A 1% change in b moves x by up to 40%; κ = 40."
- **Tutor hooks.** Ids: `handle:b`, `disc`, `cloud`, `ellipse`, `slider:eps`, `slider:delta`.
- **Performance.** At most 500 samples.
- **Artifact and web.** No difference.
- **Generators.** Matrices with seeded condition numbers.

---
## 7. Stochastic calculus composites (3.2)

All of these run on `sim-runner`'s counter-based randomness (2.13), so a seed reproduces every path on every device, and refining a partition never changes a path's coarse points.

### 7.1 `path-simulator`: Random walks and Brownian motion

Composite. P0 for the walk, barrier and scaled-walk modes (1.5 random walks, wave D); P2 for the Brownian, two-dimensional and Poisson modes. Uses: `plot-2d`, `sim-runner`, `slider`, `drag-point` (time cursor, barriers), `marks` (paths, envelope, sideways histogram, density), `value-table`, `numeric-input`, `choice`.

- **Purpose.** Random walks and Brownian motion: the scaling limit, a fan of paths, the distribution at time $t$, independent increments, absorbing barriers (gambler's ruin), correlated paths in two dimensions, self-similarity, and a Poisson process for contrast.
- **Serves.** 1.5 (random walks, gambler's ruin), cross-cluster; 3.2.1 L7; 3.2.2 L1, L2, L5; 2.2 (random walks against stationary series), cross-cluster.
- **Interactions.** Pointer: Run paths; drag the time cursor to see a sideways histogram of $W_t$ against the $N(0,t)$ density; the $n$ slider for the scaled walk (steps of $\pm1/\sqrt n$ every $1/n$ time units), so paths roughen into Brownian motion; barrier mode: drag absorbing levels and tally which is hit first; 2D mode: a $\rho$ slider and a scatter of increments; zoom: hands over to `local-zoom` in Brownian mode. Keyboard: base; `sim-runner` buttons.
- **State.** `{ seed: number; paths: number; n: number; t: number; barriers?: { lower?: number; upper?: number }; rho?: number }`.
- **Checks.** `numeric` ($\mathrm{Var}(W_t)$; $P(\text{hit }b\text{ first})=\frac{a}{a+b}$ for a symmetric walk started $a$ above the lower barrier and $b$ below the upper; expected duration $ab$); `choice` (properties; what step size makes the limit non-trivial); `point` (predict the one-standard-deviation envelope at $t$). Predictions are graded before Run.
- **Config.** `{ model: 'walk' | 'scaled-walk' | 'brownian' | 'brownian-2d' | 'poisson'; seed: number; paths: { initial: number; max: number }; n?: { values: number[] }; T: number; drift?: number; sigma?: number; barriers?: { lower?: number; upper?: number; absorbing: boolean }; rho?: number; show: { envelope: boolean; histogramAtT: boolean; density: boolean }; predictFirst?: CheckSpec }`.
- **Visual.** Paths on a canvas, 1px ink at 25% opacity; one emphasised sample path in s2, 2px, which explanations follow; the envelope $\pm\sqrt t$ and $\pm2\sqrt t$ dashed in s3 with labels; the sideways histogram in s2 at 40% at the cursor; the density in s3; barriers dashed in ink; the time cursor a `--manip` vertical line with its handle on the axis. Answer objects: prediction fields and handles.
- **Motion.** Run draws paths left to right over 600ms (content).
- **Reduced motion.** Paths appear at once.
- **Accessibility.** "200 paths to T = 1. At t = 0.5 the sample variance is 0.49 (theory 0.5)." Quantile table at the cursor.
- **Tutor hooks.** Ids: `path:<i>`, `path:sample`, `cursor:t`, `hist:t`, `density`, `envelope`, `barrier:upper`, `barrier:lower`, `slider:n`, `slider:rho`.
- **Performance.** Up to 1,000 paths of 1,024 steps generated in a worker (4 MB as `Float32Array`); at most 200 drawn, each reduced to the minimum and maximum per pixel column (at most 512 points); full redraw under 6 ms; dragging the cursor redraws only the histogram layer (under 1 ms).
- **Artifact and web.** No difference.
- **Generators.** Seeds; barrier levels; $\rho$ values; drift and volatility for prediction items.

### 7.2 `quadratic-variation`: Quadratic variation

Composite. P2. Uses: `plot-2d` (three panels), `sim-runner`, `slider`, `marks`, `value-table`, `numeric-input`, `choice`.

- **Purpose.** The roughness that defines Brownian motion: as the partition refines, $\sum(\Delta W)^2\to T$ while $\sum\lvert\Delta W\rvert\to\infty$; a smooth path has zero quadratic variation. This is where $(dW)^2=dt$ comes from.
- **Serves.** 3.2.2 L3; 3.2.3 L3.
- **Interactions.** Pointer: the partition slider ($2^k$ intervals, $k$ from 1 to 14); a smooth comparison toggle; predict the limit before refining. Keyboard: base.
- **State.** `{ k: number; seed: number; comparison: boolean }`.
- **Checks.** `numeric` (the limit, predicted first); `choice`.
- **Config.** `{ seed: number; T: number; kRange: [number, number]; comparison?: Expr; show: Array<'total-variation' | 'quadratic-variation'> }`.
- **Visual.** The path in ink with partition ticks in `--text-muted`; squared increments as small s2 bars; the running quadratic variation in s3 approaching the dashed line $y=t$; total variation in s2 on its own axis. Answer objects: the fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** Table of $k$, total variation and quadratic variation.
- **Tutor hooks.** Ids: `slider:k`, `path`, `ticks`, `qv`, `tv`, `line:t`.
- **Performance.** $2^{14}$ points drawn as one canvas path; bars as one path; under 4 ms.
- **Artifact and web.** No difference.
- **Generators.** Seeds.

### 7.3 `reflection-principle`: Reflection principle

Composite. P2 (the walk mode can serve 1.5 if the probability cluster wants it). Uses: `plot-2d`, `sim-runner`, `drag-point` (level $m$), `marks`, `value-table`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** $P(\max_{t\le T}W_t\ge m)=2P(W_T\ge m)=2\bigl(1-\Phi(m/\sqrt T)\bigr)$ for $m>0$, by reflecting each path after it first hits $m$; the lattice-path version for random walks.
- **Serves.** 3.2.1 L7; 3.2.2 L4; 3.3 (interview problems), cross-cluster.
- **Interactions.** Pointer: drag $m$; tap a path to show its reflection after its hitting time $\tau$; Run many to tally paths that hit $m$, paths that end above $m$, and reflected paths that end above $m$. Keyboard: base.
- **State.** `{ m: number; selected?: number; tallies: Record<string, number> }`.
- **Checks.** `numeric` (the probability, predicted first); `choice` (why the reflection is a one-to-one pairing); `ordering` (the argument's steps).
- **Config.** `{ model: 'walk' | 'brownian'; seed: number; T: number; m: number; movableM: boolean; paths: number }`.
- **Visual.** Level $m$ dashed in ink with a `--manip` handle; the selected path in s2, its reflected part dashed in s3; $\tau$ marked. Answer objects: the fields.
- **Motion.** Selecting a path draws its reflection over 480ms.
- **Reduced motion.** The reflection appears at once.
- **Accessibility.** Tallies read as counts and fractions.
- **Tutor hooks.** Ids: `handle:m`, `path:<i>`, `reflected:<i>`, `tau:<i>`, `tally:<k>`.
- **Performance.** As `path-simulator`.
- **Artifact and web.** No difference.
- **Generators.** Levels and horizons with tidy probabilities.

### 7.4 `ito-sum`: Itô integral as a limit of sums

Composite. P2. Uses: `plot-2d` (path with the step integrand; running sums), `sim-runner`, `slider`, `choice`, `marks`, `live-formula`, `numeric-input`.

- **Purpose.** The Itô integral as the limit of left-point (non-anticipating) sums; why the evaluation point matters for Brownian motion and not for smooth integrators; $\int_0^TW\,dW=\frac12(W_T^2-T)$. With the average of the endpoint values instead, every partition gives exactly $\frac12W_T^2$ (Stratonovich); with right endpoints the limit is $\frac12(W_T^2+T)$. The gap between left and right is the quadratic variation.
- **Serves.** 3.2.3 L1, L2.
- **Interactions.** Pointer: choose the evaluation rule; refine the partition; read the three running sums converging to different limits. Gambling view: "you choose your stake before the move" (left point means no peeking). Over many paths the left sum averages 0 (a martingale) and the right sum averages $T$. Keyboard: base.
- **State.** `{ k: number; rule: 'left' | 'average' | 'right'; seed: number }`.
- **Checks.** `numeric` (the left-sum limit given $W_T$; the right-minus-left gap); `choice`.
- **Config.** `{ integrand: 'W' | Expr; seed: number; T: number; kRange: [number, number]; rules: Array<'left' | 'average' | 'right'> }`.
- **Visual.** The path in ink; the step integrand in s2; the three running sums in s2, s3 and s4 with direct labels; theoretical limits dashed. Answer objects: the fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** Table of $k$ against each sum.
- **Tutor hooks.** Ids: `slider:k`, `rule:<r>`, `sum:<r>`, `step:<i>`, `path`.
- **Performance.** As `quadratic-variation`.
- **Artifact and web.** No difference.
- **Generators.** Seeds and horizons.

### 7.5 `ito-lemma-lab`: Itô's lemma

Composite. P2. Uses: `plot-2d`, `sim-runner`, `choice`, `slider`, `marks`, `derivation-steps`, `numeric-input`, `expression-input`.

- **Purpose.** Make Itô's lemma visible: for convex $f$, the average of $f(W_t)$ drifts upwards at rate $\frac12f''$; $f(W_t)-\int_0^t\frac12f''(W_s)\,ds$ has a flat average (a martingale); the second-order Taylor term survives because $(dW)^2=dt$.
- **Serves.** 3.2.3 L3, L4.
- **Interactions.** Pointer: pick $f$ ($W^2$, $e^W$, $\sin W$, $W^3$); predict whether $E[f(W_t)]$ rises, falls or stays flat; then run; toggle the compensator. Zoom-on-a-step mode: split $f(W+\Delta W)-f(W)$ into $f'\Delta W$ and $\frac12f''(\Delta W)^2$ bars; over many steps the first averages zero and the second adds up to $\frac12f''\,dt$. Keyboard: base.
- **State.** `{ f: string; paths: number; compensated: boolean }`.
- **Checks.** `choice` (the prediction); `numeric` ($E[W_t^2]=t$); `expression` ($df(W_t)$ by Itô's formula); `ordering` (derivation lines, through `derivation-steps`).
- **Config.** `{ f: Expr; seed: number; T: number; paths: number; show: { mean: boolean; predicted: boolean; compensated: 'toggle' | 'never' }; zoomStep?: boolean }`.
- **Visual.** Paths in ink at 20%; the sample mean in s2, 3px; the predicted drift dashed in s3; the compensated mean in s4 with a direct label. Answer objects: the fields.
- **Motion.** Run draws paths over 600ms.
- **Reduced motion.** Paths at once.
- **Accessibility.** "The mean of W_t² over 500 paths at t = 1 is 1.03 (theory 1)."
- **Tutor hooks.** Ids: `path:mean`, `curve:predicted`, `toggle:compensated`, `bar:first-order`, `bar:second-order`, `option:<f>`.
- **Performance.** At most 500 paths of 512 steps.
- **Artifact and web.** No difference.
- **Generators.** Seeds and choices of $f$.

### 7.6 `gbm-lab`: Geometric Brownian motion

Composite. P2 (the drag mode is an optional extension for 1.7). Uses: `plot-2d`, `sim-runner`, `slider`, `drag-point` (time cursor), `marks`, `value-table`, `live-formula`, `numeric-input`, `choice`.

- **Purpose.** Geometric Brownian motion $S_t=S_0e^{(\mu-\frac12\sigma^2)t+\sigma W_t}$: log-normal terminal values; mean against median; volatility drag; Monte Carlo prices with confidence intervals; arithmetic against geometric average returns.
- **Serves.** 3.2.3 L4; 3.2.4 L4; 1.7 (stock-price model), cross-cluster; 2.3 project 3 (Monte Carlo pricer), cross-cluster.
- **Interactions.** Pointer: sliders for $\mu$ and $\sigma$; predict whether the median path ends above $S_0$ when $\mu=5\%$ and $\sigma=40\%$ (it does not: $\mu-\frac12\sigma^2=-3\%$); run; toggle a log scale, where paths become Brownian motion with drift. Price mode: choose a payoff (call, put, digital, Asian, up-and-out barrier), Run $N$ paths and watch the 95% interval shrink like $1/\sqrt N$. Keyboard: base.
- **State.** `{ mu: number; sigma: number; T: number; seed: number; N: number; payoff?: Payoff; logScale: boolean }`.
- **Checks.** `choice` (the prediction); `numeric` (median and mean of $S_T$; the volatility at which median growth turns negative, $\sigma=\sqrt{2\mu}$; a Monte Carlo price consistent with the Black-Scholes value within the interval); `free-text` (explain why the median falls while the mean rises).
- **Config.** `{ S0: number; mu: number; sigma: number; T: number; seed: number; paths: { initial: number; max: number }; ranges: { mu: [number, number]; sigma: [number, number] }; mode: 'paths' | 'drag' | 'price'; payoff?: 'call' | 'put' | 'digital' | 'asian' | 'up-and-out'; K?: number; r?: number; barrier?: number }`.
- **Visual.** Paths in ink at 20%; the mean line in s2 and the median line in s3, both labelled; a sideways histogram at the cursor; the confidence band in `--bg-sunken`. Answer objects: the fields.
- **Motion.** Run draws paths over 600ms.
- **Reduced motion.** Paths at once.
- **Accessibility.** Mean, median and quantiles read out; table of terminal quantiles.
- **Tutor hooks.** Ids: `slider:mu`, `slider:sigma`, `line:mean`, `line:median`, `hist:T`, `band:ci`, `toggle:log`, `cursor:t`.
- **Performance.** As `path-simulator`; price mode up to $10^5$ paths in the worker, summarised without drawing.
- **Artifact and web.** No difference.
- **Generators.** $(\mu, \sigma)$ pairs either side of the drag threshold; payoffs with seeded strikes.

### 7.7 `measure-change`: Change of measure

Composite. P2. Uses: `plot-2d` (paths weighted by opacity; two histograms), `sim-runner`, `slider`, `marks`, `live-formula`, `numeric-input`, `choice`; a one-step tree in discrete mode.

- **Purpose.** Risk-neutral pricing and Girsanov's theorem: changing probabilities (reweighting paths) changes the drift, not the volatility. Discrete: $p$ against $q=\frac{1+r-d}{u-d}$ in a one-step tree. Continuous: weights $Z_T=e^{-\theta W_T-\frac12\theta^2T}$.
- **Serves.** 3.2.1 L3; 3.2.4 L2.
- **Interactions.** Pointer: slide $\theta$ and watch the weighted histogram shift; find the $\theta$ that makes the weighted mean of the discounted $S_T$ equal $S_0$. Discrete mode: drag $q$ until the discounted expected price equals $S_0$. Keyboard: base.
- **State.** `{ theta: number; q?: number; seed: number }`.
- **Checks.** `numeric` ($\theta=\frac{\mu-r}{\sigma}$; $q$); `choice` (what changes under the new measure: the drift, not the volatility).
- **Config.** `{ mu: number; r: number; sigma: number; S0: number; T: number; seed: number; paths: number; mode: 'discrete' | 'continuous'; u?: number; d?: number }`.
- **Visual.** Histogram under $P$ as an ink outline; under $Q$ as an s2 fill; path opacity proportional to weight; the $\theta$ slider in `--manip`. Answer objects: the slider value or fields.
- **Motion.** Direct.
- **Reduced motion.** Base.
- **Accessibility.** "Under the reweighting, the discounted mean is 100.4 against S0 = 100."
- **Tutor hooks.** Ids: `slider:theta`, `slider:q`, `hist:P`, `hist:Q`, `readout:mean-Q`, `tree`.
- **Performance.** Reweighting is a vector multiply over stored terminal values; under 2 ms for 10,000 paths.
- **Artifact and web.** No difference.
- **Generators.** $(\mu, r, \sigma)$ with tidy $\theta$; $(u, d, r)$ with rational $q$.

### 7.8 `binomial-tree`: Binomial pricing tree

Composite. P1 (1.7 needs it: "price a European option on a binomial tree"); reused at P2 for Shreve I. Uses: `marks` (tree), `slider`, `stepper`, `numeric-input`, `value-table`, `plot-2d` (convergence), `region-select` (early-exercise nodes).

- **Purpose.** Build an $N$-step tree; derive the risk-neutral probability; price by backward induction; replicate with $\Delta$ shares and a bond at every node; American early exercise; arbitrage when $d<1+r<u$ fails; convergence to Black-Scholes as $N$ grows.
- **Serves.** 1.7 (binomial trees), cross-cluster; 3.2.1 L1 to L3, L6; 1.9 (the C++ rewrite checks against it), cross-cluster.
- **Interactions.** Pointer: sliders for $S_0$, $u$, $d$, $r$, $K$, $N$; fill node values (terminal payoffs first, then backwards); tap nodes to mark early exercise; the stepper runs backward induction one layer at a time; arbitrage mode: build a portfolio that profits in every state. Keyboard: Up and Down follow the up and down moves, Left steps back in time; nodes are fields.
- **State.** `{ params: Params; entries: Record<NodeId, number>; exercise: NodeId[]; step: number }`.
- **Checks.** `numeric` per node through `multi` (per-node marks); `numeric` ($q$; $\Delta$ and the bond holding at the root); `set` (early-exercise nodes); `predicate: arbitrage-profitable`.
- **Config.** `{ S0: number; u: number; d: number; r: number; N: number; NMax: number; payoff: { type: 'call' | 'put' | 'digital' | 'custom'; K: number; expr?: Expr }; style: 'european' | 'american'; mode: 'build' | 'price' | 'replicate' | 'arbitrage' | 'converge'; fill: 'none' | 'terminal' | 'all'; q: 'given' | 'derive' }`.
- **Visual.** Nodes as small rounded rectangles (r-sm) with $S$ above and $V$ below; edges 1.5px ink; learner fields with a `--manip` underline; early-exercise nodes carry a flag glyph, never colour alone; the convergence plot shows prices against $N$ as s2 dots oscillating round the Black-Scholes value (dashed ink). Answer objects: the learner's node values and exercise marks.
- **Motion.** Backward induction fills one layer every 320ms (a demonstration).
- **Reduced motion.** Layers appear at once.
- **Accessibility.** The tree also renders as a table by time step and state; arrow-key navigation follows the tree.
- **Tutor hooks.** Ids: `node:<n>,<j>`, `edge:<n>,<j>,up`, `edge:<n>,<j>,down`, `q`, `delta:<n>,<j>`, `plot:converge`, `slider:<param>`.
- **Performance.** Up to $N=8$ drawn in full on phones (45 nodes); up to $N=500$ computed for the convergence plot without drawing.
- **Artifact and web.** No difference.
- **Generators.** $(u, d, r)$ with rational $q$, for example Shreve's $S_0=4$, $u=2$, $d=\frac12$, $r=\frac14$, giving $q=\frac12$; seeded strikes and styles.

### 7.9 `filtration-tree`: Information and conditional expectation

Composite. P2 (useful in 1.5 for conditional expectation as a random variable, if the probability cluster wants it). Uses: `marks` (coin-toss tree, leaf strip, partition brackets), `region-select`, `numeric-input`, `choice`, `stepper`, `live-formula`.

- **Purpose.** Information as partitions of the outcomes; $E[X\mid\mathcal F_n]$ as the average over each atom; the tower property; martingales; adapted processes; stopping times.
- **Serves.** 3.2.1 L4 to L6; 1.5 (conditional expectation), cross-cluster.
- **Interactions.** Pointer: step time $n$ and watch the atoms split; fill $E[X\mid\mathcal F_n]$ on each atom; check the martingale property by comparing with the next layer; stopping-time test: tap the outcomes where $\tau\le n$ and decide whether they form a union of atoms of $\mathcal F_n$. Keyboard: fields; region toggles.
- **State.** `{ n: number; entries: Record<AtomId, number>; selection: Id[] }`.
- **Checks.** `numeric` per atom through `multi`; `set` (the stopping set); `choice` (martingale or not; stopping time or not); `predicate: is-stopping-time`.
- **Config.** `{ tosses: 2 | 3 | 4; p: number; X: Record<string, number> | Expr; ask: 'cond-exp' | 'martingale' | 'stopping-time' | 'tower'; n?: number; tau?: Record<string, number> }`.
- **Visual.** The tree in ink; leaves as a strip of outcome cells (HHT and so on); atoms as s3 brackets under the strip; learner fields with a `--manip` underline. Answer objects: fields and selected outcomes.
- **Motion.** Atoms split over 320ms per step.
- **Reduced motion.** Splits jump.
- **Accessibility.** Outcomes as a table with columns for each $\mathcal F_n$ atom.
- **Tutor hooks.** Ids: `node:<path>`, `atom:<n>:<id>`, `leaf:<outcome>`, `entry:<atom>`, `step:<n>`.
- **Performance.** Trivial (at most 16 outcomes).
- **Artifact and web.** No difference.
- **Generators.** Seeded payoffs on leaves with rational $p$.

### 7.10 `hedging-sim`: Delta-hedging simulator

Composite. P2. Uses: `plot-2d` (two), `sim-runner`, `slider`, `marks`, `value-table`, `numeric-input`, `choice`.

- **Purpose.** Black-Scholes-Merton by replication: short a call, hold $\Delta$ shares, rebalance every $\Delta t$; hedging error shrinks like one over the square root of the number of rebalances; per-step P&L is approximately $\frac12\Gamma S^2(\sigma_{\text{realised}}^2-\sigma_{\text{implied}}^2)\Delta t$.
- **Serves.** 3.2.4 L1; 2.3 project 3, cross-cluster.
- **Interactions.** Pointer: the rebalancing frequency slider (yearly to daily on a list); realised and implied volatility sliders; one-path view or a distribution of final hedging errors over many paths; gamma-theta mode splits each step's P&L. Keyboard: base.
- **State.** `{ rebalance: number; sigmaRealised: number; sigmaImplied: number; seed: number; paths: number }`.
- **Checks.** `numeric` (the ratio of hedging-error standard deviations when rebalancing four times as often: about one half); `choice` (the sign of the P&L for a long-gamma book when realised exceeds implied); `free-text` (explain the sign).
- **Config.** `{ S0: number; K: number; T: number; r: number; sigmaImplied: number; sigmaRealised: number; rebalance: { values: number[] }; seed: number; paths: number; mode: 'one-path' | 'distribution' | 'gamma-theta' }`.
- **Visual.** Stock path in ink; hedged P&L in s2; option value in s3; the error histogram in s2. Answer objects: the fields.
- **Motion.** Run draws over 600ms.
- **Reduced motion.** At once.
- **Accessibility.** "Rebalancing 52 times: hedging error standard deviation 1.9; 208 times: 0.96."
- **Tutor hooks.** Ids: `slider:rebalance`, `slider:sigma-realised`, `slider:sigma-implied`, `path`, `pnl`, `hist:error`.
- **Performance.** Up to 2,000 paths with 252 steps in the worker; Black-Scholes deltas vectorised.
- **Artifact and web.** No difference.
- **Generators.** Seeded market parameters.

### 7.11 `heat-diffusion`: Feynman-Kac and the heat equation

Composite. P2. Uses: `plot-2d`, `sketch-pad` (payoff, prediction), `slider` (time to expiry), `sim-runner`, `marks`; optionally `plot-3d` for the price surface.

- **Purpose.** The Black-Scholes PDE as a heat equation: going back from expiry, the price curve is the payoff smoothed by a Gaussian kernel; equivalently, each point's value is the average payoff over paths that start there (Feynman-Kac).
- **Serves.** 3.2.4 L3.
- **Interactions.** Pointer: pick or sketch the payoff (call, put, digital, butterfly); slide time to expiry $\tau$ and watch the curve smooth; tap a point $(S, \tau)$ to fan Monte Carlo paths from it and see their average payoff land on the curve; predict the curve at a given $\tau$ by sketching first. Keyboard: base; sketch points mode.
- **State.** `{ payoff: Payoff; tau: number; probe?: Vec2; sketch?: SketchState }`.
- **Checks.** `curve` (the predicted price curve with features such as monotonicity and value at the strike); `numeric` (the value at a point); `choice` (what smoothing does to a digital payoff).
- **Config.** `{ payoff: 'call' | 'put' | 'digital' | 'butterfly' | { sketch: true }; sigma: number; r: number; tauRange: [number, number]; showPaths: boolean; seed: number; view3d?: boolean }`.
- **Visual.** The payoff as a ghost; the current curve in s2; the probe's paths in ink at 15% with their average marked; the surface optional. Answer objects: the sketch or fields.
- **Motion.** The $\tau$ slider is direct.
- **Reduced motion.** Base.
- **Accessibility.** Curve values at strikes read out; a table of $S$ against value.
- **Tutor hooks.** Ids: `slider:tau`, `curve:price`, `payoff`, `probe`, `paths:probe`, `sketch`.
- **Performance.** Convolution of the payoff with a Gaussian kernel on a 256-point grid per frame (under 1 ms); the probe fan at most 200 paths.
- **Artifact and web.** No difference.
- **Generators.** Seeded strikes, volatilities and times.

### 7.12 `sde-stepper`: SDE stepper and mean reversion

Composite. P2. Uses: `plot-2d`, `sim-runner`, `slider`, `expression-input`, `marks`, `value-table`, `numeric-input`, `choice`.

- **Purpose.** Simulate stochastic differential equations with Euler-Maruyama: arithmetic and geometric Brownian motion, Ornstein-Uhlenbeck, Vasicek and CIR; mean reversion, half-life $\frac{\ln2}{\kappa}$ and stationary variance $\frac{\sigma^2}{2\kappa}$; the Feller condition $2\kappa\theta\ge\sigma^2$ that keeps CIR positive; strong error against step size (order $\frac12$) compared with the exact GBM solution on the same Brownian increments.
- **Serves.** 3.2.3 L5; 3.2.4 L5; 2.2 (mean reversion; AR(1) as a discretised OU), cross-cluster; 3.1 (pairs-trading spreads, Gatev, Goetzmann and Rouwenhorst), cross-cluster.
- **Interactions.** Pointer: choose a preset or type drift and diffusion; parameter sliders; the $\Delta t$ list; paths; a stationary-distribution overlay; an error panel on log-log axes. Keyboard: base.
- **State.** `{ preset: string; params: Record<string, number>; dt: number; seed: number }`.
- **Checks.** `numeric` (half-life; stationary variance; error slope); `choice` (whether CIR can reach zero for given parameters).
- **Config.** `{ preset?: 'abm' | 'gbm' | 'ou' | 'vasicek' | 'cir'; drift?: Expr; diffusion?: Expr; x0: number; params: Record<string, number>; dtValues: number[]; T: number; seed: number; paths: number; compareExact?: boolean; stationary?: boolean }`.
- **Visual.** Paths in ink at 25%; the long-run mean dashed in s3; the stationary density sideways in s2; the error panel in ink with a slope label. Answer objects: the fields.
- **Motion.** Run draws over 600ms.
- **Reduced motion.** At once.
- **Accessibility.** Parameters and statistics read out; the error table by $\Delta t$.
- **Tutor hooks.** Ids: `slider:<param>`, `dt:<value>`, `path:<i>`, `line:mean`, `density:stationary`, `plot:error`, `field:drift`, `field:diffusion`.
- **Performance.** As `path-simulator`; CIR uses full truncation to keep the square root defined.
- **Artifact and web.** No difference.
- **Generators.** Seeded $(\kappa, \theta, \sigma)$ on either side of the Feller condition; half-life items with tidy answers.

---
## 8. Screens built from primitives alone

Some lessons need no composite: a configured host with marks and handles is enough. Listing them here shows the coverage is complete without inflating the widget count.

| Screen | Lesson | Built from |
|---|---|---|
| Integration by parts as two areas: the rectangle $uv$ splits into $\int u\,dv$ and $\int v\,du$ under a parametric curve | 1.3.4 L6 | `plot-2d`, `param-curve` and two `region` marks, `drag-point` on the curve parameter, `live-formula`, then `derivation-steps` |
| Arc length as the limit of polylines | 1.3.4 L9 | `plot-2d`, `curve`, a polyline mark through $n$ curve points, `slider` for $n$, `live-formula` |
| Growth-rate race: order $\ln x$, $x^3$, $e^x$, $x!$ | 1.3.1 L3 | `plot-2d` with a log $y$-axis, four `curve` marks, `token-tray` ordering |
| Parametric curves and velocity vectors | 1.3.2 L9 | `plot-2d`, `param-curve`, `drag-point` on the parameter, a `vector` mark for $(x'(t), y'(t))$, `live-formula` |
| Equation of a plane from a normal vector and a point | 1.3.6 L3 | `plot-3d`, a plane mark, `drag-point` for the point, a `vector` mark for the normal, `live-formula` |
| Differentiation as a matrix on cubics | 1.4.3 L8 | `matrix` (4 by 4 editable), `live-formula` showing coefficient vectors, `choice` |
| Transposes and symmetric matrices | 1.4.2 L7 | `matrix` with row and column highlights, `choice` |
| The $dt$, $dW$ multiplication table | 3.2.3 L3 | `derivation-steps` in grid layout |
| Partial fractions and trigonometric substitution | 1.3.4 L7 | `derivation-steps`, `expression-input` with `form: 'single-fraction'` |

---

## 9. Generators

Every composite marked "yes" needs seeded instances for practice, quizzes, homework and exams (contract in 2.12). "Seed only" means the generator varies the random seed and simple parameters; the maths of the item stays fixed.

| Widget | Generator | What varies | Construction for tidy answers |
|---|---|---|---|
| `limit-explorer` | yes | Function family, $a$, which side | Factor-and-cancel rationals; integer jump values |
| `epsilon-delta` | yes | $f$, $a$, $\varepsilon$ rounds | Linear and quadratic families with known $\delta(\varepsilon)$ |
| `local-zoom` | yes | Function from a catalogue, centre | L'Hôpital pairs with integer limits |
| `secant-tangent` | yes | Polynomial, points, implicit curve | Integer coefficients, round slopes |
| `derivative-tracer` | yes | $f$, option sets | Integer critical points; distractors $f''$, $-f'$, shifted $f'$, antiderivative |
| `growth-rectangle` | yes | $x$, $dx$, product pair | Integers |
| `function-mapping` | yes | Chains, points, substitution integrals | Points with tidy images |
| `root-finder` | yes | Polynomial, start, method | Integer brackets; designed cycles |
| `rates-scene` | yes | Scene sizes and rates | Pythagorean triples |
| `objective-explorer` | yes | Sheet sizes, Kelly $(p, b)$, two-asset parameters | Chosen optimum first, parameters derived |
| `sign-chart` | yes | Factors | Integer roots and poles |
| `convexity-chord` | yes | Function, interval, atoms | Rational weights |
| `riemann-sum` | yes | Polynomial, interval, rule, $n$ | Integer coefficients; rational exact areas |
| `accumulator` | yes | Integrand, bounds, $p$ | Closed-form antiderivatives |
| `slope-field` | yes | Equation family, parameters, $h$ | Separable equations with closed forms |
| `solid-of-revolution` | yes | Profile, bounds, axis | Polynomial profiles |
| `series-explorer` | yes | Series type, ratio, $p$, radius | Rational ratios; integer radii |
| `taylor-builder` | yes | Function, centre, degree; bond terms | Catalogue functions at tidy centres |
| `surface-explorer` | yes | Surface family, point | Integer partials at the point |
| `gradient-compass` | yes | Function, point | Integer gradients |
| `descent-lab` | yes | Bowl rotation, eigenvalue ratio, start | Eigenvalues chosen first |
| `quadratic-form` | yes | Entries; Hessians; correlation pairs | Chosen definiteness; tidy bounds |
| `dependency-graph` | yes | Function forms, point | Tidy values |
| `region-bounds` | yes | Boundaries, order | Integer intersections |
| `volume-slicer` | yes | Surface, region | Polynomial integrands |
| `lagrange-explorer` | yes | $f$, $g$, $c$; covariance | Chosen optimum first |
| `derivation-steps` | yes | Constants inside template derivations | Templates |
| `vector-combo` | yes | Vectors, target | Integer solutions |
| `projection-lab` | yes | Vectors, planes | Rational coefficients |
| `row-column-picture` | yes | System | Integer solutions; singular cases |
| `elimination-lab` | yes | Matrix, goal | $A=LU$ from chosen factors; unimodular matrices |
| `matrix-multiply` | yes | Matrices, shapes | Small integers |
| `transform-grid` | yes | Matrix, target glyph | Integer and unimodular matrices |
| `subspace-tester` | yes | Set from a catalogue | Parameters |
| `four-subspaces` | yes | Matrix of chosen rank, tokens | $A=CR$ with integer factors |
| `solution-set` | yes | Matrix, $\mathbf b$ | Integer particular and special solutions |
| `basis-change` | yes | Basis, point, $T$ | Determinant $\pm1$ bases |
| `least-squares-fit` | yes | Data, degree | Residuals orthogonal to the columns by construction |
| `gram-schmidt` | yes | Vectors | Whole-number norms |
| `determinant-lab` | yes | Matrix, mode | Small determinants; zero-rich rows |
| `eigen-finder` | yes | Matrix type | $X\Lambda X^{-1}$ with unimodular $X$ |
| `linear-dynamics` | yes | Matrix, $\mathbf x_0$, type | Rational steady states; one per portrait type |
| `svd-stepper` | yes | Angles, singular values | Tidy angles, integer $\sigma$ |
| `low-rank-approx` | yes | Rank, noise | Seeded factors |
| `pca-lab` | yes | Covariance, angle, ratio | Eigen-decomposition chosen first |
| `condition-number` | yes | Matrix | Chosen singular values |
| `path-simulator` | yes | Seed, barriers, drift, $\rho$ | Formula answers |
| `quadratic-variation` | seed only | Seed | |
| `reflection-principle` | yes | Level, horizon | Tidy probabilities |
| `ito-sum` | seed only | Seed, horizon | |
| `ito-lemma-lab` | seed only | Seed, $f$ | |
| `gbm-lab` | yes | $(\mu, \sigma)$, payoff, strike | Pairs either side of $\sigma=\sqrt{2\mu}$ |
| `measure-change` | yes | $(\mu, r, \sigma)$; $(u, d, r)$ | Rational $q$; tidy $\theta$ |
| `binomial-tree` | yes | $(S_0, u, d, r, K, N)$, style | Rational $q$ |
| `filtration-tree` | yes | Payoffs on leaves, $p$ | Rational values |
| `hedging-sim` | seed only | Seed, market parameters | |
| `heat-diffusion` | seed only | Strike, volatility, time | |
| `sde-stepper` | yes | $(\kappa, \theta, \sigma)$ | Either side of the Feller condition |

Primitives have no generators of their own.

---

## 10. Rejected alternatives and open questions

### 10.1 Rejected

| Alternative | Why rejected |
|---|---|
| Three.js or another WebGL library for 3D | About 150 KB or more compressed, WebGL context loss on low-end phones, a separate styling and accessibility story; our 3D needs are surfaces, planes, vectors and columns, which Canvas 2D with painter's sorting handles inside the budget |
| Desmos API or GeoGebra embeds | Both need network access or iframes, which the Artifact blocks; GeoGebra's bundle is very large; neither matches the design tokens or the check state machine |
| JSXGraph, Mafs or D3 as the plotting base | JSXGraph would cover 2D but brings its own styling and event model; Mafs needs React; D3 is a toolkit rather than a widget model. Our primitives are small, token-styled and built around keyboard paths and `describe()` from the start |
| Plotly | Several megabytes, slow on phones, chart-oriented rather than manipulation-oriented |
| math.js as the expression engine | Large for what the widgets use, and it would be a second symbolic system beside the Compute Engine; our `expr` covers evaluation, differentiation and Taylor coefficients, and the Compute Engine stays for grading only |
| Finite differences for derivatives and Taylor coefficients | Noisy at high magnification and high order; symbolic derivatives and truncated power series are exact to float precision |
| Floating-point elimination | Shows $0.333\ldots$ where the learner wrote $\frac13$; exact fractions match hand work |
| Live correctness indicators on Problem screens | Turns a problem into a search for the green state; live indicators are kept for Explore screens only |
| Hand-written widgets per lesson | The Stage 1 lesson showed the cost (1,316 lines and 23 defects for 12 minutes) |
| Implicit 3D surfaces by marching cubes | Too costly per frame on phones; 3D scenes use parametric surfaces, quadrics and planes |
| A KKT (inequality constraints) widget now | Not in 1.3's cover list or exit; a binding or slack inequality can be added to `lagrange-explorer` when 2.1 needs it |
| A Fourier-matrix widget | Not in 1.4's cover list; revisit if the course-architecture blueprint adds it |
| Dedicated widgets for measure-theoretic foundations, change of numéraire, the martingale representation theorem and Heath-Jarrow-Morton | These are proofs and modelling frameworks with no quantity the learner can usefully move; `derivation-steps` and free-text items carry them, and a widget would add machinery without an action |
| Tutor actions through page tools for every highlight | Each tool round is a separate paid request (several seconds on the default tier); one JSON reply with ids is cheaper and faster |

### 10.2 Open questions

1. **WebAssembly in the Artifact** [unverified, probe running]. Only `code-cell` depends on it; every other widget is plain JavaScript.
2. **Dynamic `import()` of the Artifact's own module files** [unverified]. Lazy loading per screen assumes it; the fallback is one bundle per course.
3. **ulab coverage** [unverified]: whether `numpy.linalg` in the MicroPython build includes `eig` (symmetric), `cholesky`, `inv` and `det`, and whether it lacks SVD. Decides which 1.4 code drills run in the Artifact.
4. **Design sign-off** on two cluster rules: skipping series slot s1 in plots with handles, and blue numbers in `live-formula` for values the learner drives.
5. **Measured budgets.** The `plot-3d` orbit budget, the 64 by 64 SVD time and the 1,000-path worker time are estimates until measured on the reference device.
6. **Ownership merges.** `sim-runner`, `path-simulator` (walk modes) and the probability cluster's simulation widget must merge into one specification; so must `number-line`, `sketch-pad` and `function-mapping` with the algebra cluster.
7. **Lesson outline.** The course-architecture blueprint may regroup the lessons in section 1; no widget depends on the numbering.

---

## 11. All widgets

Build waves: **A** Stage 0, 1.1 and 1.2; **B** single-variable calculus; **C** multivariable calculus and linear algebra; **D** probability (1.5). P1 and P2 follow wave D. Within a wave, build in the order listed.

| # | Id | Kind | Priority | Wave | Curriculum items |
|---|---|---|---|---|---|
| 1 | `plot-2d` | primitive (host) | P0 | A | 0.2 onwards; all of 1.3, 1.4, 3.2 |
| 2 | `marks` | primitive (marks) | P0 | A | all |
| 3 | `drag-point` | primitive (handle) | P0 | A | all |
| 4 | `slider` | primitive (control) | P0 | A | all |
| 5 | `live-formula` | primitive (display) | P0 | A | all |
| 6 | `value-table` | primitive (control) | P0 | A | all; the table view of every chart |
| 7 | `number-line` | primitive (host) | P0 | A | 0.1, 0.2, 1.3.1, 1.3.3, 1.3.5 |
| 8 | `stepper` | primitive (control) | P0 | A | 1.3.1, 1.3.2, 1.4.2, 1.4.4, 1.4.6, 1.4.7, 3.2 |
| 9 | `region-select` | primitive (handle) | P0 | A | 0.x, 1.3.3, 1.5, 3.2.1 |
| 10 | `token-tray` | primitive (control) | P0 | A | 1.3.1 to 1.3.6, 1.4.3, 1.4.7, 3.2.3 |
| 11 | `sketch-pad` | primitive (handle) | P0 | A | 0.2, 1.3.2 to 1.3.4, 3.2.4 |
| 12 | `choice` | primitive (control, engine) | P0 | A | all |
| 13 | `numeric-input` | primitive (control, engine) | P0 | A | all |
| 14 | `expression-input` | primitive (control, engine) | P0 | A | all |
| 15 | `code-cell` | primitive (control, programming cluster) | P0 | A | 0.4, 1.1, 1.4.4, 1.4.7 |
| 16 | `sim-runner` | primitive (runner) | P0 | A or D | 1.5, 1.4.4, 1.4.7, 3.2 |
| 17 | `plot-3d` | primitive (host) | P0 | C | 1.3.4, 1.3.6 to 1.3.8, 1.4.1 to 1.4.7, 3.2.4 |
| 18 | `matrix` | primitive (host) | P0 | C | 1.4, 1.3.6, 1.3.7, 3.2.2 |
| 19 | `derivation-steps` | composite (shared) | P0 | A | 1.3.2, 1.3.4, 1.3.5, 1.3.7, 1.3.8, 1.4.4, 3.2.3, 3.2.4 |
| 20 | `function-mapping` | composite | P0 | A | 0.2, 1.3.2, 1.3.4, 1.5 |
| 21 | `sign-chart` | composite | P0 | A | 0.2, 1.3.3 |
| 22 | `series-explorer` | composite | P0 | A | 0.3, 1.3.5, 1.7 |
| 23 | `vector-combo` | composite | P0 | A (2D), C (3D) | 0.3, 1.4.1, 1.4.3 |
| 24 | `projection-lab` | composite | P0 | A (2D dot), C | 0.3, 1.4.1, 1.4.4, 1.3.6, 1.6 |
| 25 | `row-column-picture` | composite | P0 | A (2D), C (3D) | 0.2, 1.4.2, 1.4.3 |
| 26 | `limit-explorer` | composite | P0 | B | 1.3.1, 0.3, 1.3.4 |
| 27 | `epsilon-delta` | composite | P0 | B | 1.3.1, 1.3.5 |
| 28 | `secant-tangent` | composite | P0 | B | 1.3.2, 0.2 |
| 29 | `local-zoom` | composite | P0 (Brownian mode P2) | B | 1.3.2, 3.2.2 |
| 30 | `derivative-tracer` | composite | P0 | B | 1.3.2, 1.3.3, 1.3.4 |
| 31 | `growth-rectangle` | composite | P0 | B | 1.3.2, 0.2 |
| 32 | `root-finder` | composite | P0 | B | 1.3.1, 1.3.2, 1.1, 1.7 |
| 33 | `rates-scene` | composite | P0 | B | 1.3.2 |
| 34 | `objective-explorer` | composite | P0 | B | 1.3.3, 1.5, 1.7 |
| 35 | `convexity-chord` | composite | P0 | B | 1.3.3, 1.5, 1.7, 3.2.3 |
| 36 | `riemann-sum` | composite | P0 | B | 1.3.4, 1.5 |
| 37 | `accumulator` | composite | P0 | B | 1.3.4, 1.5 |
| 38 | `slope-field` | composite | P0 | B | 1.3.4 |
| 39 | `taylor-builder` | composite | P0 | B | 1.3.5, 1.6, 1.7 |
| 40 | `surface-explorer` | composite | P0 | C | 1.3.6, 1.6, 2.1 |
| 41 | `gradient-compass` | composite | P0 | C | 1.3.6, 2.1 |
| 42 | `descent-lab` | composite | P0 (Newton P1; momentum, stochastic P2) | C | 1.3.6, 1.4.6, 1.4.7, 2.1 |
| 43 | `quadratic-form` | composite | P0 | C | 1.3.6, 1.4.6, 1.4.7, 1.5, 1.6, 3.2.2 |
| 44 | `dependency-graph` | composite | P0 (backprop P2) | C | 1.3.6, 1.3.2, 2.1 |
| 45 | `region-bounds` | composite | P0 | C | 1.3.7, 1.5 |
| 46 | `volume-slicer` | composite | P0 | C | 1.3.7, 1.5 |
| 47 | `transform-grid` | composite | P0 | C | 1.4.2, 1.4.3, 1.4.5, 1.4.6, 1.3.7 |
| 48 | `lagrange-explorer` | composite | P0 | C | 1.3.8, 1.7, 2.3 |
| 49 | `solid-of-revolution` | composite | P0 | C | 1.3.4 |
| 50 | `elimination-lab` | composite | P0 | C | 1.4.2, 1.4.3, 1.4.5 |
| 51 | `matrix-multiply` | composite | P0 | C | 1.4.1, 1.4.2, 1.4.7 |
| 52 | `subspace-tester` | composite | P0 | C | 1.4.3 |
| 53 | `solution-set` | composite | P0 | C | 1.4.3 |
| 54 | `four-subspaces` | composite | P0 | C | 1.4.3, 1.4.4, 1.4.7 |
| 55 | `basis-change` | composite | P0 | C | 1.4.3, 1.4.6, 1.4.7 |
| 56 | `least-squares-fit` | composite | P0 | C | 1.4.4, 1.3.6, 1.6, 2.1 |
| 57 | `gram-schmidt` | composite | P0 | C | 1.4.4 |
| 58 | `determinant-lab` | composite | P0 | C | 1.4.5, 1.3.7 |
| 59 | `eigen-finder` | composite | P0 | C | 1.4.6, 1.4.7, 1.5 |
| 60 | `linear-dynamics` | composite | P0 | C (Markov reuse in D) | 1.4.6, 1.5, 2.2 |
| 61 | `svd-stepper` | composite | P0 (3D mode P1) | C | 1.4.6, 1.4.7, 2.1 |
| 62 | `low-rank-approx` | composite | P0 | C | 1.4.7, 2.1, 3.1 |
| 63 | `pca-lab` | composite | P0 | C | 1.4.7, 2.1, 3.1 |
| 64 | `path-simulator` | composite | P0 (walk, barrier, scaled-walk); P2 (Brownian, 2D, Poisson) | D | 1.5, 3.2.1, 3.2.2, 2.2 |
| 65 | `binomial-tree` | composite | P1 | after D | 1.7, 3.2.1, 1.9 |
| 66 | `condition-number` | composite | P1 | after D | 1.6, 2.1, 1.4.7 extension |
| 67 | `quadratic-variation` | composite | P2 | after P1 | 3.2.2, 3.2.3 |
| 68 | `reflection-principle` | composite | P2 | after P1 | 3.2.1, 3.2.2, 3.3 |
| 69 | `ito-sum` | composite | P2 | after P1 | 3.2.3 |
| 70 | `ito-lemma-lab` | composite | P2 | after P1 | 3.2.3 |
| 71 | `gbm-lab` | composite | P2 | after P1 | 3.2.3, 3.2.4, 1.7, 2.3 |
| 72 | `measure-change` | composite | P2 | after P1 | 3.2.1, 3.2.4 |
| 73 | `filtration-tree` | composite | P2 | after P1 | 3.2.1, 1.5 |
| 74 | `hedging-sim` | composite | P2 | after P1 | 3.2.4, 2.3 |
| 75 | `heat-diffusion` | composite | P2 | after P1 | 3.2.4 |
| 76 | `sde-stepper` | composite | P2 | after P1 | 3.2.3, 3.2.4, 2.2, 3.1 |

**Count:** 76 widgets: 18 primitives and 58 composites (1 shared, 26 calculus, 19 linear algebra, 12 stochastic calculus). Of these, 64 are P0, 2 are P1 and 10 are P2.

---

## 12. Cross-cluster needs

### 12.1 Primitives other clusters will need

All 18 primitives are cluster-neutral and should be specified once, in the engine blueprint, from the union of every cluster's catalogue. The ones this catalogue expects others to need most:

1. **`plot-2d`** with log axes, polar and ternary coordinates, linked plots and the table view: algebra (graphs), probability (densities, simulations), statistics (regression), finance (payoffs, price paths), ML (losses, decision boundaries).
2. **`marks`**, especially `curve`, `region`, `bars`, `scatter`, `paths`, `band`, `ghost` and `label`.
3. **`drag-point`** with its constraint set and the E-key exact editor.
4. **`slider`**, **`stepper`**, **`value-table`** and **`live-formula`**.
5. **`number-line`**: number (0.1), inequalities (0.2), confidence intervals (1.6).
6. **`region-select`**: sample spaces, Venn regions, grids (1.5); the prototype's dice grid is already one.
7. **`token-tray`**: ordering proofs and algorithms (1.8), sorting into bins, building expressions.
8. **`sketch-pad`**: sketching graphs (0.2), CDFs (1.5), payoff diagrams (1.7).
9. **`sim-runner`** with counter-based seeds: all of probability (1.5), bootstrap and permutation tests (1.6), backtests with seeded noise (2.3).
10. **`matrix`**: covariance and design matrices (1.6), transition matrices (1.5), neural-network weights (2.1).
11. **`plot-3d`**: loss surfaces (2.1), joint densities (1.5), volatility surfaces (2.3 project 3).
12. **`derivation-steps`**: every topic with derivations or proofs.

### 12.2 Composites from this catalogue that other clusters should reuse rather than rebuild

| Composite | Other uses |
|---|---|
| `function-mapping` | 0.2 functions and inverses; 1.5 transformations of random variables |
| `sign-chart` | 0.2 inequalities |
| `series-explorer` | 0.3 sequences and series; 1.7 annuities and perpetuities |
| `vector-combo`, `projection-lab`, `row-column-picture` | 0.2 and 0.3 (2D modes) |
| `accumulator`, `riemann-sum`, `region-bounds`, `volume-slicer` | 1.5 densities, CDFs and joint distributions |
| `convexity-chord`, `objective-explorer` | 1.5 Jensen, Kelly sizing; 1.7 convexity |
| `linear-dynamics`, `eigen-finder` | 1.5 Markov chains and stationary distributions |
| `path-simulator` (walk modes) | 1.5 random walks and gambler's ruin |
| `quadratic-form`, `least-squares-fit`, `taylor-builder` | 1.6 covariance, regression, the delta method |
| `binomial-tree`, `gbm-lab`, `lagrange-explorer` | 1.7 options and portfolios; 2.3 projects |
| `descent-lab`, `dependency-graph`, `pca-lab`, `low-rank-approx` | 2.1 machine learning |
| `sde-stepper` | 2.2 mean reversion; 3.1 pairs trading |

### 12.3 What this catalogue needs from other clusters

| Need | Expected owner | Used in |
|---|---|---|
| `unit-circle` with angle handle and area overlays (triangle, sector, triangle) | precalculus (0.3) | 1.3.1 L4, 1.3.2 L8 |
| Histogram and simulate widget (design 5.3 item 13) | probability (1.5) | consistency with `path-simulator` and `gbm-lab` histograms |
| Linked density and CDF widget | probability (1.5) | `accumulator` density mode should match or reuse it |
| `code-cell` NumPy helpers (`allclose_up_to_sign`, subspace comparison) | programming (1.1) | 1.4.4 L7, 1.4.7 L8, the 1.4 exit test |
| Expression manipulator (design 5.3 item 11) | algebra (0.2) | optional in 1.3.4 L5 and L7 for algebraic steps |
| Bertie's face, speech bubble and pointer drawn beside an annotated element | engine and tutor blueprint | every `annotate()` call |

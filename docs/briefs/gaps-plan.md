# Gap pass: Stage 1 maths (topics 1.3 to 1.5)

Planner's design for `docs/ENGINE-BACKLOG.md` items 383 (calculus), 401 (linear algebra) and 423 (probability), from the coverage sections of `docs/reviews/review-1.3.md`, `review-1.4.md` and `review-1.5.md`. Each gap is judged against the topic's exit line in `docs/curriculum.md` (1.3: the MIT 18.01 final at 70% and the 18.02 problem sets on partial derivatives and Lagrange multipliers; 1.4: the MIT 18.06 final at 70%, with least squares and PCA in NumPy; 1.5: two Stat 110 past finals at 70%) and against the quant use the curriculum names.

Shape of the fix: one new level appended to each of seven courses, so no existing lesson id, exam, review, homework or progress record changes. Every level has 4 to 6 lessons plus `review-n` and `homework-n`. Total: **31 new lessons** in 7 new levels. The briefs are `docs/briefs/gap-<course>.md`, one `## Level <n>` section each.

| Course | New level | Lessons | Brief |
| --- | --- | --- | --- |
| `limits` (1.3) | 5, Theorems, rates and shape | l17 to l20 (4) | `gap-limits.md` |
| `integrals` (1.3) | 4, More techniques | l14 to l17 (4) | `gap-integrals.md` |
| `multivar` (1.3) | 5, Changing variables and many constraints | l17 to l20 (4) | `gap-multivar.md` |
| `eigen` (1.4) | 4, Factorisations at work | l13 to l17 (5) | `gap-eigen.md` |
| `random-vars` (1.5) | 5, Conditioning and inequalities | l17 to l20 (4) | `gap-random-vars.md` |
| `limits-thm` (1.5) | 4, Joint densities and transformations | l14 to l19 (6) | `gap-limits-thm.md` |
| `markov` (1.5) | 4, Reversible chains and sampling | l13 to l16 (4) | `gap-markov.md` |

## Decisions that differ from the expected additions

- **Skills.** No new skill is added. Every new lesson uses an existing skill id of its course. A new skill would also break the validator: `topic-<x>.json` must cover every skill of its topic's courses, and the exams are not edited in this pass.
- **Probability split.** The continuous material (joint densities, transformations, convolution, order statistics, Gamma, Beta, chi-square, t, MGFs) goes in `limits-thm`, not `random-vars`. The topic's course order is counting-chance, conditional, random-vars, limits-thm, markov. Densities, the exponential and the normal first appear in `limits-thm` levels 2 and 3, so a `random-vars` level 5 on densities would come before them. `random-vars` level 5 takes the material that needs only discrete tables and the 1.3 calculus: the law of total variance, random sums, Jensen and Cauchy–Schwarz, the multinomial and the negative binomial.
- **The bivariate normal** goes in `eigen` (l16, matrix form, conditional mean as a projection). It builds on eigen l8's risk ellipses and multivar l16's normal density. `limits-thm` l14 proves the independence fact for jointly normal pairs and cites eigen l16.
- **The Poisson process** goes in `markov` l16, as a process that forgets its past in continuous time. `limits-thm` l18 introduces the Gamma as the wait for the $n$th arrival, and `markov` l16 cites it.
- **The strong law** is stated in `markov` l15, as the ergodic theorem behind MCMC, and is not a lesson of its own (see the left-out lists).
- **Related rates and the MVT** fill a whole `limits` level with inverse-function derivatives and concavity, rather than one lesson each: a level needs 4 lessons, and inverse trigonometric derivatives are needed for `integrals` l15. L'Hôpital is already taught in `limits` l16 (0/0, ∞/∞, and $1^\infty$ by logs in its compounding transfer).

## limits: level 5, Theorems, rates and shape

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l17-somewhere-in-between` | The mean value theorem | Use Rolle’s theorem and the mean value theorem to bound how far a function can move. | `lm-derivative` |
| `l18-rates-in-step` | Related rates | Find one rate of change from another by differentiating an equation that links them in time. | `lm-chain` |
| `l19-running-backwards` | Derivatives of inverse functions | Differentiate an inverse function, including $\arctan x$ and $\arcsin x$. | `lm-rules`, `lm-chain` |
| `l20-which-way-it-bends` | Concavity and curve sketching | Use $f''$ to find where a graph bends up or down, and sketch a curve from its derivatives. | `lm-optimise`, `lm-derivative` |

Quant uses: a bound on a P&L move from a bound on delta (l17); how fast volatility rises when variance rises, and a bond's price drift as its yield moves (l18); implied volatility as an inverse function, $d\sigma/dC = 1/\text{vega}$, and the slope of a quantile function (l19); convex payoffs, concave log utility and the normal density's inflection at one standard deviation (l20).

Left out: hyperbolic functions (rare on 18.01 finals and unused in quant work at this stage; the reviewer rated them minor); other indeterminate forms beyond l16 (l16 already covers 0/0, ∞/∞ and $1^\infty$ through logs); differentials and linear approximation (taylor l1 to l3 cover them, with Newton's method).

## integrals: level 4, More techniques

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-splitting-fractions` | Partial fractions | Integrate a rational function by splitting it into partial fractions. | `in-techniques` |
| `l15-circles-and-powers` | Trigonometric integrals and substitution | Integrate powers of $\sin x$ and $\cos x$, and use a trigonometric substitution for $\sqrt{a^2 - x^2}$ and $a^2 + x^2$. | `in-techniques` |
| `l16-infinite-height` | Integrands that blow up | Evaluate an improper integral whose integrand is unbounded, and decide when it converges. | `in-techniques`, `in-apply` |
| `l17-solids-of-revolution` | Volumes by slicing | Find a volume of revolution by discs or shells, and the length of a curve. | `in-apply` |

Quant uses: the log-odds (logit) as $\int \frac{dp}{p(1-p)}$ and logistic adoption curves (l14); the Cauchy density, whose normaliser is $\int \frac{dx}{1+x^2} = \pi$ and whose mean does not exist (l15); the chi-square(1) and arcsine densities, which are unbounded yet integrate to 1 (l16); the volume under the bell surface by shells, which recovers multivar l16's $\pi$ (l17).

Left out: hyperbolic substitutions and hyperbolic functions (minor on 18.01 finals; no quant use here); surface area of revolution and work or fluid-force applications (rare on recent finals; no quant use); reduction formulas for high trig powers (l15 teaches the half-angle and odd-power cases, which is what finals set).

## multivar: level 5, Changing variables and many constraints

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l17-stretching-the-grid` | Change of variables | Change variables in a double integral with the Jacobian determinant. | `mv-integrals` |
| `l18-three-inputs` | Triple integrals | Evaluate a triple integral over a box and a simple solid, and use spherical coordinates for a ball. | `mv-integrals` |
| `l19-many-constraints` | Lagrange with several constraints | Optimise a function of three variables under one or two constraints, such as portfolio variance at a target return. | `mv-lagrange` |
| `l20-edges-count` | Extremes on a closed region | Find the absolute maximum and minimum on a closed region by checking the interior and the boundary. | `mv-optimise`, `mv-lagrange` |

Quant uses: the sum and difference of two returns, and why the density picks up a factor of $\frac12$ (l17); three independent shocks and the chance their total stays under a limit (l18); the minimum-variance three-asset portfolio for a target return, and the multiplier as the frontier's slope (l19); weights with position limits, where the optimum sits on the edge (l20).

Left out: line integrals, Green's theorem, divergence and curl (18.02 topics, but the exit line names only the partial-derivative and Lagrange problem sets, and no quant use arises at this stage); partial derivatives with constrained variables (one 18.02 problem type, with no quant use); the bordered Hessian (l19 and l20 compare values at the candidates instead, as 18.02 does).

## eigen: level 4, Factorisations at work

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l13-same-map-new-basis` | Similar matrices | Recognise similar matrices and what they share: eigenvalues, trace, determinant and rank. | `eg-diag`, `eg-eigen` |
| `l14-continuous-time` | Systems of differential equations | Solve $d\mathbf{u}/dt = \mathbf{A}\mathbf{u}$ with $e^{\mathbf{A}t}$ and read stability from the eigenvalues. | `eg-diag`, `eg-eigen` |
| `l15-matrix-square-root` | The Cholesky factorisation | Factor a positive definite matrix as $\mathbf{L}\mathbf{L}^T$ and use it to simulate correlated returns. | `eg-pd` |
| `l16-correlated-normals` | The multivariate normal | Describe a bivariate normal by its mean and covariance, and find the conditional mean and variance of one variable given the other. | `eg-pd`, `eg-pca` |
| `l17-best-possible-inverse` | The pseudoinverse | Build $\mathbf{A}^+$ from the SVD and use it for least squares when $\mathbf{A}^T\mathbf{A}$ is singular. | `eg-svd` |

Quant uses: one risk model written in asset and in factor coordinates (l13); two coupled mean-reverting spreads and a continuous-time rating generator, $e^{\mathbf{Q}t}$ (l14); correlated return simulation for Monte Carlo VaR (l15); the expected move of one stock given another's, and the Mahalanobis distance of an unusual day (l16); regression on collinear factors and hedging with redundant instruments (l17).

Left out: complex and Hermitian matrices (one screen in l13 shows a rotation's complex eigenvalues; Hermitian matrices and the Fourier matrix are rare on 18.06 finals and unused here); the Jordan form (eigen l3 already shows that the shear cannot be diagonalised, which is the 18.06 final's level); vector space axioms (18.06 finals ask subspace, basis and dimension questions, which elimination level 2 and least-squares l2 cover). The exam gaps the reviewer listed (least squares from the normal equations or QR in code, PCA in code, the projection matrix, the four subspaces, $d\mathbf{u}/dt = \mathbf{A}\mathbf{u}$) are for the exam extension.

## random-vars: level 5, Conditioning and inequalities

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l17-variance-given-information` | Conditional variance | Use the law of total variance, $\mathrm{Var}(Y) = E[\mathrm{Var}(Y \mid X)] + \mathrm{Var}(E[Y \mid X])$. | `rv-condexp`, `rv-variance` |
| `l18-random-sums` | Sums of a random number of terms | Find the mean and variance of a sum whose number of terms is random. | `rv-condexp`, `rv-variance` |
| `l19-convex-bets` | Jensen’s inequality | Compare $E[g(X)]$ with $g(E[X])$ for convex and concave $g$, and see why volatility drags on growth. | `rv-expect` |
| `l20-many-categories` | Several categories and repeated waits | Use the multinomial and negative binomial distributions, with means and covariances from indicators. | `rv-linearity`, `rv-variance` |

Quant uses: P&L variance across calm and volatile regimes (l17); a day's P&L as a random number of fills (l18); volatility drag, $E[\ln(1 + R)] < \ln(1 + E[R])$, and convex payoffs (l19); up, flat and down day counts and the wait for the third winning trade (l20).

## limits-thm: level 4, Joint densities and transformations

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-joint-densities` | Joint densities | Find probabilities, marginals and conditional densities from a joint density, and test independence. | `dl-continuous` |
| `l15-new-variables` | Transforming a continuous variable | Find the density of a transformed variable, with $|dx/dy|$ in one dimension and a Jacobian in two. | `dl-continuous`, `dl-normal` |
| `l16-adding-densities` | Sums and convolution | Find the density of a sum of independent variables by convolution. | `dl-continuous` |
| `l17-smallest-and-largest` | Order statistics | Find the distributions of the minimum, the maximum and the $k$th smallest of independent draws. | `dl-continuous` |
| `l18-gamma-beta` | The Gamma and Beta families | Use the Gamma, Beta, chi-square and t distributions and the stories that produce them. | `dl-continuous`, `dl-normal` |
| `l19-generating-functions` | Moment generating functions | Use moment generating functions to find moments, identify a sum’s distribution and bound a tail. | `dl-discrete`, `dl-normal`, `dl-clt` |

Quant uses: two default times (l14); inverse-transform sampling and Box–Muller for Monte Carlo (l15); the time to a second default and the P&L of two desks (l16); first-to-default among five issuers, and the best of 20 backtests (l17); a Beta prior on a strategy's hit rate, chi-square for a sample variance and t for a Sharpe ratio's t-statistic (l18); the lognormal mean as a normal MGF, and a Chernoff bound on a losing year (l19).

## markov: level 4, Reversible chains and sampling

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l13-balanced-flows` | Reversibility and detailed balance | Find a stationary distribution by checking detailed balance, and tell when a chain is reversible. | `mc-longrun` |
| `l14-walks-on-networks` | Random walks on networks | Find the stationary distribution and return times of a random walk on a weighted network. | `mc-longrun`, `mc-walks` |
| `l15-sampling-by-chain` | Markov chain Monte Carlo | Build a Metropolis chain whose stationary distribution is a chosen target, and sample from it in code. | `mc-longrun`, `mc-chains` |
| `l16-arrivals` | The Poisson process | Use the Poisson process: Poisson counts, exponential gaps, and merging and splitting streams. | `mc-chains` |

Quant uses: a market maker's inventory as a birth–death chain (l13); order flow across connected venues, and the knight's return time interview problem (l14); sampling a Bayesian posterior for a hit rate (l15); trade and order arrivals, buys and sells split from one stream (l16).

## Probability gaps left out (topic 1.5)

- Story proofs such as Vandermonde's identity: interview-style, but Stat 110 finals set them rarely, and counting-chance level 2 already builds the choose and stars-and-bars counts they rest on. A story-proof item can go in the exam extension instead.
- A full lesson on the strong law: Stat 110 finals test it only as a statement. `markov` l15 states it and the ergodic theorem.
- Continuous-time Markov chains beyond the Poisson process: not in Stat 110. `eigen` l14 shows $e^{\mathbf{Q}t}$ for a rating generator.
- Conditional variance and covariance for continuous variables: `limits-thm` l14 gives the continuous versions of $E[XY]$ and $E[Y \mid X]$ in one screen each; the discrete law of total variance (`random-vars` l17) carries over unchanged.
- The exam gaps the reviewer listed (no covariance, Poisson, exponential, hypergeometric, lognormal, reflection or absorption items; one-step items only) are for the exam extension.

## Redundant lessons (not removed)

The flagged lessons stay: progress data references them. None of their content is moved; where the new levels carry the content that should replace the repetition, the brief says so in one line and says the duplicate may be trimmed later.

- `elimination` l9 (determinant as area, repeated from vectors l10 to l11): `multivar` l17 now teaches the area factor as the Jacobian (topic 1.3, before vectors), and `eigen` l13 adds the invariance of the determinant under similarity. l9 may later be trimmed to a recap plus the product rule and $k^n$.
- `least-squares` l5 (a third pass at projection onto a line): `eigen` l17 shows $\mathbf{A}\mathbf{A}^+$ as the projection onto the column space. l5 may later be trimmed to open from the plane.
- `conditional` l2 (repeats counting-chance l7): no new content replaces it. It may later be trimmed to a bridge from counting-chance l7.
- `counting-chance` l9 screens 1 to 5 (repeat l3): no new content replaces them. They may later be trimmed to one recap screen.
- `limits-thm` l1 and l2 (repeat random-vars on the Bernoulli variance, $np(1-p)$ and $1/p$): `random-vars` l20 (negative binomial as a sum of geometric waits) and `limits-thm` l19 (MGFs of the binomial and geometric) carry the new material. l1 and l2 may later be trimmed to one recap screen each.

## For the exam extension (separate pass)

The topic exams are extended separately, after these levels are written. The briefs name the existing items each level supports. Items worth adding, one or two per level:

- topic-1.3: an MVT bound, a related-rates item, $\frac{d}{dx}\arctan x$ in a chain-rule item, a curve sketch (tap the inflection points); a partial-fractions integral, a trig substitution, $\int_0^1 x^{-p}\,dx$, a volume by shells; a Jacobian change of variables, a triple integral, a three-asset Lagrange problem, an extreme on a closed disc.
- topic-1.4: $e^{\mathbf{A}t}\mathbf{u}_0$ for a 2 × 2 system, a Cholesky factor by hand, a conditional mean of a bivariate normal, a pseudoinverse or normal-equations code item that bans `lstsq`, a PCA code item.
- topic-1.5: a law of total variance problem, a Jensen "which is larger" item, a multinomial covariance; a joint density with a marginal, a transformation, a convolution, an order statistic, a Beta posterior, an MGF identification; a detailed-balance stationary distribution, a Metropolis acceptance, a Poisson process split; one multi-part problem at Stat 110 final level.

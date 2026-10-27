# Breadth pass: maths breadth items (PLAN.md task 2b)

Planner's design for the breadth items added to `docs/curriculum.md`: 0.6 (proof), 1.10 (analysis and proof-based linear algebra), 1.11 (complex numbers, vector calculus, differential equations), 2.5 (numerical methods and optimisation), 2.6 (statistical modelling), the 3.2 additions (measure theory, PDEs), 3.4 (algebra, topology), and a gap level in `markov` for martingales and optional stopping. Each course is judged against its topic's exit line in `docs/curriculum.md`.

Shape of the pass: 13 new courses and one level appended to `markov`. No existing lesson id, level, review, homework or progress record changes. Every level has 4 to 6 lessons plus `review-n` and `homework-n`. Total: **218 new lessons** in **49 new levels** (212 lessons in 48 levels of new courses, plus 6 lessons in markov level 5).

The maps are already in place: `app/content/courses/<course>/course.json` for each new course, markov level 5 appended, and topics 0.6, 1.10, 1.11, 2.5, 2.6 and 3.4 added to `app/content/curriculum.json`, with `measure-prob` and `pdes` added to topic 3.2. The validator reports 0 errors; every new lesson shows as "not yet written". Briefs for content agents go in `docs/briefs/<course>.md`, one `## Level <n>` section each, written from the tables below.

| Course | Topic | Strand | Hours | Levels | Lessons |
| --- | --- | --- | --- | --- | --- |
| `proof` | 0.6 | pure | 40 | 3 | 15 |
| `markov` (level 5 only) | 1.5 | quant | in 1.5 | 1 | 6 |
| `analysis` | 1.10 | pure | 80 of 130 | 5 | 24 |
| `linear-maps` | 1.10 | pure | 50 of 130 | 4 | 19 |
| `complex` | 1.11 | quant | 30 | 3 | 13 |
| `vector-calc` | 1.11 | pure | 30 | 3 | 12 |
| `odes` | 1.11 | quant | 60 | 4 | 18 |
| `numerics` | 2.5 | quant | 50 of 90 | 4 | 17 |
| `convex` | 2.5 | quant | 40 of 90 | 4 | 17 |
| `stat-models` | 2.6 | quant | 50 | 4 | 18 |
| `measure-prob` | 3.2 | quant | optional | 4 | 17 |
| `pdes` | 3.2 | quant | optional | 3 | 12 |
| `algebra` | 3.4 | pure | optional | 4 | 17 |
| `topology` | 3.4 | pure | optional | 3 | 13 |

## Decisions

- **Sizing.** Existing Stage 1 courses run at about 2.7 hours per lesson (topic 1.5: 250 h over 93 lessons; topic 1.3: 200 h over 69). New courses follow that rate, between 2.4 and 3.3 hours a lesson. The splits of 1.10 (80 and 50 hours) and 2.5 (50 and 40) are my estimates; the curriculum gives only the topic totals. Optional 3.2 and 3.4 courses are sized like `ito` (3 levels of 4) and the other Stage 3 courses: 3 or 4 levels.
- **Strand.** Each new course.json has top-level `"strand"` (`quant` or `pure`) and `"strandNote"` (the roles), from the tags in `docs/curriculum.md`. Vector calculus, proof, 1.10 and 3.4 are `pure`; complex numbers, ODEs, 2.5, 2.6 and the 3.2 additions are `quant`. `markov` gets no strand field: it is a core course, and its course.json changes by additions only.
- **Skills.** New courses declare 4 to 6 new skills, all with prefixes unused elsewhere (`pv`, `an`, `lx`, `cz`, `vk`, `de`, `nm`, `cv`, `sm`, `mt`, `pe`, `ag`, `tg`); skill ids are global. Every declared skill is used by at least one planned lesson, so the "no lesson uses this skill" check passes once a course is written. `markov` level 5 uses existing `mc-*` skills only, so `topic-1.5.json` needs no change (as in `gaps-plan.md`).
- **Markov level 5.** The Poisson process is already `markov` l16. Level 5 adds martingales and optional stopping, and closes with $N_t - \lambda t$ as a martingale and the compound Poisson total, so the topic 1.5 cover line ("the Poisson process, a first look at martingales and optional stopping") is met. It sits before `ito` l8 (fair games in continuous time) and `measure-prob` level 3 (optional stopping proved).
- **Topic 3.2 course order.** `measure-prob` and `pdes` are appended after `ito`, not placed before it. `ito` is written at a computational level and needs no measure theory; `measure-prob` level 4 and `pdes` level 3 build on `ito` levels 2 and 3.
- **Black-Scholes equation before ito.** `numerics` l13 (Stage 2) solves the Black-Scholes equation before `ito` l9 derives it (Stage 3). The l13 brief should state the equation, cite `trees` l10 for the formula it must match, and say that the derivation comes in `ito` l9.
- **Optional topics.** Only 3.4 is marked `"optional": true` with hours 0, like 3.2. Topics 0.6 and 1.10 carry hours, so they are not optional in the app's sense, even though they are pure maths (see Engine notes).
- **Citations.** "Builds on" lines cite existing lessons by course and id. They also cite lessons planned in this pass (for example `markov` l17, `complex` l3, `numerics` l13), which exist in the maps but are not yet written. All 230 citations were checked against the course.json maps.

## Not changed (follow-ups for the main session)

- Stage `hours` and `exit` strings in `curriculum.json` are unchanged (stage 0 still 500, stage 1 1,400, stage 2 800). The curriculum now gives 540, 1,650 and 940, or 500, 1,490 and 940 on the quant path. Deciding which figure the app shows is a product choice.
- Stage `exitTests` lack the new pure maths lines (five short proofs; the analysis paper).
- The topic 1.5 `cover` line does not yet mention the Poisson process or martingales, and the topic 3.2 `cover` line does not mention measure theory or PDEs.
- Exam extension: `topic-1.5.json` could add an optional stopping item and a pattern-wait item for markov level 5. The new topics have no topic exams yet; they are a separate pass.

## Stage 0: From nothing

### proof (topic 0.6): Reasoning and Proof

- **Strand:** `pure`. Not needed to be hired. Research roles that hire maths PhDs, and reading proofs in papers.
- **Hours:** 40 h. 3 levels, 15 lessons, 3 reviews and 3 homework sets.
- **Art:** `steps`. **Skills:** `pv-logic` Statements and logic; `pv-sets` Sets and functions; `pv-direct` Direct proof; `pv-indirect` Contrapositive and contradiction; `pv-induction` Induction; `pv-writing` Writing a proof.

#### proof level 1: Statements and logic

- **Prerequisites:** equations L1 to L3, functions L1 (topic 0.2).
- **Builds on:** equations l1-letters-for-numbers, l10-ranges-of-answers; functions l4-one-output.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-true-or-false` | Statements that are true or false | Tell a statement from a question or an opinion, and decide whether it is true. | `pv-logic` |
| `l2-and-or-not` | And, or and not | Build compound statements with and, or and not, and check them with a truth table. | `pv-logic` |
| `l3-if-then` | If, then | Read an implication, its converse and its contrapositive, and tell which ones say the same thing. | `pv-logic` |
| `l4-for-all-there-exists` | For all and there exists | Write statements with “for all” and “there exists”, and see why their order matters. | `pv-logic` |
| `l5-saying-the-opposite` | Saying the opposite correctly | Negate a statement with quantifiers and implications without changing its meaning by accident. | `pv-logic` |

#### proof level 2: Sets and functions

- **Prerequisites:** proof L1; functions L1 and L4.
- **Builds on:** functions l1-machines, l3-what-goes-in, l4-one-output, l17-running-backwards; counting l4-choosing-without-order.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-sets` | Sets and membership | Describe a set by listing it and by a rule, and use membership and subsets. | `pv-sets` |
| `l7-combining-sets` | Unions, intersections and complements | Combine sets with union, intersection, difference and complement, and prove De Morgan’s laws. | `pv-sets`, `pv-direct` |
| `l8-functions-as-sets` | A function as a set of pairs | Treat a function as a set of input and output pairs with a domain and a codomain. | `pv-sets` |
| `l9-one-to-one-onto` | One-to-one and onto | Prove that a function is one-to-one or onto, and build its inverse when it is both. | `pv-sets`, `pv-direct` |

#### proof level 3: Proof methods

- **Prerequisites:** proof L1 and L2; series L1 (sequences) for induction.
- **Builds on:** number-sense l11-undoing-a-square; series l4-last-step, l6-gauss, l7-shifted-copy; counting l12-proving-with-vectors; quadratics l7-the-formula.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l10-direct-proof` | Direct proof | Prove a statement straight from definitions, such as “the sum of two even numbers is even”. | `pv-direct` |
| `l11-contrapositive` | Proving the contrapositive | Prove an implication through its contrapositive, such as “if $n^2$ is even then $n$ is even”. | `pv-indirect` |
| `l12-contradiction` | Proof by contradiction | Prove a statement by contradiction, including that $\sqrt{2}$ is irrational. | `pv-indirect` |
| `l13-induction` | Induction | Prove a statement for every whole number by induction, including a sum formula. | `pv-induction` |
| `l14-counterexamples` | One counterexample is enough | Disprove a general claim with a single counterexample, and tell when an example proves nothing. | `pv-logic`, `pv-direct` |
| `l15-proof-a-stranger-can-check` | A proof a stranger can check | Write a proof another reader can check line by line, with every step justified. | `pv-writing` |


## Stage 1: Foundations

### markov level 5 (topic 1.5): Martingales and stopping (gap level)

- **Strand:** `quant` (all roles; optional stopping is a common interview question). The course.json gets no `strand` field: markov is a core course, and only new courses carry one.
- **Ids:** l17 to l22 continue the existing numbering; `review-5` and `homework-5`. No existing id, level or name changes.
- **Skills:** existing `mc-*` skills only, so `topic-1.5.json` needs no change (see gaps-plan.md, Decisions).
- **Prerequisites:** markov L3 and L4; random-vars L4 (conditional expectation).
- **Builds on:** markov l9-coin-flip-walk, l10-gamblers-ruin, l7-how-long, l8-which-end, l16-arrivals; random-vars l15-given-information, l16-averaging-averages; puzzles l3-waiting-for-hh, l10-ruin-in-interviews, l20-betting-on-sequences, l23-doubling-up; ito l8-fair-games (later, Stage 3).

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l17-fair-bets` | Fair games and martingales | Recognise a martingale by checking that its expected next value, given the history, equals its value now. | `mc-chains` |
| `l18-hidden-martingales` | Martingales hiding in a walk | Build martingales from a random walk, including $S_n^2 - n$ and $(q/p)^{S_n}$. | `mc-walks` |
| `l19-optional-stopping` | Optional stopping | Use the optional stopping theorem to find ruin probabilities and expected durations without first-step equations. | `mc-walks`, `mc-firststep` |
| `l20-when-stopping-fails` | When stopping breaks the rule | Check the conditions of optional stopping, and see why doubling up cannot beat a fair game. | `mc-walks` |
| `l21-waiting-for-patterns` | Waiting for a pattern | Find the expected wait for a pattern such as HTH with a casino of fair gamblers. | `mc-firststep` |
| `l22-arrivals-fair-game` | Arrivals as a fair game | Show that $N_t - \lambda t$ is a martingale, and find the mean and variance of a compound Poisson total. | `mc-chains` |

### analysis (topic 1.10): Real Analysis

- **Strand:** `pure`. Not needed to be hired. Quant researcher at firms that hire maths PhDs; reading proofs in papers.
- **Hours:** 80 h. 5 levels, 24 lessons, 5 reviews and 5 homework sets.
- **Art:** `tangent`. **Skills:** `an-reals` The real numbers; `an-sequences` Sequences and limits; `an-series` Series; `an-continuity` Continuity; `an-calculus` Derivatives and integrals proved; `an-metric` Metric spaces.

#### analysis level 1: The real numbers

- **Prerequisites:** proof (all levels); topics 1.3 and 1.4 finished.
- **Builds on:** number-sense l11-undoing-a-square; proof l12-contradiction, l4-for-all-there-exists; series l8-adding-forever.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-gaps-in-the-rationals` | Gaps in the rationals | Show that the rationals have gaps, such as a missing square root of 2. | `an-reals` |
| `l2-least-upper-bound` | The least upper bound | Find the supremum and infimum of a set, and prove a number is one. | `an-reals` |
| `l3-completeness` | Completeness | State the completeness axiom and use it to prove that $\sqrt{2}$ exists as a real number. | `an-reals` |
| `l4-archimedes` | Whole numbers outrun everything | Prove the Archimedean property and that the rationals are dense in the reals. | `an-reals` |
| `l5-counting-infinite-sets` | Counting infinite sets | Show that the rationals are countable and, by the diagonal argument, the reals are not. | `an-reals` |

#### analysis level 2: Sequences

- **Prerequisites:** analysis L1.
- **Builds on:** limits l1-getting-closer, l2-computing-limits, l4-far-out; series l3-multiplying-each-time; limits-thm l9-averages-settle.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-epsilon-and-n` | Limits with epsilon and N | Prove that a sequence converges using the epsilon and N definition. | `an-sequences` |
| `l7-limit-laws-proved` | Proving the limit laws | Prove the limit laws for sums and products, and that a convergent sequence is bounded. | `an-sequences` |
| `l8-bounded-and-monotone` | Bounded and monotone sequences | Prove that a bounded monotone sequence converges, and use it on a recursive sequence. | `an-sequences`, `an-reals` |
| `l9-subsequences` | Subsequences and Bolzano-Weierstrass | Prove that every bounded sequence has a convergent subsequence. | `an-sequences` |
| `l10-cauchy` | Cauchy sequences | Prove that a sequence converges exactly when it is Cauchy. | `an-sequences`, `an-reals` |

#### analysis level 3: Series

- **Prerequisites:** analysis L2.
- **Builds on:** series l7-shifted-copy, l8-adding-forever; taylor l9-does-it-add-up, l10-how-far.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l11-partial-sums` | A series as a limit of partial sums | Define a series’ sum as the limit of its partial sums, and prove that terms of a convergent series tend to zero. | `an-series` |
| `l12-convergence-tests` | Comparison and ratio tests | Prove and use the comparison, ratio and integral tests. | `an-series` |
| `l13-absolute-conditional` | Absolute and conditional convergence | Tell absolute from conditional convergence, and prove the alternating series test. | `an-series` |
| `l14-rearranging` | Rearranging a series | See why rearranging a conditionally convergent series can change its sum. | `an-series` |

#### analysis level 4: Continuity and the derivative

- **Prerequisites:** analysis L2 and L3.
- **Builds on:** limits l3-without-lifting, l6-first-principles, l17-somewhere-in-between; taylor l11-bounding-error.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l15-epsilon-delta` | Continuity with epsilon and delta | Prove a function is continuous with the epsilon and delta definition, and link it to sequences. | `an-continuity` |
| `l16-intermediate-value` | The intermediate value theorem proved | Prove the intermediate value theorem from completeness. | `an-continuity`, `an-reals` |
| `l17-extreme-value` | Maximum and minimum on a closed interval | Prove that a continuous function on a closed interval attains its maximum and minimum. | `an-continuity` |
| `l18-mean-value-proved` | The derivative and the mean value theorem proved | Prove Rolle’s theorem and the mean value theorem from the definition of the derivative. | `an-calculus` |
| `l19-uniform-convergence` | Uniform convergence | Tell pointwise from uniform convergence, and prove that a uniform limit of continuous functions is continuous. | `an-continuity`, `an-sequences` |

#### analysis level 5: Integration and metric spaces

- **Prerequisites:** analysis L4.
- **Builds on:** integrals l1-thin-rectangles, l2-thinner, l5-area-undoes-slope; vectors l3-lengths-angles; least-squares l1-perpendicular.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l20-riemann-integral` | The Riemann integral defined | Define the Riemann integral with upper and lower sums, and prove that continuous functions are integrable. | `an-calculus` |
| `l21-fundamental-theorem-proved` | The fundamental theorem proved | Prove the fundamental theorem of calculus. | `an-calculus` |
| `l22-metric-spaces` | Distance in general | Check the metric space axioms for several distances, and rewrite convergence with them. | `an-metric` |
| `l23-open-and-closed` | Open and closed sets | Prove a set is open or closed, and characterise closed sets by limits of sequences. | `an-metric` |
| `l24-compactness` | Compactness | Prove that closed bounded intervals are compact and that continuous functions on compact sets are bounded. | `an-metric`, `an-continuity` |

### linear-maps (topic 1.10): Linear Maps and Proof

- **Strand:** `pure`. Not needed to be hired. Quant researcher at firms that hire maths PhDs; reading proofs in papers.
- **Hours:** 50 h. 4 levels, 19 lessons, 4 reviews and 4 homework sets.
- **Art:** `matrix`. **Skills:** `lx-spaces` Abstract vector spaces; `lx-maps` Linear maps; `lx-dual` Duality; `lx-inner` Inner product spaces; `lx-spectral` The spectral theorem; `lx-jordan` Operators and the Jordan form.

#### linear-maps level 1: Vector spaces

- **Prerequisites:** proof (all levels); topic 1.4; analysis L1.
- **Builds on:** elimination l5-everything-reachable, l7-bases, l8-real-directions; vectors l1-mixing.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-axioms` | What makes a vector space | Check the vector space axioms for lists, polynomials and functions. | `lx-spaces` |
| `l2-subspaces-and-sums` | Subspaces, sums and direct sums | Prove a subset is a subspace, and tell a sum from a direct sum. | `lx-spaces` |
| `l3-span-and-independence` | Span and independence proved | Prove that an independent list is never longer than a spanning list. | `lx-spaces` |
| `l4-bases-and-dimension` | Bases and dimension | Prove that every basis has the same length, and extend an independent list to a basis. | `lx-spaces` |

#### linear-maps level 2: Linear maps

- **Prerequisites:** linear-maps L1.
- **Builds on:** vectors l5-acting-on-a-vector, l7-one-after-another, l10-undoing; elimination l6-inputs-to-zero; least-squares l2-four-subspaces; eigen l13-same-map-new-basis.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-linear-maps` | Linear maps | Prove a map is linear, and show that a linear map is fixed by what it does to a basis. | `lx-maps` |
| `l6-kernel-and-image` | Kernel and image | Prove that the kernel and image are subspaces, and that a map is one-to-one exactly when its kernel is zero. | `lx-maps` |
| `l7-rank-nullity` | Rank-nullity proved | Prove the rank-nullity theorem and use it to count solutions. | `lx-maps` |
| `l8-maps-as-matrices` | A map as a matrix in a basis | Write a linear map as a matrix in chosen bases, and change basis. | `lx-maps` |
| `l9-invertible-and-isomorphic` | Invertible maps and isomorphic spaces | Prove that two finite-dimensional spaces are isomorphic exactly when they have the same dimension. | `lx-maps` |

#### linear-maps level 3: Duality and inner products

- **Prerequisites:** linear-maps L2.
- **Builds on:** vectors l2-lining-up, l3-lengths-angles; least-squares l1-perpendicular, l3-orthonormal, l4-straightening, l6-projection-matrix; random-vars l19-convex-bets.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l10-dual-space` | The dual space | Build the dual basis, and link the dual map to the transpose. | `lx-dual` |
| `l11-inner-products` | Inner products and norms | Check the inner product axioms, including covariance as an inner product on returns. | `lx-inner` |
| `l12-cauchy-schwarz` | Cauchy-Schwarz proved | Prove the Cauchy-Schwarz and triangle inequalities, and see why a correlation lies between $-1$ and $1$. | `lx-inner` |
| `l13-gram-schmidt-proved` | Orthonormal bases and Gram-Schmidt | Prove that Gram-Schmidt gives an orthonormal basis with the same span. | `lx-inner` |
| `l14-orthogonal-complements` | Orthogonal complements and projections | Prove that a space splits as a subspace plus its orthogonal complement, and that projection minimises distance. | `lx-inner` |

#### linear-maps level 4: Operators

- **Prerequisites:** linear-maps L3; complex L1 is helpful but not required (one screen defines complex roots).
- **Builds on:** eigen l1-directions-that-stay, l2-characteristic, l3-eigenbasis, l5-perpendicular-eigenvectors, l7-covariance-psd.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l15-eigenvalues-exist` | Why eigenvalues exist | Prove that every operator on a complex finite-dimensional space has an eigenvalue. | `lx-spectral` |
| `l16-self-adjoint` | Self-adjoint operators | Prove that a self-adjoint operator has real eigenvalues and perpendicular eigenvectors. | `lx-spectral`, `lx-inner` |
| `l17-spectral-theorem` | The spectral theorem proved | Prove the spectral theorem for symmetric matrices without notes. | `lx-spectral` |
| `l18-generalised-eigenvectors` | Generalised eigenvectors | Find generalised eigenvectors when an operator has too few eigenvectors. | `lx-jordan` |
| `l19-jordan-form` | The Jordan form | Find the Jordan form of a small matrix and read its eigenvalues’ multiplicities from it. | `lx-jordan` |

### complex (topic 1.11): Complex Numbers

- **Strand:** `quant`. Desk quant: Fourier option pricing and characteristic functions.
- **Hours:** 30 h. 3 levels, 13 lessons, 3 reviews and 3 homework sets.
- **Art:** `circle`. **Skills:** `cz-arith` Complex arithmetic; `cz-polar` The polar form and Euler’s formula; `cz-functions` Complex functions; `cz-contour` Contour integrals and residues; `cz-fourier` Fourier transforms.

#### complex level 1: The complex plane

- **Prerequisites:** topic 1.10 finished (curriculum order); trig and exp-log (topic 0.3).
- **Builds on:** quadratics l8-how-many-solutions; trig l7-arc-length, l12-adding-angles; exp-log l9-compounding-more-often; taylor l7-standard-series; eigen l13-same-map-new-basis (complex eigenvalues of a rotation).

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-square-root-of-minus-one` | A square root of minus one | Add, multiply and divide complex numbers, and solve a quadratic with no real roots. | `cz-arith` |
| `l2-points-in-a-plane` | Numbers as points in a plane | Plot complex numbers, and read modulus, argument and conjugate from the plane. | `cz-arith`, `cz-polar` |
| `l3-euler` | Euler’s formula | Derive $e^{i\theta} = \cos\theta + i\sin\theta$ from series, and multiply by rotating. | `cz-polar` |
| `l4-roots-of-unity` | Roots of unity | Find the $n$th roots of a complex number with De Moivre’s theorem. | `cz-polar` |

#### complex level 2: Complex functions

- **Prerequisites:** complex L1; multivar L1 (partial derivatives).
- **Builds on:** multivar l1-two-inputs, l4-chain-two-inputs; limits l6-first-principles; exp-log l10-natural-log.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-functions-move-the-plane` | Functions that move the plane | Picture a complex function as a map of the plane, using $z^2$ and $1/z$. | `cz-functions` |
| `l6-complex-differentiability` | Complex differentiability | Test whether a function has a complex derivative at a point. | `cz-functions` |
| `l7-cauchy-riemann` | The Cauchy-Riemann equations | Use the Cauchy-Riemann equations to decide where a function is analytic. | `cz-functions` |
| `l8-exp-and-log` | The complex exponential and logarithm | Work with the complex exponential and the many values of the logarithm. | `cz-functions`, `cz-polar` |

#### complex level 3: Integrals and Fourier

- **Prerequisites:** complex L2; integrals L3 (improper integrals); limits-thm L4 (moment generating functions).
- **Builds on:** integrals l11-to-infinity; multivar l15-polar; limits-thm l7-bell-curve, l19-generating-functions; trees l10-black-scholes; opt-dash l5-bs-pricer.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l9-contour-integrals` | Integrals along a path | Compute a contour integral by parametrising the path. | `cz-contour` |
| `l10-cauchy-theorem` | Cauchy’s theorem | Use Cauchy’s theorem and integral formula to evaluate integrals around closed paths. | `cz-contour` |
| `l11-residues` | Residues | Evaluate a real integral by summing residues inside a contour. | `cz-contour` |
| `l12-characteristic-functions` | Characteristic functions | Find a distribution’s characteristic function and recover the density by Fourier inversion. | `cz-fourier` |
| `l13-fourier-pricing` | Pricing an option by Fourier inversion | Price a European call from the characteristic function of the log price, and match Black-Scholes in code. | `cz-fourier`, `cz-contour` |

### vector-calc (topic 1.11): Vector Calculus

- **Strand:** `pure`. Not needed to be hired. Rounds out a maths degree; used in physics-style models.
- **Hours:** 30 h. 3 levels, 12 lessons, 3 reviews and 3 homework sets.
- **Art:** `grid`. **Skills:** `vk-fields` Vector fields; `vk-line` Line integrals; `vk-surface` Surface integrals; `vk-theorems` Green, Stokes and divergence.

#### vector-calc level 1: Fields and line integrals

- **Prerequisites:** multivar (all levels); complex L1 not required.
- **Builds on:** multivar l5-steepest-climb, l6-any-direction; vectors l2-lining-up; integrals l7-evaluating.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-vector-fields` | Vector fields | Sketch a vector field and read it as a gradient where possible. | `vk-fields` |
| `l2-line-integrals` | Integrating along a curve | Compute a line integral by parametrising the curve. | `vk-line` |
| `l3-work-done` | Work done by a field | Compute the work a field does along a path. | `vk-line`, `vk-fields` |
| `l4-conservative-fields` | Conservative fields and potentials | Test a field for a potential, and use it to make a line integral path-independent. | `vk-fields`, `vk-line` |

#### vector-calc level 2: Green’s theorem

- **Prerequisites:** vector-calc L1; multivar L4 (double integrals).
- **Builds on:** multivar l13-volume, l14-other-regions, l15-polar.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-divergence-and-curl` | Divergence and curl | Compute the divergence and curl of a field and read what they measure. | `vk-fields` |
| `l6-green` | Green’s theorem | Turn a line integral around a closed curve into a double integral with Green’s theorem. | `vk-theorems` |
| `l7-area-from-a-boundary` | Areas from a boundary | Find an area from a line integral around its boundary. | `vk-theorems`, `vk-line` |
| `l8-flux-across-a-curve` | Flux across a curve | Compute the flux of a field across a curve, and link it to divergence. | `vk-theorems`, `vk-line` |

#### vector-calc level 3: Surfaces and space

- **Prerequisites:** vector-calc L2; multivar L5 (change of variables, triple integrals).
- **Builds on:** multivar l17-stretching-the-grid, l18-three-inputs.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l9-parametric-surfaces` | Surfaces described by two parameters | Parametrise a surface and compute its area element. | `vk-surface` |
| `l10-surface-integrals` | Surface integrals and flux | Compute a surface integral and the flux of a field through a surface. | `vk-surface` |
| `l11-divergence-theorem` | The divergence theorem | Turn the flux out of a closed surface into a triple integral of the divergence. | `vk-theorems`, `vk-surface` |
| `l12-stokes` | Stokes’ theorem | Turn a line integral around a boundary into a surface integral of the curl. | `vk-theorems`, `vk-surface` |

### odes (topic 1.11): Differential Equations

- **Strand:** `quant`. Desk quant and rates: pricing models, mean-reverting short rates.
- **Hours:** 60 h. 4 levels, 18 lessons, 4 reviews and 4 homework sets.
- **Art:** `curve`. **Skills:** `de-first` First-order equations; `de-second` Second-order linear equations; `de-systems` Systems and stability; `de-laplace` The Laplace transform; `de-numeric` Numerical solution.

#### odes level 1: First-order equations

- **Prerequisites:** topic 1.3; complex L1 not yet needed.
- **Builds on:** exp-log l12-doubling-time; limits l11-standard-derivatives; integrals l9-undo-chain, l10-undo-product; arma l12-half-life; coint l7-snap-back.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-equations-about-rates` | Equations about rates | Write a differential equation from a story about a rate, and check a proposed solution. | `de-first` |
| `l2-separable` | Separating the variables | Solve a separable equation, including continuous compounding and logistic growth. | `de-first` |
| `l3-integrating-factor` | Linear equations and the integrating factor | Solve a first-order linear equation with an integrating factor. | `de-first` |
| `l4-slope-fields` | Slope fields and equilibria | Sketch a slope field and classify equilibria as stable or unstable. | `de-first`, `de-systems` |
| `l5-mean-reversion` | Mean reversion: the Vasicek drift | Solve $dr/dt = \kappa(\theta - r)$ and read the half-life of a rate’s pull to its mean. | `de-first` |

#### odes level 2: Second-order equations

- **Prerequisites:** odes L1; complex L1 (complex roots and Euler’s formula).
- **Builds on:** complex l3-euler; quadratics l8-how-many-solutions; trig l9-stretching-a-wave.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-second-order` | Second-order linear equations | Recognise a second-order linear equation and why it needs two starting values. | `de-second` |
| `l7-characteristic-equation` | The characteristic equation | Solve a constant-coefficient equation from its characteristic roots, real or complex. | `de-second` |
| `l8-forcing` | Forcing and particular solutions | Find a particular solution by undetermined coefficients, and add the general solution. | `de-second` |
| `l9-damping-and-resonance` | Damping and resonance | Read under-, over- and critical damping from the roots, and find when forcing resonates. | `de-second` |

#### odes level 3: Systems and stability

- **Prerequisites:** odes L2; eigen L4.
- **Builds on:** eigen l1-directions-that-stay, l2-characteristic, l14-continuous-time; multivar l9-peaks-pits-saddles.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l10-first-order-systems` | Systems of first-order equations | Write a higher-order equation as a system, and solve a linear system with eigenvectors. | `de-systems` |
| `l11-phase-plane` | The phase plane | Sketch trajectories in the phase plane for nodes, saddles, spirals and centres. | `de-systems` |
| `l12-stability` | Stability of an equilibrium | Decide an equilibrium’s stability from the trace and determinant. | `de-systems` |
| `l13-linearising` | Linearising a nonlinear system | Linearise a nonlinear system at an equilibrium with the Jacobian, as in predator and prey. | `de-systems` |

#### odes level 4: Transforms and numerical solution

- **Prerequisites:** odes L3; integrals L3 (improper integrals); first-python and numpy-pandas (topic 1.1).
- **Builds on:** integrals l11-to-infinity; taylor l6-matching-derivatives, l11-bounding-error; numpy-pandas l1-not-lists.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-laplace-transform` | The Laplace transform | Compute Laplace transforms from the definition and a table. | `de-laplace` |
| `l15-solving-with-laplace` | Solving with the Laplace transform | Solve an initial value problem with the Laplace transform and partial fractions. | `de-laplace` |
| `l16-euler-method` | Euler’s method | Step a solution forward with Euler’s method in NumPy and watch the error shrink with the step. | `de-numeric` |
| `l17-runge-kutta` | Runge-Kutta | Implement fourth-order Runge-Kutta and compare its error with Euler’s. | `de-numeric` |
| `l18-four-decimal-places` | Matching a closed form to four decimals | Solve the Vasicek drift numerically and match its closed form to four decimal places. | `de-numeric`, `de-first` |


## Stage 2: Intermediate

### numerics (topic 2.5): Numerical Methods

- **Strand:** `quant`. All roles: every pricer, fit and backtest is a numerical method.
- **Hours:** 50 h. 4 levels, 17 lessons, 4 reviews and 4 homework sets.
- **Art:** `area`. **Skills:** `nm-float` Floating point; `nm-stability` Conditioning and stability; `nm-roots` Root finding and interpolation; `nm-quadrature` Quadrature and ODE solvers; `nm-fd` Finite differences; `nm-mc` Monte Carlo.

#### numerics level 1: Errors

- **Prerequisites:** Stage 1 finished, including odes L4.
- **Builds on:** py-found l1-why-not-0-3; cpp-pricing l1-doubles; least-squares l8-qr, l10-normal-equations; regression l10-collinearity.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-floating-point` | How a computer stores a number | Read a double’s sign, exponent and mantissa, and find machine epsilon. | `nm-float` |
| `l2-cancellation` | Losing digits to cancellation | Spot catastrophic cancellation and rewrite a formula to avoid it. | `nm-float` |
| `l3-conditioning` | How sensitive a problem is | Compute a condition number and predict how much input error is amplified. | `nm-stability` |
| `l4-stability` | How sensitive an algorithm is | Compare normal equations with QR for least squares and explain which is stable. | `nm-stability` |

#### numerics level 2: Equations and curves

- **Prerequisites:** numerics L1.
- **Builds on:** taylor l3-newton; algo-think l9-halving; opt-dash l9-iv-solver; trees l11-implied-vol.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-bisection-and-newton` | Bisection and Newton compared | Compare the convergence rates of bisection, secant and Newton’s method. | `nm-roots` |
| `l6-safe-root-finder` | A root finder that never fails | Build a safeguarded Newton method and use it for implied volatility on every strike. | `nm-roots` |
| `l7-interpolation` | Interpolation and its wiggles | Fit an interpolating polynomial and see Runge’s wiggles at the ends. | `nm-roots` |
| `l8-splines` | Splines for a yield curve | Fit a cubic spline through yields and read off rates between the quoted points. | `nm-roots` |

#### numerics level 3: Integrals and time steps

- **Prerequisites:** numerics L2; odes L4.
- **Builds on:** integrals l12-no-formula, l1-thin-rectangles; odes l16-euler-method, l17-runge-kutta; limits-thm l7-bell-curve.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l9-quadrature` | Trapezium and Simpson | Integrate with the trapezium and Simpson rules and measure their error order. | `nm-quadrature` |
| `l10-gaussian-quadrature` | Gaussian quadrature | Price a European option by Gauss-Legendre quadrature against the lognormal density. | `nm-quadrature` |
| `l11-step-size` | Step size and error order | Measure a solver’s error order from a log-log plot, and choose a step for a tolerance. | `nm-quadrature`, `nm-stability` |
| `l12-stiff-equations` | Stiff equations | See an explicit solver blow up on a stiff equation, and fix it with an implicit step. | `nm-quadrature`, `nm-stability` |

#### numerics level 4: One option, three ways

- **Prerequisites:** numerics L3; trees L3; opt-dash L2.
- **Builds on:** trees l9-tiny-steps, l10-black-scholes; cpp-pricing l8-monte-carlo; opt-dash l7-mc-pricer, l8-three-pricers; multivar l3-second-partials.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l13-finite-differences` | Finite differences for a pricing equation | Replace derivatives with differences on a grid and solve the Black-Scholes equation explicitly. | `nm-fd` |
| `l14-implicit-and-crank-nicolson` | Explicit, implicit and Crank-Nicolson | Compare the stability and error of explicit, implicit and Crank-Nicolson schemes. | `nm-fd`, `nm-stability` |
| `l15-monte-carlo-error` | Monte Carlo and its error | Estimate a Monte Carlo price with its standard error, and see the $1/\sqrt{n}$ rate. | `nm-mc` |
| `l16-control-variates` | Control variates and antithetics | Cut Monte Carlo error with antithetic draws and a control variate. | `nm-mc` |
| `l17-three-ways` | One option, three numerical prices | Price one European option by finite differences, quadrature and Monte Carlo, and explain each error. | `nm-fd`, `nm-quadrature`, `nm-mc` |

### convex (topic 2.5): Convex Optimisation

- **Strand:** `quant`. All roles: portfolio construction, model fitting and execution.
- **Hours:** 40 h. 4 levels, 17 lessons, 4 reviews and 4 homework sets.
- **Art:** `ellipse`. **Skills:** `cv-convex` Convex sets and functions; `cv-lp` Linear programming; `cv-duality` Duality and KKT; `cv-qp` Quadratic programmes; `cv-descent` Gradient descent and Newton.

#### convex level 1: Convexity

- **Prerequisites:** Stage 1 finished.
- **Builds on:** eigen l6-bowls, l7-covariance-psd; random-vars l19-convex-bets; limits l20-which-way-it-bends; multivar l10-second-derivative-test.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-convex-sets` | Convex sets | Prove a set is convex, including the set of long-only weights. | `cv-convex` |
| `l2-convex-functions` | Convex functions | Test a function for convexity with the chord, the gradient and the Hessian. | `cv-convex` |
| `l3-local-is-global` | Why a local minimum is global | Prove that a local minimum of a convex function on a convex set is global. | `cv-convex` |
| `l4-recognising-convex-problems` | Recognising a convex problem | Tell whether an optimisation problem is convex, and rewrite one that is convex in disguise. | `cv-convex` |

#### convex level 2: Linear programmes

- **Prerequisites:** convex L1; elimination L2.
- **Builds on:** equations l16-where-lines-cross, l12-trapped; elimination l5-everything-reachable; numpy-pandas l1-not-lists.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-linear-programmes` | Linear programmes | Write a trading or allocation problem as a linear programme. | `cv-lp` |
| `l6-corners` | The best point is a corner | Show that a linear programme’s optimum sits at a vertex, and find it on a picture. | `cv-lp` |
| `l7-lp-in-code` | Solving a linear programme in code | Solve a linear programme with SciPy and read its status and slack. | `cv-lp` |
| `l8-lp-duality` | The dual of a linear programme | Write the dual of a linear programme and check that the optimal values match. | `cv-lp`, `cv-duality` |

#### convex level 3: Duality and KKT

- **Prerequisites:** convex L2; multivar L3 and L5 (Lagrange multipliers).
- **Builds on:** multivar l11-on-a-constraint, l12-min-variance, l19-many-constraints, l20-edges-count; alpha l13-long-short.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l9-lagrangian-dual` | The Lagrangian and the dual | Form a Lagrangian dual and prove weak duality. | `cv-duality` |
| `l10-kkt` | The KKT conditions | State the KKT conditions and solve a small inequality-constrained problem with them. | `cv-duality` |
| `l11-mean-variance-kkt` | Mean-variance by hand through KKT | Solve a constrained mean-variance problem through the KKT conditions by hand. | `cv-duality`, `cv-qp` |
| `l12-long-only` | Long-only portfolios as a quadratic programme | Solve a long-only portfolio as a quadratic programme and match a solver. | `cv-qp` |
| `l13-shadow-prices` | Multipliers as shadow prices | Read a multiplier as the value of relaxing a constraint, such as a position limit. | `cv-duality`, `cv-qp` |

#### convex level 4: Algorithms

- **Prerequisites:** convex L3; numerics L2.
- **Builds on:** multivar l8-walking-downhill; taylor l3-newton; stat-learning l7-shrinking, l8-setting-to-zero; numerics l5-bisection-and-newton.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-gradient-descent` | Gradient descent and its step size | Run gradient descent and choose a step size from the curvature. | `cv-descent` |
| `l15-convergence-rates` | How fast descent converges | Link descent’s convergence rate to the condition number of the Hessian. | `cv-descent` |
| `l16-newton-for-minimising` | Newton’s method for minimising | Minimise with Newton’s method and see quadratic convergence near the optimum. | `cv-descent` |
| `l17-checking-a-solver` | Checking a solver against theory | Check a solver’s answer with the KKT conditions and the duality gap. | `cv-duality`, `cv-descent` |

### stat-models (topic 2.6): Statistical Modelling

- **Strand:** `quant`. Quant researcher.
- **Hours:** 50 h. 4 levels, 18 lessons, 4 reviews and 4 homework sets.
- **Art:** `scatter`. **Skills:** `sm-glm` Generalised linear models; `sm-anova` Analysis of variance and design; `sm-nonpar` Nonparametric methods; `sm-bayes` Bayesian inference; `sm-mcmc` Markov chain Monte Carlo; `sm-hier` Hierarchical models.

#### stat-models level 1: Generalised linear models

- **Prerequisites:** topic 2.1 (stat-learning L3); regression (all levels).
- **Builds on:** regression l11-assumptions-fail, l12-matching-statsmodels; stat-learning l10-predicting-a-probability; estimation l6-maximising, l7-taking-logs; least-squares l10-normal-equations.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-beyond-normal-errors` | When errors are not normal | Choose a distribution and a link function for counts, proportions and yes or no outcomes. | `sm-glm` |
| `l2-logistic-as-glm` | Logistic regression as a GLM | Fit a logistic regression by maximum likelihood and read its coefficients as log odds. | `sm-glm` |
| `l3-poisson-regression` | Counts and Poisson regression | Model trade counts with Poisson regression and an exposure offset. | `sm-glm` |
| `l4-irls` | Iteratively reweighted least squares | Fit logistic and Poisson models by your own IRLS and match statsmodels. | `sm-glm` |
| `l5-deviance` | Deviance and model checks | Compare GLMs by deviance and check for overdispersion. | `sm-glm` |

#### stat-models level 2: Experiments

- **Prerequisites:** stat-models L1; testing (all levels).
- **Builds on:** testing l8-two-groups, l9-twenty-tests, l10-correcting; regression l9-several-predictors.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l6-anova` | Analysis of variance | Split variation into between-group and within-group parts. | `sm-anova` |
| `l7-f-test` | The F-test | Test whether several group means differ with an F-test, and link it to regression. | `sm-anova` |
| `l8-designing-an-experiment` | Designing an experiment | Use randomisation, blocking and replication to design an experiment. | `sm-anova` |
| `l9-execution-experiment` | Testing two execution algorithms | Design and analyse a randomised test of two execution algorithms. | `sm-anova`, `sm-nonpar` |

#### stat-models level 3: Without the assumptions

- **Prerequisites:** stat-models L2.
- **Builds on:** estimation l11-bootstrap; testing l3-p-value; garch l3-fat-tails; limits-thm l17-smallest-and-largest.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l10-rank-tests` | Rank tests | Use the Wilcoxon and Mann-Whitney tests when returns are far from normal. | `sm-nonpar` |
| `l11-permutation-tests` | Permutation tests | Build a permutation test for a strategy’s edge and compare it with a t-test. | `sm-nonpar` |
| `l12-kernel-density` | Kernel density estimates | Estimate a return density with a kernel and choose the bandwidth. | `sm-nonpar` |
| `l13-robust-estimates` | Robust estimates | Use medians, trimmed means and robust regression when outliers dominate. | `sm-nonpar` |

#### stat-models level 4: Bayesian models

- **Prerequisites:** stat-models L3; markov L4 (MCMC); limits-thm L4 (Gamma and Beta).
- **Builds on:** estimation l12-updating-a-belief; limits-thm l18-gamma-beta; markov l15-sampling-by-chain; stat-learning l7-shrinking.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-conjugate-priors` | Conjugate priors | Update Beta-binomial, Gamma-Poisson and normal models in closed form. | `sm-bayes` |
| `l15-posterior-predictive` | The posterior predictive | Predict new data from the posterior and check a model against it. | `sm-bayes` |
| `l16-fitting-by-mcmc` | Fitting a model by MCMC | Fit a Bayesian logistic regression by Metropolis sampling in code. | `sm-mcmc`, `sm-bayes` |
| `l17-has-it-converged` | Has the chain converged? | Check convergence with trace plots, several chains and the R-hat statistic. | `sm-mcmc` |
| `l18-hierarchical-models` | Hierarchical models and shrinkage | Pool many strategies’ hit rates with a hierarchical model and see the shrinkage. | `sm-hier`, `sm-bayes` |


## Stage 3: Advanced

### measure-prob (topic 3.2): Measure-Theoretic Probability

- **Strand:** `quant`. Desk quant and derivatives pricing.
- **Hours:** optional, hours not counted. 4 levels, 17 lessons, 4 reviews and 4 homework sets.
- **Art:** `bell`. **Skills:** `mt-sigma` Sigma-algebras and measures; `mt-integral` The Lebesgue integral; `mt-condexp` Conditional expectation; `mt-martingale` Martingales and stopping times; `mt-change` Change of measure.

#### measure-prob level 1: Measures

- **Prerequisites:** analysis (all levels); ito L1.
- **Builds on:** counting-chance l3-events-as-sets, l11-axioms; analysis l5-counting-infinite-sets, l20-riemann-integral; proof l7-combining-sets.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-why-measure` | Why probability needs measure | See why not every set can have a probability, with a uniform pick from an interval. | `mt-sigma` |
| `l2-sigma-algebras` | Sigma-algebras | Check the sigma-algebra axioms and generate the Borel sets. | `mt-sigma` |
| `l3-measures` | Measures and probability spaces | Build a probability space and prove continuity from above and below. | `mt-sigma` |
| `l4-measurable-functions` | Random variables as measurable functions | Define a random variable as a measurable function, and its distribution as a pushed-forward measure. | `mt-sigma` |

#### measure-prob level 2: Integration

- **Prerequisites:** measure-prob L1.
- **Builds on:** analysis l19-uniform-convergence, l20-riemann-integral; random-vars l5-long-run-average; limits-thm l9-averages-settle, l11-sums-look-normal.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-lebesgue-integral` | The Lebesgue integral | Build expectation as a Lebesgue integral from simple functions. | `mt-integral` |
| `l6-monotone-convergence` | Monotone convergence | Use the monotone convergence theorem to swap a limit and an expectation. | `mt-integral` |
| `l7-dominated-convergence` | Dominated convergence | Use dominated convergence to differentiate a price under the expectation. | `mt-integral` |
| `l8-modes-of-convergence` | Ways random variables converge | Tell almost sure, in probability, in mean square and in distribution apart. | `mt-integral` |

#### measure-prob level 3: Information and martingales

- **Prerequisites:** measure-prob L2; markov L5.
- **Builds on:** random-vars l15-given-information, l16-averaging-averages; least-squares l5-dropping-a-perpendicular; markov l17-fair-bets, l19-optional-stopping; ito l8-fair-games.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l9-information` | A sigma-algebra as information | Read a sigma-algebra as what is known, using a coin-flip tree. | `mt-condexp` |
| `l10-condexp-projection` | Conditional expectation as a projection | Define conditional expectation as a projection and prove the tower property. | `mt-condexp` |
| `l11-filtrations` | Filtrations | Model information that grows over time with a filtration, and tell adapted from predictable. | `mt-condexp`, `mt-martingale` |
| `l12-martingales-defined` | Martingales defined properly | Prove a process is a martingale with respect to a filtration. | `mt-martingale` |
| `l13-stopping-times` | Stopping times and optional stopping proved | Prove the optional stopping theorem under bounded stopping times. | `mt-martingale` |

#### measure-prob level 4: Changing measure

- **Prerequisites:** measure-prob L3; ito L3.
- **Builds on:** trees l3-risk-neutral; ito l10-changing-measure, l11-prices-as-expectations; estimation l5-which-fits.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-radon-nikodym` | The Radon-Nikodym derivative | Reweight a probability with a density and compute expectations under the new measure. | `mt-change` |
| `l15-likelihood-ratios` | Likelihood ratios as changes of measure | Use a likelihood ratio for importance sampling of a rare loss. | `mt-change` |
| `l16-girsanov-on-a-tree` | Girsanov on a binomial tree | Change the up probability on a tree and track the drift it removes. | `mt-change`, `mt-martingale` |
| `l17-risk-neutral-rigorous` | The risk-neutral measure made rigorous | Show that discounted prices are martingales under the risk-neutral measure. | `mt-change`, `mt-martingale` |

### pdes (topic 3.2): Partial Differential Equations

- **Strand:** `quant`. Desk quant and derivatives pricing.
- **Hours:** optional, hours not counted. 3 levels, 12 lessons, 3 reviews and 3 homework sets.
- **Art:** `surface`. **Skills:** `pe-heat` The heat equation; `pe-fourier` Fourier series and separation; `pe-bs` Black-Scholes as a heat equation; `pe-fk` Feynman-Kac; `pe-fd` Finite-difference solution.

#### pdes level 1: The heat equation

- **Prerequisites:** odes (all levels); ito L3.
- **Builds on:** multivar l3-second-partials; limits-thm l7-bell-curve; ito l2-normal-increments; vector-calc l5-divergence-and-curl.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-equations-in-two-variables` | Equations in two variables | Classify a partial differential equation by order and type. | `pe-heat` |
| `l2-heat-equation` | The heat equation | Derive the heat equation from a random walk and check a solution. | `pe-heat` |
| `l3-heat-kernel` | The heat kernel | Solve the heat equation on the line with the heat kernel, a normal density. | `pe-heat` |
| `l4-boundary-conditions` | Initial and boundary conditions | Pose a well-posed problem with initial and boundary conditions. | `pe-heat` |

#### pdes level 2: Separation and Fourier series

- **Prerequisites:** pdes L1; complex L1.
- **Builds on:** odes l2-separable, l7-characteristic-equation; trig l13-modelling-a-cycle; complex l3-euler.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-separation-of-variables` | Separation of variables | Split a partial differential equation into two ordinary ones by separation of variables. | `pe-fourier` |
| `l6-fourier-series` | Fourier series | Compute a function’s Fourier coefficients and plot partial sums. | `pe-fourier` |
| `l7-when-fourier-converges` | When a Fourier series converges | See where a Fourier series converges and the overshoot at a jump. | `pe-fourier` |
| `l8-heat-on-a-rod` | Heat on a rod, solved | Solve the heat equation on an interval with a Fourier series. | `pe-fourier`, `pe-heat` |

#### pdes level 3: Pricing equations

- **Prerequisites:** pdes L2; numerics L4.
- **Builds on:** ito l9-bs-pde, l11-prices-as-expectations; trees l10-black-scholes; numerics l13-finite-differences, l14-implicit-and-crank-nicolson.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l9-black-scholes-to-heat` | Turning Black-Scholes into the heat equation | Change variables to turn the Black-Scholes equation into the heat equation. | `pe-bs` |
| `l10-formula-from-the-kernel` | The Black-Scholes formula from the heat kernel | Recover the Black-Scholes formula by solving the heat equation with the heat kernel. | `pe-bs`, `pe-heat` |
| `l11-feynman-kac` | Expectations solve equations | Use Feynman-Kac to write a pricing equation’s solution as an expectation, and check it by simulation. | `pe-fk` |
| `l12-four-decimal-pricer` | A finite-difference pricer to four decimals | Match a Crank-Nicolson price to the closed form to four decimal places. | `pe-fd`, `pe-bs` |

### algebra (topic 3.4): Abstract Algebra

- **Strand:** `pure`. Not needed to be hired. Modular arithmetic and permutations come up at interview.
- **Hours:** optional, hours not counted. 4 levels, 17 lessons, 4 reviews and 4 homework sets.
- **Art:** `table`. **Skills:** `ag-groups` Groups; `ag-cosets` Subgroups and cosets; `ag-perm` Permutations; `ag-hom` Homomorphisms and quotients; `ag-rings` Rings and fields; `ag-poly` Polynomials over a field.

#### algebra level 1: Groups

- **Prerequisites:** proof (all levels); linear-maps L2.
- **Builds on:** contests l5-modulo, l6-gcd-and-primes; vectors l7-one-after-another; trig l12-adding-angles; complex l4-roots-of-unity.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-symmetries` | Symmetries that combine | Combine the symmetries of a square and see that they form a group. | `ag-groups` |
| `l2-group-axioms` | The group axioms | Check the group axioms and prove that identities and inverses are unique. | `ag-groups` |
| `l3-modular-arithmetic` | Arithmetic modulo n | Work modulo $n$ and find which residues have inverses. | `ag-groups` |
| `l4-cyclic-groups` | Cyclic groups and order | Find the order of an element and the generators of a cyclic group. | `ag-groups` |

#### algebra level 2: Inside a group

- **Prerequisites:** algebra L1.
- **Builds on:** counting l2-arranging; puzzles l5-hats; contests l8-invariants; elimination l10-computing-dets (sign of a permutation).

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-subgroups` | Subgroups | Prove a subset is a subgroup with the one-step test. | `ag-cosets` |
| `l6-cosets` | Cosets | List the cosets of a subgroup and prove that they split the group into equal pieces. | `ag-cosets` |
| `l7-lagrange` | Lagrange’s theorem | Prove Lagrange’s theorem and use it to rule out subgroup sizes. | `ag-cosets` |
| `l8-permutations-and-cycles` | Permutations and cycles | Write a permutation in cycle notation and find its order. | `ag-perm` |
| `l9-odd-and-even` | Odd and even permutations | Find a permutation’s sign, and show why the 15-puzzle cannot always be solved. | `ag-perm` |

#### algebra level 3: Maps between groups

- **Prerequisites:** algebra L2.
- **Builds on:** linear-maps l6-kernel-and-image, l9-invertible-and-isomorphic; contests l7-counting-mod; exp-log l6-products-into-sums.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l10-homomorphisms` | Homomorphisms | Prove a map is a homomorphism and find its kernel. | `ag-hom` |
| `l11-normal-subgroups` | Normal subgroups and quotients | Tell when a subgroup is normal and build the quotient group. | `ag-hom`, `ag-cosets` |
| `l12-first-isomorphism-theorem` | The first isomorphism theorem | Prove the first isomorphism theorem and use it to identify a quotient. | `ag-hom` |
| `l13-fermat-and-euler` | Fermat and Euler from Lagrange | Prove Fermat’s little theorem and Euler’s theorem from Lagrange’s theorem. | `ag-cosets`, `ag-groups` |

#### algebra level 4: Rings and fields

- **Prerequisites:** algebra L3.
- **Builds on:** quadratics l2-product-and-sum, l5-product-of-zero; contests l5-modulo; linear-maps l1-axioms.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l14-rings` | Rings | Check the ring axioms for the integers, matrices and residues modulo $n$. | `ag-rings` |
| `l15-fields` | Fields and finite fields | Prove that the integers modulo a prime form a field. | `ag-rings` |
| `l16-polynomials` | Polynomials over a field | Add, multiply and divide polynomials with coefficients in a field. | `ag-poly` |
| `l17-roots-and-factors` | Roots, factors and irreducibles | Use the factor theorem and test small polynomials for irreducibility. | `ag-poly`, `ag-rings` |

### topology (topic 3.4): Metric and Topological Spaces

- **Strand:** `pure`. Not needed to be hired. Fixed-point arguments in research papers.
- **Hours:** optional, hours not counted. 3 levels, 13 lessons, 3 reviews and 3 homework sets.
- **Art:** `circle`. **Skills:** `tg-metric` Metric spaces; `tg-open` Open sets and topologies; `tg-continuity` Continuity; `tg-connected` Connectedness; `tg-compact` Compactness; `tg-complete` Completeness and contraction.

#### topology level 1: Metric spaces revisited

- **Prerequisites:** analysis (all levels).
- **Builds on:** analysis l22-metric-spaces, l23-open-and-closed, l15-epsilon-delta; vectors l3-lengths-angles.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l1-many-distances` | Many ways to measure distance | Compare Euclidean, taxicab and maximum metrics, and draw their unit balls. | `tg-metric` |
| `l2-open-balls` | Open balls and open sets | Prove that open balls are open and that unions of open sets are open. | `tg-metric`, `tg-open` |
| `l3-closure-interior-boundary` | Closure, interior and boundary | Find the closure, interior and boundary of a set. | `tg-open` |
| `l4-continuity-by-open-sets` | Continuity through open sets | Prove that a map is continuous exactly when preimages of open sets are open. | `tg-continuity` |

#### topology level 2: Topological spaces

- **Prerequisites:** topology L1.
- **Builds on:** proof l9-one-to-one-onto; analysis l16-intermediate-value.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l5-topologies` | Topologies without distance | Check the topology axioms, including spaces with no metric. | `tg-open` |
| `l6-bases-and-subspaces` | Bases and subspaces | Build a topology from a basis and give a subset the subspace topology. | `tg-open` |
| `l7-homeomorphisms` | Homeomorphisms | Prove two spaces are homeomorphic, or find a property that tells them apart. | `tg-continuity` |
| `l8-connectedness` | Connectedness | Prove that intervals are connected, and derive the intermediate value theorem from it. | `tg-connected` |

#### topology level 3: Compact and complete

- **Prerequisites:** topology L2; numerics L2.
- **Builds on:** analysis l10-cauchy, l24-compactness; taylor l3-newton; numerics l5-bisection-and-newton.

| Id | Name | Objective | Skills |
| --- | --- | --- | --- |
| `l9-open-covers` | Compactness by open covers | Prove a set is compact with open covers, and prove Heine-Borel on the line. | `tg-compact` |
| `l10-compact-images` | Continuous images of compact sets | Prove that a continuous image of a compact set is compact. | `tg-compact`, `tg-continuity` |
| `l11-complete-spaces` | Complete metric spaces | Prove a space is complete, or find a Cauchy sequence with no limit in it. | `tg-complete` |
| `l12-contraction-mapping` | The contraction mapping theorem | Prove the contraction mapping theorem without notes. | `tg-complete` |
| `l13-fixed-point-iteration` | A fixed-point iteration that converges | Use the contraction mapping theorem to show a fixed-point iteration converges, and bound its error. | `tg-complete` |

## Levels for PLAN.md

One line per level, Stage 0, 1, 2, 3 order, and by topic number within a stage. Every required prerequisite comes earlier in this list; linear-maps L4 names complex L1 as helpful only.

- [ ] proof L1: Statements and logic [Pure maths]
- [ ] proof L2: Sets and functions [Pure maths]
- [ ] proof L3: Proof methods [Pure maths]
- [ ] markov L5: Martingales and stopping [Quant]
- [ ] analysis L1: The real numbers [Pure maths]
- [ ] analysis L2: Sequences [Pure maths]
- [ ] analysis L3: Series [Pure maths]
- [ ] analysis L4: Continuity and the derivative [Pure maths]
- [ ] analysis L5: Integration and metric spaces [Pure maths]
- [ ] linear-maps L1: Vector spaces [Pure maths]
- [ ] linear-maps L2: Linear maps [Pure maths]
- [ ] linear-maps L3: Duality and inner products [Pure maths]
- [ ] linear-maps L4: Operators [Pure maths]
- [ ] complex L1: The complex plane [Quant]
- [ ] complex L2: Complex functions [Quant]
- [ ] complex L3: Integrals and Fourier [Quant]
- [ ] vector-calc L1: Fields and line integrals [Pure maths]
- [ ] vector-calc L2: Green’s theorem [Pure maths]
- [ ] vector-calc L3: Surfaces and space [Pure maths]
- [ ] odes L1: First-order equations [Quant]
- [ ] odes L2: Second-order equations [Quant]
- [ ] odes L3: Systems and stability [Quant]
- [ ] odes L4: Transforms and numerical solution [Quant]
- [ ] numerics L1: Errors [Quant]
- [ ] numerics L2: Equations and curves [Quant]
- [ ] numerics L3: Integrals and time steps [Quant]
- [ ] numerics L4: One option, three ways [Quant]
- [ ] convex L1: Convexity [Quant]
- [ ] convex L2: Linear programmes [Quant]
- [ ] convex L3: Duality and KKT [Quant]
- [ ] convex L4: Algorithms [Quant]
- [ ] stat-models L1: Generalised linear models [Quant]
- [ ] stat-models L2: Experiments [Quant]
- [ ] stat-models L3: Without the assumptions [Quant]
- [ ] stat-models L4: Bayesian models [Quant]
- [ ] measure-prob L1: Measures [Quant]
- [ ] measure-prob L2: Integration [Quant]
- [ ] measure-prob L3: Information and martingales [Quant]
- [ ] measure-prob L4: Changing measure [Quant]
- [ ] pdes L1: The heat equation [Quant]
- [ ] pdes L2: Separation and Fourier series [Quant]
- [ ] pdes L3: Pricing equations [Quant]
- [ ] algebra L1: Groups [Pure maths]
- [ ] algebra L2: Inside a group [Pure maths]
- [ ] algebra L3: Maps between groups [Pure maths]
- [ ] algebra L4: Rings and fields [Pure maths]
- [ ] topology L1: Metric spaces revisited [Pure maths]
- [ ] topology L2: Topological spaces [Pure maths]
- [ ] topology L3: Compact and complete [Pure maths]

## Engine notes

- **`strand` and `strandNote` are accepted.** `node tools/validate.mjs` reports 0 errors with both fields present; it does not check unknown course.json fields. No error text to record.
- The app does not read either field yet (`grep strand app/js` finds nothing). An engine agent may want to show the strand tag and roles on the course card and topic header.
- `js/screens/learn.js` counts every non-optional topic towards a stage's "topics passed". Topics 0.6 and 1.10 are pure maths with hours, so they would count towards the quant path. A topic-level strand, or reading the courses' strand, would let the app leave them out.
- The validator does not require a topic exam, so the six new topics validate without one; `learn.js` shows an exam chip for them that has nothing behind it until topic exams exist.

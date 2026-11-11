# Claim ledger: limits-thm levels 1 to 3 (round 1, blind)

Stage 1 course, full ledger. Each row was judged on its own. 368 rows: 335 correct, 26 imprecise, 5 misleading, 2 wrong, 0 unverified. "finding N" refers to `docs/reviews/audit-limits-thm-1-3.md`. Sources: C&B = Casella and Berger, *Statistical Inference* (2nd ed.); Ross = Ross, *A First Course in Probability*; Feller = Feller, *An Introduction to Probability Theory and Its Applications*, vol. 1; Durrett = Durrett, *Probability: Theory and Examples*; Hull = Hull, *Options, Futures and Other Derivatives*; Lo = Lo (2002), "The Statistics of Sharpe Ratios"; Cont = Cont (2001), "Empirical properties of asset returns: stylized facts". "script" = a named check in `docs/reports/limits-thm-L1-3-concepts.py`. "deriv." = derivation given in the row. Paths use `s[i]` for `screens[i]`, `q[i]` for `quiz[i]`, `it[i]` for `items[i]`.

| # | File | Path | Claim (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l1 | s[1].explain | Three one-win paths, each 0.6 × 0.4² = 0.096 | correct | deriv.: commutativity of the product |
| 2 | l1 | s[1].wrong one-order, at-most | Slips: one path only; includes LLL | correct | sets match the stated slips |
| 3 | l1 | s[2] table | P(X=k) = paths × one path: 0.064, 0.288, 0.432, 0.216 | correct | sums to 1; C&B 3.2 |
| 4 | l1 | s[2].hints[0] | Paths are disjoint outcomes so chances add | correct | additivity axiom |
| 5 | l1 | s[3].prose | Wins in n independent trials with chance p are Bin(n, p) | correct | C&B Def. 3.2.2 |
| 6 | l1 | s[3] key and why lines | p = 0.5 gives symmetry about n/2; small p leans to 0; counts not equally likely | correct | pmf symmetric iff p = 0.5 (k ↔ n−k) |
| 7 | l1 | s[3].explain | p above 0.5 moves bulk right with a left tail | correct | skewness (1−2p)/√(npq) |
| 8 | l1 | s[4] key 10, wrong 5, 60, 3 | C(5,3) = 10; 60 = ordered picks | correct | 5·4·3/3! = 10 |
| 9 | l1 | s[4].explain | P(X=3) = 10 × 0.03456 = 0.3456 | correct | arithmetic |
| 10 | l1 | s[5] key 0.375 and options | 6 paths × 0.0625; 0.125 = two paths; 0.5 = share | correct | C(4,2)/16 |
| 11 | l1 | s[6] order | One path, same chance, count, add gives the pmf | correct | C&B 3.2 |
| 12 | l1 | s[6].explain | Conditions: fixed n, independent trials, same p | correct | definition of Bernoulli trials |
| 13 | l1 | s[7].prose | X = sum of indicators; E[X] = 20p by linearity; Var(I) = p(1−p) | correct | Ross 7.2 |
| 14 | l1 | s[7] key, wrong 400p(1−p) | Var(X) = 20p(1−p); 400p(1−p) is Var(20 I₁) | correct | Var(cY) = c²Var(Y) |
| 15 | l1 | s[7].explain | Independence makes covariances zero; without it the sum is wrong | correct | Var(ΣI) = ΣVar + ΣCov; "this sum is wrong" read as "need not hold" |
| 16 | l1 | s[8] key 2.225, wrong 4.95, 11, 3.317 | sd = √4.95 | correct | recomputed |
| 17 | l1 | s[8].explain | 9 or 13 wins is ordinary noise | correct | within 1 sd of 11 |
| 18 | l1 | s[9] solution and tests | pmf list; tail from 15 is 0.0553; edge p = 0, 1 | correct | script l1 s9; Python 0.0**0 = 1.0 |
| 19 | l1 | s[9].explain | 15 wins about once in 18 weeks | correct | 1/0.0553 = 18.1 |
| 20 | l1 | s[10] key 0.3642, wrong 0, 0.98, 0.02 | 0.98⁵⁰ | correct | script |
| 21 | l1 | s[10].explain | Recession breaks independence; many-default years likelier than binomial | correct | positive default correlation fattens tail (Hull ch. 24) |
| 22 | l1 | summary.trap | Multiply by C(n,k); trials must be independent | correct | as rows 11, 12 |
| 23 | l1 | q[0] key 0.25 | 4 × 1/16 | correct | recomputed |
| 24 | l1 | q[1] key and why lines | Shared stock breaks independence; same p not enough | correct | definition |
| 25 | l1 | q[1].explain | "X is often 0 or 10" | imprecise | overstated: dependence raises mass near the ends, not at exactly 0 or 10 "often"; finding 23 |
| 26 | l1 | q[2] key 21, wrong 30, 4.583, 70 | npq | correct | recomputed |
| 27 | l1 | q[3] key p = 0.5 | p(1−p) peaks at 0.5 | correct | calculus |
| 28 | fluency-l1 | families[0] | key C(n,k)p^k q^(n−k); slips one path, swapped p and q, guarded when equal | correct | guards `abs(key − …) > 0.0002` cover p = 0.5 and n = 2k |
| 29 | fluency-l1 | families[1] | Var = npq; slips mean, one trial | correct | recomputed for n = 10, p = 0.3 |
| 30 | fluency-l1 | families[2] | none succeed = qⁿ; slips pⁿ, 1 − pⁿ | correct | p = 0.5 excluded so pⁿ ≠ qⁿ |
| 31 | l2 | s[1] key 0.128, wrong 0.2, 0.008, 0.6, 0.488 | first fill in minute 3 = 0.8²·0.2 | correct | recomputed |
| 32 | l2 | s[2] key and explain | Minute 1 is the mode for every p; bars fall by factor 1−p | correct | pmf ratio 1−p < 1 for p > 0 |
| 33 | l2 | s[2] why "mean" | Mean exceeds mode because of long waits | correct | 1/p ≥ 1 |
| 34 | l2 | s[3].prose | P(X=k) = (1−p)^(k−1)p, trials convention, Geo(p) | correct | C&B 3.2 geometric; convention named in s[6] |
| 35 | l2 | s[3] key 0.512, wrong 0.488, 0.4096, 0.128 | P(X>3) = 0.8³ | correct | recomputed |
| 36 | l2 | s[3].explain | P(X>m) = (1−p)^m | correct | m failures |
| 37 | l2 | s[4] key 0.512; options 0.328, 0.64, 0.21 | conditional = ratio | correct | 0.8⁵/0.8² ; 0.328×0.64 = 0.21 |
| 38 | l2 | s[4].explain | Memoryless property P(X>m+n given X>m) = P(X>n) | correct | C&B p. 97 |
| 39 | l2 | s[5] key 0.2 and options | Gambler's fallacy; 0.027 is unconditional P(X=10) | correct | 0.8⁹·0.2 = 0.0268 |
| 40 | l2 | s[5].explain | "If fills get likelier, the minutes are not independent" | imprecise | a changing per-minute chance with independent minutes also breaks the model; finding 22 |
| 41 | l2 | s[6] key 0.128, wrong 0.16 | Failures convention Y = X − 1; P(Y=k) = q^k p | correct | C&B p. 97 alternative form |
| 42 | l2 | s[6].explain | Both called geometric; check which a library means | correct | scipy.stats.geom counts trials, numpy too; R dgeom counts failures |
| 43 | l2 | s[7].prose and key 1/p | First-step conditioning; E[X] = p + (1−p)(1+E[X]) | correct | Ross 7.5; assumes E[X] finite, shown by the series in s[8] |
| 44 | l2 | s[7] wrong p, (1−p)/p, 1/(1−p) | slips as described | correct | (1−p)/p = E[X] − 1 |
| 45 | l2 | s[8] order and explain | S − qS = 1/(1−q); S = 1/p² | correct | absolutely convergent for 0 ≤ q < 1 |
| 46 | l2 | s[9] key 20, wrong 19, 5, 0.05 | 1/0.05 | correct | recomputed |
| 47 | l2 | s[9].explain | Twenty no-edge variants give one lucky pass on average | correct | 20 × 0.05 = 1 |
| 48 | l2 | s[10] key 0.4013, wrong 0.5, 0.5987, 0.0315 | 1 − 0.95¹⁰ | correct | script |
| 49 | l2 | summary | pmf, tail, mean; failures shift by 1 | correct | rows 34 to 44 |
| 50 | l2 | q[0] 25/216 | (5/6)²(1/6) | correct | 0.1157 |
| 51 | l2 | q[1] | p = 1: X = 1 surely; formula does not break | correct | pmf at p = 1 |
| 52 | l2 | q[2] key (5/6)⁶; options | memoryless; 0.162, 0.694 | correct | recomputed |
| 53 | l2 | q[3] key 3 | E[Y] = (1−p)/p | correct | 0.75/0.25 |
| 54 | l3 | s[1] key 0.1074; wrong values | 0.8¹⁰; 0.2¹⁰ = 1.024e−7 | correct | recomputed |
| 55 | l3 | s[2] key and explain | (1−2/n)ⁿ → e⁻²; 0.1299 at 50, 0.1348 at 500 | correct | script l3 s2 |
| 56 | l3 | s[3].prose | Poisson pmf; counts rare independent events in a window; λ the mean | correct | C&B 3.2 Poisson; Feller VI.5 |
| 57 | l3 | s[3] key 0.2707, wrong 0.302, 0.5413, 0.1353 | e⁻²·4/2 | correct | recomputed; Bin(10,.2) P(2) = 0.3020 |
| 58 | l3 | s[3].explain | Bin(500, .004) gives 0.2712; P(1) = P(2) at λ = 2 | correct | script l3 s3 |
| 59 | l3 | s[4] key 0.2231, wrong 0.3347, 0.3679, 0 | e^(−1.5) | correct | recomputed |
| 60 | l3 | s[4].explain | P(no event) = e^(−λ) always | correct | pmf at 0 |
| 61 | l3 | s[5].prose | Var of Bin(n, 2/n) is 2(1−2/n): 1.6, 1.992 | correct | recomputed |
| 62 | l3 | s[5].explain | "As n → ∞ the variance tends to 2. So a Poisson has variance λ" | imprecise | limit in distribution does not by itself carry the variance (Billingsley Thm 25.12 needs uniform integrability); true here, but the step is a heuristic; finding 21 |
| 63 | l3 | s[5] wrong 0, 1.6, 1.414 | slips as described | correct | recomputed |
| 64 | l3 | s[6] key 1 − e^(−0.5) and options | rate is not a probability | correct | 0.3935; 0.5e^(−0.5) = 0.3033 |
| 65 | l3 | s[6].explain | Chance of at least one is below λ; a rate can exceed 1 | correct | 1 − e^(−λ) < λ for λ > 0 |
| 66 | l3 | s[7] order | Law of rare events derivation, k fixed | correct | C&B Example 2.3.13 / Feller VI.5 |
| 67 | l3 | s[7].explain | C(n,k)/n^k → 1/k! | correct | n(n−1)…(n−k+1)/n^k → 1 |
| 68 | l3 | s[8] key 0.0839, wrong 0.9161, 0.0504, 0.1008 | Pois(3) tail | correct | script l3 s8 |
| 69 | l3 | s[9] key and options | Variance 6.1 against mean 2 rules out Pois(2); Poisson has variance equal to mean | correct | C&B 3.2; dispersion test 249 × 6.1/2 = 759 on 249 df |
| 70 | l3 | s[9].hints[2], explain | Variance above mean means bursts, not independent arrivals; 4 days expected, 21 seen | correct | a day-to-day varying rate (mixed Poisson) is itself dependence between counts; script l3 s9 |
| 71 | l3 | summary | λ fixed, many tiny chances; variance equal to mean; overdispersion signals clustering | correct | rows 56, 66, 69 |
| 72 | l3 | q[0] key 0.0183; once in 55 days | e⁻⁴ | correct | 1/0.0183 = 54.6 |
| 73 | l3 | q[1] key 2.5; "limit of np(1−p) with p → 0" | Var = λ | correct | C&B 3.2 (direct sum) |
| 74 | l3 | q[2] key 0.2707; exact agrees to 4 dp | λ = np = 2 | correct | script l3 quiz2 |
| 75 | l3 | q[3] key 0.3679, wrong 0.0498, 0.0166, 0.6667 | scale λ to the window | correct | Poisson process: N(t) ~ Pois(λt), Ross 9.1 |
| 76 | l4 | s[1] tree leaves | Path chances 1/30, 1/10, 1/6 | correct | recomputed fractions |
| 77 | l4 | s[1].explain | Branch chances differ, products equal | correct | exchangeability of draws |
| 78 | l4 | s[2] key 0.3, wrong 0.1, 0.288, 0.4 | 3 × 72/720 | correct | recomputed |
| 79 | l4 | s[3] derive formulas | Hypergeometric via falling factorials, K = 0.2N | correct | checked at N = 20: 0.2817 |
| 80 | l4 | s[3] key and explain | Binomial is good when population is large against the sample | correct | C&B p. 87; hypergeometric → binomial as N → ∞ |
| 81 | l4 | s[4] key 36, wrong 6, 72, 120, 12 | C(4,2)C(6,1) | correct | recomputed |
| 82 | l4 | s[4].explain | Hypergeometric pmf | correct | C&B 3.2.1 |
| 83 | l4 | s[5] key 1; explain | E[X] = nK/N by symmetry and linearity; no independence needed | correct | Ross 7.2 Example 2g |
| 84 | l4 | s[6] key 0.6316; wrong 0.8, 0.6, 0.7895 | variance factor (N−n)/(N−1) | correct | C&B (3.2.3); recomputed |
| 85 | l4 | s[6].explain | Draws negatively correlated | correct | Cov = −p(1−p)/(N−1) (hw1 it[8]) |
| 86 | l4 | s[7] key 0.2817 and options | all-clean samples C(16,5)/C(20,5) | correct | script l4 s7 |
| 87 | l4 | s[7].explain | "Each factor is below 0.8" | wrong | the first factor is 16/20 = 0.8 exactly; script l4 s7 CLAIM; finding 1 |
| 88 | l4 | s[8] order | Counting derivation of the pmf | correct | C&B 3.2.1 |
| 89 | l4 | s[9] table and key | 0.2817, 0.3193, 0.3269; only N = 1000 within 0.001 | correct | script l4 s9 |
| 90 | l4 | s[9].explain | "A common rule: sample under about 5% of the population" | correct | stated as a rule of thumb; 5% to 10% both in use (survey sampling fpc convention) |
| 91 | l4 | s[10] solution, tests | hyper_pmf; tail 0.1096; mean 2 | correct | script l4 s10 |
| 92 | l4 | s[10].explain | Bin(10, .2) gives 0.1209, too high | correct | script |
| 93 | l4 | summary | mean nK/N; variance smaller by (N−n)/(N−1) | correct | rows 83, 84 |
| 94 | l4 | q[0] key 0.2995, wrong 0.2792, 0.0769 | one ace in five cards | correct | script l4 quiz0 |
| 95 | l4 | q[1] | n = N: X = K, variance 0 | correct | factor 0 |
| 96 | l4 | q[2].explain | "No replacement is needed for the mean" | imprecise | reads as a condition on sampling; the point is that the mean is the same with or without replacement; finding 24 |
| 97 | l4 | q[3] key and why lines | 20 of 50,000 safest; 50 of 100 gives factor about 0.5 | correct | 50/99 = 0.505 |
| 98 | review-1 | it[0] 0.3125 | C(6,3)/64 | correct | recomputed |
| 99 | review-1 | it[1] 0.2401, wrong 0.1681, 0.7599, 0.1029 | 0.7⁴ | correct | recomputed |
| 100 | review-1 | it[2] 0.2873 | 3.5e^(−2.5) | correct | recomputed |
| 101 | review-1 | it[3] key and options | 0.2743 hypergeometric; 0.2637 binomial | correct | 712,842/2,598,960 |
| 102 | review-1 | it[4] | Trials to first success is geometric; why lines for the other three | correct | definitions |
| 103 | review-1 | it[5] 0.1353; exact 0.1340 | Poisson approximation, λ = 2 | correct | 0.99²⁰⁰ = 0.1340 |
| 104 | review-1 | it[6] 9; "conventions always differ by exactly 1" | E[Y] = 1/p − 1 | correct | Y = X − 1 |
| 105 | review-1 | it[7] 1.3061, wrong 1.6, 1.28, 2 | 1.6 × 40/49 | correct | recomputed |
| 106 | homework-1 | it[0] 0.2642 and wrongs | 1 − P(0) − P(1) | correct | recomputed |
| 107 | homework-1 | it[1] order; explain | E[X] = λ; E[X(X−1)] = λ² so Var = λ | correct | C&B Example 2.2.x / 3.2 |
| 108 | homework-1 | it[2] 8; wrong 5, 7, 3 | E[X given X > 3] = 3 + 1/p | correct | memorylessness |
| 109 | homework-1 | it[3] 0.6065, wrong 0.0498, 0.5, 0.0083 | λ = 0.5 for ten minutes | correct | recomputed |
| 110 | homework-1 | it[4] 0.6894; binomial 0.6513 understates | hypergeometric complement | correct | script hw1 item4 |
| 111 | homework-1 | it[5] 2/p; wrongs | negative binomial mean r/p | correct | C&B 3.2 negative binomial |
| 112 | homework-1 | it[6] key and why lines | Variance 15 against 3.92: positive covariance between loans; Poisson no better | correct | Var(ΣI) = npq + n(n−1)Cov |
| 113 | homework-1 | it[7] 0.7361; note that dropping C(10,1) gives 0.3874 | 0.9¹⁰ + 0.9⁹ | correct | 0.9⁹(0.9 + 0.1) = 0.9⁹ = 0.3874 |
| 114 | homework-1 | it[8].model 1 to 3 | Cov(Iᵢ, Iⱼ) = −p(1−p)/(N−1); Var = npq(N−n)/(N−1) | correct | algebra rechecked line by line |
| 115 | homework-1 | it[8].model 4 | 0.6316 two ways; pmf 0.2817, 0.4696, 0.2167, 0.0310, 0.0010 | correct | script hw1 item8 |
| 116 | homework-1 | it[9].model (a) | T = min(X, m): P(T=k) = q^(k−1)p, P(T=m) = q^(m−1) | correct | deriv. |
| 117 | homework-1 | it[9].model (b), (c) | E[T] = (1 − q^m)/p by recursion and by series | correct | script hw1 item9 |
| 118 | homework-1 | it[9].model (d) | cancel chance 0.85¹⁰ = 0.1969, not 0.85⁹; E[T] = 5.354; limit 1/p | correct | script |
| 119 | l5 | s[0] key 0.75, wrongs | area under x/8 from 2 to 4 | correct | (16 − 4)/16 |
| 120 | l5 | s[1] key 0 and why lines | P(X = 3) = 0 for a density | correct | C&B Thm 1.5.x; areas 0.075, 0.0075 recomputed |
| 121 | l5 | s[1].explain | X still takes some value; chance lives in intervals | correct | uncountable additivity is not required |
| 122 | l5 | s[2] key c = 1/8 | total area 8c = 1 | correct | recomputed |
| 123 | l5 | s[2].explain | The rule is about area, never height | correct | C&B Thm 1.6.5 |
| 124 | l5 | s[3] key x²/16; explain | CDF; F′ = f by the fundamental theorem; P(a ≤ X ≤ b) = F(b) − F(a) | correct | holds where f is continuous; C&B 1.6 |
| 125 | l5 | s[4] key 8/3, wrongs; explain | E[X] = ∫x f; E[X²] = 8; Var = 8/9 | correct | recomputed |
| 126 | l5 | s[5] key 0.2 and options | density 4 on [0, 0.25] is valid | correct | area 1 |
| 127 | l5 | s[5].explain | A density is chance per unit of x | correct | f(x) = lim P(x < X < x+h)/h |
| 128 | l5 | s[6].prose | f ≥ 0, ∫f = 1, F′ = f, E[X] = ∫x f | correct | C&B 1.6, 2.2 |
| 129 | l5 | s[6] options | x/2 valid; x has area 2; 1 − x negative; x²/2 has area 4/3 | correct | recomputed |
| 130 | l5 | s[7] order | P(X = a) ≤ Mh → 0 when f ≤ M near a | correct | deriv.; hypothesis stated |
| 131 | l5 | s[7].explain | Open and closed intervals have equal chance | correct | endpoints have probability 0 |
| 132 | l5 | s[8] key 7.764, wrongs 9.5, 2.236, 5 | VaR as tail-area cut-off, loss convention | correct | (10 − v)²/100 = 0.05; Hull 22.1 |
| 133 | l5 | s[8].explain | Discrete VaR counts worst days; continuous solves a tail area | correct | quantile definition |
| 134 | l5 | s[9] key 0.2083, wrongs 0, 0.625, 0.125, 1.6667 | E[max(S − 105, 0)] | correct | ∫₀⁵ u(5−u)/100 du = 125/600 |
| 135 | l5 | s[9] why at-mean | Average of payoff is not payoff at the average | correct | Jensen, convex payoff |
| 136 | l5 | summary | endpoints make no difference; height is not a chance | correct | rows 120, 131 |
| 137 | l5 | q[0] 0.125; q[1] 3x²; q[2]; q[3] 1/18 | density drills | correct | recomputed; 2/3 − 4/9 = 0.2222 slip |
| 138 | l6 | s[0] key 0.3; explain | uniform chance is share of width | correct | C&B 3.3 |
| 139 | l6 | s[1] key 1/20 | height 1/(b − a) | correct | area 1 |
| 140 | l6 | s[2] order; explain | Var U(a, b) = (b − a)²/12; sd 2.89 for U(0, 10) | correct | w²/3 − w²/4 |
| 141 | l6 | s[3].prose | "Trades arrive at random, on average λ per minute", so the wait is exponential | imprecise | needs a Poisson process (independent increments, constant rate), not only an average rate; finding 16 |
| 142 | l6 | s[3] key 0.1353, wrongs | e⁻² | correct | recomputed |
| 143 | l6 | s[4] key e^(−2t); explain | survival function, CDF 1 − e^(−λt) | correct | C&B 3.3 exponential |
| 144 | l6 | s[5].prose | E[T] = 1/λ by parts | correct | hw2 it[2] |
| 145 | l6 | s[5] key e⁻¹ and why lines | P(T > mean) = e⁻¹; mean above median | correct | median ln 2/λ |
| 146 | l6 | s[5].explain | median 0.3466 minute, about 21 seconds | correct | 20.8 s |
| 147 | l6 | s[6] key e⁻¹ and options | memoryless conditional | correct | script MC l6 s6 |
| 148 | l6 | s[6].explain | "No trade is ever overdue" | correct | within the constant-rate model, as the screen states |
| 149 | l6 | s[7].prose, order | Memorylessness proof; geometric is the discrete twin | correct | C&B p. 101 |
| 150 | l6 | s[8].prose | In a Poisson process at rate λ the gaps are exponential with rate λ | correct | Ross 9.1 |
| 151 | l6 | s[8] key 1/3 second | mean gap 1/λ | correct | row 144 |
| 152 | l6 | s[9].prose, key 0.9048, wrongs 0.9, 0.9039, 0.0952 | constant hazard gives exponential survival | correct | Hull 24.1: survival e^(−λt) |
| 153 | l6 | s[9].explain | "the hazard rate … the default chance per year for an issuer still alive" | imprecise | a hazard is a rate per unit time, not a yearly probability (1 − e^(−0.02) = 0.0198); the course's own Poisson trap separates the two; finding 17 |
| 154 | l6 | s[9] why linear, annual | 1 − 0.1 and 0.98⁵ slips | correct | recomputed |
| 155 | l6 | s[10].prose | "Knowing only the range, the honest choice is the uniform" | misleading | principle of indifference stated as a rule; maximum entropy is a convention (Jaynes), not parametrisation-free; finding 26 |
| 156 | l6 | s[10] key 2.309, wrongs | sd 8/√12 | correct | recomputed |
| 157 | l6 | s[10].explain | Uniform is the maximum-ignorance density; "any other shape would claim knowledge we lack" | misleading | true as a maximum-entropy statement (Cover and Thomas ch. 12); presented as the only defensible model; finding 26 |
| 158 | l6 | summary.ideas[0] | Uniform "is the density to use when you know only the range" | misleading | as row 155; finding 26 |
| 159 | l6 | summary.ideas[1], [2] | Exponential is the Poisson-process wait; memoryless | correct | rows 149, 150 |
| 160 | l6 | q[0] 4/3; wrongs | (b − a)²/12 | correct | recomputed |
| 161 | l6 | q[1].prose | "reach a dealer at random, 0.25 a day" gives an exponential gap | imprecise | as row 141; finding 16 |
| 162 | l6 | q[1] key 0.1353 | e⁻² | correct | recomputed |
| 163 | l6 | q[2] key and explain | Remaining life again exponential, mean 5; real hardware ages | correct | memorylessness |
| 164 | l6 | q[3].prose | "Trades arrive at 2 a minute, so gaps are exponential" | imprecise | "so" does not follow from a rate alone; finding 16 |
| 165 | l6 | q[3] key 20.8 s; median is ln 2 times the mean | median | correct | 0.3466 min |
| 166 | l7 | s[0].prose | Normal density formula | correct | C&B 3.3 |
| 167 | l7 | s[0] key, explain | Within one σ of μ is 0.6827 for every normal; location-scale family | correct | 2Φ(1) − 1 |
| 168 | l7 | s[1].prose | 0.9545 and 0.9973 within 2 and 3 sds | correct | 2Φ(2) − 1, 2Φ(3) − 1 |
| 169 | l7 | s[1] key 0.1587, wrongs; explain | one tail is half the outside; P(Z > 2) = 0.0228 | correct | recomputed |
| 170 | l7 | s[2].prose | N(2, 5²) notation; Z = (X − μ)/σ is N(0, 1) | correct | C&B 3.3 |
| 171 | l7 | s[2] key −2, wrongs −1.6, −0.4, 2 | standardising | correct | recomputed |
| 172 | l7 | s[3].prose, table | Φ values; Φ(−z) = 1 − Φ(z) | correct | table checked against erf |
| 173 | l7 | s[3] key 0.0228, wrongs 0.9772, 0.0455, 0.0548 | Φ(−2) | correct | Φ(−1.6) = 0.0548 |
| 174 | l7 | s[3].explain | 2.3% of days is "roughly once a month" | wrong | 1/0.0228 = 44 trading days, about two months; script l7 s3 CLAIM; finding 2 |
| 175 | l7 | s[4] key and options | N(8, 16) means variance 16; 0.3085 from dividing by 16 | correct | variance convention stated on the screen |
| 176 | l7 | s[4].explain | Losing years look 13 times likelier | correct | 0.3085/0.0228 = 13.5 |
| 177 | l7 | s[5].prose, solution | Φ(z) = ½(1 + erf(z/√2)) | correct | Abramowitz and Stegun 7.1.22; "exactly" qualified as machine precision in explain |
| 178 | l7 | s[6] target 1.645, wrong regions | one-tail 5% at 1.645; 1.96 two-sided; 2.326 one-tail 1% | correct | Φ⁻¹(0.95) = 1.6449, Φ⁻¹(0.975) = 1.9600, Φ⁻¹(0.99) = 2.3263 |
| 179 | l7 | s[7] order | Total area 1 by two substitutions and the Gaussian integral | correct | deriv. |
| 180 | l7 | s[8] key 0.0055, wrongs 0.0062, 0.0171, 0.9945 | Φ(−2.5417) | correct | script l7 s8; answer and wrong bands do not overlap |
| 181 | l7 | s[8].explain | Once in 180 trading days, one or two a year; real shares do it more often | correct | 1/0.00552 = 181; Cont fact 3 (heavy tails) |
| 182 | l7 | s[9].prose | "The 1-day 99% VaR is the return r … P(R < r) = 0.01" | imprecise | VaR is quoted as a positive loss (Hull 22.1), as this course does in the density lesson and in homework; here it is a negative return; finding 18 |
| 183 | l7 | s[9] key −2.74% (stored −0.02741), wrongs | μ − 2.326σ | correct | script l7 s9; unit "%" keys are fractions per AUTHORING |
| 184 | l7 | s[9].explain | About 25 breaches in 2,520 days | correct | 25.2 |
| 185 | l7 | s[10].prose | Breach count sd about 5 | correct | √(2520 × 0.01 × 0.99) = 4.995; assumes independent days |
| 186 | l7 | s[10] why luck | 41 or more about 1 time in 450 | correct | exact binomial tail 1 in 451; script l7 s10 |
| 187 | l7 | s[10] key and other why lines | Fat tails the most likely reason; σ² would give fewer breaches; mean barely matters | correct | Cont fact 3; 2.326 × 1.44 > 2.326 × 1.2 |
| 188 | l7 | s[10].explain | Normal VaR understates big losses; risk teams backtest breach counts | correct | Hull 22.8 (back-testing) |
| 189 | l7 | summary | cut-offs 1.645, 1.96, 2.326; divide by σ never σ² | correct | row 178 |
| 190 | l7 | q[0] 0.0228; q[1] 0.8186; q[2] Φ(−1); q[3] 0.3085 | drills with stated slips | correct | Φ(−1/3) = 0.3694, Φ(2/3) = 0.7475 recomputed |
| 191 | fluency-l7 | families[0] | z = (x − μ)/σ; slips z/σ and −z | correct | σ ≥ 2 so z/σ ≠ z; z ≠ 0 |
| 192 | fluency-l7 | families[1] | P(X < x) or P(X > x) from one table value; N(μ, σ²) variance notation | correct | all four sign and direction cases traced |
| 193 | fluency-l7 | families[2] | central band 2Φ − 1; slips Φ and Φ − 0.5 | correct | deriv. |
| 194 | l8 | s[0] key 125, wrongs 100, 75 | E price of double-or-halve | correct | recomputed |
| 195 | l8 | s[0].explain | Symmetric in logs means skewed in prices | correct | exp is convex |
| 196 | l8 | s[1] key, explain | Median e^μ stays; mean e^(μ+σ²/2) rises; 137.71 at σ = 0.8 | correct | C&B 3.3 lognormal; recomputed |
| 197 | l8 | s[2].prose, key 109.95, wrongs | Median passes through the monotone map | correct | quantiles commute with increasing functions |
| 198 | l8 | s[3] order | E[e^(σZ)] = e^(σ²/2) by completing the square | correct | normal mgf, C&B 2.3 |
| 199 | l8 | s[3].explain | Mean above median when σ > 0; convexity is the reason | correct | Jensen |
| 200 | l8 | s[4] key 115.01, wrongs 109.95, 120.30, 127.74 | e^4.745 | correct | recomputed |
| 201 | l8 | s[5].prose | S_T = S₀ exp((m − σ²/2)T + σ√T Z); E[S_T] = S₀e^(mT); volatility drag | correct | Hull 15.1 to 15.3 |
| 202 | l8 | s[5] key and why lines | σ → 0 collapses to 105.13; median 103.05 at σ = 0.2 | correct | recomputed |
| 203 | l8 | s[6].prose | "expected to rise 8%" for 50e^0.08 = 54.16 | imprecise | the expected simple rise is e^0.08 − 1 = 8.3%; finding 25 |
| 204 | l8 | s[6] key 0.5 and options 0.5793, 0.5732 | log drift m − σ²/2 = 0 | correct | script l8 s6 |
| 205 | l8 | s[6].explain | Expected return and chance of a gain are different questions | correct | mean against median |
| 206 | l8 | s[7].prose and key | P(S_T > K) formula; m = 0 gives less than ½ | correct | Hull 15.1; 1 − Φ(σ√T/2) |
| 207 | l8 | s[8] key 0.2231 and four wrongs | digital probability | correct | script l8 s8 |
| 208 | l8 | s[9] key 0.5398; explain z = σ√T/2 | chance of ending below the mean | correct | script MC l8 s9 |
| 209 | l8 | summary | median, mean, drag; do not put a normal on S | correct | rows 196 to 206 |
| 210 | l8 | q[0] 8.373; q[1] 0.4013; q[2]; q[3] 105.65 | lognormal drills and slips | correct | e^2.25 = 9.488, 100e^(−0.05) = 95.12 recomputed |
| 211 | review-2 | it[0] 0.75; it[1] 3; it[2] 0.2231; it[3] 0.8186 | drills | correct | recomputed; Poisson process stated in it[2] |
| 212 | review-2 | it[4] 2; explain | Pareto density 2/x³: mean 2, E[X²] infinite, "a fat tail" | correct | ∫₁^∞ 2/x dx diverges |
| 213 | review-2 | it[5] key and options | memoryless with a stated Poisson process | correct | e^(−0.8) |
| 214 | review-2 | it[6] 0.4366, wrongs 0.4472, 0.1906 | σ from mean over median | correct | √(2 ln 1.1) |
| 215 | review-2 | it[7] 2%, wrongs 1.68%, 1.414% | sd from a one-tail 5% quantile | correct | 3.29/1.645 |
| 216 | review-2 | it[8] 0.4345, wrongs 0.353, 0.4536, 0.5 | two-year lognormal | correct | script r2 item8 |
| 217 | homework-2 | it[0] e^(−x/3); it[1] 0.125 | tails by integration | correct | recomputed |
| 218 | homework-2 | it[2] order; explain | E[T] = 1/λ by parts; boundary term vanishes | correct | deriv. |
| 219 | homework-2 | it[3] 10.25, wrongs 9.254, 9.119 | two quantile equations; Φ⁻¹(0.9) = 1.2816 | correct | script hw2 item3 |
| 220 | homework-2 | it[4] 3.25%, wrongs 3%, 3.198% | hazard from survival | correct | −ln 0.85/5; tol 0.0001 separates 0.03198 |
| 221 | homework-2 | it[5] 0.3787, wrongs 0.3526, 0.371 | lognormal interval | correct | script hw2 item5 |
| 222 | homework-2 | it[6] £352,900, wrongs; loss convention stated | lognormal VaR measured from today's value | correct | script hw2 item6; Hull 22.1 |
| 223 | homework-2 | it[6].explain | Normal on simple returns says £415,200; log return −0.536 | correct | ln(1 − 0.4152) = −0.5365 |
| 224 | homework-2 | it[7].model (a) to (c) | density check, CDF, median ln 2/λ, memoryless proof | correct | deriv. |
| 225 | homework-2 | it[7].model (d), (e) | e^(−0.3) = 0.7408; 1 − e^(−0.15) = 0.1393; constant hazard gives no gain in safety; fails when credit quality moves | correct | recomputed; Hull 24.2 |
| 226 | homework-2 | it[8].model (a), (b) | P(Tₙ > t) = (1 − λ/n)^⌊nt⌋; squeeze to e^(−λt) | correct | deriv. rechecked: r^(nt) ≤ r^j < r^(nt−1) for 0 < r < 1 |
| 227 | homework-2 | it[8].model (c) | 0.1285 and 0.1347, both below e⁻²; ln(1 − x) < −x | correct | script hw2 item8 |
| 228 | homework-2 | it[8].model (d) | Var U(a, b) from the density; mean 0.03 s, sd 0.0289 s | correct | algebra rechecked |
| 229 | l9 | s[0] key, explain | Three die averages close in on 3.5; captions 4.50, 2.60, 3.70 and 3.56, 3.43, 3.50 | correct | script l9 s0 data |
| 230 | l9 | s[0] why exact | Close is not equal | correct | convergence in probability, not eventual equality |
| 231 | l9 | s[1] key £1; captions £0.50, £0.98 | mean payout 10 × 0.1 | correct | script l9 s1 data |
| 232 | l9 | s[1].explain | "lopsided averages need more draws" | misleading | the slow settling comes from the sd (£3 against a mean of £1), not from skew: a symmetric ±£3 bet is as slow; Var(X̄) = σ²/n; finding 27 |
| 233 | l9 | s[2] bars and key | Exact far chances 1, 0.6479, 0.1355, 3.4e−6; tends to 0 | correct | script l9 s2 (exact convolution) |
| 234 | l9 | s[2].explain | Any margin, however small: the law of large numbers | correct | Durrett Thm 2.2.14 |
| 235 | l9 | s[3] key and why lines | Share settles, heads minus tails typically moves further from 0; gambler's fallacy | correct | script MC l9 s3 (0.855); sd of gap √n |
| 236 | l9 | s[3].explain | Gap −18 to −84; share misses by 84/20,000 | correct | script l9 s3 data |
| 237 | l9 | s[4].prose | Weak law: iid, finite mean, P(abs(X̄ − μ) > ε) → 0 | correct | Khinchin; Durrett Thm 2.2.14 |
| 238 | l9 | s[4] key and why lines | Law is about the chance of a miss; total minus 3.5n grows; no promise at 30 rolls | correct | sd of the total is σ√n |
| 239 | l9 | s[4].feedback.correct | "The law bounds the chance of a miss" | imprecise | the law gives a limit, not a bound; Chebyshev gives the bound; finding 12 |
| 240 | l9 | s[5] order | Var(X̄) = σ²/n; "variances of independent variables add" | correct | sufficient condition, stated as such |
| 241 | l9 | s[5].explain | Without independence the variances need not add | correct | "need not" is right |
| 242 | l9 | s[6] key 0.171, wrongs | sd of mean of 100 rolls | correct | √(35/12)/10 |
| 243 | l9 | s[6].explain | Ten times the precision costs a hundred times the data | correct | σ/√n |
| 244 | l9 | s[7] key and why lines | St Petersburg average does not settle; £13 at 1,000 games, £42 at 2,550 | correct | script l9 s7 data; MC: median of mean grows (Feller X.4: mean/log₂n → 1) |
| 245 | l9 | s[7].explain | Mean is infinite; the law needs a finite mean | correct | for iid draws a finite mean is what the law assumes; with mean +∞ the average diverges |
| 246 | l9 | s[8] key 0.0447%, wrongs | 2%/√2000 | correct | recomputed |
| 247 | l9 | s[9].prose, key | Roulette edge 10/37, sd about £10; total 27,027 with sd 3,161; loss needs 8.5 sds | correct | script l9 s9 |
| 248 | l9 | s[9].explain | Many small independent bets make the average reliable | correct | row 240 |
| 249 | l9 | summary.ideas[2] | Cauchy has no finite mean and its average does not settle | correct | script MC Cauchy; C&B Example 2.2.4 |
| 250 | l9 | summary.formula.note | "Needs independent, identically distributed draws with a finite mean" | imprecise | iid is sufficient, not necessary: uncorrelated draws with bounded variances also obey the law (Chebyshev; the course's own homework-3 it[9]); finding 5 |
| 251 | l9 | q[0] 0.3%; q[1] 1,020; q[2] within £10; q[3] | drills | correct | 497/100 = 4.97; 520 + 500 |
| 252 | l10 | s[0] key 0.2; explain | Markov by pushing mass: q ≤ 20/100 | correct | extremal distribution for Markov |
| 253 | l10 | s[1] key; explain | a·1{x ≥ a} ≤ x for x ≥ 0 | correct | two cases |
| 254 | l10 | s[2] order; explain | Markov's inequality; X ≥ 0 used only in the first line | correct | C&B Thm 3.6.1 (Chebychev form) / Durrett Thm 1.6.4 |
| 255 | l10 | s[3] key 0.2, wrongs 5, 0.04, 0.8 | 2/10 | correct | recomputed |
| 256 | l10 | s[4] key 0.5; explain | Markov fails for a P&L that can be negative; counter-example | correct | 0.5 > 0.2 |
| 257 | l10 | s[5].prose, order | Chebyshev from Markov on (X − μ)², any X with mean and sd | correct | C&B Example 3.6.2 |
| 258 | l10 | s[5].explain | Needs only a mean and a variance | correct | row 257 |
| 259 | l10 | s[6] table; explain | 0.444, 0.25, 0.111 against 0.1336, 0.0455, 0.0027; five-fold and forty-fold | correct | script l10 s6 |
| 260 | l10 | s[7] key 0.25 and options; explain | Three-point distribution attains the bound at k = 2; cannot be improved without more information | correct | sharpness example, C&B Example 3.6.3 style |
| 261 | l10 | s[8].prose, key 27.8 | At most 1/9 of days beyond 3 sd; 250/9 | correct | Chebyshev; 250 days stated on the screen (252 used elsewhere in the course) |
| 262 | l10 | s[8].explain | Real returns sit between, often a few a year | correct | Cont fact 3; 3-sd days near 1% of days for equities |
| 263 | l10 | s[9].prose | Chebyshev on X̄ "whose variance is σ²/n" | imprecise | σ²/n needs independent (uncorrelated) trades, not stated on this screen; finding 11 |
| 264 | l10 | s[9] key 4,000, wrongs 200, 400, 2,000 | n = σ²/(0.1 ε²) | correct | script l10 s9 |
| 265 | l10 | s[9].explain | "4,000 trades always suffice"; normal needs about 1,083 | imprecise | "always" holds only for independent trades; the 1,083 is right (two-sided 1.645); finding 11 |
| 266 | l10 | summary | Markov needs X ≥ 0; Chebyshev needs a finite mean and variance; a bound is a ceiling | correct | rows 254, 257 |
| 267 | l10 | q[0] 0.2; q[1] at most a quarter; q[2] k = 5; q[3] absolute change | drills | correct | recomputed |
| 268 | l11 | s[0] bars, key | Rescaled exponential averages approach the normal; exact bars | correct | script l11 s0 (gamma CDF) |
| 269 | l11 | s[0].explain | One wait cannot fall more than 1 sd below its mean; slight right lean remains at 30 | correct | min 0, mean 1, sd 1; skewness 2/√30 = 0.37 |
| 270 | l11 | s[1] key 5.48, wrongs 30, 1, 0.18 | sd of a sum of 30 | correct | √30 |
| 271 | l11 | s[2] key and why lines | Uniform n = 3 within 0.01 of each normal bar; exponential has almost nothing below −1.5 against 0.07 | correct | script l11 s2 (Irwin-Hall) |
| 272 | l11 | s[2].feedback.correct, explain | "A symmetric start gets to the bell fastest"; speed "depends on how lopsided one draw is" | imprecise | speed also depends on tail weight: symmetric t(3) is far from normal at n = 3 (script MC t(3): 0.483 against 0.383); Berry-Esseen uses E abs(X)³; finding 7 |
| 273 | l11 | s[2].explain | Exponential's lean fades roughly like 1/√n | correct | skewness of the mean 2/√n; Edgeworth first term |
| 274 | l11 | s[3] key and why lines | A large sample of single draws shows the draw's shape, not a bell | correct | Glivenko-Cantelli |
| 275 | l11 | s[4].prose | CLT: iid, mean μ, finite σ²; standardised mean tends to N(0, 1) | correct | Lindeberg-Lévy, Durrett Thm 3.4.1 |
| 276 | l11 | s[4] key and why lines | Finite variance needed for this statement; normality, symmetry, n ≥ 30 are not conditions | correct | statement divides by σ |
| 277 | l11 | s[4].explain | "The theorem needs independence, identical draws and a finite σ²" | imprecise | sufficient for this form; Lindeberg-Feller drops identical, martingale and mixing versions relax independence (Durrett 3.4.2, 8.2); finding 4 |
| 278 | l11 | s[5] order; explain | Sum and mean give the same Z; Sₙ ≈ N(nμ, nσ²) | correct | algebra |
| 279 | l11 | s[6] key 0.0786, wrongs; explain exact 0.0844 | normal approximation to a gamma sum | correct | script l11 s6 |
| 280 | l11 | s[7] key and why lines | Sum of independent normals is exactly normal at every n | correct | C&B Thm 4.2.14 / mgf |
| 281 | l11 | s[8].prose | Daily returns roughly normal in calm markets, fat tails and clustering in stress | correct | Cont facts 3, 6 |
| 282 | l11 | s[8] key | 20-day returns closer to normal, clustering slows the approach | correct | Cont fact 5 (aggregational Gaussianity); script MC l11 s8 (kurtosis 13.5, 4.1, 0.5) |
| 283 | l11 | s[8] why further | "A 20-day return is a sum of 20 daily ones" | imprecise | true for log returns only; convention not stated; finding 8 |
| 284 | l11 | s[8].explain | "slower than the theorem promises"; infinite variance would block it | imprecise | the theorem promises no rate; the comparison is with independent days; the infinite-variance clause is right; finding 13 |
| 285 | l11 | s[9] key 0.1587, wrongs 0.5, 0, 0.4801 | book of 400 positions | correct | recomputed; 0.4801 covers both stated slips |
| 286 | l11 | s[9].explain | "correlated positions would widen the bell" | imprecise | only positive correlation widens it; negative narrows; finding 9 |
| 287 | l11 | summary.ideas[0] | "independent draws with finite variance approach N(0, 1)" | imprecise | drops "identically distributed"; false without it or a Lindeberg condition; finding 6 |
| 288 | l11 | summary.ideas[2] | Infinite variance or strong dependence can block the limit | correct | stable laws; Durrett 3.8 |
| 289 | l11 | q[0] 0.1%; q[2] 0.121; q[3] | drills | correct | q[2] has no continuity correction (not yet taught); exact 0.1152, script |
| 290 | l11 | q[1] key and explain | No finite variance: theorem does not apply; mean of n Cauchy draws is Cauchy | correct | characteristic function exp(−abs(t)) |
| 291 | l12 | s[0] key | Longer record is harder to match by luck despite the smaller mean | correct | t 1.90 against 0.95 |
| 292 | l12 | s[1] key 17%; explain | Standard error σ/√n; 0.126% at 63 days | correct | script l12 numbers |
| 293 | l12 | s[2] key 1.90, wrongs; explain | 3% of no-skill traders beat 1.9 standard errors | correct | 1 − Φ(1.905) = 0.0284 |
| 294 | l12 | s[3] key 1,600; explain | n = (2σ/μ)²; a real edge clears 2 about half the time | correct | script MC l12 s3 |
| 295 | l12 | s[4].prose | t = X̄√n/σ with σ written as known; abs(t) > 2 by luck 0.0455 | imprecise | the t-ratio in practice uses the sample sd; not said; result unchanged for large n (Slutsky); finding 19 |
| 296 | l12 | s[4] key and why lines | Large t is rare under luck; not a 99% chance of skill (prosecutor's fallacy); t counts standard errors | correct | P(data given H₀) is not P(H₀ given data) |
| 297 | l12 | s[4].feedback, explain | One time in 160; needs a prior | correct | 1 − Φ(2.5) = 0.0062 |
| 298 | l12 | s[5].prose, lines | Sharpe ratio defined as μ√252/σ of "daily returns" | imprecise | Sharpe ratio uses returns in excess of the risk-free rate (Sharpe 1966, 1994; Hull); first definition in the curriculum and the excess is not stated; finding 3 |
| 299 | l12 | s[5] lines mean, sd | Yearly mean 252μ, sd √252 σ for independent days | correct | additive (log) returns, iid |
| 300 | l12 | s[5] line se; explain | SE of the annualised Sharpe about 1/√T for small Sharpe ratios | correct | Lo eq. (9): √((1 + SR²/2)/n) per period; script MC l12 s5 |
| 301 | l12 | s[6] key and why lines | Q's Sharpe 1.59 against P's 0.79 | correct | recomputed |
| 302 | l12 | s[7] key 0.606, wrongs 0.91, 0.0455, 0 | at least one of 20 with abs(t) > 2 | correct | 1 − 0.9545²⁰; independence stated |
| 303 | l12 | s[8] key and why lines | Sharpe 1.0 over 2 years is within 2 standard errors of 0; 4 years needed | correct | 1/√2 = 0.71 |
| 304 | l12 | s[8].canvas xLabel | "Plausible true Sharpe ratio" on a normal centred at the estimate | misleading | reads as a posterior for the true value, the swap the lesson warns against two screens earlier; finding 28 |
| 305 | l12 | s[9] key 0.2136, wrongs | losing year for a Sharpe 0.79 book | correct | script l12 s9 |
| 306 | l12 | summary | SE, t, n = (2σ/μ)², SE(SR) ≈ 1/√T | correct | rows 292 to 300 |
| 307 | l12 | q[0] 0.075%; q[1] t = 1; q[2] 16 years; q[3] 0.0228 | drills | correct | recomputed |
| 308 | l13 | s[0] key; explain | Normal fits badly at p = 0.05; np(1−p) = 1.43; rule of thumb np(1−p) ≥ 10 | correct | stated as a rule of thumb; variants np, nq ≥ 5 exist (C&B p. 105) |
| 309 | l13 | s[1] key 14.5; explain | Each integer owns [k − 0.5, k + 0.5]; continuity correction | correct | C&B Example 3.3.2 |
| 310 | l13 | s[2] key 0.0579, wrongs 0.9421, 0.0361, 0.0216; exact 0.0553 | corrected normal estimate | correct | script l13 |
| 311 | l13 | s[3] table; explain | errors −0.0192 and 0.0026; a third too low without the correction | correct | 0.0192/0.0553 = 35% |
| 312 | l13 | s[4] key 8.5 and why lines; explain 0.1306 against 0.1308 | P(X < 9) ends at 8.5 | correct | script l13 |
| 313 | l13 | s[5].prose, key | P(X ≤ k) ≈ Φ((k + 0.5 − np)/√(npq)); P(X = 12) strip | correct | row 309; 0.161 against 0.162, script |
| 314 | l13 | s[5].explain | Rule of thumb is cautious; near p = 0.5 the fit is good sooner | correct | Bin(20, .55) errors above |
| 315 | l13 | s[6] order; explain | Binomial as a sum of indicators, CLT, half-unit | correct | de Moivre-Laplace |
| 316 | l13 | s[7].prose, key and why lines | Bin(100, .02): exact 0.0508, Poisson 0.0527, normal 0.0371; Poisson preferred | correct | script l13 s7; 27% low |
| 317 | l13 | s[7].explain | For p near 1 count failures | correct | n − X ~ Bin(n, 1 − p) |
| 318 | l13 | s[8] key 0.0287, wrongs; exact 0.0284; one in 35 | 60 wins from a coin | correct | script l13 s8 |
| 319 | l13 | s[9].question | "quick normal estimate" keyed with the continuity correction | imprecise | the question does not ask for the correction; an uncorrected 0.0119 is a valid reading and gets only generic feedback; finding 15 |
| 320 | l13 | s[9] key 0.0159; explain exact 0.0207, Poisson 0.0218 | right tail heavier than the bell even at np(1−p) = 19.6 | correct | script l13 s9 |
| 321 | l13 | s[9].explain | Real defaults are correlated, which fattens the tail | correct | as row 21 |
| 322 | l13 | summary.ideas[2] | "When p is near 0 or 1 … the Poisson with λ = np does better" | imprecise | for p near 1, λ = n(1 − p) on the failure count; and with np(1 − p) large the normal is fine whatever p; finding 14 |
| 323 | l13 | q[0] 3 points; q[1] z = −1.9; q[2] 0.0796; q[3] | drills | correct | script l13 quiz2; 0.5/√10 = 0.158 |
| 324 | review-3 | it[0] 0.005; it[1] 1/9 | drills | correct | recomputed |
| 325 | review-3 | it[2] 0.04 | One-sided event inside the two-sided Chebyshev event | correct | {X ≥ 20} ⊂ {abs(X − 10) ≥ 10} |
| 326 | review-3 | it[3] 0.2119, wrong 0.447 covers two slips | CLT for 36 trades | correct | Φ(−0.1333) = 0.447 both ways |
| 327 | review-3 | it[4] 900 days, about 3.6 years | (2σ/μ)² | correct | 900/252 = 3.57 |
| 328 | review-3 | it[5] 1.14; at least one about 0.68 | expected flukes in 50 tests | correct | script r3 item5 |
| 329 | review-3 | it[6] 0.0968 against exact 0.0978; it[7] 0.5704 exact | continuity correction | correct | script r3 |
| 330 | review-3 | it[8] multi | Sₙ/n settles; (Sₙ − 3.5n)/√n near normal; gap does not settle; single rolls stay uniform | correct | LLN and CLT scalings |
| 331 | homework-3 | it[0] 1,167, wrongs 59, 35 | n ≥ σ²/0.05² | correct | recomputed |
| 332 | homework-3 | it[1] 0.0711 against Markov 0.2 | E abs(X) = 30 ≤ sd 40 is consistent | correct | (40/150)² |
| 333 | homework-3 | it[2] order | Weak law from Chebyshev for independent draws with common mean and variance | correct | Durrett Thm 2.2.3 |
| 334 | homework-3 | it[2].explain | "the law itself holds with a finite mean alone" | imprecise | true for identically distributed draws (Khinchin); the item's hypotheses do not say identical; finding 10 |
| 335 | homework-3 | it[3] 0.1056, wrong 0.49 covers two slips | insurer shortfall | correct | recomputed |
| 336 | homework-3 | it[4] 14.3 years | T = (3/SR)² | correct | (3/0.7937)² = 14.29 |
| 337 | homework-3 | it[5] 0.0146; exact 0.0190; Poisson 0.0218 | skewed count tail | correct | script hw3 item5 |
| 338 | homework-3 | it[6] solution, tests | exact_tail and normal_tail teach the taught method | correct | values match script; continuity correction on the right side |
| 339 | homework-3 | it[7].model 1 to 3 | SR 1.06, SE 0.82, t 1.30, 900 days | correct | script hw3 item7 |
| 340 | homework-3 | it[7].model 4 | best of 10: 1 − (1 − 0.097)¹⁰ = 0.64 | imprecise | needs the 10 strategies to be independent; not stated in prompt or model; finding 20 |
| 341 | homework-3 | it[7].model 5 | CLT assumptions; positive serial correlation makes 0.82 an underestimate | correct | Lo section on autocorrelation |
| 342 | homework-3 | it[8] key and why lines | Only the normal stock's 5-day sum is exactly normal | correct | row 280 |
| 343 | homework-3 | it[9].model (a), (b) | Markov from an indicator; Chebyshev in ε form | correct | rows 254, 257 |
| 344 | homework-3 | it[9].model (c) | Weak law for independent, non-identical bets with capped variance; σᵢ² = i counter-example gives (n+1)/(2n) | correct | deriv.: Σi/n² |
| 345 | homework-3 | it[9].model (d) | means 0.1, 0.2; variances 0.99, 3.36; Chebyshev n = 967; normal 131 | correct | script hw3 item9 |
| 346 | homework-3 | it[9].model (d) exact | 0.0528 at 131; first at most 0.05 at 136; stays below after | correct | script (checked to n = 419); S ≤ 0 iff W_A + 2W_B ≤ n |
| 347 | problems-1 | it[0] parts 0 to 4 | 0.2012; 0.0788; 0.0852; 12.7; k = 6 | correct | script p1 item0 |
| 348 | problems-1 | it[0] part 2 why poisson-alarms | 30 minutes are Bernoulli, not Pois(2.36) | correct | 0.9212³⁰ against e^(−2.364) = 0.094 |
| 349 | problems-1 | it[1] parts 0 to 3 | 7/40; 1/6; 0.2401; 0.5 | correct | recomputed fractions |
| 350 | problems-1 | it[1] part 4 key | Drawing without replacement is not memoryless | correct | chance climbs 0.3, 3/9, 3/8, 3/7, 3/6 |
| 351 | problems-1 | it[2] parts 0 to 4 | 0.1479; 0.0754; 0.0754; 0.0057; 0.1513 | correct | script p1 item2 |
| 352 | problems-1 | it[3] parts 0 to 2 | 1.5; 1.4193; 0.2181, exact 0.2139 | correct | script p1 item3 |
| 353 | problems-1 | it[3] parts 3, 4 | binomial n = 152; exact n = 146; binomial errs on the safe side | correct | script p1 item3 |
| 354 | problems-2 | it[0] parts 0 to 4 | c = 2/9; 1/9; mean 1; e⁻²; 0.25; triangle not memoryless | correct | recomputed |
| 355 | problems-2 | it[1] parts 0 to 2 | median 81.21; mean 84.95; 0.5596 | correct | recomputed |
| 356 | problems-2 | it[1] part 3 | 0.2451 with z rounded to 0.69; 0.2439 unrounded, inside tol 0.0015 | correct | rounding protocol stated in the question |
| 357 | problems-2 | it[1] part 4 | VaR £30.42 from today's price, definition stated | correct | script p2 item1 |
| 358 | problems-2 | it[2] parts 0 to 4 | 0.125; variance 6; VaR 4.10; normal 4.03; 99% gap 0.55 | correct | script p2 item2 |
| 359 | problems-2 | it[2] part 4 explain | Bounded triangle: at 99% the normal's tail is the fatter one | correct | support ends at 6 |
| 360 | problems-2 | it[3] parts 0 to 4 | 0.9512; 41.63; 39.60; 0.4761; 0.4529 | correct | script p2 item3; independence of default and Z stated |
| 361 | problems-3 | it[0] parts 0 to 2 | sd 180; 0.0228; 0.0537 with correction | correct | script p3 item0 |
| 362 | problems-3 | it[0] part 3 | exact 0.0626, Poisson 0.0648; Poisson preferred; normal 14% low | correct | script p3 item0 |
| 363 | problems-3 | it[1] parts 0 to 2 | sd 10; 0.0606 (exact 0.0605); 0.5277 | correct | script p3 item1 |
| 364 | problems-3 | it[1] part 3 | Šidák cut-off 0.0043; k = 227; exact binomial agrees | correct | script: tails 0.00534 at 226, 0.00398 at 227 |
| 365 | problems-3 | it[1] part 4 | 625 calls for an expected t of 2 at 54% | correct | (2 × 0.5/0.04)² |
| 366 | problems-3 | it[2] parts 0, 1 | Markov 1/3; Chebyshev 1/36 via the two-sided event | correct | recomputed |
| 367 | problems-3 | it[2] parts 2, 3 | Chebyshev 320 days; normal 62; "if not too lopsided" | correct | script p3 item2; days independent stated |
| 368 | problems-3 | it[3] parts 0 to 4 | SE 0.6667; t 1.8; Chebyshev 0.3086; normal 0.0718; 45 months | correct | recomputed |

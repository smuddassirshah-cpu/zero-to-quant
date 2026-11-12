# Claim ledger: limits-thm levels 1 to 3, round 2 (blind)

Every row was judged by hand from the content JSON. "script" in the basis column means a named check in `docs/reports/limits-thm-L1-3-concepts-r2.py`. Paths are relative to the file named in the first column (`s[n]` is `screens[n]`, `q[n]` is `quiz[n]`, `i[n]` is `items[n]`, `p[n]` is `parts[n]`, `fb` is `feedback`, `w` is `widget`).

Sources, cited by short name. C&B: Casella and Berger, *Statistical Inference*, 2nd ed. Ross: *A First Course in Probability*, 9th ed. Durrett: *Probability: Theory and Examples*, 4th ed. Feller: *An Introduction to Probability Theory and Its Applications*, vol. 1 (3rd ed.) and vol. 2 (2nd ed.). Hull: *Options, Futures and Other Derivatives*, 9th ed. Lo (2002): "The Statistics of Sharpe Ratios", *Financial Analysts Journal* 58(4). Cont (2001): "Empirical properties of asset returns: stylized facts and statistical issues", *Quantitative Finance* 1. Jorion: *Value at Risk*, 3rd ed.

Verdicts: `correct`, `wrong`, `imprecise`, `misleading`, `unverified`.

## l1-counting-successes

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | s[1].w.answer | exactly one win: WLL, LWL, LLW | correct | enumeration of 8 paths |
| l1 | s[1].w.wrong | one-order is one path; at-most adds LLL (no wins) | correct | enumeration; feedback names each set |
| l1 | s[1].explain | each one-win path has chance 0.6 × 0.4² = 0.096 | correct | product rule for independent trials, C&B 1.3.7 |
| l1 | s[2].w.rows | P(X=k) = 0.064, 0.288, 0.432, 0.216 | correct | 1, 3, 3, 1 paths times path chance; sums to 1 |
| l1 | s[2].hints[0] | paths are separate outcomes, so chances add | correct | disjoint additivity |
| l1 | s[2].explain | the list of chances is the distribution of X | correct | definition of a pmf, C&B 1.6 |
| l1 | s[3].prose | wins in n independent trials with chance p is Bin(n, p) | correct | C&B 3.2.2 |
| l1 | s[3].w.options | at p = 0.5 the bars are symmetric about n/2 | correct | P(X=k) = P(X=n−k) when p = ½ |
| l1 | s[3].w.options[1].why | leaning to 0 is the shape for small p | correct | mode near np |
| l1 | s[3].w.options[2].why | C(n,k) peaks in the middle | correct | binomial coefficients unimodal |
| l1 | s[3].explain | p above 0.5 moves bulk right, tail trails left | correct | skewness (1−2p)/√(npq) |
| l1 | s[4].w.answer | C(5,3) = 10 | correct | 5·4·3/6 |
| l1 | s[4].w.wrong | 5 counts trades; 60 = 5·4·3 ordered; 3 counts wins | correct | arithmetic; feedback names each |
| l1 | s[4].explain | P(X=3) = 10 × 0.03456 = 0.3456 | correct | script: l1 s4 |
| l1 | s[5].w.options | P(X=2) for Bin(4, 0.5) is 0.375; 0.0625 one path; 0.125 two paths; 0.5 share | correct | script: l1 s5; 2 × 0.0625 = 0.125 |
| l1 | s[5].explain | six orders listed; six times the colleague's answer | correct | C(4,2) = 6 |
| l1 | s[6].w.lines | derivation of C(n,k) p^k (1−p)^(n−k), order one, same, count, add | correct | C&B 3.2.2 |
| l1 | s[6].explain | two conditions: fixed n; independent trials with same p | correct | C&B 3.2.2 |
| l1 | s[7].prose | X = sum of indicators; linearity gives 20p; independent so variances add | correct | independence is given as sufficient |
| l1 | s[7].w.answer | Var(X) = 20p(1−p) and accepted forms | correct | expansion 20p − 20p² |
| l1 | s[7].w.wrong | 20p is the mean; 400p(1−p) = Var(20 I₁); p(1−p) one trade | correct | Var(cY) = c²Var(Y) |
| l1 | s[7].explain (sentence 1, 2) | independence makes covariances zero; E = np, Var = np(1−p) | correct | C&B 4.5.6 |
| l1 | s[7].explain (sentence 3) | "Without independence the covariances stay and this sum is wrong" | imprecise | finding 2: uncorrelated but dependent variables also have zero covariances, C&B 4.5 example X, X² |
| l1 | s[8].w.answer | sd = √4.95 ≈ 2.225 | correct | script: l1 s8 |
| l1 | s[8].w.wrong | 4.95 variance; 11 mean; 3.317 = √11 leaves out 1−p | correct | script: l1 s8 no-q |
| l1 | s[8].explain | 9 or 13 wins is ordinary noise | correct | within one sd of 11 |
| l1 | s[9].w.solution | list comprehension of the pmf with math.comb | correct | script: l1 s9 solution passes, starter fails |
| l1 | s[9].prose | 15 or more needs six terms | correct | k = 15 to 20 |
| l1 | s[9].explain | P(X ≥ 15) ≈ 0.0553, about once in 18 weeks; list sums to 1, mean 11 | correct | script: l1 s9 tail, once in 18 |
| l1 | s[10].w.answer | 0.98^50 ≈ 0.3642 | correct | script |
| l1 | s[10].fb.mean-one | more than a third of years have no default | correct | 0.3642 > 1/3 |
| l1 | s[10].explain | in a recession defaults move together, so many-default years are likelier than the binomial says | correct | script: MC l1 dependent funds |
| l1 | summary | ideas, formula, trap | correct | restate the above |
| l1 | q[0] | exactly one of four at 0.5: 0.25; slips 0.0625, 0.5 | correct | 4/16 |
| l1 | q[1] | funds in one stock are not independent, so not Bin(10, 0.4); X lands near 0 or 10 more often | correct | script: MC l1 |
| l1 | q[1].options[2].why | same p is needed but not enough | correct | binomial definition |
| l1 | q[2] | variance 21; slips 30 mean, 4.583 sd, 70 mean losses | correct | script: l1 q2 sd |
| l1 | q[3] | p(1−p) peaks at 0.5, largest variance 2.5; p = 0.1 gives 0.9 | correct | calculus |

## l2-first-success

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l2 | s[1].w | first fill in minute 3: 0.8² × 0.2 = 0.128 | correct | script |
| l2 | s[1].w.wrong | 0.2 one minute; 0.008 = 0.2³; 0.6 added; 0.488 = 1 − 0.8³ | correct | arithmetic; feedback names each |
| l2 | s[2].w.options | minute 1 is the most likely for every p | correct | pmf decreasing in k, C&B 3.2.5 |
| l2 | s[2].options[1].why | long waits pull the average past the tallest bar | correct | mean 1/p ≥ mode 1 |
| l2 | s[2].explain | at p = 1 a single bar | correct | pmf at p = 1 |
| l2 | s[3].prose | P(X=k) = (1−p)^(k−1) p, the geometric | correct | C&B 3.2.5 (trials convention) |
| l2 | s[3].w | P(X>3) = 0.512; slips 0.488, 0.4096 (X>4), 0.128 | correct | 0.8³ |
| l2 | s[3].explain | P(X>m) = (1−p)^m | correct | m failures in a row |
| l2 | s[4].w.options | P(X>5 given X>2) = 0.512; 0.328 = 0.8⁵; 0.64; 0.21 product | correct | script: l2 s4 opt |
| l2 | s[4].explain | memoryless: P(X>m+n given X>m) = P(X>n) | correct | C&B 3.2.5 |
| l2 | s[5].w.options | chance of a fill in minute 10 given nine waits is 0.2 | correct | conditional probability |
| l2 | s[5].options | gambler's fallacy; 0.027 is P(X=10) | correct | script: l2 s5 bar 10 |
| l2 | s[5].explain | if fills do get likelier the geometric model is wrong | correct | constant hazard characterises the geometric |
| l2 | s[6] | Y = X − 1 counts failures: P(Y=2) = 0.128; 0.16 from trials formula | correct | 0.8 × 0.2 = 0.16 |
| l2 | s[6].explain | both are called geometric; check the convention | correct | scipy.stats.geom counts trials, R dgeom counts failures |
| l2 | s[7].prose | E[X] = p·1 + (1−p)(1 + E[X]) | correct | first-step analysis, Ross 7.5 |
| l2 | s[7].w | E[X] = 1/p; slips p, (1−p)/p, 1/(1−p) | correct | algebra |
| l2 | s[7].fb.failures | (1−p)/p is the mean number of failures | correct | E[X] − 1 |
| l2 | s[8].w.lines | S = 1 + 2q + 3q² + …; S − qS geometric; S = 1/p² | correct | script: l2 mean 1/p |
| l2 | s[9] | mean 20 backtests at p = 0.05; slips 19, 5, 0.05 | correct | 1/0.05 |
| l2 | s[9].explain | on average one of 20 no-edge variants passes | correct | expected count 20 × 0.05 = 1 |
| l2 | s[10] | 1 − 0.95^10 ≈ 0.4013; slips 0.5, 0.5987, 0.0315 | correct | script |
| l2 | s[10].explain | about two times in five | correct | 0.4013 |
| l2 | summary | ideas, formula, note, trap | correct | restate |
| l2 | q[0] | 25/216 ≈ 0.1157; slips 1/6, 1/216 | correct | script |
| l2 | q[1] | p = 1: X = 1 always, mean 1, variance 0; formula does not break | correct | pmf at p = 1 |
| l2 | q[2] | (5/6)⁶ ≈ 0.335; (5/6)¹⁰ ≈ 0.162; (5/6)² ≈ 0.694 | correct | script |
| l2 | q[3] | E[Y] = 3; slips 4, 0.25 | correct | (1−p)/p |

## l3-rare-events

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l3 | s[1] | Bin(10, 0.2): P(0) = 0.8^10 ≈ 0.1074; slips 0, 0.8, 0.2^10 | correct | script |
| l3 | s[2] | (1 − 2/n)^n → e⁻² ≈ 0.1353; 0.1299 at 50, 0.1348 at 500 | correct | script |
| l3 | s[2].options | mean stays at 2 as slots shrink | correct | np = 2 |
| l3 | s[3].prose | Poisson pmf; counts events in a fixed window when rare and independent; λ is the mean | correct | C&B 3.2.4; Feller vol. 1 VI.5 |
| l3 | s[3].w | P(X=2) = 0.2707; slips 0.302, 0.5413, 0.1353 | correct | script |
| l3 | s[3].explain | 500 slots gives 0.2712; P(1) = P(2) at λ = 2 | correct | script |
| l3 | s[4].w | e^−1.5 ≈ 0.2231; slips 0.3347, 0.3679, 0 | correct | script |
| l3 | s[4].fb.zero | "About one module in five is clean" | imprecise | finding 7: 0.2231 is 1 in 4.5 |
| l3 | s[4].explain | P(X=0) = e^−λ always | correct | pmf at k = 0 |
| l3 | s[5].prose | variance 2(1 − 2/n): 1.6 at 10, 1.992 at 500 | correct | arithmetic |
| l3 | s[5].w | limit variance 2; slips 0, 1.6, 1.414 | correct | C&B 3.2.4 |
| l3 | s[5].explain | limit of variances "points to" λ; pmf sum confirms | correct | hedged; E[X(X−1)] = λ² |
| l3 | s[6] | P(at least one) = 1 − e^−0.5 ≈ 0.393, below the rate | correct | 1 − e^−λ < λ |
| l3 | s[6].options | 0.607 none; 0.303 exactly one | correct | arithmetic |
| l3 | s[6].explain | a rate can exceed 1 | correct | λ is a mean count |
| l3 | s[7].w.lines | Poisson limit derivation with k fixed | correct | C&B 2.3.3 example; Feller VI.5 |
| l3 | s[7].explain | C(n,k)/n^k becomes 1/k! | correct | ratio of falling factorial to n^k tends to 1 |
| l3 | s[8] | Pois(3): P(X ≥ 6) = 0.0839; slips 0.9161, 0.0504, 0.1008 | correct | script |
| l3 | s[8].explain | about one hour in twelve | correct | script |
| l3 | s[9].prose | Pois(2) gives 6 or more about 0.017 | correct | script: 0.0166 |
| l3 | s[9].w.options | variance three times the mean signals clustering; Poisson needs variance equal to mean | correct | script: MC l3 clustering |
| l3 | s[9].options[2].why | rare is not enough; events must also be independent | correct | Poisson process postulates, Ross 9.1 |
| l3 | s[9].explain | Pois(2) predicts about 4 such days in 250; 21 seen; overdispersion | correct | script |
| l3 | summary | ideas, formula, note, trap 0.39 | correct | restate |
| l3 | q[0] | e⁻⁴ ≈ 0.0183; once in 55 days; slips 0.25, 0.0733 | correct | script |
| l3 | q[1] | variance 2.5; sd 1.58; λ² = 6.25 | correct | C&B 3.2.4 |
| l3 | q[2] | Bin(1000, 0.002) one rejection ≈ 2e⁻² = 0.2707; exact also 0.2707 | correct | script |
| l3 | q[3] | 20 minutes at 3 an hour: e⁻¹; slips e⁻³, e⁻³/3, 2/3 | correct | script |
| l3 | q[3].explain | the rate scales with the window | correct | Poisson process, Ross 9.1 |

## l4-without-replacement

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l4 | s[1] | paths with two reds: RRB, RBR, BRR; products equal | correct | each is 4·3·6/(10·9·8) |
| l4 | s[2] | P(X=2) = 0.3; slips 0.1, 0.288 with replacement, 0.4 share | correct | script |
| l4 | s[3].cv.derive | hypergeometric bars for n = 5 with 20% marked | correct | C(5,k) falling-factorial form; script at N = 20, 100, 1000 |
| l4 | s[3].w.options | binomial is a good stand-in when the population is large against the sample | correct | C&B 3.2.3 remark; factor (N−n)/(N−1) |
| l4 | s[3].options[3].why | 0.2817 against 0.3277 at N = 20 | correct | script |
| l4 | s[4] | 36 hands of 120 hold two reds; slips 6, 72, 120, 12 | correct | C(4,2)C(6,1) |
| l4 | s[4].explain | hypergeometric pmf | correct | C&B 3.2.1 |
| l4 | s[5] | E[X] = nK/N = 1 by symmetry and linearity; slips 4, 0.2, 1.25 | correct | C&B 3.2.1 |
| l4 | s[5].explain | linearity needs no independence | correct | C&B 4.5 |
| l4 | s[6] | variance 0.8 × 15/19 ≈ 0.6316; slips 0.8, 0.6, 0.7895 | correct | script: l4 s6 variance from the pmf |
| l4 | s[6].explain | draws are negatively correlated | correct | Cov = −p(1−p)/(N−1) |
| l4 | s[7] | P(no errors) = C(16,5)/C(20,5) ≈ 0.2817; binomial 0.3277 overstates | correct | script |
| l4 | s[7].explain | factors 16/20, 15/19, …, each later one smaller | correct | arithmetic |
| l4 | s[8].w.lines | counting derivation | correct | C&B 3.2.1 |
| l4 | s[9].cv.rows | exact 0.2817, 0.3193, 0.3269; gaps 0.0459, 0.0084, 0.0008 | correct | script |
| l4 | s[9].explain | common rule: binomial when sample under about 5% of the population | correct | stated as a rule of thumb; standard 5% guideline |
| l4 | s[10].w.solution | comb(K,k)·comb(N−K,n−k)/comb(N,n) | correct | script: l4 s10 solution passes, starter fails |
| l4 | s[10].explain | P(X ≥ 4) ≈ 0.1096, one screen in nine; binomial 0.1209 | correct | script |
| l4 | summary | ideas, formula note with variance | correct | C&B 3.2.1 |
| l4 | q[0] | one ace in five cards 0.2995; binomial 0.2792 | correct | script; 52-card deck holds 4 aces |
| l4 | q[1] | n = N: X = 4 always, factor 0 | correct | (N−n)/(N−1) = 0 |
| l4 | q[2] | mean 2 with or without replacement | correct | linearity |
| l4 | q[3] | 20 of 50,000 safest; 50 of 100 factor about 0.5; 5 of 52 nearly 10% | correct | 50/99; 9.6% |

## l5-probability-as-area

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | s[0] | density x/8 on [0,4]: P(2 ≤ X ≤ 4) = 0.75; slips 0.5 height, 2 width, 0.25 left | correct | areas of triangles |
| l5 | s[1] | window areas 0.075 and 0.0075; P(X=3) = 0 | correct | (b²−a²)/16 |
| l5 | s[1].explain | chance lives in intervals, not points | correct | C&B 1.5 continuous variables |
| l5 | s[2] | c = 1/8; slip c = 0.25 gives area 2 | correct | 8c = 1 |
| l5 | s[2].prose | definition of a density; total area 1 | correct | C&B 1.6.3 |
| l5 | s[3] | F(x) = x²/16; slips x/8, x²/8 | correct | integral |
| l5 | s[3].explain | density is the derivative of the CDF; P(a ≤ X ≤ b) = F(b) − F(a) | correct | fundamental theorem of calculus; C&B 1.6 |
| l5 | s[4] | E[X] = 8/3; slips 2, 8 = E[X²], 1 | correct | integrals |
| l5 | s[4].explain | E[X²] = 8, Var = 8/9 | correct | 8 − 64/9 |
| l5 | s[5] | density 4 on [0, 0.25] is valid; P(0.05 ≤ X ≤ 0.1) = 0.2 | correct | area |
| l5 | s[5].explain | a density is chance per unit of x | correct | definition |
| l5 | s[6] | x/2 on [0,2] is a density; x has area 2; 1 − x negative; x²/2 area 4/3 | correct | integrals |
| l5 | s[7].w.lines | proof P(X=a) = 0 when f ≤ M near a | correct | squeeze |
| l5 | s[7].explain | P(a ≤ X ≤ b) = P(a < X < b) | correct | endpoints have chance 0 |
| l5 | s[8] | VaR with tail area 0.05: v = 10 − √5 ≈ 7.76; slips 9.5, 2.236, 5 | correct | script; Jorion ch. 5 quantile definition |
| l5 | s[8].explain | loses more than £7.76m on about 1 day in 20 | correct | tail 0.05 |
| l5 | s[9] | expected call payoff 125/600 ≈ 0.2083; slips 0, 0.625, 0.125, 1.6667 | correct | script |
| l5 | s[9].fb.at-mean | average of the payoff is not the payoff at the average | correct | Jensen, convex payoff |
| l5 | summary | ideas, note, trap | correct | restate |
| l5 | q[0] | P(X ≤ 0.5) = 0.125 for 3x²; slips 0.75, 0.5 | correct | integral |
| l5 | q[1] | density from CDF x³ is 3x² | correct | derivative |
| l5 | q[2] | P(X = 0.25) = 0, P(X ≤ 0.25) = 0.5 | correct | area |
| l5 | q[3] | Var = 1/18; slips 0.5, 0.2222 | correct | ½ − 4/9 |

## l6-uniform-exponential

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | s[0] | U(0,10): P(2 to 5) = 0.3; slips 3, 0.5 | correct | width × height |
| l6 | s[1] | height 1/(b−a); 1/20 at b = 20 | correct | area 1 |
| l6 | s[2].w.lines | Var U(0,w) = w²/12 and shift invariance | correct | C&B 3.3 uniform |
| l6 | s[2].prose | mean is the midpoint by symmetry | correct | symmetry |
| l6 | s[2].explain | U(0,10): variance 8.33, sd 2.89 | correct | 100/12 |
| l6 | s[3].prose | steady independent arrivals at rate λ give exponential waits, density λe^−λt | correct | Ross 9.1, Poisson process |
| l6 | s[3] | P(T>1) = e⁻² = 0.1353 at λ = 2; slips 0.8647, 0.3679 | correct | survival function |
| l6 | s[4] | P(T>t) = e^−2t; check 0.2466 at t = 0.7 | correct | script |
| l6 | s[4].explain | survival function e^−λt; CDF 1 − e^−λt | correct | C&B 3.3 exponential |
| l6 | s[5].prose | E[T] = 1/λ | correct | integration by parts |
| l6 | s[5] | P(T > mean) = e⁻¹ for every λ | correct | e^−λ/λ |
| l6 | s[5].explain | median ln 2/λ, about 21 seconds | correct | script: 20.8 |
| l6 | s[6] | P(T>1.5 given T>1) = e⁻¹; e⁻³ and e⁻² options | correct | ratio |
| l6 | s[7].w.lines | proof of memorylessness | correct | C&B exercise 3.25; Ross 5.5.1 |
| l6 | s[7].prose | geometric has it for trials; exponential is the continuous twin | correct | Ross 5.5.1 |
| l6 | s[8].prose | in a Poisson process the gaps are exponential with the same rate | correct | Ross 9.1 |
| l6 | s[8] | mean gap 1/3 second at 3 a second | correct | 1/λ |
| l6 | s[9] | survival e^−0.1 ≈ 0.9048; slips 0.9, 0.98⁵ = 0.9039, 0.0952 | correct | script; Hull 24.1 hazard rates |
| l6 | s[9].explain | hazard rate is λ: default rate per year for a survivor, close to a yearly chance when small | correct | Hull 24.1 |
| l6 | s[10] | U(−4,4) sd 8/√12 ≈ 2.31; slips 5.333, 0.667, 4 | correct | script |
| l6 | s[10].explain | uniform is the maximum-entropy density on an interval; a default, not a fact about fills | correct | Cover and Thomas, *Elements of Information Theory*, ch. 12 |
| l6 | summary | ideas, trap e⁻¹ against ½ | correct | restate |
| l6 | q[0] | Var U(−1,3) = 4/3, sd 1.15 | correct | 16/12 |
| l6 | q[1] | 8 days at 0.25 a day: e⁻²; mean gap 4 days | correct | 1/0.25 |
| l6 | q[2] | expected remaining life 5 years; constant hazard, nothing wears out | correct | memorylessness |
| l6 | q[3] | median 20.8 seconds; ln 2 times the mean | correct | script |

## l7-bell-curve

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l7 | s[0].prose | normal density formula | correct | C&B 3.3 normal |
| l7 | s[0] | within one sd is 0.6827 for every μ, σ | correct | location-scale family; script |
| l7 | s[1].prose | 0.9545 and 0.9973: the 68, 95, 99.7 rule | correct | Φ(2), Φ(3) |
| l7 | s[1] | P(Z>1) = 0.1587; slips 0.3173, 0.8413, 0.6827 | correct | symmetry |
| l7 | s[1].explain | P(Z>2) ≈ 0.0228 | correct | 1 − 0.9772 |
| l7 | s[2] | z = (−8 − 2)/5 = −2; slips −1.6, −0.4, 2 | correct | standardising |
| l7 | s[2].prose | Z = (X − μ)/σ is N(0,1) | correct | C&B 3.3 |
| l7 | s[3].cv.right | table values Φ(0.5) to Φ(2.5) | correct | standard table; script erf |
| l7 | s[3] | P(X < −8) = 0.0228; slips 0.9772, 0.0455, 0.0548 | correct | script: l7 s3 no-mu |
| l7 | s[3].explain | about 2.3% of days, roughly once every two months | correct | 1/0.0228 ≈ 44 trading days |
| l7 | s[4].prose | N(8, 16): second number is the variance | correct | convention stated |
| l7 | s[4] | P(X<0) = 0.0228; 0.3085 from dividing by 16 | correct | Φ(−0.5) |
| l7 | s[4].explain | "would make losing years look 13 times likelier" | imprecise | finding 6: 0.3085/0.0228 = 13.56 |
| l7 | s[5].prose | Φ(z) = ½(1 + erf(z/√2)) | correct | definition of erf |
| l7 | s[5].w.solution | phi with math.erf | correct | script: l7 s5 solution passes, starter fails |
| l7 | s[5].explain | exact to machine precision; phi(−1) + phi(1) = 1 | correct | test 7 |
| l7 | s[6] | one tail 5% at 1.645; 1.96 two-sided; 2.326 leaves 1% | correct | Φ⁻¹(0.95), Φ⁻¹(0.975), Φ⁻¹(0.99) |
| l7 | s[7].w.lines | total area 1 by two substitutions and the Gaussian integral | correct | C&B 3.3.14 |
| l7 | s[8] | P(R < −3) = Φ(−2.5417) ≈ 0.0055; slips 0.0062, 0.0171, 0.9945 | correct | script |
| l7 | s[8].explain | about once in 180 trading days, one or two a year | correct | 252 × 0.0055 = 1.4 |
| l7 | s[9].prose | 99% VaR: loss exceeded on 1% of days, quoted positive | correct | Jorion ch. 5; Hull 22.1 |
| l7 | s[9] | r = 0.05 − 2.326 × 1.2 ≈ −2.74%; slips −2.79, −1.92, −2.30, +2.84 | correct | script; each slip recomputed by hand |
| l7 | s[9].explain | 2,520 days give about 25 breaches | correct | 25.2 |
| l7 | s[10].prose | breach count sd about 5 | correct | √(2520 × 0.01 × 0.99) = 4.99 |
| l7 | s[10].options[1].why | 41 is about 3 sds above 25; 41 or more about 1 time in 450 | correct | script: exact binomial tail |
| l7 | s[10].options[2].why | σ² = 1.44 would give fewer breaches | correct | cut-off further out |
| l7 | s[10].options[3].why | the mean barely moves the cut-off | correct | 0.05 against 2.79 |
| l7 | s[10].explain | real daily returns have fat tails; normal VaR understates big losses | correct | Cont (2001) fact 2; script: t3 breach rate |
| l7 | summary | ideas, note, trap | correct | restate |
| l7 | q[0] | P(X>130) = 0.0228; half of the 4.6% outside two sds | correct | 0.0455/2 |
| l7 | q[1] | P(−1<Z<2) = 0.8186; slips 0.6827, 1.8185, 0.1359 | correct | script |
| l7 | q[2] | N(5,9): Φ(−1); Φ(−1/3) = 0.3694; Φ(2/3) = 0.7475 | correct | script |
| l7 | q[3] | Φ(−0.5) = 0.3085 | correct | symmetry |

## l8-lognormal

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l8 | s[0] | double or halve: expected price £125; log moves cancel | correct | ½(200 + 50) |
| l8 | s[0].w.wrong logs | 100 from averaging log moves | correct | e⁰ × 100 |
| l8 | s[0].fb.drop | 75: "averaged the gain and the loss as +100 and −50, then took off 50" | imprecise | finding 3: the average of +100 and −50 is +25, the right route to 125; 75 is ½(100 + 50) |
| l8 | s[0].explain | symmetric in logs means skewed in prices | correct | Jensen |
| l8 | s[1] | median stays e^μ; mean rises with σ; £137.71 at σ = 0.8 | correct | script |
| l8 | s[1].cv.functions | lognormal density | correct | C&B 3.3 lognormal |
| l8 | s[2].prose | lognormal definition; always positive; median e^μ since ln is increasing | correct | quantiles pass through increasing maps |
| l8 | s[2] | median e^4.7 ≈ 109.95; slips 4.7, 115.01 | correct | script |
| l8 | s[3].w.lines | E[e^σZ] = e^(σ²/2) by completing the square | correct | normal mgf, C&B 2.3.9 |
| l8 | s[3].explain | mean above median whenever σ > 0; convexity of e^x | correct | Jensen, C&B 4.7.7 |
| l8 | s[4] | mean e^4.745 ≈ 115.01; slips 109.95, 120.3, 127.74 | correct | script |
| l8 | s[4].explain | about 4.6% above the median | correct | e^0.045 = 1.046 |
| l8 | s[5].prose | S_T = S₀ exp((m − σ²/2)T + σ√T Z); E[S_T] = S₀e^mT | correct | Hull 15.1, 15.3 |
| l8 | s[5] | as σ → 0 all probability goes to £105.13 | correct | 100e^0.05 |
| l8 | s[5].options[2].why | median 100e^(0.05 − σ²/2); £103.05 at σ = 0.2 | correct | e^0.03 |
| l8 | s[6].prose | expected price 50e^0.08 = £54.16, about 8.3% up | correct | e^0.08 − 1 |
| l8 | s[6] | P(S₁ > 50) = 0.5 because log drift is 0; 0.5793 and 0.5732 options | correct | script: l8 s6 normal option |
| l8 | s[6].explain | expected return and chance of a gain are different questions | correct | mean against median |
| l8 | s[7].prose | P(S_T > K) formula; median and mean | correct | Hull 15.1 |
| l8 | s[7] | m = 0, σ > 0: P(S_T > S₀) < ½ | correct | 1 − Φ(σ√T/2) |
| l8 | s[8] | P(S₁ > 120) = 0.2231; slips 0.2419, 0.2541, 0.1977, 0.181 | correct | script, each slip recomputed |
| l8 | s[8].explain | median £103.05, mean £105.13 | correct | arithmetic |
| l8 | s[9] | P(S₁ < mean) = Φ(0.1) ≈ 0.5398; in general Φ(σ√T/2) | correct | script: MC l8 |
| l8 | summary | ideas, formula, trap | correct | restate |
| l8 | q[0] | E[S] = e^2.125 ≈ 8.373; slips 7.389, 9.488 | correct | arithmetic |
| l8 | q[1] | P(S₄ > 100) = 1 − Φ(0.25) ≈ 0.4013; down 6 times in 10 | correct | script |
| l8 | q[2] | lognormal is positive with mean above median | correct | C&B 3.3 |
| l8 | q[3] | median 100e^0.055 ≈ 105.65; slips 110.52, 95.12 | correct | script |

## l9-averages-settle

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l9 | s[0].options, explain | averages 4.50, 2.60, 3.70 after 10 rolls and 3.56, 3.43, 3.50 after 1,000 | correct | script: read from the embedded series |
| l9 | s[0].explain | "Each new roll moves a long average very little, so the lines settle near 3.5" | imprecise | finding 10: small steps alone do not give convergence; steps of size 1/n can sum without limit |
| l9 | s[0].options[2].why | all roll the same die so all head for the same place | correct | common mean |
| l9 | s[1] | scratch card average settles at £1; slips 10, 0, 5 | correct | 10 × 0.1 |
| l9 | s[1].explain | £0.50 after 100 cards, £0.98 after 2,000; sd £3 | correct | script; √(10 − 1) |
| l9 | s[2].cv.values | chance of a far average 0.6479, 0.1355, about 0.0000034 | correct | script: exact convolution |
| l9 | s[2].cv.caption | one roll is always far | correct | faces are at least 0.5 from 3.5 |
| l9 | s[2] | the chance tends to 0; for any margin | correct | WLLN, C&B 5.5.2 |
| l9 | s[3].cv.caption | share 0.491 and 0.4958; gaps −18 and −84 | correct | script: embedded data; 491 − 509, 4958 − 5042 |
| l9 | s[3].w.options | heads minus tails is typically further from 0 after 10,000 | correct | script: MC l9 gap, chance about 0.85 |
| l9 | s[3].options why | the share settles, the count gap is free to grow; gambler's fallacy | correct | sd of gap √n |
| l9 | s[3].hints[1] | 84 out of 10,000 is a share 0.0042 from a half | correct | 84/20,000 |
| l9 | s[4].prose | weak law: iid with finite mean, P(miss > ε) → 0 | correct | Khinchin; Durrett 2.2.9 |
| l9 | s[4].options | not an exact hit; not about the total; not within 0.01 after 30 rolls | correct | total minus 3.5n has sd 1.71√n |
| l9 | s[5].w.lines | Var(average) = σ²/n using independence | correct | C&B 5.2.6 |
| l9 | s[5].explain | without independence the variances need not add | correct | "need not" is the precise form |
| l9 | s[6] | sd of the average of 100 rolls 0.171; slips 0.0292, 0.0171, 0.2917, 1.708 | correct | script |
| l9 | s[6].explain | four times the rolls halves the sd; hundred times for ten times | correct | √n law |
| l9 | s[7].prose | St Petersburg game: £2^k for k tosses | correct | Feller vol. 1 X.4 |
| l9 | s[7] | the average does not settle; near £13 after 1,000 games; about £42 at 2,550 | correct | script: embedded data and MC growth |
| l9 | s[7].explain | mean is 1 + 1 + … infinite; the law needs a finite mean so promises nothing | correct | Durrett 2.4.1 with converse: for iid draws a finite almost-sure limit forces a finite mean |
| l9 | s[7].explain | "Some fat-tailed P&Ls behave like this" | unverified | no data to hand; vague empirical claim |
| l9 | s[8] | sd of average 2%/√2000 ≈ 0.0447%; slips 0.447%, 0.001% | correct | arithmetic |
| l9 | s[8].explain | 0.45% is "more than most real edges" | unverified | empirical claim about per-trade edges; plausible, not established here |
| l9 | s[9].prose | European wheel: red wins 18/37; casino mean 10/37, sd about £10 | correct | 37 pockets, 18 red; √(100 − 0.073) |
| l9 | s[9] | profit about £27,000, sd £3,161, loss all but impossible | correct | script; 8.5 sds |
| l9 | s[9].options[3].why | £270 is 1,000 bets | correct | 1000 × 0.27 |
| l9 | summary.ideas[2] | Cauchy has no finite mean and does not settle | correct | script: MC l9 Cauchy; Durrett 3.3 |
| l9 | summary.formula.note | iid with finite mean; variance line needs finite σ²; weaker conditions also give the law | correct | Durrett 2.2 |
| l9 | q[0] | 1.5%/√25 = 0.3%; slips 0.06%, 1.5% | correct | arithmetic |
| l9 | q[1] | 520 + 500 = 1,020 expected; slips 1,000, 1,040 | correct | fresh tosses |
| l9 | q[2] | sd of one policy £497; average within about £10 | correct | script; two sds of 4.97 |
| l9 | q[3] | St Petersburg fails to settle; the others have finite means | correct | SLLN |

## l10-bound-that-holds

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l10 | s[0] | at most a fifth of days can move £100k if the mean move is £20k | correct | Markov, C&B 3.6.1 remark |
| l10 | s[1] | a·1{x ≥ a} ≤ x for x ≥ 0 | correct | two cases |
| l10 | s[2].w.lines | Markov's inequality proof | correct | Ross 8.2 |
| l10 | s[2].explain | first line is the only place X ≥ 0 is needed | correct | proof structure |
| l10 | s[3] | Markov bound 2/10 = 0.2; slips 5, 0.04, 0.8 | correct | arithmetic |
| l10 | s[3].fb.flipped | "A probability bound cannot exceed 1" | imprecise | finding 4: E[X]/a exceeds 1 whenever a < E[X] and is still a valid, empty bound |
| l10 | s[3].explain | "Real volume is far less spread, so the true chance is much smaller" | unverified | empirical claim about volume; plausible |
| l10 | s[4] | P&L of +10 or −8: P(≥5) = 0.5 breaks the 0.2 "bound" | correct | script: l10 s4 counterexample |
| l10 | s[4].explain | apply Markov only to quantities that cannot go below 0 | correct | hypothesis of the theorem |
| l10 | s[5].w.lines | Chebyshev from Markov on (X − μ)² | correct | C&B 3.6.1; Ross 8.2 |
| l10 | s[5].explain | needs only a mean and a variance | correct | finite variance |
| l10 | s[6] | bounds 0.444, 0.25, 0.111; normal 0.1336, 0.0455, 0.0027 | correct | script |
| l10 | s[6].explain | five times smaller at k = 2; forty-fold at k = 3 | correct | 5.5 and 41 |
| l10 | s[7] | three-point variable attains the bound at k = 2 | correct | P = ¼, σ² = 1 |
| l10 | s[7].explain | Chebyshev cannot be improved without more information | correct | sharpness, C&B exercise 3.46 |
| l10 | s[8] | 250/9 ≈ 27.8 days; normal 0.7; slip 83.3 | correct | arithmetic |
| l10 | s[8].explain | "Real returns sit between, often a few a year" | unverified | no return data to hand; consistent with fat tails (Cont 2001) but the figure is not established |
| l10 | s[9].prose | Chebyshev on the average: bound σ²/(nε²) | correct | Ross 8.2 |
| l10 | s[9] | n = 4,000; slips 200, 400, 2,000 | correct | script |
| l10 | s[9].explain | about 1,083 if close to normal; nearly four times the data | correct | script: (1.645 × 20)² |
| l10 | summary.formula.note | needs a finite mean and variance; Markov needs X ≥ 0 | correct | hypotheses |
| l10 | summary.trap | "Markov fails for variables that can be negative" | imprecise | finding 5: it can fail; it is not guaranteed |
| l10 | q[0] | 200/1000 = 0.2 | correct | Markov |
| l10 | q[1] | at most a quarter, not exactly, not at least | correct | direction of the inequality |
| l10 | q[2] | k = 5 for a 0.04 bound | correct | 1/25 |
| l10 | q[3] | Markov applies directly to the absolute change | correct | non-negative |

## l11-sums-look-normal

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l11 | s[0].cv.params | exact bars for rescaled averages of n exponentials | correct | script: gamma CDF at n = 1, 3, 30 |
| l11 | s[0] | the shape loses its lean and hugs the normal by 30 | correct | CLT; skewness 2/√n |
| l11 | s[0].options[3].why | middle bars rise towards 0.19 | correct | Φ(0.5) − Φ(0) = 0.1915 |
| l11 | s[0].explain | one wait cannot fall below its mean by more than 1 sd | correct | mean = sd for the exponential |
| l11 | s[1] | sd of the sum of 30 waits √30 ≈ 5.48; slips 30, 1, 0.18 | correct | script |
| l11 | s[1].explain | sum and average give the same Z | correct | algebra |
| l11 | s[2] | uniform average at n = 3 is within 0.01 of each normal bar; exponential is not | correct | script: l11 s2, MC uniform |
| l11 | s[2].options[1].why | almost nothing below −1.5 against the normal's 0.07 | correct | Φ(−1.5) = 0.067 |
| l11 | s[2].explain | lean fades roughly like 1/√n; speed depends on skew and tails | correct | Berry–Esseen, Durrett 3.4.9 |
| l11 | s[3] | 1,000 single draws show the exponential shape, not a bell | correct | Glivenko–Cantelli; the CLT concerns sums |
| l11 | s[4].prose | CLT: iid, mean μ, finite variance; standardised average tends to N(0,1) | correct | Lindeberg–Lévy, Durrett 3.4.1 |
| l11 | s[4].w.options | finite variance is the condition this form cannot do without; 30 is a rule of thumb | correct | for the σ/√n scaling stated |
| l11 | s[4].explain | other forms relax independence and identical distribution | correct | Lindeberg–Feller; martingale CLT |
| l11 | s[5].w.lines | standardised sum equals standardised average | correct | algebra |
| l11 | s[5].explain | S_n ≈ N(nμ, nσ²) for large n | correct | CLT restated |
| l11 | s[6] | 50 exponential orders: 1 − Φ(1.4142) = 0.0786; slips 0.9214, 0.4207 | correct | script |
| l11 | s[6].explain | exact 0.0844; normal a little low from the right lean | correct | script: gamma(50) survival |
| l11 | s[7] | a sum of independent normals is exactly normal for any n | correct | C&B 5.2.9 (mgf) |
| l11 | s[7].explain | two days: mean 0.1%, sd 1.41% | correct | arithmetic |
| l11 | s[8].prose | daily returns: fat tails in stress, big days cluster; log returns add | correct | Cont (2001) facts 2 and 6 |
| l11 | s[8].w.options, explain | 20-day returns look closer to normal than daily; clustering slows the approach | correct | Cont (2001) fact 4, aggregational Gaussianity; script: MC l11 with fat-tailed shocks (see audit note on the normal-shock case) |
| l11 | s[8].options[1].why | trades inside a day are not independent; the conditions fail | correct | hypothesis check |
| l11 | s[8].explain (sentence 3) | "Fat tails with infinite variance would block it entirely" | imprecise | finding 11: some infinite-variance laws are still attracted to the normal with another scaling (Feller vol. 2 XVII.5, for example Student t with 2 degrees of freedom) |
| l11 | s[9] | 400 positions: P(loss) = Φ(−1) = 0.1587; slips 0.5, 0, 0.4801 | correct | script |
| l11 | s[9].explain | positively correlated positions would widen the bell | correct | Var of a sum with positive covariances |
| l11 | summary.ideas[2] | infinite variance or strong dependence can block the limit | correct | "can" |
| l11 | q[0] | 1.2%/√144 = 0.1%; slips 0.00833%, 14.4% | correct | arithmetic |
| l11 | q[1] | the theorem cannot promise a normal average for Cauchy draws; average of Cauchy is Cauchy | correct | Durrett 3.3; script: MC l9 Cauchy |
| l11 | q[2] | 100 dice: P(total > 370) ≈ 0.121; slips 0.879, 0.4727 | correct | script; no continuity correction is taught yet and Φ(1.17) is given |
| l11 | q[3] | lab errors as sums of many small independent effects | correct | hypothesis of elementary errors; Feller vol. 1 X |

## l12-skill-or-luck

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l12 | s[0] | B's 0.06% over 1,008 days is harder to match by luck than A's 0.12% over 63 | correct | t of 1.90 against 0.95 |
| l12 | s[1] | no-skill trader averages 0.12% or more over 63 days about 17% of the time | correct | script |
| l12 | s[1].explain | standard error is σ/√n | correct | C&B 5.2; standard usage |
| l12 | s[2] | B is 1.90 standard errors up; slips 0.525, 0.06, 0.95 | correct | script |
| l12 | s[2].explain | luck beats 1.9 standard errors about 3% of the time | correct | script: 0.028 |
| l12 | s[3] | two standard errors equal 0.05% at n = 1,600, about 6.3 years | correct | (2σ/μ)²; 1600/252 |
| l12 | s[3].explain | at that point a real edge clears 2 about half the time | correct | script: MC l12 |
| l12 | s[4].prose | t-ratio definition; near N(0,1) under no skill; sample sd leaves it close over hundreds of days | correct | CLT with Slutsky, C&B 5.5.17; script: MC l12 with t5 returns |
| l12 | s[4].prose | abs(t) > 2 by luck has chance about 0.0455 | correct | 2(1 − Φ(2)) |
| l12 | s[4].w.options | t = 2.5: luck rarely gives it, about one time in 160; not a 99% chance of skill | correct | script; Bayes needs a prior |
| l12 | s[5].prose, lines | Sharpe ratio is mean excess return over sd; annualised μ√252/σ; risk-free rate taken as 0 | correct | Sharpe (1994); Lo (2002) section on time aggregation |
| l12 | s[5].w.lines[3..4] | t = SR√T; standard error of SR about 1/√T | correct | Lo (2002) eq. for iid returns; script: MC l12 SE |
| l12 | s[5].explain | SR 0.79; t reaches 2 at about 6.3 years | correct | script |
| l12 | s[6] | Q's Sharpe 1.59 is twice P's 0.79; t ranks them at T = 1 | correct | arithmetic |
| l12 | s[7] | 20 no-skill tests: P(at least one abs(t) > 2) = 0.606; slips 0.91, 0.0455, 0 | correct | script |
| l12 | s[8] | Sharpe 1.0 over 2 years: band −0.41 to 2.41 contains 0; 4 years to clear 2 standard errors | correct | 1 ± 2/√T |
| l12 | s[9] | P(losing year) = Φ(−0.794) = 0.2136; slips 0.4801, 0, 0.7863 | correct | script |
| l12 | s[9].explain | Sharpe 0.79; one year in five is a loss | correct | arithmetic |
| l12 | summary | ideas, formula, note, trap | correct | restate |
| l12 | q[0] | 1.5%/√400 = 0.075% | correct | arithmetic |
| l12 | q[1] | SR 2.0 over 3 months is t = 1; slips 0.5, 4, 2 | correct | feedback names each route |
| l12 | q[2] | SR 0.5 needs 16 years | correct | (2/0.5)² |
| l12 | q[3] | P(t > 2) = 0.0228, one in 44 | correct | 1/0.0228 |

## l13-approximating-binomial

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l13 | s[0] | at p = 0.05 the bell fits Bin(30, p) poorly; np(1−p) = 1.43 | correct | 30 × 0.05 × 0.95 |
| l13 | s[0].explain | a common rule of thumb asks for np(1−p) ≥ 10 | correct | stated as a rule of thumb; one of the common textbook guidelines |
| l13 | s[1] | X ≥ 15 starts the area at 14.5; other cut points mis-cover | correct | Ross 5.4.1 continuity correction |
| l13 | s[2] | estimate 0.0579 (0.0578 unrounded); slips 0.9421, 0.0361, 0.0216 | correct | script |
| l13 | s[2].explain | exact 0.0553 | correct | script |
| l13 | s[3] | errors −0.0192 and +0.0026; uncorrected a third too low | correct | 0.0192/0.0553 = 35% |
| l13 | s[4] | P(X<9) = P(X ≤ 8) ends at 8.5; Φ(−1.124) = 0.1306 against exact 0.1308 | correct | script |
| l13 | s[5].prose | rule: P(X ≤ k) ≈ Φ((k + 0.5 − np)/√(np(1−p))) | correct | Ross 5.4.1 |
| l13 | s[5] | P(X=12) from 11.5 to 12.5: 0.161 against exact 0.162 | correct | script |
| l13 | s[5].explain | rule of thumb is cautious near p = 0.5 | correct | symmetric case |
| l13 | s[6].w.lines | binomial as a sum of indicators, CLT, half-unit step | correct | De Moivre–Laplace |
| l13 | s[7] | Bin(100, 0.02): exact 0.0508, Poisson 0.0527, normal 0.0371; use the Poisson | correct | script |
| l13 | s[7].options[2].why | normal is 27% too low | correct | (0.0508 − 0.0371)/0.0508 |
| l13 | s[7].explain | for p near 1 count failures | correct | symmetry of the binomial |
| l13 | s[8] | 60 or more wins in 100 flips: 0.0287, exact 0.0284, one time in 35; slips 0.0228, 0.9713, 0.0179 | correct | script |
| l13 | s[9] | 1,000 loans: normal 0.0159; exact 0.0207; Poisson 0.0218; slips 0.314, 0.0119, 0.9841 | correct | script |
| l13 | s[9].explain | real defaults are correlated, which fattens the tail | correct | script: MC l1 dependence |
| l13 | summary | ideas, formula, note, trap | correct | restate |
| l13 | q[0] | poll of 1,000: about 3 points at 95% | correct | 1.96 × 0.0158 |
| l13 | q[1] | z = (40.5 − 50)/5 = −1.9; exact 0.0284 | correct | script |
| l13 | q[2] | P(X=50) ≈ 0.0796, exact 0.0796 | correct | script |
| l13 | q[3] | only Bin(50, 0.5) passes: 12.5; others 4.98, 2.7, 1.8 | correct | arithmetic |

## review-1

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-1 | i[0] | 20/64 = 0.3125; slips 0.0156, 0.5 | correct | C(6,3) |
| review-1 | i[1] | 0.7⁴ = 0.2401; slips 0.1681, 0.7599, 0.1029 | correct | arithmetic |
| review-1 | i[2] | Pois(2.5): P(≤1) = 0.2873; slips 0.0821, 0.2052 | correct | 3.5e^−2.5 |
| review-1 | i[3] | two hearts 0.2743; binomial 0.2637; 5 cards about 10% of the deck | correct | script; 13 hearts in 52 |
| review-1 | i[4] | count to the first acceptance is geometric, mean 6.7 | correct | C&B 3.2.5 |
| review-1 | i[5] | Poisson approximation e⁻² = 0.1353; exact 0.1340 | correct | 0.99^200 |
| review-1 | i[6] | E[Y] = 9; conventions differ by exactly 1 | correct | 1/p − 1 |
| review-1 | i[7] | variance 1.6 × 40/49 ≈ 1.3061; slips 1.6, 1.28, 2 | correct | script |

## review-2

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-2 | i[0] | P(X>1) = 0.75 for x/2 on [0,2] | correct | 1 − ¼ |
| review-2 | i[1] | variance 3; slips 0.5, 36, 5 | correct | 36/12 |
| review-2 | i[2] | e^−1.5 = 0.2231; slips 0.0498, 0.7769 | correct | Poisson process gaps |
| review-2 | i[3] | 0.8186; slips 0.6827, 0.9545, 0.1359 | correct | Φ(2) − Φ(−1) |
| review-2 | i[4].w.answer | E[X] = 2 for 2/x³ on x ≥ 1 | correct | ∫2/x² |
| review-2 | i[4].w.wrong half, fb.half | 0.5: "You integrated 2/x³ times 1/x" | wrong | finding 1: ∫₁^∞ (2/x³)(1/x) dx = 2/3, not 0.5; script KNOWN F1 |
| review-2 | i[4].explain | E[X²] infinite: a fat tail | correct | ∫2/x diverges |
| review-2 | i[5] | e^−0.8 = 0.4493 by memorylessness; e^−2.8 option | correct | ratio |
| review-2 | i[6] | σ = √(2 ln 1.1) ≈ 0.4366; slips 0.4472, 0.1906 | correct | script |
| review-2 | i[7] | sd 3.29/1.645 = 2%; slips 1.68%, 1.414% | correct | arithmetic |
| review-2 | i[8] | P(S₂ < 100) = Φ(−0.165) ≈ 0.4345; slips 0.353, 0.4536, 0.5 | correct | script |

## review-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-3 | i[0] | sd of the share 0.005; slips 2.5e−5, 50, 5e−5 | correct | 0.5/100 |
| review-3 | i[1] | Chebyshev 1/9; slips 1/3, 0.0027 | correct | k = 3 |
| review-3 | i[2] | Chebyshev 0.04 beats Markov 0.5 on P(X ≥ 20) | correct | {X ≥ 20} inside {abs(X − 10) ≥ 10} |
| review-3 | i[3] | 36 trades: Φ(−0.8) = 0.2119; slips 0.447, 0, 0.7881 | correct | script |
| review-3 | i[4] | 900 days, about 3.6 years; slips 30, 225, 15 | correct | (2 × 1.5/0.1)² |
| review-3 | i[5] | 1.14 expected flukes; chance of at least one about 0.68 | correct | script |
| review-3 | i[6] | Bin(50, 0.4): 0.0968, exact 0.0978; slips 0.0745, 0.0562 | correct | script |
| review-3 | i[7] | Bin(40, 0.5) window 0.5704, exact 0.5704; slips 0.4729, 0.2852 | correct | script |
| review-3 | i[8] | S_n/n settles; (S_n − 3.5n)/√n near normal; the raw gap grows like √n | correct | LLN and CLT |

## homework-1

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| homework-1 | i[0] | P(X ≥ 2) = 0.2642; slips 0.6358, 0.3716, 0.6284 | correct | script |
| homework-1 | i[1] | Poisson mean proof; E[X(X−1)] = λ² | correct | C&B 3.2.4 |
| homework-1 | i[2] | E[X given X>3] = 8; slips 5, 7, 3 | correct | memorylessness |
| homework-1 | i[3] | e^−0.5 = 0.6065; slips 0.0498, 0.5, 0.0083 | correct | arithmetic |
| homework-1 | i[4] | 1 − C(45,10)/C(50,10) = 0.6894; binomial 0.6513 understates | correct | script |
| homework-1 | i[5] | E[T] = 2/p for the second pass | correct | negative binomial mean, C&B 3.2.5 |
| homework-1 | i[6] | variance 15 against 3.92 means positive covariances between loans | correct | Var of a sum of identically distributed indicators exceeds npq only with positive average covariance |
| homework-1 | i[7] | 0.7361; 0.3874 is P(X=1) and also the sum with the factor 10 dropped | correct | 0.9⁹(0.9 + 0.1) |
| homework-1 | i[8].model | Cov(I_i, I_j) = −p(1−p)/(N−1); Var = np(1−p)(N−n)/(N−1); pmf check | correct | algebra; script: l4 s6 variance |
| homework-1 | i[8].rubric | points match the model steps | correct | cross-read |
| homework-1 | i[9].model (a) | T = min(X, m): P(T=k) = q^(k−1)p, P(T=m) = q^(m−1) | correct | enumeration |
| homework-1 | i[9].model (b),(c) | E[T] = (1 − q^m)/p two ways | correct | script: h1 capped wait by the series |
| homework-1 | i[9].model (d) | cancel chance 0.85^10 ≈ 0.1969; E[T] ≈ 5.354; limit 6.667 | correct | script |
| homework-1 | i[9].rubric | required rows match the model | correct | cross-read |

## homework-2

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| homework-2 | i[0] | survival e^(−x/3) | correct | integral |
| homework-2 | i[1] | P(X>2) = 1/8 for 3/x⁴; slips 0.1875, 0.875 | correct | integral |
| homework-2 | i[2] | E[T] = 1/λ by parts | correct | C&B 3.3 |
| homework-2 | i[3] | σ = 30/(1.645 + 1.2816) ≈ 10.25, μ ≈ 8.14; slips 9.254, 9.119 | correct | script |
| homework-2 | i[4] | hazard −ln 0.85/5 ≈ 3.25%; slips 3%, 3.198% | correct | Hull 24.1 |
| homework-2 | i[5] | P(90 < S₁ < 110) = 0.3787; slips 0.3526, 0.371 | correct | script |
| homework-2 | i[6] | lognormal 99% VaR £352,900; slips 415,200, 339,800, 371,990 | correct | script; loss measured from today's value, stated |
| homework-2 | i[6].explain | −41.5% is a log return of −0.536 | correct | ln 0.585 |
| homework-2 | i[7].model | exponential density, CDF, median, memorylessness, survival 0.7408 and 0.1393 | correct | C&B 3.3; arithmetic |
| homework-2 | i[7].model (e) | constant hazard gives no gain in safety; market hazards vary with horizon and time | correct | Hull 24.1 to 24.4 |
| homework-2 | i[8].model (a),(b) | P(T_n > t) = (1 − λ/n)^floor(nt) → e^−λt by a squeeze | correct | derivation checked line by line |
| homework-2 | i[8].model (c) | 0.1285 and 0.1347, both below e⁻²; ln(1 − x) < −x | correct | script |
| homework-2 | i[8].model (d) | Var(D) = (b − a)²/12; mean 0.03, sd 0.0289 | correct | algebra |
| homework-2 | i[8].rubric | required rows match the model | correct | cross-read |

## homework-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| homework-3 | i[0] | 1,167 rolls; slips 59, 35 | correct | 2.9167/0.0025 |
| homework-3 | i[1] | Chebyshev 0.0711 beats Markov on abs(X) 0.2 | correct | (40/150)² |
| homework-3 | i[2].w.lines | weak law from Chebyshev for independent draws with finite variance | correct | C&B 5.5.2 |
| homework-3 | i[2].explain | iid draws need only a finite mean, by a harder argument | correct | Khinchin, Durrett 2.2.9 |
| homework-3 | i[3] | insurer shortfall 1 − Φ(1.25) = 0.1056; slip 0.49 | correct | arithmetic |
| homework-3 | i[4] | 14.3 years to t = 3; slips 6.3, 3.8 | correct | (3/0.794)² |
| homework-3 | i[5] | Bin(400, 0.05): normal 0.0146; exact 0.0190; Poisson 0.0218 | correct | script |
| homework-3 | i[6].w.solution | exact_tail and normal_tail | correct | script: solution passes, starter fails |
| homework-3 | i[7].model 1 to 3 | SR 1.06, standard error 0.82, t 1.30, 900 days | correct | arithmetic |
| homework-3 | i[7].model 4 | best of 10: 1 − (1 − 0.097)^10 ≈ 0.64 | correct | script |
| homework-3 | i[7].model 5 | positive serial correlation makes the standard error an underestimate; fat tails slow the approach | correct | Lo (2002); script: MC h3 |
| homework-3 | i[8] | 5-day sum exactly normal only for the normal stock; sd 2.24% | correct | C&B 5.2.9 |
| homework-3 | i[9].model (a),(b) | Markov from an indicator; Chebyshev in ε form | correct | Ross 8.2 |
| homework-3 | i[9].model (c) | weak law for independent, not identically distributed bets with capped variance; counterexample σ_i² = i | correct | Chebyshev weak law, Durrett 2.2.3 |
| homework-3 | i[9].model (d) | variances 0.99 and 3.36; n = 967 by Chebyshev; about 131 by the normal | correct | arithmetic |
| homework-3 | i[9].model (d) exact | 0.0528 at n = 131; first at or below 0.05 at n = 136; stays below after | correct | script: h3 desk exact (checked to n = 600) |
| homework-3 | i[9].rubric | required rows match the model | correct | cross-read |

## problems-1

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| problems-1 | i[0].p[0] | 0.996^400 = 0.2012; slips 0.2019, 0.7988, 0.996 | correct | script |
| problems-1 | i[0].p[1] | Pois(1.6): P(X ≥ 4) = 0.0788; slips 0.2166, 0.0551, 0.9212, 0.0237 | correct | script |
| problems-1 | i[0].p[2] | 0.9212^30 = 0.0852; slips 0.9148, 0.094, 0.0007 | correct | script; e^−2.364 = 0.094 |
| problems-1 | i[0].p[3] | mean wait 12.7 minutes; slips 11.7, 1.1, 4.6, 2.4 | correct | 1/0.0788 |
| problems-1 | i[0].p[4] | smallest k is 6: 42 minutes at 5, 166 at 6 | correct | script |
| problems-1 | i[1].p[0] | 7/10 × 6/9 × 3/8 = 0.175; slips 0.147, 0.4667, 0.3 | correct | arithmetic |
| problems-1 | i[1].p[1] | P(X=0) = 35/210 = 1/6; slips 0.2401, 0.8333, 0.5 | correct | C(7,4)/C(10,4) |
| problems-1 | i[1].p[2] | geometric model gives 0.2401 against 1/6 | correct | 0.7⁴ |
| problems-1 | i[1].p[3] | fifth call finds a taker with chance 3/6; slips 0.3, 0.0833, 0.3333 | correct | conditional count |
| problems-1 | i[1].p[4] | drawing without replacement is not memoryless; chance climbs 0.3 to 0.5 | correct | hazard rises |
| problems-1 | i[1].p[4].explain | memorylessness needs independent calls with a fixed chance | correct | the geometric is the only memoryless law on the positive integers, Ross 4.8.1 |
| problems-1 | i[2].p[0] | 0.65² × 0.35 = 0.1479; slips 0.0796, 0.2746, 0.4225 | correct | arithmetic |
| problems-1 | i[2].p[1] | 0.65⁶ = 0.0754; slips 0.116, 0.9246, 0.0406, 0.0018 | correct | arithmetic |
| problems-1 | i[2].p[2] | conditional chance again 0.0754 | correct | memorylessness |
| problems-1 | i[2].p[3] | P(X=12) = 0.0057; slips 0.0754, 0.0683, 0.0368 | correct | 0.65¹² |
| problems-1 | i[2].p[4] | P(X ≥ 10) = 0.1513, one fund in seven; slips 0.0104, 0.1088, 0.0424 | correct | script |
| problems-1 | i[3].p[0] | E[X] = 1.5; slips 0.03, 1.2 | correct | nK/N |
| problems-1 | i[3].p[1] | variance 1.4193; slips 1.455, 1.4186, 1.5, 1.1914 | correct | script |
| problems-1 | i[3].p[2] | 0.97^50 = 0.2181; exact 0.2139; Poisson 0.2231 | correct | script |
| problems-1 | i[3].p[3] | n = 152; 0.98994 at 151; slip 76 | correct | script |
| problems-1 | i[3].p[4] | exact smallest n is 146, so 152 is safe; the binomial errs on the safe side here | correct | script |

## problems-2

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| problems-2 | i[0].p[0] | c = 2/9; slips 1/3, 1/9, 4.5 | correct | area 4.5c |
| problems-2 | i[0].p[1] | P(T>2) = 1/9; slips 8/9, 2/9, 1/3 | correct | (3 − t)²/9 |
| problems-2 | i[0].p[2] | E[T] = 1; slips 1.5, 4.5 | correct | integral |
| problems-2 | i[0].p[3] | exponential with mean 1: e⁻² = 0.1353; slip 0.2636 | correct | e^(−4/3) |
| problems-2 | i[0].p[4] | triangle conditional 0.25; not memoryless; slips 0.6065, 0.0278, 0.6944 | correct | ratio of survival functions |
| problems-2 | i[1].p[0] | median 80e^0.015 ≈ 81.21; slips 84.95, 80, 88.86 | correct | arithmetic |
| problems-2 | i[1].p[1] | mean 80e^0.06 ≈ 84.95 | correct | Hull 15.3 |
| problems-2 | i[1].p[2] | P(S₁ < mean) = Φ(0.15) = 0.5596 | correct | σ/2 |
| problems-2 | i[1].p[3] | P(S₁ > 100) = 0.2451 with z = 0.69; 0.2439 unrounded; slips 0.7549, 0.2946, 0.3483 | correct | script |
| problems-2 | i[1].p[4] | 95% VaR £30.42 from today's price, stated; slips 28.14, 34.89, 35.37, 39.48 | correct | script; Jorion ch. 5 absolute VaR |
| problems-2 | i[2].p[0] | P(X < −3) = 0.125; slips 0.25, 0.0833, 0.875 | correct | triangle area |
| problems-2 | i[2].p[1] | Var = 6; slips 3, 2.4495, 12 | correct | integral |
| problems-2 | i[2].p[2] | VaR 6 − √3.6 ≈ 4.10; slips 4.66, 3.32 | correct | arithmetic |
| problems-2 | i[2].p[3] | normal VaR 1.645√6 ≈ 4.03; slips 9.87, 4.8, 4.1 | correct | arithmetic |
| problems-2 | i[2].p[4] | at 99% the normal exceeds the triangle by 0.55; slips −0.55, −0.07, 8.8 | correct | script |
| problems-2 | i[3].p[0] | survival e^−0.05 = 0.9512 | correct | Hull 24.1 |
| problems-2 | i[3].p[1] | mean given survival 40e^0.04 ≈ 41.63; median 39.16 | correct | arithmetic |
| problems-2 | i[3].p[2] | E[S₁] ≈ 39.60; slips 41.63, 39.55, 37.25 | correct | script; law of total expectation |
| problems-2 | i[3].p[3] | P(S₁ > 40 given survival) = 0.4761; slips 0.5239, 0.5438, 0.5 | correct | z = 0.06 |
| problems-2 | i[3].p[4] | P(S₁ > 40) = 0.4529 by independence; slip 0.5173 | correct | product |

## problems-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| problems-3 | i[0].p[0] | day sd £180; slips 5,400, 6, 32,400 | correct | √(900 × 36) |
| problems-3 | i[0].p[1] | P(losing day) ≈ 0.0228; slips 0.9772, 0.0456, 0.4734 | correct | Φ(−2) |
| problems-3 | i[0].p[1].explain | "the day almost never does" lose | misleading | finding 9: 0.0228 is about one day in 44, and part 3 goes on to count 5.7 losing days a year |
| problems-3 | i[0].p[2] | Bin(250, 0.0228): normal estimate 0.0537; slips 0.9463, 0.0343, 0.0211, 0.0558 | correct | z = 1.61, each slip recomputed |
| problems-3 | i[0].p[3] | exact 0.0626, Poisson 0.0648; use the Poisson; normal 14% too low | correct | script |
| problems-3 | i[0].p[3].options[2].why | "The theorem needs enough spread" | imprecise | finding 8: the theorem is a limit and holds; the approximation at this n needs enough spread |
| problems-3 | i[1].p[0] | sd 10; slips 100, 0.025, 14.14 | correct | √100 |
| problems-3 | i[1].p[1] | 216 or more: 0.0606, exact 0.0605, one in 16; slips 0.9394, 0.0548, 0.0495, 0.1212 | correct | script |
| problems-3 | i[1].p[2] | best of 12: 0.5277; slips 0.7272, 0.0606, 0.4915 | correct | script |
| problems-3 | i[1].p[3] | cut-off k = 227; exact binomial agrees; slips 217, 226 | correct | script |
| problems-3 | i[1].p[4] | 625 calls for expected t of 2; slips 157, 25, 601 | correct | (2 × 0.5/0.04)² |
| problems-3 | i[2].p[0] | Markov 12/36 = 1/3; slips 3, 0.1111 | correct | Ross 8.2 |
| problems-3 | i[2].p[1] | Chebyshev 1/36 for the one-sided event; slips 1/6, 1/81, 1/3 | correct | one-sided event inside the two-sided |
| problems-3 | i[2].p[2] | n = 320; slips 17, 80, 62 | correct | 16/0.05 |
| problems-3 | i[2].p[3] | n = 62 by the normal; slips 61, 44, 8, 320 | correct | script; "if the daily counts are not too lopsided" is stated |
| problems-3 | i[3].p[0] | standard error 0.6667; slips 0.1111, 4, 0.4444 | correct | 4/6 |
| problems-3 | i[3].p[1] | t = 1.8; slips 0.3, 10.8, 0.56 | correct | arithmetic |
| problems-3 | i[3].p[2] | Chebyshev bound 0.3086; slips 0.5556, 0.0719 | correct | 1/3.24 |
| problems-3 | i[3].p[3] | normal 0.0718, one record in 14; slips 0.0359, 0.3086, 0.9641 | correct | 2(1 − 0.9641) |
| problems-3 | i[3].p[4] | 45 months; slips 12, 44, 43 | correct | (8/1.2)² = 44.4 |

## fluency-l1-counting-successes

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| fluency-l1 | families[0] | key C(n,k)p^k(1−p)^(n−k); slips one path, swapped powers; guards stop a slip equalling the key | correct | formula read; number script 0 failures |
| fluency-l1 | families[1] | key np(1−p); slips np and p(1−p) | correct | formula read |
| fluency-l1 | families[2] | key (1−p)^n; slips p^n and 1 − p^n; p = 0.5 excluded so slips differ from the key | correct | formula read |

## fluency-l7-bell-curve

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| fluency-l7 | families[0] | z = (x − μ)/σ; slips z/σ (divided by variance) and −z | correct | (x − μ)/σ² = z/σ |
| fluency-l7 | families[1].vars.tab | ten Φ values from 0.4 to 3 | correct | standard table |
| fluency-l7 | families[1] | key by direction and sign; slips other tail and the z value | correct | four cases checked by hand |
| fluency-l7 | families[2] | key 2Φ(z) − 1; slips Φ(z) and Φ(z) − 0.5 | correct | symmetry |

## Conventions noted (no finding)

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l3, l10, problems-3 | s[9], s[8], i[0] | a year is 250 trading days | correct | stated each time it is used |
| l7, l12 | s[9], s[3], s[5] | a year is 252 trading days | correct | stated each time; 250 and 252 are both in practitioner use |
| l7, homework-2, problems-2 | s[9], i[6], i[1].p[4] | VaR is a positive loss measured from today's value, not from the mean | correct | stated in each item; Jorion ch. 5 |
| l12 | s[4] | the t-ratio uses a known σ, with the sample sd noted | correct | stated once where it first matters |

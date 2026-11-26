# Claim ledger: markov levels 4 and 5 (blind audit, round 1)

Scope: `l13` to `l22`, `review-4`, `review-5`, `homework-4`, `homework-5`, `problems-4`, `problems-5`. Stage 1, full depth: these levels had no second read, so every row was read and judged by hand. A row that names several slips covers each slip value, which was recomputed. "script" means a check in `docs/reports/markov-L4-5-concepts.py` (exact fractions or linear algebra, or seeded Monte Carlo). "grade-all" means `node tools/grade-all.mjs --code --file`, which ran the 12 Python widgets against their hidden tests with 0 failures. "F<n>" points to the finding in `docs/reviews/audit-markov-4-5.md`.

Rows: 291. Verdicts: 276 correct, 10 imprecise, 1 misleading, 4 wrong, 0 unverified.

Sources used: Norris, *Markov Chains* (1.7 invariant distributions and return times, 1.8 convergence, 1.9 time reversal and detailed balance, 1.10 ergodic theorem, 2.3 to 2.4 Poisson processes). Levin, Peres and Wilmer, *Markov Chains and Mixing Times* (LPW: 1.3 periodicity, 1.6 reversibility, 2.5 birth-death chains, 3.2 Metropolis and Hastings, 4.5 distance to stationarity, 9.1 networks). Williams, *Probability with Martingales* (10.3 to 10.4 definitions and examples, 10.7 betting systems, 10.8 stopping times, 10.10 Doob's optional stopping theorem, 10.11 ABRACADABRA, 10.12 hitting times of the walk). Grimmett and Stirzaker, *Probability and Random Processes* (3.7 random sums, 6.8 and 6.13 Poisson process and thinning, 10.2 to 10.3 renewals, Wald and excess life, 12.1 martingales, 12.7 and 12.9 continuous time and ruin). Durrett, *Probability: Theory and Examples* (4.8 optional stopping). Li (1980), "A martingale approach to the study of occurrence of sequence patterns", *Annals of Probability* 8. Hull, *Options, Futures and Other Derivatives*. Shreve, *Stochastic Calculus for Finance* I and II. Geyer, "Introduction to MCMC", *Handbook of Markov Chain Monte Carlo* ch. 1.

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l13 | screens[0] | At π = (2/3, 1/3) over 1,500 days: 100 bull-to-bear and 100 bear-to-bull switches | correct | 1000 × 0.1 = 500 × 0.2 = 100. script |
| l13 | screens[0].feedback.byKey r0c1, r1c1 | Only days in the starting state can switch | correct | Flow = π_i P_ij |
| l13 | screens[1].prose | F_ij = π_i P_ij; detailed balance π_i P_ij = π_j P_ji; a chain with such a π is reversible | correct | Norris 1.9 (Thm 1.9.3); LPW 1.6 eq. (1.30) |
| l13 | screens[1].prose | "filmed and run backwards, it looks the same" | correct | Norris Thm 1.9.1: true for the chain started from π, which screen 0 sets ("sits at its stationary split") |
| l13 | screens[1].widget (key 1/15) | Backward share of bull-then-bear equals forward share of bear-then-bull = 1/3 × 0.2 | correct | Time reversal: P̂_ij = π_j P_ji / π_i. script |
| l13 | screens[1].wrong 0.1, 0.2, 0.1333 | transition chance; bear-to-bull chance as a share; both switches added | correct | Values match the named slips (2/15 = 0.1333) |
| l13 | screens[1].explain | Equal flows mean the backward film has the same switching rates | correct | Norris Thm 1.9.3 |
| l13 | screens[2].prose | Inventory chain 0..3, buy 0.3, sell 0.5; "assume" flow up from i matches flow down from i+1 | correct | The assumption is the cut identity, true for any stationary birth-death chain (LPW 2.5) |
| l13 | screens[2] key 0.6 and slips 1.6667, 0.3, 0.5, 0.2 | π_{i+1}/π_i = 0.3/0.5 | correct | derivation; slip values match feedback |
| l13 | screens[2].explain | Selling more likely than buying, so larger inventories are rarer | correct | ratio < 1 |
| l13 | screens[3] | Weights 1, 0.6, 0.36, 0.216, total 2.176 | correct | script |
| l13 | screens[4] key 0.2647; slips 0.576, 0.1654, 0.144, 0.5 | (0.36 + 0.216)/2.176 | correct | script; each slip value recomputed |
| l13 | screens[4].explain | Column check 0.4596 × 0.7 + 0.2757 × 0.5 = 0.4596 | correct | script (πP = π to 1e-12) |
| l13 | screens[5] (order and every line) | Detailed balance for all pairs plus Σπ = 1 implies πP = π: sum over i, factor π_j, row sums to 1 | correct | Norris Lemma 1.9.2; LPW Prop. 1.20 |
| l13 | screens[5].feedback.byKey o2 to o5 | Reasons for each line's place | correct | each follows from the proof order |
| l13 | screens[6].prose | Birth-death chain: moves to a neighbour or stays; non-neighbour pairs balance trivially | correct | LPW 2.5 |
| l13 | screens[6].prose | "Every such chain on a finite set of states is reversible, with π_{i+1} = π_i P_{i,i+1}/P_{i+1,i}" | imprecise | True when every down chance P_{i+1,i} is positive (LPW 2.5 assumes it). With a zero down chance the formula divides by zero, and screen 9 itself says a one-way arrow rules out reversibility. F1 |
| l13 | screens[6] key and options | Up 0.6, down 0.1, hold at walls: reversible with π_{i+1} = 6π_i; drift does not break reversibility; equal chances not needed | correct | script (detailed balance holds on all pairs) |
| l13 | screens[6].options[2].why | "At the wall, probability piles up until flow down matches flow up" | correct | cut identity |
| l13 | screens[7] key and options | 3-cycle 0.8 / 0.2: π uniform, flows 0.267 and 0.067, stationary but not reversible | correct | script; LPW Example 1.6 style (biased walk on a cycle) |
| l13 | screens[7].explain | "Detailed balance is a stronger condition than stationarity" | correct | Norris 1.9 |
| l13 | screens[7].options[2].why | Each state receives as much as it sends, so πP = π | correct | doubly stochastic P |
| l13 | screens[8] key 64; slips 12, 3, 1 | π_A = 64π_A forces π_A = 0, no balanced distribution | correct | Kolmogorov cycle criterion: 0.8³ ≠ 0.2³ (Durrett, Essentials of Stochastic Processes, 1.6) |
| l13 | screens[8].explain | "When balance has no solution, solve πP = π instead" | correct | finite chain always has a stationary π (LPW Prop. 1.14) |
| l13 | screens[9] key {B→C, C→A} and feedback | One-way arrows; balance would need 0.2π_B = 0 | correct | derivation |
| l13 | screens[9].explain | "Every arrow in a reversible chain needs a return arrow" | imprecise | True for an irreducible chain (π > 0 everywhere). The explain's own middle sentence carries the condition ("a chain that visits B"), so minor; joined to F1 |
| l13 | screens[10] key 8/15; slips 0.5, 0.5714, 0.6, 0.25 | Queue 0..3, join 0.3, leave 0.6: π = (8, 4, 2, 1)/15 | correct | script |
| l13 | screens[10].explain | Empty 53% of the time | correct | 8/15 = 0.533 |
| l13 | summary.ideas[0..2] | Detailed balance definition; balance plus Σ = 1 implies stationary; finite birth-death always reversible; stationary does not imply reversible | correct | as rows above (birth-death clause shares F1) |
| l13 | summary.trap | "Solving πP = π always works. Detailed balance can have no solution" | correct | LPW Prop. 1.14 (finite chains) |
| l13 | quiz[0] key 4/7; slips 1/3, 0.5, 2/7 | weights 1, 1/2, 1/4 | correct | script |
| l13 | quiz[1] key and options | F with row and column sums 1/3, F_12 = 1/6, F_21 = 0: stationary, not reversible; reversible iff F = F^T | correct | definition; "stationary needs row sums to equal column sums" is πP = π written in F |
| l13 | quiz[2] key and options | i = j pairs are identities; self-loops never break balance | correct | definition |
| l13 | quiz[3] key 1/3; slips 0.2, 0.12, 0.03 | P_21 = π_1 P_12 / π_2 | correct | script |
| l13 | quiz[3].explain | "The rarer state 2 must leave faster than state 1" | correct | meant for this pair: P_21 > P_12 when π_2 < π_1 |
| l14 | screens[0] key and options | After 10,000 steps A (most links) has the largest share: about 0.37, 0.25, 0.26, 0.12 | correct | π = deg/2E = (3, 2, 2, 1)/8; script simulation |
| l14 | screens[0].options[2].why | "A start is forgotten in the long run" | correct | ergodic theorem, Norris 1.10; this graph has a triangle so it is also aperiodic |
| l14 | screens[1] table and explain | Degrees 3, 2, 2, 1 add to 8 = twice the 4 links | correct | handshake lemma |
| l14 | screens[2] key 1/10; slips 0.125, 0.2, 0.25 | Adding E linked to A: degrees 4, 2, 2, 1, 1, total 10 | correct | script |
| l14 | screens[2].explain | "Adding a link anywhere takes time from every other venue" | correct | a venue not on the new link keeps its degree while 2E rises by 2 |
| l14 | screens[3] (lines and order) | P_ij = 1/deg(i); deg(i)P_ij = deg(j)P_ji = 1; Σdeg = 2E; π = deg/2E stationary by detailed balance | correct | LPW 1.4 Example 1.12 and 1.6; Norris Example 1.9.6 |
| l14 | screens[3].feedback.byKey o2 to o5 | Reasons for each line's place | correct | proof order |
| l14 | screens[4] key 8; slips 0.125, 4, 7, 3 | Mean return time to D is 1/π_D = 8 | correct | Kac: Norris Thm 1.7.7; LPW Prop. 1.19. script (exact linear solve and simulation) |
| l14 | screens[4].explain | "In general the mean return time to a state is 1/π_i"; for A it is 8/3 | correct | holds for an irreducible chain; every network here is connected, quiz[1] states the caveat |
| l14 | screens[4].feedback.byKey.between | Return time counts the arriving step | correct | definition of first return time |
| l14 | screens[5] key 4; slips 3, 2, 0.25 | Weighted walk: π_i ∝ strength; strengths 4, 3, 5, total 12 | correct | LPW 9.1 (network walk, π(x) = c(x)/c_G). script |
| l14 | screens[6] table | Knight degrees: 4×2, 8×3, 20×4, 16×6, 16×8, total 336; 168 undirected moves | correct | script enumerates the board |
| l14 | screens[7] key 168; slips 64, 336, 42, 84 | Corner return time 336/2 | correct | script (exact solve of the hitting equations gives 168); standard interview result |
| l14 | screens[7].explain | Central square returns every 42 moves | correct | 336/8 |
| l14 | screens[8] key 0; slips 0.25, 0.5, 0.125 | 4-cycle from A: P(at A at step 1,001) = 0; B and D each 1/2 at odd steps | correct | script (matrix power) |
| l14 | screens[8].explain | P^k alternates and never converges; time share still 1/4; "a walk on a network with no odd cycles is periodic like this" | correct | LPW 1.3: walk on a connected graph has period 2 iff bipartite |
| l14 | screens[9] key 1/2 and options | Star with 3 leaves: hub 3/6 | correct | script |
| l14 | screens[9].explain | "Equal shares hold only when every degree is equal" | correct | π ∝ deg on a connected graph |
| l14 | screens[10] code | network_pi adds w to both ends; return_time_mc averages gaps, weighted choice | correct | grade-all --code runs the solution against its 8 tests; method matches Kac |
| l14 | screens[10].explain | Strengths add to "2E"; mean return to D near 8 | correct | script |
| l14 | screens[11] key 1/3; slips 0.2, 0.6667 | Dealer degrees 4, 2, 3, 2, 1, total 12 | correct | script |
| l14 | screens[11].explain | "One dealer carries a third of the flow, a single point of failure. That is an argument for a central counterparty." | misleading | A central counterparty is itself a hub by design; the case for it is netting and mutualised default resources, not removing a hub (Hull, OFOD, ch. on OTC markets and CCPs). F2 |
| l14 | summary.ideas[0..2], formula, trap | π = deg/2E reversible; weighted version; return time 1/π; bipartite: π exists, P^k does not converge; two pieces: more than one π | correct | rows above |
| l14 | quiz[0] key 6; slips 2, 4, 3 | Leaf of a 3-star returns every 6 steps | correct | script |
| l14 | quiz[1] key 1/2 and options | Two components: walker stays on A-B; formula needs one connected network | correct | Norris 1.7 (uniqueness needs irreducibility) |
| l14 | quiz[2] key 6; slips 3, 4, 12 | Strengths 3, 4, 3, 2 total 12 | correct | script |
| l14 | quiz[3] key and options | Uniform shares exactly when the graph is regular | correct | π ∝ deg |
| l15 | screens[0].prose | Flat prior on seven hit rates, 12 wins of 20: posterior ∝ p^12 (1−p)^8 | correct | Bayes on a grid; binomial coefficient cancels |
| l15 | screens[0].prose | Metropolis rule: propose ±1 with chance 1/2, move with chance min(1, w_new/w_old), else stay | correct | Metropolis et al. (1953); LPW 3.2 |
| l15 | screens[0] key 0.898; slips 1, 1.1138, 0.449 | w(0.65)/w(0.60) | correct | script |
| l15 | screens[0].wrong "bigger" value 0 | slip with no feedback line | correct | falls to generic; no claim made |
| l15 | screens[0].explain | "We never needed the total of the weights" | correct | ratio only |
| l15 | screens[1].canvas P | Transition matrix of the chain | correct | script rebuilds P from w to 4 dp |
| l15 | screens[1] key | A flat step is a rejected proposal; the state counts again | correct | LPW 3.2 |
| l15 | screens[1].options[2].why | "Flat steps are rejections, which are common near the peak" | wrong | In this chain the stay chance is lowest at the peak: P_ii = 0.50, 0.26, 0.20, 0.13, 0.10 (at 0.60), 0.15, 0.50. script. F3 |
| l15 | screens[1].explain | Counting repeats makes the visit shares right | correct | screen 5 and script |
| l15 | screens[2] key 18; hints 0.099 at k = 10, 0.187 at k = 5, target 0.042 | P(at 0.40 after k steps) from start 0.40 | correct | script (matrix powers) |
| l15 | screens[2].feedback.correct and explain | "After about 18 steps the start is forgotten"; "After that the chain behaves as if it began at the posterior" | imprecise | At k = 18 the bar is 0.059 against 0.042 and the total variation distance from the posterior is 0.069 (0.051 at k = 20); burn-in reduces start bias, it does not remove it at a fixed step. script. F4 |
| l15 | screens[2].explain | Burn-in: early samples over-represent the start and are discarded | correct | Geyer, Handbook of MCMC ch. 1.11, treats it as optional practice; the quiz option on screen 6 says the theorem does not need it |
| l15 | screens[3] (lines and order) | π_i P_ij = min(w_i, w_j)/2Z both ways, so detailed balance; Z never used; long-run shares are the posterior | correct | LPW 3.2; chain is irreducible on the grid |
| l15 | screens[4] key 1/7 and options | Always accepting gives the proposal walk's own stationary law, uniform | correct | symmetric P; script |
| l15 | screens[5] key 0.5; slips 0.75, 0.25, 0.3333 | Two states, weights 1 and 3: chain samples (1/4, 3/4); moves-only record alternates | correct | script simulation |
| l15 | screens[6].prose | Strong law: running average of independent draws with mean μ converges with probability 1; stronger than the weak law | correct | Williams 12.10 (iid, finite mean); "draws" read as iid from one law |
| l15 | screens[6].prose and key | Ergodic theorem: for an irreducible chain the time average of f tends to Σπ_i f(i) | correct | Norris Thm 1.10.2 (positive recurrent; automatic on a finite state space) |
| l15 | screens[6].options[1..3].why | Steps are dependent; averages need only irreducibility, aperiodicity is for P^k; theorem holds from step 1 | correct | Norris 1.8 and 1.10 |
| l15 | screens[6].explain | Posterior mean 0.578; chain's running mean is slower because neighbouring steps are alike | correct | script: mean 0.578; lag-1 autocorrelation of the chain is positive |
| l15 | screens[7].prose | Metropolis-Hastings acceptance min(1, w_j q_ji / (w_i q_ij)) | correct | Hastings (1970); LPW 3.2.2 |
| l15 | screens[7] key 9/14; slips 1, 1.5, 0.4286, 3.5 | 3 × 0.3 / (2 × 0.7) | correct | script |
| l15 | screens[8] code and tests | exact_posterior and metropolis as given | correct | grade-all --code runs the solution against its 7 tests; rejected and off-grid steps are counted |
| l15 | screens[8].explain | "With 100,000 steps the shares agree with the exact posterior to about 0.003" | correct | script: max error over seeds is of that order |
| l15 | screens[9] key 0.7301; slips 0.8722, 0.5714, 0.3269 | Bars above 0.5 add to 0.7296; exact 0.7301 | correct | script |
| l15 | screens[9].explain | "The chain moved on 79% of its steps" | correct | script: stationary move rate 1 − Σπ_i P_ii |
| l15 | summary | Rule, weights only, detailed balance, burn-in, ergodic theorem, Hastings ratio, both traps | correct | rows above |
| l15 | quiz[0] key 0.4; slips 1, 2.5, 0.6 | 2/5 | correct | definition |
| l15 | quiz[1] key and options | Keep every step, repeats included | correct | screen 5 |
| l15 | quiz[2] key 5/8; slips 1/3, 0.5, 5 | π ∝ w | correct | script |
| l15 | quiz[3] key 1/3; slips 1, 0.75, 0.25 | Equal weights, q_ij = 0.25, q_ji = 0.75: accept j→i with 0.25/0.75 | correct | Hastings ratio; script |
| l16 | screens[0] key 1 | One empty minute in the seeded staircase | correct | canvas series read by script |
| l16 | screens[1].prose | Poisson process: independent counts in separate stretches, Poisson(λt) counts, independent Exp(λ) gaps | correct | Norris Thm 2.4.3 (the equivalent definitions) |
| l16 | screens[1] key e^-2; slips 0.5, 0.6065, 0.8647 | P(N(1) = 0) | correct | script |
| l16 | screens[1].explain | 1.35 empty minutes expected in 10 | correct | 10 e^-2 |
| l16 | screens[2] key 0.1606; slips 0.0361, 0.1083, 0.8333 | e^-6 6^5/5! | correct | script |
| l16 | screens[3] key 1.5; slips 0.5, 3, 6 | E[T_3] = 3/λ; T_3 is Gamma(3, rate 2); P(T_1 > 1) = e^-2 | correct | Norris 2.4; Grimmett and Stirzaker 6.8 |
| l16 | screens[4] table and explain | Independent Poisson streams merge with rate 5; next order is a buy with chance 3/5 | correct | Norris 2.4 (superposition); script Monte Carlo |
| l16 | screens[5] (lines and order) | P(T_b < T_s) = λ_b/(λ_b + λ_s) by conditioning; min is Exp(5) | correct | Norris Thm 2.3.3 |
| l16 | screens[6] key e^-6; slips 0.0498, 4.54e-5, 0.0183 | Thinning with p = 0.6: buys Poisson rate 3 | correct | Grimmett and Stirzaker 6.13 (thinning); script |
| l16 | screens[7] key and options | Thinned buy and sell counts are independent; rows match Poisson(2): 13.5%, 27.1%, 27.1%, 32.3% | correct | script Monte Carlo (conditional sell distribution given buys) |
| l16 | screens[7].explain | Independence "is special to Poisson streams"; with a fixed total extra buys take from sells | correct | binomial split of a fixed n is negatively dependent; script |
| l16 | screens[8].prose | At a time fixed in advance the wait ahead is Exp, mean 0.5, and "the time since the last trade is also exponential, mean 0.5" | imprecise | The age at time t is min(Exp(λ), t), mean (1 − e^{-λt})/λ: exponential only in the limit of a long-running process. script. F5 |
| l16 | screens[8] key 1; slips 0.5, 2, 0.25 | Mean length of the gap covering a fixed time is 2/λ | correct | inspection paradox, Grimmett and Stirzaker 10.3; exact value (2 − e^{-λt})/λ, 1.00 once t is past 3 minutes. script |
| l16 | screens[8].explain | Long gaps cover more of the clock; fixed-clock sampling sees gaps twice as long | correct | length-biased sampling; script |
| l16 | screens[9] code | Exponential gaps build the path; one uniform per arrival thins it | correct | grade-all --code runs the solution against its 8 tests |
| l16 | screens[10] key 0.216; slips 0.064, 0.125, 0.6 | Next three fills all buys: (3/5)^3, independent marks | correct | script Monte Carlo |
| l16 | summary.ideas[2] | "The gap that contains a fixed time is twice as long as a typical gap" | correct | on average; row above |
| l16 | summary.ideas[2], quiz[2].explain | A changing rate gives Poisson counts with the integrated rate, not a single-rate process | correct | inhomogeneous Poisson process, Grimmett and Stirzaker 6.13 |
| l16 | summary other lines, trap | Counts, gaps, merge, split independent | correct | rows above |
| l16 | quiz[0] key e^-1; slips 0.1353, 0.5, 0.6065 | 30 seconds at 2 a minute | correct | script |
| l16 | quiz[1] key 0.2 | Given one arrival in 10 minutes its time is uniform | correct | Norris Thm 2.4.6; script Monte Carlo |
| l16 | quiz[1].wrong 0.9817, 0.1353 | "at least one trade in 2 minutes", "e^-2" | imprecise | Both values need rate 2, which this item never states. F6 |
| l16 | quiz[2] key 90; slips 150, 50, 40 | 4 × 10 + 1 × 50 | correct | arithmetic |
| l16 | quiz[3] key e^-5; slips 0.1353, 0.0498, 0.1851 | No order of either kind | correct | script |
| review-4 | items[0] key 4/7; slips 1/3, 1/7, 2, 0.4 | Buy 0.4, sell 0.2 on 0..2: weights 1, 2, 4 | correct | script |
| review-4 | items[1] key 2.8; slips 1.4, 4, 0.3571 | Strengths 3, 3, 5, 3, total 14 | correct | script |
| review-4 | items[2] key 0.7402; slips 1, 1.35, 0.37 | w(0.50)/w(0.55) | correct | script |
| review-4 | items[3] key 0.0183; slips 0.3679, 0.0498, 0.0733 | Split rates 1 and 3, independent | correct | script |
| review-4 | items[4] key and options | P with π = (0.2, 0.4, 0.4) is reversible; symmetry of P not needed | correct | script (πP = π and balance on all pairs) |
| review-4 | items[5] key and options | 6-ring: π uniform, P(at venue 1 at odd k) = 0, P^k does not converge, time shares do | correct | LPW 1.3; script |
| review-4 | items[6] key 3/7; slips 0.5, 0.75 | Weights 1, 2, 4: move chances 1/2, 3/4, 1/4, π-weighted 3/7 | correct | script |
| review-4 | items[6].wrong "third" 0.3333 | "You averaged the three states equally" | wrong | The equal-weight average of 1/2, 3/4, 1/4 is 1/2, not 1/3. script. F7 |
| review-4 | items[7] key 0.00327 and explain | P(2 buys) = 0.04462, P(1 sell) = 0.07326, product equals P(N = 3) × C(3,2) 0.6² 0.4 | correct | script |
| review-4 | items[7].wrong one-minute 0.0558, sum 0.0222 | "You used one minute: means 3 and 2"; "You added the two chances" | wrong | The named slips give 0.0606 and 0.1179. script. F9 |
| review-4 | items[7].wrong merged 0.0076 | P(N = 3) at mean 10, ignoring who bought | correct | script |
| homework-4 | items[0] key 140; slips 84, 52.5, 64, 420 | King: 4 corners deg 3, 24 edge deg 5, 36 interior deg 8, total 420; corner return 420/3 | correct | script enumerates the king graph and solves the hitting equations |
| homework-4 | items[1] keys (birth-death, network walk, symmetric Metropolis) | These must be reversible | correct | LPW 2.5, 1.6, 3.2; the birth-death option shares the F1 caveat (a line chain with a one-way step also fits the unkeyed option 5) |
| homework-4 | items[1].options[3], [4].why | Rotating cycle: flows 0.267 and 0.067; one-way arrow forces a state never visited | correct | l13 rows |
| homework-4 | items[1].explain | Network walk has π_i P_ij = 1/2E both ways | correct | (deg/2E)(1/deg) |
| homework-4 | items[2] key 0.8; slips 0.2, 0.3333 | P(X_t = A given X_{t+1} = B) = π_A P_AB / π_B at stationarity | correct | Norris Thm 1.9.1. script simulation |
| homework-4 | items[2].wrong "half" 0.5 | "You treated the chain as reversible" | wrong | Treating the chain as reversible gives P_BA = 0.2, the "forward" slip, not 0.5. F8 |
| homework-4 | items[2].explain | Backwards the chain is the anticlockwise rule with chance 0.8 | correct | P*_ji = π_i P_ij / π_j |
| homework-4 | items[3] (lines, order, same-rank pair) | Time reversal P*_ji = π_i P_ij / π_j; reversible exactly when P* = P | correct | Norris Thm 1.9.1 and 1.9.3 |
| homework-4 | items[4] keys 0.3456 and 6 | Given 4 orders buys are Bin(4, 0.6); sells independent of buys | correct | Grimmett and Stirzaker 6.13; script Monte Carlo |
| homework-4 | items[5] key 19/27; slips 1/3, 8/27, 1/27 | Given 3 arrivals in [0, 3] the times are 3 independent uniforms | correct | Norris Thm 2.4.6; script Monte Carlo |
| homework-4 | items[6] key 0.13824; slips 0.2304, 0.02304 | Exactly 2 buys before the third sell: C(4,2) 0.6² 0.4³ | correct | negative binomial on the marks; script Monte Carlo |
| homework-4 | items[7] code and explain | Random-walk Metropolis with log acceptance; −∞ log weight never accepted; repeats kept | correct | grade-all --code runs the solution on all 7 tests; LPW 3.2 |
| homework-4 | items[8].model point 1 | Moves-only record has long-run shares ∝ π_i(1 − P_ii): (0.027, 0.081, 0.145, 0.212, 0.243, 0.207, 0.086); mean 0.5764; P(p > 0.5) = 0.747 | correct | stationary law of the jump chain (Norris 1.10 exercise); script |
| homework-4 | items[8].model point 2 | First 200 steps from 0.40 average 0.5721 in expectation, 0.0059 below 0.5780 | correct | script (sum of matrix powers) |
| homework-4 | items[8].model point 3 | Identical starts share one bias and cannot reveal non-convergence | correct | Gelman and Rubin (1992) |
| homework-4 | items[8].model point 4 | "a chain needs about 20 steps to forget its start"; sampling sd of her mean about 0.004 | imprecise | sd checked by script; the 20-step claim is F4 |
| homework-4 | items[8].model corrected procedure | Keep all steps, burn-in, dispersed starts, longer runs, Monte Carlo standard error by batch means; after dropping 20 steps the expected average is 0.5776, sd about 0.005 | correct | script; Geyer, Handbook of MCMC ch. 1 |
| homework-4 | items[8].rubric | Seven lines matching the model | correct | consistent with model |
| homework-4 | items[9] code, tests, explain | MH on a network with proposal 1/deg(i): accept min(1, w_j deg(i) / (w_i deg(j))); w_i P_ij symmetric; irreducible finite chain so the law is unique and visit shares converge | correct | Hastings ratio; grade-all --code runs the solution on all 11 tests |
| homework-4 | items[9].feedback.byKey test-2..test-9 | Descriptions of the tests | correct | match tests[1], [3], [4], [5], [8] |
| problems-4 | items[0].parts[0] key 0.1; slips 0.2, 0.4 | Degrees 4, 2, 2, 1, 1 | correct | script |
| problems-4 | items[0].parts[1] key 0.2; slips 0.4, 0.1 | Walk records late payers at 0.2 against true 0.4 | correct | arithmetic |
| problems-4 | items[0].parts[2] key and options | Uniform target with q_ij = 1/deg(i): accept min(1, deg(i)/deg(j)); accepting with 1/deg(i) gives H 16/26 | correct | Hastings; script (π ∝ deg² for the last option) |
| problems-4 | items[0].parts[3] key 0.75; slips 0.25, 0 | Stay at C | correct | script |
| problems-4 | items[0].parts[4] key 0.4; slips 0, 0.3, 0.25 | Stay chances 0, 0.25, 0.25, 0.75, 0.75 at share 1/5 | correct | script builds the chain |
| problems-4 | items[1].parts[0] key 0.6; slips 1.5, 0.4 | Next arrival is a taxi | correct | superposition |
| problems-4 | items[1].parts[1] key 1.5; slips 0.6667, 0.6 | Birth-death balance on the embedded chain | correct | derivation |
| problems-4 | items[1].parts[2] key 8/65; slips 27/65, 0.25, 0.2105 | Share of passengers who find the rank empty equals π_0 | correct | The state before an arrival is independent of the arrival's type (PASTA: Wolff 1982); script simulates the continuous-time rank |
| problems-4 | items[1].parts[3] key 11.8154; slips 29.5385, 0.1969, 59.8154 | 96 × 8/65 | correct | script simulation |
| problems-4 | items[1].parts[3].explain | Losses bunch, so a long-run rate, not a Poisson stream | correct | losses occur only while the state is 0 |
| problems-4 | items[1].parts[4] key 7.2796; slips 11.8154, 36.8531, 4.5358 | Fourth space: π_0 = 16/211 | correct | script |
| problems-4 | items[2].parts[0] key 3/14; slips 1/6, 3/7 | Degrees 3, 2, 3, 3, 2, 1 | correct | script |
| problems-4 | items[2].parts[1] key 14; slips 7, 6 | Return time to F; 13 hops elsewhere on average | correct | Kac; script |
| problems-4 | items[2].parts[2] key 8/7; slips 16, 0.1429, 1.3333 | Thinned audits at F | correct | thinning; exact for the mean. Independence of marks is an approximation that "thousands of messages" makes good |
| problems-4 | items[2].parts[3] key 0.3189; slips 0.6811, 0.8669, 0.2636 | e^{-8/7} | correct | script |
| problems-4 | items[2].parts[4] key 17; slips 16, 7, 2, 1 | t > 7 ln 10 = 16.12 | correct | script |
| problems-4 | items[3].parts[0] key 0.75; slips 1, 0.25 | Low to Mid: min(1, 5 × 0.3 / (2 × 1)) | correct | Hastings; script |
| problems-4 | items[3].parts[1] key 0.6; slips 0.8571, 0.42, 0.7 | Mid to High: 0.7 × 6/7; balance check 0.5 × 0.6 = 0.3 × 1 | correct | script |
| problems-4 | items[3].parts[2] key 0.3; slips 1.875, 0.12, 0.1 | P_ML from balance and from the rule | correct | script |
| problems-4 | items[3].parts[3] key 0.1; slips 0.35, 0.1167, 0.05 | Rejection share Σπ_i P_ii | correct | script |
| problems-4 | items[3].parts[4] key 50/77; slips 0.5, 0.0854, 0.2727 | Plain rule with an asymmetric proposal targets the wrong π | correct | script (stationary solve) |
| l17 | screens[0] keys 13, 13 | Fair £1 bets: forecast for toss 9 and toss 18 given £13 at toss 8 is £13 | correct | E[step] = 0; tower property (Williams 10.3) |
| l17 | screens[1] key 13.2; slips 13, 13.6, 14 | p = 0.6: 0.6 × 14 + 0.4 × 12; drift 2p − 1 = 0.2 | correct | script |
| l17 | screens[2].prose | Martingale: E[X_{n+1} given X_0..X_n] = X_n for every n, with E abs(X_n) finite; conditioning on the whole history | correct | Williams 10.3 (natural filtration); Grimmett and Stirzaker 12.1 |
| l17 | screens[2] key and options | Fair bankroll is one; heads count (+1/2 a toss), running best, raked bankroll (−0.025 a toss) are not | correct | one-step expectations; 0.5 × 0.95 − 0.5 = −0.025 |
| l17 | screens[3] key 3; slips 5, 5.2, 3.2 | M_n = S_n − 0.2n: forecast of M_11 given S_10 = 5 is 3 = M_10 | correct | script (exact one-step drift) |
| l17 | screens[3].explain | "Subtracting the drift turns any walk into a martingale" | correct | a walk with independent steps of common finite mean (Williams 10.4(a)) |
| l17 | screens[4] key 4/9; slips 0.5, 5/9, 0.8 | 125p + 80(1 − p) = 100 | correct | script |
| l17 | screens[4].explain | "Under this chance every price on the tree is a fair game. Pricing with Trees calls it the risk-neutral chance." | imprecise | The risk-neutral chance makes the discounted price a martingale: p = (e^{rΔt} − d)/(u − d) (Hull, OFOD, ch. 13). It equals 4/9 only at a zero interest rate, which the screen does not say. F10 |
| l17 | screens[5] keys and explain | Forecasts 3/4, 1/4, 1, 1/2, 1/2, 0; each pair averages to the forecast before | correct | script (enumeration) |
| l17 | screens[5].explain | "A forecast that uses all the information so far is always a martingale" | correct | Doob martingale E[Y given F_n] for integrable Y (Williams 10.4(c)); the summary adds the finite-mean condition |
| l17 | screens[6].prose | Supermartingale: E[X_{n+1} given history] ≤ X_n; submartingale rises on average | correct | Williams 10.3 |
| l17 | screens[6] key −1/37; slips 0, −0.054, 0.486, 0.027 | Red on a European wheel | correct | 18/37 − 19/37 |
| l17 | screens[7] key and options | Sign-flip process has mean 0 at every step and is not a martingale; a constant is one | correct | E[X_{n+1} given X_n] = −X_n |
| l17 | screens[7].explain | "A constant mean is necessary for a martingale but not enough" | correct | screen 9 proof; this counterexample |
| l17 | screens[8] key 2/3; slips 0.75, 0.5, 0.625 | Pólya urn share is a martingale with dependent steps; after three draws uniform on 1/5..4/5 | correct | script (exact); Grimmett and Stirzaker 12.1 example |
| l17 | screens[9] (lines, order, distractor) | E[X_n] = E[X_0] by total expectation and induction; independence not needed | correct | Williams 10.3 |
| l17 | screens[10] code | A Markov chain on numbers is a martingale when every state's expected next state is the state | correct | definition plus the Markov property; grade-all runs the tests |
| l17 | screens[11] key 20; slips 10, 40, 30 | 0.6x + 0.4 × 70 = 40 | correct | script |
| l17 | screens[11].explain | A binary contract's price is the market's forecast of the event, a martingale; a signal claims the conditional mean differs | correct | stated under the screen's own "if the price is a fair game"; same zero-rate caveat as F10 |
| l17 | summary | Definition; keeps its mean; drift removal; forecast of revealed information when the mean is finite; trap | correct | rows above |
| l17 | quiz[0], quiz[1], quiz[2] | Forecast X_n + 0.5 is a submartingale; E[X_20] = 7; p = 1/3 | correct | definitions; arithmetic |
| l17 | quiz[3] key 1; slip 2 | 0.5 × 3 + 0.3 × 1 + 0.2x = 2 | correct | arithmetic |
| l17 | quiz[3].wrong "five" 5 | "You may have dropped the chances" | imprecise | 5 solves 0.2x = 1. Dropping the chances gives −2, an equal average gives 2. F11 |
| l18 | screens[0] key 10; slips 9, 16, 12.5 | E[S_{n+1}² given S_n = 3] = 10 | correct | (16 + 4)/2 |
| l18 | screens[1] key and explain | Average of S² − n stays near 0; E[S_100²] = 100; sd of S_100² about 141 | correct | Var(S_n²) = 2n² − 2n; script |
| l18 | screens[2] key and options | E[S_{n+1}² given S_n = s] = s² + 1, so S_n² − n is a martingale | correct | Williams 10.4 exercise; script exact |
| l18 | screens[3] key 0.96; slips 1, 0.24, 0.04 | Var of a ±1 step is 4pq; (S_n − 0.2n)² − 0.96n is a martingale | correct | script exact |
| l18 | screens[4] key 1; slips 7/6, 2/3, 0.5 | (q/p)^{S_n} is a martingale | correct | De Moivre's martingale, Grimmett and Stirzaker 12.1; script exact |
| l18 | screens[5] key 7/6; slips 1, 1.5, 4.6716 | (p/q)^{S_n} grows by 7/6 a step | correct | script |
| l18 | screens[6].prose and key | If p f(s+1, n+1) + q f(s−1, n+1) = f(s, n) then f(S_n, n) is a martingale; 2^s grows by 1.25 at p = 1/2 | correct | one-step conditional expectation; integrable because S_n is bounded at each n |
| l18 | screens[7] (lines, order, distractor) | Proof for S_n² − n; "a function of a martingale need not be one" | correct | S_n² is a submartingale (Jensen) |
| l18 | screens[8] code and the s³ − 3ns surprise | Exact drift check; s³ − 3ns is a martingale of the fair walk | correct | script exact |
| l18 | screens[9] key 5,000; slips 25,000, 1,000, 25,000,000 | sd after 25 days from E[X_25²] = 25 × 1000² | correct | script |
| l18 | screens[9].explain | "Squared minus time is the seed of quadratic variation" | correct | Shreve II, 3.4 (W_t² − t) |
| l18 | summary, quiz[0..3] | Square, power and drift martingales; base q/p; at p = 1/2 the power is the constant 1; 3/7; E[r^{S_10}] = 1; c = 0.75 | correct | script exact |
| l19 | screens[0] key 0.3; slips 0.5, 0.7, 0.43 | Fair ruin from 3 of 10 | correct | script (first-step solve) |
| l19 | screens[1] key 0.3 and explain | Stopped fair bankroll keeps its mean: 10P = 3 | correct | optional stopping, bounded stopped process (Williams 10.10(b)) |
| l19 | screens[2].prose | Stopping time: decides at step n from the first n steps only | correct | Williams 10.8 |
| l19 | screens[2].prose | Optional stopping: E[M_T] = E[M_0] if (1) T bounded, or (2) E[T] finite and steps of M bounded, or (3) stopped process bounded and T finite with chance 1 | correct | Williams 10.10 (a), (c), (b), Doob's theorem |
| l19 | screens[2] key and options | First hit of an end is a stopping time; "one bet before", "last visit", "highest point" are not | correct | Williams 10.8 |
| l19 | screens[3] (lines, order, distractor) | P = i/N with the conditions checked before the theorem is used | correct | Williams 10.11-10.12 |
| l19 | screens[4] key 21; slips 9, 30, 7 | Stop S² − n under condition (2): E[T] = i(N − i) | correct | increments are ±2S − ... bounded by 2N inside [0, N]; E[T] finite by the geometric tail (Williams 10.11); script exact |
| l19 | screens[4].explain | 25 bets from 5 of 10; 6 from 2 of 5; panel average 12.1 within sampling error of 9 | correct | script; sd of S_T² − T is about 50, so the standard error over 300 games is about 3 |
| l19 | screens[5] key 32/275; slips 0.5, 0.4, 0.8836 | Stop (q/p)^S at p = 0.4 | correct | script exact (flip slip equals 1 − P) |
| l19 | screens[6] key 50/13; slips 4, 0.769, 2.769 | E[T] = (NP − i)/(p − q); 1,904.1 bets at p = 0.49 from 50 of 100 | correct | script exact |
| l19 | screens[7].prose | Wald: independent steps with mean μ, stopping time with finite mean: E[S_T] = μE[T], from stopping S_n − nμ | correct | Grimmett and Stirzaker 10.2 (Lemma 10.2.9, iid steps); Williams 10.10(c) covers the bounded die steps |
| l19 | screens[7] key 21; slips 3.5, 6, 36 | Total of die rolls up to the first 6 | correct | script Monte Carlo (20.9 to 21.1) and the 5 × 3 + 6 route |
| l19 | screens[8] table | Martingale answers equal first-step answers | correct | script exact, 10 cases |
| l19 | screens[9] key and options | At p = 0.49 the plain walk is not a martingale; 0.1192 from (q/p)^S; 0.8808 is ruin | correct | script |
| l19 | screens[9].explain | "these games averaged £11.75, and 23 of 200 reached £100" | correct | 23 × 100/200 = 11.5; the chart's 8,000-bet window leaves an unfinished game or two at its running value, which accounts for the 0.25 |
| l19 | screens[10] code and table | ruin_by_stopping fractions (211/11, 41553/58025, 48291/2321) | correct | script exact |
| l19 | screens[11] keys 2/3, 8, 0 | Stop and target on a fair strategy | correct | script |
| l19 | summary, quiz[0..2] | Conditions restated; peak of 10 days is not a stopping time; i = N gives 0; 32 bets | correct | rows above |
| l19 | quiz[3] key 150; slips 30, 120 | Wald with a stop after the first losing trade: 30 × 5 | correct | script Monte Carlo (150 against 120) |
| l20 | screens[0] key 1; slips 0, 0.5 | Fair walk stopped at +1: E[S_T] = 1, reached with chance 1 | correct | recurrence of the simple symmetric walk (Norris 1.6) |
| l20 | screens[1] key 0.9 | Floor at −9: P = L/(L + 1), E[S_T] = 0 | correct | script |
| l20 | screens[2] key 9 and explain | E[T] = L; time grows without bound as the floor drops | correct | i(N − i) |
| l20 | screens[2].explain | "At L = 99 the batch shows only about 40, because the mean comes from rare games lasting thousands of bets" | correct | The chart runs 1,000 bets, and E[min(T, 1000)] = 49 at L = 99: the window cannot show the long games. script |
| l20 | screens[3] keys (all three conditions fail) | T unbounded, E[T] = lim L = ∞, stopped walk unbounded below; the walk is still a martingale | correct | T ≥ T_L so E[T] ≥ L for every L; Williams 10.12 |
| l20 | screens[3].explain | "With every condition gone, the theorem gives no promise" | correct | the conditions are sufficient, and the screen does not claim they are necessary |
| l20 | screens[4] keys 0.0796 and −11.56 | Cap at 100 bets: P(no +1) = C(100, 50)/2^100 by reflection; E[S_T] = 0 | correct | script exact (dynamic programme in fractions) |
| l20 | screens[5] key 0 | Doubling, ten bets, fair coin; sd of a cycle about £32 | correct | script |
| l20 | screens[6] key −0.3056; slips 0, −0.027, −1023, 0.3056 | 1 − 1024 (19/37)^10; doubling cannot turn a supermartingale into a winner | correct | script (closed form equals the branch sum); Williams 10.7 ("you cannot beat the system") |
| l20 | screens[7] key and options | Unlimited doubling: E[T] = 2, last stake 2^{T−1} has infinite mean, steps unbounded, so condition (2) fails; bankroll is a martingale | correct | script; conditions (1) and (3) fail as well, which the option texts allow for |
| l20 | screens[8], screens[10] | Rare loss sized to cancel the gains; short-option books have the same shape; a calm backtest overstates the mean | correct | expectation; Taleb-style sampling point, stated as a caution not a theorem |
| l20 | screens[9] code and table | doubling_ev; capped walk 0.9204 and 0 | correct | script exact |
| l20 | summary, formula | E[gain] = 1 − 2^d (1 − p)^d | correct | script |
| l20 | quiz[0..3] | Bounded stop gives 0; 19/20; 1/64; all three conditions fail with no floor and no cap | correct | rows above |
| l21 | screens[0] key | HTH waits longer than HHT (10 against 8) although each has chance 1/8 in a window | correct | script: exact first-step solve and Monte Carlo (60,000 games each) |
| l21 | screens[1] options | HT 4, HH 6, HHT 8, HHH 14 | correct | script exact |
| l21 | screens[2] keys 2, 6, 8 | First-step equations for HHT | correct | script exact |
| l21 | screens[3] key 10; slips 8, 14 | Gamblers hold £8 + £0 + £2 at the first HTH; casino's net T − 10 has mean 0 | correct | Li (1980); Williams 10.11 (ABRACADABRA) |
| l21 | screens[4] (lines, order, distractor) | Net is a martingale; E[T] finite and bounded steps give condition (2); windows overlap so 8 is wrong | correct | Williams exercise E10.6 |
| l21 | screens[5].prose and key 14 | E[T] = Σ 1/P(prefix) over prefixes that are also suffixes | correct | Li (1980), independent letters; script exact for 17 patterns |
| l21 | screens[6] key 3.75; slips 6, 2.25, 1.5 | HH at P(H) = 2/3: 9/4 + 3/2; first-step equations agree | correct | script exact |
| l21 | screens[7].prose | "Gamblers now bet on letters at odds of 26 to 1" | imprecise | A fair bet on a 1-in-26 letter returns £26 for £1: odds of 25 to 1. Odds of 26 to 1 return £27 and would give 27^11 + 27^4 + 27. F12 |
| l21 | screens[7] keys and explain | A, ABRA and the whole word; 26^11 + 26^4 + 26 = 3,670,344,487,444,778; first-step solve over 12 states agrees | correct | script exact (fractions) |
| l21 | screens[8] key and options | Self-overlap makes appearances clump at the same long-run rate 1/8, so the first comes later; THT waits 10 | correct | renewal argument (Grimmett and Stirzaker 10.2 exercise); script |
| l21 | screens[9] code, table, explain | Casino rule in code; HTHT 20, HHHH 30, LLL 195/8 | correct | script exact |
| l21 | screens[10] key 24.375; slips 15.625, 3, 8.75 | Three losing days in a row at 0.4 | correct | script exact |
| l21 | summary, quiz[0..3] | Rule; note that the whole pattern always counts; 2, 4, 10, 1/0.24 | correct | script exact |
| l22 | screens[0] key 8; slips 4, 10, 12 | E[N_5 given N_3 = 4] = 8; a count is a submartingale | correct | independent increments; script Monte Carlo |
| l22 | screens[1] keys −2, −2 | N_t − 2t forecast equals today's value | correct | script |
| l22 | screens[2] (lines, order, distractor) | N_t − λt is a martingale in continuous time | correct | Grimmett and Stirzaker 12.7; Shreve II, 11.2.2 |
| l22 | screens[3] key 8; slips 4, 16, 0 | (N_t − λt)² − λt is a martingale | correct | Shreve II, 11.2 exercise; script Monte Carlo (8.0 against 4) |
| l22 | screens[4] key 1.5 and prose | Stop N_t − 2t at T_3: "the stopped count is at most 3 and E[T_3] is finite, so optional stopping applies" | correct | abs(M at t∧T) ≤ 3 + 2T with E[T] finite, so dominated convergence applies (Williams 10.10 proof; Durrett 4.8). script |
| l22 | screens[5] keys 210, 67,000, 22,900 | Moments of a trade size | correct | script |
| l22 | screens[6].prose and explain | "Wald's identity gives E[S_10] = E[N_10]E[Y]"; "The count is a stopping-time sum of independent sizes, so Wald applies" | imprecise | N_10 is not decided by the sizes seen so far; it is independent of them. The result is the random-sum rule by conditioning on N (Grimmett and Stirzaker 3.7). Wald covers it only in the form "N independent of the steps". F13 |
| l22 | screens[6] key 4,200 and "S_t − λt E[Y] is a martingale" | Compound Poisson mean | correct | independent increments; script Monte Carlo |
| l22 | screens[7] key 1,340,000 and options | Var(S) = E[N]Var(Y) + Var(N)E[Y]² = λt E[Y²] | correct | Grimmett and Stirzaker 3.7; script Monte Carlo (ratio 1.00) |
| l22 | screens[8] keys 10 and 7.07 | Net inventory as compound Poisson | correct | script |
| l22 | screens[9] code and table | compound_moments, simulate_compound | correct | (3, 4, [1, 3]) gives 24 and 60; grade-all runs the tests |
| l22 | screens[10] key 6,515; slips 4,200, 5,358, 5,554 | Mean plus two sd | correct | script |
| l22 | screens[10].explain, quiz[3].explain | Premiums must exceed λE[Y] per unit time, or ruin is certain | correct | Cramér-Lundberg: ruin has chance 1 when c ≤ λE[Y] (Grimmett and Stirzaker 12.9 example; Asmussen and Albrecher, Ruin Probabilities, IV.1) |
| l22 | summary, quiz[0..3] | Compensated count and its square; E[T_k] = k/λ; variance λt E[Y²]; 200,000; 2.5; −2; 60,000 | correct | rows above |
| review-5 | items[0] keys | S_n, S_n² − n, H_n − n/2 are martingales; S_n² and the running maximum are submartingales | correct | script exact |
| review-5 | items[1] key 9/11; items[2] key 81/202; items[3] key 84 | Base q/p; ruin at p = 0.45; fair duration | correct | script exact |
| review-5 | items[4] key and options | Only "stop at +1 with no other limit" gives a non-zero mean | correct | l20 rows |
| review-5 | items[5] key −0.3686 and slips | Doubling, 8 bets at p = 0.48 | correct | script |
| review-5 | items[6] key 18; items[7] key 9.07 | HTHH; HHH at 0.6 | correct | script exact |
| review-5 | items[8] key 12,247; slips 5,477, 10,954 | sd of compound Poisson claims | correct | script |
| review-5 | items[9] key 8 | E[T_4] at rate 0.5 | correct | k/λ |
| homework-5 | items[0] keys 0.6376 and 23.76 | Ruin at p = 0.55 from 4 of 10 | correct | script (first-step solve) |
| homework-5 | items[1] keys 1/3 and 2/3 | Chain on 0..3 made a martingale; optional stopping gives 3P = 2 | correct | bounded chain, condition (3) |
| homework-5 | items[2] key 8/17; slips 0.8, 0.64, 0.4096 | e^{θS_n}/(cosh θ)^n is a martingale; S_T independent of T by symmetry; E[0.8^T] = 8/17 | correct | Williams 10.12 exercise; script (direct sum over the law of T) |
| homework-5 | items[3] key 155/18; items[4] keys 192,000 and 36,661; items[8] key 100 | HTH at 0.6; compound claims; fair duration | correct | script |
| homework-5 | items[5] (lines, order, distractor) | Proof of E[T] = i(N − i) under condition (2); "S_T² − T is bounded" is the wrong reason | correct | T is unbounded; Williams 10.10(c) |
| homework-5 | items[6] code and explain | Dynamic programme: 193/256, 793/1024, mean exactly 0 for every cap | correct | script exact |
| homework-5 | items[7] keys and explain | First hit of 5, its cap at 100, and step 20 are stopping times; the minimum of stopping times is one | correct | Williams 10.8 |
| homework-5 | items[9] model and rubric | No-stop take-profit breaks all three conditions; with a stop at −9: 0.9, mean 0, 9 trades | correct | l20 rows; script |
| homework-5 | items[10] model part 1 | (S_n − an)² − bn is a martingale exactly for a = p − q, b = p + q − (p − q)² | correct | script exact on a grid; uniqueness argument is valid because Z_1 takes two values |
| homework-5 | items[10] model part 2 | θ^{S_n} is a martingale exactly for θ = 1 or θ = q/p; the pause chance drops out | correct | (θ − 1)(pθ − q) = 0; script |
| homework-5 | items[10] model part 3 and rubric | Condition (3) shown: bounded stopped process, T finite by the block bound; 135/211; condition (2) also holds with steps at most 1 − θ | correct | script (linear solve gives 135/211) |
| problems-5 | items[0].parts[0..4] | ATM: 45; 2,620; 2,950; sd 325.88; cash 2,271.77, with every slip | correct | script |
| problems-5 | items[1].parts[0..4] | Signal trial: −200 a day; base 11/9; 0.4780; 6.0975 days; −1,219.51 by the two ends and by Wald | correct | script exact |
| problems-5 | items[2].parts[0..1] | 60 a day; LL waits 130/9 days | correct | script exact |
| problems-5 | items[2].parts[2] key and options | Wald applies because the cut is a stopping time, E[T] is finite and each day's P&L is bounded | correct | Williams 10.10(c) |
| problems-5 | items[2].parts[3..4] | 866.67 at the LL cut; 1,152.38 at the LWL cut | correct | script exact and Monte Carlo |
| problems-5 | items[3].parts[0] key and options | Reflected walk: J_n² − n is a martingale, J_n is not (it rises at 0) | correct | at 0 the square moves 0 to 1 for certain |
| problems-5 | items[3].parts[1] key 45; slips 10, 49, 25, 5 | E[T] = 49 − 4; t_k = 49 − k² | correct | script (linear solve) |
| problems-5 | items[3].parts[2] key 5/7 | Pile empties before 7 | correct | script |
| problems-5 | items[3].parts[3] key 5; slips 7, 6, 4.2857, 0.7143 | E[idle hours] = 5/7 × 7; J_n − Z_n is a martingale | correct | script (linear solve gives 5) |
| problems-5 | items[3].parts[4] key 500 and slips | 20 × 40 − 60 × 5 by linearity | correct | arithmetic |

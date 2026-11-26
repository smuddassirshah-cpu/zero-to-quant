# Claim ledger: markov levels 4 and 5, audit round 2

Blind read at `668f3e02`. One row per definition, result, method step, convention, graded key with its slips, and the reasoning in each hint, feedback and explain group. Verdicts: `correct`, `wrong`, `imprecise`, `misleading`, `unverified`.

Sources: N = Norris, *Markov Chains*; LPW = Levin, Peres and Wilmer, *Markov Chains and Mixing Times* (2nd ed.); W = Williams, *Probability with Martingales*; GS = Grimmett and Stirzaker, *Probability and Random Processes* (3rd ed.); D = Durrett, *Probability: Theory and Examples*. "script" = a check in `docs/reports/markov-L4-5-concepts-r2.py`. "deriv." = short derivation, given in the row.

| File | JSON path | Claim (short) | Verdict | Basis |
|---|---|---|---|---|
| l13 | screens[0] | At the stationary split 1,000 bull and 500 bear days give 100 switches each way | correct | deriv.: 1000 x 0.1 = 500 x 0.2 |
| l13 | screens[0].hints, feedback | Only days in the starting state can switch | correct | flow = pi_i P_ij, N 1.9 |
| l13 | screens[1].prose | Detailed balance pi_i P_ij = pi_j P_ji; a chain with such a pi is reversible; run backwards from the stationary split it looks the same | correct | N 1.9 Thm 1.9.3; LPW 1.6. The screen sets the chain at its stationary split first |
| l13 | screens[1].widget, feedback | Backward share bull then bear = F(Bear,Bull) = 1/15; slips 0.1, 0.2, 2/15 | correct | deriv.; slip bands clear of 0.0667 |
| l13 | screens[2] | Balance between neighbours gives pi_{i+1}/pi_i = 0.3/0.5 = 0.6; slips 5/3, 0.3, 0.5, 0.2 | correct | LPW 2.5 (birth-and-death chains) |
| l13 | screens[2].prose | "Assume the long-run flow up matches the flow down" stated as an assumption | correct | justified on screens[5]; cut argument LPW 2.5 |
| l13 | screens[3] | Weights 1, 0.6, 0.36, 0.216, total 2.176 | correct | script (solve pi P = pi) |
| l13 | screens[4] | pi_2 + pi_3 = 0.2647; column check 0.4596 x 0.7 + 0.2757 x 0.5 = 0.4596; slips 0.576, 0.1654, 0.144, 0.5 | correct | script |
| l13 | screens[5] | Detailed balance plus sum 1 implies pi P = pi (sum over i, row sums 1) | correct | N Lemma 1.9.2; LPW Prop 1.20 |
| l13 | screens[6].prose | A birth-death chain on finitely many states in which each up step can be undone is reversible, pi_{i+1} = pi_i P_{i,i+1}/P_{i+1,i} | correct | LPW 2.5 |
| l13 | screens[6].widget | Walker up 0.6 down 0.1 on 0 to 5: reversible, pi_{i+1} = 6 pi_i; "drift" and "only if equal" options false | correct | deriv.; drift does not prevent balance on a finite range |
| l13 | screens[7] | Rotation 0.8 / 0.2 on three states: uniform pi is stationary, flows 0.267 v 0.067, not reversible | correct | script; N Example 1.9.4 |
| l13 | screens[7].explain | Detailed balance is stronger than stationarity (sufficient, not necessary) | correct | N 1.9 |
| l13 | screens[8] | Balance round the cycle forces pi_A = 64 pi_A, so pi_A = 0: no balanced distribution; then solve pi P = pi | correct | deriv.; Kolmogorov cycle criterion, GS 6.5 |
| l13 | screens[9] | One-way edge P_BC > 0, P_CB = 0 forces pi_B = 0; a chain that visits B has no such pi; tap B to C and C to A | correct | deriv.; holds for an irreducible chain, which this one is |
| l13 | screens[10] | Queue join 0.3 leave 0.6 capped at 3: pi = (8,4,2,1)/15, empty 0.5333; slips 0.5, 0.5714, 0.6, 0.25 | correct | script |
| l13 | summary | Three ideas, formula, trap "solving pi P = pi always works" | correct | existence on a finite state space, LPW Prop 1.14 |
| l13 | quiz[0] | 0 to 2 queue, 0.2 up 0.4 down: pi_0 = 4/7; slips 1/3, 0.5, 2/7 | correct | deriv. |
| l13 | quiz[1] | F with equal row and column sums but F12 != F21: stationary, not reversible; reversible iff F = F^T | correct | LPW 1.6 (pi_i P_ij symmetric) |
| l13 | quiz[2] | Pairs i = j never need checking | correct | identity |
| l13 | quiz[3] | P21 = 0.5 x 0.2 / 0.3 = 1/3; slips 0.2, 0.12, 0.03 | correct | script |
| l14 | screens[0] | Seeded run: A largest share, D least; shares near 0.37, 0.25, 0.26, 0.12 | correct | script (exact 3/8, 1/4, 1/4, 1/8); frames are a quoted seeded run |
| l14 | screens[1] | Degree = number of links at a venue; degrees add to twice the links | correct | handshake lemma, LPW 1.4 |
| l14 | screens[2] | Adding E to A: D's share 1/10; slips 1/8, 1/5, 1/4; "a link anywhere takes time from every other venue" | correct | deriv.: venues off the new link keep degree while 2E rises |
| l14 | screens[3] | pi_i = deg(i)/2E satisfies detailed balance, so is stationary | correct | LPW Example 1.21 |
| l14 | screens[4].widget | Mean gap between visits to D is 1/pi_D = 8; slips 0.125, 4, 7, 3 | correct | script (first-step solve); Kac, N Thm 1.7.7 |
| l14 | screens[4].explain | "In general the mean return time to a state is 1/pi_i" | imprecise | N Thm 1.7.7 needs an irreducible chain; on a network in two pieces (quiz[1]) pi is not unique. Finding 9 |
| l14 | screens[5] | Weighted links: pi proportional to strength; pi_B = 3/12, return 4; slips 3, 2, 0.25 | correct | script; LPW 9.1 |
| l14 | screens[6].widget | Knight degrees by type add to 336 | correct | script |
| l14 | screens[6].explain | "there are 168 legal moves from square to square" | imprecise | 168 is the number of links (unordered pairs); ordered moves number 336. Finding 7 |
| l14 | screens[7] | Corner return 168, centre 42; slips 64, 336, 42, 84 | correct | script (exact solve on the knight graph) |
| l14 | screens[8] | Square: P^k(A,A) = 0 at odd k, P^k never converges, time share still 1/4; a network with no odd cycle is periodic | correct | script; LPW 1.3 (bipartite iff period 2) |
| l14 | screens[9] | Star: hub share 1/2, leaf 1/6; equal shares only when degrees are equal | correct | deriv. |
| l14 | screens[10].widget | `network_pi`, `return_time_mc`: strength to both ends, weighted choice, gaps averaged | correct | code read; tests match exact shares |
| l14 | screens[10].explain | "the strengths add to 2E" for weighted edges | imprecise | they add to twice the total strength; 2E only when every weight is 1. Finding 8 |
| l14 | screens[11] | Dealer network: D1 share 4/12; D5 cut off if D1 fails | correct | deriv. |
| l14 | summary | Walk on an undirected network reversible with deg/2E; return 1/pi; bipartite has pi but no convergence; two pieces, more than one pi | correct | LPW 1.6, 1.7 |
| l14 | quiz[0] | Leaf of a star returns in 6 | correct | deriv. |
| l14 | quiz[1] | Two pieces: share at B is 1/2 from A; deg/2E needs one connected network | correct | N 1.7 (closed classes) |
| l14 | quiz[2] | Weighted square: strengths 3, 4, 3, 2, return to D 6 | correct | deriv. |
| l14 | quiz[3] | Uniform shares exactly when all degrees equal (connected network) | correct | deriv. |
| l15 | screens[0] | Metropolis rule min(1, w_new/w_old) with symmetric proposal; 1.281/1.427 = 0.898; total never needed | correct | script; LPW 3.2 |
| l15 | screens[1] | Flat step = rejected proposal, state counted again; canvas P is the Metropolis matrix; rejection likeliest at the ends | correct | script (canvas P v computed) |
| l15 | screens[2] | P^k from 0.40: 0.187 at 5, 0.099 at 10, below 0.06 first at 18; burn-in discards early steps; pull halves about every five steps | correct | script: half-life 4.69 steps from the second eigenvalue |
| l15 | screens[3] | Both flows equal min(w_i, w_j)/2Z, so balance holds and Z cancels; off-grid proposal only changes P_ii | correct | LPW 3.2.1 |
| l15 | screens[3].o5 | "so the chain's long-run shares are the posterior" | correct | chain is irreducible on 7 states; N Thm 1.10.2 |
| l15 | screens[4] | Always accepting, walls refusing: uniform 1/7 | correct | script (symmetric P) |
| l15 | screens[5] | Recording moves only on weights 1, 3 gives L, H, L, H: share 1/2 | correct | script |
| l15 | screens[6].prose | Strong law for independent draws; ergodic theorem for an irreducible chain: time averages tend to the pi-average | correct | N Thm 1.10.2 (positive recurrent; automatic on a finite state space, the only case in the course) |
| l15 | screens[6].widget | Aperiodicity not needed for averages; theorem holds from step 1 | correct | N Thm 1.10.2; script (periodic square) |
| l15 | screens[6].explain | Both running means settle near 0.578; the chain's is slower because neighbouring steps are alike | correct | script: posterior mean 0.5780; MC time averages |
| l15 | screens[7] | Hastings ratio w_j q_ji / (w_i q_ij) = 9/14; slips 1, 1.5, 3/7, 3.5 | correct | LPW 3.2.2; script |
| l15 | screens[8] | Sampler code; "100,000 steps agree to about 0.003" | correct | script: median max error 0.0029 over 300 runs |
| l15 | screens[9] | P(p > 0.5) from bars 0.7296, exact 0.7301, 0.50 excluded; "moved on 79% of its steps" | correct | script: stationary move share 0.7876 |
| l15 | summary | Ideas, formula, trap | correct | as rows above |
| l15 | quiz[0] | 2/5 = 0.4; back up certain | correct | rule |
| l15 | quiz[1] | Keep every step: A 7, B 3 | correct | ergodic average counts repeats |
| l15 | quiz[2] | Weights 1, 2, 5: third share 5/8 | correct | balance |
| l15 | quiz[3] | q_ij = 0.25, q_ji = 0.75, equal weights: move j to i accepted with 1/3 | correct | deriv. |
| l16 | screens[0] | Seeded staircase, one empty minute; each empty with chance 0.135 | correct | e^-2 |
| l16 | screens[1].prose | Poisson process: independent counts on separate stretches, Poisson(lambda t) counts, independent Exp(lambda) gaps | correct | N Thm 2.4.3 (equivalent definitions) |
| l16 | screens[1].widget | e^-2 = 0.1353; slips 0.5, e^-0.5, 1 - e^-2 | correct | script |
| l16 | screens[2] | P(N(3) = 5) = 0.1606; slips 0.0361, 0.1083, 5/6 | correct | script |
| l16 | screens[3] | E[T_3] = 1.5; T_3 is Gamma(3, rate 2); P(T_1 > 1) = e^-2 | correct | N 2.4; GS 6.8 |
| l16 | screens[4] | Merged rate 5; next order a buy with chance 3/5 | correct | N Thm 2.4.4 (superposition) |
| l16 | screens[5] | P(T_b < T_s) = lambda_b/(lambda_b + lambda_s) by conditioning; min is Exp(5) | correct | N Thm 2.3.3 |
| l16 | screens[6] | Thinning with chance 0.6 gives Poisson streams at 3 and 2; no buys in 2 minutes e^-6; slips e^-3, e^-10, e^-4 | correct | GS 6.13 (thinning / colouring) |
| l16 | screens[7] | Split streams are independent; table rows match Poisson(2); special to Poisson | correct | script: corr 0.0007, conditional means 2.00 |
| l16 | screens[8] | Gap containing a fixed time has mean 1, twice a typical gap (stationary process); memorylessness both ways | correct | script MC 0.998; GS 10.3 (excess life; inspection paradox) |
| l16 | screens[9] | `poisson_path` by exponential gaps, `split_counts` by coin flips | correct | code read |
| l16 | screens[10] | Next three fills all buys (3/5)^3 = 0.216 | correct | independence of marks |
| l16 | summary | Ideas, formula, trap; changing rate gives Poisson counts with the integrated rate | correct | GS 6.13 (inhomogeneous process) |
| l16 | quiz[0] | e^-1 | correct | script |
| l16 | quiz[1] | Given one arrival in 10 minutes it is uniform: 0.2 | correct | N Thm 2.4.6 |
| l16 | quiz[2].widget | Mean orders 4 x 10 + 1 x 50 = 90 | correct | linearity |
| l16 | quiz[2].feedback, explain | "The count is Poisson with the integrated rate" | imprecise | true for a Poisson process with a changing rate; the prose never says the orders are Poisson. Finding 10 |
| l16 | quiz[3] | e^-5 = e^-3 e^-2 | correct | independence |
| l17 | screens[0] | Fair bet: forecast 13 for toss 9 and toss 18 | correct | tower property, W 9.7 |
| l17 | screens[1] | p = 0.6: forecast 13.2; drift 2p - 1 | correct | deriv. |
| l17 | screens[2].prose | Martingale: E[X_{n+1} given X_0..X_n] = X_n with E abs X_n finite | correct | W 10.3 |
| l17 | screens[2].widget | Fair bankroll is one; heads count, running best, raked bankroll are not | correct | deriv.; running max is a submartingale |
| l17 | screens[3] | M_n = S_n - 0.2n: forecast 3 = M_10; subtracting the drift makes a walk a martingale | correct | W 10.4(a) |
| l17 | screens[4] | Up 25% down 20%: p = 4/9; zero-rate risk-neutral chance | correct | deriv.; Shreve I 1.2 |
| l17 | screens[5] | Forecaster: 3/4, 1/4, 1, 1/2, 1/2, 0; a forecast using all information so far is a martingale | correct | Doob martingale, W 10.4(c) |
| l17 | screens[6] | Supermartingale E <= X_n, submartingale rises; red on a European wheel loses 1/37 a spin | correct | W 10.3 |
| l17 | screens[7] | Sign-flip process: constant mean 0, not a martingale; constant mean necessary, not sufficient | correct | deriv. |
| l17 | screens[8] | Polya urn share is a martingale; after three draws uniform on 1/5..4/5 | correct | script; W E10.1, D 4.3 |
| l17 | screens[9] | E[X_n] = E[X_0] by total expectation and induction; independence not needed | correct | W 10.3 |
| l17 | screens[10] | A chain on numbers is a martingale when each state's next mean is the state; code and tests | correct | deriv.; code read |
| l17 | screens[11] | Binary contract: 0.6x + 0.4 x 70 = 40 gives 20 | correct | deriv.; conditional on "if the price is a fair game" |
| l17 | summary, quiz[0..3] | Sub/super naming; mean kept at 7; p = 1/3; x = 1 | correct | deriv. |
| l18 | screens[0] | From 3 the next square averages 10 = 9 + 1 | correct | deriv. |
| l18 | screens[1] | E[S_100^2] = 100; S_100^2 has sd about 141, so 2,000 walks miss by several units | correct | script: sqrt(2n^2 - 2n) = 140.7 |
| l18 | screens[2] | E[S_{n+1}^2 given S_n = s] = s^2 + 1; S_n^2 - n a martingale | correct | W 10.4; D Example 4.2.2 |
| l18 | screens[3] | p = 0.6: step variance 0.96 = 4pq; (S_n - 0.2n)^2 - 0.96n a martingale | correct | script (one-step test) |
| l18 | screens[4] | (q/p)^{S_n} a martingale: 0.6 r + 0.4/r = 1 at r = 2/3; E[r^{S_10}] = 1 | correct | script; GS 12.1 (De Moivre's martingale) |
| l18 | screens[5] | (p/q)^{S_n} grows by 7/6 a step, 4.6716 over ten | correct | script |
| l18 | screens[6] | Recipe p f(s+1,n+1) + q f(s-1,n+1) = f(s,n); only base 1 is fair when p = q | correct | deriv. |
| l18 | screens[7] | Proof order; "any function of a martingale is one" false; S_n^2 a submartingale | correct | Jensen, W 10.4 |
| l18 | screens[8] | Code; s^3 - 3ns a fair-walk martingale | correct | script |
| l18 | screens[9] | sd after 25 days 5,000; spread grows with root n | correct | deriv. |
| l18 | summary, quiz[0..3] | (q/p)^S constant when p = q; base 3/7; E[r^{S_10}] = 1; c = 0.75 | correct | deriv. |
| l19 | screens[0] | 97 of 300 reach 10, average final bankroll 3.23 | correct | 970/300 = 3.23, consistent |
| l19 | screens[1] | E[S_T] = S_0 gives P = 3/10; slips 0.5, 0.7, 3/7 | correct | script; W 10.12 |
| l19 | screens[2].prose | Stopping time: decided at step n from the first n steps. Optional stopping in three cases: T bounded; E[T] finite with bounded steps; stopped process bounded with T finite a.s. | correct | W 10.10 (a), (c), (b) |
| l19 | screens[2].widget | First hit is a stopping time; "one bet before", "last visit", "peak" are not | correct | W 10.8 |
| l19 | screens[3] | Ruin chance i/N in five lines, conditions checked first | correct | W 10.12 |
| l19 | screens[4] | Stopping S_n^2 - n under condition (2): E[T] = 21 = i(N - i); 2,500 from 50 of 100 | correct | script; steps at most 2N before T; E[T] finite by a geometric bound, asserted not shown |
| l19 | screens[4].explain | 20.2 bets and panel 12.1 "within sampling error of 9" | correct | script: se over 300 games 2.5 |
| l19 | screens[5] | p = 0.4, 5 of 10: P = 32/275 = 0.1164 | correct | script |
| l19 | screens[5].feedback.flip | "You used r = p/q. That gives the chance of going broke, 1 - P" | correct | true here because the start is the midpoint; deriv.: equality holds iff i = N/2 |
| l19 | screens[6] | E[T] = (NP - i)/(p - q) = 50/13; at p = 0.49, 50 of 100, about 1,904.1 | correct | script |
| l19 | screens[7].prose | "Take independent steps with mean mu, and a stopping time T with finite mean. Then E[S_T] = mu E[T]" | imprecise | D 4.8 (Wald) and GS 10.2 (Wald's equation) need identically distributed steps with finite mean (or bounded steps). Script: doubling stakes are independent, mean 0, E[T] = 2, E[S_T] = 1. Finding 2 |
| l19 | screens[7].widget | Die until first 6: expected total 21; second route 15 + 6 | correct | script MC 20.98 |
| l19 | screens[8] | Two routes agree on all five rows | correct | script |
| l19 | screens[9].widget | p = 0.49: 0.5 is wrong because S_n is not a martingale; 0.1192 from (q/p)^S | correct | script |
| l19 | screens[9].explain | "these games averaged 11.75, and 23 of 200 reached 100" | imprecise | 23 of 200 gives 11.50; 11.75 needs a game still running at bet 8,000 (script: 1.09 expected in 200). The text does not say so. Finding 4 |
| l19 | screens[10] | `ruin_by_stopping`, `wald_total`; table of four cases | correct | script (exact first-step solves) |
| l19 | screens[11] | Stop 4 below, target 2 above: 2/3, 8 trades, P&L 0 | correct | deriv. |
| l19 | summary.ideas[2] | "Wald's identity is optional stopping for sums of independent steps" | imprecise | same missing hypothesis as screens[7]. Finding 2 |
| l19 | summary (rest), quiz[0..2] | Three conditions; peak not a stopping time; duration 0 on the barrier; 32 bets | correct | W 10.10; deriv. |
| l19 | quiz[3] | Stop after the first losing trade: 30 x 5 = 150 | correct | D 4.8 (Wald), taking the trades as identically distributed |
| l20 | screens[0] | Stop at +1 with no limit: E[S_T] = 1, S_0 = 0 | correct | W 10.12 remark; recurrence N 1.6 |
| l20 | screens[1] | Floor at -9: chance 0.9, E[S_T] = 0 | correct | script (exact DP) |
| l20 | screens[2].widget | E[T] = L: 9 at L = 9, 99 at L = 99 | correct | script |
| l20 | screens[2].explain | "At L = 99 the batch shows only about 40, because the mean comes from rare games lasting thousands of bets" | imprecise | the chart stops at 1,000 bets, so it averages min(T, 1000), whose mean is 49.4 (script). Fresh batches centre on 49, never on 99. Finding 5 |
| l20 | screens[3] | No floor: T unbounded, E[T] infinite, stopped walk unbounded below; walk still a martingale | correct | D 4.8; monotone limit of E[T] = L |
| l20 | screens[4] | Cap at 100: fail chance C(100,50)/2^100 = 0.0796 by reflection; mean when failing -11.56 | correct | script; GS 3.10 |
| l20 | screens[5] | Doubling with 1,023: gain 0; one cycle has sd about 32 | correct | script |
| l20 | screens[6] | At red: 1 - 1024 (19/37)^10 = -0.3056; doubling cannot turn a supermartingale into a winner | correct | script; W 10.9 (stopped supermartingale) |
| l20 | screens[7].prose | E[T] = 2; last stake 2^(T-1) has infinite mean | correct | deriv. |
| l20 | screens[7].widget | Single choice "which condition fails": key "steps not bounded"; option "T is not bounded" marked wrong | imprecise | conditions (1) and (3) fail too (T unbounded; stopped bankroll unbounded below). The rejected option's first clause is true. Finding 3 |
| l20 | screens[8] | Rare loss sized to cancel the gains; independence of cycles | correct | deriv. |
| l20 | screens[9] | `doubling_ev`, `stop_when_up`; loses more as d grows at the wheel | correct | script |
| l20 | screens[10] | Short-volatility book has the doubling shape; a calm backtest overstates the mean | correct | qualitative; no number claimed |
| l20 | summary, quiz[0..3] | Floor or cap restores 0; 19/20; 1/64; all three conditions fail | correct | script |
| l21 | screens[0] | HTH waits 10, HHT waits 8 | correct | script (first-step solve and MC 9.99, 8.01) |
| l21 | screens[1] | Progress chain for HHT; 4 is HT, 6 is HH, 14 is HHH | correct | script |
| l21 | screens[2] | First-step equations give 2, 6, 8 | correct | deriv. |
| l21 | screens[3] | Gamblers betting on the pattern; casino net is a martingale; at T they hold 8 + 0 + 2 | correct | W E10.6; Li (1980) |
| l21 | screens[4] | Argument order; T has finite mean and M has bounded steps, so condition (2) | correct | W 10.10(c), 10.11 |
| l21 | screens[5] | E[T] = sum of 1/P(prefix) over prefixes that are suffixes; HHH 14 | correct | Li (1980); script |
| l21 | screens[6] | Heads 2/3: HH waits 15/4; first-step check | correct | script |
| l21 | screens[7] | ABRACADABRA: 26^11 + 26^4 + 26 = 3,670,344,487,444,778 | correct | script (exact solve); W E10.6 |
| l21 | screens[8] | Overlap makes appearances clump at the same long-run rate, so the first wait is longer; THT waits 10 | correct | renewal argument, GS 10.2; script |
| l21 | screens[9] | `pattern_wait`, `simulate_wait`; table waits 10, 30, 15/4, 195/8 | correct | script |
| l21 | screens[10] | LLL at 0.4: 24.375 days; LL 8.75 | correct | script |
| l21 | summary, quiz[0..2] | H 2, HT 4, THT 10 | correct | script |
| l21 | quiz[3].widget | HT at heads 0.6: 1/0.24 = 4.1667 | correct | script |
| l21 | quiz[3].feedback.hh | Slip 4.4444: "You used 0.6^2, the chance of HH" | imprecise | 1/0.36 = 2.7778; the banded value is the HH wait 1/0.36 + 1/0.6. Finding 6 |
| l22 | screens[0] | E[N_5 given N_3 = 4] = 8; a count is a submartingale | correct | independent increments, N 2.4 |
| l22 | screens[1] | N_t - 2t: value -2 now, forecast -2 | correct | deriv. |
| l22 | screens[2] | N_t - lambda t is a martingale in continuous time | correct | deriv. in the screen; independent increments, N 2.4 |
| l22 | screens[3] | (N_t - lambda t)^2 - lambda t a martingale; E[(N_5 - 10)^2 given N_3 = 4] = 8 | correct | script MC 8.000 |
| l22 | screens[4] | Stop at the third trade: E[T_3] = 1.5; count at most 3 and E[T_3] finite | correct | script; dominated convergence with 3 + 2 T_3 |
| l22 | screens[5] | E[Y] = 210, E[Y^2] = 67,000, Var 22,900 | correct | script |
| l22 | screens[6] | E[S_10] = 4,200; S_t - lambda t E[Y] a martingale | correct | GS 6.13 (compound Poisson) |
| l22 | screens[7] | Var(S) = E[N] Var(Y) + Var(N) E[Y]^2 = lambda t E[Y^2] = 1,340,000 | correct | script MC; GS 3.7 |
| l22 | screens[8].widget | Net inventory over 10 minutes: mean 10, sd 7.07 | correct | deriv. |
| l22 | screens[8].explain | "The mean is 50 x 0.2 = 10 lots: t lots a minute" | wrong | the mean rate is lambda E[Y] = 1 lot a minute; t lots is the mean after t minutes. Script check fails. Finding 1 |
| l22 | screens[9] | `compound_moments`, `simulate_compound` | correct | code read; tests |
| l22 | screens[10] | Capacity 4,200 + 2 x 1,157.6 = 6,515; mean exceeded about half the time; premiums at or below lambda E[Y] make ruin certain | correct | script: P(S > 4200) = 0.46; Asmussen, *Ruin Probabilities*, ch. III (net profit condition) |
| l22 | summary, quiz[0..3] | T_k mean k/lambda; constant size 200,000; forecast -2; claims 60,000 | correct | deriv. |
| review-4 | items[0] | Trader chain pi_2 = 4/7; slips | correct | deriv. |
| review-4 | items[1] | Strengths 3, 3, 5, 3: return to C 2.8 | correct | deriv. |
| review-4 | items[2] | 0.954/1.288 = 0.74 | correct | script weights |
| review-4 | items[3] | One buy and no sells: e^-1 e^-3 = 0.0183 | correct | thinning |
| review-4 | items[4] | Given P and pi = (0.2, 0.4, 0.4): reversible though P is not symmetric | correct | deriv.: pi P = pi and both pairs balance |
| review-4 | items[5] | Ring of six: uniform pi, P^k(1,1) = 0 at odd k | correct | LPW 1.3 |
| review-4 | items[6] | Metropolis on 1, 2, 4: move share 3/7 | correct | deriv. |
| review-4 | items[7] | 2 buys and 1 sell in 2 minutes: 0.00327 = P(N = 3) C(3,2) 0.6^2 0.4 | correct | deriv. |
| review-5 | items[0] | S_n, S_n^2 - n, H_n - n/2 are martingales; S_n^2 and the running max are not | correct | W 10.4 |
| review-5 | items[1..3] | Base 9/11; ruin 81/202; duration 84 | correct | script |
| review-5 | items[4] | Only the unlimited stop at +1 gives E[S_T] != 0 | correct | W 10.10 |
| review-5 | items[5] | Doubling 8 bets at 0.48: -0.3686 | correct | script |
| review-5 | items[6..7] | HTHH 18; HHH at 0.6: 9.07 | correct | script |
| review-5 | items[8..9] | Claims sd 12,247; fourth order at 8 minutes | correct | script |
| homework-4 | items[0] | King: degrees add to 420, corner return 140 | correct | script |
| homework-4 | items[1] | Birth-death, network walk, symmetric Metropolis must be reversible; cycle and one-way arrow are not | correct | LPW 1.6, 2.5, 3.2 |
| homework-4 | items[2] | P(X_t = A given X_{t+1} = B) = pi_A P_AB / pi_B = 0.8; backwards it is the anticlockwise rule | correct | script MC 0.799; N Thm 1.9.1 |
| homework-4 | items[3] | Reversed chain P*_ji = pi_i P_ij / pi_j; P* = P iff detailed balance | correct | N Thm 1.9.1, 1.9.3 |
| homework-4 | items[4] | Buys given 4 orders are Bin(4, 0.6): 0.3456; sells given 7 buys still mean 6 | correct | GS 6.13 |
| homework-4 | items[5] | First of three arrivals before time 1: 19/27 | correct | script MC 0.703; N Thm 2.4.6 |
| homework-4 | items[6] | Exactly 2 buys before the third sell: C(4,2) 0.6^2 0.4^3 = 0.13824 | correct | script MC 0.138 |
| homework-4 | items[7] | Random-walk Metropolis on the line, log acceptance, off-support never accepted | correct | code read; LPW 3.2 |
| homework-4 | items[8].model | Move-only shares proportional to pi_i (1 - P_ii): (0.027 .. 0.086), mean 0.5764, tail 0.747 | correct | script (jump-chain stationary law) |
| homework-4 | items[8].model | First 200 steps average 0.5721; with 20 discarded 0.5776; sds about 0.004 and 0.005 | correct | script: exact means; MC sds 0.0039 and 0.0050 |
| homework-4 | items[8].model, rubric | Identical starts share one bias; dispersed starts test convergence; report a Monte Carlo error | correct | standard practice, LPW 3; Gelman and Rubin (1992) |
| homework-4 | items[9] | MH on a network: accept min(1, w_j deg(i) / (w_i deg(j))); irreducible finite chain so the shares converge | correct | script (same construction, problems-4); N Thm 1.10.2 |
| homework-5 | items[0] | p = 0.55, 4 of 10: P = 0.6376, E[T] = 23.76 | correct | script |
| homework-5 | items[1] | x = 1/3; chance of 3 from 2 is 2/3 | correct | deriv. |
| homework-5 | items[2] | e^{theta S}/cosh(theta)^n a martingale; S_T independent of T by symmetry; E[0.8^T] = 8/17 | correct | script MC 0.4703, corr -0.003; W 10.12 |
| homework-5 | items[3] | HTH at 0.6: 155/18 | correct | script |
| homework-5 | items[4] | Insurer: mean 192,000, sd 36,661; 24,000 without the count's randomness | correct | deriv. |
| homework-5 | items[5] | Duration proof under condition (2); "S_T^2 - T is bounded" rejected | correct | W 10.10(c) |
| homework-5 | items[6] | Exact DP: 193/256 at 10, 793/1024 at 11, mean 0 | correct | script |
| homework-5 | items[7] | First hit, capped first hit, fixed time are stopping times; last visit and maximum are not | correct | W 10.8 |
| homework-5 | items[8] | Limits at +-5,000 in 500 steps: 100 days | correct | deriv. |
| homework-5 | items[9] | Take-profit with no stop: all three conditions fail; with a stop at -9: 0.9, 0, 9 trades | correct | script |
| homework-5 | items[10] | Lazy walk: a = p - q, b = p + q - (p - q)^2, unique; theta = 1 or q/p; 135/211 | correct | script; derivation checked line by line |
| problems-4 | items[0].parts[0..1] | Survey: pi_C = 0.1; recorded rate 0.2 against true 0.4 | correct | deriv. |
| problems-4 | items[0].parts[2] | Uniform target: accept min(1, deg(i)/deg(j)); 1/deg(i) gives H 16/26 | correct | script |
| problems-4 | items[0].parts[3..4] | C stays 0.75; repeats 0.4 | correct | script |
| problems-4 | items[1].parts[0..2] | Taxi rank: next arrival a taxi 0.6; ratio 1.5; passengers find it empty 8/65 | correct | script MC 0.1231; PASTA, GS 11.3 |
| problems-4 | items[1].parts[3..4] | 11.82 lost an hour; 7.28 with a fourth space; losses are not a Poisson stream | correct | deriv. |
| problems-4 | items[2].parts[0..1] | pi_D = 3/14; return to F 14 | correct | script |
| problems-4 | items[2].parts[2..4] | Audits at F Poisson at 1/7 an hour: mean 8/7, none e^{-8/7}, 17 hours for 0.9 | correct | script; thinning |
| problems-4 | items[3].parts[0..3] | Regime sampler: 0.75, 0.6, 0.3 by balance, rejections 0.1 | correct | script |
| problems-4 | items[3].parts[4] | Plain rule with an asymmetric proposal gives Mid 50/77 | correct | script |
| problems-5 | items[0] | Cash machine: 45, forecast 2,620, E[Y^2] 2,950, sd 325.88, cash 2,271.77 | correct | deriv.; GS 6.13 |
| problems-5 | items[1].parts[0..2] | Signal trial: -200 a day (supermartingale); r = 11/9; P = 24381/51001 | correct | script |
| problems-5 | items[1].parts[3..4] | E[T] = 6.0975; P&L -1,219.51 by Wald and by the two ends | correct | script |
| problems-5 | items[2].parts[0..1] | Edge 60 a day; LL at 0.3 waits 130/9 | correct | script |
| problems-5 | items[2].parts[2] | Wald usable: stopping time, E[T] finite, bounded daily P&L; look-ahead rule breaks it | correct | D 4.8 (Wald); W 10.10(c) |
| problems-5 | items[2].parts[3..4] | 866.67; LWL 19.2063 days, 1,152.38 | correct | script |
| problems-5 | items[3].parts[0..1] | Reflecting pile: J_n^2 - n a martingale; E[T] = 45 | correct | script (first-step solve) |
| problems-5 | items[3].parts[2..4] | Empties first 5/7; idle hours 5 (J_n - Z_n fair); profit 500 | correct | script |

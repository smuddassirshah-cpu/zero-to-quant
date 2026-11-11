# Claim ledger, round 1: random-vars levels 1 to 3

Auditor: blind Fable reader, round 1. Written before any earlier review, audit, ledger, concepts script or author report of this course was opened, and before the git history of the course folder was read.

Scope: `app/content/courses/random-vars/` files `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3` (with the performance task `h-build-pmf`), `problems-1` to `problems-3` and `fluency-l9-measuring-spread`. Levels 4 and 5 are out of scope. Topic 1.5 is Stage 1, so the ledger has full depth.

Rows: 334. Verdicts: correct 322, wrong 2, imprecise 10, misleading 0, unverified 0. The 2 wrong rows are findings 1 and 2; the 10 imprecise rows belong to findings 2 to 10.

How to read a row. Each row is one claim, or the lines of one screen that state the same fact (the key, its slip values and their feedback lines; or the hints and the explanation). Every string in a grouped row was read against the recomputed value or the cited result; none was passed by pattern. A sentence that carries its own rule, definition, condition or "always, never, only" claim has its own row.

File codes: `l1` to `l12` are the lesson files, `rv` review, `hw` homework, `pb` problems, `fl9` the fluency set.

Basis codes:
- E: exact enumeration with fractions, in `docs/reports/random-vars-L1-3-concepts.py`.
- D: a short derivation, given in the row; most are recomputed in the same script.
- MC: seeded Monte Carlo in the same script.
- S: a named source. BH is Blitzstein and Hwang, *Introduction to Probability*, second edition: 3.1 random variables, 3.2 pmfs, 3.6 CDFs, 3.7 functions of random variables, 4.1 expectation, 4.2 linearity, 4.4 indicators and the fundamental bridge, 4.6 variance, 7.3 covariance and correlation, 10.1 inequalities, 10.2 law of large numbers. Hull is *Options, Futures and Other Derivatives*. Other sources are named in the row.
- "run in CPython": the code was executed by the script in CPython 3.13, not in Pyodide 0.27.7 (Python 3.12). The values depend only on `random` and float arithmetic, which agree across these versions.

## Level 1: Distributions

### l1-number-per-outcome

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | objectives[0], screens[2].prose, summary.ideas[0] | a random variable is a rule giving every outcome one number (a function on the sample space) | correct | S: BH 3.1 definition 3.1.1. Measurability is vacuous on a finite space |
| l1 | screens[0] key, wrong `one-order`, byKey | {total = 9} is the four cells (3,6), (4,5), (5,4), (6,3); ordered pairs are distinct cells | correct | E: 4 of 36 |
| l1 | screens[0] byKey cell lines (13) | each named cell's total (8, 9 or 10) | correct | E: each pair summed by hand and in the script |
| l1 | screens[0].explain | P(total = 9) = 4/36 | correct | E |
| l1 | screens[1] key, wrongs `cross`, `row-only`, `square` | {larger die = 4} is the L of 7 cells; the cross, row and square are not | correct | E: 7 cells; (4,6) has max 6, (2,3) has max 3 |
| l1 | screens[1] byKey cell lines (23) | each named cell's larger die | correct | E |
| l1 | screens[1].explain | chance 7/36; same outcomes carry a different number | correct | E |
| l1 | screens[2].prose | X(3,6) = 9, Y(3,6) = 6 | correct | E |
| l1 | screens[2] key, options, hints | {X = 9} is an event (a set of outcomes), not a number, a chance or one outcome | correct | S: BH 3.1 (events defined through a random variable) |
| l1 | screens[2].explain | P(X = 9) = 4/36; a random variable turns a question about a number into an event | correct | E; BH 3.1 |
| l1 | screens[3] key, slips, hints, byKey | D = 1 on 10 cells, two diagonals of 5; slips 5, 6, 12 | correct | E |
| l1 | screens[3].explain, canvas | P(D = 1) = 10/36; D takes 0 to 5; the grid of gaps | correct | E: all 36 cells compared |
| l1 | screens[4].prose | a random variable needs one number for every outcome, nothing more | correct | S: BH 3.1 (finite space) |
| l1 | screens[4] key, options, byKey | an indicator, a constant and a signed difference are random variables; a probability and an event are not | correct | S: BH 3.1; a constant is a degenerate random variable (BH 3.2) |
| l1 | screens[4] hint step | at (2,5): I = 0, C = 7, S = −3 | correct | E |
| l1 | screens[4].explain | {I = 1} is the event of a double; a constant is still a rule from cells to numbers | correct | D |
| l1 | screens[5] key, options, hints, byKey | P(Y = 6) = 11/36 by inclusion and exclusion; 1/6, 6/36, 12/36 are slips | correct | E: 6 + 6 − 1 |
| l1 | screens[5].explain, summary.ideas[2], summary.trap | P(Y = 1) = 1/36; values are not equally likely; a value is as likely as the outcomes behind it | correct | E; this is the pmf definition |
| l1 | screens[6].prose, summary.formula | {X = x} = {ω : X(ω) = x}, P(X = x) = sum of P(ω) over those ω | correct | S: BH 3.2 |
| l1 | screens[6] key, options, explain | {X = 3} = {(1,2), (2,1)}; {(1,1),(1,2),(2,1)} is {X ≤ 3}; P = 2/36 | correct | E |
| l1 | screens[7] key cells, hints, byKey | call payoff max(S − 100, 0) on 94, 97, 100, 103, 106 is 0, 0, 0, 3, 6 | correct | D; Hull ch. 10 (payoff of a long call) |
| l1 | screens[7].explain | C is a random variable on five outcomes; {C = 0} has three outcomes | correct | D |
| l1 | screens[8] leaves, key, wrongs, byKey | N on the 8 fill paths; {N = 2} = FFM, FMF, MFF | correct | E |
| l1 | screens[8].explain | N takes 0, 1, 2, 3 | correct | E |
| l1 | quiz[0] key, options, explain | {Y = 2} = {(1,2),(2,1),(2,2)}; P = 3/36 | correct | E |
| l1 | quiz[1] key, options, explain | P(total ≥ 10) = 6/36 = 1/6; an indicator's chance of 1 is its event's chance | correct | E |
| l1 | quiz[2] key, slips, explain | L = 200M is −200 at M = −1; values −200, 0, 400 | correct | D |
| l1 | quiz[3] key, slips, explain | first minus second takes 11 values, −5 to 5; 36 outcomes share them unevenly | correct | E |

### l2-listing-chances

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l2 | screens[0] keys, accept, byKey, explain | p(2..7) = 1/36 .. 6/36, one more cell per diagonal, shrinking past 7 | correct | E |
| l2 | screens[1] exact bars, key, options, explain | pmf of the total; p(5) = p(9) = 4/36; mirror image about 7; 8 has five cells | correct | E |
| l2 | screens[1].explain | in 1,000 rolls the bars wobble around the exact chances | correct | MC: largest gap in 1,000 rolls is about 0.02 |
| l2 | screens[2].prose, summary.ideas[0], summary.formula | the pmf is p(x) = P(X = x) over the values X can take; zero elsewhere | correct | S: BH 3.2 definition 3.2.2 |
| l2 | screens[2] key, slips, byKey | the pmf adds to 1; 21/36 is p(2) to p(7) only | correct | E |
| l2 | screens[2].explain | any pmf adds to 1 because X always takes some value | correct | S: BH theorem 3.2.7 |
| l2 | screens[3] key, slip ranges, hints | faces 1 to 5 at 0.1 force p(6) = 0.5 | correct | D |
| l2 | screens[3].explain, screens[7].prose | a pmf need only be non-negative and add to 1; P(X in A) is the sum of its bars | correct | S: BH theorem 3.2.7 |
| l2 | screens[4] keys, byKey, explain | heads in three fair tosses: 1/8, 3/8, 3/8, 1/8 | correct | E |
| l2 | screens[5] key, slips, explain | heads plus tails is 3 on every outcome; a pmf with all its mass on one value | correct | E |
| l2 | screens[6] key, options, hints, explain | 25/36, 11/36, 1/36 add to 37/36; the 11 cells include (6,6); exactly one six is 10 cells | correct | E |
| l2 | screens[6] option `equal` why | a pmf can be lopsided | correct | D |
| l2 | screens[7] key, slips, explain | P(X ≥ 10) = 6/36; 3/36 and 3/11 are slips | correct | E |
| l2 | screens[8] leaves, keys, hints, byKey, explain | two-day change: 0.04, 0.20, 0.37, 0.30, 0.09; paths multiply (days independent), equal changes add | correct | E: nine paths |
| l2 | summary.ideas[1], summary.trap | a pmf is never negative and adds to 1; a list in [0,1] is not enough | correct | BH 3.2 |
| l2 | quiz[0] key, options, explain | heads in two tosses: 1/4, 1/2, 1/4 | correct | E |
| l2 | quiz[1] key, slips, explain | p(4) = 0.3; P(X ≥ 2) = 0.8 = 1 − p(1) | correct | D |
| l2 | quiz[2] key, options, explain | P(larger = 3) = 5/36 = (9 − 4)/36 | correct | E |
| l2 | quiz[3] key, slips, explain | P(Z = 0) = 0.5 + 0.2 = 0.7 | correct | D |

### l3-up-to-a-point

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l3 | screens[0] key, slips, explain | P(X ≤ 1) = 1/2 for heads in three tosses; 0.875 is at least one | correct | E |
| l3 | screens[1] canvas steps, derive | F is 0, 1/8, 4/8, 7/8, 1 on [.,0), [0,1), [1,2), [2,3), [3,.); closed dot on the upper step | correct | E; right-continuity, BH theorem 3.6.3 |
| l3 | screens[1] key, options | F jumps exactly at the values X can take, and is flat between | correct | BH 3.6 |
| l3 | screens[1].explain | each jump adds one bar; at x = 2 the height is already 7/8 because X ≤ 2 includes X = 2 | correct | D |
| l3 | screens[2].prose, summary.ideas[0], summary.formula | F(x) = P(X ≤ x), up to and including x, defined for every real x | correct | S: BH definition 3.6.1 |
| l3 | screens[2] key, slips, byKey, explain | F(2.4) = F(2) = 7/8 although X is never 2.4 | correct | E |
| l3 | screens[3] key, slips, explain | P(1 < X ≤ 3) = F(3) − F(1) = 1/2; 7/8 includes X = 1 | correct | E |
| l3 | screens[4] key, slips, hints, explain | P(X > 2) = 1 − F(2) = 1/8; 1 − F(1) is P(X ≥ 2) | correct | E |
| l3 | screens[5] key, wrongs, byKey cells | {Y ≤ 4} is the 4 by 4 square, both dice at most 4 | correct | E |
| l3 | screens[5].explain | F(y) = y²/36 for y = 1..6 | correct | E |
| l3 | screens[6] steps, key, slips, explain | the jump at 4 is 16/36 − 9/36 = 7/36; every jump of a CDF is a bar of the pmf | correct | E; BH 3.6 |
| l3 | screens[7] key, options, hints, explain, summary.trap | P(2 ≤ Y ≤ 4) = F(4) − F(1) = 15/36; F(4) − F(2) = 12/36 drops Y = 2 | correct | E |
| l3 | screens[8] lines, key, byKey, explain | P(a < X ≤ b) = F(b) − F(a) by a disjoint split of {X ≤ b}; the only valid order | correct | D; BH 3.6 |
| l3 | screens[9] keys, hints, byKey | running totals 0.30, 0.55, 0.75, 0.90, 0.96, 0.99, 1.00 | correct | E |
| l3 | screens[9].explain, byKey r6c2 | a CDF never falls and ends at 1; P(L ≤ 2) = 0.90 | correct | BH theorem 3.6.3 |
| l3 | screens[10].prose (first sentence), key, slips, explain | VaR 95% is the smallest x with F(x) ≥ 0.95, here £5k; the quantile of a discrete loss sits on a jump | correct | S: McNeil, Frey and Embrechts, *Quantitative Risk Management*, definition 2.10 (generalised inverse) |
| l3 | screens[10].prose (second sentence) | "On 95% of days the loss is at most this" | imprecise | E: P(L ≤ 5) = 0.96. The definition gives at least 95%. Finding 6 |
| l3 | screens[10] byKey | P(L > 2) = 0.10; VaR ignores the size of the worst 5% | correct | E |
| l3 | summary.ideas[1], [2] | a staircase from 0 to 1 jumping by p(x); P(X > x) = 1 − F(x) | correct | BH 3.6 |
| l3 | quiz[0] key, options, explain | a CDF never decreases, reaches 1 at the largest value, is 0 far left | correct | BH theorem 3.6.3 |
| l3 | quiz[1] key, slips, explain | P(X = 2) = 0.7 − 0.2 = 0.5; pmf 0.2, 0.5, 0.3 | correct | D |
| l3 | quiz[2] key, slips, explain | P(X < 2) = F(1) = 0.2; strict and weak differ by P(X = 2) | correct | D |
| l3 | quiz[3] key, slips, explain | P(L > 2) = 0.10; 1 − F(1) = 0.25 is P(L ≥ 2); P(L > 5) = 0.04 | correct | E |

### l4-transforming

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l4 | screens[0] key, wrongs, byKey cells, explain | (X − 7)² = 1 on totals 6 and 8: 10 cells; two values of X merge | correct | E |
| l4 | screens[1] derive bars | pmf of max(X − K, 0): P(Y = 0) = P(X ≤ K), P(Y = y) = P(X = K + y) | correct | E: the canvas formulas match enumeration for K = 2..12 |
| l4 | screens[1] key, options, explain | at K = 10 totals 2 to 10 pay 0 (33/36); 11 and 12 pay 1 and 2 | correct | E |
| l4 | screens[2] table, keys, byKey, explain | pmf of (X − 7)²: 6, 10, 8, 6, 4, 2 over 36 on 0, 1, 4, 9, 16, 25 | correct | E |
| l4 | screens[3] keys, hints, explain | \|X\| for the two-day change: 0.37, 0.50, 0.13 | correct | E |
| l4 | screens[4] key, options, explain | S = 100 + X is one-to-one, so the same chances sit on 96..104; merging needs a g that is not one-to-one | correct | S: BH theorem 3.7.3 |
| l4 | screens[5] key, options, hints, explain | P(X² = 1) = 0.2 + 0.1 = 0.3; pmf of X² is 0.3, 0.3, 0.4 on 0, 1, 4 | correct | E |
| l4 | screens[6].prose, summary.formula, summary.ideas | P(g(X) = y) = sum of p_X(x) over x with g(x) = y; apply g to values, never to chances | correct | S: BH theorem 3.7.3 |
| l4 | screens[6] key, options, explain | P((X − 7)² = 4) = 8/36 | correct | E |
| l4 | screens[7] keys, hints, byKey | call payoff on 96..104: P(C = 0) = 0.61, P(C = 2) = 0.30, P(C = 4) = 0.09 | correct | E |
| l4 | screens[7].explain | "the call pays something on only 39% of paths" | imprecise | E: 3 of the 9 paths pay; their chance is 0.39. Finding 9 |
| l4 | screens[8] key, slips, hints, explain | short 250 shares: L = −1000 exactly when X = 4, chance 0.09; the map flips the order | correct | D |
| l4 | summary.trap | P(X² = 1) needs both roots; squaring a probability is never the step | correct | D |
| l4 | quiz[0] key, slips, explain | P(X² = 1) = 0.5 | correct | D |
| l4 | quiz[1] key, options, explain | P(3X + 1 = 4) = p(1) = 0.5 | correct | D |
| l4 | quiz[2] key, options, explain | P(max(X − 10, 0) = 0) = 33/36 | correct | E |
| l4 | quiz[3] key, slips, explain | P(\|X\| = 4) = 0.13 | correct | E |
## Level 2: Expectation

### l5-long-run-average

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | screens[0].prose | the average of many repeated counts settles on one number, found without tossing | correct | S: law of large numbers, BH theorem 10.2.1 |
| l5 | screens[1] key, wrongs, hints, explain | heads in three tosses balances at 1.5; a balance point need not be a value of X | correct | E: E[X] = 12/8; centre of mass, BH 4.1 |
| l5 | screens[2] series, key, options | the running average of a fair die settles near 3.5 | correct | MC in the script; the stored series ends at 3.503 |
| l5 | screens[2].explain | after 10 rolls the average was 4.5; after 1,000 a roll moves it by less than 0.003 | correct | E: series value 10 is 4.5; the largest move is 2.5/1001 |
| l5 | screens[2] option `never` why | late rolls barely move a long average | correct | D: a roll moves the mean by (x − mean)/(n + 1) |
| l5 | screens[3].prose, explain | the balance point and the long-run average are the same number, E[X]; one die gives 21/6 = 3.5 | correct | BH 4.1 and 10.2 |
| l5 | screens[3] key, slips | 3.5; 21 unweighted; 1 is the weights | correct | E |
| l5 | screens[4] key, slips, hints, explain | loaded die (6 at 1/2, others 1/10): E = 1.5 + 3 = 4.5 | correct | E |
| l5 | screens[5] key, slips, explain | E[I] = 1/6; an indicator's expected value is its event's chance | correct | S: BH theorem 4.4.1 (fundamental bridge) |
| l5 | screens[6] blocks, key, options, hints | sixes in two rolls: 25/36, 10/36, 1/36; E = 12/36 = 1/3 | correct | E |
| l5 | screens[6].explain | the plain average of the values is 1; for the dice total it is 7 only because the pmf is symmetric | correct | E |
| l5 | screens[7].prose, summary.formula | E[X] = sum of x P(X = x) over the values, "for any discrete random variable" | correct | S: BH definition 4.1.1. Every variable in levels 1 to 3 takes finitely many values, so the sum always exists; the finite-mean condition is stated in l7 `summary.formula.note` |
| l5 | screens[7] key, options, explain | (−1)(0.8) + 4(0.2) = 0 | correct | D |
| l5 | screens[8] solution, tests, starter, `how` | the solution passes the 8 hidden tests, the starter fails, "8 hidden tests" is the count | correct | run in CPython 3 (script) |
| l5 | screens[8] examples[1], explain | simulate(die, 100000) with seed 1 prints 3.50167 | correct | run in CPython (script); `random.choices` is stable across 3.x |
| l5 | screens[8].explain | more draws shrink the gap; the exact sum needs no draws | correct | LLN; the error scales as 1/√n |
| l5 | screens[9] key, slips, hints, feedback | E[P&L] = 0.6 − 0.4 = £0.20; no single day makes £0.20 | correct | E |
| l5 | screens[9].explain | "Over 250 trading days that is about £50" | imprecise | D: the expected total is exactly £50, but the total has standard deviation 1.4 × √250 ≈ £22 for independent days. Finding 10 |
| l5 | summary.ideas | E is the balance point and long-run average; a constant is its own expected value; E need not be a value | correct | BH 4.1 |
| l5 | summary.trap | the unweighted average agrees for equal chances or a symmetric pmf but not in general | correct | D |
| l5 | quiz[0] key, options, explain | E of a constant is the constant | correct | BH 4.1 |
| l5 | quiz[1] key, slips, explain | E[N] = 1.2; plain average 1.5 | correct | E |
| l5 | quiz[2] key, options, explain | after ten tails the next toss is still 0.5; the average settles by dilution, not correction | correct | S: BH 10.2 (gambler's fallacy discussion) |
| l5 | quiz[3] key, slips, explain | 10(0.1) + 1(0.9) = 1.9 | correct | E |

### l6-fair-price

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | screens[0] key, options, hints, explain | £10 on a total of 7 returns 10/6 ≈ £1.67 on average, so £2 loses about 33p a ticket | correct | E |
| l6 | screens[0] option `unknown` why | one roll is unpredictable but the average over many tickets is not | correct | LLN |
| l6 | screens[1] key, options, explain | the simulated break-even price is about £1.67; above it the buyer loses in the long run | correct | MC in the script (1,000 tickets: 1.67 ± 0.12); LLN |
| l6 | screens[2].prose, summary.ideas[0], screens[7].prose | the fair price is defined as the price with zero average profit, which is the expected payoff | correct | S: the classical definition of a fair game (Feller vol. 1, X.3; BH 4.3). It is a definition, not a claim about what anyone would pay; the lesson says a fair bet "has no edge, only risk" and names risk-neutral pricing |
| l6 | screens[2] key, slips, explain | 10 × 6/36 = 1.6667; 10/36 and 5 are slips | correct | E |
| l6 | screens[3] key, slips, explain | expected profit 1.67 − 2 = −0.33; the buyer is favoured only when the price is below E[payoff] | correct | D ("favoured" is in expected profit) |
| l6 | screens[4] key, slips, byKey, explain | 12 × 6/36 + 6 × 2/36 = 7/3; slips 18, 2, 9, 2.1667 | correct | E |
| l6 | screens[5] key, options, explain | pay £1 for £2 on heads: expected profit 0; fair is not good, it has no edge, only risk | correct | D |
| l6 | screens[5].explain | casinos and market makers live on bets priced a little away from fair | correct | S: house edge; bid-ask spread (Harris, *Trading and Exchanges*, ch. 13) |
| l6 | screens[6] key, options, explain | £100 at chance 0.05 has fair price £5; the mode gives £0, the payoff £100 | correct | D |
| l6 | screens[7] key, options | E[payoff] 4 at price 4.50: expected profit −0.50, favours the seller | correct | D |
| l6 | screens[7].explain | over 100 such bets the buyer expects to lose about £50 | correct | D: linearity, 100 × 0.50 |
| l6 | screens[8] lines, key, byKey, explain | E[X − c] = E[X] − c, by splitting the sum and using that the chances add to 1; the only valid order | correct | D; BH theorem 4.2.1 |
| l6 | screens[9] leaves, key, slips, byKey | binary on "above £102" after two days: only up-up, 0.16, £16; slips 48, 32, 64 | correct | E: nine paths |
| l6 | screens[9].explain | desks price by expectation under probabilities read off market prices, called risk-neutral | correct | S: Hull ch. 13 (risk-neutral valuation). Discounting over two days is ignored, which is harmless here |
| l6 | screens[10] key, slips, explain | buying all three £1 tickets costs £1.07 for a sure £1: a 7p sure loss, the overround | correct | D; fair prices of £1 tickets on exclusive, exhaustive results add to 1 |
| l6 | summary.ideas[1], [2], formula, trap | expected profit = expected payoff − price; a fair bet has zero expected profit | correct | D |
| l6 | quiz[0] key, slips, explain | lottery: 1 + 0.5 − 2 = −0.5 (linearity, whether or not the prizes exclude each other) | correct | D |
| l6 | quiz[1] key, slips, explain | 20/36 − 3 = −2.44 | correct | E |
| l6 | quiz[2] key, options, explain | A: 1.80 < 2; B: 0.95 > 0.90; only B favours the buyer | correct | D |
| l6 | quiz[3] key option text | "over many bets you expect to roughly break even" | imprecise | D and MC: the average per bet settles at 0, but the typical size of the total grows like √n (about £80 after 10,000 fair £1 coin bets). Finding 7 |
| l6 | quiz[3] other options, explain | zero expected profit is no edge; single bets still win or lose; only the long-run average is zero | correct | D |

### l7-linearity

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l7 | screens[0] key, slips, explain | row 1 of the totals averages 4.5; row k averages k + 3.5 | correct | E |
| l7 | screens[1] key, options, explain | X + Y and X + X have different shapes and the same average 7; the doubled die is uniform on the even totals | correct | E |
| l7 | screens[1].explain | the average of a sum does not care how its parts depend on each other | correct | BH theorem 4.2.1 |
| l7 | screens[2] key, slips | the six row averages 4.5..9.5 average 7 | correct | E |
| l7 | screens[2].explain (last sentence) | "Nothing in the argument used the dice being independent" | wrong | D: the argument uses "row k averages k + 3.5", that is E[Y given X = k] = 3.5 for every k, which holds because the dice are independent. For Y = X row k has the single cell 2k. Finding 1 |
| l7 | screens[2].explain (rest) | linearity of expectation: E[X + Y] = E[X] + E[Y] | correct | BH theorem 4.2.1 |
| l7 | screens[3] key, slips, explain | E[X + X] = 7; the diagonal 2, 4, .., 12 averages 7; X and X are fully dependent and linearity holds | correct | E |
| l7 | screens[4] cells, key, slips, explain | E[X − Y] = 0 though X − Y = 0 only one roll in six; E\|X − Y\| = 70/36 | correct | E |
| l7 | screens[5] cells, key, slips, explain | E[3X − 5] = 5.5; slips 10.5, −1.5, −4.5 | correct | E |
| l7 | screens[6] key, options | E[X²] = 91/6 for a die, not 3.5² | correct | E |
| l7 | screens[6].explain; screens[7] option `product` why; quiz[2] byKey `product` | "E[XY] = E[X]E[Y] needs independence" | imprecise | D: independence is sufficient, not necessary. The product rule holds exactly when the covariance is zero (X uniform on −1, 0, 1 and Y = X²). Finding 3 |
| l7 | screens[6] byKey `squared` | the product rule fails here, because X depends completely on itself | correct | E: 91/6 against 12.25 |
| l7 | screens[6].explain | E[g(X)] ≠ g(E[X]) in general; for a curve bending upwards the average of the squares beats the square of the average | correct | S: Jensen's inequality, BH theorem 10.1.5 |
| l7 | screens[7].prose, key, options, explain | sums, differences, scalings and shifts pass through E for any X and Y; products and squares do not in general | correct | BH 4.2 |
| l7 | screens[8] lines, key, byKey, explain | derivation of E[X + Y] from the joint table; no line multiplies two marginal chances; the only valid order | correct | D; BH 7.2 (two-dimensional LOTUS) |
| l7 | screens[9] key, options, explain | E[A] = 80, E[B] = −10, total 70 without the joint table; the link changes risk, not the expected P&L | correct | E |
| l7 | screens[10] key, slips, explain | 200 orders at expected £4.50 cost £900 on average; clustering changes the risk, not this number | correct | D |
| l7 | summary.ideas[0], [1], formula and note, trap | linearity for any X and Y with finite means, dependent or not | correct | BH theorem 4.2.1 |
| l7 | summary.ideas[2] | E[X²] ≠ E[X]² unless X is constant; E[XY] = E[X]E[Y] when X and Y are independent | correct | D: Var(X) = 0 only for a constant; BH theorem 7.3.2 |
| l7 | quiz[0], quiz[1] keys, slips, explains | three dice 10.5; E[2X + 3] = 11 | correct | D |
| l7 | quiz[2] key, slip | E[X·X] = 0.5 for a 0-or-1 coin, not 0.25 | correct | E |
| l7 | quiz[2].explain (last sentence) | "The product rule fails for dependent variables" | wrong | D: false as a general statement. X uniform on −1, 0, 1 and Y = X² are dependent with E[XY] = 0 = E[X]E[Y] (script). The rule can fail, not must fail. Finding 2 |
| l7 | quiz[3] key, options, explain | 300 − 120 = 180 whatever the link | correct | D |

### l8-indicators

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l8 | screens[0] cells, key, explain | three sixes at rolls 2, 5, 8; a count is a sum of 0s and 1s | correct | E |
| l8 | screens[1] key, options, explain | the average count of sixes in ten rolls settles near 10/6 ≈ 1.67; 1 is the most common count | correct | E: the mode of Binomial(10, 1/6) is 1; MC in the script |
| l8 | screens[2].prose, key, slips, explain | N = I_1 + .. + I_10, E[N] = 10/6 without the pmf of N | correct | S: BH 4.4 |
| l8 | screens[3] key, slips, byKey | five cards drawn back at random: E[own cards] = 5 × 1/5 = 1; 1/120 is the chance all match | correct | E: 120 permutations |
| l8 | screens[3].explain | the indicators are dependent (four matches force the fifth); the answer is 1 for any number of traders | correct | E; BH example 4.4.4 (matching) |
| l8 | screens[4] key, slips, explain | certain events give E = 10; impossible ones 0; an expected count lies between 0 and the number of events | correct | D |
| l8 | screens[5].prose | birthdays "spread evenly over 365 days" (uniform; independence across people is implied, 29 February ignored) | correct | BH example 4.4.5 |
| l8 | screens[5] key, slips, byKey | C(23,2)/365 = 253/365 ≈ 0.693; slips 23/365, 506/365, 0.5073 | correct | E; MC in the script |
| l8 | screens[5].explain | the pair indicators are dependent: two matches through Bo force the third | correct | D (they are pairwise independent but not mutually; the sentence claims only dependence of the three) |
| l8 | screens[6] key, options, explain | expected fixed points of a shuffled deck is 52 × 1/52 = 1 | correct | BH example 4.4.4; MC in the script |
| l8 | screens[7].prose, key, options, explain, summary.formula | E[N] = P(A_1) + .. + P(A_n) for any events; E[I_k] = P(A_k) from the indicator's pmf | correct | BH theorem 4.4.1 and 4.2.1 |
| l8 | screens[8] lines, key, byKey, explain | count, linearity, indicator pmf, sum of chances; the only valid order | correct | D |
| l8 | screens[9] key, slips, explain | the ten fill chances add to 4.65 | correct | E |
| l8 | screens[9].explain | clustering makes 0 or 10 fills more likely than under independence, with the same expected count | correct | D: for nested limit prices P(10 fills) = 0.1 against a product of 2 × 10⁻⁵, and P(0 fills) = 0.1 against 5 × 10⁻⁴ |
| l8 | screens[10] key, options, explain | 50 × 0.04 = 2 defaults whatever the correlation; the correlation sets the spread | correct | D; MC in the script with a common shock |
| l8 | summary.ideas, trap | write a count as a sum of indicators; no independence needed; skip the distribution | correct | BH 4.4 |
| l8 | quiz[0], quiz[2] keys, slips | 20 × 0.3 = 6; 250 × 0.53 = 132.5 | correct | D |
| l8 | quiz[1] key, slips, explain | aces in five cards: 5 × 4/52 = 5/13, though the draws are dependent | correct | E; BH example 4.4.3 (hypergeometric mean) |
| l8 | quiz[3] key, options, explain | 100 traders: expected own cards is 1 | correct | D |
## Level 3: Variance and co-movement

### l9-measuring-spread

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l9 | screens[0] key, options, explain | two trades with mean £0 differ in distance from the mean: £1 against £3 | correct | D |
| l9 | screens[1] key, slips, explain | at size 2 the signed distances average 0 and the squared ones 4; squaring stops the signs cancelling | correct | D: E[X − μ] = 0 for every X |
| l9 | screens[2].prose, summary.formula | Var(X) = E[(X − μ)²], μ = E[X] | correct | S: BH definition 4.6.1 |
| l9 | screens[2] key, slips, byKey | pmf 1, 3, 7 at 0.5, 0.25, 0.25: mean 3, variance 6; slips 0, 2, 15, 6.667, 3 | correct | E |
| l9 | screens[2].explain | the £7 outcome supplies two thirds of the variance; squaring magnifies big distances | correct | E: 4 of 6 |
| l9 | screens[3] keys, hints, explain | die: squares 6.25, 2.25, 0.25; variance 35/12; sd 1.7078 defined as the root of the variance | correct | E; BH 4.6 |
| l9 | screens[3].explain | "a roll typically lands about 1.7 from 3.5", in the units of the die | correct | D: the root-mean-square distance is 1.708 (the mean absolute distance is 1.5); "typically, about" is the usual reading |
| l9 | screens[4] key, options, explain; quiz[2] | a variance is never negative and is 0 only for a constant | correct | BH 4.6 (Var(X) = 0 exactly when X is constant with chance 1) |
| l9 | screens[5] key, slips, explain, summary.trap | −1 at 0.8 and 4 at 0.2: variance 4 £², sd £2; variance is in squared units | correct | E |
| l9 | screens[6] lines, key, byKey | Var(X) = E[X²] − μ², by expanding and linearity; the only valid order | correct | D; BH theorem 4.6.2 |
| l9 | screens[6].explain | die: 91/6 − 3.5² = 2.9167 | correct | E |
| l9 | screens[7] solution, tests, starter, `how` | the solution passes the 7 hidden tests, the starter fails, "7 hidden tests" is the count | correct | run in CPython (script) |
| l9 | screens[7].explain | the seeded simulation prints 2.9207 and converges to 35/12; `E[X^2] - mu**2` works too | correct | run in CPython (script). The simulated figure divides by n; at 100,000 rolls n − 1 changes the fifth decimal only |
| l9 | screens[8] table, key, slips, explain | A: variance 60,000, sd £244.95; B: sd £500, about twice A's | correct | E |
| l9 | screens[8].explain | for the same expected P&L a desk prefers the smaller sd | correct | S: mean-variance preference, Markowitz (1952); stated as a desk's preference, not a theorem |
| l9 | screens[9] table, key, options, hints | both trades have mean 0, variance 99, sd £9.95; the sd cannot see which side the rare move is on | correct | E |
| l9 | screens[9].explain | the lopsidedness is called skew; insurance sellers show a small sd until the rare day | correct | S: BH 6.2 (skewness); Taleb, *Dynamic Hedging*, on short-option P&L |
| l9 | summary.ideas | distances average to zero; variance and sd units | correct | BH 4.6 |
| l9 | quiz[0], quiz[1], quiz[3] keys, slips, explains | 0 or 4: variance 4; variance 16 £² gives sd £4; 13 − 9 = 4 | correct | D |

### l10-scaling-and-adding

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l10 | screens[0] key, options, explain | Var(X + 10) = Var(X): the mean moves with the outcomes | correct | D; BH 4.6 |
| l10 | screens[1] canvas, key, options, explain | the sd band is 3.5 ± 1.708; only the scale changes the spread; a = 2 doubles the sd, a = −1 leaves it | correct | E |
| l10 | screens[2] key, slips, explain | Var(2X) = 4 × 35/12 = 35/3 | correct | E |
| l10 | screens[3] dots, key, slips, explain | −3X + 5: dots 2..−13, mean −5.5, variance 26.25 | correct | E |
| l10 | screens[4] key, slips, hints, explain | Var(X + Y) = 35/6 = 35/12 + 35/12 for two independent dice; E[T²] = 54.833; E\|T − 7\| = 1.944 | correct | E |
| l10 | screens[5] key, slips, explain | Var(X − Y) = 35/6: Var(−Y) = Var(Y), so for independent variables the minus sign disappears | correct | E |
| l10 | screens[6] key, options, byKey | Var(X + X) = 4 Var(X) = 35/3, twice Var(X + Y); sd of X + Y is 2.415; the extremes are six times as likely | correct | E |
| l10 | screens[6].explain (first clause of last sentence), summary.formula.note | "Adding variances needs independence"; "The second needs X and Y independent" | imprecise | D: Var(X ± Y) = Var(X) + Var(Y) ± 2Cov(X, Y), so zero covariance is what is needed. Independence is sufficient. Finding 3 |
| l10 | screens[6].explain (second clause) | adding sds works only when the two move in lockstep | correct | D: sd(X + Y) = σ_X + σ_Y exactly when ρ = 1 (or one sd is 0) |
| l10 | screens[7] lines, key, byKey, explain | Var(aX + b) = a² Var(X); the only valid order | correct | D |
| l10 | screens[8].prose, key, slip, explain | n independent days: variance n × 100², sd 100√n, £300 at n = 9; mean £500 equals one sd at n = 25 | correct | D |
| l10 | screens[9] key, slips, byKey | 1.2% daily gives 1.2% × √252 = 19.05%; 252 trading days is the stated convention | correct | S: Hull ch. 15 (estimating volatility, 252 trading days) |
| l10 | screens[9].explain | "The √252 rule assumes independent days" | imprecise | D: it also treats the yearly return as the sum of the daily returns, which holds for log returns and only roughly for simple returns. The item never says which. Finding 8 |
| l10 | screens[10] key, slips, explain | double the position, ten independent days: 2 × 400 × √10 = £2,529.82 | correct | D |
| l10 | summary.ideas, formula tex, trap | shift leaves variance; scale a gives a² and sd \|a\|; variances of independent variables add, even for a difference | correct | BH 4.6 |
| l10 | summary.ideas[2] (last clause) | "the sd of n copies grows like √n" | imprecise | D: screens[6] uses "a copy" for the same variable counted again, where the sd grows like n (X + X has sd 2σ). √n is for n independent variables. Finding 5 |
| l10 | quiz[0..3] keys, slips, explains | 36; 5; 8; 4% | correct | D |

### l11-moving-together

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l11 | screens[0] table, key, options, explain | the nine chances add to 1; same-direction corners carry 0.40 against 0.04 | correct | E |
| l11 | screens[1] key, wrongs, byKey, explain | the product of returns is positive only in the two same-sign corners; a zero return gives 0 | correct | E |
| l11 | screens[2].prose | Cov(X, Y) = E[(X − μ_X)(Y − μ_Y)]; with zero means it is E[XY] | correct | S: BH definition 7.3.1 |
| l11 | screens[2] key, slips, explain | Cov = 0.40 − 0.04 = 0.36 %²; positive covariance means the two tend to sit on the same side of their means | correct | E |
| l11 | screens[3] keys, hints, byKey, explain | E[X] = 0.5, E[Y] = 1.4, E[XY] = 1.9, Cov = 1.2 by E[XY] − E[X]E[Y] | correct | E |
| l11 | screens[4].prose | ρ = Cov/(σ_X σ_Y) has no units; σ_X = 1.5, σ_Y = 1.96 | correct | E: variances 2.25 and 3.84; BH definition 7.3.4 |
| l11 | screens[4] key, slips | ρ = 1/√6 ≈ 0.408; slips 1.2, 0.1389, 0.8 | correct | E |
| l11 | screens[4].explain | correlation always lies in [−1, 1]; the extremes mean the points lie exactly on a line | correct | S: BH theorem 7.3.5 (Cauchy-Schwarz) |
| l11 | screens[5] points, derive, key, options, explain | y = ρx + √(1 − ρ²)e builds a cloud of correlation ρ; the sign gives the tilt, the size the tightness | correct | D: Cov(X, ρX + √(1 − ρ²)E) = ρ for unit, uncorrelated X and E |
| l11 | screens[6].prose | the left cloud has "ρ = 0.8" | correct | E: the 40 plotted points have sample correlation 0.80 to two places (script) |
| l11 | screens[6] key, options, byKey, explain | ρ(X, 3Y) = ρ(X, Y); the covariance and the slope Cov/Var(X) triple; correlation is not a slope | correct | D |
| l11 | screens[7] table, key, options, hints, explain | X uniform on −1, 0, 1 and Y = X²: covariance 0, yet Y is a function of X; independence gives zero covariance, not the reverse | correct | E; BH example 7.3.3 |
| l11 | screens[7] option `indep` why, quiz[3] option `zero` why | covariance only catches a straight-line tilt | correct | BH 7.3 |
| l11 | screens[8] lines, key, byKey, explain | Cov = E[XY] − E[X]E[Y]; Var(X) = Cov(X, X); the only valid order | correct | D |
| l11 | screens[9] table, key, slips, hints, explain | Var(X) = 0.5, Var(Y) = 4.5, Cov = 0.78, ρ = 0.52 | correct | E |
| l11 | screens[9].explain | many pairs of large stocks have daily correlations near 0.5 | correct | S: average pairwise correlation of S&P 500 members has ranged roughly 0.2 to 0.6 (Cboe implied correlation index history). "Many", not "most" |
| l11 | screens[10].prose, key, slips, byKey | minimum-variance hedge ratio β = Cov/Var(X) = 1.56: short £156,000 of A; σ_Y/σ_X = 3 would be right only at ρ = 1 | correct | S: Hull ch. 3 (minimum variance hedge ratio h* = ρσ_S/σ_F) |
| l11 | screens[10].explain | the hedge cuts the variance from 4.5 to 4.5 − 0.78²/0.5 = 3.28 | correct | E: Var(Y − βX) on the table |
| l11 | summary.ideas, formula | covariance, correlation in [−1, 1], zero covariance does not prove independence | correct | BH 7.3 |
| l11 | summary.trap (last sentence), quiz[2].feedback.correct | "Scaling either variable leaves ρ unchanged"; "Scaling and shifting Y leave ρ alone" | imprecise | D: ρ(X, aY + b) = sign(a) ρ(X, Y). A negative scale, a short position, flips the sign (script). Finding 4 |
| l11 | summary.trap (first sentence) | correlation is not a slope; covariances in different units cannot be compared | correct | D |
| l11 | quiz[0], quiz[1] keys, slips | 0.5 − 0.2 = 0.3; 6/10 = 0.6 | correct | D |
| l11 | quiz[2] key, options, explain | ρ(X, 2Y + 0.01) = 0.3 (the scale 2 is positive) | correct | D |
| l11 | quiz[3] key, options, explain | opposite sides of the means give negative covariance | correct | D |

### l12-diversification

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l12 | screens[0] cells, key, options, explain | 50:50 mix of two independent ±20% funds returns −20, 0, 0, +20; less spread than one fund | correct | E |
| l12 | screens[1].prose | diversification: lowering risk by mixing assets that do not move in lockstep | correct | S: Markowitz (1952); Bodie, Kane and Marcus ch. 7 |
| l12 | screens[1] key, slips, byKey, explain | mix variance 0.02, sd 14.14% = 20%/√2 | correct | E |
| l12 | screens[2] curve, key, options, explain | Var = w²σ_X² + (1 − w)²σ_Y² + 2w(1 − w)ρσ_Xσ_Y; equal sds: flat at 0.04 for ρ = 1, 0.02 at 50:50 for ρ = 0, 0 for ρ = −1 | correct | D |
| l12 | screens[3] key, slip ranges, explain | sds 30% and 10% with ρ = −1: w = 0.25 gives zero variance, a perfect hedge | correct | D: w = σ_Y/(σ_X + σ_Y) |
| l12 | screens[4] key, slip ranges, explain | ρ = 0.8: the minimum is at w ≈ −0.269 with sd 7.89%, below Y's 10%; any long X adds risk | correct | D: w* = −0.014/0.052; variance rises in w above w* |
| l12 | screens[5] key, slips, hints, byKey | 50:50 of 30% and 10% at ρ = 0.2: variance 0.028, sd 16.73%; slips 0.2, 0.1581, 0.1628 | correct | E |
| l12 | screens[5].explain, summary.ideas[1], summary.trap | the sd of a long-only mix equals the weighted average of the sds only at ρ = 1 and is below it otherwise; at ρ = −1 a mix can be riskless | correct | D: σ_P² = (wσ_X + (1 − w)σ_Y)² − 2w(1 − w)(1 − ρ)σ_Xσ_Y. Read for weights between 0 and 1, which is the case on these screens |
| l12 | screens[6] lines, key, byKey, explain | derivation of the two-asset variance; the cross term carries the correlation; the only valid order | correct | D; BH 7.3 (variance of a sum) |
| l12 | screens[7].prose, summary.formula.note | w* = (σ_Y² − ρσ_Xσ_Y)/(σ_X² + σ_Y² − 2ρσ_Xσ_Y) | correct | D: derivative of the quadratic in w; Bodie, Kane and Marcus ch. 7 |
| l12 | screens[7] key, slips, explain | w* = 0.0075/0.055 = 0.136; w* is positive exactly when ρ < σ_Y/σ_X = 0.6 | correct | D |
| l12 | screens[8].prose | equal weights, common sd σ and common correlation ρ: Var = σ²/n + (1 − 1/n)ρσ² | correct | D: n terms σ²/n² plus n(n − 1) terms ρσ²/n²; MC in the script |
| l12 | screens[8] key, slips, byKey, explain | the sd tends to √(ρσ²) = 13.42%, not 0; 30 assets give 14.28%; shared risk cannot be diversified away | correct | D; Elton and Gruber ch. 4 |
| l12 | screens[8] byKey `zero` | removing all risk "needs ρ = 0" | correct | D: the limit ρσ² is 0 only at ρ = 0 (a common ρ cannot stay negative as n grows) |
| l12 | screens[9] table, key, slips, explain | P&L sds £10,800 and £2,400 at ρ = 0.2: variance 132,768,000 £², sd £11,522 against £13,200 for added sds | correct | E |
| l12 | screens[10] table, key, slips | 500 stocks, σ = 30%, ρ = 0.3: 0.00018 + 0.026946, sd 16.47%; floor 16.43% | correct | E |
| l12 | screens[10].explain | a broad index has an sd near this; index funds remove idiosyncratic risk, never market risk | correct | S: long-run S&P 500 annual volatility is about 15 to 20% (Hull ch. 15); Sharpe (1964) on systematic risk |
| l12 | summary.ideas[0], [2], formula | weighted variances plus a cross term; own risk falls like 1/n, shared risk floors at ρσ² | correct | D |
| l12 | quiz[0..3] keys, slips, explains | 7.07%; 20% at ρ = 1; 10% for four independent assets; ρ = −1 is lowest | correct | D |
## Sets

### review-1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| rv1 | items[0] key, options, explain | {N = 1} = {HTT, THT, TTH}, chance 3/8 | correct | E |
| rv1 | items[1] key, slips, explain | p(x) = cx on 1..4 forces c = 0.1 | correct | D |
| rv1 | items[2] key, slips, explain | P(1 ≤ X ≤ 2) = F(2) − F(0) = 0.7; F(2) − F(1) drops X = 1 | correct | D |
| rv1 | items[3] key, slips, explain | P(X² = 1) = 0.45; P(X² = 4) = 0.25 | correct | D |
| rv1 | items[4] key, slips, explain | three independent fills at 0.6: P(N = 2) = 0.432; 0.648 is at least two | correct | E |
| rv1 | items[5] key, options, explain | P(Y ≥ 5) = 1 − F(4) = 20/36; 1 − F(5) is the strict tail | correct | E |
| rv1 | items[6] key, slips, explain | P(max(X − 9, 0) ≥ 2) = 3/36 | correct | E |
| rv1 | items[7] key, slips, explain | VaR 95% is £6k, the first F at or above 0.95 | correct | E |

### review-2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| rv2 | items[0] key, slips, explain | 4(0.55) − 3(0.45) = 0.85 | correct | D |
| rv2 | items[1] key, slips, explain | fair price 6/6 + 3/6 = £1.50 | correct | D |
| rv2 | items[2], items[3] keys, slips | E[4X − 3] = 7; 30 rolls give 5 expected sixes | correct | D |
| rv2 | items[4] key, slips, explain | E[X²] = 1.1 against E[X]² = 0.01 | correct | D |
| rv2 | items[5] key, slips, explain | the seller of 600 tickets expects 600 × (2 − 10/6) = £200 | correct | D |
| rv2 | items[6] key, options, explain | independent dice: E[XY] = 12.25; for one die times itself the rule fails (91/6) | correct | E; BH theorem 7.3.2. "For independent variables" is the sufficient direction, stated correctly here |
| rv2 | items[7] key, slips, explain | 13 cards hold 1 ace on average though the cards are dependent | correct | D |
| rv2 | items[8] leaves, key, slips, explain | two ±10% days from £50: only up-up pays, 10.50 × 0.25 = 2.625 | correct | E |
| rv2 | items[9] key, slips, explain | 9 overlapping places, each a double with chance 1/4: 2.25; neighbours are dependent | correct | D |

### review-3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| rv3 | items[0] key, slips, explain | −2, 0, 4 at 0.25, 0.5, 0.25: variance 4.75 | correct | E |
| rv3 | items[1] key, slips, explain | Var(5 − 2X) = 12 | correct | D |
| rv3 | items[2] table, key, slips, explain | two 0-or-1 results: Cov 0.15, sds 0.5, ρ = 0.6 | correct | E |
| rv3 | items[3] key, slips, explain | 50:50 at ρ = 0.5: sd 17.32% | correct | D |
| rv3 | items[4] key, slips, explain | 16 independent days: £1,000 | correct | D |
| rv3 | items[5] key, options, explain | zero covariance rules out only a linear tilt; Y = X² is the counterexample | correct | E; BH example 7.3.3 |
| rv3 | items[6] key, options, explain | variance 0.0004 is an sd of 2% | correct | D |
| rv3 | items[7] key, slips, explain | Var(X − Y) = 4 + 9 − 2 × 3 = 7 | correct | D |
| rv3 | items[8] key, slips, explain | uncorrelated 20% and 10%: w* = 0.2, variance 0.008, sd 8.94% | correct | D |

### homework-1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| hw1 | items[0] key, options, explain | P(smaller = 2) = (25 − 16)/36 | correct | E |
| hw1 | items[1] keys, byKey, explain | four tosses: 1, 4, 6, 4, 1 over 16 | correct | E |
| hw1 | items[2] key, slips, explain | F_M(2) = 20/36; F_M(m) = 1 − ((6 − m)/6)² | correct | E |
| hw1 | items[3] lines, key, explain | CDF of the max by independence, pmf as the jump (2y − 1)/36; the only valid order | correct | E |
| hw1 | items[4] key, slips, explain | three-day call struck at 102 pays with chance 0.135 + 0.027 = 0.162; 0.441 includes S = 102 | correct | E: 27 paths |
| hw1 | items[5] key, slips, explain | VaR on a tie: F(4) = 0.95 meets the "at least" rule, so £4k | correct | E; the same definition as l3 |
| hw1 | items[6] key, options, explain | the remainder of the total mod 3 is uniform: 12 cells each | correct | E |
| hw1 | items[7] model, rubric | CDF y²/36, 0 below 1 and 1 from 6 on, flat between; pmf of max(Y − 4, 0) is 16, 9, 11 over 36 | correct | E |
| hw1 | items[8] solution, tests, starter, `how` | the solution passes the 10 hidden tests, the starter fails, "10 hidden tests" is the count | correct | run in CPython (script) |
| hw1 | items[8] byKey test-4, test-7, explain | ten 0.1s added one at a time give 0.9999999999999999; the test-7 chances give 0.9999999999999998 even with `sum` | correct | run in CPython 3.13, whose `sum` is compensated as in Python 3.12 (script) |
| hw1 | items[8] byKey test-5, test-9, test-10 | a zero-chance outcome adds no value; 0.9999 and a negative chance raise | correct | D; the two pmf rules |

### homework-2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| hw2 | items[0] key, slips, explain | the missing chance is 0.4; E[X] = 2.7 | correct | D |
| hw2 | items[1] key, slips, explain | E[X²] − 15 = 1/6; pricing by 3.5² gives −2.75 | correct | E |
| hw2 | items[2] key, accept, wrongs, explain | E[pairs] = n(n − 1)/730 | correct | D |
| hw2 | items[3] lines, key, explain | E[aX + b] = aE[X] + b for discrete X; the only valid order | correct | D |
| hw2 | items[4] key, slips, explain | capped doubling game: each toss adds £1, fair price £5; uncapped, the sum grows without limit (St Petersburg) | correct | S: BH example 4.3.14. This is where the course shows an expected value that does not exist as a finite number |
| hw2 | items[5] key, slips, explain | E[distinct faces in 6 rolls] = 6(1 − (5/6)⁶) = 3.991 | correct | D |
| hw2 | items[6] key, slips, explain | Y = 7 − X: E[XY] = 28/3, below 12.25 because a high top face means a low bottom face | correct | E |
| hw2 | items[6] byKey `product` | "X and Y are dependent, so the product rule fails" | imprecise | D: it fails here because Cov(X, Y) = −35/12; dependence alone does not make it fail. Finding 2 |
| hw2 | items[7] key, slip, explain | decimal odds 1.80, 3.60, 4.50: prices add to 19/18, overround 5.56%; a balanced book keeps 1/19 of stakes | correct | D |
| hw2 | items[8] key, options, explain | two loans: 0.2 expected defaults in both books; no default 0.81 against 0.9; both 0.01 against 0.1 | correct | D |
| hw2 | items[9] key, slips, explain | E[empty venues] = 10 × 0.9¹⁰ = 3.487; the indicators are dependent | correct | D |
| hw2 | items[10] model, rubric | E[matches] = 1 for every n; n = 3 lists 3, 1, 1, 1, 0, 0; N = 2 is impossible | correct | E |

### homework-3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| hw3 | items[0] key, slips, explain | Var(max(X − 4, 0)) = 5/6 − 1/4 = 7/12 | correct | E |
| hw3 | items[1] key, accept, wrongs, explain | Var(I) = p(1 − p), largest 0.25 at p = 0.5 | correct | D; BH example 4.6.4 |
| hw3 | items[2] lines, key, explain | Var(X + Y) = Var(X) + Var(Y) + 2Cov(X, Y) for any X and Y; independence makes the covariance 0 | correct | D; BH 7.3 |
| hw3 | items[3] key, slips, explain | sds 3 and 4 (£k) at ρ = −0.5: √13 thousand | correct | D |
| hw3 | items[4] key, accept, wrongs, explain | 4w² + (1 − w)² = 5w² − 2w + 1, lowest at w = 0.2 | correct | D |
| hw3 | items[5] key, slips, explain | σ = 25%, ρ = 0.36: 13 stocks reach 16% (15.99%); 12 give 16.07%; the floor is 15% | correct | E |
| hw3 | items[6] model, rubric | means 8 and 9, variances 216 and 84, Cov 48, ρ = 0.356, Var(A + B) = 396; 23.86 at ρ = 1 and 17.32 at ρ = 0 | correct | E |
| hw3 | items[7] key, slips, explain | 70:30 at ρ = −0.2: variance 0.029425, sd 17.15% | correct | D |

### problems-1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| pb1 | items[0] parts[0..3] keys, slips, explains | product of two spins of 1..4: p(4) = 3/16, F(4) = 8/16, P(4 < M ≤ 9) = 5/16, P(max(M − 6, 0) = 0) = 10/16; each carried slip is the earlier slip propagated | correct | E |
| pb1 | items[1] parts[0..2] keys, slips | four independent bonds at 0.1: P(1) = 0.2916, F(1) = 0.9477, P(2) = 0.0486 | correct | E |
| pb1 | items[1] parts[3], parts[4] | VaR 95% of L = 25N is £50k; with three bonds F(1) = 0.972 and it falls to £25k; VaR is a level of the CDF, not a share | correct | E |
| pb1 | items[2] parts[0..3] keys, slips, explains | c = 0.15; straddle \|X\|: P(2) = 0.25, F(1) = 0.75; two independent days: P(T ≥ 3) = 0.3375 | correct | E |
| pb1 | items[3] parts[0..3] keys, slips, explains | min of three uniform spreads on 1..5: 27 outcomes with T ≥ 3, F(2) = 0.784, P(T = 2) = 0.296; 1 − 0.6ⁿ ≥ 0.99 first at n = 10 | correct | E |

### problems-2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| pb2 | items[0] parts[0..2] keys, slips | E[claim] = £45, profit £15 a policy, £30,000 on 2,000 whatever the link between claims | correct | D |
| pb2 | items[0] parts[3] key, slips, explain | a £50 excess comes off only when there is a claim: 45 − 50 × 0.15 = 37.5, price £57.50 | correct | D |
| pb2 | items[1] parts[0], parts[1] | a reversal has chance 0.48; 19 indicators give E[R] = 9.12 | correct | D |
| pb2 | items[1] parts[2] key, options, explain | I_2 and I_3 share a day and are dependent, which leaves E[R] alone and matters for the variance | correct | E: P(I_2 = I_3 = 1) = 0.24 against 0.48² = 0.2304 |
| pb2 | items[1] parts[3], parts[4] | E[57 − 8R] = −15.96; break-even gain 45.6/9.88 = £4.62 | correct | D |
| pb2 | items[2] parts[0..3] keys, slips, explains | E[S] = 41.2, E[call] = 2.4, put 1.2 by C − Q = S − 40 and linearity; the max is not linear; her expected profit £0.60 | correct | E; Hull ch. 11 (put-call parity at expiry) |
| pb2 | items[3] parts[0..2] | a draw without replacement: each position is gold with chance 0.3; E[G] = 1.2; E[V] = £38 | correct | E: 210 hands |
| pb2 | items[3] parts[3], parts[4] | P(G ≥ 2) = 70/210; expected bonus 15(1/3 + 1/30) = 5.50; fair price £43.50; the with-replacement slips 0.3483 and 0.0837 | correct | E |

### problems-3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| pb3 | items[0] parts[0..3] keys, slips, explains | mean 1.1, variance 5.89; 100 independent trades: sd √589 = 24.27; sd at most 10% of the mean first at n = 487 | correct | E |
| pb3 | items[1] parts[0..3] keys, slips | E[A] = 0.8%, Var(A) = 2.16, Cov = 1.68, ρ = 7/12 | correct | E |
| pb3 | items[1] parts[4] key, slips, explain | h = Cov/Var(B) = 0.4375 leaves Var(A)(1 − ρ²) = 1.425; the hedge removes ρ² ≈ 34% of the variance | correct | E; Hull ch. 3 |
| pb3 | items[2] parts[0..3] keys, slips | E[X] = 0.12, Var(X) = 0.0196; independent funds: w* = 0.2, sd 0.0626 | correct | E |
| pb3 | items[2] parts[4] key, options, explain | mean per unit of sd: mix 1.02, X 0.86, Y 0.71 | correct | D (a ratio of mean to sd; the item names no risk-free rate and does not call it a Sharpe ratio) |
| pb3 | items[3] parts[0..3] keys, slips, explains | linked fills: Cov(I_j, I_k) = 0.05; Var(N) = 4(0.25) + 12(0.05) = 1.6; sd of 12N − 8 is £15.18; largest n with sd ≤ £20 is 5 | correct | D: variance of a sum over ordered pairs; BH 7.3 |

### fluency-l9-measuring-spread

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| fl9 | families[0] key, wrongs, solution | two-outcome P&L (a with chance p, −b otherwise): variance E[X²] − μ²; slips E[X²] and E[X²] − μ, shown only when they differ from the key | correct | E: all 5 × 12 × 12 sampled cases (script) |
| fl9 | families[1] key, wrongs, solution | three-value variance by the same shortcut; every key is a terminating decimal | correct | D |
| fl9 | families[2] key, wrongs, solution | sd = √(pq)(a + b), the root of the variance; each listed pair gives √(pq) = 0.5, 0.4 or 0.3 | correct | E (script) |
| fl9 | all families | the variance meant is that of a distribution (weights are chances), so there is no n or n − 1 choice | correct | D: no item in levels 1 to 3 computes a sample variance from data; the two simulations divide by n at 100,000 draws |

# Claim ledger: random-vars levels 4 and 5 (audit round 1, blind)

Stage 1 course, full ledger. One row per claim, judged one at a time. Columns: path | claim | verdict | basis. The file is the section heading. `s[n]` is `screens[n]`, `q[n]` is `quiz[n]`, `i[n]` is `items[n]`, `p[n]` is `parts[n]`. "script" means `docs/reports/random-vars-L4-5-concepts.py`. Sources: Blitzstein and Hwang, *Introduction to Probability* (BH), 2nd ed.; Casella and Berger, *Statistical Inference* (CB), 2nd ed.; Ross, *A First Course in Probability* (Ross).

## l13-joint-tables.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[1].prose | nine joint cells add to 1 | correct | sum 0.12+0.06+0.02+0.10+0.30+0.10+0.03+0.09+0.18 = 1 |
| s[1].widget.answer | "market falls 1%" is row 1 | correct | row heads are X; wrong set `column` is the Y = −2 column, as its feedback says |
| s[1].explain | disjoint cells add: P(X = −1) = 0.20 | correct | additivity over disjoint events, BH 1.6 |
| s[2].explain | P(Y = 2) = 0.02+0.10+0.18 = 0.30 | correct | column sum |
| s[3].prose | row and column totals are the marginal distributions | correct | BH 7.1 definition |
| s[3].widget | margins 0.25, 0.45, 0.30, total 1 | correct | column sums recomputed |
| s[3].explain | a margin is a pmf for Y alone; counts every cell once | correct | marginalisation, BH 7.1 |
| s[4].widget | P(Y = −2 given X = −1) = 0.12/0.20 = 0.60 | correct | definition of conditional pmf |
| s[4] option col | 0.48 = 0.12/0.25 conditions on Y | correct | 0.12/0.25 = 0.48 = P(X = −1 given Y = −2) |
| s[4] option marg | 0.25 is P(Y = −2) | correct | column total |
| s[5].widget | conditional row 0.60, 0.30, 0.10 | correct | each cell over 0.20 |
| s[5].fb r3c2 | dividing a row by its total always gives sum 1 | correct | needs total > 0, which s[7] and the summary state |
| s[5].explain | drop six times as likely as rise | correct | 0.60/0.10 |
| s[6] key | 0.10, 0.30, 0.60 | correct | row 3 over 0.30 |
| s[6] option cols | 0.12, 0.20, 0.60 are P(X = 1 given Y = y), sum 0.92 | correct | 0.03/0.25, 0.09/0.45, 0.18/0.30 |
| s[6].explain | raw cells sum to P(X = 1) | correct | row sum |
| s[7] lines | conditional row sums to 1 when P(X = x) > 0 | correct | derivation checked line by line |
| s[8].widget | 0.60, 0.50, 3/13 | correct | 0.12/0.20, 0.40/0.80, 0.12/0.52 |
| s[8].explain | "a real edge" 0.60 against 0.50 | correct | conditional chances differ; population table, no sampling claim |
| s[8].explain | "You met this table as Bayes on a trading signal in Conditional Probability" | imprecise | `conditional/l26-trading-signal` uses a different table (flash before 60% of up days, 40% of down days); finding 1 |
| s[9].widget | P(B = 2 given A = 2) = 0.75; slips 0.30 cell, 0.40 margin | correct | 0.30/0.40 |
| s[9].explain | fills move together because price trades through both | correct | plausible mechanism, stated as story not theorem |
| summary.ideas | three summary statements | correct | restate rows above |
| summary.formula | conditional pmf, defined only when P(X = x) > 0 | correct | BH 7.1 |
| summary.trap | a conditional row that does not add to 1 was not divided by the margin | correct | follows from s[7] |
| q[0] | P(Y = 1) = 0.40; slips 0.30, 0.50 | correct | recomputed |
| q[1] | P(X = 1 given Y = 1) = 0.75; reversed 0.60 | correct | 0.30/0.40; 0.30/0.50 |
| q[2] | list adding to 0.9 cannot be a conditional pmf | correct | pmf sums to 1 |
| q[3] | margins give P(Y = 2) but not a cell or a conditional | correct | "always" framing; Fréchet class has many tables for generic margins |
| q[3] option joint why | "The margins do not fix any one cell" | correct | true as an answer to "always"; degenerate margins aside (see hw-4 finding 18 for the "never" form) |

## l14-independent-rvs.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[0] key | P(Y = 1 given X = 2) = 0.40 = P(Y = 1) | correct | 0.12/0.30 |
| s[0] option col | 0.30 = P(X = 2 given Y = 1) | correct | 0.12/0.40 |
| s[1] derive | every rescaled row is 0.30, 0.40, 0.30 | correct | three rows recomputed |
| s[1].explain | rows equal the margin, so each cell is row total times column total | correct | P(y given x) = P(y) iff P(x, y) = P(x)P(y) |
| s[2].prose | definition: every conditional row equals the margin | correct | equivalent to factorisation when rows have positive total |
| s[2].prose | C and D have the same margins as A and B | correct | script: margins match |
| s[2].widget | products 0.15, 0.20, 0.15, 0.09, 0.12, 0.09 | correct | recomputed |
| s[3].answer | four cells differ: top-left 2 by 2 block | correct | script `mism(CD)` |
| s[3].explain | a single failing cell is enough for dependence | correct | independence is "for every x, y" |
| s[4] key | E[XY] = 1.10 = E[X]E[Y]; slips 2.1, 0.56 | correct | 0.20+0.30+0.24+0.36; 1.1+1.0; 0.20+0.15+0.12+0.09 |
| s[4].explain | independence forced Cov = 0 | correct | BH 7.3 |
| s[5] key | pools dependent: cell (1,1) is 0.11 against 0.09 | correct | script |
| s[5] option yes-margins why | every joint table has margins that add to 1 | correct | trivial |
| s[5] option no-equal why | independence does not need equal cells | correct | A and B table |
| s[5].explain | four cells fail: (1,1), (1,2), (2,1), (2,2) | correct | script |
| s[5].explain | "A default in one pool makes two in the other likelier" | wrong | P(Y = 2 given X = 1) = 0.01/0.30 = 0.033 < 0.10, and P(Y = 2 given X ≥ 1) = 0.05/0.50 = 0.10 exactly; true only for X = 2; finding 2 |
| s[5].explain | checking first row or margins misses it | correct | first row and first column all match their products |
| s[6] key | Cov(X, X²) = 0; slips 2/3 and 2/9 | correct | E[X³] = 0, E[X] = 0; Var(Y) = 2/3 − 4/9 |
| s[7] key | dependent: P(0,0) = 1/3 against 1/9 | correct | direct |
| s[7].explain | covariance measures only straight-line co-movement | correct | Cov is bilinear; ρ = ±1 iff linear, BH 7.3 |
| s[8] lines | E[XY] = E[X]E[Y] under independence; converse fails | correct | finite double sum factors |
| s[9] canvas | every margin 0.25, correlation 0 | correct | script |
| s[9] key | P(B = 3 given A = 3) = 0.5; slips 0.25, 0.0625, 0.125 | correct | 0.125/0.25 |
| s[9].explain | big move predicts big move of either sign; correlation misses shared volatility | correct | E[B² given A] is 9 or 1; correlation 0 |
| s[10] key | exactly one fill 0.50; slips 1.1, 0.3, 0.2 | correct | 0.30+0.20 |
| summary.ideas[0] | independence iff every cell is a product; one failing cell breaks it | correct | definition |
| summary.ideas[1] | independence gives flat conditional rows and Cov = 0 | correct | sufficient direction only, as stated |
| summary.ideas[2] | zero covariance does not give independence | correct | Y = X² example |
| summary.formula.note | "Matching margins, or one matching cell, prove nothing" | imprecise | in a 2 by 2 table one matching cell forces all four (script, algebra: a = rc gives r − a = r(1 − c)); the lesson's own s[10] and q[0] are 2 by 2; finding 3 |
| summary.trap | "Checking one cell, or the margins, is not a test" | imprecise | same as above; finding 3 |
| q[0] | 2 by 2 table independent, all four cells are products | correct | 0.28, 0.42, 0.12, 0.18 |
| q[0] option one why | the table decides it directly | correct | pmf given in full |
| q[1] | E[XY] = −6 | correct | independence |
| q[2] | Cov = 0 means E[XY] = E[X]E[Y], not independence | correct | definition of covariance |
| q[3] | neither fills 0.18; slips 0.9, 0.28 | correct | 0.3 × 0.6 |

## l15-given-information.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[0] table | margins 0.20, 0.50, 0.30; 0.23, 0.42, 0.35 | correct | recomputed |
| s[0] key | E[Y given X = −1] = −0.8 | correct | −2(0.5) + 2(0.1) |
| s[0] options | −0.16 unscaled, 0.24 overall, −2 mode | correct | each recomputed; mode has chance 0.5 |
| s[1] derive | conditional rows and means −0.8, 0.2, 1.0 | correct | script |
| s[1] option equal why | at x = 0 the average is 0.2, not 0 | correct | row 2 |
| s[2].prose | definition of conditional expectation as the row average | correct | BH 9.1 |
| s[2].widget | 0.2 and 1.0 | correct | script |
| s[3].prose | E[Y given X] takes −0.8, 0.2, 1.0 depending on X | correct | BH 9.2 |
| s[3] key | P(E[Y given X] = 1.0) = 0.3; slips 0.18, 0.35, 1.0 | correct | the three conditional means are distinct, so the event is X = 1 |
| s[3].explain | E[Y given X] is a random variable, a function of X | correct | BH 9.2 |
| s[4] key | g = 0.2 minimises average squared error | correct | E(Y − g)² = Var + (mean − g)²; script grid search |
| s[4].explain | errors 1.96, 1.9616, 2.00 | correct | script |
| s[4].explain | E[Y given X = x] against x is the regression function, best guess under squared error | correct | BH 9.3, CB 4.4 |
| s[4] option mode why | 0 is right most often | correct | chance 0.5 |
| s[5] key | 1.0; slips 0.30 unscaled, 0.77 column-divided, 0.24 | correct | script (0.7677) |
| s[5].explain | unscaled sum short by factor P(X = 1) | correct | 0.30 = 1.0 × 0.30 |
| s[6] key | E[Y given X = 2] = 1.0 = E[Y] under independence | correct | rows equal the margin |
| s[6].explain | when X ⊥ Y the regression function is flat | correct | sufficient direction, as stated |
| s[7] lines | E[Y given x] = (1/P(x)) Σ y P(x, y) | correct | derivation checked |
| s[8].widget | −0.9 and 0.7; columns add to 1 | correct | recomputed |
| s[8].explain | "conditional beta" 0.9 down, 0.7 up; single beta 0.8 hides asymmetry | correct | ratios of mean moves at x = ∓1; the line through the two points has slope 0.8; loose use of "beta" but consistent with downside and upside beta |
| s[9] key | E[F given Q = 500] = 220; slips 225, 500, 70 | correct | 30 + 90 + 100 |
| s[9].explain | 44% and 70% of quote; five times the size, about three times the fill | correct | 220/500, 70/100, 220/70 = 3.14 |
| summary.ideas[1] | regression function is the best guess under squared error | correct | as s[4] |
| summary.ideas[2] | if X ⊥ Y then E[Y given X = x] = E[Y] | correct | one direction only |
| summary.formula | sum y times cells, divide once | correct | s[7] |
| summary.trap | raw cells forget the division; column totals mix conditions | correct | s[5] |
| q[0] | 8; slips 4, 6 | correct | 10 × 0.40/0.50; E[Y] = 6 |
| q[1] | E[Y given X] is a random variable, a function of X | correct | BH 9.2 |
| q[1] option funcy why | Y has been averaged out | correct | definition |
| q[2] | 3 under independence | correct | as s[6] |
| q[3] | 2.25; slips 7/3, 2 | correct | 0.25 + 1 + 1 |

## l16-averaging-averages.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[0] key | E[Y] = 0.24; slips 0.13, −0.16, 0.2 | correct | weighted sum; plain mean 0.133; product −0.16 |
| s[0].explain | matches the margin: −2(0.23) + 2(0.35) | correct | 0.24 |
| s[1] key | break-even at 40% volatile; slips 0.5, 0.6 | correct | 120 = 300p; at 0.5 average −£30; flipped weights give 0.6 |
| s[2].prose | law of total expectation, discrete form | correct | BH 9.1 (Theorem 9.1.5) |
| s[2] key | E[N given tail first] = 1 + E | correct | independence of tosses (fair coin, stated) gives a fresh copy |
| s[3] | E = 1 + E/2 gives E = 2 | correct | algebra; E finite since geometric series converges |
| s[4] key | E = 4 for p = 1/4; slips 3, 0.25, 1 | correct | E = 1 + 3E/4; dropping the 1 gives E = 1 |
| s[5] key | two heads in a row: E = 6; slips 4, 3 | correct | E = 3/2 + 3E/4; script MC |
| s[5].explain | a tail after a head wastes two tosses | correct | restart from the start state |
| s[6] key | first six: 6 rolls; colleague's 5 counts misses only | correct | E = 1 + 5E/6; E[failures] = (1 − p)/p = 5 |
| s[7] lines | E[N] = 1/p for independent trials, p > 0 | correct | first-step analysis, Ross 7.5; hypothesis stated in prose |
| s[7].explain | p = 1/2, 1/4, 1/6, 1 give 2, 4, 6, 1 | correct | 1/p |
| s[8] code | `n = 1` then count tails; `rng.random() >= p` is a tail | correct | random() uniform on [0, 1); P(≥ p) = 1 − p |
| s[8].how | within about six standard errors of 1/p | correct | sd √(1 − p)/p; 0.05/0.0063 = 7.9, 0.15/0.0245 = 6.1, 0.12/0.02 = 6.0 |
| s[8].explain | seeds give 1.99834, 6.03976, 5.03602 | correct | script runs the taught solution |
| s[8].explain | `n = 0` gives 1/p − 1 | correct | counts failures only |
| s[8] starter | starter fails the tests | correct | script |
| s[9] key | fill wait 5 minutes; slips 4, 0.2 | correct | 1/0.2; independence of minutes stated |
| s[10] key | £130; slips −50, 280, −150 | correct | 280 − 150 |
| s[10].explain | volatile regime takes back more than half the calm gains | correct | 150/280 = 54% |
| summary.ideas[0] | law of total expectation | correct | as s[2] |
| summary.ideas[1] | failure branch holds a fresh copy plus the trial used | correct | needs independence, stated in s[7] |
| summary.ideas[2] | "Trials that each succeed with chance p take 1/p on average" | imprecise | independence dropped; with fully dependent trials (all succeed or all fail) the wait is 1 or infinite; finding 4 |
| summary.formula.note | never multiply the conditional averages | correct | the law is a weighted sum |
| summary.trap | forgetting the first trial gives 1/p − 1, the failures | correct | hw-4 h-failures |
| q[0] | p = 1 gives 1 trial | correct | N = 1 surely |
| q[1] | £11,250; slip 19,000; grade C carries 60% | correct | 1,000 + 3,500 + 6,750; 6,750/11,250 |
| q[2] | 3 rolls; slips 2, 6 | correct | p = 1/3 |
| q[3] | E[Y] = 5; slips 4, 12 | correct | 0.5 + 4.5 |

## l17-variance-given-information.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[0] key | 0.8(10,000) + 0.2(90,000) = 26,000; slips 50,000, 19,600, 90,000, 10,000 | correct | recomputed; 140² = 19,600 |
| s[1] sim | simulated days have regime means and sds as stated | correct | two-point outcomes 220/20 and 120/−480: means 120, −180; sds 100, 300 (script) |
| s[1] key | variance settles above 26,000, near 40,000 | correct | population variance 40,400 (script, exact and MC) |
| s[2].prose | E[Y given X] is a random variable with centre £60 | correct | 96 − 36 |
| s[2] key | Var(E[Y given X]) = 14,400; slips 30,600, 120, 90,000, 3,600 | correct | 2,880 + 11,520 |
| s[3].prose | law of total variance | correct | BH 9.5 (Eve's law), CB Theorem 4.4.7 |
| s[3] key | 40,400; sd £201; 26,000 alone gives £161 | correct | √40,400 = 200.998; √26,000 = 161.2 |
| s[4].widget | conditional variances 1.76, 1.96, 1.8 | correct | script |
| s[5].prose | given N = n, H has mean n/2 and variance n/4 | correct | binomial(n, 1/2) |
| s[5].widget | 7/8, 35/48, 77/48 | correct | script exact pmf of H |
| s[5].fb r1c1 | scaling by 1/2 divides the variance by 4 | correct | Var(aN) = a²Var(N) |
| s[6].prose | Var(Y given X) is a random variable until X is known | correct | BH 9.5 |
| s[6] key | E[Var(Y given X)] = 1.872; slips 1.84, 1.96 | correct | script |
| s[6].explain | Var(E[Y given X]) = 0.3904; total 2.2624 matches the margin | correct | script both ways |
| s[7] key | the report left out the spread of the regime averages | correct | 40,400 − 26,000 = 14,400 |
| s[7] option noise why | the gap stays however long we wait | correct | population identity |
| s[7].explain | about 20% steadier in sd | correct | 161/201 = 0.80 |
| s[8] key | 2.64; slips 2.6, 0.04; overall mean 0 | correct | 0.08 − 0.08 = 0; 0.008 + 0.032 |
| s[8].explain | equal conditional means make the second piece 0; Y fixed by X makes the first 0 | correct | each piece is a variance or an average of variances |
| s[9] lines | proof of the law of total variance | correct | checked line by line, BH 9.5.4 |
| s[10] key | share 14,400/40,400 = 0.3564; slips 0.6436, 0.5538, 0.2 | correct | recomputed |
| s[10].explain | −£480 is 6 calm sds and 1 volatile sd below the regime means | correct | (120 + 480)/100; (−180 + 480)/300 |
| s[10].explain | "a mixture has fatter tails than either regime" | imprecise | with normal regimes the mixture's chance below −£480 is 0.032 against 0.159 for the volatile regime alone; only the kurtosis (7.5) exceeds a normal's (script); finding 5 |
| summary.ideas | three statements | correct | as s[3], s[8] |
| summary.trap | stopping at the average variance misses the second piece | correct | s[7] |
| q[0] | 5 + 3 = 8 | correct | the law |
| q[1] | 29; slips 4, 25, 33 | correct | 4 + 25 |
| q[2] key | Y = X²: E[Var(Y given X)] = 0 | correct | Y is a function of X |
| q[2] option vary why | "That holds only if X tells you nothing about Y" | imprecise | E[Var(Y given X)] = Var(Y) iff E[Y given X] is constant, which is weaker than independence (script: vol-regime table); finding 6 |
| q[3] key | Var(Y) ≥ E[Var(Y given X)] for every X, Y | correct | second piece is a variance (finite variance assumed throughout) |
| q[3] option eq why | second piece vanishes only when the regime averages agree | correct | Var(E[Y given X]) = 0 iff constant |

## l18-random-sums.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[0].prose | each fill earns £5 on average whatever N is | correct | hypothesis stated |
| s[0] key | E[S] = 100 = E[N]E[X]; slips 5, 20, 125 | correct | 30 + 20 + 50; E[N] = 20 |
| s[1] sim | fills £35 or −£25: mean 5, sd 30; dashed line 20 × 900 | correct | (35 − 5)² = 900 |
| s[1] key | variance settles above 18,000, near 18,500 | correct | Var(N) = 20; 18,000 + 500 |
| s[2] key | Var(S given N = 25) = 22,500; slips 562,500, 750, 900 | correct | independent fills add variances |
| s[2].explain | no factor 25² because fills do not move together | correct | Var(ΣX) = nVar(X) for uncorrelated terms |
| s[3].prose | "Eve's law from lesson 17" | imprecise | l17 never names the law "Eve's law" (nor l16 "Adam's law"); the learner meets the name here undefined; finding 7 |
| s[3].widget | 18,000, 500, 18,500; sd £136.01 | correct | script |
| s[4].prose | pieces E[N]Var(X) and Var(N)E[X]²; E[S] = E[N]E[X] | correct | BH Example 9.6.1, Ross 7.5 |
| s[4] key | fixed N = 20: sd £134.16; slips 136.01, 600, 18,000 | correct | √18,000 |
| s[5] key | die and coins by the formula: 77/48; slips 0.875, 3.0625 | correct | 3.5/4 + 35/48 |
| s[6] key | £600 treats 20 fills as one fill scaled up | correct | sd of sum is √20 × 30 = 134 |
| s[6] option count why | the count adds only 500 | correct | Var(N)E[X]² |
| s[6] option nothing why | sum of independent fills spreads like the square root of their number | correct | sd = √n σ |
| s[7] lines | proof of the random-sum variance | correct | each step checked; uses fills independent given N with unchanged mean and variance |
| s[7].explain | "Adam's law gives the mean the same way" | imprecise | name not introduced; finding 7 |
| s[8] key | fills average 0: Var(S) = 18,000; slips 18,500, 134.16 | correct | second term has factor 0 |
| s[8].explain | "The formulas also need N independent of the fills: if busy days have worse fills, they fail" | imprecise | independence is sufficient, not needed: Wald's identity keeps E[S] = E[N]E[X] for a stopping time (script); the example itself is right; finding 8 |
| s[9] code | `variance = en * vx + vn * ex ** 2` | correct | the formula; seven tests recomputed (172,000,000; 225; 77/48) |
| s[9].explain | seed 8 gives sample variance 18466.21 | correct | script runs the taught code |
| s[9] code | simulation uses the population variance of daily totals | correct | E[S²] − mean² over trials |
| s[10] key | 23,200; slips 21,600, 152.32, 518,400 | correct | E[N] = 24, Var(N) = 64; cross-check by total variance over the regime (script) |
| s[10].explain | first term grows by 3,600, second adds 1,600 | correct | 21,600 − 18,000 |
| s[10].explain | if volatile days had worse fills the formulas would fail | correct | then E[S given N] is not N E[X]; specific case |
| summary.ideas[0] | given N, S is an ordinary sum of N independent fills | correct | under the stated assumptions |
| summary.ideas[2] | "If N depends on the fills, the formulas fail" | imprecise | converse of the theorem; false in general (Wald; shape-only dependence, script); finding 8 |
| summary.trap | sd times count treats fills as moving together | correct | perfect correlation gives nσ |
| q[0] | 86; slips 50, 500, 110 | correct | 50 + 36; 100 × 5; 4 × 5 + 10 × 9 |
| q[1] | constant fill £10: Var(S) = 2,000 | correct | Var(10N) |
| q[2] key | formulas fail when busy days have worse fills | correct | specific dependence that changes the conditional mean |
| q[2] option rand why | "They fail only if the count and the fills are linked" | imprecise | they also fail when fills are correlated with each other; and a link need not break them; finding 8 |
| q[2].explain | given N, fills taken independent with the same mean and variance | correct | the proof's hypotheses |
| q[3] | insurer sd £13,115 | imprecise | key needs claims independent of each other and of the count; prompt does not say so; finding 9 |
| q[3] slips | 10,392 and 36,000 | correct | √108,000,000; 12 × 3,000 |

## l19-convex-bets.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[0] key | £99 after +10% and −10%; slips 100, 90, 110 | correct | 1.1 × 0.9 |
| s[1].explain | a concave curve's chord lies below it | correct | definition of concavity |
| s[2].prose | definitions of concave and convex; Jensen for concave g | correct | BH 10.1, CB Theorem 4.7.7 |
| s[2] key | ½ ln 0.99 = −0.00503; slips 0, +0.00503, 0.0953 | correct | script |
| s[2].explain | it is the daily growth rate of the £100 | correct | long-run growth rate is E[ln(1 + R)] by the law of large numbers |
| s[3] key | E[X²] − (E[X])² = 9 = Var(X) | correct | 34 − 25 |
| s[3].explain | Jensen for x² says a variance is never negative | correct | x² convex |
| s[4] key | average price £17.14; slips 23.33, 20, 17.5 | correct | 300/17.5 |
| s[4].explain | 1/x convex so E[1/X] ≥ 1/E[X]; a fixed sum buys more shares than at the average price | correct | 0.0583 > 0.0429; 1/x convex on x > 0 |
| s[5] key | E[(X − 100)⁺] = 10; slips 0, 20, 100 | correct | ½(20) |
| s[5].explain | convex payoff has expected value at least its value at the expected price | correct | Jensen; "worth" read as expected payoff, no discounting claimed |
| s[6] key | E[√X] < √E[X] for positive non-constant X | correct | strict concavity of the root |
| s[6] option equal why | gap never zero unless X is constant | correct | strict concavity |
| s[6] option dep why | one direction holds for every positive X | correct | Jensen needs only concavity and a finite mean |
| s[6].fb equal | "The gap is about σ² over a few times the mean" | imprecise | second-order gap is σ²/(8μ^1.5), not σ²/(kμ); for X = 1 or 9 it is 0.18 against an exact 0.24 (script); finding 10 |
| s[6].explain | X = 1 or 9: 2 against √5 | correct | recomputed |
| s[7] slots | e^X: left ≥ right; root: left ≤ right; cube on X > 0: left ≥ right; E[X]E[Y] against E[XY]: either way | correct | convexity of each on the stated domain; gap is −Cov |
| s[8] lines | proof of Jensen by the tangent at μ | imprecise | assumes g′(μ) exists; the lesson's own call payoff has a kink at its mean, £100; a supporting line is needed there; finding 11 |
| s[9] key | X = −3 or 1: gap −12; slips 12, 0, −13 | correct | −13 − (−1) |
| s[9].fb sign | "This X lives where the cube bends down" | imprecise | X = 1 lies where the cube bends up; the reason is that the chord from −3 to 1 is below the curve at −1; finding 12 |
| s[9].explain | X = −1 or 3 gives +12; no inequality in general | correct | 13 − 1 |
| s[10].prose | Cauchy–Schwarz for expectations | correct | BH 10.1.1, CB Theorem 4.7.3 |
| s[10] key | max abs covariance 6; slips 5, 36, 1.5 | correct | √(4 × 9) |
| s[10].explain | abs ρ ≤ 1; equality only for a straight-line relation | correct | equality case of Cauchy–Schwarz, sds positive |
| s[11] key | average log return 0.818%; slips 1%, 0.64%, 0.18% | correct | script |
| s[11].explain | μ − σ²/2 = 0.82% from the Taylor series | correct | ln(1 + r) ≈ r − r²/2; E gives μ − (σ² + μ²)/2, μ² negligible |
| s[11].explain | "Over 120 months that is e^0.982 = 2.67 times your money, not 1.01^120 = 3.30" | imprecise | 3.30 is exactly the expected wealth under independence; 2.67 is the typical (median) path (script MC: median 2.67, mean 3.30); finding 13 |
| s[11].explain | Kelly maximises E[ln W], not E[W] | correct | Kelly (1956); `limits/l14-best-value` teaches the Kelly fraction |
| summary.ideas[0] | concave: E[g(X)] ≤ g(E[X]); convex reverses | correct | Jensen |
| summary.ideas[1] | "Equality needs X constant" | imprecise | true for strictly curved g only; a call payoff gives equality for any X that stays one side of the strike; finding 14 |
| summary.ideas[1] | gap for x² is the variance; for ln(1 + R) about σ²/2 | correct | s[3], s[11] |
| summary.ideas[2] | if g bends both ways no inequality holds for every X | correct | s[9] |
| summary.trap | a nearly linear function still has a gap | correct | strict curvature, non-constant X |
| q[0] | E[ln X] < ln E[X] for positive non-constant X | correct | strict concavity |
| q[0] option eq why | equality needs X constant, or a straight-line g | correct | in the context of ln |
| q[1] key | gap 1 = Var(X); slips 5, 4 | correct | 5 − 4 |
| q[1].fb sd | wrong value 0.5: "Half the range is not the variance" | wrong | half the range of {1, 3} is 1, which equals the variance; 0.5 is a quarter of the range; finding 15 |
| q[2] | average price £8; slips 12.5, 25 | correct | 200/25 |
| q[3] | X of both signs: no inequality for the cube | correct | s[9] pair of examples |

## l20-many-categories.json

| path | claim | verdict | basis |
|---|---|---|---|
| s[0] key | C(10, 5) = 252; slip 30,240 ordered | correct | 30,240/120 |
| s[0].explain | bars symmetric: choosing 5 up also chooses 5 not up | correct | C(n, k) = C(n, n − k) |
| s[1].widget | 2,520 records; chance 0.0851 | correct | script |
| s[1].explain | 2,520 = 10!/(5! 2! 3!); each record 0.00003375 | correct | recomputed |
| s[2].prose | multinomial pmf; each count alone is binomial | correct | BH 7.4 (lumping) |
| s[2] key | P(5 ups) = 252/1024 = 0.2461 | correct | binomial(10, 0.5) |
| s[2].fb one | 0.0313 "is the chance of one particular record" | wrong | 0.0313 = 0.5⁵; one up or not-up record has chance 0.5¹⁰ = 0.00098, and 252 × 0.0313 = 7.9; finding 16 |
| s[3].prose | counts that add to n cannot be independent | correct | N_down ≤ n − N_up; non-degenerate chances here |
| s[3] lines | Cov(N_up, N_down) = −n p_up p_down = −1.5 | correct | script exact; BH Theorem 7.4.6 |
| s[3].explain | Cov(N_i, N_j) = −n p_i p_j for different categories | correct | same |
| s[4].prose | binomial chances 0.2051 and 0.2001, product 0.0410 | correct | 210/1024; 210 × 0.3⁴ × 0.7⁶ |
| s[4] key | P(4 up, 4 down) = 0.0638 | correct | script |
| s[4].widget.accept | "3150 × 0.0000202" | imprecise | one record is 0.00002025; 3150 × 0.0000202 = 0.0636, not 0.0638; finding 17 |
| s[4].explain | correlation −1.5/√(2.5 × 2.1) = −0.65; product of marginals cannot be right | correct | script; nonzero covariance rules out independence |
| s[5] key | E[T] = 7.5; slips 2.5, 4.5, 1.2 | correct | 3/0.4 |
| s[5].explain | "The waits need not be independent for the mean, only for the variance" | imprecise | adding variances needs zero covariance, not independence; finding 19 |
| s[6].prose | "Eve's law gives V = 0.6V + 1.5" | imprecise | equation right (Var of means 1 and 3.5 with chances 0.4, 0.6 is 1.5); name undefined; finding 7 |
| s[6] key | Var(T) = 11.25; slips 3.75, 7.5, 33.75 | correct | 3 × 0.6/0.16; script exact |
| s[6].fb | formula r(1 − p)/p² | correct | BH 4.3 with the trials convention |
| s[7].prose | negative binomial as trials up to the rth success | correct | convention stated, and the failures convention is named in the explain |
| s[7].widget | P(T = 5) = 0.1382; P(T ≤ 6) = 0.4557 | correct | script |
| s[7].explain | P(T ≤ 6) is the chance of at least three wins in six trades | correct | event identity |
| s[8] key | C(5, 3) p³q² = 0.2304 is exactly three wins in five trades | correct | binomial |
| s[8] options | 0.3174 is T ≤ 5; six trades would change coefficient and power | correct | 0.064 + 0.1152 + 0.1382 |
| s[8].explain | 10 patterns include 4 with an earlier third win | correct | 10 − 6 |
| s[9] key | zero-chance category with zero count: 0.2508 | correct | 0⁰ = 1 convention stated; equals binomial(10, 0.6) at 6 |
| s[9].explain | r = 1 negative binomial is the geometric | correct | C(t − 1, 0) = 1 |
| s[10] code | `multinomial_pmf` and `nb_pmf` | correct | script runs solution; `comb(t − 1, r − 1)` is 0 for t < r |
| s[11] key | P(T > 10) = 0.1673; slips 0.8327, 0.006 | correct | at most two wins in ten |
| s[11].explain | mean 7.5, sd 3.35; a wait past ten is far from rare | correct | 17% |
| summary.ideas[1] | counts that add to n are negatively correlated | correct | multinomial, both chances positive |
| summary.ideas[2] | mean r/p, variance r(1 − p)/p² | correct | sum of r independent geometric waits |
| summary.trap | C(t, r) lets the last trial be a failure | correct | s[8] |
| q[0] | 0.18; slips 0.015, 0.09 | correct | 12 × 0.015 |
| q[1] | Cov = −2; slips 2, 0, 3.75 | correct | −20 × 0.25 × 0.4 |
| q[2] | P(T = 4) = 3/16 | imprecise | key needs independent trials; prompt says only "Each trial succeeds with chance 0.5"; finding 4 |
| q[2] slips | 0.375, 0.0625 | correct | 6/16, 1/16 |
| q[3] | r = 1 is the geometric | correct | as s[9] |

## review-4.json

| path | claim | verdict | basis |
|---|---|---|---|
| i[0] | P(Y = 1) = 0.45; slips 0.25, 0.40 | correct | column sum |
| i[1] | P(+1% given strong) = 0.625; options 0.25, 0.556, 0.45 | correct | 0.25/0.40; 0.25/0.45 |
| i[2] | four cells differ, first column matches | correct | products 0.20, 0.12, 0.08, 0.30, 0.18, 0.12 |
| i[2].explain | dependent though the first column looks independent | correct | one failing cell suffices |
| i[3] key | X in {−2, −1, 1, 2}, Y = X²: Cov 0 and dependent | correct | E[X³] = 0; P(X = 1, Y = 4) = 0 against 1/8 |
| i[3] option pos why | Y grows with abs X, not X | correct | even function |
| i[4] | E[Y given strong] = 0.5; slips 0.2, 0.25 | correct | 0.20/0.40 |
| i[5] | E[Y] = 0.25 with E[Y given weak] = 1/12; slips 0.2917, 0.0417 | correct | 0.05/0.60 = 1/12 |
| i[6] | first tail at chance 0.4: 2.5 tosses; slips 1.5, 0.4, 1.667 | correct | 1/0.4; tosses of a coin are independent |
| i[7] | best forecast under squared error is the conditional mean 0.5% | correct | as l15 s[4] |
| i[7] option zero why | 0% is the middle value, not the average | correct | values −1, 0, 1 |

## homework-4.json

| path | claim | verdict | basis |
|---|---|---|---|
| i[0] | 0.9, 0.6, 0.3, 2/21 | correct | recomputed |
| i[0].explain | most volume earns the tighter spreads | correct | 0.57/0.63 of fills at 1 or 2 ticks |
| i[1] | c = 0.18; slips 0.12, 0.3 | correct | 0.6 × 0.3; rows proportional with factor 1.5 |
| i[2] a | independence gives Cov = 0 | correct | BH 7.3 |
| i[2] b | Cov = 0 does not give independence | correct | Y = X² |
| i[2] c | independence gives flat conditional mean | correct | l15 |
| i[2] d | flat conditional mean does not give independence | correct | vol-regime table |
| i[2] e | same margins do not give the same table | correct | A, B against C, D |
| i[2].explain | "Margins never fix the cells" | imprecise | if one variable is constant the margins fix every cell; finding 18 |
| i[3] key | E[B given A = a] = 0 for every a, yet dependent | correct | each row symmetric about 0 |
| i[3] option sq why | E[B² given A] is 9 or 1 | correct | script |
| i[4] | E[M] = (1 − p)/p; slips 1/p, p/(1 − p) | correct | first-step equation |
| i[5] | head then tail: 4 tosses; slips 6, 2, 3 | correct | E_H = 2, E = 2 + E/2; script MC |
| i[5].explain | a failed attempt keeps the head | correct | state after HH is still "just after a head" |
| i[6] lines | law of total expectation from the joint pmf | correct | finite sums swapped; every P(X = x) > 0 stated |
| i[7] | −£85; slips −266.67, 140 | correct | 200 − 60 − 225 |
| i[8].model part 1 | E[N] = 1/p, with finiteness noted | correct | Ross 7.5 |
| i[8].model part 2 | two sixes in a row: 42 rolls, b = 36 | correct | a/36 = 7/6; script MC |

## review-5.json

| path | claim | verdict | basis |
|---|---|---|---|
| i[0] | 125; slips 25, 100, 150 | correct | 25 + 100 |
| i[1] | Var(S) = 105; slips 24, 144, 90 | correct | 24 + 81 |
| i[2] | E[1/X] larger for positive non-constant X; equality needs X constant | correct | 1/x strictly convex on x > 0 |
| i[3] | 0.1296; slips 0.00648, 0.0648 | correct | 20 × 0.00648 |
| i[4] | sd of E[Y given X] is √5; slips 5, 2, 3 | correct | 9 − 4 |
| i[5] | μ − σ²/2 = 0.92%; exact 0.9165%; slips | correct | script; mean 1%, sd 4% of the ±model |
| i[6] | 2,400; slips 2,000, 40,000, 49 | correct | E[N] = 20, Var(N) = 100 |
| i[7] | Var(T) = 40; slips 20, 8, 10 | correct | 2 × 0.8/0.04 |
| i[8] | geometric count mean 4, variance 12; total fee variance 128 | correct | 0.75/0.0625; fees independent of N stated |
| i[8].explain | the count's term dominates because a geometric count has a large variance | correct | 108 against 20 |
| i[9] | e^X, ln, x² hold; 1/x and root options reversed | correct | X positive, non-constant |

## homework-5.json

| path | claim | verdict | basis |
|---|---|---|---|
| i[0] | Var(Y) = 15; slips 12, 3, 20; overall mean 0 | correct | 12 + 3 |
| i[1] lines | Cov = −n p_i p_j and ρ = −√(p_i p_j / ((1 − p_i)(1 − p_j))) | correct | BH 7.4.6; n cancels |
| i[2] | Var(S) = 3,630; sd £60.25; slips | correct | 750 + 2,880 |
| i[3] slots | ln: ≤; abs: ≥; fourth power: ≥; E[XY] against √(E[X²]E[Y²]): ≤ | correct | concave, convex, convex, Cauchy–Schwarz |
| i[4] | ρ = −0.599; slips −7, 0.599, 0 | correct | −7/√(12 × 11.375) |
| i[5] | E[T given exactly one win in four] = 9; slips 7.5, 6.5, 11.5 | correct | future trials independent of the past; script MC |
| i[6] code | `book_sim` and `book_exact`; Var(N) = 400p(1 − p) | correct | script runs solution: seeds give (120.21, 22822.56) and (99.66, 18248.28) |
| i[6] code | population variance of daily P&L | correct | consistent with l18 |
| i[7].model step 1 | 1.012^120 = 4.18 is the mean wealth under independence | correct | expectation of a product of independent factors |
| i[7].model step 2 | typical (median) wealth is e^(120 E[ln(1 + R)]), below the mean | correct | median of log wealth is near its mean for a sum of 120 terms; l19 MC in script shows the same |
| i[7].model steps 3, 4 | 0.955% a month; e^1.146 = 3.1; about a quarter lower | correct | script |
| i[7].model step 5 | "The mixture has fatter tails than either regime" | imprecise | as l17 s[10]; finding 5 |
| i[7].model caveat | approximation and independence are assumptions | correct | stated |
| i[8] | Var(S) = mb + va²; slips | correct | the formula |

## problems-4.json

| path | claim | verdict | basis |
|---|---|---|---|
| i[0].p[0] | P(Y = 1) = 0.38; slips 0.18, 0.20, 0.19 | correct | column sum |
| i[0].p[1] | P(Y = 2 given X = 2) = 0.2; slips 0.08, 0.57, 0.13 | correct | 0.08/0.40; 0.08/0.14; 0.08/0.60 |
| i[0].p[2] | dependent: 0.36 against 0.288 | correct | one failing cell |
| i[0].p[2] option cov why | zero covariance would not prove independence anyway | correct | l14 |
| i[0].p[3] | E[Y given X = 2] = 0.9; slips 0.36, 0.5, 1 | correct | 0.36/0.40 |
| i[0].p[4] | £3.96; slips 4.2, 8.4, 5.4, 2.66 | correct | 6 × 0.66; carried slip 6 × 0.444 |
| i[1].p[0] | 0.09; slips 0.6, 0.3 | correct | independence stated |
| i[1].p[1] | P(S = 2) = 0.23; slips 0.14, 0.09, 0.74 | correct | 0.14 + 0.09 |
| i[1].p[2] | E[X given S = 2] = 0.37/0.23; slips 0.37, 0.7, 1.5 | correct | recomputed |
| i[1].p[3] | seeing S changes Y's chances though X ⊥ Y | correct | P(Y = 1 given S = 2) = 9/23 against 0.3 |
| i[1].p[3] option small why | any total that depends on Y moves its chances | correct | Cov(Y, X + Y) = Var(Y) > 0 |
| i[1].p[4] | E[Y given S = 2] = 0.3913 by linearity; slips | correct | 9/23; conditional expectation is linear |
| i[2].p[0] | P(young given 2 claims) = 3/7; slips 0.03, 0.15, 0.2 | correct | 0.03/0.07 |
| i[2].p[1] | E[X given young] = 0.55; slips 0.11, 1, 0.25 | correct | 0.11/0.20 |
| i[2].p[2] | E[X] = 0.31; slips 0.4, 0.49, 0.22 | correct | 0.11 + 0.20; margin check 0.17 + 0.14 |
| i[2].p[3] | expected loss £480 on a young policy; slips | correct | 1,100 − 620 |
| i[2].p[4] | each older driver pays £120 above expected claims; slips 96, 480, 500 | correct | 620 − 500; 0.2 × 480 = 0.8 × 120 |
| i[3].p[0] | E[T given error first] = 2 + m | correct | tries independent, stated |
| i[3].p[1] | m = 4.2; slips 2.1, 2, 1.4, 3, 1 | correct | m = 2.1 + 0.5m; script MC |
| i[3].p[2] | E[T given first try fails] = 7.4; slips 3.7, 3.2, 7.7, 5.3 | correct | 3.2 + 4.2; check 0.5 + 0.5 × 7.4 = 4.2 |
| i[3].p[3] | backup mean 2.7857; new mean 3.4929; slips | correct | 1.95/0.7; 0.5 + 0.5 × 5.9857 |
| i[3].p[4] | m_B = 1.8 for a 3-second mean; slips 3, 2.8, −2.4 | correct | 3.2 + m_B = 5 |

## problems-5.json

| path | claim | verdict | basis |
|---|---|---|---|
| i[0].p[0] | E[N] = 31; slips 25, 19 | correct | 28 + 3 |
| i[0].p[1] | Var(N) = 220; slips 31, 189, 43.6, 256 | correct | 31 + 189 |
| i[0].p[2] | E[S] = 46.5 kg; slips 15.5, 60, 37.5 | correct | weights independent of N, stated |
| i[0].p[3] | Var(S) = 502.75; slips 7.75, 337.75, 510.5, 77.5 | correct | 7.75 + 495; script MC |
| i[0].p[3].explain | "Eve's law gives ..." | imprecise | name undefined in the course; finding 7 |
| i[0].p[4] | count's share 0.9846; slips 0.0154, 0.9771, 0.8458 | correct | 495/502.75 |
| i[0].p[4].explain | most of that comes from the weather | correct | 189 of 220 |
| i[1].p[0] | E[V] = 42.5; slips 43.3, 40 | correct | recomputed |
| i[1].p[1] | planned time 16.94 minutes; slips 0.28, 16.62 | correct | 720/42.5 |
| i[1].p[2] | E[T] = 18 minutes | correct | 6 + 9 + 3 |
| i[1].p[3] | 1/v convex so E[12/V] ≥ 12/E[V]; they agree only when V is fixed | correct | strict convexity on v > 0 |
| i[1].p[4] | P(four flights need more than 80 minutes) = 37/256; slips 0.2617, 0.3633, 0.0938 | correct | script exact enumeration |
| i[2].p[0] | P(T = 5) on line A = 0.02916; slips 0.0729, 0.0073 | correct | 4 × 0.01 × 0.729 |
| i[2].p[1] | E[T] = 16; pooled 14.29 is wrong because r/p is not linear in p | correct | 12 + 4; Jensen direction consistent (14.29 < 16) |
| i[2].p[2] | E[Var(T given line)] = 124; slips 140, 110, 62 | correct | 108 + 16 |
| i[2].p[3] | Var(T) = 148; slips 124, 24, 128.8 | correct | 124 + 24 |
| i[2].p[3].explain | "Eve's law: ..." | imprecise | name undefined; the formula is written out beside it; finding 7 |
| i[2].p[4] | share 24/148 = 0.1622; slips | correct | recomputed |
| i[2].p[4].explain | a tester who knew the line faces 180 or 40 | correct | conditional variances |
| i[3].p[0] | E[ln R] = ½ ln 0.9 = −0.0527; slips 0.0488, 0.05, −0.0229 | correct | script |
| i[3].p[1] | E[ln W] = −0.2108 | correct | exact 2 ln 0.9 = −0.2107; key uses the rounded input and the band 0.0005 takes both |
| i[3].p[2] | Var(ln W) = 0.8452; Var(ln R) = 0.2099; Var(N) = 2 | correct | exact 0.84514; band 0.0005 takes both |
| i[3].p[2] slip count-squared | 3.3612 for E[N]² Var(ln R) + count term | correct | 16 × 0.2099 + 0.0056 = 3.3640, inside the slip's band of 0.0035 |
| i[3].p[3] | both E[W] = 1.2184 and E[ln W] < 0 hold by Jensen | correct | E[1.05^N] = 1.2184 (script); ln 1.2184 = 0.1975 |
| i[3].p[3] option equal why | equality only when W is fixed | correct | ln strictly concave |
| i[3].p[4] | P(W < 1) = 89/128; slips 0.3047, 0.6875, 0.6979 | correct | script exact |
| i[3].p[4].explain | W < 1 exactly when at most half the rounds are up | correct | for N = 2, 4, 6: threshold k < 0.5575N |

## Totals

371 rows: 343 correct, 3 wrong, 25 imprecise, 0 misleading, 0 unverified. The 28 non-correct rows map to findings 1 to 19 of `docs/reviews/audit-random-vars-4-5.md` (several rows share a finding).

# Claim ledger: random-vars levels 1 to 3, round 2 (blind)

Reader: Fable, blind to the round 1 audit, its ledger, its scripts and all earlier reviews until this file and the findings were committed. Stage 1, full ledger. Each row was judged by hand; "script" means the row is also recomputed in `docs/reports/random-vars-L1-3-concepts-r2.py`. Sources: Blitzstein and Hwang, *Introduction to Probability* (BH); Ross, *A First Course in Probability* (Ross); Casella and Berger, *Statistical Inference* (CB); McNeil, Frey and Embrechts, *Quantitative Risk Management* (MFE); Hull, *Options, Futures and Other Derivatives* (Hull); Bodie, Kane and Marcus, *Investments* (BKM).

Verdict counts are at the foot. Files are under `app/content/courses/random-vars/`.

## l1-number-per-outcome

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget.answer | Four cells total 9 | correct | (3,6),(4,5),(5,4),(6,3); script |
| screens[0].feedback.byKey (13 cell lines) | Each named pair's total, and "swapping the dice gives a different cell" | correct | each sum checked by hand: 8, 8, 8, 10, 8, 10, 8, 10 for the wrong cells |
| screens[1].widget.answer, wrong[] | Larger die 4 is an L of 7 cells; cross (11), row-only (4), square (16) are slips | correct | max(a,b)=4 needs both ≤ 4 and one = 4: 16 − 9 = 7; script |
| screens[1].feedback.byKey (24 lines) | Larger die of each named pair | correct | each checked: e.g. (4,6) is 6, (2,3) is 3 |
| screens[2].prose | A rule giving every outcome a number is a random variable | correct | BH 3.1, definition 3.1.1 (function on the sample space) |
| screens[2].widget.options | {X = 9} is an event, not 9, not 4/36, not one outcome | correct | BH 3.1: {X = x} is the set of outcomes s with X(s) = x |
| screens[3].widget | D = 1 on 10 cells; slips 5, 6, 12 | correct | two off-diagonals of 5; script |
| screens[3].explain.text | D takes the values 0 to 5 | correct | |a − b| ranges 0..5 |
| screens[4].widget.options | Indicator, constant and signed difference are random variables; a probability and an event are not | correct | BH 3.1; a constant is a degenerate r.v. |
| screens[4].feedback.byKey.signed | A random variable may be negative | correct | definition places no sign restriction |
| screens[5].widget | P(Y = 6) = 11/36; slips 1/6, 6/36, 12/36 | correct | 6 + 6 − 1; script |
| screens[5].explain.text | P(Y = 1) = 1/36; "a value is as likely as the outcomes behind it" | correct | only (1,1); pmf as sum over outcomes |
| screens[6].prose | P(X = x) = Σ P(ω) over ω with X(ω) = x; a count over 36 here | correct | BH 3.2 (discrete sample space) |
| screens[6].widget.options | {X = 3} = {(1,2),(2,1)}; the three slips | correct | enumeration |
| screens[7].widget.rows | Call payoff max(S − 100, 0): 0, 0, 0, 3, 6 | correct | Hull, chapter on option mechanics (payoff of a long call); arithmetic |
| screens[7].explain.text | C is a random variable; {C = 0} has three outcomes | correct | 94, 97, 100 |
| screens[8].widget | N = 2 on FFM, FMF, MFF; at-least and first-two slips | correct | enumeration of 8 paths |
| screens[8].feedback.byKey (5 lines) | Fill count of each named path | correct | checked each |
| summary.ideas, formula, trap | Three ideas, pmf sum, 11/36 not 1/6 | correct | as rows above |
| quiz[0] | {Y = 2} = {(1,2),(2,1),(2,2)}; slips | correct | enumeration |
| quiz[1] | P(total ≥ 10) = 6/36; slips 1/2, 3/36, 3/11; "an indicator's chance of 1 is the chance of its event" | correct | 3 + 2 + 1; script |
| quiz[2] | L = 200M is −200 at M = −1; values −200, 0, 400 | correct | arithmetic |
| quiz[3] | First minus second die takes 11 values; slips 6, 36, 10 | correct | −5..5; script |

## l2-listing-chances

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget.rows, feedback.byKey | p(2..7) = 1/36..6/36 with the listed cells | correct | diagonal counts; script |
| screens[0].explain.text | Chances climb 1/36 a step to 7, then shrink | correct | triangle pmf of two dice (Ross 4.1 ex.) |
| screens[1].canvas.params.exact | Eleven exact heights | correct | 1..6..1 over 36 to 4 dp |
| screens[1].widget.options | 9 matches 5 (four cells each); 6 and 8 have five, 10 has three | correct | symmetry about 7 |
| screens[2].prose | Definition of pmf, p(x) = P(X = x) | correct | BH section 3.2 |
| screens[2].widget, feedback | Sum is 1; slips 21/36, 11, 36 | correct | script |
| screens[2].explain.text | Every pmf adds to 1 because X always takes some value | correct | BH section 3.2 |
| screens[3].widget, explain | p(6) = 0.5; a pmf need only be non-negative and add to 1 | correct | BH section 3.2 (valid pmf conditions) |
| screens[3].feedback.byKey.over | Sum above 1 counts chance that does not exist | correct | axiom P(S) = 1 |
| screens[4].widget.rows | Three tosses: 1/8, 3/8, 3/8, 1/8 | correct | C(3,k)/8 |
| screens[5].widget, explain | Heads plus tails is 3 on every outcome, P(S = 3) = 1; a point mass is still a pmf | correct | degenerate distribution |
| screens[6].widget, explain | 25/36, 11/36, 1/36 adds to 37/36; exactly one six is 10 cells | correct | script (25, 10, 1) |
| screens[6].widget.options[2].why | "A pmf can be lopsided; it just has to add to 1" | correct | non-negativity is given in context (all entries shown positive) |
| screens[7].prose | p ≥ 0, Σp = 1, P(X ∈ A) = Σ_{x∈A} p(x) | correct | BH 3.2 |
| screens[7].widget | P(X ≥ 10) = 1/6; slips 3/36, 3/11 | correct | script |
| screens[8].prose | Days independent (stated) | correct | needed for the products; stated |
| screens[8].widget.rows, feedback.byKey | Two-day pmf 0.04, 0.20, 0.37, 0.30, 0.09 with the listed paths | correct | script |
| summary.ideas[1] | A pmf is never negative and adds to 1; if not, an outcome was missed or double-counted | correct | as above; second sentence is diagnostic advice |
| summary.formula.note | Unlisted values have p(x) = 0 | correct | support convention |
| quiz[0] | Two tosses: 1/4, 1/2, 1/4; three slips | correct | enumeration |
| quiz[1] | p(4) = 0.3, P(X ≥ 2) = 0.8; slips 0.5, 0.3, 0.7 | correct | arithmetic |
| quiz[2] | P(max = 3) = 5/36; slips 1/6, 6/36, 9/36 | correct | 9 − 4; script |
| quiz[3] | P(Z = 0) = 0.7 | correct | 0.5 + 0.2 |

## l3-up-to-a-point

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget | P(X ≤ 1) = 1/2; slips 0.375, 0.125, 0.875 | correct | 1/8 + 3/8 |
| screens[1].canvas.derive | Step heights 0, 1/8, 4/8, 7/8, 1 with the value included at the jump | correct | right-continuity of F (BH section 3.6) |
| screens[1].widget.options | F jumps only at 0, 1, 2, 3 | correct | BH 3.6: jumps at support points |
| screens[1].explain.text | At x = 2 the height is already 7/8 | correct | F(x) = P(X ≤ x) |
| screens[2].prose | F(x) = P(X ≤ x); closed dot on the upper step | correct | CB def. 1.5.1; convention stated where it first matters |
| screens[2].widget | F(2.4) = 7/8; slips 0.375, 0.5, 0 | correct | F flat between support points |
| screens[3].widget | P(1 < X ≤ 3) = F(3) − F(1) = 1/2; slips 0.875, 1, 0.375 | correct | BH section 3.6 consequence; arithmetic |
| screens[4].widget | P(X > 2) = 1 − F(2) = 1/8; slips 0.875, 0.5 = P(X ≥ 2) | correct | complement |
| screens[5].widget, feedback.byKey (36 lines) | {Y ≤ 4} is the 4 by 4 square; each cell line | correct | max ≤ 4 iff both ≤ 4; each line checked against the rule |
| screens[5].explain.text | F(y) = y²/36 for y = 1..6 | correct | script |
| screens[6].widget | Jump at 4 is 7/36; slips 16/36, 1/6, 9/36 | correct | script |
| screens[6].explain.text | Every jump of a CDF is a bar of the pmf | correct | P(X = x) = F(x) − F(x−) |
| screens[7].widget.options | P(2 ≤ Y ≤ 4) = F(4) − F(1) = 15/36; F(4) − F(2) = 12/36 drops Y = 2 (3/36) | correct | script |
| screens[8].widget.lines | Proof of P(a < X ≤ b) = F(b) − F(a) for a < b | correct | disjoint union and additivity (CB thm 1.5.3 route) |
| screens[9].widget.rows | Running totals 0.30 .. 1.00 | correct | arithmetic |
| screens[9].feedback.byKey.r6c2 | The last value of a CDF is always 1 | correct | finite support: F at the largest value is 1 |
| screens[10].prose | 95% VaR is the smallest x with F(x) ≥ 0.95; on at least 95% of days the loss is at most this | correct | MFE section 2.2 (VaR as the generalised inverse of F_L) |
| screens[10].widget | VaR = 5; slips 2, 10, 20 | correct | script |
| screens[10].feedback.byKey.worst | VaR is exceeded on at most 5% of days and says nothing about how far | correct | P(L > VaR) ≤ 1 − α; MFE 2.2.2 remark on tail blindness |
| screens[10].explain.text | For a discrete loss the quantile sits on a jump | correct | smallest x with F(x) ≥ α is a point of increase |
| summary.ideas | Staircase from 0 to 1, jumps p(x); P(a < X ≤ b) = F(b) − F(a); P(X > x) = 1 − F(x) | correct | as rows above |
| summary.trap | Subtract F(1), not F(2), for P(2 ≤ Y ≤ 4) | correct | integer support |
| quiz[0] | 0.2, 0.5, 1 could be a CDF; the three others cannot | correct | monotone, ends at 1, X takes all three values |
| quiz[0].explain.text | Never decreases, 1 past the largest value, 0 far left | correct | CB thm 1.5.3 |
| quiz[1] | P(X = 2) = 0.5; slips | correct | jump |
| quiz[2] | P(X < 2) = F(1) = 0.2; differs from P(X ≤ 2) by P(X = 2) | correct | identity true for any X |
| quiz[3] | P(L > 2) = 0.10; slips 0.9, 0.25 = P(L ≥ 2), 0.04 | correct | script |

## l4-transforming

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget, feedback.byKey (24 lines) | (X − 7)² = 1 on totals 6 and 8, ten cells; each cell line | correct | script; lines checked |
| screens[1].canvas.derive | P(max(X − K, 0) = 0) = P(X ≤ K) by the closed forms; other bars P(X = K + j) | correct | script, K = 2..12 |
| screens[1].widget, explain | K = 10: totals 2 to 10 pay 0, chance 33/36 | correct | 1 − 3/36 |
| screens[2].widget.rows | pmf of (X − 7)²: 6, 10, 8, 6, 4, 2 over 36 | correct | script |
| screens[2].explain.text | Grouping by y gives the distribution of g(X) | correct | BH section 3.7 (pmf of g(X)) |
| screens[3].widget.rows | pmf of |X|: 0.37, 0.50, 0.13 | correct | arithmetic |
| screens[4].widget.options | S = 100 + X keeps the five chances; one-to-one g only relabels | correct | BH 3.7 (one-to-one case) |
| screens[5].widget.options | P(X² = 1) = 0.3; slips 0.1, 0.01, 0.2; full pmf 0.3, 0.3, 0.4 | correct | arithmetic |
| screens[6].prose | P(g(X) = y) = Σ_{x: g(x) = y} p_X(x) | correct | BH section 3.7 |
| screens[6].widget.options | P((X − 7)² = 4) = 8/36; slips 4/36, 3/36, 16/36 | correct | totals 5 and 9 |
| screens[7].widget.rows | Call payoff pmf 0.61, 0.30, 0.09 | correct | script |
| screens[7].explain.text | The call pays something with chance only 0.39 | correct | 0.30 + 0.09; a chance, not a count of paths |
| screens[8].widget | P(L = −1000) = 0.09 for L = −250X; slips 0.04, 0.13 | correct | script |
| screens[8].explain.text | x ↦ −250x is one-to-one and reverses order | correct | strictly decreasing |
| summary | Three ideas, formula, "apply g to the values, never to the probabilities" | correct | as above |
| quiz[0..3] | 0.5; 0.5 (Y = 3X + 1); 33/36; 0.13, with their slips | correct | arithmetic and enumeration |

## l5-long-run-average

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[1].widget, feedback | Beam balances at 1.5; pivot at 1 tips right, at 2 tips left | correct | torque about 1: (3/8)(1) + (1/8)(2) > (1/8)(1) |
| screens[1].explain.text | A balance point need not be a value X can take | correct | E[X] = 1.5 |
| screens[2].canvas.params.series | Running average: 4.5 after 10 rolls, 3.503 after 1,000 | correct | script reads the series |
| screens[2].widget.options | The average settles near 3.5; not 3, not "never", not the leading face | correct | strong law of large numbers (BH section 10.2) |
| screens[2].explain.text | After 1,000 rolls a new roll moves the average by less than 0.003 | correct | at most 2.5/1001 = 0.0025; script |
| screens[3].prose | Balance point and long-run average are the same number, E[X] | correct | centre of mass = Σ x p(x); LLN |
| screens[3].widget | Σ k/6 = 3.5; slips 21, 1 | correct | arithmetic |
| screens[4].widget | Loaded die mean 4.5; slips 3.5, 6 | correct | script |
| screens[5].widget, explain | E[I] = 1/6; an indicator's mean is its event's chance | correct | BH section 4.4 (fundamental bridge) |
| screens[6].widget.options | Sixes in two rolls: E = 1/3; slips 1, 0, 10/36 | correct | script |
| screens[6].explain.text | Plain average of 2..12 equals 7 because the pmf is symmetric | correct | symmetric pmf about 7 has mean 7 |
| screens[7].prose | "For any discrete random variable X, E[X] = Σ x P(X = x)" | imprecise | finding 3: true as stated only when the sum converges absolutely (BH section 4.1; Ross 4.3); homework-2 items[4] itself meets the divergent St Petersburg sum |
| screens[7].widget.options | (−1)(0.8) + 4(0.2) is E[X]; three slips | correct | definition |
| screens[8].widget.solution | sum(x * p) is the definition; simulate draws with the pmf weights | correct | code read; method is the definition |
| screens[8].widget.examples[1], explain | The seeded 100,000 draws print 3.50167 | correct | script reproduces 3.50167 with `random.Random(1)` |
| screens[8].explain.text | "More draws shrink that gap" | imprecise | finding 2: true of the typical gap (RMS ∝ 1/√n, script MC), not draw by draw; same seed gives gap 0.00167 at 100,000 and 0.00325 at 200,000 (script note) |
| screens[9].widget | Expected P&L £0.20; slips 0, 0.6, 1.0 | correct | 0.6 − 0.4 |
| screens[9].explain.text | Over 250 days the expected total is £50 | correct | linearity, 250 × 0.2 |
| summary.ideas, trap | Balance point; weigh by chance; constant and indicator cases; unweighted average agrees only in special cases | correct | as above |
| quiz[0] | A constant is its own expected value | correct | E[c] = c |
| quiz[1] | E[N] = 1.2; slips 1.5, 1 | correct | arithmetic |
| quiz[2] | After ten tails the next toss is heads with chance 0.5; the run is diluted, not corrected | correct | independence of tosses; script MC (0.5 after a run) |
| quiz[3] | E[X] = 1.9; slips 5.5, 1 | correct | arithmetic |

## l6-fair-price

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget, explain | £10 on a 7 returns 10/6 ≈ £1.67 on average; £2 loses about 33p | correct | P(7) = 6/36 |
| screens[1].canvas, explain | Seeded 1,000 tickets return about £1.67 | correct | script reproduces the engine RNG: 167 sevens |
| screens[1].widget.options | Break-even near £1.67; slips £5, £10, £0.28 | correct | 10 × 1/36 = 0.28 |
| screens[2].prose | The fair price is the price with zero average profit, the expected payoff | correct | Ross 4.3 (fair game); stated as a definition |
| screens[2].widget | 10/6; slips 0.2778, 5, 10 | correct | script |
| screens[3].widget, explain | Expected profit −1/3; buyer favoured only when price < E[payoff] | correct | E[X − c] = E[X] − c |
| screens[4].widget | 12(6/36) + 6(2/36) = 7/3; slips 18, 2, 9, 2.1667 | correct | script |
| screens[5].widget, explain | Fair coin bet: expected profit 0; fair is not good, only risk | correct | definition; risk-aversion remark is standard |
| screens[6].widget.options | Crash contract fair price £5; slips £0, £100, £50 | correct | 100 × 0.05 |
| screens[7].prose, widget | E[profit] = E[payoff] − price; 4 − 4.50 = −0.50 favours the seller | correct | linearity |
| screens[8].widget.lines | Derivation of E[X − c] = E[X] − c | correct | split the sum; Σ p = 1 |
| screens[9].prose | Two-day tree; each day up 0.4, flat 0.4, down 0.2 | imprecise | finding 4: the key multiplies 0.4 × 0.4, which needs the days independent; the prose does not say so (the tree's repeated branch labels imply it) |
| screens[9].widget | Binary pays above £102: fair price £16; slips 48, 32, 100, 64 | correct | script (given independence) |
| screens[9].explain.text | Desks price by expectation under risk-neutral probabilities read off market prices | correct | Hull, chapter on binomial trees (risk-neutral valuation); discounting omitted at zero rate is harmless here |
| screens[10].widget, explain | Tickets cost 1.07 and pay 1: sure loss 7p, the overround; fair prices of exhaustive exclusive results add to 1 | correct | Σ P = 1; script |
| summary | Fair price, expected profit, fair not good | correct | as above |
| quiz[0] | Lottery expected profit −0.5; slips 1.5, 0.5, −1 | correct | script |
| quiz[1] | 20/36 − 3 ≈ −2.44; slips | correct | script |
| quiz[2] | Only B is favourable (0.95 > 0.90; 1.80 < 2) | correct | arithmetic |
| quiz[3] | Zero expected profit: fair; average per bet settles near 0 over many bets | correct | LLN for repeated independent bets |

## l7-linearity

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget, explain | Row 1 averages 4.5; row k averages k + 3.5 | correct | script |
| screens[1].widget.options, explain | X + Y and X + X have different shapes and both average 7 | correct | 2 × 3.5; script reproduces the seeded averages 7.00 and 6.99 |
| screens[2].widget | E[X + Y] = 7; slips 3.5, 42 | correct | average of row averages (rows equally likely) |
| screens[2].explain.text | Rows averaged k + 3.5 because the dice are independent; the rule holds without that | correct | E[Y given X = k] = 3.5 uses independence; linearity itself does not (BH section 4.2) |
| screens[3].widget, explain | E[X + X] = 7; X with itself is as dependent as can be | correct | diagonal 2..12 averages 7 |
| screens[4].widget | E[X − Y] = 0; slip 70/36 = E|X − Y| | correct | script |
| screens[5].widget | E[3X − 5] = 5.5; slips 10.5, −1.5, −4.5 | correct | script |
| screens[6].widget.options | E[X²] = 91/6; slips 12.25, 7, 91/36 | correct | script |
| screens[6].feedback.byKey.squared | "That product rule fails here, because X depends completely on itself" | imprecise | finding 9: dependence is necessary, not sufficient, for failure; the course's own X, X² pair (l11) is fully dependent yet E[XY] = E[X]E[Y]. It fails here because Var(X) > 0 |
| screens[6].explain.text | E[XY] = E[X]E[Y] can fail without independence; E[g(X)] ≠ g(E[X]) in general; for an upward-bending g the average of g beats g of the average | correct | Jensen (BH section 10.1), strict for non-constant X and strictly convex g |
| screens[7].prose | E[X + Y] = E[X] + E[Y] and E[aX + b] = aE[X] + b need no independence | correct | BH section 4.2 |
| screens[7].widget.options | Sum, affine and difference rules hold for any X, Y; product and square rules do not | correct | counterexample Y = X on a die |
| screens[7].widget.options[3].why | Product rule holds for independent variables, can fail otherwise | correct | sufficient, not necessary: wording is right |
| screens[8].widget.lines | Proof of linearity from the joint table | correct | BH section 4.2 (discrete case) |
| screens[8].feedback.correct | No line multiplies two chances, so independence is never used | correct | inspection of the proof |
| screens[9].widget.options | Desk expects £70; the joint table is needed for spread, not the mean | correct | 80 − 10; script (two opposite couplings give 70) |
| screens[10].widget | 200 orders cost £900 on average; clustering changes risk, not this | correct | linearity; script |
| summary.ideas[2] | E[X²] ≠ E[X]² unless X is constant; E[XY] = E[X]E[Y] when independent | correct | Var(X) = 0 iff X constant (a.s.); product rule sufficient condition |
| summary.formula.note | For any X and Y with finite means | correct | hypothesis stated |
| quiz[0..1] | 10.5; 11 with slips | correct | arithmetic |
| quiz[2] | E[X·X] = 0.5 for a coin; product slip 0.25; "safe for independent variables, and X is not independent of itself" | correct | X non-constant |
| quiz[3] | £180 whatever the link | correct | linearity |

## l8-indicators

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget, explain | Three sixes at rolls 2, 5, 8; a count is a sum of 0s and 1s | correct | read the row |
| screens[1].widget.options | Average sixes in ten rolls settles near 1.67; 1 is the most common count | correct | 10/6; mode of Bin(10, 1/6) is 1 (script); seeded run 1.662 (script) |
| screens[2].prose | Definition of an indicator; N = I₁ + … + I₁₀ | correct | BH sections 3.1 and 4.4 (indicator random variables) |
| screens[2].widget | E[N] = 10/6; slips 1/6, 1, 10 | correct | linearity |
| screens[2].explain.text | The pmf of N was never needed | correct | linearity uses marginals only |
| screens[3].widget | Five traders, own cards: E[N] = 1; slips 0.2, 1/120, 5 | correct | script, exact over 120 permutations |
| screens[3].explain.text | Indicators dependent (four matches force the fifth); answer 1 for any n | correct | script: exactly four matches impossible |
| screens[4].widget, explain | Certain events: E[M] = 10; expected count lies between 0 and the number of events | correct | 0 ≤ P(A_k) ≤ 1 |
| screens[5].prose | 23 people, "birthdays spread evenly over 365 days" | imprecise | finding 6: a pair shares with chance 1/365 only if the two birthdays are independent as well as uniform; independence is not stated |
| screens[5].widget | Expected sharing pairs 253/365 ≈ 0.693; slips 0.063, 1.386, 0.5073 | correct | script (exact and MC) |
| screens[5].explain.text | Pair indicators are dependent (Ann-Bo and Bo-Cai force Ann-Cai) | correct | transitivity; jointly dependent though pairwise independent |
| screens[6].widget.options | Shuffled deck: one match expected; the distribution is not needed; dependence does not block adding | correct | script MC, n = 52 |
| screens[7].prose | E[N] = Σ P(A_k) for dependent events too | correct | BH 4.4 |
| screens[7].widget.options | E[I_k] = 1·P(A_k) + 0; independence plays no part | correct | definition |
| screens[8].widget.lines | Four-line derivation of the expected count | correct | linearity then the indicator pmf |
| screens[9].widget | Expected fills 4.65; slips 5, 0.465, 10 | correct | script |
| screens[9].explain.text | Clustering makes 0 or 10 fills more likely than under independence | correct | script: nested fills give 0.2 against 0.0011 + 0.00004 |
| screens[10].widget.options | 50 loans at 0.04: 2 expected defaults whatever the correlation | correct | linearity |
| screens[10].explain.text | Correlation decides the frequency of bad years | correct | variance of the count depends on covariances |
| summary | Three ideas, formula, trap | correct | as above |
| quiz[0..3] | 6; 5/13 aces (dependent draws); 132.5; 1 for 100 traders | correct | linearity; script for 5/13 |

## l9-measuring-spread

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget.options | ±£3 is riskier than ±£1 at the same mean | correct | larger spread about a common mean |
| screens[1].widget, feedback | E[X − μ] = 0 always; at size 2 the mean squared distance is 4; slips 0, 2 | correct | linearity; arithmetic |
| screens[2].prose | Var(X) = E[(X − μ)²], μ = E[X] | correct | BH section 4.6 |
| screens[2].widget | Variance 6 for {1: 0.5, 3: 0.25, 7: 0.25}; slips 0, 2, 15, 6.67, 3 | correct | script |
| screens[2].explain.text | The £7 outcome supplies two thirds of the variance | correct | 4 of 6 |
| screens[3].widget.rows | Die: squares 6.25, 2.25, 0.25; variance 35/12, sd 1.7078 | correct | script |
| screens[3].prose | The square root of the variance is the standard deviation | correct | BH section 4.6 |
| screens[3].explain.text | "A roll typically lands about 1.7 from 3.5" | correct | usual gloss of sd as root-mean-square distance; the lesson separates it from the mean distance on screens[5] and [8] |
| screens[4].widget.options, explain | A variance can be 0 or 2.5, never −1; it is 0 only for a constant | correct | BH section 4.6 |
| screens[5].widget | sd £2 for {−1: 0.8, 4: 0.2}; slips 0, 1.6, 4; variance is in £² | correct | script |
| screens[6].widget.lines | Var(X) = E[X²] − μ² | correct | BH section 4.6 |
| screens[7].widget.solution | Σ (x − μ)² p; the check divides by n | correct | definition; population formula applied to a simulated sample, no estimator claim made |
| screens[7].explain.text | The seeded run prints 2.9207 and converges to 35/12 as rolls grow | correct | script reproduces 2.9207; LLN for the second moment |
| screens[8].widget | A: sd £244.95; slips 60,000, 264.58, 240; B's sd £500, about twice A's | correct | script |
| screens[9].canvas, widget | Both trades: mean 0, sd 9.95; the sd misses which side the rare move is on; that is skew | correct | script; third moment sign (BH section 6.2) |
| summary | Square before averaging; shortcut; never negative; units | correct | as above |
| quiz[0..3] | 4; £4; 0; 13 − 9 = 4 with slips | correct | arithmetic |

## l10-scaling-and-adding

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget.options | Var(X + 10) = Var(X) | correct | BH section 4.6 |
| screens[1].canvas.derive, explain | sd of aX + b is |a| × 1.7078; a = 2 gives 3.416, a = −1 gives 1.708 | correct | sd(aX + b) = |a| sd(X) |
| screens[2].widget | Var(2X) = 35/3; slips 5.83, 2.92, 3.42 | correct | script |
| screens[3].widget | Var(−3X + 5) = 26.25; slips −26.25, 8.75, −8.75, 31.25 | correct | script |
| screens[4].prose | Two dice rolled independently (stated) | correct | hypothesis present |
| screens[4].widget | Var(T) = 35/6; slips 11.67, 2.92, 54.83, 1.94 | correct | script |
| screens[5].prose | The pmf of X − Y is the total's, slid to sit on 0 | correct | X − Y = X + (7 − Y) − 7 in distribution; script |
| screens[5].widget, explain | Var(X − Y) = 35/6; for independent variables the minus sign disappears | correct | Var(−Y) = Var(Y); additivity under independence |
| screens[6].widget.options | Var(X + X) = 4 Var(X), twice Var(X + Y); sds add only in lockstep | correct | sd(X + Y) = sd X + sd Y iff ρ = 1 (both sds positive) |
| screens[6].feedback.byKey.same | With a copy the extremes are six times as likely | correct | 1/6 against 1/36 |
| screens[7].widget.lines | Proof of Var(aX + b) = a² Var(X) | correct | BH section 4.6 |
| screens[8].prose | "For independent X and Y", Var(X + Y) = Var(X) + Var(Y) | correct | sufficient condition, stated as such (BH section 4.6) |
| screens[8].widget | sd first reaches £300 at n = 9; three days give 100√3 ≈ 173 | correct | script (exact and MC) |
| screens[8].explain.text | At 25 days the mean, £500, equals one sd | correct | 20 × 25 = 100 × 5 |
| screens[9].widget | Annual vol 1.2% × √252 = 19.05%; slips 302.4%, 22.93%, 1.2% | correct | script; 252-day convention stated in the prose |
| screens[9].explain.text | √252 rule holds for independent days of equal variance whose returns add; adding is exact for log returns | correct | Hull, chapter on the Black-Scholes-Merton model (volatility and the square root of time); conditions stated (uncorrelated would suffice, "holds for" is sufficient phrasing) |
| screens[10].widget | 2 × 400 × √10 = £2,529.82; four slips | correct | script |
| summary.ideas[2], formula.note, trap | Variances add for independent variables, also for a difference; never add sds of independent variables | correct | as above |
| quiz[0..3] | 36; 5; 8; 4% with slips | correct | arithmetic |

## l11-moving-together

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget, feedback | Same-direction corners 0.40, opposite 0.04: the assets move together | correct | read the table |
| screens[1].widget | Product positive only at both-down and both-up; zero where either is flat | correct | signs |
| screens[2].prose | Cov(X, Y) = E[(X − μ_X)(Y − μ_Y)] | correct | BH section 7.3 |
| screens[2].widget | Cov = 0.36; slips 0.40, 0.44, 0 | correct | script |
| screens[2].explain.text | Positive covariance: the two tend to sit on the same side of their means | correct | sign of the weighted product |
| screens[3].widget.rows | E[X] = 0.5, E[Y] = 1.4, E[XY] = 1.9, Cov = 1.2 | correct | script |
| screens[4].prose | ρ = Cov/(σ_X σ_Y), unit-free; σ_X = 1.5, σ_Y = 1.96 | correct | BH section 7.3; script |
| screens[4].widget | ρ = 1/√6 ≈ 0.408; slips 1.2, 0.139, 0.8 | correct | script |
| screens[4].explain.text | ρ always lies in [−1, 1]; the extremes mean an exact straight line | correct | Cauchy-Schwarz (BH section 7.3) |
| screens[5].canvas.derive | Dots y = ρx + √(1 − ρ²) z | correct | standard construction of correlation ρ with unit variances |
| screens[5].widget.options | At ρ = −0.8, B tends to be below its mean when A is well above | correct | E[Y given X] = ρX for the bivariate normal |
| screens[6].canvas (both clouds) | Left cloud has r = 0.8 and fitted slope 0.8; right has slope 2.4 | correct | script: sample r 0.8000, slopes 0.8000 and 2.4002 |
| screens[6].widget.options | ρ(X, 3Y) = 0.8; the slope triples, covariance triples, ρ cannot exceed 1 | correct | ρ invariant to positive scaling |
| screens[6].explain.text | Slope is Cov/Var(X); correlation measures tightness, not steepness | correct | OLS slope formula |
| screens[7].widget.options | X ∈ {−1, 0, 1} uniform, Y = X²: Cov = 0 yet dependent | correct | script; BH section 7.3 |
| screens[7].explain.text | Independence gives zero covariance, not the converse | correct | BH section 7.3 |
| screens[8].widget.lines | Proof of Cov = E[XY] − E[X]E[Y] | correct | BH 7.3 |
| screens[8].explain.text | Var(X) = Cov(X, X) | correct | definition |
| screens[9].widget | ρ = 0.78/1.5 = 0.52; slips 0.78, 0.347, 0.6 | correct | script |
| screens[9].explain.text | Many pairs of large stocks have daily correlations near this | correct | order of magnitude: average pairwise correlation of large US stocks is commonly 0.3 to 0.6 (Cboe implied correlation index range); "many pairs" is a weak claim |
| screens[10].prose | Hedge ratio β = Cov(X, Y)/Var(X): short £β of A per £1 of B | correct | minimum-variance hedge ratio, Hull, chapter on hedging with futures (h* = ρ σ_S/σ_F); script grid search |
| screens[10].widget | £156,000; slips 52,000, 300,000, 17,333 | correct | script |
| screens[10].feedback.byKey.vol | Ratio of sds is right only if ρ = 1; β = ρσ_Y/σ_X | correct | identity; script |
| screens[10].explain.text | Hedge cuts variance from 4.5 to 3.28; much of B's risk cannot be hedged with A | correct | Var(Y)(1 − ρ²); script |
| summary.trap | Positive scaling leaves ρ unchanged; a negative scale flips its sign | correct | Cov(aX, Y) = a Cov; sd(aX) = |a| sd |
| quiz[0..3] | 0.3; 0.6; 0.3 after 2Y + 0.01; negative sign | correct | arithmetic and invariance |

## l12-diversification

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| screens[0].widget, explain | 50:50 mix of two independent ±20% funds is less spread out | correct | mix is 0 half the time |
| screens[1].prose | Diversification: lowering risk by mixing assets not in lockstep | correct | BKM ch. 7 |
| screens[1].widget | sd √0.02 = 14.14%; slips 0.2, 0.1, 0.02 | correct | script |
| screens[2].canvas.derive | Var = w²σ_X² + (1 − w)²σ_Y² + 2w(1 − w)ρσ_Xσ_Y | correct | BKM ch. 7 (two-asset portfolio variance) |
| screens[2].widget.options, explain | At ρ = 1 with equal sds the curve is flat at 0.04; at ρ = −1 the 50:50 mix has variance 0 | correct | script |
| screens[3].widget | ρ = −1, sds 30% and 10%: riskless at w = 0.25 | correct | script |
| screens[4].widget | ρ = 0.8: lowest variance at w ≈ −0.27, sd 7.89%; any long X adds risk | correct | script (grid and formula) |
| screens[5].widget | 50:50, ρ = 0.2: sd 16.73%; slips 0.2, 0.158, 0.028, 0.163 | correct | script |
| screens[5].explain.text | "Below 1, the mix is always safer than the average" | imprecise | finding 1: true for weights strictly between 0 and 1 (script), false for the short weight taught one screen earlier (sd 7.89% against a weighted average of 4.6%) |
| screens[5].feedback.byKey.avg | Averaging sds is right only when ρ = 1 | correct | in this screen's 50:50 context |
| screens[6].widget.lines | Derivation of the two-asset variance | correct | expand the square; linearity |
| screens[6].explain.text | Diversification lives in the cross term, which shrinks as ρ falls | correct | for positive weights |
| screens[7].prose | w* = (σ_Y² − ρσ_Xσ_Y)/(σ_X² + σ_Y² − 2ρσ_Xσ_Y) from the derivative in w | correct | derived by hand: d/dw = 0; BKM ch. 7 (minimum-variance portfolio) |
| screens[7].prose (last sentence) | "Multivariable calculus, lesson 12, derived it with a Lagrange multiplier" | imprecise | finding 8: `multivar/l12-min-variance` solves a numeric case with a multiplier and derives the formula by substitution and one derivative ("The formula, from one derivative") |
| screens[7].widget | w* = 0.0075/0.055 ≈ 0.136; slips 0.864, 0.265 | correct | script |
| screens[7].explain.text | w* is positive while ρ < σ_Y/σ_X = 0.6 and negative above | correct | sign of the numerator; script |
| screens[8].prose | Equal weights, common σ and ρ: Var = σ²/n + (1 − 1/n)ρσ² | correct | (1/n²)(nσ² + n(n − 1)ρσ²); BKM ch. 7 |
| screens[8].widget | Limit sd √0.018 = 13.42%; slips 0, 0.018, 0.06, 0.1428 (n = 30) | correct | script (exact and MC at n = 30) |
| screens[8].explain.text | The sd never drops below 13.42%; shared risk cannot be diversified away | correct | Var = ρσ² + (1 − ρ)σ²/n > ρσ² |
| screens[9].widget | £11,522; slips 13,200, 11,063, 132,768,000 | correct | script |
| screens[10].widget | Index fund sd 16.47%; slips 1.34%, 30%, 0.0271 | correct | script |
| screens[10].explain.text | Near 16.5%, like real broad equity indices | correct | long-run annualised volatility of broad US indices is about 15 to 20% (BKM ch. 5 tables) |
| summary.ideas[1] | "Below ρ = 1 the mix is safer than the average of the sds" | imprecise | finding 1 (same hypothesis dropped) |
| summary.ideas[2], formula | Own risk falls like 1/n; floor ρσ²; formula and w* | correct | as above |
| summary.trap | Averaging the sds is right only at ρ = 1 | imprecise | finding 1 (long-only hypothesis; counted once) |
| quiz[0..3] | 7.07%; 20% at ρ = 1; 10% for four; ρ = −1 gives least risk at 50:50 with equal sds | correct | script formulae |

## review-1, review-2, review-3

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| review-1 items[0] | {N = 1} = {HTT, THT, TTH}; slips | correct | enumeration |
| review-1 items[1] | p(x) = cx on 1..4 gives c = 0.1; slips 0.25, 0.4 | correct | script |
| review-1 items[2] | P(1 ≤ X ≤ 2) = F(2) − F(0) = 0.7; slips 0.4, 0.8 | correct | arithmetic |
| review-1 items[3] | P(X² = 1) = 0.45; slips; P(Y = 4) = 0.25 | correct | arithmetic |
| review-1 items[4] | Independent fills (stated): P(N = 2) = 0.432; slips 0.144, 0.36, 0.648 | correct | script |
| review-1 items[5] | P(Y ≥ 5) = 20/36 = 1 − F(4); slips 11/36, 1/3, 9/36 | correct | script |
| review-1 items[6] | P(max(X − 9, 0) ≥ 2) = 3/36; slips 2/36, 6/36, 1/36 | correct | script |
| review-1 items[7] | 95% VaR = 6 | correct | script |
| review-2 items[0] | 4(0.55) − 3(0.45) = 0.85; slips 0.5, 2.2, 3.55 | correct | script |
| review-2 items[1] | Fair price 1.5; slips 9, 1, 4.5 | correct | arithmetic |
| review-2 items[2] | E[4X − 3] = 7; slips 10, −2 | correct | arithmetic |
| review-2 items[3] | 30 rolls: 5 sixes expected | correct | linearity |
| review-2 items[4] | E[X²] = 1.1, far from E[X]² = 0.01 | correct | arithmetic |
| review-2 items[5] | Seller's expected profit on 600 tickets is £200; slips | correct | script |
| review-2 items[6] | Independent dice: E[XY] = 12.25; 91/6 is E[X²] | correct | product rule under independence |
| review-2 items[7] | 13 cards: one ace expected; cards dependent | correct | 13 × 4/52 |
| review-2 items[8].prose | Two-day ±10% tree | imprecise | finding 5: independence of the two days is used (0.5 × 0.5) and not stated |
| review-2 items[8].widget | Call fair price 2.625; slips 5.25, 10.5 | correct | script (given independence) |
| review-2 items[9] | Doubles in 10 tosses: 9/4; slips 2.5, 4.5; neighbours dependent | correct | script, exact over 1,024 sequences |
| review-3 items[0] | Var = 4.75; slips 5, 1.75, 6.25 | correct | script |
| review-3 items[1] | Var(5 − 2X) = 12; slips −12, 6, −6, 37 | correct | arithmetic |
| review-3 items[2] | ρ = 0.6; slips 0.15, 0.4, 2.4 | correct | script |
| review-3 items[3] | sd √0.03 = 17.32%; slips | correct | script |
| review-3 items[4] | 16 independent days: £1,000 | correct | 250 × 4 |
| review-3 items[5] | Cov = 0 means only no straight-line tilt; dependence remains possible | correct | BH section 7.3 |
| review-3 items[6] | Variance 0.0004 gives sd 2%; three slips | correct | arithmetic |
| review-3 items[7] | Var(X − Y) = 4 + 9 − 6 = 7; slips 13, 19, −5 | correct | Var(X − Y) = Var X + Var Y − 2Cov |
| review-3 items[8] | Uncorrelated, sds 20% and 10%: w* = 0.2, sd 8.94% | correct | script |

## homework-1, homework-2, homework-3

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| homework-1 items[0] | P(min = 2) = 9/36; slips 1/6, 11/36, 25/36 | correct | script |
| homework-1 items[1] | Four tosses: 1, 4, 6, 4, 1 over 16 | correct | binomial coefficients |
| homework-1 items[2] | F_M(2) = 20/36; F_M(m) = 1 − ((6 − m)/6)² | correct | script |
| homework-1 items[3].widget.lines | CDF of the max by independence, pmf (2y − 1)/36 as the jump | correct | independence stated in line 2 |
| homework-1 items[4] | Three independent days (stated): call pays with chance 0.162; slips 0.135, 0.045, 0.441 | correct | script |
| homework-1 items[5] | VaR 4: F(4) = 0.95 meets "≥"; slip 8 | correct | MFE section 2.2; script |
| homework-1 items[6] | X mod 3 is uniform on 0, 1, 2; three slips | correct | script |
| homework-1 items[7].model, rubric | CDF y²/36, pmf (2y − 1)/36, Z pmf 16/36, 9/36, 11/36 | correct | script values |
| homework-1 items[8].widget.solution | Checks non-negativity and total 1 within 1e-9, then merges outcomes by value | correct | code read; teaches the definition of a pmf of g |
| homework-1 items[8].feedback.byKey.test-4, test-7 | Ten 0.1s added one at a time give 0.9999999999999999; test 7's chances give 0.9999999999999998 even with `sum` | correct | script, CPython 3.13 (Pyodide 0.27 is 3.12: same compensated `sum`) |
| homework-1 items[8] tests[6] | Longest head run pmf 0.027, 0.336, 0.294, 0.343 | correct | script runs the solution |
| homework-2 items[0] | Missing chance 0.4; E[X] = 2.7; slips 2.5, 1.5 | correct | arithmetic |
| homework-2 items[1] | 91/6 − 15 = 1/6; slip −2.75 from 3.5² | correct | Jensen gap |
| homework-2 items[2].prose | n people, "birthdays spread evenly over 365 days" | imprecise | finding 7 (independence of birthdays not stated) |
| homework-2 items[2].widget | E[N] = n(n − 1)/730; slips | correct | C(n,2)/365 |
| homework-2 items[3].widget.lines | Proof of E[aX + b] = aE[X] + b | correct | split the sum |
| homework-2 items[4] | Capped St Petersburg: fair price £5; slips 62, 32, 2; uncapped sum grows without bound | correct | script; Ross ch. 4 theoretical exercise (St Petersburg) |
| homework-2 items[5] | E[distinct faces] = 6(1 − (5/6)⁶) ≈ 3.991; slips | correct | script (exact and MC) |
| homework-2 items[6] | E[X(7 − X)] = 28/3; product slip 12.25; negative dependence makes the rule fail | correct | script; Cov(X, 7 − X) = −Var(X) < 0 |
| homework-2 items[7] | Overround 5.56%; balanced book keeps 1/19 of stakes | correct | script |
| homework-2 items[8].widget.options | Both books expect 0.2 defaults; no default likelier in B (0.9 > 0.81); both defaulting 0.01 against 0.1 | correct | arithmetic |
| homework-2 items[9] | Independent routing (stated): 10 × 0.9¹⁰ ≈ 3.487 empty venues; slips 0.349, 10/e, 0; at most nine empty | correct | script (exact and MC) |
| homework-2 items[10].model 1 to 3 | E[N] = 1 for every n ≥ 1; indicators dependent; n = 3 list 3, 1, 1, 1, 0, 0 | correct | script |
| homework-2 items[10].prompt part 4 | "How many traders expect to keep their own account?" | misleading | finding 10: read literally, no trader expects it (each has chance 1/40); the model answers the expected number of traders |
| homework-3 items[0] | Var(max(X − 4, 0)) = 7/12; slips 0.833, 2.917, 0.764 | correct | script |
| homework-3 items[1] | Var(I) = p − p² | correct | I² = I |
| homework-3 items[2].widget.lines | Var(X + Y) = Var X + Var Y + 2Cov for any X, Y | correct | BH 7.3 property 5 |
| homework-3 items[3] | sd √13 thousand = £3,605.55; slips 7,000, 5,000, 1,000, 6,082.76 | correct | script |
| homework-3 items[4] | 5w² − 2w + 1, minimum at w = 0.2 | correct | expansion; derivative |
| homework-3 items[5] | Smallest n is 13 (15.99%; 16.07% at 12; 16.28% at 10); independent slip 3 | correct | script |
| homework-3 items[6].model, rubric | Means 8, 9; variances 216, 84; Cov 48; ρ 0.356; Var(A + B) 396; sds add to 23.86; 17.32 at ρ = 0 | correct | script |
| homework-3 items[7] | 70:30, ρ = −0.2: sd 17.15%; slips 0.205, 0.1776, 0.1834, 0.0294 | correct | script |

## problems-1, problems-2, problems-3, fluency

| Path | Claim | Verdict | Basis |
|---|---|---|---|
| problems-1 items[0].parts[0..3] | Spinner product: 3/16; F(4) = 8/16; P(4 < M ≤ 9) = 5/16; P(W = 0) = 10/16; all slips and carried values | correct | script; pmf 1,2,2,3,2,2,1,2,1 over 16 by hand |
| problems-1 items[1].parts[0..2] | Independent bonds (stated): 0.2916; 0.9477; 0.0486 and slips | correct | binomial(4, 0.1) |
| problems-1 items[1].parts[3..4] | 95% VaR £50k with four bonds, £25k with three; VaR is a level of the CDF | correct | script; MFE section 2.2 |
| problems-1 items[2].parts[0..3] | c = 0.15; P(Y = 2) = 0.25; F_Y(1) = 0.75; independent days (stated) give P(T ≥ 3) = 0.3375; slips | correct | script |
| problems-1 items[3].parts[0..3] | Min of three independent quotes: 27 outcomes; 0.784; 0.296; 10 dealers; slips 21 and 6 | correct | script |
| problems-2 items[0].parts[0..3] | Expected claim £45; profit £15; £30,000 whatever the link; excess gives £57.50 | correct | script; X − 50·I with E[I] = 0.15 |
| problems-2 items[1].parts[0..1] | Independent days (stated): reversal chance 0.48; E[R] = 9.12 | correct | script |
| problems-2 items[1].parts[2] | Dependence of neighbouring indicators changes nothing in E[R] | correct | linearity; script shows P(I₃ given I₂) = 0.5, mean unchanged |
| problems-2 items[1].parts[3..4] | E[57 − 8R] = −15.96; break-even gain 45.6/9.88 ≈ 4.62; slips | correct | script |
| problems-2 items[2].parts[0..3] | E[S] = 41.2; call 2.4 (max is not linear: 1.2 slip); put 1.2 by C − Q = S − 40; trader expects £0.60 | correct | script; put-call parity payoff identity (Hull, chapter on properties of stock options) |
| problems-2 items[3].parts[0] | Third token gold with chance 0.3 by symmetry | correct | exchangeability; script MC |
| problems-2 items[3].parts[1..4] | E[G] = 1.2; E[V] = 38; P(G ≥ 2) = 1/3; fair price 43.50; with-replacement slips 0.3483, 44.48, 43.72 | correct | script, exact over 210 hands |
| problems-3 items[0].parts[0..3] | Mean 1.1; variance 5.89; 100 independent trades sd 24.27; n = 487 | correct | script |
| problems-3 items[1].parts[0..3] | E[A] = 0.8%; Var(A) = 2.16; Cov = 1.68; ρ = 7/12; slips | correct | script |
| problems-3 items[1].parts[4] | h = Cov/Var(B) = 0.4375 leaves Var(A)(1 − ρ²) = 1.425; removes ρ² ≈ 34% | correct | script; Hull, same chapter |
| problems-3 items[2].parts[0..4] | E[X] = 0.12; Var 0.0196; independent funds (stated): w* = 0.2; sd 0.0626; mix has the best mean per unit sd of the three | correct | script |
| problems-3 items[3].parts[0..3] | Cov(I_j, I_k) = 0.05; Var(N) = 1.6; sd £15.18; largest n is 5; slips 11 and 6 | correct | script; a model with these pair chances exists (script MC) |
| fluency families[0..1] | Var = E[X²] − μ² for two- and three-point pmfs; slip lines for E[X²] and for subtracting μ | correct | identity; slip guards mu ≠ 0, mu ≠ 1 are exactly the cases where the slips coincide with the key |
| fluency families[2] | sd of a two-point trade is √(pq)(a + b) | correct | script over every draw |

## Counts

Rows: 342. Verdicts: correct 330, imprecise 11, misleading 1, wrong 0, unverified 0. Three of the l12 rows marked imprecise are one finding (finding 1); the eleven imprecise rows map to findings 1 to 9 and the misleading row to finding 10. Many rows cover a key together with its slip values or a block of per-cell feedback lines; each value in such a row was recomputed singly, by hand or in the script.

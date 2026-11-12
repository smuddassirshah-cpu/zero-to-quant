# Claim ledger: random-vars levels 4 and 5, round 2 (blind)

Scope: `l13` to `l20`, `review-4`, `review-5`, `homework-4`, `homework-5`, `problems-4`, `problems-5` in `app/content/courses/random-vars/`. No `fluency-*.json` file belongs to l13 to l20 (the only fluency file is for l9).

Every row was judged by hand from the content text; none is generated. Grouping convention: the three hints of a screen share one row when they are one method chain; each graded key has a row; each wrong option or slip has a row together with its `why` or `byKey` line; each `explain` has a row, split where it makes more than one claim.

Bases. BH = Blitzstein and Hwang, *Introduction to Probability*, 2nd ed.: ch. 3.8 and 7.1 (joint, marginal, conditional pmf, independence), 7.3 (covariance, correlation), 7.4 (multinomial), 4.3 and 4.4 (geometric, negative binomial, indicators; section numbers are given to two levels only), 9.1 to 9.3 (conditional expectation, Adam's law), 9.5 (Eve's law), 9.6 (random sums), 10.1 (Cauchy–Schwarz, Jensen). CB = Casella and Berger, *Statistical Inference*, 2nd ed., ch. 4. `script` = a named check in `docs/reports/random-vars-L4-5-concepts-r2.py`. `deriv` = the short derivation written in the row.

Verdicts: `correct`, `wrong`, `imprecise`, `misleading`, `unverified`.

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l13 | screens[0].prose | one table holds the chance of every (market, stock) pair | correct | BH 7.1 joint pmf |
| l13 | screens[1].prose | nine cells add to 1 | correct | script `l13 cells sum` |
| l13 | screens[1].widget.answer | market −1% is row 1, three cells | correct | script `l13 s1 answer row` |
| l13 | screens[1].widget.wrong column + byKey | column shaded is "stock falls 2%" | correct | column 1 head is −2% |
| l13 | screens[1].feedback.byKey r2c1, r3c1 | row 2 flat market, row 3 market rise | correct | row heads 0%, +1% |
| l13 | screens[1].hints | market move picks a row | correct | table layout |
| l13 | screens[1].explain | disjoint cells add: 0.12+0.06+0.02 = 0.20 = P(X=−1) | correct | BH 7.1 marginal; script |
| l13 | screens[2].widget.answer | stock +2% is column 3 | correct | script |
| l13 | screens[2].wrong row + byKey | row 3 is "market rises 1%" | correct | row heads |
| l13 | screens[2].explain | column sum 0.30 = P(Y=2) whatever the market | correct | BH 7.1; script col totals |
| l13 | screens[3].prose | margins are called marginal distributions; column totals give P(Y=y) | correct | BH 7.1 |
| l13 | screens[3].widget rows | 0.25, 0.45, total 1 | correct | script `l13 s3` |
| l13 | screens[3].hints + byKey | add down each column | correct | marginalisation |
| l13 | screens[3].explain | column totals count every cell once, so they are a pmf for Y | correct | BH 7.1 |
| l13 | screens[4].prose | knowing X=−1 leaves only row 1 | correct | conditioning restricts the sample space, BH 2.2 |
| l13 | screens[4] key 0.60 | 0.12/0.20 | correct | script `l13 s4 key` |
| l13 | screens[4] option cell 0.12 + why | joint cell is chance of both out of all days | correct | definition of joint |
| l13 | screens[4] option col 0.48 + why | 0.12/0.25 conditions on the stock's move | correct | script; that is P(X=−1 given Y=−2) |
| l13 | screens[4] option marg 0.25 + why | P(Y=−2) over all days | correct | script |
| l13 | screens[4].hints, explain | row 1 is the new whole; before the news 0.25 | correct | BH 7.1 conditional pmf |
| l13 | screens[5] keys 0.30, 0.10, 1 | row rescaled by 0.20 | correct | script `l13 s5` |
| l13 | screens[5].byKey r3c2 | a row divided by its own total always sums to 1 | correct | deriv on screens[7]; needs total > 0, said there |
| l13 | screens[5].explain | full pmf for the stock given X=−1; drop six times as likely as rise | correct | script `l13 s5 six times` |
| l13 | screens[6] key 0.10, 0.30, 0.60 | row 3 over 0.30 | correct | script `l13 s6 right` |
| l13 | screens[6] option cells + why/byKey | joint cells add to 0.30 = P(X=1), not 1 | correct | row total |
| l13 | screens[6] option cols + why/byKey | 0.12, 0.20, 0.60 are P(X=1 given Y=y), add to 0.92 | correct | script `l13 s6 cols` |
| l13 | screens[6] option marg + why | 0.25, 0.45, 0.30 is the marginal of Y | correct | script |
| l13 | screens[6].explain | a conditional row always sums to 1; raw cells sum to P(X=1) | correct | deriv screens[7] |
| l13 | screens[7].prose | P(X=x) = Σ_y P(x,y); P(Y=y given X=x) = P(x,y)/P(X=x) | correct | BH 7.1 definitions |
| l13 | screens[7].widget lines + answer | Σ_y conditional = 1 by pulling out 1/P(X=x) | correct | deriv, finite sum |
| l13 | screens[7].byKey, hints | order of the derivation | correct | each line uses the previous |
| l13 | screens[7].explain | need P(X=x) > 0 | correct | division by the margin |
| l13 | screens[8] keys 0.6, 0.5, 0.2308 | 0.12/0.20, 0.40/0.80, 0.12/0.52 | correct | script `l13 s8` |
| l13 | screens[8].hints, byKey | divide by the total of the row or column you were told | correct | BH 7.1 |
| l13 | screens[8].explain (edge) | 0.60 against 0.50: a real edge | correct | P(U given S=1) > P(U given S=0), in the model |
| l13 | screens[8].explain (cross-reference) | same turn-around met as Bayes on a trading signal in Conditional Probability | correct | `conditional/l26-trading-signal.json`, title "Bayes on a trading signal" |
| l13 | screens[9] key 0.75 | 0.30/0.40 | correct | script |
| l13 | screens[9] slip cell 0.3 | joint chance both fill | correct | cell (2,2) |
| l13 | screens[9] slip marg 0.4 | "P(B=2) on its own" | correct | column total 0.40; also the row total, the line stays true |
| l13 | screens[9].explain | fills move together because both fill when the price trades through | correct | modelling story; table shows positive dependence (0.75 > 0.40) |
| l13 | summary.ideas | joint, marginal, conditional row | correct | BH 7.1 |
| l13 | summary.formula + note | conditional pmf, defined only when P(X=x) > 0 | correct | BH 7.1 |
| l13 | summary.trap | a joint cell is not a conditional chance | correct | screens[6] |
| l13 | quiz[0] key 0.4, slips 0.3, 0.5 | column sum; cell; row total P(X=1) | correct | script `l13 q0` |
| l13 | quiz[1] key 0.75, slips 0.6, 0.3 | 0.30/0.40; reversed is P(Y=1 given X=1) | correct | script `l13 q1` |
| l13 | quiz[2] key + whys | list adding to 0.9 cannot be conditional; chances can be anything in [0,1]; raw cells add to P(X=2) | correct | row sums to 1 |
| l13 | quiz[3] key + whys | margins give P(Y=2), not a cell or a conditional | correct | script `l13 q3`; "always" in the stem covers degenerate margins |
| l14 | screens[0] key 0.40, options 0.12, 0.30 | 0.12/0.30; cell; 0.12/0.40 = P(X=2 given Y=1) | correct | script `l14 s0` |
| l14 | screens[0].explain | conditional equals the margin 0.40: A's count did not move B's chances | correct | script `l14 AB independent` |
| l14 | screens[1].canvas.derive | each row over its total | correct | all rows give 0.3, 0.4, 0.3 |
| l14 | screens[1] key + whys | bars stay at 0.30, 0.40, 0.30; dividing by the row total cancels the change | correct | script |
| l14 | screens[1].explain | knowing X tells nothing about Y, so each cell = row total × column total | correct | BH 3.8, equivalent forms of independence |
| l14 | screens[2].prose | definition: every conditional row equals the margin ⇔ independent ⇔ cells are products | correct | BH 7.1; rows with positive total |
| l14 | screens[2] six products | 0.15, 0.20, 0.15, 0.09, 0.12, 0.09 | correct | script `l14 s2 product` |
| l14 | screens[2].explain | same margins as A and B, so the products match A and B's cells | correct | script `l14 CD same margins` |
| l14 | screens[3] answer four cells | (0,0), (0,1), (1,0), (1,1) differ | correct | script `l14 s3 failing cells` |
| l14 | screens[3] slip one + byKey | one failing cell is enough to break independence | correct | definition needs every cell |
| l14 | screens[3].explain | same margins, different insides | correct | script |
| l14 | screens[4].prose | E[X] = 1.1, E[Y] = 1.0 | correct | script |
| l14 | screens[4] key 1.1 | E[XY] over four non-zero cells | correct | script `l14 s4 key` |
| l14 | screens[4] slips 2.1, 0.56 | E[X]+E[Y]; sum of the four chances | correct | script |
| l14 | screens[4].explain | Cov = E[XY] − E[X]E[Y] = 0; independence forced it | correct | BH 7.3 |
| l14 | screens[5] key + option whys | (1,1) holds 0.11 against 0.09; margins always add to 1; equal cells not needed | correct | script `l14 s5 four fail` |
| l14 | screens[5].explain | four cells fail; P(Y=2 given X=2) = 0.20 against 0.10; first row and margins would miss it | correct | script |
| l14 | screens[6] key 0, slips 2/3, 2/9 | Cov(X, X²) = 0; E[Y]; Var(Y) = 2/3 − 4/9 | correct | script `l14 s6` |
| l14 | screens[6].hints, explain | XY = X³, E[XY] = 0, E[X] = 0 | correct | deriv |
| l14 | screens[7] key + whys | P(0,0) = 1/3 but product 1/9; covariance really is 0 | correct | script `l14 s7` |
| l14 | screens[7].explain | covariance measures only straight-line co-movement | correct | BH 7.3, correlation as linear association |
| l14 | screens[8] derivation | E[XY] = E[X]E[Y] under independence; uses it once, on the cells | correct | BH 7.3 proof (discrete) |
| l14 | screens[8].explain | zero covariance is the weaker statement; Y = X² satisfies line 4, fails line 2 | correct | BH example 7.3.3 |
| l14 | screens[9].canvas cells + caption | joint of the shared-volatility pair; every margin 0.25; correlation 0 | correct | script `l14 s9 canvas`, `corr 0` |
| l14 | screens[9] key 0.5, slips 0.25, 0.0625, 0.125 | 0.125/0.25; margin; product of margins; joint cell | correct | script |
| l14 | screens[9].explain | big move in one predicts big move in the other; correlation matrix misses shared volatility | correct | E[B² given A] differs, script `hw4 3` |
| l14 | screens[10] key 0.5 | 0.6×0.5 + 0.4×0.5, independence stated | correct | script |
| l14 | screens[10] slips 1.1, 0.3, 0.2 | sum of fill chances; both fill; A misses and B fills | correct | script; 0.3 is also "A fills, B misses", the line stays true |
| l14 | summary.ideas[0..2] | product rule every cell; independence ⇒ conditional rows equal margin and Cov 0; zero covariance does not give independence | correct | BH 7.1, 7.3 |
| l14 | summary.formula.note, trap | beyond 2 by 2, one matching cell proves nothing; in 2 by 2 it does | correct | script `l14 2x2 one cell is enough` |
| l14 | quiz[0] key + whys | 0.28, 0.42, 0.12, 0.18 are the products | correct | script `l14 q0` |
| l14 | quiz[1] key −6, slip −1 | independence gives E[XY] = E[X]E[Y] (sufficient, stated as such) | correct | BH 7.3 |
| l14 | quiz[2] key + whys | Cov = 0 is exactly E[XY] = E[X]E[Y]; does not give independence | correct | definition |
| l14 | quiz[3] key 0.18, slips 0.9, 0.28 | 0.3×0.6; added misses; both fill | correct | script |
| l15 | screens[0] key −0.8 | row 1 rescaled 0.5, 0.4, 0.1 | correct | script `l15 cond means` |
| l15 | screens[0] options −0.16, 0.24, −2 | raw-cell sum; E[Y]; mode | correct | script |
| l15 | screens[1] key + whys | −0.8, 0.2, 1.0; 0.24 is the overall mean; not equal to x | correct | script |
| l15 | screens[2].prose | definition of E[Y given X = x] as the average inside row x | correct | BH 9.1 |
| l15 | screens[2] keys 0.2, 1.0 | rows rescaled 0.2, 0.5, 0.3 and 0.1, 0.3, 0.6 | correct | script |
| l15 | screens[3].prose | E[Y given X] takes −0.8, 0.2, 1.0 depending on X | correct | BH 9.2 |
| l15 | screens[3] key 0.3, slips 0.18, 0.35, 1.0 | P(X=1); cell P(X=1,Y=2); P(Y=2); the value | correct | script `l15 s3` |
| l15 | screens[3].explain | E[Y given X] is a random variable, a function of X, with pmf 0.2, 0.5, 0.3 | correct | BH 9.2 |
| l15 | screens[4] key g = 0.2 | conditional mean minimises expected squared error | correct | BH 9.3; script `l15 s4 mean minimises` |
| l15 | screens[4] options 0, 0.24, 0.25 + whys | mode; overall mean; the cell chance (0,0) | correct | script; cell is 0.25 |
| l15 | screens[4].explain | errors 1.96, 1.9616, 2.00; E[Y given X=x] plotted against x is the regression function | correct | script; standard term, CB 4.4 |
| l15 | screens[5] key 1.0, options 0.30, 0.77, 0.24 | raw-cell sum 0.30; column-scaled 0.77; E[Y] | correct | script `l15 s5` |
| l15 | screens[5].explain | unscaled sum short by the factor P(X=1) | correct | deriv screens[7] |
| l15 | screens[6] key 1.0, slips 0.3, 1.1 | independent desks; unscaled sum; E[X] | correct | script |
| l15 | screens[6].explain | X ⊥ Y ⇒ E[Y given X=x] = E[Y] for every x (one direction, as stated) | correct | BH 9.3 |
| l15 | screens[7] derivation | E[Y given X=x] = Σ y P(x,y) / P(X=x) | correct | BH 9.1 |
| l15 | screens[8] keys −0.9, 0.7 | column-weighted means | correct | script `l15 s8` |
| l15 | screens[8].explain (averages) | falls 0.9% on an average down day, rises 0.7% on an up day | correct | script |
| l15 | screens[8].explain (beta) | "conditional beta is 0.9 on the way down and 0.7 on the way up"; "a single beta of 0.8" | imprecise | x = ±1 labels the kind of day, not a 1% move; beta is a regression slope of return on market return (Hull ch. 3.5). Finding 5 |
| l15 | screens[9] key 220, slips 225, 500, 70 | column mean; equal average; full quote; E[F given Q=100] | correct | script `l15 s9` |
| l15 | screens[9].explain | 44% and 70% of the quote; five times the size buys about three times the fill | correct | 220/70 = 3.14 |
| l15 | summary.ideas, formula, trap | conditional mean; random variable; regression function; flat if independent | correct | BH 9.1 to 9.3 |
| l15 | quiz[0] key 8, slips 4, 6 | 10×0.4/0.5; unscaled; E[Y] | correct | script |
| l15 | quiz[1] key + whys | E[Y given X] is a random variable, function of X; Y averaged out | correct | BH 9.2 |
| l15 | quiz[2] key 3 + byKey | independence leaves the conditional mean at E[Y] | correct | BH 9.3 |
| l15 | quiz[3] key 2.25, slips 2.3333, 2 | weighted; plain average 7/3; mode | correct | script |
| l16 | screens[0] key 0.24 | 0.2(−0.8)+0.5(0.2)+0.3(1.0) | correct | script |
| l16 | screens[0] option 0.13 + why | plain average of the three | correct | 0.4/3 = 0.133 |
| l16 | screens[0] option −0.16 + why | product of the three averages | correct | −0.8×0.2×1.0; also the first weighted term, the line stays true |
| l16 | screens[0] option 0.2 + why | most likely branch only; the other two happen half the time | correct | 0.2+0.3 = 0.5 |
| l16 | screens[0].explain | matches E[Y] from the margin | correct | script `l15 E[Y]` |
| l16 | screens[1] key 0.4, slips 0.5, 0.6 | break-even share; at 50% the average is −£30; weights the wrong way round | correct | script `l16 s1` |
| l16 | screens[2].prose | law of total expectation, sum form | correct | BH 9.1 |
| l16 | screens[2] key 1+E + whys | one toss used, coin has no memory, fresh copy | correct | BH 9.1, conditioning on the first step |
| l16 | screens[3] E = 2 | E = 1 + E/2 | correct | deriv |
| l16 | screens[3].explain | "on average the first head comes on the second toss" | correct | E[N] = 2 |
| l16 | screens[4] key 4, slips 3, 0.25, 1 | 1/p; failures only; the chance; E = 1/4 + 3E/4 gives 1 | correct | script `l16 s4` |
| l16 | screens[5] key 6 | E = ½(1+E) + ¼·2 + ¼(2+E) | correct | script; MC `l16 s5 MC HH wait 6` |
| l16 | screens[5] slip 4 + byKey | doubled the one-head wait; a tail after a head restarts | correct | deriv |
| l16 | screens[5] slip 3 + byKey | "three tosses would be enough only if no tail ever interrupted" | imprecise | with no tail at all two tosses are enough; 3 is the one-head wait plus one toss. Finding 2 |
| l16 | screens[5].explain | a tail after a head wastes two tosses | correct | the h-t leaf is 2 + E |
| l16 | screens[6] key 6 + whys | 5 is misses only; 3.5 is the mean face; 1/6 is the chance | correct | BH 4.3 geometric |
| l16 | screens[7] derivation | E[N] = 1/p for p > 0 | correct | BH 4.3; dividing by p > 0 said; E[N] finite is used silently (the homework model answer says it) |
| l16 | screens[7].explain | 2, 4, 6 and 1 for p = ½, ¼, 1/6, 1 | correct | script |
| l16 | screens[8] code | n = 1 counts the head; starter fails, solution passes | correct | script `l16 s8 code` |
| l16 | screens[8].widget.how | within about six standard errors | correct | 7.9, 6.1 and 6.0 SEs, script |
| l16 | screens[8].explain | n = 0 gives 1/p − 1; averages 1.99834, 6.03976, 5.03602 | correct | script replays the solution with those seeds |
| l16 | screens[9] key 5, slips 4, 0.2 | 1/0.2; waits only; the chance | correct | script |
| l16 | screens[9].explain | on average four quiet minutes, fills in the fifth | correct | E[failures] = 4 |
| l16 | screens[10] key 130, slips −50, 280, −150 | weighted; plain; calm branch; volatile branch | correct | script |
| l16 | screens[10].explain | volatile takes back more than half of calm gains | correct | 150/280 = 0.54 |
| l16 | summary.ideas, formula.note, trap | weight and add; condition on the first trial; 1/p; 1/p − 1 is failures | correct | BH 9.1, 4.3 |
| l16 | quiz[0] key 1, slip 0 | p = 1 | correct | N = 1 always |
| l16 | quiz[1] key 11250, slip 19000 | weighted loss; plain; C carries 60% | correct | script |
| l16 | quiz[2] key 3, slips 2, 6 | p = 1/3 | correct | script |
| l16 | quiz[3] key 5, options 4, 12 | 0.25×2 + 0.75×6 | correct | script |
| l17 | screens[0] key 26000, slips 50000, 19600, 90000, 10000 | weighted variances; equal weights; (average sd)²; each regime alone | correct | script `l17 s0` |
| l17 | screens[1].canvas sim | each day one sd either side of its regime mean | correct | outcomes 220/20 and 120/−480 |
| l17 | screens[1] key above + whys, explain | variance settles near 40,400, above 26,000 | correct | MC `l17 s1 MC variance 40,400` |
| l17 | screens[2].prose | E[Y given X] is £120 w.p. 0.8, −£180 w.p. 0.2, centre £60 | correct | script `l17 mean 60` |
| l17 | screens[2] key 14400 | 0.8·60² + 0.2·240² | correct | script |
| l17 | screens[2] slips 30600, 120, 90000, 3600 | unweighted; sd; 300²; overall mean squared | correct | script; 3600 is also the calm distance squared, the line stays true |
| l17 | screens[3].prose | law of total variance | correct | BH 9.5 (Eve's law) |
| l17 | screens[3] key 40400, slips | sum; pieces alone; sd 201 | correct | script |
| l17 | screens[3].explain | sd £201 against £161 from 26,000 alone | correct | script |
| l17 | screens[4] keys 1.96, 1.8 (and 1.76) | conditional variances of the rows | correct | script `l17 s4 cond vars` |
| l17 | screens[4].byKey | 2.0 and 2.8 are E[Y² given X] | correct | script |
| l17 | screens[5].prose | given N = n, H has mean n/2, variance n/4 | correct | Binomial(n, ½) |
| l17 | screens[5] keys 0.875, 0.7292, 1.6042 | E[N]/4; Var(N)/4; 77/48 | correct | script |
| l17 | screens[5].byKey | 1.75 uses n/2; scaling by ½ divides the variance by 4 | correct | Var(aN) = a²Var(N) |
| l17 | screens[5].explain | 77/48 is the variance of H found from its own distribution | correct | script `l17 s5 Var(H) from its own pmf` (exact) |
| l17 | screens[6].prose | Var(Y given X) is a random variable until X is known | correct | BH 9.5 |
| l17 | screens[6] key 1.872, slips 1.84, 1.96 | weighted; plain; modal row | correct | script |
| l17 | screens[6].explain | Var(E[Y given X]) = 0.3904, Var(Y) = 2.2624 from the column totals | correct | script `l17 s6 Var(Y) two ways` |
| l17 | screens[7] key + whys | the report left out the spread of regime averages; equal weights give 50,000 | correct | Eve's law |
| l17 | screens[7].explain | about 20% steadier in sd | correct | script |
| l17 | screens[8] key 2.64, slips 2.6, 0.04 | overall mean 0; inside 2.6; between 0.04 | correct | script |
| l17 | screens[8].explain | equal conditional means ⇒ second piece 0; Y fixed by X ⇒ first piece 0 | correct | each piece is a variance or an average of variances |
| l17 | screens[9] derivation | Eve's law from Adam's law on Y and Y² | correct | BH 9.5 proof; d2 and d3 in either order |
| l17 | screens[10] key 0.3564, slips 0.6436, 0.5538, 0.2 | 14400/40400; inside share; over the inside piece; share of days | correct | script |
| l17 | screens[10].explain | −£480 is 6 calm sds below the calm mean, one volatile sd below the volatile mean | correct | script |
| l17 | summary | two pieces; when each vanishes | correct | BH 9.5 |
| l17 | quiz[0] key 8, slips | sum, not product or difference | correct | Eve's law |
| l17 | quiz[1] key 29, slips 4, 25, 33 | inside 4, between 25 | correct | script |
| l17 | quiz[2] key 0 + whys | Y fixed by X ⇒ E[Var(Y given X)] = 0; equality with Var(Y) needs constant E[Y given X] | correct | true equivalence: Var(E[Y given X]) = 0 |
| l17 | quiz[3] key ≥ + whys | Var(Y) ≥ E[Var(Y given X)] always; second piece vanishes only when the conditional means agree | correct | true equivalence |
| l18 | screens[0].prose | each fill earns £5 on average whatever N is | correct | the hypothesis that makes E[S given N] = 5N |
| l18 | screens[0] key 100, slips 5, 20, 125 | E[N]·5; one fill; E[N]; busiest branch | correct | script |
| l18 | screens[1].prose | dashed line: 20 independent fills, 20×900 | correct | variances of independent terms add |
| l18 | screens[1] key above + whys, explain | variance settles near 18,500 | correct | script `l18 exact variance 18,500` (exact enumeration) |
| l18 | screens[2] key 22500 | Var(S given N = 25) = 25×900, independent fills | correct | BH 7.3 |
| l18 | screens[2] slip 562500 + byKey | 25²×900, as if all fills were one draw | correct | Var(25X) |
| l18 | screens[2] slip 750 + byKey | "That is 25 × 30. Sds do not add, variances do." | imprecise | variances add for uncorrelated terms; sds add under perfect positive correlation. Finding 3 |
| l18 | screens[2].explain | no factor 25² because the fills do not move together | correct | Var of a sum of uncorrelated terms |
| l18 | screens[3] keys 18000, 500, 18500 | E[Var(S given N)]; Var(5N); sum; sd £136.01 | correct | script |
| l18 | screens[4].prose | random-sum formulas E[N]Var(X), Var(N)E[X]², E[S] = E[N]E[X] | correct | BH example 9.6.1 |
| l18 | screens[4] key 134.16, slips 136.01, 600, 18000 | fixed N: √18000 | correct | script |
| l18 | screens[5] key 1.6042, slips 0.875, 3.0625 | die and coins; first term only; E[N]²Var(X) | correct | script |
| l18 | screens[6] key + whys | 20×30 treats 20 fills as one fill scaled up; count adds only 500; sum of independent fills spreads like √n | correct | script |
| l18 | screens[7] derivation | Var(S) = E[N]Var(X) + Var(N)E[X]² | correct | BH 9.6; uses N independent of the fills, said on screens[8] and in the summary |
| l18 | screens[7].explain | E[S] = E[N E[X]] = E[N]E[X] | correct | Adam's law |
| l18 | screens[8] key 18000, slips 18500, 134.16 | E[X] = 0 kills the second term | correct | script |
| l18 | screens[8].explain | the proof assumed N independent of the fills; if busy days have worse fills the formulas can fail | correct | "can fail", not "fail"; script `l18 dependence can break`, `l18 Wald` |
| l18 | screens[9] code | variance = en*vx + vn*ex**2; starter fails, solution passes 7 tests | correct | script `l18 s9 code` |
| l18 | screens[9].explain | seed 8, 20,000 days: 18466.21 | correct | script replays `random_sum` |
| l18 | screens[10].prose | trades independent of the others and of the count | correct | hypothesis stated |
| l18 | screens[10] key 23200, slips 21600, 152.32, 518400 | E[N] = 24, Var(N) = 64 | correct | script, two ways |
| l18 | screens[10].explain | first term grows by 3,600, second adds 1,600; with dependence the formulas could fail | correct | script; sufficient-condition wording |
| l18 | summary.ideas, formula, trap | condition on N; mean and variance; zero-mean fills; assumption named | correct | BH 9.6 |
| l18 | quiz[0] key 86, slips 50, 500, 110 | 50 + 36; count term dropped; E[N]²Var(X); E[N]E[X]² + Var(N)Var(X) | correct | script |
| l18 | quiz[1] key 2000, slips 0, 20, 200 | S = 10N | correct | Var(10N) |
| l18 | quiz[2] stem + key | "When do they fail?" keyed "when N and the fills are dependent" | imprecise | independence of N is sufficient, not necessary: E[S] = E[N]E[X] holds for any stopping time N (Wald's identity; Ross, *A First Course in Probability*, ch. 7; script `l18 Wald`). Finding 4 |
| l18 | quiz[2] whys, explain | formulas are for random counts; zero-mean fills are fine; if the count changes the mean, E[S given N] is no longer N E[X] | correct | derivation line e2 |
| l18 | quiz[3] key 13115, slips 10392, 36000 | √172,000,000 | correct | script |
| l19 | screens[0] key 99, slips 100, 90, 110 | returns multiply | correct | script |
| l19 | screens[1] key below + whys, explain | chord of a concave curve lies below it; midpoint touches only at a = 0 | correct | definition of concavity |
| l19 | screens[2].prose | concave: chords lie below; Jensen for concave g | correct | BH 10.1 |
| l19 | screens[2] key −0.00503, slips 0, 0.00503, 0.0953 | ½ ln 0.99 | correct | script |
| l19 | screens[2].explain | it is the daily growth rate of the £100 | correct | E[ln(1+R)] is the long-run log growth rate (SLLN) |
| l19 | screens[3] key 9, slips 34, 25, 3 | E[X²] − (E[X])² = Var(X) | correct | script |
| l19 | screens[3].explain | Jensen for x² says a variance is never negative | correct | BH 10.1 |
| l19 | screens[4].prose | 1/x is convex (x > 0); shares per pound is 1/X | correct | second derivative 2/x³ > 0 |
| l19 | screens[4] key 17.14, slips 23.33, 20, 17.5 | harmonic mean of the prices | correct | script |
| l19 | screens[4].explain | E[1/X] ≥ 1/E[X]: a fixed sum buys more shares than at the average price | correct | script |
| l19 | screens[5].prose | call payoff (X − 100)⁺ is convex | correct | max of two linear functions |
| l19 | screens[5] key 10, slips 0, 20, 100 | average payoff | correct | script |
| l19 | screens[5].explain | expected convex payoff is at least the payoff at the expected price | correct | Jensen, BH 10.1 |
| l19 | screens[6] key < + whys | strict for non-constant positive X; one direction for every positive X | correct | √ strictly concave, BH 10.1 equality case |
| l19 | screens[6].byKey.equal | second-order gap σ²/(8μ^{3/2}) | correct | script `l19 s6 second-order gap` |
| l19 | screens[6].explain | X = 1 or 9: 2 against 2.236 | correct | script |
| l19 | screens[7].prose | "Stat 110 style" | correct | BH ch. 10 exercises ask for ≥, ≤, = or ? between pairs |
| l19 | screens[7] keys | e^X ≥; √ ≤; X³ on X > 0 ≥; E[X]E[Y] v E[XY] either way | correct | script `l19 s7`; Cov has either sign |
| l19 | screens[8] derivation | tangent-line proof for smooth convex g | correct | BH 10.1 proof |
| l19 | screens[8].explain | at a kink any supporting line does the same job | correct | supporting hyperplane, Rockafellar thm 23.4 |
| l19 | screens[9].prose | cube bends down for x < 0, up for x > 0 | correct | g'' = 6x |
| l19 | screens[9] key −12, slips 12, 0, −13 | −13 − (−1) | correct | script |
| l19 | screens[9].explain | X = −1 or 3 gives +12, so no inequality in general | correct | script `l19 s9 mirror` |
| l19 | screens[10].prose | Cauchy–Schwarz | correct | BH 10.1 |
| l19 | screens[10] key 6, slips 5, 36, 1.5 | sd_X sd_Y | correct | script |
| l19 | screens[10].explain | abs(ρ) ≤ 1; equality only when one is a straight-line function of the other | correct | BH 7.3; non-zero sds |
| l19 | screens[11].prose | +7% or −5% has mean 1%, sd 6% | correct | script |
| l19 | screens[11] key 0.00818, slips 0.01, 0.0064, 0.0018 | ½(ln 1.07 + ln 0.95); arithmetic mean; σ² in full; drag alone | correct | script |
| l19 | screens[11].explain (numbers) | 0.818%; μ − σ²/2 = 0.82%; e^0.982 = 2.67; 1.01¹²⁰ = 3.30 | correct | script, median path is 60 ups |
| l19 | screens[11].explain (Kelly) | Kelly, from the Limits course, maximises E[ln W] | correct | Kelly (1956); `limits/l14-best-value.json` teaches the Kelly fraction |
| l19 | summary | concave and convex directions; equality needs X constant for a curve with no straight stretch; no inequality if g bends both ways | correct | BH 10.1 |
| l19 | quiz[0] key + whys | E[ln X] < ln E[X]; equality needs X constant or a straight-line g | correct | strict concavity |
| l19 | quiz[1] key 1, slips 5, 4, 0.5 | gap is Var(X) | correct | script; the 0.5 feedback names no quantity and redirects |
| l19 | quiz[2] key 8, slips 12.5, 25 | £200 for 25 shares | correct | script |
| l19 | quiz[3] key + whys | cube convex only for x > 0; oddness does not fix the direction | correct | screens[9] |
| l20 | screens[0] key 252, slips 30240, 5 | C(10,5); ordered picks | correct | script |
| l20 | screens[0].explain | symmetric bars | correct | C(n,k) = C(n,n−k) |
| l20 | screens[1] keys 2520, 0.0851 | 252×10; ×0.00003375 | correct | script |
| l20 | screens[2].prose | multinomial pmf; each count alone is binomial | correct | BH 7.4, 7.4.3 (lumping) |
| l20 | screens[2] key 0.2461, slips 0.0851, 0.5, 0.0313 | 252/1024 | correct | script |
| l20 | screens[3].prose | counts add to n so cannot be independent | correct | Cov = −n p_i p_j ≠ 0 |
| l20 | screens[3] derivation + explain | Cov(N_up, N_down) = −n p_up p_down = −1.5 | correct | BH 7.4; script exact enumeration |
| l20 | screens[4].prose | 0.2051, 0.2001, product 0.0410 | correct | script |
| l20 | screens[4] key 0.0638, slips 0.041, 0.00002 | 3150 × 0.00002025 | correct | script |
| l20 | screens[4].feedback, explain | ρ = −0.65; the counts are not independent so the product of marginals is not the joint | correct | script |
| l20 | screens[5].prose | T is three waits, each averaging 2.5 | correct | BH 4.3 (sum of geometrics) |
| l20 | screens[5] key 7.5, slips 2.5, 4.5, 1.2 | 3/p; failures only 3(0.6)/0.4; 3×0.4 | correct | script |
| l20 | screens[5].explain | the mean needs no independence; adding variances needs uncorrelated, which independence gives | correct | linearity; BH 7.3. Sufficient-condition wording is right |
| l20 | screens[6].prose | V = 0.6V + 1.5; 1.5 is the variance of the conditional means 1 and 3.5 | correct | script `l20 s6` |
| l20 | screens[6] key 11.25, slips 3.75, 7.5, 33.75 | r(1−p)/p² | correct | BH 4.3; MC `l20 MC Var(T)` |
| l20 | screens[7].prose | negative binomial as trials up to the rth success | correct | convention stated; the failures convention is named in the explain |
| l20 | screens[7] keys 0.1382, 0.4557; canvas pmf | C(4,2)0.4³0.6²; sum T = 3..6 | correct | script |
| l20 | screens[7].explain | equals at least three wins in six trades; some books count failures, T − r | correct | script; BH 4.3 uses failures |
| l20 | screens[8] key + whys, explain | C(5,3) counts three wins in five; 0.3174; 4 of the 10 patterns finish early | correct | script |
| l20 | screens[9].prose | chances 0.6, 0, 0.4; ask 6, 0, 4 | correct | sets the question |
| l20 | screens[9].canvas.params.levels[0].branches | tree shows Up 0.5, Flat 0.2, Down 0.3 | wrong | contradicts the screen's prose and key (0.6, 0, 0.4); script check fails on purpose. Finding 1 |
| l20 | screens[9] key 0.2508, slips 0, 0.0012 | C(10,6)0.6⁶0.4⁴ | correct | script |
| l20 | screens[9].hints, byKey, explain | 0! = 1 and 0⁰ = 1 so the category drops out; r = 1 gives the geometric | correct | convention 0⁰ = 1 for the empty product, Knuth (1992); Python agrees |
| l20 | screens[10] code | both functions; starter fails; comb is 0 when t < r | correct | script `l20 s10 code` |
| l20 | screens[11] key 0.1673, slips 0.8327, 0.006 | at most two wins in ten | correct | script, two ways |
| l20 | screens[11].explain | E[T] = 7.5, sd 3.35, a wait past ten is far from rare | correct | script |
| l20 | summary | multinomial; covariance; negative binomial moments; traps | correct | BH 7.4, 4.3 |
| l20 | quiz[0] key 0.18, slips 0.015, 0.09 | 12 orders | correct | script |
| l20 | quiz[1] key −2, slips 2, 0, 3.75 | −n p_i p_j; variance of the up count | correct | script |
| l20 | quiz[2] key 0.1875, slips 0.375, 0.0625 | C(3,1)0.5⁴ | correct | script |
| l20 | quiz[3] key + whys | r = 1 is the geometric | correct | BH 4.3 |
| rev4 | items[0] key 0.45, slips 0.25, 0.4 | column sum; strong cell; P(strong) | correct | script |
| rev4 | items[1] key 0.625, options 0.25, 0.556, 0.45 | 0.25/0.40; cell; P(strong given Y=1); margin | correct | script |
| rev4 | items[2] answer + byKey, explain | four cells off by 0.02; first column matches | correct | script `rev4 2` |
| rev4 | items[3] key + whys, explain | Cov(X, X²) = 0 on {−2, −1, 1, 2}; P(X=1, Y=4) = 0 against 1/8 | correct | script |
| rev4 | items[4] key 0.5, slips 0.2, 0.25 | conditional mean; unscaled; E[Y] | correct | script |
| rev4 | items[5] key 0.25, slips 0.2917, 0.0417 | E[Y given weak] = 1/12; plain; product | correct | script |
| rev4 | items[6] key 2.5, slips 1.5, 0.4, 1.6667 | 1/0.4; heads only; chance; 1/0.6 | correct | script; independent tosses are the convention for a coin |
| rev4 | items[7] key 0.5% + whys | conditional mean minimises squared error; mode 1%; overall 0.25% | correct | BH 9.3 |
| rev5 | items[0] key 125, slips 25, 100, 150 | inside 25, between 100 | correct | script |
| rev5 | items[1] key 105, slips 24, 144, 90 | 24 + 81; E[N]²Var(X); E[N]E[X]² + Var(N)Var(X) | correct | script |
| rev5 | items[2] key + whys | E[1/X] > 1/E[X] for non-constant positive X | correct | strict convexity |
| rev5 | items[3] key 0.1296, slips 0.00648, 0.0648 | 20 orders | correct | script |
| rev5 | items[4] key 2.236, slips 5, 2, 3 | √(9 − 4) | correct | Eve's law |
| rev5 | items[5] key 0.0092, slips; exact 0.9165% | μ − σ²/2; σ² = 0.16% | correct | script |
| rev5 | items[6] key 2400, slips 2000, 40000, 49 | E[N] = 20, Var(N) = 100; independence of fills and count stated | correct | script |
| rev5 | items[7] key 40, slips 20, 8, 10 | r(1−p)/p² | correct | script |
| rev5 | items[8].prose | fees "independent of N"; independence between the fees unsaid | imprecise | E[N]Var(X) needs the fees uncorrelated with each other. Finding 8 |
| rev5 | items[8] key 128, slips 20, 108, 80 | 4×5 + 12×9; geometric mean 4, variance 12 | correct | script |
| rev5 | items[9] keys a, b, c + whys | Jensen directions for exp, ln, x², 1/x, √ | correct | script `l19 s7` |
| hw4 | items[0] keys 0.9, 0.6, 0.3, 0.0952 | row and column conditionals | correct | script |
| hw4 | items[0].explain | most volume earns the tighter spreads | correct | 0.57/0.63 of fills at 1 or 2 ticks |
| hw4 | items[1] key 0.18, slips 0.12, 0.3 | c = 0.6×0.3; rows proportional (1.5 times) | correct | script |
| hw4 | items[2] keys a, c + whys, explain | independence ⇒ zero covariance and flat conditional mean; neither converse; margins do not fix cells | correct | BH 7.3, 9.3.2; script `hw4 3` |
| hw4 | items[3] key + whys, explain | E[B given A=a] = 0 for every a; E[B² given A] is 9 or 1 | correct | script |
| hw4 | items[4] key (1−p)/p, slips 1/p, p/(1−p) | failures before the first success | correct | BH 4.3 |
| hw4 | items[5] key 4, slips 6, 2, 3 | head then tail | correct | script; MC `hw4 5 MC HT wait 4` |
| hw4 | items[5].explain (equations) | E_H = 2, E = 2 + E/2 | correct | deriv |
| hw4 | items[5].explain (last sentence) | "Head then tail beats head then head" | misleading | in a race the two patterns are equally likely to come first; only the mean wait is shorter. MC `hw4 5 race HT v HH is even`. Finding 6 |
| hw4 | items[6] derivation | Adam's law from the joint pmf, finite sums, P(X=x) > 0 | correct | BH 9.1 |
| hw4 | items[7] key −85, slips −266.67, 140 | three regimes | correct | script |
| hw4 | items[8].model part 1 | E[N] = 1/p with each step justified, finiteness noted | correct | BH 4.3 |
| hw4 | items[8].model part 2, rubric | two states; a = 42, b = 36; a = 6 + b | correct | script exact and MC `hw4 8 MC two sixes 42` |
| hw5 | items[0] key 15, slips 12, 3, 20 | inside 12, between 3, overall mean 0 | correct | script |
| hw5 | items[1] derivation | Cov = −n p_i p_j; ρ free of n | correct | BH 7.4 |
| hw5 | items[2] key 3630, slips 750, 2880, 22500 | random sum; sd £60.25 | correct | script |
| hw5 | items[3] keys | ln concave; abs and x⁴ convex; Cauchy–Schwarz | correct | BH 10.1 |
| hw5 | items[4].prose | "Over 50 days, up has chance 0.4, down 0.35 and flat 0.25": independence of days unsaid | imprecise | the key −n p_i p_j assumes independent days. Finding 7 |
| hw5 | items[4] key −0.599, slips −7, 0.599, 0 | −7/√(12×11.375) | correct | script |
| hw5 | items[5] key 9, slips 7.5, 6.5, 11.5 | 4 + 2/0.4 | correct | MC `hw5 5 MC 9` |
| hw5 | items[5].explain | the past does not change future trials | correct | independence of trials |
| hw5 | items[6] code | simulation and exact; starter fails, solution passes 8 tests on fixed seeds | correct | script `hw5 6 code` |
| hw5 | items[6].explain | Var(N) = 400p(1−p); 23,200 at p = 0.2 | correct | script |
| hw5 | items[7].model step 1 | 1.012¹²⁰ ≈ 4.18 is the mean wealth, by independence | correct | script |
| hw5 | items[7].model step 2 (Jensen) | E[ln(1+R)] < ln 1.012 = 0.01193 | correct | script |
| hw5 | items[7].model step 2 (median) | "the typical (median) wealth is e^{120 E[ln(1+R)]}" | imprecise | the median of log wealth is only close to its mean (CLT, near symmetry). Finding 9 |
| hw5 | items[7].model steps 3, 4 | 0.955% a month; e^1.146 ≈ 3.1; roughly a quarter lower | correct | script |
| hw5 | items[7].model step 5 | a mixture hides a larger sd; usually fatter tails; extra tail lowers E[ln(1+R)] | correct | script `hw5 7 mixture with the same sd lowers E[ln(1+R)]`; hedged with "usually" |
| hw5 | items[7].rubric | six criteria match the model | correct | read against the model |
| hw5 | items[8] key mb + va², slips | random-sum variance in symbols | correct | BH 9.6 |
| p4 | items[0].prose | six cells of the van table | correct | script `p4 vans sum` |
| p4 | items[0].parts[0] key 0.38, slips 0.18, 0.2, 0.19 | column sum | correct | script |
| p4 | items[0].parts[1] key 0.2, slips 0.08, 0.57, 0.13 | 0.08/0.40; cell; 0.08/0.14; 0.08/0.60 | correct | script |
| p4 | items[0].parts[2] key + whys, explain | 0.36 against 0.288; zero covariance would not prove independence | correct | script |
| p4 | items[0].parts[3] key 0.9, slips 0.36, 0.5, 1 | conditional mean | correct | script |
| p4 | items[0].parts[4] key 3.96, slips 4.2, 8.4, 5.4, 2.66 | 6 × 0.66; column check | correct | script |
| p4 | items[1].parts[0] key 0.09, slips 0.6, 0.3 | independence stated | correct | script |
| p4 | items[1].parts[1] key 0.23, slips 0.14, 0.09, 0.74 | (2,0) or (1,1) | correct | script |
| p4 | items[1].parts[2] key 1.6087, slips 0.37, 0.7, 1.5 | 0.37/0.23 | correct | script |
| p4 | items[1].parts[3] key + explain | yes: P(Y=1 given S=2) = 0.39 against 0.3; a total of 2 is likelier when route 2 is late | correct | script `p4 1.3` |
| p4 | items[1].parts[3] option small why | "Any total that depends on Y moves its chances" | imprecise | S and Y are always dependent, but one seen value can leave Y's chances unchanged: two fair bits, S = 1. Script counterexample. Finding 10 |
| p4 | items[1].parts[3] options no-indep, no-never whys | S is built from Y as well as X | correct | Cov(Y, X+Y) = Var(Y) > 0 |
| p4 | items[1].parts[4] key 0.3913, slips | linearity given S | correct | script |
| p4 | items[2].parts[0] key 0.4286, slips 0.03, 0.15, 0.2 | 3/7 | correct | script |
| p4 | items[2].parts[1] key 0.55, slips 0.11, 1, 0.25 | young conditional mean | correct | script |
| p4 | items[2].parts[2] key 0.31, slips 0.4, 0.49, 0.22 | Adam's law; column check | correct | script |
| p4 | items[2].parts[3] key 480, slips 620, 1100, 300 | 1100 − 620 | correct | script |
| p4 | items[2].parts[4] key 120, slips 96, 480, 500 | 620 − 500; balance 0.2×480 = 0.8×120 | correct | script |
| p4 | items[3].parts[0] key 2+m + whys | first-step analysis, tries independent (stated) | correct | BH 9.1 |
| p4 | items[3].parts[1] key 4.2, five slips | m = 2.1 + 0.5m | correct | script; MC `p4 3 MC` |
| p4 | items[3].parts[2] key 7.4, slips | 3.2 + 4.2; check 0.5 + 0.5×7.4 = 4.2 | correct | script |
| p4 | items[3].parts[3] key 3.4929, slips; m_B = 2.7857 | 0.5 + 0.5(3.2 + m_B) | correct | script |
| p4 | items[3].parts[4] key 1.8, slips 3, 2.8, −2.4 | solve for m_B | correct | script |
| p5 | items[0].parts[0] key 31, slips 25, 19 | Adam's law | correct | script |
| p5 | items[0].parts[1] key 220, slips 31, 189, 43.6, 256 | Eve's law | correct | script |
| p5 | items[0].parts[2] key 46.5, slips | E[N]E[X], independence stated | correct | script |
| p5 | items[0].parts[3] key 502.75, slips 7.75, 337.75, 510.5, 77.5 | random-sum variance | correct | script |
| p5 | items[0].parts[4] key 0.9846, slips; explain | count share; most of it is the weather | correct | 189/220 |
| p5 | items[1].parts[0] key 42.5, slips | mean speed | correct | script |
| p5 | items[1].parts[1] key 16.94, slips | 12/42.5 hours | correct | script |
| p5 | items[1].parts[2] key 18, slips | mean time | correct | script |
| p5 | items[1].parts[3] key + whys | 1/v convex so E[12/V] ≥ 12/E[V]; agree only when V is fixed | correct | Jensen |
| p5 | items[1].parts[4] key 0.1445, slips 0.2617, 0.3633, 0.0938 | 37/256; no total equals 80, so strict and non-strict agree | correct | script, enumeration of 81 paths |
| p5 | items[1].parts[4].explain | about one day in seven | correct | 1/0.1445 = 6.9 |
| p5 | items[2].prose | chips independent given the line | correct | conditional independence stated |
| p5 | items[2].parts[0] key 0.02916, slips 0.0729, 0.0073 | negative binomial r = 2 | correct | script |
| p5 | items[2].parts[1] key 16, slips 14.29, 15, 8 | mixture of means; pooled p gives 14.29 | correct | script |
| p5 | items[2].parts[2] key 124, slips 140, 110, 62 | 180 and 40 | correct | script |
| p5 | items[2].parts[3] key 148, slips 124, 24, 128.8 | Eve's law | correct | script exact pmf `p5 2 exact` |
| p5 | items[2].parts[4] key 0.1622, slips | 24/148 | correct | script |
| p5 | items[3].prose | N independent of the multipliers | correct | hypothesis stated |
| p5 | items[3].parts[0] key −0.0527, slips 0.0488, 0.05, −0.0229 | ½ ln 0.9 | correct | script |
| p5 | items[3].parts[1] key −0.2108, slips | E[N]E[ln R] | correct | script |
| p5 | items[3].parts[2] key 0.8452, slips; Var(ln R) = 0.2099 | random-sum variance | correct | script |
| p5 | items[3].parts[3] key + whys | both hold; E[W] = 1.2184; ln E[W] = 0.1975 | correct | script |
| p5 | items[3].parts[4] key 0.6953, slips 0.3047, 0.6875, 0.6979 | 89/128 | correct | script |
| p5 | items[3].parts[4].explain | "So W < 1 exactly when at most half the rounds are up" | imprecise | true for N = 2, 4, 6 (script) but the pairing argument gives one direction only; false in general (N = 20, k = 11). Finding 11 |

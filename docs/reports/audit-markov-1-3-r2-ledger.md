# Claim ledger, round 2: markov levels 1 to 3

Auditor: blind Fable reader, round 2. Written before any earlier audit, review, ledger, concepts script or author report of this course was opened.

Scope: `app/content/courses/markov/` files `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l2-transition-matrix`. Stage 1, so full ledger depth.

Path shorthand: `s3` is `screens[3]`, `q1` is `quiz[1]`, `i2` is `items[2]`, `i2.p1` is `items[2].parts[1]`; `ex` is `explain.text`, `fb` is `feedback`, `bk.x` is `feedback.byKey.x`, `w.x` is the `widget.wrong` entry with id `x`, `opt.x` is the option with id `x` (its `why` included), `h` is the hints. A row that names several paths judges each of them; they share one basis.

Basis shorthand: **script** is a check in `docs/reports/markov-L1-3-concepts-r2.py` (exact fractions, exact dynamic programming, full enumeration or seeded Monte Carlo); **N** is Norris, *Markov Chains* (1997); **GS** is Grimmett and Stirzaker, *Probability and Random Processes*, 3rd ed.; **F** is Feller, *An Introduction to Probability Theory and Its Applications*, vol. 1, 3rd ed.; **KS** is Kemeny and Snell, *Finite Markov Chains* (1960); **Sh** is Shreve, *Stochastic Calculus for Finance I*.

Verdict counts are at the foot of the table.

| # | File | Path | Claim | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l1-only-now | s0 key, h, bk.R, bk.S, ex | From Rain the arrows are 0.2, 0.5, 0.3, so Cloudy is most likely; arrows from other states say nothing about tomorrow | correct | Read from the graph; N 1.1 |
| 2 | l1-only-now | s1 prose, canvas | Seeded path SRRSSCRCCCCCSSSC; days 2 and 7 are Rain, day 3 Rain, day 8 Cloudy, day 1 Sunny, day 6 Cloudy | correct | script: every move has positive chance; the days quoted match. The generator of this path is not in the engine, so "fixed seed" is taken on trust |
| 3 | l1-only-now | s1 key, opt.outcome, opt.day1, opt.all, ex | Both days were drawn from Rain's three arrows; outcomes differ, chances do not; older days add nothing | correct | Markov property, N 1.1 |
| 4 | l1-only-now | s2 prose | A Markov chain is a list of states with, for each, the chances of the next: transition probabilities | correct | N 1.1 (time-homogeneous chain) |
| 5 | l1-only-now | s2 key, w.into-rain, w.one-arrow, w.loop, bk, ex | Arrows out of a state add to 1, so 1 − 0.3 − 0.4 = 0.3; slips 0.6, 0.7, 0.4 named correctly; arrows into a state need not add to anything | correct | script; rows of a stochastic matrix |
| 6 | l1-only-now | s3 key, w, bk, ex | P(S, S given R) = 0.2 × 0.6 = 0.12; slips 0.8, 0.6, 0.2, 0.04 | correct | script; multiplication rule plus Markov property |
| 7 | l1-only-now | s4 key, opt, h, ex | A 3-cycle: 7 steps from Open is Closed; all arrows 1 is deterministic and still Markov; the smallest chain has one state with a loop of 1 | correct | 7 = 2 × 3 + 1; a degenerate stochastic matrix is still one |
| 8 | l1-only-now | s5 key, opt, bk, ex | With states Up and Down the two-day rule is not Markov: Up today leaves 0.7 or 0.4; averaging needs P(yesterday up), not given | correct | Second-order chain; GS 6.1 |
| 9 | l1-only-now | s6 prose, key, bk, ex | Pair state (yesterday, today) is Markov; from DU the chain moves to UU (0.4) or UD (0.6) | correct | State enlargement; table row Down, Up gives 0.4 |
| 10 | l1-only-now | s7 prose, key, opt, ex | P(X_{n+1} = j given X_n = i and the past) = p_ij, same arrows every day, rows add to 1; X_5 alone is enough for X_6 | correct | N 1.1, Theorem 1.1.1; homogeneity is stated ("the same on every day") |
| 11 | l1-only-now | s8 key, w, bk, ex | 0.3 × 0.6 × 0.35 = 0.063; slips 1.25, 0.35, 0.15, 0.105; Filled and Cancelled absorb | correct | script |
| 12 | l1-only-now | s9 prose, canvas, key, w, bk, ex | From Down, two ups: 0.45 × 0.6 = 0.27; slips 0.36, 0.2025, 0.33, 1.05; chart moves 1% a day | correct | script (series ratios are 1.01 or 0.99) |
| 13 | l1-only-now | summary ideas, formula, trap | Past adds nothing given the present; path chance is the product of arrows; enlarge the state when two histories ending in the same state disagree | correct | N 1.1 |
| 14 | l1-only-now | q0, q1 keys, w, bk, ex | 0.3 × 0.3 = 0.09 (slips 0.6, 0.3); 1 − 0.92 − 0.07 = 0.01 (slips 0.93, 0.08) | correct | script |
| 15 | l1-only-now | q2 key, opt, ex | A one-state chain has transition probability 1 | correct | Row sums to 1 |
| 16 | l1-only-now | q3 key, w, bk, ex | Dependence on the last three signs needs 2³ = 8 states; two arrows leave each triple | correct | script; state must carry the three signs when the eight chances differ |
| 17 | l2-transition-matrix | s0 key, bk, ex | p_ij = P(next = j given now = i): rows are today, columns tomorrow, rows add to 1 | correct | Row convention, N 1.1; stated at first use |
| 18 | l2-transition-matrix | s1 canvas, key, w, bk, ex | k-step bars from Rain; Sunny at k = 2 is 0.33; bars 0.33, 0.41, 0.26 add to 1 | correct | script: every bar within rounding of row Rain of P^k, k = 0 to 10 |
| 19 | l2-transition-matrix | s2 lines, order, bk, ex | P(X_2 = S given X_0 = R) = sum over m of p_Rm p_mS: split, multiplication rule, Markov property, numbers 0.12 + 0.15 + 0.06 | correct | Chapman–Kolmogorov, N Theorem 1.1.3; script |
| 20 | l2-transition-matrix | s3 prose, canvas, key, w, bk, ex | Entry (i, j) of P² is row i times column j; (P²)_SR = 0.18; slips 0.01, 0.06, 0.26, 0.1; squaring 0.1 "is no path"; rows of P² add to 1 | correct | script: P² matches the canvas matrix |
| 21 | l2-transition-matrix | s4 prose, key, w, bk, ex | pi_1 = pi_0 P with pi a row vector; Rain on Tuesday 0.16; slip 0.23 is P pi (column convention), 0.7 the unweighted column | correct | script; N 1.1 |
| 22 | l2-transition-matrix | s5 key, opt, ex | P^0 = I; P^m P^n = P^{m+n} holds at m = 0 | correct | Definition |
| 23 | l2-transition-matrix | s6 key, w, bk, ex | True two-step Sunny to Sunny is 0.47; squaring entries matches one path on the diagonal and none off it; squared row adds to 0.46 | correct | script |
| 24 | l2-transition-matrix | s7 prose, key, opt, ex | (P^k)_ij are the k-step chances; pi_k = pi_0 P^k; P^{m+n} = P^m P^n is the Chapman–Kolmogorov equation; P^5 pi_0 is the column convention | correct | N Theorem 1.1.3 |
| 25 | l2-transition-matrix | s8 key, w.three-times, w.no-migration, w.two-years, bk, ex | (P³)_AD = 0.051895; row A of P² is (0.8145, 0.1575, 0.028); slips 0.03, 0.0297, 0.028; the B route 0.01575 is nearly twice the A route 0.008145 | correct | script |
| 26 | l2-transition-matrix | s8 w.cubed, bk.cubed | Cubing 0.01 "keeps the impossible path D, D, D from A" | imprecise | 0.01³ is the chance of no path from A (script, finding 2). The line means "no real path" but says a path is kept |
| 27 | l2-transition-matrix | s9 code, tests, fb, ex | `step` is pi P, `after` applies it k times; five days from Normal gives (0.4288, 0.4123, 0.1589); k = 0 returns the start | correct | script: solution passes 8 tests, starter fails; values recomputed |
| 28 | l2-transition-matrix | summary ideas, formula, note, trap | k steps is P^k, zero steps I; with columns adding to 1 write M^k s_0 | correct | Transpose convention |
| 29 | l2-transition-matrix | q0 key, w, ex | (P²)_bear,bull = 0.2(0.9) + 0.8(0.2) = 0.34; slips 0.04, 0.18, 0.16 | correct | script |
| 30 | l2-transition-matrix | q0 bk.squared | "You squared 0.2. That keeps one path" | wrong | The two paths have chances 0.18 and 0.16; 0.04 is the chance of neither (script, fails on purpose; finding 1). The lesson's own trap says an off-diagonal square matches no path |
| 31 | l2-transition-matrix | q0 bk.one-path, bk.other | 0.18 is bear, bull, bull; 0.16 is bear, bear, bull | correct | script |
| 32 | l2-transition-matrix | q1 key, w, bk, ex | pi_1 bull = 0.55; slip 0.5 uses the bull row, 1.1 the unweighted column, 0.45 the bull part | correct | script |
| 33 | l2-transition-matrix | q2 key, opt, ex | With M = P transposed and column vectors, s_1 = M s_0; products do not commute | correct | Transpose of pi_1 = pi_0 P |
| 34 | l2-transition-matrix | q3 key, opt.sum, opt.pow6, ex | P² P³ gives the 5-step chances; P² + P³ has rows adding to 2; (P²)³ = P⁶ | correct | Chapman–Kolmogorov |
| 35 | l2-transition-matrix | q3 opt.entry why | Entry by entry "keeps one route through the middle" | imprecise | True on the diagonal only (route through m = i); off it the product equals no route term (script; finding 2) |
| 36 | fluency-l2-transition-matrix | families[0] key, wrong, solution | Two-state two-step key is sum over the middle state; slip is the squared entry or the one-step entry, each guarded by `when` | correct | script: 1,788-check course script passes; formula read as (P²)_ij |
| 37 | fluency-l2-transition-matrix | families[1] key, wrong, solution | Row Sunny times column j; all picked rows add to 1 | correct | script |
| 38 | fluency-l2-transition-matrix | families[2] key, wrong, solution | pi_1 entry is u p_0j + v p_1j; slips are the bull row alone and the unweighted column | correct | script |
| 39 | l3-never-leave | s0 key, bk, ex | A state with p_ii = 1 is absorbing; C is the only one; B has no loop | correct | N 1.3 |
| 40 | l3-never-leave | s1 canvas, key, opt, ex | Bars are row A of P^k; by k = 20 about 0.43 in C and 0.57 in D and E; A and B about 0.001 each | correct | script: all 105 bars; absorption at C is 3/7 |
| 41 | l3-never-leave | s2 key, w, bk, ex | f_A = 0.5 + 0.5 × 0.3 = 0.65; slips 0.5, 0.8, 1, 0.15; a state you may leave and never revisit is transient | correct | First-step split; N 1.5 |
| 42 | l3-never-leave | s3 prose, key, w.not-absorbing, bk, ex | Recurrent: returns with chance 1, otherwise transient; A and B transient; D, E and C recurrent | correct | N 1.5; closed finite classes are recurrent (N Theorem 1.5.6) |
| 43 | l3-never-leave | s3 fb.generic, h | "Transient when the chain can leave it for somewhere with no way back" | correct | True for finite chains, the setting here; s8 states the finite hypothesis |
| 44 | l3-never-leave | s4 prose, key, opt, ex | Communicating classes {A, B}, {C}, {D, E}; {D, E} closed; the transient states are the class that can leak | correct | N 1.2, 1.5 |
| 45 | l3-never-leave | s5 key, w, bk, ex | Ruin from £2 of £4: over within 4 bets with chance 0.75; one end 3/8; chances only grow | correct | script (P⁴) |
| 46 | l3-never-leave | s6 key, w, bk, ex | A loop of 0.95 is not absorbing; mean stay 1/0.05 = 20 months; Watch is transient | correct | Geometric mean; reaches Default |
| 47 | l3-never-leave | s7 key, opt, ex | Bull and bear: neither absorbing, both recurrent, one closed class; not every chain has an absorbing state | correct | N Theorem 1.5.6 |
| 48 | l3-never-leave | s8 prose, key, opt, ex | Absorbing p_ii = 1; transient f_i < 1; recurrent f_i = 1; i reaching a j that cannot reach back is transient; in a finite chain the converse holds | correct | N Theorem 1.5.3, 1.5.5, 1.5.6; the converse is given its finite hypothesis |
| 49 | l3-never-leave | s9 canvas, key, w, bk, ex | (P^k)_AD is cumulative because D absorbs; year 3 alone is 0.0519 − 0.0280 = 0.0239; yearly increments 0.010, 0.018, 0.024 | correct | script: five bars and the slips |
| 50 | l3-never-leave | summary ideas, formula, trap | In a finite chain a state is transient when it can reach a state that cannot reach it back | correct | N 1.5 |
| 51 | l3-never-leave | q0 key, opt, ex | Filled and Cancelled absorbing; every order ends in one; New and Partial transient | correct | Each transient state reaches an absorbing one, finite chain |
| 52 | l3-never-leave | q1, q2 keys, w, opt, ex | f_i = 0.7; the regime chain disproves "every chain gets stuck" | correct | script |
| 53 | l3-never-leave | q3 key, w, ex | 0.1111 − 0.0800 = 0.0311 | correct | script: exact 0.03105, inside the tolerance |
| 54 | l4-regimes | s0 key, opt, ex | Unbroken bull for 3 periods: 0.9³ = 0.729; (P³)_bull,bull = 0.781 counts returns; run survival is geometric | correct | script |
| 55 | l4-regimes | s1 prose, key, opt, ex | P(L = n) = p^{n−1}(1 − p); the mode is 1 for every p; mean 1/(1 − p) | correct | Geometric distribution on 1, 2, …; GS 3.5 |
| 56 | l4-regimes | s2 lines, order, ex | E[L] = (1 − p) × 1/(1 − p)² = 1/(1 − p) by differentiating the geometric series; bull 10 periods | correct | Power series differentiated inside its radius; script sums the series |
| 57 | l4-regimes | s3 key, w, bk, ex | Bear mean 5; slips 1.25, 10, 0.2; 0.8/0.2 = 4 counts the periods after the first | correct | p/(1 − p) is the mean of the count of extra periods |
| 58 | l4-regimes | s4 key, w, bk, ex | Long-run bull share 10/(10 + 5) = 2/3, the steady state (2/3, 1/3) | correct | Renewal-reward; script: stationary vector |
| 59 | l4-regimes | s5 key, opt, bk, ex | Exit chance is 0.1 whatever the run's age; 1 − 0.9^14 ≈ 0.77 is for a fresh run; expected time still to run is again 10 | correct | Memorylessness of the geometric; time to the first bear period has mean 10 |
| 60 | l4-regimes | s6 prose, canvas, key, w, bk, ex | P(bull at k given bull) − P(bull at k given bear) = 0.7^k; 0.7 is the second eigenvalue; first below 0.05 at k = 9 | correct | script for k = 0 to 12; Hamilton, *Time Series Analysis* 22.2 |
| 61 | l4-regimes | s7 prose, key, opt, ex | Two-state persistence p_11 + p_22 − 1; equal rows give independent draws and persistence 0; identity gives 1; matrix D gives −0.8 | correct | Trace minus 1; for two states equal rows is equivalent to persistence 0 |
| 62 | l4-regimes | s8 table, bk, ex | Counts UU 13, UD 2, DU 2, DD 2; estimates 13/15 and 2/4; divide by moves out, not periods | correct | script counts the 19 pairs; maximum-likelihood estimate, Hamilton 22.4 |
| 63 | l4-regimes | s9 prose, key, w, bk, ex | Positions £12.5m and £4m; expected next position from bear £5.7m; long run £9.67m; gap closes by 0.7 a period | correct | script |
| 64 | l4-regimes | s10 key, w, bk, ex | Counting this week, the drawdown is expected to last 1/0.15 = 6.67 weeks more; slips 2.67, 10.67, 0.15, 1.18; real P&L may have memory | correct | Memorylessness; script |
| 65 | l4-regimes | summary, formula, note, trap | E[L_i] = 1/(1 − p_ii); lambda_2 = 0 is independent draws; p_ii is not the share of time | correct | As rows 55 to 61 |
| 66 | l4-regimes | q0 to q3 keys, w, bk, ex | 20 days (slips 1.0526, 19); persistence 0.4 (slips 1.4, 0.48, 0.2), eigenvalues add to the trace; bull share 0.75; p_bull,bull is a one-step conditional chance | correct | script |
| 67 | review-1 | i0 key, opt, ex | Only the rating chain is Markov in its stated states | correct | Definition |
| 68 | review-1 | i1, i2 keys, w, bk | Missing entry 0.6 (slips 0.8, 0.85); bull next 0.34 (slips 0.26, 1.1, 0.2) | correct | script |
| 69 | review-1 | i3 key, w, bk.squared, ex | (P²)_CR = 0.24; 0.3² = 0.09 "is only the path that rains tomorrow and the day after" | correct | script: here p_CR p_RR = 0.3 × 0.3, so the square is that path |
| 70 | review-1 | i4 key, opt, ex | Only state 3 is transient; {1, 2} closed, 4 absorbing | correct | N 1.5 |
| 71 | review-1 | i5, i6 keys, w, bk | Over within 2 bets 0.75; mean 4 days (slips 4/3, 3) | correct | script |
| 72 | review-1 | i7 key, opt, ex | Exit chance 0.1; 1 − 0.9^10 ≈ 0.65 | correct | script |
| 73 | review-1 | i8 key, w, bk, ex | p-hat = 15/25, mean run 2.5 days; about 10 Stressed runs | correct | script |
| 74 | homework-1 | i0 key, w, bk, ex | 8 forced zeros in the pair-state matrix | correct | Two successors per pair |
| 75 | homework-1 | i1 key, w, bk, ex | (P²)_BB = 0.61; slips 0.49 (path B, B, B), 0.7, 0.58; above the long-run share | correct | script: pi_B = 4/7 |
| 76 | homework-1 | i2 table, bk, ex | pi_1 = (0.49, 0.385, 0.125); pi_2 = (0.4815, 0.3805, 0.138) | correct | script |
| 77 | homework-1 | i3 table, bk, ex | From B: 0.15, 0.2655, 0.356475, and 0.090975 during year 3 | correct | script |
| 78 | homework-1 | i4 key, opt, ex | Recurrent: 3, 4, 5; classes {1, 2}, {3}, {4, 5} | correct | N 1.5 |
| 79 | homework-1 | i5 key, w, bk, ex | h = 0.3 + 0.2h = 0.375; f_1 = 0.6 + 0.4h = 0.75; slip 0.72 | correct | script |
| 80 | homework-1 | i6 lines, order, ex | E[L] = 1 + p E[L], so 1/(1 − p), with p < 1 | correct | First-step analysis; total expectation |
| 81 | homework-1 | i7 key, w, bk, ex | lambda_2 = a + b − 1; determinant ab − (1 − a)(1 − b) equals it too | correct | Algebra |
| 82 | homework-1 | i8 code, tests, ex | Count adjacent pairs, divide by moves out | correct | script: solution passes 6 tests, starter fails |
| 83 | homework-1 | i9 model (a) to (c), rubric | P-hat = ((0.95, 0.05), (0.15, 0.85)); durations 20 and 6.67; Calm share 0.75 against 200/261 | correct | script; 260 moves, 200 from Calm |
| 84 | homework-1 | i9 model (d), (e), rubric | lambda_2 = 0.8; P(Stressed at k given Stressed) = 0.25 + 0.75 × 0.8^k = 0.5572 at k = 4; positions £24m, £8m; £15.08m | correct | script |
| 85 | homework-1 | i9 model (f), rubric | Memoryless model; 1/(1 − p) is steep near 1; few Stressed runs | correct | Interpretation; derivative 1/(1 − p)² |
| 86 | problems-1 | i0.p0 to p3 keys, w, bk, ex | p-hat_TT = 0.7; (P²)_TT = 0.535; mean Thin spell 3.33; Thin share 1/3; every slip value | correct | script |
| 87 | problems-1 | i1.p0 to p3 keys, w, bk, ex | 0.0216; 0.18; 0.306; stop exactly on trade 4 is 0.1098; (P⁴)_WS = 0.4158 | correct | script |
| 88 | problems-1 | i2.p0, p1 keys, w, bk, ex | Healthy at least once in two days 0.65 (not (P²)_MH = 0.6); ever Healthy again 5/7 | correct | script |
| 89 | problems-1 | i2.p2, p3 keys, w, opt, ex | f_H = 34/35; H and M transient, liquidated with chance 1; 2/7 is one call ending in X | correct | script; finite chain, X the only closed class |
| 90 | problems-1 | i3.p0 to p2 keys, w, bk, ex | Stressed spell 3.33 months; calm share 6/7; long-run £10/7m a month | correct | script |
| 91 | problems-1 | i3.p3, p4 keys, w, bk, ex | From stressed −£4.7m; rule "on only after calm" earns 6/7 × 2.45 = £2.1m, beating £1.43m by 4.7/7 | correct | script; stationary weighting of the next month's conditional mean |
| 92 | l5-where-it-settles | s0 canvas, key, opt, ex | P(bull after k) is 2/3 + 0.7^k/3 from bull and 2/3 − 2 × 0.7^k/3 from bear; both reach 0.667 | correct | script |
| 93 | l5-where-it-settles | s1 table, bk, ex | (2/3, 1/3) P = (2/3, 1/3); a distribution with pi P = pi is stationary | correct | N 1.7 |
| 94 | l5-where-it-settles | s2 key, w, bk, ex | 0.95x + 0.15(1 − x) = x gives 0.75; flow out equals flow in; slips 0.5, 0.25, 3, 0.95 | correct | script |
| 95 | l5-where-it-settles | s3 table, h, bk, ex | pi_M = 2.5 pi_L, pi_H = 1.5 pi_L, pi = (0.2, 0.5, 0.3); column M then holds | correct | script |
| 96 | l5-where-it-settles | s4 key, opt, h | For Perf and Def the stationary distribution is (0, 1); 0.97^100 ≈ 0.048 | correct | script |
| 97 | l5-where-it-settles | s4 ex | "an absorbing state takes all the long-run mass" | imprecise | True when that state is the only closed class, as here; with two absorbing states (l3 s5, l8) each takes a share. Finding 4 |
| 98 | l5-where-it-settles | s5 key, opt, bk, ex | P v = v is solved by (1, 1, 1) for every row-stochastic P; the share solves pi P = pi and is 0.3; 0.577 is 1/√3 | correct | Rows add to 1; script |
| 99 | l5-where-it-settles | s6 prose, lines, order, ex | For a + b > 0, pi_1 = b/(a + b), pi_2 = a/(a + b); without normalising any multiple solves pi P = pi | correct | N Example 1.7.3; the hypothesis a + b > 0 is stated |
| 100 | l5-where-it-settles | s7 code, tests, ex | Share of bull days converges to 2/3; seeds 1, 2, 7 give 0.666255, 0.668935, 0.66784 | correct | script: values reproduced digit for digit; ergodic theorem N 1.10 |
| 101 | l5-where-it-settles | s8 prose, key, w, bk, ex | Long-run mean return is the sum of pi_i mu_i = 0.33% a month; slips −0.5%, 1.5%, −1.33% | correct | script; ergodic theorem for a function of the state |
| 102 | l5-where-it-settles | summary ideas, formula, note, trap | pi P = pi with the normalising equation; the regime chain settles at pi from any start; pi_i is the share of time | correct | N 1.7, 1.8, 1.10 for this irreducible aperiodic chain |
| 103 | l5-where-it-settles | q0 to q3 keys, w, opt, ex | Trending 1/3; (1/2, 1/2) moves to 0.55; £150m; add the normalising equation | correct | script |
| 104 | l6-always-settle | s0 canvas, key, opt, ex | Swap chain: P^k is I for even k and P for odd k and never converges; a 0.5 start never moves | correct | P² = I |
| 105 | l6-always-settle | s1 canvas, key, w, ex | Share of days at A tends to 1/2; (1/2, 1/2) is stationary; period 2; a periodic chain still has a stationary pi read as a share of time | correct | N 1.8, 1.10 (irreducible finite chain) |
| 106 | l6-always-settle | s2 canvas, key, opt, ex | With a 0.1 self-loop P(at A) = 0.5 + 0.5(−0.8)^k; 0.506 at k = 20; aperiodic | correct | script |
| 107 | l6-always-settle | s3 key, opt, ex | Ring of 3: X_100 = B; period 3; pi = (1/3, 1/3, 1/3) | correct | 100 = 99 + 1 |
| 108 | l6-always-settle | s4 key, w, bk, ex | From A only A and B are reachable; {A, B} and {C, D} are closed classes; the chain is reducible | correct | N 1.2 |
| 109 | l6-always-settle | s5 prose, key, w, bk, ex | Inside {A, B} pi is (1/3, 2/3), inside {C, D} (1/2, 1/2); from E the long-run chance at B is 1/3; from A 2/3, from C 0 | correct | script: P^200 |
| 110 | l6-always-settle | s6 key, opt, bk, ex | (1/6, 1/3, 1/4, 1/4, 0) is one stationary distribution among many; among starting states it is the limit only from E; two closed classes give many | correct | script |
| 111 | l6-always-settle | s7 prose, key, opt, ex | Irreducible: every state reaches every other; aperiodic: returns not locked to multiples of d > 1; a finite chain that is both has a unique pi and pi_0 P^k tends to pi | correct | N Theorem 1.8.3 with 1.7.7; both conditions and finiteness stated |
| 112 | l6-always-settle | s8 lines, order, ex | P^{2m} = I, P^{2m+1} = P; the average (I + P)/2 has rows (1/2, 1/2) | correct | Algebra |
| 113 | l6-always-settle | s9 table, bk, ex | Long, Flat, Short rule: pi = (1/4, 1/2, 1/4); Flat on day 100 with chance 1, on day 101 with chance 0 | correct | script |
| 114 | l6-always-settle | summary ideas, formula, note, trap | Two or more closed classes give many stationary distributions; one closed class gives one pi even if reducible; irreducible alone gives a unique pi as a share of time | correct | N 1.7, 1.8; finite chains |
| 115 | l6-always-settle | summary ideas[2] | "A self-loop breaks a period" | correct | In an irreducible chain one state of period 1 makes all aperiodic (N Lemma 1.8.2); the sentence sits with the irreducible theorem |
| 116 | l6-always-settle | q0 to q3 keys, w, opt, ex | Swap has stationary (1/2, 1/2); two closed classes; pi_1 = 5/9; ring of 4 is at C at step 10 | correct | script |
| 117 | l7-how-long | s0 canvas, key, opt, ex | Walk on 0 to 3 from 1: still moving with chance (1/2)^k | correct | Derive formulas checked by hand for k = 1, 2, 3 |
| 118 | l7-how-long | s1 key, w, bk, ex | E[T] = 1/p = 2; the shortcut needs the same exit chance in every state | correct | script (linear system) |
| 119 | l7-how-long | s2 lines, order, ex | t_1 = 1 + t_0/2 + t_2/2 with t_0 = t_3 = 0 gives 2 | correct | N 1.3, Theorem 1.3.5 |
| 120 | l7-how-long | s3 table, ex | Walk on 0 to 4: t = (3, 4, 3) = i(4 − i) | correct | script |
| 121 | l7-how-long | s4 table, bk, ex | t_IG = 30, t_HY = 25; naive 100 and 20 | correct | script |
| 122 | l7-how-long | s5 key, opt, ex | t_X = 0, t_A = 2, t_C infinite: the equations have no finite solution | correct | C never reaches X |
| 123 | l7-how-long | s6 key, opt, ex | Lazy walk t_1 = 4; dropping the +1 gives 0; t = 1 at the ends gives 5 | correct | script |
| 124 | l7-how-long | s7 prose, key, opt, ex | t = 1 + Qt, so (I − Q)t = 1; the absorbing rows of (I − P)t = 1 say 0 = 1 | correct | KS 3.3 |
| 125 | l7-how-long | s8 key, w, bk, ex | t_F = 2, t_B = 4; 2.5 is the mean stay at the back; three quarters of orders reach the front | correct | script |
| 126 | l7-how-long | summary, q0 to q3 | A state that cannot reach absorption has infinite expected time; keys 5, 0, missing +1, 3 | correct | script |
| 127 | l8-which-end | s0 canvas, key, opt, ex | From 2 the walk ends at 3 with chance 2/3; (1/2)^12 ≈ 0.0002 still moving | correct | script |
| 128 | l8-which-end | s1 key, opt, ex | h_1 = h_0/2 + h_2/2 with h_3 = 1, h_0 = 0; no +1 | correct | N Theorem 1.3.2 |
| 129 | l8-which-end | s2 lines, order, ex | h_2 = 2/3, h_1 = 1/3; for a fair walk the distance from the bottom over the width | correct | script |
| 130 | l8-which-end | s3 table, ex | Up 2/3, down 1/3: h_1 = 4/7, h_2 = 6/7 | correct | script |
| 131 | l8-which-end | s4 prose, canvas, table, ex | H = (I − Q)^{−1} R; inverse ((1.5, 0.25), (0.5, 1.75)); det 0.4; H = ((0.8, 0.2), (0.6, 0.4)); rows add to 1 | correct | script; KS 3.3 |
| 132 | l8-which-end | s5 key, opt, ex | One absorbing state reachable from every other: h = 1; h_i = 1 solves the equations since rows add to 1 | correct | Finite chain; N 1.3 |
| 133 | l8-which-end | s6 key, opt, bk, ex | Both boundary values 1 measures absorption anywhere; correct h = (1/4, 1/2, 3/4) | correct | script |
| 134 | l8-which-end | s7 prose, key, opt, ex | h_i = sum of P_ij h_j, h_A = 1, h_B = 0; (I − Q)h = r; g_i = 1 − h_i | correct | N 1.3 |
| 135 | l8-which-end | s8 table, ex | h_F = 0.8, h_B = 0.6; 40% of back orders cancelled | correct | script |
| 136 | l8-which-end | summary, q0 to q3 | Keys 0.75, 0.6 (slip 2.6 from a +1), 1, 0.2 with H = 2R | correct | script |
| 137 | review-2 | i0, i1 keys, w, bk, ex | Calm share 0.25; pi = (0.4, 0.4, 0.2), mean spread 1.8 ticks; 1.9 uses the middle row | correct | script |
| 138 | review-2 | i2 key, opt, ex | The three irreducible chains with a self-loop converge; the swap is periodic, the identity reducible; third chain reaches (1/3, 2/3) | correct | N Theorem 1.8.3; script |
| 139 | review-2 | i3 key, w, bk, ex | From 4, the chance of ending in {1, 2} is 0.4 | correct | h = 0.5h + 0.2 |
| 140 | review-2 | i4 to i7 keys, w, bk, ex | t_2 = 6 on 0 to 5; t_B = 2.25; repaid 0.8; down-drift h_2 = 3/7, h_1 = 1/7 | correct | script |
| 141 | homework-2 | i0, i1 table, key, w, ex | pi = (0.5, 0.3, 0.2); long-run return 0.2% (slips −0.67%, 1%) | correct | script |
| 142 | homework-2 | i2 key, w, ex | pi_1 = b/(a + b) for a + b > 0; b/a is the ratio pi_1/pi_2 | correct | As row 99 |
| 143 | homework-2 | i3 key, opt, ex | Two closed classes, one periodic; (1/2, 1/2, 0, 0) stationary; joins the pair with chance 1/2; P(X_k = 1) alternates near 1/6 and 1/3 | correct | script: P^200 and P^201 |
| 144 | homework-2 | i4 table, bk, ex | Up-drift walk: t_1 = 15/7, t_2 = 12/7 | correct | script |
| 145 | homework-2 | i5 lines, order, ex | H = R + QH, so H = (I − Q)^{−1} R, the inverse existing when every transient state can reach absorption; t = (I − Q)^{−1} 1 | correct | KS Theorem 3.2.1 |
| 146 | homework-2 | i6 model 1 to 4, rubric | t = (6, 5); h = (0.6, 0.5); (I − Q)^{−1} = ((5, 1), (2.5, 2.5)), its entries expected years in each rating | correct | script; KS 3.2 |
| 147 | homework-2 | i6 model 5, rubric | Expected loss £1.76m; B loans end sooner but more often in default | correct | script |
| 148 | homework-2 | i7 key, w, bk, ex | HTH takes 10 days on average; t_H = 8, t_HT = 6; 8 would be 1/P(HTH) for independent trials; HH takes 6 | correct | script; GS 5.12 on pattern waits |
| 149 | homework-2 | i7 ex | "mulberry32 generator and seed 7, 200,000 simulated runs average 9.995" | correct | script reproduces 9.995 with heads when u < 0.5 |
| 150 | homework-2 | i8 prose, code, tests, bk, ex | Absorbing when P[i][i] is 1; if every other state can reach one the chain is absorbed with chance 1; H = (I − Q)^{−1} R; from deuce 9/13 after 50/13 points | correct | script: solution passes 12 tests, starter fails; tennis values p²/(p² + q²) and 2/(1 − 2pq) |
| 151 | problems-2 | i0.p0 to p2 keys, w, bk, ex | (P²)_IA = 0.14; pi_B = 0.2 pi_I; pi_I = 20/29; pi = (4, 20, 5)/29 | correct | script |
| 152 | problems-2 | i0.p3 key, opt, ex | Irreducible with self-loops, so pi_0 P^60 is close to pi from every start; "share only" holds for a periodic chain | correct | script: P^60 within 1e−4 of pi; N Theorem 1.8.3 |
| 153 | problems-2 | i0.p4 key, w, bk, ex | Long-run P&L 7/29 ≈ £0.24k a day | correct | script |
| 154 | problems-2 | i1.p0 to p3 keys, w, bk, ex | On in two weeks 0.42; live On share 0.8; ever live 0.6; far-ahead chance of On 0.48, depending on the start | correct | script: P^300 |
| 155 | problems-2 | i2.p0 to p3 keys, w, bk, ex | h_C = 0.2 + 0.5q; q = 0.6; t_Q = 1.75, t_C = 1.875; tighter quote q = 0.6588 | correct | script |
| 156 | problems-2 | i2.p4 key, opt, ex | £30 against £26.35 a request; the tighter quote ends in about 1.53 rounds | correct | script |
| 157 | problems-2 | i3.p0 to p2 keys, w, bk, ex | h_R = 0.625; h_A = 0.575; t_A = 3.5 months | correct | script |
| 158 | problems-2 | i3.p3, p4 keys, w, bk, ex | Expected value £8.30; break-even price £8.23 = 8.30 − 0.02 E[T], named as the price with expected profit 0 | correct | script; linearity of expectation for the cost |
| 159 | l9-coin-flip-walk | s0 prose, canvas, key, w, bk, ex | Seeded 10-toss path ends at 2; U + D = 10 and U − D = 2 give 6 ups | correct | script: seed 43 reproduced from the engine generator, ends at 2 |
| 160 | l9-coin-flip-walk | s1 key, opt, h, ex | Four times the steps gives about twice the spread; ±2√n holds about 95% of endpoints; the range grows like n | correct | Var(S_n) = n; normal approximation |
| 161 | l9-coin-flip-walk | s2 prose, key, w, bk, ex | Simple random walk: independent ±1 steps, up with probability p; mean of S_100 at p = 0.6 is 20; slips 60, 10, 0.2; drift is the slope | correct | F ch. III; script and Monte Carlo |
| 162 | l9-coin-flip-walk | s3 key, w, h, bk, ex | sd of S_100 is 10; "variances of independent steps add" | correct | Independence used as a sufficient condition |
| 163 | l9-coin-flip-walk | s4 key, w, bk, ex | sd √96 ≈ 9.80; p(1 − p) = 0.24 is the 0-or-1 coin, 4 times smaller | correct | script |
| 164 | l9-coin-flip-walk | s5 key, w, bk, ex | p = 1 gives variance 0; slips 50, 200, 12.5 | correct | script; 12.5 is np(1 − p) at p = 0.5 |
| 165 | l9-coin-flip-walk | s6 lines, order, ex | E[S_n] = n(2p − 1) by linearity; Var(S_n) = 4np(1 − p); independence makes covariances zero "though uncorrelated steps would be enough" | correct | Algebra; independence is correctly marked sufficient, not necessary |
| 166 | l9-coin-flip-walk | s7 prose, key, w, bk, ex | S_20 = 2K − 20 with K binomial; P(S_20 = 4) = 125970/2^20 ≈ 0.1201; slips 0.0046, 0.0370; near normal by the CLT | correct | script; de Moivre–Laplace |
| 167 | l9-coin-flip-walk | s8 prose, canvas | Seeded walk sits at 10 after 100 steps and has not been below 0 since step 1 | correct | script: seed 61 reproduced, ends at 10, minimum after the start is 0 or more |
| 168 | l9-coin-flip-walk | s8 key, opt, bk, ex | E[S_200 given S_100 = 10] = 10; no pull to 0; about 7 returns in 100 steps | correct | Independent increments; script: expected returns 7.04 |
| 169 | l9-coin-flip-walk | s9 prose, key, w, bk, ex | Mean £40, sd √998.4 ≈ £31.6; 1.27 sd above zero; about one run in ten loses | correct | script: exact binomial P(S < 0) = 0.097 |
| 170 | l9-coin-flip-walk | summary ideas, formula, note, trap | "Independence gives the variance"; endpoint 2K − n; no pull back | correct | Sufficient-condition wording; s6 gives the weaker condition |
| 171 | l9-coin-flip-walk | q0, q1 keys, opt, w, ex | Endpoint parity matches the number of steps; Var(S_40) = 30 at p = 0.25 | correct | script |
| 172 | l9-coin-flip-walk | q2 key, w, bk, ex | P(down) ≈ Phi(−1.27) ≈ 0.10; exact binomial 0.097 | correct | script |
| 173 | l9-coin-flip-walk | q3 prose, key, opt, ex | About 7 returns in 100 steps and 79 in 10,000; returns grow like √n; a fair walk returns with probability 1 | correct | script: 7.04 and 78.8; recurrence of the simple symmetric walk, F III.2 and XIV.7 |
| 174 | l10-gamblers-ruin | s0 canvas, h, fb, ex | In the seeded batch 9 of 30 games reach £10 | correct | script: seed 11 reproduced, 9 reach £10 |
| 175 | l10-gamblers-ruin | s0 key, opt, ex | From £3 of £10 with fair bets the chance is 3/10; the nearer end is likelier | correct | F XIV.2 |
| 176 | l10-gamblers-ruin | s1 key, opt, ex | Games from the middle last longest; "25 bets on average from £5, against 7 from £1" in this batch | correct | script: seed 6 reproduced (means round to 25 and 7; theory 25 and 9) |
| 177 | l10-gamblers-ruin | s2 lines, order, ex | P_i = (P_{i+1} + P_{i−1})/2, equal gaps, P_i = i/N | correct | F XIV.2; script checks the formula against the linear system |
| 178 | l10-gamblers-ruin | s3 prose, key, w, bk, ex | D_i = 1 + (D_{i+1} + D_{i−1})/2, D_0 = D_N = 0, solution i(N − i); 2500 from £50 of £100; "this batch averaged 2,398" | correct | F XIV.3; script (system and seed 28 reproduced) |
| 179 | l10-gamblers-ruin | s4 prose, key, w, h, bk | P_i = (1 − r^i)/(1 − r^N), r = (1 − p)/p; 0.1192 at p = 0.49; r^50 ≈ 7.39, r^100 ≈ 54.6; 0.8808 for p = 0.51 | correct | F XIV.2 (2.4); script |
| 180 | l10-gamblers-ruin | s4 ex; s5 opt.small why; summary.trap | "the game lasts thousands of bets"; "Over thousands of bets"; "repeated thousands of times" | imprecise | The expected length is (50 − 100 P_50)/(q − p) = 1,904 bets (F XIV.3 (3.4); script). Finding 7 |
| 181 | l10-gamblers-ruin | s5 key, opt, bk, ex | One £50 bet gives 0.49 against 0.1192; £10 bets give 0.450; at p = 0.51 small bets give 0.8808 against 0.51; bet big when the odds are against you, small when for you | correct | script; Dubins and Savage, *How to Gamble If You Must*, bold play in subfair red-and-black |
| 182 | l10-gamblers-ruin | s6 prose, key, opt, fb, ex | As N grows ruin is certain for p ≤ 1/2; for p > 1/2 the ruin chance is r^i | correct | F XIV.2 |
| 183 | l10-gamblers-ruin | s7 key, w, h, bk, ex | i = 20, N = 40, p = 0.49: 0.31; loses the stake about 69% of the time | correct | script |
| 184 | l10-gamblers-ruin | s8 key, w, bk, ex | Limits ±10: 100 trades on average; ±20 would give 400; "these 20 paths averaged 102" | correct | script (seed 8 reproduced) |
| 185 | l10-gamblers-ruin | summary ideas, formula, note | Fair odds i/N, length i(N − i); with an edge the r formula; endless money ruins p ≤ 1/2 | correct | As rows 177 to 182 |
| 186 | l10-gamblers-ruin | q0 to q2 keys, w, opt, ex | P_N = 1 and D_N = 0; D_2 = 12 with N = 8; 9/13 at p = 0.6 (slip 4/13) | correct | script |
| 187 | l10-gamblers-ruin | q3 key, opt, ex | Proportional staking never reaches exactly 0; fixed stakes are a walk with an absorbing barrier | correct | Product of positive factors |
| 188 | l11-reflection | s0 key, w, bk, ex | 15 paths to (6, 2); a path to (n, k) has (n + k)/2 ups | correct | script |
| 189 | l11-reflection | s1 key, bk, ex | First touch of level 2 at step 4; the flipped path ends at (8, 4) | correct | Read from the segments |
| 190 | l11-reflection | s2 key, opt, ex | Reflecting after the first touch of m sends an end k < m to 2m − k | correct | F III.1 |
| 191 | l11-reflection | s3 prose, key, w, bk | Paths to (8, 0) touching 2 pair one for one with paths to (8, 4): 28 of 70 | correct | script: full enumeration |
| 192 | l11-reflection | s3 ex | "For an end at or below the level, k ≤ m": the count is C(n, (n + 2m − k)/2) | imprecise | Holds for a level at or above the start, m ≥ 0. For a level below the start, m < 0, every path ending at k < m passes m, and the formula miscounts (n = 4, m = −2, k = −4: 1 path, formula gives C(4, 2) = 6). Finding 5 |
| 193 | l11-reflection | s4 key, w, bk, ex | Every path to (8, 2) touches 2: 56; with k = m the mirror end is the same point | correct | script |
| 194 | l11-reflection | s5 key, w, h, bk, ex | 130 of 256 paths reach 2: 93 end at 2 or above, 37 fall back, matching the paths ending above 2; P(max ≥ 2) ≈ 0.508 | correct | script: enumeration |
| 195 | l11-reflection | s6 prose, lines, order, ex | For a fair walk and m > 0: P(max_{j ≤ n} S_j ≥ m) = P(S_n ≥ m) + P(S_n > m); needs fair steps | correct | F III.1 and III.7; script for six (n, m) pairs; non-strict then strict, as it should be |
| 196 | l11-reflection | s7 key, w, bk, ex | n = 4, m = 2: 5/16 + 1/16 = 0.375; six walks reach 2, one of them up-up-down-down | correct | script |
| 197 | l11-reflection | s8 prose, key, w, h, bk, ex | 6 wins and 4 losses: 126 − 84 = 42 orders stay above 0; chance (a − b)/(a + b) = 0.2: the ballot theorem | correct | script: enumeration of the 210 orders; F III.1 |
| 198 | l11-reflection | s9 prose, key, w, h, bk, ex | P(min ≤ −4 within 20) = P(S_20 ≤ −4) + P(S_20 ≤ −6) = 0.2517 + 0.1316 = 0.3833; parity makes "< −4" mean "≤ −6" | correct | script: exact dynamic programme |
| 199 | l11-reflection | s9 fb.correct | "the 0.25 chance of ending beyond the limit" | imprecise | 0.2517 is the chance of ending at or beyond −£4k; strictly beyond is 0.1316 (script). Finding 6 |
| 200 | l11-reflection | summary ideas, formula, note, trap | Mirror rule for k < m; fair steps only | correct | F III.1 |
| 201 | l11-reflection | q0, q1 keys, w, opt, ex | 45 of 252 paths to (10, 0) touch 3; all 6 paths to (6, 4) touch 2 | correct | script |
| 202 | l11-reflection | q2 key, w, bk, ex | First reaches 2 at step 4 with chance 2/16; the hitting time theorem (m/n) P(S_n = m) agrees | correct | script; GS 3.10 (14) |
| 203 | l11-reflection | q3 key, w, bk, ex | Knock-out within 6 days at +2: 22/64 + 7/64 = 29/64 | correct | script |
| 204 | l12-price-paths | s0 canvas, key, h, bk.left, ex | Chart B moves exactly £1 a day; chart A has falls of over 6% on days 71 and 106 | correct | script: simple returns below −6% on days 71 and 106 only |
| 205 | l12-price-paths | s1 key, opt, ex | With sigma = 0 all paths are the line mu t | correct | Model definition |
| 206 | l12-price-paths | s2 prose, key, w, h, bk, ex | Log price as a walk with drift; independent daily returns, so the 250-day sd is 1% × √250 ≈ 15.81% and the mean 12.5% | correct | script; independence stated as an assumption of the model; log returns named |
| 207 | l12-price-paths | s3 prose, key, w, ex | i.i.d. daily returns with mean mu and sd sigma give ln P_n − ln P_0 ≈ N(n mu, n sigma²) for large n; P(negative year) ≈ 0.21 | correct | Lindeberg–Lévy CLT; script |
| 208 | l12-price-paths | s3 ex; w.daily | "One day alone is close to a coin flip: Phi(−0.05) ≈ 0.48" | imprecise | Uses a normal daily return, on the screen that says daily returns need not be normal; the CLT gives nothing for n = 1. Finding 8 |
| 209 | l12-price-paths | s4 prose, key, w, bk, ex | u = 1.25, d = 0.8: up, up, down gives £125; ud = 1 so only the number of ups matters; ln 1.25 = 0.2231 | correct | script; Sh 1.1 |
| 210 | l12-price-paths | s5 prose, key, w, h, bk, ex | Touching £195.31 is the log walk touching +3; exact chance 352/1024 = 0.34375; in the batch 13 of 40 touch; the bold path touches 3 on day 7 and ends at 0 | correct | script: exact value and seed 32 reproduced |
| 211 | l12-price-paths | s6 prose, code, tests, ex | Simulation estimate near 0.34375 and 0.26318; standard error about 0.003 | correct | script: solution passes 7 tests, starter fails; example value 0.34 |
| 212 | l12-price-paths | s6 ex; s9 question, ex; summary.ideas[1]; q3 prose | "the same code prices a walk with drift"; "fair price" of the one-touch; "reflection or simulation prices a barrier event" | imprecise | Pay-out times the modelled touch chance is the no-arbitrage price only when the modelled walk is itself a fair bet (s9: fair additive walk, no interest). With p = 0.55 the expected pay-out is £41.03 but the price stays £26.32 (script); Sh 1.1 to 1.2. problems-3 i1.p3 says this correctly. Finding 3 |
| 213 | l12-price-paths | s7 prose, canvas, key, opt, bk, ex | A fair walk rose from £100 to £140 in 200 days; expected change over the next 50 days is £0; a fitted line is not a drift | correct | script: seed 781 reproduced, ends at 140 |
| 214 | l12-price-paths | s8 key, opt, ex | Real returns show fat tails and volatility clustering; signs are close to uncorrelated; many-day returns look roughly normal; GARCH models add these | correct | Cont (2001), "Empirical properties of asset returns", facts 1, 2, 4, 6; Bollerslev (1986) |
| 215 | l12-price-paths | s8 canvas, h | The top panel is chart A's returns; first 40 days calm, later wild, a fall of 6.5% | correct | script: panel equals the log returns of chart A in %, −6.5 present |
| 216 | l12-price-paths | s9 key, w, h, bk | Touch chance 2 × 0.13159 = 0.26318, pay-out £26.32; in the batch 10 of 40 touch | correct | script: exact and seed 10 reproduced |
| 217 | l12-price-paths | s9 ex (last two sentences) | Higher volatility puts the barrier fewer steps away; drift breaks the symmetry reflection needs | correct | Hull, *Options, Futures and Other Derivatives*, barrier options; F III.1 |
| 218 | l12-price-paths | summary ideas[0], ideas[2], formula, trap | Mean n mu, sd sigma √n, roughly normal; fat tails and clustering; a line through one path is not a drift | correct | As rows 206, 207, 214 |
| 219 | l12-price-paths | q0 to q2 keys, w, ex | 10% log return with sigma = 0; 2% × √25 = 10%; 6 distinct prices after 5 days | correct | script |
| 220 | l12-price-paths | q3 key, opt, ex | With p = 0.55 a reflected path has a different probability; the count is right, the chances are not; tilt each path by its drift | correct | Probability ratio (q/p) to the power of the reflected rise; script confirms the tilted formula |
| 221 | review-3 | i0 to i3 keys, w, bk, ex | sd √396 ≈ 19.90; 30/120 = 0.25, mean 2700 bets; 220 of 792 paths; 1.5% × 4 = 6% | correct | script |
| 222 | review-3 | i4 key, w, bk, ex | Ruin against endless money at p = 0.51 from £20: (49/51)^20 ≈ 0.4493; certain only for p ≤ 1/2 | correct | script; F XIV.2 |
| 223 | review-3 | i5, i6 keys, w, bk, ex | P(S_10 = 0) = 252/1024; touch 4 within 12: 0.1938 + 0.0730 = 1093/4096 | correct | script |
| 224 | review-3 | i7, i8 keys, w, bk, ex | p = 0.55, £5 to £10 in £1 bets: 0.7317 against 0.55 bold; 3 ups and 1 down from £100 gives £144 | correct | script |
| 225 | homework-3 | i0, i1 keys, w, bk, ex | D_i = i(20 − i); Var(S_n) = 0.84n; the mean overtakes the sd after a few trades | correct | script; 0.4n > √(0.84n) once n > 5.25 |
| 226 | homework-3 | i2 lines, order, ex | Gaps grow by r = q/p; P_i = (1 − r^i)/(1 − r^N) for p ≠ 1/2; tends to i/N as p tends to 1/2 | correct | F XIV.2 |
| 227 | homework-3 | i3, i4 keys, w, bk, ex | 165 paths to (10, 2) never touch 4; P(T = 9) for level 3 is 28/512 | correct | script: enumeration and dynamic programme |
| 228 | homework-3 | i5 prose, key, w, fb, ex | Red wins with chance 18/37 at even money; 0.3680 with £1 bets against 0.486 bold; house edge 2.7% | correct | script; single-zero wheel has 18 red of 37 pockets, edge 1/37 |
| 229 | homework-3 | i6 code, tests, ex | Dynamic programme for any p; 0.4523 at p = 0.55 where reflection would give 0.5321 | correct | script: solution passes 9 tests, starter fails; both numbers recomputed |
| 230 | homework-3 | i7 model 1, rubric | Proof of the reflection rule for m ≥ 1: split, first touch tau, S'_j = 2m − S_j after tau, bijection onto {S_n > m} | correct | F III.1; the proof shows one to one and onto |
| 231 | homework-3 | i7 model 2, 3, rubric | Take-profit 0.26318; with p = 0.55 the formula gives 0.504 against the exact 0.410; P(max ≥ m) = P(S_n ≥ m) + E[(q/p)^{S_n − m}; S_n > m] | correct | script: 0.5039, 0.4103, and the tilted formula equals the exact value to 1e−12 |
| 232 | homework-3 | i8 key, w, bk, ex | About 2,496 trades for the mean to sit 2 sd above zero; 624 for 1 sd | correct | script |
| 233 | problems-3 | i0.p0 to p2 keys, w, bk, ex | Var 3.96; sd £39.80; P(down) ≈ Phi(−2.01) ≈ 0.022; exact binomial about 0.020 | correct | script: exact 0.0197 |
| 234 | problems-3 | i0.p3 key, w, bk, ex | Smallest n for a 1% tail is 538; slips 543, 268, 24, 396; four times the trades double the z-score | correct | script |
| 235 | problems-3 | i1.p0 to p2 keys, w, bk, ex | 495 paths end at −4; 495 paths ending at −2 touch −3; touch chance 1588/4096 = 0.3877 | correct | script: mirror enumeration and dynamic programme |
| 236 | problems-3 | i1.p3 key, w, bk, ex | Expected pay-out £61.23; a desk prices with the up-chance that makes the share a fair bet, about 0.476, giving about £55.57 | correct | script: q = (1 − d)/(u − d) = 0.4762, price 55.57; Sh 1.1 to 1.2 |
| 237 | problems-3 | i1.p4 key, opt, ex | With p = 0.52 reflection pairs paths of unequal chance; simulate or tilt | correct | As row 220 |
| 238 | problems-3 | i2.p0 to p3 keys, w, bk, ex | −£4 a trade; 0.5026 with £100 stakes; 0.5515 with £200; expected profit −£48.51 against −£97.36 | correct | script |
| 239 | problems-3 | i3.p0 to p2 keys, w, bk, ex | Target +3, stop −5: target first with chance 5/8; 15 days; expected exit change 0 | correct | script; optional stopping for a bounded fair walk |
| 240 | problems-3 | i3.p3, p4 keys, w, opt, ex | Expected P&L −£600; exits +2 and −6 last 12 days and cost least; none makes money | correct | script |

Rows: 240. Verdicts: correct 231, wrong 1, imprecise 8, misleading 0, unverified 0.

The one `wrong` row is finding 1. The eight `imprecise` rows are findings 2 (rows 26 and 35), 3 (row 212), 4 (row 97), 5 (row 192), 6 (row 199), 7 (row 180) and 8 (row 208).

Depth note: each row was judged by hand against the content text. Rows that name several paths (for example a key with its slips and their feedback lines) were read line by line; every numeric key, `wrong[]` value and slip named in such a row is recomputed in the script (1,537 checks), and each slip's feedback line was read against the quantity the slip value is.

# Claim ledger: markov L1 to L3 (concept audit round 1, blind, 11 Nov 2026)

Scope: `l1` to `l12`, `review-1..3`, `homework-1..3`, `problems-1..3`, `fluency-l2-transition-matrix.json`. One row per definition, result, method step, convention, "always / never / every / only" claim, code-behaviour claim and line of reasoning in an `explain`, `why`, hint or feedback. Rows were judged one at a time; every graded key, `wrong[]` value and slip line was recomputed by hand or in `docs/reports/markov-L1-3-concepts.py` (script checks are named "S:").

Path shorthand: `s[i]` = `screens[i]`, `q[i]` = `quiz[i]`, `it[i]` = `items[i]`, `p[j]` = `parts[j]`, `w` = `widget`, `fb` = `feedback`, `ex` = `explain.text`, `opt[k]` = `widget.options[k]`.

Sources: Norris, *Markov Chains* (N); Grimmett and Stirzaker, *Probability and Random Processes* 3e (GS); Kemeny and Snell, *Finite Markov Chains* ch. 3 (KS); Grinstead and Snell, *Introduction to Probability* ch. 11 to 12 (GrS); Feller, *An Introduction to Probability Theory* vol. 1 (F); Levin, Peres and Wilmer, *Markov Chains and Mixing Times* (LPW); Ross, *Introduction to Probability Models* (R); Hamilton, *Time Series Analysis* ch. 22 (H); Shreve, *Stochastic Calculus for Finance I* ch. 1 (Sh); Hull, *Options, Futures and Other Derivatives* (Hu); Cont (2001), "Empirical properties of asset returns: stylized facts" (C); Casella and Berger (CB). "D:" marks a derivation.

Verdict counts: 339 rows; 322 correct, 12 imprecise, 2 misleading, 3 wrong, 0 unverified.

## l1-only-now.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | s[0] key, fb, ex | From Rain the largest arrow is 0.5 to Cloudy; only arrows leaving today's state matter | correct | D: row R = (0.2, 0.5, 0.3) |
| l1 | s[1] key, opt whys | Days 3 and 8 both follow a Rain day, so both were drawn from (0.2, 0.5, 0.3); outcomes differ, chances do not | correct | D: cells 2 and 7 are R; Markov property N 1.1 |
| l1 | s[1] opt[3].why | "Once today is known, older days add nothing" | correct | Markov property stated as conditional on the present, N Thm 1.1.2 |
| l1 | s[2] prose | Markov chain = states plus, for each state, the chances of the next one | correct | N 1.1 (homogeneous chain) |
| l1 | s[2] key | Missing arrow Cloudy to Rain is 1 - 0.3 - 0.4 = 0.3 | correct | D |
| l1 | s[2] wrong[] | 0.6 from the arrows into Rain (1 - 0.1 - 0.3); 0.7 from removing only 0.3; 0.4 is the loop | correct | D: each slip value matches its feedback line |
| l1 | s[2] ex | Arrows leaving a state add to 1; arrows arriving need not | correct | Row-stochastic matrix, N 1.1 |
| l1 | s[3] key, wrong[], ex | P(S, S given R) = 0.2 x 0.6 = 0.12; second factor read from Sunny's row | correct | D; multiplication rule plus Markov property |
| l1 | s[4] key | Open, 7 steps round a 3-cycle: Closed | correct | D: 7 mod 3 = 1 |
| l1 | s[4] opt[1].why | After 6 steps it is Open | correct | D |
| l1 | s[4] opt[2].why | Pre-open comes from "stopping one step early or going backwards" | wrong | D: one step early (6 steps) is Open; 8 steps or 7 backwards give Pre-open. S: FINDING l1 s4 |
| l1 | s[4] ex | A deterministic chain (one 1 per row) is still Markov; the smallest chain has one state | correct | N 1.1 |
| l1 | s[5] key, whys | P(up tomorrow) is not fixed by today alone: rows 0.7 and 0.4 disagree; 0.55 needs P(yesterday up) | correct | D: law of total probability needs the weight |
| l1 | s[5] ex | With states Up and Down the process is not Markov | correct | GS 6.1 definition |
| l1 | s[6] prose, key, ex | Pair state (yesterday, today) is Markov; from DU the chain goes to UU (0.4) or UD (0.6) | correct | D from the table; standard state enlargement, GS 6.1 ex. |
| l1 | s[7] prose | P(X_{n+1}=j given X_n=i, past) = P(X_{n+1}=j given X_n=i) = p_ij, rows add to 1 | imprecise | The last equality (no dependence on n) is time-homogeneity, never stated in L1 to L3 though every later result uses it. GS 6.1 separates the two |
| l1 | s[7] key, whys, ex | X_5 alone is enough for X_6; "given the present, the past adds nothing" | correct | N Thm 1.1.2 |
| l1 | s[8] key, wrong[], ex | 0.3 x 0.6 x 0.35 = 0.063; slips 1.25, 0.35, 0.15, 0.105 | correct | D |
| l1 | s[8] ex | Each factor needs only the current state, never the order's age | correct | Markov property |
| l1 | s[9] key, wrong[], ex | 0.45 x 0.6 = 0.27; slips 0.36, 0.2025, 0.33, 1.05 | correct | D |
| l1 | s[9] canvas | Path moves 1% up or down each day | correct | D: 100, 101, 102.01, 100.99 |
| l1 | summary ideas, trap | Product of arrows gives a path chance; enlarge the state until today is enough | correct | as above |
| l1 | q[0] | Sunny, Cloudy, Rain path: 0.3 x 0.3 = 0.09; slips 0.6 (added), 0.3 (one step) | correct | D |
| l1 | q[1] | Default from A: 1 - 0.92 - 0.07 = 0.01; slips 0.93, 0.08 | correct | D |
| l1 | q[2] | One-state chain has loop 1 | correct | D |
| l1 | q[3] key, ex | Three signs need 2^3 = 8 states; two arrows leave each triple | correct | D (generic dependence on the three signs) |

## l2-transition-matrix.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l2 | s[0] ex | p_ij = P(next = j given now = i); rows now, columns next; rows add to 1 | correct | Row convention, N 1.1; said here first and kept in every later file |
| l2 | s[1] canvas, key | Bars are row Rain of P^k; 0.33 at k = 2 | correct | S: l2 s1 bars |
| l2 | s[2] lines, order | Split by X_1, multiplication rule, Markov property drops X_0, numbers | correct | Chapman-Kolmogorov proof, N Thm 1.1.3 |
| l2 | s[2] ex | Leaves 0.12 + 0.15 + 0.06 = 0.33 = row Rain times column Sunny | correct | D |
| l2 | s[3] key, wrong[], ex | (P^2)_{S,R} = 0.18; slips 0.01, 0.06, 0.26, 0.1; rows of P^2 add to 1 | correct | S: l2 s3 |
| l2 | s[3] fb squared | 0.1 squared "is no path" | correct | D: S,R,R has chance 0.1 x 0.3 |
| l2 | s[4] key, wrong[] | pi_1 Rain = 0.16; col-conv 0.23, col-sum 0.7, 0.07, 0.09 | correct | D |
| l2 | s[4] fb col-conv | With rows as today the vector goes on the left | correct | Convention kept |
| l2 | s[5] key, ex | P^0 = I; P^m P^n = P^{m+n} holds at m = 0 | correct | D |
| l2 | s[6] key, ex | True two-step 0.47; squared entries match the stay-put path on the diagonal and no path off it; squared row adds to 0.46 | correct | D |
| l2 | s[7] prose | k-step chances are (P^k)_ij; pi_k = pi_0 P^k | correct | N Thm 1.1.3 (uses homogeneity, see l1 s[7]) |
| l2 | s[7] opt[1].why | P^5 pi_0 is the column convention | correct | D: transpose |
| l2 | s[7] ex | P^{m+n} = P^m P^n is the Chapman-Kolmogorov equation | correct | GS 6.1 Thm 7 |
| l2 | s[8] key, wrong[], ex | (P^3)_{AD} = 0.051895; row A of P^2; slips 0.03, 0.0297, 0.028, 1e-6; B route 0.01575 against A route 0.008145 | correct | S: default by year |
| l2 | s[9] solution, tests | step is pi P, after repeats it k times; expected values | correct | S: after R3, B |
| l2 | s[9] ex | k = 0 returns the start, as P^0 = I | correct | D |
| l2 | summary note | With columns adding to 1 write M^k s_0 | correct | transpose |
| l2 | q[0] | (P^2)_{bear,bull} = 0.2(0.9) + 0.8(0.2) = 0.34; slips 0.04, 0.18, 0.16 | correct | D |
| l2 | q[1] | pi_1 bull = 0.55; bull-row slip 0.5(0.9) + 0.5(0.1) = 0.5; column sum 1.1; 0.45 | correct | D |
| l2 | q[2] | Column-stochastic M = P^T moves s by M s | correct | D |
| l2 | q[3] | P^2 P^3 gives five steps; (P^2)^3 is P^6 | correct | D |
| fluency-l2 | families[0] | key = P_i0 P_0j + P_i1 P_1j; slips squared entry and one-step, guarded by `when` | correct | D of the `let` expressions |
| fluency-l2 | families[1] | Row Sunny of P^2 from picked rows (each adds to 1) | correct | D: all 18 rows sum to 1 |
| fluency-l2 | families[2] | u P_0j + (1 - u) P_1j; slips bull row only, unweighted column | correct | D |

## l3-never-leave.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l3 | s[0] ex | Absorbing: p_ii = 1 | correct | N 1.2 |
| l3 | s[1] canvas, key, ex | By k = 20 about 0.43 in C, 0.57 in D and E; A and B drain | correct | S: l3 s1; D: absorption at C is 3/7 |
| l3 | s[2] key, wrong[], ex | f_A = 0.5 + 0.5 x 0.3 = 0.65 | correct | D: B has no loop, so A-B-A is the only other return |
| l3 | s[2] ex | "A state you may leave and never revisit is transient" | correct | N 1.5 |
| l3 | s[3] prose | Recurrent: returns with chance 1; otherwise transient | correct | N 1.5 |
| l3 | s[3] key, set slip | Transient: A, B | correct | D |
| l3 | s[3] fb D, E | "From D the chain goes only to E, and E sends it back" | imprecise | D keeps the chain with 0.6 and E with 0.3; the conclusion (recurrent) is right |
| l3 | s[3] fb C | Absorbing state returns at every step, so recurrent | correct | D |
| l3 | s[4] prose | "A group of states that all communicate is a communicating class" | imprecise | Classes are the maximal such groups (equivalence classes), N 1.2; as worded {D} alone qualifies, yet the item marks it wrong |
| l3 | s[4] key, whys | Class of D is {D, E} | correct | D |
| l3 | s[4] ex | Closed class: can be entered, never left; classes {A,B}, {C}, {D,E}; transient states are the class that leaks | correct | N 1.2, Thm 1.5.6 (finite closed class is recurrent) |
| l3 | s[5] key, wrong[], ex | Over within 4 bets: 0.75; one end 3/8 | correct | S: l3 s5 |
| l3 | s[6] key, ex | Loop 0.95 is sticky, mean stay 20 months; Watch reaches Default so is transient | correct | Geometric mean 1/0.05; N Thm 1.5.5 |
| l3 | s[7] key, ex | Bull and bear: one closed class, both recurrent, none absorbing | correct | N Thm 1.5.6 |
| l3 | s[8] prose | absorbing p_ii = 1; transient f_i < 1; recurrent f_i = 1 | correct | N 1.5 |
| l3 | s[8] key, ex | i reaches j, j cannot reach i: transient; converse in a finite chain | correct | N Thm 1.5.5, 1.5.6 |
| l3 | s[9] key, wrong[], ex | Default during year 3 = 0.051895 - 0.028 = 0.0239; bars cumulative because D absorbs | correct | S; D |
| l3 | s[9] ex | Yearly figure climbs 0.010, 0.018, 0.024 | correct | D (unconditional chance of default in that year) |
| l3 | summary ideas | Finite chain: transient exactly when it can reach a state that cannot reach it back | correct | N 1.5 |
| l3 | q[0] | Filled and Cancelled absorbing; New and Partial transient; every order ends in one of them | correct | N Thm 1.3.2: finite chain, absorbing states reachable |
| l3 | q[1] | Loop 0.7, else absorbed: f_i = 0.7, transient | correct | D |
| l3 | q[2] | Regime chain refutes "every chain gets stuck in an absorbing state" | correct | D |
| l3 | q[3] | Default during year 5: 0.1111 - 0.0800 = 0.0311; slips 0.1111, 0.1911 | correct | S: default by year |

## l4-regimes.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l4 | s[0] key, whys | Unbroken bull for 3 more periods: 0.9^3 = 0.729; (P^3)_{bull,bull} = 0.781 counts returns | correct | D; S |
| l4 | s[1] prose | Run length L has P(L = n) = p^{n-1}(1 - p), n from 1 | correct | Geometric on 1, 2, ...; CB 3.2 |
| l4 | s[1] key, ex | Mode is 1 for every p; mean 1/(1 - p) | correct | D |
| l4 | s[2] lines | E[L] by differentiating the geometric series | correct | D (term-by-term inside the radius) |
| l4 | s[2] ex | Expected duration of a regime is 1/(1 - p_ii) | correct | H 22.2 uses the same formula |
| l4 | s[3] key, wrong[] | Bear 5 periods; slips 1.25, 10, 0.2, 4 | correct | D |
| l4 | s[4] key, ex | Long-run bull share 10/15 = 2/3, equal to the stationary pi | correct | Alternating renewal, R 7.5; b/(a+b) |
| l4 | s[5] key, whys | Exit chance next period is 0.1 whatever the run's age | correct | Markov property; S: MC memoryless |
| l4 | s[5] ex | "Expected time still to run is again 10 periods" | correct | True counting the present period; see l4 s[10] row |
| l4 | s[6] prose, key | Forecast gap = 0.7^k, 0.7 the second eigenvalue; below 0.05 first at k = 9 | correct | S: gap; D: 0.7^8 = 0.0576, 0.7^9 = 0.0404 |
| l4 | s[7] key, whys, ex | Equal rows: persistence 0, runs of mean 2; identity: persistence 1; D: -0.8 | correct | D |
| l4 | s[8] key, fb, ex | Counts 13, 2, 2, 2; p_UU = 13/15, p_DD = 2/4; divide by moves out of the state | correct | S; maximum likelihood, Anderson and Goodman (1957) |
| l4 | s[9] key, wrong[], ex | E[position] = 5.7; long run 9.667; gap closes by 0.7 a period | correct | S; D |
| l4 | s[10] question, key | "How many more weeks": 6.67 | imprecise | 6.67 counts the present week; with the present week excluded the mean is 0.85/0.15 = 5.67, a valid reading that is graded wrong. S: FINDING l4 s10 |
| l4 | s[10] fb total, subtract, ex | Total 10.67 is 4 + 6.67; no relief is due | correct | Consistent with the keyed reading |
| l4 | s[10] ex | A real P&L may have memory the chain lacks | correct | caveat |
| l4 | summary | p_ii is not the share of time; long run is not overdue | correct | D |
| l4 | q[0] | Stay chance 0.95: mean run 20 days; slips 1/0.95, 19 | correct | D |
| l4 | q[1] | Persistence 0.8 + 0.6 - 1 = 0.4 = trace minus 1; slips 1.4, 0.48, 0.2 | correct | D |
| l4 | q[2] | Bull share 20/26.67 = 0.75 = 0.15/(0.05 + 0.15) | correct | D |
| l4 | q[3] | p_ii is a one-step conditional chance, not a share of time nor a run length | correct | D |

## l5-where-it-settles.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | s[0] canvas, key | P(bull at k) = 2/3 + 0.7^k/3 from bull, 2/3 - 2(0.7^k)/3 from bear | correct | D: spectral form of a 2-state chain |
| l5 | s[1] key, ex | (2/3, 1/3) P = (2/3, 1/3); stationary means pi P = pi | correct | N 1.7 |
| l5 | s[2] key, wrong[], ex | x = 0.75; flow out 0.05x = flow in 0.15(1 - x) | correct | D |
| l5 | s[3] key, hints, ex | pi = (0.2, 0.5, 0.3) by columns L and H plus normalising | correct | S |
| l5 | s[4] key, whys, ex | Perf/Def chain: pi = (0, 1); 0.97^100 = 0.048 | correct | D |
| l5 | s[5] key, whys, ex | P v = v is solved by (1,1,1) for every row-stochastic P; share is 0.3 | correct | D |
| l5 | s[6] lines, ex | pi_1 = b/(a + b), needs a + b > 0; both columns give the same equation | correct | D |
| l5 | s[7] prose | pi is also the long-run share of time | correct | Ergodic theorem, N Thm 1.10.2 (irreducible chain here) |
| l5 | s[7] code, ex | Counts bull days; shares 0.666255, 0.668935, 0.66784 | correct | S: l5 s7 (exact match) |
| l5 | s[8] key, wrong[], ex | Long-run mean return 0.3333%; slips -0.5%, 1.5%, -1.3333% | correct | D; N Thm 1.10.2 |
| l5 | summary ideas | Equations dependent; add normalising equation; regime chain settles from any start | correct | D |
| l5 | q[0] | Trending share 0.2/0.6 = 1/3; swap slip 2/3 | correct | D |
| l5 | q[1] | (1/2, 1/2) moves to 0.55 bull, so it is not stationary | correct | D |
| l5 | q[2] | pi_A = 0.3/0.4 = 0.75, so 150m of 200m; slips 100, 180, 50 | correct | D; share of a large book by the law of large numbers |
| l5 | q[3] | pi P = pi alone is singular; normalising picks (2/3, 1/3) | correct | D |

## l6-always-settle.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | s[0] key, ex | Swap: P^k alternates I, P; start at 0.5 never moves | correct | D |
| l6 | s[1] key, ex | Share of days at A tends to 1/2; periodic with period 2; pi read as share of time | correct | N Thm 1.10.2 |
| l6 | s[2] key, ex | Self-loop 0.1: P(at A) = 0.5 + 0.5(-0.8)^k; 0.506 at k = 20; aperiodic | correct | D |
| l6 | s[3] key, whys, ex | Ring of 3: X_100 = B; period 3; pi uniform | correct | D |
| l6 | s[4] key, sets | From A only A and B are reachable | correct | D |
| l6 | s[4] ex | "A set the chain never leaves is a closed class" | imprecise | A closed set need not be a class ({A,B,C,D} is closed); N 1.2 |
| l6 | s[4] ex | Reducible: not every state reaches every other | correct | N 1.2 |
| l6 | s[5] prose, key, ex | Class limits (1/3, 2/3) and (1/2, 1/2); from E the chance at B is 1/3 | correct | S: l6 limits |
| l6 | s[6] key, ex | Software pi = (1/6, 1/3, 1/4, 1/4, 0) is one of many; from C the limit is (0,0,1/2,1/2,0) | correct | S |
| l6 | s[6] fb unique | "This chain is reducible, so it has many" | wrong | Inference false: a reducible chain with one closed class has one pi (the lesson-5 Perf/Def chain). LPW Prop. 1.26 and ex. 1.13. S: FINDING |
| l6 | s[7] prose | Finite, irreducible, aperiodic: unique pi and pi_0 P^k tends to pi | correct | N Thm 1.8.3; LPW Thm 4.9 |
| l6 | s[7] key, whys, ex | Self-loop chain converges; swap and ring periodic; identity reducible | correct | D |
| l6 | s[8] lines, ex | Swap: even powers I, odd powers P; average of a pair has rows (1/2, 1/2) | correct | D |
| l6 | s[9] key, ex | pi = (1/4, 1/2, 1/4); Flat on every even day | correct | S |
| l6 | summary.ideas[1] | "A reducible chain has several closed classes and many stationary distributions" | wrong | False as stated: Perf/Def (l5 s[4]) and every single-absorbing-state chain is reducible with one closed class and one pi. Number of extreme stationary laws = number of closed classes. S: FINDING |
| l6 | summary formula note | Irreducible alone gives a unique pi, as a share of time | correct | N Thm 1.7.7, 1.10.2 |
| l6 | q[0] | Swap has stationary (1/2, 1/2); only convergence fails; (1,0) and (0,1) are not stationary | correct | D |
| l6 | q[1] | Two closed classes {1,2} and {3}; so reducible and pi not unique | correct | D (direction of the inference is right here) |
| l6 | q[2] | pi_1 = 1/1.8 = 5/9; irreducible with a self-loop, so it converges | correct | N Thm 1.8.3 |
| l6 | q[3] | Ring of 4: X_10 = C; pi uniform describes time only | correct | D |

## l7-how-long.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l7 | s[0] canvas, key, ex | Still moving with chance (1/2)^k | correct | D |
| l7 | s[1] key, ex | E[T] = 2; shortcut needs equal exit chances | correct | D |
| l7 | s[2] lines, ex | t_1 = 1 + (1/2)t_2 with t_0 = t_3 = 0; t_1 = 2 | correct | KS Thm 3.3.5 |
| l7 | s[3] key, ex | t = (3, 4, 3) = i(4 - i) | correct | D |
| l7 | s[4] key, hints, ex | t_IG = 30, t_HY = 25 | correct | S |
| l7 | s[5] key, ex | t_X = 0, t_A = 2, t_C infinite | correct | D |
| l7 | s[6] key, whys | Lazy walk t_1 = 4; slips 0, 5, 2 | correct | S; D for 5 |
| l7 | s[7] prose, key | t = 1 + Qt, so (I - Q)t = 1; Q is the transient block | correct | KS Thm 3.3.5; GrS Thm 11.5 |
| l7 | s[7] opt[3].why | With all of P the absorbing rows read 0 = 1 | correct | D |
| l7 | s[8] key, wrong[], ex | t_B = 4; 2.5 at the back; three quarters reach the front | correct | S; D: 0.3/0.4 |
| l7 | summary | No path to absorption gives infinite time | correct | D |
| l7 | q[0] | t = 1 + 0.8t gives 5 minutes; slips 1.25, 4, 0.8 | correct | D |
| l7 | q[1] | t_0 = 0 at an absorbing state | correct | D |
| l7 | q[2] | Equation lacks the +1; with it t_1 = 3 on 0 to 4 | correct | D |
| l7 | q[3] | t_F = 1, t_B = 3; slips 2, 4 | correct | D |

## l8-which-end.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l8 | s[0] canvas, key | From 2 the walk ends at 3 with chance 2/3 | correct | D |
| l8 | s[1] key, whys | h_1 = (1/2)h_0 + (1/2)h_2, no +1; h_0 = 0, h_3 = 1 | correct | N Thm 1.3.2 |
| l8 | s[2] lines, ex | h = (1/3, 2/3); fair walk: straight line | correct | D |
| l8 | s[3] key | h = (4/7, 6/7) for up-chance 2/3 | correct | S |
| l8 | s[4] prose, key, ex | H = (I - Q)^{-1} R; inverse and H as shown; rows of H add to 1 | correct | S; KS Thm 3.3.7 |
| l8 | s[5] key, ex | One absorbing state reachable from all: h = 1 | correct | N Thm 1.3.2 with finite state space |
| l8 | s[6] key, whys, ex | h = (1/4, 1/2, 3/4); boundary values decide what h measures | correct | D |
| l8 | s[7] prose, key | (I - Q)h = r with r the one-step chances into A; g = 1 - h | correct | KS 3.3 |
| l8 | s[8] key, ex | h_F = 0.8, h_B = 0.6 | correct | S |
| l8 | q[0] | Fair walk on 0 to 4 from 3: 3/4 | correct | D |
| l8 | q[1] | h = 0.5h + 0.3 gives 0.6; +1 slip gives 2.6 | correct | D |
| l8 | q[2] | Finite chain, one absorbing state reachable from all: absorbed there with chance 1 | correct | N Thm 1.3.2 |
| l8 | q[3] | H = 2R: from state 2, A with 0.2, B with 0.8; from state 1, 0.6 | correct | D |

## l9-coin-flip-walk.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l9 | s[0] prose, key | Seed-43 path ends at 2, so 6 ups | correct | S: engine walk replicated |
| l9 | s[1] key, ex | Spread grows like root n; plus or minus 2 root n holds about 95% | correct | Var = n; normal approximation |
| l9 | s[2] prose | Simple random walk: independent +1 with chance p, else -1 | correct | F III.1 |
| l9 | s[2] key, wrong[], ex | E[S_100] = 20; drift 0.2 a step | correct | D |
| l9 | s[3] key, wrong[] | sd of S_100 = 10 | correct | D |
| l9 | s[4] key, wrong[], ex | sd = root 96 = 9.80; 0-or-1 coin slip 4.9 | correct | D |
| l9 | s[5] key, wrong[] | p = 1: variance 0 | correct | D |
| l9 | s[6] lines | Mean n(2p - 1) by linearity; variance 4np(1 - p) as independent steps have no covariance | correct | D |
| l9 | s[6] ex | "The variance needs independence" | imprecise | Zero covariances suffice. S: FINDING l9 s6 (pairwise-uncorrelated dependent steps) |
| l9 | s[7] key, wrong[], ex | P(S_20 = 4) = C(20,12)/2^20 = 0.1201; endpoint 2K - n | correct | S |
| l9 | s[8] key, whys | E[S_200 given S_100 = 10 and the past] = 10 | correct | Independent increments |
| l9 | s[8] ex, q[3] | About 7 returns to 0 in 100 steps, 79 in 10,000; returns grow like root n; returns with chance 1 | correct | S: returns; F III.4 (recurrence), expected count about root(2n/pi) |
| l9 | s[9] key, wrong[], ex | sd 31.6; mean 1.27 sd above zero; about one run in ten loses | correct | S: exact 0.0973 |
| l9 | summary trap | Fair walk has no pull back to 0 | correct | Martingale property |
| l9 | q[0] | After 10 steps only even endpoints; 3 is impossible | correct | D: endpoint 2K - 10 |
| l9 | q[1] | Var(S_40) = 4(40)(0.25)(0.75) = 30; mean -20 | correct | D |
| l9 | q[2] | P(down) about Phi(-1.27) = 0.10; exact 0.097; one-sd slip 0.16 | correct | S |

## l10-gamblers-ruin.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l10 | s[0] key, ex | P = 3/10; 9 of 30 simulated games reach 10 | correct | S: seed 11 |
| l10 | s[1] key, ex | Middle start lasts longest; batch means 25 and 7 | correct | S: seed 6 (25.00, 6.60) |
| l10 | s[2] lines | P_0 = 0, P_N = 1; equal gaps; P_i = i/N | correct | F XIV.2 |
| l10 | s[3] prose, key, ex | D_i = i(N - i), D_0 = D_N = 0; 2,500; batch mean 2,398; check identity | correct | F XIV.3; S: seed 28 |
| l10 | s[4] prose, key, wrong[] | P_i = (1 - r^i)/(1 - r^N), r = (1 - p)/p; 0.1192; flip 0.8808 | correct | F XIV.2 eq. 2.4; S |
| l10 | s[4] ex, summary trap | Game lasts "thousands of bets" | correct | S: mean 1,904 bets, loosely "thousands" |
| l10 | s[5] key, whys | One bet of 50: 0.49; ten-pound bets 0.450; one-pound bets 0.1192 | correct | S |
| l10 | s[5] ex | "Bet big when the odds are against you, small when they are for you" | imprecise | True for reaching a fixed target with even-money bets (Dubins and Savage bold play); stated as a general rule |
| l10 | s[6] key, whys, ex | N to infinity: ruin certain for p at most 1/2; r^i for p above 1/2 | correct | F XIV.2 eq. 2.8 |
| l10 | s[7] key, ex | 0.31; loses the stake 69% of the time | correct | S |
| l10 | s[8] key, ex | 100 trades; batch mean 102; plus or minus 20 gives 400 | correct | S: seed 8 |
| l10 | q[0] | At i = N: P_N = 1 and D_N = 0; at 0: P_0 = 0, D_0 = 0 | correct | Boundary conventions as derived |
| l10 | q[1] | D_2 = 2 x 6 = 12; chance of reaching 8 is 0.25 | correct | D |
| l10 | q[2] | p = 0.6, i = 2, N = 4: 9/13; inverted r gives 4/13 = 0.3077, the ruin chance; 1/(1 + r^2) when N = 2i | correct | S; D |
| l10 | q[3] | Fractional staking never reaches exactly 0 | correct | D |

## l11-reflection.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l11 | s[0] key, ex | C(6,4) = 15; paths to (n,k): C(n,(n+k)/2) | correct | F III.1 |
| l11 | s[1] key, ex | First touch at step 4; reflection ends at (8,4) | correct | D |
| l11 | s[2] key | End below level m reflects to 2m - k | correct | F III.1 Lemma |
| l11 | s[3] prose, key | Bijection with paths to (8,4): 28 of 70 | correct | S: brute force |
| l11 | s[3] ex | "In general" count C(n,(n+2m-k)/2) | imprecise | Holds for k at most m only; for k above m every path touches. S: FINDING l11 s3 |
| l11 | s[4] key, ex | Ends on the level: all 56 touch | correct | S |
| l11 | s[5] key, hints, ex | 93 + 37 = 130 of 256; P(max at least 2) = 0.508 | correct | S |
| l11 | s[6] lines, ex | P(max at least m) = P(S_n at least m) + P(S_n above m), m above 0, fair steps | correct | F III.7 Thm 1 |
| l11 | s[7] key, ex | 6/16; the walk up-up-down-down is the one the end count misses | correct | S |
| l11 | s[8] key, hints, ex | 126 - 84 = 42 of 210; ballot theorem (a - b)/(a + b) | correct | S; F III.1 ballot theorem |
| l11 | s[9] key, wrong[], ex | 0.2517 + 0.1316 = 0.3833; parity: below -4 means at most -6 | correct | S |
| l11 | summary note | Fair steps only | correct | D |
| l11 | q[0] | Paths to (10,0) touching 3: C(10,8) = 45 of 252; 210 counts paths to (10,2) | correct | S |
| l11 | q[1] | Paths to (6,4) all pass through 2: 6; mirror rule is for ends below the level | correct | D |
| l11 | q[2] | First reach 2 at step 4: 2/16; hitting time theorem (m/n)P(S_n = m) | correct | D; GS 3.10 Thm 14 |
| l11 | q[3] key | Knock-out within 6 days: 22/64 + 7/64 = 29/64 | correct | S |
| l11 | q[3] ex | Barrier products are priced from this path probability | correct | True for this plus or minus one pound walk (a fair bet) with no interest; see problems-3 it[1] row |

## l12-price-paths.json

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l12 | s[0] key, fb | Chart B moves exactly 1 pound; Chart A falls over 6% on days 71 and 106 | correct | S |
| l12 | s[1], s[2] prose | Log price is a walk; n-day log return is the sum of n independent daily ones | correct | Convention (log returns, independence) stated where first used; Hu 15.1 |
| l12 | s[2] key, wrong[], ex | sd 15.81%, mean 12.5%; noise larger than drift over a year | correct | D |
| l12 | s[3] prose | "If they are independent with mean mu and sd sigma, the CLT gives..." | imprecise | Needs identical distribution or a Lindeberg condition; CB Thm 5.5.14 |
| l12 | s[3] key, ex | Phi(-0.79) = 0.21; one day Phi(-0.05) = 0.48 | correct | S |
| l12 | s[4] key, ex | 125; ud = 1 so only the number of ups matters; ln 1.25 = 0.2231 | correct | D |
| l12 | s[5] key, hints, ex | 352/1024; parity; 13 of 40 touch; bold path touches on day 7, ends at 0 | correct | S: seed 32 |
| l12 | s[6] code, tests, ex | Solution passes its tests; standard error 0.003 | correct | S |
| l12 | s[7] key, whys, ex | Expected change 0; a line through one path is not a drift; path ends at 140 | correct | S: seed 781 |
| l12 | s[8] key, whys | Fat tails and volatility clustering; signs close to uncorrelated; long-horizon returns roughly normal | correct | C stylised facts 1, 3, 4, 6 |
| l12 | s[8] ex | GARCH adds these features | correct | Tsay ch. 3 |
| l12 | s[9] key, wrong[] | One-touch: 100 x 0.26318 = 26.32 | correct | S; the unit-step walk is a fair bet, so expectation is the no-arbitrage value with no interest (Sh 1.2) |
| l12 | s[9] ex | Higher volatility raises the price; drift breaks reflection | correct | Hu ch. 26 |
| l12 | q[0] | sigma = 0: 250-day log return is exactly 10% | correct | D |
| l12 | q[1] | 25-day sd = 2% x 5 = 10%; variance slip 0.01 | correct | D |
| l12 | q[2] key | Six prices after 5 days because ud = 1 | correct | D |
| l12 | q[3] | With p = 0.55 a reflected path has a different probability; the count is still right | correct | D |
| l12 | q[2] ex | Path with k ups "ends at 100 x 1.1^{2k-5}" | imprecise | No starting price is given in the item |

## review-1, review-2, review-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-1 | it[0] | Only the rating chain is Markov in its stated states | correct | GS 6.1 |
| review-1 | it[1] | Missing entry 0.6; column slip 0.8; 0.85 | correct | D |
| review-1 | it[2] | pi_1 bull = 0.34; P pi slip 0.26; 1.1; 0.2 | correct | D |
| review-1 | it[3] | (P^2)_{C,R} = 0.24; 0.09 is the path Rain, Rain; 0.12 through Cloudy | correct | D |
| review-1 | it[4] | Only state 3 transient | correct | D |
| review-1 | it[5] | From 1 on 0 to 3: over within 2 bets with 0.75 | correct | D |
| review-1 | it[6] | Persist 0.75: mean run 4 days; slips 1.33, 3 | correct | D |
| review-1 | it[7] | Exit chance 0.1; time still to come 10 weeks | correct | Counting the present week, as l4 |
| review-1 | it[8] | 15/25, mean run 2.5; about 10 Stressed runs | correct | D |
| review-2 | it[0] | Calm share 0.1/0.4 = 0.25 | correct | D |
| review-2 | it[1] | pi = (0.4, 0.4, 0.2); mean spread 1.8; middle-row slip 1.9 | correct | D |
| review-2 | it[2] | Three chains converge; swap periodic; identity reducible | correct | N Thm 1.8.3 |
| review-2 | it[3] key | h = 0.4 | correct | D |
| review-2 | it[3] ex | "The limit depends on the start because the chain is reducible" | imprecise | The cause is two closed classes, not reducibility |
| review-2 | it[4] | Fair walk 0 to 5 from 2: t = (4, 6, 6, 4) | correct | D: i(5 - i) |
| review-2 | it[5] | t = (1.75, 2.25); row sums of (I - Q)^{-1} | correct | S |
| review-2 | it[6] | h = 0.75h + 0.2 gives 0.8 | correct | D |
| review-2 | it[7] | Down-drift walk: h_2 = 3/7, h_1 = 1/7; slips 2/3, 1/3, 6/7 | correct | D: r = 2 in the ruin formula |
| review-3 | it[0] | sd of 400 trades at p = 0.55: root 396 = 19.90; mean 40 | correct | D |
| review-3 | it[1] | 30 of 120: 0.25; mean length 2,700 bets | correct | D |
| review-3 | it[2] | Paths to (12,2) touching 4: C(12,9) = 220 of 792; 495 to (12,4) | correct | D |
| review-3 | it[3] | 16-day sd = 1.5% x 4 = 6% | correct | D |
| review-3 | it[4] | Ruin against endless money with p = 0.51 from 20: (49/51)^20 = 0.4493 | correct | S; F XIV.2 |
| review-3 | it[5] | P(S_10 = 0) = 252/1024 = 0.2461 | correct | D |
| review-3 | it[6] | Touch 4 within 12: 0.1938 + 0.0730 = 1093/4096 | correct | S |
| review-3 | it[7] | p = 0.55, 5 of 10: 1/(1 + r^5) = 0.7317; ruin 0.2683 | correct | S |
| review-3 | it[8] | Three ups, one down at u = 1.2: 144 | correct | D |

## homework-1, homework-2, homework-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| homework-1 | it[0] | 8 forced zeros | correct | D |
| homework-1 | it[1] | 0.61; buy two trades later likelier than long-run share 4/7 | correct | D |
| homework-1 | it[2] | pi_1 = (0.49, 0.385, 0.125); pi_2 = (0.4815, 0.3805, 0.138) | correct | D |
| homework-1 | it[3] | In default by year 1, 2, 3: 0.15, 0.2655, 0.356475; during year 3: 0.090975 | correct | S |
| homework-1 | it[4] | Recurrent: 3, 4, 5; classes {1,2}, {3}, {4,5} | correct | D |
| homework-1 | it[5] | h = 0.3 + 0.2h = 0.375; f_1 = 0.6 + 0.4h = 0.75; slip 0.72 | correct | D |
| homework-1 | it[6] | E[L] = 1 + pE[L] | correct | First-step analysis |
| homework-1 | it[7] | lambda_2 = a + b - 1 = determinant | correct | D |
| homework-1 | it[8] | Counting estimator and six expected matrices | correct | D by hand for each test |
| homework-1 | it[9] (a), (b) | P-hat rows 190/200 and 51/60; durations 20 and 6.67 weeks | correct | D |
| homework-1 | it[9] (c) | Calm share 0.75 against sample 200/261; 10 Stressed runs | correct | D: 10 C-to-S and 9 S-to-C moves mean the record starts Calm and ends Stressed |
| homework-1 | it[9] (d) | lambda_2 = 0.8; P(S at k given S) = pi_S + (1 - pi_S)lambda^k; 0.5572 at k = 4 | correct | S; spectral form |
| homework-1 | it[9] (e) | Positions 24m and 8m; expected 15.08m in 4 weeks | correct | S |
| homework-1 | it[9] (f) | Memoryless; few Stressed runs; 1/(1 - p) steep near 1 | correct | D |
| homework-2 | it[0] | pi = (0.5, 0.3, 0.2) | correct | D: all three columns checked |
| homework-2 | it[1] | Mean return 0.2%; slips -0.667%, 1% | correct | D |
| homework-2 | it[2] | pi_1 = b/(a + b); slips a/(a + b), b/a | correct | D |
| homework-2 | it[3] | Two closed classes, one periodic; join the pair with chance 1/2; alternates near 1/6 and 1/3 | correct | S |
| homework-2 | it[4] | t = (15/7, 12/7) | correct | S |
| homework-2 | it[5] | H = R + QH; inverse exists when every transient state reaches absorption | correct | KS Thm 3.2.1 |
| homework-2 | it[6] | t = (6, 5); h = (0.6, 0.5); N; loss 1.76m; entries of N are expected years in each rating | correct | D; KS Thm 3.2.4 |
| homework-2 | it[7] key, ex | HTH takes 10 days on average; simulated 9.995 | correct | S (9.9948 with the engine generator) |
| homework-2 | it[7] fb eight | 8 comes from treating "each block of three days" as a fresh trial | imprecise | Block trials would give 24 days; 8 is the wait for one event of chance 1/8. S: FINDING |
| homework-2 | it[8] | H = N R, t = N 1; six chains' expected values; absorption certain when every state reaches an absorbing one | correct | S |
| homework-3 | it[0] | D_i = i(20 - i); check identity | correct | D |
| homework-3 | it[1] | Var(S_n) = 0.84n; mean overtakes sd after about 6 trades | correct | D |
| homework-3 | it[2] | Gaps grow by r = q/p; geometric sum; P_i = (1 - r^i)/(1 - r^N); tends to i/N as p tends to 1/2 | correct | F XIV.2 |
| homework-3 | it[3] | Paths to (10,2) never touching 4: 210 - 45 = 165 | correct | D |
| homework-3 | it[4] | P(T = 9) for level 3: 28/512 = 0.0547 = (3/9)(84/512) | correct | D; hitting time theorem |
| homework-3 | it[5] | Roulette 0.3680 | correct | S |
| homework-3 | it[6] | DP solution exact for any p; 0.4523 against reflection's 0.5321 | correct | S |
| homework-3 | it[7] part 1 | Reflection proof for m at least 1 | correct | F III.7 |
| homework-3 | it[7] part 3 | Formula overstates at p = 0.55 (0.504 against 0.410); (q/p)^{S_n - m} weighting repairs it | correct | S: tilt identity exact |
| homework-3 | it[8] | About 2,496 trades | correct | D |

## problems-1, problems-2, problems-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| problems-1 | it[0] p[0] | p_TT = 14/20 = 0.7; slips 14/60, 14/48, 0.5 | correct | D |
| problems-1 | it[0] p[1] | (P^2)_{TT} = 0.535; slips 0.49, 0.745, 0.58 | correct | D |
| problems-1 | it[0] p[2] | Thin spell 1/0.3 = 3.33; slips 1.43, 2.33, 2.15 | correct | D |
| problems-1 | it[0] p[3] | Thin share 1/3; record agrees (20 of 60 moves start in T) | correct | D |
| problems-1 | it[1] p[0] | Path loss, win, loss, loss: 0.0216; slips 0.0189, 0.0108, 0.0378 | correct | D |
| problems-1 | it[1] p[1] | Stopped after two trades: 0.18; row W of P^2 = (0.61, 0.21, 0.18) | correct | D |
| problems-1 | it[1] p[2] | Stopped by trade 3: 0.306; slips 0.126, 0.39, 0.243 | correct | D |
| problems-1 | it[1] p[3] | Stops on trade 4 exactly: 0.183 x 0.6 = 0.1098 = 0.4158 - 0.306 | correct | D |
| problems-1 | it[2] p[0] | Healthy at least once in two days from M: 0.65; (P^2)_{MH} = 0.6 is a different event | correct | D |
| problems-1 | it[2] p[1] | Ever Healthy again from M: h = 0.5 + 0.3h = 5/7 | correct | D |
| problems-1 | it[2] p[2] | f_H = 0.9 + 0.1(5/7) = 34/35; H transient | correct | D |
| problems-1 | it[2] p[3] | Healthy account is liquidated in the end with chance 1; X the only closed class | correct | N Thm 1.5.6; D |
| problems-1 | it[3] p[0] | Stressed spell 3.33 months | correct | D |
| problems-1 | it[3] p[1] | Calm share 6/7 = 0.3/0.35; slips 0.5758, 0.9333 | correct | D |
| problems-1 | it[3] p[2] | Long-run P&L 10/7; slips -2.5, 2.2667, 3.7143, -6.4286 | correct | D |
| problems-1 | it[3] p[3] | After a stressed month: -4.7; after calm: 2.45 | correct | D |
| problems-1 | it[3] p[4] | Rule "trade only after a calm month" earns 2.1 | misleading | Arithmetic right; it assumes the regime is observed as each month ends, though regimes are inferred late and with error (H 22.4). Not said |
| problems-2 | it[0] p[0] | (P^2)_{I,A} = 0.14 | correct | D |
| problems-2 | it[0] p[1] | pi_B = 0.2 pi_I; pi_A = 0.25 pi_I | correct | D |
| problems-2 | it[0] p[2] | pi_I = 20/29; slips 0.7407, 2.2222 | correct | S |
| problems-2 | it[0] p[3] | Irreducible and aperiodic (self-loops), so pi can be used 60 days ahead from any start | correct | N Thm 1.8.3 |
| problems-2 | it[0] p[4] | Mean P&L 7/29 = 0.2414; slips 1.6667, 1.6207, -0.2, 0.931 | correct | D |
| problems-2 | it[1] p[0] | (P^2)_{Test,On} = 0.42 | correct | D |
| problems-2 | it[1] p[1] | On share inside the live class: 0.8 | correct | D |
| problems-2 | it[1] p[2] | Ever goes live: h = 0.3 + 0.5h = 0.6 | correct | D |
| problems-2 | it[1] p[3] | Far ahead On with 0.6 x 0.8 = 0.48; limit depends on the start | correct | D |
| problems-2 | it[2] p[0] | h_C = 0.2 + 0.5q | correct | D |
| problems-2 | it[2] p[1] | q = 0.6; slips 0.4, 0.48, 0.5, 0.65 | correct | S |
| problems-2 | it[2] p[2] | t_Q = 1.75, t_C = 1.875 | correct | S |
| problems-2 | it[2] p[3] | Tighter quote: q = 0.56/0.85 = 0.6588 | correct | S |
| problems-2 | it[2] p[4] | Old quote earns 30 against 26.35; tighter quote ends in 1.53 rounds | correct | S |
| problems-2 | it[3] p[0] | h_R = 0.625 | correct | D |
| problems-2 | it[3] p[1] | h_A = 0.575; slips 0.2875, 0.4, 0.43125 | correct | S |
| problems-2 | it[3] p[2] | t_A = 3.5; slips 1.75, 2, 1.5, 4.5 | correct | S |
| problems-2 | it[3] p[3] | Expected value at resolution 8.30 | correct | D |
| problems-2 | it[3] p[4] | Break-even 8.30 - 0.02 x 3.5 = 8.23; expected cost uses E[T] | correct | D: linearity (Wald) |
| problems-3 | it[0] p[0] | Var of one 2-pound trade: 3.96 | correct | D |
| problems-3 | it[0] p[1] | sd after 400 trades: 39.80 | correct | D |
| problems-3 | it[0] p[2] | P(down) about 0.022; exact binomial about 0.020 | correct | S: 0.0199 |
| problems-3 | it[0] p[3] | Smallest n for a 1% tail: 538; slips 543, 268, 24, 396 | correct | D |
| problems-3 | it[1] p[0] | Paths ending at -4: C(12,4) = 495 | correct | D |
| problems-3 | it[1] p[1] | Paths ending at -2 that touch -3: 495 by reflection | correct | D |
| problems-3 | it[1] p[2] | 794 end at or below -4; touch chance 1588/4096 = 0.3877 | correct | S |
| problems-3 | it[1] p[3] | "With no interest the fair price is the expected pay-out": 61.23 | misleading | Under up-chance 0.5 the share itself grows 0.45% a day, so 0.5 is not the pricing chance; with q = 0.476 the note is worth 55.57 (Sh 1.1 to 1.2). S: FINDING |
| problems-3 | it[1] p[4] | Simulate with drift; upward drift touches a lower barrier less often | correct | D |
| problems-3 | it[2] p[0] | Mean of one 100-pound trade: -4 | correct | D |
| problems-3 | it[2] p[1] | 100 stakes: 0.5026; inverted 0.6923 | correct | S |
| problems-3 | it[2] p[2] | 200 stakes: 0.5515; inverted 0.6472 | correct | S |
| problems-3 | it[2] p[3] | Expected profit -48.5 against -97.4 | correct | D |
| problems-3 | it[3] p[0] | Exit at +3 before -5: 5/8 | correct | S: MC |
| problems-3 | it[3] p[1] | Mean length 15 days | correct | S: MC |
| problems-3 | it[3] p[2] | Expected change at exit 0 ticks: barriers cannot make an edge on a fair walk | correct | Optional stopping, bounded exit; D |
| problems-3 | it[3] p[3] | Expected P&L -600 | correct | D: linearity |
| problems-3 | it[3] p[4] | +2 and -6 best at -480 (12 days against 15 and 16) | correct | D |

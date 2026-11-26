# Ledger: delta audit 2026-11-26 batch 4

Scope: strings and values added or changed between each course's close and `b2fa22b4` in the ten problem-set files of `delta-batch4.tsv`. Basis "script" means `docs/reports/audit-delta-2026-11-26-4-concepts.py` (exact recompute; MC marks a Monte Carlo check there). Parts are numbered from 1.

| # | file | path | claim (short) | verdict | basis |
|---|---|---|---|---|---|
| C1 | conditional/problems-2 | filters problem, part 3 byKey.skipped-a | 0.5882 starts from the 2% base rate; B only sees A-flagged prints, 0.3265 of them errors | correct | prose: "Flagged prints go on to filter B"; odds 0.02/0.98 × 70 = 1.4286, chance 0.5882; 0.019/0.0582 = 0.3265 |
| C2 | conditional/problems-3 | p-two-papers prose | groups 0.4 / 0.6; each group P(M) = 0.2, P(C) = 0.55; pooled independent; graduates P(C given M) = 0.85 | correct | joint tables feasible (0.17 ≤ 0.2, 0.07 ≥ 0); pooled 0.4 × 0.17 + 0.6 × 0.07 = 0.11 = 0.2 × 0.55; MC |
| C3 | conditional/problems-3 | part 1 question, key 0.17 | P(both, graduate) = 0.2 × 0.85 | correct | multiplication rule |
| C4 | conditional/problems-3 | part 1 slip indep 0.11 + feedback | 0.2 × 0.55 treats the papers as unlinked | correct | recompute |
| C5 | conditional/problems-3 | part 1 slip cond 0.85 + feedback | 0.85 is P(C given M), needs × 0.2 | correct | definition |
| C6 | conditional/problems-3 | part 1 slip over-y 0.4675 + feedback | 0.85 × 0.55 pairs the conditional with the wrong marginal | correct | 0.85 × 0.55 = 0.4675 |
| C7 | conditional/problems-3 | part 1 correct, generic, explain | 0.2 × 0.85 = 0.17 | correct | recompute |
| C8 | conditional/problems-3 | part 2 question | pooled independence gives P(both) = 0.2 × 0.55 = 0.11 | correct | pooled marginals equal the group marginals, since both groups share them |
| C9 | conditional/problems-3 | part 2 key 0.07, correct, explain | 0.11 = 0.4 × 0.17 + 0.6 p, p = 0.042 / 0.6 | correct | total probability; carried 0.17 |
| C10 | conditional/problems-3 | part 2 slip unweighted 0.042 + feedback | career-changers' part of the pooled 0.11, a share of all applicants | correct | 0.6 × 0.07 = 0.042 = P(both and career-changer) |
| C11 | conditional/problems-3 | part 2 slip equal 0.05 + feedback | equal group weights | correct | (0.11 − 0.5 × 0.17) / 0.5 = 0.05 |
| C12 | conditional/problems-3 | part 2 slip indep 0.11 + feedback | assumes unlinked for career-changers | correct | 0.2 × 0.55 |
| C13 | conditional/problems-3 | part 2 generic | pooled 0.11 is a weighted mean of the groups' chances | correct | total probability |
| C14 | conditional/problems-3 | part 3 question, key 0.35, correct | P(C given M, career) = 0.07 / 0.2 | correct | definition; carried 0.07 |
| C15 | conditional/problems-3 | part 3 slip joint 0.07 + feedback | joint is out of all career-changers | correct | definition |
| C16 | conditional/problems-3 | part 3 slip over-y 0.1273 + feedback | 0.07 / 0.55 is P(M given C) among career-changers | correct | 0.127273 |
| C17 | conditional/problems-3 | part 3 slip unweighted 0.21 + feedback | 0.042 / 0.2; 0.042 is not a within-group chance | correct | carried part 2 slip gives 0.21 |
| C18 | conditional/problems-3 | part 3 generic, explain | 0.35 < 0.55: a maths pass makes coding less likely for a career-changer | correct | P(C given M) < P(C) |
| C19 | conditional/problems-3 | part 4 question + option both-dep (key) | pooled independent, dependent within each group | correct | 0.17 ≠ 0.11, 0.07 ≠ 0.11, pooled 0.11 |
| C20 | conditional/problems-3 | part 4 option carry + why | pooled independence does not pass to the groups | correct | the problem is its own counterexample; independence does not imply conditional independence (Casella and Berger 1.3; Grimmett and Stirzaker 1.5) |
| C21 | conditional/problems-3 | part 4 option cancel + why | links of opposite sign offset; pooled 0.11 exact | correct | 0.4 × 0.30 − 0.6 × 0.20 = 0 |
| C22 | conditional/problems-3 | part 4 option same-sign + why | 0.85 above 0.55, 0.35 below | correct | recompute |
| C23 | conditional/problems-3 | part 4 correct, generic | pooled P(C given M) = 0.55 | correct | 0.11 / 0.2; MC 0.550 |
| C24 | conditional/problems-3 | part 4 explain | shifts weighted 0.4 and 0.6 offset exactly; a pooled check misses both | correct | the weights are P(group given M), equal to P(group) because P(M) is 0.2 in both groups |
| C25 | conditional/problems-4 | p-dark-fills prose | 60% one fill, 40% three fills; each fill dark with chance 0.2, independently of fills and size | correct | well posed |
| C26 | conditional/problems-4 | part 1 question, key 0.6667, correct, explain | P(fill from large) = 1.2 / 1.8 | correct | size-biased sampling; exact in expectation, and "thousands of orders" makes the realised ratio stable; MC 0.667 |
| C27 | conditional/problems-4 | part 1 slip orders 0.4 + feedback | share of orders | correct | prior |
| C28 | conditional/problems-4 | part 1 feedback even (0.5) | the two kinds are not equally likely to supply the fill | correct | 1.2 against 0.6 |
| C29 | conditional/problems-4 | part 1 slip small 0.3333 + feedback, generic | complement | correct | 0.6 / 1.8 |
| C30 | conditional/problems-4 | part 2 question, key 0.6667, correct, explain | dark news has likelihood ratio 1 for the drawn fill | correct | P(dark given a large order's fill) = P(dark given a small order's fill) = 0.2; MC 0.667 |
| C31 | conditional/problems-4 | part 2 slip orders-slip 0.4 + feedback | carried part 1 slip, unchanged by a ratio of 1 | correct | 0.4 × 1 |
| C32 | conditional/problems-4 | part 2 slip joint 0.1333 + feedback | 2/3 × 0.2 = P(dark and large) | correct | recompute |
| C33 | conditional/problems-4 | part 2 slip double 0.8299 + feedback | fill weighting, then the order-level ratio 0.488 / 0.2 | correct | odds 2 × 2.44 = 4.88; 4.88 / 5.88 = 0.82993 |
| C34 | conditional/problems-4 | part 2 generic | ask whether a dark fill is likelier from a large order | correct | method |
| C35 | conditional/problems-4 | part 3 question, key 0.488, correct, explain | 1 − 0.8³; 0.2 for a small order | correct | complement rule |
| C36 | conditional/problems-4 | part 3 slip sum 0.6 + feedback | 3 × 0.2 double counts | correct | inclusion and exclusion |
| C37 | conditional/problems-4 | part 3 slip all 0.008 + feedback | 0.2³ | correct | recompute |
| C38 | conditional/problems-4 | part 3 slip exactly-one 0.384 + feedback | 3 × 0.2 × 0.8² | correct | binomial |
| C39 | conditional/problems-4 | part 3 slip one 0.2 + feedback, generic | a single fill | correct | recompute |
| C40 | conditional/problems-4 | part 4 question, key 0.6193, correct, explain | 0.1952 / 0.3152 | correct | Bayes; MC 0.619 |
| C41 | conditional/problems-4 | part 4 slip no-news 0.4 + feedback | prior; a yes raises it | correct | ratio 2.44 > 1 |
| C42 | conditional/problems-4 | part 4 slip sum-slip 0.6667 + feedback | 0.6 from the part 3 slip acts like a drawn fill | correct | 0.24 / 0.36; ratio 3 equals the fill-count ratio |
| C43 | conditional/problems-4 | part 4 slip no-prior 0.7093 + feedback | 0.488 / 0.688 | correct | recompute |
| C44 | conditional/problems-4 | part 4 slip path 0.1952 + feedback, generic | numerator alone; P(yes) = 0.3152 | correct | recompute |
| C45 | conditional/problems-4 | part 5 question | 0.6667 and 0.6193 are both up from 0.4 | correct | 0.4 is the order prior on both routes |
| C46 | conditional/problems-4 | part 5 option ratio (key), correct feedback | drawn fill has ratio 3; a yes has 0.488 / 0.2 = 2.44 | correct | odds 2/3 × 3 = 2 gives 0.6667; 2/3 × 2.44 = 1.627 gives 0.6193 |
| C47 | conditional/problems-4 | part 5 option irrelevant + why | three fills can give the yes | correct | 0.488 > 0.2 |
| C48 | conditional/problems-4 | part 5 option same + why | several dark fills give one yes, so 2.44 < 3 | correct | 1 − 0.8³ < 3 × 0.2 |
| C49 | conditional/problems-4 | part 5 option less-dark + why, generic | every fill goes dark with chance 0.2 | correct | prose |
| C50 | conditional/problems-4 | part 5 explain, sentence 1 | "A fill drawn at random is 3 times as likely to come from a large order, one per fill" | imprecise | a drawn fill is 2 times as likely to come from a large order (2/3 against 1/3); 3 is the per-order likelihood ratio. Finding 2 |
| C51 | conditional/problems-4 | part 5 explain, rest | the yes lifts 0.4 to 0.6193, not 0.6667 | correct | C40, C26 |
| C52 | conditional/problems-5 | p-doubling-desk prose | £1 opening stake, doubled after each losing bet, round ends at the first win or five losses running | correct | same game as before the edit: a win nets £1, five losses cost 1 + 2 + 4 + 8 + 16 = 31 |
| C53 | conditional/problems-5 | part 1 question | "On average, how much does one round make", key 0 | correct | 31/32 × 1 − 1/32 × 31 = 0 |
| L1 | limits-thm/problems-2 | p-digital-share part 1 explain | Z is below 0 half the time and S₁ rises with Z, so the median is the value at Z = 0 | correct | quantiles pass through increasing maps (Casella and Berger 2.1); MC median 81.21 |
| L2 | limits-thm/problems-2 | part 3 question | Φ(0.15) = 0.5596, Φ(0.2) = 0.5793 | correct | scipy 0.559618, 0.579260 |
| L3 | limits-thm/problems-2 | part 3 slip no-centre 0.5793 | value | correct | Φ(0.06 / 0.3) |
| L4 | limits-thm/problems-2 | part 3 byKey.no-centre | leaves out the log drift 0.015; z = 0.045 / 0.3 = 0.15 | correct | ln(S₁/80) ~ N(0.015, 0.09) |
| M1 | markov/problems-1 | carry trade part 1 byKey.used-stay | 0.7 is P(stress follows stress); a spell ends with chance 0.3, mean 1 / 0.3 | correct | geometric holding time (Norris, *Markov Chains*, 1.1); slip 1 / 0.7 = 1.4286 |
| M2 | markov/problems-1 | part 4 slip sign 4.7 | value is the key with its sign flipped | correct | −(−4.7) |
| M3 | markov/problems-1 | part 4 byKey.sign, sentence 1 | 0.3 × 3 = 0.9, 0.7 × (−8) = −5.6, sum below zero | correct | recompute |
| M4 | markov/problems-1 | part 4 byKey.sign, sentence 2 | "A positive 4.7 drops the minus sign of the stressed-month loss" | wrong | dropping that minus gives 0.9 + 5.6 = 6.5, not 4.7. Finding 1 |
| M5 | markov/problems-3 | p-barrier-note part 2 question | reflection in the level −3 | correct | the mirror of −2 in −3 is −4; C(12, 4) = 495 (Feller I, III.1) |
| M6 | markov/problems-3 | part 2 placeholder | "a whole number" | correct | key 495, tol 0 |
| M7 | markov/problems-3 | p-stake-size part 1 slip sign 4 + feedback | mean 100(2 × 0.48 − 1) = −4; +4 books the drift as a gain | correct | recompute |
| M8 | markov/problems-3 | part 4 slip sign 48.51 + feedback | wealth £551.49 is below £600 | correct | exact P₃ = 0.551490, so 551.49 and −48.51 |
| M9 | markov/problems-3 | p-pairs-exit part 4 slip sign 600 + feedback | £40 × 15 days; the spread earns 0 on average | correct | optional stopping for the fair walk; D = 5 × 3 = 15 |
| R1 | random-vars/problems-2 | reversals part 4 slip sign 15.96 + feedback | 8 × 9.12 = 72.96 > 57; 72.96 − 57 | correct | recompute |
| R2 | random-vars/problems-3 | hedge part 2 slip decimal 0.000216 + feedback | variance with returns as decimals; × 10,000 | correct | (0.01)² scaling; 2.16 / 10⁴ |
| R3 | random-vars/problems-3 | part 2 slip tol 0.0000043 | 2% band, clear of the key and other slips | correct | nearest other value 2.0 |
| R4 | random-vars/problems-3 | part 3 slip decimal 0.000168 + feedback, tol | covariance in decimals | correct | 1.68 / 10⁴ |
| R5 | random-vars/problems-3 | part 5 slip decimal 0.0001425 + feedback, tol | hedged variance in decimals | correct | 1.425 / 10⁴ |
| R6 | random-vars/problems-5 | p-startup-rounds part 1 slip sign 0.0527 | value is the key with its sign flipped | correct | ½ ln 0.9 = −0.05268 |
| R7 | random-vars/problems-5 | part 1 byKey.sign, sentence 1 | ln 0.6 = −0.5108 outweighs ln 1.5 = 0.4055 | correct | −0.510826, 0.405465 |
| R8 | random-vars/problems-5 | part 1 byKey.sign, sentence 2 | "A positive 0.0527 takes 0.5108 − 0.4055" | imprecise | 0.5108 − 0.4055 = 0.1053; the slip is half of that. Finding 3 |
| R9 | random-vars/problems-5 | part 2 slip sign 0.2108 + feedback | 4 × (−0.0527); +0.2108 drops the minus of E[ln R] | correct | Wald: E[ln W] = E[N] E[ln R]; 4 × 0.0527 = 0.2108 |

Rows: conditional 53, limits-thm 4, markov 9, random-vars 9; total 75. Verdicts: 72 correct, 1 wrong, 2 imprecise, 0 misleading, 0 unverified.

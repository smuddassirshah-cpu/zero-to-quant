# Claim ledger: conditional (topic 1.5), levels 1 to 3, audit round 3

Blind read, 11 Nov 2026. Every row was judged by hand from the content string named; none was generated. Stage 1 course, so the ledger has full depth: definitions, rules, methods, conventions, graded keys, slips, and the reasoning in explanations, hints and feedback.

Sources, cited by short name:
- **Ross**: S. Ross, *A First Course in Probability*, ch. 3 (3.2 conditional probabilities, 3.3 Bayes's formula, 3.4 independent events, 3.5 P(·|F) is a probability) and ch. 4.6 (binomial).
- **BH**: Blitzstein and Hwang, *Introduction to Probability*, ch. 2 (2.2 definition, 2.3 Bayes' rule and the law of total probability, 2.4 conditional probabilities are probabilities, 2.5 independence of events, 2.6 coherency of Bayes' rule, 2.8 pitfalls and paradoxes).
- **GS**: Grimmett and Stirzaker, *Probability and Random Processes*, 1.4 (conditional probability), 1.5 (independence; a family is independent when the product rule holds for every finite subfamily).
- **GH**: Gigerenzer and Hoffrage (1995), "How to improve Bayesian reasoning without instruction: frequency formats", *Psychological Review* 102.
- **Pearl**: J. Pearl, *Probabilistic Reasoning in Intelligent Systems*, 2.2.4 (explaining away).
- **Hull**: J. Hull, *Options, Futures, and Other Derivatives*, ch. 8 (securitisation and the 2007 crisis) and the credit-risk chapter on default correlation and the one-factor model.
- **script**: a check in `docs/reports/conditional-L1-3-concepts-r3.py` (exact enumeration with fractions, or seeded Monte Carlo where marked MC).

Verdict counts are at the foot.

| # | File | JSON path | Claim (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l1 | screens[1] key, why, explain | Even news makes a 6 more likely; three rivals drop out and survivors share the whole chance | correct | Ross 3.2; 1/6 to 1/3, script |
| 2 | l1 | screens[2] answer and byKey | Faces left after "even" are 2, 4, 6; odd faces ruled out | correct | enumeration |
| 3 | l1 | screens[3] answer, slips, explain | P(6 given even) = 1/3; "doubled the chance by halving what is left"; slip 1/2 treats 6 and not-6 as equal | correct | 1/3 = 2 × 1/6; three faces left of six |
| 4 | l1 | screens[4] options | P(even given above 3) = 2/3; 2/6 divides by all six; 1/3 counts the odd face | correct | script |
| 5 | l1 | screens[5] | A face the news rules out has chance 0 | correct | P(A∩B) = 0, Ross 3.2 |
| 6 | l1 | screens[6] key and explain | "At most 4" leaves even at 1/2; news changes a chance only when the removed outcomes hold a different share of the event | correct | P(A given B) = P(A) iff P(A given not B) = P(A) for 0 < P(B) < 1, by total probability |
| 7 | l1 | screens[7] rule and key | Equally likely outcomes: count in A and B over count in B; the bottom is what the news allows | correct | Ross 3.2, eq. for equally likely outcomes |
| 8 | l1 | screens[8] answer, slips, explain | 56/80 = 0.7 against 120/200 = 0.6; slips 0.6, 56/120, 56/200 named rightly | correct | script (venn counts) |
| 9 | l1 | summary.ideas, formula, trap | News can raise, zero, or leave a chance; formula flagged "for equally likely outcomes" | correct | hypothesis stated; Ross 3.2 |
| 10 | l1 | quiz[0..2] | 13/26 hearts; 1/4 for "at least 3"; odd raises "at most 3" from 1/2 to 2/3 | correct | script |
| 11 | l2 | screens[1] | After a seen red, 2 of 4 left; slips 3/5, 2/5, 3/4 described rightly | correct | enumeration |
| 12 | l2 | screens[2], [3] | 20 ordered pairs, 6 both red, 12 with red first; 6/12 = 2/4 | correct | script |
| 13 | l2 | screens[4] explain | Each branch leaves a different bag, so the same question gets different answers | correct | 2/4 and 3/4, script |
| 14 | l2 | screens[5] | P(both red) = 6/20 = 3/5 × 2/4; slips 0.36, 0.5, 0.6 | correct | multiplication rule, Ross 3.2 |
| 15 | l2 | screens[6] key, slips, explain | Unseen first draw: P(second red) = 12/20 = 3/5; plain average 0.625 is wrong because red first is likelier | correct | script, MC l2; exchangeability of draws |
| 16 | l2 | screens[7] prose | P(A∩B) = P(A)P(B given A) named the multiplication rule | correct | Ross 3.2 |
| 17 | l2 | screens[8] expression key | 6/20 = 12/20 × 6/12; accept list 6/12, 1/2, 0.5, 2/4 | correct | arithmetic; all accepted forms equal 1/2 |
| 18 | l2 | screens[9] | 4/10 × 3/9 = 2/15; sampling without repeats is drawing without replacement | correct | hypergeometric path, Ross 3.2 |
| 19 | l2 | summary | Second draw has the same chance as the first with no news; trap line | correct | script |
| 20 | l2 | quiz[0..2] | 1/5; 1/221; hidden first gives 2/5 (3/10 + 1/10) | correct | recomputed by hand |
| 21 | l3 | screens[1] | Five outcomes total 8; (4,4) counts once | correct | script |
| 22 | l3 | screens[2] | First die 5 leaves 6 cells; chance of 8 moves from 5/36 to 1/6 | correct | enumeration |
| 23 | l3 | screens[3] prose and key | Protocol stated: you ask "does at least one die show a 5?" and hear yes; 11 outcomes left | correct | news is the event itself, so conditioning on it is right, BH 2.8; script |
| 24 | l3 | screens[4] | P(total 10 given at least one 5) = 1/11; "fixed die" slip 1/6; before the news 3/36 | correct | script and MC l3 (separates 1/11 from 1/6) |
| 25 | l3 | screens[5] order and explain | Counts over 36 become probabilities; P(A∩B)/P(B) is the definition when outcomes are not equally likely | correct | Ross 3.2 definition |
| 26 | l3 | screens[6] | About 11/36 of rolls survive; slips 91, 167, 333 | correct | MC l3; 1000/11 = 90.9, 1000/6, 1000 × 12/36 |
| 27 | l3 | screens[7] | Two stocks, asked "did at least one finish up": 1/3, not 1/2 | correct | script; protocol stated in the prose |
| 28 | l3 | summary.formula.note | Defined only when P(B) > 0 | correct | Ross 3.2; exact for this discrete stage |
| 29 | l3 | summary.trap | "At least one is a 5" leaves 11; "the first is a 5" leaves 6 | correct | script |
| 30 | l3 | quiz[0] | P(a 3 shows given total 7) = 1/3; 2/11 is the reverse | correct | script |
| 31 | l3 | quiz[1], [2] | 2/3; knowing A rose gives 1/2 against 1/3 for "at least one" | correct | script |
| 32 | l4 | screens[1], [2] | After 9H: 3 hearts of 5; after 3S: 4 hearts of 5 | correct | enumeration |
| 33 | l4 | screens[3] | Both hearts 4/6 × 3/5 = 2/5; slips 4/9, 3/5, 2/3, 8/15 | correct | script |
| 34 | l4 | screens[4] | Three hearts 4/6 × 3/5 × 2/4 = 1/5 | correct | script |
| 35 | l4 | screens[5] | With replacement P(B given A) = P(B): plain product 4/9 | correct | Ross 3.4 |
| 36 | l4 | screens[6] trap | Sam's 16/36 counts the diagonal; each marginal 4/6 is right alone but not after a heart | correct | script (both hearts 12/30) |
| 37 | l4 | screens[7] | Chain rule for three events; heart, spade, heart = 4/6 × 2/5 × 3/4 = 1/5 | correct | Ross 3.2 multiplication rule; script |
| 38 | l4 | screens[8] | P(B) = 10/30, P(A given B) = 8/10; either order gives 8/30 | correct | script |
| 39 | l4 | screens[9] explain | 0.4 × 0.6 = 0.24; treating fills as unrelated gives 0.16, a third lower | correct | (0.24 − 0.16)/0.24 = 1/3; "understates the clustering" read as understating this chance |
| 40 | l4 | summary | Trap: P(A)P(B) is wrong when the first draw changes the second | correct | Ross 3.4 |
| 41 | l4 | quiz[0..3] | 1/22; 4/663; 1/16; 1/10 and their slips | correct | recomputed by hand |
| 42 | l5 | screens[1] tree and table | Second-stage branches 4/7, 3/7 after black; 5/7, 2/7 after white | correct | script tree check |
| 43 | l5 | screens[3] | White then white 3/8 × 2/7 = 3/28; a path multiplies | correct | Ross 3.2 |
| 44 | l5 | screens[4] | Leaves 20, 15, 15, 6 over 56 add to 1; every outcome lies on exactly one path | correct | script; partition argument |
| 45 | l5 | screens[5] | A branch with chance 0/5 can be pruned without changing any chance | correct | leaf = 1/6 × 0 |
| 46 | l5 | screens[6] | Black, black, white = 5/8 × 4/7 × 3/6 = 5/28; three slips | correct | recomputed (75/512, 60/448, 60/392) |
| 47 | l5 | screens[7] trap | Kim's leaves add to 1 yet the tree is wrong; true path 15/56 | correct | script: any tree whose node branches add to 1 has leaves adding to 1 |
| 48 | l5 | screens[8] | A branch off "white" carries P(second black given first white) = 5/7; leaf is the joint; unconditional is 5/8 | correct | definitions, Ross 3.2 |
| 49 | l5 | screens[9] proof | Two leaves after black add to P(B1); proof needs only each node's branches to add to 1 | correct | derivation in the item is valid |
| 50 | l5 | screens[10] | 0.6 × 0.45 = 0.27; using the all-days 0.52 overstates; called adverse selection | correct | conditional on a fill differs from unconditional; standard microstructure term (Glosten and Milgrom 1985) |
| 51 | l5 | summary.trap | Leaves that add to 1 do not prove a tree right | correct | screens[7] counterexample |
| 52 | l5 | quiz[0..3] | 0.004; 12/51 on the branch and 1/17 leaf; missing leaf 0.12; blue-blue pruned | correct | recomputed |
| 53 | l6 | screens[1], [3] | Leaves 3/12 and 2/12 add to 5/12; the two paths cannot both happen | correct | script; additivity for disjoint events |
| 54 | l6 | screens[2] | P(red) moves from 1/4 to 3/4 as P(bag A) goes 0 to 1: a weighted average | correct | 0.75p + 0.25(1 − p) |
| 55 | l6 | screens[4] | Three bags: 11/24; first stage can have any number of branches if they cover every case without overlap | correct | law of total probability, BH 2.3; script |
| 56 | l6 | screens[5] | Same conditional chance in every bag: weights drop out; "the bag tells you nothing" | correct | P(B given A_i) = c for all i gives P(B) = c |
| 57 | l6 | screens[6] trap | Firm error rate 0.02, not the plain average 0.035 | correct | 0.8 × 0.01 + 0.2 × 0.06 |
| 58 | l6 | screens[7] rule and key | Parts must cover every case with no overlap (a partition); need not be equally likely, two, or independent of B | correct | BH 2.3 (law of total probability) |
| 59 | l6 | screens[8] order | Split B, add disjoint pieces, multiply each | correct | BH 2.3 proof |
| 60 | l6 | screens[9] | 0.7 × 0.4 + 0.3 × 0.8 = 0.52 | correct | arithmetic |
| 61 | l6 | summary | Result lies between the smallest and largest conditional chance | correct | script (weighted average bound) |
| 62 | l6 | quiz[0..3] | 0.034 with grade C over half the defaults; 0.27 with two thirds of flags false; 0.3; second heart 1/4 | correct | script |
| 63 | l7 | screens[1]..[3] | 8/10 one way, 8/26 the other: same overlap, different whole | correct | Ross 3.3; venn counts 2, 8, 18, 72 |
| 64 | l7 | screens[4]..[6] | Tree 0.08, 0.02, 0.18, 0.72; P(+) = 0.26; 0.08/0.26 | correct | script tree check |
| 65 | l7 | screens[7] | Leaflet 90% is P(+ given ill); patient's chance 3/7; named the inverse fallacy | correct | BH 2.8 (confusion of the inverse); script |
| 66 | l7 | screens[8] order | Bayes from P(A∩B) written two ways; either of the first two lines may come first; P(A) not 0 | correct | Ross 3.3; `same` key allows the swap |
| 67 | l7 | screens[9] | P(up given signal) = 0.44/0.575 = 88/115; an 80% detection rate is not "right 80% of the time" | correct | script |
| 68 | l7 | summary.ideas[2] | With P(A∩B) > 0 the two directions agree exactly when P(A) = P(B); if it is 0 both are 0 | correct | P(A given B)/P(B given A) = P(A)/P(B); script |
| 69 | l7 | summary.formula, trap | Bayes' rule with bottom by total probability; trap states the inverse fallacy | correct | Ross 3.3 |
| 70 | l7 | quiz[0..3] | 4/12 kings; 0.45; equal sizes give 0.6; "90% of fraud is abroad" is P(abroad given fraud) | correct | recomputed; P(A∩B) = 0.18 ≤ min |
| 71 | fluency-l7 | families[0] | From counts: key a/(a+b); inverse a/(a+c); joint a/tot; b ≠ c keeps key off the inverse | correct | script over every variable combination |
| 72 | fluency-l7 | families[1] | From rates: key = Bayes; slips inverse, joint, unweighted others; `where` keeps slips 0.002 apart | correct | script |
| 73 | fluency-l7 | families[2] | P(+) = p·s + (1 − p)·f exactly; unweighted slip adds f unweighted | correct | script; engine adds 1e-12 slack on tol 0 (`_base.js` within) |
| 74 | l8 | screens[0] | Base rate 1%, 90% and 5%: about 15%; "over five times bigger" | correct | 0.0495/0.009 = 5.5; script, MC l8 |
| 75 | l8 | screens[1] slider | Posterior crosses 0.5 between 5% and 6%; 0.49, 0.53, 0.89 at 30%, 0.95 at 50% | correct | script |
| 76 | l8 | screens[2] key and slips | P(+) = 0.0585; slip 0.059 graded "added 5% without weighting" | imprecise | finding 4: the question says "Give a decimal", and 0.0585 to 3 places is 0.059, which is graded as that slip |
| 77 | l8 | screens[3] | 2/13 ≈ 0.154; "raised the chance fifteenfold" | correct | 0.1538/0.01 = 15.4 |
| 78 | l8 | screens[4] | 11/13 of positives false; "when a condition is much rarer than the false-positive rate, most positives are false" | correct | h·b < f(1 − b) whenever b ≪ f, since h ≤ 1 |
| 79 | l8 | screens[5] | 50% base rate cancels: 0.9/(0.9 + 0.05) = 18/19 | correct | script |
| 80 | l8 | screens[6] | Clinic B's positive is likelier right; 85% false against 11% | correct | 0.035/0.305 = 0.115 |
| 81 | l8 | screens[7] formula | P = hb/(hb + f(1 − b)); f(1 − b) = 0.0495 beats hb = 0.009 | correct | Ross 3.3 |
| 82 | l8 | screens[8], [9] | Fraud 0.16; backtest 9/28; "when most candidates are noise, most winners are noise" | correct | script; tree leaves checked |
| 83 | l8 | summary | Base rate defined; trap quotes 0.15 and 0.89 | correct | script |
| 84 | l8 | quiz[0..3] | 0.24; rises less than tenfold (4.3×); 0.8; perfect detection still gives 0.505 | correct | script |
| 85 | l9 | screens[0], [1] | Grid: 8 of 10 and 9 of 90 positive; 8/17 | correct | script counts the grid cells |
| 86 | l9 | screens[2] | Natural frequencies named; 5% applies to the 990 healthy: 49.5 | correct | GH (1995) |
| 87 | l9 | screens[3], [4] | 59 positives after rounding; 9/59 ≈ 0.153 against exact 2/13; gap is rounding | correct | key 0.1525 ± 0.004 accepts both 9/59 and 2/13 |
| 88 | l9 | screens[5] | 10,000 people: 90 of 585, exactly 2/13 | correct | script |
| 89 | l9 | screens[6] trap | 240/268; the 4% applies to 700 genuine emails, not all 1,000 | correct | 0.04 × 700 = 28 |
| 90 | l9 | screens[7], [8] | False-positive rate is a share of the healthy group; method order forced | correct | definition of P(+ given not H) |
| 91 | l9 | screens[9] | 140/220 = 7/11; rates 70% and 10% | correct | script counts the grid |
| 92 | l9 | summary, quiz[0..3] | Count formula; 135 flagged; 40/135; no false positives gives 1; "about 50 of 990" | correct | recomputed |
| 93 | l10 | screens[0] | 49.5 healthy positives per 9 true: 5.5 to 1; before the test 99 to 1 | correct | counts from l9 tree |
| 94 | l10 | screens[1] | Odds = cases to non-cases = p/(1 − p); p = odds/(1 + odds); 1/6.5 = 2/13 | correct | BH 2.3 (odds) |
| 95 | l10 | screens[2] | Odds multiplied by 18 = 0.9/0.05, the likelihood ratio | correct | BH 2.3 (odds form of Bayes' rule) |
| 96 | l10 | screens[3] | On a log-odds line the same evidence is the same step wherever you start | correct | log posterior odds = log prior odds + log LR; label positions checked by script |
| 97 | l10 | screens[4] | Odds 1/4 × 6 = 3/2, p = 0.6; slips 1.2 and 6/7 | correct | arithmetic |
| 98 | l10 | screens[5] | LR = 1 leaves the odds unchanged, however often the signal fires | correct | odds form |
| 99 | l10 | screens[6] trap | Odds 1/9 × 3 = 1/3, p = 1/4; multiplying the probability gives 0.3 | correct | arithmetic |
| 100 | l10 | screens[7] order | Divide Bayes for H by Bayes for not H; P(E) cancels | correct | BH 2.3 (odds form); order pinned by "Start with Bayes' rule for H" |
| 101 | l10 | screens[8] | Four signals of LR 1.5 from 1:4; ln 4/ln 1.5 ≈ 3.42; signals fire independently "whether or not a trend has begun" | correct | script; conditional independence stated in the prose |
| 102 | l10 | summary, quiz[0..3] | "3 to 1 on" is p = 0.75; LR 4 from evens gives 0.8; 1/50 × 10 = 1/5; LR 1/4 gives 0.2 | correct | British betting usage: odds-on 3 to 1 means three wins per loss |
| 103 | l11 | screens[0] | Second test errs independently "both with and without the condition"; posterior 36/47 | correct | conditional independence given H and given not H stated; script |
| 104 | l11 | screens[1] | Order of two ratios does not matter: ×72 either way | correct | commutativity |
| 105 | l11 | screens[2] | Odds 1/99 × 18 × 18 = 324/99; p = 324/423 | correct | script |
| 106 | l11 | screens[3] | Negative has LR 0.1/0.95 = 2/19; odds 4/209; p ≈ 0.019, just above the base rate | correct | script; direction right (0.0188 > 0.01) |
| 107 | l11 | screens[4] | Negative first, positive second: exactly the same | correct | commutativity; label −6.8464 checked |
| 108 | l11 | screens[5] | "Two positives" as one piece: 0.81/0.0025 = 324 = 18 × 18, because the tests err independently | correct | needs independence given each hypothesis, stated on screens[0] and [7] |
| 109 | l11 | screens[6] trap | Restarting from 1% gives 0.154 again; right is 0.766 | correct | script |
| 110 | l11 | screens[7] order | LR1·LR2 equals the joint ratio under independent errors given H and given not H | correct | BH 2.6 coherency |
| 111 | l11 | screens[8] prose, key | Two analysts, mistakes unrelated "whichever way it goes"; 49/58; tree leaves 0.245, 0.255, 0.045, 0.455 | correct | script and MC l11 |
| 112 | l11 | screens[8].feedback.byKey.one | "The second independent call adds more." | imprecise | finding 1: the calls are dependent overall (P(both up) = 0.29, not 0.25); independence holds only given the direction |
| 113 | l11 | screens[9] | A copied call has LR 1; answer 0.7 | correct | MC l11 |
| 114 | l11 | summary | Ratios multiply for evidence that errs independently given H and given not H | correct | BH 2.6 |
| 115 | l11 | quiz[0..2] | 0.6; ratios 4 and 1/4 cancel to 0.3 not 0.5; same sample is little more than one positive | correct | arithmetic; shared error breaks conditional independence |
| 116 | l12 | screens[0], [1] | Likelihoods 0, 1/6, 1/8; "likelihoods need not add to 1; here 7/24" | correct | arithmetic |
| 117 | l12 | screens[2], [3] | Products 0, 1/18, 1/24 add to 7/72 = P(5); normalised 0, 4/7, 3/7; both live dice gained | correct | script |
| 118 | l12 | screens[4] | After a 3: 16/25 and 9/25; restart-from-1/3 slip is 4/13 | correct | script; (1/6)/(1/4 + 1/6 + 1/8) = 4/13 |
| 119 | l12 | screens[5] | A hypothesis at 0 stays at 0; called Cromwell's rule | correct | Lindley, *Making Decisions* (1985), names the rule |
| 120 | l12 | screens[6] trap | Heads-biased coin 0.32; normalising likelihoods alone gives 0.53 | correct | 0.16/0.5; 0.8/1.5 |
| 121 | l12 | screens[7] | Hypotheses "cannot overlap and whose priors add to 1"; the bottom is P(E) | correct | exclusivity and exhaustiveness both stated; BH 2.3 |
| 122 | l12 | screens[8] | Regimes after a big move: 2/9, 1/3, 4/9; crisis rose from 0.1 to 0.44, calm fell from 0.6 to 0.22 | correct | script; directions right |
| 123 | l12 | screens[9] | Random walk falls from 0.5 to 0.25 | correct | script |
| 124 | l12 | summary, quiz[0..3] | Posterior ∝ prior × likelihood; 8/47; prior 0 stays 0; equal likelihoods keep the prior ratio | correct | script; ratio of posteriors = ratio of products |
| 125 | l13 | screens[1] | Total 7 leaves first die 6 at 1/6 | correct | script |
| 126 | l13 | screens[2], [3] | Total 12 forces a first 6; independence defined as P(A given B) = P(A); dice independent, events not | correct | Ross 3.4 |
| 127 | l13 | screens[4] | Product test; table values 1/6, 1/36, 1/36, 1/216; tests agree whenever P(B) > 0 | correct | script |
| 128 | l13 | screens[5] multi | Independent of A: second die 6, even total; dependent: at least one 6 (6/11), first die even (1/3) | correct | script |
| 129 | l13 | screens[6] trap | Disjoint events with positive chances are dependent | correct | P(A∩C) = 0 ≠ P(A)P(C); Ross 3.4 |
| 130 | l13 | screens[7] order, explain | Conditional test gives the product form, which is symmetric and makes sense at P(B) = 0, "so it is the usual definition" | correct | GS 1.5 |
| 131 | l13 | screens[8] | An event is independent of itself only if P is 0 or 1 | correct | x = x²; script |
| 132 | l13 | screens[9], [10] | Tally 7, 3, 3, 7; P(up given up yesterday) = 0.7 against 0.5; small sample, a hypothesis to test | correct | script (tally and chain consistency) |
| 133 | l13 | summary, quiz[0..3] | Ace and heart independent; product 0.2; disjoint gives 0; a certain event is independent of every event | correct | P(S∩B) = P(B) = 1·P(B) |
| 134 | l14 | screens[1]..[3] | Independent trials: same chances whatever came before; products along paths; leaves checked | correct | Ross 3.4 (independent trials); script |
| 135 | l14 | screens[2] explain | 0.45⁵ = 0.0185, about once in 54; below 1% at six | correct | script |
| 136 | l14 | screens[4], [5] | Three paths with two wins, each 0.55² × 0.45; C(n,k) p^k (1 − p)^(n−k) | correct | Ross 4.6 |
| 137 | l14 | screens[6] trap | "Three independent trade ideas": 1 − 0.7³ = 0.657; adding overcounts and would pass 1 with four | correct | bare "independent" for a family means mutual by convention (GS 1.5); see finding 6 on stating it |
| 138 | l14 | screens[7] | With p = 1 the chance of exactly 7 wins in 10 is 0 | correct | 1⁷ × 0³ |
| 139 | l14 | screens[8] order | Complement, intersection, independence, numbers | correct | Ross 3.4 |
| 140 | l14 | screens[9] code | `p_at_least` sums exact binomial terms; 8 hidden tests; starter fails | correct | script runs the solution and the starter (CPython) |
| 141 | l14 | screens[9] explain, screens[10] | 0.2660; 0.1013 for 30 or more of 50; about 2 of 20 no-edge strategies clear 60% | correct | script and MC l14 |
| 142 | l14 | summary, quiz[0..3] | Needs independence and the same p; 1/16; 0.271; 0.0768; six trades | correct | recomputed |
| 143 | l15 | screens[1]..[3] | First H, second H, coins match: each pair passes the product test (pairwise independent) | correct | script |
| 144 | l15 | screens[4], [5] | P(all three) = 1/4, not 1/8; given A and B, C is certain | correct | script |
| 145 | l15 | screens[6] trap key | Pair checks alone leave P(all three) anywhere from 0 to 1/4 | correct | atoms t, 1/4 − t are non-negative exactly for t in [0, 1/4]; script; venn atoms checked |
| 146 | l15 | screens[7] | Mutual independence: product rule for every group of two or more; 11 equations for four events | correct | GS 1.5; 6 + 4 + 1 |
| 147 | l15 | screens[8] multi | Mutual gives pairwise; pairwise does not give mutual; triple equation alone does not give pairs (P(C) = 0, A = B); a chance-0 event is independent of every event | correct | counterexample valid: P(A∩A) = 1/2 ≠ 1/4 |
| 148 | l15 | screens[9], [10] | X, Y, Z: zero pairwise correlation and pairwise independent, yet all three fall with chance 1/4, twice the 1/8 | correct | script and MC l15 |
| 149 | l15 | summary.formula.note | "Neither part implies the other: check both." | correct | screens[8] counterexamples |
| 150 | l15 | whole lesson | No sentence says that "independent" for several events, unqualified, means mutually independent | imprecise | finding 6: convention used in l14, l17, review-3, homework-3, problems-3 but never stated where the distinction is taught |
| 151 | l15 | quiz[0..3] | A and "differ" independent; four equations for three events; P(D given A and B) = 0; mutual implies pairwise | correct | script |
| 152 | l16 | screens[1] | Seeing A rise raises B's chance: news flows through the sector | correct | 0.68 > 0.5; script |
| 153 | l16 | screens[2], [3] | P(both) = 0.34; P(B given A) = 0.68 | correct | script; tree leaves checked |
| 154 | l16 | screens[4] | Conditional independence given C: P(A∩B given C) = P(A given C)P(B given C); passes given a good day, fails over all days | correct | BH 2.5 (conditional independence) |
| 155 | l16 | screens[5] | P(B given A∩C) = P(B given C) = 0.8 | correct | derivation on screens[9] |
| 156 | l16 | screens[6] trap | Independence given C does not give independence: 0.34, not 0.25 | correct | BH 2.5 example; MC l16 |
| 157 | l16 | screens[7] | Alert fires on news or drop; P(news given alert) = 5/7 | correct | script |
| 158 | l16 | screens[8] key, explain | Learning the drop makes news fall to 0.2; independent causes become dependent given the shared effect | correct | direction right (0.714 to 0.2); Pearl 2.2.4; MC l16 |
| 159 | l16 | screens[9] order | Proof of P(B given A∩C) = P(B given C) with P(A∩C) > 0 | correct | each step valid |
| 160 | l16 | screens[10] | P(2 says beat given 1 says beat) = 7/12, not 0.45; correlated overall, independent given the truth | correct | script; tree leaves checked |
| 161 | l16 | summary | "Neither independence nor conditional independence implies the other" | correct | BH 2.5 |
| 162 | l16 | quiz[0..3] | Symptoms "usually not" independent overall; 0.3; crash explains the loss and the chance falls back to the prior; coin 5/6 | correct | deterministic OR gives P(bad call given crash) = prior; script |
| 163 | l17 | screens[0], [1] | Independent bars 0.5987, 0.3151, 0.0746, 0.0115; a shared shock raises P(3 or more) with each borrower still 0.05 | correct | script |
| 164 | l17 | screens[2] slider | As the recession chance rises both the 0 bar and the 3-or-more bar rise; at 0.2: 0.7269 and 0.0646 | correct | script checks monotone rise over the whole slider range |
| 165 | l17 | screens[3] | 0.2 × 0.2 + 0.8 × 0.0125 = 0.05 | correct | tree leaves checked |
| 166 | l17 | screens[4] | Pair 0.008125 against 0.0025: more than three times | correct | script |
| 167 | l17 | screens[5] key and slips | 0.2 × 0.3222 + 0.8 × 0.0002 = 0.0646; 5.6 times 0.0115 | correct | script |
| 168 | l17 | screens[5].canvas | Tree canvas whose leaves are 0.3222 and 0.0002: conditional tails, not path products, and they do not add to 1 | misleading | finding 5: l5 taught that leaves are path products and add to 1; here the prose says what they are but the caption does not |
| 169 | l17 | screens[6] trap | A binomial with p = 0.05 needs independence overall; defaults are independent only given the economy | correct | mixture of binomials is not binomial; MC l17 |
| 170 | l17 | screens[7] | All-or-nothing: P(3 or more) = 0.05, over four times 0.0115 | correct | arithmetic |
| 171 | l17 | screens[8] | P(K ≥ 3) = Σ P(r) P(K ≥ 3 given r); binomial inside each regime by independence given the regime | correct | total probability; Hull, one-factor model |
| 172 | l17 | screens[9] code | `book_tail` mixes two binomial tails; 7 hidden tests; starter fails | correct | script runs both |
| 173 | l17 | screens[10] | Pre-2008 models priced slices as if defaults were only weakly linked; falling house prices were the shared factor | correct | Hull ch. 8 |
| 174 | l17 | summary, quiz[0..3] | Diversification removes separate risks, not shared ones; book Y likelier to have no defaults; 0.05; 0.0034; large pool loses 10% with chance about 0.2 | correct | script and MC l17 (large pool) |
| 175 | review-1 | items[0], [2], [6] | 1/3; red die news leaves blue at 1/6; total 9 gives 1/2 | correct | enumeration |
| 176 | review-1 | items[1] | Neither in arrears 28/45; "not both" slip 44/45 | correct | 1 − 2/10 × 1/9 |
| 177 | review-1 | items[3] | Asked "at least two heads": all three heads 1/4 | correct | script; protocol stated |
| 178 | review-1 | items[4], [7], [8] | 3/51; 5/14; second blue 2/5 | correct | recomputed |
| 179 | review-1 | items[5], [9] | Credit tree 0.15 × 0.12 = 0.018 (branches add to 1); signal 0.18 | correct | script tree check |
| 180 | review-2 | items[0] | P(spike given down) = 30/80; reverse 30/40 | correct | venn counts add to 200 |
| 181 | review-2 | items[1], [2] | 0.1976, about 80% of flags false; 780 flagged, 300/780 fraud | correct | recomputed |
| 182 | review-2 | items[3], [4] | LR 3; 25% with LR 4 gives 4/7 | correct | odds form |
| 183 | review-2 | items[5] prose and key | Two signals of LR 3, arising independently "battle or no battle": 0.5 | correct | conditional independence stated |
| 184 | review-2 | items[5].feedback.byKey.added | "Independent ratios multiply, giving 9." | imprecise | finding 2: ratios are numbers; what is independent is the signals, given each hypothesis |
| 185 | review-2 | items[6] | Three coins after two heads: 16/33; slips 0.5517, 0.25, 0.3636 | correct | script |
| 186 | review-2 | items[7], [8] | Bayes form; the inverse equals it only when P(A) = P(B) or P(A∩B) = 0; 0.875 | correct | l7 row 68 |
| 187 | review-3 | items[0], [1] | P(A given total 8) = 3/5; disjoint events have P(A∩B) = 0, not 0.12 | correct | enumeration |
| 188 | review-3 | items[2], [3] | 1 − 0.8⁴ = 0.5904; C(4,2) 0.6² 0.4² = 0.3456 | correct | bare "independent" means mutual by convention; see finding 6 |
| 189 | review-3 | items[4], [5] | A, B, "differ" not mutually independent; all three assets fall on about 62.5 of 250 days | correct | script |
| 190 | review-3 | items[6] | Second symptom given the first: 0.117/0.27 = 0.4333, up from 0.27 | correct | recomputed |
| 191 | review-3 | items[7] | Margin call: P(A bad given call) = 0.3/0.65; given B bad it returns to 0.3 | correct | script |
| 192 | review-3 | items[8] | Two loans 0.00936; 0.048² = 0.0023; "four times likelier" | correct | 4.06 |
| 193 | homework-1 | items[0] | "You are told the total is at least 10": doubles 1/3 | correct | script; the news is the event itself |
| 194 | homework-1 | items[1], [2] | 4/17; asked "at least one 6": 1/11 | correct | script |
| 195 | homework-1 | items[3] multi | P(A given B) = 1/6; P(A given C) = 1/5; P(C given A) = 1/6; P(B given C) = 0 | correct | enumeration |
| 196 | homework-1 | items[4], [5] | 11/850; fills 0.35 × 0.55 × 0.55, "whatever came before" stated | correct | Markov assumption stated in the prose |
| 197 | homework-1 | items[6] | Asked "at least one ace": all three aces 4/4804 = 1/1201; 1/425 conditions on the first card | correct | script |
| 198 | homework-1 | items[7] order | Three-event multiplication rule, assuming P(A∩B) > 0 | correct | Ross 3.2 |
| 199 | homework-1 | items[8], [9] | Default by any route 0.0166, downgrade path almost half; grade B rate 0.06 | correct | 0.008/0.0166 = 0.48 |
| 200 | homework-1 | items[10] multi | P(B) lies between the two conditionals; equals the common value when they agree; plain sum and plain average false in general | correct | weighted average with weights in (0, 1) |
| 201 | homework-1 | items[11] model, rubric | Proof of total probability with P(A) and P(Aᶜ) positive; use gives 2/5 | correct | BH 2.3 |
| 202 | homework-2 | items[0], [1] | 0.3664; LR of 99 lifts 1% to 50% | correct | odds 1/99 × 99 = 1 |
| 203 | homework-2 | items[2] | A positive, B negative, erring independently "with or without the condition": 5/54 | correct | script |
| 204 | homework-2 | items[3] | Four dice after a 5: 0, 0.6, 0.3, 0.1; priors add to 1 | correct | products 0.05, 0.025, 0.00833 over 1/12 |
| 205 | homework-2 | items[4] order, explain | Posterior = 1/(1 + (f/h)((1 − b)/b)); reaches 1/2 only when f/h ≤ b/(1 − b) | correct | algebra; order pinned by "Start from Bayes' rule" |
| 206 | homework-2 | items[5] | Two passes, tests err independently "real edge or noise": 256/275; counts 6.4 and 0.475 | correct | script |
| 207 | homework-2 | items[6] prompt, model, rubric | Odds form derived with P(E) > 0 and P(E given not H) > 0; 2/13; n = 3; (c) says "independent repeat tests" and (d) asks for the assumption, answered as independence given H and given not H | correct | 18ⁿ > 1881; the bare word in (c) is the thing (d) asks the learner to sharpen |
| 208 | homework-2 | items[7], [8] | Shared source is little more than one piece of evidence; warning with LR 1/3 for a beat gives 1/3 | correct | odds 1.5 × 1/3 |
| 209 | homework-2 | items[9] model parts 1, 2 | One flag from the multiplication rule with P(J) > 0; two flags need independent flagging on bad ticks and on good ticks, each used where shown | correct | BH 2.6; both halves of conditional independence named |
| 210 | homework-2 | items[9] model parts 3, 4, rubric | 15/64, 50/57; shared stale quote: P(J∩V given G) = 0.03, answer 3/10; second-update check 1.4 | correct | script |
| 211 | homework-3 | items[0] | 33/60 = 77/140 = 110/200: signal independent of up days in this data | correct | arithmetic |
| 212 | homework-3 | items[1], [2] | 0.7¹² = 0.01384, about once in 72; nine trades for 0.999 | correct | recomputed |
| 213 | homework-3 | items[3] multi | P(Z falls given X falls) = 1/2; given both, 1; not mutually independent; all three never rise | correct | four states |
| 214 | homework-3 | items[4] | Both analysts say beat: 6/7; copied calls would not be independent given the truth | correct | 0.225/0.2625 |
| 215 | homework-3 | items[5] | Five loans: 0.1 × 0.5125 + 0.9 × 0.0038 = 0.0547, about 2.4 times 0.0226 | correct | recomputed by hand and against the l17 hidden test value 0.0547086 |
| 216 | homework-3 | items[6] order | A and B independent gives A and Bᶜ independent | correct | Ross 3.4 (independence of E and the complement of F) |
| 217 | homework-3 | items[7] model | P(D1∩D2) − P(D1)P(D2) = q(1 − q)(p_b − p_g)²; never negative; zero exactly when q is 0 or 1 or p_b = p_g; 0.005625 | correct | script (identity on a grid) |
| 218 | problems-1 | items[0] | 7/64; asked "at least one 8": 2/15; reverse 2/7; joint 1/32 | correct | script; protocol stated in part 2 |
| 219 | problems-1 | items[1] | 5/18; 4/7; 10/63; 10/21; given exactly two banks the miner was third with chance 1/3; unconditional third-pick miner 4/9 | correct | recomputed; exchangeability |
| 220 | problems-1 | items[2] | 0.3; 0.72; 0.944; 0.98; Z first wins by 0.036; re-send fills with 0.8 "whatever happened before" | correct | arithmetic; assumption stated |
| 221 | problems-1 | items[3] | 4/15; 1/6; 5/6; given a stop on call 2 or 3, call 2 has 8/13 | correct | script |
| 222 | problems-2 | items[0] | 180; 456; 180/456; break-even base rate 0.06/0.51 | correct | 0.45b = 0.06(1 − b) |
| 223 | problems-2 | items[1] parts[0..1] | Prior odds 3/17; delay LR 3 gives 9/17 | correct | odds form |
| 224 | problems-2 | items[1] parts[2] key | Exit LR 6: odds 54/17, p = 54/71 | correct | script |
| 225 | problems-2 | items[1] parts[2] byKey.ratio-sum | "Independent evidence multiplies" | imprecise | finding 3: the kind is independence given the truth, as the item's own prose says |
| 226 | problems-2 | items[1] parts[3] question | "how many more independent reports, each with ratio 3"; key 2 | imprecise | finding 3: key right (9.53 then 28.6 against 19); bare word where the conditional kind is needed |
| 227 | problems-2 | items[1] parts[4] feedback.correct | "The exit was not independent of the delay" | imprecise | finding 3: exit and delay were never independent overall; what fails is independence given the truth |
| 228 | problems-2 | items[1] parts[4] key and explain | The exit partly repeats the delay, so 0.76 is too high | correct | double counting; explain names "arise independently" as defined in the prose |
| 229 | problems-2 | items[2] | 0.46; 16/46; 16/31; next fill 0.6185 | correct | script |
| 230 | problems-2 | items[3] | 0.0582; 0.3265; after B 0.9714; 392 good prints; share 0.0286 | correct | recomputed; filters err independently "given the truth" stated |
| 231 | problems-3 | items[0] | 0.65 both ways, product test 0.195; 4 × 0.65³ × 0.35 = 0.3845; 1 − 0.65⁴ = 0.8215 | correct | recomputed |
| 232 | problems-3 | items[1] | 0.475; 12/19; squeeze returns the signal to 0.3; given a loss the causes are dependent | correct | script; Pearl 2.2.4 |
| 233 | problems-3 | items[2] | 0.1; 0.005536; model 0.001; ratio 5.536 | correct | recomputed |
| 234 | problems-3 | items[3] | Three desks sharing feeds: pairwise independent, P(all calm) = 1/4, P(C given A∩B) = 1; 1 − 0.75⁸ = 0.8999 | correct | script |

## Cross-cutting rows

| # | Scope | Claim (short) | Verdict | Basis |
|---|---|---|---|---|
| 235 | every tree canvas in scope with `levels` | Branches out of each node add to 1; shown leaves equal path products and add to 1 | correct, bar row 168 | script, generic tree check over all 27 files |
| 236 | count trees (l9, l10) | Children add to the parent count; first stage adds to the crowd | correct | script |
| 237 | every numeric widget in scope | No listed slip value lies inside the accepted band of the key | correct | script |
| 238 | every summary `trap` line, l1 to l17 | The trap as described gives the stated wrong answer or names the right slip | correct | read one by one against the trap screen of each lesson |
| 239 | direction words in explanations (rose, fell, up from, down from, back to) | Each matches the item's own numbers | correct | read one by one; the pairs checked include l1 s3, s4; l2 s1; l3 s2; l8 s3; l11 s3; l12 s8, s9; l16 s8; l17 s2; review-3 items[6], [7]; problems-3 items[1] |
| 240 | "at least one" and "you are told" items | The prose says how the news arose (a yes to a stated question), or the news is a plain event about a total | correct | l3 s3, s7; review-1 items[3]; homework-1 items[2], [6]; problems-1 items[0] part 2 |
| 241 | law of total probability and many-hypothesis Bayes | Parts are exclusive and exhaustive wherever used (weights add to 1) | correct | l6 s7; l12 s7 states both conditions; every prior list in scope adds to 1 |
| 242 | odds against probability | Odds always cases to non-cases; conversions p = odds/(1 + odds) | correct | l10, l11, review-2, homework-2, problems-2 read against BH 2.3 |
| 243 | natural-frequency counts | Counts match the stated rates | correct | l7 venn, l9 grids and trees, review-2 items[2], problems-2 items[0], items[3] |

## Verdict counts

243 rows: 235 correct, 0 wrong, 7 imprecise (rows 76, 112, 150, 184, 225, 226, 227), 1 misleading (row 168), 0 unverified. Rows 225 to 227 belong to one finding. Row 235 is correct for every tree except the one recorded at row 168.

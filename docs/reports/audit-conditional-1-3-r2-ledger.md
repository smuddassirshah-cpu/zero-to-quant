# Claim ledger, round 2: conditional levels 1 to 3

Auditor: blind Fable reader, round 2. Written before any earlier audit, review, ledger, concepts script or author report of this course was opened.

Scope: `app/content/courses/conditional/` files `l1` to `l17`, `review-1` to `review-3`, `homework-1` to `homework-3` (with the performance task `h-two-filters`), `problems-1` to `problems-3` and `fluency-l7-turning-around`. Stage 1, so full ledger depth.

Rows: 459. Verdicts: correct 443, wrong 3, imprecise 13, misleading 0, unverified 0. The 3 wrong rows make findings 1 and 2; the 13 imprecise rows make findings 3 to 10.

How to read a row. Each row is one claim, or the lines of one screen that state the same fact (key, slip values and their feedback; or hints and feedback; or the explanation). Every line in a grouped row was read against the recomputed value; none was passed by pattern. A sentence with its own rule, definition, condition or "always, never, only" claim has its own row.

File codes: `l1` to `l17` are the lesson files, `rv` review, `hw` homework, `pb` problems, `fl7` the fluency set.

Basis codes:
- E: exact enumeration of the outcome space with fractions, in `docs/reports/conditional-L<n>-concepts-r2.py`.
- D: a short derivation, also recomputed in the same script.
- MC: seeded Monte Carlo in the same script; the estimate is quoted.
- S: a named source. BH is Blitzstein and Hwang, *Introduction to Probability*, second edition, chapter 2 (2.2 definition, 2.3 Bayes' rule, total probability and odds form, 2.5 independence, pairwise and conditional independence, 2.6 coherence of updating, 2.8 pitfalls) and chapter 3 (3.3 Bernoulli and binomial). Other sources are named in the row.
- trees(): the generic check that the branches out of every tree node add to 1 and each stated leaf equals the product along its path.

## Level 1: Updating on evidence

### l1-what-changes

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | screens[1] key | told "even", a 6 is more likely than before | correct | E: 1/3 > 1/6. Protocol: the friend reports parity; read as the answer to a fixed question (made explicit in l3 screens[3]) |
| l1 | screens[1] why ×2 | "same" keeps six faces; "less" forgets 6 is even | correct | E: 1, 3, 5 leave, 6 stays |
| l1 | screens[1] hints, feedback | 6 is one face of six before, one of three after | correct | E |
| l1 | screens[1].explain | fewer faces share the whole chance, so each survivor gets a bigger share | correct | D: equally likely survivors renormalise; BH 2.2 |
| l1 | screens[2] key, wrongs, byKey | survivors are 2, 4, 6; odd faces are ruled out | correct | E |
| l1 | screens[2].explain | the three marked faces are all that is left to count | correct | BH 2.2 (conditioning restricts the sample space) |
| l1 | screens[3].prose | notation P(6 given even), read "given" | correct | S: standard notation, BH Def 2.2.1 |
| l1 | screens[3] key | P(6 given even) = 1/3 | correct | E |
| l1 | screens[3] wrongs | 1/6 is the prior; 1/2 splits 6 against not-6 (two faces are not 6) | correct | E |
| l1 | screens[3] hints, feedback | one face of three, each equally likely | correct | E |
| l1 | screens[3].explain | news doubled the chance by halving what is left | correct | D: 1/3 = 2 × 1/6; three of six faces remain |
| l1 | screens[4] key | P(even given greater than 3) = 2/3 | correct | E: {4, 5, 6}, evens 4 and 6 |
| l1 | screens[4] why ×3 | 1/2 prior; 2/6 divides by six; 1/3 counts the odd face 5 | correct | E |
| l1 | screens[4] hints, explain | right circle holds 4, 5, 6; overlap 4, 6; up from 1/2 | correct | E; Venn values 2 / 4,6 / 5 / 1,3 partition the six faces |
| l1 | screens[5] key | P(1 given greater than 3) = 0 | correct | E |
| l1 | screens[5] wrongs | 1/6 prior; 1/3 gives 1 a share it does not have | correct | E |
| l1 | screens[5].explain | news can push a chance to zero; a ruled-out outcome has chance 0 | correct | D: A∩B empty gives P(A given B) = 0 |
| l1 | screens[6] key | even given at most 4 stays at 1/2 | correct | E: 2/4 |
| l1 | screens[6] why, byKey | rises: assumed news always changes a chance; falls: counted only the 6 that left | correct | E: 6 and 5 both left |
| l1 | screens[6].explain (a) | removed one even and one odd face, so the share did not move | correct | E for this case |
| l1 | screens[6].explain (b) | "News changes a chance only when it removes outcomes unevenly" | imprecise | D: unchanged iff the share of A among removed outcomes equals P(A). Removing one A face and one non-A face from A = {1, 2} moves 1/3 to 1/4 (r2 L1 script). Finding 4 |
| l1 | screens[7].prose | equally likely outcomes: P(A given B) = (outcomes in both) / (outcomes in B) | correct | BH 2.2; hypothesis "equally likely" is stated |
| l1 | screens[7] key, why ×2 | the bottom is what the news allows, not A and not everything | correct | D |
| l1 | screens[7] hints, explain | divided by 3 (even), 3 (above 3), 4 (at most 4) | correct | E |
| l1 | screens[8] key | P(up given high volume) = 56/80 = 0.7 | correct | E on the Venn counts 24, 56, 64, 56 = 200 |
| l1 | screens[8] wrongs | 0.6 = 120/200; 0.4667 = 56/120; 0.28 = 56/200 | correct | E |
| l1 | screens[8].explain | 0.7 against 0.6: volume "tells you something about the direction in this dataset" | correct | E; hedged to the dataset, no causal claim |
| l1 | summary.ideas | news rules outcomes out; count inside what is left; can raise, zero or leave a chance | correct | lesson body; BH 2.2 |
| l1 | summary.formula + note | counting formula, "For equally likely outcomes" | correct | hypothesis stated |
| l1 | summary.trap | news does not always change a chance | correct | screens[6] |
| l1 | quiz[0] | heart given red = 1/2; slips 1/4, 1, 1/26 | correct | E on 52 cards |
| l1 | quiz[1] | 6 given at least 3 = 1/4; slips 1/6, 1/3 (dropped the 3) | correct | E |
| l1 | quiz[2] | at most 3 given odd = 2/3; slips 1/2, 1/3, 2/6 | correct | E |

### l2-counting-left

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l2 | screens[0].prose | without replacement the bag changes; each draw is counted on what the last left | correct | BH 2.3 |
| l2 | screens[1] key, why ×3 | after a seen red: 2/4; slips 3/5, 2/5, 3/4 | correct | E over 20 ordered pairs |
| l2 | screens[1].explain | 2/4, down from 3/5 | correct | E |
| l2 | screens[2] | 20 ordered pairs; six both red; diagonal impossible | correct | E |
| l2 | screens[3] key, wrongs | P(2nd red given 1st red) = 6/12; 0.3 divides by 20; 0.6 puts back | correct | E |
| l2 | screens[3].explain | grid and bag agree: 6/12 = 2/4 | correct | E |
| l2 | screens[4] key, wrongs | after blue: 3/4; slips 0.6, 0.5, 0.25 | correct | E |
| l2 | screens[4].explain | each branch leaves a different bag | correct | D |
| l2 | screens[5] key, wrongs | both red = 6/20 = 0.3; slips 0.36, 0.5, 0.6 | correct | E |
| l2 | screens[5] hints, explain | 3/5 of the time, then 2/4 of that: 3/5 × 2/4 = 6/20 | correct | D: multiplication rule |
| l2 | screens[6] key | unseen first draw: second is red with 12/20 = 3/5 | correct | E; MC 0.600 |
| l2 | screens[6] wrongs | 0.5 assumes red; 0.75 assumes blue; 0.625 is the equal average of 2/4 and 3/4 | correct | E; weighted 3/5·1/2 + 2/5·3/4 = 3/5 |
| l2 | screens[6].explain | a hidden first draw tells you nothing; the bag changes for you once you see | correct | D: exchangeability, BH Ex 2.3; total probability |
| l2 | screens[7].prose | P(A∩B) = P(A) P(B given A), "multiplication rule" | correct | BH Thm 2.3.1. P(A) > 0 is implied by the conditional being defined (l3 summary) |
| l2 | screens[7] key, why ×3 | blue, blue = 2/5 × 1/4 = 1/10 = 2 cells of 20 | correct | E |
| l2 | screens[8] | 6/20 = 12/20 × 6/12; slips 3/5, 12/6, 6/20 | correct | D; accept list all equal 1/2 |
| l2 | screens[8].explain | first factor P(1st red), second P(2nd red given 1st red); the rule is the count split in two | correct | D |
| l2 | screens[9] key, wrongs | 4/10 × 3/9 = 2/15; slips 0.16, 3/9, 0.4 | correct | E over 90 ordered picks |
| l2 | screens[9].explain | sampling without repeats is drawing without replacement | correct | D |
| l2 | summary.ideas[2], trap | with no news about the first draw, the second has the same chance as the first | correct | E; symmetry |
| l2 | quiz[0] | second faulty given first faulty = 1/5; slips 2/6, 2/5, 1/15 (both) | correct | E |
| l2 | quiz[1] | two aces = 1/221 = 0.004525; slips (4/52)², 3/51 | correct | D |
| l2 | quiz[2] | unseen first, second blue = 2/5; 3/10 + 1/10 | correct | E |

### l3-shrinking

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l3 | screens[1] | five outcomes total 8; P = 5/36; byKey sums (7s and 9s) | correct | E |
| l3 | screens[2].prose | "A friend peeks and tells you the first die shows 5" | correct | protocol: a report about a named die; contrasted with the asked question on screens[3] |
| l3 | screens[2] key, why ×3 | P(total 8 given first is 5) = 1/6; slips 5/36, 1/36, 5/6 | correct | E |
| l3 | screens[3].prose | you ask "does at least one die show a 5?"; yes, and nothing more | correct | protocol stated: a fixed yes/no question, so the event is exactly "at least one 5" |
| l3 | screens[3] key, wrongs | 11 outcomes; slips 12, 10, 6, 36, 25 | correct | E: 6 + 6 − 1 |
| l3 | screens[4] key, why ×3 | P(total 10 given at least one 5) = 1/11; slips 1/6, 1/12, 3/36 | correct | E; MC 0.091 |
| l3 | screens[4].explain | before the news 3/36 = 1/12 | correct | E |
| l3 | screens[5] order | counted, divide by 36, name the probabilities | correct | D |
| l3 | screens[5].explain | P(A∩B)/P(B) "is taken as the definition when outcomes are not equally likely" | correct | BH Def 2.2.1 |
| l3 | screens[6] key, wrongs | about 1000 × 11/36 = 305.6 kept; slips 91, 167, 333, 1000 | correct | E; MC 0.3056; sim expression has chance 11/36 |
| l3 | screens[7].prose | two stocks, equal chance, independent; you ask whether at least one rose | correct | protocol stated |
| l3 | screens[7] key, why ×3 | both up given at least one up = 1/3; slips 1/4, 1/2, 2/3 | correct | E |
| l3 | summary.ideas | new sample space; count; P(A∩B)/P(B) is the definition for any outcomes | correct | BH 2.2 |
| l3 | summary.formula.note | defined only when P(B) > 0 | correct | condition stated |
| l3 | summary.trap | "at least one is a 5" leaves 11 outcomes, "the first is a 5" leaves 6 | correct | E |
| l3 | quiz[0] | a 3 showing given total 7 = 1/3; reversed = 2/11 | correct | E |
| l3 | quiz[1] | greater than 3 given even = 2/3 | correct | E |
| l3 | quiz[2] | both up given A up = 1/2; at-least-one gives 1/3; 3/4 is P(at least one) | correct | E |

### l4-multiplication-rule

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l4 | screens[1], [2] | after 9H: 3 hearts of 5; after 3S: 4 hearts of 5 | correct | E on the 6-card deck |
| l4 | screens[2].explain | the second deal's chance depends on what the first took | correct | D |
| l4 | screens[3].prose | P(A∩B) = P(A) P(B given A) | correct | BH Thm 2.3.1 |
| l4 | screens[3] key, wrongs | both hearts = 4/6 × 3/5 = 2/5; slips 0.4444, 0.6, 0.6667, 0.5333 | correct | E over 30 deals |
| l4 | screens[4] key, wrongs | three hearts = 1/5; slips (4/6)³ = 0.2963, 0.4, 0.5 | correct | E over 120 deals; MC 0.200 |
| l4 | screens[5] key, wrongs | with replacement 4/9; slips 0.4, 0.6667, 1.3333 (added) | correct | D |
| l4 | screens[5].explain | "the edge case where P(B given A) = P(B)" | correct | D; names independence without the word, consistent with l6 and l13 |
| l4 | screens[6] key, why ×3 | Sam's 4/9 is wrong; 2/5; slips 8/15, 2/3 | correct | E: 12 of 30 |
| l4 | screens[6].explain | Sam's 4/6 for the second card is right only when the first is unseen; 16/36 counts the diagonal | correct | E: P(2nd heart) = 4/6 |
| l4 | screens[7].prose | P(A∩B∩C) = P(A) P(B given A) P(C given A∩B) | correct | BH Thm 2.3.2 |
| l4 | screens[7] key, why ×3 | heart, spade, heart = 4/6 × 2/5 × 3/4 = 1/5 | correct | E |
| l4 | screens[8] | P(B) = 10/30, P(A given B) = 8/10; both orders give 8/30 | correct | E; symmetry of the rule |
| l4 | screens[9] key, wrongs | 0.4 × 0.6 = 0.24; slips 0.16, 0.6, 1.0 | correct | D; last month's share is used as the first-fill chance (stated set-up) |
| l4 | screens[9].explain | 0.16 "understates the clustering by a third" | correct | D: (0.24 − 0.16)/0.24 = 1/3 |
| l4 | summary.ideas, formula, trap | chain of factors; either order; with replacement a plain product; P(A)P(B) is wrong when the first draw changes the second | correct | BH 2.3 |
| l4 | quiz[0] | 3/12 × 2/11 = 1/22 | correct | D |
| l4 | quiz[1] | ace then king = 4/663; slips 1/169, 1/221, 2/13 | correct | D |
| l4 | quiz[2] | with replacement, two hearts 1/16; kept-out 1/17 | correct | D |
| l4 | quiz[3] | three seniors 1/10; slips 0.216, 0.3 | correct | D |

### l5-trees

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | screens[1] cells, byKey | 4/7, 3/7, 5/7, 2/7 | correct | E over 56 ordered pairs |
| l5 | screens[1].explain | second-stage numbers depend on the branch they hang from | correct | D |
| l5 | screens[2] | route white, white is two branches; each route is one outcome | correct | D |
| l5 | screens[3].prose | a path is one outcome of both draws | correct | definition |
| l5 | screens[3] key, wrongs | 3/8 × 2/7 = 3/28; slips 9/64, 0.6607 (added), 2/7 | correct | E |
| l5 | screens[4] cells | 20/56, 15/56, 15/56, 6/56, total 1 | correct | E; trees() |
| l5 | screens[4].explain | every outcome lies on exactly one path, so a tree's leaves always add to 1 | correct | D: paths partition the sample space |
| l5 | screens[5] | white, white has chance 0 with one white sock; a zero branch can be pruned | correct | E |
| l5 | screens[6] key, wrongs | 5/8 × 4/7 × 3/6 = 5/28; slips 0.1465, 0.1339, 0.1531 | correct | E over 336 triples |
| l5 | screens[7] key, why ×3 | true black, white = 15/56; Kim 15/64; added 59/56; branch 3/7 | correct | E |
| l5 | screens[7].explain | Kim's leaves still add to 1, so the check cannot catch the slip | correct | E: 64/64 |
| l5 | screens[8].prose | first-stage branch P(A); branch off A carries P(B given A); leaves add to 1 | correct | BH 2.3 |
| l5 | screens[8] key, why ×3 | the branch is P(2nd black given 1st white), not P(2nd black), the leaf, or the reverse | correct | D |
| l5 | screens[8].explain | with no news the second sock is black with 5/8, "a third number" | correct | E |
| l5 | screens[9] order, explain | leaves after one node add to that node's chance; proof needs only each node's branches adding to 1 | correct | D |
| l5 | screens[10] key, wrongs | 0.6 × 0.45 = 0.27; slips 0.312, 0.45, 1.05, 0.6 | correct | D |
| l5 | screens[10].explain | fills arrive on worse days; the gap is adverse selection | correct | S: Glosten and Milgrom (1985); O'Hara, Market Microstructure Theory ch. 3 |
| l5 | summary.ideas, formula, trap | multiply along a path; leaves adding to 1 do not prove a tree right | correct | screens[7], [9] |
| l5 | quiz[0] | downgrade then default 0.004, "4 bonds in 1,000" | correct | D |
| l5 | quiz[1] | branch 12/51; leaf 1/17 | correct | D |
| l5 | quiz[2] | fourth leaf 0.12; slips 0.88, 0.72 | correct | D |
| l5 | quiz[3] | blue, blue is the zero path; others 1/2, 1/4, 1/4 | correct | E |

### l6-adding-branches

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | screens[1] | two red leaves, 3/12 and 2/12; "one path or the other, never both" | correct | E; trees() |
| l6 | screens[2] key, why ×3 | chance of red moves from 1/4 to 3/4 as the bag-A chance goes 0 to 1 | correct | D: 0.75p + 0.25(1 − p) |
| l6 | screens[2].explain | a weighted average, pulled towards the more likely bag | correct | D |
| l6 | screens[3].prose | adding every path that ends in red is the law of total probability | correct | BH Thm 2.3.6 |
| l6 | screens[3] key, wrongs | 5/12; slips 0.5 (average), 0.25, 0.1667, 1.0 | correct | E; MC 0.4167 |
| l6 | screens[3].explain | paths cannot both happen, so their chances add; nearer bag B's 1/4 | correct | D |
| l6 | screens[4] key, wrongs | 11/24; slips 0.5833, 1.75, 0.125 | correct | D |
| l6 | screens[4].explain | any number of first-stage branches, if they cover every case without overlap | correct | partition condition stated |
| l6 | screens[5] key, wrongs | all bags 1/4, so 1/4; slips 0.75, 1/12 | correct | D |
| l6 | screens[5].explain | equal conditional chance in every bag means the bag tells you nothing: independence | correct | D: P(B given A_i) = P(B) for all i |
| l6 | screens[6] key, why ×3 | 0.8 × 0.01 + 0.2 × 0.06 = 0.02; slips 0.035, 0.07, 0.012 | correct | D |
| l6 | screens[7].prose | if A_1..A_n cover every case without overlap, P(B) = Σ P(B given A_i) P(A_i) | correct | BH Thm 2.3.6; P(A_i) > 0 implied by the conditionals |
| l6 | screens[7] why "independent" | if the branches were independent of B every term would equal P(B) | correct | D |
| l6 | screens[7].explain | a set of branches that covers every case once is a partition | correct | definition |
| l6 | screens[8] order, explain | split B, add (disjoint axiom), multiply each piece | correct | D: Kolmogorov additivity |
| l6 | screens[9] key, wrongs | 0.7 × 0.4 + 0.3 × 0.8 = 0.52; slips 0.6, 1.2, 0.28, 0.24 | correct | D |
| l6 | summary.ideas[2] | a weighted average, so it lies between the smallest and largest conditional | correct | D; random check in r2 L1 script |
| l6 | summary.formula.note, trap | parts must cover every case once; do not average or add unweighted | correct | D |
| l6 | quiz[0] | 0.034; grade C is a fifth of the book, more than half the defaults (59%) | correct | D |
| l6 | quiz[1] | 0.27; two thirds of flags on days with no drop | correct | D: 0.18/0.27 |
| l6 | quiz[2] | same rate 0.3 in every phase gives 0.3 | correct | D |
| l6 | quiz[3] | unseen first card, second a heart = 1/4 (156 + 507 = 663 of 2652) | correct | D |

### review-1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| rv1 | items[0] | 6 given even = 1/3 | correct | E |
| rv1 | items[1] | neither in arrears 8/10 × 7/9 = 28/45; not-both = 0.9778 | correct | D |
| rv1 | items[2] | blue 6 given red 4 = 1/6; news about the other die does not move it | correct | E; fair separate dice |
| rv1 | items[3] | asked "at least two heads?": all three = 1/4; slips 1/8, 1/2 | correct | E on 8 outcomes; protocol stated |
| rv1 | items[4] | second king 3/51; slips 4/52, 3/52 (bands do not overlap) | correct | D |
| rv1 | items[5] | 0.15 × 0.12 = 0.018; the 0.12 is already conditional | correct | D; trees() |
| rv1 | items[6] | first die even given total 9 = 2/4 | correct | E |
| rv1 | items[7] | two reds 5/14; slips 25/64, 5/16 | correct | D |
| rv1 | items[8] | second blue 2/5 | correct | E |
| rv1 | items[9] | signal fires 0.12 + 0.06 = 0.18 | correct | D |

### homework-1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| hw1 | items[0] key | doubles given total at least 10 = 2/6 | correct | E |
| hw1 | items[0] why b, c | 1/6 prior; 1/2 counts two against two | correct | E |
| hw1 | items[0] why d | "Only six totals reach 10" | imprecise | E: six outcomes, three totals (10, 11, 12). Finding 10 |
| hw1 | items[1] | second heart 12/51 = 4/17; slips 1/4, 13/51, 3/51 | correct | D |
| hw1 | items[2] | asked "at least one 6?": both sixes 1/11 | correct | E; protocol stated |
| hw1 | items[3] | true: P(A given B) = 1/6, P(C given A) = 1/6, P(B given C) = 0; P(A given C) = 1/5 | correct | E |
| hw1 | items[4] | three hearts 11/850 = 0.012941; item 8 is the three-event rule | correct | D; item order checked |
| hw1 | items[5] | 0.35 × 0.55 × 0.55 = 0.105875, "whatever came before" (Markov step stated); about 2.5 times 0.042875 | correct | D: 2.47 |
| hw1 | items[6] | asked "at least one ace?": all aces 4/4804 = 1/1201; slips 1/425, 1/5525, 1/221 | correct | E by counting hands; MC 0.00083 |
| hw1 | items[7] | three-event rule from the two-event rule, assuming P(A∩B) > 0 | correct | D; condition stated |
| hw1 | items[8] | 0.0001, 0.0085, 0.008, total 0.0166; downgrade path nearly half the risk (48%) | correct | D |
| hw1 | items[9] | grade B rate 0.06; slips 0.018, 0.051, 0.024 | correct | D |
| hw1 | items[10] | always true: P(B) between the two conditionals; equal conditionals give that value | correct | D: weighted average with 0 < P(A) < 1 stated |
| hw1 | items[11].model, rubric | proof of total probability with P(A) > 0 and P(A^c) > 0 named; use gives 2/5 | correct | D; rubric sums to 10 |

### problems-1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| pb1 | items[0].parts[0] | two d8, total 10: 7/64; slips 4/64, 8/64, 3/36 | correct | E on 64 outcomes |
| pb1 | items[0].parts[1] | asked "at least one 8?": total 10 has 2/15 | correct | E; protocol stated |
| pb1 | items[0].parts[2] | reverse: an 8 given total 10 = 2/7 | correct | E |
| pb1 | items[0].parts[3] | joint 7/64 × 2/7 = 1/32; plain product 7/64 × 15/64 is wrong | correct | E |
| pb1 | items[1].parts[0..2] | bank, bank 5/18; miner third 4/7; path 10/63 | correct | E over 504 ordered picks |
| pb1 | items[1].parts[3] | exactly two banks 30/63; six-orders slip 60/63 | correct | E |
| pb1 | items[1].parts[4] | miner third given exactly two banks = 1/3 (the three orders are equally likely) | correct | E |
| pb1 | items[2].parts[0..1] | X and fills 0.3; first-venue fill 0.72 | correct | D |
| pb1 | items[2].parts[2] | within two tries 0.72 + 0.28 × 0.8 = 0.944; re-send fills with 0.8 "whatever happened before" stated | correct | D |
| pb1 | items[2].parts[3..4] | Z first 0.98; wins by 0.036 | correct | D |
| pb1 | items[3].parts[0..1] | first good quote on call 2: 4/15; on call 3: 1/6 | correct | E over 720 ordered triples |
| pb1 | items[3].parts[2] | within three calls 5/6; all three miss 1/6 | correct | E |
| pb1 | items[3].parts[3] | call 2 given within three and not call 1 = 8/13; slips 0.32, 4/15, 5/13, 0.625 | correct | E |

## Level 2: Bayes' rule

### l7-turning-around

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l7 | screens[1] key, wrongs | P(+ given ill) = 8/10; slips 0.08, 8/26, 0.1 | correct | E on Venn 2, 8, 18, 72 |
| l7 | screens[2] | 26 positives: 8 ill, 18 well; "the new whole we count inside" | correct | E |
| l7 | screens[3] key, wrongs | P(ill given +) = 8/26 = 0.3077; slips 0.8, 0.08, 18/26 | correct | E |
| l7 | screens[3].explain | same overlap, different whole; turning the condition round changes the answer | correct | BH 2.8 (confusion of the inverse) |
| l7 | screens[4], [5] | P(ill and +) = 0.08; P(+) = 0.26; slips incl. unweighted 1.0 and 0.5 | correct | D; trees() |
| l7 | screens[6] key, why ×3 | 0.08/0.26 ≈ 0.31; joint 0.08; well 0.69; 0.08/0.1 is P(+ given ill) again | correct | D |
| l7 | screens[7] key, why ×3 | leaflet 90%, base rate 20%, false positives 30%: P(ill given +) = 3/7 | correct | D: 0.18/0.42 |
| l7 | screens[7].explain | swapping the condition is "the inverse fallacy" | correct | S: also "confusion of the inverse", "transposed conditional" |
| l7 | screens[8] order | P(A∩B) two ways, set equal, divide by P(A) "which is not 0" | correct | BH Thm 2.3.3; condition stated |
| l7 | screens[8].explain | the bottom P(A) is every path into A | correct | total probability |
| l7 | screens[9] key, wrongs | P(up given signal) = 0.44/0.575 = 0.7652; slips 0.8, 0.44, 0.55, 0.575 | correct | D; MC 0.765 |
| l7 | screens[9].explain | an 80% detection rate does not make the signal right 80% of the time | correct | D: 76.5% here, and it moves with the base rate |
| l7 | summary.ideas[0..1] | the two conditionals share a top but divide by different groups, so they usually differ | correct | D |
| l7 | summary.ideas[2] | when P(A∩B) > 0 they agree exactly when P(A) = P(B); if it is 0 both are 0 | correct | D: P(AB)/P(A) = P(AB)/P(B); random check in r2 L2 script |
| l7 | summary.formula + note | Bayes' rule; P(A) = P(A given B)P(B) + P(A given B^c)P(B^c) | correct | BH 2.3 |
| l7 | summary.trap | catching 90% of the ill does not make a positive 90% likely to be right | correct | screens[7] |
| l7 | quiz[0] | king given face card = 4/12 | correct | E |
| l7 | quiz[1] | P(A given B) = 0.6 × 0.3/0.4 = 0.45; upside-down 0.8 | correct | D; inputs are coherent (P(AB) = 0.18) |
| l7 | quiz[2] | equal marginals give equal conditionals: 0.6 | correct | D |
| l7 | quiz[3] | "90% of fraudulent payments are made abroad" is P(abroad given fraud) | correct | D |

### l8-base-rates

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l8 | screens[0] key, why ×3 | 1%, 90%, 5%: about 15% | correct | D: 0.009/0.0585 = 0.1538; MC 0.154 |
| l8 | screens[0].explain | healthy-and-positive 0.0495 is "over five times" 0.009 | correct | D: 5.5 |
| l8 | screens[1] key, hints, why | crosses 0.5 between 5% and 6% (0.49, 0.53); 0.89 at 30%; 0.95 at 50% | correct | D: threshold f/(h + f) = 0.0526 |
| l8 | screens[1].explain | the test never changed, only how common the condition is | correct | D |
| l8 | screens[2].prose | "how common the condition is before any test" is the base rate | correct | definition (prior probability, prevalence) |
| l8 | screens[2] key, wrongs | P(+) = 0.0585; slips 0.009, 0.059 (unweighted), 0.95 | correct | D |
| l8 | screens[3] key, explain | 2/13 = 0.1538; "raised the chance fifteenfold" | correct | D: 15.4 times |
| l8 | screens[4] key, wrongs | share of positives that are false 11/13 = 0.8462; 0.05 is the rate among the healthy | correct | D |
| l8 | screens[4].explain | "When a condition is much rarer than the false-positive rate, most positive tests are false" | correct | D: posterior < 1/2 iff h·b < f(1 − b); grid check with b ≤ f/2 in r2 L2 script |
| l8 | screens[5] key, explain | at a 50% base rate 18/19; the 0.5 cancels, only the two rates are left | correct | D |
| l8 | screens[6] key, byKey, explain | clinic B (30%): 0.27/0.305 = 0.89; clinic A 0.15; 85% and 11% false | correct | D |
| l8 | screens[6].explain | a positive cannot be turned into a chance without the base rate of the people tested | correct | D; assumes the test's two rates carry over to the symptomatic group (set-up says "the same test") |
| l8 | screens[7].prose | P(condition given +) = hb / (hb + f(1 − b)) | correct | D |
| l8 | screens[7] key, why, explain | f(1 − b) = 0.0495 beats hb = 0.009; healthy group is 99 times larger | correct | D |
| l8 | screens[8] | fraud flag: 0.0019/0.01188 = 0.16; slips 0.95, 0.0019, 0.99 | correct | D |
| l8 | screens[9] | backtest pass: 0.045/0.14 = 9/28; "when most candidates are noise, most backtest winners are noise too" | correct | D; S: Harvey, Liu and Zhu (2016) on false discoveries |
| l8 | summary.ideas, formula, trap | base rate belongs in every calculation; rare against f; 50% cancels; 0.15 and 0.89 | correct | lesson body |
| l8 | quiz[0] | breakout 0.03/0.125 = 0.24 | correct | D |
| l8 | quiz[1] | base rate ×10 raises the posterior 4.3 times (0.154 to 0.667); "cannot fall" | correct | D: posterior increases in b |
| l8 | quiz[2] | even base rate: 0.8 | correct | D |
| l8 | quiz[3] | perfect detection, 2% false positives, 2% base: 0.505 | correct | D |

### l9-natural-frequencies

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l9 | screens[0] | 17 positives: 8 of the 10 with the condition, 9 of the 90 healthy | correct | E on the grid cells |
| l9 | screens[1] key, wrongs | "you are one of the 17 positives": 8/17 = 0.4706 | correct | E; protocol: a uniformly chosen positive |
| l9 | screens[2].prose | counting people instead of chances is "natural frequencies" | correct | S: Gigerenzer and Hoffrage (1995), Psychological Review 102 |
| l9 | screens[2], [3] | 5% of 990 = 49.5; 9 + 50 = 59 positives | correct | D; counts tree checked by trees() |
| l9 | screens[4] key, explain | 9/59 = 0.153; exact 2/13 = 0.154; gap from rounding 49.5 | correct | D; both values inside the accepted band |
| l9 | screens[5] | 10,000 people: 90 + 495 = 585; 90/585 = 2/13 exactly | correct | D |
| l9 | screens[6] key, why ×3 | spam: 240/268 = 0.90; 4% of all 1,000 gives the slip 240/280 | correct | D |
| l9 | screens[6].explain | taking 4% of everyone counts spam emails as false flags | correct | D |
| l9 | screens[7] | the false-positive rate applies to the healthy group only | correct | definition of P(+ given healthy) |
| l9 | screens[8] order, explain | crowd, split, rates, add, divide; "Bayes' rule, written in people" | correct | D |
| l9 | screens[9] key, wrongs, explain | 140 trend signals, 80 others: 7/11; rates 70% and 10% | correct | E on the grid: 14 and 8 squares of 10 days |
| l9 | summary.ideas, formula, trap | count over a count; pick a crowd that makes counts whole; false-positive rate is a share of the healthy | correct | lesson body |
| l9 | quiz[0], [1] | 40 + 95 = 135 flagged; 40/135 = 0.296 | correct | D |
| l9 | quiz[2] | no false positives: a positive is certain | correct | D |
| l9 | quiz[3] | "about 50 of the 990 healthy people test positive" is the frequency form | correct | D |

### l10-odds-form

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l10 | screens[0] | among positives 49.5 healthy to 9 cases: 5.5 to 1; before 99 to 1 | correct | D |
| l10 | screens[1].prose | odds are the ratio cases to non-cases, written as a fraction 1/5.5 | correct | S: odds in favour = p/(1 − p), BH Def 2.3.4 |
| l10 | screens[1] key, wrongs, explain | odds 1:5.5 is p = 1/6.5 = 2/13; odds = p/(1 − p), p = odds/(1 + odds) | correct | D |
| l10 | screens[2] key, wrongs | odds multiplied by 18; slips 15.38 (probabilities), 0.9, 93.5 | correct | D: 1/5.5 = 18/99 |
| l10 | screens[2].explain | 18 = 0.9/0.05 is the likelihood ratio: how many times likelier the evidence is with the condition | correct | BH Thm 2.3.5 |
| l10 | screens[3] | on the log-odds line a fixed ratio is a fixed step; evidence adds ln 18 | correct | D; label positions ln(odds) checked |
| l10 | screens[4] key, wrongs | 20% and ratio 6: odds 3/2, p = 0.6; slips 1.2, 6/7, 0.2 | correct | D; MC 0.600 |
| l10 | screens[5] key, explain | fires 30% either way: ratio 1, stays 0.55; "noise, however often it fires" | correct | D |
| l10 | screens[5] byKey.sum | "Evidence multiplies odds; it never adds probabilities" | correct | D: odds form |
| l10 | screens[6] key, wrongs, explain | 10% and ratio 3: 1/4, not 0.3 | correct | D |
| l10 | screens[7] order, explain | Bayes for H and for ¬H, divide, P(E) cancels: posterior odds = LR × prior odds | correct | BH Thm 2.3.5 |
| l10 | screens[8].prose | each signal fires independently of the others "whether or not a trend has begun" | correct | conditional independence given the hypothesis is stated |
| l10 | screens[8] key, wrongs, explain | four signals: 0.84 after three, 1.27 after four; ln 4 / ln 1.5 = 3.42 | correct | D |
| l10 | summary.ideas, formula, trap | odds conversions; LR multiplies odds, never probabilities, and is not the answer | correct | lesson body |
| l10 | quiz[0] | "3 to 1 on" means 3 wins per loss, p = 0.75 | correct | S: UK betting convention, odds-on |
| l10 | quiz[1] | 50% and ratio 4: 0.8 | correct | D |
| l10 | quiz[2] | 1:50 times 10 is 1:5, about 0.17 | correct | D |
| l10 | quiz[3] | ratio 1/4 from even odds: 0.2; a ratio below 1 is evidence against | correct | D |

### l11-updating-twice

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l11 | screens[0].prose | second test "errs independently of the first, both with and without the condition" | correct | conditional independence stated in full |
| l11 | screens[0] key, wrongs | from 2/13, second positive gives 36/47 = 0.766; slips 0.154, 0.9, 0.1385 | correct | D; MC 0.77 |
| l11 | screens[1] key, explain | 18 then 4 or 4 then 18: odds × 72 either way; order does not matter | correct | D: commutativity |
| l11 | screens[2].prose | using the first answer as the next starting point is "updating twice" | correct | BH 2.6 (conditioning on more evidence) |
| l11 | screens[2] key, wrongs | odds 324/99 = 3.27, p = 324/423 = 0.766 | correct | D |
| l11 | screens[3] key, hints, explain | positive then negative: LR 2/19, odds 4/209, p = 4/213 = 0.0188 | correct | D; MC 0.019 |
| l11 | screens[3] byKey.base | a negative does not exactly cancel a positive: 18 × 0.105 = 1.9 | correct | D |
| l11 | screens[4] | negative first, then positive: exactly the same | correct | D |
| l11 | screens[5] key, wrongs | LR of "two positives" = 0.81/0.0025 = 324 | correct | D |
| l11 | screens[5].explain | one update on the joint evidence lands where two did; "that works because the tests err independently" | correct | D |
| l11 | screens[6] key, why ×3 | 0.766 from 2/13; 0.154 restarts at 1%; 0.81 has no prior; 0.024 squares | correct | D |
| l11 | screens[7] order | chained odds; "independent errors make this the ratio of both results together" | correct | D; assumption stated in the prose |
| l11 | screens[8].prose | each right 70% whichever way it goes, "and they work independently" | imprecise | needs errors independent given the direction; overall the calls are dependent (l16 screens[10]). Finding 5 |
| l11 | screens[8] key | P(up given both say up) = 0.49/0.58 = 49/58 | correct | D; odds (7/3)² |
| l11 | screens[8].canvas leaves | leaves 0.49, 0.51, 0.09, 0.91 | wrong | D: path chances are 0.245, 0.255, 0.045, 0.455; the stated leaves add to 2, against l5 "leaves add to 1". Finding 2 |
| l11 | screens[8] byKey.joint | 0.49 "is up with both calls up, out of everything" | wrong | D: P(up and both say up) = 0.5 × 0.49 = 0.245; 0.49 is P(both say up given up). Finding 2 |
| l11 | screens[8] byKey.one, either | 0.7 is one call; 0.91 is "at least one is right" | correct | D: 1 − 0.09 |
| l11 | screens[8].explain | each call has LR 7/3; two give 49/9; "the tree gives the same: 0.49/0.58" | correct | D: the ratio is right because the prior is 50% (see finding 2 for the leaves) |
| l11 | screens[9] key, why ×3 | B copies A: 0.7; B's call has LR 1 | correct | D; MC 0.700 |
| l11 | screens[9].explain | sources that share their errors count for less than their number | correct | D |
| l11 | summary.ideas[1] | "for independent evidence the likelihood ratios multiply, in any order" | correct | read with the formula note, which states independence given H and given ¬H |
| l11 | summary.formula + note, trap | O2 = LR1 × LR2 × O0, valid when the evidence errs independently given H and given ¬H | correct | D |
| l11 | quiz[0] | 20%, ratios 2 and 3: 0.6; "a second, independent report" | imprecise | value correct (D); wording as finding 5 |
| l11 | quiz[1] | ratios 4 and 1/4 cancel: stays 0.3, not 0.5; "a later, independent rumour" | imprecise | value correct (D); wording as finding 5 |
| l11 | quiz[2] | same sample, same machine: little more than one positive | correct | D |

### l12-many-hypotheses

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l12 | screens[0] | die picked at random, rolled, "5": the 6-sided die is most likely | correct | E; protocol stated |
| l12 | screens[1] cells, explain | likelihoods 0, 1/6, 1/8; "need not add to 1; here 7/24" | correct | D |
| l12 | screens[2] cells, explain | products 0, 1/18, 1/24; total 7/72 = P(5) | correct | D |
| l12 | screens[3].prose | dividing by the total is "normalising" | correct | definition |
| l12 | screens[3] key, wrongs | 6-sided: 4/7; slips 1/18, 1/3, 1/6 | correct | D |
| l12 | screens[3].explain (a) | posteriors 0, 4/7, 3/7 | correct | D; MC |
| l12 | screens[3].explain (b) | "The 6-sided die gained and the 8-sided die lost a little" | wrong | D: the 8-sided die rose from 1/3 to 3/7 (its likelihood 1/8 exceeds P(5) = 7/72); MC 0.429. Finding 1 |
| l12 | screens[4] key, wrongs | second roll 3: 16/25 = 0.64; slips 0.571, 4/13 (old prior), 2/21 | correct | D; MC 0.64 |
| l12 | screens[4].explain | the 4-sided die could have rolled a 3, yet it stays at 0 | correct | D |
| l12 | screens[5].prose | "a 3 is the 4-sided die's best roll" | imprecise | every face of the 4-sided die has chance 1/4; the 3 favours it only against the other dice. Finding 9 |
| l12 | screens[5] key, why ×3 | still 0; "no evidence can bring back a hypothesis at 0" | correct | D |
| l12 | screens[5].explain | never give 0 to something that could be true: Cromwell's rule | correct | S: Lindley, Making Decisions (1985) |
| l12 | screens[6] key, wrongs | 0.16/0.5 = 0.32; likelihood-only slip 0.8/1.5 = 0.533 | correct | D |
| l12 | screens[7].prose | hypotheses "that cannot overlap and whose priors add to 1"; general Bayes | correct | BH Thm 2.3.3 with 2.3.6; exclusive and exhaustive both stated |
| l12 | screens[7] key, why ×2 | the bottom is P(E), not 1 and not the sum of likelihoods | correct | total probability |
| l12 | screens[8] cells, explain | regimes: 2/9, 1/3, 4/9; 0.75 if the priors are dropped | correct | D |
| l12 | screens[9] key, wrongs | random walk 0.006/0.024 = 0.25; slip 0.1379 | correct | D; the three models are taken as the whole set (priors add to 1) |
| l12 | summary.ideas, formula, trap | prior times likelihood, normalise; posterior proportional to prior × likelihood | correct | BH 2.3 |
| l12 | quiz[0] | skilled: 0.08/0.47 = 0.1702 | correct | D |
| l12 | quiz[1] | prior exactly 0 stays 0 | correct | D |
| l12 | quiz[2] | 0.12/0.2 = 0.6 | correct | D |
| l12 | quiz[3] | equal likelihoods keep the 3 to 1 ratio; other hypotheses divide both alike | correct | D |

### review-2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| rv2 | items[0] | P(spike given down) = 30/80; reverse 30/40 | correct | E on the Venn |
| rv2 | items[1] | insider flag 0.0049/0.0248 = 0.198; about 80% of flags false | correct | D |
| rv2 | items[2] | 300 + 480 = 780; 300/780 = 0.38 | correct | D |
| rv2 | items[3] | likelihood ratio 0.45/0.15 = 3 | correct | D |
| rv2 | items[4] | 25% and ratio 4: 4/7 | correct | D |
| rv2 | items[5] | 10%, "two independent news signals" each ratio 3: 0.5 | imprecise | value correct (D); wording as finding 5 |
| rv2 | items[6] | two heads: 16/33; slips 0.5517, 0.25, 0.3636 | correct | D; flips independent given the coin (implicit, standard) |
| rv2 | items[7] | Bayes form; conditionals equal only when P(A) = P(B) or P(A∩B) = 0 | correct | D; "both have positive probability" stated |
| rv2 | items[8] | even base rate: 0.875 | correct | D |

### homework-2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| hw2 | items[0] | anomaly: 0.017/0.0464 = 0.366 | correct | D |
| hw2 | items[1] | prior 1% needs LR 99 to reach 50% | correct | D |
| hw2 | items[2] | A positive, B negative: odds 5/49, p = 5/54; "B, run independently" | imprecise | value correct (D); wording as finding 5 |
| hw2 | items[3] | four dice after a 5: 0, 0.6, 0.3, 0.1; 1/3 if priors dropped | correct | D |
| hw2 | items[4] order, explain | posterior = 1/(1 + (f/h)((1 − b)/b)); reaches 1/2 only when f/h ≤ b/(1 − b) | correct | D; random check in r2 L2 script |
| hw2 | items[5] | two passes: 256/275 = 0.931; counts 6.4 and 0.475; one pass 8 of 17.5 | correct | D |
| hw2 | items[6].model (a) | odds form with P(E) > 0 and P(E given ¬H) > 0 named | correct | D; conditions stated |
| hw2 | items[6].model (b), (c) | 2/13; n = 3 from 18^n > 1881 (2.61); 0.766 and 0.983 | correct | D |
| hw2 | items[6].model (d) | assumes the tests err independently given H and given ¬H; fails on a shared sample or trait | correct | D |
| hw2 | items[7] | two notes from one presentation: not much more than one piece of evidence | correct | D |
| hw2 | items[8] | 60% and a warning 3 times likelier under a miss: 1/3 | correct | D |
| hw2 | items[9].model 1 | P(B given J) from the multiplication rule, needing P(J) > 0 | correct | D; condition stated |
| hw2 | items[9].model 2 | two flags need independence on bad ticks and on good ticks, each used once | correct | D |
| hw2 | items[9].model 3 | 15/64 and 50/57; odds check 1/49 × 15 × 70/3 = 50/7 | correct | D; MC 0.877 |
| hw2 | items[9].model 4 | shared stale quote: P(J∩V given G) = 0.03, answer 3/10; V's ratio after J is 1.4 | correct | D (needs f_V ≤ f_J, true here); MC 0.300 |
| hw2 | items[9].rubric | four required rows, 10 points; each row matches the model | correct | checked against the model text |

### problems-2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| pb2 | items[0].parts[0..2] | 180 rumoured targets; 456 rumoured; 180/456 = 0.3947 | correct | D |
| pb2 | items[0].parts[3] | break-even base rate b = 0.06/0.51 = 0.1176 | correct | D: 0.45b = 0.06(1 − b) |
| pb2 | items[1].prose | the two reports arise independently "given the truth" | correct | conditional independence stated |
| pb2 | items[1].parts[0..2] | odds 3/17; × 3 = 9/17; × 6 gives 54/71 = 0.7606 | correct | D |
| pb2 | items[1].parts[3] | odds 19 needed; two more ratio-3 reports ("independent reports") | correct | D; wording as finding 5 |
| pb2 | items[1].parts[4] | the exit followed from the delay, so 0.76 double counts and is too high | correct | D |
| pb2 | items[2].prose | "given the kind, orders fill independently" | correct | conditional independence stated |
| pb2 | items[2].parts[0..3] | 0.46; 16/46; 16/31; next fill 153.4/248 = 0.6185 | correct | D; MC 0.618 |
| pb2 | items[3].prose | "given the truth, the two filters err independently" | correct | stated |
| pb2 | items[3].parts[0..2] | 0.0582; 0.3265; after B (ratio 70) 0.9714 | correct | D |
| pb2 | items[3].parts[3..4] | 392 good prints deleted; 392/13,692 = 0.0286 = 1 − 0.9714 | correct | D |

### fluency-l7-turning-around

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| fl7 | families[0] | from counts: key a/(a + b); slips a/(a + c) and a/tot; b ≠ c keeps them apart | correct | E over 4,000 draws: the population is consistent and no slip equals the key |
| fl7 | families[1] | from rates: Bayes; slips P(+ given bad), joint, unweighted others | correct | E over every parameter draw |
| fl7 | families[2] | P(+) by total probability; slips one path, unweighted others | correct | E over every parameter draw |
| fl7 | solution lines | positives are a + b; divide the joint path by P(+) | correct | D |

## Level 3: Independence

### l13-knowing-nothing

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l13 | screens[1] key, why ×2 | learning the total is 7 leaves "first die is 6" at 1/6 | correct | E: one 7 in each row |
| l13 | screens[2] | total 12 leaves only (6, 6): the chance jumps to 1 | correct | E |
| l13 | screens[3].prose | news that leaves a chance unchanged: independent, P(A given B) = P(A) | correct | BH Def 2.5.1 (equivalent form when P(B) > 0; screens[7] gives the product form) |
| l13 | screens[3] key, why ×2 | A and "total 12" are dependent; the dice being independent is a different statement; rare news can be strong | correct | E |
| l13 | screens[4] cells | P(B) 1/6 and 1/36; products 1/36 and 1/216; joints 1/36 and 1/36 | correct | E |
| l13 | screens[4].explain | the product test and the conditional test agree whenever P(B) > 0 | correct | D |
| l13 | screens[5] key | independent of A: "second die is 6", "total is even"; dependent: "at least one 6" (6/11), "first die even" (1/3) | correct | E |
| l13 | screens[5].explain | events that mention the first die are often, but not always, dependent on A | correct | E: "total is even" mentions it and is independent |
| l13 | screens[6] key, why, byKey | disjoint A and C are dependent: P(A given C) = 0; equal chances say nothing | correct | E |
| l13 | screens[6].explain | "Disjoint events with positive chances are as dependent as events can be" | correct | D: P(A given C) = 0 is the largest possible fall; rhetorical, harmless |
| l13 | screens[7] order | with P(A) > 0 and P(B) > 0: conditional test, definition, product, then P(B given A) = P(B) | correct | D; conditions stated |
| l13 | screens[7].explain | the product form is symmetric and "makes sense when P(B) = 0, so it is the usual definition" | correct | BH Def 2.5.1; Grimmett and Stirzaker 1.5 |
| l13 | screens[8] key, why ×3 | A is independent of itself only when P(A) is 0 or 1 | correct | D: x = x² |
| l13 | screens[9].prose | "Many models assume the pairs are independent" | imprecise | the tally tests today's sign against yesterday's; consecutive pairs share a day, so pairs cannot be the independent objects. Finding 8 |
| l13 | screens[9] cells, hints | tally 7, 3, 3, 7; up-up on days 7, 8, 15 to 19 | correct | E on the 20 rows, which chain as consecutive days |
| l13 | screens[10] key, wrongs | P(up given up yesterday) = 0.7 against P(up) = 0.5; slips 0.5, 0.35, 0.3 | correct | E |
| l13 | screens[10].explain | "Twenty days is a small sample, so this is a hypothesis to test on more data" | correct | sample estimate is hedged, no population claim |
| l13 | summary.ideas, formula + note | product test equivalent to the conditional test when P(B) > 0; self-independence only at 0 or 1 | correct | D |
| l13 | summary.trap, ideas[2] | disjoint events with positive chances are never independent | correct | D: 0 ≠ P(A)P(B) > 0; "positive chances" stated |
| l13 | quiz[0] | ace and heart independent: 1/13 both ways | correct | E |
| l13 | quiz[1] key, byKey.add | independent: 0.2; adding is for "either" and only when the events cannot overlap | correct | D |
| l13 | quiz[1] byKey.disjoint | "Independent events can, and usually do, happen together" | imprecise | D: with positive chances P(A∩B) = P(A)P(B) > 0 always; "usually do" also reads as "most of the time" (0.2 here). Finding 6 |
| l13 | quiz[2] | disjoint: P(A given B) = 0 | correct | D |
| l13 | quiz[3] | a certain event is independent of every event | correct | D |

### l14-independent-trials

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l14 | screens[1] key, wrongs, explain | two losses 0.45² = 0.2025; the second factor stays 0.45 | correct | D; trees() |
| l14 | screens[2] key, wrongs, explain | 0.45⁵ = 0.0185, about once in 54; below 1% at six | correct | D |
| l14 | screens[3].prose | independent trials: "each has the same chances, whatever came before"; a sequence's chance is a product | correct | S: Bernoulli trials, BH 3.3; both parts (same p, independence) are in the definition and the formula note |
| l14 | screens[3] key, wrongs | win, win, loss = 0.1361; any order 0.4084 | correct | D |
| l14 | screens[4] | three paths with two wins; 3 × 0.1361 = 0.4084 | correct | E |
| l14 | screens[5].prose | P(k wins in n) = C(n, k) p^k (1 − p)^(n − k) | correct | BH Thm 3.3.5 |
| l14 | screens[6] key, why ×3, explain | at least one of three at 0.3: 1 − 0.7³ = 0.657; adding gives 0.9 and overcounts; four ideas would give 1.2 | correct | D; MC 0.657 |
| l14 | screens[7] key, why ×3 | win chance 1: exactly 7 of 10 has chance 0; C(10, 7) = 120 | correct | D |
| l14 | screens[7].explain | "Independence still holds; it just has nothing to do" | correct | D: constant events are independent of everything (l13 quiz[3]) |
| l14 | screens[8] order, explain | complement, intersection, independence, (1 − p)^n | correct | D |
| l14 | screens[9] code | solution sums C(n, j) p^j (1 − p)^(n − j) for j = k..n; passes 8 hidden tests; starter fails | correct | executed in CPython by the r2 L3 script; every expect recomputed |
| l14 | screens[9].explain | 7 or more of 10 at 0.55: 0.2660, "only about a quarter of the time" | correct | D; MC 0.266 |
| l14 | screens[10].prose | no-edge strategy: P(30 or more of 50) = 0.1013, "about one time in ten" | correct | D; MC 0.101 |
| l14 | screens[10] key, wrongs, explain | expect 20 × 0.1013 ≈ 2 lucky strategies; "a good 50-trade backtest is weak evidence of skill" | correct | D: linearity of expectation; S: Bailey and López de Prado (2014) |
| l14 | summary.ideas, formula + note, trap | binomial and complement; "needs independence and the same p on every trial"; adding can pass 1 | correct | conditions stated |
| l14 | quiz[0..3] | 1/16; 0.271; 5 × 0.6 × 0.4⁴ = 0.0768; six trades for an all-loss chance below 0.01 | correct | D |

### l15-pairwise

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l15 | screens[1] key, why ×2, explain | P(C given A) = 1/2 = P(C): A and "coins match" are independent | correct | E on HH, HT, TH, TT |
| l15 | screens[2], [3] | every pair holds together only in HH: 1/4 = 1/2 × 1/2; "pairwise independent" | correct | E; BH Example 2.5.5 |
| l15 | screens[4] key, wrongs, explain | P(A∩B∩C) = 1/4, not 1/8 | correct | E |
| l15 | screens[5] | given A and B, C is certain: any two settle the third | correct | E |
| l15 | screens[6] key | pair checks alone leave P(all three) anywhere from 0 to 1/4 | correct | D: with P(ABC) = x the eight atoms are x, 1/4 − x (×3), x (×3), 1/4 − x, valid exactly for 0 ≤ x ≤ 1/4 (r2 L3 script) |
| l15 | screens[6] why ×2, explain | coins give 1/4; with "coins differ" every pair still passes and the triple is 0 | correct | E |
| l15 | screens[7].prose | mutually independent: the product rule for every group of two or more; four equations for three events | correct | BH Def 2.5.6; Grimmett and Stirzaker 1.5 |
| l15 | screens[7] key, why ×3 | four events need 6 + 4 + 1 = 11 equations | correct | D: 2⁴ − 4 − 1 |
| l15 | screens[8] key | true: mutual gives pairwise; a chance-0 event is independent of every event | correct | D |
| l15 | screens[8] why "triple" | the triple equation alone does not give the pairs: P(C) = 0, A = B with chance 1/2 | correct | D |
| l15 | screens[8].feedback.correct | "Mutual gives pairwise, never the other way round" | imprecise | pairwise does not imply mutual, but pairwise independent events can be mutually independent (two separate coins and a third). Finding 7 |
| l15 | screens[9].prose | Z falls exactly when X and Y move the same way; each pair has zero correlation and is independent | correct | E on the four states |
| l15 | screens[9] key, explain | all three fall with chance 1/4; 1/8 is "half the true crash risk" | correct | E |
| l15 | screens[10] key, why ×3, explain | a correlation matrix describes pairs; the crash needs all three; joint tail risk needs joint data or a joint model | correct | D |
| l15 | summary.ideas[2] | "Mutual independence implies pairwise independence, never the other way round" | imprecise | as screens[8].feedback.correct. Finding 7 |
| l15 | summary.formula + note | triple product and every pair; "neither part implies the other" | correct | D: screens[4] and screens[8] give both counter-examples |
| l15 | quiz[0..3] | A and "differ" independent; four equations; P(D given A∩B) = 0; mutual gives the pair A, C | correct | E; D |

### l16-conditional-independence

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l16 | screens[1].prose | "Given the sector's day, the stocks move separately" | correct | conditional independence set up in words |
| l16 | screens[1] key, why ×2, explain | A's rise raises B's chance: news flows through the sector | correct | E: 0.68 > 0.5 |
| l16 | screens[2], [3] | P(both rise) = 0.32 + 0.02 = 0.34; P(B given A) = 0.68; slips 0.5, 0.34, 0.8 | correct | E on the weighted tree; MC 0.680 |
| l16 | screens[3].explain | dependent overall, yet they multiply inside each half: "independent given the sector" | correct | E |
| l16 | screens[4].prose | conditionally independent given C: P(A∩B given C) = P(A given C) P(B given C) | correct | BH Def 2.5.7 |
| l16 | screens[4] cells, explain | given good 0.64 = 0.64; overall 0.25 against 0.34; "different properties" | correct | E |
| l16 | screens[5] key, wrongs, explain | given good day and A up, B is still 0.8: P(B given A∩C) = P(B given C) | correct | E |
| l16 | screens[6] key, why ×3, explain | 0.34, not 0.25; "independence given C does not give independence" | correct | E; BH Example 2.5.10 |
| l16 | screens[7] key, wrongs | alert fires on news or drop: P(news given alert) = 0.20/0.28 = 5/7 | correct | E on the four rows |
| l16 | screens[8] key, why ×3 | then the drop is learned: back to 0.2 | correct | E; MC 0.200 |
| l16 | screens[8].explain | independent causes become dependent given the alert; "conditioning on a shared effect can link its causes, as it does here" | correct | S: explaining away, Pearl (1988) ch. 2; BH Example 2.5.11; hedged with "can" |
| l16 | screens[9] order | P(B given A∩C) = P(B given C) under conditional independence with P(A∩C) > 0 | correct | D; condition stated |
| l16 | screens[10] key, wrongs | P(2 says beat given 1 says beat) = 0.2625/0.45 = 7/12 | correct | E |
| l16 | screens[10].explain | forecasts correlated overall yet independent given the truth: "exactly what lets you multiply their likelihoods" | correct | D; ties back to l11 |
| l16 | summary.ideas, formula + note, trap | equivalence when P(A∩C) > 0; "neither independence nor conditional independence implies the other" | correct | BH 2.5; both directions shown on screens[6] and [8] |
| l16 | quiz[0] | symptoms independent given the disease are "usually not" independent overall | correct | D; hedged |
| l16 | quiz[1] | 0.6 × 0.5 = 0.3 | correct | D |
| l16 | quiz[2] key | fund lost money and there was a crash: the chance of a bad call "falls" | imprecise | D: it falls against the chance after the loss, but equals the prior, so the wrong option "It is unchanged: the causes are independent" is right against the prior. Finding 3 |
| l16 | quiz[2].explain | the loss raised the chance; the crash removes that need, so it "falls back" | correct | D for every pair of cause chances (r2 L3 script) |
| l16 | quiz[3] | fair or two-headed coin, first toss heads: second heads 5/6; unconditional 0.75 | correct | E |

### l17-correlated-defaults

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l17 | screens[0..1] bars | ten independent borrowers at 0.05: 0.5987, 0.3151, 0.0746, 0.0115 | correct | D: binomial(10, 0.05) |
| l17 | screens[1] key, why ×2, explain | a recession that lifts every chance, with each overall chance still 0.05, raises P(3 or more) | correct | D: the tail is at least its tangent at 0.05 on [0, 1]; random check over 3,000 two-regime mixes in r2 L3 script |
| l17 | screens[2] key, hints, explain | as the recession chance rises both end bars rise; at 0.2: 0.7269 and 0.0646; the middle thins | correct | D at every slider step 0 to 0.25 |
| l17 | screens[3].prose | independent given the economy, moving together overall: "correlated defaults" | correct | S: one-factor (Vasicek) model; Hull, Options, Futures and Other Derivatives, ch. on credit risk |
| l17 | screens[3] key, wrongs | 0.2 × 0.2 + 0.8 × 0.0125 = 0.05; slips 0.2125, 0.10625, 0.2 | correct | D |
| l17 | screens[4] key, wrongs, explain | both default 0.008125, more than three times 0.0025 | correct | D: 3.25 |
| l17 | screens[5].prose | "The leaves show P(3 or more defaults) in each regime" | correct | stated, so these leaves are conditional tails by declaration (0.3222, 0.0002) |
| l17 | screens[5] key, wrongs, explain | 0.2 × 0.3222 + 0.8 × 0.0002 = 0.0646, 5.6 times 0.0115 | correct | D; MC 0.0646 |
| l17 | screens[6] key, why ×3, explain | the model treated independence given the economy as independence overall; the binomial at 0.05 needs the latter | correct | D |
| l17 | screens[6] why "n" | "The binomial works for any number of independent trials" | correct | with one p, as the hint states |
| l17 | screens[7] key, wrongs, explain | all-or-nothing: P(3 or more) = 0.05, over four times 0.0115; "behave like one big loan" | correct | D |
| l17 | screens[8] | P(K ≥ 3) = Σ P(r) P(K ≥ 3 given r); the binomial inside a regime needs independence given the regime | correct | D |
| l17 | screens[9] code | book_tail = q·tail(p_bad) + (1 − q)·tail(p_good); passes 7 hidden tests; starter fails; gives 0.0646 | correct | executed in CPython by the r2 L3 script; every expect recomputed |
| l17 | screens[10].prose | before 2008 many models priced such slices as if mortgage defaults were only weakly linked | correct | S: Coval, Jurek and Stafford (2009), The Economics of Structured Finance; Hull ch. on the 2007 credit crisis |
| l17 | screens[10] key, why ×3, explain | a shared factor (house prices) made 3 or more far likelier; more loans do not remove it; diversification removes separate risks, not shared ones | correct | D; MC large pool 0.20 |
| l17 | summary.ideas, formula + note, trap | factor-model tail by total probability; 0.0646 not 0.0115 | correct | D |
| l17 | quiz[0] | the shared-economy book is likelier to have no defaults (0.7269 against 0.5987) | correct | D: (1 − p)^10 is convex, Jensen; holds for every mix |
| l17 | quiz[1], [2] | 0.05; pair 0.0034 against 0.0025 | correct | D |
| l17 | quiz[3] | very large pool: at least 10% default with chance about 0.2 | correct | D: law of large numbers inside each regime; MC 0.20 at 1,000 loans |

### review-3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| rv3 | items[0] | first die even and total 8 are dependent: 3/5 | correct | E |
| rv3 | items[1] | disjoint: P(A∩B) = 0, not 0.12 | correct | D |
| rv3 | items[2] | at least one of four at 0.2: 0.5904 | correct | D |
| rv3 | items[3] | exactly two of four at 0.6: 0.3456 | correct | D |
| rv3 | items[4] | A, B, "differ": pairwise only, triple 0 | correct | E |
| rv3 | items[5] | all three fall on 250 × 1/4 = 62.5 days, double 31.25 | correct | E; expectation needs no independence across days |
| rv3 | items[6] | second symptom given the first: 0.117/0.27 = 0.4333 | correct | E; "given disease status, the symptoms are independent" stated |
| rv3 | items[7] | margin call: P(A bad given call) = 0.3/0.65; then B bad is learned: 0.3 | correct | E; the baseline is stated in the prose |
| rv3 | items[8] | two loans 0.00936; independent model 0.048² = 0.0023; "four times likelier" | correct | D: 4.06 |

### homework-3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| hw3 | items[0] | 33/60 = 77/140 = 110/200 = 0.55: independent "in this data" | correct | E; hedged to the sample |
| hw3 | items[1] | 0.7¹² = 0.01384, about once in 72 | correct | D; "assume months are independent" stated |
| hw3 | items[2] | nine trades for 1 − 0.45^n ≥ 0.999 (8.65) | correct | D |
| hw3 | items[3] | true: P(Z falls given X falls) = 1/2, P(Z falls given both fall) = 1; not mutual; all three never rise | correct | E |
| hw3 | items[4] | both say beat: 0.225/0.2625 = 6/7; copying analysts would overstate the evidence | correct | E |
| hw3 | items[5] | five loans: 0.1 × 0.5125 + 0.9 × 0.0038 = 0.0547, 2.4 times 0.0226; each loan alone 0.05 | correct | D |
| hw3 | items[6] | A and B independent gives A and B^c independent | correct | BH Prop 2.5.3 |
| hw3 | items[7].model (a), (b) | P(D1) = q p_b + (1 − q) p_g; joint minus product = q(1 − q)(p_b − p_g)² | correct | D; random check in r2 L3 script |
| hw3 | items[7].model (c) | never negative; zero exactly when q is 0 or 1 or p_b = p_g | correct | D |
| hw3 | items[7].model (d) | 0.005625 = 0.008125 − 0.0025; 3.25 times | correct | D |

### problems-3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| pb3 | items[0].parts[0..1] | P(up given gap) = 78/120 = 0.65 = 260/400: independent in the sample | correct | E |
| pb3 | items[0].parts[2..3] | "treat gap days as independent trials": exactly 3 of 4: 0.3845; at least one down 0.8215 | correct | D; assumption stated |
| pb3 | items[1].parts[0..1] | losing week 0.475; signal failed given loss 0.3/0.475 = 0.6316 | correct | E |
| pb3 | items[1].parts[2..3] | squeeze learned: 0.3; given a loss the causes are dependent (0.63 to 0.3) | correct | E; the baseline "given a loss" is explicit |
| pb3 | items[2].parts[0..3] | one loan 0.1; all three 0.005536; independent model 0.001; ratio 5.536 | correct | D |
| pb3 | items[3].prose | three desks, three shared feeds; a desk is calm when its two feeds agree; each 1/2 | correct | E on the eight feed states |
| pb3 | items[3].parts[0..1] | P(C given A) = 1/2; every pair independent | correct | E |
| pb3 | items[3].parts[2..3] | P(A∩B∩C) = 1/4; P(C given A∩B) = 1 | correct | E |
| pb3 | items[3].parts[4] | eight independent days: 1 − 0.75⁸ = 0.8999 | correct | D |

# Claim ledger: mental L1 to L3 (concept audit)

Blind audit of `app/content/courses/mental/` levels 1 to 3 (l1 to l12, review-1 to review-3, homework-1 to homework-3). One row per definition, result, method step, convention, always/never/every/only claim, interpretation, causal claim, and the reasoning of each explain, why, hint and feedback line (lines that restate the same reasoning share a row). Paths are JSON paths inside the file. Verdicts: correct, wrong, imprecise, misleading, unverified. `sim:` names a check in `docs/reports/mental-L<n>-concepts.py` (L1 for l1 to l4, L2 for l5 to l8, L3 for l9 to l12).

Sources used: field axioms of arithmetic (commutative, associative and distributive laws; Spivak, *Calculus*, ch. 1); place value and the division algorithm (Hardy and Wright, *An Introduction to the Theory of Numbers*, ch. 1 and sec. 9.1 on decimals; casting out nines, sec. 9.5); triangle inequality for the rounding bound (Spivak ch. 1); Hull, *Options, Futures and Other Derivatives*, sec. 3.4 (hedge ratio) and sec. 15.4 (volatility per trading day, 252 days); Harris, *Trading and Exchanges*, ch. 4 (bid, ask, spread); Zetamac default settings as recorded in `app/content/warmup.json` (the vendor site is outside this session's network, so vendor claims are checked against the app's copy). Exhaustive enumeration over the finite domain is used wherever a claim says always, never, every or only.

Row count 230: correct 219, imprecise 11, wrong 0, misleading 0, unverified 0. The 11 imprecise rows group into 8 findings.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-left-to-right.json | screens[0].prose | On paper we add from the right and carry; in the head add the big part first | correct | method statement; both orders give a + b by associativity |
| l1-left-to-right.json | screens[1] hints, feedback, byKey | A jump of 30 is three jumps of 10; 47, 57, 67, 77; the 3 in 30 counts tens | correct | place value: 30 = 3 x 10 |
| l1-left-to-right.json | screens[1].explain | Adding tens changes only the tens digit; the units ride along | imprecise | units claim true for every pair (sim: L1:l1_units_ride_along); the tens-digit-only claim fails once the sum passes 100, as in screens[5] 66 + 50 = 116 (sim: L1:l1_tens_digit_only, 450 of 810 pairs). Finding 1 |
| l1-left-to-right.json | screens[2] widget, byKey, explain | 47 + 36: tens to 77, units to 83; lost-ten 73 keeps only the 3 of 13; side 713; the sum cannot exceed 47 + 40 = 87 | correct | sim: L1:l1_s2_key; 36 < 40 gives the bound |
| l1-left-to-right.json | screens[3].prose | Adding from the left: tens first, then units; say each stop | correct | definition of the method; a + b = (a + tens of b) + units of b |
| l1-left-to-right.json | screens[3] hints, byKey, explain | 58 + 27: 78, then 2 to reach 80 and 5 beyond, 85; slips 75 and 715 | correct | sim: L1:l1_s3_key |
| l1-left-to-right.json | screens[4].prose, explain | The units jump is the one that can cross a ten; split it at the ten (bridging through ten): 68 + 7 = 68 + 2 + 5 | correct | sim: L1:l1_bridge; a tens jump never changes the units digit |
| l1-left-to-right.json | screens[4].feedback.byKey | +3 and +4 make 7 but 68 + 3 overshoots 70; split at the ten, not anywhere | correct | 68 + 3 = 71 |
| l1-left-to-right.json | screens[5] hints, byKey, explain | 66 + 58: 116, bridge 120, 124; a sum past 100 works the same way | correct | sim: L1:l1_s5_key |
| l1-left-to-right.json | screens[6] prose, hints, byKey, explain | 68 + 35: 98, bridge 100, 103; crossing 100 is one more bridge through a ten | correct | 100 is a multiple of ten; 98 + 2 + 3 |
| l1-left-to-right.json | screens[7] prose, options, byKey | 57 + 38 = 95; Sam's 85 loses the carry; 815 side by side; 105 adds the carried ten twice | correct | 80 + 15 = 95; 95 + 10 = 105 |
| l1-left-to-right.json | screens[7].explain | From the right the carry must be held while adding the tens; from the left the carry is a jump past 90 | correct | description of the two algorithms; the question stays on screen, so only the running stop is held |
| l1-left-to-right.json | screens[8].prose, summary.formula | a + b = (a + tens of b) + units of b; when the units cross a ten, hop to the ten first | correct | sim: L1:l1_split_identity (all two-digit pairs) |
| l1-left-to-right.json | screens[8] options, explain | 64 + 29: first stop 84; 73 adds units first; 66 adds 2 not 20; 93 is the final answer | correct | 64 + 20 = 84; 84 + 6 + 3 = 93 |
| l1-left-to-right.json | screens[9] prose, hints, byKey, explain | Pounds play the part of tens and pence of units; £47.65 + £47.68 = £95.33; slips £94.33 and £95.30 | correct | sim: L1:l1_fills |
| l1-left-to-right.json | summary.ideas, summary.trap | Tens then units; hop to the ten; say each stop so one number is held; carrying from the right means holding a digit | correct | restates rows above |
| l1-left-to-right.json | quiz[0..2] keys, byKey, explain | 59 + 34 = 93; stops 38, 78, 83; 76 + 48 = 124; slip readings | correct | direct arithmetic; "38, 83, 88" adds the 5 twice (83 + 5) |
| l1-left-to-right.json | quiz[3] | £23.85 + £23.79 = £47.64; the second fill was 6p lower; slips £46.64, £47.70 | correct | sim: L1:l1_quiz_fills |
| l2-round-and-adjust.json | screens[0].prose, screens[1] | 54 + 29: add 30 (1 too many), step back 1, 83; slips 85 and 84 | correct | sim: L1:l2_s1 |
| l2-round-and-adjust.json | screens[2] options, explain | Adding 28 as +30 overshoots by 2, so the correction is -2; -8 uses the units digit | correct | 30 - 28 = 2; 38 + 28 = 66 |
| l2-round-and-adjust.json | screens[3].prose | Round, then adjust: change the awkward number to a round one, then undo the change | correct | a + b = a + (b + d) - d; sim: L1:l2_identities |
| l2-round-and-adjust.json | screens[3] byKey, explain | 67 + 38 = 67 + 40 - 2 = 105; slips 109, 107 | correct | sim: L1:l2_s3 |
| l2-round-and-adjust.json | screens[4] prose, byKey, explain | A number just below 100 is 100 minus a little; 46 + 97 = 146 - 3 = 143; lost-ten 133 | correct | sim: L1:l2_s4; 6 + 7 = 13 keeps 3, 4 + 9 = 13 gives 133 |
| l2-round-and-adjust.json | screens[5] prose, explain | Either number can be rounded; the order does not matter in a sum; round whichever sits nearer a ten | correct | commutativity; sim: L1:l2_s5 |
| l2-round-and-adjust.json | screens[6] prose, options, byKey, explain | 71 - 38: taking away 40 removes 2 too many, so 2 goes back on, 33; Ana's 29 adjusts the wrong way; in a subtraction the adjustment goes the other way | correct | sim: L1:l2_subtract_direction; 33 + 38 = 71 |
| l2-round-and-adjust.json | screens[7].prose, summary.formula | a + b = a + (b + d) - d and a - b = a - (b + d) + d; added too much, take it off; took away too much, give it back | correct | sim: L1:l2_identities (d from -5 to 5) |
| l2-round-and-adjust.json | screens[7] options, explain | 92 - 47: take 50, add 3, 45; "add 7" uses the units digit | correct | 50 - 47 = 3; 45 + 47 = 92 |
| l2-round-and-adjust.json | screens[8] lines, byKey, explain | 152 - 98: round to 100, take 100, give 2 back, 54; the correction goes up because too much was taken | correct | 54 + 98 = 152 |
| l2-round-and-adjust.json | screens[9] prose, byKey, explain | £48.98 is £49 less 2p; £72.40 - £49 + 2p = £23.42; the move handles any price ending in 95p to 99p | correct | sim: L1:l2_profit; profit = sale price less purchase price |
| l2-round-and-adjust.json | summary.ideas, summary.trap | Round to a ten or to 100, then undo; either number in a sum; the trap is taking the difference off again in a subtraction | correct | restates rows above |
| l2-round-and-adjust.json | quiz[0..3] | 56 + 39 = 95; 84 - 49 = 35; 27 + 98 = 125; £61.25 - £35.97 = £25.28; slip readings | correct | sim: L1:l2_quiz_profit; direct arithmetic |
| l3-making-100.json | screens[0].prose | Change, a gap between prices, a distance to a target are subtractions done by counting up | correct | b - a is the distance from a to b on the line |
| l3-making-100.json | screens[1] hints, byKey, explain | 37 to 100: 3 to 40, 60 to 100, gap 63; 73 takes each digit to 10 (37 + 73 = 110); 53 counts five tens | correct | 100 - 37 = 63 |
| l3-making-100.json | screens[2] options, explain | For pairs making 100 the tens digits make 9 and the units digits make 10; it works for every pair except numbers ending in 0 | correct | sim: L1:l3_complement_rule (holds for 90 of the 99 numbers 1 to 99; fails exactly on 10, 20, ..., 90) |
| l3-making-100.json | screens[3].prose | The partner is the complement to 100: tens to 9, units to 10 | imprecise | the definition is right; the digit rule is restated with no exception and fails on numbers ending in 0 (sim: L1:l3_rule_without_exception). Finding 2 |
| l3-making-100.json | screens[3] byKey, explain | 100 - 58 = 42; 52 takes both digits to 10 (sum 110); 41 takes both to 9 (sum 99) | correct | 58 + 42 = 100 |
| l3-making-100.json | screens[4] prose, byKey, explain | Any subtraction is a gap; 83 - 47 = 3 + 30 + 3 = 36; slips 44 (smaller from larger) and 46 (kept the ten) | correct | sim: L1:l3_s4 |
| l3-making-100.json | screens[5] prose, byKey, explain | Counting up crosses 100: 132 - 68 = 32 + 32 = 64; slips 136, 74, 62 | correct | sim: L1:l3_s5; 62 counts from 70 |
| l3-making-100.json | screens[6] prose, byKey, explain | 92 - 86 = 4 + 2 = 6 with no tens jump; a gap under 10 can still cross a ten | correct | sim: L1:l3_s6 |
| l3-making-100.json | screens[7] prose, options, explain | 91 - 37 = 54; Ben's 64 borrows but never takes the ten; 66 smaller from larger; 44 takes the ten twice; counting up never borrows | correct | 3 + 50 + 1 = 54; 37 + 54 = 91 |
| l3-making-100.json | screens[8].prose, summary.formula | b - a = hop to the next ten + tens + the rest; for 100 - a this gives the complement: tens to 9, units to 10 | correct | sim: L1:l3_count_up (every a < b where the gap reaches the next ten; the lesson's "every gap today" scopes it); the complement clause shares finding 2 |
| l3-making-100.json | screens[8] options, explain | 74 - 28: +2, +40, +4 = 46; +50 lands on 80; +8 hops by the units digit | correct | 28 + 46 = 74 |
| l3-making-100.json | screens[9].prose | Bid is the best price a buyer offers, ask the best price a seller wants, spread the gap between them | correct | Harris, *Trading and Exchanges*, ch. 4; best bid £47.86 and best ask £48.13 are the top row of the book shown |
| l3-making-100.json | screens[9] hints, byKey, explain | Spread £48.13 - £47.86 = 14p + 13p = 27p; buying at the ask and selling straight back at the bid loses 27p; slips 73 and 127 | correct | sim: L1:l3_spread; round trip per share loses ask - bid |
| l3-making-100.json | summary.ideas[0], [1], summary.trap | A subtraction is a gap; count up from the smaller number; the trap is borrowing in the head | correct | restates rows above |
| l3-making-100.json | summary.ideas[2] | The complement to 100 takes the tens to 9 and the units to 10 | imprecise | no exception for numbers ending in 0; Finding 2 |
| l3-making-100.json | quiz[0], [2], [3] | 100 - 64 = 36; 75 - 38 = 37; spread £24.11 - £23.94 = 17p; slip readings | correct | sim: L1:l3_spread; direct arithmetic |
| l3-making-100.json | quiz[1].prose | With pence, every digit goes up to 9 except the last, which goes up to 10 | imprecise | true exactly when the last digit is not 0 (sim: L1:l3_pence_rule, 9,000 of 9,999 amounts under £100); for £37.40 the rule asks a digit to be 10. Finding 2 |
| l3-making-100.json | quiz[1] key, byKey, explain | Change from £100 for £37.45 is £62.55; £62.65 sums to £100.10; £63.55 sums to £101 | correct | sim: L1:l3_change |
| l4-running-total.json | screens[1] hints, byKey, explain | 17 + 13 = 30 and 26 + 34 = 60; units that add to 10 pair into whole tens; total 90 | correct | sim: L1:l4_pairs |
| l4-running-total.json | screens[2] key, byKey, explain | Of 18, 25, 31, 15, 22 only 31 has no partner; total 40 + 40 + 31 = 111 | correct | sim: L1:l4_odd_one (unique) |
| l4-running-total.json | screens[3] prose, byKey, explain | Running total: 46 + 27 - 18 + 35 goes 73, 55, 90; only the latest total matters; 108 restarts from 73 | correct | left-to-right evaluation of a chain of + and - |
| l4-running-total.json | screens[4] key, byKey, explain | 38, 26, 71, 42, 99; each row uses only the row above | correct | sim: L1:l4_running |
| l4-running-total.json | screens[5] prose, hints, byKey | Round each of 48, 31, 67, 22 to the nearest ten: estimate 170; 150 rounds every number down; 168 is the exact total | correct | sim: L1:l4_estimate_170 |
| l4-running-total.json | screens[5].explain, explain.canvas.caption | Rounding moved the numbers by 2, 1, 3, 2, at most 8 in all, so the true total lies in the band; 146 is 24 below, so wrong; the friend left out the 22 | correct | triangle inequality; sim: L1:l4_estimate_bound, L1:l4_left_out |
| l4-running-total.json | screens[6] prose, byKey, explain | 0 + 35 - 52 + 28 goes 35, -17, 11; below zero, count up to 0 first; zero is one more ten to bridge | correct | sim: L1:l4_below_zero |
| l4-running-total.json | screens[7] prose, options, byKey, explain | 70 - 18 + 12 = 64; Cara's 40 takes both away; each number carries its own sign; pairing across a minus is safe only when the signs come along | correct | sim: L1:l4_trap; a - b + c = a + (c - b) |
| l4-running-total.json | screens[8].prose, summary.formula | Add in any order with each number keeping its own sign: a - b + c = a + (c - b) | correct | commutativity of addition of signed numbers; sim: L1:l4_sign_identity |
| l4-running-total.json | screens[8] options, explain | In 63 - 27 + 17 the pair -27 and +17 makes -10, so 53; "63 and 27 making 90" treats the 27 as added | correct | 63 - 27 = 36, 36 + 17 = 53 |
| l4-running-total.json | screens[9] key, byKey, explain | Ten sums: 83, 87, 36, 35, 125, 55, 133, 65, 85, 46; one move from the level per sum | correct | sim: L1:l4_drill |
| l4-running-total.json | screens[10] prose, key, byKey, explain | P&L means profit and loss; running P&L £12.40, £4.55, £27.65, £12.00 | correct | sim: L1:l4_pnl |
| l4-running-total.json | summary.ideas, summary.trap | Pairs into tens; one number held; a rounded estimate catches a total far too big or too small | correct | restates rows above |
| l4-running-total.json | quiz[0..2] | 24 + 38 + 16 = 78; position 35, 17, 44, 4 (bought 62, sold 58); 90 - 26 + 14 = 78 | correct | direct arithmetic |
| l4-running-total.json | quiz[3].widget.options[0], explain | 29 + 52 + 38 + 71: estimate 190; rounding moved the numbers by 1, 2, 2, 1, at most 6 in all; 170 is 20 away, so wrong; true total 190 | correct | sim: L1:l4_estimate_190 |
| l4-running-total.json | quiz[3].widget.options[1].why | Each number moved by at most 2 when rounded, so the total can be off by no more than 6 | imprecise | the bound 6 is right (1 + 2 + 2 + 1) but does not follow from "each at most 2", which gives 8 for four numbers (sim: L1:l4_quiz3_inference). Finding 3 |
| l4-running-total.json | quiz[3].widget.options[2].why | The last digit is not a check of size | correct | 170 and 190 share a last digit and differ by 20 |
| review-1.json | items[0..4] | 68 + 57 = 125; 84 - 39 = 45; 100 - 73 = 27; 15 + 28 + 35 + 12 = 90; 82 - 47 = 35 (45 is smaller-from-larger or a lost borrow) | correct | sim: L1:review1_keys; 45 arises from both slips |
| review-1.json | items[5], [6] | Spread £36.14 - £35.88 = 26p; £29.99 + £47.56 = £30 + £47.56 - 1p = £77.55 | correct | sim: L1:review1_keys |
| review-1.json | items[7], [8] | 143 - 96 = 143 - 100 + 4 = 47, counting up agrees; 85 - 35 + 15 = 65 | correct | sim: L1:review1_keys |
| review-1.json | items[9] | Running P&L £8.25, -£5.25, £1.15; below zero, climb to zero first | correct | sim: L1:review1_pnl |
| homework-1.json | items[0], [1] | 79 + 86 = 165 (also 80 + 86 - 1); 161 - 77 = 23 + 61 = 84; slips 155, 1515, 116, 94 | correct | sim: L1:hw1_keys; column slips recomputed by hand |
| homework-1.json | items[2] prose, lines, explain | For 10t + u with u not 0 the complement to 100 is (9 - t) tens and (10 - u) units: filling the units makes t + 1 tens, ten tens make 100 | correct | sim: L1:hw1_complement_proof; the hypothesis u not 0 is stated |
| homework-1.json | items[3] | £36.47 + £36.53 + £36.50 = £109.50; 47p and 53p make £1; slips £108.50 and £109.41 | correct | sim: L1:hw1_keys; 3 x 36.47 = 109.41 |
| homework-1.json | items[4] | Position 45, 17, 53, 36, 45, 5; bought 90, sold 85 | correct | sim: L1:hw1_position |
| homework-1.json | items[5] | Spread £100.04 - £99.87 = 13p + 4p = 17p | correct | sim: L1:hw1_keys |
| homework-1.json | items[6] | -£18.60 + £34.95 - £52.40 + £41.15 = £5.10; gains £76.10, losses £71.00 | correct | sim: L1:hw1_day |
| homework-1.json | items[7] prose, options, explain | Estimate 210 for 58 + 23 + 41 + 87; moves 2, 3, 1, 3 bound the error by 9, so the true total lies from 201 to 219; only 229 is ruled out; 205 is wrong but cannot be ruled out; an estimate catches big slips, not small ones | correct | sim: L1:l4_estimate_210, L1:hw1_check_options |
| homework-1.json | items[8] | 173 - 88 = 173 - 90 + 2 = 85 | correct | sim: L1:hw1_keys |
| homework-1.json | items[9].model (a) to (c), rubric[0..5] | Cost £96.00; profits £3.29 and £3.21, total £6.50; spread 17p; buying both back at the ask costs £102.84 | correct | sim: L1:hw1_longform |
| homework-1.json | items[9].model (d), rubric[6] | Rounded prices give a profit of about £6; rounding moved each price by at most 25p, four prices at most £1; £16.50 is more than £10 away, so it cannot be right | correct | sim: L1:hw1_longform_estimate (moves 4p, 4p, 25p, 25p) |
| l5-tables.json | screens[0] key, byKey, explain | 24 sits in six cells: 2 x 12, 3 x 8, 4 x 6 both ways; the table mirrors across its diagonal; 144 cells hold 78 different facts | correct | sim: L2:l5_cells_24, L2:l5_78_facts (unordered pairs from 1 to 12) |
| l5-tables.json | screens[1] key, byKey, explain | In the 9 row every product's digits add to 9 except 99 (18, still a multiple of 9); each step adds a ten and takes a unit | correct | sim: L2:l5_nines_digit_sum; 9 = 10 - 1 |
| l5-tables.json | screens[2].prose | Nines pattern: 9 x n = 10n - n | correct | distributive law; sim: L2:l5_row_rules |
| l5-tables.json | screens[2] key, byKey, explain | 62 should be 63 and 118 should be 108; 99 is right; the digit sum caught both slips but does not give 9 on 99, so trust 10n - n | correct | sim: L2:l5_slips_caught |
| l5-tables.json | screens[3] prose, byKey, explain | Up to 11 x 9 the 11 row repeats the digit; 11 x 12 = 120 + 12 = 132; "1212" works only for one-digit numbers; ten lots plus one lot works all along the row | correct | sim: L2:l5_eleven_repeat |
| l5-tables.json | screens[4] prose, byKey, explain | Twelve lots is ten lots plus two lots; 12 x 8 = 80 + 16 = 96; any 12s fact is a 10s fact plus a doubled fact | correct | sim: L2:l5_row_rules |
| l5-tables.json | screens[5] prose, key, byKey, explain | 56 appears only as 7 x 8 and 8 x 7; neighbours 48, 54, 63 are 6 x 8, 6 x 9, 7 x 9; rebuild as 7 x 7 + 7 | correct | sim: L2:l5_cells_56 |
| l5-tables.json | screens[6].prose | For any whole n: 9n = 10n - n, 11n = 10n + n, 12n = 10n + 2n | correct | sim: L2:l5_row_rules |
| l5-tables.json | screens[6].prose; objectives[2] | a x b = b x a halves the table; symmetry halves the facts you need to learn | imprecise | symmetry leaves 78 of 144 facts (54%), and quiz[3] keys 72, "halved", as a slip (sim: L2:l5_halves). Finding 4 |
| l5-tables.json | screens[6] options, explain | 9 x 12 = 120 - 12 = 108; also 90 + 18; the other three workings do not give 108; both routes meet because a x b = b x a | correct | sim: L2:l5_options |
| l5-tables.json | screens[7] lines, explain | 9 x 8 = (10 - 1) x 8 = 80 - 8 = 72; the same four lines work for any 9n | correct | distributive law |
| l5-tables.json | screens[8] prose, key, byKey, explain | A trade's value is shares times price; £56 + £108 + £132 = £296 | correct | sim: L2:l5_transfer |
| l5-tables.json | summary.ideas, summary.formula, summary.trap | Mirror table, 78 facts; row rules; step from a neighbour; the digits of 9n add to a multiple of 9; 7 x 8 = 56 and 6 x 9 = 54 | correct | sim: L2:l5_digit_sum_multiple_of_9 (n up to 99,999; Hardy and Wright sec. 9.5) |
| l5-tables.json | quiz[0..2] | 8 x 7 = 56; 9 x 12 = 108 (118 takes 2 not 12); 12 x 7 = 70 + 14 = 84 | correct | direct arithmetic |
| l5-tables.json | quiz[3] key, byKey, explain | 12 diagonal squares plus half of the other 132 cells: 78 facts; 72 forgets that squares have no mirror partner; 66 leaves the squares out | correct | sim: L2:l5_78_facts |
| l6-splitting.json | screens[0] key, byKey, explain | 23 x 7 = 20 x 7 + 3 x 7 = 140 + 21 = 161; both pieces are table facts, one with a zero | correct | distributive law (area model) |
| l6-splitting.json | screens[1].explain (first sentence) | Every cut gives the same total, 161, because the rectangle never changes | correct | (a + b) x c = ac + bc for every a + b = 23 |
| l6-splitting.json | screens[1].widget.options[1].why, feedback.generic, explain | 12 x 7 and 11 x 7 both need their own working; look for a cut where both pieces are table facts; cutting at 20 makes both pieces table facts | imprecise | 12 x 7 = 84 and 11 x 7 = 77 are facts of the 12 by 12 table taught in l5, so the stated criterion also fits the 12 and 11 cut (sim: L2:l6_cut_criterion); the key 20 and 3 is defensible on no-carry grounds, which the text does not give. Finding 5 |
| l6-splitting.json | screens[1].widget.options[2], [3] | 13 x 7 still needs splitting; 22 x 7 is no easier than 23 x 7 | correct | 13 and 22 lie outside the table |
| l6-splitting.json | screens[2] prose, key, explain | Splitting: cut into tens and units, multiply each part; 47 x 6 = 240 + 42 = 282 | correct | definition; distributive law |
| l6-splitting.json | screens[3] key, byKey, explain | 79 x 8 = 560 + 72 = 632; the tens 6 + 7 = 13 carry a hundred; add the pieces as numbers, never as strings of digits; slips 5672, 532, 560, 640 | correct | sim: L2:l6_79x8 |
| l6-splitting.json | screens[4].prose | Zetamac asks things like 12 x 87 | correct | app copy of the default settings: multiplication 2 to 12 by 2 to 100 (sim: L3:l9_zetamac_division) |
| l6-splitting.json | screens[4] key, explain | 12 x 87: 800 + 70 + 160 + 14 = 870 + 174 = 1044 | correct | sim: L2:l6_12x87 |
| l6-splitting.json | screens[5] prose, hints, byKey, explain | 11 shortcut: write the two digits apart with their sum between; when the digits add to 10 or more, carry the 1; 11 x 68 = 680 + 68 = 748 | correct | sim: L2:l6_eleven_shortcut (all two-digit numbers), L2:l6_eleven_no_carry; the carry condition is stated |
| l6-splitting.json | screens[6] prose, options, byKey, explain | 12 x 47 = 400 + 70 + 80 + 14 = 564, not 414; splitting both numbers in two always gives four pieces | correct | sim: L2:l6_trap, L2:l6_four_pieces |
| l6-splitting.json | screens[7].prose, summary.formula | For any numbers (a + b) x c = a x c + b x c; (a + b)(c + d) = ac + ad + bc + bd | correct | distributive law; sim: L2:l6_distributive, L2:l6_four_pieces |
| l6-splitting.json | screens[7] lines, explain | 86 x 7 = 560 + 42 = 602; the tens 6 + 4 = 10 carry a hundred | correct | direct arithmetic |
| l6-splitting.json | screens[8] prose, byKey, explain | 8 x £36.25 = 240 + 48 + 2 = £290.00; 8 lots of 25p is £2 | correct | sim: L2:l6_transfer |
| l6-splitting.json | summary.ideas, summary.trap | Cut at a ten; four pieces all count; add as numbers; tens times tens plus units times units drops two pieces | correct | restates rows above |
| l6-splitting.json | quiz[0..3] | 7 x 86 = 602; 12 x 34 = 408 (308, 348, 368 drop pieces); 11 x 79 = 869; 9 x 58 = 450 + 72 = 522 | correct | sim: L2:l6_quiz |
| l7-near-round.json | screens[0] prose, byKey, explain | 7 x 99 = 700 - 7 = 693; slips 699, 700, 707 | correct | n(100 - 1) = 100n - n |
| l7-near-round.json | screens[1] byKey, explain | 7 x 97 = 700 - 21 = 679; the further from 100, the more lots you pay back | correct | sim: L2:l7_compensate |
| l7-near-round.json | screens[2] prose, byKey, explain | Compensating: round up, pay back the gap in whole lots; 9 x 46 = 460 - 46 = 414; this is the nines pattern on any number | correct | sim: L2:l7_keys |
| l7-near-round.json | screens[3] prose, byKey, explain | Five is half of ten: 5 x 68 = 680 / 2 = 340; 50 x 68 is half of 6800 | correct | sim: L2:l7_halving_rules |
| l7-near-round.json | screens[4] prose, byKey, explain | 25 is a quarter of 100: 7 x 25 = 700 halved twice = 175 | correct | sim: L2:l7_halving_rules |
| l7-near-round.json | screens[5] prose, byKey, explain | Four lots is two lots doubled: 4 x 87 = 174 doubled = 348; doubling twice is times 4, halving twice is a quarter; three doublings is eight lots | correct | 4 = 2 x 2, 8 = 2 x 2 x 2 |
| l7-near-round.json | screens[6] prose, options, byKey, explain | 8 x 98 = 800 - 2 x 8 = 784, not 798; pay back the gap times the other number, never the gap alone | correct | sim: L2:l7_trap |
| l7-near-round.json | screens[7].prose, summary.formula | For any whole n: 99n = 100n - n, 5n = 10n / 2, 25n = 100n / 4; n(100 - k) = 100n - kn | correct | sim: L2:l7_compensate, L2:l7_halving_rules |
| l7-near-round.json | screens[7] lines, explain | 12 x 25 = 1200 / 4 = 600 / 2 = 300; multiplying by 100 adds two zeros (whole numbers); dividing by 4 is two halvings | correct | sim: L2:l7_derive; the numbers in the lesson are whole |
| l7-near-round.json | screens[8] prose, byKey, explain | 250 shares at £12.00: a quarter of £12,000 is £3,000; 25, 250, 2,500 are quarters of 100, 1,000, 10,000 | correct | sim: L2:l7_keys |
| l7-near-round.json | summary.ideas, summary.trap | Round the multiplier, pay back in whole lots; the payback is the gap times the other number; half of ten, quarter of 100 | correct | restates rows above |
| l7-near-round.json | quiz[0], [1], [3] | 6 x 99 = 594; 5 x 86 = 430; 8 x 51 = 400 + 8 = 408 | correct | sim: L2:l7_quiz |
| l7-near-round.json | quiz[2] prose, byKey, explain | A hedge ratio of 0.99 means selling £0.99 of index per £1 of stock; 0.99 x £6,400 = £6,400 - £64 = £6,336 | correct | Hull sec. 3.4 (hedge ratio = size of hedge position over size of exposure); sim: L2:l7_quiz |
| l8-squaring.json | screens[0] key, byKey, explain | 13 x 13 = 100 + 30 + 30 + 9 = 169; the two equal strips make squaring quick; slips 109, 139, 26 | correct | (10 + 3)^2 |
| l8-squaring.json | screens[1] options, explain | The two strips add to 20b; (10 + 4)^2 = 196; double the units digit and put a zero on for the middle piece | correct | 2 x 10 x b; scoped to a side of 10 + b by the screen's prose |
| l8-squaring.json | screens[2].prose, summary.formula | Square of a sum: (a + b)^2 = a^2 + 2ab + b^2 | correct | sim: L2:l8_square_of_sum |
| l8-squaring.json | screens[2] key, byKey, explain | 17^2 = 100 + 140 + 49 = 289; slips 149, 219, 254 | correct | sim: L2:l8_keys |
| l8-squaring.json | screens[3] prose, key, hints, explain | (n + 1)^2 = n^2 + 2n + 1; from 225: 256, 289, 324, 361, then +39 lands on 400; each step adds the next odd number | correct | sim: L2:l8_step, L2:l8_squares_16_19 |
| l8-squaring.json | screens[4] prose, byKey | 19 x 21 = (20 - 1)(20 + 1) = 400 + 20 - 20 - 1 = 399; from 19^2 add two 19s; from 21^2 take two 21s | correct | sim: L2:l8_keys, L2:l8_19x21_slips |
| l8-squaring.json | screens[4].explain | Two numbers either side of a round number multiply to its square, less the gap squared | imprecise | true only when the two numbers are the same distance from it (sim: L2:l8_equal_gaps_only, 72 of 648 pairs); the hypothesis is in the examples, not in the rule. Finding 6 |
| l8-squaring.json | screens[5] prose, options, byKey, explain | 14^2 = 100 + 40 + 40 + 16 = 196, not 116; squaring a sum always has a middle piece, twice the product of the parts | correct | sim: L2:l8_trap |
| l8-squaring.json | screens[6].prose (first sentence); summary.ideas[2]; objectives[2] | For two numbers either side of a round number, the strips always cancel | imprecise | "always" fails for unequal gaps: 18 x 21 = 378 (sim: L2:l8_either_side); the formula that follows carries the hypothesis. Finding 6 |
| l8-squaring.json | screens[6].prose (formula), summary.formula.note | For any a and b: (a - b)(a + b) = a^2 - b^2 | correct | sim: L2:l8_diff_squares |
| l8-squaring.json | screens[6] lines, explain | 19 x 21 = 20^2 + 20 - 20 - 1 = 399; for 18 x 22 the gap is 2, so 400 - 4 = 396 | correct | direct expansion |
| l8-squaring.json | screens[7].prose | Annual volatility 18% is 0.18; variance is the volatility squared | correct | definition: variance = standard deviation squared (Hull sec. 15.4 uses volatility as the standard deviation of the return) |
| l8-squaring.json | screens[7] key, hints, byKey | 0.18^2 = 0.0324; two decimal places times two places gives four; the each-part slip 0.0164 misses two strips of 0.008 | correct | sim: L2:l8_variance |
| l8-squaring.json | screens[7].explain (last sentence) | Variances of independent risks add and volatilities do not | correct | Var(X + Y) = Var X + Var Y for independent X, Y (Casella and Berger, Theorem 4.5.6); sim: L2:l8_variances_add |
| l8-squaring.json | summary.ideas[0], [1], summary.trap | (10 + b)^2 is 100, two strips of 10b and b^2; step by 2n + 1; squaring each part drops the strips | correct | restates rows above |
| l8-squaring.json | quiz[0], [1], [3] | 16^2 = 256 = 225 + 31; 18 x 22 = 400 - 4 = 396 (the gap is squared); 21^2 = 441 | correct | sim: L2:l8_quiz |
| l8-squaring.json | quiz[2].prose | Traders turn daily volatility into annual volatility by multiplying by the square root of 252, for 252 trading days | correct | Hull sec. 15.4: volatility per annum = volatility per trading day x sqrt(252); the standard practitioner convention |
| l8-squaring.json | quiz[2] options, explain | 16^2 = 256 is 4 above 252 and 15^2 = 225 is 27 below, so the root is nearest 16; 1% a day is about 16% a year | correct | sqrt(252) = 15.87; sim: L2:l8_root_252, L2:l8_nearest_square (nearest square gives the nearest whole root for every whole n) |
| review-2.json | items[0], [1] | 6 x 8 = 48 = 40 + 8; neighbours 42, 54, 56; 12 x 9 = 90 + 18 = 108 = 120 - 12 | correct | sim: L2:review2_keys |
| review-2.json | items[2], [3] | 8 x 67 = 480 + 56 = 536 (tens 8 + 5 = 13 carry); 11 x 57 = 627 (5 + 7 = 12 carries) | correct | sim: L2:review2_keys |
| review-2.json | items[4], [5] | 12 x 63 = 600 + 30 + 120 + 6 = 756 = 630 + 126; 4 x 98 = 400 - 8 = 392 | correct | sim: L2:review2_keys |
| review-2.json | items[6] | 3% means 3 for every 100; 3% of £1,200 is 12 x £3 = £36 | correct | definition of per cent; sim: L2:review2_keys |
| review-2.json | items[7] | 2.5% is 0.025 = 25/1000; 0.025 x £400,000 = 25 x £400 = £10,000; slips £100,000 (0.25), £1,000 (0.0025), £20,000 (50 lots) | correct | sim: L2:review2_keys |
| review-2.json | items[8], [9] | 18^2 = 324 (or 400 - 40 - 40 + 4); 17 x 23 = 20^2 - 3^2 = 391 | correct | sim: L2:review2_keys; 17 and 23 are both 3 from 20 |
| homework-2.json | items[0] | 6 x 7 = 36 + 6; 7 x 8 = 49 + 7; 8 x 9 = 80 - 8; 7 x 12 = 70 + 14 | correct | direct arithmetic |
| homework-2.json | items[1] | 9 x £47.80 = £478.00 - £47.80 = £430.20 | correct | sim: L2:hw2_keys |
| homework-2.json | items[2] | 12 x 96 = 1200 - 48 = 960 + 192 = 1152; two routes that agree are a check; slips 912, 1196, 1188 | correct | sim: L2:hw2_keys |
| homework-2.json | items[3] | Hedge ratio 0.98: £8,400 - 0.02 x £8,400 = £8,232 | correct | sim: L2:hw2_keys; Hull sec. 3.4 |
| homework-2.json | items[4] | 0.0025 is 25 ten-thousandths; 0.0025 x £4,800,000 = 25 x £480 = £12,000 | correct | sim: L2:hw2_keys |
| homework-2.json | items[5] | 37 x 43 = (40 - 3)(40 + 3) = 1600 - 9 = 1591; the strips +120 and -120 cancel | correct | sim: L2:hw2_keys; both numbers are 3 from 40 |
| homework-2.json | items[6] | (10 + b)^2 = 100 + 10b + 10b + b^2 = 100 + 20b + b^2; forgetting one strip gives 156 for 14^2 | correct | sim: L2:hw2_derive |
| homework-2.json | items[7] key, explain | 85^2 = 6400 + 800 + 25 = 7225; for any number ending in 5, (10n + 5)^2 = 100n(n + 1) + 25 | correct | sim: L2:hw2_ends_in_5 (n up to 999) |
| homework-2.json | items[8] | 0.24^2 = 0.0576; each-part slip 0.0416 misses two strips of 0.008 | correct | sim: L2:hw2_keys |
| homework-2.json | items[9].model, rubric | 12 x £49 = £588 by compensating (600 - 12), splitting (490 + 98) and the grid (400 + 90 + 80 + 18); slips 599 and 418 | correct | sim: L2:hw2_longform |
| l9-missing-multiplication.json | screens[0].prose, screens[1] | Every division hides a multiplication; 84 / 7 = 12 because 7 x 12 = 84; the row number is the answer | correct | definition of division as the inverse of multiplication |
| l9-missing-multiplication.json | screens[2] key, byKey, explain | 72 sits in four cells (6 x 12, 8 x 9 both ways); each place gives its own division facts | correct | sim: L3:l9_cells_72 |
| l9-missing-multiplication.json | screens[3].prose, screens[8].prose (first formula) | The missing factor: a / b = c means b x c = a | correct | definition (b not 0; every divisor in the course is from 2 to 12) |
| l9-missing-multiplication.json | screens[3] byKey, explain | 108 / 9 = 12; 9 x 11 = 99 falls 9 short; 9 x 13 = 117 overshoots by 9 | correct | direct arithmetic |
| l9-missing-multiplication.json | screens[4].prose | The 4 times table stops at 48, so 96 is off the table | imprecise | 96 is in the 12 by 12 table as 8 x 12 and 12 x 8 (sim: L3:l9_96_off_table); it is past the end of column 4 only, and screens[2] has just said a number sits in several places. Finding 7 |
| l9-missing-multiplication.json | screens[4] key, byKey, explain | 96 / 4 = 80 / 4 + 16 / 4 = 20 + 4 = 24; splitting works because both pieces share the height 4 | correct | (x + y) / b = x / b + y / b; sim: L3:l9_split_dividend |
| l9-missing-multiplication.json | screens[5] prose, byKey, explain | Since 4 = 2 x 2, dividing by 4 is halving twice; 136 / 4 = 34; three halvings divide by 8 | correct | sim: L3:l9_halving_doubling |
| l9-missing-multiplication.json | screens[6] prose, byKey, explain | A 5 is half a 10, so any number holds twice as many 5s as 10s; 115 / 5 = 230 / 10 = 23 | correct | n / 5 = 2n / 10; sim: L3:l9_halving_doubling |
| l9-missing-multiplication.json | screens[7] prose, options, byKey, explain | 84 / 12 = 7, not 84 / 10 + 84 / 2 = 50.4; the two strips share one width; split the number being divided, never the divisor | correct | sim: L3:l9_trap, L3:l9_never_split_divisor (no positive case where the divisor split holds); "split" is additive, factoring the divisor (4 = 2 x 2) is taught separately |
| l9-missing-multiplication.json | screens[8].prose, summary.formula | (x + y) / b = x / b + y / b; halving twice divides by 4; doubling then dividing by 10 divides by 5 | correct | sim: L3:l9_split_dividend, L3:l9_halving_doubling |
| l9-missing-multiplication.json | screens[8] options, explain | 156 / 12 = 120 / 12 + 36 / 12 = 10 + 3 = 13; the half-done option leaves 36 undivided | correct | 12 x 13 = 156 |
| l9-missing-multiplication.json | screens[9] lines, explain | 184 / 8 = 92 / (2 x 2) = 46 / 2 = 23; each halving removes one 2 | correct | sim: L3:l9_keys |
| l9-missing-multiplication.json | screens[10] key, byKey, explain | £764.00 / 8 = £95.50; the last halving splits the odd £1 into two 50p halves; £95.10 writes the remainder as a digit | correct | sim: L3:l9_keys |
| l9-missing-multiplication.json | summary.ideas, summary.trap | Missing factor; split the dividend into multiples of the divisor; halve twice or three times; double then divide by 10; 84 / 12 is not 84 / 10 + 84 / 2 | correct | restates rows above |
| l9-missing-multiplication.json | quiz[0], [2], [3] | 72 / 6 = 12; 135 / 5 = 27; 192 / 8 = 24 by three halvings; the wrong workings give 48, 96 and 52 | correct | sim: L3:l9_quiz |
| l9-missing-multiplication.json | quiz[1].prose | In a default Zetamac round, division answers go up to 100 | correct | app copy: division is multiplication (2 to 12 by 2 to 100) reversed with the 2 to 12 factor as divisor (sim: L3:l9_zetamac_division; `app/js/engine/arith.js` returns whole / a) |
| l9-missing-multiplication.json | quiz[1] key, explain | 700 / 7 = 100; the zeros carry straight across | correct | 7 x 100 = 700 |
| l10-known-decimals.json | screens[1] prose, byKey, explain | Halving 1 three times gives 0.5, 0.25, 0.125, so 1/8 = 0.125; eighths are a little bigger than tenths | correct | sim: L3:l10_eighths, L3:l10_orderings |
| l10-known-decimals.json | screens[2] key, byKey, explain | 5/8 = 5 x 0.125 = 0.625 = 1/2 + 1/8; 1.6 is 8 / 5 | correct | sim: L3:l10_eighths |
| l10-known-decimals.json | screens[3].prose | 1/8 is a unit fraction: one piece of the whole; every other eighth is a multiple of it | correct | definition (numerator 1) |
| l10-known-decimals.json | screens[3] key, byKey, explain | 7/8 = 1 - 0.125 = 0.875; 7/8 is more than 0.7; 0.88 is a rounding, not exact | correct | sim: L3:l10_eighths, L3:l10_orderings |
| l10-known-decimals.json | screens[4] prose, byKey, explain | 1/3 = 0.333... for ever; a sixth is half a third, 0.1666...; to three places look at the fourth digit: 0.167 | correct | sim: L3:l10_rounding; Hardy and Wright sec. 9.1 (recurring decimals) |
| l10-known-decimals.json | screens[4].widget.accept | 0.167; also 0.1667 or 0.16667 | correct | sim: L3:l10_sixth_tolerance (tolerance 0.00035 accepts both, rejects 0.166) |
| l10-known-decimals.json | screens[5] prose, byKey, explain | 1/12 is half a sixth, 0.08333..., about 0.0833; 7/12 = 1/2 + 1/12 = 0.5833; twelfths are smaller than tenths | correct | sim: L3:l10_rounding, L3:l10_orderings |
| l10-known-decimals.json | screens[6] prose, byKey, explain | 23 / 4 is 5 remainder 3; the 3 left over is 3/4 of a row, so 5.75 | correct | sim: L3:l10_remainder_keys |
| l10-known-decimals.json | screens[7] prose, options, explain | 38 / 8 = 4 remainder 6 = 4 + 6/8 = 4.75; the remainder counts eighths, not tenths; 7 / 2 = 3.5, not 3.1 | correct | sim: L3:l10_remainder_keys |
| l10-known-decimals.json | screens[8].prose, summary.formula | a / b = q remainder r = q + r / b; r is always less than b; 1/8 = 0.125, 1/3 about 0.333, 1/6 about 0.167, 1/12 about 0.083 | correct | division algorithm (Hardy and Wright ch. 1); sim: L3:l10_remainder_formula |
| l10-known-decimals.json | screens[8] options, explain | 29 / 6 = 4 + 5/6, and 5/6 = 1 - 1/6, about 0.833, so 4.83 | correct | sim: L3:l10_rounding |
| l10-known-decimals.json | screens[9] prose, lines, explain | 5/12 = 4/12 + 1/12 = 1/3 + 1/12, about 0.33333 + 0.08333 = 0.41666, about 0.4167; carrying the extra place keeps the rounding right | correct | sim: L3:l10_carry_extra_place (four-place pieces give 0.4166, the wrong last digit) |
| l10-known-decimals.json | screens[10] prose, key, byKey, explain | The return is the profit as a fraction of the capital used; £2,500 / £30,000 = 25/300 = 1/12, about 0.0833, an 8.33% return | correct | simple return = profit / capital (Hull sec. 4.2 convention for a holding-period return); sim: L3:l10_return |
| l10-known-decimals.json | summary.ideas, summary.trap | Unit fractions to know; build the rest; a remainder is a fraction of the divisor; 7 / 2 is 3.5, the remainder counts halves | correct | restates rows above |
| l10-known-decimals.json | quiz[0..3] | 3/8 = 0.375 (0.38 is its two-place rounding); 2/3 = 0.667 to three places; 45 / 8 = 5.625; 11/12 = 1 - 0.0833 = 0.9167, 0.92 to two places | correct | sim: L3:l10_eighths, L3:l10_rounding, L3:l10_remainder_keys |
| l11-percent-shortcuts.json | screens[0] key, byKey, explain | One strip of ten of £340 is £34, so 10% is £34; dividing by 10 moves each digit one place to the right | correct | place value; sim: L3:l11_pieces |
| l11-percent-shortcuts.json | screens[1] key, byKey, explain | 5% of £340 is half of £34, £17; halving 10% gives 5% every time | correct | sim: L3:l11_halving |
| l11-percent-shortcuts.json | screens[2] prose, byKey, explain | Per cent means per hundred; 1% is one hundredth; dividing by 100 moves each digit two places; 1% of £340 is £3.40; £0.34 is 0.1% | correct | definition; sim: L3:l11_pieces |
| l11-percent-shortcuts.json | screens[3] key, byKey, explain | 17% of £340 = £34 + £17 + £6.80 = £57.80 | correct | sim: L3:l11_pieces |
| l11-percent-shortcuts.json | screens[4] key, byKey, explain | 35% of £240 = £72 + £12 = £84; £96 is 40%; £8.40 is 3.5% | correct | sim: L3:l11_keys |
| l11-percent-shortcuts.json | screens[5] prose, byKey, explain | 49% from pieces would take nine of them; 49% of £260 = £130 - £2.60 = £127.40 | correct | sim: L3:l11_nine_pieces (four 10s, one 5, four 1s is the minimum), L3:l11_keys |
| l11-percent-shortcuts.json | screens[6] prose, options, byKey, explain | 0.5% of £3,600 is half of 1% (£36): £18; reading 0.5% as 5% gives £180, ten times the fee; £1.80 is 0.05% | correct | sim: L3:l11_keys |
| l11-percent-shortcuts.json | screens[7].prose, summary.formula | 10% is A / 10, 5% is half of that, 1% is A / 100; p per cent of A is (p / 100) x A; add pieces or subtract from an easy neighbour | correct | definition of percentage; distributive law |
| l11-percent-shortcuts.json | screens[7] options, explain | 23% of £600 = 2 x £60 + 3 x £6 = £138; £123 adds £3 not 3%; £78 is 13%; £300 treats 1% as £60 | correct | sim: L3:l11_keys |
| l11-percent-shortcuts.json | screens[8] prose, lines, explain | 2.5% is half of 5%; 17.5% of £240 = £24 + £12 + £6 = £42 | correct | sim: L3:l11_keys |
| l11-percent-shortcuts.json | screens[9] prose, key, explain | A 60:40 book of £8,450: £5,070 in equities, £3,380 in bonds; the sleeves add back to the total | correct | sim: L3:l11_keys |
| l11-percent-shortcuts.json | summary.ideas, summary.trap | 10%, 5%, 1% pieces; build up or come down from a neighbour; small rates start from 1%; 0.5% of £3,600 is £18, not £180 | correct | restates rows above |
| l11-percent-shortcuts.json | quiz[0..3] | 5% of £780 = £39; 1% of £2,350 = £23.50; 15% of £86 = £12.90; a 21% rise on £300 gains £63 | correct | sim: L3:l11_quiz |
| l12-against-the-clock.json | screens[0].prose | A Zetamac round gives 120 seconds of mixed questions | correct | `app/content/warmup.json` seconds 120, four operations |
| l12-against-the-clock.json | screens[1] key, byKey, explain | Score 30 in 120 s is 4 s an answer; the 10th answer is due at 40 s, a third of the round | correct | sim: L3:l12_pace |
| l12-against-the-clock.json | screens[2] key, byKey, explain | Score 40 needs 3 s an answer; 1/3 is answers per second; each second saved per answer adds a lot of score at the fast end | correct | score = 120 / pace is convex; sim: L3:l12_fast_end (4 s to 3 s adds 10, 10 s to 9 s adds 1) |
| l12-against-the-clock.json | screens[3].prose | Pace is seconds per answer: pace = 120 / score; sort each division before starting it | correct | definition; matches screens[1] |
| l12-against-the-clock.json | screens[3] key, hints, byKey, explain | The answer is past the table exactly when the number exceeds the divisor times 12: 96 / 4, 135 / 5, 176 / 8; 84 / 7 and 132 / 11 land on 12 | correct | sim: L3:l12_past_table |
| l12-against-the-clock.json | screens[4] canvas (method card), key, byKey | Card: in the table, recall; by 4 or 8, halve twice or three times; by 5, double then divide by 10; otherwise split at multiples of the divisor; answers 12, 24, 23, 21, 13 | correct | each method proved in l9 rows; direct arithmetic |
| l12-against-the-clock.json | screens[5].prose | A score of 25 means about 48 seconds for ten | correct | 120 / 25 = 4.8 s; ten answers 48 s (sim: L3:l12_pace); 25 is the Stage 0 target in `warmup.json` |
| l12-against-the-clock.json | screens[5] key, hints, byKey, explain | 7, 27, 29, 11, 31, 13, 39, 24, 14, 8; three recall, two halvings, two doublings, three splits | correct | sim: L3:l12_round_of_ten, L3:l12_method_counts |
| l12-against-the-clock.json | screens[6] prose, key, byKey, explain | One round is noisy, so average the week; mean of 18, 21, 19, 24, 23 is 105 / 5 = 21; Thursday and Friday are above it | correct | sim: L3:l12_average; arithmetic mean |
| l12-against-the-clock.json | screens[7] prose, options, byKey, explain | 126 / 7 split as 100 + 26 leaves 14 r 2 and 3 r 5; 120 + 6 also leaves remainders; split at multiples of 7: 70 + 56 gives 10 + 8 = 18; the divisor cannot be split | correct | sim: L3:l12_splits |
| l12-against-the-clock.json | screens[8].prose, summary.formula | a / b = (mb + nb) / b = m + n; choose mb and nb as multiples of b you know | correct | sim: L3:l12_split_formula |
| l12-against-the-clock.json | screens[8] key, screens[9] lines | 232 / 8 = 29 by three halvings; 204 / 12 = 120 / 12 + 84 / 12 = 10 + 7 = 17 | correct | sim: L3:l12_keys |
| l12-against-the-clock.json | screens[10] key, hints, byKey, explain | £1,182 / 12 = (1200 - 18) / 12 = 100 - 1.5 = £98.50; £9.60 on £3,200 is 0.3%, 0.003; £1,500 on £12,000 is 1/8 = 0.125; 40% of £7,250 is £2,900 | correct | sim: L3:l12_transfer; splitting by subtraction is the same identity with y negative |
| l12-against-the-clock.json | summary.ideas[0], [1], summary.trap | Pace is 120 / score, 30 needs 4 s; sort before you work; 100 + 26 leaves remainders in both pieces | correct | restates rows above |
| l12-against-the-clock.json | summary.ideas[2] | Split at multiples of the divisor, not at round numbers: 126 is 70 + 56 for 7 | imprecise | the instruction is right, but 70 is itself a round number, as are 120, 140 and 90 in the lesson's own good splits; the contrast meant is with a round number that is not a multiple of the divisor. Finding 8 |
| l12-against-the-clock.json | quiz[0..3] | Pace 120 / 30 = 4; 196 / 7 = 140 / 7 + 56 / 7 = 28; 117 / 9: split 90 + 27, halving gives 58.5, doubling divides by 5; mean of 22, 25, 24, 27, 27 is 25 (27 is the mode) | correct | sim: L3:l12_keys |
| review-3.json | items[0..4] | 96 / 12 = 8; 17% of £260 = £44.20; 53 / 4 = 13.25; pace 120 / 24 = 5 s; 216 / 8 = 27 | correct | sim: L3:review3_keys |
| review-3.json | items[5] | 5/6 = 1 - 0.1666... = 0.8333..., 0.833 to three places; also 0.8333 accepted; 0.834 rounds up wrongly | correct | sim: L3:l10_rounding; tolerance 0.00035 |
| review-3.json | items[6] | 0.25% of £6,400 is a quarter of 1% (£64): £16; £160 is 2.5%; £1.60 is 0.025% | correct | sim: L3:review3_keys |
| review-3.json | items[7] | 147 / 7: 140 + 7 gives 20 + 1 = 21; 100 + 47 and 120 + 27 leave remainders in both pieces | correct | sim: L3:l12_splits |
| review-3.json | items[8], [9] | 165 / 5 = 330 / 10 = 33; £7,000 on £42,000 is 1/6, 0.1667 to four places | correct | sim: L3:review3_keys, L3:l10_rounding |
| homework-3.json | items[0], [1] | 228 / 12 = 10 + 9 = 19 (the divisor split gives 136.8); 13, 46, 37, 19, 14 | correct | sim: L3:hw3_keys, L3:hw3_timed |
| homework-3.json | items[2] | £1,026 / 8 = 513, 256.5, 128.25; the remainder 1 is half of 2, not a tenth | correct | sim: L3:hw3_keys |
| homework-3.json | items[3], [7] | 11/12 = 1 - 0.08333... = 0.9167; £1,000 on £24,000 is 1/24, half of 1/12, 0.0417 to four places | correct | sim: L3:l10_rounding, L3:hw3_keys |
| homework-3.json | items[4], [5] | £850.50 / 9 = 810 / 9 + 40.5 / 9 = £94.50; 23% of £1,850 = £370 + £55.50 = £425.50 | correct | sim: L3:hw3_keys |
| homework-3.json | items[6] | 60:40 of £12,500 is £7,500 and £5,000; 0.2% of £7,500 is a fifth of £75: £15 | correct | sim: L3:hw3_book |
| homework-3.json | items[8] prose, key, explain | p% of A = (p / 100) x A = (A / 100) x p, so 36% of 25 equals 25% of 36 = 9 | correct | commutativity; sim: L3:hw3_swap (all p, A from 1 to 100) |
| homework-3.json | items[9].model, rubric | £1,148 / 8 = £143.50 (143 remainder 4 is 4/8); 0.15% of £1,148 is £1.722, and £17.22 is 1.5%; £287 / £1,148 = 1/4 = 0.25 | correct | sim: L3:hw3_blotter |

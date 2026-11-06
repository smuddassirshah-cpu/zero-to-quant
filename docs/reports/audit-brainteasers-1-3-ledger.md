# Claim ledger: brainteasers L1 to L3 (concept audit, blind)

Scope: `app/content/courses/brainteasers/` l1 to l16, review-1 to review-3, homework-1 to homework-3. One row per definition, result, method step, convention, always/never/every/only claim, causal claim and the reasoning in each explain, why, hint and feedback line. Verdicts: correct, wrong, imprecise, misleading, unverified. `sim: L<n>:<name>` points at a check in `docs/reports/brainteasers-L<n>-concepts.py` (each prints `ok <name>`). Sources: Engel, *Problem-Solving Strategies* (Springer 1998) ch. 1 (invariance principle), ch. 2 (colouring proofs), ch. 4 (pigeonhole); Zhou, *A Practical Guide to Quantitative Finance Interviews* ch. 2 (brain teasers); Dyson (1946) "The problem of the pennies", *Math. Gazette* 30; Crack, *Heard on the Street*; Osborne, *An Introduction to Game Theory* ch. 5 to 7 (backward induction); Fagin, Halpern, Moses and Vardi, *Reasoning About Knowledge* ch. 1 and 7 (muddy children, common knowledge); Gál and Miltersen (2003) / Curtin and Warshauer (2006) "The locker puzzle", *Math. Intelligencer* 28; Rote (2002) "Crossing the bridge at night", *EATCS Bulletin* 78; Hardy and Wright, *An Introduction to the Theory of Numbers* ch. 5 and 6 (congruences, Fermat); Graham, Knuth and Patashnik, *Concrete Mathematics* ch. 2 (sums).

Paths are JSON paths inside the named file; `s3` abbreviates `screens[3]`, `q1` `quiz[1]`, `i4` `items[4]`, `o2` `widget.options[2]`, `w1` `widget.wrong[1]`.

## Level 1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | s0.hints, feedback, explain | Red meets blue, then green meets blue twice, takes (1,2,3) to (4,2,0); each step removes one blue | correct | sim: L1:l1 s0 (BFS distance 3) |
| l1 | s0.widget.states.*.ops[].why | A colour with count 0 cannot meet | correct | rule of the puzzle |
| l1 | s1.o1.why, byKey.even | The total never changes, so it cannot separate targets | correct | each meeting is -1, -1, +2: total fixed |
| l1 | s1.o2.why, byKey.longer | Only nine positions are reachable from 1, 2, 3 and none has one colour | correct | sim: L1:l1 s1 byKey.longer |
| l1 | s1.o3.why, byKey.red | Green and blue never both reach 0 | correct | g - b = -1 mod 3 invariant; sim: L1:l1 s1 byKey.red |
| l1 | s1.hints[1..2], explain | A meeting moves two counts by -1 and one by +2, so every pairwise difference moves by 0 or ±3; residues mod 3 are invariant; one colour needs a difference of 0 | correct | derivation: (x-1)-(y-1) = x-y; (x-1)-(z+2) = x-z-3; Engel ch. 1 E7; sim: L1:l1 s1 explain |
| l1 | s2.prose | Definition: an invariant is a quantity no move changes | correct | Engel ch. 1 |
| l1 | s2.hints, explain, byKey.* | Turning k heads and 4-k tails changes heads by 4-2k, even; 9 odd never reaches 0 | correct | derivation; sim: L1:l1 s2 |
| l1 | s2.explain.canvas.caption | Closest reachable is 1 head | correct | sim: L1:l1 s2 (min reachable heads 1) |
| l1 | s3.explain | a+b+ab = (a+1)(b+1)-1, product of (x+1) invariant, 5040-1 = 5039 for any order | correct | identity; sim: L1:l1 s3 (all orders) |
| l1 | s4.lines, d1.why | Proof order identity, invariant, start value, end value, conclusion; the sum is not invariant (move adds ab) | correct | derivation |
| l1 | s4.explain | Every invariant proof: show a move cannot change the quantity, compare start and end | correct | Engel ch. 1 |
| l1 | s5.prose (candidate) | Each row/column move toggles 3 lamps so the lit parity flips | correct | 3 is odd |
| l1 | s5.o1.why, byKey.parity | Parity allows 1 but a finer invariant rules it out; parity allowing a target does not prove it reachable | correct | sim: L1:l1 s5 (32 patterns, none with 1 lit) |
| l1 | s5.o2.why, o3.why | Row 1 then columns 2, 3 leave 5 on; a row and a column leave 4 on | correct | sim: L1:l1 s5 option 3/4 why |
| l1 | s5.hints[2], explain | A row or column move toggles 0 or 2 lamps of any 2 x 2 block, so each block's lit count stays even; only 32 of 512 patterns reachable | correct | a line meets a 2 x 2 block in 0 or 2 cells; GF(2) span of 6 generators with one relation has dimension 5; sim: L1:l1 s5 |
| l1 | s6.prose | Contest Practice lesson 8 (Parity and invariants) showed an invariant allowing the target is not a route | correct | `contests/l8-invariants.json` screen "An invariant is not a route" |
| l1 | s6.hints, byKey.two, explain | Two moves change heads by at most 8, so 3 moves at least; 10, 6, 4, 0 works | correct | sim: L1:l1 s6 (BFS 3) |
| l1 | s6.byKey.never | Parity now allows it: heads change by an even number and 10 is even | correct | derivation |
| l1 | s7.prose | I(start) != I(target) implies unreachable | correct | contrapositive of invariance |
| l1 | s7.prose, summary.ideas[2] | A quantity that only falls is a monovariant: it proves a process stops | imprecise | needs the quantity to take whole-number (or well-ordered) values and be bounded below; x_n = 1/n only falls and never stops. Engel ch. 1 ("a strictly decreasing positive integer function ... the process terminates") |
| l1 | s7.prose | Zhou (ch. 2), Crack, Joshi are rich in invariant puzzles | correct | Zhou ch. 2 "Brain Teasers" (coloured lizards, chessboard tiling); Crack ch. on brainteasers |
| l1 | s7.o1.why, o2.why | Coin total does not separate start from target; move count only grows | correct | derivation |
| l1 | s8.hints, explain, byKey.* | a+b-1 lowers the sum by 1; 19 moves; 210 - 19 = 191 | correct | sum of 1..20 = 210; n numbers take n-1 moves; sim: L1:l1 s8 |
| l1 | s9.hints, explain, o3..o5.why | P (2,5,8): differences 3, 3, 6, all 0 mod 3, every colour reachable, all blue in 5 meetings; Q (4,6,8): differences 2, 2, 4, never 0 mod 3, never one colour | correct | sim: L1:l1 s9 (BFS on both islands) |
| l1 | s9.hints[2] | One colour needs two counts of 0, a difference of 0 mod 3 | correct | derivation |
| l1 | s10.hints, explain, byKey.* | A neighbour swap flips exactly one pair; reversal needs C(6,2) = 15 flips; bubble sort does it in 15 | correct | inversion count; sim: L1:l1 s10 (BFS 15) |
| l1 | s11.hints, explain, byKey.* | 2(a+b+2ab)+1 = (2a+1)(2b+1); product 3*5*7*9 = 945 = 2N+1; N = 472; old product of (x+1) no longer invariant | correct | identity; sim: L1:l1 s11 (all orders) |
| l1 | s11.prose | Contest Practice lesson 8 checked that a fill leaves cash plus holdings unchanged | correct | `contests/l8-invariants.json` backtest fills screen |
| l1 | summary.ideas[0..1], formula | Invariant definition and test; agreement proves nothing | correct | Engel ch. 1 |
| l1 | summary.trap | Lit parity flips each move yet 1 lamp unreachable: each 2 x 2 block stays even | correct | sim: L1:l1 s5 |
| l1 | q0.o1.why, o2.why, explain | Each move changes heads by 2, 0, -2; 11 stays odd; no move turns one coin | correct | sim: L1:l1 quiz 0 |
| l1 | q1.o0.why, o1.why | One lit lamp leaves a block odd; two lit lamps always leave a block with exactly one | correct | sim: L1:l1 quiz 1 option 1/2 why (all 36 pairs) |
| l1 | q1.o6.why, o7.why | 7 on is the complement of 2 on (toggle every row complements the grid); 8 on mirrors 1 | correct | toggling all three rows toggles every lamp once; sim: L1:l1 quiz 1 |
| l1 | q1.explain, feedback.correct | Reachable counts 0, 3, 4, 5, 6, 9 with constructions | correct | sim: L1:l1 quiz 1 |
| l1 | q2.o1..o3.why, explain | (x+1) product fits a+b+ab only; sum gains 2ab; (a+2)(b+2) = ab+2a+2b+4; (2a+1)(2b+1) = 2(a+b+2ab)+1 | correct | expansions |
| l1 | q3.explain, byKey.* | a+b+1 raises the sum by 1; 9 moves; 55 + 9 = 64 | correct | sim: L1:l1 quiz 3 |
| l2 | s0.hints, explain, byKey.* | 5 x 5 chessboard: 13 dark (corners, centre) and 12 light; a domino covers one of each; removed square must be dark; every dark removal tiles | correct | Engel ch. 2; sim: L1:l2 s0 (13 tilings found, 12 light removals fail) |
| l2 | s0.explain principle | Colour so each piece covers the colours in a fixed way, then count | correct | Engel ch. 2 |
| l2 | s1.hints, explain, o1.why, o2.why | A knight move changes i+j by ±1 or ±3 (odd), so flips shade; A and B both dark; odd move counts impossible | correct | derivation; sim: L1:l2 s1 (distance parity = colour parity) |
| l2 | s2.hints, explain, byKey.* | i+j rises 14, at most 3 per move, so 5 at least; parity rules out 5; 6 attained | correct | sim: L1:l2 s2 (BFS 6) |
| l2 | s3.hints, explain, byKey.far | A door step changes shade; rooms 1, 3, ..., 25 share S's shade; the end is one of the 12 other dark rooms; each ends some tour; 824 tours from the corner | correct | sim: L1:l2 s3 (824 Hamiltonian paths, endpoint set = dark minus S) |
| l2 | s4.canvas caption, rows | Colour (i+j) mod 4 numbered from the corner: counts 9, 10, 9, 8 | correct | sim: L1:l2 s4 counts |
| l2 | s4.hints[1], explain, byKey.r4c1 | A straight 1 x 4 covers four consecutive values of i+j, one of each colour; nine tiles need 9 of each; no tiling; area is necessary never sufficient | correct | Engel ch. 2 E3; sim: L1:l2 s4 (search) |
| l2 | s5.o1..o3.why, explain | Removing 2 and 5 isolates squares 1 and 6; removing 1 and 4 leaves two neighbouring pairs; balanced colours are necessary not sufficient | correct | inspection |
| l2 | s6.prose | #A != #B implies no tiling; equal counts prove nothing; cut chessboard in Contest Practice lesson 8 | correct | `contests/l8-invariants.json` "Dominoes on a chessboard" |
| l2 | s6.o1.why, o2.why, explain | A 1 x 3 covers 2 and 1 on a chessboard; an upright tile crosses alternate rows; (i+j) mod 3 gives one of each class per tile | correct | derivation |
| l2 | s7.lines, d1.why | Proof order; chessboard balances 18/18 and each 1 x 4 covers 2 and 2, so it proves nothing | correct | derivation |
| l2 | s8.hints, explain, o1..o2.why | A T covers 3 of one shade and 1 of the other, ±2 to dark minus light; nine ±2 terms sum to an odd multiple of 2, never 0; four T pieces do tile 4 x 4 | correct | sim: L1:l2 s8 (6 x 6 search fails, 4 x 4 tiling found) |
| l2 | s9.o1..o3.why, explain | A closed tour alternates shades and returns, so needs equal counts; 16 splits 8/8 and a cycle exists; 25 cannot split | correct | sim: L1:l2 s9 (cycle found on 4 x 4, none on 5 x 5) |
| l2 | s10.hints, explain, o1.why, o3.why | 7 x 7 has 25 dark, 24 light; only a dark square can go; corner and third square along an edge are dark and both tile; next-to-corner is light | correct | sim: L1:l2 s10 (search) |
| l2 | s11.canvas caption, hints[1] | Shaded cubes have even coordinate sum; corners are even, 14 of 27; centre odd | imprecise | true with coordinates 0, 1, 2; with 1, 2, 3 the corners are odd and the centre even. The counts (14 with the corners, 13 with the centre) and the conclusion are unaffected; sim: L1:l2 s11 |
| l2 | s11.explain, o1.why, o2.why | A path of 27 alternates, so it starts and ends on the corner's colour; the centre has the other; connectivity does not help | correct | sim: L1:l2 s11 (no corner-to-centre Hamiltonian path) |
| l2 | summary.ideas, formula, note | Colouring test; colours never prove a tiling possible; for 1 x k tiles colour by (i+j) mod k | correct | Engel ch. 2 |
| l2 | q0.o1..o2.why, explain | Tour of 25 ends on the start's shade; the neighbour has the other; the count is fixed at 25 | correct | sim: L1:l2 quiz 0 |
| l2 | q1.o1..o2.why, explain | A path from the centre needs 14 of the centre's colour; only 13 exist; corner and centre are not symmetric | correct | sim: L1:l2 quiz 1 (search from centre fails) |
| l2 | q2.o1..o2.why, explain | Each move flips the shade on any board; 9 moves cannot return | correct | derivation |
| l3 | s0.hints, explain, byKey | Worst hand is one of each colour; the fourth matches; 3 is not enough | correct | Engel ch. 4; sim: L1:l3 s0 |
| l3 | s1.hints, explain, byKey.* | Pairs (k, 13-k) are six boxes; seven picks force a pair; 1 to 6 shows six can fail | correct | sim: L1:l3 s1 |
| l3 | s2.hints, explain, o1..o2.why | Counts 0..5; 0 and 5 cannot coexist (a 5 shook everyone); five values for six guests | correct | Engel ch. 4 E1 |
| l3 | s3.lines, d1.why | Nothing forces a guest to shake hands; the proof must handle 0 | correct | derivation |
| l3 | s4.hints, explain, byKey.* | Worst case takes all 7 red and 4 green first; 11 + 2 = 13 | correct | sim: L1:l3 s4 |
| l3 | s5.prose, summary.formula | n objects in k boxes: some box holds at least ceil(n/k); worst case then add one | correct | Engel ch. 4 |
| l3 | s5.prose | Met in Reasoning and Proof lesson 9 and Counting and Chance lesson 10 | correct | `proof/l9-one-to-one-onto.json` (5,000 ids, 1,024 buckets), `counting-chance/l10-birthday.json` |
| l3 | s5.o1..o2.why, explain | Numbers are objects; sums are not what you place; each pick lands in its pair | correct | derivation |
| l3 | s6.hints, explain, o1..o2.why | Nine unit squares, ten points, two share one, at most sqrt 2 apart; nine points 1.5 apart show nine are not enough | correct | diameter of a closed unit square is sqrt 2; sim: L1:l3 s6 |
| l3 | s7.hints, explain, byKey.* | 3 x 13 = 39 < 40 so some counterparty has 4; one 4 and twelve 3s shows 5 is not certain | correct | ceil(40/13) = 4 |
| l3 | s8.hints, explain, byKey.* | Boxes {0}, {5}, {1,9}, {2,8}, {3,7}, {4,6}; two in a box have sum or difference divisible by 10; seven force it; 0..5 shows six can fail | correct | sim: L1:l3 s8 (max residue set of size 6) |
| l3 | s9.hints, explain, byKey.* | Worst case empties blue and red (16) then two green: 18 | correct | sim: L1:l3 s9 |
| l3 | s10.hints, explain, byKey.* | Two of each of four colours is 8 with no three alike; ninth forces it | correct | sim: L1:l3 s10 |
| l3 | s11.prose, explain, byKey.* | k colours, r alike: k(r-1)+1; hashing n keys into k buckets puts ceil(n/k) in one | correct | Engel ch. 4 |
| l3 | summary.trap | Two blue need 13 not 4 | correct | sim: L1:l3 s4 |
| l3 | q0.o1..o2.why, explain | Six can take one from each pair; 12, 11, 10, 4, 5, 6 also works; bound tight when one per box possible | correct | 12+1, 11+2, 10+3, 4+9, 5+8, 6+7 are the pairs; inspection |
| l3 | q1.explain, byKey.* | 24 each is 96 so some flavour has 25; 25 each shows 26 is not certain | correct | ceil(100/4) = 25 |
| l3 | q2.explain, byKey.* | 12 months, 13 people; 25 forces three | correct | ceil(25/12) = 3 |
| l4 | s0.hints, explain | One weighing has three outcomes, so finishes 3 suspects; 3 v 3 then 1 v 1 | correct | Zhou ch. 2; sim: L1:l4 s6 (heavy_ok) |
| l4 | s1.hints, explain, byKey.* | 27, 9, 3, 1 in 3; two weighings have 9 outcomes < 27; halving gives 5 | correct | sim: L1:l4 s9 (27 needs 3); ceil(log2 27) = 5 |
| l4 | s2.hints, explain, byKey.* | Left sinks: 1..4 heavy or 5..8 light, 9..12 genuine: 8 cases; two weighings give 9 outcomes | correct | enumeration |
| l4 | s3.hints, explain, byKey.* | (1,2,5) v (3,6,9) splits the 8 cases 3, 2, 3, each finishable in one weighing | correct | sim: L1:l4 s3 |
| l4 | s4.o1..o2.why, explain | Halving uses two outcomes; thirds use all three; 9, 3, 1 in 2; log3 not log2 | correct | sim: L1:l4 s6 |
| l4 | s5.o1..o3.why, explain | With two coins and no genuine coin, 1 heavy and 2 light tip the same way; repeats add nothing | correct | sim: L1:l4 s5 |
| l4 | s6.prose, summary.ideas[0] | k weighings tell apart at most 3^k cases; split into thirds; with one heavy fake n coins are n cases | correct | information bound; sim: L1:l4 s6 (3^k exact for k = 1..5) |
| l4 | s6.explain, byKey.* | 81 needs 4; 3 gives 27; 7 is ceil(log2 81) | correct | arithmetic |
| l4 | s7.prose, lines, explain, d1.why | 13 coins, no genuine, say which: 26 < 27 yet impossible; tilt needs a <= 4, level needs a >= 5 | correct | Dyson (1946): (3^k-3)/2 without a reference coin; sim: L1:l4 s7 (search) |
| l4 | s8.hints, explain, byKey.* | 3^5 = 243 coins; 32 is 2^5; 15 is 3 x 5; 121 = (3^5-1)/2 for heavy-or-light with a genuine spare | correct | Dyson (1946); sim: L1:l4 summary note (k = 2..4), formula for k = 5 |
| l4 | s9.hints, explain, byKey.* | 50 needs 4; 17, 17, 16 then thirds; 6 is ceil(log2 50) | correct | sim: L1:l4 s9 |
| l4 | s10.hints, explain, byKey.* | 36 coins, 180 g genuine, 5 g extra names bag 5 | correct | sim: L1:l4 s10 |
| l4 | s11.prose | Bisecting a failing commit: k pass/fail tests separate 2^k commits | correct | binary search bound |
| l4 | s11.hints, explain, byKey.* | (3^k-3)/2: 12 for 3, 39 for 4; 40 fails without a genuine coin and works with one; 81 ignores the two cases per coin | correct | sim: L1:l4 s11 (search: 39 yes, 40 no, 40 + genuine yes) |
| l4 | summary.formula.note, ideas[2] | Heavy only n <= 3^k; heavy or light no genuine n <= (3^k-3)/2; 12 in 3, 39 in 4 | correct | Dyson (1946); sim: L1:l4 summary note |
| l4 | summary.trap | Halving wastes level: 9 coins take 2 not 3 | correct | sim: L1:l4 s6 |
| l4 | q0.o1..o2.why, explain, byKey.* | With a genuine coin weigh 5 v 4 + genuine: tilt leaves 9 cases, level 8; 13 can be done, 14 cannot | correct | sim: L1:l4 quiz 0 (search) |
| l4 | q1.explain, byKey.* | 10 coins need 3; 9 outcomes short of 10; 4 is halving | correct | sim: L1:l4 s9 |
| l4 | q2.o1..o2.why, explain | 13 v 13 or 10 v 10 leave more than 9 suspects on a tilt | correct | sim: L1:l4 quiz 2 |
| l5 | s0.hints, explain | Fill 5, pour, fill 5, pour: 2 left; nothing shorter than 4 | correct | sim: L1:l5 s0 (BFS 4) |
| l5 | s1.hints, explain, byKey.* | 6 litres with 4 and 9 in 8 steps; none in 6; four steps make 1 or 8 but not 6; 10 works | correct | sim: L1:l5 s1 (BFS 8; amounts within 4 steps) |
| l5 | s2.hints, explain, byKey.* | A lit at both ends goes out at 40; B then has 40 of burn left; a second flame halves it: 60; 80 ignores the second flame; 120 restarts B | correct | Zhou ch. 2 (burning ropes); two flames consume burn time at twice the rate |
| l5 | s3.lines, d1.why | Only an event triggers a step; cutting measures length not time | correct | derivation |
| l5 | s4.o1..o3.why, explain | Two flames use the 80 minutes of burn between them and meet after 40, wherever they meet; half the length is not half the time; no clock | correct | Zhou ch. 2 |
| l5 | s5.hints, explain, o1..o2.why | Fill, empty and pour keep multiples of gcd(6, 9) = 3; 4 never | correct | sim: L1:l5 s5 (reachable amounts 0, 3, 6, 9) |
| l5 | s6.prose, summary.ideas[1], formula | Jugs of a and b with a tap make exactly the multiples of gcd(a, b) up to max(a, b) | correct | Bezout plus the fill-pour cycle; sim: L1:l5 s6 formula (all a, b <= 12) |
| l5 | s6.o1.why, o4.why, explain | 6 and 15: 3, 6, 9, 12, 15 reachable; 4 and 10 never | correct | sim: L1:l5 s6 |
| l5 | s7.lines, hints, explain, d1.why | 5 and 9 glasses: turn the 5 at 5 and at 9; the 4 minutes of sand run back to 13; nothing marks 4 on the 9 | correct | sim: L1:l5 s7 (simulation) |
| l5 | s8.hints, explain, o0..o1.why, o5.why | With lighting only at the start or at an event, the marks are exactly 40, 60, 80, 120, 160; 100 would need an event at 80 after one at 40 | correct | sim: L1:l5 s8 (every event-driven plan enumerated) |
| l5 | s9.lines, hints, explain | 4 and 7 glasses mark 9: turn 4 at 4, 7 at 7, 7 again at 8 | correct | sim: L1:l5 s9 |
| l5 | s10.hints, explain | 10, 7, 3 with no tap: route via 3,7,0 and 9,1,0 reaches 5,5,0; states are splits of 10 | correct | sim: L1:l5 s11 (route is a shortest route) |
| l5 | s11.hints, explain, byKey.* | Fewest pours 9; none in 7; 10 into 3 first takes 10 at best | correct | sim: L1:l5 s11 (BFS) |
| l5 | summary.ideas[2], trap | Only an event is a clock; a second flame halves the burn left; cutting does not halve time | correct | Zhou ch. 2 |
| l5 | q0.explain, byKey.* | 3 and 7: 5 litres in 8 steps; four steps make 1 or 6 not 5; none in 6 | correct | sim: L1:l5 quiz 0 |
| l5 | q1.o1..o2.why, explain | gcd(4, 6) = 2, 3 is odd, never; half a jug cannot be judged | correct | sim: L1:l5 quiz 1 |
| l5 | q2.explain, byKey.* | Earliest event is a rope lit at both ends at 30; 15 would need a quarter | correct | sim: L1:l5 quiz 2 |
| review-1 | i0.o1..o2.why, explain | Turning k heads of 6 changes heads by 6-2k; 15 stays odd | correct | sim: L1:review-1 item 0 |
| review-1 | i1.o1..o2.why, explain | Centre of 7 x 7 is dark; 24 and 24 remain; a tiling exists (rings) | correct | sim: L1:review-1 item 1 (search) |
| review-1 | i2.explain, byKey.* | Worst case all ten left gloves; the eleventh matches | correct | sim: L1:review-1 item 2 (brute force over hands) |
| review-1 | i3.explain, byKey.* | 100 coins need 5; 34, 33, 33 | correct | sim: L1:l4 s9 |
| review-1 | i4.lines, d1.why, explain | 6 and 11 glasses mark 16; a full 6 at 11 ends at 17 | correct | sim: L1:review-1 item 4 |
| review-1 | i5.o*.why, explain | r rows and c columns light r(4-c)+c(4-r) = 4r+4c-2rc; counts 0, 4, 6, 8, 10, 12, 16; 128 patterns | correct | sim: L1:review-1 item 5 |
| review-1 | i6.o1..o2.why, explain | Seven T pieces give seven ±2 terms, never 0; turning over keeps 3 and 1 | correct | sim: L1:review-1 item 6 (search) |
| review-1 | i7.explain, byKey.* | Pairs (1,2)...(99,100) are 50 boxes; 51 force; the 50 odds show 50 can fail | correct | sim: L1:review-1 item 7 |
| review-1 | i8.explain, byKey.* | 55 coins, 550 g, 8 g short names bag 8 | correct | sim: L1:l4 s10 |
| homework-1 | i0.lines, d1.why, explain | Differences 1, 4, 5 are 1, 1, 2 mod 3; invariant; total proves nothing | correct | sim: L1:homework-1 item 0 |
| homework-1 | i1.explain, byKey.* | (i+j) mod 3 classes 17, 16, 16 force i+j = 2 mod 3; (i-j) mod 3 forces i-j = 0; nine squares i, j in {1, 4, 7}; each tiles | correct | sim: L1:homework-1 item 1 (search over all 49 removals) |
| homework-1 | i2.explain, byKey.* | Midpoints cut the side-2 triangle into four closed triangles of side 1 and diameter 1; five points force two in one; corners plus centre (2/sqrt 3 from each corner) show four can fail | correct | sim: L1:homework-1 item 2 |
| homework-1 | i3.o1.why, o3.why, explain | 12 yes; 13 no (first weighing); 13 + genuine yes; 14 + genuine no (28 > 27) | correct | sim: L1:l4 s7, quiz 0 |
| homework-1 | i4.lines, d1..d2.why, explain | 120-minute ropes: A both ends out at 60; B's last 60 take 30; 90 | correct | sim: L1:homework-1 item 4 |
| homework-1 | i5.explain, byKey.* | 5 and 11: 3 litres in 12 steps, none in 6 or 10 | correct | sim: L1:homework-1 item 5 (BFS 12) |
| homework-1 | i6.explain, byKey.* | 8 grey + 1 black + 1 white is 10 with no usable pair; 11 forces | correct | sim: L1:homework-1 item 6 |
| homework-1 | i7.model, rubric | 10 x 10 by 25 straight 1 x 4: colour (i+j) mod 4, counts 25, 26, 25, 24, each tile covers one of each, contradiction; chessboard balances 50/50 | correct | sim: L1:homework-1 item 7 model (counts) |

## Level 2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | s0.prose, canvas caption | Rules: senior proposes, at least half passes, proposer votes; preferences survive, coins, throw others; offered what he gets anyway a pirate votes no | correct | the standard pirate game (Stewart, *Sci. Am.* May 1999; Zhou ch. 2); the tie convention is stated |
| l6 | s0.hints, explain, byKey.* | 2 aboard C 60; 3 aboard (59, 0, 1) since D gets 0 under C; 4 aboard (59, 0, 1, 0) since C gets 0 under B | correct | sim: L2:l6 s0 (full backward induction) |
| l6 | s1.prose, explain, o1..o3.why | Price of a vote = coins after a failure + 1; prices 60 (B), 1 (C), 2 (D); two votes of four is half | correct | sim: L2:l6 s1 explain |
| l6 | s2.hints, explain, o1..o2.why | 1 lion eats, 2 wait, odd numbers eat; with 7, the eater leaves 6 awake who do not eat | correct | sim: L2:l6 s2 (recursion n = 1..29) |
| l6 | s3.o1..o3.why, explain | Equal split loses B (59 under his own split); A needs one vote; C costs 1 | correct | sim: L2:l6 s0 |
| l6 | s4.prose, hints, explain, o1..o2.why | Merciful pirates (yes when offered the fallback): every bought vote costs 0, so the proposer keeps 60 for every crew | correct | sim: L2:l6 s4 (n = 2..10; the number of zeros in the next game is at least the votes needed for every n) |
| l6 | s5.prose | Backward induction defined; price = coins after failure + 1; references to Zhou, Crack, Joshi | correct | Osborne ch. 5 (backward induction); Zhou ch. 2 |
| l6 | s5.explain, byKey.* | With 5 aboard, at least half of 5 is 3 votes, so buy 2 | correct | ceil(5/2) = 3 |
| l6 | s5.explain | Take-away games in Probability Puzzles; bargaining in Games, Auctions and Poker | correct | `puzzles/l19-who-wins.json`, `game-theory/l10-splitting-a-pie.json` |
| l6 | s6.prose, explain, o1..o3.why, summary formula | Proposer keeps 60 - floor((n-1)/2) for n = 2..10; needs ceil(n/2) - 1 = floor((n-1)/2) others; each costs 1 from those who get 0 next; 60 - (n-2) fails at n = 4; 60 - ceil(n/2) fails at n = 2 | correct | sim: L2:l6 s6 (full induction); the number of zeros in the (n-1) split is floor((n-1)/2), exactly the votes needed, so no tie among cheapest voters |
| l6 | s7.hints, explain, byKey.* | (58, 0, 1, 0, 1): pirates 3 and 5 get 0 under the 4-aboard split | correct | sim: L2:l6 s7 |
| l6 | s8.hints, explain, byKey.* | Six aboard: half is 3, buy 2: (58, 0, 1, 0, 1, 0) | correct | sim: L2:l6 s7 |
| l6 | s9.hints, explain, o1..o2.why | Ten lions: eating leaves 9, odd, so the first waits; hunger does not enter | correct | sim: L2:l6 s2 |
| l6 | s10.hints, explain, byKey.* | 40 coins, 3 pirates: (39, 0, 1); offered 0 the junior votes no | correct | sim: L2:l6 s10 |
| l6 | s11.prose, hints, explain, byKey.* | More than half: with 2 aboard C dies and D keeps 60; with 3, C dies if B fails so votes yes for 0: (60, 0, 0); with 4, A buys C and D at 1: (58, 0, 1, 1) | correct | sim: L2:l6 s11 (strict majority induction with survival first) |
| l6 | s11.prose | A committee vote: price each vote by what its holder gets if the motion fails | correct | same backward induction (Osborne ch. 5) |
| l6 | summary.ideas, trap | Smallest case first; vote price; redo the induction when a rule changes; equal split loses | correct | sim: L2:l6 |
| l6 | q0.explain, byKey.* | Seven pirates: 4 votes needed, buy 3, keep 57 | correct | sim: L2:l6 quiz 0 |
| l6 | q1.explain, o2..o3.why | Five pirates: C and E get 0 under B's (59, 0, 1, 0); D costs 2; B costs 60 | correct | sim: L2:l6 s7 |
| l6 | q2.explain, o1.why | Four lions: eating leaves 3 awake, odd, so no | correct | sim: L2:l6 s2 |
| l6 | q3.explain, byKey.one | Merciful D accepts 0 since C keeps 60 if B fails | correct | sim: L2:l6 quiz 3 |
| l7 | s0.prose, hints, explain, byKey.* | Code: back says blue iff even reds seen; each later person adds reds called behind to reds seen; calls B R B R R B B R; seven right, person 8 wrong | correct | sim: L2:l7 s0 (canvas hats R B B R R B R R) |
| l7 | s1.hints, explain, o1..o2.why | Person 4 knows 1 red in front and 2 red calls behind, total even, so red; he can tell | correct | parity arithmetic; sim: L2:l7 s0 |
| l7 | s2.prose, hints, explain, byKey.* | Three colours: back calls the sum mod 3 (5 mod 3 = 2); person 4: 2 - 0 = 2; person 3: 2 - 2 - 2 = 1 mod 3; sum modulo k plays the part of parity | correct | sim: L2:l7 s2 |
| l7 | s3.prose, hints, explain, byKey.* | Simultaneous code: person i assumes total = i mod 7; person 4 sees 20, guesses 5; true total 22 leaves 1, so person 1 alone right; the seven guesses cover all remainders | correct | sim: L2:l7 s3 (canvas hats 3 5 0 6 2 2 4) |
| l7 | s4.o1..o3.why, explain | Only person 8 guesses; the other 7 deduce; random calls average 4; person 8 cannot be sure | correct | sim: L2:l7 s4 (every pattern; back call wrong on half) |
| l7 | s5.explain, byKey.* | A line of one: chance 1/2; the code guarantees n - 1 = 0 | correct | derivation |
| l7 | s6.prose, formula, explain, o1..o2.why | With k colours the back announces the sum seen mod k; person i calls s - seen - heard mod k; n - 1 certain; simultaneous mod-7 code: exactly one right on every pattern | correct | sim: L2:l7 s6 (all 7^7 patterns), s4 (all patterns of the line code) |
| l7 | s7.hints, explain, byKey.* | Twenty in a line: 19 guaranteed; 10 is random calling | correct | sim: L2:l7 s4 (n = 20) |
| l7 | s8.hints, explain, byKey.* | Twelve people, three colours: 11; one call carries the sum mod 3; 4 is the random rate | correct | sim: L2:l7 s4 (n = 12, k = 3) |
| l7 | s9.hints, explain, byKey.* | Six in a line, hats B R R B R B: calls R R B R R B, five right, person 6 wrong | correct | sim: L2:l7 s9 |
| l7 | s10.prose, hints, explain, byKey.* | Three-player pass-or-guess: guess the opposite only when the two seen match; wins in 6 of 8 (loses RRR, BBB); 0.75 is the best possible | correct | Ebert (1998); sim: L2:l7 s10 (all 81^3 deterministic strategies: max 6 of 8) |
| l7 | s11.prose, hints, explain, byKey.* | Hamming-code strategy for seven loses only on its 16 codewords: 112/128 = 7/8 | correct | Hamming (1950) [7,4] code; sim: L2:l7 s11 (all 128 patterns) |
| l7 | s11.prose | The same codes guard data sent between trading systems | correct | Hamming SECDED codes in ECC memory and link-layer error correction (Hamming 1950); a general statement about hardware, not a claim about the puzzle |
| l7 | summary.ideas, formula, trap | One call carries the parity or sum; n - 1 certain; simultaneous: exactly one right; calls are not coin flips | correct | sim: L2:l7 |
| l7 | q0.explain, o1.why | Five reds is odd, so he calls red; his call carries parity | correct | code definition |
| l7 | q1.explain, byKey.* | 2 + 2 + 1 = 5 leaves 2 mod 3 | correct | arithmetic |
| l7 | q2.explain, byKey.* | 30 leaves 2 mod 7, so person 2 alone right | correct | sim: L2:l7 quiz 2 |
| l8 | s0.hints, explain, byKey.* | Follow box 1 to 2 to 4; cycle (1 2 4) of length 3; with 2 openings he fails; box 3 is a loop of length 1 | correct | inspection of the canvas permutation |
| l8 | s1.prose | Each prisoner succeeds exactly when his cycle has length at most the openings | correct | following the numbers walks the cycle through his box (Curtin and Warshauer 2006) |
| l8 | s1.prose | Opening 2 random boxes instead, the team wins with chance (1/2)^4 | correct | each prisoner's random choice hits with chance 2/4 independently of the others and of the order; sim: L2:l8 s1 prose |
| l8 | s1.hints, explain, byKey.* | Win iff every cycle has length 1 or 2: 1 + 6 + 3 = 10 of 24; losing orders 8 + 6 = 14 | correct | sim: L2:l8 s1 (all 24 orders) |
| l8 | s2.prose, hints, explain, byKey.* | Six open 3: fail iff a cycle of length 4, 5 or 6; such a cycle has chance 1/k for k > 3; two cannot fit; chances add: 37/60, success 23/60 | correct | sim: L2:l8 s2 (all 720 orders), s4 (1/k for k > n/2) |
| l8 | s3.o1..o3.why, explain | (1/2)^100 assumes independence; each prisoner's chance is still 1/2; the team fails iff a cycle exceeds 50, about 69%; a shared strategy correlates outcomes | correct | sim: L2:l8 s5, s6 |
| l8 | s4.lines, d1.why, explain | Orders with a k-cycle: C(n,k)(k-1)!(n-k)! = n!/k, chance 1/k; k > n/2 so at most one such cycle and nothing counted twice; a cycle has (k-1)! joins not k! | correct | Curtin and Warshauer (2006); sim: L2:l8 s4 (n = 6, 7, every k); the hypothesis k > n/2 is needed (k = 2, n = 6 gives not 1/2) |
| l8 | s5.prose, hints, explain, byKey.* | H100 = 5.1874, H50 = 4.4992; failure H100 - H50 = 0.6882; success 0.3118; 1 - ln 2 = 0.3069 is the limit | correct | sim: L2:l8 s5 |
| l8 | s6.hints, explain, o1..o3.why | The cycle through box 1 has each length 1..100 with chance 1/100; success iff length <= 50: exactly 1/2; only the joint chance changes | correct | sim: L2:l8 s6 (uniform cycle length, n = 6, 8) |
| l8 | s7.prose, explain, o1..o2.why | P(win) = 1 - (H_2m - H_m); the sum tends to the integral of 1/x from m to 2m = ln 2; the chance falls towards 1 - ln 2 and never below | correct | H_2m - H_m is increasing in m with limit ln 2; sim: L2:l8 s7 (m up to 299) |
| l8 | s8.hints, explain, byKey.* | Eight open 4: 1/5 + 1/6 + 1/7 + 1/8 = 533/840; success 307/840 | correct | sim: L2:l8 s8 (all 40,320 orders) |
| l8 | s9.hints, explain, byKey.* | Cycles (1 3 7), (2 5 8 6), (4): 3, 4, 1; all at most 4 so everyone succeeds | correct | sim: L2:l8 s9 |
| l8 | s10.hints, explain, byKey.* | Chance of a cycle longer than 50 is H100 - H50 = 0.6882; at most one; more likely than not | correct | sim: L2:l8 s5 |
| l8 | s11.hints, explain, o1..o3.why | Swapping the contents of two boxes in one cycle splits it; split L <= 100 into floor(L/2) and ceil(L/2), both <= 50; at most one long cycle, so one swap makes success certain; odd lengths work | correct | a transposition of two elements of a cycle splits it into cycles of the two arc lengths; sim: L2:l8 s11 (every order, n = 6, 8) |
| l8 | summary.ideas, formula, trap | Cycle-following; only one cycle can exceed half; P(win) = 1 - sum_{k > n/2} 1/k; 0.3118 for 100 | correct | sim: L2:l8 |
| l8 | q0.explain, byKey.fail | Ten open 5: 1627/2520 fail, 893/2520 win; the chance falls slowly as the team grows | correct | sim: L2:l8 quiz 0, s7 |
| l8 | q1.explain, byKey.* | 60 openings: H100 - H60 = 0.5075, success 0.4925 | correct | sim: L2:l8 quiz 1 |
| l8 | q2.explain, o1.why | Cycles share no box; two 4-cycles need 8 boxes; six boxes hold at most one cycle longer than 3; that is why the failure chances add | correct | cycles of a permutation partition the boxes |
| l9 | s0.prose | Model: an egg breaks from some floor upwards, every egg alike, the highest safe floor may be none or the top; one egg forces floor by floor | correct | standard two-egg problem (Zhou ch. 2) |
| l9 | s0.hints, explain, byKey.* | 10 floors, two eggs: 4 drops from floor 4 (break: 3 floors for one egg; survive: 6 floors in 3 drops); from 5 a break costs 5 | correct | sim: L2:l9 s0 (minimax search; first floor must be 4) |
| l9 | s1.hints, explain, byKey.* | Leaps 4, 3, 2, 1 reach 10; next floors 7, 9, 10 | correct | f(3,1) = 3 floors below the second drop; sim: L2:l9 s7 |
| l9 | s2.prose, hints, explain, byKey.* | d drops cover d(d+1)/2 floors; 13 cover 91, 14 cover 105, so 14; floors 14, 27, ..., 99, 100; 10 every ten floors has worst case 19; 7 is binary search | correct | sim: L2:l9 s2 (search 14; leaps list) |
| l9 | s3.o1..o3.why, explain | Binary search: break at 50 leaves 49 floors for one egg, worst 50; every ten: 10 + 9 = 19; shrinking leaps give 14 | correct | sim: L2:l9 s3 |
| l9 | s4.prose, hints, explain, byKey.* | f(d, e) = f(d-1, e-1) + f(d-1, e) + 1; f(8,3) = 92, f(9,2) = 45, f(9,3) = 129; 3 eggs and 100 floors need 9 | correct | sim: L2:l9 s4 (recurrence and search) |
| l9 | s5.lines, d1.why, explain | First drop from floor f(d-1, e-1) + 1; break and survive cases; the middle floor wastes drops since the floors below must fit e - 1 eggs | correct | derivation (the recurrence) |
| l9 | s6.hints, explain, byKey.* | One egg: no floor can be skipped; 100 drops; surviving 99 still needs floor 100; f(d, 1) = d | correct | sim: L2:l9 s6 |
| l9 | s7.prose, explain, byKey.* | f(d, e) = sum_{i=1}^{e} C(d, i); f(d, 2) = d(d+1)/2; fewest drops is the smallest d with f(d, e) >= floors; f(5, 4) = 30; f(4,3) + f(4,4) + 1 = 30 | correct | sim: L2:l9 s7 (identity against the recurrence and against the search for e <= 3, floors <= 120) |
| l9 | s8.hints, explain, byKey.* | 50 floors: 45 < 50 <= 55, so 10 | correct | sim: L2:l9 s8 |
| l9 | s9.hints, explain, byKey.* | 36 floors need 8 drops with no slack; a break at x leaves x - 1 floors for 7 drops so x <= 8; survival leaves 36 - x <= f(7, 2) = 28 so x >= 8 | correct | sim: L2:l9 s9 (first floor set is exactly {8}) |
| l9 | s10.hints, explain, byKey.* | f(d, 2) = f(d-1, 2) + d = 1 + ... + d = d(d+1)/2 = C(d,1) + C(d,2); d^2 fails at d = 2 | correct | derivation |
| l9 | s11.prose, hints, explain, byKey.* | f(14, 2) = 105; 1,000 floors need 45 with two eggs (990 < 1000 <= 1035) and 19 with three (987 < 1000 <= 1159) | correct | sim: L2:l9 s11 |
| l9 | s11.prose | A release manager bisecting a build with few test rigs faces the same count | correct | same minimax with a bounded number of destructive tests (analogy) |
| l9 | summary.ideas, formula, trap | Balance each drop; d(d+1)/2; recurrence; binary search worst case 50 | correct | sim: L2:l9 |
| l9 | q0.explain, byKey.* | 200 floors: 190 < 200 <= 210, so 20, first from 20 | correct | sim: L2:l9 quiz 0 |
| l9 | q1.explain, byKey.* | 21 floors: 6 drops exactly, leaps 6..1, no spare | correct | sim: L2:l9 quiz 1 |
| l9 | q2.explain, o1.why | With 14 drops and 105 floors of cover there is slack 5; first floor 10 works (9 floors and 13 drops; 90 floors and 13 drops which settle 91); any first floor 9 to 14 works | correct | sim: L2:l9 quiz 2 (first-floor set {9..14}) |
| l10 | s0.prose, hints, explain, byKey.* | Muddy children with a public 'at least one' and perfect reasoners: k muddy step forward in round k | correct | Fagin, Halpern, Moses, Vardi ch. 1; sim: L2:l10 s0 (possible-worlds model) |
| l10 | s1.hints, explain, o1..o2.why | If A were clean, B would see no mud and step forward in round 1; silence rules that world out | correct | sim: L2:l10 s0 (k = 2) |
| l10 | s2.prose, hints, explain, byKey.* | Seven blue-eyed islanders, public announcement, leave on night 7; without the visitor nobody leaves; each waits to see whether the six leave on night 6 | correct | sim: L2:l10 s2, quiz 1 |
| l10 | s3.hints, explain, o1..o2.why | Each 'I don't know' means the speaker wants one (a no-wanter answers no at once to 'everyone?'); the fourth, wanting one, says yes | correct | logic of the question "does everyone want a coffee" |
| l10 | s4.hints, explain, o1..o2.why | Everyone knew the fact but not that everyone knew that everyone knew (chain of six links); the announcement made it common knowledge and started the count | correct | Fagin et al. ch. 1 and 7; sim: L2:l10 quiz 1 (no announcement: never) |
| l10 | s5.explain, byKey.* | One blue-eyed islander leaves on night 1: base case | correct | sim: L2:l10 s5 |
| l10 | s6.prose, explain, byKey.* | Common knowledge defined; round = k; eight muddy: seven silent rounds; induction on k | correct | sim: L2:l10 s6 |
| l10 | s7.lines, d1.why, explain | Induction: base, hypothesis (round k and not before), step via the world where she is clean; the rule 'act in the round equal to the faces seen' acts a round early | correct | Fagin et al. ch. 1 |
| l10 | s8.hints, explain, byKey.* | Five muddy of nine: round 5; clean children never act | correct | sim: L2:l10 s8 |
| l10 | s9.hints, explain, byKey.* | 100 blue-eyed: night 100 | correct | same induction; sim: L2:l10 s9 (k = 12 in the model) |
| l10 | s10.hints, explain, o1..o2.why | After a 'No' the answer is settled: not everyone wants one | correct | one counterexample refutes 'everyone' |
| l10 | s11.prose, hints, explain, byKey.* | 'At least two': 2 muddy act in round 1; k muddy in round k - 1 | correct | sim: L2:l10 s11 |
| l10 | s11.prose | A widely expected rate cut still matters once announced: it becomes common knowledge among traders | correct | Aumann (1976) and Morris and Shin (2002) on public announcements as common knowledge; an analogy |
| l10 | summary.ideas, formula, trap | Nobody can act before round k; silence is news; announcement makes common knowledge; round = k - m + 1 after 'at least m' | correct | sim: L2:l10 s11, quiz 0 |
| l10 | q0.explain, byKey.* | 'At least three', four muddy: round 2 | correct | sim: L2:l10 quiz 0 |
| l10 | q1.explain, o1.why | With no announcement, two muddy children never step forward: silence proves nothing | correct | sim: L2:l10 quiz 1 |
| l10 | q2.explain, o1..o2.why | Sees five, night 5 silent, so six including her, all leave on night 6 | correct | sim: L2:l10 quiz 2 |
| l11 | s0.prose, hints, explain | Bridge rules; 1 and 3 cross, 1 back, 6 and 8 cross, 3 back, 1 and 3 cross: 18 | correct | Rote (2002); sim: L2:l11 s0 (Dijkstra over states) |
| l11 | s1.hints, explain, byKey.* | 1, 4, 5, 6: escort 17, shuttle 19; 17 is optimal | correct | sim: L2:l11 s1 |
| l11 | s2.hints, explain, byKey.* | Six sides, two places, 4 minutes: lower bound 12, schedule A1 B1 / A2 C1 / B2 C2 | correct | sim: L2:l11 s2 (schedule search) |
| l11 | s3.o1..o3.why, explain, byKey.* | Escorting 19; 6 and 8 first then 6 back costs 24; 17 impossible | correct | sim: L2:l11 s3, s0 |
| l11 | s4.prose | A plan has at least three trips over and two back; a search of every plan shows more trips cost more | correct | 4 people, 2 per trip, torch returns; sim: L2:l11 s4 (5 trips 18, 7 and 9 trips more) |
| l11 | s4.lines[0..2], explain | With 3 over and 2 back each trip over carries two; case 1 (6 and 8 apart): at least 8 + 6 + 3 + 1 + 1 = 19 | correct | over carries 6 people in 3 trips, back 2 in 2; the third trip over costs at least 3 |
| l11 | s4.lines[3..5] | Case 2: 6 and 8 cross together costing 8 "and neither walks back"; the other trips over are 1 and 3 at 3 each; returns 1 + 3; at least 18 | imprecise | "neither walks back" is asserted, not derived: a return by 6 or 8 costs at least 6, giving at least 8 + 6 + 3 + 3 + 1 = 21 > 18 (the homework-2 item 7 model says exactly this). As ordered, the proof has a gap a reader would carry away |
| l11 | s4.d1.why | Escorting is one plan, not a bound | correct | derivation |
| l11 | s5.explain, byKey.* | Two people cross together once at the slower pace: 8; nobody returns | correct | sim: L2:l11 s5 |
| l11 | s6.prose | "escort costs z + a + y + a; shuttle costs b + a + z + b" | imprecise | both omit the final crossing of a and b (cost b), common to both patterns: escort is z + 2a + y + b and shuttle z + a + 3b. The comparison 2b < a + y is right (the shared b cancels), but the stated "costs" are not the plan costs: for 1, 3, 4, 9 they give 15 and 16, not the 18 and 19 the same screen's explain states |
| l11 | s6.prose, formula, summary.ideas[1] | Shuttle iff 2b < a + y; 1, 3, 6, 8 shuttle (6 < 7); 1, 4, 5, 6 escort (8 > 6); the cheaper of the two patterns is optimal for four | correct | Rote (2002) Thm for n = 4; sim: L2:l11 s6 (every a <= b <= y <= z <= 12 against the search) |
| l11 | s6.explain, o1..o2.why, byKey.* | 1, 3, 4, 9: escort 9 + 1 + 4 + 1 + 3 = 18, shuttle 19 | correct | sim: L2:l11 s6 |
| l11 | s7.hints, explain, byKey.* | 2, 3, 8, 9: 6 < 10 so shuttle, 20; escort 24 | correct | sim: L2:l11 s7 |
| l11 | s8.hints, explain, byKey.* | 1, 5, 6, 7: 10 > 7 so escort, 20; shuttle 23 | correct | sim: L2:l11 s8 |
| l11 | s9.prose, hints, explain, byKey.* | Three auditors and three traders, boat for two, traders never outnumber auditors on a bank with an auditor: 11 crossings, none in 9; 5 moves too few people; 13 works | correct | missionaries and cannibals (Amarel 1968); sim: L2:l11 s9 (BFS 11); a 13-crossing walk is the 11-route with one trader crossing and returning first |
| l11 | s10.hints, explain, byKey.* | Ten sides, two places, 3 minutes: 15 with no empty place | correct | sim: L2:l11 s10 |
| l11 | s11.prose, hints, explain, byKey.* | 1, 3, 6, 8, 12: shuttle 8 and 12 for 19, then 1, 3, 6 for 10: 29; escort all 32; 3 escorting costs 31 | correct | Rote (2002) greedy for n >= 4; sim: L2:l11 s11 (search 29) |
| l11 | s11.prose | Trade allocation across a few channels is scheduled the same way | correct | scheduling with a shared resource (analogy) |
| l11 | summary.ideas, formula, trap | Escort or shuttle; shuttle iff 2b < a + y; case split proof; escorting gives 19 | correct | sim: L2:l11 |
| l11 | q0.explain, byKey.escort | 1, 2, 7, 8: 4 < 8 so shuttle: 15; escort 19 | correct | sim: L2:l11 quiz 0 |
| l11 | q1.explain, byKey.* | Eight sides, three places: ceil(8/3) = 3 slots of 5 = 15, with the schedule given | correct | sim: L2:l11 quiz 1 |
| l11 | q2.explain, o1..o2.why | The 3 returns so that 6 and 8 share a trip; net saving 1 minute (saves 6, adds 3 + 2) | correct | 19 - 18 = 1; derivation |
| review-2 | i0.explain, byKey.* | 100 coins, 4 pirates: (99, 0, 1) then 99 | correct | sim: L2:review-2 item 0 |
| review-2 | i1.explain, byKey.* | Ten people, three colours: 9 guaranteed; the back person has no information; random guesses guarantee nobody | correct | sim: L2:l7 s4 (n = 10, k = 3) |
| review-2 | i2.explain, byKey.* | Twelve open 6: fail 1/7 + ... + 1/12 = 0.6532, win 9613/27720 = 0.3468; at most one such cycle | correct | sim: L2:review-2 item 2 |
| review-2 | i3.explain, byKey.* | 80 floors: 78 < 80 <= 91, so 13, first from 13; 9 (sqrt 80) is the every-k idea | correct | sim: L2:l9 quiz 0 (80 floors 13) |
| review-2 | i4.explain, byKey.* | Four muddy of six, 'at least one': round 4 | correct | sim: L2:l10 s8 |
| review-2 | i5.explain, byKey.* | 1, 2, 4, 9: 4 < 5 so shuttle 16; escort 17 | correct | sim: L2:l11 quiz 0 |
| review-2 | i6.explain, o1..o2.why | Twelve lions: eating leaves 11, odd, so no; n odd eats | correct | sim: L2:l6 s2 |
| review-2 | i7.explain, byKey.* | Hats R R B B B R: calls B B B B R R; five right | correct | sim: L2:review-2 item 7 |
| review-2 | i8.explain, byKey.* | Prisoner 1's cycle length uniform on 1..10; 5/10 = 0.5 | correct | sim: L2:l8 s6 |
| review-2 | i9.explain, o1..o2.why | Two 'I don't know' mean yes; the third wants none, so no | correct | logic of 'everyone' |
| homework-2 | i0.lines, d1..d2.why, explain | 2 aboard C 100; 3 aboard (99, 0, 1); 4 aboard A buys C: (99, 0, 1, 0); C's vote would cost 101; D's price 2 | correct | sim: L2:review-2 item 0 |
| homework-2 | i1.prose, solution, tests, explain | min_drops grows d until sum C(d, i) >= floors; tests (1,10)=10, (2,0)=0, (2,1)=1, (2,36)=8, (2,100)=14, (3,100)=9, (2,1000)=45, (3,1000)=19; binary-search starter fails; a full search agrees up to 100 floors | correct | sim: L2:homework-2 item 1 (solution passes, starter fails; search agreement for floors <= 120) |
| homework-2 | i2.explain, byKey.* | Person 3 sees 7, needs 7 + g = 3 mod 5, g = 1; right only if the total leaves 3 | correct | sim: L2:homework-2 item 2 |
| homework-2 | i3.lines, d1..d2.why, explain | Fail iff a cycle longer than n/2; at most one; n!/k orders; chance 1/k, disjoint; P(win) = 1 - sum_{k > n/2} 1/k; independence fails; rotations are one cycle | correct | sim: L2:l8 s4 |
| homework-2 | i4.explain, byKey.* | 300 = 24 x 25/2 exactly, 276 short, so 24 with no slack, first from 24 | correct | sim: L2:homework-2 item 4 |
| homework-2 | i5.explain, o1..o3.why | Merciful five pirates: (60, 0, 0, 0, 0); (58, 0, 1, 0, 1) is the bloodthirsty split | correct | sim: L2:l6 s4 |
| homework-2 | i6.explain, byKey.* | 1, 2, 5, 8, 10: shuttle 8 and 10 for 15, then 1, 2, 5 for 8: 23; escort all 28; 2 escorting costs 24; 17 omits the 8 | correct | sim: L2:l11 s11 (search 23) |
| homework-2 | i7.model, rubric | Trip count; case apart 19; case together with the first-or-last sub-case (6 or 8 returns, at least 21) so middle trip, 18; both exceed 17; plan 18 | correct | sim: L2:l11 s4; the model closes the gap left in l11 s4 |

## Level 3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l12 | s0.hints, explain, byKey.* | Minute hand 6 degrees a minute, hour hand 0.5; at 3:40 they are at 240 and 110, 130 apart; 230 is the long way round; the angle between the hands is the smaller one | correct | sim: L3:l12 s0 |
| l12 | s1.prose, hints, explain, byKey.* | At 3:00 the gap is 90; it closes at 6 - 0.5 = 5.5 a minute (same direction, so the difference); 90/5.5 = 180/11; the hands meet every 720/11 minutes, 11 times in 12 hours | correct | sim: L3:l12 s1 (direct count of coincidences) |
| l12 | s2.hints, explain, byKey.* | Gap of 6 km closes at 90 - 72 = 18 km/h: 20 minutes; adding speeds is for approach; ride with the slower mover | correct | relative velocity (Galilean frame); sim: L3:l12 s2 |
| l12 | s3.hints, explain, o1..o2.why | 2 h out, 3 h back, 240 km in 5 h = 48; the plain mean 50 overweights the fast leg; an average lies between the speeds | correct | sim: L3:l12 s3 |
| l12 | s4.hints, explain, o1..o2.why | Averaging 80 over 40 km allows 30 minutes, all spent on the way out; no return speed works; at 160 the average is 64 | correct | sim: L3:l12 s4 |
| l12 | s5.prose, summary formula | theta = \|30h - 5.5m\|, then 360 - theta if above 180; two movers close at the relative speed; equal distances average to the harmonic mean 2ab/(a+b) | correct | hour hand at 30h + 0.5m, minute hand at 6m; sim: L3:l12 s5 (every minute of 12 hours) |
| l12 | s5.explain, byKey.raw | At 12:00 the formula gives 360, which the rule turns into 0 | correct | sim: L3:l12 s5 |
| l12 | s6.lines, d1.why, explain | 2d over d/a + d/b = 2ab/(a+b); legs equal in distance not time | correct | derivation |
| l12 | s7..s8, quiz 2; l16 quiz 2; review-3 item 0 | 9:15 gives 172.5 (187.5 the long way); 2:20 gives 50; 6:30 gives 15; 4:50 gives 155; 10:10 gives 115 | correct | sim: L3:l12 s5 |
| l12 | s7.explain | The hour hand is never exactly on its number except on the hour | correct | hour hand at 30h + 0.5m is on a numeral iff m = 0 |
| l12 | s9.hints, explain, byKey.* | In 12 hours the minute hand gains 5.5 x 720 = 3960 degrees = 11 laps; each lap passes 90 and 270 once: 22 right angles; 44 in a day | correct | sim: L3:l12 s9 (direct count) |
| l12 | s10.hints, explain, byKey.* | Rates add: 1/4 + 1/12 = 1/3 of the tank an hour, so 3 hours; times do not add or average | correct | sim: L3:l12 s10 |
| l12 | s11.hints, explain, byKey.* | In 24 hours the minute hand gains 22 laps; each lap passes 180 once: 22; 11 in 12 hours; 44 counts right angles | correct | sim: L3:l12 s11 |
| l12 | s11.prose | A desk counts recurring events by laps of the relative motion | correct | analogy to the same counting |
| l12 | summary.ideas, trap | Rate times time; close at the difference or the sum; harmonic mean below the plain mean | correct | AM-HM inequality; sim: L3:l12 |
| l12 | q0.explain, byKey.mean | Equal pounds at two prices average to the harmonic mean: 48 | correct | sim: L3:l12 quiz 0 |
| l12 | q1.explain, byKey.* | Speeds in the same frame add: 2.5 m/s, 24 s | correct | sim: L3:l12 s10 |
| l12 | q3.explain, byKey.* | Rates add with a sign: 1/6 - 1/9 = 1/18, so 18 hours | correct | sim: L3:l12 s10 |
| l13 | s0.hints, explain | Last digit of a product depends only on last digits; powers of 7 end 7, 9, 3, 1 with cycle 4 | correct | multiplication mod 10 is well defined; sim: L3:l13 s0 |
| l13 | s1.hints, explain, byKey.* | Only the power mod 4 matters; 2026 = 4 x 506 + 2, so 7^2026 ends like 7^2: 9 | correct | sim: L3:l13 s0 |
| l13 | s2.prose, hints, explain, byKey.* | Digit sum 45 so 9 divides 123456789; alternating sum from the right 5 is the remainder mod 11; 10 is 1 mod 9 and -1 mod 11 | correct | Hardy and Wright ch. 9 (divisibility tests); sim: L3:l13 s2 |
| l13 | s3.prose, explain | A trailing zero needs a 2 and a 5; even numbers supply more 2s than 5s; twelve multiples of 5 up to 60 | correct | sim: L3:l13 s3 (Legendre counts, n < 500) |
| l13 | s4.hints, explain, o1..o2.why | 25 and 50 hold two 5s each: 14 zeros; count factors not multiples; a 5 pairs with a spare 2 | correct | sim: L3:l13 s4 (from 60! itself) |
| l13 | s5.prose, explain, summary formula | Z(n) = floor(n/5) + floor(n/25) + floor(n/125) + ...; Z(30) = 7 | correct | Legendre's formula (Hardy and Wright ch. 22); sim: L3:l13 s5 |
| l13 | s5.prose | Contest Practice lesson 5 (modulo) kept big numbers small | correct | `contests/l5-modulo.json` |
| l13 | s6.lines, d1.why, explain | Place value, 10 = -1 mod 11, 10^k = (-1)^k, alternating sum; 10 = 1 holds mod 9 not 11; a divisibility test is a remainder of 10 in disguise | correct | derivation; sim: L3:l13 s2 |
| l13 | s7.hints, explain, byKey.* | Powers of 3 end 3, 9, 7, 1; 2027 = 4 x 506 + 3, so 7 | correct | sim: L3:l13 s7 |
| l13 | s8.hints, explain, byKey.* | 125!: 25 + 5 + 1 = 31 | correct | sim: L3:l13 s8 |
| l13 | s9.hints, explain, byKey.* | Repunit remainders mod 7 run 1, 4, 6, 5, 2, 0 (each step 10r + 1); 111111 = 7 x 15873; one must exist since remainders repeat | correct | sim: L3:l13 s9; pigeonhole on remainders with gcd(10, 7) = 1 |
| l13 | s10.hints, explain, byKey.* | 2^10 ends 24, 2^20 = (2^10)^2 ends like 24^2 = 576: 76; square the remainder | correct | sim: L3:l13 s10 |
| l13 | s10.prose | Contest Practice lesson 5 built a checksum of trade ids this way | correct | `contests/l5-modulo.json` "A checksum of trade IDs" |
| l13 | s11.hints, explain, byKey.* | Binary trailing zeros of 60! = factors of 2 = 30 + 15 + 7 + 3 + 1 = 56; the layered count works for any prime base | correct | Legendre; sim: L3:l13 s11 |
| l13 | summary.ideas, trap | Last digits mod 10 by cycle; 9 digit sum, 11 alternating sum; trailing zeros count 5s; 60! has 14 | correct | sim: L3:l13 |
| l13 | q0.explain, o4..o5.why | d^2 ending in d for 0, 1, 5, 6 only; 4 and 9 alternate | correct | sim: L3:l13 quiz 0 |
| l13 | q1.explain, byKey.* | 2^3 = 1 mod 7; 100 = 3 x 33 + 1; 2^100 leaves 2 | correct | sim: L3:l13 quiz 1 |
| l13 | q2.explain, byKey.* | From 5! every factorial ends in 0; 1 + 2 + 6 + 24 = 33: last digit 3 | correct | sim: L3:l13 quiz 2 |
| l14 | s0.hints, explain, byKey.* | Pairs from the ends add to 21; 7 pairs with 14; ten pairs: 210 | correct | sim: L3:l14 s0 |
| l14 | s1.prose, hints, explain, byKey.* | Series lesson 6 paired 1 to 100; 1 to 200 makes 100 pairs of 201: 20,100 | correct | `series/l6-gauss.json`; sim: L3:l14 s1 |
| l14 | s2.hints, explain, byKey.* | Running totals n/(n+1); 49 terms give 49/50; 50 terms give 50/51; 1 is the infinite sum | correct | sim: L3:l14 s2 |
| l14 | s3.lines, d1.why, explain | 1/k - 1/(k+1) = 1/(k(k+1)); neighbours cancel; 1 - 1/50 survives; a sum of products is not a product of sums | correct | Graham, Knuth, Patashnik ch. 2 (telescoping) |
| l14 | s4.hints, explain, byKey.* | Each match removes one player; 49 of 50 must go: 49 matches, byes or not | correct | sim: L3:l14 s4 (simulated with byes, n < 200) |
| l14 | s5.hints, explain, o1..o2.why | 12 x 11 counts each handshake twice: 66; 144 includes self-handshakes | correct | sim: L3:l14 s5 |
| l14 | s6.options, explain | 1 player 0 matches; one term gives 1/2; 2 players 1 match; 2 people 1 handshake | correct | formulas at n = 1, 2 |
| l14 | s7.prose, hints, explain, byKey.* | n(n+1)/2; telescoping; counting twice; a decagon has 10 x 7 / 2 = 35 diagonals; 45 includes the sides | correct | sim: L3:l14 s7 |
| l14 | s8.hints, explain, byKey.* | 75 pairs of 151: 11,325 | correct | sim: L3:l14 s8 |
| l14 | s9.hints, explain, byKey.* | 1/2 - 1/10 = 0.4 | correct | sim: L3:l14 s9 |
| l14 | s10.hints, explain, byKey.* | A k x k square fits (9 - k)^2 ways; 64 + ... + 1 = 204 | correct | sim: L3:l14 s10 |
| l14 | s11.prose, hints, explain, byKey.* | A rectangle is fixed by two of 9 vertical and two of 9 horizontal lines: 36^2 = 1296; 50 stocks have C(50,2) = 1225 pairs | correct | sim: L3:l14 s11 (counted as pairs of lines) |
| l14 | summary.ideas, formula, trap | Pairing, telescoping, counting two ways; sum 1/(k(k+1)) = n/(n+1) | correct | sim: L3:l14 |
| l14 | q0.explain, byKey.* | Pair n with 999 - n including 0: digits sum to 27 with no carry, 500 pairs: 13,500 | correct | each column of n and 999 - n adds to 9; sim: L3:l14 quiz 0 (direct sum) |
| l14 | q1.explain, byKey.* | 100 odd numbers, 50 pairs of 200: 10,000 = 100^2; the first n odd numbers sum to n^2 | correct | sim: L3:l14 quiz 1 |
| l14 | q2.explain, byKey.* | 50 pairs of -1: -50 | correct | sim: L3:l14 quiz 2 |
| l15 | s0.hints, explain, byKey.* | 2^19 = 524,288, 2^20 = 1,048,576; ten doublings are about a thousandfold | correct | sim: L3:l15 s0 |
| l15 | s1.prose, hints, explain, byKey.* | 2^10 = 1024 adds 2.4% per ten doublings, compounding to 7.4% at 2^30 = 1.074 x 10^9; 2^32 = 4.29 billion, the count of 32-bit values | correct | sim: L3:l15 s1 |
| l15 | s2.prose | Mental Arithmetic Drills lesson 8 squared numbers; Mental Maths Under Pressure lesson 8 drills roots | correct | `mental/l8-squaring.json`, `mental-pressure/l8-square-roots.json` |
| l15 | s2.hints, explain, byKey.* | 1.41^2 = 1.9881 and 1.42^2 = 2.0164 bracket 2; 1.415^2 = 2.0022 > 2 so round down; bracket then test the midpoint | correct | sim: L3:l15 s2 |
| l15 | s3.prose | Money at r% a year (yearly compounding) doubles in ln 2 / ln(1 + r/100) years; Exponentials and Logarithms lesson 12 met the rule of 72 | correct | (1 + r)^T = 2; `exp-log/l12-doubling-time.json` |
| l15 | s3.hints, explain, o1..o2.why | At 8% the exact time is 9.006 and r T = 72.05; 72/8 = 9 is off by 0.006 and 69.3/8 = 8.66 by 0.34; at 6% 11.90 against 12; 69.3 is right only as the rate falls to 0; the right numerator rises with the rate | correct | sim: L3:l15 s3 (r T increasing on (0, 1]) |
| l15 | s4.prose, hints, explain, byKey.* | At 36%: ln 2 / ln 1.36 = 0.6931/0.3075 = 2.254 against the rule's 2; the right numerator is 81; 69.3/36 = 1.93 is further off | correct | sim: L3:l15 s4 |
| l15 | s5.prose table | sqrt 2 1.414, sqrt 3 1.732, e 2.718, 1/e 0.368, ln 2 0.693, ln 10 2.303, pi^2 9.870, 2^10 1024; doubling ln 2 / ln(1 + r) about 69.3/r; 72 corrects for ordinary rates and divides easily | correct | sim: L3:l15 s5 |
| l15 | s5.explain, byKey.* | ln 5 = ln 10 - ln 2 = 1.610; adding gives ln 20; dividing logs is not ln of a quotient | correct | log laws; sim: L3:l15 s5 |
| l15 | s6.lines, d1.why, explain | (1 + r)^T = 2; T ln(1 + r) = ln 2; ln(1 + r) = r for small r; T = 69.3/r%; simple interest 1 + rT gives 12.5 years at 8%; the -r^2/2 term makes ln(1 + r) smaller so the true numerator is bigger | correct | Taylor series of ln(1 + r); sim: L3:l15 s6 |
| l15 | s7.hints, explain, byKey.* | (3 + 0.1416)^2 = 9 + 0.8496 + 0.0201 = 9.8696; 6.28 is 2 pi, 9.42 is 3 pi | correct | sim: L3:l15 s7 |
| l15 | s8.hints, explain, byKey.* | 72/9 = 8; exact 8.04; 69.3/9 = 7.7; 100/9 is simple interest; near 8% the rule is good to a few hundredths | correct | sim: L3:l15 s8 |
| l15 | s9.hints, explain, byKey.* | 100 ln 1.01 = 0.995; 1.01^100 = e^0.995 = 2.705, below e; (1 + x)^n is about e^{nx} for small x | correct | sim: L3:l15 s9 |
| l15 | s10.hints, explain, byKey.* | Quadrupling is two doublings: 18; exact ln 4 / ln 1.08 = 18.01 | correct | sim: L3:l15 s10 |
| l15 | s10.prose | A desk sanity-checks projected fund growth this way | correct | the rule of 72 as a mental check (analogy) |
| l15 | s11.hints, explain, byKey.* | Tenfold is log2 10 = 3.32 doublings; 3.32 x 9 = 29.9; exact ln 10 / ln 1.08 = 29.92 | correct | sim: L3:l15 s11 |
| l15 | summary.ideas, formula, trap | Table of constants; logs turn products into sums; T = ln 2 / ln(1 + r) about 72/r%; at 36% the exact time is 2.25 | correct | sim: L3:l15 |
| l15 | q0.explain, o1..o2.why | Compare logs: pi = 3.1416 against e ln pi = 3.1117, so e^pi (23.14) beats pi^e (22.46) | correct | sim: L3:l15 quiz 0 |
| l15 | q1.explain, byKey.rule | ln 2 / ln 1.72 = 1.278 against the rule's 1; at large rates the rule is badly short | correct | sim: L3:l15 quiz 1 |
| l15 | q2.explain, byKey.* | ln 0.99 = -0.01005; 0.99^100 = e^{-1.005} = 0.366, a little below 1/e; losing 1% a hundred times is not losing 100% | correct | sim: L3:l15 quiz 2 |
| l15 | q3.explain, byKey.* | 10 ln 2 is about 3 ln 10, so ln 2 is about 0.3 x 2.303 = 0.691; 0.30 is log10 2 | correct | sim: L3:l15 quiz 3 |
| l15 | q4.explain, byKey.* | 2^16 = 256^2 = 65,536; doubling the power squares the number | correct | sim: L3:l15 s0 |
| l16 | s0.hints, explain, byKey.* | Five colours: five socks can all differ, the sixth repeats; ten guarantees two pairs | correct | pigeonhole; sim: L3:l16 s0 |
| l16 | s1.hints, explain, o1..o2.why | Turning four changes heads by 4, 2, 0, -2, -4: parity invariant; 13 odd never reaches 0 | correct | sim: L3:l16 s1 (BFS) |
| l16 | s2.options, explain | A weighing has three outcomes so split into thirds; halving uses two; colouring proves impossibility; backward induction suits games with turns | correct | method taxonomy consistent with l2, l4, l6 |
| l16 | s3.hints, explain, byKey.* | 27 < 30 <= 81 so 4 weighings; 10, 10, 10 then 4, 3, 3 works; 5 comes from halving | correct | sim: L3:l16 s3 (search) |
| l16 | s4.hints, explain, o1..o2.why | 7 x 7 has 25 dark (corners) and 24 light; the square next to a corner is light; 25 against 23 so no tiling; order of placing does not matter | correct | sim: L3:l16 s4 (count and search) |
| l16 | s5.options, explain | Pirates: each vote compares the offer with the next round, so backward induction | correct | Osborne ch. 5 |
| l16 | s6.hints, explain, byKey.* | Three pirates, 50 coins: B keeps 50 with two left, C gets 0, so A offers (49, 0, 1); A's own vote is one of three, less than half | correct | sim: L3:l16 s6 |
| l16 | s7.hints, explain, byKey.* | Fifteen in a line: parity call makes 14 certain; the back person cannot be promised; pairing wastes calls | correct | sim: L2:l7 s4 (the modulo code for every n) |
| l16 | s8.hints, explain, byKey.* | 1, 2, 6, 9: shuttle 2 + 1 + 9 + 2 + 2 = 16; escort 19 | correct | sim: L3:l16 s8 (search) |
| l16 | s9.hints, explain, o1..o2.why | 30 and 60 km/h over equal distances average 40 (harmonic mean), not 45; an average cannot exceed the faster speed | correct | sim: L3:l12 s3 |
| l16 | s10.options, explain | Arrival needs distance over speed and no speed is given, so ask; an assumed speed is a guess | correct | the item's own premise (missing-information family) |
| l16 | s11.hints, explain, byKey.* | Shuttle 9 and 12: 2 + 1 + 12 + 2 = 17, then 1, 2, 6 take 6 + 1 + 2 = 9: 26; escorting everyone 32; pairing 6 with 9 is worse | correct | sim: L3:l16 s8 (search 26) |
| l16 | summary.ideas, formula, trap | Name the family first; 3^w >= n for one light coin; harmonic mean | correct | sim: L3:l16 |
| l16 | q0.explain, byKey.* | Twenty prisoners fail iff a cycle longer than 10, chance 1/11 + ... + 1/20 = 0.6688; success 0.3312; 1 - ln 2 is the limit | correct | sim: L3:l16 quiz 0; L2:l8 s4 |
| l16 | q1.explain, byKey.* | t drops cover t(t+1)/2 floors; 15 x 16/2 = 120; 14 covers 105 | correct | sim: L3:l16 quiz 1 (minimax search) |
| l16 | q3.explain, byKey.one | Powers of 9 alternate 9, 1; 2027 odd so 9 | correct | sim: L3:l13 s7 |
| l16 | q4.explain, byKey.* | 80!: 16 + 3 = 19; 25, 50, 75 bring a second 5 | correct | sim: L3:l13 s4 |
| review-3 | i0.explain, byKey.* | 10:10: 245 the long way, 115 | correct | sim: L3:l12 s5 |
| review-3 | i1.explain, byKey.* | 13^47 ends like 3^47; 47 = 4 x 11 + 3: 7 | correct | sim: L3:l13 s7 |
| review-3 | i2.explain, byKey.* | 150 pairs of 301: 45,150 | correct | sim: L3:l14 s0 |
| review-3 | i3.explain, byKey.* | 72/4 = 18; exact 17.67; 69.3/4 = 17.3; 100/4 is simple interest | correct | sim: L3:l15 s8 |
| review-3 | i4.explain, byKey.* | 45 and 90 over equal distances: 60 | correct | sim: L3:l12 s3 |
| review-3 | i5.explain, byKey.* | 200!: 40 + 8 + 1 = 49 | correct | sim: L3:l13 s4 |
| review-3 | i6.explain, byKey.* | 1/3 - 1/12 = 1/4 | correct | sim: L3:l14 s2 |
| review-3 | i7.explain, o1..o2.why | 2^100 = 1.024^10 x 10^30 = 1.27 x 10^30, larger; the 2.4% excess grows to 27% | correct | sim: L3:l15 s1 |
| review-3 | i8.explain, byKey.* | 20 x 19 ends, halve: 190; 400 includes self-handshakes | correct | sim: L3:l14 s5 |
| review-3 | i9.explain, byKey.* | 5 and 7 jugs: 1 litre in 8 steps starting with the 5; starting with the 7 takes 10 at best; none in 6 | correct | sim: L3:review-3 item 9 (BFS) |
| homework-3 | i0.lines, d1.why, explain | Cycle 7, 9, 3, 1 of length 4; 2026 leaves 2; digit 9; no power of 7 ends in 0 | correct | sim: L3:l13 s0 |
| homework-3 | i1.lines, d1.why, explain | Telescoping derivation of S_n = n/(n+1) with the n = 1 and 49 checks; (n-1)/n fails at n = 1 | correct | sim: L3:l14 s2 |
| homework-3 | i2.explain, byKey.* | Gap 210 closes to 180 at 5.5 a minute: 60/11 = 5.45; the hands meet at 38.18 | correct | sim: L3:homework-3 item 2 |
| homework-3 | i3.explain, byKey.* | 3^6 = 1 mod 7; 100 = 6 x 16 + 4; 3^4 = 81 leaves 4 | correct | Fermat (Hardy and Wright ch. 6); sim: L3:l13 quiz 1 |
| homework-3 | i4.explain, byKey.* | 5 x 5 board: C(6,2)^2 = 225 rectangles; 55 squares | correct | sim: L3:l14 s10 |
| homework-3 | i5.explain, byKey.down | 2.235^2 = 4.9952 < 5 so sqrt 5 rounds up to 2.24; the midpoint, not the nearer square, decides | correct | sim: L3:l15 s2 |
| homework-3 | i6.explain, byKey.* | Eightfold is three doublings of 72/9 = 8: 24; exact ln 8 / ln 1.09 = 24.13; 77.8 is simple interest | correct | sim: L3:l15 s10 |
| homework-3 | i7.model, rubric | T = ln 2 / ln(1 + r); ln(1 + r) = r - r^2/2 (0.06755 against 0.06766 at 7%); T = 10.24 against 72/7 = 10.29 and 69.3/7 = 9.90; numerator 69.3(1 + r/2) = 72.07 at 8%; 72 divides by 2, 3, 4, 6, 8, 9, 12, 18; at 36% the truth is 2.25; continuous compounding numerator 69.3 | correct | sim: L3:homework-3 model |

## Verdict counts

Rows: 368 (level 1: 128; level 2: 131; level 3: 109). Verdicts: correct 364, imprecise 4 (l1 s7 and summary monovariant; l2 s11 cube coordinate convention; l11 s4 "neither walks back"; l11 s6 escort and shuttle costs), wrong 0, misleading 0, unverified 0.

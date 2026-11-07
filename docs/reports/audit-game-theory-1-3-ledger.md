# Claim ledger: game-theory L1 to L3 (blind concept audit)

Written incrementally, one file at a time. Verdicts: correct, wrong, imprecise, misleading, unverified. Basis: a named source with section, a short derivation, or `sim: <script>:<check>`. Sources abbreviated: Osb = Osborne, *An Introduction to Game Theory* (2004); FT = Fudenberg and Tirole, *Game Theory* (1991); Kr = Krishna, *Auction Theory* (2nd ed., 2010); My = Myerson, *Game Theory: Analysis of Conflict* (1991); CA = Chen and Ankenman, *The Mathematics of Poker* (2006); OR = Osborne and Rubinstein, *A Course in Game Theory* (1994); Kelly (1956); Rubinstein (1982).

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-payoff-tables.json | screens[0].prose | Convention: cell reads (row player's payoff, column player's payoff) | correct | Osb 2.2 (Figure 2.1 convention) |
| l1-payoff-tables.json | screens[0].explain | Ana's best reply to a column maximises her own (first) number down that column: U, D, M | correct | Osb 2.8.1 best-response definition; column L: 3 > 2 > 1; C: 3 > 2 > 0; R: 4 > 2 > 1 |
| l1-payoff-tables.json | screens[0].feedback.byKey.second | Picking largest second number per row reads Ben's payoffs | correct | derivation: the set {r1c3, r2c1, r3c2} is Ben's row-wise best replies |
| l1-payoff-tables.json | screens[1].explain | Ben's best reply to a row maximises second number along it: R, L, C; (D, C) carries both marks | correct | rows: U 4 > 2 > 1; M 3 > 1 > 0; D 3 > 2 > 1; (D, C) is mutual best reply (Osb 2.8.2) |
| l1-payoff-tables.json | screens[2].explain | Story to table: off-diagonal cells are mirror images, buyer gets £3 | correct | derivation from the stated story; symmetric game |
| l1-payoff-tables.json | screens[3].explain | Against Wait, Buy (3) beats Wait (2) although (Wait, Wait) pays both more than (Buy, Buy) | correct | derivation: 3 > 2 and 2 > 1 |
| l1-payoff-tables.json | screens[4].explain | Ben collects the second number; best reply to M is L | correct | row M second numbers 3 > 1 > 0 |
| l1-payoff-tables.json | screens[5].explain | A best reply is any move doing as well as the best, so there can be several | correct | Osb 2.8.1: best response set may contain several actions |
| l1-payoff-tables.json | screens[6].prose | Ana: argmax_i a_ij, Ben: argmax_j b_ij | correct | Osb 2.8.1 |
| l1-payoff-tables.json | screens[6].options[c].why | Along a row Ben's move changes; Ana varies her row down a column | correct | table convention, Osb 2.2 |
| l1-payoff-tables.json | screens[7].explain | 2 by 3: Ana's best replies T, B, B (3 cells), Ben's C, R (2 cells) | correct | L: 4 > 1; C: 3 > 2; R: 5 > 0; row T: 3 > 2 > 1; row B: 4 > 1 > 0 |
| l1-payoff-tables.json | screens[7].explain | Belief 0.6 L, 0.4 R: U 2.6, M 2.2, D 1.6 | correct | expected payoff of a pure action against a belief (Osb 4.1); 1.8 + 0.8, 0.6 + 1.6, 1.2 + 0.4 |
| l1-payoff-tables.json | screens[7].rows[3] | Buy is Ana's best reply to both of Ben's moves | correct | 1 > 0 and 3 > 2 (strict dominance, Osb 2.9) |
| l1-payoff-tables.json | screens[7].hints[0] | One best reply per column for Ana when there are no ties | correct | argmax is a singleton without ties |
| l1-payoff-tables.json | screens[8].explain | Against 3 ticks: 1 tick £100, 2 ticks £200, 3 ticks £150; best reply undercut by one tick; wide quotes invite undercutting | correct | derivation from the stated rule (tighter quote takes all 100 lots, tie splits 50/50): 100 x 1, 100 x 2, 50 x 3; Bertrand undercutting logic (Osb 3.2) |
| l1-payoff-tables.json | screens[8].canvas cells | Off-diagonal cells 100,0 / 0,100 / 0,200 and diagonal 50,50 / 100,100 / 150,150 | correct | same derivation |
| l1-payoff-tables.json | quiz[0] | Ana's best reply to R is T (4 > 1); tie option is wrong because row sums are irrelevant | correct | Osb 2.8.1 |
| l1-payoff-tables.json | quiz[1] | Ben's best reply to B is R (2 > 0) | correct | row B second numbers |
| l1-payoff-tables.json | quiz[2] | Row T worth 0.3 x 2 + 0.7 x 4 = 3.4; B worth 2.2, so T is best reply to the belief | correct | Osb 4.1 expected payoff; 1.5 + 0.7 = 2.2 |
| l1-payoff-tables.json | quiz[3] | Ana has two best replies to L (U and M tie at 2) | correct | column L: 2, 2, 1 |
| l1-payoff-tables.json | summary | Best reply down a column for Ana, along a row for Ben; ties give several | correct | Osb 2.8.1 |
| l2-dominated-moves.json | screens[0].explain | Tight beats Wide for Ana against each of Ben's quotes (2 > 1, 5 > 4) | correct | strict dominance, Osb 2.9.1 |
| l2-dominated-moves.json | screens[1].prose | Wide is strictly dominated by Tight; symmetric table so same for Ben | correct | Osb 2.9.1; transpose symmetry of the payoff matrix |
| l2-dominated-moves.json | screens[1].explain | Both quote Tight (2, 2) though (4, 4) is available: the prisoner's dilemma | correct | Osb 2.2 (Prisoner's Dilemma: dominant action equilibrium Pareto-dominated) |
| l2-dominated-moves.json | screens[1].byKey.wide | Both would like (Wide, Wide) but each gains by switching | correct | 5 > 4 for the deviator |
| l2-dominated-moves.json | screens[2].states.s0 | Only C is strictly dominated at the start (by R: 2 > 1, 6 > 4, 8 > 6); B, M, R, L not | correct | derivation; also no mix of T and B strictly beats M (needs alpha < 1/4 against C and alpha > 1/4 against R) and no mix beats B |
| l2-dominated-moves.json | screens[2].states.s1 | After C goes, T beats M (4 > 2, 6 > 3) and B (4 > 3, 6 > 2); R still beats L in rows M, B | correct | derivation |
| l2-dominated-moves.json | screens[2].explain | With only T left Ben prefers L (3 > 2); game ends at (T, L) | correct | iterated elimination, Osb 12.2 (finite game) |
| l2-dominated-moves.json | screens[2].prose | After each deletion look again: the smaller table can show a new dominated move | correct | Osb 12.2 iterated elimination |
| l2-dominated-moves.json | screens[3].explain | D (1, 1) is strictly dominated by half U half M (1.5, 1.5) though no pure row dominates it | correct | Osb 4.11 (domination by mixed strategy) |
| l2-dominated-moves.json | screens[3].options[d].why | Half U half D pays 0.5 against R | correct | 0.5 x 0 + 0.5 x 1 |
| l2-dominated-moves.json | screens[4].explain | Mix pays 1.5 in both columns; same check with Ben's numbers removes a column | correct | derivation; symmetric treatment of column player |
| l2-dominated-moves.json | screens[5] | Weak-deletion order 1 (U then L) ends at (2, 1); order 2 (D then R) ends at (1, 1) | correct | derivation: U weakly dominated by M (1 = 1, 0 < 2); then L by R over rows M, D (1 = 1, 0 < 1); D weakly dominated by M (0 < 1, 2 = 2); then R by L over rows U, M (1 > 0, 1 = 1) |
| l2-dominated-moves.json | screens[5].options[b].why | Order never matters for strict deletion; with ties the order picks the answer | correct | OR Prop 61.2 (order independence of strict IESDS in finite games); Osb 12.3 example of order dependence under weak dominance; the game here is finite |
| l2-dominated-moves.json | screens[5].explain | (U, L), (M, L), (M, R), (D, R) are the cells where neither gains by moving alone | correct | derivation: each is a pure Nash equilibrium (checked both players' deviations) |
| l2-dominated-moves.json | screens[5].explain | Weak deletion threw some equilibria away | correct | Osb 12.3: weak elimination can remove Nash equilibria |
| l2-dominated-moves.json | screens[6].explain | Matching pennies: no move dominated, deletion leaves whole table | correct | each action is a strict best response to one of the opponent's actions (Osb 4.3) |
| l2-dominated-moves.json | screens[7].prose | s strictly dominated by t when u(t, c) > u(s, c) for every c | correct | Osb 2.9.1 |
| l2-dominated-moves.json | screens[7].options[b].why | Never worse is weak dominance; strict needs more against every column | correct | Osb 2.9.2 (weak domination) |
| l2-dominated-moves.json | screens[8] drill | Round 1 removes T (by M) and C (by half L half R: 3.5 > 0, 6 > 5, 6 > 5); round 2 L (by R: 8 > 4, 7 > 5); round 3 M (5 < 6); end (B, R), Ana 6 | correct | derivation; rounds counted as simultaneous deletion of all dominated actions |
| l2-dominated-moves.json | screens[8].rows[2] | One-at-a-time game is three rounds: C; M and B; R | correct | derivation on screens[2] table |
| l2-dominated-moves.json | screens[8].rows[3] | Half L half C pays Ben 2 in row T and row B, beating R's 1 | correct | 0.5(4 + 0) = 2 |
| l2-dominated-moves.json | screens[9].explain | Tight pays 3000 + 2000k, Wide 2000k; Tight strictly dominant with three desks | correct | derivation from stated rule; n-player dominant strategy (Osb 2.9) |
| l2-dominated-moves.json | screens[10].explain | All Tight earn £3,000 each though all Wide pays £4,000; the prisoner's dilemma survives a third player | correct | derivation; n-player PD (Osb 2.8.4 analogue) |
| l2-dominated-moves.json | summary | Delete only strictly dominated moves; weak deletion can lose equilibria and depends on order | correct | Osb 12.2 to 12.3 |
| l2-dominated-moves.json | quiz[0] | R dominated by half L half C (2 > 1 in each row); L not dominated by C | correct | Osb 4.11 |
| l2-dominated-moves.json | quiz[1] | T beats B (4 > 3, 2 > 1), L beats R (1 > 0, 3 > 2); (T, L) Ben earns 1 | correct | derivation |
| l2-dominated-moves.json | quiz[2] | Cut strictly dominates Keep for both; (1, 1) | correct | Osb 2.2 PD |
| l3-nash-equilibrium.json | screens[0].explain | Only (D, C) is a best reply for both: D best to C and C best to D | correct | Osb 2.8.2 (NE as mutual best responses); column C: 3 > 2 > 0; row D: 3 > 2 > 1 |
| l3-nash-equilibrium.json | screens[1].prose | A cell where both play a best reply is a pure Nash equilibrium | correct | Osb 2.6 Definition 23.1 |
| l3-nash-equilibrium.json | screens[1].explain | From (D, C) Ana's switches pay 0 or 2 < 3; Ben's pay 2 or 1 < 3; neither gains alone | correct | derivation |
| l3-nash-equilibrium.json | screens[2].explain | Venue game: (X, X) and (Y, Y) both equilibria; equilibrium is stable, not necessarily good | correct | Osb 2.7 (coordination game, Pareto-ranked equilibria); deviations drop to 0 |
| l3-nash-equilibrium.json | screens[3].explain | Race (chicken): (A, P) and (P, A) only; from (P, P) a deviator gains 1, from (A, A) 2 | correct | Osb 2.7 hawk-dove analogue; 4 > 3, 0 > -2 |
| l3-nash-equilibrium.json | screens[4].explain | (Wide, Wide) has the largest total but is not an equilibrium: 5 > 4 for a lone deviator | correct | Osb 2.2 PD |
| l3-nash-equilibrium.json | screens[5].explain | Matching pennies: every cell has a loser who gains £2 by switching; no pure equilibrium | correct | Osb 2.7 Example 17.1 |
| l3-nash-equilibrium.json | screens[6].prose | a_{i*j*} >= a_{ij*} for all i and b_{i*j*} >= b_{i*j} for all j | correct | Osb 2.6 Definition 23.1 (weak inequality) |
| l3-nash-equilibrium.json | screens[6].options[c].why | Totals play no part in the equilibrium condition | correct | Osb 2.6 |
| l3-nash-equilibrium.json | screens[7] drill | Game 1: 0 pure NE; game 2: 1 at (B, C); game 3: 2 at (T, C), (M, L); venue game 2 | correct | sim: game-theory-L1-concepts.py:l3_drill (brute-force best-reply enumeration) |
| l3-nash-equilibrium.json | screens[7].prose | No best replies tie in the three games | correct | all column and row maxima are strict (enumeration) |
| l3-nash-equilibrium.json | screens[8].explain | Spread table: (1, 1) and (2, 2) are equilibria, (3, 3) is not; a tie keeps an equilibrium | correct | weak inequality in Definition 23.1; at (2, 2) undercut to 1 tick gives 100 = 100; sim: game-theory-L1-concepts.py:l3_spread |
| l3-nash-equilibrium.json | screens[8].explain | Competing quotes can stop at two ticks as well as one | correct | discrete Bertrand with a tick size has equilibria at the lowest two prices (Osb 3.2 exercise analogue) |
| l3-nash-equilibrium.json | quiz[0] | (3, 3) fails because an undercut to 2 ticks pays 200 > 150 | correct | derivation |
| l3-nash-equilibrium.json | quiz[1] | 2 by 3 game has no pure equilibrium | correct | Ana's best replies (B, L), (T, C), (B, R); Ben's (T, L), (B, C); disjoint |
| l3-nash-equilibrium.json | quiz[2].explain | Any strict gain breaks an equilibrium; a tie still holds | correct | Osb 2.6 (weak inequality) |
| l3-nash-equilibrium.json | summary | A game can have several equilibria or none in pure moves | correct | Osb 2.7 |
| l4-mixing.json | screens[0].explain | Heads pays Ana 2q - 1, Tails 1 - 2q; equal at q = 1/2 | correct | expected payoff against a mixed strategy (Osb 4.1) |
| l4-mixing.json | screens[1].prose | Symmetric game, so Ana mixing half makes Ben indifferent too | correct | derivation: Ben's heads pays -(2p - 1), tails -(1 - 2p) |
| l4-mixing.json | screens[1].explain | Value 0; neither improves by changing their mix alone: a mixed equilibrium | correct | Osb 4.3 Example 108.1 (matching pennies, unique NE (1/2, 1/2)) |
| l4-mixing.json | screens[2].explain | Each mixes to make the other indifferent: p = 3/5 from 2p = 3(1 - p); q = 2/5 from 3q = 2(1 - q); each expects 1.2, below either pure equilibrium | correct | Osb 4.3 indifference condition (BoS Example 111.1 analogue); sim: game-theory-L1-concepts.py:l4_venues |
| l4-mixing.json | screens[3].explain | Raising Ana's (X, X) payoff to 6 changes Ben's mix to q = 1/4 and Ana's expectation to 1.5 | correct | 6q = 2(1 - q); sim: game-theory-L1-concepts.py:l4_raised |
| l4-mixing.json | screens[4].explain | Ana's mix exists to keep Ben indifferent, so only Ben's payoffs enter it; p stays 3/5 | correct | Osb 4.3 Prop 116.2 (indifference characterisation) |
| l4-mixing.json | screens[4].options[d].why | 3p = 2(1 - p) is Ben's equation the wrong way round | correct | gives p = 2/5, the slip |
| l4-mixing.json | screens[5].explain | Crossing at q = -1/2 means U pays more for every q in [0, 1]: dominance; a dominated move is never mixed in | correct | 3 + q > 2 - q on [0, 1]; a strictly dominated action has zero weight in any NE (Osb 4.11 Prop 120.1) |
| l4-mixing.json | screens[5].explain | A mix outside 0 to 1 is the signal to delete moves first | correct | for a 2 by 2, lines crossing outside [0, 1] means one row is strictly better on all of [0, 1] (linearity) |
| l4-mixing.json | screens[6].prose | p solves p b11 + (1 - p) b21 = p b12 + (1 - p) b22; q the same in Ana's payoffs | correct | Osb 4.3 Prop 116.2 |
| l4-mixing.json | screens[6].explain | Check 0 < p < 1; a value outside means a move is dominated | correct | 2 by 2 linearity argument as above |
| l4-mixing.json | screens[7] drill | Race: a = 1/3, payoff 2; venues: 1/4, 0.75; new game q = 3/4, p = 1/2, each 1.5 | correct | sim: game-theory-L1-concepts.py:l4_drill |
| l4-mixing.json | screens[7].byKey.r3c1 | Mixed venue payoff 0.75 is worse than either pure equilibrium | correct | pure equilibria pay 3 and 1 |
| l4-mixing.json | screens[8].explain | Modified RPS (rock beats scissors for 2): unique equilibrium rock 1/4, paper 1/2, scissors 1/4, value 0; the bigger prize lifts its answer | correct | antisymmetric matrix so value 0 and symmetric optimal strategies (Ferguson Part II 2.4); uniqueness from the constraints Aq <= 0; sim: game-theory-L1-concepts.py:l4_rps2 |
| l4-mixing.json | screens[8].explain | A trader randomising order times is mixing so a predator cannot time her | correct | interpretation of mixed strategy as unpredictability (Osb 4.2) |
| l4-mixing.json | summary | Each mixes so the other is indifferent between the moves the other uses; solution outside 0 to 1 means a dominated move | correct | Osb 4.3 Prop 116.2 (indifference only over the support) |
| l4-mixing.json | quiz[0] | p = 1/4 from 3p + (1 - p) = 2(1 - p); q = 3/4 | correct | sim: game-theory-L1-concepts.py:l4_quiz1 |
| l4-mixing.json | quiz[1] | RPS with scissors beating paper for 3: rock 3/5, paper 1/5, scissors 1/5 | correct | sim: game-theory-L1-concepts.py:l4_rps3; uniqueness by the same constraint argument |
| l4-mixing.json | quiz[2] | T dominates B (5 > 2, 1 > 0) so Ana never mixes; payoffs do not become chances | correct | Osb 4.11 |
| l5-zero-sum.json | screens[0].explain | Row minima 2, 3, 0; midday guarantees at least 3 (maximin) | correct | Osb 11.1 (maxminimiser); derivation |
| l5-zero-sum.json | screens[1].explain | Column maxima 6, 3, 7; max-min = min-max = 3: a saddle point; value £300 | correct | Osb 11.3 (saddle point of a strictly competitive game); derivation |
| l5-zero-sum.json | screens[2].prose | Penalty: row minima 0.55, 0.65 miss column maxima 0.90, 0.95: no saddle | correct | derivation |
| l5-zero-sum.json | screens[2].explain | Lines 0.90 - 0.35p and 0.65 + 0.30p cross at p = 5/13, value 199/260; Ben dives left 6/13 | correct | sim: game-theory-L1-concepts.py:l5_penalty |
| l5-zero-sum.json | screens[2].explain | Ana kicks left less often because a left dive hurts her most there | correct | interpretation: (left, left) = 0.55 is her worst cell; optimal p = 5/13 < 1/2 |
| l5-zero-sum.json | screens[2].byKey.half | Half and half lets Ben dive left, holding Ana to 0.725 | correct | 0.90 - 0.175 = 0.725 < 0.80 |
| l5-zero-sum.json | screens[3].explain | 2 by 3: lower envelope peaks at p = 1/2, value 2.5; Ben mixes columns 2, 3 at 1/4, 3/4, never column 1 | correct | graphical method for 2 by n (Ferguson, *Game Theory*, Part II 2.3); sim: game-theory-L1-concepts.py:l5_2x3 |
| l5-zero-sum.json | screens[4].explain | Unequal pennies: Ben shows heads 3/8; both of Ana's moves pay -1/8; averaging the cells assumes random play | correct | sim: game-theory-L1-concepts.py:l5_unequal |
| l5-zero-sum.json | screens[4].options[b].why | Totals ignore how often each cell happens, which the players choose | correct | expected payoff weights cells by the product of mixing probabilities |
| l5-zero-sum.json | screens[5].hints[1] | v = (a11 a22 - a12 a21) / (a11 - a12 - a21 + a22) | correct | Ferguson Part II 2.2 (2 by 2 without saddle) |
| l5-zero-sum.json | screens[6].explain | Rows (3, 1), (5, 2): saddle at (2, 2) worth 2; formula gives p = 3 because it assumes no saddle | correct | row 2 strictly dominates row 1; max-min = min-max = 2 |
| l5-zero-sum.json | screens[7].prose | Saddle check max_i min_j a_ij = min_j max_i a_ij; otherwise p = (a22 - a21)/D, v as above | correct | Ferguson Part II 2.2; Osb 11.3 |
| l5-zero-sum.json | screens[7].options[c].why | The sign of D does not matter; a saddle is what breaks the formula | correct | without a saddle D is nonzero and the formula holds for either sign (Ferguson Part II 2.2) |
| l5-zero-sum.json | screens[7].explain | The value is what Ana can guarantee and Ben can hold her to | correct | von Neumann minimax theorem (Osb 11.4) |
| l5-zero-sum.json | screens[8] drill | Morra p = 9/16, v = -1/16; game B p = 1/3, v = 3; game C saddle worth 4 at (1, 1) | correct | sim: game-theory-L1-concepts.py:l5_drill |
| l5-zero-sum.json | screens[8].prose | Morra payoffs 3, -4, -4, 5 from total + 1 on even totals | correct | derivation: totals 2, 3, 3, 4 |
| l5-zero-sum.json | screens[9].explain | Ben expects £12.50 over 100 rounds; while he mixes 3/8 nothing Ana does helps | correct | 100 x 1/8; equaliser property of the optimal strategy in a 2 by 2 without saddle |
| l5-zero-sum.json | screens[9].feedback.correct | If Ana leans one way Ben can lean against it and win more | correct | best response to a non-equilibrium mix is pure and pays more than the value |
| l5-zero-sum.json | summary | Ana mixes to make her worst case as large as possible; that is the value | correct | Osb 11.4 (minimax theorem) |
| l5-zero-sum.json | quiz[0] | Rows (6, 2), (3, 4): no saddle, D = 5, p = 1/5, v = 3.6, between maximin 3 and minimax 4 | correct | sim: game-theory-L1-concepts.py:l5_quiz1; max-min <= v <= min-max |
| l5-zero-sum.json | quiz[1] | Rows (2, 4), (1, 3): saddle at (1, 1) worth 2; D = 0 | correct | row 1 dominates; derivation |
| l5-zero-sum.json | quiz[2] | Ana's equilibrium mix pays the value against either column, so Ben's pure switch changes nothing | correct | in a 2 by 2 without saddle both columns are in Ben's support, so Ana's optimal mix equalises them (Osb 4.3 Prop 116.2) |
| review-1.json | items[0] | Ben's best replies L, C, R along the diagonal | correct | row T 5 > 3 > 1; M 6 > 2 > 1; B 4 > 2 > 0 |
| review-1.json | items[1] | D strictly dominated by half U half M (2.5 > 2) | correct | Osb 4.11 |
| review-1.json | items[2] | Rows (5, 7), (2, 3): saddle 5 at (1, 1); formula gives -1 and does not apply | correct | derivation; D = -1 |
| review-1.json | items[3] | One pure NE at (T, L) | correct | sim: game-theory-L1-concepts.py:r1_count_one |
| review-1.json | items[4] | p = 2/5 from 2(1 - p) = 3p; q = 1/3 from 2q = 1 - q; no pure NE | correct | sim: game-theory-L1-concepts.py:r1_mixed |
| review-1.json | items[5] | IESDS: R (by C), T (by M), L (by C), B (by M); (M, C) = (7, 7) | correct | sim: game-theory-L1-concepts.py:r1_deletion |
| review-1.json | items[6] | No pure NE | correct | sim: game-theory-L1-concepts.py:r1_none |
| review-1.json | items[7] | 2 by 3 value 2.4 at p = 2/5; Ben mixes columns 2, 3 at 1/5, 4/5 | correct | sim: game-theory-L1-concepts.py:r1_2x3 |
| review-1.json | items[8] | Two pure NE at (T, C), (B, L) | correct | sim: game-theory-L1-concepts.py:r1_count_two |
| homework-1.json | items[0] | Derivation order: Ben's indifference, collect, divide, check 0 < p < 1, mirror for q; distractor sets Ana's own payoffs equal | correct | Osb 4.3 Prop 116.2; algebra checked |
| homework-1.json | items[0].lines[s4] | Outside 0 < p < 1 a move is dominated and nobody mixes | correct | 2 by 2 linearity: one column then dominates for Ben and the game has a pure equilibrium, contradicting the item's hypothesis |
| homework-1.json | items[1] | pure_nash with <= keeps ties; loop order returns sorted pairs; 7 tests | correct | sim: game-theory-L1-concepts.py:hw1_pure_nash (solution run against all tests, starter fails) |
| homework-1.json | items[2] | IESDS: M (by B), then L and C (by R), then B (by T); (T, R) = (3, 2) | correct | sim: game-theory-L1-concepts.py:hw1_deletion |
| homework-1.json | items[3] | q = 2/5 from 4q = q + 2(1 - q); p = 3/4; Ana expects 1.6; no pure NE | correct | sim: game-theory-L1-concepts.py:hw1_mixed |
| homework-1.json | items[4] | 2 by 2 zero-sum solver: saddle check (any row attaining max-min with any column attaining min-max is a saddle), else formula with q = (a22 - a12)/D; 7 tests | correct | if max row-min = min col-max = v then a[i][j] >= v and <= v for such i, j; Ferguson Part II 2.2; sim: game-theory-L1-concepts.py:hw1_zero_sum |
| homework-1.json | items[4].explain | With a saddle p and q are 0 or 1 | correct | pure optimal strategies exist at a saddle (Osb 11.3); the function's convention |
| homework-1.json | items[5].options[a] | A strictly dominated move is never played in an equilibrium | correct | Osb 4.11 Prop 120.1 |
| homework-1.json | items[5].options[c] | Deleting weakly dominated moves can lose an equilibrium | correct | Osb 12.3 |
| homework-1.json | items[5].explain | "A dominated move always has a better reply, so it never survives in an equilibrium" | imprecise | drops "strictly": a weakly dominated action can be played in a Nash equilibrium, as the lesson-2 trap shows ((U, L) is an equilibrium with U weakly dominated by M); Osb 12.3 |
| homework-1.json | items[6] | 2 by 3 rows (1, 5, 3), (6, 0, 2): value 8/3 at p = 2/3; Ben mixes columns 1, 3 at 1/6, 5/6 | correct | sim: game-theory-L1-concepts.py:hw1_2x3 |
| homework-1.json | items[7].model | Rows (5, -2), (-2, 1): no saddle; p = q = 3/10; value +0.10; cell average 0.50 assumes random play; if Ben shows heads over 30% Ana leans to heads | correct | sim: game-theory-L1-concepts.py:hw1_longform; 7q - 2 > 1 - 3q iff q > 0.3 |
| l6-game-trees.json | screens[0].explain | Backward induction: incumbent shares (5 > 2), entrant enters (3 > 0) | correct | Osb 5.5 (backward induction); derivation |
| l6-game-trees.json | screens[1].explain | Strategic form has two pure NE, (Out, Fight) and (In, Share); against Out the incumbent is indifferent between plans | correct | Osb 5.3 to 5.4 Example 156.1 (entry game); checked all four cells |
| l6-game-trees.json | screens[2].explain | (Out, Fight) relies on an empty threat; an equilibrium where every mover best-replies at every node, reached or not, is subgame perfect | correct | Osb 5.4 Definition 164.1 |
| l6-game-trees.json | screens[2].options[d].why | Tables often have several equilibria; the tree rules one out | correct | Osb 5.4: SPE is a refinement of NE |
| l6-game-trees.json | screens[3].explain | Centipede: every mover takes (5 > 4, 4 > 3, 3 > 2, 2 > 1); Ana takes at once, (2, 0), though both prefer (6, 4) | correct | Osb 7.1 Exercise 207.1 (centipede); sim: game-theory-L2-concepts.py:l6_centipede |
| l6-game-trees.json | screens[4].explain | An announced threat changes no payoff; a threat is credible only if its maker would carry it out | correct | Osb 5.4 (cheap talk changes no subgame) |
| l6-game-trees.json | screens[5].explain | With a tie at the incumbent's node both Out and In are subgame perfect outcomes | correct | Osb 5.5 (backward induction with indifference gives several SPE); derivation |
| l6-game-trees.json | screens[6].prose | V(node) = child's V with the mover's largest payoff, starting from the last decisions | correct | Osb 5.5 (Kuhn's backward induction, finite perfect-information game) |
| l6-game-trees.json | screens[6].options[b].why | The first mover's best end may need later movers to act against themselves | correct | centipede (6, 4) example |
| l6-game-trees.json | screens[7] drill | Six-move centipede 2; tree 2 via (2, 2); venue game Ana first 3, Ben first 2 | correct | sim: game-theory-L2-concepts.py:l6_drill (backward-induction solver) |
| l6-game-trees.json | screens[8].explain | Capacity makes Fight (6 - k) beat Share (5 - k); entrant stays out; incumbent keeps 10 - k against 5, so pays up to £5m | correct | commitment through sunk investment (Dixit 1980; Osb 5.4 analogue); derivation |
| l6-game-trees.json | screens[8].explain | A published hard risk limit buys the same credibility | correct | interpretation: commitment device |
| l6-game-trees.json | summary | A threat its maker would not carry out is discarded by the tree; paying to change your later payoffs can make it credible | correct | Osb 5.4; Schelling commitment |
| l6-game-trees.json | quiz[0] | Fight (3) beats Share (2): threat credible, entrant stays out | correct | derivation |
| l6-game-trees.json | quiz[1] | Ben picks (0, 3) after Risky, so Ana plays Safe for 2 | correct | derivation |
| l6-game-trees.json | quiz[2] | Sequential chicken: Ana goes straight, Ben swerves; first mover commits and gets 3 | correct | Osb 5.5 (first-mover advantage in chicken); derivation |
| l7-guess-two-thirds.json | screens[0].explain | Target is at most 66.67; a guess above it never does better than 66.67 whatever others write | correct | derivation: for g > 200/3, distance of g to target exceeds that of 200/3 by (g - 200/3)(1 - 2/(3n)) > 0 |
| l7-guess-two-thirds.json | screens[1].explain | Bound after k rounds is 100(2/3)^k; below 1 after 12 rounds; in the limit 0 is the only equilibrium | correct | Nagel (1995) AER; iterated dominance; unique NE at 0 for real-valued guesses and p < 1 (with integer guesses and many players "all 1" is also an equilibrium, a case the lesson does not pose); sim: game-theory-L2-concepts.py:l7_bounds |
| l7-guess-two-thirds.json | screens[2].explain | Level k guesses 50(2/3)^k; experiments find most players stop after one to three levels | correct | Nagel (1995): spikes at levels 1 and 2; Camerer, Ho and Chong (2004) average level about 1.5 |
| l7-guess-two-thirds.json | screens[3].explain | Room average 925/27 = 34.26, target 1850/81 = 22.84 | correct | weighted average; derivation |
| l7-guess-two-thirds.json | screens[4].explain | Zero wins only if everyone reasons all the way down; against this room guess about two thirds of its average | correct | best reply to a level-k population (Nagel 1995); derivation |
| l7-guess-two-thirds.json | screens[5].explain | Two players: target (a + b)/3 is always nearer the lower guess; 0 never loses | correct | derivation: (2b - a)/3 > abs(b - 2a)/3 for 0 <= a < b; sim: game-theory-L2-concepts.py:l7_two_player |
| l7-guess-two-thirds.json | screens[6].prose | bound_k = 100 p^k, level_k = 50 p^k; deleted guesses are only weakly dominated (they can tie) | correct | derivation; all-100 room makes every guess tie |
| l7-guess-two-thirds.json | screens[6].explain | For p < 1 deletion ends at 0, the one equilibrium | correct | Nagel (1995); contraction of the bound |
| l7-guess-two-thirds.json | screens[7] drill | Halving: 7 rounds, level 2 = 12.5; room target 26.30; plus 10 equilibrium 30 | correct | 100(1/2)^7 = 0.78; 355/9 x 2/3; x = 2x/3 + 10 unique fixed point (contraction) |
| l7-guess-two-thirds.json | screens[8].explain | Target 1.5 x average capped at 100: all 0 and all 100 are equilibria, all 50 and all 66.67 are not | correct | derivation with 50 players: a lone deviator from 0 moves the target by 3% of his guess; at 100 the cap holds; sim: game-theory-L2-concepts.py:l7_upward |
| l7-guess-two-thirds.json | screens[8].explain | Keynes's beauty contest: a market price is a guess about what others will pay | correct | Keynes (1936) ch. 12; standard interpretation |
| l7-guess-two-thirds.json | quiz[0] | 100(3/4)^2 = 56.25; 28.125 is the level-2 guess | correct | derivation |
| l7-guess-two-thirds.json | quiz[1] | Level 1 guesses 37.5 | correct | derivation |
| l7-guess-two-thirds.json | quiz[2] | Large room, others at 30: guess 20 | correct | best reply 20(n - 1)/(n - 2/3) tends to 20 |
| l8-sealed-bids.json | screens[0].explain | Against a rival bidding V/2, win chance 2b/100; (80 - b) 2b/100 peaks at b = 40, £32; shade to half | correct | Kr 2.3 (two uniform bidders, b = v/2 is the symmetric equilibrium); sim: game-theory-L2-concepts.py:l8_best_reply |
| l8-sealed-bids.json | screens[1] derive | Slope (160 - 4b)/100 zero at 40; ends 0 and 30 below 32 | correct | calculus; b > 50 wins surely and earns 80 - b < 30 |
| l8-sealed-bids.json | screens[2].explain | Second price: bid decides only whether you win, never what you pay; shading loses profitable lots, overbidding buys losses; bid your value | correct | Vickrey (1961); Kr 2.1 Prop 2.1 (weakly dominant); Osb 3.5 |
| l8-sealed-bids.json | screens[3].explain | Two uniform bidders: larger value averages 66.67, smaller 33.33; first price pays half the larger (33.33), second price the smaller (33.33); your profit 32 both ways | correct | E[max] = 2/3, E[min] = 1/3 (order statistics); sim: game-theory-L2-concepts.py:l8_revenue |
| l8-sealed-bids.json | screens[3].explain | "This is revenue equivalence: with n bidders the price averages (n-1)/(n+1) x 100" | imprecise | true for risk-neutral bidders with independent private values (Kr 3.1 Prop 3.1; Vickrey 1961); with risk-averse bidders the first-price auction raises more (Kr 4.1 Prop 4.1); neither hypothesis is stated here, in screens[6], the summary, or homework-2 items[6] option c |
| l8-sealed-bids.json | screens[4].explain | In second price your bid sets whether you win, never the price; bidding 80 wins exactly the lots worth winning; bidding value in first price earns nothing | correct | Kr 2.1 |
| l8-sealed-bids.json | screens[4].options[c].why | "Overbidding wins only when the second bid is above £80, and then you pay more than the lot is worth" | imprecise | overbidding to £100 also wins whenever the second bid is below £80, as £80 would; only the extra wins (second bid between 80 and 100) are described; Kr 2.1 |
| l8-sealed-bids.json | screens[5].explain | With a reserve, bidding your value is still right; a value below the reserve stays out | correct | Kr 2.5 (reserve price in a second-price auction; truthful bidding remains weakly dominant) |
| l8-sealed-bids.json | screens[6].prose | n uniform bidders: second price bid v; first price bid (n-1)v/n; E[price] = (n-1)/(n+1) x 100; the first-price bid is the expected second-highest value given yours is highest | correct | Kr 2.3 Example (beta(v) = E[Y1 given Y1 < v] = (n-1)v/n for uniform); E[second-highest of n] = (n-1)/(n+1); sim: game-theory-L2-concepts.py:l8_equilibrium_bid |
| l8-sealed-bids.json | screens[6].explain | More bidders mean less shading | correct | (n-1)/n increases in n |
| l8-sealed-bids.json | screens[7] drill | 40, 72, 60, 55 | correct | formulas above; second price pays the second bid |
| l8-sealed-bids.json | screens[8].explain | Ten bidders: top value averages 10/11 x 100, winner bids 9/10 of it: 81.82; an English auction ends near the second-highest value | correct | Kr 2.3; Kr 1.1 (English auction and second-price equivalence under private values) |
| l8-sealed-bids.json | summary | Bid value in second price; shade to (n-1)/n in first price; both give the seller (n-1)/(n+1) x 100 | correct (see imprecise row above for the missing hypotheses) | Kr 2.3, 3.1 |
| l8-sealed-bids.json | quiz[0] | Winner pays 45, the second-highest bid | correct | rule of the format |
| l8-sealed-bids.json | quiz[1] | Six bidders: bid 5/6 x 72 = 60 | correct | Kr 2.3 |
| l8-sealed-bids.json | quiz[2] | Seven bidders: price 75 either way; top value averages 87.5 | correct | E[second-highest] = 6/8; E[max] = 7/8; 6/7 x 87.5 = 75 |
| l9-winners-curse.json | screens[0].explain | Five unbiased estimates with errors U(-10, 10): the winning (largest) error averages 10 x 4/6 = 6.67; winning says your estimate was probably too high | correct | E[max of n U(-a, a)] = a(n-1)/(n+1); P(max > 0) = 1 - 2^-5; sim: game-theory-L2-concepts.py:l9_overshoot |
| l9-winners-curse.json | screens[0] exact bars | Bin masses 0.0003 ... 0.4095 | correct | F(x) = ((x + 10)/20)^5 differences |
| l9-winners-curse.json | screens[1] derive | Error = -a + 2aU keeps order; E[max U] = n/(n+1); overshoot a(n-1)/(n+1) | correct | order statistics of the uniform (Casella and Berger 5.4) |
| l9-winners-curse.json | screens[2].explain | Ten bidders overshoot 8.18; a winner who bid her estimate loses that on average; more bidders means shading more | correct | formula; Kagel and Levin (1986) RNNE bid x - a + Y shades more as n grows; Thaler (1988) |
| l9-winners-curse.json | screens[3] derive | Acquire-a-company: owner accepts iff V <= b; E[V given accept] = b/2; worth 0.8b; every accepted offer loses 0.2b; offer nothing | correct | Samuelson and Bazerman (1985); derivation; sim: game-theory-L2-concepts.py:l9_acquire |
| l9-winners-curse.json | screens[4].explain | £60m offer buys a firm worth £48m on average given acceptance; the unconditional average never enters | correct | derivation |
| l9-winners-curse.json | screens[5].explain | Expected profit 0.6 x (-12) = -7.2; in general (b/100)(kb/2 - b) | correct | law of total expectation; valid for b <= 100 |
| l9-winners-curse.json | screens[6].explain | At k = 2 every offer breaks even; below 2 every offer loses; above 2 offer £100m; the sign of k/2 - 1 decides | correct | derivation: profit (b/100)(k/2 - 1)b, increasing in b when k > 2, acceptance certain at 100 |
| l9-winners-curse.json | screens[7].prose | Two curses, one rule: condition on winning; overshoot a(n-1)/(n+1); profit (b/100)(kb/2 - b) | correct | as above |
| l9-winners-curse.json | screens[8] drill | 16.36, 7.20, 0, 50 | correct | formulas above |
| l9-winners-curse.json | screens[9].explain | Having won among five with estimate 100 and no other information, best guess of V is 100 - 6.67 = 93.33; a fill is a win too (adverse selection) | correct | diffuse prior: given winning, your error is distributed as the max of five; Glosten and Milgrom (1985) analogy; sim: game-theory-L2-concepts.py:l9_posterior |
| l9-winners-curse.json | summary.formula.note | "Shade by this; it grows with the number of bidders" | imprecise | shading by exactly the mean overshoot makes the winner's expected profit zero (E[V - (x_max - s)] = s - a(n-1)/(n+1)); it is the break-even shade, not the best bid, which shades more (Kagel and Levin 1986 RNNE b(x) = x - a + Y with Y <= 2a/(n+1)); sim: game-theory-L2-concepts.py:l9_breakeven |
| l9-winners-curse.json | quiz[0] | Six bidders on ±14: 14 x 5/7 = 10 | correct | formula |
| l9-winners-curse.json | quiz[1] | k = 1.2, offer 50: 0.5 x (30 - 50) = -10 | correct | derivation |
| l9-winners-curse.json | quiz[2] | Doubling rivals: shade more, since the winning estimate is the largest of more errors | correct | a(n-1)/(n+1) increases in n; Kagel and Levin (1986) |
| l10-splitting-a-pie.json | screens[0].explain | Three-round shrinking pie: 81, then Ben keeps 9 of 90, then Ana keeps 91 | correct | Osb 16.1 finite-horizon alternating offers; backward induction |
| l10-splitting-a-pie.json | screens[1].explain | Ultimatum: an indifferent Ben accepts £0, Ana keeps £100; in whole pounds with a Ben who refuses £0 she keeps £99; real responders refuse small offers | correct | Osb 6.1 Example 183.1 (two SPE with indivisible units); Güth, Schmittberger and Schwarze (1982) |
| l10-splitting-a-pie.json | screens[2].explain | Shares 1 - 0.9 s recursively: 0.1, 0.91, 0.181, 0.8371, closing on 1/1.9 | correct | derivation; sim: game-theory-L2-concepts.py:l10_finite |
| l10-splitting-a-pie.json | screens[3] derive | Rubinstein: 1 - x = delta_B y, 1 - y = delta_A x, x = (1 - delta_B)/(1 - delta_A delta_B); equal delta gives 1/(1 + delta) | correct | Rubinstein (1982); Osb 16.1.3 Prop 467.1 |
| l10-splitting-a-pie.json | screens[4].explain | delta_A = 0.9, delta_B = 0.8: Ana 0.7143; patience is bargaining power | correct | formula |
| l10-splitting-a-pie.json | screens[5].explain | No last round, delta = 0.9: s = 1 - 0.9 s gives 52.63% | correct | Osb 16.1.3 |
| l10-splitting-a-pie.json | screens[6].explain | delta = 0 is the ultimatum game, share 1; delta near 1 gives an even split | correct | limits of 1/(1 + delta) |
| l10-splitting-a-pie.json | screens[7].explain | delta = 0.99: 50.25%; when waiting costs almost nothing proposing first is worth almost nothing | correct | formula |
| l10-splitting-a-pie.json | screens[8] drill | 20%, 55.56%, 68.97%, 84% | correct | formulas; sim: game-theory-L2-concepts.py:l10_drill |
| l10-splitting-a-pie.json | screens[9].explain | Outside option £30 below Ben's 47.37 changes nothing; £60 binds, Ana offers 60 and keeps 40 | correct | outside option principle (Binmore, Shaked and Sutton 1989; Osb 16.1.4) |
| l10-splitting-a-pie.json | quiz[0] | Two rounds, delta = 0.6, Ben last: Ana 40% | correct | derivation |
| l10-splitting-a-pie.json | quiz[1] | delta = 0.5, no last round: 66.67% | correct | formula |
| l10-splitting-a-pie.json | quiz[2] | Ana's share falls as delta_B rises | correct | d x / d delta_B = (delta_A - 1)/(1 - delta_A delta_B)^2 < 0 |
| review-2.json | items[0] | Entry game: share, enter, 2 | correct | backward induction |
| review-2.json | items[1] | Three-move centipede ends at (2, 0) | correct | sim: game-theory-L2-concepts.py:r2_centipede |
| review-2.json | items[2] | Two fifths: level 2 guesses 8; 16 is the deletion bound | correct | 50 p^2, 100 p^2 |
| review-2.json | items[3] | Four bidders, value 80: bid 60 | correct | Kr 2.3 |
| review-2.json | items[4] | Second price pays 67 | correct | rule |
| review-2.json | items[5] | Five bidders: 66.67 either format | correct | Kr 3.1 (same hypothesis note as l8) |
| review-2.json | items[6] | Five bidders ±9: overshoot 6 | correct | formula |
| review-2.json | items[7] | k = 1.5, offer 40: -4 | correct | derivation |
| review-2.json | items[8] | Three rounds delta = 0.7: 79%; no last round delta = 0.95: 51.28% | correct | formulas |
| homework-2.json | items[0] derive | Best reply to a rival bidding V/2 is b = v/2; end b = 50 earns v - 50 <= v^2/200 | correct | (v - 100)^2 >= 0; for b > 50 profit v - b falls |
| homework-2.json | items[1] | spe(tree): recursion keeping the child best for the mover; no ties; 7 tests; starter follows the first move | correct | Osb 5.5; sim: game-theory-L2-concepts.py:hw2_spe (solution passes all tests, starter fails) |
| homework-2.json | items[2] | Capacity worth up to £3m: 9 - k against 6 | correct | derivation |
| homework-2.json | items[3] | delta_A = 0.85, delta_B = 0.95: Ana 25.97% | correct | Rubinstein formula |
| homework-2.json | items[4] | Eight bidders ±15: 11.67 | correct | formula |
| homework-2.json | items[5] | Two thirds plus 12: equilibrium 36 | correct | fixed point of a contraction |
| homework-2.json | items[6] | Truthful bidding never worse (a); price equals first price with uniform values (c); more bidders raise the price (d false) | correct | Vickrey (1961); Kr 2.3, 3.1 (option c inherits the l8 hypothesis note) |
| homework-2.json | items[7].model | k = 1.5: loss 0.25b; at 60, -9; break-even at 2; above 2 offer 100; the curse comes from the seller's information, not rivals | correct | Samuelson and Bazerman (1985); derivation |
| l11-pot-odds.json | screens[0].explain | A call wins 150 with chance x and loses 50: 200x - 50, break-even 25%, the call over the pot after you call; that is the price | correct | CA ch. 4 (pot odds); derivation; sim: game-theory-L3-concepts.py:l11_price |
| l11-pot-odds.json | screens[0].byKey.half, byKey.third | 50% divides by the pot before the bet; 33% forgets your own call | correct | derivation of the three denominators |
| l11-pot-odds.json | screens[1].explain | Call earns 45 - 35 = 10; call whenever your chance beats the price | correct | EV = (chance - price)(P + 2B) |
| l11-pot-odds.json | screens[2].explain | 9 hearts remain among 46 unseen; against K♣ Q♦ all 44 rivers confirm the 9 win; "your chance is 9/46 = 19.57%" | imprecise | 9 of 44 rivers win is exact (sim: game-theory-L3-concepts.py:l11_outs); but the prose has said "your opponent holds a king" and the explain names K♣ Q♦, information under which the river is a heart with chance 9/45 = 20% (one known non-heart) or 9/44 = 20.45% (both known); 9/46 holds only under the unstated convention that his cards count as unseen |
| l11-pot-odds.json | screens[3].explain | Price 30/150 = 20%, chance 19.57% a whisker less, call earns -0.65, fold | imprecise | key right only under the 46-card convention; with his king known the call breaks even exactly (9/45 = 20%), and against the K♣ Q♦ of screens[2] it earns +£0.07 (9/44); sim: game-theory-L3-concepts.py:l11_convention |
| l11-pot-odds.json | screens[4].explain | Two cards: no heart 38/47 x 37/46 = 0.6503 so 34.97%; price 33.3%: call; exact equity against K♣ Q♦ is 376/990 = 37.98% | correct | hypergeometric; full enumeration with a 7-card evaluator gives 376 wins of 990 (sim: game-theory-L3-concepts.py:l11_flop_equity) |
| l11-pot-odds.json | screens[4].byKey.four, twice | Rule of four is a quick check (36 vs 34.97); adding 9/47 twice double counts | correct | derivation |
| l11-pot-odds.json | screens[5].explain | Price 50/200 = 25%; pot odds 3 to 1 say the same | correct | CA ch. 4 |
| l11-pot-odds.json | screens[6].explain | A check makes the price 0 so always see the card; an all-in call ends the betting so no implied odds | correct | definition of implied odds (CA ch. 4, Sklansky *Theory of Poker* ch. 7) |
| l11-pot-odds.json | screens[7].prose | price = B/(P + 2B); chance about outs/unseen; about 2% an out per card, 4% with two | correct | CA ch. 4; the rule of 2 and 4 is an approximation (checked in sim) |
| l11-pot-odds.json | screens[8] drill | 20%; 8/46 = 17.39%; 1 - 39/47 x 38/46 = 31.45%; 3 to 1 is 25% | correct | sim: game-theory-L3-concepts.py:l11_two_card; the 9♠8♠ draw has exactly 8 outs by enumeration |
| l11-pot-odds.json | screens[9].explain | Implied odds: 8/46 (80 + X) = 38/46 x 20 gives X = 15 | correct | derivation |
| l11-pot-odds.json | summary | Price is the call over the final pot; count outs over unseen cards; 2% and 4% rule | correct | CA ch. 4 |
| l11-pot-odds.json | quiz[0] | 25 into 75: 25/125 = 20% | correct | formula |
| l11-pot-odds.json | quiz[1] | 10/46 = 21.74%; on the turn 46 cards are unseen | correct | 52 - 2 - 4 |
| l11-pot-odds.json | quiz[2] | 20% below a 25% price with no betting left: fold; each call loses 5% of the final pot | correct | EV = (chance - price)(P + 2B); sim: game-theory-L3-concepts.py:l11_quiz3 |
| l12-ranges.json | screens[0].explain | AK has 16 combos, 4 suited 12 offsuit; the A♠ on the board kills 4 | correct | 4 x 4; enumeration (sim: game-theory-L3-concepts.py:l12_combos) |
| l12-ranges.json | screens[1].explain | A pair has C(4, 2) = 6 combos, 3 with one card seen | correct | enumeration |
| l12-ranges.json | screens[2].explain | Range AQ 12, 99 3, 54s 4, JTs 4 = 23; you beat 4; 4/23 = 17.39% below 25%: fold | correct | combos by enumeration; each hand's strength against KK on A9632 checked with the evaluator (sim: l12_river_hands) |
| l12-ranges.json | screens[3].explain | Your aces leave him 2 x 4 = 8 AK combos: a blocker | correct | enumeration |
| l12-ranges.json | screens[4].explain | Your kings leave 2 KQs combos; 6 of 25 = 24% is a fold; counted as 4 it would be 8/27 and +£9.26 | correct | enumeration and EV |
| l12-ranges.json | screens[4].options[c].why | A raise folds his bluffs and gets called by better hands | correct | standard river logic (CA ch. 13); no hand in the stated range both beats KK and folds |
| l12-ranges.json | screens[5].explain | 6 of 25: 36 - 38 = -2 | correct | derivation |
| l12-ranges.json | screens[6].explain | Three aces seen: C(1, 2) = 0 combos of AA | correct | enumeration |
| l12-ranges.json | screens[7].prose and summary.formula | equity = combos you beat / combos in the range; pair C(k, 2), two ranks k1 k2 | imprecise | true on the river with no split pots, which is every spot in the lesson; with cards to come, or when some combos chop, equity is the win share over runouts (CA ch. 3), so the summary states it without its hypothesis |
| l12-ranges.json | screens[8] drill | KQo with a king on the board: 9; a pair is dealt 78/1326 = 1/17; one extra bluff makes 7/26 = 26.9% > 25% | correct | enumeration; (6 + b)/(25 + b) >= 1/4 iff b >= 1/3 |
| l12-ranges.json | screens[9].explain | Pot-sized bet needs 33.3%; (6 + b)/(25 + b) >= 1/3 gives b >= 3.5, so 4 bluffs such as QJs | correct | derivation; QJs has 4 live combos on this board |
| l12-ranges.json | quiz[0], quiz[1] | 88 with two eights seen: 1; AJs with A♣ seen: 3 | correct | enumeration |
| l12-ranges.json | quiz[2] | 3 of 10 (30%) beats a 25% price: call, EV 10; a raise gains nothing over calling | correct | derivation |
| l13-toy-poker.json | screens[0].explain | Ben's call earns 300x - 100, zero at x = 1/3; that bluff share leaves Ben nothing to exploit | correct | CA ch. 11 (bluffing ratio alpha = B/(P + B) of value bets, B/(P + 2B) of bets); sim: game-theory-L3-concepts.py:l13_freqs |
| l13-toy-poker.json | screens[1].explain | A bluff earns 100(1 - c) - 100c, zero at c = 1/2; each mix makes the other indifferent | correct | CA ch. 11 (defence frequency 1 - alpha = P/(P + B)) |
| l13-toy-poker.json | screens[2].explain | Half-pot: bluffs 1/4, calls 2/3; the bluff share equals the caller's price; smaller bets need fewer bluffs and more calls | correct | formulas; B/(P + 2B) decreases in B/P |
| l13-toy-poker.json | screens[3].explain | Cut-down three-card game: Ana bets K always, J one in three, checks Q; Ben calls K, folds J, calls Q one in three; value +1/18 to Ana | correct | CA ch. 11 (the AKQ game, P = 2: alpha = 1/3, bluff a third of the lowest card, call the middle card 1/3); verified by best-reply enumeration over all pure plans (sim: game-theory-L3-concepts.py:l13_cut) |
| l13-toy-poker.json | screens[3].byKey.r1c1, r2c1 | Ben's queen wins 3 against a jack and loses 1 to a king, so one jack bet per three kings; Ben calls 2/3 of bets, every king and a third of queens | correct | indifference arithmetic; 1/2 + 1/2 x 1/3 = 2/3 = P/(P + B) |
| l13-toy-poker.json | screens[4].explain | A bluff that loses when called still pays by making Ben pay off kings; never bluffing is as readable as always bluffing | correct | CA ch. 11; sim: l13_cut uniqueness check (any other jack rate is exploited by a pure reply) |
| l13-toy-poker.json | screens[5].explain | Bluffing above a third makes Ben call everything; below, fold everything; an unbalanced player is exploited by a pure reply | correct | linearity of the call's value in x |
| l13-toy-poker.json | screens[6].prose | bluffs = B/(P + 2B) of bets; calls = P/(P + B) of the time | correct | CA ch. 11 |
| l13-toy-poker.json | screens[7] drill | 2/5 and 1/3; 3/10 and 4/7; Ana also betting every queen is worth -1/9 against any best reply | correct | formulas; sim: game-theory-L3-concepts.py:l13_queen_bets |
| l13-toy-poker.json | screens[8].explain | Full Kuhn poker is worth -1/18 to the first player; 64 pure plans a side | correct | Kuhn (1950); LP over the 64 by 64 matrix gives -1/18 (sim: game-theory-L3-concepts.py:l13_kuhn_full) |
| l13-toy-poker.json | summary | Bluff B/(P + 2B) of bets, call P/(P + B); too many or too few bluffs is beaten by a pure reply | correct | CA ch. 11 |
| l13-toy-poker.json | quiz[0], quiz[1] | 100 into 300: bluffs 1/5, calls 3/4 | correct | formulas |
| l13-toy-poker.json | quiz[2] | Against a player who never bluffs, a bluff-catcher folds | correct | exploitative reply (CA ch. 11) |
| l14-value-of-information.json | screens[0], [1] | Blind 30; with one look 1/3 + 2/3 x 1/2 = 2/3, so 60; the look is worth 30 | correct | derivation |
| l14-value-of-information.json | screens[2].explain | Trade worth 5 now; told the outcome 15; perfect information worth 10, the most any message can be worth | correct | EVPI (Raiffa, *Decision Analysis* ch. 2); EVSI <= EVPI |
| l14-value-of-information.json | screens[3].explain | 80% analyst: good call makes the trade worth 20, bad -10 so skip; with him 10 against 5: worth 5 | correct | Bayes with a symmetric signal; sim: game-theory-L3-concepts.py:l14_analyst |
| l14-value-of-information.json | screens[4].explain | +50/-10 trade: after a bad call still +2, so the analyst is worth 0; information that cannot change a decision is worth nothing | correct | Raiffa ch. 2; sim |
| l14-value-of-information.json | screens[5].explain | 60% analyst worth 0 (bad call leaves exactly 0); 70% worth 2.5; accuracy pays only past the point where a message flips the decision | correct | sim |
| l14-value-of-information.json | screens[6].prose | VOI = E[max_a E[payoff given message]] - max_a E[payoff]; never negative, never above perfect information | correct | Raiffa ch. 2; Jensen-type argument; sim bounds check |
| l14-value-of-information.json | screens[7] drill | Die: E[max(X, 3)] = 4 against 3.5, worth 0.5; seeing his cards worth 36; analyst worth 5 so do not pay 6 | correct | derivation |
| l14-value-of-information.json | screens[8].explain | Tell: weak with chance 43/125, win 24/43 so call; strong 82/125, win 3/41 so fold; worth 0.192 x 150 - 0.152 x 50 = 21.20 | correct | Bayes; sim: game-theory-L3-concepts.py:l14_tell |
| l14-value-of-information.json | quiz[0] | +40 (0.6) / -40 (0.4): now 8, perfect 24, worth 16 | correct | derivation |
| l14-value-of-information.json | quiz[1] | A report that never changes the trade is worth 0; more information never hurts | correct | Raiffa ch. 2 |
| l14-value-of-information.json | quiz[2] | Seeing a fair coin before a £10 evens bet is worth 5 | correct | derivation |
| l15-sizing-and-risk.json | screens[0].explain | Growth 0.3 ln(1 + 4f) + 0.7 ln(1 - f) peaks at f = 0.125, 2.82% a bet; past about 0.268 it is negative; expected profit keeps rising | correct | Kelly (1956); sim: game-theory-L3-concepts.py:l15_growth (root 0.268 found numerically; simulated mean log return matches) |
| l15-sizing-and-risk.json | screens[1].explain | All-in ten times survives with 0.3^10; expected profit says stake it all, growth says otherwise | correct | derivation; E[profit] = 0.5 f is increasing |
| l15-sizing-and-risk.json | screens[2].explain | Kelly f* = p - q/b = 0.125; growth 0.02817; half Kelly 0.02177 (77%); double Kelly 0.00657 though every bet has edge | correct | Kelly (1956); Thorp (2006) "The Kelly criterion in blackjack, sports betting and the stock market" sec. 3 |
| l15-sizing-and-risk.json | screens[3].explain | Ruin with n stakes, even money, p > 1/2, no target: (q/p)^n: 0.3666, 0.1344, 0.0181; doubling n squares it; seed 4 shows 46 of 300 broke, within sampling error of 13.44% | correct | Feller vol. I XIV.2 (gambler's ruin against an infinitely rich opponent); simulation agrees; the seeded engine count replicated exactly (sim: game-theory-L3-concepts.py:l15_walk_seed); 46/300 = 15.3% is 1 standard error (2.0 points) above 13.44% |
| l15-sizing-and-risk.json | screens[4].explain | At f = 0.3 growth is -0.0131 so the bankroll shrinks though every bet has edge; Kelly p - q/b is always below p | correct | derivation |
| l15-sizing-and-risk.json | screens[5].explain | 3 to 1 at 25% is fair, f* = 0, every stake shrinks the bankroll; growth needs edge | correct | Jensen: E[ln(1 + fR)] < ln(1 + f E[R]) = 0 |
| l15-sizing-and-risk.json | screens[6].prose | Three yardsticks; poker ruin about e^(-2 mu B / sigma^2), the continuous form of (q/p)^n | correct | CA ch. 22 (risk of ruin); Brownian approximation of the simple walk |
| l15-sizing-and-risk.json | screens[7] drill | 0.175, 0.02924, (12/13)^15 = 0.3010, e^(-2 x 0.05 x 1500/64) = 0.0960 between 0.2096 and 0.0439 | correct | formulas; sigma per hand = 80/sqrt(100) = 8 big blinds |
| l15-sizing-and-risk.json | screens[8].explain | At the true 25%, f = 0.125 grows 0.0012 a bet; half Kelly 0.0074; desks bet a fraction of Kelly when the edge is uncertain | correct | derivation; MacLean, Thorp and Ziemba (2010) on fractional Kelly |
| l15-sizing-and-risk.json | summary | Past about twice Kelly growth shrinks; ruin (q/p)^n | correct | for this bet the root is 2.14 Kelly; for small edges the zero of growth is near 2f* (quadratic approximation) |
| l15-sizing-and-risk.json | quiz[0], quiz[1] | Kelly 0.2 at 3 to 1 and 40%; ruin (2/3)^8 = 0.0390 | correct | formulas |
| l15-sizing-and-risk.json | quiz[2] | Half Kelly keeps about three quarters of growth; the curve is near a parabola at its top | correct | g(f*/2) = 3/4 g(f*) for a parabola; here 77% |
| review-3.json | items[0] | 40 into 80: price 25%, call earns 36 - 28 = 8 | correct | derivation |
| review-3.json | items[1], items[2] | 4/46 = 8.70%; 12 outs twice 44.96%, rule of four 48% too high | correct | sim: l11_two_card |
| review-3.json | items[3], items[4] | JJ with one jack seen 3; AQ with an ace seen and a queen held 9 | correct | enumeration |
| review-3.json | items[5] | 60 into 120: call 2/3; bluffs 1/4 | correct | formulas |
| review-3.json | items[6] | A 30% caller: each bluff earns +40; he should call half the time | correct | derivation |
| review-3.json | items[7] | 90% analyst worth 7.5 | correct | sim: l14_analyst |
| review-3.json | items[8], items[9] | Kelly 1/15; ruin (9/11)^15 = 0.0493 | correct | formulas |
| homework-3.json | items[0] | Bluff-share derivation: call wins P + B against a bluff, loses B; x(P + B) = (1 - x)B; x = B/(P + 2B); the distractor fixes Ben's calls | correct | CA ch. 11 |
| homework-3.json | items[1] | combos and range_equity: strike dead cards from the deck; 14 tests; starter fails ten | correct | enumeration reproduces every expected value (sim: l12_combos); the starter ignores dead so tests 4 to 13 fail |
| homework-3.json | items[2] | Implied odds X = 250/9 | correct | derivation |
| homework-3.json | items[3] | 100 into 150: bluffs 2/7, calls 3/5 | correct | formulas |
| homework-3.json | items[4] | +40 (0.4) / -20 (0.6): now 4, perfect 12; 75% analyst: good with chance 0.45 worth 20, bad -9.09 skip; worth 5 | correct | Bayes; sim: l14_analyst |
| homework-3.json | items[5] | Full Kelly on a wrong edge: 0.0012; half Kelly 0.0074 | correct | derivation |
| homework-3.json | items[6] | More stakes lower ruin; doubling the stake turns r into sqrt r; edge does not prevent ruin; Kelly maximises growth not expected profit | correct | (q/p)^n; Kelly (1956) |
| homework-3.json | items[7].model | 60 into 120: price 25%; 25 combos, 6 win, 24%; EV -2.40; one more bluff flips it; 4 more against a pot-sized bet; balanced bluff share a quarter at this size | correct | derivation; enumeration |

## Verdict counts

298 claim rows: correct 291, imprecise 7, wrong 0, misleading 0, unverified 0. The seven imprecise rows are the six findings in `docs/reviews/audit-game-theory-1-3.md` (the l11 finding spans two rows).

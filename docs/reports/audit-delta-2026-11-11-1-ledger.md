# Claim ledger: delta audit 2026-11-11, batch 1

Blind audit of content added or changed after each course closed (puzzles, game-theory, brainteasers, coding-int, research-int, systems, ito, measure-prob). One row per claim in the changed items. "script" in the basis column means a check in `docs/reports/delta-2026-11-11-1-concepts.py`.

Rows: 349. Verdicts: correct 340, wrong 1, imprecise 7, misleading 1, unverified 0.

| course | rows | correct | wrong | imprecise | misleading | unverified |
|---|---|---|---|---|---|---|
| puzzles | 42 | 42 | 0 | 0 | 0 | 0 |
| game-theory | 28 | 27 | 0 | 1 | 0 | 0 |
| brainteasers | 31 | 31 | 0 | 0 | 0 | 0 |
| coding-int | 46 | 43 | 1 | 2 | 0 | 0 |
| research-int | 55 | 52 | 0 | 2 | 1 | 0 |
| systems | 69 | 68 | 0 | 1 | 0 | 0 |
| ito | 31 | 31 | 0 | 0 | 0 | 0 |
| measure-prob | 47 | 46 | 0 | 1 | 0 | 0 |

| course | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| puzzles | homework-4.json | items[9].prompt | 6 to 5 pays £1.20 profit per £1; draw refunds; chances 0.45, 0.25, 0.30 sum to 1 | correct | Odds convention b = 6/5; 0.45 + 0.25 + 0.30 = 1 |
| puzzles | homework-4.json | items[9].model Hypotheses | Independent matches with the same chances, p + r + q = 1, q > 0 | correct | Hypotheses of the strong law used in step 1; q > 0 used in step 4 |
| puzzles | homework-4.json | items[9].model Hypotheses | Fixed fraction f with 0 <= f < 1 keeps wealth positive | correct | Loss multiplier 1 - f > 0 |
| puzzles | homework-4.json | items[9].model Hypotheses | Fastest long-run growth means maximising the expected log per match | correct | Kelly (1956); Cover and Thomas, Elements of Information Theory, ch. 16 (Th. 16.3.1) |
| puzzles | homework-4.json | items[9].model Hypotheses | Favourable means pb > q: expected profit pb - q per £1 | correct | E[profit] = pb + r*0 - q |
| puzzles | homework-4.json | items[9].model step 1 | Multipliers 1 + bf, 1 and 1 - f with chances p, r, q | correct | Direct from the payouts |
| puzzles | homework-4.json | items[9].model step 1 | ln(W_n/W_0) is a sum of i.i.d. bounded terms; SLLN gives (1/n) ln(W_n/W_0) -> E[ln M] a.s. | correct | Strong law of large numbers (Durrett, PTE, Th. 2.4.1); three finite values since f < 1 |
| puzzles | homework-4.json | items[9].model step 1 | Wealth grows like e^{n g(f)}, so the fastest growth maximises g | correct | Consequence of the SLLN limit; script MC (growth 0.0319 at f*) |
| puzzles | homework-4.json | items[9].model step 2 | g(f) = p ln(1 + bf) + q ln(1 - f); the draw term is r ln 1 = 0 | correct | Expectation of ln M |
| puzzles | homework-4.json | items[9].model step 3 | g'(f) = pb/(1 + bf) - q/(1 - f) | correct | Chain rule |
| puzzles | homework-4.json | items[9].model step 4 | g'' = -pb^2/(1 + bf)^2 - q/(1 - f)^2 < 0, so g strictly concave on [0, 1) | correct | Both terms negative as q > 0 |
| puzzles | homework-4.json | items[9].model step 4 | A zero of g' is the unique maximum; it exists as g'(0) = pb - q > 0 and g' -> -inf as f -> 1 | correct | Intermediate value theorem with strict monotonicity |
| puzzles | homework-4.json | items[9].model step 5 | f* = (pb - q) / (b(p + q)) | correct | Algebra from pb(1 - f) = q(1 + bf); script grid maximum |
| puzzles | homework-4.json | items[9].model step 6 | 0 < f* < 1; with no draw f* = p - q/b | correct | pb - q < pb + qb; standard Kelly formula (Thorp 2006, sec. 2) |
| puzzles | homework-4.json | items[9].model step 6 | g = (p + q) h with h the growth of the conditional bet; the draw scales growth and keeps the peak | correct | Factor p + q out of g; script identity check |
| puzzles | homework-4.json | items[9].model step 7 | f* = 0.24/0.9 = 4/15 = 0.2667; multipliers 1.32 and 11/15 | correct | script |
| puzzles | homework-4.json | items[9].model step 7 | g(4/15) = 0.1249 - 0.0930 = 0.0319 a match | correct | script |
| puzzles | homework-4.json | items[9].model step 7 | Slip: draw as a loss gives p - (1 - p)/b = -0.0083 | correct | script |
| puzzles | homework-4.json | items[9].model step 7 | Slip: p - q/b = 0.2 forgets p + q is not 1 | correct | script |
| puzzles | homework-4.json | items[9].model step 8 | At 8/15: multipliers 1.64 and 7/15; g = 0.2226 - 0.2286 = -0.0060 | correct | script |
| puzzles | homework-4.json | items[9].model step 8 | Negative growth: ln W_n -> -inf, wealth tends to 0 almost surely | correct | SLLN of step 1; script MC (95% of 20,000-match paths below start, mean growth -0.0060) |
| puzzles | homework-4.json | items[9].model step 8 | Mean multiplier is still 1 + f(pb - q) = 1.128; the mean is carried by rare paths | correct | E[M] = 1 + 0.5333 x 0.24; Jensen |
| puzzles | homework-4.json | items[9].model step 8 | Second-order parabola (pb - q)f - (pb^2 + q)f^2/2 is back at 0 at twice its peak | correct | ln(1 + x) = x - x^2/2 + ...; symmetry of a parabola |
| puzzles | homework-4.json | items[9].model step 8 | Exact zero of g is about 0.513, just below 2f* | correct | script bisection: 0.51307 |
| puzzles | homework-4.json | items[9].model step 8 | For a long shot the sign can differ: 20 to 1, p = 0.1 gives g(2f*) = 0.0114 > 0 | correct | script: f* = 0.055, g(0.11) = 0.0114 |
| puzzles | homework-4.json | items[9].rubric[0] | Required: four hypotheses, the log aim by the law of large numbers, pb > q | correct | Matches the prompt ("state your hypotheses"); nothing false demanded |
| puzzles | homework-4.json | items[9].rubric[1] | Required: g(f), the draw term r ln 1 = 0, f* = (pb - q)/(b(p + q)) | correct | Steps 2 to 5 |
| puzzles | homework-4.json | items[9].rubric[2] | Required: g'' < 0 so the zero is the maximum; g'(0) > 0 so f* > 0 | correct | Step 4 |
| puzzles | homework-4.json | items[9].rubric[3] | Required: f* = 4/15 = 0.2667 and g(f*) = 0.0319 | correct | script |
| puzzles | homework-4.json | items[9].rubric[4] | Optional: g(2f*) = -0.0060 < 0, wealth to 0 though the mean is positive | correct | script |
| puzzles | review-1.json | items[9].widget.answer | Expected turns to five different stickers of eight: 7.0762 | correct | Sum of geometric waits 8/8 + 8/7 + 8/6 + 8/5 + 8/4; script exact and MC |
| puzzles | review-1.json | items[9].widget.wrong[0] | Slip 21.7429 = 8 H_8, the wait for all eight | correct | script; not a valid answer to this question |
| puzzles | review-1.json | items[9].widget.wrong[1] | Slip 5: one turn per sticker | correct | Ignores repeats; not valid under any method |
| puzzles | review-1.json | items[9].feedback.generic | With k held a new sticker comes with chance (8 - k)/8 | correct | Uniform draws |
| puzzles | review-1.json | items[9].feedback.byKey | all-eight: that is 8 H_8; one-each: repeats cost extra turns | correct | As above |
| puzzles | review-1.json | items[9].explain | Wait 8/(8 - k) for k = 0..4: 1 + 8/7 + 8/6 + 8/5 + 2 = 7.0762 | correct | Mean of a geometric; Ross, First Course, ch. 7 (coupon collecting) |
| puzzles | review-4.json | items[9].widget.answer | Ticket paying £16 if THH precedes HHH is worth £14 | correct | P(THH first) = 7/8; script MC 0.875 |
| puzzles | review-4.json | items[9].widget.wrong[0] | Slip 8: race treated as even | correct | P is 7/8, not 1/2 |
| puzzles | review-4.json | items[9].widget.wrong[1] | Slip 2: prices the HHH side, 16 x 1/8 | correct | Complement |
| puzzles | review-4.json | items[9].feedback.generic | Ask when HHH can win at all | correct | Only on flips 1 to 3 |
| puzzles | review-4.json | items[9].feedback.byKey.even | Any T before the first HHH hands the race to THH | correct | After a T, the first HH is preceded by T |
| puzzles | review-4.json | items[9].explain | HHH wins only if the first three flips are HHH (1/8); any earlier T means the first HH after it completes THH | correct | Standard Penney argument; Grinstead and Snell, sec. 11 (pattern races) |
| game-theory | homework-1.json | items[7].widget.model (display edit) | The three-line aligned display states the same indifference: 5p - 2(1 - p) = -2p + (1 - p), 7p - 2 = 1 - 3p, p = 3/10 | correct | Diff is layout only; algebra rechecked; script |
| game-theory | homework-1.json | items[7].widget.model Saddle | Row minima -2, -2; column maxima 5, 1; maximin -2 < minimax 1, so no saddle | correct | von Neumann; Osborne, Introduction to Game Theory, sec. 11.2; script |
| game-theory | homework-1.json | items[7].widget.model Mix | Ana's p makes Ben indifferent between his columns; q = 3/10 by the same equation | correct | Symmetric matrix; indifference principle |
| game-theory | homework-1.json | items[7].widget.model Value | Value +£0.10 a round to Ana; cell average +£0.50 assumes random play | correct | script |
| game-theory | homework-1.json | items[7].widget.model Lean | If Ben shows heads more than 30%, heads pays Ana more (7q - 2 > 1 - 3q) | correct | 7q - 2 > 1 - 3q iff q > 3/10 |
| game-theory | homework-1.json | items[7].widget.rubric | Seven rows restate the model; none required | correct | Each row matches a model step |
| game-theory | homework-1.json | items[8].prose | Each home buys from the nearer cart; ties split a half each; same spot splits every home | correct | Hotelling line with discrete sites; well defined |
| game-theory | homework-1.json | items[8].question | Row i is Ana at ana_spots[i]; column j is Ben at ben_spots[j]; cell (Ana £, Ben £) | correct | Standard bimatrix convention |
| game-theory | homework-1.json | items[8].question | ana[j] lists every best row to column j; ben[i] every best column to row i, increasing | correct | Definition of best reply with ties kept; Osborne sec. 2.8 |
| game-theory | homework-1.json | items[8].widget.solution | street_table counts coffees with halves and multiplies by each own price | correct | script: agrees with an exact-fraction version on 300 random streets |
| game-theory | homework-1.json | items[8].widget.solution | best_replies takes the maxima of first numbers down a column and second numbers along a row, ties kept | correct | script: agrees with a definition-based check |
| game-theory | homework-1.json | items[8].widget.solution | Float equality on a x (count of halves) is exact | correct | Halves and small integers are exact in binary floating point |
| game-theory | homework-1.json | items[8].widget.tests | Nine hidden tests; solution passes, starter fails | correct | script |
| game-theory | homework-1.json | items[8].widget.how | Check runs 9 hidden tests; cells compared by isclose, reply lists exactly | correct | Count of tests is 9 |
| game-theory | homework-1.json | items[8].feedback.correct | Every best reply is found, ties included | correct | Tests 5, 6, 7, 9 carry ties |
| game-theory | homework-1.json | items[8].explain | Ana's best replies are the rows with the largest first number down a column; Ben's the columns with the largest second number along a row | correct | Definition of best reply |
| game-theory | review-1.json | items[9].prose | The game has no pure equilibrium | correct | script: no cell is a mutual best reply |
| game-theory | review-1.json | items[9].widget.answer | Ana's expected payoff at the mixed equilibrium is 2.2 | correct | q = 2/5 from 4q + (1 - q) = q + 3(1 - q); script |
| game-theory | review-1.json | items[9].widget.wrong[0] | Slip 2.25: average of her four payoffs | correct | (4 + 1 + 1 + 3)/4; not an equilibrium value |
| game-theory | review-1.json | items[9].widget.wrong[1] | Slip 1.5: Ben's payoff from Ana's mix of 1/2 | correct | p = 1/2 from 2 - p = 3p; script |
| game-theory | review-1.json | items[9].feedback.generic | Ben mixes to make Ana indifferent; then either row gives her value | correct | Indifference principle |
| game-theory | review-1.json | items[9].feedback.byKey | average: as if both mix half and half; ben: that is Ben's payoff | correct | As above |
| game-theory | review-1.json | items[9].explain | q = 2/5; T pays Ana 4 x 0.4 + 0.6 = 2.2 | correct | script |
| game-theory | review-2.json | items[9].prose | Each round of deletion removes every guess above the current bound | imprecise | Read literally, no guess lies above the current bound (100 at the start); the round removes guesses above half of it. Finding G1 |
| game-theory | review-2.json | items[9].widget.answer | The bound first falls below 1 after 7 rounds | correct | 100/2^7 = 0.78125; script |
| game-theory | review-2.json | items[9].widget.wrong[0] | Slip 6: bound 1.5625, still above 1 | correct | 100/64 |
| game-theory | review-2.json | items[9].feedback.generic | Round k leaves guesses up to 100 x 0.5^k | correct | Target is at most half the largest surviving guess; Osborne sec. 12.2 (iterated elimination) |
| game-theory | review-2.json | items[9].explain | Six rounds give 1.5625; round 7 gives 0.78125 | correct | script |
| brainteasers | homework-1.json | items[8].widget.prompt | An L-tetromino is three squares in a line plus one beside an end, at right angles | correct | Definition (Golomb, Polyominoes, ch. 1) |
| brainteasers | homework-1.json | items[8].widget.prompt | Fifteen L pieces cannot cover a 6 by 10 board | correct | Area 60 is not a multiple of 8; Golomb; proved below |
| brainteasers | homework-1.json | items[8].widget.model Area | 6 x 10 = 60 = 15 x 4, so area decides nothing | correct | Arithmetic |
| brainteasers | homework-1.json | items[8].widget.model Chessboard | Every L covers 2 dark and 2 light; board is 30 and 30 | correct | script: all 304 placements are 2-2 |
| brainteasers | homework-1.json | items[8].widget.model Stripes | Odd columns dark: 5 columns of 6, so 30 dark and 30 light | correct | Arithmetic |
| brainteasers | homework-1.json | items[8].widget.model Split | Line down one column: three of one colour, extra square in the next column, so 3 and 1 | correct | script: every placement is 3-1 |
| brainteasers | homework-1.json | items[8].widget.model Split | Line across c, c+1, c+2: two of one colour, extra square in column c or c+2, so 3 and 1 | correct | script |
| brainteasers | homework-1.json | items[8].widget.model Track | Each piece adds +2 or -2 to dark minus light; total 4a - 30, never 0; nearest +-2 at a = 7, 8 | correct | 30 is not a multiple of 4; script |
| brainteasers | homework-1.json | items[8].widget.model Contradiction | A tiling needs dark minus light 0, so none exists | correct | Invariant argument |
| brainteasers | homework-1.json | items[8].widget.model Rows | Alternate rows give the same split and the same 30 and 30 | correct | 3 dark rows of 10; script row-stripe check |
| brainteasers | homework-1.json | items[8].widget.rubric[0] | Optional: area and chessboard decide nothing | correct | Matches the optional part of the prompt |
| brainteasers | homework-1.json | items[8].widget.rubric[1] | Required: stripes by column or row, 30 of each | correct | Either stripe accepted |
| brainteasers | homework-1.json | items[8].widget.rubric[2] | Required: both cases of the 3 and 1 split argued | correct | Both cases are needed for a complete proof |
| brainteasers | homework-1.json | items[8].widget.rubric[3] | Required: steps of +-2 total 4a - 30, never 0 | correct | Parity argument |
| brainteasers | homework-1.json | items[8].explain | Chessboard balances every L; stripes give 3 and 1; fifteen steps of +-2 cannot cancel | correct | An odd number of +-2 steps sums to 2 mod 4 |
| brainteasers | homework-2.json | items[8].prose | Each sees only the two neighbours; simultaneous guesses; with two people left and right are the same hat | correct | Indices i - 1 and i + 1 modulo 2 coincide |
| brainteasers | homework-2.json | items[8].prose | A plan can get at least floor(n/2) right for every colouring, for every n >= 2 | correct | Pairing plan; script: solution passes n = 2..12 |
| brainteasers | homework-2.json | items[8].widget.solution | Even i bets its hat matches the right neighbour; odd i bets it differs from the left; lone last person guesses 0 | correct | Exactly one of each pair is right; Winkler, Mathematical Puzzles (hat pairs) |
| brainteasers | homework-2.json | items[8].widget.postlude | worst_case plays every colouring and returns the fewest right | correct | Exhaustive over 2^n colourings; shuffle only defeats state |
| brainteasers | homework-2.json | items[8].widget.tests | Tests demand exactly floor(n/2), not "at least" | correct | No plan exceeds it: mean right is n/2; script exhaustive at n = 3, 4 |
| brainteasers | homework-2.json | items[8].widget.tests | Solution passes all nine; starter fails all | correct | script |
| brainteasers | homework-2.json | items[8].widget.how | Nine hidden tests for circles of 2 to 12, odd sizes included | correct | n = 2, 3, 4, 5, 7, 8, 9, 10, 12 |
| brainteasers | homework-2.json | items[8].feedback.correct | Each pair covers both cases, match and differ, so one of every pair is right | correct | Hats either match or differ |
| brainteasers | homework-2.json | items[8].explain | Persons 2m and 2m + 1 see each other; exactly one is right whatever the hats | correct | As above |
| brainteasers | homework-2.json | items[8].explain | No plan does better: a guess never depends on your own hat, so it is right on half the colourings and the average is n/2 | correct | Linearity of expectation over uniform colourings; minimum <= mean; script exhaustive n = 3, 4 |
| brainteasers | review-1.json | items[9].prose | Fill, empty and pour each count as a step | correct | Convention stated |
| brainteasers | review-1.json | items[9].widget.answer | Fewest steps to 8 litres in the 11-litre jug is 6 | correct | script BFS over all states |
| brainteasers | review-1.json | items[9].widget.wrong[0] | Slip 8: best route that starts by filling the 7 | correct | script BFS from (7, 0): 7 more steps |
| brainteasers | review-1.json | items[9].widget.wrong[1] | Slip 3: counted only the pours | correct | The 6-step route has 3 pours |
| brainteasers | review-1.json | items[9].feedback.generic | Write the states and search from the start, shortest first | correct | Breadth-first search gives a shortest route |
| brainteasers | review-1.json | items[9].explain | Fill 11, pour (leaves 4), empty 7, move 4 across, refill 11, top up 7 with 3, leaving 8 | correct | States (0,11) (7,4) (0,4) (4,0) (4,11) (7,8) |
| coding-int | homework-3.json | items[8].prose | mkdir and write make missing folders; write replaces old text; read gives None when no file | correct | Specification; internally consistent with the tests |
| coding-int | homework-3.json | items[8].prose | ls gives sorted names, [name] for a file, [] for a missing path | correct | Specification; test 1, 5 |
| coding-int | homework-3.json | items[8].prose | rm deletes a file or a whole folder; removing / or a missing path does nothing | correct | Specification; test 4 |
| coding-int | homework-3.json | items[8].prose | mv refuses, changing nothing, when src is missing or /, or dst exists or lies inside src | correct | Specification; test 6; moving a folder into itself would orphan it |
| coding-int | homework-3.json | items[8].prose | size is the total text length at or below a path; missing path 0 | correct | Specification |
| coding-int | homework-3.json | items[8].prose | Every method but ls must cost time in proportion to the names in its paths, whatever the number of files | correct | Achievable with a cached total per node; script timing (2,000 against 64,000 files, same cost) |
| coding-int | homework-3.json | items[8].widget.solution | Trie of nodes, each with children, text and a cached total | correct | Standard design (CLRS ch. 12 trees; the design lesson of this level) |
| coding-int | homework-3.json | items[8].widget.solution | write adds len(text) - old total to every node above the file | correct | script: passes test 3 and the random case |
| coding-int | homework-3.json | items[8].widget.solution | rm subtracts the removed total from the nodes above and unlinks once | correct | script |
| coding-int | homework-3.json | items[8].widget.solution | mv checks every refusal first, compares names not strings (d[:len(s)] == s), then relinks and moves the total | correct | script: tests 6, 7; agrees with a flat-dict version on a random case |
| coding-int | homework-3.json | items[8].widget.solution | An empty text is still a file (text is not None) | correct | Test 3 reads '' back |
| coding-int | homework-3.json | items[8].widget.tests | Ten hidden tests; solution passes, starter fails; big_case answer [1492763773, 2048, 33199, 43591] | correct | script |
| coding-int | homework-3.json | items[8].widget.postlude | big_case never writes to a folder or inside a file: files end in .t, folders are single letters | correct | Read of the generator; keeps the stated promise |
| coding-int | homework-3.json | items[8].widget.how | Ten hidden tests; test 10 plays 100,000 random steps within 5 s | correct | Count is 10; 0.3 s native; Pyodide time checked by the playthrough gate |
| coding-int | homework-3.json | items[8].feedback.correct | Each node carries the size below it, so every step is one walk down a path | correct | As the solution |
| coding-int | homework-3.json | items[8].feedback.byKey.test-2 | A moved file leaves every folder above src and joins every folder above dst | correct | Totals above both ends change |
| coding-int | homework-3.json | items[8].feedback.byKey.test-3 | Rewriting changes the folders above by the difference in length | correct | As the solution |
| coding-int | homework-3.json | items[8].feedback.byKey.test-4 | Removed size leaves every folder above; / stays | correct | Test 4 |
| coding-int | homework-3.json | items[8].feedback.byKey.test-6 | Test 6 asks for three moves that must be refused | wrong | Test 6 holds four refused moves: /a to /b, /a to /a/k/l, / to /z, /a/f to /b/g (script check fails). Finding C1 |
| coding-int | homework-3.json | items[8].feedback.byKey.test-6 | Check every refusal before you make any folder for dst | correct | ls('/a') must stay ['f'] |
| coding-int | homework-3.json | items[8].feedback.byKey.test-7 | Compare names, not strings: /ab is not inside /a | correct | Prefix-of-string bug |
| coding-int | homework-3.json | items[8].feedback.byKey.test-10 | If it timed out, keep a running total on each node | correct | Recomputing size is O(files) a call |
| coding-int | homework-3.json | items[8].explain | size is one walk; write, rm and mv change totals only above the change; a moved folder keeps its own totals | correct | As the solution |
| coding-int | homework-4.json | items[8].widget.prompt | count_pairs counts pairs of positions i < j with sizes[i] + sizes[j] == target | correct | Definition |
| coding-int | homework-4.json | items[8].widget.model Restate | Equal sizes at different positions pair; a position never pairs with itself | correct | i < j |
| coding-int | homework-4.json | items[8].widget.model Example | [4, 6, 5, 5, 1, 9, 5] with target 10 gives 5 | correct | script: model code and brute force |
| coding-int | homework-4.json | items[8].widget.model Brute | n(n - 1)/2 = 19,999,900,000 pair checks at 200,000 | correct | script |
| coding-int | homework-4.json | items[8].widget.model Plan A | For each x add the count of earlier target - x, then count x: each pair once, never with itself | correct | script: equals brute force on 500 random lists |
| coding-int | homework-4.json | items[8].widget.model Plan A | Each step is a constant-time dict look-up, so time is O(n) | imprecise | Hash look-ups are constant time on average, not in the worst case (CLRS sec. 11.2). Finding C3 |
| coding-int | homework-4.json | items[8].widget.model Plan A | The dict holds up to n keys: O(n) memory | correct | One key per distinct value |
| coding-int | homework-4.json | items[8].widget.model Plan B | Sort, two pointers; below target moves left up, above moves right down | correct | Sorted two-sum; script |
| coding-int | homework-4.json | items[8].widget.model Plan B | Sort is O(n log n); about log n extra for std::sort; Python sort up to n/2 | correct | Introsort recursion depth; Timsort merge buffer (CPython listsort.txt) |
| coding-int | homework-4.json | items[8].widget.model Plan B | Two different values multiply run lengths; a run of k equal halves gives k(k - 1)/2 | correct | script: run rule equals brute force |
| coding-int | homework-4.json | items[8].widget.model Trade-off | A is faster and has no duplicate rule; B saves the dict memory but sorts and reorders or copies | correct | O(n) against O(n log n) |
| coding-int | homework-4.json | items[8].widget.model Code | The typed code is correct | correct | script |
| coding-int | homework-4.json | items[8].widget.model Follow-up 1 | Sorted input: two pointers run in O(n) time and O(1) memory and win | correct | No sort needed |
| coding-int | homework-4.json | items[8].widget.model Follow-up 2 | Many targets: counts once; each target sums c_v c_{t-v} for v < t - v and c_v(c_v - 1)/2 at v = t - v, O(d) | correct | script: formula equals brute force |
| coding-int | homework-4.json | items[8].widget.model Follow-up 3 | C++ answer can reach about 2 x 10^10, above int 2,147,483,647, so long long | correct | 32-bit int on mainstream ABIs; script |
| coding-int | homework-4.json | items[8].widget.rubric[0] | Optional: restates as pairs of positions with a repeated-value example | correct | Matches the prompt |
| coding-int | homework-4.json | items[8].widget.rubric[1] | Optional: brute force n(n - 1)/2, about 2 x 10^10 | correct | script |
| coding-int | homework-4.json | items[8].widget.rubric[2] | Required: both plans with costs and a choice with a reason | correct | The prompt asks for the trade-offs |
| coding-int | homework-4.json | items[8].widget.rubric[3] | Required: code correct, and said why target - x is looked up before x is counted | imprecise | A correct plan that counts first and then sums c_v c_{t-v} has no such order to explain, yet cannot tick a required row. Finding C2 |
| coding-int | homework-4.json | items[8].widget.rubric[4] | Optional: sorted input, two pointers O(n) and O(1) | correct | Follow-up 1 |
| coding-int | homework-4.json | items[8].explain | Dict: one pass, O(n) time and memory; two pointers trade a sort for O(1) memory beyond the sort | correct | As the model (average-case caveat under C3) |
| coding-int | homework-4.json | items[8].explain | Looking up before counting counts each pair once and never a size with itself | correct | script |
| coding-int | homework-4.json | items[8].explain | Saying the trade-off before the code lets the interviewer steer early | correct | Interview practice; McDowell, Cracking the Coding Interview, ch. VII |
| research-int | homework-1.json | items[8].widget.prompt (added) | Optional point: plain words, no unexplained null, alpha or type I error, inside two minutes | correct | Restates rubric[3], which is not required; no content claim |
| research-int | homework-1.json | items[8].widget.prompt | Sharpe 1.0 over five years: t = sqrt(5) = 2.24, p = 0.025 | correct | t = SR sqrt(T) (Lo 2002, eq. 6 with i.i.d. returns); script two-sided p 0.0253 |
| research-int | homework-1.json | items[8].widget.prompt | Power 0.61 against a true Sharpe of 1 | correct | script: 0.609 |
| research-int | homework-1.json | items[8].widget.model p-value | With no edge, luck gives a result this strong, up or down, about 1 in 40; not the chance the signal is worthless | correct | Definition of a two-sided p-value; Casella and Berger sec. 8.3.4; ASA statement (2016) |
| research-int | homework-1.json | items[8].widget.model Power | A real Sharpe of 1 is caught about six times in ten; a miss proves little | correct | script |
| research-int | homework-1.json | items[8].widget.model Correction | Twenty unrelated nulls give a p of 0.025 or less about four times in ten | correct | 1 - 0.975^20 = 0.397; script |
| research-int | homework-1.json | items[8].widget.model Correction | Bonferroni bar 0.05/20 = 0.0025; 0.025 is ten times too big | correct | Bonferroni; Casella and Berger sec. 11.2.4 context |
| research-int | homework-1.json | items[8].widget.model Follow-up 2 | 80% power needs t to average 2.8, so 7.84 years | correct | script |
| research-int | homework-1.json | items[8].widget.model Follow-up 3 | Holm tests the best against 0.05/20 first and stops | correct | Holm (1979) step-down |
| research-int | homework-1.json | items[8].widget.model Follow-up 3 | Benjamini-Hochberg can pass only if at least half the versions did well, as when all twenty are under 0.05 | correct | p_(k) <= k/400 with p_(k) >= 0.025 needs k >= 10; script MC |
| research-int | homework-1.json | items[8].widget.rubric | Rows 0 to 2 required, row 3 optional; match the model | correct | Unchanged rows |
| research-int | homework-2.json | items[8].widget.prompt | Eigenvalues 20.6, 3.1, 2.4, then 47 falling from 0.85 to about 0.17; 23 components explain 80% | correct | script: sum 50.07, first 23 reach 80.6% |
| research-int | homework-2.json | items[8].widget.model What | Each component is a basket of standardised returns weighted by an eigenvector of the correlation matrix | correct | Jolliffe, Principal Component Analysis, sec. 2.3 |
| research-int | homework-2.json | items[8].widget.model What | Baskets are uncorrelated; each eigenvalue is the variance of its basket | correct | Jolliffe sec. 2.1 (in sample) |
| research-int | homework-2.json | items[8].widget.model What | On correlations the eigenvalues sum to 50; share is eigenvalue over 50; first is 41% | correct | Trace of a correlation matrix; script |
| research-int | homework-2.json | items[8].widget.model What | Nearly every stock has the same sign in the first, so it is the market; next two (6%, 5%) are usually group against group | correct | Perron-Frobenius for positive correlations; Laloux et al. (1999) |
| research-int | homework-2.json | items[8].widget.model How many | It depends on the job | correct | Jolliffe ch. 6 |
| research-int | homework-2.json | items[8].widget.model How many | Pure noise tops out near (1 + sqrt(50/500))^2 = 1.73 | correct | Marchenko-Pastur upper edge; script MC mean 1.67, max 1.78 over 300 draws |
| research-int | homework-2.json | items[8].widget.model How many | First three clear it; the fourth, 0.85, does not | correct | script MC with three planted factors: exactly three clear the edge in 100 of 100 |
| research-int | homework-2.json | items[8].widget.model How many | Other 47 sum to 23.9, about 0.51 a stock, so a stricter bar is 0.51 x 1.73 = 0.88 | imprecise | Arithmetic right, but 0.88 is the lower bar, easier to clear than 1.73; "stricter" reads the wrong way (script check fails). Finding R1 |
| research-int | homework-2.json | items[8].widget.model How many | Three are structure; the 80% rule adds 20 that are noise | correct | 23 - 3 |
| research-int | homework-2.json | items[8].widget.model How many | For the forecast choose the number by error on later data, in time order | correct | Hastie, Tibshirani and Friedman, ESL sec. 3.5.1 and 7.10 |
| research-int | homework-2.json | items[8].widget.model Mislead | PCA ranks by variance, never by prediction; a tiny component can carry the forecast | correct | Jolliffe (1982), A note on the use of principal components in regression; script MC |
| research-int | homework-2.json | items[8].widget.model Mislead | On covariance the most volatile stocks take over; correlations treat every stock alike | correct | Jolliffe sec. 3.3 |
| research-int | homework-2.json | items[8].widget.model Mislead | In a sell-off correlations rise, the market share grows, smaller loadings reshuffle | correct | Equicorrelation eigenvalue 1 + (n - 1) rho rises with rho |
| research-int | homework-2.json | items[8].widget.model Mislead | Signs are arbitrary; fix a convention before comparing fits | correct | v and -v are both eigenvectors |
| research-int | homework-2.json | items[8].widget.model Follow-up 1 | The 41% is same-day shared movement and says nothing about tomorrow's direction | correct | Variance share is contemporaneous |
| research-int | homework-2.json | items[8].widget.model Follow-up 2 | Covariance only if the stocks had similar volatilities | imprecise | Covariance is also right when variance in return units is the object, as in a risk model (Jolliffe sec. 3.3; Connor and Korajczyk 1988). Finding R3 |
| research-int | homework-2.json | items[8].widget.model Follow-up 3 | Equicorrelation rho: first eigenvalue 1 + 49 rho; 20.6 matches 0.4; at 0.6 it is 30.4, a 61% share | correct | script |
| research-int | homework-2.json | items[8].widget.model Follow-up 3 | Baskets fitted in calm markets describe a stressed market badly; refit on a rolling window | correct | Non-stationary correlations; practice |
| research-int | homework-2.json | items[8].widget.rubric[0] | Required: uncorrelated baskets of standardised returns, share is eigenvalue over 50, first is the market | correct | Model |
| research-int | homework-2.json | items[8].widget.rubric[1] | Required: noise reaches about 1.73, three are structure, 20 of noise; forecast number on held-out data | correct | The noise edge is taught in the PCA lesson of this level, so the row asks for taught content |
| research-int | homework-2.json | items[8].widget.rubric[2] | Required: variance not relevance, plus one of units, drift, signs | correct | Model |
| research-int | homework-2.json | items[8].widget.rubric[3] | Optional: plain words inside two minutes | correct | Matches the prompt |
| research-int | homework-2.json | items[8].explain | First carries 41%; noise reaches 1.73, so three are structure; forecast number from held-out error | correct | As the model |
| research-int | homework-4.json | items[8].prose | Ignore cancelled quotes; replace prices sharing a second by their mean | correct | Cleaning rule; matches the lesson |
| research-int | homework-4.json | items[8].prose | Between neighbouring quoted seconds interpolate linearly in time; None if more than max_gap apart | misleading | The value at t reads the next quote, which arrives after t; the item never says the fill is for use after the fact (script check fails). Finding R2 |
| research-int | homework-4.json | items[8].prose | Before the first or after the last quoted second hold the end price up to max_gap away | correct | Rule as stated; the backward hold is covered by finding R2 |
| research-int | homework-4.json | items[8].prose | Each asked second must cost time in proportion to the log of the quote count | correct | Binary search on sorted seconds (CLRS sec. 2.3 exercise; bisect) |
| research-int | homework-4.json | items[8].widget.solution | Drops None, averages repeats, sorts, bisects; exact hit, ends held, gap test, linear formula | correct | script: passes all ten; an independent linear-scan version agrees |
| research-int | homework-4.json | items[8].widget.solution | y0 + (y1 - y0)(t - x0)/(x1 - x0) | correct | Linear interpolation formula |
| research-int | homework-4.json | items[8].widget.tests | Ten hidden tests; starter fails; big_case [9080, 3091996.9543693475] | correct | script |
| research-int | homework-4.json | items[8].widget.how | isclose at relative 1e-9; None must be None; 40,000 seconds of 40,000 quotes in 5 s | correct | Another correct summation order differs far below 1e-9 |
| research-int | homework-4.json | items[8].feedback.byKey.test-3 | Drop cancelled quotes before looking for neighbours; a cancelled price is not 0 | correct | Test 3 |
| research-int | homework-4.json | items[8].feedback.byKey.test-4 | Two quotes at second 10: their mean 102 stands | correct | (101 + 103)/2 |
| research-int | homework-4.json | items[8].feedback.byKey.test-6 | Neighbours exactly max_gap apart still interpolate; 61 apart do not | correct | Rule says "more than" |
| research-int | homework-4.json | items[8].feedback.byKey.test-9 | Three quotes at second 0 average to 102; a second asked twice is answered twice | correct | (100 + 101 + 105)/3 |
| research-int | homework-4.json | items[8].feedback.byKey.test-10 | Sort once and find each bracket by bisection | correct | O(log n) a query |
| research-int | homework-4.json | items[8].explain | Cleaning first leaves sorted seconds bisect can search; the bracket decides; answers go back in the order asked | correct | As the solution |
| research-int | review-1.json | timed.seconds | Timer 585 s | correct | Equals the sum of the ten paces |
| research-int | review-1.json | items[9].widget.answer | det(I + uu^T) = 26 for u = (2, 1, 2, 4) | correct | Matrix determinant lemma: 1 + u.u (Horn and Johnson sec. 0.8.5); script |
| research-int | review-1.json | items[9].widget.wrong[0] | Slip 25: u.u without the identity | correct | Eigenvalue of uu^T |
| research-int | review-1.json | items[9].widget.wrong[1] | Slip 29: the trace | correct | 4 + 25 |
| research-int | review-1.json | items[9].feedback.generic | Find the eigenvalues of uu^T, then add 1 to each | correct | Shift by the identity |
| research-int | review-1.json | items[9].explain | uu^T has rank one with eigenvalue 25 and three zeros; adding I gives 26, 1, 1, 1 | correct | Axler, Linear Algebra Done Right, ch. 5 |
| systems | homework-1.json | items[7].widget.model Predictor | The core reaches the branch before the comparison resolves, guesses from recent history, and discards the work on a wrong guess | correct | Hennessy and Patterson, Computer Architecture, sec. 3.3 |
| systems | homework-1.json | items[7].widget.model Cost | On random data no predictor beats 30% wrong at a 30% pass rate | correct | Bayes-optimal guess for i.i.d. outcomes is the majority class |
| systems | homework-1.json | items[7].widget.model Cost | 3,000,000 wrong guesses x 5 ns = 15 ms; rest 10 ms; branch is 60% of 25 ms | correct | script |
| systems | homework-1.json | items[7].widget.model Cost | A two-bit counter is wrong about 36% of the time, about 18 ms | correct | Stationary law of the 4-state chain: 0.3621; script simulation 0.362 |
| systems | homework-1.json | items[7].widget.model Rewrite | Store every price; add the comparison (1 or 0) to k; no jump | correct | bool converts to 0 or 1 (C++ [conv.prom]); script equivalence |
| systems | homework-1.json | items[7].widget.model Rewrite | out needs room for all n prices | correct | Highest store is index kept, unknown in advance, so n slots is the safe size; script |
| systems | homework-1.json | items[7].widget.model Rewrite | If the body stays near 1 ns the pass is 10 ms, not 25: 2.5 times faster | correct | Arithmetic under the stated assumption |
| systems | homework-1.json | items[7].widget.model No help | At 99% passing the branch costs 0.5 ms; sorted prices mislead about once | correct | script |
| systems | homework-1.json | items[7].widget.model No help | Then the unconditional store can cost more than the branch; measure both on real prices | correct | Practice; Agner Fog, Optimizing software in C++, sec. 7.12 |
| systems | homework-1.json | items[7].widget.model Follow-up 1 | Half pass: 25 ms, the worst case for random data | correct | min(p, 1 - p) peaks at 1/2 |
| systems | homework-1.json | items[7].widget.model Follow-up 2 | A running sum can become a conditional move; a compiler may not add a store the code does not make | correct | Speculative stores can write out of bounds or introduce data races (C++ [intro.races]; Boehm 2005) |
| systems | homework-1.json | items[7].widget.model Follow-up 3 | Time both loops many times on recorded prices; perf stat counts branch misses | correct | Practice |
| systems | homework-1.json | items[7].widget.rubric[0] | Required: guess before the comparison, from history; wrong guess about 5 ns; no guess beats 30% wrong | correct | Model; 5 ns is given in the prompt |
| systems | homework-1.json | items[7].widget.rubric[1] | Required: 15 ms against 10 ms | correct | script |
| systems | homework-1.json | items[7].widget.rubric[2] | Required: store every price, add the comparison, room for n | correct | Model |
| systems | homework-1.json | items[7].widget.rubric[3] | Optional: predictable data make the branch nearly free; measure | correct | Matches the optional prompt part |
| systems | homework-1.json | items[7].explain | At least 30% wrong: 15 ms of misses against 10 ms of work; on predictable data measure first | correct | As the model |
| systems | homework-3.json | items[7].widget.model Process | A process has its own address space and descriptor table; threads of one process share both | correct | Tanenbaum, Modern Operating Systems, sec. 2.1 and 2.2 |
| systems | homework-3.json | items[7].widget.model Process | So a pointer cannot be handed across, and the pipe copies bytes through the kernel | correct | pipe(7) |
| systems | homework-3.json | items[7].widget.model System call | The core enters the kernel and returns to the same thread; two per order, 0.4 us | correct | Round figure given; write plus read |
| systems | homework-3.json | items[7].widget.model Switch | A context switch changes which thread runs on a core | correct | Tanenbaum sec. 2.4 |
| systems | homework-3.json | items[7].widget.model Switch | Blocking read sleeps the sender (2), the write wakes it, scheduler (1), switch back (2): 5 us an order | correct | Model with the given figures; holds while orders are spaced wider than the handling time (50 us apart here) |
| systems | homework-3.json | items[7].widget.model Switch | Between processes the switch changes the address space; old TLB entries are no use, so first reads pay page walks | correct | Hennessy and Patterson app. B.4; qualified by follow-up 3 (tagged entries) |
| systems | homework-3.json | items[7].widget.model Per order | 5.4 us of core time; the order itself waits 1 + 2 = 3 us plus the two calls | correct | script |
| systems | homework-3.json | items[7].widget.model Per order | 20,000 x 5.4 = 108 ms a second, about 11% of a core; 93% of it is the wake | correct | script |
| systems | homework-3.json | items[7].widget.model Fix | Shared memory or threads, a queue in that memory, sender spinning on its own core: no call, no switch | correct | Standard low-latency design (LMAX Disruptor paper, 2011) |
| systems | homework-3.json | items[7].widget.model Fix | The price is a core kept 100% busy; measure the gain | correct | Busy polling |
| systems | homework-3.json | items[7].widget.model Follow-up 1 | Two threads with the pipe still pay two calls and a wake; only the address-space change goes | correct | Same kernel path |
| systems | homework-3.json | items[7].widget.model Follow-up 2 | Spinning saves 108 ms of core time a second and about 3.4 us of waiting per order | correct | script |
| systems | homework-3.json | items[7].widget.model Follow-up 3 | Untagged TLB entries are flushed on the switch; tagged ones may have been pushed out | correct | x86 PCID / ARM ASID; Intel SDM vol. 3, sec. 4.10 |
| systems | homework-3.json | items[7].widget.rubric[0] | Required: own address space and descriptor table, shared by threads; pipe copies through the kernel | correct | Model |
| systems | homework-3.json | items[7].widget.rubric[1] | Required: enters the kernel, same thread, 0.2 us; two per order | correct | Model |
| systems | homework-3.json | items[7].widget.rubric[2] | Required: wake 2 + 1 + 2 = 5; 5.4 us; 108 ms; 11% | correct | script |
| systems | homework-3.json | items[7].widget.rubric[3] | Optional: kernel off the path, shared memory, polling, busy core, measure | correct | Matches the optional prompt part |
| systems | homework-3.json | items[7].explain | Two calls 0.4 us and a wake 5 us; 108 ms a second; a shared queue with a spinning sender removes both | correct | As the model |
| systems | homework-4.json | items[6].prose | Single producer calls only try_push; consumer calls only try_pop, drain and size | correct | SPSC contract; makes size safe, as only the consumer moves head_ |
| systems | homework-4.json | items[6].prose | N must be a power of two; TickRing<6> must fail to compile | correct | static_assert; script compile test |
| systems | homework-4.json | items[6].prose | head_ and tail_ only grow and may wrap past 4,294,967,295 | correct | Unsigned arithmetic is modular (C++ [basic.fundamental]); script wrap test |
| systems | homework-4.json | items[6].prose | head_ and tail_ sit on different 64-byte cache lines | correct | False sharing; Herlihy and Shavit, Art of Multiprocessor Programming, app. B; script layout |
| systems | homework-4.json | items[6].widget.solution | Producer: tail relaxed (its own), head acquire, full when t - h == N, write slot, store tail release | correct | Lamport queue with C++11 orders; Williams, C++ Concurrency in Action, sec. 5.3 and 7.2 |
| systems | homework-4.json | items[6].widget.solution | Consumer: head relaxed, tail acquire, empty when h == t, read slot, store head release | correct | As above; out untouched when empty |
| systems | homework-4.json | items[6].widget.solution | drain: one acquire, copy up to max, one release | correct | Batch pop; slots stay owned by the consumer until head_ is stored |
| systems | homework-4.json | items[6].widget.solution | No data race and no undefined behaviour | correct | Each slot access is ordered by a release/acquire pair; script: ThreadSanitizer clean, 2,000,000-tick stress across the wrap in order |
| systems | homework-4.json | items[6].widget.solution | alignas(64) on both counters and the buffer; no heap | correct | script: offsets 64 apart, alloc count 0 |
| systems | homework-4.json | items[6].widget.tests | Twelve hidden tests; solution passes all under g++ 13; starter fails | correct | script (starter passes only the empty-pop, alloc and nothing else) |
| systems | homework-4.json | items[6].widget.tests | Addresses 64 or more bytes apart imply different 64-byte lines | correct | Two bytes in one line differ by at most 63 |
| systems | homework-4.json | items[6].widget.how | One thread cannot check the memory orders; twelve tests listed | correct | Count is 12; stated honestly |
| systems | homework-4.json | items[6].feedback.correct | Growing counters, a mask for the slot, each counter on its own line | correct | As the solution |
| systems | homework-4.json | items[6].feedback.correct | Check your loads and stores against the explain | imprecise | The explain gives the tail_ pair only; the head_ pair (consumer release, producer acquire) is not there to check against. Finding S1 |
| systems | homework-4.json | items[6].explain | tail_ - head_ is the count even after a wrap: unsigned subtraction is exact modulo 2^32 | correct | Modular arithmetic; 32-bit unsigned on the target; script |
| systems | homework-4.json | items[6].explain | The masked slot stays in order across the wrap because N divides 2^32 | correct | script |
| systems | homework-4.json | items[6].explain | Producer stores tail_ with release after writing; consumer loads with acquire before reading, so no tick is read half-written | correct | C++ [atomics.order]: release/acquire gives happens-before |
| systems | review-1.json | items[9].prose | Random bytes make the guess wrong half the time | correct | Stated as the item's premise for a 50/50 branch |
| systems | review-1.json | items[9].widget.answer | Wrong guesses use 10% of the 5 us budget | correct | 200 x 0.5 x 5 ns = 500 ns; script |
| systems | review-1.json | items[9].widget.wrong | Slips 20 (all 200 charged) and 0.1 (a fraction, not a percentage) | correct | script |
| systems | review-1.json | items[9].feedback.generic | Extra time is n x p_wrong x 5 ns | correct | Expected misses |
| systems | review-1.json | items[9].explain | 100 wrong guesses, 500 ns of 5,000 ns | correct | script |
| systems | review-2.json | items[9].widget.answer | Producer first blocks after 12 ms | correct | 600/(250,000 - 200,000) s; script |
| systems | review-2.json | items[9].widget.wrong | Slips 2.4 (no consumer) and 3 (consumer rate) | correct | script |
| systems | review-2.json | items[9].feedback.generic | The queue grows at the difference of the two rates | correct | Fluid model |
| systems | review-2.json | items[9].explain | 50,000 a second net; 600/50,000 = 0.012 s | correct | script |
| systems | review-3.json | items[9].widget.answer | Price starts at offset 13 | correct | 1 + 4 + 8; script |
| systems | review-3.json | items[9].widget.wrong[0] | Slip 16: host struct with natural alignment | correct | seq at 4, id at 8, price at 16 (System V x86-64 ABI sec. 3.1.2); script |
| systems | review-3.json | items[9].widget.wrong[1] | Slip 14: counted from 1 | correct | Offsets count from 0, as stated |
| systems | review-3.json | items[9].explain | A host struct would pad it to 16, which is why the frame is written byte by byte | correct | Padding differs from the wire layout |
| systems | review-4.json | items[9].widget.answer | 200 messages wait at the end of the burst | correct | 1,000 arrive, 2,000/2.5 = 800 handled; script |
| systems | review-4.json | items[9].widget.wrong | Slips 1,000 (every arrival) and 800 (the number handled) | correct | script |
| systems | review-4.json | items[9].feedback.generic | Count the arrivals, then the messages handled in the same 2 ms | correct | Fluid model |
| systems | review-4.json | items[9].explain | Backlog grows by 100 for every millisecond of burst | correct | 500 - 400 a millisecond |
| ito | homework-2.json | items[7].model step 2 (display edit) | The aligned display states the same result: d(ln S) = dS/S - sigma^2 dt/2 = (mu - sigma^2/2) dt + sigma dW | correct | Layout only; Shreve, Stochastic Calculus for Finance II, sec. 4.4.3 |
| ito | homework-2.json | items[7].model steps 3 to 6 | Unchanged text: (dS)^2 = sigma^2 S^2 dt; gap about sigma^2 T/2 on every path; median growth mu - sigma^2/2 | correct | script MC: gap 0.02 at 252 and 4,032 steps, small spread |
| ito | homework-2.json | items[8].prompt (edit) | The check on e^{x - t/2} becomes optional | correct | A derivation is complete without the worked check; rubric[4] carries the point and is not required |
| ito | homework-2.json | items[8].rubric[0].required | Now required: a and b adapted, integrable; f in C^{1,2} | correct | The prompt asks for these; hypotheses of Ito's formula (Shreve II Th. 4.4.6; Karatzas and Shreve Th. 3.3.3) |
| ito | homework-2.json | items[8].rubric[1].required | Now required: second-order Taylor in x, (dX)^2 kept because dW is of size sqrt(dt) | correct | Core step of the heuristic derivation |
| ito | homework-2.json | items[8].model Setting | dX shorthand for the integral form; a, b adapted with integrals of /a/ and b^2 finite a.s.; f in C^{1,2} | correct | Definition of an Ito process (Shreve II Def. 4.4.3) |
| ito | homework-2.json | items[8].model step 3 | Weighted sums of (dW)^2 - dt have mean 0 and variance at most 2 sup g^2 t dt after stopping | correct | Var((dW)^2) = 2 dt^2; orthogonal increments; script MC |
| ito | homework-2.json | items[8].model step 4 | Sum of dt dW is at most t max/dW/ -> 0; sum of dt^2 = t dt -> 0 | correct | Uniform continuity of the path |
| ito | homework-2.json | items[8].model step 5 | df = (f_t + a f_x + b^2 f_xx/2) dt + b f_x dW | correct | Ito's formula (Shreve II Th. 4.4.6) |
| ito | homework-2.json | items[8].model Caution | The dW integral is a local martingale; mean zero when E of the integral of b^2 f_x^2 is finite | correct | Shreve II Th. 4.3.1; Karatzas and Shreve sec. 3.2 |
| ito | homework-2.json | items[8].model Check | d e^{W - t/2} = e^{W - t/2} dW; mean 1; E of the integral of e^{2W_s - s} is e^t - 1 | correct | script MC and quadrature |
| ito | homework-3.json | items[7].prompt | F_t = S_t e^{r(T_F - t)} for a share with no dividends and constant r | correct | Hull, Options, Futures and Other Derivatives, sec. 5.4 |
| ito | homework-3.json | items[7].model Assumptions | GBM, no dividends, constant r with borrowing, continuous costless trading, European claim, V smooth, no arbitrage | correct | Black-Scholes assumptions (Hull sec. 15.5) |
| ito | homework-3.json | items[7].model step 1 | f_t = -r f, f_s = e^{r(T_F - t)}, f_ss = 0; dF = (mu - r) F dt + sigma F dW | correct | Ito on a function linear in s; Hull sec. 18.6 |
| ito | homework-3.json | items[7].model step 1 | No Ito correction because f is linear in s; (dF)^2 = sigma^2 F^2 dt | correct | f_ss = 0 |
| ito | homework-3.json | items[7].model step 2 | dV = (V_t + (mu - r) F V_F + sigma^2 F^2 V_FF/2) dt + sigma F V_F dW | correct | Ito's formula |
| ito | homework-3.json | items[7].model step 3 | Book -V + Delta S; dW coefficient sigma(Delta S - F V_F); Delta = e^{r(T_F - t)} V_F | correct | script MC: this hedge replicates a Black-76 call under an 11% drift |
| ito | homework-3.json | items[7].model step 3 | Delta held fixed over each step, so dPi = -dV + Delta dS | correct | Self-financing convention of the standard derivation (Hull sec. 15.6) |
| ito | homework-3.json | items[7].model step 3 | r = 4%, 1.5 years to delivery: e^{0.06} = 1.0618 V_F shares | correct | script |
| ito | homework-3.json | items[7].model step 4 | The mu terms cancel; dPi = (-V_t - sigma^2 F^2 V_FF/2 + r F V_F) dt | correct | -(mu - r) F V_F + mu F V_F = r F V_F |
| ito | homework-3.json | items[7].model step 5 | A riskless book earns r, or borrowing or selling it is an arbitrage; dPi = r(-V + F V_F) dt | correct | No-arbitrage argument (Hull sec. 15.6) |
| ito | homework-3.json | items[7].model step 5 | With the cash C = V - Delta S in the book it costs nothing and its dt term is zero: the same equation | correct | Equivalent zero-cost form |
| ito | homework-3.json | items[7].model step 6 | V_t + sigma^2 F^2 V_FF/2 - rV = 0 with V(T, F) = g(F) | correct | Black (1976); Hull sec. 18.7; script: Black-76 call solves it numerically |
| ito | homework-3.json | items[7].model step 6 | No first-derivative term because the forward price drifts at r - r = 0 under the risk-neutral measure | correct | Hull sec. 18.6 |
| ito | homework-3.json | items[7].model step 7 | Claim paying F_T - K is worth e^{-r(T - t)}(F - K); V_t = rV, V_FF = 0 | correct | Static replication; script |
| ito | homework-3.json | items[7].model step 8 | U(t, S) = V(t, S e^{r(T_F - t)}): U_t = V_t - r F V_F, S U_S = F V_F, S^2 U_SS = F^2 V_FF; Black-Scholes operator reduces to the forward one | correct | Ordinary chain rule on a deterministic change of variables |
| ito | homework-3.json | items[7].rubric[0] | Required: all assumptions | correct | The prompt asks for each assumption |
| ito | homework-3.json | items[7].rubric[1] | Required: dF by Ito with f_t = -rf, f_ss = 0; dV with the V_FF term | correct | Steps 1, 2 |
| ito | homework-3.json | items[7].rubric[2] | Required: Delta = e^{r(T_F - t)} V_F, mu cancels, riskless book earns r | correct | Steps 3 to 5 |
| ito | homework-3.json | items[7].rubric[3] | Required: the equation with terminal condition; r F V_F terms cancel | correct | Step 6 |
| ito | homework-3.json | items[7].rubric[4] | Optional: a check, forward claim or substitution | correct | Steps 7, 8 |
| measure-prob | homework-1.json | items[8].model Space | All subsets of the positive integers form a sigma-algebra | correct | Power set; Billingsley, Probability and Measure, sec. 2 |
| measure-prob | homework-1.json | items[8].model Space | A non-negative sum over a countable set is the supremum of finite partial sums, in [0, inf], order-free | correct | Rudin, Principles, Th. 3.55 context; Folland sec. 0.5 |
| measure-prob | homework-1.json | items[8].model Total mass | p_k = 1/k - 1/(k + 1); partial sums 1 - 1/(m + 1) rise to 1 | correct | script exact |
| measure-prob | homework-1.json | items[8].model Additivity | s <= t: a finite F in A meets finitely many A_j | correct | F is finite and the A_j are disjoint |
| measure-prob | homework-1.json | items[8].model Additivity | t <= s: finite F_j in A_j are disjoint subsets of A; suprema over each F_j then over J | correct | Supremum of a finite sum over independent choices is the sum of suprema |
| measure-prob | homework-1.json | items[8].model From below | No finiteness needed; B_n = A_n minus A_{n-1} are disjoint with union A and A_n = B_1 u ... u B_n | correct | Billingsley Th. 10.2(i); Williams, Probability with Martingales, 1.10 |
| measure-prob | homework-1.json | items[8].model From below | Finite additivity is countable additivity with empty sets added | correct | Uses mu(empty) = 0 |
| measure-prob | homework-1.json | items[8].model From above | Needs mu(A_1) finite; C_n = A_1 minus A_n increase to A_1 minus A; subtract finite terms | correct | Billingsley Th. 10.2(ii) |
| measure-prob | homework-1.json | items[8].model From above | Without it mu(A_1) - mu(A_n) could be inf - inf; some finite mu(A_m) is enough; always holds for a probability | correct | Counter-example: counting measure on tails of the integers |
| measure-prob | homework-1.json | items[8].model Our space | P({n, n+1, ...}) = 1/n by complement and by continuity from below; tails decrease to the empty set, limit 0 | correct | script exact |
| measure-prob | homework-1.json | items[8].rubric[0] | Required: Omega, all subsets with a reason, P(A) as a sum, P(Omega) = 1 by telescoping | correct | Model |
| measure-prob | homework-1.json | items[8].rubric[1] | Required: countable additivity of P through finite partial sums | correct | Model |
| measure-prob | homework-1.json | items[8].rubric[2] | Required: continuity from below by disjoint slices | correct | Standard proof |
| measure-prob | homework-1.json | items[8].rubric[3] | Required: the finiteness hypothesis and the subtraction that needs it | correct | The dropped-hypothesis check; correct |
| measure-prob | homework-1.json | items[8].rubric[4] | Optional: P(tail) = 1/n and the limit 0 | correct | Matches the optional prompt part |
| measure-prob | homework-2.json | items[9].model Simple | phi_n = floor(NX)/N with N = 2^n takes values k/N, k = 0..N | correct | 0 <= X <= 1 |
| measure-prob | homework-2.json | items[9].model Simple | {phi_n = k/N} = {k^2/N^2 <= U < (k+1)^2/N^2}, an interval of chance (2k + 1)/N^2 | correct | Squaring preserves order on [0, inf); uniform law |
| measure-prob | homework-2.json | items[9].model Simple | The value 1 is taken only on {U = 1}, of chance 0 | correct | Single point under a uniform law |
| measure-prob | homework-2.json | items[9].model Below | 0 <= phi_n <= X < phi_n + 1/N, so phi_n -> X at every outcome | correct | Floor inequality; script MC |
| measure-prob | homework-2.json | items[9].model Below | 2 floor(NX) <= floor(2NX), so phi_n <= phi_{n+1} | correct | An integer at most 2NX is at most its floor; script MC |
| measure-prob | homework-2.json | items[9].model Means | E[phi_n] = (N - 1)(4N + 1)/(6N^2); 3/8 at n = 1 (1/2 x 3/4); 231/384 = 0.6016 at n = 3 | correct | script exact fractions |
| measure-prob | homework-2.json | items[9].model Limit | E[X] is the supremum over simple functions below X, so E[phi_n] <= E[X] | correct | Definition (Williams 5.2; Billingsley sec. 15) |
| measure-prob | homework-2.json | items[9].model Limit | Monotone convergence needs 0 <= phi_1 <= phi_2 <= ... and phi_n -> X a.s.; gives E[phi_n] up to E[X] = 2/3 | correct | Monotone convergence theorem (Williams 5.3); hypotheses checked |
| measure-prob | homework-2.json | items[9].model Limit | Shortfall (3N + 1)/(6N^2), about 2^{-n-1} | correct | script exact |
| measure-prob | homework-2.json | items[9].model Limit | Layer cake: P(X > t) = 1 - t^2, integral 2/3 | correct | E[X] = integral of P(X > t) for X >= 0 (Billingsley eq. 21.9) |
| measure-prob | homework-2.json | items[9].model Both signs | E[Y] = E[Y+] - E[Y-] unless both are infinite; both lie in [0, 1] here | correct | Definition (Williams 5.4) |
| measure-prob | homework-2.json | items[9].model Both signs | E[Y+] = 5/12, E[Y-] = 1/12, E[Y] = 1/3 = 2 x 2/3 - 1 | correct | script MC; integrals of 1 - (1 + t)^2/4 and (1 - t)^2/4 |
| measure-prob | homework-2.json | items[9].rubric[0] | Required: simple functions below X, each value on an interval with its chance | correct | "such as" admits other choices |
| measure-prob | homework-2.json | items[9].rubric[1] | Required: 0 <= phi_n <= X, increasing, convergent | correct | Model |
| measure-prob | homework-2.json | items[9].rubric[2] | Required: exact mean, (N - 1)(4N + 1)/(6N^2) for the dyadic choice | correct | Other choices allowed by the wording |
| measure-prob | homework-2.json | items[9].rubric[3] | Required: supremum bound, monotone convergence with hypotheses, limit 2/3 | correct | Model |
| measure-prob | homework-2.json | items[9].rubric[4] | Optional: E[Y] = 5/12 - 1/12 = 1/3 with finiteness | correct | Model |
| measure-prob | homework-3.json | items[8].model Setting | R_0 = 1, R_{n+1} = R_n + D_{n+1}; n + 2 balls after n draws | correct | Polya urn |
| measure-prob | homework-3.json | items[8].model Setting | F_n has one atom per string of n colours, each of positive chance | correct | Both colours stay in the urn |
| measure-prob | homework-3.json | items[8].model Adapted | R_n and M_n are functions of the first n draws, so constant on atoms | correct | Measurability for a finite sigma-algebra |
| measure-prob | homework-3.json | items[8].model Integrable | 1 <= R_n <= n + 1, so 0 < M_n < 1 | correct | script exact |
| measure-prob | homework-3.json | items[8].model Next draw | P(D_{n+1} = 1 / A) = R_n/(n + 2) on each atom; conditional expectation given a finite sigma-algebra is the atom average | correct | Williams 9.1 to 9.2 |
| measure-prob | homework-3.json | items[8].model Next draw | The next draw is not independent of the past | correct | Its chance depends on R_n |
| measure-prob | homework-3.json | items[8].model Step | E[M_{n+1} / F_n] = (R_n + M_n)/(n + 3) = M_n | correct | Linearity, taking out what is known; script exact on every atom to n = 8 |
| measure-prob | homework-3.json | items[8].model Check | After red, red: 3/4 x 4/5 + 1/4 x 3/5 = 3/4 | correct | script |
| measure-prob | homework-3.json | items[8].model Consequences | E[M_n] = 1/2 for every n by the tower property; draw n + 1 is red with chance 1/2 | correct | script exact to n = 9 |
| measure-prob | homework-3.json | items[8].model Consequences | E[R_{n+1} / F_n] = R_n + M_n > R_n, so R_n is not a martingale | correct | A submartingale; script |
| measure-prob | homework-3.json | items[8].rubric[0] | Required: recursion and the conditional chance, with the atom reason | correct | Model |
| measure-prob | homework-3.json | items[8].rubric[1] | Required: adapted and integrable with reasons | correct | Definition of a martingale (Williams 10.3) |
| measure-prob | homework-3.json | items[8].rubric[2] | Required: the conditional step line by line, not by independence | correct | Model |
| measure-prob | homework-3.json | items[8].rubric[3] | Required: finds E[M_n] = 1/2 by the tower property, so the draw is red with chance 1/2 | imprecise | The 1/2 also follows from the symmetry of the two colours, a complete argument the row would not credit. Finding M1 |
| measure-prob | homework-3.json | items[8].rubric[4] | Optional: R_n is not a martingale | correct | Model |

# Claim ledger: contests level 4 (blind concept audit, round 1)

Files: `app/content/courses/contests/` l13-virtual-contest, l14-which-first, l15-debugging-under-time, l16-upsolving, review-4, homework-4. Script: `docs/reports/contests-L4-concepts.py` (`sim:` rows name the check; part A runs every solution and starter, part B every `test-N` line as a real submission, part C the numbers, part D the solutions in Pyodide 0.27.7). Sources: Laaksonen = *Competitive Programmer's Handbook*; CLRS = Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* 3e; Pinedo = *Scheduling: Theory, Algorithms and Systems* (Smith's rule, weighted completion time, section 3.1); Python docs = `sys.setrecursionlimit`, `sorted`; ICPC = ICPC regional rules (ECNA "Official Rules": solved count, then penalty minutes; 20 per rejected run on a solved problem only) and World Finals judging notes; engine = `app/js/engine/widgets/code.js` and `app/js/screens/drill-worker.js`; curriculum = `docs/curriculum.md` section 2.4. "F n" points at finding n of `docs/reviews/audit-contests-4.md`.

Every row was judged by hand. Verdict counts are at the foot.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l13 | screens[0].prose | A virtual contest of four problems in 60 minutes; the player has no clock, so the timer is kept outside the app | correct | engine: no lesson timer in the code widget; course convention |
| l13 | screens[0].question, answer | Problem C (smallest van for k days) is the binary search on the answer | correct | Laaksonen 3.3; monotone predicate, sim: C hw/l13 C |
| l13 | screens[0].hints[1], hints[2], feedback.correct | A bigger van works if a smaller one does; that monotone shape is what binary search on the answer needs | correct | if capacity c ships in k days, the same day plan is legal for c + 1 |
| l13 | screens[0].feedback.byKey.l2 | A (peaks) is one pass over the closes | correct | sim: A l13 A peaks |
| l13 | screens[0].feedback.byKey.l3 | B (shortest run holding every name) is a sliding window | correct | Laaksonen 8.1 (two pointers); sim: A l13 B |
| l13 | screens[0].feedback.byKey.l5 | D (fewest unit moves on a grid) is a BFS | correct | CLRS 22.2: BFS gives shortest paths in unweighted graphs |
| l13 | screens[0].feedback.byKey.l1 | Line 1 is the header | correct | canvas line 1 |
| l13 | screens[0].explain | Naming the patterns: loop, window, binary search on the answer, BFS | correct | as the four rows above |
| l13 | screens[1].canvas A | Peak: 1 < i < n and strictly above both neighbours; example 3 5 4 6 2 gives 2 | correct | sim: C l13 A example |
| l13 | screens[1].canvas B | Example AAA BBB AAA CCC BBB with BBB CCC gives 2 | correct | CCC BBB; sim: A l13 B (test 1) |
| l13 | screens[1].canvas C | Example 4 8 2 7 5 3, k = 3 gives 12 | correct | 4+8, 2+7, 5+3; 11 needs four days; sim: A l13 C (tests 1 to 3) |
| l13 | screens[1].canvas D | One-way cells are left only their way and may be entered from any side | correct | matches the solution's move rule; sim: A l13 D |
| l13 | screens[1].question, answer, accept | 5 1 5 has 0 peaks | correct | day 2 is a dip, ends excluded |
| l13 | screens[1].wrong ends = 2, byKey.ends | Counting both ends gives 2; the note excludes ends | correct | 5 > 1 on each side |
| l13 | screens[1].wrong valley = 1, byKey.valley | Counting day 2 gives 1; 1 is below 5 on both sides | correct | arithmetic |
| l13 | screens[1].hints | Only day 2 could be a peak | correct | 1 < i < 3 |
| l13 | screens[1].explain | The rule and the note both exclude the ends; reading it saves a wrong answer on test 3 | correct | sim: B l13 A "counts the last day" first fails at test-3 |
| l13 | screens[1].explain | "Every statement has a line like it" | imprecise | F 14: an "every" that is false as stated; problems B and C of this very round carry no such note |
| l13 | screens[2].prose | Virtual contest: a past round, alone, at full length | correct | definition; Codeforces "virtual participation" |
| l13 | screens[2].prose | Codeforces calls it virtual participation and shows the scoreboard as it stood | unverified | name is Codeforces' own; the "as it stood" scoreboard rests on community posts (ghost participants), no official page fetched |
| l13 | screens[2].prose | The curriculum asks for one contest a week | correct | curriculum 2.4 line "enter one contest a week" |
| l13 | screens[2].options tests.why | Each code screen runs hidden tests, as a judge does | correct | engine: widget.tests |
| l13 | screens[2].options statements.why, rating.why | Statements are on the previous screen; ratings run from about 800 to about 1500 | correct | screens[1]; `how` texts of screens[3] to [6] |
| l13 | screens[2].hints, feedback, explain | Only the clock is missing; a lesson lets you take as long as you like | correct | engine: no round timer |
| l13 | screens[3].prose, how | Problem A is about 800 on Codeforces' scale | unverified | author's estimate; plausible for a one-pass problem |
| l13 | screens[3].solution, tests | `peaks` passes 10 tests; starter fails | correct | sim: A l13 A peaks |
| l13 | screens[3].how | Test list: example, n = 1, n = 2, dip, flat, plateau; tests 9 and 10 are 200,000 closes | correct | read against tests |
| l13 | screens[3].hints | Loop i from 1 to n - 2, compare both neighbours | correct | the solution |
| l13 | screens[3].feedback.byKey.test-2 | Single close: `range(1, 0)` is empty, so 0 without a special case | correct | sim: B "reads closes[1] before the loop" first fails at test-2 |
| l13 | screens[3].feedback.byKey.test-3 | 4 9: the last day is never a peak | correct | sim: B "counts the last day" first fails at test-3 |
| l13 | screens[3].feedback.byKey.test-4 | 5 1 5: ends are not peaks | correct | sim: B "counts the first day" first fails at test-4 |
| l13 | screens[3].feedback.byKey.test-6 | Plateau 1 3 3 1: neither 3 is strictly above both | correct | sim: B ">= on one side only" first fails at test-6 |
| l13 | screens[3].explain | "The plateau test catches a `>=` slip" | imprecise | F 1: `>=` on both sides stops at test 5 (flat closes), which has no line; sim: FINDING 1 |
| l13 | screens[4].prose | Problem B is about 1100; at n = 2·10^5 a restart at every trade is too slow | correct | O(n^2) worst case; rating is an estimate |
| l13 | screens[4].solution, tests | `shortest_cover` passes 9 tests; starter fails | correct | sim: A l13 B |
| l13 | screens[4].how | ZZZ only as the last trade; test 8 allows 4n reads of a 2,000-trade tape | correct | prelude `_tape`; 8000 = 4 × 2000 |
| l13 | screens[4].hints[2], feedback.correct | Each trade enters and leaves the window once: O(n) | correct | Laaksonen 8.1; amortised two-pointer argument |
| l13 | screens[4].feedback.byKey.test-3 | A name that never trades: return -1 | correct | sim: B "returns infinity" first fails at test-3 |
| l13 | screens[4].feedback.byKey.test-5 | BBB listed twice: use `set(needed)` | correct | sim: B "len(needed)" first fails at test-5 |
| l13 | screens[4].feedback.byKey.test-8 | A restart at every left end rereads the tape | correct | sim: B "restart at every left end" first fails at test-8 |
| l13 | screens[4].feedback.byKey.test-9 | A restart is O(n^2) on 200,000 trades because ZZZ is last | correct | sim: B "restart ... on a plain copy" first fails at test-9 (5 s limit) |
| l13 | screens[4].explain | The left end never moves back, so O(n); a restart is about 2·10^10 steps on test 9 | correct | n(n+1)/2 = 2.00001·10^10; sim: C l13 B |
| l13 | screens[5].prose | C about 1300; search between the heaviest order and the total; must call `can_ship` | correct | the bounds are right (sim: C l13 C test 10); the "must call" instruction is sound but not enforced: an inline check makes 0 calls and passes test 10 (Inbox 1) |
| l13 | screens[5].solution, tests | Both functions pass 11 tests; starter fails | correct | sim: A l13 C |
| l13 | screens[5].how | Test 10: 40 orders, total 1,807, 13 calls allowed; test 11: 100,000 orders, k = 500 | correct | sim: C l13 C test 10 |
| l13 | screens[5].hints | Monotone in capacity; greedy fills each day until the next order would overflow; lo = max, hi = sum | correct | exchange argument for the greedy: shipping an order earlier never needs more days |
| l13 | screens[5].feedback.correct | About log2(total) checks | correct | 11 at 1,807; 30 at 10^9 |
| l13 | screens[5].feedback.byKey.test-2 | 11 needs four days: 4, then 8 and 2, then 7, then 5 and 3 | correct | hand trace; sim: B "can_ship left unwritten" first fails at test-2 |
| l13 | screens[5].feedback.byKey.test-4 | An order of 5 and a van of 4: return False | correct | sim: B "an order heavier than the van rides alone" first fails at test-4; a greedy with no explicit test still passes (B l13 C) |
| l13 | screens[5].feedback.byKey.test-10 | More than 13 calls: halve the range | correct | sim: B "scan capacities upwards" first fails at test-10 |
| l13 | screens[5].feedback.byKey.test-11 | Checks must be about 30, not a million | correct | sim: B "scan upwards with an inline check" first fails at test-11; C l13 C test 11 |
| l13 | screens[5].explain | Answer between heaviest and total; about 30 checks at n = 10^5; test 10 used 11 against about 811 for a scan from 99 | correct | sim: C l13 C test 10 (11 calls, 909 - 99 + 1 = 811) |
| l13 | screens[6].prose, canvas | D about 1500; the example grid gives 11 | correct | sim: C l13 D example |
| l13 | screens[6].solution, tests | `grid_moves` passes 9 tests; starter fails | correct | sim: A l13 D |
| l13 | screens[6].hints | Unit moves: BFS with a distance per cell; an arrow offers one move | correct | CLRS 22.2 |
| l13 | screens[6].feedback.byKey.test-1 | Ignoring arrows gives 7, through the dead end at the `v` | correct | sim: B "ignores the arrows" first fails at test-1; C l13 D |
| l13 | screens[6].feedback.byKey.test-2 | Both of the start's neighbours are arrows that lead out of the grid: -1 | correct | `>` at (0,1) and `v` at (1,0); descriptive line, names no slip |
| l13 | screens[6].feedback.byKey.test-3 | One cell: 0 moves | correct | sim: B "checks for the target only when pushing" first fails at test-3 |
| l13 | screens[6].feedback.byKey.test-9 | 200,000 cells: a search that revisits cells cannot finish | correct | sim: B "a queue with no visited marks" first fails at test-9 |
| l13 | screens[6].explain | Each cell once, at most four moves: O(rc); the courier detours through the `>` in row 2 | correct | path traced: 11 moves via (2,3) of the grid, 1-indexed row 2 |
| l13 | screens[7].canvas, options, hints | Sam: second wrong answer 13 minutes after the first; A took seven minutes; D 52 | correct | sim: C l13 Sam |
| l13 | screens[7].options hard.why, summary.trap | The hardest problem's time is the most uncertain, so it can take the hour | correct | reasoning, not a theorem; consistent with l14's rate rule |
| l13 | screens[7].options c.why | C is quicker than D, but A and B are quicker still | correct | the round's ratings 800 to 1500 |
| l13 | screens[7].explain | 52 minutes on D scored nothing; with A, B, C first D gets what is left | correct | arithmetic on the log |
| l13 | screens[8].widget, hints, feedback | Totals 16, 27, 17, adding to 60 | correct | sim: C l13 Alex log totals |
| l13 | screens[8].explain | Debugging 17 minutes, 12 on C | correct | table row C |
| l13 | screens[9].prose | Routine: read all, name patterns, order of ease, 15-minute cap, log | correct | course convention, used the same way in l14 and homework-4 |
| l13 | screens[9].options, explain | Reading first chooses the order; letters only roughly follow difficulty | correct | l14 screens[8] makes the same point with solve counts |
| l13 | screens[10].prose, options | Assessment: 1, 2, then 3 with a 15-minute cap | correct | the routine applied |
| l13 | screens[10].options three | "3 first, since it carries the most marks" | correct | a distractor: its premise (most marks) is the learner's own, and the why and byKey.three answer it (hardest first, uncertain time) |
| l13 | screens[10].options all.why | Partial code passes no hidden tests | correct | unfinished code does not run |
| l13 | screens[10].options skip | Four minutes is a sixth of a problem's time | correct | 75 / 3 = 25; 4 / 25 = 0.16; sim: C l13 transfer |
| l13 | screens[10].feedback.byKey.three, explain | An assessment scores solved problems; scored by what passes | correct | true of the scenario ("graded on hidden tests"); "scored by what passes" also covers platforms that score per test |
| l13 | summary.ideas | Virtual contest; read constraints first; log minutes | correct | as rows above |
| l13 | summary.formula | checks ≈ log2(sum - max); each check O(n) | correct | sim: C l13 summary formula |
| l13 | quiz[0] | About 30 checks since 2^30 > 10^9; 3·10^6 steps | correct | sim: C l13 quiz |
| l13 | quiz[0].options n.why, billion.why | The search halves capacities, not orders; a scan is one check per capacity | correct | definition of the search |
| l13 | quiz[1] | Shortest run holding AAA, BBB, CCC is 3 (trades 2 to 4 or 3 to 5) | correct | sim: A l13 B (test 2) |
| l13 | quiz[1].byKey | The whole tape is 5; two trades hold only two names | correct | pigeonhole |
| l13 | quiz[2] | 2 2 3 3 2 has no peak | correct | each 3 has an equal neighbour |
| l13 | quiz[3] | `.>` over `v.` returns -1 | correct | sim: C l13 D quiz |
| l14 | screens[0].prose | Rule: lose v/250 a minute until solved, 50 per rejected attempt, floor 0.3v | correct | the course's stated rule; used consistently in l14, review-4 |
| l14 | screens[0].prose | "This course's illustration, not Codeforces' current rule" | unverified | v/250 a minute for a two-hour round matches Codeforces' published decay (blog entry 133094, by search); the 50 and 30% were not confirmed from an official page |
| l14 | screens[0].canvas | Lost per minute 2, 4, 6, 8 | correct | v / 250 |
| l14 | screens[0].answer, same | A B C D, with A and B in either order | correct | sim: C l14 3,550 is the best of all 24 orders, reached by ABCD and BACD only |
| l14 | screens[0].hints, explain | Rates 50, 50, about 43, 40; best rate first makes the slow problem wait | correct | sim: C l14 rates |
| l14 | screens[1].canvas | Three orders score 3,550, 3,440, 3,520 with the bars shown | correct | sim: C l14 A B C D / D C B A / C A B D |
| l14 | screens[1].byKey.hard, cabd | Hardest first: D gains, the rest lose more; C first makes A and B wait 35 minutes | correct | sim: C l14 hardest first |
| l14 | screens[1].explain | D rises 1,080 to 1,600, the others drop 630; easy first loses the fewest | correct | sim: C l14 hardest first; best of 24 |
| l14 | screens[2].prose | Points per minute: value over estimated solving time, largest first | correct | Smith's ratio rule with weight v/250: Pinedo 3.1; sim: C l14 points-per-minute order loses the fewest |
| l14 | screens[2].widget | C 42.857, D 40 | correct | 1500 / 35, 2000 / 50 |
| l14 | screens[2].explain | Rates fall from A to D here; estimates, so a wrong estimate changes the order | correct | 50, 50, 42.9, 40 |
| l14 | screens[3] | B at minute 35 with one rejection scores 810; slips 860, 300, 760 | correct | sim: C l14 B at minute 35 |
| l14 | screens[3].explain | The 30% floor matters only for a problem solved very late | correct | with no rejections the floor binds from minute 175 of 120; with rejections sooner (test 2) |
| l14 | screens[4].solution, tests | `decayed_score` passes 8 tests; starter fails | correct | sim: A l14 decayed_score |
| l14 | screens[4].how | Compared within 10^-9; floor exactly at minute 175; test 7 floor 0 | correct | engine isclose rel 1e-9; sim: C l14 test lines |
| l14 | screens[4].feedback.byKey.test-2 | A at 120 with three rejections: 110, below the floor 150 | correct | sim: B "no floor" first fails at test-2 |
| l14 | screens[4].feedback.byKey.test-6 | "Apply the floor after both costs" | wrong | F 2: flooring before either cost stops at test 2; sim: FINDING 2 (two mutants) |
| l14 | screens[4].feedback.byKey.test-7 | Floor 0 and a value below 0: the score is 0 | correct | sim: B "a floor of 0 treated as no floor" first fails at test-7 |
| l14 | screens[4].explain | The larger of the two applies the floor after both costs; test 5 sits on it | correct | 1000 - 700 = 300 |
| l14 | screens[5].prose | ICPC style: solved count, then penalty, lower first; penalty = solve minute + 20 per rejection on a solved problem | correct | ICPC regional rules; the 20 is labelled "our illustration" and equals the ICPC figure |
| l14 | screens[5].solution, tests | `icpc_rank_key` passes 7 tests; starter fails | correct | sim: A l14 icpc_rank_key |
| l14 | screens[5].hints | Rejections on an unsolved problem cost nothing; 12 + 61 + 135 = 208 | correct | ICPC rules; sim: C l14 ICPC table |
| l14 | screens[5].feedback.byKey.test-1 | D's three rejections do not count | correct | sim: B "charges rejections on unsolved problems" first fails at test-1 |
| l14 | screens[5].feedback.byKey.test-2 | No solves: (0, 0) whatever the rejections | wrong | F 3: the slip it names stops at test 1; sim: FINDING 3 |
| l14 | screens[5].feedback.byKey.test-7 | Z ranks first despite a penalty of 400 | wrong | F 3: the figure is right (400), but no wrong key reaches test 7: each fails test 1; sim: FINDING 3 (three mutants) |
| l14 | screens[5].explain | Negating the solved count lets one ascending sort rank both parts | correct | tuple ordering, Python docs |
| l14 | screens[6].prose, caption | E(x) = 1000(1 - e^(-x/50)) + 800(1 - e^(-(60-x)/15)) is "the expected score if D gets the first x minutes and E the rest" | imprecise | F 9: true only if D keeps its x minutes even when it falls early; sim: C l14 split curve, stop-when-solved version |
| l14 | screens[6].target, hints, explain | Top near 35 minutes (34.84), about 1,152; all D 699, all E 785 | correct | sim: C l14 split curve (grid search and first-order condition) |
| l14 | screens[6].feedback.byKey.all | Region x 50 to 60: "You gave D the whole hour, which is about 699" | imprecise | F 10: 699 holds only at x = 60; at x = 50 the curve reads 1,021 |
| l14 | screens[6].feedback.byKey.none | Region x 0 to 8: "You skipped D altogether, which is about 785" | imprecise | F 10: 785 holds only at x = 0; at x = 8 the curve reads 923 |
| l14 | screens[6].explain | "A time cap on a stuck problem is this curve in practice" | imprecise | F 9: a cap leaves D when it is solved; the same model then tops at 45.3 minutes, not 35 |
| l14 | screens[7].options stay.why, byKey.stay | Time spent is gone either way: the sunk-cost mistake | correct | standard decision theory: choose on marginal, not sunk, cost |
| l14 | screens[7].options resub.why | Each rejection costs 50 points and teaches nothing | correct | the rule; a resubmission without a new idea gives the same verdict |
| l14 | screens[7].options floor.why | The floor applies only once D is solved; unsolved, D scores 0 | correct | the rule's "until solved" |
| l14 | screens[7].hints, explain | C at about 30 minutes is the best use of 40 | correct | judgement consistent with the figures given |
| l14 | screens[8] | E (702 solves) is likelier easier than D (96); about seven times | correct | 702 / 96 = 7.3; sim: C l14 scoreboard |
| l14 | screens[8].explain, summary.ideas[2] | Letters are the setters' guess; solve counts are evidence | correct | hedged "very likely" in the hint; counts early in a round favour earlier letters, which strengthens the inference here |
| l14 | screens[9].prose | i first loses (v_j t_i - v_i t_j)/250 more while neither score is at its floor; negative exactly when v_i/t_i > v_j/t_j | correct | derivation; sim: C l14 exchange formula and its sign rule hold on 20,000 random neighbour pairs |
| l14 | screens[9] | C then D scores 20 more than D then C; A B D C is 3,530 | correct | sim: C l14 C then D beats D then C by 20 |
| l14 | screens[9].byKey.neg, big | -20 is the change in points lost; 5000 forgets the 250 | correct | arithmetic |
| l14 | screens[9].explain | "Lesson 10's exchange argument applied to the round itself" | correct | l10-greedy-proofs defines the exchange argument; adjacent swaps give the sorted order (Pinedo 3.1) |
| l14 | screens[10].prose, solution, tests | `best_order` by brute force, ties to the alphabetically first order; passes 6 tests; starter fails | correct | sim: A l14 best_order |
| l14 | screens[10].how | Six problems give 720 orders | correct | 6! = 720 |
| l14 | screens[10].feedback.byKey.test-2 | 60 minutes: no three fit; B then C is 2,090 | correct | sim: B "points per minute order, no search" first fails at test-2; C l14 60 minutes |
| l14 | screens[10].feedback.byKey.test-3 | Listed backwards: sort by name first | correct | sim: B "no sort by name" first fails at test-3 |
| l14 | screens[10].feedback.byKey.test-4 | A 10-minute problem in a 5-minute round scores 0 | correct | sim: B "best total starts at 0" first fails at test-4 |
| l14 | screens[10].explain | With 60 minutes B then C (2,090) beats A then B (1,360); the rule of thumb is a default | correct | sim: C l14 60 minutes (both lines) |
| l14 | screens[11].prose, options | "The same rule applies: value per minute, largest first"; quote first, hedge graded wrong | imprecise | F 11: no decay is stated for the desk; with both tasks fitting before the close, hedge then quote earns the same £15,000 |
| l14 | screens[11].hints, why | £600, £480, £100 a minute; quote and hedge fit the half hour | correct | sim: C l14 desk |
| l14 | screens[11].explain | An interview with three questions in an hour works the same way | correct | analogy; no factual content |
| l14 | summary.ideas[0], formula | Points per minute order; Δlost = (v_j t_i - v_i t_j)/250 under our rule | correct | as screens[9] |
| l14 | summary.ideas[1], trap | Cap the time; sunk minutes are gone; resubmitting without an idea adds penalties | correct | as screens[7] |
| l14 | quiz[0] | 1000 - 720 - 50 = 230, floored to 300; 280 leaves out the rejection | correct | sim: C l14 quiz q-floor |
| l14 | quiz[1] | Z, then Y (185), then X (195); more solves always rank higher | correct | sim: C l14 ICPC quiz; ICPC rules |
| l14 | quiz[2] | P first: 30 against 25 a minute; totals differ with the order | correct | sim: C l14 quiz q-rate (1,550 against 1,525) |
| l14 | quiz[3] | Only a new idea justifies staying; time spent does not | correct | as screens[7] |
| l15 | screens[0].prose | Codeforces will not show you test 4 during the round | unverified | standard Codeforces behaviour (verdict and test number only); no official page fetched |
| l15 | screens[0].prose, summary.ideas[0] | "Most wrong answers are misreadings" | unverified | an empirical "most" with no source; see the unverified list in the audit for a softer wording |
| l15 | screens[0].answer, byKey | Line 6 (`range(len(xs) - 2, -1, -1)`) disagrees; the other four lines are right | correct | sim: C l15 hand cases; line numbering checked against the canvas |
| l15 | screens[0].explain | Starts at n - 2, so a match in the last place is missed; the example hides it | correct | sim: C l15 the example 4 7 7 1 hides the bug |
| l15 | screens[0].explain | An off-by-one at the end of the array is a very common wrong answer | correct | hedged; not a counted claim |
| l15 | screens[1].canvas | Four hand cases: expected 0, 2, 1, -1; submission -1, 1, 1, -1 | correct | sim: C l15 hand cases |
| l15 | screens[1].answer, byKey, explain | Two cases differ, both with x last | correct | same check |
| l15 | screens[1].explain | A small case you can trace beats a large one you cannot | correct | method statement; Laaksonen 1.5 style advice |
| l15 | screens[2].answer | Order: reread, hand cases, overflow and recursion, stress test | correct | the course's routine, ordered by cost as argued |
| l15 | screens[2].explain | Rereading finds misreadings, hand cases off-by-ones, limits overflow | correct | each is the bug class of its own example in this lesson |
| l15 | screens[2].explain | "The stress test, from lesson 4, finds the rest" | imprecise | F 12: a small random stress test cannot show slowness, deep recursion or overflow at large values, and misses bugs both programs share |
| l15 | screens[3].starter, solution, tests | Starter fails first at test 4; fix passes 7 tests | correct | sim: A l15 last_occurrence (both checks) |
| l15 | screens[3].feedback.byKey.test-4 | `[5]`, x = 5: the loop must visit index 0 | correct | the starter itself lands here |
| l15 | screens[3].feedback.byKey.test-3 | Empty list: `range(-1, -1, -1)` is empty | correct | sim: B "checks xs[-1] first" first fails at test-3 |
| l15 | screens[3].explain | The fix is one character | correct | 2 becomes 1 |
| l15 | screens[4].starter, solution, tests | Starter (`>=`) fails first at test 3; fix passes 7 tests | correct | sim: A l15 count_inversions_small |
| l15 | screens[4].how | 1,500 values, about 1.1 million pairs | correct | 1,124,250; sim: C l15 test 7 of fix 2 |
| l15 | screens[4].feedback.byKey.test-3 | `[2, 2]` has no inversion; `>=` counted it | correct | starter lands here |
| l15 | screens[4].feedback.byKey.test-6 | `[2, 1, 2, 1]` has 3 inversions | correct | sim: B "removes repeated values, keeps >=" first fails at test-6; C l15 inversions |
| l15 | screens[4].explain | Distinct values hide `>=`; the equal hand case separates them | correct | example 3 1 2 |
| l15 | screens[5].starter, solution, tests | Starter fails first at test 2; fix passes 6 tests | correct | sim: A l15 solve_all |
| l15 | screens[5].feedback.byKey.test-2 | The answer counted AAA and BBB from the first case | correct | starter returns [2, 3] |
| l15 | screens[5].feedback.byKey.test-6 | Two calls: a module-level set keeps the first call's tickers | wrong | F 4: the tests share one loaded module (engine), so such a set shows by test 2 or 3; sim: FINDING 4 |
| l15 | screens[5].explain | Reset per-case state at the top of the loop, or keep it local | correct | standard practice |
| l15 | screens[6].options, hints, explain | The checker reads all of standard output; debug lines belong on standard error | correct | judges compare stdout; stderr is not compared |
| l15 | screens[6].explain | Standard error is shown to you but ignored by the judge | correct | true of the verdict on Codeforces, AtCoder and ICPC systems; heavy stderr still costs time |
| l15 | screens[6].options rewrite.why, byKey.rewrite | A one-line fix is faster and safer than a rewrite under time | correct | judgement, consistent with screens[3] |
| l15 | screens[7].prose | Python stops at about 1,000 nested calls by default | correct | Python docs: default recursion limit 1000 (native check: 1000). The page's widgets use 3,000, but this screen runs no code |
| l15 | screens[7].options stack, feedback.correct, explain | An explicit stack is safe on any judge; depth becomes list length | correct | iterative DFS, CLRS 22.3 exercise; memory is the only bound |
| l15 | screens[7].options limit.why | Raising the limit works in this app's Pyodide, which ran a million frames | correct | sim: D Pyodide "million frames" (node, V8); other browser engines not tested |
| l15 | screens[7].options limit.why | On some judges deep recursion still crashes the interpreter | correct | CPython before 3.11 and PyPy overflow the C stack; Python docs warn that a high limit can crash |
| l15 | screens[7].options bfs.why | Halving still needs 50,000 frames | correct | 100,000 / 2 |
| l15 | screens[7].explain | In C++, check `int` overflow at the same step | correct | step 3 of the routine |
| l15 | screens[8].prose | `debug` prints to `sys.stderr`; four steps | correct | as screens[2], [6] |
| l15 | screens[8].options | Trace the failing hand case; a stress test would find the same small input; the same code gives the same answer | correct | deterministic program |
| l15 | screens[9].prose, solution, tests | `smallest_failing` grows n from 1 to 8 with 200 trials; passes 7 tests; starter fails | correct | sim: A l15 smallest_failing |
| l15 | screens[9].feedback.byKey.test-3 | "Try every length from 1 upwards, not only the longest" | wrong | F 5: trying only the longest stops at test 1; test 3 is reached by stopping at length 2; sim: FINDING 5 and B "tries lengths 1 and 2 only" |
| l15 | screens[9].feedback.byKey.test-6 | Values to 10^6 almost never tie, so the tie bug stays hidden | correct | sim: C l15 values to 1e6 (under 5% for any tie in the call); B "ignores gen" first fails at test-6 |
| l15 | screens[9].feedback.byKey.test-7 | Fails only from length 5: run up to 8 | correct | sim: B "stops at length 4" first fails at test-7 |
| l15 | screens[9].explain | Growing n returns the shortest failing case the trials find | correct | worded as "the trials find", not "the shortest that exists" |
| l15 | screens[10] | One fill and a restart is the n = 1 case; a doubled position means the replay is not idempotent | correct | definition of idempotent replay |
| l15 | screens[10].explain | Interviewers mark this calm, small-case habit | unverified | soft claim about interviews, no source |
| l15 | summary.ideas[1], [2], formula, trap | Routine order; stderr; per-case state; one-line fix; stdout prints fail every test | correct | as rows above |
| l15 | quiz[0] | 2·10^5 values of 10^9 overflow an `int` (2,147,483,647); `long long` to about 9.2·10^18 | correct | sim: C l15 quiz; wasm32 and x86-64 both have 32-bit `int`, 64-bit `long long` |
| l15 | quiz[0].options slow.why | Adding 2·10^5 numbers takes microseconds | correct | order of 100 microseconds |
| l15 | quiz[1] | 5 5 exposes `>=`; one close and distinct rising closes do not | correct | direct |
| l15 | quiz[2] | An uncleared global shows from the second test case on | correct | first case starts empty |
| l15 | quiz[3] | Neighbours-only count of `[3, 2, 1]` is 2; the smallest failing case has three values | correct | sim: C l15 neighbours-only count (exhaustive) |
| l16 | screens[0] | Upsolve D and E before the next round; reading without writing does not make the idea yours | correct | course's method; consistent through the lesson |
| l16 | screens[0].hints[2] | Solving them after the round teaches the most per hour | unverified | training claim, no source |
| l16 | screens[1].prose | After a round, Codeforces shows the failing test and the editorial | unverified | standard Codeforces behaviour (large tests are shown truncated); no official page fetched |
| l16 | screens[1].canvas | Double loop over cuts with prefix sums; test 9 is 200,000 zeros, answer 19999700001 | correct | sim: C l16 C(199999, 2); B "the double loop over cuts" first fails at test-8 |
| l16 | screens[1].canvas editorial | 3 must divide S; cuts work when P[i] = S/3 and P[j] = 2S/3; count earlier i at each j | correct | sim: C l16 equal_thirds equals the cut-by-cut brute force |
| l16 | screens[1].answer, byKey | Five zeros: C(4, 2) = 6; 10 is C(5, 2); 3 is for four zeros | correct | sim: C l16 binomials |
| l16 | screens[1].explain | About 2·10^10 pairs on test 9; the answer overflows a 32-bit `int` | correct | 19,999,700,001 > 2^31 - 1 |
| l16 | screens[2].prose | Upsolving: solving after the round what you could not solve in time | correct | standard usage of the term |
| l16 | screens[2].answer | Idea, close it, own code, accepted, write-up and log, redo a week later | correct | course's routine |
| l16 | screens[2].explain | The redo is the app's redo rhythm and the curriculum's weekly review block | correct | docs/PLAN.md redo at 7 days; curriculum review row |
| l16 | screens[3].prose, how | D about 1600; cuts 1 ≤ i < j ≤ n - 1 with P_i = S/3, P_j = 2S/3 | correct | the rating is an estimate (the classic version of this problem is rated near 1700) |
| l16 | screens[3].solution, tests | `equal_thirds` passes 9 tests; starter fails | correct | sim: A l16 equal_thirds; brute-force agreement |
| l16 | screens[3].hints[2] | Return 0 early if `S % 3` | correct | Python `%` is non-negative for a positive modulus |
| l16 | screens[3].feedback.byKey.test-2 | With S = 0 count the first cut only after checking the second | correct | sim: B "counts the first cut before checking the second" first fails at test-2 |
| l16 | screens[3].feedback.byKey.test-5 | Total 2: return 0 at once | correct | sim: B "no divisibility test" first fails at test-5 |
| l16 | screens[3].feedback.byKey.test-6 | Negatives, total 0: do not stop at the first match | correct | sim: B "stops once the prefix passes 2S/3" first fails at test-6 |
| l16 | screens[3].feedback.byKey.test-8 | A double loop is about 2·10^10 steps | correct | sim: B "the double loop over cuts" first fails at test-8 |
| l16 | screens[3].explain | Checking 2S/3 first stops a zero total pairing a cut with itself; C++ needs `long long` | correct | as test-2; count above 2^31 |
| l16 | screens[4] | Counts 3, 2, 2, 1 of eight | correct | sim: C l16 log counts |
| l16 | screens[4].explain | The top line is the rule to act on | correct | method statement |
| l16 | screens[5].solution, tests | `mistakes_summary` passes 8 tests; starter fails | correct | sim: A l16 mistakes_summary |
| l16 | screens[5].feedback.byKey.test-2 | Empty log: return an empty list | correct | sim: B "max() of an empty log" first fails at test-2 |
| l16 | screens[5].feedback.byKey.test-4 | Test 4's tie: break it alphabetically | wrong | F 6: test 1 already has a tie at 2, so every missing tie-break stops at test 1; sim: FINDING 6 (three mutants) |
| l16 | screens[5].feedback.byKey.test-6 | Python sorts capitals before lower case | correct | Python docs: string comparison by code point; sim: B "sorts names without regard to case" first fails at test-6 |
| l16 | screens[5].feedback.byKey.test-7 | Sort by count first, then name | correct | sim: B "sorts by name only" first fails at test-7 |
| l16 | screens[5].explain | The key (-count, name) sorts both ways in one call | correct | tuple ordering |
| l16 | screens[6] | Upsolve at most about 300 above your rating: C 1400 and D 1500 at 1,200 | correct | arithmetic; the 300 is the course's rule of thumb |
| l16 | screens[6].explain, byKey.l4 | Just above your level teaches one new idea; far above, editorials assume several | unverified | training heuristic, no source |
| l16 | screens[7].prose | The curriculum asks for one contest a week once 100 problems are behind you | correct | curriculum 2.4 |
| l16 | screens[7].options | Practise about 100 to 200 above; 2000 is 750 above 1,250 | correct | arithmetic; the band is the course's rule of thumb |
| l16 | screens[7].options rounds.why, screens[8].options contests.why | Without upsolving the same mistakes repeat and the rating stalls | unverified | causal training claim, no source |
| l16 | screens[7].explain | Project Euler adds maths with code, as the curriculum suggests | correct | curriculum 2.4 "Add" |
| l16 | screens[8] | Read is not solved: the code must be written and accepted | correct | the lesson's definition of upsolved |
| l16 | screens[9] | The weekly loop; upsolved means your own code accepted | correct | as above |
| l16 | screens[10].prose, summary.ideas[2] | 1,400 is a fair first-year target; rating shortlisting is mainly Indian campus hiring; helps developer applications, little for trader or researcher interviews | unverified | copied faithfully from curriculum 2.4; the hiring claims themselves have no checkable source |
| l16 | screens[10].prose | Most coding interviews use LeetCode-style problems; aim for a fresh medium in 30 minutes | unverified | matches curriculum 2.2 exit line; hiring claim, no checkable source |
| l16 | screens[10].canvas, options | Developer, trader and researcher interviews test the lists shown | unverified | consistent with the app's interview courses; no external source |
| l16 | screens[11] | Researchers add Kaggle, traders IMC Prosperity, everyone Project Euler; 1,800 - 1,410 = 390 | correct | curriculum 2.4 "Add"; IMC Prosperity is IMC's own trading competition; arithmetic |
| l16 | summary.formula | ways = sum over j with P_j = 2S/3 of the number of i < j with P_i = S/3 | correct | as screens[3] |
| l16 | quiz[0] | Four zeros: C(3, 2) = 3; 6 is for five zeros | correct | sim: C l16 binomials |
| l16 | quiz[1] | At 1,500 upsolve the 1700, not the 2100 (600 above) | correct | arithmetic on the 300 rule |
| l16 | quiz[2] | `[('edge case', 2), ('misread', 2), ('overflow', 1)]` | correct | solution's key; sim: A l16 mistakes_summary (test 4 shape) |
| l16 | quiz[3] | Trader interviews test probability, mental arithmetic and market-making games | unverified | as screens[10] |
| review-4 | items[0] | Smallest daily limit paying n redemptions in order over k days: binary search with a greedy check; a scan is up to about 2·10^14 limits | correct | problem C's shape; sim: C l13 review r4-pattern |
| review-4 | items[0].options window.why, bfs.why | "In order" is not a window; no graph here | correct | pattern definitions |
| review-4 | items[1] | Debugging share 18 / 60 = 30%; slips 50% and 60% | correct | sim: C r4 debugging share |
| review-4 | items[1].explain | That share is the first thing to cut, with hand cases before submitting | correct | l15's routine |
| review-4 | items[2] | 1500 - 288 - 100 = 1,112; slips 1,212, 1,162; floor 450 | correct | sim: C r4 decay |
| review-4 | items[3] | Q then P scores 20 more; waits cost 60 and 80; rates 33 and 25 | correct | sim: C r4 swap |
| review-4 | items[4] | The loop from index 1 returns 0 on `[5]`, 4 on `[2, 2, 2]`, 0 on the empty list | correct | sim: C r4 hand |
| review-4 | items[5] | The count needs `long long`; a `double` holds it exactly here; about nine times 2^31 - 1 | correct | sim: C l16 the count is about nine times; 2^53 bound |
| review-4 | items[5].options double.why | `long long` is exact to about 9.2·10^18 | correct | 2^63 - 1; on wasm32 too (`long` would not do, and is not offered) |
| review-4 | items[5].explain | Checking types is step 3 of the debugging routine | correct | l15 screens[2] |
| review-4 | items[6] | At 1,350 upsolve 1500 and 1600; 1900 and 2300 are 550 and 950 above | correct | sim: C r4 upsolve |
| review-4 | items[7] | E solved at 115 scores 675; slip 1,150; floor 375 | correct | sim: C r4 late |
| review-4 | items[7].explain | The score decays from minute 0, not from when you start the problem | correct | the rule's "until solved" |
| homework-4 | items[0].prose, solution, tests | Groups after removing link `cut`; self-links and repeats allowed; passes 8 tests; starter fails | correct | sim: A hw4 desks_after_cut |
| homework-4 | items[0].canvas | Examples: ring cut once stays 1 group; chain cut gives 3 | correct | tests 1 and 2 |
| homework-4 | items[0].how | A recursive DFS goes 100,000 deep, "far past Python's default limit of 1,000" | imprecise | F 13: this widget runs with a limit of 3,000 (engine), so the figure a learner meets is not the one named; depth 100,000 is right (sim: C hw4 desks) |
| homework-4 | items[0].feedback.byKey.test-4 | Cutting one copy of a repeated link leaves the other | correct | sim: B "removes every copy of the cut link" first fails at test-4 |
| homework-4 | items[0].feedback.byKey.test-5 | Test 5 has isolated desks; each is a group | wrong | F 7: example 2 (test 2) already has isolated desks, so the slip stops there; sim: FINDING 7 (two mutants) |
| homework-4 | items[0].feedback.byKey.test-7 | Chain of 200,000: use a queue or explicit stack | correct | sim: B "recursive DFS (3,000 frames on the page)" first fails at test-7 |
| homework-4 | items[0].explain | O(n + m); each BFS start is one group | correct | CLRS 22.2, connected components |
| homework-4 | items[1].prose, solution, tests | At most k trades, one unit, same-day sale and purchase allowed, O(nk); passes 8 tests; starter fails | correct | sim: A hw4 max_profit_k; C hw4 max_profit_k equals a brute force |
| homework-4 | items[1].canvas | 3 2 6 5 0 3 with k = 2 gives 7 | correct | 4 + 3 |
| homework-4 | items[1].feedback.correct, explain | `buy[j]` best cash after the j-th purchase, `sell[j]` after the j-th sale; O(nk) = 2·10^5 updates | correct | standard DP; with same-day trades "j-th" and "at most j" coincide in value; sim: C hw4 k trades |
| homework-4 | items[1].feedback.byKey.test-3 | No trades allowed: 0 | correct | sim: B "arrays of length k" first fails at test-3 |
| homework-4 | items[1].feedback.byKey.test-4 | Falling prices: best is not to trade | correct | sim: B "forces exactly k trades" first fails at test-4 |
| homework-4 | items[1].feedback.byKey.test-6 | Ten trades allowed, three rises help: 2 + 3 + 4 = 9 | correct | sim: B hw4 max_profit_k test 6 arithmetic; descriptive line, names no slip |
| homework-4 | items[1].feedback.byKey.test-8 | Every pair of days per trade is O(n^2 k), about 2·10^9 | correct | sim: B "every pair of days" first fails at test-8 |
| homework-4 | items[2].prose, solution, tests | Largest minimum distance for m bots on distinct levels; passes 8 tests; starter fails | correct | sim: A hw4 widest_gap; C hw4 widest_gap equals choosing every set |
| homework-4 | items[2].canvas | 1 2 8 4 9 with m = 3 gives 3 (bots at 1, 4, 8 or 1, 4, 9) | correct | brute force |
| homework-4 | items[2].feedback.byKey.test-4 | Three equal levels and two bots: 0 | correct | sim: B "search starts at distance 1" first fails at test-4 |
| homework-4 | items[2].feedback.byKey.test-5 | "Test 5 is unsorted. Sort the levels" | wrong | F 8: the example, test 1, is unsorted too, so a missing sort stops there; sim: FINDING 8 |
| homework-4 | items[2].feedback.byKey.test-8 | About 30 greedy checks, not every distance | correct | sim: B "tries every distance upwards" first fails at test-8 |
| homework-4 | items[2].explain | If d can be kept so can every smaller distance; greedy places each bot on the first level at least d above the last; O(n log n) plus about 30 O(n) checks | correct | Laaksonen 3.3; greedy stays-ahead argument; log2(10^9) ≈ 30 |
| homework-4 | items[3] | First ten minutes: timer, constraints and output, patterns, rank by points per minute and scoreboard, restate, code | correct | l13 and l14 routines |
| homework-4 | items[3].explain | Restating before coding catches a misreading at the cheapest moment | correct | l15 step 1 |
| homework-4 | items[4] | Penalty 8 + 27 + 64 + 110 + 60 = 269; E's rejections do not count; slips 349 and 209 | correct | ICPC rules; sim: C hw4 penalty |
| homework-4 | items[5] | Pushing the rating does least for a trader application | unverified | follows curriculum 2.4; hiring claim |
| homework-4 | items[6].model A to D | Ideas, complexities and edge cases of the four problems | correct | match the solutions; k = 1 gives the total, k = n the heaviest |
| homework-4 | items[6].model times | A 9, B 17, C 27 (12 debugging), 7 left for D; rejections 0, 1, 2 | correct | sim: C l13 Alex per problem |
| homework-4 | items[6].model C | "My check let an order heavier than the van start a new day" cost two rejections | correct | a real bug when the search starts below the heaviest order; with lo = max(weights) it cannot show (B l13 C) |
| homework-4 | items[6].model plan, rating | Upsolve to about 300 above 1,250; five problems 1350 to 1450; rating paragraph | correct | l16 screens[6], [7], [10] |
| homework-4 | items[6].rubric | Six rubric lines, 10 points | correct | consistent with the model |

Rows: 270. Verdicts: correct 238, wrong 8, imprecise 9, misleading 0, unverified 15.

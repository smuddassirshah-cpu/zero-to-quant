# Claim ledger: contests level 4, round 2 (blind)

Files in `app/content/courses/contests/`. Every row was judged by hand. `script` is `docs/reports/contests-L4-concepts-r2.py`; Pyodide figures come from a run of the solutions in Pyodide 0.27.7 under node. Paths use `screens[i]` and `items[i]` from 0.

Rows: 251. Verdicts: correct 232, wrong 2, imprecise 9, misleading 1, unverified 7.

| file | JSON path | claim | verdict | basis |
| --- | --- | --- | --- | --- |
| l13-virtual-contest.json | screens[0].prose | A virtual contest here is four problems in 60 minutes; the player has no clock | correct | Engine fact: lesson screens are untimed; consistent with screens[2] |
| l13-virtual-contest.json | screens[0].widget.answer | C (smallest van for k days) is the binary-search-on-the-answer problem | correct | Feasibility is monotone in capacity; CLRS-style parametric search; standard 'ship within days' problem |
| l13-virtual-contest.json | screens[0].hints[1] | A bigger van always works if a smaller one does | correct | Derivation: any day split valid at capacity c is valid at c + 1 |
| l13-virtual-contest.json | screens[0].hints[2] | Smallest capacity with every larger one working is the shape binary search on the answer needs | correct | Monotone predicate; lesson 2 convention |
| l13-virtual-contest.json | screens[0].feedback.byKey.l2 | Counting peaks is one pass | correct | O(n) loop; solution of screens[3] |
| l13-virtual-contest.json | screens[0].feedback.byKey.l3 | Shortest run holding every name is a sliding window | correct | Minimum window cover, two pointers; solution of screens[4] |
| l13-virtual-contest.json | screens[0].feedback.byKey.l5 | Fewest moves on a grid is a BFS | correct | Unit-cost shortest path; CLRS 22.2 |
| l13-virtual-contest.json | screens[0].explain | A loop, B sliding window, C binary search on the answer, D BFS | correct | Matches the four solutions, all run by script |
| l13-virtual-contest.json | screens[1].canvas A | Peak: 1 < i < n and strictly above both neighbours; ends never peaks; example 3 5 4 6 2 gives 2 | correct | script: solution on the example |
| l13-virtual-contest.json | screens[1].canvas B | Example AAA BBB AAA CCC BBB with BBB CCC gives 2 | correct | script: test 1 |
| l13-virtual-contest.json | screens[1].canvas C | Example 4 8 2 7 5 3 with k = 3 gives 12 | correct | Split 4 8 / 2 7 / 5 3 has loads 12, 9, 8; 11 needs 4 days; script |
| l13-virtual-contest.json | screens[1].canvas D | Arrow cells are left only their own way and may be entered from any side | correct | Matches the solution's move rule |
| l13-virtual-contest.json | screens[1].widget.answer | 5 1 5 has 0 peaks | correct | Day 2 is below both; ends excluded; test 4 |
| l13-virtual-contest.json | screens[1].wrong ends/valley | 2 counts both ends; 1 counts the dip | correct | Slip values are wrong under the statement; grade-all routes them |
| l13-virtual-contest.json | screens[1].hints[2] | Only day 2 could be a peak and 1 is below both neighbours | correct | Direct |
| l13-virtual-contest.json | screens[1].explain | Reading the note saves a wrong answer on test 3 later | correct | script: counting the ends fails first at test 3 of problem A |
| l13-virtual-contest.json | screens[2].prose | A virtual contest is a past round sat alone at full length; Codeforces calls it virtual participation | correct | Codeforces contest pages offer 'Virtual participation' for finished rounds |
| l13-virtual-contest.json | screens[2].prose | The curriculum asks for one contest a week; a virtual one counts when no live round fits | correct | docs/curriculum.md 2.4: 'enter one contest a week'; the second half is the course's own reading |
| l13-virtual-contest.json | screens[2].options | The lesson cannot keep the clock; it does judge on hidden tests, give statements and an estimated rating | correct | Engine: code widgets run hidden tests; ratings 800 to 1500 stated on screens[3..6] |
| l13-virtual-contest.json | screens[2].explain | The timer runs outside the app and minutes are logged after each problem | correct | Course routine, consistent with screens[8] |
| l13-virtual-contest.json | screens[3].prose | Problem A is about 800 on Codeforces' scale by our estimate | unverified | An estimate, labelled as one; no source can confirm a rating for an invented problem |
| l13-virtual-contest.json | screens[3].widget.solution | peaks: one pass over 1..n-2 with strict comparisons | correct | script: passes 10 tests natively and in Pyodide 0.27.7; starter fails |
| l13-virtual-contest.json | screens[3].widget.how | 10 hidden tests; tests 9 and 10 are 200,000 closes | correct | script: counted |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-2 | A single close: range(1, 0) is empty, so no special case is needed | correct | script: an unguarded read of closes[1] fails first at test 2 |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-3 | 4 9: the last day is never a peak | correct | script: counting the last day fails first at test 3 |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-4 | 5 1 5: the ends are not peaks | correct | script: counting the first day fails first at test 4 |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-5 | 2 2 2 2: >= counts peaks that are not there | correct | script: >= on both sides fails first at test 5 |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-6 | 1 3 3 1: neither 3 is strictly above both | correct | script: >= on one side fails first at test 6 |
| l13-virtual-contest.json | screens[3].explain | The flat and plateau tests catch a >= slip | correct | script: tests 5 and 6 |
| l13-virtual-contest.json | screens[4].prose | With n = 2e5, restarting a scan at every trade is too slow | correct | Worst case n^2/2 = 2e10 steps; script |
| l13-virtual-contest.json | screens[4].widget.solution | shortest_cover: sliding window with counts per needed name | correct | script: passes 9 tests; 2 pointers, O(n) |
| l13-virtual-contest.json | screens[4].widget.how | Test 8 allows 4n reads on 2,000 trades; ZZZ appears only as the last trade | correct | Prelude: reads <= 8000; _tape appends the rare name |
| l13-virtual-contest.json | screens[4].hints[2] | Each trade enters and leaves once: O(n) | correct | Amortised two-pointer argument |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-3 | A name that never trades: return -1 | correct | script: returning the start value fails first at test 3 |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-5 | BBB listed twice: cover each distinct name once, set(needed) | correct | script: comparing with len(needed) fails first at test 5 |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-8 | Restarting at every left end rereads the tape | correct | script: the restart fails first at test 8 (about 2 million reads) |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-9 | The restart is O(n^2) here because ZZZ is only at the end | correct | script: the restart on a copied tape passes test 8 and times out at test 9 |
| l13-virtual-contest.json | screens[4].explain | About 2e10 steps on test 9 | correct | 200000 * 200001 / 2 = 2.0e10 |
| l13-virtual-contest.json | screens[5].prose | Binary search between the heaviest order and the total; min_capacity must call can_ship | correct | Bounds are right (answer lies in [max, sum]); the 'must call' is an instruction the tests do not enforce (0 calls pass test 10): inbox bullet |
| l13-virtual-contest.json | screens[5].widget.solution | Greedy check plus binary search on capacity | correct | script: passes 11 tests; greedy fill is optimal for a fixed order (exchange) |
| l13-virtual-contest.json | screens[5].widget.how | Test 4 has an order heavier than the van (so the guard is tested) | imprecise | script FINDING 4: the standard greedy without the w > cap guard passes all 11 tests |
| l13-virtual-contest.json | screens[5].widget.how | 40 orders with a total of 1,807; 13 calls allowed | correct | script: total 1,807, heaviest 99, 11 calls used |
| l13-virtual-contest.json | screens[5].hints | If c works so does every larger; greedy fills each day until the next order would overflow | correct | Monotone predicate; greedy stays-ahead |
| l13-virtual-contest.json | screens[5].feedback.correct | About log2(total) checks | correct | ceil(log2(sum - max)) <= log2(total) |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-2 | Shown when can_ship miscounts 11 as shipping in 3 days | imprecise | script FINDING 1: with min_capacity calling can_ship, any such miscount fails test 1 first; the line shows only when min_capacity bypasses can_ship |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-2 | 11 needs 4 days: 4 / 8 2 / 7 / 5 3 | correct | Hand trace; script |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-4 | Order of 5, van of 4: return False | correct | script: a greedy that carries an overweight order alone fails first at test 4 |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-10 | More than 13 calls: search between heaviest and total, halving | correct | script: bounds 1..1e9 (30 calls) and a scan (811 calls) both fail first at test 10 |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-11 | Checks must be about 30, not a million | correct | script: an inlined scan passes test 10 and times out at test 11; answer minus heaviest is about 1e6 |
| l13-virtual-contest.json | screens[5].explain | About 30 checks at n = 1e5; test 10 used 11 checks against about 811 for a scan from 99 | correct | script: 11 and 909 - 99 + 1 = 811 |
| l13-virtual-contest.json | screens[6].prose | From '.' any open neighbour; from an arrow only its way; example answer 11 | correct | Hand trace of the grid (path through the > in row 2); script |
| l13-virtual-contest.json | screens[6].widget.solution | BFS whose moves depend on the cell left | correct | script: passes 9 tests; 0.2 s in Pyodide on 400 by 500 |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-1 | Ignoring the arrows gives 7, through the dead end at the v | correct | script: the arrow-blind BFS returns 7 and fails test 1 |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-2 | Both neighbours of the start are arrows that lead out of the grid: -1 | correct | script: returning None for unreachable fails first at test 2 |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-3 | One cell: 0 moves | correct | script: testing the target only on a push fails first at test 3 |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-9 | 200,000 cells; a search that revisits cells cannot finish | correct | script: a DFS that revisits on a shorter distance passes tests 1 to 8 and times out at test 9 |
| l13-virtual-contest.json | screens[6].explain | Each cell visited once with at most four moves: O(rc); the v is a dead end | correct | BFS bound; v sits on the last row and points off the grid |
| l13-virtual-contest.json | screens[7].canvas | Sam: D wrong at 00:38 and 00:51, A opened 00:52, accepted 00:59, 1 solved | correct | Internally consistent |
| l13-virtual-contest.json | screens[7].options | Hardest first: its time is the most uncertain and can eat the hour; second wrong answer cost 13 more minutes | correct | 51 - 38 = 13; uncertainty claim is the lesson's premise, illustrated by the log |
| l13-virtual-contest.json | screens[7].feedback/explain | D took 52 minutes and scored nothing; A took seven | correct | 52 - 0 and 59 - 52 |
| l13-virtual-contest.json | screens[8].widget | Totals 16, 27, 17; together 60 | correct | script |
| l13-virtual-contest.json | screens[8].explain | Debugging took 17 minutes, 12 on C | correct | Table |
| l13-virtual-contest.json | screens[9].prose | Routine: read all in minutes 0 to 5, solve in order of ease, move on after 15 minutes without a new idea, log | correct | Course convention, stated as a routine; used consistently in l14 and homework |
| l13-virtual-contest.json | screens[9].explain | The letters only roughly follow difficulty | correct | Codeforces practice: problems are ordered by setters' estimate; solve counts often disagree |
| l13-virtual-contest.json | screens[10].options | Order of ease with a 15-minute cap; four minutes is a sixth of a problem's time | correct | 75 / 3 = 25; 4 / 25 = 0.16 |
| l13-virtual-contest.json | screens[10].options.all.why | Partial code passes no hidden tests | correct | Unfinished code; true as stated for code that does not yet run |
| l13-virtual-contest.json | screens[10].explain | An online assessment is auto-graded, timed and scored by what passes | correct | General description of auto-graded assessments (HackerRank, CodeSignal score by tests passed) |
| l13-virtual-contest.json | summary.ideas | Virtual contest; read every statement first; log minutes and wrong submissions | correct | Restates screens[2], [9], [8] |
| l13-virtual-contest.json | summary.formula | checks is about log2(sum w - max w), each one greedy pass O(n) | correct | Range of the search is [max, sum]; script |
| l13-virtual-contest.json | summary.trap | Opening the most interesting problem first | correct | Restates screens[7] |
| l13-virtual-contest.json | quiz.q-capacity | About 30 checks since 2^30 > 1e9; 3e6 steps | correct | 2^30 = 1.07e9; 30 * 1e5 |
| l13-virtual-contest.json | quiz.q-cover | Shortest run with all three names is 3 | correct | Trades 2 to 4 or 3 to 5; no run of 2 holds three names |
| l13-virtual-contest.json | quiz.q-plateau | 2 2 3 3 2 has 0 peaks | correct | script |
| l13-virtual-contest.json | quiz.q-boxed | .> over v. returns -1 | correct | script: test 2 |
| l14-which-first.json | screens[0].prose | Our rule: lose v/250 a minute, 50 per rejected attempt, floor 0.3v; an illustration, check the real round | correct | It is the Codeforces rule for a two-hour round (Codeforces contest rules); the text labels it as the course's illustration |
| l14-which-first.json | screens[0].canvas | Lost per minute 2, 4, 6, 8 | correct | v / 250 |
| l14-which-first.json | screens[0].widget.answer | A B C D, with A and B interchangeable, is the best order | correct | script: of 24 orders only ABCD and BACD reach 3,550 |
| l14-which-first.json | screens[0].hints[2] | Points per minute 50, 50, about 43, 40 | correct | 500/10, 1000/20, 1500/35 = 42.86, 2000/50 |
| l14-which-first.json | screens[0].explain | Best rate first means the slow problem waits, not the quick ones | correct | Smith's rule (Smith 1956) for weighted completion time; screens[9] derives it |
| l14-which-first.json | screens[1].canvas | A B C D 3,550 (480, 880, 1110, 1080); D C B A 3,440 (270, 580, 990, 1600); C A B D 3,520 (410, 740, 1290, 1080) | correct | script |
| l14-which-first.json | screens[1].feedback.byKey | Hardest first: D gains, the rest lose more; C first makes A and B wait 35 minutes | correct | +520 against -630; C takes 35 minutes |
| l14-which-first.json | screens[1].explain | Hardest first lifts D from 1,080 to 1,600 and drops the other three by 630 | correct | script |
| l14-which-first.json | screens[2].prose | Order of points per minute: value over estimated solving time, largest first | correct | Smith's ratio rule; exact for a linear decay proportional to v with no floor or deadline (screens[9]) |
| l14-which-first.json | screens[2].widget | C about 42.9 (42.857), D 40 | correct | 1500/35, 2000/50 |
| l14-which-first.json | screens[2].explain | The rates fall from A to D; when letters and rates disagree the rates win; a wrong estimate changes the order | correct | 50, 50, 42.9, 40 (A and B tie, as screens[0] says) |
| l14-which-first.json | screens[3].widget.answer | B at minute 35 with one rejection scores 810 | correct | 1000 - 140 - 50 |
| l14-which-first.json | screens[3].wrong | 860 omits the rejection, 300 is the floor, 760 charges it twice | correct | Arithmetic |
| l14-which-first.json | screens[3].explain | The floor of 30% matters only for a problem solved very late | imprecise | script FINDING 5: by time alone the floor is reached at minute 175, after a two-hour round; inside the round it binds only with rejections (next screen's test 2) |
| l14-which-first.json | screens[4].prose | Score is the larger of floor * value and value less time and attempt costs | correct | Definition of the rule |
| l14-which-first.json | screens[4].widget | decayed_score solution and 8 tests; compared within 1e-9 | correct | script; code.js isclose rel_tol 1e-9, abs_tol 1e-12 |
| l14-which-first.json | screens[4].feedback.byKey.test-2 | A at 120 with three rejections: 110, below the floor of 150; floor after both costs | correct | script: floor before the attempt cost, and no floor, both fail first at test 2 |
| l14-which-first.json | screens[4].feedback.byKey.test-7 | Floor 0 and a value below 0: the score is 0 | correct | script: treating floor 0 as no floor fails first at test 7 |
| l14-which-first.json | screens[4].explain | Test 5 sits exactly on the floor: 1000 - 4 * 175 = 300 | correct | Arithmetic |
| l14-which-first.json | screens[5].prose | ICPC style: rank by problems solved, then lower penalty; penalty is solve minute plus 20 per rejected attempt on solved problems | correct | ICPC World Finals rules: 20 penalty minutes per rejected run on a solved problem |
| l14-which-first.json | screens[5].widget | icpc_rank_key returns (-solved, penalty); table gives (-3, 208) | correct | script: 12 + 61 + 135 |
| l14-which-first.json | screens[5].hints | Rejections on an unsolved problem cost nothing | correct | ICPC rules |
| l14-which-first.json | screens[5].feedback.byKey.test-1 | D's three rejections do not count | correct | script: charging them fails test 1 |
| l14-which-first.json | screens[5].feedback.byKey.test-5 | A bare `if minute:` drops a solve at minute 0 | correct | script: fails first at test 5 |
| l14-which-first.json | screens[5].explain | Negating the solved count lets one ascending sort rank the board | correct | Tuple ordering; test 7 |
| l14-which-first.json | screens[6].prose | E(x) = 1000(1 - e^(-x/50)) + 800(1 - e^(-(60-x)/15)) is the expected score for a fixed split | correct | Exponential solving times with means 50 and 15; P(solved within x) = 1 - e^(-x/mean) |
| l14-which-first.json | screens[6].widget.target | Best split x = 34.84, about 1,152 points | correct | script: grid search; first-order condition gives 34.84 |
| l14-which-first.json | screens[6].feedback.byKey | All D about 699; no D about 785 | correct | script |
| l14-which-first.json | screens[6].explain | Leaving D when solved, the same model puts the best cap near 45 minutes | correct | script: cap 45.3, 1,229 points (quadrature and Monte Carlo) |
| l14-which-first.json | screens[6].explain | Implied: D is the problem to start on | misleading | script FINDING 6: under the same model, E first (leaving E when solved) expects 1,363 against 1,229; the lesson's own rate rule says E first (53 against 20 points a minute) |
| l14-which-first.json | screens[7].options | Spent time is gone either way; the floor applies only once D is solved; unsolved D scores 0 | correct | Sunk cost; rule of screens[0] |
| l14-which-first.json | screens[7].options.resub.why | Each rejection costs 50 points | correct | Rule of screens[0]; realised when the problem is solved |
| l14-which-first.json | screens[7].explain | Only future minutes can be allocated; C at about 30 minutes is the best use of 40 | correct | Decision depends on remaining time only |
| l14-which-first.json | screens[8].widget.answer | E (702 solves) before D (96): E is very likely easier | correct | 702 / 96 = 7.3; solve counts are the standard live difficulty signal |
| l14-which-first.json | screens[8].explain | Letters are the setters' guess; the scoreboard is contestants' evidence | correct | Standard contest practice |
| l14-which-first.json | screens[9].prose | i first loses (v_j t_i - v_i t_j)/250 more than j first, while neither score is at its floor; negative exactly when v_i/t_i > v_j/t_j | correct | script: checked on every adjacent pair of every order; Smith (1956) exchange argument; the swap leaves other problems' finish times unchanged |
| l14-which-first.json | screens[9].widget.answer | C then D scores 20 more than D then C | correct | (70000 - 75000)/250 = -20; script |
| l14-which-first.json | screens[9].explain | A B C D 3,550 against A B D C 3,530; lesson 10's exchange argument | correct | script; l10-greedy-proofs teaches the exchange argument |
| l14-which-first.json | screens[10].prose | best_order: back to back, a problem finishing after `minutes` scores 0, ties alphabetical | correct | Definition; solution brute-forces all orders |
| l14-which-first.json | screens[10].widget | Solution and 6 tests, 720 orders for six problems | correct | script: passes; 6! = 720 |
| l14-which-first.json | screens[10].feedback.byKey.test-2 | 60 minutes: no three problems fit; B then C is worth 2,090 | correct | script: letting late problems score fails first at test 2; 10 + 20 + 35 = 65 |
| l14-which-first.json | screens[10].feedback.byKey.test-3 | Sort by name first so ties come out the same | correct | script: no sort fails first at test 3 |
| l14-which-first.json | screens[10].feedback.byKey.test-4 | The only problem cannot finish: total 0 | correct | script: starting the best total at 0 fails first at test 4 |
| l14-which-first.json | screens[10].explain | With 60 minutes the best order skips A: 2,090 against 1,360 | correct | script |
| l14-which-first.json | screens[11].prose | Tasks lose a fixed share of value each minute; value per minute, largest first | correct | Same exchange argument with rate proportional to value |
| l14-which-first.json | screens[11].options | Quote 600, hedge 480, reconcile 100 pounds a minute | correct | 3000/5, 12000/25, 2000/20 |
| l14-which-first.json | screens[11].feedback.correct, hints[2] | Quote first, then hedge, then reconcile (within the half hour) | imprecise | script FINDING 7: 5 + 25 + 20 = 50 minutes against 30; the explain itself says only the quote and hedge fit |
| l14-which-first.json | screens[11].explain | At 1% a minute quote first costs the hedge 600 pounds; hedge first costs the quote 750 | correct | script |
| l14-which-first.json | screens[11].explain | An interview with three questions in an hour works the same way | unverified | Interview scoring does not decay by a known rule; advice, not established |
| l14-which-first.json | summary | Points per minute; cap a stuck problem; the scoreboard beats the letters; swap formula under our rule | correct | Restates screens[2], [7], [8], [9] |
| l14-which-first.json | quiz.q-floor | 1000 - 720 - 50 = 230, so the score is the floor, 300 | correct | Arithmetic |
| l14-which-first.json | quiz.q-icpc | Z (four solves), then Y 185, then X 195; more solves always rank higher | correct | ICPC rules; arithmetic |
| l14-which-first.json | quiz.q-rate | P 30 a minute against Q 25; best_order agrees | correct | script: test 5 of screens[10] |
| l14-which-first.json | quiz.q-sunk | Only a new idea justifies staying | correct | Sunk-cost reasoning |
| l15-debugging-under-time.json | screens[0].widget.answer | Line 6 starts at n - 2 and never looks at the last element | correct | range(len(xs) - 2, -1, -1) |
| l15-debugging-under-time.json | screens[0].explain | The example hides it because its last 7 is not at the end | correct | 4 7 7 1 returns 2 with the bug; script |
| l15-debugging-under-time.json | screens[0].explain | An off-by-one at the end of the array is a very common wrong answer | correct | Common-knowledge claim about contest bugs; not quantified |
| l15-debugging-under-time.json | screens[1].canvas | Hand cases: [5] gives -1, [3,3,3] gives 1, [1e9,1e9,1] gives 1, [4,7] with 9 gives -1 | correct | script |
| l15-debugging-under-time.json | screens[1].widget.answer | Two of the four cases are wrong, both with x last | correct | script |
| l15-debugging-under-time.json | screens[1].explain | A small case you can trace beats a large one you cannot | correct | Debugging practice; Kernighan and Pike, The Practice of Programming ch. 5 (make the failing case small) |
| l15-debugging-under-time.json | screens[2].widget.answer | The only correct order is reread, hand cases, limits, stress test | imprecise | Finding 10: the prompt orders by cost; a glance at types and depth is not dearer than running hand cases, so s3 before s2 is defensible |
| l15-debugging-under-time.json | screens[2].explain | Each step is cheaper than the next | imprecise | Finding 10: not established for steps 2 and 3 |
| l15-debugging-under-time.json | screens[2].explain | Rereading finds misreadings, hand cases off-by-ones, limits overflow; the stress test finds wrong answers small random cases can show | correct | Lesson 4 (stress testing) states the same limit of a stress test |
| l15-debugging-under-time.json | screens[3].widget | Fix is one character; 7 tests | correct | script: solution passes, starter fails first at test 4 |
| l15-debugging-under-time.json | screens[3].feedback.byKey.test-4 | [5] with x = 5: the loop must visit index 0 | correct | script: the starter fails first at test 4 |
| l15-debugging-under-time.json | screens[3].feedback.byKey.test-3 | Empty list: range(-1, -1, -1) is empty, so -1 without a special case | correct | script: a special case reading xs[-1] fails first at test 3 |
| l15-debugging-under-time.json | screens[4].prose | Inversions: pairs i < j with x_i > x_j; the submission failed test 3 | correct | script: the starter (>=) fails first at test 3, [2, 2] |
| l15-debugging-under-time.json | screens[4].widget.how | 1,500 values make about 1.1 million pairs | correct | 1500 * 1499 / 2 = 1,124,250 |
| l15-debugging-under-time.json | screens[4].feedback.byKey.test-3 | >= counted the equal pair | correct | script |
| l15-debugging-under-time.json | screens[4].feedback.byKey.test-6 | Shown for a count that is not strictly-greater | wrong | script FINDING 2: every non-strict comparison fails test 3 first; the line shows for other bugs (removing repeated values fails first at 6), which its advice does not fit |
| l15-debugging-under-time.json | screens[4].feedback.byKey.test-6 | [2, 1, 2, 1] has 3 inversions | correct | Pairs (1,2), (1,4), (3,4) |
| l15-debugging-under-time.json | screens[4].explain | Distinct values make >= and > agree; the equal case separates them | correct | Direct |
| l15-debugging-under-time.json | screens[5].widget | Per-case state: a set created inside the loop | correct | script: solution passes 6 tests; starter fails first at test 2 |
| l15-debugging-under-time.json | screens[5].feedback.byKey.test-2 | The answer counted AAA and BBB from the first case too | correct | script: the starter returns [2, 3]; code.js runs all tests in one namespace |
| l15-debugging-under-time.json | screens[5].feedback.byKey.test-3 | A set kept outside solve_all still holds tickers from an earlier call | correct | script: a global set emptied between cases but not per call fails first at test 3 |
| l15-debugging-under-time.json | screens[5].explain | A multi-case bug hides from every t = 1 example; reset per-case state, better keep it local | correct | Standard practice |
| l15-debugging-under-time.json | screens[6].prose, canvas | Prints added 'to see what was happening' show case 2 as seen = {'CCC'} and answer 1 | imprecise | Finding 11: with the bug still in, case 2 prints three names and 3; and screens[5] says the judged example has t = 1 |
| l15-debugging-under-time.json | screens[6].options | The checker reads all of standard output; extra lines anywhere make it wrong | correct | Token and line checkers (testlib wcmp, ncmp) reject extra output |
| l15-debugging-under-time.json | screens[6].hints[2], feedback.correct, explain | Standard error is ignored by the judge | imprecise | Finding 9: it is not compared, but writing it still costs run time; heavy debug output is a known cause of time limit exceeded |
| l15-debugging-under-time.json | screens[6].explain | The judge compared lines 2 to 5 with the expected 2 and 1 | correct | Canvas lines 2 to 5 |
| l15-debugging-under-time.json | screens[7].prose | Python stops at about 1,000 nested calls by default | correct | CPython sys.getrecursionlimit() default 1000; the page sets 3,000 and homework says so |
| l15-debugging-under-time.json | screens[7].options.limit.why | setrecursionlimit(10**6) works in this app's Pyodide, which ran a million frames | correct | Run here: Pyodide 0.27.7 (CPython 3.12.7, wasm32) under node completed a 1,000,000-deep pure-Python DFS |
| l15-debugging-under-time.json | screens[7].options.limit.why | On some judges deep recursion still crashes the interpreter | correct | CPython before 3.11 uses the C stack per Python call and segfaults when it runs out |
| l15-debugging-under-time.json | screens[7].options | Halving the depth still needs 50,000 frames; test 9 is already a line of 100,000 | correct | Arithmetic |
| l15-debugging-under-time.json | screens[7].explain | An explicit stack works on every judge; in C++ check int overflow at the same step | correct | Depth becomes list length; graphs-dp l3 teaches the explicit stack |
| l15-debugging-under-time.json | screens[8].prose | debug() prints to sys.stderr; the routine's four steps | correct | print(file=sys.stderr); see the row on screens[6] for 'judge ignores it' |
| l15-debugging-under-time.json | screens[8].options | After a failing hand case, trace it; the same code gives the same answer | correct | Deterministic program |
| l15-debugging-under-time.json | screens[9].widget | smallest_failing grows n from 1 to 8 with 200 trials each | correct | script: solution passes 7 tests; stress matches lesson 4's signature |
| l15-debugging-under-time.json | screens[9].feedback.byKey.test-3 | The bug needs three values: keep growing past 2 | correct | script: stopping at length 2 fails first at test 3 |
| l15-debugging-under-time.json | screens[9].feedback.byKey.test-6 | Values up to 1e6 almost never tie, so the tie bug stays hidden | correct | script: chance of any tie over the whole loop is 1.7%; a fixed gen_list fails first at test 6 |
| l15-debugging-under-time.json | screens[9].feedback.byKey.test-7 | Fails only from length 5: run up to 8 | correct | script: stopping at length 4 fails first at test 7 |
| l15-debugging-under-time.json | screens[9].explain | Returns the shortest failing case the trials find | correct | Hedged correctly: random trials, not a proof of minimality |
| l15-debugging-under-time.json | screens[10] | Incident: reproduce with one fill and a restart; a non-idempotent replay double-counts | correct | Standard incident practice; 2,400 = 2 * 1,200 |
| l15-debugging-under-time.json | summary | Reread, hand cases, limits, stress; debug to standard error; a one-line fix beats a rewrite | correct | Restates the screens (see rows on order and standard error) |
| l15-debugging-under-time.json | quiz.q-overflow | 2e5 * 1e9 = 2e14 overflows a 32-bit int (max 2,147,483,647); long long to about 9.2e18 | correct | ISO C++ [basic.fundamental]; int is 32 bits on wasm32 and on judges; script |
| l15-debugging-under-time.json | quiz.q-overflow.slow.why | Adding 2e5 numbers takes microseconds | correct | About 1e5 to 1e6 additions per millisecond; order of 100 microseconds |
| l15-debugging-under-time.json | quiz.q-equal | 5 5 separates >= from > | correct | Direct |
| l15-debugging-under-time.json | quiz.q-stale | A global never cleared shows from the second test case on | correct | Direct |
| l15-debugging-under-time.json | quiz.q-adjacent | [3, 2, 1] gives 2; the smallest failing case has three values | correct | script; for n = 2 neighbours are all pairs |
| l16-upsolving.json | screens[0] | Upsolve D and E before a new round; reading without writing does not make the idea yours | correct | Course convention on training; standard competitive-programming advice (Halim, Competitive Programming, ch. 1) |
| l16-upsolving.json | screens[1].canvas | Double loop over cuts; test 9 is 200,000 zeros with answer 19,999,700,001 | correct | script: C(199999, 2) |
| l16-upsolving.json | screens[1].widget.answer | Five zeros: 6 ways, 2 of the 4 gaps | correct | C(4, 2); script test 2 |
| l16-upsolving.json | screens[1].feedback.byKey | 10 is C(5,2); 3 is for four zeros | correct | Arithmetic |
| l16-upsolving.json | screens[1].explain | About 2e10 pairs; the answer overflows a 32-bit int | correct | 19,999,700,001 > 2^31 - 1 |
| l16-upsolving.json | screens[1].canvas editorial | Cuts i < j work when P[i] = S/3 and P[j] = 2S/3; count earlier i at each good j | correct | Codeforces 466C 'Number of Ways' editorial idea; script |
| l16-upsolving.json | screens[2].prose | Upsolving: solving after the round what you could not solve in time; use the editorial for the idea, never to copy | correct | Standard usage of the term on Codeforces |
| l16-upsolving.json | screens[2].widget.answer | Idea, own code, accepted, write-up and log, redo a week later | correct | Each step needs the one before; unique order |
| l16-upsolving.json | screens[2].explain | The redo a week later is the app's redo rhythm and the curriculum's weekly review block | correct | docs/PLAN.md: redo queued for 7 days; docs/curriculum.md weekly rhythm: redo one week later |
| l16-upsolving.json | screens[3].prose | Problem D is about 1600 | unverified | An estimate; the problem it follows (Codeforces 466C, Number of Ways) carries a site rating near 1700 from memory, not checked online |
| l16-upsolving.json | screens[3].widget | equal_thirds in one pass; 9 tests | correct | script: solution passes; 0.13 s in Pyodide |
| l16-upsolving.json | screens[3].feedback.byKey.test-2 | With S = 0 count the first cut only after checking the second | correct | script: counting first fails first at test 2 (10 against 6) |
| l16-upsolving.json | screens[3].feedback.byKey.test-5 | Total 2 is not divisible by 3: return 0 | correct | script: no divisibility test fails first at test 5 |
| l16-upsolving.json | screens[3].feedback.byKey.test-6 | Do not stop at the first match | wrong | script FINDING 3: stopping at the first match fails test 1 (1 against 2); the bug that fails first at test 6 is stopping once the prefix passes 2S/3 |
| l16-upsolving.json | screens[3].feedback.byKey.test-8 | A double loop over cuts is about 2e10 steps | correct | script: passes tests 1 to 7, times out at test 8 |
| l16-upsolving.json | screens[3].explain | Checking 2S/3 before adding S/3 stops a zero total pairing a cut with itself; C++ needs long long | correct | Derivation; count exceeds 2^31 - 1 |
| l16-upsolving.json | screens[4] | Log counts 3, 2, 2, 1; eight in all | correct | script |
| l16-upsolving.json | screens[5].widget | mistakes_summary sorts by (-count, name) | correct | script: solution passes 8 tests |
| l16-upsolving.json | screens[5].feedback.byKey.test-1 | Tie at 2 broken alphabetically | correct | script: count-only sort fails test 1 |
| l16-upsolving.json | screens[5].feedback.byKey.test-2 | Empty log returns an empty list | correct | script: max() of an empty log fails first at test 2 |
| l16-upsolving.json | screens[5].feedback.byKey.test-6 | Python sorts capitals before lower case; leave names as they are | correct | Code point order; script: case-insensitive sort fails first at test 6 |
| l16-upsolving.json | screens[5].feedback.byKey.test-7 | Sort by count first, then name | correct | script: name-only sort passes tests 1 to 6 and fails at 7 |
| l16-upsolving.json | screens[6].prose | Upsolve problems at most about 300 above your rating | correct | Stated as this lesson's assumption in the explain |
| l16-upsolving.json | screens[6].widget.answer | C 1400 and D 1500 for a rating of 1,200 | correct | 1200 + 300; E and F are 700 and 1,200 above |
| l16-upsolving.json | screens[7].prose | The curriculum asks for one contest a week once 100 problems are behind you | correct | docs/curriculum.md 2.4 |
| l16-upsolving.json | screens[7].options.hard.why, hints | Practise about 100 to 200 above your rating | unverified | A common rule of thumb in Codeforces training posts; not in the curriculum and not established; the 300 rule is flagged as an assumption, this one is not |
| l16-upsolving.json | screens[7].options | 2000 is 750 above 1,250; 1350 to 1450 is 100 to 200 above | correct | Arithmetic |
| l16-upsolving.json | screens[7].explain | Project Euler adds maths with code, as the curriculum suggests | correct | docs/curriculum.md 2.4 'Add' |
| l16-upsolving.json | screens[8] | Read is not solved: only accepted code and a later redo count | correct | Course convention, consistent with screens[2] |
| l16-upsolving.json | screens[9] | The weekly loop: round, upsolve, write up, log, redo | correct | Restates the level |
| l16-upsolving.json | screens[10].prose | The curriculum sets 1,400 as a first-year target, treats rating shortlists as mainly Indian campus practice, counts a rating for developer applications | correct | docs/curriculum.md 2.4, lines 226 to 227: the attribution is exact |
| l16-upsolving.json | screens[10].prose | The underlying hiring facts (where a rating counts) | unverified | Attributed to the curriculum, which gives no source; cannot be established here |
| l16-upsolving.json | screens[10].canvas | Track table: developer algorithms, C++, systems design; trader probability, mental arithmetic, market-making games; researcher statistics, machine learning, a data take-home | correct | docs/curriculum.md track table (abridged: it adds betting games, probability and regression) |
| l16-upsolving.json | screens[10].prose | The curriculum's coding aim is a fresh LeetCode medium in 30 minutes | correct | docs/curriculum.md line 157 |
| l16-upsolving.json | screens[11].canvas | Additions: IMC Prosperity for traders, Kaggle for researchers, Project Euler for everyone | correct | docs/curriculum.md 2.4 'Add'; IMC Prosperity is IMC Trading's competition |
| l16-upsolving.json | screens[11].options.cut.why | Write-ups show how you think, which interviewers do read about | unverified | A hiring claim with no source |
| l16-upsolving.json | screens[11].feedback.byKey.rating | Another 390 rating points | correct | 1800 - 1410 |
| l16-upsolving.json | summary.ideas | Upsolve after every round; log; redo; 300 above; 1,400 target | correct | Restates the screens |
| l16-upsolving.json | summary.formula | ways = sum over j with P_j = 2S/3 of #{i < j : P_i = S/3} | imprecise | script FINDING 8: no limit j <= n - 1 (or i >= 1); on a zero total P_n = 2S/3 too, giving 10 for five zeros against 6 |
| l16-upsolving.json | quiz.q-zeros | Four zeros: 3 ways | correct | C(3, 2) |
| l16-upsolving.json | quiz.q-range | 1700 is within 300 of 1,500; 2100 is 600 above | correct | Arithmetic |
| l16-upsolving.json | quiz.q-sort | [('edge case', 2), ('misread', 2), ('overflow', 1)] | correct | Key (-count, name) |
| l16-upsolving.json | quiz.q-trader | By the table, trader interviews test probability, mental arithmetic and market-making games | correct | Internal reference to screens[10] |
| review-4.json | items[0] r4-pattern | Smallest daily limit paying n redemptions in order over k days: binary search with a greedy check | correct | Same monotone predicate as l13 C |
| review-4.json | items[0].options.brute.why | A scan is correct but slow: up to about 2e14 limits | correct | 2e5 * 1e9 |
| review-4.json | items[1] r4-log | 18 of 60 minutes is 30%; slips 50% and 60% | correct | script; grade-all |
| review-4.json | items[2] r4-decay | 1500 - 288 - 100 = 1,112, above the floor of 450 | correct | script |
| review-4.json | items[3] r4-swap | Q then P scores 20 more: waits cost 60 against 80 | correct | script |
| review-4.json | items[4] r4-hand | [5] returns 0; [2,2,2] returns 4; an empty list hides the bug | correct | script |
| review-4.json | items[5] r4-type | The count needs long long; a double holds it exactly here; about nine times 2^31 - 1 | correct | script: below 2^53; ratio 9.31; long long is 64 bits on wasm32 where long is 32 |
| review-4.json | items[6] r4-upsolve | 1500 and 1600 for a rating of 1,350; 550 and 950 above for the others | correct | Arithmetic |
| review-4.json | items[7] r4-late | E solved at minute 115 scores 675; the score decays from minute 0 | correct | 1250 - 5 * 115; rule of l14 screens[0] |
| homework-4.json | items[0].prose | Groups after removing link number `cut`; self-links and repeats allowed; about 1300 | correct | Connected components; rating is an estimate (see the unverified rating rows) |
| homework-4.json | items[0].widget | BFS from each unseen desk; 8 tests | correct | script: solution passes; 0.65 s in Pyodide |
| homework-4.json | items[0].widget.how | A recursive DFS goes 100,000 deep, past the 3,000 nested calls this page allows (Python's default is 1,000) | correct | drill-worker.js RECURSION_LIMIT = 3000; piece of 100,001 desks; script |
| homework-4.json | items[0].feedback.byKey.test-2 | Each isolated desk is a group of its own: 3 | correct | script: counting only linked desks fails first at test 2 |
| homework-4.json | items[0].feedback.byKey.test-4 | Cutting one copy of a repeated link leaves the other | correct | script: removing by value fails first at test 4 |
| homework-4.json | items[0].feedback.byKey.test-7 | Use a queue or an explicit stack, not deep recursion | correct | script: a recursive DFS fails first at test 7 with RecursionError |
| homework-4.json | items[0].explain | O(n + m); the queue never recurses | correct | BFS bound |
| homework-4.json | items[1].prose | At most k trades, one unit, same-day sale and purchase allowed, O(nk) | correct | LeetCode 188 'Best Time to Buy and Sell Stock IV' |
| homework-4.json | items[1].widget | buy[j], sell[j] DP; 8 tests | correct | script: solution passes; in-place update allows a same-day sale and purchase, as the prose states |
| homework-4.json | items[1].feedback.byKey.test-3 | No trades allowed: 0 | correct | script: tables of size k fail first at test 3 |
| homework-4.json | items[1].feedback.byKey.test-4 | Prices only fall: do not trade | correct | script: forcing exactly k trades fails first at test 4 |
| homework-4.json | items[1].feedback.byKey.test-6 | Ten trades allowed but only three rises help: 2 + 3 + 4 = 9 | correct | Arithmetic; the line names no mistake, so no submission was written for it |
| homework-4.json | items[1].feedback.byKey.test-8 | Every pair of days for each trade is O(n^2 k), about 2e9 steps | correct | script: passes tests 1 to 7, times out at test 8 |
| homework-4.json | items[1].explain | O(nk), here 2e5 updates | correct | 1e4 * 20 |
| homework-4.json | items[2].prose | Maximise the smallest distance between m bots on distinct levels; example gives 3 | correct | 'Aggressive cows' (SPOJ AGGRCOW); script |
| homework-4.json | items[2].widget | Sort, binary search the distance, greedy check; 8 tests | correct | script: solution passes; 0.78 s in Pyodide |
| homework-4.json | items[2].feedback.byKey.test-1 | The levels are not sorted: sort before the greedy check | correct | script: no sort fails test 1 |
| homework-4.json | items[2].feedback.byKey.test-4 | Three equal levels and two bots: 0 | correct | script: starting the search at 1 fails first at test 4 |
| homework-4.json | items[2].feedback.byKey.test-8 | About 30 greedy checks, not every distance | correct | script: a scan upwards times out at test 8 |
| homework-4.json | items[2].explain | If d can be kept so can every smaller; greedy places each bot on the first level at least d above the last | correct | Monotone predicate; greedy stays-ahead |
| homework-4.json | items[3] hw4-first10 | Open all, read constraints, name patterns, rank, restate, code | correct | Each step needs the one before; matches l13 screens[9] and l14 |
| homework-4.json | items[4] hw4-penalty | Penalty 269; E's rejections do not count | correct | script |
| homework-4.json | items[5] hw4-track | For a trader application the rating does least | correct | Internal reference to l16 screens[10]; underlying hiring claim is the unverified row there |
| homework-4.json | items[6].widget.model | Alex's log: A 9, B 17, C 27 minutes, 7 left for D; ideas and complexities of A to D | correct | script: sums of l13 screens[8]; matches the four solutions |
| homework-4.json | items[6].widget.model | C: 'my check let an order heavier than the van start a new day' | correct | A plausible bug (see finding 4: the hidden tests would not catch its commonest form) |
| homework-4.json | items[6].widget.rubric | Practice 100 to 200 above the rating | unverified | Same rule of thumb as l16 screens[7] |

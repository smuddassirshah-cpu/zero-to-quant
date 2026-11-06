# Claim ledger: coding-int level 4 (blind concept audit)

Files: `app/content/courses/coding-int/` l15 to l19, review-4, homework-4. Script: `docs/reports/coding-int-L4-concepts.py` (`sim:` rows name its check message). Sources: CLRS = Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* 3e; Laaksonen = *Competitive Programmer's Handbook*; Beck = *Test-Driven Development by Example*; Python docs = *The Python Language Reference* 6.7 (binary arithmetic); ISO C++ = [expr.mul]/4; AUTHORING = `docs/AUTHORING.md`.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l15 | screens[0].prose | Reported assessments set two problems in 60 minutes or three in 90; platforms differ on scoring test groups versus whole problems | unverified | hedged as "Reported"; no source in the lesson; consistent with `exams/mock-oa-code.json` `models` line, itself candidate reports |
| l15 | screens[0].prose | Partial credit and a minute budget are new relative to contests l14-which-first | correct | contests/l14-which-first.json exists; cross-reference only |
| l15 | screens[0].question, options | P1 at 40/20 = 2.0 points a minute beats P3 at 1.8 and P2 at 1.71 | correct | sim: l15 screens[0] rates |
| l15 | screens[0].options[1..3].why, feedback.byKey, explain | Rates 2.0, 1.71, 1.8; the biggest score is not the best rate | correct | 60/35 = 1.714, 90/50 = 1.8; sim: l15 screens[0] rates |
| l15 | screens[0].hints | Rate is full score over full minutes | correct | definition stated in summary.formula |
| l15 | screens[1].prose, hints, explain | Greedy by rate taking whole problems and skipping any that no longer fits earns P1 then P2 = 100 in 55 minutes; P3 is skipped as 42 < 50 | correct | sim: l15 screens[1] greedy by rate earns 100 |
| l15 | screens[1].feedback.byKey.over/all/one | P1+P3 need 70 > 62; all three need 105; after P1, P2 fits | correct | 20+50, 20+35+50, 62-20 = 42 >= 35 |
| l15 | screens[2].rows, hints, explain | Best full/partial/skip plan in 62 minutes is P3 full + P2 partial: 62 minutes, 115 points; P1 skipped | correct | brute force over 27 plans; sim: l15 screens[2] optimum at 62 minutes is 115, the 115 plan is unique |
| l15 | screens[2].explain | 115 is more than the 100 of full marks alone | correct | sim: l15 screens[1] and [2] |
| l15 | screens[2].feedback.byKey r1c1..r3c2 | P2 partial 12 min/25 pts, P3 full 50/90, totals 62/115 | correct | data lines; 12+50, 25+90 |
| l15 | screens[3].prose | Listing every choice is 3^n plans | correct | three choices per problem; sim: l15 screens[3] prose 3^n |
| l15 | screens[3].canvas, solution | best[m] = most points in at most m minutes; per problem copy the table, try full and partial from the old table, keep the max; return best[budget] | correct | 0/1 knapsack over items with two mutually exclusive sizes, CLRS 16.2 (0-1 knapsack DP, Ex. 16.2-2); sim: l15 screens[3] DP equals brute force on random papers, tests[0..9] |
| l15 | screens[3].tests[0..9].expect | 100, 110, 160, 0, 20, 0, 40, 30, 80, 2724 | correct | brute force on tests 0 to 8; seed-1 test agrees with the solution and with an independent memoised DP (sim: l15 screens[3] tests[i]) |
| l15 | screens[3].starter | The starter (returns 0) fails | correct | sim: l15 screens[3] starter fails test 1 |
| l15 | screens[3].hints | best[m] is 0 before any problem; a problem can only improve it; copy, try both prices from best[m - minutes], return best[budget] | correct | DP initialisation and transition as above |
| l15 | screens[3].feedback.byKey.test-1 | For the test paper at 55 minutes, P3 full + P2 partial = 100 | correct | 45+10 = 55, 80+20 = 100; brute force |
| l15 | screens[3].feedback.byKey.test-5 | At 14 minutes only a partial fits | correct | partials cost 5, 10, 15; two partials need 15 > 14; brute force gives 20 |
| l15 | screens[3].feedback.byKey.test-7 | When the partial costs as much as the full, take the full | correct | [[40,20,10,20]] at 20: 40 > 10 |
| l15 | screens[3].feedback.byKey.test-8 | The partial costs 5 and fits in 10 | correct | [[40,20,30,5]] at 10 gives 30 |
| l15 | screens[3].feedback.byKey.test-10 | Trying every choice on 60 problems would take 3^60 steps | correct | 3^n with n = 60 |
| l15 | screens[3].explain | Work is problems times budget; choosing from the old copy stops one problem being used twice | correct | counter equals n x (budget+1) (sim: l15 screens[3] explain: work is problems x budget); reading `best` not `new` is the 0/1 (not unbounded) knapsack transition, CLRS 16.2 |
| l15 | screens[4].prose, options[0] | Full-only plan earns 100 here; P3 full + P2 partial earns 115 | correct | sim: l15 screens[1], [2] |
| l15 | screens[4].options[2].why, byKey.c | P1 and P3 in full need 70 > 62 | correct | 20+50 |
| l15 | screens[4].options[3].why, byKey.d | The partials of P1 and P2 pay 2.0 and 2.08 a minute, as good as any full | correct | 12/6 = 2.0, 25/12 = 2.083; fulls are 2.0, 1.71, 1.8; sim: l15 screens[4] byKey d |
| l15 | screens[4].explain | A plan with no partials cannot reach 115 | correct | full-only plans: max 100 by enumeration (sim: l15 screens[1]) |
| l15 | screens[5].prose | Count about 10^8 steps a second | correct (stated convention) | Laaksonen ch. 2 ("some hundreds of millions of simple operations per second"); the lesson flags it as the contests l2 convention |
| l15 | screens[5].rows, hints, byKey | O(n^2) passes only n <= 1,000 (10^6, 10^10, 10^12 steps); O(n log n) and O(n) pass all three; n log n at 10^6 is about 2 x 10^7 | correct | 10^6 log2 10^6 = 1.99 x 10^7; sim: l15 screens[5] quadratic step counts, n log n at 1e6 |
| l15 | screens[5].explain | The quadratic solution scores the small group and stops there | correct | under group scoring; follows from the step counts |
| l15 | screens[6].answer, hints, byKey, explain | Read every statement, note limits and points, estimate minutes, rank by rate and settle partials, set time boxes, then start | correct (method, internally consistent) | each step needs the previous one's output; matches the lesson's own planning method and the summary |
| l15 | screens[7].prose, answer, same | Update for one problem: copy best into new (the skip), try full and partial from the old table, keep the larger, replace best | correct | same transition as screens[3]; `same` allows s2 and s3 in either order, which the code's max makes order-free |
| l15 | screens[7].byKey.s5, explain | Swapping before the pass ends breaks the table; each price looks back in the old table so a problem is used at most once | correct | 0/1 knapsack reasoning as above |
| l15 | screens[8].prose, answer, hints, explain | At 58 minutes the greedy still earns 100; the best plan is P3 full + P1 partial = 102 in 56 minutes; all 27 choices agree | correct | sim: l15 screens[8] optimum at 58 minutes is 102, greedy still 100, 27 choices |
| l15 | screens[8].byKey.same/greedy/low | P3 full + P2 partial needs 62 > 58; greedy plan is P1+P2 in 55; P3 alone leaves 8 minutes for P1's partial | correct | 50+12, 20+35, 58-50 = 8 >= 6 |
| l15 | screens[9].prose, options, byKey, explain | Two-problem bank paper in 55 minutes: A full + B partial = 55 min, 75 points is the maximum; B full + A partial needs 57; both full need 85; both partial leaves 28 idle | correct | brute force over 9 plans; sim: l15 screens[9] bank paper optimum 75 |
| l15 | screens[9].explain | `#exam/mock-oa-code` is two Python problems in 60 minutes and scores a problem only when every hidden test passes | correct | `exams/mock-oa-code.json` models and description lines say so |
| l15 | summary.ideas[2], formula | Check the scoring rule first; rank by rate, then check that a partial does not fill a gap better | correct | the lesson's screens[2], [8] show rate-greedy beaten by a partial filling the gap |
| l15 | summary.trap | Allowing no partial credit leaves minutes unspent | correct | screens[1] vs [2]: 55 of 62 used vs 62 of 62 |
| l15 | quiz[0] q-rate | Y at 28/14 = 2.0 beats X at 36/24 = 1.5 | correct | sim: l15 quiz q-rate rates |
| l15 | quiz[0].options[3].why | Taking longer lowers the rate | correct | rate = points/minutes, decreasing in minutes |
| l15 | quiz[1] q-budget | 80 - 5 - 5 = 70 | correct | sim: l15 quiz q-budget |
| l15 | quiz[2] q-group | n^2 passes n <= 2,000 (4 x 10^6) not n <= 300,000 (9 x 10^10) | correct | sim: l15 quiz q-group step counts |
| l15 | quiz[2].options[1].why, byKey.b | A correct but slow solution fails the large group by time | correct | 9 x 10^10 steps at 10^8/s is 900 s |
| l15 | quiz[2].options[2].why | Not every quadratic solution is too slow: 4 x 10^6 steps is quick | correct | 0.04 s at 10^8/s |
| l15 | quiz[3] q-partial | With 8 minutes left only the 5-minute partial (12 points) fits; full marks needs 25 | correct | arithmetic |

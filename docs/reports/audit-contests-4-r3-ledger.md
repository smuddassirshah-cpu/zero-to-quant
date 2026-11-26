# Claim ledger: contests level 4, audit round 3

Blind ledger, written before any earlier review, audit or author report was opened. Scope: `l13-virtual-contest`, `l14-which-first`, `l15-debugging-under-time`, `l16-upsolving`, `review-4`, `homework-4` (no `problems-*` file exists for level 4). Stage 2 course, so the ledger is full: every prose, statement line, option, why, hint, feedback line, how-note, accept note, explanation, summary line, rubric line and model answer has a row. Statement lines repeated on later canvases have one row.

Rows: 951. Verdicts: correct 948, imprecise 2, misleading 1; wrong 0, unverified 0.

"Script" is `docs/reports/contests-L4-concepts-r3.py`; the quoted words are the names of its checks. "Sweep" is part C of that script: natural codings of the mistake a `test-N` line names, graded by the page's own harness under Pyodide 0.27.7 (`tools/code-runner.mjs`) and again in CPython.

## Bases

Each row's basis is a key into this table (file/screen, item or quiz index), or, for a `test-N` line, the sweep result written in the row.

| Key | Basis |
|---|---|
| l13/0 | Derivation: C asks for the least capacity with a monotone yes/no test, the shape of binary search on the answer (Laaksonen, Competitive Programmer's Handbook, ch. 3); A is one pass, B a sliding window (ch. 8), D a BFS (CLRS 22.2). Tap ids l2 to l5 are lines A to D of the canvas. |
| l13/1 | Statement rule 1 < i < n and its note; script checks 'l13 s1 key', 'slip ends', 'slip valley'. |
| l13/2 | Codeforces Help, 'virtual participation'; docs/curriculum.md line 226 (one contest a week); screens 3 to 6 state estimates 800, 1100, 1300, 1500. |
| l13/3 | Statement (strictly above both neighbours, ends excluded); script 'l13 statement example' and the sweep of 14 codings. |
| l13/4 | Sliding window, each element enters and leaves once, O(n) (Handbook ch. 8); script 'l13 B example', 's4 explain', 's4 how'; sweep. |
| l13/5 | Binary search on the answer (Handbook ch. 3); the greedy fill uses the fewest days by an exchange argument; script 'l13 C example', 's5 how/explain', 'summary formula'; sweep. |
| l13/6 | BFS gives fewest moves in a unit-cost graph in O(V + E) (CLRS 22.2); script 'l13 D example', 'D test-1 line', 'D explain', 'test 2'; sweep. |
| l13/7 | Arithmetic on the six log lines; script 'l13 trap'. The advice (read first, easy first) is the level's routine, a judgement. |
| l13/8 | Column sums; script 'l13 log totals'. |
| l13/9 | Restates screens 0 to 8; the 15-minute cap is this course's rule, stated as such. |
| l13/10 | Same routine applied; 75 / 3 = 25 minutes a problem, 4 / 25 is about a sixth. |
| l13/summary | Restates screens 0 to 9; formula checked in script 'l13 summary formula'. |
| l13/q0 | Script 'l13 q-capacity'. |
| l13/q1 | Script 'l13 B example', 'q-cover'. |
| l13/q2 | Script 'l13 q-plateau key', 'q-plateau slips'. |
| l13/q3 | Script 'l13 q-boxed / test 2'. |
| l14/0 | Codeforces rules: in a two-hour round a problem loses 1/250 of its value a minute, 50 per unsuccessful attempt, floor 30% (the lesson flags the numbers as its illustration). Order: Smith's rule, weighted shortest processing time (Smith 1956; Pinedo, Scheduling, sec. 3.1); script 'l14 s0 key' (all 24 orders). |
| l14/1 | Script 'l14 s1 bars' (three orders) and 's1 explain'. |
| l14/2 | Script 'l14 s2 rates'. Smith's ratio rule. |
| l14/3 | Script 'l14 s3 key and slips', 's3 explain' (120 / 250 = 48%). |
| l14/4 | Script sweep (6 codings); tests recomputed with the solution under Pyodide (all pass). |
| l14/5 | ICPC World Finals rules: rank by problems solved, then total time, 20 penalty minutes per rejected run on a solved problem; script 'l14 s5', sweep. |
| l14/6 | Calculus: E'(x) = 20 e^(-x/50) - (160/3) e^(-(60-x)/15) = 0 at x = 34.84; exponential solve times are memoryless, so E first until solved then D is the best adaptive plan (constant hazards 53.3 against 20 points a minute); script 'l14 s6 key', 's6 explain', Monte Carlo (400,000 rounds). |
| l14/7 | Sunk cost: only future costs and gains bear on a choice (any decision-theory text, e.g. Mankiw, Principles of Economics, ch. 13); the 50-point rejection and 'unsolved scores 0' follow the rule on screen 0. |
| l14/8 | Solve counts as evidence of difficulty: 702 / 96 is about 7.3. A judgement, consistent with Codeforces practice. |
| l14/9 | Adjacent exchange argument (Pinedo sec. 3.1); script 'l14 s9 key', 's9: points-per-minute order is optimal' (300 random rounds against brute force). |
| l14/10 | Script 'l14 s10'; 4! = 24 and 6! = 720 orders; sweep (11 codings). |
| l14/11 | Script 'l14 transfer'. |
| l14/summary | Restates screens 0 to 9; formula from screen 9. |
| l14/q0 | Script 'l14 q-floor'. |
| l14/q1 | Script 'l14 q-icpc'. |
| l14/q2 | Script 'l14 q-rate'. |
| l14/q3 | Sunk cost, as screen 7. |
| l15/0 | Trace: range(len(xs) - 2, -1, -1) starts at n - 2; script 'l15 s0', 's1 table'. Canvas line ids l5 to l9 are the five code lines. |
| l15/1 | Script 'l15 s1 table' (the starter run on the four cases). |
| l15/2 | The order is by cost of the check, the lesson's own routine; stress testing is lesson 4 (Handbook ch. 1 names the same checks). |
| l15/3 | Sweep (5 codings); range(-1, -1, -1) is empty in Python. |
| l15/4 | Definition of an inversion, i < j and x_i > x_j, strict (CLRS problem 2-4); script 'l15 s4'; sweep (5 codings). |
| l15/5 | Module-level state persists between cases and, on this page, between tests (seen under Pyodide: the starter gives [2, 3] on test 2); sweep (9 codings). |
| l15/6 | Judges compare standard output only; standard error is discarded (Codeforces and ICPC judging; Kattis help 'Output'). Writing to stderr still costs time. |
| l15/7 | Python docs, sys.getrecursionlimit: default 1000 (asserted in the script's child process). Under this app's Pyodide 0.27.7 in node (tools/code-runner.mjs), sys.setrecursionlimit(10**6) ran a line DFS of 100,000 and plain recursion of 999,900 frames; Chrome not run. CPython before 3.11 overflows the C stack on deep recursion, so 'some judges' is right. |
| l15/8 | Restates the routine; a failing hand case is already a minimal input. |
| l15/9 | Script: tests pass with the solution; Monte Carlo 'l15 s9 test-6 line'; sweep (10 codings). |
| l15/10 | Idempotence of replay: applying a fill twice doubles the position; analogy to the n = 1 hand case. |
| l15/summary | Restates screens 0 to 9. |
| l15/q0 | Script 'l15 q-overflow'; int is 32 bits and long long 64 on x86-64 and on the page's wasm32 clang (ISO C++ [basic.fundamental] minimums; both ABIs). |
| l15/q1 | 5 >= 5 is true, 5 > 5 false. |
| l15/q2 | As screen 5. |
| l15/q3 | Script 'l15 q-adjacent'. |
| l16/0 | Study-method judgement: unsolved problems mark the edge of ability (deliberate practice, Ericsson et al. 1993). Not an empirical claim the lesson quantifies. |
| l16/1 | Counting: with all zeros every pair of the n - 1 gaps works, C(n - 1, 2); script 'l16 s1 key', 'test 9 answer'. |
| l16/2 | Retrieval practice: rebuilding from memory is retained better than rereading (Roediger and Karpicke 2006); the weekly redo is the curriculum's review block. |
| l16/3 | Classic prefix-count solution (Codeforces 466C, Number of Ways): script 'l16 s3: one-pass count equals the double loop' (2,000 random cases), 's3 lines'; sweep (11 codings). |
| l16/4 | Script 'l16 s4 tally'. |
| l16/5 | Python sorts tuples lexicographically and upper case before lower case (code points); script 'l16 q-sort key'; sweep (11 codings). |
| l16/6 | The lesson's rule of thumb, stated as an assumption; arithmetic in script 'l16 ratings'. |
| l16/7 | docs/curriculum.md line 226 (one contest a week after 100 problems) and 228 (Project Euler); the 100-to-200 band is labelled the lesson's own rule; script 'l16 ratings'. |
| l16/8 | As screen 2: reading without writing is not retrieval; a judgement the level states consistently. |
| l16/9 | Restates screens 0 to 8. |
| l16/10 | docs/curriculum.md lines 157, 192 to 194, 226 and 227 (the table abridges the track rows). |
| l16/11 | docs/curriculum.md line 228 (Kaggle, IMC Prosperity, Project Euler); 1,800 - 1,410 = 390. |
| l16/summary | Restates screens 0 to 10; formula is screen 3's count. |
| l16/q0 | Script 'l16 q-zeros key'. |
| l16/q1 | Script 'l16 ratings'. |
| l16/q2 | Script 'l16 q-sort key'. |
| l16/q3 | docs/curriculum.md line 192. |
| review-4/0 | As l13 screen 5; script 'r4-pattern'. |
| review-4/1 | Script 'r4-log'. |
| review-4/2 | Script 'r4-decay'. |
| review-4/3 | Script 'r4-swap'. |
| review-4/4 | Script 'l15 r4-hand'. |
| review-4/5 | Script 'l16 test 9 answer' (above 2^31 - 1, exact in a double, below 2^53). |
| review-4/6 | Script 'r4-upsolve'. |
| review-4/7 | Script 'r4-late'. |
| homework-4/0 | Connected components by BFS, O(n + m) (CLRS 22.2); example 2 fixes that links count from 0; script 'hw4-desks'; sweep (10 codings; the recursive DFS also passes with sys.setrecursionlimit(10**6) under Pyodide in node). |
| homework-4/1 | State DP over (trades used, holding), the standard solution of 'best time to buy and sell stock IV'; script 'hw4-ktrades' (DP against a brute force on 1,500 cases), 'sizes'; sweep (11 codings). |
| homework-4/2 | Binary search on the answer with a greedy check (the 'aggressive cows' problem, SPOJ AGGRCOW); script 'hw4-gap' (against a brute force on 800 cases); sweep (7 codings). |
| homework-4/3 | Restates l13 screen 9 and l14's ranking; an ordering by the level's routine. |
| homework-4/4 | Script 'hw4-penalty'. |
| homework-4/5 | docs/curriculum.md lines 192, 227, 228. |
| homework-4/6 | Model answer checked against l13 screen 8's log (script 'l13 homework model minutes'), the screens' complexities and docs/curriculum.md lines 226 to 228. |

## Rows

| File | JSON path | Claim | Verdict | Basis |
|---|---|---|---|---|
| l13-virtual-contest.json | screens[0].prose | This lesson is a virtual contest: four problems, A to D, in 60 minutes. The lesso... | correct | l13/0 |
| l13-virtual-contest.json | screens[0].canvas.params.lines[0] | Virtual round · 4 problems · 60 minutes | correct | l13/0 |
| l13-virtual-contest.json | screens[0].canvas.params.lines[1] | A Local peaks days above both neighbours | correct | l13/0 |
| l13-virtual-contest.json | screens[0].canvas.params.lines[2] | B Every ticker shortest run holding every name | correct | l13/0 |
| l13-virtual-contest.json | screens[0].canvas.params.lines[3] | C Shipping smallest van for k days | correct | l13/0 |
| l13-virtual-contest.json | screens[0].canvas.params.lines[4] | D Courier fewest moves across a city grid | correct | l13/0 |
| l13-virtual-contest.json | screens[0].hints[0].text | Which problem asks for the smallest value that still works? | correct | l13/0 |
| l13-virtual-contest.json | screens[0].hints[1].text | A bigger van always works if a smaller one does. | correct | l13/0 |
| l13-virtual-contest.json | screens[0].hints[2].text | C asks for the smallest capacity, and every larger capacity also works. That is t... | correct | l13/0 |
| l13-virtual-contest.json | screens[0].feedback.correct | C: the smallest capacity that works, and every larger one works too. | correct | l13/0 |
| l13-virtual-contest.json | screens[0].feedback.generic | Not quite right. Look for a smallest value with a yes-or-no test. | correct | l13/0 |
| l13-virtual-contest.json | screens[0].feedback.byKey.l2 | You tapped A. Counting peaks is one pass over the closes. | correct | l13/0 |
| l13-virtual-contest.json | screens[0].feedback.byKey.l3 | You tapped B. A shortest run holding every name is a sliding window. | correct | l13/0 |
| l13-virtual-contest.json | screens[0].feedback.byKey.l5 | You tapped D. Fewest moves on a grid is a breadth-first search. | correct | l13/0 |
| l13-virtual-contest.json | screens[0].feedback.byKey.l1 | That is the round's header line. | correct | l13/0 |
| l13-virtual-contest.json | screens[0].explain.text | Naming each problem's pattern takes a minute and shapes the hour. A is a loop, B ... | correct | l13/0 |
| l13-virtual-contest.json | screens[1].prose | Before coding anything, read all four statements, constraints first. Slide throug... | correct | l13/1 |
| l13-virtual-contest.json | screens[1].canvas.params.lines[0] | A. Local peaks (1 s, 256 MB) | correct | l13/1 |
| l13-virtual-contest.json | screens[1].canvas.params.lines[1] | A desk logs n daily closes c₁ … cₙ. Day i is a peak if 1 < i < n and cᵢ is strict... | correct | l13/1 |
| l13-virtual-contest.json | screens[1].canvas.params.lines[2] | Input: n (1 ≤ n ≤ 2·10⁵), then c₁ … cₙ (≤ 10⁹). | correct | l13/1 |
| l13-virtual-contest.json | screens[1].canvas.params.lines[3] | Output: the number of peaks. | correct | l13/1 |
| l13-virtual-contest.json | screens[1].canvas.params.lines[4] | Example: 3 5 4 6 2 → 2 | correct | l13/1 |
| l13-virtual-contest.json | screens[1].canvas.params.lines[5] | Note: the first and last days are never peaks. | correct | l13/1 |
| l13-virtual-contest.json | screens[1].widget.accept | 0: day 2 is below both neighbours, and days 1 and 3 are ends. | correct | l13/1 |
| l13-virtual-contest.json | screens[1].hints[0].text | Which days can be peaks at all? | correct | l13/1 |
| l13-virtual-contest.json | screens[1].hints[1].text | The note: the first and last days are never peaks. | correct | l13/1 |
| l13-virtual-contest.json | screens[1].hints[2].text | Only day 2 could be a peak, and its close 1 is below both neighbours. So there ar... | correct | l13/1 |
| l13-virtual-contest.json | screens[1].feedback.correct | None: the ends never count, and day 2 is a dip. | correct | l13/1 |
| l13-virtual-contest.json | screens[1].feedback.generic | Not quite right. Apply the note, then check day 2. | correct | l13/1 |
| l13-virtual-contest.json | screens[1].feedback.byKey.ends | You counted both ends, which are above their one neighbour. The note says the end... | correct | l13/1 |
| l13-virtual-contest.json | screens[1].feedback.byKey.valley | You counted day 2, but 1 is below 5 on both sides. | correct | l13/1 |
| l13-virtual-contest.json | screens[1].explain.text | The rule $1 < i < n$ and the note both rule out the ends. Reading that line now s... | correct | l13/1 |
| l13-virtual-contest.json | screens[2].prose | What you are sitting is a **virtual contest**: a past round, alone, at its full l... | correct | l13/2 |
| l13-virtual-contest.json | screens[2].widget.options[0].text | Keep the 60-minute clock | correct | l13/2 |
| l13-virtual-contest.json | screens[2].widget.options[1].text | Judge your code on hidden tests | correct | l13/2 |
| l13-virtual-contest.json | screens[2].widget.options[1].why | You chose testing, but each code screen runs hidden tests, as a judge does. | correct | l13/2 |
| l13-virtual-contest.json | screens[2].widget.options[2].text | Give you the statements | correct | l13/2 |
| l13-virtual-contest.json | screens[2].widget.options[2].why | The statements are on the previous screen. The clock is what is missing. | correct | l13/2 |
| l13-virtual-contest.json | screens[2].widget.options[3].text | Show an approximate difficulty | correct | l13/2 |
| l13-virtual-contest.json | screens[2].widget.options[3].why | Each code screen gives our estimate of its rating, from about 800 to about 1500. | correct | l13/2 |
| l13-virtual-contest.json | screens[2].hints[0].text | What did the first screen ask you to set up? | correct | l13/2 |
| l13-virtual-contest.json | screens[2].hints[1].text | The lesson player has no contest timer. | correct | l13/2 |
| l13-virtual-contest.json | screens[2].hints[2].text | The code screens judge you and the statements are here. Only the clock is yours t... | correct | l13/2 |
| l13-virtual-contest.json | screens[2].feedback.correct | The clock is yours: a timer outside the app. | correct | l13/2 |
| l13-virtual-contest.json | screens[2].feedback.generic | Not quite right. Ask what a lesson screen has no way of doing. | correct | l13/2 |
| l13-virtual-contest.json | screens[2].explain.text | A lesson lets you take as long as you like, which is the opposite of a contest. S... | correct | l13/2 |
| l13-virtual-contest.json | screens[3].prose | Problem A, about 800 on Codeforces' scale by our estimate. Write `peaks(closes)`,... | correct | l13/3 |
| l13-virtual-contest.json | screens[3].widget.how | Problem A, about 800. Check runs 10 hidden tests: the example, $n = 1$ and $n = 2... | correct | l13/3 |
| l13-virtual-contest.json | screens[3].hints[0].text | Which indices can be peaks? | correct | l13/3 |
| l13-virtual-contest.json | screens[3].hints[1].text | Loop $i$ from 1 to $n - 2$ and compare with both neighbours. | correct | l13/3 |
| l13-virtual-contest.json | screens[3].hints[2].text | `for i in range(1, len(closes) - 1)`: count `closes[i] > closes[i - 1] and closes... | correct | l13/3 |
| l13-virtual-contest.json | screens[3].feedback.correct | One pass, the ends skipped, strict comparisons. | correct | l13/3 |
| l13-virtual-contest.json | screens[3].feedback.generic | Not quite right. Look at the first failing test. | correct | l13/3 |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-3 | Test 3 is 4 9. The last day is never a peak, even when it is above its one neighb... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-4 | Test 4 is 5 1 5. The ends are not peaks, even when they are higher than their one... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-6 | Test 6 is a plateau, 1 3 3 1. Neither 3 is strictly above both neighbours. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-2 | Test 2 is a single close. `range(1, 0)` is empty, so the loop gives 0 without a s... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[3].feedback.byKey.test-5 | Test 5 is four equal closes, 2 2 2 2. No close is strictly above a neighbour, so ... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[3].explain.text | A is an implementation problem: the only traps are the ends and the word *strictl... | correct | l13/3 |
| l13-virtual-contest.json | screens[4].prose | Problem B, about 1100. Write `shortest_cover(tickers, needed)`: the length of the... | correct | l13/4 |
| l13-virtual-contest.json | screens[4].canvas.params.lines[0] | B. Every ticker (1 s, 256 MB) | correct | l13/4 |
| l13-virtual-contest.json | screens[4].canvas.params.lines[1] | A tape lists n trades by ticker, in time order. Find the shortest run of consecut... | correct | l13/4 |
| l13-virtual-contest.json | screens[4].canvas.params.lines[2] | Input: n (1 ≤ n ≤ 2·10⁵), the tape, then m names (1 ≤ m ≤ n; a name may be listed... | correct | l13/4 |
| l13-virtual-contest.json | screens[4].canvas.params.lines[3] | Output: the run's length, or -1 if there is none. | correct | l13/4 |
| l13-virtual-contest.json | screens[4].canvas.params.lines[4] | Example: AAA BBB AAA CCC BBB; BBB CCC → 2 | correct | l13/4 |
| l13-virtual-contest.json | screens[4].widget.how | Problem B, about 1100. Check runs 9 hidden tests: the examples, a missing name, a... | correct | l13/4 |
| l13-virtual-contest.json | screens[4].hints[0].text | Keep a window whose right end moves one trade at a time. | correct | l13/4 |
| l13-virtual-contest.json | screens[4].hints[1].text | Count each needed name inside the window, and how many names have a count above 0. | correct | l13/4 |
| l13-virtual-contest.json | screens[4].hints[2].text | Add `tickers[right]`; while every name is covered, record the length, then drop `... | correct | l13/4 |
| l13-virtual-contest.json | screens[4].feedback.correct | A sliding window: each trade enters once and leaves once. | correct | l13/4 |
| l13-virtual-contest.json | screens[4].feedback.generic | Not quite right. Look at the first failing test. | correct | l13/4 |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-3 | Test 3 needs a name that never trades. Return −1 when no window covers everything. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-5 | Test 5 lists BBB twice. Cover each distinct name once: use `set(needed)`. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-8 | Test 8 counted far more than $4n$ reads. Restarting at every left end rereads the... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[4].feedback.byKey.test-9 | Test 9 is 200,000 trades. A restart at every left end is $O(n^2)$ here, because Z... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test (timing: the slow coding is stopped at 5 s; margin is orders of magnitude); the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[4].explain.text | The window's left end never moves back, so the work is $O(n)$. Here a restart at ... | correct | l13/4 |
| l13-virtual-contest.json | screens[5].prose | Problem C, about 1300. Write `can_ship(weights, k, cap)`, the greedy test of one ... | correct | l13/5 |
| l13-virtual-contest.json | screens[5].canvas.params.lines[0] | C. Shipping (1 s, 256 MB) | correct | l13/5 |
| l13-virtual-contest.json | screens[5].canvas.params.lines[1] | n orders, weights w₁ … wₙ, leave in this order over k days. Each day ships the ne... | correct | l13/5 |
| l13-virtual-contest.json | screens[5].canvas.params.lines[2] | Input: n, k (1 ≤ k ≤ n ≤ 10⁵), w₁ … wₙ (≤ 10⁴). | correct | l13/5 |
| l13-virtual-contest.json | screens[5].canvas.params.lines[3] | Output: the smallest capacity that ships every order within k days. | correct | l13/5 |
| l13-virtual-contest.json | screens[5].canvas.params.lines[4] | Example: 4 8 2 7 5 3 with k = 3 → 12 | correct | l13/5 |
| l13-virtual-contest.json | screens[5].widget.tests | (the 11 hidden tests, against the solution's `if w > cap: return False`) | imprecise | Finding 3. No hidden test needs the guard: the greedy without it passes all 11 and returns True for `can_ship([5, 5], 3, 4)`. Test 4 passes by the day count (2 > 1). Script 'FINDING 3'. Open since round 2, finding 4. |
| l13-virtual-contest.json | screens[5].widget.how | Problem C, about 1300. Check runs 11 hidden tests: the example, `can_ship` on its... | correct | l13/5 |
| l13-virtual-contest.json | screens[5].hints[0].text | If capacity $c$ works, so does every larger one. | correct | l13/5 |
| l13-virtual-contest.json | screens[5].hints[1].text | Greedy test: fill each day until the next order would overflow, then start a new ... | correct | l13/5 |
| l13-virtual-contest.json | screens[5].hints[2].text | Search `lo = max(weights)`, `hi = sum(weights)`: if `can_ship(weights, k, mid)` s... | correct | l13/5 |
| l13-virtual-contest.json | screens[5].feedback.correct | A greedy check inside a binary search: about $\log_2(\text{total})$ checks. | correct | l13/5 |
| l13-virtual-contest.json | screens[5].feedback.generic | Not quite right. Look at the first failing test. | correct | l13/5 |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-4 | Test 4 has an order of 5 and a van of 4. No day can carry it, so return False. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-10 | Test 10 counted more than 13 calls to `can_ship`. Search between the heaviest ord... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-11 | Test 11 has 100,000 orders. Each check is $O(n)$, so the number of checks must be... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 2 failing codings of the named mistake fail first on this test (timing: the slow coding is stopped at 5 s; margin is orders of magnitude); the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-1 | Test 1 expects 12. If you got less, check `can_ship` at 11 by hand: it needs 4 da... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[5].feedback.byKey.test-2 | Test 2 calls `can_ship` alone and asks whether 11 ships in 3 days. Greedily it ne... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[5].explain.text | The answer lies between the heaviest order and the total, and *works* is monotone... | correct | l13/5 |
| l13-virtual-contest.json | screens[6].prose | Problem D, about 1500. Write `grid_moves(grid)`, with `grid` a list of strings. F... | correct | l13/6 |
| l13-virtual-contest.json | screens[6].canvas.params.lines[0] | ..#.> | correct | l13/6 |
| l13-virtual-contest.json | screens[6].canvas.params.lines[1] | .#>.. | correct | l13/6 |
| l13-virtual-contest.json | screens[6].canvas.params.lines[2] | .#.#. | correct | l13/6 |
| l13-virtual-contest.json | screens[6].canvas.params.lines[3] | ...v. | correct | l13/6 |
| l13-virtual-contest.json | screens[6].canvas.params.lines[5] | grid_moves(grid) for this grid is 11. | correct | l13/6 |
| l13-virtual-contest.json | screens[6].widget.how | Problem D, about 1500. Check runs 9 hidden tests: the example, a boxed-in start, ... | correct | l13/6 |
| l13-virtual-contest.json | screens[6].hints[0].text | Fewest moves with every move costing 1: which search? | correct | l13/6 |
| l13-virtual-contest.json | screens[6].hints[1].text | Breadth-first search from the top left, with a distance for each cell. | correct | l13/6 |
| l13-virtual-contest.json | screens[6].hints[2].text | Pop a cell; its moves are the arrow's one direction, or all four for `.`. Push ea... | correct | l13/6 |
| l13-virtual-contest.json | screens[6].feedback.correct | A BFS whose moves depend on the cell you leave. | correct | l13/6 |
| l13-virtual-contest.json | screens[6].feedback.generic | Not quite right. Look at the first failing test. | correct | l13/6 |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-1 | Test 1 expects 11. Ignoring the arrows gives 7, straight down and along the botto... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-2 | Test 2's start has an arrow on each side pointing away from the target. Both lead... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-3 | Test 3 is one cell: start and target coincide, so 0 moves. | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[6].feedback.byKey.test-9 | Test 9 is 200,000 cells. Visit each cell once with a queue; a search that revisit... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test (timing: the slow coding is stopped at 5 s; margin is orders of magnitude); the facts in the line recomputed in the script. |
| l13-virtual-contest.json | screens[6].explain.text | Each cell is visited once and has at most four moves, so the search is $O(rc)$. T... | correct | l13/6 |
| l13-virtual-contest.json | screens[7].prose | Sam sat the same round. Sam skipped the reading pass and opened D first, because ... | correct | l13/7 |
| l13-virtual-contest.json | screens[7].canvas.params.lines[0] | 00:00 opens D | correct | l13/7 |
| l13-virtual-contest.json | screens[7].canvas.params.lines[1] | 00:38 D Wrong answer on test 3 | correct | l13/7 |
| l13-virtual-contest.json | screens[7].canvas.params.lines[2] | 00:51 D Wrong answer on test 5 | correct | l13/7 |
| l13-virtual-contest.json | screens[7].canvas.params.lines[3] | 00:52 opens A | correct | l13/7 |
| l13-virtual-contest.json | screens[7].canvas.params.lines[4] | 00:59 A Accepted | correct | l13/7 |
| l13-virtual-contest.json | screens[7].canvas.params.lines[5] | 01:00 round over: 1 solved | correct | l13/7 |
| l13-virtual-contest.json | screens[7].widget.options[0].text | Read all four statements, then start with A | correct | l13/7 |
| l13-virtual-contest.json | screens[7].widget.options[1].text | Started with D: the hardest problem needs the most time | correct | l13/7 |
| l13-virtual-contest.json | screens[7].widget.options[1].why | You put the hardest first. Its time is the most uncertain, so it can eat the hour... | correct | l13/7 |
| l13-virtual-contest.json | screens[7].widget.options[2].text | Started with C: binary search is quick to code | correct | l13/7 |
| l13-virtual-contest.json | screens[7].widget.options[2].why | You skipped the reading pass too. C is quicker than D, but A and B are quicker st... | correct | l13/7 |
| l13-virtual-contest.json | screens[7].widget.options[3].text | Kept going on D after the first wrong answer | correct | l13/7 |
| l13-virtual-contest.json | screens[7].widget.options[3].why | You chose to stay. Sam did, and the second wrong answer cost 13 more minutes. | correct | l13/7 |
| l13-virtual-contest.json | screens[7].hints[0].text | Which problem took Sam seven minutes? | correct | l13/7 |
| l13-virtual-contest.json | screens[7].hints[1].text | A was accepted seven minutes after Sam opened it. | correct | l13/7 |
| l13-virtual-contest.json | screens[7].hints[2].text | Reading first shows A, B and C are quicker than D. Solving them first banks point... | correct | l13/7 |
| l13-virtual-contest.json | screens[7].feedback.correct | Read everything, then bank the quick problems. | correct | l13/7 |
| l13-virtual-contest.json | screens[7].feedback.generic | Not quite right. Compare what A cost Sam with what D cost. | correct | l13/7 |
| l13-virtual-contest.json | screens[7].feedback.byKey.hard | You started with the most interesting problem, as Sam did. D took 52 minutes and ... | correct | l13/7 |
| l13-virtual-contest.json | screens[7].explain.text | Sam's 52 minutes on D scored nothing, and A took seven. With A, B and C first, D ... | correct | l13/7 |
| l13-virtual-contest.json | screens[8].prose | After each problem, log its minutes for reading, coding and debugging, and its wr... | correct | l13/8 |
| l13-virtual-contest.json | screens[8].hints[0].text | Add each column down the four problems. | correct | l13/8 |
| l13-virtual-contest.json | screens[8].hints[1].text | Reading: $2 + 4 + 5 + 5$. | correct | l13/8 |
| l13-virtual-contest.json | screens[8].hints[2].text | Reading 16, coding 27, debugging 17. The three add up to the 60 minutes. | correct | l13/8 |
| l13-virtual-contest.json | screens[8].feedback.correct | 16, 27 and 17 minutes: 60 in all. | correct | l13/8 |
| l13-virtual-contest.json | screens[8].feedback.generic | Not quite right. Add each column again; the three should total 60. | correct | l13/8 |
| l13-virtual-contest.json | screens[8].explain.text | Debugging took 17 minutes, 12 of them on C alone. That entry is the one to act on... | correct | l13/8 |
| l13-virtual-contest.json | screens[9].prose | Here is what you did this hour, as a routine: ```text minutes 0-5 read every stat... | correct | l13/9 |
| l13-virtual-contest.json | screens[9].widget.options[0].text | To choose the order: the easiest may not be A | correct | l13/9 |
| l13-virtual-contest.json | screens[9].widget.options[1].text | To keep every statement in memory while coding | correct | l13/9 |
| l13-virtual-contest.json | screens[9].widget.options[1].why | You read to remember. The point is to choose an order and spot the quick wins. | correct | l13/9 |
| l13-virtual-contest.json | screens[9].widget.options[2].text | There is no reason: start A at once | correct | l13/9 |
| l13-virtual-contest.json | screens[9].widget.options[2].why | You skipped the reading pass. Sometimes C is easier than B, and only reading show... | correct | l13/9 |
| l13-virtual-contest.json | screens[9].feedback.correct | Reading first is how you choose the order. | correct | l13/9 |
| l13-virtual-contest.json | screens[9].feedback.generic | Not quite right. Ask what the reading pass decides. | correct | l13/9 |
| l13-virtual-contest.json | screens[9].explain.text | The letters only roughly follow difficulty. Five minutes of reading shows which p... | correct | l13/9 |
| l13-virtual-contest.json | screens[10].prose | A trading firm's online assessment gives you three problems in 75 minutes, graded... | correct | l13/10 |
| l13-virtual-contest.json | screens[10].canvas.params.lines[0] | Online assessment · 3 problems · 75 minutes | correct | l13/10 |
| l13-virtual-contest.json | screens[10].canvas.params.lines[1] | 1 Duplicate orders n ≤ 10⁵ looks quick | correct | l13/10 |
| l13-virtual-contest.json | screens[10].canvas.params.lines[2] | 2 Book imbalance n ≤ 2·10⁵ prefix sums | correct | l13/10 |
| l13-virtual-contest.json | screens[10].canvas.params.lines[3] | 3 Route latency n ≤ 10⁵, m ≤ 2·10⁵ Dijkstra | correct | l13/10 |
| l13-virtual-contest.json | screens[10].widget.options[0].text | 1, then 2, then 3, logging minutes; leave 3 if no idea in 15 minutes | correct | l13/10 |
| l13-virtual-contest.json | screens[10].widget.options[1].text | 3 first, since it carries the most marks | correct | l13/10 |
| l13-virtual-contest.json | screens[10].widget.options[1].why | You started with the hardest, as Sam did. Its time is the most uncertain. | correct | l13/10 |
| l13-virtual-contest.json | screens[10].widget.options[2].text | Write a little of each, then return to finish them | correct | l13/10 |
| l13-virtual-contest.json | screens[10].widget.options[2].why | You split the time evenly. Partial code passes no hidden tests, so finish one pro... | correct | l13/10 |
| l13-virtual-contest.json | screens[10].widget.options[3].text | Skip the reading: four minutes is a sixth of a problem's time | correct | l13/10 |
| l13-virtual-contest.json | screens[10].widget.options[3].why | You saved four minutes but lost the order. Reading is what showed problem 1 is qu... | correct | l13/10 |
| l13-virtual-contest.json | screens[10].hints[0].text | Which problem banks marks fastest? | correct | l13/10 |
| l13-virtual-contest.json | screens[10].hints[1].text | Problem 1 looks quick; problem 3 is the heaviest. | correct | l13/10 |
| l13-virtual-contest.json | screens[10].hints[2].text | Same routine as the round: read all, solve in order of ease, cap the time on a st... | correct | l13/10 |
| l13-virtual-contest.json | screens[10].feedback.correct | The same routine: easy first, a cap on the hard one. | correct | l13/10 |
| l13-virtual-contest.json | screens[10].feedback.generic | Not quite right. Apply the hour's routine to these three problems. | correct | l13/10 |
| l13-virtual-contest.json | screens[10].feedback.byKey.three | You started with the heaviest problem. An assessment scores solved problems, so b... | correct | l13/10 |
| l13-virtual-contest.json | screens[10].explain.text | An online assessment is a short contest: auto-graded, timed, and scored by what p... | correct | l13/10 |
| l13-virtual-contest.json | summary.ideas[0] | A virtual contest is a past round sat alone at full length: the weekly contest wh... | correct | l13/summary |
| l13-virtual-contest.json | summary.ideas[1] | Read every statement first, constraints first, and name each problem's pattern be... | correct | l13/summary |
| l13-virtual-contest.json | summary.ideas[2] | Log each problem's reading, coding and debugging minutes and its wrong submission... | correct | l13/summary |
| l13-virtual-contest.json | summary.formula.name | Problem C's search | correct | l13/summary |
| l13-virtual-contest.json | summary.formula.tex | \text{checks} \approx \log_2(\textstyle\sum w_i - \max w_i) | correct | l13/summary |
| l13-virtual-contest.json | summary.formula.note | Each check is one greedy pass, $O(n)$. | correct | l13/summary |
| l13-virtual-contest.json | summary.trap | Opening the most interesting problem first: its time is the most uncertain, and i... | correct | l13/summary |
| l13-virtual-contest.json | quiz[0].prose | Problem C has $n = 10^5$ orders, each at most $10^4$. The total is at most $10^9$. | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].widget.options[0].text | About 30, since $2^{30} > 10^9$ | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].widget.options[1].text | About $10^5$, one per order | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].widget.options[1].why | You counted orders. The search halves the range of capacities, not the orders. | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].widget.options[2].text | About $10^9$, one per capacity | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].widget.options[2].why | That is a scan through every capacity. Halving the range needs about 30 steps. | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].feedback.correct | About 30 checks, each $O(n)$. | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].feedback.generic | Not quite right. Count how many halvings shrink $10^9$ to 1. | correct | l13/q0 |
| l13-virtual-contest.json | quiz[0].explain.text | Each check halves the range of capacities, and $2^{30} \approx 1.07 \cdot 10^9$. ... | correct | l13/q0 |
| l13-virtual-contest.json | quiz[1].prose | Problem B's tape is AAA BBB AAA CCC BBB. Now every name is needed: AAA, BBB and CCC. | correct | l13/q1 |
| l13-virtual-contest.json | quiz[1].widget.accept | 3: AAA CCC BBB, trades 3 to 5 (or BBB AAA CCC, trades 2 to 4). | correct | l13/q1 |
| l13-virtual-contest.json | quiz[1].feedback.correct | 3 trades. | correct | l13/q1 |
| l13-virtual-contest.json | quiz[1].feedback.generic | Not quite right. Slide a window and find the shortest that holds all three names. | correct | l13/q1 |
| l13-virtual-contest.json | quiz[1].feedback.byKey.whole | The whole tape works, but trades 2 to 4 already hold all three. | correct | l13/q1 |
| l13-virtual-contest.json | quiz[1].feedback.byKey.two | Two trades can hold only two names. | correct | l13/q1 |
| l13-virtual-contest.json | quiz[1].explain.text | Trades 2 to 4 are BBB AAA CCC, and trades 3 to 5 are AAA CCC BBB. No run of 2 hol... | correct | l13/q1 |
| l13-virtual-contest.json | quiz[2].prose | Problem A, with closes 2 2 3 3 2. | correct | l13/q2 |
| l13-virtual-contest.json | quiz[2].widget.accept | 0: neither 3 is strictly above both neighbours. | correct | l13/q2 |
| l13-virtual-contest.json | quiz[2].feedback.correct | None: the plateau has no strict peak. | correct | l13/q2 |
| l13-virtual-contest.json | quiz[2].feedback.generic | Not quite right. Check *strictly* above both neighbours. | correct | l13/q2 |
| l13-virtual-contest.json | quiz[2].feedback.byKey.one | You counted a 3, but each 3 has a neighbour equal to it, not below. | correct | l13/q2 |
| l13-virtual-contest.json | quiz[2].feedback.byKey.two | You counted both 3s. Each is level with the other, so neither is strictly above b... | correct | l13/q2 |
| l13-virtual-contest.json | quiz[2].explain.text | Day 3 has neighbours 2 and 3, and day 4 has neighbours 3 and 2. Neither is strict... | correct | l13/q2 |
| l13-virtual-contest.json | quiz[3].prose | Problem D with the 2 by 2 city `.>` over `v.`: the start's right neighbour points... | correct | l13/q3 |
| l13-virtual-contest.json | quiz[3].widget.accept | −1: both moves lead to arrows that point out of the grid. | correct | l13/q3 |
| l13-virtual-contest.json | quiz[3].feedback.correct | −1: the target cannot be reached. | correct | l13/q3 |
| l13-virtual-contest.json | quiz[3].feedback.generic | Not quite right. Follow each arrow from the start's two neighbours. | correct | l13/q3 |
| l13-virtual-contest.json | quiz[3].feedback.byKey.two | You ignored the arrows. From `>` the only move is right, off the grid; from `v`, ... | correct | l13/q3 |
| l13-virtual-contest.json | quiz[3].feedback.byKey.one | One move reaches only a neighbour, not the opposite corner. | correct | l13/q3 |
| l13-virtual-contest.json | quiz[3].explain.text | The courier can enter either arrow cell, but each arrow points off the grid, so n... | correct | l13/q3 |
| l14-which-first.json | screens[0].prose | A two-hour round with decaying scores. Our rule: a problem loses $v / 250$ points... | correct | l14/0 |
| l14-which-first.json | screens[0].widget.lines[0].text | A: 500 points, about 10 minutes | correct | l14/0 |
| l14-which-first.json | screens[0].widget.lines[1].text | B: 1,000 points, about 20 minutes | correct | l14/0 |
| l14-which-first.json | screens[0].widget.lines[2].text | C: 1,500 points, about 35 minutes | correct | l14/0 |
| l14-which-first.json | screens[0].widget.lines[3].text | D: 2,000 points, about 50 minutes | correct | l14/0 |
| l14-which-first.json | screens[0].hints[0].text | Every minute a problem waits, it loses points. | correct | l14/0 |
| l14-which-first.json | screens[0].hints[1].text | Compare points per minute of work: A earns 500 in 10 minutes. | correct | l14/0 |
| l14-which-first.json | screens[0].hints[2].text | Points per minute: A 50, B 50, C about 43, D 40. Solve the best rate first; A and... | correct | l14/0 |
| l14-which-first.json | screens[0].feedback.correct | Quickest points first; A and B can go either way. | correct | l14/0 |
| l14-which-first.json | screens[0].feedback.generic | Not quite right. Work out points per minute of solving for each problem. | correct | l14/0 |
| l14-which-first.json | screens[0].explain.text | A and B pay 50 points per minute of work, C about 43 and D 40. Doing the best rat... | correct | l14/0 |
| l14-which-first.json | screens[1].prose | The bars show each problem's score under three orders. Solving times are 10, 20, ... | correct | l14/1 |
| l14-which-first.json | screens[1].widget.accept | 3,550, for A B C D. | correct | l14/1 |
| l14-which-first.json | screens[1].hints[0].text | Read the caption for each order. | correct | l14/1 |
| l14-which-first.json | screens[1].hints[1].text | The three totals are in the captions. | correct | l14/1 |
| l14-which-first.json | screens[1].hints[2].text | A B C D scores 3,550, D C B A 3,440 and C A B D 3,520. | correct | l14/1 |
| l14-which-first.json | screens[1].feedback.correct | 3,550, with the easiest first. | correct | l14/1 |
| l14-which-first.json | screens[1].feedback.generic | Not quite right. Compare the three captions. | correct | l14/1 |
| l14-which-first.json | screens[1].feedback.byKey.hard | 3,440 is the hardest-first order. D gains, but A, B and C lose more. | correct | l14/1 |
| l14-which-first.json | screens[1].feedback.byKey.cabd | 3,520 is C A B D. Putting C first makes A and B wait 35 minutes. | correct | l14/1 |
| l14-which-first.json | screens[1].explain.text | Hardest first lifts D from 1,080 to 1,600 but drops the other three by 630 togeth... | correct | l14/1 |
| l14-which-first.json | screens[2].prose | That order has a name: solve in order of **points per minute**, the value over th... | correct | l14/2 |
| l14-which-first.json | screens[2].hints[0].text | Divide the points by the minutes. | correct | l14/2 |
| l14-which-first.json | screens[2].hints[1].text | C: $1500 / 35$. | correct | l14/2 |
| l14-which-first.json | screens[2].hints[2].text | C: $1500 / 35 \approx 42.9$. D: $2000 / 50 = 40$. | correct | l14/2 |
| l14-which-first.json | screens[2].feedback.correct | C about 42.9 and D 40, so C before D. | correct | l14/2 |
| l14-which-first.json | screens[2].feedback.generic | Not quite right. Divide each problem's points by its minutes. | correct | l14/2 |
| l14-which-first.json | screens[2].explain.text | The rates fall from A to D here, so the letters happen to be the order. When they... | correct | l14/2 |
| l14-which-first.json | screens[3].prose | Our rule: a problem loses $v / 250$ points a minute until solved, 50 per rejected... | correct | l14/3 |
| l14-which-first.json | screens[3].widget.accept | 810: $1000 - 4 \cdot 35 - 50$. | correct | l14/3 |
| l14-which-first.json | screens[3].hints[0].text | Start from 1,000 and take off the minutes, then the attempt. | correct | l14/3 |
| l14-which-first.json | screens[3].hints[1].text | B loses $1000 / 250 = 4$ points a minute. | correct | l14/3 |
| l14-which-first.json | screens[3].hints[2].text | $1000 - 4 \cdot 35 - 50 = 810$, above the floor of 300. | correct | l14/3 |
| l14-which-first.json | screens[3].feedback.correct | 810 points. | correct | l14/3 |
| l14-which-first.json | screens[3].feedback.generic | Not quite right. Subtract 4 per minute and 50 per rejected attempt. | correct | l14/3 |
| l14-which-first.json | screens[3].feedback.byKey.nopen | You left out the rejected attempt, which costs 50. | correct | l14/3 |
| l14-which-first.json | screens[3].feedback.byKey.floor | The floor is 300, but 810 is above it, so it does not apply. | correct | l14/3 |
| l14-which-first.json | screens[3].feedback.byKey.twice | You charged the attempt twice. One rejection costs 50. | correct | l14/3 |
| l14-which-first.json | screens[3].explain.text | Thirty-five minutes cost 140 points and the rejection 50, so B scores 810. In a t... | correct | l14/3 |
| l14-which-first.json | screens[4].prose | Write `decayed_score(value, minute, wrong, per_minute, per_wrong, floor)`. It is ... | correct | l14/4 |
| l14-which-first.json | screens[4].widget.how | Check runs 8 hidden tests on the rule above. They include A late with three rejec... | correct | l14/4 |
| l14-which-first.json | screens[4].hints[0].text | Two candidates; return the larger. | correct | l14/4 |
| l14-which-first.json | screens[4].hints[1].text | One is `floor * value`. | correct | l14/4 |
| l14-which-first.json | screens[4].hints[2].text | `return max(floor * value, value - per_minute * minute - per_wrong * wrong)`. | correct | l14/4 |
| l14-which-first.json | screens[4].feedback.correct | The decayed value, floored at a fraction of the original. | correct | l14/4 |
| l14-which-first.json | screens[4].feedback.generic | Not quite right. Look at the first failing test. | correct | l14/4 |
| l14-which-first.json | screens[4].feedback.byKey.test-2 | Test 2 is A at minute 120 with three rejections: $500 - 240 - 150 = 110$, below t... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l14-which-first.json | screens[4].feedback.byKey.test-7 | Test 7 has a floor of 0 and a value that decays below 0. The floor still holds: t... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l14-which-first.json | screens[4].explain.text | Taking the larger of the two applies the floor after both costs. Test 5 sits exac... | correct | l14/4 |
| l14-which-first.json | screens[5].prose | An ICPC-style round ranks by problems solved, then by penalty, lower first. A sol... | correct | l14/5 |
| l14-which-first.json | screens[5].widget.how | Check runs 7 hidden tests: the table's results, no solves, an empty list and a so... | correct | l14/5 |
| l14-which-first.json | screens[5].hints[0].text | Rejections on an unsolved problem cost nothing. | correct | l14/5 |
| l14-which-first.json | screens[5].hints[1].text | D is unsolved, so its three rejections do not count. | correct | l14/5 |
| l14-which-first.json | screens[5].hints[2].text | Penalty $= 12 + (41 + 20) + (95 + 40) = 208$, so the key is `(-3, 208)`. | correct | l14/5 |
| l14-which-first.json | screens[5].feedback.correct | Solved count first, then penalty from solved problems only. | correct | l14/5 |
| l14-which-first.json | screens[5].feedback.generic | Not quite right. Look at the first failing test. | correct | l14/5 |
| l14-which-first.json | screens[5].feedback.byKey.test-1 | Test 1 expects `(-3, 208)`. D's three rejections do not count, because D was neve... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l14-which-first.json | screens[5].feedback.byKey.test-5 | Test 5 is a solve at minute 0 after five rejections. Test `minute is not None`: a... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l14-which-first.json | screens[5].explain.text | Negating the solved count lets one ascending sort put more solves first and less ... | correct | l14/5 |
| l14-which-first.json | screens[6].prose | Sixty minutes are left. D is worth 1,000 but slow to crack; E is worth 800 and qu... | correct | l14/6 |
| l14-which-first.json | screens[6].hints[0].text | Watch the caption as you drag. | correct | l14/6 |
| l14-which-first.json | screens[6].hints[1].text | The curve rises, then falls: staying on D too long costs E. | correct | l14/6 |
| l14-which-first.json | screens[6].hints[2].text | The top is near 35 minutes, at about 1,152 points. Then switch to E. | correct | l14/6 |
| l14-which-first.json | screens[6].feedback.correct | About 35 minutes on D, then switch to E. | correct | l14/6 |
| l14-which-first.json | screens[6].feedback.generic | Not quite right. Find the top of the curve. | correct | l14/6 |
| l14-which-first.json | screens[6].feedback.byKey.all | You gave D nearly the whole hour. All 60 minutes on D is about 699 points, and E'... | correct | l14/6 |
| l14-which-first.json | screens[6].feedback.byKey.none | You gave D almost no time. Skipping D altogether is about 785 points, and some ti... | correct | l14/6 |
| l14-which-first.json | screens[6].explain.text | The best fixed split is about 35 minutes on D, for about 1,152 points. All D give... | correct | l14/6 |
| l14-which-first.json | screens[7].prose | Eighty minutes into a two-hour round, you have spent 45 minutes on D. It has two ... | correct | l14/7 |
| l14-which-first.json | screens[7].canvas.params.lines[0] | 01:20 D 45 minutes, 2 rejected, no new idea | correct | l14/7 |
| l14-which-first.json | screens[7].canvas.params.lines[1] |  C unread, 1,500 points, about 30 minutes | correct | l14/7 |
| l14-which-first.json | screens[7].canvas.params.lines[2] |  40 minutes left in the round | correct | l14/7 |
| l14-which-first.json | screens[7].widget.options[0].text | Move to C now; return to D only with a new idea | correct | l14/7 |
| l14-which-first.json | screens[7].widget.options[1].text | Stay on D, or the 45 minutes are wasted | correct | l14/7 |
| l14-which-first.json | screens[7].widget.options[1].why | You counted the time already spent. It is gone either way; only the next 40 minut... | correct | l14/7 |
| l14-which-first.json | screens[7].widget.options[2].text | Resubmit D with a small change and hope | correct | l14/7 |
| l14-which-first.json | screens[7].widget.options[2].why | You resubmitted without a new idea. Each rejection costs 50 points and teaches no... | correct | l14/7 |
| l14-which-first.json | screens[7].widget.options[3].text | Stay on D: the floor guarantees 30% of 2,000 | correct | l14/7 |
| l14-which-first.json | screens[7].widget.options[3].why | The floor applies only once D is solved. Unsolved, D scores 0. | correct | l14/7 |
| l14-which-first.json | screens[7].hints[0].text | Which choice depends on the past rather than the next 40 minutes? | correct | l14/7 |
| l14-which-first.json | screens[7].hints[1].text | C needs about 30 minutes and has not lost its chance. | correct | l14/7 |
| l14-which-first.json | screens[7].hints[2].text | The 45 minutes are spent whatever you do. Compare what the next 40 minutes can st... | correct | l14/7 |
| l14-which-first.json | screens[7].feedback.correct | Move on: the spent time is gone either way. | correct | l14/7 |
| l14-which-first.json | screens[7].feedback.generic | Not quite right. Judge only the time that is left. | correct | l14/7 |
| l14-which-first.json | screens[7].feedback.byKey.stay | You stayed because of the time already spent. That is the sunk-cost mistake; the ... | correct | l14/7 |
| l14-which-first.json | screens[7].explain.text | Only future minutes can be allocated. C at about 30 minutes is the best use of 40... | correct | l14/7 |
| l14-which-first.json | screens[8].prose | You have solved A, B and C with 40 minutes left. The scoreboard shows how many co... | correct | l14/8 |
| l14-which-first.json | screens[8].canvas.params.lines[0] | Problem solved by | correct | l14/8 |
| l14-which-first.json | screens[8].canvas.params.lines[1] | A 4,210 | correct | l14/8 |
| l14-which-first.json | screens[8].canvas.params.lines[2] | B 3,105 | correct | l14/8 |
| l14-which-first.json | screens[8].canvas.params.lines[3] | C 1,388 | correct | l14/8 |
| l14-which-first.json | screens[8].canvas.params.lines[4] | D 96 | correct | l14/8 |
| l14-which-first.json | screens[8].canvas.params.lines[5] | E 702 | correct | l14/8 |
| l14-which-first.json | screens[8].hints[0].text | Is D easier than E because its letter is earlier? | correct | l14/8 |
| l14-which-first.json | screens[8].hints[1].text | Compare how many have solved D and E. | correct | l14/8 |
| l14-which-first.json | screens[8].hints[2].text | 702 solved E against 96 for D: E is very likely the easier problem. | correct | l14/8 |
| l14-which-first.json | screens[8].feedback.correct | E: seven times as many have solved it. | correct | l14/8 |
| l14-which-first.json | screens[8].feedback.generic | Not quite right. Trust the solve counts over the letters. | correct | l14/8 |
| l14-which-first.json | screens[8].feedback.byKey.l5 | You followed the letters. Only 96 have solved D, against 702 for E. | correct | l14/8 |
| l14-which-first.json | screens[8].explain.text | Letters are the setters' guess; the scoreboard is thousands of contestants' evide... | correct | l14/8 |
| l14-which-first.json | screens[9].prose | Take neighbouring problems $i$ and $j$. Doing $i$ first, $j$ waits $t_i$ minutes ... | correct | l14/9 |
| l14-which-first.json | screens[9].widget.accept | 20: $(2000 \cdot 35 - 1500 \cdot 50) / 250 = -20$, so C first loses 20 fewer. | correct | l14/9 |
| l14-which-first.json | screens[9].hints[0].text | Take $i = $ C and $j = $ D. | correct | l14/9 |
| l14-which-first.json | screens[9].hints[1].text | $v_D t_C - v_C t_D = 2000 \cdot 35 - 1500 \cdot 50$. | correct | l14/9 |
| l14-which-first.json | screens[9].hints[2].text | $70000 - 75000 = -5000$, and $-5000 / 250 = -20$: C first loses 20 points fewer. | correct | l14/9 |
| l14-which-first.json | screens[9].feedback.correct | 20 points: C then D scores more. | correct | l14/9 |
| l14-which-first.json | screens[9].feedback.generic | Not quite right. Put C's and D's values into the formula. | correct | l14/9 |
| l14-which-first.json | screens[9].feedback.byKey.neg | −20 is the change in points *lost*. Losing 20 fewer means scoring 20 more. | correct | l14/9 |
| l14-which-first.json | screens[9].feedback.byKey.big | You forgot to divide by 250, the rate rule's denominator. | correct | l14/9 |
| l14-which-first.json | screens[9].explain.text | A B C D scores 3,550 and A B D C scores 3,530: the swap costs 20. This is lesson ... | correct | l14/9 |
| l14-which-first.json | screens[10].prose | Write `best_order(problems, minutes)`. Each problem is `(name, value, time)`; sol... | correct | l14/10 |
| l14-which-first.json | screens[10].widget.how | Check runs 6 hidden tests: the round above at 120 and 60 minutes, and the problem... | correct | l14/10 |
| l14-which-first.json | screens[10].hints[0].text | Six problems give at most 720 orders: try them all. | correct | l14/10 |
| l14-which-first.json | screens[10].hints[1].text | Sort the problems by name first, so `permutations` gives orders alphabetically. | correct | l14/10 |
| l14-which-first.json | screens[10].hints[2].text | For each order, add each finish time and score it if it is within `minutes`. Keep... | correct | l14/10 |
| l14-which-first.json | screens[10].feedback.correct | Every order tried, ties broken alphabetically. | correct | l14/10 |
| l14-which-first.json | screens[10].feedback.generic | Not quite right. Look at the first failing test. | correct | l14/10 |
| l14-which-first.json | screens[10].feedback.byKey.test-2 | Test 2 has only 60 minutes. No three problems fit, and B then C is worth 2,090. | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l14-which-first.json | screens[10].feedback.byKey.test-3 | Test 3 lists the problems backwards. Sort by name before trying orders, so ties c... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l14-which-first.json | screens[10].feedback.byKey.test-4 | Test 4's only problem needs 10 minutes of a 5-minute round. It scores 0, and the ... | misleading | Finding 1. Facts true (10 > 5, score 0). But all three codings that fail first on test 4 already return a total of 0 and fail on the names: `(0, None)` or `(0, [])`. The coding that does score the late problem fails first on test 2. Script 'FINDING 1'. |
| l14-which-first.json | screens[10].explain.text | With 60 minutes the best order skips A: B then C scores 2,090, against 1,360 for ... | correct | l14/10 |
| l14-which-first.json | screens[11].prose | Half an hour before the close, three tasks wait on a trading desk. Each has an es... | correct | l14/11 |
| l14-which-first.json | screens[11].widget.options[0].text | Quote the client: £600 a minute | correct | l14/11 |
| l14-which-first.json | screens[11].widget.options[1].text | Hedge the position: the largest value | correct | l14/11 |
| l14-which-first.json | screens[11].widget.options[1].why | You chose the biggest value. At £480 a minute it is second; the quote earns £600 ... | correct | l14/11 |
| l14-which-first.json | screens[11].widget.options[2].text | Reconcile the break: clear the oldest problem first | correct | l14/11 |
| l14-which-first.json | screens[11].widget.options[2].why | You chose by age. At £100 a minute it comes last. | correct | l14/11 |
| l14-which-first.json | screens[11].hints[0].text | Divide value by minutes for each task. | correct | l14/11 |
| l14-which-first.json | screens[11].hints[1].text | Quote: $3000 / 5$. | correct | l14/11 |
| l14-which-first.json | screens[11].hints[2].text | Quote £600, hedge £480, reconcile £100 a minute: quote first, then the hedge. | correct | l14/11 |
| l14-which-first.json | screens[11].feedback.correct | Quote first, then the hedge; the break waits until after the close. | correct | l14/11 |
| l14-which-first.json | screens[11].feedback.generic | Not quite right. Compare value per minute. | correct | l14/11 |
| l14-which-first.json | screens[11].feedback.byKey.hedge | You chose by size. The quote takes 5 minutes and earns more per minute, then the ... | correct | l14/11 |
| l14-which-first.json | screens[11].explain.text | Both fit in the half hour, so only the waiting differs. At 1% a minute, quote fir... | correct | l14/11 |
| l14-which-first.json | summary.ideas[0] | Read every statement, then solve in order of points per minute: value over estima... | correct | l14/summary |
| l14-which-first.json | summary.ideas[1] | Cap the time on a stuck problem: the spent minutes are gone, and resubmitting wit... | correct | l14/summary |
| l14-which-first.json | summary.ideas[2] | The scoreboard beats the letters: many solves of a later problem mean it is easier. | correct | l14/summary |
| l14-which-first.json | summary.formula.name | Swapping two problems | correct | l14/summary |
| l14-which-first.json | summary.formula.tex | \Delta_{\text{lost}} = \dfrac{v_j t_i - v_i t_j}{250} | correct | l14/summary |
| l14-which-first.json | summary.formula.note | Under our rule; so $i$ first when $v_i / t_i > v_j / t_j$. | correct | l14/summary |
| l14-which-first.json | summary.trap | Staying on a problem because of the time already spent on it. | correct | l14/summary |
| l14-which-first.json | quiz[0].prose | Under our rule, a 1,000-point problem loses 4 points a minute and 50 per rejectio... | correct | l14/q0 |
| l14-which-first.json | quiz[0].widget.accept | 300: $1000 - 720 - 50 = 230$ is below the floor of 300. | correct | l14/q0 |
| l14-which-first.json | quiz[0].feedback.correct | 300, the floor. | correct | l14/q0 |
| l14-which-first.json | quiz[0].feedback.generic | Not quite right. Compute the decayed value, then compare it with the floor. | correct | l14/q0 |
| l14-which-first.json | quiz[0].feedback.byKey.nofloor | 230 is below the floor, and the score never falls below $0.3 \cdot 1000 = 300$. | correct | l14/q0 |
| l14-which-first.json | quiz[0].feedback.byKey.nopen | 280 leaves out the rejection, and it is below the floor anyway: the score is 300. | correct | l14/q0 |
| l14-which-first.json | quiz[0].explain.text | $1000 - 4 \cdot 180 - 50 = 230$, under $0.3 \cdot 1000 = 300$. So the floor appli... | correct | l14/q0 |
| l14-which-first.json | quiz[1].prose | ICPC style, 20 penalty minutes per rejection on a solved problem. X solved at 15,... | correct | l14/q1 |
| l14-which-first.json | quiz[1].widget.options[0].text | Z, then Y (penalty 185), then X (195) | correct | l14/q1 |
| l14-which-first.json | quiz[1].widget.options[1].text | Z, then X, then Y | correct | l14/q1 |
| l14-which-first.json | quiz[1].widget.options[1].why | You ranked X above Y. X's penalty is $155 + 40 = 195$ and Y's is $165 + 20 = 185$... | correct | l14/q1 |
| l14-which-first.json | quiz[1].widget.options[2].text | Y, X, then Z: Z's times are later | correct | l14/q1 |
| l14-which-first.json | quiz[1].widget.options[2].why | You ranked by penalty first. More solves always rank higher. | correct | l14/q1 |
| l14-which-first.json | quiz[1].feedback.correct | Solves first, then the lower penalty. | correct | l14/q1 |
| l14-which-first.json | quiz[1].feedback.generic | Not quite right. Count solves, then add the penalties. | correct | l14/q1 |
| l14-which-first.json | quiz[1].explain.text | Z's four solves beat any three. X: $15 + 50 + 90 + 2 \cdot 20 = 195$; Y: $20 + 45... | correct | l14/q1 |
| l14-which-first.json | quiz[2].prose | P is worth 750 and takes about 25 minutes. Q is worth 1,250 and takes about 50. | correct | l14/q2 |
| l14-which-first.json | quiz[2].widget.options[0].text | P: 30 points a minute against 25 | correct | l14/q2 |
| l14-which-first.json | quiz[2].widget.options[1].text | Q: it is worth more | correct | l14/q2 |
| l14-which-first.json | quiz[2].widget.options[1].why | You chose by value alone. Q earns 25 points a minute and P 30. | correct | l14/q2 |
| l14-which-first.json | quiz[2].widget.options[2].text | Either: the total is the same | correct | l14/q2 |
| l14-which-first.json | quiz[2].widget.options[2].why | The order changes how long each problem waits, so the totals differ. | correct | l14/q2 |
| l14-which-first.json | quiz[2].feedback.correct | P first: the better rate. | correct | l14/q2 |
| l14-which-first.json | quiz[2].feedback.generic | Not quite right. Compare points per minute. | correct | l14/q2 |
| l14-which-first.json | quiz[2].explain.text | $750 / 25 = 30$ and $1250 / 50 = 25$. So P goes first, which is also the order `b... | correct | l14/q2 |
| l14-which-first.json | quiz[3].prose | You have spent 30 minutes on a problem and have no new idea. Thirty minutes are l... | correct | l14/q3 |
| l14-which-first.json | quiz[3].widget.options[0].text | You have a new idea for the rejected case | correct | l14/q3 |
| l14-which-first.json | quiz[3].widget.options[1].text | You have already put 30 minutes in | correct | l14/q3 |
| l14-which-first.json | quiz[3].widget.options[1].why | You chose the time already spent. It is gone whatever you do next. | correct | l14/q3 |
| l14-which-first.json | quiz[3].widget.options[2].text | You feel close | correct | l14/q3 |
| l14-which-first.json | quiz[3].widget.options[2].why | A feeling without a new idea usually means another rejection. Read the unread pro... | correct | l14/q3 |
| l14-which-first.json | quiz[3].feedback.correct | Only a new idea justifies staying. | correct | l14/q3 |
| l14-which-first.json | quiz[3].feedback.generic | Not quite right. Ask which reason is about the next 30 minutes. | correct | l14/q3 |
| l14-which-first.json | quiz[3].explain.text | Staying is right only when the next minutes on this problem beat the alternatives... | correct | l14/q3 |
| l15-debugging-under-time.json | screens[0].prose | Your solution to problem L passed the example and failed test 4. This round's jud... | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[0] | L. Last fill: print the largest i (from 0) with | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[1] |  xs[i] = x, or -1 if x never appears. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[2] | Example: xs = 4 7 7 1, x = 7 → 2 | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[4] | def last_occurrence(xs, x): | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[5] |  for i in range(len(xs) - 2, -1, -1): | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[6] |  if xs[i] == x: | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[7] |  return i | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[8] |  return -1 | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].canvas.params.lines[10] | Verdict: Wrong answer on test 4 | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].hints[0].text | The statement asks for the largest index. Where does the search start? | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].hints[1].text | The last index of a list of length $n$ is $n - 1$. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].hints[2].text | `range(len(xs) - 2, -1, -1)` starts at $n - 2$, so it never looks at the last ele... | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].feedback.correct | Line 6 starts one place too early, at $n - 2$. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].feedback.generic | Not quite right. Check which indices the loop visits. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].feedback.byKey.l5 | That line only names the function. Look at which indices the loop visits. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].feedback.byKey.l7 | That comparison is what the statement asks: `xs[i] == x`. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].feedback.byKey.l9 | Returning −1 when nothing matches is right; the statement says so. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].feedback.byKey.l8 | Returning the first match from the right is right, if the loop starts at the end. | correct | l15/0 |
| l15-debugging-under-time.json | screens[0].explain.text | The loop starts at $n - 2$, so a match in the last place is missed. The example h... | correct | l15/0 |
| l15-debugging-under-time.json | screens[1].prose | Suppose you had not spotted line 6. The next step is hand-made edge cases: $n = 1... | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].canvas.params.lines[0] | case expected yours | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].canvas.params.lines[1] | n = 1: [5], x = 5 0 -1 differ | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].widget.accept | 2: the cases where x is the last element. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].hints[0].text | Slide to the fourth case. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].hints[1].text | Compare the expected column with yours on each row. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].hints[2].text | Rows 1 and 2 differ; rows 3 and 4 agree. Both failures have x in the last place. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].feedback.correct | Two, and both have the match at the end. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].feedback.generic | Not quite right. Count the rows marked *differ*. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].feedback.byKey.one | You stopped after the first case. Slide on: the all-equal case fails too. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].feedback.byKey.all | Cases 3 and 4 agree: there the last element is not the answer. | correct | l15/1 |
| l15-debugging-under-time.json | screens[1].explain.text | Each hand case takes seconds, and two of four caught the bug. What they share, x ... | correct | l15/1 |
| l15-debugging-under-time.json | screens[2].prose | What you just did is the start of a **debugging routine**: cheap checks first, th... | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].widget.lines[0].text | Reread the statement against the code | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].widget.lines[1].text | Run hand-made edge cases: $n = 1$, all equal, maximum, negative | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].widget.lines[2].text | Check overflow in C++ and recursion depth in Python | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].widget.lines[3].text | Stress test against a brute force on small random cases | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].hints[0].text | Which step costs the least? | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].hints[1].text | Rereading takes a minute; a stress test needs a brute force and a generator. | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].hints[2].text | Statement, hand cases, overflow and recursion, then stress test: the dearest step... | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].feedback.correct | Reread, hand cases, limits, then stress. | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].feedback.generic | Not quite right. The two steps you have just taken come first, and the stress tes... | correct | l15/2 |
| l15-debugging-under-time.json | screens[2].explain.text | Rereading takes a minute and a stress test needs a brute force and a generator, s... | correct | l15/2 |
| l15-debugging-under-time.json | screens[3].prose | Fix `last_occurrence(xs, x)`. The starter is the submission that failed test 4. C... | correct | l15/3 |
| l15-debugging-under-time.json | screens[3].widget.how | Check runs 7 hidden tests: the example, an absent value, an empty list, $n = 1$, ... | correct | l15/3 |
| l15-debugging-under-time.json | screens[3].hints[0].text | Which index should the loop visit first? | correct | l15/3 |
| l15-debugging-under-time.json | screens[3].hints[1].text | The last index is `len(xs) - 1`. | correct | l15/3 |
| l15-debugging-under-time.json | screens[3].hints[2].text | `for i in range(len(xs) - 1, -1, -1):` and nothing else changes. | correct | l15/3 |
| l15-debugging-under-time.json | screens[3].feedback.correct | One character: start at `len(xs) - 1`. | correct | l15/3 |
| l15-debugging-under-time.json | screens[3].feedback.generic | Not quite right. Look at the first failing test. | correct | l15/3 |
| l15-debugging-under-time.json | screens[3].feedback.byKey.test-4 | Test 4 is `[5]` with x = 5. The loop must visit index 0, the last index. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[3].feedback.byKey.test-3 | Test 3 is an empty list. `range(-1, -1, -1)` is empty, so −1 comes back without a... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[3].explain.text | The fix is one character, and the hand cases that failed now pass. Rewriting the ... | correct | l15/3 |
| l15-debugging-under-time.json | screens[4].prose | Problem M: count pairs $i < j$ with $x_i > x_j$, for $n \le 2000$. This submissio... | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].canvas.params.lines[0] | M. Inversions: count pairs i < j with xᵢ > xⱼ. | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].canvas.params.lines[1] |  n ≤ 2000, 1 ≤ xᵢ ≤ 10⁹. | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].canvas.params.lines[2] | Example: 3 1 2 → 2 | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].canvas.params.lines[3] | Verdict: Wrong answer on test 3 | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].widget.how | Check runs 7 hidden tests: the example, a falling list, an equal pair, one value,... | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].hints[0].text | What should `[2, 2]` give? | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].hints[1].text | Equal values are not an inversion: $2 > 2$ is false. | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].hints[2].text | Change `>=` to `>` in the comparison. | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].feedback.correct | Strictly greater: equal values are not inversions. | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].feedback.generic | Not quite right. Look at the first failing test. | correct | l15/4 |
| l15-debugging-under-time.json | screens[4].feedback.byKey.test-3 | Test 3 is `[2, 2]`, which has no inversion. `>=` counted the equal pair. | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[4].feedback.byKey.test-6 | Test 6, `[2, 1, 2, 1]`, has 3 inversions: the first 2 is larger than both 1s, and... | correct | Sweep under Pyodide 0.27.7 and CPython: 4 of 4 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[4].explain.text | The example has distinct values, so `>=` and `>` agree on it. The hand case with ... | correct | l15/4 |
| l15-debugging-under-time.json | screens[5].prose | Problem N has $t$ test cases. Each gives $n$ tickers, and the answer is the numbe... | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].canvas.params.lines[0] | N. Distinct tickers, t test cases | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].canvas.params.lines[1] | Input: t, then for each case n and n tickers. | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].canvas.params.lines[2] | Example input: 1 / 3 / AAA BBB AAA | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].canvas.params.lines[3] | Example output: 2 | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].canvas.params.lines[4] | Verdict: Wrong answer on test 2 | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].widget.how | Check runs 6 hidden tests: the example, two and three test cases, and blank lines... | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].hints[0].text | What happens to `seen` after the first test case? | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].hints[1].text | `seen` is created once, outside `solve_all`, and never emptied. | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].hints[2].text | Create `seen = set()` inside the loop over test cases, so each case starts empty. | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].feedback.correct | Fresh state for every test case. | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].feedback.generic | Not quite right. Look at the first failing test. | correct | l15/5 |
| l15-debugging-under-time.json | screens[5].feedback.byKey.test-2 | Test 2's second case is CCC CCC, one distinct ticker. Your answer counted AAA and... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[5].feedback.byKey.test-3 | Test 3's first case is AAA alone, so its answer is 1. A set kept outside `solve_a... | imprecise | Finding 2. True only for a set cleared between cases but not before the first (2 contrived codings, `[2, 1, 2]`). Three of five codings that keep the set outside fail first on test 2. The coding that counts only new tickers per case fails first here with its first case right, `[1, 0, 1]`, and no outside set. Script 'FINDING 2' and 'line l15 screens[5] test-3'. |
| l15-debugging-under-time.json | screens[5].explain.text | A bug that shows only with several test cases hides from every $t = 1$ example. R... | correct | l15/5 |
| l15-debugging-under-time.json | screens[6].prose | You fixed the bug but left two debug prints inside the loop. Your own two-case fi... | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].canvas.params.lines[0] | $ python3 sol.py < two_cases.txt | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].canvas.params.lines[1] | debug: case 1, seen = {'AAA', 'BBB'} | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].canvas.params.lines[2] | 2 | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].canvas.params.lines[3] | debug: case 2, seen = {'CCC'} | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].canvas.params.lines[4] | 1 | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].canvas.params.lines[6] | Verdict: Wrong answer on test 1 | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].widget.options[0].text | Print debug lines to standard error: `print(..., file=sys.stderr)` | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].widget.options[1].text | Delete the solution and rewrite it from scratch | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].widget.options[1].why | You chose to start again in a panic. The bug is small; rewriting brings new ones ... | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].widget.options[2].text | Keep one debug print, not two | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].widget.options[2].why | One extra line still makes the output differ from the answer on every test. | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].widget.options[3].text | Move the prints after the answers | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].widget.options[3].why | The checker reads all of standard output. Extra lines anywhere make it wrong. | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].hints[0].text | What does the judge compare? | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].hints[1].text | It compares everything your program writes to standard output. | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].hints[2].text | Write debug lines to `sys.stderr`, which the judge does not compare, or delete th... | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].feedback.correct | Debug to standard error; the judge reads only standard output. | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].feedback.generic | Not quite right. Ask what the checker reads. | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].feedback.byKey.rewrite | You chose to rewrite everything. A fix of one line is faster and safer than a new... | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].feedback.byKey.fewer | You kept a print in standard output. Any extra line there turns every test into a... | correct | l15/6 |
| l15-debugging-under-time.json | screens[6].explain.text | The judge compares all of standard output, so a debug line beside the answer brea... | correct | l15/6 |
| l15-debugging-under-time.json | screens[7].prose | Problem P is a DFS over 100,000 desks joined in a line. Your recursive DFS passed... | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].canvas.params.lines[0] | def dfs(u): | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].canvas.params.lines[1] |  seen[u] = True | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].canvas.params.lines[2] |  for v in adj[u]: | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].canvas.params.lines[3] |  if not seen[v]: | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].canvas.params.lines[4] |  dfs(v) | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].canvas.params.lines[6] | RecursionError: maximum recursion depth exceeded | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].canvas.params.lines[7] | Verdict: Runtime error on test 9 | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].widget.options[0].text | Rewrite the DFS with an explicit stack, as in `graphs-dp` | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].widget.options[1].text | Only call `sys.setrecursionlimit(10**6)` | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].widget.options[1].why | You raised the limit. It works in this app's Pyodide, which ran a million frames ... | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].widget.options[2].text | Recurse on every second node to halve the depth | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].widget.options[2].why | You halved the depth. A line of 100,000 still needs 50,000 frames. | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].widget.options[3].text | Hope the hidden tests are smaller | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].widget.options[3].why | Test 9 is already a line of 100,000. | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].hints[0].text | What grows with the length of the line? | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].hints[1].text | Each `dfs` call waits for the next one: 100,000 frames deep. | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].hints[2].text | An explicit stack keeps the pending nodes in a list, so depth costs memory, not f... | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].feedback.correct | An explicit stack never hits a depth limit. | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].feedback.generic | Not quite right. Choose the fix that removes deep recursion. | correct | l15/7 |
| l15-debugging-under-time.json | screens[7].explain.text | A list used as a stack holds the nodes still to visit, so depth is just list leng... | correct | l15/7 |
| l15-debugging-under-time.json | screens[8].prose | The routine, with the one helper it needs: ```python import sys def debug(*args):... | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].widget.options[0].text | Trace that small case by hand through the code | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].widget.options[1].text | Write a stress test anyway | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].widget.options[1].why | You skipped ahead. A failing hand case is already the small input a stress test w... | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].widget.options[2].text | Resubmit to see whether it was a fluke | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].widget.options[2].why | The same code gives the same answer, and a rejection costs penalty. | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].feedback.correct | Trace the failing case: it is already small. | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].feedback.generic | Not quite right. Use the failing case you have. | correct | l15/8 |
| l15-debugging-under-time.json | screens[8].explain.text | A failing case of three values can be traced in a minute, and the bug shows itsel... | correct | l15/8 |
| l15-debugging-under-time.json | screens[9].prose | Write `smallest_failing(fast, brute, gen, seed)`. Here `gen(rng, n)` makes a case... | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].canvas.params.lines[0] | stress(fast, brute, gen, trials, seed) lesson 4 | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].canvas.params.lines[1] | gen_list(rng, n) n values from 1 to 3 | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].canvas.params.lines[2] | gen_wide(rng, n) n values from 1 to 10⁶ | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].canvas.params.lines[3] | brute_inv(xs) inversions, every pair | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].canvas.params.lines[4] | fast_ties, fast_no_last, fast_adjacent buggy | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].canvas.params.lines[5] | fast_merge merge sort, correct | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].widget.how | Check runs 7 hidden tests with the functions listed above. Each expects the case ... | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].hints[0].text | Grow the length instead of shrinking a case. | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].hints[1].text | The generator for length $n$ is `lambda rng: gen(rng, n)`. | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].hints[2].text | `for n in range(1, 9):` call `stress(fast, brute, lambda rng: gen(rng, n), 200, s... | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].feedback.correct | The first failure at the smallest length, found by growing $n$. | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].feedback.generic | Not quite right. Look at the first failing test. | correct | l15/9 |
| l15-debugging-under-time.json | screens[9].feedback.byKey.test-3 | Test 3's bug needs three values. Keep growing the length past 2: try every length... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[9].feedback.byKey.test-6 | Test 6 uses values up to $10^6$, which almost never tie, so the tie bug stays hid... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[9].feedback.byKey.test-7 | Test 7 fails only from length 5. Run up to length 8 before giving up. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l15-debugging-under-time.json | screens[9].explain.text | Trying lengths 1, 2, 3 and so on returns the shortest failing case the trials fin... | correct | l15/9 |
| l15-debugging-under-time.json | screens[10].prose | At 08:05 the position report of a trading system shows twice the overnight fills ... | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].canvas.params.lines[0] | 08:05 report: book EQ-7 position 2,400 (fills say 1,200) | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].canvas.params.lines[1] | 07:58 service restarted after a deploy | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].canvas.params.lines[2] | 07:59 fills replayed from 18:00 yesterday | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].widget.options[0].text | Reproduce it with the smallest input: one fill, then a restart | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].widget.options[1].text | Rewrite the position service before the open | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].widget.options[1].why | You chose a rewrite under time, the panic move. It risks new bugs in code that mo... | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].widget.options[2].text | Add print statements to the live service | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].widget.options[2].why | You debugged in production, as with stdout prints. Reproduce it offline first. | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].widget.options[3].text | Replay the whole night's fills to see it again | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].widget.options[3].why | That is the large failing case. One fill and a restart is the small one you can t... | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].hints[0].text | What did the restart do to the fills? | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].hints[1].text | The log replays fills after the restart. | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].hints[2].text | Try one fill, a restart and a replay. If the position doubles, the replay is not ... | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].feedback.correct | Smallest reproduction first: one fill and a restart. | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].feedback.generic | Not quite right. Apply the contest routine: reproduce small, then fix. | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].feedback.byKey.rewrite | You chose to rewrite everything under time pressure. A small reproduction locates... | correct | l15/10 |
| l15-debugging-under-time.json | screens[10].explain.text | One fill and a restart is the $n = 1$ hand case of this incident. If the position... | correct | l15/10 |
| l15-debugging-under-time.json | summary.ideas[0] | After a wrong answer, reread the statement against the code: it is the cheapest c... | correct | l15/summary |
| l15-debugging-under-time.json | summary.ideas[1] | Then run hand-made edge cases ($n = 1$, all equal, maximum, negative), check over... | correct | l15/summary |
| l15-debugging-under-time.json | summary.ideas[2] | Debug prints go to standard error and per-case state is reset. A one-line fix bea... | correct | l15/summary |
| l15-debugging-under-time.json | summary.formula.name | The routine | correct | l15/summary |
| l15-debugging-under-time.json | summary.formula.tex | \text{reread} \to \text{hand cases} \to \text{limits} \to \text{stress test} | correct | l15/summary |
| l15-debugging-under-time.json | summary.formula.note | Cheapest check first. | correct | l15/summary |
| l15-debugging-under-time.json | summary.trap | Adding debug prints to standard output: every test then fails, including the ones... | correct | l15/summary |
| l15-debugging-under-time.json | quiz[0].prose | In C++, you sum $n = 2 \cdot 10^5$ values, each up to $10^9$, into an `int`. | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].widget.options[0].text | It overflows: the sum can reach $2 \cdot 10^{14}$ | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].widget.options[1].text | Nothing: an `int` holds any sum of `int`s | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].widget.options[1].why | You assumed the sum stays in range. A 32-bit `int` stops at 2,147,483,647. | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].widget.options[2].text | It is too slow | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].widget.options[2].why | Adding $2 \cdot 10^5$ numbers takes microseconds. The problem is the type. | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].feedback.correct | Overflow: use `long long`. | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].feedback.generic | Not quite right. Compare the largest sum with an `int`'s limit. | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[0].explain.text | $2 \cdot 10^5 \cdot 10^9 = 2 \cdot 10^{14}$, while an `int` holds at most $2^{31}... | correct | l15/q0 |
| l15-debugging-under-time.json | quiz[1].prose | A problem asks for days whose close is strictly greater than the day before. Your... | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].widget.options[0].text | Two equal closes: 5 5 | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].widget.options[1].text | One close: 5 | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].widget.options[1].why | With one close there is no day before, so both versions give 0. | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].widget.options[2].text | Rising closes: 1 2 3 | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].widget.options[2].why | On distinct values `>=` and `>` agree. | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].feedback.correct | Equal values are where `>=` and `>` differ. | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].feedback.generic | Not quite right. Find the case where the two comparisons disagree. | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[1].explain.text | On 5 5, `>=` counts day 2 and `>` does not. That is why the all-equal case is on ... | correct | l15/q1 |
| l15-debugging-under-time.json | quiz[2].prose | A solution keeps a global list `seen` and never clears it. Each input has $t$ tes... | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].widget.options[0].text | From the second test case on | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].widget.options[1].text | On every test | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].widget.options[1].why | With $t = 1$ the list starts empty, so the first case is right. | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].widget.options[2].text | Only on large inputs | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].widget.options[2].why | Size does not matter. The second test case inherits the first one's state. | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].feedback.correct | From the second case on, which a $t = 1$ example never shows. | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].feedback.generic | Not quite right. Think about what the first case leaves behind. | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[2].explain.text | The first case runs on a fresh list and is right. Every later case starts with le... | correct | l15/q2 |
| l15-debugging-under-time.json | quiz[3].prose | A buggy count of inversions compares only neighbouring values. The case is `[3, 2... | correct | l15/q3 |
| l15-debugging-under-time.json | quiz[3].widget.accept | 2: it counts (3, 2) and (2, 1) and misses (3, 1). | correct | l15/q3 |
| l15-debugging-under-time.json | quiz[3].feedback.correct | 2, against the correct 3. | correct | l15/q3 |
| l15-debugging-under-time.json | quiz[3].feedback.generic | Not quite right. Count only neighbouring pairs. | correct | l15/q3 |
| l15-debugging-under-time.json | quiz[3].feedback.byKey.right | 3 is the correct count. The buggy one never compares 3 with 1, which are not neig... | correct | l15/q3 |
| l15-debugging-under-time.json | quiz[3].feedback.byKey.zero | Both neighbouring pairs, 3 then 2 and 2 then 1, are inversions. | correct | l15/q3 |
| l15-debugging-under-time.json | quiz[3].explain.text | The neighbouring pairs are (3, 2) and (2, 1); the pair (3, 1) is missed. That is ... | correct | l15/q3 |
| l16-upsolving.json | screens[0].prose | Last week you sat a five-problem virtual round, a different one from lesson 13's.... | correct | l16/0 |
| l16-upsolving.json | screens[0].canvas.params.lines[0] | A Accepted 00:09 | correct | l16/0 |
| l16-upsolving.json | screens[0].canvas.params.lines[1] | B Accepted 00:24 | correct | l16/0 |
| l16-upsolving.json | screens[0].canvas.params.lines[2] | C Accepted 00:51 | correct | l16/0 |
| l16-upsolving.json | screens[0].canvas.params.lines[3] | D Time limit exceeded on test 9 | correct | l16/0 |
| l16-upsolving.json | screens[0].canvas.params.lines[4] | E not opened | correct | l16/0 |
| l16-upsolving.json | screens[0].widget.options[0].text | Solve D and E properly, then sit the next round | correct | l16/0 |
| l16-upsolving.json | screens[0].widget.options[1].text | Sit a new virtual round straight away | correct | l16/0 |
| l16-upsolving.json | screens[0].widget.options[1].why | You chose another round. D and E show exactly what you cannot do yet, and a new r... | correct | l16/0 |
| l16-upsolving.json | screens[0].widget.options[2].text | Read D's and E's editorials and mark them solved | correct | l16/0 |
| l16-upsolving.json | screens[0].widget.options[2].why | You read without writing. Until your own code is accepted, the idea is not yours. | correct | l16/0 |
| l16-upsolving.json | screens[0].widget.options[3].text | Solve ten easier problems for practice | correct | l16/0 |
| l16-upsolving.json | screens[0].widget.options[3].why | You chose comfort. Problems you can already solve add little; D is just beyond you. | correct | l16/0 |
| l16-upsolving.json | screens[0].hints[0].text | Which problems show what you cannot do yet? | correct | l16/0 |
| l16-upsolving.json | screens[0].hints[1].text | D failed and E was never read. | correct | l16/0 |
| l16-upsolving.json | screens[0].hints[2].text | Solving them after the round, with help if needed, works on exactly what you coul... | correct | l16/0 |
| l16-upsolving.json | screens[0].feedback.correct | Solve the problems that beat you first. | correct | l16/0 |
| l16-upsolving.json | screens[0].feedback.generic | Not quite right. Ask which hour teaches you something new. | correct | l16/0 |
| l16-upsolving.json | screens[0].explain.text | The problems you could not solve are the edge of your ability, chosen for you by ... | correct | l16/0 |
| l16-upsolving.json | screens[1].prose | After this round, the judge shows you the failing test and the editorial is out. ... | correct | l16/1 |
| l16-upsolving.json | screens[1].canvas.params.lines[0] | P = prefix sums of a, P[0] = 0 | correct | l16/1 |
| l16-upsolving.json | screens[1].canvas.params.lines[1] | for i in 1 .. n-2: | correct | l16/1 |
| l16-upsolving.json | screens[1].canvas.params.lines[2] |  for j in i+1 .. n-1: | correct | l16/1 |
| l16-upsolving.json | screens[1].canvas.params.lines[3] |  if P[i] == P[j] - P[i] == P[n] - P[j]: | correct | l16/1 |
| l16-upsolving.json | screens[1].canvas.params.lines[4] |  ways += 1 | correct | l16/1 |
| l16-upsolving.json | screens[1].canvas.params.lines[6] | Verdict: Time limit exceeded on test 9 | correct | l16/1 |
| l16-upsolving.json | screens[1].widget.accept | 6: choose 2 of the 4 gaps between the five days. | correct | l16/1 |
| l16-upsolving.json | screens[1].hints[0].text | With all zeros, every cut works. | correct | l16/1 |
| l16-upsolving.json | screens[1].hints[1].text | Five days have 4 gaps, and you choose 2 of them. | correct | l16/1 |
| l16-upsolving.json | screens[1].hints[2].text | $\binom{4}{2} = 6$. For 200,000 zeros it is $\binom{199999}{2} = 19{,}999{,}700{,... | correct | l16/1 |
| l16-upsolving.json | screens[1].feedback.correct | 6 ways: any 2 of the 4 gaps. | correct | l16/1 |
| l16-upsolving.json | screens[1].feedback.generic | Not quite right. Count pairs of gaps between the days. | correct | l16/1 |
| l16-upsolving.json | screens[1].feedback.byKey.ten | 10 is $\binom{5}{2}$, choosing 2 of the 5 days. Cuts go in the 4 gaps between them. | correct | l16/1 |
| l16-upsolving.json | screens[1].feedback.byKey.three | 3 is for four zeros. Five zeros have 4 gaps, so $\binom{4}{2} = 6$. | correct | l16/1 |
| l16-upsolving.json | screens[1].feedback.byKey.one | With zeros every cut makes three equal totals of 0, so every pair of gaps works. | correct | l16/1 |
| l16-upsolving.json | screens[1].explain.text | With all zeros every pair of cuts is valid: 6 pairs for five zeros, and about $2 ... | correct | l16/1 |
| l16-upsolving.json | screens[2].prose | Solving the problems you could not solve in time, after the round, is **upsolving... | correct | l16/2 |
| l16-upsolving.json | screens[2].canvas.params.lines[0] | Editorial, idea only: | correct | l16/2 |
| l16-upsolving.json | screens[2].canvas.params.lines[1] | Let S be the total. If 3 does not divide S, print 0. | correct | l16/2 |
| l16-upsolving.json | screens[2].canvas.params.lines[2] | Cuts i < j work when P[i] = S/3 and P[j] = 2S/3. | correct | l16/2 |
| l16-upsolving.json | screens[2].canvas.params.lines[3] | Scan j from left to right. Keep a count of earlier | correct | l16/2 |
| l16-upsolving.json | screens[2].canvas.params.lines[4] | i with P[i] = S/3, and add it at each good j. | correct | l16/2 |
| l16-upsolving.json | screens[2].widget.lines[0].text | Read the editorial's idea, then close it | correct | l16/2 |
| l16-upsolving.json | screens[2].widget.lines[1].text | Write your own code from a blank file | correct | l16/2 |
| l16-upsolving.json | screens[2].widget.lines[2].text | Submit until it is accepted | correct | l16/2 |
| l16-upsolving.json | screens[2].widget.lines[3].text | Write it up and add the mistake to your log | correct | l16/2 |
| l16-upsolving.json | screens[2].widget.lines[4].text | Redo it a week later without notes | correct | l16/2 |
| l16-upsolving.json | screens[2].hints[0].text | The code must be yours, so when do you close the editorial? | correct | l16/2 |
| l16-upsolving.json | screens[2].hints[1].text | Before writing any code. | correct | l16/2 |
| l16-upsolving.json | screens[2].hints[2].text | Idea, close it, your own code, accepted, write-up and log, then a redo a week later. | correct | l16/2 |
| l16-upsolving.json | screens[2].feedback.correct | Idea, own code, accepted, written up, redone. | correct | l16/2 |
| l16-upsolving.json | screens[2].feedback.generic | Not quite right. The editorial gives the idea; everything after is yours. | correct | l16/2 |
| l16-upsolving.json | screens[2].explain.text | Closing the editorial makes you rebuild the idea, which is what sticks. The redo ... | correct | l16/2 |
| l16-upsolving.json | screens[3].prose | Problem D, about 1600 by our estimate. Write `equal_thirds(xs)` from the editoria... | correct | l16/3 |
| l16-upsolving.json | screens[3].canvas.params.lines[0] | D. Three equal periods (1 s, 256 MB) | correct | l16/3 |
| l16-upsolving.json | screens[3].canvas.params.lines[1] | A fund's P&L over n days, a₁ … aₙ, is to be cut | correct | l16/3 |
| l16-upsolving.json | screens[3].canvas.params.lines[2] | into three non-empty runs of consecutive days | correct | l16/3 |
| l16-upsolving.json | screens[3].canvas.params.lines[3] | with equal totals. Count the ways to cut it. | correct | l16/3 |
| l16-upsolving.json | screens[3].canvas.params.lines[4] | Input: n (1 ≤ n ≤ 2·10⁵), a₁ … aₙ (/aᵢ/ ≤ 10⁹). | correct | l16/3 |
| l16-upsolving.json | screens[3].canvas.params.lines[5] | Output: the number of ways. | correct | l16/3 |
| l16-upsolving.json | screens[3].canvas.params.lines[6] | Example: 1 2 3 0 3 → 2 | correct | l16/3 |
| l16-upsolving.json | screens[3].widget.how | Problem D, about 1600. Check runs 9 hidden tests: the example, five zeros, $n = 2... | correct | l16/3 |
| l16-upsolving.json | screens[3].hints[0].text | Count, do not list: the answer can be about $2 \cdot 10^{10}$. | correct | l16/3 |
| l16-upsolving.json | screens[3].hints[1].text | Scan the second cut $j$; keep how many first cuts $i < j$ had $P_i = S/3$. | correct | l16/3 |
| l16-upsolving.json | screens[3].hints[2].text | Running prefix over `range(len(xs) - 1)`: if it equals $2S/3$ add the count; then... | correct | l16/3 |
| l16-upsolving.json | screens[3].feedback.correct | One pass, counting first cuts as you go. | correct | l16/3 |
| l16-upsolving.json | screens[3].feedback.generic | Not quite right. Look at the first failing test. | correct | l16/3 |
| l16-upsolving.json | screens[3].feedback.byKey.test-2 | Test 2 is five zeros: 6 ways. With $S = 0$, both $S/3$ and $2S/3$ are 0, so count... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[3].feedback.byKey.test-5 | Test 5's total is 2, which 3 does not divide. Return 0 at once. | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[3].feedback.byKey.test-6 | Test 6 has negative values and a total of 0, so the prefix sum rises and falls. D... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[3].feedback.byKey.test-8 | Test 8 is 200,000 zeros: 19,999,700,001 ways. A double loop over cuts is about $2... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test (timing: the slow coding is stopped at 5 s; margin is orders of magnitude); the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[3].explain.text | Each second cut adds the number of good first cuts before it, so the pairs are co... | correct | l16/3 |
| l16-upsolving.json | screens[4].prose | Every upsolved problem adds a line to a **mistakes log**: the problem, what went ... | correct | l16/4 |
| l16-upsolving.json | screens[4].hints[0].text | Go down the log once, keeping a tally. | correct | l16/4 |
| l16-upsolving.json | screens[4].hints[1].text | Rows 2, 4 and 8 are *forgot n = 1*. | correct | l16/4 |
| l16-upsolving.json | screens[4].hints[2].text | Forgot $n = 1$: 3. Misread a constraint: 2. Greedy without proof: 2. Overflow: 1. | correct | l16/4 |
| l16-upsolving.json | screens[4].feedback.correct | 3, 2, 2 and 1: eight mistakes in all. | correct | l16/4 |
| l16-upsolving.json | screens[4].feedback.generic | Not quite right. Tally the categories again; they should total 8. | correct | l16/4 |
| l16-upsolving.json | screens[4].explain.text | The top line is the rule to act on: test $n = 1$ by hand before every submission.... | correct | l16/4 |
| l16-upsolving.json | screens[5].prose | Write `mistakes_summary(log)`, where `log` is a list of `(problem, category)` pai... | correct | l16/5 |
| l16-upsolving.json | screens[5].widget.how | Check runs 8 hidden tests: the log above, an empty log, one entry, a tie between ... | correct | l16/5 |
| l16-upsolving.json | screens[5].hints[0].text | Count first, then sort. | correct | l16/5 |
| l16-upsolving.json | screens[5].hints[1].text | A dictionary of counts, then `sorted` with a key. | correct | l16/5 |
| l16-upsolving.json | screens[5].hints[2].text | Sort the `(category, count)` items with `key=lambda kv: (-kv[1], kv[0])`. | correct | l16/5 |
| l16-upsolving.json | screens[5].feedback.correct | Counted, then sorted by count and name. | correct | l16/5 |
| l16-upsolving.json | screens[5].feedback.generic | Not quite right. Look at the first failing test. | correct | l16/5 |
| l16-upsolving.json | screens[5].feedback.byKey.test-2 | Test 2 is an empty log. Return an empty list. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[5].feedback.byKey.test-6 | Test 6 has *Overflow* with a capital. Python sorts capitals before lower case; le... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[5].feedback.byKey.test-7 | Test 7 has *overflow* twice and *misread* once. Sort by count first, then by name. | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[5].feedback.byKey.test-1 | Test 1 ties *greedy without proof* and *misread a constraint* at 2. Sort by count... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| l16-upsolving.json | screens[5].explain.text | The key `(-count, name)` sorts by count downwards, then by name upwards, in one c... | correct | l16/5 |
| l16-upsolving.json | screens[6].prose | Your rating is 1,200. These are the problems you did not solve in your last round... | correct | l16/6 |
| l16-upsolving.json | screens[6].canvas.params.lines[0] | Unsolved after round 45 | correct | l16/6 |
| l16-upsolving.json | screens[6].canvas.params.lines[1] | C rating 1400 | correct | l16/6 |
| l16-upsolving.json | screens[6].canvas.params.lines[2] | D rating 1500 | correct | l16/6 |
| l16-upsolving.json | screens[6].canvas.params.lines[3] | E rating 1900 | correct | l16/6 |
| l16-upsolving.json | screens[6].canvas.params.lines[4] | F rating 2400 | correct | l16/6 |
| l16-upsolving.json | screens[6].hints[0].text | Add 300 to your rating. | correct | l16/6 |
| l16-upsolving.json | screens[6].hints[1].text | $1200 + 300 = 1500$. | correct | l16/6 |
| l16-upsolving.json | screens[6].hints[2].text | C at 1400 and D at 1500 are within 300. E and F are 700 and 1,200 above. | correct | l16/6 |
| l16-upsolving.json | screens[6].feedback.correct | C and D: both within about 300 of your rating. | correct | l16/6 |
| l16-upsolving.json | screens[6].feedback.generic | Not quite right. Keep problems rated up to about 1,500. | correct | l16/6 |
| l16-upsolving.json | screens[6].feedback.byKey.l4 | You chose E, 700 above your rating. Its editorial may rest on ideas you have not ... | correct | l16/6 |
| l16-upsolving.json | screens[6].feedback.byKey.l5 | You chose F, 1,200 above. That is too far for now. | correct | l16/6 |
| l16-upsolving.json | screens[6].explain.text | This lesson assumes a problem up to 300 above you needs one new idea. One far abo... | correct | l16/6 |
| l16-upsolving.json | screens[7].prose | The curriculum asks for one contest a week, once 100 problems are behind you. You... | correct | l16/7 |
| l16-upsolving.json | screens[7].canvas.params.lines[0] | Mon one virtual round, 2 hours, time log kept | correct | l16/7 |
| l16-upsolving.json | screens[7].canvas.params.lines[1] | Tue upsolve to one problem beyond what you solved | correct | l16/7 |
| l16-upsolving.json | screens[7].canvas.params.lines[2] | Wed five Codeforces problems rated 1350 to 1450 | correct | l16/7 |
| l16-upsolving.json | screens[7].canvas.params.lines[3] | Thu write-ups and the mistakes log | correct | l16/7 |
| l16-upsolving.json | screens[7].canvas.params.lines[4] | Sat one Project Euler-style problem | correct | l16/7 |
| l16-upsolving.json | screens[7].widget.options[0].text | Plan A, as shown | correct | l16/7 |
| l16-upsolving.json | screens[7].widget.options[1].text | Five virtual rounds and no upsolving | correct | l16/7 |
| l16-upsolving.json | screens[7].widget.options[1].why | You chose volume. Without upsolving, nothing closes the gaps each round shows, so... | correct | l16/7 |
| l16-upsolving.json | screens[7].widget.options[2].text | Thirty problems rated 800 | correct | l16/7 |
| l16-upsolving.json | screens[7].widget.options[2].why | You chose problems far below your level. They add speed but no new ideas. | correct | l16/7 |
| l16-upsolving.json | screens[7].widget.options[3].text | Five problems rated 2000 | correct | l16/7 |
| l16-upsolving.json | screens[7].widget.options[3].why | You chose problems 750 above you. This lesson's rule of thumb is to practise abou... | correct | l16/7 |
| l16-upsolving.json | screens[7].hints[0].text | How far above 1,250 should practice problems be? | correct | l16/7 |
| l16-upsolving.json | screens[7].hints[1].text | This lesson's rule of thumb is about 100 to 200 above: 1,350 to 1,450. | correct | l16/7 |
| l16-upsolving.json | screens[7].hints[2].text | Plan A has one round, its upsolving, five problems in range, write-ups and one ma... | correct | l16/7 |
| l16-upsolving.json | screens[7].feedback.correct | Plan A: a round, its upsolving, and practice just above your level. | correct | l16/7 |
| l16-upsolving.json | screens[7].feedback.generic | Not quite right. Look for practice about 100 to 200 above 1,250. | correct | l16/7 |
| l16-upsolving.json | screens[7].explain.text | A round shows the gaps, upsolving closes them, and five problems just above your ... | correct | l16/7 |
| l16-upsolving.json | screens[8].prose | Jo upsolves by reading each editorial and nodding along. Jo's log reads *solved* ... | correct | l16/8 |
| l16-upsolving.json | screens[8].canvas.params.lines[0] | D, round 41 read editorial solved | correct | l16/8 |
| l16-upsolving.json | screens[8].canvas.params.lines[1] | E, round 41 read editorial solved | correct | l16/8 |
| l16-upsolving.json | screens[8].canvas.params.lines[2] | D, round 42 read editorial solved | correct | l16/8 |
| l16-upsolving.json | screens[8].canvas.params.lines[3] | ... (nine more) | correct | l16/8 |
| l16-upsolving.json | screens[8].widget.options[0].text | None of it was written and accepted, so the ideas are not Jo's | correct | l16/8 |
| l16-upsolving.json | screens[8].widget.options[1].text | Nothing: twelve editorials a month is plenty | correct | l16/8 |
| l16-upsolving.json | screens[8].widget.options[1].why | You counted editorials read as problems solved. Understanding an idea is not the ... | correct | l16/8 |
| l16-upsolving.json | screens[8].widget.options[2].text | Jo should sit more contests instead | correct | l16/8 |
| l16-upsolving.json | screens[8].widget.options[2].why | You chose more rounds. More rounds without upsolving can leave the same gaps open. | correct | l16/8 |
| l16-upsolving.json | screens[8].widget.options[3].text | Jo should read harder editorials | correct | l16/8 |
| l16-upsolving.json | screens[8].widget.options[3].why | Harder editorials read the same way teach no more. | correct | l16/8 |
| l16-upsolving.json | screens[8].hints[0].text | When is a problem upsolved? | correct | l16/8 |
| l16-upsolving.json | screens[8].hints[1].text | When your own code for it is accepted. | correct | l16/8 |
| l16-upsolving.json | screens[8].hints[2].text | Reading feels like learning. Writing the code, getting it accepted and redoing it... | correct | l16/8 |
| l16-upsolving.json | screens[8].feedback.correct | Read is not solved: the code must be written and accepted. | correct | l16/8 |
| l16-upsolving.json | screens[8].feedback.generic | Not quite right. Ask what Jo never did. | correct | l16/8 |
| l16-upsolving.json | screens[8].feedback.byKey.more | You treated reading an editorial as solving the problem. Jo never wrote or submit... | correct | l16/8 |
| l16-upsolving.json | screens[8].explain.text | An editorial read in five minutes feels clear, but the details are where the bugs... | correct | l16/8 |
| l16-upsolving.json | screens[9].prose | The loop this level built: ```text round one virtual or live contest, timed upsol... | correct | l16/9 |
| l16-upsolving.json | screens[9].widget.options[0].text | When your own code for it is accepted | correct | l16/9 |
| l16-upsolving.json | screens[9].widget.options[1].text | When you have understood the editorial | correct | l16/9 |
| l16-upsolving.json | screens[9].widget.options[1].why | You chose understanding. The code, written and accepted, is the test of it. | correct | l16/9 |
| l16-upsolving.json | screens[9].widget.options[2].text | When an accepted solution is in your folder | correct | l16/9 |
| l16-upsolving.json | screens[9].widget.options[2].why | Someone else's accepted code teaches you their idea, not your implementation. | correct | l16/9 |
| l16-upsolving.json | screens[9].feedback.correct | Your code, accepted. | correct | l16/9 |
| l16-upsolving.json | screens[9].feedback.generic | Not quite right. Ask what proves you can do it under time. | correct | l16/9 |
| l16-upsolving.json | screens[9].explain.text | The loop turns one round into a week of learning. The redo a week later shows whe... | correct | l16/9 |
| l16-upsolving.json | screens[10].prose | The curriculum sets a rating of 1,400 as a fair first-year target. It treats rati... | correct | l16/10 |
| l16-upsolving.json | screens[10].widget.options[0].text | A developer application | correct | l16/10 |
| l16-upsolving.json | screens[10].widget.options[1].text | A trader application | correct | l16/10 |
| l16-upsolving.json | screens[10].widget.options[1].why | You chose trading. In the table, trader interviews test probability, mental arith... | correct | l16/10 |
| l16-upsolving.json | screens[10].widget.options[2].text | A researcher application | correct | l16/10 |
| l16-upsolving.json | screens[10].widget.options[2].why | You chose research. In the table, those interviews test statistics, machine learn... | correct | l16/10 |
| l16-upsolving.json | screens[10].hints[0].text | Which interviews test algorithms directly? | correct | l16/10 |
| l16-upsolving.json | screens[10].hints[1].text | Look at the first row. | correct | l16/10 |
| l16-upsolving.json | screens[10].hints[2].text | In the table, developer interviews test algorithms and C++, which a rating eviden... | correct | l16/10 |
| l16-upsolving.json | screens[10].feedback.correct | Developer roles, where interviews test algorithms. | correct | l16/10 |
| l16-upsolving.json | screens[10].feedback.generic | Not quite right. Match the rating to the interviews that test algorithms. | correct | l16/10 |
| l16-upsolving.json | screens[10].explain.text | A rating is evidence of algorithmic skill, which the table's developer interviews... | correct | l16/10 |
| l16-upsolving.json | screens[11].prose | You are on the researcher track. Your CV says *Codeforces 1,410; 80 problem write... | correct | l16/11 |
| l16-upsolving.json | screens[11].widget.options[0].text | A Kaggle competition, written up | correct | l16/11 |
| l16-upsolving.json | screens[11].widget.options[1].text | Push the rating from 1,410 to 1,800 | correct | l16/11 |
| l16-upsolving.json | screens[11].widget.options[1].why | You chose the rating. It counts for little in researcher interviews. | correct | l16/11 |
| l16-upsolving.json | screens[11].widget.options[2].text | IMC Prosperity | correct | l16/11 |
| l16-upsolving.json | screens[11].widget.options[2].why | That is the trader track's addition. Researchers add Kaggle. | correct | l16/11 |
| l16-upsolving.json | screens[11].widget.options[3].text | Delete the write-ups: nobody reads them | correct | l16/11 |
| l16-upsolving.json | screens[11].widget.options[3].why | You chose to delete evidence. Write-ups show how you think, and an interviewer ma... | correct | l16/11 |
| l16-upsolving.json | screens[11].hints[0].text | What do researcher interviews test? | correct | l16/11 |
| l16-upsolving.json | screens[11].hints[1].text | Statistics, machine learning and a data take-home. | correct | l16/11 |
| l16-upsolving.json | screens[11].hints[2].text | A Kaggle competition is that work in public; write it up as you write up problems. | correct | l16/11 |
| l16-upsolving.json | screens[11].feedback.correct | Kaggle, for the researcher track. | correct | l16/11 |
| l16-upsolving.json | screens[11].feedback.generic | Not quite right. Match the addition to your track. | correct | l16/11 |
| l16-upsolving.json | screens[11].feedback.byKey.rating | You chose more rating. For a researcher, a Kaggle result says more than another 3... | correct | l16/11 |
| l16-upsolving.json | screens[11].explain.text | The rating and the write-ups stay on the CV as evidence of solid coding. For rese... | correct | l16/11 |
| l16-upsolving.json | summary.ideas[0] | Upsolve after every round: take the editorial's idea, close it, and get your own ... | correct | l16/summary |
| l16-upsolving.json | summary.ideas[1] | Keep a mistakes log of problem, category and rule; redo each upsolved problem a w... | correct | l16/summary |
| l16-upsolving.json | summary.ideas[2] | The curriculum's first-year target is a rating of 1,400; it counts a rating towar... | correct | l16/summary |
| l16-upsolving.json | summary.formula.name | Problem D's count | correct | l16/summary |
| l16-upsolving.json | summary.formula.tex | \text{ways} = \sum_{j \le n-1:\, P_j = 2S/3} \#\{\, 1 \le i < j : P_i = S/3 \,\} | correct | l16/summary |
| l16-upsolving.json | summary.formula.note | One pass, counting first cuts as you go. | correct | l16/summary |
| l16-upsolving.json | summary.trap | Reading the editorial and calling the problem solved without writing the code. | correct | l16/summary |
| l16-upsolving.json | quiz[0].prose | Problem D with four days, all zeros. | correct | l16/q0 |
| l16-upsolving.json | quiz[0].widget.accept | 3: choose 2 of the 3 gaps. | correct | l16/q0 |
| l16-upsolving.json | quiz[0].feedback.correct | 3 ways. | correct | l16/q0 |
| l16-upsolving.json | quiz[0].feedback.generic | Not quite right. Count pairs among the 3 gaps between four days. | correct | l16/q0 |
| l16-upsolving.json | quiz[0].feedback.byKey.six | 6 is for five zeros. Four days have 3 gaps, and $\binom{3}{2} = 3$. | correct | l16/q0 |
| l16-upsolving.json | quiz[0].feedback.byKey.four | 4 is $\binom{4}{1}$. Each cut pair uses 2 of the 3 gaps. | correct | l16/q0 |
| l16-upsolving.json | quiz[0].explain.text | Four days have 3 gaps, and any 2 of them work when every value is 0. So the answe... | correct | l16/q0 |
| l16-upsolving.json | quiz[1].prose | Your rating is 1,500. You did not solve problems rated 1700 and 2100 in your last... | correct | l16/q1 |
| l16-upsolving.json | quiz[1].widget.options[0].text | The 1700, and note the 2100 for later | correct | l16/q1 |
| l16-upsolving.json | quiz[1].widget.options[1].text | Both: every unsolved problem must be upsolved | correct | l16/q1 |
| l16-upsolving.json | quiz[1].widget.options[1].why | You chose both. The 2100 is 600 above you; its editorial assumes ideas you have n... | correct | l16/q1 |
| l16-upsolving.json | quiz[1].widget.options[2].text | The 2100: it teaches the most | correct | l16/q1 |
| l16-upsolving.json | quiz[1].widget.options[2].why | Far above your level, an editorial teaches several ideas at once and few stick. | correct | l16/q1 |
| l16-upsolving.json | quiz[1].feedback.correct | The 1700, within about 300 of your rating. | correct | l16/q1 |
| l16-upsolving.json | quiz[1].feedback.generic | Not quite right. Upsolve up to about 300 above your rating. | correct | l16/q1 |
| l16-upsolving.json | quiz[1].explain.text | $1500 + 300 = 1800$, so the 1700 is in range and the 2100 is not yet. Note it in ... | correct | l16/q1 |
| l16-upsolving.json | quiz[2].prose | A log has *misread* twice, *edge case* twice and *overflow* once. | correct | l16/q2 |
| l16-upsolving.json | quiz[2].widget.options[0].text | `[('edge case', 2), ('misread', 2), ('overflow', 1)]` | correct | l16/q2 |
| l16-upsolving.json | quiz[2].widget.options[1].text | `[('misread', 2), ('edge case', 2), ('overflow', 1)]` | correct | l16/q2 |
| l16-upsolving.json | quiz[2].widget.options[1].why | You kept the order of first appearance. Ties are broken alphabetically. | correct | l16/q2 |
| l16-upsolving.json | quiz[2].widget.options[2].text | `[('overflow', 1), ('edge case', 2), ('misread', 2)]` | correct | l16/q2 |
| l16-upsolving.json | quiz[2].widget.options[2].why | You sorted by count upwards. The most frequent mistake comes first. | correct | l16/q2 |
| l16-upsolving.json | quiz[2].feedback.correct | By count, most first, then alphabetically. | correct | l16/q2 |
| l16-upsolving.json | quiz[2].feedback.generic | Not quite right. Sort by count down, then name up. | correct | l16/q2 |
| l16-upsolving.json | quiz[2].explain.text | The key `(-count, name)` puts the two 2s first, *edge case* before *misread*, the... | correct | l16/q2 |
| l16-upsolving.json | quiz[3].prose | A friend on the trader track has a Codeforces rating of 1,600 and is preparing fo... | correct | l16/q3 |
| l16-upsolving.json | quiz[3].widget.options[0].text | Probability, mental arithmetic and market-making games | correct | l16/q3 |
| l16-upsolving.json | quiz[3].widget.options[1].text | Contest algorithms, as the rating shows | correct | l16/q3 |
| l16-upsolving.json | quiz[3].widget.options[1].why | You matched the rating to the interview. The table's trader row lists other skills. | correct | l16/q3 |
| l16-upsolving.json | quiz[3].widget.options[2].text | Machine learning and a data take-home | correct | l16/q3 |
| l16-upsolving.json | quiz[3].widget.options[2].why | That is the researcher track's interview. | correct | l16/q3 |
| l16-upsolving.json | quiz[3].feedback.correct | Probability, mental arithmetic and market-making games. | correct | l16/q3 |
| l16-upsolving.json | quiz[3].feedback.generic | Not quite right. Recall what trader interviews test. | correct | l16/q3 |
| l16-upsolving.json | quiz[3].explain.text | This lesson's table lists probability, mental arithmetic and market-making games ... | correct | l16/q3 |
| review-4.json | items[0].prose | A statement in a virtual round: a fund must pay $n$ redemptions in order over $k$... | correct | review-4/0 |
| review-4.json | items[0].widget.options[0].text | Binary search on the limit, with a greedy check of each guess | correct | review-4/0 |
| review-4.json | items[0].widget.options[1].text | A sliding window over the redemptions | correct | review-4/0 |
| review-4.json | items[0].widget.options[1].why | You matched *in order* to a window. The question asks for the smallest value that... | correct | review-4/0 |
| review-4.json | items[0].widget.options[2].text | Breadth-first search | correct | review-4/0 |
| review-4.json | items[0].widget.options[2].why | BFS finds fewest moves in a graph. There is no graph here. | correct | review-4/0 |
| review-4.json | items[0].widget.options[3].text | Try every limit from the largest redemption upwards | correct | review-4/0 |
| review-4.json | items[0].widget.options[3].why | That is correct but slow: up to about $2 \cdot 10^{14}$ limits, each checked in $... | correct | review-4/0 |
| review-4.json | items[0].feedback.correct | Binary search on the answer: problem C in disguise. | correct | review-4/0 |
| review-4.json | items[0].feedback.generic | Not quite right. Look for *the smallest value that works*. | correct | review-4/0 |
| review-4.json | items[0].explain.text | A larger limit always works if a smaller one does, so *works* is monotone in the ... | correct | review-4/0 |
| review-4.json | items[1].prose | Your time log for a 60-minute round reads: reading 12 minutes, coding 30, debuggi... | correct | review-4/1 |
| review-4.json | items[1].widget.accept | 30%: $18 / 60$. | correct | review-4/1 |
| review-4.json | items[1].feedback.correct | 30%. | correct | review-4/1 |
| review-4.json | items[1].feedback.generic | Not quite right. Divide the debugging minutes by the whole round. | correct | review-4/1 |
| review-4.json | items[1].feedback.byKey.code | 50% is the coding share, $30 / 60$. | correct | review-4/1 |
| review-4.json | items[1].feedback.byKey.of-code | 60% is debugging over coding, $18 / 30$. Divide by the whole hour. | correct | review-4/1 |
| review-4.json | items[1].explain.text | $18 / 60 = 0.3$, so 30% of the hour went on debugging. That share is the first th... | correct | review-4/1 |
| review-4.json | items[2].prose | Under the course's rule, a problem worth 1,500 loses 6 points a minute and 50 per... | correct | review-4/2 |
| review-4.json | items[2].widget.accept | 1,112: $1500 - 6 \cdot 48 - 2 \cdot 50$. | correct | review-4/2 |
| review-4.json | items[2].feedback.correct | 1,112 points. | correct | review-4/2 |
| review-4.json | items[2].feedback.generic | Not quite right. Subtract the minutes, then both rejections. | correct | review-4/2 |
| review-4.json | items[2].feedback.byKey.nopen | You left out both rejections, which cost 100. | correct | review-4/2 |
| review-4.json | items[2].feedback.byKey.onepen | You charged one rejection. There were two. | correct | review-4/2 |
| review-4.json | items[2].explain.text | $6 \cdot 48 = 288$ and $2 \cdot 50 = 100$, so $1500 - 388 = 1112$. That is well a... | correct | review-4/2 |
| review-4.json | items[3].prose | Same rule: each problem loses its value over 250 per minute until solved. P, wort... | correct | review-4/3 |
| review-4.json | items[3].widget.accept | 20: $(1000 \cdot 15 - 500 \cdot 40) / 250 = -20$ for Q first, so Q first loses 20... | correct | review-4/3 |
| review-4.json | items[3].feedback.correct | 20 points, so Q first. | correct | review-4/3 |
| review-4.json | items[3].feedback.generic | Not quite right. Use the swap formula from lesson 14. | correct | review-4/3 |
| review-4.json | items[3].feedback.byKey.neg | −20 is the change in points lost. Losing 20 fewer means scoring 20 more. | correct | review-4/3 |
| review-4.json | items[3].feedback.byKey.nodiv | Divide by 250, the rule's rate. | correct | review-4/3 |
| review-4.json | items[3].explain.text | Q earns about 33 points a minute and P 25. Q first: P waits 15 minutes and loses ... | correct | review-4/3 |
| review-4.json | items[4].prose | A solution sums a list with `for i in range(1, len(xs)): total += xs[i]`, startin... | correct | review-4/4 |
| review-4.json | items[4].widget.options[0].text | $n = 1$: `[5]`, expected 5 | correct | review-4/4 |
| review-4.json | items[4].widget.options[1].text | All equal: `[2, 2, 2]`, expected 6 | correct | review-4/4 |
| review-4.json | items[4].widget.options[1].why | That fails too, giving 4, but the single value shows the missing first element at... | correct | review-4/4 |
| review-4.json | items[4].widget.options[2].text | 200,000 random values | correct | review-4/4 |
| review-4.json | items[4].widget.options[2].why | A large case fails without showing why. Hand cases are small on purpose. | correct | review-4/4 |
| review-4.json | items[4].widget.options[3].text | An empty list, expected 0 | correct | review-4/4 |
| review-4.json | items[4].widget.options[3].why | The buggy loop also gives 0 there, so the bug stays hidden. | correct | review-4/4 |
| review-4.json | items[4].feedback.correct | `[5]` returns 0: the first element is never added. | correct | review-4/4 |
| review-4.json | items[4].feedback.generic | Not quite right. Find the smallest case whose answer depends on the first element. | correct | review-4/4 |
| review-4.json | items[4].explain.text | The loop starts at index 1, so `xs[0]` is never added. On `[5]` it returns 0 inst... | correct | review-4/4 |
| review-4.json | items[5].prose | In C++, problem D of lesson 16 counts the ways to cut 200,000 zeros into three eq... | correct | review-4/5 |
| review-4.json | items[5].widget.options[0].text | `long long`: the count is above $2^{31} - 1$ | correct | review-4/5 |
| review-4.json | items[5].widget.options[1].text | `int`: it is only a count of ways | correct | review-4/5 |
| review-4.json | items[5].widget.options[1].why | You assumed counts are small. 19,999,700,001 is far above an `int`'s 2,147,483,647. | correct | review-4/5 |
| review-4.json | items[5].widget.options[2].text | `double`: it is a very large number | correct | review-4/5 |
| review-4.json | items[5].widget.options[2].why | A `double` holds it exactly here, but integer counts belong in `long long`, which... | correct | review-4/5 |
| review-4.json | items[5].feedback.correct | `long long`. | correct | review-4/5 |
| review-4.json | items[5].feedback.generic | Not quite right. Compare the count with an `int`'s limit. | correct | review-4/5 |
| review-4.json | items[5].explain.text | $\binom{199999}{2} = 19{,}999{,}700{,}001$, about nine times $2^{31} - 1$. Checki... | correct | review-4/5 |
| review-4.json | items[6].prose | Your rating is 1,350. Your last round left problems rated 1500, 1600, 1900 and 23... | correct | review-4/6 |
| review-4.json | items[6].widget.options[0].text | 1500 | correct | review-4/6 |
| review-4.json | items[6].widget.options[1].text | 1600 | correct | review-4/6 |
| review-4.json | items[6].widget.options[2].text | 1900 | correct | review-4/6 |
| review-4.json | items[6].widget.options[2].why | 1900 is 550 above you. Note it and come back later. | correct | review-4/6 |
| review-4.json | items[6].widget.options[3].text | 2300 | correct | review-4/6 |
| review-4.json | items[6].widget.options[3].why | 2300 is 950 above you, too far for now. | correct | review-4/6 |
| review-4.json | items[6].feedback.correct | 1500 and 1600, within about 300 of 1,350. | correct | review-4/6 |
| review-4.json | items[6].feedback.generic | Not quite right. Keep problems up to about 1,650. | correct | review-4/6 |
| review-4.json | items[6].explain.text | $1350 + 300 = 1650$, so 1500 and 1600 are in range. The others go in the log for ... | correct | review-4/6 |
| review-4.json | items[7].prose | Minute 95 of a two-hour round. The scoreboard shows E solved by many more than D.... | correct | review-4/7 |
| review-4.json | items[7].widget.accept | 675: solved at minute 115, $1250 - 5 \cdot 115$. | correct | review-4/7 |
| review-4.json | items[7].feedback.correct | 675 points. | correct | review-4/7 |
| review-4.json | items[7].feedback.generic | Not quite right. The score decays from the start of the round, not from minute 95. | correct | review-4/7 |
| review-4.json | items[7].feedback.byKey.twenty | You decayed it for 20 minutes only. The score falls from minute 0, so use the sol... | correct | review-4/7 |
| review-4.json | items[7].feedback.byKey.floor | 375 is the floor, but $1250 - 575 = 675$ is above it. | correct | review-4/7 |
| review-4.json | items[7].explain.text | E is solved at minute $95 + 20 = 115$, so it loses $5 \cdot 115 = 575$ points. Th... | correct | review-4/7 |
| homework-4.json | items[0].prose | **Cut link** (about 1300 by our estimate). A firm has $n$ trading desks, numbered... | correct | homework-4/0 |
| homework-4.json | items[0].canvas.params.lines[0] | Example 1: n = 4, links (0,1) (1,2) (2,3) (3,0) | correct | homework-4/0 |
| homework-4.json | items[0].canvas.params.lines[1] |  cut = 0 → 1 (still joined: 0-3-2-1) | correct | homework-4/0 |
| homework-4.json | items[0].canvas.params.lines[2] | Example 2: n = 4, links (0,1) (1,2), cut = 1 | correct | homework-4/0 |
| homework-4.json | items[0].canvas.params.lines[3] |  → 3 ({0, 1}, {2} and {3}) | correct | homework-4/0 |
| homework-4.json | items[0].widget.how | Check runs 8 hidden tests: the examples, a self-link, a repeated link, isolated d... | correct | homework-4/0 |
| homework-4.json | items[0].feedback.correct | Build the graph without the cut link, then count BFS starts. | correct | homework-4/0 |
| homework-4.json | items[0].feedback.generic | Not quite right. Look at the first failing test. | correct | homework-4/0 |
| homework-4.json | items[0].feedback.byKey.test-4 | Test 4 repeats a link. Cutting one copy leaves the other, so desks 0 and 1 stay t... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[0].feedback.byKey.test-7 | Test 7 is a chain of 200,000 desks. Use a queue or an explicit stack, not deep re... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[0].feedback.byKey.test-2 | Test 2 cuts link (1, 2), which leaves desks 2 and 3 with no link. Each isolated d... | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[0].explain.text | Skip link `cut` while building the adjacency lists, then start a BFS from each un... | correct | homework-4/0 |
| homework-4.json | items[1].prose | **At most k trades** (about 1500 by our estimate). Given daily prices, buy and se... | correct | homework-4/1 |
| homework-4.json | items[1].canvas.params.lines[0] | Example: prices 3 2 6 5 0 3, k = 2 → 7 | correct | homework-4/1 |
| homework-4.json | items[1].canvas.params.lines[1] |  buy at 2, sell at 6; buy at 0, sell at 3 | correct | homework-4/1 |
| homework-4.json | items[1].widget.how | Check runs 8 hidden tests: the example with $k$ = 2, 1 and 0, falling prices and ... | correct | homework-4/1 |
| homework-4.json | items[1].feedback.correct | A DP over trades: best cash holding and not holding after $j$ purchases. | correct | homework-4/1 |
| homework-4.json | items[1].feedback.generic | Not quite right. Look at the first failing test. | correct | homework-4/1 |
| homework-4.json | items[1].feedback.byKey.test-3 | Test 3 allows no trades, so the profit is 0. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[1].feedback.byKey.test-4 | Test 4's prices only fall. The best is not to trade: 0. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[1].feedback.byKey.test-6 | Test 6 allows 10 trades but only three rises help: $2 + 3 + 4 = 9$. | correct | Sweep under Pyodide 0.27.7 and CPython: 3 of 3 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[1].feedback.byKey.test-8 | Test 8 is 10,000 prices with $k = 20$. Trying every pair of days for each trade i... | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test (timing: the slow coding is stopped at 5 s; margin is orders of magnitude); the facts in the line recomputed in the script. |
| homework-4.json | items[1].explain.text | Keep `buy[j]`, the best cash after the $j$-th purchase, and `sell[j]`, after the ... | correct | homework-4/1 |
| homework-4.json | items[2].prose | **Spread the bots** (about 1600 by our estimate). You have price levels $x_1, \do... | correct | homework-4/2 |
| homework-4.json | items[2].canvas.params.lines[0] | Example: levels 1 2 8 4 9, m = 3 → 3 | correct | homework-4/2 |
| homework-4.json | items[2].canvas.params.lines[1] |  bots at 1, 4 and 8 (or 1, 4 and 9) | correct | homework-4/2 |
| homework-4.json | items[2].widget.how | Check runs 8 hidden tests: the example with $m$ = 3, 2 and 5, equal levels and tw... | correct | homework-4/2 |
| homework-4.json | items[2].feedback.correct | Sort, then binary search the distance with a greedy check. | correct | homework-4/2 |
| homework-4.json | items[2].feedback.generic | Not quite right. Look at the first failing test. | correct | homework-4/2 |
| homework-4.json | items[2].feedback.byKey.test-4 | Test 4 has three equal levels and two bots, so the best distance is 0. | correct | Sweep under Pyodide 0.27.7 and CPython: 1 of 1 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[2].feedback.byKey.test-8 | Test 8 has 200,000 levels. Try each distance by binary search, about 30 greedy ch... | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test (timing: the slow coding is stopped at 5 s; margin is orders of magnitude); the facts in the line recomputed in the script. |
| homework-4.json | items[2].feedback.byKey.test-1 | Test 1's levels, 1 2 8 4 9, are not sorted. Sort them before the greedy check. | correct | Sweep under Pyodide 0.27.7 and CPython: 2 of 2 failing codings of the named mistake fail first on this test; the facts in the line recomputed in the script. |
| homework-4.json | items[2].explain.text | If distance $d$ can be kept, so can every smaller one, so binary search $d$. To c... | correct | homework-4/2 |
| homework-4.json | items[3].prose | The first ten minutes of a contest decide its order. | correct | homework-4/3 |
| homework-4.json | items[3].widget.lines[0].text | Start the timer and open every statement | correct | homework-4/3 |
| homework-4.json | items[3].widget.lines[1].text | Read each problem's constraints and output first | correct | homework-4/3 |
| homework-4.json | items[3].widget.lines[2].text | Name each problem's pattern and allowed complexity | correct | homework-4/3 |
| homework-4.json | items[3].widget.lines[3].text | Rank the problems by points per minute; check the scoreboard | correct | homework-4/3 |
| homework-4.json | items[3].widget.lines[4].text | Restate the first problem in one sentence | correct | homework-4/3 |
| homework-4.json | items[3].widget.lines[5].text | Start coding it | correct | homework-4/3 |
| homework-4.json | items[3].feedback.correct | Read everything, rank, then restate and code the first. | correct | homework-4/3 |
| homework-4.json | items[3].feedback.generic | Not quite right. Coding comes last; reading and ranking come first. | correct | homework-4/3 |
| homework-4.json | items[3].explain.text | Reading all the constraints first is what lets you rank the problems. Restating t... | correct | homework-4/3 |
| homework-4.json | items[4].prose | ICPC style, 20 penalty minutes per rejection on a solved problem. You solved A at... | correct | homework-4/4 |
| homework-4.json | items[4].widget.accept | 269: $8 + 27 + 64 + 110 + 20 \cdot 3$. | correct | homework-4/4 |
| homework-4.json | items[4].feedback.correct | 269 minutes. | correct | homework-4/4 |
| homework-4.json | items[4].feedback.generic | Not quite right. Add the solve minutes, then 20 for each rejection on a solved pr... | correct | homework-4/4 |
| homework-4.json | items[4].feedback.byKey.withE | You charged E's four rejections. E was never solved, so they cost nothing. | correct | homework-4/4 |
| homework-4.json | items[4].feedback.byKey.nopen | You left out the rejections on B and C, which cost 60. | correct | homework-4/4 |
| homework-4.json | items[4].explain.text | The solve minutes total 209, and the three rejections on B and C add 60, for 269.... | correct | homework-4/4 |
| homework-4.json | items[5].prose | You are on the trader track, with a Codeforces rating of 1,380 and a month before... | correct | homework-4/5 |
| homework-4.json | items[5].widget.options[0].text | Push the rating from 1,380 past 1,600 | correct | homework-4/5 |
| homework-4.json | items[5].widget.options[1].text | Enter IMC Prosperity and write it up | correct | homework-4/5 |
| homework-4.json | items[5].widget.options[1].why | That is the trader track's own addition, so it does a lot. | correct | homework-4/5 |
| homework-4.json | items[5].widget.options[2].text | Daily probability and mental-arithmetic drills | correct | homework-4/5 |
| homework-4.json | items[5].widget.options[2].why | Lesson 16's table lists these for trader interviews. | correct | homework-4/5 |
| homework-4.json | items[5].widget.options[3].text | Practise market-making games with a friend | correct | homework-4/5 |
| homework-4.json | items[5].widget.options[3].why | Market-making games are on lesson 16's trader row. | correct | homework-4/5 |
| homework-4.json | items[5].feedback.correct | The rating: the curriculum counts it for little in trader interviews. | correct | homework-4/5 |
| homework-4.json | items[5].feedback.generic | Not quite right. Ask what trader interviews test. | correct | homework-4/5 |
| homework-4.json | items[5].explain.text | Lesson 16's table lists probability, mental arithmetic and market-making games fo... | correct | homework-4/5 |
| homework-4.json | items[6].widget.prompt | Write up the virtual contest from lesson 13 as you sat it, or from Alex's log. Fo... | correct | homework-4/6 |
| homework-4.json | items[6].widget.model | **Virtual round, 60 minutes: A, B and C accepted, D not submitted.** **A, local p... | correct | homework-4/6 |
| homework-4.json | items[6].widget.rubric[0].text | Gives each problem's idea correctly: a loop, a sliding window, a binary search wi... | correct | homework-4/6 |
| homework-4.json | items[6].widget.rubric[1].text | States each complexity with its reason, at the stated limits | correct | homework-4/6 |
| homework-4.json | items[6].widget.rubric[2].text | Records the minutes and rejections per problem, from a time log | correct | homework-4/6 |
| homework-4.json | items[6].widget.rubric[3].text | Names at least two mistakes, each with a category and a rule to take from it | correct | homework-4/6 |
| homework-4.json | items[6].widget.rubric[4].text | Plans next week: one round, upsolving up to about 300 above, practice 100 to 200 ... | correct | homework-4/6 |
| homework-4.json | items[6].widget.rubric[5].text | Says plainly what a rating counts for on their track: helps developer roles, litt... | correct | homework-4/6 |
| homework-4.json | items[6].feedback.correct | Compare your write-up with the model and tick the rubric. | correct | homework-4/6 |
| homework-4.json | items[6].feedback.generic | Compare your write-up with the model and tick the rubric. | correct | homework-4/6 |
| homework-4.json | items[6].explain.text | A write-up turns an hour of contest into rules you will use next week. The rating... | correct | homework-4/6 |

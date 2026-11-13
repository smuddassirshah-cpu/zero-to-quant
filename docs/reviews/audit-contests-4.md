# Concept audit: contests level 4 (round 1, blind)

Scope: `app/content/courses/contests/` l13-virtual-contest, l14-which-first, l15-debugging-under-time, l16-upsolving, review-4, homework-4 (Stage 2, full ledger). Ledger: `docs/reports/audit-contests-4-ledger.md` (270 rows: correct 238, wrong 8, imprecise 9, misleading 0, unverified 15). Script: `docs/reports/contests-L4-concepts.py` (276 checks with `--pyodide`; 15 fail, all labelled FINDING 1 to 8, so it exits 1 until those lines are fixed).

Blind rule: the earlier reviews, reports, audit files, log, notes and the course folder's git history were not opened before the ledger and the findings below were committed (commit "WIP: contests L4 ledger and findings"). One leak to declare: a `grep` for function names in `docs/reports/contests-L4-numbers.py` also printed nine of its comment lines, which name earlier findings 12 to 27 by number and state two of them (the "about a sixth" figure and the ends slip on test 3 of problem A). Both lines were re-derived here and are correct; neither is a finding of this audit.

How the code was run. All 16 code widgets are Python; the level has no C++ and no `error` or `compile` feedback line. The script copies the page's harness (`app/js/engine/widgets/code.js`): prelude and learner code load once into one module, the tests run in order in that module, a wrong value, an exception or 5 s without an answer on test N gives the key `test-N`, and `error` shows only when the code does not load. Natively this is CPython 3.13 with `sys.setrecursionlimit(3000)`; part D reruns every solution in Pyodide 0.27.7 (CPython 3.12.7, wasm32) under node with the local CDN. Where native and page could differ: speed (Pyodide is slower; the slowest solution test took 0.8 s there against a 5 s limit, and every time-limit mutant ran past 5 s natively, so it does on the page too); `random` streams (the seeded expected values agree in both, since every solution passed in Pyodide); recursion (same limit of 3,000 in both; a million frames ran in Pyodide under node's V8 once the limit was raised, other browser engines were not tested); integer width (Python integers are unbounded on wasm32 too, and the only C++ type claims are `int` and `long long`, 32 and 64 bits on wasm32 as elsewhere).

Each of the 52 `test-N` lines was tested by writing the mistake it names as a real submission. 44 lines hold: their slip first fails at test N, or the line only describes the test and is true. The 8 lines in findings 2 to 8 do not.

## Findings

1. l13-virtual-contest.json | screens[3].explain.text and screens[3].feedback.byKey | imprecise | minor | The explain says "The plateau test catches a `>=` slip", and the only plateau line is `test-6`. A `>=` written on both comparisons stops one test earlier, on the flat closes of test 5, which has no line, so the learner sees only the generic sentence. | Script FINDING 1: `closes[i] >= closes[i - 1] and closes[i] >= closes[i + 1]` returns 2 on `[2, 2, 2, 2]` and first fails at test-5. A `>=` on one side only does reach test-6 (part B). | Add `feedback.byKey.test-5`: "Test 5 is four equal closes, 2 2 2 2. No close is strictly above a neighbour, so `>=` counts peaks that are not there." Change the explain's second sentence to: "The flat and plateau tests catch a `>=` slip."

2. l14-which-first.json | screens[4].feedback.byKey.test-6 | wrong | minor | "Test 6 decays to 100, under the floor of 450. Apply the floor after both costs." The mistake it names, flooring before a cost, never reaches test 6. | Script FINDING 2: `max(floor * value, value - per_minute * minute) - per_wrong * wrong` gives 110 on test 2 (expected 150), and so does the floor applied before the time cost. Both first fail at test-2. No simple slip was found that passes tests 1 to 5 and fails 6. | Delete `test-6`. Replace `test-2` with: "Test 2 is A at minute 120 with three rejections: $500 - 240 - 150 = 110$, below the floor of 150. Apply the floor after both costs."

3. l14-which-first.json | screens[5].feedback.byKey.test-2 and screens[5].feedback.byKey.test-7 | wrong | minor | `test-2` ("no solves: the key is `(0, 0)`, whatever the rejections") names charging rejections on unsolved problems, which has already failed test 1, where `test-1` says the same thing. `test-7` ("Z ranks first despite its penalty of 400") cannot be reached: a key that sorts the three teams wrongly also fails test 1. The slip the tests do catch alone, `if minute:` dropping a solve at minute 0 (test 5), has no line. | Script FINDING 3: the unsolved-rejections mutant first fails at test-1; `(solved, penalty)`, `(penalty, -solved)` and `(-solved, -penalty)` each first fail at test-1; the `if minute:` mutant first fails at test-5. | Delete `test-2` and `test-7`. Add `test-5`: "Test 5 is a solve at minute 0 after five rejections. Test `minute is not None`: a bare `if minute:` drops a solve at minute 0."

4. l15-debugging-under-time.json | screens[5].feedback.byKey.test-6 | wrong | minor | "Test 6 calls `solve_all` twice. A set at module level keeps the first call's tickers." On the page the learner's code is loaded once and all six tests run in that one module, so a module-level set that survives a call is already stale at test 2 or 3. The line cannot show for the mistake it names. | Engine: `code.js` harness (no per-test reload outside script mode). Script FINDING 4: a module-level set emptied between cases but not between calls first fails at test-3 (test 2 ends with CCC in the set; test 3's first case then counts 2). The starter itself fails at test-2. | Delete `test-6`. Add `test-3`: "Test 3's first case is AAA alone, so its answer is 1. A set kept outside `solve_all` still holds tickers from an earlier call."

5. l15-debugging-under-time.json | screens[9].feedback.byKey.test-3 | wrong | minor | "Test 3's bug needs three values. Try every length from 1 upwards, not only the longest." A submission that tries only the longest length fails test 1, which expects `[2, 2]`. Test 3 is reached by stopping too early, at length 2. | Script FINDING 5: `stress(..., gen(rng, 8), ...)` alone first fails at test-1; a loop over lengths 1 and 2 first fails at test-3. | "Test 3's bug needs three values. Keep growing the length past 2: try every length from 1 to 8."

6. l16-upsolving.json | screens[5].feedback.byKey.test-4 | wrong | minor | "Test 4 ties *edge case* and *misread* at 2. Break the tie alphabetically." Test 1, the lesson's own log, already ties *greedy without proof* and *misread a constraint* at 2, with *misread* logged first. Every missing tie-break stops there, under the generic line. | Script FINDING 6: sorting by count only, `Counter.most_common()` and a descending sort of `(count, name)` each first fail at test-1. | Delete `test-4`. Add `test-1`: "Test 1 ties *greedy without proof* and *misread a constraint* at 2. Break the tie alphabetically: *greedy without proof* first."

7. homework-4.json | items[0].feedback.byKey.test-5 | wrong | minor | "Test 5 has isolated desks. Each one is a group of its own." Example 2, which is test 2, already leaves desks 2 and 3 isolated, so a count that misses isolated desks stops at test 2. | Script FINDING 7: starting only from desks that still have a link, or only from desks named in a link, first fails at test-2 (1 or 2 groups against 3). | Delete `test-5`. Add `test-2`: "Test 2 leaves desks 2 and 3 with no link. Each isolated desk is a group of its own, so the answer is 3."

8. homework-4.json | items[2].feedback.byKey.test-5 | wrong | minor | "Test 5 is unsorted. Sort the levels before the greedy check." The example, test 1, is `1 2 8 4 9`, unsorted too. A solution with no sort returns 1 there, not 3. | Script FINDING 8: the solution with `xs = list(levels)` first fails at test-1. | Delete `test-5`. Add `test-1`: "Test 1's levels, 1 2 8 4 9, are not sorted. Sort them before the greedy check."

9. l14-which-first.json | screens[6].prose and screens[6].explain.text | imprecise | minor | The curve $E(x) = 1000(1 - e^{-x/50}) + 800(1 - e^{-(60 - x)/15})$ is the expected score only if D keeps its $x$ minutes whether or not it has fallen. The explain then says "A time cap on a stuck problem is this curve in practice", but a cap is left as soon as D is solved, and under the same model that policy peaks later and higher. A learner takes 35 minutes as the best cap; it is the best fixed split. | Derivation: with solve times exponential (means 50 and 15), stopping D when solved gives $V'(x) = e^{-x/50}\,(20 - \tfrac{160}{3} e^{-(60 - x)/15})$, zero at $x = 60 - 15\ln(8/3) = 45.3$, with $V = 1{,}229$ against $1{,}202$ at 35. Script: "split curve, stop-when-solved version" (quadrature) and a Monte Carlo of 200,000 rounds at each cap, which agree. The key 34.84 is right for the curve as drawn. | Prose, third sentence: "The curve is the expected score if D gets exactly the first $x$ minutes, solved or not, and E the rest." Explain: "The best fixed split is about 35 minutes on D, for about 1,152 points. All D gives 699 and all E 785. If you leave D the minute it falls, the same model puts the best cap later, near 45 minutes."

10. l14-which-first.json | screens[6].feedback.byKey.all and screens[6].feedback.byKey.none | imprecise | minor | The `all` region is $x$ from 50 to 60 and its line says "You gave D the whole hour, which is about 699 points"; the `none` region is $x$ from 0 to 8 and says "You skipped D altogether, which is about 785 points". Each figure holds at one edge only. A point dropped at 50 reads 1,021 in the caption, and at 8 it reads 923. | $E(60) = 698.8$, $E(50) = 1021.4$, $E(0) = 785.3$, $E(8) = 922.9$ (script: split curve check, and direct evaluation). | `all`: "You gave D nearly the whole hour. All 60 minutes on D is about 699 points, and E's quick points were worth more." `none`: "You gave D almost no time. Skipping D altogether is about 785 points, and some time on D pays."

11. l14-which-first.json | screens[11].prose (with options[1] and feedback.byKey.hedge) | imprecise | serious | "The same rule applies: value per minute, largest first." The lesson's rule was proved for scores that decay while a problem waits. The desk states no decay, only a close in 30 minutes. As written, quote then hedge and hedge then quote both finish by the close and both earn £15,000, so the option graded wrong is as good as the key. Screen 10 of the same lesson shows the rate order failing under a deadline, which makes the unqualified "same rule" the wrong lesson to carry. | Exchange argument of screens[9]: the swap changes the loss by $(v_j t_i - v_i t_j)/250$ only because each problem loses value per minute waited (Smith's rule, Pinedo section 3.1). With no loss rate the order of two tasks that both fit does not matter: $5 + 25 = 30$ either way. With a loss in proportion to value, the rates £600, £480 and £100 a minute give quote, hedge, reconcile (script: desk check). | Prose: "Half an hour before the close, three tasks wait on a trading desk. Each has an estimated value and time, and loses a fixed share of that value for every minute it waits. The same rule applies: value per minute, largest first."

12. l15-debugging-under-time.json | screens[2].explain.text | imprecise | minor | "The stress test, from lesson 4, finds the rest." A stress test on small random cases finds wrong answers that small cases can show. It cannot show a solution that is too slow, a recursion that is too deep or an overflow that needs large values, and it misses a misreading shared by the fast and brute versions. The lesson's own test 6 of `smallest_failing` shows a stress test missing the tie bug. | Script: `smallest_failing(fast_ties, brute_inv, gen_wide, 3)` is `None` (part A, test 6); the chance of any tie in that call is under 5% (part C). Laaksonen, chapter 1 (testing against a brute force on small inputs). | "Each step is cheaper than the next and catches a common bug class. Rereading finds misreadings, hand cases find off-by-ones, and limits find overflow. The stress test, from lesson 4, finds what small random cases can show, not slowness or large-value overflow."

13. homework-4.json | items[0].widget.how | imprecise | minor | "a recursive DFS goes 100,000 deep, far past Python's default limit of 1,000". The default is 1,000, but this widget runs with `sys.setrecursionlimit(3000)`, so the limit the learner meets, and can read with `sys.getrecursionlimit()`, is 3,000. | Engine: `drill-worker.js`, `RECURSION_LIMIT = 3000`. Script part D, "limit 3000": 3,500 nested calls raise `RecursionError` in Pyodide; part B: the recursive DFS first fails at test-7. The depth is right: the cut leaves a run of 100,001 desks. | Second sentence of `how`: "Test 7 is a chain of 200,000 desks cut in the middle: a recursive DFS goes 100,000 deep, far past the 3,000 nested calls this page allows (Python's default is 1,000)."

14. l13-virtual-contest.json | screens[1].explain.text | imprecise | minor | "Every statement has a line like it." Problems B and C of this round have no such note, so the "every" is false on the screen that states it. | The four statements in screens[1].canvas: only A and D carry a note. | Third sentence: "Many statements have a line like it."

Severity counts: wrong 7 (all minor), imprecise 7 (1 serious, 6 minor), misleading 0. Serious 1, minor 13.

### Unverified rows (15)

None is a pass. They are listed so that an owner can source or soften them; no fix is proposed except where stated.

- Codeforces behaviour (4 rows): the scoreboard "as it stood" in virtual participation (l13 screens[2]); the failing test hidden during a round (l15 screens[0]) and shown afterwards with the editorial (l16 screens[1]); and "not Codeforces' current rule" (l14 screens[0]). On the last: a search found Codeforces' own description of the decay, 2 points a minute for a 500-point problem in a two-hour round, which is $v/250$. The 50 per rejection and the 30% floor were not confirmed from an official page. If all three match, the disclaimer should read "close to Codeforces' rule for a two-hour round".
- "Most wrong answers are misreadings" (l15 screens[0].prose and summary.ideas[0]): an empirical "most" with no source. Suggested wording in both places: "Many wrong answers are misreadings".
- Problem ratings "about 800" (l13 screens[3]): the author's estimate; the same holds for the other "about" ratings, judged plausible.
- Training claims (4 rows): upsolving "teaches the most per hour" (l16 screens[0]); one new idea just above your level (l16 screens[6]); ratings stall without upsolving (l16 screens[7], [8]); interviewers mark the small-case habit (l15 screens[10]).
- Hiring claims (5 rows): the 1,400 target, Indian campus shortlisting, where a rating helps, LeetCode mediums in 30 minutes, and what each track's interviews test (l16 screens[10], quiz[3]; homework-4 items[5]). All copy `docs/curriculum.md` section 2.4 faithfully; the curriculum itself cites no checkable source.

### Checked and clean

- Every solution passes its hidden tests natively and in Pyodide; every starter fails; the three "fix this submission" starters fail at the test their screen names (4, 3 and 2).
- ICPC rules as stated (solved count, then penalty; 20 per rejection, on solved problems only) match ICPC regional rules and World Finals judging notes, and the lesson labels the 20 as its illustration.
- The decay arithmetic of l14 and review-4, the three bar charts, the brute-force optimum over all 24 orders (3,550, reached by A B C D and B A C D only, which the `same` pair accepts), the 60-minute exception (2,090), and the exchange formula with its sign rule (20,000 random pairs, and 2,000 random rounds against brute force).
- `equal_thirds`, `max_profit_k` and `widest_gap` against independent brute forces; the binomial counts; the overflow and `double` claims; the hand-case table of l15; the logs of l13.
- "It works in this app's Pyodide, which ran a million frames in our test" (l15 screens[7]): reproduced under node.

## Gates

- `node tools/validate.mjs 2>&1 | tail -5`: 0 errors, 4537 warnings (exit 0).
- `node tools/run-number-scripts.mjs --python <venv python> --only contests-L4`: 1 of 367 scripts, 1 passed, 0 new failures (exit 0).
- `node tools/grade-all.mjs --file <path> --local-cdn <pkgs>`: 0 failures for each of the six files (exit 0 each; 10, 10, 9, 12, 8 and 2 widgets checked).
- `python docs/reports/contests-L4-concepts.py --pyodide <pkgs>`: 276 checks, 15 failing, exit 1. All 15 are FINDING 1 to 8 checks, which hold content claims that are false. Without `--pyodide`: 237 checks, the same 15 failing.
- No content was changed, so no playthrough was run.

## Overlap with earlier reads

Filled after commit 79c722bc ("WIP: contests L4 ledger and findings"), from `docs/reviews/review-contests-3-4.md`, level 4 section (findings 13 to 27, with the level 4 parts of the advisory classes 11 and 12) and its fix pass. Every one of its findings was applied before this audit read the files, so the audit read the corrected text.

| Count | Conceptual findings |
|---|---|
| Audit only | 14 (findings 1 to 14 above) |
| Earlier review only | 5 (13, 14, 20, 21, 22; all fixed before this audit) |
| Both | 0 |

The earlier review's conceptual findings at level 4, and what this audit found in their place:

- 13, l13 screens[10] "a tenth of a problem": fixed to "a sixth"; the ledger records the new line as correct ($4 / 25 = 0.16$).
- 14, l13 screens[3] no `test-3` line for the ends slip: fixed; the script's "counts the last day" mutant lands on the new line. This is the same class as findings 2 to 8 here, which the earlier review found once and this audit found in seven more widgets by sweeping every line.
- 20, l14 screens[9] swap formula without the floor condition: fixed; the ledger records the conditioned sentence as correct, and finding 11 here is the same missing-hypothesis class one screen later (the desk has no decay at all).
- 21, l15 screens[0] "the commonest wrong answer" against "Most wrong answers are misreadings": fixed to "a very common"; the surviving "Most" is in the unverified list.
- 22, l15 screens[9] "no longer than it has to be" and "never tie": fixed; the ledger records both new sentences as correct. Finding 12 here is a neighbouring overclaim about the stress test that the earlier review did not raise.

Its other level 4 findings are voice, layout, continuity or freshness (15 to 19, 23 to 27, and classes 11 and 12) and are not counted. Its engine item 3 (a `list(xs)` copy defeats the read counter on l13 problem B) was met again here as the mutant that reaches `test-9`; no content change follows.

Miss rate of a single read, as this pair measures it: 19 distinct conceptual findings, 0 found by both. All 7 `wrong` findings here are feedback lines that cannot show for the mistake they name; none changes a definition, method or graded answer.

## Inbox

- Code widget tests are not independent: the learner's module is loaded once and every test runs in it (`code.js`, non-script harness). A "two calls in a row" test therefore adds nothing over the tests before it (finding 4). Worth a line in `docs/AUTHORING.md`, or a per-test reload option.
- Finding class "the mistake a `test-N` line names stops at an earlier test" appeared 8 times in 52 lines here, and at a similar rate in sister courses. Under SESSION PROTOCOL 6 it should become a tool: let a number script declare `mutants` (key, code) per code widget and have `run-number-scripts` or the validator assert the first failing key.
- l13 screens[5], test 10: the test allows at most 13 `can_ship` calls but not fewer than one, so a `min_capacity` with its own inline check passes although the prose says it must call `can_ship`. A bound of `1 <= calls <= 13` would enforce the sentence.
- drag-point `wrong[].region` feedback is fixed text for a whole region (finding 10). Allowing the `derive` template (`{{fixed(...)}}`) in `feedback.byKey` lines would let the line quote the value at the dropped point.

## Fix pass

Opus fixer, round 1. Every `test-N` line below was rerun as a real submission in Pyodide 0.27.7 under node (local CDN), with the page's harness: one module, tests in order, `sys.setrecursionlimit(3000)`, first failing test gives the key (scratch `contests4-fix/mutants.py`, 24 runs, all as stated). No key, slip value, hidden test, solution or starter changed. The concepts script's FINDING checks and `EXPECT_KEYS` now pin the moved lines. The number script's two checks on deleted lines (l14 `test-6` 100, `test-7` 400) were replaced by checks on the new lines and the new figures (45, 699, 785, 600, 750).

| # | status | basis (fixer's own) |
|---|---|---|
| 1 | fixed | Both-sided `>=` returns 2 on `[2, 2, 2, 2]` and first fails at test-5; left-only `>=` passes test 5 and fails test-6, so both lines are reachable. Explain now says "flat and plateau tests". |
| 2 | fixed | No floor, floor before the time cost and floor before the attempt cost each give 110 on test 2 and first fail there; nothing found reaches test 6. `test-6` deleted, "Apply the floor after both costs" moved to `test-2`. |
| 3 | fixed | Charging unsolved rejections gives `(-3, 268)` on test 1; any wrong order or sign of the tuple fails test 1's exact compare; `if minute:` returns `(0, 0)` on `[(0, 5)]` and first fails at test-5. `test-2` and `test-7` deleted, `test-5` added. |
| 4 | fixed | Tests 1 to 6 run in one module, so state that survives a call is caught by test 2 or 3 already; the set cleared between cases only first fails at test-3 (CCC left from test 2). `test-6` deleted, `test-3` added. |
| 5 | fixed | Length 8 only returns a length-8 case on test 1 (fails test-1); lengths 1 and 2 only return `None` on test 3 (fails test-3). The line now names stopping at 2. |
| 6 | fixed differently | A count-only stable sort and `most_common()` put *misread a constraint* first on test 1 and fail there. The new `test-1` line also says "Sort by count, most first", since any wrong sort shows it. |
| 7 | fixed differently | Starting only from desks with a link gives 1 group on test 2 (cutting (1, 2) leaves desks 2 and 3 bare). The line names the cut link, so the learner sees why desk 2 is isolated. |
| 8 | fixed | Without the sort, test 1's `1 2 8 4 9` gives 1, not 3 (first fails at test-1). |
| 9 | fixed differently | Derived: with exponential solve times (means 50 and 15), leaving D when solved gives $V'(x) = e^{-x/50}(20 - \tfrac{160}{3}e^{-(60-x)/15})$, zero at $60 - 15\ln(8/3) = 45.29$; quadrature gives 45.29 and $V = 1{,}229$, Monte Carlo (400,000 rounds) 1,229 at 45 against 1,204 at 35. The fixed split peaks at 34.84, 1,152.3 (scipy and golden section). Prose now says "exactly $x$ minutes, solved or not"; the explain names the fixed split and the later cap near 45. Key 34.84 unchanged. |
| 10 | fixed | $E(60) = 698.8$, $E(50) = 1{,}021.4$, $E(0) = 785.3$, $E(8) = 922.9$; the new lines give each figure as the edge value, not the dropped point's. |
| 11 | fixed differently | With no loss while waiting, quote then hedge and hedge then quote both total £15,000 by the close, so two answers tied. The prose now says each task loses a fixed share $s$ of its value each minute it waits. Then quote first changes the loss by $s(3{,}000 \cdot 25 - 12{,}000 \cdot 5)$ in its favour, a saving of $15{,}000s$, so the quote is the one best answer (Smith's rule: £600, £480, £100 a minute). The explain works it at 1% a minute: quote first costs the hedge $12{,}000 \times 0.05 = £600$, hedge first costs the quote $3{,}000 \times 0.25 = £750$. Key unchanged. |
| 12 | fixed differently | Test 6 of `smallest_failing` (wide values, tie bug, `None`) shows a stress test missing a bug. The third sentence now says it finds "wrong answers that small random cases can show", without a list of what it misses. |
| 13 | fixed | `code.js` runs Python through `drill-worker.js`, which sets `RECURSION_LIMIT = 3000`; the recursive DFS first fails at test-7 in Pyodide. |
| 14 | fixed differently | Only A and D carry a note, and the auditor's "Many statements" is itself an unsourced frequency claim. Now an instruction: "Look for a line like it in every statement: D's note is another." |

Unverified rows (15):

| row | status | basis |
|---|---|---|
| l13 screens[2]: scoreboard "as it stood" | fixed | Clause removed; the name "virtual participation" is Codeforces' own and stays. |
| l13 screens[3]: "about 800 on Codeforces' scale" | fixed | Now "by our estimate"; screen 2's option now says each code screen gives "our estimate of its rating". The problems are the course's own, so a rating can only be an estimate. |
| l14 screens[0]: "not Codeforces' current rule" | fixed | Replaced by an instruction: "check a real round's announcement for its rule". No claim about Codeforces' rule remains. |
| l15 screens[0]: test hidden during the round | fixed | Now a fact of the scenario: "This round's judge shows the verdict, not test 4 itself" (the canvas shows only the verdict line). |
| l15 screens[0] and summary.ideas[0]: "most wrong answers are misreadings" | fixed | Both now give the reason the lesson can stand behind: rereading is the cheapest check (screen 2's ordering). |
| l15 screens[10]: interviewers mark the habit | fixed | Replaced by "It is the contest routine again: the smallest reproduction first." |
| l16 screens[0].hints[2]: "teaches the most per hour" | fixed | Now "works on exactly what you could not do", true by the scenario (D and E are the problems that beat you). |
| l16 screens[1]: Codeforces shows the failing test and editorial | fixed | Now a fact of this round: "the judge shows you the failing test and the editorial is out". |
| l16 screens[6]: one new idea just above your level | fixed | Stated as the lesson's assumption, with the conclusion drawn on it; `byKey.l4` says the editorial "may" rest on unmet ideas. |
| l16 screens[7], [8]: ratings stall without upsolving | fixed | Now "nothing closes the gaps each round shows, so the same mistakes can repeat" and "more rounds without upsolving leave the same gaps open": a possibility, not a causal law. |
| l16 screens[10]: 1,400 target, Indian shortlisting, where a rating helps | fixed | Attributed to the curriculum (`docs/curriculum.md` 2.4, read), as are summary.ideas[2], homework-4 items[5].feedback.correct and the model answer's rating paragraph (items[6]). |
| l16 screens[10]: LeetCode mediums in 30 minutes | fixed | "Most coding interviews use" removed; now the curriculum's aim (1.8 exit line). |
| l16 screens[10]: what each track's interviews test | fixed | Prose says the table is the curriculum's (its Stage 2 track table); option whys, hint and explain now read "in the table". |
| l16 quiz[3]: trader interviews test | fixed | The question asks "By this lesson's table"; the why and explain cite the table's trader row. |
| homework-4 items[5]: the rating does least for a trader | fixed | Prose adds "Take lesson 16's table"; the whys and explain cite it. The key (the rating) is unchanged and follows from the table. |

Counts: fixed 8, fixed differently 6, not applied 0, disputed 0; unverified rows rewritten 15 of 15. review-4.json had no finding and was not changed.

Gates (fixer): validator 0 errors (manifest unchanged); `contests-L4-concepts.py --pyodide`: 276 checks, 0 failing; `run-number-scripts --only contests-L4`: 1 passed; `grade-all --file`: 0 failures on each of the five changed files; `voice-scan.py 35`: 0 explanations over three sentences, 0 sentences over 35 words; playthrough of l13, l14, l15, l16 (`--lesson`) and homework-4 (`--set`), desktop and `--mobile`: all passed.

## Fix-pass read

Round 1, blind read of `git diff c71901d3~1 c71901d3 -- app/content/courses/contests` (46 changed strings in five files). Each row was read with its whole screen or item. Check script: `docs/reports/contests-L4-fixread.py` (exit 0, 118 checks). "Run" means the named mistake was written as a submission and run against the widget's hidden tests in order, with the judge of `js/engine/widgets/code.js` (one namespace for all tests, key `test-(first failure + 1)`, recursion limit 3000 from `js/screens/drill-worker.js`). Curriculum citations were matched against `docs/curriculum.md` sections 1.8, Stage 2 track table and 2.4.

| file | JSON path | new text (short) | verdict | basis |
| --- | --- | --- | --- | --- |
| l13-virtual-contest | screens[1].explain.text | "Look for a line like it in every statement: D's note is another." | correct | Frame D of the same screen ends "Note: a one-way cell may be entered from any side"; the sentence is an instruction, not a claim that every statement has a note. |
| l13-virtual-contest | screens[2].prose | "Codeforces calls it virtual participation." | correct | Codeforces contest pages and help use the term "Virtual participation"; the scoreboard claim is gone. Curriculum 2.4 asks for one contest a week. |
| l13-virtual-contest | screens[2].widget.options[3].why | "Each code screen gives our estimate of its rating, from about 800 to about 1500." | correct | The four code screens' prose reads about 800, 1100, 1300, 1500 (script). |
| l13-virtual-contest | screens[3].prose | "about 800 on Codeforces' scale by our estimate" | correct | Stated as the course's own estimate. |
| l13-virtual-contest | screens[3].feedback.byKey.test-5 | "Test 5 is four equal closes, 2 2 2 2 ... `>=` counts peaks that are not there." | correct | Run: `>=` on both sides passes tests 1 to 4, returns 2 on test 5, first failure test 5. |
| l13-virtual-contest | screens[3].explain.text | "The flat and plateau tests catch a `>=` slip." | correct | Tests 5 (2 2 2 2) and 6 (1 3 3 1) both fail under `>=`; run. |
| l14-which-first | screens[0].prose | "this course's illustration; check a real round's announcement for its rule" | correct | No platform claim left; table rows lose v/250 a minute (2, 4, 6, 8). |
| l14-which-first | screens[4].feedback.byKey.test-2 | "500 - 240 - 150 = 110, below the floor of 150. Apply the floor after both costs." | correct | 500 - 2(120) - 3(50) = 110; 0.3(500) = 150. Run: floor before the attempt cost, and no floor, both fail first at test 2. |
| l14-which-first | screens[5].feedback.byKey.test-5 | "a solve at minute 0 after five rejections ... a bare `if minute:` drops a solve at minute 0" | correct | Run: `if minute:` passes tests 1 to 4, gives (0, 0) for [(0, 5)], first failure test 5. |
| l14-which-first | screens[6].prose | "if D gets exactly x minutes, solved or not, and E the rest" | correct | Matches E(x) = 1000(1 - e^(-x/50)) + 800(1 - e^(-(60-x)/15)): a fixed split. |
| l14-which-first | screens[6].feedback.byKey.all | "nearly the whole hour. All 60 minutes on D is about 699 points" | correct | E(60) = 1000(1 - e^(-1.2)) = 698.8; region x in [50, 60]. |
| l14-which-first | screens[6].feedback.byKey.none | "almost no time. Skipping D altogether is about 785 points" | correct | E(0) = 800(1 - e^(-4)) = 785.3; region x in [0, 8]; E rises to x = 34.84. |
| l14-which-first | screens[6].explain.text | "best fixed split is about 35 minutes ... Leave D the moment it is solved, and the same model puts the best cap later, near 45 minutes." | correct | Grid: argmax 34.84, E = 1152.3. Stop-when-solved with exponential solving times (means 50 and 15): dV/dc = e^(-c/50)(20 - (800/15)e^(-(60-c)/15)) = 0 at c = 60 - 15 ln(8/3) = 45.29. Simulation of 400,000 rounds agrees with the integral and puts 45 above 35. Three sentences. |
| l14-which-first | screens[11].prose | "loses a fixed share of its value each minute it waits. The same rule applies: value per minute, largest first." | correct | A fixed share of value per minute of waiting is weighted completion time; Smith's rule (1956) orders by value over time. |
| l14-which-first | screens[11].explain.text | "Both fit in the half hour ... At 1% a minute, quote first costs the hedge £600 and hedge first costs the quote £750." | correct | 5 + 25 = 30; 1% x 5 x 12,000 = 600; 1% x 25 x 3,000 = 750. Enumeration of all six orders with a 30-minute close, five rates from 0.1% to 3%, waiting counted to start or to finish: quote first is the unique best. Option figures £600, £480, £100 a minute recomputed. |
| l15-debugging-under-time | screens[0].prose | "This round's judge shows the verdict, not test 4 itself. A misreading is the cheapest bug to check for" | correct | Stated for this round, not for a platform. Rereading needs no new code or input, the other three steps do. |
| l15-debugging-under-time | screens[2].explain.text | "The stress test ... finds wrong answers that small random cases can show." | correct | True by construction of a stress test; lesson 4 is `l4-stress-testing`. Three sentences. |
| l15-debugging-under-time | screens[5].feedback.byKey.test-3 | "Test 3's first case is AAA alone ... A set kept outside `solve_all` still holds tickers from an earlier call." | correct | Run: a module-level set cleared only between cases passes tests 1 and 2 (test 1 leaves AAA, BBB, which test 2's first case repeats), then gives [2, 1, 2] on test 3, first failure test 3. The starter fails first at test 2. |
| l15-debugging-under-time | screens[9].feedback.byKey.test-3 | "Keep growing the length past 2: try every length from 1 to 8." | correct | Run: `range(1, 3)` passes tests 1 and 2 (found at length 2), returns None on test 3 (expects [2, 1, 1]), first failure test 3. |
| l15-debugging-under-time | screens[10].explain.text | "It is the contest routine again: the smallest reproduction first." | correct | Restates the screen's key; the hiring claim is gone. Three sentences. |
| l15-debugging-under-time | summary.ideas[0] | "reread the statement against the code: it is the cheapest check" | correct | As screens[0] and the hint on screens[2] (rereading takes a minute). |
| l16-upsolving | screens[0].hints[2].text | "works on exactly what you could not do" | correct | Definitional: the unsolved problems are what you could not do. |
| l16-upsolving | screens[1].prose | "After this round, the judge shows you the failing test and the editorial is out." | correct | Stated for this round. C(4, 2) = 6 and C(199999, 2) = 19,999,700,001 recomputed. |
| l16-upsolving | screens[5].feedback.byKey.test-1 | "Test 1 ties *greedy without proof* and *misread a constraint* at 2 ... *greedy without proof* first." | correct | Run: a stable sort by count only, and `Counter.most_common()`, both put misread first and fail first at test 1. Expected row order checked. |
| l16-upsolving | screens[6].feedback.byKey.l4 | "Its editorial may rest on ideas you have not met yet" | correct | Hedged; 1900 - 1200 = 700. |
| l16-upsolving | screens[6].explain.text | "This lesson assumes a problem up to 300 above you needs one new idea ... On that assumption" | correct | Stated as the lesson's assumption. Three sentences. |
| l16-upsolving | screens[7].widget.options[1].why | "nothing closes the gaps each round shows, so the same mistakes can repeat" | correct | Hedged ("can"); follows from the plan having no upsolving. |
| l16-upsolving | screens[8].widget.options[2].why | "More rounds without upsolving leave the same gaps open." | unverified | A training claim stated without a hedge: a later round can meet the same idea and close a gap. The sibling line on screens[7] was hedged; this one was not. Minor. Replacement below. |
| l16-upsolving | screens[10].prose | "The curriculum sets a rating of 1,400 ... Its coding aim is a fresh LeetCode medium in 30 minutes." | correct | docs/curriculum.md 2.4 (1400 target; shortlisting "mainly a feature of Indian campus hiring"; "Elsewhere a rating helps developer applications and counts for little in trader or researcher interviews"), Stage 2 track table, 1.8 exit. The table is a shortened copy of the curriculum's rows. Longest sentence under 35 words. |
| l16-upsolving | screens[10].widget.options[1].why | "In the table, trader interviews test probability, mental arithmetic and market-making games, not contest algorithms." | correct | The screen's trader row. |
| l16-upsolving | screens[10].widget.options[2].why | "In the table, those interviews test statistics, machine learning and a data take-home." | correct | The screen's researcher row. |
| l16-upsolving | screens[10].hints[2].text | "In the table, developer interviews test algorithms and C++" | correct | The screen's developer row. |
| l16-upsolving | screens[10].explain.text | "which the table's developer interviews test directly. The trader and researcher rows test other things" | correct | Conditional on the table. Two sentences. |
| l16-upsolving | summary.ideas[2] | "The curriculum's first-year target is a rating of 1,400; it counts a rating towards developer applications, and little towards trader or researcher interviews." | correct | Curriculum 2.4; the interview statement follows from the track table, which has no regional condition. |
| l16-upsolving | quiz[3].question | "By this lesson's table, what will the interviews mostly test?" | correct | Conditional on the table; the key is the trader row. |
| l16-upsolving | quiz[3].widget.options[1].why | "The table's trader row lists other skills." | correct | Trader row has no algorithms. |
| l16-upsolving | quiz[3].explain.text | "This lesson's table lists probability, mental arithmetic and market-making games for traders" | correct | Trader row; IMC Prosperity is the curriculum's trader addition (2.4). |
| homework-4 | items[0].widget.how | "a recursive DFS goes 100,000 deep, far past the 3,000 nested calls this page allows (Python's default is 1,000)" | correct | `RECURSION_LIMIT = 3000` in drill-worker.js; CPython's default is 1000. Cutting link 100,000 leaves desks 0 to 100,000 in one chain. Run: a recursive DFS passes tests 1 to 6 and fails first at test 7; in Pyodide 0.27.7 under node the same DFS raises RecursionError at 200,000 desks. |
| homework-4 | items[0].feedback.byKey.test-2 | "Test 2 cuts link (1, 2), which leaves desks 2 and 3 with no link ... the answer is 3." | correct | Test 2 is n = 4, links (0,1) (1,2), cut 1: groups {0,1}, {2}, {3}. Run: counting only desks that keep a link passes test 1, gives 1 on test 2, first failure test 2. |
| homework-4 | items[2].feedback.byKey.test-1 | "Test 1's levels, 1 2 8 4 9, are not sorted. Sort them before the greedy check." | correct | Run: the solution without the sort returns 1, not 3, on test 1. |
| homework-4 | items[5].prose | "Take lesson 16's table of what each track's interviews test." | correct | Lesson 16 screens[10] has that table. |
| homework-4 | items[5].widget.options[2].why | "Lesson 16's table lists these for trader interviews." | correct | Trader row: probability, mental arithmetic. |
| homework-4 | items[5].widget.options[3].why | "Market-making games are on lesson 16's trader row." | correct | Trader row. |
| homework-4 | items[5].feedback.correct | "The rating: the curriculum counts it for little in trader interviews." | correct | Curriculum 2.4. The key is the only option off the trader row and the trader addition. |
| homework-4 | items[5].explain.text | "Lesson 16's table lists probability, mental arithmetic and market-making games for trader interviews." | correct | Trader row. Three sentences. |
| homework-4 | items[6].widget.model | "The curriculum says that outside Indian campus hiring a rating helps developer applications." | correct | Curriculum 2.4, "Elsewhere a rating helps developer applications". |

Tally: 46 rows; 45 correct, 0 wrong, 0 imprecise, 0 misleading, 1 unverified (minor). Voice gates pass on all 46 strings (no exclamation mark, no em-dash, longest sentence 35 words or fewer, every `explain` at most three sentences).

Replacement text:

1. `l16-upsolving.json` `screens[8].widget.options[2].why`: `You chose more rounds. More rounds without upsolving can leave the same gaps open.` Basis: a possibility, not a law; it matches the hedge on `screens[7].widget.options[1].why`. Two sentences, 14 words, British English.

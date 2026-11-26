# Concept audit, round 3: contests level 4

Auditor brief: `docs/briefs/concept-audit.md`, "Auditor brief (binding)". Blind: the ledger and the findings below were written before any earlier review, audit or author report on this course was opened. Content at `e69cac72`, unchanged by this audit.

Scope: `l13-virtual-contest`, `l14-which-first`, `l15-debugging-under-time`, `l16-upsolving`, `review-4`, `homework-4`. Level 4 has no `problems-*` file. The course is Stage 2 (topic 2.4), so the ledger is full.

- Ledger: `docs/reports/audit-contests-4-r3-ledger.md`, 951 rows: correct 948, imprecise 2, misleading 1, wrong 0, unverified 0.
- Script: `docs/reports/contests-L4-concepts-r3.py`, 342 checks. It exits 1 with 4 failing checks, which are the three findings below (finding 2 fails two checks). It will exit 0 once the two lines are reworded, the test of finding 3 is added, and the checks are re-pointed at the new content.

## Method

1. Every line of the six files read; every stated number recomputed from the JSON in part A of the script (scores for all 24 orders, the split curve, the swap formula, counts, slips, the log totals, the homework model's minutes).
2. Empirical claims by Monte Carlo in part B: the sequential plan "E first, then D" is worth about 1,363 (400,000 rounds, agrees with the closed form 1,362.9); "values to 10⁶ almost never tie" (probability 0.017 that a whole run of 1,600 cases holds any tie; 3 of 300 seeds find one).
3. Reference solutions against independent brute forces: `equal_thirds` (2,000 random cases), `max_profit_k` (1,500), `widest_gap` (800), and the points-per-minute order against all permutations (300 random rounds, no floor binding).
4. The `test-N` sweep, part C. All 52 `feedback.byKey.test-N` lines of the 16 code widgets were swept with 147 codings (plus the 16 solutions). Each coding was graded by the page's own harness under Pyodide 0.27.7 (`tools/code-runner.mjs`, 5 s a test, recursion limit 3,000) and again in CPython by the script; the two agree on all 163. Rule applied: a line that names a mistake is right only if at least half of the failing codings of that mistake fail first on test N. Codings written to probe a line but that are a different mistake are marked `named: false` in the script and do not count for or against it.

No C++ widget is in this level. The two C++ statements (a 32-bit `int` stops at 2,147,483,647; `long long` reaches about 9.2·10¹⁸) hold on x86-64 and on the page's wasm32 clang alike, by the ABI sizes, so no compile was needed.

## Findings

Three findings, all minor. Findings 1 and 2 are new `test-N` feedback lines. Finding 3 is round 2's finding 4, still open. No finding is `wrong`.

1. `l14-which-first.json` | `screens[10].feedback.byKey.test-4` | misleading, minor | The line says "It scores 0, and the total is 0", which points at the total. Every coding that fails first on test 4 already has the total right and fails on the names. | Test 4 is `best_order([('A', 500, 10)], 5)`, expected `(0, ['A'])`. Three natural codings fail first here: the best total started at 0 with a strict `>` gives `(0, None)`; the same with an empty list gives `(0, [])`; filtering out problems that cannot fit gives `(0, [])`. The one coding that does score a late problem fails first on test 2. So the line corrects a number the learner already has and is silent on what failed. Script checks `FINDING 1` (fails) and the line under it (passes). | Replace the line with: `Test 4's only problem needs 10 minutes of a 5-minute round, so it scores 0. The order still names it: return \`(0, ['A'])\`. Start the best total below 0, so that a total of 0 can still win.`

2. `l15-debugging-under-time.json` | `screens[5].feedback.byKey.test-3` | imprecise, minor | The line says the first case went wrong because "a set kept outside `solve_all` still holds tickers from an earlier call". That is one way to reach test 3, and not the likelier one. | Test 3 is `'3\n1\nAAA\n1\nAAA\n2\nBBB AAA\n'`, expected `[1, 1, 2]`. Of five codings that keep the set outside the function, three fail first on test 2, whose line fits them. Two reach test 3 with `[2, 1, 2]`, and both clear the set between cases but not before the first, which is contrived. A coding with no outside set at all, one set per call and the count of new tickers per case, also fails first on test 3, with `[1, 0, 1]`: its first case is right and its second is wrong, so both sentences of the line miss it. Script checks `line l15 screens[5] test-3` (2 of 5) and `FINDING 2` (both fail). | Replace the line with: `Test 3 is AAA, then AAA, then BBB AAA, so the answers are 1, 1 and 2. Each case counts its own tickers. Start every case, the first included, with an empty set.`

3. `l13-virtual-contest.json` | `screens[5].widget.tests` (with `.how` and `feedback.byKey.test-4`) | imprecise, minor | The solution returns False at once for an order heavier than the van, and the `how` note and the `test-4` line point at that case. No hidden test needs the guard, so a `can_ship` that is wrong on such inputs is accepted. | The usual greedy with no `w > cap` line passes all 11 tests under Pyodide: on test 4, `can_ship([5], 1, 4)`, the order opens day 2 and 2 > 1 gives False by the day count. The same code returns True for `can_ship([5, 5], 3, 4)`. Script check `FINDING 3` (fails) and the line under it (passes). | Not a one-sentence fix: it needs a hidden test, so it goes to a content pass that may add tests. Append a twelfth test, so no `test-N` line is renumbered: `{"call": "can_ship([5, 5], 3, 4)", "expect": "False", "compare": "equal"}`. In `how`, "Check runs 12 hidden tests" and, after the sentence on test 11, `Test 12 has two orders heavier than the van and three days.` Add `feedback.byKey.test-12`: `Test 12 has two orders of 5, a van of 4 and three days. No van load can hold an order of 5, so return False however many days there are.`

## Checked and left alone

These were probed because they looked at risk, and they hold.

- `l13` `screens[5]` `test-11` ("about 30 checks, not a million"): a scan that calls `can_ship` fails first on test 10, whose line also fits it. A scan with the greedy check written inline passes test 10 (no calls counted) and fails first on test 11, by time. One of two codings; the line is right for every submission that reaches it. Timing-dependent.
- `l13` `screens[5]` `test-4`: the line itself is right for what reaches it. Codings where the first order opens day 1 unconditionally fail first on test 4 (two of three). The plain greedy with no guard passes it, which is finding 3.
- `l13` `screens[5]` `test-10`: a search from 0 to the total passes (11 calls, limit 13), so the line's "between the heaviest order and the total" is advice, not what the test enforces. An upper bound of 10⁹ and a scan both fail first on test 10.
- `l13` `screens[6]` `test-9`: a BFS with no visited check passes tests 1 to 8 and is stopped on test 9, as the line says. Timing-dependent, with a wide margin.
- `l13` `screens[3]` `test-3` and `test-4`: codings that count both ends fail first on test 2 (one close); those that count only the last day fail on test 3, only the first on test 4. Each line fits the codings that reach it.
- `l15` `screens[7]`, option `limit`: "It works in this app's Pyodide, which ran a million frames in our test." Reproduced in node under Pyodide 0.27.7 with the page's worker grader: after `sys.setrecursionlimit(10**6)`, a line DFS of 100,000 and plain recursion of 999,900 frames both ran. Chrome was not run.
- `homework-4` `items[0]` `test-7`: the recursive DFS fails first on test 7; with `sys.setrecursionlimit(10**6)` it passes all 8 tests under Pyodide in node. The line's advice stands.
- `homework-4` `items[1]` `test-6`: reachable (three codings that demand exactly k trades, or refuse k > n, return 0 here), and its arithmetic, 2 + 3 + 4 = 9, is right.
- `l14` `screens[6]`: the curve's top is at 34.84 minutes and 1,152.3 points; "E first, then D" is the best adaptive plan because exponential solve times are memoryless and E's hazard, 53.3 points a minute, is above D's 20.
- `homework-4` `items[0]`: the statement says desks are numbered from 0 and does not say so of links; example 2 settles it (cut = 1 removes link (1, 2)).

## Timing-dependent lines

Six `test-N` lines rest on Pyodide's speed: `l13` `screens[4]` `test-9`, `screens[5]` `test-11`, `screens[6]` `test-9`; `l16` `screens[3]` `test-8`; `homework-4` `items[1]` `test-8` and `items[2]` `test-8`. In each the slow coding does at least 2·10⁹ basic steps against a 5 s limit, and the reference solution takes under 1 s under Pyodide in node (the slowest, `widest_gap`, 0.82 s). None is marginal.

## Validator and number scripts

- Validator (`cd app && node tools/validate.mjs`): 0 errors, 4,606 warnings; `content/manifest.json` unchanged.
- Number scripts (`node tools/run-number-scripts.mjs --only contests`, venv Python, NumPy 2.5): 5 of 436 scripts ran, 5 passed, 0 new failures, exit 0. The concepts script is not a number script and is not picked up by that job.
- `docs/reports/contests-L4-concepts-r3.py`: 342 checks, 4 failing, exit 1 (the findings).
- No playthrough: content unchanged.

## Overlap with earlier reads

Filled after the ledger and findings above were written.

Read after the blind work: `docs/reviews/audit-contests-4.md` (round 1, 14 findings, fix pass, fix-pass read), `docs/reviews/audit-contests-4-r2.md` (round 2, 11 findings, fix pass, fix-pass read) and the level 4 conceptual findings of `docs/reviews/review-contests-3-4.md` as those two audits list them (13, 14, 20, 21, 22). A finding counts as "both" only where an earlier read named the same defect.

| Count | Conceptual findings |
| --- | --- |
| This audit only | 2 (findings 1 and 2) |
| Earlier reads only | 29 (round 1 findings 1 to 14; round 2 findings 1 to 3 and 5 to 11; review findings 13, 14, 20, 21, 22) |
| Both | 1 (finding 3 here is round 2 finding 4) |

New `wrong` findings: 0. New findings of any severity: 2, both minor, one `misleading` and one `imprecise`.

How the three sit against the earlier reads:

- Finding 1 (`l14` `screens[10]` `test-4`): no earlier read flagged the line. Its facts are true, which is how a sweep that asks only "does some coding reach test 4" passes it; the defect is that what reaches it has the total right already.
- Finding 2 (`l15` `screens[5]` `test-3`): the line was written by round 1's fix pass (round 1 finding 4), on the basis "the set cleared between cases only first fails at test-3". That coding does land there, and round 2 confirmed the landing. Neither read asked how natural it is, nor tried the count-of-new-tickers coding, which also lands there and which the line misdescribes.
- Finding 3: round 2's finding 4, marked "not applied" in its fix pass because a concept fix may not add a test. It is still open at `e69cac72` and was not in `docs/BACKLOG-INBOX.md`; it is there now.
- Every line the two fix passes moved or rewrote lands on its test in this sweep: `l13` `screens[3]` `test-5`, `screens[5]` `test-1` and `test-2`; `l14` `screens[4]` `test-2`, `screens[5]` `test-5`; `l15` `screens[4]` `test-6`, `screens[9]` `test-3`; `l16` `screens[3]` `test-6`, `screens[5]` `test-1`; homework `items[0]` `test-2`, `items[2]` `test-1`. Round 2's reworded sentences (48% and the floor, E first for 1,363, "not compared", the ranged summary formula) recompute here.
- Nothing an earlier read fixed was found wrong again.

## Inbox

Written to `docs/BACKLOG-INBOX.md` under "Raised later (audit contests):".

- `l13` problem C needs a twelfth hidden test, `can_ship([5, 5], 3, 4)` expecting False, so the solution's `w > cap` guard is required (finding 3; open since round 2).
- A `test-N` line can be true and reachable and still not fit what reaches it. A check that a committed submission reaches test N (item 1028) would pass both new findings here; the committed submission would also need its returned value compared with what the line says.

## Fix pass

Opus fixer, on `92870c42`. Each line was checked by submitting natural codings of the mistakes it names under the page's own harness (Pyodide 0.27.7, `tools/code-runner.mjs`); results in the table. The codings are in the concepts script as the `fix-` variants, and each new line has `mutants` entries, so `grade-all.mjs --code` now fails if a coding stops landing on its test.

1. `l14` `screens[10]` `test-4`: **fixed differently**. Basis: test 4's answer is `(0, ['A'])`, and seven codings of two mistakes all fail first on test 4 with the total 0 already right and the names wrong. A best total started at 0 with a strict `>` never keeps an order worth 0, so it returns `(0, None)` or `(0, [])` (four codings). Dropping the problems that cannot fit leaves only the empty order, `(0, [])` (three codings). The auditor's text covers the first mistake only, so the line names both. New line: "Test 4's only problem cannot finish in 5 minutes, so it scores 0, but the order still names it: `(0, ['A'])`. Start the best total below 0, so an order worth 0 is still kept. Keep the problems that cannot fit in every order you try." Mutants: the zero start and the filter, both test 4.
2. `l15` `screens[5]` `test-3`: **fixed**. Basis: each case's answer is its own count of distinct tickers, so test 3 is 1, 1 and 2. Two mistakes land there. Counting only tickers new to the call gives `[1, 0, 1]` (three codings, plus the auditor's `t3-increments-per-call`). Emptying the set between cases but not before a call's first case gives `[2, 1, 2]` (three codings, plus the auditor's two). The old line fitted the second only. New line, the auditor's with its second sentence made to name the first mistake: "Test 3's cases are AAA, then AAA, then BBB AAA, so the answers are 1, 1 and 2. A ticker counts again in a later case: count each case's distinct tickers, not just the new ones. Start every case, the first included, with an empty set." Mutants: one of each, both test 3.
3. `l13` `screens[5]` tests: **fixed**. Basis: an order of 5 fits no load of a van of 4, so `can_ship([5, 5], 3, 4)` is False whatever `k` is; the greedy without the guard counts 3 days and returns True. Added as test 12, so no `test-N` line is renumbered; the model solution passes it, the starter still fails (test 1), and four guard-free codings pass tests 1 to 11 and fail first on test 12. `how` now says 12 hidden tests and adds "Test 12 has two orders heavier than the van and three days." New `test-12`: "Test 12 has two orders of 5, a van of 4 and three days. Counting days gives 3, but no day can carry an order of 5. Return False as soon as an order is heavier than the van." Mutant: the plain greedy, test 12. `can_ship` is in no homework or review file, so there is no other copy.

| Widget | Coding | First failing test | Returned there |
| --- | --- | --- | --- |
| l14 s10 | best total 0, names `None` | 4 | `(0, None)` |
| l14 s10 | best total 0, names `[]` | 4 | `(0, [])` |
| l14 s10 | best kept as a tuple `(0, [])` | 4 | `(0, [])` |
| l14 s10 | keep only orders worth more than 0 | 4 | `(0, [])` |
| l14 s10 | filter inside `permutations` | 4 | `(0, [])` |
| l14 s10 | filter the list first | 4 | `(0, [])` |
| l14 s10 | return `(0, [])` when nothing fits | 4 | `(0, [])` |
| l14 s10 | late problem scores its floor (other mistake) | 2 | `(3550.0, ...)` |
| l15 s5 | new tickers, before and after | 3 | `[1, 0, 1]` |
| l15 s5 | new tickers, counted when not seen | 3 | `[1, 0, 1]` |
| l15 s5 | new tickers, set difference | 3 | `[1, 0, 1]` |
| l15 s5 | outside set cleared if case > 0 | 3 | `[2, 1, 2]` |
| l15 s5 | outside set cleared after all but the last case | 3 | `[2, 1, 2]` |
| l15 s5 | outside set replaced after all but the last case | 3 | `[2, 1, 2]` |
| l15 s5 | one set per call, never emptied (other mistake) | 2 | `[2, 3]` |
| l13 s5 | plain greedy, no guard | 12 | `True` |
| l13 s5 | days counted at the ends, no guard | 12 | `True` |
| l13 s5 | new day starts with the order, no guard | 12 | `True` |
| l13 s5 | early exit on days, no guard | 12 | `True` |

Concepts script: only the checks that encoded the old defects changed, as its docstring says. The three `FINDING` checks now test the fixed content. Five sweep labels moved with the new lines: the two unguarded greedies now land on test 12 (`pyodide` recorded as `test-12`), `t3-increments-per-call` is now test 3's named mistake, and the two codings that never empty the set between cases are test 2's mistake, not test 3's. Twelve `fix-` codings were added.

Gates: validator 0 errors (4,606 warnings, unchanged); voice scan 35 on the three lessons 0 and 0; `contests-L4-concepts-r3.py` 356 checks, 0 failing, exit 0; number scripts `--only contests` 5 of 5 passed; `grade-all.mjs --code --file` on each lesson 0 failures (mutants included); playthrough of l13, l14 and l15 green desktop and `--mobile`.

## Fix-pass read

Fresh reader, blind to this file until the rows below were written. Diff read: `git show 51c05b3e -- app/content/courses`. Script: `docs/reports/contests-L4-fixread-r3.py <pkgs> [scratch]`, exit 0 (8 brute-force checks independent of the model solutions, then 19 submissions through `app/tools/code-runner.mjs` under Pyodide 0.27.7). `grade-all.mjs --code --file` on l13, l14 and l15: 11 Python widgets, 0 failures (so each `mutants` entry first fails the test it names).

| # | file | JSON path | claim | verdict | basis |
|---|------|-----------|-------|---------|-------|
| 1 | l13-virtual-contest | screens[5].widget.tests[11] | `can_ship([5, 5], 3, 4)` is False | correct | Brute force over every split of [5, 5] into at most 3 contiguous days: no day holds a 5 at capacity 4. Solution passes all 12; starter fails test 1. |
| 2 | l13-virtual-contest | screens[5].widget.how | "Check runs 12 hidden tests" | correct | `tests` has 12 entries; the listed kinds (example, `can_ship` alone, k = 1, k = n, one order, equal weights) match tests 1 to 8. |
| 3 | l13-virtual-contest | screens[5].widget.how | "Test 12 has two orders heavier than the van and three days." | correct | Weights 5 and 5, cap 4, k = 3. |
| 4 | l13-virtual-contest | screens[5].feedback.byKey.test-12, sentence 1 | Two orders of 5, a van of 4, three days | correct | Reads off tests[11]. |
| 5 | l13-virtual-contest | same, sentence 2 | "Counting days gives 3, but no day can carry an order of 5." | correct | Guard-free greedy by hand and in the script: day 1 empty, days 2 and 3 take one order each, 3 <= 3 gives True. 5 > 4, so no feasible day. |
| 6 | l13-virtual-contest | same, sentence 3 | "Return False as soon as an order is heavier than the van." | correct | An order above the capacity makes every schedule infeasible, so the early return is exact. Codings A (else branch starts the day with w), B (add, then test overflow) and C (early exit once days pass k) all pass tests 1 to 11 and first fail test 12 with True. Contrast D (days counted from 0) first fails test 4, whose line gives the same repair. |
| 7 | l13-virtual-contest | screens[5].widget.mutants[0] | No `w > cap` guard: day count 3, returns True, first fails test 12 | correct | grade-all `--code` 0 failures; same result as coding A to C. Test 4 does not catch it because [5] at k = 1 counts 2 days. |
| 8 | l14-which-first | screens[10].feedback.byKey.test-4, sentence 1 | The only problem cannot finish in 5 minutes, scores 0, and the answer is `(0, ['A'])` | correct | Problem A needs 10 minutes; the prose says a late finish scores 0; brute force over orders gives (0, ['A']). Consistent with test 2, which also names unsolved problems. |
| 9 | l14-which-first | same, sentence 2 | "Start the best total below 0, so an order worth 0 is still kept." | correct | Totals are sums of non-negative scores, so any start below 0 with a strict `>` keeps the first (alphabetically first) order. Codings A (start 0, names None) and B (start 0, names []) first fail test 4 with (0, None) and (0, []). Coding E (start -1, float total) passes all six. |
| 10 | l14-which-first | same, sentence 3 | "Keep the problems that cannot fit in every order you try." | correct | Coding C (filter `p[2] <= minutes` before permuting) first fails test 4 with (0, []); the instruction repairs it. Contrast D (names only solved problems) first fails test 2, so it never reaches this line. Wording note, not a finding: the sentence can be parsed two ways. |
| 11 | l14-which-first | screens[10].widget.mutants[0] | Start 0 with strict `>` returns (0, None), first fails test 4 | correct | grade-all `--code`; same as coding A. |
| 12 | l14-which-first | screens[10].widget.mutants[1] | Dropping the problem that cannot fit returns (0, []), first fails test 4 | correct | grade-all `--code`; same as coding C. |
| 13 | l15-debugging-under-time | screens[5].feedback.byKey.test-3, sentence 1 | Cases AAA, AAA, BBB AAA; answers 1, 1 and 2 | correct | Test input `3\n1\nAAA\n1\nAAA\n2\nBBB AAA\n`; independent per-case set count gives [1, 1, 2]. |
| 14 | l15-debugging-under-time | same, sentence 2 | "A ticker counts again in a later case: count each case's distinct tickers, not just the new ones." | correct | The problem asks for distinct tickers per case. Coding A (one set per call, counts tickers not seen before) passes tests 1 and 2 and first fails test 3 with [1, 0, 1]. |
| 15 | l15-debugging-under-time | same, sentence 3 | "Start every case, the first included, with an empty set." | correct | Hidden tests share one module state. Codings B (global set emptied between cases only) and C (cleared at the top of every case but the first) pass tests 1 and 2 and first fail test 3 with [2, 1, 2], from CCC left by test 2. Contrast D (one set per call, never emptied) first fails test 2. |
| 16 | l15-debugging-under-time | screens[5].widget.mutants[0] | Counts only tickers new to the call: [1, 0, 1], first fails test 3 | correct | grade-all `--code`; same as coding A. |
| 17 | l15-debugging-under-time | screens[5].widget.mutants[1] | First case keeps tickers from an earlier call: [2, 1, 2], first fails test 3 | correct | grade-all `--code`; same as coding C. |

Counts: 17 rows; correct 17, wrong 0, imprecise 0, misleading 0, unverified 0.

Fixes: none needed. Optional wording only for row 10, if the line is touched again: `Do not drop a problem that cannot fit: every order still names it.`

Voice: all new sentences under 35 words, no em-dashes or exclamation marks.

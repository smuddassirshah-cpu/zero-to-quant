# Concept audit, round 2 (blind): contests level 4

Auditor: Fable, round 2, blind to round 1, its fix pass, the author reports and the course's git history until the ledger and findings below were committed.
Scope: `app/content/courses/contests/` files `l13-virtual-contest.json`, `l14-which-first.json`, `l15-debugging-under-time.json`, `l16-upsolving.json`, `review-4.json`, `homework-4.json`. Stage 2, full ledger. Paths count `screens[i]` and `items[i]` from 0.
Ledger: `docs/reports/audit-contests-4-r2-ledger.md` (251 rows: correct 232, wrong 2, imprecise 9, misleading 1, unverified 7).
Script: `docs/reports/contests-L4-concepts-r2.py` (255 checks; exits 1 while findings 1 to 8 stand; no other check fails).

Summary: 11 findings. Wrong 2 (both minor), imprecise 8 (all minor), misleading 1 (minor). No serious finding: every graded key, every worked figure and every code solution is right. All 16 code solutions pass their hidden tests natively and in Pyodide 0.27.7; all 16 starters fail. Of 51 `byKey.test-N` lines, 50 name or imply a mistake and were swept with a real submission (homework `max_profit_k` test-6 names none); 47 land on their own test, 3 do not (findings 1 to 3; finding 1's line is a true description of its test, so it is graded imprecise, not wrong). There are no `byKey.error`, `compile` or C++ widgets in scope.

## Findings

Pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

1. l13-virtual-contest.json | `screens[5].feedback.byKey.test-2` | imprecise | minor | The line explains a `can_ship` that wrongly says 11 ships in 3 days. The prose makes `min_capacity` call `can_ship`, so that mistake makes test 1 return less than 12 and fail first. The line then never shows for the mistake it explains. | Script, FINDING 1: a greedy that drops the overflowing order returns 8 on test 1 (key `test-1`, no line). Test 2 is the first failure only when `min_capacity` does not call `can_ship` (script: `can_ship` left unwritten, own check inside `min_capacity`). Basis: `app/js/engine/widgets/code.js` keys on the first failing row. | Add `"test-1": "Test 1 expects 12. If you got less, check `can_ship` at 11: it needs 4 days (4, then 8 and 2, then 7, then 5 and 3)."` and change `test-2` to `"Test 2 calls `can_ship` alone and asks whether 11 ships in 3 days. Greedily it needs 4 days: 4, then 8 and 2, then 7, then 5 and 3."`

2. l15-debugging-under-time.json | `screens[4].feedback.byKey.test-6` | wrong | minor | The line's advice ("Count only pairs where the first is strictly larger") names the non-strict comparison. Every non-strict comparison fails test 3 first (`[2, 2]`), so this line never shows for it. It shows for other bugs, which the advice does not fit. | Script, FINDING 2: `>=` fails first at test 3. A submission that removes repeated values first passes tests 1 to 5 and fails first at test 6 (returns 1). | `"test-6": "Test 6, `[2, 1, 2, 1]`, has 3 inversions: the first 2 is above both 1s, and the second 2 is above the last 1. Keep repeated values in the list, because each copy makes its own pairs."`

3. l16-upsolving.json | `screens[3].feedback.byKey.test-6` | wrong | minor | "Do not stop at the first match" names a mistake that fails test 1, not test 6: the example has two good second cuts, so stopping at the first returns 1 against 2. | Script, FINDING 3. The mistake that does fail first at test 6 is an early exit once the prefix passes $2S/3$, which assumes non-negative values (script: passes tests 1 to 5, returns 0 on test 6). | `"test-6": "Test 6 has negative values and a total of 0, so prefix sums rise and fall. Scan every day; do not stop once the prefix passes $2S/3$."`

4. l13-virtual-contest.json | `screens[5].widget.tests`, `.how`, `feedback.byKey.test-4` | imprecise | minor | The `how` line says test 4 has an order heavier than the van, and the solution carries a `w > cap` guard. No hidden test needs the guard: the standard greedy without it passes all 11 tests, because on test 4 the day count is already 2 against 1. A learner can leave out a line the solution needs. | Script, FINDING 4: unguarded greedy passes 11 of 11; `can_ship([5, 5], 3, 4)` returns True for it and False for the solution. The `test-4` line still shows for a greedy that carries an overweight order alone (swept, lands on test 4). | Append test 12 `{"call": "can_ship([5, 5], 3, 4)", "expect": "False", "compare": "equal"}`. In `how`, change "11 hidden tests" to "12 hidden tests" and add before the last sentence: "Test 12 has two orders heavier than the van and three days." Add `"test-12": "Test 12 has two orders of 5, a van of 4 and three days. A new day does not help: an order heavier than the van never ships, so return False."`

5. l14-which-first.json | `screens[3].explain.text` | imprecise | minor | "The floor of 30% matters only for a problem solved very late." Under the stated rule the floor is reached by time alone at minute 175, after the two-hour round ends. Inside the round it binds only with rejections, and then not only late: the next screen's test 2 is such a case. | Script, FINDING 5: $v - 120v/250 = 0.52v$; A at minute 60 with five rejections is 130, below 150. | `"Thirty-five minutes cost 140 points and the rejection 50, so B scores 810. In a two-hour round, time alone leaves 52% of the value. So the floor of 30% is reached only when rejections add to the time cost."`

6. l14-which-first.json | `screens[6].explain.text` (last sentence) | misleading | minor | "Leave D the moment it is solved, and the same model puts the best cap later, near 45 minutes." The figure is right (cap 45.3, about 1,229 points), but it keeps D first. Once you may leave a solved problem the order matters, and the same model prefers E first by a wide margin. The screen so teaches the opposite of the lesson's own rate rule (E pays about 53 points per expected minute, D 20). | Script, FINDING 6: with solving times exponential with means 50 and 15, D first with the best cap expects 1,229 and E first then D expects 1,363 (quadrature, and Monte Carlo of 200,000 rounds). For a fixed split the order does not matter, so the graded target (34.84, about 1,152) stands. | `"The best fixed split is about 35 minutes on D, for about 1,152 points. All D gives 699 and all E 785. If you may leave a problem once it is solved, start with E, the better rate, and give D the rest: about 1,363 expected."`

7. l14-which-first.json | `screens[11].feedback.correct`, `screens[11].hints[2].text` | imprecise | minor | Both say "quote, hedge, reconcile", but the three tasks need 50 minutes and the close is in 30. The explain says only the quote and the hedge fit. | Script, FINDING 7: $5 + 25 + 20 = 50$. | `feedback.correct`: `"Quote first, then the hedge; the break waits until after the close."` `hints[2].text`: `"Quote £600, hedge £480, reconcile £100 a minute: quote first, then the hedge."`

8. l16-upsolving.json | `summary.formula.tex` | imprecise | minor | The sum has no range for the cuts. With a zero total, $P_n = 2S/3$ as well, so read over every $j$ it overcounts: 10 for five zeros against 6. The lesson's own key test is all zeros. | Script, FINDING 8; the ranged form matches the solution on 2,000 random lists. Basis: cuts satisfy $1 \le i < j \le n - 1$ (screens[3].prose). | `"tex": "\\text{ways} = \\sum_{j \\le n-1:\\, P_j = 2S/3} \\#\\{\\, 1 \\le i < j : P_i = S/3 \\,\\}"`

9. l15-debugging-under-time.json | `screens[6].explain.text`, `screens[6].hints[2].text`, `screens[8].prose` (code comment) | imprecise | minor | "Standard error is ... ignored by the judge." It is not compared, but writing it still costs run time. A learner who leaves heavy debug output on standard error can turn an accepted solution into a time limit exceeded. | Basis: the verdict compares standard output only (testlib checkers), while the time limit covers the whole run; a standard caution in competitive programming guides. | `explain.text`: `"The judge compared lines 2 to 5 with the expected 2 and 1, and the debug lines broke it. Standard error is shown to you and not compared by the judge. Writing it still takes run time, so remove heavy debug output before submitting."` `hints[2].text`: `"Write debug lines to `sys.stderr`, which the judge does not compare, or delete them before submitting."` In `screens[8].prose` change the comment to `# not compared`.

10. l15-debugging-under-time.json | `screens[2].widget`, `screens[2].explain.text` | imprecise | minor | The prompt asks for cheapest first, and the explain says "Each step is cheaper than the next". That is not established for steps 2 and 3: a glance at the types and the recursion depth costs no more than running four hand cases. A learner who puts the limits check second has followed the stated rule and is marked wrong. | Basis: the item gives no costs; the only cost claims in the lesson are for rereading (a minute) and the stress test (a brute force and a generator), in `hints[1]`. | Add `"same": [["s2", "s3"]]` to the widget. `explain.text`: `"Rereading is the cheapest step and the stress test the dearest; hand cases and the limits check sit between, in either order. Rereading finds misreadings, hand cases find off-by-ones, and limits find overflow. The stress test, from lesson 4, finds wrong answers that small random cases can show."`

11. l15-debugging-under-time.json | `screens[6].prose` | imprecise | minor | The prose says the prints were added "to see what was happening", so the bug of the previous screen is still in. The console then shows what the fixed program prints: case 2 as `seen = {'CCC'}` and 1. The buggy program prints three names and 3. The run also has two cases, while the previous screen says the judged example has $t = 1$. | Script: the starter of `screens[5]` returns `[2, 3]` on that input. | `"prose": "You fixed the bug but left two debug prints inside the loop. A run on your own two-case file looks right, yet the judge's verdict is worse than before."`

### Unverified rows (no verdict of correct given; hedges offered)

- Ratings "about 800 / 1100 / 1300 / 1500" (l13), "about 1600" (l16 `screens[3]`), "about 1300 / 1500 / 1600" (homework). Labelled "by our estimate" once, in l13 `screens[3]`. Suggested: l16 `screens[3].prose` starts `"Problem D, about 1600 by our estimate."`
- l16 `screens[7].options[hard].why` and `hints`, homework rubric: "Practise about 100 to 200 above your rating." A common rule of thumb, not in the curriculum. The 300 rule is flagged as an assumption; this one is not. Suggested `why`: `"You chose problems 750 above you. This lesson's rule of thumb is practice about 100 to 200 above your rating."`
- l16 `screens[10]`, `screens[11]`, homework `items[5]`: where a rating counts in hiring. The attribution to `docs/curriculum.md` is exact (section 2.4 and the track table); the hiring facts themselves have no source.
- l16 `screens[11].options[cut].why`: "Write-ups show how you think, which interviewers do read about." Suggested: `"Write-ups show how you think. Keep them."`
- l14 `screens[11].explain.text`: "An interview with three questions in an hour works the same way." Interview scores do not decay by a known rule. Suggested last sentence: `"In an interview with three questions in an hour, the same habit helps: bank the quick one, then go deep."`

### Checked and found right (the points the brief singled out)

- Scoring rules are tied to their format: the decay rule is called "our rule" and "this course's illustration" (it is the Codeforces rule for a two-hour round); the 20-minute penalty is "ICPC style ... (our illustration)". No rule is stated as universal.
- The exchange argument in l14 `screens[9]` proves what it claims: an adjacent swap leaves every other finish time unchanged, and the difference is $(v_j t_i - v_i t_j)/250$ for every adjacent pair of every order (script). Its hypothesis (no score at its floor) is stated; the deadline exception is taught by `screens[10]` test 2.
- The keyed order A B C D is the unique best of the 24 orders up to the A and B tie the widget allows (script).
- Page facts: no content contradicts the 3,000 recursion limit (homework states it), the 32-bit `long` of wasm32 (the content uses `long long`), or the 5 s per-test limit (the "1 s" on statement cards belongs to the fictional judge). The claim that this app's Pyodide ran a million frames holds in Pyodide 0.27.7 under node.
- All tests of a code widget run in one namespace, in order (`code.js` function mode). The l15 `screens[5]` lines about state left by an earlier call rely on this and are right.

## Gates

- `node tools/validate.mjs`: 0 errors, 4539 warnings. `content/manifest.json` unchanged.
- `node tools/run-number-scripts.mjs --only contests-L4`: 1 script, 1 passed, exit 0.
- `node tools/grade-all.mjs --file <path> --local-cdn <pkgs>` on each of the six files: 0 failures, exit 0 each.
- `docs/reports/contests-L4-concepts-r2.py`: 255 checks, 247 hold, 8 print as FINDING 1 to 8, 0 unexpected failures, exit 1 (it will exit 0 once findings 1 to 8 are fixed; findings 9 to 11 are judgements with no executable check).
- Solutions in Pyodide 0.27.7 (CPython 3.12.7, wasm32, node): all 16 pass; slowest case 0.78 s (`widest_gap`), against the 5 s limit.
- Native against page: the sweep ran on CPython 3.13 with the page's semantics (one namespace, recursion limit 3,000, 5 s per case, first failing row is the key). Native is faster than Pyodide, so each of the 7 "times out" mistakes was required to pass 5 s natively. Integers are unbounded in both; no check depends on pointer size or on float formatting. Browser stack limits differ from node only for recursion through C code, which no solution uses.
- No content changed, so no playthrough was run.

## Overlap with earlier reads

Filled after the blind commit 63ce5a72 ("WIP: contests L4 r2 ledger and findings"), from `docs/reviews/audit-contests-4.md` (round 1: 14 findings, its fix pass and its fix-pass read) and `docs/reviews/review-contests-3-4.md` (level 4 conceptual findings 13, 14, 20, 21 and 22). All of those were fixed before this read, so this audit read the corrected text.

| Count | Conceptual findings |
| --- | --- |
| This audit only | 11 (findings 1 to 11) |
| Earlier reads only | 19 (round 1 findings 1 to 14; review findings 13, 14, 20, 21, 22) |
| Both | 0 |

New `wrong` findings, found by no earlier read: 2 (findings 2 and 3, both minor, both a `byKey` line that cannot show for the mistake it names). Round 1 swept the same two lines and passed them as "the line only describes the test and is true"; each also gives advice, and that advice fits only a mistake that fails an earlier test.

How the 11 sit against the earlier reads:

- Finding 6 is in text the round 1 fix pass wrote. Round 1's finding 9 proposed the sentence "the same model puts the best cap later, near 45 minutes", and the fix-pass read passed it. The figure is right; neither read asked whether D should come first once a solved problem can be left.
- Finding 7 is on the desk screen that round 1's finding 11 repaired (it added the decay). The repair's explain says only two tasks fit; the feedback and hint were left saying three.
- Finding 4 is next to round 1's inbox bullet on problem C (the test allows 0 `can_ship` calls), which this audit also met; the missing guard test is new.
- Findings 1, 5, 8, 9, 10 and 11 touch text no earlier read flagged.
- Nothing an earlier read fixed was found wrong again. The lines round 1 moved (l13 `test-5`, l14 `test-2` and `test-5`, l15 `test-3`, l16 `test-1`, homework `test-2` and `test-1`) all land on their tests in this sweep.
- Unverified rows: round 1 listed 15 and rewrote all of them. Of this audit's 7, the rating estimates and the hiring facts behind the curriculum repeat round 1's classes; "100 to 200 above", the write-ups line and the interview sentence in l14 are new.

## Inbox

- Code widget: `byKey` keys on the test number only. A `test-1` line shows for every first-test failure, including a submission that returns `None`; a line cannot be tied to the returned value (for example 7 on l13 problem D).
- Code widget: a test cannot require that one learner function calls another. l13 problem C counts `can_ship` calls with an upper bound, so a `min_capacity` with its own check passes with 0 calls, against the prose.
- `tools/grade-all.mjs` skips code widgets, and no node tool runs a named wrong submission against a widget's hidden tests. A `--submission <file> --expect-key test-N` mode would let authors commit one mistake per `byKey` line (three lines in this level miss their test).
- Validator: nothing checks that a `byKey.test-N` line has a committed submission that reaches it.

## Fix pass

Fixer: Opus, round 2. Scripts changed where they pinned text: `docs/reports/contests-L4-concepts-r2.py` (findings 1 to 3 now sweep the new lines; findings 5 to 8 now read the content; finding 4 recorded as not applied), `docs/reports/contests-L4-concepts.py` (l13 C key list gains `test-1`, with its submission), `docs/reports/contests-L4-numbers.py` (l14 `screens[6]` figure 1,363 in closed form; l13 `test-1` figures). No graded key, slip, hidden test, solution or starter changed.

| # | Status | Basis (the fixer's own) |
| --- | --- | --- |
| 1 | fixed | A `can_ship` that drops the overflowing order says 11 ships in 3 days; called by `min_capacity` it returns 8 on test 1, and with `min_capacity` running its own check it fails first at test 2 (both run). Greedy at 11 by hand: [4], [8, 2], [7], [5, 3], four days. New `test-1` line is conditional ("If you got less") so it stays true for other first-test failures. |
| 2 | fixed | `>=` fails first at test 3 (`[2, 2]` gives 1); removing repeated values passes tests 1 to 5 and gives 1 on test 6 (run). Pairs of `[2, 1, 2, 1]` counted by hand: (0,1), (0,3), (2,3), three. Wording "larger than" in place of "above". |
| 3 | fixed | Stopping at the first good second cut gives 1 on the example (expected 2), so it fails test 1; breaking once the prefix exceeds $2S/3$ passes tests 1 to 5 and gives 0 on test 6, `[1, -1, 1, -1, 1, -1]`, whose first prefix is 1 > 0 (run, traced by hand). |
| 4 | not applied | True: the unguarded greedy passes all 11 tests and returns True for `can_ship([5, 5], 3, 4)`. The fix needs a new hidden test, which a concept fix may not add; the text that stands is true (test 4 does have an order heavier than the van). Raised in the inbox below. |
| 5 | fixed differently | In a two-hour round time alone costs at most $120/250 = 48\%$ (also $4 \cdot 120 = 480$ of 1,000), so the 30% floor needs rejections; A at minute 120 with three rejections, 110 < 150, is the next screen's test 2. Wording: "time alone takes at most 48% of a problem's value", which reads more directly than "leaves 52%". |
| 6 | fixed | Recomputed by scipy quadrature and by 400,000-round Monte Carlo (own seed): D first with the best cap (45.3) 1,228.8 and 1,227.8; E first, leaving it when solved, 1,362.9 and 1,361.8; a cap on E never helps (best cap is the whole hour). Closed form for E first, $1800(1 - e^{-4}) - 1000e^{-1.2}\frac{10}{7}(1 - e^{-2.8}) = 1{,}362.9$. Applied the auditor's sentence, which these figures support. |
| 7 | fixed | Quote 5 and hedge 25 fill the 30 minutes; the break's 20 does not fit ($5 + 25 + 20 = 50$), as the screen's own explain says. |
| 8 | fixed | Cuts are $1 \le i < j \le n - 1$ (`screens[3].prose`); on five zeros the ranged sum is 1 + 2 + 3 = 6 and the unranged one 10, by hand and by the script on 2,000 random lists. |
| 9 | fixed | Standard error is not compared but is written during the timed run; the claim is kept as advice about heavy output, not a figure. Explain, `hints[2]` and the `screens[8]` comment now say "not compared". |
| 10 | fixed differently | Adding `same` would change a graded key, so the key stays and the stated rule now fixes the order: the prose says the two steps just taken (reread on screen 0, hand cases on screen 1) come first, and the explain gives the cost reason only for first and last. `hints[2]`, `feedback.correct` and `generic` no longer say "cheapest first". |
| 11 | fixed | The starter of `screens[5]` prints 2 and 3 on the two-case input; the console shows 2 and 1, the fixed program. Prose now says the bug is fixed and the file is the learner's own two-case file (renamed `two_cases.txt`); the explain no longer claims the judge compared that run. |

Unverified rows:

| Row | Status | Basis |
| --- | --- | --- |
| l13 `screens[3]` rating "about 800 ... by our estimate" | left | Labelled as an estimate, and l13's quiz says every code screen gives "our estimate"; an estimate stated as one is established as such. |
| l16 `screens[3]` "about 1600" | fixed | Prose now "about 1600 by our estimate"; homework's three ratings likewise. |
| l16 `screens[7]` "100 to 200 above" | fixed | `options[hard].why` and `hints[1]` now call it "this lesson's rule of thumb". |
| homework `items[6]` rubric "100 to 200 above" | left | The rubric grades the plan against the rule l16 now states as its rule of thumb; it asserts nothing beyond that. |
| l16 `screens[10]` hiring facts | left | Every sentence is attributed to the curriculum ("The curriculum sets ... It treats ... it counts"), and the attribution is exact; the screen does not assert the facts in its own voice. |
| l16 `screens[11]` write-ups | fixed | Now "Write-ups show how you think, and an interviewer may ask about them": a possibility, not a claim about what interviewers read. |
| l14 `screens[11]` interview sentence | fixed | Now a stated condition: "If an interview sets three questions in an hour, the same habit helps". |

Sweep: 52 `byKey.test-N` lines in the six files (51 plus the new l13 `test-1`). 51 run as real submissions in `contests-L4-concepts-r2.py`, page semantics (one namespace, recursion limit 3,000, 5 s, first failing row); all 51 land on their test after the fix. Homework `max_profit_k` `test-6` names no mistake and its figure (2 + 3 + 4 = 9) is checked. Lines rewritten: 3 (l13 `test-2`, l15 `test-6`, l16 `test-6`), 1 added (l13 `test-1`).

Gates: validator 0 errors (4,541 warnings, two new soft long-sentence ones in l14 `screens[6]` and l15 `screens[2]`; manifest unchanged); `contests-L4-concepts-r2.py` 257 of 257, exit 0; `contests-L4-concepts.py --pyodide` 277 checks, 0 failing; `contests-L4-fixread.py` 0 failures; `run-number-scripts --only contests-L4` 1 passed; `grade-all --file` 0 failures on each of the five changed files; voice scan 35: 0 and 0; playthrough of l13, l14, l15, l16 and homework-4, desktop and mobile, all passed.

Inbox: l13 C needs a hidden test such as `can_ship([5, 5], 3, 4)` expecting False (finding 4), so the solution's `w > cap` guard is required; a content agent or engine pass that may add tests should take it.

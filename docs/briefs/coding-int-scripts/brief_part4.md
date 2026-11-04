
## Level 4

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `coding-int` (topic 3.5), level 4 ("Under the clock"): lessons `l15-reading-an-assessment`, `l16-edge-cases-first`, `l17-two-in-sixty`, `l18-talking-while-coding`, `l19-a-live-round`, plus `review-4.json` and `homework-4.json`, in `app/content/courses/coding-int/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids of `course.json` exactly (`ci-timed` on l15 to l19; l19 also `ci-design`). Use £ for money. Scripts: `l4.py` (every problem of this level; C++ checks; timings), `l_extra.py` (the C++ `longest_consecutive`), `harness.py`, `numbers_check.py`, `numbers_check3.py`, `numbers_check4.py`.

Level promise. The learner has the patterns and the designs; now the clock. This level teaches how an online assessment is read and planned, how to find the edge cases before writing a line, how to use 60 minutes on two problems, how to talk while coding, and how a 45-minute live round with follow-ups runs. Formats are reported, not official: say "reported" and keep firm names out ("a bank's online assessment", "a market maker's developer screen", "a developer role at a trading firm").

**Engine features (pass C).**
- **E8 (drill library)**: l17 screen 8 sends the learner to `#drill` to start a two-drill, 60-minute session with filters pattern `prefix-sums` or `hashing`, difficulty 3 to 4, language Python or C++ (the C++ drills are `language: "cpp"`); l19 screen 9 sends the learner to a single-drill stopwatch on an `intervals` drill, difficulty 4, language Python or C++. The drill files belong to the drill packs (authored separately); this level names the filters only. Use the pattern names the E8 filter lists show; if the built filter uses other slugs, use those and tell the report.
- **E3 (item banks in exams)**: l15 screen 10 and l17 screen 10 link to `#exam/mock-oa-code`, a mock whose paper draws from the bank by `draw` so a resat is fresh. The mock is authored in a separate task; this level only links to it, and tags its own review and homework items (`oa-triage`, `edge-case-list`, `complexity-read`, `timed-plan`) so the bank families can use them.
- **E11 (follow-up parts)**: homework items 1 and 2, each a live round with follow-ups revealed in turn and graded per part. A part may be a `code` widget (the part's hidden tests are the whole item's cumulative tests up to that part), a `choice` or a `numeric`.
- **`timed` on a level review (existing, built)**: `review-4.json` carries `"timed": { "seconds": 600, "lockAtZero": false }` so the clock is a guide, shown with a live score, for ten items. Not allowed on homework.
- Existing: `code` Python and C++ (with `testkit` and per-case `defines` for l16, a `postlude` driver for l19), `table`, `order`, `choice`, `multi`, `numeric`, `longform`, canvases `console`, `table`, `array`, `number-line` (intervals for the calendar).
- E14 is not needed in level 4.

**Builds on (by id) and what is new.**

| Lesson | Builds on | New over those |
| --- | --- | --- |
| l15-reading-an-assessment | `contests` l14-which-first (order by points and difficulty), `contests` l2-limits-to-complexity (constraints to complexity), `contests` l13-virtual-contest, `recruiting` l9 (online assessments) | Partial credit as a choice per problem (full, partial or skip, solved by dynamic programming), the greedy trap with numbers, test groups by input size. The constraints table is cited, not re-taught. |
| l16-edge-cases-first | `contests` l4-stress-testing, `contests` l15-debugging-under-time, `pytest` l5-empty-one-many, `pytest` l10-test-first, `cpp` l18-unit-tests | Writing inputs that catch planted bugs (a mutation check), edge-case families for arrays, strings, intervals and numbers, and the same game in C++ with `testkit` and `defines`. |
| l17-two-in-sixty | `contests` l13-virtual-contest, `contests` l16-upsolving, `ds` l7-prefix-sums, `ds` l2-constant-time-lookup | Splitting 60 minutes across two problems, a brute force that earns partial credit, the E8 session, two classic hash patterns (prefix-sum counts, a set of starts). |
| l18-talking-while-coding | `recruiting` l12-reasoning-aloud, `mm-games` l12-thinking-aloud | Narrating a plan and its trade-offs in comments before code, naming complexity out loud, handling a constraint ("no division") while talking. |
| l19-a-live-round | `ci-patterns` l1-merging-intervals (this course), `ds` l15-search-trees, `cpp` l15-maps | A 45-minute live problem in three stages: base, a changed rule, a new operation, with the sorted-list design and its sweep replacement. |

### l15-reading-an-assessment (13 min; tags `oa-triage`, `partial-credit`, `timed-plan`)

Objective: Triage an assessment's problems and plan the minutes before writing code. Method stated after use: in the first five minutes read every statement, note the constraints and the point values, estimate full and partial minutes, then pick for each problem full, partial or skip so that the points are most for the minutes you have. Reported formats to quote with the word "reported": an online assessment of two algorithm problems in 60 minutes at a bank, three problems in 90 minutes at a developer role; points often depend on how many hidden test groups pass.

The running assessment (prices of time in minutes): three problems, each with full points and the minutes you estimate for full marks, and partial points (the small test groups) and the minutes for that: P1 `(40, 20, 12, 6)`, P2 `(60, 35, 25, 12)`, P3 `(90, 50, 30, 18)`. The assessment lasts 65 minutes and reading takes 3, so the budget is 62.

Screens (10):
1. Hook `problem`, `console` showing the three problems; `choice`: which has the most points per minute? P1 (40/20 = 2.0; P2 is 1.71; P3 is 1.80).
2. `ladder`, `numeric`: take problems by points per minute, full marks only, within 62 minutes: P1 (20) then P3 (50) is 70, too much, so P2 (35) fits: 55 minutes, 100 points.
3. `ladder`, `table` widget: the learner fills the best plan: P2 partial (12 minutes, 25 points) and P3 full (50 minutes, 90 points) is 62 minutes and 115 points.
4. `problem`, code A, `best_plan`, `pace` 900, difficulty 4 (`best_plan` over `(full_pts, full_min, part_pts, part_min)` lists).
5. `trap`, `choice`: "every problem full or nothing". The learner who allows no partials gets 100; the right answer 115. Name the action in `byKey` ("You ruled out partial credit").
6. `ladder`, `choice`: test groups. A statement lists groups `n <= 1,000`, `n <= 100,000` and `n <= 1,000,000`; which of an `O(n^2)`, an `O(n log n)` and an `O(n)` solution earns which groups (the learner marks a three-by-three table; cite `contests` l2 for the arithmetic).
7. `ladder`, `order`: the first five minutes (read all, mark constraints, rank by points per minute, settle partials, set time boxes, start the surest problem).
8. `generalise` + `derive` (`order` the plan steps).
9. `transfer`, `numeric`: with budget 60 instead of 62, the best plan is 102 (P1 partial, P2 full, P3 partial: 6, 35 and 18 minutes) and the greedy by points per minute still makes 100; computed by the program and by listing the 27 choices.
10. `transfer`, `choice`: the learner picks the plan for a different assessment of two problems in 60 minutes; closing prose links `#exam/mock-oa-code` (E3, a fresh paper each attempt).

Quiz (4): points per minute; a budget after reading; a test group; a partial choice.

**Problem 15.1** `best_plan(problems, budget)`; Python; difficulty 4. Statement: "Each problem is `[full_points, full_minutes, partial_points, partial_minutes]`. For each you choose full, partial or skip. Return the most points obtainable in at most `budget` minutes." Reference (dynamic programming over minutes), starter (returns 0; fails 8 of 10), tests (brute force over all `3^n` choices; the last has 60 problems and budget 600, expected from a memoised recursion):

@@PY:l4:BP_REF@@

@@PY:l4:BP_START@@

@@T:l4:bp@@

The lesson example (`P1` to `P3` at 62) is not in the table; its numbers come from `numbers_check4.py`: best 115 (by the program and by listing 27 choices), greedy 100, and at 60 minutes best 102 and greedy 100.

### l16-edge-cases-first (13 min; tags `edge-case-list`, `test-first`, `mutation-tests`)

Objective: List edge cases and write tests before the solution. Method stated after use: before the code, write the empty, the single, the repeated and the boundary inputs and their expected outputs; run them against a wrong solution to see them fail; only then write the real one. The learner's own lists are marked by planted bugs, not by matching a model list.

The function under test: `longest_run(xs)`, the length of the longest run of equal neighbours in a list of whole numbers (0 for an empty list). Six planted bugs: `m1` forgets the last run, `m2` returns 1 for an empty list, `m3` returns 0 for a single element, `m4` counts non-decreasing runs, `m5` restarts a run at 0 after a break, `m6` compares only with the first value.

Screens (11):
1. Hook `problem`, `multi`: which of `[]`, `[1, 2]`, `[2, 2, 2]`, `[3, 1, 1]`, `[2, 1]` expose bug `m1`? `[2, 2, 2]` and `[3, 1, 1]` (the last run is the longest).
2. `ladder`, `table` widget: the expected outputs of `[]`, `[7]`, `[1, 2]`, `[3, 1, 1]`, `[2, 2, 2]`, `[1, 1, 2, 2, 2]`: 0, 1, 1, 2, 3, 3.
3. `problem`, code A, Python `edge_cases()` returning at most 8 inputs (the hidden harness runs the reference and each planted bug on them), `pace` 480, difficulty 3.
4. `ladder`, `numeric`: how many of the six bugs does `[3, 1, 1]` expose? 3 (`m1`, `m5`, `m6`).
5. `trap`, `choice`: "A thousand random lists" miss `m2`, the empty list, because random lists are rarely empty; the learner who relies on random tests only is wrong. Name the action in `byKey`.
6. `problem`, code B, C++ twin with `testkit`: the learner writes `TEST` blocks with `CHECK`; the hidden postlude defines `longest_run` and, for each case with `defines`, a planted bug; the correct version must pass every test (the learner's expected values must be right), and each bug must make `run_tests()` report a failure.
7. `ladder`, `table` widget: the edge-case families (arrays: empty, one, two equal, all equal, sorted, reverse, negatives; strings: empty, one letter, repeated; intervals: touching, nested, identical; numbers: 0, negative, largest).
8. `generalise` (a checklist in code comments) + `derive` (`order` the test-first steps).
9. `transfer`, `multi`: the three tests worth writing first for `merge_intervals` (`[]`, a touching pair, a nested pair).
10. `transfer`, `numeric`: the smallest number of inputs among ten candidates that exposes all six bugs: 3 (`[]`, `[7]`, `[1, 1, 2, 2, 2]`), found by trying every subset of the ten.
11. `transfer`, `choice`: what to say aloud before writing the tests ("I will start with empty, single, repeated and boundary").

Quiz (4): which input exposes a bug; the expected value of an edge input; why random tests miss; a checklist item.

**Problem 16.1** `edge_cases()`; Python; difficulty 3. Statement: "Return a list of at most 8 inputs (each a list of whole numbers) for `longest_run`. They are run against the correct function and six wrong versions; every wrong version must give a different answer on at least one of your inputs." `prelude` holds the reference and the six planted bugs and the checker `caught(name)` and `well_formed()`; the tests call them:

@@PY:l4:LR_PRELUDE@@

Reference (`edge_cases` returning `[[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2]]`):

@@PY:l4:EC_REF@@

Starter (returns an empty list; fails 6 of 7):

@@PY:l4:EC_START@@

@@T:l4:ec@@

Coverage table (which planted bug each candidate input exposes, computed by running every bug): `[]` m2; `[7]` m1, m3; `[1, 2]` m4; `[3, 1, 1]` m1, m5, m6; `[2, 2, 2]` m1; `[1, 1, 2, 2, 2]` m1, m4, m5, m6; `[1, 1]` m1; `[2, 1]` none; `[1, 2, 2]` m1, m4, m5, m6; `[5, 5, 5, 1]` none. The reference `longest_run` was checked against a brute force over all runs on 2,000 random lists.

**Problem 16.2** the C++ twin of `edge_cases`; difficulty 3. The learner writes tests, not a function. Hidden `prelude` (declaration; the `testkit` provides `TEST`, `CHECK` and `run_tests()`):

```cpp
#include <vector>
#include <algorithm>
int longest_run(const std::vector<int>& xs);
```

Hidden `postlude` (the function and five planted bugs behind `defines`; the correct version is the `#else`):

@@CPP:l4:CPP_POST@@

Starter (one test; it passes the correct version and exposes only `BUG2`):

@@CPP:l4:CPP_LEARNER_START@@

Model solution (passes the correct version; every bug makes at least one test fail):

@@CPP:l4:CPP_LEARNER_SOL@@

Hidden cases (`"testkit": true` on the widget): `{ "call": "run_tests()", "expect": 0 }` with no defines, and for each `n` from 1 to 5 `{ "call": "run_tests() > 0", "expect": true, "defines": { "BUGn": 1 } }`. The starter fails four of the six cases (every bug except `BUG2`). The model solution was compiled with `g++` under `-std=c++20 -O1 -fno-exceptions` against a stand-in `testkit` (`TEST`, `CHECK`, `run_tests`) and passed the correct version and failed each of `BUG1` to `BUG5`. The level agent confirms the real `testkit` behaves the same in the playthrough.

### l17-two-in-sixty (14 min; tags `timed-plan`, `prefix-sum-count`, `hash-set-starts`)

Objective: Solve two medium problems inside 60 minutes, with a plan for partial credit. Method stated after use: 5 minutes to read both, 25 minutes for each problem (brute force first when it earns points, then the fast version), 5 minutes to run tests and edge cases, and a rule that you move on at the box. The pace of a medium is 25 minutes (1,500 seconds) on each code screen of this lesson.

Screens (10):
1. Hook `problem`, `table`: the plan 5 read, 25, 25, 5 test; `numeric`: if the first problem takes 28 minutes, how many minutes are left for the second after reading and testing? 22.
2. `problem`, code A, Python `count_subarrays_sum_k`, `pace` 1500; the starter is a correct quadratic brute force.
3. `ladder`, `numeric`: how many of the 11 tests does the brute force pass? 9 (it stops at the first large case). The prose says partial credit is a score for the small groups.
4. `ladder`, code A in C++ (the same 11 tests; the quadratic starter is correct and fails by time on the first large case: about 11 seconds natively at `n = 200,000`, so the wasm run is slower than the 5 s limit).
5. `trap`, `choice`: polishing the first problem for 40 minutes leaves 15 for the second and 0 for tests; the right call is to submit the partial and move on at the box.
6. `problem`, code B, Python `longest_consecutive` (a set; only start counting at a value whose predecessor is absent), `pace` 1200.
7. `ladder`, `choice`: `set` against sorting: both beat the list scan; sorting is `O(n log n)`, the set is `O(n)` on average.
8. `transfer`, E8: the prose sends the learner to `#drill`: "Start a session: two drills, 60 minutes, filters `prefix-sums` and `hashing`, difficulty 3 to 4." The screen's `choice` asks which split they will set before starting (5, 25, 25, 5 is correct; 0, 30, 30, 0 and 10, 20, 20, 10 are wrong with a `why`). A second, shorter prose line says a C++ learner picks `language: cpp`.
9. `generalise` + `derive` (`order` the minute plan).
10. `transfer`, `choice`: which of two problems to start with given a 60-minute clock and a partial-credit rule; closing prose links `#exam/mock-oa-code` (E3).

Quiz (4): minutes left; partial credit; the box rule; set against sort.

**Problem 17.1** `count_subarrays_sum_k(nums, k)`; Python and C++ twin; difficulty 3. Statement: "Return the number of non-empty contiguous subarrays of `nums` whose sum equals `k`. Values may be negative or zero." Python reference (a dict of prefix-sum counts), starter (correct but quadratic: it passes the nine small cases and is stopped by the clock on the tenth), tests (the tenth is 200,000 zeros, answer `200000 * 200001 / 2 = 20,000,100,000`, the eleventh is `[1, -1]` repeated 50,000 times with `k = 0`, answer 2,500,000,000, by the closed form `sum of (100,000 - L + 1)` over even `L`):

@@PY:l4:CS_REF@@

@@PY:l4:CS_START@@

@@T:l4:cs@@

Both languages use 200,000 zeros in the tenth row (`xs = [0] * 200000`, expected 20,000,100,000), so that the C++ starter fails by time. Python: the quadratic starter takes about 0.15 s at 3,000 values, so about 170 s at 100,000 and longer at 200,000, far past 5 s. C++: the quadratic starter ran for 10.96 s natively at 200,000 (`-O1`); WebAssembly is slower. Both are verified by timing, since the starter is correct and fails only by the clock. The hash-map reference passes all 11 cases in Python and in C++.

C++ reference, with `long long` for the result and the sums (starter: the quadratic loop; signature `long long count_subarrays_sum_k(std::vector<int> nums, long long k)`; the cases use `args` and `types: ["std::vector<int>", "long long"]`, the large case builds `std::vector<int>(200000, 0)` in `call`):

@@CPP:l4:CS_CPP_REF@@

@@CPP:l4:CS_CPP_START@@

**Problem 17.2** `longest_consecutive(nums)`; Python; difficulty 3. Statement: "Return the length of the longest run of consecutive whole numbers present in `nums` (in any order, with repeats); 0 for an empty list." Reference (a set, start only at run starts), starter (scans the list with `in nums`, correct but quadratic: passes the eight small cases, stopped at the first large one), tests:

@@PY:l4:LC_REF@@

@@PY:l4:LC_START@@

@@T:l4:lc@@

### l18-talking-while-coding (13 min; tags `narration`, `tradeoffs`, `product-except-self`)

Objective: Explain the plan and its trade-offs aloud while writing the code. Method stated after use: say the problem back in one sentence, give an example, name the brute force and its cost, name the better idea, write the plan as comments, then code it while saying each non-obvious line. No audio is recorded and none is graded: the lesson is practised by speaking aloud and ticking a rubric (`longform`) in the homework; in the lesson the code screen checks that the plan exists as comments.

Screens (10):
1. Hook `problem`, `console` with a transcript of a candidate who codes in silence for ten minutes and a second who narrates; `choice`: which minute counts they lose or gain (the interviewer's notes; keyed to naming the brute force first).
2. `ladder`, `choice`: the one-sentence restatement of `product_except_self` (each output is the product of all the others).
3. `ladder`, `numeric`: the brute force on `[2, 3, 4, 5]` gives `[60, 40, 30, 24]`; the cost of the brute force on `n = 100,000` is `n (n - 1) = 9,999,900,000` multiplications.
4. `ladder`, `choice`: the division idea (total product divided by each) and why it fails with a zero; `[3, 0, 2]` gives `[0, 6, 0]`.
5. `problem`, code A, `product_except_self`, `pace` 720: the hidden tests also check no division in the code and at least three comment lines of plan.
6. `trap`, `choice`: coding first and explaining after; the learner who silently writes the final loop cannot say why two passes work. Name the action in `byKey`.
7. `ladder`, `table` widget: three lines of narration matched to the three lines of code they explain (the plan comment, the left pass, the right pass).
8. `generalise` + `derive` (`order` the narration steps).
9. `transfer`, `choice`: an interviewer interrupts with "what if the list is a stream?"; the learner picks the answer that states what changes (output space, order of passes).
10. `transfer`, `choice`: how to state complexity aloud: "linear time, constant extra space apart from the output."

Quiz (4): the brute force cost; why division fails; the passes; the complexity sentence.

**Problem 18.1** `product_except_self(nums)`; Python; difficulty 3. Statement: "Return a list whose `i`-th entry is the product of every entry of `nums` except the `i`-th, without division, in `O(n)` time. Write your plan as comments first." Reference, starter (a stub with one comment, returns zeros; fails 8 of 10), tests (the last two check the source: no `/` in any code part of a line, and at least three comment lines):

@@PY:l4:PE_REF@@

@@PY:l4:PE_START@@

@@T:l4:pe@@

The big case (`[1] * 100000` with `xs[10] = 2` and `xs[500] = 3`) sums to `6 * 99,998 + 5 = 599,993`, checked by the closed form and the reference; a 50-element version was checked by the brute force.

### l19-a-live-round (15 min; tags `live-round`, `calendar-booking`, `follow-up-layering`)

Objective: Work a 45-minute live problem with two follow-ups. Skills `ci-timed` and `ci-design`. The round (reported for developer roles at trading firms: a 45-to-60-minute problem where requirements are added part-way): a calendar. Minute plan: 5 clarify and examples, 10 base, 5 test, 10 first follow-up, 10 second follow-up, 5 explain. Stage A: `Calendar().book(start, end)` accepts a half-open booking `[start, end)` if it overlaps none. Stage B (follow-up 1): `Calendar(k)` allows up to `k` bookings at any instant. Stage C (follow-up 2): `cancel(start, end)` removes one exact earlier booking and `next_free(duration, after)` returns the earliest whole start at or after `after` where a booking of that length would be accepted.

Screens (11):
1. Hook `problem`, `number-line` with bookings `[1,4)`, `[3,6)`, `[4,8)` and `[0,1)`; `tap-regions` on the bookings: tap the ones that are accepted in order with `k = 1`: `[1,4)`, `[4,8)`, `[0,1)` (the second overlaps the first).
2. `ladder`, `choice`: clarifying questions to ask in the first five minutes (half-open or closed, whole numbers, can bookings be cancelled), with a `why` on each.
3. `problem`, code A, stage A (`pace` 900): sorted starts and ends with `bisect`.
4. `ladder`, `numeric`: stage A on `[1,4)`, `[3,6)`, `[4,8)`, `[0,1)` returns `True, False, True, True`: three accepted.
5. `problem`, code B, stage B (`k`): the sorted-list shortcut breaks, so the starter is the reference of stage B with `_fits` as a stub; the learner counts overlaps at the start and at every booking start inside the new interval.
6. `ladder`, `numeric`: `k = 2` on `[1,4)`, `[3,6)`, `[2,5)`, `[4,8)` returns `True, True, False, True`.
7. `problem`, code C, stage C (`cancel` and `next_free`; the candidates for `next_free` are `after` and the booking ends after it).
8. `ladder`, `numeric`: `k = 1`, bookings `[9,12)` and `[12,15)`: `next_free(3, 9)` is 15; after `cancel(9, 12)` it is 9 (the run `[True, True, 15, 15, True, 9]` with a `next_free(2, 9)` as the third call; by the program and by trying each start in turn).
9. `transfer`, E8: the prose sends the learner to a single-drill stopwatch on an `intervals` drill of difficulty 4 (Python or C++), 45 minutes, to keep the minute plan. A `choice` asks which minute plan fits a 45-minute round with two follow-ups: 5, 10, 5, 10, 10, 5 is correct; 0, 25, 0, 10, 10, 0 and 15, 15, 5, 5, 5, 0 are wrong with a `why` each.
10. `generalise` + `derive` (`order` the 45-minute plan).
11. `transfer`, `choice`: for 10 million bookings the interviewer asks for `O(log n)` per booking with `k` general: a balanced tree or a sorted map of boundary counts (`std::map<int, int>` of +1 and -1 changes, or a sorted container in Python); the learner picks the structure and names the cost.

Quiz (4): the half-open rule; a `k` booking; `next_free` candidates; the minute plan.

**Problems 19.1 to 19.3** `Calendar`; Python; difficulty 3, 4 and 4. Driver `run_cal(k, ops)` (rows `[0, start, end]` book, `[1, start, end]` cancel, `[2, duration, after]` next_free; the driver returns one result per row: a bool for book and cancel, an int for `next_free`). For stage A the driver builds `Calendar()` with no argument. Stage A reference (sorted lists and `bisect`), then the stage B and C reference (a list of bookings and a sweep over the booking starts inside the new interval):

@@PY:l4:CAL_A@@

@@PY:l4:CAL_REF@@

Hidden driver for stages B and C (`postlude`; for stage A replace `Calendar(k)` by `Calendar()`):

@@PY:l4:CAL_POST@@

Starter (all stages; `book` always accepts, `cancel` returns `False`, `next_free` returns `after`; stage A fails 4 of 6, stage B 8 of 11, stage C 12 of 16):

@@PY:l4:CAL_START@@

Stage A tests (`k = 1`, book rows only; the last row books 3,000 disjoint bookings then one that overlaps them all, and counts the `True` results: 3,000):

@@T:l4:cal1@@

Stage B tests (all stage A rows, plus these):

@@T:l4:cal2@@

Stage C tests (all stage A and B rows, plus these):

@@T:l4:cal3@@

Checks: stage A (`bisect`) and stages B and C were each compared with a brute force that checks every integer time for occupancy, on 2,000 random book-only streams (stage A) and 3,000 random streams with all three operations and `k` from 1 to 3 (B and C). The stage C `next_free` result is the same as scanning start times one by one.

### Level 4 review (`review-4.json`, 10 items, difficulty 2 to 4, interleaving all five lessons, every case unseen in the lessons, each with `tags` and `skills`; `timed: { "seconds": 600, "lockAtZero": false }`)

| # | Lesson | Widget | d | Prompt (summary) | Key |
| --- | --- | --- | --- | --- | --- |
| 1 | l15 | `numeric` | 3 | Problems `(30, 15, 10, 5)`, `(50, 30, 20, 10)`, `(80, 45, 25, 15)` (full points, full minutes, partial points, partial minutes), budget 55. Best points. | 100 (the third problem full, 45 minutes, and the second partial, 10 minutes) |
| 2 | l15 | `numeric` | 3 | The same problems: points from taking them by points per minute, full marks only, within 55 minutes. | 80 (the first, 15 minutes, then the second, 30 minutes) |
| 3 | l16 | `multi` | 3 | For `second_largest(xs)` (the second largest distinct value, or `None` if there are fewer than two distinct values), which inputs are edge cases worth a test: `[]`, `[5]`, `[5, 5]`, `[3, 1, 2]`, `[2, 2, 1]`? | `[]`, `[5]`, `[5, 5]`, `[2, 2, 1]` (`[3, 1, 2]` is the ordinary case) |
| 4 | l16 | `numeric` | 3 | `second_largest([4, 4, 3, 3, 1])`. | 3 |
| 5 | l17 | `numeric` | 2 | A 60-minute plan has 5 minutes reading and 5 minutes testing; the first problem took 31 minutes. Minutes left for the second. | 19 |
| 6 | l17 | `numeric` | 3 | `count_subarrays_sum_k([3, 4, 7, 2, -3, 1, 4, 2], 7)`. | 4 (computed by prefix sums and by listing all 36 subarrays) |
| 7 | l17 | `numeric` | 3 | Inner-loop steps of the quadratic count for `n = 200,000`: `n (n + 1) / 2`. | 20,000,100,000 |
| 8 | l18 | `numeric` | 3 | `product_except_self([1, 2, 3, 4])`: the entry at index 2. | 8 (`[24, 12, 8, 6]`) |
| 9 | l19 | `numeric` | 3 | `Calendar()` (k = 1) books `[10,20)`, `[15,25)`, `[20,30)`: how many are accepted? | 2 |
| 10 | l19 | `numeric` | 3 | Bookings `[10,20)` and `[30,40)`, `k = 1`: `next_free(11, 10)`. | 40 (a start at 10 overlaps; at 20 a booking of 11 reaches 31, which overlaps `[30,40)`) |

The numbers are in `numbers_check.py`, `numbers_check3.py` and `numbers_check4.py`, each computed by two methods. Item 3's second largest distinct values were checked with a sort of the distinct values and a one-pass method.

### Level 4 homework (`homework-4.json`, 8 items, difficulty 3 to 5 with at least one 5, `tags` on each; one `longform`, two E11 `parts` items, one C++ `code` item)

| # | Lesson | Kind | d | Item | Key or reference |
| --- | --- | --- | --- | --- | --- |
| 1 | l19 | `parts` (E11): `code`, `choice`, `code` | 4 | A live round on a leaderboard (below). | tests and keys below |
| 2 | l19 | `parts` (E11): `numeric`, `choice`, `numeric` | 4 | Follow-ups on the calendar (below). | 499,500; the sorted structure; 20 |
| 3 | l17 | `code` (C++) | 4 | `longest_consecutive` in C++ (below). | tests below |
| 4 | l18 | `longform` | 5 | Say aloud, timing yourself to 6 minutes, the first part of a live round on `count_subarrays_sum_k`: restate, an example, the brute force and its cost, the prefix-sum idea, the plan as comments, then the complexity. | Model answer: restate (count the subarrays with sum `k`); example `[1, 1, 1]` with `k = 2` gives 2; the brute force is `O(n^2)`, 20,000,100,000 steps at `n = 200,000`; the prefix sum `S_j - S_i = k` means we count earlier prefix sums equal to `S_j - k` in a dict; plan; `O(n)` time and `O(n)` memory. Rubric (10): 2 restates and an example, 2 brute force with its cost, 2 the prefix-sum idea, 2 the plan before code, 2 complexity stated. |
| 5 | l19 | `numeric` | 4 | A leaderboard with 100,000 players answers 2,000 `top(10)` queries; sorting every score each time visits how many scores, and how many times more than a maintained top 10 that touches 10 entries per query? | 200,000,000 visits; 10,000 times more (`100,000 / 10`) |
| 6 | l15 | `order` | 4 | The first five minutes of an assessment: read every statement; note constraints and points; estimate full and partial minutes; choose full, partial or skip by points per minute and the budget; start the surest problem. Distractors: "start with the hardest problem" and "write code for the first problem before reading the others", each with a `why`. |
| 7 | l15 | `numeric` | 4 | The lesson's problems (below, in l15) with a budget of 60: best points. | 102 (and the greedy by points per minute gives 100) |
| 8 | l16 | `choice` | 4 | For `longest_consecutive`, a learner's tests so far are `[]`, `[5]`, `[1, 2, 3]` and `[1, 1, 1]`. Which test is the one most worth adding? | `[100, 4, 200, 1, 3, 2]` (shuffled, with a gap; the answer is 4). Distractors: `[2, 3, 4]` (a sorted run again), `[0]` (a single again), `[1, 2]` (a short run). |

Item 7 uses the lesson's problem set P1 `(40, 20, 12, 6)`, P2 `(60, 35, 25, 12)`, P3 `(90, 50, 30, 18)` at budget 60; the lesson itself uses budget 62 (and states 100 and 115), so the homework number 102 is new. Computed twice in `numbers_check4.py`.

**Homework item 1 (E11 parts), live round on a leaderboard.** Part 1 (code, difficulty 3): `Leaderboard` with `add_score(player, delta)` and `top(k)`, the sum of the `k` highest scores. Part 2 (choice, difficulty 4): "The interviewer says there are 100,000 players and 2,000 `top(10)` calls. What do you change?": keep a size-10 structure updated on each score change, rather than sorting every time (distractors: sort once and never update; use a list instead of a dict; recompute `top` only on the first call). Part 3 (code, difficulty 5): add `reset(player)`, which sets a player's score to zero and removes the player from the board. Driver `run_board(ops)` with rows `[0, player, delta]` add, `[1, k]` top, `[2, player]` reset; the driver returns the `top` results. Reference and starter for part 1 (the starter returns 0 from `top`; fails 3 of 4), reference and starter for part 3 (the starter's `reset` does nothing; fails 3 of 4), both with the driver; the part 3 starter shows part 1's reference. Brute force: a `Counter` sorted on every `top`; 2,000 random runs agreed.

@@PY:l4:LB1_REF@@

@@PY:l4:LB1_START@@

@@PY:l4:LB2_REF@@

@@PY:l4:LB2_START@@

@@PY:l4:LB_POST@@

Part 1 tests (rows without `reset`):

@@T:l4:lb1@@

Part 3 tests (all rows, with `reset`):

@@T:l4:lb2@@

**Homework item 2 (E11 parts), calendar follow-ups.** Part 1 (`numeric`): 1,000 bookings are accepted one at a time into a list that `book` scans in full; how many booking comparisons are made in all? 499,500 (`0 + 1 + ... + 999`, and `1,000 * 999 / 2`). Part 2 (`choice`): "Thousands of bookings a second; what do you do for `k = 1`?": keep the starts and ends sorted and use `bisect` for an `O(log n)` check (distractors: scan faster, cache the last booking only, sort the list on every `book`). Part 3 (`numeric`): the number of comparisons a binary search needs on 1,000,000 bookings, as a whole number rounded up: 20 (`ceil(log2(10^6))`, and `(10^6).bit_length()`).

**Problem H4.3** `longest_consecutive(nums)` in C++; difficulty 4; the same statement and eight small cases as `l17` Python, `std::vector<int>` in and `int` out (`args: [[100,4,200,1,3,2]]`, `types: ["std::vector<int>"]`), plus two large cases built in `call`: a permutation-like list of 200,000 values `(i * 7919) % 200003` whose expected longest run is 176,246 (from a sort-and-scan brute force), and 200,000 even numbers (expected 1). The starter is a correct but quadratic `std::find` loop (it passes the small cases and is stopped by the clock on the large ones: 6.6 s natively on the even list, longer in wasm and longer still on the permutation). Reference verified on all ten cases under `-std=c++17` and `-std=c++20`.

@@CPP:lx:LCC_REF@@

@@CPP:lx:LCC_START@@

@@T:lx:lcc@@

### Level 4 report notes

Report as `docs/LEVEL-BRIEF.md` says, naming where E3, E8 and E11 were used and whether the filter slugs matched. Do not edit files outside `app/content/courses/coding-int/`.

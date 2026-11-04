# coding-int level 4 ("Under the clock"): report

Written from `docs/briefs/coding-int.md` `## Level 4`, following `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`. Lesson ids, names, objectives and skills are those of `course.json` (`ci-timed` on l15 to l18; `ci-timed` and `ci-design` on l19). Builders and checkers are in the scratchpad folder `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/coding-int-4/` (`build4.py` writes the seven course files from `b15.py` to `b19.py`, `b_rev.py` and `b_hw.py`; `refs4.py` holds every reference, starter, driver and hidden test with its brute force; `build_drills.py` and `build_drills2.py` write the drills; `starters.mjs` grades every starter and solution in the real app; `dup4.py` is the freshness grep; `finalcheck.py` re-asserts the quiz numbers). The orchestrator may copy them to `docs/briefs/coding-int-scripts/` (my brief allowed no edits there).

## Files

All course files are in `app/content/courses/coding-int/`.

| File | Screens | Quiz / items | Code widgets (hidden tests) | Notes |
| --- | --- | --- | --- | --- |
| `l15-reading-an-assessment.json` | 10 | 4 | `best_plan` Python (10) | `console` of the three problems, two `table` widgets (a plan, Yes or No for test groups), two `order` screens, the mock named on screen 10 |
| `l16-edge-cases-first.json` | 11 | 4 | `edge_cases` Python (7), C++ `testkit` with `defines` (6) | `multi` hook on a planted bug, `table` of expected values and of edge families, a six-mutant checker in the `prelude` |
| `l17-two-in-sixty.json` | 10 | 4 | `count_subarrays_divisible_by_k` Python (11) and C++ (11), `longest_zero_sum_subarray` Python (11) | correct-but-slow starters, `table` canvases for the minute plan, the E8 session screen, the mock named on screen 10 |
| `l18-talking-while-coding.json` | 10 | 4 | `product_except_self` Python (10, two read `__learner_source__`) | `console` transcripts, `table` matching narration to code lines |
| `l19-a-live-round.json` | 11 | 4 | `Calendar` stage A (6), stage B (8), stage C (13), Python with a `run_cal` driver in `postlude` | `number-line` of half-open bookings with `tap-regions` on the intervals, the E8 stopwatch screen |
| `review-4.json` | | 10 items, d 2 to 3 | | `timed: { seconds: 900, lockAtZero: false }`; every item has `tags` and `skills` |
| `homework-4.json` | | 8 items, d 4 to 5 (one 5) | `Leaderboard` parts 1 and 3 (Python), `longest_zero_sum_subarray` (C++) | two E11 `parts` items first, one `longform` (10-point rubric), one `order` with two distractors |

Drills, in `app/content/drills/` with ten rows appended to `drills/index.json` (append only): see "Drills" below.

Every code screen has `pace` (480 on l16 screen 3 and 6, 720 on l18, 900 on l15, l19, 1,500 on l17 screens 2 and 4, 1,200 on l17 screen 6) and `tags`. Tag families are the brief's. Bank families used: `oa-triage` (l15 screens 1 to 2 and 7, review item 2, homework item 6), `edge-case-list` (l16, review 3 and 4, homework 8), `complexity-read` (l15 screen 6, review item 7, homework item 5), `timed-plan` (l15, l17, review 5, homework 7).

## Validator

`node tools/validate.mjs`: **0 errors**, and no warning on any of my files (the 487 warnings are other courses'). `docs/reviews/voice-scan.py` with `VOICE_BASE` set to the coding-int folder: 0 explanations over three sentences, 0 sentences over 20 words. `sent4.py` (the L3 checker): no prose over 60 words, no `byKey` over three sentences, no key more than 1.5 times longer than the longest distractor. No em-dash, no exclamation mark, no emoji, no firm or platform name in learner text (the only `!` is the C++ and Python `!=` inside code). Every choice has `"shuffle": true`.

## Playthrough

`node tools/playthrough.mjs --lesson coding-int/<each of the five> --set coding-int/review-4 --set coding-int/homework-4 --mobile --why --shots <dir> --local-cdn <pkgs>` (desktop and 390 px in one run), and `--drill`, `--drills` with and without `--mobile`. Results are in the table below. I read the screenshots of every new screen kind at both widths.

| File | Desktop and 390 px, `--mobile --why` (final content) |
| --- | --- |
| l15 | ok, 14 checks, quiz 4/4 |
| l16 | ok, 15 checks, quiz 4/4 (the C++ `testkit` screen compiled with the real clang) |
| l17 | ok, 14 checks, quiz 4/4 |
| l18 | ok, 14 checks, quiz 4/4 |
| l19 | ok, 15 checks, quiz 4/4 |
| review-4 | ok, recorded 10 of 10 |
| homework-4 | ok, 8 of 8 right, 38 of 38 marks, and the parts checks (open parts kept in the draft, part credit in the marks) |
| `--drills` | all 33 drill files and the sample session ok, desktop and `--mobile` (the ten `ci-` drills: the model solution passes every hidden test and the starter fails) |

An earlier desktop-only run of the same files also passed. About 460 screenshots of the final run were read at both widths for layout.

Layout fixes from the screenshots: the l15 test-group table clipped its third column at 390 px with headers such as "n up to 1,000,000", so it now has "Group 1" to "Group 3" and the sizes sit in a console above it; the l16 edge-family table wrapped code calls over three lines in a three-column layout, so it has two columns and shorter function names (`blocks`, `digits`). Every `console` has `wrap: true`.

## Starters and solutions in the app (Pyodide 0.27.7, YoWASP clang 21)

`starters.mjs` opens each code widget with the local CDN, sets the starter and grades it, then sets the solution and grades that (after a pause, because a timed-out Python run restarts the worker).

| Widget | Tests | Starter passes (so fails) | Solution |
| --- | --- | --- | --- |
| l15 `best_plan` | 10 | 2 (fails 8: tests 1, 2, 3, 5, 7, 8, 9, 10) | passes 10 |
| l16 `edge_cases` | 7 | 1 (fails 6) | passes 7 |
| l16 C++ `testkit` tests | 6 | 2 (the correct version and `BUG2`; fails 4) | passes 6 |
| l17 `count_subarrays_divisible_by_k` Python | 11 | 9 (stopped at the 5 s limit on test 10) | passes 11 |
| l17 `count_subarrays_divisible_by_k` C++ | 11 | 9 (stopped at the 5 s limit on test 10) | passes 11 |
| l17 `longest_zero_sum_subarray` | 11 | 9 (stopped on test 10) | passes 11 |
| l18 `product_except_self` | 10 | 2 (fails 8) | passes 10 |
| l19 `Calendar` stage A | 6 | 2 (fails 4) | passes 6 |
| l19 `Calendar` stage B | 8 | 1 (fails 7) | passes 8 |
| l19 `Calendar` stage C | 13 | 9 (fails 4: tests 9, 10, 11 and 13) | passes 13 |
| H4.3 `longest_zero_sum_subarray` C++ | 11 | 9 (stopped on test 10) | passes 11 |
| H4.1 `Leaderboard` part 1 | 4 | 1 (fails 3) | passes 4 |
| H4.1 `Leaderboard` part 3 | 4 own, 8 merged | 5 of 8 (fails 3) | passes all 8 |

The two `Leaderboard` starters were run natively (the app's solution check covers the parts: 38 of 38 marks). The stage B and stage C starters are the previous stage's reference with the new methods stubbed (`_fits` returns True; `cancel` returns False and `next_free` returns `after`), as the brief says for stage B.

wasm timings. The Python quadratic starters stop at the 5 s limit on the first 400,000-number test. The C++ quadratic starters are stopped by the 5 s limit on test 10 as well. The hash-map solutions pass all 11 tests inside the limit. The C++ `testkit` and `defines` behave as the brief's stand-in did: the correct version passes the learner's six tests and each of `BUG1` to `BUG5` fails at least one.

## Numbers and their sources

Every keyed number is asserted in `refs4.py`, `nums4.py`, `nums19.py`, a builder or `finalcheck.py` by two methods (the reference and an independent brute force, or a closed form or hand sum).

- Brute-force cross-checks, seeded random: `best_plan` 3,000 papers against all `3^n` choices and a memoised recursion; `longest_streak` 2,000 lists against all runs; `count_subarrays_divisible_by_k` 4,000 lists against the double loop; `longest_zero_sum_subarray` 5,000 lists against the double loop; `product_except_self` 2,000 lists against the pairwise product; `Calendar` 2,000 book-only streams (stage A) and 3,000 streams with all operations and `k` 1 to 3 (stages B and C) against a check of every integer time; `Leaderboard` 2,000 runs against a sort on every `top`. Drills: 3,000 random cases each against a brute force, with a second method for the digit-sum pairs.
- l15: rates $40/20 = 2.0$, $60/35 = 1.71$, $90/50 = 1.8$; greedy by rate 100 (P1 and P2, 55 minutes); best at 62 is 115 (P2 partial 12 minutes and 25 points, P3 full 50 and 90; by the program and by listing all 27 choices); at 60 minutes best 102 and greedy 100; the screen 10 assessment (budget 55) best 75 (A full, B part), greedy 60; quiz 1.5 against 2.0, 70 (80 minus 5 minus 5), $2{,}000^2 = 4 \times 10^6$ against $300{,}000^2 = 9 \times 10^{10}$, partial 12.
- l16: the coverage table (`[]` m2; `[7]` m1, m3; `[1, 2]` m4; `[3, 1, 1]` m1, m5, m6; `[2, 2, 2]` m1; `[1, 1, 2, 2, 2]` m1, m4, m5, m6; `[1, 1]` m1; `[2, 1]` none; `[1, 2, 2]` m1, m4, m5, m6; `[6, 6, 6, 1]` none) by running every bug; the smallest subset exposing all six is 3 (`[]`, `[7]`, `[1, 1, 2, 2, 2]`), by trying every subset of ten; `[3, 1, 1]` exposes three; `[2, 2, 2]` and `[3, 1, 1]` expose m1; the correct version and `BUG1` to `BUG5` in C++ were checked in the real clang by the playthrough (the starter passes 2 of 6, the model tests pass 6 of 6). Quiz: `[1, 4, 4]` exposes a first-run-only version, `longest_streak([8, 8, 3, 8, 8, 8])` is 3.
- l17: $60 - 5 - 28 - 5 = 22$; the 11 tests of each problem as in the brief, with the first large case changed to `k = 3` (below); $400{,}000 \times 400{,}001 / 2 = 80{,}000{,}200{,}000$ and $200{,}001 \times 200{,}000 / 2 + 200{,}000 \times 199{,}999 / 2 = 40{,}000{,}000{,}000$; zero-sum 400,000 and 399,999; screen 7 on `[4, -4, 3, -3]` (whole list, 4, against 2 if the latest sighting is kept); the C++ negative remainder: the version without the fix returns 1 on test 9, not 3 (compiled and run); quiz $90 - 6 - 8 - 37 = 39$, $5{,}000^2 = 2.5 \times 10^7$ and 60 points, `[5, -3, 3]` gives 2.
- l18: `[2, 3, 4, 5]` gives `[60, 40, 30, 24]`; $100{,}000 \times 99{,}999 = 9{,}999{,}900{,}000$; `[3, 0, 2]` gives `[0, 6, 0]`; the big test sums to $6 \times 99{,}998 + 5 = 599{,}993$; quiz $50{,}000 \times 49{,}999 = 2{,}499{,}950{,}000$, `[4, 0, 5]` gives `[0, 20, 0]`, left pass of `[3, 4, 5]` is `[1, 3, 12]`.
- l19: screen 1 `[1,4)`, `[4,8)`, `[0,1)` accepted; screen 4 (new stream) 4 accepted; screen 6 `k = 2` gives True, True, False, True (3); screen 8 gives True, True, 15, 15, True, 9; every stage test table as in the brief and re-run against the brute force; quiz `[2,6)` then `[6,9)` accepted, `k = 2` with `[4,6)` refused, `next_free(2, 5)` is 9.
- Review: 92 and 84 (see below), 19 ($60 - 5 - 5 - 31$), 4 (prefix remainders 0, 0, 1, 1, 0, 2, 3 and the double loop), 31,250,125,000 ($250{,}000 \times 250{,}001 / 2$), 8 (`[2, 1, 3, 4]` gives `[12, 24, 8, 6]`), 3 and 20 for the calendar.
- Homework: leaderboard parts by the reference and a sort on every `top` (rows in `refs4.py` and `b_hw.py`); 719,400 ($1{,}200 \times 1{,}199 / 2$); 20 ($2^{19} = 524{,}288 < 10^6 < 2^{20}$, and `(10**6 - 1).bit_length()`); longform example `[7, -2, 9, 4, -5, 6]` with `k = 5` gives 3 (prefix remainders 0, 2, 0, 4, 3, 3, 4) and $300{,}000 \times 300{,}001 / 2 = 45{,}000{,}150{,}000$; 120,000,000 ($80{,}000 \times 1{,}500$) and 16,000 times fewer than a maintained top 5; 101 at 58 minutes (third in full, second in part; greedy 82); `[5, 3, -1, -2, 4, 7]` gives 3.

## Differences from the brief (and why)

- **Fresh numbers (DECISIONS).** Several keyed items in the brief repeat a lesson's hidden test or screen. Changed: review items 1 and 2 (the brief used the 15.1 test row, budget 55, answer 100) now use `(36, 20, 14, 8)`, `(48, 30, 16, 9)`, `(75, 44, 30, 15)` at 56 minutes, best 92 and greedy 84; homework item 7 (the brief's budget 60 and answer 102 are l15 screen 9) uses `(28, 16, 9, 5)`, `(54, 32, 21, 11)`, `(80, 46, 26, 14)` at 58 minutes, 101 against greedy 82; review item 7 and the longform use $n = 250{,}000$ and $n = 300{,}000$ (the brief's 400,000 and 80,000,200,000 are l17's test); the longform example is `[7, -2, 9, 4, -5, 6]` with `k = 5` (the brief's list is l17 test 1); homework item 3 has fresh cases (nine small ones and `[2, -2] * 150000`, 300,000, and `[3, 1, -4] * 120000 + [6]`, 360,000; the brief repeated the eleven l17 cases); homework 2 part 1 uses 1,200 bookings (719,400; 499,500 appears in seven other files); homework 5 uses 80,000 players, 1,500 queries of `top(5)` (the brief's 100,000 and 2,000 are in homework item 1 part 2); review item 8 uses `[2, 1, 3, 4]`; the pair-gap, balanced-run and l16 candidate lists were changed where `dup4.py` found a list in another course.
- **Lesson difficulty.** The brief gives 15.1 difficulty 4 and other code screens 3 and 4; the validator caps a lesson screen at 3, so every lesson screen is 1 to 3. Review items are 2 to 3 and homework items 4 to 5.
- **l15.** Screen 3's table has numeric cells (minutes and points) in place of typed words. Screen 6 is a three-by-three Yes or No table with `accept: ["y", "n"]`. Screen 8's `order` is the update of one problem in the table (the brief says "the plan steps", and screen 7 already orders the opening minutes). The quiz is the brief's four.
- **l16.** Screen 5 asks which wrong version random lists of length 5 to 50 can never catch (m2). The brief says random lists "miss the empty list"; they also miss a one-element list (m3) and, in a seeded run of 1,000, caught m1 only 30 times, so the options leave m3 and m1 out and the key is the one that is impossible. The correct version and five bugs are used in C++ as the brief says (`m6` is Python only).
- **l17.** The first large case uses `k = 3` instead of `k = 1` in both languages (same expected count): clang folds `total % 1` and finishes the brief's C++ case at once, so the C++ starter passed the case meant to stop it (raised in the inbox). Screen 4's tests are the same 11 in both languages. The E8 screen says to choose one pattern, since the filter is a single select.
- **l19.** The validator needs a trap screen and the brief has none, so screen 6 (`k = 2`, four bookings) is a `trap`: a learner who checks only the new booking's start accepts `[2, 5)` and says 4. Screen 4 runs stage A on a new stream (`[2,5)`, `[5,7)`, `[4,6)`, `[7,9)`, `[0,2)`, 4 accepted), because screen 1 already asks the brief's four bookings. Stage B's starter is the stage C reference with `_fits` stubbed (7 of 8 fail); stage C's starter has `book` and `_fits` working and `cancel` and `next_free` stubbed.
- **E11 (homework).** Items 1 and 2 are the two `parts` items, first and second, as the brief and `partsHomeworkChecks` need. Part 3 of item 1 shows part 1's reference with `reset` doing nothing, and its own four tests are two of the brief's rows and two new rows (reset then add again, and reset of an unknown player); merged with part 1's four rows it runs eight.
- **Choice screens.** The brief's keys were shortened or the distractors lengthened where the key was more than 1.5 times the longest distractor (l16 quiz 3, l18 screens 4 and 6, l19 screens 2 and 11, homework 8).

## Mock and drill claims

The mock named on l15 screen 10 and l17 screen 10 is `#exam/mock-oa-code`, built before this level: two Python problems in 60 minutes drawn from the eight `oa` drills (one of difficulty 3 and one of 4), a problem scoring only when every hidden test passes. The lessons say exactly that, in prose that does not name a firm, and say that a brute-force partial earns nothing there (l17), so the mock is for the plan, not for partial credit. Reported formats are called "reported" (l15 screen 1 and l19 screen 2).

## Drills

The brief names the E8 filters, not the drills, and packs 1 to 4 did not exist, so `#drill` had nothing for `prefix-sums`, `hashing` or `intervals` (only hidden samples). I authored ten drills in pack `ci` so that the lesson screens work. The filter slugs matched the engine's vocabulary (`prefix-sums`, `hashing`, `intervals`). The session picks two drills that pass one pattern, so each of `prefix-sums` and `hashing` has two drills in each language at difficulty 3 to 4, and `intervals` has one in each language at difficulty 4 (`pool.py` prints them).

| Drill | Language | Pattern | d | Tests | Starter fails |
| --- | --- | --- | --- | --- | --- |
| `ci-balanced-run` | Python | `prefix-sums` | 4 | 12 | 8 |
| `ci-split-points` | Python | `prefix-sums` | 3 | 14 | 11 |
| `ci-cpp-longest-sum-k` | C++ | `prefix-sums` | 4 | 14 | yes |
| `ci-cpp-range-sums` | C++ | `prefix-sums` | 3 | 10 | yes |
| `ci-pair-gaps` | Python | `hashing` | 3 | 12 | 10 |
| `ci-same-total-pairs` | Python | `hashing` | 3 | 12 | 10 |
| `ci-cpp-first-missing` | C++ | `hashing` | 3 | 13 | yes |
| `ci-cpp-sum-pairs` | C++ | `hashing` | 3 | 12 | yes |
| `ci-interval-intersections` | Python | `intervals` | 4 | 11 | 9 |
| `ci-cpp-insert-interval` | C++ | `intervals` | 4 | 13 | yes |

Every drill has a model solution that passes every test, a starter that fails (`playthrough --drill` for each, and `--drills`, which also passes the sample session), expected values from an independent brute force or a closed form, and large cases that stop the slow method. No pattern slug was added.

## Engine features used

E3: not used directly (the mock was authored earlier; l15 and l17 name it). E8: l17 screen 8 (a `#drill/session` split) and l19 screen 9 (a `#drill` stopwatch on `intervals`), backed by the drills above. E11: homework items 1 and 2 (`code`, `choice`, `code` and `numeric`, `choice`, `numeric`); the playthrough's parts checks pass. C-parts-code: the cumulative tests worked (part 3 passes part 1's rows under its own widget). `testkit` and `defines`: l16 screen 6. `timed` on `review-4`. Canvases: `console`, `table`, `number-line` with `tapIntervals`.

## Proposed `course.json` change

None.

## Inbox

Five bullets under `Raised later (coding-int level 4):` in `docs/BACKLOG-INBOX.md`: no link markup in prose, the single-pattern drill filter, clang folding a constant `k` in a C++ case, a select cell for the `table` widget, and the starter check missing for `parts` code widgets.

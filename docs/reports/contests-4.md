# contests level 4 (In the contest): report

This level was written by a content agent that a container restart stopped just before it reported. The six files were on disk and committed, with the validator at 0 errors. A second agent triaged them: it played every file, recomputed every number independently, checked every code widget against its starter and against wrong versions, and fixed what it found with targeted edits. The level is kept.

## Files

All in `app/content/courses/contests/`. Skills are as the brief asks: `cn-strategy` and `cn-patterns` for l13, `cn-strategy` for l14 and l16, `cn-impl` and `cn-strategy` for l15.

| File | Screens or items | Quiz | Code screens | Notes |
|---|---|---|---|---|
| `l13-virtual-contest.json` | 11 screens (difficulty 1 to 3) | 4 | 4: `peaks` (A, about 800), `shortest_cover` (B, about 1100), `can_ship` with `min_capacity` (C, about 1300), `grid_moves` (D, about 1500) | statements in a `console` with a frames control; a time-log `table`; trap: starting with D |
| `l14-which-first.json` | 12 screens | 4 | 3: `decayed_score`, `icpc_rank_key`, `best_order` | bars with a frames control over three orders; plane of expected score against minutes on D; trap: sunk cost; edge case: the scoreboard beats the letters |
| `l15-debugging-under-time.json` | 11 screens | 4 | 4: three fix-the-bug screens (`last_occurrence`, `count_inversions_small`, `solve_all`) and `smallest_failing` | trap: debug prints on standard output; deep recursion answered with an explicit stack |
| `l16-upsolving.json` | 12 screens | 4 | 2: `equal_thirds` (D, about 1600), `mistakes_summary` | mistakes-log tables; closing screens on what a rating counts for |
| `review-4.json` | 8 items: 2 at difficulty 2, 4 at 3, 2 at 4 | | none | covers all four lessons |
| `homework-4.json` | 7 items: 2 at 3, 3 at 4, 2 at 5 | | 3: `desks_after_cut` (4), `max_profit_k` (4), `widest_gap` (5) | an `order` item (the first ten minutes of a contest), a numeric ICPC penalty, a track choice, and a `longform` (5) with a 10-point rubric and a full model answer |

## Validator

`node tools/validate.mjs` (from `app/`): 0 errors, 328 warnings overall, none on these six files.

## Playthrough

`node tools/playthrough.mjs --lesson contests/<id>` and `--set contests/review-4` or `homework-4`, each with `--local-cdn <scratchpad>/pkgs`. All six passed before any edit. After the fixes I ran all six again with `--shots ... --mobile --why`, then once more without shots, and finally l14, review-4 and homework-4 alone after the last prose edits. The final results:
- l13: ok, 15 checks, quiz 4/4
- l14: ok, 16 checks, quiz 4/4
- l15: ok, 15 checks, quiz 4/4
- l16: ok, 16 checks, quiz 4/4
- review-4: ok, 8 of 8 recorded
- homework-4: ok, 7 of 7 right, 33 of 33 marks
- No console errors.

I looked at desktop and 390 px screenshots of the custom canvases (the l13 statements frames and time-log table, l14's bars frames and plane, l15's verdict console and hand-case frames, l16's logs and track table). Two faults found, both fixed (see below). The 390 px time-log table scrolls sideways (see open issues).

## Code widgets checked

Every code widget (16 in total: l13 four, l14 three, l15 four, l16 two, homework three) was run in CPython 3.13 (`harness.py`, the app's namespace rules: prelude, code, postlude, then each case) and in Pyodide 0.27.7 under Node (`pyrun2.mjs`). The two agree on every case.
- **Solutions** pass every hidden test in both. The slowest case in Pyodide is 0.67 s (`widest_gap`, 200,000 levels); `desks_after_cut` takes 0.47 s.
- **Starters** fail:
  - The "write it" starters (`...` bodies) fail every test, except cases whose expected value is `None` or whose check passes on a no-op (see "Fixes made", counting cases).
  - The three planted-bug starters in l15 pass exactly the tests the lesson says they pass: `last_occurrence` fails tests 4 to 7, `count_inversions_small` fails 3, 5, 6 and 7, `solve_all` passes test 1 (the example) and fails 2 to 6.
- **Wrong versions** each fail the intended test. Verified by running them:
  - l13 A: `>=`, and counting the ends (tests 5, 6, 10 and 2 to 4).
  - l13 B: a restart scan (test 8 by reads, test 9 stopped on time); `len(needed)` instead of `len(set(needed))` (test 5).
  - l13 C: a linear scan (test 10 by calls, test 11 stopped on time); a search starting at `hi = 10**9` (test 10, 30 calls against the 13 allowed); a binary search from `lo = 1` (passes, 11 calls).
  - l13 D: ignoring arrows (tests 1, 2, 9); arrows checked on entry (tests 1, 2, 8, 9); a relaxing DFS (stopped on time).
  - l14: no floor (2, 6, 7); floor before the costs (2, 6); unsolved rejections counted in the ICPC key (1, 2); `+solved` (1, 4 to 7); greedy by points per minute (2, 3); no sort of names (3); late problems scored (2, 4, 6).
  - l15: first occurrence (1, 5, 6); adjacent-only inversions (1, 2, 6, 7); a global reset after the loop (2); `smallest_failing` run at length 8 only (1 to 4, 7) or up to 4 only (7).
  - l16: a double loop (test 8 stopped on time); adding the first cut before checking the second, or letting the third run be empty (2, 6, 8); no divisibility check (5); sorting by name only (7, 8, since this version passed all six original tests); first-appearance ties (1, 4); lower-casing (6).
  - Homework: recursive DFS at the default limit (7, 8); cutting by pair rather than by index (4); a quadratic component merge (stopped on time); an O(n^2 k) DP (stopped on time); unlimited trades (2, 3, 8); a linear scan over distances (stopped on time); no sort (1, 3, 5, 7, 8); `lo = 1` (4).
- **Size and counting cases reject slow code**:
  - l13 B test 8 (reads, at most 8,000 for a tape of 2,000; the solution reads 3,922) and test 9 (200,000 trades with the rare name last, where a restart scan needs about $2 \cdot 10^{10}$ steps).
  - l13 C test 10 (calls to `can_ship`, at most 13; the solution makes 11, a linear scan about 811) and test 11 (100,000 orders).
  - l13 D test 9 (200,000 cells).
  - l16 `equal_thirds` tests 8 and 9 (200,000 days, a double loop is about $2 \cdot 10^{10}$ steps).
  - Homework: item 1 tests 7 and 8, item 2 test 8 (10,000 prices, $k = 20$, where $O(n^2 k)$ is about $2 \cdot 10^9$), item 3 test 8 (200,000 levels).
  - l13 A and l15's three fix screens are not about speed; their size cases only confirm that a linear solution is fast enough.

## Numbers checked

Every number was computed three ways: the agent's solution in CPython and Pyodide (the tests above), my own independent code (`indep.py`, `nums13.py`, `nums14.py`, with NumPy and SciPy where useful: `shortest_path` for the grid, `connected_components` for the desks, `cumsum` for the thirds), and, for scoring and fractions, a hand check against the stated rule. All agree.

**l13**
- Problem A: 66,543 peaks (seed 13, values to $10^9$) and 37,237 (seed 14, values 1 to 3) at $n = 200{,}000$, both by a NumPy comparison of neighbours; the eight small cases (2, 0, 0, 0, 0, 0, 2, 1) traced by hand.
- Problem B: the example gives 2, and 3 with all three names. Both size answers are 75 (200,000 trades, seed 21) and 79 (2,000 trades, seed 22), computed by reading the tape backwards to the first moment all 26 names are seen. The 2,000-trade solution makes 3,922 reads against the allowed 8,000. A restart scan needs $200{,}000^2 / 2 = 2 \cdot 10^{10}$ steps.
- Problem C:
  - The example is 12; capacity 11 needs 4 days (4; 8, 2; 7; 5, 3).
  - The 40-order case has total 1,807 and maximum 99, answer 909. The search makes 11 calls; a scan upwards from 99 makes $909 - 99 + 1 = 811$. $\log_2 1807 = 10.8$.
  - The 100,000-order case (seed 31, $k = 500$) gives 1,002,823, computed with an independent greedy that jumps by `bisect` on prefix sums.
  - Lesson numbers: $2^{30} = 1.07 \cdot 10^9$; $30 \cdot 10^5 = 3 \cdot 10^6$.
- Problem D: the example is 11 (path through the `>` in row 2); ignoring arrows gives 7. The 400 by 500 city (seed 40) gives 908. The seven small cases (-1, 0, -1, 2, 4, 2, 2) and the quiz grid `.>` over `v.` (-1) agree with the SciPy search.
- Sam's round: D took 52 minutes, the second rejection came 13 minutes after the first, A took 7. Alex's log totals 16, 27 and 17 minutes and 3 rejections; the three times sum to 60.

**l14**
- The rule (loses $v/250$ per minute and 50 per rejection, floor 0.3 of the value):
  - B at minute 35 after one rejection: $1000 - 140 - 50 = 810$ (860 and 760 are the distractors); all eight `decayed_score` tests recomputed, including the floor reached exactly at minute 175 (300) and A late with three rejections (110 against a floor of 150).
  - Orders: A B C D 480 + 880 + 1,110 + 1,080 = 3,550; D C B A 1,600 + 990 + 580 + 270 = 3,440; C A B D 1,290 + 410 + 740 + 1,080 = 3,520; A B D C 3,530. D C B A loses 630 on A, B and C together (210, 300, 120).
  - Rates: 50, 50, 42.857, 40. The swap formula gives $(2000 \cdot 35 - 1500 \cdot 50)/250 = -20$, so C then D scores 20 more.
- Plane: $E(x) = 1000(1 - e^{-x/50}) + 800(1 - e^{-(60-x)/15})$ peaks at $x = 34.84$ with 1,152.3 points (a root-finder and a fine grid agree); $E(0) = 785.3$, $E(60) = 698.8$, $E(10) = 952.7$.
- `best_order` by an independent brute force: 3,550 for A B C D at 120 minutes; 2,090 for B C A D at 60 (A then B scores 1,360, A then D 2,000); 1,550 for P then Q; 5,132 for E B A C D F on the six-problem set. The 60-minute case needs a different order from the greedy one (greedy by rate fails tests 2 and 3).
- ICPC: $12 + 61 + 135 = 208$; X 195, Y 185; the homework penalty $209 + 60 = 269$ (349 with E's rejections, 209 with none).
- Desk triage: £600, £480 and £100 a minute; quote and hedge fit in 30 minutes. 702 / 96 = 7.3.

**l15**
- `last_occurrence`: the buggy starter returns -1 on `[5]` and 1 on `[3, 3, 3]`, and agrees on the other two hand cases, so exactly two of the four differ.
- `count_inversions_small`: 435,115 for 1,500 values from 1 to 5 (seed 81), by an independent counting method; `[2, 1, 2, 1]` has 3; `[5, 4, 3, 2, 1]` has 10.
- `smallest_failing`: all seven expected cases ([2, 2], [3, 2], [2, 1, 1], [3, 2, 2], None, None, [1, 1, 1, 2, 1]) reproduced by an independent implementation of the same loop with its own brute force and generators.
- Recursion: a 100,000-long line fails at Python's default limit of 1,000 and passes with `sys.setrecursionlimit(10**6)`, in CPython, in Pyodide under Node, and in a Pyodide worker in Chromium (a million frames). The lesson says exactly this (see departures).
- Quiz: $2 \cdot 10^5 \cdot 10^9 = 2 \cdot 10^{14}$ against $2^{31} - 1 = 2{,}147{,}483{,}647$; `[3, 2, 1]` gives 2 for neighbour pairs, 3 correct.

**l16**
- `equal_thirds`: the example gives 2; five zeros give 6, and $\binom{199999}{2} = 19{,}999{,}700{,}001$ (200,000 zeros); the seed-92 case (values -1 to 1) gives 97,944 by a NumPy `cumsum` count; the other small cases (0, 1, 0, 1, 0) were traced by hand. $\binom{4}{2} = 6$, $\binom{3}{2} = 3$; $19{,}999{,}700{,}001 / 2{,}147{,}483{,}647 = 9.3$.
- Mistakes log: 3, 2, 2 and 1, eight in all. `mistakes_summary` of the lesson log is already in alphabetical order, so I added two tests where it is not (see fixes).
- Thresholds: $1200 + 300 = 1500$ (C 1400 and D 1500 in range; E 1900 is 700 above, F 2400 is 1,200 above); $1250 + 100$ to $200$ gives 1350 to 1450; $1500 + 300 = 1800$; $1350 + 300 = 1650$; 2000 is 750 above 1250; 1410 to 1800 is 390.

**Review and homework**
- Review: 18 / 60 = 30% (50% and 60% are the distractors); $1500 - 288 - 100 = 1112$; Q then P scores 20 more (60 and 80 lost); E at minute 115 scores $1250 - 575 = 675$ against a floor of 375; $2 \cdot 10^5 \cdot 10^9 = 2 \cdot 10^{14}$ limits for the brute-force option.
- Homework size cases: 32,360 groups for 200,000 random links (seed 51, cut link 7) by SciPy; 2 groups for a chain cut in the middle; 19,958 profit for 10,000 prices (seed 61, $k = 20$) by a second DP formulation; 996,391 widest gap for 200,000 levels (seed 71, $m = 1000$) by `bisect` jumps. The small cases (3, 8, 1, 0, 9, 2, 3) agree.
- Model answer: the time rows match l13's log (9, 17, 27 and 7 minutes, 60 in all), and the mistakes follow from the l13 tests.

## Starters

The brief asks that the starter fails the hidden tests. Checked in CPython and Pyodide, as above. The l15 screens give starters with the planted bug, which pass the example and fail the rest by design. `smallest_failing`'s starter returns `None`, so it passes the two tests that expect `None`; the other five fail it.

## Fixes made

Targeted edits only, nothing regenerated. No graded answer changed except the tolerance on one cell (item 6).

1. **l13 counting cases passed a do-nothing starter.** Test 8 of B and test 10 of C checked only the read count or the call count, so a starter returning `None` passed. Each now also checks the answer (`shortest_cover(...) == 79 and reads_for(...) <= 8000`; `checks_used(w, 2)[0] == 909 and checks_used(w, 2)[1] <= 13`). The starters now fail every test.
2. **l13 C test 10's message** said trying capacities one by one is linear, which misdescribed a search that starts at $10^9$ (30 calls, over the allowed 13). It now says to search between the heaviest order and the total, halving the range.
3. **l13 statement D** said one-way cells were "left only that way", which reads as "abandoned". Now "exited only that way".
4. **l14 explore** said the bars used "the times in the table" although the screen has no table. The prose now gives the four solving times.
5. **l14 hook** now says the decay rule is this course's illustration, not Codeforces' current rule, as the brief asks.
6. **l14 rate table:** the tolerance on C's points per minute was 0.05, so a learner who rounded 42.857 to 43 failed. It is now 0.15, which accepts 43 and still rejects 42 and 44. This is the only graded answer touched.
7. **l16 `mistakes_summary` tests were too weak.** The lesson's own log has its counts in alphabetical order, so a function that sorted by name alone passed all six tests. Added test 7 (`overflow` twice, `misread` once) and test 8 (`x` three times, `z` twice, `y` once), a `byKey` line for test 7, and the `how` text (now 8 tests).
8. **l16 screen 12:** "more than 400 more points" for a rise from 1,410 to 1,800 (390 points) now reads "more than another 390 rating points".
9. **review-4 item 1:** the "about $2 \cdot 10^{14}$ limits" in a distractor had no stated bound. The statement now says each redemption is at most $10^9$.
10. **homework-4 item 1:** the `how` now says the chain is deeper than Python's default limit of 1,000.
11. **Voice:** homework item 3's explanation had four sentences and is now three; the model answer's three longest sentences (23 to 25 words) were split.

## Departures from the brief, with reasons

- **l15's recursion claim differs from the brief.** The brief says Pyodide's stack is small, so deep recursion crashes before `sys.setrecursionlimit` helps. It does not: in this app's Pyodide (checked in Node and in a Chromium worker) a 100,000-deep DFS passes with the limit raised, and a million frames run. The lesson says so, and still teaches an explicit stack, because a judge with a small stack can crash and the default limit fails. A recursive DFS with the limit raised would pass homework item 1 in the app.
- **l16's problem D is a new problem, not l13's D.** The brief allows "a new problem at about 1500 whose editorial idea the lesson gives in prose". Its rating is stated as about 1600. The statement is original wording, but the task (cut an array into three runs of equal sum) is a standard one.
- **Homework items 2 and 3 are standard problems:** "at most $k$ trades" (the usual best-time-to-trade DP) and "spread the bots" (the usual binary search on the minimum distance, the "aggressive cows" idea). The statements and numbers are original; the brief suggested the first.
- **The l13 time log is Alex's, not the learner's.** A table widget cannot store the learner's own minutes, so the lesson asks for the 60-minute timer and a log outside the app and grades a worked log. The first screen says the lesson has no clock.
- **No Codeforces rank names or current rules are quoted.** The files avoid the names (Pupil, Specialist) and any exact Codeforces scoring, so nothing needed checking on codeforces.com. The only scoring quoted is the course's own rule, labelled as an illustration.

## Open issues

- **Table width at 390 px.** l13's five-column time log (Problem, Read, Code, Debug, Wrong) scrolls sideways on a phone with no hint, and the Wrong column is off screen. Shortening the first header did not help.
- **Counting-only cases** still pass a do-nothing starter in general; here each is paired with an answer check, but the harness could offer a `reads` comparison that also checks the value (see inbox).

## Backlog

Four bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (contests level 4)": the five-column table at 390 px, the lack of a lesson clock or a learner-owned log, counting cases that pass a do-nothing starter, and the recursion fact above.

## Proposed course.json change

None.

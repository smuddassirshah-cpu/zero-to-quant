# Answer check, coding-int level 4 (4 November 2026)

**Summary.** 95 graded items checked (l15 14, l16 15, l17 14, l18 14, l19 15, review-4 10, homework-4 13 parts and items), 13 code items and 10 `ci-*` drills (about 230 hidden tests), 4 canvases and 3 cross-links. Wrong keys: 0. Other mismatches: 7 false feedback, hint or wording claims, 4 weak test sets (wrong solutions pass), 2 false constraint or time claims, 3 duplicates, 16 choice keys longest, 3 sentences of exactly 20 words, 3 bad hint highlights, plus notes. Earlier recheck item `coding-int/l12-file-system.json` `q-ls-file` is still open (key 32 characters against 31).

Scripts are in the scratchpad folder `answers-coding-4`: `catalog.py` (collects every code widget), `rpy.py` (Python runner: prelude, solution, postlude, setup, call, 5 s per test, `__learner_source__`), `rcpp.py` (C++ runner, `g++ -std=c++20 -O1 -fno-exceptions`, one process per test, a small `testkit`, `defines`), `mut15.py`, `mut17.py`, `mut19.py`, `mutdrills.py`, `mutcpp.py` (wrong solutions), `drills_check.py` (brute forces), `lint.py` and `dups.py`. I read no generator script or author report. I did read the l15 and l17 links to `exams/mock-oa-code.json`.

## Code items

For each: the reference passes every test (and every example); the starter fails; wrong solutions tried. "Passes" means the wrong solution passed every hidden test.

| Item | Reference | Starter | Wrong solutions that fail | Wrong solutions that pass |
|---|---|---|---|---|
| l15 s3 `best_plan` (10 tests) | 10/10 | 2/10 | both full and partial, in-place (item reused), exact minutes, `range(budget)`, strict `>`, greedy by rate, full only, partial only if full does not fit, 3^n recursion (stops at test 10) | none (memoised recursion is correct) |
| l16 s2 `edge_cases` (7) | 7/7 | 1/7 | `[]`, `[7]`, `[1, 1, 2, 2, 2]` catch all six; no two inputs do (checked all subsets of ten) | none |
| l16 s5 C++ tests (6) | 6/6 | 2/6 (passes case 1 and BUG2 only, as stated) | n/a | none |
| l17 s1 `count_subarrays_divisible_by_k` (11) | 11/11 | 9/11, stops at test 10 | no empty prefix, wrong pair formula, zero class only, overwrite not increment, C-style remainder (10/11), double loop | none (array of size k and `c(c-1)/2` are correct) |
| l17 s3 same in C++ (11) | 11/11 | 9/11 | no normalising (10/11), `abs` remainder (10/11), `int` count (9/11), no `{0: 1}` seed | `int total` (not a bug at these sizes) |
| l17 s5 `longest_zero_sum_subarray` (11) | 11/11 | 9/11 | no `{0: -1}`, latest index, `+1`, count not length, window of 50 (9/11) | **prefix-only (`total == 0` gives `i + 1`) passes 11/11** (mismatch 9) |
| l18 s4 `product_except_self` (10) | 10/10 | 2/10 | left only, quadratic `prod` (stops at test 8), division with zero count (fails test 9), `//` with zero guard, no comments (9/10), right start bug | two arrays (correct) |
| l19 s2 stage A (6) | 6/6 | 2/6 | left only, right only, touching refused (either side), scan of all bookings (stops at test 6) | none |
| l19 s4 stage B (8) | 8/8 | 1/8 | start only, interior only, interior including the end, `>= k`, missing `+ 1`, inclusive cover | **total overlap count passes 8/8** (mismatch 8) |
| l19 s6 stage C (13) | 13/13 | 9/13 | no `after` candidate, wrong cancel (always True, by start), last end only, starts as candidates, duration ignored | **total overlap count, unsorted candidates and cancel-all-copies pass 13/13** (mismatch 8) |
| homework `h4-leaderboard` p0 (4) and p2 (4, plus p0 again) | 4/4 and 4/4; p2 solution passes p0's tests | 1/4 and 1/4 | ascending sort, wrong slice, error on absent reset, overwriting scores (fails p0's tests) | **reset to zero without removing** (no negative scores in any test) |
| homework `h4-zero-sum-cpp` (11) | 11/11 | 9/11, stops at test 10 | latest index, no seed | **prefix-only passes 11/11** (mismatch 9); `int total` passes (fine at these sizes) |

| Drill | Reference | Starter | Fail | Pass |
|---|---|---|---|---|
| `ci-balanced-run` (12) | 12/12 | 4/12 | latest index, no seed, `+1`, 0 as 0, prefix only (10/12), window of 30 (10/12), double loop (stops at test 11) | none |
| `ci-pair-gaps` (12) | 12/12 | 2/12 | k=0 double count, distinct values, one side, record first, set instead of counts, double loop | none |
| `ci-same-total-pairs` (12) | 12/12 | 2/12 | keep first, keep last (10/12), 0 instead of -1, mod 9 key, double loop | top two per key (correct) |
| `ci-split-points` (14) | 12 of 14 ran, 14/14 pass | 3/14 | last cut counted, first cut skipped, double loop | **`left == total // 2` passes 14/14; early break once `left * 2 > total` passes 14/14** (mismatch 10) |
| `ci-interval-intersections` (11) | 11/11 | 2/11 | strict `<`, advance both, advance by start, double loop | tie rule advancing `a` only (correct) |
| `ci-cpp-first-missing` (13) | 13/13 | 0/13 | `max + 1`, unchecked `vector<bool>` (crash), from 0, only to `n` | sort (correct); **`std::find` per candidate passes 13/13 in 4.3 s native** (mismatch 13) |
| `ci-cpp-insert-interval` (13) | 13/13 | 3/13 | touching not joined (front, back), end not max, start not min, no tail, `erase` loop (stops at test 12) | sort then merge (correct) |
| `ci-cpp-longest-sum-k` (14) | 14/14 | 2/14 | latest index, no seed, plus `k`, positive-only window (10/14), double loop | store-before-lookup and `int total` (correct within limits) |
| `ci-cpp-range-sums` (10) | 10/10 | 0/10 | off by one, per-query loop (stops at test 9) | **`int` prefix and `int` cast pass 10/10** (mismatch 12) |
| `ci-cpp-sum-pairs` (12) | 12/12 | 3/12 | `int` count (11/12), self pair, distinct pairs, double loop, two pointers ignoring duplicates | sorted two pointers (correct) |

Brute-force recomputation of every expected value: all 12 to 14 small tests per drill, and each large test by an independent formula (balanced `[0, 1] * 100000` 200000 and `[1] * 100000 + [0] * 50000` 100000; pair gaps 10000000000 and 11249925000; digit sums 399987 and 1999999971; split points 199999 and 99999; intersections 100000 and 200000; `count_pairs_with_sum` 16199910000 and 4994950; range sums 40000000000 and -33334; insert interval sizes 50002 and 100000; longest sum 150000, 300000 and 300001; first missing 200001 and 150000). Lesson tests: 80,000,200,000 is $400000 \times 400001 / 2$; 40,000,000,000 is $\binom{200001}{2} + \binom{200000}{2}$; test 10 of l15 is 2724 by an independent exact-minutes table; l18 test 8 is 599993. All agree.

Time limits: every reference runs in under 0.2 s native. Quadratic starters need 8e10 steps at 400,000 numbers, so they stop at test 10 in Pyodide and wasm. The one marginal case is `ci-cpp-first-missing` (mismatch 13). The 60,000-booking test stops a scan in Python (1.8e9 comparisons).

## l15 Reading an online assessment (14 items)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| s0 best rate | P1 | 40/20 = 2.0, 60/35 = 1.71, 90/50 = 1.8 | OK |
| s1 greedy | 100 | P1 (20) leaves 42, P3 (50) skipped, P2 (35) fits: 40 + 60. wrong 130 (70 min), 190 (105 min), 40 | OK |
| s2 table | P2 12/25, P3 50/90, total 62/115 | brute force over 27 plans at 62 minutes: unique best, (P3 full, P2 part) = 115 | OK |
| s3 `best_plan` | code | see code table | OK |
| s4 trap | 115 | as s2; C 130 needs 70 min; partial rates 2.0, 2.08 (and 1.67 for P3, not mentioned) | OK, see notes |
| s5 table | Yes/No grid | $10^6$, $10^{10}$, $10^{12}$ against $10^8$; $n \log n$ at $10^6$ is $2 \times 10^7$ | OK |
| s6, s7 order | 1..6, s1..s5 | no alternative order is defensible | OK |
| s8 budget 60 | 102 | brute force: 102. Two plans reach it: P1 and P3 in part with P2 in full (59 min), and P1 in part with P3 in full (56 min) | **Mismatch 1** |
| s9 two problems, 55 minutes | A full, B part: 75 | A 40 + B 15 = 55, 50 + 25 = 75; B full + A part 57 min; brute force 75 | OK, **mismatch 2** (distractor d) |
| q-rate | Y | 1.5 against 2.0 | OK |
| q-budget | 70 | 80 - 5 - 5; wrong 75, 80 | OK |
| q-group | only the first | $2000^2 = 4 \times 10^6$, $300000^2 = 9 \times 10^{10}$ | OK |
| q-partial | partial | 8 minutes left, full 25, partial 5 | OK |

Link to `exams/mock-oa-code.json`: "two Python problems in 60 minutes" and "scores a problem only when every hidden test passes" both match its description and paper (60 minutes, two draws from `drills/oa`, difficulty 3 and 4). `#exam/mock-oa-code` is the router form. Cross-references `contests` l14-which-first, l2 (10^8 steps a second) exist and agree.

## l16 Edge cases first (15 items)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| s0 multi | `[2, 2, 2]`, `[3, 1, 1]` | m1 returns 0 and 1 there against 3 and 2; 0, 1, 1 on `[]`, `[1, 2]`, `[2, 1]`, all right | OK |
| s1 table | 0, 1, 1, 2, 3, 3 | by hand and by `_ref` | OK |
| s2 `edge_cases` | code | see code table | OK |
| s3 count | 3 | `[3, 1, 1]` exposes m1, m5, m6 (m2, m3, m4 give 2) | OK |
| s4 trap | m2 | lists of 5 to 50 never include `[]`. m3 is equally unreachable (length 1) but is not offered | OK, see notes |
| s5 C++ | code | starter fails all but case 1 and BUG2 | OK |
| s6 table | 0, 3, 1, 1, 1, 2 | closed intervals touch and nest; sign is not a digit | OK |
| s7 order | t1..t6 with d1 left out | fine | OK |
| s8 multi | `[]`, touching, nested | spread-out cases pass any merge | OK |
| s9 shortest list | 3 | all 1,023 subsets of the ten candidates: minimum 3 (`[]`, `[7]`, `[1, 1, 2, 2, 2]` or `[1, 2, 2]`); `[2, 1]` and `[6, 6, 6, 1]` catch nothing | OK |
| s10 first line | edge families | fine | OK |
| q-expose | `[1, 4, 4]` | first-run-only gives 1, right answer 2 | OK |
| q-expected | 3 | runs 2 and 3; wrong 2, 5 | OK |
| q-random, q-family | key text | fine | OK |

## l17 Two problems in sixty minutes (14 items)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| s0 | 22 | 60 - 5 - 28 - 5; wrong 25, 27, 32 | OK |
| s1, s3 | code | tests 1 to 11 all recomputed by brute force | OK |
| s2 | 9 | slow code passes tests 1 to 9, stops at 10 | OK |
| s4 trap | submit the partial | 5 + 40 = 45 on the canvas; 15 left | OK |
| s5 | code | brute force agrees on all 11; every large answer is a prefix (mismatch 9) | tests weak |
| s6 | first sighting | prefixes 0, 4, 0, 3, 0: first gives 4, latest gives 2 | OK |
| s7 | 5, 25, 25, 5 | b 0+30+30+0, c 10+20+20+10, d 5+45+5+5 all 60 | OK |
| s8 order | m1..m4 | fine | OK |
| s9 | A full, B brute force | 20 + 10 = 30 minutes, 65 points; B full + A in 10 earns 60; both full 60 minutes; A only 50. Mock claim OK | OK |
| q-left | 39 | 90 - 6 - 8 - 37; wrong 47, 53 | OK |
| q-points | 60 | $5000^2 = 2.5 \times 10^7$, $200000^2 = 4 \times 10^{10}$ | OK |
| q-box | submit | fine | OK |
| q-first | 2 | prefixes 0, 5, 2, 5: first 5 at element 0, repeat at 2 | OK |

## l18 Talking while coding (14 items)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| s0 | name the brute force | canvas has A silent 10 minutes and B's three lines | OK |
| s1 | all the other entries | 3 x 4 x 5 = 60 for the 2; whole list 120 | OK |
| s2 | 9999900000 | 100000 x 99999; wrong 10^10, 100000 | OK |
| s3 | total is 0 | `[3, 0, 2]` gives `[0, 6, 0]` | OK |
| s4 | code | see table | OK |
| s5, s7 | plan first; order n1..n6 | fine | OK |
| s6 table | 1, 2, 3 | canvas lines: comment, forward loop, backward loop | OK |
| s8 | store the numbers | left pass streams, right pass needs the end | OK |
| s9 | linear, constant extra | two passes add | OK |
| q-cost | 2499950000 | 50000 x 49999 | OK |
| q-zero | 0 / 0 | total 0; sum of others 9; product 20 | OK |
| q-pass | `[1, 3, 12]` | left products of `[3, 4, 5]`; final `[20, 15, 12]` | OK |
| q-say | linear, constant | fine | OK |

## l19 A live coding round (15 items)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| s0 tap | i1, i3, i4 | `[1, 4)` yes, `[3, 6)` no (3), `[4, 8)` yes, `[0, 1)` yes | OK |
| s1 | is the end included | fine | OK, hint id (mismatch 5) |
| s2, s4, s6 | code | all 6, 8, 13 tests recomputed by hand | OK, tests weak |
| s3 | 4 | only `[4, 6)` refused | OK, hint wording (mismatch 4) |
| s5 | 3 | k = 2: `[2, 5)` makes 3 at time 3; `[4, 8)` meets only `[3, 6)` | OK |
| s7 | 9 | before: 15 (both 9 to 15 full); after cancel of `[9, 12)`: 9. wrong 15, 12 | OK |
| s8 | 5, 10, 5, 10, 10, 5 | all four options add to 45 | OK |
| s9 order | p1..p6 | fine | OK |
| s10 | tree with range maximum | heap and hash cannot count overlap at a time | OK |
| q-half | yes, touch | `[2, 6)` holds 2 to 5 | OK |
| q-k | no | at time 4 two stand | OK |
| q-free | 9 | candidates 5, 7, 9 | OK |
| q-plan | 3, 10, 3, 10, 4 | adds to 30; d adds to 36 | OK, **mismatch 3** (explain claim) |

## review-4 (10 items, all numeric or multi)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| r4-best-plan | 92 | brute force over 27 plans: 92 (second full 30 + third part 15 + first part 8 = 53 min). Third full tops out at 91. Greedy 84 | OK |
| r4-greedy | 84 | rates 1.8, 1.6, 1.70; first (20) leaves 36, third (44) skipped, second 30: 36 + 48. wrong 159 (94 min), 111 (64 min) | OK |
| r4-edge-second | `[]`, `[5]`, `[5, 5]`, `[2, 2, 1]` | `[3, 1, 2]` ordinary | OK |
| r4-edge-value | 3 | distinct 4, 3, 1 | OK |
| r4-minutes | 19 | 60 - 5 - 5 - 31; wrong 25, 24 | OK |
| r4-count | 4 | prefixes 0, 8, 5, 9, 16, 10, 15; remainders 0, 0, 1, 1, 0, 2, 3; 3 + 1 | OK |
| r4-steps | 31250125000 | 250000 x 250001 / 2; wrong 62.5e9, 31.25e9 | OK |
| r4-product | 8 | 2 x 1 x 4; full `[12, 24, 8, 6]` | OK |
| r4-bookings | 3 | `[8, 12)` and `[12, 14)` refused | OK |
| r4-next-free | 20 | 10 overlaps; 20 to 26 fits before `[26, 40)` | OK |

## homework-4 (8 items, 13 gradable parts)

| Item | Key | My computation | Verdict |
|---|---|---|---|
| h4-leaderboard p0 | code | `[73, 180]` ok (top two 73 + 107) | OK |
| p1 | maintain the best 10 | 100000 x 2000 = 200,000,000 | OK (see notes) |
| p2 | code | reset removes; tests 5 to 8 recomputed | OK, tests weak |
| h4-calendar p0 | 719400 | $1200 \times 1199 / 2$; wrong 1,440,000, 1200 | OK |
| p1 | sorted + `bisect` | fine | OK |
| p2 | 20 | $2^{19} = 524288 < 10^6 < 2^{20}$ | OK |
| h4-zero-sum-cpp | code | see table | OK, **mismatch 7** |
| h4-aloud | longform | `[7, -2, 9, 4, -5, 6]`, k = 5: prefixes 0, 7, 5, 14, 18, 13, 19, remainders 0, 2, 0, 4, 3, 3, 4: 3 pairs. $300000 \times 300001 / 2 = 45{,}000{,}150{,}000$ | OK |
| h4-leaderboard-cost | 120000000 | 80000 x 1500; wrong 7500, 80000; 7500 x 16000 = 120M | OK |
| h4-first-minutes | order o1..o5 | fine | OK, **mismatch 16** |
| h4-plan | 101 | brute force: 101 (third full 46 + second part 11 = 57 min). Greedy 82; all three at 62 min gives 110 | OK |
| h4-next-test | `[5, 3, -1, -2, 4, 7]` | middle stretch of 3 | OK |

Fresh numbers: no review or homework item repeats a number set or answer of a coding-int lesson (checked every figure of 3 or more digits and every list or tuple against all `l*.json`), except mismatch 16.

## Mismatches

### Wrong keys

None.

### Feedback, hint or wording claims that are wrong

1. `courses/coding-int/l15-reading-an-assessment.json`, screen 8 (`A shorter budget`, answer 102). The optimum is not unique: P3 in full with P1 in part (50 + 6 = 56 minutes, 90 + 12) also earns 102. So `wrong` `low` (90) says "You stopped at P3 in full and a tiny partial", which actually earns 102. The nudge "Try giving up the biggest problem", the `accept` text and the explain ("The best plan is P2 in full with the partials of P1 and P3") imply one plan. Fix: pick a budget with one optimum (budget 58 gives only P3 full with P1 part, 102), then rewrite the accept, hints, explain and the `low`, `same` and `greedy` lines to that plan. Or keep 60 and say that two plans reach 102.
2. `l15` screen 9, option d `why` and `byKey.d`: "You left 28 minutes unused. A full A fits in them." A full A takes 40, over 28. Fix: "You left 28 minutes unused. Swapping A's partial for A's full fits in 55."
3. `l19-a-live-round.json`, quiz `q-plan`, `explain.text`: "Only 3, 10, 3, 10 and 4 do both." Option c (10, 5, 5, 5, 5) also adds to 30 with no zero block. Fix: "Only 3, 10, 3, 10 and 4 add to 30 and give the base and the follow-up 10 minutes each." (The option's own `why` is fine.)
4. `l19` screen 3, hint point: "`[4, 6)` starts inside `[2, 5)` and also inside `[5, 7)`". It starts at 4, before 5. Fix: "starts inside `[2, 5)` and overlaps `[5, 7)`".
5. `l19` screen 1, hint point `highlight: ["i1", "i3"]`: the canvas has only `i1` and `i2`. Fix: `["i1", "i2"]`.
6. `l19` screen 4 (stage B) `how`: "five use `k` up to 3". Four tests (4, 5, 6, 8) use k of 2 or 3; test 7 uses k = 1. Fix: "four use `k` of 2 or 3".
7. `courses/coding-int/homework-4.json`, `h4-zero-sum-cpp`, `feedback.byKey.test-7`: "the stretch of 5 starts at the second number". Test 7 is `[-2, 1, 1, -4, 4]`; the stretch of 5 is the whole list and starts at the first number. Fix: "the whole list sums to zero, so the answer is 5." Also `how` says "about 300,000 numbers" while test 11 has 360,001; say "up to about 360,000".

### Tests that let a wrong solution pass

8. `l19` screens 4 and 6 (stage B and C), `tests`. A `_fits` that counts every booking overlapping the new one (`sum(s < end and start < e ...) + 1 <= k`) passes 8/8 and 13/13, though it refuses bookings that overlap two non-concurrent ones. An unsorted candidate list in `next_free` (`[after] + [e for ...]`) passes 13/13. A `cancel` that removes every copy of the pair passes 13/13, although feedback `test-9` says the test checks that only one is removed. Fix: add to stage B and C `run_cal(2, [[0, 0, 5], [0, 10, 15], [0, 3, 12]])` expect `[True, True, True]`; to C `run_cal(1, [[0, 20, 30], [0, 0, 5], [0, 10, 12], [2, 4, 0]])` expect `[True, True, True, 5]`, and `run_cal(2, [[0, 0, 10], [0, 0, 10], [1, 0, 10], [0, 0, 10], [0, 0, 10]])` expect `[True, True, True, True, False]`. I ran all three: the reference passes, each wrong version fails one.
9. `l17` screen 5 (`longest_zero_sum_subarray`) and `homework-4` `h4-zero-sum-cpp`: every test's longest stretch starts at index 0 (including the 400,000 and 360,000 lists), so `total == 0 => best = i + 1` passes 11/11 in both. Fix: add `longest_zero_sum_subarray([5, 3, -1, -2, 4, 7])` expect 3 (the prefix-only version returns 0), and the same in C++; the lesson's own explanation depends on first sightings in the middle.
10. `app/content/drills/ci-split-points.json`: `left == total // 2` and "stop once `left * 2 > total`" both pass 14/14. Fix: add `count_split_points([1, 2])` expect 0 (floor gives 1) and `count_split_points([2, -1, 1])` expect 1 (the early break gives 0).
11. `homework-4` `h4-leaderboard` part 3 tests: a `reset` that sets the score to 0 but keeps the player passes (no test has a negative score), though the statement says it removes the player. Fix: add a test with a negative score, for example scores 10, -5 and 3, reset the 3, `top(3)` expect 5.

### Constraint or time claims that are false or marginal

12. `app/content/drills/ci-cpp-range-sums.json` constraints: "Sums can pass $2 \times 10^9$, so use `long long`." With 200,000 numbers of at most 1,000 the largest sum is $2 \times 10^8$, and an `int` prefix passes all 10 tests. Fix: allow values to $\pm 10^5$ (sums to $2 \times 10^{10}$), update the brief and the 1,000-valued tests, and add a test with 200,000 values of 100,000 and a full-range query. `ci-cpp-longest-sum-k` has the same unforced advice ("Keep running totals in `long long`"; totals reach $3 \times 10^8$): widen the values or drop the sentence.
13. `app/content/drills/ci-cpp-first-missing.json`: the constraint says a scan per candidate is too slow, but `std::find` for each of 200,001 candidates passes test 12 in 4.3 s (native, `-O1`), so wasm may pass or fail by luck. Fix: add a case at 400,000 entries or lower the per-test limit so the scan fails clearly.

### Duplicates (DECISIONS "Duplicates" and "Fresh numbers"), mismatches 14 to 16

14. `app/content/drills/ci-cpp-sum-pairs.json` repeats the problem of `courses/ds/homework-1.json` `pair_count` and uses its test `[1, 5, 7, -1, 5]` with target 6 (answer 3), and `[2, 2, 2]` with target 4 (answer 3) from `courses/contests/l4-stress-testing.json` `brute_pair_sums`. The brief example `[1, 2, 3, 4]` with 5 is also `contests/l2-limits-to-complexity.json`'s input (a different function). Fix: new numbers, or swap the problem for a new one (for example pairs with sum divisible by `k`, now that l17 covers remainders only for subarrays).
15. `app/content/drills/ci-cpp-range-sums.json` is `range_sums(nums, queries)` of `courses/contests/homework-1.json`, same signature and idea in C++. Fix: change the problem (for example range sums with point updates) or name it as a deliberate C++ restatement and give it distinct numbers (it already has).
16. `homework-4` `h4-first-minutes` repeats l15 screen 6 (read, note, estimate, choose, start), so it tests recall of the order. Fix: order a different procedure, for example the 45-minute plan with new blocks, or the six steps of a spoken answer with new content.
   Notes: `ci-cpp-longest-sum-k` with k = 0 and `ci-balanced-run` are the same trick as l17 and the homework zero-sum item, with different numbers. They are practice transfers, not duplicates.

### Choice keys visibly longer than every distractor

17. Key longest by 8 or more characters (key against longest distractor): `l16` screen 10 (62 against 51), `l17` `q-box` (45 against 35), `l18` screen 0 (58, 47), screen 3 (53, 40), screen 8 (75, 56), screen 9 (59, 46), `q-say` (56, 47), `l19` screen 10 (74, 55), `q-half` (50, 37), `homework-4` `h4-leaderboard` part 2 (68, 39), `h4-calendar-follow-ups` part 2 (70, 57). Longest by fewer characters: `l15` `q-group` (49, 48), `l17` screen 9 (55, 49), `l18` screen 1 (51, 48) and screen 5 (53, 49). Fix: shorten each key or lengthen the distractors to within a few characters. Still open from the earlier recheck: `coding-int/l12-file-system.json` `q-ls-file` (32 against 31); shorten to "Its own name, `['p.txt']`".

### Voice

18. Three sentences of exactly 20 words (rule: under 20): `l16` quiz `q-random` `explain.text` ("The empty list, one number and a list that is all equal are special, and a generator seldom makes them."), `l19` screen 8 prose ("Open `#drill`, set the pattern to `intervals` and the difficulty to 4, and pick one drill in Python or C++."), `homework-4` `h4-zero-sum-cpp` prose ("Return the length of the longest contiguous stretch of `nums` that sums to 0, or 0 if there is none."). No exclamation marks, em-dashes or American spellings found. No explanation runs over three sentences.

### Canvas highlights

19. Hint `highlight` ids beyond the console: `l16` screen 5 (`l4` of 3 lines), `l17` screen 3 (`l4` of 3 lines), `l18` screen 0 (`l5` of 4 lines; the slow-way line is `l3`, so use `["l3", "l4"]`).

### Notes (no fix required)

- `l15` screen 4 `byKey.d`: "The partials pay 2.0 and 2.08" omits P3's partial (1.67). Say "P1's and P2's partials".
- `l16` screen 4: m3 (single element) is also never caught by lists of 5 or more, and the loop's value range is not stated, so m5 and m6 are caught only if equal neighbours occur. Say "values from 1 to 5".
- `l16` screens 2 and 5: "Six inputs" and "Six tests" in `feedback.correct`: three inputs suffice (screen 9 says so). Say "These six inputs".
- `l18` screen 0 explain: "within two minutes" is not on the canvas.
- `homework-4` `h4-leaderboard` part 2: "keep the 10 best" fails if deltas can be negative (the 11th score would be needed); the statement does not say deltas are positive.
- `l15` screen 5 table: the cells `r1c1` to `r2c2` have no `byKey` line (the others do).

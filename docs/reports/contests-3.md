# contests level 3 (Common patterns): report

The original content agent stopped after writing and committing its six files, before it reported, and its scratchpad generators were lost. This report comes from a triage pass: every number was recomputed independently, every code screen was re-run against its starter, and a few small fixes were made. The level is kept.

## Files

All in `app/content/courses/contests/`. Skill `cn-patterns` for every lesson.

| File | Screens or items | Quiz | Code screens | Notes |
|---|---|---|---|---|
| `l9-constructive.json` | 10 screens (difficulty 1 to 3) | 4 | 2 (`no_adjacent` through `check_no_adjacent`; `fill_array` through `check_fill`) | `array` slider over $n$ = 1 to 8; two `console` pages; a trap on `permutations`; a transfer on slicing a parent order |
| `l10-greedy-proofs.json` | 11 screens | 4 | 3 (`max_non_overlapping`; `min_rooms`; `greedy_counterexample`) | `number-line` intervals with a three-rule slider; exchange argument as a `table`; touching ends both ways; coins 1, 3, 4 |
| `l11-bitmasks.json` | 11 screens | 4 | 3 (`best_subset`; `count_subsets_with_sum`; `popcounts`) | `grid` of masks for $n = 3$; `table` of four bit operations; the `1 << n - 1` trap; TSP states and meet in the middle as numeric screens |
| `l12-difference-arrays.json` | 10 screens | 4 | 2 (`apply_ranges` with a `_Counted` count; `max_coverage`) | `array` stepper over three updates; spare cell; 2D corners on a `grid`; positions from fills |
| `review-3.json` | 8 items: 2 at difficulty 2, 5 at 3, 1 at 4 | | 1 (`ring_string` through `check_ring`) | covers l9 to l12; one `place` item pairs five patterns (including BFS) with statements |
| `homework-3.json` | 8 items: 3 at difficulty 3, 4 at 4, 1 at 5 | | 3 (`fewest_alerts` d4, `spans` d4, `first_over_cap` d5) | one `order` item (the exchange proof, six lines); one `longform` (10-point rubric, full model answer); one numeric (bitmask DP states) and two choices |

Brief must-haves, all present: constructive checkers (any valid answer, `expect: "True"`); the three wrong greedy keys and the coin counterexample; the exchange argument; touching ends under both readings; submasks and $O(3^n)$; meet in the middle; the $n \le 16$ against $n \le 20$ note; the difference array with the spare cell, a `_Counted` test and a 2D screen; the homework stack, greedy and difference-array-plus-binary-search drills.

## Validator

`node tools/validate.mjs`: 0 errors overall. Warnings on my files, none blocking:
- Five "a ladder screen usually reuses the previous canvas kind" warnings: l9 s4 and s8; l11 s6 and s7; l12 s4 (a code ladder moves between console, array, table).
- One "a point hint usually highlights the canvas": l10 s7 (the trap's console has no line for amount 6).

## Playthrough

`--local-cdn <scratchpad>/pkgs`, run after the fixes below:

- l9-constructive: ok, 14 checks, quiz 4/4
- l10-greedy-proofs: ok, 15 checks, quiz 4/4
- l11-bitmasks: ok, 15 checks, quiz 4/4
- l12-difference-arrays: ok, 14 checks, quiz 4/4
- review-3: ok, 8 of 8 recorded
- homework-3: ok, 8 of 8 marked right, 36 of 36 marks
- The four lessons were also played with `--mobile` (390 px): all passed. Screenshots of the explore, grid, 2D and console screens were inspected and fit.

## Numbers checked

Each number was computed twice. First computation: CPython in `contests-3/verify.py`, with an algorithm different from the shipped solution and a brute force on every small case. Second: Pyodide 0.27.7 (the playthrough, and `contests-3/pyharness.py` under Node, which runs every solution against every hidden test: all pass).

**l9**
- Valid orders for $n = 4$: exactly 2 and 3 1 4 2 and 2 4 1 3. No order for $n = 2$ and 3, one for every other $n$ from 1 to 8 (all permutations tried). Of the six candidates in the hook, lines 2 and 4 are valid and the other four each hold a neighbouring pair that differs by 1.
- Problem F with $n = 3$, $k = 4$: sums 3 to 12, so 10 values of $s$ from 1 to 20. With $n = 4$, $k = 5$, only $s = 3$ of 1 to 3 fails; sums 4 to 20 all occur.
- Slicing 1,000 shares into 6 children of 100 to 250: schedules B and C pass, A, D and E fail.
- The three checkers (`check_no_adjacent`, `check_fill`, `check_ring`) accept exactly the valid answers: tried on every permutation for $n \le 7$, every list for small $n$ and $k$, every string over a, b, c for $n \le 6$.

**l10**
- Six meetings: best 3 (B, D, F); shortest first 2 (F, C); earliest start 1 (A); earliest finish 3; fewest rooms 3 (A, B, C at 4.5; no moment with four).
- Touching ends: 3 meetings, or 2 under the strict rule. Auction table: 4 filled; earliest start gives 3; order 1 blocks orders 2 to 5.
- 200,000 random meetings (`random.Random(2024)`, start up to $10^9$, length 1 to $10^6$): 11,256 kept, 144 rooms (max-disjoint by a bisect DP, rooms by a sweep and by a heap).
- Hand cases of both problems against a brute force over subsets.
- Coins 1, 3, 4: greedy first wrong at 6 (3 coins against 2); 7 and 8 are right. Coins 1, 5, 6: first wrong at 10 (5 against 2); 15 gives 5 against 3. Coins 1, 5, 10, 20, 25: first wrong at 40 (3 against 2).
- `greedy_counterexample`, seeds 1 to 4 with 200 trials: ([1, 4, 6], 8), ([1, 4, 5], 8), ([1, 4, 6], 9), ([1, 4, 6], 8); 10 trials with seed 1: None; with seed 2: ([1, 5, 7], 11); coins 1, 2, 5, 10, 300 trials: None. The first failure on seed 1 is ([1, 5, 8], 15), as the feedback says.
- Review: the six meetings table gives 4 (earliest start 2).

**l11**
- Four trades: best B and D, £11k at 6 units (all 16 subsets).
- Mask 10: `10 >> 1 & 1` = 1, `10 | 1 << 2` = 14, `10 & -10` = 2, popcount 2. `len(range(1 << 4 - 1))` = 8. Mask 13 = bits 0, 2, 3; mask 22 = bits 1, 2, 4; mask 10110 has 8 submasks.
- $n = 16$ size case: 5,895 at limit 400 (a risk-indexed knapsack DP) and 6,848 with no limit (sum of the profits).
- `count_subsets_with_sum`: 12 for [3, 1, 4, 1, 5, 9, 2, 6] at 10; 723 and 1 for the first 16-value list at 120 and 0; 1,324 for the signed list at 7 (dict DP and `itertools.combinations` agree).
- Popcounts for $n = 18$: length 262,144, sum 2,359,296 ($18 \cdot 2^{17}$), last 18.
- TSP states $2^{10} \cdot 10 = 10{,}240$; $9! = 362{,}880$; $2^{16} \cdot 16^2 = 16{,}777{,}216$; $2^{40} = 1.0995 \cdot 10^{12}$; two halves 2,097,152; 27 pairs for $n = 3$; $3^{16} = 43{,}046{,}721$; 63 backtests. Homework: $2^{12} \cdot 12 = 49{,}152$, $12! = 479{,}001{,}600$, 24,576.
- Pyodide speeds under Node (this sandbox, measured, quote as about): `best_subset` over $n = 16$ about 0.12 s, $n = 18$ about 0.55 s, $n = 20$ about 2.4 s; a meet-in-the-middle subset count at $n = 40$ about 2.1 s (CPython 1.7 s); `popcounts(18)` about 0.04 s. CPython: 0.05, 0.21, 1.0 s.

**l12**
- Hook: $10^5 \cdot 2 \cdot 10^5 = 2 \cdot 10^{10}$. The test 8 range loop: 5,000,805,623 additions (about $5 \cdot 10^9$). The `max_coverage` size case: total length 6,649,961,122, mean 66,499.6 (about $6.6 \cdot 10^9$ steps).
- Example: updates (1, 4, 3), (2, 6, 2), (5, 7, 1) on 8 days give 0, 3, 5, 5, 5, 3, 3, 1; difference cells 0, 3, 2, 0, 0, −2, 0, −2, −1; day 5 is 3.
- Test 8 checksum 404,786,420 (`random.Random(12)`, numpy cumulative sum). Coverage of the five windows: 1, 2, 3, 3, 3, 3, 3, 3, 2, 1, so 3. Size case 49,889 (`random.Random(13)`).
- 2D corners: +v, −v, −v, +v give a block of 1s only (checked with cumulative sums). Fills 300, −100, +200 give 400 at day 4. Quiz difference list 5, −2, 0, −5, 2, 0; day 2 is 3.
- Review: difference list 2, 0, 5, −6, 0, 0, −1, running totals 2, 2, 7, 1, 1, 1.

**Homework**
- `fewest_alerts` hand cases against a brute force over alert sets; size case 35,817 (`random.Random(31)`, a bisect DP on the dual: most disjoint closed windows).
- `spans`: the example 1, 1, 1, 2, 1, 4, 6 and the small cases by walking back; rising 200,000 closes sum to 20,000,100,000; random closes (`random.Random(33)`, values 1 to 1000) sum to 18,188,896.
- `first_over_cap`: hand cases by an incremental brute force; size cases (`random.Random(35)`) 36,515 at cap 100,000, 72,568 at 200,000 and −1 at $10^9$, each checked by evaluating prefix $k - 1$ (not over) and $k$ (over) with numpy.
- Derangement: no answer only for $n = 1$ (every $n$ to 7 by search); the reverse and pair swaps fail at $n = 3$.

## Starters and tests

- Every solution passes all hidden tests in CPython and in Pyodide (`pyharness.py`: slowest cases 0.4 s, 0.76 s, 0.79 s).
- The untouched starter now fails every test in all 14 code widgets (`harness.py starter`). Before the fixes it passed 5 cases (see below).
- Slow solutions are rejected, each by a timeout on the size case in CPython within 6 s (so slower still in Pyodide): `permutations` search, adding 1 at a time, an all-kept scan, an all-pairs room count, the range loop, a per-window scan of alerts, a walk-back `spans` and an $O(nq)$ cap search. Counting tests: a per-day scan reads 500,000 times against a limit of 2,500; a walk-back `spans` fails test 7.
- Common wrong solutions fail the intended test: sort by start or length, strict `>` (touching), end-after-start tie order, a missing or misplaced $-v$, `1 << n - 1`, `<` for `<=`, a skipped empty set, popping on `<` in `spans`, `>=` for `>` in the cap search.
- Constructive checkers accept any valid answer (exhaustive checks above) and reject every invalid one.
- Alternative correct solutions all pass (even and odd split, fair share, heap for rooms, accumulate, sparse events, stack with run lengths, bisect on `hi`).

## Fixes made

- l10 `greedy_counterexample`: tests 5 and 7 expect `None`, which the starter returned. They now call a prelude helper `trials_run`, expect `(None, 10)` and `(None, 300)`, and also count the calls to `gen`. `how` and the two feedback lines say so.
- l11 `popcounts` test 8 (a source check) passed on the starter. It now also needs `popcounts(3)` right.
- l12 `apply_ranges` test 7 and homework `spans` test 7 (counting) passed on the starter with 0 reads. They now read `0 < reads <= bound`.
- l11 timings re-measured and the lesson text corrected: $n = 16$ "about 0.2 s" became about 0.1 s, $n = 20$ "about 3 s" became about 2.5 s, meet in the middle "about 1.5 s" became about 2 s.
- Voice: three sentences over 20 words in the homework `longform` (the prompt and two lines of the model answer) were split. Three `how` lines that said "each checked against a brute force" now say the expected answers come from one.
- Nothing else was changed. No graded answer value (numeric, choice, order, place) changed; four hidden-test expressions were tightened as above.

## Seeds and generators in the files

- l10: `random.Random(2024)` for the 200,000 meetings (shared by `max_non_overlapping` and `min_rooms`); the coin generators `gen_coins` (two coins from 2 to 9 plus 1, amount 1 to 20) and `gen_canonical` are in the prelude.
- l11: two fixed 16-value lists for `best_subset`; fixed 16-value lists for the subset counts.
- l12: `random.Random(7)` (counting case, 500 updates over 1,000 days), `Random(12)` (test 8), `Random(13)` (coverage).
- Homework: `Random(31)` windows, `Random(33)` closes, `Random(35)` updates.
- The scratchpad scripts (`verify.py`, `harness.py`, `slow.py`, `wrongs.py`, `alts.py`, `checkers.py`, `speed.py`, `voice.py`) are in `contests-3`; they are not part of the app.

## Open issues

- A numpy slice loop (`a[l:r + 1] += v`) passes l12's size case in about 0.8 s in CPython, since imports of numpy get extra time. The course is pure Python; see the backlog bullet.
- `min_rooms` by assigning meetings to the first free room costs $n$ times the peak (144), about $3 \cdot 10^7$ steps, so it passes the size case. It is a correct solution, not a failure.
- No `course.json` change proposed.
- Three engine bullets were added to `docs/BACKLOG-INBOX.md` under "Raised later (contests level 3)".

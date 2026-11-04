# Answer check, 4 November 2026: systems level 4

**Summary.** 81 items checked: lessons l15 (16), l16 (16), l17 (16), l18 (15), `review-4` (9), `homework-4` (6, with 13 parts and a long-form) and the three drills (3, 29 hidden tests). Every keyed number, table cell, tap set, order, choice key and `wrong` value recomputed independently. Wrong keys: 0. 10 C++ items, 1 Python item and 3 drills run against their hidden tests: every reference passes, every starter fails. About 100 plausible wrong solutions written: 25 pass every hidden test. 10 of those show a real gap (a wrong idea the tests do not catch), listed below; the rest pass legitimately. Other mismatches: 1 count that depends on wording, 1 hollow claim, 2 near duplicates, 2 borderline choice keys.

Scripts are in the scratchpad folder `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/answers-systems-4/`:

- `runcpp.py` builds a test program from a widget's `prelude`, source, `postlude`, `setup` and `call` (with `alloc_count()` and `-fno-builtin` where `allocCheck` is on) and compiles it with `g++ -O1 -fno-exceptions -std=c++17`.
- `runall.py` runs every reference and starter. `variants.py`, `variants2.py`, `variants3.py` and `variants4.py` hold the wrong solutions.
- `dump.py` prints each item without canvases. `voice.py` checks voice. Other checks were short inline scripts.

Voice check (em-dashes, exclamation marks, American spellings, sentences over 20 words, explanations over 3 sentences) over every text field in the nine files: no hits. Validation: 0 errors.

## Items, keys and verdicts

All verdicts are OK unless a row says otherwise.

### l15 No allocation on the hot path

| Item | Key | Computation | Verdict |
|---|---|---|---|
| Tap the allocations | l3, l4, l5, l6 | line 3 first push, 4 `new`, 5 100 chars past the small string, 6 map node. Line 2 empty vector owns nothing | OK |
| What one allocation costs | 10 ms; wrongs 10000, 50 | 50 ns x 200,000 = 10,000,000 ns = 10 ms = 10,000 us | OK |
| Four allocations | 200, 40, 4 | 4 x 50; 200 x 200,000 = 40 ms; 40/1000 | OK |
| A pool of slots | c0 | free list 0 -> 2 -> 3, head 0 | OK |
| What a pool saves | 30, 1.2, 25 | 600,000 x 50 ns; x 2 ns; 30/1.2 | OK |
| Count the heap (code) | 9 tests | reference 9 of 9, starter 3 of 9 | OK, see gap 1 |
| Which one allocates | push | only the first push | OK |
| When the pool runs out | minus | the other three each allocate or share | OK |
| Allocate first | before | | OK |
| Write the pool (code) | 10 tests | reference 10 of 10, starter 3 of 10 | OK |
| Drill by hand | 1, 2, -1, 1 | free-list stack: release 1; release 0 then 2; empty; release 3,1,2 gives 2,1,3 | OK |
| How big a pool | 1500, 36000, 48000, 25 | 1000 x 1.5; x 24; x 32; 1 - 24/32. 36000/1024 = 35.2 KiB, 48000/1024 = 46.9 KiB; both over 32,768 | OK |
| q15-cost | 37.5 | 250 ns x 150,000; wrong 37500 | OK |
| q15-reserve | no | `reserve` keeps capacity, `clear` keeps it | OK |
| q15-pool | 0; wrong 3 | release 3 then 0: head 0 | OK |
| q15-size | 24000; wrongs 1200, 16000 | 800 x 1.5 = 1200; x 20; 800 x 20 = 16000 | OK |

### l16 A ring buffer

| Item | Key | Computation | Verdict |
|---|---|---|---|
| Fill a ring of four | 5, 3 | frames re-read: fifth push refused, third pop 3 | OK |
| From counter to slot | 1, 7, 4 | 5 & 3; 20 - 13; 20 & 7. Stored slots 5 to 7 and 0 to 3 = 7 | OK |
| When the counters wrap | 1, 0, 0, 429.5 | 2^32 - 4 is a multiple of 4, so 4294967293 & 3 = 1. 2^32 mod 3 = 1, so 4294967295 mod 3 = 0. 2^32/10^7 = 429.4967, tol 0.05. Console slot columns recomputed (2,3,0,1 and 2,0,0,1) | OK |
| Two counters, one line | row1 | `row1` is a valid grid id (README). Head col 5, tail col 6, line 2 empty | OK |
| What the line costs | 600, 10 | 10^7 x 60 ns; x 1 ns | OK |
| The producer's push | s1..s5 | s1 before s2 (uses `t`), s3 uses `t`, s4 after s3: one valid order | OK |
| Does it need a lock | no | | OK |
| The full ring | 4; wrongs 0, 3 | 11 - 7 = 4; 7 & 3 = 11 & 3 = 3 | OK |
| Full | diff | | OK |
| Write the ring (code) | 10 tests | reference 10 of 10, starter 3 of 10 | OK, see gap 2 |
| Drill by hand | 0, 7, 13, 3 | 45 & 15 = 13 | OK |
| Size the ring | 200, 256, 6144, 8192 | 200,000 x 0.001; next power of two; 256 x 24; 5,000 -> 8192. 8192 x 24 = 192 KiB | OK |
| q16-slot | 13; wrong 2 | 50 - 37; 50 & 15 = 2 | OK |
| q16-pow2, q16-owner | mask, consumer | | OK |
| q16-stall | 2048; wrong 2000 | 0.005 x 400,000 = 2000 | OK |

### l17 Measuring latency

| Item | Key | Computation | Verdict |
|---|---|---|---|
| The average request | 19.9, 0 | (990 x 10 + 10 x 1000)/1000 | OK |
| Slide the slow requests | 11; wrongs 10, 1 | 989 fast puts position 990 in the slow group. Mean at 11 = 20.89 ("20.9") | OK |
| Read the percentiles | 10, 10, 1000, 10 | positions 500, 990, 999; one slow: p99.9 position 999 is fast | OK |
| Who waited | intended | CSV recomputed (below) | OK, see mismatch 1 |
| Measure it both ways (Python) | 7 tests | I recomputed from `latencies.csv` with Fractions: p50/p99/p99.9 sent 40/50/248, true 49/48,821/49,911, mean 10,584.622. Reference passes 7 of 7, starter fails | OK, see gap 3 |
| Quote the mean or the tail | both | | OK |
| The rank at the edge | 10; wrong 1000 | in doubles `99.9/100*1000` = 999.0000000000001 and `0.999*1000` = 999.0, both as stated. `np.percentile(..., 99.9, method="inverted_cdf")` gives 1000 on NumPy 2.5.3. I could not install 2.0.2 (no wheel for this Python), but 2.0.2 divides q by 100 first, the same arithmetic | OK, 2.0.2 not run |
| Nearest rank | r38 | 0.95 x 40 = 38 | OK |
| Write the percentile (code) | 13 tests | reference 13 of 13, starter 6 of 13 | OK, see gap 4, mismatch 2 |
| Timing a small thing | 80, 0.04 | 40/50; 40/1000 | OK |
| Drill percentiles | 1, 3, 4, 5 | ceil(1), ceil(2.5), ceil(4), 5 | OK |
| Fleet p99 | 1000, 505, 1000 | B: 970 fast, position 990 slow; (10 + 1000)/2; pooled 1970 fast, position 1980 slow | OK |
| q17-rank | 8; wrong 7 | ceil(7.5) | OK |
| q17-closed, q17-batch | hidden, batch | | OK |
| q17-mean | 39; wrong 210 | (1900 + 2000)/100; (20 + 400)/2 | OK |

### l18 Designing a feed handler

| Item | Key | Computation | Verdict |
|---|---|---|---|
| Packet in, order out | s1..s6 | s2 before s3 before s4: one order | OK |
| Where the time goes | 40; wrongs 33.3, 0.4 | 1000/2500; 1000/3000. Running totals 1000, 1200, 1500, 2000, 2500 | OK |
| A time budget | 2500, 500, 2700, 7500 | sum; 3000 - 2500; + 4 x 50; + 5000 | OK |
| Arrays for the book | 201, 1608, 16384, 18032 | 10100 - 9900 + 1; 201 x 2 x 4; 1024 x 16; sum + 40 | OK |
| Two feeds, one stream | c0, c2, c4, c7 | replayed: 1A, 2A, 4A (gap 1), 5A; 3B < 5 | OK |
| A map for the orders | nodes | | OK |
| Frames in pieces | 2, 2, 1, 4 | 50 = 2 x 24 + 2; 42 -> 1 + 18; 98 -> 4 + 2. Seven in all | OK |
| Pipeline with a budget | gap | | OK |
| Build the handler (code) | 14 tests | reference 14 of 14, starter 3 of 14 | OK, see gaps 5 to 7 |
| Drill budget and bytes | 2000, 2150, 3.6, 37, 12 | sum; + 150; 150,000 x 24 = 3.6 MB; 900/24 = 37.5; 900 - 888 | OK |
| Fifty instruments | 901600, 880.5, 28 | 50 x 18032; /1024 = 880.469 (tol 0.05); /32768 = 27.51 | OK |
| q18-budget | 1500; wrong 600 | | OK |
| q18-gap | 4; wrong 5 | 14 - 10 | OK |
| q18-orders | 32768; wrong 2048 | 2048 x 16 | OK |
| q18-stale | drop | | OK, see mismatch 5 |

### review-4

| Item | Key | Computation | Verdict |
|---|---|---|---|
| r4-allocating-lines | emplace, new, string | first push; `new`; 64 chars past the small string | OK |
| r4-pool-order | 1; wrongs 2, 3 | release 2, 3, 1: head 1 | OK |
| r4-alloc-bill | 18; wrong 18000 | 3 x 50 = 150 ns x 120,000 = 18 ms | OK |
| r4-ring-counters | 15, 21 | 85 - 70; 85 & 31 = 21 | OK |
| r4-ring-order | 40; wrongs 30, 10 | pops 10, 20, 40 | OK |
| r4-mean-p99 | 26.64, 500 | (970 x 12 + 30 x 500)/1000 = 26.64; position 990 slow | OK, see mismatch 3 |
| r4-p60 | 6; wrongs 5, 7 | sorted 1,2,3,5,6,7,8,9; ceil(4.8) = 5 holds 6; rank 4 holds 5; rank 6 holds 7 | OK |
| r4-budget | 2900; wrong 2600 | 900 + 250 + 400 + 600 + 450 = 2600; + 300 | OK |
| r4-two-reads | 3; wrong 2 | 31 + 41 = 72 = 3 x 24 | OK |

### homework-4

| Item | Key | Computation | Verdict |
|---|---|---|---|
| h4-latency-hist (code) | 12 tests | reference 12 of 12, starter 2 of 12. Expected values re-derived by hand (bucket 3 -> 16, bucket 9 -> 1024, bucket 6 -> 128, bucket 19 -> 1,048,576) | OK, see gap 8, mismatch 3 |
| h4-sizing | 3000, 60000, 512, 12288, ring | 2400 x 1.25; x 20; 300 -> 512; x 24; 60000 - 32768 = 27232; 72288 - 32768 = 39520 | OK |
| h4-handler-aloud | rubric 2+2+2+2+1+1 | model figures: 1200 + 250 + 350 + 600 + 600 = 3000, slack 1000 of 4000; 401 levels for a 400-penny range | OK |
| h4-two-hosts | 410, 800, 20, pool | (20 + 800)/2; 1960 fast, position 1980 slow; 1985 fast, position 1980 fast; 15/2000 = 0.75% | OK |
| h4-pop-order | s1..s5 | one valid order | OK |
| h4-stall-count | 160; wrongs 40, 40000 | 40,000/250 | OK |

### Drills

| Drill | Result |
|---|---|
| sy-lru-cache | reference 7 of 7, starter 2 of 7. Expected arrays traced by hand for tests 1, 3, 5, 7 |
| sy-token-bucket | reference 7 of 7, starter 3 of 7. Tests 3, 4, 6 traced by hand in billionths |
| sy-bits | reference 15 of 15, starter 5 of 15. 0x12345678 -> 0x78563412 = 2018915346; 0xFF00 -> 0x00FF0000 = 16711680 |

## Wrong solutions that pass every hidden test

These are the gaps. Each wrong idea compiled and passed all tests. "Add" is a test that catches it, run against the reference to confirm the expected value.

| # | File and item | Wrong solution that passes | Add |
|---|---|---|---|
| 1 | `l15` Count the heap | No `'\0'` written after the text, although the brief requires it. No test reads `buf[n]` | `char buf[32]; memset(buf, 'x', 32); int n = format_price(buf, 5);` call `buf[n]`, expect 0 |
| 2 | `l16` Write the ring | None found. The tests catch a wrong mask, N+1 items, one `alignas`, reversed order and a missing empty check. Modulo and padding variants pass legitimately | none |
| 3 | `l17` Measure it both ways | `numpy.percentile(..., method="lower")`, `"nearest"` and a rounding rank all pass, because this file's ranks land on whole numbers or the values coincide. Float `ceil(p * n / 100)` passes too (99.9 x 2000 / 100 is exactly 1998.0) | A second data file, or a hidden row set where `p * n / 100` is not whole. The float trap of the screen "The rank at the edge" is never tested in Python |
| 4 | `l17` Write the percentile | (a) Rounding to nearest, `floor(p * n / 100 + 0.5)`. (b) No `1e-9` guard, `ceil(p * n / 100.0)` | (a) `{5,1,4,2,3,7,6}`, p30: rank ceil(2.1) = 3, value 3 (rounding gives 2). (b) 250 samples 1 to 250, p64.4: `64.4 * 250 / 100` = 161.00000000000003, so the unguarded rank is 162, the exact rank 161, expect 161 |
| 5 | `l18` Build the handler | After a gap, `expected_ = expected_ + 1` instead of `seq + 1`. Tests send nothing after a gap | frames seq 1, 2, 5, 6: `gaps()` is 2 (the wrong handler gives 4) |
| 6 | `l18` Build the handler | A `T` with qty above the resting qty, with no `min`: the level underflows. No test trades more than is resting | add 100 at 10000, `T` qty 150: `bid_qty(10000)` expect 0, `best_bid()` expect 0 |
| 7 | `l18` Build the handler | `X` for an unknown or dead order with no `live` check: index `-9900` write. Passes only because the test reads `best_bid()`, and out-of-bounds writes may not crash natively. In wasm it may crash or not | `X` of id 9 then `bid_qty(10000)` on a handler holding a live order there: expect unchanged |
| 8 | `h4-latency-hist` | (a) Rounding rank. (b) No `1e-9` guard. (c) Nothing above bucket 39 tested | (a) ten-sample ladder 1 to 10, p31: rank 4 holds 4, bucket upper 8 (rounding gives rank 3, upper 4). (b) 161 samples of 10 and 89 of 1000, p64.4: expect 16 (no guard gives 1024) |
| 9 | `sy-token-bucket` | Clock updated only on an allowed call, so refill is counted twice for refused calls. The cap hides it in every test | `drive(1000, 5, {0,0,0,0,0,500000,600000})` expect `{1,1,1,1,1,0,0}` (the wrong one gives a 1 at the last call) |
| 10 | `sy-token-bucket` | Floating point: four `double` variants (token count in doubles, `dt * rate / 1e9`, `dt / (1e9 / rate)`, a `1e-9` epsilon) pass all 7 tests, although the constraint says not to use it and the hint says a slip shows after many calls. I also fuzzed 20,000 random call sequences: doubles never differed from exact | Either drop the claim "a rounding slip shows up after many calls", or add a test that makes a double fail (I could not find one) |
| 11 | `sy-bits` | `is_pow2` through a signed int (`(int)x > 0`) passes; `bswap32` through a signed int with arithmetic `>> 24` and no mask passes. Every `bswap32` input has the top bit clear and no `is_pow2` input is 2^31 | `is_pow2(2147483648u)` true; `(long long)bswap32(4026531841u)` (0xF0000001) expect 16777456 |
| 12 | `sy-lru-cache` | None found. Evict-before-insert, a vector-scan version and no capacity-0 guard pass legitimately | none |

Caught by the tests (checked, no action): ring with N+1 items, `mask = capacity`, wrapped indexes, one `alignas`, tail before head, no empty check; pool with FIFO release, a `std::list` free list (allocates on release), a missing `in_use` decrement, `head_ = 0` for a pool of 0; `format_price` with a vector, `new[]`, a padded `std::string`, naive `snprintf` for negatives; percentile floor+1, linear interpolation, descending sort, no p0 clamp, `ceil(p / 100 * n)`; handler without range checks (crash), copying the byte vector, an `unordered_map` of orders, a dropped partial frame, little-endian reads, a cached best bid; histogram upper bound versus lower bound, `seen > rank`, a sample vector; LRU without recency on `get` or `put`, evicting the front, not erasing the map entry; token bucket with integer division, no cap, a cap after the spend, an empty start; bits `next_pow2` without the `x - 1` smear, `is_pow2` without the zero test, a wrong byte mask.

## Numbered mismatches

None of these is a wrong key.

1. `app/content/courses/systems/l17-measuring-latency.json`, screen "Who waited" (console line `875 of 2,000 late by over 100 us` and the `noise` feedback "875 requests were late by over 100 µs"). From the CSV: 875 requests have a done-minus-intended time over 100 us, and 875 have a send later than intended, but only 850 sent more than 100 us late. "Late by over 100" reads as the 850. Fix: say "875 of 2,000 took over 100 us from their due time", or "875 of 2,000 sent late".
2. `l17-measuring-latency.json`, screen "Write the percentile" (prose and starter comment: "Subtract 1e-9 before the ceil, so 99 x 1,000 / 100 does not round up"). `99 * 1000 / 100.0` is exactly 990 in a double, so no guard is needed for that example, and no test needs the guard (gap 4b). Fix: use a case that does need it, for example 64.4 x 250 / 100 = 161.00000000000003, and add it as a test.
3. Duplicates (DECISIONS "Fresh numbers" and "Duplicates"): `review-4.json` `r4-mean-p99` (1,000 requests, 970 fast and 30 slow) and `homework-4.json` `h4-latency-hist` (tests built from 970 x 10 and 30 x 1000) reuse the host B mix of the l17 transfer "Follow-up: the fleet p99" (970 at 10 us, 30 at 1,000 us, p99 1,000). `r4-mean-p99` changes the values (12 and 500) but keeps both counts. Fix: use other counts in `r4-mean-p99` (for example 940 and 60 with p99 at position 990 still slow, or 985 and 15 with a fast p99) and other values and counts in the hist tests.
4. `app/content/drills/sy-lru-cache.json`, test 3 (`drive(2, {p 1 1, p 2 2, p 1 9, p 3 3, g 1, g 2, g 3})` expecting `[9, -1, 3]`) has the same shape as a test in `app/content/courses/coding-int/l11-lru-cache.json` (`[2, [[0,1,1],[0,2,2],[0,1,5],[0,3,3],[1,1],[1,2],[1,3]]]` expecting `[5, -1, 3]`): the same capacity, keys and order, one value changed. Fix: change the keys and the capacity, for example capacity 3 with an update of the middle key. (`sy-token-bucket` test 4, `drive(2, 2, {0,0,0,...})`, shares only the first three calls and the pair 2, 2 with a coding-int l14 test; times differ, so no change needed.)
5. Borderline choice keys, longest option of the set: `l17` `q17-closed` key 44 characters against 39 for the longest distractor, `l18` `q18-stale` key 49 against 44. Both are under the 1.4 ratio of the 14-item rebalance, so low priority. Fix: lengthen one distractor in each, for example "Half of them, as slow requests, with the tail left clean".
6. Gaps 1, 3, 4, 5, 6, 7, 8, 9 and 11 above: tests to add as listed (each added test was run: the reference passes and the wrong solution fails). Gap 10 (`sy-token-bucket`): drop the claim "a rounding slip shows up after many calls" from the constraint, or find a test that makes a double fail.

Wrong keys: 0.

## Fix pass

Ran from the worktree. Scripts: `.../scratchpad/answers-systems-4/` (`apply.py`, `apply2.py` edit the JSON; `verify.py`, `verify2.py` run the references, starters and wrong solutions with `g++ -O1 -fno-exceptions -std=c++17`; `pytest17.py` runs the Python variants; `tb.py` searches for a double that slips). Gaps 1 and 3 to 11 fixed, gap 2 and 12 had none. Mismatches 1 to 5 fixed, plus the two items from `recheck-2026-11-04-a.md`. Disputed: 0. Deferred: 0.

### Gaps

- Gap 1 (`l15` Count the heap): FIXED. New test 9 of 10: `char buf[32]; for (int i = 0; i < 32; ++i) buf[i] = 'x'; int n = format_price(buf, 5);` call `(int)buf[n]`, expect 0. Hand check: "0.05" has 4 characters, so `buf[4]` is the terminator. The no-NUL solution fails test 9 only; reference 10 of 10, starter 4 of 10. `how` now says ten tests.
- Gap 3 (`l17` Measure it both ways): FIXED. Four tests (8 to 11) write small files in `setup`: row i has `done - sent = (37 i mod n) + 10`, `sent = intended`. 37 is coprime to 77, 78 and 1,000, so the latencies are 10 to n + 9, each once, and rank r holds r + 9. Test 8 `h77.csv` p99 expects 86 (rank ceil(76.23) = 77, 77 + 9). Test 9 `h77.csv` p99.9 expects 86 (rank ceil(76.923) = 77). Test 10 `h1000.csv` p99.9 expects 1008 (rank 999). Test 11 `h78.csv` p50 expects 48 (rank 39). Second check: sorted values 10..86, last = 86; 1000 rows, 999th = 1008; 78 rows, 39th = 48. Plain Python harness, 11 tests: reference 11 of 11. Fail: rounding rank (test 8), `ceil(p / 100 * n)` (tests 3, 6, 9), `floor(p n / 1000)` (tests 8, 9), `s[n // 2]` for p50 (test 11), NumPy `lower`, `nearest`, `higher`, `linear`, `closest_observation`, `interpolated_inverted_cdf`, and `inverted_cdf` (tests 3, 6, 9; NumPy 2.5.3 here, 2.0.2 divides q by 100 first, same arithmetic). Still pass, and correctly: `ceil(p * n / 100)` and `ceil(permille * 0.001 * n)`. I checked n = 1 to 20,000 for p50, p99 and p99.9: both equal the exact rank every time, so no test can fail them for these three percentiles. `how` updated.
- Gap 4 (`l17` Write the percentile): FIXED. Test 13 `{5,1,4,2,3,7,6}` p30 expect 3 (ceil(2.1) = 3; sorted 1..7). Test 14 samples 1 to 250, p64.4 expect 161 (64.4 x 250 / 100 = 161 exactly; the double is 161.00000000000003, so the unguarded rank is 162). Rounding rank fails test 13; no guard fails test 14; `ceil(p / 100 * n)` fails test 6. Reference 15 of 15, starter 6 of 15. A guard of 1e-12 passes (correct).
- Gap 5 (`l18`): FIXED. Test 6 now sends seq 1, 2, 5, 6 (id 4 added); `gaps()` stays 2 (5 - 3 = 2, then 6 is next). `expected_ + 1` gives 4 and fails test 6 only.
- Gap 6 (`l18`): FIXED. Test 5 trade changed from qty 100 to qty 150 against 100 resting; `best_bid()` stays 0. The trade without `min` fails test 5 only.
- Gap 7 (`l18`): FIXED. New test 15: add 100 and 40 at 10000, cancel id 1 twice; `bid_qty(10000)` expects 40 (100 + 40 - 100). The `X` without a live check subtracts 100 again and fails test 15 only. My own correction to the checker's suggestion: a cancel of an unknown id subtracts `o.qty` = 0, so only a double cancel shows the gap. `how` now says fifteen tests. Reference 15 of 15, starter 3 of 15.
- Gap 8 (`h4-latency-hist`): FIXED for (a) and (b). Test 7: ladder 1 to 10, p31 expect 8 (ceil(3.1) = 4, value 4, bucket 2, upper 8; rounding gives rank 3, upper 4). Test 8: 161 samples of 10 and 89 of 1000, p64.4 expect 16 (rank 161 is a 10, bucket 3; unguarded rank 162 gives 1024). Rounding fails test 7, no guard fails test 8. (c) Test 9: one sample of 2^45 = 35,184,372,088,832, p100 expect 2^40 = 1,099,511,627,776. "Drop above 39" fails test 9. A solution with no clamp writes past the array, which is undefined: it passes natively here, so test 9 cannot be relied on to catch it.
- Gap 9 (`sy-token-bucket`): FIXED. Test 8: `drive(1000, 5, {0,0,0,0,0,500000,600000})` expect `{1,1,1,1,1,0,0}`. Five spent at 0; 0.5 token at 500,000 ns; 0.6 token at 600,000 ns, both refused. A clock that moves only on allowed calls counts 0.5 + 0.6 = 1.1 and allows the last. It fails tests 8 and 9.
- Gap 10 (`sy-token-bucket`): FIXED by a test that makes a double fail. Test 9: `drive(1, 1, {0, 1e8, 2e8, ..., 1.1e9})` (12 calls, 0.1 s apart) expect `{1,0,0,0,0,0,0,0,0,0,1,0}`. In billionths: one token at t = 0, back after 1,000,000,000 units = call 11 (index 10). In doubles ten additions of 0.1 give 0.9999999999999999, so the call at index 10 is refused and index 11 is allowed. Three double variants (`dt * rate / 1e9`, `dt / 1e9 * rate`, `dt / (1e9 / rate)`) fail test 9. A `tok + 1e-9 < 1` epsilon variant still passes: it is a double that happens to be right on this input. The constraint now reads "ten refills of 0.1 of a token do not add up to exactly 1". Reference 9 of 9, starter 4 of 9.
- Gap 11 (`sy-bits`): FIXED, within the 15-test cap by replacing two tests that `bswap32(305419896u)` already covers. `bswap32(1u)` became `(long long)bswap32(4026531841u)` expect 16777456 (0xF0000001 to 0x010000F0: 0x010000F0 = 16,777,216 + 240). `bswap32(65280u)` became `is_pow2(2147483648u)` expect true. Signed `is_pow2` fails test 15; signed `bswap32` with no mask fails test 13; with a 0xFF mask it passes (correct). Reference 15 of 15, starter 6 of 15.

Wrong solutions from the checker now failing: every one listed in gaps 1, 3 to 11 except the undefined no-clamp histogram variant. Correct-equivalent ones still passing: `ceil(p n / 100)` in Python for p50, p99, p99.9; 1e-12 guard; 0xFF-masked signed `bswap32`; epsilon double bucket.

### Mismatches

1. `l17` "Who waited": console line `875 of 2,000 late by over 100 us` is now `875 of 2,000 sent late`; `noise` feedback now "875 requests were sent late. That is not one outlier." Check from `latencies.csv`: sent later than intended 875, done minus intended over 100 us 875, sent more than 100 us late 850. Computed twice (counting rows, and the same with `csv.DictReader` columns): 875 each. The `why` "Delayed requests number 875" is unchanged and true.
2. `l17` "Write the percentile": prose and starter comment now use 64.4 x 250 / 100 (Python `repr` 161.00000000000003, C++ `%.17g` 161.00000000000003, `ceil` 162 against 161 with the guard). Old: "99 x 1,000 / 100 does not round up" (exactly 990.0 in a double).
3. Fresh numbers. `r4-mean-p99`: old 970 at 12 us and 30 at 500 us (mean 26.64, p99 500). New 940 at 15 us and 60 at 400 us. Mean: (940 x 15 + 60 x 400) / 1,000 = (14,100 + 24,000) / 1,000 = 38.1; second way 15 + 0.06 x (400 - 15) = 15 + 23.1 = 38.1. Fast positions 1 to 940, so position 990 is slow, p99 = 400. Key answers 38.1 (tol 0.005) and 400; `correct`, `byKey` and `explain` rewritten to match. Neither 38,100 nor 38.1 us appears elsewhere in `systems`. `h4-latency-hist` mix: old 970 at 10 and 30 at 1000 (p50 16, p97 16, p98 1024). New 920 at 6 ns and 80 at 3,000 ns, p50 8, p92 8, p93 4096 (6 is bucket 2, upper 8; 3,000 is bucket 11 since 2,048 <= 3,000 < 4,096; rank for p92 is 920, for p93 930). Second way: 920 / 1,000 = 92%. Tests 1 to 3 changed; `how` updated.
4. LRU drill test 3: old `drive(2, {p 1 1, p 2 2, p 1 9, p 3 3, g 1, g 2, g 3})` expect `[9, -1, 3]`. New `drive(3, {p 4 40, p 5 50, p 6 60, p 4 44, p 7 70, g 4, g 5, g 6, g 7})` expect `[44, -1, 60, 70]`. Trace: after 4, 5, 6 the order is 6, 5, 4; updating 4 makes 4, 6, 5; adding 7 drops 5. Second way: recency list ends with 5, the only key missing. A put that does not count as a use drops 4 and fails test 3 only; no recency on `get` fails tests 1 and 5.
5. Borderline keys: `q17-closed` option `half` "Half of them, as slow requests" (30) is now "Half of them, recorded as slow requests in the report" (53); the key (44) is no longer the longest. `q18-stale` option `wait` "It holds the frame until 8 arrives" is now "It holds the frame back until the missing 8 arrives" (51); the key (49) is no longer the longest. From the recheck: `review-3` `r3-handshake` `feedback.correct` "60 ms." is now "54 ms." (3 x 18 = 54; RTT 36, one way 18). `l13` "What a gap is" key "Nothing: it is already held" (27, longest by one) is now "Nothing: it is held" (19).

### Results

Validator: 0 errors. Playthrough with `--local-cdn`, with and without `--mobile`: lessons l13, l15, l17, l18; sets `review-3`, `review-4`, `homework-4`; `--drills`: all passed. Graded answers changed: `r4-mean-p99` (26.64 and 500 to 38.1 and 400) and the three `h4-latency-hist` tests 1 to 3, plus new tests.

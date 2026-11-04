# Answer check, coding-int level 3 (4 November 2026)

**Summary.** 77 items checked: lessons l11 to l14 (43 screens, 16 quiz items), `review-3.json` (10) and `homework-3.json` (8 items, 10 parts). Wrong keys: 0. Every keyed answer, tolerance and quoted figure was recomputed in my own code; all 12 code widgets (10 Python, 1 C++, plus homework) pass their reference solution and the starters fail. Mismatches: 3 wrong-value distractors, 4 hidden-test gaps (a wrong solution passes), 2 canvas contradictions, 4 repeats of lesson content, plus notes.

Method. I read no author report until my numbers were done. Scripts are in `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/answers-coding-3/`:

- `codecheck.py` runs each Python widget's solution and starter against every hidden test and example.
- `nums.py` holds independent simulators (LRU, TTL, ledger by lots, sliding log, token bucket, LFU) for every numeric key and `wrong` value.
- `mut1.py`, `mut2.py`, `mut3.py` run wrong solutions (about 45 mutants) against the hidden tests.
- `cpp_sol.cpp` and `cpp_starter.cpp` are the C++ screen compiled with `g++ -O1 -fno-exceptions`.
- `voice.py` scans voice and choice-key length.

## Code widgets

| Screen | Solution | Starter | Wrong solutions tried (all caught unless listed under Mismatches) |
|---|---|---|---|
| l11 s2 LRU Python (8 tests) | 8/8 | fails 6, passes t5, t8 | get no refresh, update no refresh. **Passes: evict-first, O(capacity) list** |
| l11 s4 LRU C++ (7 tests, g++) | 7/7 | fails 6, passes t5 | same tests as Python, same gap |
| l11 s6 TTL (6 tests) | 6/6 | fails 6 | `>` for `>=`, no purge in get, no refresh on get. **Passes: put of stored key does not stamp the time** |
| l12 s4 four methods (5) | 5/5 | fails 4 | no skip of empty names, ls of file, unsorted ls, overwrite |
| l12 s7 size (6) | 6/6 | fails t5 only | shallow size, count of files |
| l13 s1 stage 1 (3) | 3/3 | fails 2 | n/a |
| l13 s3 stage 2 (7) | 7/7 | fails 6 | no oversell check, mean of prices, no reset, required `price` (t7) |
| l13 s6 stage 3 (11) | 11/11 | fails t8 to t10 | fifo by average, stale average, newest first |
| l14 s3 limiter (6) | 6/6 | fails 6 | record-before-check, strict pop, global log, fixed window |
| l14 s6 bucket (6) | 6/6 | fails 5 | start empty, rate ignored, last not updated. **Passes: no cap at capacity** |
| homework h3-lfu (7) | 7/7 | fails 6 | MRU tie, capacity 0. **Passes: plain LRU, update not counted as a use, O(capacity) scan** |
| homework h3-hit-counter (5) | 5/5 | fails 4 | no stamp, window off by one, no slot reset |

Each `how` count (8, 7, 6, 5, 6, 3, 7, 11, 6, 6, 7, 5) matches the number of tests. Every example is also a test. Every `byKey` test key points at a real test.

## l11 least recently used cache

| Screen | Key | My computation | Verdict |
|---|---|---|---|
| s0 order get(9) | g1 g2 g3 g4 | lookup, unlink, push, return; 9, 2, 5 | ok |
| s1 choice unlink | a | two neighbours, two assignments; b, c, d each leave a link | ok |
| s2 code | tests | see table | gap, mismatch 1 |
| s3 numeric | 1 | gets 1, -1, 2; wrong 0 and 2 plausible | ok |
| s4 C++ | tests | see table | gap, mismatch 1 |
| s5 choice | a `10` and `21` | put 1, put 2, update 2 evicts nothing; b = -1, 21; c = 10, 20; d = 10, -1 | ok. Canvas contradicts caption, mismatch 4 |
| s6 TTL code | tests | see table | gap, mismatch 2 |
| s7 choice | a | times fall from head to tail; at 12 with ttl 5 the entries at 7 and 4 are expired, 9 live | ok. Explain canvas wrong, mismatch 5 |
| s8 order | p1 p2 p3 p4, d1 left out | lookup, update and stop, evict, insert | ok |
| s9 choice | a | scan makes hot keys oldest | ok |
| s10 numeric | 99499499 | simulated 100,000 puts: 99,499,500 - 1; wrong 99499500 = miss as 0 | ok |
| q-evict | Key 9 | order 7, 9 after get; put 4 drops 9 | ok |
| q-pointer | a | `node.next.prev = node.prev` | ok |
| q-update | 9 | wrong 8 old value, -1 miss | ok |
| q-expiry | 10 | 6 + 4; age rule `>=`; wrong 7 = 3 + 4 | ok |

## l12 file system

| Screen | Key | My computation | Verdict |
|---|---|---|---|
| s0 tap-regions | a-b | only `b` is a direct child; wrong sets deep and self | ok |
| s1 numeric | 3 | a, b, c; wrong 1 and 4 | ok |
| s2 choice | `['d.txt']` | file lists itself | ok |
| s3 choice | `'hello world'` | write appends and creates | ok |
| s4 code | tests | see table | ok |
| s5 choice | a | `'/'.split('/')` gives two empty names; a plain walk looks up `''` and fails | ok |
| s6 numeric | 12 | 4 + 2 + 6; wrong 10 = 4 + 6, 3 = file count | ok |
| s7 code | tests | `/docs` 9, `/docs/n` 8, file 1, root 9 (5 + 3 + 1) | ok |
| s8 order | w1 to w7, d1 out, w1 and w2 swappable | walk order matches the listing | ok |
| s9 choice | a read-only flags | the other three are methods | ok |
| q-split | `['', 'a', '', 'b']` | run in Python | ok |
| q-ls-file | `['p.txt']` | n/a | ok. Key 11 characters against 4, 7, 7 (ratio 1.57), note 9 |
| q-mkdir-twice | `['r.txt']` | second mkdir changes nothing | ok |
| q-size | 13 | 3 + 10; wrong 20 = whole `/s`, 10 = `c` only | ok |

## l13 requirements change

| Screen | Key | My computation | Verdict |
|---|---|---|---|
| s0 numeric | 50 | 100 + 100 - 150; wrong 350, 150 | ok |
| s1, s3, s6 code | tests | see table | ok |
| s2 numeric | 300 | average 11; 150 x 2; wrong 450 (first buy), 150 (last buy) | ok |
| s4 choice | a | required argument raises `TypeError` | ok |
| s5 numeric | 350 | 100 x 3 + 50 x 1; wrong 300 average, 150 newest | ok. Same trades as `ds` l11 `q-fifo-basis`, note 12 |
| s7 choice | a | lots serve both methods | ok. Key 69 against 51, 42, 49 (1.35) |
| s8 order | c1 to c5, d1 out | n/a | ok |
| s9 choice | a | n/a | ok |
| s10 numeric | 36 | FIFO 5 x 4 + 15 x 3 = 65; average: 20, then 15 x (33 - 32.4) = 9, total 29; wrong 65 and 29 | ok. Explain: sentence of exactly 20 words, note 13 |
| q-position | 15 | 30 - 12 + 5 - 8; wrong 55, -15 | ok |
| q-average | 12 | 1,200 / 100; wrong 11.5 | ok |
| q-fifo-lot | 20 | 5 x 4; wrong 5 (newest), 12.5 (average 9.5) | ok |
| q-old-call | a | `price=0` | ok |

## l14 rate limiter

| Screen | Key | My computation | Verdict |
|---|---|---|---|
| s0 choice | 15 and 16 | log 5, 6; cut-offs 4, 5, 6 give refuse, accept, accept | ok |
| s1 numeric | 16 | cut-off 6 at 16; wrong 17, 15, 6 | ok |
| s2 numeric | 4 | accepted 0, 1, 3, 4 (limit 2, window 3); wrong 2 and 3 are mental slips | ok |
| s3, s6 code | tests | see table | s6 gap, mismatch 3 |
| s4 choice | 0, 1, 10, 11 | correct limiter accepts T T F T T; record-before-check gives T T F F F (option b) | ok |
| s5 numeric | 80 | 40 + 40 across the boundary; wrong 40 | ok |
| s7 numeric | 4 | 2 + 2; wrong 2 (no refill), 3 (one token) | ok |
| s8 order | a1 to a4, d1 out | n/a | ok |
| s9 choice | a | n/a | ok |
| s10 choice | a | exact cap is the log, bursts the bucket, cheap the fixed window; b, c, d feedback each match their swap | ok |
| q-edge | a | cut-off 6, 6 not above 6 | ok |
| q-refused | a | log holds only 0, cut-off 0 at 5 | ok |
| q-bucket | 3 | min(5, 0 + 3); wrong 5, 1 | ok |
| q-choose | a | n/a | ok |

## review-3

| Item | Key | My computation | Verdict |
|---|---|---|---|
| r3-lru-sum | 14 | gets 2, -1, 6, -1, 8; wrong 16 = misses as 0, 22 = no eviction | ok |
| r3-lru-evicted | Key 15 | order 11, 15, 12; get 12 gives 12, 11, 15 | ok |
| r3-ttl-misses | 3 | get 2 hits and refreshes; 5, 6, 9 miss | key ok; wrong `one`, mismatch 8 |
| r3-fs-size | 21 | 6 + 11 + 4; wrong 17, 4 | ok |
| r3-fs-ls | `['m.txt', 'x', 'y']` | sorted direct children | ok |
| r3-fifo | 1100 | 200 x 5 + 50 x 2; wrong 1000 (average 21), 950 (newest first) | ok |
| r3-default-arg | a | n/a | ok |
| r3-window-accept | 4 | accepted 0, 1, 5, 6 | key ok; wrong `three`, mismatch 9; repeat, mismatch 11 |
| r3-bucket-accept | 8 | 4 + 2 + 1 + 1; wrong 4 (no refill), 10 | ok |
| r3-ring | a | 300 slots | ok |

## homework-3

| Item | Key | My computation | Verdict |
|---|---|---|---|
| h3-ledger part 1 | 35 | 20 + 12 x (45 - 43.75) = 15; wrong 20, 15 | ok |
| part 2 | 20 | 20 - 30 + 30; wrong 35, 50 | ok |
| part 3 | 15 | 35 - 20; wrong -15, 55 | ok. Repeats a lesson test, mismatch 11 |
| h3-lfu | tests | see table | gap, mismatch 7 |
| h3-hit-counter | tests | t5: 150 hits in (99,699, 99,999] | ok |
| h3-rate-limit-aloud | rubric 10 points | numbers 200 against 100, 100/60 a second | ok |
| h3-boundary | 200 | 100 + 100; wrong 100 | ok |
| h3-get-steps | s1 to s4, d1 out | n/a | ok. Repeats l11 s0, mismatch 11 |
| h3-constant-time | get, put, del | list and median are linear | ok |
| h3-lfu-trace | 9 | gets 1, -1, 3, -1, 3, 4; wrong 11 = misses as 0 | key ok; wrong `tie`, mismatch 10 |

## Mismatches

### Wrong keys

None.

### Hidden tests that a wrong solution passes

1. `l11-lru-cache.json` s2 and s4 (and the same ops in the C++ tests): the trap of screen 5 is not tested. A solution that evicts before looking the key up passes all 8 (and 7) tests, because `t3` is not full and `t6` updates the key that is least recent anyway. Fix: add `run_lru(2, [[0, 1, 10], [0, 2, 20], [0, 2, 21], [1, 1], [1, 2]])` expecting `[10, 21]` to both widgets (the buggy version returns `[-1, 21]`), and update the `how` counts and a `test-N` feedback line.
2. `l11-lru-cache.json` s6: a put of a stored key that does not refresh its time passes all 6 tests. Fix: add `run_ttl(2, 5, [[0, 1, 10, 0], [0, 1, 11, 4], [1, 1, 7]])` expecting `[11]` (the buggy version returns `[-1]`).
3. `l14-rate-limiter.json` s6: the cap at capacity is not tested; `tokens + elapsed * rate` with no `min` passes all 6. The cap is the lesson's formula. Fix: add `run_bucket(2, 1, [0, 10, 10, 10])` expecting `[True, True, True, False]`. Related note: the speed tests (l11 s2 and s4 t7, l14 s3 t6, homework LFU t7) have a capacity of 1,000 or less, so an O(capacity) list or scan solution passes them in under a second. Raise the capacity to 20,000 or more if the lesson means to enforce constant time.
7. `homework-3.json` h3-lfu: all 7 tests pass a plain LRU cache, and a version that does not count an update as a use also passes, though `how` claims "an update that counts as a use". In every test the least frequent key is also the least recent. Fix: add `run_lfu(2, [[0, 1, 1], [1, 1], [0, 2, 2], [0, 3, 3], [1, 1], [1, 2], [1, 3]])` expecting `[1, 1, -1, 3]` (LRU returns `[1, -1, 2, 3]`) and `run_lfu(2, [[0, 1, 1], [0, 1, 7], [0, 2, 2], [0, 3, 3], [1, 1], [1, 2], [1, 3]])` expecting `[7, -1, 3]` (no-count version returns `[-1, 2, 3]`). I ran both against the reference solution: they pass.

### Canvas contradicts the text

4. `l11-lru-cache.json` s5 canvas `cells: [1, 2]` with caption "most recent first is 2, then 1". Fix: `cells: [2, 1]`.
5. `l11-lru-cache.json` s7 `explain.canvas`: cells show key 3 (t=9) and key 1 (t=7) but the caption says keys 1 and 2 are purged. At time 12 with ttl 5 only key 3 survives. Fix: cells `[{"v": 3, "label": "t=9"}]`.

### `wrong` value that its feedback does not produce

| # | Path | Item | Stored | Described slip gives | Fix |
|---|---|---|---|---|---|
| 8 | `review-3.json` | r3-ttl-misses `one` | 1 | "let the entry live at age 3" gives 0 misses (get 2 hits, 5 hits at age 3, 6 and 9 hit), the same as `none` | Change `one` to a slip that gives 1, or drop it and keep `none`; reword the line to the real count |
| 9 | `review-3.json` | r3-window-accept `three` | 3 | "kept the time 0 alive at 5" accepts 0, 1, 6, 7: 4, the key | Replace with a slip that gives 3, or change the times so a boundary slip changes the count |
| 10 | `homework-3.json` | h3-lfu-trace `tie` | 8 | tie to the most recent gives gets 1, -1, 3, 1, -1, 4: sum 7 | Change the value to 7 |

### Repeats of a lesson (DECISIONS "Fresh numbers in reviews and homework")

11. Four repeats in the same course:
    - `homework-3.json` h3-ledger-follow-ups buys 10 at £50, sells 4 at £55, buys 10 at £40, sells 12 at £45. This is hidden test 10 of `l13` s6 (realised 20 under FIFO). Give the homework fresh trades.
    - `review-3.json` r3-window-accept (limit 2, window 5, times 0, 1, 2, 5, 6) repeats user `a` in hidden test 2 of `l14` s3 (T T F T T). Change the window or the times.
    - `homework-3.json` h3-get-steps asks for the four steps of `get` that `l11` s0 asks for, with the same answer order. Ask for `put` of a stored key, or a different operation.
    - `homework-3.json` h3-lfu test 1 starts with the first five operations of `l11` s2 test 1 (put 5/50, put 6/60, get 5, put 7/70, get 6). Change the keys and values.

### Notes (no key or test wrong)

12. `l13` s5 uses the trades of `ds` `l11-first-in-first-out` `q-fifo-basis` (100 at £10, 100 at £12, sell 150). The question differs (realised profit, 350, against cost basis, £1,600). A different course, and a lesson not a review or bank item, so I leave it to you.
13. Voice. No exclamation marks, no em-dashes, no American spellings. Eleven sentences have exactly 20 words, where the rule says under 20: `l11` s4 prose and `how`, `l11` s9 explain, `l11` s10 prose, `l13` s10 explain, `l14` s3 `test-1` feedback, `homework-3` h3-lfu prose, `how` and `test-4`, h3-rate-limit-aloud model, h3-lfu-trace explain. No explanation has more than three sentences.
14. Choice keys: no key is visibly longer than its distractors, except `l12` q-ls-file (11 characters against 4, 7, 7, ratio 1.57, short code literals). `l13` s4 (1.44) and s7 (1.35) are within the 1.5 limit.
15. h3-hit-counter: a deque of every hit passes all 5 tests, since "fixed amount of memory" cannot be tested by output. The `how` line does not claim it, so no change.
16. The checked lessons sit in `l11` to `l14` of `coding-int` and no other course, exam, drill or bank file repeats their numbers. I grepped `app/content/` for each sum, trace and test input: `ds` `h-lru` has the same shape as hidden LRU test 4 but different keys and answers.

## Fix pass

Fixed 14 findings (1 to 11, notes 13 and 14), disputed 0, deferred 3 (note 12, note 15, and the O(capacity) speed-test note under mismatch 3). Every number below was computed twice, by hand and with a simulator in the scratchpad `fix/` folder.

1. FIXED. LRU evict-first. Added hidden test `run_lru(2, [[0,1,10],[0,2,20],[0,2,21],[1,1],[1,2]])` expecting `[10, 21]` as Python test 9 and C++ test 8. Evict-first returns `[-1, 21]` and fails; reference passes. Counts in `how` now 9 and 8, `test-9` and `test-8` feedback added.
2. FIXED. TTL put refresh. Added `run_ttl(2, 5, [[0,1,10,0],[0,1,11,4],[1,1,7]])` expecting `[11]` as test 7. The put at 4 stamps 4, age 3 at 7 is live. No-stamp gives age 7, `-1`, and fails. `how` says 7; `test-7` added.
3. FIXED. Bucket cap. Added `run_bucket(2, 1, [0, 10, 10, 10])` expecting `[True, True, True, False]` as test 7. Capped: 2 tokens, spend 1 at 0, refill to min(2, 11) = 2 at 10, three spends leave 1, 0, then refuse. Uncapped gives all True and fails. `how` 7; `test-7` added. Speed-test capacities left at 1,000 or less: a constant-time check cannot be made reliable under the 5 s limit by capacity alone, deferred.
4. FIXED. l11 s5 canvas `cells` `[1, 2]` to `[2, 1]`.
5. FIXED. l11 s7 explain canvas cells key 3 and key 1 to key 3 only (`t=9`). At 12, ttl 5: ages 3, 5, 8, so 3 live, keys 1 and 2 purged.
6. (Table rows 8, 9, 10, all FIXED.) 8: `review-3` r3-ttl-misses `one` stays 1; old line gave 0 (same as `none`). New slip: count only the miss at 5, giving 1. Gets: 2 hit, 5 miss, 6 miss, 9 miss is 3; slip counts 1. 9: r3-window-accept replaced by new numbers (see 11). 10: `homework-3` h3-lfu-trace `tie` 8 to 7. Gets with the tie going to the most recent: put4 evicts key 3, so gets 1, -1, 3, 1, -1, 4. Sum 1 - 1 + 3 + 1 - 1 + 4 = 7, and by running totals 0, 3, 4, 3, 7.
7. FIXED. h3-lfu: added `run_lfu(2, [[0,1,1],[1,1],[0,2,2],[0,3,3],[1,1],[1,2],[1,3]])` expecting `[1, 1, -1, 3]` (test 8) and `run_lfu(2, [[0,1,1],[0,1,7],[0,2,2],[0,3,3],[1,1],[1,2],[1,3]])` expecting `[7, -1, 3]` (test 9). Plain LRU fails test 8 and 9; the no-count version fails test 9; reference passes both.
11. FIXED, four repeats.
    - Ledger now buys 8 at £60, sells 3 at £64, buys 15 at £52, sells 10 at £58. Average: 3 x 4 = 12, then 5 x 60 + 15 x 52 = 1,080 over 20 = 54 (also 60 x 1/4 + 52 x 3/4 = 54), 10 x 4 = 40, total 52. FIFO: 12, then 5 x (58 - 60) = -10 and 5 x 6 = 30, total 32 (also sold cost 300 + 260 = 560 against 580, profit 20, plus 12). Gap 20 (also leftover 10 shares cost 540 on average and 520 by FIFO). Wrong values: part 1 `fifo` 32, `second` 40; part 2 `avg` 52, `skip` 42 (12 + 30); part 3 `flip` -20, `sum` 84 (52 + 32).
    - r3-window-accept now limit 3, window 7, times 0, 1, 2, 3, 4, 7, 8. Correct: accepts 0, 1, 2, refuses 3 and 4, at 7 the log [1, 2] accepts, at 8 [2, 7] accepts: 5. `edge` (time at the cut-off still counts) refuses 7, accepts 8: 4. `recorded` (refused times logged) accepts 0, 1, 2 only: 3. Each recomputed by simulator.
    - h3-get-steps now orders the LFU touch (remove from bucket, raise minimum, add one, join the new bucket last), with `same` on s2 and s3 and the distractor "front of the new bucket". No lesson covers it.
    - h3-lfu test 1 keys and values moved to 15 to 18 and 150 to 180; expect `[150, -1, 170, -1, 170, 180]`, same structure, so same trace.
13. FIXED. Rewrote the 20-word sentences in l11 s4 (prose, `how`), l11 s9 explain, l11 s10 prose, l13 s10 explain, l14 s3 prose and `test-1`, h3-lfu prose, `how`, `test-4`, h3-rate-limit-aloud model, h3-lfu-trace explain. All at 19 words or fewer; the new `how` lines also checked.
14. FIXED. l12 q-ls-file options now carry short labels (key 31 characters against 31, 27, 26).
12 and 15 left as the checker advised. Mutant results are in the list below.

Mutants run against the new tests (all from the checker's scripts, repointed to this worktree): FAIL now: LRU evict-first (t9), TTL put-update no stamp (t7), TB no cap (t7), LFU as plain LRU (t8, t9), LFU put no count (t9). Still pass, deferred: LRU list O(capacity), LFU O(capacity) scan, TTL no purge in put and lazy get-only (equivalent output), RL full-history list, HC deque, FS truthy content. Reference passes every test and starters fail.

### Changed keys and tests for recheck

- Tests added: l11 s2 test 9; l11 s4 test 8; l11 s6 test 7; l14 s6 test 7; homework-3 h3-lfu tests 8 and 9. Test changed: h3-lfu test 1 (keys and expect).
- Keys changed: `review-3` r3-window-accept answer 4 to 5 (wrong 4 and 3); `homework-3` h3-ledger-follow-ups answers 35, 20, 15 to 52, 32, 20 (wrong values 32, 40; 52, 42; -20, 84); h3-lfu-trace wrong `tie` 8 to 7; h3-get-steps new answer order; r3-ttl-misses wrong `one` text only (value 1); l11 s5 canvas cells; l11 s7 explain canvas; l12 q-ls-file option texts (key still `a`).

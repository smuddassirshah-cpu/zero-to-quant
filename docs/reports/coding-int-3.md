# coding-int level 3 ("Design in code"): report

Written from `docs/briefs/coding-int.md` `## Level 3`, following `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`. Lesson ids, names, objectives and skills are those of `course.json` (`ci-design` on l11, l12 and l14; `ci-design` and `ci-timed` on l13). Money is whole £ in l13 and in the ledger items. Builders and checkers live in the scratchpad folder `coding-int-3` (`build.py` rebuilds every file from `b11.py` to `b14.py`, `b_rev.py` and `b_hw.py`; `refs3.py` holds every reference, starter, driver and hidden test; `verify.py` is the brute-force check; `starters.mjs` grades every starter and solution in the real app).

## Files

All in `app/content/courses/coding-int/`.

| File | Screens | Quiz / items | Code widgets (hidden tests) | Notes |
| --- | --- | --- | --- | --- |
| `l11-lru-cache.json` | 11 | 4 | `LRUCache` Python (8), `LRUCache` C++ (7), `TTLCache` (6) | linked-mode `array` hook and explore (a `frames` slider through the two unlink assignments), consoles for statements |
| `l12-file-system.json` | 10 | 4 | `FileSystem` stage A (5), stage B `size` (6) | `tree` canvases (tap on a branch, a `frames` slider with `dim` for `mkdir`), a `console` of `split` outputs for the trap |
| `l13-requirements-change.json` | 11 | 4 | `Ledger` stage 1 (3), stage 2 (7), stage 3 (11) | `table` of trades; each stage's starter is the previous reference with stubs; tests use `setup` lines and `compare: "raises"` |
| `l14-rate-limiter.json` | 11 | 4 | `RateLimiter` (6), `TokenBucket` (6) | `array` in queue mode with a time `frames` slider; `table` canvases for the transfers |
| `review-3.json` | | 10 items, d 3 | | every item has `tags` and `skills`; all four lessons |
| `homework-3.json` | | 8 items, d 3 to 5 (two 5s) | `LFUCache` (7), `HitCounter` (5) | one `longform` (10-point rubric), one `order` with a distractor, one `multi`, one E11 `parts` item (three `numeric` parts), `tags` on each |

Every code screen has `pace` (480, 600, 720, 840 or 900 s; 300 for l13 stage 1) and `tags`. Tag families are the brief's. New homework family: `hit-counter` (the brief named none for H3.2).

## Validator

`node tools/validate.mjs`: **0 errors**. Warnings for my files: three, "a ladder screen usually reuses the previous canvas kind" (l11 screen 8, l12 screen 7, l14 screen 6): the brief puts a ladder after a code or trap screen that has a console or another canvas. Every other warning is about other courses' unwritten files. `VOICE_BASE=<worktree>/app/content/courses/coding-int python3 docs/reviews/voice-scan.py` gives 0 explanations over three sentences and 0 sentences over 20 words. No em-dashes, no exclamation marks, no emoji; every choice has `"shuffle": true` and no key is visibly longer than its distractors (checked by length, ratio at most 1.5).

## Playthrough

`node tools/playthrough.mjs --lesson coding-int/<each of the four> --set coding-int/review-3 --set coding-int/homework-3 --local-cdn <pkgs>`: all passed, with and without `--mobile --why --shots` (the 390 px runs wrote about 400 screenshots; all read for layout).

| File | Desktop | 390 px (`--mobile --why`) |
| --- | --- | --- |
| l11 | ok, 15 checks, quiz 4/4 | ok |
| l12 | ok, 14 checks, quiz 4/4 | ok |
| l13 | ok, 15 checks, quiz 4/4 | ok |
| l14 | ok, 15 checks, quiz 4/4 | ok |
| review-3 | ok, recorded 10 of 10 | ok |
| homework-3 | ok, 8 of 8 right, 38 of 38 marks; parts checks ok | ok |

Layout fixes made from the screenshots: `console` lines ran off the right edge at 390 px, so every console has `wrap: true` and its statement lines are one sentence each (no hand-aligned columns); the l11 and l14 statements were rewritten for that. Trees of a single chain are tall at desktop width but readable; left as drawn.

## Starters and solutions in the app (Pyodide 0.27.7, YoWASP clang 21)

Each code widget was opened in the app with the local CDN, its starter set and graded, then its solution (`coding-int-3/starters.mjs`, results in `starters.json`). The Python references were also checked natively against independent brute forces.

| Widget | Tests | Starter passes (so fails) | Solution |
| --- | --- | --- | --- |
| l11 `LRUCache` Python | 8 | 2 (fails 6: tests 1, 2, 3, 4, 6, 7) | passes 8 |
| l11 `LRUCache` C++ | 7 | 1 (fails 6) | passes 7 |
| l11 `TTLCache` | 6 | 0 (fails 6) | passes 6 |
| l12 `FileSystem` stage A | 5 | 1 (fails 4) | passes 5 |
| l12 `FileSystem` stage B | 6 | 5 (fails 1, test 5) | passes 6 |
| l13 `Ledger` stage 1 | 3 | 1 (fails 2) | passes 3 |
| l13 `Ledger` stage 2 | 7 | 1 (fails 6) | passes 7 |
| l13 `Ledger` stage 3 | 11 | 8 (fails 3: FIFO rows 8, 9, 10) | passes 11 |
| l14 `RateLimiter` | 6 | 0 (fails 6) | passes 6 |
| l14 `TokenBucket` | 6 | 1 (fails 5) | passes 6 |
| H3.1 `LFUCache` | 7 | 1 (fails 6) | passes 7 |
| H3.2 `HitCounter` | 5 | 1 (fails 4) | passes 5 |

The stage B and stage 3 starters are the previous stage's reference with the new methods stubbed, as the brief says, so they fail only the new rows (1 of 6 and 3 of 11). The stage A starter is the brief's plain-dict starter. C++ `-O1` clang with libc++ hardening ran the LRU reference through all seven cases, including the 100,000-put case (sum 99,499,499, in a `long long`), with no difference from Python.

## Numbers and their sources

Every keyed number is asserted in a builder or in `verify.py` by two methods (the reference class and an independent brute force, or a closed form or hand sum):

- Brute-force cross-checks, seeded random runs: LRU 3,000 against a list of keys; TTL 3,000 against a list that purges every expired entry on each call; LFU 3,000 against `min` over (uses, last use); file system 2,936 valid sequences against a flat set of folders and a dict of files; ledger 3,000 trade lists per method against a replay of the whole history; limiter 3,000 against a scanned list; bucket 3,000 against a second-by-second loop; hit counter 2,000 against a list. Every hidden test row was also checked against its brute force.
- l11: hook order and the explore frames are structural; capacity 1 gets `1, -1, 2` (one miss); trap `put 1 (10), put 2 (20), put 2 (21)` then `get 1`, `get 2` gives `10, 21` (the evict-first bug gives `-1, 21`; checked by running both); transfer sum `1,000 * (99,000 + 99,999) / 2 - 1 = 99,499,499` (closed form and the reference); quiz: evicts key 9, capacity 1 update returns 9, expiry at 10 (`6 + 4`).
- l12: size of `/logs` is `4 + 2 + 6 = 12` (tree and by lengths); `size('/s/t')` is 13; the trap strings by `split`; quiz `'/a//b'.split('/')` is `['', 'a', '', 'b']`.
- l13: hook position 50; average cost £11 and realised £300; FIFO realised `100 * 3 + 50 * 1 = 350` with 50 left at £12 (average cost and FIFO by the references and by hand); screen 11 trades `(20, £30), (-5, £34), (10, £36), (-15, £33)` give FIFO 65 and average cost 29 (average of the 25 shares £32.4, `15 * 0.6 = 9`), difference 36; quiz 15, 12, 20.
- l14: hook `[5, 6]` limit 2 window 10 gives 14 no, 15 yes, 16 yes; explore: the time 6 leaves at 16; limit 2 window 3 over 0 to 5 gives 4 accepted; trap `0, 1, 5, 10, 11` gives `T T F T T` (the append-first bug locks out the rest); fixed counter against sliding log with limit 40 and 30-second blocks gives 80 and 40 (both run); bucket capacity 2 rate 2 gives 4; quiz edge accept, refused request (`T F T`), 3 tokens, the log as the only per-request store.
- Review: 14 (`2, -1, 6, -1, 8`, class and `OrderedDict`), evicted key 15 (keys 12, 15, 11, get 12, put 14), 3 misses (TTL, ages 2, 3), 21 (`6 + 11 + 4`; 17 is `/var/a`), `['m.txt', 'x', 'y']`, FIFO 1,100 (average cost £21 gives 1,000; newest-first gives 950), 4 accepted (`T T F T T F`; an off-by-one gives 3, recording refusals gives 2), 8 accepted by the bucket (`4 + 2 + 1 + 1`; no refill gives 4).
- Homework: ledger parts 35, 20 and 15 (average after the second buy `(6 * 50 + 10 * 40) / 16 = 43.75`, `12 * 1.25 = 15`; FIFO `20 - 30 + 30`; by the reference ledger with both methods and by hand); LFU trace sum 9 (`1, -1, 3, -1, 3, 4`, brute force; the tie-to-newest slip gives 8, a miss counted as 0 gives 11); fixed counter 200 against sliding log 100 (both run); LFU 50,000 puts sum 49,499,500 (`sum(49,000..49,999)`); hit counter 150 (50,000 hits at even seconds, count at 99,999).

## Differences from the brief (and why)

- **Homework order.** The E11 `parts` item (brief item 5) is item 1 of `homework-3`, because the playthrough's `partsHomeworkChecks` only works when the parts item is first (raised again in the inbox). The other items keep the brief's content; the order is parts, `LFUCache`, `HitCounter`, longform, fixed-window numeric, `get` order, `multi`, LFU trace.
- **Fresh numbers (DECISIONS).** The brief's l14 screen 6 and homework item 4 both used "100 at second 59, 100 at second 60, 200 against 100"; the lesson now uses limit 40 per 30-second block (80 against 40) and the homework keeps 100 and 200. The brief's l13 screen 11 told the agent to use a list different from the homework's; it is `(20, £30), (-5, £34), (10, £36), (-15, £33)`. Review item 2 (put 1, 2, 3, get 1, put 4) matched the trace in `ds` `h-lru`, so it uses keys 12, 15, 11 and 14, and hidden LRU test 4 uses keys 7, 8, 9 and 6 with the same shape and answer.
- **Trap screen of l11.** The brief's example (puts 1, 2, then 1 again) does not distinguish evicting first from the right rule, because key 1 is the least recent and is evicted and re-added with the same effect. The screen uses puts 1, 2 and then 2 again on a full cache: evicting first loses key 1.
- **Hook of l11 and homework item 6.** Both order the steps of `get` (as the brief says). The lesson has no distractor and key 9; the homework item has a distractor, "delete the node and create a new one", and no numbers.
- **Explore on unlinking (l11 screen 2).** The brief asks for four assignments; the question has four options of two assignments each, with the single-link slips as distractors, and the slider steps through the two real assignments.
- **l12 generalise.** `same: [["w1", "w2"]]` lets "start at the root" and "split the path" swap places.
- **Stage starters.** The l12 stage B and l13 stage 3 starters carry stubs (`size` returns 0; `method` is stored and ignored), so a learner can run them as they stand.

## Proposed `course.json` change

None.

## Hidden code

Python drivers (`run_lru`, `run_ttl`, `run_lfu`, `run_fs`, `run_limiter`, `run_bucket`, `run_hits`) are `postlude`; the console statement on each screen says the driver is hidden and what its rows mean. The C++ drivers `run_lru` and `big_lru_sum` are `postlude` too; the big case builds its own operations so the test row is one call.

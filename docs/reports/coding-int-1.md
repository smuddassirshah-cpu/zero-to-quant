# coding-int level 1 report: Patterns still to learn

Author: content agent, 4 November 2026. Brief: `docs/briefs/coding-int.md` `## Level 1`. All files in `app/content/courses/coding-int/`. No engine pass C feature is used. `course.json` is unchanged.

## Files

| File | Screens | Quiz / items | Code widgets | Notes |
| --- | --- | --- | --- | --- |
| `l1-merging-intervals.json` | 10 | 4 | 3 (Python merge, C++ merge, Python sweep) | number-line with `tapIntervals`, a dragged point with `derive` moving `i5`, a `table` widget |
| `l2-prefix-trees.json` | 10 | 4 | 2 (`Trie` via a `run_trie` postlude driver, `top_completions`) | `tree` with `nodes`, a `frames` control stepping the inserts with `dim` |
| `l3-window-maximum.json` | 10 | 4 | 1 (`longest_within_limit`) | `manipulate` on a `pair` of arrays (queue mode, `{v, label}` cells), a `frames` explore over a `pair` of array and table |
| `l4-top-k.json` | 11 | 4 | 3 (Python and C++ `top_k_frequent`, `kth_largest_stream`) | `table` canvas with `tap: "rows"`, heaps shown as a `table` with a `frames` control |
| `l5-bit-tricks.json` | 10 | 4 | 2 (`single_number`, `hamming_total`) | `table` explore whose cells are written by `derive` from two sliders (`&`, `|`, binary via `toString(2)`) |
| `review-1.json` | | 10 items, difficulty 2 to 4 | 0 | every item has `skills` and `tags`; two per lesson |
| `homework-1.json` | | 9 items, difficulty 3 to 5 (two at 5) | 4 (`free_gaps`, `two_singles`, `shortest_at_least`, `window_median`) | one `longform` (10-point rubric, spoken), one `order` with a distractor, three `numeric` |

Every lesson: `skills: ["ci-patterns"]`, objective copied from `course.json` `lessonObjectives`, one `trap` with a `byKey` line naming the action, a `generalise` screen whose pattern is a fenced code block and whose widget is the `order` derivation (with one distractor and its `why`), at least one transfer in a desk context, and an edge case (empty list, touching ends, empty prefix, repeated insert, `k = 0`, `limit = 0`, negatives). `tags` and `pace` on every code screen; `tags` on every quiz, review and homework item.

## Validator

`node tools/validate.mjs`: **0 errors** (406 warnings in all, mostly other courses' unwritten lessons). Warnings in this level's files: 12 on l1 screen 6 (`std::vector<std::vector<int>>` "not a supported type"; it works, see the backlog), and two "a ladder usually reuses the previous canvas kind" (l4 screen 8 and l5 screen 5 move from an array to a table of the same numbers).

Voice: `docs/reviews/voice-scan.py` with `VOICE_BASE` set to the absolute `coding-int` path: 0 sentences over 20 words and 0 explanations over three sentences; also 0 at a limit of 19. No exclamation marks, em-dashes or emoji. Every fenced block in learner text fits 54 characters a line (scratch lint).

## Playthrough

`node tools/playthrough.mjs --lesson coding-int/<each> --set coding-int/review-1 --set coding-int/homework-1 --local-cdn <scratchpad>/pkgs`: all passed, then again with `--mobile` (and once with `--mobile --why --shots`): all passed.

| Lesson or set | Checks | Quiz / marks |
| --- | --- | --- |
| l1-merging-intervals | 14 | 4/4 |
| l2-prefix-trees | 14 | 4/4 |
| l3-window-maximum | 14 | 4/4 |
| l4-top-k | 15 | 4/4 |
| l5-bit-tricks | 14 | 4/4 |
| review-1 | 10 items | 10 of 10 |
| homework-1 | 9 items | 9 of 9, 41 of 41 marks |

Screenshots (desktop, 390 px, Why? sheets) were reviewed. Fixed from them: interval labels on row 0 crossing the axis (rows now start at 1), a C++ signature and generalise comments too wide (wrapped), tall tries on code screens (`maxHeight`), the `left` pointer colliding with the window label (label dropped), the two-heap pair drawn tiny (now a table), the ten-column sizes table scrolling at 390 px (now two rows of five).

## Starters and solutions in the app (Pyodide 0.27.7, YoWASP clang 21)

KNOWN_ISSUES says the brief's code was checked natively only. Every starter and every solution was run through the app's own Check (scratch Playwright script `codecheck.mjs`, same local CDN), plus a correct but slow version where a test is meant to stop it. Seconds are the wall time of one Check, from click to result.

| Widget | Starter | Solution | Slow but correct version |
| --- | --- | --- | --- |
| l1 `merge_intervals` (Python) | 4/10, 0.17 s | 10/10, 0.12 s | |
| l1 `merge_intervals` (C++) | 4/10, 20.4 s (first compile after load) | 10/10, 7.0 s | |
| l1 `count_overlapping_pairs` | 3/8, 0.23 s | 8/8, 0.72 s | double loop: 7/8, stopped on test 8 at 5 s |
| l2 `Trie` | 1/6, 0.16 s | 6/6, 0.14 s | |
| l2 `top_completions` | 6/8, 0.15 s | 8/8, 0.16 s | |
| l3 `longest_within_limit` | 2/11, 0.15 s | 11/11, 0.97 s | double loop with early break: 8/11, stopped on test 9 (`[1] * 100000`) |
| l4 `top_k_frequent` (Python) | 5/7, 0.23 s | 7/7, 0.20 s | |
| l4 `top_k_frequent` (C++) | 3/7, 9.4 s | 7/7, 5.3 s | |
| l4 `kth_largest_stream` | 1/6, 5.2 s (test 6 stops it) | 6/6, 0.24 s | re-sort after each add: 5/6, stopped on test 6 |
| l5 `single_number` | 2/7, 0.13 s | 7/7, 0.17 s | |
| l5 `hamming_total` | 3/8, 0.13 s | 8/8, 0.44 s | pairwise loop: 7/8, stopped on test 8 |
| hw `free_gaps` | 2/8 | 8/8, 0.03 s | |
| hw `two_singles` | 0/4 | 4/4, 0.04 s | |
| hw `shortest_at_least` | 2/9 | 9/9, 0.21 s | |
| hw `window_median` | 3/7 | 7/7, 0.31 s | |

C++ differences from the brief's native check: none in results. The C++ `top_k_frequent` starter fails 4 of 7 in libc++ as natively. `std::vector<std::vector<int>>` arguments (including the empty list with `types` given) and results compare correctly. The l4 large C++ case builds its 50,000 words in `setup` with `std::to_string(10000 + i % 1000).substr(1)`, so no extra header is needed.

Engine behaviours the brief relied on and that were confirmed in the browser: a `derive` rule `"i5.from": "p.x"` (with `i5.to` and a `{{}}` label) moves a number-line interval as its point is dragged (inbox bullet "Confirm two bindings", first half: it works); `frames` controls on `tree` (`dim`, `values`) and on a `pair` and a `table` (`values`); `derive` writing `values.r0c1` on a `table` from slider params, with `&`, `|` and `(x).toString(2).padStart(4, '0')`.

## Numbers (each computed twice)

Script: `<scratchpad>/coding-int-1/l1_level_numbers.py` (two independent methods per number; all asserted equal). Brief numbers were also rerun from `docs/briefs/coding-int-scripts/l1.py`, `l_extra.py`, `l3_trap.py`, `l5_new.py` (all OK).

| Where | Number | Method 1 | Method 2 |
| --- | --- | --- | --- |
| l1 s1 | blocks `[1, 8]`, `[10, 15]` | merge | half-unit point cover |
| l1 s2 | largest joining start 12 | merge for p = 11..14 | point cover |
| l1 s3 | unsorted loop returns `[[8, 10]]` | the loop without `sorted` | trace: 1 and 2 are at most 10 |
| l1 s7 | bug returns `[[1, 3], [4, 5]]`; right `[[1, 10]]` | buggy loop | point cover |
| l1 s10 | active 0, 1, 1, 1; pairs 3 | sweep | double loop |
| l1 quiz | 3 blocks; 19,931,569 comparisons; 4,999,950,000 pair checks | merge; `n log2 n`; `n(n-1)/2` | point cover; `n ln n / ln 2`; `comb(n, 2)` |
| l2 | nodes 8 (tea ten to inn), 6 (buy bus bid), 9 (car card care cat dog), 5 (apple); bound 10,000; `count_prefix('bid')` 2; `log2 4000` = 11.97 | inserting | distinct prefixes |
| l3 | maxima 5, 5, 6, 6, 7, 9 sum 38; deque after index 4 `[4]`; explore trace (`[10, 1, 2, 4, 7, 2]`, limit 5) best 4; trap buggy 1, right 3; operations 400,000; naive 2,500,050,000; ticks longest 4; quiz deque after index 3 `[2, 3]`; quiz new list 4 | deque | slice max / brute force over all runs |
| l4 | panel TAV, BLN, MPL; pops 7 (10 values, k = 3) and 8 (12, k = 4); ties `['ask', 'bid']` vs count-only `['bid', 'ask']`; medians 7, 5, 7, 5, 7, 5 sum 36, sizes 3 and 3; ratio 500,000 | heap / sort | `nsmallest` / `statistics.median` / `log(1e5)/log(10)` |
| l5 | `4^1^2^1^2` = 4; `44 & 43` = 40, 3 runs; `12 & -12` = 4, `40 & -40` = 8; `2^2^2^7^7^7^5` = 0; bits in 0..15 = 32; quiz 9, 4 runs (77), 8 (88), 23 | Python operators | binary strings, `bin().count`, closed forms |
| review | 4 blocks; 2 pairs; 9 nodes; count 3; window sum 59; deque size 2; k-th sum 34 (5, 6, 7, 8, 8); 104; 3 | as above | as above (heap against re-sorting for 34) |
| homework | 19.9 million; 815,030 set bits; 2,080,000 bytes | `n log2 n`; summing `bin(i).count('1')`; `1000*10*26*8` | `n ln n / ln 2`; per-column period formula; per-node sum |

Wrong-answer values used in `numeric` `wrong[]` lists were also computed (for example the review k-th distractors: maxima sum 54, second-largest sum 40).

## Deviations from the brief, with reasons

- l1 screen 3: the brief keys `[[8,10],[1,6]]` as what a single pass without sorting returns. Run as written (the merge loop minus `sorted`), it returns `[[8, 10]]`, because `1 <= 10` merges `[1, 3]` into `[8, 10]`. The screen shows that loop, keys `[[8, 10]]`, and keeps `[[8, 10], [1, 6]]` as a distractor (a true overlap test).
- l1 screen 7: the brief says the learner who copies the next end returns `[[1,5]]`. Run, `out[-1][1] = e` returns `[[1, 3], [4, 5]]`. The question asks for the right output, `[[1, 10]]`; both `[[1, 3], [4, 5]]` (byKey: "You copied the last end instead of keeping the larger") and `[[1, 5]]` are distractors.
- Each "generalise + derive" item is one `generalise` screen with an `order` widget, so the screen counts match the brief (l1 10, l2 10, l4 11, l5 10).
- l3 has 10 screens, not 9: screen 9's "which structure" and "how long" are two `transfer` screens (one widget each). Screen 6 asks the 400,000 count; the naive 2,500,050,000 is quiz item 3 as a choice of magnitudes.
- l3 screen 4 shows the two deques as a table beside the array (a `pair` holds two canvases, not three).
- l4 screen 8 shows the heaps as a `table` with a `frames` control, not `array` or `tree` canvases (the array pair rendered unreadably small; backlog bullet).
- l5 screens 3 and 5 ask both brief numbers in one `table` widget (two cells).
- Difficulties: brief problem difficulties of 4 (l3, l4) are 3 on lesson screens, the cap for lesson screens; review and homework difficulties follow the brief table.
- `pace`: 480 (l5 code A, as the brief says), 600 or 720 elsewhere; 900 on homework code items.
- l4 hook symbols are made-up three-letter tickers (KRN, TAV, ORX, ZEN, MPL, VLT, BLN, QRS) with counts chosen so a three-way tie at 11 forces the alphabet; firm-neutral.

## course.json

No change proposed.

## Seeds and conventions

Seeded tests as in the brief (`random.seed(3)` for the k-th stream sum 28,666,963,171; `random.seed(9)` for the window-median sum 19,786,861,586.5). Intervals closed unless a screen says half-open; money in pence on the l3 transfer.

## Backlog

Five bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (coding-int L1, 4 Nov)": table `wrong[]` keys refused by the validator, `std::vector<std::vector<int>>` warning, a tiny `pair` of arrays, no node mark on `tree`, no starter check in the playthrough.

Generators and checks (scratch, not committed): `<scratchpad>/coding-int-1/` (`gen_l1.py` to `gen_l5.py`, `gen_sets.py`, `genall.py`, `l1_level_numbers.py`, `codecheck.mjs`, `slow.json`, `probe.mjs`).

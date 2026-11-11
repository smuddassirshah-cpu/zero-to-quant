# Drills pack `ci`, pack 8 (intervals, greedy, bits, simulation)

Brief: `docs/briefs/drills-ci-packs-5-8.md`, row "Pack 8", on top of `docs/briefs/drills-ci-packs.md` and `docs/briefs/drills-1.8.md`. 15 Python drills, `"pack": "ci"`, `"course": "coding-int"`, skills `ci-patterns` and `ci-timed`, tags `["pack-8", ("stdin",) <slug>]`, rows appended to `app/content/drills/index.json`. Every drill carries `constraints` objects (ENGINE-BACKLOG 866) beside the prose. All four pattern slugs are in the vocabulary, so no tag stands in for a missing slug.

| id | idea | pattern | diff. | pace (s) | stdin | hidden tests | planted | further wrong |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ci-grace-sessions` | merging intervals with a grace gap, counts | intervals | 2 | 960 | no | 14 | 3 | 6 |
| `ci-rest-days` | task scheduling with a rest per machine, fixed order | greedy | 2 | 900 | no | 15 | 3 + slow | 5 |
| `ci-robot-floor` | a robot run step by step, stopped by shelves and edges | simulation | 2 | 1080 | yes | 12 | 3 | 6 |
| `ci-one-bit-apart` | pairs one bit apart, 30 flips a code | bits | 3 | 1200 | no | 13 | 3 + slow | 6 |
| `ci-switch-panel` | subsets by bit mask, smallest then first in order | bits | 3 | 1500 | no | 15 | 5 | 5 |
| `ci-ring-turns` | ring rotation of a matrix, alternating, line rings stay | simulation | 3 | 1500 | no | 14 | 2 + slow | 6 |
| `ci-double-checks` | fewest points stabbing intervals, `need` each | intervals | 4 | 1980 | no | 15 | 4 + slow | 6 |
| `ci-first-fit-slot` | inserting an interval at the first fit, joining touches | intervals | 3 | 1260 | no | 15 | 5 | 6 |
| `ci-room-numbers` | fewest rooms: lowest free room, cleaning gap | intervals | 3 | 1620 | no | 14 | 3 + 3 slow | 6 |
| `ci-loop-starts` | refuelling circuit: every start that works | greedy | 4 | 1860 | no | 14 | 3 + 3 slow | 5 |
| `ci-stone-hops` | fewest jumps with a shortest and a longest hop, water | greedy | 4 | 2040 | no | 15 | 5 + 3 slow | 5 |
| `ci-k-bit-count` | counting numbers with `k` set bits in a range | bits | 4 | 2100 | no | 13 | 3 + 2 slow | 5 |
| `ci-ring-bonuses` | two-pass greedy on a circle | greedy | 4 | 2160 | no | 15 | 3 + 2 slow | 5 |
| `ci-spiral-cells` | the cell at step `k` of a spiral on a huge field | simulation | 5 | 2400 | no | 13 | 3 + 3 slow | 5 |
| `ci-stop-cascade` | order book with stop orders that set each other off | simulation | 5 | 2700 | yes | 15 | 5 + 3 slow | 6 |

Mix: three at 2, five at 3, five at 4, two at 5; two stdin drills. Every idea of the row is covered: merging and inserting intervals (grace sessions, first-fit slot), fewest rooms or arrows (room numbers, double checks), jump reachability and fewest jumps (stone hops), a refuelling circuit (loop starts), task scheduling with a gap (rest days), counting bits and a single-bit difference (one bit apart, k-bit count), subsets by bit mask (switch panel), spiral and rotation of a matrix (spiral cells, ring turns), a robot and an order book run step by step (robot floor, stop cascade). "Single number" itself is taught in `coding-int` l5 and `two_singles` in homework 1, so the bits drills use flips and counts instead.

## Pyodide timings, difficulty 4 and 5

Measured by `drills-ci-8-check.py --pyodide <pkgs>`: Pyodide 0.27.7 under node, all hidden tests in one run, as the drill page runs them against its 5 s limit. "Over 12 s" means the run was cut off at the 12 s cap. Every model is under 0.5 s, more than a factor of ten inside the limit; every slow method is past 12 s.

| id | model | slow method (planted, last entries) | in Pyodide |
| --- | --- | --- | --- |
| `ci-double-checks` | 0.07 s | every set of minutes by size (lazy, no list of minutes built) | over 12 s |
| `ci-room-numbers` | 0.30 s | free minutes in a list, scanned from room 0 | over 12 s |
| | | `min` over a set of free rooms | over 12 s |
| | | the list scanned from the top down | over 12 s |
| `ci-loop-starts` | 0.24 s | drive from every depot, stop when empty | over 12 s |
| | | `accumulate` over the turned list per depot | over 12 s |
| | | skip ahead to one start, then drive from every depot | over 12 s |
| `ci-stone-hops` | 0.25 s | breadth-first search over the whole window | over 12 s |
| | | the same search back from the end | over 12 s |
| | | a table with a minimum over each window | over 12 s |
| `ci-k-bit-count` | 0.01 s | check every number in the range | over 12 s |
| | | step through the `k`-bit numbers (Gosper) | over 12 s |
| `ci-ring-bonuses` | 0.27 s | sweep forwards until nothing changes | over 12 s |
| | | sweep backwards until nothing changes | over 12 s |
| `ci-spiral-cells` | 0.26 s | walk the spiral a step at a time | over 12 s |
| | | skip ring by ring for each step | over 12 s |
| | | sort the steps, skip rings once for all | over 12 s |
| `ci-stop-cascade` | 0.42 s | scan the waiting stops after every event | over 12 s |
| | | scan the book for the cheapest sell | over 12 s |
| | | sort the stops again after every event | over 12 s |

Following the pack 5 review, each ruled-out method is planted in its turned-round or sorted form as well, and the large tests are built so that order does not save it (both a rising and a falling run in `ci-ring-bonuses`, the full window from either end in `ci-stone-hops`, stops listed with falling prices in `ci-stop-cascade`). Sorted-list variants with `bisect.insort` are not ruled out. Measured in Pyodide after the fix pass: free rooms 0.73 s, busy and free rooms both 1.24 s, stops 0.70 to 1.40 s (falling order popped from the end, and ascending with `pop(0)`), against models at 0.31 s and 0.44 s; the room left under the 5 s limit is 4.0 to 6.8 times for rooms and 3.6 to 7.1 for stops, under the brief's factor of five in the slower forms. Both drills now say in `constraints[1]` that a sorted list kept with `bisect` also passes, by a smaller margin than two heaps, and that heaps are the target. In `ci-ring-bonuses`, sweeping both ways in turn until nothing changes settles in two rounds and is right; the constraint rules out one-way sweeps only.

## Checks

1. `docs/reports/drills-ci-8-check.py` (scratchpad venv Python): exit 0, "15 drills, 0 errors" (4 min 10 s natively). It imports `drills-ci-8-indep.py` (an independent method per drill: brute force on small inputs, such as every set of minutes, every 2-colouring of switches, a day-by-day calendar, single steps of every ring, a list-and-scan order book; a different algorithm on large ones, such as a segment tree over rooms, a sliding-window minimum, a digit DP, three copies in a line, an integer square root for the ring, price levels with every stop in reach fired as one buy) and `drills-ci-8-wrong.py`. Per drill it checks model and independent method against every `expect`, every call's real arguments against the constraint objects and the prose rules, the starter fails, every planted wrong solution fails inside 2.5 s, every slow plant runs past 5 s, every further wrong solution fails, the stated numbers of each brief (`STATED`), the mix, tags, paces, `how` test counts and index rows. The Pyodide timings above came from `--pyodide <pkgs>` runs on the seven difficulty 4 and 5 drills, in two calls (the full run with Pyodide takes over ten minutes).
2. `node tools/validate.mjs`: 0 errors; no `[no-constraints]` warning on these files. The only warnings on them are "pace over 30 minutes" on the seven drills paced over 1,800 s, which the brief allows.
3. `node tools/playthrough.mjs --drill <15 ids> --local-cdn <pkgs>`: All passed; with `--mobile`: All passed. Shots at 440 px of the two longest briefs (stop cascade, spiral cells) read cleanly.
4. Voice: `voice-scan.py 35` on the 15 files: 0 sentences over 35 words, 0 explanations over three sentences; no em-dashes; the only `!` are `!=` in code.
5. This report and three inbox bullets.
6. `node tools/planted-check.mjs --drill <15 ids> --require --local-cdn <pkgs>`: 15 drills, 65 planted solutions, 0 failures.
7. `node tools/fresh-check.mjs --drill <id>`: 0 hits for all 15.

## Wrong solutions beyond `planted`, and the tests they added

`drills-ci-8-wrong.py` holds 83 further wrong or too-slow solutions, five or six a drill (wrong tie and boundary rules, sorting by the wrong key, the slow method in another order, missed edge cases, the classic's code applied unchanged). On first run, 8 passed every hidden test. Six of those turned out to be right, and are replaced in the file by real slips: waiting a day past the ready day (`ci-rest-days`), counting rings from the smaller side (`ci-ring-turns`), a booking ending at the slot taken as a clash (`ci-first-fit-slot`), numbering a new room by the busy count (`ci-room-numbers`), the earlier minimum one depot too far (`ci-loop-starts`), and two rounds of sweeps both ways (`ci-ring-bonuses`, see above). Two were wrong, two more were caught only by a time-out or not at all, and each now fails on a test added for it:

- `ci-ring-turns`, the caller's grid changed in place: `(lambda g: (turn_rings(g, 3), g))(...)` returns the grid as well, so a changed input shows.
- `ci-double-checks`, shortest jobs first: `[[5, 7, 2], [1, 3, 1], [7, 8, 1]]` = 3 (the candidate gives 4; found by a random search against the brute force).
- `ci-double-checks` planted[1], the duplicate minute, passed once its slow count was made fast: `[[4, 5, 1], [0, 5, 3], [5, 8, 2]]` = 4 catches it (it gives 3), and the weaker `[[0, 9, 2], [0, 9, 2], [0, 9, 1]]` was dropped to stay at 15 tests.
- `ci-rest-days`, a later job going first while the next one waits, failed only by running slow on the large tests: `run_days(['kiln', 'kiln', 'drum'], {'kiln': 2})` = `[1, 4, 5]` now fails it by value (it gives the drum day 2).
- `ci-stop-cascade` planted[2], a stop kept waiting while the book is empty, got its test with the plant: `'4\nS 5 1\nB 1\nT 5 3\nS 6 2\n'`, last line `5 1` (the plant buys at 6).

## Freshness

Every example and test input was written for these drills. Taught or drilled setups avoided: `merge_intervals`, `count_overlapping_pairs` (coding-int l1), `free_gaps`, `two_singles` (homework 1), `single_number`, `hamming_total` (l5), `spiral_order`, `rotate` (l9), `run_book` (l10), `min_rooms`, `max_non_overlapping` (contests l10), `fewest_alerts` (homework 3), `popcounts`, `best_subset` (contests l11), `dsa-loop-depots` (one start), `oa-min-jumps`, `dsa-rotate-rota`, `dsa-looping-route`, `ci-interval-intersections`, `ci-cpp-insert-interval`, `ci-no-repeat-rota`. Eleven drills grow from a known task (recalled from memory, not checked online) and each `how` says what changed and why it changes the code: merge intervals (a grace gap and a count), task scheduler II (a rest per machine in a dict, every day returned), the walking robot (edges stop it, distinct cells), rotating grid rings (alternate directions, line rings stay, odd sizes allowed), set intersection of size two (any `need` per job), insert interval (a first-fit search and joining of touches), meeting rooms (cleaning time, the lowest free number per meeting), gas station (every start), jump game with a range (fewest hops, water), candy (on a circle) and spiral order (one cell at step `k` on a field of $10^{18}$ plots). `ci-one-bit-apart`, `ci-switch-panel`, `ci-k-bit-count` and `ci-stop-cascade` are generic tasks in our own settings.

Worked numbers in the briefs (`[[0, 20, 2], [30, 47, 2], [50, 52, 1]]`, `[1, 2, 4, 7, 8]`, `'0 1 S 4'`, 6, `[0, 3]`, `[[9, 4, 7], [8, 5, 1], [3, 6, 2]]`, 3, `[9, [[2, 14], [16, 20]]]`, `[0, 1, 1, 0]`, `[0]`, 2, `[5]`, 8, `[[1, 3], [1, 1], [1, 2]]`, `'- 0\n- 0\n- 0\n12 4'`) are the `expect` of each drill's first example, and the check script recomputes each one with the independent method, with the side numbers the briefs quote (the gaps 2 and 3, the bits 1, 2 and 4, the gains and battery readings, the twelve-step spiral, the 15 of both switch pairs, the free minutes 12 and 32, $5 \times 10^8$ rings).

`app/content/manifest.json` was rewritten by the validator and is not committed.

## Fix pass (second read of pack 8)

- `ci-k-bit-count` resized to at most 400 queries (tests[11] over `range(400)`, tests[12] with 300 copies of the repeated query). Measured in Pyodide 0.27.7 under node, all hidden tests in one run: the textbook digit recursion with `lru_cache` takes 0.85 s (4.4 s at 2,000 queries), a factor of 5.9 inside the 5 s limit; the model takes 0.01 s; both obvious methods (every number in the range, stepping through the `k`-bit numbers) still run past 12 s on tests[6], a range of $2^{60}$.
- `ci-ring-bonuses`: sizes kept (the 50,000-long runs are what fail the one-way sweeps), and `constraints[1]` now says a recursion from trader to trader goes too deep for Python here, so use loops. Same sentence for `ci-stop-cascade` (20,000 stops in one event).
- `ci-double-checks` is now difficulty 4, pace 1,980, and `ci-room-numbers` difficulty 3, pace 1,620 (mix unchanged). Double checks gains a slow planted method (every set of minutes by size, built lazily so it holds no list of a billion minutes), cut off at 12 s in Pyodide, and a `how` that names the obvious method and the step to the target.
- Ten reader candidates are now `planted` entries (first-fit slot 2, stop cascade 2, stone hops 2, double checks 1, switch panel 2, rest days 1), with the tests listed in the review's `## Fix pass`. Planted slow entries stay last: `SLOW_IDX` in `drills-ci-8-indep.py` follows the new indices.
- `ci-room-numbers` example 0 uses `[[0, 28], [4, 9], [11, 40], [33, 50]]`, answer still `[0, 1, 1, 0]`; the `STATED` row follows.

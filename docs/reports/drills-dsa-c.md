# Drills, pack `dsa`, sub-pack C (trees, heaps and tries, intervals)

Brief: `docs/briefs/drills-1.8.md`, sub-pack C. Fifteen Python drills in `app/content/drills/`, each with a row appended to `drills/index.json`.

## Drills

| id | pattern | course | difficulty | pace (s) | stdin | hidden tests |
| --- | --- | --- | --- | --- | --- | --- |
| `dsa-route-order` | trees | ds | 1 | 600 | no | 11 |
| `dsa-shallowest-leaf` | trees | ds | 1 | 480 | no | 11 |
| `dsa-shared-tail` | trees | ds | 2 | 900 | yes | 13 |
| `dsa-common-manager` | trees | ds | 2 | 900 | no | 12 |
| `dsa-closest-level` | trees | ds | 2 | 900 | no | 11 |
| `dsa-swapped-levels` | trees | ds | 3 | 1500 | no | 13 |
| `dsa-nearest-strikes` | heaps-tries | ds | 1 | 600 | no | 12 |
| `dsa-short-codes` | heaps-tries | ds | 2 | 1200 | no | 12 |
| `dsa-print-queue` | heaps-tries | ds | 3 | 1500 | yes | 12 |
| `dsa-window-every-venue` | heaps-tries | ds | 3 | 1500 | no | 12 |
| `dsa-total-booked` | intervals | algo-think | 1 | 600 | no | 12 |
| `dsa-double-booked` | intervals | algo-think | 1 | 480 | no | 12 |
| `dsa-peak-calls` | intervals | algo-think | 2 | 900 | yes | 12 |
| `dsa-cover-opening` | intervals | algo-think | 2 | 1200 | no | 13 |
| `dsa-shortest-cover` | intervals | algo-think | 3 | 1500 | no | 12 |

Difficulty split 5 / 6 / 4; three stdin drills (`solve_<slug>(text)`, tagged `stdin`, tests with trailing newlines, blank lines and extra spaces). Skills: `ds-lists`, `ds-trees`, `ds-hashing`, `ds-pointers` (declared by `ds` lessons) and `at-sort`, `at-greedy`, `at-complexity` (declared by `algo-think` lessons).

Encodings, stated in each brief: a linked list is either `[stop, next_stop]` pairs in any order (`dsa-route-order`) or a pool of next-pointer indices with `-1` at the end (`dsa-shared-tail`); a tree is a nested tuple `(value, left, right)` with `None` for empty. Tree tests keep every root-to-leaf path at 400 nodes or fewer, so a recursive answer stays inside Python's recursion limit.

## Complexity tests

Each drill's last one or two tests are large (100,000 to 200,000 items). Naive versions (list scans per step, all pairs, per-minute marking, per-query full scans, contains-search at every level of a 397-deep chart, repeated child recursion, try-every-swap) were timed natively in `<scratchpad>/dsa-c/naive.py`: all 15 ran past 12 s. The model solutions take at most about 1 s natively, including building the test input. Where the target is $O(n)$ on a tree (`dsa-shallowest-leaf`, `dsa-swapped-levels`), the large test catches recursion that recomputes a child and pair-trying, not an $O(n \log n)$ walk.

## Checks

1. `docs/reports/drills-dsa-c-check.py` (venv Python): the model solution and an independent method (reverse-link walk, set of queue A, breadth-first search, parent map, in-order plus bisect, comparison with the sorted reading, full sort, neighbour common prefixes, page buckets, numpy `searchsorted` over every start, event sweep, union length against summed lengths, a Fenwick-tree DP over shifts, union-find assignment by window length) agree with every example and hidden `expect`. The starter fails at least one hidden test in all 15. It also checks each model against a brute force on 4,160 random small inputs. Exit 0, `errors: 0`.
2. `node tools/validate.mjs`: 0 errors, no warnings on these files.
3. Playthrough `--drill` x15 `--local-cdn`: all passed (the model passes every hidden test, the starter fails), and all passed again with `--mobile`. Browser relaunches 0. A first run made while fresh-check was also running had two flaky failures: a 200,000-job print-queue test overran 5 s, and a mobile stopwatch record held the starter's run. The print queue now uses 100,000 jobs (naive still past 12 s natively), and both pass on reruns; this is raised in the inbox.
4. Voice: `voice-scan.py 35` on a copy of the 15 files: 0 over three sentences, 0 sentences over 35 words of 450. No exclamation marks, no em or en dashes in prose (the only `!` is `!=` inside code); British spelling.
5. Fresh: `node tools/fresh-check.mjs --drill <id>` gives 0 hits for all 15. Triage at `--min-run 8 --min-share 0` turns up only house phrasing shared with sub-pack A, `ci-` drills and each other: the time-limit constraint sentence, the stdin sentence "Lines may carry extra spaces, and the text may end with blank lines" (also py-found `homework-1` item 5), and "the time from `start` up to but not including `end`". None is a shared setup. No function name is shared with a lesson code widget.

## Fresh-setup notes

Taught material avoided: `ds/l12` and `l13` (reverse, remove nth from end, cycle, middle), `ds/l14` to `l16` (traversals, BST insert and validate, height, balance, root-to-leaf maximum), `ds/review-4` (diameter), `ds/homework-4` (merge k lists, kth smallest, running median), `coding-int/l1` (merge intervals, overlapping pairs), `l2` (prefix counts), `l4` (top k frequent, kth largest stream, running median), `homework-1` (free gaps), `ci-interval-intersections`, `ci-cpp-insert-interval` and `oa-merge-cost`. A first plan had a running median and fewest bookings to cancel. Both were dropped: the median is taught in `coding-int/l4` and `ds/homework-4`, and the cancel count is the complement of earliest-finish scheduling in `algo-think/l14`. The tree diameter was dropped for `ds/review-4`.

Close neighbours that stand: `dsa-swapped-levels` uses the in-order reading that `ds/l15` uses to validate a BST, but asks which two levels were swapped. `dsa-total-booked` sorts and merges like `coding-int/l1`, but asks for the covered length.

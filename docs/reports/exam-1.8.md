# Topic 1.8 exam: data structures and algorithms

File: `app/content/exams/topic-1.8.json` (id `topic-1.8`, 60 minutes, pass 0.7).
Generator and checks: `scratchpad/exam-1.8/` (`gen.py` builds the file, `code.py` builds the code items and their expected values, `calc.py`, `search*.py`, `verify_large.py`, `grid2.py` recompute the numbers, `codecheck.mjs` and `slowcheck.mjs` run the code items in Pyodide).

## Shape

28 items, interleaving the three courses (algo-think, ds, graphs-dp).

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 6 | 21% | 20% |
| 3 | 14 | 50% | 50% |
| 4 | 5 | 18% | 20% |
| 5 | 3 | 11% | 10% |

Widgets: 9 numeric, 6 tap-regions (graph x2, array, grid, tree x2), 4 choice, 4 code, 2 table, 1 order, 1 multi, 1 longform.

| # | id | d | skills | widget / canvas |
|---|---|---|---|---|
| 1 | e-tick-lookup | 2 | at-complexity, ds-hashing | choice |
| 2 | e-bfs-next | 2 | gd-traversal, gd-graphs | tap-regions on graph (next node BFS processes) |
| 3 | e-pointer-scan | 2 | ds-pointers | tap-regions on array (cells of the 4th two-pointer comparison) |
| 4 | e-search-probes | 2 | at-search | numeric |
| 5 | e-stack-top | 2 | ds-stacks | choice, array in stack mode |
| 6 | e-heap-sift | 2 | ds-trees | numeric, array |
| 7 | e-loop-halving | 3 | at-complexity | choice |
| 8 | e-adj-memory | 3 | gd-graphs | numeric |
| 9 | e-front-insert | 3 | ds-arrays | numeric |
| 10 | e-latency-order | 3 | gd-paths | order, weighted graph (Dijkstra settle order) |
| 11 | e-two-sum-trace | 3 | ds-hashing | table, array |
| 12 | e-quick-sorted | 3 | at-sort | numeric |
| 13 | e-kahn-ready | 3 | gd-traversal | tap-regions on directed graph (Kahn's second round) |
| 14 | e-window-losses | 3 | ds-pointers | numeric, array |
| 15 | e-slice-recursion | 3 | at-recursion, at-complexity | multi |
| 16 | e-knap-cells | 3 | gd-dp | tap-regions on grid (cells a knapsack cell fills from) |
| 17 | e-cancel-list | 3 | ds-lists | choice |
| 18 | e-auction-greedy | 3 | at-greedy | numeric, table |
| 19 | e-prune-tree | 3 | gd-backtrack | tap-regions on tree (pruned branches) |
| 20 | e-code-lifo | 3 | ds-stacks | code |
| 21 | e-bisect-table | 4 | at-search | table, array |
| 22 | e-code-flat | 4 | ds-hashing, ds-arrays | code |
| 23 | e-recurrence | 4 | at-recursion, at-complexity | numeric |
| 24 | e-code-fee | 4 | gd-dp | code |
| 25 | e-bst-delete | 4 | ds-trees | tap-regions on tree (successor and its child) |
| 26 | e-two-trades | 5 | gd-dp, at-greedy | numeric, array |
| 27 | e-code-grid | 5 | gd-paths, ds-trees | code (fresh medium: Dijkstra on a 4-way cost grid) |
| 28 | e-book-design | 5 | ds-trees, ds-hashing, ds-lists, at-complexity | longform, 10-point rubric, full model answer |

Skills: all 16 of the topic are covered (`skills` map is the union of the three course.json files): at-complexity 4, at-recursion 2, at-search 2, at-sort 1, at-greedy 2, ds-arrays 2, ds-hashing 3, ds-pointers 2, ds-stacks 2, ds-lists 2, ds-trees 4, gd-graphs 2, gd-traversal 2, gd-paths 2, gd-backtrack 1, gd-dp 3.

Quant framing: tick feeds, bank exposure graphs, netting trade sizes, undo stacks for amendments, ask heaps, venue latency, client fills, overnight risk jobs, daily P&L windows, hedges under a margin budget, resting-order cancels, execution slots, LIFO realised P&L, fill-time ranges, zero-sum P&L runs, trading with fees, price-level BSTs, hedge-roll cost grids, an order book design.

Fresh against the courses: course code already covers merge-k, sliding-window maximum, top-k, Dijkstra on adjacency lists and right/down grid DP, so the exam's code items are new problems: LIFO P&L with a lot stack, the longest zero-sum run (prefix sums plus a dict), max profit with a fee (two-state DP), and cheapest route on a grid with moves in four directions (needs Dijkstra, not the taught right/down table).

## Code items (app grader in Node Pyodide 0.27.7, `codecheck.mjs`)

| item | tests | solution | starter | wrong versions (each fails) |
|---|---|---|---|---|
| e-code-lifo | 8 | 8/8, max test 4 ms | fails (5 of 8) | FIFO (test 1), whole sale off the top lot (test 4), one lot per sale (test 4) |
| e-code-flat | 10 | 10/10, max test 154 ms | fails all | keeps last index (test 5), no `{0: -1}` seed (test 3) |
| e-code-fee | 10 | 10/10, max test 302 ms | fails all | sell every rise (test 1), single trade (test 1) |
| e-code-grid | 10 | 10/10, max test 819 ms | fails all | right/down DP (test 5), BFS by hops (test 1) |

All compare with `equal` on whole numbers. Large hidden inputs are built in `setup`: 100,000-day P&L lists (seeded `random`, all ones, alternating ±7), 100,000-price paths, and 300 by 300 and 250 by 250 grids (a serpentine wall maze, seeded random costs, a formula grid). Each `how` says that the quadratic approach runs out of time. Checked with `slowcheck.mjs` in Pyodide: the all-pairs zero-sum search (tests 8 and 9), the all-buy-days fee table (test 9), the min-scan Dijkstra (test 10) and repeated full-grid sweeps (test 8) were each still running after 40 s, against the 5 s budget. The CPython sweep on the maze also passed 900 s.

## Numbers computed twice

Every answer was recomputed by a second method in Python: brute force against the scan for the window (7), knapsack (9), interval greedy against exhaustive search (4; earliest start 2, shortest first 3), two-trade DP against split-point brute force (16; one trade 13, greedy 14, unlimited 17, two largest moves 12), the quicksort count by simulation against $n(n-1)/2$ (66), the probe bound by simulated lower-bound searches (20), the heap sift by `heapq` (index 1; `i // 2` parent gives 5), Dijkstra by heap against a hand order (LDN, AMS, PAR, FRA, ZRH, MIL), bisect values against direct counts (1, 4, 5, 7, 6, 1), the recurrence ratio by memoised recursion against $3n^{\log_2 3} - 2n$ (9.06). The code items' small tests were checked against brute force; the large ones by a second algorithm (grouped prefix positions, explicit DP arrays, SPFA on the grids).

## Validation and playthrough

- `node app/tools/validate.mjs`: 0 errors overall, no warning for this file; the manifest now lists `exams/topic-1.8.json`.
- Copy lint (the 1.7 `lint.py`): no `!`, no sentence of 20 words or more, no American spellings.
- `playthrough.mjs --exam topic-1.8`: 28 of 28, passed, desktop and `--mobile`.
- Screenshots reviewed (`scratchpad/exam-1.8/shots`). Fixes made from them: the heap parent formula moved from KaTeX (`//` rendered badly) to code; the Kahn graph re-laid out top to bottom so it is planar and fits a phone; the backtracking tree lost its level labels and uses short branch labels (+A, skip) so it scales larger on a phone; the bisect table uses `L(x)` and `R(x)` so the expressions no longer wrap on a phone.

## Engine notes

- The tree canvas has a fixed 540 px frame, so an eight-leaf decision tree (item 19) and a five-level BST (item 25) scale down on a 390 px phone; labels are small but legible. The graph canvas narrows its frame on phones; the tree does not.
- During the first desktop run the tree canvas threw `ReferenceError: Cannot access 'rootNv' before initialization` (tree.js line 104) while another agent was editing `js/engine/canvas/tree.js`. It cleared on the next run once the edit landed; every later run passed.
- The worker grader in Node does not enforce the 5 s limit, so the quadratic versions' time-outs were measured separately (`slowcheck.mjs`), not through `codecheck.mjs`.

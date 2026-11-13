# Claim ledger: graphs-dp L1 to L3, round 2 blind audit

Auditor: Fable, blind (round 2). Stage 1, full depth. Python checks ran on CPython 3.13.18 (`docs/reports/graphs-dp-L1-3-r2-concepts.py`); page timing claims were also run in Pyodide 0.27.7 under node where stated. Sources: CLRS = Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms*, 3rd ed.; S&W = Sedgewick and Wayne, *Algorithms*, 4th ed.; "run" = executed in the concepts script (check name in brackets).

Columns: file | JSON path | claim (short) | verdict | basis. A row covers the claims of one screen or item that share a basis; every graded key, `wrong[]` value, option `why` and `byKey` line named in a row was checked on its own, and every `test-N` line that names a mistake has its own submission in part C of the script.

## l1-nodes-and-edges

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l1 | screens[0] answer, byKey B/F/C | C's neighbours are A, D, E; B is two edges away via A or D; F joins E | correct | edge set A-B, A-C, B-D, C-D, C-E, E-F read off the canvas |
| l1 | screens[0].explain | neighbours of every node determine the graph | correct | adjacency-list representation, CLRS 22.1 |
| l1 | screens[1] rows, hint 3 | B: A,D; C: A,D,E; D: B,C; E: C,F; F: E | correct | run [l1-adj] |
| l1 | screens[1].explain | adjacency list is a dict of lists; undirected edge appears twice | correct | CLRS 22.1 |
| l1 | screens[2] row C, byKey | row C = 1 0 0 1 1 0; diagonal 0 without self-loop | correct | run [l1-matrix] |
| l1 | screens[2].explain | `M[2][3]` answers an edge query in one step; row C equals column C | correct | symmetric matrix of an undirected graph, CLRS 22.1 |
| l1 | screens[3] key 12, slips 6, 36 | 12 ones; 6 = edges counted once; 36 = all cells | correct | run [l1-matrix]: row sums 2,2,3,2,2,1 |
| l1 | screens[3].explain | undirected matrix is symmetric with 2E ones when no self-loops; V^2 cells whatever E | correct | derivation; hypothesis stated |
| l1 | screens[4] options | directed weighted graph as dict of (neighbour, weight) lists; JPY needs a key; `adj["JPY"]` raises KeyError if absent | correct | run [l1-directed] |
| l1 | screens[4].explain | directed matrix need not be symmetric | correct | CLRS 22.1 |
| l1 | screens[5] solution, starter, tests | solution passes 6 tests, starter fails | correct | run [widgets] |
| l1 | screens[5].byKey test-1 | one-way append fails test 1 | correct | run [fb l1s5 t1] |
| l1 | screens[5].byKey test-2 | building keys from the edges passes test 1, fails test 2 | correct | run [fb l1s5 t2] |
| l1 | screens[5].byKey test-3 | appending both ends on a self-loop passes 1 to 2, fails 3 | correct | run [fb l1s5 t3] |
| l1 | screens[5].explain | "the build takes O(V + E) time" for a function that also sorts every list | imprecise | the appends are O(V + E); the sort adds O(sum deg log deg). The line says sorting is only for fixed output but still bills the whole build as O(V + E). Finding 11 |
| l1 | screens[5].explain | dict holds 2E entries | correct | no self-loops in the six-edge graph; one per self-loop otherwise |
| l1 | screens[6] key `[]`, options | one-way loop leaves `adj["D"]` empty; no KeyError | correct | run [l1-trap] |
| l1 | screens[6].explain | a search from D would stop at once without error | correct | D has no stored neighbours |
| l1 | screens[7].prose | list O(V + E) space, neighbours in O(deg u); matrix O(V^2) space, edge query O(1) | correct | CLRS 22.1 |
| l1 | screens[7].prose | "Most real graphs are sparse" | correct | S&W 4.1 ("huge sparse graphs are typical in practice"); CLRS 22.1 makes the same remark |
| l1 | screens[7] key and options | 10^10 cells; 2e6 list entries; 1e6 edges; 1e5 nodes | correct | run [l1-sizes] |
| l1 | screens[7].explain | 10^10 pointers at 8 bytes is about 80 GB; list is tens of megabytes | correct | 8e10 bytes = 80 GB; 2e6 pointers = 16 MB plus 1e5 list headers |
| l1 | screens[8].prose, explain | `[[0] * n] * n` repeats one row reference; setting `m[0][1]` sets column 1 in every row | correct | run [l1-alias] |
| l1 | screens[8] solution, tests | solution passes, starter fails | correct | run [widgets] |
| l1 | screens[8].byKey test-1 | shared-row build fails test 1 | correct | run [fb l1s8 t1] |
| l1 | screens[8].byKey test-5 | test 5 is n = 0 expecting [] | correct | test list |
| l1 | screens[8].explain | building costs O(V^2) before any edge is read | correct | n rows of n zeros |
| l1 | screens[9].prose | at most one central counterparty | correct | two such firms would each have to post to the other and to nobody (n >= 2) |
| l1 | screens[9] solution, tests | passes 7, starter fails | correct | run [widgets] |
| l1 | screens[9].byKey test-3 | checking only in-degree passes 1 to 2, fails 3 | correct | run [fb l1s9 t3] |
| l1 | screens[9].byKey test-4 | checking only out-degree passes 1 to 3, fails 4 (returns firm 2) | correct | run [fb l1s9 t4] |
| l1 | screens[9].byKey test-5 | n = 1: firm 0 qualifies since into == 0 == n - 1 | correct | vacuous truth; solution returns 0 |
| l1 | screens[9].feedback.correct, explain | two degree counts in one pass, O(V + E); in-degree and out-degree defined | correct | CLRS B.4 |
| l1 | summary.ideas, formula, trap | list O(V + E), matrix O(V^2), storage rules for directed and weighted edges | correct | as above |
| l1 | quiz q-entries | 14 entries; 7 = once; 49 = E^2 | correct | handshake lemma, sum of degrees = 2E |
| l1 | quiz q-lookup | matrix answers an edge check in O(1); list scan up to deg(i); edge list O(E) and order-sensitive | correct | CLRS 22.1 |
| l1 | quiz q-lookup.explain | dict of sets gives O(1) checks with less space | correct | expected O(1) hash lookup; 2E entries against V^2 |
| l1 | quiz q-cells | 10^6 cells; 7,000 = V + 2E; 6,000 = 2E; 99.4% zeros | correct | run [l1-sizes] |
| l1 | quiz q-directed | `adj["score"]` is [] | correct | run [l1-directed] |

## l2-level-by-level

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l2 | screens[0] answer, slips, byKey | day 2 is C, E, F; G and H on day 3 (every A to G route has three edges); B on day 1 | correct | run [l2 rumour days] |
| l2 | screens[0].explain | ring-by-ring spreading is breadth-first search | correct | CLRS 22.2 |
| l2 | screens[1] answer, byKey, explain | BFS order A, B, D, E, C, F, G, H; order within a day is discovery order; first in first out is a queue | correct | run [l2 BFS order] |
| l2 | screens[2] answer, byKey, explain | after B: queue D, E; a node joins once; FIFO finishes one day before the next | correct | hand trace; CLRS Lemma 22.3 |
| l2 | screens[3] steps | queue contents at each step; G not queued twice | correct | hand trace of the solution |
| l2 | screens[4] solution, starter, `how` | passes 7 tests, starter fails; 7 tests as stated | correct | run [widgets]; Pyodide run |
| l2 | screens[4].byKey test-3 | "If D appears twice, mark nodes seen when you queue them" shown at test 3 | imprecise | a mark-on-pop submission fails test 1 first (G appears twice there), so this line never reaches that learner. Run [C l2 screens[4] test-3], Pyodide: first fail 1. Finding 6a |
| l2 | screens[4].byKey test-4 | test 4 starts at X with no neighbours; answer `["X"]` | correct | test list |
| l2 | screens[4].byKey test-7 | a search that calls itself once per node goes 3,000 deep, past the limit | correct | Pyodide run: recursive BFS passes 1 to 6, RecursionError on 7 (limit 3,000 in drill-worker.js); a plain list with `pop(0)` passes in 3 ms |
| l2 | screens[4].explain | `seen` check queues each node once; each edge read once from each end; O(V + E); sorting only fixes the order | correct | CLRS 22.2 |
| l2 | screens[5] key, options, byKey | mark-on-pop gives A, B, D, E, C, F, G, H, G; it terminates; no visits lost | correct | run [l2 trap mark-on-pop order] |
| l2 | screens[5].explain | a node can be queued once per neighbour, O(E) copies | correct | each edge can queue its far end at most once per direction |
| l2 | screens[6] answer, byKey, explain | with two edges gone BFS from A misses C and G; BFS returns the start's connected component; restart from each unseen node to visit all | correct | run [l2 unreachable C, G] |
| l2 | screens[7].prose | each node joins once, each edge read twice, O(V + E); a node first found in round d is d edges away, the fewest | correct | CLRS Theorem 22.5 (unweighted) |
| l2 | screens[7] options, explain | `list.pop(0)` shifts the rest, so BFS can take O(V^2); same order; up to 10^10 moves against 10^5 | correct | CPython list is an array; `deque.popleft` is O(1) (Python docs, collections.deque) |
| l2 | screens[8] solution, tests | passes 7, starter fails; within 2 hops: Alder, Birch, Elm, Fir, Larch, Oak; Hazel is 3 | correct | run [l2 within 2 hops of Cedar], [widgets] |
| l2 | screens[8].byKey test-1 | Hazel appearing means a firm at distance k was expanded | correct | Pyodide run: expand-at-k fails test 1 |
| l2 | screens[8].byKey test-3 | k = 0 gives [] | correct | a record-then-stop submission passes 1 to 2 and fails 3 (Pyodide run) |
| l2 | screens[8].byKey test-7 | "Each neighbour should appear once, so mark firms when they are found" at the triangle test | imprecise | no late-marking submission fails first at test 7: mark-on-pop with a list fails test 5 (Oak twice), unmarked level lists fail test 4, unmarked level sets pass everything. Finding 6b |
| l2 | screens[8].explain | BFS finds each firm at its fewest hops, so `dist` is exact when first seen | correct | CLRS Theorem 22.5 |
| l2 | summary | BFS order, mark on joining, `deque.popleft`, O(V + E), component, round = fewest edges | correct | as above |
| l2 | quiz q-queue-kind | queue gives level order; a stack dives; a set has no order | correct | definitions |
| l2 | quiz q-star | 6 nodes queued after the centre; slips 7 and 1 | correct | hand count |
| l2 | quiz q-fx-chain | first found in round 3 means the shortest chain has 3 trades; BFS counts edges not costs; not the number of routes | correct | CLRS Theorem 22.5; the weights caveat is stated |
| l2 | quiz q-disconnected | prints ['X', 'Y']; Z never looked up | correct | hand trace |

## l3-going-deep

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l3 | screens[0] answer, byKey, explain | DFS order A, B, E, G, C, D, F, H; BFS gave A, B, D, E, C, F, G, H | correct | run [l3 DFS pre-order and post-order] |
| l3 | screens[1] answer, byKey, explain | first dead end is F, then H; stepping back is backtracking, done by a returning call | correct | hand trace |
| l3 | screens[2] solution, tests, `how` | passes 6, starter fails | correct | run [widgets] |
| l3 | screens[2].byKey test-4 | "Test 4 is a triangle. If it never finished, a node was visited twice: check `seen`" | imprecise | a submission with no `seen` check, or a parent-only check, raises RecursionError on test 1 (the lesson's graph has a loop), so the line never reaches it. Finding 6c |
| l3 | screens[2].byKey test-3 | single node gives `["A"]` | correct | test list |
| l3 | screens[2].explain | `seen` stops walking round a cycle; each node once, each edge twice; O(V + E) like BFS | correct | CLRS 22.3 |
| l3 | screens[3] key, options, byKey | no `seen` on a triangle raises RecursionError; default limit about 1,000 frames; no call returns | correct | Python docs, `sys.getrecursionlimit` (default 1000); run |
| l3 | screens[3].explain | "On a tree there is no cycle, so the bug can hide until real data arrives" | imprecise | true only for a tree stored as parent-to-child arrows. With an undirected tree stored at both ends, as lessons 1 to 3 store graphs, A calls B and B calls A for ever. Run [l3 screens[3].explain]. Finding 7 |
| l3 | screens[3].explain | a loop-based search without `seen` would hang; recursion fails fast | correct | the stack grows without bound; RecursionError at the limit |
| l3 | screens[4] key, options | sorted pushes give A, D, F, C, G, E, H, B; recursive and BFS orders as stated | correct | run [l3 naive stack order] |
| l3 | screens[4].explain | reverse-sorted pushes with mark and skip on pop match the recursive order exactly | correct | run [l3 stack DFS ... 300 random graphs] |
| l3 | screens[5] solution, tests, `how` | passes 6, starter fails; 5,000-node path is deeper than the recursion limit | correct | run [widgets]; limit 3,000 on the page, 1,000 by default |
| l3 | screens[5].hints[1] | "A node can be on the stack twice, as G is here" (highlight G) | wrong | in the solution on this graph the node pushed twice is D (by A and by C); G is pushed once. With sorted pushes it is B. chk run: pushes {'D': 2}. Finding 5 |
| l3 | screens[5].byKey test-1 | A, D, F, ... means the largest neighbour came off first | correct | Pyodide run: sorted-push fails test 1 |
| l3 | screens[5].byKey test-3 | "Test 3 is a square. If D appeared twice, skip a popped node already in `seen`" | imprecise | a no-skip submission fails test 1 first (D twice there); on the square the repeated node is C, not D. Finding 6d |
| l3 | screens[5].byKey test-6 | a recursive helper hits the frame limit on 5,000 nodes | correct | Pyodide run: RecursionError on test 6 only |
| l3 | screens[5].explain | a node may sit on the stack twice; skip on pop handles it; a list stack has no depth limit | correct | hand trace |
| l3 | screens[6] answer, byKey, explain | post-order F, D, C, G, H, E, B, A; pre-order and post-order defined; in post-order a node follows all it led to | correct | run [l3 DFS pre-order and post-order]; CLRS 22.3 |
| l3 | screens[7].prose, key, options | default limit about 1,000 frames; a 5,000 chain raises RecursionError; raising the limit is not always safe (C stack) | correct | Python docs, `sys.setrecursionlimit`: "a too-high limit can lead to a crash" |
| l3 | screens[7].explain | recursion depth equals the longest path the search follows | correct | one open frame per node on the current path |
| l3 | screens[8] solution, tests, `how` | passes 7, starter fails | correct | run [widgets] |
| l3 | screens[8].byKey test-2, test-3, test-7 | a node with no edges is a component; empty graph has 0; a recursive search runs out of frames on 3,000 nodes | correct | Pyodide runs: only-nodes-with-edges fails 2; recursive fails 7 with RecursionError |
| l3 | screens[8].explain | counting is O(V + E); BFS works as well | correct | CLRS 22.3 / 22.5 exercise |
| l3 | screens[9].prose, hints, explain | in a directed graph a cycle needs an edge to a node on the current path; three states | correct | CLRS Lemma 22.11 (back edge to a grey node) |
| l3 | screens[9] solution, tests | passes 7, starter fails | correct | run [widgets] |
| l3 | screens[9].byKey test-2, test-3, test-5 | plain `seen` calls a diamond a cycle; self-read is a cycle; start from every rule | correct | Pyodide runs: plain-seen fails 2, first-rule-only fails 5 |
| l3 | summary | DFS, both versions need `seen`, pre and post order, 1,000 frames by default, O(V + E) | correct | as above |
| l3 | quiz q-holdings | BFS and DFS reach the same component | correct | both mark exactly the reachable set |
| l3 | quiz q-cc | 4 components; slips 2 and 6 | correct | hand count |
| l3 | quiz q-tree | 0 meetings on a tree ignoring the parent edge; DFS tests treeness (no such edge, all reached) | correct | a tree is a connected acyclic graph, CLRS B.5 |
| l3 | quiz q-post | post-order U, S, T, R; pre-order R, S, U, T; reverse R, T, S, U | correct | hand trace |

## l4-islands

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l4 | screens[0], screens[1] | marked island has 3 cells; 6 islands; diagonal slip 4; 14 land cells | correct | run [l4 islands 6, diagonal slip 4, 14 land cells] |
| l4 | screens[1].explain | island count is the component count with cells as nodes; each search must mark | correct | lesson 3 method |
| l4 | screens[2] solution, tests, byKey, explain | passes 6, starter fails; no bounds check fails the corner; `grid[-1]` is the last row | correct | run [widgets]; Pyodide run no-bounds fails 2 |
| l4 | screens[3] key, slips, explain | 4,000,000 looks at most on 1,000 by 1,000; O(rc) | correct | 10^6 cells times 4 |
| l4 | screens[4] solution, tests, `how` | passes 11, starter fails | correct | run [widgets] |
| l4 | screens[4].byKey test-2, test-10 | `[]` needs the guard; sinking fails the unchanged-grid test | correct | Pyodide runs: fail 2 (IndexError), fail 10 |
| l4 | screens[4].byKey test-5 | "Test 5 is two cells meeting at a corner ... Use only the four side neighbours" | imprecise | an 8-neighbour submission fails test 1 first (4 islands instead of 6). Finding 6e |
| l4 | screens[4].byKey test-11 | 20 by 20 island, answer 1 | correct | test list; a recursive flood fill 400 deep passes on the page (Pyodide run) |
| l4 | screens[4].explain | mark on push; `seen` costs O(rc) memory; stack avoids depth limits | correct | derivation |
| l4 | screens[5] key, options, explain | prints `2 [[0, 0, 0], [0, 0, 0]]`; `grid.copy()` is shallow | correct | Python data model: lists are passed by reference; `list.copy` is shallow |
| l4 | screens[6] key, options, explain | recursive flood on 300 by 300 land has about 90,000 open calls; BFS is O(rc) too | correct | run [l4 recursion depth on all land equals the cell count] (order up, down, left, right) |
| l4 | screens[7] | grid pattern, O(rc) time and space; 4 neighbours; 8 if corners count | correct | derivation |
| l4 | screens[8] solution, tests | passes 7, starter fails; regions 2, 1, 0, 2 | correct | run [l4 loss regions] |
| l4 | screens[8].byKey test-1, test-2, explain | two regions at £50k (crash and rally, vol up); one at £10k through the +4 column | correct | run; grid read |
| l4 | screens[8].byKey test-6, tests[5] | "Test 6 checks the boundary: −50 is not below −50" | wrong | `[[-50, -51]]` has 1 region under `<` and under `<=`, so the test cannot check the boundary; a `<=` submission passes all 7 tests (Pyodide run). Finding 4 |
| l4 | screens[8] canvas caption | P&L of a short straddle book: losses for large spot moves and for vol up | correct | short straddle is short gamma and short vega, Hull ch. 12 and 19 |
| l4 | summary, quiz q-corr | a thresholded correlation matrix is an adjacency matrix, not a map | correct | cell (i, j) is a pair of stocks |
| l4 | quiz q-x, q-mark, q-row | 5 islands (1 with corners); `seen` set leaves the grid intact; 3 runs | correct | run [l4 quiz X grid]; hand count |

## l5-tasks-in-order

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l5 | screens[0] | four valid orders; topological order and DAG defined | correct | run [l5 four valid orders]; CLRS 22.4 |
| l5 | screens[1], screens[2] | in-degrees 0, 0, 2, 1, 1, 2, 1; signals and risk free after returns; Kahn's algorithm described | correct | hand count; Kahn (1962) as in CLRS exercise 22.4-5 |
| l5 | screens[3] solution, tests, `how` | passes 8, starter fails; expected order calendar, prices, returns, risk, signals, backtest, report | correct | run [widgets], [l5 Kahn order] |
| l5 | screens[3].byKey test-1, test-3, test-6 | plain queue puts risk after signals; no cycle check returns [] not None; empty graph gives [] | correct | Pyodide runs: fail 1, 3, 6 respectively |
| l5 | screens[3].explain | O(V + E), or O(V log V + E) with the heap; a task on a cycle is never emitted | correct | CLRS 22.4; heap of at most V items |
| l5 | screens[4] key, options, explain | pre-order from sorted names starts with backtest; full result backtest, report, calendar, returns, risk, signals, prices; from calendar it still reaches backtest before signals | correct | run [l5 pre-order trap and post-order] |
| l5 | screens[5] answer, explain | appended report, backtest, risk, signals, returns, calendar, prices; reversed is a valid order on any DAG from any start | correct | run; CLRS Theorem 22.12 |
| l5 | screens[6] key, slips, explain | with backtest → risk added Kahn emits 4; fewer than V emitted means a cycle | correct | run [l5 Kahn stalls after 4] |
| l5 | screens[7] | O(V + E); leftover nodes always mean a cycle (each has an arrow in from a leftover; walking back must repeat) | correct | pigeonhole on a finite set |
| l5 | screens[8] solution, tests, byKey, explain | passes 7, starter fails; order market_data, positions, scenarios, pnl_vectors, var_report, limits_check | correct | run [widgets]; Pyodide run no-raw-inputs fails 1 |
| l5 | summary | topological order exists only without a cycle; pre-order is not valid | correct | CLRS 22.4 |
| l5 | quiz | 24 orders; a, c, b only; post-order lists a task after its dependents; in-degree 3 | correct | run [l5 quiz] |

## review-1 and homework-1

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-1 | r-entries | 30 entries; 25 is V + E; 100 is V^2 | correct | 2E |
| review-1 | r-bfs-order, r-dfs-order | BFS P, Q, S, R, T, U; DFS P, Q, R, U, T, S; sorted-push stack P, S, T, U, R, Q | correct | run [review-1 BFS and DFS orders]; hand trace of the stack |
| review-1 | r-islands | 4 islands; 3 with corners; 10 land cells | correct | run [review-1 islands] |
| review-1 | r-topo | load, clean, features, calendar, model is invalid; the other two valid | correct | features needs calendar |
| review-1 | r-pop | `deque.pop()` makes it a stack; all reachable nodes still visited; rounds no longer distances | correct | marking on push still visits each node once |
| review-1 | r-kahn-cycle | Kahn emits 3; d has in-degree 3 | correct | run [review-1 Kahn emits 3] |
| review-1 | r-has-path solution, tests, byKey | passes 7, starter fails; undirected fails 2; check-on-discovery fails 4; recursion fails 7 | correct | run [widgets]; Pyodide runs |
| homework-1 | h-fx-hops | passes 7, starter fails; GBP to SEK is 3 | correct | run [widgets] |
| homework-1 | h-contagion-days | passes 8, starter fails; multi-source BFS; first-source-only fails 2; no-reach-check fails 5; 999 on the 2,000 chain | correct | run [widgets]; Pyodide runs |
| homework-1 | h-rounds | passes 8, starter fails; 5 rounds for the VaR run; layers equal the longest chain | correct | run [widgets]; Pyodide runs for test-1, 3, 4, 7 lines |
| homework-1 | h-kahn-steps | step order | correct | lesson 5 |
| homework-1 | h-matrix-gb | 3.2 GB; slips 0.4 and 0.00016; list 3.2 MB | correct | run [hw1 matrix GB] |
| homework-1 | h-ring | 2 islands; 16 border cells | correct | run [hw1 ring] |
| homework-1 | h-exposed | reverse the arrows and search from Z | correct | losses flow from a firm to its owners |
| homework-1 | h-overnight-hang model, rubric | Kahn, O(V + E), leftover means cycle, three-state DFS reports it, batches equal longest chain | correct | CLRS 22.4; derivations above |
| homework-1 | h-split-desks solution, tests, `how` | passes 12, starter fails; two-colouring by BFS; an equal-group neighbour closes an odd loop; O(D + C) plus the sort | correct | run [widgets]; a graph is bipartite iff it has no odd cycle (König; CLRS B.4) |
| homework-1 | h-split-desks byKey test-2 to test-10 | each named mistake fails first at its test | correct | Pyodide runs: one-way 2, no-clash-check 3, first-set-only 4, adj-from-conflicts 5, given-order 6, any-loop-is-clash 7, one-conflict-at-a-time 8, clash-only-in-first-set 9, recursive 10 (RecursionError) |

## l6-fewest-steps

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l6 | screens[0], screens[1] | fewest route A, E, F, H (3 hops); others 4; ring 2 is C, F, G; D and H in ring 3 | correct | run [l6 rings and queue order] |
| l6 | screens[2] | queue order A, B, E, C, F, G, D, H; parents F: E, D: C, H: F; parent is one ring nearer | correct | run; hand trace |
| l6 | screens[3] | walk back gives ['H', 'F', 'E', 'A']; reversed is the route | correct | hand trace |
| l6 | screens[4] solution, tests, `how` | passes 9, starter fails | correct | run [widgets] |
| l6 | screens[4].byKey test-1, test-4, test-5 | unreversed walk or deep-first route fails 1; C to C is ['C']; check `t in parent` | correct | Pyodide runs: not-reversed 1, same-node-empty 4, no-reach-check 5 (KeyError) |
| l6 | screens[4].explain | `parent` marks and remembers; O(V + E) | correct | CLRS 22.2 |
| l6 | screens[5] | DFS returns A, B, C, D, G, E, F, H (7 hops); DFS finds a route, not the shortest | correct | run [l6 trap DFS route] |
| l6 | screens[5].explain, screens[6] | the queue hands out every node k hops away before any k + 1 away, which is why first found is shortest | correct | CLRS Lemma 22.3, Theorem 22.5; unweighted graph stated in the lesson title and objectives |
| l6 | screens[7] | 2 intermediaries, 3 hops, several routes tie | correct | run [l6 settlement: 3 hops] |
| l6 | screens[8] solution, tests, prelude | passes 8, starter fails; NGN to THB is 4; twelve pairs | correct | run [widgets] |
| l6 | screens[8].byKey test-1, test-7 | 5 means currencies counted; MXN in no pair needs `adj.get` | correct | Pyodide runs: fail 1, fail 7 (KeyError) |
| l6 | screens[8].byKey test-3 | "Test 3 goes from HUF back to GBP ... add both directions" | imprecise | pairs stored one way fail test 1 first (NGN to THB returns −1 in either direction). Finding 6f |
| l6 | screens[8].explain | with equal spreads fewer hops always cost less; unequal spreads need weights | correct | cost = hops times spread |
| l6 | summary, quiz q-cost | O(V + E) with an adjacency list; O(V^2) with a matrix; V pops plus 2E checks | correct | CLRS 22.2 |
| l6 | quiz q-same, q-weights, q-maze | ['B']; BFS returns the 4.0 bp direct route though 2.7 bp exists; maze 6 moves | correct | run [l6 quiz maze 6 moves] |

## l7-dijkstra

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l7 | screens[0] | cheapest A, C, B, D, F at 7; others 8, 9, 9 | correct | run [l7 route costs 7, 8, 9, 9] |
| l7 | screens[1] | with every cost at least 0 the smallest tentative cost is final | correct | CLRS Theorem 24.6 |
| l7 | screens[2] states | heap contents after each pop; stale (4, B) skipped; D pops at 4 and lowers F to 7; ties to the earlier letter | correct | run [l7 costs and pop order]; tuple ordering |
| l7 | screens[3] | at most E + 1 heap entries; O(log V) each since E <= V^2; heap version O((V + E) log V); list version O(V^2); Bellman-Ford O(VE) | correct | CLRS 24.3 (binary heap), 24.1; lazy deletion keeps the heap at most E + 1 |
| l7 | screens[3].explain | list scan pays off only when nearly every pair is joined | correct | E about V^2 gives V^2 log V for the heap |
| l7 | screens[4] solution, tests, prelude | passes 9, starter fails; hub at 300 with 299 stale entries | correct | run [widgets], [l7 test 9] |
| l7 | screens[4].byKey test-1, test-9 | B at 4 from seen-on-push or record-on-pop; no stale check reads the hub more than once | correct | Pyodide runs: seen-on-push 1, no-stale-check 9 only |
| l7 | screens[4].byKey test-2 | "Test 2 starts at G ... Every other node must still be in the dict" | imprecise | a dict of reached nodes only fails test 1 first, since G is unreachable from A there. Finding 6g |
| l7 | screens[4].explain | without the check the answer stays right here, stale entries redo work | correct | the `nd < dist[v]` guard keeps costs right |
| l7 | screens[5] key | record-on-pop gives B 4 | correct | run [l7 trap record-on-pop] |
| l7 | screens[5].explain | "Here B ends at 4 and F at 9, both wrong" | imprecise | D also ends wrong, at 6 against a true 4 (the canvas shows D·6). Run [l7 screens[5].explain]. Finding 8 |
| l7 | screens[5].explain | fix: `if u in dist: continue` after the pop | correct | first pop of a node is final with non-negative weights |
| l7 | screens[6] | true cost 1; textbook Dijkstra keeps 2; re-pushing code gets 1 but loses its speed bound; a negative loop means no cheapest cost | correct | run [l7 negative arrow]; CLRS 24.3 and 24.1 |
| l7 | screens[7] | O((V + E) log V) when every w >= 0; equal weights give 5 times the BFS distance | correct | derivation |
| l7 | screens[8] | £260 at 2.6 bp; slips 400, 270, 290; settles EUR 0.5, USD 1.1, CHF 1.2, JPY 2.6; exact compounding £259.98 | correct | run [l7 FX costs], [l7 exact compounding] |
| l7 | screens[9] solution, tests, byKey | passes 8, starter fails; 103.4 through Chicago against 115.2 | correct | run [l7 latency map]; Pyodide runs sum-of-costs 1, max-of-finite 4, nodes-from-links 8 |
| l7 | summary.ideas, formula | non-negative weights make the smallest tentative cost final; O((V + E) log V); a negative edge breaks the guarantee | correct | CLRS 24.3 |
| l7 | summary.trap | "Without the stale check, an old larger entry can pop later and overwrite a correct cost" | imprecise | true only for a version that records the cost at each pop (screens[5]). In the taught pattern the cost is set at the push, so leaving out the check costs time, not correctness, as screens[4].explain says. Finding 9 |
| l7 | quiz q-seen, q-single, q-sparse, q-pushes | B 4; {'X': 0}; about 10^7 against 10^10; at most E + 1 = 10 entries | correct | run [l7 quiz seen-on-push], [l7 quiz sparse], [l7 quiz: 6 nodes, 9 edges] |

## l8-groups

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l8 | screens[0], screens[1] | groups chain through links; one link merges two whole groups; representative, union | correct | disjoint-set forests, CLRS 21.1 |
| l8 | screens[2] | find(7) is 2 in three steps; same root iff same group | correct | run [l8 find(7)] |
| l8 | screens[3] | path compression re-points 7 and 6 only | correct | hand trace |
| l8 | screens[4] | point the smaller root at the larger; depth at most log2 n | correct | S&W 1.5 Proposition H (weighted quick-union) |
| l8 | screens[5] solution, tests, `how` | passes 9, starter fails; 10,000 finds on a 5,000 chain; a recursive find can go 5,000 deep | correct | run [widgets]; Pyodide: solution 4 ms, naive find 921 ms (fast is False), recursive find RecursionError |
| l8 | screens[5].byKey test-5, test-7, test-9 | self-union must return False and keep 3 groups; re-pointing the node splits 1 from 2; walking the chain fails the timing | correct | Pyodide runs: count-drops 5, repoint-node 7, naive and recursive find 9 |
| l8 | screens[5].explain, screens[7].prose, summary.formula | m operations cost O(m α(n)); α(n) at most 4 in practice | correct | CLRS Theorem 21.14; Tarjan and van Leeuwen (1984) for linking by size |
| l8 | screens[6] | `parent[a] = b` loses the link; False; fix joins the roots | correct | hand trace |
| l8 | screens[7] key, explain | 4 components: {0, 1, 2, 3}, {5, 6}, {4}, {7} | correct | run [l8 screens[7]: 4 components] |
| l8 | screens[7].wrong edges = 3, byKey.edges | "You counted only the groups with edges" | wrong | the groups with edges are {0, 1, 2, 3} and {5, 6}: that count is 2, not 3. Run [l8 screens[7] slip "edges"]. Finding 1 |
| l8 | screens[8] | Kruskal's steps; MST definition; sorting O(E log E) dominates; a skipped edge joins nodes already connected | correct | CLRS 23.2 |
| l8 | screens[9] solution, tests, byKey, explain | passes 7, starter fails; five clusters at 0.7; no-abs fails 1; `>=` fails 3; grouping by parent fails 7 | correct | run [l8 five clusters]; Pyodide runs |
| l8 | quiz | 3 settlement groups; `False 4`; 2 clients; O(n^2) for n finds on a chain | correct | run [l8 quiz netting]; hand count |

## l9-arbitrage-cycle

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l9 | screens[0] | GBP, USD, EUR loop returns 1.004824; CHF loop 0.998108; other loops below 1 | correct | run [l9 loop products] |
| l9 | screens[1] | break-even r = 1/1.1684 = 0.855871; 0.86 still makes 0.48% | correct | run [l9 break-even rate] |
| l9 | screens[2] | weights −0.239017, 0.083382, 0.150823 sum to −0.004812; slips; negative cycle | correct | run [l9 log weights] |
| l9 | screens[3] | pass table B 2; C 5; D 6; V − 1 passes always suffice | correct | run [l9 pass table]; CLRS Lemma 24.2 (no negative cycle reachable; the next screen adds the detector) |
| l9 | screens[4] solution, tests, byKey | passes 9, starter fails; one pass fails 1; no detection fails 3; a zero cycle is not negative | correct | run [widgets]; Pyodide runs |
| l9 | screens[4].explain | O(VE); extra pass detects; unreachable cycle stays at ∞ | correct | CLRS 24.1 |
| l9 | screens[5] | with w = −rate every loop sums below 0 (−3.05, −3.012) | correct | run [l9 log weights] |
| l9 | screens[6] | `-log(1.25) - log(0.8)` is −5.55e−17 so prints True | correct | Pyodide 0.27.7 run: −5.551115123125783e−17; same in CPython 3.13 |
| l9 | screens[7] | derivation product > 1 iff sum of −ln r < 0; steps reversible | correct | ln is strictly increasing |
| l9 | screens[8] | cross 0.854331; gross 1.0000359; −£264.03 after 3 bp; £35.95 gross | correct | run [l9 after costs] |
| l9 | screens[8].explain | triangular arbitrage rarely survives costs | correct | Fenn, Howison, McDonald, Williams and Johnson (2009), "The mirage of triangular arbitrage in the spot foreign exchange market", IJTAF 12(8) |
| l9 | screens[9] solution, tests, byKey | passes 10, starter fails; −rate fails 2; no eps fails 4; no start node fails 9; £4,824 on £1m | correct | run [widgets], [l9 test products]; Pyodide runs |
| l9 | summary, quiz | 320 relaxations; 0.99949 round trip; implied cross 0.8400; Dijkstra needs weights >= 0 | correct | run [l9 quiz] |

## review-2 and homework-2

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-2 | r-walk-back, r-compress | ['S', 'A', 'C', 'T']; [0, 0, 0, 0, 0] | correct | hand trace |
| review-2 | r-dijkstra, r-stale | cost 8; slips 14, 11; 3 stale pops | correct | run [review-2 Dijkstra 8 and 3 stale pops] |
| review-2 | r-loop | 1.000579; slip 192.059135; 5.8 bp | correct | run [review-2 loop] |
| review-2 | r-kruskal | 11; slips 10, 15 | correct | run [review-2 Kruskal 11] |
| review-2 | r-passes | 5 passes; slips 1, 6 | correct | run [review-2 chain] |
| review-2 | r-choose | union-find for growing connectivity; O(α(n)) per operation | correct | CLRS 21.3 (amortised) |
| homework-2 | h-maze | passes 8, starter fails; counts-cells fails 1; no start-wall check fails 4 | correct | run [widgets]; Pyodide runs |
| homework-2 | h-within-k solution, tests, explain | passes 9, starter fails; Bellman-Ford cut at k + 1 rounds from a copy; O(k E) | correct | run [widgets]; CLRS 24.1 path-relaxation property |
| homework-2 | h-within-k byKey test-1, test-7 | k rounds instead of k + 1 fails 1; no route gives −1 | correct | Pyodide run: k-rounds fails 1 |
| homework-2 | h-within-k byKey test-2 | "Copy the costs each round so one round adds only one conversion" at test 2 | imprecise | a no-copy submission, and plain Dijkstra, fail test 1 first (2.6 instead of 4.0). Finding 6h |
| homework-2 | h-clients | passes 7, starter fails; direct-shares-only fails 1 | correct | run [widgets]; Pyodide run |
| homework-2 | h-dijkstra-proof | proof order; non-negative weights carry line 4 | correct | CLRS Theorem 24.6 |
| homework-2 | h-latency, h-triangle, h-pick | 103.4 ms; £1,195.55 (gross 1,796.51, one cost 1,596.15); Bellman-Ford | correct | run [l7 latency map], [hw2 triangle] |
| homework-2 | h-scanner model, rubric | bid and 1/ask edges; −ln weights; V − 1 passes plus one; start node; 31 × 830 relaxations; cycle recovery by V parent steps; tolerance | correct | run [hw2 scanner arithmetic]; CLRS 24.1; cycle recovery is the standard Bellman-Ford predecessor walk |
| homework-2 | h-cheapest-count solution, tests, explain | passes 11, starter fails; counts are final when a venue leaves the heap because fees are at least 1; O((V + E) log V) | correct | run [widgets]; positive weights make every cheapest predecessor pop first |
| homework-2 | h-cheapest-count byKey test-2, 3, 5, 7, 8, 11 | each named mistake fails first at its test | correct | Pyodide runs: tie-adds-1 2, cheaper-keeps-count 3, no stale check with `cost[u]` 5, undirected 7, dict of linked venues 8; test 11 has 358,584,264,000 routes |
| homework-2 | h-cheapest-count byKey test-4 | "The answer is known only when AMS comes off the heap" at test 4 | imprecise | returning when AMS is first reached fails test 1 first, with (3, 1) instead of (3, 2). Finding 6i |

## l10-every-subset

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l10 | screens[0], [1], [3] | 8 holdings; half contain B; 1,024 for 10 stocks; walk visits 2^(n+1) − 1 nodes | correct | run [l10 counts] |
| l10 | screens[2] | walk order; B C is fifth; backtracking defined | correct | run [l10 walk order] |
| l10 | screens[4], [6] | 6 orderings; n!; 120 for 5 | correct | run [l10 counts] |
| l10 | screens[5] | storing `path` gives eight empty lists | correct | one list object, emptied by the pops |
| l10 | screens[7] | order of the walk body | correct | lesson code |
| l10 | screens[8] | 8 lists, 4 holdings; 6 if repeats counted | correct | run [l10 duplicate ticker] |
| l10 | screens[9] solution, tests, `how` | passes 11, starter fails | correct | run [widgets] |
| l10 | screens[9].byKey test-1, test-2, test-7 | skip-first fails 1; empty input must give [[]] in both | correct | Pyodide runs: fail 1, 2, 7 |
| l10 | screens[9].byKey test-5 | "Test 5 found fewer than 8 distinct lists. You stored `path` itself" | imprecise | storing `path` itself fails test 1 first (every list is []); no submission that passes test 1 can fail test 5, since 8 different contents are 8 objects. Finding 6j |
| l10 | screens[10], [11] | 42 portfolios; slips 41, 20, 64, 120; 12.4 days; 40 stocks about 35 years | correct | run [l10 counts], [l10 thirty stocks] |
| l10 | quiz | no-pop output; 1 list for []; 24 orders; 15 calls | correct | run [l10 quiz no pop] |

## l11-dead-ends

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l11 | screens[0], [1], [2] | 6 safe cells; r3c1, r4c1, r4c3; 2 placements | correct | run [l11 queen counts] and hand check of the cells |
| l11 | screens[3], summary.formula | 341 against 17 (1, 4, 6, 4, 2); 19,173,961 against 2,057 for 8 queens | correct | run [l11 four queens node counts], [l11 eight queens] |
| l11 | screens[4] | three take-6 branches refused; with positive numbers a total never comes back | correct | hand trace |
| l11 | screens[5] | combos([2, 3, 5], 8) has 3 lists; 6 if order counted | correct | run [l11 combos] |
| l11 | screens[6] | unsafe prune returns False though 6 − 4 = 2 | correct | run [l11 trap and review-3] |
| l11 | screens[7] | sorted positive: if `xs[i]` overshoots, all later do | correct | monotonicity |
| l11 | screens[8] solution, tests, `how` | passes 13, starter fails; about 67 million calls without pruning | correct | run [widgets], [l11 test 13 size]; Pyodide: the unpruned walk takes 10.6 s on test 13, past the 5 s limit |
| l11 | screens[8].byKey | no undo gives fewer than 2; empty subset sums to 0; test 13 needs the cut | correct | Pyodide runs: no-undo 2, empty-list-special-case 10 |
| l11 | screens[9] | budget, rota and count prunes safe; net exposure prune unsafe | correct | monotone quantities |
| l11 | quiz q-three key, explain | 0 placements | correct | run [l11 queen counts] |
| l11 | quiz q-three byKey.two | "You may have checked only columns" for the answer 2 | wrong | checking only columns gives 3! = 6, which is the `orders` slip; nothing in the line produces 2. Run [l11 quiz q-three slip]. Finding 2 |
| l11 | quiz q-full, q-restore, q-combo | 8^8; no undo gives 0; 2 lists | correct | run [l11 eight queens], [l11 combos]; Pyodide run no-undo |

## l12-remembering

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l12 | screens[0], [1] | f(2) three times; calls 1, 1, 3, 5, 9, 15, 25; fib(30) makes 2,692,537 calls; growth about 1.6 per step | correct | run [l12 call counts]; golden ratio |
| l12 | screens[2] | three cache hits; 15 calls become 9; memoisation is top-down DP | correct | run [l12 memoised fib(5)]; CLRS 15.1 |
| l12 | screens[3], [4] | naive column 5, 8, 5, 3, 2, 1, 1; 7 values; 31 values and 59 calls for fib(30) | correct | run [l12 naive column], [l12 memoised fib(30)] |
| l12 | screens[5] | 10 paths = C(5, 2) | correct | run [l12 grid and lattice] |
| l12 | screens[6], [7], [8] | stale 95.24; lists unhashable; default dict shared, one `computing` line | correct | run [l12 prices]; Python docs, functools.lru_cache and default argument values |
| l12 | screens[9] solution, tests, `how` | passes 14, starter fails; grid_paths(18, 18) needs billions of calls uncached | correct | run [widgets], [l12 grid and lattice] |
| l12 | screens[9].byKey test-1, test-12 | base cases count; unmemoised grid times out | correct | Pyodide runs: base-not-counted 1; unmemoised run stopped after 45 s |
| l12 | screens[9].byKey test-4 | "If you got 59, you counted cache lookups" at test 4 | imprecise | counting lookups fails test 3 first, with (8, 11). Finding 6k |
| l12 | screens[9].byKey test-6 | "A count other than 11 means the cache or counter outlived the first call" at test 6 | imprecise | the tests share one namespace, so a module-level or default-argument cache fails test 3 first, with (8, 5). Finding 6l |
| l12 | screens[10] | 496 node values; recombining tree; memo on (step, ups) is the backward induction | correct | Hull ch. 13 (binomial trees); 31 × 32 / 2 |
| l12 | summary, quiz | 25 prices; stale 0.907; 41 calls; (0, 1) | correct | run [l12 prices], [l12 call counts] |

## l13-climbing-stairs

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| l13 | screens[0], [1], [2] | 5 ways; last step from 3 or 4; table 1, 1, 2, 3, 5, 8, 13; bottom-up DP; O(n) | correct | run [l13 stairs tables] |
| l13 | screens[3] | prev 8, cur 13; O(1) space | correct | hand trace |
| l13 | screens[4] | ways(0) = 0 gives 3 | correct | run [l13 stairs tables] |
| l13 | screens[5] | best = 0, 1, 2, 1, 1, 2, 2; greedy gives 3 for 6; greedy can fail, the table cannot | correct | run [l13 coin tables and greedy]; CLRS 16.2 (greedy needs the greedy-choice property) |
| l13 | screens[6] | downward fill returns −1; table 0, 1, ∞, 1, 1, ∞, ∞ | correct | run [l13 wrong direction table] |
| l13 | screens[7], [8] | five-step recipe; three-step recurrence gives 1, 1, 2, 4, 7, 13 | correct | run [l13 stairs tables]; CLRS 15.3 |
| l13 | screens[9] solution, tests, byKey, `how` | passes 15, starter fails; ways(0) = 0 fails 1; memo recursion fails 6; greedy fails 7; −1 for amount 0 fails 8; returning inf fails 9 | correct | run [widgets]; Pyodide runs |
| l13 | screens[10] key | 20 paths = C(6, 3) | correct | run [l13 lattice and hw3] |
| l13 | screens[10].explain | "That is Pascal's triangle: the same recurrence as climbing stairs, on a lattice" | imprecise | Pascal's rule C(i, j) = C(i − 1, j) + C(i, j − 1) is a different recurrence from ways(n) = ways(n − 1) + ways(n − 2); what they share is the split by the last move. Finding 10 |
| l13 | screens[11] | 2 trades for 1,100; greedy 3 | correct | run [l13 coin tables and greedy] |
| l13 | summary, quiz | 0 for amount 0; 4 coins for 11 with 2 and 5 (greedy stuck); 13 ways; ways(0) = 1 | correct | run |

## review-3 and homework-3

| file | path | claim | verdict | basis |
|---|---|---|---|---|
| review-3 | r-four-subsets, r-loop-order | 16 lists; [], [1], [1, 2], [1, 2, 3] first | correct | hand trace |
| review-3 | r-queen-row2, r-negative-prune | 2 safe cells; False | correct | run [l11 trap and review-3] |
| review-3 | r-fib8, r-three-steps, r-coins-greedy | 67; 24; 2 coins with best(10), best(6), best(5), best(2) = 2, 1, 1, 2 | correct | run [l12 call counts], [l13 stairs tables], [l13 coin tables and greedy] |
| review-3 | r-unsafe-cache, r-which-memo | a function reading a global is unsafe to cache; memoisation helps fib and grid paths, not listings or queens | correct | overlapping subproblems, CLRS 15.3 |
| homework-3 | h-combination-sum | passes 8, starter fails; 45 and 192; loop-from-0 fails 1; unsorted fails 3; zero target fails 5 | correct | run [widgets], [hw3 combination counts]; Pyodide runs |
| homework-3 | h-word-break | passes 9, starter fails; len(s) + 1 states; billions of splits of 40 letters | correct | run [widgets], [hw3 word break]; Pyodide: unmemoised run stopped after 45 s |
| homework-3 | h-order-perms | walk order | correct | lesson 10 |
| homework-3 | h-legs key, explain | 12 orders; swapping A and D pairs the orders | correct | run [hw3 h-legs: 12 orders] |
| homework-3 | h-legs byKey.fixed (value 6) | "You fixed A first and D last" | wrong | A first and D last leaves 2 orders; 6 is A first alone (3!). Run [hw3 h-legs slip "fixed"]. Finding 3 |
| homework-3 | h-subset-states, h-lattice, h-complexity | 2,121 states; 252 paths; O(r c) | correct | run [l13 lattice and hw3] |
| homework-3 | h-netting-search prompt, model, rubric | 33,554,432 subsets (over nine hours at 1 ms); 245,506 of size at most 6; count prune safe, net prune unsafe; bound prune |net| > 10k; 22,022 states | correct | run [l13 lattice and hw3] |
| homework-3 | h-fee-trades solution, tests, byKey, explain | passes 11, starter fails; flat and long recurrences; each named mistake fails first at its test | correct | run [widgets], [hw3 fee trades feedback numbers]; Pyodide runs: single trade 2, each rise 3, skips first day 4, skips last day 5, trades below the fee 6, empty raises 7 |

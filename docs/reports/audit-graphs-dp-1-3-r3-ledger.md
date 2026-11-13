# Claim ledger: graphs-dp levels 1 to 3, audit round 3 (blind)

Scope: `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3` in `app/content/courses/graphs-dp/`. Stage 1, full depth.
Rows: 426. Verdicts: correct 417, imprecise 7, unverified 2.
"Script" in the basis column means `docs/reports/graphs-dp-L1-3-r3-concepts.py` (340 checks, exit 0, CPython 3.12 with `sys.setrecursionlimit(3000)` as on the page). "Mutant" means a version of the solution with the named mistake, run against the widget's own tests in that script. CLRS section numbers are from the fourth edition.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-nodes-and-edges | screens[0].widget.answer, feedback.byKey.B/F/C | C's neighbours are A, D, E; B is two edges away through A or D; F joins E only | correct | edges A-B A-C B-D C-D C-E E-F read off; B-A-C and B-D-C both length 2 |
| l1-nodes-and-edges | screens[0].explain | knowing every node's neighbours determines the graph | correct | adjacency lists determine the edge set (CLRS 4e 20.1) |
| l1-nodes-and-edges | screens[1].widget.rows, hints[2] | lists B: A,D; C: A,D,E; D: B,C; E: C,F; F: E | correct | script check `l1_adj` builds them from the lesson's edges |
| l1-nodes-and-edges | screens[1].explain | adjacency list is a dict of lists; undirected edge A-B appears in both lists | correct | CLRS 20.1; script |
| l1-nodes-and-edges | screens[2].widget.rows, feedback | row C is 1 0 0 1 1 0; diagonal 0 without a self-loop | correct | script `l1_matrix` |
| l1-nodes-and-edges | screens[2].explain | `M[2][3]` is one step; row C equals column C because edges work both ways | correct | undirected matrix is symmetric; list indexing O(1) |
| l1-nodes-and-edges | screens[3].widget.answer, wrong edges=6, cells=36, hints[2] | 12 ones; row counts 2,2,3,2,2,1; 6 = edges once; 36 = all cells | correct | script: sum of rows is 12 |
| l1-nodes-and-edges | screens[3].explain | undirected matrix symmetric with 2E ones when no self-loops; V^2 = 36 cells whatever E | correct | a self-loop adds one diagonal 1, so the hypothesis is stated |
| l1-nodes-and-edges | screens[4].widget.options | directed weighted list stores (neighbour, rate) at the start node; JPY keeps an empty list; `adj["JPY"]` on the dict without it raises KeyError | correct | Python dict semantics; run |
| l1-nodes-and-edges | screens[4].explain | directed matrix need not be symmetric; level 2 searches such a graph for a profitable loop | correct | l9 is in level 2 (course.json) |
| l1-nodes-and-edges | screens[5].widget (solution, tests, how) | adj_list passes 6 tests incl. isolated node, self-loop, empty graph; starter fails | correct | script `widgets` |
| l1-nodes-and-edges | screens[5].feedback.byKey.test-1 | one-way append fails test 1 | correct | mutant run: first failing test 1 |
| l1-nodes-and-edges | screens[5].feedback.byKey.test-2 | dict built from edges passes test 1, drops isolated C in test 2 | correct | mutant run: first failing test 2 |
| l1-nodes-and-edges | screens[5].feedback.byKey.test-3 | appending both ends for a self-loop passes 1 to 2, fails 3 | correct | mutant run: first failing test 3 |
| l1-nodes-and-edges | screens[5].explain | building costs O(V + E); lists hold 2E entries without self-loops; sorting adds a little more | correct | V empty lists plus 2E appends; sort is O(sum deg log deg) |
| l1-nodes-and-edges | screens[6].widget, feedback | the one-way loop prints `[]` for D; no KeyError; D is second in both its pairs | correct | run in script `l1_missing_half` |
| l1-nodes-and-edges | screens[6].explain | a search from D finds no neighbours and stops with no error | correct | run: BFS from D on the one-way dict visits only D |
| l1-nodes-and-edges | screens[7].prose | list O(V+E) space, neighbours in O(deg u); matrix O(V^2) space, edge check O(1) | correct | CLRS 20.1 |
| l1-nodes-and-edges | screens[7].prose | "Most real graphs are sparse" | unverified | empirical generalisation with no source; true of the usual examples (road, social, trade networks) but not sourced |
| l1-nodes-and-edges | screens[7].widget.options | 10^10 cells; 2 x 10^6 list entries; 10^6 edges; 10^5 firms | correct | 1e5^2; 1e5*20; 1e5*20/2 |
| l1-nodes-and-edges | screens[7].explain | 10^10 8-byte pointers is about 80 GB; list of 2 million entries is tens of megabytes | correct | 8e10 bytes; 2e6*8 = 16 MB plus 1e5 list headers of 56+ bytes |
| l1-nodes-and-edges | screens[8].prose, explain, feedback.test-1 | `[[0]*n]*n` makes n references to one row, so one write shows in every row; mutant fails test 1 | correct | run: all rows identical; first failing test 1 |
| l1-nodes-and-edges | screens[8].widget | adj_matrix passes 6 tests; starter fails; test 5 has n = 0 and expects [] | correct | script `widgets` |
| l1-nodes-and-edges | screens[8].explain | building the matrix costs O(V^2) before any edge is read | correct | n rows of n zeros |
| l1-nodes-and-edges | screens[9].prose | a counterparty that receives from all others and posts to none is unique if it exists | correct | two such nodes would each have to post to the other |
| l1-nodes-and-edges | screens[9].widget | find_ccp passes 7 tests; starter fails | correct | script `widgets` |
| l1-nodes-and-edges | screens[9].feedback.byKey.test-3 | test 3: firm 2 receives from both others and posts to 0; an in-degree-only check passes 1 to 2 and fails 3 | correct | mutant run |
| l1-nodes-and-edges | screens[9].feedback.byKey.test-4 | test 4: firm 2 has no arrows in or out; an out-degree-only check passes 1 to 3 and fails 4 | correct | mutant run |
| l1-nodes-and-edges | screens[9].feedback.byKey.test-5 | n = 1: into == 0 == n - 1 so firm 0 qualifies | correct | vacuous truth; test expects 0 |
| l1-nodes-and-edges | screens[9].feedback.correct, explain | two degree counts in one pass, O(V + E); in-degree and out-degree definitions | correct | CLRS B.4 |
| l1-nodes-and-edges | summary.ideas, formula, trap | list O(V+E), matrix O(V^2), storage of undirected, directed, weighted edges; one-way append loses reverse edges silently | correct | as above |
| l1-nodes-and-edges | quiz[0] | 7 edges, no self-loops: 14 list entries; 7 = once; 49 = E^2 | correct | 2E |
| l1-nodes-and-edges | quiz[1] | matrix check is one read; `j in adj[i]` scans up to deg(i); `(i, j) in edges` is O(E) and misses (j, i); 250,000 cells | correct | Python list membership is linear; 500^2 |
| l1-nodes-and-edges | quiz[1].explain | a dict of sets gives O(1) checks with less space | imprecise | set membership is O(1) on average, not worst case; and "less space" holds only for a sparse graph. Finding 7 |
| l1-nodes-and-edges | quiz[2] | 10^6 cells; 7000 = V + 2E; 6000 = 2E ones; 99.4% zeros | correct | holds for the undirected, loop-free graph the lesson uses throughout; 1 - 6000/1e6 |
| l1-nodes-and-edges | quiz[3] | directed pipeline: `adj["score"]` is `[]`; no KeyError | correct | run |
| l2-level-by-level | screens[0].widget.answer, wrong.cumulative, explain | day 1: B, D; day 2: C, E, F; day 3: G, H; cumulative set is B, C, D, E, F | correct | script `l2_levels`: BFS distances on the lesson's graph |
| l2-level-by-level | screens[0].feedback.byKey.G/H/B | every route from A to G has three edges; H through B then E on day 3; B on day 1 | correct | simple paths A-B-E-G and A-D-C-G both have 3 edges; script enumerates simple paths |
| l2-level-by-level | screens[1].widget.answer, hints, feedback | BFS order with alphabetical neighbours is A, B, D, E, C, F, G, H | correct | script runs the lesson's `bfs` on the lesson's graph |
| l2-level-by-level | screens[1].explain | within a day the order is discovery order; first in, first out is a queue | correct | CLRS 20.2 |
| l2-level-by-level | screens[2].widget.answer, feedback | after B is processed the queue is D, E and Processed is A, B | correct | script traces queue states |
| l2-level-by-level | screens[2].explain | FIFO is what makes BFS finish one day before the next | correct | CLRS Lemma 20.3 (queue holds at most two consecutive distances, in order) |
| l2-level-by-level | screens[3].steps[0..5] | queue states A; B, D; D, E; E, C, F; C, F, G, H; C finds G already seen | correct | script trace matches every caption |
| l2-level-by-level | screens[4].widget | bfs passes 7 tests (lesson graph from A and H, square, isolated start, disconnected, directed, 3,000-node path); starter fails | correct | script `widgets` |
| l2-level-by-level | screens[4].feedback.byKey.test-1 | marking on pop makes G appear twice in test 1 | correct | mutant run: output has G twice, first failing test 1 |
| l2-level-by-level | screens[4].feedback.byKey.test-3 / test-4 | square answer A, B, C, D; isolated start answer ['X'] | correct | match tests 3 and 4 |
| l2-level-by-level | screens[4].feedback.byKey.test-7 | a search that recurses once per node goes 3,000 deep on the 3,000-node path, past Python's recursion limit | correct | recursive queue-driven BFS passes tests 1 to 6 and raises RecursionError at limit 3000 (page) and at 1000 (default); script |
| l2-level-by-level | screens[4].explain | each node queued once, each edge read once from each end, O(V + E); sorting only fixes the order | correct | CLRS 20.2; the sort cost is set aside in words |
| l2-level-by-level | screens[5].widget.options, feedback | late marking gives A, B, D, E, C, F, G, H, G; it terminates; no node is lost | correct | script runs the screen's code |
| l2-level-by-level | screens[5].explain | with late marking a node can be queued once per neighbour, O(E) copies in all | correct | each edge can enqueue its far end at most once per direction |
| l2-level-by-level | screens[6].widget.answer, explain | with D-C and E-G removed, BFS from A reaches A, B, D, E, F, H and misses C, G; BFS returns the start's connected component | correct | script |
| l2-level-by-level | screens[7].prose | each node joins once, each edge read twice, O(V + E); a node first found in round d is d edges away, the fewest possible | correct | CLRS Theorem 20.5, undirected unweighted graph as on the page |
| l2-level-by-level | screens[7].widget.options | `list.pop(0)` shifts the remaining items, so BFS can take O(V^2); order unchanged | correct | CPython list_pop memmove; a star graph queues V - 1 nodes at once |
| l2-level-by-level | screens[7].explain | up to 10^10 moves against 10^5 with popleft | correct | stated as an upper bound: 1e5 pops x up to 1e5 items (a star gives about 5e9) |
| l2-level-by-level | screens[8].widget | within_hops passes 7 tests; starter fails | correct | script `widgets` |
| l2-level-by-level | screens[8].feedback.byKey.test-1 | expanding a firm at distance k lets Hazel (3 hops) into the k = 2 answer | correct | mutant without the `dist[u] == k` stop: first failing test 1, Hazel present |
| l2-level-by-level | screens[8].feedback.byKey.test-3 | k = 0 returns [] | correct | test 3 |
| l2-level-by-level | screens[8].feedback.byKey.test-5 | with k = 10 Alder and Larch are both expanded and both find Oak; late marking lists Oak twice | correct | mutant (mark on pop, list result) passes tests 1 to 4 and fails 5 with Oak twice |
| l2-level-by-level | screens[8].feedback.byKey.test-7 | triangle with k = 1 gives ['B', 'C'] | correct | test 7 |
| l2-level-by-level | screens[8].explain | BFS distance is exact when a firm is first seen; within 2 hops of Cedar: Alder, Birch, Elm, Fir, Larch, Oak; Hazel is 3 hops | correct | script distances |
| l2-level-by-level | summary | BFS finishes distance d before d + 1; O(V + E) with mark-on-join and popleft; only the start's component; late marking queues a node once per neighbour | correct | as above |
| l2-level-by-level | quiz[0] | queue gives level order; stack gives depth-first; a set has no order | correct | CLRS 20.2, 20.3 |
| l2-level-by-level | quiz[1] | star with 6 leaves: queue holds 6 after the centre; 7 keeps the centre; 1 queues only the first | correct | trace |
| l2-level-by-level | quiz[2] | found in round 3 means the shortest chain has 3 trades; BFS counts edges not costs nor routes | correct | CLRS Theorem 20.5 |
| l2-level-by-level | quiz[3] | `bfs` from X prints ['X', 'Y']; Z never looked up | correct | run |
| l3-going-deep | screens[0].widget.answer, hints, feedback | DFS pre-order from A with alphabetical neighbours is A, B, E, G, C, D, F, H; BFS gave A, B, D, E, C, F, G, H | correct | script runs the lesson's `dfs` and l2's `bfs` on the lesson's graph |
| l3-going-deep | screens[1].widget.answer, feedback, hints[2] | first dead end is F; H is the second, reached last; D still has F | correct | script records dead ends in order: F, H |
| l3-going-deep | screens[1].explain | "steps back to D, C, G and E, each with nothing new. E still has H" | imprecise | D, C and G have nothing new; E has H, as the next sentence says. Finding 1 |
| l3-going-deep | screens[1].explain | a recursive call returning does the backtracking | correct | call stack semantics |
| l3-going-deep | screens[2].widget | recursive dfs passes 6 tests; starter fails | correct | script `widgets` |
| l3-going-deep | screens[2].feedback.byKey.test-1 | without the `seen` check test 1 ends in RecursionError | correct | mutant run at limit 3000 and 1000 |
| l3-going-deep | screens[2].feedback.byKey.test-3, test-4 | single node gives ['A']; triangle gives A, B, C | correct | tests 3, 4 |
| l3-going-deep | screens[2].explain | each node visited once, each edge read twice, O(V + E) like BFS | correct | CLRS 20.3, undirected adjacency list |
| l3-going-deep | screens[3].widget.options, feedback | no-`seen` DFS on a triangle raises RecursionError; A calls B, B calls A; default limit about 1,000 frames | correct | run; `sys.getrecursionlimit()` is 1000 in stock CPython 3.12; the page sets 3000 and the error is the same |
| l3-going-deep | screens[3].explain | a loop-based search with no `seen` would hang; recursion fails fast; a parent-to-child tree hides the bug | correct | stack version pushes for ever; a rooted tree has no path back |
| l3-going-deep | screens[4].widget.options | naive stack order is A, D, F, C, G, E, H, B | correct | script runs the screen's code |
| l3-going-deep | screens[4].explain | the naive order is a valid depth-first order, largest neighbour first; reverse-sorted pushes match the recursive order exactly | correct | script: equals recursive DFS with neighbours reverse-sorted; reverse-push version equals recursive `dfs` on 300 random graphs |
| l3-going-deep | screens[5].widget, how | dfs_stack passes 6 tests incl. a 5,000-node path, deeper than the recursion limit (3000 on the page, 1000 default); starter fails | correct | script `widgets` |
| l3-going-deep | screens[5].feedback.byKey.test-1 | sorted pushes give an order starting A, D, F; no skip on pop makes D appear twice | correct | two mutant runs, both first fail test 1 |
| l3-going-deep | screens[5].feedback.byKey.test-3 | square: C is pushed by A and by D; answer A, B, D, C | correct | traced in script |
| l3-going-deep | screens[5].feedback.byKey.test-6 | a recursive helper hits the frame limit on 5,000 nodes | correct | mutant: passes 1 to 5, RecursionError on 6 at limit 3000 |
| l3-going-deep | screens[5].explain, hints[1] | a node can sit on the stack twice (D here); skip on pop handles it | correct | trace: D pushed by A and by C |
| l3-going-deep | screens[6].widget.answer | post-order is F, D, C, G, H, E, B, A | correct | script |
| l3-going-deep | screens[6].explain | pre-order and post-order definitions; in post-order a node comes after all nodes it led to | correct | CLRS 20.3 finishing times |
| l3-going-deep | screens[7].prose, options, hints | default limit about 1,000; recursive dfs on a 5,000 chain raises RecursionError partway; about 5,000 frames would be open | correct | run at 1000 and at 3000 |
| l3-going-deep | screens[7].widget.options[2].why | raising the limit can overflow the C stack and crash the interpreter | correct | Python docs, `sys.setrecursionlimit`: "a too-high limit can lead to a crash"; hedged with "can" |
| l3-going-deep | screens[7].explain | recursion depth equals the longest path the search follows | correct | one open frame per node on the current DFS path |
| l3-going-deep | screens[8].widget | count_components passes 7 tests; starter fails | correct | script `widgets` |
| l3-going-deep | screens[8].feedback.byKey.test-2, test-3, test-7 | isolated Z gives 2; empty graph gives 0; a recursive search runs out of frames on the 3,000-node path | correct | mutants: start-only-nodes-with-edges fails test 2 first; recursive version passes 1 to 6 and fails 7 at limit 3000 |
| l3-going-deep | screens[8].explain | counting is O(V + E); the outer loop catches other pieces; BFS works as well | correct | CLRS 20.3; each edge is read from each end, by one search only |
| l3-going-deep | screens[9].prose, explain | in a directed graph a visited node is not a cycle unless it is on the current path; spot is done when vega reaches it | correct | CLRS Lemma 20.11 (back edge iff cycle); script trace of states |
| l3-going-deep | screens[9].widget | has_cycle passes 7 tests; starter fails | correct | script `widgets` |
| l3-going-deep | screens[9].feedback.byKey.test-2 | a plain `seen` set calls the diamond a cycle | correct | mutant: passes test 1, fails 2 |
| l3-going-deep | screens[9].feedback.byKey.test-3 | `limit` reads itself: a one-rule cycle | correct | test 3 |
| l3-going-deep | screens[9].feedback.byKey.test-5 | loop c, d, e is unreachable from a; search from every rule | correct | mutant searching from the first rule only: passes 1 to 4, fails 5 |
| l3-going-deep | summary | DFS, both versions need `seen`, reverse pushes, pre and post order, limit about 1,000 by default; O(V + E) | correct | as above |
| l3-going-deep | quiz[0] | BFS and DFS reach the same connected component | correct | both mark exactly the nodes reachable from the start |
| l3-going-deep | quiz[1] | 4 components; 2 counts only groups with edges; 6 counts nodes | correct | run of lesson's count_components |
| l3-going-deep | quiz[2] | DFS on a 10-node tree meets 0 visited nodes apart from the parent; 9 is the edge count; test for a tree | correct | a non-parent edge to a visited node closes a cycle; simple graph assumed, as everywhere in the lesson |
| l3-going-deep | quiz[3] | post-order U, S, T, R; pre R, S, U, T; reversed R, T, S, U; BFS R, S, T, U | correct | run |
| l4-islands | screens[0].widget.answer, wrong.diag, feedback | island of the marked cell is r1c5, r2c4, r2c5; r3c3 touches r2c4 only at a corner | correct | script flood fill on the lesson's grid |
| l4-islands | screens[0].explain | land cells are nodes with up to four neighbours; an island is a connected component | correct | definition (4-connectivity) |
| l4-islands | screens[1].widget.answer, wrong diag=4, cells=14, hints[2] | 6 islands (3, 3, 1, 3, 3, 1 cells); 8-neighbour joining gives 4; 14 land cells | correct | script: 4-connected count 6 with those sizes, 8-connected count 4, land 14 |
| l4-islands | screens[1].explain | scan and start a new island at each unseen land cell; each search must mark what it reaches | correct | l3's component counter |
| l4-islands | screens[2].widget | neighbours passes 6 tests; starter fails | correct | script `widgets` |
| l4-islands | screens[2].feedback.byKey.test-2, explain | no bounds check passes the middle cell and fails corner (0, 0); `grid[-1]` is the last row, so a missing check wraps silently | correct | mutant: first failing test 2; Python negative indexing |
| l4-islands | screens[2].feedback.byKey.test-1 | order up, down, left, right; no diagonals | correct | test 1 |
| l4-islands | screens[3].widget.answer, wrong | 10^6 cells x 4 looks = 4,000,000; 10^6 counts cells; 10^12 pairs every cell with every other | correct | arithmetic; the solution tries 4 candidates per popped cell |
| l4-islands | screens[3].explain | work is O(rc); no adjacency list is built | correct | each cell scanned once, pushed at most once |
| l4-islands | screens[4].widget, how | count_islands passes 11 tests; starter fails | correct | script `widgets` |
| l4-islands | screens[4].feedback.byKey.test-1 | 8-neighbour version returns 4 on the map | correct | mutant: returns 4, first failing test 1 |
| l4-islands | screens[4].feedback.byKey.test-2 | `len(grid[0])` unguarded fails on `[]` | correct | mutant: IndexError on test 2 after passing 1 |
| l4-islands | screens[4].feedback.byKey.test-5 | two cells meeting at a corner are two islands | correct | test 5 |
| l4-islands | screens[4].feedback.byKey.test-10 | the sinking version counts correctly but leaves the grid zeroed | correct | mutant: passes 1 to 9, fails 10 |
| l4-islands | screens[4].feedback.byKey.test-11 | 20 by 20 island of 400 cells, answer 1 | correct | test 11 |
| l4-islands | screens[4].explain | marking on push stops double counting; `seen` costs O(rc) memory; a stack avoids recursion limits | correct | as l2, l3 |
| l4-islands | screens[5].widget.options, explain | sinking version prints `2 [[0, 0, 0], [0, 0, 0]]`; Python passes the same list; `grid.copy()` shares the rows | correct | script runs a sinking counter; `g.copy()[0] is g[0]` |
| l4-islands | screens[6].prose, options, hints | recursive fill (up, down, left, right) on all land snakes through every cell: 16 open calls on 4 by 4, 90,000 on 300 by 300 | correct | script simulates the recursion's maximum depth: 16 and 90,000, with the drawn path on 4 by 4 |
| l4-islands | screens[6].explain | BFS on a grid is also O(rc) | correct | each cell queued once |
| l4-islands | screens[7].prose, options | pattern is O(rc) time and space; neighbours are the four side cells inside the grid; negative indexes wrap by accident | correct | as above; a negative index wraps, an index past the end raises |
| l4-islands | screens[7].explain | 8-neighbour problems change only the step list | correct | same scan and search |
| l4-islands | screens[8].widget | count_loss_regions passes 7 tests; starter fails | correct | script `widgets` |
| l4-islands | screens[8].feedback.byKey.test-1, test-2, explain, hints[1] | at £50k the loss cells are r1c4, r1c5, r5c4, r5c5: 2 regions; at £10k the +4 vol column loses everywhere and joins them: 1 region | correct | script lists cells below -50 and below -10 |
| l4-islands | screens[8].feedback.byKey.test-6 | test 6 is the first non-square grid; taking columns from `len(pnl)` passes 1 to 5 and fails 6; only -51 is below -50 | correct | mutant run |
| l4-islands | screens[8].canvas, explain | a short straddle book loses on a sharp move either way and with vol up | correct | Hull, Options, Futures and Other Derivatives, ch. 12 (straddles): short straddle is short gamma and short vega |
| l4-islands | summary | grid as graph, O(rc), mark on push, diagonals merge islands | correct | as above |
| l4-islands | quiz[0].widget.options[0], explain | a thresholded correlation matrix is an adjacency matrix; clusters are components | correct | definition; cells are pairs, not places |
| l4-islands | quiz[0].widget.options[2].why | counting rows with a 1 "counts stocks with at least one partner" | imprecise | as defined, cell (i, i) is 1 (a stock's correlation with itself is 1 > 0.8), so every row holds a 1 and the count is 50. Finding 2 |
| l4-islands | quiz[1] | X pattern has 5 islands; joining corners gives 1 | correct | script |
| l4-islands | quiz[2].widget.options[0..1], explain | a `seen` set avoids double counting and leaves the grid; sinking damages it; O(rc) memory | correct | as screens[4], [5] |
| l4-islands | quiz[2].widget.options[2].why | with no marks "the search steps back and forth for ever, and the outer loop counts each island again" | imprecise | the two cannot both happen: a search that never ends never returns to the outer loop. Finding 3 |
| l4-islands | quiz[3] | one row: 3 runs of 1s (2, 1, 3 cells); 6 land cells | correct | count |
| l5-tasks-in-order | screens[0].widget.answer, same, explain | four valid orders: prices and calendar either way, signals and risk either way; topological order and DAG definitions | correct | script counts topological orders by brute force: 4; CLRS 20.4 |
| l5-tasks-in-order | screens[1].widget.rows, explain | in-degrees 0, 0, 2, 1, 1, 2, 1; in-degree 0 is free; finishing a task lowers its successors' counts | correct | script |
| l5-tasks-in-order | screens[2].widget.answer, feedback, explain | after prices, calendar, returns: signals and risk are free; backtest waits for both; Kahn's algorithm description | correct | script; Kahn (1962), CLRS exercise 20.4-5 |
| l5-tasks-in-order | screens[3].widget, caption | topo_sort passes 8 tests; expected order calendar, prices, returns, risk, signals, backtest, report; starter fails | correct | script `widgets` |
| l5-tasks-in-order | screens[3].feedback.byKey.test-1 | a plain queue keeps arrival order, so risk lands after signals | correct | deque mutant returns prices, calendar, returns, signals, risk, backtest, report; first failing test 1 |
| l5-tasks-in-order | screens[3].feedback.byKey.test-3 | two-task cycle: nothing is free, order is empty; return None not [] | correct | mutant without the length check: passes 1 to 2, returns [] on 3 |
| l5-tasks-in-order | screens[3].feedback.byKey.test-6 | empty graph gives [] | correct | test 6 |
| l5-tasks-in-order | screens[3].explain | O(V + E), or O(V log V + E) with the heap; a task on a cycle never reaches in-degree 0 | correct | V pushes and pops at O(log V); a cycle node always keeps an arrow in from its cycle predecessor |
| l5-tasks-in-order | screens[4].widget, explain | the pre-order version starts with backtest; full result backtest, report, calendar, returns, risk, signals, prices; from calendar it still reaches backtest through risk before signals | correct | script runs the screen's code, and again starting at calendar |
| l5-tasks-in-order | screens[5].widget.answer, hints, explain | post-order report, backtest, risk, signals, returns, calendar, prices; reversed it is a valid order | correct | script runs it and checks every arrow |
| l5-tasks-in-order | screens[5].explain | on a graph with no cycle reversed post-order is valid from any starting point | correct | CLRS Theorem 20.12; script checks 200 random DAGs with random start orders |
| l5-tasks-in-order | screens[5].feedback.byKey.prices | "prices is tried last by the outer loop" | imprecise | `sorted(adj)` tries backtest, calendar, prices, report, returns, risk, signals; prices is third. It is the last task the loop visits, since the four after it are already seen. Finding 4 |
| l5-tasks-in-order | screens[6].widget.answer, wrong, explain | with backtest to risk added Kahn emits 4 of 7: calendar, prices, returns, signals; report is stuck behind the cycle | correct | script |
| l5-tasks-in-order | screens[7].prose | Kahn is O(V + E); reversed DFS post-order costs the same and needs the three-state check to notice a cycle | correct | CLRS 20.4 |
| l5-tasks-in-order | screens[7].widget.options, explain | leftover nodes lie on a cycle or wait on one; an isolated node is emitted at the start; walking arrows backwards among leftovers must repeat a node | correct | finite set, every leftover has a leftover predecessor (pigeonhole) |
| l5-tasks-in-order | screens[8].widget, explain | run_order passes 7 tests; order market_data, positions, scenarios, pnl_vectors, var_report, limits_check; starter fails | correct | script `widgets` |
| l5-tasks-in-order | screens[8].feedback.byKey.test-1, test-2, test-4 | raw inputs must be nodes; one job with no prerequisites; two-job cycle gives None | correct | mutant using only `deps` keys fails test 1 first; tests 2 and 4 as stated |
| l5-tasks-in-order | summary | a topological order exists only when there is no cycle; often several; Kahn; reversed post-order valid, pre-order not; O(V + E) | correct | CLRS 20.4 |
| l5-tasks-in-order | quiz[0] | four tasks, no arrows: 4! = 24 orders | correct | arithmetic |
| l5-tasks-in-order | quiz[1] | a, c, b is the only valid order | correct | script brute force |
| l5-tasks-in-order | quiz[2] | post-order lists a task after its dependents; reversing puts prerequisites first; reversed post-order is not pre-order | correct | CLRS Theorem 20.12 |
| l5-tasks-in-order | quiz[3] | in-degree of q is 3; 4 counts every arrow touching q; 1 is the out-degree | correct | count |
| l6-fewest-steps | screens[0].widget.answer, wrong, hints[2], explain | fewest-hops route A to H is A, E, F, H (3 hops); top and middle routes take 4; none takes 2 | correct | script enumerates simple A to H paths: lengths 3, 4, 4, and longer |
| l6-fewest-steps | screens[1].prose | "The badges show the visiting order so far" | imprecise | the labels A·0, B·1, E·1 are hop counts, as the caption says; visiting order would be 0, 1, 2. Finding 5 |
| l6-fewest-steps | screens[1].widget.answer, wrong.with-d, explain | ring 2 is C, F, G; D and H are ring 3; ring number is fewest hops because each ring finishes before the next starts | correct | script BFS distances; CLRS Theorem 20.5 |
| l6-fewest-steps | screens[2].prose, rows, explain | queue order A, B, E, C, F, G, D, H; parent F = E; D at 3 with parent C; H at 3 with parent F; C left the queue before G | correct | script runs BFS with sorted neighbours, records dist and parent |
| l6-fewest-steps | screens[3].widget.options, explain | the walk gives ['H', 'F', 'E', 'A']; no None appended; reversed is A, E, F, H; 4 nodes, 3 hops | correct | script runs the screen's loop |
| l6-fewest-steps | screens[4].widget | shortest_path passes 9 tests (incl. s == t, unreachable, directed, tie, 12-ring); starter fails | correct | script `widgets` |
| l6-fewest-steps | screens[4].feedback.byKey.test-1 | a stack gives a longer route; an unreversed walk gives H, F, E, A | correct | two mutants, both first fail test 1 with those outputs |
| l6-fewest-steps | screens[4].feedback.byKey.test-4 | C to C is ['C'] | correct | test 4 |
| l6-fewest-steps | screens[4].feedback.byKey.test-5 | no route to Z: check `t in parent` before walking back | correct | mutant without the check: passes 1 to 4, KeyError on 5 |
| l6-fewest-steps | screens[4].explain | `parent` marks seen and remembers the route; O(V + E) | correct | as l2 |
| l6-fewest-steps | screens[5].widget.options, hints, feedback | DFS `find_path` returns A, B, C, D, G, E, F, H: seven hops; at D sorted neighbours are C, G, H | correct | script runs the screen's code |
| l6-fewest-steps | screens[5].explain | DFS returns the first route it finishes; only the queue's ring order guarantees fewest hops | correct | CLRS 20.2 against 20.3; holds for unweighted graphs, which is the lesson's stated setting |
| l6-fewest-steps | screens[6].widget.options, explain | the queue hands out every node k hops away before any at k + 1; sorting only breaks ties; parents do not make a route short | correct | CLRS Lemma 20.3 |
| l6-fewest-steps | screens[7].widget.answer, wrong, explain | fund is 3 hops away on several routes; 2 intermediaries; 3 = hops; 4 = nodes | correct | script: distance 3, four shortest routes |
| l6-fewest-steps | screens[8].widget | fewest_conversions passes 8 tests on the twelve `PAIRS`; starter fails | correct | script `widgets`; `len(PAIRS)` is 12 |
| l6-fewest-steps | screens[8].feedback.byKey.test-1 | NGN, ZAR, USD, SGD, THB is 4; one-way storage gives -1 | correct | mutant: one-way adjacency returns -1 on test 1 |
| l6-fewest-steps | screens[8].feedback.byKey.test-3 | HUF to GBP runs against the written order of the pairs; 3 conversions | correct | pairs ('GBP','EUR'), ('EUR','PLN'), ('PLN','HUF') |
| l6-fewest-steps | screens[8].feedback.byKey.test-7 | MXN is in no pair; `adj[u]` raises; use `adj.get(u, [])` | correct | mutant: passes 1 to 6, KeyError on 7 |
| l6-fewest-steps | screens[8].explain | with equal spreads fewer hops always cost less; with different spreads the edges need weights | correct | equal positive weights make cost proportional to hop count |
| l6-fewest-steps | summary | BFS reaches each node first along a fewest-hops route; parent walk; [s] and None cases; O(V + E); dist(v) = dist(parent(v)) + 1; DFS can return a far longer route | correct | as above |
| l6-fewest-steps | quiz[0] | BFS on an adjacency list is O(V + E); O(V^2) is the matrix cost; V pops plus 2E neighbour checks | correct | CLRS 20.2 |
| l6-fewest-steps | quiz[1] | `shortest_path(..., 'B', 'B')` prints ['B'] | correct | run |
| l6-fewest-steps | quiz[2] | BFS returns the direct one-hop route at 4.0 bp, not the 2.7 bp route through USD | correct | 1.2 + 1.5 = 2.7; BFS minimises edges |
| l6-fewest-steps | quiz[3] | maze needs 6 moves: right, right, down, down, right, down; 7 counts cells | correct | script BFS on the grid |
| l7-dijkstra | screens[0].widget.answer, wrong, hints | cheapest A to F is A, C, B, D, F at 7; A, C, D, F is 9; A, C, E, F is 9; A, B, D, F is 8; every other route costs 8 or more | correct | script enumerates all A to F routes and their costs |
| l7-dijkstra | screens[1].widget.answer, hints[2], feedback.B | C at 1 is final; any other route to C must start through B at 4; B's 4 can still improve to 3 | correct | A has two arrows only; non-negative weights |
| l7-dijkstra | screens[1].explain | the smallest tentative cost is safe when no arrow is negative | correct | CLRS Theorem 22.6 (Dijkstra correctness); labels B 3, D 6, E 3 after C checked by script |
| l7-dijkstra | screens[2].prose | Dijkstra with a heap of (cost, node); an entry larger than its node's current cost is stale | correct | lazy-deletion Dijkstra (Sedgewick and Wayne 4.4) |
| l7-dijkstra | screens[2].widget.states s0..s5, explain | heap contents after each pop: (3,B),(3,E),(4,B),(6,D); (3,E),(4,B),(4,D),(6,D); (4,B),(4,D),(6,D),(9,F); skip (4,B); (6,D),(7,F),(9,F); pop order A 0, C 1, B 3, E 3, D 4, F 7; (6,D) and (9,F) stale | correct | script instruments the lesson's solution and compares sorted heap contents at each state |
| l7-dijkstra | screens[2].hints[0] | `heapq` pops the smallest; ties on cost go to the earlier letter | correct | tuple comparison |
| l7-dijkstra | screens[3].prose, hints[2], explain | at most E + 1 pushes; each heap step O(log V) since E <= V^2; total O((V + E) log V) | correct | one push per successful relaxation, each edge relaxed once from its popped tail; log E <= 2 log V |
| l7-dijkstra | screens[3].widget.options | list version O(V^2); BFS O(V + E); Bellman-Ford O(VE) with V - 1 rounds; Dijkstra relaxes each edge once | correct | CLRS 22.1, 22.3 |
| l7-dijkstra | screens[3].feedback.byKey.scan, explain | a million nodes gives 10^12 steps for the list version; the list version pays off only on dense graphs | correct | (1e6)^2; with E near V^2 the heap costs V^2 log V |
| l7-dijkstra | screens[4].widget | dijkstra passes 9 tests; starter fails; `hub_scans(300)` returns (300, 1) | correct | script `widgets` |
| l7-dijkstra | screens[4].feedback.byKey.test-1 | B at 4 from marking on first push, or from a stale pop overwriting; missing G when unreachable nodes are left out | correct | three mutants, each first fails test 1 with the stated symptom |
| l7-dijkstra | screens[4].feedback.byKey.test-2 | from G only F is reached | correct | test 2 |
| l7-dijkstra | screens[4].feedback.byKey.test-9, explain | without the stale check the hub's edges are read more than once; the answers stay right; 299 stale entries | correct | mutant passes 1 to 8 and returns (300, 300) on 9; script counts 300 hub pushes, 299 stale |
| l7-dijkstra | screens[5].widget.answer, explain | record-on-pop with no check gives B 4, D 6, F 9; the fix `if u in dist: continue` | correct | script runs the screen's code, then with the one-line fix (B 3, D 4, F 7) |
| l7-dijkstra | screens[6].widget.answer, feedback | with C to B at -2 the true cost to B is 1; textbook Dijkstra keeps 2 | correct | 3 - 2; script runs a settle-on-pop version: 2 |
| l7-dijkstra | screens[6].explain | our heap code re-pushes B at 1 and is right here, but nodes can be popped many times and the speed bound is lost; a negative loop has no cheapest cost | correct | script: lesson's solution returns B 1; Johnson (1973) shows exponential behaviour of label-correcting Dijkstra with negative edges |
| l7-dijkstra | screens[7].prose, options, explain | O((V + E) log V) when every w >= 0; equal weights of 5 give 5 times the BFS distance; BFS is then faster | correct | script compares on the lesson's test graph |
| l7-dijkstra | screens[8].widget.answer, wrong, hints, explain | cheapest GBP to JPY is 0.5 + 0.6 + 1.5 = 2.6 bp, £260; direct £400; via USD £270; via EUR £290; settle order EUR 0.5, USD 1.1, CHF 1.2, JPY 2.6; exact compounding £259.98 | correct | script Dijkstra and 1e6 x (1 - (1 - 5e-5)(1 - 6e-5)(1 - 1.5e-4)) = 259.98 |
| l7-dijkstra | screens[9].widget | slowest_arrival passes 8 tests; starter fails | correct | script `widgets` |
| l7-dijkstra | screens[9].feedback.byKey.test-1, explain | from LD4: TY3 at 29.5 + 3.9 + 70.0 = 103.4 through Chicago, 115.2 through Singapore | correct | script |
| l7-dijkstra | screens[9].feedback.byKey.test-4, test-8 | TY3 has no outgoing links; HK1 is reached by no link; both give -1 | correct | tests 4, 8; mutant that ignores unreachable centres passes 1 to 3 and fails 4 |
| l7-dijkstra | summary | smallest tentative cost is final with non-negative weights; push on improvement and skip stale; O((V + E) log V); a negative edge breaks finality; relaxation formula | correct | CLRS 22.3 |
| l7-dijkstra | quiz[0] | mark-on-first-push gives B 4 | correct | script runs the variant |
| l7-dijkstra | quiz[1] | `dijkstra({'X': []}, 'X')` prints {'X': 0} | correct | run |
| l7-dijkstra | quiz[2] | 100,000 nodes and 400,000 edges: about 8.5 x 10^6 against 10^10; about a thousand times | correct | 5e5 x log2(1e5) = 8.3e6; ratio about 1,200 |
| l7-dijkstra | quiz[3] | 6 nodes, 9 edges, positive weights: at most E + 1 = 10 heap entries | correct | one push per edge at most, directed or undirected, plus the start; script random search never exceeds E + 1 |
| l8-groups | screens[0].widget.answer, explain | groups {SHEL, BP}, {HSBA, BARC, LLOY}, {AZN, GSK}; a group is everything joined by a chain of links; each group named by a representative | correct | connected components; CLRS 19.1 (disjoint-set representative) |
| l8-groups | screens[1].widget.answer, wrong.one-card, explain | linking LLOY and BP merges both whole groups: SHEL, BP, HSBA, BARC, LLOY; union re-points one representative | correct | script union-find on the named links |
| l8-groups | screens[2].widget.answer, wrong, explain | `find(7)` is 2 by 7, 6, 4, 2 in three steps; 6 is the parent; `find(1)` is 0; same group iff same root | correct | script runs the screen's code on the screen's `parent` |
| l8-groups | screens[3].widget.answer, wrong.four, explain | `find(7)` with compression changes parents of 7 and 6 only; 4 already points at 2; next `find(7)` takes one step | correct | script diff of `parent` before and after |
| l8-groups | screens[4].prose, options | root 2 heads 6 items and root 0 heads 2; `parent[0] = 2` deepens two items; `parent[2] = 0` deepens six; `parent[0] = 5` leaves 0's group two steps lower than needed | correct | script depths under each choice: 0 at depth 1 against depth 3 |
| l8-groups | screens[4].explain | union by size: an item gets deeper only when its group at least doubles, so depth is at most log2 n | correct | CLRS exercise 19.3 / Sedgewick and Wayne Proposition H (weighted quick-union) |
| l8-groups | screens[5].widget, how | DSU passes 9 tests; `chain_check(5000)` returns (True, 1, True); starter fails | correct | script `widgets` |
| l8-groups | screens[5].widget.how | a recursive `find` can go 5,000 deep on this chain, past the recursion limit | correct | mutant (naive `parent[find(a)] = find(b)`, recursive find): RecursionError at limit 3000 and at 1000 |
| l8-groups | screens[5].feedback.byKey.test-5 | union(2, 2) must return False and leave 3 groups | correct | mutant that merges and decrements before comparing roots passes 1 to 4 and returns (False, 2) on 5 |
| l8-groups | screens[5].feedback.byKey.test-7 | re-pointing node 0, not its root, leaves 1 apart from 2 | correct | mutant `parent[a] = rb`: passes 1 to 6, fails 7 |
| l8-groups | screens[5].feedback.byKey.test-9 | a find that walks the whole chain gives RecursionError or a False timing flag | correct | iterative no-compression mutant with naive union: 2.5e7 steps, over 0.5 s in CPython 3.12 here (Pyodide is slower); recursive mutant: RecursionError |
| l8-groups | screens[5].explain, screens[7].prose, summary.formula | m operations cost O(m alpha(n)); alpha(n) <= 4 for any practical n; grows slower than any logarithm | correct | Tarjan (1975); CLRS 19.4, Theorem 19.14 |
| l8-groups | screens[6].widget, explain | node-level union loses the link: after union(0, 1), union(0, 2), find(1) != find(2); fix joins the roots | correct | script runs the screen's code |
| l8-groups | screens[7].widget.answer, wrong, explain | 8 nodes with edges 0-1, 2-3, 1-3, 5-6: 4 components {0,1,2,3}, {5,6}, {4}, {7}; four merges | correct | script DSU count |
| l8-groups | screens[8].prose | a minimum spanning tree joins every node with the cheapest set of edges and no loops; an edge whose ends share a root would close a loop | correct | CLRS 21.1, connected graph understood |
| l8-groups | screens[8].widget.answer, same | Kruskal: sort and singletons (either order), take edge and find, keep if roots differ, stop at n - 1 kept | correct | CLRS 21.2 MST-KRUSKAL; script checks the lesson's steps against brute force on 200 random connected graphs |
| l8-groups | screens[8].explain | sorting O(E log E) dominates; n - 1 kept edges leave one group; a skipped edge joins two already-connected nodes | correct | CLRS 21.2 |
| l8-groups | screens[9].widget | clusters passes 7 tests; starter fails | correct | script `widgets` |
| l8-groups | screens[9].feedback.byKey.test-1 | comparing `rho` not `abs(rho)` drops GILT | correct | mutant: first failing test 1, GILT alone |
| l8-groups | screens[9].feedback.byKey.test-3 | threshold 0.76 with HSBA-BARC exactly 0.76: strict rule drops the link | correct | `>=` mutant passes 1 to 2, fails 3 |
| l8-groups | screens[9].feedback.byKey.test-7 | D sits two steps below the root; gathering by `parent` splits it off | correct | mutant grouping by `d.parent[i]` passes 1 to 6, fails 7; script prints D's depth 2 |
| l8-groups | screens[9].feedback.correct, explain | five clusters at 0.7; HSBA and LLOY at 0.69 share a cluster through BARC; AZN and GSK at 0.64 stay apart | correct | script |
| l8-groups | screens[9].prose | a strong negative correlation is the same risk factor with the sign flipped | correct | modelling choice stated as such; \|rho\| measures linear co-movement either way |
| l8-groups | summary | one parent per item; union joins roots, smaller under larger; near-constant operations; node-level parent set drops links | correct | as above |
| l8-groups | quiz[0] | trades 1-2, 3-4, 2-5 among six: 3 groups; 2 forgets counterparty 6 | correct | DSU count |
| l8-groups | quiz[1] | `d.union(3, 3), d.count()` prints False 4 | correct | run on the lesson's DSU |
| l8-groups | quiz[2] | five records: 2 clients; 3 misses the r1, r2, r3 chain | correct | script DSU on shared fields |
| l8-groups | quiz[3] | chain with neither trick: n finds of find(0) cost O(n^2); 2.5 x 10^7 at n = 5,000; O(n log n) needs union by size | correct | script counts steps: n(n - 1) = 24,995,000 at n = 5,000 |
| l9-arbitrage-cycle | screens[0].widget.answer, hints[2], explain | GBP, USD, EUR loop multiplies to 1.004824; every other loop is below 1; £1,000,000 returns £1,004,824 | correct | script enumerates all simple directed cycles: 1.004824, 0.998108, 0.997323 |
| l9-arbitrage-cycle | screens[0].feedback.byKey.chf | USD, EUR, CHF loop gives 1.142 x 0.92 x 0.95 = 0.998108 | correct | script |
| l9-arbitrage-cycle | screens[1].widget.answer, explain, feedback.now | break-even r = 1/1.1684 = 0.855871 (0.8559); at 0.86 the loop makes 0.48%; a loop worth exactly 1 is not an arbitrage | correct | script |
| l9-arbitrage-cycle | screens[2].prose, answer, hints, wrong | w = -ln(rate); weights -0.239017, 0.083382, 0.150823 sum to -0.004812; 3.05 adds rates; 1.004824 is the product; +0.004812 is the sign slip | correct | script, 6 dp |
| l9-arbitrage-cycle | screens[2].explain | product above 1 becomes sum below 0; arbitrage detection is negative-cycle detection, which Dijkstra cannot do | correct | CLRS problem 22-3 (arbitrage); Dijkstra needs non-negative weights |
| l9-arbitrage-cycle | screens[3].widget.rows, hints | with edge order C to D, B to C, A to B: pass 1 gives B 2; pass 2 gives C 5; pass 3 gives D 6 | correct | script runs the passes in that order |
| l9-arbitrage-cycle | screens[3].explain | in the worst order each pass extends correct costs by one edge; a shortest route has at most V - 1 edges, so V - 1 passes suffice | correct | CLRS Lemma 22.2 (path-relaxation), no negative cycle |
| l9-arbitrage-cycle | screens[4].prose | after n - 1 passes, an edge that still improves means a negative cycle is reachable | correct | CLRS Theorem 22.4 |
| l9-arbitrage-cycle | screens[4].widget | bellman_ford passes 9 tests; starter fails | correct | script `widgets` |
| l9-arbitrage-cycle | screens[4].feedback.byKey.test-1 | fewer than n - 1 passes leaves node 3 at inf on the backwards chain | correct | mutant with n - 2 passes: [0, 2, 5, inf] on test 1 |
| l9-arbitrage-cycle | screens[4].feedback.byKey.test-3 | cycle 1, 2, 1 has total -2; no extra pass misses it | correct | mutant without the detection pass: passes 1 to 2, fails 3 |
| l9-arbitrage-cycle | screens[4].feedback.byKey.test-6 | cycle of total exactly 0 is not negative | correct | test 6 weights 1 and -1 |
| l9-arbitrage-cycle | screens[4].explain | O(V E); slower than Dijkstra; an unreachable negative cycle stays at inf since inf + w is never smaller than inf | correct | float semantics, test 4 |
| l9-arbitrage-cycle | screens[5].widget, hints, feedback | with w = -rate every loop is negative; GBP loop sums to -3.05; CHF loop to -3.012 | correct | script |
| l9-arbitrage-cycle | screens[5].explain | only -ln(rate) turns the product test into a sum test; rate 1 gets weight 0 | correct | ln is the unique continuous map from products to sums up to scale |
| l9-arbitrage-cycle | screens[6].widget, hints, feedback | `-math.log(1.25) - math.log(0.8)` is -5.55e-17, so `w < 0` prints True | correct | script: -5.551115123125783e-17 in CPython 3.12 (same libm results expected in Pyodide; both are IEEE doubles) |
| l9-arbitrage-cycle | screens[6].explain | real code uses a tolerance such as 1e-9 | correct | standard numerical practice |
| l9-arbitrage-cycle | screens[7].widget.answer, explain | r1 r2 r3 > 1 iff sum of -ln r_i < 0; each step reversible; 0.004812 | correct | ln strictly increasing; log of a product |
| l9-arbitrage-cycle | screens[8].prose | implied cross 1.0850 / 1.2700 = 0.854331; loop returns 1.0000359 per pound | correct | script: 0.8543307, 1.00003595 |
| l9-arbitrage-cycle | screens[8].widget.answer, wrong, hints, feedback | after three 1 bp costs: 0.999736, loss about £264 (-264.03); gross £35.95; 0.36 bp gross against 3 bp costs | correct | script: -264.03 from unrounded rates |
| l9-arbitrage-cycle | screens[8].explain | "triangular arbitrage rarely survives costs" | unverified | empirical claim with no source in the content; consistent with Akram, Rime and Sarno (2008, J. Int. Econ.) but not cited |
| l9-arbitrage-cycle | screens[8].explain | costs make each weight -ln(0.9999 x rate) and the cycle stops being negative | correct | script: cycle weight +0.000264 |
| l9-arbitrage-cycle | screens[9].prose, explain | a start node joined to every currency at weight 0 makes every cycle reachable | correct | CLRS 22.4 / Johnson's reweighting source; adds no cycle since nothing enters the start |
| l9-arbitrage-cycle | screens[9].widget | has_arbitrage passes 10 tests; starter fails; test 4 is worth exactly 1 | correct | script `widgets`; 1.25 x 0.8 == 1.0 |
| l9-arbitrage-cycle | screens[9].feedback.byKey.test-2 | with EUR to GBP at 0.855 no loop pays; `-rate` weights report True | correct | mutant: passes test 1, fails 2; best loop 0.998982 |
| l9-arbitrage-cycle | screens[9].feedback.byKey.test-4 | without eps the exactly-1 round trip reads as negative | correct | mutant eps = 0: passes 1 to 3, returns True on 4 |
| l9-arbitrage-cycle | screens[9].feedback.byKey.test-9 | JPY, KRW loop is unreachable from GBP; needs the start node | correct | mutant starting at index 0: passes 1 to 8, fails 9; 9.1 x 0.1102 = 1.00282 |
| l9-arbitrage-cycle | screens[9].explain | hook's loop is worth £4,824 on £1,000,000 before costs | correct | 1e6 x 0.004824 |
| l9-arbitrage-cycle | summary | arbitrage iff product above 1 iff sum of -ln below 0; V - 1 passes plus one; tolerance; -rate weights make every loop look profitable | correct | as above |
| l9-arbitrage-cycle | quiz[0] | 8 currencies, 40 quotes: 8 passes x 40 = 320; 280 omits detection; 360 is 9 passes | correct | arithmetic |
| l9-arbitrage-cycle | quiz[1] | 1.27 x 0.787 = 0.99949; spread 5.1 bp; weight sum +0.000510 | correct | script |
| l9-arbitrage-cycle | quiz[2] | implied EUR/GBP = 1.05 / 1.25 = 0.8400; 1.1905 is euros per pound | correct | script |
| l9-arbitrage-cycle | quiz[3] | a rate above 1 gives a negative weight; Dijkstra needs weights >= 0; works with real weights and directed graphs | correct | CLRS 22.3 |
| l10-every-subset | screens[0].widget.answer, wrong | three take-or-skip choices give 2 x 2 x 2 = 8 holdings; 7 drops the empty one; 6 is 3!; 3 is one per stock | correct | product rule; script counts `subsets("ABC")` |
| l10-every-subset | screens[1].widget.answer, explain | four of eight holdings contain B; each stock splits the holdings in two | correct | script |
| l10-every-subset | screens[2].prose, answer, feedback | the walk records A B C, A B, A C, A, B C, B, C, none; fifth is B C; A fourth; B sixth; empty last | correct | script runs the screen's `walk` |
| l10-every-subset | screens[2].explain | a depth-first walk over choices that undoes each choice on the way back is backtracking | correct | Skiena, Algorithm Design Manual 9.1; CLRS has no chapter, Knuth TAOCP 4B 7.2.2 |
| l10-every-subset | screens[3].widget.answer, wrong, explain | 10 stocks: 2^10 = 1,024 holdings; 100, 20 and 10! slips; the walk visits 2^(n+1) - 1 nodes | correct | script counts calls for n = 3 and n = 10: 15 and 2,047 |
| l10-every-subset | screens[4].widget.answer, explain | orderings of X, Y, Z: 3 x 2 x 1 = 6; two send X last; n! in general; a `used` flag skips chosen trades | correct | script |
| l10-every-subset | screens[5].widget.options, explain | storing `path` itself prints eight empty lists: one list object, ending empty | correct | script runs the console's code |
| l10-every-subset | screens[6].prose, options | choose, recurse, un-choose; 2^n leaves for subsets, n! for orderings; 5! = 120; 32, 25, 15 slips | correct | arithmetic |
| l10-every-subset | screens[7].widget.answer, feedback.s4, explain | walk body order: base case, take, recurse, pop, recurse; the pop restores `path` for the skip branch | correct | matches the solution that passes its tests |
| l10-every-subset | screens[8].widget.options, explain | ['VOD', 'BP', 'VOD'] gives 8 lists and 4 different holdings; counting VOD VOD and VOD BP VOD as new gives 6; clean with `sorted(set(xs))` | correct | script: 8 lists, 4 distinct sets, 6 distinct multisets |
| l10-every-subset | screens[9].widget, how | subsets and permutations pass 11 tests; starter fails | correct | script `widgets` |
| l10-every-subset | screens[9].feedback.byKey.test-1 | skip-before-take gives [] first; storing `path` gives every list [] | correct | two mutants, both first fail test 1 with those outputs |
| l10-every-subset | screens[9].feedback.byKey.test-2, test-5, test-7 | `subsets([])` is [[]]; 8 separate list objects; `permutations([])` is [[]] | correct | tests 2, 5, 7; mutant returning [] on empty input fails test 2 first |
| l10-every-subset | screens[9].explain | empty input reaches the base case at once; copy keeps answers separate; pop restores `path` | correct | run |
| l10-every-subset | screens[10].widget.answer, wrong, explain | at most 3 of 6: 1 + 6 + 15 + 20 = 42; 41, 20, 64, 120 slips; with 3 held only skip remains | correct | script counts with the capped walk: 42 |
| l10-every-subset | screens[11].widget.answer, wrong, explain | 2^30 ms = 1,073,742 s = 12.4 days = 298 hours; 40 stocks about 35 years | correct | script: 12.43 days, 298.3 hours, 34.8 years |
| l10-every-subset | summary | backtracking definition; 2^n and n!; copy at the leaf; empty input has one subset and one ordering | correct | as above |
| l10-every-subset | quiz[0] | without the pop `subsets(['a', 'b'])` returns [a,b], [a,b], [a,b,b], [a,b,b]; no IndexError | correct | script runs the quiz's code |
| l10-every-subset | quiz[1] | `subsets([])` returns 1 list; 2^0 = 1 | correct | run |
| l10-every-subset | quiz[2] | 4 legs: 4! = 24 orders; 16 and 10 slips | correct | arithmetic |
| l10-every-subset | quiz[3] | `walk` is called 15 times for three items: 1 + 2 + 4 + 8; 8 leaves; 7 branching calls | correct | script call counter |
| l11-dead-ends | screens[0].widget.answer, wrong.no-diag, feedback | with a queen on r1c2 the safe cells in rows 2 to 4 are r2c4, r3c1, r3c3, r4c1, r4c3, r4c4; r2c1, r2c3, r3c4 are on its diagonals | correct | script attack test on a 4 by 4 board |
| l11-dead-ends | screens[1].widget.answer, explain | with queens on r1c2 and r2c4: r3c1, r4c1, r4c3 are safe; a queen on r3c1 attacks r4c1, leaving r4c3; solution r1c2, r2c4, r3c1, r4c3 | correct | script |
| l11-dead-ends | screens[2].widget.answer, wrong, explain | 4 queens has 2 placements, mirror images; corners fail in row 3 or row 4; pruning definition | correct | script brute force over 4! and 4^4 boards; Skiena 9.1 |
| l11-dead-ends | screens[3].widget.rows, explain, summary.formula | boards by depth without pruning 1, 4, 16, 64, 256 = 341; with pruning 1, 4, 6, 4, 2 = 17; row 2 safe cells 2, 1, 1, 2 | correct | script counts nodes at each depth |
| l11-dead-ends | screens[3].explain | for 8 queens 19,173,961 boards against 2,057 | correct | script: (8^9 - 1)/7 = 19,173,961; pruned node count 2,057 |
| l11-dead-ends | screens[3].explain | pruning does not change the answers, only the work | correct | true of a safe prune, which is what this screen uses; the unsafe case is screens[6] |
| l11-dead-ends | screens[4].widget.answer, explain | subsets of 3, 5, 6 summing to 8: take-6 is refused at totals 8, 3, 5 (would reach 14, 9, 11); the one answer is 3 + 5; positive totals never fall | correct | script |
| l11-dead-ends | screens[5].widget.answer, wrong, hints | `combos([2, 3, 5], 8)` returns 3 lists: [2,2,2,2], [2,3,3], [3,5]; 6 counts orders; 1 forbids reuse; line 12 passes `i`; line 10 breaks | correct | script runs the console's code; ordered count 6; line numbers checked against `lines` |
| l11-dead-ends | screens[5].explain | passing `start` keeps lists non-decreasing so each combination appears once; the sorted `break` prunes all larger candidates | correct | canonical-form argument; candidates sorted ascending |
| l11-dead-ends | screens[6].widget.options, hints, feedback | `subset_sum([6, -4, 3], 2)` returns False though 6 + (-4) = 2; the take +6 branch is cut at total 6; no basket without +6 sums to 2 | correct | script runs the screen's code and brute-forces all 8 baskets |
| l11-dead-ends | screens[6].explain, screens[7].prose | a prune is safe only if a branch failing it can never recover (fails in every extension) | correct | definition of an admissible prune; Skiena 9.1 |
| l11-dead-ends | screens[7].widget.options, explain | with sorted positive numbers, `total + xs[i] > target` rules out every later number too | correct | xs[j] >= xs[i] for j > i and all positive; script compares pruned search with brute force on 500 random inputs |
| l11-dead-ends | screens[8].widget | n_queens and subset_sum pass 13 tests (1, 2, 10, 4, 0, 0, 92); starter fails | correct | script `widgets`; OEIS A000170 |
| l11-dead-ends | screens[8].widget.how | last test: 25 even numbers, odd target; without pruning about 67 million calls | correct | len(range(2, 52, 2)) = 25; 2^26 - 1 = 67,108,863 calls for a full take-or-skip tree |
| l11-dead-ends | screens[8].widget.how | 67 million calls "takes several seconds" | correct | timed here: 2^23 calls take 0.47 s in CPython 3.12, so about 3.8 s for 2^26; Pyodide is several times slower, past the page's 5 s limit |
| l11-dead-ends | screens[8].feedback.byKey.test-2 | without the undo `n_queens(4)` gives fewer than 2 | correct | mutant: passes test 1, returns 0 on test 2 |
| l11-dead-ends | screens[8].feedback.byKey.test-5 | 2 and 3 queens have no placement | correct | A000170 |
| l11-dead-ends | screens[8].feedback.byKey.test-9 | every subset making 13 uses 8, last after sorting; end-of-list check before `total == target` fails | correct | script: subsets summing to 13 are {5, 8} and {2, 3, 8}; mutant passes 1 to 8, fails 9 |
| l11-dead-ends | screens[8].feedback.byKey.test-10, test-13 | empty subset sums to 0; unpruned search times out on test 13 | correct | test 10; call count above |
| l11-dead-ends | screens[8].explain, hints[1] | row - col is constant on a diagonal, row + col on an anti-diagonal; three sets give O(1) safety tests | correct | set membership average O(1); geometry |
| l11-dead-ends | screens[9].widget.options, explain | spend, clashes and counts are monotone so their cuts are safe; net exposure is not: +5 - 3 + 2 - 4 = 0 passes +2 on the way | correct | running nets 5, 2, 4, 0 |
| l11-dead-ends | screens[9].explain | for netting, prune on a bound such as the most the remaining shorts could take off | correct | branch-and-bound lower bound |
| l11-dead-ends | summary | pruning changes work not answers; safe when failing now means failing every extension; restore state after every branch; sorted cut | correct | as above |
| l11-dead-ends | quiz[0].widget.answer, explain, feedback | 3 queens: 0 placements; a middle queen attacks all of row 2; a corner queen leaves one row 2 cell whose queen kills row 3 | correct | script |
| l11-dead-ends | quiz[0].widget.accept | "every queen in row 1 leaves row 3 with nothing safe" | imprecise | with the queen on r1c2 it is row 2 that has nothing safe; r3c1 and r3c3 are not attacked by it. Finding 6 |
| l11-dead-ends | quiz[1] | unpruned 8 queens checks 8^8 = 16,777,216 full boards; 8! = 40,320; 19,173,961 counts partial boards; pruned search visits 2,057 and finds 92 | correct | script |
| l11-dead-ends | quiz[2] | with the undo deleted `n_queens(4)` returns 0; stale marks only block | correct | script runs the mutated function |
| l11-dead-ends | quiz[3] | `combos([2, 3, 6, 7], 7)` returns 2 lists: [2,2,3] and [7]; 4 counts orders | correct | script |
| l12-remembering | screens[0].widget.answer, wrong.ones, explain | the call tree of `fib(5)` computes f(2) three times and f(3) twice; five f(1) calls | correct | script builds the call tree and counts labels |
| l12-remembering | screens[1].canvas rows, answer, wrong | naive calls 1, 1, 3, 5, 9, 15, 25; fib(6) = 1 + 15 + 9; 24, 30, 21 slips | correct | script call counter |
| l12-remembering | screens[1].explain | calls grow about 1.6 times per step; `fib(30)` makes 2,692,537 calls to compute 832,040; 31 different values | correct | C(n) = 2F(n+1) - 1 = 2 x 1,346,269 - 1; script counts by recurrence and by running fib(25) scaled check; golden ratio 1.618 |
| l12-remembering | screens[2].widget.answer, feedback, explain | with a dict the stored hits are f(1) under f(3), f(2) under f(4), f(3) under f(5); 15 calls become 9; memoisation is top-down dynamic programming | correct | script traces a memoised fib with call paths; CLRS 14.1 (top-down with memoization) |
| l12-remembering | screens[3].widget.rows, explain | cache 0, 1, 1, 2, 3, 5, 8; naive computes n = 0..6 respectively 5, 8, 5, 3, 2, 1, 1 times (total 25); memo 7 values | correct | script per-argument call counts for naive fib(6) |
| l12-remembering | screens[4].widget.answer, wrong, explain | memoised `fib(30)` computes 31 values; with 28 cache hits, 59 calls; O(n) | correct | script instruments the memoised fib: 31 computed, 28 hits |
| l12-remembering | screens[5].prose, answer, wrong, explain | right-or-down paths on a 3 by 4 grid of points: paths(i, j) = paths(i-1, j) + paths(i, j-1); corner 10 = C(5, 2); neighbour 6 | correct | script table and math.comb |
| l12-remembering | screens[6].widget.options, explain | the cached `price(100, 1)` prints 95.24 twice after `rate` changes; fresh value would be 90.91; cache only pure functions | correct | script runs the console's code |
| l12-remembering | screens[7].prose | memoised recursion shape; function must be pure; work = states x work per state | correct | CLRS 14.3 |
| l12-remembering | screens[7].widget.options, explain | `lru_cache` raises TypeError on a list argument; tuples, floats, strings are hashable; lists, dicts, sets are not | correct | script calls each |
| l12-remembering | screens[8].prose, answer, explain | a default dict is created once at `def`; after `fib(5)`, `fib(6)` prints one `computing` line; the shown transcript for fib(5) | correct | script runs the console's code and captures prints |
| l12-remembering | screens[9].widget, how | fib_memo and grid_paths pass 14 tests; starter fails; grid_paths(18, 18) = 2,333,606,220 needs billions of naive calls; comparison with C(r + c - 2, r - 1) | correct | script `widgets`; naive calls 2 C(34, 17) - 1 = 4.67e9 |
| l12-remembering | screens[9].feedback.byKey.test-1 | (0, 1): the base case counts | correct | mutant not counting base cases returns (0, 0) on test 1 |
| l12-remembering | screens[9].feedback.byKey.test-2 | a count of 2 means the counter outlived test 1 | correct | mutant with a module-level counter: passes 1, returns (1, 2) on 2 (tests share one module, see code.js) |
| l12-remembering | screens[9].feedback.byKey.test-3 | 11 counts lookups too; 5 means the cache outlived earlier tests | correct | two mutants: lookup-counting gives (8, 11) and first fails 3; module-level cache gives (8, 5) and first fails 3 |
| l12-remembering | screens[9].feedback.byKey.test-4, test-6, test-12 | 31 values; second `fib_memo(10)` still counts 11; unmemoised `paths` times out on test 12 | correct | tests 4, 6; naive call count above |
| l12-remembering | screens[9].explain | n + 1 states for fib; at most r x c points for the grid; count equals C(r + c - 2, r - 1) | correct | script compares for all r, c up to 12 |
| l12-remembering | screens[10].prose, answer, wrong, explain | recombining 30-step tree: step k has k + 1 nodes, 496 in all, against 2^30 paths; value depends only on (step, ups) | correct | 31 x 32 / 2; Hull ch. 13 (binomial trees; Cox, Ross and Rubinstein 1979), for payoffs that depend on the node only |
| l12-remembering | screens[10].explain | memoising on (step, ups) is the backward induction of a binomial pricer | correct | same recurrence V(k, j) = disc x (p V(k+1, j+1) + (1-p) V(k+1, j)); top-down order instead of bottom-up |
| l12-remembering | summary | naive recomputation; work = distinct states x work per state; pure function, hashable arguments; stale global or `self.rate` | correct | as above |
| l12-remembering | quiz[0] | 200 passes over the same 25 bonds: 25 prices computed; 5,000 counts every call | correct | 25 distinct keys |
| l12-remembering | quiz[1] | `lru_cache` on a method keys on `self` by identity: prints 0.907 after the rate changes; fresh 0.89; cache keeps instances alive | correct | script runs the class; Python docs functools FAQ "How do I cache method calls?" |
| l12-remembering | quiz[2] | naive `fib(7)` makes 41 calls; memoised computes 8 values | correct | 1 + 25 + 15 |
| l12-remembering | quiz[3] | `fib_memo(0)` returns (0, 1) | correct | run |
| l13-climbing-stairs | screens[0].widget.answer, wrong, explain | 4 stairs in steps of 1 or 2: 5 ways (1111, 112, 121, 211, 22); 3 end with a 1 and 2 end with a 2; 3 mixes ignoring order | correct | script enumerates compositions |
| l13-climbing-stairs | screens[1].widget.answer, explain | stair 5 is reached from 4 or 3; the cases are disjoint by last step, so ways(5) = ways(4) + ways(3) | correct | partition by last step |
| l13-climbing-stairs | screens[2].prose, rows, explain | ways(0) = ways(1) = 1; table 1, 1, 2, 3, 5, 8, 13; bottom-up dynamic programming; O(n) | correct | script; CLRS 14.1 (bottom-up method) |
| l13-climbing-stairs | screens[3].widget.options, explain | `stairs(6)` ends with prev = 8, cur = 13 after 5 passes; O(1) space, O(n) time; tuple assignment uses old values | correct | script runs the screen's code and inspects locals |
| l13-climbing-stairs | screens[4].widget.answer, explain | with ways(0) = 0 the code returns 3 for n = 4; table 0, 1, 1, 2, 3; ways(2) comes out 1 | correct | script runs the screen's code |
| l13-climbing-stairs | screens[5].prose, rows, feedback | coins 1, 3, 4: best = 0, 1, 2, 1, 1, 2, 2; best(a) = 1 + min best(a - c); 6 = 3 + 3; largest-first gives 4 + 1 + 1 | correct | script table and a greedy run |
| l13-climbing-stairs | screens[5].explain | greedy can fail; the recurrence cannot, because it tries every last coin for every amount | correct | optimal substructure of coin change (CLRS problem 15-1 notes greedy fails for general coin sets); script compares the table with brute force on 300 random coin sets |
| l13-climbing-stairs | screens[6].widget.answer, explain canvas | filling from the top down returns -1 for amount 6; final table 0, 1, inf, 1, 1, inf, inf | correct | script runs the screen's code |
| l13-climbing-stairs | screens[6].explain | each best[a] reads smaller amounts, so smaller amounts must be filled first | correct | dependency order of the recurrence |
| l13-climbing-stairs | screens[7].prose, options, explain | five-step recipe; with steps 1, 2, 3 the recurrence has three terms; 1, 1, 2, 4, 7, 13 | correct | script enumerates compositions with parts 1 to 3 |
| l13-climbing-stairs | screens[8].widget.answer, explain | recipe for coins: state, recurrence, base case with infinities, order upwards, answer or -1 | correct | matches the solution |
| l13-climbing-stairs | screens[9].widget, how | stairs and min_coins pass 15 tests; starter fails; stairs(90) = 4,660,046,610,375,530,309; stairs(5000) mod 1e9+7 = 419,609,281 | correct | script `widgets`; independent matrix-free recomputation |
| l13-climbing-stairs | screens[9].feedback.byKey.test-1 | one way to climb zero stairs | correct | mutant with ways(0) = 0 fails test 1 |
| l13-climbing-stairs | screens[9].feedback.byKey.test-5 | plain recursion on stairs(90) runs out of time | correct | naive calls 2 F(91) - 1, about 9.3e18; mutant passes 1 to 4 |
| l13-climbing-stairs | screens[9].feedback.byKey.test-6 | a memoised recursion goes 5,000 deep on stairs(5000), past the recursion limit | correct | memoised mutant passes 1 to 5 and raises RecursionError on 6 at limit 3000 (and 1000) |
| l13-climbing-stairs | screens[9].feedback.byKey.test-7, test-8, test-9 | greedy gives 3 on [1, 3, 4], 6; amount 0 gives 0; coins of 2 cannot make 3 | correct | greedy mutant first fails test 7 with 3; tests 8, 9 |
| l13-climbing-stairs | screens[9].explain | min_coins does amount x len(coins) steps | correct | two nested loops |
| l13-climbing-stairs | screens[10].prose, answer, wrong, explain | equal up and down factors recombine; 6 days back at £100 needs 3 ups and 3 downs: C(6, 3) = 20 = 10 + 10; 64 paths in all; Pascal's triangle | correct | math.comb; Hull ch. 13 |
| l13-climbing-stairs | screens[11].widget.answer, wrong, explain | lots 100, 500, 600, 900 for 1,100: 2 trades (500 + 600); greedy 900 + 100 + 100 is 3; level 4 covers knapsack and sequence comparison | correct | script min_coins([1, 5, 6, 9], 11) = 2; course.json level 4 |
| l13-climbing-stairs | summary | split by last choice; bottom-up order; best(a) recurrence with best(0) = 0; greedy can fail; ways(0) = 0 and wrong order fail silently | correct | as above |
| l13-climbing-stairs | quiz[0] | `min_coins([2, 5], 0)` returns 0 | correct | run |
| l13-climbing-stairs | quiz[1] | `min_coins([2, 5], 11)` returns 4 (5 + 2 + 2 + 2); greedy takes 5 + 5 and is stuck | correct | run |
| l13-climbing-stairs | quiz[2] | steps 1, 2, 3: ways(5) = 13; 8 with steps 1 or 2 | correct | script |
| l13-climbing-stairs | quiz[3] | ways(0) = 1 because the empty climb is one way; with 0, ways(2) would be 1 | correct | as screens[4] |
| review-1 | items[0] | 10 nodes, 15 edges, no self-loops: 30 list entries; 15 once; 25 = V + E; 100 = V^2 | correct | 2E |
| review-1 | items[1] | BFS from P alphabetical: P, Q, S, R, T, U; U is three edges away | correct | script runs l2's `bfs` |
| review-1 | items[2] | recursive DFS: P, Q, R, U, T, S; sorted-push stack version gives P, S, T, U, R, Q | correct | script runs l3's `dfs` and the naive stack code |
| review-1 | items[3] | 4 islands; joining corners gives 3 (r3c1 touches r2c2 diagonally); 10 land cells | correct | script |
| review-1 | items[4] | load, clean, features, calendar, model is invalid: features before calendar; the other two orders are valid | correct | arrow check |
| review-1 | items[5] | `deque.pop()` takes the newest, so the search is depth-first in style; all reachable nodes still visited once; rounds no longer mean distances | correct | stack discipline; `seen` unchanged |
| review-1 | items[6] | Kahn emits 3 of 7 (a, b, c); d has in-degree 3; d, e, f form a cycle and g waits behind f | correct | script |
| review-1 | items[7].widget | has_path passes 7 tests incl. a 5,001-node chain; starter fails | correct | script `widgets` |
| review-1 | items[7].feedback.byKey.test-2, test-4, test-7 | C cannot reach A against the arrows; a path of length 0 counts; recursion runs out of frames on the chain | correct | tests 2, 4; recursive mutant passes 1 to 6 and raises RecursionError on 7 |
| review-2 | items[0] | parent walk from T gives T, C, A, S; reversed S, A, C, T, three hops | correct | trace |
| review-2 | items[1] | Dijkstra from S: S 0, A 2, B 5, C 6, T 8 by S, A, B, C, T; S, B, T is 14; S, A, C, T is 11 | correct | script runs l7's `dijkstra` |
| review-2 | items[2] | `find(4)` with compression turns [0, 0, 1, 2, 3] into [0, 0, 0, 0, 0] | correct | script |
| review-2 | items[3] | 191.20 x 0.006135 x 0.8530 = 1.000579; intermediate 1.173012; sum slip 192.059135; weight -0.000579; 5.8 bp | correct | script |
| review-2 | items[4] | lazy Dijkstra pops and skips 3 stale entries: (6, B), (9, C), (13, T) | correct | script instruments the run |
| review-2 | items[5] | Kruskal total 1 + 2 + 3 + 5 = 11; A-B at 4 closes a loop (10 if kept instead of B-D); 15 keeps five edges | correct | script, and brute force over spanning trees |
| review-2 | items[6] | chain of 6 nodes in the worst edge order: node 5 correct after 5 passes = V - 1; one pass fixes only node 1 | correct | script |
| review-2 | items[7] | incremental connectivity fits union-find; BFS per query costs O(V + E); no costs so not Dijkstra or Bellman-Ford; O(alpha(n)) per operation | correct | CLRS 19 (amortised bound) |
| review-3 | items[0] | `subsets` of four items returns 16 lists; 15 omits the empty one; 24 is 4! | correct | script |
| review-3 | items[1] | record-at-every-node walk gives [], [1], [1, 2], [1, 2, 3] first, 8 subsets in all | correct | script runs the item's code |
| review-3 | items[2] | queen on r1c1: r2c3 and r2c4 safe; under r1c2 only one cell (r2c4) is safe | correct | script |
| review-3 | items[3] | pruned walk on [4, -2, 1] with target 3 returns False though 4 - 2 + 1 = 3; without the 4 no basket reaches 3 | correct | script runs the item's code and brute force |
| review-3 | items[4] | naive `fib(8)` makes 67 calls; memoised computes 9 values | correct | script |
| review-3 | items[5] | a cached function that reads global `TODAY` can return a stale answer; the other three depend only on their arguments | correct | cache key = arguments (functools docs) |
| review-3 | items[6] | steps 1, 2, 3: ways(6) = 13 + 7 + 4 = 24; 20 adds two terms | correct | script |
| review-3 | items[7] | coins 1, 5, 6, 9 for 11: 2 coins (5 + 6); greedy 9 + 1 + 1 is 3; best(10), best(6), best(5), best(2) = 2, 1, 1, 2 | correct | script |
| review-3 | items[8] | memoisation helps `fib(40)` and grid paths; not listing orderings; rarely n-queens | correct | overlapping subproblems (CLRS 14.3); a partial board placed row by row is reached by one path only, so "almost never reached twice" errs on the cautious side |
| homework-1 | items[0] | shortest_hops passes 7 tests; GBP to SEK is 3 by GBP, EUR, CHF, SEK; GBP to GBP is 0; NOK gives -1; one-way edge gives -1 | correct | script `widgets` |
| homework-1 | items[1] | days_to_spread passes 8 tests; multi-source BFS; 2,000-chain with both ends gives 999; O(V + E) | correct | script `widgets`; single-source mutant first fails test 2 with 5 |
| homework-1 | items[2] | batch_rounds passes 8 tests; VaR run needs 5 rounds; rounds equal the longest chain of dependencies; y, z cycle beside w gives None | correct | script `widgets`; layers of Kahn = longest path in jobs |
| homework-1 | items[3] | Kahn steps in order: count, seed, take, lower, release, repeat, check | correct | matches l5's solution |
| homework-1 | items[4] | 20,000^2 x 8 bytes = 3.2 GB; 0.4 counts cells; 0.00016 is one row; list of 400,000 entries about 3.2 MB | correct | script |
| homework-1 | items[5] | ring with a centre cell: 2 islands; 16 border cells; enclosure is not connection | correct | script |
| homework-1 | items[6] | owners of Z, transitively, are found by reversing every arrow and searching from Z; forward search finds what Z owns; undirected search adds unexposed firms | correct | reachability in the transpose graph (CLRS 20.5) |
| homework-1 | items[7].model, rubric | topological order exists exactly when there is no cycle; Kahn in O(V + E); leftovers imply a cycle; three-state DFS finds it; pre-order and plain `seen` fail; same-pass jobs are independent; batches equal the longest chain | correct | CLRS 20.4; argued as in l5 rows |
| homework-1 | items[8].widget, how | split_desks passes 12 tests; `desk_web()` has three linked sets (index classes mod 3); `desk_chain()` is a 3,000 chain | correct | script `widgets`; construction read from the postlude |
| homework-1 | items[8].feedback.byKey.test-2..test-10 | each named mistake fails first at its test: one-way storage (2), no clash check (3), first set only (4), desks from conflicts (5), given order (6), any placed neighbour a clash (7), one conflict at a time (8), recursion on the chain (10); test 9 has an odd loop in the second set | correct | eight mutants in the script, each with the stated symptom |
| homework-1 | items[8].explain | a neighbour already in the same group closes an odd loop, so no split exists; O(D + C) plus the sort | correct | a graph is two-colourable iff it has no odd cycle (Konig; Diestel 1.6.1) |
| homework-2 | items[0] | maze_steps passes 8 tests; test 1 is 6 (7 counts cells); test 4 has a wall at the start; BFS is O(rows x cols) | correct | script `widgets` |
| homework-2 | items[1].widget, explain | cheapest_within passes 9 tests; after round i `cost` holds the cheapest routes of at most i conversions; relaxing from a copy; O(k E) | correct | script `widgets`; CLRS 22.1 path-relaxation by rounds |
| homework-2 | items[1].feedback.byKey.test-1 | k rounds gives -1; in-place relaxation gives 2.6 | correct | two mutants, both first fail test 1 with those values |
| homework-2 | items[1].feedback.byKey.test-2 | 2.7 through USD; 2.9 when USD's two-step 1.1 replaces its one-step 1.2 | correct | hop-limited Dijkstra mutant passes test 1 and returns 2.9 on test 2 |
| homework-2 | items[1].feedback.byKey.test-7 | no route from JPY back to GBP | correct | QUOTES has no edge out of JPY except to THB |
| homework-2 | items[2] | count_clients passes 7 tests; chains of shared identifiers merge; test 4 joins two pairs through a third record | correct | script `widgets` |
| homework-2 | items[3] | proof order: pop at d; any other route leaves the final set at x; x's cost is at least d; the rest is non-negative; so d is cheapest; a negative edge breaks line 4 | correct | CLRS Theorem 22.6, in sketch form |
| homework-2 | items[4] | LD4 to TY3 is 103.4 ms through Chicago; 115.2 through FR2 and SG1; 118.0 through SG1 direct; settle order FR2 4.2, NY4 29.5, CH1 33.4, SG1 81.2, TY3 103.4 | correct | script |
| homework-2 | items[5] | 1.2650 x 0.9230 x 0.8580 = 1.00179651, an 18 bp loop; after 0.9998^3 about £1,195.55; one cost only £1,596.15; gross £1,796.51 | correct | script |
| homework-2 | items[6] | negative weights without a negative cycle: Bellman-Ford in O(V E); Dijkstra needs weights >= 0 | correct | CLRS 22.1, 22.3 |
| homework-2 | items[7].model, rubric | bid and 1/ask edges; weights -ln(rate) less the log of a fee factor; V - 1 passes plus one; start node; 31 x 830 = 25,730 relaxations; cycle recovery by walking `parent` V steps; tolerance; loss of about £264 on the worked loop | correct | CLRS 22.1 and problem 22-3; arithmetic in script |
| homework-2 | items[7].model (e) | "if many arbitrageurs watch liquid quotes, mispricings stay small and short-lived" | correct | stated as a conditional, not as an empirical fact |
| homework-2 | items[8].widget, how | count_cheapest passes 11 tests; `venue_ladder()` has 61 layers of 5 venues; 358,584,264,000 routes | correct | script `widgets` |
| homework-2 | items[8].feedback.byKey.test-1..test-8 | named mistakes fail first at their tests: return when dst first reached (1, count 1), a tie adds 1 or pushes again (2), cheaper cost adds the count (3), stale entry expanded (5, (7, 2)), dst looked up (8) | correct | six mutants in the script; test 4 and test 7 lines state the tests' facts correctly |
| homework-2 | items[8].explain | with fees at least 1 a cheapest route into a venue passes only venues popped earlier, so the count is final at the pop; O((V + E) log V) | correct | strictly positive weights give a strict order of settlement; zero weights would break the count |
| homework-3 | items[0] | combination_sum passes 8 tests; loop from 0 repeats [2, 3, 2]; unsorted candidates fail test 3; target 0 gives [[]] | correct | script `widgets`; two mutants |
| homework-3 | items[0].explain | the `break` is safe because candidates are sorted and positive | correct | as l11 screens[5] |
| homework-3 | items[1] | word_break passes 9 tests; state is the start index; len(s) + 1 states; test 8 has billions of splits | correct | script `widgets`; compositions of 40 into parts 1 to 4 exceed 10^9 (script) |
| homework-3 | items[2] | ordering walk: base case, loop over unused, mark and append, recurse, pop and unmark | correct | matches l10's solution |
| homework-3 | items[3] | 4 legs with A before D: 12 orders, half of 24 by the A and D swap; 6 fixes A first | correct | script enumeration |
| homework-3 | items[4] | at most 21 x 101 = 2,121 (i, total) states against 2^20 subsets; 2,000 and 2,100 slips | correct | arithmetic |
| homework-3 | items[5] | 10 days back at the start: C(10, 5) = 252; 1,024 paths in all | correct | math.comb |
| homework-3 | items[6] | memoised grid_paths is O(r x c); naive is exponential; the answer's size is not the work | correct | states x O(1) |
| homework-3 | items[7].model, rubric | 2^25 = 33,554,432 subsets, over nine hours at 1 ms; 245,506 of size at most 6; count prune safe, net prune unsafe (+5, +2, -3, -4); bound \|net\| > 10k; 26 x 7 x 121 = 22,022 states; pure function with hashable arguments | correct | script arithmetic; monotonicity argument as l11 |
| homework-3 | items[8].widget | trade_with_fee passes 11 tests; starter fails | correct | script `widgets` |
| homework-3 | items[8].feedback.byKey.test-2..test-7 | two trips make 8 where one makes 4; 10 to 16 then 13 to 18 makes 7 where each rise alone makes 6; first day and last day belong in the table; a rise below the fee gives 0; no prices gives 0 | correct | four mutants in the script (one trip, each rise, no first day, no last day), each first failing at its test |
| homework-3 | items[8].explain | flat = max(flat, long + p - fee), long = max(long, flat - p), from flat 0 and long -inf; answer is flat; O(n) | correct | two-state DP; optimal substructure by the last action |

# Claim ledger: graphs-dp L1 to L3 (round 1 blind audit, 13 Nov 2026)

Scope: `app/content/courses/graphs-dp/` l1 to l13, review-1 to review-3, homework-1 to homework-3 (Stage 1, full depth). Level 4 files are out of scope. Every row was judged by hand from a derivation, a named source or a run. "script" means a named check in `docs/reports/graphs-dp-L1-3-concepts.py` (CPython 3.13). "Pyodide" means a value read from the local Pyodide 0.27.7 build under Node (Python 3.12.7): `sys.getrecursionlimit()` is 1000, `-math.log(1.25) - math.log(0.8)` is `-5.551115123125783e-17`, a recursive DFS on a 5,000 chain raises `RecursionError` and runs after `sys.setrecursionlimit(10**6)`, and an unpruned subset sum over 25 numbers takes 6.8 s. All 38 Python code widgets were run under CPython: every solution passes every hidden test and example, and every starter fails (script, `check_all_code`). There are no C++ widgets in scope.

Paths are shortened: `s3` is `screens[3]`, `q1` is `quiz[1]`, `i4` is `items[4]`; `w` is `widget`, `fb` is `feedback`, `ex` is `explain.text`. "F7" points to finding 7 and "U3" to unverified row 3 in `docs/reviews/audit-graphs-dp-1-3.md`.

Sources named: CLRS = Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* (3rd ed.), chapters 15 (dynamic programming), 21 (disjoint sets), 22 (graph algorithms), 23 (minimum spanning trees), 24 (single-source shortest paths); Sedgewick and Wayne, *Algorithms* (4th ed.), chapter 4; Kleinberg and Tardos, *Algorithm Design*, chapters 3, 4 and 6; Python docs (`collections.deque`, `heapq`, `functools.lru_cache`, `sys.setrecursionlimit`, data model on hashing, FAQ on mutable defaults and on multidimensional lists); Hull, *Options, Futures and Other Derivatives* (9th ed.), chapters 5 and 13; Fenn, Howison, McDonald, Williams and Johnson (2009), "The mirage of triangular arbitrage in the spot foreign exchange market", *IJTAF* 12(8).

## l1-nodes-and-edges

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, hints, fb | C's neighbours are A, D, E; B is two edges away; F joins E only | correct | edge list A-B, A-C, B-D, C-D, C-E, E-F |
| s0.ex | neighbours defined; knowing every node's neighbours fixes the graph | correct | CLRS 22.1 |
| s1 keys, accept, fb | lists B: A, D; C: A, D, E; D: B, C; E: C, F; F: E | correct | script: l1 s1 |
| s1.ex | adjacency list as a dict of lists; an undirected edge appears twice | correct | CLRS 22.1 |
| s2 keys, hints, fb | row C is 1 0 0 1 1 0; diagonal 0 with no self-loop | correct | script |
| s2.ex | adjacency matrix; `M[2][3]` is an O(1) edge check; row C equals column C | correct | CLRS 22.1 |
| s3 key, wrong, fb | 12 ones; 6 = each edge once; 36 = all cells; rows hold 2, 2, 3, 2, 2, 1 | correct | script: l1 s3 |
| s3.ex | an undirected matrix is symmetric with 2E ones; V² cells whatever E | imprecise | 2E only with no self-loops: this lesson's own `adj_matrix(2, [(1, 1)])` has one 1 (script). F9 |
| s4.prose | directed edge and weight defined; arrow GBP to USD is selling pounds for dollars at that rate | correct | CLRS 22.1; quote read as units of the second per unit of the first, as l9 s0 states |
| s4 key, whys | one (neighbour, rate) pair per arrow at its start; JPY needs a key; `adj["JPY"]` raises `KeyError` without one | correct | Python dict semantics |
| s4.ex | a directed matrix need not be symmetric; node with no out-edges keeps an empty list | correct | CLRS 22.1 |
| s5.prose, tests | edge list; self-loop stored once; every node keyed | correct | script: code widget passes |
| s5 fb test-1, 2, 3 | both ends; build from `nodes`; self-loop once | correct | tests[0], [1], [2] |
| s5.ex | two appends per edge, so O(V + E) build and 2E entries; sorting only fixes the output | correct | the count excludes the sort, which the sentence sets aside; 2E for no self-loops |
| s6 key, whys, hints, fb | one-way loop prints `[]` for D; no `KeyError`; C-D lands in C's list | correct | script: l1 s6 |
| s6.ex | a search from D finds nothing, silently; fix is `adj[v].append(u)` | correct | run |
| s7.prose | list O(V + E) space, neighbours in O(deg u); matrix O(V²) space, edge check O(1) | correct | CLRS 22.1 |
| s7.prose | most real graphs are sparse | correct | Sedgewick and Wayne 4.1: "the huge graphs that arise in practice are sparse" |
| s7 key, whys | 10^10 cells; 2 x 10^6 entries; 10^6 edges; 10^5 = one per firm | correct | script |
| s7.ex | 80 GB of 8-byte pointers; list of 2 million entries is tens of megabytes; matrix for small or dense graphs or edge-check loads | correct | script (8 bytes per list cell); 2e6 x 8 = 16 MB plus 10^5 list headers |
| s8.prose, ex | `[[0] * n] * n` is n references to one row; comprehension builds separate rows; O(V²) build | correct | script; Python FAQ "How do I create a multidimensional list?" |
| s8 fb test-1, test-5 | shared rows; n = 0 gives `[]` | correct | tests[0], [4] |
| s9.prose | central counterparty: receives from all others, posts to none; at most one | correct | two such firms would each have to post to the other |
| s9 fb test-3, test-5 | firm 2 also posts to 0; one firm qualifies with `into == 0 == n - 1` | correct | tests[2], [4] |
| s9 fb test-4 | "firm 2 posts to nobody, but nobody needs to post to it" | wrong | in tests[3] nobody posts to firm 2, and every other firm must (script). F13 |
| s9 fb.correct, ex | in-degree and out-degree; one pass, O(V + E) | correct | CLRS 22.1 |
| summary | list, matrix, storage rules, space formula, trap | correct | as rows above |
| q0 key, wrong, fb, ex | 14 entries; 7 = once; 49 = E² | correct | 2 x 7, no self-loops stated |
| q1 key, whys | matrix read is fastest; list scan is up to deg(i); edge list is O(E) and misses (j, i) | correct | CLRS 22.1 |
| q1.ex | 250,000 cells; a dict of sets also gives O(1) checks with less space | correct | 500²; expected O(1) hashing |
| q2 key, wrong, fb, ex | 10^6 cells; 7,000 = V + 2E; 6,000 = 2E; 99.4% hold 0 | correct | script |
| q3 key, whys, ex | directed storage gives `[]` for score; no `KeyError` | correct | run by hand |

## l2-level-by-level

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, fb | day 2 is C, E, F; G and H hear on day 3; every route A to G has three edges | correct | BFS by hand; the two simple routes are A-B-E-G and A-D-C-G |
| s0.ex | ring-by-ring spread is breadth-first search | correct | CLRS 22.2 |
| s1 key, hints, fb | order A, B, D, E, C, F, G, H | correct | script: l2 s1 |
| s1.ex | order within a day is discovery order; first in, first out is a queue | correct | CLRS 22.2 |
| s2 key, fb | after B: queue D, E; processed A, B | correct | hand trace |
| s2.ex | FIFO makes BFS finish one day before the next | correct | CLRS lemma 22.3 |
| s3 steps | queue contents A; B, D; D, E; E, C, F; C, F, G, H; G not queued twice | correct | hand trace |
| s4.prose | `popleft()` is one step | correct | Python docs `collections.deque`: O(1) at both ends |
| s4 solution, tests, how | BFS with mark on queueing | correct | script: code widget |
| s4 fb test-3, test-4 | square catches marking on pop; start with no neighbours | correct | tests[2], [3] |
| s4 fb test-7 | a timeout on the 3,000 path means `list.pop(0)` | misleading | on a path the queue never holds more than one node, so `pop(0)` passes in 0.7 ms (script). F10 |
| s4.ex | each node queued once, each edge read from each end: O(V + E); sorting only fixes order | correct | CLRS 22.2 |
| s5 key, whys, hints, fb | late marking gives A, B, D, E, C, F, G, H, G; it stops; nothing is lost | correct | script: l2 s5 |
| s5.ex | a node can be queued once per neighbour, O(E) copies in all | correct | at most one copy per incoming edge |
| s6 key, fb, ex | C and G unreachable; BFS returns the start's connected component; restart from unseen nodes | correct | CLRS 22.2 and B.4 |
| s7.prose | pattern; each node joins once, each edge read twice; first found in round d means d edges, the fewest | correct | CLRS theorem 22.5 (unweighted) |
| s7 key, whys, fb | `pop(0)` shifts the rest, so up to O(V²); same order | correct | Python TimeComplexity wiki; script: l2 s7 |
| s7.ex | up to 10^10 moves against 10^5 pops | correct | 10^5 pops of up to 10^5 moves |
| s8 solution, tests, fb | BFS distances, stop expanding at k | correct | script: code widget; l2 s8 |
| s8.ex | `dist` is exact when first seen; Hazel is three hops out | correct | CLRS 22.5; script |
| s8.prose | firms within k links "face losses first" | unverified | framing device, no source; harmless to the method. U1 |
| summary | BFS order, mark on joining, component, cost | correct | rows above |
| q0 key, whys, ex | queue gives level order; stack gives depth-first; set has no order | correct | CLRS 22.2, 22.3 |
| q1 key, wrong, fb | star: 6 in the queue after the centre | correct | hand trace |
| q2 key, fb, ex | round 3 means exactly 3 edges, none shorter | correct | CLRS 22.5 |
| q2 why cheapest | "the cheapest chain needs the rates as weights: Dijkstra" | imprecise | rates multiply; l9 shows rate weights need `-ln` and Bellman-Ford. Additive costs, as in l7 s8, are what Dijkstra takes. F17 |
| q2 why count | BFS gives fewest edges, not the number of routes | correct | definition |
| q3 key, whys, ex | prints `['X', 'Y']`; Z never looked up | correct | run by hand |

## l3-going-deep

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, hints, fb | DFS order A, B, E, G, C, D, F, H | correct | script: l3 s0 |
| s0.ex | depth-first search defined; BFS order quoted | correct | CLRS 22.3 |
| s1 key, fb, ex | first dead end is F; back through D, C, G, E; then H; backtracking | correct | hand trace |
| s2 solution, tests, fb | recursive DFS; triangle needs `seen` | correct | script: code widget |
| s2.ex | `seen` stops cycles; each node once, each edge twice; O(V + E) | correct | CLRS 22.3 |
| s3 key, whys, hints, fb | no `seen` on a triangle raises `RecursionError`; about 1,000 frames | correct | script; Pyodide limit 1000 |
| s3.ex | a loop-based search would hang; recursion fails fast; on a tree the bug hides | correct | an explicit stack with no `seen` grows without end; a rooted tree with child lists has no cycle |
| s4 key, whys, hints | naive stack order A, D, F, C, G, E, H, B | correct | script: l3 s4 |
| s4.ex | valid depth-first order, mirrored; reverse-sorted pushes match recursion | correct | script: stack matches recursion from every start |
| s5 solution, tests, how, fb | mark on pop, skip seen, reverse-sorted pushes; 5,000 path | correct | script: code widget |
| s5.ex | a node may sit on the stack twice; marking on pop matches recursion; a list stack has no depth limit | correct | script |
| s6 key, hints, fb | post-order F, D, C, G, H, E, B, A | correct | script: l3 s6 |
| s6.ex | pre-order and post-order defined; a node comes after all it led to | correct | CLRS 22.3 (parenthesis theorem) |
| s7.prose, key, hints | about 1,000 frames; 5,000 chain raises `RecursionError` | correct | Pyodide: limit 1000, chain raises |
| s7 why limit | raising the limit can overflow the C stack and crash the interpreter | correct | Python docs `sys.setrecursionlimit`: "a too-high limit can lead to a crash"; on this chain in Pyodide 3.12 the raised limit does run, so "can" is the right word |
| s7.ex | recursion depth equals the longest path the search follows | correct | one frame per node on the current path |
| s8 solution, tests, fb | count components by restarting | correct | script: code widget |
| s8.ex | all searches together are O(V + E); BFS works as well | correct | CLRS 22.3 |
| s9.prose | in a directed graph a visited node is not enough; it must be on the current path | correct | CLRS 22.3: a back edge goes to a grey vertex (lemma 22.11) |
| s9 solution, tests, fb | three states; diamond is not a cycle; self-read is a cycle; start from every rule | correct | script: l3 s9 |
| s9.ex | spot is done, not active, when vega reaches it | correct | hand trace |
| summary | recursion or stack; `seen`; pre and post; O(V + E); trap | correct | rows above |
| q0 key, whys, ex | BFS and DFS reach the same component | correct | CLRS 22.2, 22.3 |
| q1 key, wrong, fb, ex | 4 components | correct | by hand |
| q2 key, fb | 0 non-parent visited nodes on a tree | correct | a tree has no cycle |
| q2.ex | "that is also how DFS tests whether an undirected graph is a tree" | imprecise | no such edge shows only that the reached part is acyclic; a tree also needs every node reached (script: two-piece forest). F12 |
| q3 key, why pre, why bfs | post-order U, S, T, R; pre-order R, S, U, T; BFS R, S, T, U | correct | script: l3 q-post |
| q3 why rev | R, T, S, U "reverses the pre-order" | wrong | it is the reversed post-order; the reversed pre-order is T, U, S, R (script). F3 |
| q3.ex | every node comes after its descendants | correct | CLRS 22.3 |

## l4-islands

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb | island of the marked cell is r1c5, r2c4, r2c5; r3c3 touches at a corner | correct | grid by hand |
| s0.ex | land cell as node with up to four neighbours; island is a connected component | correct | definition |
| s1 key, wrong, fb | 6 islands; 4 if corners join; 14 land cells | correct | script: l4 s1 |
| s1.ex | scan and start a search at each unseen land cell; marking stops recounts | correct | l3 component counter |
| s2 solution, tests, fb | four neighbours in order, bounds checked | correct | script: code widget |
| s2.ex | `grid[-1]` is the last row, so a missing check wraps silently | correct | Python sequence indexing |
| s3 key, wrong, fb | 4,000,000 looks at most; 10^6 cells; 10^12 pairs | correct | 10^6 x 4 |
| s3.ex | O(rc); no adjacency list is built | correct | each cell scanned once and popped once |
| s4 solution, tests, how | `seen` set, stack, grid unchanged | correct | script: code widget |
| s4 fb test-2, 5, 10 | guard empty grid; corners do not join; sinking fails the unchanged test | correct | tests[1], [4], [9] |
| s4 fb test-11 | a timeout on 20 by 20 means cells were not marked when pushed | misleading | marking on pop with a skip pushes at most 4 per cell and cannot time out (script); only no marking at all loops, and that fails test 1 first. F10 |
| s4.ex | mark on push; `seen` costs O(rc) memory; stack avoids depth limits | correct | rows above |
| s5 key, whys, fb | prints `2 [[0, 0, 0], [0, 0, 0]]`; Python passes the same list | correct | Python docs: arguments are passed by assignment |
| s5.ex | `[row[:] for row in grid]` copies; `grid.copy()` shares rows | correct | Python docs `copy`: shallow copy |
| s6 key, whys, hints | 300 by 300 of land: about 90,000 open calls; the dive snakes | correct | script: l4 s6 (depth k² for order up, down, left, right) |
| s6.ex | BFS on a grid is also O(rc) | correct | CLRS 22.2 |
| s7 pattern, key, whys, ex | four side neighbours; eight if corners count; wrapping is the missing bounds check | correct | rows above |
| s8.prose | loss region defined; "separate regions mean separate ways to lose" | unverified | interpretive gloss, no source; kept out of the graded content. U2 |
| s8 solution, tests, fb | 2 regions at £50k, 1 at £10k, 0 at £100k, 2 at £30k; strict threshold | correct | script: l4 s8 |
| s8.ex | at £10k the +4 vol column loses everywhere and joins the regions | correct | script |
| s8.ex | "the count tells risk whether one hedge can cover the losses" | unverified | no source; one strangle hedges both corners of a short straddle (Hull ch. 12), so the count does not settle it. U3 |
| s8 caption | grid is a short straddle book's P&L | correct | loses on large moves either way and on vol up (Hull ch. 12, 19) |
| summary | grid as graph; O(rc); `seen`; trap | correct | rows above |
| q0 key, whys, ex | thresholded correlation matrix is an adjacency matrix; neighbouring cells mean nothing | correct | definition of adjacency matrix |
| q1 key, wrong, ex | 5 islands; 1 with corners | correct | script |
| q2 key, whys, ex | `seen` set on push; sinking damages the map; no mark loops | correct | rows above |
| q3 key, wrong, ex | 3 runs of 1s | correct | by hand |

## l5-tasks-in-order

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, same, fb | valid order; prices and calendar swap, signals and risk swap | correct | script |
| s0.ex | four orders work; topological order; DAG | correct | script: 4 of 5,040 permutations; CLRS 22.4 |
| s1 keys, fb | in-degrees 0, 0, 2, 1, 1, 2, 1 | correct | by hand |
| s1.ex | in-degree 0 is free; finishing a task lowers its successors' counts | correct | Kahn (1962); Kleinberg and Tardos 3.6 |
| s2 key, fb, ex | signals and risk are free; Kahn's algorithm described | correct | Kleinberg and Tardos 3.6 |
| s3.prose | `adj` maps a task to the tasks that need it; heap for name ties; leftovers mean a cycle | correct | rows below |
| s3 solution, tests, fb | Kahn with a heap; `None` on a cycle; `[]` on empty | correct | script: code widget, l5 s3 |
| s3.ex | O(V + E), or O(V log V + E) with the heap; a task on a cycle is never emitted | correct | each task pushed and popped once at O(log V) |
| s4 key, hints | pre-order from sorted names starts with backtest | correct | script |
| s4 title, whys, fb | the fault is that the loop "starts in the wrong place" | misleading | pre-order from the free task calendar gives calendar, returns, risk, backtest before signals (script). The fault is recording on arrival. F6 |
| s4.ex | full result backtest, report, calendar, returns, risk, signals, prices | correct | script: l5 s4 |
| s4.ex | "either start from in-degree 0 (Kahn), or use post-order" | misleading | reads as "start the pre-order from in-degree 0"; that is still invalid. F6 |
| s5 key, hints, fb | post-order report, backtest, risk, signals, returns, calendar, prices | correct | script: l5 s5 |
| s5.ex | post-order lists each task after its dependents; reversed is valid from any starting point | imprecise | true on a DAG; on a cyclic graph it returns an order with no warning (script). F11 |
| s6 key, wrong, fb, ex | Kahn emits 4 of 7; risk, backtest and report are stuck | correct | script: l5 s6 |
| s7 pattern | O(V + E); reversed post-order "gives an order too, at the same cost" | imprecise | same DAG condition; unlike Kahn it has no built-in cycle check. F11 |
| s7 key, whys, ex | leftovers lie on a cycle or wait on one; proof by walking arrows backwards | correct | Kleinberg and Tardos (3.19) |
| s7 fb.correct | "leftover nodes always mean a cycle" | correct | same proof |
| s8 solution, tests, fb | reverse the arrows, include raw inputs, Kahn | correct | script: code widget |
| s8.ex | order market_data, positions, scenarios, pnl_vectors, var_report, limits_check | correct | script |
| summary.ideas[0], [1] | order exists only with no cycle; Kahn; fewer than V means a cycle | correct | CLRS 22.4; Kleinberg and Tardos (3.18), (3.20) |
| summary.ideas[2] | reversed post-order valid; pre-order is not | correct | CLRS theorem 22.12, read with ideas[0] |
| summary.trap | "starting from a task that still has arrows in, or emitting on arrival" | misleading | names the starting place as a cause. F6 |
| q0 key, wrong, ex | 24 orders with no arrows | correct | 4! |
| q1 key, whys, ex | only a, c, b | correct | script |
| q2 key, whys, ex | post-order lists dependents first, so reverse it | correct | CLRS 22.4 |
| q3 key, wrong, ex | in-degree of q is 3 | correct | by hand |

## review-1

| path | claim | verdict | basis |
|---|---|---|---|
| i0 key, wrong, fb | 30 entries; 15 once; 25 = V + E; 100 = V² | correct | 2 x 15 |
| i1 key, fb, ex | BFS P, Q, S, R, T, U; U is three edges away | correct | by hand |
| i2 key, whys, ex | DFS P, Q, R, U, T, S; naive stack gives P, S, T, U, R, Q | correct | by hand, both traced |
| i3 key, wrong, fb, ex | 4 islands; 3 with corners; 10 cells | correct | script |
| i4 key, whys, ex | load, clean, features, calendar, model is invalid | correct | calendar to features |
| i5 key, whys, ex | `pop()` makes the deque a stack; all reachable nodes still visited; levels lost | correct | Python docs `deque.pop` |
| i6 key, wrong, fb, ex | Kahn emits a, b, c; d, e, f cycle; g stuck | correct | script |
| i7 solution, tests, fb, ex | stack reachability; path of length 0 counts | correct | script: code widget |

## homework-1

| path | claim | verdict | basis |
|---|---|---|---|
| i0 solution, tests, fb | BFS hops; 0 for same; −1 unreachable; GBP to SEK is 3 | correct | script: code widget |
| i0.prose | fewest trades wanted "since each trade pays a spread" | correct | stated as the task's premise |
| i0.ex | stopping when `t` is popped saves work | correct | dist is final when popped |
| i1 solution, tests | multi-source BFS; −1 if a firm is never reached | correct | script: code widget |
| i1 fb test-2, test-5 | seed both ends; isolated firm gives −1 | correct | tests[1], [4] |
| i1 fb test-8 | "one BFS per defaulted firm is too slow" on the 2,000 chain | misleading | two sources on 2,000 nodes is 4,000 pops; it cannot time out. F10 |
| i1.ex | seeding all sources gives each firm its fewest days from the nearest default; O(V + E) | correct | BFS from a virtual source (CLRS 22.2) |
| i2 solution, tests, fb | Kahn by layers; 5 rounds for the VaR run | correct | script: hw1 rounds |
| i2.ex | layers equal the longest chain of dependencies, 5 here | correct | longest path counted in jobs: market_data to limits_check |
| i3 key, fb, ex | order of Kahn's steps | correct | l5 s7 pattern |
| i4 key, wrong, fb | 3.2 GB; 0.4 = cells; 0.00016 = one row | correct | script |
| i4.ex | "bonds share an issuer with few others, so a list of a few megabytes" | unverified | no source; large issuers have hundreds of bonds, and k bonds of one issuer give k² entries. U4 |
| i5 key, wrong, fb, ex | ring and centre: 2 islands; 16 border cells | correct | script |
| i6 key, whys, ex | reverse the arrows and search from Z; O(V + E) | correct | transpose graph, CLRS 22.1 |
| i7 model (a), (b) | graph model; Kahn; O(V + E) | correct | rows in l5 |
| i7 model (c) | leftovers imply a cycle | correct | Kleinberg and Tardos (3.19) |
| i7 model (d) | three-state DFS; reaching an active job closes a cycle; path gives the cycle | correct | CLRS lemma 22.11 |
| i7 model (e) | "starting from a job with in-degree above 0 does the same" | misleading | carries the l5 s4 framing. F6 |
| i7 model (e) | a plain `seen` set flags diamonds as cycles | correct | l3 s9 |
| i7 model (f), (g) | same-pass jobs are independent; batches equal the longest chain; check on each change | correct | i2 |
| i7 rubric | seven lines, 10 points | correct | matches the model |
| i8 solution, tests, how | two-colouring by BFS from the first desk of each linked set | correct | script: code widget (12 tests) |
| i8 fb test-2 to test-10 | each names the fault its test catches | correct | traced tests[1] to [9]; test-2 and test-8 checked by hand |
| i8.ex | a neighbour in the same group closes an odd loop; O(D + C) plus the sort | correct | a graph is bipartite iff it has no odd cycle (Kleinberg and Tardos 3.4) |

## l6-fewest-steps

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb | A, E, F, H is 3 hops; the others take 4 | correct | script |
| s0.ex | no route in two hops; short routes first | correct | script: rings |
| s1 key, hints | ring 2 is C, F, G | correct | script: l6 s1 |
| s1 fb with-d | "D is two hops from C, which makes it three hops from A" | wrong | D is one hop from C; C is two hops from A (script). F2 |
| s1.ex | ring number is the fewest hops because each ring finishes first; D and H are ring 3 | correct | CLRS 22.5 |
| s2.prose, keys, hints | queue order A, B, E, C, F, G, D, H; F from E; D from C at 3; H from F at 3 | correct | hand trace |
| s2.ex | C left the queue before G, so C is D's parent; parents sit one ring nearer | correct | CLRS lemma 22.6 (breadth-first tree) |
| s3 key, whys, fb, ex | walk gives H, F, E, A; reversed is the route; 4 nodes, 3 hops | correct | by hand |
| s4 solution, tests, fb | `parent` dict BFS; `[s]`; `None` | correct | script: code widget |
| s4.ex | `parent` marks and remembers; O(V + E) | correct | CLRS 22.2 |
| s5 key, whys, hints, fb | DFS returns A, B, C, D, G, E, F, H: seven hops | correct | script: l6 s5 |
| s5.ex | DFS finds a route, not the shortest; only the ring order guarantees fewest hops | correct | CLRS 22.2 against 22.3 |
| s6 key, whys, ex | queue hands out every node k hops away before k + 1 | correct | CLRS lemma 22.3 |
| s7 key, wrong, fb, ex | fund is 3 hops; 2 intermediaries; several routes tie | correct | by hand: four 3-hop routes |
| s7.prose | each hop "adds a day of delay and an operational risk check" | unverified | framing device, no source. U5 |
| s8 solution, tests, fb | 4 conversions NGN to THB; unknown currency is −1 | correct | script: l6 s8 |
| s8.ex | "a route with fewer hops usually costs less" | unverified | no source; illiquid crosses are routinely cheaper through the dollar, and q2 of this lesson is a counter-example. U6 |
| summary | BFS rings; parent walk; edge cases; formula; trap | correct | rows above |
| q0 key, whys, ex | O(V + E) with an adjacency list; O(V²) with a matrix; V pops plus 2E checks | correct | CLRS 22.2 |
| q1 key, whys, ex | prints `['B']` | correct | run by hand |
| q2 key, whys, ex | BFS returns the direct route at 4.0 bp; 2.7 bp through USD is cheaper | correct | 1.2 + 1.5 |
| q3 key, wrong, fb, ex | 6 moves; 7 counts cells | correct | script: l6 quiz maze |

## l7-dijkstra

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb | A, C, B, D, F costs 7; others 8, 9, 9 | correct | script: l7 s0 |
| s0.ex | counting hops is the wrong measure with costs | correct | l6 q2 |
| s1.prose, key, hints, fb | with all costs at least 0, C at 1 is final; B at 4 can still improve to 3 | correct | CLRS theorem 24.6 |
| s1.ex | the smallest tentative cost is safe because every other route starts from something at least as big; needs no negative arrows | correct | CLRS 24.3 |
| s2.prose | heap of (cost, node); push on improvement; an entry above its node's cost is stale | correct | lazy-deletion form (Sedgewick and Wayne 4.4 describes the eager form) |
| s2 states, ops, whys | heap after C, B, E, skip (4, B), D as shown; ties to the earlier letter | correct | script: l7 s2 heap trace |
| s2.ex | pops fix A 0, C 1, B 3, E 3, D 4; then (6, D) stale, F at 7, (9, F) skipped | correct | script: three stale in all |
| s3.prose | at most E + 1 entries; each heap step O(log V) since E ≤ V² | correct | log E ≤ 2 log V |
| s3 key, hints | O((V + E) log V) | correct | CLRS 24.3 (binary heap) |
| s3 why scan, fb | list version O(V²); 10^12 at a million nodes | correct | CLRS 24.3 (array) |
| s3 why bfs, ve | BFS is O(V + E); Bellman-Ford O(V·E), relaxing every edge V − 1 times | correct | CLRS 22.2, 24.1 |
| s3.ex | heap wins on sparse graphs; the scan only pays when nearly every pair is joined | correct | E log V against V² |
| s4 solution, tests, how | lazy Dijkstra; `inf` for unreachable; hub test (300, 1) | correct | script: code widget, l7 s4 |
| s4 fb test-1, 2, 9 | B at 4 means marked on push or overwritten; all nodes in the dict; stale skip | correct | tests[0], [1], [8]; q0 |
| s4.ex | stale check is O(1); without it the answer stays right here, with repeated work | correct | relaxing from a stale larger d cannot lower anything |
| s4.ex | "Test 9 had 300 of them" | wrong | h is pushed 300 times and 299 entries are stale (script). F4 |
| s5 key, wrong, hints, fb | no-check version leaves B at 4 | correct | script: l7 s5 |
| s5.ex | B ends at 4 and F at 9; fix `if u in dist: continue` | correct | script |
| s5.ex | "or `if d > dist[u]: continue`" as a one-line fix | wrong | `dist` starts empty in this code, so it raises `KeyError: 'A'` on the first pop (script). F1 |
| s6 key, hints, fb.correct | true cost A to B is 1 | correct | 3 − 2 |
| s6.prose, fb pop | Dijkstra "treats a popped node as final"; 2 is "the cost Dijkstra fixed" | imprecise | true of the textbook algorithm (CLRS 24.3). The lesson's own `dijkstra` pushes B again and returns 1 (script). F5 |
| s6.ex | a negative arrow can lower a popped cost; a loop below zero has no cheapest cost | correct | CLRS 24.3, 24.1 |
| s7 pattern | O((V + E) log V) when every w ≥ 0 | correct | CLRS 24.3 |
| s7 key, whys, ex | equal weights of 5 give 5 times the BFS distance; BFS is then faster | correct | script: tests[4] |
| s8.prose | 1 bp is 0.01%; costs add along a route "to within a penny" | wrong | adding gives £260.00, compounding £259.98: about 2 pence (script). F7 |
| s8 key, wrong, hints, fb | £260 via EUR and USD; 400 direct; 270; 290 | correct | script: l7 s8 |
| s8.ex | settles EUR 0.5, USD 1.1, CHF 1.2, JPY 2.6; exact £259.98 | correct | script |
| s9 solution, tests, fb | max of Dijkstra costs; 103.4, 110.7, 107.6; −1 if unreachable | correct | script: l7 s9 |
| s9.ex | through Chicago 103.4 ms, through Singapore 115.2 ms | correct | script |
| summary.ideas | non-negative weights make the smallest cost final; stale skip; O((V + E) log V); a negative edge breaks finality | correct | CLRS 24.3 |
| summary.formula, note | relaxation; once per edge from when its tail is popped | correct | CLRS 24.3 |
| summary.trap | without the stale check an old entry can overwrite a cost | correct | holds for the s5 version, which assigns on pop |
| q0 key, fb, ex | seen-on-push gives B = 4; a cost may fall until popped | correct | hand trace |
| q1 key, whys, ex | `{'X': 0}` | correct | run |
| q2 key, whys, ex | about 8.5 x 10^6 against 10^10 | correct | script: l7 quiz sparse |
| q3 key, wrong, fb, ex | at most E + 1 = 10 pushes | correct | script: bound attained on 6 nodes, 9 edges |

## l8-groups

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, fb | groups SHEL+BP, HSBA+BARC+LLOY, AZN+GSK | correct | by hand |
| s0.ex | a group is everything joined by a chain; representative; that is all union-find stores | correct | CLRS 21.1 |
| s1 key, wrong, fb, ex | one link merges two whole groups; union re-points a representative | correct | CLRS 21.1 |
| s2 key, wrong, hints, fb | `find(7)` is 2 by 7, 6, 4, 2 | correct | script: l8 s2 |
| s2.ex | same group exactly when `find` agrees; `find(1)` is 0 | correct | CLRS 21.1 |
| s3 key, wrong, fb | compression re-points 7 and 6; 4 already points at 2 | correct | script |
| s3.ex | next `find(7)` takes one step | correct | parent[7] = 2 |
| s4.prose, key, whys | root 2 heads 6 items, root 0 heads 2; hang the small root; attach root to root | correct | canvas after compression; depths by hand |
| s4.ex | union by size; an item deepens only when its group at least doubles, so depth ≤ log2 n | correct | Sedgewick and Wayne 1.5 (weighted quick-union, depth at most lg N); script |
| s5 solution, tests, fb | DSU with both tricks; `union(2, 2)` is `False` | correct | script: code widget |
| s5.ex | m operations cost O(m α(n)); α(n) ≤ 4 in practice | correct | CLRS theorem 21.14 and section 21.4 |
| s6 key, whys, fb | node-level union loses the link: `False` | correct | hand trace |
| s6.ex | union must join roots | correct | CLRS 21.3 |
| s7 key, wrong, fb, ex | 8 nodes, four merging edges: 4 components | correct | script: l8 s7 |
| s8.prose | minimum spanning tree: joins every node, cheapest edges, no loops; an edge within one root would close a loop | correct | CLRS 23.2, for a connected weighted undirected graph |
| s8 key, same, fb | sort, singletons, find, keep or skip, stop at n − 1 | correct | CLRS 23.2 (Kruskal) |
| s8.ex | sort is O(E log E) and dominates; n − 1 kept edges leave one group; a skipped edge joins connected nodes | correct | CLRS 23.2 |
| s9.prose | link when the absolute correlation exceeds 0.7; a strong negative correlation is the same risk factor | correct | a factor loading of either sign is exposure to that factor; stated as the task's rule |
| s9 solution, tests, fb | clusters at 0.7, 0.6, 0.76; strict threshold | correct | script: l8 s9 |
| s9.ex | HSBA and LLOY at 0.69 share a cluster through BARC | correct | script |
| summary | parent per item; union by size; compression; O(m α(n)); α slower than any logarithm; trap | correct | CLRS 21.4 |
| q0 key, wrong, ex | 3 settlement groups | correct | 6 − 3 |
| q0.prose | each connected group "can be netted to a single settlement" | unverified | framing device, no source; multilateral netting needs an agreed netting set. U7 |
| q1 key, whys, ex | `False 4` | correct | script: tests[4] |
| q2 key, wrong, fb, ex | 2 clients | correct | by hand |
| q3 key, whys, ex | n finds on an n chain cost O(n²); 2.5 x 10^7 at 5,000 | correct | script |

## l9-arbitrage-cycle

| path | claim | verdict | basis |
|---|---|---|---|
| s0.prose | quote convention; arbitrage is a loop returning more than it took | correct | Hull 1.9 (arbitrageurs), 5.10 |
| s0 key, wrong, hints, fb, ex | 1.004824 round GBP, USD, EUR; CHF loop 0.998108; the four-currency loop is below 1 | correct | script: l9 s0 |
| s1 key, wrong, fb, ex | break-even r = 0.855871; at 0.86 the loop makes 0.48%; a loop worth 1 is not an arbitrage | correct | script |
| s2.prose | w = −ln(rate) turns products into sums | correct | ln(ab) = ln a + ln b |
| s2 key, wrong, hints, fb | −0.004812; +0.004812 sign slip; 3.05 sum of rates; 1.004824 product | correct | script: l9 s2 |
| s2.ex | product above 1 is a negative cycle; Dijkstra cannot detect one | correct | CLRS 24.1, 24.3 |
| s3.prose, keys, hints | passes give B = 2; C = 5; D = 6 in the listed order | correct | script: l9 s3 |
| s3.ex | worst order extends one edge per pass; a shortest route has at most V − 1 edges, so V − 1 passes suffice | correct | CLRS lemma 24.2, with no negative cycle reachable |
| s4.prose | one more pass; an improvement means a negative cycle | correct | CLRS theorem 24.4 |
| s4 solution, tests, fb | Bellman-Ford; zero cycle is not negative; unreachable cycle ignored | correct | script: code widget, l9 s4 |
| s4.ex | O(V·E); the extra pass is the detector; ∞ + w is never smaller | correct | CLRS 24.1; IEEE 754 |
| s5 key, whys, hints, fb | w = −rate makes every loop negative; CHF loop −3.012 | correct | 1.142 + 0.92 + 0.95 |
| s5.ex | only −ln turns "above 1" into "below 0"; rate 1 gets weight 0 | correct | derivation in s7 |
| s6 key, whys, hints, fb | prints `True`; the float sum is −5.55 x 10^-17 | correct | script; Pyodide |
| s6.ex | use a tolerance such as 10^-9 | correct | standard floating-point practice |
| s7 key, fb, ex | derivation in four lines; every step reversible | correct | ln is strictly increasing |
| s8.prose | implied cross 0.854331; loop returns 1.0000359 | correct | script: l9 s8 |
| s8 key, wrong, hints, fb | −£264.03 after 3 costs of 1 bp; gross £35.95 | correct | script |
| s8.ex | 0.36 bp gross against 3 bp of costs; costs make each weight −ln(0.9999 x rate) | correct | script |
| s8.ex | mispricings between liquid quotes are this small, so triangular arbitrage rarely survives costs | correct | Fenn et al. (2009): triangular opportunities exist but most have short durations and small magnitudes, and are not profitable over time |
| s9.prose, solution, tests | start node at weight 0 to every currency; `eps=1e-9`; 10 tests | correct | script: code widget, l9 s9; CLRS 24.4 (super-source) |
| s9 fb, ex | test-2, test-4, test-9 name their faults; £4,824 on £1m | correct | tests[1], [3], [8] |
| summary | product rule; negative cycle; V − 1 passes plus one; tolerance; formula; trap | correct | rows above |
| q0 key, wrong, fb, ex | 320 relaxations; 280; 360 | correct | 8 x 40 |
| q1 key, whys, ex | 0.99949; 5.1 bp spread; weight +0.000510 | correct | script |
| q2 key, wrong, fb, ex | implied EUR/GBP 0.8400; 1.1905 inverted | correct | script |
| q3 key, whys, ex | a rate above 1 gives a negative weight; Dijkstra needs weights at least 0 | correct | CLRS 24.3 |

## review-2

| path | claim | verdict | basis |
|---|---|---|---|
| i0 key, whys, ex | route S, A, C, T | correct | parent walk |
| i1 key, wrong, fb, ex | cheapest S to T is 8; 14; 11 | correct | script |
| i2 key, whys, ex | `[0, 0, 0, 0, 0]` after `find(4)` | correct | by hand |
| i3 key, wrong, fb, ex | 1.000579; 5.8 bp; weight −0.000579 | correct | script |
| i4 key, wrong, fb, ex | three stale entries: (6, B), (9, C), (13, T) | correct | script |
| i5 key, wrong, fb, ex | Kruskal total 11; 10 keeps a loop edge; 15 keeps five edges | correct | script: minimum over all spanning trees |
| i6 key, wrong, fb, ex | 5 passes; node k fixed after pass k | correct | script |
| i7 key, whys, ex | union-find for incremental connectivity; BFS is O(V + E) per query; O(α(n)) per operation | correct | CLRS 21.4 (amortised) |

## homework-2

| path | claim | verdict | basis |
|---|---|---|---|
| i0 solution, tests, fb, ex | grid BFS; 6, 16, 58, 10; O(rows x cols) | correct | script: code widget |
| i1.prose | Dijkstra ignores the hop limit | correct | plain Dijkstra keeps one cost per node |
| i1 solution, tests, fb | k + 1 rounds from a copy; 4.0, 2.7, 2.6; 7.5, 4.3, 4.2 | correct | script: hw2 within k |
| i1.ex | after round i, cheapest routes of at most i conversions; O(k·E) | correct | CLRS 24.1 path-relaxation property |
| i2 solution, tests, fb, ex | union-find on shared identifiers | correct | script: code widget |
| i3 key, fb | proof order p1 to p5 | correct | CLRS theorem 24.6, sketched |
| i3.ex | a negative edge breaks line 4 | correct | the remainder of the route could be negative |
| i4 key, wrong, fb, ex | 103.4 ms; 115.2; 118.0; settle order | correct | script |
| i5 key, wrong, fb | £1,195.55; gross 1,796.51; one cost 1,596.15; 18 bp | correct | script: hw2 triangle |
| i5.ex | "a gap this wide between liquid quotes would close within milliseconds" | unverified | no source for the timescale. U8 |
| i6 key, whys, ex | Bellman-Ford for negative edges with no negative cycle; O(V·E) | correct | CLRS 24.1 |
| i6 why Dijkstra | "Dijkstra's answers may be wrong" | imprecise | true of the textbook algorithm; the course's lazy code returns the right costs here, more slowly. F5 |
| i7 model (a) | bid as a to b, 1/ask as b to a; weight −ln(rate) less the log of a fee factor | correct | Hull 1.3 (Table 1.1, bid and offer quotes); −ln(rate x f) |
| i7 model (b) | V − 1 passes; a further improvement means a reachable negative cycle; start node | correct | CLRS 24.1 |
| i7 model (c) | V = 31, E = 830: about 26,000 relaxations, a few milliseconds | correct | 31 x 830 = 25,730 |
| i7 model (d) | step back V times through `parent` to land in the cycle; tolerance for −5.6 x 10^-17 | correct | Sedgewick and Wayne 4.4; l9 s6 |
| i7 model (e) | worked example: 1.0000359 gross, £36, costs about £300, loss about £264 | correct | l9 s8 |
| i7 model (e) | liquid mispricings are "a fraction of a basis point" | unverified | Fenn et al. (2009) report small magnitudes but I could not confirm the figure. U9 |
| i7 rubric | seven lines, 10 points | correct | matches the model |
| i8.prose | fees are whole pence, at least 1; routes differ when their link lists differ | correct | conditions the count needs |
| i8 solution, tests, how | Dijkstra with route counts; 11 tests | correct | script: code widget; equals brute force on 200 random maps |
| i8 fb test-2 to test-11 | each names the fault its test catches | correct | traced tests[1] to [10] |
| i8.ex | with fees at least 1, a cheapest route passes only venues that leave the heap first, so counts are final on leaving | correct | strict positivity gives a strict order of settlement (CLRS 24.3) |

## l10-every-subset

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, fb, ex | 8 holdings; 7 without the empty one; 6 orders; 3 singles | correct | 2³ |
| s1 key, wrong, fb, ex | four leaves hold B; each stock is in half the holdings | correct | 2² |
| s2 key, hints, fb | fifth leaf recorded is B C | correct | script: l10 s2 |
| s2.ex | backtracking defined as a depth-first walk over choices, undoing each | correct | CLRS has no chapter; Skiena, *Algorithm Design Manual* 7.1 |
| s3 key, wrong, fb | 1,024; 100; 20; 10! | correct | 2^10 |
| s3.ex | walk visits 2^(n+1) − 1 nodes | correct | full binary tree |
| s4 key, wrong, fb, ex | Y Z X and Z Y X send X last; n! orderings | correct | by hand |
| s5 key, whys, hints, fb, ex | storing `path` prints eight empty lists | correct | Python reference semantics; run by hand |
| s6 pattern, key, whys, ex | choose, recurse, un-choose; 120 orderings of 5 | correct | 5! |
| s7 key, hints, fb, ex | order of the walk's lines; pop sits between the calls | correct | l10 s2 code |
| s8 key, whys, hints, ex | 8 lists, 4 holdings; 6 if repeats counted | correct | script: l10 s8 |
| s9 solution, tests, fb, ex | subsets and permutations; `[[]]` for empty input | correct | script: code widget |
| s10 key, wrong, fb, ex | 42 portfolios of at most 3 of 6; 41; 20; 64; 120 | correct | script |
| s11 key, wrong, fb | 12.4 days; 298 hours; 1,073,742 s | correct | script |
| s11.ex | 40 stocks take about 35 years | correct | script |
| summary | backtracking; 2^n and n!; copy at the leaf; trap | correct | rows above |
| q0 key, whys, ex | no pop: paths pile up as shown | correct | script: l10 q-no-pop |
| q1 key, wrong, ex | `subsets([])` has 1 list | correct | 2^0 |
| q2 key, wrong, fb, ex | 24 orders | correct | 4! |
| q3 key, wrong, fb, ex | 15 calls | correct | 2^4 − 1 |

## l11-dead-ends

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb, ex | six safe cells under r1c2 | correct | script: l11 s0 |
| s1 key, hints, fb, ex | r3c1, r4c1, r4c3 safe; answer r1c2, r2c4, r3c1, r4c3 | correct | by hand |
| s2 key, wrong, fb | 2 placements, mirror images | correct | script: `n_queens(4)` |
| s2 hint | a corner queen "leads to a dead end by row 3" | imprecise | from r1c1, r2c3 dies in row 3 but r2c4 reaches r3c2 and dies in row 4 (script); the explain says "row 3 or row 4". F14 |
| s2.ex | pruning defined; corners fail in row 3 or row 4 | correct | script |
| s3 keys, hints, fb | 16, 64, 256 without pruning; 6, 4, 2 with; totals 341 and 17 | correct | script: l11 s3 |
| s3.ex | 8 queens: 19,173,961 against 2,057; pruning changes the work, not the answers | correct | script |
| s4 key, hints, fb, ex | three take-6 branches refused; only 3 + 5 hits 8; safe because totals cannot fall with positives | correct | by hand |
| s5 key, wrong, hints, fb, ex | 3 combinations; 6 ordered sums; 1 without reuse | correct | script: l11 s5 |
| s6 key, whys, hints, fb | unsafe prune returns `False` on 6, −4, 3 with target 2 | correct | script |
| s6.ex | a prune is safe only if a failing branch can never recover | correct | definition of a valid bound (Skiena 7.1) |
| s7 pattern, key, whys, ex | sorted and positive: if `xs[i]` overshoots, all later ones do | correct | xs sorted ascending |
| s8 solution, tests, fb | queens counts 1, 0, 0, 2, 10, 4, 92; subset sum cases | correct | script: code widget; OEIS A000170 |
| s8 how | without pruning the last test "takes far longer than the 5-second limit" | imprecise | Pyodide: the unpruned walk takes 6.8 s here, a margin of about 1.4 times. F18 |
| s8.ex | row − col and row + col index the diagonals; O(1) safety test | correct | geometry |
| s9 keys, whys, fb, ex | budget, rota and count prunes are safe; net exposure is not | correct | +5 − 3 + 2 − 4 = 0 passes +2 |
| summary | pruning; safe prune; restore state; formula 341 against 17; trap | correct | rows above |
| q0 key, wrong, fb, ex | 3 queens on 3 by 3: none | correct | script |
| q1 key, wrong, fb, ex | 8^8 = 16,777,216 full boards; 8! is itself a prune | correct | script |
| q2 key, whys, ex | no undo: `n_queens(4)` returns 0 | correct | script: l11 q-restore |
| q3 key, wrong, fb, ex | 2 lists: [2, 2, 3] and [7] | correct | script |

## l12-remembering

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb, ex | f(2) computed three times, f(3) twice, in `fib(5)` | correct | tree by hand |
| s1 key, wrong, fb | 25 calls for `fib(6)` | correct | script: l12 call counts |
| s1.ex | calls grow about 1.6 times per step; `fib(30)` makes 2,692,537 calls for 832,040; 31 distinct values | correct | script; golden ratio 1.618 |
| s2 key, hints, fb | hits at f(1) under f(3), f(2) under f(4), f(3) under f(5) | correct | script: 3 hits |
| s2.ex | 15 calls become 9; memoisation; top-down dynamic programming | correct | script; CLRS 15.3 |
| s3 keys, fb | cache 1, 2, 3, 5, 8; naive column 5, 8, 5, 3, 2, 1, 1; 7 values | correct | script: l12 s3 |
| s3.ex | work is the number of different subproblems | correct | CLRS 15.3 |
| s4 key, wrong, fb, ex | 31 values; 28 hits; 59 calls; O(n) | correct | script: l12 s4 |
| s5 key, wrong, hints, fb, ex | 10 paths on 3 by 4 points; C(5, 2) | correct | script |
| s6 key, whys, hints, fb | prints 95.24 twice | correct | script: l12 s6 |
| s6.ex | cache only pure functions; pass `rate` as an argument | correct | Python docs `functools.lru_cache` |
| s7 pattern | function must be pure; work is states times work per state | correct | CLRS 15.3 |
| s7 key, whys, ex | a list argument raises `TypeError`; tuples, floats, strings are hashable | correct | script; Python data model `__hash__` |
| s8 key, wrong, hints, fb, ex | warm default dict: `fib(6)` prints one line | correct | Python FAQ on mutable default arguments; hand trace |
| s9 solution, tests, how, fb | `fib_memo` and `grid_paths`; 18 by 18 needs billions of calls uncached | correct | script: code widget; 2·C(34, 17) − 1 |
| s9.ex | n + 1 values; at most r x c points; count is C(r + c − 2, r − 1) | correct | script |
| s10 key, wrong, fb | 496 nodes for 30 steps; 2^30 paths | correct | 31 x 32 / 2 |
| s10.ex | recombining tree; memoising on (step, ups) is the pricer's backward induction | correct | Hull 13.1 to 13.4 |
| summary | repeated subproblems; memoisation; purity and hashable keys; formula; trap | correct | rows above |
| q0 key, wrong, fb, ex | 25 prices computed | correct | 25 distinct keys |
| q1 key, whys, ex | method cache keyed on `self` by identity returns `0.907`; keeps every `Curve` alive | correct | script: l12 q-method; Python docs `lru_cache` |
| q2 key, wrong, ex | 41 calls for `fib(7)` | correct | script |
| q3 key, whys, ex | `fib_memo(0)` is `(0, 1)` | correct | script |

## l13-climbing-stairs

| path | claim | verdict | basis |
|---|---|---|---|
| s0 key, wrong, hints, fb, ex | 5 ways to climb 4 stairs | correct | script: l13 stairs |
| s1 key, fb, ex | last step from stair 3 or 4; ways(5) = ways(4) + ways(3); no double count | correct | disjoint cases by last step |
| s2 keys, fb | 2, 3, 5, 8, 13 | correct | script |
| s2.ex | bottom-up dynamic programming; O(n) | correct | CLRS 15.1, 15.3 |
| s3 key, whys, ex | `prev = 8`, `cur = 13`; O(1) space, O(n) time | correct | hand trace |
| s4 key, wrong, fb, ex | `ways(0) = 0` returns 3 for 4 stairs; ways(0) = 1 | correct | script: l13 s4 |
| s5.prose, keys, hints, fb | best(a) = 1 + min best(a − c); table 0, 1, 2, 1, 1, 2, 2 | correct | script: l13 coins table |
| s5.ex | greedy gives 4 + 1 + 1; the recurrence checks every last coin | correct | optimal substructure (CLRS 15.3; Kleinberg and Tardos 6.4) |
| s6 key, wrong, hints, fb, ex | filling from the top amount down returns −1; final table 0, 1, ∞, 1, 1, ∞, ∞ | correct | script: l13 s6 |
| s6.prose | the failing loop is labelled "top down" | misleading | l12 s2 named memoisation "top-down dynamic programming", which is correct for this problem (script). F8 |
| s7 recipe, key, whys, ex | three-step recurrence; 1, 1, 2, 4, 7, 13 | correct | script |
| s8 key, hints, fb, ex | recipe order for coins | correct | s7 recipe |
| s9 solution, tests, fb, ex | `stairs` and `min_coins`; amount x len(coins) steps | correct | script: code widget |
| s10.prose | up or down by the same factor returns to £100 after an up and a down | correct | u x (1/u) = 1 (Hull 13.7, Cox-Ross-Rubinstein d = 1/u) |
| s10 key, wrong, fb, ex | 20 paths; Pascal's triangle | correct | C(6, 3) |
| s11 key, wrong, fb, ex | 2 trades for 1,100 from lots 100, 500, 600, 900 | correct | script |
| summary | last-choice split; bottom-up order; coins recurrence; trap | correct | rows above |
| q0 key, whys, ex | `min_coins([2, 5], 0)` is 0 | correct | script |
| q1 key, wrong, fb, ex | 4 coins for 11 from 2 and 5; greedy is stuck | correct | script |
| q2 key, wrong, ex | 13 ways with steps of 1, 2, 3 | correct | script |
| q3 key, whys, ex | ways(0) = 1: the empty climb | correct | s4 |

## review-3

| path | claim | verdict | basis |
|---|---|---|---|
| i0 key, wrong, fb, ex | 16 subsets of four items | correct | 2^4 |
| i1 key, whys, ex | node-recording walk gives `[]`, `[1]`, `[1, 2]`, `[1, 2, 3]` first | correct | hand trace |
| i2 key, wrong, fb, ex | 2 safe cells in row 2 under r1c1; one under r1c2 | correct | l11 s0, s3 |
| i3 key, whys, ex | unsafe prune returns `False` on 4, −2, 1 with target 3 | correct | script |
| i4 key, wrong, fb, ex | 67 calls for `fib(8)`; 9 memoised values | correct | script |
| i5 key, whys, ex | `days_to_expiry` reads a global outside the key | correct | l12 s6 |
| i6 key, wrong, fb, ex | ways(6) = 24 | correct | script |
| i7 key, wrong, fb, ex | 2 coins for 11 from 1, 5, 6, 9; greedy takes 3 | correct | script |
| i8 keys, whys, ex | memoisation pays for `fib` and grid paths, not for listings or queens | correct | overlapping subproblems (CLRS 15.3); in a row-by-row search no partial board repeats |

## homework-3

| path | claim | verdict | basis |
|---|---|---|---|
| i0 solution, tests, fb, ex | combination sum with reuse; counts 45 and 192 | correct | script: code widget, hw3 combination counts |
| i1 solution, tests, fb | word break memoised on the start index | correct | script: code widget |
| i1 how | 40 letters split in billions of ways | correct | script: 1.4 x 10^11 compositions with parts 1 to 4 |
| i1.ex | len(s) + 1 states, about n x \|words\| prefix checks | correct | CLRS 15.3 |
| i2 key, fb, ex | order of the permutation walk's lines | correct | l10 s9 |
| i3 key, wrong, fb, ex | 12 orders with A before D | correct | script |
| i4 key, wrong, fb, ex | 2,121 states | correct | 21 x 101 |
| i5 key, wrong, ex | 252 paths return after 10 days | correct | C(10, 5) |
| i5 fb half | "half of all paths do not return" | wrong | 772 of 1,024 paths, about 75%, do not return (script). F15 |
| i6 key, whys, ex | memoised `grid_paths` is O(r x c) | correct | states times O(1) |
| i7 prompt | the 2^25 script "never finishes" | misleading | building and filtering 2^25 subsets takes seconds in CPython (script); l10 s11 needed 1 ms per subset to reach days. F16 |
| i7 model (a) | 33,554,432 subsets; 245,506 of size at most 6 | correct | script |
| i7 model (b) | walk on (i, count, net); count prune safe; net prune unsafe; bound prune on 10k | correct | +5 + 2 − 3 − 4 = 0; \|net\| can change by at most 10 per trade |
| i7 model (c) | at most 26 x 7 x 121 = 22,022 states; pure function, hashable arguments | correct | script |
| i7 model (d) | test list | correct | covers the unsafe prune and the size rule |
| i7 rubric | six lines, 10 points | correct | matches the model |
| i8 solution, tests, how | two-state table, flat and long | correct | script: equals an exhaustive DP on 300 random series |
| i8 fb test-2 to test-7 | worked cases 8, 7, 3, 4, 0, 0 | correct | script; tests[1] to [6] by hand |
| i8.ex | recurrences for flat and long; start 0 and −∞; O(n) | correct | Kleinberg and Tardos 6.1 style state argument; script |

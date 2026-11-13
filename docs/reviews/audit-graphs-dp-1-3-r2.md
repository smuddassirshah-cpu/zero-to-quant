# Concept audit, round 2: graphs-dp levels 1 to 3 (topic 1.8, Stage 1)

Blind auditor: Fable. Scope: `app/content/courses/graphs-dp/` lessons l1 to l13, review-1 to review-3, homework-1 to homework-3 (19 files). Level 4 was not read. The earlier reviews, the round 1 audit, its fix pass and the author reports were opened only after the ledger and the findings below were committed (WIP commit named in the overlap section).

- Ledger: `docs/reports/audit-graphs-dp-1-3-r2-ledger.md`, 276 rows: 254 correct, 5 wrong, 17 imprecise, 0 misleading, 0 unverified.
- Script: `docs/reports/graphs-dp-L1-3-r2-concepts.py`, 320 checks. It exits 1 today: the 20 failing checks are the content findings below (the fix pass turns them green by changing content).
- Findings: 11 (5 wrong, 6 imprecise, 0 misleading). Serious 0, minor 11. Finding 6 is one class covering 12 feedback lines.

## What was run

| check | result |
|---|---|
| `node tools/validate.mjs` | 0 errors (4,534 warnings, none new); manifest unchanged |
| `docs/reports/graphs-dp-1-perf-numbers.py`, `-2-`, `-3-` (run, not opened) | exit 0, 0, 0 |
| `node tools/grade-all.mjs --file` on the 19 files | 155 widgets, 0 failures |
| `docs/reports/graphs-dp-L1-3-r2-concepts.py` (CPython 3.13.18) | 320 checks, 20 failed, exit 1 (each failure is listed below) |
| Pyodide 0.27.7 (Python 3.12.7) under node, through the page's own grader (`GRADER` from `js/screens/drill-worker.js`, recursion limit read as 3,000) | 38 code widgets: every solution passes every hidden test, every starter fails; the 127 submissions of script part C (110 named mistakes, 13 variants, 4 controls) run for the `test-N` lines |

No playthrough was run (no content changed).

Method for the `test-N` lines. For each line that names a mistake I wrote a submission with that mistake and ran it against the widget's own tests, in Pyodide and again in CPython (part C of the script). The line holds when the first failing test is N. Timing and depth claims were measured in Pyodide: the solutions' slowest test takes 98 ms; a recursive search fails with `RecursionError` on the 3,000-node, 5,000-node and 5,001-node chains (limit 3,000 plus the harness frames); the unpruned `subset_sum` takes 10.6 s on l11 test 13 (limit 5 s); the naive `find` takes 0.92 s on l8 test 9 (limit 0.5 s inside the test); a 400-deep recursive flood fill passes l4 test 11.

Conditions checked and found stated where they matter: BFS shortest paths only for unweighted graphs (l2 quiz, l6 screens[8] and quiz); Dijkstra only for weights of at least 0 (l7 screens[1], [6], [7], summary; homework-2 proof and h-pick); topological order only on a DAG (l5 screens[0], [7], summary); greedy against the table (l13 screens[5], [11], quiz); safe pruning only for quantities that cannot fall back (l11 screens[6], [7], [9]); every big-O line names or implies its representation (adjacency list for O(V + E), matrix for O(V^2), heap for O((V + E) log V), both tricks for O(m α(n))).

## Findings

1. `l8-groups.json` | `screens[7].widget.wrong[0]` (id `edges`, value 3) with `screens[7].feedback.byKey.edges` | **wrong**, minor | The line says "You counted only the groups with edges", but that count is 2, not 3. A learner who answers 2 gets the generic line; one who answers 3 is told a mistake they did not make. | The groups with edges are {0, 1, 2, 3} and {5, 6}. Script check `l8 screens[7] slip "edges"`. The sister item `quiz[0]` (`pairs`, value 2) has the same line and the right value. | Set `screens[7].widget.wrong[0].value` to `2`. Keep the text.

2. `l11-dead-ends.json` | `quiz[0].feedback.byKey.two` | **wrong**, minor | "You may have checked only columns" cannot explain an answer of 2: checking only columns gives 3! = 6, which is the `orders` slip. | Script check `l11 quiz q-three slip "two"`. Two is the 4 by 4 answer from screens[2]. | Replace the line with: "Two is the count for a 4 by 4 board. On 3 by 3, every start runs out of safe cells by row 3."

3. `homework-3.json` | `items[3].feedback.byKey.fixed` (value 6) | **wrong**, minor | "You fixed A first and D last" leaves 2 orders (B and C in the middle), not 6. Six is A first alone. | Script check `hw3 h-legs slip "fixed"`: A first and D last 2; A first 6. | Replace the line with: "You sent A first every time, which leaves $3! = 6$ orders. A only needs to come before D, anywhere."

4. `l4-islands.json` | `screens[8].widget.tests[5]` and `screens[8].feedback.byKey["test-6"]` | **wrong**, minor | "Test 6 checks the boundary" is false: `[[-50, -51]]` with limit 50 has 1 region under `<` and under `<=`. A submission using `<=` passes all 7 hidden tests although `how` says strictly below. | Pyodide run of the `<=` submission: every test passes. Script checks `l4 screens[8] test 6` and `C ... non-strict <=`. | Change `tests[5]` to `{"call": "count_loss_regions([[-50, 10, -51]], 50)", "expect": "1", "compare": "equal"}` (strict gives 1, `<=` gives 2; script check `l4 proposed replacement test`). Replace the line with: "Test 6 checks the boundary: −50 is not below −50, so only −51 counts and the answer is 1. Compare with `<`, not `<=`."

5. `l3-going-deep.json` | `screens[5].hints[1]` (text and highlight) | **wrong**, minor | "A node can be on the stack twice, as G is here" names the wrong node. With reverse-sorted pushes on this graph the node pushed twice is D (by A, then by C). G is pushed once, by E. | Script check `l3 screens[5].hints[1]`: pushed twice ['D']. With the sorted pushes of screens[4] it is B, so G is right in neither version. | Text: "A node can be on the stack twice, as D is here." Highlight: `["D"]`.

6. Twelve `test-N` lines name a mistake that fails an earlier test, so the learner who makes it sees only "Check the first failing test" | **imprecise**, minor (each) | Evidence: Pyodide and script part C; the first failing test of each mistaken submission is given. Fix pattern: move the diagnosis to the test that fails first, and let the later line describe its own test. All texts below were checked against the runs.

   a. `l2-level-by-level.json` | `screens[4].feedback.byKey["test-3"]` | marking on pop fails test 1 (G appears twice). | Add `"test-1"`: "Test 1 is the lesson's graph. If G appears twice, mark nodes seen when you queue them, not when you pop them." Replace `test-3` with: "Test 3 is a square: D is next to both B and C, and must appear once. The answer is `['A', 'B', 'C', 'D']`."

   b. `l2-level-by-level.json` | `screens[8].feedback.byKey["test-7"]` | no late-marking submission fails first on the triangle: marking on pop fails test 5 (Oak twice), and two unmarked variants fail test 4 or pass everything. | Add `"test-5"`: "Test 5 has k = 10, so the search goes right round the loop through Oak. If a firm appears twice, mark firms when they are found." Replace `test-7` with: "Test 7 is a triangle with k = 1. B and C are each one edge from A, so the answer is `['B', 'C']`."

   c. `l3-going-deep.json` | `screens[2].feedback.byKey["test-4"]` | no `seen` check (or a parent-only check) raises `RecursionError` on test 1. | Add `"test-1"`: "Test 1 is the lesson's graph, which has a loop. A `RecursionError` means a node was visited twice: check `seen` before each call." Replace `test-4` with: "Test 4 is a triangle, a loop of three. Each node appears once: `['A', 'B', 'C']`."

   d. `l3-going-deep.json` | `screens[5].feedback.byKey["test-3"]` | no skip on pop fails test 1 (D twice). On the square of test 3 the repeated node is C, not D. | Replace `test-1` with: "Test 1 is the lesson's graph. If you got A, D, F, ... push `sorted(adj[u], reverse=True)`. If D appears twice, skip a popped node that is already in `seen`." Replace `test-3` with: "Test 3 is a square. C is pushed by both A and D, but it must appear once: `['A', 'B', 'D', 'C']`."

   e. `l4-islands.json` | `screens[4].feedback.byKey["test-5"]` | eight neighbours fail test 1 (4 islands, not 6). | Add `"test-1"`: "Test 1 is the map above, with 6 islands. A 4 means cells meeting at a corner were joined: use only the four side neighbours." Replace `test-5` with: "Test 5 is two cells meeting at a corner: two islands."

   f. `l6-fewest-steps.json` | `screens[8].feedback.byKey["test-3"]` | pairs stored one way fail test 1 (−1 for NGN to THB, in either direction). | Replace `test-1` with: "Test 1 expects 4: NGN, ZAR, USD, SGD, THB. A 5 means you counted currencies, not conversions. A −1 means each pair was stored one way only: add both directions." Replace `test-3` with: "Test 3 goes from HUF back to GBP, against the order the pairs are written in. It still takes 3 conversions."

   g. `l7-dijkstra.json` | `screens[4].feedback.byKey["test-2"]` | a dict of reached nodes only fails test 1, where G is unreachable from A. | Replace `test-1` with: "Test 1 expects B at 3, F at 7 and G at `math.inf`. B at 4 means you marked nodes seen when first pushed, or a stale pop overwrote a cost. A missing G means unreachable nodes were left out of the dict." Replace `test-2` with: "Test 2 starts at G, which reaches only F. Every other node stays at `math.inf`."

   h. `homework-2.json` | `items[1].feedback.byKey["test-2"]` | relaxing without a copy (and plain Dijkstra) fails test 1 with 2.6. | Replace `test-1` with: "Test 1 allows no intermediates: only the direct quote, 4.0 bp. A −1 means you ran `k` rounds, not `k + 1`. A 2.6 means one round chained several conversions: relax from a copy of last round's costs." Replace `test-2` with: "Test 2 allows one intermediate currency, so GBP, EUR, USD, JPY at 2.6 bp is too long. The answer is 2.7 bp through USD."

   i. `homework-2.json` | `items[8].feedback.byKey["test-4"]` | returning when `dst` is first reached fails test 1 with (3, 1). | Add `"test-1"`: "Test 1 has two cheapest routes at 3, through PAR and through FRA. A count of 1 means you returned when AMS was first reached: wait until it comes off the heap." Replace `test-4` with: "Test 4 reaches AMS first for 9, then for 2 through PAR. The cheaper cost replaces the first, so the answer is `(2, 1)`."

   j. `l10-every-subset.json` | `screens[9].feedback.byKey["test-5"]` | storing `path` itself fails test 1 (every list is `[]`). No submission that passes test 1 can fail test 5: 8 different contents are 8 objects. | Replace `test-1` with: "Test 1 checks the order: take before skip. If you got `[]` first, swap the two branches. If every list is `[]`, you stored `path` itself: store `path[:]`." Replace `test-5` with: "Test 5 checks that the 8 stored subsets are 8 separate lists."

   k. `l12-remembering.json` | `screens[9].feedback.byKey["test-4"]` | counting lookups fails test 3 with (8, 11). | Add `"test-3"`: "Test 3 expects `(8, 7)`. An 11 means you counted cache lookups as well as computations. A 5 means the cache outlived the earlier tests: make it inside `fib_memo`." Replace `test-4` with: "Test 4 expects `(832040, 31)`: 31 values, one for each `n` from 0 to 30."

   l. `l12-remembering.json` | `screens[9].feedback.byKey["test-6"]` | the hidden tests share one namespace, so a module-level or default-argument cache fails test 3 with (8, 5), long before test 6. | The `test-3` line in (k) covers it. Replace `test-6` with: "Test 6 runs `fib_memo(10)` twice and expects 11 both times, because each call starts with an empty cache."

7. `l3-going-deep.json` | `screens[3].explain.text` (third sentence) | **imprecise**, minor | "On a tree there is no cycle, so the bug can hide until real data arrives." True only for a tree stored as parent-to-child arrows. Lessons 1 to 3 store undirected graphs at both ends, and there a DFS with no `seen` set never returns even on a two-node tree: A calls B, B calls A. The same lesson's quiz (`q-tree`) has to say "ignore the edge back to the node a call came from". | Script check `l3 screens[3].explain`. | Replace the sentence with: "On a tree stored as parent-to-child arrows nothing leads back, so the bug can hide until real data arrives."

8. `l7-dijkstra.json` | `screens[5].explain.text` (second sentence) | **imprecise**, minor | "Here B ends at 4 and F at 9, both wrong." D ends wrong too, at 6 against a true 4; the explain canvas already shows D·6. A learner reads that only two nodes are wrong. | Script check `l7 screens[5].explain`: wrong nodes B (4, true 3), D (6, true 4), F (9, true 7). | Replace the sentence with: "Here B ends at 4, D at 6 and F at 9, all wrong."

9. `l7-dijkstra.json` | `summary.trap` | **imprecise**, minor | "Without the stale check, an old larger entry can pop later and overwrite a correct cost." In the pattern the lesson teaches (cost set at the push, guarded by `d + w < dist[v]`) leaving out the check never overwrites anything; it only repeats work, as `screens[4].explain` says. The overwrite happens only in the trap's version, which records the cost at each pop. | Pyodide run: the taught code without the check passes tests 1 to 8 and fails only the scan-count test 9. | Replace with: "Recording a cost at every pop, with no stale check, lets an old larger entry overwrite a correct cost."

10. `l13-climbing-stairs.json` | `screens[10].explain.text` (second sentence) | **imprecise**, minor | "That is Pascal's triangle: the same recurrence as climbing stairs, on a lattice." Pascal's rule, count(i, j) = count(i − 1, j) + count(i, j − 1), is not the stairs recurrence ways(n) = ways(n − 1) + ways(n − 2); one gives binomial coefficients, the other Fibonacci numbers. What they share is the split by the last move. | Derivation. | Replace the sentence with: "That is Pascal's triangle: the same split by the last move as climbing stairs, on a lattice."

11. `l1-nodes-and-edges.json` | `screens[5].explain.text` | **imprecise**, minor | "Each edge costs two appends, so the build takes $O(V + E)$ time" is said of a function that also sorts every list, which costs O(sum of deg log deg). | Derivation; CLRS 22.1 for the unsorted build. | Replace the text with: "Building from `nodes` first keeps isolated nodes. Each edge costs two appends, so the appends take $O(V + E)$ time and the dict holds $2E$ entries. Sorting costs a little more, and is only there to make the output fixed."

## Checked and left alone

- `l9-arbitrage-cycle.json` `screens[4].byKey["test-6"]`: non-strict detection (`<=`) fails test 1, not test 6, but the line names no mistake; it only states that a zero cycle is not negative, which is right.
- `l11-dead-ends.json` `screens[8].byKey["test-10"]`: testing `i == len(xs)` before `total == target` fails test 9 first, but a submission that special-cases the empty list does reach test 10, and the line's advice fits it.
- `l8-groups.json` `screens[5].byKey["test-5"]`: a union with no root check fails test 4 first; a union that lowers the count before the check reaches test 5, so the line holds.
- `l9-arbitrage-cycle.json` `screens[6]`: the floating-point sum is −5.551115123125783e−17 in Pyodide 0.27.7 as well as in CPython, so `True` is right on the page.
- "About 1,000 frames by default" (l3) is true of CPython; the page sets 3,000. Every depth the content relies on (3,000, 5,000, 5,001, 90,000) is past both.

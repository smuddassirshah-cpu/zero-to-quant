# Concept audit, round 2: graphs-dp levels 1 to 3 (topic 1.8, Stage 1)

Blind auditor: Fable. Scope: `app/content/courses/graphs-dp/` lessons l1 to l13, review-1 to review-3, homework-1 to homework-3 (19 files). Level 4 was not read. The earlier reviews, the round 1 audit, its fix pass and the author reports were opened only after the ledger and the findings below were committed (WIP commit `a218df99`).

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

## Overlap with the earlier reads

Read after the WIP commit `a218df99`: `docs/reviews/review-1.8.md` (graphs-dp L1 to L3 part and its fix pass), `docs/reviews/audit-graphs-dp-1-3.md` (round 1 audit, its fix pass, the fix-pass read and the follow-up).

What the earlier reads hold for this scope: the 1.8 review has no conceptual finding (three over-long explains and sentence lengths only). The round 1 audit has 18 findings and 9 unverified rows, all fixed; the fix-pass read has 1 finding, fixed in the follow-up. This audit read the content after those fixes, so it could not meet them again; every fixed sentence was read here as a ledger row and each one stands (for example l6 `with-d`, l3 `q-post` option `rev`, l5 screens[4], l7 screens[4] to [6] and [8], l11 `how`, homework-3 `half`).

| | count |
|---|---|
| Conceptual findings by this audit only | 11 (finding 6 covers 12 lines) |
| By an earlier read only (1.8 review 0, round 1 audit 18 plus 9 unverified rows, fix-pass read 1), all fixed before this read | 28 |
| By both | 0 |
| Earlier findings still standing in the content | 0 |

How the two rounds relate, finding by finding:

- Findings 1, 2 and 3 (slip values whose line names another mistake) and finding 5 (the hint naming G): round 1 reported that no `wrong[]` value or slip was incorrect and recomputed lines from their mistakes; these four were missed.
- Finding 4 (l4 test 6) and finding 6 (12 `test-N` lines): round 1 finding 10 is the neighbouring class, three lines that named a slow method their test cannot catch. It did not run a submission per line, so the lines that name a mistake caught by an earlier test went unseen. None of the 12 lines is one of round 1's three.
- Finding 8 sits in a sentence round 1 rewrote: its finding 1 fixed the last sentence of `l7` screens[5].explain and carried "both wrong" through, and the fix-pass read passed the row.
- Finding 9 is the summary-level echo of round 1 finding 5 (the taught lazy code against textbook Dijkstra); the fix pass corrected screens[6] and left the summary trap.
- Findings 7, 10 and 11 have no counterpart.

New `wrong` findings that no earlier read found: **5** (findings 1 to 5), all minor. None changes a graded key; finding 1 changes one slip value and finding 4 one hidden test.

By the convergence rule (at most one new `wrong` per three levels) the course does not close on round 2.

## Fix pass

Fixer: Opus. Every fix below was established from my own runs, not from the auditor's text: part D of `docs/reports/graphs-dp-L1-3-r2-concepts.py` holds my own submissions (each the widget's solution with one named mistake put in by a text replacement), run through the same harness as part C (CPython, recursion limit 3,000, 5 s per test, one shared namespace across tests as in `js/engine/widgets/code.js`); part E recomputes every numeric slip. Borderline timings were run in Pyodide 0.27.7 under node from the local pkgs folder.

| # | status | basis (own) |
|---|---|---|
| 1 | fixed | Union-find on 0–1, 2–3, 1–3, 5–6 leaves {0, 1, 2, 3} and {5, 6} with edges: 2, twice (part E and by hand). Slip `edges` 3 → 2; no clash with the key 4. Text kept. |
| 2 | fixed differently | Columns only gives 3! = 6, one diagonal direction gives 3, both computed: no 3 by 3 mistake gives 2. Two is the 4 by 4 count (enumerated: 2). New line: "Two is the count for 4 queens on a 4 by 4 board. On 3 by 3, every start runs out of safe cells by row 3." Slip value unchanged. |
| 3 | fixed | A first: 3! = 6; A first and D last: 2 (enumerated). Line now "You sent A first every time, which leaves $3! = 6$ orders. ..." Also the `all` line said "removes those that send D first" (D in position 1 is 6 orders, not 12): now "send D before A". |
| 4 | fixed differently | `<=` passes all 7 tests (part C control, kept as a control). Tests unchanged, inbox bullet left. A square-grid submission (`cols = rows`) passes tests 1 to 5 and first fails test 6 with 0, so the line now names that: "Test 6 is the first grid that is not square: one row of two cells. Take the row count from `len(pnl)` and the column count from `len(pnl[0])`. Only −51 counts, so the answer is 1." |
| 5 | fixed | Traced reverse-sorted pushes on the screen's graph: D is pushed by A and by C; G once, by E. Hint text and highlight now D. |
| 6a to 6l | fixed (6h fixed differently) | All 12 lines re-run with my own submissions; each diagnosis now sits on the test its mistake fails first, and each later line describes its own test. 6h: a hop-limited Dijkstra keeping one cost per currency passes test 1 and first fails test 2 with 2.9 (USD's 1.1 bp two-step cost blocks its 1.2 bp one-step), so the test-2 line names that cause as well as the description. 6k: I also added `test-2`, since a counter that outlives the call fails test 2 with (1, 2). |
| 7 | fixed | A no-`seen` DFS on A–B stored both ways recurses for ever; on parent-to-child arrows it returns. Auditor's sentence used. |
| 8 | fixed | Ran the colleague's code: B 4 (true 3), D 6 (true 4), F 9 (true 7). Sentence now names all three; the explain highlight gains D to match. |
| 9 | fixed | The taught code without the stale check passes tests 1 to 8 (part D `no stale check` first fails 9 only), so the overwrite happens only with record-on-pop. Auditor's sentence used. |
| 10 | fixed | Pascal's rule adds count(i − 1, j) and count(i, j − 1); stairs adds ways(n − 1) and ways(n − 2). Shared idea: split by the last move. Auditor's sentence used. |
| 11 | fixed differently | The appends are O(E) and the empty lists O(V); a self-loop is stored once, so "2E entries" needs no self-loops; sorting costs extra. New text: "... The empty lists and the appends take $O(V + E)$ time, and without self-loops the lists hold $2E$ entries. Sorting adds a little more, and is only there to make the output fixed." |

### Sweep of every `test-N` line (L1 to L3)

138 lines on 38 code widgets after the fix (129 before, 9 added). For each line that names a cause, a submission with that cause passes tests 1 to N − 1 and first fails test N (part D, 121 runs, 3 of them controls that must pass every test). For each line that names no cause, its stated facts were checked against the test and the solution (35 lines). Beyond finding 6, the sweep changed:

- `l11-dead-ends` screens[8]: added `test-9` (checking `i == len(xs)` before `total == target` first fails test 9, since both subsets that make 13 use 8, the last number after sorting); `test-5` said "Tests 5", now "Test 5". `test-10` and `test-13` hold: an empty-list special case first fails test 10; the unpruned walk takes 7.06 s on test 13 in Pyodide (limit 5 s).
- `l13-climbing-stairs` screens[9]: `test-6` said "hit the recursion limit or the clock", but plain recursion runs out of time on test 5 (`stairs(90)`), so the clock half could never show at test 6. Added `test-5` for plain recursion; `test-6` now names a recursion 5,000 calls deep (a memoised recursion first fails test 6 with `RecursionError`).
- Checked and left: l8 screens[5] test-9 (a plain loop `find` takes 0.75 s in Pyodide, so `False` in the last place; a recursive `find` raises `RecursionError`); hw2 items[8] test-5 (true for the version that expands a stale entry from `cost[u]`, which first fails test 5 with (7, 2)); hw2 items[8] test-11 (counting cheapest routes one by one passes test 10 and runs out of time on test 11).

Line by line (cause: first failing test; "describes": facts hold):

- `l1-nodes-and-edges#screens[5]`: test-1: stores each edge at one end: first fails 1 | test-2: describes its test, facts hold, keys from the edges only: first fails 2 | test-3: self-loop added at both ends: first fails 3.
- `l1-nodes-and-edges#screens[8]`: test-1: rows are one shared list: first fails 1 | test-5: describes its test, facts hold.
- `l1-nodes-and-edges#screens[9]`: test-3: checks only the arrows in: first fails 3 | test-4: checks only that it posts to nobody: first fails 4 | test-5: needs at least one poster: first fails 5.
- `l2-level-by-level#screens[4]`: test-1 (added): marks on pop: first fails 1 | test-3 (rewritten): describes its test, facts hold | test-4: describes its test, facts hold | test-7: recursive level search: first fails 7.
- `l2-level-by-level#screens[8]`: test-1: expands a firm at distance k: first fails 1 | test-3: describes its test, facts hold | test-5 (added): marks on pop, records a firm when queued: first fails 5 | test-7 (rewritten): describes its test, facts hold.
- `l3-going-deep#screens[2]`: test-1 (added): no seen check: first fails 1 | test-3: describes its test, facts hold | test-4 (rewritten): describes its test, facts hold.
- `l3-going-deep#screens[5]`: test-1 (rewritten): pushes in sorted order; no skip on pop: first fails 1 | test-3 (rewritten): describes its test, facts hold | test-6: recursive helper: first fails 6.
- `l3-going-deep#screens[8]`: test-2: counts only nodes with edges: first fails 2 | test-3: describes its test, facts hold | test-7: recursive search: first fails 7.
- `l3-going-deep#screens[9]`: test-2: plain seen set: first fails 2 | test-3: describes its test, facts hold | test-5: searches from the first rule only: first fails 5.
- `l4-islands#screens[2]`: test-1: adds diagonals; order left, right, up, down: first fails 1 | test-2: no bounds check: first fails 2.
- `l4-islands#screens[4]`: test-1 (added): eight neighbours: first fails 1 | test-2: no guard on the empty grid: first fails 2 | test-5 (rewritten): describes its test, facts hold | test-10: sinks the land: first fails 10 | test-11: describes its test, facts hold, control recursive flood fill: passes all.
- `l4-islands#screens[8]`: test-1: describes its test, facts hold | test-2: describes its test, facts hold | test-6 (rewritten): assumes a square grid: first fails 6, control non-strict <=: passes all.
- `l5-tasks-in-order#screens[3]`: test-1: plain queue: first fails 1 | test-3: no cycle check: first fails 3 | test-6: empty order read as a cycle: first fails 6.
- `l5-tasks-in-order#screens[8]`: test-1: raw inputs left out: first fails 1 | test-2: describes its test, facts hold | test-4: describes its test, facts hold.
- `review-1#items[7]`: test-2: treats the arrows as two-way: first fails 2 | test-4: checks the target only on discovery: first fails 4 | test-7: recursive search: first fails 7.
- `homework-1#items[0]`: test-3: describes its test, facts hold | test-4: describes its test, facts hold | test-6: describes its test, facts hold.
- `homework-1#items[1]`: test-2: spreads from the first firm only: first fails 2 | test-5: no check that every firm is reached: first fails 5 | test-8: describes its test, facts hold, control one search per defaulted firm: passes all.
- `homework-1#items[2]`: test-1: raw inputs not counted as a round: first fails 1 | test-3: describes its test, facts hold, empty input read as a cycle: first fails 3 | test-4: describes its test, facts hold, no cycle check: first fails 4 | test-7: cycle check only when nothing starts free: first fails 7.
- `homework-1#items[8]`: test-2: stores each conflict one way: first fails 2 | test-3: no clash check: first fails 3 | test-4: searches from the first desk only: first fails 4 | test-5: desks taken from the conflicts: first fails 5 | test-6: desks in the given order: first fails 6 | test-7: any placed neighbour but the parent is a clash: first fails 7 | test-8: places one conflict at a time: first fails 8 | test-9: checks clashes only in the first linked set: first fails 9 | test-10: recursive search: first fails 10.
- `l6-fewest-steps#screens[4]`: test-1: walk back not reversed; depth-first stack: first fails 1 | test-4: start equal to target gives no route: first fails 4 | test-5: no reach check: first fails 5.
- `l6-fewest-steps#screens[8]`: test-1 (rewritten): counts currencies; pairs stored a to b only; pairs stored b to a only: first fails 1 | test-3 (rewritten): describes its test, facts hold | test-7: adj[u] without a default: first fails 7.
- `l7-dijkstra#screens[4]`: test-1 (rewritten): marks seen when first pushed; dict of reached nodes only: first fails 1 | test-2 (rewritten): describes its test, facts hold | test-9: no stale check: first fails 9.
- `l7-dijkstra#screens[9]`: test-1: sums every cost: first fails 1 | test-4: max over the reached centres only: first fails 4 | test-8: centres taken from the links: first fails 8.
- `l8-groups#screens[5]`: test-5: count falls before the root check: first fails 5 | test-7: re-points the node, not its root: first fails 7 | test-9: recursive find, no union by size: first fails 9.
- `l8-groups#screens[9]`: test-1: compares rho, not abs(rho): first fails 1 | test-3: non-strict threshold: first fails 3 | test-7: groups by parent: first fails 7.
- `l9-arbitrage-cycle#screens[4]`: test-1: one pass only; n - 2 passes: first fails 1 | test-3: no detection pass: first fails 3 | test-6: describes its test, facts hold.
- `l9-arbitrage-cycle#screens[9]`: test-2: weights ln(rate); weights -rate: first fails 2 | test-4: no eps: first fails 4 | test-9: search from the first currency only: first fails 9.
- `homework-2#items[0]`: test-1: counts cells: first fails 1 | test-4: no check on the start cell: first fails 4.
- `homework-2#items[1]`: test-1 (rewritten): k rounds; relaxes in place, no copy: first fails 1 | test-2 (rewritten): Dijkstra keeping one cost per currency, with a hop limit: first fails 2 | test-7: describes its test, facts hold.
- `homework-2#items[2]`: test-1: merges only records that share directly with a group's first record: first fails 1 | test-4: describes its test, facts hold.
- `homework-2#items[8]`: test-1 (added): returns when dst is first reached: first fails 1 | test-2: a tie adds 1; a tie pushes the venue again: first fails 2 | test-3: a cheaper route keeps the old count: first fails 3 | test-4 (rewritten): describes its test, facts hold | test-5: no stale check, base cost[u]: first fails 5 | test-7: links stored both ways: first fails 7 | test-8: looks dst up in a cost dict of the linked venues: first fails 8 | test-11: counts the cheapest routes one by one: first fails 11.
- `l10-every-subset#screens[9]`: test-1 (rewritten): skip before take; stores path itself: first fails 1 | test-2: empty input gives no subsets: first fails 2 | test-5 (rewritten): describes its test, facts hold | test-7: empty input gives no orderings: first fails 7.
- `l11-dead-ends#screens[8]`: test-2: no undo after the call: first fails 2 | test-5 (rewritten): describes its test, facts hold | test-9 (added): end of list checked before the target: first fails 9 | test-10: empty list answered False: first fails 10 | test-13: unpruned walk: 7.06 s on test 13 in Pyodide (limit 5 s), passes in CPython; line holds.
- `l12-remembering#screens[9]`: test-1: base cases not counted: first fails 1 | test-2 (added): counter outlives the call: first fails 2 | test-3 (added): counts cache lookups; cache outlives the call; cache as a default argument: first fails 3 | test-4 (rewritten): describes its test, facts hold | test-6 (rewritten): describes its test, facts hold | test-12: grid not memoised: first fails 12.
- `l13-climbing-stairs#screens[9]`: test-1: ways(0) taken as 0: first fails 1 | test-5 (added): plain recursion runs out of time: first fails 5 | test-6 (rewritten): memoised recursion: first fails 6 | test-7: largest coin first: first fails 7 | test-8: amount 0 answered -1: first fails 8 | test-9: infinite entry returned: first fails 9.
- `homework-3#items[0]`: test-1: loop from 0: first fails 1 | test-3: not sorted: first fails 3 | test-5: target 0 gives no combination: first fails 5.
- `homework-3#items[1]`: test-2: describes its test, facts hold | test-5: empty string answered False: first fails 5 | test-8: no memo: first fails 8.
- `homework-3#items[8]`: test-2: one round trip only: first fails 2 | test-3: each rising run traded on its own: first fails 3 | test-4: table starts on day 1: first fails 4 | test-5: table stops before the last day: first fails 5 | test-6: describes its test, facts hold | test-7: reads prices[0] for the start: first fails 7.

### Sweep of every numeric slip with a feedback line (L1 to L3)

140 values on 75 items, each recomputed in part E from the mistake its line names (from the item's own data: graphs, grids, rates, code). After the fix all 140 hold. Changed: l8 screens[7] `edges` 3 → 2 (finding 1); the l11 `two` and homework-3 `fixed` and `all` lines (findings 2 and 3). No other slip value, key or tolerance changed, and no shown figure changed apart from the l7 explain highlight (finding 8). Values checked:

`l1-nodes-and-edges#screens[3]` edges 6, cells 36; `l1-nodes-and-edges#quiz[0]` once 7, sq 49; `l1-nodes-and-edges#quiz[2]` list 7000, edges2 6000; `l2-level-by-level#quiz[1]` centre 7, one 1; `l3-going-deep#quiz[1]` edges 2, nodes 6; `l3-going-deep#quiz[2]` edges 9; `l4-islands#screens[1]` diag 4, cells 14; `l4-islands#screens[3]` cells 1e+06, pairs 1e+12; `l4-islands#quiz[1]` diag 1; `l4-islands#quiz[3]` cells 6; `l5-tasks-in-order#screens[6]` all 7, none 0, five 5; `l5-tasks-in-order#quiz[0]` one 1, four 4; `l5-tasks-in-order#quiz[3]` all 4, out 1; `review-1#items[0]` once 15, plus 25, sq 100; `review-1#items[3]` diag 3, cells 10; `review-1#items[6]` all 7, four 4; `homework-1#items[4]` nobytes 0.4, linear 0.00016; `homework-1#items[5]` inside 1, sides 4; `l6-fewest-steps#screens[7]` hops 3, nodes 4; `l6-fewest-steps#quiz[3]` cells 7; `l7-dijkstra#screens[5]` right 3; `l7-dijkstra#screens[6]` pop 2; `l7-dijkstra#screens[8]` direct 400, usd 270, eurjpy 290; `l7-dijkstra#quiz[0]` right 3; `l7-dijkstra#quiz[3]` nodes 6; `l8-groups#screens[2]` one 6, self 7; `l8-groups#screens[7]` edges 2; `l8-groups#quiz[0]` pairs 2; `l8-groups#quiz[2]` direct 3; `l9-arbitrage-cycle#screens[1]` now 0.86; `l9-arbitrage-cycle#screens[2]` sign 0.004812, sum 3.05, prod 1.00482; `l9-arbitrage-cycle#screens[8]` gross 35.95, sign 264.03; `l9-arbitrage-cycle#quiz[0]` nodet 280, v 360; `l9-arbitrage-cycle#quiz[2]` inv 1.1905; `review-2#items[1]` sb 14, sat 11; `review-2#items[3]` sum 192.059; `review-2#items[4]` none 0; `review-2#items[5]` cycle 10, all-small 15; `review-2#items[6]` one 1, v 6; `homework-2#items[4]` sg 115.2, direct-sg 118; `homework-2#items[5]` gross 1796.51, onecost 1596.15; `l10-every-subset#screens[0]` no-empty 7, orders 6, one-each 3; `l10-every-subset#screens[3]` square 100, double 20, factorial 3.6288e+06; `l10-every-subset#screens[10]` no-cash 41, exactly-3 20, all 64, ordered 120; `l10-every-subset#screens[11]` hours 298, seconds 1.07374e+06; `l10-every-subset#quiz[1]` zero 0; `l10-every-subset#quiz[2]` pow 16, sum 10; `l10-every-subset#quiz[3]` leaves 8, inner 7; `l11-dead-ends#screens[2]` one 1, rows 4, orders 24; `l11-dead-ends#screens[5]` orders 6, no-reuse 1; `l11-dead-ends#quiz[0]` orders 6, one 1, two 2; `l11-dead-ends#quiz[1]` perm 40320, total 1.9174e+07; `l11-dead-ends#quiz[3]` orders 4, one 1; `l12-remembering#screens[1]` no-one 24, double 30; `l12-remembering#screens[4]` no-zero 30, lookups 59, naive 2.69254e+06; `l12-remembering#screens[5]` row 6, both 12; `l12-remembering#screens[8]` fresh 7, none 0; `l12-remembering#screens[10]` paths 1.07374e+09, square 961, last 31; `l12-remembering#quiz[0]` all 5000; `l12-remembering#quiz[2]` no-one 40; `l13-climbing-stairs#screens[0]` pow3 8, pow4 16, three 3; `l13-climbing-stairs#screens[4]` right 5, two 2; `l13-climbing-stairs#screens[6]` right 2, one 1; `l13-climbing-stairs#screens[10]` one-side 10, all 64; `l13-climbing-stairs#screens[11]` greedy 3; `l13-climbing-stairs#quiz[1]` greedy -1; `l13-climbing-stairs#quiz[2]` two-steps 8; `review-3#items[0]` no-empty 15, orders 24; `review-3#items[2]` col-only 3; `review-3#items[4]` no-one 66, memo 9; `review-3#items[6]` two 20; `review-3#items[7]` greedy 3; `homework-3#items[3]` all 24, fixed 6; `homework-3#items[4]` subsets 1.04858e+06, no-ends 2000, one-off 2100; `homework-3#items[5]` all 1024, half 512.

### Scripts and gates

- `docs/reports/graphs-dp-L1-3-r2-concepts.py`: 897 checks, exit 0 (was 320, 20 failing). The five part A checks that asserted the old content (l3 screens[3], l4 test 6, l7 screens[5], l11 `two`, homework-3 `fixed`) now assert the fixed content, each marked "fix pass"; the 12 part C submissions of finding 6 now point at the test their mistake fails first, and the `<=` submission for l4 test 6 is a control. Parts D and E were added. The l11 unpruned walk passes in CPython, so it is reported as info there and timed in Pyodide (7.06 s against 5 s).
- `docs/reports/graphs-dp-L1-3-concepts.py`: 231 checks, exit 0.
- `docs/reports/graphs-dp-1-perf-numbers.py`, `-2-`, `-3-`: exit 0. `-2-` checked the exact set of homework-2 items[8] `test-N` keys; it now allows the added `test-1`, which its own plant "returns on first reaching dst" first fails.
- Validator 0 errors (4,538 warnings); voice scan at 35: 0 over 35 words, 0 explanations over three sentences.
- Playthrough desktop and `--mobile` of the 13 edited files (11 lessons, homework-2, homework-3): 26 of 26 "All passed".

# Concept audit, round 3 (blind): graphs-dp levels 1 to 3

Scope: `l1` to `l13`, `review-1` to `review-3` and `homework-1` to `homework-3` in `app/content/courses/graphs-dp/` (Stage 1, topic 1.8, full ledger depth). Level 4 files are out of scope. This read was blind: no earlier review, audit, ledger, author report or concepts script for this course was opened before the ledger and findings below were committed (WIP commit named in the overlap section).

Ledger: `docs/reports/audit-graphs-dp-1-3-r3-ledger.md`, 426 rows: 417 correct, 7 imprecise, 2 unverified, 0 wrong, 0 misleading.
Script: `docs/reports/graphs-dp-L1-3-r3-concepts.py`, 340 checks, exit 0.

## Method

- Page facts confirmed in the engine: `app/js/engine/widgets/code.js` loads Pyodide 0.27.7 and sets `TEST_MS = 5000`; `app/js/screens/drill-worker.js` sets `RECURSION_LIMIT = 3000` and calls `sys.setrecursionlimit`. Tests of one widget share one namespace (prelude, learner code, postlude, then each test's setup and call), so module-level state survives between tests. The script copies that harness and sets the same recursion limit.
- All 38 code widgets: the solution passes every test and the starter fails (also `grade-all.mjs`, 0 failures on the six review and homework files).
- Every `test-N` feedback line that names a mistake was checked with a mutant holding that mistake: 97 mutant runs, each passing tests 1 to N-1 and failing test N, with the stated symptom where one is given (G twice, Oak twice, Hazel present, B at 4, `(300, 300)`, `(8, 11)`, `(8, 5)`, 2.9 bp, `(7, 2)` and so on). Lines that only restate a test were checked against the test.
- Every worked example was traced by running the lesson's own code on the lesson's own graph: BFS and DFS orders, queue and heap contents step by step, post-orders, Kahn's emissions, parent tables, Bellman-Ford passes, union-find parents, call counts, memo hits and DP tables.
- Algorithm conditions: BFS shortest paths are claimed only for unweighted graphs (l2, l6, with the weighted counter-example in l6 quiz 3). Dijkstra is tied to non-negative weights on every screen that states a guarantee or a bound (l7 screens 1, 3, 6, 7; homework-2 item 4). Topological order is tied to "no cycle" (l5 screens 0, 5, 7 and summary). Union-find costs are given as O(m alpha(n)) with both tricks, log2 n depth for union by size alone, and O(n^2) for the chain with neither. Greedy against DP (l13 screens 5, 11; review-3 item 8), safe against unsafe pruning (l11 screens 4, 6, 7, 9) and memoisation against tabulation (l12 against l13) are each stated with the hypothesis that makes them true.
- Recursion-limit sentences: each names either the default ("about 1,000 frames by default") or a depth of 3,000 to 5,001 that exceeds both the default and the page's 3,000. Each was run at both limits.
- Randomised cross-checks where a claim is general: stack DFS against recursive DFS (300 graphs), reversed post-order on random DAGs (200), Kruskal against brute force over spanning trees (200), at most E + 1 heap pushes (300 graphs), sorted subset-sum prune against brute force (500), coin table against BFS (300).

## Findings

No `wrong` and no `misleading` finding. Seven `imprecise`, all `minor`.

1. `l3-going-deep.json` | `screens[1].explain.text` | imprecise | minor | "From F the search steps back to D, C, G and E, each with nothing new. E still has H" says E has nothing new and then that it has H. | D (A, C, F), C (D, G) and G (C, E) have only visited neighbours; E still has H (script: dead ends are F then H). | Replace the first two sentences with: "From F the search steps back through D, C and G, each with nothing new, and reaches E. E still has H, so the dive continues there."

2. `l4-islands.json` | `quiz[0].widget.options[2].why` | imprecise | minor | "That counts stocks with at least one partner" is not what the item's own matrix gives: cell (i, i) is 1 because a stock's correlation with itself is 1, above 0.8, so every row holds a 1. | Definition in the item's prose; corr(X, X) = 1. | Replace with: "Every row holds a 1 on its diagonal, since a stock has correlation 1 with itself. So that counts all 50 stocks, not the clusters."

3. `l4-islands.json` | `quiz[2].widget.options[2].why` | imprecise | minor | "Then the search steps back and forth between two land cells forever, and the outer loop counts each island again." A search that never ends never returns to the outer loop, so the two halves cannot both happen. | With no marks, a stack search on two joined cells pushes each from the other without end; a one-cell island is counted once, correctly. | Replace with: "Then, on any island of two or more cells, the search steps back and forth between neighbours for ever."

4. `l5-tasks-in-order.json` | `screens[5].feedback.byKey.prices` | imprecise | minor | "prices is tried last by the outer loop" is not what `sorted(adj)` does: the loop tries backtest, calendar, prices, report, returns, risk, signals, so prices is third. It is the last task visited. | Script runs the screen's code: post-order ends with prices; the four names after it are already seen. | Replace with: "prices is the last task to be visited. Its only arrow leads to returns, already done, so it is appended at once."

5. `l6-fewest-steps.json` | `screens[1].prose` | imprecise | minor | "The badges show the visiting order so far" contradicts the labels A·0, B·1, E·1 and the caption, which give hops from A. Visiting order would be 0, 1, 2. | Canvas labels and caption on the same screen. | Replace the sentence with: "The labels show each visited node's number of hops from A."

6. `l11-dead-ends.json` | `quiz[0].widget.accept` | imprecise | minor | "0: every queen in row 1 leaves row 3 with nothing safe." For the middle queen it is row 2 that has nothing safe; r3c1 and r3c3 are not attacked by it. The item's own explain has it right. | Script: `safe3([(1, 2)], 2) == []`, `safe3([(1, 2)], 3) == [1, 3]`; corner queen leaves r2c3 only, whose queen attacks all of row 3. | Replace with: "0: a middle queen in row 1 leaves row 2 with nothing safe, and a corner queen leaves row 3 with nothing safe."

7. `l1-nodes-and-edges.json` | `quiz[1].explain.text` | imprecise | minor | "A dict of sets would also give $O(1)$ checks with less space" drops two conditions: set membership is O(1) on average, not in the worst case, and the space saving needs a sparse graph. | Python wiki, TimeComplexity (`x in s`: average O(1), worst O(n)); a set entry costs more than a matrix cell, so a dense graph is not smaller. | Replace the sentence with: "A dict of sets would also give $O(1)$ checks on average, and takes less space when the graph is sparse."

## Unverified (not passes, not findings of error)

- `l1-nodes-and-edges.json` | `screens[7].prose` and `summary.formula.note` | "Most real graphs are **sparse**" is an unsourced empirical generalisation. Suggested wording, which is a definition and needs no source: prose "A graph is **sparse** when $E$ is far below $V^2$, as in the trading networks of this course."; note "On a sparse graph the list wins."
- `l9-arbitrage-cycle.json` | `screens[8].explain.text` | "Mispricings between liquid quotes are this small, so triangular arbitrage rarely survives costs" is an unsourced claim about markets. It agrees with Akram, Rime and Sarno (2008), "Arbitrage in the foreign exchange market", Journal of International Economics 76, but the content cites nothing. Suggested conditional wording, true of the screen's numbers (0.36 bp gross against 3 bp of costs): "When mispricings between liquid quotes are this small, triangular arbitrage does not survive costs."

## Gates

- `node tools/validate.mjs`: 0 errors.
- `docs/reports/graphs-dp-1-perf-numbers.py`, `graphs-dp-2-perf-numbers.py`, `graphs-dp-3-perf-numbers.py`: exit 0, 0, 0 (run, not read, before the WIP commit).
- `docs/reports/graphs-dp-L1-3-r3-concepts.py`: exit 0, 340 checks.
- `node tools/grade-all.mjs --file` on `review-1`, `review-2`, `review-3`, `homework-1`, `homework-2`, `homework-3`: 0 failures each.

## Limits

- The script runs in CPython 3.12, not in Pyodide. Semantics checked here (recursion limit, float results of `math.log`, dict and list behaviour) are the same in Pyodide 0.27.7, which is CPython 3.12.7; speed is not, so the two timing claims (l8 test 9 under half a second, l11 test 13 over the limit) rest on CPython timings scaled by the engine's "several times slower", and on the course's own perf-numbers scripts.
- `order` widgets' `feedback.byKey` lines (keyed by a line id) were read as statements about that line's place in the right answer. The engine rule that picks which key shows was not traced.
- Same model family as the authors and earlier readers; shared misconceptions can survive.

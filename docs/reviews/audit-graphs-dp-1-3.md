# Concept audit: graphs-dp L1 to L3 (round 1, blind)

Auditor: Fable, 13 Nov 2026, branch `claude/fable-audit`. Scope: `app/content/courses/graphs-dp/` l1 to l13, review-1 to review-3, homework-1 to homework-3 (Stage 1, topic 1.8, full ledger depth). Level 4 (l14 to l17, review-4, homework-4) is out of scope. Blind rule kept: `docs/reviews/review-1.8.md`, `docs/reviews/voice-1.8-graphs-dp.txt`, the dsa and triage files and the graphs-dp, dsa and 1.8 reports were opened only after the ledger and the findings below were committed (WIP commit named in the hand-back). The three perf number scripts were run but not opened before then.

- Ledger: `docs/reports/audit-graphs-dp-1-3-ledger.md`, 430 rows: correct 396, wrong 7, imprecise 9, misleading 9, unverified 9.
- Script: `docs/reports/graphs-dp-L1-3-concepts.py`, 223 checks. It exits 1 at present: 207 pass and 16 fail, and each failing check tests a sentence named in a finding below (the finding number is printed). No check fails for any other reason.
- Code: all 38 Python code widgets were run under CPython 3.13 with the recursion limit at 1000. Every solution passes every hidden test and example, and no starter does. Pyodide 0.27.7 (local build, Python 3.12.7) confirms the recursion limit of 1000, the float sum −5.55 × 10⁻¹⁷ of l9 screen 6, the `RecursionError` on a 5,000 chain, and the 6.8 s of finding 18. There is no C++ in scope.

Findings: 18 (wrong 7, imprecise 7, misleading 4); serious 1, minor 17. Nine further rows are `unverified` (U1 to U9). No graded key, `wrong[]` value or slip was found incorrect.

## Findings

1. `l7-dijkstra.json` | `screens[5].explain.text` | **wrong, minor** | "The fix is one line after the pop: `if u in dist: continue`, or `if d > dist[u]: continue`." The second line does not fix this code. The colleague's version starts with `dist = {}`, so `dist[u]` raises `KeyError: 'A'` on the first pop. The stale test works only in the lesson's own version, where every cost starts at `math.inf`. | Evidence: script (`fix(D7, "A", 2)` raises; fix 1 returns the right costs). | Fix: "Every stale entry still pops, and the last one wins. Here B ends at 4 and F at 9, both wrong. The fix is one line after the pop: `if u in dist: continue`."

2. `l6-fewest-steps.json` | `screens[1].feedback.byKey.with-d` | **wrong, minor** | "D is two hops from C, which makes it three hops from A." The graph has the edge C–D, so D is one hop from C. It is C that is two hops from A. | Evidence: script (BFS from C gives D at 1; BFS from A gives C at 2). | Fix: "D is one hop from C, and C is two hops from A. So D is three hops from A, in the next ring."

3. `l3-going-deep.json` | `quiz[3].widget.options[2].why` (id `rev`) | **wrong, minor** | The option R, T, S, U is explained as "That reverses the pre-order." The pre-order is R, S, U, T, whose reverse is T, U, S, R. R, T, S, U is the post-order U, S, T, R reversed. The slip matters because lesson 5 builds on reversed post-order. | Evidence: script (`l3 q-post`). | Fix: "That reverses the post-order. A node finishes after its children, so R comes last, not first."

4. `l7-dijkstra.json` | `screens[4].explain.text` | **wrong, minor** | "Test 9 had 300 of them" (stale entries). The hub `h` is pushed 300 times, at costs 599 down to 300. One of those entries is the live one, so 299 are stale. | Evidence: script (300 pushes of `h`, 299 stale pops). | Fix: "Test 9 had 299 of them."

5. `l7-dijkstra.json` | `screens[6].prose`, `screens[6].feedback.byKey.pop`, `screens[6].explain.text`; `homework-2.json` | `items[6].widget.options[1].why` | **imprecise, minor** | The screen says Dijkstra "treats a popped node as final" and that 2 is "the cost Dijkstra fixed". That is the textbook algorithm (CLRS 24.3). The `dijkstra` the learner wrote two screens earlier has no settled set: on this graph it pushes B again at 1 and returns the right answer. A learner who runs their own code sees no failure and may doubt the rule. Homework 2 item 6 has the same gap: with negative edges and no negative cycle, the course's code returns correct costs, only without its speed bound. The graded keys are right under the standard convention. | Evidence: script (`dijkstra(neg, 'A')['B'] == 1`; the lazy code agrees with Bellman-Ford on 300 random negative-weight DAGs). Basis: CLRS 24.3 for the textbook claim. | Fix for `screens[6].explain.text`: "A negative arrow can lower a cost after its node is popped, so a popped node is no longer final. Our heap code would push B again at 1 here, but then a node's edges can be read more than once and the running-time bound is lost. If a loop's costs sum below zero, no cheapest cost exists; this level's last lesson deals with that." Fix for the homework why: "A negative edge can lower a cost after its node is popped, so Dijkstra's guarantee and its running time are lost."

6. `l5-tasks-in-order.json` | `screens[4].title`, `screens[4].explain.text`, `summary.trap`; `homework-1.json` | `items[7].model` part (e) | **misleading, serious** | The trap is framed as "Starting in the wrong place". The explain offers "Either start from in-degree 0 (Kahn), or use post-order", the summary trap lists "starting from a task that still has arrows in" as a cause, and the homework model says "Starting from a job with in-degree above 0 does the same". A learner takes away that recording on arrival is fine when the search starts at a free task. It is not: pre-order from `calendar`, which has in-degree 0, gives calendar, returns, risk, backtest, report, signals, with backtest before its input signals. The fault is emitting on arrival, wherever the search starts. | Evidence: script (`l5 s4 trap`). Basis: CLRS 22.4 (only finishing times give a topological order). | Fix: title "Recording too early". Explain: "The full result is backtest, report, calendar, returns, risk, signals, prices: backtest runs first, before its inputs. Starting at a free task does not cure it: pre-order from calendar still emits backtest before signals. Use in-degrees (Kahn's algorithm), or record on finishing, next." Summary trap: "Emitting a task on arrival runs it before its prerequisites, wherever the search starts." Homework model (e), second sentence: "That holds even when the search starts from a job with in-degree 0."

7. `l7-dijkstra.json` | `screens[8].prose` | **wrong, minor** | "At these sizes the costs add up along a route, to within a penny." Adding 0.5 + 0.6 + 1.5 bp gives £260.00; compounding gives £259.98, as the same screen's explain says. The gap is 1.95 pence. | Evidence: script. | Fix: "At these sizes the costs add up along a route, to within a few pence."

8. `l13-climbing-stairs.json` | `screens[6].prose` (code comment `# top down`) | **misleading, minor** | The failing loop, which fills the table from the largest amount first, is labelled "top down". Lesson 12 screen 2 gave that name to memoisation ("It is top-down dynamic programming"), which is a correct method for this very problem. A learner can leave with "top-down fails for coins". | Evidence: script (a top-down, memoised solution returns 2 for amount 6). Basis: CLRS 15.3 uses "top-down" for memoisation. | Fix: change the comment to `# largest amount first`. The prose line "from the top amount down" can stay.

9. `l1-nodes-and-edges.json` | `screens[3].explain.text` | **imprecise, minor** | "So an undirected graph's matrix is symmetric, with $2E$ ones." A self-loop adds one 1, not two. The lesson allows self-loops two screens later, and its own hidden test `adj_matrix(2, [(1, 1)])` expects a single 1 for one edge. | Evidence: script. | Fix: "So an undirected graph's matrix is symmetric, with $2E$ ones when no node is joined to itself."

10. `l2-level-by-level.json` | `screens[4].feedback.byKey.test-7`; `l4-islands.json` | `screens[4].feedback.byKey.test-11`; `homework-1.json` | `items[1].feedback.byKey.test-8` | **misleading, minor** | Three feedback lines name a slow method that their test cannot catch. (a) "If it timed out, use `deque.popleft()` rather than `list.pop(0)`": on a path the queue never holds more than one node, so `pop(0)` passes in under a millisecond. (b) "If it timed out, mark a cell when you push it": marking on pop with a skip makes at most 4 pushes per cell on the 20 by 20 grid. (c) "One BFS per defaulted firm is too slow": two sources on 2,000 firms is 4,000 pops. A learner whose code fails these tests for another reason is sent to the wrong fix. | Evidence: script (`l2 s4 test 7`, `l4 s4 test 11`). | Fix (a): "Test 7 is a path of 3,000 nodes. A search that calls itself once per node runs out of frames; use the queue loop." Fix (b): "Test 11 is a 20 by 20 island of 400 cells. The answer is 1." Fix (c): "Test 8 is a 2,000-firm chain with defaults at both ends. The last firms fall on day 999, so seed both ends in one queue."

11. `l5-tasks-in-order.json` | `screens[5].explain.text`, `screens[7].prose` | **imprecise, minor** | "That is a valid order, from any starting point" and "Reversed DFS post-order gives an order too, at the same cost" hold only on a graph with no cycle. With the loop of screen 6 added, reversed post-order still returns all seven tasks, in an invalid order, with no warning. Kahn's algorithm returns `None`. | Evidence: script. Basis: CLRS theorem 22.12 is stated for a DAG. | Fix for screen 5: "On a graph with no cycle that is a valid order, from any starting point." Fix for screen 7: "On a DAG, reversed DFS post-order gives an order too, at the same cost; it needs the three-state check to notice a cycle."

12. `l3-going-deep.json` | `quiz[2].explain.text` | **imprecise, minor** | "That is also how DFS tests whether an undirected graph is a tree." No edge to a visited non-parent node shows only that the part reached has no cycle. A forest of two pieces passes that test from any start and is not a tree. | Evidence: script. Basis: CLRS theorem B.2 (a tree is connected and acyclic). | Fix: "A connected undirected graph with no such edge is a tree, which is how DFS tests for one."

13. `l1-nodes-and-edges.json` | `screens[9].feedback.byKey.test-4` | **wrong, minor** | "In test 4 firm 2 posts to nobody, but nobody needs to post to it." The requirement runs the other way: every other firm must post to a counterparty. In the test nobody posts to firm 2. | Evidence: script (in-degree of firm 2 is 0 in `find_ccp(4, [(0, 3), (1, 3)])`). | Fix: "In test 4 firm 2 posts to nobody, but nobody posts to it either. Check `into == n - 1`."

14. `l11-dead-ends.json` | `screens[2].hints[1].text` | **imprecise, minor** | "A queen in a corner of row 1 leads to a dead end by row 3." From r1c1 the branch r2c4 places r3c2 and only then fails, in row 4. The same screen's explain says "row 3 or row 4". | Evidence: script. | Fix: "A queen in a corner of row 1 leads to a dead end in row 3 or row 4."

15. `homework-3.json` | `items[5].feedback.byKey.half` | **wrong, minor** | "Half of all paths do not return: most end above or below." Read as written it says exactly half fail to return. 772 of the 1,024 paths, about 75%, do not. | Evidence: script. | Fix: "Far fewer than half the paths return: 252 of 1,024. Most end above or below the start."

16. `homework-3.json` | `items[7].prompt` | **misleading, minor** | "It never finishes." The script builds 2²⁵ subsets, about 33.6 million. Building and filtering them takes seconds in CPython. Lesson 10 screen 11 needed a cost of 1 ms per subset to turn 2³⁰ into days, and this prompt gives no cost. The premise teaches a wrong sense of scale for 2²⁵. | Evidence: script (about 13 million subsets a second on the audit machine; a few seconds in all). | Fix: replace "It never finishes." with "Each basket needs a 1 millisecond risk check, so the full run would take over nine hours." (2²⁵ ms is 33,554 s, 9.3 hours.)

17. `l2-level-by-level.json` | `quiz[2].widget.options[1].why` | **imprecise, minor** | "The cheapest chain needs the rates as weights: Dijkstra, in level 2." Rates multiply along a chain. Lesson 9 shows that rate weights need `-ln(rate)`, which can be negative, and so Bellman-Ford; its quiz 3 marks "Dijkstra on those weights" wrong. Dijkstra takes additive, non-negative costs, as in lesson 7 screen 8. | Basis: l9 screens 2 and 5, l9 quiz 3; CLRS 24.3. | Fix: "BFS counts edges, not costs. The cheapest chain needs each trade's cost as a weight: Dijkstra, in level 2."

18. `l11-dead-ends.json` | `screens[8].widget.how` | **imprecise, minor** | "Without pruning, it takes far longer than the 5-second limit." The unpruned walk on the 25 even numbers makes 2²⁶ − 1 calls. In the local Pyodide 0.27.7 build that takes 6.8 s, about 1.4 times the limit, not far longer. On a faster machine an unpruned solution may pass. | Evidence: Pyodide run (ledger header). | Fix: "Without pruning it makes about 67 million calls, several seconds of work." An inbox bullet asks for a wider margin.

## Unverified rows (not counted as findings)

Empirical or framing remarks with no source. None is graded. Suggested wording removes the unsourced claim.

- U1 `l2` `screens[8].prose` (firms within k links "face losses first"), U5 `l6` `screens[7].prose` (each hop "adds a day of delay"), U7 `l8` `quiz[0].prose` (a connected group "can be netted to a single settlement"), U2 `l4` `screens[8].prose` ("separate regions mean separate ways to lose"): story premises. No change needed.
- U3 `l4-islands.json` `screens[8].explain.text`: "The count tells risk whether one hedge can cover the losses." One long strangle covers both loss corners of a short straddle. Suggested: "The count tells risk how many separate loss scenarios the book has at that limit."
- U4 `homework-1.json` `items[4].explain.text`: "Bonds share an issuer with few others, so an adjacency list of a few megabytes does the same job." Suggested: "If each bond shares its issuer with about 20 others, the adjacency list holds 400,000 entries, about 3 MB of pointers." (20,000 × 20 × 8 bytes is 3.2 MB.)
- U6 `l6-fewest-steps.json` `screens[8].explain.text`: "a route with fewer hops usually costs less". Illiquid crosses are often cheaper through the dollar, and quiz 2 of the same lesson is a counter-example. Suggested second sentence: "Each conversion pays a spread, so fewer hops is a sensible first target."
- U8 `homework-2.json` `items[5].explain.text`: "would close within milliseconds". Fenn et al. (2009) support "short-lived", not the timescale. Suggested: "A gap this wide between liquid quotes would not last."
- U9 `homework-2.json` `items[7].model` part (e): mispricings "are a fraction of a basis point". Suggested: "so mispricings are small and short-lived".

## Checks the brief asks for, and what they found

- BFS shortest paths only on unweighted graphs: stated wherever used (l2 screen 7, l6 screens 6 and 8, l6 quiz 2, l7 screen 7). The one loose line is finding 17.
- Dijkstra only with non-negative weights: stated in l7 screens 1, 6 and 7, the summary, l9 quiz 3 and homework 2 items 3 and 6. The proof order in homework 2 item 3 is sound (CLRS theorem 24.6). The gap between the rule and the taught lazy code is finding 5.
- Topological order only on a DAG: Kahn's cycle test is right and proved (l5 screen 7). The DAG condition is missing for reversed post-order (finding 11), and pre-order is misdiagnosed (finding 6).
- Bellman-Ford: V − 1 passes, the extra pass, the unreachable-cycle case, the zero cycle and the tolerance are all correct (l9 screens 3, 4, 6 and 9).
- Greedy against DP and optimal substructure: the coin examples (1, 3, 4 for 6; 2, 5 for 11; 1, 5, 6, 9 for 11; lots for 1,100) all make greedy fail as claimed, and the recurrences are right. Kruskal's greedy rule is checked against every spanning tree of the review graph.
- Pruning safety: every "safe" prune is monotone and every "unsafe" one has a working counter-example (l11 screens 4, 6, 7 and 9; review-3 item 3; homework-3 item 7).
- Big-O against case and representation: list against matrix for space and BFS (l1 screen 7, l6 quiz 0), heap against scan for Dijkstra (l7 screen 3), Kahn with a heap (l5 screen 3), union-find with both heuristics (l8 screen 5), memoised counts (l12, homework-3). All correct as stated.
- Feedback against slips: every `wrong[]` value and `byKey` line was recomputed from the mistake it names. Findings 2, 3, 10, 13 and 15 are the lines that do not match.
- Counting shortest routes (homework 2 item 8) needs fees of at least 1; the prose states it and the explain uses it. The solution equals a brute-force count on 200 random maps.

## Gates

- `node tools/validate.mjs`: 0 errors, 4,531 warnings (whole app); `content/manifest.json` unchanged.
- Number scripts: the course has no `graphs-dp-L*-numbers.py`. `docs/reports/graphs-dp-1-perf-numbers.py`, `-2-` and `-3-` exit 0.
- `node tools/grade-all.mjs --file` on review-1, review-2, review-3, homework-1, homework-2, homework-3: 0 failures each (6, 8, 9, 3, 3 and 4 widgets). It checks numeric, choice and multi widgets only; the code, order and longform items were covered by the concepts script and by hand.
- `python3 docs/reports/graphs-dp-L1-3-concepts.py`: exit 1, 207 pass, 16 fail, as described above.
- No playthrough was run: no content was changed.

## Overlap with the earlier read

Read after the WIP commit: `docs/reviews/review-1.8.md` (second read of algo-think, ds and graphs-dp together, with its fix pass). For graphs-dp L1 to L3 it lists only style items: three explains over three sentences (`l1` screens[8], `l3` screens[2], `review-1` items[3]) and sentences over 20 words. Its grading, test-strength and explanation sections name no graphs-dp L1 to L3 item, so it has no conceptual finding in this scope.

| | count |
|---|---|
| Conceptual findings by this audit only | 18 |
| By the earlier review only | 0 |
| By both | 0 |

New `wrong` findings that no earlier read found: 7 (findings 1, 2, 3, 4, 7, 13 and 15), all minor. None changes a graded key.

Two notes on the earlier read. It states that unpruned searches time out in graphs-dp l11; finding 18 measures that margin at about 1.4 times the limit. Its fix pass shortened the `l1` screens[8] and `l3` screens[2] explains; both shortened texts were read here as ledger rows and are correct.

By the convergence rule (at most one new `wrong` per three levels) this course does not close on round 1: there are seven new `wrong` rows across three levels.

## Fix pass

Fixer: Opus, 13 Nov 2026. Every basis below is my own run (CPython 3.13, recursion limit 1000) or derivation; the auditor's text was used only where my run agreed. No graded key, tolerance, `wrong[]` value or slip value changed. No test, size or time limit changed: test design and the engine are out of scope, so the inbox bullet on the l11 test 13 margin stays open.

1. fixed. Colleague's code with `if d > dist[u]` raises `KeyError: 'A'` on the first pop (`dist = {}`); with `if u in dist` it returns B 3, F 7; unfixed it gives B 4, F 9.
2. fixed. BFS on the l6 graph: D is 1 from C, C is 2 from A, D is 3 from A.
3. fixed. Tree R(S(U), T): pre R, S, U, T; post U, S, T, R; R, T, S, U is the reversed post-order.
4. fixed. Simulated `hub_scans(300)` with the lesson's code: h pushed 300 times, 299 stale pops (no other stale pops).
5. fixed differently. The lesson's code returns B = 1 and pops B twice on the canvas graph; prose now says "Textbook Dijkstra", the `pop` feedback says 2 is B's cost when first popped (still the slip the value 2 names), and the explain says our heap code pushes B again at 1 but nodes can be popped many times and the speed bound is lost. Homework 2 why: guarantee and speed bound lost.
6. fixed differently (serious). My counter-example: pre-order from calendar (in-degree 0) gives calendar, returns, risk, backtest, report, signals, prices, so backtest precedes signals; from prices it also fails; the minimal case a→b, a→c, c→b from a gives a, b, c. Title "Recording too early"; the explain names the calendar case and the cure in the lesson's edge direction (`adj` maps a task to the tasks that need it): record a task when its call finishes, after every task that needs it, then reverse, or use Kahn. Summary trap: "Emitting a task when DFS first reaches it can put it before its prerequisites, wherever the search starts." Homework 1 (e) in its own direction (A → B when B needs A). Reversed post-order checked valid from every start order.
7. fixed. 10⁶ × (1 − 0.99995 × 0.99994 × 0.99985) = £259.9805; 260 − 259.98 is 1.95p.
8. fixed. Comment now `# largest amount first`; the loop still gives [0, 1, inf, 1, 1, inf, inf].
9. fixed. The lesson's `adj_matrix(2, [(1, 1)])` sets one cell.
10. fixed differently. (a) A self-calling search on the 3,000 path raises `RecursionError` at the limit of 1,000; `list.pop(0)` passes in 0.9 ms, so the new line names the recursion limit. (b) auditor's text. (c) chain 0 to 1,999 seeded at both ends: firms 999 and 1000 fall on day 999; new line says the waves meet in the middle. Test sizes and limits unchanged (out of scope).
11. fixed. Reversed post-order on the cyclic pipeline returns all 7 tasks, risk before backtest, with no warning; screen 7 now points to lesson 3's three-state check. Same DAG condition added to summary idea 3.
12. fixed differently. A two-piece forest meets no back edge from node 0 and is not a tree; text now: DFS "must meet no such edge and reach every node".
13. fixed. In test 4 firm 2 has in-degree 0 and out-degree 0.
14. fixed. From r1c1: r2c3 dies in row 3, r2c4 reaches r3c2 and dies in row 4.
15. fixed differently. Slip value is 512 (half of 1,024); feedback now names 512 and states 252 of 1,024 return (C(10, 5)).
16. fixed differently. Premise is a stated condition: "Each subset also goes through a 1 millisecond risk check, so the run would take over nine hours" (2²⁵ ms = 33,554 s = 9.32 h). Model and rubric unaffected.
17. fixed. l7 screen 8 uses additive bp costs with Dijkstra; l9 handles rates through −ln.
18. fixed differently. The unpruned walk makes 2²⁶ − 1 = 67,108,863 calls, 4.98 s in CPython here (audit: 6.8 s in Pyodide); text: "about 67 million calls, which takes several seconds". Test and limit unchanged.

Unverified rows, each treated as a finding:
- U1 fixed: stated as risk's rule ("Risk treats every firm at most `k` links away as first in line for losses").
- U2 fixed: now a consequence of the definition ("Each region is a separate group of losing scenarios").
- U3 fixed differently: "So the count depends on the limit as well as on the book" (tests: 2 regions at £50k, 1 at £10k).
- U4 fixed: stated condition; 20,000 × 20 = 400,000 entries × 8 bytes = 3.2 MB.
- U5 fixed: "Suppose each hop adds a day of delay ...".
- U6 fixed differently: "If every conversion paid the same spread, fewer hops would always cost less" (1 − (1 − s)ʰ rises with h).
- U7 fixed: "Suppose each group ... can be netted to a single settlement".
- U8 fixed differently: "If many desks watch these liquid quotes, a gap this wide would not last."
- U9 fixed differently: "If many arbitrageurs watch liquid quotes, mispricings stay small and short-lived." The worked example (loop 1.0000359, £36, about £300 of costs) recomputed and unchanged.

Concepts script: 16 failing checks now pass. Checks for findings 5, 9, 10, 12, 14 and 16 tested code facts that a text fix cannot change, so each now also accepts the corrected sentence; four checks were added (recursion fails test 7, rev option is reversed post-order, l5 trap wording and counter-example, hw3 slip 512 and 252). 227 pass, 0 fail.

Gates: validator 0 errors (4,534 warnings, manifest unchanged); concepts script and the three perf scripts exit 0; voice scan 35: 0 and 0; playthrough green desktop and `--mobile` for l1, l2, l3, l4, l5, l6, l7, l8, l11, l13 and homework 1 to 3; the five code widgets whose feedback or `how` changed: solution passes every hidden test, starter fails.

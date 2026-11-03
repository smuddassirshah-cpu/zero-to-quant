# Topic 1.8 (Data structures and algorithms): second-reader findings

Scope: every lesson, review and homework file in `app/content/courses/algo-think/` (l1 to l14, review-1 to review-3, homework-1 to homework-3), `app/content/courses/ds/` (l1 to l18, review-1 to review-4, homework-1 to homework-4) and `app/content/courses/graphs-dp/` (l1 to l17, review-1 to review-4, homework-1 to homework-4), and `app/content/exams/topic-1.8.json`.

Method. Every keyed number and choice was recomputed by hand or in Python: loop and pair counts, copy totals for doubling, tripling and fixed growth, recurrences (tree method and closed forms, including $T(4096)/T(1024) = 9.06$ for $3T(n/2) + n$), fast-power multiplication counts (12 for 252, 16 for 2,520, 41 for $10^9$), Black-Scholes bisection (0.2411), every BFS, DFS, Kahn, Dijkstra, Bellman-Ford and union-find trace, every heap sift, every knapsack, LCS, edit-distance and grid table, the dice and dealer stopping values (4.25, 4.6667, 4.9444, 99.6375, 99.7630), the secretary value 0.3987, the arbitrage loops (1.004824, $-264.03$, £1,195.55), FIFO and LIFO lot costs, and every exam item. Distractor values were re-derived from their `why`.
Code: each of the 133 Python code widgets (129 in the courses, 4 in the exam) was extracted and run in CPython against its hidden tests with a harness that mirrors `app/js/engine/widgets/code.js` (setup, prelude, postlude, `isclose`/`equal`/`raises`, the 5 s per-case limit plus `budget`). Every solution passes and every starter fails at least one test. Where a screen claims a complexity or space bound, a naive version was written and run (39 of them: pair loops, list scans, re-slicing windows, unmemoised recursion, unpruned search, `sorted()` shortcuts, sets of seen nodes, sweep relaxation). 28 are caught by a test. Ten are not, listed below; the eleventh, a `bisect.insort` running median for ds homework-4 items[2], is a fair answer there. Harness and naive files: the scratchpad folder `/tmp/claude-0/-home-user-zero-to-quant/f2cb57c1-0333-5a7c-8b45-5ff551a039e9/scratchpad/read-1.8` (`tools/runcode.py`, `naive/`, results in `code-results.txt`). Every proposed extra test below was run there too: the solution passes it and the naive version fails.
Playthrough with `--local-cdn`: all 49 lessons, all 22 reviews and homework sets and the exam pass. Desktop screenshots of every lesson screen were checked as contact sheets; `--mobile` (390 px) on algo-think l2, ds l7 and l18, graphs-dp l9, l14 and l16.
Style: a script scanned every string for exclamation marks, dashes, American spellings, money symbols, sentences over 20 words (a code or maths span counts as one word) and explanations over three sentences (`style.py` and `style.txt` in the same scratchpad folder).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, overstated claim, grading that accepts a wrong method or rejects a defensible answer, or a binding-rule breach; note = style. Screen, item and quiz numbers are zero-based.

All other stated numbers check. No exclamation marks (the one hit is $n!$ in a formula), no em-dashes, no American spellings outside the engine's `align: "center"` parameter, £ throughout (dollars appear only as currency names in FX screens). The exam has 28 items at 6/14/5/3 by difficulty 2/3/4/5 (the 8.4 ramp) and covers all 16 skills.

## Grading and keyed answers

- app/content/courses/ds/homework-3.json | items[2] (FIFO cost basis) | error | The plain average of the three lot prices times 350, $(50 + 52 + 49.5)/3 \times 350$, is exactly £17,675, the key. A learner who averages the prices, the method the `avg` byKey calls wrong, is marked right. The two wrong values do not match their byKeys either: true LIFO (300 at £49.50 plus 50 at £52) is £17,450, not 17,325, and the weighted average cost is £17,529.17, not 17,558.33. | Change the third lot to £49.00: prose "then 300 at £49.00"; `answer` 17650; `accept` "£17,650: $200 \times 50 + 100 \times 52 + 50 \times 49$"; `wrong` lifo 17300, avg 17441.67 (tol abs 1); explain "£10,000 for the first lot, £5,200 for the second, and $50 \times 49 = $ £2,450 from the third: £17,650. The queue keeps 250 shares at £49.00." The plain average is then £17,616.67, which no longer matches. Recomputed: FIFO 17,650, LIFO 17,300, weighted 17,441.67.
- app/content/courses/ds/homework-1.json | items[6] (10,000 cancels by `list.remove`) | warning | The key 250,000,000 assumes the list stays at 50,000 ids, but nothing says so: with no new orders it shrinks to 40,000 and the expected comparisons are 225,007,500, which `tol: { rel: 0.05 }` rejects. | Prose: add "New orders arrive as fast as old ones are cancelled, so the list stays at about 50,000 ids." Keep the key.
- app/content/courses/algo-think/homework-3.json | items[1] option `b` why | warning | "each coin is at least double the one below" reads as a rule that makes greedy safe. It is not: 1, 4, 9 has each coin at least double the one below, and greedy pays 12 as 9 + 1 + 1 + 1 against 4 + 4 + 4. | "Greedy is optimal for this system, as it is for UK coins. Try 6, 8 or 9: it is never beaten."
- app/content/courses/ds/l15-search-trees.json | quiz[3] option `c` why | note | "A dict ... keeps no order" is false in Python 3.7 on: dicts keep insertion order. | "A dict finds an exact price in $O(1)$ but does not keep keys sorted, so it cannot answer a range."

## Tests that do not catch the solution the screen rules out

Each line: a naive version that passes every hidden test, and an added test that the solution passes and the naive version fails (checked in CPython).

- app/content/courses/algo-think/review-3.json | items[6] `count_between` | warning | Asks for $O(\log n)$ per call, but `sum(1 for c in closes if low <= c <= high)` passes all 8 tests: the largest list has 8 closes. | Add the `Looks` class from `l9-halving.json` screens[3] to the prelude and a test `{ "setup": "big = Looks(range(0, 2000000, 2)); r = count_between(big, 1000, 2000)", "call": "(r, big.looks <= 100)", "expect": "(501, True)", "compare": "equal" }`; add it to `how` ("and a million closes with your reads counted").
- app/content/courses/ds/homework-3.json | items[0] `MinStack` | warning | Asks for $O(1)$ `get_min` "not by scanning", but `return min(self.xs)` passes: test 6 calls `get_min` once. | Add `{ "setup": "s6 = MinStack()\nfor v in range(200000, -1, -1): s6.push(v)", "call": "sum(s6.get_min() for _ in range(20000))", "expect": "0", "compare": "equal" }`; `how`: "Test 7 calls `get_min` 20,000 times on that stack."
- app/content/courses/ds/homework-3.json | items[4] `LRUCache` | warning | Asks for $O(1)$ operations, but a list of keys with `remove` and `pop(0)` passes in 0.06 s: test 7's cache holds only 1,000 keys. | Add `{ "call": "run(50000, [['put', i, i] for i in range(100000)] + [['get', i] for i in range(99999, 49999, -1)]) == list(range(99999, 49999, -1))", "expect": "True", "compare": "equal" }`.
- app/content/courses/ds/homework-3.json | items[5] `cycle_start` | warning | Asks for $O(1)$ extra space, but a set of seen node ids passes. | Add `peak_bytes` from `algo-think/l3-memory.json` screens[3] to the prelude and `{ "setup": "h = make_cycle(list(range(100000)), 77777)", "call": "peak_bytes(lambda: cycle_start(h)) < 50_000", "expect": "True", "compare": "equal" }`; `how`: "Test 10 checks your peak memory on 100,000 nodes."
- app/content/courses/ds/l13-fast-and-slow.json | screens[9] `has_loop` | warning | The question says "using $O(1)$ extra space" and the prose "without storing it", yet a set of seen rules passes. | Same `peak_bytes` prelude; `{ "setup": "fb = {**{i: i + 1 for i in range(100000)}, 100000: 50000}", "call": "peak_bytes(lambda: has_loop(fb, 0)) < 50_000", "expect": "True", "compare": "equal" }`.
- app/content/courses/ds/l13-fast-and-slow.json | screens[7] `has_cycle`, `middle` | note | The prose says honestly that a set would pass, which undercuts the screen's point. | Optional: the same `peak_bytes` test on `has_cycle(make_cycle(list(range(100000)), 50000))`, and drop "A set of seen nodes would pass the tests" from the prose.
- app/content/courses/ds/homework-4.json | items[1] `merge_k` | warning | The question says "using `heapq`" and the how "re-sorting everything ignores that each list is already sorted", but `sorted(x for l in lists for x in l)` passes all 8 tests in 0.02 s. | Add a postlude flag and test as `algo-think/homework-3.json` items[5] does: `{ "call": "'sorted(' not in __learner_source__ and '.sort(' not in __learner_source__", "expect": "True", "compare": "equal" }` (the solution uses neither); `how`: "and a check that you did not call `sorted` or `.sort`".
- app/content/courses/ds/l17-always-the-smallest.json | screens[9] `top_k` | warning | Asks for a heap of at most $k$ items, but `sorted(xs, reverse=True)[:k]` passes, iterator test included. | Add `peak_bytes` to the prelude and `{ "call": "peak_bytes(lambda: top_k(iter(range(200000)), 3)) < 50_000", "expect": "True", "compare": "equal" }`; `how`: "and a 200,000-value stream whose peak memory must stay small".
- app/content/courses/algo-think/l13-quicksort.json | screens[8] `quickselect` | note | A hand-written merge sort followed by `[k]` passes (0.3 s), since only `sorted` and `.sort` are banned. The lesson's point, $O(n)$ against $O(n \log n)$, is untested. | Either accept it and say in `how` "a hand-written full sort also passes, but costs $O(n \log n)$", or count comparisons with an `int` subclass in the prelude and require fewer than $10^6$ on the 100,001-value test (check the solution's count first).
- app/content/courses/algo-think/homework-3.json | items[6] `kth_largest` | note | Removing the maximum $k - 1$ times, $O(nk)$, passes in 1.8 s in CPython (likely 3 to 5 s in Pyodide), against the claimed $O(n)$ average. | Make test 9 ask for the 20,000th largest (`kth_largest(sizes, 20000)`; recompute the expected value from `sorted(sizes)[-20000]`), which pushes $O(nk)$ far past the limit.

All other complexity claims are enforced: pair loops time out (algo-think hw1, hw2, l12; ds l3, l5, l8, hw1, hw2, review-1), list scans time out (ds l2, l4), window re-slicing times out (ds l6, l11), quadratic next-greater and span scans time out (ds l10, hw3), unmemoised and unpruned searches time out or hit the recursion limit (graphs-dp l11, l12, l13, hw3, hw4), and in the exam a right-and-down DP fails `cheapest_route` tests 5 to 8 while a sweep-until-stable version times out on the snake grid.

## Explanations

- app/content/courses/algo-think/l13-quicksort.json | screens[0] explain | warning | "The two sides need not be sorted yet: only on the right side of 5." does not parse as a sentence and does not say what it means. | "Three values belong left, so the pivot ends at index 3. Neither side needs to be sorted yet; each value only has to be on the right side of 5."
- app/content/courses/ds/l7-prefix-sums.json | screens[8] explain | note | "each prefix value appears 10,000 times" is not quite right for `[1, -1] * 10000`: the prefix 0 appears 10,001 times (with `pre[0]`) and 1 appears 10,000 times, giving $\binom{10001}{2} + \binom{10000}{2} = 10^8$. | "The answer in test 13 is $10{,}000^2$: the prefix 0 appears 10,001 times and the prefix 1 appears 10,000 times."
- app/content/courses/algo-think/l3-memory.json | screens[4] explain | note | "here `getsizeof` reports roughly half": in a 32-bit build a pointer is 4 bytes and a float 16, so a list of floats is about 20 bytes a value, about 60% of 32. | "The Python in this page is a 32-bit build: about 20 bytes a float, not 32."

## Explanations over three sentences (binding limit)

- app/content/courses/algo-think/l1-counting-work.json | screens[2] explain | note | Four sentences. | "With one price, the inner loop is `range(1, 1)`, which is empty; with none, the outer loop never starts." Keep the other two.
- app/content/courses/algo-think/review-3.json | items[1] explain | note | Five sentences. | "Keys 3, 2 and 1 take one, two and three tests, each then reaching the left end. Key 5 takes one test against 4, which stops it. Total $1 + 2 + 3 + 1 = 7$."
- app/content/courses/ds/homework-1.json | items[5] explain | note | Four sentences. | Merge the last two: "Sorting first also works, in $O(n \log n)$, but walking from every number costs $O(n^2)$ on one long run."
- app/content/courses/ds/l10-next-greater.json | quiz[1] explain | note | Four sentences. | "6 and 4 are pushed; 5 pops 4, stops at 6, and is pushed. Then 2 is pushed. The stack falls from bottom to top: 6, 5, 2."
- app/content/courses/ds/l13-fast-and-slow.json | screens[3] explain | note | Four sentences. | Last two become "So once `slow` is in a cycle of length $L$, they meet within $L$ moves: $O(n)$ in all."
- app/content/courses/ds/l15-search-trees.json | screens[1] explain | note | Four sentences. | "65 > 50, 65 < 70 and 65 > 60 send it right, left, then right onto a `None`. So 65 becomes 60's right child: an insert always adds a leaf."
- app/content/courses/ds/l16-tree-recursion.json | screens[8] explain | note | Four sentences. | "Bottom up, −5 reports 3, so 3 reports 6, and −1 reports 3. The root takes 2 + max(3, 6) = 8. Choosing the best child step by step finds only 6."
- app/content/courses/ds/l16-tree-recursion.json | screens[9] explain | note | Four sentences. | "Base case: a leaf; recurse only into children that exist; combine the node with the better child. It runs in $O(n)$, and the same shape prices a binomial lattice backwards."
- app/content/courses/ds/review-4.json | items[3] explain | note | Four sentences. | "1 starts at index 5, and its parent at index 2 holds 4: swap. Its new parent, index 0, holds 3: swap, and 1 is the root."
- app/content/courses/graphs-dp/l1-nodes-and-edges.json | screens[8] explain | note | Four sentences. | "`[[0] * n] * n` repeats a reference to one row, so setting `m[0][1]` sets column 1 in every row." Keep the other two.
- app/content/courses/graphs-dp/l3-going-deep.json | screens[2] explain | note | Four sentences. | Last two become "So DFS is $O(V + E)$, like BFS; only the order differs."
- app/content/courses/graphs-dp/review-1.json | items[3] explain | note | Five sentences. | "Top left: r1c1, r1c2, r2c2; top right: r1c5, r2c4, r2c5. Bottom left: r3c1, r4c1, r4c2, and r4c4 alone. Corner contacts do not join."
- app/content/exams/topic-1.8.json | items[27] explain | note | Four sentences. | "Each job gets its own structure: dicts find, linked lists keep time order, and a heap or array keeps price order." Keep the other two.

## Sentences over 20 words

The script finds 250 sentences over 20 words (76 in algo-think, 75 in ds, 99 in graphs-dp, none in the exam); 185 are 21 to 24 words and are listed in `style.txt` in the scratchpad folder above. Most of the long ones are `how` lines that list the hidden tests after a colon.

- app/content/courses/algo-think (all files) | see list | note | 24 sentences of 25 words or more. | Split each `how` test list into two sentences ("Check runs 8 hidden tests. They include ..."), and split the others at the semicolon or colon.
- app/content/courses/ds (all files) | see list | note | 14 sentences of 25 words or more. | As above.
- app/content/courses/graphs-dp (all files) | see list | note | 27 sentences of 25 words or more. | As above.

Sentences of 25 words or more (word count in brackets):
- algo-think/homework-1: items[5] how (26)
- algo-think/homework-3: items[4] how (32), items[5] how (34), items[6] how (46), items[7] prompt (35)
- algo-think/l3-memory: screens[3] prose (25)
- algo-think/l4-cheap-on-average: screens[6] how (25)
- algo-think/l9-halving: screens[3] how (31), screens[5] how (35), screens[9] how (29)
- algo-think/l10-search-the-answer: screens[3] how (39), screens[5] how (28)
- algo-think/l11-sorting-by-hand: screens[3] how (30), screens[8] how (31)
- algo-think/l12-merge-sort: screens[7] how (33), screens[8] how (26), summary.trap (25)
- algo-think/l13-quicksort: screens[3] how (32), screens[4] how (27), screens[8] how (35)
- algo-think/l14-best-step-now: screens[3] how (37), screens[3] explain (26), screens[5] how (35)
- algo-think/review-3: items[4] how (31), items[6] how (33), items[7] how (33)
- ds/l2-constant-time-lookup: summary.ideas[0] (26)
- ds/l6-sliding-window: screens[8] prose (25), summary.ideas[1] (25)
- ds/l9-last-in-first-out: screens[10] question (26)
- ds/l11-first-in-first-out: screens[4] explain (27)
- ds/l13-fast-and-slow: screens[7] how (25)
- ds/l16-tree-recursion: screens[6] how (32)
- ds/l18-order-book-heaps: summary.ideas[1] (28)
- ds/review-2: items[8] prose (27)
- ds/homework-2: items[7].rubric[2] (26), items[7].rubric[5] (30)
- ds/homework-3: items[6] explain (25), items[7] prompt (26)
- ds/homework-4: items[2] prose (26), items[6] prompt (29)
- graphs-dp/l2-level-by-level: screens[4] how (25)
- graphs-dp/l4-islands: screens[4] how (33), summary.ideas[0] (26)
- graphs-dp/l5-tasks-in-order: screens[8] how (25)
- graphs-dp/l9-arbitrage-cycle: screens[9] prose (25)
- graphs-dp/l10-every-subset: screens[9] how (38)
- graphs-dp/l11-dead-ends: screens[8] how (25), quiz[1] prose (26)
- graphs-dp/l12-remembering: screens[2].hints[2] (27)
- graphs-dp/l13-climbing-stairs: summary.ideas[2] (26)
- graphs-dp/l14-knapsack: screens[6] how (38)
- graphs-dp/l15-common-subsequence: screens[9] prose (31)
- graphs-dp/l16-grid-paths: screens[5] prose (25), screens[6] how (36)
- graphs-dp/l17-dice-stopping: quiz[3] prose (25)
- graphs-dp/review-2: items[6] prose (26)
- graphs-dp/homework-1: items[0] how (26), items[1] how (32)
- graphs-dp/homework-2: items[4] prose (32)
- graphs-dp/homework-3: items[1] how (26), items[4] prose (40), items[5] prose (27), items[7] prompt (31)
- graphs-dp/homework-4: items[2] explain (26)

## Exam (topic-1.8)

Every keyed answer checks, including 625, 66, 7 (losses at 1, 3, 4, 7, 10), 9 (exact ratio 9.06), 16 for two round trips, 4 intervals, the heap index 1, the Dijkstra order and the BST deletion. The four code items pass with their solutions and fail with their starters; quadratic versions of `longest_flat` and `max_profit` time out.

- app/content/exams/topic-1.8.json | skills | note | Sorting (`at-sort`, items[11] only) and backtracking (`gd-backtrack`, items[18] only) have one item each; linked lists appear only as a design choice (items[16], [27]), with nothing on pointer manipulation or fast and slow pointers. | Consider replacing one of the five `at-complexity` items with a short reversal or cycle-detection trace (ds l12 and l13), so each course's core skills are tested twice.

## Layout (playthrough screenshots)

- app/content/courses/algo-think/l3-memory.json | screens[9] canvas | warning | The bars chart labels the unknown `numpy 200` bar "0.0", so it reads as an answer of 0 GB. The `numpy 100` bar (3.9) also lets the learner double it, without the computation the screen asks for. | Add `"showZero": false` to `params`, so the empty bar has no label until the explain patch fills it. Optionally drop the `n50` and `n100` bars.
- app/content/courses/algo-think/l1-counting-work.json | screens[3] canvas | warning | The four bars the table asks for (scan 16, pairs 16, scan 32, pairs 32) are drawn labelled "0". | Add `"showZero": false` to `params`.
- app/content/courses/graphs-dp/l17-dice-stopping.json | screens[5] canvas | warning | The bar for $V_4$, the value the table asks for, is labelled "0.00", and the bar for $V_3$ shows 4.67, the other cell the table asks for. | Add `"showZero": false` to `params`; as $V_3$ was worked out on screens[4], either make its row a given cell or drop the `3` bar until the explain.
- app/content/courses/ds/l18-order-book-heaps.json | screens[7] prose | note | At 390 px the display formula "add: $O(\log n)$, cancel: $O(1)$, best: $O(1)$ amortised, ..." is cut off at "best: O(1) an" with no visible scroll cue. | Write it as an `aligned` block, one operation per line.
- app/content/courses/ds/l18-order-book-heaps.json screens[0] to [4]; app/content/courses/graphs-dp/l14-knapsack.json screens[1] to [5] | canvas | note | At 390 px the order-book sizes and the knapsack table cells draw at about 8 px. They are legible but small. | `canvas.maxHeight` does not help here; raise an engine bullet for a minimum label size on `orderbook` and `table` canvases at narrow widths.

## Counts

1 error, 13 warnings, 25 notes.

## Fix pass

Targeted string edits only (a raw-text replace that must match once, then a JSON parse); no file was regenerated, and no lesson, screen or item id changed. Every number I touched was computed twice, once by a formula and once by a count (`fix-1.8` in the scratchpad: `rep.py`, `chk.py`, `long_fix.py`, `style2.py`). Each new hidden test was run in CPython with the reader's harness (`read-1.8/tools/runcode.py`) against the solution, the starter and the reader's naive version. The solution passes, and the starter and the naive version fail. Slow or memory-hungry versions are caught by large inputs, a read counter or `tracemalloc` peak memory, never a wall-clock assert (DECISIONS). Every case stays well inside 5 s: the slowest new case takes 0.3 s with the solution.

Status: fixed 37, disputed 0, deferred 2 (one needs a new exam item, one an engine change). Where a fix differs from the proposal, the line says why. Screen, item and quiz numbers are zero-based, as in the findings.

### Grading and keyed answers (4)

1. ds homework-3 items[2] (error): fixed as proposed. Third lot £49.00; `answer` 17650; `accept` "£17,650: $200 \times 50 + 100 \times 52 + 50 \times 49$"; `wrong` lifo 17300, avg 17441.67 (tol abs 1). Checked: FIFO $10{,}000 + 5{,}200 + 2{,}450 = 17{,}650$; LIFO $300 \times 49 + 50 \times 52 = 17{,}300$; weighted $29{,}900 / 600 \times 350 = 17{,}441.67$. The plain average of the prices, $(50 + 52 + 49)/3 \times 350 = 17{,}616.67$, is now outside the key's 0.5 tolerance. The `lifo` byKey says £49.00; the `avg` byKey says "weighted average cost"; the explain is the proposed one.
2. ds homework-1 items[6]: fixed, the proposed sentence. The key of 250,000,000 stands ($10{,}000 \times 50{,}001/2 = 250{,}005{,}000$).
3. algo-think homework-3 items[1] `b` why: fixed as proposed. Checked: greedy pays 6, 8 and 9 with 2, 3 and 3 coins, the fewest.
4. ds l15 quiz[3] `c` why: fixed as proposed.

### Tests that did not catch the ruled-out solution (10)

5. algo-think review-3 items[6]: fixed as proposed. The `Looks` prelude from l9 and a test on a million closes with `big.looks <= 100` (expect 501: the even numbers from 1,000 to 2,000). The scan reads 1,000,000 values and fails; two bisections read about 40. The `how` is split into three sentences.
6. ds homework-3 items[0]: fixed as proposed (test 7: 20,000 calls of `get_min` on 200,001 values). `min(self.xs)` stops after 5 s on it.
7. ds homework-3 items[4]: fixed as proposed (test 8: a 50,000-key cache, 150,000 calls). The list-of-keys version stops after 5 s; the solution takes 0.13 s.
8. ds homework-3 items[5]: fixed as proposed (`peak_bytes` added to the prelude; test 10 on 100,000 nodes). The set version fails it.
9. ds l13 screens[9]: fixed as proposed (a new prelude with `peak_bytes`; test 9). The set version fails it.
10. ds l13 screens[7] (note): fixed, with one more test than proposed. Test 13 checks `has_cycle` and test 14 `middle` (a list of nodes also passed before). Each naive version fails its own test. The prose now says "Aim for $O(1)$ space: two tests check your peak memory".
11. ds homework-4 items[1]: fixed as proposed. A postlude flag `NO_SORT` is test 9, and the `how` names it. The solution uses neither `sorted` nor `.sort`. `sorted(...)` fails.
12. ds l17 screens[9]: fixed as proposed (`peak_bytes` in the prelude; test 11 on a 200,000-value stream). `sorted(xs, reverse=True)[:k]` fails it.
13. algo-think l13 screens[8] (note): fixed with the first option, a line in `how`: "A hand-written full sort also passes, but costs $O(n \log n)$." I did not count comparisons. Merge sort on 100,001 values makes about $1.7 \times 10^6$. A fair three-way-partition quickselect can make about $10^6$ (three comprehensions over about $3.4n$ values). So no threshold separates them safely.
14. algo-think homework-3 items[6] (note): fixed as proposed. Test 9 asks for `kth_largest(sizes, 20000)`, expect 8005, from `sorted(sizes)[-20000]` and again from a count of values above each level. The $O(nk)$ removal and a scan-and-swap version both stop after 5 s; the solution takes 0.05 s. The `how` says "the 20,000th largest" and is split.

### Explanations (3)

15. algo-think l13 screens[0]: fixed as proposed.
16. ds l7 screens[8]: fixed as proposed. Checked: $\binom{10001}{2} + \binom{10000}{2} = 10^8$, and a count of the prefixes gives 10,001 and 10,000.
17. algo-think l3 screens[4]: fixed as proposed (4-byte pointer plus 16-byte float).

### Explanations over three sentences (13)

18 to 29. algo-think l1 screens[2] and review-3 items[1]; ds homework-1 items[5], l10 quiz[1], l13 screens[3], l15 screens[1], l16 screens[8] and [9], review-4 items[3]; graphs-dp l1 screens[8], l3 screens[2] and review-1 items[3]. All fixed as proposed.
30. Exam items[27]: fixed in a different way. The proposed first sentence runs to 21 words. Instead the last two sentences merge: "The design is judged by its worst common operation, here the cancel, which must be $O(1)$."

### Sentences over 20 words (3)

31 to 33. algo-think, ds, graphs-dp: fixed for the 65 sentences of 25 words or more. Each is split at its colon, semicolon or list, mostly "Check runs N hidden tests. They include ...". graphs-dp homework-4 items[2] lists its rows as "Rows 1 to 3: ... Rows 4 and 5: ...". The homework-2 items[4] latencies are grouped "from LD4" and "Other links"; every figure is unchanged. The two ds homework-2 rubric lines keep their points. The scan now finds no sentence over 24 words. It finds 183 of 21 to 24 words, against 185 before. A few new splits were tightened to stay at 20 or under. The rest are left for a later style pass, as the finding lists only those of 25 or more.

### Exam (1)

34. Skills coverage (note): deferred. Swapping an `at-complexity` item for a reversal or cycle trace means authoring and checking a new exam item, more than a targeted fix. It suits the next revision of the 1.8 exam.

### Layout (5)

35. algo-think l3 screens[9]: fixed. `showZero: false` was added, and the `numpy 50` and `numpy 100` bars start at 0, so nothing can be doubled. The explain patch already fills all six bars (1.97, 3.93, 7.86). The hint that compares the lists bar with the numpy one still holds.
36. algo-think l1 screens[3]: fixed, `showZero: false`.
37. graphs-dp l17 screens[5]: fixed. `showZero: false` was added, and the $V_3$ bar starts at 0. The explain patch now sets `"3": 4.6667` beside `"4": 4.9444`. Row 3 stays editable, so the graded cells are unchanged. Checked: $V_2 = 4.25$, $V_3 = 14/3$, $V_4 = 89/18 = 4.9444$.
38. ds l18 screens[7]: fixed. The formula is an `aligned` block, one operation per line.
39. ds l18 screens[0] to [4], graphs-dp l14 screens[1] to [5], label size: deferred as an engine change. The bullet is under "Raised later (fix pass 1.8)" in `docs/BACKLOG-INBOX.md`.

### Acceptance

From `app/`, with `--local-cdn`:
- `node tools/validate.mjs`: 0 errors (386 warnings; the only one in these courses is the ladder-canvas warning on ds l8 screens[6], a file this pass did not touch).
- `--lesson`: all 34 changed lessons pass (algo-think l1, l3, l4, l9 to l14; ds l2, l6, l7, l9 to l11, l13, l15 to l18; graphs-dp l1 to l5, l9 to l17).
- `--set`: all 15 changed reviews and homework sets pass.
- `--exam topic-1.8`: 28 of 28, passed.

Graded answers changed: ds homework-3 items[2] (key 17,650 and both wrong values). Nine code widgets gained hidden tests: algo-think review-3 items[6]; ds homework-3 items[0], [4] and [5]; ds l13 screens[7] (two) and [9]; ds homework-4 items[1]; ds l17 screens[9]. Test 9 of algo-think homework-3 items[6] is now the 20,000th largest. Every other key, option, cell and tolerance is unchanged. Not changed: `course.json`, any id, engine files.

### Finding 34, completed

Two items were replaced in place, so the count (28) and the ramp (6 at 2, 14 at 3, 5 at 4, 3 at 5) are unchanged.

- items[0] `e-tick-lookup` (d2, `at-complexity`, `ds-hashing`) became `e-insertion-count` (d2, `at-sort`). Insertion sort on 105, 102, 108, 106, 103, counted as algo-think l11 counts. The key is 8 comparisons. Checked by hand ($1 + 1 + 2 + 4$) and by an instrumented sort. Each wrong value names one slip: shifts only 5, the left end counted 9, the reversed worst case 10, sorted input 4.
- items[6] `e-loop-halving` (d3, `at-complexity`) became `e-floyd-meet` (d3, `ds-lists`). Eight nodes, 8 points back at 6; `slow` and `fast` as in ds l13. The key is 6 moves, meeting on node 7. Checked by a move-by-move trace and by a simulation. Wrong values: the cycle length 3, the moves to the cycle's start 5, the node count 8. The graph is drawn on two rows so it reads at 390 px.

Skills now: `at-sort` 2, `ds-lists` 3, `at-complexity` 3, `ds-hashing` 3; every skill appears at least twice except `gd-backtrack` (1), as the brief allowed one second item. The sentence scan finds none over 20 words in the exam, and no explanation over three sentences, so no other text changed. Validator 0 errors; `--exam topic-1.8` with `--local-cdn` passes 28 of 28 (also checked with `--mobile` screenshots).

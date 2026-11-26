# Concept audit: ds level 4, trees and heaps (blind, round 1)

Scope: `app/content/courses/ds/` l14-binary-trees, l15-search-trees, l16-tree-recursion, l17-always-the-smallest, l18-order-book-heaps, review-4, homework-4, read at commit bca3d7db. Ledger: `docs/reports/audit-ds-4-ledger.md` (180 rows: correct 149, wrong 4, imprecise 14, misleading 13, unverified 0). Script: `docs/reports/ds-L4-concepts.py`. The level's earlier reviews and reports were not opened until the ledger and the findings below were committed; the overlap table was filled afterwards.

Sources: CLRS 3e (B.5, 6, 12, 13, 17), Sedgewick and Wayne 4e (2.4, 3.2, 3.3), the CPython `heapq` and `bisect` documentation and `Lib/heapq.py`, CPython `Objects/listsort.txt`, the Python Language Reference 6.10.1, Harris, *Trading and Exchanges* ch. 6.

## Findings

1. l15-search-trees.json | screens[6].explain.text | wrong, minor | "A search for 6 would go right at 10 and never find it." The search goes left at 10. | 6 < 10, so the walk of screens[0] turns left at 10, reaches 5, turns right and steps onto `None`. The conclusion (not found) is right; the stated turn contradicts the rule the lesson has just taught. Script: `EXPECTED_FAIL l15 s6 explain`. Basis: CLRS 12.2 TREE-SEARCH. | Replace the last sentence with: "A search for 6 would go left at 10, because 6 < 10, and never find it."

2. l16-tree-recursion.json | screens[4].feedback.byKey.test-2 | wrong, minor | "Test 2 is one node, height 0. If you got 1, `None` returned 0 instead of −1." A `height` whose `None` case returns 0 fails test 1 (`height(None)`, expects −1) and is shown the test-1 line. The learners who do reach test 2 with a 1 have `None` at −1 and a leaf at 1 by another route, so the diagnosis is false for everyone who reads it. | Sweep: `None` → 0 fails test 1; a leaf special-cased to 1 and `max(..., 0)` fail test 2. Script: `EXPECTED_FAIL l16-tree-recursion widget 4 feedback.byKey.test-2`. | Replace with: "Test 2 is one node, height 0. A leaf needs no case of its own: `1 + max(-1, -1)` is already 0."

3. l14-binary-trees.json | screens[9].feedback.byKey.gross | wrong, minor | The slip value 5388 is explained as "You treated × as + or skipped the inner −." Treating × as + gives 50 + 8 − 12 = 46. | 5388 = 50 × 108 − 12, the inner subtraction skipped. Script: `EXPECTED_FAIL l14 s9 feedback.byKey.gross`. | Replace with: "You skipped the inner −: 50 × 108 − 12. The inner node gives 108 − 100 = 8 first, and 50 × 8 = 400."

4. l18-order-book-heaps.json | screens[9].widget.tests | misleading, serious | The lesson's objective is price-time priority, and `feedback.correct` says "Price-time priority, lazy cancels and partial fills, all in two heaps." The hidden tests do not enforce time priority: every test names its orders in arrival order (A1 before A2, A1 before A3), so a book that pushes `(price, order_id)` and keeps no time at all passes all 12 tests and is marked right. | Pyodide sweep: coding "no-time-in-tuple-id-breaks-tie" passes; on `A9` then `A1` at one price it fills the later order first. Script: `EXPECTED_FAIL l18 s9 tests`. Basis: Harris ch. 6 (time precedence is by arrival, not by identifier). | Append a 13th hidden test (the existing `test-N` lines keep their numbers): call `play([('add', 'A9', 'sell', 100.02, 200), ('add', 'A1', 'sell', 100.02, 300), ('add', 'B1', 'buy', 100.02, 250), ('match',)])`, expect `[[('B1', 'A9', 100.02, 200), ('B1', 'A1', 100.02, 50)]]` (the solution returns this). Change `how` to "Check runs 13 hidden tests." and add `feedback.byKey.test-13`: "Test 13 names the earlier order A9 and the later one A1. Time decides a price tie, not the id: keep the arrival time second in the tuple."

5. l14-binary-trees.json | screens[8].prose; summary.formula.note; l15-search-trees.json screens[3].explain.text | imprecise, minor | "Each node is visited once. Appending to one shared list keeps a walk $O(n)$." and "Every node is visited once: $O(n)$." The walk shown on the same screen, and the solution of screens[6], join lists with `+`. That copies every list at every level: O(n h), quadratic on a chain. The prose hints at this but never says the taught form is not O(n). | Script counts element copies on left chains of 200, 400, 800 nodes: doubling n quadruples the copies (`l14 s8` passes, `EXPECTED_FAIL l14 summary.formula.note` fails). Basis: list concatenation is O(len), CPython `list_concat`; CLRS Theorem 12.1 gives Θ(n) for a walk that prints. | screens[8].prose, replace the last paragraph with: "Each node is visited once. Joining lists with `+` copies them at every level, up to $O(n^2)$ on a chain. Appending to one shared list keeps a walk $O(n)$." summary.formula.note: "$v$ is the node, $L$ and $R$ its left and right sides. Every node is visited once: $O(n)$ when the walk appends to one list." l15 screens[3].explain, last sentence: "In-order on a BST gives sorted output, in $O(n)$ when the walk appends to one list."

6. homework-4.json | items[1] (h4-merge) prose and widget.how; l15-search-trees.json quiz[3] option d why; l17-always-the-smallest.json screens[7].prose and quiz[1] option d why; l18-order-book-heaps.json screens[8] option d why and feedback.byKey.d | imprecise, minor | These state the generic comparison-sort bound as the cost of Python's sort on data that is already nearly sorted: "Sorting everything again costs $O(N \log N)$", "re-sorting everything ignores that each list is already sorted", "`sort()` after every insert ... costs $O(n \log n)$ per insert". CPython's sort (Timsort) finds existing runs: a sorted list plus one item re-sorts in O(n), and k sorted lists joined end to end sort in about N log2 k comparisons, the same order as the heap merge. | Script, counted comparisons: `sort()` after one append to 16,384 sorted items makes under 3n comparisons; `sorted` on 64 presorted runs of 512 makes 182,308 comparisons against N log2 N = 491,520 and the heap merge's 229,354. Basis: CPython `Objects/listsort.txt`. The heap answers stay right; only the stated reason is too strong, and a learner would carry "sorted() ignores existing order" into an interview. | h4-merge prose, last sentence: "A general sort of all $N$ trades costs $O(N \log N)$; a heap holding one item per venue merges them in $O(N \log k)$, one trade at a time." h4-merge how, replace the third sentence with: "Use `heapq` with one entry per list, so the merge works item by item as a live feed needs." l15 quiz[3] option d why: "A general sort costs $O(n \log n)$; Python's does a nearly sorted list in about $O(n)$. `bisect.insort` finds the place in $O(\log n)$ and shifts once." l17 screens[7].prose: "Re-sorting from scratch after every update costs up to $O(n \log n)$ each time." l17 quiz[1] option d why: "That costs at least $O(n)$ per push and still leaves `heapq` popping the smallest." l18 screens[8] option d why: "That costs at least $O(n)$ per message. Heaps or arrays by tick keep the order as they go." l18 feedback.byKey.d: "You picked re-sorting. That is at least $O(n)$ per message; engines keep order incrementally."

7. l17-always-the-smallest.json | screens[4].prose | imprecise, minor | "Level $d$ of a heap holds $2^d$ items, so a heap of $n$ items has $\lfloor \log_2 n \rfloor + 1$ levels." Only full levels hold 2^d; the last level may hold fewer. The screen's own canvas is an 8-item heap whose level 3 holds one item. | Script: `EXPECTED_FAIL l17 s4 prose`. Basis: CLRS 6.1 (a heap is filled on all levels except possibly the lowest), Exercise 6.1-2. The level count itself is right. | Replace the second sentence with: "Level $d$ of a heap holds up to $2^d$ items, and every level but the last is full. So a heap of $n$ items has $\lfloor \log_2 n \rfloor + 1$ levels."

8. l18-order-book-heaps.json | screens[7].prose; quiz[3] (q-amortised) option c why | imprecise, minor | "With $n$ live entries: add $O(\log n)$ ..." and, against "lazy deletion makes the heap grow without limit": "Dead entries leave as soon as they reach the top, and each was pushed once." With lazy deletion the heap also holds every cancelled entry that has not surfaced, and a bid cancelled below the best never surfaces unless the market trades down to it. So n is the heap size, dead entries included, and the heap is bounded by the orders ever added, not by the live ones. | Script: 4,000 adds with 90% cancels and a read after each message leave 3,921 heap entries for 418 live bids, while total dead pops stay below the cancel count (the amortised claim itself is right, CLRS 17.1). The homework model answer already says "Dead entries also use memory until they reach the top". Basis: heapq docs, Priority Queue Implementation Notes. | screens[7].prose: replace "With $n$ live entries:" with "With $n$ entries in the heap, live or dead:" and append after the amortised sentence: "Dead entries below the top stay until they surface, so the heap can hold far more entries than live orders." quiz[3] option c why: "The heap never holds more entries than orders were added. Dead ones near the top leave at the next read; ones deep in the book wait, which costs memory."

9. l14-binary-trees.json | screens[6].feedback.byKey.test-5 | misleading, minor | "Test 5 passes `None`, an empty tree. Start with `if root is None: return []`." A walk with no `None` case never reaches test 5: it raises `AttributeError` at the first leaf of test 1 and gets the generic line. | Sweep: no-base-case codings fail test 1 (2 of 3); only a walk that checks each child before recursing reaches test 5. | Replace test-5 with: "Test 5 passes `None`, an empty tree. Checking `root.left` and `root.right` before each call is not enough: start with `if root is None: return []`." Add `test-1`: "Test 1 expects `[1, 2, 4, 5, 3, 6, 7]`. If it raised `AttributeError`, the walk stepped onto `None`: start with `if root is None: return []`."

10. l14-binary-trees.json | screens[10].feedback.byKey.test-4 | misleading, minor | "Test 4 is a single leaf, 42. A leaf has no children: return its value without recursing." A missing leaf case fails test 1; no natural coding reaches test 4 first. | Sweep: no leaf case fails test 1 (`AttributeError`), `None` as 0 fails test 1, a leaf test by `isinstance(node.val, int)` fails test 8 (the 0.5 leaf). | Delete `test-4`. Add `test-1` (see finding 11) and `test-8`: "Test 8 has a leaf of 0.5. Tell a leaf by its missing children, not by the type of its value."

11. l14-binary-trees.json | screens[10].feedback.byKey.test-7 | misleading, minor | "Test 7 expects −7 for 3 − 10. Subtract the right child from the left." Right minus left already fails test 1 with 412. | Sweep: `b - a` and swapped evaluation give 412 on test 1; `abs(a - b)` gives 7 on test 3. | Delete `test-7`. Add `test-1`: "Test 1 is the P&L tree, 388. If you got 412, `'-'` ran right minus left. If it raised `AttributeError`, you recursed below a leaf: return a leaf's own value."

12. l15-search-trees.json | screens[5].feedback.byKey.test-10 and test-2 | misleading, minor | "Test 10 inserts into an empty tree. Return `Node(v)` as the new root." `bst_from` starts every tree from `None`, so an `insert` with no empty-tree case fails test 1. "Test 2 checks the shape" is also out of reach: tests 1 and 2 use the same input, and every shape slip tried breaks test 1's in-order first. | Sweep: three codings of each; all six fail test 1. | Delete `test-10` and `test-2`. Add `test-1`: "Test 1 builds the tree from empty, so the first `insert` gets `None`: return `Node(v)` as the new root. After that, smaller values go left and larger go right."

13. l15-search-trees.json | screens[9].feedback.byKey.test-7 | misleading, minor | "Test 7 is a chain with no left children. Check for `None` before reading a node." A missing `None` check fails test 1. Test 7 is reached by treating a node with no left child as a leaf. | Sweep: no `None` check and a right-only guard fail test 1; "leaf means no left child" fails test 7 with `[]`. | Replace with: "Test 7 is a chain with no left children. A node with no left child can still have a right one: do not treat it as a leaf."

14. l16-tree-recursion.json | screens[4].feedback.byKey.test-5 | misleading, minor | "Test 5 is the empty tree, which has 0 nodes." A wrong base value (−1 copied from `height`) or no base case fails test 4, the first `size` test. | Sweep: −1 base gives −1 on test 4; no base raises on test 4; only a `size` that checks each child first reaches test 5. | Replace test-5 with: "Test 5 is the empty tree, which has 0 nodes. Checking each child before the call is not enough: start with `if root is None: return 0`." Add `test-4`: "Test 4 expects 6 nodes. The base case of `size` is 0, not −1: an empty tree has no nodes."

15. review-4.json | items[3] (r4-push) widget.options[3].why | wrong, minor | Option `[1, 3, 5, 9, 6, 4]`: "You swapped 1 with index 1, but its parent is index 2." Swapping the appended 1 with index 1 and then with the root gives `[1, 3, 4, 9, 6, 5]`, not this option. The option is the key with indices 1 and 2 exchanged. | Script: `EXPECTED_FAIL review-4 r4-push option d why`. | Replace the why with: "5 and 3 have changed places. 1 climbs from index 5 to index 2 to index 0, so 3 drops to index 2 and 5 never moves."

16. review-4.json | items[5] (r4-valid) explain.text | imprecise, minor | "The others each hide one node that passes its parent but fails an ancestor." Option d's repeated 3 is the left child of 3 and fails against its own parent. | Script: `looks_ok` rejects option d (`EXPECTED_FAIL review-4 r4-valid explain`). | Replace the second sentence with: "Two of the others hide a node that passes its parent but fails an ancestor. The last repeats a value, which the strict rule forbids."

17. l16-tree-recursion.json | screens[9].feedback.byKey.test-6 | misleading, minor | "Test 6 has only negative values. Do not start the best total at 0." A best total started at 0 already fails test 4 (`[1, -5]`, expects −4) or test 3 (`[-3]`). | Sweep: three codings; none reaches test 6. | Delete `test-6`. Replace `test-4` with: "Test 4 is 1 with one child, −5. The only route is 1 + (−5) = −4. If you got 1, a missing child or a best total started at 0 beat the real route."

18. l17-always-the-smallest.json | screens[5].feedback.byKey.test-6 | misleading, minor | "Test 6 pops the only item. After `heap.pop()` the list is empty: do not write to index 0." Test 5 drains a heap to empty, so this slip raises `IndexError` there first. | Sweep: both codings fail test 5. | Delete `test-6`. Add `test-5`: "Test 5 pops until the heap is empty. After the last `heap.pop()` the list is empty: do not write to index 0."

19. l17-always-the-smallest.json | screens[9].feedback.byKey.test-4 | misleading, minor | "Replace only when a value is strictly larger than `h[0]`, and keep duplicates." Replacing on `>=` is not a mistake: it passes all 11 tests. Only dropping repeats fails test 4. | Sweep: `>=` passes; a set, and skipping values already in the heap, give `[7, 3]` on test 4. | Replace with: "Test 4 has repeats: `[7, 7]`. Keep every copy: do not use a set, and do not skip a value already in the heap."

20. homework-4.json | items[2] (h4-median) feedback.byKey.test-7 | misleading, minor | "Test 7 has negative values. Remember the lower heap stores negated values: negate again when you read it." Reading the lower heap without negating fails test 1 (−5.0 for 5.0). Test 7 is reached by `abs(lo[0])`. | Sweep: four codings; only `abs` reaches test 7. | Replace test-7 with: "Test 7 has negative values. Read the lower heap's top as `-lo[0]`, not `abs(lo[0])`." Replace test-1 with: "Test 1 expects `[5.0, 10.0, 5.0, 4.0]`. A first value of −5.0 means the lower heap was read without negating. A wrong second value is the even case: the mean of the two tops."

21. l16-tree-recursion.json | screens[6].widget.tests | misleading, minor | The screen teaches a flag that travels up ("return −1 at once if either child returned −1"). A `check` that drops that step, and only returns −1 where the gap itself is too large, passes all 12 hidden tests. It calls a left chain of four nodes balanced: the −1 from below is read as a height. | Sweep: "flag-not-propagated" passes; script: `l16 s6: the flag-not-passed-up version calls a 4-node chain balanced` and `EXPECTED_FAIL l16 s6 tests`. | Append a 13th hidden test: call `is_balanced(build([1, 2, None, 3, None, 4]))`, expect `False` (the solution returns `False`). Change `how` to "Check runs 13 hidden tests." and add `feedback.byKey.test-13`: "Test 13 is a chain of four. An unbalanced side must send −1 straight up: return −1 as soon as either child returns −1."

22. homework-4.json | items[5] (h4-leaves) explain.text | imprecise, minor | "So indices 50 to 99 are leaves: 50 of them, half the heap. That is why sift-down from the middle builds a heap in $O(n)$." Half the items being leaves is why the build can start at the middle. It is not why the build is O(n): the other half could each sink log n levels. The bound comes from most nodes sitting near the bottom. | CLRS 6.3: sum over heights of ⌈n / 2^(h+1)⌉ · O(h) = O(n). Script: heapify makes under 3n comparisons against about n log2 n for worst-case pushes (`homework-4 h4-leaves explain` passes). | Replace the last sentence with: "So a heap can be built by sift-down from the middle index back to 0. Most items sit near the bottom and sink only a level or two, which makes that build $O(n)$."

23. l18-order-book-heaps.json | screens[8].widget.options[4].why | imprecise, minor | "Fills happen at the resting order's price. That is part of the price-time rule." Price-time priority decides who trades first. The trade price is a separate rule. | Harris ch. 6 treats order precedence rules and trade pricing rules apart; summary.ideas[1] already lists them side by side. | Replace with: "Fills happen at the resting order's price: it made the offer, and the arriving order accepts it."

Severity counts: wrong 4 (1, 2, 3, 15); imprecise 7 (5, 6, 7, 8, 16, 22, 23); misleading 12 (4, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21). Serious 1 (finding 4), minor 22.

## test-N sweep

Every `feedback.byKey.test-N` line on the level's 15 Python code widgets (47 lines) was swept. For each line, two to four natural codings of the mistake it names were appended to the widget's solution (a later `def` replaces the earlier one) and graded by the page's own harness under Pyodide 0.27.7 through `app/tools/code-runner.mjs`. Codings: `docs/reports/ds-L4-test-line-codings.txt` (108). Runner: `node docs/reports/ds-L4-test-line-sweep.mjs <abs app dir> <pkgs> docs/reports/ds-L4-test-line-codings.txt`. 68 codings fail the named test first, 40 do not.

| widget | line | codings that fail test N first | verdict |
|---|---|---|---|
| l14 screens[6] | test-2, test-7 | 2 of 2, 2 of 2 | correct |
| l14 screens[6] | test-5 | 1 of 3 (others fail test 1) | finding 9 |
| l14 screens[10] | test-4 | 0 of 3 (test 1, test 1, test 8) | finding 10 |
| l14 screens[10] | test-7 | 0 of 3 (test 1, test 3, test 1) | finding 11 |
| l15 screens[5] | test-2 | 0 of 3 (all test 1) | finding 12 |
| l15 screens[5] | test-6, test-9 | 2 of 3, 2 of 2 | correct |
| l15 screens[5] | test-8 | 1 of 3 (the named slip matches; two no-base recursions fail test 7) | correct |
| l15 screens[5] | test-10 | 0 of 3 (all test 1) | finding 12 |
| l15 screens[7] | test-2, test-4, test-6, test-14 | 1 of 1, 2 of 3, 2 of 2, 2 of 2 | correct |
| l15 screens[9] | test-2 | 1 of 3 (descriptive line; only `None` for an empty result reaches it) | correct |
| l15 screens[9] | test-9 | 2 of 2 | correct |
| l15 screens[9] | test-7 | 1 of 3 (the two `None`-check slips fail test 1) | finding 13 |
| l16 screens[4] | test-1 | 2 of 2 | correct |
| l16 screens[4] | test-2 | the named slip fails test 1; two other slips reach test 2 | finding 2 |
| l16 screens[4] | test-5 | 1 of 3 (others fail test 4) | finding 14 |
| l16 screens[6] | test-1, test-10 | 2 of 2, 2 of 2 | correct |
| l16 screens[6] | test-5 | 1 of 2 (the other passes every test) | correct; finding 21 |
| l16 screens[9] | test-4, test-1 | 2 of 2, 1 of 1 | correct |
| l16 screens[9] | test-6 | 0 of 3 (test 4, test 3, test 4) | finding 17 |
| l17 screens[5] | test-1, test-4, test-11 | 2 of 2, 2 of 2, 1 of 1 | correct |
| l17 screens[5] | test-6 | 0 of 3 (all test 5) | finding 18 |
| l17 screens[9] | test-1, test-10 | 2 of 2, 2 of 2 | correct |
| l17 screens[9] | test-3 | 1 of 2 (the other coding is correct code and passes) | correct |
| l17 screens[9] | test-4 | 2 of 3 (`>=` passes every test) | finding 19 |
| l18 screens[9] | test-1, test-3, test-7 | 2 of 2, 1 of 1, 2 of 2 | correct |
| l18 screens[9] | test-5 | 2 of 3 (no time at all passes every test) | correct; finding 4 |
| l18 screens[9] | test-6 | 1 of 3 (the named slip, the seller's price, matches; bid price and midpoint fail test 4) | correct |
| homework-4 h4-kth | test-8 | 2 of 2 | correct |
| homework-4 h4-merge | test-3, test-4 | 1 of 1, 2 of 2 | correct |
| homework-4 h4-median | test-1 | 1 of 1 | correct |
| homework-4 h4-median | test-7 | 1 of 4 (test 1, test 5, test 1) | finding 20 |
| homework-4 h4-save-tree | test-2, test-3, test-5 | 2 of 2, 2 of 2, 3 of 3 | correct |

Timing: no `test-N` line in the level depends on a time limit. The three efficiency lines (l15 screens[9] test-9, l16 screens[6] test-10, h4-kth test-8) count node reads, so they do not vary with the machine. One unnatural coding (a `pop` that puts the last item back) looped and was stopped at 5 s on l17 screens[5] test 5; no line names it. Recursion: the deepest test is a 300-node chain (l16 screens[6] test 11) against the page's limit of 3,000; every solution ran under Pyodide (wasm32) without a depth error.

Numeric slips: every `wrong[]` value with a feedback line was recomputed from the mistake it names (script and ledger). One does not match its line (finding 3). `homework-4` h4-leaves `levels` (36) and l18 screens[3] `skip` (−100) carry no feedback line and fall to the generic one.

## Checked and clean

Conventions are stated once and kept: root at depth 0, height in links, one node at height 0, `height(None)` = −1 (l14 screens[1], l16 screens[1], l15 screens[8], review-4, with l17 counting levels explicitly). BST costs are given as O(h) with both ends, floor(log2 n) ≤ h ≤ n − 1, and the chain worst case is shown before any balanced claim; no average-case claim is made. `heapq` is a min-heap throughout, ties fall to the next tuple field, and only the price is negated. Heap index rules, sift-up, sift-down, the level count and the 19-swap bound check out. Lazy deletion's amortised argument is right (each entry pushed once and popped at most once; the script counts dead pops against cancels). Price-time priority and fills at the resting price match Harris ch. 6. The diameter rule h(L) + h(R) + 2 agrees with a BFS diameter on 300 random trees, and both height conventions give the same balance verdict on them. `top_k` equals `heapq.nlargest` on 300 random inputs; `merge_k` and `running_median` equal `sorted` and `statistics.median` on 100 random inputs each. Heapify O(n) against n pushes O(n log n) appears once (h4-leaves) and holds by comparison count.

## Runs

- `node tools/validate.mjs`: 0 errors, 4606 warnings.
- `node tools/run-number-scripts.mjs --only ds` (venv Python): 1 of 436 scripts, 1 passed, 0 new failures, exit 0.
- `node tools/grade-all.mjs --code --file` on the seven files: 55 widgets and 15 Python code widgets, 0 failures, exit 0.
- `python -I docs/reports/ds-L4-concepts.py`: 23 failing checks, all 23 `EXPECTED_FAIL` (findings 1 to 21, with two checks each for findings 6 and 12; findings 22 and 23 rest on CLRS 6.3 and Harris ch. 6), 0 unexpected; exit 1 until the content is fixed.
- No playthrough (not in this audit's brief).

## Overlap with the earlier review

Filled after commit 117aa267 (ledger and findings). The earlier reads of these files are the topic 1.8 second read `docs/reviews/review-1.8.md` (ds l1 to l18, with its fix pass), the answer check `docs/reviews/answers-2026-11-03.md`, and `docs/reviews/review-perf-retrofit-12.md` (h4-save-tree: no finding). `docs/reports/ds-4-perf.md` is the author report of h4-save-tree. All were opened only after that commit.

| Count | Conceptual findings |
|---|---|
| Audit only | 23 (findings 1 to 23 above) |
| Earlier reads only | 4 (listed below, all applied before this audit) |
| Both | 0 |

Earlier conceptual findings at level 4 and why this audit did not raise them:

- review-1.8, l15 quiz[3] option c why said a dict "keeps no order": fixed to "does not keep keys sorted" before this audit; the ledger records the fixed line as correct.
- review-1.8, homework-4 h4-merge: `sorted(...)` passed all tests. Fixed with the `NO_SORT` test 9, which the audit's runs exercise. The review quoted the `how` sentence "re-sorting everything ignores that each list is already sorted" but did not question it; finding 6 here is about that sentence being false for CPython, a different point.
- review-1.8, l17 screens[9] `top_k`: `sorted(xs, reverse=True)[:k]` passed. Fixed with the `peak_bytes` test 11; nothing left to find.
- answers-2026-11-03, `NO_SORT` read the raw source, so a comment tripped it: fixed with the tokenised postlude, which the audit read. The raw `'heapq' not in __learner_source__` check of l17 screens[5] test 11 still has the comment weakness that file notes; it is an engine matter, not a concept.

The rest of the earlier findings on these files are style (sentence counts and lengths, 390 px layout). The earlier read ran every solution and 39 naive versions for complexity claims, but did not submit the mistakes the `test-N` lines name, which is where 12 of this audit's 23 findings come from; the two accepted wrong programs (findings 4 and 21) are wrong on correctness, not speed, so the naive-version method did not meet them.

## Fix pass

Opus fixer, on `0e8b282d`. Each fix was established independently of the auditor's text (own derivation, a run under the page's Pyodide, or CLRS 3e / CPython `Objects/listsort.txt`); where my fix differs from the proposed text, the status says so. Every rewritten or new `test-N` line was checked by submitting natural codings of the mistake it names under the page's harness (Pyodide 0.27.7, `tools/code-runner.mjs`, via `node docs/reports/ds-L4-test-line-sweep.mjs <abs app> <pkgs> docs/reports/ds-L4-fix-codings.txt`). The 56 codings are in `docs/reports/ds-L4-fix-codings.txt`; 55 fail the named test first and one (`>=` in `top_k`) is correct code that passes, as a control. 24 `mutants` entries now pin these lines, so `grade-all.mjs --code` fails if a coding stops landing on its test (checked: mis-numbering one gives `mutant-wrong-test`).

| # | status | basis (own) |
|---|---|---|
| 1 | fixed | 6 < 10, so TREE-SEARCH turns left at 10, then right at 5 onto `None` (CLRS 12.2; the tree is `[10, 5, 15, None, None, 6, 20]`). |
| 2 | fixed | `None` at 0 fails test 1 (`height(None)` expects −1). The codings that give 1 on test 2 special-case a leaf or floor the `max` at 0: 3 of 3 fail test 2 first, so the new line says a leaf needs no case. |
| 3 | fixed (mistake renamed, value kept) | 50 × 108 = 5,400 and 5,400 − 12 = 5,388; checked back: (5,388 + 12) / 50 = 108. × read as + gives 50 + 8 − 12 = 46. Slip band `abs 0` at 5,388 stays clear of 388, 400 and −388. |
| 4 | fixed differently | Hidden test 13 has a tie on each side (asks A9 then A1 at £100.02, bids B9 then B2 at £100.00), so a book that drops time on either side alone also fails. Expected value from the model solution, which keys on `(price, time, id)`; time is unique, so the id never decides. 3 codings (`(price, id)`, `(price, id, time)`, sorted lists by `(price, id)`) fail test 13 first; the starter fails test 1. `how` says 13 tests. |
| 5 | fixed differently | A `+` walk copies each subtree's list at its root: total copies = Σ subtree sizes = Σ (depth + 1) = Θ(n h), n(n + 1)/2 on a chain; CPython list concatenation copies both operands. l14 s8 now names $O(n^2)$ on a chain; the summary note and l15 s3 qualify $O(n)$ by the shared list. |
| 6 | fixed differently | Timsort's `count_run` finds the sorted prefix in n − 1 comparisons, so a sort after one append is O(n), not Θ(n log n) (`listsort.txt`); any re-sort must still read all n items, so "at least $O(n)$" is the bound used. Edited l15 q-bisect d, l17 s7, l17 q-max d, l18 s8 d and `byKey.d`, h4-merge prose and `how`, and the same claim in h4-median explain, which the finding did not list. The heap and `bisect` answers are unchanged. |
| 7 | fixed | A heap is a complete tree: levels 0 to L − 2 are full and the last holds 1 to 2^(L−1) items, so 2^(L−1) ≤ n ≤ 2^L − 1 and L = ⌊log₂ n⌋ + 1 (CLRS 6.1). |
| 8 | fixed differently | The heap holds every entry pushed and not yet popped. A cancelled entry is popped only at the top, so the size is bounded by adds, not live orders. Shorter appended sentence than proposed, to keep the screen's prose under 60 words. q-amortised c adds that heap size enters only through log n. |
| 9 | fixed | test-1 added: 3 codings (no base case, in-order shape, right before left) fail test 1. test-5: 3 codings that guard the children fail test 5 first. |
| 10 | fixed differently | test-4 is reachable, so it is rewritten, not deleted: 3 codings that test leaves only as children raise at test 4 on the lone leaf 42. test-8 added: 3 codings that tell a leaf by type (`isinstance(.., int)`, `type(..) is int`, `isdigit`) recurse onto `None` at the 0.5 leaf. |
| 11 | fixed differently | test-7 is reachable by clipping `'-'` at 0 (as in a payoff), so it is rewritten: 3 codings give 0 on test 7 and pass tests 1 to 6. test-1 added: right minus left gives 412 (2 codings), no leaf case raises (1). |
| 12 | fixed | `bst_from` starts from `None` (prelude), so an `insert` without the empty case fails test 1. With distinct keys, a sorted in-order and the standard walk fix the shape, so test 2 shares test 1's input and no natural coding reaches it. Deleted test-2 and test-10; test-1 added, 3 codings. |
| 13 | fixed | 3 codings that treat a node with no left child, or not two children, as a leaf return `[]` on test 7. The missing-`None`-check coding fails test 1 and gets the generic line. |
| 14 | fixed | test-4 added: base −1 gives −1, no base raises, `1 + max(...)` gives 4 (3 codings, test 4). test-5: 3 codings that guard the children raise at test 5. |
| 15 | fixed | Sift-up of 1 from index 5: parent 2 holds 4, swap; parent 0 holds 3, swap: `[1, 5, 3, 9, 6, 4]`. Option d is that list with indices 1 and 2 exchanged; the named path (index 1, then root) gives `[1, 3, 4, 9, 6, 5]`. |
| 16 | fixed | In option d the second 3 is the left child of 3; the strict rule needs left < parent, so it fails its own parent, not an ancestor. |
| 17 | fixed | 3 codings (best from 0, missing child as 0 by `None` case, by inline `else 0`) give 1 on test 4; none reaches test 6, so test-6 is deleted. |
| 18 | fixed | 3 codings that write index 0 after the last `heap.pop()` raise `IndexError` at test 5, which drains to empty; test-6 deleted. |
| 19 | fixed | `x >= h[0]` swaps an item for an equal one, so the kept multiset is unchanged: correct code, and it passes all 11 tests. The line now names the set and skip mistakes (3 codings give `[7, 3]` or `[7]`). |
| 20 | fixed differently | Same diagnosis, worded without the solution's variable names. test-1: 3 codings (lower top not negated, even case not negated, even case one top) fail test 1. test-7: 3 codings using `abs` fail test 7 first. |
| 21 | fixed differently | Hidden test 13 is the five-node zigzag `[1, None, 2, 3, None, None, 4, 5]`, not a left chain: a search over random trees found it the smallest that also catches a flag passed up from one side only, and `and` for `or`. 4 codings fail test 13 first; the solution returns False (unbalanced at 3: heights 0 and 2 in nodes). `how` says 13 tests. |
| 22 | fixed | CLRS 6.3: BUILD-MAX-HEAP costs Σ_h ⌈n / 2^(h+1)⌉ O(h) = O(n). Half the items being leaves only sets the start index, ⌊n/2⌋ − 1 = 49. |
| 23 | fixed | Priority decides who trades first; the price is a separate rule: the trade is at the resting order's limit, because it made the quote and the arriving order accepts it. |

Not changed: no existing hidden test, solution or key. Two hidden tests added (l16 s6 test 13, l18 s9 test 13), each passing the model solution, failed by the starter and by the named wrong program.

Concepts script: `docs/reports/ds-L4-concepts.py` now exits 0. The checks for findings 1, 3, 5, 6, 7, 8, 15 and 16 encoded the old text as a computation the content cannot change; they are re-pointed to the content strings and keep the computation as evidence (docstring says so). The test-N checks name the line each coding now lands on, and the script also runs the fixer's 56 codings in CPython. On the old content it fails 48 checks (the 23 findings plus the 25 fixer codings whose lines did not exist).

Gates: validator 0 errors (4,608 warnings, the same as before the fix); voice scan 35 on the seven files 0 and 0; concepts script 0 failing, exit 0; number scripts `--only ds` 1 of 1 passed; `grade-all.mjs --code --file` on each of the seven files 0 failures (mutants included); playthrough of l14 to l18, review-4 and homework-4 green desktop and `--mobile` (14 runs).

## Fix-pass read

Fresh reader, blind to the audit, the earlier reviews and the fixer's script and codings until the rows below were written. Read: `git show dc9834ae -- app/content/courses` (ds l14 to l18, review-4, homework-4). Content at `a229f564` is identical to `dc9834ae` for these seven files.

Script: `docs/reports/ds-L4-fixread.py --local-cdn <pkgs>` exits 0 (95 checks; the one failing check is finding F1 and is listed in `KNOWN`). Part A derives the two new hidden-test expects and the numbers in the changed text. Part B grades 45 of my own codings, plus solution and starter of the 11 changed code widgets, under the page's Pyodide through `app/tools/code-runner.mjs`. `grade-all.mjs --code --file` on the seven files: 15 code widgets, 0 failures, so all 24 committed mutants first fail the test they name. Validator 0 errors.

Counts found in the diff: 18 `test-N` lines added or rewritten, 4 deleted (l15 s5 `test-2` and `test-10`, l16 s9 `test-6`, l17 s5 `test-6`), 24 mutants in 11 groups, 2 hidden tests added.

### Ledger (55 rows)

Sources: CLRS 4th ed. (ch. 6 heaps, 12 search trees, B.5 trees), Sedgewick and Wayne *Algorithms* 4th ed. (2.4, 3.2), CPython `heapq`, `bisect` and `listsort.txt` docs. "run" means the script above.

| # | file | JSON path | claim | verdict | basis |
|---|---|---|---|---|---|
| 1 | homework-4 | items[1].prose | general sort O(N log N); k-way heap merge O(N log k), one trade at a time | correct | CLRS ex. 6.5-9; heap holds at most k entries |
| 2 | homework-4 | items[1].widget.how | one entry per list lets the merge work item by item | correct | derivation: each pop needs only the heads; 9 tests counted |
| 3 | homework-4 | items[2].feedback.byKey.test-1 | first value −5.0 means the lower top was read un-negated; wrong second value is the even case | correct | run: my 3 codings first fail test 1 with `[-5.0, ...]`, `[5.0, 5.0, ...]`, `[5.0, 5.0, ...]` |
| 4 | homework-4 | items[2].feedback.byKey.test-7 | negate the lower top; `abs` gives the wrong sign on negatives | correct | run: 2 codings pass tests 1 to 6, first fail test 7 with `[1.0, 0.5, 2.0]` |
| 5 | homework-4 | items[2].widget.mutants (2) | first fail tests 1 and 7; symptoms as stated | correct | grade-all run |
| 6 | homework-4 | items[2].explain.text | each step O(log n); re-sorting costs at least O(n) | correct | CLRS 6.5; a sort must read every item. See note N1 |
| 7 | homework-4 | items[5].explain.text | indices 50 to 99 are leaves; build sifts from 49 to 0; most items sink a level or two; build is O(n) | correct | run: 88% of 100 items (87.5% of 10^5) can sink at most two levels, total sink room 97 < 2n; CLRS 6.3 |
| 8 | l14-binary-trees | screens[6].feedback.byKey.test-1 | pre-order is node, left, right; `AttributeError` means the walk stepped onto `None` | correct | run: stack walk pushing `None` raises at test 1; node-after-left gives `[4, 2, 5, 1, 6, 3, 7]` at test 1 |
| 9 | l14-binary-trees | screens[6].feedback.byKey.test-5 | checking children before each call still fails `preorder(None)` | correct | run: 2 codings pass tests 1 to 4, raise at test 5 |
| 10 | l14-binary-trees | screens[6].widget.mutants (2) | first fail tests 1 and 5 | correct | grade-all run |
| 11 | l14-binary-trees | screens[8].prose | `+` copies the lists at every level: O(n²) on a chain; one shared list keeps O(n) | correct | run: copies on a chain of 400 are 80,200 = n(n+1)/2, of 800 are 320,400 (ratio 4.0) |
| 12 | l14-binary-trees | screens[9].feedback.byKey.gross | 5388 is 50 × 108 − 12; inner node 108 − 100 = 8, 50 × 8 = 400 | correct | arithmetic, and the `gross` value is 5388 |
| 13 | l14-binary-trees | screens[10].feedback.byKey.test-1 | 388; 412 is right minus left; `AttributeError` is recursion below a leaf | correct | run: `b - a` gives 412 at test 1 (12 − 50 × (100 − 108)); no leaf case raises at test 1 |
| 14 | l14-binary-trees | screens[10].feedback.byKey.test-4 | the root can be a leaf: test `node`, not only its children | correct | run: 2 codings pass tests 1 to 3, raise at test 4 |
| 15 | l14-binary-trees | screens[10].feedback.byKey.test-7 | do not clip `'-'` at 0; only `'max'` with a 0 child does that | correct | run: 2 clipped codings pass tests 1 to 6, give 0 at test 7. See note N2 |
| 16 | l14-binary-trees | screens[10].feedback.byKey.test-8 | tell a leaf by its missing children, not the type of its value | correct | run: `type(...) is int` and `str(...).isdigit()` pass tests 1 to 7, raise at test 8 |
| 17 | l14-binary-trees | screens[10].widget.mutants (4) | first fail tests 1, 4, 7, 8 | correct | grade-all run |
| 18 | l14-binary-trees | summary.formula.note | O(n) when the walk appends to one list | correct | as row 11 |
| 19 | l15-search-trees | screens[3].explain.text | in-order on a BST is sorted, O(n) when appending to one list | correct | CLRS thm 12.1; as row 11 |
| 20 | l15-search-trees | screens[5].feedback.byKey.test-1 | first call gets `None`: return `Node(v)`; smaller left, larger right; assign the result | correct | run: no empty case raises, unassigned call gives `[50]`, mirrored sides give descending, all at test 1 |
| 21 | l15-search-trees | screens[5].feedback.byKey test-2, test-10 (deleted) | neither can be the first failing test for the mistakes they named | correct | test 1 calls `insert(None, v)` and checks order first; the three codings of row 20 all stop at test 1 |
| 22 | l15-search-trees | screens[5].widget.mutants (1) | first fails test 1 | correct | grade-all run |
| 23 | l15-search-trees | screens[6].explain.text | a search for 6 goes left at 10 and never finds it | correct | run: path 10 left, 5 right, `None` |
| 24 | l15-search-trees | screens[9].feedback.byKey.test-7 | a node with no left child can still have a right one | correct | run: 2 codings pass tests 1 to 6, return `[]` at test 7 |
| 25 | l15-search-trees | screens[9].widget.mutants (1) | first fails test 7 | correct | grade-all run |
| 26 | l15-search-trees | quiz[3].widget.options[3].why | `sort()` on a nearly sorted list still compares all n items; `insort` needs O(log n) comparisons and one shift | correct | run: 1,020 comparisons at n = 1,000 and 4,024 at 4,000 against 10 and 12; CPython `listsort.txt` (run detection reads every item) |
| 27 | l16-tree-recursion | screens[4].feedback.byKey.test-2 | one node has height 0; `1 + max(-1, -1)` is 0, so no leaf case | correct | CLRS B.5.2 (height in edges, leaf 0); run: 2 codings pass test 1, give 1 at test 2 |
| 28 | l16-tree-recursion | screens[4].feedback.byKey.test-4 | `size(None)` is 0, not −1; add both sides | correct | run: −1 base gives −1 (n nodes, n + 1 empty links); `max` gives 4; both at test 4 |
| 29 | l16-tree-recursion | screens[4].feedback.byKey.test-5 | child checks are not enough for `size(None)` | correct | run: 2 codings pass tests 1 to 4, raise at test 5 |
| 30 | l16-tree-recursion | screens[4].widget.mutants (3) | first fail tests 2, 4, 5 | correct | grade-all run |
| 31 | l16-tree-recursion | screens[6].widget.tests[12] | `build([1, None, 2, 3, None, None, 4, 5])` is not balanced | correct | run: shape 1 R 2 L 3 R 4 L 5; by the definition with a separate edge height, False, and 3 is the only unbalanced node (sides −1 and 1). Solution passes, starter fails |
| 32 | l16-tree-recursion | screens[6].widget.how | 13 hidden tests | correct | counted |
| 33 | l16-tree-recursion | screens[6].feedback.byKey.test-13 | five-node zigzag, unbalanced at 3; return −1 as soon as either child returns −1 | correct | run: flag never passed, right-only and left-only codings all pass tests 1 to 12 and answer `True` at test 13 |
| 34 | l16-tree-recursion | screens[6].widget.mutants (4) | all first fail test 13 | correct | grade-all run; my no-propagation helper also answers the four older unbalanced builds, so only test 13 separates it |
| 35 | l16-tree-recursion | screens[9].feedback.byKey.test-4 | route is 1 + (−5) = −4; a 1 comes from a missing child or a best started at 0 | correct | run: both codings give 1 at test 4. See note N3 |
| 36 | l16-tree-recursion | screens[9].feedback.byKey.test-6 (deleted) | no false text remains | correct | see note N3: one coding does reach test 6 first and now gets the generic line |
| 37 | l16-tree-recursion | screens[9].widget.mutants (2) | both first fail test 4 with 1 | correct | grade-all run |
| 38 | l17-always-the-smallest | screens[4].prose | level d holds up to 2^d items, every level but the last is full, ⌊log₂ n⌋ + 1 levels | correct | CLRS 6.1 and ex. 6.1-2; run for n = 1 to 5,000 |
| 39 | l17-always-the-smallest | screens[5].feedback.byKey.test-5 (test-6 deleted) | the drain's last pop empties the list: do not write to index 0 | correct | run: `heap[0] = heap.pop()` in two forms passes tests 1 to 4, `IndexError` at test 5; test 6 can no longer be first |
| 40 | l17-always-the-smallest | screens[5].widget.mutants (1) | first fails test 5 | correct | grade-all run |
| 41 | l17-always-the-smallest | screens[7].prose | re-sorting reads all n items: at least O(n), O(n log n) for a general sort | correct | as rows 6 and 26; CLRS thm 8.1 for the general bound |
| 42 | l17-always-the-smallest | screens[9].feedback.byKey.test-4 | keep every copy: no set, no skipping a value already in the heap | correct | run: both codings give `[7, 3]` at test 4; a `>=` replace passes all 11, so the old "strictly larger" advice was rightly dropped |
| 43 | l17-always-the-smallest | screens[9].widget.mutants (1) | first fails test 4 | correct | grade-all run |
| 44 | l17-always-the-smallest | quiz[1].widget.options[3].why | reverse-sorting after each push "still leaves `heapq` popping the smallest" | **wrong** | run: after push and `sort(reverse=True)` of 5, 1, 3, 9, 4, `heappop` returns 9, 1, 3, 4, 5. `heappop` returns index 0 (CPython `heapq` docs), which is the largest. Finding F1 |
| 45 | l18-order-book-heaps | screens[7].prose | n counts heap entries live or dead; dead entries below the top wait, so the heap can outgrow the live book | correct | derivation: lazy deletion pops only at the top; Sedgewick 2.4 |
| 46 | l18-order-book-heaps | screens[8].widget.options[3].why | re-sorting reads the whole book, at least O(n) per message | correct | as row 6 |
| 47 | l18-order-book-heaps | screens[8].widget.options[4].why | fills at the resting order's price: it made the offer, the arriving order accepts | correct | Harris, *Trading and Exchanges*, ch. 6 (discriminatory pricing in continuous order-driven markets) |
| 48 | l18-order-book-heaps | screens[8].feedback.byKey.d | same as row 46 | correct | as row 6 |
| 49 | l18-order-book-heaps | screens[9].widget.tests[12] | expect `[[('B1','A9',100.02,200), ('B1','A1',100.02,50)], [('B9','A5',100.0,100), ('B2','A5',100.0,50)]]` | correct | run: my reference book (no heap, minimum of (price, time), fill at the earlier order's price) gives the same, and agrees with tests 1 to 11. Solution passes, starter fails |
| 50 | l18-order-book-heaps | screens[9].widget.how | 13 hidden tests; test 12 has 8,000 orders | correct | counted |
| 51 | l18-order-book-heaps | screens[9].feedback.byKey.test-13 | A9 before A1 and B9 before B2 at one price; time decides, so time goes second in the tuple | correct | run: (price, id) and (price, id, time) pass tests 1 to 12 and fill A1 and B2 first at test 13; (price, time, id) passes. Tuples compare left to right (Python reference, 6.10.1) |
| 52 | l18-order-book-heaps | screens[9].widget.mutants (3) | all first fail test 13 | correct | grade-all run |
| 53 | l18-order-book-heaps | quiz[3].widget.options[2].why | heap never holds more entries than orders added; size enters only through log n; deep dead entries cost memory | correct | derivation: one push per add |
| 54 | review-4 | items[3].widget.options[3].why | in option d, 5 and 3 have changed places; 1 climbs 5 to 2 to 0, 3 drops to index 2, 5 never moves | correct | run: `heappush` gives `[1, 5, 3, 9, 6, 4]` |
| 55 | review-4 | items[5].explain.text | two others fail an ancestor; "the last" repeats a value | imprecise | run: b and c pass the parent check and fail 8; d repeats 3. But the options have `"shuffle": true`, so "the last" names a different option on most draws. Finding F2 |

Counts: 55 rows. correct 53, wrong 1, imprecise 1, misleading 0, unverified 0.

Conventions checked in the changed text: height in edges with `None` at −1 and a leaf at 0 (l16 s4), node-count heights only inside the `is_balanced` helper and said so (l16 s6), heap levels ⌊log₂ n⌋ + 1 with swaps one fewer (l17 s4), price then arrival time with fills at the resting price (l18 s8, s9). All consistent with each other and with CLRS and Sedgewick.

### Findings

F1. l17-always-the-smallest | quiz[1].widget.options[3].why | wrong, minor | The line says a reverse sort "still leaves `heapq` popping the smallest". `heappop` returns index 0, and after a reverse sort that is the largest item. The fix pass changed only the cost clause; the false clause is older text in the same sentence. | Run in the script: pops are 9, 1, 3, 4, 5. Derivation: `heappop` then moves the last item, the smallest, to the root, where it stays, so the second pop returns the smallest. | Paste-ready:

```json
"why": "That costs at least $O(n)$ per push, and it breaks the order `heapq` relies on. The first pop returns the largest, but the next returns the smallest."
```

F2. review-4 | items[5].explain.text | imprecise, minor | "The last repeats a value" points by position, and the options are shuffled. | The repeated 3 is option d only in file order. | Paste-ready:

```json
"text": "In the valid tree, 8's left side is below 8 and its right side is above 8, at every level. Two of the others hide a node that passes its parent but fails an ancestor. The one with two 3s repeats a value, which the strict rule forbids."
```

### Notes (no verdict changes)

N1. "At least $O(n)$" appears in six changed lines. CLRS 3.2 would write Ω(n); the course has not taught Ω, and the meaning ("no cheaper than linear") is right. No fix asked.

N2. l14 s10: `'-'` coded as `abs(a - b)` first fails test 3 (gets 7 for `max(98 − 105, 0)`), which has no line. Optional: `"test-3": "Test 3 expects 0: 98 − 105 is −7, and 'max' with 0 lifts it to 0. If you got 7, '-' dropped the sign."`

N3. l16 s9: "best total started at 0" has two more natural codings. One running best over all routes fails test 3 first (returns 0 for the single node −3). One-child nodes handled apart, with a two-child best started at 0, fails test 6 first (−10), the line the fix pass deleted. Both get only the generic line. Optional:

```json
"test-3": "Test 3 is one node, −3, so the answer is −3. Do not start the best total at 0.",
"test-6": "Test 6 has only negative values: the best route is −10 + (−2) = −12. Do not start the best total at 0."
```

After the rows: read against the audit above. F1 is in a sentence finding 6 rewrote; neither the audit nor the fix pass questioned its last clause. F2 is the wording of finding 16's own paste-ready fix, applied as written. The one `wrong` (F1) counts towards the convergence rule for this round.

## Fix-pass follow-up (orchestrator)

- The fix-pass read's wrong row (l17 `quiz[1]` option d `why`) and imprecise row (review-4 `items[5].explain`) applied with the reader's text. Basis checked by the orchestrator: `heapq.heappop` on `[9, 5, 4, 3, 1]` returns 9, then 1, 3, 4, 5 (CPython 3.13); the options are shuffled, so "the last" names no fixed option. The wrong counts towards round 1 (5 wrong in all). Gates: validator 0 errors, voice scan 0 and 0, concepts and fixread scripts 0, ds number script 1 of 1, grade-all --code 0 failures, playthrough desktop and mobile green on both files.

# Claim ledger: ds level 4, trees and heaps (blind concept audit, round 1)

Files: `app/content/courses/ds/` l14-binary-trees, l15-search-trees, l16-tree-recursion, l17-always-the-smallest, l18-order-book-heaps, review-4, homework-4, read at commit bca3d7db. Script: `docs/reports/ds-L4-concepts.py` (`sim:` rows name its check message). Sweep: the Pyodide run of 108 codings against the hidden tests, table in `docs/reviews/audit-ds-4.md` (`sweep:` rows).

Sources: CLRS = Cormen, Leiserson, Rivest, Stein, *Introduction to Algorithms* 3e (B.5 trees; 6 heapsort; 12 binary search trees; 13 red-black trees and Problem 13-3 AVL; 17 amortised analysis). SW = Sedgewick and Wayne, *Algorithms* 4e (2.4 priority queues; 3.2 binary search trees; 3.3 balanced search trees). heapq docs = CPython library reference, `heapq` ("min-heap", "heap[0] is always its smallest element", "Priority Queue Implementation Notes") and `Lib/heapq.py`. bisect docs = CPython library reference, `bisect` (performance notes: "the O(n) insertion step"). listsort = CPython `Objects/listsort.txt` (Timsort run detection and merge cost). LangRef = *The Python Language Reference* 6.10.1 (value comparisons: sequences compare lexicographically; no default ordering for mappings). Harris = Harris, *Trading and Exchanges* (2003) ch. 6 (order precedence rules: price priority then time precedence; the discriminatory pricing rule, each trade at the standing order's price).

Conventions checked once and then for consistency: depth of the root 0, height in links, one node has height 0, `height(None)` = −1 (l14 screens[1], l16 screens[1], review-4 r4-height, l15 screens[8], l17 screens[4] in levels): consistent throughout, CLRS B.5.2. `heapq` is a min-heap with tuple ties broken by the next field: consistent. Fills at the resting order's price: consistent.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l14 | screens[0].prose | A binary tree is nodes with a value and `left`, `right` links; a link to nothing is `None` | correct | CLRS 10.4, B.5.3 |
| l14 | screens[0].widget.answer, feedback.byKey.l, r | D, E, F, G have both links `None`; B and C do not | correct | canvas tree A(B(D,E),C(F,G)) |
| l14 | screens[0].hints, feedback.correct | Nodes with no line below are the ones with no children | correct | restates the definition |
| l14 | screens[0].explain | A node with no children is a leaf; every node except the root has exactly one parent | correct | CLRS B.5.2 |
| l14 | screens[1].prose, answer, wrong nodes 3 | Two links from A to G; 3 counts nodes | correct | sim: l14 s1 and q-height |
| l14 | screens[1].explain | Depth = links from the root (root 0); height = greatest depth; a one-node tree has height 0 | correct | CLRS B.5.2 (depth, height in edges); sim: l14 s1 and q-height |
| l14 | screens[2].prose, order, hints, feedback, explain | Print before both calls gives A B D E C F G; this is pre-order | correct | sim: l14 s2-s5; CLRS 12.1 |
| l14 | screens[2].feedback.byKey.C, D | C straight after B is level order; D first is in-order thinking | correct | follows from the code |
| l14 | screens[3] (all) | Print between the calls gives D B E A F C G; in-order | correct | sim: l14 s2-s5 |
| l14 | screens[4] (all) | Print after both calls gives D E B F G C A; post-order; the root comes last | correct | sim: l14 s2-s5 |
| l14 | screens[4].explain | A parent waits for its children, which is what a calculation over the tree needs | correct | post-order is bottom-up evaluation, CLRS 12.1 exercise style; used in l16 |
| l14 | screens[5].prose, options, explain | Queue walk; after C is taken out and its children added the queue holds D, E, F, G; first in first out keeps each level ahead of the next | correct | traced; BFS, CLRS 22.2 |
| l14 | screens[5].options[1..3].why | F,G drops D,E; D,E stops early; F,G,D,E adds at the front | correct | traced |
| l14 | screens[6].prose | `build` reads a level-order list; `None` marks a missing child, which gets no children of its own in the list | correct | prelude `build` read and run |
| l14 | screens[6].widget solution, tests, how | Three traversals pass 14 tests; empty tree, one node, chains | correct | sim: widget 6 solution passes; grade-all --code 0 failures |
| l14 | screens[6].hints, explain | Each recursive version is an empty case plus two sides joined round the node; level order swaps recursion for a queue | correct | matches the solution |
| l14 | screens[6].feedback.byKey.test-2 | 1 first on test 2 means the node was added before its left side | correct | sweep: 2 of 2 codings fail test 2 first |
| l14 | screens[6].feedback.byKey.test-5 | Test 5 (`preorder(None)`) is where a missing `None` case shows | misleading | sweep: the plain missing base case fails test 1 with AttributeError (2 of 3); only a child-guarding walk reaches test 5. Finding 9 |
| l14 | screens[6].feedback.byKey.test-7 | Test 7 (`level_order(None)`): start the queue empty or `node.val` fails | correct | sweep: 2 of 2 fail test 7 first |
| l14 | screens[7].prose, options, feedback | Node first is pre-order whatever the name; swapping the calls gives A C G F B E D; sorting hides the bug | correct | sim: l14 s7 option b |
| l14 | screens[7].explain | Dropping the `None` check raises `AttributeError` (`None.left`) | correct | CPython: `'NoneType' object has no attribute 'left'`, seen in the sweep |
| l14 | screens[8].prose | One pattern, three orders; "Each node is visited once. Appending to one shared list keeps a walk O(n)" | imprecise | true, but the walk shown and taught joins lists with `+`, which is O(n h), quadratic on a chain; the sentence never says so. sim: l14 s8 and the EXPECTED_FAIL beside it. Finding 5 |
| l14 | screens[8].options, feedback, explain | A parent that needs its children's results fits post-order; pre, in and level order each miss a result | correct | definition of post-order |
| l14 | screens[9].prose, answer | Expression tree 50 × (108 − 100) − 12 = 388, operators take the left child first | correct | sim: l14 s9 key 388 |
| l14 | screens[9].wrong fee 400, sign −388 and their feedback | 400 stops at ×; −388 is 12 − 400 | correct | sim: l14 s9 key 388, slips |
| l14 | screens[9].feedback.byKey.gross | 5388: "You treated × as + or skipped the inner −" | wrong | 5388 = 50 × 108 − 12 (inner − skipped); × as + gives 46. sim: EXPECTED_FAIL l14 s9. Finding 3 |
| l14 | screens[9].hints, explain | Bottom up: 8, 400, 388; expressions are evaluated post-order | correct | arithmetic; CLRS 12.1 |
| l14 | screens[10].prose | Leaves hold numbers, inner nodes `+ - * max` with two children; a call pays max(S − K, 0) | correct | Hull ch. 10 payoff; tree as stated |
| l14 | screens[10].widget solution, tests, how | `evaluate` passes 8 tests; `'-'` is left minus right; test 6 is a bull call spread worth 10 | correct | sim: widget 10 solution passes; l14 s10 test 6 |
| l14 | screens[10].feedback.byKey.test-4 | Test 4 (a single leaf) is where a missing leaf case shows | misleading | sweep: 0 of 3 codings reach test 4 (no leaf case fails test 1; int-only leaf test fails test 8). Finding 10 |
| l14 | screens[10].feedback.byKey.test-7 | Test 7 (3 − 10) is where right-minus-left shows | misleading | sweep: right minus left gives 412 on test 1; abs gives 7 on test 3. Finding 11 |
| l14 | screens[10].explain, caption | Post-order; max(110 − 95, 0) − max(110 − 105, 0) = 10; 100 × 10 = 1000 | correct | sim: l14 s10 |
| l14 | summary.ideas | Tree = nodes with links, empty tree is `None`; three orders are one recursion; level order uses a queue | correct | as above |
| l14 | summary.formula | pre: v, L, R; in: L, v, R; post: L, R, v. "Every node is visited once: O(n)" | imprecise | visits are O(n); the cost of the taught `+` walk is not. Finding 5 |
| l14 | summary.trap | Node before its left side is pre-order; without the `None` check the walk crashes at the first leaf | correct | crash is on the leaf's `None` child |
| l14 | quiz q-chain | In-order of 5 → 4 → 3 (left chain) is [3, 4, 5]; pre-order is [5, 4, 3]; no error | correct | run |
| l14 | quiz q-decision | A question, then its yes-branch, then its no-branch is pre-order | correct | definition |
| l14 | quiz q-portfolio | Fund, all regions, all desks, all books is level order with a queue; a stack dives deep | correct | BFS versus DFS, CLRS 22.2, 22.3 |
| l14 | quiz q-height | One node has height 0 in links; 1 counts the node | correct | CLRS B.5.2 |
| l15 | screens[0].prose, answer, feedback, explain | BST: left side smaller, right side larger at every node; 60 is found by 50, 70, 60; the left side of 50 is never looked at | correct | CLRS 12.1, 12.2; sim: l15 s0 |
| l15 | screens[1] (all) | Insert walks as a search and puts the node on the `None` link it steps onto; 65 becomes 60's right child; an insert always adds a leaf | correct | CLRS 12.3 TREE-INSERT; sim: l15 s1, s2 |
| l15 | screens[2] (all) | 35 goes left, right, left; 85 right three times; one comparison per level, so the cost is the height | correct | sim: l15 s1, s2; CLRS 12.3 (O(h)) |
| l15 | screens[3].options, why | In-order of the BST is sorted; the other lists are pre, level and post order | correct | sim: l15 s3; CLRS Theorem 12.1 |
| l15 | screens[3].explain | In-order on a BST gives sorted output in O(n) | imprecise | Θ(n) for a walk that appends (CLRS Theorem 12.1); the lesson-14 `inorder` it names joins with `+`. Covered by finding 5 |
| l15 | screens[4].prose, answer, slips | Sorted arrivals 10..50 make a right chain; a search for 50 makes 5 comparisons; 3 is the balanced figure, 4 counts links | correct | sim: l15 s4 |
| l15 | screens[4].explain | Chain height n − 1, so search and insert are O(n); AVL and red-black trees rotate to keep h near log2 n; Python has none built in; `bisect` or `sortedcontainers` | correct | CLRS 12.2, 13.1 (h ≤ 2 lg(n+1)), Problem 13-3 (AVL h = O(lg n)); Python stdlib has no tree map |
| l15 | screens[5].prose | Duplicates are not inserted again, so the tree holds a set | correct | a stated convention, applied in the solution and test 9 |
| l15 | screens[5].widget solution, tests, how, hints | `insert`, `contains`, `min_value` pass 13 tests | correct | sim: widget 5 solution passes |
| l15 | screens[5].feedback.byKey.test-2 | Test 2 checks the shape | misleading | sweep: 0 of 3 shape slips reach test 2; each breaks test 1's in-order first (same input). Finding 12 |
| l15 | screens[5].feedback.byKey.test-6 | Test 6 searches the empty tree | correct | sweep: 2 of 3 fail test 6 first (a recursive `contains` with no `None` case fails test 5) |
| l15 | screens[5].feedback.byKey.test-8 | Test 8's root has no left child | correct | sweep: starting at `root.left` fails test 8 first; a recursion with no base case is another mistake and fails test 7 |
| l15 | screens[5].feedback.byKey.test-9 | Test 9 inserts repeats | correct | sweep: 2 of 2 fail test 9 first |
| l15 | screens[5].feedback.byKey.test-10 | Test 10 (`insert(None, 7)`) is where a missing empty-tree case shows | misleading | sweep: 0 of 3; `bst_from` starts every tree from `None`, so the slip fails test 1. Finding 12 |
| l15 | screens[5].explain | Each function walks one path, O(h); returning `root` lets the caller start from `None`; the minimum is the leftmost node | correct | CLRS 12.2 TREE-MINIMUM |
| l15 | screens[6].prose, answer, feedback | `looks_ok` passes [10, 5, 15, None, None, 6, 20]; 6 breaks the rule (on 10's right, below 10) | correct | sim: l15 s6, s7 |
| l15 | screens[6].explain | "A search for 6 would go right at 10 and never find it" | wrong | 6 < 10, so the search goes left at 10, then right at 5 onto `None`. sim: EXPECTED_FAIL l15 s6 explain. Finding 1 |
| l15 | screens[7].prose, hints | Pass `lo`, `hi` down; going left the node becomes `hi`, going right `lo`; bounds are strict | correct | standard bounds check; CLRS 12.1 BST property with the lesson's no-duplicates rule |
| l15 | screens[7].widget solution, tests, how | `validate_bst` passes 14 tests | correct | sim: widget 7 solution passes |
| l15 | screens[7].feedback.byKey.test-2, test-4, test-6, test-14 | Children-only check; empty tree; equal values; a large-number sentinel | correct | sweep: 1/1, 2/3, 2/2, 2/2 codings fail the named test first |
| l15 | screens[7].explain | Each call carries the tightest ancestor bounds; O(n) | correct | each node visited once |
| l15 | screens[8].prose, summary.formula | cost O(h), floor(log2 n) ≤ h ≤ n − 1; a perfect tree of height h holds 2^(h+1) − 1 nodes | correct | CLRS B.5.3, 12.2; sim: l15 s8 (400 random BSTs) |
| l15 | screens[8].answer, slips, explain | 1,023 = 2^10 − 1, height 9, 10 comparisons; 9 is links, 1,023 a chain, 512 one halving | correct | sim: l15 s8 perfect tree |
| l15 | screens[9].prose, solution, tests, how | Range query by pruned in-order; narrow ranges read at most 40 nodes of 1,023 | correct | sim: widget 9 solution passes |
| l15 | screens[9].hints | If `node.val <= lo`, everything on its left is below `lo` | correct | strict BST property |
| l15 | screens[9].feedback.byKey.test-2 | Test 2 is an empty range: return `[]` | correct | descriptive; sweep: only a `None`-when-empty return reaches it (1 of 3) |
| l15 | screens[9].feedback.byKey.test-9 | Test 9 counts reads; prune both sides | correct | sweep: 2 of 2 unpruned walks fail test 9 first; a read count, not a timing |
| l15 | screens[9].feedback.byKey.test-7 | Test 7: "Check for `None` before reading a node" | misleading | sweep: a missing `None` check fails test 1 (2 of 3); test 7 is reached by treating a node with no left child as a leaf. Finding 13 |
| l15 | screens[9].explain | Pruning reads the in-range nodes plus two paths, about O(h + k); a tick array finds a level in O(1) | correct | CLRS Exercise 12.2-8 style bound; direct addressing, CLRS 11.1 |
| l15 | summary.ideas, trap | Search and insert walk one path; cost is the height; in-order is sorted; validity needs ancestor bounds | correct | as above |
| l15 | quiz q-min | The minimum is the leftmost node; not the lowest leaf, not the root's left child | correct | CLRS 12.2 |
| l15 | quiz q-sorted | 1,000 ascending inserts give height 999; 9 or 10 is the balanced height; 1,000 counts nodes | correct | sim: l15 q-sorted |
| l15 | quiz q-tick | Index `round((price − 90) / 0.01)` finds a level in O(1); many matching engines use arrays by tick | correct | direct addressing, CLRS 11.1; engine practice as in Harris ch. 6 and public exchange design notes (not a quantified claim) |
| l15 | quiz q-bisect options a, b, c | `bisect` on a sorted list; a heap is not sorted; a dict does not keep keys sorted | correct | bisect docs; heapq docs; dicts keep insertion order only |
| l15 | quiz q-bisect option d why | "Call `sort()` after every insert ... costs O(n log n) per insert" | imprecise | the generic comparison-sort bound; CPython's Timsort re-sorts a sorted list plus one item in O(n) (listsort). sim: l15 q-bisect and its EXPECTED_FAIL. Finding 6 |
| l15 | quiz q-bisect explain | `bisect` searches in O(log n); inserting still shifts, O(n); `sortedcontainers` does better for millions | correct | bisect docs (performance notes); sim: l15 q-bisect |
| l16 | screens[0] (all) | Height 3 for [1, 2, 3, 4, 5, None, None, 6]; 4 counts nodes; 1 follows the right side; each node is one more than its taller child | correct | sim: l16 s0, s1 |
| l16 | screens[1].prose, table, feedback | h(v) = 1 + max(h(L), h(R)); `None` must be −1 for a leaf to be 0; 4 is 1, 2 is 2, 1 is 3 | correct | CLRS B.5.2; Weiss convention for the empty tree; sim: l16 s0, s1 |
| l16 | screens[1].explain | Counting nodes instead, `None` is 0 and a leaf 1; either works if kept | correct | sim: l16 q-convention |
| l16 | screens[2] (all) | Best root-to-leaf total 27 via 5, 4, 11, 7; other routes 26 and 22 | correct | sim: l16 s2 |
| l16 | screens[3].prose | Balanced: at every node the two sides' heights differ by at most 1; balanced trees keep searches near log2 n | correct | AVL height balance, CLRS Problem 13-3 (h = O(lg n), about 1.44 lg n) |
| l16 | screens[3].answer, feedback, explain | Only node 2 is lopsided (1 against −1); the root passes with 2 against 1; the check must run at every node | correct | sim: l16 s3 |
| l16 | screens[4].widget solution, tests, hints, explain | `height` with −1 and `size` with 0; both O(n) | correct | sim: widget 4 solution passes |
| l16 | screens[4].feedback.byKey.test-1 | Test 1 is the empty tree, −1 | correct | sweep: 2 of 2 fail test 1 first |
| l16 | screens[4].feedback.byKey.test-2 | "Test 2 ... If you got 1, `None` returned 0 instead of −1" | wrong | `None` → 0 fails test 1 (`height(None)`), so this line never shows for it; the codings that do reach test 2 return −1 for `None` and give a leaf 1 another way. sweep; sim: EXPECTED_FAIL widget 4 test-2. Finding 2 |
| l16 | screens[4].feedback.byKey.test-5 | Test 5 (`size(None)`) is where the base case shows | misleading | sweep: a −1 base or no base fails test 4 (2 of 3); only a child-guarding `size` reaches test 5. Finding 14 |
| l16 | screens[5].prose, options, hints, explain | `height` at every node makes `is_balanced` O(n^2) on a chain: n(n−1)/2, about 500,000 for 1,000; O(n log n) on a balanced tree | correct | sim: l16 s5 (499,500 counted) |
| l16 | screens[6].prose, explain | Return height or a flag from one pass; heights in nodes free −1 as the flag; O(n); with −1 for `None` another flag is needed | correct | standard one-pass check; solution run |
| l16 | screens[6].widget solution, tests, how | Passes 12 tests; test 10 counts `.left`/`.right` reads, at most 6 per node | correct | sim: widget 6 solution passes |
| l16 | screens[6].widget.tests (coverage) | The tests enforce the flag being passed up | misleading | a `check` that never returns −1 on a child's −1 passes all 12 tests yet calls a 4-node chain balanced. sweep (PASS); sim: EXPECTED_FAIL l16 s6 tests. Finding 21 |
| l16 | screens[6].feedback.byKey.test-1, test-5, test-10 | Empty tree; root-only check; a separate `height` per node | correct | sweep: 2/2, 1/2 (the other passes all, finding 21), 2/2; test 10 is a read count, not a timing |
| l16 | screens[7].prose, options, explain | Base, recurse, combine; longest path bending at v is h(L) + h(R) + 2 with h(None) = −1; the diameter is the largest such value | correct | sim: l16 s7 (300 random trees against BFS) |
| l16 | screens[8].prose | A tree of price moves, "like the binomial lattice of the trees course" | correct | analogy only; a binomial lattice recombines, a tree does not, and the screen claims no more than likeness |
| l16 | screens[8].answer, slips, hints, explain | Best route 8 through −5; greedy gives 6; skipping −5 gives 13 | correct | sim: l16 s8 |
| l16 | screens[9].prose, solution, tests, hints | A route ends at a leaf; a missing child is not a route of value 0 | correct | sim: widget 9 solution passes |
| l16 | screens[9].feedback.byKey.test-4, test-1 | `None` as 0 gives 1 on test 4; greedy gives 6 on test 1 | correct | sweep: 2/2 and 1/1 |
| l16 | screens[9].feedback.byKey.test-6 | Test 6 (all negative) is where a best total started at 0 shows | misleading | sweep: 0 of 3; a 0 start fails test 4 (or 3). Finding 17 |
| l16 | screens[9].explain | O(n); the same shape prices a binomial lattice backwards | correct | backward induction is base, recurse, combine (Hull ch. 13) |
| l16 | summary (all) | One convention kept; return what the parent needs; h(v) rule; balanced gap ≤ 1; diameter through v; the O(n^2) trap | correct | as above |
| l16 | quiz q-convention | Shifting every height by 1 leaves every gap, so both conventions give the same verdict | correct | sim: l16 q-convention |
| l16 | quiz q-empty | `is_balanced(None)` is `True`; it is also the base case | correct | vacuous truth; solution |
| l16 | quiz q-diameter | Diameter of [1, 2, 3, 4, 5] is 3; 2 is the height; 4 counts nodes | correct | sim: l16 q-diameter |
| l16 | quiz q-portfolio | With depth = 1 + max over children, a childless position must return 1 for the fund to report 4 | correct | arithmetic |
| l17 | screens[0].prose, answer, feedback | A tree with every parent no larger than its children, stored level by level; 5's children are at indices 3 and 4 | correct | CLRS 6.1 (0-based form); sim: l17 s0, s1 |
| l17 | screens[0].explain | Children of i at 2i + 1 and 2i + 2; a binary heap; the smallest is always at index 0 | correct | heapq docs ("heap[k] <= heap[2*k+1] and heap[k] <= heap[2*k+2]") |
| l17 | screens[1] (all) | Parent of i is (i − 1) // 2; index 5 and 6 both give 2 | correct | CLRS 6.1; sim |
| l17 | screens[2] (all) | Push 4: append, swap with 9, swap with 5, stop under 2; result [2, 4, 3, 5, 6, 7, 8, 9]; sift-up | correct | sim: l17 s2 |
| l17 | screens[2].explain | A push makes at most as many swaps as the tree has levels | correct | an upper bound; the exact bound, levels − 1, is given on screens[4] |
| l17 | screens[3] (all) | Pop: move the last item to the top, swap with the smaller child; result [3, 4, 7, 5, 6, 9, 8]; swapping with the larger child breaks the rule | correct | CLRS 6.2 MIN-HEAPIFY, 6.5; sim: l17 s3 |
| l17 | screens[4].prose | "Level d of a heap holds 2^d items", so n items have floor(log2 n) + 1 levels | imprecise | only full levels hold 2^d; the last may hold fewer (the screen's own 8-item heap has 1 item on level 3). The level count is right, CLRS Exercise 6.1-2. sim: EXPECTED_FAIL l17 s4 prose. Finding 7 |
| l17 | screens[4].answer, slips, explain | A million items: 20 levels, at most 19 swaps; push and pop are O(log n) | correct | sim: l17 s4, s7; CLRS 6.5 |
| l17 | screens[5].prose, solution, tests, how, hints, explain | `push` and `pop` on a list; popping the last item leaves nothing to move; moving the last item keeps the list packed | correct | sim: widget 5 solution passes |
| l17 | screens[5].feedback.byKey.test-1, test-4, test-11 | One swap only; first child not smaller child; `heapq` used | correct | sweep: 2/2, 2/2, 1/1 |
| l17 | screens[5].feedback.byKey.test-6 | Test 6 (pop the only item) is where writing to index 0 of the emptied list shows | misleading | sweep: 0 of 3; test 5 drains a heap to empty first, so the slip fails test 5. Finding 18 |
| l17 | screens[6] (all) | Negated pushes with pop at size > 3 leave 45, 60, 80; `heapq` is a min-heap; to keep the k largest store them plain and pop the smallest | correct | sim: l17 s6; heapq docs |
| l17 | screens[7].prose | peek O(1); push, pop O(log n); top k of n O(n log k); popping all n is heapsort, O(n log n) | correct | CLRS 6.4, 6.5; sim: l17 s7 |
| l17 | screens[7].prose | "Sorting after every update costs O(n log n) each time" | imprecise | generic bound; CPython re-sorts a nearly sorted list in O(n). Finding 6 |
| l17 | screens[7].options, explain | A heap of 10 has floor(log2 10) = 3 levels to climb; O(n log k) overall | correct | sim: l17 s4, s7 |
| l17 | screens[8] (all) | `(price, time, id)` tuples compare by the first item, then the next; A3 is on top; price-time priority | correct | LangRef 6.10.1; heapq docs; Harris ch. 6; sim: l17 s8 |
| l17 | screens[9].prose, solution, tests, how, hints | Min-heap of at most k; `heapreplace` pops and pushes in one step; test 11 measures peak memory | correct | heapq docs; sim: widget 9 solution passes |
| l17 | screens[9].feedback.byKey.test-1, test-3, test-10 | Smallest three; k = 0; an iterator | correct | sweep: 2/2, 1/2 (the other coding is correct code), 2/2 |
| l17 | screens[9].feedback.byKey.test-4 | "Replace only when a value is strictly larger than `h[0]`, and keep duplicates" | misleading | replacing on `>=` passes every test; only dropping repeats fails test 4. sweep. Finding 19 |
| l17 | screens[9].explain | One comparison per value and sometimes an O(log k) replace; `heapq.nlargest(k, xs)` does the same | correct | `Lib/heapq.py` nlargest; sim: l17 s9 |
| l17 | summary (all) | Index rules; push sifts up, pop sifts down; min-heap of size k is O(n log k); store −x for a max-heap; negating flips what you keep | correct | as above |
| l17 | quiz q-parent | Parent of 10 is 4; 10 // 2 is the 1-based rule; 21 is a child | correct | CLRS 6.1 (1-based PARENT(i) = floor(i/2)) |
| l17 | quiz q-max options a, b, c | Push −price and negate on the way out; `heap[-1]` is only a leaf, the largest can be at any leaf | correct | CLRS Exercise 6.1-4 analogue |
| l17 | quiz q-max option d why | Sorting in reverse after each push "costs O(n log n) per push" | imprecise | generic bound; finding 6 |
| l17 | quiz q-bigk | `top_k([4, 1], 5)` is [4, 1] | correct | solution; `heapq.nlargest` agrees |
| l17 | quiz q-sorted | `sorted(seen)[0]` per arrival is about n^2 log n in all; heap pushes about n log n | correct | `seen` is in arrival order, so each sort is a true n log n; n pushes are O(n log n) worst case (about linear on random arrivals). sim: l17 q-sorted (two checks) |
| l18 | screens[0] (all) | Bids and asks; a buyer takes the lowest ask, a seller the highest bid; best bid £100.00, best ask £100.02, spread £0.02 | correct | Harris ch. 6 |
| l18 | screens[0].explain | A max-heap of bids and a min-heap of asks | correct | CLRS 6.5 |
| l18 | screens[1] (all) | Negate the price only; `bids[0]` is (−100.0, 1, "B1"); best bid −bids[0][0] in O(1) | correct | sim: l18 s1 |
| l18 | screens[2] (all) | Quote table after add A4, cancel B1, add B4, cancel A4 | correct | sim: l18 s2 |
| l18 | screens[3] (all) | Buy 500 at £100.03 takes 200 at £100.02 and 300 at £100.03, £50,013; 100 left; each fill at the resting order's price | correct | sim: l18 s3; Harris ch. 6 discriminatory pricing rule |
| l18 | screens[4] (all) | Same price: earlier order fills first; A1 200, A5 50; time second in the tuple | correct | sim: l18 s4 |
| l18 | screens[5].options, why | Lazy deletion; `remove` from the middle breaks the heap and is O(n); remove plus `heapify` is correct but O(n) per cancel; most orders on a busy book are cancelled | correct | heapq docs, "Priority Queue Implementation Notes" (mark as removed); CLRS 6.3 |
| l18 | screens[5].explain | Cancel is O(1); reads drop dead entries off the top; each entry is popped at most once | correct | sim: l18 s7, q-amortised |
| l18 | screens[6] (all) | A `best_bid` that never reads `cancelled` returns the stale £100.00; fix with a `while` pop before reading; `match` must skip too | correct | traced |
| l18 | screens[7].prose | "With n live entries: add O(log n), cancel O(1), best O(1) amortised, each fill O(log n)" | imprecise | the costs hold with n = entries in the heap, dead ones included; dead entries below the top stay, so the heap is not bounded by the live count. The O(1) amortised read is right when each pop is charged to its push (CLRS 17.1). sim: EXPECTED_FAIL l18 s7 prose. Finding 8 |
| l18 | screens[7].answer, slips, explain | At most 900,000 dead pops; 1,000,000 counts adds; 9 × 10^11 is the product | correct | sim: l18 s7, q-amortised |
| l18 | screens[8].options a, b, c, explain | Real engines add arrays by tick with FIFO queues, an id map, self-match prevention | correct | exchange practice (self-match prevention is a published exchange feature); no figure is claimed beyond "millions of messages a second", an order of magnitude |
| l18 | screens[8].options[3].why, feedback.byKey.d | Re-sorting the whole book "costs O(n log n) per message" | imprecise | generic bound; finding 6 |
| l18 | screens[8].options[4].why | "Fills happen at the resting order's price. That is part of the price-time rule" | imprecise | price-time priority orders who trades first; the trade price is a separate rule (Harris ch. 6 treats precedence rules and pricing rules apart). Finding 23 |
| l18 | screens[9].prose, solution, tests, how, hints | `OrderBook`: two heaps and a dict; fills at the earlier order's price; 12 tests | correct | sim: widget 9 solution passes |
| l18 | screens[9].widget.tests (coverage) | The tests enforce time priority | misleading | a book with `(price, order_id)` tuples and no time passes all 12 tests, because every test names orders in arrival order. sweep (PASS); sim: EXPECTED_FAIL l18 s9 tests. Finding 4 |
| l18 | screens[9].feedback.byKey.test-1, test-3, test-5, test-6, test-7 | Empty book; stale quote after a cancel; tie at one price; fill at the resting £100.05; `match` skipping dead entries | correct | sweep: 2/2, 1/1, 2/3 (the third passes all, finding 4), 1/3 (the named slip, seller's price, matches; bid price and midpoint are other slips and fail test 4), 2/2 |
| l18 | screens[9].explain | Test 11: B3 sweeps A1 and A3 at £100.02 and part of A2; A4 sells into B2 at £99.99, the resting price | correct | run of the solution on test 11 |
| l18 | summary (all) | Two heaps; match while bid ≥ ask; lazy cancel; costs; stale-quote trap | correct | as above; the cost line shares finding 8's n |
| l18 | quiz q-empty | An empty side quotes `None`, not 0.0 | correct | solution |
| l18 | quiz q-negate | `(-price, time, order_id)`; negating time puts the latest first | correct | sweep: negated time fails test 5 |
| l18 | quiz q-price | A buy at £100.05 crossing a resting sell at £100.02 trades at £100.02, a £0.03 improvement | correct | sim: l18 q-price; Harris ch. 6 |
| l18 | quiz q-amortised options a, b, explain, feedback | Each dead entry is popped once, so reads average out; O(log n) per dead entry, once | correct | sim: l18 s7, q-amortised; CLRS 17.1 |
| l18 | quiz q-amortised option c why | "Dead entries leave as soon as they reach the top, and each was pushed once" (so the heap does not grow without limit) | imprecise | bounded by total adds, yes, but entries cancelled below the top never reach it and stay; the script's run ends with 3,921 heap entries for 418 live bids. Finding 8 |
| r4 | r4-post | Post-order 4, 2, 5, 3, 1; the others are pre-order and in-order | correct | run on the canvas tree |
| r4 | r4-insert | 55 goes right, left, right to become 50's right child | correct | traced |
| r4 | r4-height | Height 3; 4 counts nodes or uses 0 for `None` | correct | sim: review-4 r4-height |
| r4 | r4-push key, options b, c | Push 1 onto [3, 5, 4, 9, 6] gives [1, 5, 3, 9, 6, 4]; sorted list and one-swap list are slips | correct | sim: review-4 r4-push key |
| r4 | r4-push option d why | [1, 3, 5, 9, 6, 4]: "You swapped 1 with index 1" | wrong | that slip gives [1, 3, 4, 9, 6, 5]; the option is the key with indices 1 and 2 exchanged. sim: EXPECTED_FAIL review-4 r4-push. Finding 15 |
| r4 | r4-quotes | Spread £0.04; 0.01 uses the cancelled quotes; 0.05 uses B2 | correct | sim: review-4 r4-quotes |
| r4 | r4-valid key, options why | [8, 3, 10, 1, 6, None, 14] is the only BST; 9 under 3, 7 under 10, repeated 3 | correct | sim: review-4 r4-valid |
| r4 | r4-valid explain | "The others each hide one node that passes its parent but fails an ancestor" | imprecise | option d's repeated 3 fails against its own parent. sim: EXPECTED_FAIL review-4 r4-valid. Finding 16 |
| r4 | r4-topk | O(n log 20), which is O(n) for fixed 20 | correct | sim: l17 s7 |
| r4 | r4-sweep | Seller receives £59,995; 59,988 prices at the limit; 60,000 at the best bid; 300 stay bid | correct | sim: review-4 r4-sweep |
| r4 | r4-diameter | Diameter 4 (5, 3, 2, 4, 6); through the root 3; 5 counts nodes | correct | sim: l16 q-diameter and review-4 r4-diameter |
| h4 | h4-kth prose, solution, tests, explain | k-th smallest by an in-order walk that stops; reads about h + k nodes | correct | sim: widget 0 solution passes; CLRS 12.1 |
| h4 | h4-kth feedback.byKey.test-8 | A full in-order list reads all 1,023 | correct | sweep: 2 of 2 fail test 8 first; a read count |
| h4 | h4-merge prose, how | "Sorting everything again costs O(N log N)"; "re-sorting everything ignores that each list is already sorted"; heap merge O(N log k) | imprecise | the heap bound is right (CLRS Exercise 6.5-9). CPython's sort does not ignore the runs: it merges k presorted runs in about N log2 k comparisons (listsort). sim: EXPECTED_FAIL homework-4 h4-merge (182,308 comparisons against the heap's 229,354). Finding 6 |
| h4 | h4-merge solution, tests, explain | `(value, list index, position)`; the index breaks ties; the heap never holds more than k | correct | sim: h4-merge equals the sorted concatenation |
| h4 | h4-merge feedback.byKey.test-3, test-4 | Only empty lists; repeats across lists | correct | sweep: 1/1, 2/2 |
| h4 | h4-median prose, solution, tests, explain | Lower half in a max-heap, upper half in a min-heap, sizes equal or lower one larger; odd count: lower top; even: mean of tops; O(log n) per step | correct | sim: h4-median equals statistics.median on every prefix |
| h4 | h4-median feedback.byKey.test-1 | Even case: mean of the two tops | correct | sweep: 1/1 |
| h4 | h4-median feedback.byKey.test-7 | Test 7 (negatives) is where a missing negation on the lower heap shows | misleading | sweep: 1 of 4; reading `lo[0]` unnegated fails test 1; only `abs(lo[0])` reaches test 7. Finding 20 |
| h4 | h4-match-order | Clean tops, check, price and quantity (either order), record and reduce, mark finished | correct | matches the l18 solution's loop |
| h4 | h4-dict-tuple | A price tie makes `heapq` compare the dicts, which raises `TypeError`; put a time or counter second | correct | sim: h4-dict-tuple; LangRef 6.10.1; heapq docs implementation notes |
| h4 | h4-leaves key, slip, feedback | A heap of 100 has 50 leaves, indices 50 to 99; index 49 has a child at 99 | correct | sim: h4-leaves; CLRS Exercise 6.1-7 |
| h4 | h4-leaves explain | "That is why sift-down from the middle builds a heap in O(n)" | imprecise | leaves being half is why the build can start at the middle; the O(n) bound comes from most nodes being near the bottom (CLRS 6.3). Heapify O(n) against n pushes O(n log n) checked: sim: h4-leaves explain. Finding 22 |
| h4 | h4-design model, rubric, explain | Costs of sorted list, balanced BST, two heaps with lazy deletion, array by tick; 2,001 slots for £90 to £110 at £0.01; dead entries use memory until they reach the top | correct | bisect docs; CLRS 13, 6.5, 11.1; (110 − 90)/0.01 + 1 = 2,001 |
| h4 | h4-save-tree prose, solution, tests, explain | Pre-order with `#` for every empty child fixes the shape; one iterator reads it back; O(n) | correct | sim: widget 7 solution passes |
| h4 | h4-save-tree feedback.byKey.test-2, test-3, test-5 | Empty tree is `'#'`; reading position kept inside the call and `int` values; multi-digit, negative and 0 tokens | correct | sweep: 2/2, 2/2, 3/3 |
| all | recursion depth | No test recurses deeper than a 300-node chain (l16 screens[6] test 11); the page limit is 3,000 | correct | tests read; `sys.setrecursionlimit(3000)` in drill-worker.js; all solutions ran under Pyodide in the sweep |
| all | timing | No `test-N` line depends on a time limit; three count reads instead (l15 s9 test 9, l16 s6 test 10, h4-kth test 8) | correct | sweep: no solution or named-mistake coding timed out (one unnatural coding looped) |

Rows: 180. Verdicts: correct 149, wrong 4, imprecise 14, misleading 13, unverified 0.

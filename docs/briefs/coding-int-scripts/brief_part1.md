
## Level 1

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `coding-int` (topic 3.5), level 1 ("Patterns still to learn"): lessons `l1-merging-intervals`, `l2-prefix-trees`, `l3-window-maximum`, `l4-top-k`, `l5-bit-tricks`, plus `review-1.json` and `homework-1.json`, in `app/content/courses/coding-int/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids of `course.json` exactly (`ci-patterns` on every lesson). Use £ for money. Scripts: `l1.py` (merge, trie, completions, window, k-th, running median, bits, numbers), `l_extra.py` (overlapping pairs, free gaps, top-k frequent, window median), `harness.py`.

Level promise. The learner meets five patterns that interviews ask and the earlier courses leave out or only touch: merging intervals, tries, windows whose condition is not a sum, heaps for frequency and streams, and bit tricks. Each lesson is a method, three or four problems, a trap and a transfer; Python by default, with C++ twins in l1 and l4.

**Engine features.** E3, E8, E11 and E14 are not needed in level 1. Existing: `code` (Python and C++), `number-line` with `intervals` and `tapIntervals`, `array` in queue mode with `pointers` and `cells` labels (a deque of indices and values), `tree` for tries, `manipulate`, `order`, `tap-regions`, `table`.

**Builds on (by id) and what is new.**

| Lesson | Builds on | New over those |
| --- | --- | --- |
| l1-merging-intervals | `algo-think` l11-sorting-by-hand, `contests` l10-greedy-proofs ("How many rooms?"), `contests` l12-difference-arrays | Sort by start, one pass keeping the last end, the touching rule; counting overlapping pairs by a sweep (the rooms count is cited, not set). |
| l2-prefix-trees | `ds` l14-binary-trees (nodes and children), `ds` l4-frequencies (dict of counts) | The trie: a dict of children per node, end marks, prefix counts, completions in alphabetical order. Nothing in the app teaches it. |
| l3-window-maximum | `ds` l11-first-in-first-out (window maximum with a deque), `ds` l10-next-greater, `ds` l6-sliding-window, `ds` l7-prefix-sums | One recap run; then windows judged by max minus min (two deques) and by sums with negatives (a deque of prefix sums, in homework). |
| l4-top-k | `ds` l17-always-the-smallest, `ds` homework-4 h4-median, `algo-think` homework-3 h-kth-largest, `cpp` l15-maps | Counting then a size-k heap with a two-key order; the C++ `priority_queue` comparator trap; a streaming k-th largest. |
| l5-bit-tricks | `contests` l11-bitmasks, `ds` l3-two-sum | XOR cancelling pairs, `n & (n - 1)`, `n & -n`, counting bits by a recurrence, and splitting two singles by a set bit. |

### l1-merging-intervals (14 min; tags `intervals-merge`, `intervals-sweep`)

Objective (`course.json`): Sort and merge intervals, and count overlaps with a sweep. Method stated after use: sort by start; keep the last merged interval; if the next start is at most its end, extend the end to the larger of the two ends, else start a new one. Intervals here are closed on both ends and written `[start, end]` unless a screen says half-open; a half-open `[start, end)` interval touching another does not overlap it (the meeting-room convention, cited from `contests` l10).

Screens (10):
1. Hook `problem`, `number-line` with five `intervals` `[1,5]`, `[2,3]`, `[4,8]`, `[10,12]`, `[11,15]` and `tapIntervals: true`; `tap-regions`: "Tap every interval that ends up in the same block as `[1, 5]`." Answer `[1,5]`, `[2,3]`, `[4,8]`. Explain: the blocks are `[1, 8]` and `[10, 15]`.
2. `explore`, same canvas with the last interval `[p, 15]` and a draggable `p`; `numeric`: the largest whole `p` at which the last two blocks still join: 12 (a start of 12 touches the end of `[10, 12]`; 13 leaves a gap). Both checked by listing blocks.
3. `ladder`, `choice`: the five intervals given in the order `[8,10]`, `[1,3]`, `[2,6]`: what does a single pass without sorting return? `[[8,10],[1,6]]`, a wrong answer; the right answer needs the sort first.
4. `ladder`, `choice` (touching rule): `[1,4]` and `[4,5]` merge when closed. For a meeting list `[0,10]`, `[10,20]` the rule is half-open and they do not overlap.
5. `problem`, code A, Python `merge_intervals` (below), `pace` 600.
6. `ladder`, code A in C++ (same tests).
7. `trap`, `choice`: `[[1,10],[2,3],[4,5]]`: the learner who sets the end to the next interval's end returns `[[1,5]]`; the right output is `[[1,10]]`. The `byKey` line names the action ("You copied the last end instead of keeping the larger").
8. `generalise`: the pattern as fenced code; `derive`: `order` the five steps of merge (sort, start with the first, compare start with last end, extend with max or append, return), with the distractor "compare the end of the new interval with the last end" and its `why`.
9. `transfer`, code B, Python `count_overlapping_pairs` (half-open sweep: events `(time, +1)` and `(time, -1)`, the end sorting first at equal times, add the current active count at each start). Framing: "Two orders rest in the book over the same moment: how many pairs of overlapping resting orders are there?" Cite `contests` l10 for the room count.
10. `transfer`, `table` widget: a four-row table of orders (start, end, active count when it starts) the learner fills for `[[1,4],[2,6],[5,9],[8,10]]`: active counts 0, 1, 1, 1 and a total of 3 pairs, matching the test.

Quiz (4): blocks of a list of intervals; a touching case; the cost of sorting `n = 1,000,000` intervals (about 19.9 million comparisons, computed below); pairs counted by a sweep against the double loop at `n = 100,000` (the loop makes 4,999,950,000 pair checks, the sweep about 200,000 events after the sort).

**Problem 1.1** `merge_intervals(intervals)`; Python and C++ twin; difficulty 3. Statement: "Intervals `[start, end]` with whole numbers, in any order, may overlap or touch. Return the merged list, sorted by start, as lists. Two intervals that share an end point merge." Reference (Python), starter, tests:

@@PY:l1:MERGE_REF@@

Starter (fails 6 of 10: it only sorts):

@@PY:l1:MERGE_START@@

@@T:l1:merge@@

C++ twin (same ten cases, `call: "merge_intervals"`, `args: [[[1,3],[2,6],[8,10],[15,18]]]`, `types: ["std::vector<std::vector<int>>"]`, `expect` the same nested lists; the empty case is `args: [[]]` with the type given). Reference and starter (starter only sorts, fails 6 of 10); both compiled and run under `-std=c++17` and `-std=c++20`:

@@CPP:l1:MERGE_CPP_REF@@

@@CPP:l1:MERGE_CPP_START@@

**Problem 1.2** `count_overlapping_pairs(intervals)`; Python; difficulty 3. Statement: "Half-open intervals `[start, end)`, `start < end`, whole numbers, any order. Return how many pairs of intervals overlap. Touching ends do not overlap." Reference:

@@PY:lx:CP_REF@@

Starter returns 0, fails 5 of 8 (the three zero cases pass):

@@PY:lx:CP_START@@

@@T:lx:cp@@

Checks: brute double loop on 3,000 random lists; the last case also checks the closed form: `n` intervals `[i, i + 3)` give `(n - 1) + (n - 2)` pairs, which is 199,997 at `n = 100,000`.

### l2-prefix-trees (14 min; tags `trie`, `prefix-count`, `autocomplete`)

Objective: Build a trie and use it for prefix search and word lookups. Method stated after use: each node holds a dict from a letter to a child and a flag that a word ends here; to insert, walk letter by letter and create what is missing; to search, walk and check the flag; to test a prefix, walk and only check that you arrived.

Screens (10):
1. Hook `problem`, `tree` with `nodes` for the words `tea`, `ten`, `to`, `inn` (letters on the branches, end nodes shaded); `numeric`: "How many nodes are there, not counting the root?" Answer 8 (computed by inserting and by counting distinct prefixes).
2. `explore`, same `tree`, a control stepping through the inserts; `tap-regions`: tap the nodes that exist after inserting `tea`, `ten` (answer `t`, `te`, `tea`, `ten`).
3. `ladder`, `choice`: search `te` after the four inserts: `False` (the node exists but is not a word end); `starts_with("te")`: `True`.
4. `ladder`, `numeric`: with 1,000 words of length 10 and no shared prefixes there are at most 10,000 nodes besides the root (answer 10,000); the same words in a list of strings cost 1,000 words but each search compares up to 1,000 words.
5. `problem`, code A, `Trie` (below).
6. `ladder`, `choice`: how a prefix count is kept (a counter on each node, incremented once per new word); the learner who counts on a repeated insert gets 2 for `inn` inserted twice; the answer is 1.
7. `trap`, `choice`: `search("app")` after only `apple` is inserted; the learner returns `True`. Right answer `False`.
8. `generalise` (the pattern in code) and `derive` (`order`: walk, create missing child, mark end, increment counts only for a new word).
9. `transfer`, code B, `top_completions` (desk story: an order-entry box that suggests the first `k` symbols with a typed prefix, alphabetical).
10. `transfer`, `choice`: when a trie loses to a sorted list with `bisect` (a few thousand symbols, prefix queries only, memory tight).

**Problem 2.1** `Trie` class with `insert(word)`, `search(word)`, `starts_with(prefix)`, `count_prefix(prefix)`; Python; difficulty 3. Statement: "`count_prefix` returns how many distinct inserted words start with the prefix; inserting a word twice counts once; the empty prefix counts every word." Driver and tests go through `run_trie(ops)` with `ops` lists of `(operation, text)` pairs; the driver returns the results of every operation except `insert`.

@@PY:l1:TRIE_REF@@

Hidden driver (`postlude`):

@@PY:l1:TRIE_POST@@

Starter (insert does nothing, queries return `False` or 0; fails 5 of 6):

@@PY:l1:TRIE_START@@

@@T:l1:trie@@

**Problem 2.2** `top_completions(words, prefix, k)`; Python; difficulty 3. Statement: "Return the `k` alphabetically smallest distinct words that start with `prefix`; fewer if fewer exist; an empty list for no match or `k = 0`." Reference (trie plus alphabetical depth-first search that stops at `k`):

@@PY:l1:TC_REF@@

Starter (first `k` matches in input order; fails 2 of 8, the cases where the input is not alphabetical or has duplicates):

@@PY:l1:TC_START@@

@@T:l1:tc@@

### l3-window-maximum (13 min; tags `monotonic-deque`, `window-range`)

Objective: Keep a monotonic deque to find every window's maximum in linear time. This is not new in method (`ds` l11); the lesson is about what the deque answers when the window is not a fixed width. Method stated after use: one deque of indices whose values fall as you go keeps the maximum; a second one whose values rise keeps the minimum; the window is valid while the front maximum minus the front minimum is within the limit, and the left end moves right until it is.

Screens (9):
1. Hook `problem`, `array` (queue mode, cells `[1, 3, -1, -3, 5, 3, 6, 7]` with labels for the index, pointers for the window `k = 3`), `manipulate` run of the deque (the recap; cite `ds` l11): the learner replays the deque after each index. Last state after index 4 holds one index, `4` (the 5 beats everything).
2. `numeric`: the window maxima sum to 29 (`3, 3, 5, 5, 6, 7`); computed by the deque and by `max` of each slice.
3. `ladder`, `choice`: "How long is the longest run in which the biggest and smallest differ by at most 4?" for `[8, 2, 4, 7]`: 2. One deque cannot answer it: why.
4. `explore`, `array` with two pointer rows, a `max` deque and a `min` deque as two `array` queue canvases in a `pair`; the learner moves `right` and watches the fronts.
5. `problem`, code A, `longest_within_limit` (below), `pace` 720.
6. `ladder`, `numeric`: pushes and pops on `n = 100,000` values: 100,000 pushes and at most 100,000 pops per deque, so at most 400,000 deque operations for the two deques (answer 400,000; the naive recomputation of every window maximum with a window of 50,000 does 2,500,050,000 comparisons, `(100,000 - 50,000 + 1) * 50,000`, offered as a `choice` of four magnitudes).
7. `trap`, `choice`: on `[4, 2, 2, 2, 4, 4, 2, 2]` with `limit = 0`: a deque that pops only strictly smaller values (`<`) keeps equal values and the front index goes stale; the learner who writes `<` gets a window of 4; the right answer is 3. The `byKey` line names the action ("You kept equal values in the deque").
8. `generalise` + `derive` (`order`: move right, pop the max deque from the back while smaller or equal, same for min, shrink while the range is too big, record the length).
9. `transfer`, `choice`: "A signal desk wants the longest stretch of ticks in which the price stayed within 5 pence of itself." Which structure? Two deques. Then a `numeric` for the stretch in the visible example. (The homework item `shortest_at_least` extends the same idea to prefix sums with negatives.)

Quiz (4): the deque after an index; why `<=` pops equals; the cost; a window query on a new list (keyed by the agent, computed twice).

**Problem 3.1** `longest_within_limit(nums, limit)`; Python; difficulty 4. Statement: "Return the length of the longest contiguous run of `nums` in which the largest value minus the smallest is at most `limit`; 0 for an empty list." Reference (two deques), starter (returns 1 for a non-empty list; fails 9 of 11), tests (the last four use 100,000 values; a quadratic solution stops at the first of them):

@@PY:l1:LW_REF@@

@@PY:l1:LW_START@@

@@T:l1:lw@@

### l4-top-k (14 min; tags `heap-top-k`, `heap-comparator`, `stream-kth`)

Objective: Use a size-k heap and two heaps for top-k and streaming medians. Method stated after use: to keep the `k` largest, hold a min-heap of size `k` and pop whenever it grows to `k + 1`; the top of the heap is the `k`-th largest. To rank by frequency then alphabet, count first, then keep the best `k` by a two-part key.

Screens (11):
1. Hook `problem`, `table` canvas of eight words with counts; `tap-regions`: tap the three words a "most traded" panel shows when ties break alphabetically; answer given by the counts in the example (the agent chooses counts and checks them twice).
2. `ladder`, `numeric`: after reading a stream of ten trade sizes with a heap of size 3, how many pushes and pops (10 pushes, 7 pops).
3. `ladder`, `choice`: the heap keeps the 3 largest: min-heap or max-heap? Min-heap, so that the smallest of the three is the one to drop.
4. `problem`, code A, `top_k_frequent` (Python), `pace` 600.
5. `ladder`, code A in C++ (`std::priority_queue` with a comparator; the same eight tests). The comparator trap is shown: `priority_queue` pops the largest by its comparator, so a size-k heap of the worst needs the reverse order.
6. `trap`, `choice`: ties. The learner who sorts only by count returns `['i', 'love']` on one input and a different list when the dict order changes; the right order is count descending then word ascending.
7. `problem`, code B, `kth_largest_stream` (Python), difficulty 3.
8. `ladder`, `array` canvases showing two heaps (`tree`) for a running median of `[7, 3, 9, 1, 8, 2]` (the learner built this in `ds` homework-4 h4-median; cite it): medians `7, 5, 7, 5, 7, 5`, sum 36 (computed by the heaps and by `statistics.median`); heap sizes after 11 values are 6 and 5.
9. `generalise` + `derive`.
10. `transfer`, `choice`: "A risk screen shows the median of the last 500 trades" asks which structure: two heaps with lazy deletion (the homework item), not a sorted list rebuilt each time.
11. `transfer`, `numeric`: sorting 100,000 values per query against a size-10 heap visits the same 100,000 values per query; the maintained top-10 touches 10 per update (the numbers are in homework item 8 of level 4; here only the ratio of cost per update: sort `n log n` against `log k`).

**Problem 4.1** `top_k_frequent(words, k)`; Python and C++; difficulty 4. Statement: "Return the `k` most frequent words, most frequent first; words with equal counts in alphabetical order; fewer than `k` if there are fewer distinct words." Python reference, starter (first `k` distinct words in input order; fails 2 of 7), tests (the last has 50,000 words, 1,000 distinct, 50 each, so the answer is the first three alphabetically):

@@PY:lx:TK_REF@@

@@PY:lx:TK_START@@

@@T:lx:tk@@

C++ twin (signature `std::vector<std::string> top_k_frequent(std::vector<std::string> words, int k)`; the same seven cases with `args` and `types: ["std::vector<std::string>", "int"]`; the large case built in `setup`): reference with a `priority_queue` and a comparator, starter (the first `k` keys of an `unordered_map`, fails 4 of 7). Compiled and run on all seven cases.

@@CPP:l4:TKF_REF@@

@@CPP:l4:TKF_START@@

**Problem 4.2** `kth_largest_stream(k, initial, adds)`; Python; difficulty 3. Statement: "Start with the numbers in `initial`. After each number in `adds` is added, record the `k`-th largest of everything so far (the largest is the first). Every call has at least `k` numbers after the first add." Reference (size-k min-heap), starter (returns the maximum so far; fails 5 of 6), tests (the last has 31,000 numbers and checks the sum, expected value from an independent `bisect` insertion):

@@PY:l1:KL_REF@@

@@PY:l1:KL_START@@

@@T:l1:kl@@

### l5-bit-tricks (12 min; tags `bit-xor`, `bit-count`, `bit-lowest`)

Objective: Use XOR, masks and shifts for the classic bit problems. Method stated after use: `x ^ x = 0` and `x ^ 0 = x`, so XOR cancels pairs in any order; `n & (n - 1)` clears the lowest set bit; `n & -n` isolates it; `n >> 1` halves.

Screens (10):
1. Hook `problem`, `array` of eight numbers written in binary; `numeric`: the XOR of `[4, 1, 2, 1, 2]` is 4 (the learner tries pairing by hand).
2. `explore`, a `table` of two numbers and their XOR, AND and OR in binary; `choice`: which operation cancels equal values.
3. `ladder`, `numeric`: `44 & 43 = 40` (binary `101100 & 101011 = 101000`); how many times `n &= n - 1` runs before 44 reaches 0: 3.
4. `problem`, code A, `single_number`, `pace` 480.
5. `ladder`, `numeric`: `12 & -12 = 4` and `40 & -40 = 8` (two's complement: the lowest set bit).
6. `trap`, `choice`: "Every value appears three times except one: `[2, 2, 2, 7, 7, 7, 5]`. Does XOR still find the single?" XOR gives 0 (`2 ^ 7 ^ 5 = 0`, since three equal values leave one copy), so the right answer is no: count bits modulo 3 or use a `Counter`. Name the learner's action in `byKey` ("You assumed XOR cancels any repeat").
7. `problem`, code B, `count_bits`: the recurrence `bits[i] = bits[i >> 1] + (i & 1)`.
8. `generalise` + `derive`.
9. `transfer`, `choice`: "A feed sends each message twice except one; find the lost partner" (XOR in O(n) time and O(1) memory against a `Counter` in O(n) memory).
10. `transfer`, `numeric`: total set bits in 0 to 15 is 32 (each of 4 bits is set in 8 of 16 numbers), computed by counting and by the formula.

**Problem 5.1** `single_number(nums)`; Python; difficulty 2. Statement: "Every number appears twice except one that appears once; return it. Numbers may be negative; the list has odd length." Reference, starter (returns `sum(nums)`; fails 5 of 7), tests (the last has 199,999 values):

@@PY:l1:SN_REF@@

@@PY:l1:SN_START@@

@@T:l1:sn@@

**Problem 5.2** `count_bits(n)`; Python; difficulty 3. Statement: "Return a list of length `n + 1` whose `i`-th entry is the number of 1 bits in `i`; in `O(n)` time, without calling a bit-count function." Reference, starter (all zeros; fails 7 of 8):

@@PY:l1:CB_REF@@

@@PY:l1:CB_START@@

@@T:l1:cb@@

### Level 1 review (`review-1.json`, 10 items, difficulty 2 to 4, interleaving all five lessons, every case unseen in the lessons, each with `tags` and `skills`)

Every numeric answer below was computed twice (`numbers_check.py`: two independent methods each).

| # | Lesson | Widget | d | Prompt (summary) | Key |
| --- | --- | --- | --- | --- | --- |
| 1 | l1 | `numeric` | 2 | How many blocks do `[1,3]`, `[2,4]`, `[6,8]`, `[10,12]`, `[11,15]`, `[20,21]` merge into? | 4 (`[1,4]`, `[6,8]`, `[10,15]`, `[20,21]`; by merging and by marking half-unit points) |
| 2 | l1 | `numeric` | 3 | How many pairs of the same six intervals overlap, read as half-open? | 2 (`[1,3)` with `[2,4)`, and `[10,12)` with `[11,15)`; by a sweep and by the double loop) |
| 3 | l2 | `numeric` | 2 | Nodes (not counting the root) of the trie of `car`, `card`, `care`, `cat`, `dog`. | 9 (by inserting and by counting distinct prefixes) |
| 4 | l2 | `numeric` | 3 | After inserting `car`, `card`, `care`, `cat`, `dog`, `car`, what does `count_prefix("car")` return? | 3 (`car`, `card`, `care`; the repeat counts once) |
| 5 | l3 | `numeric` | 3 | Window maxima of `[4,2,12,3,8,5,1,7]` with `k = 3`, summed. | 59 (`12, 12, 12, 8, 8, 7`; by the deque and by `max` of each slice) |
| 6 | l3 | `numeric` | 3 | How many indices does the deque hold after processing index 5 of the same list? | 2 (indices 4 and 5, values 8 and 5; by the trace and by listing which indices in the window can still win) |
| 7 | l4 | `numeric` | 3 | `kth_largest_stream(3, [4,5,8,2], [3,5,10,9,4])`: sum of the five answers. | 30 (`4, 5, 5, 8, 8`) |
| 8 | l4 | `choice` | 3 | To keep the 3 largest of a stream, which heap, and when do you pop? | A min-heap; pop when its size reaches 4. Distractors: max-heap of size 3, a sorted list re-sorted each step. |
| 9 | l5 | `numeric` | 2 | `108 & 107`. | 104 (`1101100 & 1101011 = 1101000`) |
| 10 | l5 | `numeric` | 3 | XOR of `[9, 14, 9, 3, 14]`. | 3 |

### Level 1 homework (`homework-1.json`, 9 items, difficulty 3 to 5 with at least one 5, `tags` on each; four `code` items, one `longform`)

| # | Lesson | Kind | d | Item | Key or reference |
| --- | --- | --- | --- | --- | --- |
| 1 | l1 | `code` | 3 | `free_gaps(busy, start, end)` (below). | tests below |
| 2 | l5 | `code` | 4 | `two_singles(nums)` (below). | tests below |
| 3 | l3 | `code` | 5 | `shortest_at_least(nums, k)` (below). | tests below |
| 4 | l4 | `code` | 5 | `window_median(nums, w)` (below). | tests below |
| 5 | l3 | `longform` | 4 | Say aloud, timing yourself to three minutes: how a monotonic deque gives every window maximum in linear time, with the counts for `n = 100,000`. | Model answer: each index is pushed once and popped at most once, at most 200,000 operations for one deque; the front is the maximum because everything behind it that is smaller can never win while the front stays. Rubric (10): 2 states the invariant (values fall from front to back), 2 pushes and pops once, 2 the count 200,000, 2 the front leaves when its index leaves the window, 2 compares with the double loop (`n * k`). |
| 6 | l1 | `numeric` | 3 | Comparisons to sort one million intervals before merging, about `n log2 n`, in millions to one decimal place. | 19.9 (19,931,569 computed by `n log2 n` and by `n ln n / ln 2`; accept 19.8 to 20.0) |
| 7 | l5 | `numeric` | 4 | Total set bits in the numbers 0 to 100,000. | 815,030 (summing `bin(i).count("1")` and counting bit by bit with a period formula) |
| 8 | l2 | `numeric` | 3 | Upper bound on trie memory for 1,000 words of length 10 if each node holds 26 child pointers of 8 bytes: bytes, ignoring the root. | 2,080,000 (`1000 * 10 * 26 * 8`, and by summing per node) |
| 9 | l4 | `order` | 4 | Insert into two heaps for a running median: (1) push to the lower max-heap if the value is at most its top, else to the upper min-heap; (2) rebalance so the sizes differ by at most one, the lower heap holding the extra; (3) the median is the lower top, or the mean of both tops when the sizes are equal. | Distractor: "push to whichever heap is larger" with its `why` (the order of values breaks). `same`: none. |

**Problem H1.1** `free_gaps(busy, start, end)`; Python; difficulty 3. Statement: "A trading room is booked in half-open slots `[s, e)` (whole minutes, in any order, overlapping allowed). Return the free gaps inside `[start, end)` as `[a, b]` lists, sorted." Reference, starter (returns the whole day; fails 6 of 8), tests (brute: a free-or-busy flag per minute):

@@PY:lx:FG_REF@@

@@PY:lx:FG_START@@

@@T:lx:fg@@

**Problem H1.2** `two_singles(nums)`; Python; difficulty 4. Statement: "Every number appears twice except two different numbers that appear once. Return those two, smaller first. Use `O(1)` extra memory." Reference (XOR all, isolate the lowest differing bit, split), starter (returns `[0, 0]`; fails 4 of 4), tests:

@@PY:l1:TS_REF@@

@@PY:l1:TS_START@@

@@T:l1:ts@@

**Problem H1.3** `shortest_at_least(nums, k)`; Python; difficulty 5. Statement: "`nums` may contain negative values. Return the length of the shortest non-empty contiguous run with sum at least `k` (`k >= 1`), or -1." Reference (a deque of prefix-sum indices), starter (returns -1; fails 7 of 9), tests (the last two have 100,000 values; the quadratic loop stops at the first of them):

@@PY:l1:SA_REF@@

@@PY:l1:SA_START@@

@@T:l1:sa@@

The last case's expected value, 9, was checked by the quadratic brute force on the first 600 values of the same periodic list (the shortest run is local) and by the reference; the case before it has the closed form 100,000.

**Problem H1.4** `window_median(nums, w)`; Python; difficulty 5. Statement: "Return the median of every window of `w` consecutive values (even `w`: the mean of the middle two), as floats. `1 <= w <= len(nums)`." Reference (two heaps, lazy deletion), starter (returns the first element of each window; fails 4 of 7), tests (the last has 40,000 values, `w = 500`, and checks the sum; the expected value comes from an independent sorted-window method):

@@PY:lx:WM_REF@@

@@PY:lx:WM_START@@

@@T:lx:wm@@

### Level 1 report notes

Report as `docs/LEVEL-BRIEF.md` says. Raise in `docs/BACKLOG-INBOX.md` anything the engine could not do. Do not edit files outside `app/content/courses/coding-int/`.

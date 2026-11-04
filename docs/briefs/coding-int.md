# Level briefs: coding-int (Coding Interviews, topic 3.5)

Course context. `coding-int` is a course of the new topic 3.5, Interviews by role (track `speed`, 60 hours plus the drill packs; plan in `docs/briefs/interview-plan.md` section (b), priority [Must]). Its promise is the `course.json` description: "Learn the patterns still missing, then solve interview problems against the clock while you explain them." The gap analysis (`docs/briefs/interview-gaps.md`, row "Coding and data structures", partial) names the patterns the app lacks at interview form: intervals, tries, monotonic deques, string parsing, simulation and object design, plus every timed online assessment format. Developer and strats roles ask this at speed, and trading and research roles meet it in online assessments (HackerRank, CodeSignal) and in live rounds where requirements are added part-way. User decisions of 29 October 2026 bind: UK first, trader and researcher tracks first (this course follows `research-int` L1 to L4), no audio (spoken answers are `longform` items the learner says aloud and then self-marks), firm-neutral content (firm types such as "a market maker's online assessment", never firm names).

The course has 4 levels and 19 lessons (5, 5, 4, 5). Lesson ids and titles below are copied from `app/content/courses/coding-int/course.json`; never rename an id. The skill ids are those of `course.json` (`ci-patterns`, `ci-strings`, `ci-design`, `ci-timed`) and are assigned per lesson as in `docs/briefs/interview-plan.md`: l1 to l5 `ci-patterns`; l6, l7, l9 `ci-strings`; l8 `ci-strings` and `ci-timed`; l10 `ci-strings` and `ci-design`; l11, l12, l14 `ci-design`; l13 `ci-design` and `ci-timed`; l15 to l18 `ci-timed`; l19 `ci-timed` and `ci-design`.

Prerequisites the learner holds (plan): `ds` L1 to L4, `graphs-dp` L1 to L4, `contests` L1 (stress testing). Everything else is named per lesson under "Builds on" with `course/lesson-id`. The courses that exist are `ds`, `algo-think`, `graphs-dp`, `contests`, `cpp`, `py-found` and `micro` (there is no `algorithms` or `python` course).

## Shared facts (every level)

**What the learner already has, so that this course never repeats topic 1.8.** The following were checked in the content files and are binding.

| Existing lesson or item | What it already teaches | Consequence here |
| --- | --- | --- |
| `ds` l11-first-in-first-out | Queue and deque; the sliding-window maximum with a monotonic deque of indices ("Values that can never win", "Run the deque", "Write it"). | l3 does not teach window maximum again: one recap `manipulate` run on new numbers, then variable windows (two deques) and prefix sums. |
| `ds` l10-next-greater | The monotonic stack and why each index is pushed and popped once. | l3 cites it for the push-and-pop count. |
| `ds` l9-last-in-first-out | Balanced brackets and postfix evaluation with a stack. | l7 starts from infix with precedence, unary minus, truncating division and nested decoding. |
| `ds` l4-frequencies, l5-both-ends | Anagram test by counts, anagram key by sorting, palindrome check by two pointers (letters only, ignoring case). | l6 starts from windows of counts, expanding centres and palindromic permutations. |
| `ds` l17-always-the-smallest, `ds` homework-4 h4-median, h4-merge, `algo-think` homework-3 h-kth-largest | Size-k heap, running median with two heaps (difficulty 5 homework), k-way merge, k-th largest. | l4 sets frequency top-k with ties (and the C++ comparator trap), a streaming k-th largest, and a sliding-window median as homework. The plain running median is a review item only. |
| `ds` l18-order-book-heaps, `micro` l1 to l3 | A heap-based order book with add, cancel (lazy) and crossing match, price-time priority. | l10 is an event processor over price levels with FIFO queues, market orders and amend rules, in Python and C++. |
| `ds` homework-3 h-lru (difficulty 5), `ds` l12-nodes-and-pointers | LRU cache from a dict and a doubly linked list with sentinels, in Python. | l11 does not teach it afresh: it is a from-memory recall, a C++ version with `std::list`, then a TTL cache and LFU. |
| `ds` l11-first-in-first-out transfer | A sliding-window-log rate limiter with a deque for one client. | l14 adds per-client keys, a fixed-window comparison, the token bucket and the ring-buffer hit counter. |
| `contests` l10-greedy-proofs | Meeting rooms by sweep (touching ends sort first), activity selection. | l1 counts overlapping pairs and merges; it cites the room count and does not set it as a problem. |
| `contests` l11-bitmasks | Enumerating subsets with a mask. | l5 is XOR, `n & (n - 1)`, `n & -n` and counting bits. |
| `contests` l2, l4, l13 to l16 | Limits to complexity, stress testing, a virtual contest, which problem first, debugging under time, upsolving. | l15 to l19 add partial-credit planning, planted-bug edge cases, pacing in timed drill sessions, narration and layered follow-ups. They cite these lessons. |
| `graphs-dp` l4-islands | Flood fill and counting islands. | l9 adds spiral order, in-place rotation and a border-seeded flood fill. |
| `py-found` l12-data-with-behaviour, `cpp` l10 to l12 | Writing a class in each language. | l12 to l14 design several cooperating classes and extend them under changing requirements. |
| `algo-think` l11-sorting-by-hand, l14-best-step-now | Sorting and greedy. | l1 sorts by start; l15 shows the greedy trap. |

**Runtime.** Python runs in Pyodide 0.27.7 (standard library only in this course; no NumPy). C++ runs in YoWASP clang 21 (WebAssembly, libc++, `-O1`, no exceptions, so no `try` or `catch`; the app flags are `-std=c++17`). Each case has 5 s. Every C++ reference below was compiled with the system `g++` with `-std=c++17` and `-std=c++20`, both with `-O1 -fno-exceptions`; the level agent still runs the playthrough, which uses the real clang and wasm, and reports any difference. `#include <bits/stdc++.h>` does not exist in libc++: write the headers.

**How a coding screen is written (all four levels).** Section 3 of `docs/AUTHORING.md`, `code`: `language`, `starter`, `examples` (two, visible), `tests` (at most 15, hidden), `how`, `solution` (always; the playthrough runs it), `prelude` and `postlude` for hidden code. Classes are tested through a hidden driver function in `postlude` that builds the learner's class, replays a list of operations and returns the results; the tests call the driver. In C++ a driver in `postlude` does the same, because `postlude` comes after the learner's code. A C++ argument of type list of lists (`std::vector<std::vector<int>>`) is written in `args` as nested JSON lists, rows may have different lengths, and the harness converts them with braced lists; give `types` for any argument where inference could be ambiguous (an empty list is ambiguous: give `["std::vector<std::vector<int>>"]`). A case that runs past its limit stops the later cases, so order the cases small to large: a slow solution then passes the small cases and fails at the first large one, which is the partial credit the course teaches. Every starter below is a runnable stub that fails at least one hidden test; for starters that are correct but slow, the failing case is a large input and the brief names the size.

**Lesson shape.** `docs/AUTHORING.md` sections 1, 2 and 6, as in the `ds` lessons: a hook `problem` (the learner tries before any rule is named), an `explore` or two, `ladder` screens that add one constraint, one `trap`, a `generalise` whose pattern is a fenced code block (a programming course states the pattern in code), a `derive` (`order`), a `transfer` in a quant or desk context, then the summary and a quiz of 3 to 5 items at difficulty 2 to 3. 8 to 12 screens; at most one `title` and two non-task screens. Every lesson has one edge case. Explanations are at most three sentences and refer to the learner's action. No audio anywhere; a spoken answer is a `longform` item whose prose tells the learner to say it aloud, timing themselves, before opening the model answer.

**Tags and pace.** Every drill-style screen, every review item and every homework item carries `"tags": ["<family>"]` (kebab-case, family first; families are given per lesson), so the interview bank can draw them later. `pace` (seconds) on every code screen of the lessons: 600 to 900 for a medium, as an assessment allows.

**Voice.** British English, no exclamation marks, no em-dashes, sentences under 20 words, explanations at most three sentences, £ for money (prices in the desk stories are in pence or £; say so on the first screen). Firm-neutral: "an exchange", "a market maker", "a bank's online assessment". Say "reported" for any format taken from candidate reports. Every stated number is computed twice. Every code solution passes its hidden tests and the starter fails them. These rules bind everything the level agent writes for the learner, including the quoted statements below (split a long statement into short sentences); the brief's own lines are instructions to the agent.

**Engine features from pass C** (built before these levels; no fallbacks anywhere).

| Item | What it provides | Used in |
| --- | --- | --- |
| E3 exam item banks | `draw: [{ "from": "bank/<family>", "tags": [...], "difficulty": [3, 4], "n": 5 }]` in an exam paper, resolved per attempt with a stored seed, items seen recorded, fresh items preferred. | Level 4: the closing screens of l15 and l17 send the learner to `#exam/mock-oa-code`, whose paper draws from the bank so that a resat is fresh; the level 4 review and homework items carry the tags that bank families use (`oa-triage`, `edge-case-list`, `complexity-read`, `timed-plan`). The mock file is authored in a separate task. |
| E8 drill library | `language: "cpp"` drills, a stopwatch on each drill, filters by pattern and difficulty on `#drill`, and a session of two drills in 60 minutes with one countdown. | Level 4: l17 (the session itself), l19 (a single-drill stopwatch for a 45-minute round). |
| E11 follow-up parts | `parts: [...]` on an item, each revealed after the previous answer is checked, graded per part. | Level 3 homework item 5 (ledger follow-ups); level 4 homework items 1 and 2 (live-round follow-ups). |
| E14 data files for code items | `data: { "<name>": "content/data/<path>" }` on a `code` widget, copied into the working directory before each run. | Level 2: l8 screen 8 (price files). |

**Existing engine features used.** `code` widget (Python and C++; `postlude` drivers; `testkit` and per-case `defines` in C++ for l16; `compare: "equal"`, `isclose`; `budget` and per-case time limits; `__learner_source__` checks); `choice`, `multi`, `numeric`, `order`, `table`, `tap-regions`, `manipulate`, `longform`; canvases `number-line` (with `intervals` and `tapIntervals`), `array` (stack, queue and linked modes, pointers, highlight ranges, cell labels), `tree`, `grid`, `orderbook`, `table`, `console`, `bars`; `carry`, `tags`, `pace`; `timed` on a level review (level 4 review, see below); mock assessments (`exams/mock-*.json`, built).

**Scripts and checks.** Every reference solution, starter and test below was run in `/tmp/claude-0/-home-user-zero-to-quant/ab4c69e5-1166-5ca2-9e21-f6569e1af79e/scratchpad/coding-int/`. Each level lists its files. Method: the reference is compared with an independent brute force (or a closed form) on thousands of seeded random cases, each expected value in the tables comes from the brute force and was asserted equal to the reference, and each starter was run against the tests and fails at least one (`harness.py` does both). Keyed answers in reviews and homework are in `numbers_check.py`, `numbers_check2.py` and each level script, each computed by two methods. The level agent recomputes every number it states.

**Reading the test tables.** A row is a hidden test: the call, and the expected value. A long setup is shown in the row as `setup; call`. `run_*` names are the hidden driver functions in `postlude`. "Starter fails n" counts the hidden tests the starter fails.

## Overlap rules for the level agents

- Say in the prose of each lesson, in one sentence, what the learner already did in an earlier lesson (cite by id) and what is new. Do not re-teach.
- Use the numbers and examples of this brief, not the earlier lessons' (for example, the window-maximum recap in l3 uses `[1, 3, -1, -3, 5, 3, 6, 7]`, not the `ds` l11 numbers).
- Every C++ screen has the same tests as its Python screen.

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

### l1-merging-intervals: Merging intervals (14 min; tags `intervals-merge`, `intervals-sweep`)

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

```python
def merge_intervals(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

Starter (fails 6 of 10: it only sorts):

```python
def merge_intervals(intervals):
    return sorted([list(x) for x in intervals])
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])` | `[[1, 6], [8, 10], [15, 18]]` |
| 2 | `merge_intervals([[1, 4], [4, 5]])` | `[[1, 5]]` |
| 3 | `merge_intervals([])` | `[]` |
| 4 | `merge_intervals([[5, 6]])` | `[[5, 6]]` |
| 5 | `merge_intervals([[8, 10], [1, 3], [2, 6]])` | `[[1, 6], [8, 10]]` |
| 6 | `merge_intervals([[1, 10], [2, 3], [4, 5]])` | `[[1, 10]]` |
| 7 | `merge_intervals([[2, 3], [4, 5], [6, 7]])` | `[[2, 3], [4, 5], [6, 7]]` |
| 8 | `merge_intervals([[-5, -2], [-3, 1]])` | `[[-5, 1]]` |
| 9 | `merge_intervals([[1, 2], [1, 2]])` | `[[1, 2]]` |
| 10 | `merge_intervals([[1, 2], [3, 4]])` | `[[1, 2], [3, 4]]` |

C++ twin (same ten cases, `call: "merge_intervals"`, `args: [[[1,3],[2,6],[8,10],[15,18]]]`, `types: ["std::vector<std::vector<int>>"]`, `expect` the same nested lists; the empty case is `args: [[]]` with the type given). Reference and starter (starter only sorts, fails 6 of 10); both compiled and run under `-std=c++17` and `-std=c++20`:

```cpp
#include <vector>
#include <algorithm>
std::vector<std::vector<int>> merge_intervals(std::vector<std::vector<int>> intervals) {
    std::sort(intervals.begin(), intervals.end());
    std::vector<std::vector<int>> out;
    for (const auto& iv : intervals) {
        if (!out.empty() && iv[0] <= out.back()[1]) out.back()[1] = std::max(out.back()[1], iv[1]);
        else out.push_back(iv);
    }
    return out;
}
```

```cpp
#include <vector>
#include <algorithm>
std::vector<std::vector<int>> merge_intervals(std::vector<std::vector<int>> intervals) {
    std::sort(intervals.begin(), intervals.end());
    return intervals;
}
```

**Problem 1.2** `count_overlapping_pairs(intervals)`; Python; difficulty 3. Statement: "Half-open intervals `[start, end)`, `start < end`, whole numbers, any order. Return how many pairs of intervals overlap. Touching ends do not overlap." Reference:

```python
def count_overlapping_pairs(intervals):
    events = []
    for s, e in intervals:
        events.append((s, 1))
        events.append((e, -1))
    events.sort()                      # at equal times -1 sorts first, so touching ends do not overlap
    active = pairs = 0
    for _, step in events:
        if step == 1:
            pairs += active
        active += step
    return pairs
```

Starter returns 0, fails 5 of 8 (the three zero cases pass):

```python
def count_overlapping_pairs(intervals):
    return 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `count_overlapping_pairs([[1, 5], [2, 3], [4, 8], [10, 12], [11, 15]])` | `3` |
| 2 | `count_overlapping_pairs([[0, 10], [10, 20]])` | `0` |
| 3 | `count_overlapping_pairs([])` | `0` |
| 4 | `count_overlapping_pairs([[1, 2]])` | `0` |
| 5 | `count_overlapping_pairs([[0, 5], [0, 5], [0, 5]])` | `3` |
| 6 | `count_overlapping_pairs([[0, 10], [1, 2], [3, 4], [5, 6]])` | `3` |
| 7 | `count_overlapping_pairs([[1, 4], [2, 6], [5, 9], [8, 10]])` | `3` |
| 8 | `iv = [[i, i + 3] for i in range(100000)]; count_overlapping_pairs(iv)` | `199997` |

Checks: brute double loop on 3,000 random lists; the last case also checks the closed form: `n` intervals `[i, i + 3)` give `(n - 1) + (n - 2)` pairs, which is 199,997 at `n = 100,000`.

### l2-prefix-trees: Prefix trees (14 min; tags `trie`, `prefix-count`, `autocomplete`)

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

```python
class Trie:
    def __init__(self):
        self.root = {'#n': 0}
    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {'#n': 0})
        if not node.get('#end'):
            node['#end'] = True
            node = self.root
            node['#n'] += 1
            for ch in word:
                node = node[ch]
                node['#n'] += 1
    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node
    def search(self, word):
        node = self._walk(word)
        return bool(node and node.get('#end'))
    def starts_with(self, prefix):
        return self._walk(prefix) is not None
    def count_prefix(self, prefix):
        node = self._walk(prefix)
        return node['#n'] if node else 0
```

Hidden driver (`postlude`):

```python
def run_trie(ops):
    t = Trie()
    out = []
    for op, arg in ops:
        if op == 'insert': t.insert(arg)
        elif op == 'search': out.append(t.search(arg))
        elif op == 'starts_with': out.append(t.starts_with(arg))
        else: out.append(t.count_prefix(arg))
    return out
```

Starter (insert does nothing, queries return `False` or 0; fails 5 of 6):

```python
class Trie:
    def __init__(self):
        self.words = []
    def insert(self, word):
        pass
    def search(self, word):
        return False
    def starts_with(self, prefix):
        return False
    def count_prefix(self, prefix):
        return 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_trie([('insert', 'tea'), ('insert', 'ten'), ('insert', 'to'), (...` | `[False, True, True, 2, 3]` |
| 2 | `run_trie([('insert', 'apple'), ('search', 'apple'), ('search', 'app...` | `[True, False, True, True, 2]` |
| 3 | `run_trie([('search', 'a'), ('starts_with', 'a'), ('count_prefix', '...` | `[False, False, 0]` |
| 4 | `run_trie([('insert', 'inn'), ('insert', 'inn'), ('count_prefix', 'i...` | `[1, 1, 0]` |
| 5 | `run_trie([('insert', 'a'), ('insert', 'ab'), ('insert', 'abc'), ('c...` | `[3, True, False]` |
| 6 | `run_trie([('insert', 'cat'), ('insert', 'car'), ('insert', 'cart'),...` | `[2, 3, False, True]` |

**Problem 2.2** `top_completions(words, prefix, k)`; Python; difficulty 3. Statement: "Return the `k` alphabetically smallest distinct words that start with `prefix`; fewer if fewer exist; an empty list for no match or `k = 0`." Reference (trie plus alphabetical depth-first search that stops at `k`):

```python
def top_completions(words, prefix, k):
    root = {}
    for w in set(words):
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node['$'] = True
    node = root
    for ch in prefix:
        if ch not in node:
            return []
        node = node[ch]
    out = []
    def dfs(node, path):
        if len(out) >= k:
            return
        if '$' in node:
            out.append(prefix + path)
        for ch in sorted(c for c in node if c != '$'):
            dfs(node[ch], path + ch)
    dfs(node, '')
    return out[:k]
```

Starter (first `k` matches in input order; fails 2 of 8, the cases where the input is not alphabetical or has duplicates):

```python
def top_completions(words, prefix, k):
    return [w for w in words if w.startswith(prefix)][:k]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `top_completions(['tea', 'ten', 'to', 'team', 'tear', 'inn', 'tea'],...` | `['tea', 'team', 'tear']` |
| 2 | `top_completions(['tea', 'ten', 'to', 'team', 'tear', 'inn'], 'te', 10)` | `['tea', 'team', 'tear', 'ten']` |
| 3 | `top_completions(['tea', 'ten', 'to'], '', 2)` | `['tea', 'ten']` |
| 4 | `top_completions(['tea', 'ten', 'to'], 'x', 2)` | `[]` |
| 5 | `top_completions(['car', 'card', 'care', 'cat', 'dog'], 'car', 2)` | `['car', 'card']` |
| 6 | `top_completions(['b', 'a', 'ab', 'abc'], 'a', 0)` | `[]` |
| 7 | `top_completions([], 'a', 3)` | `[]` |
| 8 | `top_completions(['ab', 'a', 'abc'], 'ab', 5)` | `['ab', 'abc']` |

### l3-window-maximum: The maximum of a sliding window (13 min; tags `monotonic-deque`, `window-range`)

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

```python
from collections import deque
def longest_within_limit(nums, limit):
    hi, lo = deque(), deque()
    left = best = 0
    for right, x in enumerate(nums):
        while hi and nums[hi[-1]] <= x:
            hi.pop()
        hi.append(right)
        while lo and nums[lo[-1]] >= x:
            lo.pop()
        lo.append(right)
        while nums[hi[0]] - nums[lo[0]] > limit:
            left += 1
            if hi[0] < left: hi.popleft()
            if lo[0] < left: lo.popleft()
        best = max(best, right - left + 1)
    return best
```

```python
def longest_within_limit(nums, limit):
    return 1 if nums else 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `longest_within_limit([8, 2, 4, 7], 4)` | `2` |
| 2 | `longest_within_limit([10, 1, 2, 4, 7, 2], 5)` | `4` |
| 3 | `longest_within_limit([4, 2, 2, 2, 4, 4, 2, 2], 0)` | `3` |
| 4 | `longest_within_limit([], 3)` | `0` |
| 5 | `longest_within_limit([5], 0)` | `1` |
| 6 | `longest_within_limit([1, 5, 6, 7, 8, 10, 6, 5, 6], 4)` | `5` |
| 7 | `longest_within_limit([3, 3, 3], 0)` | `3` |
| 8 | `xs = list(range(100000)); longest_within_limit(xs, 10)` | `11` |
| 9 | `ys = [1] * 100000; longest_within_limit(ys, 0)` | `100000` |
| 10 | `zs = [i % 7 for i in range(100000)]; longest_within_limit(zs, 6)` | `100000` |
| 11 | `ws = [i % 7 for i in range(100000)]; longest_within_limit(ws, 3)` | `4` |

### l4-top-k: The k largest and the running median (14 min; tags `heap-top-k`, `heap-comparator`, `stream-kth`)

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

```python
import heapq
from collections import Counter

def top_k_frequent(words, k):
    count = Counter(words)
    best = heapq.nsmallest(k, count.items(), key=lambda kv: (-kv[1], kv[0]))
    return [w for w, _ in best]
```

```python
from collections import Counter

def top_k_frequent(words, k):
    return list(Counter(words))[:k]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `top_k_frequent(['i', 'love', 'leetcode', 'i', 'love', 'coding'], 2)` | `['i', 'love']` |
| 2 | `top_k_frequent(['the', 'day', 'is', 'sunny', 'the', 'the', 'the', '...` | `['the', 'is', 'sunny', 'day']` |
| 3 | `top_k_frequent(['a'], 1)` | `['a']` |
| 4 | `top_k_frequent(['b', 'a'], 5)` | `['a', 'b']` |
| 5 | `top_k_frequent(['x', 'y', 'x', 'y', 'z'], 2)` | `['x', 'y']` |
| 6 | `top_k_frequent(['q', 'q'], 0)` | `[]` |
| 7 | `words = ['w%04d' % (i % 1000) for i in range(50000)]; top_k_frequen...` | `['w0000', 'w0001', 'w0002']` |

C++ twin (signature `std::vector<std::string> top_k_frequent(std::vector<std::string> words, int k)`; the same seven cases with `args` and `types: ["std::vector<std::string>", "int"]`; the large case built in `setup`): reference with a `priority_queue` and a comparator, starter (the first `k` keys of an `unordered_map`, fails 4 of 7). Compiled and run on all seven cases.

```cpp
#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <algorithm>
std::vector<std::string> top_k_frequent(std::vector<std::string> words, int k) {
    std::unordered_map<std::string, int> count;
    for (const auto& w : words) ++count[w];
    auto worse = [](const std::pair<int, std::string>& a, const std::pair<int, std::string>& b) {
        if (a.first != b.first) return a.first > b.first;
        return a.second < b.second;
    };
    std::priority_queue<std::pair<int, std::string>, std::vector<std::pair<int, std::string>>, decltype(worse)> heap(worse);
    for (const auto& kv : count) {
        heap.push({kv.second, kv.first});
        if ((int)heap.size() > k) heap.pop();
    }
    std::vector<std::string> out(heap.size());
    for (int i = (int)out.size() - 1; i >= 0; --i) {
        out[i] = heap.top().second;
        heap.pop();
    }
    return out;
}
```

```cpp
#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <algorithm>
std::vector<std::string> top_k_frequent(std::vector<std::string> words, int k) {
    std::unordered_map<std::string, int> count;
    for (const auto& w : words) ++count[w];
    std::vector<std::string> out;
    for (const auto& kv : count) out.push_back(kv.first);
    if ((int)out.size() > k) out.resize(k);
    return out;
}
```

**Problem 4.2** `kth_largest_stream(k, initial, adds)`; Python; difficulty 3. Statement: "Start with the numbers in `initial`. After each number in `adds` is added, record the `k`-th largest of everything so far (the largest is the first). Every call has at least `k` numbers after the first add." Reference (size-k min-heap), starter (returns the maximum so far; fails 5 of 6), tests (the last has 31,000 numbers and checks the sum, expected value from an independent `bisect` insertion):

```python
import heapq
def kth_largest_stream(k, initial, adds):
    heap = []
    for x in initial:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    out = []
    for x in adds:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
        out.append(heap[0])
    return out
```

```python
def kth_largest_stream(k, initial, adds):
    return [max(initial + adds[:i + 1]) for i in range(len(adds))]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `kth_largest_stream(3, [4, 5, 8, 2], [3, 5, 10, 9, 4])` | `[4, 5, 5, 8, 8]` |
| 2 | `kth_largest_stream(1, [], [-3, -2, -4, 0, 4])` | `[-3, -2, -2, 0, 4]` |
| 3 | `kth_largest_stream(2, [0], [-1, 1, -2, -4, 3])` | `[-1, 0, 0, 0, 1]` |
| 4 | `kth_largest_stream(3, [5, 5, 5], [5, 6, 1])` | `[5, 5, 5]` |
| 5 | `kth_largest_stream(4, [10, 9, 8], [7, 100, 1])` | `[7, 8, 8]` |
| 6 | `import random; random.seed(3); xs = [random.randint(0, 10**6) for _...` | `28666963171` |

### l5-bit-tricks: Bit tricks at interview (12 min; tags `bit-xor`, `bit-count`, `bit-lowest`)

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

```python
def single_number(nums):
    x = 0
    for v in nums:
        x ^= v
    return x
```

```python
def single_number(nums):
    return sum(nums)
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `single_number([2, 2, 1])` | `1` |
| 2 | `single_number([4, 1, 2, 1, 2])` | `4` |
| 3 | `single_number([7])` | `7` |
| 4 | `single_number([-3, 5, -3])` | `5` |
| 5 | `single_number([10, 20, 30, 20, 10])` | `30` |
| 6 | `single_number([0, 1, 0])` | `1` |
| 7 | `xs = [v for v in range(1, 100001) if v != 54321] * 2 + [54321]; sin...` | `54321` |

**Problem 5.2** `count_bits(n)`; Python; difficulty 3. Statement: "Return a list of length `n + 1` whose `i`-th entry is the number of 1 bits in `i`; in `O(n)` time, without calling a bit-count function." Reference, starter (all zeros; fails 7 of 8):

```python
def count_bits(n):
    out = [0] * (n + 1)
    for i in range(1, n + 1):
        out[i] = out[i >> 1] + (i & 1)
    return out
```

```python
def count_bits(n):
    return [0] * (n + 1)
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `count_bits(0)` | `[0]` |
| 2 | `count_bits(1)` | `[0, 1]` |
| 3 | `count_bits(2)` | `[0, 1, 1]` |
| 4 | `count_bits(5)` | `[0, 1, 1, 2, 1, 2]` |
| 5 | `count_bits(8)` | `[0, 1, 1, 2, 1, 2, 2, 3, 1]` |
| 6 | `count_bits(16)` | `[0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4...` |
| 7 | `count_bits(31)` | `[0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4...` |
| 8 | `sum(count_bits(100000))` | `815030` |

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

```python
def free_gaps(busy, start, end):
    gaps = []
    cursor = start
    for s, e in sorted(busy):
        if s > cursor:
            gaps.append([cursor, min(s, end)])
        cursor = max(cursor, e)
        if cursor >= end:
            break
    if cursor < end:
        gaps.append([cursor, end])
    return [g for g in gaps if g[0] < g[1]]
```

```python
def free_gaps(busy, start, end):
    return [[start, end]]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `free_gaps([[9, 12], [10, 11], [14, 15]], 9, 17)` | `[[12, 14], [15, 17]]` |
| 2 | `free_gaps([[0, 5]], 0, 5)` | `[]` |
| 3 | `free_gaps([], 8, 16)` | `[[8, 16]]` |
| 4 | `free_gaps([[8, 10], [10, 12]], 8, 12)` | `[]` |
| 5 | `free_gaps([[1, 3], [2, 6], [8, 9]], 0, 10)` | `[[0, 1], [6, 8], [9, 10]]` |
| 6 | `free_gaps([[0, 20]], 5, 10)` | `[]` |
| 7 | `free_gaps([[3, 4]], 5, 10)` | `[[5, 10]]` |
| 8 | `free_gaps([[7, 9], [1, 2]], 3, 8)` | `[[3, 7]]` |

**Problem H1.2** `two_singles(nums)`; Python; difficulty 4. Statement: "Every number appears twice except two different numbers that appear once. Return those two, smaller first. Use `O(1)` extra memory." Reference (XOR all, isolate the lowest differing bit, split), starter (returns `[0, 0]`; fails 4 of 4), tests:

```python
def two_singles(nums):
    x = 0
    for v in nums:
        x ^= v
    low = x & -x
    a = 0
    for v in nums:
        if v & low:
            a ^= v
    b = x ^ a
    return sorted([a, b])
```

```python
def two_singles(nums):
    return [0, 0]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `two_singles([1, 2, 1, 3, 2, 5])` | `[3, 5]` |
| 2 | `two_singles([-1, 0])` | `[-1, 0]` |
| 3 | `two_singles([4, 4, 6, 9])` | `[6, 9]` |
| 4 | `two_singles([0, 7, 0, 3, 7, 3, -8, 12])` | `[-8, 12]` |

**Problem H1.3** `shortest_at_least(nums, k)`; Python; difficulty 5. Statement: "`nums` may contain negative values. Return the length of the shortest non-empty contiguous run with sum at least `k` (`k >= 1`), or -1." Reference (a deque of prefix-sum indices), starter (returns -1; fails 7 of 9), tests (the last two have 100,000 values; the quadratic loop stops at the first of them):

```python
from collections import deque
def shortest_at_least(nums, k):
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    dq = deque()
    best = len(nums) + 1
    for j, p in enumerate(pre):
        while dq and p - pre[dq[0]] >= k:
            best = min(best, j - dq.popleft())
        while dq and pre[dq[-1]] >= p:
            dq.pop()
        dq.append(j)
    return best if best <= len(nums) else -1
```

```python
def shortest_at_least(nums, k):
    return -1
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `shortest_at_least([1], 1)` | `1` |
| 2 | `shortest_at_least([1, 2], 4)` | `-1` |
| 3 | `shortest_at_least([2, -1, 2], 3)` | `3` |
| 4 | `shortest_at_least([84, -37, 32, 40, 95], 167)` | `3` |
| 5 | `shortest_at_least([1, 2, 3], 6)` | `3` |
| 6 | `shortest_at_least([-1, -2], 1)` | `-1` |
| 7 | `shortest_at_least([5, -3, 4], 5)` | `1` |
| 8 | `xs = [1] * 100000; shortest_at_least(xs, 100000)` | `100000` |
| 9 | `ys = [3, -2] * 50000; shortest_at_least(ys, 7)` | `9` |

The last case's expected value, 9, was checked by the quadratic brute force on the first 600 values of the same periodic list (the shortest run is local) and by the reference; the case before it has the closed form 100,000.

**Problem H1.4** `window_median(nums, w)`; Python; difficulty 5. Statement: "Return the median of every window of `w` consecutive values (even `w`: the mean of the middle two), as floats. `1 <= w <= len(nums)`." Reference (two heaps, lazy deletion), starter (returns the first element of each window; fails 4 of 7), tests (the last has 40,000 values, `w = 500`, and checks the sum; the expected value comes from an independent sorted-window method):

```python
import heapq
from collections import defaultdict

def window_median(nums, w):
    lo, hi = [], []                    # lo: max-heap by negation, hi: min-heap
    late = defaultdict(int)            # values waiting to be deleted lazily
    lo_n = hi_n = 0                    # live sizes
    def prune(heap, sign):
        while heap and late[sign * heap[0]] > 0:
            late[sign * heap[0]] -= 1
            heapq.heappop(heap)
    def rebalance():
        nonlocal lo_n, hi_n
        if lo_n > hi_n + 1:
            heapq.heappush(hi, -heapq.heappop(lo)); lo_n -= 1; hi_n += 1; prune(lo, -1)
        elif lo_n < hi_n:
            heapq.heappush(lo, -heapq.heappop(hi)); hi_n -= 1; lo_n += 1; prune(hi, 1)
    def add(x):
        nonlocal lo_n, hi_n
        if not lo or x <= -lo[0]:
            heapq.heappush(lo, -x); lo_n += 1
        else:
            heapq.heappush(hi, x); hi_n += 1
        rebalance()
    def remove(x):
        nonlocal lo_n, hi_n
        late[x] += 1
        if lo and x <= -lo[0]:
            lo_n -= 1
            if x == -lo[0]: prune(lo, -1)
        else:
            hi_n -= 1
            if hi and x == hi[0]: prune(hi, 1)
        rebalance()
    out = []
    for i, x in enumerate(nums):
        add(x)
        if i >= w:
            remove(nums[i - w])
        if i >= w - 1:
            out.append(float(-lo[0]) if w % 2 else (-lo[0] + hi[0]) / 2)
    return out
```

```python
def window_median(nums, w):
    return [float(nums[i]) for i in range(len(nums) - w + 1)]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `window_median([1, 3, -1, -3, 5, 3, 6, 7], 3)` | `[1.0, -1.0, -1.0, 3.0, 5.0, 6.0]` |
| 2 | `window_median([1, 2, 3, 4, 2, 3, 1, 4, 2], 3)` | `[2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]` |
| 3 | `window_median([5], 1)` | `[5.0]` |
| 4 | `window_median([1, 4, 2, 3], 4)` | `[2.5]` |
| 5 | `window_median([7, 7, 7, 7], 2)` | `[7.0, 7.0, 7.0]` |
| 6 | `window_median([2, 2, 2, 2, 2], 5)` | `[2.0]` |
| 7 | `import random; random.seed(9); xs = [random.randint(0, 10**6) for _...` | `19786861586.5` |

### Level 1 report notes

Report as `docs/LEVEL-BRIEF.md` says. Raise in `docs/BACKLOG-INBOX.md` anything the engine could not do. Do not edit files outside `app/content/courses/coding-int/`.

## Level 2

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `coding-int` (topic 3.5), level 2 ("Strings and simulation"): lessons `l6-anagrams-and-palindromes`, `l7-parsing-with-a-stack`, `l8-simulating-the-rules`, `l9-grids-and-matrices`, `l10-matching-engine`, plus `review-2.json` and `homework-2.json`, in `app/content/courses/coding-int/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids of `course.json` exactly. Use £ for money (prices in l8 and l10 are whole pence; say so on the first screen). Scripts: `l2.py` (every problem of this level, brute forces, C++ cross-check of the matching engine on 300 random streams), `l2_data.py` (price files), `harness.py`, `numbers_check.py`, `numbers_check2.py`.

Level promise. The learner turns text into code that is right at the edges: string questions with counts and centres, nested expressions, a long rule statement as an online assessment sets it, a matrix without off-by-one errors, and a small matching engine. It is the first level where the clock is part of the lesson, so every code screen carries a `pace`.

**Engine features.** E14 (data files) in l8 screen 8; E3, E8 and E11 are not needed. Existing: `code` (Python and C++; Python `data` is E14), `grid` canvas for matrices (grid ids are one-based, cell text plain), `orderbook` canvas for the engine, `console` for an assessment statement and its output, `array` (stack mode) for the parser, `manipulate`, `order`, `tap-regions`, `table`.

**Builds on (by id) and what is new.**

| Lesson | Builds on | New over those |
| --- | --- | --- |
| l6-anagrams-and-palindromes | `ds` l4-frequencies (anagram counts and key), `ds` l5-both-ends (palindrome by two pointers), `ds` l6-sliding-window | Counting inside a moving window of fixed width, expanding from `2n - 1` centres, and when a string can be rearranged into a palindrome. |
| l7-parsing-with-a-stack | `ds` l9-last-in-first-out (brackets, postfix), `algo-think` l5-calls-itself | Infix with precedence on two stacks, unary minus, division that truncates toward zero, nested decoding with a stack of (text, count). |
| l8-simulating-the-rules | `contests` l1-reading-statements, `contests` l15-debugging-under-time, `py-found` l10-reading-a-csv | Turning an eight-rule statement into state, events and an order of checks; reading a price file (E14). |
| l9-grids-and-matrices | `graphs-dp` l4-islands, `ds` l1-arrays-in-memory | Boundary shrinking for spiral order, index maps for in-place rotation, flood fill from the border; Game of Life in homework. |
| l10-matching-engine | `ds` l18-order-book-heaps, `micro` l1-bids-and-asks, `micro` l3-the-queue, `cpp` l15-maps | An event processor over price levels with FIFO queues; market orders; cancel and amend by id; the same engine in C++ with `std::map` and `std::deque`. |

### l6-anagrams-and-palindromes: Anagrams and palindromes (13 min; tags `anagram-window`, `palindrome-centres`, `palindrome-permutation`)

Objective: Solve string questions with counts, two pointers and expanding centres. Method stated after use: to find anagrams of `p` in `s`, keep a count of the letters in the current window of length `len(p)`, add the new letter, drop the old one, and compare the counts; to find palindromes, grow outwards from each of the `2n - 1` centres (each letter, and each gap between two letters) while the two ends match.

Screens (10):
1. Hook `problem`, `array` of `cbaebabacd` with a highlight range of width 3; `tap-regions`: tap the starts of windows that are anagrams of `abc`; answer index 0 and index 6.
2. `explore`: slide the window with a control; `numeric`: how many windows of width 3 does `cbaebabacd` have (8).
3. `ladder`, `numeric`: sorting every window of width 1,000 in a string of 100,000 does 99,001 sorts of 1,000 letters; the count version updates 100,000 times (answer: the number of windows, 99,001, computed as `n - w + 1` and by counting starts).
4. `problem`, code A, `find_anagrams`, `pace` 600.
5. `ladder`, `array` showing centres of `abba` (7 centres: four letters and three gaps); `numeric`: the number of centres of a string of 7 letters is 13 (`2n - 1`).
6. `problem`, code B, `longest_palindrome`, `pace` 600.
7. `trap`, `choice`: a learner who only expands from letters misses even palindromes: `cbbd` has the answer `bb`; right answer 2 (the gap centre).
8. `generalise` + `derive` (`order`: for each centre set `lo` and `hi`, widen while equal and in range, record if longer).
9. `transfer`, `multi`: which of `carerac`, `abcabc`, `aabbccd`, `abcd`, `aabbcd` can be rearranged into a palindrome (at most one letter with an odd count): `carerac`, `abcabc`, `aabbccd`.
10. `transfer`, `numeric`: how many palindromic substrings has `abba` (6: `a`, `b`, `b`, `a`, `bb`, `abba`) and how many has `aaa` (6), counted by centres and by listing every substring.

Quiz (4): window counts; centres for `n = 7`; palindromic permutation; the worst case of centre expansion on `aaaa...` (quadratic).

**Problem 6.1** `find_anagrams(s, p)`; Python; difficulty 3. Statement: "Return the start index of every window of `s` that is an anagram of `p`, in increasing order." Reference, starter (finds exact copies of `p`, not anagrams; fails 4 of 8), tests (the last has 100,000 letters and `p` of 1,000):

```python
def find_anagrams(s, p):
    need = {}
    for ch in p:
        need[ch] = need.get(ch, 0) + 1
    have = {}
    out = []
    for i, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if i >= len(p):
            old = s[i - len(p)]
            have[old] -= 1
            if have[old] == 0:
                del have[old]
        if have == need:
            out.append(i - len(p) + 1)
    return out
```

```python
def find_anagrams(s, p):
    return [i for i in range(len(s)) if s[i:i + len(p)] == p]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `find_anagrams('cbaebabacd', 'abc')` | `[0, 6]` |
| 2 | `find_anagrams('abab', 'ab')` | `[0, 1, 2]` |
| 3 | `find_anagrams('aaaa', 'aa')` | `[0, 1, 2]` |
| 4 | `find_anagrams('abc', 'abcd')` | `[]` |
| 5 | `find_anagrams('', 'a')` | `[]` |
| 6 | `find_anagrams('baa', 'aa')` | `[1]` |
| 7 | `find_anagrams('xyzzyx', 'zy')` | `[1, 3]` |
| 8 | `s = 'ab' * 50000; len(find_anagrams(s, 'ba' * 500))` | `99001` |

**Problem 6.2** `longest_palindrome(s)`; Python; difficulty 3. Statement: "Return the longest palindromic substring of `s`; when two have the same length, the one that starts first; the empty string for an empty input." Reference, starter (returns the first letter; fails 7 of 10), tests (the last has `'a' * 3000`, so 3,000 centres expanding fully: about 9 million steps, inside the limit):

```python
def longest_palindrome(s):
    best = (0, 0)
    for c in range(2 * len(s) - 1):
        lo, hi = c // 2, c // 2 + c % 2
        while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
            lo -= 1
            hi += 1
        if hi - lo - 1 > best[1] - best[0]:
            best = (lo + 1, hi)
    return s[best[0]:best[1]]
```

```python
def longest_palindrome(s):
    return s[:1]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `longest_palindrome('babad')` | `'bab'` |
| 2 | `longest_palindrome('cbbd')` | `'bb'` |
| 3 | `longest_palindrome('a')` | `'a'` |
| 4 | `longest_palindrome('')` | `''` |
| 5 | `longest_palindrome('abacdfgdcaba')` | `'aba'` |
| 6 | `longest_palindrome('forgeeksskeegfor')` | `'geeksskeeg'` |
| 7 | `longest_palindrome('abcd')` | `'a'` |
| 8 | `longest_palindrome('aaaa')` | `'aaaa'` |
| 9 | `longest_palindrome('racecarxyz')` | `'racecar'` |
| 10 | `s = 'a' * 3000; len(longest_palindrome(s))` | `3000` |

### l7-parsing-with-a-stack: Parsing with a stack (14 min; tags `expression-parse`, `decode-nested`, `integer-division`)

Objective: Evaluate and decode nested expressions with a stack. Method stated after use: keep a stack of numbers and a stack of operators; before pushing an operator, apply every operator on top that binds at least as tightly; a closing bracket applies operators back to its opening bracket; a minus where an operand is expected is unary.

Screens (11):
1. Hook `problem`, `array` (stack mode, two stacks) for `3+2*2`; `numeric`: the value (7); the learner who evaluates left to right gets 10.
2. `explore`, `manipulate` over `3+2*2`: push, push, push, apply `*`, apply `+`; the postfix form is `3 2 2 * +` (cite `ds` l9 for postfix).
3. `ladder`, `choice`: `10-2-3` must be 5, not 11: equal precedence applies the earlier operator first (`>=`).
4. `ladder`, `numeric`: `2*(5+5*2)/3+(6/2+8)` is 21 (hand: `2*15/3 = 10`, `6/2 + 8 = 11`); the peak size of the operator stack is 4.
5. `trap`, `numeric`: `-7/2` under the statement's rule, which truncates toward zero: -3. Python's `//` gives -4. Name the action in `byKey` ("You used floor division").
6. `problem`, code A, `calculate`, `pace` 840, difficulty 4.
7. `ladder`, `numeric`: decode `3[a2[c]]` has length 9 and `2[abc]3[cd]ef` has length 14; `choice` for what to push on `[` (the pair: text so far and the count).
8. `problem`, code B, `decode_string`, `pace` 600.
9. `generalise` + `derive` (`order` the decode steps with the distractor "push the digits as characters").
10. `transfer`, `choice`: a risk formula in a config file with brackets and `-` signs: which of the two parsers (stack, or `eval`) a firm would allow, and why (`eval` runs arbitrary code).
11. `transfer`, `numeric`: `9[9[9[a]]]` decodes to 729 letters (`9^3`), so decode in place would be `O(output)`; the stack is `O(depth)`.

Quiz (4): precedence with equal ranks; truncation; a decode length; the stack depth on nested brackets.

**Problem 7.1** `calculate(s)`; Python; difficulty 4. Statement: "`s` holds non-negative whole numbers, `+ - * /`, spaces and brackets; a `-` may also be unary (`-(2+3)*4`, `2*-3`). `/` truncates toward zero. Every input is valid and never divides by zero. Return the value as an `int`." Reference (two stacks and a unary operator), starter (calls `eval` with `//`; fails 2 of 15: negative division and unary minus), tests:

```python
def calculate(s):
    prec = {'+': 1, '-': 1, '*': 2, '/': 2, 'u': 3}
    nums, ops = [], []
    def apply():
        op = ops.pop()
        if op == 'u':
            nums.append(-nums.pop())
            return
        b, a = nums.pop(), nums.pop()
        if op == '+': nums.append(a + b)
        elif op == '-': nums.append(a - b)
        elif op == '*': nums.append(a * b)
        else: nums.append(abs(a) // abs(b) * (1 if (a < 0) == (b < 0) else -1))
    i, expect_operand = 0, True
    while i < len(s):
        c = s[i]
        if c == ' ':
            i += 1
        elif c.isdigit():
            j = i
            while j < len(s) and s[j].isdigit():
                j += 1
            nums.append(int(s[i:j]))
            i, expect_operand = j, False
        elif c == '(':
            ops.append(c); i += 1; expect_operand = True
        elif c == ')':
            while ops[-1] != '(':
                apply()
            ops.pop(); i += 1; expect_operand = False
        else:
            if c == '-' and expect_operand:
                c = 'u'
            if c != 'u':
                while ops and ops[-1] != '(' and prec[ops[-1]] >= prec[c]:
                    apply()
            ops.append(c); i += 1; expect_operand = True
    while ops:
        apply()
    return nums[0]
```

```python
def calculate(s):
    return int(eval(s.replace('/', '//')))
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `calculate('3+2*2')` | `7` |
| 2 | `calculate(' 3/2 ')` | `1` |
| 3 | `calculate('(1+(4+5+2)-3)+(6+8)')` | `23` |
| 4 | `calculate('-(2+3)*4')` | `-20` |
| 5 | `calculate('14-3/2')` | `13` |
| 6 | `calculate('-7/2')` | `-3` |
| 7 | `calculate('(-7)/2')` | `-3` |
| 8 | `calculate('2*(5+5*2)/3+(6/2+8)')` | `21` |
| 9 | `calculate('1-(-2)')` | `3` |
| 10 | `calculate('2*-3')` | `-6` |
| 11 | `calculate('10-2-3')` | `5` |
| 12 | `calculate('100/10/5')` | `2` |
| 13 | `calculate('42')` | `42` |
| 14 | `calculate('-(-(5))')` | `5` |
| 15 | `calculate('8/3*3')` | `6` |

Checks: 3,913 random expressions compared with a parser built on `ast` with truncating division; the postfix forms and values of `3+2*2` (`3 2 2 * +`, 7), `10-2-3` (`10 2 - 3 -`, 5) and `(1+2)*3` (`1 2 + 3 *`, 9) match the stack evaluator.

**Problem 7.2** `decode_string(s)`; Python; difficulty 3. Statement: "`k[text]` repeats `text` `k` times; `k` may have several digits; brackets nest; letters outside brackets stay as they are. Every input is valid." Reference, starter (returns `s`; fails 8 of 10), tests:

```python
def decode_string(s):
    stack = []
    count, cur = 0, []
    for ch in s:
        if ch.isdigit():
            count = count * 10 + int(ch)
        elif ch == '[':
            stack.append((cur, count))
            cur, count = [], 0
        elif ch == ']':
            prev, k = stack.pop()
            prev.append(''.join(cur) * k)
            cur = prev
        else:
            cur.append(ch)
    return ''.join(cur)
```

```python
def decode_string(s):
    return s
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `decode_string('3[a]2[bc]')` | `'aaabcbc'` |
| 2 | `decode_string('3[a2[c]]')` | `'accaccacc'` |
| 3 | `decode_string('2[abc]3[cd]ef')` | `'abcabccdcdcdef'` |
| 4 | `decode_string('abc')` | `'abc'` |
| 5 | `decode_string('10[a]')` | `'aaaaaaaaaa'` |
| 6 | `decode_string('')` | `''` |
| 7 | `decode_string('2[2[2[a]]]')` | `'aaaaaaaa'` |
| 8 | `decode_string('a2[b]c')` | `'abbc'` |
| 9 | `decode_string('1[]')` | `''` |
| 10 | `decode_string('12[xy]')` | `'xyxyxyxyxyxyxyxyxyxyxyxy'` |

### l8-simulating-the-rules: Simulating the rules (14 min; tags `simulation-rules`, `file-read`, `edge-order`)

Objective: Turn a long rule statement into a correct simulation, as online assessments often ask. Method stated after use: list the state (what must be remembered between steps), the events (what arrives each step) and the order of the checks; write one function that applies one event; test it on a hand-built trace. Skills `ci-strings` and `ci-timed`.

The running story (a rule-based bot as an assessment states it, prices in whole pence):

> A bot trades one unit of one stock. It starts flat. Day 0 never trades. While flat on day `i >= 1` it buys at that day's price when the price is below the previous day's price. While long, on each later day it sells at that day's price if, in this order: (1) the price is at least 5% above the entry price (`100 * p >= 105 * entry`); (2) the price is at most 3% below the entry (`100 * p <= 97 * entry`); (3) it has held for exactly 3 days (`i - bought == 3`). A bot that sells on day `i` does not buy on day `i`. If it still holds at the end it sells at the last price. Return `[total profit in pence, number of trades]`.

Screens (11):
1. Hook `problem`, `console` showing the statement and a six-day price list `[100, 98, 99, 100, 104, 110]`; `numeric`: total profit (6). The learner traces by hand: buys 98 on day 1, sells 104 on day 4 (`10400 >= 10290`).
2. `explore`, `table` widget with columns day, price, state, action filled for the six days (the learner completes it).
3. `ladder`, `choice`: which rule fires first on a day when the price is both 5% up and the third day: rule 1 (the order of checks decides).
4. `ladder`, `numeric`: the time rule counts days since the buy. A bot that buys on day 2 sells on which day if no other rule fires? Day 5 (`2 + 3`). (The homework item uses a list where `== 3` and `> 3` differ.)
5. `problem`, code A, `run_strategy`, `pace` 840.
6. `trap`, `choice`: prices `[100, 95, 90, 85]`. The stop rule sells at 90 on day 2 (`9000 <= 9215`). A bot that also buys on the day it sells gets `[-10, 3]`; the right answer is `[-5, 2]` (it buys at 85 on day 3 and sells at the end for 0). Name the action in `byKey` ("You let the bot buy on the day it sold"). Both traces were run and the correct one was checked by hand.
7. `generalise`: state, events, order, in fenced code; `derive`: `order` the six steps of reading a long statement.
8. `problem`, code B (E14), `strategy_from_file` reading `ticks-40.csv`, `ticks-3.csv` and `ticks-header-only.csv`; `data` on the widget. The starter includes the working `run_strategy` and a `load_prices` stub.
9. `transfer`, `choice`: which of three statements of the same rule is ambiguous ("sells after three days" against "sells on the third day after the buy"): the learner picks the ambiguity and the question to ask.
10. `transfer`, `numeric`: a different price list the agent chooses and computes twice (suggested: `[100, 95, 100, 106, 90, 89, 95, 99]` gives `[10, 2]`: the review item uses it, so choose another for the lesson).
11. `transfer`, `choice` on testing: write two hand traces before the code (the lesson of `contests` l15).

Quiz (4): an order-of-checks question; the same-day buy rule; a file edge case (header only); a traced profit.

**Problem 8.1** `run_strategy(prices)`; Python; difficulty 4. Statement: the story above; `prices` is a list of whole numbers, possibly empty; return `[profit, trades]` as a list of two ints. Reference, starter (profit is the last price minus the first, one trade; fails 8 of 8), tests (expected values from a second implementation that scans forward from each buy, matched on 5,000 random lists):

```python
def run_strategy(prices):
    pnl = trades = 0
    long_, entry, bought = False, 0, 0
    for i, p in enumerate(prices):
        if not long_:
            if i >= 1 and p < prices[i - 1]:
                long_, entry, bought = True, p, i
        else:
            if 100 * p >= 105 * entry or 100 * p <= 97 * entry or i - bought == 3:
                pnl += p - entry
                trades += 1
                long_ = False
    if long_:
        pnl += prices[-1] - entry
        trades += 1
    return [pnl, trades]
```

```python
def run_strategy(prices):
    return [prices[-1] - prices[0], 1]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_strategy([100, 98, 99, 100, 104, 110])` | `[6, 1]` |
| 2 | `run_strategy([100, 100, 100])` | `[0, 0]` |
| 3 | `run_strategy([100, 99, 98, 97, 96, 95, 94, 93])` | `[-5, 2]` |
| 4 | `run_strategy([100, 99, 105, 104, 103, 102])` | `[4, 2]` |
| 5 | `run_strategy([100, 95, 100, 106, 90, 89, 95, 99])` | `[10, 2]` |
| 6 | `run_strategy([50])` | `[0, 0]` |
| 7 | `run_strategy([100, 101, 99, 100, 101])` | `[2, 1]` |
| 8 | `run_strategy([100, 96, 92, 93, 99, 98, 97, 96])` | `[-6, 2]` |

**Problem 8.2** `strategy_from_file(path)`; Python; difficulty 3; E14: `"data": { "ticks-40.csv": "content/data/coding-int/ticks-40.csv", "ticks-3.csv": "content/data/coding-int/ticks-3.csv", "ticks-header-only.csv": "content/data/coding-int/ticks-header-only.csv" }`. The level agent creates these three files with exactly the text below (the first line is the header `day,price_pence`; rows end with a newline; `ticks-header-only.csv` is the header and nothing else; `ticks-3.csv` is `0,10000`, `1,9900`, `2,10600`). Statement: "`path` is a CSV with columns `day` and `price_pence` in day order. Read the prices and return what `run_strategy` returns for them." The starter shows `run_strategy` complete (the reference above) and a stub `load_prices(path)`, so the learner writes only the reader. Reference reader:

```python
import csv

def load_prices(path):
    with open(path) as f:
        return [int(row['price_pence']) for row in csv.DictReader(f)]

def strategy_from_file(path):
    return run_strategy(load_prices(path))
```

Tests (starter, whose `load_prices` returns an empty list, fails 2 of 3; checked with the files in a working directory): `strategy_from_file('ticks-40.csv')` returns `[249, 8]`, `strategy_from_file('ticks-3.csv')` returns `[700, 1]` (buy 9,900 on day 1, sell 10,600 on day 2 because `1060000 >= 1039500`), and `strategy_from_file('ticks-header-only.csv')` returns `[0, 0]`. The 40-row file was generated by `l2_data.py` (seed 77) and is given in full for the level agent:

```text
day,price_pence
0,10279
1,10152
2,9953
3,10250
4,9940
5,9944
6,10017
7,10136
8,9855
9,9989
10,10014
11,10337
12,9948
13,10359
14,10096
15,10390
16,10422
17,10745
18,10482
19,10349
20,10011
21,10273
22,10328
23,10094
24,9854
25,9527
26,9307
27,9377
28,9350
29,9535
30,9215
31,9503
32,9916
33,10142
34,10376
35,10710
36,10368
37,10359
38,10014
39,10278
```

Each file's rows were parsed two ways (`csv.DictReader` and a `split(',')`), and the three expected values come from the reference and a second implementation that agree.

### l9-grids-and-matrices: Grids and matrices (14 min; tags `matrix-spiral`, `matrix-rotate`, `flood-border`)

Objective: Traverse, rotate and flood-fill a matrix without off-by-one errors. Method stated after use: keep four bounds (`top`, `bottom`, `left`, `right`) and shrink them after each side of a spiral; rotate a square by transposing and then reversing each row; flood fill from the cells you know are safe, here the border, instead of from the cells you doubt.

Screens (12):
1. Hook `problem`, `grid` 3 by 4 with the numbers 1 to 12; `tap-regions`: "Walk clockwise round the edge. Tap every cell on the first lap." Answer every cell except `r2c2` and `r2c3` (the numbers 6 and 7 are left for the second lap).
2. `explore`, `grid` with a stepper over the spiral; `numeric`: the last number visited in a 3 by 4 matrix is 7 (computed by the bounds method and by a visited-set walk).
3. `ladder`, `choice`: a 1 by 3 and a 3 by 1 matrix: which `if` stops the bottom row being read twice (`top < bottom`) and the left column (`left < right`).
4. `problem`, code A, `spiral_order`, `pace` 600.
5. `ladder`, `numeric` (rotation): in a 5 by 5 matrix rotated 90° clockwise, the value at row 0, column 1 moves to row 1, column 4 (zero-based): `(r, c)` goes to `(c, n - 1 - r)`. Provide `(1, 3)` to `(3, 3)` and `(4, 0)` to `(0, 0)` as the next two checks.
6. `problem`, code B, `rotate` (in place, returns nothing), `pace` 600.
7. `trap`, `choice`: building a new matrix and assigning it to the parameter name leaves the caller's matrix unchanged; the test checks the caller's list. Name the action in `byKey`.
8. `ladder`, `grid` with a border of `X` and `O` regions; `tap-regions`: tap the `O` cells that cannot be captured (those connected to the border).
9. `problem`, code C, `capture_regions`, `pace` 720.
10. `generalise` + `derive` (`order` the four-bounds loop).
11. `transfer`, `choice`: a heat map of a book's depth as a grid: which traversal prints a clockwise ring.
12. `transfer`, `numeric`: the last value of the spiral of a 300 by 300 matrix filled row by row from 0: 45,149.

Quiz (4): a bound update; the transpose and reverse; a border region count; the memory of copying versus in place.

**Problem 9.1** `spiral_order(m)`; Python; difficulty 3. Statement: "Return the entries of a rectangular matrix (list of rows) in clockwise spiral order from the top left; `[]` for no rows." Reference, starter (row-major order; fails 4 of 8), tests (the last is 300 by 300, checking the last entry, 45,149, from a visited-set walk):

```python
def spiral_order(m):
    if not m:
        return []
    top, bottom, left, right = 0, len(m) - 1, 0, len(m[0]) - 1
    out = []
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(m[top][c])
        for r in range(top + 1, bottom + 1):
            out.append(m[r][right])
        if top < bottom:
            for c in range(right - 1, left - 1, -1):
                out.append(m[bottom][c])
        if left < right:
            for r in range(bottom - 1, top, -1):
                out.append(m[r][left])
        top += 1; bottom -= 1; left += 1; right -= 1
    return out
```

```python
def spiral_order(m):
    return [x for row in m for x in row]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `spiral_order([[1, 2, 3], [4, 5, 6], [7, 8, 9]])` | `[1, 2, 3, 6, 9, 8, 7, 4, 5]` |
| 2 | `spiral_order([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])` | `[1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]` |
| 3 | `spiral_order([[1]])` | `[1]` |
| 4 | `spiral_order([[1, 2, 3]])` | `[1, 2, 3]` |
| 5 | `spiral_order([[1], [2], [3]])` | `[1, 2, 3]` |
| 6 | `spiral_order([])` | `[]` |
| 7 | `spiral_order([[1, 2], [3, 4], [5, 6], [7, 8]])` | `[1, 2, 4, 6, 8, 7, 5, 3]` |
| 8 | `m = [[r * 300 + c for c in range(300)] for r in range(300)]; spiral...` | `45149` |

**Problem 9.2** `rotate(m)`; Python; difficulty 3. Statement: "Rotate an `n` by `n` matrix 90° clockwise in place. Return nothing." Tests set up `m`, call `rotate(m)` and then read `m`, so a new list assigned to the name inside the function fails. Reference, starter (does nothing; fails 4 of 6), tests:

```python
def rotate(m):
    n = len(m)
    for r in range(n):
        for c in range(r + 1, n):
            m[r][c], m[c][r] = m[c][r], m[r][c]
    for row in m:
        row.reverse()
```

```python
def rotate(m):
    pass
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]; rotate(m); m` | `[[7, 4, 1], [8, 5, 2], [9, 6, 3]]` |
| 2 | `m = [[1, 2], [3, 4]]; rotate(m); m` | `[[3, 1], [4, 2]]` |
| 3 | `m = [[1]]; rotate(m); m` | `[[1]]` |
| 4 | `m = [[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]]...` | `[[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], ...` |
| 5 | `m = []; rotate(m); m` | `[]` |
| 6 | `m = [[r * 200 + c for c in range(200)] for r in range(200)]; rotate...` | `[39800, 39600, 39400]` |

**Problem 9.3** `capture_regions(board)`; Python; difficulty 4. Statement: "`board` is a list of equal-length strings of `X` and `O`. Every group of `O` cells (joined up, down, left and right) that does not touch the border becomes `X`. Return a new list of strings." Reference (seed from the border, stack), starter (returns the board unchanged; fails 5 of 8), tests (the last is 400 by 400 with an open interior joined to nothing at the border: no `O` survives; the reference is checked by a fixed-point brute force on 2,000 random boards):

```python
def capture_regions(board):
    rows, cols = len(board), len(board[0]) if board else 0
    safe = set()
    stack = [(r, c) for r in range(rows) for c in range(cols)
             if (r in (0, rows - 1) or c in (0, cols - 1)) and board[r][c] == 'O']
    while stack:
        r, c = stack.pop()
        if (r, c) in safe:
            continue
        safe.add((r, c))
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'O' and (nr, nc) not in safe:
                stack.append((nr, nc))
    return [''.join('O' if ch == 'O' and (r, c) in safe else ('X' if ch == 'O' else ch) for c, ch in enumerate(row))
            for r, row in enumerate(board)]
```

```python
def capture_regions(board):
    return list(board)
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `capture_regions(['XXXX', 'XOOX', 'XXOX', 'XOXX'])` | `['XXXX', 'XXXX', 'XXXX', 'XOXX']` |
| 2 | `capture_regions(['X'])` | `['X']` |
| 3 | `capture_regions(['O'])` | `['O']` |
| 4 | `capture_regions(['XXX', 'XOX', 'XXX'])` | `['XXX', 'XXX', 'XXX']` |
| 5 | `capture_regions(['OOO', 'OXO', 'OOO'])` | `['OOO', 'OXO', 'OOO']` |
| 6 | `capture_regions(['XOXO', 'OXOX', 'XOXO'])` | `['XOXO', 'OXXX', 'XOXO']` |
| 7 | `capture_regions(['XXXXX', 'XOOOX', 'XOXOX', 'XOOOX', 'XXXXX'])` | `['XXXXX', 'XXXXX', 'XXXXX', 'XXXXX', 'XXXXX']` |
| 8 | `b = ['X' * 400] + ['X' + 'O' * 398 + 'X'] * 398 + ['X' * 400]; sum(...` | `0` |

### l10-matching-engine: A matching engine (15 min; tags `book-events`, `price-levels`, `amend-priority`)

Objective: Simulate price-time priority matching of limit and market orders. Skills `ci-strings` and `ci-design`. Method stated after use: one queue per price level, a map from price to queue for each side, and a map from order id to where it rests; a limit order trades against the best opposite levels it crosses, oldest first, at the resting price, and the rest rests; a market order trades until filled or the other side is empty, and its remainder is dropped.

The event format (use these codes in the statement, in Python and in C++; every field is a whole number, ids are unique, `side` is 0 for buy and 1 for sell, prices are whole pence): `[0, id, side, price, qty]` limit order; `[1, id, side, qty]` market order; `[2, id]` cancel (ignored if the id does not rest); `[3, id, new_qty]` amend (ignored if the id does not rest): a smaller quantity keeps the place in the queue, an equal quantity changes nothing, a larger quantity loses the place and joins the back of the same level. A trade is `[taker_id, maker_id, price, qty]`. `run_book(events)` returns the trades in order; `levels(events, side)` returns the resting levels of one side after all events as `[price, total_qty]`, best first.

Screens (12):
1. Hook `problem`, `orderbook` with asks 3 at 100 (id 1) and 4 at 100 (id 2) (level labels `#1`, `#2`); `numeric`: a buy limit of 5 at 100 leaves how many at the ask level: 2.
2. `explore`, `orderbook` with a market order control; the learner watches fills at each level.
3. `ladder`, `table` widget: trades produced by the stream `[[0,1,1,101,4],[0,2,1,102,6],[0,3,0,102,7]]`: `[3,1,101,4]` and `[3,2,102,3]`; the buy of 7 is filled in full, and 3 remain on the ask side at 102.
4. `ladder`, `choice`: the maker's price is the trade price (the buyer pays 101, not 102).
5. `ladder`, `numeric`: one bid of 10 at 99, then a market sell of 4, then a market sell of 20 (`[[0,1,0,99,10],[1,2,1,4],[1,3,1,20]]`): the trades are 4 and 6, the other 14 is dropped, and the bid side ends empty. Ask for the total traded: 10.
6. `trap`, `choice`: amend a quantity up from 5 to 8 at the front of a level: the order loses its place. With two sells of 5 at 101 and a buy of 6, the amended order trades 1 and the other 5. Name the action in `byKey`.
7. `problem`, code A, Python `run_book` and `levels`, `pace` 900, difficulty 4.
8. `ladder`, code A in C++ (same twelve tests): `std::map<int, std::deque<Resting>>` and `std::unordered_map` for ids.
9. `generalise` + `derive` (`order` the matching loop).
10. `transfer`, `choice`: heaps with lazy deletion (`ds` l18) against price-level queues: which makes cancel by id cheaper and amend simpler (the queue), and which needs `O(log n)` per best-price query (a plain dict needs a scan; the map gives it).
11. `transfer`, `numeric`: after `[[0,1,0,100,2],[0,2,0,99,3],[0,3,1,99,4],[0,4,1,100,1]]` the best bid is 99 and the best ask is 100, so the spread is 1 penny; the total traded is 4.
12. `transfer`, `choice`: the hidden requirements an interviewer adds next (self-trade prevention, immediate-or-cancel, order modification time stamps): which changes one function (a rule in the matching loop) and which changes the data structure.

Quiz (4): trade price; leftover of a market order; a cancelled order that does not rest; the amend rules.

**Problem 10.1** `run_book(events)` and `levels(events, side)`; Python and C++ twin; difficulty 4. Python reference (price-level queues), starter (both functions return an empty list; fails 10 of 12), and the twelve tests, which are the same in C++ (`call: "run_book"`, `args: [<events>]`, `types: ["std::vector<std::vector<int>>"]`; rows of different lengths; for `levels`, `args: [<events>, side]` and `types: ["std::vector<std::vector<int>>", "int"]`):

```python
from collections import deque

def _simulate(events):
    books = {0: {}, 1: {}}            # side -> price -> deque of [id, qty]
    where = {}                        # id -> (side, price)
    trades = []

    def match(taker, side, qty, limit):
        opp = books[1 - side]
        while qty > 0 and opp:
            best = min(opp) if side == 0 else max(opp)
            if limit is not None and ((side == 0 and best > limit) or (side == 1 and best < limit)):
                break
            queue = opp[best]
            while qty > 0 and queue:
                maker = queue[0]
                fill = min(qty, maker[1])
                trades.append([taker, maker[0], best, fill])
                qty -= fill
                maker[1] -= fill
                if maker[1] == 0:
                    queue.popleft()
                    del where[maker[0]]
            if not queue:
                del opp[best]
        return qty

    for ev in events:
        kind = ev[0]
        if kind == 0:
            _, oid, side, price, qty = ev
            rest = match(oid, side, qty, price)
            if rest > 0:
                books[side].setdefault(price, deque()).append([oid, rest])
                where[oid] = (side, price)
        elif kind == 1:
            _, oid, side, qty = ev
            match(oid, side, qty, None)
        elif kind == 2:
            oid = ev[1]
            if oid in where:
                side, price = where.pop(oid)
                queue = books[side][price]
                for k, o in enumerate(queue):
                    if o[0] == oid:
                        del queue[k]
                        break
                if not queue:
                    del books[side][price]
        else:
            _, oid, new_qty = ev
            if oid in where:
                side, price = where[oid]
                queue = books[side][price]
                for k, o in enumerate(queue):
                    if o[0] == oid:
                        if new_qty < o[1]:
                            o[1] = new_qty
                        elif new_qty > o[1]:
                            del queue[k]
                            queue.append([oid, new_qty])
                        break
    return trades, books

def run_book(events):
    return _simulate(events)[0]

def levels(events, side):
    book = _simulate(events)[1][side]
    prices = sorted(book, reverse=(side == 0))
    return [[p, sum(o[1] for o in book[p])] for p in prices]
```

```python
def run_book(events):
    return []

def levels(events, side):
    return []
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_book([[0, 1, 0, 100, 5], [0, 2, 1, 101, 5], [0, 3, 1, 100, 3]])` | `[[3, 1, 100, 3]]` |
| 2 | `run_book([[0, 1, 1, 101, 4], [0, 2, 1, 102, 6], [0, 3, 0, 102, 7]])` | `[[3, 1, 101, 4], [3, 2, 102, 3]]` |
| 3 | `run_book([[0, 1, 1, 100, 3], [0, 2, 1, 100, 4], [0, 3, 0, 100, 5]])` | `[[3, 1, 100, 3], [3, 2, 100, 2]]` |
| 4 | `run_book([[0, 1, 0, 99, 10], [1, 2, 1, 4], [1, 3, 1, 20]])` | `[[2, 1, 99, 4], [3, 1, 99, 6]]` |
| 5 | `run_book([[0, 1, 0, 100, 5], [2, 1], [0, 2, 1, 100, 5]])` | `[]` |
| 6 | `run_book([[0, 1, 1, 101, 5], [0, 2, 1, 101, 5], [3, 1, 3], [0, 3, 0...` | `[[3, 1, 101, 3], [3, 2, 101, 3]]` |
| 7 | `run_book([[0, 1, 1, 101, 5], [0, 2, 1, 101, 5], [3, 1, 8], [0, 3, 0...` | `[[3, 2, 101, 5], [3, 1, 101, 1]]` |
| 8 | `run_book([[0, 1, 0, 100, 2], [0, 2, 0, 99, 3], [0, 3, 1, 99, 4], [0...` | `[[3, 1, 100, 2], [3, 2, 99, 2]]` |
| 9 | `levels([[0, 1, 0, 100, 5], [0, 2, 1, 101, 5], [0, 3, 1, 100, 3]], 1)` | `[[101, 5]]` |
| 10 | `levels([[0, 1, 0, 100, 2], [0, 2, 0, 99, 3], [0, 3, 1, 99, 4], [0, ...` | `[[99, 1]]` |
| 11 | `levels([[0, 1, 0, 100, 2], [0, 2, 0, 99, 3], [0, 3, 1, 99, 4], [0, ...` | `[[100, 1]]` |
| 12 | `levels([[0, 1, 0, 99, 10], [1, 2, 1, 4], [1, 3, 1, 20]], 0)` | `[]` |

C++ reference and starter (the same signatures, `std::vector<std::vector<int>> run_book(std::vector<std::vector<int>> events)` and `std::vector<std::vector<int>> levels(std::vector<std::vector<int>> events, int side)`; the starter returns `{}` and fails 10 of 12). The reference was compiled under `-std=c++17` and `-std=c++20`, matched the twelve tests, and matched the brute force on 300 random event streams:

```cpp
#include <vector>
#include <map>
#include <deque>
#include <unordered_map>
#include <algorithm>
struct Resting { int id; int qty; };
struct Engine {
    std::map<int, std::deque<Resting>> bids, asks;
    std::unordered_map<int, std::pair<int, int>> where;
    std::vector<std::vector<int>> trades;
    int match(int taker, int side, int qty, bool has_limit, int limit) {
        while (qty > 0) {
            if (side == 0 ? asks.empty() : bids.empty()) break;
            int best = side == 0 ? asks.begin()->first : bids.rbegin()->first;
            if (has_limit && ((side == 0 && best > limit) || (side == 1 && best < limit))) break;
            auto& queue = side == 0 ? asks[best] : bids[best];
            while (qty > 0 && !queue.empty()) {
                Resting& m = queue.front();
                int fill = std::min(qty, m.qty);
                trades.push_back({taker, m.id, best, fill});
                qty -= fill; m.qty -= fill;
                if (m.qty == 0) { where.erase(m.id); queue.pop_front(); }
            }
            if (queue.empty()) { if (side == 0) asks.erase(best); else bids.erase(best); }
        }
        return qty;
    }
    std::map<int, std::deque<Resting>>& book(int side) { return side == 0 ? bids : asks; }
    void apply(const std::vector<int>& ev) {
        if (ev[0] == 0) {
            int rest = match(ev[1], ev[2], ev[4], true, ev[3]);
            if (rest > 0) { book(ev[2])[ev[3]].push_back({ev[1], rest}); where[ev[1]] = {ev[2], ev[3]}; }
        } else if (ev[0] == 1) {
            match(ev[1], ev[2], ev[3], false, 0);
        } else if (ev[0] == 2) {
            auto it = where.find(ev[1]);
            if (it == where.end()) return;
            auto& q = book(it->second.first)[it->second.second];
            q.erase(std::find_if(q.begin(), q.end(), [&](const Resting& r) { return r.id == ev[1]; }));
            if (q.empty()) book(it->second.first).erase(it->second.second);
            where.erase(it);
        } else {
            auto it = where.find(ev[1]);
            if (it == where.end()) return;
            auto& q = book(it->second.first)[it->second.second];
            auto pos = std::find_if(q.begin(), q.end(), [&](const Resting& r) { return r.id == ev[1]; });
            if (ev[2] < pos->qty) pos->qty = ev[2];
            else if (ev[2] > pos->qty) { q.erase(pos); q.push_back({ev[1], ev[2]}); }
        }
    }
};
std::vector<std::vector<int>> run_book(std::vector<std::vector<int>> events) {
    Engine e;
    for (const auto& ev : events) e.apply(ev);
    return e.trades;
}
std::vector<std::vector<int>> levels(std::vector<std::vector<int>> events, int side) {
    Engine e;
    for (const auto& ev : events) e.apply(ev);
    std::vector<std::vector<int>> out;
    auto add = [&](int price, const std::deque<Resting>& q) { int t = 0; for (const auto& r : q) t += r.qty; out.push_back({price, t}); };
    if (side == 0) for (auto it = e.bids.rbegin(); it != e.bids.rend(); ++it) add(it->first, it->second);
    else for (const auto& kv : e.asks) add(kv.first, kv.second);
    return out;
}
```

```cpp
#include <vector>
std::vector<std::vector<int>> run_book(std::vector<std::vector<int>> events) {
    return {};
}
std::vector<std::vector<int>> levels(std::vector<std::vector<int>> events, int side) {
    return {};
}
```

Checks: the Python reference and a brute force that rescans a flat list for the best price and earliest sequence agree on 4,000 random streams (limit, market, cancel and amend mixed).

### Level 2 review (`review-2.json`, 10 items, difficulty 2 to 4, interleaving all five lessons, every case unseen in the lessons, each with `tags` and `skills`)

| # | Lesson | Widget | d | Prompt (summary) | Key |
| --- | --- | --- | --- | --- | --- |
| 1 | l6 | `numeric` | 2 | How many windows of `abab` are anagrams of `ab`? | 3 (starts 0, 1 and 2) |
| 2 | l6 | `numeric` | 3 | How many palindromic substrings has `abcba`? | 7 (`a`, `b`, `c`, `b`, `a`, `bcb`, `abcba`; by centres and by listing) |
| 3 | l6 | `multi` | 3 | Which can be rearranged into a palindrome: `civic`, `ivicc`, `aabbcd`, `abcde`, `xxyyz`? | `civic`, `ivicc`, `xxyyz` (checked by counting odd letters and by trying every arrangement) |
| 4 | l7 | `numeric` | 3 | `(8+2)*(9-4)/5-3`. | 7 (`10 * 5 / 5 - 3`) |
| 5 | l7 | `numeric` | 3 | Length of the decode of `2[x3[y]]z`. | 9 (`2 * (1 + 3) + 1`; by repeated replacement) |
| 6 | l7 | `numeric` | 3 | `-9/4` when division truncates toward zero. | -2 (floor division gives -3) |
| 7 | l8 | `numeric` | 3 | Profit in pence of the bot on `[100, 95, 100, 106, 90, 89, 95, 99]`. | 10 (two trades: 95 to 100, then 90 to 95) |
| 8 | l9 | `numeric` | 2 | Last entry of the clockwise spiral of the 4 by 3 matrix with rows `1 2 3`, `4 5 6`, `7 8 9`, `10 11 12`. | 8 (the spiral is `1 2 3 6 9 12 11 10 7 4 5 8`; by the bounds method and a visited-set walk) |
| 9 | l9 | `choice` | 3 | A 5 by 5 matrix is rotated 90° clockwise: where does the entry at row 2, column 3 go (zero-based)? | row 3, column 2 (`(r, c)` goes to `(c, n - 1 - r)`). Distractors: row 2, column 1 (a counter-clockwise turn); row 3, column 3 (a transpose); row 1, column 2. |
| 10 | l10 | `numeric` | 3 | Three sells of 4 at 100 (ids 1, 2, 3 in that order); id 1 is amended down to 2; a buy of 7 at 100 arrives. How many does id 3 trade? | 1 (id 1 keeps its place and trades 2, id 2 trades 4, id 3 trades 1; by the engine and by hand) |

### Level 2 homework (`homework-2.json`, 8 items, difficulty 3 to 5 with at least one 5, `tags` on each; three `code` items, one `longform`)

| # | Lesson | Kind | d | Item | Key or reference |
| --- | --- | --- | --- | --- | --- |
| 1 | l7 | `code` | 3 | `simplify_path(path)` (below). | tests below |
| 2 | l9 | `code` | 4 | `life_step(board)` (below). | tests below |
| 3 | l7 | `code` | 5 | `longest_valid_parentheses(s)` (below). | tests below |
| 4 | l8 | `longform` | 4 | Say aloud, timing yourself to three minutes, how you read a long statement: state, events, order of checks, a hand trace. Use the bot on `[100, 99, 99, 99, 98, 97]`. | Model: state is long or flat, entry price and buy day; the event is a day's price; the order is take profit, stop, time; the trace buys 99 on day 1, sells 98 on day 4 for -1, buys 97 on day 5 and sells it at the end: `[-1, 2]`. Rubric (10): 2 names the state, 2 the events, 2 the order of checks, 2 a hand trace with the numbers, 2 the end-of-data rule. |
| 5 | l9 | `numeric` | 4 | Last entry of the clockwise spiral of a 300 by 300 matrix filled row by row from 0. | 45,149 (the bounds method and a visited-set walk) |
| 6 | l7 | `order` | 4 | Decode with a stack: on a digit build the count; on `[` push the text so far and the count and start fresh; on `]` pop, repeat the current text count times and append it to the popped text; on a letter append; return the text. | Distractor: "push the digits as characters onto the stack" with its `why` (a count of 12 splits into 1 and 2). |
| 7 | l10 | `numeric` | 4 | After `[[0,1,0,100,2],[0,2,0,99,3],[0,3,1,99,4],[0,4,1,100,1]]`, what quantity has traded in total? | 4 (trades `[3,1,100,2]` and `[3,2,99,2]`; the spread is then 1) |
| 8 | l8 | `choice` | 3 | For prices `[100, 99, 99, 99, 98, 97]`, which result does the correct rule (`i - bought == 3`) give? | `[-1, 2]`. Distractors: `[-2, 1]` (the rule written `> 3`), `[0, 1]`, `[-1, 1]`. |

**Problem H2.1** `simplify_path(path)`; Python; difficulty 3. Statement: "`path` is an absolute Unix path starting with `/`. `.` means here, `..` means up one folder (the root stays the root), repeated slashes count as one, a name such as `...` is an ordinary name. Return the shortest equivalent path with no trailing slash (the root is `/`)." Reference, starter (returns the path unchanged; fails 5 of 7), tests (brute: `posixpath.normpath` on 3,000 random paths):

```python
def simplify_path(path):
    stack = []
    for part in path.split('/'):
        if part == '..':
            if stack:
                stack.pop()
        elif part and part != '.':
            stack.append(part)
    return '/' + '/'.join(stack)
```

```python
def simplify_path(path):
    return path
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `simplify_path('/home/')` | `'/home'` |
| 2 | `simplify_path('/home//foo/')` | `'/home/foo'` |
| 3 | `simplify_path('/a/./b/../../c/')` | `'/c'` |
| 4 | `simplify_path('/../')` | `'/'` |
| 5 | `simplify_path('/.../a/..')` | `'/...'` |
| 6 | `simplify_path('/a/b/c')` | `'/a/b/c'` |
| 7 | `simplify_path('/')` | `'/'` |

**Problem H2.2** `life_step(board)`; Python; difficulty 4. Statement: "`board` is a rectangle of 0 and 1. One step of the Game of Life: a live cell with 2 or 3 live neighbours (of 8) lives; a dead cell with exactly 3 becomes live; the border has no neighbours beyond it. Return the new board." Reference, starter (returns a copy; fails 5 of 7), tests (brute: counts neighbours with a `Counter` over live cells; the last case is 100 by 100 and sums the live cells):

```python
def life_step(board):
    rows, cols = len(board), len(board[0])
    def live_neighbours(r, c):
        n = 0
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if (dr or dc) and 0 <= r + dr < rows and 0 <= c + dc < cols:
                    n += board[r + dr][c + dc]
        return n
    return [[1 if (live_neighbours(r, c) == 3 or (board[r][c] and live_neighbours(r, c) == 2)) else 0
             for c in range(cols)] for r in range(rows)]
```

```python
def life_step(board):
    return [row[:] for row in board]
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `life_step([[0, 1, 0], [0, 1, 0], [0, 1, 0]])` | `[[0, 0, 0], [1, 1, 1], [0, 0, 0]]` |
| 2 | `life_step([[1, 1], [1, 1]])` | `[[1, 1], [1, 1]]` |
| 3 | `life_step([[0, 0, 0], [0, 0, 0]])` | `[[0, 0, 0], [0, 0, 0]]` |
| 4 | `life_step([[1, 0], [0, 0]])` | `[[0, 0], [0, 0]]` |
| 5 | `life_step([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]])` | `[[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]` |
| 6 | `life_step([[1, 1, 1]])` | `[[0, 1, 0]]` |
| 7 | `b = [[(r * 7 + c * 3) % 5 % 2 for c in range(100)] for r in range(1...` | `4079` |

**Problem H2.3** `longest_valid_parentheses(s)`; Python; difficulty 5. Statement: "`s` holds `(` and `)`. Return the length of the longest valid (well-formed, contiguous) bracket substring." Reference (a stack of indices with a base of -1), starter (twice the number of `()` pairs; fails 5 of 10), tests (the last is `(` repeated 50,000 times then `)` 50,000 times, answer 100,000, which stops a cubic checker):

```python
def longest_valid_parentheses(s):
    stack = [-1]
    best = 0
    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return best
```

```python
def longest_valid_parentheses(s):
    return s.count('()') * 2
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `longest_valid_parentheses('(()')` | `2` |
| 2 | `longest_valid_parentheses(')()())')` | `4` |
| 3 | `longest_valid_parentheses('')` | `0` |
| 4 | `longest_valid_parentheses('()(())')` | `6` |
| 5 | `longest_valid_parentheses('(()(((()')` | `2` |
| 6 | `longest_valid_parentheses('()(()')` | `2` |
| 7 | `longest_valid_parentheses(')(')` | `0` |
| 8 | `longest_valid_parentheses('((()))')` | `6` |
| 9 | `longest_valid_parentheses('())((())')` | `4` |
| 10 | `s = '(' * 50000 + ')' * 50000; longest_valid_parentheses(s)` | `100000` |

### Level 2 report notes

Report as `docs/LEVEL-BRIEF.md` says. Add to the report any difference between the clang and wasm run and the `g++` runs of the matching engine. Do not edit files outside `app/content/courses/coding-int/` and `app/content/data/coding-int/`.

## Level 3

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `coding-int` (topic 3.5), level 3 ("Design in code"): lessons `l11-lru-cache`, `l12-file-system`, `l13-requirements-change`, `l14-rate-limiter`, plus `review-3.json` and `homework-3.json`, in `app/content/courses/coding-int/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids of `course.json` exactly. Use £ for money (prices in l13 are whole £). Scripts: `l3.py` (every problem of this level; the C++ LRU; random cross-checks), `harness.py`, `numbers_check.py`.

Level promise. Interviews at developer and strats desks and at some trading firms set a design problem in code: several small classes, a clear interface, and a requirement that arrives half-way. This level builds four such systems and teaches how to keep code open to change. Python by default; the LRU cache has a C++ twin.

**Engine features.** E11 (`parts`) in homework item 5. E3, E8 and E14 are not needed. Existing: `code` (a hidden driver in `postlude` replays operations; `__learner_source__` checks; C++ `postlude` driver), `array` (linked mode) for lists, `tree` for the folder tree, `table`, `order`, `choice`, `multi`, `longform`. Staged problems (l12, l13) use one `code` screen per stage; each later stage's starter is the reference solution of the previous stage plus stubs for the new methods, so every screen is self-contained.

**Builds on (by id) and what is new.**

| Lesson | Builds on | New over those |
| --- | --- | --- |
| l11-lru-cache | `ds` homework-3 h-lru (the Python LRU with sentinels), `ds` l12-nodes-and-pointers, `cpp` l15-maps | A from-memory recall against the clock, the C++ version with `std::list::splice` and an iterator map, a TTL cache where recency order is also expiry order, and LFU in homework. |
| l12-file-system | `py-found` l12-data-with-behaviour, `ds` l14-binary-trees, `ds` l16-tree-recursion | A tree of nodes that are folders or files, paths split on `/`, `mkdir -p` and append semantics, a recursive size. |
| l13-requirements-change | `py-found` l8-who-changes-the-list, `contests` l16-upsolving | Extending working code in three stages (positions, average cost, FIFO lots) so that earlier tests keep passing. |
| l14-rate-limiter | `ds` l11-first-in-first-out (the single-client sliding log), `ds` l7-prefix-sums | Per-client logs, fixed window against sliding log against token bucket with numbers, a token bucket in code, a ring-buffer hit counter in homework. |

### l11-lru-cache: A least recently used cache (14 min; tags `lru-cache`, `cache-ttl`, `cache-lfu`)

Objective: Combine a hash map and a linked list for constant-time get and put. The learner built this in `ds` homework-3; the lesson is the interview version: from memory, against a pace of 480 seconds, then in C++, then with expiry. Method stated after use: the dict maps a key to its node, the doubly linked list orders nodes by recency (head side most recent), sentinels remove the empty-list special cases, and every get or put moves its node to the front; when full, drop the node before the tail sentinel.

Screens (11):
1. Hook `problem`, `array` (linked mode) holding keys 2, 5, 9, most recent first; `order`: put the steps of `get` of key 9 in order (look up the node, unlink it, push it to the front, return its value; return -1 first if the key is absent).
2. `explore`, `array` with pointers `head` and `tail`; `choice`: which pointer assignments unlink a node (four assignments; the learner who writes only two leaves a dangling `prev`).
3. `problem`, code A, Python `LRUCache` (`pace` 480; no `OrderedDict`; the hidden tests check `'OrderedDict' not in __learner_source__`). Prose names `ds` homework-3 and says an interviewer often forbids the library class.
4. `ladder`, `numeric`: a cache of capacity 1 with the operations put 2 (value 1), get 2, put 3 (value 2), get 2, get 3: the gets return `1, -1, 2`; ask how many gets miss: 1.
5. `ladder`, code A in C++ (same tests): `std::list<std::pair<int,int>>` and `std::unordered_map<int, std::list<...>::iterator>`; `splice` moves a node in `O(1)` without invalidating iterators. Prose says why `std::list` iterators stay valid.
6. `trap`, `choice`: `put` of an existing key must update the value and move it to the front, not evict; the learner who evicts first on a full cache loses a live key (capacity 2: puts 1, 2, then 1 again). Name the action in `byKey`.
7. `problem`, code B, Python `TTLCache` (below): a use refreshes the entry.
8. `ladder`, `choice`: why the expired entries are exactly a suffix of the recency list (the time of last use is non-decreasing from the tail to the head); the learner picks the sentence that says so.
9. `generalise` + `derive` (`order` the steps of a `put`).
10. `transfer`, `choice`: LFU against LRU for a pricing service with a few very hot symbols and a long tail of scans; why a scan evicts hot keys under LRU (the lesson leads into homework item 1).
11. `transfer`, `numeric`: with a cache of 1,000 entries, 100,000 puts of keys 0 to 99,999, then gets of keys 99,000 to 99,999 and of key 0: the surviving keys are 99,000 to 99,999 and key 0 is gone, so the gets sum to 99,499,499 (`99,499,500 - 1`; by the closed form and by running the reference).

Quiz (4): a trace; a pointer update; capacity 1; the expiry rule.

**Problem 11.1** `LRUCache(capacity)` with `get(key)` and `put(key, value)`; Python and C++ twin; difficulty 4. Statement: "`get` returns the value or -1 and counts as a use; `put` inserts or updates and counts as a use; at capacity, `put` of a new key first drops the least recently used entry. Both are `O(1)`." Driver `run_lru(cap, ops)`: `ops` rows are `[0, key, value]` for `put` and `[1, key]` for `get`; the driver returns the list of `get` results. Reference (sentinels, no library class):

```python
class _Node:
    def __init__(self, key=0, value=0):
        self.key, self.value = key, value
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.map = {}
        self.head, self.tail = _Node(), _Node()       # sentinels: head.next is the most recent
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value):
        node = self.map.get(key)
        if node is not None:
            node.value = value
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.capacity:
            last = self.tail.prev
            self._unlink(last)
            del self.map[last.key]
        node = _Node(key, value)
        self.map[key] = node
        self._push_front(node)
```

Driver (`postlude`):

```python
def run_lru(cap, ops):
    c = LRUCache(cap)
    out = []
    for op in ops:
        if op[0] == 0:
            c.put(op[1], op[2])
        else:
            out.append(c.get(op[1]))
    return out
```

Starter (a plain dict that never evicts; fails 6 of 8):

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}

    def get(self, key):
        return self.data.get(key, -1)

    def put(self, key, value):
        self.data[key] = value
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_lru(2, [[0, 1, 1], [0, 2, 2], [1, 1], [0, 3, 3], [1, 2], [0, 4,...` | `[1, -1, -1, 3, 4]` |
| 2 | `run_lru(1, [[0, 2, 1], [1, 2], [0, 3, 2], [1, 2], [1, 3]])` | `[1, -1, 2]` |
| 3 | `run_lru(2, [[0, 2, 1], [0, 2, 2], [1, 2], [0, 1, 1], [0, 4, 1], [1,...` | `[2, -1]` |
| 4 | `run_lru(3, [[0, 1, 10], [0, 2, 20], [0, 3, 30], [1, 1], [0, 4, 40],...` | `[10, -1, 10, 30, 40]` |
| 5 | `run_lru(2, [[1, 9]])` | `[-1]` |
| 6 | `run_lru(2, [[0, 1, 1], [0, 2, 2], [0, 1, 5], [0, 3, 3], [1, 1], [1,...` | `[5, -1, 3]` |
| 7 | `ops = [[0, i, i] for i in range(100000)] + [[1, i] for i in range(9...` | `99499499` |
| 8 | `'OrderedDict' not in __learner_source__` | `True` |

C++ twin: the same seven cases without the source check (six trace cases and the large case: 100,000 puts, 1,000 gets of the newest keys and one get of key 0, summed into a `long long`, expected 99,499,499). Driver in `postlude`, reference, starter (a plain `unordered_map`, fails 6 of 7). Compiled and run under `-std=c++17` and `-std=c++20`; the expected values come from the brute force `lru_brute` (a list of keys, `O(n)` per operation) on the small cases and from the closed form on the large one.

```cpp
#include <list>
#include <unordered_map>
#include <vector>
class LRUCache {
public:
    explicit LRUCache(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = index_.find(key);
        if (it == index_.end()) return -1;
        items_.splice(items_.begin(), items_, it->second);
        return it->second->second;
    }
    void put(int key, int value) {
        auto it = index_.find(key);
        if (it != index_.end()) {
            it->second->second = value;
            items_.splice(items_.begin(), items_, it->second);
            return;
        }
        if ((int)items_.size() == capacity_) {
            index_.erase(items_.back().first);
            items_.pop_back();
        }
        items_.emplace_front(key, value);
        index_[key] = items_.begin();
    }
private:
    int capacity_;
    std::list<std::pair<int, int>> items_;
    std::unordered_map<int, std::list<std::pair<int, int>>::iterator> index_;
};
```

```cpp
#include <list>
#include <unordered_map>
#include <vector>
class LRUCache {
public:
    explicit LRUCache(int capacity) : capacity_(capacity) {}
    int get(int key) {
        auto it = data_.find(key);
        return it == data_.end() ? -1 : it->second;
    }
    void put(int key, int value) { data_[key] = value; }
private:
    int capacity_;
    std::unordered_map<int, int> data_;
};
```

```cpp
std::vector<int> run_lru(int cap, std::vector<std::vector<int>> ops) {
    LRUCache c(cap);
    std::vector<int> out;
    for (const auto& op : ops) {
        if (op[0] == 0) c.put(op[1], op[2]);
        else out.push_back(c.get(op[1]));
    }
    return out;
}
```

**Problem 11.2** `TTLCache(capacity, ttl)` with `get(key, now)` and `put(key, value, now)`; Python; difficulty 4. Statement: "Times are whole seconds and never go backwards. An entry that was last used (by `get` or `put`) `ttl` or more seconds ago has expired: `get` returns -1 for it and it takes no room. A use refreshes the entry and makes it the most recent. When a new key arrives and the cache is full after expired entries are dropped, drop the least recently used." Driver `run_ttl(cap, ttl, ops)` with rows `[0, key, value, now]` and `[1, key, now]`. Reference (purges from the tail, which is enough because the order of last use is the order of expiry), starter (a dict, fails 6 of 6), tests (brute force: purges every expired key in a list on each call; 4,000 random runs agreed):

```python
class _Node:
    def __init__(self, key=0, value=0, touched=0):
        self.key, self.value, self.touched = key, value, touched
        self.prev = self.next = None

class TTLCache:
    def __init__(self, capacity, ttl):
        self.capacity, self.ttl = capacity, ttl
        self.map = {}
        self.head, self.tail = _Node(), _Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _push_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _purge(self, now):
        while self.tail.prev is not self.head and now - self.tail.prev.touched >= self.ttl:
            last = self.tail.prev
            self._unlink(last)
            del self.map[last.key]

    def get(self, key, now):
        self._purge(now)
        node = self.map.get(key)
        if node is None:
            return -1
        node.touched = now
        self._unlink(node)
        self._push_front(node)
        return node.value

    def put(self, key, value, now):
        self._purge(now)
        node = self.map.get(key)
        if node is not None:
            node.value, node.touched = value, now
            self._unlink(node)
            self._push_front(node)
            return
        if len(self.map) == self.capacity:
            last = self.tail.prev
            self._unlink(last)
            del self.map[last.key]
        node = _Node(key, value, now)
        self.map[key] = node
        self._push_front(node)
```

```python
def run_ttl(cap, ttl, ops):
    c = TTLCache(cap, ttl)
    out = []
    for op in ops:
        if op[0] == 0:
            c.put(op[1], op[2], op[3])
        else:
            out.append(c.get(op[1], op[2]))
    return out
```

```python
class TTLCache:
    def __init__(self, capacity, ttl):
        self.capacity, self.ttl = capacity, ttl
        self.data = {}

    def get(self, key, now):
        return self.data.get(key, -1)

    def put(self, key, value, now):
        self.data[key] = value
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_ttl(2, 5, [[0, 1, 10, 0], [0, 2, 20, 1], [1, 1, 4], [1, 2, 6], ...` | `[10, -1, 10]` |
| 2 | `run_ttl(2, 5, [[0, 1, 10, 0], [1, 1, 5]])` | `[-1]` |
| 3 | `run_ttl(2, 5, [[0, 1, 10, 0], [1, 1, 4], [1, 1, 8], [1, 1, 13], [1,...` | `[10, 10, -1, -1]` |
| 4 | `run_ttl(2, 10, [[0, 1, 1, 0], [0, 2, 2, 1], [0, 3, 3, 2], [1, 1, 3]...` | `[-1, 2, 3]` |
| 5 | `run_ttl(2, 3, [[0, 1, 1, 0], [0, 2, 2, 2], [0, 3, 3, 3], [1, 1, 3],...` | `[-1, 2, 3]` |
| 6 | `run_ttl(3, 4, [[0, 1, 1, 0], [0, 2, 2, 1], [0, 3, 3, 2], [1, 1, 3],...` | `[1, -1, 1, 4, 3]` |

### l12-file-system: An in-memory file system (14 min; tags `file-system`, `path-tree`, `recursive-size`)

Objective: Design classes for a small file system with paths, folders and files. Method stated after use: one `Node` class with a dict of children and a `content` that is `None` for a folder and a string for a file; a helper walks a path one name at a time and may create what is missing; every public method is a few lines on top of the helper.

Screens (10):
1. Hook `problem`, `tree` of `/a/b/c` with a file `d.txt` under `c`; `tap-regions`: tap the nodes `ls('/a')` lists (`b` only).
2. `explore`, `tree` with a control stepping `mkdir('/a/b/c')`; `numeric`: how many folders exist afterwards (3: `a`, `b`, `c`).
3. `ladder`, `choice`: `ls` of a file path returns the file name in a list, of a folder the sorted names inside it.
4. `ladder`, `choice`: `write` to a path whose folders do not exist creates them (like `mkdir -p`) and appends to a file that exists; the second write of `' world'` makes `'hello world'`.
5. `problem`, code A, Python `FileSystem` with `mkdir`, `write`, `read`, `ls`, `pace` 840, difficulty 4.
6. `trap`, `choice`: `'/'.split('/')` returns two empty strings; a path walker that does not skip empty names looks for a child named `''`. Name the action in `byKey`.
7. `ladder`, `numeric`: files `/logs/a.txt` (`abcd`), `/logs/old/b.txt` (`xy`) and `/logs/c.txt` (`abcdef`): `size('/logs')` is 12 and `size('/logs/old')` is 2 (by the tree and by adding the lengths).
8. `problem`, code B, extend the class with `size(path)` (recursive; the starter is the reference of A without `size`).
9. `generalise` + `derive` (`order` the walk).
10. `transfer`, `choice`: a design question an interviewer asks next ("add `rm`", "add `find(name)`", "add file permissions"): the learner sorts each into "one new method" or "a new field on `Node`".

Quiz (4): a path split; `ls` of a file; `mkdir` twice; a size.

**Problem 12.1** `FileSystem` with `mkdir(path)`, `write(path, text)`, `read(path)`, `ls(path)` (stage A) and `size(path)` (stage B); Python; difficulty 4. Statement: "Absolute paths start with `/`, the root is `/`. `mkdir` creates every missing folder and does nothing if the folder exists. `write` creates missing folders and the file and appends `text` to its content. `read` returns a file's content. `ls` of a folder returns the names inside it sorted (files and folders together); `ls` of a file returns a one-element list with its name. `size` of a file is the number of characters of its content; of a folder the total of every file below it. Inputs are valid: no operation uses a file as a folder." Driver `run_fs(ops)` with rows `('mkdir', path)`, `('write', path, text)`, `('ls', path)`, `('read', path)`, `('size', path)`, returning the results of `ls`, `read` and `size`. Reference, driver, starter (fails 5 of 6; stage A tests are rows 1 to 4 and 6, stage B adds row 5), tests (brute force: flat sets of folders and a dict of files keyed by the full path; 3,000 random valid sequences agreed):

```python
class _Node:
    def __init__(self):
        self.children = {}
        self.content = None          # None for a folder, a string for a file

class FileSystem:
    def __init__(self):
        self.root = _Node()

    def _walk(self, path, create=False):
        node = self.root
        for name in path.split('/'):
            if not name:
                continue
            if name not in node.children:
                if not create:
                    return None
                node.children[name] = _Node()
            node = node.children[name]
        return node

    def mkdir(self, path):
        self._walk(path, create=True)

    def write(self, path, text):
        node = self._walk(path, create=True)
        node.content = (node.content or '') + text

    def read(self, path):
        return self._walk(path).content

    def ls(self, path):
        node = self._walk(path)
        if node.content is not None:
            return [path.rstrip('/').split('/')[-1]]
        return sorted(node.children)

    def size(self, path):
        node = self._walk(path)
        def total(n):
            if n.content is not None:
                return len(n.content)
            return sum(total(c) for c in n.children.values())
        return total(node)
```

```python
def run_fs(ops):
    fs = FileSystem()
    out = []
    for op in ops:
        if op[0] == 'mkdir': fs.mkdir(op[1])
        elif op[0] == 'write': fs.write(op[1], op[2])
        elif op[0] == 'ls': out.append(fs.ls(op[1]))
        elif op[0] == 'read': out.append(fs.read(op[1]))
        else: out.append(fs.size(op[1]))
    return out
```

```python
class FileSystem:
    def __init__(self):
        self.files = {}

    def mkdir(self, path):
        pass

    def write(self, path, text):
        self.files[path] = text

    def read(self, path):
        return self.files[path]

    def ls(self, path):
        return []

    def size(self, path):
        return 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_fs([('mkdir', '/a/b/c'), ('ls', '/'), ('ls', '/a'), ('write', '...` | `[['a'], ['b'], ['d.txt'], ['d.txt'], 'hello wor...` |
| 2 | `run_fs([('write', '/x.txt', 'abc'), ('ls', '/'), ('read', '/x.txt')])` | `[['x.txt'], 'abc']` |
| 3 | `run_fs([('ls', '/')])` | `[[]]` |
| 4 | `run_fs([('mkdir', '/a/b'), ('mkdir', '/a/b'), ('write', '/a/z.txt',...` | `[['b', 'z.txt']]` |
| 5 | `run_fs([('write', '/docs/n/a.txt', '12345'), ('write', '/docs/n/b.t...` | `[9, 8, 1, 9, ['c.txt', 'n']]` |
| 6 | `run_fs([('mkdir', '/b'), ('mkdir', '/a'), ('write', '/c.txt', '1'),...` | `[['a', 'b', 'c.txt']]` |

### l13-requirements-change: When the requirements change (15 min; tags `requirements-change`, `average-cost`, `fifo-lots`)

Objective: Extend working code when the interviewer adds a requirement part-way. Skills `ci-design` and `ci-timed`. Method stated after use: keep the old calls valid (a new argument gets a default), add the new behaviour behind a name, run the old tests first, and only then the new ones. The running story is a trade ledger at a small desk, prices in whole £.

Stage 1: `Ledger()` with `trade(symbol, qty)` (signed whole shares, positive buys) and `position(symbol)`. Stage 2: `trade(symbol, qty, price=0)` keeps old calls valid; add `avg_cost(symbol)` and `realised(symbol)`; a sale realises `qty * (price - average cost)`; selling more than held raises `ValueError`. Stage 3: `Ledger(method='average')` or `Ledger(method='fifo')`; under `'fifo'` a sale consumes the oldest lots first and `avg_cost` is the average of the lots still held; the earlier tests must still pass.

Screens (11):
1. Hook `problem`, `table` of three trades (buy 100 at £10, buy 100 at £12, sell 150 at £13); `numeric`: position after the three (50).
2. `problem`, code A, stage 1 (`pace` 300, difficulty 2).
3. `ladder`, `numeric`: average cost after the two buys: £11. Realised on the sale by average cost: 150 times (13 minus 11) = £300.
4. `problem`, code B, stage 2 (starter: the reference of stage 1 with the new signatures stubbed; the tests include the stage 1 test).
5. `trap`, `choice`: adding `price` as a required argument breaks every old call; the learner who does that fails the stage 1 test. Name the action in `byKey`.
6. `ladder`, `numeric`: the interviewer asks for FIFO: realised on the same trades is 100 times (13 minus 10) plus 50 times (13 minus 12) = £350; the remaining lot is 50 at £12, so `avg_cost` is £12.
7. `problem`, code C, stage 3 (the tests of stages 1 and 2 plus the FIFO cases).
8. `ladder`, `choice`: which of two designs absorbs a fourth requirement (short selling) with the fewest changes: lots held in a deque, or only a running average; the learner chooses and a `why` names the cost.
9. `generalise` + `derive` (`order` the steps of absorbing a change).
10. `transfer`, `choice`: how an interviewer scores this (reading the new requirement, keeping old tests, naming the cost) and what to say aloud in the first minute.
11. `transfer`, `numeric`: trades `(10, £50)`, `(-4, £55)`, `(10, £40)`, `(-12, £45)` give realised £20 under FIFO and £35 under average cost (the homework item has this; use a different list in the lesson, computed twice).

Quiz (4): a position; an average cost; a FIFO lot; an old call.

**Problems 13.1 to 13.3** `Ledger`, three stages; Python; difficulty 2, 3 and 4. Tests use a `setup` line that builds a `Ledger` and replays trades, and a call that reads `[position, avg_cost, realised]` with `compare: "isclose"`. Stage 1 reference and starter (fails 2 of 3), tests:

```python
class Ledger:
    def __init__(self):
        self.pos = {}

    def trade(self, symbol, qty):
        self.pos[symbol] = self.pos.get(symbol, 0) + qty

    def position(self, symbol):
        return self.pos.get(symbol, 0)
```

```python
class Ledger:
    def __init__(self):
        pass

    def trade(self, symbol, qty):
        pass

    def position(self, symbol):
        return 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `L = Ledger(); L.trade('ABC', 100); L.trade('ABC', -40); L.position(...` | `60` |
| 2 | `L = Ledger(); L.trade('ABC', 5); L.trade('XYZ', 7); L.trade('ABC', ...` | `[8, 7, 0]` |
| 3 | `L = Ledger(); L.trade('ABC', 10); L.trade('ABC', -10); L.position('...` | `0` |

Stage 2 reference (stage 2 tests include the stage 1 test as the last row), starter (fails 6 of 7):

```python
class Ledger:
    def __init__(self):
        self.pos, self.avg, self.pnl = {}, {}, {}

    def trade(self, symbol, qty, price=0):
        held = self.pos.get(symbol, 0)
        if held + qty < 0:
            raise ValueError('cannot sell more than held')
        if qty > 0:
            total = held * self.avg.get(symbol, 0.0) + qty * price
            self.avg[symbol] = total / (held + qty)
        else:
            self.pnl[symbol] = self.pnl.get(symbol, 0) + (-qty) * (price - self.avg[symbol])
        self.pos[symbol] = held + qty
        if self.pos[symbol] == 0:
            self.avg[symbol] = 0.0

    def position(self, symbol):
        return self.pos.get(symbol, 0)

    def avg_cost(self, symbol):
        return self.avg.get(symbol, 0.0)

    def realised(self, symbol):
        return self.pnl.get(symbol, 0)
```

```python
class Ledger:
    def __init__(self):
        self.pos = {}

    def trade(self, symbol, qty, price=0):
        self.pos[symbol] = self.pos.get(symbol, 0) + qty

    def position(self, symbol):
        return self.pos.get(symbol, 0)

    def avg_cost(self, symbol):
        return 0.0

    def realised(self, symbol):
        return 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `L = Ledger(); L.trade('ABC', 100, 10); L.trade('ABC', 100, 12); L.t...` | `[50, 11.0, 300.0]` |
| 2 | `L = Ledger(); L.trade('ABC', 10, 50); L.trade('ABC', -10, 55); [L.p...` | `[0, 0.0, 50.0]` |
| 3 | `L = Ledger(); L.trade('ABC', 100, 10); L.trade('ABC', 200, 13); [L....` | `[300, 12.0, 0]` |
| 4 | `L = Ledger(); L.trade('ABC', 100, 10); L.trade('ABC', -40, 12); L.t...` | `[120, 10.5, 80.0]` |
| 5 | `L = Ledger(); L.trade('ABC', 5, 10); L.trade('ABC', -5, 8); L.trade...` | `[3, 20.0, -6.0]` |
| 6 | `L = Ledger(); L.trade('ABC', 10, 5); L.trade('ABC', -11, 6)` | `'ValueError'` |
| 7 | `L = Ledger(); L.trade('ABC', 100); L.trade('ABC', -40); L.position(...` | `60` |

Stage 3 reference (every earlier row plus four FIFO rows), starter (fails 10 of 11):

```python
from collections import deque

class Ledger:
    def __init__(self, method='average'):
        self.method = method
        self.lots, self.pnl = {}, {}              # symbol -> deque of [qty, price]
        self.pos, self.avg = {}, {}

    def trade(self, symbol, qty, price=0):
        held = self.pos.get(symbol, 0)
        if held + qty < 0:
            raise ValueError('cannot sell more than held')
        lots = self.lots.setdefault(symbol, deque())
        if qty > 0:
            total = held * self.avg.get(symbol, 0.0) + qty * price
            self.avg[symbol] = total / (held + qty)
            lots.append([qty, price])
        else:
            left = -qty
            if self.method == 'fifo':
                gain = 0
                while left:
                    take = min(left, lots[0][0])
                    gain += take * (price - lots[0][1])
                    lots[0][0] -= take
                    left -= take
                    if lots[0][0] == 0:
                        lots.popleft()
            else:
                gain = left * (price - self.avg[symbol])
                while left:
                    take = min(left, lots[0][0])
                    lots[0][0] -= take
                    left -= take
                    if lots[0][0] == 0:
                        lots.popleft()
            self.pnl[symbol] = self.pnl.get(symbol, 0) + gain
        self.pos[symbol] = held + qty
        if self.pos[symbol] == 0:
            self.avg[symbol] = 0.0
        elif self.method == 'fifo':
            self.avg[symbol] = sum(q * p for q, p in lots) / sum(q for q, p in lots)

    def position(self, symbol):
        return self.pos.get(symbol, 0)

    def avg_cost(self, symbol):
        return self.avg.get(symbol, 0.0)

    def realised(self, symbol):
        return self.pnl.get(symbol, 0)
```

```python
class Ledger:
    def __init__(self, method='average'):
        self.pos = {}
        self.method = method

    def trade(self, symbol, qty, price=0):
        self.pos[symbol] = self.pos.get(symbol, 0) + qty

    def position(self, symbol):
        return self.pos.get(symbol, 0)

    def avg_cost(self, symbol):
        return 0.0

    def realised(self, symbol):
        return 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `L = Ledger(); L.trade('ABC', 100, 10); L.trade('ABC', 100, 12); L.trade('ABC', -150, 13); [L.position('ABC'...` | `[50, 11.0, 300.0]` |
| 2 | `L = Ledger(); L.trade('ABC', 10, 50); L.trade('ABC', -10, 55); [L.position('ABC'), L.avg_cost('ABC'), L.rea...` | `[0, 0.0, 50.0]` |
| 3 | `L = Ledger(); L.trade('ABC', 100, 10); L.trade('ABC', 200, 13); [L.position('ABC'), L.avg_cost('ABC'), L.re...` | `[300, 12.0, 0]` |
| 4 | `L = Ledger(); L.trade('ABC', 100, 10); L.trade('ABC', -40, 12); L.trade('ABC', 60, 11); [L.position('ABC'),...` | `[120, 10.5, 80.0]` |
| 5 | `L = Ledger(); L.trade('ABC', 5, 10); L.trade('ABC', -5, 8); L.trade('ABC', 5, 20); L.trade('ABC', -2, 22); ...` | `[3, 20.0, -6.0]` |
| 6 | `L = Ledger(); L.trade('ABC', 10, 5); L.trade('ABC', -11, 6)` | `'ValueError'` |
| 7 | `L = Ledger(); L.trade('ABC', 100); L.trade('ABC', -40); L.position('ABC')` | `60` |
| 8 | `L = Ledger(method='fifo'); L.trade('ABC', 100, 10); L.trade('ABC', 100, 12); L.trade('ABC', -150, 13); [L.p...` | `[50, 12.0, 350]` |
| 9 | `L = Ledger(method='fifo'); L.trade('ABC', 100, 10); L.trade('ABC', 200, 13); L.trade('ABC', -250, 14); [L.p...` | `[50, 13.0, 550]` |
| 10 | `L = Ledger(method='fifo'); L.trade('ABC', 10, 50); L.trade('ABC', -4, 55); L.trade('ABC', 10, 40); L.trade(...` | `[4, 40.0, 20]` |
| 11 | `L = Ledger(method='fifo'); L.trade('ABC', 5, 10); L.trade('ABC', -5, 8); L.trade('ABC', 5, 20); L.trade('AB...` | `[3, 20.0, -6]` |

Checks: the incremental references were compared with a brute force that replays the whole history (lots in a list, recomputed from scratch) on 3,000 random trade lists, for both methods, with `isclose`. The worked numbers (50 held, average £11, realised £300; FIFO £350 and £12) come from that brute force and from the hand sums above.

### l14-rate-limiter: Counting events in a time window (13 min; tags `rate-limit-log`, `token-bucket`, `rate-limit-window`)

Objective: Design a sliding-window counter and a rate limiter for timestamped events. Method stated after use: a sliding log keeps the accepted times of one client in a deque, drops those at or before `t - window`, and accepts only if fewer than `limit` remain; a token bucket holds up to `capacity` tokens, refills `rate` per second and spends one per request.

Screens (11):
1. Hook `problem`, `array` (queue mode) showing the log `[5, 6]` with limit 2 and window 10; `choice`: of three separate requests, at 14, at 15 and at 16, which are accepted? 14 no (both 5 and 6 are above 4), 15 yes (5 is not above 5, so only 6 counts), 16 yes (neither is above 6).
2. `explore`, `array` with a time control; the window slides.
3. `ladder`, `numeric`: with limit 2 and window 3 the times `0, 1, 2, 3, 4, 5` give `True, True, False, True, True, False`: four accepted.
4. `problem`, code A, Python `RateLimiter(limit, window)` with `allow(user, t)` (a dict of deques; `pace` 600). Prose says it extends the one-client version of `ds` l11.
5. `trap`, `choice`: a rejected request must not be recorded; the learner who appends before checking locks a client out for ever. Name the action in `byKey`.
6. `ladder`, `numeric`: a fixed one-minute counter with limit 100 admits 100 requests at second 59 and 100 more at second 60: 200 within two seconds; a sliding log admits 100 (computed by running both).
7. `problem`, code B, Python `TokenBucket(capacity, rate)` with `allow(t)`, `pace` 600, difficulty 4.
8. `ladder`, `numeric`: a bucket of capacity 2 with rate 2 gives, for the times `0, 0, 0, 1, 1, 1`, the answers `True, True, False, True, True, False`: four accepted (by the program and by adding tokens second by second).
9. `generalise` + `derive`.
10. `transfer`, `choice`: memory when a million clients each make one request: the log holds a million deques; the learner chooses to drop an idle client's entry when its deque empties.
11. `transfer`, `choice`: which limiter fits (a) a hard cap per minute on an exchange gateway (sliding log), (b) bursts allowed but a steady average (token bucket), (c) a cheap counter with some error (fixed window).

Quiz (4): an accept at the edge; a rejected request; a bucket after a pause; a limiter choice.

**Problem 14.1** `RateLimiter(limit, window)` with `allow(user, t)`; Python; difficulty 3. Statement: "Times are whole numbers that never go backwards. A request at `t` counts the accepted requests of the same user at times greater than `t - window`; it is accepted when that count is below `limit`. A rejected request is not recorded." Driver `run_limiter(limit, window, calls)` with `calls` rows `[user, t]` returning the list of accepted flags. Reference, driver, starter (a counter that never forgets; fails 6 of 6), tests (brute force: a list of accepted times per user, scanned; 3,000 random runs; the last case has 60,000 requests of one user and expects 1,000 accepted, by the closed form `20,000 s / 100 s * 5`):

```python
from collections import deque

class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.log = {}

    def allow(self, user, t):
        q = self.log.setdefault(user, deque())
        while q and q[0] <= t - self.window:
            q.popleft()
        if len(q) < self.limit:
            q.append(t)
            return True
        return False
```

```python
def run_limiter(limit, window, calls):
    r = RateLimiter(limit, window)
    return [r.allow(u, t) for u, t in calls]
```

```python
class RateLimiter:
    def __init__(self, limit, window):
        self.limit, self.window = limit, window
        self.count = {}

    def allow(self, user, t):
        self.count[user] = self.count.get(user, 0) + 1
        return self.count[user] <= self.limit
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_limiter(3, 10, [['a', 1], ['a', 2], ['a', 3], ['a', 4], ['a', 1...` | `[True, True, True, False, False, True, True]` |
| 2 | `run_limiter(2, 5, [['a', 0], ['b', 0], ['a', 1], ['a', 2], ['b', 2]...` | `[True, True, True, False, True, True, True]` |
| 3 | `run_limiter(1, 1, [['a', 0], ['a', 0], ['a', 1], ['a', 1], ['a', 2]])` | `[True, False, True, False, True]` |
| 4 | `run_limiter(2, 3, [['a', 0], ['a', 1], ['a', 2], ['a', 3], ['a', 4]...` | `[True, True, False, True, True, False]` |
| 5 | `run_limiter(3, 60, [['a', 0], ['a', 10], ['a', 20], ['a', 30], ['a'...` | `[True, True, True, False, False, False, True, T...` |
| 6 | `calls = [['a', t // 3] for t in range(60000)]; sum(run_limiter(5, 1...` | `1000` |

**Problem 14.2** `TokenBucket(capacity, rate)` with `allow(t)`; Python; difficulty 4. Statement: "The bucket starts full at time 0. Each whole second adds `rate` tokens, never above `capacity`. A request at `t` first adds the tokens for the time since the last request, then spends one token if it has at least one (accepted) or is rejected. `rate` and times are whole numbers." Driver `run_bucket(capacity, rate, times)`. Reference, driver, starter (allows the first `capacity` requests only; fails 5 of 6), tests (brute force: advances second by second; 3,000 random runs; the last case sends 4 requests a second for 50,000 seconds with capacity 10 and rate 1: 10 + 49,999 = 50,009 accepted, by the closed form and by the reference):

```python
class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity, self.rate = capacity, rate
        self.tokens, self.last = capacity, 0

    def allow(self, t):
        self.tokens = min(self.capacity, self.tokens + (t - self.last) * self.rate)
        self.last = t
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
```

```python
def run_bucket(capacity, rate, times):
    b = TokenBucket(capacity, rate)
    return [b.allow(t) for t in times]
```

```python
class TokenBucket:
    def __init__(self, capacity, rate):
        self.capacity, self.rate = capacity, rate
        self.used = 0

    def allow(self, t):
        self.used += 1
        return self.used <= self.capacity
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_bucket(3, 1, [0, 0, 0, 0, 1, 1, 2, 10])` | `[True, True, True, False, True, False, True, True]` |
| 2 | `run_bucket(2, 2, [0, 0, 0, 1, 1, 1])` | `[True, True, False, True, True, False]` |
| 3 | `run_bucket(1, 0, [0, 5, 10])` | `[True, False, False]` |
| 4 | `run_bucket(5, 1, [0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3])` | `[True, True, True, True, True, False, True, Tru...` |
| 5 | `run_bucket(2, 1, [0, 0, 0, 2, 2, 2, 2])` | `[True, True, False, True, True, False, False]` |
| 6 | `ts = [t // 4 for t in range(200000)]; sum(run_bucket(10, 1, ts))` | `50009` |

### Level 3 review (`review-3.json`, 10 items, difficulty 2 to 4, interleaving all four lessons, every case unseen in the lessons, each with `tags` and `skills`)

| # | Lesson | Widget | d | Prompt (summary) | Key |
| --- | --- | --- | --- | --- | --- |
| 1 | l11 | `numeric` | 3 | Capacity 2; put 1, put 2, get 1, put 3, get 2, put 4, get 1, get 3, get 4 (values equal to keys). Sum of the gets. | 6 (`1, -1, -1, 3, 4`) |
| 2 | l11 | `choice` | 3 | Capacity 3; put 1, 2, 3; get 1; put 4; get 3. Which key was evicted? | 2 (recency, most recent first: 3, 4, 1) |
| 3 | l11 | `numeric` | 3 | TTL cache, capacity 2, ttl 5: put key 1 at time 0; get at times 4, 8, 13, 14. How many return -1? | 2 (ages 4, 4, 5, then gone) |
| 4 | l12 | `numeric` | 3 | Files `/docs/n/a.txt` (12345), `/docs/n/b.txt` (678), `/docs/c.txt` (9): `size('/docs')`. | 9 (`size('/docs/n')` is 8) |
| 5 | l12 | `choice` | 3 | After `mkdir('/b')`, `mkdir('/a')`, `write('/c.txt', '1')`, `mkdir('/a/z')`: what does `ls('/')` return? | `['a', 'b', 'c.txt']` |
| 6 | l13 | `numeric` | 3 | Buy 200 at £20, buy 100 at £23, sell 250 at £25: realised £ under FIFO. | 1,100 (`200 * 5 + 50 * 2`; average cost, £21 on 300 shares, gives `250 * 4 = 1,000`) |
| 7 | l13 | `choice` | 3 | Why does `trade(symbol, qty, price=0)` keep the stage 1 tests passing? | Old calls pass two arguments and the default fills the third. Distractors: Python ignores extra arguments; the tests are not run again; `price` is optional in every language. |
| 8 | l14 | `numeric` | 3 | Limit 3, window 10, requests at 1, 2, 3, 4, 10, 11, 12: how many are accepted? | 5 (`T T T F F T T`) |
| 9 | l14 | `numeric` | 3 | Bucket capacity 3, rate 1, requests at 0, 0, 0, 0, 1, 1, 2, 10: how many are accepted? | 6 |
| 10 | l14 | `choice` | 3 | A hit counter that only needs the last 300 seconds: what does a ring of 300 buckets cost as traffic grows? | Constant memory, 300 slots. Distractors: memory proportional to the hits, to the clients, to the seconds so far. |

### Level 3 homework (`homework-3.json`, 8 items, difficulty 3 to 5 with at least one 5, `tags` on each; two `code` items, one `longform`, one E11 `parts` item)

| # | Lesson | Kind | d | Item | Key or reference |
| --- | --- | --- | --- | --- | --- |
| 1 | l11 | `code` | 5 | `LFUCache(capacity)` (below). | tests below |
| 2 | l14 | `code` | 3 | `HitCounter` (below). | tests below |
| 3 | l14 | `longform` | 4 | Say aloud, timing yourself to three minutes: design a per-client rate limit for an exchange gateway. Compare fixed window, sliding log and token bucket on accuracy, memory and bursts, with the 200 against 100 example. | Model: a fixed window lets 200 requests through in two seconds around a boundary; a sliding log lets 100 and costs memory per request; a token bucket bounds the average and allows a burst of the capacity. Rubric (10): 2 states the three designs, 2 the boundary burst with numbers, 2 memory per design, 2 burst behaviour of the bucket, 2 a justified choice. |
| 4 | l14 | `numeric` | 4 | Limit 100 per minute. 100 requests arrive at second 59 and 100 at second 60. How many does a fixed one-minute counter admit? | 200 (a sliding log admits 100; both run in a script) |
| 5 | l13 | `parts` (E11), `numeric` ×3 | 4 | Trades `(10, £50)`, `(-4, £55)`, `(10, £40)`, `(-12, £45)`. Part 1: realised £ by average cost. Part 2: realised £ by FIFO. Part 3: average minus FIFO. | 35, 20, 15 (working below) |
| 6 | l11 | `order` | 4 | The steps of `get`: look up the node (return -1 if absent); unlink it; push it to the front; return its value. | Distractor: "delete the node and create a new one" with its `why` (the dict entry then points at a dead node). |
| 7 | l11 | `multi` | 3 | Which are `O(1)` with a dict of nodes and a doubly linked list: `get`, `put` of a new key at capacity, delete by key, list all keys in recency order, find the median key. | `get`, `put`, delete by key. The last two are `O(n)` and `O(n log n)`. |
| 8 | l11 | `numeric` | 5 | LFU with capacity 2 on `put 1, put 2, get 1, put 3, get 2, get 3, put 4, get 1, get 3, get 4` (values equal keys; ties go to the least recently used): sum of the gets. | 9 (`1, -1, 3, -1, 3, 4`; traced by hand and by the brute force) |

The working for item 5 above, stated plainly for the level agent: average cost after the first buy is £50; the sale of 4 at £55 realises `4 * (55 - 50) = £20`; 6 shares at £50 remain; the buy of 10 at £40 brings 16 shares at an average of `(6 * 50 + 10 * 40) / 16 = £43.75`; the sale of 12 at £45 realises `12 * (45 - 43.75) = £15`; total £35. FIFO: the first sale uses the £50 lot, realising £20; the second uses the 6 remaining £50 lots (`6 * (45 - 50) = -£30`) and 6 of the £40 lot (`6 * (45 - 40) = £30`); total £20. The difference is £15. (Both methods were computed in `numbers_check.py`.)

**Problem H3.1** `LFUCache(capacity)` with `get(key)` and `put(key, value)`; Python; difficulty 5. Statement: "As `LRUCache`, but when full drop the entry used the fewest times; ties go to the least recently used of those. A `get` or `put` of an existing key counts as a use; a new key starts at one use. Capacity 0 stores nothing. Both are `O(1)`." Driver `run_lfu(cap, ops)` as `run_lru`. Reference (frequency buckets of ordered dicts and a minimum frequency), starter (a plain dict; fails 6 of 7), tests (brute force: evicts by `min` over `(frequency, last use)`; 4,000 random runs agreed):

```python
from collections import defaultdict, OrderedDict

class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.vals, self.freq = {}, {}
        self.buckets = defaultdict(OrderedDict)    # freq -> keys, oldest first
        self.min_freq = 0

    def _touch(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq += 1
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.vals:
            return -1
        self._touch(key)
        return self.vals[key]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.vals:
            self.vals[key] = value
            self._touch(key)
            return
        if len(self.vals) == self.capacity:
            victim, _ = self.buckets[self.min_freq].popitem(last=False)
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.vals[victim], self.freq[victim]
        self.vals[key], self.freq[key] = value, 1
        self.buckets[1][key] = None
        self.min_freq = 1
```

```python
def run_lfu(cap, ops):
    c = LFUCache(cap)
    out = []
    for op in ops:
        if op[0] == 0:
            c.put(op[1], op[2])
        else:
            out.append(c.get(op[1]))
    return out
```

```python
class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}

    def get(self, key):
        return self.data.get(key, -1)

    def put(self, key, value):
        self.data[key] = value
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_lfu(2, [[0, 1, 1], [0, 2, 2], [1, 1], [0, 3, 3], [1, 2], [1, 3]...` | `[1, -1, 3, -1, 3, 4]` |
| 2 | `run_lfu(0, [[0, 0, 0], [1, 0]])` | `[-1]` |
| 3 | `run_lfu(2, [[0, 1, 1], [0, 2, 2], [0, 3, 3], [1, 1], [1, 2], [1, 3]])` | `[-1, 2, 3]` |
| 4 | `run_lfu(2, [[0, 1, 1], [0, 2, 2], [1, 1], [1, 1], [0, 3, 3], [1, 2]...` | `[1, 1, -1, 3, 1]` |
| 5 | `run_lfu(3, [[0, 1, 1], [0, 2, 2], [0, 3, 3], [1, 1], [1, 2], [0, 4,...` | `[1, 2, -1, 1, 2, 4]` |
| 6 | `run_lfu(1, [[0, 1, 1], [0, 1, 9], [1, 1], [0, 2, 2], [1, 1], [1, 2]])` | `[9, -1, 2]` |
| 7 | `ops = [[0, i, i] for i in range(50000)] + [[1, i] for i in range(49...` | `49499500` |

**Problem H3.2** `HitCounter` with `hit(t)` and `count(t)`; Python; difficulty 3. Statement: "`hit(t)` records a hit at whole second `t`; `count(t)` returns the hits at times greater than `t - 300` and at most `t`. Calls come in non-decreasing time. Use a fixed amount of memory." Driver `run_hits(ops)` with rows `[0, t]` for `hit` and `[1, t]` for `count`. Reference (a ring of 300 buckets), driver, starter (counts every hit ever; fails 4 of 5), tests (brute force: a list of times; 2,000 random runs; the last case sends 50,000 hits at even seconds to 99,998 and counts at 99,999: 150):

```python
class HitCounter:
    def __init__(self):
        self.times = [0] * 300
        self.counts = [0] * 300

    def hit(self, t):
        i = t % 300
        if self.times[i] != t:
            self.times[i], self.counts[i] = t, 0
        self.counts[i] += 1

    def count(self, t):
        return sum(c for s, c in zip(self.times, self.counts) if t - 300 < s <= t)
```

```python
def run_hits(ops):
    h = HitCounter()
    out = []
    for op in ops:
        if op[0] == 0:
            h.hit(op[1])
        else:
            out.append(h.count(op[1]))
    return out
```

```python
class HitCounter:
    def __init__(self):
        self.hits = []

    def hit(self, t):
        self.hits.append(t)

    def count(self, t):
        return len(self.hits)
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_hits([[0, 1], [0, 2], [0, 3], [1, 4], [0, 300], [1, 300], [1, 3...` | `[3, 4, 3, 2, 1]` |
| 2 | `run_hits([[1, 1]])` | `[0]` |
| 3 | `run_hits([[0, 1], [0, 1], [1, 1], [1, 300], [1, 301]])` | `[2, 2, 0]` |
| 4 | `run_hits([[0, 5], [0, 305], [1, 305], [1, 604], [1, 605]])` | `[1, 1, 0]` |
| 5 | `ops = [[0, t] for t in range(0, 100000, 2)] + [[1, 99999]]; run_hit...` | `[150]` |

### Level 3 report notes

Report as `docs/LEVEL-BRIEF.md` says. Do not edit files outside `app/content/courses/coding-int/`.

## Level 4

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `coding-int` (topic 3.5), level 4 ("Under the clock"): lessons `l15-reading-an-assessment`, `l16-edge-cases-first`, `l17-two-in-sixty`, `l18-talking-while-coding`, `l19-a-live-round`, plus `review-4.json` and `homework-4.json`, in `app/content/courses/coding-int/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids of `course.json` exactly (`ci-timed` on l15 to l19; l19 also `ci-design`). Use £ for money. Scripts: `l4.py` (every problem of this level; C++ checks; timings), `l_extra.py` (the C++ `longest_consecutive`), `harness.py`, `numbers_check.py`, `numbers_check3.py`, `numbers_check4.py`.

Level promise. The learner has the patterns and the designs; now the clock. This level teaches how an online assessment is read and planned, how to find the edge cases before writing a line, how to use 60 minutes on two problems, how to talk while coding, and how a 45-minute live round with follow-ups runs. Formats are reported, not official: say "reported" and keep firm names out ("a bank's online assessment", "a market maker's developer screen", "a developer role at a trading firm").

**Engine features (pass C).**
- **E8 (drill library)**: l17 screen 8 sends the learner to `#drill` to start a two-drill, 60-minute session with filters pattern `prefix-sums` or `hashing`, difficulty 3 to 4, language Python or C++ (the C++ drills are `language: "cpp"`); l19 screen 9 sends the learner to a single-drill stopwatch on an `intervals` drill, difficulty 4, language Python or C++. The drill files belong to the drill packs (authored separately); this level names the filters only. Use the pattern names the E8 filter lists show; if the built filter uses other slugs, use those and tell the report.
- **E3 (item banks in exams)**: l15 screen 10 and l17 screen 10 link to `#exam/mock-oa-code`, a mock whose paper draws from the bank by `draw` so a resat is fresh. The mock is authored in a separate task; this level only links to it, and tags its own review and homework items (`oa-triage`, `edge-case-list`, `complexity-read`, `timed-plan`) so the bank families can use them.
- **E11 (follow-up parts)**: homework items 1 and 2, each a live round with follow-ups revealed in turn and graded per part. A part may be a `code` widget (the part's hidden tests are the whole item's cumulative tests up to that part), a `choice` or a `numeric`.
- **`timed` on a level review (existing, built)**: `review-4.json` carries `"timed": { "seconds": 600, "lockAtZero": false }` so the clock is a guide, shown with a live score, for ten items. Not allowed on homework.
- Existing: `code` Python and C++ (with `testkit` and per-case `defines` for l16, a `postlude` driver for l19), `table`, `order`, `choice`, `multi`, `numeric`, `longform`, canvases `console`, `table`, `array`, `number-line` (intervals for the calendar).
- E14 is not needed in level 4.

**Builds on (by id) and what is new.**

| Lesson | Builds on | New over those |
| --- | --- | --- |
| l15-reading-an-assessment | `contests` l14-which-first (order by points and difficulty), `contests` l2-limits-to-complexity (constraints to complexity), `contests` l13-virtual-contest, `recruiting` l9 (online assessments) | Partial credit as a choice per problem (full, partial or skip, solved by dynamic programming), the greedy trap with numbers, test groups by input size. The constraints table is cited, not re-taught. |
| l16-edge-cases-first | `contests` l4-stress-testing, `contests` l15-debugging-under-time, `pytest` l5-empty-one-many, `pytest` l10-test-first, `cpp` l18-unit-tests | Writing inputs that catch planted bugs (a mutation check), edge-case families for arrays, strings, intervals and numbers, and the same game in C++ with `testkit` and `defines`. |
| l17-two-in-sixty | `contests` l13-virtual-contest, `contests` l16-upsolving, `ds` l7-prefix-sums, `ds` l2-constant-time-lookup | Splitting 60 minutes across two problems, a brute force that earns partial credit, the E8 session, two classic hash patterns (prefix-sum counts, a set of starts). |
| l18-talking-while-coding | `recruiting` l12-reasoning-aloud, `mm-games` l12-thinking-aloud | Narrating a plan and its trade-offs in comments before code, naming complexity out loud, handling a constraint ("no division") while talking. |
| l19-a-live-round | `ci-patterns` l1-merging-intervals (this course), `ds` l15-search-trees, `cpp` l15-maps | A 45-minute live problem in three stages: base, a changed rule, a new operation, with the sorted-list design and its sweep replacement. |

### l15-reading-an-assessment: Reading an online assessment (13 min; tags `oa-triage`, `partial-credit`, `timed-plan`)

Objective: Triage an assessment's problems and plan the minutes before writing code. Method stated after use: in the first five minutes read every statement, note the constraints and the point values, estimate full and partial minutes, then pick for each problem full, partial or skip so that the points are most for the minutes you have. Reported formats to quote with the word "reported": an online assessment of two algorithm problems in 60 minutes at a bank, three problems in 90 minutes at a developer role; points often depend on how many hidden test groups pass.

The running assessment (prices of time in minutes): three problems, each with full points and the minutes you estimate for full marks, and partial points (the small test groups) and the minutes for that: P1 `(40, 20, 12, 6)`, P2 `(60, 35, 25, 12)`, P3 `(90, 50, 30, 18)`. The assessment lasts 65 minutes and reading takes 3, so the budget is 62.

Screens (10):
1. Hook `problem`, `console` showing the three problems; `choice`: which has the most points per minute? P1 (40/20 = 2.0; P2 is 1.71; P3 is 1.80).
2. `ladder`, `numeric`: take problems by points per minute, full marks only, within 62 minutes: P1 (20) then P3 (50) is 70, too much, so P2 (35) fits: 55 minutes, 100 points.
3. `ladder`, `table` widget: the learner fills the best plan: P2 partial (12 minutes, 25 points) and P3 full (50 minutes, 90 points) is 62 minutes and 115 points.
4. `problem`, code A, `best_plan`, `pace` 900, difficulty 4 (`best_plan` over `(full_pts, full_min, part_pts, part_min)` lists).
5. `trap`, `choice`: "every problem full or nothing". The learner who allows no partials gets 100; the right answer 115. Name the action in `byKey` ("You ruled out partial credit").
6. `ladder`, `choice`: test groups. A statement lists groups `n <= 1,000`, `n <= 100,000` and `n <= 1,000,000`; which of an `O(n^2)`, an `O(n log n)` and an `O(n)` solution earns which groups (the learner marks a three-by-three table; cite `contests` l2 for the arithmetic).
7. `ladder`, `order`: the first five minutes (read all, mark constraints, rank by points per minute, settle partials, set time boxes, start the surest problem).
8. `generalise` + `derive` (`order` the plan steps).
9. `transfer`, `numeric`: with budget 60 instead of 62, the best plan is 102 (P1 partial, P2 full, P3 partial: 6, 35 and 18 minutes) and the greedy by points per minute still makes 100; computed by the program and by listing the 27 choices.
10. `transfer`, `choice`: the learner picks the plan for a different assessment of two problems in 60 minutes; closing prose links `#exam/mock-oa-code` (E3, a fresh paper each attempt).

Quiz (4): points per minute; a budget after reading; a test group; a partial choice.

**Problem 15.1** `best_plan(problems, budget)`; Python; difficulty 4. Statement: "Each problem is `[full_points, full_minutes, partial_points, partial_minutes]`. For each you choose full, partial or skip. Return the most points obtainable in at most `budget` minutes." Reference (dynamic programming over minutes), starter (returns 0; fails 8 of 10), tests (brute force over all `3^n` choices; the last has 60 problems and budget 600, expected from a memoised recursion):

```python
def best_plan(problems, budget):
    best = [0] * (budget + 1)               # best[m]: most points using at most m minutes
    for full_pts, full_min, part_pts, part_min in problems:
        new = best[:]
        for m in range(budget + 1):
            if m >= full_min:
                new[m] = max(new[m], best[m - full_min] + full_pts)
            if m >= part_min:
                new[m] = max(new[m], best[m - part_min] + part_pts)
        best = new
    return best[budget]
```

```python
def best_plan(problems, budget):
    return 0
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `best_plan([[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15]], 55)` | `100` |
| 2 | `best_plan([[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15]], 60)` | `110` |
| 3 | `best_plan([[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15]], 90)` | `160` |
| 4 | `best_plan([[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15]], 0)` | `0` |
| 5 | `best_plan([[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15]], 14)` | `20` |
| 6 | `best_plan([], 30)` | `0` |
| 7 | `best_plan([[40, 20, 10, 20]], 20)` | `40` |
| 8 | `best_plan([[40, 20, 30, 5]], 10)` | `30` |
| 9 | `best_plan([[30, 15, 10, 5], [50, 30, 20, 10], [80, 45, 25, 15], [20...` | `80` |
| 10 | `import random; random.seed(1); ps = []
for _ in range(60):
    fm =...` | `2724` |

The lesson example (`P1` to `P3` at 62) is not in the table; its numbers come from `numbers_check4.py`: best 115 (by the program and by listing 27 choices), greedy 100, and at 60 minutes best 102 and greedy 100.

### l16-edge-cases-first: Edge cases first (13 min; tags `edge-case-list`, `test-first`, `mutation-tests`)

Objective: List edge cases and write tests before the solution. Method stated after use: before the code, write the empty, the single, the repeated and the boundary inputs and their expected outputs; run them against a wrong solution to see them fail; only then write the real one. The learner's own lists are marked by planted bugs, not by matching a model list.

The function under test: `longest_run(xs)`, the length of the longest run of equal neighbours in a list of whole numbers (0 for an empty list). Six planted bugs: `m1` forgets the last run, `m2` returns 1 for an empty list, `m3` returns 0 for a single element, `m4` counts non-decreasing runs, `m5` restarts a run at 0 after a break, `m6` compares only with the first value.

Screens (11):
1. Hook `problem`, `multi`: which of `[]`, `[1, 2]`, `[2, 2, 2]`, `[3, 1, 1]`, `[2, 1]` expose bug `m1`? `[2, 2, 2]` and `[3, 1, 1]` (the last run is the longest).
2. `ladder`, `table` widget: the expected outputs of `[]`, `[7]`, `[1, 2]`, `[3, 1, 1]`, `[2, 2, 2]`, `[1, 1, 2, 2, 2]`: 0, 1, 1, 2, 3, 3.
3. `problem`, code A, Python `edge_cases()` returning at most 8 inputs (the hidden harness runs the reference and each planted bug on them), `pace` 480, difficulty 3.
4. `ladder`, `numeric`: how many of the six bugs does `[3, 1, 1]` expose? 3 (`m1`, `m5`, `m6`).
5. `trap`, `choice`: "A thousand random lists" miss `m2`, the empty list, because random lists are rarely empty; the learner who relies on random tests only is wrong. Name the action in `byKey`.
6. `problem`, code B, C++ twin with `testkit`: the learner writes `TEST` blocks with `CHECK`; the hidden postlude defines `longest_run` and, for each case with `defines`, a planted bug; the correct version must pass every test (the learner's expected values must be right), and each bug must make `run_tests()` report a failure.
7. `ladder`, `table` widget: the edge-case families (arrays: empty, one, two equal, all equal, sorted, reverse, negatives; strings: empty, one letter, repeated; intervals: touching, nested, identical; numbers: 0, negative, largest).
8. `generalise` (a checklist in code comments) + `derive` (`order` the test-first steps).
9. `transfer`, `multi`: the three tests worth writing first for `merge_intervals` (`[]`, a touching pair, a nested pair).
10. `transfer`, `numeric`: the smallest number of inputs among ten candidates that exposes all six bugs: 3 (`[]`, `[7]`, `[1, 1, 2, 2, 2]`), found by trying every subset of the ten.
11. `transfer`, `choice`: what to say aloud before writing the tests ("I will start with empty, single, repeated and boundary").

Quiz (4): which input exposes a bug; the expected value of an edge input; why random tests miss; a checklist item.

**Problem 16.1** `edge_cases()`; Python; difficulty 3. Statement: "Return a list of at most 8 inputs (each a list of whole numbers) for `longest_run`. They are run against the correct function and six wrong versions; every wrong version must give a different answer on at least one of your inputs." `prelude` holds the reference and the six planted bugs and the checker `caught(name)` and `well_formed()`; the tests call them:

```python
def _ref(xs):
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best
def _m1(xs):                      # forgets the last run
    best = run = 0
    for i, x in enumerate(xs):
        if i and x == xs[i - 1]:
            run += 1
        else:
            best = max(best, run)
            run = 1
    return best
def _m2(xs):                      # empty list gives 1
    best = run = 1
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else 1
        best = max(best, run)
    return best
def _m3(xs):                      # a single element gives 0
    if len(xs) == 1:
        return 0
    return _ref(xs)
def _m4(xs):                      # counts non-decreasing runs
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x >= xs[i - 1] else 1
        best = max(best, run)
    return best
def _m5(xs):                      # restarts the run at 0 after a break
    best = run = 0
    for i, x in enumerate(xs):
        run = run + 1 if i and x == xs[i - 1] else (1 if i == 0 else 0)
        best = max(best, run)
    return best
def _m6(xs):                      # only compares with the first value
    best = run = 0
    for x in xs:
        run = run + 1 if x == xs[0] else 0
        best = max(best, run)
    return best
_MUTANTS = {'m1': _m1, 'm2': _m2, 'm3': _m3, 'm4': _m4, 'm5': _m5, 'm6': _m6}
def caught(name):
    try:
        cases = edge_cases()
    except Exception:
        return False
    return any(_MUTANTS[name](list(c)) != _ref(list(c)) for c in cases)
def well_formed():
    cases = edge_cases()
    return len(cases) <= 8 and all(isinstance(c, list) and all(isinstance(v, int) for v in c) for c in cases)
```

Reference (`edge_cases` returning `[[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2]]`):

```python
def edge_cases():
    return [[], [7], [1, 2], [3, 1, 1], [2, 2, 2], [1, 1, 2, 2, 2]]
```

Starter (returns an empty list; fails 6 of 7):

```python
def edge_cases():
    return []
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `caught('m1')` | `True` |
| 2 | `caught('m2')` | `True` |
| 3 | `caught('m3')` | `True` |
| 4 | `caught('m4')` | `True` |
| 5 | `caught('m5')` | `True` |
| 6 | `caught('m6')` | `True` |
| 7 | `well_formed()` | `True` |

Coverage table (which planted bug each candidate input exposes, computed by running every bug): `[]` m2; `[7]` m1, m3; `[1, 2]` m4; `[3, 1, 1]` m1, m5, m6; `[2, 2, 2]` m1; `[1, 1, 2, 2, 2]` m1, m4, m5, m6; `[1, 1]` m1; `[2, 1]` none; `[1, 2, 2]` m1, m4, m5, m6; `[5, 5, 5, 1]` none. The reference `longest_run` was checked against a brute force over all runs on 2,000 random lists.

**Problem 16.2** the C++ twin of `edge_cases`; difficulty 3. The learner writes tests, not a function. Hidden `prelude` (declaration; the `testkit` provides `TEST`, `CHECK` and `run_tests()`):

```cpp
#include <vector>
#include <algorithm>
int longest_run(const std::vector<int>& xs);
```

Hidden `postlude` (the function and five planted bugs behind `defines`; the correct version is the `#else`):

```cpp
int longest_run(const std::vector<int>& xs) {
    int best = 0, run = 0;
#ifdef BUG1
    for (size_t i = 0; i < xs.size(); ++i) {
        if (i && xs[i] == xs[i - 1]) ++run;
        else { best = std::max(best, run); run = 1; }
    }
    return best;
#elif defined(BUG2)
    best = 1;
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG3)
    if (xs.size() == 1) return 0;
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG4)
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] >= xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#elif defined(BUG5)
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : (i == 0 ? 1 : 0);
        best = std::max(best, run);
    }
    return best;
#else
    for (size_t i = 0; i < xs.size(); ++i) {
        run = (i && xs[i] == xs[i - 1]) ? run + 1 : 1;
        best = std::max(best, run);
    }
    return best;
#endif
}
```

Starter (one test; it passes the correct version and exposes only `BUG2`):

```cpp
#include <vector>
#include <algorithm>
TEST(empty) { CHECK(longest_run({}) == 0); }
```

Model solution (passes the correct version; every bug makes at least one test fail):

```cpp
#include <vector>
#include <algorithm>
TEST(empty) { CHECK(longest_run({}) == 0); }
TEST(single) { CHECK(longest_run({7}) == 1); }
TEST(rising) { CHECK(longest_run({1, 2}) == 1); }
TEST(run_after_break) { CHECK(longest_run({3, 1, 1}) == 2); }
TEST(whole_list) { CHECK(longest_run({2, 2, 2}) == 3); }
TEST(two_runs) { CHECK(longest_run({1, 1, 2, 2, 2}) == 3); }
```

Hidden cases (`"testkit": true` on the widget): `{ "call": "run_tests()", "expect": 0 }` with no defines, and for each `n` from 1 to 5 `{ "call": "run_tests() > 0", "expect": true, "defines": { "BUGn": 1 } }`. The starter fails four of the six cases (every bug except `BUG2`). The model solution was compiled with `g++` under `-std=c++20 -O1 -fno-exceptions` against a stand-in `testkit` (`TEST`, `CHECK`, `run_tests`) and passed the correct version and failed each of `BUG1` to `BUG5`. The level agent confirms the real `testkit` behaves the same in the playthrough.

### l17-two-in-sixty: Two problems in sixty minutes (14 min; tags `timed-plan`, `prefix-sum-count`, `hash-set-starts`)

Objective: Solve two medium problems inside 60 minutes, with a plan for partial credit. Method stated after use: 5 minutes to read both, 25 minutes for each problem (brute force first when it earns points, then the fast version), 5 minutes to run tests and edge cases, and a rule that you move on at the box. The pace of a medium is 25 minutes (1,500 seconds) on each code screen of this lesson.

Screens (10):
1. Hook `problem`, `table`: the plan 5 read, 25, 25, 5 test; `numeric`: if the first problem takes 28 minutes, how many minutes are left for the second after reading and testing? 22.
2. `problem`, code A, Python `count_subarrays_sum_k`, `pace` 1500; the starter is a correct quadratic brute force.
3. `ladder`, `numeric`: how many of the 11 tests does the brute force pass? 9 (it stops at the first large case). The prose says partial credit is a score for the small groups.
4. `ladder`, code A in C++ (the same 11 tests; the quadratic starter is correct and fails by time on the first large case: about 11 seconds natively at `n = 200,000`, so the wasm run is slower than the 5 s limit).
5. `trap`, `choice`: polishing the first problem for 40 minutes leaves 15 for the second and 0 for tests; the right call is to submit the partial and move on at the box.
6. `problem`, code B, Python `longest_consecutive` (a set; only start counting at a value whose predecessor is absent), `pace` 1200.
7. `ladder`, `choice`: `set` against sorting: both beat the list scan; sorting is `O(n log n)`, the set is `O(n)` on average.
8. `transfer`, E8: the prose sends the learner to `#drill`: "Start a session: two drills, 60 minutes, filters `prefix-sums` and `hashing`, difficulty 3 to 4." The screen's `choice` asks which split they will set before starting (5, 25, 25, 5 is correct; 0, 30, 30, 0 and 10, 20, 20, 10 are wrong with a `why`). A second, shorter prose line says a C++ learner picks `language: cpp`.
9. `generalise` + `derive` (`order` the minute plan).
10. `transfer`, `choice`: which of two problems to start with given a 60-minute clock and a partial-credit rule; closing prose links `#exam/mock-oa-code` (E3).

Quiz (4): minutes left; partial credit; the box rule; set against sort.

**Problem 17.1** `count_subarrays_sum_k(nums, k)`; Python and C++ twin; difficulty 3. Statement: "Return the number of non-empty contiguous subarrays of `nums` whose sum equals `k`. Values may be negative or zero." Python reference (a dict of prefix-sum counts), starter (correct but quadratic: it passes the nine small cases and is stopped by the clock on the tenth), tests (the tenth is 200,000 zeros, answer `200000 * 200001 / 2 = 20,000,100,000`, the eleventh is `[1, -1]` repeated 50,000 times with `k = 0`, answer 2,500,000,000, by the closed form `sum of (100,000 - L + 1)` over even `L`):

```python
def count_subarrays_sum_k(nums, k):
    seen = {0: 1}
    total = count = 0
    for x in nums:
        total += x
        count += seen.get(total - k, 0)
        seen[total] = seen.get(total, 0) + 1
    return count
```

```python
def count_subarrays_sum_k(nums, k):
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `count_subarrays_sum_k([1, 1, 1], 2)` | `2` |
| 2 | `count_subarrays_sum_k([1, 2, 3], 3)` | `2` |
| 3 | `count_subarrays_sum_k([], 0)` | `0` |
| 4 | `count_subarrays_sum_k([0, 0, 0], 0)` | `6` |
| 5 | `count_subarrays_sum_k([1, -1, 0], 0)` | `3` |
| 6 | `count_subarrays_sum_k([3, 4, 7, 2, -3, 1, 4, 2], 7)` | `4` |
| 7 | `count_subarrays_sum_k([5], 5)` | `1` |
| 8 | `count_subarrays_sum_k([5], -5)` | `0` |
| 9 | `count_subarrays_sum_k([-1, -1, 1], 0)` | `1` |
| 10 | `xs = [0] * 200000; count_subarrays_sum_k(xs, 0)` | `20000100000` |
| 11 | `ys = [1, -1] * 50000; count_subarrays_sum_k(ys, 0)` | `2500000000` |

Both languages use 200,000 zeros in the tenth row (`xs = [0] * 200000`, expected 20,000,100,000), so that the C++ starter fails by time. Python: the quadratic starter takes about 0.15 s at 3,000 values, so about 170 s at 100,000 and longer at 200,000, far past 5 s. C++: the quadratic starter ran for 10.96 s natively at 200,000 (`-O1`); WebAssembly is slower. Both are verified by timing, since the starter is correct and fails only by the clock. The hash-map reference passes all 11 cases in Python and in C++.

C++ reference, with `long long` for the result and the sums (starter: the quadratic loop; signature `long long count_subarrays_sum_k(std::vector<int> nums, long long k)`; the cases use `args` and `types: ["std::vector<int>", "long long"]`, the large case builds `std::vector<int>(200000, 0)` in `call`):

```cpp
#include <vector>
#include <unordered_map>
long long count_subarrays_sum_k(std::vector<int> nums, long long k) {
    std::unordered_map<long long, long long> seen;
    seen[0] = 1;
    long long total = 0, count = 0;
    for (int x : nums) {
        total += x;
        auto it = seen.find(total - k);
        if (it != seen.end()) count += it->second;
        ++seen[total];
    }
    return count;
}
```

```cpp
#include <vector>
#include <unordered_map>
long long count_subarrays_sum_k(std::vector<int> nums, long long k) {
    long long count = 0;
    for (size_t i = 0; i < nums.size(); ++i) {
        long long total = 0;
        for (size_t j = i; j < nums.size(); ++j) {
            total += nums[j];
            if (total == k) ++count;
        }
    }
    return count;
}
```

**Problem 17.2** `longest_consecutive(nums)`; Python; difficulty 3. Statement: "Return the length of the longest run of consecutive whole numbers present in `nums` (in any order, with repeats); 0 for an empty list." Reference (a set, start only at run starts), starter (scans the list with `in nums`, correct but quadratic: passes the eight small cases, stopped at the first large one), tests:

```python
def longest_consecutive(nums):
    present = set(nums)
    best = 0
    for x in present:
        if x - 1 not in present:
            length = 1
            while x + length in present:
                length += 1
            best = max(best, length)
    return best
```

```python
def longest_consecutive(nums):
    best = 0
    for x in nums:
        length = 1
        while x + length in nums:
            length += 1
        best = max(best, length)
    return best
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `longest_consecutive([100, 4, 200, 1, 3, 2])` | `4` |
| 2 | `longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])` | `9` |
| 3 | `longest_consecutive([])` | `0` |
| 4 | `longest_consecutive([5])` | `1` |
| 5 | `longest_consecutive([1, 2, 0, 1])` | `3` |
| 6 | `longest_consecutive([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6])` | `7` |
| 7 | `longest_consecutive([1, 1, 1])` | `1` |
| 8 | `longest_consecutive([-2, -1, 0, 1])` | `4` |
| 9 | `import random; random.seed(2); xs = list(range(200000)); random.shu...` | `200000` |
| 10 | `ys = list(range(0, 400000, 2)); longest_consecutive(ys)` | `1` |

### l18-talking-while-coding: Talking while you code (13 min; tags `narration`, `tradeoffs`, `product-except-self`)

Objective: Explain the plan and its trade-offs aloud while writing the code. Method stated after use: say the problem back in one sentence, give an example, name the brute force and its cost, name the better idea, write the plan as comments, then code it while saying each non-obvious line. No audio is recorded and none is graded: the lesson is practised by speaking aloud and ticking a rubric (`longform`) in the homework; in the lesson the code screen checks that the plan exists as comments.

Screens (10):
1. Hook `problem`, `console` with a transcript of a candidate who codes in silence for ten minutes and a second who narrates; `choice`: which minute counts they lose or gain (the interviewer's notes; keyed to naming the brute force first).
2. `ladder`, `choice`: the one-sentence restatement of `product_except_self` (each output is the product of all the others).
3. `ladder`, `numeric`: the brute force on `[2, 3, 4, 5]` gives `[60, 40, 30, 24]`; the cost of the brute force on `n = 100,000` is `n (n - 1) = 9,999,900,000` multiplications.
4. `ladder`, `choice`: the division idea (total product divided by each) and why it fails with a zero; `[3, 0, 2]` gives `[0, 6, 0]`.
5. `problem`, code A, `product_except_self`, `pace` 720: the hidden tests also check no division in the code and at least three comment lines of plan.
6. `trap`, `choice`: coding first and explaining after; the learner who silently writes the final loop cannot say why two passes work. Name the action in `byKey`.
7. `ladder`, `table` widget: three lines of narration matched to the three lines of code they explain (the plan comment, the left pass, the right pass).
8. `generalise` + `derive` (`order` the narration steps).
9. `transfer`, `choice`: an interviewer interrupts with "what if the list is a stream?"; the learner picks the answer that states what changes (output space, order of passes).
10. `transfer`, `choice`: how to state complexity aloud: "linear time, constant extra space apart from the output."

Quiz (4): the brute force cost; why division fails; the passes; the complexity sentence.

**Problem 18.1** `product_except_self(nums)`; Python; difficulty 3. Statement: "Return a list whose `i`-th entry is the product of every entry of `nums` except the `i`-th, without division, in `O(n)` time. Write your plan as comments first." Reference, starter (a stub with one comment, returns zeros; fails 8 of 10), tests (the last two check the source: no `/` in any code part of a line, and at least three comment lines):

```python
def product_except_self(nums):
    # plan: out[i] = (product of everything left of i) * (product of everything right of i)
    # pass 1 fills out[i] with the left product, pass 2 multiplies in the right product
    # no division, so zeros are safe; two passes, O(n) time and O(1) extra space
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out
```

```python
def product_except_self(nums):
    # plan: write two or three comment lines here before the code
    return [0] * len(nums)
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `product_except_self([1, 2, 3, 4])` | `[24, 12, 8, 6]` |
| 2 | `product_except_self([-1, 1, 0, -3, 3])` | `[0, 0, 9, 0, 0]` |
| 3 | `product_except_self([2, 0, 0])` | `[0, 0, 0]` |
| 4 | `product_except_self([0, 5])` | `[5, 0]` |
| 5 | `product_except_self([7, 3])` | `[3, 7]` |
| 6 | `product_except_self([1, 1, 1])` | `[1, 1, 1]` |
| 7 | `product_except_self([5, -2])` | `[-2, 5]` |
| 8 | `xs = [1] * 100000; xs[10] = 2; xs[500] = 3; sum(product_except_self(xs))` | `599993` |
| 9 | `all('/' not in line.split('#')[0] for line in __learner_source__.splitlines())` | `True` |
| 10 | `sum(1 for l in __learner_source__.splitlines() if l.strip().startswith('#')) >= 3` | `True` |

The big case (`[1] * 100000` with `xs[10] = 2` and `xs[500] = 3`) sums to `6 * 99,998 + 5 = 599,993`, checked by the closed form and the reference; a 50-element version was checked by the brute force.

### l19-a-live-round: A live coding round (15 min; tags `live-round`, `calendar-booking`, `follow-up-layering`)

Objective: Work a 45-minute live problem with two follow-ups. Skills `ci-timed` and `ci-design`. The round (reported for developer roles at trading firms: a 45-to-60-minute problem where requirements are added part-way): a calendar. Minute plan: 5 clarify and examples, 10 base, 5 test, 10 first follow-up, 10 second follow-up, 5 explain. Stage A: `Calendar().book(start, end)` accepts a half-open booking `[start, end)` if it overlaps none. Stage B (follow-up 1): `Calendar(k)` allows up to `k` bookings at any instant. Stage C (follow-up 2): `cancel(start, end)` removes one exact earlier booking and `next_free(duration, after)` returns the earliest whole start at or after `after` where a booking of that length would be accepted.

Screens (11):
1. Hook `problem`, `number-line` with bookings `[1,4)`, `[3,6)`, `[4,8)` and `[0,1)`; `tap-regions` on the bookings: tap the ones that are accepted in order with `k = 1`: `[1,4)`, `[4,8)`, `[0,1)` (the second overlaps the first).
2. `ladder`, `choice`: clarifying questions to ask in the first five minutes (half-open or closed, whole numbers, can bookings be cancelled), with a `why` on each.
3. `problem`, code A, stage A (`pace` 900): sorted starts and ends with `bisect`.
4. `ladder`, `numeric`: stage A on `[1,4)`, `[3,6)`, `[4,8)`, `[0,1)` returns `True, False, True, True`: three accepted.
5. `problem`, code B, stage B (`k`): the sorted-list shortcut breaks, so the starter is the reference of stage B with `_fits` as a stub; the learner counts overlaps at the start and at every booking start inside the new interval.
6. `ladder`, `numeric`: `k = 2` on `[1,4)`, `[3,6)`, `[2,5)`, `[4,8)` returns `True, True, False, True`.
7. `problem`, code C, stage C (`cancel` and `next_free`; the candidates for `next_free` are `after` and the booking ends after it).
8. `ladder`, `numeric`: `k = 1`, bookings `[9,12)` and `[12,15)`: `next_free(3, 9)` is 15; after `cancel(9, 12)` it is 9 (the run `[True, True, 15, 15, True, 9]` with a `next_free(2, 9)` as the third call; by the program and by trying each start in turn).
9. `transfer`, E8: the prose sends the learner to a single-drill stopwatch on an `intervals` drill of difficulty 4 (Python or C++), 45 minutes, to keep the minute plan. A `choice` asks which minute plan fits a 45-minute round with two follow-ups: 5, 10, 5, 10, 10, 5 is correct; 0, 25, 0, 10, 10, 0 and 15, 15, 5, 5, 5, 0 are wrong with a `why` each.
10. `generalise` + `derive` (`order` the 45-minute plan).
11. `transfer`, `choice`: for 10 million bookings the interviewer asks for `O(log n)` per booking with `k` general: a balanced tree or a sorted map of boundary counts (`std::map<int, int>` of +1 and -1 changes, or a sorted container in Python); the learner picks the structure and names the cost.

Quiz (4): the half-open rule; a `k` booking; `next_free` candidates; the minute plan.

**Problems 19.1 to 19.3** `Calendar`; Python; difficulty 3, 4 and 4. Driver `run_cal(k, ops)` (rows `[0, start, end]` book, `[1, start, end]` cancel, `[2, duration, after]` next_free; the driver returns one result per row: a bool for book and cancel, an int for `next_free`). For stage A the driver builds `Calendar()` with no argument. Stage A reference (sorted lists and `bisect`), then the stage B and C reference (a list of bookings and a sweep over the booking starts inside the new interval):

```python
import bisect

class Calendar:
    def __init__(self):
        self.starts, self.ends = [], []       # sorted by start; bookings never overlap

    def book(self, start, end):
        i = bisect.bisect_left(self.starts, start)
        if i > 0 and self.ends[i - 1] > start:
            return False
        if i < len(self.starts) and self.starts[i] < end:
            return False
        self.starts.insert(i, start)
        self.ends.insert(i, end)
        return True
```

```python
class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def _fits(self, start, end):
        points = [start] + [s for s, e in self.bookings if start < s < end]
        for p in points:
            if sum(1 for s, e in self.bookings if s <= p < e) + 1 > self.k:
                return False
        return True

    def book(self, start, end):
        if not self._fits(start, end):
            return False
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        if (start, end) in self.bookings:
            self.bookings.remove((start, end))
            return True
        return False

    def next_free(self, duration, after):
        for t in sorted({after} | {e for s, e in self.bookings if e > after}):
            if self._fits(t, t + duration):
                return t
```

Hidden driver for stages B and C (`postlude`; for stage A replace `Calendar(k)` by `Calendar()`):

```python
def run_cal(k, ops):
    c = Calendar(k)
    out = []
    for op in ops:
        if op[0] == 0: out.append(c.book(op[1], op[2]))
        elif op[0] == 1: out.append(c.cancel(op[1], op[2]))
        else: out.append(c.next_free(op[1], op[2]))
    return out
```

Starter (all stages; `book` always accepts, `cancel` returns `False`, `next_free` returns `after`; stage A fails 4 of 6, stage B 8 of 11, stage C 12 of 16):

```python
class Calendar:
    def __init__(self, k=1):
        self.k = k
        self.bookings = []

    def book(self, start, end):
        self.bookings.append((start, end))
        return True

    def cancel(self, start, end):
        return False

    def next_free(self, duration, after):
        return after
```

Stage A tests (`k = 1`, book rows only; the last row books 3,000 disjoint bookings then one that overlaps them all, and counts the `True` results: 3,000):

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_cal(1, [[0, 10, 20], [0, 15, 25], [0, 20, 30]])` | `[True, False, True]` |
| 2 | `run_cal(1, [[0, 0, 5], [0, 5, 10], [0, 3, 6], [0, 10, 11], [0, 4, 5]])` | `[True, True, False, True, False]` |
| 3 | `run_cal(1, [[0, 5, 10], [0, 0, 5], [0, 10, 15], [0, 0, 15]])` | `[True, True, True, False]` |
| 4 | `run_cal(1, [[0, 1, 2]])` | `[True]` |
| 5 | `run_cal(1, [])` | `[]` |
| 6 | `ops = [[0, 2 * i, 2 * i + 1] for i in range(3000)] + [[0, 0, 6000]]...` | `3000` |

Stage B tests (all stage A rows, plus these):

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_cal(2, [[0, 10, 20], [0, 15, 25], [0, 20, 30], [0, 12, 18]])` | `[True, True, True, False]` |
| 2 | `run_cal(2, [[0, 10, 20], [0, 15, 25], [0, 5, 15], [0, 5, 11]])` | `[True, True, True, False]` |
| 3 | `run_cal(3, [[0, 1, 5], [0, 2, 5], [0, 3, 5], [0, 4, 5], [0, 0, 2]])` | `[True, True, True, False, True]` |
| 4 | `run_cal(1, [[0, 1, 3], [0, 3, 5]])` | `[True, True]` |
| 5 | `run_cal(2, [[0, 0, 10], [0, 0, 10], [0, 10, 20], [0, 5, 15]])` | `[True, True, True, False]` |

Stage C tests (all stage A and B rows, plus these):

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_cal(1, [[0, 10, 20], [1, 10, 20], [0, 15, 25], [1, 15, 26], [1,...` | `[True, True, True, False, True, True]` |
| 2 | `run_cal(1, [[0, 10, 20], [0, 30, 40], [2, 5, 0], [2, 10, 5], [2, 10...` | `[True, True, 0, 20, 20, 40, 40]` |
| 3 | `run_cal(2, [[0, 0, 10], [0, 0, 10], [2, 5, 0], [1, 0, 10], [2, 5, 0...` | `[True, True, 10, True, 0, 3]` |
| 4 | `run_cal(1, [[2, 5, 7]])` | `[7]` |
| 5 | `run_cal(1, [[0, 0, 3], [0, 3, 6], [0, 9, 12], [2, 3, 0], [2, 4, 0],...` | `[True, True, True, 6, 12, True, 3]` |

Checks: stage A (`bisect`) and stages B and C were each compared with a brute force that checks every integer time for occupancy, on 2,000 random book-only streams (stage A) and 3,000 random streams with all three operations and `k` from 1 to 3 (B and C). The stage C `next_free` result is the same as scanning start times one by one.

### Level 4 review (`review-4.json`, 10 items, difficulty 2 to 4, interleaving all five lessons, every case unseen in the lessons, each with `tags` and `skills`; `timed: { "seconds": 600, "lockAtZero": false }`)

| # | Lesson | Widget | d | Prompt (summary) | Key |
| --- | --- | --- | --- | --- | --- |
| 1 | l15 | `numeric` | 3 | Problems `(30, 15, 10, 5)`, `(50, 30, 20, 10)`, `(80, 45, 25, 15)` (full points, full minutes, partial points, partial minutes), budget 55. Best points. | 100 (the third problem full, 45 minutes, and the second partial, 10 minutes) |
| 2 | l15 | `numeric` | 3 | The same problems: points from taking them by points per minute, full marks only, within 55 minutes. | 80 (the first, 15 minutes, then the second, 30 minutes) |
| 3 | l16 | `multi` | 3 | For `second_largest(xs)` (the second largest distinct value, or `None` if there are fewer than two distinct values), which inputs are edge cases worth a test: `[]`, `[5]`, `[5, 5]`, `[3, 1, 2]`, `[2, 2, 1]`? | `[]`, `[5]`, `[5, 5]`, `[2, 2, 1]` (`[3, 1, 2]` is the ordinary case) |
| 4 | l16 | `numeric` | 3 | `second_largest([4, 4, 3, 3, 1])`. | 3 |
| 5 | l17 | `numeric` | 2 | A 60-minute plan has 5 minutes reading and 5 minutes testing; the first problem took 31 minutes. Minutes left for the second. | 19 |
| 6 | l17 | `numeric` | 3 | `count_subarrays_sum_k([3, 4, 7, 2, -3, 1, 4, 2], 7)`. | 4 (computed by prefix sums and by listing all 36 subarrays) |
| 7 | l17 | `numeric` | 3 | Inner-loop steps of the quadratic count for `n = 200,000`: `n (n + 1) / 2`. | 20,000,100,000 |
| 8 | l18 | `numeric` | 3 | `product_except_self([1, 2, 3, 4])`: the entry at index 2. | 8 (`[24, 12, 8, 6]`) |
| 9 | l19 | `numeric` | 3 | `Calendar()` (k = 1) books `[10,20)`, `[15,25)`, `[20,30)`: how many are accepted? | 2 |
| 10 | l19 | `numeric` | 3 | Bookings `[10,20)` and `[30,40)`, `k = 1`: `next_free(11, 10)`. | 40 (a start at 10 overlaps; at 20 a booking of 11 reaches 31, which overlaps `[30,40)`) |

The numbers are in `numbers_check.py`, `numbers_check3.py` and `numbers_check4.py`, each computed by two methods. Item 3's second largest distinct values were checked with a sort of the distinct values and a one-pass method.

### Level 4 homework (`homework-4.json`, 8 items, difficulty 3 to 5 with at least one 5, `tags` on each; one `longform`, two E11 `parts` items, one C++ `code` item)

| # | Lesson | Kind | d | Item | Key or reference |
| --- | --- | --- | --- | --- | --- |
| 1 | l19 | `parts` (E11): `code`, `choice`, `code` | 4 | A live round on a leaderboard (below). | tests and keys below |
| 2 | l19 | `parts` (E11): `numeric`, `choice`, `numeric` | 4 | Follow-ups on the calendar (below). | 499,500; the sorted structure; 20 |
| 3 | l17 | `code` (C++) | 4 | `longest_consecutive` in C++ (below). | tests below |
| 4 | l18 | `longform` | 5 | Say aloud, timing yourself to 6 minutes, the first part of a live round on `count_subarrays_sum_k`: restate, an example, the brute force and its cost, the prefix-sum idea, the plan as comments, then the complexity. | Model answer: restate (count the subarrays with sum `k`); example `[1, 1, 1]` with `k = 2` gives 2; the brute force is `O(n^2)`, 20,000,100,000 steps at `n = 200,000`; the prefix sum `S_j - S_i = k` means we count earlier prefix sums equal to `S_j - k` in a dict; plan; `O(n)` time and `O(n)` memory. Rubric (10): 2 restates and an example, 2 brute force with its cost, 2 the prefix-sum idea, 2 the plan before code, 2 complexity stated. |
| 5 | l19 | `numeric` | 4 | A leaderboard with 100,000 players answers 2,000 `top(10)` queries; sorting every score each time visits how many scores, and how many times more than a maintained top 10 that touches 10 entries per query? | 200,000,000 visits; 10,000 times more (`100,000 / 10`) |
| 6 | l15 | `order` | 4 | The first five minutes of an assessment: read every statement; note constraints and points; estimate full and partial minutes; choose full, partial or skip by points per minute and the budget; start the surest problem. Distractors: "start with the hardest problem" and "write code for the first problem before reading the others", each with a `why`. |
| 7 | l15 | `numeric` | 4 | The lesson's problems (below, in l15) with a budget of 60: best points. | 102 (and the greedy by points per minute gives 100) |
| 8 | l16 | `choice` | 4 | For `longest_consecutive`, a learner's tests so far are `[]`, `[5]`, `[1, 2, 3]` and `[1, 1, 1]`. Which test is the one most worth adding? | `[100, 4, 200, 1, 3, 2]` (shuffled, with a gap; the answer is 4). Distractors: `[2, 3, 4]` (a sorted run again), `[0]` (a single again), `[1, 2]` (a short run). |

Item 7 uses the lesson's problem set P1 `(40, 20, 12, 6)`, P2 `(60, 35, 25, 12)`, P3 `(90, 50, 30, 18)` at budget 60; the lesson itself uses budget 62 (and states 100 and 115), so the homework number 102 is new. Computed twice in `numbers_check4.py`.

**Homework item 1 (E11 parts), live round on a leaderboard.** Part 1 (code, difficulty 3): `Leaderboard` with `add_score(player, delta)` and `top(k)`, the sum of the `k` highest scores. Part 2 (choice, difficulty 4): "The interviewer says there are 100,000 players and 2,000 `top(10)` calls. What do you change?": keep a size-10 structure updated on each score change, rather than sorting every time (distractors: sort once and never update; use a list instead of a dict; recompute `top` only on the first call). Part 3 (code, difficulty 5): add `reset(player)`, which sets a player's score to zero and removes the player from the board. Driver `run_board(ops)` with rows `[0, player, delta]` add, `[1, k]` top, `[2, player]` reset; the driver returns the `top` results. Reference and starter for part 1 (the starter returns 0 from `top`; fails 3 of 4), reference and starter for part 3 (the starter's `reset` does nothing; fails 3 of 4), both with the driver; the part 3 starter shows part 1's reference. Brute force: a `Counter` sorted on every `top`; 2,000 random runs agreed.

```python
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])
```

```python
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return 0
```

```python
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return sum(sorted(self.scores.values(), reverse=True)[:k])

    def reset(self, player):
        self.scores.pop(player, None)
```

```python
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_score(self, player, delta):
        self.scores[player] = self.scores.get(player, 0) + delta

    def top(self, k):
        return 0

    def reset(self, player):
        pass
```

```python
def run_board(ops):
    b = Leaderboard()
    out = []
    for op in ops:
        if op[0] == 0: b.add_score(op[1], op[2])
        elif op[0] == 1: out.append(b.top(op[1]))
        else: b.reset(op[1])
    return out
```

Part 1 tests (rows without `reset`):

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_board([[0, 1, 73], [0, 2, 56], [0, 3, 39], [0, 4, 51], [0, 5, 4...` | `[73, 180]` |
| 2 | `run_board([[0, 1, 5], [0, 1, 7], [1, 1], [1, 3]])` | `[12, 12]` |
| 3 | `run_board([[1, 2]])` | `[0]` |
| 4 | `run_board([[0, 1, 10], [0, 2, 20], [0, 3, 30], [1, 2], [1, 2], [1, ...` | `[50, 50, 60]` |

Part 3 tests (all rows, with `reset`):

| # | Call | Expected |
| --- | --- | --- |
| 1 | `run_board([[0, 1, 73], [0, 2, 56], [0, 3, 39], [0, 4, 51], [0, 5, 4...` | `[73, 102]` |
| 2 | `run_board([[0, 1, 5], [0, 1, 7], [1, 1], [1, 3]])` | `[12, 12]` |
| 3 | `run_board([[1, 2]])` | `[0]` |
| 4 | `run_board([[0, 1, 10], [0, 2, 20], [0, 3, 30], [1, 2], [2, 3], [1, ...` | `[50, 30, 30]` |

**Homework item 2 (E11 parts), calendar follow-ups.** Part 1 (`numeric`): 1,000 bookings are accepted one at a time into a list that `book` scans in full; how many booking comparisons are made in all? 499,500 (`0 + 1 + ... + 999`, and `1,000 * 999 / 2`). Part 2 (`choice`): "Thousands of bookings a second; what do you do for `k = 1`?": keep the starts and ends sorted and use `bisect` for an `O(log n)` check (distractors: scan faster, cache the last booking only, sort the list on every `book`). Part 3 (`numeric`): the number of comparisons a binary search needs on 1,000,000 bookings, as a whole number rounded up: 20 (`ceil(log2(10^6))`, and `(10^6).bit_length()`).

**Problem H4.3** `longest_consecutive(nums)` in C++; difficulty 4; the same statement and eight small cases as `l17` Python, `std::vector<int>` in and `int` out (`args: [[100,4,200,1,3,2]]`, `types: ["std::vector<int>"]`), plus two large cases built in `call`: a permutation-like list of 200,000 values `(i * 7919) % 200003` whose expected longest run is 176,246 (from a sort-and-scan brute force), and 200,000 even numbers (expected 1). The starter is a correct but quadratic `std::find` loop (it passes the small cases and is stopped by the clock on the large ones: 6.6 s natively on the even list, longer in wasm and longer still on the permutation). Reference verified on all ten cases under `-std=c++17` and `-std=c++20`.

```cpp
#include <vector>
#include <unordered_set>
#include <algorithm>
int longest_consecutive(std::vector<int> nums) {
    std::unordered_set<int> present(nums.begin(), nums.end());
    int best = 0;
    for (int x : present) {
        if (present.count(x - 1)) continue;
        int length = 1;
        while (present.count(x + length)) ++length;
        best = std::max(best, length);
    }
    return best;
}
```

```cpp
#include <vector>
#include <unordered_set>
#include <algorithm>
int longest_consecutive(std::vector<int> nums) {
    int best = 0;
    for (int x : nums) {
        int length = 1;
        while (std::find(nums.begin(), nums.end(), x + length) != nums.end()) ++length;
        best = std::max(best, length);
    }
    return best;
}
```

| # | Call | Expected |
| --- | --- | --- |
| 1 | `longest_consecutive([100, 4, 200, 1, 3, 2])` | `4` |
| 2 | `longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])` | `9` |
| 3 | `longest_consecutive([])` | `0` |
| 4 | `longest_consecutive([5])` | `1` |
| 5 | `longest_consecutive([1, 2, 0, 1])` | `3` |
| 6 | `longest_consecutive([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6])` | `7` |
| 7 | `longest_consecutive([1, 1, 1])` | `1` |
| 8 | `longest_consecutive([-2, -1, 0, 1])` | `4` |

### Level 4 report notes

Report as `docs/LEVEL-BRIEF.md` says, naming where E3, E8 and E11 were used and whether the filter slugs matched. Do not edit files outside `app/content/courses/coding-int/`.

# Concept audit, round 2 (blind): algo-think L1 to L3

Auditor: Fable reader, 13 Nov 2026, branch tip `b4eb9cdb` of `claude/fable-audit`. Scope: every file in `app/content/courses/algo-think/` (`l1` to `l14`, `review-1` to `review-3`, `homework-1` to `homework-3`). Stage 1, topic 1.8, full ledger depth.

Blind rule kept: the ledger, the findings below and the concepts script were written and committed (WIP commit) before any of `docs/reviews/audit-algo-think*`, `docs/reviews/review-1.8.md`, `docs/reviews/voice-1.8-algo-think.txt` or any `docs/reports/*algo-think*` or `*1.8*` file was opened. The earlier number and concepts scripts were run, not opened.

## Result

- Ledger: `docs/reports/audit-algo-think-1-3-r2-ledger.md`, 297 rows: 289 correct, 5 imprecise, 2 wrong, 1 unverified. Rows group the hints and feedback of a screen with its key where they state one claim; every line was read and judged.
- Findings: 8, all `minor`. 2 `wrong`, 6 `imprecise` (one of them the `unverified` row). 0 `serious`.
- No finding touches a definition, a theorem, a complexity class, a graded key or a code solution. All eight are feedback, `why` or explain sentences.

## Method

- Every complexity, operation-count, memory and code-behaviour claim was run: `docs/reports/algo-think-L1-3-r2-concepts.py`, 146 checks under CPython 3.13.18 and 144 under Pyodide 0.27.7 (Python 3.12.7, wasm32; the two 64-bit size checks become one 32-bit check). Comparisons, calls and frames are counted by instrumented copies of the taught code; worst cases are brute-forced (binary search to n = 600, the leftmost search to n = 129, all 5,040 orders of 7 values for insertion sort and quicksort); `tracemalloc` peaks are measured; coin systems are checked against a dynamic programme to 2,000; earliest-finish-first is checked against brute force on 1,500 random diaries; quickselect and quicksort averages are Monte Carlo (seeded).
- All 41 code widgets were run in Pyodide 0.27.7 with the widget's own prelude, postlude, setup and tests: every solution passes every hidden test, every starter fails. Harness: a node loader for the local Pyodide package and a Python runner (kept in the scratchpad, not committed).
- Hand traces: every `manipulate` state, table key, `wrong[]` value and slip feedback was traced or recomputed.
- Big-O statements were checked against their stated case (worst, average, amortised) and conditions. Greedy claims were checked for the condition that makes greedy correct: the coin system (UK coins: verified optimal; 1, 3, 4 and 1, 10, 25 and 1, 5, 12: counterexamples), earliest finish (exchange argument), fractional against 0/1 knapsack, one order against many. Each is stated in the content.

Two claims deserve a note although they pass:

- l6 `screens[3]` and `screens[7]`: "a huge recursion limit lets the real stack overflow, and Python can crash with no traceback". On this page's Python the pure-Python `sum_to(5000)` runs once the limit is raised (pure-Python calls stopped using the C stack in 3.11). The claim still holds as written ("can"): recursion through built-in code, 5,000 deep with the limit at 10^9, kills Pyodide 0.27.7 with a fatal `RangeError`. The Python docs give the same warning. Verdict: correct.
- l13 `summary.formula.note`: "about 1.39 n log2 n" is the leading term. At n = 20,001 the measured mean is 2(n+1)H_n - 4n, about 1.19 n log2 n. Standard statement (Sedgewick and Wayne 2.3). Verdict: correct.

## Findings

1. `l14-best-step-now.json` | `quiz[2].feedback.byKey.whole` (slip 30) | wrong, minor | The feedback says "You took whole items by value: 20 and 10." Whole items taken in value order are 20 (weight 4) then 18 (weight 6); both fit and give 38, the right answer. The named mistake does not produce 30. | Script check `FINDING 1`: by value gives 38; the two lightest items whole (weights 4 and 5) give 20 + 10 = 30. | Replace with: "You took the two lightest items whole: 20 and 10. Rank by value per weight instead, and parts are allowed."

2. `l12-merge-sort.json` | `screens[2].feedback.byKey.test-9` | wrong, minor | "Sorting the joined list, or `pop(0)`, is too slow; walk two indices." Neither named cause fails test 9. `sorted(a + b)` on the two 50,000-value lists takes 2 ms (the lists are two runs, which Timsort merges in one pass). A `pop(0)` merge takes 0.9 s in Pyodide 0.27.7, under the 5 s case limit. | Script check `FINDING 2`; timing run in Pyodide. | Replace with: "Test 9 merges 100,000 values and has 5 seconds. Walk two indices once through the lists, and do not rebuild a list at each step." Also see the inbox bullet: the exercise accepts `return sorted(a + b)`.

3. `l4-cheap-on-average.json` | `screens[7].feedback.byKey.to-1000` (slip 50,500) | imprecise, minor | "The array is never full at 1,000 here: the last resize is at size 990." After the 1,000th append size and capacity are both 1,000, so the array is full. What is true: no append finds it full at 1,000, so nothing is copied then. | Script check `FINDING 3 and 4` (simulation: capacity 1,000, size 1,000). | Replace with: "No resize happens at size 1,000: the array fills there, but no append follows. The last resize is at size 990."

4. `review-1.json` | `items[6].feedback.byKey.to-thousand` (slip 5,500) | imprecise, minor | Same statement: "The array is not full at 1,000 within these appends." It is full after append 1,000. | Same check (capacity 100, step 100). | Replace with: "The array fills at 1,000, but no append follows, so nothing is copied then. The last resize is at size 900."

5. `homework-3.json` | `items[6].feedback.byKey.test-8` | imprecise, minor | "Test 8 is already sorted. A fixed end pivot makes that O(n^2); pick the pivot at random." Test 8 is `kth_largest(list(range(5000)), 1)`. With the last value as pivot, the scheme the course teaches, the first partition puts the pivot at the target index: 4,999 comparisons, linear. Only a fixed first pivot is quadratic there (12,497,500 comparisons). | Script checks `FINDING 5` and `homework-3 I6 fix text`. | Replace with: "Test 8 is already sorted. A fixed first pivot peels off one value per round there, which is $O(n^2)$; pick the pivot at random." The test itself does not catch a fixed last pivot; see the inbox bullet.

6. `l13-quicksort.json` | `screens[5].feedback.byKey.nlogn` (slip 14) | imprecise, minor | "You assumed even splits." Even splits of 7 values cost 6 + 2 + 2 = 10 comparisons (the minimum over all 5,040 orders), not 14. The slip 14 is 7 comparisons on each of 2 levels. | Script check `FINDING 6`. | Replace the first sentence with: "You charged 7 comparisons to each of 2 levels, as if the splits were even." Keep the second sentence.

7. `l11-sorting-by-hand.json` | `quiz[3].widget.options[2].why` (option `c`) | imprecise, minor | "That is only for input already in order." Timsort is also O(n) on exactly reversed input (a descending run is reversed in place): n - 1 comparisons on 20,000 reversed values. | Script checks `FINDING 7` and `l11 Q3 fix text`; `listsort.txt` in the CPython source. | Replace with: "That is the best case, for input already in order or exactly reversed. On random prices Timsort needs $O(n \log n)$."

8. `l1-counting-work.json` | `quiz[2].explain.text`, last sentence | imprecise (ledger verdict `unverified`), minor | "A daily job over 10,000 instruments cannot afford a further loop over $n$ inside its pair loop." An unsourced feasibility claim. The loop would cost about 5 x 10^11 steps, which is minutes in compiled code and hours in Python: slow, not impossible for a nightly job. | Script check `l1 Q2 further loop is 5e11 steps`. | Replace the sentence with: "A further loop over $n$ inside the pair loop would multiply that by 10,000: about $5 \times 10^{11}$ steps."

## Gates

- Validator (`node tools/validate.mjs`, from `app/`): 0 errors, 4,531 warnings; `content/manifest.json` unchanged.
- Number scripts, run without opening: `docs/reports/algo-think-2-perf-numbers.py` exit 0; `docs/reports/algo-think-3-perf-numbers.py` exit 0; the round 1 `docs/reports/algo-think-L1-3-concepts.py` exit 0.
- `node tools/grade-all.mjs --file ...` on the three review and three homework files: 33 widgets, 0 failures. On all 20 files: 177 widgets, 0 failures.
- Round 2 concepts script: exit 1 with 6 failing checks, each one a finding above (findings 3 and 4 share a check; finding 8 has none). It exits 0 once findings 1 to 7 are fixed and their checks are updated to the new text.
- Code widgets in Pyodide 0.27.7: 41 of 41 solutions pass, 41 of 41 starters fail.
- No playthrough: no content changed.

## Overlap table

Filled after the WIP commit; see the end of this file.

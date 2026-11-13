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

Read after WIP commit `e38802fc`: `docs/reviews/audit-algo-think-1-3.md` (round 1 audit, its fix pass and its fix-pass read), `docs/reviews/review-1.8.md` (algo-think part only) and `docs/reviews/voice-1.8-algo-think.txt` (sentence lengths, nothing conceptual).

Earlier conceptual findings on algo-think: 2 in the 1.8 review (the "each coin at least double" rule in `homework-3` `items[1]`; the 32-bit sizes in `l3` `screens[4]`), 22 in the round 1 audit (wrong 3, imprecise 18, misleading 1; 2 serious) plus its 2 unverified rows, and 0 in the fix-pass read (37 rows, all correct). All 26 were fixed before this round. This audit read the fixed text of each as ordinary ledger rows and found every one correct. None of them is among the 8 findings above, and none of the 8 was raised by any earlier read. The 1.8 review's note on `homework-3` `items[6]` concerns test 9 and an O(nk) method, not the test 8 feedback of finding 5.

| Conceptual findings | Count |
|---|---|
| Found by this round only | 8 (wrong 2, imprecise 6; all minor) |
| Found by an earlier read only (1.8 review, round 1 audit, fix-pass read) | 26 (2 + 24 + 0), all fixed and now correct |
| Found by both | 0 |

New `wrong` findings that no earlier read found: **2** (findings 1 and 2). Both are minor, both are feedback lines, and neither is text written by the round 1 fix pass. That is one above the convergence limit of one new `wrong` per three levels. The six `imprecise` findings are new as well. No serious finding in this round, against 2 in round 1.

## Inbox

Four bullets appended to `docs/BACKLOG-INBOX.md` under `Raised later (audit algo-think):` (round 2): slip feedback is not checked against its value; `merge` can be passed by `sorted(a + b)`; `kth_largest` test 8 does not catch a fixed pivot; a Pyodide `--code` mode for `grade-all.mjs`.

## Fix pass

Opus fixer, 13 Nov 2026. Every candidate mistake below was run in Pyodide 0.27.7 (node loader, the page's recursion limit of 3,000 from `js/screens/drill-worker.js`) and in CPython. No graded key, tolerance, `wrong[]` option or slip value changed; no test changed.

1. `l14` `quiz[2]` `whole` (30): **fixed differently.** Recomputed twice (greedy loop and by hand): whole items by value give 20 + 18 = 38; the two lightest whole (weights 4 and 5) give 20 + 10 = 30; lightest first with parts gives 33; so 30 is "lightest, whole" and collides with neither 38 nor 48. New text: "You took the two lightest items whole: 20 and 10. Rank by value per unit of weight instead: 5, 3 and 2." (The auditor's "parts are allowed" dropped: parts are not what 30 misses, since 0/1 and fractional both give 38.)
2. `l12` `screens[2]` `test-9`: **fixed differently.** Runs on test 9: `sorted(a + b)` 0.01 s, `pop(0)` 0.9 s and `a = a[1:]` 4.0 s all pass; a recursive merge raises `RecursionError`; `out = out + [x]` takes 9.3 s against the 5 s case limit. New text names only the two that fail: "Test 9 merges 100,000 values. A recursive merge hits Python's recursion limit there, and `out = out + [x]` is too slow. Walk two indices in one loop."
3. `l4` `screens[7]` `to-1000` (50,500): **fixed differently** (wording). Simulation: size and capacity 1,000 after append 1,000, no copy at that append; 49,500 + 1,000 = 50,500. "You counted a resize at size 1,000. The array fills there, but no append follows, so nothing is copied. The last resize is at size 990."
4. `review-1` `items[6]` `to-thousand` (5,500): **fixed differently** (same wording, last resize 900; 4,500 + 1,000 = 5,500).
5. `homework-3` `items[6]` `test-8`: **fixed differently.** Run on test 8: fixed last pivot 4,999 comparisons, passes; fixed first pivot in a loop is quadratic (12,497,500 comparisons) yet passes in 0.5 s; only the recursive first-pivot form fails, nesting 5,000 calls past the limit. New text: "Test 8 is 5,000 sorted values. A fixed first pivot drops one value per round, so a recursive version nests about 5,000 calls. That is past Python's recursion limit; pick the pivot at random."
6. `l13` `screens[5]` `nlogn` (14): **fixed** as proposed. Brute force over all 5,040 orders: minimum 10 comparisons; 7 x 2 = 14.
7. `l11` `quiz[3]` option `c`: **fixed differently.** Counted: 19,999 comparisons on 20,000 values ascending and on strictly descending; Timsort reverses only strictly descending runs (`listsort.txt`), so "exactly reversed" became "in strictly falling order": "That is the best case, for input already in order or in strictly falling order."
8. `l1` `quiz[2]` explain: **fixed** as proposed. 10,000 x 9,999 / 2 = 49,995,000; x 10,000 = 4.9995 x 10^11.

Same-screen sweep. `homework-3` `items[6]` `test-2` named index `k - 1`, which already fails test 1 (it returns 1, not 9), so test-2 never showed for it: **fixed**, now "Test 1 passed, so check how your target index depends on $k$: the $k$th largest sits at index `len(xs) - k` of the sorted order." Other keys on the touched screens (`l14` `best` 48; `l4` `resizes` 99, `doubling` 1,023, `ten-each` 990; `review-1` 9 and 900; `l13` `shuffled` 12, `square` 49; `l12` `test-6`, `test-2`; `homework-3` `test-7`, `test-10`) recomputed or run: correct.

Not applied, outside the touched screens (for the orchestrator): `l13` `screens[8]` `test-7` says "A fixed end pivot makes this $O(n^2)$". True, but a fixed end pivot passes test 7 (`quickselect(list(range(3000)), 1500)`): 0.31 s in Pyodide, loop or recursive (1,500 deep, under 3,000). Same class as finding 5 and the test-8 inbox bullet.

Scripts: `algo-think-L1-3-r2-concepts.py` now 150 checks, exit 0 (CPython 3.13) and 148, 0 failing under Pyodide; each `FINDING` check is replaced by a `fixed:` check of the new text, plus checks for the recursive merge, the recursive first pivot and test-2. `algo-think-L1-3-concepts.py` exit 0 (124 of 124); `algo-think-2-perf-numbers.py` and `-3-` exit 0. Validator 0 errors, 4,531 warnings, manifest unchanged; voice scan 35: 0 and 0. Playthrough desktop and mobile green: `l1`, `l4`, `l11`, `l12`, `l13`, `l14`, `review-1`, `homework-3`.

## Fix-pass read

Reader: fresh, has not seen the audit, its ledger or the fix-pass notes. Diff read: `git diff aea02fb9~1 aea02fb9 -- app/content/courses/algo-think/` (8 files, 9 changed strings), plus one named row outside the diff (`l13-quicksort.json` `screens[8]` `test-7`).

Method. Numbers recomputed from each item's data in a script and by hand. Code rows: 21 submissions written and run against the items' own tests, in CPython 3 and in Pyodide 0.27.7 (node, local copy), both with the recursion limit the page sets: `RECURSION_LIMIT = 3000` in `app/js/screens/drill-worker.js` (not 1,000). The per-test limit is `TEST_MS = 5000` in `app/js/engine/widgets/code.js`. Solutions pass and starters fail in both.

| # | File | JSON path | New text (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | homework-3.json | items[6] (`h-kth-largest`) feedback.byKey.test-2 | "Test 1 passed, so check how your target index depends on $k$ ... index `len(xs) - k`" | correct | Sorted data 1 2 4 5 7 8 9: 3rd largest is 7, index 7 - 3 = 4. Run: a target that ignores k (`len - 1`) and an off-by-one target (`len - k - 1` for k > 1) both pass test 1 and first fail test 2. The old line's `k - 1` first fails test 1, so removing it was right. |
| 2 | homework-3.json | items[6] feedback.byKey.test-8 | "5,000 sorted values. A fixed first pivot drops one value per round, so a recursive version nests about 5,000 calls. That is past Python's recursion limit; pick the pivot at random." | correct | Run: fixed first pivot, recursive (in place and on slices) passes tests 1 to 7 and raises RecursionError on test 8, in CPython and Pyodide at limit 3,000 (5,000 > 3,000 > 1,000). Random pivot, recursive: all 10 pass. A fixed end pivot passes test 8 in one round (pivot 4,999 lands on the target), so "first" is the right word. Fixed first pivot as a loop passes (0.62 s in Pyodide); the line limits itself to "a recursive version", so it agrees. |
| 3 | l1-counting-work.json | quiz[2] (`q-universe`) explain.text | "A further loop over $n$ inside the pair loop would multiply that by 10,000: about $5 \times 10^{11}$ steps." | correct | 10,000 x 9,999 / 2 = 49,995,000; x 10,000 = 4.9995 x 10^11. Ratio to 1,999,000 is 25.01, as the first sentence says. |
| 4 | l11-sorting-by-hand.json | quiz[3] (`q-sorted`) options[2].why | "That is the best case, for input already in order or in strictly falling order." | correct | Timsort's run detection takes one ascending or one strictly descending run and reverses it. Counted comparisons with `sorted` and `cmp_to_key`: n - 1 for ascending and for strictly descending at n = 10,000 and 100,000. Agrees with the question (worst case) and the key. |
| 5 | l12-merge-sort.json | screens[2] feedback.byKey.test-9 | "A recursive merge hits Python's recursion limit there, and `out = out + [x]` is too slow. Walk two indices in one loop." | correct | Run: recursive merge passes tests 1 to 8, RecursionError on test 9. `out = out + [x]` with two indices passes 1 to 8 and takes 10.8 s (CPython) and 11.8 s (Pyodide) on test 9, over the 5 s limit. `sorted(a + b)` passes; `pop(0)` passes in 0.91 s in Pyodide, so dropping those two claims was right. |
| 6 | l13-quicksort.json | screens[5] feedback.byKey.nlogn | "You charged 7 comparisons to each of 2 levels, as if the splits were even." | correct | 7 x 2 = 14, the slip value; 7 values split evenly give 2 partition levels (7, then 3 and 3). True count 6 + 5 + 4 + 3 + 2 + 1 = 21, the key. |
| 7 | l14-best-step-now.json | quiz[2] (`q-frac`) feedback.byKey.whole | "You took the two lightest items whole: 20 and 10. Rank by value per unit of weight instead: 5, 3 and 2." | correct | Weights 4, 6, 5: the two lightest are 4 and 5 (weight 9, fits), values 20 + 10 = 30, the slip value. Ratios 20/4, 18/6, 10/5 = 5, 3, 2. The two largest values give 38, so the old "by value" wording could not produce 30. |
| 8 | l4-cheap-on-average.json | screens[7] feedback.byKey.to-1000 | "You counted a resize at size 1,000. The array fills there, but no append follows, so nothing is copied. The last resize is at size 990." | correct | 10 + 20 + ... + 1,000 = 50,500, the slip value. Simulation: 1,000 appends give 99 resizes, 49,500 copies, last resize at append 991 copying 990, and size equals capacity (1,000) after the last append. |
| 9 | review-1.json | items[6] (`r-fixed-100`) feedback.byKey.to-thousand | "You counted a resize at size 1,000. ... The last resize is at size 900." | correct | 100 + ... + 1,000 = 5,500, the slip value. Simulation: 9 resizes, 4,500 copies, last at append 901 copying 900, array full at 1,000 after the last append. |
| 10 | l13-quicksort.json | screens[8] feedback.byKey.test-7 (outside the diff) | "Test 7 is sorted input. A fixed end pivot makes this $O(n^2)$; pick the pivot at random." | misleading (minor) | The complexity claim is true (about 1,500 rounds, 3.4 million comparisons). But a fixed end pivot does not fail test 7: as a loop, as a recursion and as a recursion on slices it passes all 9 tests, test 7 in 0.30 s, 0.31 s and 0.35 s in Pyodide (0.16 s to 0.18 s in CPython). The reported 0.31 s is confirmed. What does first fail test 7 with a fixed end pivot is a recursion that sorts both sides: 3,000 sorted values nest about 3,000 calls and raise RecursionError at limit 3,000 (run, both interpreters). The same full sort with a random pivot passes all 9. |

### Findings

1. `l13-quicksort.json` `screens[8].feedback.byKey.test-7`: misleading, minor. The line shows only when test 7 fails, and names a mistake that passes it. The advice (random pivot) does cure the submissions that really fail there, so no learner is sent the wrong way; the stated cause is off. Replacement, checked against the runs above (two submissions that recurse on both sides with a fixed end pivot pass tests 1 to 6 and fail test 7 with RecursionError; the random-pivot version passes):

   `"test-7": "Test 7 is 3,000 sorted values. A fixed end pivot drops one value per call there, so a recursion that sorts both sides nests about 3,000 calls. That is past the recursion limit; pick the pivot at random."`

   It agrees with the screen's `how` ("A hand-written full sort also passes"), which holds for a random pivot.

Rows 1 to 9: no findings.

### Notes outside the rows

- `l12-merge-sort.json` `screens[2].feedback.byKey.test-6` (unchanged, not judged as a row): a merge that drops both tails first fails test 1 (run: the 15 is lost), and one that drops only the tail of `a` first fails test 3 by the same reasoning. The "You dropped the leftover tail" line may therefore never show for that mistake. Worth a look in a later pass.
- Row 5, optional: the remedy names two indices but not `append`; "Walk two indices in one loop and `append`." would cover the second named cause. Not required.

## Fix-pass follow-up

Fixer: Opus, after the fix-pass read. Method: for every `feedback.byKey.test-N` line on a code widget in the L1 to L3 lesson, review and homework files (41 widgets, 127 lines), I wrote the submission each line names (or the natural mistakes near it), ran it against the item's own tests through a harness that copies the widget's (one namespace, prelude, learner code, postlude, each case's setup then call, the same `equal`/`isclose` judge), with `sys.setrecursionlimit(3000)` as in `app/js/screens/drill-worker.js`, and recorded the first failing test. Timing ran in CPython with an alarm at 5 s / 3, and the borderline cases again in Pyodide 0.27.7 (node, local copy). About 180 submissions in all, plus each item's solution (passes) and starter (fails). Check: the named mistake passes tests 1 to N-1 and fails test N; a line that names no cause must be a true description of test N. Tests are unchanged.

### The two named lines

1. `l13-quicksort.json` `screens[8].feedback.byKey.test-7`: fixed differently. Runs (CPython and Pyodide, limit 3,000): in-place Lomuto, fixed end pivot, recursing on both sides: RecursionError on test 7, tests 1 to 6 pass. The same on slices: RecursionError on test 7. The same recursing on the smaller side and looping on the larger: all 9 pass (test 7 0.40 s in Pyodide). Random pivot, both sides: all 9 pass. Quickselect with a fixed end pivot, recursive on one side: all 9 pass (1,500 deep, 0.31 s in Pyodide), so the slow complexity alone never fails test 7. The reader's text is true of the failing submissions, but "a recursion that sorts both sides" also covers the smaller-side version, which passes, and its remedy omits the screen's own cure. New: "Test 7 is 3,000 sorted values. A fixed end pivot peels off one value per call there, so recursing into both sides nests about 3,000 calls: past the recursion limit. Keep only the side that holds `k`, with a random pivot." Both cures were run: one side only passes, a random pivot passes.
2. `l12-merge-sort.json` `screens[2].feedback.byKey.test-6`: fixed. Runs: dropping both tails fails test 1; dropping only `a`'s tail fails test 3; dropping only `b`'s tail fails test 1 (the reader is right about those). But guards `if not a: return list(b)` and `if not b: return list(a)` plus a loop that keeps only `b[j:]` pass tests 1 to 5 and first fail test 6 (`[1, 2, 3, 4]`, the 5 lost). That is a natural shape: the example leaves its tail in `b`, and the guards cover tests 2 to 4. New: "Test 6 leaves 5 in `a` after `b` runs out. You kept the tail of `b` but dropped the tail of `a`; extend with both `a[i:]` and `b[j:]`."

### Sweep

Result key: ok = named mistake first fails test N, or a true description; fixed = rewritten (new text in the hand-back).

| File | Widget | Key | Result | Basis (runs) |
|---|---|---|---|---|
| homework-1 | items[5] best_trade | test-3 | fixed | Best started at the first pair or at -inf first fails 3 (returns -1). Selling before buying (max - min, abs pairs) first fails test 2, so that sentence went. |
| homework-1 | items[5] | test-4 | ok | `low = prices[0]`: IndexError on test 4, 1 to 3 pass. |
| homework-1 | items[5] | test-7 | fixed | Using the later low against the earlier high first fails test 2 (`[3, 8, 1, 4]` has the same shape); no natural mistake found that first fails 7 (falsy-low and min-before-max both pass all). Now a description: 9 - 1 = 8, 5 - 0 = 5. |
| homework-1 | items[5] | test-8 | ok | Pair loop: tests 1 to 7 pass, test 8 times out (about 2 x 10^10 pairs). |
| homework-1 | items[6] copies_fixed | test-4, 5, 6 | ok | Descriptions; values from the simulation (0; 10; 1 + 2 + 3 + 4 = 10). `k = n // step - 1` formula first fails test 5. |
| homework-2 | items[0] flatten | test-1 | ok | Appending the sublist first fails 1. |
| homework-2 | items[0] | test-3 | ok | Description; a version keeping a nested empty list first fails 3. |
| homework-2 | items[5] sort_count | test-1 | fixed | Adding 1 instead of `len(a) - i` passes test 1 (3 either way) and first fails test 4. Forgetting the halves' counts first fails 1; the line now names both. |
| homework-2 | items[5] | test-5 | ok | `<` in the merge, and pairs with `>=`, first fail 5. |
| homework-2 | items[5] | test-7 | ok | Pair counting passes test 6 (4.5 million pairs) in Pyodide and times out on 7. |
| homework-2 | items[6] total_value | test-1 | fixed | Old "including the sub-funds' own" names leaves-only, which passes test 1 (the sub-funds hold 0.0) and first fails 4. Top-level-only and not pushing grandchildren first fail 1 (miss 120.5 - 30.25 = 90.25). |
| homework-2 | items[6] | test-4 | fixed | Recursion: RecursionError on 4. Leaves-only also first fails 4 (returns 1.0); the line now covers it. |
| homework-2 | items[9] split_feed | test-1, 2, 12 | ok | Greedy longest and first-success first fail 1; base case `[]` for an empty feed first fails 2; `listed.sort()` first fails 12. |
| homework-2 | items[9] | test-3 | ok | Description (no ticker ends in X). |
| homework-2 | items[9] | test-4 | fixed | "Not just the longest": greedy longest first fails test 1. Now a description. |
| homework-2 | items[9] | test-5 | fixed (wording) | List as given first fails 5. Old "finds each split that uses `BT` more than once" also reads as "splits using BT twice"; `B T BT` uses it once and is found twice. |
| homework-2 | items[9] | test-6 | fixed | Stopping when the rest is a ticker first fails test 5 (loses `B T B T`). Now a description. |
| homework-2 | items[9] | test-7 | fixed | A cut that cannot reach `len(feed)` first fails test 1 (or 2 with a whole-feed base). Now a description. |
| homework-2 | items[9] | test-8 | fixed | De-duplicating splits as sets first fails test 5. Now a description. |
| homework-2 | items[9] | test-9, 10, 11 | ok | Descriptions; 927 is the tribonacci count for 12; the solution returns 4,374. |
| homework-3 | items[4] min_capacity | test-6 | fixed | `lo = 1`, `lo = min`, `lo = sum // days` all first fail test 3 (answer 3 = the largest order there too). Now a description. |
| homework-3 | items[4] | test-8 | ok | Linear scan from `max(sizes)` times out on 8. |
| homework-3 | items[5] merge_k | test-2, 7 | ok | `lists[0]` and `reduce` without a start fail 2; `sorted` fails 7. |
| homework-3 | items[5] | test-6 | ok | Growing result: 4.46 s in CPython, 6.6 s in Pyodide, over 5 s. Margin is narrow on a fast machine. |
| homework-3 | items[6] kth_largest | test-2, 7, 8, 10 | ok | Ignoring k and the off-by-one target fail 2; in place fails 7; first pivot, recursive, RecursionError on 8; `sorted` fails 10. |
| homework-3 | items[8] find_trade | test-1, 2, 4, 5, 8, 13 | ok | Sorted position and plain search fail 1; reading `ring[0]` fails 2; returning `lo` unchecked fails 4; `<` in the order test fails 5; excluding `ring[hi]` fails 8; `index`/`in` and a linear scan fail 13. Solution reads at most 90 slots a search. |
| homework-3 | items[8] | test-9 | ok | Comparing with `ring[0]` strictly first fails 9 (strict `ring[lo]` fails 1; the line names both ends). |
| homework-3 | items[8] | test-3, 6, 10, 11, 12, 14 | ok | Descriptions, true of the data. |
| homework-3 | items[8] | test-7 | fixed | "Keep looking while `lo <= hi`": `while lo < hi` first fails test 1; with a final check it passes all. Now a description. |
| l1-counting-work | screens[8] count_pairs | test-3 | fixed | Inner loop from `i` first fails test 1 (5, not 3). Now a description. |
| l1-counting-work | screens[8] | test-4 | fixed | Both orders first fails 1 (6). Comparing values `a < b` and de-duplicating with `set` first fail 4; the line now names them. |
| l1-counting-work | screens[8] | test-5 | fixed | `>=` first fails test 1 (3 x 5 = 15 there too: 4, not 3). Now a description. |
| l2-big-o | screens[8] | test-4, 6, 10 | ok | Always "A" fails 4; no tie branch fails 6; a ratio raises ZeroDivisionError on 10. |
| l3-memory | screens[3] stream_mean | test-1, 3, 7 | ok | `len(ticks)` fails 1; dividing by 0 fails 3; `list(ticks)` fails 7. |
| l3-memory | screens[5] prefix_sums | test-1, 4 | ok | Description; `pre[j - 1]` first fails 4. |
| l3-memory | screens[5] | test-2 | fixed | No leading 0 first fails test 1. Now a description; `[0, prices[0]]` first fails 2. |
| l4-cheap-on-average | screens[6] | test-2, 3, 10 | ok | Resizing when the array fills gives 1 and first fails 2; adding the new one fails 3; test 10 a description (1 + 2 + ... + 1,024 = 2,047). |
| l5-calls-itself | screens[5] | test-1, 2, 7 | ok | Missing `return` fails 1; base case at one value fails 2; `power` base at `n == 1` recurses past 0 on 7. |
| l5-calls-itself | screens[9] | test-1, 2 | ok | Skipping dicts and one level fail 1 (smaller totals); test 2 a description. |
| l6-call-stack | screens[6] | test-3, 10 | ok | Recursive `sum_to` fails 3; ignoring `d` fails 10. |
| l6-call-stack | screens[6] | test-9 | fixed | Sum of branches and call counts first fail test 7 (`depth(2)` is 4 or 3). Now a description. |
| l6-call-stack | screens[9] | test-1 | ok | Sum fails 1; count first fails 4 but the line's max/sum/count advice is still right. |
| l6-call-stack | screens[9] | test-2 | fixed | Returning 0 for a leaf first fails 1 (gives 3). Now a description. |
| l7-split-in-half | screens[5] | test-5, 10 | ok | One at a time: RecursionError on 5. Two calls per level: tests 6 to 9 pass, 10 times out. |
| l7-split-in-half | screens[5] | test-9 | fixed | The odd case without `* x` first fails test 6 (2^10 halves through 5). Now a description: 3^2 one, then two more, 3. |
| l8-cost-of-recursion | screens[5] | test-1, 6, 10 | ok | `fib_calls(0) = 0` fails 1; making the calls times out on 6; no memo times out on 10. |
| l9-halving | screens[3] | test-4, 11 | ok | `lo < hi` with a final check: IndexError on 4; linear scan fails 11. |
| l9-halving | screens[3] | test-5 | fixed | `while lo < hi` first fails test 1 (64 is never read). Now a description. |
| l9-halving | screens[5] | test-1, 4, 7 | ok | Returning on the first equal fails 1; `hi = len - 1` fails 4; 7 a description. |
| l9-halving | screens[9] | test-2, 4, 6 | ok | `bisect_right` fails 2; no `None` fails 4; checking `days[-1]` fails 6. |
| l10-search-the-answer | screens[3] | test-3, 4, 9 | ok | Range one short fails 3; unchecked `a` fails 4; `pred(a)` before the range check fails 9. |
| l10-search-the-answer | screens[4] | test-2 | ok | Range ending at `n`: TypeError on 2. |
| l10-search-the-answer | screens[5] | test-1, 8 | ok | Updates the wrong way fail 1; no range check fails 8 (4 x 5 + 100 = 120). |
| l11-sorting-by-hand | screens[3] | test-4 | fixed | No early stop first fails test 1 (15, not 12). Now a description. |
| l11-sorting-by-hand | screens[3] | test-6, 8 | ok | `>=` fails 6; in place fails 8. |
| l11-sorting-by-hand | screens[8] | test-1, 4 | ok | `>=` on times fails 1; whole tuples pass 1 and fail 4. |
| l12-merge-sort | screens[2] | test-2, 9 | ok | One leftover appended fails 2; recursive merge (RecursionError) and `out = out + [x]` (over 5 s) fail 9. |
| l12-merge-sort | screens[3] | test-7 | fixed | One value at a time gives RecursionError at 20,000 deep, not a time-out. |
| l12-merge-sort | screens[7] | test-8, 9 | ok | `<` fails 8; pairs time out on 9. |
| l12-merge-sort | screens[8] | test-2, 3 | fixed | Whole tuples, `<` on times and dropping `b`'s tail all first fail test 1; dropping `a`'s tail first fails 4. Both now descriptions. |
| l13-quicksort | screens[3] | test-1 | fixed | `j` to `hi` inclusive with `return i - 1` passes all; a missing final swap first fails 1, which the old line did not name. |
| l13-quicksort | screens[3] | test-2 | ok | `i` from 0 fails 2. |
| l13-quicksort | screens[3] | test-3 | fixed | A missing final swap first fails test 1. Now a description. |
| l13-quicksort | screens[4] | test-2, 7 | ok | Returning the list fails 2; end pivot: RecursionError on 7. |
| l13-quicksort | screens[8] | test-9 | ok | `sorted` fails 9. |
| l14-best-step-now | screens[3] | test-3, 4, 5 | ok | `reversed(coins)` fails 3; `[]` treated as no answer fails 4; no `None` check fails 5. |
| l14-best-step-now | screens[5] | test-1 | fixed | By start gives 1 on test 1. `s > end` also first fails test 1, with 3; a sentence now names it. |
| l14-best-step-now | screens[5] | test-2 | ok | Description. |
| l14-best-step-now | screens[5] | test-4 | fixed | `>` first fails test 1. Now a description. |
| review-3 | items[4] | test-1 | ok | No de-duplication fails 1. |
| review-3 | items[4] | test-2 | fixed | Dropping `b`'s tail or both tails first fails test 1. Now a description. |
| review-3 | items[6] | test-1, 7 | ok | `bisect_left` for `high` fails 1; a negative count fails 7. |
| review-3 | items[7] | test-3, 4 | ok | `None - 1` fails 3; returning -1 fails 4. |

Totals: 127 lines on 41 widgets checked; 31 rewritten (the 2 named, 29 from the sweep); 96 unchanged. Where no natural mistake first fails test N, the new line describes test N and names no cause, as the brief asks.

Outside the byKey lines (not edited): `l6-call-stack.json` `screens[6].widget.how` says `sum_to(100000)` is "far deeper than the limit of 1,000"; the page's limit is 3,000 (true either way for 100,000).

Gates: validator 0 errors (manifest unchanged); `algo-think-L1-3-concepts.py` and `algo-think-L1-3-r2-concepts.py` exit 0; voice scan 35 on the course 0 over 35 words, 0 explanations over three sentences; playthroughs of the 13 edited files, desktop and `--mobile`: all 26 runs "All passed".

## Fix-pass read (follow-up sweep)

Blind read of `git diff 11df1919~1 11df1919 -- app/content/courses/algo-think/` (13 files, 31 `feedback.byKey.test-N` lines) plus one row outside the diff (`l6-call-stack.json` `screens[6].widget.how`). Method: every item's solution and starter were run against the item's own tests under CPython with `sys.setrecursionlimit(3000)` (all 19 solutions pass, all starters fail test 1, slowest solution test 0.03 s). For each line, the stated facts were recomputed, each named mistake was written as a submission and its first failing test recorded, and each named remedy was run. An exception raised inside a test gets key `test-N`, not `error` (`app/js/engine/widgets/code.js` line 576: `error` is for load errors and crashes only), so the `RecursionError` lines are reachable.

Rows: 32. Verdicts: 31 `correct`, 1 `imprecise` (minor), 0 `wrong`, 0 `misleading`, 0 `unverified`.

| # | File | JSON path | New text (short) | Verdict | Basis (run or derivation) |
|---|---|---|---|---|---|
| 1 | homework-1.json | items[5].feedback.byKey.test-3 | expects 0 when prices only fall; start the best profit at 0 | correct | `[5, 4, 3, 2]` gives 0. Submission with best starting unset passes 1 to 2, fails 3 with -1; same code with best = 0 passes all 8. |
| 2 | homework-1.json | items[5].feedback.byKey.test-7 | `[1, 9, 0, 5]` expects 8; buying at the later low of 0 makes only 5 | correct | 9 - 1 = 8, 5 - 0 = 5. See observation B. |
| 3 | homework-2.json | items[5].feedback.byKey.test-1 | expects `([1, 2, 3, 4], 3)`; add both halves' counts, and `len(a) - i` on taking `b[j]` | correct | Omitting the halves' counts gives a count of 1 at test 1. Both remedies together pass all 8. (Adding 1 in place of `len(a) - i` still passes test 1 and fails test 4; the clause is a true remedy, not a false claim.) |
| 4 | homework-2.json | items[6].feedback.byKey.test-4 | chain of 5,000 funds worth £1 each, expects £5,000; recursion runs out of frames; count every fund | correct | Setup builds 5,000 nodes of 1.0 (counted). Two recursive submissions pass 1 to 3 and raise `RecursionError` at 4 (5,000 is past 3,000 and past 1,000). A loop that skips single-child nodes' values passes 1 to 3 and returns 1.0 at 4, so "not only the last" is reachable. |
| 5 | homework-2.json | items[6].feedback.byKey.test-1 | expects £340.25, £90.25 of it two levels down; push each node's children | correct | 120.5 - 30.25 = 90.25; 250 + 90.25 = 340.25. Root-children-only submission returns 250.0 at test 1. |
| 6 | homework-2.json | items[9].feedback.byKey.test-4 | `IAGS` fits but leaves `SE`, no split; only `IAG SSE` | correct | `split_feed('SE', ...)` is `[]`; full answer `[['IAG', 'SSE']]`. |
| 7 | homework-2.json | items[9].feedback.byKey.test-5 | `BT` listed twice, four different splits; list as given finds each split with `BT` more than once; use a set | correct | List-as-given submission passes 1 to 4, fails 5. Counts: `BT BT` 4 times, `BT B T` twice, `B T BT` twice, `B T B T` once. Set version is the solution. |
| 8 | homework-2.json | items[9].feedback.byKey.test-6 | `BABA` and `BA BA` are both splits | correct | Solution returns `[['BA', 'BA'], ['BABA']]`. |
| 9 | homework-2.json | items[9].feedback.byKey.test-7 | one ticker `RIO`, one split | correct | Solution returns `[['RIO']]`. |
| 10 | homework-2.json | items[9].feedback.byKey.test-8 | three splits: `A A A`, `A AA`, `AA A` | correct | Solution returns exactly these three. |
| 11 | homework-3.json | items[4].feedback.byKey.test-6 | one day per order, capacity is the largest order, 10 | correct | 5 orders, 5 days, max of `[7, 2, 5, 10, 8]` is 10; solution returns 10. |
| 12 | homework-3.json | items[8].feedback.byKey.test-7 | `[7]` searched for 7 then 6, expects `[0, -1]` | correct | Matches the test and the solution. |
| 13 | l1-counting-work.json | screens[8].feedback.byKey.test-3 | expects 0 for one price: a pair needs two different positions | correct | `count_pairs([7], 0)` is 0; no mistake named. |
| 14 | l1-counting-work.json | screens[8].feedback.byKey.test-4 | `[2, 2, 2]` expects 3; pair positions, not values, keep repeats | correct | Two submissions (prices made a set; pairing values `a < b`) pass 1 to 3 and return 0 at 4. Position pairs `i < j` give 3. |
| 15 | l1-counting-work.json | screens[8].feedback.byKey.test-5 | 5 × 3 equals 15, only a product above 15 counts | correct | 15 > 15 is false; expects 0. |
| 16 | l11-sorting-by-hand.json | screens[3].feedback.byKey.test-4 | sorted input, 4 comparisons: one per new value | correct | Solution returns `([1, 2, 3, 4, 5], 4)`: 4 insertions, one comparison each. |
| 17 | l12-merge-sort.json | screens[2].feedback.byKey.test-6 | leaves 5 in `a`; kept the tail of `b`, dropped the tail of `a`; extend with both | correct | True whenever test 6 is the first failure (tests 1, 2, 5 need `b`'s tail). A submission that drops `a`'s tail but returns `a` when `b` is empty passes 1 to 5 and gives `[1, 2, 3, 4]` at 6. Both `extend` calls pass all 9. See observation A. |
| 18 | l12-merge-sort.json | screens[3].feedback.byKey.test-7 | 20,000 values; one-at-a-time split nests 20,000 calls, past the limit | correct | Two one-at-a-time submissions pass 1 to 6 and raise `RecursionError` at 7. Middle split is the solution (depth about 15). |
| 19 | l12-merge-sort.json | screens[8].feedback.byKey.test-2 | logs swapped; at 09:00:03 the CXE trade, now in the first log, comes first | correct | Expected slice is CXE then LSE. Submissions that put LSE first on a tie pass 1 and fail 2. |
| 20 | l12-merge-sort.json | screens[8].feedback.byKey.test-3 | empty first log, answer is the second log as it stands | correct | Expected value equals the second argument. |
| 21 | l13-quicksort.json | screens[3].feedback.byKey.test-3 | expects `(0, [1, 2])`; no value is at most the pivot 1, `i` stays at `lo`, final swap moves 1 there | correct | `[2, 1]`: `xs[0]` is 2, above 1, so `i = 0`; the swap gives `[1, 2]`, return 0. |
| 22 | l13-quicksort.json | screens[3].feedback.byKey.test-1 | expects `(3, [2, 4, 1, 5, 9, 8, 7])`; walk `j` to `hi - 1`, swap pivot into `i`, return `i` | correct | The remedy is the solution; passes all 8. Walking `j` to `hi` with the final swap gives index 4 at test 1. |
| 23 | l13-quicksort.json | screens[8].feedback.byKey.test-7 | 3,000 sorted values; fixed end pivot with both sides recursed nests about 3,000 calls; keep one side, random pivot | correct | Full quicksort with fixed end pivot (two guard styles) passes 1 to 6 and raises `RecursionError` at 7 under limit 3,000. One side kept with a random pivot passes all 9. Also true under the standard limit of 1,000. |
| 24 | l14-best-step-now.json | screens[5].feedback.byKey.test-1 | got 1: sorted by start; got 3: touching meeting refused, use `>=` | correct | Sort by start returns 1; sort by end with `>` returns 3 (keeps B, D, F); `>=` returns 4. |
| 25 | l14-best-step-now.json | screens[5].feedback.byKey.test-4 | three touching meetings, expects 3 | correct | `(9, 10), (10, 11), (11, 12)` gives 3. |
| 26 | l3-memory.json | screens[5].feedback.byKey.test-2 | `[0]` for no prices: the leading 0 is always there | correct | Submission returning `[]` for an empty list passes 1 and fails 2. |
| 27 | l6-call-stack.json | screens[6].feedback.byKey.test-9 | `depth(15)` is 15: chain `fib(15)` down to `fib(1)` | correct | 15, 14, ..., 1 is 15 frames; solution returns 15. |
| 28 | l6-call-stack.json | screens[9].feedback.byKey.test-2 | lone position is one level, counting both ends | correct | Solution returns 1; matches the question's wording. |
| 29 | l7-split-in-half.json | screens[5].feedback.byKey.test-9 | `(243, 3)`: 3² takes one multiplication, 3⁵ = 3² × 3² × 3 takes two more | correct | `power_fast(3, 2)` is `(9, 1)`; 9 × 9 × 3 = 243 with 1 + 2 = 3. |
| 30 | l9-halving.json | screens[3].feedback.byKey.test-5 | `[7]` searched for 7, expect index 0 | correct | Matches the test and the solution. |
| 31 | review-3.json | items[4].feedback.byKey.test-2 | empty first list, every id from the second: `[3, 5]` | correct | Matches the test and the solution. |
| 32 | l6-call-stack.json | screens[6].widget.how (outside the diff) | Test 3 is `sum_to(100000)`, far deeper than the limit of 1,000 | imprecise | 1,000 is standard Python's default and the lesson's figure (`screens[3]`), but the page sets 3,000 (`drill-worker.js`, `RECURSION_LIMIT`). The point holds under both: a recursive `sum_to` passes tests 1 to 2 and raises `RecursionError` at test 3 with the limit at 1,000 and at 3,000. Only the figure is untrue of the page. |

### Findings

1. l6-call-stack.json | `screens[6].widget.how` | imprecise, minor | "the limit of 1,000" names a figure that is not the limit in force on the page (3,000). | Run: recursive `sum_to(100000)` raises `RecursionError` at limit 1,000 and at limit 3,000; the loop returns 5000050000. | Replace the whole `how` with text true of both:

   ```
   Check runs 10 hidden tests. Test 3 is `sum_to(100000)`: as a recursion it would need about 100,000 frames, far past Python's recursion limit. Test 10 starts the count at `d = 10`.
   ```

### Observations (no verdict change, no fix required)

A. l12-merge-sort.json `screens[2]`: the plain form of the mistake named in `test-6` (extend with `b[j:]` only) fails test 3 first, with `[]` for `merge([1, 2], [])`. Test 3 has no `byKey` line, so that learner sees the generic line. Optional addition, mirroring the existing `test-2` line, verified by that run:

   ```
   "test-3": "Test 3 has an empty `b`. The loop never runs, so everything comes from the tail of `a`."
   ```

B. homework-1.json `items[5]`: the mistake that `test-7` points at (buy at the lowest price of the day) fails test 2 first, returning 3 for `[3, 8, 1, 4]`; test 2 has no `byKey` line. The `test-7` line itself is true. Optional addition (8 - 3 = 5, 4 - 1 = 3):

   ```
   "test-2": "Test 2 expects 5 for `[3, 8, 1, 4]`: buy at 3 and sell at 8. Buying at the later low of 1 makes only 3."
   ```

C. Not judged here (outside the diff and the extra row): `l6-call-stack.json` `screens[3]` says `sys.getrecursionlimit()` returns 1000, which is standard Python's value, not the page's.

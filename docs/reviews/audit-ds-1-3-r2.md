# Concept audit, round 2 (blind): ds L1 to L3

Auditor: Fable, 13 Nov 2026. Scope: `app/content/courses/ds/` lessons l1 to l13, review-1 to review-3, homework-1 to homework-3 (Stage 1, topic 1.8, full ledger depth). Read blind: no earlier review, audit, fix pass, report or concepts script of this course was opened before the ledger and the findings below were committed.

- Ledger: `docs/reports/audit-ds-1-3-r2-ledger.md`, 285 rows: 267 correct, 1 wrong, 14 imprecise, 1 misleading, 2 unverified.
- Script: `docs/reports/ds-L1-3-r2-concepts.py` (CPython 3.13.18; Pyodide 0.27.7 values read with node). 180 checks. 168 pass. 12 fail, each tied to a finding below (1 to 12), so the script exits 1 until those are fixed.

## Summary

The course is in good order. Every graded key was recomputed and is right. All 32 code widgets pass their hidden tests with the solution and fail with the starter, in CPython 3.13 and under the local Pyodide 0.27.7 build (`docs/reports/ds-L1-3-r2-pyodide-widgets.mjs`). The complexity claims hold: hash lookups were counted on spread and on colliding keys, appends on CPython's real growth pattern, and `pop(0)`, `insert(0, x)`, `popleft()` and deque indexing were timed.

There is one `wrong`, in a slip feedback line, and it is minor. The other twelve findings are wording that is true only under a premise the screen does not state. None is serious.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l7-prefix-sums.json` | `screens[6].feedback.byKey.four` | **wrong**, minor | The slip value is 4 and the line says "You forgot one of the runs of two days: `xs[0:2]` and `xs[1:3]`." Forgetting one run of two leaves 5, not 4. | `[0, 0, 0]` with `k = 0` has 3 single days, 2 pairs and 1 whole list: 6. A count of 4 misses two runs (script B, "slip four"). | Replace with: "You missed two runs. There are three single days, two pairs (`xs[0:2]` and `xs[1:3]`) and the whole list."

2. `l1-arrays-in-memory.json` | `screens[6].prose` (also `widget.accept`, hints, `explain.text` "a quarter of the memory") | **imprecise**, minor | "A Python list stores pointers, 8 bytes each" and "a separate 24-byte object" are stated as facts about Python. They are facts about a 64-bit build. | `sys.getsizeof(1.0)` is 24 on 64-bit CPython. The app's own Python is Pyodide 0.27.7 on wasm32: `struct.calcsize('P')` is 4 and `sys.getsizeof(1.0)` is 16 (run with node from the local Pyodide build). There the list costs 20 MB against NumPy's 8 MB, not 32 against 8. A learner who checks in the app's editor sees 16. | Replace the first prose sentence with: "On a 64-bit computer, a Python list stores pointers, 8 bytes each, side by side." Keep the rest. Optional extra sentence: "The Python inside this app is a 32-bit build, where the sizes are 4 and 16 bytes."

3. `l1-arrays-in-memory.json` | `screens[10].widget.options[2].why` | **imprecise**, minor | "Slicing copies 19 closes into a new list, then adds one: still about 20 copies per tick." `+` does not add one in place. It builds a third list. | `window[1:]` copies 19 pointers; `+ [close]` allocates a new list and copies 19 + 1 into it: 39 copies (list concatenation always builds a new list; Python docs, "Common sequence operations"). | Replace with: "Slicing copies 19 closes into a new list, and `+` copies all 20 into another: about 40 copies per tick."

4. `l3-two-sum.json` | `screens[0].explain.text` | **imprecise**, minor | "Only 5 finds its partner, 12, in the list." 12 finds its partner, 5, too. | Complements for 17: 3 → 14, 8 → 9, 5 → 12, 12 → 5, 6 → 11. Two prices find a partner (script B). | Replace the second sentence with: "Only 5 and 12 find their partners in the list: each other."

5. `l5-both-ends.json` | `screens[5].prose` | **imprecise**, minor | "We have reached `i` on 4 and `j` on 8." The correct walk for target 10 never stands there. | The walk is (1, 15), (1, 11), (1, 8), (3, 8), (3, 6), (4, 6) (script B). The state (4, 8) is screen 1's mistake state `m3`. The lesson of the screen is sound from that state; only "we have reached" is untrue. | Replace the second sentence with: "Suppose a walk stands with `i` on 4 and `j` on 8: the sum is 12, too big."

6. `l6-sliding-window.json` | `summary.formula.note` | **imprecise**, minor | "Shrinking a window on a sum is safe only when every number is positive." Zeros are safe as well. | With no negative number, dropping the left item cannot raise the sum, so the argument of screens 3 and 4 holds. The shrinking window matched brute force on 400 random lists with zeros (script E). Homework-2 item 6 already says "never negative". | Replace with: "Shrinking a window on a sum is safe only when no number is negative."

7. `l8-best-day.json` | `screens[6].explain.text` (third sentence); `homework-2.json` | `items[2].prose` (first sentence) | **imprecise**, minor | "On daily returns, the same loop finds the best stretch of a strategy." Kadane adds. Simple returns compound, so their sum is not the return of the stretch. | Simple returns +50%, −40%, +50%: the largest sum is the whole run (0.6), which compounds to +35%. The best compounded stretch is one day, +50% (script E). Log returns and daily P&L do add (Tsay, *Analysis of Financial Time Series*, 1.1). Lesson 6 screen 9 already says "daily log returns". | l8: "On daily log returns, or daily P&L, the same loop finds the best stretch of a strategy." homework-2: "The best stretch of a strategy's daily P&L is the maximum subarray."

8. `l10-next-greater.json` | `screens[2].explain.text` (third sentence); `summary.ideas[1]` (first sentence) | **imprecise**, minor | "The waiting values always fall from bottom to top." Under the lesson's own convention ties wait, so equal values sit together on the stack. | `[5, 5, 4]` leaves 5, 5, 4 waiting (script B). The stack is non-increasing, not decreasing; homework-3 item 7's model answer already says "never rise". | explain: "The waiting values never rise from bottom to top, so this is called a **monotonic stack**." summary: "The waiting values never rise from bottom to top: a monotonic stack."

9. `l10-next-greater.json` | `screens[7].explain.text` (third sentence) | **imprecise**, minor | "200,000 values take about 400,000 stack operations." 2n is the upper bound, not the usual count. | The widget's own 200,000-value test is a falling list: 200,000 pushes and no pops (script C). | Replace with: "200,000 values take at most 400,000 stack operations."

10. `l12-nodes-and-pointers.json` | `screens[0].explain.text` (second sentence); `summary.ideas[0]` | **imprecise**, minor | "Reading the $k$-th value takes $k$ steps." Quiz 0 grades 4,999 steps for the 5,000th close and marks 5,000 as a slip ("You counted nodes, not steps"). | From `head`, the $k$-th node is $k - 1$ `next` steps away, and $k$ nodes are visited. The lesson and its quiz use "steps" in two ways. | explain: "Reading the $k$-th value means visiting $k$ nodes, so there is no $O(1)$ indexing." summary: "A linked list is nodes joined by `next` pointers. There is no indexing: reaching the $k$-th node takes $k - 1$ steps from the head."

11. `l2-constant-time-lookup.json` | `screens[6].feedback.correct`; `summary.ideas[2]` (first sentence) | **imprecise**, minor | "Strings, numbers and tuples are keys." A tuple is hashable only if everything in it is. | `{(1, [2]): 0}` raises `TypeError: unhashable type: 'list'` (script D). The screen's explain already says "tuples of them". | feedback: "Strings, numbers and tuples of them are keys; lists and dicts are not." summary: "Keys must be hashable: strings, numbers and tuples of them, not lists or dicts."

12. `l4-frequencies.json` | `screens[6].widget.options[3].why` | **misleading**, minor | `all(a.count(c) == b.count(c) for c in a)` is called only slow. The same screen labels the set check "wrong", so silence here reads as "correct but slow". It is wrong too. | The check never looks at letters that are only in `b`: it returns `True` for `'ab'` and `'abc'` (script D). | Replace with: "Each `.count` scans a whole string, so this is $O(n^2)$. It is wrong too: `ab` and `abc` pass, because letters only in `b` are never checked."

13. `l3-two-sum.json` | `screens[6].prose` (last line) | **imprecise**, minor | "One pass of $O(1)$ dict steps: $O(n)$ time." The $O(1)$ is an average. Lesson 2 says so; lesson 3 and the later lessons (l4 `screens[1].explain`, l4 `summary.ideas[0]`, l6 `screens[5].explain`) state it bare. | CLRS Theorems 11.1 and 11.2: expected $\Theta(1 + \alpha)$, worst case $\Theta(n)$ per lookup. Script C counts both cases. One reminder on the pattern screen is enough. | Replace the line with: "One pass of dict steps, each $O(1)$ on average: $O(n)$ time, $O(n)$ extra memory."

### Unverified remarks (not counted as findings by severity)

- `l8-best-day.json` | `screens[9].explain.text` | "often via a misaligned index" is an unsourced remark about how backtests go wrong. Suggested: "To beat it, a backtest must sell before buying, for example through a misaligned index, or fill at other prices."
- `l13-fast-and-slow.json` | `screens[1].explain.text` | "in an interview it is a fine first answer" is an opinion about interviews. Suggested: "It is correct, and a sound first answer."

## Counts

| severity | serious | minor |
|---|---|---|
| wrong | 0 | 1 |
| imprecise | 0 | 11 |
| misleading | 0 | 1 |

## Gates

- Validator (`node tools/validate.mjs`, from `app/`): 0 errors, 4531 warnings; `content/manifest.json` unchanged.
- `node tools/grade-all.mjs --file <path> --local-cdn <pkgs>`: 0 failures, exit 0, on review-1 to review-3, homework-1 to homework-3 and all 13 lesson files. It grades numeric, choice and multi widgets only, so the code widgets were run separately.
- `docs/reports/ds-L1-3-r2-pyodide-widgets.mjs` (node, Pyodide 0.27.7): 32 widgets, 0 problems, exit 0. Slowest hidden test 0.17 s.
- `docs/reports/ds-L1-3-r2-concepts.py`: exit 1, 168 of 180 checks pass; the 12 failures are findings 1 to 12.
- Number scripts: none exists for ds levels 1 to 3. The round 1 script `docs/reports/ds-L1-3-concepts.py`, run after the blind commit: exit 0 (167 checks).

## Overlap with earlier reads

Opened only after the blind commit `1481fb73`: `docs/reviews/review-1.8.md` (ds L1 to L3 lines), `docs/reviews/audit-ds-1-3.md` (round 1 audit, its fix pass and its fix-pass read).

| Conceptual findings, ds L1 to L3 | Count |
|---|---|
| Found by this audit only | 13 (findings 1 to 13) |
| Found by earlier reads only | 21 (review 1.8: 3; round 1 audit: 18; fix-pass read: 0) |
| Found by both | 0 |

All 21 earlier findings were fixed before this read, so none could be found again. This audit read each fixed text as it now stands, and every one holds (the ledger rows for those paths are `correct`), with one reservation below.

New `wrong` findings that no earlier read found: **1** (finding 1, minor, a slip feedback line). That is within the convergence limit of one per three levels, subject to the fix-pass read of this round.

Notes on the comparison.

- Round 1 found nine `wrong` and this round one. The one left is of a class round 1 met twice (its findings 7 and 8, slip value against feedback). It is now seen three times in this course, so by SESSION PROTOCOL 6 it should become a validator rule; an inbox bullet asks for it.
- Finding 13 differs from a round 1 judgement. Round 1's "checks that found nothing" accepted that hash costs are "on average where first stated". This audit asks for one more reminder on the l3 pattern screen, because l3 to l6 state $O(1)$ bare on five screens. It is minor either way.
- One reservation on the round 1 fix pass. Its text for l8 `screens[9].explain.text` says a backtest beats the bound "often via a misaligned index". The fix-pass read marked the sentence correct. The bound and the two routes past it are right; "often" is an unsourced frequency, so this audit lists it as unverified.
- Findings 2, 3, 4, 5, 6, 8, 9, 10, 11 and 12 are on sentences that all three earlier reads passed. Finding 2 needed a run in the app's own interpreter, which no earlier read made.

## Limits of this audit

- Sources named in the ledger without a run (CLRS, Knuth, Harris, Hull, Tsay, Bacon, the CPython and pandas sources) were cited from memory of the named section and were not reopened here.
- Timing checks ran in native CPython 3.13 only. Pyodide ran the code widgets for correctness, not against the 5 s limit.
- The ledger groups hint and feedback lines that restate one computation into one row (285 rows for 19 files). Every line was read; a row's verdict covers each key it names.
- Author, earlier readers and this auditor are the same model family, so a shared misconception can survive all four reads.

## Fix pass

Fixer: Opus, 13 Nov 2026. Content strings only; no lesson id, key, tolerance or `wrong[]` value changed.

1. `l7` `screens[6].feedback.byKey.four` | **fixed differently** | Slip 4 is kept; the line now names the mistake that gives it: "You counted the three single days and the whole list, but missed the two pairs, `xs[0:2]` and `xs[1:3]`." Basis: 3 singles + 1 whole = 4, and 6 − 2 pairs = 4 (brute force on `[0, 0, 0]`, `k = 0`, gives 6). No collision with key 6 or slips 3 and 1. The other two lines hold: singles alone give 3, the whole list alone gives 1.
2. `l1` `screens[6]` | **fixed** (extended) | Measured under node in the local Pyodide 0.27.7: `struct.calcsize('P')` 4, `sys.getsizeof(1.0)` 16, NumPy float64 `itemsize` 8, `sys.maxsize` 2³¹ − 1; CPython 3.13 here: 8 and 24. Prose, question, point hint, explain and caption now say "64-bit"; the prose adds "This app's Python is a 32-bit build: there a pointer is 4 bytes and a float object 16." Key 32 is right for the question as now posed (64-bit), which asks for a computation, not a run, so it is unchanged. The byKey lines (8 MB pointers alone, 24 MB objects alone) hold under that premise. Check updated to test the stated premise and the app sizes.
3. `l1` `screens[10].widget.options[2].why` | **fixed** | `window[1:]` builds a 19-item list, then `+` builds a new 20-item list (concatenation never works in place): 39, about 40 copies.
4. `l3` `screens[0].explain.text` | **fixed** | Complements for 17 of 3, 8, 5, 12, 6 are 14, 9, 12, 5, 11; only 12 and 5 are in the list.
5. `l5` `screens[5].prose` | **fixed** | Walked `[1, 3, 4, 6, 8, 11, 15]` for 10: (1, 15), (1, 11), (1, 8), (3, 8), (3, 6), (4, 6). (4, 8) is never reached, so it is now a supposition. The hints and explain hold from that state.
6. `l6` `summary.formula.note` | **fixed** | With no negative item, dropping the left item cannot raise the sum, so shrinking never skips a shorter qualifying window; the script's brute-force run on lists with zeros agrees.
7. `l8` `screens[6].explain.text`; `homework-2` `items[2].prose` | **fixed** | Kadane maximises a sum. Log returns and £ P&L add; simple returns compound. +50%, −40%, +50%: best sum is the whole run (0.6, compounding to +35%), best compounded stretch is one day (+50%), which log returns also pick. Homework tests and feedback are unaffected.
8. `l10` `screens[2].explain.text`; `summary.ideas[1]` | **fixed** | With `<`, ties wait: `[5, 5, 4]` leaves 5, 5, 4 on the stack, non-increasing.
9. `l10` `screens[7].explain.text` | **fixed** | Each index is pushed once and popped at most once: at most 2n. The 200,000 falling test makes 200,000 pushes and no pops. While here: `test-6` (`<=` passes tests 1 to 5, which have no ties, and fails `[5, 5, 6]`) and `test-10` (nested scan passes 1 to 9, times out on 10) both hold.
10. `l12` `screens[0].explain.text`; `summary.ideas[0]` | **fixed** | From `head`, the k-th node is k − 1 `next` moves away and k nodes are visited (screen 0: 9 is the third node, three nodes tapped; quiz 0: 4,999 steps).
11. `l2` `screens[6].feedback.correct`; `summary.ideas[2]` | **fixed** | `{(1, [2]): 0}` raises `TypeError: unhashable type: 'list'`; a tuple is hashable only if its items are.
12. `l4` `screens[6].widget.options[3].why` | **fixed** | `all(a.count(c) == b.count(c) for c in 'ab')` is `True` for `b = 'abc'`; each of n `.count` calls scans n characters, O(n²). Explanation is two sentences.
13. `l3` `screens[6].prose` | **fixed** | Dict lookup is O(1) expected under uniform hashing, Θ(n) worst case (CLRS ch. 11); lesson 2 states "on average".

Unverified remarks:
- `l8` `screens[9].explain.text` | **fixed** | "often via" replaced by "for example through": a stated possibility, not a frequency.
- `l13` `screens[1].explain.text` | **fixed differently** | The interview judgement is dropped: "It is correct and simple to write." Both halves are visible in the code shown.

Scripts: `docs/reports/ds-L1-3-r2-concepts.py` checks for findings 1 to 12 rewritten to test the corrected facts and the new wording (each still tagged with its finding); 180 of 180 pass, exit 0. `docs/reports/ds-L1-3-concepts.py` exit 0. `docs/reports/ds-L1-3-r2-pyodide-widgets.mjs`: 32 widgets, 0 problems, exit 0.

Gates: validator 0 errors (manifest unchanged); voice scan 35: 0 and 0; playthrough desktop and `--mobile` of the 12 edited files (11 lessons, homework-2): all passed.

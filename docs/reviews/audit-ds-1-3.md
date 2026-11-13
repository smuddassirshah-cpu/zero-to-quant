# Concept audit: ds levels 1 to 3 (round 1, blind)

Course `ds` (Core Data Structures, topic 1.8, Stage 1). Scope: lessons l1 to l13, review-1 to review-3 and homework-1 to homework-3, as `course.json` maps them to levels 1 to 3. Level 4 is out of scope. Read blind: `docs/reviews/review-1.8.md`, the voice file and every ds report were opened only after the ledger and the findings below were committed.

- Ledger: `docs/reports/audit-ds-1-3-ledger.md`, 250 rows: correct 229, wrong 9, imprecise 8, misleading 0, unverified 4.
- Script: `docs/reports/ds-L1-3-concepts.py` (CPython 3.13). 147 checks pass and 11 fail; each failing check is a finding below, so the script exits 1 until the fix pass. It also runs every one of the 32 Python code widgets: each solution passes its hidden tests and each starter fails.
- No C++ widgets occur in these levels.

## Findings

Severities: `wrong` 9 (serious 1, minor 8), `imprecise` 7 (serious 1, minor 6), `misleading` 0, `unverified` 2 (minor 2). Serious findings are 12 and 13.

1. `l1-arrays-in-memory.json` | `screens[4].explain.text` | wrong, minor | "The copies are $1 + 2 + 4 + 8 = 15$, always fewer than the appends." The general claim is false. | With doubling from capacity 1, 17 appends make $1 + 2 + 4 + 8 + 16 = 31$ copies, and 3 appends make 3. The true bound is fewer than twice the appends (CLRS 3rd edition, section 17.4; script checks `l1.s4 explain` and `[fix] copies`). The screen's own case, 15 for 16, is right. | Replace the first sentence with: "The copies are $1 + 2 + 4 + 8 = 15$, and with doubling they are always fewer than twice the appends." Keep the other two sentences.

2. `l1-arrays-in-memory.json` | `screens[10].widget.options[3].why` | wrong, minor | "`remove` searches for the value, then shifts the rest left: two linear steps instead of one." | `window.remove(window[0])` finds its value on the first comparison (script: one `__eq__` call), so only the shift is linear. In general a search of $k$ items plus a shift of $n - k - 1$ is one linear pass, never two. | "`remove` finds the value at index 0 on its first comparison, then shifts the rest left: the same linear cost as `pop(0)`."

3. `l5-both-ends.json` | `screens[4].feedback.byKey.c3` | wrong, minor | "2 is nearest zero, so its square is the smallest. It goes in the first slot, not the last." | In `[-7, -3, -1, 2, 4, 6]` the value nearest zero is −1, as `byKey.c2` on the same screen says. The squares in order are 1, 4, 9, 16, 36, 49, so 4 goes second (script check `l5.s4 feedback c3`). | "2 is not at an end. Its square, 4, is the second smallest, so it goes in the second slot, not the last."

4. `l5-both-ends.json` | `quiz[2].prose` | imprecise, minor | "A strangle's payoff at six strikes, from £90 to £115". | A strangle has two strikes. The six numbers are payoffs at six prices of the underlying at expiry; they match a put struck at £100 and a call struck at £105 (script check; Hull, *Options, Futures and Other Derivatives*, chapter on trading strategies, strangles). | "A strangle's payoff at six expiry prices, from £90 to £115, is `[10, 5, 0, 0, 5, 10]`. To check it is symmetric, we run the palindrome check on the list."

5. `l6-sliding-window.json` | `screens[6].prose` | wrong, minor | "This version passes `'abcbdae'`." | It does not. At the second `a` the code sets `left = last['a'] + 1 = 1`, so the window runs back over both `b`s and the function returns 6; the right answer is 5 (script check `l6.s6 prose`). The trap's graded key (3 on `'abba'`) is right. | "This version passes `'abcbd'`. Run it on `'abba'` by hand." (Checked: the buggy and the correct version both return 3 on `'abcbd'`.)

6. `l6-sliding-window.json` | `quiz[3].widget.options[3].why` | imprecise, minor | "It is just as fast, and every sum after the first is wrong." | Each step adds `xs[k - 1] - xs[k]` of error, which telescopes: after $k$ steps the sum is off by `xs[0] - xs[k]`. So a sum is right whenever `xs[k]` equals `xs[0]` (script: on `[3, 9, 3, 5, 3, 1]` with $w = 2$ two of the four later sums are right). | "It is just as fast, but after $k$ steps the sum is off by `xs[0] - xs[k]`."

7. `review-2.json` | `items[1].widget.wrong[1].value` with `items[1].feedback.byKey.kept` | wrong, minor | The slip value 15 is paired with "You added the new numbers without dropping the old ones." | That mistake gives $6 + 4 + 6 = 16$. 15 is $5 + 4 + 6$: the 1 dropped and the 5 kept (script check). The feedback does not name the mistake that produces its value. | Change `wrong[1].value` from 15 to 16 and keep the feedback. (16 clashes with no other value on the item: the answer is 10 and the other slip is 5.)

8. `review-2.json` | `items[2].widget.wrong[0].value` with `items[2].feedback.byKey.off` | wrong, minor | The slip value 9 is paired with "That is `pre[4] - pre[0]`, which adds day 0 back." | `pre[4] - pre[0] = 10 - 0 = 10`. 9 is `pre[4] - pre[2] = 10 - 1` (script check). | Change `wrong[0].value` from 9 to 10 and keep the feedback. (10 clashes with no other value: the answer is 6 and the other slip is 3.)

9. `homework-2.json` | `items[0].feedback.byKey.test-6` | imprecise, minor | "Test 6 has a repeated 2. Keep `i` and `j` on different positions." | With `d > 0`, when `i == j` the gap is 0, which is below `d`, so `j` moves on anyway. The answer is the same with or without the guard on 4,000 random lists (script `[basis] hw2 h-difference`). The line names a slip that cannot fail this test. | "Test 6 is `[2, 2, 5]` with `d = 3`. The pair is 5 and either 2, so the answer is `True`."

10. `homework-2.json` | `items[4].prose` (last sentence) | imprecise, minor | "So `P[r][c]` sums rows below `r` and columns below `c`." | It means rows and columns with a smaller index. In the table shown, "below" reads as a larger index, the opposite; l7 says "above and left". | "So `P[r][c]` sums the rows before row `r` and the columns before column `c`."

11. `homework-2.json` | `items[5].feedback.byKey.four` | wrong, minor | "`[12, 3, 7, 9]` is the first window to reach 20". | The growing window reaches 20 at `[12, 3, 7]`, which sums to 22, as the item's own explain says (script check `hw2 h-min-volume`). | "`[12, 3, 7, 9]` reaches 20, but so does `[12, 3, 7]`, at 22, with one minute fewer."

12. `l8-best-day.json` | `screens[5].prose` and `screens[5].question`; `homework-2.json` | `items[7].prompt` and `items[7].model` part (c) | imprecise, serious | The lesson says "That is the maximum drawdown, which you coded in Python Foundations and tested in the pytest course", then asks for it in pounds. The homework asks for "the maximum drawdown of 10 years of daily closing prices" and computes the largest fall in pounds. | Those earlier lessons define drawdown as a fraction of the peak (`py-found/l7-arguments.json`: "the largest $1 - \text{value}/\text{peak}$"; `pytest/l3-reading-failure.json`: "It is a fraction of the peak"). The fall in pounds is a different measure and can pick a different episode: for `[100, 60, 200, 130]` the largest fall in pounds is 200 to 130, and the largest fractional fall is 100 to 60 (script `[basis] absolute and fractional`). The model's identities in (c), "best trade on the negated prices" and "minus the minimum sum of consecutive changes", hold for the pound measure only. The graded keys (15 and, in review-2, 80) are right for the measure asked. A learner is told one name covers both without being told the measure changed. | `l8` `screens[5].prose`: "Reflect the loop: keep the **highest** price so far, and the worst fall from it. That is the maximum drawdown, here in pounds. Python Foundations and the pytest course measured the same fall as a fraction of the peak." `homework-2` `items[7].prompt`, first sentence: "A colleague's risk script computes the maximum drawdown, in pounds, of 10 years of daily closing prices like this:". `homework-2` `items[7].model`, end of part (c), add: "These identities hold for the fall in pounds. For the fall as a fraction of the peak, keep the same running high and divide each fall by it."

13. `l8-best-day.json` | `screens[9].explain.text` (sentences 2 and 3) | wrong, serious | "A backtest beating it is reading future prices or mispricing fills. Common causes are a look-ahead bug or a wrong index alignment." | `best_trade` is already the perfect-foresight answer: the maximum of $p_j - p_i$ over every $i < j$ is 9 (script check). A strategy that reads future closes can reach £9 and can never exceed it, so look-ahead cannot explain £12. Only a trade that is not "buy at one of these closes, then sell at a later one" can. The sentence teaches a wrong idea of what the bound means. The graded key (the backtest has a bug) is right. | "`best_trade` gives an upper bound for any one-trade strategy on these closes, even one that could see the future: £9. A backtest that beats it did not buy and then sell at these closes. Check for a wrong index alignment, a sale booked before its purchase, or fills at prices outside the series."

14. `l11-first-in-first-out.json` | `screens[0].prose` (sentence 2) | imprecise, minor | "An exchange fills orders at one price in arrival order." | True under price-time priority. Some markets share fills pro rata among orders at one price (CME Group, matching algorithm overview: FIFO and pro-rata algorithms). | "This exchange fills orders at one price in arrival order, a rule called price-time priority."

15. Unverified remarks about markets and industry (three paths) | unverified, minor | (a) `l10-next-greater.json` `screens[9].prose`: "A long wait means a ceiling held. A short one means momentum." (b) `l12-nodes-and-pointers.json` `screens[10].prose`: "An exchange keeps each price level as a queue of resting orders. Cancels are frequent, so each node has both `prev` and `next`". (c) `l13-fast-and-slow.json` `quiz[2].explain.text`: "That is the reason interviewers ask for it." | None has a source, and none is needed for the teaching. | (a) "The desk reads a long wait as a ceiling that held, and a short one as momentum." (b) "This exchange keeps each price level as a queue of resting orders. It expects many cancels, so each node has both `prev` and `next`: a **doubly linked list**." (c) "That saving in memory is why Floyd's method is worth knowing."

16. `l11-first-in-first-out.json` | `screens[6].widget.how` and `screens[6].feedback.byKey.test-11`, with `screens[6].widget.tests[10]` | unverified, minor | "Test 11 has 200,000 values with $w = 2000$; slicing each window cannot finish in time." | `[max(xs[i:i + w]) for i in ...]` on that input takes 3.2 s in native CPython 3.13, under the 5 s case limit (`docs/AUTHORING.md`, code widget limits). Pyodide is slower by a factor that depends on the machine, so the claim may or may not hold in the app. I could not run Pyodide timing here. | Change `tests[10].call` to `max_sliding_window(list(range(200000, 0, -1)), 20000)[:3]`; the expected value `[200000, 199999, 199998]` is unchanged (script `[fix] l11 test`). Change "$w = 2000$" to "$w = 20000$" in `how`. The slice version then does ten times the work.

17. `l11-first-in-first-out.json` | `screens[7].explain.text` (last sentence) | wrong, minor | "Add `if dq[0] <= i - w: dq.popleft()` before the back pops." | Placed there in the loop shown, the line runs at `i = 0` with an empty deque and raises `IndexError: deque index out of range` (script check `l11.s7 explain fix`). The lesson's own solution guards it. | "Add `if dq and dq[0] <= i - w: dq.popleft()` before the back pops."

18. `review-3.json` | `items[7].prose` (sentence 2) | imprecise, minor | "The deepest nesting tells you how many intermediate results a stack-based evaluator holds at once." | `(1 + (2 * (3 - 4)))` has depth 3, and a two-stack evaluator holds four operands before the first `)` (script check). Depth bounds the bracket stack, not the number of pending values. | "The deepest nesting is the tallest the bracket stack ever gets."

## Checks that found nothing

- Every graded key, every `wrong[]` value and every slip was recomputed; apart from findings 3, 7, 8 and 11 each feedback line names the mistake that produces its value.
- Big-O statements carry their case: hash operations are "on average" where first stated and the worst case is taught (l2 screens[3], homework-1 item 8); append is "amortised" (l1); deque ends are $O(1)$ and the middle $O(n)$ (homework-3). Timing checks in the script separate linear from quadratic for `insert(0)`, `pop(0)` and `popleft()`.
- Window and prefix invariants hold: the shrinking window is stated to need positive numbers and its failure on negatives is graded; `pre` uses $n + 1$ entries throughout; `count_subarrays_with_sum`, `best_trade`, the monotonic stack, the monotonic deque and Floyd's method each agree with brute force on random inputs.
- Kadane appears in two forms, and both are labelled: the empty-run form in l8 (matches "no trade") and the non-empty form in homework-2.

## Gates

- Validator: `node tools/validate.mjs` gives 0 errors (4531 warnings); the manifest did not change.
- Number scripts: none exists for ds levels 1 to 3 in `docs/reports/` (only `ds-4-perf-numbers.py`, out of scope).
- `grade-all.mjs --file` on review-1, homework-1, review-2, homework-2, review-3 and homework-3: 0 failures each, exit 0. It checks numeric, choice and multi widgets only (31 widgets), so the concepts script runs the code widgets.
- `ds-L1-3-concepts.py`: exit 1, with 11 failing checks that map to findings 1, 2, 3, 5, 6, 7, 8, 11, 13, 17 and 18.

## Overlap with the earlier read

Earlier read: `docs/reviews/review-1.8.md` (algo-think, ds and graphs-dp together), opened after the WIP commit `15ab4d08`. Only its ds level 1 to 3 lines are counted. Its fix pass had already been applied to the content this audit read, so its three conceptual findings could no longer be found.

| Conceptual findings, ds L1 to L3 | Count |
|---|---|
| Found by this audit only | 18 (findings 1 to 18) |
| Found by the earlier review only | 3 |
| Found by both | 0 |

The earlier review's three conceptual findings, all fixed before this read: homework-3 `items[2]` (the FIFO key equalled the plain-average slip, error), homework-1 `items[6]` (the key assumed an unstated constant list length, warning) and l7 `screens[8]` explain (prefix counts 10,001 and 10,000, note). This audit rechecked all three as they now stand and they hold (ledger rows for those paths are `correct`).

Not counted as conceptual: the earlier review's five test-strength findings in scope (homework-3 `items[0]`, `[4]`, `[5]`; l13 `screens[7]`, `[9]`), three explanations over three sentences and its sentence-length lists.

New `wrong` findings that no earlier read found: **9** (findings 1, 2, 3, 5, 7, 8, 11, 13 and 17), of which 1 is serious (13). That is above the convergence limit of one per three levels, so the course needs another blind audit after its fix pass.

One disagreement to record. The earlier review states that window re-slicing times out on l11. Finding 16 measured 3.2 s for the same naive method on this machine, under the 5 s limit. The two runs do not settle it, which is why the verdict is `unverified` and the fix widens the test instead of arguing the timing.

## Limits of this audit

- Sources named in the ledger without a run (CLRS, Knuth, Bentley, Hull, the CPython and pandas sources, the CME overview) were cited from memory of the named section. They were not reopened in this session.
- Code ran in CPython 3.13, not in Pyodide 0.27.7. No check depends on a behaviour that differs between CPython 3.12 and 3.13, but Pyodide timing was not measured.
- Severity of finding 12 is a judgement. The graded keys are right for the measure asked; the finding is that one name is used for two measures without saying so. A fixer may reasonably rate it minor.

## Fix pass

Opus fixer, audit session 11. Every new sentence and code line was checked by a run (CPython 3.13) or a derivation; the concepts script tests each corrected text under a tag ending "(fix pass)", and keeps the round 1 evidence as "[basis]" lines.

1. fixed. Doubling from capacity 1 copies $2^k - 1 < 2n$ items for $n$ appends; run for $n < 5000$ (17 appends give 31).
2. fixed. `list.remove` stops at the first match (identity first, then one `__eq__`); timed: 10 times the length gives about 10 times the cost, as for `pop(0)`.
3. fixed differently. Pointers are at indices 1 and 5, so 2 is not at an end; squares sort to `[1, 4, 9, 16, 36, 49]`, so 4 goes second. The next slot here is the fifth, not the last, so the line ends "not the fifth".
4. fixed. Put struck at £100 plus call at £105 gives `[10, 5, 0, 0, 5, 10]` at £90 to £115 (run); a strangle has two strikes, so the six numbers are expiry prices.
5. fixed. Run: the trap returns 6 on `'abcbdae'` (right answer 5) and 3 on `'abcbd'` (right answer 3).
6. fixed. The bug adds `xs[k-1] - xs[k]` per slide, which telescopes to `xs[0] - xs[k]`; checked on 2,000 random lists.
7. fixed. Slip `kept` changed 15 to 16: adding without dropping gives $5 + 1 + 4 + 6 = 16$, and $6 + 4 + 6 = 16$. No clash with the key 10 or slip 5.
8. fixed. Slip `off` changed 9 to 10: `pre[4] - pre[0] = 10 - 0 = 10`, and $4 - 3 + 6 + 3 = 10$. No clash with the key 6 or slip 3.
9. fixed. With `d > 0`, `i == j` gives gap 0 < `d`, so `j` moves on with or without the guard; the new line states test 6 and its answer, `True` (run).
10. fixed differently. "Rows before row `r`" still reads loosely; the line now says `P[r][c]` sums every cell in rows 0 to `r - 1` and columns 0 to `c - 1`, which gives $14 - 4 - 7 + 2 = 5$ (run).
11. fixed (worded "already makes 22"). Run: the growing window reaches 20 at `[12, 3, 7]` = 22.
12. fixed differently. l8 `screens[5].prose` now says the drawdown is measured here in pounds and is usually quoted as a fraction of the peak, as in py-found and pytest (both checked in their files). homework-2 `items[7].prompt` adds "in pounds", so the model's identities in (c) hold as stated; the brief asked for the convention once, so (c) is unchanged. Keys 15 and 80 unchanged.
13. fixed differently. Run: the best buy-before-sell pair is 9, and both pairs that make 12 sell before they buy (days 1 and 5). New text: look-ahead can reach £9 but never beat it; beating it needs a sale before the purchase (a misaligned index) or fills at other prices.
14. fixed differently. "This exchange uses price-time priority: at one price, orders fill in arrival order." Price-time priority means best price first, then arrival order at one price; pro-rata markets exist (CME matching algorithms), so the rule is stated as this exchange's.
15. fixed. All three now state a desk's reading, this exchange's design, or the teaching reason, with no claim about markets or interviews.
16. fixed. Test 11 now uses $w = 20000$; run: the deque solution gives `[200000, 199999, 199998]` in 0.03 s, while slicing 2,001 of the 180,001 windows already takes 0.32 s (about 29 s for all). `how` changed to match.
17. fixed. Run: the unguarded line raises `IndexError` at `i = 0`; with `dq and` the loop gives `[5, 4, 4, 6]`, matching the lesson's solution.
18. fixed differently. "The deepest nesting is the tallest a stack of open brackets ever grows." Checked on five strings, including `(1 + (2 * (3 - 4)))` at 3.

Ledger `unverified` rows 202, 212, 225 and 239 are findings 15 and 16; none was left over.

Script changes: `docs/reports/ds-L1-3-concepts.py` now tests the corrected texts (the 11 failing checks were rewritten as "(fix pass)" checks, with the old evidence kept as passing "[basis]" lines) and adds checks for findings 4, 9, 10, 12 and 16. 167 pass, 0 fail, exit 0; all 32 code widgets: solution passes, starter fails, l11 `screens[6]` with the new test.

Gates: validator 0 errors (4531 warnings, as before; manifest unchanged); `ds-4-perf-numbers.py` exit 0; voice scan 35 on ds: 0 and 0; `grade-all --file` on review-2, review-3, homework-2: 0 failures; playthrough desktop and `--mobile` of l1, l5, l6, l8, l10, l11, l12, l13, review-2, review-3 and homework-2: all green.

## Fix-pass read

Reader: fresh Fable reader, blind to the audit, its ledger and the fixer's notes. Diff read: `git diff e9442db7~1 e9442db7 -- app/content/courses/ds/` (11 files, 22 changed strings). Every row hand-checked, then re-run in CPython 3.13 from the item's own JSON (solutions, tests, tables and series loaded from the files, not retyped).

| # | File | JSON path | New text (short) | Verdict | Basis |
|---|------|-----------|------------------|---------|-------|
| 1 | homework-2.json | items[0].feedback.byKey.test-6 | "Test 6 is `[2, 2, 5]` with `d = 3`. The pair is 5 and either 2, so `True`" | correct | Sixth test is `has_pair_with_difference([2, 2, 5], 3)`, expect `True`; 5 − 2 = 3 for either 2. Solution run: passes all 10 tests. |
| 2 | homework-2.json | items[4].prose | "`P[r][c]` sums every cell in rows 0 to `r - 1` and columns 0 to `c - 1`" | correct | Rebuilt `P` from the grid under that definition: equals the canvas table cell for cell (`P[3][3] = 14`). `14 - 4 - 7 + 2 = 5` equals the direct sum 4 + 1 − 2 + 2. Standard 2D prefix sum with a zero border. |
| 3 | homework-2.json | items[5].feedback.byKey.four | "`[12, 3, 7, 9]` reaches 20, but `[12, 3, 7]` already makes 22, with one minute fewer" | correct | 12 + 3 + 7 + 9 = 31 ≥ 20; 12 + 3 + 7 = 22; brute force over all windows gives fewest 3, best pair 19. Agrees with key 3 and the explain. |
| 4 | homework-2.json | items[7].prompt | "computes the maximum drawdown, in pounds, of 10 years of daily closing prices" | correct | The quoted code returns `prices[i] - prices[j]`, a price difference. Run on the l8 series it returns 15, not 15/110. Model answer and rubric use the same absolute measure. |
| 5 | l1-arrays-in-memory.json | screens[4].explain.text | "with doubling they are always fewer than twice the appends" | correct | From capacity 1, copies after n appends are 2^k − 1 with 2^k the smallest power of two ≥ n, and 2^k < 2n. Simulated n = 1 to 199,999: copies < 2n throughout; copies(16) = 15. (Copies ≥ appends at n = 3, 5, 6, 7, so the bound of twice is the right one.) CLRS section 17.4. |
| 6 | l1-arrays-in-memory.json | screens[10].widget.options[3].why | "`remove` finds the value at index 0 on its first comparison, then shifts the rest left: the same linear cost as `pop(0)`" | correct | `list.remove` scans from index 0 and `window[0]` matches itself at once (CPython `list_remove`, identity shortcut; run confirmed, 20 items left). The tail then shifts left by one, as for `pop(0)`: O(n). |
| 7 | l10-next-greater.json | screens[9].prose | "The desk reads a long wait as a ceiling that held, and a short one as momentum" | correct | Now an attributed reading, not a claim about markets. Table recomputed: `[2, 1, 3, 2, 1, 0, 0]`. |
| 8 | l11-first-in-first-out.json | screens[0].prose | "This exchange uses price-time priority: at one price, orders fill in arrival order" | correct | Definition of price-time (FIFO) priority; Harris, *Trading and Exchanges*, ch. 6. Scoped to "this exchange", so pro-rata venues are not denied. 400 shares fill A 300 then B 100, as keyed. |
| 9 | l11-first-in-first-out.json | screens[6].widget.tests[10].call | `max_sliding_window(list(range(200000, 0, -1)), 20000)[:3]`, expect `[200000, 199999, 199998]` | correct | Runs below. Window i of a descending list has maximum `xs[i]` = 200000 − i, so the first three are as expected; the solution's full output (180,001 values) equals `xs[:180001]`. Solution passes 11 of 11; starter passes 2 of 11 (tests 6 and 7, both `[]`) and fails test 11. |
| 10 | l11-first-in-first-out.json | screens[6].widget.how | "Test 11 has 200,000 values with $w = 20000$; slicing each window cannot finish in time" | correct | Matches the test call. Slicing does 180,001 × 20,000 = 3.6 × 10^9 element reads; measured 29.5 s native, against a 5 s limit (`TEST_MS = 5000` in `engine/widgets/code.js`). |
| 11 | l11-first-in-first-out.json | screens[7].explain.text | "Add `if dq and dq[0] <= i - w: dq.popleft()` before the back pops" | correct | Ran the screen's loop with the line inserted: `[5, 4, 4, 6]`. Without `dq and` the same line raises `IndexError` at `i = 0` (empty deque). Now identical to the solution and step hint on screens[6]. Trap code alone returns `[5, 5, 5, 6]`, as keyed. |
| 12 | l12-nodes-and-pointers.json | screens[10].prose | "This exchange keeps each price level as a queue of resting orders. It expects many cancels, so each node has both `prev` and `next`" | correct | A design choice attributed to one exchange. O(1) unlink from the middle needs `prev`; CLRS section 10.2. Agrees with the keyed option. |
| 13 | l13-fast-and-slow.json | quiz[2].explain.text | "That saving in memory is why Floyd's method is worth knowing" | correct | Follows from the two sentences before it: O(n) set against two references, both O(n) time. Knuth, TAOCP vol. 2, section 3.1, exercise 6. |
| 14 | l5-both-ends.json | screens[4].feedback.byKey.c3 | "2 is not at an end. Its square, 4, is the second smallest, so it goes in the second slot, not the fifth" | correct | Squares sorted: `[1, 4, 9, 16, 36, 49]`; 4 is at position 2. The slot being filled is the fifth (36), as the explain says. Pointers are at −3 and 6, so 2 is under neither. |
| 15 | l5-both-ends.json | quiz[2].prose | "A strangle's payoff at six expiry prices, from £90 to £115" | correct | Put struck at £100 plus call struck at £105, at expiry prices 90, 95, ..., 115: `[10, 5, 0, 0, 5, 10]`, recomputed. The x-axis is the underlying at expiry, not strikes; Hull, ch. 12 (trading strategies). |
| 16 | l6-sliding-window.json | screens[6].prose | "This version passes `'abcbd'`" | correct | Ran the screen's code: `'abcbd'` gives 3, brute force 3. (On `'abcbdae'` it gives 6 against a true 5, so the new string is the one that passes.) `'abba'` gives 3 against a true 2, as keyed; the explain's `max(left, ...)` fix gives 2. |
| 17 | l6-sliding-window.json | quiz[3].widget.options[3].why | "after $k$ slides the sum is off by `xs[0] - xs[k]`" | correct | Slide m subtracts `xs[m]` where `xs[m - 1]` should go; the errors telescope to `xs[0] - xs[k]`. Checked on 2,000 random lists and widths: buggy total minus true window sum equals `xs[0] - xs[k]` at every slide. |
| 18 | l8-best-day.json | screens[5].prose | "That is the maximum drawdown, measured here in pounds. It is usually quoted as a fraction of the peak, as in Python Foundations and the pytest course" | correct | Screen's key is £15 (110 to 95), recomputed over all pairs. Standard definition is (peak − trough) / peak; here 15 / 110 = 13.6%. Cross-references hold: py-found l13 uses `(peak - p) / peak`, pytest l3 says "a fraction of the peak". |
| 19 | l8-best-day.json | screens[9].explain.text | "`best_trade` caps any one long trade on these closes at £9, even one chosen with sight of the future. So a look-ahead bug can reach £9 but never beat it. To beat it, a backtest must sell before buying, often via a misaligned index, or fill at other prices" | correct | Maximum of `px[j] - px[i]` over all i < j is 9 (98 to 107): this is the perfect-foresight bound, so foresight alone attains it at most. Dropping the order constraint gives 15, so beating 9 at these closes needs a sale dated before the purchase; the only other route is a fill that is not one of these closes. Agrees with the keyed option and the `range` distractor. Note, no change needed: a P&L arithmetic slip would also show more than £9; the sentence covers trades, not sums. |
| 20 | review-2.json | items[1].widget.wrong[1].value | 16 (`kept`: "added the new numbers without dropping the old ones") | correct | 6 + 4 + 6 = 16 (equally 5 + 1 + 4 + 6). Distinct from the key 10 and the slip 5. |
| 21 | review-2.json | items[2].widget.wrong[0].value | 10 (`off`: "That is `pre[4] - pre[0]`") | correct | `pre = [0, 4, 1, 7, 10, 6]` rebuilt; `pre[4] - pre[0]` = 10 − 0 = 10. Distinct from the key 6 and the slip 3 (`pre[3] - pre[1]` = 7 − 4). |
| 22 | review-3.json | items[7].prose | "The deepest nesting is the tallest a stack of open brackets ever grows" | correct | Pushed `(` and popped on `)` for each test string: maximum stack height equals each expected value. Solution passes 6 of 6, starter 0 of 6. |

### Runs

- `l11` screens[6], CPython 3.13.18, native: solution 11 of 11, slowest test 0.03 s; test 11 best of five 0.027 s. Starter 2 of 11. Trap version (no front check) 6 of 11, failing 2, 3, 8, 10 and 11.
- Slow methods on test 11, native: `max(xs[i:i + w])` per window 29.5 s measured in full; `deque(maxlen=w)` with `max(dq)` about 26 s; pure-Python double loop about 62 s. At the old $w = 2000$ the first two took about 3 s natively, inside the limit, so the old test could pass a slow method on a fast machine.
- Margin against the 5 s limit: the slow method is about 6 times over natively and Pyodide only widens that. The solution has about 180 times headroom natively; at a tenfold Pyodide slowdown it is near 0.3 s, still about 17 times inside. The descending input is also the worst case for "rescan only when the maximum leaves", so that shortcut does not slip through.

### Findings

None. 22 rows read: 22 correct, 0 wrong, 0 imprecise, 0 misleading, 0 unverified. No slip value collides with a key or another slip.

Observation only, not a finding: `screens[6].widget.how` writes "200,000" with a comma and "$w = 20000$" without one. The old text had the same pattern.

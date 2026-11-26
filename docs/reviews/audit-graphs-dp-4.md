# Blind concept audit: graphs-dp level 4 (Dynamic programming), round 1

Commit 6c01af87. Files: `l14-knapsack`, `l15-common-subsequence`, `l16-grid-paths`, `l17-dice-stopping`, `review-4`, `homework-4` (all under `app/content/courses/graphs-dp/`). Stage 1 course, full ledger.

- Ledger: `docs/reports/audit-graphs-dp-4-ledger.md`, 896 rows: 868 correct, 13 wrong, 9 misleading, 6 imprecise, 0 unverified. The 28 non-correct rows fold into the 14 findings below.
- Concepts script: `docs/reports/graphs-dp-L4-concepts.py`, 161 checks, exits 1 at this commit. Three checks fail because the content is wrong (F1, F2, F3 below) and stay failing until the fix pass.
- Sources: CLRS 3e ch. 15 and 16.2; Kleinberg and Tardos ch. 6.4; Sedgewick and Wayne; Garey and Johnson 4.2; Ferguson, *Optimal Stopping and Applications*, ch. 1 and 2; Hull ch. 11 and 13; Feller vol. 1 ch. II.

## Watch list

| watch item | result |
|---|---|
| 0/1 against unbounded knapsack | Correct throughout. The upward one-row loop equals the unbounded optimum on 200 random cases and the downward loop equals the 0/1 optimum on 300 (brute force). `knapsack_1d([2, 3], [30, 40], 6)` is 90, and the trace 0, 0, 30, 30, 60, 60, 90 is right. Homework `unbounded_knapsack` states weights of at least 1, which the recurrence needs. |
| pseudo-polynomial stated as polynomial | Correct. l14 `screens[8]`, the quiz and homework `h4-pseudo` all say the cost is polynomial in the value of W and exponential in its length, and that the general problem is NP-hard. |
| top-down memo against bottom-up table | No claim made in this level; nothing to fault. |
| optimal substructure and overlapping subproblems as sufficient | No such claim in this level. |
| stopping values, exact and Monte Carlo | V1 to V4 = 7/2, 17/4, 14/3, 89/18; thresholds 4, 5, 5, 5, then 6; V10 = 5.6502, V50 = 5.99976; all exact with fractions and by Monte Carlo of 10^6 games each (within 4 standard errors). Stopping on a 4 with three rolls is worth 4.625, measured more than 10 standard errors below 4.6667. Dealer values 99.6375, 99.75 and 99.7630 exact. One slip value is wrong (F2). |

## Findings

Severity then tag. 4 wrong, 5 misleading, 5 imprecise; 1 serious, 13 minor.

1. `l15-common-subsequence.json` | `screens[7]`: `widget.options[1].why`, `options[2].why`, `options[3].why`, `hints[0].text`, `hints[2].text`, `feedback.correct`, `feedback.byKey.three`, `explain.text` | **wrong, serious** | The trap says the off-by-one code crashes "at `i = 5`", reading `a[5]`, after it "compares the wrong letters for i < 5". It never gets there. The inner loop runs `j` to `n = 4` in the very first row, so the first error is at `i = 1`, `j = 4`, reading `b[4]`. The key (`IndexError`) is right; the account of how the code runs is false in eight strings, on a screen whose whole job is tracing. | Run in CPython: first `IndexError` at `(i, j) = (1, 4)` (concepts script, check F1). For any non-empty `b` the inner loop reaches `b[n]` in row 1, so no choice of words can make `a[m]` the crash site. | Paste-ready replacements:
   - `options[1].why`: "You read `a[i]` and `b[j]` as the cell's letters. Cell $(i, j)$ is for `a[i - 1]` and `b[j - 1]`; at $j = 4$ the code reads `b[4]`, which does not exist."
   - `options[2].why`: "Before any wrong number comes out, the first row reaches $j = 4$ and reads `b[4]`, past the end of EDGY."
   - `options[3].why`: "The loop never finishes: `b[4]` does not exist."
   - `hints[0].text`: "What is the largest `j` the inner loop reaches, and how long is EDGY?"
   - `hints[2].text`: "At `i = 1`, `j = 4`, `b[4]` is read. EDGY has indices 0 to 3."
   - `feedback.correct`: "In the first row, at `j = 4`, it reads `b[4]`, one past the end of EDGY."
   - `feedback.byKey.three`: "You expected the right answer. With the padded table, `b[j]` is one letter ahead, and at `j = 4` it runs off the end."
   - `explain.text`: "Row 0 and column 0 are the empty prefixes, so cell $(i, j)$ compares `a[i - 1]` with `b[j - 1]`. Writing `a[i]` and `b[j]` compares the wrong letters, then crashes in the first row at $j = 4$, on `b[4]`. With other loop bounds the same slip gives a silently wrong count, which is worse."
   - `explain.canvas.highlight` to `["r2c5"]` and `explain.canvas.caption` to "Column 4 holds b[3], the Y; b[4] does not exist". `feedback.generic` and `hints[1]` can stay.

2. `l17-dice-stopping.json` | `screens[9].widget.wrong[2]` (`first-best`) and `feedback.byKey.first-best` | **wrong, minor** | The slip "accepted 99.5 and 99.9 from the first dealer" has value 99.65. That policy is worth 99.625, so a learner who makes the named mistake gets the generic line, and 99.65 matches no policy. | (99.5 + 99.9) / 4 + (2/4) × 99.55 = 49.85 + 49.775 = 99.625, exact; Monte Carlo of 400,000 sales gives 99.625 within 0.0025 and excludes 99.65 (check F2). | Set `wrong[2].value` to `99.625`. The feedback line is then correct as written.

3. `homework-4.json` | `items[2].widget.wrong[0]` (`edge`) and `feedback.byKey.edge` | **wrong, minor** | The slip for "first column kept at 1 below its block" has value 12. Filling the first row and column with 1s gives 11 (rows 4 and 5 become 1 2 4 4 7 and 1 3 0 4 11). Zeroing only the blocked cell gives 9, the right answer. Nothing gives 12. | Concepts script check F3: both edge variants tabulated, reachable values {11, 9}. | Set `wrong[0].value` to `11`. The feedback line is then correct as written.

4. `l17-dice-stopping.json` | `screens[7].feedback.byKey.test-3` | **wrong, minor** | "If you got 4.25, run the loop n − 1 times, not n − 2." A loop of n − 2 steps returns 3.5 for `dice_value(2)` and fails test 2 first. A learner who sees this line has passed test 2, so the loop count is not the fault: the rule was applied once only (4.25), or always against 3.5 (4.625). | Mutants under the page Pyodide: `loop_n_minus_2` first fails test 2; `one_step_only` first fails test 3 with 4.25; `value_vs_3.5` first fails test 3 with 4.625. | "Test 3 is $V_3 = 4.666667$. If you got 4.25, you applied the rule once. Apply it $n - 1$ times, each time against the value just computed."

5. `l17-dice-stopping.json` | `screens[7].feedback.byKey.test-9` | **misleading, minor** | "With 5 rolls, compare with V4 = 4.9444, not 3.5." Comparing with 3.5 gives threshold 4 for three rolls and fails test 8 first, so the learner who makes this mistake never sees the line. | Mutant `thr_vs_3.5` first fails test 8 (returns 4, expects 5). | Move the diagnosis: add `test-8`: "Test 8: with 3 rolls, compare with $V_2 = 4.25$, not 3.5. Stop from 5." Change `test-9` to: "Test 9: with 5 rolls the bar is $V_4 = 4.9444$, so a 5 still stops you."

6. `l14-knapsack.json` | `screens[6].feedback.byKey.test-3`, `test-5`, `test-10` | **misleading, minor** | Each line names a mistake that fails an earlier test. No fit check: 170 on test 1. Reading the same row (unbounded): 50 on test 4. Trying every subset, or plain recursion: time out on test 9 (60 items), not test 10. All three learners get the generic line. | Mutants: `nofit` and `nofit_from1` fail test 1; `unbounded_samerow` and `unbounded_1d` fail test 4; `subsets` and `recursion` stop at test 9. | Replace the three keys with: `test-1`: "Test 1 expects 90. If you got 170, take an item only when `wt <= w`: a negative index `w - wt` wraps round in Python." `test-4`: "Test 4 expects 18: each item may be used once. Read the row above, `best[i - 1]`, when you take an item." `test-9`: "Test 9 has 60 items. If it timed out, fill the table rather than trying every subset."

7. `l15-common-subsequence.json` | `screens[6].feedback.byKey.test-5` and `byKey.error` | **misleading, minor** | "Add 1 only when the letters match" sits on test 5, but adding 1 without a match returns 4 on test 1. The `error` line gives `IndexError` advice, but an exception inside a test is graded as `test-1`; the `error` key fires only when the code fails to load. Neither line reaches its learner. | Mutants: `always_plus1` fails test 1 with 4; `ai_bj` gives key `test-1` with the traceback in the row. `app/js/engine/widgets/code.js` line 622. | Replace both with `test-1`: "Test 1 expects 3. If you got 4, add 1 only when the letters match. If you see `IndexError`, compare `a[i - 1]` with `b[j - 1]`."

8. `l15-common-subsequence.json` | `screens[9].feedback.byKey.test-4` and `test-6` | **misleading, minor** | A missing first column returns 1 on test 1; adding 1 on a match returns 5 on test 1. Both lines sit on later tests. (`test-3`, the missing first row, is right: that mutant passes tests 1 and 2.) | Mutants: `no_first_col` fails test 1 (1), `plus1_on_match` fails test 1 (5), `no_first_row` fails test 3. | Replace both with `test-1`: "Test 1 expects 2. If you got 1, set the first column to `d[i][0] = i`. If you got 5, copy the diagonal on a match without adding 1."

9. `l16-grid-paths.json` | `screens[7].feedback.byKey.test-3` | **misleading, minor** | "Do not take a min with a missing cell" sits on test 3. Counting a missing neighbour as 0, or letting index −1 wrap, returns 6 on test 1. | Mutants `missing_zero` and `wrap_min` both fail test 1 with 6. | Replace with `test-1`: "Test 1 expects 12. If you got 6, a missing neighbour was counted as 0 inside the min. On the edges use the one neighbour there is."

10. `l16-grid-paths.json` | `screens[9].feedback.byKey.no-down` | **imprecise, minor** | 0.1664 is 0.55³. It leaves out the down-move and the count of 4 paths; the line names only the first, and following it gives 0.0749, another wrong value. | 0.55³ = 0.166375; 0.55³ × 0.45 = 0.0749; 4 × 0.0749 = 0.2995. | "0.1664 is $0.55^3$, the three up-moves alone. Each path also has one down-move, 0.45, and 4 paths reach the node."

11. `l17-dice-stopping.json` | `screens[6].widget.options[3].why` | **imprecise, minor** | "Even with many rolls left, the next roll could be your last chance." With many rolls left it is not. The right reason is that no 6 may ever come. | P(no 6 in n rolls) = (5/6)^n > 0; exactly, 6 − V_n = (5/6)(6 − V_(n−1)) from n = 6 on (concepts script). | "With $n$ rolls there is a $(5/6)^n$ chance of never seeing a 6, so $V_n < 6$ for every $n$."

12. `l17-dice-stopping.json` | `screens[6].explain.text` (last sentence) | **imprecise, minor** | "The secretary problem is the same idea: pass on early candidates, then take the first that beats the rest." The rule takes the first candidate better than all seen so far, not one that "beats the rest", which the chooser cannot know. The quiz states it correctly. | Ferguson ch. 2.3. | Last sentence: "The secretary problem is a cousin: pass on about the first $n/e$ candidates, then take the first who beats everyone seen so far."

13. `l17-dice-stopping.json` | `quiz[3].widget.options[1].why` and `options[2].why` | **imprecise, minor** | "Keeps a chance near 37% for every n": the best chance is 0.5 at n = 3 and 0.3987 at n = 10 (the homework's own figure). The exact statement is "above 1/e". The second line argues that 1/2 "would need the best candidate to land in the second half and be picked every time", which is not why 1/2 is out of reach. | Exact optimal chance is above 1/e for n = 1 to 150 and falls to it (concepts script). | `options[1].why`: "It feels as if a huge field must defeat any rule. But the best rule keeps the chance above $1/e$, about 37%, for every $n$." `options[2].why`: "No rule does that well for large $n$. The best rule sometimes stops too early and sometimes never stops, and its chance falls towards $1/e$."

14. `homework-4.json` | `items[8].widget.model` ("Risk in pence" paragraph) | **imprecise, minor** | "Round risk to coarse units … and accept a small error." Rounding weights carries no error bound. Rounding to the nearest unit can break the budget; rounding up keeps the budget but can lose most of the profit. (The textbook approximation scheme rounds values, not weights.) | Concepts script: two trades of 7,400 each against 10,000 both round to 1 unit of 5,000 and fit a 2-unit budget, but use 14,800; trades (5,001, 5,001, 9,999) against 10,002 drop from profit 20 to 11 when rounded up. Kleinberg and Tardos 11.8. | Replace the sentence with: "Then round each trade's risk up to coarse units (say £10,000, giving 200 columns again). The plan stays within budget but may no longer be the best."

Not findings, for the fixer's eye only: `homework-4` `items[0].widget.wrong[1]` (`ratio`, value 3) has no feedback line, and packing by value per kg gives 7 there, so the entry does nothing. l14 `screens[8]` says "about 1,000 times" where the exact ratio of cells is 875; fine as an estimate.

## Code widgets: feedback sweep

Every `feedback.byKey.test-N` line was swept. Mutants were graded under the page's Pyodide 0.27.7 (wasm32, recursion limit 3000) through `app/tools/code-runner.mjs`; 53 mutants over 9 widgets.

| widget | line | natural codings of the mistake, first failing test | verdict |
|---|---|---|---|
| l14 `screens[6]` | test-3 | no fit check, two codings: test 1 (170) | not reached (F6) |
| l14 `screens[6]` | test-5 | same-row read, upward one-row: test 4 (50) | not reached (F6) |
| l14 `screens[6]` | test-10 | every subset, plain recursion: stopped at test 9 | not reached (F6); timing-dependent |
| l14 `screens[9]` | test-1, test-4 | lines describe their tests | correct |
| l14 `screens[9]` | test-5 | take on a tie: test 5 | correct |
| l15 `screens[6]` | test-2 | describes its test | correct |
| l15 `screens[6]` | test-5, error | always add 1: test 1; `a[i]`: key test-1 | not reached (F7) |
| l15 `screens[9]` | test-3 | no first row: test 3 | correct |
| l15 `screens[9]` | test-4, test-6 | no first column: test 1; add 1 on match: test 1 | not reached (F8) |
| l16 `screens[6]` | test-2 | edges all 1s, zeroed block with 1s after: test 2 | correct |
| l16 `screens[6]` | test-3 | start always 1: test 3 | correct |
| l16 `screens[6]` | test-10 | plain recursion: stopped after 5 s at test 10 | correct; timing-dependent |
| l16 `screens[7]` | test-2, test-7 | lines describe their tests | correct |
| l16 `screens[7]` | test-3 | missing cell as 0, wrapped index: test 1 (6) | not reached (F9) |
| l17 `screens[7]` | test-3 | loop n − 2: test 2 | false diagnosis (F4) |
| l17 `screens[7]` | test-6 | no n = 1 case: test 6 | correct |
| l17 `screens[7]` | test-9 | threshold against 3.5: test 8 | not reached (F5) |
| homework `items[4]` | test-1 | describes its test | correct |
| homework `items[4]` | test-8 | start from 0, loop n times: test 8 | correct |
| homework `items[5]` | test-1 | 0/1 downward loop: test 1 | correct |
| homework `items[5]` | test-5 | describes its test | correct |
| homework `items[5]` | test-9 | recursion without memo: stopped at test 9 | correct; timing-dependent |

Hidden tests reject every obviously wrong program tried (greedy packing, unbounded for 0/1 and the reverse, contiguous substring for LCS, letter counting, insert and delete only, greedy routes, forward valuation). One mutant passed all tests, l16 `screens[6]` with unguarded `ways[i - 1][j] + ways[i][j - 1]`; it is in fact correct, because the wrapped cells are still 0 when read. Memoised recursion passes homework test 9 within the recursion limit, as it should.

## Checks run

- `node tools/validate.mjs`: 0 errors (4,610 warnings, repository-wide).
- `node tools/run-number-scripts.mjs --only graphs-dp`: 3 scripts, 3 passed.
- `node tools/grade-all.mjs --code --file <each of the six files> --local-cdn <pkgs>`: 0 failures; 9 Python code widgets run.
- `docs/reports/graphs-dp-L4-concepts.py`: exit 1; 161 checks, 3 failing (F1, F2, F3), by design until the fix pass. Run with the venv Python 3 (NumPy not needed; no figure depends on a library version).
- No playthrough, as instructed.

## Overlap with earlier reads

Read after the ledger and findings above were written: `docs/reviews/review-1.8.md` (the only earlier read that covers level 4), `docs/reviews/review-1.9.md` (no graphs-dp content), `docs/reviews/audit-graphs-dp-1-3*.md` (levels 1 to 3 only; level 4 is out of their scope) and `docs/reports/graphs-dp-*` (performance reports for levels 1 to 3; no level 4 author report or number script exists).

`review-1.8.md` raised nothing conceptual on level 4. Its level 4 lines are a canvas label on l17 `screens[5]` (fixed), a small-label note on l14 (deferred to the engine) and sentence lengths. It checked that solutions pass and starters fail, and recomputed V2 to V4, which agree with this audit.

| conceptual findings | count |
|---|---|
| found by this audit only | 14 |
| found by the earlier review only | 0 |
| found by both | 0 |

New `wrong` that no earlier read found: 4 (F1 serious; F2, F3, F4 minor). That is over the convergence limit of one per three levels, so level 4 needs a fix pass, a fix-pass read and a second blind audit.

Finding class for SESSION PROTOCOL 6: ten `byKey` lines (F4 to F9) sit on a test their named mistake never reaches first, or on the `error` key for an in-test exception. The class is already ENGINE-BACKLOG 1028 and 1036; none of the nine level 4 code widgets declares `mutants`. The fixer should add a `mutants` entry for each rewritten line, using the mistakes named in this audit's table.

## Fix pass

Opus fixer, from commit 26f0197c. Every figure below was recomputed in this pass with exact fractions or a CPython run, and every mutant was graded under the page's Pyodide through `app/tools/code-runner.mjs`. No graded key, hidden test or solution changed; two slip values changed (F2, F3).

| # | status | basis (own) |
|---|---|---|
| 1 | fixed | CPython on HEDGE, EDGY: row `i = 1` reads `a[1]` fine and stops at `j = 4` on `b[4]` (EDGY has 4 letters). The eight strings now name `b[4]` in row 1. `hints[1]` now names cell $(i, j)$ with both letters; it and the explain canvas highlight `r2c5`, the crash cell. |
| 2 | fixed | Accept 99.5 or 99.9 first, then the two-dealer value: (99.5 + 99.9)/4 + (1/2)(99.55) = 99.625 exact; a 400,000-sale simulation gives 99.6247. Slip set to 99.625, 0.0125 clear of the key. |
| 3 | fixed | Table with the whole first row and column at 1 ends 1 3 0 4 11; brute force over all 70 routes gives 9. Slip set to 11. |
| 4 | fixed differently | Mutants: rule applied once and loop against 3.5 both give 4.25 at test 3; always stopping on 4 gives 4.625 at test 3; a loop of n − 2 fails test 2. The line now names both 4.25 codings and says to compare with the value just computed. |
| 5 | fixed | Threshold against 3.5, against `dice_value(n - 2)` and against `dice_value(1)` all return 4 at test 8. New `test-8` line. `test-9` now describes its test; guessing the pattern (n + 2, a lookup of 4, 5 then 6, 3 + (n + 1) // 2) returns 6 there first. |
| 6 | fixed | No fit check (three codings) gives 170 at test 1; same-row read and the upward one-row loop give 50 at test 4; subsets, bit masks and plain recursion run past 25 s on test 9. Lines moved to `test-1`, `test-4` (plus the downward loop for one row) and `test-9`. |
| 7 | fixed differently | My codings of "add 1 without a match" give 4, 7 and 8 on test 1, not only 4, so the line says "more than 3". `a[i]`, `b[j]` codings raise inside test 1 (key `test-1`). `test-2` kept: three unpadded tables raise `IndexError` there. |
| 8 | fixed | No first column (three codings) gives 1 at test 1; adding 1 on a match (three codings) gives 5. Also added: insert and delete only gives 3 at test 1 (three codings, $5 + 4 - 2 \times 3$), so the line names it. `test-3` kept (three codings). |
| 9 | fixed | Missing neighbour as 0, wrapped index and a 0-padded table give 6 at test 1. Also added: leaving out the start fee gives 9 at test 1 (three codings). `test-2` and `test-7` kept as descriptions: none of the 14 codings tried fails either first. |
| 10 | fixed | $0.55^3 = 0.166375$; times 0.45 is 0.0749; times 4 is 0.2995. |
| 11 | fixed | The chance of no 6 in n rolls is $(5/6)^n > 0$; exact fractions give $V_n \le 6 - (5/6)^n$ for n = 1 to 79. |
| 12 | fixed | Ferguson ch. 2: after the first r − 1, take the first candidate better than all seen so far. |
| 13 | fixed | Exact optimum by cutoff: 1/2 at n = 2 and 3, 0.4583 at 4, 0.3987 at 10, above 1/e and non-increasing for n = 1 to 60. |
| 14 | fixed | Rounding risk up makes the rounded total at least the true total, so a plan within 200 units is within £2,000,000. Trades (5,001, 5,001, 9,999) with profits 10, 10, 11 and budget 10,002 drop from 20 to 11 when rounded up to units of 5,000. |

Mutants: 77 entries over all 9 level 4 code widgets, each first failing the test its `byKey` line names (`grade-all --code`: 0 failures; 9 are `timeout: true`, checked at 5 times the limit). Kept lines with no mutant: l16 `screens[7]` `test-2` and `test-7`, homework `items[5]` `test-5`; each describes its test, and none of the codings tried reaches it first. Not changed: homework `items[0]` slip `ratio` (value 3, no line; packing by value per kg gives the key, 7), left for the author.

Gates: validator 0 errors; voice scan 35 on the five files, 0 and 0; concepts script exit 0, 161 checks, none re-pointed; `run-number-scripts --only graphs-dp` 3 of 3 passed; `grade-all --code` on the five files, 0 failures; playthrough of l14 to l17 and `homework-4`, desktop and `--mobile`, all passed. Files: `l14-knapsack`, `l15-common-subsequence`, `l16-grid-paths`, `l17-dice-stopping`, `homework-4`.

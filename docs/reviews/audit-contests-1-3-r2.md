# Concept audit, round 2: contests levels 1 to 3

Blind audit of `app/content/courses/contests/` at e69cac72, after round 1's fixes merged: lessons l1 to l12, `review-1` to `review-3`, `homework-1` to `homework-3` (the course has no `problems-*` files for these levels). Auditor brief: `docs/briefs/concept-audit.md`. The ledger and the findings below were written before any earlier review, audit, author report or earlier script of this course was opened.

- Ledger: `docs/reports/audit-contests-1-3-r2-ledger.md`, 2,686 rows: correct 2,680, wrong 2, imprecise 4, misleading 0, unverified 0. Finding 5 covers two rows.
- Script: `docs/reports/contests-L1-3-concepts-r2.py`. Part A has 103 checks. Part B grades 107 codings against the `test-N` lines.
- Content, engine and state files are unchanged.

## Verdict

Five findings, all minor: 2 wrong, 3 imprecise, 0 misleading. No definition, theorem, method, convention or graded key is wrong. Every graded key and every numeric slip gives the value its feedback names.

## Findings

1. l3-fast-io.json | `screens[8].feedback.byKey.test-7` | wrong, minor | The line blames a list: "A list gives a new iterator each time." A list cannot reach test 7. | Under the page's Pyodide, `[int(x) for x in data.split()]` and `list(map(int, data.split()))` both stop at test 6 with `TypeError: 'list' object is not an iterator`. Test 6 has its own line, which names the list correctly. Test 7 is reached only by an object that has `__next__` but whose `__iter__` returns something else; the script's class coding stops there. Basis: Python docs, Iterator Types (`iterator.__iter__` returns the iterator itself); sweep in script part B. | Replace the line with: "Test 7 checks `iter(it) is it`. An iterator's `__iter__` must return the iterator itself: return `map(...)` or a generator, not your own class."

2. l9-constructive.json | `screens[1].widget.options[2].why` (option `odd`) | wrong, minor | "For $n = 5$, 2 4 1 3 5 has gaps 2, 3 and 2." Five numbers have four neighbouring gaps. | $|2-4| = 2$, $|4-1| = 3$, $|1-3| = 2$, $|3-5| = 2$. The lesson's own quiz (`q-not-valid`, option `eo`) gives "gaps 2, 3, 2 and 2" for the same order. Basis: derivation, script part A. | Replace with: "You looked at the parity of $n$. For $n = 5$, 2 4 1 3 5 has gaps 2, 3, 2 and 2."

3. l12-difference-arrays.json | `screens[5].explain.text` | imprecise, minor | "A stress test against a brute force, as in lesson 4, finds it on the first random case almost every time." The first case shows the bug well under nine times in ten. | The missing $-v$ shows only when some update ends before the last day. Simulated with 20,000 small cases per generator (script part A): the first case shows it 59% of the time for $n$ from 1 to 6 with up to 4 updates, 69% for $n$ to 8 with up to 5, and 84% for $n$ from 2 to 10 with up to 6. Within five cases it shows over 98% of the time. | Replace the last sentence with: "A stress test against a brute force, as in lesson 4, finds it within the first few random cases."

4. l4-stress-testing.json | `quiz[1].widget.options[2].why` (option `time`) | imprecise, minor | "That changes the cases every run, which is why you lost this one." The stem says the run used `random.Random(4)`, so this case is not lost. The correct option says so. | The reason given contradicts the item's own key. A time seed is what would lose a case. Basis: Python docs, `random.Random(seed)` repeats its sequence. | Replace with: "That changes the cases every run, so a failing case could never be found again."

5. l6-gcd-and-primes.json | `summary.ideas[1]` and `screens[8].hints[2].text` | imprecise, minor | "A composite $n$ has a divisor at most $\sqrt n$." As written, 1 is such a divisor of every $n$, prime or not. The bound that lets trial division stop is on a divisor above 1. | Hardy and Wright, *An Introduction to the Theory of Numbers*, section 1.4: a composite $n$ has a prime factor not exceeding $\sqrt n$. The numeric widget's `accept` line states it correctly with $n = de$, $d \le e$. | `summary.ideas[1]`: "A composite $n$ has a divisor above 1 and at most $\sqrt n$, so trial division and factorising stop there." `screens[8].hints[2].text`: "A composite $n$ has a divisor $d$ with $1 < d \le \sqrt n$, and $\lfloor \sqrt{1{,}000{,}003} \rfloor = 1000$."

## The test-N sweep

All 98 `feedback.byKey.test-N` lines in levels 1 to 3 were swept: 94 on Python widgets, 4 on the C++ widget l3 `screens[10]`. For each line that names a mistake, two or three natural codings were submitted through `app/tools/code-runner.mjs` under Pyodide 0.27.7, with the page's limits and its recursion limit of 3,000. 107 codings in all; the keys are in the script (`OTHER` holds every coding whose first failing test is not the line probed).

- 1 line is wrong: finding 1.
- 82 lines are reached by at least one natural coding of the mistake they name.
- 15 lines only describe their test and name no mistake. Each statement was recomputed and is true. I found no natural coding that stops there first: l2 `screens[9]` test-7; l3 `screens[10]` test-4 and test-6; l4 `screens[8]` test-1; l9 `screens[8]` test-8; l10 `screens[4]` test-6 and test-7; l10 `screens[8]` test-5 and test-7; l11 `screens[3]` test-5; l12 `screens[4]` test-2; review-3 `items[1]` test-9; homework-1 `items[1]` test-8; homework-3 `items[2]` test-4 and test-10.

Timing-dependent lines. These hold because a test is stopped at the 5 s limit under Pyodide; each was confirmed stopped under node Pyodide here, one worker at a time: l1 `screens[9]` test-7 and `screens[10]` test-9; l2 `screens[9]` test-15 and `screens[10]` test-9; l9 `screens[5]` test-8 and `screens[8]` test-9; l10 `screens[4]` test-8 and `screens[6]` test-7; l12 `screens[4]` test-8 and `screens[7]` test-7; homework-1 `items[0]` test-10 and test-11, `items[1]` test-11, `items[2]` test-6; homework-3 `items[0]` test-9, `items[1]` test-8, `items[2]` test-8 (25 s limit). Margins seen: `2 ** n` without a guard takes 0.45 s at $n = 10^8$ (tests 13 and 14 pass) and is stopped only at $10^{18}$, as the line says. The positions-list coding of homework-1 takes 0.96 s on test 10 and is stopped on test 11, as its line says.

C++. `clang++ -m32` has no headers in this container. The three codings of l3 `screens[10]` were compiled natively (x86-64, `-O1 -fwrapv -fno-exceptions`), where `int` is 4 bytes as on wasm32. A `long` sum, 4 bytes on wasm32, was modelled with `int32_t`: it fails test 3 as an `int` sum does, and the line's advice, `long long`, is right for it.

## Notes (no verdict change)

1. l2 `screens[9]`: a solution that uses the table's cut-offs throughout (20, 500, 5,000) first fails test 3, $n = 26$, which has no line, so it gets the generic feedback. The test-6 line is reached by a solution that checks $2^n$ exactly and keeps 500 for the cubic. An optional `test-3` line: "Test 3 has $n = 26$: $2^{26} \approx 6.7 \cdot 10^7$ fits, so the answer is `"2^n"`. Compute the step count; the table's 20 is a rule of thumb."
2. l3 `screens[9]` test-4 is hedged ("reading lines may not"). `input()`, `sys.stdin.readline()` and `read().split('\n')` by index all pass test 4 and stop at test 5. A reader that strips the newline with `line[:-1]` stops at test 4.
3. l4 `screens[7]`: calling `gen` twice per trial stops at test 1, which has no line. A new `random.Random(seed)` per trial stops at test 2, as its line says.
4. l10 `screens[8]`: the prose asks for "the first one if tied", but a solution that keeps the last of the tied smallest (`<=`) passes all 7 tests. No hidden test has a tie. This is a test gap, not a concept error.
5. Timings stated in the text were re-measured here and agree in size. C++ on $10^6$ numbers: 0.78 s, 0.11 s and 0.46 s (text: 0.86, 0.12, 0.54). CPython reading $2 \cdot 10^5$ lines: about 0.12 s and 0.03 s (text: 0.14, 0.04). Printing $10^5$ lines: 0.12 s, 0.06 s, 0.01 s (text: 0.17, 0.08, 0.01). Under node Pyodide: l2 test 9 in 0.37 s, sieve to $2 \cdot 10^6$ in 0.34 s from $p^2$ and 0.38 s from $2p$, `build_tables` to $10^6$ in 0.49 s and 3.8 s with one `pow` per entry, `math.comb` per query stopped at test 6.
6. `tools/code-runner.mjs` cannot run the pytest widget l4 `screens[8]` in node (see the inbox bullet). Its four codings and its solution were graded with real pytest 9.2.0 in CPython, using the widget's own prelude and postlude.

## Overlap with earlier reads

The ledger and the five findings above were written first. Then these were read: `docs/reviews/review-contests-1-2.md`, `docs/reviews/review-contests-3-4.md` (levels 1 to 3 only), `docs/reviews/audit-contests-1-3.md` with its fix pass, fix-pass read and follow-up, and the round 1 ledger and script. No verdict, finding or fix text changed afterwards. Nothing was committed before that reading, so the order rests on this statement.

| Conceptual findings (wrong, misleading, imprecise) | Count | Which |
|---|---|---|
| By this audit only | 5 | findings 1 to 5 |
| By earlier reads only | 47 | review-contests-1-2 findings 1 to 14; review-contests-3-4 findings 1, 2, 3, 4, 5, 7 and 10; round 1 audit findings 1 to 22; the 4 imprecise rows of round 1's fix-pass read |
| By both | 0 | |

Notes on the comparison.

- All 47 earlier findings were fixed before this read. Each fixed text was a ledger row here and 46 were judged correct. Round 1's 13 `test-N` fixes hold under the page's Pyodide: every line they rewrote or added is now reached by the mistake it names, or only describes its test.
- Finding 3 is the one exception, and it is a fix-pass sentence. review-contests-3-4 finding 7 replaced "finds it in one trial" with "finds it on the first random case almost every time". Round 1's audit judged the new sentence correct. The simulation puts it at 59% to 84%. The earlier read named a certainty; this one names an overstated frequency, so it is counted as new.
- Finding 1 is a row round 1 judged correct with the same evidence: its ledger says a class with `__next__` lands at test 7 and "a plain list stops at test 6". Round 1 read "A list gives a new iterator each time" as a contrast that explains the check. I read it as the diagnosis a learner takes from a feedback line. Each sentence of the line is true on its own; the verdict turns on that reading. If the coordinator takes round 1's reading, finding 1 is `misleading` or `correct`, and the count of new `wrong` is 1.
- Findings 2, 4 and 5 are sentences no earlier read gave its own row. Round 1's ledger had 465 rows, grouped by screen; this one has 2,686, one per leaf.
- New `wrong` that no earlier read found: 2 (findings 1 and 2), both minor, over three levels. Under the convergence rule that is one more than a close allows, so the course needs another round after the fix pass, unless finding 1 is read as round 1 read it.

## For the fix pass

- The engine already has the check this class needs: a `mutants` list on a code widget (AUTHORING, engine pass 7 package 1) asserts that a wrong source first fails test N. No level 1 to 3 widget carries one. The codings in the script's part B are ready to paste as mutants, with `timeout: true` for the 22 listed in `TIMING`.
- The pytest widget l4 `screens[8]` cannot take mutants until the node runner can run it (inbox).

## Inbox

Written to `docs/BACKLOG-INBOX.md` under "Raised later (audit contests):".

- `tools/code-runner.mjs`, and so `grade-all.mjs --code`, cannot run the pytest widget l4 `screens[8]` in node 22: Pyodide dies with a fatal `fd` error inside `pytest.main`, the solution is reported as `solution-fails`, and the worker stays dead for the next widget.
- No validator warning ties a `byKey.test-N` line that names a mistake to a `mutants` entry for N.

## Checks run

- Validator: `cd app && node tools/validate.mjs`: 0 errors, 4,606 warnings.
- Number scripts: `node tools/run-number-scripts.mjs --only contests`: 5 of 436 scripts, 5 passed, 0 new failures.
- `node tools/grade-all.mjs` on the 18 files: 168 widgets, 0 failures (keys, bands and slip routing).
- `docs/reports/contests-L1-3-concepts-r2.py --cxx --pkgs <pkgs>`: 213 checks, exit 1, with 3 failing checks, which are findings 1, 2 and 3. The other 210 pass. Without `--pkgs` it runs part B in CPython and skips the 22 timing codings: 191 checks, the same 3 fail, exit 1. Findings 4 and 5 are wording and have no check.
- No playthrough: content is unchanged.

## Fix pass

Opus fixer, on 5847cb4c. Each fix was established before the audit's suggested text was compared; no key, slip, tolerance, solution or hidden test changed.

| # | File, location | Status | Basis (own) |
|---|---|---|---|
| 1 | l3 `screens[8].feedback.byKey.test-7` | fixed differently | Graded under the page's Pyodide (code-runner, 1 worker): four natural codings of a hand-made iterator stop first at test 7 (a class whose `__iter__` returns `iter(self.vals)`; one whose `__iter__` is a generator; a `list` subclass with `__next__`; one whose `__iter__` returns a new `map`). The list comprehension and `list(map(...))` stop at test 6; `iter(list)` and a class returning `self` pass. So the line now names the class mistake and the remedy: "Test 7 checks `iter(it) is it`. Your object has `__next__`, but an iterator's `__iter__` must `return self`. Or return `map(...)`, which already does." The audit's "not your own class" was not used: a class whose `__iter__` returns `self` passes. |
| 2 | l9 `screens[1].widget.options[2].why` (`odd`) | fixed | $|2-4|, |4-1|, |1-3|, |3-5| = 2, 3, 2, 2$: five numbers, four gaps. Now "gaps 2, 3, 2 and 2". |
| 3 | l12 `screens[5].explain.text` | fixed differently | Own simulation, 20,000 cases per generator, signed and unsigned $v$, $n$ from 1: the first case shows the missing $-v$ 44% to 83% of the time; within ten cases at least 99.7% in every generator tried (worst: $n \le 6$, 0 to 4 updates, $v$ in $-5..5$). Now "finds it within ten random cases almost every time". The run is in the concepts script part A. |
| 4 | l4 `quiz[1].widget.options[2].why` (`time`) | fixed differently | `random.Random(4)` repeats its sequence (Python docs, `random`: a seeded generator is reproducible), so the stem's case is not lost; a time seed would give new cases. Now "A new seed gives new cases, so this one would not come back. Seed 4 makes it again." |
| 5 | l6 `summary.ideas[1]`, `screens[8].hints[2].text` | fixed | If $n = de$ with $1 < d \le e < n$, then $d^2 \le de = n$, so $2 \le d \le \sqrt n$; checked for every composite up to 5,000 in the script. Both rows now read "a divisor $d$ with $2 \le d \le \sqrt n$". |

Mutants. l3 `screens[8].widget.mutants` now holds three entries: the `iter(self.vals)` class and the `list` subclass (test 7) and the list comprehension (test 6). `grade-all --code` confirms each first fails its test.

Scripts re-pointed (said so in their docstrings). `docs/reports/contests-L1-3-concepts-r2.py`: the `list(map(...))` coding is now probed against the test-6 line, not an OTHER "finding" at test 7; the "> 90% on the first case" check is now "> 99% within ten"; text checks added for findings 1, 4 and 5, and the fixer's simulation added. `docs/reports/contests-L3-numbers.py` (round 1's finding 7 lookup) now looks up the new l12 phrase.

Checks: validator 0 errors (4,606 warnings, as before); voice scan 35 on the five lessons 0 and 0; concepts script `--cxx --pkgs`: 219 checks, 0 failed, exit 0; `run-number-scripts --only contests`: 5 of 5 passed; `grade-all --code --file` on each edited lesson: 0 failures, except l4's two on the pytest widget `screens[8]`, which the original l4 at 5847cb4c also gives (the node runner limit in this audit's inbox); playthrough of l3, l4, l6, l9 and l12 desktop and `--mobile`: all passed.

## Fix-pass read

Fresh reader, blind to this file, the earlier contests reviews and the concepts script until the rows below were written. Diff read: `git show 15f568f7 -- app/content/courses` at HEAD `24ae7389`. Script: `docs/reports/contests-L1-3-fixread-r2.py` (exit 0). Code runs: the page's harness and worker grader under the local Pyodide 0.27.7, through `tools/code-runner.mjs`.

| # | File | JSON path | Claim | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l3-fast-io | screens[8].feedback.byKey.test-7, sentence 1 | Test 7 checks `iter(it) is it` | correct | tests[6].call is `(lambda it: iter(it) is it)(read_tokens(b'1 2'))`, expecting True. |
| 2 | l3-fast-io | same, sentence 2 | A submission that first fails test 7 has `__next__`; an iterator's `__iter__` must `return self` | correct | Python docs, Library "Iterator Types": `iterator.__iter__()` returns the iterator object itself. Test 6 (`next(...)`) passed, so the type has `__next__`. Five codings submitted: `__iter__` returns `iter(self.v)`; `__iter__` written as a generator; a list subclass with `__next__`; `__next__` with `__getitem__` and no `__iter__`; `__iter__` returns a fresh copy. All five first fail test 7 with actual False. With `return self` the class passes all 10. `__next__` alone first fails test 1 (not iterable), so it never sees this line. |
| 3 | l3-fast-io | same, sentence 3 | `map(...)` already returns itself from `__iter__` | correct | The solution `map(int, data.split())` passes test 7; `iter(m) is m` for a map object (same docs section). `iter([...])` and a generator function also pass all 10. |
| 4 | l3-fast-io | screens[8].widget.mutants[0] | `__iter__` returns `iter(self.vals)`: first fails test 7 | correct | Run: key `test-7`, actual False; tests 1 to 6 pass. The symptom text matches the source. |
| 5 | l3-fast-io | screens[8].widget.mutants[1] | A list subclass with `__next__`: `iter` gives a list iterator; first fails test 7 | correct | Run: key `test-7`, actual False. `list.__iter__` is inherited and returns a `list_iterator`. |
| 6 | l3-fast-io | screens[8].widget.mutants[2] | Returning a list: `next` raises TypeError; first fails test 6 | correct | Run: key `test-6`, `TypeError: 'list' object is not an iterator`. A tuple does the same. `grade-all.mjs --code --file` on the lesson: 0 failures. |
| 7 | l4-stress-testing | quiz[1].widget.options[time].why | A new seed gives new cases, so the lost case would not come back; seed 4 makes it again | correct | Python docs, `random.seed`: the same seed gives the same sequence. Script: seed 4 replays its 50 cases; none of 2,000 other seeds repeats them (the lesson's own `gen_pairs`). |
| 8 | l6-gcd-and-primes | screens[8].hints[2] (step) | A composite $n$ has a divisor $d$ with $2 \le d \le \sqrt n$; $\lfloor \sqrt{1{,}000{,}003} \rfloor = 1000$ | correct | $n = ab$ with $2 \le a \le b$ gives $a^2 \le n$ (Hardy and Wright, ch. 1). $1000^2 = 1{,}000{,}000 \le 1{,}000{,}003 < 1{,}002{,}001 = 1001^2$. Script checks every $n$ to 200,000. The lower bound is needed: $d = 1$ divides a prime. |
| 9 | l6-gcd-and-primes | summary.ideas[1] | Same bound, so trial division and factorising stop there | correct | Same derivation; factorising applies it to the remaining cofactor, as the lesson's code does. |
| 10 | l9-constructive | screens[1].widget.options[odd].why | For $n = 5$, 2 4 1 3 5 has gaps 2, 3, 2 and 2 | correct | Recount: $|2-4| = 2$, $|4-1| = 3$, $|1-3| = 2$, $|3-5| = 2$. Four gaps for five numbers, none equal to 1. |
| 11 | l12-difference-arrays | screens[5].explain.text, sentence 3 | A stress test against a brute force finds the missing $-v$ within ten random cases almost every time | correct | Monte Carlo, 20,000 seeded runs per generator, updates drawn as the lesson's hidden tests draw them ($l$ uniform, $r$ uniform on $[l, n-1]$, $v$ uniform). Within ten: 1.0000 ($n$ 1 to 6, up to 6 updates), 0.9999 ($n$ 1 to 8, up to 5), 1.0000 ($n$ and updates up to 10), 0.9990 ($n$ up to 5, up to 3 updates), 0.9553 for a tiny generator ($n$ up to 3, up to 2 updates). First-case rates are 0.63, 0.66, 0.79, 0.49 and 0.27, so the old "first random case" wording was false and the new one holds. |

Counts: 11 rows; correct 11, wrong 0, imprecise 0, misleading 0, unverified 0.

Fixes: none needed.

Checks run: `node tools/grade-all.mjs --code --file content/courses/contests/l3-fast-io.json --local-cdn <pkgs>`: 2 Python code widgets run, 0 failures. `docs/reports/contests-L1-3-fixread-r2.py`: exit 0.

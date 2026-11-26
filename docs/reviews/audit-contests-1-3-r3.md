# Concept audit, round 3: contests levels 1 to 3

Auditor: fresh reader, blind to every earlier review, audit, fix pass and author report of this course until the ledger and the findings below were written. Brief: `docs/briefs/concept-audit.md`, "Auditor brief (binding)". Content at commit `64887c8e`.

Scope: `app/content/courses/contests/` lessons `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3` (levels 1 to 3 have no `problems-*` files). Topic 2.4, Stage 2, so the ledger is full depth.

- Ledger: `docs/reports/audit-contests-1-3-r3-ledger.md`, 378 rows: correct 372, wrong 1, imprecise 5, misleading 0, unverified 0.
- Script: `docs/reports/contests-L1-3-concepts-r3.py`, 485 checks. It exits 1 today: the five failing checks are findings 1 to 5 and nothing else fails.
- Findings: 5. Wrong 1 (minor), imprecise 4 (minor), misleading 0. Serious 0, minor 5.

## Method

1. Every string of the 18 files was read once and each claim checked against a named source, a derivation or the script. The script uses reference code written for this audit, not the content's solutions: extended Euclid for inverses, a DP for interval scheduling, a heap for rooms, a knapsack and a ways-per-sum count for the mask screens, the divisor sum $\sum_{d \mid n} d\,\varphi(n/d)$ for the gcd sum, a mirror-image greedy for the alerts. Every hidden-test expectation of every Python function widget is recomputed that way.
2. Empirical claims have Monte Carlo checks in the script: generator A finds no tie in 4 seeds of 100,000 trials (l4), and a stress test catches the missing $-v$ within ten random cases in more than 99.9% of 20,000 runs (l12).
3. Code feedback sweep, the known risk of this course. All 98 `feedback.byKey.test-N` lines of levels 1 to 3 were swept. For each line that names a mistake, two or three natural codings of that mistake were written and submitted: 180 Python submissions through the page's grader, 14 C++ programs and 12 pytest files. The line is correct only if most of them fail test N first.
   - Python: the page's own harness and worker grader through `app/tools/code-runner.mjs`, under Pyodide 0.27.7 from the local CDN, with the page's limits (5 s a case plus budgets, recursion limit 3000).
   - The pytest widget, l4 `screens[8]`: real pytest 8 in CPython 3.13 (the venv), with the widget's prelude, the candidate and the postlude in one namespace. It cannot run in node (Pyodide `fd` error).
   - C++ (l3 `screens[10]`, l5 `screens[8]`, and every C++ claim in the prose): YoWASP clang 21.1.4 from the local CDN, run in node, target wasm32-wasi, `-std=c++17 -O1 -fno-exceptions`, the program then run under `node:wasi` on each hidden input. A probe printed `sizeof` int, long, long long and pointer as 4, 4, 8, 4, `-3 % 7` as $-3$, `x & (x - 1) == 0` for 8 as 0 and `mask & 1 << i == 0` for 5, 1 as 0.
4. Timing-dependent lines are recorded as such in the ledger and listed below. This machine ran the page's Pyodide about 1.4 times slower than the figures quoted in the content, so orderings and ratios were checked, not absolute times.

## Findings

1. `l3-fast-io.json` | `quiz[2].feedback.byKey.lines` | wrong, minor | The slip is 2 for the text `"2\n\n5 -3"`. The line says "You counted words on the first line only, or lines with text". The first line is `2`, one word, so the first named mistake gives 1, not 2. | Script check "FINDING 1": words on the first line 1, lines with text 2, words on the last line 2. A slip's feedback must name a mistake that gives that slip's value. | Replace the line with: `You counted the lines with text, or only the two numbers on the last line. Count every number.`

2. `l2-limits-to-complexity.json` | `screens[2].feedback.byKey.r0c1` | imprecise, minor | "Your entry for $n \le 20$ is not the slowest that fits" is shown for every entry other than $2^n$. An entry of `O(n*2^n)` is slower and fits: $20 \cdot 2^{20} \approx 2.1 \cdot 10^7$, which `screens[3].explain` itself calls "fine in C++" and l11 uses as $O(2^n n)$. The learner is told a true answer is not the slowest. | Script check "FINDING 2". Halim, *Competitive Programming 3*, sec. 1.2.3, lists $O(2^n n^2)$ for $n \le 18$ to 22. | Replace the line with: `Your entry for $n \le 20$ is not the growth meant here. $2^{20} \approx 10^6$, so trying every subset fits: enter $2^n$.` Better still, also add `"O(n*2^n)"`, `"n*2^n"`, `"O(2^n*n)"` and `"O(2^n n)"` to `screens[2].widget.rows[0][1].accept`.

3. `l2-limits-to-complexity.json` | `screens[2].feedback.byKey.r4c1` | imprecise, minor | "Your entry for $10^{18}$ is too slow" is shown for every wrong entry in that cell, including `O(1)`, which is faster. The table on `screens[8]` even reads "$\log n$: halve, or a formula". The three lines above it use the two-sided wording. | Script check "FINDING 3". | Replace the line with: `Your entry for $10^{18}$ is not the slowest that fits. You cannot even count to $10^{18}$ in time, but halving fits: $\log n$.`

4. `l6-gcd-and-primes.json` | `screens[9].widget.how` | imprecise, minor | "Trial division up to $n$ instead of $\sqrt n$ is stopped on those", where "those" are the three values near $10^{12}$. The usual loop without the square-root stop, `while n > 1`, divides $n$ down as it goes. It finishes $999983^2$ and $999983 \cdot 1000003$ after about $10^6$ turns, 0.13 s each in Pyodide, and is stopped only on the prime 999,999,999,989. A learner who reads the row will see two of the three "stopped" tests pass. | Sweep: `while n > 1` coding, tests 7 and 8 pass, test 9 stopped after 5 s; a fixed `range(2, n + 1)` loop is stopped from test 5. Script check "FINDING 4". | Replace the last sentence of `how` with: `Without the $\sqrt n$ stop the loop is stopped on the prime: it must count up to 999,999,999,989.`

5. `l12-difference-arrays.json` and `homework-3.json` | `screens[4].widget.how`, `screens[4].feedback.byKey.test-7`, `screens[4].widget.tests[6].call`; `items[1].widget.how`, `items[1].feedback.byKey.test-7`, `items[1].widget.tests[6].call` | imprecise, minor | `how` says "at most 2,500 pass" (homework: "at most 10,000 pass"), but the tests are `0 < update_reads(1000, ups) <= 2500` and `0 < reads_for(spans, ...) <= 10000`. The counting list sees only `[]` and `for`. A correct linear solution that reads through `reversed(...)` or `.copy()` registers 0 reads, fails test 7 and is told it "read the list far more than 2,500 times", which is false. The cases are uncommon, but the right-to-left stack over `reversed(closes)` is a textbook way to write spans. | Sweep: `apply_ranges` over `reversed(updates)` and over `updates.copy()`, and `spans` over `closes.copy()` and over `reversed(closes)`, all correct on every other test, all fail test 7 with `actual False`. Script check "FINDING 5". | Keep the tests (the lower bound was added so that the starter fails test 7) and make the counting list see these reads. In both preludes, inside `class _Counted(list):`, add:

   ```python
       def __reversed__(self):
           _Counted.reads += len(self)
           return list.__reversed__(self)

       def copy(self):
           _Counted.reads += len(self)
           return list.copy(self)
   ```

   Checked in CPython: `reversed(x)`, `x.copy()` and `for v in x` then each count `len(x)` reads, so the four correct codings land at 500 or 1,000 reads and pass, and "at most 2,500 pass" is true of them. If the preludes must stay as they are, change the words instead. l12 `how`: `Test 7 passes 500 updates in a list that counts its reads; from 1 to 2,500 pass.` l12 `test-7`: `Test 7 counted no reads of the updates list, or far more than 2,500. Loop over the updates once; do not scan them for each day.` homework-3 `how`: `Test 7 passes 1,000 rising closes in a list that counts its reads; from 1 to 10,000 pass.` homework-3 `test-7`: `Test 7 counted no reads of the list, or far more than 10,000. Walking back day by day on rising prices costs about $n^2 / 2$ reads.`

No finding needs a screen rewritten. Findings 1 to 4 are one sentence each; finding 5 is two prelude methods in two files.

## Code feedback sweep: result

All 98 `test-N` lines are `correct` by the rule of the brief; each has its own row in the ledger with the codings tried. Summary by widget:

| widget | lines | named mistakes that reach their line first | notes |
|---|---|---|---|
| l1 `screens[9]` parse | 4 | 4 of 4 | `pop(0)` is stopped on test 7; re-slicing the list passes in 3 s |
| l1 `screens[10]` new_highs | 4 | 4 of 4 | |
| l2 `screens[9]` budget_class | 3 | 2 of 2, 1 descriptive | unguarded `2 ** n` passes tests 13 and 14 in about 0.6 s and is stopped on test 15; a coding with every table threshold fails test 3 first and gets the generic line |
| l2 `screens[10]` pair_sums_at_most | 5 | 5 of 5 | |
| l3 `screens[8]` read_tokens | 3 | 3 of 3 | |
| l3 `screens[9]` program S | 3 | 3 of 3 | `sys.stdin.buffer` does not exist in the runner, as the prose says |
| l3 `screens[10]` program S in C++ | 4 | 2 of 2, 2 descriptive | `long` sum also fails test 3: `long` is 4 bytes on wasm32 |
| l4 `screens[7]` stress | 4 | 4 of 4 | |
| l4 `screens[8]` pytest | 4 | 4 of 4 | graded with real pytest in CPython |
| l9 `screens[5]`, `[8]` | 10 | 8 of 8, 2 descriptive | |
| l10 `screens[4]`, `[6]`, `[8]` | 11 | 9 of 9, 2 descriptive | the tie rule "first if tied" is not tested: keeping the last of equal amounts passes |
| l11 `screens[3]`, `[5]`, `[6]` | 10 | 9 of 9, 1 descriptive | a pruning recursion fails test 10 of `[5]`, not test 5, and gets the generic line |
| l12 `screens[4]`, `[7]` | 8 | 7 of 7, 1 descriptive | finding 5 |
| review-3 `items[1]` | 3 | 2 of 2, 1 descriptive | |
| homework-1 `items[0]` to `[2]` | 10 | 9 of 9, 1 descriptive | |
| homework-3 `items[0]` to `[2]` | 12 | 10 of 10, 2 descriptive | finding 5 |

The `how` claims of the widgets that have no `test-N` lines were swept the same way (l5 `power_mod`, l6 `gcd`, `sieve`, `factorise`, l7 `build_tables`, `count_queries`, l8 `can_reach`, `final_parity`, homework-2 `gcd_sum`, `smallest_k`). All hold except finding 4.

## Timing-dependent lines (recorded, not findings)

| claim | content | measured here |
|---|---|---|
| l2 `screens[2]`: $10^7$ additions | 1 s Pyodide, 0.3 s CPython | 0.98 s, 0.29 s |
| l3 `screens[0]`: 200,000 `input()` calls against one split | 0.19 and 0.06 s Pyodide; 0.14 and 0.04 s CPython | 0.25 and 0.05 s; 0.09 and 0.02 s (in-memory stdin) |
| l3 `screens[4]`: print loop, write loop, join | 0.17, 0.08, 0.01 s CPython | same order, in memory: 0.017, 0.008, 0.006 s |
| l3 `screens[5]`: g++, $10^6$ numbers | 0.86, 0.12, 0.54 s | 0.70, 0.11, 0.44 s |
| l6 `screens[7]`: per-number trial division is stopped | on the last tests | stopped on test 9; dividing by earlier primes only passes, 3.5 s on the last test |
| l7 `screens[6]`: backward loop against one `pow` per entry | 0.3 s and 3 s | 0.45 s and 3.9 s |
| l7 `screens[9]`: one `math.comb` at $n = 10^6$ | about 7 s | 10.2 s Pyodide, 5.4 s CPython |
| l11 `screens[3]`: mask loop at n = 16 and n = 20 | 0.1 s and 2.5 s | 0.15 to 0.2 s and 2.5 s |
| l11 `screens[8]`: meet in the middle, sums, n = 40 | about 2 s | 2.1 s |
| l3 `screens[10]`, l5 `screens[8]`: compiler download | about 26 MB | the package's wasm and resources gzip to 26.4 MB |

Every line of the sweep whose first failure is a "Stopped after 5 s" is marked timing-dependent in the ledger.

## Checks run

- `cd app && node tools/validate.mjs`: 0 errors, 4606 warnings.
- `cd app && node tools/run-number-scripts.mjs --only contests` (venv Python first on PATH): 5 of 436 scripts, 5 passed, 0 new failures.
- `node tools/grade-all.mjs --code --file ... --local-cdn <pkgs>` on the 17 files other than l4: 158 widgets and 35 Python code widgets, 0 failures. With l4 in the same run, the pytest widget's known `fd` error is followed by 37 false failures on other widgets (see the inbox).
- `python docs/reports/contests-L1-3-concepts-r3.py`: 485 checks, 5 failed (findings 1 to 5), exit 1. Each failing check reads the content, so it passes once its finding is fixed by any of the fixes offered.
- No playthrough, as instructed.

## Overlap with earlier reads

The ledger, the script and the five findings above were written first. Then these were read: `docs/reviews/review-contests-1-2.md`, `docs/reviews/review-contests-3-4.md` (levels 1 to 3 only), `docs/reviews/audit-contests-1-3.md` and `docs/reviews/audit-contests-1-3-r2.md` with their fix passes and fix-pass reads, the author reports `docs/reports/contests-1.md` to `contests-3.md`, and the contests rows of `docs/reports/concept-audit-log.md`. "Both" counts only a defect an earlier read named.

| Conceptual findings (wrong, misleading, imprecise) | Count | Which |
|---|---|---|
| By this audit only | 5 | findings 1 to 5 |
| By earlier reads only | 52 | the 47 counted by round 2 (review-contests-1-2 findings 1 to 14; review-contests-3-4 findings 1, 2, 3, 4, 5, 7 and 10; round 1 audit findings 1 to 22; the 4 imprecise rows of round 1's fix-pass read) and round 2 audit findings 1 to 5 |
| By both | 0 | |

New `wrong` in this round, found by no earlier read: 1 (finding 1, minor). Round 2's fix-pass read found none, and there is no fix pass for this round yet.

Notes on the comparison.

- All 52 earlier findings were fixed before this read. None of the five findings here is on a text that an earlier fix wrote. Round 2's five fixes hold: the l3 `screens[8]` `test-7` line and its three mutants, the l9 gap count, the l12 "within ten random cases" claim (Monte Carlo here: above 99.9%), the l4 seed option and the l6 divisor bound.
- The texts of findings 1 to 4 are the author's first wording (`git log -S`): no fix pass wrote them. Three earlier reads passed them. Findings 2 and 3 fire only for entries other than the common ones, and finding 4 only shows when a no-square-root loop is run.
- Finding 5's lower bound was added by the author on purpose (`docs/reports/contests-3.md`: the starter passed the counting tests with 0 reads). The side effect on correct solutions was not noticed.
- Round 2's notes 1, 3 and 4 (the table-threshold coding of l2 `screens[9]`, `gen` called twice in l4 `screens[7]`, the untested tie rule of l10 `screens[8]`) were seen again here, independently, with the same results. They remain notes, not findings.
- Three rounds on levels 1 to 3: 13, 2 and 1 new `wrong`, all minor feedback lines. The one left in this round is a quiz slip line, not a `test-N` line.

## Inbox bullets

Added to `docs/BACKLOG-INBOX.md` under "Raised later (audit contests):".

- (round 3, levels 1 to 3) The counting list `_Counted` in the preludes of contests l2 `screens[10]`, l12 `screens[4]`, homework-1 `items[0]` and `[1]` and homework-3 `items[1]` counts only `[]` and `for`. `reversed(xs)`, `xs.copy()`, `xs.count()` and `xs.index()` read the list without being counted. Where the test also has a lower bound (`0 < reads`), a correct solution is refused (finding 5). One shared counted-list helper for preludes, overriding `__reversed__`, `copy`, `count` and `index` as well, would end the class.
- (round 3, levels 1 to 3) `grade-all.mjs --code` skips C++ code widgets. YoWASP clang 21 runs in node as shipped (`gen/bundle.js`, `runClang`) and its `main.wasm` runs under `node:wasi`; this audit graded l3 `screens[10]` and l5 `screens[8]` that way with a 40-line script (first compile about 15 s). A `tools/cpp-runner.mjs` beside `code-runner.mjs` would bring C++ solutions, starters and `mutants` under `grade-all`.
- (round 3, levels 1 to 3) Second vote for the dead-worker bullet below (pytest widget, `fd` error): in one 18-file `grade-all --code` run the fatal error in l4 `screens[8]` was followed by 37 false `solution-fails` and `examples-fail` lines on 18 other widgets. The runner should replace a worker after a Pyodide fatal error.

## Fix pass

Fixer: Opus, on `df08dc20`. Each fix was established by an own run or derivation before the edit. No key, accept list, solution, hidden test or prelude was changed.

| # | status | basis (own) | edit |
|---|---|---|---|
| 1 | fixed | `"2\n\n5 -3"`: lines with text are `2` and `5 -3`, 2; words on the last line, `5` and `-3`, 2; words on the first line 1. Both named mistakes now give the slip's value 2, clear of the key 3 and the slip 4. Slip value unchanged. | l3 `quiz[2].feedback.byKey.lines`: "You counted the lines with text, or only the numbers on the last line. Count every number." |
| 2 | fixed | $20 \cdot 2^{20} = 20{,}971{,}520 < 10^8$, so `O(n*2^n)` fits and is slower than $2^n$; the old line was false for it. The line now says the entry is not the growth meant and names $2^n$, true for every wrong entry. Widening the accept list was not done (keys unchanged); left to the orchestrator. | l2 `screens[2].feedback.byKey.r0c1` |
| 3 | fixed | `O(1)` fits and is faster than $\log n$, so "too slow" was false for it. "Not the slowest that fits" is true both for a faster entry and for one that does not fit, as in rows 1 and 2. | l2 `screens[2].feedback.byKey.r4c1` |
| 4 | fixed | CPython run of the `while n > 1` loop with no square-root stop: $999983^2$ and $999983 \cdot 1000003$ finish in about $10^6$ turns, 0.05 s each; on the prime 999,999,999,989 it needs about $10^{12}$ turns. All three numbers checked prime (sympy and trial division). A fixed `range(2, n + 1)` loop is stopped earlier, so "stopped on it" holds for both codings. | l6 `screens[9].widget.how`, last sentence: "Without the $\sqrt n$ stop the loop must count up to that last prime and is stopped on it." |
| 5 | fixed differently | Own run in CPython with the widgets' own preludes: `apply_ranges` over `reversed(updates)` and over `updates.copy()`, `spans` by a right-to-left stack over `reversed(closes)` and over `closes.copy()`, pass every other test and register 0 reads, so fail test 7; the plain `for` and index codings register 500 and 1,998 reads and pass; the naive codings register 500,000 and 999,000. The harness is part of the hidden tests and stays; the words were made true instead. The harness limit is already in `docs/BACKLOG-INBOX.md` (round 3 bullet on `_Counted`); only these two widgets have the `0 <` lower bound. | l12 `screens[4]` and homework-3 `items[1]`: `how` now reads "from 1 to N pass. It counts indexing and `for` loops over the list, not reads through `reversed()` or `.copy()`."; `test-7` now opens "Test 7 counted no reads of the ... list, or far more than N. Reads through `reversed()` or `.copy()` are not counted." |

Script: `docs/reports/contests-L1-3-concepts-r3.py` exits 0, 485 checks. No check was re-pointed; the FINDING 5 check was widened to also require the new `how` and `test-7` wording (noted in its docstring).

Gates on the five edited files: validator 0 errors, no warning on an edited field; voice scan 35: 0 and 0; `run-number-scripts --only contests` 5 of 5 pass; `grade-all --code --file` 0 failures on each of the five; playthrough desktop and `--mobile` of each, results below.

Playthrough, `--local-cdn`: l3, l2, l6 and l12 with `--lesson`, homework-3 with `--set`, each desktop and `--mobile`: all passed (10 runs). Content commit for the fix-pass read: `ce87d1b0`.

## Fix-pass read

Fresh reader, blind to this audit and to the earlier contests reviews and scripts. Diff read: `git show ce87d1b0 -- app/content/courses` at HEAD 542cf515. Script: `docs/reports/contests-L1-3-fixread-r3.py` (exit 0; imprecise rows print as `note`). Pyodide runs through `app/tools/code-runner.mjs` (`makeRunner().grade(spec, src, 'tests')`, local CDN), keys as the page gives them.

| # | File | JSON path | Claim (new or changed sentence) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l3-fast-io | quiz[2].feedback.byKey.lines | Slip 2 is "the lines with text, or only the numbers on the last line" | correct | Text `"2\n\n5 -3"`: lines with text are `2` and `5 -3`, so 2; last line holds 5 and −3, so 2. The old "words on the first line only" gave 1. Script. |
| 2 | l2-limits-to-complexity | screens[2].feedback.byKey.r0c1, sentence 1 | A miss on $n \le 20$ "is not the growth meant here" | correct | True of any entry the key refuses; no longer claims the key is the slowest that fits (see open point). |
| 3 | l2-limits-to-complexity | screens[2].feedback.byKey.r0c1, sentence 2 | $2^{20} \approx 10^6$, every subset fits, enter $2^n$ | correct | $2^{20} = 1{,}048{,}576 \le 10^8$. |
| 4 | l2-limits-to-complexity | screens[2].feedback.byKey.r4c1, sentence 1 | A miss on $10^{18}$ "is not the slowest that fits" | imprecise | $\log n$ is not the slowest that fits $10^8$: $\sqrt[3]{n} = 10^6$ and $\log^2 n \approx 3{,}600$ steps both fit and grow faster. A learner who enters `O(n^(1/3))` is told something false. Same class as the open point. |
| 5 | l2-limits-to-complexity | screens[2].feedback.byKey.r4c1, sentence 2 | Counting to $10^{18}$ does not fit; halving does | correct | $10^{18} > 10^8$; $\log_2 10^{18} = 59.8$. |
| 6 | l6-gcd-and-primes | screens[9].widget.how, last sentence | Without the $\sqrt n$ stop the loop counts up to 999,999,999,989 and is stopped on it | correct | Pyodide: `while d <= n` and `while n > 1` variants both give key `test-9`, "Stopped after 5 s"; tests 7 and 8 pass (largest factor about $10^6$, since $n$ shrinks). All three numbers are prime (script). The old sentence said all three were stopped, which was false. |
| 7 | l12-difference-arrays | screens[4].widget.how | Test 7: 500 updates, "from 1 to 2,500 pass" | correct | Test call is `0 < update_reads(1000, ups) <= 2500`; solution reads 500. |
| 8 | l12-difference-arrays | screens[4].widget.how | Counts indexing and `for` loops, not `reversed()` or `.copy()` | correct | `_Counted` overrides only `__getitem__` and `__iter__`. Pyodide: index loop and `for` loop pass; correct solutions with `reversed(updates)` and `updates.copy()` give key `test-7`, actual `False` (0 reads). Not exhaustive, and does not claim to be: `pop()` is also uncounted, `list()`, `sorted()` and a slice are counted. |
| 9 | l12-difference-arrays | screens[4].feedback.byKey.test-7, sentence 1 | Test 7 "counted no reads of the updates list, or far more than 2,500" | imprecise | True for 0 reads and for the per-day scan (500,000). False for a correct $O(n + q)$ answer just over the cap: six reads per update is 3,000, key `test-7` (Pyodide, six-pass variant). "Far" is the unstated part. |
| 10 | l12-difference-arrays | screens[4].feedback.byKey.test-7, sentence 2 | Reads through `reversed()` or `.copy()` are not counted | correct | As row 8; this is the line a learner with a correct `reversed()` answer sees, and it names the cause. |
| 11 | homework-3 | items[1].widget.how | Test 7: 1,000 rising closes, "from 1 to 10,000 pass" | correct | Test call is `0 < reads_for(spans, list(range(1000))) <= 10000`; solution passes. |
| 12 | homework-3 | items[1].widget.how | Counts indexing and `for` loops, not `reversed()` or `.copy()` | correct | Same class. Pyodide: correct stack solutions that start `xs = closes.copy()` or loop `for c in reversed(closes)` give key `test-7`, actual `False`; `list(closes)`, `closes[:]` and direct indexing pass. |
| 13 | homework-3 | items[1].feedback.byKey.test-7, sentence 1 | Test 7 "counted no reads of the list, or far more than 10,000" | correct | 0 reads as row 12; the walk-back answer reads about $10^6$ times. A stack answer needs more than 10 reads per close to land just over the cap, which no reasonable one does. |
| 14 | homework-3 | items[1].feedback.byKey.test-7, sentence 2 | Reads through `reversed()` or `.copy()` are not counted | correct | As row 12. |

Counts: 14 rows; correct 12, imprecise 2, wrong 0, misleading 0, unverified 0.

The l12 and homework-3 text is true of what the learner sees: a correct `reversed()` or `.copy()` answer still fails test 7, and the new `how` and test-7 lines now say why. The harness itself still refuses those correct answers; that is an engine or test matter (count `__reversed__` and `copy`, or drop the `0 <` bound), not a wording one.

### Fixes (paste-ready)

Row 4, `l2-limits-to-complexity.json` `screens[2].feedback.byKey.r4c1`:

```
"r4c1": "Your entry for $10^{18}$ is not the growth meant here. You cannot even count to $10^{18}$ in time, but halving fits: enter $\\log n$."
```

Row 9, `l12-difference-arrays.json` `screens[4].feedback.byKey["test-7"]` (drop "far"; homework-3 may take the same edit for symmetry, with 10,000):

```
"test-7": "Test 7 counted no reads of the updates list, or more than 2,500. Reads through `reversed()` or `.copy()` are not counted. Scanning every update for each day costs $n \\cdot q$ reads."
```

### Open point: l2 screens[2], $n \le 20$ and $O(n \cdot 2^n)$

Judgement: the key is not right as the question is worded. Screens 1 and 2 set the budget at about $10^8$ steps. $20 \cdot 2^{20} = 20{,}971{,}520$ fits and grows faster than $2^n$; $n^2 \cdot 2^n = 4.2 \cdot 10^8$ does not. So "the slowest growth that still fits" $n \le 20$ is $O(n \cdot 2^n)$, and a learner who works it out is marked wrong. The same holds for two more rows: $n \le 2 \cdot 10^5$ (given as `O(n log n)`, yet $n \sqrt n = 8.9 \cdot 10^7$ fits) and $10^{18}$ (row 4 above). Only the $n^3$ and $n^2$ rows are strictly the slowest ($n^3 \log n$ and $n^2 \log n$ overshoot). The `correct` line is also false as stated: $10^6$, $3.5 \cdot 10^6$ and 60 steps do not "land near $10^8$".

The keys are the standard rule-of-thumb table (Laaksonen, *Competitive Programmer's Handbook*, ch. 2 "Estimating efficiency": $n \le 20 \to O(2^n)$, $n \le 500 \to O(n^3)$, $n \le 5000 \to O(n^2)$, large $n \to O(\log n)$; Halim, *Competitive Programming 3*, table 1.4 gives $O(2^n n)$ for $n \le 18$ to 22). So keep the keys, change what the question asks, and accept $n \cdot 2^n$. "Slowest growth" also reads two ways (a slowly growing function is the opposite of what is meant), which the new wording removes. The `explain` already speaks of "the setter's hint about the intended solution" and needs no change. Rows r1c1 and r2c1 are true as they stand.

`screens[2].question`:

```
"question": "Fill in the growth each limit usually calls for."
```

`screens[2].widget.columns`:

```
"columns": ["Constraint", "Usual growth"]
```

`screens[2].widget.rows[0][1].accept` (the table's big-O normaliser drops `O( )`, spaces and `*`, so these cover `n 2^n`, `n·2^n` and `2^n n`):

```
"accept": ["2^n", "O(2**n)", "O(n*2^n)", "O(2^n*n)"]
```

`screens[2].feedback.correct`:

```
"correct": "Each row is the growth a setter usually intends at that limit."
```

`screens[2].feedback.byKey.r0c1` (so the line still holds beside the wider accept list):

```
"r0c1": "Your entry for $n \\le 20$ is not the growth meant here. $2^{20} \\approx 10^6$, so trying every subset fits: enter $2^n$."
```

(unchanged; listed to confirm it stays true.) After the edit run `node tools/grade-all.mjs --file content/courses/contests/l2-limits-to-complexity.json` for the new accept forms.

Out of scope, noted only: homework-3 test-7 third sentence (unchanged) says the walk-back costs about $n^2 / 2$ reads; with `closes[j] <= closes[i]` it is two reads per comparison, about $n^2$ ($2 \cdot 500{,}500 = 1{,}001{,}000$ at $n = 1000$).

# Blind concept audit: first-python, levels 1 to 3 (round 1)

Scope: `app/content/courses/first-python/`, all 18 content files at commit `030096d3`: lessons `l1` to `l12`, `review-1` to `review-3`, `homework-1` to `homework-3` (the course has no `problems-*` or `fluency-*` files). Stage 0, so the ledger uses the reduced depth, with a row for every graded key, wrong option, slip, stated rule, code-behaviour claim and `test-N` line.

Read blind. The ledger and the findings below were written before any earlier read of the course was opened.

- Ledger: `docs/reports/audit-first-python-1-3-ledger.md`, 794 rows: correct 765, wrong 1, imprecise 27, misleading 1, unverified 0.
- Concepts script: `docs/reports/first-python-L1-3-concepts.py`, 795 checks.
- Test-line sweep: `docs/reports/first-python-L1-3-test-line-sweep.mjs`, 133 submissions through the page harness.

## How each kind of claim was checked

| Claim | Check |
|---|---|
| What a snippet prints or raises (93 snippets, and the scripts in the three long-form models) | Run in CPython 3.13 and inside the page's Pyodide 0.27.7 (Python 3.12.7, wasm32). The key must be the output; no wrong option may be the output. |
| Keys with no snippet in the prose (canvas code, taps, boxes, concept choices) | Recomputed one by one, concepts section A2. |
| 94 slip values and named wrong options | Recomputed from the mistake each line names, section B. |
| 12 quoted error messages | Raised and compared as text, section C. |
| 15 printed tracebacks | Each script rebuilt with its line numbers and run. Exact match, carets included, on Python 3.12.7 inside Pyodide; File lines and last line on 3.13. |
| Stated rules | Grids: 156 int pairs for `/` and `//`, every slice of a 10-character string, 1,794 counting loops for the pass formula, 372 loop-against-power cases for compounding. |
| 58 code widgets | `grade-all.mjs --code`: every solution passes, every starter fails. |
| Every `test-N` and `error` line | 133 natural codings of the named mistakes, submitted through `tools/code-runner.mjs`. No line is timing-dependent except the three "ran too long" lines, which rest on the page's 5-second limit (observed: "Stopped after 5 s on this test"). |

Nothing in the course depends on the raised recursion limit or on wasm32 sizes: it has no recursion and states no size. No item sits on a `round()` tie, so banker's rounding changes no key (2249.728, 1628.8946, 31.836, 605.0000000000001). The course never uses `is`, default arguments or string mutation.

## Findings

One `wrong`, eleven `imprecise`, one `misleading`. One is serious, twelve are minor.

1. `l1-calculator.json` | `quiz[q-floor].feedback.byKey.nearest` | **wrong, minor** | The line says "You rounded 3.33 to the nearest." The slip value is 4. 3.33 to the nearest whole number is 3, which is the right answer. A learner who typed 4 rounded up. | `round(20 / 6)` is 3; the one failing check of the concepts script. Lesson 1 itself teaches that 3.8 goes to 4 "to the nearest" (screen 4), so the same phrase now names a different mistake. | Replace with: "You rounded 3.33 up to 4. `//` rounds down. You cannot buy a fourth share with £2."

2. Thirteen files and paths below | `feedback.byKey.error` | **imprecise, minor** | Each line names a mistake that the page does not key as `error`. A runtime error or a timeout during a test fails that test and keys as `test-N`. Only code that cannot start (in practice a `SyntaxError`, or a crash at load in a function-mode widget) keys as `error`. So the learner who makes the named mistake sees the generic line instead, and two generic lines then point the wrong way (`l6` screen 6 and `homework-2` item 2 tell a learner whose loop never ends to check a start equal to the target). | Sweep, 17 submissions: in script mode (any stdout test) a `NameError`, `TypeError` or `ValueError` gives `test-1`; in function mode the `IndexError` on the empty list gives `test-4` (`l8`) and `test-2` (`review-2`), the unset `action` gives `test-3`, and each endless loop gives `test-1` or `test-2` with "Stopped after 5 s on this test". `docs/AUTHORING.md` (script mode: the code runs afresh for every case). | Move each text to the key that fires, worded as a condition because a `test-N` line shows for every failure of that test. Paste-ready:
   - `l2-naming-a-value` `screens[3]`: add `"test-1": "Test 1 expects 50.0. If the row shows `NameError`, a name is spelt differently in two places."`
   - `l4-asking-and-printing` `screens[4]`: add `"test-1": "Test 1 expects 51.0. If the row shows `ValueError`, use `float` rather than `int` for decimal text."`
   - `l4-asking-and-printing` `screens[7]`: add `"test-1": "Test 1 expects 100.0. If the row shows `TypeError`, read its last line: which value is still text?"`
   - `l4-asking-and-printing` `screens[9]`: add `"test-1": "Test 1 expects `Return: 2.80%`. A `TypeError` on the return line means a price is still text: convert with `float`."`
   - `l4-asking-and-printing` `screens[10]`: add `"test-1": "Test 1 expects 0.045, then `Interest: £90.00`. A `ValueError` means the text still has its % sign: slice it off first."`
   - `review-1` `items[6]`: add `"test-1": "Test 1 expects `Value: £6180.00`. A `TypeError` means one value is still text: convert it first."`
   - `l12-savings-script` `screens[10]`: `test-1` already covers a stopped script.
   - `l6-until-done` `screens[6]`: add `"test-1": "If the row says it stopped after 5 seconds, the loop never ends. Check that the block changes `value`, so the test can fail."`
   - `l6-until-done` `screens[9]`: add `"test-1": "If the row says it stopped after 5 seconds, the loop never ends. Check that the block changes `balance`."`
   - `l8-many-values` `screens[6]`: add `"test-4": "Test 4 passes an empty list. An `IndexError` means `values[0]` ran on it: put that line inside the length check."`
   - `review-2` `items[6]`: add `"test-2": "Test 2 passes an empty list. An `IndexError` means `pnls[0]` ran on it: put that line inside the length check."`
   - `homework-2` `items[0]`: add `"test-3": "Test 3 is a price between the stop and the target. An error naming `action` means no branch set it: add the `else`."`
   - `homework-2` `items[2]`: add `"test-2": "Test 2 has a rate of 0. If the row says it stopped after 5 seconds, the loop never ends: guard it with `rate > 0`."`
   - In all thirteen, set `"error"` to: "Your code could not start. Read the last line of the message under the editor, then the line it points to."

3. `l2-naming-a-value.json`, `l8-many-values.json` | `l2` `summary.ideas[2]`, `l2` `screens[5].explain.text`; `l8` `screens[2]`, `screens[8].prose` | **imprecise, serious** | Lesson 2 teaches assignment as copying: "A later change to a leaves b where it was" and "Changing a later never changes b." That is true only of assigning to `a` again. Screen 4 hedges once ("For numbers"); the summary and screen 5 do not. Lesson 8 then teaches changing a list in place (`append`, `closes[0] = ...`) and never says that `b = a` shares one list. A learner carries the copy rule to lists, where it is false, and no later screen of the course corrects it. | `a = [1.0]; b = a; a.append(2.0)` leaves `b` as `[1.0, 2.0]` (concepts section E, note). Python tutorial 3.1.3: "Simple assignment in Python never copies data. When you assign a list to a variable, the variable refers to the existing list." Language reference 3.1 and 7.2. | Three edits.
   - `l2` `summary.ideas[2]`: "`b = a` gives b the value a has now. Assigning to a again later leaves b where it was."
   - `l2` `screens[5].explain.text`, last sentence: "Assigning to a again later never changes b."
   - `l8` `screens[8].prose`, add after the code block: "One warning: `b = prices` does not copy a list. Both names then refer to the same list, so `prices.append(99.50)` shows through `b` too."

4. `l10-reading-errors.json` | `screens[6].feedback.byKey.test-1` | **imprecise, minor** | "Convert with `float` before adding 1.50" names the unconverted price. Two of its three natural codings never reach test 1: the starter as given and `int(price_text)` both stop on the script's own `print` line and key as `error`. The line does show when the fee is forgotten or joined as text, where "convert" is the wrong advice. | Sweep: starter gives `error`, `int` gives `error`, `price_text + "1.50"` gives `test-1`, `float(price_text)` with no fee gives `test-1`. | Replace with: "Test 1 passes the text `\"101.20\"` and expects the number 102.7. Check what your function hands back: the fee is added to a number, not joined to text."

5. `homework-1.json` | `items[4].feedback.byKey.test-1`, `items[6].feedback.byKey.test-1` | **imprecise, minor** | "If it lacks a sign, use `+.2f`" and "Check the sign format `+.2f` on both lines" name a mistake that cannot fail the test. Every graded value is negative, and for a negative value `.2f` and `+.2f` print the same text. A program with no `+` in any format passes both items, although item 4 asks for "a signed percentage". | Sweep: both no-plus programs give `pass`. `f"{-3.61:.2f}" == f"{-3.61:+.2f}"` (concepts E). | `items[4]`: "If the line reads -0.04 or -0.036, multiply by 100 before formatting. Keep `+.2f`, so a rising week would show its plus sign." `items[6]`: "Check that the return is multiplied by 100 and that both lines show two decimals. Keep `+.2f`, so a gain would show its plus sign."

6. `l12-savings-script.json` | `screens[5].widget.tests`, `screens[7].widget.tests` | **imprecise, minor** | The hidden tests accept append mode. Each test empties its file first, so `open(name, "a")` passes, and so does `open(name, "a")` inside the loop on screen 7, which is the trap of screen 6 in append form. The lesson's own quiz says a plan file is written with `"w"` because a second run in `"a"` repeats the lines. | Sweep: both append programs give `pass`. | Add one test to each that leaves a line in the file.
   - `screens[5].widget.tests`, append: `{ "call": "(open('s4.txt', 'w').write('old line\\n'), save_line('s4.txt', 1, 1050.0), open('s4.txt').read())[2]", "expect": "'Year 1: £1050.00\\n'", "compare": "equal" }`; `how`: "Check runs 4 hidden tests. Three empty a file first and one leaves a line in it. Each calls your function, then reads back what the file holds."; add `"test-4": "Test 4 writes to a file that already holds a line. Open with `\"w\"`, so the old line goes."`
   - `screens[7].widget.tests`, append: `{ "call": "(open('p5.txt', 'w').write('Year 9: old\\n'), save_plan('p5.txt', 1000.00, 0.05, 2), open('p5.txt').read().splitlines())[2]", "expect": "['Year 1: £1050.00', 'Year 2: £1102.50']", "compare": "equal" }`; `how`: "Check runs 5 hidden tests. Four empty a file first and one leaves a line in it. Each calls your function, then reads back the lines the file holds."; add `"test-5": "Test 5 writes to a file that already holds a line. Open it once with `\"w\"`, before the loop, so the old plan goes."`

7. `l5-decisions.json` | `screens[2].explain.text` | **imprecise, minor** | "An `if` line only asks whether its condition's value is `True`." An `if` runs its block for any truthy value: `if 5:`, `if "no":` and `if [0]:` all run. The course only ever writes comparisons, so no key is affected, but "only" states a rule that the next course contradicts. | Library reference, Truth Value Testing; language reference 8.1; concepts E, note. | Replace the sentence with: "An `if` line runs its block when its condition works out to `True`."

8. `l2-naming-a-value.json` | `screens[3].prose` | **imprecise, minor** | "A name starts with a letter and has no spaces." A name may also start with an underscore. | Language reference 2.3, Identifiers. | "A name starts with a letter or an underscore and has no spaces."

9. `l3-text.json` | `screens[6].widget.options[twodp].why` | **imprecise, minor** | "Python never adds digits on its own." `print(0.1 + 0.2)` shows `0.30000000000000004`. The point meant is that `print` does not pad a float with zeros. | Run; Python tutorial 15, Floating-Point Arithmetic. | "`print` shows a float with the fewest digits that pin it down: 12.5, not 12.50. And here `+` cannot join a string to a float at all."

10. `l6-until-done.json` | `screens[8].feedback.byKey.r1c1` | **imprecise, minor** | "You added £70 again" names one mistake (1140.00), but a line keyed on a cell id shows for every wrong value typed in that cell. | `app/js/engine/widgets/table.js`: a miss keys as the cell's matching `wrong[]` id, else the cell id. `docs/AUTHORING.md`, table cells: "key the slip line on the wrong id". | On the cell `rows[1][1]` add `"wrong": [{ "id": "simple", "value": 1140, "tol": { "abs": 0.01 } }]`; add `"simple": "You added £70 again. The second year's 7% is on £1,070.00, so it adds £74.90."`; set `"r1c1": "Multiply £1,070.00 by 1.07: £1,144.90."`

11. `l11-numbers-from-a-file.json` | `summary.ideas[0]` | **imprecise, minor** | "A file gives you text, one line at a time, each ending in a newline." The last line of a file need not end in one. The lesson's own test 2 on screen 2 passes `"Mon,101.20"` with none. | Python tutorial 7.2.1: the newline "is only omitted on the last line of the file if the file doesn't end in a newline". | "A file gives you text, one line at a time, usually ending in a newline. Convert with `float` before doing sums."

12. `l11-numbers-from-a-file.json` (also `l12` screen 10, `review-3` item 6, `homework-3` items 2 and 7) | `screens[3].prose` and the solutions | **misleading, minor** | Every file is read with `for line in open(name)` or `open(name).readlines()` and never closed. Lesson 12 then teaches `with` for writing and says it closes the file. The course never says that its reading form leaves the file open, so the learner takes the unclosed form as the standard way to read. The code is correct and CPython closes the file when the object is dropped, so no key changes. | Python tutorial 7.2: "It is good practice to use the `with` keyword when dealing with file objects"; without it "you should call `f.close()`". | Add to the end of `l11` `screens[3].prose`: "This short form leaves closing the file to Python. `with open(name) as f:` followed by `for line in f:` reads the same lines and closes the file; you meet `with` when you write files."

13. `l3-text.json`, `l10-reading-errors.json` | `l3` `screens[8].prose`; `l10` `summary.ideas[2]` | **imprecise, minor** | "A slice `s[a:b]` ... holds $b - a$ characters" and "A slice `[a:b]` stops before `b`, so it holds $b - a$ values" are stated without the condition. The lesson 3 summary note does give it ("when both lie inside the string"). Lesson 10 does not, and its own quiz relies on the other case: `closes[5:]` on a short list is empty. | `len("ABCDEFGHIJ"[2:15])` is 8, not 13 (concepts E, note). Python tutorial 3.1.2: out-of-range slice indexes are handled gracefully. | `l3` `screens[8].prose`: "...so it holds $b - a$ characters when both lie inside the string." `l10` `summary.ideas[2]`: "A list of $n$ values has indexes 0 to $n - 1$. A slice `[a:b]` stops before `b`, so inside the list it holds $b - a$ values."

## Checked and found right

- Every graded key, and every wrong option and slip except finding 1. In particular `-7 // 2` is −4, `"12" == 12` is `False`, `print(type(8 / 4))`, the `None` from a function that prints, `closes = closes.append(...)`, the header and blank-line `ValueError`s, `"w"` inside a loop, and the first-True rule of `elif`.
- All 15 tracebacks print exactly as Python 3.12 prints them, including the caret lines and the frame with no carets in `l10` `q-two-frames`. The `SyntaxError` text in `l5` screen 6 is the 3.12 text.
- Every `test-N` line names mistakes whose natural codings fail that test first, except findings 4 and 5: 96 of the 133 submissions are such codings and all 96 key as the line says.
- The hidden tests reject the obvious wrong programs except in finding 6. Two programs pass that the tests cannot reject by design and that are not wrong for the task: a running peak that starts at 0 (`l8` screen 9: prices are positive) and a hand-typed plus sign on a fixed positive value (`l3` screen 9).
- The finance: simple return $(p_1 - p_0)/p_0$, compound growth $B_0(1+r)^n$, doubling in 11 years at 7%, end-of-year deposits, maximum drawdown as a fraction of the running peak. Each convention is stated where it is first used.

## Validator, scripts and grading

- `node tools/validate.mjs`: 0 errors (4,618 warnings, none new: no content was edited).
- `node tools/run-number-scripts.mjs --only first-python`: 5 of 5 passed (the runner does not collect concepts scripts).
- `node tools/grade-all.mjs --code --file <each of the 18 files> --local-cdn <pkgs>`: 135 widgets and 58 Python code widgets, 0 failures.
- `python docs/reports/first-python-L1-3-concepts.py`: 795 checks, 1 failing (finding 1), 7 notes; exit 1. Same result inside Pyodide 0.27.7 with exact tracebacks.
- `node docs/reports/first-python-L1-3-test-line-sweep.mjs --local-cdn <pkgs>`: 133 submissions, 17 where a crash or timeout keys as `test-N` and not `error` (the routing fact behind finding 2; 13 of them hit the thirteen lines, 4 hit lines already worded for it in `l1` screen 9, `l11` screen 8 and `homework-3` item 8); exit 0. With `--concepts` it exits 1 for finding 1.
- No playthrough, as the brief sets.

## Overlap with the earlier read

Earlier read, opened only after the ledger and the findings above were written: `docs/reviews/review-first-python-1-3.md` (29 findings, of which 19 are conceptual: 11 `wrong`, 8 `misleading`; the other ten are voice, continuity and layout). The performance-task read (`review-perf-retrofit-14.md`, rows for `h-split-bill` and `h-contract-cost`) has no conceptual finding on this course. No earlier audit of this course exists.

| | Count | Which |
|---|---|---|
| Found by this audit only | 11 | Findings 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12 |
| Found by the earlier read only | 17 | Its findings 1 to 12, 14 to 16, 18 and 19. All 17 are fixed in the content read here, and the checks of this audit confirm each fix: `//` as rounding down, powers right to left, the 15 tracebacks with their caret lines, the 137.0 total, the `test-1` and `test-4` keys |
| Found by both | 2 | Finding 4 with its finding 13: the `test-1` line of `l10` `screens[6]`, where the fix pass moved the error half and left a line that still names the unconverted price. Finding 13 with its finding 17: the slice length without its condition, fixed there in the question and the lesson 3 summary note, still open in the lesson 3 prose and the lesson 10 summary |

New `wrong` that no earlier read found: 1 (finding 1). It is original authoring (`git log -S`: commit `4a127ead`), not fix-pass text.

Convergence: the rule allows at most one new `wrong` per three levels. This round found one, so the course can close once the fix pass and its fix-pass read are done.

## Inbox

One bullet in `docs/BACKLOG-INBOX.md` under "Raised later (audit first-python):", for the finding class of finding 2.

## Fix pass

Opus fixer, on commit `7ac0ec7e`. Every code-behaviour claim written here was run inside the page's Pyodide 0.27.7 (concepts section G, run through the sweep with `--concepts`), and every new `test-N` line was checked by submitting natural codings of its mistake through `tools/code-runner.mjs` (61 submissions, all first failing the test the line names; recorded as `mutants`, which `grade-all.mjs --code` now enforces).

| # | Status | Basis |
|---|---|---|
| 1 | fixed | `math.ceil(20 / 6)` is 4 and `round(20 / 6)` is 3, so the slip 4 is rounding up: the line now says "You rounded 3.33 up to 4." Slip value and key unchanged. |
| 2 | fixed | Own submissions: in script mode a `NameError`, `TypeError` or `ValueError` fails test 1; in function mode the raising or endless call fails its own test (`l8` test 4, `review-2` test 2, `homework-2` item 0 tests 3 and 4, item 2 tests 2 and 4); only a `SyntaxError` keys `error` (`code.js` line 622: `error` only when the run cannot load). Each sentence moved to the `test-N` line it reaches, worded as a condition; all thirteen `error` lines now say the code stopped before any test could run (`homework-2` item 0 keeps its colon hint). Differently from the audit: `review-1` item 6 also names `ValueError` (an unconverted price repeats the text, then `:.2f` raises `ValueError`); `homework-2` item 0 gains a `test-4` line (strict `elif` for hold, and `<=` on the stop, fail test 4) and item 2 a `test-4` line (`rate != 0` runs for ever on the negative rate); `l12` screen 10 moves the `Close` advice into its `test-1` line. |
| 3 | fixed | Python tutorial 3.1.3 ("simple assignment never copies data") and a run: `b = prices; prices.append(99.50)` shows through `b`, `prices.copy()` does not, and assigning a new list to `a` leaves `b`. `l2` summary and screen 5 now say "Assigning to a again later"; screen 4's `a7` line says "For a number"; `l8` screen 8 adds the list warning with `append`, index assignment and `.copy()`. |
| 4 | fixed differently | Own submissions: fee forgotten gives 101.2, `+ "1.50"` gives `'101.201.50'`, no conversion with the print deleted gives `TypeError`, `int` with it deleted gives `ValueError`, all at test 1. The line names all four; the starter and `int` with the print kept still key `error`, whose line already covers them. |
| 5 | fixed | `f"{-3.61:+.2f}" == f"{-3.61:.2f}"` and `f"{3.61:+.2f}"` is `+3.61`: no graded value can show the sign. Both lines reworded as the audit gives. |
| 6 | fixed | `"a"` keeps an existing line, `"w"` empties it (run). Added `l12` screen 5 test 4 and screen 7 test 5, each on a file holding an old line, with `test-4` and `test-5` lines and three append-mode mutants each. Expected values computed twice: `f"{1050.0:.2f}"` and the model solution; `1000 * 1.05` and `round(1000 * 1.05 ** 2, 2)` against the solution's lines. Solutions pass, starters fail, append programs fail the new test first. |
| 7 | fixed | Library reference, Truth Value Testing: `if 5:` runs. The sentence now states a sufficient condition only. |
| 8 | fixed | Language reference 2.3; `'_price'.isidentifier()` is True, `'1price'` and `'unit price'` are not. |
| 9 | fixed | `repr` of a float is the shortest text that gives back the same float (`str(12.5)` is `12.5`, `str(0.1 + 0.2)` is `0.30000000000000004`). |
| 10 | fixed | `table.js` line 57 keys a matching `wrong[]` id first. Added `wrong: simple, 1140` on `rows[1][1]` (1000 + 70 + 70; clear of 1144.90); the £70 line moved to `simple`, `r1c1` now gives the working. |
| 11 | fixed differently | Python tutorial 7.2.1; a run: `list(open(...))` on `101.20\n102.50` ends `'102.50'`. Wording: "Each line ends in a newline, except perhaps the last." |
| 12 | fixed | Python tutorial 7.2; a run: the `with` form reads the same list and `f.closed` is True after the block. One paragraph added to `l11` screen 3; no solution changed. |
| 13 | fixed | `len("ABCDEFGHIJ"[2:15])` is 8 and `s[7:2]` is empty. `l3` screen 8 prose adds the condition; `l10` summary adds it and says a slice past the end holds fewer. The `l3` summary note also gains "a is not after b". |

Scripts: the concepts script's old-text checks are re-pointed (the `q-floor` check tests the new line; each NOTE fires only while its old wording is present; the `l6` 74.90 check reads the new `simple` line), and section G checks the fix-pass claims: 815 checks, 0 failing, 0 notes, in CPython 3.13 and in Pyodide (strict tracebacks). The sweep's 17 routing facts and the two append programs are re-pointed in its `FIXED` map, so `KNOWN` is empty: 133 submissions, 0 differing, exit 0, also with `--concepts`.

Gates: validator 0 errors (4,618 warnings, as before); voice scan 35 on the 14 edited files 0 and 0; `run-number-scripts --only first-python` 5 of 5; `grade-all.mjs --code` on the 14 files 0 failures (mutants checked); playthrough of the 10 lessons and 4 sets green desktop and `--mobile`.

## Fix-pass read

Fresh reader, blind to this file until the rows below were written. Diff read: `git diff 7ac0ec7e 3157b5c1 -- app/content/courses/first-python` (14 files), at HEAD `eba9ca3e` (no later change to the course folder).

Method. Every code claim ran under the page's Pyodide 0.27.7 through `tools/code-runner.mjs` (the widget's own `casePlan` and the page's worker grader). For each moved or new `test-N` line I wrote my own codings of the mistake it names (95 submissions over 18 widgets, none copied from the committed mutants) and read the key and the failing row. `grade-all.mjs --code --file` ran on the ten files that carry mutants: 0 failures (61 mutants first fail the test they name; solutions pass; starters fail). Numbers were recomputed in floats and in `Decimal`.

How `error` is keyed (`js/engine/widgets/code.js` line 622, `tools/code-runner.mjs` `grade`): the key is `error` only when the run reports a load error, otherwise `test-N` for the first failing row. Measured: in script mode (a `stdout` test present) only a `SyntaxError` or `IndentationError` gives `error`, and a runtime error lands in row 1 (`test-1`). In call mode `error` also comes from a module-level runtime error (the learner's own call at the bottom of the file) and from a module-level loop that passes the load time limit. In every such case no test row ran, so "stopped before any test could run" is true as stated.

| # | File | JSON path | Claim | Verdict | Basis |
|---|------|-----------|-------|---------|-------|
| 1 | homework-1 | items.4 feedback.byKey.test-1 | -0.04 or -0.036 means no times 100; `+.2f` shows a plus on a rising week | correct | Run: `f"{r:+.2f}"` is -0.04, `round(r, 3)` and `.3f` are -0.036, times 100 gives -3.61; a +0.0361 return prints +3.61. My two codings key test-1. `.2f` without the plus passes, so "keep", not "use", is the right verb |
| 2 | homework-1 | items.4 widget.mutants (3) | each first fails test 1 | correct | grade-all 0 failures |
| 3 | homework-1 | items.6 feedback.byKey.test-1 | return times 100, two decimals on both lines | correct | Run: my three codings (no times 100; P&L printed as -1890.0; return to one decimal) key test-1. -6.30 × 300 = -1890.00; -6.30 / 104.50 = -6.03% |
| 4 | homework-1 | items.6 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 5 | homework-2 | items.0 feedback.byKey.error | stopped before any test; check the colons | correct | Run: a missing colon after `if` or after `else` keys `error` (`SyntaxError: expected ':'`); a missing branch does not (rows 6, 7) |
| 6 | homework-2 | items.0 feedback.byKey.test-3 | 52.10 between 50 and 56 holds; an error naming `action` means no branch set it | correct | Run: no-`else` coding and three-`if` coding give `UnboundLocalError ... 'action'` in row 3; a wrong word in `else` also keys test-3 |
| 7 | homework-2 | items.0 feedback.byKey.test-4 | price on the stop holds: `<`, not `<=` | correct | Run: `<=` with early returns gives 'sell' in row 4; hold on `stop < price <= target` gives the `action` error in row 4 |
| 8 | homework-2 | items.0 widget.mutants (6) | three first fail test 3, three test 4 | correct | grade-all |
| 9 | homework-2 | items.2 feedback.byKey.error | read the last line of the message, then the line it points to | imprecise | Run: an unguarded loop plus the learner's own `print(years_to_target(1000.00, 0.0, 1500.00))` keys `error` with "Stopped after the time limit.", which points to no line. First sentence true. Minor |
| 10 | homework-2 | items.2 feedback.byKey.test-2 | rate 0, answer `None`; a 5 second stop means guard with `rate > 0` | correct | Run: unguarded `while True` coding and a `rate < 0`-only guard both stop after 5 s in row 2; returning the text "None" keys test-2 on its value |
| 11 | homework-2 | items.2 feedback.byKey.test-4 | negative rate, answer `None`; `rate > 0`, not `rate != 0` | correct | Run: `elif rate:` and `if rate == 0.0: return None` both stop after 5 s in row 4; 1000 × 0.9^n never reaches 1200 |
| 12 | homework-2 | items.2 widget.mutants (6, 5 timeouts) | first fail test 2 or 4, margins hold | correct | grade-all, 129.5 s, 0 failures |
| 13 | l1-calculator | quiz[2] (q-floor) feedback.byKey.nearest | 3.33 rounded up to 4; `//` rounds down; £2 left | correct | The `nearest` wrong value is 4; 20 / 6 = 3.33, 20 // 6 = 3, 20 % 6 = 2. The old "to the nearest" would have been 3, the key |
| 14 | l10-reading-errors | screens.6 feedback.byKey.test-1 | `TypeError` or `ValueError` in the row means not yet a float; 101.2 means no fee; `'101.201.50'` means joined as text | correct | Run: print removed with text + number gives the TypeError in row 1; `int(...)` with print commented out gives the ValueError in row 1; fee dropped gives 101.2; `+ "1.50"` gives `'101.201.50'` (with `str(1.50)` the row shows `'101.201.5'`, same reading) |
| 15 | l10-reading-errors | screens.6 widget.mutants (4) | each first fails test 1 | correct | grade-all |
| 16 | l10-reading-errors | summary.ideas[2] | `[a:b]` holds b - a values with both inside and a not after b; fewer past the end | correct | Run: `len(s[i:j]) == j - i` for all 0 ≤ i ≤ j ≤ n; `s[7:2]` is empty; `s[8:15]` on 10 characters holds 2 |
| 17 | l11-numbers-from-a-file | screens.3 prose | the short form leaves closing to Python; `with open(name) as f:` reads the same lines and closes at block end; lesson 12 explains `with` | correct | Run: same list both ways, `f.closed` True after the block. l12 screens.5 explains `with` |
| 18 | l11-numbers-from-a-file | summary.ideas[0] | each line ends in a newline, except perhaps the last | correct | Run: a file written without a final `\n` gives a last line with none |
| 19 | l12-savings-script | screens.5 widget.tests[3] | file holding `old line`, then `save_line('s4.txt', 1, 1050.0)`, reads back `'Year 1: £1050.00\n'` | correct | Run in Pyodide with a `"w"` model: equal. Solution passes; starter fails (`error`: its own read of a missing file). Append codings fail it: `"a"` with `with`, and `"a+"` with `close`, both give `'old line\nYear 1: £1050.00\n'` in row 4 |
| 20 | l12-savings-script | screens.5 widget.how | 4 tests, three empty the file and one leaves an old line | correct | Count of tests; tests 1 to 3 call `open(..., 'w').close()` |
| 21 | l12-savings-script | screens.5 feedback.byKey.test-4 | open with `"w"` so the old line goes | correct | Row 19. A `"w"` coding without `with` passes all four |
| 22 | l12-savings-script | screens.5 widget.mutants (3) | append codings first fail test 4 | correct | grade-all |
| 23 | l12-savings-script | screens.7 widget.tests[4] | file holding `Year 9: old`, then two years at 5% on 1000.00, reads `['Year 1: £1050.00', 'Year 2: £1102.50']` | correct | Run, and `Decimal`: 1000 × 1.05 = 1050.00, × 1.05 = 1102.50. Solution passes; starter fails. Append once with a `while` loop, and append inside a `for` loop, both give three lines in row 5 |
| 24 | l12-savings-script | screens.7 widget.how | 5 tests, four empty the file | correct | Count |
| 25 | l12-savings-script | screens.7 feedback.byKey.test-5 | open once with `"w"` before the loop | correct | Run: `"w"` inside the loop keys test-1 (one line), so test-5 is reached only by append codings. Emptying with `"w"` and then appending in the loop passes, as it should |
| 26 | l12-savings-script | screens.7 widget.mutants (3) | each first fails test 5 | correct | grade-all |
| 27 | l12-savings-script | screens.10 feedback.byKey.error | stopped before any test | correct | Script mode: only a syntax error keys `error` (run: missing colon) |
| 28 | l12-savings-script | screens.10 feedback.byKey.test-1 | 5 means the loop began at index 0; a `ValueError` about `Close` means the header is still read | correct | Run: header kept, with or without a top-level call, gives `ValueError: could not convert string to float: 'Close\n'` in row 1; an index-0 loop gives 5, its first return pairing Friday with Monday |
| 29 | l12-savings-script | screens.10 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 30 | l2-naming-a-value | screens.3 prose | a name starts with a letter or an underscore | correct | Python reference, 2.3 Identifiers; run: `_x = 1` works, `1x = 2` is a SyntaxError |
| 31 | l2-naming-a-value | screens.3 feedback.byKey.error | stopped before any test | correct | Script mode. Run: `my price = 12.5` and an unclosed bracket key `error` |
| 32 | l2-naming-a-value | screens.3 feedback.byKey.test-1 | expects 50.0; a `NameError` means two spellings | correct | 12.5 × 4 = 50.0. Run: `Qty`/`qty` and `prise`/`price` give the NameError in row 1 |
| 33 | l2-naming-a-value | screens.3 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 34 | l2-naming-a-value | screens.4 feedback.byKey.a7 | for a number, assignment copies | correct | For an immutable value the copy model and the binding model predict the same output; the hedge "for a number" agrees with the l8 warning (row 59) |
| 35 | l2-naming-a-value | screens.5 explain.text | assigning to a again later never changes b | correct | Run: `a = 7; b = a; a = 10` leaves b at 7; true for any type, since rebinding a never touches b |
| 36 | l2-naming-a-value | summary.ideas[2] | same rule | correct | Row 35 |
| 37 | l3-text | screens.6 widget.options[2] (twodp) why | `print` shows a float with the fewest digits that pin it down: 12.5, not 12.50 | correct | Python tutorial 15 (shortest repr that round-trips); run: `print(12.50)` shows 12.5 |
| 38 | l3-text | screens.8 prose | the b - a count needs a and b within the string, a not after b | correct | Row 16; `len(s[2:7])` is 5, so the keyed answer stands |
| 39 | l3-text | summary.formula.note | same condition | correct | Row 16 |
| 40 | l4-asking-and-printing | screens.4 feedback.byKey.error, test-1 | expects 51.0; a `ValueError` means `int` on decimal text | correct | 12.75 × 4 = 51.0. Run: `int(typed)` and `int(typed) * 1.0` give the ValueError in row 1 |
| 41 | l4-asking-and-printing | screens.4 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 42 | l4-asking-and-printing | screens.7 feedback.byKey.error, test-1 | expects 100.0; a `TypeError` means a value is still text | correct | Run: `float(price * typed_qty)` gives the TypeError in row 1; the untouched starter does too |
| 43 | l4-asking-and-printing | screens.7 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 44 | l4-asking-and-printing | screens.9 feedback.byKey.error, test-1 | expects `Return: 2.80%`; a `TypeError` means a price is still text | correct | (189.35 - 184.20) / 184.20 = 2.80%. Run: one price left as text, and both left as text, give the TypeError in row 1 |
| 45 | l4-asking-and-printing | screens.9 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 46 | l4-asking-and-printing | screens.10 feedback.byKey.error, test-1 | expects 0.045 then `Interest: £90.00`; a `ValueError` means the % sign is still there | correct | 2000 × 0.045 = 90.00. Run: `float(text)`, `text[0:4]` and `text[-1]` all give a ValueError whose text still shows `%` |
| 47 | l4-asking-and-printing | screens.10 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 48 | l5-decisions | screens.2 explain.text | an `if` line runs its block when its condition works out to `True` | correct | Python reference 8.1; run |
| 49 | l6-until-done | screens.6 feedback.byKey.error | read the last line of the message, then the line it points to | imprecise | Run: an endless loop plus the learner's own `print(steps_to_reach(100, 150, 20))` keys `error` with "Stopped after the time limit.", which points to no line. Minor |
| 50 | l6-until-done | screens.6 feedback.byKey.test-1 | 3 steps from 100 to 150; a 5 second stop means the block never changes `value` | correct | 100, 120, 140, 160: 3 steps. Run: only `count` changing, and `value = start + step` on every pass, both stop after 5 s in row 1 |
| 51 | l6-until-done | screens.6 widget.mutants (3 timeouts) | each first fails test 1 past five times the limit | correct | grade-all |
| 52 | l6-until-done | screens.8 widget cell r1c1 wrong `simple` | 1140 is the slip of adding £70 again | correct | 1000 × 0.07 = 70; 1070 + 70 = 1140. The table grader keys a matching `wrong` id of the first wrong cell (`table.js` lines 57, 90). 1140 is within 0.01 of no keyed cell (1070.00, 1144.90, 1225.04) |
| 53 | l6-until-done | screens.8 feedback.byKey.simple, r1c1 | year 2 adds £74.90; 1070.00 × 1.07 = 1144.90 | correct | 1070 × 0.07 = 74.90; `Decimal`: 1070 × 1.07 = 1144.90 exactly; 1144.90 × 1.07 = 1225.04 |
| 54 | l6-until-done | screens.9 feedback.byKey.error | read the last line, then the line it points to | imprecise | As row 49 (run with `print(years_to_double(1000.00, 0.07))`). Minor |
| 55 | l6-until-done | screens.9 feedback.byKey.test-1 | 11 years at 7%; a 5 second stop means the growth is not stored | correct | 1.07^10 = 1.967, 1.07^11 = 2.105. Run: `balance * (1 + rate)` unstored stops after 5 s in row 1 |
| 56 | l6-until-done | screens.9 widget.mutants (3 timeouts) | each first fails test 1 past five times the limit | correct | grade-all |
| 57 | l8-many-values | screens.6 feedback.byKey.error, test-4 | test 4 is the empty list and expects `None`; an `IndexError` means `values[0]` ran on it | correct | Run: `values[0]` before any check, with a `for` or a `while`, gives `IndexError` in row 4. With the learner's own `print(largest([]))` the key is `error` and its message does point to the line |
| 58 | l8-many-values | screens.6 widget.mutants (3) | each first fails test 4 | correct | grade-all |
| 59 | l8-many-values | screens.8 prose | `b = prices` does not copy; `append` and `prices[0] = ...` show through `b`; `b = prices.copy()` gives a separate list | correct | Run: after `b = prices`, an append and an item assignment leave `b is prices` with both changes; a `.copy()` taken earlier keeps its values |
| 60 | review-1 | items.6 feedback.byKey.error | stopped before any test | correct | Script mode, row 31 |
| 61 | review-1 | items.6 feedback.byKey.test-1 | a `TypeError` or a `ValueError` means a value is still text | imprecise | Run: `price = int(price_text)` with both values converted gives `ValueError: invalid literal for int() ... '41.20'` in row 1. No value is still text there; the cure is `float`, the l4 screen 4 mistake this review covers. The other two cases are right (`float(price_text) * qty_text` TypeError; text times int then `.2f` gives `ValueError: Unknown format code 'f'`). Minor |
| 62 | review-1 | items.6 widget.mutants (3) | each first fails test 1 | correct | grade-all |
| 63 | review-2 | items.6 feedback.byKey.error, test-2 | test 2 is the empty list; an `IndexError` means `pnls[0]` ran on it | correct | Run: no guard, and a guard placed after `pnls[0]`, both give `IndexError` in row 2 |
| 64 | review-2 | items.6 widget.mutants (3) | each first fails test 2 | correct | grade-all |

Counts: 64 rows. correct 60, wrong 0, imprecise 4 (all minor), misleading 0, unverified 0.

Notes. The diff holds 61 mutants and 13 reworded `error` lines as briefed, but 11 timeout mutants, not 12 (5 in homework-2 items.2, 6 in l6). One coding outside the lesson passes l12 screens.5 test 4 without `"w"`: `"r+"` overwrites in place because the new line is longer than the old one. Nothing in the course teaches `"r+"`, so no change is asked.

Fixes (paste-ready).

1. Rows 9, 49, 54: `homework-2.json` items.2, `l6-until-done.json` screens.6 and screens.9, `feedback.byKey.error`. Replace with:
   `"error": "Your code stopped before any test could run. Read the last line of the message under the editor. If it names the time limit, a loop never ends; otherwise go to the line it points to."`
   Basis: the three loop exercises are the ones where a module-level call can pass the load limit; the engine's message then reads "Stopped after the time limit." with no line.

2. Row 61: `review-1.json` items.6 `feedback.byKey.test-1`. Replace with:
   ``"test-1": "Test 1 expects `Value: £6180.00`. A `TypeError`, or a `ValueError` about a format code, means a value is still text: convert both first. A `ValueError` from `int` means the price has a decimal point: use `float`."``
   Basis: the three row messages measured above.

Scripts (scratch, not committed): `fpr-fp13/run.mjs` with `subs.mjs` and `subs2.mjs` (submissions), `fpr-fp13/claims.mjs` (Pyodide claims and numbers, 23 checks, all ok).

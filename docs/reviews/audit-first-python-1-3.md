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

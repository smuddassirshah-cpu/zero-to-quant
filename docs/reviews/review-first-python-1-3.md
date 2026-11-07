# First Python Scripts levels 1 to 3 (Values; Control flow; Functions and files): second-reader findings

Scope: `app/content/courses/first-python/` l1 to l12, `review-1.json` to `review-3.json`, `homework-1.json` to `homework-3.json`, and `course.json` (maps and `requires`). The course has three levels, so the continuity skim covers the courses that require it (`py-found` L1, `cpp` L1) and every cross-reference to it (`pytest` l11 and homework-3). No course brief (`docs/briefs/first-python.md`) and no author reports (`docs/reports/first-python-<n>.md`) exist; the levels were read against `course.json` objectives, `docs/AUTHORING.md` and the Stage 0 rule that a step may use only what an earlier screen taught.

Method: every lesson screen, quiz item, set item, `why`, `byKey`, hint and model answer read in full. Every graded key, `wrong[]` value and stated number recomputed twice in three new scripts (method 1 runs the Python the screen shows, method 2 is hand arithmetic or a closed form). All 56 code widgets run through an emulation of the engine's harness (`app/js/engine/widgets/code.js`: function mode with load errors as the `error` key, script mode with `printed`, one working directory per Check shared by its cases, `isclose` as `__zq_cmp`) in CPython 3.13.18 and in Pyodide 0.27.7 (Python 3.12.7) under node from the local CDN. Every quoted error message and all 15 quoted tracebacks rebuilt and run in both, file names and line numbers matched. 29 slips that feedback lines name were applied to the solutions to see which `test-N` (or `error`) key the engine would actually return. Concept order checked: each name, operator, error type and built-in against the first screen that teaches it.

Tool results:
- `python3 docs/reports/first-python-L1-numbers.py`: exit 1, 135 of 145. The 10 failures are content errors, each a finding below (1, 2, 3, 4, 5, 11); they pass once the fixes reword the sentences. 9 "check by hand" lines, each read, all fine.
- `python3 docs/reports/first-python-L2-numbers.py`: exit 1, 167 of 172. The 5 failures are findings 6, 7, 8, 15, 16. 16 "check by hand" lines, all fine.
- `python3 docs/reports/first-python-L3-numbers.py`: exit 1, 137 of 138. The failure is finding 9. 8 "check by hand" lines, all fine.
- Code items: 56 of 56 solutions pass every hidden test and example, and every starter fails at least one, in CPython and in Pyodide (scratch runner `read-first-python-L1-L3/allcode.py`). The only interpreter difference met: a missing file is `[Errno 2]` in CPython and `[Errno 44]` in Pyodide; no first-python text quotes an errno. Every quoted error last line (TypeError, ValueError, NameError, IndexError, ZeroDivisionError both forms, SyntaxError with its "Maybe you meant '==' or ':='" hint) matches Python 3.12 exactly; every float the prose says is printed (2.5, 121.5, 4560.0, 4627.5, 101.85, 98.5, 1628.89 and the rest) prints that way in both.
- Slip check (`read-first-python-L1-L3/mutate.py`): 23 of 29 named slips land on the key their line is written for; the 6 that do not are findings 7, 8 and 13.
- `cd app && node tools/validate.mjs`: 0 errors, 4122 warnings in all. first-python warnings: 45 (21 problem screen without a canvas before the ladder ends, 10 `key-length`, 7 advisory `O2-long-sentence` of 20 to 34 words, 4 `O2-explain-answer`, 2 `float-example`, 1 ladder canvas kind on l11 `screens[3]`). Of the `key-length` ten, four are real giveaways (finding 19); the rest are long because the right reading is specific, and were left.
- `VOICE_BASE=app/content/courses/first-python python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words (4767 scanned), 0 explanations over three sentences. My own scan of learner text: no exclamation marks, no em or en dashes, no American spellings, money in £ throughout (every `$` is a KaTeX delimiter).
- `node tools/fresh-check.mjs --file content/courses/first-python/<set>.json --min-run 10`: review-1, homework-1, homework-2 0 hits; review-2 1 (finding 21); review-3 3 (one same-course, finding 21; two cross-course code names, `average` with `cpp` l2 and `average_close` with `py-found` review-3, which are the later courses' to change); homework-3 1 (`best_day` with `py-found` review-4, the later course's). It missed homework-3 `items[1]` against l10 `screens[8]` (Engine 1).
- `node tools/playthrough.mjs --local-cdn <scratchpad>/pkgs`: 36 of 36 green, every lesson (`--lesson`, 13 to 15 checks each, every quiz full marks) and every set (`--set` review-1 to review-3 recorded 8 of 8; homework-1 to homework-3 marked every item right, longform by the button), each with and without `--mobile`. Screenshots read: l5 desktop and 440 px (flowchart, code and trap screens), l10 and homework-2 samples; no layout faults.

Format: `N. file | JSON path | severity | problem | evidence | exact fix`. Severities: wrong, misleading, voice, layout, continuity. Freshness repeats are filed as continuity. No fix cites a lesson by number.

## Findings

1. l1-calculator.json | `screens[1].explain.text`; `screens[4].widget.options[2].why`; `quiz[2].feedback.byKey.decimal` | wrong | Three lines define `//` as dropping the decimals ("drops everything after the decimal point", "drops the part after the decimal point", "keeps only the whole part"). That is truncation; `//` rounds down. homework-1 `items[0]` then marks exactly this model as the misconception ("You dropped the decimals of -3.5"). | `-7 // 2` is -4, `int(-7 / 2)` is -3. `screens[2].explain.text` and the summary already say "rounds down". | `screens[1].explain.text` last sentence: "So `//` divides and then rounds down to a whole number." `screens[4].widget.options[2].why`: "That is `19 / 5`. The double slash rounds down to a whole number." `quiz[2].feedback.byKey.decimal`: "That is `20 / 6`. The double slash rounds down to a whole number."

2. l1-calculator.json | `screens[8].prose`; `summary.formula.note` | wrong | "Ties go left to right" is stated for every group, including powers, which group right to left. | `2 ** 3 ** 2` is 512 (`2 ** 9`), not 64. | In `screens[8].prose` replace "Ties go left to right." with "Ties go left to right, except powers: `2 ** 3 ** 2` is `2 ** 9`." `summary.formula.note`: "Ties go left to right, except powers. Add brackets when in doubt."

3. l3-text.json | `screens[5].hints[1].text`; `screens[5].widget.options[2].why` | wrong | "Different types are not equal" and "When the types differ it answers False" are false, and the learner has just met int and float. | `1 == 1.0` is True; `True == 1` is True. | `hints[1].text`: "One side is a str, the other an int. A str is never equal to a number." `options[2].why`: "`==` accepts any two values. A str and a number are never equal, so it answers False rather than stopping."

4. l3-text.json | `quiz[2].explain.text` | wrong | "Only `+` between a str and a number fails" is false. | `"3" - 2`, `"3" / 2` and `"3" * 2.0` are all TypeErrors in both Pythons. | "`"3" * 2` repeats the text to give `"33"`, which is still a str. Text times a whole number is allowed; text plus a number is a TypeError."

5. homework-1.json | `items[7].model` (last line) | wrong | "It prints 520.0 and then 51.0." The fixed script reassigns `price = 52`, an int, so `value = price * qty` is the int 520 and prints `520`. | Run in CPython and Pyodide: `520` then `51.0`. | "It prints 520 and then 51.0. The new price, 52, is an int, so the recomputed `value` is the int 520."

6. review-2.json | `items[5].prose`; `items[5].explain.text` | wrong | The prose says the fixed program "should print the day's total P&L, £137.00", but with these floats it prints `136.99999999999997`, which no screen of the course explains. | `310.40 - 120.15 - 95.25 + 42.00` prints 136.99999999999997 in both Pythons. | Change the list in the prose code to `pnls = [310.50, -120.25, -95.25, 42.00]` (sum exactly 137.0; the bug still prints `42.0`). `explain.text` last sentence: "Moved above the loop it runs once, and the sum is 310.50 − 120.25 − 95.25 + 42.00 = 137.00." Prose first line unchanged.

7. l7-for-each.json | `screens[9].feedback.byKey.test-3` | wrong | The line for the `r >= 0` slip is keyed on test 3, but test 1's list already holds a 0.0 day, so that slip fails test 1 first and this line never shows. | Slip `if r >= 0:` returns 4 on test 1 (engine key `test-1`). | Rename the key to `"test-1"` with text: "If test 1 got 4, you counted the 0.0 day. A return of exactly 0.0 is flat, not up: use `r > 0`, not `r >= 0`."

8. homework-2.json | `items[3].feedback.byKey.test-6` | wrong | The line for comparing one day's P&L with the limit is keyed on test 6, but that slip fails test 4 first (day 2's −150.00 breaches, the running total −50.00 does not). | Slip `if p <= -limit:` returns 2 on test 4, expected `None` (engine key `test-4`). | Rename the key to `"test-4"` with text: "Day 2's own loss is −150.00, but the running total is only −50.00, so there is no breach. Compare the total, not the day."

9. l9-packaging-steps.json | `screens[5].widget.options[2]` (`swapped`) | wrong | The distractor `-105.0` has the why "You treated the first argument as `new`", but that slip gives `105.0 - 100.0 = 5.0`, the value of the `by-size` option; no slip gives −105.0. | `new - old` with `new = 105.0`, `old = 100.0` is 5.0. | Replace the option with `{ "id": "int", "text": "`-5`", "why": "You dropped the decimal point. Both prices are floats, so `new - old` is the float −5.0." }`.

10. review-1.json | `items[3].widget.options[2]` (`text`) | misleading | "Cost: £1212121..." has the why "You treated the values as text", but text times text is a TypeError, so no misconception prints this. | `"12" * "3.5"` raises `TypeError: can't multiply sequence by non-int of type 'str'`. | Replace with `{ "id": "braces", "text": "Cost: £{shares * price:.2f}", "why": "The `f` before the quotes makes Python fill in the braces." }`.

11. l3-text.json | `screens[2].prose` | wrong | "runs to the end, index 6": `"GBPUSD"` has no index 6; its last index is 5, and 6 is the stop. | `len("GBPUSD") - 1` is 5. | "Slices work in a program the same way. `print(pair[0:3])` prints `GBP`. The second currency starts at index 3 and runs to the end. The last index is 5, so the stop is 6."

12. l4-asking-and-printing.json, l10-reading-errors.json, review-1.json, review-3.json, homework-1.json, homework-3.json | the 15 quoted tracebacks (below) and seven sentences about "the line above" | misleading | Python 3.11 and later, and Pyodide 0.27.7's 3.12 in the editor, print a caret line (`^^^` or `~~~^~~~`) under the failing code line. Every traceback in the course leaves it out, and two also drop the `Traceback (most recent call last):` header. So the line "just above" the last line is a caret line in real output, not the File line or the code line the course says. | Each block rebuilt with the same file name and line numbers and run in Pyodide 0.27.7 (Python 3.12.7). The worker's `_tb` uses `traceback.format_list`, which prints the carets in 3.12. CPython 3.13 prints the same lines, with `~` in place of some `^` under a call (`~~~^^^^^^^` for `^^^^^^^^^^`). | Replace each block with the text below (last lines unchanged), then reword the seven sentences.
   - l4 `screens[5].prose`, the `text` block:
     ```text
     Traceback (most recent call last):
       File "main.py", line 3, in <module>
         total = price * qty
                         ^^^
     NameError: name 'qty' is not defined
     ```
   - l4 `quiz[2].prose`:
     ```text
     Traceback (most recent call last):
       File "main.py", line 4, in <module>
         shares = int(typed)
                  ^^^^^^^^^^
     ValueError: invalid literal for int() with base 10: '12.5'
     ```
   - review-1 `items[7].prose` (header added):
     ```text
     Traceback (most recent call last):
       File "main.py", line 3, in <module>
         total = price + fee
                 ~~~~~~^~~~~
     TypeError: unsupported operand type(s) for +: 'float' and 'str'
     ```
   - homework-1 `items[3].prose` (header added):
     ```text
     Traceback (most recent call last):
       File "main.py", line 2, in <module>
         cash = float(typed)
                ^^^^^^^^^^^^
     ValueError: could not convert string to float: '1,250.40'
     ```
   - l10 `screens[2].prose`:
     ```text
     Traceback (most recent call last):
       File "closes.py", line 2, in <module>
         print(prices[4])
               ~~~~~~^^^
     IndexError: list index out of range
     ```
   - l10 `screens[3].prose`:
     ```text
     Traceback (most recent call last):
       File "avg.py", line 1, in <module>
         print(average([101.20, 102.50]))
               ^^^^^^^
     NameError: name 'average' is not defined
     ```
   - l10 `screens[4].prose`:
     ```text
     Traceback (most recent call last):
       File "closes.py", line 3, in <module>
         count = len(closes)
                 ^^^^^^^^^^^
     TypeError: object of type 'NoneType' has no len()
     ```
   - l10 `screens[5].prose`:
     ```text
     Traceback (most recent call last):
       File "returns.py", line 5, in <module>
         print(daily_return(closes[0], closes[1]))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       File "returns.py", line 2, in daily_return
         return (p1 - p0) / p0
                ~~~~~~~~~~^~~~
     ZeroDivisionError: float division by zero
     ```
   - l10 `screens[6].prose`:
     ```text
     Traceback (most recent call last):
       File "fees.py", line 4, in <module>
         print(with_fee("101.20"))
               ^^^^^^^^^^^^^^^^^^
       File "fees.py", line 2, in with_fee
         return price_text + 1.50
                ~~~~~~~~~~~^~~~~~
     TypeError: can only concatenate str (not "float") to str
     ```
   - l10 `screens[8].prose`:
     ```text
     Traceback (most recent call last):
       File "risk.py", line 13, in <module>
         print(max_drawdown([100.00, 110.00, 99.00]))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       File "risk.py", line 5, in max_drawdown
         price = prices[i]
                 ~~~~~~^^^
     IndexError: list index out of range
     ```
   - l10 `quiz[1].prose`:
     ```text
     Traceback (most recent call last):
       File "load.py", line 7, in <module>
         closes.append(float(parts[1]))
                       ^^^^^^^^^^^^^^^
     ValueError: could not convert string to float: 'n/a'
     ```
   - l10 `quiz[3].prose` (no caret under `report(closes)`: it is the whole line):
     ```text
     Traceback (most recent call last):
       File "report.py", line 12, in <module>
         report(closes)
       File "report.py", line 8, in report
         print(average(closes[5:]))
               ^^^^^^^^^^^^^^^^^^^
       File "report.py", line 3, in average
         return sum(xs) / len(xs)
                ~~~~~~~~^~~~~~~~~
     ZeroDivisionError: division by zero
     ```
   - review-3 `items[1].prose`:
     ```text
     Traceback (most recent call last):
       File "risk.py", line 9, in <module>
         print(worst_day(closes))
               ^^^^^^^^^^^^^^^^^
       File "risk.py", line 4, in worst_day
         change = closes[i + 1] - closes[i]
                  ~~~~~~^^^^^^^
     IndexError: list index out of range
     ```
   - homework-3 `items[4].prose`:
     ```text
     Traceback (most recent call last):
       File "load.py", line 11, in <module>
         closes = read_closes("prices.csv")
                  ^^^^^^^^^^^^^^^^^^^^^^^^^
       File "load.py", line 5, in read_closes
         closes.append(float(parts[1]))
                             ~~~~~^^^
     IndexError: list index out of range
     ```
   - homework-3 `items[7].prompt`:
     ```text
     Traceback (most recent call last):
       File "returns.py", line 12, in <module>
         closes = read_closes("prices.csv")
                  ^^^^^^^^^^^^^^^^^^^^^^^^^
       File "returns.py", line 4, in read_closes
         closes.append(float(line.split(",")[1]))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^
     ValueError: could not convert string to float: 'Close\n'
     ```
   - Sentences: l4 `objectives[1]`: "Read a traceback: the error on the last line, the place in the File line above it". l4 `screens[5].explain.text`: "Read a traceback from the bottom: the last line gives the error, and the `^` marks show the part that failed. The File line above them says where. Here line 2 made `quantity` and line 3 asked for `qty`." l4 `summary.ideas[2]`: "Read a traceback from the bottom: the last line says what went wrong, the File line above it says where." l4 `quiz[2].explain.text` second sentence: "The File line above it says this happened on line 4." l10 `screens[2].feedback.correct`: "The last line names the error; the File line above it shows where." l10 `screens[2].feedback.generic`: "Not quite right. Read the last line of the traceback, then the code line it points to." l10 `screens[2].hints[2].text` second sentence: "The code line above it, line 2, asks for `prices[4]`, but the last index is 3." l10 `summary.ideas[0]`: "Read a traceback from the bottom: the last line names the error, and the File line nearest the bottom is where Python stopped." homework-3 `items[7].model`: replace "The File line just above it says" with "The File line nearest the bottom says".

13. l10-reading-errors.json, l11-numbers-from-a-file.json, review-3.json | l10 `screens[6].feedback.byKey`; l11 `screens[2].feedback.byKey`; l11 `screens[6].feedback.byKey.test-1`; review-3 `items[6].feedback.byKey.test-1`; l10 `screens[8].feedback.byKey.test-1` | misleading | Each script calls the function on its last line, so a slip that raises (text plus a float, `int` on a decimal, index 0, the header still read, the loop past the end) stops the load and returns the `error` key. The `test-1` clauses written for those slips never show. In l10 `screens[6]` and l11 `screens[2]` the learner gets no line for the slip at all. | Slip check: `int(price_text)`, `price_text + 1.50`, `float(parts[0])`, `lines` for `lines[1:]`, `readlines()` for `readlines()[1:]` and `len(prices) + 1` all return `error`. | l10 `screens[6]`: `byKey.error` "Your script still stops on its last line before the tests run. A `TypeError` means the price is still text when you add; a `ValueError` from `int` means `int` cannot read a decimal point: use `float`."; `byKey.test-1` "Test 1 passes the text `\"101.20\"` and expects 102.7. Convert with `float` before adding 1.50." l11 `screens[2]`: add `byKey.error` "Your script stops on its last line before the tests run. An error about `'Tue'` means you took index 0: the price is index 1."; `byKey.test-1` "Test 1 expects the number 102.5. Text such as `'102.50\n'` means `float` is missing." l11 `screens[6].feedback.byKey.test-1`: "Test 1 expects all five closes. Four closes means the slice skipped one line too many." review-3 `items[6].feedback.byKey.test-1`: "Test 1 expects 101.0. About 84.17 means you divided by the line count, header included." l10 `screens[8].feedback.byKey.test-1`: "Test 1 expects 0.2, the £22.00 fall measured against the £110.00 peak."

14. l1-calculator.json, l2-naming-a-value.json | l1 `screens[9].feedback.byKey.test-1`; l2 `screens[7].feedback.byKey.test-1` | misleading | `test-1` is the stdout test, so these lines fire on any wrong output: printing 5.0 gets "Check your brackets", and forgetting `print(cash)` gets "Check the order of operations". | Slip check: deleting `print(cash)` returns `test-1`. | l1: "If it printed 261.5, check your brackets: `262.5 - 250 / 250` divides first." l2: "Your program should print 640 on one line. Store the new value in `cash`, then print it."

15. l7-for-each.json | `screens[7].explain.text` | misleading | "The count is always `b − a`" fails when `b` is below `a`. | `len(range(5, 2))` is 0, not −3. | Second sentence: "The count is `b − a` whenever `b` is at least `a`: here 13 − 1 = 12 months."

16. l8-many-values.json | `screens[2].explain.text` | misleading | "Python prints floats without trailing zeros, as `100.0`" contradicts its own example, which ends in a zero. | `print(100.00)` shows `100.0`; `print(99.80)` shows `99.8`. | Last sentence: "Python prints a float with the digits it needs, keeping one after the point, so 100.00 shows as `100.0`."

17. l3-text.json | `screens[8].question` | misleading | "How many characters does `s[2:7]` keep?" has no `s`; the key 5 holds only when `s` has at least 7 characters. | `"abc"[2:7]` is `"c"`. | "`s` holds 10 characters. How many does `s[2:7]` keep?"

18. l8-many-values.json, homework-2.json | l8 `screens[9].explain.text`; homework-2 `items[4]` (title, prose, widget) | misleading | l8 says the maximum drawdown "comes in a later course", but two lessons later the error-reading lesson teaches it. homework-2 defines **maximum drawdown** in pounds, while that lesson and homework-3 `items[1]` define it as a fraction of the peak. A learner meets two answers to one name. | l10 `screens[8].prose`: "worst fall from a running peak, as a fraction of that peak". | l8 `explain.text` second sentence: "The gap between peak and price is the **drawdown**: here it is largest, £3.20, on the last day. Later in this course you measure it as a share of the peak." homework-2 `items[4]`: title "Largest fall"; prose "The **largest fall** of a price list, in pounds, is the biggest drop from the highest price so far to any later price. For 100.00, 104.00, 101.50, 106.20, 103.00 it is 106.20 − 103.00 = £3.20. A list that never falls gives 0."; question "Complete `largest_fall`."; replace `max_drawdown` with `largest_fall` in the starter, solution, every test and example `call`, and the code in `explain.text`; starter comment unchanged.

19. l4-asking-and-printing.json, l9-packaging-steps.json, review-3.json | l4 `screens[3].widget.options`, `screens[6].widget.options`; l9 `quiz[0].widget.options`; review-3 `items[5].widget.options` | misleading | The key is the only "it stops with an error" option among "it prints" options, and much longer, so it can be picked by shape (validator `key-length`). | Key 26, 25, 43 and 50 characters against distractors of at most 13, 13, 16 and 17. | l4 `screens[3]`: add `{ "id": "type", "text": "It stops with a TypeError", "why": "A TypeError means the wrong kind of value. Here `int` got text, the right kind, but the text is not a whole number." }`. l4 `screens[6]`: add `{ "id": "value", "text": "It stops with a ValueError", "why": "A ValueError means the right kind of value with the wrong contents. Here a str and an int cannot be joined at all." }`. l9 `quiz[0]`: key text "It stops with a `NameError`"; add `{ "id": "type", "text": "It stops with a `TypeError`", "why": "A `TypeError` needs a value of the wrong kind. At line 1 there is no value: the name `with_fee` does not exist yet." }`. review-3 `items[5]`: key text "It stops with a `NameError`"; add `{ "id": "type", "text": "It stops with a `TypeError`", "why": "A `TypeError` needs a value of the wrong kind. Here the main program has no `s` at all." }`.

20. l5-decisions.json | `screens[0].explain.text` | voice | A stray comma: "Its answer, is written `True` or `False`". | | "The question 'below 98.00?' is `price < 98.00` in Python. Its answer is written `True` or `False`, and for £97.40 it is `True`. So the program follows the True arrow and sells."

21. review-1.json, review-2.json, review-3.json, homework-1.json, homework-2.json, homework-3.json | the six items below | continuity | Freshness: each repeats a lesson screen's setup, code or test lists. | review-3 `items[3]` is l12 `quiz[2]`'s program word for word with new numbers (fresh-check run 23); homework-3 `items[1]` reuses four of l10 `screens[8]`'s seven test lists (`[100, 110, 99, 105, 88, 95]`, `[100, 101, 102]`, `[120]`, `[50, 40, 60, 30]`); review-2 `items[2]` is l7 `screens[3]` with `range(3, 7)` (fresh-check run 10); homework-2 `items[0]` uses l5's stop, target and prices (97.40, 98.00, 110.00, 112.50); homework-1 `items[5]` uses l2 `screens[9]`'s position (25 shares at £182.40); review-1 `items[2]` is l3 `quiz[0]` (a `.L` ticker sliced from 0). | All numbers below recomputed in both Pythons.
   - review-3 `items[3]`: code after the function becomes `a = project(1500.00, 0.02, 3)`, `b = project(a, 0.02, 1)`, `print(round(b - a, 2))`; answer 31.84 (tol 0.005); `accept` "31.84: one more year's 2% on £1,591.81."; wrong `simple` 30 (byKey "You took 2% of the first £1,500.00. The fourth year's 2% is paid on £1,591.81."); wrong `b` 1623.65 (byKey "That is `b`, the balance after four years. The line prints `b - a`, one year's growth."); remove `two`; `feedback.correct` "The fourth year adds £31.84, more than the first year's £30.00."; `explain.text` "`a` is $1500 \times 1.02^3 = 1591.812$. One more year multiplies by 1.02, adding 2% of 1591.812, which is 31.836. Rounded, it prints 31.84."
   - homework-3 `items[1].widget.tests`: test 2 `max_drawdown([200.00, 250.00, 225.00, 240.00, 175.00, 210.00])` expect `0.3`; test 5 `max_drawdown([80.00, 80.00, 85.00])` expect `0.0`; test 6 `max_drawdown([42.00])` expect `0.0`; test 7 `max_drawdown([60.00, 45.00, 90.00, 54.00])` expect `0.4`. `byKey.test-2`: "Test 2 expects 0.3, from £250.00 to £175.00 across several days. About 0.271 measures one-day falls only; the fall must run from the peak." (The one-day slip still passes test 1 and fails test 2 first.)
   - review-2 `items[2]`: code `total = 0`, `for k in range(4):`, `    total = total + 2 * k + 1`, `print(total)`; answer 16; `accept` "16: 1 + 3 + 5 + 7."; wrongs `with-four` 25 (byKey "You included 4. `range(4)` stops before 4.") and `from-one` 24 (byKey "You started at 1. `range(4)` starts at 0."); `feedback.correct` "1 + 3 + 5 + 7 = 16."; `feedback.generic` "Not quite right. List the numbers `range(4)` gives, then work out each term."; `explain.text` "`range(4)` gives 0, 1, 2 and 3, so the terms are 1, 3, 5 and 7. The accumulator adds them: 16."
   - homework-2 `items[0].widget.tests` and example: `decide(48.90, 50.00, 56.00)` 'sell'; `decide(57.25, 50.00, 56.00)` 'take profit'; `decide(52.10, 50.00, 56.00)` 'hold'; `decide(50.00, 50.00, 56.00)` 'hold'; `decide(56.00, 50.00, 56.00)` 'hold'; keep `decide(0.95, 1.00, 1.20)` 'sell'; example `decide(48.90, 50.00, 56.00)` 'sell'.
   - homework-1 `items[5]`: starter and solution `price = 63.50`, `qty = 40`; prose "You buy 40 shares at £63.50. The broker charges a fee given as the text `\"0.25%\"` of the trade value."; question "Print `Fee: £6.35`, then `Total: £2546.35`. Store the fee in `fee`."; test 1 expect "Fee: £6.35\nTotal: £2546.35\n"; test 2 expect `6.35`; `how` "... the value of fee (close to 6.35 is enough) ..."; `feedback.correct` "A fee of £6.35 on a £2,540 trade."; `byKey.test-1` "If the fee reads £635.00, you used 0.25 as the rate. Divide by 100 to turn the percentage into a decimal."; `explain.text` "The trade is worth £2,540. The rate is $0.25 / 100 = 0.0025$, so the fee is £6.35 and the total £2,546.35. Forgetting the division by 100 makes the fee a hundred times too big."
   - review-1 `items[2]`: prose code `date = "2026-10-16"`, `print(date[5:7])`; options `right` "10", `stop` "10-" (why "You kept index 7, the dash. The stop index is left out."), `from1` "-1" (why "You counted from 1. Index 5 is the sixth character, the 1 of 10."); `feedback.correct` "Indexes 5 and 6: the month."; `feedback.generic` "Not quite right. Start at index 5 and leave index 7 out."; `explain.text` "`date[5:7]` keeps indexes 5 and 6, which spell 10, the month. It holds $7 - 5 = 2$ characters."

22. l3-text.json | `screens[8].prose`; `summary.formula.tex` | continuity | The formula uses `len`, which no screen has taught; lists bring it in later. | First teaching: the list lesson, "`len(prices)` counts all of them". | In the prose replace `$$\text{len}(s[a:b]) = b - a$$` with `$$\text{characters in } s[a:b] = b - a$$`; `summary.formula.tex` "\text{characters in } s[a:b] = b - a"; `summary.formula.note` "The start is kept and the stop is left out, when both lie inside the string."

23. l3-text.json | `quiz[2]`; `screens[0].explain.text` | continuity | The quiz tests `"3" * 2` (text repetition), which no screen shows; the next lesson's hook then relies on it. | Repetition appears first in `quiz[2]`, then l4 `screens[0]` "Text times a whole number is allowed". | `screens[0].explain.text`: "`\"12\"` and `\"5\"` are strings, so `+` joins them into `\"125\"`. With numbers, `12 + 5` would be 17. On text, `*` repeats instead: `\"12\" * 2` is `\"1212\"`."

24. l10-reading-errors.json, l12-savings-script.json, l11-numbers-from-a-file.json, homework-3.json, l12-savings-script.json | l10 `screens[3].prose`; l12 `screens[0].prose`; l11 `quiz[1].explain.text`; homework-3 `items[2].widget.solution`; l12 `screens[6].explain.text` | continuity | Five steps use something never taught: `sum` (l10, first use anywhere in the course), `round` (l12's opening question needs it to pick 2249.73), `continue` (l11's explanation), `is None` (homework-3's model solution), and the `"a"` mode, which l12's objective promises but only its quiz shows. | Grep of the course: no earlier screen names any of the five. | l10 `screens[3].prose` first line: "Another script, another traceback. `sum(xs)` adds up the values in a list." l12 `screens[0].prose` first paragraph: "£2,000.00 sits in a savings account paying 4% a year. Each year the balance is multiplied by 1.04. `round(x, 2)` rounds `x` to two decimal places." l11 `quiz[1].explain.text` second sentence: "Put the append under `if line.strip() != \"\":`, or remove the empty line from the file." homework-3 `items[2].widget.solution`, the function (checked: passes all five tests): `def best_day(name):` / `    lines = open(name).readlines()[1:]` / `    best = lines[0].split(",")[0]` / `    best_price = float(lines[0].split(",")[1])` / `    for line in lines:` / `        parts = line.split(",")` / `        price = float(parts[1])` / `        if price > best_price:` / `            best = parts[0]` / `            best_price = price` / `    return best`. l12 `screens[6].explain.text`: "`\"w\"` empties the file every time it opens, and this opens it three times. Opening with `\"a\"` instead keeps what is there and writes at the end. Here, open it once, before the loop:" then the existing code block.

25. l2-naming-a-value.json, l4-asking-and-printing.json, l5-decisions.json | l2 `screens[3].feedback.byKey.error`; l4 `screens[5].widget.options[3].why`; l5 `quiz[2].explain.text` | continuity | Error names and a print form before they are taught: `NameError` two lessons before the first traceback; `ZeroDivisionError` six lessons early; `print` with two values in a quiz, before any screen shows the space it puts between them. | First teaching: NameError in the asking-and-printing traceback, ZeroDivisionError in the error-reading trap; two-value `print` next appears in the savings-pot loop. | l2: "Your code stopped with an error. If its last line says `NameError`, a name is spelt differently in two places." l4: "A maths error, such as dividing by zero, would name a different error. NameError is about a name." l5 last sentence: "`print` shows both booleans on one line, with a space between them."

26. l10-reading-errors.json, l4-asking-and-printing.json | l10 `screens[0].prose`, `screens[1].prose`, `screens[2].prose`; l4 `screens[5].title` | continuity | The error-reading lesson re-teaches as new, in bold, what earlier lessons taught: **index** (strings, then lists), **slice** (strings), `len` (lists) and **traceback** (the input lesson read one, under the same title "Reading an error message" as this lesson's name). Its new content is lists' slices, multi-frame tracebacks and a cause that sits earlier. | Bold terms in l3 `screens[1].prose`, l8 `screens[0].explain.text`, l4 `screens[5]`. | l10 `screens[0].prose` first sentences: "As with text, square brackets after a list's name pick one value out by its index, counted from 0." l10 `screens[1].prose`: "A slice works on a list as it did on text: `prices[1:3]` takes a start index, a colon, then an end index. `len(prices)` is 4." l10 `screens[2].prose` second sentence: "Python prints a traceback, the error report you first read when converting input." l4 `screens[5].title`: "A first traceback".

27. l5-decisions.json, l8-many-values.json, l11-numbers-from-a-file.json, l12-savings-script.json | l5 `screens[2].explain.text`; l8 `screens[0].explain.text`; l11 `screens[2].prose`; l12 `screens[4].prose` | continuity | Terms bolded as new a second time: **booleans** (bool in the text lesson), **index** (text lesson), **list** (the for-each lesson), **f-string** (the text lesson). | Original bold: l3 `screens[3].explain.text` (bool), l3 `screens[1].prose` (index), l7 `screens[0].prose` (list), l3 `screens[7]` title (f-strings). | l5 second sentence: "`True` and `False` are the bool values you met with text, also called booleans." l8 first sentence: "The number in square brackets is the index, as with text: the position, counted from 0." l11: "`split` returns a list of pieces, so `[1]` picks the second one." (unbolded). l12: "A script should show money to the penny. As with text, an f-string fills the braces with values, and `:.2f` rounds a number to two decimal places."

28. l7-for-each.json, l10-reading-errors.json | l7 `screens[5].hints[1]`; l10 `screens[3].hints[1]` | layout | The point hints highlight a cell unrelated to their text: l7 lights the 3.00 cell for "`total = 0` is indented"; l10 lights the first price for "`NameError` means Python looked for a name". | Canvas cells are the list values. | l7: `"highlight": ["c0", "c1", "c2", "c3"]`, text "`total = 0` is indented, so it runs on every one of these passes." l10: change the rung to `"nudge"` and drop `highlight`.

29. l8-many-values.json, review-2.json | l8 `screens[9].widget.examples[0]`; review-2 `items[6].widget.examples[0]` | layout | Float examples with no `compare` (validator `float-example`): Run examples compares exactly while the hidden tests use `isclose`. | Validator warning. | Add `"compare": "isclose"` to both examples.

## Orchestrator (course.json; content agents do not edit it)

A. `first-python/L1` uses the maths order of operations and powers ("Python multiplies before it adds, as in maths"; `2 * 3 ** 2`) and turns percentages into decimals (`"4.5%"` to 0.045, returns printed ×100), with no edge. The mapping keeps first levels of Stage 0 courses open (`docs/reports/prereq-mapping.md`), so add diagnostics, not gates: `"requires": [ { "ref": "number-sense/L3", "why": "Predicts lines such as 2 * 3 ** 2 from the maths order of operations and powers.", "gate": false }, { "ref": "ratio/L1", "why": "Turns percentages into decimals, such as 4.5% into 0.045, and prints returns as percentages.", "gate": false } ]`.

B. `first-python/L2` (implicit `first-python/L1` only) grows savings by 1.07 a year and compares compound with simple interest (l6 `screens[8]`, `screens[9]`, `quiz[3]`; homework-2 `items[1]`, `items[2]`). Add: `"requires": [ "first-python/L1", { "ref": "ratio/L2", "why": "Grows savings by a yearly multiplier such as 1.07 and compares compound with simple interest." } ]`.

C. `first-python/L3` requires `terminal/L1` (files and folders), but l12 `screens[8]` asks the learner to `cd` into a folder and tell `cat` from `python3 savings.py`, which terminal teaches in L2 (`l5-where-am-i`, `l7-looking-inside`). No first-python screen uses a path beyond a bare file name. Replace the entry with `{ "ref": "terminal/L2", "why": "Uses cd to enter a folder and cat to show a file before running a script with python3." }` (terminal has no `requires`, so no cycle; `cpp/L1` already takes `terminal/L2` for the same reason).

D. `lessonNames["l12-savings-script"]` is "From prices to returns, as a script" and its objective "Write, save and run a complete script that reads prices and prints the returns", but the lesson is titled "A compound interest script" and spends nine of eleven screens on savings. Set `lessonNames["l12-savings-script"]` to "A compound interest script" and `lessonObjectives["l12-savings-script"]` to "Write, save and run scripts that project savings and turn a prices file into returns."

E. Each review has 8 items. L1 and L2 gate the next level and L3 gates `py-found/L1`, and AUTHORING section 11 asks 12 or more review items of a level others require, so a second test-out is a new paper. A content pass should add four fresh items to each review.

## Continuity

Notation and voice match across the three levels: `int`, `float`, `str`, `bool`, f-strings with `:.2f`, `:+.2f` and `:.2%`, £ to the penny, `daily_return(p0, p1)` reused from the functions lesson in the last transfer. Cross-references checked: `pytest` l11 and homework-3 cite "First Python Scripts (l10)" for `max_drawdown` with `range(1, len(prices) + 1)`, which matches l10 `screens[8]`'s starter. `py-found` L1 (`l2-slicing`) re-teaches indexing from 0 and negative indexes with an explore screen as if new; first-python teaches both (text lesson, list lesson, error-reading lesson). The `py-found` side should change, to a recall line. `cpp` L1's diagnostic edge to `first-python/L3` reads true. Findings 18, 22 to 27 are this course's own continuity findings.

## Engine

1. `tools/fresh-check.mjs --file`: the code-name check matched function names across courses (`average`, `average_close`, `best_day`) but not homework-3 `items[1]`'s `max_drawdown` against l10 `screens[8]` in the same course, where four of seven test `call` strings are identical. Compare a set item's test `call` strings with the lesson widgets of its own course, and report any shared call.
2. Validator (advisory): in function mode, when the solution (or starter) calls the tested function at module level, a `byKey` `test-N` line that names an exception (`TypeError`, `ValueError`, `IndexError`, "an error") can only arrive as `error`, because the load fails first. Five such lines here (finding 13). Warn on that pattern.
3. Validator (advisory): a ```` ```text ```` block that starts `Traceback (most recent call last):` where a code line is followed directly by the error line, or by another `File` line, with no `^` or `~` line between. Python 3.11+ and Pyodide 0.27.7 print one except when the failing expression is the whole line. 15 blocks here (finding 12).

Orchestrator (session W): A, B and D applied. C: first-python L3 now requires terminal/L3 (review-terminal-1-3 item 2: running python3 needs the install and command-finding taught in L3), which covers the cd and cat of terminal L2; not changed to L2. E (four fresh items per review, to 12) is deferred to its own authored task with a second read, recorded in PLAN and KNOWN_ISSUES; not part of this fix pass.

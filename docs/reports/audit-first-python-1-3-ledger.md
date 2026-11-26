# Claim ledger: first-python, levels 1 to 3 (blind audit, round 1)

Stage 0 depth (docs/briefs/concept-audit.md): definitions, rules, "always / never / every" claims, conventions, every graded key, wrong option and slip, every code-behaviour claim, and every `test-N` and `error` line of the code widgets. Hints and feedback lines have a row only where they state a rule or name a slip.

Bases. "concepts A, A2, B, C, D, E" are the sections of `docs/reports/first-python-L1-3-concepts.py` (795 checks; run on CPython 3.13 and inside Pyodide 0.27.7, Python 3.12.7, where the traceback checks are exact). "sweep" is `docs/reports/first-python-L1-3-test-line-sweep.mjs` (133 submissions through the page harness). "grade-all" is `tools/grade-all.mjs --code` on all 18 files (58 code widgets, 0 failures). Python documentation is cited by section (3.12).

Rows: 794. correct 765, imprecise 27, misleading 1, wrong 1, unverified 0.

## l1-calculator

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.options[fourteen]` | key: 14 | correct | run, concepts A: this is what Python does |
| `screens[0].widget.options[twenty]` | wrong option: 20 / You worked left to right: 2 + 3 first, then times 4. Python multiplie… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[0].widget.options[text]` | wrong option: 2 + 3 * 4 / You expected `print` to repeat what you typed. Without quotes, Python… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.options[float]` | key: 3.0 | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[1].widget.options[int]` | wrong option: 3 / You expected a whole answer because 6 splits evenly. The caption show… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[1].widget.options[half]` | wrong option: 3.5 / That is 7 / 2. With n at 6, the point for n / 2 sits exactly on 3. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[2].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[3].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[4].widget.options[three]` | key: 3 | correct | run, concepts A: this is what Python does |
| `screens[4].widget.options[four]` | wrong option: 4 / You rounded 3.8 to the nearest whole number. `//` always rounds down,… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[4].widget.options[decimal]` | wrong option: 3.8 / That is `19 / 5`. The double slash rounds down to a whole number. | correct | recomputed from the mistake its why names (concepts B) |
| `screens[4].widget.options[rem]` | wrong option: 4.0 / You rounded to the nearest number and kept a float. `//` on two ints … | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[eighteen]` | key: 18 | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[thirtysix]` | wrong option: 36 / You multiplied 2 by 3 first, then squared 6. The power binds to the 3… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[twelve]` | wrong option: 12 / You read the two stars as times 2. They mean a power: `3 ** 2` is 3 t… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[sixtyfour]` | wrong option: 64 / You worked out 2 to the power 6. The power belongs to 3 ** 2 only, wh… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[6].widget.options[avg]` | wrong option: 12.0 / You added the prices first, as the writer intended. Python divides be… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[6].widget.options[right]` | key: 17.0 | correct | run, concepts A: this is what Python does |
| `screens[6].widget.options[int]` | wrong option: 17 / The order is right, but `/` always gives a float. So the answer print… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[6].widget.options[twelve]` | wrong option: 12 / You added first and dropped the decimal point. Python halves 14 first… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[8].widget.options[div]` | key: `6 / 2` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[8].widget.options[sub]` | wrong option: `8 - 6` / You went left to right. Division outranks subtraction, so `6 / 2` goe… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[same]` | wrong option: Both at once / Python does one operation at a time, in a fixed order. Division comes… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.test-1` | test-1 line: If it printed 261.5, check your brackets: `262.5 - 250 / 250` divides first. | correct | sweep under the page harness: no brackets gives test-1 |
| `screens[9].feedback.byKey.error` | error line: Your code stopped with an error. Read the last line of the message under the editor. | correct | sweep under the page harness: NameError gives test-1; SyntaxError gives error |
| `quiz[q-precedence].widget.options[right]` | key: 11 | correct | run, concepts A: this is what Python does |
| `quiz[q-precedence].widget.options[lr]` | wrong option: 14 / You added 3 and 4 first. Multiplication goes before addition. | correct | recomputed from the mistake its why names (concepts B) |
| `quiz[q-precedence].widget.options[float]` | wrong option: 11.0 / No division here, and all the values are ints, so the result is an in… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-type].widget.options[float]` | key: <class 'float'> | correct | run, concepts A: this is what Python does |
| `quiz[q-type].widget.options[int]` | wrong option: <class 'int'> / You expected an int because 8 / 4 is exactly 2. `/` gives a float eve… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-type].widget.options[two]` | wrong option: 2.0 / That is what `print(8 / 4)` shows. `type(...)` names the type of the … | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-floor].widget.answer` | key: 3 | correct | run or recomputation, concepts A2 |
| `quiz[q-floor].feedback.byKey.nearest` | slip 4: You rounded 3.33 to the nearest. `//` rounds down. You cannot buy a fourth share with £2. | wrong | Finding 1: 3.33 to the nearest is 3; the slip value 4 is rounding up (concepts B, the one failing check) |
| `quiz[q-floor].feedback.byKey.decimal` | slip 3.3333: That is `20 / 6`. The double slash rounds down to a whole number. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[0].explain` | Python follows the usual order of operations; print shows the result, not the sum typed | correct | Language reference 6.17 Operator precedence; run |
| `screens[1].explain, summary.ideas[1]` | / always gives a float; // on two ints gives an int, rounded down | correct | Python tutorial 3.1.1; Language reference 6.7; grid of 156 int pairs incl. negatives (concepts E) |
| `screens[2].explain` | // is floor division: divides, then rounds down to a whole number | correct | Language reference 6.7 ("floor division"); grid, -7 // 2 == -4 |
| `screens[3].explain` | float is a number with a decimal point; int a whole number; type decides what Python can do | correct | Python tutorial 3.1.1; Language reference 3.2 |
| `screens[4].feedback.byKey.four, explain` | // always rounds down, never to the nearest | correct | grid (concepts E) |
| `screens[5].prose, explain` | ** is a power; powers come before multiplication; brackets always go first | correct | Language reference 6.5, 6.17; run |
| `screens[8].prose, summary.formula` | order: brackets, **, then * / //, then + -; ties left to right except powers: 2 ** 3 ** 2 is 2 ** 9 | correct | Language reference 6.17 (unary minus and % left out, not misstated); run 512 |
| `screens[9].prose` | return = (new - old) / old | correct | simple return; Hull, Options, Futures and Other Derivatives, ch. 4 conventions; convention stated in the item |

## l2-naming-a-value

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.options[right]` | key: 36 | correct | run, concepts A: this is what Python does |
| `screens[0].widget.options[text]` | wrong option: price * 3 / You read line 2 as text to repeat. `price` has no quotes, so Python l… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[0].widget.options[error]` | wrong option: An error: price is not a number / You expected Python to forget line 1. Line 1 stored 12 in price, and … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.answer` | place key: {'price': ['c12'], 'qty': ['c3']} | correct | run or recomputation, concepts A2 |
| `screens[1].feedback.byKey.c12` | wrong pick line: Line 1 says `price = 12`, so 12 goes into the price box. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.c3` | wrong pick line: Line 2 says `qty = 3`, so 3 goes into the qty box. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.c5` | wrong pick line: No line mentions 5, so it stays in the tray. | correct | true of the pick it names (trace of the snippet) |
| `screens[2].widget.answer` | place key: {'qty': ['c5'], 'tray': ['c3']} | correct | run or recomputation, concepts A2 |
| `screens[2].feedback.byKey.c5` | wrong pick line: Line 2 puts 5 into the qty box. | correct | true of the pick it names (trace of the snippet) |
| `screens[2].feedback.byKey.c3` | wrong pick line: You kept 3 in the box. Line 2 replaces it, so take the 3 out. | correct | true of the pick it names (trace of the snippet) |
| `screens[3].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[3].feedback.byKey.error` | error line: Your code stopped with an error. If its last line says `NameError`, a name is spelt differently in two p… | imprecise | Finding 2: a NameError keys as test-1 here (script mode); sweep |
| `screens[4].widget.answer` | place key: {'a': ['a7'], 'b': ['b7']} | correct | run or recomputation, concepts A2 |
| `screens[4].feedback.byKey.a7` | wrong pick line: You moved a's own 7 into b. Assignment copies: a keeps its 7 and b gets a 7 of its own. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.b7` | wrong pick line: Line 2 looks up a, finds 7, and puts a 7 into b. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.c10` | wrong pick line: No line mentions 10 yet, so it stays in the tray. | correct | true of the pick it names (trace of the snippet) |
| `screens[5].widget.answer` | place key: {'a': ['c10'], 'b': ['b7'], 'tray': ['a7']} | correct | run or recomputation, concepts A2 |
| `screens[5].feedback.byKey.b7` | wrong pick line: You changed b along with a. `b = a` copied 7 into b at that moment. It does not tie b to a for ever. | correct | true of the pick it names (trace of the snippet) |
| `screens[5].feedback.byKey.c10` | wrong pick line: Line 3 puts 10 into the a box. | correct | true of the pick it names (trace of the snippet) |
| `screens[5].feedback.byKey.a7` | wrong pick line: a can hold one value. Take its old 7 out when the 10 goes in. | correct | true of the pick it names (trace of the snippet) |
| `screens[6].widget.options[right]` | key: 6 | correct | run, concepts A: this is what Python does |
| `screens[6].widget.options[error]` | wrong option: An error, because x cannot equal x + 1 / You read `=` as the equals sign of algebra. In Python it means: work … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[five]` | wrong option: 5 / You expected line 2 to leave x alone. It works out 5 + 1 and puts 6 i… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[false]` | wrong option: False / You read line 2 as a question: is x equal to x + 1? A comparison uses… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[7].feedback.byKey.test-1` | test-1 line: Your program should print 640 on one line. Store the new value in `cash`, then print it. | correct | sweep under the page harness: not stored gives test-1; no print gives test-1; printed twice gives test-1 |
| `screens[8].widget.options[right]` | key: Works out `total + fee` with the old total | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[8].widget.options[check]` | wrong option: Checks whether total equals total + fee / That would be a comparison, written `==`. A single `=` assigns. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[move]` | wrong option: Empties the box total / Nothing is emptied first. The old total is needed to work out the rig… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.test-1` | test-1 line: If you printed 4560.0, value still holds the old position. Assign value again after the price changes. | correct | sweep under the page harness: stale value gives test-1 |
| `quiz[q-copy].widget.options[right]` | key: 4 | correct | run, concepts A: this is what Python does |
| `quiz[q-copy].widget.options[five]` | wrong option: 5 / You changed b along with a. `b = a` copied 4 into b, and line 3 chang… | correct | recomputed from the mistake its why names (concepts B) |
| `quiz[q-copy].widget.options[error]` | wrong option: An error / Every name here has a value before it is used, so nothing goes wrong. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-stale].widget.options[right]` | key: 30 | correct | run, concepts A: this is what Python does |
| `quiz[q-stale].widget.options[new]` | wrong option: 33 / You expected value to follow price. Line 2 worked out 30 once; line 3… | correct | recomputed from the mistake its why names (concepts B) |
| `quiz[q-stale].widget.options[expr]` | wrong option: price * 3 / value holds the result of the sum, not the sum itself. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-steps].widget.answer` | key: 7 | correct | run, concepts A |
| `quiz[q-steps].feedback.byKey.first` | slip 2: You kept the first value. Lines 2 and 3 each give x a new value. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-steps].feedback.byKey.order` | slip 9: You added before multiplying. Line 2 runs before line 3: 2 times 3 is 6, then 6 plus 1. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[0].explain` | a name that holds a value is a variable; line 2 looks the name up | correct | Python tutorial 3.1.1; Language reference 4.2 |
| `screens[1].explain` | = is the assignment sign: puts the value on its right into the name on its left | correct | Language reference 7.2 |
| `screens[2].explain` | a variable holds one value at a time, the latest | correct | Language reference 7.2 (rebinding) |
| `screens[3].prose` | A name starts with a letter and has no spaces | imprecise | Finding 8: Language reference 2.3 Identifiers: a letter or an underscore |
| `screens[3].explain` | Python reads names exactly: Price and price are two names | correct | Language reference 2.3 (case is significant) |
| `screens[4].explain` | For numbers, assigning one name from another copies the value | correct | Language reference 7.2: binds the same object; for immutable numbers indistinguishable from a copy; the hedge "for numbers" is stated |
| `screens[5].explain, summary.ideas[2]` | Changing a later never changes b / A later change to a leaves b where it was | imprecise | Finding 3: true for reassignment only; a list changed in place shows through b (Python tutorial 3.1.3, Language reference 3.1; concepts E note) |
| `screens[6].explain, screens[8].prose, summary` | right side first with the current values, then store; x = x + 1 means x becomes x plus 1 | correct | Language reference 7.2 ("evaluates the expression list ... and assigns") |
| `screens[9].explain` | value does not follow price: it holds the number worked out when its line ran | correct | run (concepts E): 4560.0, 4627.5, gain 67.50 |

## l3-text

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.options[right]` | key: 125 | correct | run, concepts A: this is what Python does |
| `screens[0].widget.options[sum]` | wrong option: 17 / You added 12 and 5 as numbers. The quotes make them text, and `+` joi… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[0].widget.options[spaced]` | wrong option: 12 5 / You expected a space between the parts. `+` joins text exactly, with … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.answer` | tap-regions key: ['r0c1', 'r0c2', 'r0c3'] | correct | run or recomputation, concepts A2 |
| `screens[1].feedback.byKey.stop-in` | wrong pick line: You included index 3, the U. A slice stops just before its second number. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.from-one` | wrong pick line: You started counting at 1. Python's first index is 0, the G. | correct | true of the pick it names (trace of the snippet) |
| `screens[2].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[2].feedback.byKey.test-1` | test-1 line: If you see USD missing its D, your stop is too small: the stop index is left out, so use 6. | correct | sweep under the page harness: stop 5 gives test-1 |
| `screens[3].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[4].widget.options[right]` | key: U | correct | run, concepts A: this is what Python does |
| `screens[4].widget.options[third]` | wrong option: P / You counted from 1, so the third character looked like index 3. Count… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[4].widget.options[rest]` | wrong option: USD / One number in square brackets picks a single character. A slice needs… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[4].widget.options[first]` | wrong option: GBP / That is `pair[0:3]`, the three characters before index 3. | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[right]` | key: False | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[true]` | wrong option: True / You compared what they look like on screen. A string is never equal t… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[error]` | wrong option: An error / `==` accepts any two values. A str and a number are never equal, so i… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[joined]` | wrong option: It prints Price: 12.5 / You expected `+` to turn the number into text. It joins only strings,… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[right]` | key: It stops with a TypeError | correct | run, concepts A: this is what Python does |
| `screens[6].widget.options[twodp]` | wrong option: It prints Price: 12.50 / Python never adds digits on its own. And here `+` cannot join a strin… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[7].feedback.byKey.test-1` | test-1 line: If you see 12.5 instead of 12.50, add `:.2f` after price inside the braces. | correct | sweep under the page harness: no .2f gives test-1 |
| `screens[8].widget.options[right]` | key: 5 | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[8].widget.options[six]` | wrong option: 6 / You counted both ends, 2 and 7. The stop index is left out, so it is … | correct | recomputed from the mistake its why names (concepts B) |
| `screens[8].widget.options[seven]` | wrong option: 7 / You read the stop as a length. The slice runs from index 2 up to 7, l… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.test-1` | test-1 line: If a line reads -8.5, add `.2f` to the format. If Monday has no plus sign, add the `+` before `.2f`. | correct | sweep under the page harness: no .2f gives test-1; no plus gives test-1 |
| `quiz[q-slice].widget.options[right]` | key: VOD | correct | run, concepts A: this is what Python does |
| `quiz[q-slice].widget.options[four]` | wrong option: VOD. / You kept index 3. The stop index is left out. | correct | recomputed from the mistake its why names (concepts B) |
| `quiz[q-slice].widget.options[from1]` | wrong option: OD. / You started at index 1. The first character is index 0. | correct | recomputed from the mistake its why names (concepts B) |
| `quiz[q-format].widget.options[right]` | key: Cost: £7.00 | correct | run, concepts A: this is what Python does |
| `quiz[q-format].widget.options[plain]` | wrong option: Cost: £7 / You ignored the format. `.2f` always shows two decimal places. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-format].widget.options[braces]` | wrong option: Cost: £{cost:.2f} / The `f` before the quotes makes Python fill in the braces. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-type].widget.options[right]` | key: <class 'str'> | correct | run, concepts A: this is what Python does |
| `quiz[q-type].widget.options[int]` | wrong option: <class 'int'> / You treated "3" as the number 3. It is text, and text times 2 is text… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-type].widget.options[error]` | wrong option: An error / Text times a whole number is allowed: it repeats the text. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[0].explain` | quotes make a str; + joins strings; * repeats | correct | Python tutorial 3.1.2; run |
| `screens[1].prose` | index counts from 0; s[0:3] takes index 0 up to index 3, leaving 3 out | correct | Python tutorial 3.1.2 ("start is always included, and the end always excluded") |
| `screens[3].explain` | bool has only the values True and False | correct | Library reference Boolean type |
| `screens[5].options[true].why` | A string is never equal to a number, whatever it spells | correct | Language reference 6.10.1 (different built-in types compare unequal); run |
| `screens[6].options[twodp].why` | Python never adds digits on its own | imprecise | Finding 9: print(0.1 + 0.2) shows 0.30000000000000004 (concepts E note); the point meant is no padding zeros |
| `screens[7].prose` | f before the quotes fills names in braces; .2f means two decimal places | correct | Python tutorial 7.1.1; Library reference Format Specification Mini-Language |
| `screens[8].prose` | s[a:b] holds b - a characters | imprecise | Finding 13: needs 0 <= a <= b <= len(s); the summary note says so, the prose does not |
| `summary.formula.note` | b - a when both lie inside the string | correct | grid of all a <= b on a 10-character string (concepts E) |
| `screens[9].prose` | +.2f always shows + or -, then two decimals | correct | Library reference format spec, sign option "+"; run |

## l4-asking-and-printing

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.options[right]` | key: 33 | correct | run, concepts A: this is what Python does |
| `screens[0].widget.options[six]` | wrong option: 6 / You expected `input()` to give a number. It always gives text, so qty… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[0].widget.options[error]` | wrong option: An error / Text times a whole number is allowed in Python: it repeats the text. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.answer` | tap-regions key: ['r0c1', 'r3c1', 'r5c1'] | correct | run or recomputation, concepts A2 |
| `screens[1].feedback.byKey.no-input` | wrong pick line: You missed `input()`. Whatever is typed, it hands back a str. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.looks` | wrong pick line: You marked every row with a 3 or a 6 in it. `int(...)` turns text into a number, so those values ar… | correct | true of the pick it names (trace of the snippet) |
| `screens[2].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[2].feedback.byKey.test-1` | test-1 line: If you see 250250, you multiplied the text. Convert with `int(typed)` first. | correct | sweep under the page harness: text times 2 gives test-1; text times 2, no qty gives test-1 |
| `screens[3].widget.options[right]` | key: It stops with a ValueError | correct | run, concepts A: this is what Python does |
| `screens[3].widget.options[seven]` | wrong option: It prints 7 / You expected `int` to drop the decimals. It does that to a float, but… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.options[eight]` | wrong option: It prints 8 / You expected rounding. `int` never rounds text: "7.5" is not a whole … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.options[float]` | wrong option: It prints 7.5 / `int` can only give a whole number. For decimals use `float`. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.options[type]` | wrong option: It stops with a TypeError / A TypeError means the wrong kind of value. Here `int` got text, the r… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[4].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[4].feedback.byKey.error` | error line: Your code stopped. If the message says ValueError, use `float` rather than `int` for decimal text. | imprecise | Finding 2: a ValueError keys as test-1 here; sweep |
| `screens[5].widget.options[right]` | key: Line 3 uses the name qty, which no line created | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[line1]` | wrong option: Line 1 is wrong: float cannot read "12.50" / You blamed the first line. The message names line 3, and lines 1 and … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[quotes]` | wrong option: qty needs quotes around it / Quotes would make qty the text "qty", and a price times text fails. T… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[maths]` | wrong option: Line 3 has a maths error / A maths error, such as dividing by zero, would name a different error… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[fifteen]` | wrong option: It prints 15 / You expected `input()` to give the number 10. It gives the text "10",… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[joined]` | wrong option: It prints 105 / You expected `+` to join the text and the number. `+` joins only two … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[right]` | key: It stops with a TypeError | correct | run, concepts A: this is what Python does |
| `screens[6].widget.options[value]` | wrong option: It stops with a ValueError / A ValueError means the right kind of value with the wrong contents. H… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[7].feedback.byKey.error` | error line: The program still stops. Read the last line of the message: which value is still text? | imprecise | Finding 2: the TypeError keys as test-1 here; sweep |
| `screens[8].widget.options[right]` | key: `price = float(input("Price: "))` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[8].widget.options[noconv]` | wrong option: `price = input("Price: ")` / This keeps the price as text, so any sum with it fails or repeats. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[int]` | wrong option: `price = int(input("Price: "))` / A price such as 12.75 would stop `int` with a ValueError. Use `float`. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.error` | error line: Your code stopped. A TypeError on the return line means a price is still text: convert with `float`. | imprecise | Finding 2: the TypeError keys as test-1 here; sweep |
| `screens[10].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[10].feedback.byKey.error` | error line: Your code stopped. A ValueError means the text still has its % sign: slice it off first. | imprecise | Finding 2: the ValueError keys as test-1 here; sweep |
| `quiz[q-input-type].widget.options[right]` | key: <class 'str'> | correct | run, concepts A: this is what Python does |
| `quiz[q-input-type].widget.options[int]` | wrong option: <class 'int'> / You expected Python to notice the digits. `input()` returns text what… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-input-type].widget.options[value]` | wrong option: 42 / That is what `print(x)` would show. `type(x)` names its type. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-convert].widget.answer` | key: 100 | correct | run, concepts A |
| `quiz[q-convert].feedback.byKey.forty` | slip 40: You kept qty alone. The line multiplies qty by price. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-convert].feedback.byKey.eighty` | slip 80: You read 2.5 as 2. `float` keeps the decimals. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-traceback].widget.options[right]` | key: Line 4 tried to read "12.5" as a whole number | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-traceback].widget.options[name]` | wrong option: A name on line 4 was not defined / That would be a NameError. The last line names a ValueError. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-traceback].widget.options[line1]` | wrong option: The error is on line 1 / Line 1 of the message is a heading. The place is `line 4`. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[0].explain, summary.ideas[0]` | input() always returns a str, whatever is typed | correct | Library reference built-in input(): "converts it to a string" |
| `screens[3]` | int reads whole-number text only; int drops the decimals of a float | correct | Library reference int(); run int("7.5"), int(7.5) == 7 |
| `screens[3].options[type].why, screens[6].options[value].why` | TypeError: wrong kind of value; ValueError: right kind, wrong contents | correct | Library reference Built-in Exceptions |
| `screens[5].explain, summary.ideas[2]` | read a traceback from the bottom: last line the error, File line above says where, ^ marks the part | correct | Python tutorial 8.2; exact traceback reproduced on Python 3.12.7 (concepts D) |
| `screens[10].prose` | text[0:-1] stops just before the end | correct | Python tutorial 3.1.2; run |
| `screens[10].explain` | Rates go into sums as decimals, never as percentages | correct | convention of the course (ratio/L1), stated |

## review-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.options[right]` | key: 5.0 | correct | run, concepts A: this is what Python does |
| `items[0].widget.options[added]` | wrong option: 4.0 / You added 2 and 6 first. Division comes before addition. | correct | recomputed from the mistake its why names (concepts B) |
| `items[0].widget.options[int]` | wrong option: 5 / The order is right, but `/` always gives a float, so Python prints 5.… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[1].widget.options[right]` | key: 380 | correct | run, concepts A: this is what Python does |
| `items[1].widget.options[follow]` | wrong option: 300 / You expected cash to follow the new cost. Line 3 ran once, with cost … | correct | recomputed from the mistake its why names (concepts B) |
| `items[1].widget.options[start]` | wrong option: 500 / Line 3 stores a new value in cash, so it is no longer 500. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[2].widget.options[right]` | key: 10 | correct | run, concepts A: this is what Python does |
| `items[2].widget.options[stop]` | wrong option: 10- / You kept index 7, the dash. The stop index is left out. | correct | recomputed from the mistake its why names (concepts B) |
| `items[2].widget.options[from1]` | wrong option: -1 / You counted from 1. Index 5 is the sixth character, the 1 of 10. | correct | recomputed from the mistake its why names (concepts B) |
| `items[3].widget.options[right]` | key: Cost: £42.00 | correct | run, concepts A: this is what Python does |
| `items[3].widget.options[nodp]` | wrong option: Cost: £42.0 / You ignored the format. `.2f` always shows two decimal places. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[3].widget.options[braces]` | wrong option: Cost: £{shares * price:.2f} / The `f` before the quotes makes Python fill in the braces. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[4].widget.answer` | key: 12 | correct | run, concepts A |
| `items[4].feedback.byKey.nearest` | slip 13: You rounded 3.6 to 4. Floor division always rounds down, to 3. | correct | recomputed from the mistake its line names (concepts B) |
| `items[4].feedback.byKey.times` | slip 9: You read `3 ** 2` as 3 times 2. Two stars mean a power: 3 squared is 9. | correct | recomputed from the mistake its line names (concepts B) |
| `items[5].widget.options[right]` | key: P&L: -12.50 | correct | run, concepts A: this is what Python does |
| `items[5].widget.options[both]` | wrong option: P&L: +-12.50 / You read the `+` as text to print. In a format it means: always show … | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[5].widget.options[short]` | wrong option: P&L: -12.5 / You ignored `.2f`. It always prints two decimal places. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[6].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[6].feedback.byKey.error` | error line: Your code stopped. A TypeError means one value is still text: convert it first. | imprecise | Finding 2: the TypeError keys as test-1 here; sweep |
| `items[7].widget.options[right]` | key: `total = price + float(fee)` | correct | run or recomputation, concepts A2: this is what Python does |
| `items[7].widget.options[str]` | wrong option: `total = str(price) + fee` / That joins two strings, so a fee of 1.5 gives the text "99.51.5", not… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[7].widget.options[quotes]` | wrong option: `total = price + "fee"` / Quotes make the word fee itself into text. A float plus text still fa… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[7].widget.options[int]` | wrong option: `total = int(price) + fee` / The left side was never the problem. fee is still a str on the right. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |

## homework-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.options[right]` | key: -4 | correct | run, concepts A: this is what Python does |
| `items[0].widget.options[chop]` | wrong option: -3 / You dropped the decimals of -3.5. Floor division rounds down, and dow… | correct | recomputed from the mistake its why names (concepts B) |
| `items[0].widget.options[float]` | wrong option: -3.5 / That is `-7 / 2`. The double slash rounds down to a whole number. | correct | recomputed from the mistake its why names (concepts B) |
| `items[1].widget.answer` | key: 16 | correct | run, concepts A |
| `items[1].feedback.byKey.linked` | slip 24: You changed a when b changed. `b = a` copied 4; tripling b leaves a at 4, so a becomes 4 + 12. | correct | recomputed from the mistake its line names (concepts B) |
| `items[1].feedback.byKey.stale` | slip 8: You used b's old value, 4. Line 3 made b 12 before line 4 ran. | correct | recomputed from the mistake its line names (concepts B) |
| `items[2].widget.answer` | key: 4 | correct | run, concepts A |
| `items[2].feedback.byKey.bracketed` | slip 2.2222: You added 2 and 18 first. Addition comes last. | correct | recomputed from the mistake its line names (concepts B) |
| `items[2].feedback.byKey.divfirst` | slip 38: You divided 18 by 3 before the power. Powers come first: `3 ** 2` is 9. | correct | recomputed from the mistake its line names (concepts B) |
| `items[3].widget.options[right]` | key: The text has a comma, which float cannot read | correct | run, concepts A: this is what Python does |
| `items[3].widget.options[int]` | wrong option: float cannot read decimals; int is needed / float is the one that reads decimals. int would fail too, because of … | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[3].widget.options[line1]` | wrong option: Line 1 is wrong: text cannot hold numbers / Line 1 ran fine. The message points at line 2 and quotes the text flo… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[3].widget.options[name]` | wrong option: The name typed was never defined / That would be a NameError. The last line names a ValueError. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[4].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[4].feedback.byKey.test-1` | test-1 line: If the line reads -0.04 or -0.036, multiply by 100 before formatting. If it lacks a sign, use `+.2f`. | imprecise | Finding 5: "If it lacks a sign" cannot fail the test: the value is negative, so .2f and +.2f print the same; sweep (pass) |
| `items[5].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[5].feedback.byKey.test-1` | test-1 line: If the fee reads £635.00, you used 0.25 as the rate. Divide by 100 to turn the percentage into a decimal. | correct | sweep under the page harness: rate 0.25 gives test-1 |
| `items[6].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[6].feedback.byKey.test-1` | test-1 line: Check the sign format `+.2f` on both lines, and that the return is multiplied by 100. | imprecise | Finding 5: both values are negative, so the + in the format is never tested; sweep (pass) |
| `items[7].model` | model answer and rubric: **What it prints.** The user types 50, so `price` is the text `"50"`. ```text 5… | correct | every printed output and error in the model run (concepts A, the model blocks) |
| `items[0].explain` | for positive numbers dropping the decimals and rounding down agree; for negatives they do not | correct | int(-3.5) == -3, -7 // 2 == -4 (concepts B) |
| `items[3].feedback.correct` | float reads digits, one point and a sign, not commas | correct | Library reference float() grammar (also exponents and underscores, not misstated for this item); run |

## l5-decisions

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.answer` | tap-regions key: ['sell'] | correct | run or recomputation, concepts A2 |
| `screens[0].feedback.byKey.hold` | wrong pick line: You followed the False arrow. 97.40 is less than 98.00, so the answer is True. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].widget.options[right]` | key: `sell`, then `done` | correct | run, concepts A: this is what Python does |
| `screens[1].widget.options[only-sell]` | wrong option: `sell` only / You treated `print("done")` as part of the `if` block. It is not inde… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.options[both]` | wrong option: `sell`, `hold`, then `done` / You ran both blocks. The `else` block runs only when the condition is… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.options[else]` | wrong option: `hold`, then `done` / You took the `else` block. `97.40 < 98.00` is `True`, so the `if` blo… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[right]` | key: `False` | correct | run, concepts A: this is what Python does |
| `screens[2].widget.options[price]` | wrong option: `101.25` / You expected `below` to hold a price. It holds the answer to the comp… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[flip]` | wrong option: `True` / You read the sign the wrong way round. 101.25 is above 98.00, so `pri… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[name]` | wrong option: `below` / `below` has no quotes, so it is a variable name. Python prints the va… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.answer` | tap-regions key: ['hold'] | correct | run or recomputation, concepts A2 |
| `screens[3].feedback.byKey.sell` | wrong pick line: You read `<` as 'at or below'. A number is never less than itself, so `98.00 < 98.00` is `False`. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].widget.answer` | tap-regions key: ['q1', 'q2', 'take'] | correct | run or recomputation, concepts A2 |
| `screens[4].feedback.byKey.sell` | wrong pick line: You took the True arrow at the first question. 112.50 is not below 98.00, so that answer is False. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.hold` | wrong pick line: You took the False arrow at the second question. 112.50 is above 110.00, so the answer is True. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.q1` | wrong pick line: Every price passes through the first question. Tap it too. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.q2` | wrong pick line: The first answer is False, so the program asks the second question before acting. Tap it too. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.take` | wrong pick line: Follow the second question's True arrow to the step the program carries out. | correct | true of the pick it names (trace of the snippet) |
| `screens[5].widget.options[right]` | key: `up` | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[best]` | wrong option: `big up` / You picked the branch that fits best. Python takes the first `True` c… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[all]` | wrong option: `up`, then `big up` / You ran every branch whose condition holds. Once one branch runs, the… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[else]` | wrong option: `flat or down` / You took the `else` branch. 6.5 is above 2, so the first condition is… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[runs]` | wrong option: It prints `send order`. / You read `=` as 'is equal to'. In Python one `=` stores a value, and … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[right]` | key: Python stops with a `SyntaxError` before running any line. | correct | run, concepts A: this is what Python does |
| `screens[6].widget.options[nothing]` | wrong option: It prints nothing, because the test fails. / You expected a False answer. Python never asks the question: it rejec… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.options[stores]` | wrong option: It stores `"buy"` in `signal` again, then prints `send orde… / Some languages do that. Python refuses a single `=` inside a conditio… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[7].feedback.byKey.error` | error line: Your code stopped with an error. Check the colon at the end of each `if`, `elif` and `else` line, and th… | correct | sweep under the page harness: missing colon gives error |
| `screens[8].widget.options[right]` | key: `if qty == 0:` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[8].widget.options[single]` | wrong option: `if qty = 0:` / One `=` stores a value. Python rejects it inside a condition with a S… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[text]` | wrong option: `if qty == "0":` / That compares with the text `"0"`. A number never equals text, so thi… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[not]` | wrong option: `if qty != 0:` / `!=` means 'not equal', so this asks the opposite question. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.solution` | solution and 5 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.test-2` | test-2 line: A price exactly on the stop must hold. Use `<`, not `<=`. | correct | sweep under the page harness: <= gives test-2 |
| `quiz[q-at-least].widget.options[right]` | key: `large` | correct | run, concepts A: this is what Python does |
| `quiz[q-at-least].widget.options[strict]` | wrong option: `small` / You read `>=` as `>`. `>=` includes equal, so `100 >= 100` is `True`. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-at-least].widget.options[both]` | wrong option: `large`, then `small` / You ran both blocks. `else` runs only when the condition is `False`. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-loss-chain].widget.options[right]` | key: `big loss` | correct | run, concepts A: this is what Python does |
| `quiz[q-loss-chain].widget.options[general]` | wrong option: `loss` / You went to the last branch that fits. Python takes the first `True` … | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-loss-chain].widget.options[all]` | wrong option: `big loss`, then `loss` / You ran every branch whose condition holds. After one branch runs, th… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-loss-chain].widget.options[none]` | wrong option: Nothing / You expected nothing without an `else`. Here the second condition is … | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-equal-and-less].widget.options[right]` | key: `True False` | correct | run, concepts A: this is what Python does |
| `quiz[q-equal-and-less].widget.options[le]` | wrong option: `True True` / You treated `<` as 'at or below'. 98.00 is not less than itself. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-equal-and-less].widget.options[ff]` | wrong option: `False False` / You expected `==` to fail. The two prices are the same value, so `==`… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-equal-and-less].widget.options[values]` | wrong option: `98.0 98.0` / `print` shows the comparisons' answers, which are booleans, not the p… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-reject].widget.options[right]` | key: `if pnl = 0:` | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-reject].widget.options[eq]` | wrong option: `if pnl == 0:` / This is the correct way to ask 'is `pnl` equal to 0?'. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-reject].widget.options[le]` | wrong option: `if pnl <= 0:` / `<=` is a valid comparison: 'less than or equal to'. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-reject].widget.options[store]` | wrong option: `flat = pnl == 0` / This is allowed. The right side is a comparison, and its boolean is s… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[1].explain, summary` | if block runs only when the condition is True, else block only when False; unindented line runs either way | correct | Python tutorial 4.1; Language reference 8.1 |
| `screens[2].explain` | An if line only asks whether its condition's value is True | imprecise | Finding 7: any truthy value runs the block (Library reference Truth Value Testing; concepts E note) |
| `screens[3].explain` | < is strict; <= reads less than or equal to | correct | Language reference 6.10 |
| `screens[4].explain, screens[5].explain, summary.formula.note` | elif: questions asked in order; at most one branch runs, the first True one | correct | Language reference 8.1 |
| `screens[6].hints[2], quiz[q-reject].prose` | Python reads the whole program before running it | correct | Language reference 2 and 9.1: the file is compiled first; run: SyntaxError before any print |
| `screens[6].explain` | SyntaxError text "invalid syntax. Maybe you meant '==' or ':=' instead of '='?" | correct | run on 3.12.7 and 3.13 (concepts C) |
| `screens[8].options[text].why, explain` | A number never equals text | correct | Language reference 6.10.1; run |
| `screens[9].explain` | real stop orders differ on whether they fire at the level: < against <= | correct | the item states its own rule (strictly below); convention stated |

## l6-until-done

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.rows` | table keys: [[0], [1], [2], [3]] | correct | trace recomputed (concepts A2 or B) |
| `screens[0].feedback.byKey.r0c1` | cell line: On the first arrival line 3 has not run yet, so `n` is still 0. | correct | true of its cell (trace, concepts) |
| `screens[0].feedback.byKey.r3c1` | cell line: Three passes through line 3 come before the 4th arrival, so `n` is 3. | correct | true of its cell (trace, concepts) |
| `screens[1].widget.options[right]` | key: 0, 1 and 2, one per line | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[1].widget.options[after]` | wrong option: 1, 2 and 3, one per line / You printed after adding 1. Line 3 prints before line 4 adds, so the … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[1].widget.options[extra]` | wrong option: 0, 1, 2 and 3, one per line / You ran the block when `n` was 3. `3 < 3` is `False`, so the loop end… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[1].widget.options[once]` | wrong option: 0 only / You ran the block once, as `if` would. A `while` loop goes back to li… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[2].widget.answer` | key: -2 | correct | run or recomputation, concepts A2 |
| `screens[2].feedback.byKey.last-positive` | slip 1: You stopped at 1. `1 > 0` is still `True`, so the block runs once more and `k` becomes −2. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[2].feedback.byKey.zero` | slip 0: `k` never lands on 0: it steps 10, 7, 4, 1, −2. The loop stops when the test fails, not at a target… | correct | recomputed from the mistake its line names (concepts B) |
| `screens[2].feedback.byKey.start` | slip 10: The loop changes `k` before line 4 runs. Line 4 shows the value after the last pass. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[2].feedback.byKey.sign` | slip 2: The last positive value is 1, and the next pass gives 1 − 3, which is −2. A positive 2 takes 3 − 1,… | correct | recomputed from the mistake its line names (concepts B) |
| `screens[3].widget.rows` | table keys: [[120, 1], [140, 2], [160, 3]] | correct | trace recomputed (concepts A2 or B) |
| `screens[3].feedback.byKey.r2c1` | cell line: After pass 2 the balance is 140, still below 150, so pass 3 runs and gives 160. | correct | true of its cell (trace, concepts) |
| `screens[4].widget.options[lt]` | wrong option: `n = 1` with `while n < 5:` / You stopped at `n < 5`. When `n` reaches 5 the test is `False`, so 5 … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[4].widget.options[right]` | key: `n = 1` with `while n <= 5:` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[4].widget.options[zero-le]` | wrong option: `n = 0` with `while n <= 5:` / You started the counter at 0, so 0 prints first: six numbers. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[4].widget.options[zero-lt]` | wrong option: `n = 0` with `while n < 5:` / This prints 0 to 4: it starts one too low and stops one too early. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[5].widget.options[right]` | key: It prints 1 again and again, and never reaches line 4. | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[5].widget.options[grows]` | wrong option: It prints 1 to 5, then `done`. / You expected `n` to grow by itself. No line in the block changes `n`,… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[5].widget.options[once]` | wrong option: It prints 1, then `done`. / You treated `while` like `if`. After the block, Python goes back to l… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[5].widget.options[error]` | wrong option: Python stops with an error before printing. / Every line here is valid Python. The problem only shows when it runs:… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[6].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[6].feedback.byKey.error` | error line: Your code stopped with an error or ran too long. Check that the block changes `value`, so the test can f… | imprecise | Finding 2: a loop that runs too long keys as test-1 ("Stopped after 5 s on this test"), not error; sweep |
| `screens[7].widget.options[right]` | key: 4 | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[7].widget.options[ten]` | wrong option: 5 / You let 10 through. `10 < 10` is `False`, so the block runs for 2, 4,… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[7].widget.options[ones]` | wrong option: 8 / You counted every number from 2 to 9. The counter jumps by 2 each pas… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[7].widget.options[skip-first]` | wrong option: 3 / You skipped the first pass. The block runs with `n` equal to 2 before… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[8].widget.rows` | table keys: [[1070.0, 1], [1144.9, 2], [1225.04, 3]] | correct | trace recomputed (concepts A2 or B) |
| `screens[8].feedback.byKey.r1c1` | cell line: You added £70 again. The second year's 7% is on £1,070.00, so it adds £74.90. | imprecise | Finding 10: names the 1140.00 mistake but shows for every wrong value in the cell (table.js keys a miss by cell id) |
| `screens[8].feedback.byKey.r2c1` | cell line: Multiply £1,144.90 by 1.07: £1,225.04 to the penny. | correct | true of its cell (trace, concepts) |
| `screens[9].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.error` | error line: Your code stopped with an error or ran too long. Check that the block changes `balance`. | imprecise | Finding 2: a loop that runs too long keys as test-1, not error; sweep |
| `quiz[q-zero-passes].widget.options[right]` | key: `50.0` | correct | run, concepts A: this is what Python does |
| `quiz[q-zero-passes].widget.options[hundred]` | wrong option: `100.0` / You expected the loop to run until the test fails. It fails on the fi… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-zero-passes].widget.options[once]` | wrong option: `40.0` / You ran the block once, as if the test came at the end. It comes firs… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-zero-passes].widget.options[forever]` | wrong option: Nothing: it never ends / This loop never starts, so it cannot run for ever. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-count-prints].widget.answer` | key: 3 | correct | run, concepts A |
| `quiz[q-count-prints].feedback.byKey.fifteen` | slip 4: You counted 15. `15 < 15` is `False`, so 15 is never printed. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-count-prints].feedback.byKey.ones` | slip 12: The counter jumps by 4, not 1. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-never-ends].widget.options[right]` | key: `while x > 0:` with `x = x + 1` | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-never-ends].widget.options[down]` | wrong option: `while x > 0:` with `x = x - 1` / This counts down to 0, and `0 > 0` is `False`, so it ends. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-never-ends].widget.options[up]` | wrong option: `while x < 100:` with `x = x + 1` / This counts up to 100 and stops there. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-never-ends].widget.options[double]` | wrong option: `while x < 1000:` with `x = x * 2` / Doubling reaches 1280 after seven passes, which fails the test. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-to-1500].widget.answer` | key: 5 | correct | run or recomputation, concepts A2 |
| `quiz[q-to-1500].feedback.byKey.four` | slip 4: After 4 years the balance is £1,464.10, still below £1,500.00, so the loop runs a 5th time. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[0].explain, summary.ideas[0]` | while: test, block if True, back to the test | correct | Python tutorial 3.2; Language reference 8.2 |
| `screens[2].explain` | a loop stops when its test is False, which need not be at a round number | correct | run: 10, 7, 4, 1, -2 |
| `screens[4].explain` | n < 6 is the same test as n <= 5 for whole numbers | correct | checked for n in -10..19 (concepts E) |
| `screens[5].explain` | infinite loop; in the exercises tests stop after 5 seconds | correct | app/js/screens/drill-worker.js header: 5-second limit |
| `screens[7].prose, summary.formula` | passes = ceil((b - a)/s) for a counter from a in steps s under while n < b | correct | all a in -5..7, b in a+1..24, s in 1..6 (concepts E); the summary states s > 0, a < b and zero passes otherwise |
| `screens[8].explain` | doubles in 11 years, not the 1/0.07 = 14.3 of simple interest | correct | run (concepts E) |
| `screens[9].explain` | 1.07^10 = 1.967, 1.07^11 = 2.105; rule of 72 gives 10.3 | correct | recomputed (concepts E) |

## l7-for-each

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.answer` | tap-regions key: ['c1'] | correct | run or recomputation, concepts A2 |
| `screens[0].feedback.byKey.c0` | wrong pick line: That is the first pass. Each pass moves `p` one value to the right. | correct | true of the pick it names (trace of the snippet) |
| `screens[0].feedback.byKey.c2` | wrong pick line: You skipped a value. The second pass takes the second value, −4.00. | correct | true of the pick it names (trace of the snippet) |
| `screens[0].feedback.byKey.c3` | wrong pick line: That is the last pass. The second pass takes the second value. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].widget.options[right]` | key: 0, 1, 2 and 3, one per line | correct | run, concepts A: this is what Python does |
| `screens[1].widget.options[from-one]` | wrong option: 1, 2, 3 and 4, one per line / You started at 1. `range(4)` starts at 0 and gives four numbers. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.options[to-four]` | wrong option: 0, 1, 2, 3 and 4, one per line / You included 4. `range(4)` stops before 4, so it gives four numbers, … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.options[once]` | wrong option: 4 / You printed the 4 itself. The loop runs once per number in the range,… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.answer` | None key: None | correct | run or recomputation, concepts A2 |
| `screens[3].widget.answer` | key: 15 | correct | run, concepts A |
| `screens[3].feedback.byKey.with-six` | slip 21: You included 6. `range(1, 6)` stops before 6, so the last number is 5. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[3].feedback.byKey.last` | slip 5: You gave the last value of `k`. `total` collects every value, so print shows the sum. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[3].feedback.byKey.from-zero` | slip 10: You used 0 to 4, which is `range(5)`. `range(1, 6)` starts at 1. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[4].widget.answer` | tap-regions key: ['c0', 'c3', 'c5'] | correct | run or recomputation, concepts A2 |
| `screens[4].feedback.byKey.flat` | wrong pick line: You counted the 0.0 day. `0.0 > 0` is `False`: a flat day is not an up day. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.c2` | wrong pick line: You counted the 0.0 day. `0.0 > 0` is `False`: a flat day is not an up day. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.c1` | wrong pick line: −1.2 is below 0, so `r > 0` is `False` on that pass. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.c4` | wrong pick line: −0.4 is below 0, so `r > 0` is `False` on that pass. | correct | true of the pick it names (trace of the snippet) |
| `screens[5].widget.options[sum]` | wrong option: `18.75` / You expected the total of all four. `total = 0` is inside the loop no… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[right]` | key: `3.0` | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[zero]` | wrong option: `0` / The reset comes before the addition on each pass, so the last pass le… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[error]` | wrong option: An error: `total` is used before it exists / `total = 0` runs on every pass before `total + p`, so `total` always … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.solution` | solution and 5 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[6].feedback.byKey.test-1` | test-1 line: `sum_to(5)` should be 15. If you got 10, the range stops before 5: use `range(1, n + 1)`. | correct | sweep under the page harness: range(1, n) gives test-1; range(n) gives test-1 |
| `screens[7].widget.options[right]` | key: `range(1, 13)` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[7].widget.options[twelve]` | wrong option: `range(12)` / That gives 0 to 11: twelve numbers, but starting at 0. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[7].widget.options[short]` | wrong option: `range(1, 12)` / That stops before 12, so it gives 1 to 11. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[7].widget.options[long]` | wrong option: `range(0, 13)` / That gives 0 to 12: thirteen numbers. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.solution` | solution and 5 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.test-1` | test-1 line: If test 1 got 4, you counted the 0.0 day. A return of exactly 0.0 is flat, not up: use `r > 0`, not `r >… | correct | sweep under the page harness: >= gives test-1 |
| `quiz[q-range-two-five].widget.options[right]` | key: 2, 3 and 4 | correct | run, concepts A: this is what Python does |
| `quiz[q-range-two-five].widget.options[to-five]` | wrong option: 2, 3, 4 and 5 / You included 5. `range(2, 5)` stops before 5. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-range-two-five].widget.options[zero]` | wrong option: 0, 1, 2, 3 and 4 / You started at 0. `range(2, 5)` starts at its first number, 2. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-range-two-five].widget.options[count]` | wrong option: 3 / You printed how many numbers there are. The loop prints each one. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-lines].widget.answer` | key: 4 | correct | run, concepts A |
| `quiz[q-lines].feedback.byKey.inside` | slip 6: You printed `report` on every pass. It is not indented, so it runs once, after the loop. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-lines].feedback.byKey.three` | slip 3: You missed `report`. It runs once, after the loop ends. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-losses-only].widget.answer` | key: -1.5 | correct | run, concepts A |
| `quiz[q-losses-only].feedback.byKey.all` | slip 2.0: You added every value. The `if` lets only negative returns into the total. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-losses-only].feedback.byKey.last` | slip -1.0: You kept only the last loss. `total` adds each negative return to what it already holds. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-losses-only].feedback.byKey.gains` | slip 3.5: You added the positive values. The test is `r < 0`, so only losses are added. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-losses-only].feedback.byKey.sign` | slip 1.5: Only the two negative returns pass the test, so the total is −0.5 + (−1.0), which is −1.5. A positi… | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-empty-list].widget.options[right]` | key: It prints `0`. | correct | run, concepts A: this is what Python does |
| `quiz[q-empty-list].widget.options[error]` | wrong option: It stops with an error, because the list is empty. / Looping over an empty list is allowed: the block simply runs zero tim… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-empty-list].widget.options[nothing]` | wrong option: It prints nothing. / `print(total)` is outside the loop, so it runs once whatever the list… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-empty-list].widget.options[none]` | wrong option: It prints `None`. / `total` was set to 0 before the loop, and nothing changed it. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[0].explain, summary.ideas[0]` | for hands the items over one per pass; an empty list gives zero passes | correct | Python tutorial 4.2; Language reference 8.3; run |
| `screens[1].explain, screens[7].prose, summary.ideas[1]` | range(n) is 0..n-1; range(a, b) is a..b-1; count b - a whenever b >= a | correct | Python tutorial 4.3; grid (concepts E) |
| `screens[3].explain, screens[7].prose` | accumulator: starts before the loop, every pass adds to it; computes the sum | correct | run |
| `screens[5].explain` | lines before the for run once; lines inside run every pass | correct | Language reference 8.3; run 3.0 |
| `screens[9].explain` | hit rate = up days divided by the number of days | correct | standard usage (fraction of winning periods); "every backtest reports" is idiom |

## l8-many-values

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.answer` | tap-regions key: ['c2'] | correct | run or recomputation, concepts A2 |
| `screens[0].feedback.byKey.c1` | wrong pick line: You counted from 1. Python numbers positions from 0, so `prices[2]` is the third value. | correct | true of the pick it names (trace of the snippet) |
| `screens[0].feedback.byKey.c3` | wrong pick line: You counted one too far. Positions run 0, 1, 2 from the left. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].widget.options[right]` | key: `104.75 5` | correct | run, concepts A: this is what Python does |
| `screens[1].widget.options[last-index]` | wrong option: `104.75 4` / You gave the last index, 4. `len` counts the values, and there are 5. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.options[first]` | wrong option: `101.2 5` / You read `-1` as the first value. A negative index counts from the en… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.options[error]` | wrong option: An error: there is no index −1 / Negative indexes are allowed. `-1` is the last value, `-2` the one be… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[right]` | key: `[100.0, 101.25]` | correct | run, concepts A: this is what Python does |
| `screens[2].widget.options[added]` | wrong option: `[99.8, 101.25, 100.0]` / You treated `closes[0] = ...` as adding. Assigning to an index replac… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[front]` | wrong option: `[100.0, 99.8, 101.25]` / You inserted at the front. `closes[0] = 100.00` overwrites position 0… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[second]` | wrong option: `[99.8, 100.0]` / You replaced the second value. Index 0 is the first. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.answer` | None key: None | correct | run or recomputation, concepts A2 |
| `screens[4].widget.answer` | tap-regions key: ['c2', 'c4'] | correct | run or recomputation, concepts A2 |
| `screens[4].feedback.byKey.ties` | wrong pick line: The second 52.00 equals the peak. `52.0 > 52.0` is `False`, so nothing changes. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.first` | wrong pick line: `peak` already starts at the first price, so pass 1 changes nothing. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.c3` | wrong pick line: The second 52.00 equals the peak. `52.0 > 52.0` is `False`, so nothing changes. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.c1` | wrong pick line: 48.00 is below the peak of 50.00. | correct | true of the pick it names (trace of the snippet) |
| `screens[4].feedback.byKey.c5` | wrong pick line: 51.00 is below the peak of 55.00. | correct | true of the pick it names (trace of the snippet) |
| `screens[5].widget.options[largest]` | wrong option: `-45.5` / That is the best day, but `best` starts at 0 and no loss is above 0. … | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[right]` | key: `0` | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[first]` | wrong option: `-120.0` / You started from the first P&L. This code starts `best` at 0 instead. | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[sum]` | wrong option: `-245.5` / You added the days up. The loop keeps the largest, not the total. | correct | recomputed from the mistake its why names (concepts B) |
| `screens[6].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[6].feedback.byKey.error` | error line: Your code stopped with an error. If it is an `IndexError`, `values[0]` ran on the empty list: put it ins… | imprecise | Finding 2: the IndexError on the empty list keys as test-4, not error; sweep |
| `screens[7].widget.options[right]` | key: `ok` for 0.4, −0.8 and 1.1, then `limit hit -2.6` | correct | run, concepts A: this is what Python does |
| `screens[7].widget.options[carry-on]` | wrong option: `ok` for 0.4, −0.8 and 1.1, `limit hit -2.6`, `ok 0.9`, the… / You carried on after `break`. It ends the whole loop, so the last two… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.options[ok-too]` | wrong option: `ok` for 0.4, −0.8 and 1.1, `limit hit -2.6`, then `ok -2.6` / You finished the pass after `break`. It leaves at once, so `ok -2.6` … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.options[first-neg]` | wrong option: `ok 0.4`, then `limit hit -0.8` / You stopped at the first loss. −0.8 is not below −2.0, so it passes. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[8].widget.options[right]` | key: 7 | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[8].widget.options[len]` | wrong option: 8 / That is the length. Indexes start at 0, so the last is one less. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[one]` | wrong option: 1 / That counts from the end with a positive number. The last value is at… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[neg]` | wrong option: −8 / `prices[-8]` is the first value of an 8-long list, not the last. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[9].feedback.byKey.test-1` | test-1 line: Check that you append on every day, not only when the peak changes. | correct | sweep under the page harness: append only on change gives test-1; append only on change, from 0 gives test-1 |
| `quiz[q-index-sum].widget.answer` | key: 24 | correct | run, concepts A |
| `quiz[q-index-sum].feedback.byKey.from-one` | slip 20: You took `x[1]` as the first value, 4. Index 1 is the second value, 8. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-index-sum].feedback.byKey.neg-second-last` | slip 23: You took `x[-1]` as 15. Index −1 is the last value, 16. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-empty-index].widget.options[right]` | key: It prints `0`, then stops with an `IndexError`. | correct | run, concepts A: this is what Python does |
| `quiz[q-empty-index].widget.options[zeros]` | wrong option: It prints `0` twice. / An empty list has no value at index 0, so Python cannot print one. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-empty-index].widget.options[none]` | wrong option: It prints `0`, then `None`. / Python does not fill in missing values. Asking for one is an error. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-empty-index].widget.options[first-line]` | wrong option: It stops with an error before printing anything. / `len([])` is fine: it is 0. Only the second line fails. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-break-count].widget.answer` | key: 3 | correct | run, concepts A |
| `quiz[q-break-count].feedback.byKey.counted-break` | slip 4: You counted −5. `break` comes before `count = count + 1`, so that pass adds nothing. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-break-count].feedback.byKey.no-break` | slip 5: You counted every value. `break` ends the loop at −5. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-break-count].feedback.byKey.skipped-neg` | slip 2: −1 is not below −2, so it is counted. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-lowest-start].widget.options[right]` | key: `low = prices[0]` | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-lowest-start].widget.options[zero]` | wrong option: `low = 0` / No price is below 0, so `low` would stay 0, a price that never happen… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-lowest-start].widget.options[big]` | wrong option: `low = 1000000` / That only works while every price is below a million. Start from a re… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-lowest-start].widget.options[len]` | wrong option: `low = len(prices)` / That is a count, not a price. It could be below every price and never… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[1].explain, screens[8].prose` | indexes 0 to n - 1; -1 is the last; len counts | correct | Python tutorial 3.1.3; run |
| `screens[2].prose, explain` | append adds at the end; assigning to an index replaces; a float prints with the digits it needs, keeping one after the point | correct | Python tutorial 3.1.3, 5.1; run [100.0, 101.25] |
| `screens[2], screens[8]` | lists change in place (append, index assignment) with no word that b = a shares the list | imprecise | Finding 3 (the same defect as l2): the place where the copy picture of l2 stops being true |
| `screens[5].explain, summary.trap` | starting a maximum at 0 invents a value; start from x[0] | correct | run: 0 against -45.5 |
| `screens[6].prose` | values[0] on an empty list stops with an IndexError | correct | run |
| `screens[7].prose, summary.ideas[2]` | break ends a loop at once | correct | Python tutorial 4.4; Language reference 7.9 (the innermost loop; only one loop is in play) |
| `screens[8].prose, summary.formula` | peak_t = max(peak_{t-1}, p_t), peak_0 = p_0; the gap peak - p is the drawdown | correct | definition; the fraction-of-peak form is promised and given in l10; £3.20 recomputed |

## review-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.options[right]` | key: `at target` | correct | run, concepts A: this is what Python does |
| `items[0].widget.options[gt]` | wrong option: `take profit` / You read `>` as 'at or above'. 110.00 is not greater than itself, so … | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[0].widget.options[hold]` | wrong option: `hold` / You skipped the `elif`. `price == target` is `True`, so its branch ru… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[0].widget.options[two]` | wrong option: `at target`, then `hold` / You ran `else` as well. Only one branch of the chain ever runs. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[1].widget.answer` | key: 5 | correct | run, concepts A |
| `items[1].feedback.byKey.stopped-81` | slip 4: You stopped at 81. `81 < 100` is still `True`, so one more pass runs. | correct | recomputed from the mistake its line names (concepts B) |
| `items[1].feedback.byKey.n` | slip 243: That is the final `n`. The program prints `count`, the number of passes. | correct | recomputed from the mistake its line names (concepts B) |
| `items[2].widget.answer` | key: 16 | correct | run, concepts A |
| `items[2].feedback.byKey.with-four` | slip 25: You included 4. `range(4)` stops before 4. | correct | recomputed from the mistake its line names (concepts B) |
| `items[2].feedback.byKey.from-one` | slip 24: You started at 1. `range(4)` starts at 0. | correct | recomputed from the mistake its line names (concepts B) |
| `items[3].widget.options[right]` | key: `-8.25` | correct | run, concepts A: this is what Python does |
| `items[3].widget.options[error]` | wrong option: An `IndexError` / `len(pnls) - 1` is 3, a valid index. `pnls[len(pnls)]` would be the o… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[3].widget.options[third]` | wrong option: `22.0` / You counted from 1, taking index 3 as the third value. Index 3 is the… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[3].widget.options[len]` | wrong option: `4` / That is `len(pnls)`. The brackets pick the value at index 3. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[4].widget.options[lt]` | wrong option: `n = 10` with `while n < 50:` / `50 < 50` is `False`, so 50 never prints. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[4].widget.options[right]` | key: `n = 10` with `while n <= 50:` | correct | run or recomputation, concepts A2: this is what Python does |
| `items[4].widget.options[zero]` | wrong option: `n = 0` with `while n <= 50:` / Starting at 0 prints 0 first: six numbers. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[4].widget.options[ne]` | wrong option: `n = 10` with `while n != 55:` / `n` steps 10, 20, 30 and never equals 55, so this loop never ends. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[5].widget.options[right]` | key: Move `total = 0` above the `for` line. | correct | run, concepts A: this is what Python does |
| `items[5].widget.options[indent-print]` | wrong option: Indent `print(total)` into the loop. / That prints after every pass, and each value is still just that pass'… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[5].widget.options[delete]` | wrong option: Delete `total = 0`. / Then the first `total + p` fails: `total` does not exist yet. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[5].widget.options[range]` | wrong option: Loop over `range(4)` instead. / The loop already visits every P&L. The problem is the reset on each p… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[6].widget.solution` | solution and 5 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[6].feedback.byKey.error` | error line: Your code stopped with an error. An `IndexError` means `pnls[0]` ran on the empty list. | imprecise | Finding 2: the IndexError on the empty list keys as test-2, not error; sweep |
| `items[7].widget.answer` | key: 3 | correct | run, concepts A |
| `items[7].feedback.byKey.fifteen` | slip 4: You counted 15.00. It passes `p > 0` but fails `p > 50`, and the `elif` is not asked because the ou… | correct | recomputed from the mistake its line names (concepts B) |
| `items[7].feedback.byKey.minus-forty` | slip 2: You missed one. −210.00 fails `p > 0`, so the `elif` asks `p < -100`, which is `True`. | correct | recomputed from the mistake its line names (concepts B) |

## homework-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[0].feedback.byKey.error` | error line: Your code stopped with an error. Check the colons and that every branch sets `action`. | imprecise | Finding 2: a branch that leaves action unset keys as test-3 (UnboundLocalError in the call); only the missing colon keys as error; sweep |
| `items[1].widget.answer` | key: 5 | correct | run, concepts A |
| `items[1].feedback.byKey.four` | slip 4: After 4 years the balance is £1,082.43, still short, so the loop runs again. | correct | recomputed from the mistake its line names (concepts B) |
| `items[2].widget.solution` | solution and 7 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[2].feedback.byKey.error` | error line: Your code stopped with an error or ran too long. A rate of 0 never grows the balance: guard the loop wit… | imprecise | Finding 2: the unguarded loop keys as test-2 ("Stopped after 5 s"), not error; sweep |
| `items[3].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[3].feedback.byKey.test-4` | test-4 line: Day 2's own loss is −150.00, but the running total is only −50.00, so there is no breach. Compare the to… | correct | sweep under the page harness: compares the day gives test-4 |
| `items[4].widget.solution` | solution and 6 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[4].feedback.byKey.test-3` | test-3 line: For 100, 90, 95, 80, 120, 110 the answer is 20: the fall from 100 to 80. The later fall from 120 to 110 … | correct | sweep under the page harness: keeps the last gap gives test-3; fall from the final peak only gives test-3 |
| `items[5].widget.answer` | key: 3 | correct | run, concepts A |
| `items[5].feedback.byKey.flat-up` | slip 5: You counted 0.0 as an up day. `0.0 > 0` is `False`, so `run` resets there. | correct | recomputed from the mistake its line names (concepts B) |
| `items[5].feedback.byKey.all-ups` | slip 6: You counted every up day. `run` resets on each day that is not up; `best` keeps the longest run. | correct | recomputed from the mistake its line names (concepts B) |
| `items[5].feedback.byKey.last-run` | slip 1: That is `run` at the end. The program prints `best`, the longest run seen. | correct | recomputed from the mistake its line names (concepts B) |
| `items[6].widget.options[right]` | key: `no order` | correct | run, concepts A: this is what Python does |
| `items[6].widget.options[send]` | wrong option: `send order` / You treated `"buy"` and `"BUY"` as equal. `==` compares text letter b… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[6].widget.options[error]` | wrong option: A `SyntaxError` / `==` is the right way to compare. Every line here is valid. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[6].widget.options[both]` | wrong option: `send order`, then `no order` / Only one branch runs, and here the test is `False`. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[7].widget.options[right]` | key: `for i in range(len(prices)):` | correct | run or recomputation, concepts A2: this is what Python does |
| `items[7].widget.options[skip]` | wrong option: `for i in range(1, len(prices)):` / That starts at 1, so the first price, at index 0, is skipped. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[7].widget.options[over]` | wrong option: `for i in range(len(prices) + 1):` / The last `i` is `len(prices)`, one past the end, so `prices[i]` stops… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[7].widget.options[shifted]` | wrong option: `for i in range(1, len(prices) + 1):` / That counts 1 to `len(prices)`: it skips index 0 and runs one past th… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[8].model` | model answer and rubric: **(a)** It prints `64.75 120.5 3`. The loop starts at `i = 1`, so it sees 120.5… | correct | every printed output and error in the model run (concepts A, the model blocks) |
| `items[9].widget.solution` | solution and 8 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[9].feedback.byKey.test-1` | test-1 line: Test 1 splits £60.00 between 3 people, so each pays £20.00 with no charge. If the row shows TypeError, a… | correct | sweep under the page harness: no float gives test-1; prints gives test-1; missed a price gives test-1; always charges gives test-1 |
| `items[9].feedback.byKey.test-2` | test-2 line: Test 2's prices have pence, and each of 2 people pays £11.85. `int()` cannot read `"12.50"`, so convert … | correct | sweep under the page harness: int gives test-2; // gives test-2 |
| `items[9].feedback.byKey.test-3` | test-3 line: Test 3 is a group of exactly 6, so the charge applies and each pays £18.00. Check your comparison: 6 or … | correct | sweep under the page harness: > 6 gives test-3 |
| `items[9].feedback.byKey.test-4` | test-4 line: Test 4 has 8 people but only 5 dishes. The charge depends on how many people there are, not how many pri… | correct | sweep under the page harness: charge by dishes gives test-4 |
| `items[9].feedback.byKey.error` | error line: Your code stopped before any test ran. Read the last line of the error below the editor, then the line i… | correct | describes its test; true (test read, values in concepts E) |
| `items[2].prose` | a rate of 0 or below never reaches a target above the balance | correct | for a positive balance and rate in (-1, 0]; the tests use 0 and -0.10 |
| `items[6].explain` | == compares text letter by letter, capitals included | correct | Language reference 6.10.1; run |
| `items[4].prose` | largest fall: biggest drop from the highest price so far to any later price | correct | absolute drawdown; 3.20, 20, 35 recomputed by grade-all and concepts |

## l9-packaging-steps

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.options[nine]` | key: `9` | correct | run, concepts A: this is what Python does |
| `screens[0].widget.options[ten]` | wrong option: `10` / You added 1 to the 4 before doubling. Python finishes the call `doubl… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[0].widget.options[eight]` | wrong option: `8` / You stopped at the function's answer. The `+ 1` still applies to the … | correct | recomputed from the mistake its why names (concepts B) |
| `screens[0].widget.options[error]` | wrong option: An error: `x` was never given a value / You read `x` as an ordinary variable. It is filled in by the call: `d… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.answer` | place key: {'main': ['fee'], 'call': ['px', 'cost']} | correct | run or recomputation, concepts A2 |
| `screens[1].feedback.byKey.fee` | wrong pick line: `def fee(...)` is a line of the main program. It makes the name `fee` there, before any call happen… | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.px` | wrong pick line: `px` is the name in the brackets of `def fee(px)`. The call creates it, holding 250.00. (`px` is a … | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.cost` | wrong pick line: `cost = ...` is indented under `def`, so it only runs inside the call. | correct | true of the pick it names (trace of the snippet) |
| `screens[2].widget.options[right]` | key: `2.5` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[2].widget.options[arg]` | wrong option: `250.0` / You printed the value that went in. The call hands back `cost`, which… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[2].widget.options[name]` | wrong option: `cost` / You printed the name. `print` shows the value the call hands back, no… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[2].widget.options[pennies]` | wrong option: `2.50` / You wrote it as money. Python prints a float with only the digits it … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[3].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[3].feedback.byKey.test-1` | test-1 line: Test 1 calls `with_fee(100.00)` and expects 101.5. If it got `None`, your function printed the answer in… | correct | sweep under the page harness: prints gives test-1 |
| `screens[4].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[4].feedback.byKey.test-1` | test-1 line: Test 1 buys 10 shares at £12.50 and expects 126.5. A result of 140.0 means the fee was added to every sh… | correct | sweep under the page harness: fee per share gives test-1; no fee gives test-1 |
| `screens[5].widget.options[right]` | key: `-5.0` | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[by-size]` | wrong option: `5.0` / You matched the prices by meaning, so the bigger one went first. Pyth… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[5].widget.options[int]` | wrong option: `-5` / You dropped the decimal point. Both prices are floats, so `new - old`… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[error]` | wrong option: An error, because the prices are in the wrong order / Python never checks what the names mean. It fills `old`, then `new`, … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.answer` | place key: {'main': ['fee', 'net', 'cash'], 'gone': ['px', 'left']} | correct | run or recomputation, concepts A2 |
| `screens[6].feedback.byKey.left` | wrong pick line: `left` was made inside `net`. When the call returned, its frame was cleared and `left` went with it. | correct | true of the pick it names (trace of the snippet) |
| `screens[6].feedback.byKey.px` | wrong pick line: `px` is a parameter, so it lived in the frame. It was cleared when the call returned. | correct | true of the pick it names (trace of the snippet) |
| `screens[6].feedback.byKey.fee` | wrong pick line: `fee = 1.50` is a main-program line, so `fee` is still there. The function could read it too. | correct | true of the pick it names (trace of the snippet) |
| `screens[6].feedback.byKey.net` | wrong pick line: `def net` is a main-program line. It made the name `net`, which stays. | correct | true of the pick it names (trace of the snippet) |
| `screens[6].feedback.byKey.cash` | wrong pick line: `cash = net(100.00)` runs in the main program. It holds the 98.5 the call handed back. | correct | true of the pick it names (trace of the snippet) |
| `screens[7].widget.options[both]` | wrong option: It prints `3.0`, then `30.0` / You assumed `print` hands the value back. It only shows it on screen,… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.options[right]` | key: It prints `3.0`, then stops with a `TypeError` | correct | run, concepts A: this is what Python does |
| `screens[7].widget.options[none]` | wrong option: It prints `3.0`, then `None` / `print(g)` would show `None`. But `g * 10` is worked out first, and `… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[7].widget.options[only]` | wrong option: It prints `30.0` / The call runs its own `print` first, so `3.0` appears before anything… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[8].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[8].feedback.byKey.test-1` | test-1 line: Test 1 expects 3.0 back. If it got `None`, the body still prints instead of returning. If it got −3.0, t… | correct | sweep under the page harness: still prints gives test-1; wrong way round gives test-1 |
| `screens[9].widget.options[none]` | key: `None` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[9].widget.options[printed]` | wrong option: The last value it printed / You treated printing as handing back. `print` only shows a value on s… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.options[last]` | wrong option: The value of its last line / Some languages work that way, but Python does not. Without `return`, … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.options[zero]` | wrong option: `0` / Python uses a special value for nothing, `None`, not the number 0. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[10].widget.solution` | solution and 5 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[10].feedback.byKey.test-1` | test-1 line: Test 1 expects −0.02. About −0.0204 means you divided by the new price; 244.0 means the brackets are mis… | correct | sweep under the page harness: divide by new gives test-1; no brackets gives test-1; times 100 gives test-1 |
| `quiz[q-before-def].widget.options[right]` | key: It stops with a `NameError` | correct | run, concepts A: this is what Python does |
| `quiz[q-before-def].widget.options[value]` | wrong option: It prints `11.5` / You read the whole file first, as a person would. Python runs top to … | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-before-def].widget.options[none]` | wrong option: It prints `None` / `None` comes from a function with no `return`. Here the function does… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-before-def].widget.options[type]` | wrong option: It stops with a `TypeError` / A `TypeError` needs a value of the wrong kind. At line 1 there is no … | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-print-none].widget.options[right]` | key: `10.0`, then `None` | correct | run, concepts A: this is what Python does |
| `quiz[q-print-none].widget.options[twice]` | wrong option: `10.0` twice / You treated `print` as handing the value back. `t` holds what `tax` r… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-print-none].widget.options[just-none]` | wrong option: Only `None` / The call still runs its own `print`, so 10.0 appears first. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-print-none].widget.options[just-ten]` | wrong option: Only `10.0` / `print(t)` always shows something. Here `t` is `None`, so it shows `N… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-local-copy].widget.options[right]` | key: `500.0` | correct | run, concepts A: this is what Python does |
| `quiz[q-local-copy].widget.options[changed]` | wrong option: `550.0` / You expected the function to change `savings`. It changed its own `ba… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-local-copy].widget.options[error]` | wrong option: `NameError` / `savings` is a main-program name, so it exists on the last line. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-local-copy].widget.options[none]` | wrong option: `None` / `savings` was set to 500.00 and nothing changed it. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-cost].widget.answer` | key: 121.5 | correct | run, concepts A |
| `quiz[q-cost].feedback.byKey.fee-each` | slip 195: You added the fee to the price before multiplying. Python multiplies first, so the fee is added onc… | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-cost].feedback.byKey.no-fee` | slip 120: You left out the third argument. `fee` is 1.50 and it is added at the end. | correct | recomputed from the mistake its line names (concepts B) |
| `screens[0].prose, summary.ideas[0]` | def builds a function; a call fills parameters in order and runs the body in a fresh frame | correct | Python tutorial 4.8; Language reference 4.2, 8.7 |
| `screens[2].prose` | frame, parameter, return sends one value back to where the call was written | correct | Python tutorial 4.8 |
| `screens[2].options[pennies].why, explain` | Python prints a float with only the digits it needs: 2.5, not 2.50 | correct | run: 250.0 * 0.01 prints 2.5 |
| `screens[5].options` | Python matches arguments by position, never by what the names mean | correct | Python tutorial 4.8; run -5.0 |
| `screens[6].prose, summary.ideas[2]` | when a call returns its frame is cleared; names made inside vanish; a function can read a main-program name | correct | Language reference 4.2.2; run: NameError for left |
| `screens[7].hints[1], screens[9], summary.ideas[1]` | a function with no return hands back None | correct | Python tutorial 4.8 ("functions without a return statement do return a value ... None"); run |
| `summary.ideas[2], quiz[q-before-def]` | define a function before the line that calls it; Python runs top to bottom | correct | run: NameError |
| `screens[10].prose, summary.formula` | daily return r = (p1 - p0) / p0 | correct | simple return, convention stated in the item |

## l10-reading-errors

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.answer` | tap-regions key: ['c2'] | correct | run or recomputation, concepts A2 |
| `screens[0].feedback.byKey.c1` | wrong pick line: You counted from 1, so index 2 looked like the second value. Python counts from 0: index 2 is the t… | correct | true of the pick it names (trace of the snippet) |
| `screens[0].feedback.byKey.c0` | wrong pick line: That is index 0, the first value. Count on two more places. | correct | true of the pick it names (trace of the snippet) |
| `screens[0].feedback.byKey.c3` | wrong pick line: That is index 3, the last value. Index 2 is one place to its left. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].widget.answer` | tap-regions key: ['c1', 'c2'] | correct | run or recomputation, concepts A2 |
| `screens[1].feedback.byKey.inclusive` | wrong pick line: You included index 3. A slice stops just before its end index, so `[1:3]` takes indexes 1 and 2. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.from-one` | wrong pick line: You started at the first value. A slice starts at its start index, 1, which is the second value. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.c0` | wrong pick line: Index 0 comes before the slice's start, 1. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.c3` | wrong pick line: Index 3 is the end index, and a slice stops just before it. | correct | true of the pick it names (trace of the snippet) |
| `screens[2].widget.options[right]` | key: Line 2 asked for index 4, past the end of the list | correct | run, concepts A: this is what Python does |
| `screens[2].widget.options[line1]` | wrong option: Line 1 built the list wrongly / The traceback names line 2. Line 1 ran without any complaint. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[print]` | wrong option: `print` cannot show a price / The last line names an `IndexError`. The problem is the index, not `p… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[2].widget.options[empty]` | wrong option: The list is empty / The list holds 4 values. Index 4 would be a fifth one. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.options[right]` | key: Move the `def` block above the `print` line | correct | run, concepts A: this is what Python does |
| `screens[3].widget.options[return]` | wrong option: Add a `return` line to `average` / `average` already returns. The error says the name `average` does not… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.options[rename]` | wrong option: Rename the function to `Average` / The spelling already matches. The problem is order: line 1 runs befor… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[3].widget.options[list]` | wrong option: Store the list in a variable first / The list is fine. `NameError` is about the name `average`, which line… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[4].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[4].feedback.byKey.error` | error line: Your script still stops before the tests run. The `None` comes from line 2: `append` hands back `None`, … | correct | sweep under the page harness: starter gives error |
| `screens[4].feedback.byKey.test-2` | test-2 line: `count` should be the number of prices in `closes`, which is 3. | correct | sweep under the page harness: count is last index gives test-2; count before append gives test-2 |
| `screens[5].widget.options[top]` | wrong option: Line 5, the `print` line / You read the first File line. Calls are listed oldest first, so the F… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[right]` | key: Line 2, inside `daily_return` | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[def]` | wrong option: Line 1, `def daily_return` / Line 1 only defines the function. The division happens on line 2 when… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[data]` | wrong option: Line 4, where `closes` is made / Line 4 is not in the traceback. It is where the 0.00 came from, which… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[6].feedback.byKey.error` | error line: Your script still stops on its last line before the tests run. A `TypeError` means the price is still te… | correct | sweep under the page harness: starter (not converted) gives error; int gives error; SyntaxError gives error |
| `screens[6].feedback.byKey.test-1` | test-1 line: Test 1 passes the text `"101.20"` and expects 102.7. Convert with `float` before adding 1.50. | imprecise | Finding 4: not converting keys as error (starter, int) in two of three natural codings; the line shows for a forgotten fee |
| `screens[7].widget.options[value]` | key: `ValueError` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[7].widget.options[type]` | wrong option: `TypeError` / `TypeError` is for the wrong kind of value, such as text plus a numbe… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[7].widget.options[index]` | wrong option: `IndexError` / No list position is involved. `float` was handed text it cannot read … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[7].widget.options[name]` | wrong option: `NameError` / `float` exists. The problem is the text it was given. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.solution` | solution and 5 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[8].feedback.byKey.error` | error line: The script still stops before the tests run, on the `print` line. The loop runs one step past the end: `… | correct | sweep under the page harness: starter gives error |
| `screens[8].feedback.byKey.test-1` | test-1 line: Test 1 expects 0.2, the £22.00 fall measured against the £110.00 peak. | correct | describes its test; true (test read, values in concepts E) |
| `screens[8].feedback.byKey.test-5` | test-5 line: Test 5 ends on its lowest price, £30.00. A loop that stops one step early never sees it. | correct | sweep under the page harness: one step early gives test-5; range(len - 1) gives test-5 |
| `quiz[q-slice].widget.options[right]` | key: `[102.5, 99.8, 100.4]` | correct | run, concepts A: this is what Python does |
| `quiz[q-slice].widget.options[all]` | wrong option: `[101.2, 102.5, 99.8, 100.4]` / You started the slice at the first value. Index 1 is the second value. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-slice].widget.options[one]` | wrong option: `102.5` / That is `closes[1]`. The colon makes a slice: everything from index 1… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-slice].widget.options[drop-last]` | wrong option: `[102.5, 99.8]` / With no end index, a slice runs to the end of the list. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-read-value].widget.options[right]` | key: Line 7 met the text `n/a` where it expected a price | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-read-value].widget.options[append]` | wrong option: `append` cannot add a float to a list / The error is a `ValueError` from `float`, which runs before `append`. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-read-value].widget.options[index]` | wrong option: `parts[1]` does not exist / That would be an `IndexError`. Here `parts[1]` exists and holds `n/a`. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-read-value].widget.options[line1]` | wrong option: The file could not be opened / The traceback names line 7 and a conversion. Opening the file worked. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-last-index].widget.answer` | key: 3 | correct | run, concepts A |
| `quiz[q-last-index].feedback.byKey.count` | slip 4: 4 is `len(closes)`. The line subtracts 1, which gives the last index. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-last-index].feedback.byKey.no-append` | slip 1: Both `append` lines add a value, so the list has 4 by the end. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-two-frames].widget.options[right]` | key: Line 3, in `average` | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-two-frames].widget.options[top]` | wrong option: Line 12, the call to `report` / You read the top File line. The calls are listed oldest first; Python… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-two-frames].widget.options[middle]` | wrong option: Line 8, in `report` / Line 8 made the call that failed. Python was inside `average`, on lin… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[1].explain` | a slice of a list works as on text; prices[1:] is everything after the first | correct | Python tutorial 3.1.3; run |
| `screens[2], screens[5], summary` | last line names the error; the File line nearest the bottom is where Python stopped; calls listed oldest first | correct | Python tutorial 8.2; Library reference traceback ("most recent call last"); all eight tracebacks of the lesson reproduced exactly on 3.12.7 (concepts D) |
| `screens[4].hints[1], explain` | append changes the list in place and hands back None | correct | Python tutorial 5.1 footnote; run |
| `screens[6].explain` | float ignores spaces and newlines around the digits | correct | Library reference float(): leading and trailing whitespace allowed; run |
| `screens[8].prose` | maximum drawdown: worst fall from a running peak, as a fraction of that peak | correct | standard definition (Bacon, Practical Portfolio Performance Measurement, drawdown); 22/110 = 0.2 recomputed |
| `summary.ideas[2]` | a slice [a:b] holds b - a values | imprecise | Finding 13: only inside the list; the quiz of the same lesson uses closes[5:] on a short list, which is empty |
| `summary.formula` | last index = len(xs) - 1; range(1, len(xs)) never runs off the end | correct | run |

## l11-numbers-from-a-file

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.options[sum]` | wrong option: It prints `303.5` / You read each line as a number. Python reads every line of a file as … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[0].widget.options[right]` | key: It stops with a `TypeError` on the first line | correct | run, concepts A: this is what Python does |
| `screens[0].widget.options[joined]` | wrong option: It prints `101.20102.5099.80` / Joining would happen if `total` started as text. It starts as the num… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[1].widget.answer` | tap-regions key: ['r0c1', 'r3c1'] | correct | run or recomputation, concepts A2 |
| `screens[1].feedback.byKey.missed-gap` | wrong pick line: You found the header. Look again at Wednesday: its price is `n/a`, a missing value. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.missed-header` | wrong pick line: Python reads the header line too. Its second piece is `Close`, which is not a number. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.r1c1` | wrong pick line: Monday's second piece is `101.20`, which `float` reads. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.r2c1` | wrong pick line: Tuesday's second piece is `102.50`, which `float` reads. | correct | true of the pick it names (trace of the snippet) |
| `screens[1].feedback.byKey.r4c1` | wrong pick line: Thursday's second piece is `100.40`, which `float` reads. | correct | true of the pick it names (trace of the snippet) |
| `screens[2].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[2].feedback.byKey.error` | error line: Your script stops on its last line before the tests run. An error about `'Tue'` means you took index 0: … | correct | sweep under the page harness: index 0 gives error |
| `screens[2].feedback.byKey.test-1` | test-1 line: Test 1 expects the number 102.5. Text such as `'102.50\n'` means `float` is missing. | correct | sweep under the page harness: no float gives test-1 |
| `screens[3].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[3].feedback.byKey.test-1` | test-1 line: Test 1 expects `[101.2, 102.5, 99.8]`. Items like `'101.20\n'` mean the `float` is missing; a single num… | correct | sweep under the page harness: no float gives test-1; replaced gives test-1 |
| `screens[4].widget.options[right]` | key: Each line keeps its own newline, and `print` adds another | correct | run, concepts A: this is what Python does |
| `screens[4].widget.options[file]` | wrong option: The file has empty lines between the prices / The table shows none. Each line has one newline at its end, and that … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[4].widget.options[print]` | wrong option: `print` always leaves an empty line after its text / Normally `print` ends with one newline, so lines sit together. Here t… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[4].widget.options[loop]` | wrong option: The loop runs twice for every line / The loop visits each line once. Count the prices printed: three, not … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[works]` | wrong option: It prints `[101.2, 102.5, 99.8, 100.4, 101.1]` / You expected Python to skip the header. It reads every line, and the … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[right]` | key: It stops on the first line with a `ValueError` | correct | run, concepts A: this is what Python does |
| `screens[5].widget.options[days]` | wrong option: It stops because `parts[1]` is the day / Index 1 is the second piece, the price. The day is index 0. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.options[index]` | wrong option: It stops with an `IndexError` / Every line has a comma, so `parts[1]` exists. The trouble is what it … | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[6].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[6].feedback.byKey.error` | error line: Your script stops before the tests run. `ValueError` about `'Close\n'` means the header line is still be… | correct | sweep under the page harness: header kept gives error |
| `screens[6].feedback.byKey.test-1` | test-1 line: Test 1 expects all five closes. Four closes means the slice skipped one line too many. | correct | sweep under the page harness: lines[2:] gives test-1 |
| `screens[7].widget.options[right]` | key: `'Wed'` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[7].widget.options[price]` | wrong option: `'99.80\n'` / That is index 1. Index 0 is the first piece, before the comma. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[7].widget.options[number]` | wrong option: `99.8` / `split` gives text pieces and never converts them. You would need `fl… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[7].widget.options[letter]` | wrong option: `'W'` / Index 0 of the line itself is `'W'`. After `split`, index 0 is a whol… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[8].feedback.byKey.test-1` | test-1 line: Test 1 expects 101.1, Friday's close. `IndexError` means the index ran past the end; 101.2 means you too… | correct | sweep under the page harness: first data line gives test-1; index past end, no print yet gives test-1; split on newline, last piece empty gives test-1 |
| `screens[8].feedback.byKey.test-4` | test-4 line: Your function works, but the script should print exactly one line, `Last close: £101.10`. Use `:.2f` so … | correct | sweep under the page harness: no .2f gives test-4; no print gives test-4 |
| `quiz[q-split].widget.options[right]` | key: `['Thu', '100.40\n']` | correct | run, concepts A: this is what Python does |
| `quiz[q-split].widget.options[number]` | wrong option: `['Thu', 100.4]` / `split` only cuts text. The pieces stay text until you call `float`. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-split].widget.options[joined]` | wrong option: `Thu 100.40` / `split` returns a list, so `print` shows brackets and quotes. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-split].widget.options[no-newline]` | wrong option: `['Thu', '100.40']` / The newline belongs to the last piece. Only `strip` would remove it. | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-blank-line].widget.options[right]` | key: It stops with a `ValueError` on line 3 of the file | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-blank-line].widget.options[skips]` | wrong option: `closes` ends as `[101.2, 102.5]`; empty lines are skipped / Python skips nothing. The empty line arrives as `"\n"`, and `float` c… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-blank-line].widget.options[zero]` | wrong option: `closes` ends as `[101.2, 102.5, 0.0]` / `float` never turns empty text into 0.0. It raises an error instead. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-count-rows].widget.answer` | key: 20 | correct | run or recomputation, concepts A2 |
| `quiz[q-count-rows].feedback.byKey.with-header` | slip 21: 21 is `len(lines)`. The slice `[1:]` leaves out the header. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-count-rows].feedback.byKey.two-off` | slip 19: The slice drops only index 0, the header. All 20 days remain. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-strip].widget.options[right]` | key: `101.200` | correct | run, concepts A: this is what Python does |
| `quiz[q-strip].widget.options[sum]` | wrong option: `101.2` / You treated the text as a number. `+` on two pieces of text joins the… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-strip].widget.options[spaces]` | wrong option: ` 101.200` / `strip` removes spaces from both ends, not just the newline. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[0], summary.ideas[0]` | a file gives text, one line at a time, each ending in a newline | imprecise | Finding 11: the last line need not end in one (the lesson's own test 2 on screen 2 has none) |
| `screens[1].prose, screens[7].prose` | split(",") cuts the text at each comma into a list of text pieces | correct | Library reference str.split; run |
| `screens[3].solution, screens[6].solution` | for line in open(name) / open(name).readlines(), never closed | misleading | Finding 12: Python tutorial 7.2 recommends with for every file; the course uses with for writing only and never says the reading form leaves the file open |
| `screens[4].explain` | print adds a newline; strip() removes spaces and newlines from both ends | correct | Library reference print, str.strip; run |
| `screens[6].prose, summary.ideas[2]` | readlines() gives every line as a list; lines[1:] leaves out the header; lines[-1] is the last | correct | Python tutorial 7.2.1; run |
| `summary.trap` | Python does not skip a header for you | correct | run: ValueError on Close |

## l12-savings-script

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.options[right]` | key: `2249.73` | correct | run, concepts A: this is what Python does |
| `screens[0].widget.options[simple]` | wrong option: `2240.0` / You added 4% of the first £2,000.00 each year. The loop multiplies th… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[0].widget.options[once]` | wrong option: `2080.0` / That is one year. `range(3)` runs the loop three times: years 0, 1 an… | correct | recomputed from the mistake its why names (concepts B) |
| `screens[0].widget.options[four]` | wrong option: `2339.72` / That is four years. `range(3)` gives 0, 1, 2: three passes, not four. | correct | recomputed from the mistake its why names (concepts B) |
| `screens[1].widget.options[right]` | key: Each year's step is bigger than the one before | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[1].widget.options[equal]` | wrong option: Every step is the same size / Equal steps would be simple interest, £50.00 a year at 5%. Here each … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[1].widget.options[double]` | wrong option: Doubling the rate doubles the final gain / Try 5% then 10%. The ten-year gain goes from £628.89 to £1,593.74, mu… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[2].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[2].feedback.byKey.test-1` | test-1 line: Test 1 expects about 2249.73. 2240.0 is simple interest; 2339.72 is one year too many; a tiny number mea… | correct | sweep under the page harness: simple interest gives test-1; one year too many gives test-1; times rate gives test-1 |
| `screens[3].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[3].feedback.byKey.test-1` | test-1 line: Test 1 expects 1307.5. 1317.75 means the deposit went in before the interest; 1302.5 means all deposits … | correct | sweep under the page harness: deposit first gives test-1; deposits at end gives test-1 |
| `screens[4].widget.options[right]` | key: `Year 10: £1628.89` | correct | run, concepts A: this is what Python does |
| `screens[4].widget.options[long]` | wrong option: `Year 10: £1628.894626777442` / You left out the `:.2f`. It keeps exactly two decimal places. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[4].widget.options[up]` | wrong option: `Year 10: £1628.90` / You rounded up. `.2f` rounds to the nearest penny, and .894 is nearer… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[4].widget.options[braces]` | wrong option: `Year {year}: £{balance:.2f}` / The `f` before the opening quote tells Python to fill in the braces. | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[5].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[5].widget.tests` | the hidden tests reject the obvious wrong programs | imprecise | Finding 6: an append-mode save_line passes every test (files are emptied first); sweep (pass) |
| `screens[5].feedback.byKey.test-1` | test-1 line: Test 1 expects `'Year 10: £1628.89\n'`. A missing `\n` at the end, or many decimal places, are the usual… | correct | sweep under the page harness: no newline gives test-1; no .2f gives test-1 |
| `screens[6].widget.options[three]` | wrong option: Three lines: `Year 1`, `Year 2`, `Year 3` / You expected each write to add a line. Opening with `"w"` empties the… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[6].widget.options[right]` | key: One line: `Year 3` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[6].widget.options[first]` | wrong option: One line: `Year 1` / Each later pass empties the file again, so the last write survives, n… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[6].widget.options[empty]` | wrong option: Nothing: the file is empty / The last pass opens the file and then writes `Year 3`, so that line s… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[7].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[7].widget.tests` | the hidden tests reject the obvious wrong programs | imprecise | Finding 6: opening with "a" inside the loop, the trap of screen 6 in append form, passes every test; sweep (pass) |
| `screens[7].feedback.byKey.test-1` | test-1 line: Test 1 expects three lines ending `Year 3: £2249.73`. One line means the file is opened inside the loop;… | correct | sweep under the page harness: open inside loop gives test-1; range stops early gives test-1; write before growing gives test-1 |
| `screens[8].widget.options[right]` | key: `python3 savings.py` | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[8].widget.options[prompt]` | wrong option: `python3`, then type `savings.py` at the `>>>` prompt / At the `>>>` prompt Python expects code, not a file name. It reports … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[cd]` | wrong option: `cd savings.py` / `cd` moves into a folder. `savings.py` is a file for Python to run. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[8].widget.options[cat]` | wrong option: `cat savings.py` / `cat` shows the text of the file. Nothing runs. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.options[right]` | key: $1000 \times 1.1^2 = 1210$ | correct | run or recomputation, concepts A2: this is what Python does |
| `screens[9].widget.options[simple]` | wrong option: $1000 \times (1 + 2 \times 0.1) = 1200$ / That adds 10% of the first £1,000.00 twice. The second year's 10% is … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.options[rate]` | wrong option: $1000 \times 0.1^2 = 10$ / You multiplied by the rate, not by $1 + r$. Each year keeps the balan… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[9].widget.options[extra]` | wrong option: $1000 \times 1.1^3 = 1331$ / That is three years. `range(2)` makes two passes. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `screens[10].widget.solution` | solution and 7 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `screens[10].feedback.byKey.error` | error line: Your script stops before the tests run. Read the traceback from the bottom: a `ValueError` about `Close`… | imprecise | Finding 2: the ValueError keys as test-1 here; sweep |
| `screens[10].feedback.byKey.test-1` | test-1 line: Test 1 expects 4 returns from 5 closes. Five means the loop started at index 0, pairing the last close w… | correct | sweep under the page harness: loop from 0 gives test-1 |
| `screens[10].feedback.byKey.test-2` | test-2 line: Test 2 expects Tuesday's return, about +0.0128. A small negative number means the two closes are passed … | correct | sweep under the page harness: swapped gives test-2 |
| `screens[10].feedback.byKey.test-7` | test-7 line: Your returns are right, but the script should print exactly four lines: `1.28%`, `-2.63%`, `0.60%` and `… | correct | sweep under the page harness: plain print gives test-7 |
| `quiz[q-range-count].widget.answer` | key: 4 | correct | run, concepts A |
| `quiz[q-range-count].feedback.byKey.five` | slip 5: `range(1, 5)` stops before 5, so there is no Year 5. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-range-count].feedback.byKey.three` | slip 3: The range starts at 1 and includes it: 1, 2, 3, 4. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-append-mode].widget.options[right]` | key: Two lines: `Mon 101.20`, then `Tue 102.50` | correct | run or recomputation, concepts A2: this is what Python does |
| `quiz[q-append-mode].widget.options[wiped]` | wrong option: One line: `Tue 102.50` / That is what `"w"` would do. `"a"` opens for appending and keeps what… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-append-mode].widget.options[first]` | wrong option: Two lines, with `Tue 102.50` first / Appending adds to the end of the file, after what is already there. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `quiz[q-ten-percent].widget.answer` | key: 605 | correct | run, concepts A |
| `quiz[q-ten-percent].feedback.byKey.simple` | slip 600: You added 10% of £500.00 twice. The second year's interest is 10% of £550.00. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-ten-percent].feedback.byKey.once` | slip 550: That is one year. `range(2)` runs the loop twice. | correct | recomputed from the mistake its line names (concepts B) |
| `quiz[q-silent].widget.options[right]` | key: The script defines `project` but never calls it or prints anything | correct | run, concepts A: this is what Python does |
| `quiz[q-silent].widget.options[terminal]` | wrong option: Scripts run from the terminal cannot print / They can: `print` writes to the terminal. This script simply has no `… | correct | run, concepts A: not what Python does; its why line read against the run |
| `quiz[q-silent].widget.options[return]` | wrong option: `return` should be `print` / Swapping it would still print nothing, because nothing calls `project… | correct | run, concepts A: not what Python does; its why line read against the run |
| `screens[0].prose` | round(x, 2) rounds x to two decimal places | correct | Library reference round(): to the nearest, ties to even on the binary value; no item here sits on a tie (2249.728, 1628.8946, 31.836, 605.0000000000001) |
| `screens[0].explain` | compound interest: each year's rate applied to a bigger balance | correct | definition; 2080.00, 2163.20, 2249.728 recomputed |
| `screens[4].prose, options[up].why` | :.2f rounds to two decimal places, to the nearest penny | correct | Library reference format spec; run |
| `screens[5].prose, explain` | "w" creates or empties the file; write adds no newline; with closes the file at the end of the block | correct | Python tutorial 7.2; run |
| `screens[6].explain, quiz[q-append-mode]` | "a" keeps what is there and writes at the end | correct | Python tutorial 7.2; run |
| `screens[8]` | python3 savings.py runs the file top to bottom then exits; python or py on Windows; at >>> a file name is a NameError | correct | Python tutorial 2.1; Using Python on Windows 4.8 (py launcher); run: NameError name savings |
| `screens[9].prose, summary` | B_n = B_0 (1 + r)^n; the loop computes exactly this | correct | loop against the power for 3 balances, 4 rates, n = 0..30 to relative 1e-12 (concepts E); "exactly" is exact in arithmetic, equal to the last bits in floats |
| `screens[10].prose` | f"{r:.2%}" shows 0.0128 as 1.28% | correct | Library reference format spec, type %; run |

## review-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.options[right]` | key: `10.0` only | correct | run, concepts A: this is what Python does |
| `items[0].widget.options[both]` | wrong option: `fee worked out`, then `10.0` / You expected every line of the body to run. `return` ends the call at… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[0].widget.options[after]` | wrong option: `10.0`, then `fee worked out` / Nothing in the body runs after `return`, so that line never prints. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[0].widget.options[none]` | wrong option: `None` / The function does return: `amount * 0.002` is 10.0. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[1].widget.options[right]` | key: Line 4, `change = closes[i + 1] - closes[i]` | correct | run or recomputation, concepts A2: this is what Python does |
| `items[1].widget.options[top]` | wrong option: Line 9, `print(worst_day(closes))` / You read the top File line, the oldest call. Python stopped on the bo… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[1].widget.options[first]` | wrong option: Line 1 of the file / The traceback never mentions line 1. Start from the bottom File line. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[2].widget.options[right]` | key: The text `'1200\n'` | correct | run, concepts A: this is what Python does |
| `items[2].widget.options[number]` | wrong option: The number `1200` / `split` never converts. Every piece is text until you call `int` or `… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[2].widget.options[price]` | wrong option: The text `'245.00'` / That is index 1. Index 2 is the third piece. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[2].widget.options[error]` | wrong option: Nothing: index 2 is out of range / The line has two commas, so it splits into three pieces: indexes 0, 1… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[3].widget.answer` | key: 31.84 | correct | run, concepts A |
| `items[3].feedback.byKey.simple` | slip 30: You took 2% of the first £1,500.00. The fourth year's 2% is paid on £1,591.81. | correct | recomputed from the mistake its line names (concepts B) |
| `items[3].feedback.byKey.b` | slip 1623.65: That is `b`, the balance after four years. The line prints `b - a`, one year's growth. | correct | recomputed from the mistake its line names (concepts B) |
| `items[4].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[4].feedback.byKey.test-1` | test-1 line: Test 1 expects about 101.17. `None` means the function prints instead of returning; 151.75 means you div… | correct | sweep under the page harness: prints gives test-1; len - 1 gives test-1 |
| `items[5].widget.options[right]` | key: It stops with a `NameError` | correct | run, concepts A: this is what Python does |
| `items[5].widget.options[sum]` | wrong option: It prints `203.7` / You expected `s` to outlive the call. It lived in the call's frame, w… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[5].widget.options[zero]` | wrong option: It prints `0.0` / There is no `s` in the main program at all, not even the starting 0.0. | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[5].widget.options[type]` | wrong option: It stops with a `TypeError` / A `TypeError` needs a value of the wrong kind. Here the main program … | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[6].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[6].feedback.byKey.error` | error line: Your script stops before the tests run. A `ValueError` about `Close` means the header is still being con… | correct | sweep under the page harness: header kept gives error |
| `items[6].feedback.byKey.test-1` | test-1 line: Test 1 expects 101.0. About 84.17 means you divided by the line count, header included. | correct | sweep under the page harness: divide by line count gives test-1 |
| `items[7].widget.options[right]` | key: Open the file with `"w"` once, then write each day inside the loop | correct | run or recomputation, concepts A2: this is what Python does |
| `items[7].widget.options[inside]` | wrong option: Open with `"w"` inside the loop and write each day / Each pass empties the file again, so only `Wed` would be left. | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[7].widget.options[print]` | wrong option: Loop over the days and `print` each one / `print` writes to the screen, not to the file. `report.txt` is never … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[7].widget.options[return]` | wrong option: Loop over the days and `return` each one / `return` ends the function on the first pass and writes nothing to th… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[0].explain` | return ends the call at once | correct | Language reference 7.6; run |

## homework-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.solution` | solution and 4 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[0].feedback.byKey.test-1` | test-1 line: Test 1 expects 147.0: 50 shares gain £3.00 each, then two £1.50 fees. 148.5 charges one fee; 0.0 charges… | correct | sweep under the page harness: one fee gives test-1; fees per share gives test-1; wrong way round gives test-1 |
| `items[1].widget.solution` | solution and 7 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[1].feedback.byKey.test-1` | test-1 line: Test 1 expects 0.25 (£120.00 to £90.00). About 0.31 compares the highest and lowest prices in any order;… | correct | sweep under the page harness: high and low in any order gives test-1; peak never moves gives test-1 |
| `items[1].feedback.byKey.test-2` | test-2 line: Test 2 expects 0.3, from £250.00 to £175.00 across several days. About 0.271 measures one-day falls only… | correct | sweep under the page harness: one-day falls gives test-2 |
| `items[2].widget.solution` | solution and 5 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[2].feedback.byKey.test-1` | test-1 line: Test 1 expects the text `'Tue'`. A number back means you returned the price, not the day; `'Wed'` means … | correct | sweep under the page harness: returns the price gives test-1; text compare gives test-1 |
| `items[2].feedback.byKey.test-4` | test-4 line: Test 4 has a tie at £101.00. Use `>` rather than `>=` so the first day keeps the lead. | correct | sweep under the page harness: >= gives test-4 |
| `items[3].widget.solution` | solution and 3 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[3].feedback.byKey.test-1` | test-1 line: Test 1 expects `'VOD 1.28%\n'`. Check the newline at the end and use `:.2%`, which multiplies by 100 and… | correct | sweep under the page harness: no newline gives test-1 |
| `items[3].feedback.byKey.test-2` | test-2 line: Test 2 logs two stocks and expects both lines. Only the last one means `"w"` emptied the file; use `"a"`. | correct | sweep under the page harness: w mode gives test-2 |
| `items[4].widget.options[right]` | key: A line with no comma, such as an empty last line | correct | run or recomputation, concepts A2: this is what Python does |
| `items[4].widget.options[header]` | wrong option: The header line `Day,Close` / The header would give a `ValueError` about `Close`. An `IndexError` m… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[4].widget.options[na]` | wrong option: A price written as `n/a` / `n/a` would give a `ValueError` from `float`. Here `parts[1]` itself … | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[4].widget.options[call]` | wrong option: Line 11 of the script / Line 11 only calls the function. Python stopped on line 5, the bottom… | correct | run or recomputation, concepts A2: not what Python does; its why line read against the run |
| `items[5].widget.options[right]` | key: `1000.0` | correct | run, concepts A: this is what Python does |
| `items[5].widget.options[grown]` | wrong option: `1157.625` / You expected `grow` to change `savings`. It changes its own local `ba… | correct | recomputed from the mistake its why names (concepts B) |
| `items[5].widget.options[none]` | wrong option: `None` / `savings` is set to 1000.00 and nothing assigns to it again, so it is… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[5].widget.options[error]` | wrong option: A `TypeError` / Nothing does arithmetic on `None` here: the `None` that `grow` return… | correct | run, concepts A: not what Python does; its why line read against the run |
| `items[6].widget.answer` | key: 630.5 | correct | run or recomputation, concepts A2 |
| `items[6].feedback.byKey.no-interest` | slip 600: That adds the deposits with no interest. Each deposit earns 5% for every full year after it. | correct | recomputed from the mistake its line names (concepts B) |
| `items[6].feedback.byKey.start-of-year` | slip 662.03: That pays each deposit in at the start of the year, so it earns an extra year of interest. | correct | recomputed from the mistake its line names (concepts B) |
| `items[7].model` | model answer and rubric: **(a) Reading the traceback.** Start at the last line: a `ValueError`, because … | correct | every printed output and error in the model run (concepts A, the model blocks) |
| `items[8].widget.solution` | solution and 7 hidden tests | correct | grade-all --code under Pyodide 0.27.7: the solution passes every hidden test and example, the starter fails; expected values recomputed in concepts E |
| `items[8].feedback.byKey.test-1` | test-1 line: Test 1 is one year at £10.00 a month: £120.00. A ValueError, or an error naming str, means a text was no… | correct | sweep under the page harness: no float gives test-1; prints, no script print yet gives test-1; raise before paying gives test-1 |
| `items[8].feedback.byKey.test-2` | test-2 line: Year 1 pays £240.00, then the fee rises 10% to £22.00: £504.00 in all. 480.0 means `10 // 100` gave 0, s… | correct | sweep under the page harness: rise // 100 gives test-2; return inside loop gives test-2; int(fee), no script print yet gives test-2 |
| `items[8].feedback.byKey.test-3` | test-3 line: Test 3's rise is 3.5%, and `int()` cannot read `"3.5"`. Turn both texts into numbers with `float()`. | correct | sweep under the page harness: int(rise) gives test-3 |
| `items[8].feedback.byKey.test-6` | test-6 line: Test 6 is a 0-year contract, so nothing is paid and the total is 0. | correct | sweep under the page harness: year loop from 1 pays first year outside gives test-6 |
| `items[8].feedback.byKey.test-7` | test-7 line: Your function passes, but the printed line does not match. Call it on the form's two texts for 2 years, … | correct | sweep under the page harness: right function, no print gives test-7 |
| `items[8].feedback.byKey.error` | error line: Your code could not start. Read the last line of the error below the editor, then the line it points to. | correct | sweep under the page harness: prints, with the script print line gives test-1; int(fee), with the script print line gives test-1; SyntaxError gives error |
| `items[1].prose` | maximum drawdown as a fraction of the running peak: 30/120 = 0.25 | correct | recomputed (concepts E) |
| `items[6].prose` | deposits at the end of each year, interest on the start-of-year balance: 630.50 | correct | recomputed; the timing convention is stated |
| `items[7].model (d)` | index -1 is legal, so the loop from 0 pairs the first close with the last and raises nothing | correct | run: five numbers print |


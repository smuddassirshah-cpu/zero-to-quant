# Claim ledger: py-found L1 to L3, round 2 (blind)

Auditor: Fable, audit session 11, 12 Nov 2026. Scope: `app/content/courses/py-found/` lessons l1 to l12, review-1 to review-3, homework-1 to homework-3. Stage 1, full depth. Written before any earlier review, audit, report or ledger for this course was opened.

How the rows were made. Every prose block, option `why`, hint, feedback line, explain, summary line, model answer and rubric line was read in full and judged against a derivation, a named source or a run. Graded keys (`KEY:`) and slip values (`SLIP`) have their own rows. The table was then laid out by a script from the content files, so paths and claim text are exact (claims are cut at 110 characters; code blocks show as `[code]`). Rows of one screen that rest on the same run or derivation share one basis, written once and then shown as "as the row above"; a row that makes a claim of its own has its own basis. No claim-free line was dropped, so some rows (for example "Not quite right. Read the first failing test.") carry only the screen's basis.

Basis vocabulary:
- "run `label`" is a check of that name in `docs/reports/py-found-L1-3-r2-concepts.py` (447 checks, exit 0 on CPython 3.13.18). Checks marked "subprocess" run a real script in a fresh folder.
- "harness" is the last section of the same script, a run of all 58 code widgets: each `solution` against its `tests` (all pass), each `starter` (none passes all), each `how` test count, and each `feedback.byKey.test-N` index. Examples were compared with the tests in a one-off run. The named slips were traced by hand to the first failing test.
- "docs" is the Python 3.12 documentation, section named.

Version note. Pyodide 0.27.7 is CPython 3.12. Behaviour checked here is version-stable. Three message wordings differ by version and are matched by prefix: `NameError` for a standard-library name (3.12 and later append "Did you forget to import ...?"), and the shadowed-module `ImportError` and `AttributeError` (3.13 appends a renaming hint; 3.12 prints the lines the content shows).

Verdicts: `correct`, `wrong`, `imprecise`, `misleading`, `unverified`. Findings are numbered as in `docs/reviews/audit-py-found-1-3-r2.md`.

## l1-why-not-0-3.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A 10p coin and a 20p coin make 30p. This check looks as safe as arithmetic gets. [code] | correct | run `l1 0.1+0.2 != 0.3`, `l1 repr sum`, `l1 0.3 to 17 dp`, `l1 gap 5.6e-17` (gap is exactly 2^-54) |
| `screens[0].widget.options[0].why` | You did the sum in decimal, as on paper. Python stores 0.1 and 0.2 in binary, and their sum lands a hair aw... | correct | as the row above |
| `screens[0].widget.options[1].text` | KEY: `False` | correct | as the row above |
| `screens[0].widget.options[2].why` | You printed the sum. The line prints the comparison `total == 0.3`, which is `True` or `False`. | correct | as the row above |
| `screens[0].widget.options[3].why` | `==` works on floats. It asks whether the two values are exactly equal, to the last digit. | correct | as the row above |
| `screens[0].hints[0].text` | `==` asks for an exact match, down to the last stored digit. | correct | as the row above |
| `screens[0].hints[1].text` | Python stores 0.3, and the sum, as separate values. Do they have to agree exactly? | correct | as the row above |
| `screens[0].hints[2].text` | 0.1 and 0.2 are each stored slightly off. Their sum is 0.30000000000000004, so `==` gives `False`. | correct | as the row above |
| `screens[0].feedback.correct` | The sum is stored as 0.30000000000000004, so it is not equal to 0.3. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. `==` needs the two floats to match exactly. | correct | as the row above |
| `screens[0].feedback.byKey.true` | You did the sum in decimal, as on paper. Python stores 0.1 and 0.2 in binary, and their sum lands a hair aw... | correct | as the row above |
| `screens[0].explain.text` | `==` needs an exact match. The sum is stored as 0.30000000000000004 and 0.3 as 0.29999999999999999. At this... | correct | as the row above |
| `screens[1].prose` | Decimal has the same problem with one third. Keep more digits of 0.333… with the slider and watch the gap t... | correct | 1/3 has no finite decimal expansion (3 does not divide a power of 10); 1/10 has none in binary (5 does not divide a power of 2); run `l1 0.1 binary`, `l1 53 bits`; IEEE 754 binary64 |
| `screens[1].widget.options[0].text` | KEY: It shrinks every time but never reaches zero | correct | as the row above |
| `screens[1].widget.options[1].why` | The dots meet because the line is too coarse to show the gap. The table still shows one: 0.00000000333 at 8... | correct | as the row above |
| `screens[1].widget.options[2].why` | Each extra 3 brings the stored value closer. Watch the last column fall as you slide right. | correct | as the row above |
| `screens[1].widget.options[3].why` | Read the last column at 1 digit and at 4. Each digit makes the gap ten times smaller. | correct | as the row above |
| `screens[1].hints[0].text` | Slide to the far right and read the last column. | correct | as the row above |
| `screens[1].hints[1].text` | Watch the gap between these two dots, then the last column once they meet. | correct | as the row above |
| `screens[1].feedback.correct` | Every digit cuts the gap tenfold, yet 0.333… never ends. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Read the last column of the table at several positions. | correct | as the row above |
| `screens[1].explain.text` | One third has no finite decimal form, so any stored copy stops short. Binary has the same problem with one ... | correct | as the row above |
| `screens[2].prose` | A **float** is Python's number with a decimal point. It is stored in binary with about 17 significant digit... | imprecise | Finding 6. 53 bits carry 53 log10(2) = 15.95 decimal digits (sys.float_info.dig is 15); 17 is the count needed to print a double uniquely, not its precision; run `l1 17 digits identify a double` |
| `screens[2].widget.options[0].why` | You expected `print` to tidy the sum. It prints the shortest decimal that identifies the stored value, and ... | correct | run `l1 stored 0.1/0.2/0.3` (Decimal of the stored doubles), `l1 0.1 and 0.2 high, 0.3 low`; repr is the shortest round-tripping decimal (Python tutorial, Floating Point Arithmetic) |
| `screens[2].widget.options[1].text` | KEY: `0.30000000000000004` | correct | as the row above |
| `screens[2].widget.options[2].why` | You took the stored 0.3 from the table. The stored 0.1 and 0.2 are both a little high, so their sum lands a... | correct | as the row above |
| `screens[2].hints[0].text` | Are the stored 0.1 and 0.2 above or below the true values? | correct | as the row above |
| `screens[2].hints[1].text` | Both are a little high, so the sum is a little high. The stored 0.3 is a little low. | correct | as the row above |
| `screens[2].hints[2].text` | The sum is stored just above 0.3, and `print` shows it as 0.30000000000000004. | correct | as the row above |
| `screens[2].feedback.correct` | Two values stored a little high add to a value a little high. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Compare the stored 0.1 and 0.2 with their true values. | correct | as the row above |
| `screens[2].explain.text` | Both inputs are stored slightly high, so their sum is slightly high. 0.3 is stored slightly low. `print` sh... | correct | as the row above |
| `screens[3].prose` | Binary writes halves, quarters and eighths exactly, the way decimal writes tenths exactly. Tenths are binar... | correct | run `l1 s3 exact checks`, `l1 s3 tenth checks False`, `l1 0.1*3`, `l1 0.7+0.1`; dyadic rationals are exact in binary64 |
| `screens[3].hints[0].text` | Which numbers are made of halves and quarters only? | correct | as the row above |
| `screens[3].hints[1].text` | These use only halves, quarters and whole numbers. | correct | as the row above |
| `screens[3].hints[2].text` | 0.5, 0.25, 1.5 and 2.5 are exact, so those three checks print `True`. Each check here with a tenth in it pr... | correct | as the row above |
| `screens[3].feedback.correct` | Halves and quarters are exact; tenths drift. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Ask which numbers are whole halves, quarters or eighths. | correct | as the row above |
| `screens[3].feedback.byKey.r0c0` | You left out `0.5 + 0.25 == 0.75`. A half and a quarter are exact in binary, so the sum is exact and this p... | correct | as the row above |
| `screens[3].feedback.byKey.r1c0` | `0.1 + 0.2 == 0.3` is the check from the first screen. The stored 0.1 and 0.2 are slightly high, so it prin... | correct | as the row above |
| `screens[3].feedback.byKey.r2c0` | You left out `0.25 * 4 == 1.0`. A quarter is exact in binary, and so is four of them: it prints `True`. | correct | as the row above |
| `screens[3].feedback.byKey.r3c0` | `0.1 * 3` is 0.30000000000000004, because 0.1 is stored slightly high. This prints `False`. | correct | as the row above |
| `screens[3].feedback.byKey.r4c0` | Tenths are not exact in binary. `0.7 + 0.1` is 0.7999999999999999, so this prints `False`. | correct | as the row above |
| `screens[3].feedback.byKey.r5c0` | You left out `1.5 + 2.5 == 4.0`. Halves and whole numbers are exact in binary, so this prints `True`. | correct | as the row above |
| `screens[3].explain.text` | You picked the checks made only of halves, quarters and whole numbers, which binary stores exactly. Every c... | correct | as the row above |
| `screens[4].prose` | So never test computed floats with `==`. Test the gap. Python has a gap test built in: `math.isclose(a, b)`... | correct | math.isclose docs: abs(a-b) <= max(rel_tol*max(/a/,/b/), abs_tol), rel_tol=1e-9, abs_tol=0; run `l1 isclose pair`, `l1 isclose allowance 3e-10/6e-26`, `l1 isclose abs_tol` |
| `screens[4].widget.options[0].text` | KEY: `True`, then `False` | correct | as the row above |
| `screens[4].widget.options[1].why` | You read tiny as tiny in size. `isclose` scales the allowed gap by the larger number, here the gap itself, ... | correct | as the row above |
| `screens[4].widget.options[2].why` | You treated `isclose` like `==`. Next to 0.3 it allows a gap of 0.0000000003, which covers this drift easily. | correct | as the row above |
| `screens[4].widget.options[3].why` | That is the reverse. The first gap is tiny next to 0.3; the second is measured against itself, since the ot... | correct | as the row above |
| `screens[4].hints[0].text` | Work out one billionth of the larger number on each line. | correct | as the row above |
| `screens[4].hints[1].text` | On the second line the larger number is the tiny gap itself, since the other is 0.0. | correct | as the row above |
| `screens[4].hints[2].text` | Line 1 allows about 0.0000000003, so it is `True`. Line 2 allows one billionth of the gap itself, so it is ... | correct | as the row above |
| `screens[4].feedback.correct` | Next to 0.3 the allowance is generous; next to 0.0 it is a billionth of the gap itself. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. Fill in the allowed gap for each line, then compare. | correct | as the row above |
| `screens[4].feedback.byKey.tt` | You read tiny as tiny in size. `isclose` scales the allowed gap by the larger number, here the gap itself, ... | correct | as the row above |
| `screens[4].explain.text` | The allowance is one billionth of the larger number. Next to 0.3 that covers the drift; next to 0.0 the lar... | correct | as the row above |
| `screens[5].prose` | Money has a natural tolerance that also works near zero: half a penny. Write your own gap test: two prices ... | correct | run `l1 same_price no abs slip`, `l1 same_price row 1`; harness: solution passes 6 tests, no-abs slip first fails test 3 |
| `screens[5].widget.how` | Check runs 6 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[5].hints[0].text` | The gap between two numbers is their difference, made positive. | correct | run `l1 same_price no abs slip`, `l1 same_price row 1`; harness: solution passes 6 tests, no-abs slip first fails test 3 |
| `screens[5].hints[1].text` | `abs(10.00 - 10.003)` is 0.003, the gap in the first row. | correct | as the row above |
| `screens[5].hints[2].text` | `return abs(a - b) < 0.005` | correct | as the row above |
| `screens[5].feedback.correct` | A gap under half a penny counts as the same price. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Read the first failing test and work its gap out by hand. | correct | as the row above |
| `screens[5].feedback.byKey.test-1` | Test 1 checks `0.1 + 0.2` against `0.3` and expects `True`. If you got `False`, you compared with `==`; com... | correct | as the row above |
| `screens[5].feedback.byKey.test-3` | Test 3 compares £10.00 with £10.01 and expects `False`. If you got `True`, you tested `a - b` without `abs`... | correct | as the row above |
| `screens[5].explain.text` | `abs(a - b)` measures the gap whichever price is larger, and `< 0.005` sets the tolerance. Test 1 passes: a... | correct | as the row above |
| `screens[6].prose` | A savings pot takes ten deposits of £0.10. The script checks the total at the end. [code] | correct | run `l1 ten deposits`, `l1 running totals` |
| `screens[6].widget.options[0].why` | You expected the small errors to wash out. Each sum is rounded again, and the total ends at 0.9999999999999... | correct | as the row above |
| `screens[6].widget.options[1].text` | KEY: `short` | correct | as the row above |
| `screens[6].widget.options[2].why` | The program prints one of its two messages, never the total itself. | correct | as the row above |
| `screens[6].widget.options[3].why` | `range(10)` runs exactly ten times, whatever the values inside the loop. | correct | as the row above |
| `screens[6].hints[0].text` | Each `+= 0.1` adds a value that is not exactly a tenth, and each sum is rounded again. | correct | as the row above |
| `screens[6].hints[1].text` | After three deposits the total is already 0.30000000000000004. | correct | as the row above |
| `screens[6].hints[2].text` | The ten deposits add to 0.9999999999999999, so `total == 1.0` is `False`. | correct | as the row above |
| `screens[6].feedback.correct` | Ten deposits add to 0.9999999999999999, so `==` fails. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Track the running total after each deposit. | correct | as the row above |
| `screens[6].feedback.byKey.cancel` | You expected the small errors to wash out. Each sum is rounded again, and the total ends at 0.9999999999999... | correct | as the row above |
| `screens[6].explain.text` | You added a slightly wrong value ten times, and every sum was rounded again. The total ends at 0.9999999999... | correct | as the row above |
| `screens[7].prose` | Money has a cleaner fix: count whole pence. Whole numbers are exact in Python however many you add. `round(... | correct | round(x) returns an int, nearest with ties to even; the tie rule is taught in homework-1 items[0]; run `l1 round returns int`, `hw1 round ties` |
| `screens[7].widget.how` | Check runs 6 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[7].hints[0].text` | Turn each price into pence before it joins the total. | correct | run `l1 0.29*100`, `l1 19.99*100`, `l1 int slip 1999`, `l1 unrounded float`, `l1 round returns int`; ints are arbitrary precision (Python docs, Numeric Types) |
| `screens[7].hints[1].text` | `0.29 * 100` is 28.999999999999996, so pick the function that goes to the nearest whole number. | correct | as the row above |
| `screens[7].hints[2].text` | Inside the loop: `total += round(p * 100)`. | correct | as the row above |
| `screens[7].feedback.correct` | Each price becomes whole pence before it is added, so nothing drifts. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Read the first failing test and what your function returned. | correct | as the row above |
| `screens[7].feedback.byKey.test-2` | Test 2 expects 2000 pence from £19.99 and £0.01. If you got 1999, you used `int`, which chops: `19.99 * 100... | correct | as the row above |
| `screens[7].feedback.byKey.test-3` | Test 3 expects 29 pence from £0.29. If you got 28, you used `int`, which chops: `0.29 * 100` is 28.99999999... | correct | as the row above |
| `screens[7].feedback.byKey.test-6` | Test 6 checks the type. Use `round(p * 100)`, which gives an `int`, rather than adding floats. | correct | as the row above |
| `screens[7].explain.text` | Each `round(p * 100)` snaps one price to whole pence before it joins the total, so no drift builds up. Test... | correct | as the row above |
| `screens[8].prose` | Every check you wrote asked one question: is the gap within a tolerance? $$/a - b/ < \text{tol}$$ `math.isc... | correct | run `l1 isclose(x,0) acts like ==`, `l1 round(-0.4)==0`; abs(pnl) < 0.005 is same_price with b = 0 |
| `screens[8].widget.options[0].why` | You compared with `==`. A sum of float trades can land a hair away from 0.0, as 0.1 + 0.2 − 0.3 did. | correct | as the row above |
| `screens[8].widget.options[1].why` | That is the edge case from earlier. Next to 0.0 the allowed gap is a billionth of the size of `pnl`, so it ... | correct | as the row above |
| `screens[8].widget.options[2].text` | KEY: `abs(pnl) < 0.005` | correct | as the row above |
| `screens[8].widget.options[3].why` | `round` goes to whole pounds, so a £0.40 loss would pass as zero. | correct | as the row above |
| `screens[8].feedback.correct` | A gap under half a penny counts as zero. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Look for the test that has a tolerance and keeps it above zero. | correct | as the row above |
| `screens[8].explain.text` | `abs(pnl) < 0.005` is the `same_price` test with zero as the second price. It ignores drift far below a pen... | correct | as the row above |
| `screens[9].prose` | You have £550.00 and a share costs £1.10, so you can buy exactly 500 shares. Floats disagree: [code] `a // ... | correct | run `l1 550/1.10`, `l1 7//2`, `l1 10000/300`, `l1 pence route`; 55000 // 110 = 500 and 500 x 1.10 = 550.00 |
| `screens[9].widget.how` | Check runs 6 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[9].hints[0].text` | Turn both amounts into whole pence first. | correct | run `l1 550/1.10`, `l1 7//2`, `l1 10000/300`, `l1 pence route`; 55000 // 110 = 500 and 500 x 1.10 = 550.00 |
| `screens[9].hints[1].text` | £550.00 is 55000 pence and £1.10 is 110 pence. Which operator divides and drops the remainder? | correct | as the row above |
| `screens[9].hints[2].text` | `return round(cash * 100) // round(price * 100)` | correct | as the row above |
| `screens[9].feedback.correct` | 55000 pence buys 500 shares at 110 pence, exactly. | correct | as the row above |
| `screens[9].feedback.generic` | Not quite right. Read the first failing test and redo it in pence by hand. | correct | as the row above |
| `screens[9].feedback.byKey.test-1` | Test 1 expects 500 shares. If you got 499, you divided the floats: `550.00 / 1.10` is 499.99999999999994. C... | correct | as the row above |
| `screens[9].feedback.byKey.test-3` | Test 3 expects 33 whole shares. If you got 33.333333333333336, use `//` to drop the part share. | correct | as the row above |
| `screens[9].explain.text` | In pence the sum is `55000 // 110`, exactly 500. Whole numbers divide without drift, so the order size is r... | correct | as the row above |
| `summary.ideas[0]` | A float stores the nearest binary value, so tenths and hundredths drift by tiny amounts. | correct | restates s2, s4, s7; run `l1 0.29*100`, `l1 isclose abs_tol` |
| `summary.ideas[1]` | Compare floats by their gap: `abs(a - b) < tol`, or `math.isclose`, with `abs_tol` near zero. | correct | as the row above |
| `summary.ideas[2]` | For money, count whole pence with `round(p * 100)`: integers never drift. | correct | as the row above |
| `summary.formula.tex` | /a - b/ < \text{tol} | correct | as the row above |
| `summary.formula.note` | `math.isclose(a, b)` uses one billionth of the larger number; near 0.0 pass `abs_tol`. | correct | as the row above |
| `summary.trap` | `int(0.29 * 100)` is 28, not 29: `int` chops, `round` goes to the nearest. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l1 q round(2.675,2)`, `l1 q 2.675 stored` |
| `quiz[0].widget.options[0].why` | You rounded the decimal you typed. Python stores 2.675 as 2.67499999…, just below halfway, so it rounds down. | correct | as the row above |
| `quiz[0].widget.options[1].text` | KEY: `2.67` | correct | as the row above |
| `quiz[0].widget.options[2].why` | Two places means two digits after the point, so the third must go. | correct | as the row above |
| `quiz[0].widget.options[3].why` | That is `round(2.675)` with no places. The 2 asks for two decimal places. | correct | as the row above |
| `quiz[0].feedback.correct` | 2.675 is stored just below 2.675, so it rounds down. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. Think about how 2.675 is stored. | correct | as the row above |
| `quiz[0].explain.text` | 2.675 is stored as 2.67499999999999982236431605997495353221893310546875. That is below the halfway point, s... | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l1 q 6/3`; true division always returns float (PEP 238) |
| `quiz[1].widget.options[0].why` | You expected a whole number because 3 goes into 6 exactly. `/` always gives a float. | correct | as the row above |
| `quiz[1].widget.options[1].text` | KEY: `2.0` | correct | as the row above |
| `quiz[1].widget.options[2].why` | Python prints a float with only the digits it needs. Two places would need an f-string. | correct | as the row above |
| `quiz[1].widget.options[3].why` | 6 and 3 are whole numbers, which floats store exactly, and so is their quotient 2. | correct | as the row above |
| `quiz[1].feedback.correct` | `/` always returns a float; 2.0 is exact. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Which type does `/` return? | correct | as the row above |
| `quiz[1].explain.text` | `/` returns a float even when the division is exact, so `6 / 3` prints 2.0. Whole numbers are exact as floa... | correct | as the row above |
| `quiz[2].prose` | A price of £0.57 is turned into pence with `int(0.57 * 100)`. In Python, `0.57 * 100` is 56.99999999999999. | correct | run `l1 q 0.57*100`; int() truncates towards zero (Python docs, int) |
| `quiz[2].widget.answer` | KEY: 56 | correct | as the row above |
| `quiz[2].widget.accept` | 56 exactly: `int` chops towards zero. | correct | as the row above |
| `quiz[2].widget.wrong[0].value` | SLIP value: 57 | correct | as the row above |
| `quiz[2].feedback.correct` | `int` chops 56.99999999999999 to 56. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. `int` does not round; it drops everything after the point. | correct | as the row above |
| `quiz[2].feedback.byKey.nearest` | You rounded to the nearest whole number. `int` chops instead, so 56.99999999999999 becomes 56. That is why ... | correct | as the row above |
| `quiz[2].explain.text` | `int` drops the fractional part, so 56.99999999999999 becomes 56: a penny lost. `round(0.57 * 100)` gives 57. | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l1 q 0.2+0.4`, `l1 q some tenth sums exact` |
| `quiz[3].widget.options[0].why` | You treated every float sum as unsafe. Halves and quarters are exact in binary, so the first check is `True`. | correct | as the row above |
| `quiz[3].widget.options[1].text` | KEY: `True`, then `False` | correct | as the row above |
| `quiz[3].widget.options[2].why` | 0.2 and 0.4 are tenths, which binary cannot store exactly. Their sum is 0.6000000000000001, so `==` gives `... | correct | as the row above |
| `quiz[3].widget.options[3].why` | That is the reverse. Halves and quarters are the exact ones. | correct | as the row above |
| `quiz[3].feedback.correct` | Quarters are exact; tenths drift. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. Which of the numbers are halves or quarters? | correct | as the row above |
| `quiz[3].explain.text` | 0.5, 0.25 and 0.75 are exact in binary, so the first check is `True`. 0.2 + 0.4 is stored as 0.600000000000... | correct | as the row above |
| `screens[3].widget.answer` | KEY: ["r0c0", "r2c0", "r5c0"] | correct | run `l1 s3 exact checks`, `l1 s3 tenth checks False`, `l1 0.1*3`, `l1 0.7+0.1`; dyadic rationals are exact in binary64 |

## l2-slicing.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Six daily closes. The small numbers under the cells are the indices, counted from 0. [code] | correct | run `l2 [1:4]`; slice a[i:j] takes i <= k < j (Python docs, Common Sequence Operations) |
| `screens[0].hints[0].text` | A slice `[a:b]` starts at index `a`. Does it include index `b`? | correct | as the row above |
| `screens[0].hints[1].text` | The first cell is index 0, so index 1 is 102.50. | correct | as the row above |
| `screens[0].hints[2].text` | Indices 1, 2 and 3: the slice stops just before index 4. | correct | as the row above |
| `screens[0].feedback.correct` | Indices 1, 2 and 3: three closes. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Start at index 1 and stop before index 4. | correct | as the row above |
| `screens[0].feedback.byKey.end-in` | You included index 4. A slice stops just before its end index. | correct | as the row above |
| `screens[0].feedback.byKey.from-one` | You counted the first close as index 1. Python counts from 0, so `closes[1]` is 102.50. | correct | as the row above |
| `screens[0].feedback.byKey.c0` | Index 0 is the first close, 101.20. The slice starts at index 1. | correct | as the row above |
| `screens[0].feedback.byKey.c4` | Index 4 is the end of the slice, and a slice stops before its end. | correct | as the row above |
| `screens[0].feedback.byKey.c5` | Index 5 is past the end of the slice `[1:4]`. | correct | as the row above |
| `screens[0].feedback.byKey.c1` | You missed index 1, 102.50. A slice includes its start index. | correct | as the row above |
| `screens[0].explain.text` | You kept indices 1, 2 and 3. A slice `[a:b]` starts at index `a` and stops before `b`. Inside the list it h... | correct | as the row above |
| `screens[1].prose` | Python also counts from the end. `closes[-1]` is the last close. Slide to move the pointer, and read which ... | correct | run `l2 [-2] is [4]`; negative index -k means len - k (same docs, note 3) |
| `screens[1].widget.answer` | KEY: 4 | correct | as the row above |
| `screens[1].widget.accept` | 4 exactly: `-2` means `len(closes) - 2`, which is 6 − 2. | correct | as the row above |
| `screens[1].widget.wrong[0].value` | SLIP value: 2 | correct | as the row above |
| `screens[1].widget.wrong[1].value` | SLIP value: 3 | correct | as the row above |
| `screens[1].hints[0].text` | Slide the pointer to −2 and read the small index under the cell. | correct | as the row above |
| `screens[1].hints[1].text` | `-1` is the last cell, index 5. | correct | as the row above |
| `screens[1].feedback.correct` | `closes[-2]` and `closes[4]` are the same cell, 103.10. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Slide to −2 and read the index under the pointer. | correct | as the row above |
| `screens[1].feedback.byKey.sign` | Index 2 counts from the front. A minus sign counts back from the end. | correct | as the row above |
| `screens[1].feedback.byKey.off` | You counted one cell too far. `-1` is the last cell, index 5, so `-2` is index 4. | correct | as the row above |
| `screens[1].explain.text` | At −2 the pointer sits on index 4, 103.10. A negative index `-k` means `len(closes) - k`: here `6 - 2 = 4`.... | correct | as the row above |
| `screens[2].prose` | Taking a run of items this way is called **slicing**. Negative indices work in slices too, and a missing en... | correct | run `l2 [-3:]`; repr(100.40) is 100.4 |
| `screens[2].widget.options[0].text` | KEY: `[100.4, 103.1, 104.0]` | correct | as the row above |
| `screens[2].widget.options[1].why` | That is `closes[-3:-1]`: you stopped before the last cell. A missing end runs to the end of the list. | correct | as the row above |
| `screens[2].widget.options[2].why` | You took two cells. `-3` is the third from the end, index 3, and the slice starts there. | correct | as the row above |
| `screens[2].widget.options[3].why` | You read the list backwards. A slice keeps the original order unless you give it a negative step. | correct | as the row above |
| `screens[2].hints[0].text` | Which ordinary index is `-3` in a list of 6? | correct | as the row above |
| `screens[2].hints[1].text` | `-3` is index 3, 100.40. | correct | as the row above |
| `screens[2].hints[2].text` | Start at index 3 and run to the end: indices 3, 4 and 5. | correct | as the row above |
| `screens[2].feedback.correct` | The last three closes, in their original order. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Turn `-3` into an ordinary index, then run to the end. | correct | as the row above |
| `screens[2].explain.text` | `-3` is index 3, and the missing end runs to the last cell. So `closes[-3:]` is always the latest three clo... | correct | as the row above |
| `screens[3].prose` | A slice can take a third number, the **step**: how far to jump each time. `closes[0:6:2]` takes indices 0, ... | correct | run `l2 [1::2]`; two-on slip is closes[1:2] |
| `screens[3].hints[0].text` | The numbers are start, end and step. Here the end is missing. | correct | as the row above |
| `screens[3].hints[1].text` | Start at index 1, then jump 2 at a time. | correct | as the row above |
| `screens[3].hints[2].text` | Indices 1, 3 and 5; index 7 would be next, but the list ends at 5. | correct | as the row above |
| `screens[3].feedback.correct` | From index 1 in steps of 2: indices 1, 3 and 5. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Start at index 1 and jump 2 each time. | correct | as the row above |
| `screens[3].feedback.byKey.from-zero` | You started at index 0. The first number, 1, is the start. | correct | as the row above |
| `screens[3].feedback.byKey.two-on` | You read `2` as the end, so you kept only index 1. With two colons the numbers are start, end and step, and... | correct | as the row above |
| `screens[3].feedback.byKey.c0` | Index 0 comes before the start, index 1. | correct | as the row above |
| `screens[3].feedback.byKey.c2` | Index 2 is skipped: from index 1, a step of 2 lands on 3. | correct | as the row above |
| `screens[3].feedback.byKey.c4` | Index 4 is skipped: the steps land on 1, 3 and 5. | correct | as the row above |
| `screens[3].explain.text` | From index 1 the step of 2 lands on 1, 3 and 5, and the missing end lets it run to the last cell. Index 7 w... | correct | as the row above |
| `screens[4].prose` | A backtest often needs the latest `n` closes. Assume `0 <= n <= len(prices)`. Hidden tests include the smal... | correct | run `l2 -0 slice`; harness: prices[-n:] slip first fails test 4 |
| `screens[4].widget.how` | Check runs 5 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[4].hints[0].text` | Where does the run of the last `n` start, counted from the front? | correct | run `l2 -0 slice`; harness: prices[-n:] slip first fails test 4 |
| `screens[4].hints[1].text` | Run test 4 in your head. What is `-0`? | correct | as the row above |
| `screens[4].hints[2].text` | `return prices[len(prices) - n:]` starts `n` cells before the end, and works when `n` is 0. | correct | as the row above |
| `screens[4].feedback.correct` | `len(prices) - n` marks where the last `n` begin, even when `n` is 0. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. Read the first failing test and work its slice out by hand. | correct | as the row above |
| `screens[4].feedback.byKey.test-4` | Test 4 asks for the last 0 prices and expects `[]`. If you got the whole list, you wrote `prices[-n:]`: wit... | correct | as the row above |
| `screens[4].explain.text` | `len(prices) - n` is the index where the last `n` begin. The tempting `prices[-n:]` breaks at `n = 0`, beca... | correct | as the row above |
| `screens[5].prose` | Two weeks of closes, Monday to Friday. The Fridays sit at index 4 and index 9, and every fifth day after that. | correct | run `l2 fridays`; start-0 slip gives [101.2, 104.0] |
| `screens[5].widget.how` | Check runs 5 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[5].hints[0].text` | You need a start, no end, and a step. | correct | run `l2 fridays`; start-0 slip gives [101.2, 104.0] |
| `screens[5].hints[1].text` | The first Friday is index 4, and Fridays are 5 apart. | correct | as the row above |
| `screens[5].hints[2].text` | `return closes[4::5]` | correct | as the row above |
| `screens[5].feedback.correct` | Start at 4, run to the end, step 5. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Compare your slice's start and step with the highlighted cells. | correct | as the row above |
| `screens[5].feedback.byKey.test-1` | Test 1 expects `[103.1, 105.2]`. If you got `[101.2, 104.0]`, your slice started at 0; start at index 4. If... | correct | as the row above |
| `screens[5].explain.text` | `closes[4::5]` starts at the first Friday and jumps a week each time. Test 2 is an edge case: with only thr... | correct | as the row above |
| `screens[6].prose` | Before adding today's close, you keep a backup of the list in `b`. [code] Each name is a card; each box is ... | correct | run `l2 alias`; assignment binds a name, never copies (Python docs, Data model 3.1) |
| `screens[6].widget.options[0].why` | You treated `b = a` as a copy. It puts a second name on the same list, so the append shows through both. | correct | as the row above |
| `screens[6].widget.options[1].text` | KEY: `4` | correct | as the row above |
| `screens[6].widget.options[2].why` | `len` counts the items. It returns a number, not the list. | correct | as the row above |
| `screens[6].widget.options[3].why` | `b` is a valid name for the same list, so `len(b)` works. | correct | as the row above |
| `screens[6].hints[0].text` | Does `b = a` build a new list, or name an existing one? | correct | as the row above |
| `screens[6].hints[1].text` | Only one line in the program builds a list. | correct | as the row above |
| `screens[6].hints[2].text` | `b = a` makes `b` a second name for the one list. After the append that list has 4 closes. | correct | as the row above |
| `screens[6].feedback.correct` | One list, two names: the append shows through `b`. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Count how many lists the program builds. | correct | as the row above |
| `screens[6].feedback.byKey.copy` | You treated `b = a` as a copy. It puts a second name on the same list, so the append shows through both. | correct | as the row above |
| `screens[6].explain.text` | `b = a` stuck a second name on the same list. `append` changed that one list, so both names see four closes... | correct | as the row above |
| `screens[7].prose` | Every slice of a list builds a new list, so `a[:]`, the slice with no start and no end, is a copy: a new li... | correct | run `l2 slice always new list` |
| `screens[7].hints[0].text` | Which lines build a list, and which only add a name? | correct | as the row above |
| `screens[7].hints[1].text` | `c = a[:]` slices, and a slice is always a new list. | correct | as the row above |
| `screens[7].hints[2].text` | `a` and `b` go on the line 1 list; `c` goes on the line 3 list. | correct | as the row above |
| `screens[7].feedback.correct` | `b` shares the original; `c` has its own copy. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Assignment adds a name; slicing builds a list. | correct | as the row above |
| `screens[7].feedback.byKey.a` | `a` names the list built on line 1. | correct | as the row above |
| `screens[7].feedback.byKey.b` | `b = a` copies the name, not the list, so `b` belongs on the line 1 list. | correct | as the row above |
| `screens[7].feedback.byKey.c` | `a[:]` is a slice, and every slice builds a new list. `c` labels that new list. | correct | as the row above |
| `screens[7].explain.text` | `b = a` added a name; `a[:]` built a new list with the same values. Now `a.append(...)` changes what `b` se... | correct | as the row above |
| `screens[8].prose` | A function that adds a close should not change the list it was given: someone else may hold a name for it. ... | correct | harness: solution passes 4 tests; append-to-argument slip fails test 2 |
| `screens[8].widget.how` | Check runs 4 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[8].hints[0].text` | If you `append` to `closes` itself, the caller's list grows. | correct | harness: solution passes 4 tests; append-to-argument slip fails test 2 |
| `screens[8].hints[1].text` | Copy first with a slice, then append to the copy. | correct | as the row above |
| `screens[8].hints[2].text` | `new = closes[:]`, then `new.append(price)`, then `return new`. | correct | as the row above |
| `screens[8].feedback.correct` | The copy grew; the caller's list did not. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `screens[8].feedback.byKey.test-2` | Test 2 returns your result and the original list side by side. If the original grew too, you appended to `c... | correct | as the row above |
| `screens[8].explain.text` | `closes[:]` built a new list, and only that list grew. Test 2 shows the original afterwards: still two clos... | correct | as the row above |
| `screens[9].prose` | Every slice you took followed one rule: start at $i$, jump by $k$, stop before $j$. $$\texttt{a[i:j:k]} = [... | correct | len(a[i:j]) = j - i for 0 <= i <= j <= len(a); run `l2 count j-i` |
| `screens[9].widget.answer` | KEY: 5 | correct | as the row above |
| `screens[9].widget.accept` | 5 exactly: 7 − 2. | correct | as the row above |
| `screens[9].widget.wrong[0].value` | SLIP value: 6 | correct | as the row above |
| `screens[9].widget.wrong[1].value` | SLIP value: 7 | correct | as the row above |
| `screens[9].feedback.correct` | Indices 2 to 6: five items. | correct | as the row above |
| `screens[9].feedback.generic` | Not quite right. Subtract the start from the end. | correct | as the row above |
| `screens[9].feedback.byKey.both` | You counted index 7 too. The slice stops before its end. | correct | as the row above |
| `screens[9].feedback.byKey.end` | That is the end index, not the count. Subtract the start: 7 − 2. | correct | as the row above |
| `screens[9].explain.text` | The slice takes indices 2, 3, 4, 5 and 6, stopping before 7. That is $7 - 2 = 5$ items, the same $j - i$ co... | correct | as the row above |
| `screens[10].prose` | Traders watch the 5-day average: the mean of the latest five closes. A close above it is read as strength. ... | unverified | 'A close above it is read as strength' is a market-usage remark with no source in the lesson; the code and the mean (103.48) are verified by run `l2 sma` |
| `screens[10].widget.how` | Check runs 5 hidden tests that call your function. A number is accepted when it is within `math.isclose` of... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[10].hints[0].text` | Take the last `n` closes with a slice, then average them. | correct | run `l2 sma` (517.40 / 5 = 103.48; first five 101.40; all ten 102.44) |
| `screens[10].hints[1].text` | `sum(xs)` adds a list of numbers. | correct | as the row above |
| `screens[10].hints[2].text` | `return sum(closes[-n:]) / n` | correct | as the row above |
| `screens[10].feedback.correct` | The last five closes average £103.48. | correct | as the row above |
| `screens[10].feedback.generic` | Not quite right. Check which closes your slice took in test 1. | correct | as the row above |
| `screens[10].feedback.byKey.test-1` | Test 1 expects 103.48, the mean of the last five. If you got 101.40, your slice took the first five instead. | correct | as the row above |
| `screens[10].explain.text` | `closes[-n:]` takes the last `n` closes, `sum` adds them and dividing by `n` gives the mean: £517.40 / 5 = ... | correct | as the row above |
| `summary.ideas[0]` | `a[i:j:k]` starts at index `i`, jumps by `k`, and stops before `j`. A missing part means: from the start, t... | correct | restates s3, s1, s6, s7 |
| `summary.ideas[1]` | A negative index counts from the end: `a[-k]` is `a[len(a) - k]`. | correct | as the row above |
| `summary.ideas[2]` | `b = a` adds a second name for one list. A slice such as `a[:]` builds a new list. | correct | as the row above |
| `summary.formula.tex` | \texttt{a[i:j:k]} = [\,a_i,\ a_{i+k},\ a_{i+2k},\ \dots\,],\ \text{stopping before } j | correct | as the row above |
| `summary.formula.note` | With step 1 it holds $j - i$ items, when both ends lie inside the list. | correct | as the row above |
| `summary.trap` | `b = a` does not copy: change the list through `a` and `b` sees it. Copy with `a[:]`. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l2 q reversed` |
| `quiz[0].widget.options[0].text` | KEY: `[99.8, 102.5, 101.2]` | correct | as the row above |
| `quiz[0].widget.options[1].why` | You ignored the step. A step of −1 walks backwards from the end. | correct | as the row above |
| `quiz[0].widget.options[2].why` | That is `closes[-1:]`. Here the `-1` is the step, after two colons. | correct | as the row above |
| `quiz[0].widget.options[3].why` | A negative step is allowed. It walks from the end towards the start. | correct | as the row above |
| `quiz[0].feedback.correct` | A step of −1 walks the list backwards. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. With two colons, the third number is the step. | correct | as the row above |
| `quiz[0].explain.text` | With no start or end, a step of −1 runs from the last item back to the first. `closes[::-1]` is a reversed ... | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l2 q slice past end` |
| `quiz[1].widget.options[0].why` | You treated the slice like an index. `closes[10]` fails, but a slice past the end just stops at the end. | correct | as the row above |
| `quiz[1].widget.options[1].text` | KEY: `[99.8, 100.4]` | correct | as the row above |
| `quiz[1].widget.options[2].why` | Python never pads a slice. It returns only the items that exist. | correct | as the row above |
| `quiz[1].widget.options[3].why` | Indices 2 and 3 exist, so the slice keeps them. | correct | as the row above |
| `quiz[1].feedback.correct` | A slice past the end stops at the end. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Which of indices 2 to 9 exist? | correct | as the row above |
| `quiz[1].explain.text` | Indices 2 and 3 exist; 4 to 9 do not, and a slice quietly stops at the end. An index past the end, like `cl... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | same behaviour as s6 and s7; run `l2 alias`, `l2 slice always new list` |
| `quiz[2].widget.options[0].why` | You treated the slice as a second name. `a[:]` built a new list, so `b` kept 2 items. | correct | as the row above |
| `quiz[2].widget.options[1].why` | You treated `c = a` as a copy. `c` is another name for `a`'s list, so it sees the append. | correct | as the row above |
| `quiz[2].widget.options[2].text` | KEY: `2 3` | correct | as the row above |
| `quiz[2].widget.options[3].why` | That swaps the two. The slice `b` is the copy; `c` shares the list. | correct | as the row above |
| `quiz[2].feedback.correct` | `b` is a copy and kept 2; `c` shares the list and sees 3. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. Which line built a new list? | correct | as the row above |
| `quiz[2].explain.text` | `b = a[:]` built a copy before the append, so it still has 2 items. `c = a` is a second name for the same l... | correct | as the row above |
| `quiz[3].prose` | `closes` holds 20 daily closes, at indices 0 to 19. | correct | run `l2 q 1:20:3`; slips 6 and 19 = 20 - 1 |
| `quiz[3].widget.answer` | KEY: 7 | correct | as the row above |
| `quiz[3].widget.accept` | 7 exactly: indices 1, 4, 7, 10, 13, 16 and 19. | correct | as the row above |
| `quiz[3].widget.wrong[0].value` | SLIP value: 6 | correct | as the row above |
| `quiz[3].widget.wrong[1].value` | SLIP value: 19 | correct | as the row above |
| `quiz[3].feedback.correct` | Indices 1, 4, 7, 10, 13, 16 and 19. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. List the indices: start at 1 and add 3 while below 20. | correct | as the row above |
| `quiz[3].feedback.byKey.dropped-last` | You stopped at 16. Index 19 is still below the end, 20, so it counts. | correct | as the row above |
| `quiz[3].feedback.byKey.divided` | That is the span from 1 to 20. The step of 3 takes every third index. | correct | as the row above |
| `quiz[3].explain.text` | From 1, steps of 3 give 1, 4, 7, 10, 13, 16 and 19. The next, 22, is past the end. That is 7 items. | correct | as the row above |
| `screens[0].widget.answer` | KEY: ["c1", "c2", "c3"] | correct | run `l2 [1:4]`; slice a[i:j] takes i <= k < j (Python docs, Common Sequence Operations) |
| `screens[0].widget.wrong[0].set` | SLIP set: c1,c2,c3,c4 | correct | as the row above |
| `screens[0].widget.wrong[1].set` | SLIP set: c0,c1,c2,c3 | correct | as the row above |
| `screens[3].widget.answer` | KEY: ["c1", "c3", "c5"] | correct | run `l2 [1::2]`; two-on slip is closes[1:2] |
| `screens[3].widget.wrong[0].set` | SLIP set: c0,c2,c4 | correct | as the row above |
| `screens[3].widget.wrong[1].set` | SLIP set: c1 | correct | as the row above |
| `screens[7].widget.answer` | KEY: {"first": ["a", "b"], "second": ["c"]} | correct | run `l2 slice always new list` |

## l3-unpacking.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A feed stored the best bid and ask the wrong way round: the bid should be the lower price. One line is mean... | correct | run `l3 swap`; right side is evaluated fully before assignment (Python docs, Assignment statements) |
| `screens[0].widget.options[0].text` | KEY: `99.5 100.5` | correct | as the row above |
| `screens[0].widget.options[1].why` | You ran it as two steps: `bid = ask`, then `ask = bid`. Python builds the whole right side first, from the ... | correct | as the row above |
| `screens[0].widget.options[2].why` | The second line does change things: its right side is `(99.5, 100.5)`, handed out to `bid` and `ask` in order. | correct | as the row above |
| `screens[0].widget.options[3].why` | Several names on the left are allowed, as long as the right side has the same number of values. | correct | as the row above |
| `screens[0].hints[0].text` | Work out the whole right side, `ask, bid`, before anything is assigned. | correct | as the row above |
| `screens[0].hints[1].text` | The right side is the pair (99.5, 100.5), built from the old values. | correct | as the row above |
| `screens[0].hints[2].text` | Then `bid` takes 99.5 and `ask` takes 100.5. | correct | as the row above |
| `screens[0].feedback.correct` | The right side was built first, then handed out in order. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Build the right side from the old values first. | correct | as the row above |
| `screens[0].feedback.byKey.seq` | You ran it as two steps: `bid = ask`, then `ask = bid`. Python builds the whole right side first, from the ... | correct | as the row above |
| `screens[0].explain.text` | Python built the pair `(99.5, 100.5)` from the old values, then handed it out left to right. The values nev... | correct | as the row above |
| `screens[1].prose` | The pair on the last screen was a **tuple**: values in a fixed order, written with round brackets. This one... | imprecise | Finding 3. Commas make a tuple, not brackets: the pair on the previous screen had none, and (5) is an int; run `l3 commas make the tuple` |
| `screens[1].hints[0].text` | Python matches the names to the values by position. | correct | positional unpacking; run `l3 swap`, `l3 commas make the tuple` |
| `screens[1].hints[1].text` | The first value goes to the first name. | correct | as the row above |
| `screens[1].feedback.correct` | First to first, second to second, third to third. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Match by position, left to right. | correct | as the row above |
| `screens[1].feedback.byKey.v1` | `VOD` is the first value, so it lands in the first name, `ticker`. | correct | as the row above |
| `screens[1].feedback.byKey.v2` | `72.5` is the second value, so it lands in the second name, `price`. | correct | as the row above |
| `screens[1].feedback.byKey.v3` | `100` is the third value, so it lands in the third name, `qty`. | correct | as the row above |
| `screens[1].explain.text` | You matched names to values by position. Taking a tuple apart into names like this is called **unpacking**.... | correct | as the row above |
| `screens[2].prose` | Unpacking needs one name per value. This time the code asks for only two fields. [code] | correct | run `l3 too many values`, `l3 star` |
| `screens[2].widget.options[0].text` | KEY: It stops with `ValueError: too many values to unpack` | correct | as the row above |
| `screens[2].widget.options[1].why` | You expected Python to drop the extra value. It refuses, because a silent drop could hide a real bug. | correct | as the row above |
| `screens[2].widget.options[2].why` | Only a starred name collects extras: `ticker, *rest = trade` makes `rest` the list `[72.5, 100]`. A plain n... | correct | as the row above |
| `screens[2].widget.options[3].why` | Unpacking goes by position. Python never skips a value to reach a later one. | correct | as the row above |
| `screens[2].hints[0].text` | How many values does `trade` hold, and how many names are on the left? | correct | as the row above |
| `screens[2].hints[1].text` | Three values, two names: where would the third go? | correct | as the row above |
| `screens[2].hints[2].text` | Python will not guess, so it raises `ValueError`. | correct | as the row above |
| `screens[2].feedback.correct` | Three values cannot fit two names. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Count the values and the names. | correct | as the row above |
| `screens[2].explain.text` | Three values cannot fit two names, so Python raises `ValueError` rather than guess. When you need only some... | correct | as the row above |
| `screens[3].prose` | The price in the record was mistyped. Someone tries to fix it in place. [code] | correct | run `l3 tuple assign` (exact message) |
| `screens[3].widget.options[0].text` | KEY: It stops with a `TypeError`: a tuple cannot be changed | correct | as the row above |
| `screens[3].widget.options[1].why` | That works on a list. A tuple is fixed once built, which is what makes it a safe record. | correct | as the row above |
| `screens[3].widget.options[2].why` | Index 1 exists: it is the price. The trouble is the assignment, not the index. | correct | as the row above |
| `screens[3].widget.options[3].why` | Python never builds a new tuple behind your back. You build it yourself. | correct | as the row above |
| `screens[3].hints[0].text` | Can a tuple be changed after it is built? | correct | as the row above |
| `screens[3].hints[1].text` | Lists use square brackets and can change. Tuples use round ones. | correct | as the row above |
| `screens[3].hints[2].text` | Assigning to `trade[1]` raises `TypeError: 'tuple' object does not support item assignment`. | correct | as the row above |
| `screens[3].feedback.correct` | A tuple is fixed once built. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Ask what kind of object `trade` is. | correct | as the row above |
| `screens[3].explain.text` | Tuples are **immutable**: once built, they cannot change. To correct the price, build a new record: `trade ... | correct | as the row above |
| `screens[4].prose` | `enumerate(xs)` hands out `(index, item)` pairs, and a `for` line can unpack each one. [code] | correct | run `l3 enumerate` |
| `screens[4].widget.options[0].text` | KEY: `1`, then `3` | correct | as the row above |
| `screens[4].widget.options[1].why` | You counted from 1. `enumerate` starts at 0 unless you pass `start=1`. | correct | as the row above |
| `screens[4].widget.options[2].why` | You printed the close. `i` is the index half of each pair. | correct | as the row above |
| `screens[4].widget.options[3].why` | The `for` line unpacks each pair into `i` and `px`, so `i` alone is an index. | correct | as the row above |
| `screens[4].hints[0].text` | Which closes are below 100? | correct | as the row above |
| `screens[4].hints[1].text` | 99.80 and 98.90 are below 100. What are their indices? | correct | as the row above |
| `screens[4].hints[2].text` | They sit at index 1 and index 3, and `print(i)` shows the index. | correct | as the row above |
| `screens[4].feedback.correct` | The closes below 100 sit at index 1 and index 3. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. `i` is the index, counted from 0. | correct | as the row above |
| `screens[4].explain.text` | Each pass, `enumerate` handed over a pair like `(1, 99.8)`, and the `for` line unpacked it into `i` and `px... | correct | as the row above |
| `screens[5].prose` | `zip(xs, ys)` pairs two lists item by item. Here one list is shorter. [code] | correct | run `l3 zip stops`, `l3 zip strict` (strict= is Python 3.10+; Pyodide 0.27.7 is 3.12) |
| `screens[5].widget.options[0].text` | KEY: `Mon 101.2` and `Tue 99.8`, then it stops | correct | as the row above |
| `screens[5].widget.options[1].why` | You expected `zip` to pad the short list. It stops as soon as either list runs out. | correct | as the row above |
| `screens[5].widget.options[2].why` | By default `zip` does not complain about lengths. It stops at the shorter one, silently; `zip(days, closes,... | correct | as the row above |
| `screens[5].widget.options[3].why` | `zip` pairs across the lists, one item from each, not one list per line. | correct | as the row above |
| `screens[5].hints[0].text` | What could `zip` pair with `"Wed"`? | correct | as the row above |
| `screens[5].hints[1].text` | Each pass takes one item from each list. | correct | as the row above |
| `screens[5].hints[2].text` | After two pairs `closes` is used up, so the loop ends. | correct | as the row above |
| `screens[5].feedback.correct` | `zip` stops when the shorter list runs out. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Pair the lists row by row and stop when one is empty. | correct | as the row above |
| `screens[5].explain.text` | `zip` made two pairs and stopped when `closes` ran out. That silence is a hazard with mismatched data, and ... | correct | as the row above |
| `screens[6].prose` | `zip(closes, closes[1:])` pairs each close with the next one, and stops when the shorter list runs out. A d... | correct | run `l3 returns`; simple return (p1 - p0)/p0, stated on the screen |
| `screens[6].widget.how` | Check runs 6 hidden tests that call your function. Numbers are accepted within `math.isclose` of the expect... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[6].hints[0].text` | What pairs does `zip(closes, closes[1:])` give for three closes? | correct | run `l3 returns`; simple return (p1 - p0)/p0, stated on the screen |
| `screens[6].hints[1].text` | Unpack each pair in the `for` line: `for prev, cur in zip(closes, closes[1:]):`. | correct | as the row above |
| `screens[6].hints[2].text` | Inside the loop: `rets.append((cur - prev) / prev)`. | correct | as the row above |
| `screens[6].feedback.correct` | Three closes, two pairs, two returns. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `screens[6].feedback.byKey.test-1` | Test 1 expects 0.05 from £100.00 to £105.00. About 0.0476 means you divided by the later close; divide by `... | correct | as the row above |
| `screens[6].feedback.byKey.test-3` | Test 3 expects 2 returns from 3 closes. A different count means your loop did not pair each close with the ... | correct | as the row above |
| `screens[6].explain.text` | `closes[1:]` is one shorter, so `zip` stops after `len(closes) - 1` pairs: one return for each day after th... | correct | as the row above |
| `screens[7].prose` | A trade arrives as a line of text from a file. `split(",")` cuts it at each comma. [code] | correct | run `l3 split strings`, `l3 str*str TypeError`, `l3 convert` |
| `screens[7].widget.options[0].why` | You treated the fields as numbers. `split` hands back strings, so `price` is the text `'72.50'`. | correct | as the row above |
| `screens[7].widget.options[1].text` | KEY: It stops with a `TypeError` | correct | as the row above |
| `screens[7].widget.options[2].why` | That would be `price + qty`, which joins two strings. `*` between two strings is not allowed. | correct | as the row above |
| `screens[7].widget.options[3].why` | Three fields and three names: the counts match. The trouble is on the next line. | correct | as the row above |
| `screens[7].hints[0].text` | What type is each piece that `split` returns? | correct | as the row above |
| `screens[7].hints[1].text` | `split` cuts text into smaller texts: `'VOD'`, `'72.50'` and `'100\n'`. | correct | as the row above |
| `screens[7].hints[2].text` | `'72.50' * '100\n'` multiplies two strings, which raises `TypeError`. | correct | as the row above |
| `screens[7].feedback.correct` | Both fields are still strings, and Python cannot multiply two strings. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Ask what type `price` and `qty` hold. | correct | as the row above |
| `screens[7].feedback.byKey.numbers` | You treated the fields as numbers. `split` hands back strings, so `price` is the text `'72.50'`. | correct | as the row above |
| `screens[7].feedback.byKey.joined` | That would be `price + qty`, which joins two strings. `*` between two strings raises `TypeError`. | correct | as the row above |
| `screens[7].explain.text` | `split` cut the line into three strings: `'VOD'`, `'72.50'` and `'100\n'`. Multiplying two strings is a `Ty... | correct | as the row above |
| `screens[8].prose` | Writing a line is the reverse of splitting one. `",".join(parts)` glues a list of strings with commas betwe... | correct | run `l3 join needs str`, `l3 split/join inverse` |
| `screens[8].widget.how` | Check runs 4 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[8].hints[0].text` | Unpack the tuple first, then turn each part into a string. | correct | run `l3 join needs str`, `l3 split/join inverse` |
| `screens[8].hints[1].text` | `f"{price:.2f}"` writes 72.5 as `'72.50'`; `str(100)` is `'100'`. | correct | as the row above |
| `screens[8].hints[2].text` | `ticker, price, qty = trade`, then `return ",".join([ticker, f"{price:.2f}", str(qty)])`. | correct | as the row above |
| `screens[8].feedback.correct` | Three strings, glued with commas. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `screens[8].feedback.byKey.test-1` | Test 1 expects `'VOD,72.50,100'`. A `TypeError` from `join` means a part was still a number. `'VOD,72.5,100... | correct | as the row above |
| `screens[8].feedback.byKey.error` | Your code stopped with an error. If it was a `TypeError` in `join`, one of the parts was still a number: wr... | correct | as the row above |
| `screens[8].explain.text` | Unpacking named the three fields; the f-string and `str` turned the numbers into text; `join` put commas on... | correct | as the row above |
| `screens[9].prose` | Every time, the left side named the parts and the right side supplied them, matched by position: $$\texttt{... | correct | run `l3 enumerate rows`, `l3 unpack list itself`, `l3 three names ValueError` |
| `screens[9].widget.options[0].text` | KEY: `for ticker, price in rows:` | correct | as the row above |
| `screens[9].widget.options[1].why` | You added `enumerate`. Each pair would then be (index, record), so `price` would hold a whole tuple. | correct | as the row above |
| `screens[9].widget.options[2].why` | That unpacks the list itself: two records into two names, so `ticker` would be the whole first tuple. | correct | as the row above |
| `screens[9].widget.options[3].why` | Each record has two fields, so three names raise `ValueError`. | correct | as the row above |
| `screens[9].feedback.correct` | Each pass hands over one two-field record. | correct | as the row above |
| `screens[9].feedback.generic` | Not quite right. Match the names to the fields of one record. | correct | as the row above |
| `screens[9].explain.text` | Each pass of `for` hands over one record, such as `("VOD", 72.5)`, and two names take its two fields. The o... | correct | as the row above |
| `screens[10].prose` | A broker's file has lines like `' vod,72.50,100\n'`: stray spaces, lower case, a newline. A clean record is... | correct | run `l3 float/int ignore spaces`; harness: no-strip slip fails test 2, line-only strip fails test 5 |
| `screens[10].widget.how` | Check runs 6 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[10].hints[0].text` | Split the line, unpack the three fields, then clean and convert each one. | correct | run `l3 float/int ignore spaces`; harness: no-strip slip fails test 2, line-only strip fails test 5 |
| `screens[10].hints[1].text` | `float` and `int` ignore spaces around a number, but a ticker needs its own `strip()`. | correct | as the row above |
| `screens[10].hints[2].text` | `ticker, price, qty = line.strip().split(",")`, then `return (ticker.strip().upper(), float(price), int(qty... | correct | as the row above |
| `screens[10].feedback.correct` | A clean, fixed record from a messy line. | correct | as the row above |
| `screens[10].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `screens[10].feedback.byKey.test-1` | Test 1 expects `('VOD', 72.5, 100)`. If you got strings such as `'72.50'`, convert the fields with `float` ... | correct | as the row above |
| `screens[10].feedback.byKey.test-2` | Test 2 has a lower-case ticker after a space. Strip the ticker and call `.upper()` on it. | correct | as the row above |
| `screens[10].feedback.byKey.test-5` | Test 5 has a space after the ticker, inside the line. Strip the ticker field itself, not only the whole line. | correct | as the row above |
| `screens[10].explain.text` | `split` and unpacking named the three fields; `strip`, `upper`, `float` and `int` cleaned each one. Returni... | correct | as the row above |
| `summary.ideas[0]` | A tuple is a fixed record: values in order, and it cannot be changed once built. | correct | restates s1 to s7 |
| `summary.ideas[1]` | Unpacking matches names to values by position, and the counts must agree. `for` lines unpack each pair from... | correct | as the row above |
| `summary.ideas[2]` | `zip(closes, closes[1:])` pairs each close with the next, and stops when the shorter list runs out. | correct | as the row above |
| `summary.formula.tex` | \texttt{a, b, c} = (x,\ y,\ z) \;\Rightarrow\; a = x,\ b = y,\ c = z | correct | as the row above |
| `summary.formula.note` | One name per value. `split` gives strings: convert before doing sums. | correct | as the row above |
| `summary.trap` | `line.split(",")` gives strings, not numbers: `'72.50' * '100'` is a `TypeError`. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l3 q in` |
| `quiz[0].widget.options[0].why` | On a list, `in` checks whole items. `'OD'` is part of `'VOD'` but is not an item of the list. | correct | as the row above |
| `quiz[0].widget.options[1].text` | KEY: `True`, then `False` | correct | as the row above |
| `quiz[0].widget.options[2].why` | On a string, `in` looks for a run of characters, and `'OD'` appears inside `'VOD'`. | correct | as the row above |
| `quiz[0].widget.options[3].why` | That is the reverse. Strings search inside; lists compare whole items. | correct | as the row above |
| `quiz[0].feedback.correct` | On a string `in` searches inside; on a list it compares whole items. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. Ask what `in` compares on each kind of sequence. | correct | as the row above |
| `quiz[0].explain.text` | For strings, `in` asks whether the text appears anywhere inside, so `'OD' in 'VOD'` is `True`. For lists, i... | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l3 q join` |
| `quiz[1].widget.options[0].text` | KEY: `VOD, BP, AZN` | correct | as the row above |
| `quiz[1].widget.options[1].why` | `join` puts the separator only between parts, never after the last. | correct | as the row above |
| `quiz[1].widget.options[2].why` | `join` returns one string, not a list. | correct | as the row above |
| `quiz[1].widget.options[3].why` | The string before `.join` is the separator, here a comma and a space. | correct | as the row above |
| `quiz[1].feedback.correct` | The separator goes between the parts only. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. The string before `.join` goes between each pair of parts. | correct | as the row above |
| `quiz[1].explain.text` | `", ".join(...)` puts a comma and a space between neighbouring parts, giving one string. With three parts t... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | run `l3 q enumerate start` |
| `quiz[2].widget.options[0].why` | You started at 0. `start=1` makes the first pair `(1, 'Mon')`, so Tuesday is 2. | correct | as the row above |
| `quiz[2].widget.options[1].text` | KEY: `2 Tue` | correct | as the row above |
| `quiz[2].widget.options[2].why` | `enumerate` puts the index first, so `day` holds the number. | correct | as the row above |
| `quiz[2].widget.options[3].why` | The `for` line unpacks each pair, so `print` gets two separate values. | correct | as the row above |
| `quiz[2].feedback.correct` | With `start=1`, Tuesday is day 2. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. List the pairs `enumerate` hands out with `start=1`. | correct | as the row above |
| `quiz[2].explain.text` | With `start=1`, `enumerate` hands out `(1, 'Mon')` and `(2, 'Tue')`. Each pair is unpacked into `day` and `... | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l3 q strip split` |
| `quiz[3].widget.options[0].text` | KEY: `['72', '50']` | correct | as the row above |
| `quiz[3].widget.options[1].why` | `split` always returns strings, so the parts keep their quotes. | correct | as the row above |
| `quiz[3].widget.options[2].why` | `strip` ran first and removed the spaces and the newline. | correct | as the row above |
| `quiz[3].widget.options[3].why` | The separator here is `"."`, so the cut happens at the decimal point. | correct | as the row above |
| `quiz[3].feedback.correct` | `strip` trims, then `split(".")` cuts at the point. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. Apply `strip` first, then `split`. | correct | as the row above |
| `quiz[3].explain.text` | `strip` removed the leading spaces and the newline, leaving `'72.50'`. `split(".")` then cut it at the poin... | correct | as the row above |
| `screens[1].widget.answer` | KEY: {"ticker": ["v1"], "price": ["v2"], "qty": ["v3"]} | correct | positional unpacking; run `l3 swap`, `l3 commas make the tuple` |

## l4-one-line-lists.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Three daily returns, as decimals. One line turns them into percentages. [code] | correct | run `l4 pct` |
| `screens[0].widget.options[0].text` | KEY: `[1.2, -3.4, 0.5]` | correct | as the row above |
| `screens[0].widget.options[1].why` | You read it as a loop that prints. The brackets build one list, and one `print` shows it. | correct | as the row above |
| `screens[0].widget.options[2].why` | `pct` is a new list holding `round(r * 100, 1)` for each `r`; only `rets` keeps the decimals. | correct | as the row above |
| `screens[0].widget.options[3].why` | The `for r in rets` part defines `r`, even though it is written after the expression. | correct | as the row above |
| `screens[0].hints[0].text` | Read it as: for each `r` in `rets`, work out `round(r * 100, 1)`. | correct | as the row above |
| `screens[0].hints[1].text` | The first `r` is 0.012, which becomes 1.2. | correct | as the row above |
| `screens[0].hints[2].text` | Each return times 100, to one place, collected in a new list: `[1.2, -3.4, 0.5]`. | correct | as the row above |
| `screens[0].feedback.correct` | One new list, one value per return. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Apply `round(r * 100, 1)` to each return in turn, and collect the results. | correct | as the row above |
| `screens[0].explain.text` | The line ran `round(r * 100, 1)` for each `r` and collected the results in a new list, in order. It is the ... | correct | as the row above |
| `screens[1].prose` | Ten daily returns. Put an `if` at the end, and the line keeps only the items that pass the test. [code] | correct | 0.0 < 0 is False; run `l4 losses idx` |
| `screens[1].hints[0].text` | Test each return: is it below 0? | correct | as the row above |
| `screens[1].hints[1].text` | Look closely at index 5. | correct | as the row above |
| `screens[1].feedback.correct` | Four losses, and the flat day left out. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Keep a return only if `r < 0` is `True`. | correct | as the row above |
| `screens[1].feedback.byKey.zero` | You kept the flat day at index 5. `0.0 < 0` is `False`: a flat day is not a loss. | correct | as the row above |
| `screens[1].feedback.byKey.c0` | 0.012 is a gain, so `r < 0` is `False` and it is left out. | correct | as the row above |
| `screens[1].feedback.byKey.c2` | 0.005 is a gain, so it is left out. | correct | as the row above |
| `screens[1].feedback.byKey.c4` | 0.021 is a gain, so it is left out. | correct | as the row above |
| `screens[1].feedback.byKey.c5` | 0.0 is not below 0, so `r < 0` is `False`: a flat day is left out. | correct | as the row above |
| `screens[1].feedback.byKey.c7` | 0.009 is a gain, so it is left out. | correct | as the row above |
| `screens[1].feedback.byKey.c9` | 0.017 is a gain, so it is left out. | correct | as the row above |
| `screens[1].feedback.byKey.c1` | You missed −0.034, a loss. | correct | as the row above |
| `screens[1].feedback.byKey.c3` | You missed −0.008, a loss. | correct | as the row above |
| `screens[1].feedback.byKey.c6` | You missed −0.015, a loss. | correct | as the row above |
| `screens[1].feedback.byKey.c8` | You missed −0.002, a small loss but still below 0. | correct | as the row above |
| `screens[1].explain.text` | You kept the four returns below zero, in their original order. The flat day, 0.0, fails `r < 0`: that is th... | correct | as the row above |
| `screens[2].prose` | A list built from a `for` inside square brackets is a **list comprehension**. The optional `if` filters. Un... | correct | run `l4 losses idx` |
| `screens[2].widget.options[0].text` | KEY: `[1, 3, 6, 8]` | correct | as the row above |
| `screens[2].widget.options[1].why` | That collects `r`. The expression at the front is `i`, the index half of each pair. | correct | as the row above |
| `screens[2].widget.options[2].why` | You counted from 1. `enumerate` starts at 0. | correct | as the row above |
| `screens[2].widget.options[3].why` | You kept index 5. Its return is 0.0, and `0.0 < 0` is `False`. | correct | as the row above |
| `screens[2].hints[0].text` | The front of the comprehension says what is collected. | correct | as the row above |
| `screens[2].hints[1].text` | `i` is the index of each return that passes `r < 0`. | correct | as the row above |
| `screens[2].hints[2].text` | The losses sit at indices 1, 3, 6 and 8. | correct | as the row above |
| `screens[2].feedback.correct` | The indices of the four losing days. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Collect the index `i` of every return below 0. | correct | as the row above |
| `screens[2].explain.text` | `enumerate` handed out `(i, r)` pairs, the `if` kept the losing ones, and the front collected `i`. So `idx`... | correct | as the row above |
| `screens[3].prose` | A report needs the dates of the losing days. Dates and returns arrive as two lists of the same length. | correct | harness: solution passes 4 tests; `r <= 0` slip first fails test 2 |
| `screens[3].widget.how` | Check runs 4 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[3].hints[0].text` | You need each date beside its return: which function pairs two lists? | correct | harness: solution passes 4 tests; `r <= 0` slip first fails test 2 |
| `screens[3].hints[1].text` | `for d, r in zip(dates, rets)` unpacks each pair. | correct | as the row above |
| `screens[3].hints[2].text` | `return [d for d, r in zip(dates, rets) if r < 0]` | correct | as the row above |
| `screens[3].feedback.correct` | Zip, unpack, filter, collect: in one line. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `screens[3].feedback.byKey.test-1` | Test 1 expects `['Tue']`. If you got `[-0.034]`, you collected the return; put `d` at the front. | correct | as the row above |
| `screens[3].feedback.byKey.test-2` | Test 2 has a flat Tuesday, 0.0. If it appeared, your test was `r <= 0`; a loss needs `r < 0`. | correct | as the row above |
| `screens[3].explain.text` | `zip` paired each date with its return, the `for` unpacked each pair, the `if` kept the losses, and the fro... | correct | as the row above |
| `screens[4].prose` | `sorted(xs)` returns a new list in order. `key=` names a function whose result is compared instead of each ... | correct | run `l4 sorted`, `l4 capitals before lower case` (code points A-Z 65-90, a-z 97-122) |
| `screens[4].widget.options[0].text` | KEY: `['AZN', 'VOD', 'bp']`, then `['AZN', 'bp', 'VOD']` | correct | as the row above |
| `screens[4].widget.options[1].why` | You sorted as a person would, ignoring case. Plain `sorted` compares character codes, and every capital com... | correct | as the row above |
| `screens[4].widget.options[2].why` | The key changes what is compared: with `str.lower`, `'VOD'` is compared as `'vod'`, which comes after `'bp'`. | correct | as the row above |
| `screens[4].widget.options[3].why` | The key only decides the order. `sorted` hands back the original items, capitals and all. | correct | as the row above |
| `screens[4].hints[0].text` | In character codes, does `'V'` come before or after `'b'`? | correct | as the row above |
| `screens[4].hints[1].text` | All capitals come before all lower-case letters, so `'bp'` is the odd one out. | correct | as the row above |
| `screens[4].hints[2].text` | Plain: `AZN`, `VOD`, `bp`. With the key the comparison uses `azn`, `bp`, `vod`, but the items keep their ow... | correct | as the row above |
| `screens[4].feedback.correct` | The key decides the order; the items come back unchanged. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. Work out each line separately: first by character codes, then by the lower-case versions. | correct | as the row above |
| `screens[4].explain.text` | Plain `sorted` puts every capital first, so `'bp'` lands last. With `key=str.lower` the comparison uses `'a... | correct | as the row above |
| `screens[5].prose` | Your own function can be the key. It receives one item and returns what to compare. [code] | correct | run `l4 by price` |
| `screens[5].hints[0].text` | `price_of` turns each trade into its price. Which price is largest? | correct | as the row above |
| `screens[5].hints[1].text` | `reverse=True` puts the largest first. Find the largest price. | correct | as the row above |
| `screens[5].hints[2].text` | 120.00, then 72.50, then 4.85: AZN, VOD, BP. | correct | as the row above |
| `screens[5].feedback.correct` | Largest price first, and the tuples come back whole. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Compare the prices only, then put the largest first. | correct | as the row above |
| `screens[5].explain.text` | `sorted` called `price_of` on each trade and compared 72.5, 120.0 and 4.85. `reverse=True` put the largest ... | correct | as the row above |
| `screens[6].prose` | A risk manager wants the largest moves either way. `abs` works as a key: `key=abs` compares sizes and ignor... | correct | run `l4 biggest moves`; sorted returns a new list (docs, sorted) |
| `screens[6].widget.how` | Check runs 5 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[6].hints[0].text` | Sort by size, largest first, then keep the first `n`. | correct | run `l4 biggest moves`; sorted returns a new list (docs, sorted) |
| `screens[6].hints[1].text` | `sorted(rets, key=abs, reverse=True)` orders by size. A slice keeps the first `n`. | correct | as the row above |
| `screens[6].hints[2].text` | `return sorted(rets, key=abs, reverse=True)[:n]` | correct | as the row above |
| `screens[6].feedback.correct` | Sorted by size, signs kept, first `n` taken. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `screens[6].feedback.byKey.test-1` | Test 1 expects `[-0.034, 0.021]`. `[0.021, 0.012]` means you sorted by value; add `key=abs`. `[0.034, 0.021... | correct | as the row above |
| `screens[6].feedback.byKey.test-5` | Test 5 shows your result beside the list you were given. If that list came back reordered, you used `rets.s... | correct | as the row above |
| `screens[6].explain.text` | `key=abs` compared sizes, `reverse=True` put the largest first, and `[:n]` kept `n` of them. Test 3 asks fo... | correct | as the row above |
| `screens[7].prose` | Each day is a `(day, return)` tuple. You want the best day. [code] | correct | run `l4 max tuples`; tuples compare lexicographically (docs, Comparing Sequences) |
| `screens[7].widget.options[0].why` | You expected `max` to look at the returns. Tuples compare field by field, starting with the day's name. | correct | as the row above |
| `screens[7].widget.options[1].text` | KEY: `('Wed', 0.012)` | correct | as the row above |
| `screens[7].widget.options[2].why` | `max` returns one of the items, a whole tuple, never a single field. | correct | as the row above |
| `screens[7].widget.options[3].why` | Tuples compare like words in a dictionary: first fields first, then the second fields on a tie. | correct | as the row above |
| `screens[7].hints[0].text` | How does Python compare two tuples? | correct | as the row above |
| `screens[7].hints[1].text` | It compares the first fields, the names, and only moves on when they tie. | correct | as the row above |
| `screens[7].hints[2].text` | `'Wed'` is the largest name alphabetically, so `max` picks Wednesday. | correct | as the row above |
| `screens[7].feedback.correct` | `max` compared the names, and `'Wed'` won. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Compare the tuples field by field, starting with the first. | correct | as the row above |
| `screens[7].feedback.byKey.by-return` | You expected `max` to look at the returns. Tuples compare field by field, starting with the day's name. | correct | as the row above |
| `screens[7].feedback.byKey.field` | `max` returns one of the items, a whole tuple, never a single field. | correct | as the row above |
| `screens[7].explain.text` | `max` compared the first fields: `'Wed'` beats `'Tue'` and `'Mon'` alphabetically. The returns were never l... | correct | as the row above |
| `screens[8].prose` | Every comprehension is a loop in disguise. Rebuild the loop that makes the same list as `[r for r in rets i... | correct | comprehension semantics (Python reference 6.2.4): equivalent nested for/if with append |
| `screens[8].hints[0].text` | The list has to exist before anything is appended. | correct | as the row above |
| `screens[8].hints[1].text` | The `for` comes before the `if`, as in the comprehension. | correct | as the row above |
| `screens[8].hints[2].text` | Empty list, `for`, `if`, `append`. | correct | as the row above |
| `screens[8].feedback.correct` | Same parts, same order: the comprehension just drops the `append`. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Make the list first, then loop, then filter, then add. | correct | as the row above |
| `screens[8].feedback.byKey.init` | The empty list has to come first: you cannot append to a list that does not exist yet. | correct | as the row above |
| `screens[8].feedback.byKey.add` | The `append` goes last, inside the `if`, so only the losses are added. | correct | as the row above |
| `screens[8].explain.text` | Read the comprehension left to right after its first part: `for r in rets`, then `if r < 0`. The first part... | correct | as the row above |
| `screens[9].prose` | A comprehension is that loop, folded: $$[\,f(x)\ \texttt{for}\ x\ \texttt{in}\ xs\ \texttt{if}\ c(x)\,]$$ I... | correct | a running balance needs the previous result: V_t = V_{t-1}(1 + r_t); the other three are per-item maps or filters |
| `screens[9].widget.options[0].text` | KEY: Growing £1,000.00 by each return in turn | correct | as the row above |
| `screens[9].widget.options[1].why` | Each item is changed on its own, so one comprehension does it: `[r * 100 for r in rets]`. | correct | as the row above |
| `screens[9].widget.options[2].why` | That is one filter: `[r for r in rets if r < -0.02]`. | correct | as the row above |
| `screens[9].widget.options[3].why` | `list(zip(dates, rets))` does it in one call, with no loop at all. | correct | as the row above |
| `screens[9].feedback.correct` | Each balance needs the one before it, so the loop is clearer. | correct | as the row above |
| `screens[9].feedback.generic` | Not quite right. Look for the job where each step depends on the last result. | correct | as the row above |
| `screens[9].explain.text` | Today's balance is yesterday's balance times `1 + r`, so each step needs the previous result. A comprehensi... | correct | as the row above |
| `screens[10].prose` | A backtest logs each day as a `(date, return)` tuple. The report needs the dates of the best and worst days... | correct | run `l4 max dates slip`, `l4 dates are Mon-Thu`; harness: solution passes 4 tests |
| `screens[10].widget.how` | Check runs 4 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[10].hints[0].text` | `max` with `key=ret_of` returns the whole best tuple. | correct | run `l4 max dates slip`, `l4 dates are Mon-Thu`; harness: solution passes 4 tests |
| `screens[10].hints[1].text` | Unpack it: `best_date, _ = max(days, key=ret_of)`. | correct | as the row above |
| `screens[10].hints[2].text` | Do the same with `min`, then `return (best_date, worst_date)`. | correct | as the row above |
| `screens[10].feedback.correct` | The best day was 12 October and the worst 13 October. | correct | as the row above |
| `screens[10].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `screens[10].feedback.byKey.test-1` | Test 1 expects `('2026-10-12', '2026-10-13')`. If the best came out as `'2026-10-15'`, `max` compared the d... | correct | as the row above |
| `screens[10].explain.text` | `max` and `min` compared returns through `ret_of` and handed back whole tuples. Unpacking each tuple pulled... | correct | as the row above |
| `summary.ideas[0]` | `[f(x) for x in xs if c(x)]` builds a new list: one transform, one optional filter, the original order kept. | correct | restates s1, s4 to s9 |
| `summary.ideas[1]` | `sorted`, `max` and `min` take `key=`: the key decides what is compared, and the whole item comes back. | correct | as the row above |
| `summary.ideas[2]` | Keep a loop when each step needs the previous result, such as a running balance. | correct | as the row above |
| `summary.formula.tex` | [\,f(x)\ \texttt{for}\ x\ \texttt{in}\ xs\ \texttt{if}\ c(x)\,] | correct | as the row above |
| `summary.formula.note` | The same list as a loop that appends $f(x)$ whenever $c(x)$ holds. | correct | as the row above |
| `summary.trap` | `max(days)` on `(name, return)` tuples compares the names first. Pass `key=` to compare the returns. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l4 q filter` |
| `quiz[0].widget.options[0].text` | KEY: `[101.2, 100.4]` | correct | as the row above |
| `quiz[0].widget.options[1].why` | That would be `[p > 100 for p in closes]`. Here the test sits in the `if`, which filters. | correct | as the row above |
| `quiz[0].widget.options[2].why` | 100.40 is above 100 too, so it stays. | correct | as the row above |
| `quiz[0].widget.options[3].why` | The `if p > 100` drops 99.80. | correct | as the row above |
| `quiz[0].feedback.correct` | The filter keeps the two closes above 100. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. Keep each close that passes `p > 100`, in order. | correct | as the row above |
| `quiz[0].explain.text` | The `if` kept 101.2 and 100.4 and dropped 99.8, and the front, `p`, collected the closes themselves, in the... | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l4 q min key` |
| `quiz[1].widget.options[0].why` | You compared the strings themselves. `key=len` compares their lengths. | correct | as the row above |
| `quiz[1].widget.options[1].text` | KEY: `bp` | correct | as the row above |
| `quiz[1].widget.options[2].why` | `min` returns the item with the smallest key, not the key itself. | correct | as the row above |
| `quiz[1].widget.options[3].why` | `'VOD'` has three letters; `'bp'` has two. | correct | as the row above |
| `quiz[1].feedback.correct` | `'bp'` has the shortest length, so it is the minimum. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Compare `len` of each item. | correct | as the row above |
| `quiz[1].explain.text` | `key=len` compared 3, 2 and 3. The smallest key belongs to `'bp'`, and `min` returned that item, not the 2. | correct | as the row above |
| `quiz[2].prose` | [code] | correct | run `l4 q sort returns None` |
| `quiz[2].widget.options[0].why` | You treated `.sort()` like `sorted`. It reorders `rets` in place and returns `None`. | correct | as the row above |
| `quiz[2].widget.options[1].text` | KEY: `None` | correct | as the row above |
| `quiz[2].widget.options[2].why` | `ordered` does not hold the list at all. `.sort()` returns `None`. | correct | as the row above |
| `quiz[2].widget.options[3].why` | Lists do have a `.sort()` method. It works in place. | correct | as the row above |
| `quiz[2].feedback.correct` | `.sort()` changes the list in place and returns `None`. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. What does the method `.sort()` return? | correct | as the row above |
| `quiz[2].explain.text` | `rets.sort()` reordered `rets` itself and returned `None`, so `ordered` is `None`. Use `sorted(rets)` when ... | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l4 q <= count`; slips 2 (strict) and 6 (all) |
| `quiz[3].widget.answer` | KEY: 4 | correct | as the row above |
| `quiz[3].widget.accept` | 4 exactly: two flat days and two losses. | correct | as the row above |
| `quiz[3].widget.wrong[0].value` | SLIP value: 2 | correct | as the row above |
| `quiz[3].widget.wrong[1].value` | SLIP value: 6 | correct | as the row above |
| `quiz[3].feedback.correct` | Two losses plus two flat days. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. `<=` keeps the zeros as well as the losses. | correct | as the row above |
| `quiz[3].feedback.byKey.strict` | You counted only the losses. The test is `r <= 0`, so the two flat days count too. | correct | as the row above |
| `quiz[3].feedback.byKey.all` | That is every return. The filter drops the two gains. | correct | as the row above |
| `quiz[3].explain.text` | `r <= 0` keeps −0.011, −0.002 and both 0.0 days: four items. With `r < 0` it would be 2. Read the compariso... | correct | as the row above |
| `screens[1].widget.answer` | KEY: ["c1", "c3", "c6", "c8"] | correct | 0.0 < 0 is False; run `l4 losses idx` |
| `screens[1].widget.wrong[0].set` | SLIP set: c1,c3,c5,c6,c8 | correct | as the row above |
| `screens[5].widget.answer` | KEY: ["azn", "vod", "bp"] | correct | run `l4 by price` |
| `screens[8].widget.answer` | KEY: ["init", "for", "if", "add"] | correct | comprehension semantics (Python reference 6.2.4): equivalent nested for/if with append |

## review-1.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | [code] | correct | run `r1 1.1+2.2` |
| `items[0].widget.options[0].why` | You did the sum on paper. 1.1 and 2.2 are stored slightly off, and their sum is 3.3000000000000003. | correct | as the row above |
| `items[0].widget.options[1].text` | KEY: `False` | correct | as the row above |
| `items[0].widget.options[2].why` | The line prints the comparison, which is `True` or `False`, not the sum. | correct | as the row above |
| `items[0].feedback.correct` | `1.1 + 2.2` is 3.3000000000000003, so `==` fails. | correct | as the row above |
| `items[0].feedback.generic` | Not quite right. Are 1.1 and 2.2 stored exactly? | correct | as the row above |
| `items[0].explain.text` | Tenths have no exact binary form, so 1.1 and 2.2 are stored slightly off and their sum misses 3.3. Compare ... | correct | as the row above |
| `items[1].prose` | [code] | correct | run `r1 [-4:-1]` |
| `items[1].widget.options[0].text` | KEY: `[102.5, 99.8, 100.4]` | correct | as the row above |
| `items[1].widget.options[1].why` | You ran to the end. An end of `-1` stops before the last item. | correct | as the row above |
| `items[1].widget.options[2].why` | That is `closes[:3]`. A negative start counts from the end: `-4` is index 1. | correct | as the row above |
| `items[1].widget.options[3].why` | A slice keeps the original order unless the step is negative. | correct | as the row above |
| `items[1].feedback.correct` | Indices 1, 2 and 3, in order. | correct | as the row above |
| `items[1].feedback.generic` | Not quite right. Turn `-4` and `-1` into ordinary indices first. | correct | as the row above |
| `items[1].explain.text` | In a list of 5, `-4` is index 1 and `-1` is index 4. The slice runs from index 1 and stops before index 4. | correct | as the row above |
| `items[2].prose` | [code] | correct | nested unpacking of (2, ('Wed', 100.4)) |
| `items[2].widget.options[0].text` | KEY: `2 Wed 100.4` | correct | as the row above |
| `items[2].widget.options[1].why` | You counted from 1. `enumerate` starts at 0. | correct | as the row above |
| `items[2].widget.options[2].why` | `enumerate` hands out `(i, pair)`, two values, and the brackets unpack the pair. The counts match. | correct | as the row above |
| `items[2].widget.options[3].why` | The brackets in `(d, px)` unpack each pair, so `d` and `px` are separate values. | correct | as the row above |
| `items[2].feedback.correct` | The last pass has `i` = 2, `d` = `'Wed'` and `px` = 100.4. | correct | as the row above |
| `items[2].feedback.generic` | Not quite right. Write out the last item `enumerate` hands over, then unpack it. | correct | as the row above |
| `items[2].explain.text` | The last item is `(2, ('Wed', 100.4))`. The names `i, (d, px)` have the same shape, so each value lands in ... | correct | as the row above |
| `items[3].prose` | [code] | correct | keys 100, 250, 5: AZN first |
| `items[3].widget.options[0].text` | KEY: `AZN` | correct | as the row above |
| `items[3].widget.options[1].why` | BP has the largest quantity. `sorted` puts the smallest key first unless `reverse=True`. | correct | as the row above |
| `items[3].widget.options[2].why` | That is the first trade before sorting. `sorted` reorders by quantity. | correct | as the row above |
| `items[3].widget.options[3].why` | `[0][0]` takes the first field of the first trade: its ticker, not its quantity. | correct | as the row above |
| `items[3].feedback.correct` | AZN has the smallest quantity, 5, so it sorts first. | correct | as the row above |
| `items[3].feedback.generic` | Not quite right. Sort by the third field, smallest first, then take the first trade's ticker. | correct | as the row above |
| `items[3].explain.text` | `qty_of` gave 100, 250 and 5, so AZN sorts first. `[0]` takes that whole trade and the second `[0]` its tic... | correct | as the row above |
| `items[4].prose` | A refund of −£4.35 is turned into pence with `int(-4.35 * 100)`. In Python, `-4.35 * 100` is -434.999999999... | correct | run `r1 -4.35*100` (int -434, round -435, floor -435) |
| `items[4].widget.answer` | KEY: -434 | correct | as the row above |
| `items[4].widget.accept` | −434 exactly: `int` chops towards zero. | correct | as the row above |
| `items[4].widget.wrong[0].value` | SLIP value: -435 | correct | as the row above |
| `items[4].widget.wrong[1].value` | SLIP value: 434 | correct | as the row above |
| `items[4].feedback.correct` | `int` chops −434.99999999999994 towards zero, to −434. | correct | as the row above |
| `items[4].feedback.generic` | Not quite right. `int` drops the part after the point, towards zero; it does not round. | correct | as the row above |
| `items[4].feedback.byKey.nearest` | You rounded, or rounded down. `int` chops towards zero, so −434.99999999999994 becomes −434. `round(-4.35 *... | correct | as the row above |
| `items[4].feedback.byKey.sign` | The refund is negative, so int(−434.99…) drops the fraction towards zero and gives −434. A positive 434 los... | correct | as the row above |
| `items[4].explain.text` | `int` drops the fractional part towards zero, so −434.99999999999994 becomes −434 and the refund is a penny... | correct | as the row above |
| `items[5].prose` | [code] | correct | run `l2 alias`, `l2 slice always new list` |
| `items[5].widget.options[0].text` | KEY: `101.2 100.0` | correct | as the row above |
| `items[5].widget.options[1].why` | You treated the slice as a second name. `closes[:]` built a copy before the change. | correct | as the row above |
| `items[5].widget.options[2].why` | You treated `alias = closes` as a copy. It is a second name for the same list. | correct | as the row above |
| `items[5].widget.options[3].why` | That swaps the two. The slice is the copy; the plain assignment shares the list. | correct | as the row above |
| `items[5].feedback.correct` | The copy kept 101.2; the second name sees 100.0. | correct | as the row above |
| `items[5].feedback.generic` | Not quite right. Which line built a new list? | correct | as the row above |
| `items[5].explain.text` | `snap = closes[:]` built a new list, so changing `closes[0]` leaves it alone. `alias = closes` shares the o... | correct | as the row above |
| `items[6].prose` | [code] | correct | run `r1 str*2` |
| `items[6].widget.options[0].why` | You treated the field as a number. `split` gives strings, so `'4.85' * 2` repeats the text. | correct | as the row above |
| `items[6].widget.options[1].text` | KEY: `4.854.85` | correct | as the row above |
| `items[6].widget.options[2].why` | A string times a whole number is allowed: it repeats the string. A string times a string or a float fails. | correct | as the row above |
| `items[6].widget.options[3].why` | `fields[1]` is one string, not a list, so `* 2` repeats the whole string. | correct | as the row above |
| `items[6].feedback.correct` | `'4.85' * 2` repeats the text. | correct | as the row above |
| `items[6].feedback.generic` | Not quite right. What type does `split` return? | correct | as the row above |
| `items[6].explain.text` | `fields[1]` is the string `'4.85'`, and a string times 2 is the string twice. Convert with `float(fields[1]... | correct | as the row above |
| `items[7].prose` | A day is an up day when its close is above the close before it. Number the days from 0, so day 1 is the fir... | correct | harness: solution passes 5 tests; `>=` slip fails test 4 |
| `items[7].widget.how` | Check runs 5 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[7].feedback.correct` | Each up day is found by pairing a close with the one before. | correct | harness: solution passes 5 tests; `>=` slip fails test 4 |
| `items[7].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `items[7].feedback.byKey.test-1` | Test 1 expects `[1, 3]`. `[0, 2]` means your numbering starts at 0 for the first pair: pass `start=1` to `e... | correct | as the row above |
| `items[7].feedback.byKey.test-4` | Test 4 has a flat day. A close equal to the one before is not an up day: use `>`, not `>=`. | correct | as the row above |
| `items[7].explain.text` | `zip(closes, closes[1:])` pairs each close with the next, `enumerate(..., start=1)` numbers the later day, ... | correct | as the row above |

## homework-1.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | 2.5 and 3.5 are stored exactly, so each sits exactly halfway between two whole numbers. [code] | correct | run `hw1 round ties`; round-half-to-even (docs, round) |
| `items[0].widget.options[0].why` | You rounded each half up, as at school. Python rounds an exact tie to the even neighbour: 2.5 to 2 and 3.5 ... | correct | as the row above |
| `items[0].widget.options[1].text` | KEY: `6` | correct | as the row above |
| `items[0].widget.options[2].why` | `round` with no places returns an `int`, so the sum prints without a point. | correct | as the row above |
| `items[0].widget.options[3].why` | Python does not always round down. 3.5 goes to 4, its even neighbour. | correct | as the row above |
| `items[0].feedback.correct` | Ties go to the even neighbour: 2 + 4 = 6. | correct | as the row above |
| `items[0].feedback.generic` | Not quite right. Python breaks an exact tie towards the even whole number. | correct | as the row above |
| `items[0].explain.text` | Python rounds an exact tie to the even neighbour, so `round(2.5)` is 2 and `round(3.5)` is 4. Over many tra... | correct | as the row above |
| `items[1].prose` | `closes` holds 20 daily closes, at indices 0 to 19. | correct | run `hw1 [3:-2]` (slips 16, 17, 1) |
| `items[1].widget.answer` | KEY: 15 | correct | as the row above |
| `items[1].widget.accept` | 15 exactly: indices 3 to 17. | correct | as the row above |
| `items[1].widget.wrong[0].value` | SLIP value: 16 | correct | as the row above |
| `items[1].widget.wrong[1].value` | SLIP value: 17 | correct | as the row above |
| `items[1].widget.wrong[2].value` | SLIP value: 1 | correct | as the row above |
| `items[1].feedback.correct` | Indices 3 to 17: 15 items. | correct | as the row above |
| `items[1].feedback.generic` | Not quite right. Turn `-2` into an ordinary index first. | correct | as the row above |
| `items[1].feedback.byKey.kept-end` | You included index 18. `-2` is index 18, and the slice stops before it. | correct | as the row above |
| `items[1].feedback.byKey.no-start` | You dropped only the first three: that is `closes[3:]`. The end `-2` also drops the last two closes. | correct | as the row above |
| `items[1].feedback.byKey.abs` | You subtracted the raw numbers, 3 and 2. Turn `-2` into index 18 first, then use $j - i$. | correct | as the row above |
| `items[1].explain.text` | `-2` means `20 - 2 = 18`, so the slice is `closes[3:18]`: $18 - 3 = 15$ items. It drops the first three clo... | correct | as the row above |
| `items[2].prose` | A tiny order book starts as three empty levels of `[price, size]`. [code] | correct | run `hw1 list * 3` |
| `items[2].widget.options[0].why` | You expected three separate levels. `* 3` repeats the reference to one inner list, so all three slots hold ... | correct | as the row above |
| `items[2].widget.options[1].text` | KEY: `[[99.5, 0.0], [99.5, 0.0], [99.5, 0.0]]` | correct | as the row above |
| `items[2].widget.options[2].why` | `book[0]` exists, and so does `book[0][0]`. | correct | as the row above |
| `items[2].widget.options[3].why` | `* 3` on the outer list repeats its one item, the inner list. It does not flatten anything. | correct | as the row above |
| `items[2].feedback.correct` | One inner list, three references to it. | correct | as the row above |
| `items[2].feedback.generic` | Not quite right. How many inner lists does `[[0.0, 0.0]] * 3` build? | correct | as the row above |
| `items[2].explain.text` | `[[0.0, 0.0]] * 3` builds one inner list and repeats the reference to it three times, like `b = a`. Changin... | correct | as the row above |
| `items[3].prose` | [code] | correct | run `hw1 tuple holds list` |
| `items[3].widget.options[0].why` | The tuple still holds the same two objects. It is the list inside it that changed, and lists may change. | correct | as the row above |
| `items[3].widget.options[1].text` | KEY: It prints `('VOD', [72.5, 73.1])` | correct | as the row above |
| `items[3].widget.options[2].why` | `append` changed the list in place, and the tuple holds that very list. | correct | as the row above |
| `items[3].widget.options[3].why` | `append` added to the list, not to the tuple. | correct | as the row above |
| `items[3].feedback.correct` | The tuple is fixed, but the list it holds is not. | correct | as the row above |
| `items[3].feedback.generic` | Not quite right. Ask what `pos[1]` is, and whether that kind of object can change. | correct | as the row above |
| `items[3].explain.text` | A tuple fixes which objects it holds, not what happens inside them. `pos[1]` is a list, and `append` change... | correct | as the row above |
| `items[4].prose` | A $k$-day return compares each close with the close $k$ days later: $\dfrac{p_{t+k} - p_t}{p_t}$. With $n$ ... | correct | run `hw1 k-day`; harness: solution passes 6 tests |
| `items[4].widget.how` | Check runs 6 hidden tests that call your function. Numbers are accepted within `math.isclose` of the expect... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[4].feedback.correct` | `zip(closes, closes[k:])` pairs each close with the one $k$ days on. | correct | run `hw1 k-day`; harness: solution passes 6 tests |
| `items[4].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `items[4].feedback.byKey.test-1` | Test 1 expects 0.05, from 100.0 to 105.0 two days later. 0.02 means you paired neighbours: shift by `k`, no... | correct | as the row above |
| `items[4].feedback.byKey.test-5` | Test 5 has fewer closes than `k` and expects `[]`. An `IndexError` means you indexed past the end; `zip` wi... | correct | as the row above |
| `items[4].explain.text` | `closes[k:]` is the list shifted by `k`, and `zip` stops when it runs out, so there are exactly `n - k` pai... | correct | as the row above |
| `items[5].prose` | A file of closes has been read into one string. The first line is a header, and the text may end with blank... | correct | harness: solution passes 4 tests (CRLF, blank tail); returns +4%, -0.96%, +1.94%, -4% |
| `items[5].widget.how` | Check runs 4 hidden tests that call your function. Each answer must equal the expected value exactly (`==`). | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[5].feedback.correct` | Parse, pair, compute, then compare with a key. | correct | harness: solution passes 4 tests (CRLF, blank tail); returns +4%, -0.96%, +1.94%, -4% |
| `items[5].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `items[5].feedback.byKey.test-1` | Test 1 expects `('2026-10-13', '2026-10-16')`. `'2026-10-15'` as best means you compared closes, not return... | correct | as the row above |
| `items[5].feedback.byKey.test-2` | Test 2 ends with a blank line. A `ValueError` from unpacking means an empty line reached `split(",")`: stri... | correct | as the row above |
| `items[5].feedback.byKey.error` | Your code stopped before the tests ran. Read the error under the editor: it names the line to fix. | correct | as the row above |
| `items[5].explain.text` | Strip and split the text into lines, skip the header with `[1:]`, and unpack each line into a `(date, close... | correct | as the row above |
| `items[6].prose` | [code] | correct | run `hw1 stable sort`; sort stability is guaranteed (docs, Sorting HOW TO) |
| `items[6].widget.options[0].text` | KEY: `['AZN', 'BP', 'VOD']` | correct | as the row above |
| `items[6].widget.options[1].why` | You expected the tied quotes to swap. Python's sort is stable: items with equal keys keep their original or... | correct | as the row above |
| `items[6].widget.options[2].why` | Python guarantees the order: a stable sort keeps tied items as they were. | correct | as the row above |
| `items[6].widget.options[3].why` | `sorted` puts the smallest key first, and AZN's 1.20 is smallest. | correct | as the row above |
| `items[6].feedback.correct` | AZN first; BP and VOD tie and keep their order. | correct | as the row above |
| `items[6].feedback.generic` | Not quite right. Sort by price, and keep ties in their original order. | correct | as the row above |
| `items[6].explain.text` | The key gives 4.85, 4.85 and 1.20, so AZN comes first. BP and VOD tie, and a stable sort keeps them in thei... | correct | as the row above |
| `items[7].prompt` | A colleague's end-of-day check flags a mismatch on a day with two fills, £0.10 and £0.20, and an expected t... | correct | run `hw1 mismatch message`, `hw1 isclose abs_tol`, `l1 0.29*100` |
| `items[7].model` | **What happens.** Floats are stored in binary. 0.10 and 0.20 have no exact binary form, so each is stored a... | correct | as the row above |
| `items[7].rubric[0].text` | Explains that 0.10 and 0.20 are stored as nearest binary values, so the sum is 0.30000000000000004 and `==`... | correct | as the row above |
| `items[7].rubric[1].text` | Explains that `:.2f` rounds only the display, so the message shows 0.30 twice | correct | as the row above |
| `items[7].rubric[2].text` | Gives a correct tolerance fix in code, with a sensible tolerance such as half a penny | correct | as the row above |
| `items[7].rubric[3].text` | Gives a correct whole-pence fix in code, converting with `round`, not `int` | correct | as the row above |
| `items[7].rubric[4].text` | Chooses whole pence for a ledger, with the reason: integers add exactly, so drift cannot build up | correct | as the row above |
| `items[7].rubric[5].text` | Names the zero case for `math.isclose` and the `abs_tol` remedy | correct | as the row above |
| `items[8].prose` | [code] `trades` holds `(ticker, price, qty)` tuples. | correct | run `hw1 if before for needs else` |
| `items[8].widget.options[0].text` | KEY: `[t for t, p, q in trades if p * q > 1000]` | correct | as the row above |
| `items[8].widget.options[1].why` | An `if` before the `for` is a choice between two values and needs an `else`. A filter goes at the end. | correct | as the row above |
| `items[8].widget.options[2].why` | Each item is a whole tuple, so `p` and `q` are never defined. Unpack all three fields. | correct | as the row above |
| `items[8].widget.options[3].why` | That collects whole records. The loop appends only the ticker, `t`. | correct | as the row above |
| `items[8].feedback.correct` | Same unpacking, same filter, same item collected. | correct | as the row above |
| `items[8].feedback.generic` | Not quite right. Match each part of the loop: what is unpacked, the filter, and what is appended. | correct | as the row above |
| `items[8].explain.text` | The comprehension reads like the loop without `append`: collect `t`, for each unpacked `t, p, q`, if `p * q... | correct | as the row above |
| `items[9].prose` | Each day is a `(date, open, close)` tuple, oldest first. A day's **overnight gap** compares its open with t... | correct | run `hw1 gaps`; harness: solution passes 10 tests |
| `items[9].widget.how` | Check runs 10 hidden tests that call your function. Numbers are accepted within `math.isclose` of the expec... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[9].feedback.correct` | Each gap pairs a day's open with the close before it, and the flags keep moves either way. | correct | run `hw1 gaps`; harness: solution passes 10 tests |
| `items[9].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `items[9].feedback.byKey.test-2` | Test 2 expects 0.02 first: Tuesday opened at 103.02 after Monday closed at 101.0. Divide by the previous cl... | correct | as the row above |
| `items[9].feedback.byKey.test-3` | Test 3 expects Tuesday and Friday. Friday fell about 2%, so compare `abs(gap)`; and flag the day that opene... | correct | as the row above |
| `items[9].feedback.byKey.test-4` | Test 4 expects 4 gaps from 5 days. Index -1 is the last day, so a loop from index 0 adds a gap for Monday. | correct | as the row above |
| `items[9].feedback.byKey.test-5` | Test 5 uses a limit of 0. Thursday opened at its previous close, a gap of 0, which is not more than 0. | correct | as the row above |
| `items[9].feedback.byKey.test-9` | Test 9 passes no days at all and expects two empty lists. `zip` with a slice handles it without an `if`. | correct | as the row above |
| `items[9].feedback.byKey.test-10` | Test 10 reads your code for `.append(`. Build both lists with comprehensions, as the question asks. | correct | as the row above |
| `items[9].explain.text` | `zip(days, days[1:])` gives one `(before, today)` pair per gap, and none for a single day. `abs` makes a fa... | correct | as the row above |

## l5-lookup-by-name.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Curly brackets pair each ticker with its closing price in £. Square brackets then ask for one of them. [code] | correct | dict lookup by key (docs, Mapping Types) |
| `screens[0].hints[0].text` | Find the row whose ticker matches the text inside the square brackets. | correct | as the row above |
| `screens[0].hints[1].text` | "BP" is the name being asked for. | correct | as the row above |
| `screens[0].hints[2].text` | The price paired with "BP" is 4.85. | correct | as the row above |
| `screens[0].feedback.correct` | `prices["BP"]` finds the name "BP" and hands back its price, 4.85. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Find "BP" on the left, then take what is paired with it. | correct | as the row above |
| `screens[0].feedback.byKey.r1c0` | You tapped the ticker itself. `prices["BP"]` hands back what is stored under "BP", its price. | correct | as the row above |
| `screens[0].feedback.byKey.r0c1` | That is the first price. Nothing here is looked up by position: the name in the brackets picks the row. | correct | as the row above |
| `screens[0].feedback.byKey.r2c1` | That is HSBA's price. The brackets ask for "BP". | correct | as the row above |
| `screens[0].explain.text` | Each pair is a **key** and a **value**: the ticker is the key, the price is its value. `prices["BP"]` finds... | correct | as the row above |
| `screens[1].prose` | Square brackets can also store a value under a key. A position book records the shares held in each stock. ... | correct | assignment to an existing key replaces the value; final book {'BP': 500, 'VOD': 1000} |
| `screens[1].hints[0].text` | Two lines store under "BP". What happens to the first value when the second arrives? | correct | as the row above |
| `screens[1].hints[1].text` | 300 and 500 are both stored under "BP", in that order. | correct | as the row above |
| `screens[1].hints[2].text` | 500 replaces 300 under "BP", so 300 is overwritten. 1000 stays under "VOD". | correct | as the row above |
| `screens[1].feedback.correct` | A key holds one value, so the second store under "BP" replaced the first. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Follow the lines in order; a store under an existing key replaces its value. | correct | as the row above |
| `screens[1].feedback.byKey.v300` | You kept 300 under "BP". The last line stores 500 under the same key, and that replaces 300. | correct | as the row above |
| `screens[1].feedback.byKey.v500` | 500 is stored under "BP" by the last line, and nothing replaces it. | correct | as the row above |
| `screens[1].feedback.byKey.v1000` | 1000 is stored under "VOD" and no later line touches "VOD". | correct | as the row above |
| `screens[1].explain.text` | Storing under a key that already exists replaces its value, so 300 is gone. Each key holds exactly one valu... | correct | as the row above |
| `screens[2].prose` | You have been using a **dictionary**: a collection of key–value pairs. `d[key]` reads a value and `d[key] =... | correct | run `l5 position values`; harness: solution passes 6 tests |
| `screens[2].widget.how` | Check runs 6 hidden tests, one of them a short position (negative shares). Values are compared with `math.i... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[2].hints[0].text` | Two lookups with the same key, then multiply. | correct | run `l5 position values`; harness: solution passes 6 tests |
| `screens[2].hints[1].text` | `book[ticker]` is the number of shares; `prices[ticker]` is the price of one. | correct | as the row above |
| `screens[2].hints[2].text` | Return `book[ticker] * prices[ticker]`. Use the variable `ticker`, without quotes. | correct | as the row above |
| `screens[2].feedback.correct` | All six tests passed, the short position included. | correct | as the row above |
| `screens[2].feedback.generic` | Some tests failed. Multiply the shares held by the price, both looked up with `ticker`. | correct | as the row above |
| `screens[2].feedback.byKey.test-1` | Test 1 failed. If it is a `KeyError: 'ticker'`, you wrote `"ticker"` in quotes: that looks up the literal w... | correct | as the row above |
| `screens[2].explain.text` | Both dictionaries are keyed by ticker, so the same key reads both numbers. A short of 200 BP at £4.85 is wo... | correct | as the row above |
| `screens[3].prose` | `.items()` hands back each key with its value, ready to unpack in a loop. [code] | correct | run `l5 insertion order`; dicts keep insertion order, updating a key keeps its place (docs, dict, since 3.7) |
| `screens[3].widget.options[0].text` | KEY: `VOD 0.74`, then `BP 4.85`, then `AZN 118.5` | correct | as the row above |
| `screens[3].widget.options[1].why` | You sorted the keys alphabetically. A dictionary keeps keys in the order they were first added. | correct | as the row above |
| `screens[3].widget.options[2].why` | You moved VOD to the end when its price changed. Replacing a value keeps the key where it was. | correct | as the row above |
| `screens[3].widget.options[3].why` | You printed VOD's first price. The line before the loop replaced 0.72 with 0.74. | correct | as the row above |
| `screens[3].hints[0].text` | Does a dictionary sort its keys, or remember when each one arrived? | correct | as the row above |
| `screens[3].hints[1].text` | VOD arrived first. Does changing its price move it? | correct | as the row above |
| `screens[3].hints[2].text` | Keys come out in the order they were first added: VOD, BP, AZN. VOD now holds 0.74. | correct | as the row above |
| `screens[3].feedback.correct` | Insertion order, with VOD's new price in VOD's old place. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Keys come out in the order they were first added, and a replaced value keeps its place. | correct | as the row above |
| `screens[3].feedback.byKey.sorted` | You sorted the keys. Dictionaries are not sorted: they remember the order keys were first added, VOD then B... | correct | as the row above |
| `screens[3].explain.text` | A dictionary remembers the order its keys were first added. Storing a new value under an old key keeps its ... | correct | as the row above |
| `screens[4].prose` | A value can be any object, a list included. Here each ticker maps to its last three closes. [code] | correct | len of a dict counts keys; history['VOD'][-1] is 0.74 |
| `screens[4].widget.options[0].text` | KEY: `2 0.74` | correct | as the row above |
| `screens[4].widget.options[1].why` | You counted every price. `len` of a dictionary counts its keys, and there are two. | correct | as the row above |
| `screens[4].widget.options[2].why` | You took the last close of BP's list. `history["VOD"]` picks VOD's list, then `[-1]` takes its last close. | correct | as the row above |
| `screens[4].widget.options[3].why` | You stopped after the key lookup. The `[-1]` then indexes into VOD's list. | correct | as the row above |
| `screens[4].hints[0].text` | Read `history["VOD"][-1]` left to right: what does each pair of brackets hand back? | correct | as the row above |
| `screens[4].hints[1].text` | `history["VOD"]` is this whole list. | correct | as the row above |
| `screens[4].hints[2].text` | There are 2 keys. VOD's list is [0.72, 0.71, 0.74], and its last value is 0.74. | correct | as the row above |
| `screens[4].feedback.correct` | Two keys, and the last of VOD's closes. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. `len` counts keys; the first brackets pick a list and the second index into it. | correct | as the row above |
| `screens[4].explain.text` | `history["VOD"]` hands back a list, and `[-1]` indexes that list. `len(history)` counts keys, 2. Ticker to ... | correct | as the row above |
| `screens[5].prose` | Someone asks for the price of Tesco, ticker TSCO. [code] | correct | run `l5 KeyError text`, `l5 get` |
| `screens[5].widget.options[0].text` | KEY: It stops with a `KeyError` | correct | as the row above |
| `screens[5].widget.options[1].why` | You expected a blank for a missing key. Square brackets never invent a value: a missing key is an error. | correct | as the row above |
| `screens[5].widget.options[2].why` | You expected a missing ticker to count as zero. Python cannot know what a missing price should be, so it st... | correct | as the row above |
| `screens[5].widget.options[3].why` | You expected it to fall back to the last entry. A lookup matches the key exactly or fails. | correct | as the row above |
| `screens[5].hints[0].text` | Is "TSCO" one of the keys? | correct | as the row above |
| `screens[5].hints[1].text` | These are all the keys there are. | correct | as the row above |
| `screens[5].hints[2].text` | "TSCO" is not a key, so `prices["TSCO"]` has nothing to hand back. Python raises an error rather than guess. | correct | as the row above |
| `screens[5].feedback.correct` | A missing key stops the program with `KeyError`. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Check whether "TSCO" is a key, and what `[]` does when it is not. | correct | as the row above |
| `screens[5].feedback.byKey.none` | You expected `None` for a missing key. `[]` raises `KeyError` instead; `get` is the method that returns `No... | correct | as the row above |
| `screens[5].feedback.byKey.zero` | You treated a missing ticker as zero. That would value an unknown stock at £0, so Python refuses and raises... | correct | as the row above |
| `screens[5].explain.text` | `[]` promises a value, so a missing key stops the program with `KeyError: 'TSCO'`. When a missing key is ex... | correct | as the row above |
| `screens[6].prose` | A broker's flat fee per trade, by venue. [code] | correct | run `l5 get` (get never inserts) |
| `screens[6].widget.options[0].text` | KEY: `0.8 2.0 None` | correct | as the row above |
| `screens[6].widget.options[1].why` | You used the default for TQ too. The default is used only when the key is missing, and TQ is there. | correct | as the row above |
| `screens[6].widget.options[2].why` | You carried the default into the third call. With no default, `get` returns `None`. | correct | as the row above |
| `screens[6].widget.options[3].why` | `get` never raises `KeyError`. A missing key gives the default, or `None` without one. | correct | as the row above |
| `screens[6].hints[0].text` | Which of the two venues asked for is a key? | correct | as the row above |
| `screens[6].hints[1].text` | TQ is a key; CBOE is not. | correct | as the row above |
| `screens[6].hints[2].text` | TQ gives its own 0.8. CBOE gives the default 2.0, then `None` when no default is given. | correct | as the row above |
| `screens[6].feedback.correct` | The stored value when the key is there; the default, or `None`, when it is not. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. `get` uses the default only for a missing key. | correct | as the row above |
| `screens[6].explain.text` | `fees.get(k, default)` returns `fees[k]` when `k` is a key, else the default. Without a default it returns ... | correct | as the row above |
| `screens[7].prose` | Price history arrives as a dictionary of lists. Some tickers are missing, and a newly listed one can have a... | correct | run `l5 empty [-1]`; harness: solution passes 6 tests |
| `screens[7].widget.how` | Check runs 6 hidden tests, including a missing ticker, an empty list and an empty dictionary. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[7].hints[0].text` | Two things can be missing: the ticker, and the prices in its list. | correct | run `l5 empty [-1]`; harness: solution passes 6 tests |
| `screens[7].hints[1].text` | `history.get(ticker, [])` turns a missing ticker into an empty list, so one length check covers both. | correct | as the row above |
| `screens[7].hints[2].text` | Set `closes = history.get(ticker, [])` and `last = None`. If `len(closes) > 0`, set `last = closes[-1]`. Re... | correct | as the row above |
| `screens[7].feedback.correct` | All six tests passed: missing tickers and empty lists both give `None`. | correct | as the row above |
| `screens[7].feedback.generic` | Some tests failed. Try a missing ticker and an empty list by hand. | correct | as the row above |
| `screens[7].feedback.byKey.test-2` | Test 2 asks for a ticker that is not in `history`. `history[ticker]` raises `KeyError` there; use `history.... | correct | as the row above |
| `screens[7].feedback.byKey.test-3` | Test 3 has an empty list. `[-1]` on an empty list raises `IndexError`, so check the length first. | correct | as the row above |
| `screens[7].explain.text` | The empty-list default folds a missing ticker into the empty-list case. Then one length check guards `close... | correct | as the row above |
| `screens[8].prose` | A dictionary maps each key to one value, $k \mapsto v$. Everything you used: [code] | correct | one value per key; len counts keys |
| `screens[8].widget.answer` | KEY: 1 | correct | as the row above |
| `screens[8].widget.accept` | 1: the second line replaces BP's value; it adds no key. | correct | as the row above |
| `screens[8].widget.wrong[0].value` | SLIP value: 2 | correct | as the row above |
| `screens[8].feedback.correct` | One key, now holding 4.90. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Count keys, not stores. | correct | as the row above |
| `screens[8].feedback.byKey.two` | You counted two stores as two entries. Storing under an existing key replaces its value, so there is still ... | correct | as the row above |
| `screens[8].explain.text` | Each key holds one value, so storing under "BP" again replaces 4.85 with 4.90. `len` counts keys: still 1. | correct | as the row above |
| `screens[9].prose` | A broker charges a fee rate by venue, as a fraction of the trade's notional (its £ size). Venues not on the... | correct | run `l5 fees`; keys match exactly ('lse' != 'LSE') |
| `screens[9].widget.how` | Check runs 7 hidden tests, some on venues that are not on the schedule. Fees are compared with `math.isclose`. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[9].hints[0].text` | This is a lookup with a default. | correct | run `l5 fees`; keys match exactly ('lse' != 'LSE') |
| `screens[9].hints[1].text` | `FEES.get(venue, STANDARD)` is the rate for any venue, listed or not. | correct | as the row above |
| `screens[9].hints[2].text` | Return `notional * FEES.get(venue, STANDARD)`. | correct | as the row above |
| `screens[9].feedback.correct` | All seven tests passed, unknown venues included. | correct | as the row above |
| `screens[9].feedback.generic` | Some tests failed. Look the rate up with `get`, using `STANDARD` as the default, then multiply by the notio... | correct | as the row above |
| `screens[9].feedback.byKey.test-4` | Test 4 uses AQX, which is not on the schedule. `FEES[venue]` raises `KeyError` there, and `FEES.get(venue)`... | correct | as the row above |
| `screens[9].feedback.byKey.test-7` | Test 7 passes "lse" and expects the standard 1.5. Keys match exactly here, so look up `venue` as given. | correct | as the row above |
| `screens[9].explain.text` | `get` with `STANDARD` as the default is the whole schedule in one line. Keys match exactly, so "lse" is not... | correct | as the row above |
| `summary.ideas[0]` | A dictionary maps keys to values: `d[k]` reads, `d[k] = v` stores or replaces, and each key holds one value. | correct | restates s0 to s6 |
| `summary.ideas[1]` | `d[k]` raises `KeyError` for a missing key; `d.get(k, default)` returns the default instead, or `None` with... | correct | as the row above |
| `summary.ideas[2]` | Keys keep the order they were first added, not sorted order. A value can be any object, such as a list of c... | correct | as the row above |
| `summary.formula.tex` | \texttt{d.get(k, dflt)} = \begin{cases} \texttt{d[k]} & \text{if } k \text{ is a key} \\ \texttt{dflt} & \t... | correct | as the row above |
| `summary.formula.note` | Without a default, `get` returns `None` for a missing key; `d[k]` raises `KeyError`. | correct | as the row above |
| `summary.trap` | `prices["TSCO"]` for a missing key raises `KeyError`. It does not return `None` or 0. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | 300 + 200 = 500; AZN is a third key |
| `quiz[0].widget.options[0].text` | KEY: `3 500` | correct | as the row above |
| `quiz[0].widget.options[1].why` | You treated the new key like a replacement. "AZN" is not in the book yet, so the book grows to 3. | correct | as the row above |
| `quiz[0].widget.options[2].why` | You counted the update to BP as a new entry. BP's value changes; its key is still one key. | correct | as the row above |
| `quiz[0].widget.options[3].why` | You stored 200. The line reads the old 300, adds 200, and stores 500. | correct | as the row above |
| `quiz[0].feedback.correct` | Three keys, and BP now holds 500. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. A new key adds an entry; an existing key is updated. | correct | as the row above |
| `quiz[0].explain.text` | The right side reads 300 first, so BP becomes 500. "AZN" is a new key, so `len(book)` goes from 2 to 3. | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l5 q list(d)` |
| `quiz[1].widget.options[0].text` | KEY: `['b', 'a']` | correct | as the row above |
| `quiz[1].widget.options[1].why` | You sorted the keys. A dictionary keeps the order the keys were written in. | correct | as the row above |
| `quiz[1].widget.options[2].why` | You listed the values. A dictionary used as a list gives its keys. | correct | as the row above |
| `quiz[1].widget.options[3].why` | Those are the pairs, which `d.items()` gives. `list(d)` gives keys only. | correct | as the row above |
| `quiz[1].feedback.correct` | Keys, in the order they were added. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Turning a dictionary into a list gives its keys, in insertion order. | correct | as the row above |
| `quiz[1].explain.text` | Looping over a dictionary, or calling `list` on it, gives its keys. They come in insertion order: "b" was w... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | run `l5 q total 5.8` (slips 3.8 and 4.3) |
| `quiz[2].widget.answer` | KEY: 5.8 | correct | as the row above |
| `quiz[2].widget.accept` | 5.8: 1.50 + 0.80 + 2.00 + 1.50. | correct | as the row above |
| `quiz[2].widget.wrong[0].value` | SLIP value: 3.8 | correct | as the row above |
| `quiz[2].widget.wrong[1].value` | SLIP value: 4.3 | correct | as the row above |
| `quiz[2].feedback.correct` | 1.50 + 0.80 + 2.00 + 1.50 = 5.80. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. Add one fee per venue in the list, using 2.00 for any venue not in `fees`. | correct | as the row above |
| `quiz[2].feedback.byKey.skip` | You skipped AQX. It is not a key, so `get` adds the default 2.00 for it. | correct | as the row above |
| `quiz[2].feedback.byKey.once` | You charged LSE once. It appears twice in the list, so its fee is added twice. | correct | as the row above |
| `quiz[2].explain.text` | The loop adds one fee per trade: 1.50 for LSE, 0.80 for TQ, the default 2.00 for AQX and 1.50 for LSE again... | correct | as the row above |
| `quiz[3].prose` | A price feed has a key for BP but no price yet. [code] | correct | run `l5 q stored None` |
| `quiz[3].widget.options[0].text` | KEY: `None` | correct | as the row above |
| `quiz[3].widget.options[1].why` | You treated a stored `None` as a missing key. The key exists, so `get` returns its value, which is `None`. | correct | as the row above |
| `quiz[3].widget.options[2].why` | `get` never raises `KeyError`, and "BP" is a key anyway. | correct | as the row above |
| `quiz[3].widget.options[3].why` | `get` returns the value stored under the key, not the key. | correct | as the row above |
| `quiz[3].feedback.correct` | The key is there, so its value comes back, even though that value is `None`. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. The default is used only when the key is missing. | correct | as the row above |
| `quiz[3].explain.text` | `get` asks one question: is the key there? "BP" is, so its stored value comes back, and here that value is ... | correct | as the row above |
| `screens[0].widget.answer` | KEY: ["r1c1"] | correct | dict lookup by key (docs, Mapping Types) |
| `screens[1].widget.answer` | KEY: {"bp": ["v500"], "vod": ["v1000"], "gone": ["v300"]} | correct | assignment to an existing key replaces the value; final book {'BP': 500, 'VOD': 1000} |

## l6-membership.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Today's blotter lists the ticker of every trade, in the order they happened. [code] | correct | first appearances at indices 0, 1, 3 by inspection |
| `screens[0].hints[0].text` | Walk left to right. Tap a ticker only if you have not seen it before. | correct | as the row above |
| `screens[0].hints[1].text` | This BP has already appeared once. | correct | as the row above |
| `screens[0].hints[2].text` | BP first appears at position 0, VOD at 1 and AZN at 3. Everything after is a repeat. | correct | as the row above |
| `screens[0].feedback.correct` | Three different tickers: BP, VOD and AZN. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Tap each ticker once, the first time it appears. | correct | as the row above |
| `screens[0].feedback.byKey.c2` | BP already appeared at position 0. Tap only the first time each ticker shows up. | correct | as the row above |
| `screens[0].feedback.byKey.c4` | VOD already appeared at position 1. This one is a repeat. | correct | as the row above |
| `screens[0].feedback.byKey.c5` | BP already appeared at position 0. This one is a repeat. | correct | as the row above |
| `screens[0].explain.text` | You kept a memory of the tickers already seen and skipped repeats. That gave three different tickers, in th... | correct | as the row above |
| `screens[1].prose` | To count trades per ticker, drop each trade into the box for its ticker. The box sizes are the counts. | correct | counts BP 3, VOD 2, AZN 1 by inspection |
| `screens[1].hints[0].text` | Read the ticker on each card and match it to a box label. | correct | as the row above |
| `screens[1].hints[1].text` | These three cards all say BP. | correct | as the row above |
| `screens[1].hints[2].text` | Three BP cards, two VOD cards and one AZN card. | correct | as the row above |
| `screens[1].feedback.correct` | BP 3, VOD 2, AZN 1. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Every card goes in the box with the same ticker. | correct | as the row above |
| `screens[1].feedback.byKey.t0` | That card says BP; it belongs in the BP box. | correct | as the row above |
| `screens[1].feedback.byKey.t2` | That card says BP; it belongs in the BP box. | correct | as the row above |
| `screens[1].feedback.byKey.t5` | That card says BP; it belongs in the BP box. | correct | as the row above |
| `screens[1].feedback.byKey.t1` | That card says VOD; it belongs in the VOD box. | correct | as the row above |
| `screens[1].feedback.byKey.t4` | That card says VOD; it belongs in the VOD box. | correct | as the row above |
| `screens[1].feedback.byKey.t3` | That card says AZN; it belongs in the AZN box. | correct | as the row above |
| `screens[1].explain.text` | Box sizes are the counts: BP 3, VOD 2, AZN 1. In code the boxes are a dictionary from ticker to count, `{"B... | correct | as the row above |
| `screens[2].prose` | The memory you kept on the first screen is a **set**: a collection holding each value at most once. `set(tr... | correct | run `l6 set` (set is unordered and not subscriptable) |
| `screens[2].widget.options[0].text` | KEY: `3 False True` | correct | as the row above |
| `screens[2].widget.options[1].why` | You counted the list. The set keeps each ticker once, so it holds 3. | correct | as the row above |
| `screens[2].widget.options[2].why` | You read `in` as a count. It answers yes or no: `True` or `False`. | correct | as the row above |
| `screens[2].widget.options[3].why` | TSCO was never traded, so it is not in the set. | correct | as the row above |
| `screens[2].hints[0].text` | How many different tickers did you tap on the first screen? | correct | as the row above |
| `screens[2].hints[1].text` | These are the only values the set keeps. | correct | as the row above |
| `screens[2].hints[2].text` | The set holds BP, VOD and AZN: length 3. TSCO is not there; BP is. | correct | as the row above |
| `screens[2].feedback.correct` | Three values in the set; TSCO is not one of them, BP is. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. A set keeps each value once, and `in` gives `True` or `False`. | correct | as the row above |
| `screens[2].explain.text` | `set(trades)` keeps BP, VOD and AZN once each, so `len` is 3. `in` returns `True` or `False`. A set has no ... | correct | as the row above |
| `screens[3].prose` | Now the boxes in code. Start with an empty dictionary. For each ticker, add 1 to its count; a ticker seen f... | correct | harness: solution passes 6 tests; counts[t] before get raises KeyError |
| `screens[3].widget.how` | Check runs 6 hidden tests, including an empty list. Dictionaries are compared with `==`; one test also chec... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[3].hints[0].text` | One line inside a `for` loop does it: read the old count, add 1, store it back. | correct | harness: solution passes 6 tests; counts[t] before get raises KeyError |
| `screens[3].hints[1].text` | `counts.get(t, 0)` is the count so far, and 0 the first time. Each BP card adds 1. | correct | as the row above |
| `screens[3].hints[2].text` | Loop `for t in trades:` and inside write `counts[t] = counts.get(t, 0) + 1`. | correct | as the row above |
| `screens[3].feedback.correct` | All six tests passed, the empty list included. | correct | as the row above |
| `screens[3].feedback.generic` | Some tests failed. Read the old count with a default of 0, add 1, and store it back. | correct | as the row above |
| `screens[3].feedback.byKey.test-1` | Test 1 failed. If it is a `KeyError`, `counts[t]` ran before `t` had a count: read it with `counts.get(t, 0... | correct | as the row above |
| `screens[3].explain.text` | `get` with a default of 0 covers a ticker's first appearance, so one line does the counting. An `if t in co... | correct | as the row above |
| `screens[4].prose` | A risk check refuses orders in 5,000 restricted tickers. The same tickers can be kept as a list or as a set... | correct | run `l6 list miss costs n comparisons` (5,000 __eq__ calls), `l6 set miss about one`, `l6 list hit averages about half` (2,000 random hits), `l6 million orders`; CPython set is a hash table |
| `screens[4].widget.options[0].text` | KEY: List: 5,000. Set: about 1. | correct | as the row above |
| `screens[4].widget.options[1].why` | You assumed a list can jump to the answer. It has no index by value, so it checks every item before saying no. | correct | as the row above |
| `screens[4].widget.options[2].why` | You assumed a set searches too. A set computes where the value would be stored and looks only there. | correct | as the row above |
| `screens[4].widget.options[3].why` | Half the list is the average when the ticker is there. A missing ticker must be checked against every item. | correct | as the row above |
| `screens[4].hints[0].text` | To be sure ZZZ is not in a list, which items must you look at? | correct | as the row above |
| `screens[4].hints[1].text` | A set stores each value at a place worked out from the value itself. | correct | as the row above |
| `screens[4].hints[2].text` | The list compares ZZZ with all 5,000 items. The set looks in the one place ZZZ would be. | correct | as the row above |
| `screens[4].feedback.correct` | A list checks item after item; a set looks in one place. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. A missing value forces a list to check every item; a set looks where the value would be. | correct | as the row above |
| `screens[4].explain.text` | A list answers `in` by comparing item after item, so a miss costs 5,000 comparisons. A set **hashes** the v... | correct | as the row above |
| `screens[5].prose` | `set(trades)` forgets the order trades arrived. Write `first_seen`, which keeps each ticker once, in first-... | correct | harness: solution passes 6 tests; list(set(...)) loses arrival order |
| `screens[5].widget.how` | Check runs 6 hidden tests. Order matters, and the list you are given must not change. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[5].hints[0].text` | Loop over the trades. For each one, ask whether you have seen it. | correct | harness: solution passes 6 tests; list(set(...)) loses arrival order |
| `screens[5].hints[1].text` | Only when `t not in seen`: add it to `seen` and append it to `result`. | correct | as the row above |
| `screens[5].hints[2].text` | `for t in trades:`, then `if t not in seen:` with `seen.add(t)` and `result.append(t)` inside. | correct | as the row above |
| `screens[5].feedback.correct` | All six tests passed: one of each, in first-seen order. | correct | as the row above |
| `screens[5].feedback.generic` | Some tests failed. Append a ticker only when it is not yet in `seen`, and add it to `seen` as you do. | correct | as the row above |
| `screens[5].feedback.byKey.test-1` | Test 1 failed. If you returned `list(set(trades))`, the order is lost: a set does not remember arrival orde... | correct | as the row above |
| `screens[5].explain.text` | The set answers "seen it?" in about one step; the list keeps the order. Each does the job it is good at. [c... | correct | as the row above |
| `screens[6].prose` | A position book from the last lesson. Is 300 in it? [code] | correct | run `l6 in keys` |
| `screens[6].widget.options[0].text` | KEY: `False True` | correct | as the row above |
| `screens[6].widget.options[1].why` | You searched the values. `in` on a dictionary checks keys only, and 300 is a value. | correct | as the row above |
| `screens[6].widget.options[2].why` | You searched the values and treated a holding of 0 as absent. `in` checks keys, and "AZN" is a key whatever... | correct | as the row above |
| `screens[6].widget.options[3].why` | You treated AZN's 0 shares as no entry. The key is there, so `in` says `True`. | correct | as the row above |
| `screens[6].hints[0].text` | When you loop over a dictionary you get its keys. What does `in` look through? | correct | as the row above |
| `screens[6].hints[1].text` | `in` looks only down this column. | correct | as the row above |
| `screens[6].hints[2].text` | 300 is not a key, so `False`. "AZN" is a key, even with 0 shares, so `True`. | correct | as the row above |
| `screens[6].feedback.correct` | `in` looks at keys only, and a key holding 0 is still a key. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. `in` on a dictionary checks its keys, never its values. | correct | as the row above |
| `screens[6].feedback.byKey.values` | You searched the values. `300 in book` checks keys only, so it is `False`; `300 in book.values()` would be ... | correct | as the row above |
| `screens[6].feedback.byKey.zero` | You searched the values and treated a 0 as missing. Both are mistakes: `in` checks keys, and "AZN" is one. | correct | as the row above |
| `screens[6].explain.text` | `in` on a dictionary asks about keys, so `300 in book` is `False`. A key holding 0 is still a key, so `"AZN... | correct | as the row above |
| `screens[7].prose` | For a list of $n$ items, `x in items` makes up to $n$ comparisons; `x in seen` makes about $1$ on average. ... | correct | run `l6 {} is dict`; average O(1) membership for sets (Python wiki TimeComplexity) |
| `screens[7].widget.options[0].text` | KEY: `set()` | correct | as the row above |
| `screens[7].widget.options[1].why` | You wrote empty braces. `{}` is an empty dictionary; dictionaries had the braces first. | correct | as the row above |
| `screens[7].widget.options[2].why` | That is an empty list, which keeps repeats and order. | correct | as the row above |
| `screens[7].widget.options[3].why` | That is an empty tuple, which cannot change at all. | correct | as the row above |
| `screens[7].feedback.correct` | `set()` is the only way to write an empty set. | imprecise | Finding 2. `{*()}` and `set([])` also evaluate to an empty set; run `l6 other spellings of an empty set exist` |
| `screens[7].feedback.generic` | Not quite right. Empty braces already mean something else. | correct | run `l6 {} is dict`; average O(1) membership for sets (Python wiki TimeComplexity) |
| `screens[7].explain.text` | `{"BP", "VOD"}` is a set, but `{}` alone is an empty dictionary. So an empty set is written `set()`. | correct | as the row above |
| `screens[8].prose` | Each trade is a `(ticker, quantity)` pair: positive for a buy, negative for a sell. Net them into a positio... | correct | harness: solution passes 7 tests; run `l6 del in loop RuntimeError` (both key positions) |
| `screens[8].widget.how` | Check runs 7 hidden tests, including books that go flat and an empty list of trades. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[8].hints[0].text` | This is counting, but adding `qty` instead of 1. Then drop the zeros. | correct | harness: solution passes 7 tests; run `l6 del in loop RuntimeError` (both key positions) |
| `screens[8].hints[1].text` | Inside the loop: `book[ticker] = book.get(ticker, 0) + qty`. | correct | as the row above |
| `screens[8].hints[2].text` | After the loop, build `result = {}` and copy across every `ticker, qty` in `book.items()` with `qty != 0`. ... | correct | as the row above |
| `screens[8].feedback.correct` | All seven tests passed: trades netted, flat tickers dropped. | correct | as the row above |
| `screens[8].feedback.generic` | Some tests failed. Add each quantity to a running total per ticker, then keep only the non-zero totals. | correct | as the row above |
| `screens[8].feedback.byKey.test-1` | Test 1 trades BP twice. Add each quantity to the running total with `book.get(ticker, 0) + qty`, rather tha... | correct | as the row above |
| `screens[8].feedback.byKey.test-2` | Test 2 nets BP to 0, and a flat ticker must be left out. If you deleted keys inside `for t in book`, Python... | correct | as the row above |
| `screens[8].explain.text` | The first loop is the counting idiom with `qty` in place of 1. The second builds a fresh dictionary of open... | correct | run `l6 del in loop RuntimeError`: CPython raises on the next iteration step whichever key was deleted, last key included |
| `summary.ideas[0]` | A set holds each value once: `set(xs)` drops repeats, and `x in s` takes about one step on average, however... | correct | restates s2 to s7 |
| `summary.ideas[1]` | Count or net into a dictionary with `d[k] = d.get(k, 0) + amount`; the default covers a key's first appeara... | correct | as the row above |
| `summary.ideas[2]` | `in` on a dictionary checks keys, never values. `{}` is an empty dictionary; `set()` is an empty set. | correct | as the row above |
| `summary.formula.tex` | \texttt{counts[k]} \leftarrow \texttt{counts.get(k, 0)} + 1 | correct | as the row above |
| `summary.formula.note` | Each new key starts at 0. Add a quantity instead of 1 to net trades. | correct | as the row above |
| `summary.trap` | `300 in book` checks the keys, so it is `False` even when some ticker holds 300 shares. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l6 q set len` |
| `quiz[0].widget.answer` | KEY: 2 | correct | as the row above |
| `quiz[0].widget.accept` | 2: the set holds 4.85 and 0.72 once each. | correct | as the row above |
| `quiz[0].widget.wrong[0].value` | SLIP value: 4 | correct | as the row above |
| `quiz[0].widget.wrong[1].value` | SLIP value: 3 | correct | as the row above |
| `quiz[0].feedback.correct` | Two different values, each held once. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. A set ignores a value it already holds. | correct | as the row above |
| `quiz[0].feedback.byKey.all` | You counted every value written. The set drops the repeat 4.85, and adding 0.72 again changes nothing. | correct | as the row above |
| `quiz[0].feedback.byKey.three` | You counted the `add` as new. 0.72 is already in the set, so adding it changes nothing. | correct | as the row above |
| `quiz[0].explain.text` | `set([4.85, 4.85, 0.72])` holds 4.85 and 0.72. Adding 0.72 again leaves it unchanged, so `len(s)` is 2. | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l6 in keys` |
| `quiz[1].widget.options[0].text` | KEY: `False` | correct | as the row above |
| `quiz[1].widget.options[1].why` | You searched the values. "VOD" is a value here; the only key is "BP". | correct | as the row above |
| `quiz[1].widget.options[2].why` | `in` never raises `KeyError`. It answers `True` or `False`. | correct | as the row above |
| `quiz[1].feedback.correct` | `in` checks keys, and the only key is "BP". | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Ask which strings are keys. | correct | as the row above |
| `quiz[1].explain.text` | The dictionary has one key, "BP", whose value happens to be "VOD". `in` looks at keys only, so the answer i... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | 3 buys - 2 sells = 1 |
| `quiz[2].widget.answer` | KEY: 1 | correct | as the row above |
| `quiz[2].widget.accept` | 1: three buys minus two sells. | correct | as the row above |
| `quiz[2].widget.wrong[0].value` | SLIP value: 3 | correct | as the row above |
| `quiz[2].widget.wrong[1].value` | SLIP value: 5 | correct | as the row above |
| `quiz[2].feedback.correct` | Three buys, two sells: the difference is 1. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. Count each side, then subtract. | correct | as the row above |
| `quiz[2].feedback.byKey.buys` | You gave the number of buys. The line subtracts the 2 sells. | correct | as the row above |
| `quiz[2].feedback.byKey.total` | You counted every trade. The line subtracts sells from buys. | correct | as the row above |
| `quiz[2].explain.text` | The loop leaves `{"buy": 3, "sell": 2}`. The difference is 1. | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l6 q dict add` (exact message) |
| `quiz[3].widget.options[0].text` | KEY: It stops with an `AttributeError`. | correct | as the row above |
| `quiz[3].widget.options[1].why` | You read `{}` as an empty set. Empty braces make a dictionary; an empty set is `set()`. | correct | as the row above |
| `quiz[3].widget.options[2].why` | Dictionaries store values with `d[k] = v`. They have no `add` method at all. | correct | as the row above |
| `quiz[3].feedback.correct` | `{}` is an empty dictionary, and dictionaries cannot `add`. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. What type do empty braces make? | correct | as the row above |
| `quiz[3].explain.text` | `{}` makes an empty dictionary, so `seen.add` does not exist: `AttributeError: 'dict' object has no attribu... | correct | as the row above |
| `screens[0].widget.answer` | KEY: ["c0", "c1", "c3"] | correct | first appearances at indices 0, 1, 3 by inspection |
| `screens[1].widget.answer` | KEY: {"bp": ["t0", "t2", "t5"], "vod": ["t1", "t4"], "azn": ["t3"]} | correct | counts BP 3, VOD 2, AZN 1 by inspection |

## l7-arguments.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A trade costs price times quantity, plus a broker's fee. The `def` line gives `fee` a value of its own. [code] | correct | run `l7 cost` |
| `screens[0].widget.options[0].text` | KEY: `251.5`, then `250.0` | correct | as the row above |
| `screens[0].widget.options[1].why` | You expected every parameter to need a value. `fee=1.50` gives it one when the call leaves it out. | correct | as the row above |
| `screens[0].widget.options[2].why` | You kept the 1.50 on the second call. A value you pass replaces the default. | correct | as the row above |
| `screens[0].widget.options[3].why` | You left the fee out of the first call. When the call gives no fee, 1.50 is still added. | correct | as the row above |
| `screens[0].hints[0].text` | The first call gives two values for three parameters. Where does `fee` get one? | correct | as the row above |
| `screens[0].hints[1].text` | `fee` holds 1.50 before any call fills it. | correct | as the row above |
| `screens[0].hints[2].text` | First call: 2.50 × 100 + 1.50 = 251.5. Second call: the 0.00 replaces 1.50, so 250.0. | correct | as the row above |
| `screens[0].feedback.correct` | The left-out fee falls back to 1.50; a passed fee replaces it. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. A parameter with `=` in the `def` line has a value to fall back on. | correct | as the row above |
| `screens[0].explain.text` | `fee=1.50` is a value the parameter starts with. The first call fills `price` and `qty` and leaves `fee` al... | correct | as the row above |
| `screens[1].prose` | Arguments can also name the parameter they fill. [code] | correct | argument binding: positional left to right, then keywords by name (Python reference 6.3.4 Calls) |
| `screens[1].hints[0].text` | Values with `name=` go to that name. Values without one fill parameters from the left. | correct | as the row above |
| `screens[1].hints[1].text` | These two carry their parameter's name. | correct | as the row above |
| `screens[1].hints[2].text` | 2.50 fills `price`, 200 fills `qty` and 0.00 fills `fee`. The default 1.50 is not used. | correct | as the row above |
| `screens[1].feedback.correct` | Unnamed values fill from the left; named ones go straight to their parameter. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Match each `name=value` by its name, and the unnamed value by position. | correct | as the row above |
| `screens[1].feedback.byKey.a1` | 2.50 has no name, so it fills the first parameter, `price`. | correct | as the row above |
| `screens[1].feedback.byKey.a2` | `fee=0.00` names its parameter, so 0.00 goes to `fee` wherever it sits in the call. | correct | as the row above |
| `screens[1].feedback.byKey.a3` | `qty=200` is matched by name, not by position: 200 fills `qty`. | correct | as the row above |
| `screens[1].feedback.byKey.d150` | The call passes a fee, 0.00, so the default 1.50 is not used. | correct | as the row above |
| `screens[1].explain.text` | Unnamed values fill parameters left to right, and named ones go straight to their parameter. So the order o... | correct | as the row above |
| `screens[2].prose` | A value matched by position is a **positional argument**. `qty=200` in a call is a **keyword argument**. `f... | correct | run `l7 positional after keyword SyntaxError` |
| `screens[2].widget.options[0].text` | KEY: `cost(price=2.50, 100)` | correct | as the row above |
| `screens[2].widget.options[1].why` | This one is fine: a positional value first, then a keyword. | correct | as the row above |
| `screens[2].widget.options[2].why` | This one is fine: keywords may come in any order, since each names its parameter. | correct | as the row above |
| `screens[2].widget.options[3].why` | This one is fine: the keyword replaces the default. | correct | as the row above |
| `screens[2].hints[0].text` | In which call does a bare value come after a named one? | correct | as the row above |
| `screens[2].hints[1].text` | After `price=2.50`, which parameter should a bare 100 fill? | correct | as the row above |
| `screens[2].hints[2].text` | `cost(price=2.50, 100)` puts a positional value after a keyword. Python rejects that before running anything. | correct | as the row above |
| `screens[2].feedback.correct` | A positional argument after a keyword is a `SyntaxError`. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Look for a bare value that comes after a `name=value`. | correct | as the row above |
| `screens[2].feedback.byKey.swapped` | Keyword order never matters, so this call is fine. Look for a bare value after a keyword. | correct | as the row above |
| `screens[2].explain.text` | After a keyword argument Python cannot tell which parameter a bare value should fill. So `cost(price=2.50, ... | correct | as the row above |
| `screens[3].prose` | A broker charges a rate on the notional (the trade's £ size), but never less than a minimum. Give `fee` two... | correct | run `l7 fee`; harness: minimum-before-rate slip first fails test 3 |
| `screens[3].widget.how` | Check runs 7 hidden tests, some with keyword arguments in any order. Fees are compared with `math.isclose`. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[3].hints[0].text` | Only the `def` line needs to change. | correct | run `l7 fee`; harness: minimum-before-rate slip first fails test 3 |
| `screens[3].hints[1].text` | A default is written `name=value` inside the brackets of `def`. | correct | as the row above |
| `screens[3].hints[2].text` | `def fee(notional, rate=0.001, minimum=1.50):` | correct | as the row above |
| `screens[3].feedback.correct` | All seven tests passed, keyword calls included. | correct | as the row above |
| `screens[3].feedback.generic` | Some tests failed. Give `rate` and `minimum` their defaults in the `def` line, in that order. | correct | as the row above |
| `screens[3].feedback.byKey.test-1` | Test 1 calls `fee(20000.00)` with no rate or minimum. Give both parameters defaults: `rate=0.001, minimum=1... | correct | as the row above |
| `screens[3].feedback.byKey.test-3` | Test 3 calls `fee(20000.00, 0.0005)`, so the second positional value must fill `rate`. Keep `rate` before `... | correct | as the row above |
| `screens[3].explain.text` | Defaults make the common call short, and keywords let a caller change just the one they need. Order still m... | correct | as the row above |
| `screens[4].prose` | [code] | correct | run `l7 tuple return` |
| `screens[4].widget.options[0].text` | KEY: `(4.91, 4.72) 2` | correct | as the row above |
| `screens[4].widget.options[1].why` | You thought `return` stops at the first comma. The comma builds one tuple holding both values. | correct | as the row above |
| `screens[4].widget.options[2].why` | Commas make a tuple, printed with round brackets, not a list. | correct | as the row above |
| `screens[4].widget.options[3].why` | It does return one value: a tuple. `hi, lo = r` then unpacks it. | correct | as the row above |
| `screens[4].hints[0].text` | What do commas build, outside any brackets? | correct | as the row above |
| `screens[4].hints[1].text` | `return a, b` hands back the tuple `(a, b)`. | correct | as the row above |
| `screens[4].hints[2].text` | `r` is `(4.91, 4.72)`, a tuple of length 2. | correct | as the row above |
| `screens[4].feedback.correct` | One tuple, holding both answers. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. `return max(prices), min(prices)` returns a single tuple. | correct | as the row above |
| `screens[4].explain.text` | `return a, b` builds one tuple, `(4.91, 4.72)`. Unpacking from level 1 splits it: `hi, lo = high_low(...)`.... | correct | as the row above |
| `screens[5].prose` | A string on the first line of a function's body is its **docstring**. Python stores it, and `help(high_low)... | correct | run `l7 mid spread`; docstring is the first statement of the body, stored in __doc__ (PEP 257) |
| `screens[5].widget.how` | Check runs 7 hidden tests: the tuple's parts, its length, a keyword call, and a check that the docstring is... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[5].hints[0].text` | Three lines: the docstring, the two calculations, and one `return` with a comma. | correct | run `l7 mid spread`; docstring is the first statement of the body, stored in __doc__ (PEP 257) |
| `screens[5].hints[1].text` | `mid = (bid + ask) / 2` and `spread = ask - bid`. | correct | as the row above |
| `screens[5].hints[2].text` | First line `"""Return the mid and spread of a quote."""`, then `return mid, spread`. | correct | as the row above |
| `screens[5].feedback.correct` | All seven tests passed: a documented function returning one tuple. | correct | as the row above |
| `screens[5].feedback.generic` | Some tests failed. Return `mid, spread` in that order, and open the body with a string. | correct | as the row above |
| `screens[5].feedback.byKey.test-1` | Test 1 wants a tuple. `return mid, spread` builds one; square brackets build a list. | correct | as the row above |
| `screens[5].feedback.byKey.test-2` | Test 2 reads the first item as the mid. Return `mid, spread` in that order. | correct | as the row above |
| `screens[5].feedback.byKey.test-6` | Test 6 looks for a docstring. A `#` comment is thrown away; put a string in triple quotes on the body's fir... | correct | as the row above |
| `screens[5].explain.text` | For a bid of 4.84 and an ask of 4.86 the mid is 4.85 and the spread 0.02. The docstring says what comes bac... | correct | as the row above |
| `screens[6].prose` | A helper keeps a log of tickers traded. Leave `log` out and you get a new list, or so its author thought. [... | correct | run `l7 shared default`; defaults are evaluated once at definition (Python reference 8.7) |
| `screens[6].widget.options[0].text` | KEY: `['BP', 'VOD']` | correct | as the row above |
| `screens[6].widget.options[1].why` | You expected a fresh empty list on each call. The default list is made once, when `def` runs, and every cal... | correct | as the row above |
| `screens[6].widget.options[2].why` | `b` is the result of the second call, which appended VOD. | correct | as the row above |
| `screens[6].widget.options[3].why` | `log` has a default, so a call may leave it out. | correct | as the row above |
| `screens[6].hints[0].text` | When is the `[]` in the `def` line evaluated: at each call, or once? | correct | as the row above |
| `screens[6].hints[1].text` | There is only one default list, and it is made when `def` runs. | correct | as the row above |
| `screens[6].hints[2].text` | The first call appends BP to the default list; the second appends VOD to the same list. | correct | as the row above |
| `screens[6].feedback.correct` | One list, made once, shared by both calls. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Ask how many default lists exist. | correct | as the row above |
| `screens[6].feedback.byKey.fresh` | You expected a new list per call. `log=[]` runs once, at `def`, so both calls append to one list: `a` and `... | correct | as the row above |
| `screens[6].explain.text` | Python evaluates `log=[]` once, when `def` runs, and keeps that one list as the default. Each call without ... | correct | as the row above |
| `screens[7].prose` | A dictionary default has the same problem. The fix is `None` as the default, and a fresh object made inside... | correct | same rule as s6; harness: solution passes 6 tests |
| `screens[7].widget.how` | Check runs 6 hidden tests in one session, so a default that remembers earlier calls fails. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[7].hints[0].text` | Change the default to `None`, then make the dictionary inside the call. | correct | same rule as s6; harness: solution passes 6 tests |
| `screens[7].hints[1].text` | `if book is None:` is true only when the caller left `book` out. | correct | as the row above |
| `screens[7].hints[2].text` | `def record(ticker, qty, book=None):`, then `if book is None:` and `book = {}` before the update. | correct | as the row above |
| `screens[7].feedback.correct` | All six tests passed: fresh books for fresh calls, and a passed book updated. | correct | as the row above |
| `screens[7].feedback.generic` | Some tests failed. Use `book=None` and make a new dictionary only when `book is None`. | correct | as the row above |
| `screens[7].feedback.byKey.test-2` | Test 2 is a fresh call, but your book still held BP from test 1. Use `book=None` and make a new dictionary ... | correct | as the row above |
| `screens[7].feedback.byKey.test-3` | Test 3 passes a book holding 100 BP, and your code threw it away. Make a new dictionary only when `book is ... | correct | as the row above |
| `screens[7].explain.text` | `None` cannot change, so sharing it is harmless; `is None` tells a left-out book from a passed one. A passe... | correct | as the row above |
| `screens[8].prose` | [code] | correct | run `l7 f(1,c=[5])` |
| `screens[8].widget.options[0].text` | KEY: `(1, 2, [5])` | correct | as the row above |
| `screens[8].widget.options[1].why` | You filled `b` with the second value written. `c=[5]` names `c`, so `b` keeps its default 2. | correct | as the row above |
| `screens[8].widget.options[2].why` | You replaced the passed list. `c` is not `None` here, so the `if` leaves it alone. | correct | as the row above |
| `screens[8].widget.options[3].why` | `return a, b, c` builds a tuple, not a list. | correct | as the row above |
| `screens[8].feedback.correct` | `b` keeps its default, `c` is the list passed by name, and the three come back as one tuple. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Match `c=[5]` by name, and let `b` fall back to its default. | correct | as the row above |
| `screens[8].explain.text` | `a` is 1 by position, `c` is `[5]` by name, and `b` falls back to 2. The `if` does nothing because `c` was ... | correct | as the row above |
| `screens[9].prose` | A backtest gives daily returns as decimals. Return a tuple: the mean return, and the **maximum drawdown**. ... | correct | run `l7 drawdown`; maximum drawdown = max_t (1 - V_t / max_{s<=t} V_s) (Bacon, Practical Portfolio Performance Measurement, ch. 4); starting value as first peak is stated |
| `screens[9].widget.how` | Check runs 8 hidden tests on the parts of the tuple. Numbers are compared with `math.isclose`. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[9].hints[0].text` | One loop does the drawdown: grow `value`, raise `peak` when beaten, and keep the worst fall. | correct | run `l7 drawdown`; maximum drawdown = max_t (1 - V_t / max_{s<=t} V_s) (Bacon, Practical Portfolio Performance Measurement, ch. 4); starting value as first peak is stated |
| `screens[9].hints[1].text` | Inside the loop: `value = value * (1 + r)`, then update `peak`, then `fall = 1 - value / peak`. | correct | as the row above |
| `screens[9].hints[2].text` | Keep `worst` as the largest `fall`. After the loop, `mean = sum(returns) / len(returns)`; return `mean, wor... | correct | as the row above |
| `screens[9].feedback.correct` | All eight tests passed: the mean, and the worst fall from a peak. | correct | as the row above |
| `screens[9].feedback.generic` | Some tests failed. Check the drawdown on two losing days, `[-0.10, -0.10]`: it should be 0.19. | correct | as the row above |
| `screens[9].feedback.byKey.test-1` | Test 1 wants a tuple. `return mean, worst` builds one. | correct | as the row above |
| `screens[9].feedback.byKey.test-5` | Test 5 is two days of −10%: £1.00 falls to £0.81, a drawdown of 0.19. The peak starts at the £1.00 you bega... | correct | as the row above |
| `screens[9].explain.text` | For −10% then −10%, £1.00 becomes £0.90 then £0.81, so the drawdown is $1 - 0.81/1.00 = 0.19$, not 0.20. Re... | correct | as the row above |
| `summary.ideas[0]` | A default (`fee=1.50`) lets a call leave an argument out; a keyword argument (`qty=200`) matches by name, a... | correct | restates s0 to s9 |
| `summary.ideas[1]` | `return a, b` returns one tuple, which the caller unpacks. A docstring on the body's first line says what c... | correct | as the row above |
| `summary.ideas[2]` | A default is evaluated once, at `def`. For a list or dictionary, default to `None` and make a fresh one ins... | correct | as the row above |
| `summary.formula.tex` | \text{MDD} = \max_t \left(1 - \dfrac{V_t}{\max_{s \le t} V_s}\right), \quad V_0 = 1 | correct | as the row above |
| `summary.formula.note` | $V_t$ is the value of £1 after $t$ days of returns; the starting £1 counts as a peak. | correct | as the row above |
| `summary.trap` | `def f(x, log=[])` shares one list across every call that leaves `log` out. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l7 q scale is 11` |
| `quiz[0].widget.options[0].text` | KEY: `11` | correct | as the row above |
| `quiz[0].widget.options[1].why` | You put 1 into `factor`. `offset=1` names its parameter, so `factor` keeps its default 2. | wrong | Finding 1. Putting 1 into factor gives 5 x 1 + 0 = 5, not 6; 6 is 5 + 1 (factor left out); run `l7 q FINDING` |
| `quiz[0].widget.options[2].why` | You left the offset out. The call passes `offset=1`, so 1 is added. | correct | run `l7 q scale is 11` |
| `quiz[0].widget.options[3].why` | `factor` has a default, so a call may skip it. | correct | as the row above |
| `quiz[0].feedback.correct` | 5 × 2 + 1 = 11. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. `factor` keeps its default; `offset` is set by name. | correct | as the row above |
| `quiz[0].explain.text` | `x` is 5 by position, `factor` falls back to 2, and `offset` is 1 by name. So the result is 5 × 2 + 1 = 11. | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l7 q unpack message` (exact message) |
| `quiz[1].widget.options[0].text` | KEY: It stops with a `ValueError`: not enough values to unpack. | correct | as the row above |
| `quiz[1].widget.options[1].why` | Unpacking never fills gaps. The tuple has two items for three names, so it fails. | correct | as the row above |
| `quiz[1].widget.options[2].why` | The tuple is split item by item, and the counts must match. | correct | as the row above |
| `quiz[1].widget.options[3].why` | Python does not repeat the last value. Two items cannot fill three names. | correct | as the row above |
| `quiz[1].feedback.correct` | Two values cannot fill three names. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Count the items in the returned tuple. | correct | as the row above |
| `quiz[1].explain.text` | `f()` returns the tuple `(1, 2)`. Unpacking needs exactly one name per item, so three names raise `ValueErr... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | same rule as s6: one list holds 1, 2, 3 |
| `quiz[2].widget.answer` | KEY: 3 | correct | as the row above |
| `quiz[2].widget.accept` | 3: all three calls append to the one default list. | correct | as the row above |
| `quiz[2].widget.wrong[0].value` | SLIP value: 1 | correct | as the row above |
| `quiz[2].feedback.correct` | The one default list holds 1, 2 and 3. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. Count how many default lists exist. | correct | as the row above |
| `quiz[2].feedback.byKey.fresh` | You expected a fresh list each call. `seen=[]` is made once, at `def`, so it holds all three values by the ... | correct | as the row above |
| `quiz[2].explain.text` | `seen=[]` runs once, when `def` runs. Each call appends to that same list, so the third call sees `[1, 2, 3... | correct | as the row above |
| `quiz[3].prose` | You want `help(value)` to explain what `value` returns. | correct | PEP 257; comments are not stored |
| `quiz[3].widget.options[0].text` | KEY: As a string on the first line inside the body | correct | as the row above |
| `quiz[3].widget.options[1].why` | A comment is thrown away when Python reads the file. Only a string that opens the body is kept. | correct | as the row above |
| `quiz[3].widget.options[2].why` | Code after `return` never runs, and Python looks only at the body's first statement. | correct | as the row above |
| `quiz[3].widget.options[3].why` | A long name helps, but `help` shows the docstring, which is a string opening the body. | correct | as the row above |
| `quiz[3].feedback.correct` | The body's first statement, as a string. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. Python keeps one particular string. | correct | as the row above |
| `quiz[3].explain.text` | Python stores the string that opens a function's body as its `__doc__`, and `help` prints it. Triple quotes... | correct | as the row above |
| `screens[1].widget.answer` | KEY: {"price": ["a1"], "qty": ["a3"], "fee": ["a2"], "unused": ["d150"]} | correct | argument binding: positional left to right, then keywords by name (Python reference 6.3.4 Calls) |

## l8-who-changes-the-list.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | Two names, one assignment between them, and one change. [code] | correct | run `l2 alias` (same behaviour) |
| `screens[0].widget.options[0].text` | KEY: `[5, 8, 3]` | correct | as the row above |
| `screens[0].widget.options[1].why` | You read `b = a` as a copy. It gives the same list a second name, so a change through `b` shows through `a`. | correct | as the row above |
| `screens[0].widget.options[2].why` | You put 3 at the front. `append` adds at the end. | correct | as the row above |
| `screens[0].hints[0].text` | Does `b = a` build a new list, or point a second name at the old one? | correct | as the row above |
| `screens[0].hints[1].text` | No line builds a second list, so there is only one. Appending through `b` changes the list `a` names. | correct | as the row above |
| `screens[0].feedback.correct` | One list with two names; the change shows through both. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Count how many lists the code builds. | correct | as the row above |
| `screens[0].explain.text` | `b = a` does not copy anything. It puts a second name on the same list. `b.append(3)` changes that one list... | correct | as the row above |
| `screens[1].prose` | Think of a name as a label stuck on an object. `list(a)` builds a new list with the same values. [code] | correct | list(a) builds a new list; names bind to objects (docs, Data model) |
| `screens[1].hints[0].text` | Which line builds a second list? Every other name shares the first. | correct | as the row above |
| `screens[1].hints[1].text` | `c = list(a)` is the only line that makes a new list. | correct | as the row above |
| `screens[1].hints[2].text` | `a` and `b` label the list that was appended to. `c` labels the copy, still [5, 8]. | correct | as the row above |
| `screens[1].feedback.correct` | `a` and `b` share one list; `c` has its own. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Only `list(a)` builds a new object; `b = a` just adds a label. | correct | as the row above |
| `screens[1].feedback.byKey.a` | `a` still labels the first list, and the append changed that list. | correct | as the row above |
| `screens[1].feedback.byKey.b` | `b = a` puts the label `b` on the list `a` already labels. It does not make a new list. | correct | as the row above |
| `screens[1].feedback.byKey.c` | `list(a)` builds a new list with the same values, so `c` has its own, which the append never touches. | correct | as the row above |
| `screens[1].explain.text` | Names are labels on objects. `b = a` adds a label, while `list(a)` makes a new object. `b.append(3)` change... | correct | as the row above |
| `screens[2].prose` | A call does what `b = a` does: the parameter becomes another label on the object you pass. A function that ... | correct | arguments are passed by assignment (Python FAQ, Programming: call by object reference) |
| `screens[2].widget.options[0].text` | KEY: `[250.0, 120.0, 1.5]` | correct | as the row above |
| `screens[2].widget.options[1].why` | You treated `costs` as a copy. It is a second label on `mine`'s list, so the append shows. | correct | as the row above |
| `screens[2].widget.options[2].why` | `add_fee` returns `None`, but the line prints `mine`, not the result of the call. | correct | as the row above |
| `screens[2].hints[0].text` | During the call, which list does `costs` label? | correct | as the row above |
| `screens[2].hints[1].text` | No line in this program makes a copy. | correct | as the row above |
| `screens[2].hints[2].text` | `costs` labels `mine`'s list, so `costs.append(1.50)` adds to it. | correct | as the row above |
| `screens[2].feedback.correct` | The function changed the caller's list. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. A parameter labels the object passed in; it is not a copy. | correct | as the row above |
| `screens[2].feedback.byKey.copy` | You expected the function to work on a copy. Python never copies on a call, so `mine` gains the 1.50. | correct | as the row above |
| `screens[2].explain.text` | The call labels `mine`'s list as `costs` too. `append` changes that one object, so `mine` shows the fee aft... | correct | as the row above |
| `screens[3].prose` | [code] | correct | run `l8 reset/clear` |
| `screens[3].widget.options[0].text` | KEY: `[1.5, 2.0] []` | correct | as the row above |
| `screens[3].widget.options[1].why` | You treated `costs = []` as emptying the list. It moves the label `costs` to a new list; `x` still labels t... | correct | as the row above |
| `screens[3].widget.options[2].why` | You treated both as local. `clear()` is a method call on the object itself, so `y` sees it. | correct | as the row above |
| `screens[3].widget.options[3].why` | You swapped them. `=` only moves a label; `clear()` empties the object. | correct | as the row above |
| `screens[3].hints[0].text` | Which function changes an object, and which only moves a name? | correct | as the row above |
| `screens[3].hints[1].text` | `costs = []` sticks the label `costs` on a brand new list. | correct | as the row above |
| `screens[3].hints[2].text` | `reset` moves its local label and changes nothing outside. `clear` empties `y`'s list. | correct | as the row above |
| `screens[3].feedback.correct` | `=` moved a local label; `clear()` changed the object. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Assigning to a parameter never touches the caller's object. | correct | as the row above |
| `screens[3].explain.text` | Inside `reset`, `costs = []` moves the local label to a new empty list, and `x` is untouched. Inside `clear... | correct | as the row above |
| `screens[4].prose` | [code] | correct | run `l8 sort vs sorted` |
| `screens[4].widget.options[0].text` | KEY: `[4.72, 4.91] None [4.72, 4.91]` | correct | as the row above |
| `screens[4].widget.options[1].why` | You expected `sort()` to hand the list back. It changes the list in place and, like `append`, returns `None`. | correct | as the row above |
| `screens[4].widget.options[2].why` | You treated `sort()` like `sorted`. `sort()` reorders the list itself. | correct | as the row above |
| `screens[4].widget.options[3].why` | `sorted` returns a new list in order; it does not hand back the original order. | correct | as the row above |
| `screens[4].hints[0].text` | One of these builds a new list; the other changes the old one. | correct | as the row above |
| `screens[4].hints[1].text` | `sorted(prices)` returns a new list. `prices.sort()` reorders `prices` and returns nothing. | correct | as the row above |
| `screens[4].hints[2].text` | `s` is the sorted copy, `t` is `None`, and `prices` is now sorted too. | correct | as the row above |
| `screens[4].feedback.correct` | `sorted` returns a new list; `.sort()` changes the list and returns `None`. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. Check what each one returns, and which one changes `prices`. | correct | as the row above |
| `screens[4].explain.text` | `sorted` returns a new sorted list and leaves its argument alone. `.sort()` mutates the list and returns `N... | correct | as the row above |
| `screens[5].prose` | A colleague's `median` looks as if it only reads the prices. [code] | correct | run `l8 median side effect` |
| `screens[5].widget.options[0].text` | KEY: `4.72` | correct | as the row above |
| `screens[5].widget.options[1].why` | You assumed `median` only reads `prices`. `xs.sort()` sorts the caller's list in place, so its first value ... | correct | as the row above |
| `screens[5].widget.options[2].why` | That is the median, `m`. The line prints `prices[0]`. | correct | as the row above |
| `screens[5].hints[0].text` | Which list does `xs` label during the call? | correct | as the row above |
| `screens[5].hints[1].text` | `xs.sort()` is a mutating method. | correct | as the row above |
| `screens[5].hints[2].text` | `xs` labels `prices`, so the sort reorders `prices` to [4.72, 4.85, 4.91]. Its first value is 4.72. | correct | as the row above |
| `screens[5].feedback.correct` | The call sorted the caller's list as a side effect. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Ask what `xs.sort()` does to the list passed in. | correct | as the row above |
| `screens[5].feedback.byKey.reads` | You trusted the name `median` to mean read-only. `xs.sort()` reordered `prices` itself, so `prices[0]` is n... | correct | as the row above |
| `screens[5].explain.text` | `xs` is a second label on `prices`, so `xs.sort()` reorders the caller's list. Anyone reading `prices` afte... | correct | as the row above |
| `screens[6].prose` | Fix `median` so it never changes the list it is given. For an even number of values, return the mean of the... | correct | sorted leaves its argument alone; 'only reads its arguments' read strictly is the standard definition (no side effects, result depends on arguments only). See finding 4 for the looser summary line |
| `screens[6].widget.how` | Check runs 6 hidden tests. Two of them look at your argument after the call; even lengths are compared with... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[6].hints[0].text` | Work on `sorted(xs)`, never on `xs` itself. | correct | run `l8 even median`; harness: solution passes 6 tests |
| `screens[6].hints[1].text` | With `s = sorted(xs)` and `mid = len(s) // 2`, an odd length gives `s[mid]`. | correct | as the row above |
| `screens[6].hints[2].text` | If `len(s) % 2 == 1` return `s[mid]`; otherwise return `(s[mid - 1] + s[mid]) / 2`. | correct | as the row above |
| `screens[6].feedback.correct` | All six tests passed, and no argument changed. | correct | as the row above |
| `screens[6].feedback.generic` | Some tests failed. Sort a copy with `sorted`, and average the two middle values for an even length. | correct | as the row above |
| `screens[6].feedback.byKey.test-2` | Test 2 looked at the list after the call, and it had been sorted. Use `s = sorted(xs)` instead of `xs.sort()`. | correct | as the row above |
| `screens[6].feedback.byKey.test-3` | Test 3 has four values, so the median is the mean of the two middle ones: (4.80 + 4.90) / 2 = 4.85. | correct | as the row above |
| `screens[6].explain.text` | `sorted` hands back a new list, so the caller's prices keep their order. For four values the two middle one... | correct | as the row above |
| `screens[7].prose` | `return` inside a loop ends the whole call at once. A function that falls off the end without finding anyth... | correct | 0.00 < 0 is False; first loss at index 1 |
| `screens[7].widget.options[0].text` | KEY: `1 None` | correct | as the row above |
| `screens[7].widget.options[1].why` | You kept going after the first loss. `return` ends the call at once, at index 1. | correct | as the row above |
| `screens[7].widget.options[2].why` | 0.00 is not below 0, so it is not a loss. The second call reaches `return None`. | correct | as the row above |
| `screens[7].widget.options[3].why` | When the loop finds nothing, the last line returns `None`; nothing fails. | correct | as the row above |
| `screens[7].hints[0].text` | In the first list, which index is the first P&L below 0? | correct | as the row above |
| `screens[7].hints[1].text` | Is 0.00 below 0? | correct | as the row above |
| `screens[7].hints[2].text` | The first call returns 1 as soon as it sees −35.50. The second finds no loss and returns `None`. | correct | as the row above |
| `screens[7].feedback.correct` | An early `return` at index 1, and `None` when there is no loss. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Stop at the first value strictly below 0; otherwise the call returns `None`. | correct | as the row above |
| `screens[7].explain.text` | The loop stops the moment `return i` runs, so −80.00 is never checked. In the second list 0.00 fails `< 0`,... | correct | as the row above |
| `screens[8].prose` | Return a new book with one trade netted in; the caller's book must not change. `dict(book)` makes a copy to... | correct | run `l8 dict copy shallow`; harness: solution passes 7 tests |
| `screens[8].widget.how` | Check runs 7 hidden tests. Some look at the book you were given after the call. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[8].hints[0].text` | Copy first, then change only the copy. | correct | run `l8 dict copy shallow`; harness: solution passes 7 tests |
| `screens[8].hints[1].text` | `new = dict(book)` is a new dictionary with the same pairs. | correct | as the row above |
| `screens[8].hints[2].text` | Update `new[ticker]`, `del new[ticker]` if it is 0, and return `new`. | correct | as the row above |
| `screens[8].feedback.correct` | All seven tests passed: a new book every time, and the old one untouched. | correct | as the row above |
| `screens[8].feedback.generic` | Some tests failed. Copy with `dict(book)`, change the copy, and drop a ticker that nets to 0. | correct | as the row above |
| `screens[8].feedback.byKey.test-2` | Test 2 looked at the book you were given after the call, and it had changed. Copy it first with `new = dict... | correct | as the row above |
| `screens[8].feedback.byKey.test-4` | Test 4 nets BP to 0. Remove a flat ticker with `del new[ticker]`. | correct | as the row above |
| `screens[8].explain.text` | `dict(book)` builds a new dictionary, so storing or deleting a key lands on the copy. The caller can keep t... | correct | as the row above |
| `screens[9].prose` | Two kinds of function, and how to tell them apart: [code] A mutating function should say so in its docstring. | correct | run `l8 + builds new list`, `l8 sort vs sorted` |
| `screens[9].widget.options[0].text` | KEY: `ys = xs + [4.95]` | correct | as the row above |
| `screens[9].widget.options[1].why` | `append` is a method that adds to the list itself. | correct | as the row above |
| `screens[9].widget.options[2].why` | `ys = xs` adds a label, not a copy, so appending through `ys` changes `xs`. | correct | as the row above |
| `screens[9].widget.options[3].why` | `sort` reorders the list in place and returns `None`. | correct | as the row above |
| `screens[9].feedback.correct` | `+` builds a new list and leaves `xs` alone. | correct | as the row above |
| `screens[9].feedback.generic` | Not quite right. Look for the one that builds a new object. | correct | as the row above |
| `screens[9].explain.text` | `xs + [4.95]` builds a new list and labels it `ys`. The other three all reach the object `xs` labels and ch... | correct | as the row above |
| `screens[10].prose` | Value a position book at today's closing prices in £. If any held ticker has no price, the total is unknown... | correct | run `l8 book value`; harness: solution passes 7 tests |
| `screens[10].widget.how` | Check runs 7 hidden tests, including a ticker with no price, a short position and an empty book. Totals are... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[10].hints[0].text` | Check each ticker before you look its price up. | correct | run `l8 book value`; harness: solution passes 7 tests |
| `screens[10].hints[1].text` | `if ticker not in prices:` is the test, and `return None` leaves at once. | correct | as the row above |
| `screens[10].hints[2].text` | Put `if ticker not in prices: return None` as the first line inside the loop. | correct | as the row above |
| `screens[10].feedback.correct` | All seven tests passed: a total when every price is known, `None` when one is not. | correct | as the row above |
| `screens[10].feedback.generic` | Some tests failed. Return `None` as soon as a held ticker has no price. | correct | as the row above |
| `screens[10].feedback.byKey.test-2` | Test 2 holds TSCO, which has no price. `prices[ticker]` raises `KeyError`, and pricing it at 0 or skipping ... | correct | as the row above |
| `screens[10].explain.text` | For 500 BP at £4.85 and 1,000 VOD at £0.72 the book is worth £3,145.00. A missing price makes the whole tot... | correct | as the row above |
| `summary.ideas[0]` | Assignment and calls never copy: `b = a` and passing `a` to a function put a second label on the same object. | correct | restates s0 to s8 |
| `summary.ideas[1]` | Methods such as `append`, `sort` and `clear` change the object for every label and return `None`. `d[k] = v... | correct | as the row above |
| `summary.ideas[2]` | A pure function reads its arguments and returns a new value (`sorted`, `dict(book)`). An early `return None... | imprecise | Finding 4. Purity also needs no other side effect (printing, globals, the random stream) and a result fixed by the arguments; a function can read its arguments, return a new value and still not be pure |
| `summary.formula.tex` | \texttt{sorted(xs)} \to \text{a new list}, \qquad \texttt{xs.sort()} \to \texttt{None} | correct | restates s0 to s8 |
| `summary.formula.note` | If a function changes its argument, say so in the docstring and return `None`. | correct | as the row above |
| `summary.trap` | A function that sorts or appends to its argument changes the caller's list too. Copy first, or use `sorted`. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l8 + builds new list` |
| `quiz[0].widget.options[0].text` | KEY: `[1] [1, 0]` | correct | as the row above |
| `quiz[0].widget.options[1].why` | You treated `xs + [0]` as changing the list. `+` builds a new list, and the label `xs` moves to it. | correct | as the row above |
| `quiz[0].widget.options[2].why` | The function returns `xs`, the new list. | correct | as the row above |
| `quiz[0].feedback.correct` | `+` made a new list; `a` is untouched. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. Does `+` change a list, or build a new one? | correct | as the row above |
| `quiz[0].explain.text` | `xs + [0]` builds a new list `[1, 0]`, and `xs = ...` moves the local label to it. `a` still labels `[1]`. ... | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l4 q sort returns None` |
| `quiz[1].widget.options[0].text` | KEY: `None` | correct | as the row above |
| `quiz[1].widget.options[1].why` | You expected `sort()` to return the list. It sorts in place and returns `None`. | correct | as the row above |
| `quiz[1].widget.options[2].why` | `x` is not the list at all: it is what `sort()` returned. | correct | as the row above |
| `quiz[1].feedback.correct` | `sort()` returns `None`. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. What does `.sort()` return? | correct | as the row above |
| `quiz[1].explain.text` | `.sort()` sorts the list in place and returns `None`, so `x` is `None`. The sorted list itself had no name ... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | 100 + 50 = 150 through one dict (slips 100, 50) |
| `quiz[2].widget.answer` | KEY: 150 | correct | as the row above |
| `quiz[2].widget.accept` | 150: `b` and `c` label one dictionary. | correct | as the row above |
| `quiz[2].widget.wrong[0].value` | SLIP value: 100 | correct | as the row above |
| `quiz[2].widget.wrong[1].value` | SLIP value: 50 | correct | as the row above |
| `quiz[2].feedback.correct` | Both calls changed the one dictionary. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. How many dictionaries does this code build? | correct | as the row above |
| `quiz[2].feedback.byKey.copy` | You treated `c = b` as a copy. It is a second label, so the 50 lands in the same book. | correct | as the row above |
| `quiz[2].feedback.byKey.last` | The second call adds 50 to the 100 already there; it does not replace it. | correct | as the row above |
| `quiz[2].explain.text` | `c = b` labels the same dictionary twice. Both calls mutate it, so BP ends at 100 + 50 = 150. | correct | as the row above |
| `quiz[3].prose` | [code] | correct | None default: a new list per call (same rule as l7 s7) |
| `quiz[3].widget.options[0].text` | KEY: `[2]` | correct | as the row above |
| `quiz[3].widget.options[1].why` | You expected the shared-default problem. With `None` as the default, each call makes a fresh list. | correct | as the row above |
| `quiz[3].widget.options[2].why` | The function returns `out`, the list. | correct | as the row above |
| `quiz[3].feedback.correct` | A fresh list for each call that leaves `out` out. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. When is `out = []` run? | correct | as the row above |
| `quiz[3].explain.text` | `out = []` runs inside the call, so each call without `out` gets its own new list. The second call's list h... | correct | as the row above |
| `screens[1].widget.answer` | KEY: {"l1": ["a", "b"], "l2": ["c"]} | correct | list(a) builds a new list; names bind to objects (docs, Data model) |

## review-2.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | [code] | correct | get default 0 + 300 |
| `items[0].widget.options[0].text` | KEY: `300` | correct | as the row above |
| `items[0].widget.options[1].why` | `get` never raises for a missing key; it returns the default, 0. | correct | as the row above |
| `items[0].widget.options[2].why` | You expected `get` to return `None` here. The default 0 comes back, and 0 + 300 is fine. | correct | as the row above |
| `items[0].widget.options[3].why` | `get` returns the stored value or the default, never the key. | correct | as the row above |
| `items[0].feedback.correct` | The default 0 plus BP's 300. | correct | as the row above |
| `items[0].feedback.generic` | Not quite right. What does `get` return for a missing key when you give a default? | correct | as the row above |
| `items[0].explain.text` | "VOD" is missing, so `stock.get("VOD", 0)` returns the default 0. `stock["BP"]` is 300, and the sum is 300. | correct | as the row above |
| `items[1].prose` | [code] | correct | 5 fills, 3 distinct |
| `items[1].widget.options[0].text` | KEY: `3 5` | correct | as the row above |
| `items[1].widget.options[1].why` | You counted the repeats in the set. A set holds BP once, however often it appears. | correct | as the row above |
| `items[1].widget.options[2].why` | The list keeps all five fills; the set keeps three different tickers. | correct | as the row above |
| `items[1].widget.options[3].why` | You dropped BP altogether. A set keeps one copy of a repeated value. | correct | as the row above |
| `items[1].feedback.correct` | Three different tickers among five fills. | correct | as the row above |
| `items[1].feedback.generic` | Not quite right. A set keeps each value once; a list keeps them all. | correct | as the row above |
| `items[1].explain.text` | `split` gives a list of five strings. The set keeps BP, VOD and AZN once each, so its length is 3; the list... | correct | as the row above |
| `items[2].prose` | Each trade is `(ticker, qty)`, negative for a sell. Volume counts shares traded either way, so a sell of 30... | correct | harness: solution passes 6 tests; 500 + 300 = 800 |
| `items[2].widget.how` | Check runs 6 hidden tests, including a ticker whose buys and sells cancel. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[2].feedback.correct` | All six tests passed: volume counts both sides. | correct | harness: solution passes 6 tests; 500 + 300 = 800 |
| `items[2].feedback.generic` | Some tests failed. Add `abs(qty)` to each ticker's running total. | correct | as the row above |
| `items[2].feedback.byKey.test-1` | Test 1 sells 300 BP, which is still 300 shares traded. Add `abs(qty)`, not `qty`, or the sell cancels the buy. | correct | as the row above |
| `items[2].explain.text` | This is the counting idiom with `abs(qty)` in place of 1. Netting would add `qty`; volume ignores the sign.... | correct | as the row above |
| `items[3].prose` | [code] | correct | keyword binding (l7 s1) |
| `items[3].widget.options[0].text` | KEY: `('buy', 100, 4.85)` | correct | as the row above |
| `items[3].widget.options[1].why` | You filled `side` with the third value written. `limit=4.85` is matched by name, so `side` keeps "buy". | correct | as the row above |
| `items[3].widget.options[2].why` | You kept the default for `limit`. The call passes `limit=4.85`. | correct | as the row above |
| `items[3].widget.options[3].why` | `side` has a default, so a call may skip it. | correct | as the row above |
| `items[3].feedback.correct` | `side` keeps its default; `limit` is set by name. | correct | as the row above |
| `items[3].feedback.generic` | Not quite right. Match `limit=4.85` by its name. | correct | as the row above |
| `items[3].explain.text` | `ticker` and `qty` are filled by position, `limit` by name, and `side` falls back to "buy". The function re... | correct | as the row above |
| `items[4].prose` | [code] | correct | lookup returns the stored object, no copy |
| `items[4].widget.answer` | KEY: 3 | correct | as the row above |
| `items[4].widget.accept` | 3: `closes` labels the list stored under "BP". | correct | as the row above |
| `items[4].widget.wrong[0].value` | SLIP value: 2 | correct | as the row above |
| `items[4].feedback.correct` | The list inside the dictionary gained a close. | correct | as the row above |
| `items[4].feedback.generic` | Not quite right. Does `closes = history["BP"]` copy the list? | correct | as the row above |
| `items[4].feedback.byKey.copy` | You treated `closes` as a copy. A lookup hands back the stored list itself, so the append changes the list ... | correct | as the row above |
| `items[4].explain.text` | `history["BP"]` hands back the list object stored there, and `closes` labels that same object. Appending th... | correct | as the row above |
| `items[5].prose` | `returns` maps ticker to today's return. Return a tuple `(best, worst)`: the ticker with the highest return... | correct | harness: solution passes 6 tests; start-at-0 slip first fails test 3 |
| `items[5].widget.how` | Check runs 6 hidden tests, including an empty dictionary, a single ticker and a day when everything fell. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[5].feedback.correct` | All six tests passed, the empty and all-negative days included. | correct | harness: solution passes 6 tests; start-at-0 slip first fails test 3 |
| `items[5].feedback.generic` | Some tests failed. Start from a real ticker, not from a return of 0. | correct | as the row above |
| `items[5].feedback.byKey.test-3` | Test 3 has one ticker that fell. Starting the best at a return of 0 means no fall can beat it: start from a... | correct | as the row above |
| `items[5].feedback.byKey.test-4` | Test 4 is a day when everything fell. The best ticker is the one that fell least; a start at 0 never moves. | correct | as the row above |
| `items[5].explain.text` | The early `return None, None` handles the empty book. After that, `best is None` lets the first ticker in, ... | correct | as the row above |
| `items[6].prose` | Two desks hold position books. Return one merged book, netting tickers that appear in both and dropping any... | correct | harness: solution passes 7 tests |
| `items[6].widget.how` | Check runs 7 hidden tests. One looks at both books after the call; one checks you returned a new dictionary. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[6].feedback.correct` | All seven tests passed: netted, flat tickers dropped, inputs untouched. | correct | harness: solution passes 7 tests |
| `items[6].feedback.generic` | Some tests failed. Copy `a`, add each of `b`'s quantities to the copy, and drop zeros. | correct | as the row above |
| `items[6].feedback.byKey.test-2` | Test 2 holds BP in both books. Add `b`'s quantity to the running total rather than replacing it. | correct | as the row above |
| `items[6].feedback.byKey.test-3` | Test 3 nets BP to 0, and a flat ticker must be dropped. If you changed `a` itself, test 5 will catch that t... | correct | as the row above |
| `items[6].explain.text` | `dict(a)` gives a copy to work on, so neither desk's book changes. Netting each of `b`'s positions into it ... | correct | as the row above |
| `items[7].prose` | Each version should start a fresh history whenever the caller does not pass one. | correct | defaults evaluated once at def, list() included (Python reference 8.7); run `r2 tuple append` |
| `items[7].widget.options[0].text` | KEY: `def add(p, history=None):` then `if history is None: history = []` | correct | as the row above |
| `items[7].widget.options[1].why` | The `[]` is made once, when `def` runs, and every call that leaves `history` out shares it. | correct | as the row above |
| `items[7].widget.options[2].why` | `list()` is still run once, at `def`, so there is still one shared list. | correct | as the row above |
| `items[7].widget.options[3].why` | A tuple cannot change, so `append` fails with `AttributeError`. | correct | as the row above |
| `items[7].feedback.correct` | `None` as the default, and a new list made inside the call. | correct | as the row above |
| `items[7].feedback.generic` | Not quite right. When is each default evaluated? | correct | as the row above |
| `items[7].explain.text` | Every default is evaluated once, when `def` runs, whether written `[]` or `list()`. Only code inside the bo... | correct | as the row above |
| `items[8].prose` | [code] | correct | run `r2 items/keys/in` |
| `items[8].widget.options[0].text` | KEY: `True True False` | correct | as the row above |
| `items[8].widget.options[1].why` | You let `in` search the values. `in fees` checks keys only, and 1.25 is a value. | correct | as the row above |
| `items[8].widget.options[2].why` | `fees.items()` holds `(key, value)` pairs, and `("TQ", 0.60)` is one of them. | correct | as the row above |
| `items[8].widget.options[3].why` | `fees.keys()` holds the keys, and "LSE" is one of them. | correct | as the row above |
| `items[8].feedback.correct` | Pairs in `.items()`, keys in `.keys()`, and only keys for `in fees`. | correct | as the row above |
| `items[8].feedback.generic` | Not quite right. Ask what each `in` looks through. | correct | as the row above |
| `items[8].explain.text` | `fees.items()` holds the `(key, value)` pairs, so `("TQ", 0.60)` is found, and `fees.keys()` holds "LSE". `... | correct | as the row above |

## homework-2.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | `history` maps each ticker to its closes, oldest first. Return a new dictionary of each ticker's latest clo... | correct | harness: solution passes 6 tests |
| `items[0].widget.how` | Check runs 6 hidden tests, including an empty list and an empty dictionary. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[0].feedback.correct` | All six tests passed, the empty list skipped. | correct | harness: solution passes 6 tests |
| `items[0].feedback.generic` | Some tests failed. Loop over `history.items()` and take `closes[-1]` only when the list is not empty. | correct | as the row above |
| `items[0].feedback.byKey.test-2` | Test 2 has a ticker with no closes. `closes[-1]` raises `IndexError` there: check `len(closes) > 0` first. | correct | as the row above |
| `items[0].explain.text` | `.items()` hands back each ticker with its list, and the length check skips a listing with no closes yet. [... | correct | as the row above |
| `items[1].prose` | Before closing out BP, a trader saves the book twice. [code] | correct | label versus dict(book) copy |
| `items[1].widget.options[0].text` | KEY: `0 300` | correct | as the row above |
| `items[1].widget.options[1].why` | You treated `snapshot = book` as a copy. It is a second label, so it sees BP set to 0. | correct | as the row above |
| `items[1].widget.options[2].why` | `dict(book)` builds a new dictionary, so the later change does not reach `backup`. | correct | as the row above |
| `items[1].widget.options[3].why` | You swapped them: `snapshot` is the label, `backup` is the copy. | correct | as the row above |
| `items[1].feedback.correct` | The label sees the change; the copy does not. | correct | as the row above |
| `items[1].feedback.generic` | Not quite right. Which line builds a new dictionary? | correct | as the row above |
| `items[1].explain.text` | `snapshot = book` adds a label to the same dictionary, so it shows BP at 0. `dict(book)` built a separate c... | correct | as the row above |
| `items[2].prose` | Each fill is `(ticker, qty, price)`: shares bought (negative for sold) at a £ price. Marked at today's clos... | correct | run `hw2 pnl` (25 + 10 = 35; 20; 30; 8) |
| `items[2].widget.how` | Check runs 6 hidden tests on single tickers' totals and the key order. Totals are compared with `math.isclo... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[2].feedback.correct` | All six tests passed: every fill marked to the close and summed per ticker. | correct | run `hw2 pnl` (25 + 10 = 35; 20; 30; 8) |
| `items[2].feedback.generic` | Some tests failed. Check BP in the example: 500 × 0.05 + (−200) × (−0.05) = £35.00. | correct | as the row above |
| `items[2].feedback.byKey.test-1` | Test 1 has two BP fills. Add each fill's P&L to BP's running total, and keep the sign of `qty`: a sale abov... | correct | as the row above |
| `items[2].explain.text` | Bought 500 BP at £4.80 and sold 200 at £4.90, marked at £4.85: £25.00 + £10.00 = £35.00. The sale gains bec... | correct | as the row above |
| `items[3].prose` | Write `commission(notional, venue="LSE", minimum=2.00)`. Look the venue's rate up in `FEES`, with 0.002 for... | correct | run `hw2 commission` |
| `items[3].widget.how` | Check runs 7 hidden tests, called with positional and keyword arguments. Fees are compared with `math.isclo... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[3].feedback.correct` | All seven tests passed, keyword calls and unlisted venues included. | correct | run `hw2 commission` |
| `items[3].feedback.generic` | Some tests failed. Give `venue` and `minimum` defaults, look the rate up with `get`, and apply the minimum ... | correct | as the row above |
| `items[3].feedback.byKey.test-1` | Test 1 calls `commission(25000.00)` alone. Give `venue` and `minimum` defaults in the `def` line. | correct | as the row above |
| `items[3].feedback.byKey.test-3` | Test 3 is a £800.00 trade: 0.0012 × 800 = £0.96, below the £2.00 minimum. Return `max(notional * rate, mini... | correct | as the row above |
| `items[3].feedback.byKey.test-4` | Test 4 trades on AQX, which is not listed. Use `FEES.get(venue, 0.002)`. | correct | as the row above |
| `items[3].explain.text` | Defaults make `commission(25000.00)` mean LSE with a £2.00 minimum, and keywords let a caller change just o... | correct | as the row above |
| `items[4].prose` | Return a tuple `(book, value)`. `book` nets the `(ticker, qty)` trades, leaving out flat tickers. `value` i... | correct | harness: solution passes 9 tests; 300 x 4.85 + 1000 x 0.72 = 2175 |
| `items[4].widget.how` | Check runs 9 hidden tests on both parts of the tuple. They include a missing price, a ticker that goes flat... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[4].feedback.correct` | All nine tests passed: netted, flat tickers dropped, and an honest `None` when a price is missing. | correct | harness: solution passes 9 tests; 300 x 4.85 + 1000 x 0.72 = 2175 |
| `items[4].feedback.generic` | Some tests failed. Net first, drop the zeros, then value only what is still open. | correct | as the row above |
| `items[4].feedback.byKey.test-1` | Test 1 wants a tuple. `return book, value` builds one. | correct | as the row above |
| `items[4].feedback.byKey.test-4` | Test 4 holds TSCO with no price. The value is unknown, so return the book with `None`, not a partial total. | correct | as the row above |
| `items[4].feedback.byKey.test-5` | Test 5 trades TSCO and then flattens it. A flat ticker must leave the book, and then it needs no price. | correct | as the row above |
| `items[4].explain.text` | Three steps in order: net with `get`, keep the non-zero positions, then value them, leaving early with `Non... | correct | as the row above |
| `items[5].prompt` | A colleague's module keeps a position book and values it. [code] (a) What happens on the first call, `add_t... | correct | run `hw2 review model`, `l7 shared default`; total 3145.0 |
| `items[5].model` | **(a)** It stops with `KeyError: 'BP'`. The book starts empty, so `book[ticker]` reads a key that is not th... | correct | as the row above |
| `items[5].rubric[0].text` | (a) Says the first call raises `KeyError: 'BP'` because the key is not there yet, and fixes it with `book.g... | correct | as the row above |
| `items[5].rubric[1].text` | (b) States `{'BP': 100, 'VOD': 50}` and explains that the default dictionary is built once, at `def`, and s... | correct | as the row above |
| `items[5].rubric[2].text` | (c) Finds that `tickers.sort()` returns `None`, so the loop raises `TypeError`, and uses `sorted(book)` | correct | as the row above |
| `items[5].rubric[3].text` | (c) Finds that `prices[t] in prices` tests a price against the keys, so nothing is added (and a missing pri... | correct | as the row above |
| `items[5].rubric[4].text` | (d) Gives a working `add_trade` with `book=None`, a fresh dictionary inside, `get` for new tickers, and a d... | correct | as the row above |
| `items[5].rubric[5].text` | (d) Gives a working `total_value` that returns `None` as soon as a held ticker has no price | correct | as the row above |
| `items[6].prose` | A pre-trade check against position limits. [code] | correct | abs(-600) = 600 > 500; early return None |
| `items[6].widget.options[0].text` | KEY: `False None` | correct | as the row above |
| `items[6].widget.options[1].why` | You compared −600 with 500 directly. `abs(-600)` is 600, which is over the limit. | correct | as the row above |
| `items[6].widget.options[2].why` | The first `if` returns `None` for VOD before `limits[ticker]` is ever read. | correct | as the row above |
| `items[6].widget.options[3].why` | The first `return` ends the call for VOD; it never reaches `return True`. | correct | as the row above |
| `items[6].feedback.correct` | Over the limit gives `False`; no limit at all gives `None`. | correct | as the row above |
| `items[6].feedback.generic` | Not quite right. Follow each call to the first `return` it reaches. | correct | as the row above |
| `items[6].explain.text` | For BP, `abs(-600)` is 600, above 500, so the call returns `False`. For VOD the first test is true, so it r... | correct | as the row above |
| `items[7].prose` | [code] | correct | 3 x 3 = 9 (slips 18, 3) |
| `items[7].widget.answer` | KEY: 9 | correct | as the row above |
| `items[7].widget.accept` | 9: BP traded 3 times, and 3 different tickers. | correct | as the row above |
| `items[7].widget.wrong[0].value` | SLIP value: 18 | correct | as the row above |
| `items[7].widget.wrong[1].value` | SLIP value: 3 | correct | as the row above |
| `items[7].feedback.correct` | 3 BP trades times 3 different tickers. | correct | as the row above |
| `items[7].feedback.generic` | Not quite right. Count BP's trades, then the different tickers. | correct | as the row above |
| `items[7].feedback.byKey.list` | You used the list's length, 6. The set holds each ticker once: 3. | correct | as the row above |
| `items[7].feedback.byKey.once` | You counted BP once. `counts["BP"]` is 3, one per BP trade. | correct | as the row above |
| `items[7].explain.text` | `counts` ends as `{"BP": 3, "VOD": 2, "AZN": 1}` and `seen` holds 3 tickers, so the product is 9. | correct | as the row above |
| `items[8].prose` | `book` maps tickers to shares held, negative for a short, and `prices` maps tickers to £ prices. A holding'... | correct | run `hw2 weights`; harness: solution passes 10 tests; weight = position value / total value including cash |
| `items[8].widget.how` | Check runs 10 hidden tests that call your function. Most read the weights as sorted `(ticker, weight)` pair... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[8].feedback.correct` | The total counts cash and every holding, and the weights land in a new dictionary. A missing price or a zer... | correct | run `hw2 weights`; harness: solution passes 10 tests; weight = position value / total value including cash |
| `items[8].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `items[8].feedback.byKey.test-2` | Test 2 passes `cash=550.0`, so the total is £4,000.00 and VOD's £750.00 is 0.1875. Add `cash` to the total,... | correct | as the row above |
| `items[8].feedback.byKey.test-4` | Test 4 holds TSCO, which has no price. Return `None` rather than skipping it or pricing it at 0. | correct | as the row above |
| `items[8].feedback.byKey.test-5` | Test 5 expects `None` for an empty book with no cash, whose total is 0, and `{}` with £100.00 of cash. | correct | as the row above |
| `items[8].feedback.byKey.test-6` | Test 6's short SHEL cancels BP exactly. With no cash the total is 0, so `None`; add `cash` before you check... | correct | as the row above |
| `items[8].feedback.byKey.test-7` | Test 7 holds a short. Its value is negative, so it lowers the total and gets a negative weight; do not use ... | correct | as the row above |
| `items[8].feedback.byKey.test-8` | Test 8 has whole-number prices and cash, and the total is 14. Divide with `/`, which keeps the fraction; `/... | correct | as the row above |
| `items[8].feedback.byKey.test-9` | Test 9 checks the book after the call. Write the weights into a new dictionary, never into `book`. | correct | as the row above |
| `items[8].explain.text` | One pass finds the total and returns `None` at the first missing price; a second pass fills a new dictionar... | correct | as the row above |

## l9-splitting-files.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A small project keeps its code in two files. You run `main.py`, and its first line is `import pricing`. | correct | import system: sys.path[0] is the script's folder (docs, sys.path) |
| `screens[0].hints[0].text` | The import names a file, but without its ending. | correct | as the row above |
| `screens[0].hints[1].text` | Python looks first in the folder that holds the script you ran. | correct | as the row above |
| `screens[0].hints[2].text` | `pricing` plus `.py` is `pricing.py`, in the same folder as `main.py`. | correct | as the row above |
| `screens[0].feedback.correct` | `import pricing` loads `pricing.py`, found beside `main.py`. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Add `.py` to the name in the import and look beside `main.py`. | correct | as the row above |
| `screens[0].feedback.byKey.q-d-c` | `prices.csv` is data, not Python code. `import` loads Python modules, not data files; data is read with `op... | correct | as the row above |
| `screens[0].feedback.byKey.q-m` | `main.py` is the file doing the importing. `import pricing` asks for a different file. | correct | as the row above |
| `screens[0].feedback.byKey.q-d` | `data` is a folder of data. Python looks for `pricing.py` beside the script you ran, not inside `data`. | correct | as the row above |
| `screens[0].explain.text` | You matched the name to `pricing.py`. Python adds `.py` and looks first in the folder of the script you ran... | correct | as the row above |
| `screens[1].prose` | Here are the two files. [code] [code] | correct | run `l9 simple return` |
| `screens[1].widget.options[0].text` | KEY: `0.05` | correct | as the row above |
| `screens[1].widget.options[1].why` | You subtracted the prices. The function divides first, $105 / 100 = 1.05$, then takes away 1. | correct | as the row above |
| `screens[1].widget.options[2].why` | `import pricing` is the line that defines the name `pricing`. After it, `pricing.` reaches everything the f... | correct | as the row above |
| `screens[1].widget.options[3].why` | You expected the import to need `pricing.py` spelled out. Python adds `.py` itself and finds the file besid... | correct | as the row above |
| `screens[1].hints[0].text` | Follow the call into `pricing.py` with $p_0 = 100$ and $p_1 = 105$. | correct | as the row above |
| `screens[1].hints[1].text` | The code that runs lives in this file. | correct | as the row above |
| `screens[1].hints[2].text` | `105.00 / 100.00 - 1` is 0.05, and rounding to 4 places keeps 0.05. | correct | as the row above |
| `screens[1].feedback.correct` | `pricing.simple_return` ran the function from `pricing.py` and returned 0.05. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Run the function in `pricing.py` by hand with 100.00 and 105.00. | correct | as the row above |
| `screens[1].explain.text` | `import pricing` made one new name in `main.py`: `pricing`. The dot reaches inside it, so `pricing.simple_r... | correct | as the row above |
| `screens[2].prose` | Now you write `pricing.py` yourself. A **log return** is $\ln(p_1 / p_0)$. Python's own `math` module has t... | correct | run `l9 log returns`, `l9 log return never above simple` (ln x <= x - 1, equality only at x = 1) |
| `screens[2].widget.how` | Check runs 6 hidden tests that call your two functions. A number passes when it is within `math.isclose` of... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[2].hints[0].text` | One line at the top makes the name `math` exist in this file. | correct | run `l9 log returns`, `l9 log return never above simple` (ln x <= x - 1, equality only at x = 1) |
| `screens[2].hints[1].text` | `math.log` is the natural log, $\ln$, and it takes one number. | correct | as the row above |
| `screens[2].hints[2].text` | Write `import math` first. Then `log_return` is `return math.log(p1 / p0)`. | correct | as the row above |
| `screens[2].feedback.correct` | Both functions now live in `pricing.py`, ready for any script to import. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Check the first failing test against the two formulas. | correct | as the row above |
| `screens[2].feedback.byKey.test-1` | Test 1 expects 0.05 from £100.00 to £105.00. Divide the new price by the old one, then take away 1. | correct | as the row above |
| `screens[2].feedback.byKey.test-3` | Test 3 calls `log_return(100.00, 105.00)`. A `NameError` for `math` means the file never ran `import math`. | correct | as the row above |
| `screens[2].explain.text` | `import math` sits at the top, so every function in the file can use `math.log`. For £100.00 to £105.00 the... | correct | as the row above |
| `screens[3].prose` | Someone adds notes to the signature in `pricing.py`. The parts after the colons and the arrow are **type hi... | correct | run `l9 str/str TypeError` (exact message); annotations are not enforced at run time (PEP 484) |
| `screens[3].widget.options[0].text` | KEY: `TypeError: unsupported operand type(s) for /: 'str' and 'str'` | correct | as the row above |
| `screens[3].widget.options[1].why` | You expected the hints to turn the text into floats. Hints convert nothing, so the strings reach the divisi... | correct | as the row above |
| `screens[3].widget.options[2].why` | Python does not check hints when it runs. The `def` line is fine; the division is what fails. | correct | as the row above |
| `screens[3].hints[0].text` | Does Python do anything with `: float` when the function runs? | correct | as the row above |
| `screens[3].hints[1].text` | Follow the two strings into the body of the function. | correct | as the row above |
| `screens[3].hints[2].text` | The hints are ignored, so the body runs `"105" / "100"`. Dividing text raises a `TypeError`. | correct | as the row above |
| `screens[3].feedback.correct` | The hints did nothing at run time. The strings reached the division and it failed. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Python ignores hints when it runs, so follow the strings into the body. | correct | as the row above |
| `screens[3].explain.text` | Python ignores type hints when it runs. They are documentation: whoever imports `pricing` sees at a glance ... | correct | as the row above |
| `screens[4].prose` | You left a quick check at the bottom of `pricing.py`: [code] `main.py` is now: [code] | correct | run `l9 import runs module top level once, main guard skipped` (subprocess) |
| `screens[4].widget.options[0].text` | KEY: `0.05`, then `0.0488` | correct | as the row above |
| `screens[4].widget.options[1].why` | You expected the check in `pricing.py` to stay quiet. Importing a module runs every top-level line in it, p... | correct | as the row above |
| `screens[4].widget.options[2].why` | The import comes first in `main.py`. So `pricing.py` runs, and prints, before the next line of `main.py`. | correct | as the row above |
| `screens[4].hints[0].text` | What does Python do with a file when it imports it? | correct | as the row above |
| `screens[4].hints[1].text` | Importing runs this file from top to bottom. | correct | as the row above |
| `screens[4].hints[2].text` | Line 1 of `main.py` runs all of `pricing.py`, so its check prints 0.05. Then `main.py` prints 0.0488. | correct | as the row above |
| `screens[4].feedback.correct` | The import ran the whole of `pricing.py`, including its stray `print`. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. Importing runs every top-level line of the module, once. | correct | as the row above |
| `screens[4].explain.text` | Importing runs the module once, from top to bottom. To keep a check that runs only when you start `pricing.... | correct | as the row above |
| `screens[5].prose` | A second way to import takes one name out of a module. [code] | correct | run `l9 from-import creates only mean` (subprocess; mean is 100.975). On 3.12 the message continues ". Did you forget to import 'statistics'?" |
| `screens[5].widget.options[0].text` | KEY: `NameError: name 'statistics' is not defined` | correct | run `l9 from-import creates only mean`; the option is the stable prefix: 3.12 appends ". Did you forget to import 'statistics'?" |
| `screens[5].widget.options[1].why` | You read the first line as importing the whole module. It brings in the name `mean` only, so `statistics` w... | correct | run `l9 from-import creates only mean` (subprocess; mean is 100.975). On 3.12 the message continues ". Did you forget to import 'statistics'?" |
| `screens[5].widget.options[2].why` | `statistics` does have a `mean`, so the first line works. The failure comes on the last line. | correct | as the row above |
| `screens[5].widget.options[3].why` | `mean` does not round. And the last line never gets that far: the name `statistics` does not exist. | correct | as the row above |
| `screens[5].hints[0].text` | List the names each line creates. | correct | as the row above |
| `screens[5].hints[1].text` | The data is fine. The question is which names exist. | correct | as the row above |
| `screens[5].hints[2].text` | `from statistics import mean` creates `mean` and nothing else. So `statistics.mean` fails, while `mean(clos... | correct | as the row above |
| `screens[5].feedback.correct` | `from statistics import mean` creates the name `mean`, not `statistics`. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Ask which names exist after the first line runs. | correct | as the row above |
| `screens[5].explain.text` | Each import form creates different names. `import statistics` gives `statistics`, used as `statistics.mean(... | correct | as the row above |
| `screens[6].prose` | Traders often draw a band two standard deviations either side of the mean price. A close outside it is unus... | unverified | 'Traders often draw a band two standard deviations either side' matches Bollinger's bands in form, but the frequency claim has no source and Bollinger uses a population sd; the arithmetic is verified by run `l9 band` |
| `screens[6].widget.how` | Check runs 5 hidden tests. Tests 4 and 5 call `mean` and `stdev` by name, so import them with `from`. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[6].hints[0].text` | Import the two names first, so you can write `mean(closes)` with no prefix. | correct | run `l9 band`, `l9 band 2`, `l9 pstdev narrower` (mean 101.50, sample sd 1.2649) |
| `screens[6].hints[1].text` | The two dashed lines sit the same distance from the mean. | correct | as the row above |
| `screens[6].hints[2].text` | `m = mean(closes)` and `s = stdev(closes)`, then return `(round(m - 2 * s, 2), round(m + 2 * s, 2))`. | correct | as the row above |
| `screens[6].feedback.correct` | The band runs from £98.97 to £104.03, and every close sits inside it. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[6].feedback.byKey.test-1` | Test 1 expects `(98.97, 104.03)`. A narrower band comes from one standard deviation, or from `pstdev`, whic... | correct | as the row above |
| `screens[6].feedback.byKey.test-4` | Test 4 calls `mean` by name. With `import statistics` only the name `statistics` exists. Use `from statisti... | correct | as the row above |
| `screens[6].explain.text` | The mean is £101.50 and the sample standard deviation is about £1.26. Two of them either side gives £98.97 ... | correct | as the row above |
| `screens[7].prose` | Ana saves some practice code as `statistics.py` in her project. Now `main.py` stops on its first line. [code] | correct | run `l9 shadowed statistics ImportError` (subprocess), `l9 sys is built in`; built-in and frozen modules are found before sys.path (docs, importlib / sys.meta_path) |
| `screens[7].widget.options[0].text` | KEY: Python imported Ana's `statistics.py`, which has no `mean` | correct | as the row above |
| `screens[7].widget.options[1].why` | `statistics` ships with every Python. The path at the end of the error shows Python found a file, just the ... | correct | as the row above |
| `screens[7].widget.options[2].why` | `from statistics import mean` is a correct form. It failed because the `statistics` Python found was Ana's ... | correct | as the row above |
| `screens[7].widget.options[3].why` | Modules often share a folder; that is how `pricing.py` worked. The problem is the name, which matches a mod... | correct | as the row above |
| `screens[7].hints[0].text` | Read the path at the very end of the error. | correct | as the row above |
| `screens[7].hints[1].text` | Python searches the script's own folder before the standard library's files. | correct | as the row above |
| `screens[7].hints[2].text` | The folder holds a `statistics.py`, so Python imports that file. It has no `mean`, so the import fails. | correct | as the row above |
| `screens[7].feedback.correct` | Ana's file hid Python's own `statistics` module. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. The path at the end of the error names the file Python actually used. | correct | as the row above |
| `screens[7].feedback.byKey.missing` | You assumed the module was missing. It ships with Python; the error shows Python found Ana's file instead. | correct | as the row above |
| `screens[7].feedback.byKey.form` | You blamed the import form. It is fine; the `statistics` Python found was Ana's file, which has no `mean`. | correct | as the row above |
| `screens[7].explain.text` | Unless a module is built into Python itself, as `sys` is, the folder of the script you run is searched firs... | correct | as the row above |
| `screens[8].prose` | You used two import forms, and each creates different names: $$\texttt{import statistics} \;\Rightarrow\; \... | correct | run `l9 from-import creates only mean`, `l9 q Counter` |
| `screens[8].widget.options[0].text` | KEY: `from collections import Counter` | correct | as the row above |
| `screens[8].widget.options[1].why` | `Counter` is a name inside the `collections` module, not a module itself. There is no `Counter.py` to import. | correct | as the row above |
| `screens[8].widget.options[2].why` | That creates the name `collections`, so you would write `collections.Counter(moves)`. | correct | as the row above |
| `screens[8].widget.options[3].why` | That swaps the two names. The module goes after `from`, and the name you want after `import`. | correct | as the row above |
| `screens[8].feedback.correct` | `from collections import Counter` creates the name `Counter` itself. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Ask which name each line creates. | correct | as the row above |
| `screens[8].explain.text` | `Counter` lives inside `collections`. Taking it out with `from` lets you write `Counter(moves)` directly. | correct | as the row above |
| `screens[9].prose` | `random` draws simulated price moves. Seeding it fixes the sequence of draws. [code] | correct | run `l9 seed 7 draws` |
| `screens[9].widget.options[0].text` | KEY: `True` | correct | as the row above |
| `screens[9].widget.options[1].why` | You expected fresh random draws the second time. Seeding with 7 again restarts the same sequence, so both l... | correct | as the row above |
| `screens[9].widget.options[2].why` | With the same seed the draws are fixed in advance. That is what makes a simulation repeatable. | correct | as the row above |
| `screens[9].hints[0].text` | What does `random.seed(7)` do to the draws that follow it? | correct | as the row above |
| `screens[9].hints[1].text` | These three draws come straight after `random.seed(7)`. | correct | as the row above |
| `screens[9].hints[2].text` | Both lists are drawn straight after `random.seed(7)`, so they are the same three moves. | correct | as the row above |
| `screens[9].feedback.correct` | Same seed, same draws: both lists hold the same three moves. | correct | as the row above |
| `screens[9].feedback.generic` | Not quite right. Think about what re-seeding with the same number does. | correct | as the row above |
| `screens[9].explain.text` | A seed fixes the whole sequence of draws that follows. Seeding with 7 twice gives `[1.01, 0.99, 1.01]` both... | correct | run `l9 seed 7 draws`; the sequence is only guaranteed for one Python version, which the line says |
| `screens[10].prose` | A backtest needs a made-up price path that comes out the same on every run. Each day the price moves 1% up ... | correct | run `l9 walk seed 7` (all 21 canvas values, 6 up days, last 92.21911860045137), `l9 walk seed 42`; random.seed sets the shared module-level generator (docs, random) |
| `screens[10].widget.how` | Check runs 6 hidden tests. They call `walk` with fixed seeds, so the same seed must give the same path. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[10].hints[0].text` | Seed once, before the loop. Then draw one move per day. | correct | run `l9 walk seed 7` (all 21 canvas values, 6 up days, last 92.21911860045137), `l9 walk seed 42`; random.seed sets the shared module-level generator (docs, random) |
| `screens[10].hints[1].text` | The path holds `days + 1` prices, because the start counts too. | correct | as the row above |
| `screens[10].hints[2].text` | `random.seed(seed)`, then `prices = [start]`. Each day, append `prices[-1] * random.choice([0.99, 1.01])`. | correct | as the row above |
| `screens[10].feedback.correct` | Seed 7 gives the same path every time, ending at £92.22 after 6 up days out of 20. | correct | as the row above |
| `screens[10].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[10].feedback.byKey.test-1` | Test 1 expects 21 prices for 20 days. Put `start` in the list before the loop. | correct | as the row above |
| `screens[10].feedback.byKey.test-3` | Test 3 compares the last price for seed 7. Seed once, before the loop, and draw with `random.choice([0.99, ... | correct | as the row above |
| `screens[10].explain.text` | Seeding once at the top fixes every draw after it. Seed 7 gives 6 up days in 20 and a last price of £92.22.... | correct | as the row above |
| `summary.ideas[0]` | `import pricing` runs `pricing.py` once and creates one name, `pricing`. Reach inside it with a dot. | correct | restates s1 to s7 |
| `summary.ideas[1]` | `from statistics import mean` creates only `mean`. Type hints such as `p0: float` document a function; Pyth... | correct | as the row above |
| `summary.ideas[2]` | Python searches the script's own folder first, so a file named `statistics.py` or `random.py` hides the rea... | correct | as the row above |
| `summary.formula.tex` | \texttt{import m} \Rightarrow \texttt{m.f(x)} \qquad \texttt{from m import f} \Rightarrow \texttt{f(x)} | correct | as the row above |
| `summary.formula.note` | Checks at the bottom of a module go under `if __name__ == "__main__":` so imports skip them. | correct | as the row above |
| `summary.trap` | Never name your own file after a module you import. For most modules Python finds your file first, and the ... | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l9 q sqrt NameError` |
| `quiz[0].widget.options[0].text` | KEY: `NameError: name 'sqrt' is not defined` | correct | as the row above |
| `quiz[0].widget.options[1].why` | You read `import math` as bringing in every name. It creates only `math`, so you need `math.sqrt(16)`. | correct | as the row above |
| `quiz[0].widget.options[2].why` | `math.sqrt` returns a float, 4.0. But here the name `sqrt` was never created. | correct | as the row above |
| `quiz[0].widget.options[3].why` | `import math` is the line that creates `math`. The name that is missing is `sqrt`. | correct | as the row above |
| `quiz[0].feedback.correct` | `import math` creates `math` only. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. List the names `import math` creates. | correct | as the row above |
| `quiz[0].explain.text` | `import math` gives one name, `math`. Write `math.sqrt(16)`, or import the name with `from math import sqrt`. | correct | as the row above |
| `quiz[1].prose` | [code] | correct | run `l9 q Counter` |
| `quiz[1].widget.options[0].text` | KEY: `[('up', 3)]` | correct | as the row above |
| `quiz[1].widget.options[1].why` | `most_common` returns a list of (value, count) pairs, even when you ask for one. | correct | as the row above |
| `quiz[1].widget.options[2].why` | The 1 asks for the single most common pair only. | correct | as the row above |
| `quiz[1].widget.options[3].why` | `most_common` gives a list of pairs, not a dict. | correct | as the row above |
| `quiz[1].feedback.correct` | Three ups and two downs; the top pair is `('up', 3)`. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Count each move, then keep the top one. | correct | as the row above |
| `quiz[1].explain.text` | `Counter` counts each value: 3 ups and 2 downs. `most_common(1)` returns a list holding the top (value, cou... | correct | as the row above |
| `quiz[2].prose` | Your folder holds `walk.py` and an old experiment saved as `random.py`, which defines no `seed`. `walk.py` ... | correct | run `l9 q shadowed random AttributeError` (subprocess; 3.13 appends a renaming hint, 3.12 prints the content's line) |
| `quiz[2].widget.options[0].text` | KEY: `AttributeError: module 'random' has no attribute 'seed'` | correct | as the row above |
| `quiz[2].widget.options[1].why` | Python searches the script's folder first, so it imported your `random.py`, not its own module. | correct | as the row above |
| `quiz[2].widget.options[2].why` | Python did find a module named `random`: yours. The error comes when it looks for `seed` inside it. | correct | as the row above |
| `quiz[2].feedback.correct` | Your `random.py` hid the real module, and it has no `seed`. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. Which `random.py` does Python find first? | correct | as the row above |
| `quiz[2].explain.text` | The script's own folder is searched before the standard library. Your `random.py` was imported instead, and... | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l9 q str repeat` |
| `quiz[3].widget.options[0].text` | KEY: `2.502.502.50` | correct | as the row above |
| `quiz[3].widget.options[1].why` | You expected the hint `price: float` to convert the text. Hints convert nothing. | correct | as the row above |
| `quiz[3].widget.options[2].why` | Python does not check hints. And `3 * "2.50"` is legal: it repeats the text three times. | correct | as the row above |
| `quiz[3].feedback.correct` | The hints were ignored and `3 * "2.50"` repeated the text. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. Python ignores hints at run time; work out `3 * "2.50"`. | correct | as the row above |
| `quiz[3].explain.text` | Type hints are documentation only. The body ran `3 * "2.50"`, which repeats the string three times. Convert... | correct | as the row above |
| `screens[0].widget.answer` | KEY: ["q-p"] | correct | import system: sys.path[0] is the script's folder (docs, sys.path) |

## l10-reading-a-csv.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A price file is plain text: a header line, then one line per day. The table shows the file held in `text`. ... | correct | run `l10 rows` |
| `screens[0].hints[0].text` | The header line is not a day of data. It names the columns. | correct | as the row above |
| `screens[0].hints[1].text` | `rows[0]` is the first day, 11 March. | correct | as the row above |
| `screens[0].hints[2].text` | `rows[2]` is the third day, 13 March, and `["close"]` picks its close. | correct | as the row above |
| `screens[0].feedback.correct` | `rows[2]["close"]` is the close on 13 March: 99.80. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Count the days from 0, leaving out the header line. | correct | as the row above |
| `screens[0].feedback.byKey.r1c1` | You counted the header line as `rows[0]`. The header becomes the keys, so `rows[0]` is 11 March. | correct | as the row above |
| `screens[0].feedback.byKey.r3c1` | That is `rows[3]`, the fourth day. `rows[2]` counts 0, 1, 2 from 11 March, so it is 13 March. | correct | as the row above |
| `screens[0].feedback.byKey.r2c0` | `["close"]` picks the close column. The date sits under the key `"date"`. | correct | as the row above |
| `screens[0].explain.text` | Each line after the header became one dict, keyed by the header names. `rows[2]` is the third day, and `["c... | correct | as the row above |
| `screens[1].prose` | Now look at one whole row. [code] | correct | run `l10 rows`; csv returns every field as str (docs, csv) |
| `screens[1].widget.options[0].text` | KEY: `{'date': '2024-03-11', 'close': '101.20'}` | correct | as the row above |
| `screens[1].widget.options[1].why` | You expected `csv` to turn the close into a number. It gives every value back as text, exactly as written. | correct | as the row above |
| `screens[1].widget.options[2].why` | That is what `csv.reader` gives: a list per line. `DictReader` keys each value by its header. | correct | as the row above |
| `screens[1].widget.options[3].why` | The header line supplies the keys. It is never returned as a row itself. | correct | as the row above |
| `screens[1].hints[0].text` | Does a CSV file record whether `101.20` is a number or text? | correct | as the row above |
| `screens[1].hints[1].text` | This is the row `rows[0]` holds. | correct | as the row above |
| `screens[1].hints[2].text` | The keys come from the header, and every value is the text from the file, trailing zero and all. | correct | as the row above |
| `screens[1].feedback.correct` | A dict keyed by the header, with every value as text. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. The file is text, and `csv` does not guess types. | correct | as the row above |
| `screens[1].explain.text` | Every value comes back as a string, exactly as written, trailing zero included. The `csv` module never gues... | correct | as the row above |
| `screens[2].prose` | Turn the close column into numbers you can calculate with. Read it by name, so the code still works if the ... | correct | run `l10 header only`; harness: solution passes 5 tests |
| `screens[2].widget.how` | Check runs 5 hidden tests. Each passes a whole file as one string, with `\n` between lines. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[2].hints[0].text` | Loop over `csv.DictReader(text.splitlines())`; each row is a dict. | correct | run `l10 header only`; harness: solution passes 5 tests |
| `screens[2].hints[1].text` | The value you want sits under the key `"close"`, as text. | correct | as the row above |
| `screens[2].hints[2].text` | For each row, append `float(row["close"])` to a list, then return the list. | correct | as the row above |
| `screens[2].feedback.correct` | Read by name, converted once, ready to use. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[2].feedback.byKey.test-1` | Test 1 expects floats such as `101.2`. Strings such as `'101.20'` mean the `float(...)` is missing. | correct | as the row above |
| `screens[2].feedback.byKey.test-2` | Test 2 has an extra `open` column. Splitting on commas and taking position 1 reads the open; `row["close"]`... | correct | as the row above |
| `screens[2].explain.text` | `DictReader` handles the header, and `row["close"]` finds the column by name in any position. `float` turns... | correct | as the row above |
| `screens[3].prose` | Another export writes a space after each comma. [code] [code] | correct | run `l10 space kept in key`, `l10 skipinitialspace` |
| `screens[3].widget.options[0].text` | KEY: `KeyError: 'close'` | correct | as the row above |
| `screens[3].widget.options[1].why` | You read the header as `close`. The space after the comma is kept, so the key is `' close'`. | correct | as the row above |
| `screens[3].widget.options[2].why` | Nothing is converted here. The lookup of `'close'` fails before any number is read. | correct | as the row above |
| `screens[3].hints[0].text` | What exactly is the second name in the header line, character by character? | correct | as the row above |
| `screens[3].hints[1].text` | This header has a space before `close`. | correct | as the row above |
| `screens[3].hints[2].text` | The keys are `'date'` and `' close'`. Asking for `'close'` finds nothing, so Python raises `KeyError`. | correct | as the row above |
| `screens[3].feedback.correct` | The key is `' close'`, with its space, so `'close'` is missing. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. Read the header exactly as written, spaces included. | correct | as the row above |
| `screens[3].explain.text` | `csv` keeps every character between the commas, so the key is `' close'`. Pass `skipinitialspace=True` to `... | correct | as the row above |
| `screens[4].prose` | You want the highest close in the file. [code] | correct | run `l10 max text` |
| `screens[4].widget.options[0].text` | KEY: `99.80` | correct | as the row above |
| `screens[4].widget.options[1].why` | You compared the closes as amounts. They are strings, compared character by character, and `'9'` comes afte... | correct | as the row above |
| `screens[4].widget.options[2].why` | That is `max` over floats. These are still the strings from the file. | correct | as the row above |
| `screens[4].widget.options[3].why` | Strings can be compared, so `max` works without an error. It compares text, not amounts. | correct | as the row above |
| `screens[4].hints[0].text` | What type is each `row["close"]`? | correct | as the row above |
| `screens[4].hints[1].text` | Compare these as words, one character at a time, as a dictionary would order them. | correct | as the row above |
| `screens[4].hints[2].text` | `'99.80'` starts with `'9'`, and every other close starts with `'1'`. As text, `'9'` comes last, so it is t... | correct | as the row above |
| `screens[4].feedback.correct` | As text, `'99.80'` beats them all, though it is the lowest price. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. These values are strings. Compare them as text. | correct | as the row above |
| `screens[4].feedback.byKey.number` | You compared amounts, but `max` saw strings. Text compares character by character, and `'9'` beats `'1'`. | correct | as the row above |
| `screens[4].feedback.byKey.float` | No `float` was applied, so `max` saw strings. `'99.80'` wins as text. | correct | as the row above |
| `screens[4].explain.text` | Strings compare letter by letter, so `'9'` beats `'1'` and `'99.80'` is the largest. It is actually the low... | correct | as the row above |
| `screens[5].prose` | UK files often write dates as day/month/year. You sort them as text. [code] | correct | run `l10 text sort`; strptime codes %d %m %Y (docs, datetime) |
| `screens[5].widget.options[0].text` | KEY: `['02/04/2024', '15/03/2024', '28/02/2024']` | correct | as the row above |
| `screens[5].widget.options[1].why` | That is date order. `sorted` compares text character by character, so the day digits decide first. | correct | as the row above |
| `screens[5].widget.options[2].why` | `sorted` does reorder the list. It just orders the strings as text. | correct | as the row above |
| `screens[5].hints[0].text` | Which characters does a text comparison look at first? | correct | as the row above |
| `screens[5].hints[1].text` | The first two characters are the day. | correct | as the row above |
| `screens[5].hints[2].text` | As text, `'02'` < `'15'` < `'28'`, so the order follows the day of the month and ignores the month. | correct | as the row above |
| `screens[5].feedback.correct` | Sorted by the day digits: 2 April lands first. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Sort the strings by their first characters. | correct | as the row above |
| `screens[5].explain.text` | Text sorting ignores what the digits mean. `datetime.strptime("15/03/2024", "%d/%m/%Y")` turns the text int... | correct | as the row above |
| `screens[6].prose` | Fix the sort. Turn each string into a date, sort by the date, and give back the original strings. | correct | run `l10 date sort`, `l10 year end text sort wrong` |
| `screens[6].widget.how` | Check runs 5 hidden tests that compare the list you return. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[6].hints[0].text` | Sort pairs whose first item is the date. Tuples sort by their first item. | correct | run `l10 date sort`, `l10 year end text sort wrong` |
| `screens[6].hints[1].text` | Each string needs `datetime.strptime(d, "%d/%m/%Y")`. | correct | as the row above |
| `screens[6].hints[2].text` | `pairs = sorted((datetime.strptime(d, "%d/%m/%Y"), d) for d in days)`, then return `[d for _, d in pairs]`. | correct | as the row above |
| `screens[6].feedback.correct` | Sorted by real dates: February, March, then April. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[6].feedback.byKey.test-1` | Test 1 expects `['28/02/2024', '15/03/2024', '02/04/2024']`. Plain `sorted(days)` orders by the day digits.... | correct | as the row above |
| `screens[6].explain.text` | Each pair holds a date and its string. Tuples compare first items first, so the pairs sort by date, and the... | correct | as the row above |
| `screens[7].prose` | Everything `csv` reads is text. Convert each field once, as you read it: $$\texttt{float(row["close"])}$$ $... | correct | int('250') = 250; '250' * 1 is still text |
| `screens[7].widget.options[0].text` | KEY: `int(row["qty"])` | correct | as the row above |
| `screens[7].widget.options[1].why` | Multiplying a string by 1 repeats it once. You still have the text `'250'`. | correct | as the row above |
| `screens[7].widget.options[2].why` | `int` needs one field's text, not the whole row dict. | correct | as the row above |
| `screens[7].feedback.correct` | `int` turns the text `'250'` into the number 250. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Convert one field's text with `int`. | correct | as the row above |
| `screens[7].explain.text` | A quantity is a whole number, so `int` fits; a price takes `float`. Convert at the moment you read the row. | correct | as the row above |
| `screens[8].prose` | A data vendor sends closes newest first, with UK dates. A backtest needs daily returns in time order. Anoth... | correct | run `l10 vendor returns`, `l10 vendor dates are consecutive trading days`, `l10 year end text sort wrong` |
| `screens[8].widget.how` | Check runs 4 hidden tests, each a whole file as one string. Returns are compared after rounding to 4 places. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[8].hints[0].text` | Build `(date, close)` pairs, sort them, then walk through neighbours. | correct | run `l10 vendor returns`, `l10 vendor dates are consecutive trading days`, `l10 year end text sort wrong` |
| `screens[8].hints[1].text` | The oldest day is at the bottom of this file. | correct | as the row above |
| `screens[8].hints[2].text` | Append `(datetime.strptime(row["date"], "%d/%m/%Y"), float(row["close"]))` for each row and sort. Then retu... | correct | as the row above |
| `screens[8].feedback.correct` | In time order the returns are [0.004, 0.0159, -0.0039, 0.0148]. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[8].feedback.byKey.test-1` | Test 1 expects `[0.004, 0.0159, -0.0039, 0.0148]`. Sorting the date strings as text puts 1 March before 28 ... | correct | as the row above |
| `screens[8].feedback.byKey.test-2` | Test 2 is the same prices in a jumbled order. Reversing the file only works when it is exactly newest first... | correct | as the row above |
| `screens[8].explain.text` | Sorted by date the closes run £100.00, £100.40, £102.00, £101.60, £103.10. Four days of change give four re... | correct | as the row above |
| `summary.ideas[0]` | `csv.DictReader` turns each line after the header into a dict keyed by the header names. | correct | restates s0 to s6 |
| `summary.ideas[1]` | Every value it gives is text. Convert closes with `float`, quantities with `int` and dates with `datetime.s... | correct | as the row above |
| `summary.ideas[2]` | Text compares character by character, so `'99.80'` beats `'102.50'` and `'02/04/2024'` sorts before `'15/03... | correct | as the row above |
| `summary.formula.tex` | \texttt{float(row["close"])} | correct | as the row above |
| `summary.formula.note` | Each `row` from `csv.DictReader` is a dict of text. `%d/%m/%Y` reads 15/03/2024 and `%Y-%m-%d` reads 2024-0... | correct | as the row above |
| `summary.trap` | `max`, `sorted` and `+` on the raw column work on text. Convert to `float` before you compare, sort or add. | correct | as the row above |
| `quiz[0].prose` | A row from `csv.DictReader` holds `{'date': '2024-03-11', 'close': '101.20'}`. [code] | correct | run `l10 q repeat` |
| `quiz[0].widget.options[0].text` | KEY: `101.20101.20` | correct | as the row above |
| `quiz[0].widget.options[1].why` | You treated the close as a number. It is the string `'101.20'`, and a string times 2 repeats it. | correct | as the row above |
| `quiz[0].widget.options[2].why` | A string times a whole number is legal in Python. It repeats the text. | correct | as the row above |
| `quiz[0].feedback.correct` | The value is text, so `* 2` repeats it. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. What type does `csv` give back? | correct | as the row above |
| `quiz[0].explain.text` | `csv` gives text, and text times 2 is the text twice. `float(row["close"]) * 2` gives `202.4`. | correct | as the row above |
| `quiz[1].prose` | `text` holds a header line, then five lines of prices, then one empty line at the end. [code] | correct | run `l10 q blank line skipped` |
| `quiz[1].widget.answer` | KEY: 5 | correct | as the row above |
| `quiz[1].widget.accept` | 5 | correct | as the row above |
| `quiz[1].widget.wrong[0].value` | SLIP value: 6 | correct | as the row above |
| `quiz[1].widget.wrong[1].value` | SLIP value: 7 | correct | as the row above |
| `quiz[1].feedback.correct` | Five rows: the header gives the keys and the empty line is skipped. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Leave out the header line and the empty line. | correct | as the row above |
| `quiz[1].feedback.byKey.header` | You counted the header line as a row. It supplies the keys, so it is not returned. | correct | as the row above |
| `quiz[1].feedback.byKey.seven` | You counted the header and the empty line. `DictReader` returns neither. | correct | as the row above |
| `quiz[1].explain.text` | The header becomes the keys, and `DictReader` skips completely empty lines. That leaves one dict per price ... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | run `l10 q strptime mismatch` |
| `quiz[2].widget.options[0].text` | KEY: It raises `ValueError` | correct | as the row above |
| `quiz[2].widget.options[1].why` | `strptime` does not guess. The format must match the text exactly, and this text uses dashes, year first. | correct | as the row above |
| `quiz[2].widget.options[2].why` | `strptime` never reads part of a field and moves on. Any mismatch raises an error. | correct | as the row above |
| `quiz[2].feedback.correct` | The format string must match the text exactly. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. Compare the format with the text character by character. | correct | as the row above |
| `quiz[2].explain.text` | `%d/%m/%Y` expects day, slash, month, slash, year. The text starts with a four-digit year and uses dashes, ... | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l10 q ISO sorts`; ISO 8601 fixed-width big-endian dates sort lexicographically |
| `quiz[3].widget.options[0].text` | KEY: `['2024-02-28', '2024-03-15', '2024-04-02']` | correct | as the row above |
| `quiz[3].widget.options[1].why` | `sorted` puts the smallest first, and these strings compare in date order. | correct | as the row above |
| `quiz[3].widget.options[2].why` | You sorted by the day digits. These strings start with the year, then the month. | correct | as the row above |
| `quiz[3].feedback.correct` | Year-month-day text sorts in date order. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. Which characters does the comparison read first here? | correct | as the row above |
| `quiz[3].explain.text` | With the year first, then a two-digit month, then a two-digit day, text order is date order. That is why IS... | correct | as the row above |
| `screens[0].widget.answer` | KEY: ["r2c1"] | correct | run `l10 rows` |

## l11-when-things-go-wrong.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A feed sends closes as text, and one day is missing. [code] | correct | run `l11 float n/a` |
| `screens[0].hints[0].text` | Which of these can `float` not read as a number? | correct | as the row above |
| `screens[0].hints[1].text` | The first two convert without trouble. | correct | as the row above |
| `screens[0].hints[2].text` | `float("n/a")` cannot work, so the program stops on the third value. | correct | as the row above |
| `screens[0].feedback.correct` | `float("n/a")` fails, and the program stops right there. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Find the first value `float` cannot read. | correct | as the row above |
| `screens[0].feedback.byKey.c3` | The loop never reaches `'100.40'`. It stops one value earlier. | correct | as the row above |
| `screens[0].feedback.byKey.c0` | `float("101.20")` is fine: it gives `101.2`. Look further along. | correct | as the row above |
| `screens[0].feedback.byKey.c1` | `float("102.50")` is fine: it gives `102.5`. Look one value further. | correct | as the row above |
| `screens[0].explain.text` | `float("n/a")` raises a `ValueError`. The program stops at once: `'100.40'` is never read and `print` never... | correct | as the row above |
| `screens[1].prose` | Now the risky line sits inside a `try` block, with an `except` block after it. [code] | correct | try/except semantics (Python reference 8.4); three good closes remain |
| `screens[1].widget.options[0].text` | KEY: `skipped n/a`, then `[101.2, 102.5, 100.4]` | correct | as the row above |
| `screens[1].widget.options[1].why` | You expected the loop to end at the error. The `except` deals with it, and the loop carries on to `'100.40'`. | correct | as the row above |
| `screens[1].widget.options[2].why` | The `except` block runs for `'n/a'`, and it contains a `print`. | correct | as the row above |
| `screens[1].widget.options[3].why` | `except ValueError` catches exactly this error, so nothing stops the program. | correct | as the row above |
| `screens[1].hints[0].text` | When `float("n/a")` raises, where does Python go next? | correct | as the row above |
| `screens[1].hints[1].text` | Only this value raises an error. | correct | as the row above |
| `screens[1].hints[2].text` | The `except ValueError` block prints `skipped n/a`. The loop then moves on and converts `'100.40'`. | correct | as the row above |
| `screens[1].feedback.correct` | The bad value is skipped and the loop carries on. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Follow the loop through all four values. | correct | as the row above |
| `screens[1].explain.text` | `try` runs its block. When a `ValueError` is raised inside it, Python jumps to the matching `except` instea... | correct | as the row above |
| `screens[2].prose` | Real feeds hold blanks, dashes and thousands separators. Keep what `float` can read. Anything other than a ... | correct | run `l11 float n/a`, `l11 nan inf readable`, `l11 float(None) TypeError`; harness: solution passes 5 tests |
| `screens[2].widget.how` | Check runs 5 hidden tests. Test 5 passes `None`, which is not text at all: it must raise `TypeError`, not b... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[2].hints[0].text` | Put the `try` inside the loop, around the one line that can fail. | correct | run `l11 float n/a`, `l11 nan inf readable`, `l11 float(None) TypeError`; harness: solution passes 5 tests |
| `screens[2].hints[1].text` | `float` reads `' 99.80 '` but not `''` or `'1,234.50'`. | correct | as the row above |
| `screens[2].hints[2].text` | In the loop: `try:` append `float(p)`, then `except ValueError:` with `pass`. Return the list. | correct | as the row above |
| `screens[2].feedback.correct` | Bad text is skipped, and a real bug such as `None` still stops the program. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[2].feedback.byKey.test-1` | Test 1 expects three closes. If you got fewer, the `try` wraps the whole loop, so the first error ends it. | correct | as the row above |
| `screens[2].feedback.byKey.test-5` | Test 5 expects `TypeError` for `None`. A bare `except:` swallowed it. Name the error: `except ValueError:`. | correct | as the row above |
| `screens[2].explain.text` | `float` ignores spaces around a number, so `' 99.80 '` is `99.8`. A blank or a comma raises `ValueError` an... | correct | as the row above |
| `screens[3].prose` | A close of £0.00 slips into a return calculation. [code] | correct | run `l11 ZeroDivisionError` (message 'float division by zero' on 3.12 and 3.13) |
| `screens[3].widget.options[0].text` | KEY: A traceback ending `ZeroDivisionError: float division by zero` | correct | as the row above |
| `screens[3].widget.options[1].why` | You expected `except ValueError` to catch any error. It catches `ValueError` only, and dividing by zero rai... | correct | as the row above |
| `screens[3].widget.options[2].why` | Python does not return infinity for a division by zero. It raises an exception. | correct | as the row above |
| `screens[3].widget.options[3].why` | An exception raised inside a function travels out to the caller. The `try` there sees it. | correct | as the row above |
| `screens[3].hints[0].text` | Which exception does dividing by zero raise? | correct | as the row above |
| `screens[3].hints[1].text` | This value is the divisor. | correct | as the row above |
| `screens[3].hints[2].text` | `101.20 / 0.00` raises `ZeroDivisionError`. The `except` names `ValueError`, so it does not match and the p... | correct | as the row above |
| `screens[3].feedback.correct` | The `except` names a different error, so this one escapes. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. An `except` catches only the type it names. | correct | as the row above |
| `screens[3].explain.text` | The error is raised inside `ret` and travels out to the `try` around the call. There Python checks each `ex... | correct | as the row above |
| `screens[4].prose` | You can raise an exception yourself when a value makes no sense. [code] | correct | raise / except ... as e; str(e) is the message |
| `screens[4].widget.options[0].text` | KEY: `rejected: qty must be positive` | correct | as the row above |
| `screens[4].widget.options[1].why` | The `if` catches −50 before the `return` line, and `raise` leaves the function at once. | correct | as the row above |
| `screens[4].widget.options[2].why` | `e` is the exception itself. Printing it shows its message, not its type. | correct | as the row above |
| `screens[4].widget.options[3].why` | The caller's `except ValueError` catches what `order` raised, so nothing stops. | correct | as the row above |
| `screens[4].hints[0].text` | Does `order(-50)` ever reach its `return` line? | correct | as the row above |
| `screens[4].hints[1].text` | This size fails the check `qty <= 0`. | correct | as the row above |
| `screens[4].hints[2].text` | `raise` leaves `order` with a `ValueError`. The caller's `except ValueError as e` catches it, and printing ... | correct | as the row above |
| `screens[4].feedback.correct` | `order` raised, the caller caught it, and `e` printed as its message. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. Follow the −50 through the `if`. | correct | as the row above |
| `screens[4].explain.text` | `raise` stops the function and hands the exception to the caller. `except ValueError as e` catches it and n... | correct | as the row above |
| `screens[5].prose` | An order file gives quantities as text. A bad quantity should be refused loudly, not passed on. | correct | run `l11 int text`; harness: solution passes 6 tests |
| `screens[5].widget.how` | Check runs 6 hidden tests. Tests 3 to 6 pass when your function raises `ValueError`. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[5].hints[0].text` | `int(text)` already raises `ValueError` for `'abc'` and `'2.5'`. What is left to check? | correct | run `l11 int text`; harness: solution passes 6 tests |
| `screens[5].hints[1].text` | These two convert fine but are not real order sizes. | correct | as the row above |
| `screens[5].hints[2].text` | `qty = int(text)`, then `if qty <= 0: raise ValueError(...)`, then `return qty`. | correct | as the row above |
| `screens[5].feedback.correct` | Good quantities come back as `int`, and bad ones raise `ValueError`. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[5].feedback.byKey.test-3` | Test 3 expects `ValueError` for `'-40'`. Returning `None` hides the problem from the caller; raise instead. | correct | as the row above |
| `screens[5].feedback.byKey.test-4` | Test 4 expects `ValueError` for `'0'`. An order for zero shares is not an order, so test `qty <= 0`. | correct | as the row above |
| `screens[5].feedback.byKey.test-5` | Test 5 expects `ValueError` for `'abc'`. Let the error from `int` travel out instead of catching it. | correct | as the row above |
| `screens[5].explain.text` | `int` does half the work: it raises for `'abc'` and `'2.5'` and strips the spaces from `' 40 '`. Your `rais... | correct | as the row above |
| `screens[6].prose` | This version uses a bare `except`, which names no error. It prints `[]`, with no error message at all. [code] | correct | run `l11 typo surfaces as NameError`; the call is on line 5 of the listing |
| `screens[6].widget.options[0].text` | KEY: `flaot` is a typo, and `except` hides its error | correct | as the row above |
| `screens[6].widget.options[1].why` | Strings can go in a list. Nothing was appended because the `append` line raised an error every time. | correct | as the row above |
| `screens[6].widget.options[2].why` | `pass` does nothing at all. The `except` ran for every price, so an error happened every time. | correct | as the row above |
| `screens[6].widget.options[3].why` | `float("101.20")` works. The function called here is `flaot`, which does not exist. | correct | as the row above |
| `screens[6].hints[0].text` | Read the line inside `try` slowly, letter by letter. | correct | as the row above |
| `screens[6].hints[1].text` | Each of these is a valid number, yet none was kept. | correct | as the row above |
| `screens[6].hints[2].text` | `flaot` is not defined, so every call raises `NameError`. The bare `except` catches it, and `pass` throws i... | correct | as the row above |
| `screens[6].feedback.correct` | The typo raised `NameError` every time, and the bare `except` hid it. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Look for an error the bare `except` could be hiding. | correct | as the row above |
| `screens[6].feedback.byKey.strings` | You blamed the data type. The values never reached the list, because the line raised a `NameError` each time. | correct | as the row above |
| `screens[6].feedback.byKey.pass` | You blamed `pass`. It does nothing; the real problem is the error it silently ignored on every value. | correct | as the row above |
| `screens[6].feedback.byKey.data` | You blamed the data. These are fine numbers; the misspelt `flaot` failed on all of them. | correct | as the row above |
| `screens[6].explain.text` | A bare `except` catches every error, including your own typos. Here the `NameError` for `flaot` hit every p... | correct | as the row above |
| `screens[7].prose` | Catch only what you expect, around only the line that can fail: $$\texttt{try:}\ \textit{risky line} \qquad... | correct | missing key raises KeyError (docs, Mapping Types) |
| `screens[7].widget.options[0].text` | KEY: `except KeyError:` | correct | as the row above |
| `screens[7].widget.options[1].why` | A bare `except` would also hide typos and every other bug in the block. | correct | as the row above |
| `screens[7].widget.options[2].why` | A missing dict key raises `KeyError`, so this `except` would not catch it. | correct | as the row above |
| `screens[7].feedback.correct` | A missing key raises `KeyError`, so name exactly that. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Which exception does a missing dict key raise? | correct | as the row above |
| `screens[7].explain.text` | Looking up a key that is not there raises `KeyError`. Naming it catches the unknown ticker and nothing else. | correct | as the row above |
| `screens[8].prose` | An order file has one `TICKER,QTY` line per order. Rejected lines are counted for the morning report. `pars... | correct | run `l11 unpack split`, `l11 None.split AttributeError`; harness: solution passes 5 tests |
| `screens[8].widget.how` | Check runs 5 hidden tests. Test 5 includes `None` where a line should be: that is a bug upstream and must n... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[8].hints[0].text` | Both the split and `parse_qty` can raise `ValueError`. Put both inside the `try`. | correct | run `l11 unpack split`, `l11 None.split AttributeError`; harness: solution passes 5 tests |
| `screens[8].hints[1].text` | This line has no comma, so unpacking it into two names fails. | correct | as the row above |
| `screens[8].hints[2].text` | In the loop: `try:` then `ticker, text = line.split(",")` and append `(ticker, parse_qty(text))`. In `excep... | correct | as the row above |
| `screens[8].feedback.correct` | Two good orders, three rejected lines, and a real bug still stops the program. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[8].feedback.byKey.test-1` | Test 1 expects `([('VOD', 250), ('AZN', 15)], 3)`. A crash on `'HSBA'` means the split sits outside the `try`. | correct | as the row above |
| `screens[8].feedback.byKey.test-5` | Test 5 expects `AttributeError` for `None`. A bare `except:` counted the bug as a rejected line. | correct | as the row above |
| `screens[8].explain.text` | `'HSBA'` splits into one piece, and unpacking one piece into two names raises `ValueError` too. So does `'S... | correct | as the row above |
| `summary.ideas[0]` | An exception stops the program at the line that raised it, unless a `try` around that line has a matching `... | correct | restates s0 to s7 |
| `summary.ideas[1]` | `raise ValueError("why")` refuses a value that makes no sense, and the caller decides what to do about it. | correct | as the row above |
| `summary.ideas[2]` | Name the exception you expect. A bare `except` also swallows `NameError`, `TypeError` and every other bug. | correct | as the row above |
| `summary.formula.tex` | \texttt{try:}\ \textit{risky line}\qquad\texttt{except ValueError:}\ \textit{handle it} | correct | as the row above |
| `summary.formula.note` | An `except` catches only the types it names. Anything else still stops the program, which is what you want ... | correct | as the row above |
| `summary.trap` | A bare `except:` hides typos. The code runs, returns nonsense, and never tells you why. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l11 int text` |
| `quiz[0].widget.options[0].text` | KEY: `ValueError` | correct | as the row above |
| `quiz[0].widget.options[1].why` | You expected `int` to drop the decimals. That happens for `int(12.5)`, a number, but not for the text `'12.... | correct | as the row above |
| `quiz[0].widget.options[2].why` | `int` never rounds. And from text with a decimal point it raises an error. | correct | as the row above |
| `quiz[0].widget.options[3].why` | `int` never gives a decimal. It returns a whole number or raises an error. | correct | as the row above |
| `quiz[0].feedback.correct` | `int` reads only whole-number text. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. Can `int` read text with a decimal point? | correct | as the row above |
| `quiz[0].explain.text` | `int("12.5")` raises `ValueError`, because the text is not a whole number. `int(float("12.5"))` gives 12. | correct | as the row above |
| `quiz[1].prose` | [code] | correct | ValueError: right type, inappropriate value (docs, Built-in Exceptions) |
| `quiz[1].widget.options[0].text` | KEY: `KeyError` | correct | as the row above |
| `quiz[1].widget.options[1].why` | `ValueError` is for a value of the right type that makes no sense. A missing key raises `KeyError`. | correct | as the row above |
| `quiz[1].widget.options[2].why` | `IndexError` is for a list position past the end. Dicts are looked up by key. | correct | as the row above |
| `quiz[1].widget.options[3].why` | Square brackets never return `None` for a missing key. `prices.get("BARC")` would. | correct | as the row above |
| `quiz[1].feedback.correct` | A missing dict key raises `KeyError`. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. What goes wrong is a lookup by key. | correct | as the row above |
| `quiz[1].explain.text` | `"BARC"` is not a key, so the lookup raises `KeyError: 'BARC'`. Catch it with `except KeyError:` or use `pr... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | 125/100 - 1 = 0.25; first call caught |
| `quiz[2].widget.options[0].text` | KEY: `None 0.25` | correct | as the row above |
| `quiz[2].widget.options[1].why` | The `except ZeroDivisionError` inside `ret` catches it and returns `None`. | correct | as the row above |
| `quiz[2].widget.options[2].why` | Catching the first error does not stop the program. The second call runs normally. | correct | as the row above |
| `quiz[2].widget.options[3].why` | The `except` block returns `None`, not 0. | correct | as the row above |
| `quiz[2].feedback.correct` | The first call is caught and returns `None`; the second gives 0.25. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. Run each call separately. | correct | as the row above |
| `quiz[2].explain.text` | The first call divides by zero, and the `except` returns `None`. The second gives $125.00 / 100.00 - 1 = 0.... | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l11 q qty 0` (subprocess) |
| `quiz[3].widget.options[0].text` | KEY: `0` | correct | as the row above |
| `quiz[3].widget.options[1].why` | `qty` was 40 for a moment. Then `float("£7.25")` raised, and the `except` set `qty` to 0. | correct | as the row above |
| `quiz[3].widget.options[2].why` | The `except ValueError` catches the error from `float`. | correct | as the row above |
| `quiz[3].feedback.correct` | The error on line 3 sent Python to the `except`, which set `qty` to 0. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. Which line raises, and what does the `except` do? | correct | as the row above |
| `quiz[3].explain.text` | `int("40")` worked, but the `£` sign makes `float` raise. Python jumps to `except` and sets `qty = 0`. This... | correct | as the row above |
| `screens[0].widget.answer` | KEY: ["c2"] | correct | run `l11 float n/a` |

## l12-data-with-behaviour.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].prose` | A position is a few facts that belong together. This **class** bundles them. [code] | correct | class instantiation calls __init__ (Python reference 3.3.1) |
| `screens[0].hints[0].text` | The name before the dot picks the object. The name after it picks the value. | correct | as the row above |
| `screens[0].hints[1].text` | This row is the object `azn`. | correct | as the row above |
| `screens[0].hints[2].text` | `azn` was made with `Position("AZN", 40, 104.20)`, so its `qty` is 40. | correct | as the row above |
| `screens[0].feedback.correct` | `azn.qty` is 40, stored by `self.qty = qty`. | correct | as the row above |
| `screens[0].feedback.generic` | Not quite right. Find the row for `azn`, then the column `qty`. | correct | as the row above |
| `screens[0].feedback.byKey.r0c2` | That is `shel.qty`. The name before the dot picks the object: `azn`. | correct | as the row above |
| `screens[0].feedback.byKey.r1c3` | That is `azn.avg_price`. The name after the dot picks the value: `qty`. | correct | as the row above |
| `screens[0].feedback.byKey.r1c1` | That is `azn.ticker`. Look one column to the right, under `qty`. | correct | as the row above |
| `screens[0].explain.text` | `Position("AZN", 40, 104.20)` made a new object, an **instance** of the class. `__init__` ran and stored ea... | correct | as the row above |
| `screens[1].prose` | A class can also carry behaviour: functions written inside it, called **methods**. This one sits inside `Po... | correct | run `l12 value` |
| `screens[1].widget.options[0].text` | KEY: `4050.0` | correct | as the row above |
| `screens[1].widget.options[1].why` | You used the average price, £26.40. `value` multiplies by the price you pass in, £27.00. | correct | as the row above |
| `screens[1].widget.options[2].why` | That is the profit, $150 \times (27.00 - 26.40)$. `value` is the quantity times today's price. | correct | as the row above |
| `screens[1].widget.options[3].why` | You expected to pass `self` yourself. Python passes `shel` as `self`, so `27.00` lands in `price`. | correct | as the row above |
| `screens[1].hints[0].text` | Which object is `self` in this call? | correct | as the row above |
| `screens[1].hints[1].text` | `self` is this object. | correct | as the row above |
| `screens[1].hints[2].text` | `self` is `shel`, so `self.qty` is 150. The method returns $150 \times 27.00$. | correct | as the row above |
| `screens[1].feedback.correct` | 150 shares at £27.00 are worth £4,050.00. | correct | as the row above |
| `screens[1].feedback.generic` | Not quite right. Work out which object `self` is, then multiply. | correct | as the row above |
| `screens[1].explain.text` | `shel.value(27.00)` runs `value` with `self` set to `shel` and `price` set to 27.00. So `self.qty` is 150, ... | imprecise | Finding 5. In Position.value(shel, 27.00), shown on screen 7, the object before the dot is the class and the first parameter is shel; run `l12 value` |
| `screens[2].prose` | Now write the class yourself. Add `pnl(price)`, the profit since you bought: $q \times (p - \bar{p})$, wher... | correct | run `l12 pnl` (the three exact floats in the tests); unrealised P&L q(p - avg), negative q for a short |
| `screens[2].widget.how` | Check runs 7 hidden tests. Money is compared with `math.isclose`, so 90.00000000000021 counts as 90.0. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[2].hints[0].text` | Store each argument on the object in `__init__`, then use `self.` to read it in the methods. | correct | run `l12 pnl` (the three exact floats in the tests); unrealised P&L q(p - avg), negative q for a short |
| `screens[2].hints[1].text` | A short position: `qty` is negative, so a falling price makes money. | correct | as the row above |
| `screens[2].hints[2].text` | `__init__` sets `self.ticker`, `self.qty` and `self.avg_price`. `value` returns `self.qty * price`; `pnl` r... | correct | as the row above |
| `screens[2].feedback.correct` | SHEL shows £90.00 profit, AZN a £108.00 loss, and the BARC short a £25.00 profit. | correct | as the row above |
| `screens[2].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[2].feedback.byKey.test-1` | Test 1 reads `.ticker`. An `AttributeError` means `__init__` did not store it: write `self.ticker = ticker`. | correct | as the row above |
| `screens[2].feedback.byKey.test-4` | Test 4 expects 90.0 for SHEL bought at £26.40 and now £27.00. Subtract the average price from today's price. | correct | as the row above |
| `screens[2].explain.text` | Every method reaches the stored facts through `self`. The BARC short gains as the price falls: $-500 \times... | correct | as the row above |
| `screens[3].prose` | You print a position to check it. [code] | correct | run `l12 default repr` |
| `screens[3].widget.options[0].text` | KEY: Something like `<__main__.Position object at 0x7f3a2c1b9d50>` | correct | as the row above |
| `screens[3].widget.options[1].why` | Python cannot guess how you want your object shown. By default it prints the class name and a memory address. | correct | as the row above |
| `screens[3].widget.options[2].why` | An object is not a dict. By default Python shows only its class and where it lives in memory. | correct | as the row above |
| `screens[3].hints[0].text` | Has the class told Python how to show a `Position` as text? | correct | as the row above |
| `screens[3].hints[1].text` | Python knows these values, but not how you want them shown. | correct | as the row above |
| `screens[3].hints[2].text` | With no instructions, Python prints the class name and a memory address. | correct | as the row above |
| `screens[3].feedback.correct` | Without instructions, Python shows the class and an address. | correct | as the row above |
| `screens[3].feedback.generic` | Not quite right. The class has not said how to show itself. | correct | as the row above |
| `screens[3].explain.text` | Python asks an object for its text by calling its `__repr__` method. The default one shows the class and a ... | correct | as the row above |
| `screens[4].prose` | Give `Position` a readable `__repr__`. It must **return** a string, not print one. Format the price with `{... | correct | run `l12 repr must return str`; str() falls back to __repr__, containers use repr (docs, object.__repr__) |
| `screens[4].widget.how` | Check runs 4 hidden tests. Test 4 shows a list of positions, which uses `__repr__` for each one. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[4].hints[0].text` | An f-string builds the text. `return` hands it back. | correct | run `l12 repr must return str`; str() falls back to __repr__, containers use repr (docs, object.__repr__) |
| `screens[4].hints[1].text` | `26.4` must show as `26.40`, and `0.5` as `0.50`. | correct | as the row above |
| `screens[4].hints[2].text` | `return f"Position({self.ticker}, {self.qty} @ £{self.avg_price:.2f})"` | correct | as the row above |
| `screens[4].feedback.correct` | Positions now show themselves, alone and inside lists. | correct | as the row above |
| `screens[4].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[4].feedback.byKey.test-1` | Test 1 expects `'Position(SHEL, 150 @ £26.40)'`. `£26.4` means the `:.2f` is missing. A `TypeError` about a... | correct | as the row above |
| `screens[4].explain.text` | `__repr__` returns the text Python shows for the object. `:.2f` keeps two decimal places, as prices need. `... | correct | as the row above |
| `screens[5].prose` | A colleague writes `__init__` without `self.`: [code] | correct | run `l12 no self AttributeError` (exact message) |
| `screens[5].widget.options[0].text` | KEY: `AttributeError: 'Position' object has no attribute 'qty'` | correct | as the row above |
| `screens[5].widget.options[1].why` | You expected `qty = qty` to store the value on the object. Without `self.` it only sets a local name, gone ... | correct | as the row above |
| `screens[5].widget.options[2].why` | Python does not fill missing attributes with `None`. Reading one that was never set raises an error. | correct | as the row above |
| `screens[5].widget.options[3].why` | `shel.qty` asks the object for an attribute, so a failure is an `AttributeError`, not a `NameError`. | correct | as the row above |
| `screens[5].hints[0].text` | Which of these lines puts anything on the object `self`? | correct | as the row above |
| `screens[5].hints[1].text` | These are local names. They vanish when `__init__` returns. | correct | as the row above |
| `screens[5].hints[2].text` | `qty = qty` reassigns a local name to itself. Nothing is stored on `self`, so `shel.qty` does not exist. | correct | as the row above |
| `screens[5].feedback.correct` | Nothing was stored on the object, so `shel.qty` does not exist. | correct | as the row above |
| `screens[5].feedback.generic` | Not quite right. Ask what `qty = qty` changes. | correct | as the row above |
| `screens[5].feedback.byKey.stored` | You expected `qty = qty` to store 150 on the object. It only reassigns a local name, which disappears when ... | correct | as the row above |
| `screens[5].feedback.byKey.none` | You expected a missing attribute to read as `None`. Python raises `AttributeError` instead. | correct | as the row above |
| `screens[5].feedback.byKey.name` | The lookup is on the object, `shel.qty`, so the error is `AttributeError`. | correct | as the row above |
| `screens[5].explain.text` | Inside `__init__`, `qty` is just a local name, like any parameter. Only `self.qty = qty` attaches the value... | correct | as the row above |
| `screens[6].prose` | A first try at a trading book keeps its list in the class body. [code] | correct | run `l12 class-body list shared` |
| `screens[6].widget.options[0].text` | KEY: `1` | correct | as the row above |
| `screens[6].widget.options[1].why` | You expected each book to get its own list. `trades = []` runs once, when the class is made, so every book ... | correct | as the row above |
| `screens[6].widget.options[2].why` | `yours` has no `trades` of its own, so Python looks in the class and finds the shared list there. | correct | as the row above |
| `screens[6].hints[0].text` | How many times does the line `trades = []` run? | correct | as the row above |
| `screens[6].hints[1].text` | Neither book stores a list of its own. Both look it up in the class. | correct | as the row above |
| `screens[6].hints[2].text` | One list lives on the class. `mine.add` appends to it, and `yours.trades` is the same list, so its length i... | correct | as the row above |
| `screens[6].feedback.correct` | Both books share the one list in the class. | correct | as the row above |
| `screens[6].feedback.generic` | Not quite right. Count how many lists exist. | correct | as the row above |
| `screens[6].explain.text` | `trades = []` in the class body runs once, so there is one list on the class. `self.trades` finds it throug... | correct | as the row above |
| `screens[7].prose` | You have seen what a method call does. Python passes the object before the dot as the first argument: $$\te... | correct | run `l12 value` (Position.value(shel, 27.00) == shel.value(27.00)), `l12 missing arg`; 40 x (101.50 - 104.20) = -108 |
| `screens[7].widget.options[0].text` | KEY: `Position.pnl(azn, 101.50)` | correct | as the row above |
| `screens[7].widget.options[1].why` | That leaves out the object. `101.50` would land in `self`, and `price` would be missing. | correct | as the row above |
| `screens[7].widget.options[2].why` | `pnl` lives inside the class. There is no plain name `pnl` outside it. | correct | as the row above |
| `screens[7].feedback.correct` | The object before the dot becomes `self`. | correct | as the row above |
| `screens[7].feedback.generic` | Not quite right. Put the object in as the first argument. | correct | as the row above |
| `screens[7].explain.text` | `azn.pnl(101.50)` becomes `Position.pnl(azn, 101.50)`, so `self` is `azn` and `price` is 101.50. It returns... | correct | as the row above |
| `screens[8].prose` | A trading book records fills and nets them by ticker. Buys have positive `qty`, sells negative. The type hi... | correct | run `l12 cash` (-420.0 and -4258.0); harness: solution passes 7 tests |
| `screens[8].widget.how` | Check runs 7 hidden tests. Each builds a fresh `Book`, adds trades, then reads the last value. Test 2 check... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `screens[8].hints[0].text` | Give each `Book` its own list in `__init__`. `add` appends to it. | correct | run `l12 cash` (-420.0 and -4258.0); harness: solution passes 7 tests |
| `screens[8].hints[1].text` | These two VOD fills net to 600 shares. | correct | as the row above |
| `screens[8].hints[2].text` | `net` adds `t.qty` for each trade whose `t.ticker` matches. `cash` adds `t.qty * t.price` over all trades a... | correct | as the row above |
| `screens[8].feedback.correct` | VOD nets to 600 shares, and the book paid out £420.00 net. | correct | as the row above |
| `screens[8].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `screens[8].feedback.byKey.test-2` | Test 2 adds AZN to one book and asks another. A list written in the class body is shared; create it in `__i... | correct | as the row above |
| `screens[8].feedback.byKey.test-3` | Test 3 asks for BARC, which this book never traded, and expects 0. Count only the trades whose `ticker` mat... | correct | as the row above |
| `screens[8].feedback.byKey.test-4` | Test 4 expects −420.0: buying spends cash, so the sign is negative. Return `round(-total, 2)`. | correct | as the row above |
| `screens[8].explain.text` | Buying 1,000 VOD at £0.72 spends £720.00, and selling 400 at £0.75 brings back £300.00. So `net("VOD")` is ... | correct | as the row above |
| `summary.ideas[0]` | A class bundles data with the functions that use it. `__init__` stores each value on the new object as `sel... | correct | restates s0 to s7 |
| `summary.ideas[1]` | `obj.method(x)` runs `Class.method(obj, x)`: the object before the dot arrives as `self`. `__repr__` decide... | correct | as the row above |
| `summary.ideas[2]` | Create lists in `__init__`. A list written in the class body is shared by every instance. | correct | as the row above |
| `summary.formula.tex` | \texttt{shel.value(27.00)} = \texttt{Position.value(shel, 27.00)} | correct | as the row above |
| `summary.formula.note` | So `def value(self, price):` needs `self` first, and `self.qty` reads this object's quantity. | correct | as the row above |
| `summary.trap` | `qty = qty` inside `__init__` stores nothing on the object. Write `self.qty = qty`. | correct | as the row above |
| `quiz[0].prose` | [code] | correct | run `l12 q missing self TypeError` |
| `quiz[0].widget.options[0].text` | KEY: A `TypeError`: `value` gets one argument too many | correct | as the row above |
| `quiz[0].widget.options[1].why` | The method has no `self` parameter. Python still passes the object, so two arguments arrive for one slot. | correct | as the row above |
| `quiz[0].widget.options[2].why` | The call fails before the body runs. Python passes two arguments to a method that accepts one. | correct | as the row above |
| `quiz[0].feedback.correct` | The object arrives as an extra argument, and `value` has no slot for it. | correct | as the row above |
| `quiz[0].feedback.generic` | Not quite right. Count the arguments Python passes to `value`. | correct | as the row above |
| `quiz[0].explain.text` | `Position(10).value(5.00)` passes the object and 5.00, but `value(price)` takes one argument. Write `def va... | correct | as the row above |
| `quiz[1].prose` | [code] | correct | names bind to one object (same as l8 s0) |
| `quiz[1].widget.options[0].text` | KEY: `300` | correct | as the row above |
| `quiz[1].widget.options[1].why` | You expected `b = a` to copy the position. It gives the same object a second name, so changing `b.qty` chan... | correct | as the row above |
| `quiz[1].widget.options[2].why` | `b` is the same object as `a`, and it has a `qty`. | correct | as the row above |
| `quiz[1].feedback.correct` | `a` and `b` name one object. | correct | as the row above |
| `quiz[1].feedback.generic` | Not quite right. Does `b = a` make a new object? | correct | as the row above |
| `quiz[1].explain.text` | `b = a` copies no data: both names point at the one `Position`. Setting `b.qty` changes that object, so `a.... | correct | as the row above |
| `quiz[2].prose` | [code] | correct | run `l12 class-body list shared` (same behaviour) |
| `quiz[2].widget.options[0].text` | KEY: `['urgent', 'small']` | correct | as the row above |
| `quiz[2].widget.options[1].why` | You expected each order to have its own list. `tags = []` sits in the class body, so both orders append to ... | correct | as the row above |
| `quiz[2].widget.options[2].why` | `__init__` appends each tag. Both appends land in the class's single list. | correct | as the row above |
| `quiz[2].feedback.correct` | One list on the class, shared by both orders. | correct | as the row above |
| `quiz[2].feedback.generic` | Not quite right. How many `tags` lists exist? | correct | as the row above |
| `quiz[2].explain.text` | The class body runs once, so there is one `tags` list. Each `__init__` appends to it. Create the list with ... | correct | as the row above |
| `quiz[3].prose` | [code] | correct | run `l12 q list uses repr` |
| `quiz[3].widget.options[0].text` | KEY: `[VOD x100, AZN x40]` | correct | as the row above |
| `quiz[3].widget.options[1].why` | The list shows each item's `__repr__` text as it is. The quotes appear only when the items are strings. | correct | as the row above |
| `quiz[3].widget.options[2].why` | The class defines `__repr__`, and lists use it for every item. | correct | as the row above |
| `quiz[3].feedback.correct` | The list used each position's `__repr__`. | correct | as the row above |
| `quiz[3].feedback.generic` | Not quite right. What does a list use to show its items? | correct | as the row above |
| `quiz[3].explain.text` | A list shows each item with `__repr__`. Here that returns `VOD x100` and `AZN x40`, placed inside the brack... | correct | as the row above |
| `screens[0].widget.answer` | KEY: ["r1c2"] | correct | class instantiation calls __init__ (Python reference 3.3.1) |

## review-3.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | [code] | correct | run `r3 sqrt` |
| `items[0].widget.options[0].text` | KEY: `True` | correct | as the row above |
| `items[0].widget.options[1].why` | `import math` on the first line creates `math`. The second line adds `sqrt` beside it. | correct | as the row above |
| `items[0].widget.options[2].why` | `from math import sqrt` creates the name `sqrt`. Both lines run, so both names exist. | correct | as the row above |
| `items[0].widget.options[3].why` | Both names reach the same function, so both calls give 1.5. | correct | as the row above |
| `items[0].feedback.correct` | Both import forms ran, so both names exist. | correct | as the row above |
| `items[0].feedback.generic` | Not quite right. List the names each import line creates. | correct | as the row above |
| `items[0].explain.text` | Each import line creates its own name: `import math` gives `math`, and `from math import sqrt` gives `sqrt`... | correct | as the row above |
| `items[1].prose` | `rows` came from `csv.DictReader` over a price file. [code] | correct | run `r3 sum of str` (exact message) |
| `items[1].widget.options[0].text` | KEY: `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | correct | as the row above |
| `items[1].widget.options[1].why` | You treated the closes as numbers. `csv` gives text, and `sum` cannot add text to its starting 0. | correct | as the row above |
| `items[1].widget.options[2].why` | `sum` starts from the number 0, and `0 + '101.20'` is an error. It never joins strings. | correct | as the row above |
| `items[1].feedback.correct` | `sum` starts at 0 and cannot add a string to it. | correct | as the row above |
| `items[1].feedback.generic` | Not quite right. What type is each close, and what does `sum` start from? | correct | as the row above |
| `items[1].explain.text` | Every value from `csv` is a string. `sum` starts at 0, and `0 + '101.20'` raises `TypeError`. Write `sum(fl... | correct | as the row above |
| `items[2].prose` | [code] | correct | instance attributes are per object |
| `items[2].widget.options[0].text` | KEY: `150 100` | correct | as the row above |
| `items[2].widget.options[1].why` | You expected two equal positions to share their data. Each `Position(...)` call makes a new object with its... | correct | as the row above |
| `items[2].widget.options[2].why` | `p.qty += 50` changes the `qty` stored on `p`. It does take effect. | correct | as the row above |
| `items[2].feedback.correct` | Two separate objects, each with its own `qty`. | correct | as the row above |
| `items[2].feedback.generic` | Not quite right. How many objects did the code make? | correct | as the row above |
| `items[2].explain.text` | `self.qty = qty` in `__init__` puts a separate `qty` on each object. Changing `p.qty` leaves `q` alone. Onl... | correct | as the row above |
| `items[3].prose` | The closes in `rows` are `'101.20'`, `'99.80'`, `'100.40'`, `'98.75'` and `'102.50'`, straight from `csv`. ... | correct | run `r3 text compare count` (5 as text, 3 as numbers) |
| `items[3].widget.answer` | KEY: 5 | correct | as the row above |
| `items[3].widget.accept` | 5 | correct | as the row above |
| `items[3].widget.wrong[0].value` | SLIP value: 3 | correct | as the row above |
| `items[3].feedback.correct` | All five pass, because the comparison is between strings. | correct | as the row above |
| `items[3].feedback.generic` | Not quite right. Compare each close with `"100"` as text, character by character. | correct | as the row above |
| `items[3].feedback.byKey.numbers` | You compared amounts: three closes are above £100. These are strings, and `'99.80'` and `'98.75'` beat `'10... | correct | as the row above |
| `items[3].explain.text` | Text compares character by character. `'9'` beats `'1'`, and `'100.40'` beats `'100'` because it is longer ... | correct | as the row above |
| `items[4].prose` | [code] The file's header is `date,close`, and every close is a valid number. | correct | KeyError on every row, swallowed by bare except |
| `items[4].widget.options[0].text` | KEY: `[]` | correct | as the row above |
| `items[4].widget.options[1].why` | The key is spelt `"Close"`, but the header says `close`. Every lookup raises `KeyError`. | correct | as the row above |
| `items[4].widget.options[2].why` | The bare `except` catches the `KeyError` on every row and throws it away. Nothing is reported. | correct | as the row above |
| `items[4].feedback.correct` | Every row raised `KeyError`, and the bare `except` hid it. | correct | as the row above |
| `items[4].feedback.generic` | Not quite right. Compare the key in the code with the header. | correct | as the row above |
| `items[4].explain.text` | Keys are case-sensitive, so `row["Close"]` raises `KeyError` on every row. The bare `except` swallows it, l... | correct | as the row above |
| `items[5].prose` | A price file has a `close` column among others. Use `csv.DictReader` and the `statistics` module. | correct | run `r3 average` (sum 507.00, mean 101.40) |
| `items[5].widget.how` | Check runs 3 hidden tests, each a whole file as one string. The mean is compared after rounding to 2 places. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[5].feedback.correct` | The five closes average £101.40. | correct | run `r3 average` (sum 507.00, mean 101.40) |
| `items[5].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `items[5].feedback.byKey.test-2` | Test 2 has `open` before `close`, and expects 0.74. Read the column by its name, `row["close"]`. | correct | as the row above |
| `items[5].explain.text` | Convert each `row["close"]` with `float`, then `mean` from `statistics` does the rest. The five closes sum ... | correct | as the row above |
| `items[6].prose` | A ticker missing from today's price dict should give `None`, but every other error should still stop the pr... | correct | run `r3 list key TypeError`; harness: solution passes 4 tests |
| `items[6].widget.how` | Check runs 4 hidden tests. Test 4 passes a list as the ticker, a bug that must raise `TypeError` rather tha... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[6].feedback.correct` | A missing ticker gives `None`, and a real bug still raises. | correct | run `r3 list key TypeError`; harness: solution passes 4 tests |
| `items[6].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `items[6].feedback.byKey.test-2` | Test 2 asks for BARC, which is not in the dict, and expects `None`. Catch the `KeyError` and return `None`. | correct | as the row above |
| `items[6].feedback.byKey.test-4` | Test 4 expects `TypeError` for a list ticker. A bare `except` returned `None` and hid the bug. | correct | as the row above |
| `items[6].explain.text` | Only a missing key is expected, so only `KeyError` is caught. A list as a key is a bug elsewhere, and its `... | correct | as the row above |
| `items[7].prose` | You are about to save a new script in your project folder. | correct | same search-order rule as l9 s7 |
| `items[7].widget.options[0].text` | KEY: `read_prices.py` | correct | as the row above |
| `items[7].widget.options[1].why` | Then `import csv` finds your own file, which has no `DictReader`. | correct | as the row above |
| `items[7].widget.options[2].why` | Then `import random` finds your own file, and `random.seed` is missing. | correct | as the row above |
| `items[7].widget.options[3].why` | Python searches the script's folder first, so a clashing name hides the real module. | correct | as the row above |
| `items[7].feedback.correct` | `read_prices.py` clashes with no module you import. | correct | as the row above |
| `items[7].feedback.generic` | Not quite right. Which names match a module the script imports? | correct | as the row above |
| `items[7].explain.text` | The script's folder is searched before the standard library. A script named `csv.py` or `random.py` would b... | correct | as the row above |
| `items[8].prose` | Buying more shares changes the average price: $\bar{p}_{\text{new}} = \dfrac{q\,\bar{p} + q'\,p'}{q + q'}$,... | correct | run `r3 avg price` (3975 / 150 = 26.50; plain average would be 26.75); weighted average cost |
| `items[8].widget.how` | Check runs 4 hidden tests. Each makes a position, calls `buy`, then reads `qty` or `avg_price`. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[8].feedback.correct` | 100 at £26.00 and 50 at £27.50 average to £26.50. | correct | run `r3 avg price` (3975 / 150 = 26.50; plain average would be 26.75); weighted average cost |
| `items[8].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `items[8].feedback.byKey.test-2` | Test 2 expects 26.5. Work out the total cost with the old quantity before you change `self.qty`. A plain av... | correct | as the row above |
| `items[8].explain.text` | Total cost is $100 \times 26.00 + 50 \times 27.50 = 3975$ for 150 shares, so the average is £26.50. Compute... | correct | as the row above |

## homework-3.json

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].prose` | Log returns add up over time, which makes them handy for risk work. The log return from $p_{t-1}$ to $p_t$ ... | unverified | Additivity is correct (Tsay s. 1.1; run `hw3 log returns`); 'handy for risk work' is an unsourced usage remark |
| `items[0].widget.how` | Check runs 4 hidden tests. Each return is compared after rounding to 6 places. | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[0].feedback.correct` | Four log returns, and they add up to the log of the whole move. | correct | run `hw3 log returns`; log returns are time-additive: sum ln(p_t/p_{t-1}) = ln(p_T/p_0) (Tsay, Analysis of Financial Time Series, s. 1.1) |
| `items[0].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `items[0].feedback.byKey.test-1` | Test 1 expects log returns. Simple returns such as 0.012 mean you skipped `math.log`; a `NameError` means `... | correct | as the row above |
| `items[0].feedback.byKey.test-2` | Test 2 doubles then halves the price. The log returns are equal and opposite, $\pm 0.693147$. | correct | as the row above |
| `items[0].explain.text` | The returns sum to $\ln(103.10 / 100.00) = 0.030529$, the log of the whole move. That is why log returns ar... | correct | as the row above |
| `items[1].prose` | A broker's file stamps each fill like `2024-03-15 16:30`. | correct | run `hw3 strptime`; %Y %m %d %H %M (docs, datetime) |
| `items[1].widget.options[0].text` | KEY: `"%Y-%m-%d %H:%M"` | correct | as the row above |
| `items[1].widget.options[1].why` | You swapped day and month. In `2024-03-15` the month comes before the day. | correct | as the row above |
| `items[1].widget.options[2].why` | `%y` is a two-digit year such as 24. A four-digit year needs `%Y`. | correct | as the row above |
| `items[1].widget.options[3].why` | `%m` is the month in every position. Minutes are `%M`. | correct | as the row above |
| `items[1].feedback.correct` | Year, month, day, then hours and minutes. | correct | as the row above |
| `items[1].feedback.generic` | Not quite right. Match each field to its code: `%Y`, `%m`, `%d`, `%H`, `%M`. | correct | as the row above |
| `items[1].explain.text` | `%Y` is the four-digit year, `%m` the month, `%d` the day, `%H` the hour and `%M` the minute. The dashes, s... | correct | as the row above |
| `items[2].prose` | [code] | correct | 1.50 + 2.25 = 3.75; exception propagates to the caller's try |
| `items[2].widget.options[0].text` | KEY: `skip x`, then `3.75` | correct | as the row above |
| `items[2].widget.options[1].why` | You expected the loop to end at the error. The `except` handles it and the loop moves on to `'2.25'`. | correct | as the row above |
| `items[2].widget.options[2].why` | The error raised in `parse` travels out to `total`, where `except ValueError` catches it. | correct | as the row above |
| `items[2].widget.options[3].why` | The `except` block prints before the loop continues. | correct | as the row above |
| `items[2].feedback.correct` | The error from `parse` was caught in `total`, and the loop carried on. | correct | as the row above |
| `items[2].feedback.generic` | Not quite right. Follow the `ValueError` out of `parse`. | correct | as the row above |
| `items[2].explain.text` | `parse("x")` raises inside `parse`, which has no `try`. The exception travels to the caller, where `except ... | correct | as the row above |
| `items[3].prose` | A vendor file has UK dates, is out of order, and some closes are blank or `n/a`. `d.strftime("%Y-%m-%d")` w... | correct | harness: solution passes 4 tests |
| `items[3].widget.how` | Check runs 4 hidden tests. Test 4 has a wrong header, `day`, which is a bug and must raise `KeyError`, not ... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[3].feedback.correct` | Four good days, in date order, with the bad closes skipped. | correct | harness: solution passes 4 tests |
| `items[3].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `items[3].feedback.byKey.test-1` | Test 1 expects `[('2024-02-28', 100.0), ('2024-02-29', 100.4), ('2024-03-01', 102.0), ('2024-03-06', 103.1)... | correct | as the row above |
| `items[3].feedback.byKey.test-4` | Test 4 expects `KeyError` for a file whose header says `day`. A bare `except` skipped every row instead of ... | correct | as the row above |
| `items[3].explain.text` | Parse the date, then try `float` on the close and skip only on `ValueError`. Sorting `(datetime, close)` pa... | correct | as the row above |
| `items[4].prose` | [code] | correct | run `hw3 str only` |
| `items[4].widget.options[0].text` | KEY: `VOD x100`, then something like `[<__main__.Position object at 0x7f...>]` | correct | as the row above |
| `items[4].widget.options[1].why` | You expected the list to use `__str__`. A list shows each item with `__repr__`, which this class does not d... | correct | as the row above |
| `items[4].widget.options[2].why` | `print(p)` calls `__str__`, which this class defines. Only the list falls back to the default. | correct | as the row above |
| `items[4].feedback.correct` | `print(p)` uses `__str__`; the list uses `__repr__`. | correct | as the row above |
| `items[4].feedback.generic` | Not quite right. Which method does each display call? | correct | as the row above |
| `items[4].explain.text` | `print(p)` asks for `__str__`, so it shows `VOD x100`. A list shows its items with `__repr__`, and this cla... | correct | as the row above |
| `items[5].prose` | Each day a price moves 1% up or down with equal chance. After 20 days it ends above £100.00 only with 11 or... | correct | run `hw3 exact 0.4119` (binomial sum), `hw3 10 up 10 down below start`, `hw3 seeded shares`, `hw3 simulation converges to 0.4119` (200,000 paths, s.e. 0.0011) |
| `items[5].widget.how` | Check runs 5 hidden tests with fixed seeds, so draw the moves in the stated order: all of path 1, then all ... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[5].feedback.correct` | Seed 1 gives 0.407, close to the exact 0.4119. | correct | run `hw3 exact 0.4119` (binomial sum), `hw3 10 up 10 down below start`, `hw3 seeded shares`, `hw3 simulation converges to 0.4119` (200,000 paths, s.e. 0.0011) |
| `items[5].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `items[5].feedback.byKey.test-1` | Test 1 expects 0.407. Seed once before all the paths, start each path at 100.0, and divide with `/`. | correct | as the row above |
| `items[5].feedback.byKey.test-4` | Test 4 has 0 days, so every path stays at exactly £100.00. That is not above £100.00, so the answer is 0.0. | correct | as the row above |
| `items[5].explain.text` | With 20 moves, 10 ups and 10 downs leave $100 \times 0.9999^{10} \approx 99.90$, just below the start. So a... | correct | as the row above |
| `items[6].prose` | A trade blotter records each fill with a UK date. A trade for zero shares is an input error. | correct | harness: solution passes 7 tests |
| `items[6].widget.how` | Check runs 7 hidden tests. Tests 4 and 5 pass when `Trade(...)` raises `ValueError`; test 6 checks that two... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[6].feedback.correct` | Trades come back in date order, zero-quantity trades are refused, and each book keeps its own list. | correct | harness: solution passes 7 tests |
| `items[6].feedback.generic` | Not quite right. Check the first failing test. | correct | as the row above |
| `items[6].feedback.byKey.test-1` | Test 1 adds trades out of order. Sort `(when, ticker, qty)` tuples by the parsed date before formatting, so... | correct | as the row above |
| `items[6].feedback.byKey.test-4` | Test 4 expects `ValueError` for a zero quantity. Check `qty == 0` in `__init__` and raise. | correct | as the row above |
| `items[6].feedback.byKey.test-6` | Test 6 checks a second book is empty. Create the list in `__init__`, not in the class body. | correct | as the row above |
| `items[6].explain.text` | Parsing the date in `__init__` means a bad date fails at once, where it was typed. Sorting tuples whose fir... | correct | as the row above |
| `items[7].prompt` | A colleague asks you to review `positions.py` before it goes into the daily risk report. The file it reads ... | correct | run `hw3 str*float message`, `hw3 text max`; line numbers 5, 21, 22, 28 counted in the listing |
| `items[7].model` | **(a) The bugs, and what each does when it runs.** 1. *`history = []` in the class body* (line 5). It runs ... | correct | as the row above |
| `items[7].rubric[0].text` | Finds the shared `history` list in the class body and explains that every position appends to one list. | correct | as the row above |
| `items[7].rubric[1].text` | Finds that `qty` and `avg_price` stay as strings, and names the `TypeError` from `value` (or the wrong `max`). | correct | as the row above |
| `items[7].rubric[2].text` | Finds the bare `except` and explains that it hides errors such as a `KeyError` from a wrong column name, re... | correct | as the row above |
| `items[7].rubric[3].text` | Finds that `biggest` compares text, so `'99.80'` beats `'104.20'`. | correct | as the row above |
| `items[7].rubric[4].text` | Gives a corrected module: list in `__init__`, `int` and `float` conversions, `except ValueError` around onl... | correct | as the row above |
| `items[7].rubric[5].text` | Names the silent bugs and argues which is most dangerous, such as the bare `except` turning a broken file i... | correct | as the row above |
| `items[8].prose` | A broker's cash account opens with a balance in £. However many deposits and withdrawals it takes, the bala... | correct | run `hw3 0.7 three times`; harness: solution passes 10 tests |
| `items[8].widget.how` | Check runs 10 hidden tests on accounts they build. Balances and moves must be exactly equal (`==`), not mer... | correct | harness: the stated test count equals len(tests); comparison mode and the tests named match the widget |
| `items[8].feedback.correct` | Whole pence keep every balance exact, refused moves change nothing, and each account keeps its own history. | correct | run `hw3 0.7 three times`; harness: solution passes 10 tests |
| `items[8].feedback.generic` | Not quite right. Read the first failing test. | correct | as the row above |
| `items[8].feedback.byKey.test-2` | Test 2 deposits £0.70 three times and expects exactly 2.1. Added as floats the total falls just short, so k... | correct | as the row above |
| `items[8].feedback.byKey.test-3` | Test 3 deposits £0.29. `0.29 * 100` is a shade under 29, so `int` gives 28 pence; `round` gives 29. | correct | as the row above |
| `items[8].feedback.byKey.test-4` | Test 4 withdraws the whole £19.99. Taking exactly the balance is allowed: refuse only more than it. | correct | as the row above |
| `items[8].feedback.byKey.test-6` | Test 6 tries to take £25.00 from £10.00. Check before you change the balance or the history, then raise. | correct | as the row above |
| `items[8].feedback.byKey.test-7` | Test 7 deposits 0. An amount that is not above zero is refused, so test `amount <= 0`. | correct | as the row above |
| `items[8].feedback.byKey.test-9` | Test 9 withdraws -£5.00, which would add money. Refuse it like a deposit of 0. | correct | as the row above |
| `items[8].feedback.byKey.test-10` | Test 10 checks that a second account starts empty. Make the list in `__init__`, not in the class body. | correct | as the row above |
| `items[8].explain.text` | Whole pence are exact integers, so three deposits of £0.70 make exactly £2.10. Every check runs before anyt... | correct | as the row above |

## Totals

2168 rows: 2159 correct, 5 imprecise, 3 unverified, 1 wrong.

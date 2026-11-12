# Concept audit, round 2 (blind): py-found L1 to L3

Auditor: Fable, audit session 11, 12 Nov 2026. Branch tip read: `5f59ee5c` on `claude/fable-audit`.

Scope: `app/content/courses/py-found/` lessons l1 to l12, review-1 to review-3, homework-1 to homework-3 (Stage 1, full ledger). L4 and the `*-sample-parts*` files are out of scope.

Blind rule: the ledger, the findings below and the concepts script were written and committed (WIP commit) before any `docs/reviews/*py-found*` or `docs/reports/*py-found*` file, or the audit log and notes, was opened. The number scripts were run but not opened. The overlap section was filled afterwards.

## Result in one paragraph

Six findings: 1 `wrong`, 5 `imprecise`, 0 `misleading`. All six are `minor`; none is `serious`. No graded key is wrong, no code solution teaches a wrong method, and every stated number, printed output and error message in scope reproduces. The ledger has 2,168 rows: 2,159 `correct`, 5 `imprecise`, 1 `wrong`, 3 `unverified`.

## Files

- Ledger: `docs/reports/audit-py-found-1-3-r2-ledger.md`
- Executed claims: `docs/reports/py-found-L1-3-r2-concepts.py` (447 checks, exit 0)

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `l7-arguments.json` | `quiz[0].widget.options[1].why` | **wrong**, minor | The option `6` is explained as "You put 1 into `factor`." That mistake does not give 6. | With 1 in `factor` the call is `scale(5, 1)`, which returns 5 × 1 + 0 = 5. The value 6 comes from leaving the factor out: 5 + 1. Run: `l7 q FINDING: 1 into factor gives 5, not 6`. The graded key, 11, is right. | Replace the `why` with: "You added the offset to 5 and left the factor out. `factor` keeps its default 2, so the result is 5 × 2 + 1."

2. `l6-membership.json` | `screens[7].feedback.correct` | **imprecise**, minor | "`set()` is the only way to write an empty set." It is the usual way, not the only one. | `{*()}` and `set([])` are also empty sets. Run: `l6 other spellings of an empty set exist`. The teaching point (empty braces make a dictionary) is right and is stated correctly in the explain. | Replace with: "An empty set is written `set()`: empty braces already mean an empty dictionary."

3. `l3-unpacking.json` | `screens[1].prose` | **imprecise**, minor | "The pair on the last screen was a **tuple**: values in a fixed order, written with round brackets." The pair on the last screen (`ask, bid`) had no brackets, and brackets alone do not make a tuple. | `type((5))` is `int`; `type((5,))` and `1, 2` are tuples. Run: `l3 commas make the tuple`. Python reference 6.2.3: the comma makes the tuple. l7 screen 4 later says "Commas make a tuple", so the course corrects itself four lessons on. | Replace the first sentence with: "The pair on the last screen was a **tuple**: values in a fixed order, separated by commas and usually written inside round brackets."

4. `l8-who-changes-the-list.json` | `summary.ideas[2]` | **imprecise**, minor | "A pure function reads its arguments and returns a new value." A function can do both and still not be pure. | The standard meaning has two parts: the result depends only on the arguments, and nothing outside the function changes. A function that reads its arguments, prints or reseeds `random`, and returns a new list fits the summary line but is not pure. The definition on screen 6 ("only reads its arguments") is acceptable when read strictly; the summary drops the "only". | Replace the first sentence with: "A pure function only reads its arguments, changes nothing else, and returns a new value (`sorted`, `dict(book)`)." Keep the second sentence.

5. `l12-data-with-behaviour.json` | `screens[1].explain.text` | **imprecise**, minor | "A method's first parameter is always the object before the dot." Screen 7 of the same lesson shows a call where this is false. | In `Position.value(shel, 27.00)` the name before the dot is the class, and the first parameter is `shel`. Run: `l12 value`. | Replace the last sentence with: "When you call a method on an object, Python passes that object as the first parameter."

6. `l1-why-not-0-3.json` | `screens[2].prose` | **imprecise**, minor | "It is stored in binary with about 17 significant digits." Seventeen is the number of digits needed to print a float uniquely, not the precision it holds. | 53 binary digits carry 53 × log10(2) = 15.95 decimal digits; `sys.float_info.dig` is 15. Run: `l1 53 bits`, `l1 17 digits identify a double`. A learner told 17 would trust one digit too many. | Replace the second sentence with: "It is stored in binary, with room for about 16 significant decimal digits, so 0.1 is kept as the nearest value it can hold."

## Unverified rows (not findings)

Three lines make a remark about market practice that the lesson does not source. The code and numbers on each screen are verified.

- `l2-slicing.json` `screens[10].prose`: "A close above it is read as strength."
- `l9-splitting-files.json` `screens[6].prose`: "Traders often draw a band two standard deviations either side of the mean price." The shape matches Bollinger's bands, which use a population standard deviation; the lesson uses the sample one and says so.
- `homework-3.json` `items[0].prose`: log returns are "handy for risk work". The additivity claim itself is correct.

They are harmless as scene-setting. If the fixer wants them out of the unverified column, "Some traders" in place of "Traders" is enough.

## Checks on the brief's list

- Conventions, each stated where it first matters: simple return as a formula (l3 screen 6), log return named against simple (l9 screen 2), sample standard deviation named and `pstdev` contrasted (l9 screen 6), drawdown as a positive fraction of the peak with the start as first peak (l7 screen 9), cash flow sign (l12 screen 8), a return dated to the later day (homework-1 item 5), short positions as negative quantities (l5 screen 2 onwards).
- Graded keys: all 127 choice keys, 17 numeric keys and 18 tap, drag and order keys reproduce by run or by hand.
- Slip values: all 30 `wrong[]` values and 5 wrong sets were recomputed from the mistake its feedback names. All match. The one mismatch found is in a choice option's `why` (finding 1).
- `feedback.byKey.test-N`: each named slip was traced to the first test it fails. All match the test they name.
- Code that passes but teaches a wrong method: none found. Money is kept in whole pence with `round`, not `int`; `sorted` is used where the caller's list must survive; exceptions are caught by name.
- Version sensitivity: three quoted interpreter messages are prefixes of what Python 3.12 prints (see the ledger's version note). None changes an answer.

## Gates

- `node tools/validate.mjs`: 0 errors, 4,531 warnings. The manifest was not changed.
- `docs/reports/py-found-L1-numbers.py`: exit 1, 408 of 409 checks. `py-found-L2-numbers.py`: exit 1, 386 of 387. `py-found-L3-numbers.py`: exit 1, 178 of 179. Each fails exactly one check, the known harness limit for performance-task tests.
- `node tools/grade-all.mjs --file` on review-1, review-2, review-3, homework-1, homework-2, homework-3: 0 failures each (31 choice and numeric widgets). It does not run code widgets; the concepts script's harness section runs all 58.
- `docs/reports/py-found-L1-3-r2-concepts.py`: exit 0, 447 checks, CPython 3.13.18.

## Overlap with earlier reads

To be filled after the WIP commit.

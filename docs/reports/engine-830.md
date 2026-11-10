# Engine 830 to 834: fluency answer forms

Source: the three bullets under "Raised later (fluency quadratics)" in `docs/BACKLOG-INBOX.md` (now marked "numbered 830", "numbered 831", "numbered 832 and 833"). Backlog items 830 to 834 are appended after 829 in `docs/ENGINE-BACKLOG.md`, each with a status line.

## What changed

| Item | Behaviour | Where |
| --- | --- | --- |
| 830 | `expression` `form: "factorised-fully"`: factorised, and no bracketed sum holds a common whole-number factor or a quadratic that factorises over the integers. `(2x+4)(x+3)` fails for `2(x+2)(x+3)`; `(x^2-4)(x+1)` fails for `(x-2)(x+2)(x+1)`. Equal but not fully factorised returns key `form`, line "Factorise fully: a bracket still has a common factor." | `grade.js` `shapeFullyFactorised`, `expression.js` |
| 831 | `form: "completed-square"`: `a(x+p)^2+q`, a, p, q numbers or fractions, a may be 1 or negative, either order, q may be left out. Expanded and any other equal shape return `form`, line "Write it as a bracket squared plus a number." | `grade.js` `shapeCompletedSquare` |
| 832 | Set answer for `expression` and `numeric`: `answers` + `unordered: true`. Typed with commas, `x = 2, x = -5`, `x = 2 or x = -5`, `\{2, -5\}`. A missing or extra value returns key `count`, line "This question needs 2 values, separated by commas. You gave 1." `\pm` (and `±`, `+-` in a numeric field) stands for both values. The maths keyboard of such an item has its own layout with `,` and `\pm`; a numeric set uses the text phone keyboard. Wrong sets are comma-separated (`tex`, or `value` as quoted numbers). | `grade.js` `exprSetGrade`, `numSetGrade`, both widgets, `exam.js` model answer |
| 833 | Fluency `vars` pick of tuples: `{ "pick": [[1, 6], [2, 3]], "as": ["r", "s"] }`; numbers or text, mixed allowed; names checked for form, reserved words and clashes. | `gen.js` |
| 834 | Validator schema (`answers`, `unordered`, `count`, both forms), `fluency-rules.mjs` and `fluency-sample.mjs` read sets, `test-fluency.mjs` grades sets and both forms in the real widgets, new unit tests, five fixture families, AUTHORING (numeric and `expression` sections, section 16). | see below |

Everything works in lessons, quizzes, reviews, homework, exams and drills as well as in Fluency, because it is in the widgets and in `ZQ.grade`. This is stated in the `expression` section of `docs/AUTHORING.md`.

## Decisions and limits

- A bracket counts as factorisable when its discriminant is a perfect square, so rational roots count as well as integer roots: `4x^2-9` and `2x^2+5x+2` fail "fully", which the brief's wording ("integer roots") would have let through. `x^2+3x` (roots 0 and -3) fails too. Brackets with fractional coefficients are not tested for a common factor.
- `completed-square` needs a bracket, so `x^2-4` (p = 0) is not accepted; the coefficient of x inside the bracket must be 1, so `(2x+3)^2-4` is refused; a surd `q` is refused.
- `answers` replaces `answer`; both together, `accept` (expression), `form`, `upToConstant` and `unit: "%"` with `answers` are validator errors. A numeric `accept` line is allowed. At least two answers; a repeated root is listed and typed twice.
- A set's `wrong[]` is matched in any order and only when the count is right, so a one-value slip is the engine's `count` key, not a `wrong`. The validator rejects a `wrong` set inside the answer's tolerance, and `test-fluency` and `fluency-rules` reject one that grades correct.
- `form` is not checked per value of a set (not used with `answers`).
- The existing `factorised` check moved unchanged into `ZQ.grade.shapeFactorised` so the new form reuses it.

## Tests

Before and after, from `app/` with `--local-cdn` (every `tools/test-*`, plus `test-expr-equations --audit`):

- `test-expr-equations --audit`: output identical before and after (530 expression widgets, 0 relations).
- Every `tools/test-*` file exits 0 before and after, except `test-cumulative.mjs`, which was already failing before this change (20 of 25, the same five cases, because the real quadratics Fluency sets now exist and its "no Fluency set written" cases assume none). The failing lines are identical before and after.
- New: `tools/test-answer-forms.mjs` (unit tests of both forms and of set grading on the real `grade.js` with the Compute Engine, and the real widgets in Chromium: default lines, count line, keyboard layout, input mode): 235 of 235.
- New: `tools/test-validate-answer-forms.mjs` (validator scratch cases on a copy of the app): all pass.
- `tools/test-fluency.mjs`: unit part gains family-rule and tuple cases (287); browser part grades the five new fixture families at 50 seeds in the real widgets (set in order, reversed, `x = a or x = b`, `a \pm b`, one value short, one too many, each wrong set, the prompt typed back for each form): all pass.
- `tools/test-validate-fluency.mjs`: ten new cases, 40 of 40.
- Validator: 0 errors, 4109 warnings (unchanged). `readiness-sums.mjs` OK.
- Playthrough: `--fluency` on `fixture/fluency-l3-opening-brackets` and `quadratics/fluency-l1-two-brackets`, three lessons that use `expression` with `form` (`series/l11-powers-of-a-bracket`, `limits/l6-first-principles`, `quadratics/l13-best-price`), `--routes-only`: all green, desktop and `--mobile`. Re-run after the restart: validator 0 errors, readiness OK, every `tools/test-*` green (test-cumulative as before), all playthroughs above green. The full `--all` run was not done (too long for the foreground limit); it is deferred.

## Fixture families added

`tools/fixtures/fluency/fluency-l3-opening-brackets.json` now has ten families: `factorise-fully` (830), `complete-the-square` (831), `roots-numeric` (832 numeric set, tuple pick 833), `roots-expression` (832 expression set with fractions, tuple pick), `roots-surd` (832 with `\pm`).

## Deferred

- The full `playthrough --all` run (only the affected lessons, the two Fluency sets, the fixture and routes were played).
- Per-value `form` for a set (for example `simplified` on surd roots).
- A `\mp` and more than two `\pm` in one value; a numeric `\pm` with arithmetic on either side.
- A set in `table` cells and in `multi`-part exam items was not looked at; only the `expression` and `numeric` widgets changed.
- The quadratics Fluency authors can now write the skipped families (l3 and l4 fully factorised, l6 completed square, l6 and l7 both roots); `test-cumulative.mjs` needs its fixtures changed to stop depending on there being no real Fluency set.

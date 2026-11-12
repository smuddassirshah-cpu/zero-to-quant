## Rule changes proposed

Counts are entries of this triage. Each change is for an engine agent; none was made here.

`[tight-band]`, printed-figure check (77 entries: 6 faults, 13 harmless, 58 tool limit):

1. Fire only when the printed figure is the stored answer rounded to fewer places (`2.47` against `2.4749`, `0.46` against `0.4615`) and is not one of the item's `wrong[]` values. This test keeps all 6 faults and drops classes T1 ({n:T1}), T2 ({n:T2}), T3 ({n:T3}) and T4 ({n:T4}), where the figure is a slip, a pre-rounding value or another quantity. If that test is not wanted, three narrow skips remove 47 of those 57: a figure equal to a `wrong[]` value; a whole-number answer with `tol.abs` of 0.5 or less; a figure followed by `\ldots`.
2. Where the question asks for k places (or a fraction) and the figure has fewer than k, report it under a separate advisory on the explanation text, not as a band fault (class H2, {n:H2}). The band is right; the text is rounded more coarsely than the form it asks for.
3. Read `49{,}988` as 49,988 (class T5, {n:T5}).

`[tight-band]`, rounded-as-asked check (2 entries, both tool limit):

4. Take "whole number" as a rounding only from the question, or from prose only in "nearest whole number" or "Give a whole number" (class T6, {n:T6}). "A whole number from 1 to 100 is picked" is not a form.

`[tight-band]`, half-unit check (70 entries: 2 faults, 68 harmless):

5. Fire only when the stored answer lies within 0.1 of a unit of a rounding edge (0.225156 at 2 places, 2.754242 at 2 places). That keeps both faults (class F2) and cuts the 70 to 11. Away from an edge a working with rounded figures still rounds to the stored answer, which is what the 68 of class H1 show.

`[wide-wrong-band]` (36 entries: 0 faults, 34 harmless, 2 tool limit):

6. Fire only when the wrong band reaches the answer band or another `wrong[]` value, the two cases in which it can take a right answer's line or another slip's line. None of the 36 does either. A small slip with an absolute band a little wider than itself (class H3, {n:H3}) is the normal way to catch the slip rounded as asked.
7. Measure the band from the authored `tol`, not from `tol` plus the grader's float slack (class T7, {n:T7}). Engine note from the same two items: the slack (1e-9 absolute, 1e-12 relative in `grade.js within`) is wider than a wrong value of 1e-12 or 2.2e-16, so a typed 0 gets that slip's line.

`grade-regression.mjs` self-grade note (257 entries, all tool limit):

8. Leave out of the "do not grade correct themselves" count any answer that holds a template: `{...}` in a `fluency-*.json` family (class T8, {n:T8}, of which 13 are fixtures under `tools/fixtures/fluency`) and `{{carry...}}` (class T9, {n:T9}). With those out the count is 0. Better, draw each family as `fluency-selfgrade.mjs` does here and grade the realised answers: 10,240 draws, none refused, none of 20,198 wrong values graded correct.
9. Do not walk `tools/fixtures` when `--content` is the app folder, or report fixtures apart from content.

# Engine backlog (raised by content agents; scheduled by the orchestrator)

Fix in one integration pass, then update AUTHORING.md and the canvas READMEs.

1. `tap-regions`: a count mode (`count: k`, optional `among: [ids]`) so "shade any 3 of 4" grades.
2. `validate.mjs`: area ids with 10 or more rows or columns are `c1-10`, not `c110`; accept a bare number `target` for `drag-point` on number-line and circle.
3. `area` canvas: honour `canvas.controls` bound to `split`/`grid` so the learner can re-cut; slider readouts support a `format: "fraction"`.
4. `number-line`: `labelPos` (above, below, left, right) on points and intervals; avoid label collisions with arrows and between close points.
5. `area`: grid lines inside shaded cells too faint.
6. `canvas.controls[].start`: document (AUTHORING.md and READMEs); default to the bound point's current value.
7. `ZQ.test` hook in set mode (runSet, homework, exams) so playthroughs cover reviews, homework and exams.
8. `number-line`: tap mode on points.
9. `state.practiceResult({results})`: Elo and the streak problem count for practice and weekly problems; `select.js` to call it.
10. `examFinished`: misses join the redo queue with ref `{ exam, item }`; `select.resolve` understands it.
11. `longform` widget help text: "Check" versus "Mark my answer" wording to match the homework button.
12. Today: show the weekly probability problems row from `select.weeklyStatus()`.

Raised later (number-sense level 3):

13. `grade.js` `prose()`: newline to `<br>` replacement corrupts KaTeX SVG output (`\sqrt` vanishes); replace newlines only outside rendered maths. Then switch `\surd{` back to `\sqrt{` in number-sense level 3 files (cube roots `{}^3\!\surd{x}` to `\sqrt[3]{x}`).
14. Validator: accept `byKey` entries keyed by a drag-point's point id (the widget returns that id when off target with no matching region).
15. `number-line`: accept keyed patches for `points` (`{"points": {"p1": {...}}}`), as README-B describes for other kinds, without throwing.
16. `grid` canvas: honour `countWord`.
17. Document in AUTHORING.md: a bare £ inside `$...$` renders italic; write `\text{£}`; grid cell text cannot hold KaTeX (use Unicode superscripts).

Raised later (ratio level 2):

18. `bars` `showValues` and `series` marker value labels: a `decimals` or `money: "£"` option so labels keep trailing zeros.
19. `bars.setParam` (or dotted `bind` in `canvas.controls`) so an explore slider can move a bar's height.
20. Linked canvas state: a `derive` block on a canvas (`"derive": { "p2.x": "0.8 * p1.x", "caption": "Change: {{(p1.x/50-1)*100}}%" }`) evaluated on every change, so explore screens can show a live computed label or a dependent point. Design and implement on number-line, plane and bars at least.
21. README-B: document `null` gaps in a series and a marker with explicit `y` to fill them.

Raised later (ratio level 1):

22. `area` canvas: `setParam` for `shade` fraction and `split`, with a `format: "percent"` option on slider readouts.
23. Slider widget: the value bubble overlaps the label near the minimum.

Raised later (ratio level 3):

24. `place` widget on a `boxes` canvas: grade the learner's own drag of items into containers (`mode: "boxes"`, answer as `{ container: [itemIds] }`).
25. `plane`: a `labelSide` (`above`|`below`) or offset on function labels.
26. `plane`: `canvas.controls` able to drive a point's coordinate (`bind: "points.p1.x"`).
27. `canvas.controls[].start`: also apply the start value to the canvas on mount so they never disagree.

## Integration pass: status

Items 1 to 23 are done; the authoring side is in AUTHORING.md sections 3, 4, 5 and 7 and the two canvas READMEs.

1. Done: `tap-regions` `count` and `among` (keys `too-few`, `too-many`), "2 of 3" count line; validator rule.
2. Done: validator area ids `c{i}-{j}` from 10 up (and circle sectors), bare number `drag-point` targets on number-line and circle, `tol` optional.
3. Done: area `setParam`/`getParam` for `split`, `grid`, `shade`; `state.grid` re-cuts; control and slider `format: "fraction"`.
4. Done: number-line `labelPos` on points and intervals, labels moved off jump arrows and stacked when close.
5. Done: area grid lines redrawn over each shading in a darker tone of its colour.
6. Done: controls open at the bound value (via `getParam` or the state) without `start`; `start` is applied to the canvas; documented.
7. Done: `ZQ.test` in `runSet` and the set page, the homework page and the exam screen; playthrough `--sets`, `--exams`, `--all`.
8. Done: number-line points are tappable (`enable('tap')`), so `tap-regions` takes point ids.
9. Done: `ZQ.state.practiceResult`, called from review.js for practice and weekly sets.
10. Done: `examFinished` queues misses as kind `exam`, ref `{ exam, item }`; `select.resolve` returns the item without hints.
11. Done: longform help line names "Mark my answer" in exam mode (homework) and "Check" in set mode.
12. Done: Today shows "Weekly probability problems: n of 3" linking to #practice/weekly when `weeklyStatus().eligible`.
13. Done: `prose()` turns newlines into `<br>` outside maths only; number-sense level 3 files use `\sqrt` and `\sqrt[3]` again.
14. Done: validator accepts drag-point point ids as `byKey` keys.
15. Done: number-line keyed patches for `points`, `intervals` and `arrows`.
16. Done: `countWord` honoured on every canvas, grid included (the player's count line).
17. Done: AUTHORING.md section 4 notes `\text{£}` in maths and Unicode in grid cell text.
18. Done: bars `decimals` and `money` for value labels; series `decimals` and `money` for `{value}` labels.
19. Done: bars `setParam`/`getParam` by category label or id, and dotted control binds now set the state path on any kind.
20. Done: `canvas.derive` (engine-wide in `ZQ.canvas.create`): linked values and `{{expression}}` captions; validator checks the expressions.
21. Done: README-B documents `null` gaps in a series and marker `y`.
22. Done: area `setParam` for `shade` and `split`; `format: "percent"` on slider and control readouts.
23. Done: the slider label has its own row above the value bubble.

Second pass (items 24 to 39):

24. Done: `place` `mode: "boxes"` grades the items the learner drags into a boxes canvas's containers (`answer: { container: [itemIds] }`, optional `ordered`); validator checks containers and items.
25. Done: plane function `labelSide` (`above`, `below`) and `labelOffset: [dx, dy]`.
26. Done: controls bind `points.p1.x` (any list item by id, on any kind); the slider opens at the point's value.
27. Done (in pass 1, confirmed): a control's `start` is applied to the canvas on mount; without it the control reads the canvas.
28. Done: balance `subtract-both` and `add-both` chips, negative weights and `coef` on unknowns (signed pans collapse to totals; divide by any non-zero number); solver and validator understand them.
29. Done: validator type checks for `hints[].highlight`, `among`, list answers, `options` and the other list fields, plus the per-file guard; a bad shape is one error line.
30. Done: mixed text and maths labels in plane and the Canvases B kit keep their spaces.
31. Done: number-line points in the explanation copy are plain dots (see 39).
32. Done: balance `state.params.x` is patchable and a control can bind `x`; the beam re-tilts.
33. Done: `expression` `form` (`expanded`, `factorised`, `simplified`) on the Compute Engine's canonical MathJSON, key `form`; without the engine the normalised `accept[]` match stands.
34. Done: `place` `byText: true` and `same` groups make tokens interchangeable, in assign and order modes.
35. Done: area text on a piece, `labels` or `state.labels` keyed by cell id.
36. Done: coins show H or T unless labelled; a `bag` (alias `sealed`) item kind.
37. Done: number-line interval rows 16px apart with `row`; a side label on a ray sits above it at the edge.
38. Done: keyed list patches in `ZQ.canvas.merge`, so explain, option and step patches merge by id on every kind.
39. Done: number-line points are plain dots unless `drag: true` or a drag-point widget lists them; never handles in tap mode or a static copy.


Raised later (equations level 2):

28. `balance`: a "subtract from both" chip, signed weights and fractional unknown blocks so `x - 3 = 8` and `7 - 3x = 22` can live on the scale.
29. Validator: report a non-list `hints[].highlight` as an error instead of crashing (one crash stops the manifest being written for everyone).
30. `plane` axis labels: mixed text and maths loses spaces ("Price $p$ (£)").
31. `number-line` inside the explanation clone: points still look like draggable handles; render static.

Raised later (equations level 1):

32. `balance`: allow `state.params.x` (the unknown's value) to be patched by controls and explanation patches.
33. `expression` widget: a `form: "expanded"|"factorised"|"simplified"` requirement (accept only when the input's canonical form matches that shape), so expand and factorise tasks can use free entry.
34. `place`: tokens with identical text are interchangeable (`same: ["t1","t2"]` or grade by text when `byText: true`).
35. `area`: optional text label per piece or region (`labels: {"c11": "3n"}`).
36. `boxes`: coins default to a face label, and a `bag`/`sealed` item kind.

Raised later (equations level 3):

37. `number-line` intervals: wider row spacing or a per-interval `row` offset; `labelPos: "right"` on rays to infinity is clipped.
38. Keyed patches (`{"points": {"id": {...}}}`) in `explain.canvas` or option `canvas` patches wipe the array: apply keyed merging in `ZQ.canvas.merge` (or in `create`'s patch path) for every kind, not only in each canvas's own update.
39. `number-line` points default to a static look unless `drag: true`; in tap mode and static clones never draw the drag handle.

Raised later (equations level 4):

40. `balance`: more than one unknown kind (`unknown` items with their own `label` and hidden `value`).
41. `plane`: function `labelPos` (above, below) and offset; falling lines overlap their label today. (Same as 25; keep one.)
42. `boxes`: remove the empty band above containers when there is no `hand` container.

Raised later (functions level 1):

43. `plane`: a `vline`/`hline` primitive (`x = a`, `y = b`) with ids; `on: "f"` respects the function's `domain`.
44. `plane`: `equal: true` ignored when `height` is given; honour both.
45. `number-line`: `colour` (series slot) on intervals and points.

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
40. Done: balance unknowns of several kinds (own `label`, hidden `value`); one remove chip per label; targets name labels; solver and validator follow.
41. Done: same as 25; `labelPos` is accepted as an alias of `labelSide` on plane function labels.
42. Done: boxes without a `hand` show the band above the containers only while an item is drawn.
43. Done: plane `vlines` and `hlines` with ids and labels; a point `on: "f"` stays inside f's `domain` when dragged.
44. Done: plane `equal: true` with `height` keeps the height and widens the shorter range so units stay square.
45. Done: number-line `colour` on points and intervals, now patchable (the old slot class is replaced).
46. Done: `derive` helpers `fixed(v, d)` and `money(v, symbol)`; `(expr).toFixed(2)` and ternaries documented.
47. Done: plane tap mode on points, so `tap-regions` takes plane point ids (validator knows them).
48. Done: the validator accepts an explore screen whose interaction is a `drag: true` point (or vectors in `state.drag`, or a `sim`); the controls plus derive pattern is documented.
49. Done: plane tangent at a corner is not drawn unless `side` picks a one-sided slope; `lengthPx` gives a length in pixels.
50. Done: series `drawdown: "money"` (and `"abs"`) labels the absolute fall; no division by a zero peak.

Third pass (items 51 to 77):

51. Done: area signed pieces: a negative `colSizes` or `rowSizes` entry makes its strip subtracted (hatched, dashed edge).
52. Done: area `colLabels`, `rowLabels` and edge `labels` patchable through state.
53. Done: area `state.move: { from, to }` (or a list) slides a copy of a piece to another cell, its place left empty.
54. Done: `ZQ.canvas.compile` wraps a unary minus before a power, so `-x^2` is -(x^2) (it compiled to a syntax error and drew nothing).
55. Done: payoff leg labels keep clear of the bold combined line (the line is an obstacle in label placement).
56. Done: derived numbers in captions and table cells print negatives with the minus sign U+2212.
57. Done: plane function `labelAnchor`; every label keeps clear of every curve and of the axes.
58. Done: `\pounds` (and `\text{£}`, rewritten to it) draws the pound sign in the prose face (core.js tex(), CSS).
59. Done: bars `setParam` with a non-category name writes `state.params`, so one control and `derive` drive every bar.
60. Done: validator knows object category ids (`id`, else `x{label}`) on bars.
61. Done: documented that a `functions` patch by id keeps the authored `domain` (the merge already kept it).
62. Done: `derive` runs in the Why? copy on the explained state (static canvases derive too).
63. Done: slider and control `decimals`; `money()` groups thousands.
64. Done: `inline()` sets maths aside first, so `**bold $x$ text**` renders bold around the formula.
65. Done: drag-point `tolX` and targets `{ "on": "f", "x": n }` (graded on x) on a plane.
66. Done: `yScale: "log"` on series and plane, ticks at 1, 2, 5 times powers of ten, price-labelled with `money`.
67. Done: validator accepts `arc` and `radius` as circle ids.
68. Done: circle `drag: true` (params or state) drags without a widget, so explore screens work with `derive` captions; the validator counts it as interactive.
69. Done: `canvas: { kind: "pair", left, right, active, stack }` with patches by side, `left:` / `right:` ids, controls and `derive` across both, a pair Why? copy, validator support and a gallery sample.
70. Done: circle README (and AUTHORING) note that a radians `tol` of 0.25 is about 14 degrees; give 0.02.
71. Done: derive functions `sin cos tan asin acos atan atan2 hypot ln log10 e` join the set.
72. Done: `ZQ.canvas.compile` maps a free `e` to Math.E (it was left undefined, so `e^x` drew nothing).
73. Done: drag-point `tol: [dx, dy]` per axis.
74. Done: verified plane `labelSide: "below"` (placement now tries below first) and `labelOffset` applied as given.
75. Done: README-B documents `hlines` and `vlines` (pass 2), now with their patchable fields.
76. Done: plane geometry kit: `polygons` with `vertexLabels`, `angles` (arcs and right-angle squares), segment `labelOffset`, `axes: false`.
77. Done: area `state.diagonal` per cell and half-cell shade ids (`c11/ul`, `c11/lr`, `c11/ur`, `c11/ll`).
78. Done: plane `xTicks: "integer"` and `yTicks: "integer"`.
79. Done: bars per-category `colour` (series slot), and `state.colours` to change them.
80. Done: `derive` runs up to three passes, so a rule can read a value another rule derives.
81. Done: table `compact` (automatic above 6 columns): tighter cells; it still scrolls sideways rather than clipping.
82. Done: plane points outside the plot are not drawn; the x-axis title moves below the axis when a point or curve sits under it.
83. Done: tree `collapse` resizes the drawing to the leaves (or depth) still shown.
84. Done: place `mode: "boxes"` counts as canvas-bound (player and the explore rule); `free: true` and `count: { container: n }` (key `count-<container>`).
85. Done: boxes containers take `fill: "top"|"bottom"`.
86. Done: the verdict chip lets long inline maths wrap between terms.
87. Done: plane `xStep` and `yStep`.
88. Done: circle cos label starts clear of the angle mark; the sin label sits past the rim (outside the circle for small angles).


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

Raised later (functions level 2):

46. Derive captions and plane point labels: document `(expr).toFixed(2)` and ternaries, and add `fixed(v, d)` and `money(v)` helpers.
47. `plane`: tap mode on points (`enable('tap')`) so tap-regions can ask "which point is (−2, 4)?".

Raised later (functions level 3):

48. Validator: accept an `explore` screen whose interaction is a `drag: true` point (or document the controls plus derive pattern).
49. `plane` tangent on a piecewise-linear function at a corner: use one-sided slope or suppress; `length` in pixel units option.
50. `series` `drawdown`: a `money` label option (absolute fall) for cumulative P&L that starts at zero.

Raised later (quadratics level 1):

51. `area`: signed pieces (negative strips drawn dashed or hatched, subtracted from the total) so (x + 5)(x − 2) stays on the area model.
52. `area`: `colLabels`/`rowLabels` patchable through state.
53. `area`: animate a piece moving (`move: { from: "c12", to: "c31" }`) for the difference-of-squares rearrangement.

Raised later (functions level 4):

54. `ZQ.canvas.compile`: `-x^2` compiles to `-x**2` which JavaScript rejects; wrap unary minus before a power (`(-x)**2` is wrong; want `-(x**2)`), or document `-(x^2)`.
55. `payoff`: leg labels may overlap the bold combined line; place labels away from it.
56. Derived numbers in tables and captions: render negatives with a proper minus sign (U+2212).

Raised later (quadratics level 2):

57. `plane` function labels: `labelAnchor` (start|end) and automatic placement clear of other curves and the axes.
58. `\text{£}` renders in a different face from prose; a `\pounds`-style macro in the KaTeX settings (define `\£` or map `\text{£}` to the sans face).

Raised later (exp-log level 1):

59. `bars` `setParam`: accept free parameter names (stored in `state.params`) so a `derive` block can drive every bar from one control.
60. Validator: for object categories `{id, label}` accept the element id as `id` as well as `x{label}`.
61. README-B: a `functions` patch by id keeps `domain` from params unless given again (document, or merge the domain).

Raised later (quadratics level 3):

62. Why? modal static clones must run `derive` after the explain patch (derived points, segments, captions stale otherwise).
63. Slider readout decimals: a `decimals` option independent of `step`; `money()` in derive uses a thousands separator.
64. Prose renderer: KaTeX inside `**bold**` (render maths first, then bold).

Raised later (exp-log level 2):

65. `drag-point` on plane: a `tolX` (x-only tolerance) and a target given as `{ "on": "f", "x": 12.3 }` so dragging along a steep curve is gradable.
66. `series` and `plane`: `yScale: "log"` option (log-price charts).

Raised later (trig level 2):

67. Validator: accept `arc` and `radius` as circle ids.
68. `circle`: free drag on explore screens (`drag: true` on the point) with `derive` live captions, like plane points.
69. A screen may hold two canvases side by side (`canvases: [...]` or a `pair` kind), or a built-in "unrolling" view on circle (angle to sine graph).
70. `circle` README: note that `drag-point` default `tol` 0.25 is about 14° in radians; recommend 0.02.
71. `derive` functions: add `sin`, `cos`, `tan`, `sqrt`, `abs`, `ln`, `exp`, `pi` to the derive function set.

Raised later (exp-log level 3):

72. `ZQ.canvas.compile`: map `e` to Math.E in function expressions (README-B says it is supported).
73. `drag-point` on plane: per-axis tolerance (`tol: [dx, dy]`).
74. `plane` `labelSide: "below"` appears ignored; `labelOffset` uneven. Verify and fix.
75. README-B: document `hlines` and `vlines`.

Raised later (trig level 1):

76. `plane` geometry: `polygons` (filled, with ids and vertex labels), `angles` (arc markers at a vertex with a label), segment `labelPos`/offset, `axes: false` to hide axes and ticks. This is the triangle kit.
77. `area`: a diagonal across a piece (`split: "diag"` on a cell).

Raised later (series level 1):

78. `plane`: `xTicks: "integer"` (and `yTicks`) option for sequence plots on small ranges.

Raised later (series level 2):

79. `bars`: per-category `colour` (series slot) or grouped series, so term bars and cumulative bars differ.
80. `derive`: evaluate rules in dependency order (or iterate to a fixed point, at most 3 passes) so a caption can read another derived value.
81. `table` canvas: shrink or scroll horizontally at narrow widths instead of clipping; the player's column is 540px so tables over about 7 columns need a compact mode.
82. `plane`: clip points and segments to the plot area; move the x-axis title clear of marks near y = 0.

Raised later (counting level 1):

83. `tree` `collapse`: size the drawing by the leaves actually shown, not the full tree.
84. `place` `mode: "boxes"`: count as a canvas-bound widget on explore screens; add `free: true` (any arrangement accepted) and grading by `count` per container.
85. `boxes` `box` container: a `fill: "top"|"bottom"` option.
86. Verdict chip: wrap long inline KaTeX instead of overflowing.

Raised later (trig level 3):

87. `plane`: `xStep`/`yStep` tick spacing parameters (degree axes at 90, month axes at 3).
88. `circle`: angle label collides with the cos label in the fourth quadrant; sin label touches the circle at small angles.

Raised later (series level 3):

89. `grid`: `state.cells` (or `values`) override so a patch can fill a cell during an explanation.
90. `derive` validation: allow `=` inside string literals in caption expressions.
91. Longform model answers and prose: wrap or scroll long display maths at narrow widths.
92. `boxes` `box` container: close the top edge (cosmetic).

Raised later (counting level 2):

93. `grid`: a `paths` overlay (sequence of cell ids drawn as a route) and a lattice-points mode.
94. `tree`: `compact: true` with narrower leaf spacing so a 16-leaf tree fits the column.
95. `graph`: `state.labels` to relabel nodes; a `ring` layout with a `rotate` patch (seats round a table).
96. `grid` `shade`: optional `colour` slot per named set.

Raised later (terminal level 1):

97. `tree`: a `current` node marker (like graph's) and a labelled root (`rootLabel`).
98. Canvas captions: render inline code (backticks) and bold like prose.
99. `graph`: shrink node labels to fit or auto-size `nodeRadius` to the longest label.
100. `grid`: optional per-row horizontal offset (`rowOffsets`) for staggered layouts such as keyboards.

Raised later (terminal level 2):

101. Validator: a `generalise` screen in a programming course may satisfy the formula rule with a fenced code block instead of KaTeX.
102. `boxes`: a wide labelled `card` (file-name width) item kind.
103. `graph`: add and remove nodes and edges through state (`nodes`/`edges` patches) with enter and exit animation.
104. Inline renderer: `$` and `*` inside backticks are literal (parse code spans first); captions render code spans.

Raised later (counting level 3):

105. `expression` widget in lesson quiz mode: the playthrough's `answerCorrect()` must wait for the maths editor loader (or the widget must accept a value while loading) so quiz items are not reported stuck.
106. README-B `vectors`: document drag on heads (origin-based vectors only) and add `points` with labels (A, B, O, M) and `labelPos` for vector labels.
107. `vectors`: tap mode on arrows.
108. Document the derive function set (it already includes acos, atan2, hypot and others) in AUTHORING.md and README-B.

Raised later (first-python level 1), high priority for the programming courses:

109. `code` widget: a `compare: "stdout"` test mode (`{ "stdin": "250\n", "expect": "Return: 5.00%\n" }`, exact or whitespace-normalised) that re-runs the learner's code per test with the given stdin, so `input()` works and printed output is graded; "Run examples" shows what the code printed. Then replace the `_getframe` trick in first-python level 1 tests (l1, l3, l4, review-1, homework-1) with the new mode.
110. `code` widget: show stdout from Run examples under the editor.
111. `boxes`: card width sized to its label (or a `wide` item kind), shared with item 102.

Raised later (terminal level 3):

112. Playthrough: on a `code` screen, wait for "Python ready" before `check()`; never reveal and move on silently; count a null check as a failure.
113. Code widget results header: let long test calls wrap (`.lsn-ic` nowrap inside `.wd-res-h`).
114. After item 109 lands, also convert the `_getframe` tests in terminal l12, review-3 and homework-3 to `compare: "stdout"`.

Raised later (first-python level 2):

115. `player.js` `resetFor`: on Start over and demonstrate reset, restore the authored initial state rather than emptying unset keys (array cells blank otherwise).
116. `table` canvas: inline code in cells (`mode: "code"` monospaced listing with line numbers).
117. `graph`: node `shape` (circle, diamond, rect) and multi-line labels; tap mode on edges.
118. `table` widget: grade text cells (`answer: "True"`, case-insensitive) as well as numbers.

Raised later (first-python level 3):

119. `array`: cells size to their text (dates, `102.50`).
120. Code widget: a fresh working directory per run in the Pyodide file system (files must not persist between runs).
121. Code widget `isclose`: require a real number, not a number-like string.
122. Player: hide "Start over" when the screen has no interactive canvas (choice and code screens with static diagrams).
123. AUTHORING.md section 3: document `compare: "stdout"`, `stdin` and `printed` once item 109 lands.

Raised later (mental level 1):

124. `orderbook`: `spreadValue: false` to hide the computed spread number.
125. `number-line`: controls may bind a free `state.params` name for `derive` (like other kinds).
126. `number-line` arrows: per-arrow `side: "below"` and automatic stacking of overlapping arcs; tidy zero-length arrows.

Raised later (mental level 2):

127. `area`: controls may bind `colSizes`/`rowSizes` entries so a cut can be dragged at true proportions.
128. `grid` `text: "marked"`: a `revealAfterGrade: true` option so tapping does not reveal the product.

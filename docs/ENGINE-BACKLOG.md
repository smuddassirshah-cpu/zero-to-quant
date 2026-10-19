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

Third pass (items 51 to 114, 123, 133 to 161; 150 deferred):

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
89. Done: grid `state.cells` (a map by id or a 2D array) overrides `params.cells` per cell; `null` restores.
90. Done: derive guard (engine and validator) blanks quoted strings first, so `=` and `;` inside a string literal are allowed.
91. Done: display maths scrolls sideways inside its own box (`.katex-display`), and longform's grid children may shrink, so a long formula never widens the page at 360px.
92. Done: a boxes `box` container is closed on all four sides (rounded corners).
93. Done: grid `state.paths` (routes through cell centres, drawn on, arrowhead, colour slot, highlightable ids) and `params.lattice: true` (points joined by streets, text above right).
94. Done: tree `compact: true` (smaller pills, closer leaves and rows); top to bottom, level labels get their own left margin.
95. Done: graph `state.labels`, `params.layout: "ring"` and `state.rotate` (seats, animated).
96. Done: grid shade sets take `{ "ids": [...], "colour": n }`.
97. Done: tree `state.current` (blue ring round a node's pill, or the root) and `params.rootLabel` (a labelled root pill).
98. Done: canvas captions (every kind and the pair caption) render through `ZQ.grade.inline`: maths, inline code, bold and italic.
99. Done: graph radius fits the longest label (22 to 34) without `nodeRadius`; longer labels shrink down to 10px.
100. Done: grid `params.rowOffsets` (per-row shift in cell widths); outlines, highlights and the point box follow the shift.
101. Done: validator: in a course on the code track, a generalise screen may state the rule in a fenced code block instead of KaTeX.
102. Done: boxes cards are as wide as their label (file names fit), shared with 111.
103. Done: graph `nodes` and `edges` live in state: a list replaces, a map merges, adds or removes (`null`); arrivals fade and grow in, leavers fade out; a removed node takes its edges.
104. Done: `ZQ.grade.inline` sets code spans aside in the same pass as maths, so `$` and `*` inside backticks are literal.
105. Done: the expression widget accepts a value while the maths editor loads (`ready()` counts it) and `grade()` waits for the load.
106. Done: README-B vectors documents head dragging (origin-based vectors only); `params.points` with compass `labelPos`, vector `labelPos: "end"|"mid"|"start"` and `labelSide`.
107. Done: vectors `tap` mode on whole arrows (wide hit stroke) and on points.
108. Done: the derive function set is tabled in AUTHORING.md section 4 and listed in README-B.
109. Done: code widget script mode: `compare: "stdout"` cases with `stdin` and `exact`, the learner's code re-run per case with `input()` fed from stdin, `printed` for call cases; validator rules; first-python l1, l3, l4, review-1, homework-1 converted.
110. Done: Run examples shows what the code printed (script mode per row; otherwise what it printed as it loaded).
111. Done: see 102.
112. Done: the playthrough waits for Python ready on code screens, fails when Python cannot load, and fails an answer that applied with nothing to check (lesson screens and set items).
113. Done: code results headers and value chips wrap long calls.
114. Done: terminal l12 and homework-3 converted to `compare: "stdout"` (review-3 had no `_getframe` tests).
123. Done: AUTHORING.md section 3 documents `compare: "stdout"`, `stdin`, `exact` and `printed` (with 109).
133. Done: bars draw negative values below a zero baseline (axis down to a nice tick, or `yMin`); a negative bar's value label sits under it.
134. Done: number-line, circle, balance and area `setParam` write any name they do not own to `state.params` (and `getParam` reads it back), as bars already did.
135. Done: fenced code blocks put the language and the Copy button in a strip above the code; long lines scroll inside the block and never widen the column.
136. Done: code cases take `setup`, Python run just before `call` (both modes).
137. Done: code `compare: "raises"` with `expect` the exception name (subclasses count); in script mode a raises case without `call` checks the whole program.
138. Done: tree `params.label` is drawn as a title above the tree (and stays its accessible name).
142. Kept: the worker's `loadPackagesFromImports(code)`; in script mode the code widget repeats the learner's import lines under `if False:` in the harness, so the worker sees them.
143. Done: code widget `budget` (ms, added to the run limit; 30 s extra by default when the code imports numpy, pandas, scipy or matplotlib); `isclose` and `equal` compare arrays, Series and nested lists element by element via `tolist()`.
144. Done: matrix scales the whole drawing to the column when it is wider than 540px.
139. Done: inline code (`.lsn-ic`) and table cells use `white-space: pre-wrap`, so padded output keeps its spaces.
140. Done: code cases take `argv` (script mode): `sys.argv` is `["main.py", ...argv]` for that run; the result row shows `python3 main.py ...`.
141. Covered by graph: pill nodes for names, nodes for objects, and edges re-pointed by a keyed `edges` patch (add, `null` to remove, animated); README-B gives the recipe. No separate `refs` kind.
145. Done: table cells and the table caption render through `ZQ.grade.inline` (with 158).
146. Done: ` ```text ` and ` ```output ` blocks have no Copy button; on other blocks the button sits in a strip above the code (135).
147. Done: see 139.
148. Done: README-B series says marker `i` and shade `from`/`to` are 0-based indices whatever `indexFrom` says.
149. Done: graph `lanes` (labelled dotted lines behind the graph) and node `dashed: true`.
150. Not done: a simulated shell is a project of its own (a POSIX subset interpreter); left for a later pass.
151. Done: `ZQ.canvas.merge` keyed patches remove an item set to `null` (and add a new id); explain clones use the same merge.
152. Done: graph per-node `r` and `shape: "pill"` (sized to the label); edges stop at the rim.
153. Done: table `tap: "rows"`: tapping a cell selects the row `r{i}`; rows take selection, grading colours and a badge in their last cell.
154. Done: inline code wraps in choice options (139).
155. Done: a pair of two tables draws both compact and stacks them whenever either would scroll side by side (ResizeObserver).
156. Done: when the untouched starter errors, Check says the starter is not finished and folds the traceback into "Show the error".
157. Done: AUTHORING.md section 3 notes the `Connection.backup()` hang and the `iterdump` copy.
158. Done: see 145.
159. Done: `console` canvas kind (lines `l1`..., prompt styling, shade, tone, highlight, tap mode); validator and gallery know it.
160. Done: pytest loads from the CDN on first use like numpy (checked: `pytest.approx` and `pytest.raises` run in the widget); its load time is kept out of the limit (161) and counts as heavy for the default budget.
161. Done: the worker posts `pkgs` start, message and end around `loadPackagesFromImports`; the code widget pauses the run's limit while packages load (two minutes of their own) and shows "Loading numpy, pandas" in the results panel.


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

Raised later (mental level 3):

129. A `timed` option on `table` widget screens (countdown, live score, lock on zero) for mental arithmetic sets; or a lesson-level link to the Today warm-up with a target score.
130. `area`: group labels (`labels: { "c11-c16": "£5,070" }` spanning cells); `colSizes`/`rowSizes` patchable (same as 127).
131. `number-line`: interval labels keep "a/b" as inline text unless wrapped in `$...$`.
132. `tap-regions` `only`: accept grid set names (`col7`, `row5`).

Raised later (py-found level 1):

133. `bars`: negative values drawn below a zero baseline.
134. `number-line` (and any kind with `setParam`): unknown control names fall back to `state.params`.
135. Prose code blocks: wrap long lines or scroll horizontally; never run under the Copy button.
136. `code` tests: a per-test `setup` line (run before `call`) so tests read cleanly.

Raised later (py-found level 3):

137. `code` tests: `compare: "raises"` with `expect` the exception name.
138. `tree` canvas: honour `params.label` as a title.

Raised later (py-found level 4):

139. Inline code and table cells: `white-space: pre-wrap` so padded output keeps its spaces.
140. `code` widget: a per-test `argv` list in script mode so `sys.argv` code can be graded.

Raised later (py-found level 2):

141. A `refs` canvas kind (or `graph` with patchable edges): names as labels pointing at objects, re-pointed by a state patch, for aliasing and mutation lessons.

Raised later (numpy-pandas level 1):

142. Done by the orchestrator: `drill-worker.js` now calls `loadPackagesFromImports(code)` before each run, so numpy and pandas load on first use.
143. `code` tests: a per-item `budget` (ms) so the first NumPy run is not charged against the 5 s case limit; `compare: "isclose"` element-wise for arrays and nested lists.
144. `matrix` canvas: scale to the column width when the matrices are wide.

Raised later (git level 1):

145. Table cells and captions: render backticks and bold (same as 98 and 104).
146. Fenced blocks: no Copy button on output-only blocks (` ```text ` or no `$` prompt), or place it so it never overlaps the first line.
147. Table cells: keep leading spaces (`white-space: pre-wrap`, same as 139).
148. README-B `series`: marker `i` and `shade` `from`/`to` are 0-based array indices even with `indexFrom: 1`.

Raised later (git level 3):

149. `graph`: lane/row labels (`lanes: [{ "y": 0.3, "label": "local" }]`) and a `dashed` node style for fetched-but-unmerged commits.
150. A small simulated shell for `sh` scripts (or `code` with `language: "sh"` running a tiny POSIX subset in JS) so loop scripts can be written for real; until then shell is prediction-only.

Raised later (git level 2):

151. `ZQ.canvas.merge`: a keyed patch with `null` removes that item from the list (works in explain clones too).
152. `graph`: per-node `r` and pill-shaped label nodes (same family as 99 and 117).

Raised later (sql level 1):

153. `table` canvas: a row-tap mode (`tap: "rows"`) where tapping any cell selects the row id `r{i}`.
154. Choice options: let inline code wrap (same family as 135 and 139).

Raised later (sql level 3):

155. `pair` canvas with two tables: allow full width per side at narrow widths (auto `stack`) and compact column sizing.
156. Code widget: when the starter itself errors before the learner edits, show a gentler "fill in the starter first" line instead of the raw traceback.

Raised later (sql level 2):

157. AUTHORING.md section 3 `code`: note that `Connection.backup()` hangs in Pyodide's sqlite3; copy a database with `executescript("".join(db.iterdump()))`.

Raised later (pytest level 1):

158. `table` canvas: cells and captions through `Z.grade.inline` so backticks and bold render (same as 145).
159. A `console` canvas kind: monospace block that keeps indentation, line ids `l{i}`, tap mode on lines, highlight (pytest output, tracebacks, shell sessions).
160. pytest in the worker: either a built-in `approx`/`raises` helper module injected when `import pytest` fails, or preloading the pytest wheel set with a larger first-run budget.

Raised later (numpy-pandas level 2):

161. Code widget: package loading (`loadPackagesFromImports`) must run outside the per-case time limit, with a "Loading pandas..." line in the results panel (extends 143).

Raised later (pytest level 3):

162. `boxes`: cards shrink but their text does not (overlap); empty containers default to one slot unless `capacity` is set (same family as 102, 111).

Raised later (pytest level 2):

163. Code widget: a hidden `prelude` field (Python run in the learner's namespace before the starter, not shown in the editor). pytest lessons carry an 18-line stand-in `pytest` class above the learner's code and a 100-line runner below; a prelude would hide both and keep the editor for the learner's own code. The stand-in needs `mark.parametrize`, `fixture`, `approx`, `raises(match=)`, `main()`, `outcome(fn=)` and `count(...)`; see `app/content/courses/pytest/l6-many-inputs.json` for the current shape. Resolves 160.
164. `table` canvas: inline code in cells (backticks) shows literally (dup of 158; pytest level 2 removed the backticks as a workaround).
165. `graph` canvas: labels shrink to unreadable sizes when nodes are close or the canvas is short; set a minimum font size and wrap or truncate instead (pytest level 2 widened the layout to work around it).

Content note (pytest level 2): drawdowns are negative fractions (−0.25) so that "drawdown is never positive" holds; py-found Stage 1 returns them positive. Reconcile when either course is revised.

Raised later (plotting level 1):

166. Validator: accept `b{i}` bin ids in hint highlights on a `bars` canvas (README-B documents them; the validator only accepts `x...` ids).
167. `bars` canvas: a bin-width binding (`params.bins` is fixed), so a slider in `canvas.controls` can re-bin a histogram without a `derive` workaround.
168. `series` canvas: an optional title and a date-format param for the ticks (so the canvas can match matplotlib's `DateFormatter` output in a lesson about date formats).
169. Worker: suppress matplotlib's "building the font cache" line in the Run examples output on the first import.

Note (plotting level 1): matplotlib 3.8.4 and its eight dependency wheels were added to the local CDN folder used for sandbox playthroughs; in the browser they come from jsDelivr as usual.

Raised later (plotting level 2):

170. Validator: `b\d+` ids for histograms in `bars` hint highlights and `curve` (plus overlay ids) in the `distribution` pattern (extends 166; the engine highlights them correctly).
171. `series` canvas: a `fill: "below"` option (shade between a line and zero) to match `fill_between`; drawdown lessons approximate it with `shade` ranges.
172. `pair` canvas: a stacked `series` panel at height 190 shows one y tick even with `y` set; keep at least three ticks at small heights.

Content note (plotting level 2): the log axis (l7 trap, homework h2) and the three-panel figure (homework h1) preview level 3's l9-log-axis, l10-panels and l13.

Raised later (limits level 1):

173. `plane`: a drag point with `on: "f"` cannot follow a function listed in `hide` (hidden functions drop out of the evaluator); keep hidden functions evaluable.
174. `plane`: a dragged point that lands exactly on a hole gets NaN and vanishes with its handle; snap onto the continuation through the hole.
175. `plane`: a per-function `holes: [x]` parameter (drawn as an open circle) instead of faking holes with `open: true` points or two pieces.
176. `plane`: tap mode makes every non-drag point tappable; a per-point `tap: false` (or a `targets` list) so decorative points stay out of tap mode.
177. Validator: the "ladder changes canvas kind" warning fires on table-to-plane ladders that are natural in limits; either downgrade it or add a table-and-plane `pair` pattern to the docs.

Raised later (numpy-pandas level 3):

178. Item prose: Markdown `- ` lists do not render in set items (show as literal dashes); route item prose through the same renderer as lesson prose.
179. AUTHORING.md: note that fenced code blocks fit about 54 characters before they scroll sideways.
180. `table` canvas: a `dim` state for rows (like the grid's), so a join explore can show a dropped row greyed rather than blanked.
181. `series` markers: `{value}` labels round to the canvas `decimals`; allow a per-marker `decimals`.
182. Worker: pandas warnings on stderr (`pct_change` with NaN in pandas 2.2) appear in the learner's test output; filter `FutureWarning` lines, or set `fill_method=None` guidance in AUTHORING.md.

Raised later (plotting level 3):

183. `pair` canvas: tap mode on whole sides (ids `left` and `right`) so "tap the misleading chart" is a canvas action rather than a choice widget.
184. `bars` canvas: opt-in `truncate: true` so `yMin` above 0 is honoured (to show a truncated-axis lie directly).
185. `pair` canvas (stacked `series`): a shared-margin option so plot areas line up across panels (currently about 20 px out, from differing tick and line-label widths).
186. `series` canvas: a second y axis (`y2` series list and scale) for the dual-axis trap.

Raised later (limits level 2):

187. `payoff` canvas: a `value` curve (smooth pre-expiry value) and a `tangent` on it, so delta can be taught on the payoff canvas rather than on `plane`.
188. `plane` and `pair`: `trace: true` on a `derive`-driven point leaves a trail, so a slope-tracing explore draws the $f'$ curve as the learner drags.
189. `area` canvas: a `dim` state; and distinguish pre-shaded regions from a tap selection (different fill or hatch) so an `enter` shade is not read as a selection.
190. `plane` tangents: a `labelOffset` so the slope label can be moved away from the point's own label on steep curves.

Raised later (limits level 3):

191. `area` canvas: let `colSizes` and `rowSizes` be patched from state or a control, so a rectangle with growing sides can drive the product-rule picture (built on `plane` polygons for now).
192. `plane` canvas: implicit curves $F(x,y)=0$ and parametric curves as function entries, with `on` and `tangent` support (circles and ellipses are two half-functions, and a dragged point cannot go round; $x^3+y^3=6xy$ is 120 segments).
193. `plane` with `sketch`: a draggable point looks like a sketch handle; give draggable points a distinct look while sketching.
194. `pair` canvas in the Why? sheet: `stack: true` is ignored (sheet shows the pair side by side).

Raised later (integrals level 1):

195. `plane` tap mode: `area` items, `polygons` and `riemann-{i}` rectangles as tap targets by id (only points are tappable now; "tap the shaded regions" uses placed points).
196. `plane` `riemann`: accept a list (left and right sums on one plane); `sumLabel` through KaTeX.
197. `derive`: read nested state values (`riemann.n`) and add a `sum(expr, k, a, b)` function.
198. `plane` `equal: true`: do not widen the x range past the authored bounds on wide viewports (empty negative-x margin on a [0, 1] plot).
199. `playthrough.mjs`: a `--mobile` flag that also captures a 390 px screenshot per screen.

Raised later (integrals level 2):

200. `expression` widget: `upToConstant: true` (grade antiderivatives by comparing derivatives, or strip an added constant symbol), so `+C`, `+c` and `+K` need not be listed in `accept`.
201. `order` widget: `same` groups of interchangeable lines (as `place` has), so independent derivation steps need not be merged to force one order.
202. `derive`: a numeric `integral(expr, a, b)` function, and let an `area` item's computed `{value}` feed captions and points.

Raised later (integrals level 3):

203. `plane`: a function's `domain` should accept parameter expressions (stop a line at $u = b$ as a slider moves).
204. `plane`: keep x-axis tick labels clear of a curve running just below $y=0$ (nudge labels below or add a halo).
205. `playthrough.mjs`: an option to also screenshot each screen's explanation state after a wrong and a right answer (see 199).

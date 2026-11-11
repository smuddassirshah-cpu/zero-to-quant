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

Fourth pass (items 115 to 132 and 162 to 194):
115. Done: Start over puts each key the screen did not set back to the canvas's first-drawn state (its own defaults) instead of emptying it, so array cells and the like no longer blank; trails clear too.
116. Covered: inline code in table cells renders (145, 158), and a monospaced listing with line numbers is the `console` canvas (`numbers: true`, 159).
117. Done: graph node `shape` "rect" and "diamond" (with "pill" from 152), multi-line labels (`\n`), and tap mode on edges (`tapEdges: true`, or edge ids in the widget's `only`/`among`).
118. Done: table widget cells with a text answer are graded as text, ignoring case and outer spaces, with `accept` spellings; the validator allows them without `tol`.
119. Done: array cells widen to their text (as far as the column allows) and long text shrinks to fit.
120. Done: every code run starts in a fresh, empty working directory (the worker removes the last one).
121. Done: `isclose` fails a string actual ("0.05" is not 0.05).
122. Done: Start over shows only with a canvas-bound widget, a canvas with controls or a draggable point, or an order, place, manipulate or table widget.
124. Done: orderbook `spreadValue: false` hides the spread number (and the mid).
125. Done: number-line controls may bind a free name, which lands in `state.params` for derive (pass 3, item 134).
126. Done: number-line arrow `side: "below"`, overlapping arcs stack in levels, and a zero-length jump is a small loop.
127. Done: area `colSizes.k` / `rowSizes.k` control binds (sign kept), see 191.
128. Done: grid `revealAfterGrade: true` (with `text: "marked"`): a tap selects without showing the text.
129. Deferred: a timed table set (countdown, live score, lock at zero) is a screen mode of its own, close to the Today warm-up; better designed with the mental arithmetic course than added to the table widget. Covered by 454 (a `timed` field on reviews and practice, with a countdown, live score and lock at zero).
130. Done: area labels keyed "c11-c16" span the rectangle between the two cells; sizes patchable (191).
131. Done: number-line interval labels are plain text unless wrapped in `$...$`.
132. Done: tap-regions `only` expands a canvas's set names (a grid's `col7`, `row5`, `cross5`).
156. Follow-ups: nothing new was raised against it; pass 3's starter message stands.
162. Done: box card text shrinks with the cards; an empty container without `capacity` holds as many places as the fullest one (2 to 6).
163. Done: code widget `prelude` and `postlude` (hidden Python before and after the learner's code, in their namespace; line numbers stay the learner's; `__learner_source__` holds their code). Real pytest loads through `loadPackagesFromImports`: `import pytest` in a postlude, write `__learner_source__` to `test_mine.py` and `pytest.main(["-q", "-p", "no:cacheprovider", "test_mine.py"])` runs parametrize, approx and `raises(match=)` (checked in the browser, about 1.7 s once the wheel is cached), so the pytest level 2 and 3 stand-ins can be replaced.
164. Covered by 158: table cells render backticks as inline code.
165. Done: graph labels never shrink below 12px; a long label wraps at a space onto two lines, then ends with an ellipsis.
166. Done: the validator accepts `b{i}` and `exact-b{i}` bin ids on a histogram `bars` canvas (and checks them against the bin count).
167. Done: bars `data` (raw observations) with `bins`: a control bound to `binWidth` re-cuts the histogram (`state.binWidth`).
168. Done: series `title` and `dateFormat` (`%Y %y %m %d %e %b %B`).
169. Done: matplotlib's "building the font cache" line (and stray library warnings) are dropped from the code results.
170. Done: validator `distribution` ids include `curve`, `sd`, `prob` and the overlay ids; bars bins as 166.
171. Done: series `fill: "below"` (or `fillTo`) shades between the line and zero or the baseline.
172. Done: charts keep at least three y ticks on short heights (stacked panels at 190px).
173. Done: hidden plane functions stay evaluable (`on`, tangents, areas), only drawing skips them.
174. Done: a plane point dragged onto a hole takes the limit there instead of NaN.
175. Done: plane function `holes: [x]` draws an open circle at the limit.
176. Done: plane point `tap: false` keeps it out of tap mode.
177. Done: the ladder canvas-kind warning no longer fires between a table and a chart of the same numbers (plane, series, bars, scatter, distribution, number-line, console) or into or out of a pair.
178. Done: prose (lessons and set items) renders `- ` and `1. ` lines as lists.
179. Done: AUTHORING.md notes that a fenced block fits about 54 characters a line before it scrolls.
180. Done: table `state.dim` greys rows, columns or cells.
181. Done: series markers take their own `decimals` for `{value}`.
182. Done: the worker ignores FutureWarning and DeprecationWarning for each run, so pandas notices stay out of the learner's output.
183. Done: pair `tap: "sides"`: each side is one tappable object (`left`, `right`), with selection, grading marks, badge and flash.
184. Done: bars `truncate: true` honours a `yMin` above 0.
185. Done: pair `shareMargins: true` gives two series the same left and right margins (series `margins` param and `margins()` method).
186. Done: series second y axis (`axis: 2`, `y2`, `y2Label`, `y2Format`).
187. Done: payoff `value: { t, sigma, r }` draws the Black-Scholes value before expiry, and `tangent` draws its tangent at the spot labelled with delta.
188. Done: plane point `trace: true` (or "x") leaves a trail as a derive-driven point moves; it clears on Start over or `clearTrace()`.
189. Done: area `state.dim` (a veil over pieces) and a tap selection with a heavy blue edge, distinct from authored shading.
190. Done: plane tangent `labelOffset` (on functions and on curves).
191. Done: area `state.colSizes` / `rowSizes` override params and re-cut the drawing; controls bind `colSizes.k`.
192. Done: plane parametric (`x`, `y`, `t`) and implicit (`implicit`, marching squares) curves as function entries, with `on` (nearest point, so a point goes round a circle) and `tangent` (`at` a point, or `t`).
193. Done: while sketching, a plane draggable point is drawn as a square.
194. Done: the Why? copy is built from the whole canvas spec, so a pair keeps `stack`, `active` and `shareMargins`.
207. Done with 230: the numeric check samples every free symbol.
230. Done: `exprEqual` no longer trusts Compute Engine's `simplify().isEqual()` alone. Whenever both sides evaluate, agreement at 6 seeded points (every free symbol from 0.3 to 3, away from 0 and 1, any number of variables) decides, so `5R` fails for `5\sqrt{R}` and `36\sqrt{xy}-9` for `36xy-9`. Requiring the symbolic check as well would reject true identities it misses (`e^{x+y}` and `e^xe^y`, `\ln(xy)` and `\ln x+\ln y` both come back unequal from it), so it decides only when neither side evaluates to a number (an equation, a set). Scratch test: 17 pairs including two-variable ones, all as expected.
231. Done: AUTHORING.md section 3 notes that NumPy's `solve` and `inv` return nan for a singular matrix in Pyodide, so `raises` cases check `det` and raise in the learner's code.
232. Done in part: parametric and implicit plane curves are documented in README-B (pass 4, 192); a `levels` contour family is not built yet.

Fifth pass (items 195 to 206, 208 to 229, 232 to 271, and the pytest level 2 and 3 conversion):
195. Done: plane tap mode takes areas and polygons by id and Riemann rectangles (`riemann-0`, or `<id>-<i>`) as well as points.
196. Done: plane `riemann` may be a list; each sum label stacks in the top right and is typeset (`sumLabel` through KaTeX).
197. Done: derive reads plain objects in state by name (`riemann.n`, `line.m`), and `sum(a, b, "term in k", name, value, ...)` adds a term over whole k.
198. Done: `equal: true` narrows the frame instead of widening x past the authored range.
199. Done: `playthrough.mjs --shots <dir> --mobile` also saves a 390 px wide screenshot of every screen (`name-390.png`).
200. Done: expression `upToConstant: true` accepts an answer that differs by a constant (extra symbols set to 0, the difference checked constant at 6 points), so `+C` need not be in `accept`.
201. Done: order `same: [["s2", "s3"]]` groups interchangeable lines; the validator checks the ids.
202. Done: derive `integral(a, b, "f(x)", name, value, ...)` (Simpson, 400 strips), and plane area values reach derive and captions as `values.<area id>`.
203. Done: a plane function's `domain` ends may be param names or expressions (`["0", "b"]`).
204. Done: plane tick labels sit in a group above the curves, with a halo.
205. Done: `--why` (with `--shots`) also saves each lesson task's Explanation sheet after the right answer (`-why`), and after a wrong one where the tool can make one, a choice distractor or a numeric answer well off (`-wrong`, `-wrong-why`); the test hook gained `answerWrong()`, `tryAgain()`, `why()` and `closeWhy()`.
206. Done: tangent `length` now spans that many x units, as documented, so a steep tangent is no longer a stub (`lengthPx` unchanged; no course used `length`).
208. Done: plane `state.view: { x, y }` (animates) and `state.zoom: { at, scale }`; a control binds `zoom`.
209. Done: the validator warns on `^` in a derive formula or `{{...}}` caption (it is XOR there) and says to write `pow(a, b)` or quote a curve formula inside `sum()` or `integral()`.
210. Done: curve formulas take `sum(k, 0, n, term)` and `fact(k)`, so a Taylor polynomial with a slider on n needs no per-term switches.
211. Done: `canvas.maxHeight` (pixels, 120 or more) caps the drawing's height (it scales down, centred), so a table widget below stays in view; validator checks it. A side-by-side layout is not added: the lesson column is too narrow for one.
212. Done: series `hlines: [{ id, y, label, dashed, colour, axis }]` in params (inside the auto range) or state; the label goes wherever no series line passes.
213. Done: explore controls take `scale: "log"` (stops at powers of ten from `min`, `perDecade` for more), the readout in units; validator checks `0 < min < max`.
214. Done: the pass gate's gallery check includes a category bars chart (`bars (below zero)`), checked in both themes this pass.
215. Covered by 232.
216. Done: plane heat map `{ heat: "expr", range, colour }` behind everything (cells coloured from the series slot).
217. Done: plane function `labelAt: x` holds a label at that x; others keep clear of it.
218. Done (already possible): `canvas.controls` render on every screen type and grading never reads them; AUTHORING.md now says so (each screen opens at its own `start`).
219. Done: plane function `labelAvoid: false`.
220. Done: a derive write to one array component (`"g.v.0"`) keeps the array an array (in a keyed list item too).
221. Done: plane points `hidden: true` (no dot) as derive-driven polygon vertices, and polygon `sector: { cx, cy, r1, r2, theta1, theta2, degrees }` with curved edges.
222. Done: plane polar areas `{ polar: "r(theta)", inner, from, to }` (limits may be expressions), value ½∫(r² − r₀²) dθ.
223. Done: area `label: "auto"` integrates over the authored bounds, not the visible part.
224. Done: derive and captions read `selected` (the tap selection) and `total(ids)` (sum of the canvas's values; a grid gives each cell's number), for a running total of tapped cells.
225. Done: vectors `angles: [{ id, a, b, label, right, radius }]`.
226. Done: `sliders` widget (two or more sliders graded together, `answer` and `tol` or `check`, `value`, `tol` and `show`; `wrong[].check`), with validator rules and playthrough support.
227. Done: vectors `lockTo: "u"` or `[dx, dy]` holds a dragged head to a line through the origin.
228. Done: a scaled plain-text vector label reads "0.6 × Equity fund".
229. Done: an inline formula of about 34 rendered characters or more may scroll sideways within its line (order lines, Why? text, model answers); short maths is unchanged.
232. Done: plane `{ contour, levels, levelLabels }` draws a contour family as joined polylines, each level labelled; implicit and parametric curves were documented in pass 4.
233. Done: AUTHORING.md documents array targets (`"g.v": "[a, b]"`) and component writes (220).
234. Done: table widget fixed cells and matrix cells print negatives with the minus sign.
235. Done: `{{expr}}` in a matrix cell fills live from params and `state.params`.
236. Done: the matrix `highlight` object form draws (it becomes a list of groups, never keyed-merged into the initial value).
237. Done: manipulate states may carry a `canvas` patch, applied along the path (Undo puts it back).
238. Done: matrix `bar: k` (augmented bar), a pivot ring that grows with wide entries, and `rowOp` defaulting to the matrix that has the rows.
239. Done: plane point labels substitute `{x}` and `{y}` only outside `$...$`.
240. Done: vectors chains resolve the full tail, to any depth.
241. Done (engine breadth pass 2, item 432): the `space` canvas gives the 3D projected view: spans and planes as translucent patches, vectors from the origin or a base, rotation by drag and keys.
242. Done: matrix highlight groups with their own `colour` (a list per matrix).
243. Done: a keyed patch that adds a new polygon id (or point, segment, vector) draws on the live canvas.
244. Done: polygon vertex labels follow derived points (they always did; now documented), and `glyph: true` draws an F in the shape's frame to show orientation flips.
245. Done: a vector added by a state patch takes its `colour` (or the next free slot).
246. Done with 229: wide `$$...$$` and long inline maths scroll in their own box, and the Explanation sheet's grid column can no longer grow past the screen (`minmax(0, 1fr)`).
247. Done: matrix cell widths come from the rendered KaTeX (measured offscreen, cached).
248. Done: matrix `rowLabels` and `colLabels`.
249. Done: vectors `state.matrix` or `state.transform { angle, shear, scale }` draw the transformed grid, basis and unit square; controls bind `m11`..`m22`, `angle`, `shear`, `scale`.
250. Done: scatter `setParam` / `getParam` and derive reach `line.m` and `line.b`.
251. Done: a matrix inside a pair is drawn at its own width (`fit: true`), and a pair with a matrix side stacks when side by side would draw either below 80% (`minScale` on any pair).
252. Done with 247.
253. Done: a vector without `colour` takes a slot no other vector uses.
254. Done: drag-point `{ line: [[x1, y1], [x2, y2]] }` and `{ expr, value, show }` targets.
255. Done: a `sumLabel` that would sit on a vector label moves below.
256. Done: `hidden` applies before `highlight`, so a Why? patch that shows a matrix and highlights it draws (checked).
257. Done: implicit curves are joined into polylines before stroking, so `dashed: true` dashes.
258. Done: a plane point the drag-point widget names is draggable and graded without `drag: true`.
259. Done: scatter `curves` (an `expr`, parametric, or `implicit` for a risk ellipse).
260. Done: matrix `scale` (a factor before the brackets).
261. Done: in a pair's Why? copy a side patch (`{ "right": {...} }`) is applied after the flattened active state, so it wins.
262. Done: vectors `lines: [ids]` (several spans as bands), `segments` (no heads), `head: false`, and the drag constraint (227).
263. Done: bars value labels on negative or near-zero bars sit clear of the baseline, with a halo.
264. Done: matrix operators accept KaTeX.
265. Done: grid default shade colours run 3, 2, 4, 5, 6, 1, so slot 1 blue (the selection colour) comes last; documented.
266. Done: bars `state.dim` (ids or labels) and per-category `dim: true`.
267. Done: `\binom`, `\dbinom`, `\tbinom`, `{n \choose k}` and `n!` are rewritten before grading, and counting answers are compared at whole-number points 1 to 12, so `\frac{n!}{(n-k)!}` and `\binom{n}{2}` grade correctly.
268. Done: on trees with 7 or more leaves shown, labels from the second level on alternate along their branches by subtree rank, an inner branch of a fan of three puts its label near the far end, and labels shrink from 9 leaves (covers 276).
269. Done: tree `state.branching` (a number, a list per level, or `{ "1": 2 }`) shows the first k branches of each node at that level; controls bind `branching` or `branching.1`.
270. Deferred: a drag-between-stars widget is a new interaction (insertion points between cells, a bar token bank); `place` in `order` mode with star and bar tokens (`byText: true`) already grades a stars-and-bars sequence, so a dedicated mode waits for a lesson that needs the array picture itself.
271. Done: the validator treats ★ ☆ ● ○ ■ □ ▲ △ ▼ ◀ ▶ ◆ and the card suits as text unless written with U+FE0F (covers 274).
Content conversion: pytest l5 to l8, review-2 and homework-2 (12 code screens) now import real pytest; one shared postlude defines `run_tests()`, `outcome(fn=planted)`, `count(test=, fixture=)` and `is_fixture()` over real pytest, and every hidden check keeps its meaning (each check gives the same result as the stand-in did, on the starter and on the solution). Level 3 (l9 to l12, review-3, homework-3) never used the stand-in classes: its checks call the learner's test functions directly, so only the "pytest cannot load on this page" comment became `import pytest` (l9, l11, l12, homework-3); prose that recommends `math.isclose` is still true and stays. Level 1 (l4, review-1, homework-1) still carries the stand-in and was outside this brief.

Sixth pass (items 272 to 339, and the pytest level 1 conversion):
272. Done: bars `yScale: "log"` (positive heights; ticks at 1, 2, 5 times powers of ten). A plane category axis was not needed.
273. Done: `lgamma(x)` and `prod(k, a, b, term)` in curve formulas, and `lgamma` and `prod(a, b, "term in k")` in derive; the exact birthday product is `1 - prod(k, 0, n - 1, (365 - k) / 365)` (checked: 0.5073 at 23).
274. Covered by 271 (pass 5): the suits are text in the validator.
275. Done: a `table` widget cell with `bind: "p.a-b"` draws what the learner types on that tree branch as they type, and tapping the branch focuses the cell; the tree takes `state.p` (and "" shows "?").
276. Covered by 268 (pass 5).
277. Done: a dimmed blank grid cell greys its background with a dashed edge.
278. Done: `--shots` waits past the enter patch, then until canvas tweens (a new `ZQ.canvas.busy()` count) and CSS animations settle, at most 3 s, instead of a fixed 300 ms.
279. Done: bars `groups` (two or more bars per category, a legend; values per group, or a sim outcome `[X, Y]`).
280. Done: `derive.let: { name: expr }` intermediates, evaluated in order before the rules and never written; the validator checks them.
281. Deferred: tap-to-classify needs a counting widget bound to the table canvas's row taps (which tally cell a tap adds to, undo, grading against the counts); tap-regions on table rows plus a table widget for the 2 by 2 covers it meanwhile, and the widget is better designed with the lesson that uses it.
282. Done: grid `population: 1000` with `state.groups` (consecutive runs of dots, one tap target per group, `values()` gives the counts); the validator knows the group ids.
283. Done: number-line `scale: "log"` and `"log-odds"` (natural-unit values, ticks and labels; `format: "percent"`).
284. Done: a capital I beside l, I or 1 (and a lone "I") in canvas SVG text is set in the serif face, so "Ill" no longer reads "III"; the canvas font is unchanged elsewhere.
285. Done: derive reads `params` (the canvas's params: `params.data[n]`) and arrays in `params.params` by name (`data[n]`); documented.
286. Done: `sim.filter` discards trials; they are not counted, and the trial count says how many were discarded.
287. Done: table widget cell `unit: "%"` (answer as a fraction, typed as a percentage, a % sign after the input).
288. Done: on a fan of three or more first-level branches the labels move along their branches, away from the root.
289. Done: boxes `size: "large"` (or "medium", or a number) and a `door` item kind.
290. Done: tap-regions `answer`, `among` and `wrong` sets take set names (`cross2`), expanded by the canvas; the validator accepts grid set names there.
291. Done: distribution `discrete` family (`values`, `probs`) and `cdf: true` (steps with closed and open dots, or the curve).
292. Done: the `slider` widget binds through the canvas's own `setParam` first, as `canvas.controls` do, so a bars category label moves its bar.
293. Done: grid `margins: true` (or given sums): row and column sums and the total outside the cells, hidden by `state.margins: false` until a patch, not part of named sets; ids `rsum1`, `csum1`, `total`.
294. Done another way: typing goes into a `table` widget cell with `bind: "cells.r2c3"`, which fills that grid cell live (margins update). Typing straight into grid cells is not added: the table widget already grades, marks and reveals typed answers.
295. Done: balance move `remove-unknown-part` (take k of an unknown, such as 1/2, from both pans); the canvas's `removeUnknownBoth`, the solver and the validator know it (E = 1 + E/2 solves as take E/2, divide by 1/2).
296. Done: scatter `sim: { n, rho, seed, mx, my, sx, sy }` (a control on `rho` re-correlates the same draws) and `values().r`.
297. Done: the validator warns when an item has both `prose` and a `prompt` (item-level or a longform widget's), since prose replaces it; and a longform widget's `prompt` now shows when there is no prose (it was never drawn). Seven homework items warn now (sql h3, py-found h4, pytest h2 and h3, plotting h1 and h2, testing h3): content agents should merge each prompt into its prose.
298. Done: bars `xAxis: "value"` with `state.transform: { a, b }` slides categories to aX + b on a numeric axis.
299. Done: discrete distribution ticks fall on every integer when there is room (else every 2nd, 5th, 10th), and a discrete family's axes follow its support as a slider moves n (`axes: "grow"` keeps the old behaviour).
300. Done: distribution `hypergeometric` family (`N`, `K`, `n`).
301. Done: bars `state.pivot` (a fulcrum under the axis, draggable with `drag: true` or a drag-point number target) and `showMean` (the weighted mean); no separate seesaw canvas.
302. Done: series controls bind `reveal`, `revealAt` (an index) and `markers.<id>.i`; a marker with `i: "reveal"` rides the end of the reveal.
303. Done: a sim outcome may return a list (`[X, Y]`), drawn as grouped bars (279).
305. Done: distribution `lognormal` family (with `showMedian` and mean markers), and shading bounds that are expressions in the params (`"mu - sigma"`).
306. Done: plane function `zeroOutside: true` (0 beyond its domain, drawn flat along the axis, so areas past the end shade correctly).
307. Done: distribution `drag: true` gives shade handles on an explore screen without a widget.
308. Done: bars `curves: [{ expr }]` reading params, state.params and the bin width `w`, so an overlay follows n.
309. Done: a distribution shade with `under: "<overlay id>"` fills under the overlay curve (hatched) separately from the bars; a bars curve takes `shade: { from, to }`.
310. Done: series `xScale: "log"` and `xStep`.
311. Done: derive `matmul`, `matpow(P, k)`, `vecmat(v, P)` (checked: π0 P^3 on a two-state chain).
312. Done: graph edge `loopAngle`.
313. Done: array `wrap` (cells per row, or true), ranges drawn row by row.
314. Done: graph node `valueSide` (or `state.valueSide`).
315. Done: walk `model: "markov"` (`states`, `P`, `start`), state paths as steps on a labelled y axis; the validator checks the matrix shape.
316. Done with 308: a curve (in state, patchable) over a data histogram on one set of axes.
317. Done: `rug` on distribution and plane (ticks, or sticks up to the density or a named function).
318. Done: plane `yAxis: "left"`; a long `xLabel` (or `xLabelPos: "below"`) sits below the ticks; and a plane whose y range starts at 0 now reserves room for its x tick labels, which used to spill under the drawing toward the caption.
319. Done: README.md (pair) and AUTHORING.md say that the right side's same-named params win in derive, and to prefer distinct names or `left.n` and `right.n`.
320. Done: distribution `shade` as a list (summed label) and `observed` marker lines.
321. Done: sim `let` bindings and `tstat(k)`, with `sample`, `mean`, `sd` and friends, so a t statistic of one sample simulates directly.
322. Done: bars `state.cut: { at, side, colour, label }`, bindable `cut.at`.
323. Done: walk per-barrier hit counts (`{up}`, `{down}`, `hitCounts()`), `xStep`, and a `{ "reseed": true }` control (a button that draws the next seeded run); the default "Step" x label now has room.
324. Done: tree `state.leaves` (every leaf has a value slot).
325. Done: overlay params may be expressions in the main params, and derive addresses an overlay by id (`nrm.params.mu`); documented.
326. Done: `sim.outcome` reads params and state.params by name (a slider re-runs the stream, which jumps rather than animates), and `mean(k, expr)`, `var`, `varp`, `sd`, `sum` draw k fresh values.
327. Done: a series `sim` with a running statistic (mean, varp, var, sd, sum); per-sample statistics are outcomes such as `mean(10, n())`.
328. Covered by 211 (pass 5): `canvas.maxHeight` caps a tall grid.
329. Done: the validator accepts "all" and `cross5-3` in grid hint highlights, overlay ids from state as well as params, and named shade regions and observed markers on a distribution.
330. Done with 309 and 320: several regions, one of them under an overlay (alpha and beta at once).
331. Done: `erf(x)` and `Phi(x)` in curve formulas and derive.
332. Done: bars `hlines` (params or state).
333. Done: the graph frame narrows to the column on a phone (down to 300 wide) and re-spaces, so node labels keep 12px; `fitWidth: false` keeps 540.
334. Done in part: below 480px the code editor's gutter narrows and its text steps down to 13px (CSS only), so about 44 characters fit before a line scrolls. Soft-wrapping is not added: the line-number gutter and the highlight layer would have to measure wrapped rows, which belongs in the editor code the C++ work is changing now.
335. Done: `--why` also shoots each review and homework item's Explanation sheet (the set-mode hook gained `why()` and `closeWhy()`), and an exam's result page with every explanation open.
336. Done: payoff tap targets `strike-<leg>`, `breakeven` (numbered when several), leg lines and `total`.
337. Done: payoff `drag: "spot"` (or a drag-point widget naming `spot`).
338. Done: payoff `showTotal: false` (legs drawn solid, spot dots per leg) and a leg's `labelAt`.
339. Done: payoff leg `floor: false`.
Content conversion (level 1): pytest l4, review-1 and homework-1 (5 code screens) now import real pytest and carry the shared postlude, with a Run examples call `run_tests()` that prints pytest's report; the "stand in for pytest" sentences are gone from their how text and prose. Their hidden checks call the learner's tests directly and keep their meaning; the five homework-1 `parse_row` breaks now use `outcome(parse_row=planted) == 'failed'`, because real `pytest.raises` fails with pytest's own Failed (a BaseException the code widget's raises check does not catch) where the stand-in raised AssertionError. Checked on starter and solution against the stand-in versions; their playthroughs pass.


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

Raised later (limits level 4):

206. `plane` tangent `length`: measured along the line in data units, not in x units as the docs say; on steep curves with unequal axes the tangent is nearly invisible. Scale by x, or correct AUTHORING.md and README-B.md (authors use `lengthPx` meanwhile).
207. `expression` widget: the numeric second opinion samples one variable only; two-variable answers such as $a/(2c)$ are unreliable (`0.5a/c` rejected). Sample every free symbol.

Raised later (taylor level 1):

208. `plane`: bindable view ranges (`state.view: { x, y }`) so a slider can zoom in on a curve near a point (the tangent-approximation hook fakes it by rescaling the function).

Raised later (taylor level 2):

209. Live captions: `^` in a caption formula is not a power (unlike curve formulas), so values go silently wrong; either accept `^` in captions or make the validator warn on it.
210. `plane` curve formulas: a partial-sum helper (`sum(k, 0, n, term)`) so Taylor polynomials with a slider on $n$ need no per-term switches (see 197).
211. Table widget beside a compact canvas pushes the table below the fold; allow a `canvas.height` cap or a side-by-side layout on wide screens.

Raised later (taylor level 3):

212. `series` canvas: horizontal reference lines (`hlines: [{ y, label, dashed }]`), for a limit such as $\pi^2/6$ across a partial-sum chart.
213. Controls: a `scale: "log"` slider option (stops at 1, 10, 100, 1000) whose readout shows the value, not the exponent.
214. `bars`: during integration pass 4 a `rebin` edit briefly broke every category bar chart (read `params.bins.width` with no bins); keep a gallery check of a category chart in the pass gate.

Raised later (multivar level 1):

215. `plane`: a contour mode (`{ "contour": "x^2+y^2", "levels": [...] }`) that draws closed level curves without the two-halves gap at vertical tangents (same need as 192).
216. `plane`: a filled heat map of a two-variable expression (colour ramp over the view) as a background layer.
217. `plane` function labels on dense contours get pushed to the plot edge and out of order; place labels along the curve at a chosen x instead.
218. Controls on non-explore screens: allow `canvas.controls` on ladder and problem screens (read-only to grading) so a slice slider can persist through a ladder.

Raised later (multivar level 2):

219. `plane`: `labelAvoid: false` on a function so background contours do not push point and vector labels away (see 217).
220. `derive`: writing one array component (`"g.v.0"`) turns the array into an object; either support numeric path segments or document that the whole vector must be set.

Raised later (multivar level 4):

221. `plane` polygons: vertices may be `derive`-driven points with `hidden: true` (no dots), and a sector or annulus-wedge shape `{ r1, r2, theta1, theta2 }` with curved edges.
222. `plane` areas: a polar region (`r` and `theta` limits) as a shadable area, not only between $y = f(x)$ curves.
223. `plane` area `label: "auto"` reads low when shading stops at the plot edge; integrate the expression to the authored bounds, not the visible ones.
224. `grid`: a live caption or `derive` that reads the current tap selection (running total of tapped cells).

Raised later (vectors level 1):

225. `vectors` canvas: angle marks between two arrows (`angles: [{ a, b, label, right: true }]`), so right angles and the θ arc in the cosine proof need not move to `plane`.
226. Grading two sliders together: a `sliders` widget (or `slider` with `params: [a, b]`) graded as a pair, for "find a and b that reach the target".
227. `vectors` drag: hold a dragged head to a line (`on: "span"` of another vector, or `lockTo`) for projection drags.
228. `vectors` labels: scaled plain-text labels render as "0.6Equity fund"; put a space or the scale in maths before a text label.
229. Long inline KaTeX in `order` lines, Why? text and longform model answers neither wraps nor scrolls on a phone; let an inline maths span overflow onto its own scrolling line.

Content note (vectors level 1): Stage 0 `counting` l9 to l13 already teach arrows, adding, length, dot product as P&L, the cosine proof and beta as a projection. Vectors level 1 uses new numbers and contexts; consider trimming `counting` or framing vectors level 1 as revision-plus.

Raised later (vectors level 3, multivar level 3):

230. Grading bug: `exprEqual` (grade.js) accepts `x` for `\sqrt{x}` because Compute Engine `simplify().isEqual()` agrees at 0 and 1; `5R` passes for `5\sqrt{R}`. Always cross-check numerically at several random points for every free symbol, including with two or more variables (covers 207).
231. Pyodide 0.27.7 NumPy 2.0.2: `np.linalg.solve` and `inv` return nan for an exactly singular matrix instead of raising `LinAlgError`; AUTHORING.md should say `compare: "raises"` cannot rely on NumPy's own singular-matrix errors.
232. `plane`: `implicit` and parametric curves exist in plane.js but are undocumented; document them and add a `levels` option for a contour family of $f(x,y)$ (resolves 192 and 215).
233. `derive` writing an array target (`"g.v": "[...]"`) works but is undocumented; document it (and see 220).
234. Negative numbers in fixed `table` widget cells and numeric `matrix` cells print a hyphen, not a minus sign; format like the table canvas.
235. Live `{{...}}` values inside a typeset matrix cell do not update; allow caption-style substitution in matrix entries.

Raised later (elimination level 1):

236. Bug, `matrix`: the object form of `highlight` (`{ "A": { "rows": [1] } }`) never draws, because the initial `highlight` is `[]` and `ZQ.canvas.merge` treats the object as a keyed-list patch; use a non-array initial value or skip keyed merging when the existing list is empty.
237. `manipulate` widget: a per-state `canvas` patch, so each tapped algebra step can animate the canvas (elimination steps on a `matrix`).
238. `matrix`: an augmented bar (`bar: k`, a separator before column k) instead of two matrices with op "|"; a pivot circle that grows with wide cells; `rowOp` should default to the matrix that holds the rows named.

Raised later (elimination level 2):

239. `plane` point labels substitute `{x}` and `{y}`, so `$\mathbf{x}$` renders as a coordinate; add an escape for literal braces (or only substitute `{x}`/`{y}` outside maths).
240. `vectors` chains: an arrow drawn `from` another arrow starts at that arrow's head measured from the origin, ignoring its tail; resolve the full tail so head-to-tail chains of three or more need no `derive`.
241. `vectors`: a simple 3D projected view (isometric or rotatable) for column spaces and nullspaces in $\mathbb{R}^3$.

Raised later (elimination level 3):

242. `matrix` highlight: with the object form fixed (236), support more than one wash colour (crossed-out row and column in one, the minor block in another), as README-B's cofactor form implies.
243. `plane` polygons: a keyed `enter` patch that adds a new polygon id does not draw on the live canvas (it does in the Why? copy); make live keyed additions render.
244. `plane` polygons: vertex labels that follow derived points, or an "F" glyph, to show orientation flips.

Raised later (vectors level 2):

245. `vectors`: an arrow added by a state patch with a new id draws in black, ignoring `colour`; apply styling to patched-in arrows.
246. Why? modal on phones: wide `$$...$$` or long inline maths widens the whole modal and pushes the diagram off-screen; scroll the maths in its own box as lesson prose does (same family as 229).
247. `matrix`: cell width is estimated from the LaTeX source, so KaTeX entries such as `\cos\theta` overlap; measure the rendered width.
248. `matrix`: row and column headings (`rowLabels`, `colLabels`) for factor-model screens.
249. `vectors`: a matrix-driven transformed grid, unit square and basis arrows whose entries (or an angle and a shear factor) bind to sliders.

Raised later (least-squares level 3):

250. `scatter`: let `derive` read and `setParam` write `line.m` and `line.b` directly (authors bind free params and derive the line, and every Why? patch must then set `params` rather than `line`).
251. `pair` of two `matrix` canvases scales each half until a 2x2 and a 3x3 are hard to read; keep a minimum font size and stack instead (same family as 155, 185).

Raised later (least-squares level 2):

252. `matrix`: size KaTeX cells from the rendered width (`\tfrac{5}{6}` comes out wide and tiny); same root as 247.
253. `vectors`: a vector with no `colour` takes slot i+1, so two vectors can share a colour by accident; document in README-B or assign distinct defaults.

Raised later (least-squares level 1):

254. `drag-point` widget: a line target, or a target checked by an expression (`2*v.x + v.y == 0`), so "drag until the dot product is 0" accepts any point on the orthogonal line.
255. `vectors`: `sumLabel` collides with a vector label when the sum's head coincides with it; offset or suppress automatically.
256. `matrix`: a cell highlight in an explanation patch that also un-hides the matrix does not show in the Why? panel (apply `hide` before `highlight`).

Raised later (eigen level 2):

257. `plane` implicit curves: `dashed: true` draws solid because each marching-squares segment restarts the dash pattern; join segments into polylines before stroking.
258. `drag-point` widget on `plane`: `points()` filters on `drag: true`, so a point without it grades silently as its id; either document that `drag: true` is required or include ids the widget enabled.
259. `scatter`: draw a curve over the cloud (implicit curve for a risk ellipse, or a `points` cloud style on `plane`).
260. `matrix`: a scalar factor outside the brackets (`scale: "\\tfrac{1}{\\sqrt{2}}"`).

Raised later (eigen level 1):

261. Bug, `pair` Why? panel: an `explain.canvas` patch under the active side's key (`{"right": {...}}`) is overwritten because `get()` flattens the active side to the top level and `set()` applies it after the side patch; apply side patches last.
262. `vectors`: `span` should allow two or more lines at once (several eigen-lines as bands); a plain line or segment without an arrowhead; a drag constraint to a line (same as 227, 254).
263. `bars`: value labels for negative or near-zero bars sit on the category label at the baseline; offset them.
264. `matrix`: operators between matrices accept KaTeX.

Raised later (counting-chance level 1):

265. `grid`: the default shade colour (slot 1) is the same blue as `selected`, so a pre-shaded event on a tap screen needs an explicit `colour`; pick a distinct default and document it.

Raised later (eigen level 3):

266. `bars`: a `dim` state (or per-bar `dim: true`) to de-emphasise bars, for "keep the largest singular values".

Raised later (counting-chance level 2):

267. `expression` grading: Compute Engine 0.30.2 cannot parse `\binom` and never equates symbolic factorial ratios (`\frac{n!}{(n-k)!}`); pre-process `\binom{n}{k}` and `n!` into a product form (or a `Binomial` function the numeric check can evaluate) before equivalence testing. Until then, counting answers must be polynomials.
268. `tree`: probability labels on the third level of a tree with 7 or more leaves overlap between neighbouring subtrees; stagger or shrink labels on deep trees.
269. `tree`: let a control drive the number of branches per level (`derive` on `levels` or `branching`), for "options per stage" sliders.
270. `array`: a drag-to-place widget (drag bars between stars) rather than `tap-regions`.
271. Validator: ★ is treated as an emoji; whitelist common geometric symbols (★ ● ■ ▲) used as tokens.

Raised later (counting-chance level 3):

272. `bars`: `yScale: "log"`; or category labels on a `plane` x axis (`xLabels`), so a log-scale chart by category needs no numeric stand-in axis.
273. `plane` expressions and `derive`: `lgamma`, `prod(k, a, b, term)` and a running product over integers (the exact birthday product needs a Stirling workaround now; see 197, 210).
274. Validator: allow the card suits ♠ ♥ ♦ ♣ in prose alongside 271's symbols.

Raised later (conditional level 1):

275. `tree` with the `table` widget: a tree-bound fill mode (tap a branch, type its probability, see it drawn on the branch) rather than values appearing only in the Why? sheet.
276. `tree`: automatic label spacing on 8-leaf and 3-branch trees (same as 268).
277. `grid`: `dim` on blank cells is invisible; hatch or grey the cell background.
278. `playthrough.mjs --shots`: capture after `enter` animations settle (wait for the animation promise, not a fixed 300 ms).

Raised later (conditional level 3):

279. `bars`: a grouped mode (two series per category with a legend) for side-by-side distributions.
280. `derive`: named intermediate values (`let`-style rules evaluated before the others), so a sub-expression need not be inlined into every rule.
281. `table` widget bound to a `table` canvas: let row taps feed counts into a 2x2 tally (tap-to-classify).

Raised later (conditional level 2):

282. `grid`: a population mode (1,000 small dots, groups shaded by count, tap a whole group) for natural-frequency lessons; cells are 24px minimum now, so about 20 columns at most.
283. `number-line`: `scale: "log"` and `"log-odds"` with readouts in the natural unit (see 213).
284. Canvas label font: capital I and lowercase l are indistinguishable ("Ill" reads "III"); use a font with a distinct I, or a serif on capital I in canvas labels.

Raised later (conditional level 5):

285. `derive`: a documented way to look up values by index from a lesson-defined array (`params.data[n]`); authors currently stash arrays under `pair.left.params.params`.
286. `bars` simulation: a documented `filter` (skip a trial when a condition fails) so the trial counter and counts exclude discarded trials.
287. `table` widget: a `%` unit per cell, as the `numeric` widget has.

Raised later (conditional level 4):

288. `tree`: first-level probability labels crowd near the root when branches have different numbers of children; offset each first-level label along its branch.
289. `boxes`: a `size` option for cards (or a door item) so three large items can fill the canvas.
290. `tap-regions`: let `answer` use grid set names (`cross2`), as `only` already does.

Raised later (random-vars level 1):

291. `distribution` canvas: a custom discrete support (`values`, `probs`) and a CDF step mode with open and closed endpoints (CDFs are built on `plane` from one constant function per step now).
292. Bug or doc mismatch: a `slider` widget bound to a `bars` category label moves the thumb but not the bar, while `canvas.controls` honours the same binding; make the widget path match (authors use a free parameter plus `derive`).

Raised later (random-vars level 4):

293. `grid`: a `margins` option (row and column sums computed and drawn outside the cells, revealable by patch, excluded from named sets such as `row1`) for joint tables.
294. `grid`: an editable mode (type into cells) so "fill the product of the margins" need not move to a `table` widget plus a `pair`.
295. `balance` canvas: allow taking a fraction of the unknown from both pans (`E/2`), so $E = 1 + E/2$ can be solved in the natural order.

Raised later (random-vars level 3):

296. `scatter`: a native `rho` parameter or a seeded `sim` option that generates correlated pairs, so a live correlation slider needs no per-point `derive` rules.
297. Validator: warn when a set item gives both `prose` and `prompt` (`prose` silently replaces `prompt`).
298. `bars`: a movable category axis (values as positions) so $aX + b$ can slide along the axis without moving to `plane`.

Raised later (limits-thm level 1):

299. `distribution`, discrete families: x ticks drop to every second integer (or only 0) on narrow ranges; always tick every integer on a discrete support, and keep the range right when a slider changes $n$.
300. `distribution`: a `hypergeometric` family (N, K, n).

Raised later (random-vars level 2):

301. A native `seesaw` canvas (masses at values, draggable pivot graded against the mean) or a `bars` option for a draggable mean marker; the see-saw is built on `plane` polygons now.
302. `series`: bind `reveal` and a marker index to a slider directly, without `derive`.
303. `bars` simulations: allow a trial to return two values (X and Y side by side) rather than stacking two simulations in a `pair`.
304. Done: C++ in the browser. The `code` widget takes `"language": "cpp"` (`js/engine/widgets/cpp-grade.js`, `js/screens/cpp-worker.js`; code.js delegates in one line). Runtime: YoWASP Clang 21.1.4 (`@yowasp/clang@21.1.4-3` on npm, clang and lld compiled to WebAssembly with wasi-libc and libc++), fetched once from jsDelivr (about 26 MB compressed, 102 MB unpacked) or from `app/vendor/yowasp-clang/` when the CDN is unreachable; a WASI preview 1 shim runs the compiled program in a separate worker that is killed on a time-out, so the compiler survives. One compile per Check with a generated harness (one function per case, JSON-like output behind a sentinel, compared in JS); script mode compiles the learner's `main` as it is and feeds `stdin`; `compare: "raises"` matches an uncaught exception type (or a base) or any abnormal exit; `prelude`/`postlude` with `#line` so diagnostics name `main.cpp` lines; precompiled headers for the starter's includes built by a second, short-lived compiler; libc++ debug hardening. Limits: C++17, no `try`/`catch` (a throw always terminates), no files or threads. binji's wasm-clang was evaluated and not used (clang 8 from 2019, demo code, only on GitHub). Validator, playthrough (`--local-cdn` serves `yowasp-clang-21.1.4-3/package/`), gallery (two C++ cards) and AUTHORING.md section 3 (C++ addendum) updated.

Raised later (limits-thm level 2):

305. `distribution`: a `lognormal` family (μ, σ) with shading and median and mean markers; shading bounds that bind to parameters directly (authors use `derive` on `shade.from` and `shade.to` now).
306. `plane` functions: a `zeroOutside: true` option so a density is 0 beyond its `domain` rather than undefined (areas past the end then shade correctly).
307. `distribution`: drag handles on an explore screen without a graded widget (handles turn on only through `drag-point` now).

Raised later (limits-thm level 3):

308. `bars`: a continuous overlay curve (`curve: { expr }`) that follows parameters, so unstandardised sums can be compared against $N(n\mu, n\sigma^2)$ as $n$ changes.
309. `distribution` and `bars`: shade an overlay curve's area from a cut (the continuity-correction strips) separately from the bar wash.
310. `series`: a scaled or log x axis (`xScale`, `xStep`) so long simulations need no thinning to "tens" or "hundreds".

Raised later (markov level 2):

311. `derive`: `matpow(P, k)` and `vecmat(v, P)` functions so a slider on $k$ can drive $\pi_0 P^k$ on `bars` or `graph` for any chain, not only ones with closed forms.
312. `graph`: a per-edge `loopAngle` for self-loops (they always point away from the centroid and collide with neighbour edges on a line layout).

Content note (markov): level 2 writes plain $P$ and $\pi$ to match the course.json objective; the notation rule says bold capitals for matrices. Settle one convention for the course when level 1 lands.

Raised later (markov level 1):

313. `array`: cells never shrink below 30px, so more than about 16 cells clip in the Why? modal; add a `wrap` option or a smaller minimum width.
314. `graph`: a per-node choice of side for the distribution value label (it always draws under the node and collides with downward self-loops; see 312).
315. `walk`: a seeded Markov-chain mode (`states`, `P`, `start`) so state paths can be simulated live rather than precomputed and indexed in `derive`.

Raised later (estimation level 2):

316. `bars` and `distribution`: overlay a fitted curve on a data histogram in one chart (an `exact` curve as a state patch), so a fit need not be a `pair` with misaligned axes (see 308).
317. `plane` and `distribution`: a data-rug option (density sticks at given x values) for likelihood-as-a-product pictures.
318. `plane`: an option to draw the y axis at the left edge rather than at $x = 0$; and keep a long `xLabel` clear of `state.caption`.
319. Docs: on a `pair`, the right side's same-named parameters override the left's in `derive`; document and prefer distinct names.

Raised later (testing level 1):

320. `distribution`: more than one shaded interval (`shade: [{from, to}, ...]`) for two-sided tails, and an observed-value marker line.
321. `bars` simulation: simple local bindings in outcome expressions (or a built-in `tstat(n)` sampler) so a statistic such as $\bar x/(s/\sqrt n)$ can be simulated.
322. `bars`: a rule-driven colour threshold (`state.colours` from one rule, or `highlightAbove: x`) so a slider can recolour every bar beyond a cut.

Raised later (markov level 3):

323. `walk`: `showHits` should count hits per barrier (top and bottom separately); whole-number x ticks (`xStep: 1`); a documented re-seed control (`controls: [{ "reseed": true }]`).
324. `tree`: leaf labels patchable from state (reveal prices in an explanation).
325. `distribution`: document addressing an overlay by id in `derive` (`nrm.params.mu`) or bind overlay parameters to sliders directly.

Raised later (estimation level 1):

326. `bars` simulation: let `sim.outcome` read `state.params` (so a slider on sample size re-runs the simulation) and add `mean(k, expr)` and `var(k, expr)` helpers (an outcome now repeats a 100-value `pick` ten times).
327. Simulations: a "statistic per sample" mode and a running statistic (running mean of the divide-by-$n$ variance), so convergence pictures need not be precomputed `series`.
328. `grid`: a size cap for grids with many cells (a 10x10 grid is about 540 px tall and pushes the question below the fold).
329. Validator: accept `"all"` in a grid hint highlight (the engine accepts it), and overlay ids on a `distribution` hint highlight when the overlay is given in `state`.

Raised later (testing level 2):

330. `distribution`: shade a second region under an overlay curve (α and β at once), extending 320.
331. `plane` expressions: `erf(x)` and `Phi(x)` so power-against-n curves can be drawn as functions.
332. `bars`: a horizontal reference line (`hlines`, as 212 asks for `series`).

Raised later (exams 1.3 and 1.4):

333. `graph` on phones: the canvas draws in a fixed 540px frame so labels shrink to 7 to 8px at 390px width; scale the layout to the viewport and keep the 12px minimum from 165.
334. Code editor on phones: lines scroll sideways at 390px; soft-wrap long lines or shrink the gutter.
335. `playthrough.mjs --why`: cover exam and set items' explanation sheets, not only lessons (see 205).

Raised later (options level 1):

336. `payoff`: tap targets on legs (`strike-{id}`, `breakeven`) so `tap-regions` can ask "tap the strike".
337. `payoff`: a draggable `spot` handle for "drag the expiry price" (only a slider bound to `spot` moves it now).
338. `payoff`: `showTotal: false` to hide the combined line, and a per-leg label position, so several positions at one strike read clearly.
339. `payoff`: a leg option to draw without its floor (`floor: false`) for the "forgot the right not to exercise" picture.

Content note (pytest): level 1 (l4, review-1, homework-1) still uses the pytest stand-in; convert to the shared `postlude` pattern that levels 2 and 3 now use.

Raised later (testing level 3):

340. `plane`: a point with `on: "f"` should stay on its curve when a control or an explanation moves its x (now only while dragged).
341. `plane` and `derive` expressions: `qnorm`, `pnorm` (with 331's `erf` and `Phi`).
342. `bars` sim: `maxn(k, expr)` or a `repeat` helper, and a catch-all category (`"4+"`) so capped outcomes need no `min` trick.
343. AUTHORING.md: document the lesson `code` widget's `solution` field (used by the playthrough).

Raised later (estimation level 3):

344. `distribution`: a `beta` family (a, b) with shading, for posteriors and credible intervals.
345. `plane` reference lines: spread labels apart when two labelled lines sit close (one label vanishes now).
346. A native intervals chart (many confidence intervals from repeated samples with a "count misses" readout); 100 intervals now take 300 `derive` rules.
347. `bars` histograms: bin edges that fall on the data's grid of values put boundary values in different bins than a node check does; document the half-open convention and make it `[lo, hi)`.
348. `number-line`: negative tick labels print a hyphen rather than a minus sign (same family as 234).
   Also raised: review equations L3 to L4

Raised later (regression level 2):

349. `console`: a `compact` or font-size option so 80-column output (a statsmodels summary) shows verbatim (about 60 columns fit at 14px).
350. `scatter` `curves`: a `thin` style or per-curve opacity for bands of resampled fits.
351. Validator: accept `fit`, curve ids and residual ids (`r-p{i}`) as `scatter` highlight targets (the engine renders them).

Raised later (micro level 1):

352. `orderbook`: bid and ask levels as patchable state (add a resting limit order, remove a level), not params only.
353. `orderbook`: a `decimals` option for the footer's average fill price, and a spread readout in pence or basis points (`spreadUnit`).
354. `boxes`: patchable item labels (a card reading "You 200" then "You 300"), and a `row` drop position that is not always the end.
355. `derive`: chained `params.*` rules (a value computed from another computed value) come out wrong in the explanation's copy of the canvas; evaluate rules in dependency order in the Why? copy too.

Raised later (markets level 1):

356. `table` widget: per-cell `byValue` feedback (name a specific wrong value) alongside 287's `%` unit.
357. Controls: a `stops` list for a slider (1, 2, 4, 12, 52, 365) in addition to 213's log scale.

Raised later (regression level 1, trees level 1):

358. `scatter`: marked points that join neither the fit nor the SSE (an $(\bar x, \bar y)$ marker), a second readout (sum of absolute residuals), whole-number x ticks, and a label slot for a second straight line.
359. `tree`: patchable `state.labels` and `state.leaves` (node and leaf values from state and from `derive`), so a slider can relabel nodes live and a learner can fill the tree in place (with 275 and 324).
360. `table` widget: per-cell `wrong` values with their own feedback keys (the `numeric` widget's `wrong[]`), extending 356.

Raised later (markets level 2):

361. `plane`: a percent tick format for an axis (`xFormat: "%"`), and `series` values bindable to a slider (see 302).

Raised later (options level 2):

362. `payoff`: per-leg label position (labels sit at 6% along the range, on the flat part of a call), extending 338.
363. `payoff`: legs as patchable state (quantity, add or remove a leg), so a `place` of legs can build a position live.
364. `place` widget: let placed tokens drive a canvas patch (`onPlace` state), so dropping a leg redraws the payoff.

Raised later (regression level 3):

365. `scatter`: colour points by group (`group` per point with a legend).
366. `plane`: document `derive` targets for `vlines` and `hlines` entries so limits can move with a slider.
367. A canvas that regenerates a seeded residual or return series from a parameter (an AR(1) slider redrawing residuals); none can now.

Raised later (C++ runtime):

368. C++ runtime: the YoWASP sysroot has no unwinder, so `try`/`catch` cannot work (a `throw` ends the program); find or build a sysroot with exception support, or document that the C++ courses teach exceptions by reading and `raises` cases only.
369. C++ runtime: show whatever a case printed before a timeout; add a C++ section to AUTHORING.md section 7 (validation rules); re-check the `bundle.js` file-write patch on any YoWASP version bump.

Raised later (micro level 2):

370. `orderbook`: bid and ask sizes as slider and patch targets (`bids.0.1`), with 352; and a `midDecimals` option so a £50.005 mid is not rounded to the price decimals.

Raised later (markets level 3):

371. `payoff`: stock legs (forwards and shorts) get a draggable entry price (or an `F` marker) and a kink label, so "drag F until the payoff is X" works.
372. `plane` sketch: the x-axis title collision check should include the sketch's own control points.
373. `series`: a step style (or a vertical top-up marker) for balances that jump, such as a margin account after a call.

Raised later (trees level 2):

374. `tree`: a recombining (`binomial`) mode: up-down and down-up paths share a node, step labels on an axis, a price and a value slot per node that `state` patches, `derive` and a `table` widget can fill. Trees 2 draws the lattice with `graph` rectangles by hand instead.
375. `plane`: point labels that show a value (`£{y}`) take a decimals option (`£{y:.2f}`), so a £100 leaf can read £100.00.

Raised later (micro level 3):

376. `orderbook`: `bids` and `asks` as patch, `derive` and control targets, and an optional fair-value row (`fair`, `halfSpread`, `skew`) that sliders bind to, so the learner's own quotes move in the book (extends 352 and 370).
377. `table` canvas ignores `canvas.maxHeight`; a fill-in ladder with a canvas table and a widget table needs a scroll on a laptop.
378. `code` `isclose`: a per-test `tol` (relative or absolute) so a simulation can be accepted within a stated tolerance rather than needing a fixed draw order.

Raised later (options level 3, trees level 3):

379. `payoff`: several `value` curves on one chart (a list for `value`, each with a label), so vega and theta can show two curves; and a plain cash leg, so "short share plus cash" need not be a stock leg with its entry at the strike.
380. Formula language (`plane` curves, `derive`, captions): built-in `erf`, `normcdf` (Φ) and `normpdf`, so Black-Scholes curves and live option values do not need hand-written polynomial approximations (options 3 used tanh, trees 3 a long polynomial).
381. `longform` prompts do not render Markdown tables; either render them or say so in AUTHORING.md section 4.
382. `bars`: the number of categories is fixed in params; let `derive` or a slider change the category list so one bar per tree leaf can follow n.

Content note (trees): l5 and the first screens of l7 grow cash by (1 + r) per step; l6 introduces e^{rΔt} explicitly and l6 onwards use it (checked by the exam 1.7 agent). The second reader for topic 1.7 should check the l5 to l6 handover reads cleanly.

Content gaps (second reader, topic 1.3), to fill in a later gap pass once every course is written:

383. Calculus coverage against the MIT 18.01 and 18.02 exit lines: no improper integrals with an unbounded integrand (integrals l7 promises them), no partial fractions, trigonometric substitution or trig powers, inverse trig functions, related rates, volumes of revolution, arc length, hyperbolic functions; the mean value theorem is used but never taught; multivar has no triple integrals or Jacobian, and Lagrange only in two variables with one constraint. Candidate: an extra level in `integrals` (techniques) and one extra lesson each in `limits` (MVT, related rates) and `multivar` (Jacobian, Lagrange in three variables).

Raised later (ds level 2):

384. `array`: pointers as tap targets ("tap the pointer that should move"), not only the cells under them.
385. `series`: a label size or offset option for `{value}` markers, so ten labelled points fit at 540 px.
386. A compact chart beside a `table` without shrinking axis text (`maxHeight: 180` makes a `series` axis unreadable); a `compact` mode or a wider `pair` split.

Raised later (algo-think level 1):

387. `array`: a built-in step control with a step counter (every stepper is now a slider plus `derive` lookups); re-layout when `cells` changes length (1 to 16 cells drew a stacked column); check that `state.active` set by `derive` shows in the Why? copy (unconfirmed).
388. `plane` with `yScale: "log"`: right-end curve labels drift away from their curves with six curves.
389. `derive` cannot build an object (braces forbidden), so `highlight: {"range": [...]}` cannot be derived; allow a derived object or a `range` shorthand.
390. `table` widget: a numeric-looking text answer is graded as a number ("1" for "O(1)"); add a normalised big-O comparison (strip "O", spaces, case) so typed complexity answers need no `accept` lists.

Raised later (ds level 1):

391. `choice` options: a fenced code block inside an option renders as broken inline code; support multi-line code in options.
392. `boxes`: containers sit in one row and shrink to 60%; wrap onto a second row or offer a grid layout for five or more buckets.
393. `array`: an insert-and-shift action like `swap`.
394. `code`: a per-test time budget (the limit is 5 s times the number of tests, so a quadratic attempt waits 30 to 45 s), a timeout reported against the test that hit it, and a way to count operations for complexity checks.
395. `code`: expose `__learner_source__` to tests always, not only when a prelude or postlude exists.

Raised later (algo-think level 2):

396. `tree`: per-node label and value patches after the drawing opens (to fill in return values call by call), and arrowheads so calls and returns can be told apart by direction (with 374 for recombining).
397. `array` stack mode: frames size to the widest text in any state, not the starting `cells`.

Raised later (graphs-dp level 1):

398. `graph`: an ordered tap mode (`ordered: true`) that grades the sequence of taps and shows badges 1, 2, 3, so BFS and DFS visit orders can be tapped on the graph itself.
399. `graph` pills with `lanes` at 390 px touch each other (with 333).
400. Playthrough: take the desktop screenshot after any `enter` patch has run (about 350 ms), not 300 ms after the screen opens.

Content gaps (second reader, topic 1.4), to fill in the gap pass with 383:

401. Linear algebra against the MIT 18.06 exit line: not taught anywhere are du/dt = Au and e^{At}, similar matrices, complex and Hermitian matrices, the pseudoinverse and Cholesky; vector spaces only informally; the exam has no least-squares code built from the normal equations or QR and no PCA in code. Duplication to cut to make room: elimination l9 repeats vectors l10 to l11 (determinant as area), least-squares l5 is the third pass at projection onto a line.

Raised later (cpp level 1):

402. C++ `code` widget: a per-widget `flags` option (for example `["-Wall"]`) so a screen can show a warning under the editor; the worker compiles without `-Wall` now.
403. C++ `code` widget: several named source files compiled and linked together, so a learner can cause and fix a multiple-definition or undefined-reference linker error (now shown only as console screenshots).
404. Playthrough: the previous screen's "Correct." toast is still visible in the next screen's screenshot (cosmetic; with 400).

Content note (pass 6, item 297): seven homework items have both prose and a longform `prompt`, so the prompt is hidden: sql h3, py-found h4, pytest h2 and h3, plotting h1 and h2, testing h3. Merge each prompt into its prose in the next fix pass for those courses.

Raised later (ds level 3):

405. `array` stack mode: a cell label separate from its value ("i2" above "6"), so a monotonic stack can show indices and values without shrinking text.
406. `graph`: named pointers attached to nodes (`pointers: {slow: "n2", fast: "n4"}`) that move by patch, like `array`'s `pointers`, so linked-list lessons need not patch pill positions and null old edge ids.
407. `manipulate` widget: reject a wrong op in place with its `why` (no dead-end state), halving the state count of stepping screens.

Raised later (graphs-dp level 4):

408. `grid`: a table-fill mode (`params.edit: [ids]`) graded per cell, with the cells a cell depends on highlighted as the learner focuses it, so a DP table can be filled on the grid itself (now a `table` widget under a `grid` that repeats it).
409. `tree`: values on inner nodes (with 396), so backward induction can show V₂ and V₃ on the drawing.
410. `grid`: two-line cell text (a fee and a running total).

Raised later (algo-think level 3):

411. `tap-regions`: a sequence mode that grades the order of taps on `array` cells (with 398 for `graph`); and a widget that grades the order after an `array` drag-reorder.
412. `tree`: stack rows per level or enforce a minimum font size when `maxHeight` caps a deep or wide-labelled tree.
413. `number-line`: intervals as tap targets, not only points.
414. AUTHORING.md section 3: note that `__learner_source__` is visible only in `prelude` and `postlude`, so a "no `sorted`" check sets a flag in a postlude (with 395).

Raised later (graphs-dp levels 2 and 3):

415. `graph`: README-B says edges are directed by default but `graph.js` draws them undirected unless `params.directed` or `edge.directed` is set; fix one or the other.
416. `graph`: edge labels as KaTeX; circle node radius fixed from the first labels (longer labels set later are cut off); a side panel for auxiliary state such as a heap's contents.
417. `tree`: a `state.dim: [paths]` to grey out pruned branches (`collapse` hides and does nothing on a leaf).
418. `grid`: `state.mark` badges sit in the cell corner and `null` in a patch prints "null" instead of removing the badge; offer a centred glyph and treat `null` as removal.
419. `code`: the time limit is 5 s times the number of cases for the whole run, so a slow-but-correct solution cannot be caught per case (with 394); agents now count reads with a hidden list subclass or time inside a test.

Raised later (ds level 4):

420. `tree`: a binary-tree mode: explicit left and right slots (a single child drawn on its side, no ∅ placeholders needed), a tappable root, per-node `highlight` and `shade` (now the whole path from the root), with 374, 396 and 409.
421. `orderbook`: `bids` and `asks` as state patches so a book can step through add, cancel and limit-order messages on one screen; order-id labels (with 376).
422. AUTHORING.md: there is no `build(values)` tree helper; either add one to the Python prelude library or remove the claim from briefs (each lesson defines `Node`, `build`, `to_list` in its prelude).

Content gaps (second reader, topic 1.5), to fill in the gap pass with 383 and 401:

423. Probability against the Stat 110 exit line: missing moment generating functions, continuous joint densities with marginals and independence, transformations and convolution, continuous order statistics, Beta, Gamma, negative binomial, multinomial, chi-square, t and bivariate normal, the law of total variance, Jensen's inequality, the strong law, Poisson process properties, reversibility and MCMC; covariance and conditional expectation only in discrete form. The exam never tests covariance, Poisson, exponential, hypergeometric, lognormal, reflection or absorption, and every item is one step. Duplication to cut: conditional l2 repeats counting-chance l7; counting-chance l9 screens 1 to 5 repeat l3; limits-thm l1 and l2 repeat random-vars.

Raised later (maths breadth pass, task 2b):

424. Done: validator checks `strand` ("quant" or "pure") and `strandNote` (non-empty when `strand` is set; an error without `strand`); rules in AUTHORING.md section 7 and 9. Checked on a scratch copy with four bad cases.
425. Done: "Pure maths" and "Quant" badge (`ZQ.content.strandBadge`, `.strand-badge` in components.css) on Learn course cards, topic chip rows and topic exam chips, the course page, the lesson start screen and the Review exam list; `strandNote` is the tooltip and screen-reader detail; untagged courses and mixed topics show none.
426. Done: setting "Quant path only" (`settings.quantOnly`, You, Settings): `content.stages()` and `courses()` drop pure courses and all-pure topics, so Learn, Today, Review, the mastery map and stage "topics passed" counts skip them. `topic()`, `course()`, `stage()`, `allStages()` and `allCourses()` are unfiltered.
427. Done: Learn shows a topic's `exit` as a "Target" line; a topic exam with no file shows "Not written yet" on Learn and Review (`content.examWritten`); a course with no written lessons opens without error everywhere (routes playthrough).
428. Open (small): stage hours on Learn still show the full curriculum figure with "Quant path only" on, and the Paths view (Stage 2 and 3.2 optional card) is not filtered.

Raised later (breadth briefs 0.6, 1.10, 1.11, markov L5; PLAN task 2b engine item "breadth visuals and complex grading"):

429. Done (engine breadth pass 2, grading): `exprEqual` compares real and imaginary parts at every seeded point when an `i` appears (own complex evaluator over MathJSON; `1/(1+i)` = `(1-i)/2`; `3-4i` and `0` rejected); real-only grading unchanged (1,837 pairs identical).
430. Done: complex-aware `isclose` in the Python harness (`cmath.isclose`, same tolerances, NumPy complex too) and the C++ harness (`std::complex` printed as `{ re, im }`, `expect: { re, im }`, `CHECK_CLOSE` takes complex); defaults kept (rel 1e-9, abs 1e-12), per-case `tol` already existed.
431. Done (plane): `field`, `slopeField` and `trajectory` layers (slider-bound formulas, `normalise`, `colourBy: "magnitude"`, fixed-step RK4 from a draggable point or fixed `starts`, `values()` `<id>EndX` and `<id>EndY` for derive); arrow and step counts capped.
432. Done: the `space` canvas (rotatable 3D in SVG: drag, keys and pinch rotate and zoom; points, vectors, curves, surfaces, spans and planes, fields; slider-bound formulas; depth order by painter's algorithm) and the `complex-map` canvas (a z-plane beside the image of its grid under f(z), slider-bound f, draggable z, `p1.u` and `p1.v` for derive).
433. Done: one `expression` takes a vector or matrix (`(2, -1, 3)`, a `pmatrix`, `\langle\rangle`), compared entry by entry; wrong size returns key `length` with a line.
434. Done: `order` `distractors` (a "Left out" list, keys: distractor ids and `left-out`); `same` groups already existed (item 201).
435. Done (vectors): `state.matrix` (or `transform`) maps every vector not marked `fixed: true`, drags store the preimage (pseudo-inverse when singular), and derive reads `matrix`, `m11` to `m22`, `det`, `trace` and `image.<id>`, and can write `matrix`.
436. Done (walk): overlays `sq`, `ratio`, `bankroll` and `expr` as panels under the walk, average at stopping (`showStopped`, `stopAt`, `drawn`), `lower` and `upper` bindable to sliders, `model: "ou"`, and `values()` for derive.
437. Done: `\min`/`\max` (rewritten to (a+b-/+|a-b|)/2), capital `N` and `D`, and `\epsilon` = `\varepsilon` in expression answers (text fallback too).

Raised by engine breadth pass 2 (the `space` canvas, `complex-map`, grading):

438. `space`: drag in 3D. A draggable point or vector head (held to a plane or an axis, for example the xy-plane at fixed z) with `points()` and `place()`, so the `drag-point` widget works on a 3D point; the camera basis for the ray to plane maths is already in `space.js`.
439. `space`: true 3D arrowheads. Heads are flat screen-space triangles, so a vector pointing at the viewer shows only a dot-sized head; a small cone built from quads would also help depth cues.
440. `space`: exact intersections. Painter's order is per piece, so two large interpenetrating pieces (a plane and a surface cutting through each other's middles) can show a jagged seam; a cut line (plane against surface, level curves, contours on a surface) would fix it and is useful in its own right.
441. `space`: opt-in `wheel: true` zoom and an `autoRotate` camera patch (left out so a wheel does not hijack page scroll).
442. `space`: a `tangent: { surface, at }` shorthand for tangent planes and gradient helpers (authors can build them from `planes` with `through` and `normal` formulas today).
443. `space`: smooth shading. Cells are flat-shaded in 16 levels, so a coarse surface shows its cells; Gouraud shading needs per-vertex colour, so the likely route is more cells within the budget or a bitmap for surfaces only.
444. `space`: highlight glow across interleaved pieces. The glow is a filter per run of pieces, so when other objects sort between an object's pieces the later run lies over the earlier one (cosmetic, seen on a vector lying in a highlighted plane).
445. Done by `complex-map` (item 432): the other half of the 3D item, a z-plane grid beside its image under f.
446. `expression`: a bare `i` is now the imaginary unit, so a real answer that uses `i` as an index or variable is read as complex and both parts are compared. Only `markov/homework-3` does this (`i(20-i)`, `20i-i^2`: identical polynomials, so it still passes); authors should use `k`, `j` or `n`. A warning in the validator for a bare `i` in a real answer would catch new cases.
447. `drill.js` keeps its own Python `isclose`, which compares floats only; it needs the same `cmath` branch if a drill ever returns complex values.
448. `complex-map`: tap mode, a domain restriction on the grid (lines span the whole visible z-plane), curve labels, and a conformal-grid option for unequal units are not built.

Raised later (Today and topic exams):

449. Done: a passed topic exam now counts as tested out. `ZQ.content.topicPassed` and `courseTestedOut` read `S.exams` at call time (no migration, existing passes apply at once); Today, Learn and the course map skip tested-out courses in `currentCourse` unless a lesson is open to resume, falling back to them only when nothing else is left. Exam result copy updated; Due queue and progress figures unchanged.

Raised later (interview plan, engine pass A; the five bullets E1, E2, E4, E5 and E6 of `docs/briefs/interview-plan.md` section f, report `docs/reports/engine-interview-a.md`):

450. Done (E1): per-paper `scoring: { right, wrong, blank }` and `passNet` in `exam.js` (a paper with neither keeps `pass` as a share of the marks). Marks are tallied per paper with `ZQ.mock.tally`; the results page headlines the net score with right, wrong and blank counts and each question's marks; the attempt keeps `net`, `max`, `wrong` and `blank`. Validator rules for the fields.
451. Done (E2): `navigation: "forward"` and `skip: false` on a paper: one question at a time, no navigator, Mark or Back, no jumping ahead, the answer locks on moving on; with `skip: false` the next question opens only after an answer (Enter moves on; Skip appears when skipping is allowed). Short papers warn in the last quarter of the clock rather than the last five minutes.
452. Done (E4): `{ generator: "arith", mix, n, options }` entries in a paper expand to seeded single-choice items (`js/engine/arith.js`, shared with the Today warm-up, which now calls the same `ZQ.arith.problem`). Near-miss distractors: reverse operation, misplaced point, slipped digit. The seed is per attempt (or `#exam/<id>/<seed>`) and stored on the attempt. Generated items never join the redo queue.
453. Done (E5): the mock exam kind `exams/mock-<id>.json` with `style` and `models`, in `exam.js` (start card, papers, checks, result with a score trend), in `ZQ.content.mocks()`, on Review under "Mock assessments" (latest, best, trend, Sit again) and in the You exam history with net scores; exempt from the topic skill-coverage rule; no XP; every attempt kept. `content/exams/mock-sample.json` is the engine sample (not a real assessment).
454. Done (E6, covers 129): `timed: { seconds, lockAtZero }` on a level review file, and `#practice/timed/<seconds>` for practice; a countdown pill and live score in the set header, `ZQ.player.runSet` handle `finish()`, and a summary note when time runs out. Bank decks (E7) will pass the same field to the same set page. Not built: a timed homework, and a timer on lessons.

Raised later (prep tags, brief `docs/briefs/prep-tags.md`, report `docs/reports/engine-prep-tags.md`):

455. Done: prep paths from one file, `content/prep.json` (schema in AUTHORING.md section 10). `ZQ.content.prep*` loads it (listed in the manifest, so no 404) and indexes lesson to paths, a course or level ref expanding to its lessons. Validator checks refs, mock ids, stage and track, the `why` length and copy rules, firm `asOf`, `source` and `reported`, unknown fields, and warns when a firm path is over 12 months old (`--prep <file>` checks a scratch copy). One "Interview prep" chip on a Learn course card and on a course map lesson node, with the stages and firms in the node detail and the chip tooltip. New `#prepare` page (`js/screens/prepare.js`): General, stage and role, or firm; steps with must or should, done, in progress or not yet written, the why line, mocks; "Reported formats, as of <month year>" on firm paths. Linked from Learn and from Review's "Mock assessments"; path names in the Today search. "Quant path only" unchanged; nothing is gated. `content/prep.json` holds only two engine sample paths (`general`, `firm-optiver`); the full mapping is a content pass. Playthrough covers `#prepare` and one deep link per path kind under `--routes-only`, at `--mobile` too.

Raised later (interview plan, engine pass B; items E7 and E9 of `docs/briefs/interview-plan.md` section f and three `tags` bullets, report `docs/reports/engine-pass-b.md`):

456. Done (E7): the interview question bank. `content/bank/<family>.json` (validator: shape, `tags`, `role`, `style`, `source`, `requires`; manifest lists it; `ZQ.content.bankIds()` and `bank(id)`), an "Interview practice" card on Review and the `#bank` deck (`ZQ.select.bankDeck`, `bankStatus`). Each item has its own Leitner schedule in the saved state (`doc.bank`, `ZQ.state.bank`, `bankResult`): 1, 3, 7 then 30 days, a right answer up one box, a miss back to box 1 and due in 1 day. The deck deals due items first, then new ones, one family at a time, and never draws an item whose `requires` lessons are unfinished. Tagged quiz, review and homework items of finished lessons feed the deck under their own uid (cheap: the existing practice pool, filtered on `tags`). Old saves load unchanged (`bank` and `timing` default to empty). `content/bank/sample.json` is the engine sample (ten items adapted from reviews, answers checked twice). Not built: SM-2 with a self-rated ease, folding the weekly problems in, `timed` on a deck, tagged lesson screens in the pool (the redo resolver already reads screens, so it is small), and a bank draw for exam papers (E3).
457. Done (E9): per-item timing. `runSet` stamps `seconds` on each checked result; the exam screen counts the time each question was open. A results line (`ZQ.mock.pacing`) gives the average, the slowest families (by first tag, else first skill) and the items over their `pace`; shown on every set summary and on the exam result, with each question's seconds. Exam attempts keep `itemSeconds`; `ZQ.state.timing.families` keeps n, seconds and over-pace per family from exams, practice and the bank deck. Optional `pace` (positive seconds) on any item, lesson screen or drill, validated. Grading never reads time. Not built: a stored timing history for reviews, redo and homework, a readiness view over `ZQ.state.timing` (E18), and a stopwatch on lessons.
458. Done (the five inbox bullets on `tags`): `tags` is defined in AUTHORING sections 2 and 5 and checked by the validator on lesson screens, quiz, review, homework, exam, mock and bank items and drills (a non-empty list of kebab-case names, no duplicates). The engine reads it (deck and pace line). Not built: a registry of family names to check a tag against (a misspelt family is a valid kebab word); the bank files themselves are the only list.

### Engine pass B: status

- 456 (E7, bank and Interview practice): done.
- 457 (E9, per-item timing and `pace`): done.
- 458 (`tags` shape and documentation): done.

Raised later (interview plan, engine pass D; inbox bullet E12 and the "running ledger" bullet, report `docs/reports/engine-pass-d.md`):

459. Done (E12): the `trade` widget, `js/engine/widgets/trade.js` (a pure game that also runs under Node, plus the widget), over the `orderbook` canvas. Per turn the learner sets bid, ask and size; a seeded counterparty (`noise` with `rate` and `reach`, `informed` with `edge`, `scripted` list of `hit`/`lift`/`none`; a list of them by `turns` range) trades at the quoted price; cards on a `schedule` (text, a `fair` that moves the mark, `reveal` of the hidden value); `limit` cuts an oversize quote and counts a break; `spread` bounds and crossed or locked quotes count breaks; a live ledger (position, cash, mark-to-market, realised, average cost) and per-turn lines; the hidden `value` settles after the last turn; results box with every turn, the counterparty type and each trade's edge. Grade: final P&L against `benchmark` or `band`, then rule breaks against `maxBreaks`; keys `low`, `high`, `limit`, `crossed`, `spread`. Deterministic under `seed` (draws from seed and turn only); `strategy` is required and replayed by the test hook, Show solution and the playthrough. Validator: shape of every field, and the strategy played through the real game (error when it misses the target or breaks a rule, warning when the untouched opening quote already passes). Sample: `content/exams/mock-trade-sample.json`.
460. Done (the ledger bullet): `carry`. A widget with `carry: "name"` stores the learner's value when its screen is checked or revealed (a number, the sliders map, or the trade ledger `{ pnl, position, cash, realised, mtm, breaks, turns, value }`); a later screen reads `{{carry.name}}`, `{{carry.name.pnl}}` or `{{carry.name|fallback}}` in any string of its spec (canvas state, prose, a numeric `answer`); a whole-string placeholder becomes the number. Validator: carry name shape, and a read with no earlier store is an error. In `player.js` (`carryResolve`, `carryReset`, called when a lesson or set starts).

### Engine pass D: status

- 459 (E12, `trade` widget): done.
- 460 (running ledger, `carry`): done.
- Inbox bullets integrated: E12 and the running ledger bullet. The game-theory `play` bullet (rounds against a seeded opponent) names E12 as a relative but is not answered by it and stays in the inbox; the mm-games level 1 and 2 bullets (`table` wrong ids, `sliders` boolean checks, number-line interval drag, log tick separators) are unrelated to E12 and stay.

Raised later (user bug report: Today still showed 0.1 after its topic exam was passed; report `docs/reports/engine-today-tested-out.md`):

461. Done: a part-open lesson in a tested-out course no longer pins Today, Learn or the course map. `currentCourse` returned the saved resume course before the tested-out filter, so any unfinished lesson in a passed topic kept it as the main lesson (and its exam card). New `ZQ.content.resumeStands(resume)`: a resume in a tested-out course counts only if its position was saved after the passing attempt (a deliberate revisit); otherwise the first not-tested-out course from the start stage is chosen, and the exam card follows it. No lesson progress is changed and the lesson stays on Learn. Not author-facing, so no AUTHORING note.

462. Done: `node tools/playthrough.mjs --bank <file>` (repeatable, or `--bank all`). Plays every item of a bank file through the real deck: unlocks the file's `requires`, clears the bank schedule, walks other items to the 30-day box, deals decks, answers each item right from its key (longform: ticks the rubric) and reports pass or fail per item and a total. Covers the inbox bullet "Playing bank items" (Bank sessions 2, 3, 4 and session 1). Not built: `uid` in `ZQ.test.current()` (the flag records each deal by wrapping `bankDeck`) and a wrong-answer pass.
463. Open (inbox, three votes): `ZQ.test.answerWrong(id)` for numeric, choice and expression widgets in lesson and set mode, so a script can route each `wrong` id and distractor to its line (`%` values scaled, `.opt[data-id]` clicked).
464. Open (inbox, four votes): `node tools/validate.mjs --dups <file>`, listing course, exam and bank items that share an item's first tag and parameters or key.
465. Open (inbox, two votes): `choice` with `shuffle: true` in a set page seeds the shuffle from the slot, not the item, so a returning bank item shows the same option order; seed by uid and seen count.
466. Done: removed `content/bank/sample.json`; the routes `#bank` check now reads its counts from the bank files (drawable, locked, unique uids, `bankStatus`) instead of assuming the sample (115 drawable of 200 in 20 files, 85 locked).

### Engine pass C (4 Nov): scope
Sources: `docs/briefs/interview-plan.md` section (f) (E3, E8, E11, E13, E14); `docs/BACKLOG-INBOX.md` sections "Raised later (brief research-int / systems / coding-int, 4 Nov)", "Raised later (fix pass ... brief, 4 Nov)" and "Raised later (topic 3.5 briefs, engine requirements, 4 Nov)"; field shapes in the engine sections of `docs/briefs/research-int.md`, `coding-int.md`, `systems.md`. Reports `docs/reports/engine-pass-c-<a|b|c|d>.md`.
467. Done: `parts` on review, homework, exam, mock and bank items (never quiz). Parts of any widget kind except `longform`, code included; part k+1 opens once part k is checked; credit is parts right over parts; unopened parts count as missed (timed lock settles the open part). Code parts have cumulative tests (`cumulative: false` opts out). Files: `app/js/engine/player.js` (`renderParts`, runSet part handling), `app/js/engine/mock.js` (`tally` credit), `app/js/screens/exam.js`, `app/js/screens/review.js` (set summary, homework marks and draft), `app/js/engine/select.js` (practice filter; `E.parts` now read only for `kind: "paper"`), `app/css/screens/lesson.css`. Validator: `checkParts` (2 to 6 parts, allowed fields, no item-level widget or feedback, no longform part, no code part in bank, quiz refused, merged code tests at most 15, `cumulative` boolean, stage-style `kind` refused). Report `docs/reports/engine-pass-c-a.md`.
468. Done: `draw: [{ from, tags?, difficulty?, n }]` on mock and stage-exam papers (topic exams refuse it), sources `bank/<file|prefix|*>` and `drills/<pack|id|*>`; seeded, family-balanced, unseen items first; attempt keeps `seed` and `drawn`. Drills become `code` items (drill `prelude` maps to widget `postlude` for Python). Files: `mock.js` (`draw`, `seenOf`), `exam.js`, `content.js`. Validator: `checkDraw` plus `verifyDraws` (source exists, pool at least n, warning below 2n), drill `pack` kebab-case. Report `docs/reports/engine-pass-c-a.md`.
469. Done (E14, C-data-cap): `data: { "name.csv": "content/data/<path>" }` on a Python `code` widget (lesson, quiz, review, homework, exam and mock items) and on a drill file. Each file is fetched once (`ZQ.content.dataFiles`, `app/js/content.js`), cached, and written into the working directory before every run, through the existing `files` mechanism in `app/js/engine/widgets/code.js` (before `prelude`, so the learner's code, `prelude`, `postlude`, `setup` and hidden `tests` all open it by bare name). A drill gets it as `spec.prelude` in `app/js/screens/drill.js` (hidden tests are expressions that read the file inside `call`). A closed "Data files in the working directory" panel under the editor shows each file's size and first six lines; `dataPeek: false` hides it (CSS in `app/css/widgets.css`). Cap: 256 KB a file, text (UTF-8) only. Validator rules (`app/tools/validate.mjs`, function `dataFiles`): `data` not a non-empty object; name not a bare file name; name also a key of `files`; path not under `content/data/`, containing `..`, or not an existing file; file over 262,144 bytes; file not UTF-8; `data` on a C++ widget; `dataPeek` not boolean. Checked on every widget the validator walks and on drill files. Report `docs/reports/engine-pass-c-b.md`.
470. Done (C-alloc-check): `allocCheck: true` on a C++ `code` widget gives `alloc_count()` and `reset_alloc_count()` (`app/js/engine/widgets/cpp-grade.js`: `ALLOC_CNT`, `ALLOC_OPS`, `LEAK_COUNTED`). One volatile `int` counter bumped by the global `operator new`, `operator new[]` and their `std::nothrow` forms (which call `malloc`); the counting rule is the brief's (whole program since the last reset or start-up, harness and setup included, `malloc` not counted). With `leakCheck` the leak wrapper's own operators are patched to bump the same counter, so the two coexist (two sets of replacement operators would not link). The unit is compiled with `-fno-builtin` when `allocCheck` is on (added to the worker's flag allow-list in `app/js/screens/cpp-worker.js`; authors cannot write it). Validator: `allocCheck` not boolean or on a Python widget; a hidden `prelude`, `postlude` or `files` source with `operator new` or defining `alloc_count`/`reset_alloc_count`; warning when no test reads `alloc_count()`. Report `docs/reports/engine-pass-c-b.md`.
471. Done (E13, with E13-blocked-lanes and the systems brief requirements): `interleave` canvas (`js/engine/canvas/interleave.js`, `css/interleave.css`; HTML in the canvas wrapper, readable at 390 px in both themes). Fields: `params.lanes` (1 to 3 lanes, 8 steps a lane, 24 in all; `id`, `label`, `short`, `steps`, `regs`), `vars`, `locks`, `outcome` (variables, `"a.r1"`, `{ label, of }`), `endings` (renames complete, deadlock, asleep), `notation` (`words`, `assign`); steps `load add store set fetch-add lock unlock wait notify`, each with an optional `if` expression, or `ops: [...]` run as one step with `text`; `state.schedule` (lane ids stepped: the whole state), `state.outcomes` (`true`, `"found"`), `selected`, `highlight`, `caption`. A lane whose next step is a held lock is disabled and drawn blocked; no steppable lane ends `deadlock` (a lane blocked on a lock) or `asleep` (only sleepers left); a `wait` sleeps until a later `notify`. Tap mode marks steps (ids `a1`, `t1-2`). `values()` for derive: shared values, `ending`, `steps`, `order`, `outcome`, `regs`, `reached`, and the enumeration `outcomes`, `outcomeList`, `schedules`, `complete`, `deadlock`, `asleep` (memoised walk over states, cached per spec). Methods `step`, `play`, `finish`, `undo`, `reset`, `enabled`, `ending`, `outcomes`. Validator rules: lane count and size, ids unique, op and per-op fields, names in expressions, variables and locks exist, reserved variable names, `outcome` entries, `endings` keys, `notation`, `state.schedule` and `enter.schedule` replay legally, `state.outcomes`, enumeration under 200,000 states, unlock-without-lock warning, `tap-regions` ids checked against the step ids; an `explore` screen on this canvas needs no controls. Player: Start over and the tap hint know it. Gallery: five cards. Sample: `content/exams/mock-interleave-sample.json` (`"sample": true`). Files: `js/engine/canvas/interleave.js`, `css/interleave.css`, `index.html`, `js/engine/player.js` (two one-line edits), `js/screens/system.js`, `tools/validate.mjs`, `canvas/README-B.md`, `docs/AUTHORING.md` (section 4 and 7). Report `docs/reports/engine-pass-c-c.md`.
472. Done (E8, with C-drill-patterns): drill library. A drill file may carry `language: "cpp"` (graded by the C++ code widget and `cpp-grade.js`, so the cases are `call`/`args`/`types`/`expect`/`compare`; nested `std::vector<std::vector<int>>`, `std::vector<long long>` and `long long` documented in AUTHORING section 3 and exercised by two sample drills), `pattern` (one slug of a fixed vocabulary, `PATTERNS` in `js/screens/drill-lib.js`, read by the validator), `pace` (seconds), `tags` and `sample: true`. Every drill page shows a stopwatch (pause, restart, pace; amber past the pace) and records its reading with each submit (`ZQ.state.drills.time`, `runs` and `best` on the drill record). `#drill` has pattern, difficulty-range and language filters (kept in `ZQ.store 'drill.filters'`). `#drill/session` (and `#drill/session/<id>` for a set session file `drills/sessions/<id>.json`) sits two drills against one 60-minute countdown with a tab per drill, resume after leaving, auto-close at zero, and a result screen (time on each drill, hidden tests passed, solved) kept with `ZQ.state.drills.session` (`doc.drillSessions`, last 50). A lesson reads the latest session as `{{carry.session.minutes1|minutes2|passed1|total1|passed2|total2|solved|minutes}}`. Files: new `app/js/screens/drill-lib.js`, `app/css/screens/drill-lib.css`; edited `app/js/screens/drill.js` (list filters, stopwatch, options, routing), `app/js/content.js` (`drills()` merges manifest metadata; `drillSessionIds`, `drillSession`), `app/js/state.js` (`drills.time`, `drills.session`, `drills.sessions`, `drillSessions`), `app/js/engine/player.js` (`carry.session`), `app/js/core.js` (pause icon), `app/index.html`, `app/tools/validate.mjs`, `app/tools/playthrough.mjs`, `docs/AUTHORING.md` (sections 3, 5, 7). Validator rules: `language` not python or cpp; `pattern` outside the vocabulary; `sample` not boolean; ids `index`, `session`, `sessions`; a C++ drill checked as a C++ code widget (3 to 15 tests, case shapes, `types`, `compare`, `tol`, flags, budget), empty starter, no `solution`, no example; warning for `fn` on a C++ drill; `CPP_TYPES` now include the nested and `long long` vectors; session files (id is the file name, `drills` exactly two different existing ids, `minutes` 10 to 180, `sample` boolean, unknown field a warning); `manifest.json` lists `drills/sessions/*.json` and gains a `drills` map (language, pattern, pace, tags, sample per file); a sample drill needs no `index.json` row; `{{carry.session...}}` is always allowed in a lesson. Playthrough: `--drill <id>` (repeatable), `--drills`, `--session`; `--routes-only` now also checks the list filters and the session setup. Report `docs/reports/engine-pass-c-d.md`.
473. Done (merge, main session): drill packs reconciled between 468 and 472. `drills/<pack>` in a `draw` matches a drill whose optional `pack` field is `<pack>`, whose id starts `<pack>-` (the 472 id-prefix convention, `ci-`, `rq-`, `sy-`) or whose id is `<pack>`; in `js/engine/mock.js` and `tools/validate.mjs` `verifyDraws`; AUTHORING section 5 drill bullet.

### Engine pass C fix pass (4 Nov): `docs/reviews/review-engine-pass-c.md`
474. Done (review 1, 7): playthrough `drawChecks` `poolOf` matches a drill by id prefix `<pack>-` as the engine and validator do, and counts the expected items with one `used` set across the entries (an item an earlier entry could claim is not counted again). New sample `exams/mock-sample-draw-prefix.json` (draws `drills/sample-cpp`, a C++ pack named by id prefix) fails the playthrough before this and passes after.
475. Done (review 2): `--bank` plays an item with `parts` (kind read from the first part when there is no `widget`; each later part is answered and checked after Continue; the item is right when every part is). `tools/playthrough.mjs` `partsHomeworkChecks` guards a part with no widget. `bank/sample-draw.json` gains `sd-parts` so a mock draw exercises a bank parts item. A scratch non-sample bank file holding it was played through `--bank` (7 of 7) and deleted: a sample bank file is never dealt by the deck, so no committed file can be played by `--bank`.
476. Done (review 3): the homework rule "at least one code item" and "at least one order or expression item" counts the widget kinds of an item's parts (`validate.mjs`, homework block). New sample `courses/py-found/homework-sample-parts-late.json`: its only code is in a parts item; it failed "needs at least one code item" before this.
477. Done (review 4, 6, 7): a drawn drill's item tags are its `tags` then its `pattern` (deduplicated, tags first so the family is unchanged), in `mock.js` `drillItem`, `validate.mjs` `drillTags` and the playthrough pool. `verifyDraws` errors when one exam's entries have `n` summing to more than the different items their pools hold together (the engine shares one `used` set, so a short entry cannot be filled); the engine cannot draw items that do not exist, so it keeps its console warning. AUTHORING says a drawn drill is graded by the code widget, not the drill harness (the typed-result check does not run), which is left as documented behaviour.
478. Done (review 5): in a code part sequence an earlier `cumulative: false` part starts a fresh merge, so a later cumulative part runs the tests from that part on (`player.js` `widgetOf`, `validate.mjs` `checkParts` count). AUTHORING "Code parts" says so, and that only `tests` merge (each code part carries its own `setup`, `prelude`, `postlude`, `files`, `data`). Behaviour changes only for a sequence that uses `cumulative: false` before a later cumulative part.
479. Done (inbox, systems L1 and research-int L1): `partsHomeworkChecks` finds the first item with three or more non-code parts wherever it sits: it answers the earlier items (every part of any item with parts), then the parts item, reads the draft from `ZQHomework.handles()[k]`, leaves that item's last part unanswered and checks the summary row of item k. Regression sample `homework-sample-parts-late` (parts item fourth); `homework-sample-parts` (first) still passes.
480. Done (review 8, 9, 10, 11, 12, 13, 15, 16): text and tooling. AUTHORING: seed fixes a draw only for a learner with no earlier attempt; the Sources bullet names the id prefix; the interleave row lists the op fields and the `wait` rule; the sample list is complete; the bank paragraph no longer says a bank draw is not built; part `id` is documented as accepted and unused (kept so existing files stay valid); the negative-marking effect on an item left at part 1 is stated. `validate.mjs` runs `noteSample` on drill session files (so `samples` and the loader agree) and refuses a real session that names a sample drill. KNOWN_ISSUES line on visible engine samples removed. Backlog 467 to 472 were already marked Done by the merge. The twelve-plus-nine pattern list (review 14) is kept; the main session confirms.

### Engine pass E (4 Nov): prerequisite gating
Source: `docs/briefs/prereq-gating.md` sections 1 to 7; author side `docs/AUTHORING.md` section 11; learner side `app/README.md`. Report `docs/reports/engine-pass-e.md`. No `course.json` carries `requires` yet (the mapping agent adds them), so only the implicit previous-level rule is live in content.
481. Done: data and the met rule. `ZQ.prereq` (new `app/js/prereq.js`): level `requires` (level and lesson references, any course), the implicit previous-level rule, `lessonRequires` (a per-lesson override map at the top of `course.json`), a mock's top-level `requires`. Met by a passed review (`state.reviews[...].passed`, sticky; a review file may carry `pass`, default 0.7), a passed topic exam, a passed stage exit test, a test-out, a grandfathering or derived record in `state.prereq.met`, or (no written review) every written lesson finished. State: `doc.prereq { met, testouts, opened, grandfathered }`, `ZQ.state.prereq.mark/testout/open/grandfather`, `settings.strictPrereqs` (default true). `sync()` records every level found met so nothing relocks, and grandfathers an old save once (all written lessons of a level finished). Files: `js/prereq.js`, `js/state.js`, `index.html`.
482. Done: locking. `lessonLocked`, `levelLocked`, `itemLocked` (lesson, review, homework), `courseLocked`; a finished lesson, an existing review or homework record, and a level opened early are never locked. The routes `#lesson`, `#review` and `#homework` open the locked card instead (`js/screens/lesson.js`, `review.js`).
483. Done: the locked card (`js/screens/locked.js`, `css/screens/locked.css`): Stage, Topic, Course, level or lesson groups with counts, direct first and open, indirect collapsed to one line per stage, "Start here" (earliest missing node whose own references are met), "Test out" on each missing level with a written review (or why not), the met-rule footnote.
484. Done: course map. A locked node has a lock and no "Jump ahead"; its card offers "See what is missing"; Continue goes to the first unlocked lesson, or "See what is missing" when the whole course is locked (`js/screens/course.js`, `css/screens/course.css`).
485. Done: test-out, `#testout/<course>/<n>` (`js/screens/review.js` `mountTestout`, reusing the set page). Up to 6 items from `review-<n>`, seeded by level and try count, passed at ceil(items x pass); a pass marks the level met; a miss lists the lessons to revisit (matched by skill) and waits 24 hours; no XP, no mastery points, no redo entries.
486. Done: Strict mode and the override. You, Settings, Study plan, "Strict prerequisites" (on by default). On hides "Open anyway"; off shows it, records `state.prereq.opened[level]` and You counts "opened early" (`js/screens/you.js`).
487. Done: Today, Learn and Prepare follow the lock. Today and Learn pick only unlocked lessons (`nextLesson` in `today.js`, `learn.js`, `course.js`); Today says in one line when the course it would have chosen is locked and offers "Start here". Prepare marks a blocked step with a lock and its first missing prerequisite, and a mock that names `requires` as Locked; the mock route (`js/screens/exam.js`) shows the locked card. The bank keeps its own lesson `requires`.
488. Done: validator rules for `requires`, `lessonRequires`, a mock's `requires` and a review's `pass` (unknown refs, self reference, earlier stage to later stage, cycles printed, later topic in the same stage, unwritten level or lesson, unwritten implicit previous level, duplicate reference, `requires` on a non-mock exam). Tested with scratch copies of `content/`.
489. Done: Refresh chip. A met level reference whose review has not been taken for 30 days (last review, test-out, topic or stage pass, or met record) shows "Refresh" on the dependent lesson's start screen, linking to that review (`js/engine/player.js`). It never relocks.
490. Done: playthrough. `--lesson`, `--set`, `--exam`, `--all` call `ZQ.prereq.unlock` (or `unlockRefs` for a mock's `requires`) before playing the target; `--bank` and `--drills` are not gated by levels. `--routes-only` gains `gatingChecks`: fresh profile (Stage 0 first lesson open, a Stage 3 level 2 lesson locked with the right card, "Start here" opens, Strict hides "Open anyway"), the override outside Strict, a failed test-out waiting 24 hours, a passed one unlocking, an old save grandfathered, the locked map node, Today with a Stage 3 start. Files: `tools/playthrough.mjs`.
491. Done (fix pass, review finding 1): the Refresh chip is drawn above the lesson's first screen whatever its kind (the strip is prepended to step 0 by `lessonFactory` in `js/engine/player.js`; `titleStep` no longer draws it). Routes check: a met record aged 31 days on a lesson whose first screen is not a title shows `.rf-chip` at 1280 and 390 px.
492. Done (finding 2): a level that is met is open as a place to work. `levelLocked` and `lessonLocked` return false for a met level (a lesson with its own `lessonRequires` entry keeps that list), so its lessons, review and homework open even when its own references are unmet, and the Refresh link never reaches a locked review. Routes check: after a test-out of a locked level its lessons, review and homework are open and `#review` shows no card.
493. Done (finding 4): started levels. `state.prereq.started` (`ZQ.state.prereq.start`) records every level with a finished lesson, in `sync()`; such a level's remaining lessons, review and homework stay open. It never counts as met for dependants and You does not count it. Decision: the brief's "finished work never locks" is read as covering work in progress, because a level a learner was part-way through was open to them before gating. Grandfathering (met) now needs every lesson on the map written and finished. Routes check: one finished lesson keeps the level's other lessons open, level not met.
494. Done (finding 5): `missingRefs` takes two passes, so a listed reference is direct whatever the list order (before, a direct reference reached through an earlier one landed in indirect). Routes check: both orders give the same direct set.
495. Done (finding 3): `requires` at the top of any exam file (mock, topic exam, stage test) is honoured: `js/screens/exam.js` shows the locked card for any exam id and the playthrough unlocks it before `--exam`. The validator no longer errors on a topic exam or stage test with `requires` (still checked, plus a warning that locking it removes the test-out route). No content edited: a content pass adds the lists to the mocks (AUTHORING section 11). Routes check uses a stand-in topic exam with `requires`.
496. Done (finding 6): test-out retakes. The record keeps `seen` (item ids shown on every attempt); a retake draws unseen items first, seeded by level and try, and repeats seen ones only to fill the 6. A review of 12 or more items gives a fully new second paper. AUTHORING says so. Files: `js/screens/review.js`, `js/state.js`.
497. Done (finding 7): a level with no written review is met only when every lesson on its map is written and finished (`fullyFinished` in `js/prereq.js`); a half-written level no longer satisfies its dependants.
498. Done (notes 9a, 10, 11, 12, 13): the validator errors when a level's `requires` names its own lesson; the locked card says "not yet written" for a level with nothing written and hides Test out; Today's "Start level n" reads "See what is missing for level n" when that level's next lesson is locked; the routes gating check compares the card with a closure computed in Node; DECISIONS lists the differences from the brief. Skipped: notes 8, 9b (documented in AUTHORING), 14, 15, 16 (reasons in `docs/reviews/review-engine-pass-e.md`, Fix pass).
499. Done (playthrough fix): the `--routes-only` samples check matches a sample's name only as a whole entry (a line of the page text or a leaf element equal to the name), not as a substring, so a real drill named "Longest run with equal zeros and ones" no longer trips on the sample "Longest run". A genuine leak still fails. File: `tools/playthrough.mjs`.
500. Done (drill failure 4 Nov): the drill page's Python runner (`PyRunner` in `js/screens/drill.js`) ignored the worker's `pkgs` messages, so downloading and unpacking pandas counted against the 5 s run limit; on a slow or loaded machine the model solution of `rq-clean-frame-py` and `rq-group-slopes-py` timed out at the top level ('Python was restarted', every test skipped, shown as 0 of N), while the starter still 'failed'. The runner now pauses the limit during package loading (its own 120 s) and re-arms the 5 s limit when loading ends, as `js/engine/widgets/code.js` has done since item 161. No content changed.

### Engine pass 3.2 (4 Nov): expression grader, `docs/reports/engine-pass-3.2.md`
Source: `docs/reviews/review-briefs-3.2.md` "[Must] engine requirements". Both inbox bullets removed.

501. Done (P32-expr-exp): `prep()` in `js/engine/grade.js` rewrites `\exp`, `\operatorname{exp}` and `\mathrm{exp}` with a bracketed argument (`(..)`, `\left(..\right)`, `{..}`) or one token into `\left(\exponentialE^{(arg)}\right)`, so every comparison (`exprEqual`, `exprEqualUpToConstant`, `exprShape`, the `form` check, exam items) reads `\exp(x)` as `e^{x}` in both directions. The validator warns when an authored `answer` or `accept` contains `\exp`.
502. Done (P32-expr-callhead): `prep()` inserts `\cdot` between a lone Latin or Greek letter (optional subscript or superscript) and an immediately following `(` or `\left(`, so `r(1-x)` is a product, unless the letter is in the new optional `functions: ["f"]` of the `expression` widget (the validator checks its shape). Every comparison and the `form` check also run inside `ce.pushScope()` and `popScope()` (`scoped`, new `ZQ.grade.withParsed`), so a symbol the engine declares while parsing (a function after `f(x)`) is a plain symbol again on the next screen.
503. Done (P32-expr-int): optional `integers: ["k"]` on the `expression` widget (and so exam and bank items). `scalarEqual` and the up-to-constant check in `js/engine/grade.js` sample each listed symbol at six distinct seeded whole numbers from 1 to 9 (own generator per symbol, so draws for other symbols and expressions without `integers` are unchanged); other symbols keep 0.3 to 3, and the usual relative tolerance 1e-9 absorbs the rounding in `\cos(k\pi)`. Validator: error on a malformed `integers`; warning when an `answer` or `accept` has `(-1)^k` or `(-1)^{k..}` and the symbol is not listed.

Status block (engine pass 3.2):
- 501 (P32-expr-exp): done.
- 502 (P32-expr-callhead): done.
- 503 (P32-expr-int): done.

### Engine pass viewports (4 Nov): `docs/reports/engine-viewports.md`
Source: user request to test the real devices (iPhone 17 Pro Max 440 x 956; iPad Pro 13-inch 1032 x 1376 and 1376 x 1032).

504. Done (VP-phone): `--mobile` in `app/tools/playthrough.mjs` runs at 440 x 956 instead of 390 x 844 in every place it is used (shots, drills, gating, Prepare for, routes); screenshot suffix `-440`; messages name the width used.
505. Done (VP-narrow): `--narrow` keeps the old 390 x 844 pass (suffix `-390`) and implies the extra pass on its own.
506. Done (VP-tablet): `--tablet` adds 1032 x 1376 and 1376 x 1032 passes with the same wider-than-window checks (suffixes `-1032`, `-1376`); every pass sets width and height through one `setVp` helper, so the old fixed 844 height is gone.

Status block (engine pass viewports):
- 504 (VP-phone): done.
- 505 (VP-narrow): done.
- 506 (VP-tablet): done.

### Engine pass devices CSS (4 Nov): `docs/reports/engine-layout-devices.md`
Source: user request after the viewport pass (iPhone 17 Pro Max 440 x 956; iPad Pro 13-inch 1032 x 1376 and 1376 x 1032); faults found by items 504 to 506.

507. Done (wider column): `--col` (`css/tokens.css`) is 780px from 768px up (540px below). The lesson, set, review, homework, exam and warm-up columns and every canvas (`.cv { max-width: var(--col) }`) follow it. Prose (`.t-prose`) and Markdown tables inside the column stop at 70ch; canvases, tables, widgets and code use the full width. The lesson verdict chip no longer sits in the left gutter at 1200px and up (the gutter is 250px); it stays above the buttons at every width from 768px. The homework model answer no longer breaks out of the column by 110px. Onboarding and the drill brief keep 540px.
508. Done (code editor): the editor already scrolled sideways inside its own box, but nothing said so, so long lines looked clipped. `code.js` and `cpp-grade.js` set `has-more` on `.wd-ed` while text runs past the right edge (also on resize); `css/widgets.css` draws a 28px fade there. On a phone the lesson, homework and exam scroll areas end 56px lower and use `scroll-padding-bottom: 88px`, so the last editor line and the run output scroll clear of the Check bar.
509. Done (exam result at 440): not a truncation. The result reveals in stages on timers (count-up 900 ms, tiles to 2.1 s) and the playthrough shot waited only for CSS animations, so a shot taken during the reveal showed the score and stamp alone (the 1280 shot read 21 of 30 mid count). `shot()` in `tools/playthrough.mjs` now also waits for `.exm-res.final` (at most 4 s).
510. Done (side tab): the screens navigator (`.proto`, `js/core.js protoNav`) sat at `top: 50%` on the left edge. It now anchors to the bottom-left corner (16px above the bottom edge, safe area respected); on a phone it is a 14 x 32px tab 4px above the bottom, clear of the lesson hint button.
511. Done (set Check button): in a set page (review, practice, redo; `.lsn-set-foot`) the button group is left-aligned with the item's content from 768px up instead of centred.

Status block (engine pass devices CSS):
- 507 (wider column): done.
- 508 (code editor, room under the Check bar): done.
- 509 (exam result at 440): done (timing in the playthrough, not a layout fault).
- 510 (side tab): done.
- 511 (set Check button): done.

### Engine pass devices 2 (4 Nov): `docs/reports/engine-layout-devices.md`
Source: faults left by the devices CSS pass.

512. Done (drill passes): `--drill <id> --tablet` (and any run with two or more viewport passes) threw `ZQDrill is not defined` from the second pass. Not an app fault and not a resize: the first pass solved the drill, the record persists, and a solved C++ drill reopens on Continue (`submit()` leaves the page when the code equals the verified code). The second pass set the same model solution, so its Submit navigated to the drill list and the test hook went with the page. `drillOne` in `tools/playthrough.mjs` now deletes the drill's record and per-drill state before opening it, so each pass starts unsolved.
513. Done (tall plane): `css/screens/lesson.css` caps a `plane` canvas at `max(300px, 46vh)` in landscape from 768px up when the author set no `canvas.maxHeight`; the picture scales down, centred, so the question stays in view.

Status block (engine pass devices 2):
- 512 (drill passes): done.
- 513 (tall plane): done.

## Engine pass 3.2 (expression grader, D)

Source: `docs/reviews/review-pdes.md`, worst finding (`pdes/l2-heat-equation` screen 5).

514. Done (P32-expr-D): `prep()` in `js/engine/grade.js` rewrites every capital `D` and `N` outside a command name and outside `\mathrm{..}` style groups to `\mathrm{D}` or `\mathrm{N}`, whatever follows (before it only a lone one, standing alone or before `(`, was rewritten). `4Dt`, `tD` and `\sqrt{2Dt}` are now products. A screen lists `"D"` or `"N"` in `functions` to keep the operator reading before a letter. Documented in `docs/AUTHORING.md` section 3. Report: `docs/reports/engine-pass-3.2.md`.

Status block (engine pass 3.2, D):
- 514 (P32-expr-D): done.

## Validator pass (per cent keys)

Source: `docs/reviews/pct-keys-scan.txt` (37 numeric widgets with `unit: "%"` stored the per cent, not the fraction).

515. Done (per cent keys): `tools/validate.mjs` (numeric case) errors when `unit: "%"` has a key or `wrong` value above 1 in absolute value and `accept` shows that number followed by `%`, and warns for any other such key unless the widget has `"over100": true`. `tools/playthrough.mjs` (`pctWidgets`) also types, for each such widget in a lesson, answer x 100 with and without `%` plus the single per cent figure in `accept`, and fails the lesson if any is not graded right. Documented in `docs/AUTHORING.md` section 3 (numeric).

516. Done (per cent leading figure): `tools/playthrough.mjs` (`pctWidgets`) and `tools/validate.mjs` (numeric case) read only the leading figure of `accept` (the first number, before any colon, followed by `%`); the extra typed form is skipped otherwise (fixes a false alarm on measure-prob l11 screens[8], "250: 1% a day for 250 days"). The validator error now also covers keys at or below 1: leading accept figure followed by `%` equal to a non-zero key (key 0.63, accept "0.630%: ...", should be 0.0063). Documented in `docs/AUTHORING.md` section 3 (numeric).

517. Done (per cent representative figure): item 516 typed the leading accept figure, which fails correct keys whose accept shows working first (limits-thm l9 screens[8]: "$2\\% / \\sqrt{2000} \\approx 0.0447\\%$", key 0.000447). `tools/playthrough.mjs` (`pctWidgets`) now types the figure after the last `=` or `\\approx` if its hundredth is within tolerance of the key, else any figure whose hundredth is, else the leading figure (which then fails, as before). `tools/validate.mjs` (numeric case) takes the figure after the last `=` or `\\approx` when followed by `%`, else the leading figure, as the figure compared with the key. Still skipped unless the leading figure is followed by `%`. Documented in `docs/AUTHORING.md` section 3 (numeric).

Status block (validator pass, per cent keys):
- 515 (per cent keys): done.
- 516 (per cent leading figure): done.
- 517 (per cent representative figure): done.

## Engine pass (C++ freed-memory harness)

Source: `docs/BACKLOG-INBOX.md`, "Raised later (cpp L5 brief, 5 Nov)".

518. Done (C-poison-quarantine, Must): in `js/engine/widgets/cpp-grade.js`, every `allocCheck` and `leakCheck` unit now uses one operator set (`allocCheck` alone no longer has its own bare-`malloc` operators). A block has a 16-byte header with magic, kind and size; `delete` fills the block with 0xDD, marks the header freed and never releases it (quarantine, capped at 64 MB, then plain `free`). A second `delete` of a quarantined block prints "Memory error: a block was deleted twice." and exits 1, in `allocCheck` alone too; `leakCheck`'s `put` no longer reads a freed header. Leak reporting stays off for `allocCheck` alone. Documented in `docs/AUTHORING.md` section 3.

519. Done (C-free-count, Should): `allocCheck` adds `free_count()` (non-null deletes since `reset_alloc_count()`, which resets it) and `live_blocks()` (never reset). `tools/validate.mjs` forbids defining them in hidden sources and counts a read of any of the three as using `allocCheck`.

520. Done (array ranges doc, Should): `highlight.ranges` for the `array` canvas documented in `app/js/engine/canvas/README-B.md` (shape from `array.js`: `{ range, label, colour, id }` or a bare pair).

Status block (engine pass, C++ freed-memory harness):
- 518 (C-poison-quarantine): done.
- 519 (C-free-count): done.
- 520 (array ranges doc): done.

521. Done (PLAN 2c item 3, N01): result provenance. Rows carry `how` (`auto`, `self`, `external`); `rate()` keeps self rows out of `skills[s]` (they go to `state.selfMarked`), no MP or item XP from them; You shows a "Self-marked" block; prerequisite met reads `passedAuto` (exam attempts and reviews) and ignores self rows and checks; old saves migrate (see AUTHORING.md section 13). Playthrough `--routes-only` has a provenance check. Report: `docs/reports/engine-pass-provenance.md`.

Status block (engine pass, provenance):
- 521 (result provenance, N01): done.

522. Done (PLAN 2c item O1): `app/tools/merge-wave.sh <branch>...` merges worktree branches by the DECISIONS "Parallel worktree merges" rules (union of `drills/index.json` by id, both sides of `BACKLOG-INBOX.md`, `PROGRESS.md` and report or review markdown, newer side of a review file, anything else aborts that branch as UNRESOLVED), scans the merge for conflict markers, runs the validator, stages `manifest.json` and commits. The last lines are one status per branch, `validator: N errors` and OK or FAIL. `app/tools/test-merge-wave.sh` is the acceptance test (two branches, conflicts in all three named files): PASS.

Status block (engine pass O1):
- 522 (merge-wave.sh, O1): done.

## Engine pass O2 (recurring finding classes as validator warnings)

Source: PLAN 2c item O2; `docs/reviews/session-operating-model.md` 2.2.

523. Done (O2-long-sentence, O2-long-explain): `tools/o2-rules.mjs`, run by `tools/validate.mjs`, warns on sentences of 20 words or more in learner-facing strings and on explanations of more than three sentences.

524. Done (O2-unshuffled-numeric): warns on interval or ordered-numeric `choice` and `multi` options without `shuffle: true`.

525. Done (O2-no-slip): warns on numeric distractors (choice options, `numeric` `wrong` entries) that match no common slip, no given number and carry no slip note.

526. Done (O2-prose-prompt): warns when `prose` and a `prompt` are both present, or the `question` repeats the prose word for word.

527. Done (O2-explain-answer): warns when `explain.text` never states a numeric key (tolerance and common formats allowed). `tools/test-validate-o2.mjs` runs a bad and an ok fixture per code; counts are in `docs/reports/engine-pass-o2.md`.

Status block (engine pass O2):
- 523 (long sentences, long explanations): done.
- 524 (unshuffled numeric choices): done.
- 525 (distractors with no slip): done.
- 526 (prose and prompt): done.
- 527 (explain against answer): done.

## Engine pass, item 4 (met rule rewrite)

528. Done (PLAN 2c item 4, N02, N03, F05.1 to .4): met rule rewrite. (1) Review pass fallback 0.8 (`prereq.js` `PASS`, `state.js` `REVIEW_PASS`, matching MASTERY); the review files' own `pass` is written by the main session. (2) `SKILL_FLOOR = 0.7`: a review pass meets its level only when every skill tagged on its items is at the floor over the attempt's auto rows and `skills[s].seen > 0`; the review record keeps `essential`, `bySkill`, `passBySkill`; test-out applies the floor to the skills it drew. (3) `REVEAL_CAP = 0.25`: `state.lessonCounts` (lesson records now keep `revealed` screens and `gradable`) gates `lessonDone`, `lessonMet`, `fullyFinished` and the progress figures; finished lessons stay unlocked and a replay clears the count. (4) Topic and stage exam passes meet a level only when one passing attempt's `bySkillAuto` (new on exam attempts) covers every essential skill at the floor (`content.essentialSkills`, `loadEssentials`). (5) `quizFinished` always queues misses. Tests: `app/tools/test-met-rule.mjs` (10 of 10). Report: `docs/reports/engine-pass-item4.md`.

Status block (engine pass, item 4):
- 528 (met rule rewrite, N02, N03): done.

## Engine pass, item 5 (performance tasks)

529. Done (PLAN 2c item 5, N07): the performance-task kind. (1) An item in a level's homework (or review) carries `"performance": "code" | "derivation" | "aloud" | "data"`, built on `code`, an empty-box `longform`, a timed `longform` with follow-ups, and a `numeric` or `longform` that reads a data file; `app/tools/perf-rules.mjs` holds the shapes and the verb rule, and `validate.mjs` applies them (`perfItem` per item, `perfLevel` per level). (2) The verb rule reads the lesson files' `objectives`: 111 written levels match (Stage 0: 4, Stage 1: 63, Stage 2: 22, Stage 3: 22). (3) `app/tools/perf-pending.json` grandfathers those 111 (`node tools/perf-pending.mjs --write | --prune`); a matched level without a task and not on the list is an error, a listed level with a task warns "remove from perf-pending". (4) Met hook: `state.perf["course/L<n>"] = { item, kind, how, at }` written by `ZQ.state.perf.pass` (called from `homeworkSubmitted` and `reviewFinished` for rows carrying `perf`); `manifest.perf` tells `ZQ.content.perfOf` which levels need one; `ZQ.prereq.derivedMet` and a `testout` met record need `perfPassed` as an extra AND; the locked card and the test-out note say so. (5) Engine support: longform `seconds` (aloud clock) and `followUps`, a data panel (`ZQ.widgets.dataPanel`) on `numeric` and `longform`. (6) Tests: `tools/test-validate-perf.mjs` (33 cases under `tools/fixtures/perf/`), 6 new cases in `tools/test-met-rule.mjs`. Documented in AUTHORING sections 5, 7 and 11; report `docs/reports/engine-pass-item5.md`.

Status block (engine pass, item 5):
- 529 (performance tasks, N07): done. Pilots (one level each in coding-int, ito, proof, research-int) remain for a content agent; the main session prunes perf-pending as tasks land.

## Engine pass, performance pilots (`docs/reports/engine-pass-pilots.md`)

Numbered from the 16 inbox bullets under "Raised later (... perf pilot)". 530 to 533 coding-int, 534 to 537 research-int, 538 to 541 proof, 542 to 545 ito.

530. Done: `playthrough.mjs --set` plays the starter of every `performance: "code"` homework item and fails if it passes (Python and C++ comment suffix).
531. Done: after a homework holding a performance item, the set playthrough asserts `state.perf["<course>/L<n>"]` exists with how auto or self.
532. Done: "Performance task, needed for the level" tag in the item header, "Performance task" in the overview list, a start-card line, and "Performance task passed / not passed" on the result row and verdict (also covers 539 and 543).
533. Deferred: per-case run time in the code widget and playthrough. Needs the worker to report per-case seconds; not cheap, no author blocked (CPython and Pyodide timings are the workaround).
534. Done (Must): Mark my answer skips the text check when the widget's `ready()` is true (an aloud item); ordinary longform keeps the guard. The set playthrough now clicks the real button, checks an empty box is refused on written items and accepted on aloud, and fails on the old bug (verified by reverting the fix).
535. Done: an aloud longform labels its box "Your notes (optional)" with a notes placeholder.
536. Deferred: a follow-ups step after the answer with the clock restarted, before the model opens. A new phase in the widget and its restore path; the content workaround (follow-up answers last, under a heading) holds.
537. Deferred: storing the aloud clock reading on the result row. Needs a widget-to-result field through `grade().detail` and the state schema; the rubric time line is 1 of 10 points.
538. Done (warning only): the validator warns on `$` in a homework, review or exam item `title`. Typesetting titles deferred (the header is uppercased text; 8 files still carry `$`, for content to reword).
539. Done: see 532.
540. Done: start card reads "Items 9 and 10 are written. You mark them yourself" for more than one longform item (also covers 542).
541. Done: `--shots` takes a `-marked` shot of each longform item after the real Mark my answer click (also covers 545).
542. Done: see 540.
543. Done: see 532.
544. Done: longform rubric rows take `"required": true`; the self-mark fails without it; validator checks the type and warns if every row is required. Scratch cases (a string `required`, all rows required, `$` in a title) run on a scratch copy of the content: error, warning, warning as expected.
545. Done: see 541.

Status block (engine pass, performance pilots):
- 530, 531, 532, 534, 535, 538 (warning), 540, 541, 544: done. 533, 536, 537: deferred with reason above. 539, 542, 543, 545: done as duplicates of 532, 540, 541.

## Engine pass, item 6 (holdout and resit integrity; `docs/reports/engine-pass-item6.md`)

546. Done (PLAN 2c item 6, F05.6): the draw is unseen-first across the whole pool, not within a family only. Seen is a drill verified in the library or an item drawn in an earlier attempt (`ZQ.mock.seenInfo`, `seenLabel`); never-seen items come first, then the least recently seen (a library solve is older than any sitting), families balanced inside each tier. A seen drawn problem shows "Previously seen: solved in the drill library" or "sat on <date>" on the paper, the start card and the results, and the attempt stores `seen`. The library stays open. Evidence: `playthrough.mjs --exam mock-oa-code` (holdout check: all 8 drills verified gives the label on both problems; five fresh sittings draw 8 distinct problems, then the label says "sat on"). Content: `tools/apply-item6-content.mjs` sets mock-oa-code `pass` to 1 and rewrites its description (mark illustrative, new behaviour).
547. Done (F05.7): `versionOf` on fixed mock versions. The Prepare page groups `<base>-<n>` under the base mock ("Version 1, 2, 3", next unsat first); prep.json keeps naming the base only (readiness-sums needs that). Validator errors: bad or missing `versionOf`, version number below 2, base named by no prep path. Evidence: `tools/test-validate-versions.mjs` (5 of 5), a Prepare check in `playthrough.mjs --routes-only`. The same script adds the field to the four `-2` and `-3` files.
548. Done: `ZQ.prereq.examLocked` ignored advisory references (role-optional courses), so mock-oa-code showed a locked card with "0 things to finish" to a non-developer profile; it now uses `blocking()` as levels do.
549. Done (decision on review-perf-pilots Q1): a performance task gates met only when its level is rule-matched. The validator writes `"gates": true` on the manifest `perf` row of a matched level; `ZQ.prereq.perfNeeded` returns null without it; the homework page says "practice only" for such a task. proof/L3 `h-prove-cube-minus-n` no longer gates. Evidence: `test-met-rule.mjs` 17 of 17 (one new case), `test-validate-perf.mjs` 33 of 33. Needs `node app/tools/validate.mjs` once to regenerate `content/manifest.json`.
550. Done (inbox, main session P, 5 Nov; number taken by the shard pass while another agent numbers in parallel): `playthrough.mjs` for long runs. `--shard i/n` (1-based, validated; a malformed value is a usage error) keeps the items of the full ordered list (lessons, then sets, then exams) whose zero-based index % n === i-1, prints `shard i/n: K of N items`, and the routes and their checks run in shard 1 only (so `--routes-only --shard 2/4` has nothing to run and passes; it does not shard the route checks). `--list` prints the item ids of the run (lesson/, set/, exam/) without a browser. Each lesson, set and exam runs under a guard: when it throws "Target page, context or browser has been closed" (or the browser `disconnected` event fired) Chromium is relaunched with the same options and routing, setup is redone on the fresh profile, and the item is retried once; an ordinary failure is never retried. The summary prints `browser relaunches: R`. Test hook: `ZQ_TEST_CLOSE_AFTER=k` closes the context after the k-th item. Evidence: 1/n..n/n partition the 1584 items with no overlap for n of 1, 2, 3, 4, 7 and 400; `--all --shard 37/400` green; with the hook the next item failed, relaunched once and passed.

Status block (engine pass, item 6):
- 546, 547, 548, 549: done. Content scripts and manifest regeneration are for the main session (commands in the report).

Status block (engine pass, playthrough shard):
- 550: done. `--shard i/n`, `--list`, browser relaunch with one retry and `browser relaunches: R` in `app/tools/playthrough.mjs` (usage text updated). Report `docs/reports/engine-pass-shard.md`.

## Engine pass, item 7 (dependency rationale; `docs/reports/engine-pass-item7.md`)

551. Done (PLAN 2c item 7, F02): `requires` entries may be `{ ref, why, gate }` as well as strings, in level `requires` and `lessonRequires` (exam files stay strings). One normaliser in `js/prereq.js` (`entryOf`, `entriesOf`, `refsOf`, `whyOf`; also loadable from node); `levelRefs`, `lessonRefs` and `examRefs` return gating strings, so `engine/select.js` and `engine/mock.js` (which read item `requires`, always strings) are unaffected; `screens/exam.js`, `screens/prepare.js`, `tools/readiness-sums.mjs`, `tools/census.mjs`, `tools/validate.mjs`, `tools/closure.mjs` and the playthrough 7d block use it.
552. Done: `why` shows as one line under each missing prerequisite on the lock card, on the Learn node card and on the Prepare step. `gate: false` is a diagnostic: never locks, shown as "Check first: <name>" with the reason and a link to sit that level's review (lock card, lesson start, Learn node card). `ZQ.prereq.diagnosticsFor`, `diagnosticsForLevel`.
553. Done: validator rules for entries (unknown keys, `why` one line, under 20 words, no em-dash, `gate: false` needs `why`, boolean `gate`) and a warning per cross-course entry without `why` (error with `--strict-why`); prints `Requires: N cross-course edges, M without why` (248 of 248 at HEAD). Scratch cases: `tools/test-validate-why.mjs`.
554. Done: route limitation. `ZQ.prereq.routeLimits*` walks the gating closure; Learn course card, Learn node card, lock card, lesson start and Prepare (step and path header) show "Route limited: <course> unwritten" per course. The `--routes-only` gating block (7d2) checks the engine list against one computed from `course.json` and the lesson files for every course, and the Learn card for pdes.
555. Done: `tools/closure.mjs` (`--role`, `--target`, `--json`, `--edges`, `--proposal-template`); reproduces trader superday 107 levels, 35 courses, 470 lessons (`--target mock-superday-trader`). `census.mjs` summary line gains the cross-course edge and no-why counts.

Status block (engine pass, item 7):
- 551, 552, 553, 554, 555: done. Content applies the `why` entries (proposal template) and may then switch the validator to `--strict-why`; the static `limited.pdes` entry (generated by readiness-sums from docs/readiness.md) can go once nothing reads it.

## Engine pass, items 10 and 11 (duration honesty, workload single source; `docs/reports/engine-pass-items10-11.md`)

556. Done (PLAN 2c item 10, F07): lesson `session` (`short` default, `workshop`, `project`); validator checks the enum and that `minutes` fits (short 5 to 20, workshop 20 to 90, project 60 to 240, the brief's ranges: the data has workshops of 25 to 60 minutes and no project). The old 10 to 15 rule is gone. `manifest.json` gains `sessions` (workshop and project lessons with minutes).
557. Done: one duration matcher, `tools/duration-prose.mjs` (five variants, rates and offsets ignored, under 20 minutes ignored, first two screens), used by the validator as warning `duration-prose` when the stated time differs from `minutes` by more than 5; `tools/duration-prose-ignore.json` names the ten false positives; `node tools/duration-prose.mjs --all` reports counts by variant; pattern and false positives in AUTHORING section 1; `tools/test-validate-session.mjs`.
558. Done: `tools/apply-item10-content.mjs` (idempotent, text edits only, explicit list of nine true hits, refuses an undecided hit, regenerates `readiness.json` and its md blocks). For the main session to run.
559. Done: cards show workshop length: the lesson start screen (title screen and the course page's lesson sheet), the course page lesson row, and the Learn course card ("Workshop, 60 min", "6 workshops, 25 to 50 min"; also in the card's accessible name). `ZQ.content.sessionOf`, `courseSessionLabel`.
560. Done (PLAN 2c item 11, F09): `app/js/hours.js` (`ZQ.hours`, loadable from node): hours per lesson, level, course, topic, stage and role sums, one weight rule (short 1, workshop or project `minutes / 14`); `readiness-sums.mjs` generates `readiness.json` through it with no figure moved on today's content.
561. Done: a stage's hours are derived (sum of topic hours) at load in `js/content.js`; the stored field is ignored (validator warns, no longer requires it). Learn stage cards, header and "about N months" (now `ZQ.hours.months`; the hard-coded 8, 21, 12, 6 are gone) read it; Prepare paths show no hours.
562. Done: `tools/apply-item11-content.mjs` removes the stage `hours` lines from `curriculum.json` (idempotent text edit).
563. Done: `tools/curriculum-hours.mjs` (`--write`, `--check`) generates the hours block in `docs/curriculum.md` and checks its prose figures; `census.mjs` reads the derived stage hours (last line `Hours: stored stage total 3695, summed topic total 3695, gap 0`) and adds a legacy-field line.

Status block (engine pass, items 10 and 11):
- 556, 557, 559: done. 558 and 562: scripts written, not run on `app/content/` (commands in the report).
- 560, 561, 563: done. Topics 3.2 and 3.4 still store 0 hours; the derived figure from lesson minutes is reported, not stored.


## Engine pass, item 8 (independent capstone; `docs/reports/engine-pass-item8.md`)

564. Done (PLAN 2c item 8, F06, N08): `content/capstones.json` (optional; absent means no records) loaded by `js/content.js`; `ZQ.content.readiness.roleState(role)` returns required levels met (every level of the role's required courses, by `ZQ.prereq.levelMet`), the record and `ready`; `readiness.verdict(role)` is the only source of the word "ready" for a role, "Ready" only with all levels met and a complete record (`external: true`, repo, reviewer, date non-empty, `rerun: pass`), else "Not ready: capstone not recorded" or similar. `readiness.capstone`, `capstones`, `capstoneComplete`.
565. Done: validator rule via `tools/capstone-rules.mjs`: unknown role, unknown field, wrong type, duplicate role, `external: true` with a blank repo, reviewer, date or rerun, malformed repo URL or date, researcher `project` other than `momentum-rep` without `equivalentOf: "momentum-rep"`. A missing file is not an error. `tools/test-validate-capstone.mjs` (17 cases).
566. Done: You card "Capstone" (`data-card="capstone"`), one read-only block per role, the learner's role first, says the reviewer fills `content/capstones.json`; stacks at 390 px.
567. Done: per-exam "% ready, from your mastery map" (Today exam card, Review card and ring label) relabelled "Mastery map estimate: N%." because it is an estimate for one exam, not a role verdict. Today shows no role verdict.
568. Done: a verified `oa` drill (`state.drills` record `verified`) counts toward the code performance task of the coding-int level it maps to, in one place (`perfPassed` in `js/prereq.js`, via `content.perfDrillsFor`). Mapping: a drill with pack `oa` (or id `oa-...`) and `course`, to its `level` field if present (drill file or index row; the validator checks it and copies `pack` and `level` into `manifest.drills`), else the lowest level of its course with a gating code task (coding-int L1 today). Content needs no field today; add `level` to an oa drill only to map it elsewhere.
569. Done: `tools/test-capstone.mjs` (9 tests: not ready without record, ready with one, incomplete record, verified and unverified oa drill, other drill or task kind, explicit level); playthrough `--routes-only` capstone check (fresh profile has no ready role, Today clear, You card renders, no sideways scroll). `docs/AUTHORING.md` section 15.

Status block (engine pass, item 8):
- 564 to 569: done. Main session: write the five empty records in `content/capstones.json`, regenerate `manifest.json` (adds `pack` to drill rows).


## Engine pass, tooling (`docs/reports/engine-pass-tooling.md`)

570. Done: `mock-sample-draw` timed check flake. Cause was in the check, not the engine: a mock that draws its items can open on an item with parts, and the check expected a whole-item score of at least 1 because it only read the file's own items (a drawn paper has none) for "parts first". With that item the sitting scores 0 whole items, with partial credit. `tools/playthrough.mjs` now records a drawn first item with `parts` (`drawnParts`) and allows 0; it also waits for `ZQ.test.current().state === 'engaged'` (the answer registered in exam state) before `setRemaining(0)`. Evidence: 12 of 12 desktop runs and 3 of 3 `--mobile` runs green (before: 2 failures in 10).
571. Done: `tools/lint-dup-keys.mjs` (no dependencies; tokenizer with strings, comments, templates with `${}`, regex; brace stack) reports an object literal with a repeated key, and a later `X.y = <function>` that replaces a function defined in X's own literal in the same file. Plain data fields reassigned later are normal state updates and are not reported. `tools/test-lint-dup-keys.mjs` with fixtures in `tools/fixtures/lint-dup-keys/` (bad: 3 findings, good: 0; it also flags the pre-9c70a04 `content.js` shadowed `status`). Run on `app/js/` (72 files): 0 findings, no engine file changed.
572. Done: `tools/test-check-first.mjs`, a Playwright DOM test of the "Check first" card (ENGINE-BACKLOG 552). It reads a real `gate: false` edge from the course files (today `proof` level 2 lesson `l6-sets`, diagnostic `counting/L1`), then on a profile with the gating prerequisites met asserts: the diagnostic is unmet and does not lock the level or lesson; the lesson start shows `.lk-check` "Check first: ..." with the why line and the link `#review/counting/review-1`; the Learn node card shows the same and the node is not `s-locked`; no sideways scroll. On a fresh profile the lesson is locked by the gating edge only and the lock card does not list the diagnostic as a prerequisite to finish. Desktop and `--mobile` pass.

Status block (engine pass, tooling):
- 570: done (12/12 desktop, 3/3 mobile). 571: done (0 findings in `app/js`). 572: done (desktop and mobile).

## Engine pass, session T step 0 (`docs/reports/engine-pass-T0.md`)

573. Done [Must]: `tools/numbers_lib.py` (standard library only). `Level(course, n)` loads a level's lessons, review and homework; `expect(file, path, value, fmt=None)` checks a number or string against a JSON path (`screens[3].prose`, `items[1].widget.wrong[0].value`, a path ending on an object searches below it, `[*]` joins); `text(file, path)` and `report()` (exit 1 on a failure). It copes with thousands commas, £, U+2212, LaTeX spacing and braces and trailing zeros. `tools/test-numbers-lib.py` ports checks from odes level 3 and proves wrong values fail. The validator warns when a written level's `docs/reports/<course>-L<n>-numbers.py` never uses `Level(` and `expect(`; LEVEL-BRIEF requires the helper.
574. Done [Should]: `validate.mjs` errors on a mapped level review with no `pass` (`tools/test-validate-review-pass.mjs` proves it); named in LEVEL-BRIEF.
575. Done [Should]: `startServer` in `tools/playthrough.mjs` retries on a new port (up to 6 attempts, short random pause) when the python server dies, and only trusts a ready answer while its own process is alive. Four simultaneous `--lesson proof/l1-true-or-false` runs all exit 0.

Status block (engine pass, session T step 0):
- 573: done (8 warnings from older scripts). 574: done (errors 0). 575: done (4 of 4 parallel runs exit 0).


## Engine pass, session T (protocol 6)

576. Done [Must]: `validate.mjs` adds each editable table cell's `wrong[].id` to the table widget's key set, so it is a valid `feedback.byKey` key. Confirmed first: `table.js` returns the matching `wrong` id as the key, and AUTHORING section 3 already says so (no doc change). `tools/test-validate-table-wrong.mjs` proves a cell wrong id is accepted and an unknown key is still refused.
577. Done [Should]: `plane` log axes (`plane.js`): `fmtLogTick` prints plain digits from 0.001 to 99 999 and powers of ten outside it (10⁻⁶, 2×10⁻⁶), so no tick prints as 0 or in every digit; `logTicks` keeps every nth power of ten when a range is too wide for one per decade. README-B updated.

Status block (engine pass, session T):
- 576: done (new test 3 of 3, `test-validate-why` 12 passed, validator 0 errors). 577: done (odes/l16-euler-method playthrough green desktop and mobile).

578. Done [Should]: `numbers_lib.expect` with a number also matches a LaTeX fraction of equal value (`\tfrac{3}{4}`, `\frac{1}{2}`, `\dfrac{a}{b}` skipped when not numeric, `\frac12`); the numerator and denominator still match as integer tokens. `tools/test-numbers-lib.py` adds checks on convex l4 (`\tfrac12`) and unit checks of the parser.
579. Done [Should]: the "number script never uses numbers_lib" warning now needs an import of numbers_lib plus `Level(`; calls through an alias (`E = lv.expect`) pass. Warnings 10 to 8 (odes L1-L3, complex L1-L2, numerics L1-L3).
580. Done [Should]: `docs/reviews/voice-scan.py` skips canvas `derive` rules (targets and `let`), and `expr`, `formula`, `polar`, `inner` strings under a canvas; a `derive.caption` is still scanned. Numerics and stat-models stay 0 and 0 (fewer sentences scanned); a long prose sentence in a temp copy is still caught.

Status block (engine pass, session T, items 578 to 580):
- 578: done (test-numbers-lib passes, 10 real, 4 wrong). 579: done (8 warnings left, validator 0 errors, test-validate-why 12 passed). 580: done (numerics 0 and 0, stat-models 0 and 0, spot check caught).

581. Done [Must, as a warning]: `validate.mjs` `wrongCannotFire` (numeric widgets and editable table cells, `grade.js` `within()` abs and rel). Flags a `wrong[]` value inside the answer tolerance, a wrong tolerance reaching it, and (as a warning) two overlapping wrong entries. Severity is `WRONG_FIRE_LEVEL = 'warning'` because 14 existing items are true hits; flip it to `'error'` after they are fixed. List in `docs/reports/engine-pass-T.md`. Test: `tools/test-validate-wrong-fire.mjs` (5 of 5).
582. Done [Should]: `numbers_lib` `lv.check_wrongs(file=None)` asserts each numeric wrong value is outside its answer tolerance and prints "check by hand" for a `byKey` text stating a different number. Test added to `tools/test-numbers-lib.py`. LEVEL-BRIEF names it in the number-recompute step and adds the general-claim hypotheses rule to the quality bar.

Status block (engine pass, session T, items 581 and 582):
- 581: done as a warning (14 error-class hits in existing content, 19 wrong-wrong overlap warnings; validator 0 errors). 582: done (test-numbers-lib passes).

583. Done [Must]: `tools/playthrough.mjs` route check `gating` no longer takes the first written level 2 lesson of Stage 3 as its locked fixture. It lists the level 2 candidates (Stage 3, then Stage 2) and, on the fresh imported profile, takes the first for which `ZQ.prereq.lessonLocked` is true. Cause: `prereq.js` `advisory()` makes references into a course optional for the profile's role non-blocking under Strict, so `momentum-rep/l6-data-you-can-get` was not locked. Test change only; `prereq.js` untouched; downstream assertions unchanged.

Design note (not a change, for the user to decide): under Strict, an in-course chain inside a course optional for the role is advisory (momentum-rep L2 opens before L1 is met for a trader). Decide whether in-course references should stay blocking.

Status block (engine pass, session T, item 583):
- 583: done (see report line in handback; routes-only gating passes).

584. Done [Should]: `validate.mjs` warns `[table-slip-key]` when a table `feedback.byKey` key is an editable cell id (`r0c1`, zero-based) and that cell has `wrong[]` entries (`table.js` returns the wrong id, so the line never fires for the slip). Message names file, path, cell id and the wrong ids to re-key to. Shared by every `checkFeedback` caller (lessons, reviews, homework, exams, drills, bank). Test: `tools/test-validate-table-slip-key.mjs` (4 of 4). Hits (43 at the time) listed in `docs/reports/scan-table-slip-keys.md`.

Status block (engine pass, item 584):
- 584: done (warning only; validator 0 errors; both table tests pass).

585. Done [Must]: `validate.mjs` warns `[shuffled-position]` when a `choice` or `multi` with `shuffle: true` has `explain`, an option `why`, a hint or a `feedback` line that names an option by place ("second option", "first answer", "top one", "the one above", "option B", "(c)"). Bare "the first" is not matched: it usually means the stem, and the first draft gave about 90 false hits. Covers lessons, reviews, homework, exams and bank through `checkItem`, parts and lesson screens (drills have no choice widgets). Test: `tools/test-validate-shuffled-position.mjs`. 14 hits, listed in `docs/reports/scan-positional-options.md`.
586. Done [Should]: `validate.mjs` warns `[key-length]` for a `choice` key of 12 or more characters and over 1.5 times every distractor. 1,658 hits at the time, so the threshold needs a decision before a content pass.
587. Done [Should]: `validate.mjs` warns `[multi-keys-uniform]` for an exam with four or more `multi` items that all have the same key count. 0 hits at the time. Tested with 585.

Status block (engine pass, items 585 to 587):
- 585: done (warning only; validator 0 errors; test passes).
- 586: done (warning only).
- 587: done (warning only).
588. Done [Must]: `tools/fresh-check.mjs` (`--exam <id> | --drill <id> | --bank <file> | --all-exams`, `--threshold`, `--json`). Compares prose, question and widget prompt text (numbers to a placeholder, KaTeX stripped) of each target item against every lesson screen, quiz, review, homework, exam, drill and bank item, and reports a shared 8-token n-gram or a 5-shingle Jaccard at or above 0.5; n-grams in more than 20 units are boilerplate; exit 1 on any hit. Test: `tools/test-fresh-check.mjs` (7 of 7). Calibration: pre-fix 0.6 item [6] and pre-fix 1.10 item [12] hit; 1.10 item [13] (integrand changed only) does not. Scan: `docs/reports/scan-freshness.md`.

Status block (engine pass, item 588):
- 588: done (new tool and test; validator 0 errors).

589. Done [Must]: exam longform marking. `screens/exam.js` `markWritten()` runs after submit (and after time-up), off the clock: it opens each written item's marking panel (the widget's own, as the homework page does), the learner ticks the rubric and presses Finish marking, or Skip marking (scores 0, result row says "Marking skipped"). A plain longform item's credit is ticks over rubric points (`ZQ.mock.tally` reads `rubric` credit), the row stays `how: self`. The test hook's `answer` only types the text and `check` defers (no more pre-marked answer); hook kind `mark` drives the step. `playthrough.mjs` `markStage()` clicks every rubric row and Finish, and checks the result rows. Forward-only papers unchanged.

Status block (engine pass, item 589):
- 589: done (see handback for playthrough results).

590. Done [Must]: rubric rows in the exam marking step took no click when a neighbouring row held a KaTeX fraction. KaTeX gives a fraction an invisible strut that reaches above its own row, so a click on the row above landed on it (the mock-video playthrough with `--local-cdn` timed out on the first rubric row, "subtree intercepts pointer events"; a real learner clicking the lower half of that row hit the wrong row). `css/widgets.css`: `.wd-rb .katex { pointer-events: none; }`, so the label takes every click. No engine JS or content change. Gates: `--exam mock-video` with and without `--local-cdn`, with and without `--mobile`, plus mock-superday-trader, topic-3.4 and mock-superday-developer.

Status block (engine pass, item 590):
- 590: done.

## Session V engine pass A (runtime and exams), items 591 to 599

591. Done [Must]: `choice` and `multi` shuffle by default. `widgets/_base.js` `orderOptions(spec, ctx)` shuffles unless `shuffle: false`, with `ctx.shuffleRng`, which `player.js` `buildScreen` seeds from the draft key, the screen key, the item id, the option ids and `ZQ.attempt` (new at every route change in `core.js`; `exam.js` sets it to the attempt seed, so `#exam/<id>/<seed>` fixes the order). A re-render in one attempt keeps the order. Every surface (lesson, quiz, review, homework, exam, mock, drill, bank, system samples) reaches the widget through `buildScreen`, so there is one path. Grading, `canvas` patches, `byKey` and the playthrough already work by option id (`widget.set(id)`), never by position; the 1 to 9 keys pick by shown position. Generated `arith` items shuffle too (their ids are hidden letters). Test: `tools/test-engine-runtime.mjs` (stable within an attempt, new for another, `shuffle: false` kept, graded by id). Content effect: 3,373 lesson `choice` widgets that listed the key first now move; any option set that is ordered or refers to its neighbours needs `shuffle: false` (agent B's `O2-unshuffled-numeric` and `[shuffled-position]` rules find them).
592. Done [Must]: `required: true` on an exam paper item. `mock.js` `requiredMissed(paper, results)` and `passed(paper, tally, results)`: the paper fails when a required item is not right, whatever the share or net. The start card gets a "Must be right to pass" rule naming the questions (and each paper row of a multi-paper exam a count), the open question a "Must be right to pass" tag, the result a line ("A required item was wrong, which fails the paper whatever the share") and the paper row the question numbers. `passedAuto` reads the same rule. Test: four cases in `test-engine-runtime.mjs`. Content: set `required: true` on the stage code exits (list in `docs/reports/engine-pass-v-a.md`).
593. Done [Must]: per-paper `tracks` on mock papers. `mock.js` `roleOf(track)` and `paperFor(paper, role)`; `exam.js` leaves an off-track paper out of the sitting (named on the start card with a link `#exam/<id>/all`), sits it as optional with the flag `all` (never gates, row says "Optional for your track, not counted"), and `as-<role>` sits as another role. Undecided counts as off every track. A mock with a left-out paper still reads as multi-paper. `playthrough.mjs` sits an exam with tracked papers through `all` (`xr()`). Test: seven cases in `test-engine-runtime.mjs`.
594. Done [Should]: draws seen in any exam or mock count as seen. `mock.js` `seenInfo` reads every other exam's attempts' `drawn` list: `{ why: 'other', rank: 0.75, exam }`, below this exam's sittings and above a library solve; label "Previously seen: sat in another exam". Test: `test-engine-runtime.mjs`.
595. Done [Should]: `importHint` reads a code test's `setup`. `code.js` `harness` (function mode) and `scriptHarness` add the `import` lines of every case's `setup` under `if False:`, so a data test that imports pandas loads it though the learner's code does not. Test: unit cases in `test-engine-runtime.mjs` (`Z.widgets.codeImports`). Content: starters that import an unused package only for a hidden setup may drop it (optional).
596. Done [Should]: `expression` `form: "rectangular"` and constant `simplified`. `widgets/expression.js` `exprForms` (`reducible`, `rectangular`) over canonical MathJSON: a constant answer must be one real part plus one imaginary term, with no two plain numbers added or multiplied, no division by a complex number and no bracket holding $i$ inside a product or power. Retyping $\frac{4+7i}{2-3i}$ returns the key `form`. Test: 30 unit cases on real Compute Engine output. Content: set `form` on the constant `expression` answers named in review-exam-1.11 (agent B adds the validator warning for a symbol-free answer with no `form`).
597. Done [Should]: automated test of the 589 Skip marking path. `test-engine-runtime.mjs` sits a synthetic mock with a written item, presses Skip marking and checks the written item scores 0, the paper fails at 100%, the row says "Marking skipped" and the line says it scores 0; Finish marking with every point ticked passes.
598. Done [Should]: a `longform` part inside `parts` scores ticks over points. `player.js` `renderParts` `gradeAll` gives a self-marked part its score over its rubric points and returns `credit` and `fractional: true`; `mock.tally`, the exam marks column, homework marks and a timed review's "counting each part" read that, so 8 of 10 ticks on a written part of two is 0.9, not a full mark. Right for mastery and `required` still means every part right. Test: two cases in `test-engine-runtime.mjs`.
599. Done [Could]: libc++ hardening without the tree walk. `cpp-worker.js` compiles with `-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_EXTENSIVE -D_LIBCPP_ENABLE_EXPERIMENTAL -D_LIBCPP_ASSERTION_SEMANTIC=_LIBCPP_ASSERTION_SEMANTIC_ENFORCE`: bounds messages kept, internal invariant checks (the map and set tree walk) off. Measured on the YoWASP clang 21.1.4-3 package: 20,000 `std::map` inserts and erases 1,730 ms in debug mode, 11 ms in extensive mode (7 ms with the flags above); the out-of-bounds message is identical to debug mode's with the flags, absent in extensive mode alone; a 28-header C++20 program compiles and runs. Not run any more: the comparator strict-weak-order check and the pedantic checks (documented in the C++ addendum). Gate: the C++ lessons, drills and exams in the full run.

Status block (Session V engine pass A):
- 591: done.
- 592: done.
- 593: done.
- 594: done.
- 595: done.
- 596: done.
- 597: done.
- 598: done.
- 599: done.

---

(separator: do not edit)

---

## Session V engine pass B (validator and tools), items 600 to 609

600. Done [Must]: `tools/fresh-check.mjs` counts word tokens only in a run (a maths span, a LaTeX command and a number are one placeholder that does not count), cuts a stop list of AUTHORING instruction sentences, and compares code function and class names (starter, solution, test call heads) of exam, drill and bank code items with every lesson, review and homework code widget (names under six characters without an underscore, generic names and names used in three or more courses are ignored). Mock versions are not compared with each other. Gate: `--min-run 12 --min-share 0.6`, Jaccard 0.5. The six session U topic exams (0.6, 1.10, 1.11, 2.5, 2.6, 3.4) give 0 hits; `--all-exams` gives 25 (17 code names, 8 prose), listed in the report. Test: `tools/test-fresh-check.mjs` (11 of 11).
601. Done [Must]: validator refinements, warnings only. `[table-slip-key]` (584) only when no `wrong[]` id of the cell has its own `byKey` line; `[shuffled-position]` (585) exclusions (the screen or parent item uses the place word or label, an earlier part's answer, a code block, `noPosCheck: true`); `[float-example]`; `[wrong-band]`; `[float-artefact]`; `[math-thousands-comma]` (house form `10{,}000`). Test: `tools/test-validate-session-v-b.mjs`.
602. Done [Must]: schema for pass A's runtime fields. `[shuffled-position]` now covers every choice and multi without `shuffle: false`; `[shuffle-false]` warns on `shuffle: false` unless the options are ordered numbers or intervals (`orderedOptionsWhy`, exported from `o2-rules.mjs`, no change to the O2 rule) or refer to each other; a non-boolean `shuffle` is an error. `required` on an exam paper item (boolean, error otherwise); `tracks` on a mock paper (non-empty list of known role ids, error on an unknown one); `expression` `form` gains `rectangular` beside the existing `expanded`, `factorised` and `simplified` (error on another value). Same test as 601.
603. Done [Should]: `tools/merge-wave.sh` keeps both sides of `docs/briefs/*.md`; for `docs/readiness.md` it keeps both sides and reduces a repeated row key to one row (ours when ours changed it, else theirs; `tools/union-table-rows.mjs`); after the validator it runs `node tools/readiness-sums.mjs --write` from `app/`, stages `content/readiness.json` and `docs/readiness.md`, and prints `readiness: OK | regenerated | FAIL (...)` before OK or FAIL. Test: `tools/test-merge-wave.sh` (a scratch repository built from a snapshot, since a clone of a shallow checkout cannot merge).

Status block (engine pass V-B, items 600 to 603):
- 600: done (gate set; six session U exams pass; test 11 of 11).
- 601: done (warnings only; validator 0 errors; test passes).
- 602: done (schema; validator 0 errors; test passes). Retire `O2-unshuffled-numeric` (73 warnings) once pass A's default shuffle lands: ordered numeric options no longer need `shuffle: true`.
- 603: done (test PASS merge-wave).

---

## Session V engine pass 7 (`docs/reports/engine-pass-7.md`), items 604 to 616

604. Done [Must]: `tools/fresh-check.mjs --file content/courses/<c>/<set>.json` works on a course review or homework set. A file inside `content/` keeps its own path (so the scan skips it as a source and no longer matches every item against itself), reads its code items from where it lives (no ENOENT on `content/exams/<set>.json`) and runs in about 13 s (the "over 120 s" reports were the crash path). Test: `tools/test-fresh-check.mjs`. Also lists, as advisory lines that leave exit 0 (a table of critical values is shared on purpose), a set item that shares three or more non-trivial numbers with one lesson screen of its course (`--shared-numbers n`, 0 off; item 614 in the report below).
605. Done [Must, warning]: `validate.mjs` `[shown-arithmetic]`. A `$...$` span that writes pure arithmetic (`a op b = c`, `\approx c`; `\times`, `/`, `+`, `-`, `^`, brackets, `\frac`) is recomputed with a small parser; it warns when the left side differs from `c` at `c`'s own places (one unit for `\approx`; `6{,}780` counts as three figures). A segment with a letter, `%` or another command is skipped, and a miss over 2% is read as a deliberate wrong claim (a distractor or a slip shown) and skipped. 197 hits in existing content before the 2% rule gave 278; read the arma, garch, coint, alpha, opt-dash ones first. Test: `tools/test-validate-shown-arithmetic.mjs`.
606. Done [Should]: `numbers_lib.py` reads hyphenated path keys (`feedback.byKey.test-3`), and adds `lv.claim(ok, label, note)`, `lv.claim_text(file, path, phrase, ok, label)` and `lv.stated(file, path, phrase, ok)` (fails only while the false phrase is in the text, so a script exits 0 once the content is fixed). Test: `tools/test-numbers-lib.py`; LEVEL-BRIEF names them.
607. Done [Should]: a table wider than its column shows a fade on its right edge while more lies to the right (`table` canvas `.cv-tbl-hold`, `table` widget `.wd-tablehold`, the console's cue). Not done: a playthrough check that every editable cell lies inside the viewport at each width (an answer column may still need a scroll; keep it in the first columns).
608. Done [Should]: lesson control rows (`.lsn-ctl`): the label takes at most 40% of the row and, at 520 px or less, sits above the track.
609. Done [Should]: `graph` below 440 px caps a `rect` or `pill` node at half the distance to its nearest same-row neighbour less 5 px (never under 20 px), in two passes, so a row of four labelled boxes keeps its edges (alpha l16 `screens[1]` checked at 440 px). Labels wrap or end in an ellipsis inside the box. README-B.
610. Done [Should]: `[wrong-band]` judges the slip as the learner rounds it: a value whose rounded form lies inside its band is no longer flagged (122 hits to 86).
611. Done [Could]: `[float-artefact]` also flags a signed zero (`-0.00`, `−0.00`) in prose and in `table` canvas cell text (a table cell was never run through the text checks); a spaced subtraction ("5 - 0.00") is not flagged.
612. Done [Could]: the start card of a mock whose papers (three or more) each hold one item shows "5 prompts, 11.5 minutes on the clocks" once, with the shared rules, and each paper by its minutes. Test: `test-engine-runtime.mjs`.
613. Done [Should]: `longform` aloud `think` (seconds of thinking time that run first and start the answer clock by themselves) and `lockAtZero` (the answer clock stops at 0:00 and the button locks); in an exam the help line says "The paper clock ends the sitting" and the maths-in-dollars line is dropped for spoken notes. Test: `test-engine-runtime.mjs`.
614. Done [Could]: the shared-numbers advisory of 604 (the arma "semantic repeat" bullet).
615. Done [Should]: `O2-unshuffled-numeric` retired (73 warnings): choice and multi shuffle by default (591), and `[shuffle-false]` judges an explicit `shuffle: false`.

616. Done [Must, protocol 6]: `order` widget `after: { line: [lines it must follow] }` (precedence rules; any topological order is correct, the key is the first line standing before a line it must follow, per-line marks follow the rule). Validator: shape errors, an answer that breaks a rule, a warning when `same` is also set. Tests: `test-engine-runtime.mjs` (2), `test-validate-session-v-b.mjs` (3). The inbox bullet on the review-analysis pass is not in this checkout's inbox (the older bullet on the law of total variance, which asked for the same `after` form, was moved here); the coordinator's copy should drop its bullet.
617. Done [Must, user bug 7 Nov]: a pass of topic 0.1 now moves Today on for good. Cause: the lesson player's `savePosition` (run on leaving a lesson by the route, the close button, Back or a reload on a lesson route) always wrote a fresh `positionAt`, so merely reopening a part-open lesson after the pass made `ZQ.content.resumeStands` (461) read the resume as saved after the pass; the user's stored resume already carries such a time. Fix: the rule now follows the learner's intent. `state.lessonPosition.pick(course, lesson)` stamps `pickedAt`, called only by the course map `launch` for a lesson (the Learn path); `summary().resume` carries `pickedAt`; `resumeStands` compares `pickedAt`, not the save time, with the pass time. Old records have no `pickedAt`, so a stale resume is skipped with no migration. Today, Back, a direct link and a reload never stamp it. `savePosition` also no longer rewrites an unchanged place (`app/js/engine/player.js`). Test: `app/tools/test-today-tested-out.mjs` (12 checks; the stale-resume check and the others failed before).

Closed, landed earlier (the inbox bullet remained after the item landed): Mark my answer for exam longform is 589 and 597; the shuffle default in the runtime is 591; `[shuffled-position]` false positives are 601; `importHint` reading `setup` is 595; per-paper `tracks` is 593; the libc++ hardening mode is 599; code-name comparison in `fresh-check` is 600.

Items 340 to 422 checked against the code and found already done (status only, no change): 343 (AUTHORING now documents `solution`), 347 (README-B: bins are `[lo, hi)`), 348 (number-line prints U+2212), 390 (`compare: "bigO"` on a table cell), 395 and 414 (`__learner_source__` always defined; AUTHORING says so), 399 (see 609), 415 (README-B corrected). All other open items in 340 to 422 and the remaining inbox bullets are deferred (see the report).

Status block (Session V engine pass 7):
- 616: done.
- 617: done (test-today-tested-out 12 of 12; failed before the fix).
- 604: done (test 12 of 12; course sets run in about 13 s). 605: done (warning; test passes). 606: done (test-numbers-lib passes).
- 607: done (cue only; no viewport check). 608: done. 609: done (screenshot at 440 px). 610: done. 611: done. 612: done. 613: done. 614: done (advisory). 615: done.
618. Done [Must, user bug 7 Nov]: `ZQ.grade.exprEqual` compared two equations by truth value at the sample points, so any two equations were equal (`n=5` against `n=\frac{a}{c-b}`). Now `splitRel` finds one top-level relation (`=`, `<`, `>`, `\le`, `\ge`, `\ne` and their spellings; `>` and `\ge` are turned round) and two relations are equal only when they are the same kind and `lhs - rhs` of one is a nonzero constant multiple of the other's at every sample point (a positive multiple for `<` and `\le`; any nonzero multiple for `=` and `\ne`). So `y=2x+1` equals `2x+1=y` and `2y=4x+2`; `x<3` equals `3>x` and `2x<6` but not `x>3`, `-x<-3` or `x\le3`. An equation against a non-equation is unequal; a chain (`1<x<3`) is equal only to the identical text; `upToConstant` refuses any relation. Audit of `app/content`: 520 `expression` widgets, none has a relation in `answer`, `accept` or `wrong[].tex`, so none accepted a wrong equation (no content change). Test: `app/tools/test-expr-equations.mjs` (37 checks, 14 failed on the old grader; `--audit`, `--full`).
   Also raised: review equations L3 to L4; review functions L1 to L2
619. Done [Should]: a learner's `<one letter, Greek letter, subscripted letter or \text{...}> = <expr>` (either side) is graded as `<expr>` when the authored answer has no relation, so `n=\frac{a}{c-b}`, `C = 3 + 2n`, `\text{cost} = 3 + 2n` and `3 + 2n = C` pass for the expression. It marks the answer correct (no `formula` key line). Only an equality qualifies, not an inequality. Same test. Documented in AUTHORING (expression widget).
   Also raised: review equations L1 to L2; review equations L3 to L4; review exp-log L1 to L3; review series L1 to L3

620. Done [Should]: the 619 strip now also drops a left (or right) side that is a decorated or subscripted symbol (`S_\infty`, `u_{n+1}`, `\bar{x}`, `x'`), a function call of symbols (`f(x)`, `f(k)`, `g(t)`, `f(x,y)`), or a name of two or more letters (`OB`, `TM`) when none of its letters is a symbol of the authored answer. With no label on either side, `L = R` is accepted only when `L` and `R` are equal expressions and `R` equals the answer (restated expand items). No item field gives the stated expression in machine-readable form, so the equal-sides rule is used. Wrong `R` never passes and `y=5` does not pass for a non-constant answer; a false restatement gets the generic line. Cause: 619 allowed only a single symbol. Same test (129 checks, 40 failed on the 619 grader). Documented in AUTHORING (expression widget).
   Also raised: review functions L3 to L4

Status block (engine pass 621):
- 621: done.

621. Done [Should, review exam topic-2.2 Engine 1]: the Learn topic-exam chip showed `examMinutes(t.hours)` (45, 60 or 90) while `exam.js` runs the file's `minutes` (topic-2.2 and topic-2.6 store 75, both chips said 45). The validator now writes `examMinutes` (exam id to the minutes the exam screen runs: the top-level `minutes`, or 60 when absent, and for an exam with `parts` the sum over its papers) into `content/manifest.json`; `ZQ.content.examMinutes(id)` reads it, and the chip uses it, keeping the hours-based figure only as a fallback with no manifest. The other places that show a duration (Review topic and mock cards, the exam intro) already read the loaded exam file; Prepare, Today and the course map show none. Files: `app/js/content.js`, `app/js/screens/learn.js`, `app/tools/validate.mjs`, new `app/tools/test-exam-minutes.mjs` (56 exams; failed 56 of 56 before the fix). Documented in AUTHORING (topic exam).
   Also raised: review exam topic-2.2

---

## Session X triage (7 Nov): session W inbox bullets, items 622 to 697

622. [Could] Validator: when a numeric item or table cell names a number of decimal places, warn if `tol.abs` exceeds half a unit in that place, or an `accept`, hint or `byKey` value rounds outside the band, so both roundings of a 5 at the next place are not accepted or refused by accident. Cheap rule, false hits likely low. [audit mental-pressure; review exam topic-0.1; review exam topic-0.3]
623. [Should] Validator: warn when a prompt names a protocol-dependent puzzle ("Monty Hall", "host opens", "boy or girl") and none of "knows", "always", "at random", "protocol". An unstated protocol makes the keyed answer wrong, and no rule sees it. [audit puzzles]
624. [Should] Process: census or validator line listing levels with a report in `docs/reports/` but no committed `<course>-L<n>-numbers.py` (SESSION PROTOCOL 4 requires it), or a LEVEL-BRIEF note. Should: protocol gate currently unenforced in two courses. [audit puzzles; audit systems]
625. [Could] Concept scripts: an agreed expected-fail marker (for example `EXPECT_FAIL = {"check": "finding N"}`) so a designed failure reads differently from a regression in the orchestrator's exit-code check. [audit puzzles; audit research-int]
626. [Could] Tool `node tools/dump.mjs <course>/<id> [--level n]` printing every author-facing string with its JSON path, canvas labels, edge weights, captions and table cells included, numbers folded. Blind readers and auditors each rebuilt this by hand. [audit puzzles; review pairs-rep round 2]
627. [Could] Seeded simulations: recompute an `explain` that quotes a seeded run (`walk`, `bars` `sim`), or document the seed, generator and draw order in the canvas README so a concept script can replicate it. Eleven research-int figures and game-theory l15 were taken as data. [audit game-theory; audit research-int]
628. [Should] Validator: check cross-course lesson references in learner prose ("Contest Practice, lesson 8 (Parity and invariants)") against the other course's `course.json` names and level map. Brainteasers carries 15, all checked by hand. Should: wrong references mislead learners. [audit brainteasers]
629. [Could] `order` (derive) widget: optional `why` on correct lines, shown in Why? after grading, and a validator warning when a derive has none, so an unproved step can be read and checked. [audit brainteasers]
630. [Should] Process: LEVEL-BRIEF tells each agent to work in `scratchpad/<branch-name>/`; the shared scratchpad let a sibling overwrite files mid-audit. Should: silent wrong-file reads. [audit coding-int]
631. [Could] Tool `node tools/run-code-tests.mjs <file> <path>` (or `run-widget.mjs --cpp`) running a C++ widget's hidden tests with the local compiler, reporting solution pass and starter fail. Each concepts script carries its own g++ harness. [audit coding-int; audit systems]
632. [Could] `code` widget: optional `reference` (a second or brute-force implementation) that the playthrough compares with the model solution, so a solution passing by a worse method than the lesson names is caught. [audit coding-int]
633. [Could] Tool `tools/compile-listings.mjs` compiling `console` canvases marked `language: "cpp"` with the app's clang and standard, catching C++20-only API in a C++17 course (systems l6, l7). [audit systems]
634. [Could] Validator: warn when prose says "independently", "at random" or "loses x%" and the question starts "How many" without "on average" or "expected", since the key is an expectation, not an exact count. [audit systems]
635. [Should] Playthrough: the timed checks of `research-int/review-1` time out twice with `--local-cdn` while review-2 passes. Diagnose (a `parts` item in a timed set, level-1 `requires` gates). Should: it blocks that set's green run. [audit research-int]
636. [Could] Validator: warn when a code `prelude` or solution computes a whole-file statistic (`fillna(...median())`, scaler fit) before `train_test_split`, the leak the course teaches against. [audit research-int]
637. [Could] Validator `[scheme-unstated]`: warn when a table row mentions "guess", "net" or "answering" without the marking scheme (+1, −1/3, "no penalty") that a sibling row states. [audit mental-pressure L4]
638. [Could] Lift the sequence-rule enumerator (`simple_rules`, `simple_rules_half`) of `mental-pressure-L4-concepts.py` into a shared helper for the other sequence courses. [audit mental-pressure L4]
639. [Could] C++ `code` widget: a two-thread option (no `<thread>` in the wasm build today), or an AUTHORING note that SPSC atomics items are graded single-threaded (systems l16 `screens[9]`). Hard; could only be documented. [audit systems L4]
640. [Could] AUTHORING section 3 and validator: one documented `tests[].expect` shape per language (Python source text, C++ JSON values) so concept scripts need no special case. [audit systems L4]
641. [Could] Playthrough: for an `allocCheck` item report whether the starter fails the `alloc_count()` test itself; today it passes that test and fails only on the contract (systems l15 `screens[9]`, homework-4). [audit systems L4 round 2]
642. [Could] `numbers_lib` shared code-item runner (`Level.run_code` / `lv.check_code`): solution and starter over every example and test with `prelude`, `setup`, `expect` as Python source, compare rules (`isclose` 1e-9, `fraction`, `raises`), `how` count and `byKey` `test-N` checks. [audit measure-prob; review py-found L1 to L2; review proof L1 to L3; review exam topic-0.4]
643. [Should] Validator `[shuffled-position]` and `[shuffle-false]` refinements: ignore hyphenated compounds ("first-year"), but flag a bare "the first/only the first sentence" on an option, and read "$n = 4$" options as ordered numbers. Should: both directions currently miss real hits. [review momentum-rep L1; review proof L1 to L3]
644. [Could] `fresh-check.mjs --file`: flag a set item whose graded numeric answer, at its asked rounding, is stated as fact in a lesson screen of the same course (momentum-rep review-1 `items[5]`). [review momentum-rep L1]
645. [Should] Validator `[float-artefact]` opt-out (ignore file, or skip values in backticks or after "prints"/"is", or quoted in the item's own prose code block). 34 hits in py-found L1 on floats the lessons must print. [review py-found L1 to L2; review exam topic-1.2]
646. [Should] Playthrough `"verify": "stdout"` on a choice item with a python block (run in Pyodide, compare the keyed option's code spans) and an advisory pass for "What does it print?" items. py-found l1 `quiz[3]` and l11 `quiz[2]` keyed wrong output and passed. [review py-found L1 to L2; review py-found L3 L4]
647. [Could] `numbers_lib` tokeniser: read a number inside a braced LaTeX argument (`\sqrt{56}`, `\sqrt{0.0025}`) and `a \cdot 10^{b}`, `10^{b}`, so `expect` needs no hand-written `fmt`. [review linear-maps L1 to L3; review counting L1 to L3; review exam topic-2.4]
648. [Could] `fresh-check.mjs --file`: compare `pmatrix` bodies and tuple literals as whole tokens, so a set item reusing a lesson's matrix or basis with a new target is caught. [review linear-maps L1 to L3]
649. [Could] Validator `[key-length]` (586): warn only when the key has a reason clause no distractor has, measure rendered text (strip LaTeX commands, braces, `$`), and exempt all-code-span options whose key extends a distractor. [review linear-maps L1 to L3; review series L1 to L3; review trig L1 to L3; review sql L1 to L3]
650. [Could] Series canvas: the `drawdown: true` overlay labels its band "Max drawdown −3.6%" while lessons define drawdown as positive (py-found l16 `screens[9]`). Drop the minus or add `params.drawdownSign`. [review py-found L3 L4]
651. [Should] Validator `unit "%"` above-1 rule (515): apply to `answer` only, since deliberate `wrong[]` slips (×252, flipped fractions) must exceed 100%; and `numbers_lib.check_wrongs` should read a `%` line against the fraction (228 false alarms in ratio). Should: 18+ false hits. [review py-found L3 L4; review plotting L1 to L3; review ratio L1 to L3]
652. [Should] Validator `[float-example]` (601): skip an example whose `call` rounds (`round(`, `np.round(`, `.round(`) or reads back input floats unchanged. 11 hits in numpy-pandas and plotting, all pass exactly. [review numpy-pandas L1 to L3; review plotting L1 to L3]
653. [Could] Table canvas: `white-space: nowrap` on row-head cells so ISO dates keep to one line at 440 px (numpy-pandas l10, l11). [review numpy-pandas L1 to L3]
654. [Could] `numbers_lib` `lv.prints(file, path, code)`: run a "What does it print" snippet and compare with an option's text, lifted from `numpy-pandas-L1-numbers.py`. [review numpy-pandas L1 to L3]
655. [Could] `fresh-check.mjs` false positives: a code-name hit where only a function name is shared with unrelated bodies (git homework-2 against ds l15), or the item's own starter or prelude defines it (topic-2.2). Require a shared test call or body line; skip self-defined names; do not exit 1 for advisory. [review git L1 to L3; review exam topic-2.2]
656. [Could] Advisory tool replaying fenced `$ git ...` or shell transcripts in a throwaway directory and diffing the printed lines; git review replayed 27 findings by hand. [review git L1 to L3]
657. [Could] AUTHORING runtime notes and validator rule: quoted pytest output must match pytest 8.1.1 (`±` form, `DID NOT RAISE <class ...>`); SQLite is 3.39.0 (round float aggregates); `sum()` of floats is compensated from Python 3.12; tracebacks come from python3.12 with `^^^^` lines. [review pytest L1 to L3; review sql L1 to L3; review exam topic-1.2; review exam topic-0.4]
658. [Could] Validator: warn when a `table` canvas cell starts with pytest prefixes (`>       `, `E       `) or `$ `, and suggest the `console` canvas. [review pytest L1 to L3]
659. [Should] Playthrough or validator: rerun each SQL solution with reversed row order to find a test expecting an unfixed tie order (sql homework-2 `items[2]` test 2). Should: it fails a correct learner answer. [review sql L1 to L3]
660. [Should] `numeric` widget: optional `"places": n` accepting only entries with exactly n decimals (4.0 against 4, £13.00 against 13), with a slip key otherwise. Should: GCSE marking asks for it. [review number-sense L1 to L3]
661. [Could] Validator: warn when a `numeric` `placeholder` parses inside the answer band or a `wrong[]` band (number-sense l3 `quiz[3]`). [review number-sense L1 to L3]
662. [Could] Validator: warn on authoring jargon in learner-facing strings ("edge case", "distractor", "misconception", "trap screen"). [review number-sense L1 to L3]
663. [Could] Validator advisory: a lesson with no `explore`, or no `generalise` or `derive`, against the lesson shape of AUTHORING section 2 (equations l5 to l9). [review equations L1 to L2]
664. [Could] Tool `tools/expr-forms.mjs <file> <path> --ok ... --bad ...` and an exported `ZQ.widgets.exprGrade(ce, spec, latex)` (accept, `form`, then `wrong` routing) so readers and `test-expr-equations.mjs` stop hand-rolling a harness. [review equations L1 to L2; review exam topic-0.2]
665. [Could] `numbers_lib` `lv.other(file, path)` or an "L2:l9" reference for cross-level continuity checks. [review equations L3 to L4]
666. [Could] Validator `[wrong-band]` (610): skip when another `wrong[]` value equals the flagged value rounded as asked (equations homework-3 `items[6]`). [review equations L3 to L4]
667. [Should] `drag-point` (`drag-point.js` line 86): test each `wrong[]` region against the points not on target only, so a correct point inside a region does not fire the slip (functions l3 `screens[4]`). [review functions L1 to L2]
668. [Should] Validator: error on `=` in an expression `answer`, `accept[]` or `wrong[].tex`; listing `y = ...` forms is an unsafe workaround that grades unrelated equations right. [review functions L3 to L4]
669. [Could] Expression grader: compare a `\pm` key as a pair of values (`-1\pm\sqrt{3}` against `-1+\sqrt{3}`); none live yet. [review quadratics L1 to L3]
670. [Could] Expression `form: "simplified"`: make it consistent on surd constants and refuse an uncancelled or retyped-decimal rational (`\frac{27}{99}` for `\frac{3}{11}`). [review quadratics L1 to L3; review series L1 to L3]
671. [Could] `plane` label placement: keep a function label off its own curve, give y-tick halos no cover over curves, and honour an explicit `labelPos: "n"` where room allows. [review functions L1 to L2; review quadratics L1 to L3; review trig L1 to L3]
672. [Could] Validator `[shown-arithmetic]` (605): in a chain "$a \approx b \times c = d$" the final `=` seems to take the `\approx` tolerance (exp-log homework-1 `items[7]`); check the last link exactly. [review exp-log L1 to L3]
673. [Could] Expression grader: strip `\mathbf{}` and `\boldsymbol{}` around a single letter before parsing, so `4\mathbf{a}+\mathbf{b}` matches `4a+b`. [review counting L1 to L3]
674. [Could] Validator `O2-explain-answer` (527): read thin-space thousands (`15\,600`) as the number; false hits in counting. [review counting L1 to L3]
675. [Could] Validator advisory: a `bars` canvas with `showValues` on a task screen that starts with a 0 bar and no `showZero: false` (series l1, l4, l5). [review series L1 to L3]
676. [Should] Expression grader: a correct decimal for an exact answer (`1.414` for $\sqrt{2}$) gets the generic line; add a built-in key saying the decimal is right but exact form is wanted. Should: it reads as a wrong method. [review trig L1 to L3]
677. [Should] Copy button (`grade.js` line 587): on `sh`, `bash`, `console` and `shell` blocks copy only `$ `/`% ` lines with the prompt removed, so pasted blocks run. [review terminal L1 to L3]
678. [Could] `table` canvas: `mono: true` per table or column that keeps leading spaces and uses the code font, so a traceback caret lines up (terminal l12). [review terminal L1 to L3]
679. [Could] `graph` canvas: a directed edge between touching nodes shows no arrowhead and no warning (terminal l11, `nodeRadius` 56); shrink the radius or warn in the validator. [review terminal L1 to L3]
680. [Could] `O2-long-explain` and `voice-scan.py`: do not count a lone `.` or `..` between spaces, or after a colon, as a sentence end. [review terminal L1 to L3]
681. [Should] Code widget `byKey.error` fires only when the load fails, never for a raise inside a test, and only the first failing test keys a line. Document it in AUTHORING; add a validator advisory for `error` lines on a module-level-call solution and for later-test lines an earlier test catches. [review first-python L1 to L3; review exam topic-1.1; review exam topic-0.4]
682. [Could] Validator advisory: a ```` ```text ```` Traceback block where a code line is followed by the error with no `^` or `~` caret line (15 quoted in first-python). [review first-python L1 to L3]
683. [Could] Homework page: close the first-visit coach tip once an answer is marked (it covers the header at 440 px). [review proof L1 to L3]
684. [Could] Series canvas and `bars`: warn in the validator when a fixed `hlines` entry lies outside an explicit `y` (or `yMin`/`yMax`) range; it is skipped silently with its label. [review exam topic-2.2]
685. [Could] Validator: warn when a code item's hidden test equals one of its examples (same `call` and `setup`, or `stdin`); seen in topic-2.2, 3.1 and 0.4. [review exam topic-2.2; review exam topic-0.4]
686. [Could] `numbers_lib.Exam(path)` entry point for exam readers, and rename the brief's `numbers.py` (shadows the standard library `numbers` that NumPy imports) to a safe name. [review exam topic-2.2; review exam topic-0.1]
687. [Should] `fresh-check.mjs` setup signature check: fingerprint answer, `wrong` values and ids, option and order-line texts, matrix and number sets, test `call` strings, whole-widget copies and one-line setups. The prose gate gave 0 hits where readers found 8 to 22 repeats per exam in session W's nine topic exams. Should: it is the only freshness gate. [review exam topic-2.3; review exam topic-2.4; review exam topic-1.2; review exam topic-0.1; review exam topic-0.2; review exam topic-0.3; review exam topic-0.4; review first-python L1 to L3; orchestrator, session W]
688. [Could] Validator: warn when a code item's example `setup` holds a numeric list equal to another item's series or prose list in the same exam (topic-2.3 `e-code-tear-line`). [review exam topic-2.3]
689. [Could] Validator: warn on TeX outside `$...$` in learner-facing strings (`^{`, `_{`, `\frac`, `\sqrt`, `\times`); topic-2.3 `e-implied-q` shows raw `e^{0.05}`. [review exam topic-2.3]
690. [Could] Exam start card: `exam.js` writes `${doc.name} covers ...` with no article; say "The Python topic exam covers ...". [review exam topic-1.1]
691. [Could] `numeric` widget `"form": "fraction"` (a/b or mixed number, optionally lowest terms, with a slip line), since 1.583 and 38/24 both pass today (topic-0.1 `e-mixed-subtract`). [review exam topic-0.1]
692. [Should] Expression `formOk` judges the whole typed LaTeX, so `y=4x^2+4x-2` fails `form: "expanded"`; judge the right-hand side after the 619/620 label strip (topic-0.2). [review exam topic-0.2]
693. [Should] Expression label strip (620): count a composite as a label (`g(f(x))`, `g\left(f\left(x\right)\right)`, `gf(x)`, `fg(x)`), with or without `functions`. Should: a correct answer gets the generic line. [review exam topic-0.2; orchestrator, session W]
694. [Could] Validator advisory `exam-no-pace`: a topic exam with no `pace` on any item, and paces summing under two thirds of, or over, `minutes`. [review exam topic-0.2]
695. [Could] `vectors` canvas: `axes: false` or `ticks: false`, so a vector-geometry item in a and b hides numbered axes (topic-0.3 `e-vector-ratio`). [review exam topic-0.3]
696. [Should] Tool or validator: check that an exam item needs only constructs its topic's courses teach (topic-0.4 uses seven absent from terminal and first-python). [review exam topic-0.4]
697. [Should] Validator: a `longform` must carry `widget.prompt`, yet reviews asked to drop a prompt repeating the item `prose`. Make the rule "prose or prompt, not both", or let `prompt` default to `prose`. Related to 297. [orchestrator, session W]

Status block (Session X triage, 7 Nov):
- New items: 622 to 697 (76), all open, none implemented.
- Merged into existing items: 8 bullets (Also raised lines under 348, 618, 619, 620, 621).
- Dropped as content notes: 3 bullets (listed in `docs/reports/engine-inbox-session-x.md`).
- Remaining 121 of the 132 bullets read are folded into the 76 new items; `docs/BACKLOG-INBOX.md` untouched.

698. Done [Should] (protocol 6, five sightings: review-perf-pilots R2, review-perf-retrofit-1 RI2-1, review-perf-retrofit-2 SY3-2, MP1-1, MP3-1) `tools/rubric-passes.mjs --item <file>#<id>` (and `--course <id>` for every performance item in a course) prints every rubric tick set that passes (at least 7 of 10 with every `required` row ticked), marking the minimal ones, so an author or reader sees a pass that skips a named part. Exit 0 always; a validator advisory is optional. Test under `tools/test-rubric-passes.mjs`. Document in AUTHORING section 5.

699. Done [Should] (protocol 6, seven sightings: review-perf-retrofit-3 RPT, review-perf-retrofit-4 overlap findings) `tools/perf-reports.mjs` checks every `docs/reports/<course>-<n>-perf.md` for a level whose task is in `content/manifest.json` `perf`: the report names the item id, the kind, the matched objective, an "Overlapping screens" line (screens, or "none" with the grep terms), and the four gate results; prints one line per missing part, exit 1 if any. Test `tools/test-perf-reports.mjs`. Document in AUTHORING section 5.

700. Done [Should] (protocol 6, six sightings: BACKLOG-INBOX lines on `exercise_boundary`, `formation_returns`, research-int DataFrames, opt-dash `h-parity-fit` and `h-black-iv`, validation `h-label-purge`, fin-ml `h-return-rank`) `code` widget `isclose` and `equal` treat NaN as equal to NaN when the expected value holds NaN at that position (scalars, lists, NumPy arrays, pandas Series), and compare a pandas DataFrame through `.to_numpy().tolist()` plus its index and columns. An actual NaN where a number is expected, or a number where NaN is expected, still fails. Both Pyodide (`app/js/engine/`) and the playthrough's grader path. Also dicts: compared by exact key set, then value by value with the same rules (opt-dash L4, py-found L2). Test cases in the code-widget test; document in AUTHORING section 3 `compare`.

701. Done [Should] (protocol 6, six sightings in session X perf bullets: puzzles L4, measure-prob, ito L3, contests L3, limits-thm, linear-maps L3) `playthrough.mjs --shots`: the `-marked` shot of a longform item is full height (the whole model and rubric after Mark my answer, `fullPage` or a scroll-and-stitch of the item's card), and the playthrough fails an item where a `.katex-display` inside the model, rubric or prompt is wider than its column at the current viewport (scrollWidth > clientWidth + 1), printing the item id and the first 40 characters of the TeX. Both desktop and `--mobile`. Test with a fixture longform holding an over-wide display. Document in AUTHORING section 5 and LEVEL-BRIEF.

701 status: done. `playthrough.mjs` shoots the marked longform card whole (element screenshot), checks `.katex-display` overflow at desktop and each extra width, `ZQ_APP_DIR` env overrides the served app; test `tools/test-playthrough-overflow.mjs` with `tools/fixtures/overflow/`.

702. Done [Should] (protocol 6, four sightings: review-perf-retrofit-7 analysis rows 5, review-perf-retrofit-9 limits-thm L1 to L3) Validator warning `[perf-optional-row]` on a performance item (homework or review, `performance` set) whose rubric has a row without `required: true` while the item's prompt text (item `prose`, `question` and the widget `prompt`) contains no "Optional" or "optional" mark. Advisory, not an error (a row may grade quality rather than a named part). Test case under `tools/fixtures/perf/`. Document in AUTHORING section 5 beside the required-row rule (DECISIONS "Session X operating decisions", optional sub-questions).

702 status: done. `[perf-optional-row]` advisory in `validate.mjs` (rule in `perf-rules.mjs` `optionalRows`), count line after the O2 line; fixtures `tools/fixtures/perf/{ok-optional-marked,warn-optional-unmarked,ok-all-required}.json`; 40 items flagged on the repository.

703. Done [Could] (follow-up to 701; sightings after 701: taylor L1, micro L3, and earlier conditional L2) The `-marked` element shot (`shot(..., '.hw-item:not([hidden])')`) is white below the first viewport at 440 px: the app scrolls in an inner container, so Chromium does not paint the card beyond the viewport. Before an element shot, set the viewport height to the element's full height (bounded, for example 8000 px), snap, then restore the viewport. The overflow check (DOM measure) is unaffected. Test: a fixture item whose model is three viewports tall; assert the PNG height covers the card and its lowest pixel row is not all white.

703 status: done. The `shot` helper grows the viewport (at most 8000 px) to the card's full height, including an inner scroll container, before an element shot, then restores it, at desktop and every extra width. Test `tools/test-playthrough-tall.mjs` (fixture `tools/fixtures/overflow/homework-2-tall.json`, own PNG decoder): fails without the fix, passes with it.
704. Done [Should] The routes block's test-out probe picks a direct prerequisite with a written review and no gating performance task, so the met-rule badge case (529) no longer fails the "level met" and "card still lists" checks; a second assertion covers a level that does carry a gating task.
704 status: done. A passed test-out there is recorded as passed, the level stays unmet, and the lock card row reads "performance task not passed". Tool change only (`tools/playthrough.mjs`); routes-only green at desktop and `--mobile`.

Raised later (session Y inbox numbering, 9 Nov; sources are the inbox's perf-retrofit bullets added after the session X triage):

705. [Should] Homework page wording on an `aloud` item: the banner still reads "Write your working first. Then mark it against the model answer." and the help line under the clock reads "Say your answer aloud. The paper clock ends the sitting." (the exam text, `longform.js:47`) though a homework has no paper clock and sets `lockAtZero`. Use the aloud wording when the item has `seconds`, and the `lock` line ("The clock stops at zero.") outside a real exam. [arma L1 perf, ito L4 perf]
706. [Could] `aloud` follow-ups: say before the clock that they come ("n follow-up questions after the clock", from `followUps.length`), and step them after the clock, before Mark my answer, so a rubric row can grade a follow-up answer honestly. Related to 536 (deferred). [ito L4 perf, coint L1 perf]
707. [Should] `aloud` widget: an optional `reveal` list, each step shown on a tap once the answer clock runs, for a round that reveals trades and cards one at a time (mm-games `h-coin-dice-aloud`, six steps). [mm-games L3 perf]
708. [Could] `aloud` longform whose product includes code: an optional `codeNotes: "python"` showing a code editor with Run examples, still self-marked (coding-int `h4-pairs-aloud`). [coding-int L4 perf]
709. [Should] Follow-up to 701: the playthrough's width check measures `.katex-display` only, and `scrollWidth` or the `.katex-html` rectangle reports the full column for a display that fills it. Measure from the leftmost to the rightmost `.katex-html > .base` span, and check every inline `.katex` whose right edge passes the card's (prompt, model, rubric), naming `<file>#<item id>` and the TeX. A `\sqrt` display reads far too wide in a scratch check, so widths need a sanity bound. [regression L1 perf, trees L1 perf, analysis L4 perf, limits-thm L3 perf]
710. [Should] Longform rubric row at 440 px: the points label is cut at the card edge ("3 points, requ") on a `required` row, and a wide inline maths span in the text pushes it off (estimation `h-mle-pareto`, arma `h-derive-arma-fan` row 3). Keep the label at its width (no shrink) with a "Required" chip, and let the text column wrap or scroll the span; or warn on a rubric maths span over about 30 characters. [puzzles L4 perf, arma L3 perf, estimation L2 perf]
711. [Could] Playthrough cannot run extra solutions in Pyodide: a slow but correct answer, planted wrong solutions or wrong test files, or a rank-deficient case that depends on the LAPACK build. Wanted: `playthrough.mjs --set <id> --variant <item>=<file>` that plays a file as the solution, prints each case's time and the first failing test; and an optional widget `wrongs` or `plants` list (source and the tests it must fail), and `slowSolutions`, pasted and checked like the starter. [coding-int L3 perf, graphs-dp L1 perf (a second vote after the topic-1.9 exam bullet), algo-think L2 perf, pytest L2 perf, vectors L3 perf]
712. [Could] Playthrough count after a stopped worker: a timed-out item 9 was reported "marked 6 of 9 right" and "scored 5 of 9 right, expected 8" though only that item had changed. Look at how a stopped Pyodide worker disturbs the count. [coding-int L3 perf]
713. [Could] C++ `code` widget: grade the shape of the compiled code, so "remove a branch from a hot loop" can be a `code` performance task (a case that greps the `-S` output of the learner's function for a conditional jump). Only if such tasks matter; systems L1 used `aloud`. [systems L1 perf]
714. [Could] A homework or review item `question` renders as one bold line, so a markdown list in it runs together. Render lists in `question`, or warn on a list there. [systems L4 perf]
715. [Could] C++ runtime has no threads, so a single-producer, single-consumer task cannot grade memory orders (`h4-spsc-ring` passes with relaxed orders, review-perf-retrofit-2 SY4-1). Note in AUTHORING section 3 that concurrency correctness is ungradable, or add a `console` pattern for a desk ThreadSanitizer run. [systems L4 perf and fix pass]
716. [Should] A `data` performance task needs its file under `app/content/data/<course>/`, which content agents may not edit. Allow a `data` path inside the course folder, or let content agents add files there (backtest `h-reversal-note` fell back to `derivation`). [backtest L4 perf]
717. [Should] `grade.prose` has no headings, so a longform model written as a document shows `# Title` literally (`backtest/homework-4` `h-note`). Render `#` to `###` lines as headings, or warn on a line that starts with `#` in prose, a model or a prompt. [backtest L4 perf]
718. [Could] AUTHORING section 5: say that a longform carries `prose` or `prompt`, not both, and that a long brief with a canvas must sit in `prompt` (above the canvas). Related to 697. [backtest L4 perf]
719. [Could] `isclose` (and `equal`) compares lists, arrays and Series but not dicts; compare key sets equal and values by key, so a function returning a dict of floats needs no `sorted(d.items())` or `[d[k] for k in KEYS]` workaround (`h4-weekend-explain`, `h-book-weights`). Follows 700. [opt-dash L4 perf, py-found L2 perf]
720. [Could] Validator warning on an `isclose` case whose non-zero `expect` is below 1e-10 in size and has no `tol` (the default absolute 1e-12 passes a function that returns 0 for 3.2e-14; `h-perf-corridor` sets `tol: { rel: 1e-9 }` by hand). [cpp-pricing L1 perf]
721. [Could] Method checks without hand-written AST tests: a shared `"noLoop": ["fn"]` option (backtest `h-breakout-twice`) and `"recursive": "fn"` (some function in the learner's code calls itself; algo-think `h-split-feed`), each with its own result row and the line found. [backtest L1 perf, algo-think L2 perf]
722. [Could] Third sighting (stat-learning L2, garch L2, mm-games L3): `playthrough.mjs --set` reads `content/manifest.json`, so after the brief's `git checkout app/content/manifest.json` a new performance task shows as "practice only". Rebuild the `perf` rows in the playthrough, warn when a `performance` item has no manifest row, or order the brief validate, playthrough, restore. Protocol 6. [stat-learning L2, garch L2, mm-games L3 perf]
723. [Could] Homework page at 440 px: the longform toast from item 8 still covers the header of item 9; clear it when the learner moves to another item (`stat-learning/homework-2`). [stat-learning L2 perf]
724. [Could] C++ `code` widget: an optional second editable file (`edit: ["returns.h", "main.cpp"]`), compiled and linked as `files` are, so an objective that names a header can be a performance task. [cpp L1 perf]
725. [Could] C++ `code` widget: a check that the data members are private whatever names the learner chooses (`"privateData": "SessionRange<int>"` failing on a public non-static data member). `h-session-range` and `h5-sole-and-counted` say in `how` that no test sees it. [cpp L3 perf, cpp L5 perf]
726. [Could] C++ planted-bug grading in script mode: a case that passes on the expected text or an abnormal end (`"compare": "stdout", "orStops": true`), so a learner input may crash any slip (`h4-test-median`). [cpp L4 perf]
727. [Could] C++ widget flag `"nullCheck": true` adding `-fsanitize=null -fsanitize-trap=null`, which traps a null member access or reference bind with no runtime library (`h5-sole-and-counted`). [cpp L5 perf]
728. [Could] Python `code` option `"pytestGrade": { "module": "costs", "versions": { ... } }` providing `trial`, `names` and `weak` (tests that never fail on a broken version), replacing about 130 lines of prelude and postlude per item (`h-average-cost-tests`). [pytest L1 perf]
729. [Could] `code` widget: an optional record of the first Run examples result after the tests appear (red or green), readable by a hidden case, so a test-first task can see a red run (`h3-fee-test-first`). [pytest L3 perf]
730. [Could] AUTHORING notes: section 3 gives Pyodide's recursion limit and deepest safe recursion; Python 3.12 `sum` of floats is compensated (ten 0.1s give 1.0, a running total does not); section 5 says a `code` task grades behaviour, so "bottom up" in an objective is taught, not tested (`h-fee-trades`). [graphs-dp L1 and L3 perf, random-vars L1 perf]
731. [Could] Richer `byKey`: a key on the returned value (`test-1:None`, `test-1:TypeError`), a key for an exception raised outside the `call` in script mode, a match on error text, and an entry that lists several messages each with a hidden `when` call. Related to 681. [graphs-dp L2 perf, first-python L2 and L3 perf, plotting L2 perf]
732. [Could] `compare: "raises"` with an optional `match` regex read against the exception message, so a test can require the learner's own refusal rather than NumPy's shape `ValueError` (`h-factor-neutral`). [least-squares L2 perf]
733. [Could] `fresh-check.mjs` code names: skip a helper nested inside the solution's function (`profit` in `strategy_card`), and names the item's own prelude or starter defines (`to_list` in `h4-save-tree`); or say in AUTHORING section 5 that nested helpers count. Third sighting of 655. [options L2 perf, ds L4 perf]
734. [Could] A shared, importable Python harness (`tools/py_grade.py`, one `grade(source, tests)` function) that `code.js` builds its harness text from and numbers scripts import, so each script stops copying `__zq_cmp` by hand (element-wise `math.isclose` at rel 1e-9 and abs 1e-12, `raises` by the exception's MRO, the 700 NaN, DataFrame and dict rules). `docs/reviews/perf-retrofit-6-scripts/harness.py` predates 700; CPython's `np.linalg.solve` raises where Pyodide's returns nan. [numpy-pandas L2 perf, regression L2 perf, trees L2 perf]
735. [Could] Package-bump watch: a census line listing the Python perf items to recheck when Pyodide's pandas or NumPy moves (`h-fills-report` slips rely on pandas 2.2.3), and the session venv for numbers scripts pinned to NumPy 2.0.2 (it has 2.5.4 against Pyodide 0.27.7's 2.0.2), or a census line naming the mismatch. [numpy-pandas L2 perf, plotting L3 perf]
736. [Could] A `warnings` list (category names caught per case) readable from a test `call`, since `quietLib` drops FutureWarning lines and shows SettingWithCopyWarning as plain output (`h-trend-shares`). [numpy-pandas L3 perf]
737. [Should] `code` widget: render the returned Figure or Axes (one PNG under the results) on Run examples and Check, so a learner sees the chart they drew (`h-wealth-peak` is a gating chart task). [plotting L2 perf]
738. [Could] Shared test helper reading the dpi and pixel size of a saved PNG (the pHYs chunk), for the plotting and backtest courses. [plotting L3 perf]
739. [Could] AUTHORING section 5 verb table: "build: `code` where it runs, else `derivation` where the product is written maths", as for design and explain (limits L4, measure-prob L2). [limits L4 perf]
740. [Could] Warning for a starter or solution line wider than the 440 px editor (about 46 characters), which scrolls sideways unflagged. [random-vars L1 perf]
741. [Could] `code` widget `language: "text"`: the editor holds the file as typed, Python never runs it, and prelude, postlude and tests read it as `__learner_source__` (`git/homework-3` `h-ignore-options-repo` would drop its `GITIGNORE = """` wrapper). [git L3 perf]
742. [Could] `tree` canvas: column widths sized to the widest pill in each column, or an overlap warning, since a long leaf name hides its parent pill at 1280 and 440 px (terminal `h-perf-fx-paths`). [terminal L1 perf]
743. [Could] A `shell` widget over a small virtual tree that runs `cd`, `ls`, `mkdir`, `cp`, `mv`, `python3 <file>` and grades the final state and output, since the terminal course can only grade command sequences as text. [terminal L3 perf]
744. [Could] A stdout case graded by `match` shows an empty "Expected output" box on failure; say "Expected the output to match" and show the pattern in words (`h-perf-trade-script`). [terminal L3 perf]
745. [Could] An advisory per-case note on the result row that does not fail the case ("your code read 200,000 slots; a binary search reads about 18"), from a shared read-counting helper (algo-think l9 wraps lists in its own prelude). [algo-think L3 perf]

Status block (session Y inbox numbering, 9 Nov):
- New items: 705 to 745 (41), all open, none implemented.
- Sightings of items already numbered, not renumbered: 700 (opt-dash L3, validation L2, fin-ml L2), 701 (puzzles L4, measure-prob L3, ito L3, contests L3, limits-thm L3, pdes L1, options L3), 703 (linear-maps L3, micro L3, taylor L1, conditional L2), 697 (backtest L4, folded into 718).
- 80 inbox bullets read (every bullet added after the session X triage); each is marked "numbered n" in `docs/BACKLOG-INBOX.md`.

746. Done [Should] (docs/briefs/engine-gen.md, Agent 1 item 2) In-app hours shown apart from outside-study hours. `ZQ.hours` (`app/js/hours.js`) gains in-app and outside figures per lesson, level, course, topic, stage and role: in-app is authored lesson minutes plus each level's review (20 min) and homework (45 min) unless the file states minutes, plus the topic exam's minutes shared by lesson weight; outside is stored less in-app, floored at 0. Learn's header, stage pills and exit card, topic headings and Paths view, the course page, Setup's stage rows, `docs/readiness.md` and `docs/curriculum.md` show both, in-app first; none shows the stored total alone.
746 status: done. Files: `app/js/hours.js` (build inputs `setMinutes`, `examMinutes`; `splitLabel`, `fmtH`), `app/js/content.js` (stage and topic `hoursApp`, `hoursOut`), `app/js/screens/{learn,course,setup}.js`, `app/css/screens/course.css`, `app/tools/{hours-source,readiness-sums,curriculum-hours,validate}.mjs` (manifest `lessonMinutes`, `setMinutes`), `content/readiness.json` (`hoursInApp`, `hoursOutside`, written by `readiness-sums.mjs --write`), `docs/AUTHORING.md` section 14. Test `tools/test-hours-split.mjs` (209 checks). Allowances are the brief's "fixed allowance per set"; the 20 and 45 are this pass's choice and live in `hours.js`.
747. Done [Should] (user decision 9 Nov, `docs/reports/review-size-audit.md` route 1) A test-out draws 5 review items and passes at 4 of 5 (0.8), so a review of 10 items gives two papers with no repeated item (8 items repeat exactly 2).
747 status: done. Files: `app/js/prereq.js` (`TESTOUT_N = 5`), `app/js/screens/review.js` (comment number only), `app/tools/test-met-rule.mjs` (new test 747 runs the real draw expression from `review.js`; rule 2 test now 4 of 5), `app/tools/playthrough.mjs` (fixture counts), `docs/AUTHORING.md` section 11 ("5 items, pass at 4"; "10 or more"). Stored state is untouched: a test-out passed under the old rule stays passed. The pass count is derived (`ceil(5 x 0.8) = 4`), and no learner-facing text states a count. Report `docs/reports/engine-747.md`.

## Engine pass G and C (`docs/reports/engine-gen-2.md`), items 800 to 829 (brief `docs/briefs/engine-gen.md`)

Generated fluency sets (G, 800 to 819): 20 fresh typed-answer items per procedural lesson, authored as JSON only; author side `docs/AUTHORING.md` section 16.

800. Done [Must] Content shape: `content/courses/<course>/fluency-<lesson>.json`, one set per lesson, found by file name (no `course.json` edit); fields `id`, `lesson`, `title`, `n`, `pass`, `minutes`, `families[]` (`id`, `weight`, `skill`, `vars`, `let`, `where`, `prompt`, `widget`, `wrong`, `solution`).
800 status: done. Schema in `tools/fluency-rules.mjs` (`checkSet`) and `js/engine/gen.js` (`checkFamily`).

801. Done [Must] Safe evaluator, no `eval` and no `Function` (`js/engine/gen.js`): `+ - * / ^ %`, comparisons, `and`/`or`/`not`, `gcd lcm abs min max floor ceil round(x, dp) sqrt comb fact sign`, exact rationals (BigInt) until a root or fractional power makes a float.
801 status: done. 261 unit cases in `tools/test-fluency.mjs` (operators, every function, 30 error cases including `constructor`, `__proto__`, `eval`).

802. Done [Must] Templates and formats in `prompt`, `widget`, `wrong`, `solution`: `{x}`, `{x:+}`, `{x:c}`, `{x:+c}`, `{x:()}`, `{x:frac}`, `{x:+frac}`, `{x:dpN}`, `{x:+dpN}`, `{poly(v; c2, c1, c0)}`, any expression before the colon; `{{` and `}}` are literal braces (LaTeX is written `\\frac{{{p}}}{{{q}}}`). `+frac` and `+dpN` are additions to the brief's list, each with a test.
802 status: done. Every format has unit cases; `poly` has 12.

803. Done [Must] Seeded drawing: `vars` `int` (with `step`), `pick`, `not`; `let` in order; `where` (redraw, 60 tries per question); one stream per question from `ZQ.arith.rng`; families round robin by weight (smooth weighted round robin); no two prompts equal in an attempt.
803 status: done. `ZQ.gen.generate(set, seed)`; the same seed gives the same attempt, in the browser and in node.

804. Done [Must] Content loader: `ZQ.content.fluencyList()`, `fluencyFor(course, lesson)`, `fluencySet(course, id)`; the manifest lists sets under `fluency`; a registered fixture (`_setFluency`, `_addFluency`) counts as a real set for the page load (the test hook; no content file).
804 status: done. `manifest.json` is unchanged while no set exists.

805. Done [Must] A generated item is shaped for `ZQ.player.runSet` (`ZQ.gen.playerItem`): `question`, `widget` (numeric or expression, graded by the existing widgets unchanged), `feedback.byKey` (the matched `wrong` line then the solution steps), `explain`.
805 status: done.

806. Done [Must] State `ZQ.state.fluency` (`result`, `get`, `list`): per set attempts, best score, last score, last pass date and per family right and wrong counts; `partial: true` (leaving part way) keeps only the family counts. No skill score, streak, XP, met rule or gate moves.
806 status: done. Checked by the playthrough (the save before and after an attempt is identical outside `fluency` and hours).

807. Done [Should] `ZQ.setPage` (the review set page) takes `back`, `backLabel`, `overview: false`, `againRoute` and a `verdict` line; `runSet`'s test hook gains `answerWrong()`.
807 status: done. Existing pages unchanged (defaults).

808. Done [Must] Route `#fluency/<course>/<set id>[/<seed>]` (`js/screens/fluency.js`): start card (pass mark, no list of questions), one item a screen, one try, no hints, result with score, pass or not, "Go again" (a new seed); 440 px.
808 status: done.

809. Done [Should] The result is recorded through `ZQ.state.fluency.result` and the time logged as review hours; leaving part way is not an attempt.
809 status: done.

810. Done [Must] Today lists a set under a "Practice" heading in the Due card, after the due work, until it is first passed and only when its lesson is done (newest lesson first, at most two rows).
810 status: done.

811. Done [Must] The lesson's card on the course page carries a Fluency row (status, Start or Go again); the lesson's end card offers the set.
811 status: done.

812. Done [Must] Validator: schema (file name, `id`, `lesson` on the course map, `n`, `pass`, `minutes`, family fields, widget kinds and fields, `wrong` shapes, static name and function checks, braces), voice rules and the 35-word gate on the text as drawn, fixtures checked on every run.
812 status: done. Rules in `tools/fluency-rules.mjs`; 30 scratch cases in `tools/test-validate-fluency.mjs`.

813. Done [Must] Validator sampling: every family at 200 seeds: every placeholder filled, the typed answer graded correct (numeric through the numeric grading; an expression by text, in full by 815), each `wrong` not correct, redraw rate at most 80%, at least 60 distinct prompts (warn below 60, error below 25).
813 status: done.

814. Done [Must] `tools/fluency-sample.mjs --set <course>/<set id> [--family id] [--seed s] [--n k] [--json] [--stats]` (also `fixture/<id>` and `--file`): prompts, answers, wrongs, solutions and variable values.
814 status: done.

815. Done [Must] `tools/test-fluency.mjs --local-cdn <pkgs>`: unit tests of the evaluator and every format; every family of every set at 50 seeds in the real browser grader (answer, accept forms and upToConstant correct; each `wrong` not; for a `form` family the prompt's own expression typed back fails).
815 status: done. 281 checks on the fixture.

816. Done [Must] `playthrough.mjs --fluency <course>/<set id>` (also `fixture/<id>`, repeatable): a failing attempt, same seed repeats, Go again draws new numbers, a passing attempt, the save, Today row appears and clears, the course row, the lesson's end card, a part-way leave, nothing else in the save moves, no overflow at any width; `--all` plays every set after the sets, and the fixtures.
816 status: done. Green at desktop and `--mobile`.

817. Done [Should] `census.mjs` prints "Fluency sets N (families M)".
817 status: done.

818. Done [Must] Fixture `app/tools/fixtures/fluency/fluency-l3-opening-brackets.json` (`"sample": true`, five families: numeric, expanded, factorised, upToConstant, fractions), never under `app/content/`.
818 status: done.

819. Done [Must] `docs/AUTHORING.md` section 16 (every `vars` kind, every `let` function, every format with an example, `where`, choosing `form`, running `fluency-sample.mjs`, what the validator samples, the recompute script, a checklist) and `app/README.md`.
819 status: done.

Cumulative weekly review (C, 820 to 829): a weekly mixed set drawn from every met level, due on Today, not opt-in, no gate.

820. Done [Must] State `ZQ.state.cumulative` (`status`, `postpone`, `record`, `seen`, `history`): due seven days after the last review was finished, the first seven days after the first level was met (`prereq.met`); postponing keeps it due; a review left part way is not a review (it keeps what was served); 100 history rows, 3000 seen uids; old saves load with an empty block.
820 status: done. Eight cases in `tools/test-cumulative.mjs` part B.

821. Done [Must] `ZQ.select.cumulative.build(model, { n, seed })`, the pure selection: tier 1 generated items from the Fluency families of met levels' lessons (weighted by wrong counts and age), tier 2 authored items never seen, tier 3 review items least recently seen; at most four from one course, relaxing only when too few courses are met; neighbours from different courses.
821 status: done. Eleven cases in part A (with and without Fluency families).

822. Done [Must] `ZQ.select.weeklyReview()` builds the model from the live save and content (met levels, fluency sets and their family counts, unseen bank items and unsat topic-exam items on met courses, the quiz and review items of the twelve least recently covered met levels) and resolves the items for `runSet`; no long-form or code item.
822 status: done. Part C on the real content.

823. Done [Must] `ZQ.select.weeklyFinish()` records the result: history row (date, score, per-level misses), authored misses to the redo queue (their own ids), family counts to the Fluency save (not an attempt), skill scores as a practice set does, seen uids; a generated miss only moves the family counts.
823 status: done.

824. Done [Must] Route `#weekly` (`js/screens/weekly.js`) on the shared set page: start card with "Not today", twenty items one try each, result with misses by level.
824 status: done. `ZQ.setPage` gains `later`.

825. Done [Must] Today's Due card lists "Weekly mixed review" when due (postponed today and overdue read differently), above the practice rows.
825 status: done.

826. Done [Should] The weekly review is never a gate: the met rule, lessons, reviews, exams and performance records are unchanged by it.
826 status: done. Checked in `test-cumulative.mjs` (before and after) and by the playthrough.

827. Done [Must] `tools/test-cumulative.mjs`: selection rules on seeded states, with and without Fluency sets, the schedule, the recording.
827 status: done. 25 cases.

828. Done [Must] Playthrough routes block (`cumulativeChecks`): nothing due on the first day, the state clock eight days on, the card appears above the practice rows, "Not today" keeps it due, the review is played (20 items) and recorded, the card clears, due again after seven days; no overflow at any width.
828 status: done. Desktop and `--mobile`.

829. Done [Must] `docs/AUTHORING.md` section 16 "The weekly mixed review" and the report `docs/reports/engine-gen-2.md`.
829 status: done.

Raised later (fluency quadratics), the answer forms of a typed expression and numeric answer:

830. Done [Should] `expression` `"form": "factorised-fully"`: as `factorised`, and no bracketed factor may still hold a common whole-number factor or a quadratic that factorises over the integers, so `(2x+4)(x+3)` fails for `2(x+2)(x+3)` and `(x^2-4)(x+1)` fails for `(x-2)(x+2)(x+1)`. An equal answer not fully factorised returns the key `form`, default line "Factorise fully: a bracket still has a common factor."
830 status: done. `ZQ.grade.shapeFullyFactorised`; a quadratic factorises when its discriminant is a perfect square (rational roots, so `4x^2-9` and `x^2+3x` fail as well as integer roots). Cases in `tools/test-answer-forms.mjs` part 1.

831. Done [Should] `expression` `"form": "completed-square"`: `a(x+p)^2+q` with a, p, q numbers or fractions (a may be 1 or negative), either order of the two terms, the number q may be left out; refuses the expanded form and any other equal shape. Default `form` line "Write it as a bracket squared plus a number."
831 status: done. `ZQ.grade.shapeCompletedSquare`; the x inside the bracket has coefficient 1 and p must not be 0. Cases in `tools/test-answer-forms.mjs` part 2.

832. Done [Should] A set answer for `expression` and `numeric`: `"answers": [...]` with `"unordered": true`, typed with commas (`2, -5`, `x = 2, x = -5`, `x = 2 or x = -5`, `{2, -5}`), a missing or extra value returns the key `count` with the line "This question needs 2 values, separated by commas. You gave 1."; `\pm` (and `±`, `+-` in a numeric field) in the input stands for both values; the maths keyboard of such an item has a comma and `\pm` and a numeric one opens the text phone keyboard.
832 status: done. `ZQ.grade.exprSetGrade`, `numSetGrade`; wrong sets are comma-separated lists (`tex` or `value`); in exams the model answer shows the set.

833. Done [Should] Fluency `vars`: a pick of tuples, `{ "pick": [[1, 6], [2, 3]], "as": ["r", "s"] }`, sets several names from one draw (numbers or text), so no `where` is needed to tie them.
833 status: done. `gen.js` `checkFamily` and `draw`; section 16 documents it.

834. Done [Must] Validator schema for the new fields and forms (`answers`, `unordered`, `count`, the two forms), `fluency-rules.mjs` and `fluency-sample.mjs` read set answers, `tools/test-fluency.mjs` grades set answers and both forms in the real widgets (the prompt's own expression typed back must fail), `tools/test-answer-forms.mjs`, five new fixture families, `docs/AUTHORING.md` (the `expression` and `numeric` sections, section 16) and the report `docs/reports/engine-830.md`.
834 status: done. They work in lessons, reviews, homework and exams as well as Fluency.

Raised later (the first Fluency content wave), engine pass 835 onward:

835. Done [Must] `tools/test-cumulative.mjs` failed 5 of 25 once real Fluency sets existed: the weekly review's per-course cap with several sets in one course must hold, and the tests must not depend on which real sets exist.
835 status: done. The cap in `select.js` was not broken (the test that draws from real content already held it at four per course); the fixtures wrongly read the real sets. Part C now reads the real sets once, starts every case with none and registers the fixture itself; one new case puts every real set in force and checks no course gives more than four. 26 of 26.

836. Done [Must] Plain-text `ln`, `log`, `exp`, `sin`, `cos`, `tan`, `sqrt` before `(` in `answer`, `accept` and learner input are the functions, not a product of letters (`ln(97)/ln(4)` equalled `97/4`).
836 status: done. `plainFns` in `grade.js`, first step of `prep`; a name behind a backslash, inside a longer word (`arcsin(`, `sinh(`) or without a bracket is untouched. `tools/audit-plain-functions.mjs` lists every such entry in `app/content` and what the fix did to it (115 entries; the list is in `docs/reports/engine-835.md`). Cases in `tools/test-expr-equations.mjs` part 1.

837. Done [Should] A Fluency answer the grader returns with key `length`, `form` or `count` shows that key's line and then the `solution` steps, as any other wrong answer does.
837 status: done. `notYetLine` in `player.js` for a generated item.

838. Done [Should] Fluency `let` and `where`: functions `ln`, `log10`, `exp`, `sin`, `cos`, `tan` (radians), the constant `pi` and `if(cond, a, b)`; a `where` that uses only vars is tested before any `let` is worked out; a `let` that divides by zero rejects the draw instead of raising an error.
838 status: done. `gen.js` (`FUNCS`, `CONSTS`, lazy `if`, `splitWhere`, the let catch). `pi`, the new function names and `if` are reserved, and no existing set used them as names. Existing sets draw the same items (the random stream and which draws are accepted are unchanged). `tools/test-fluency-reach.mjs`; fixture families `log-significant`, `height-with-sine`, `divide-reject`; AUTHORING section 16 (functions table, where). Deferred: `log(x, b)`, `asin`, `acos`, `atan`, `e`, and a degree form of the trigonometric functions.

839. Done [Should] A `wrong` entry may carry `"when": "<condition>"`: the slip is offered only on draws where it holds, and the validator's "wrong equals answer" check respects it.
839 status: done. `gen.js` `draw` and `checkFamily` (the validator, `fluency-sample.mjs` and `test-fluency.mjs` read the drawn list, so they follow). Unit cases in `tools/test-fluency-reach.mjs`; fixture families `mono-derivative`, `height-with-sine`, `divide-reject`, `exact-angle`, `fractional-coefficient`.

840. Done [Should] Fluency formats: `{mono(v; c, k)}`, power 1 never written by `poly` or `mono`, `cfrac` and `+cfrac`, `(frac)`, `sfN` and `+sfN`, and `{falling(n; r)}`; the surd text var of `poly` documented.
840 status: done. `gen.js` (`monoText`, `fallingText`, `sigFig`, the `SPEC` pattern). `poly` already wrote no power of 1, so only `mono` is new there. `dp` above 10 and `sf` outside 1 to 10 are now static errors as well as draw errors. Not done: a numeric `tol` stated in units of the last figure (authors give `abs` half a unit, as in section 16).

841. Done [Should] `expression` `"form": "fraction"` (whole number or one fraction in lowest terms; a decimal or an unreduced fraction returns key `form`) and `"form": "exact-angle"` (a multiple of pi in lowest terms; refuses degree signs, decimals and an unreduced multiple); `simplified` is unchanged.
841 status: done. `ZQ.grade.shapeFraction` and `shapeExactAngle` read the typed text (the engine's canonical form reduces `\frac{14}{18}`), called from the expression widget `formOk`, `exprFormOk`, the validator's form list and `gen.js`. Default lines for both. `tools/test-answer-forms.mjs` part 4b and the widget cases; fixture families `fraction-lowest`, `exact-angle`.
842. Done [Should] A Fluency set's saved record is keyed by course and set id, so two courses holding one set id never share a record; the weekly review's family counts use the same key.
842 status: done, and no code fault found. `ZQ.state.fluency` has always keyed `<course>/<set id>` (state.js `fluencyKey`), and the weekly review reads and writes the same key through `fluency.get` and `fluency.result`, so no migration and no legacy key exist. The shared record seen in the sharded run was the playthrough fixture `fixture/fluency-l3-opening-brackets`, which declares `"course": "equations"` and the same id as the real set, so the two sets truly are one key; that is a tool fault. The playthrough now clears the set's record before each set is played. `tools/test-fluency.mjs` checks two courses with one set id keep separate records.
843. Done [Should] Today's Practice list shows at most two Fluency rows (the most recently finished lessons first) and one "More Fluency sets" row to a full list at `#fluency-list`; the playthrough reads the full list; `--fluency-all` plays every set in one profile.
843 status: done. Cause: Today has always capped the rows at two (`flu.slice(0, 2)`) with a caption and no link, so from the third finished lesson in one profile the set under test fell outside the rows, and the playthrough probe read only those rows. The cap is right for the learner, so the product fault was only that the overflow had no way in: the caption is now a row leading to `#fluency-list` (fluency.js, every set by course with lesson done or not and passed or not). The tool fault was the probe: it now accepts a Today row or an open item in the full list. AUTHORING section 16 states the rule. Report `docs/reports/engine-842.md`.

844. Done [Should] Planted-wrong-solution check as a tool (KNOWN_ISSUES "Protocol 6 watch"; reviews `review-drills-dsa-a-b`, `review-drills-dsa-c-d`): a drill may carry `planted`, an array of `{ "code", "slip" }` wrong solutions; `node tools/planted-check.mjs --drill <id> | --all-drills [--require] [--local-cdn <pkgs>]` runs the model solution, the starter and each planted solution against the hidden tests in Pyodide or the C++ toolchain, and fails when the model fails or any wrong solution passes every test.
844 status: done. The runner is `playthrough.mjs --drill <id> --planted` (new `plantedOne`, using the same `drillReady`, `drillSubmit` and hooks as `--drill`); `planted-check.mjs` picks the drills, reads the `PLANTED-FAIL` and `PLANTED-OK` lines and adds `--require`. Validator checks the shape only. Test `tools/test-planted-check.mjs` with fixtures in `tools/fixtures/planted/`. No existing drill holds wrong solutions under another name, and no content was edited.

## Problem sets

Raised by the chained-problems decision (DECISIONS "Chained problems", session Z; PLAN 2d item M; brief `docs/briefs/chained.md`). A per-level content kind, `problems-<n>.json`, for chained problems. Items 845 to 851; report `docs/reports/engine-problems.md`.

845. Done [Must] The file kind `problems-<n>.json` and its validator rules: `{ id, course, level, items: [3 to 5], title?, minutes? }`, every item with 3 to 5 `parts` and no `longform` or `code` part, difficulty 3 to 5 with at least one 5, `skills` from the level's own lessons, no `timed`, `pass` or `dueDays`; every review item rule applies; a level without a file is not an error; the manifest lists each set under `problems`.
845 status: done. `checkProblemSet` in `tools/validate.mjs` (called from `checkSet` with kind `problems`; found by file name, like Fluency sets) and the fixture check; `tools/test-validate-problems.mjs` (33 scratch cases).

846. Done [Must] Loader, route and set page: `ZQ.content.problemsFor`, `problemsList`, `problems`, `_addProblems` (test hook); route `#problems/<course>/problems-<n>` on the shared set page; untimed, repeatable ("Go again"), not a gate; each part graded with its own feedback, item credit as the `parts` rules say.
846 status: done. `mountProblemSet` in `js/screens/review.js` (no new player); `ZQ.state.problems.finished` saves attempts, best (in items, part credit counted) and last score; it locks and unlocks with its level (`levelHolding` in `js/prereq.js` knows `problems-<n>`).

847. Done [Must] Listing: the level review's card on the course map carries a "Problem set" row with a button, and the review's result page links to it.
847 status: done. `problemsRow` in `js/screens/course.js`; the row is hidden while the level is locked.

848. Done [Should] XP on the homework scale: 50 and 5 an item right, and mastery points, on the first finished attempt only; no redo queue; a left set records its time and nothing else.
848 status: done. `problemsFinished` in `js/state.js`. Nothing else moves (reviews, homework, met levels, redo queue, performance record); `tools/test-problems.mjs` and the playthrough check it.

849. Done [Must] Weekly cumulative review: the items of the problem sets of met levels join the unseen authored pool (tier 2); an item with parts plays correctly there, a miss queues under the set's own ref and the redo session resolves it with its parts.
849 status: done, and no fault found in the player: an item with parts already played in the weekly review as in a level review (`practiceKind` leaves out a code or long-form part). Changes: `cumModel`, `loadSet`, `source`, `levelOf` and `resolve` in `js/engine/select.js`. Tested in the real player (`tools/test-problems.mjs` part B).

850. Done [Must] Hours: the in-app minutes count the set (stated `minutes`, else 40); the stored topic hours and the census "hours 3,695, gap 0" figure do not change.
850 status: done. `problemsMinutes` in `js/hours.js` `build` (read from `manifest.problems` by `js/content.js`, from the files by `tools/hours-source.mjs`); with no problem file in the content every figure is unchanged. When sets arrive, in-app hours rise and outside hours fall by the same minutes, per level, course, topic and stage; stored hours stay as they are (`tools/test-hours-split.mjs` still holds, and `tools/test-problems.mjs` checks the stored figures).

851. Done [Must] Tools: `node tools/playthrough.mjs --problems <course>/problems-<n>` (also `fixture/<file>` and `--problems all`, inside `--all`, with `--mobile` and `--local-cdn`); `tools/census.mjs` prints "Problem sets n (items m)"; `tools/test-problems.mjs`; the fixture set in `tools/fixtures/problems/`; AUTHORING section 5 and 7, `app/README.md`.
851 status: done. The playthrough checks the course row, a wrong part (its own feedback, part credit, the summary line), the XP rule, a repeat, no gate, and no overflow at the phone width.

Raised later (engine session Z, from the inbox):

852. Done [Must] Mobile overflow: the topic pill on a course page ("1.11 Complex numbers, vector calculus and differential equations") did not wrap, so `complex`, `odes` and `vector-calc` pages were wider than 440 px and `--fluency ... --mobile` failed its course-row check.
852 status: done. `css/screens/course.css`: `.zc-course-body .chip.track` wraps (`white-space: normal`, `height: auto`, `max-width: 100%`, `overflow-wrap: anywhere`). The three 1.11 courses and `vectors` pass `--fluency --mobile`.

853. Not reproduced [Should] Flake: `--fluency` "the same seed drew different questions".
853 status: not reproduced in 2 x 30 repeated same-seed plays (`vectors/fluency-l3-lengths-angles`, `vector-calc/fluency-l5-divergence-and-curl`, alternating a failing and a clean attempt). Ruled out: generation (`ZQ.gen` has no clock or `Math.random`, deterministic by seed, `fluency.js` takes the seed from the route), widget kinds (only numeric and expression, so no option shuffle), KaTeX (a synchronous script, `tex()` cannot fall back to `<code>` after load), the item render (`show` is synchronous). Left: a load-dependent read of `innerText` in the check; no code change.

854. Done [Should] `merge-wave.sh`: a conflict in the generated `app/content/manifest.json` now takes ours and the validator step regenerates it (it no longer ends as UNRESOLVED).
854 status: done. `tools/test-merge-wave.sh` adds a new drill file on each branch, so the two regenerated manifests collide; the old script failed the case, the new one passes.

855. Done [Should] `numbers_lib.py`: `Level` loads `problems-<n>.json` (ref `"problems"`); `check_wrongs` prints a count of "check by hand" lines, the lines with `verbose=True` or `--verbose`.
855 status: done. `tools/test-numbers-lib.py` extended (count versus verbose, a problem set read and checked).

856. Done [Should] Problem sets: the done page note on a clean run reads "Every problem was right first time." (not "Well done."); the result page labels each problem "Problem n." and the first sentence of its prose, cut at about 60 characters (`rowLabel` in `mountProblemSet`, `js/screens/review.js`).
856 status: done. `Well done.` remains in `js/screens/fluency.js` (a passed Fluency set); not in this item.

857. Done [Could] Validator `[answer-form]` warning: a `numeric` problem-set part with a non-integer answer whose question lacks "decimal place", "significant figure", "fraction", "nearest", "per cent" or "%".
857 status: done. `checkProblemSet` in `tools/validate.mjs`; two cases in `tools/test-validate-problems.mjs`.

858. Done [Should] `playthrough.mjs --problems ... --shots`: every part of every problem is shot at 440 px (`<set>-i<item>-p<part>-440.png`), in the first attempt.
858 status: done.

859. Done [Should] Validator: a row of `drills/index.json` that disagrees with its drill file on `name`, `course` or `difficulty` is an error; a non-sample drill file with no row is now an error (was a warning); a row with no file was already an error.
859 status: done. Real content already clean (155 rows, 162 files, 7 sample files unlisted). `tools/test-validate-drill-index.mjs` (8 cases).

860. Done [Could] Validator `[answer-form]` widened (`ANSWER_FORM` in `tools/validate.mjs`): "decimal", "place(s)", "dp", "sf", "fraction", "nearest", "per cent", "percentage", "%", "exact value/answer/result/figure", "in pounds/pence/£/basis points", "ratio". Phrases listed in `docs/AUTHORING.md` section 5.
860 status: done. 137 warnings over the 1.5 sets fall to 1. Six pass cases and one "exactly alone still warns" case in `tools/test-validate-problems.mjs`.


Raised later (engine pass AA 1, numbered from the inbox "Raised later (fluency trig, widening pass)" onward; bullets already covered by 844, 852, 853, 855 to 860 are not repeated):

861. Done [Should] Drill page compares results as the code widget does (NaN equal to NaN, dicts by key, text, bool, pandas Series, float tolerance): one shared comparison. [inbox: drills py a, drills py b]
861 status: done. `JUDGE` in `js/engine/widgets/code.js` gains `__zq_judge(actual, expected, compare, tol)` (the code widget's `__zq_cmp` calls it) and is exported as `ZQ.widgets.codeJudge`; `js/screens/drill.js` dropped `__zq_eq` and uses it, with per-test `tol`. Fixed in passing: the harness case table is now loaded with `json.loads` (a `null` tol is not Python). `tools/test-drill-page.mjs` (15 judge cases in real Python, plus a played fixture).
862. Done [Should] Drill page runs a test's `setup` and `"compare": "raises"`, which the validator accepts. [inbox: drills py a]
862 status: done. The drill harness runs `setup` (and reads its imports with `importHint`) and the `raises` mode (named exception or a subclass; result row reads `raised <Name>` or `no error, the value was ...`); `RULES.raises` gives the Accepted line. Played by `tools/fixtures/drill-page/drill-aa-page.json`, desktop and `--mobile`.
863. Done [Could] Lists (`- item`) and single line breaks in a drill `brief` render. [inbox: drills ci 1, drills cpp]
863 status: done. `block()` in `js/screens/drill-lib.js` renders `- `, `* ` and `1. ` lists (continuation lines join the item); `drill.js` uses it, so both Python and C++ pages share it. `.drl-list` in `css/screens/drill.css`. Unit cases in `tools/test-drill-page.mjs`.
864. Done [Should] A long inline code span in a drill brief wraps at 440 px, and `playthrough.mjs --mobile` fails on horizontal overflow of the drill page. [inbox: drills cpp]
864 status: done. A code span over 24 characters wraps on the C++ page too (the Python page already did); `playthrough.mjs --drill` at 440 px and the other widths fails with "the brief runs past the right edge" when a brief element ends past the clipping column (`briefClipped`). Case: a fixture with an unbreakable formula fails `--mobile` and passes desktop.
865. Done [Should] `allocCheck` passed from a C++ drill to the code widget (`drill-lib.js`). [inbox: drills cpp]
865 status: done. `allocCheck` added to the pass-through list in `js/screens/drill-lib.js`; checked by a source test (no C++ drill uses it yet).
866. Done [Should] `constraints` for a drill's inputs, machine-readable, and a validator check that every example and hidden test satisfies them (error), with a `[no-constraints]` warning for a drill without. [KNOWN_ISSUES session Z protocol 6; reviews drills-py, ci]
866 status: done. `tools/drill-constraints.mjs` (Python-literal call reader, constraint objects, one shared reader); `validate.mjs` errors on a test or example that breaks a stated constraint or a malformed object, warns `[no-constraints]` on a non-sample drill with none. Existing `constraints` strings are untouched and objects are not shown on the page. 210 of 210 existing drills carry the warning; shipped content stays at 0 errors. `docs/AUTHORING.md` section 5; `tools/test-drill-constraints.mjs` (36 checks).
867. Done [Could] AUTHORING states that a drill's `prelude` runs after the learner's code (a code widget's runs before). [inbox: drills py b]
867 status: done. Stated in `docs/AUTHORING.md` section 5 (with the rest of what the drill page runs).
868. [Could] Drill page "Accepted:" line names one rule for the whole drill; a per-test rule on each result row. [inbox: drills py a]
869. [Could] `playthrough.mjs --drill` and `planted-check.mjs` say "drill missing from content/manifest.json, run validate.mjs" instead of a 20 s timeout. [inbox: drills py b]
870. [Could] `planted-check.mjs` and `--drill --why` name the failing hidden test and its actual value. [inbox: drills py b]
871. [Could] `planted` cannot state "too slow" as the slip. [inbox: drills ci 4]
872. [Could] A drill-level hidden helper usable from `tests` but not from the learner's code. [inbox: drills ci 4]
873. [Could] Validator `pace` over 30 minutes warning: raise the threshold for drills (900 to 2,700 s allowed by the ci brief). [inbox: drills ci 1, ci 2, ci 3]
874. [Could] `voice-scan.py` skips `planted[].code` (and `slip` if not learner-facing). [inbox: drills ci 3]
875. [Could] Fluency `poly` with a surd var writes a non-whole coefficient as `\frac{7}{2}`; `mono` writes one term only. [inbox: fluency trig]
876. [Could] `form: "simplified"` applied to each value of an `answers` set. [inbox: fluency quadratics]
877. [Could] A power placeholder for any base (`{pow(k)}` writes nothing for 1); `mono` with a bracketed base. [inbox: fluency limits integrals multivar]
878. [Could] Decision wanted: the four-family cap for Fluency sets (`integrals/fluency-l9`, `l10`). [inbox: fluency limits integrals multivar]
879. [Should] `form: "standard"` for standard form (refuses `0.00042` and `42 \times 10^{-5}`). [inbox: fluency number-sense]
880. [Should] `form: "ratio"` for a ratio in simplest form (`5 : 2`, refuses `10 : 4`). [inbox: fluency ratio]
881. [Could] Thousands separator format in Fluency templates (`{x:dp2}` to `1,271.00`). [inbox: fluency ratio]
882. [Could] Fluency `numeric` widget refuses `over100`; list the two field sets in AUTHORING. [inbox: fluency ratio]
883. [Should] A whole matrix as a typed Fluency answer (keyboard, and how `[[a, b], [c, d]]` is read). [inbox: fluency vectors elimination eigen least-squares]
884. [Could] Maths keyboard of an `expression` item offers $\lambda$. [inbox: fluency vectors elimination eigen least-squares]
885. [Could] A reduced fraction written only when it differs from the working fraction (`{a/b:=frac}` or a text `if`). [inbox: fluency conditional]
886. [Could] `phi(x)` and its inverse in Fluency `let`. [inbox: fluency limits-thm]
887. [Could] A Fluency `int` bound that is an expression of an earlier var. [inbox: fluency testing]
888. [Should] `form: "rectangular"` accepts a whole number times a surd times $i$ (`9\sqrt{3}i`). [inbox: fluency complex odes vector-calc]
889. [Could] `atan` and `atan2` in Fluency `let`. [inbox: fluency complex odes vector-calc]
890. [Should] `--problems ... --shots` at 440 px shoots the "Problem set" row with the review card open and scrolled into view. [inbox: drills ci 4 levels 4 and 5, problems random-vars]
891. [Could] A `numeric` part with `tol`, no `accept` and `unit: "£"` prints "£45.00, to the penny". [inbox: problems random-vars]
892. [Could] `fresh-check.mjs` triage: required form sentences in `STOPLIST` or problem sets compared only with non-problem files. [inbox: problems markov (twice), markov levels 4 and 5, taylor, functions; also the `fresh-check` triage of series]
893. Done [Could] `fresh-check.mjs --file` on a problems set: advisory when an item shares a displayed formula or two stated parameters with a lesson, quiz, review or homework item of its course. [inbox: review problems 1.3 b]
893 status: done. `fresh-check.mjs --file` on a problem set lists, as advisory, a shared displayed formula or two shared specific parameters with a lesson, quiz, review, homework, other set or exam of its course. It finds 4 of the 10 pre-fix reuses the readers found (falling parabola, relative strength, cube root, path and pipe; the rest are by story). 92 advisory lines on the 62 current sets, no hard hit. `tools/test-fresh-check.mjs`.
894. Done [Should] Validator: the number printed after the last `=` or `\approx` in `feedback.correct` lies inside `answer ± tol` (allow parts in units of $10^{-k}$). [inbox: problems limits-thm, problems taylor]
894 status: done. validator `[tight-band]`: the figure `feedback.correct` or `explain.text` prints after its last `=` or `\approx` (within 2% of the answer, outside the band). 77 warnings on current content. `tools/test-validate-band-rules.mjs`.
895. [Could] `[wrong-band]` reads "to n places", prefers the last rounding phrase, skips `unscaled` slips, and respects units. [inbox: problems limits-thm, review problems 1.3 b; KNOWN_ISSUES session AA]
896. [Could] `numbers_lib.py` part checker (form sentence, rounding inside tolerance, printed value) and `check_wrongs` evaluating simple LaTeX in `byKey` lines. [inbox: problems limits-thm level 4, problems counting-chance]
897. [Could] Prose renderer binds a leading `+` or `-` to the following `£` and digits (no break at 440 px). [inbox: problems markov levels 4 and 5]
898. Done [Should] Expression grader: a per-symbol sampling range or domain (`s < 0.5`, `\arcsin x`), both parts of a complex value, and no refusal of a correct form with a tiny term (`\frac{400}{e^{8u}}` for `400e^{-8u}`). [inbox: problems fix pass d, problems integrals, delta session AA, review problems 1.3 c]
898 status: done. real mode now evaluates in the complex numbers (both parts compared: `\sqrt{x-5}` is not `3\sqrt{x-5}`), exact for tiny terms (`\frac{400}{e^{8u}}` equals `400e^{-8u}`, the 1.3 c barbell row), an imaginary side against an undefined one is a skipped point, and `"domain": { "s": [lo, hi] }` gives a symbol its sampling range. Side effect found by `tools/grade-regression.mjs`: ten authored `wrong` entries "0" (vector-calc, answer `2\pi`) used to grade correct and now route to their keys. Tests in `tools/test-expr-equations.mjs` Part 1b.
899. [Should] The `trade` widget takes a one-sided quote. [inbox: audit mm-games]
900. [Could] Validator warns on learner text citing a lesson or homework by number. [inbox: audit mm-games]
901. [Could] Set page: the feedback heading "Not quite right." and a `generic` line beginning "Not quite." read twice. [inbox: problems integrals]
902. Done [Should] `form: "simplified"` refuses some simplest forms (`-\frac{2r}{3}+\frac{s}{3}`, terms over 2) and passes unopened vector or bracketed forms (`3+2.5(t-2)`, `r+\frac{1}{2}(s-r)`). [inbox: review problems 0.2 b, review problems 0.3 a, problems equations, problems functions, problems counting]
902 status: done. `form: "simplified"` collects like terms, refuses an open bracket in a sum and a decimal or fraction a/b before a bracket, and passes a collected single fraction in lowest terms (`simplestVerdict`). The cases of the 0.2 b, 0.3 a readers and the three in the item pass or fail as wanted; `0.2(25n-500)` is refused, `5(n-20)` still passes (an authored accept). `\frac{1}{2}(r+s)` cannot be told from `\frac{r+s}{2}` and passes. `tools/test-answer-forms.mjs` Part 3b.
903. [Could] `expanded` and `factorised-fully` refuse uncollected like terms (`x^2+3x+8x+24`). [inbox: problems quadratics, review problems 0.2 b]
904. Done [Should] A typed left side (`y=`, `A=`, `m(e(x))=`, `f^{-1}(x)=`) is dropped before the shape checks and for nested or inverse names. [inbox: review problems 0.2 b, review problems 0.3 a]
904 status: done. the typed left side is dropped before every shape check (`dropLabel`) and a call whose head letters are not symbols of the answer, with anything in its brackets, is a label (`m(e(x))`, `B(T(n))`, `f^{-1}(x)`, `f(-x)`, `gf(x)`; not `x(x+1)`). Rows of the 0.2 b and 0.3 a readers in `tools/test-expr-equations.mjs` Part 1b.
905. Done [Should] A "Solve" inequality part does not grade the retyped question as correct. [inbox: review problems 0.2 a; KNOWN_ISSUES session AA]
905 status: done. a "Solve" part whose answer is a relation with a lone letter on one side and a number on the other (`h \le 10`, `x = 4`) now needs the learner's line solved too: the retyped question and half-solved lines get the key `form` ("not solved"). Automatic, plus `"form": "solved"` for answers with other letters on the far side (`grade.js` `solvedShape`, `autoSolved`). 0 authored answers, accepts or wrongs change. `tools/test-expr-equations.mjs` Part 1b (the bakery, fridge and van rows of the 0.2 a reader).
906. Done [Could] A thousands comma inside an expression (`12,000-s`). [inbox: review problems 0.2 a]
906 status: done. a thousands comma inside an expression (`12,000-s`, `12{,}000`) is part of the number; `(2,100)` stays a pair. `tools/test-expr-equations.mjs` Part 1b.
907. Done [Could] `numeric` field: a trailing unit or degree sign, a letter and `=` before the value, and a scale for "units of $10^{-k}$". [inbox: review problems 0.3 a, problems equations, problems taylor]
907 status: done. the numeric field drops a letter and `=` before the value and a trailing unit or degree sign (`G.numText`), and `"scale": 1e-5` accepts the true value as well as the scaled one (`G.numGrade`); validator checks `scale`. `tools/test-answer-forms.mjs` Part 3b.
908. Done [Could] Expression parser: a plain-text power with a bracketed exponent (`80*0.9^(n-1)`), and a decimal times a bracket (`0.25(500)`). [inbox: problems series, review problems 0.2 b]
908 status: done. a bracket after `^` is the whole exponent (`80*0.9^(n-1)`), and a decimal before a bracket is a product (`0.25(500)`); `grade.js` `tidy`. `tools/test-expr-equations.mjs` Part 1b.
909. Done [Could] Validator advisories `[tight-band]` and `[wide-wrong-band]` (a band over half its own value). [inbox: review problems 1.3 a, 1.3 b, 1.3 c, review problems 0.2 a]
909 status: done. validator `[tight-band]` (the answer rounded as the question asks lies outside its band; an unrounded answer with a half-unit band: 2 and 70 warnings) and `[wide-wrong-band]` (37). "to k places" is now read as the rounding asked for these two rules. `tools/test-validate-band-rules.mjs`.
910. Done [Should] Validator: an expression `wrong[].tex` that grades equal to a single `answer`. [inbox: problems equations]
910 status: done. validator error `[wrong-equals-answer]`: an expression `wrong[].tex` that `exprGrade` reads as the answer or an accept form; by value with `--local-cdn <pkgs>`, by text without. 0 on current content, so an error. `tools/test-validate-band-rules.mjs`.
911. Done [Could] Validator: an `accept` string "Any form equal to" a value that is not a ratio of whole numbers. [inbox: review problems 1.3 c]
911 status: done. validator `[accept-form]` (warning): a numeric `accept` that says "any form equal to" a value the field cannot type. 6 on current content. `tools/test-validate-band-rules.mjs`.
912. [Could] Validator: a later part saying "Using part n" with no value after it, or using a symbol only an earlier part supplies. [inbox: review problems 0.2 a, review problems 0.3 a]
913. [Could] `answers` sets: `count` key cannot name the missing value; a value cannot be a pair. [inbox: problems functions, problems multivar]
914. [Could] The fixed feedback bar covers the last part's input at 440 px once checked. [inbox: problems exp-log, problems series]
915. [Could] Expression "Accepted:" line prints `accept` forms as raw LaTeX source; render as KaTeX. [inbox: delta session AA, problems exp-log, problems functions, problems series, problems integrals, problems counting]
916. [Could] Expression "Accepted:" line says "any expression equal to" when a `form` refuses equal forms (fraction, simplified). [inbox: fluency number-sense, problems equations]

Last inbox heading numbered: "Raised later (problems series)" (end of file at the time of numbering).

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
129. Deferred: a timed table set (countdown, live score, lock at zero) is a screen mode of its own, close to the Today warm-up; better designed with the mental arithmetic course than added to the table widget.
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
241. Deferred: a 3D projected view is a new canvas (camera, depth order, rotation by drag) rather than an option on `vectors`; worth designing with the linear algebra level that needs it.
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

Content note (trees): level 2 grows cash by (1 + r) per step and level 3 by e^{rΔt}; level 3 states this. The second reader for topic 1.7 should check that level 2 never implies its convention is the only one and that the level 3 limit £10.45 is consistent with the exam.

Content gaps (second reader, topic 1.3), to fill in a later gap pass once every course is written:

383. Calculus coverage against the MIT 18.01 and 18.02 exit lines: no improper integrals with an unbounded integrand (integrals l7 promises them), no partial fractions, trigonometric substitution or trig powers, inverse trig functions, related rates, volumes of revolution, arc length, hyperbolic functions; the mean value theorem is used but never taught; multivar has no triple integrals or Jacobian, and Lagrange only in two variables with one constraint. Candidate: an extra level in `integrals` (techniques) and one extra lesson each in `limits` (MVT, related rates) and `multivar` (Jacobian, Lagrange in three variables).

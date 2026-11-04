# Canvases B: plane, bars, distribution, scatter, series, walk, matrix, vectors, complex-map, graph, array, payoff, orderbook, space, interleave

Authors write `canvas: { "kind", "params", "state", "controls" }` (AUTHORING.md section 4). This file gives, per kind, the exact params, state keys, highlightable ids and the `change` events each one emits, with one JSON example each. It also covers the `slider` and `sketch` widgets.

## Rules shared by every kind

- **Params fix the drawing; state is what changes.** `state` is merged with `ZQ.canvas.merge` (objects merge, arrays replace) and animated over 480 to 800 ms (ease-morph) unless the change is instant or the learner has reduced motion on. Numbers tween, so positions, bar heights, slopes, parameters and curves morph. Discrete things (run counters, swaps, fills) have their own animations, described per kind.
- **`state.highlight: [ids]`** puts a pear wash and a 2 px ink ring on the named elements. Hint rung 2 calls `canvas.highlight(ids)`, which pulses twice; `highlight(null, false)` clears everything.
- **`state.caption: "text"`** shows under the drawing. It may contain `$...$` maths.
- **Labels.** A label string with no `$` is plain text. A label that is entirely `$...$` is KaTeX. Mixed text and maths (`"slope of $f$"`) also works.
- **Series colours.** Series take slots 1 to 6 in order. Set `colour: 1..6` on a series, function, vector or leg to pick a slot. Learner-movable things are always manipulable blue.
- **Linked state (`derive`).** Any canvas may carry `"derive": { "<target>": "<expression>" }` beside `params` and `state`. After every change (a patch, a drag, a control) each target is set from its expression: `"p2.x": "0.8 * p1.x"` (an item's property, by id), `"values.7": "10 - values['3']"` (bars), `"params.b": "2 * a"`, `"caption": "Change: {{round((p1.x / 50 - 1) * 100, 1)}}%"` (a string fills each `{{expression}}`). Expressions see item ids (`p1.x`), param names, top-level numbers (`angle`, `ran`) and `values` (bar heights by label and id). The function set: `abs min max sqrt pow floor ceil sign hypot`, `round(v, places)`, `exp`, `log` and `ln` (natural), `log10`, `sin cos tan asin acos atan atan2` (radians), the constants `pi` and `e`, and for text `fixed(v, places)` and `money(v, symbol, places)`. `=` and `;` may appear only inside quoted strings. Rules run up to three passes, so a caption may read a value another rule derives. `fixed(3.5, 2)` is "3.50"; `money(1234.5)` is "£1,234.50" (`money(v, "$")` for dollars); negative numbers, in captions and from these helpers, print with the minus sign −; `(expr).toFixed(2)` and ternaries (`p1.x > 3 ? "high" : "low"`) work as in JavaScript. A plane explore screen often pairs points with `drag: true` and a `derive` caption: the validator accepts that as the screen's interaction. It is engine-wide (`ZQ.canvas.create`), so it works on number-line, plane, bars and every other kind, runs again in the Why? copy on the explained state, and on a `pair` reads both sides (README.md, "pair").
- **Derive, pass 7.** More functions, the same in curve formulas where they make sense: `erfc`, `Phi` (accurate to about 1e-14 relative, so `Phi(-10)` is 7.62e-24), `normcdf(x, mu, sigma)` (alias `pnorm`), `normpdf(x, mu, sigma)` (alias `dnorm`), `qnorm(p, mu, sigma)` (aliases `PhiInv`, `NormInv`); matrices `solve(A, b)` (b a vector or a matrix), `inv(A)`, `transpose(A)`; lists `seq(a, b, step)`, `vadd`, `vsub`, `vmul` (element by element, a number acts as a constant list), `vscale(a, k)`, `cumsum(a)`, `diff(a)`, `rolling(a, w, "mean" | "sd" | "sum")`; seeded noise `randn(n, seed)` and `ar1(phi, n, seed, sigma, x0)` (the same shocks for every phi); objects `obj("range", [a, b], "colour", 2)` and `range(a, b)` (= `{ range: [a, b] }`), since braces are not allowed in a formula. A single state object with an id (a plane's `area: { id: "A", ... }`) is read and written by that id (`A.to`). A rule whose value is not ready yet (it reads something another rule derives) waits for the next pass instead of writing `undefined`.
- **Ordered taps.** With a tap-regions widget's `ordered: true`, every kind numbers the selected objects 1, 2, 3 in tap order (README.md, "Canvas-bound widgets").
- **Merging.** A state patch that maps indices into an array (`{ "quotes": { "bid": { "0": 49.99 } } }`, which a control bound to `quotes.bid.0` writes) patches those entries and keeps the array.
- **Keyed list patches.** Lists with ids (`points`, `vectors`, `segments`, `markers`, `pointers`) can be patched by id: `{ "points": { "p1": { "x": 2 } } }` changes only `p1`. Sending an array replaces the whole list.
- **`state.params` overrides params.** In `plane` and `distribution` it overrides the expression or family parameters (`params.params`). In `walk` it overrides top-level numbers (`p`, `mu`, `sigma`, `steps`, `paths`, `start`). This is what a bound slider writes.
- **Interactive modes.** A widget calls `canvas.enable(mode, opts)`. The modes each kind supports are listed below. Elements the author marks as movable (`"drag": true` on a plane point, `state.drag` on vectors) move without `enable`. Clones made for the Why? modal are always static.
- **Events.** `canvas.on('change', fn)` receives one of these payloads. Drags emit on every pointer frame with `phase: "move"`, then once with `phase: "end"`. Arrow keys move a focused handle (Shift moves ten steps).
  - drag: `{ type: "drag", id, x, y, phase }`, in data units.
  - tap: `{ type: "tap", id, on, selected: [ids] }`. Space toggles and the arrow keys move focus between targets.
  - Kind-specific payloads are listed under each kind.
- **Shared methods** (see `_base.js` header): `mark(ids, cls, on)`, `unmark(cls?)`, `flash(ids)`, `unflash()`, `lock(on)`, `caption(text)`, `clone(host)`, `destroy()`. Drag kinds also have `points()` returning `{ id: { x, y } }` and `place(id, pos, { instant })`.
- **Grading classes.** `is-correct`, `is-notyet`, `is-reveal` and `is-dim` go on `.cv-obj` groups through `mark()` and survive redraws. Lines inside a marked group recolour; series are never marked by the engine.


## Column width (ENGINE-BACKLOG 507)

A canvas draws into the lesson column: `--col` in `css/tokens.css`, 540px below a 768px viewport and 780px from 768px up (an iPad, a laptop). It scales to the column width; a canvas never sets its own pixel width. A tall `viewBox` gets taller on a wide column, so cap one with `canvas.maxHeight` if a widget has to stay in view beneath it. Test at 440, 1032 and 1376 (`--mobile --tablet`).

---

## plane

Coordinate plane with functions (JS expressions), points, segments, tangents, areas, Riemann rectangles, vectors and a sketch mode.

**params**
- `x: [min, max]`, `y: [min, max]`. Defaults are `[-5, 5]`.
- `grid`: true (gridlines at the ticks), a number (grid step) or false.
- `xLabel`, `yLabel`. Defaults are `$x$` and `$y$`.
- `height` in px (default 360). `equal: true` sizes the frame so units are square.
- `functions: [{ id, expr, label, domain: [a, b], colour, dashed, endpoints: ["closed"|"open"|null, ...], labelAt: x, labelSide: "above"|"below", labelOffset: [dx, dy] }]`. `labelSide` (alias `labelPos`) puts the label above (default) or below the curve; `labelOffset` nudges it in px.
- `equal: true` gives square units. With `height` as well, the height stays and the shorter range widens about its centre.
- `vlines: [{ id, x, label, colour, dashed }]` and `hlines: [{ id, y, label, colour, dashed }]` (in params or state, patchable by id) draw the reference lines x = a and y = b across the plot, dashed unless `dashed: false`; their ids are highlightable. Labels still move apart if they would overlap.
- Mixed text and maths in a label or axis title (`"Price $p$ (£)"`) keeps its spaces.
- `labelAnchor: "start" | "end"` (default end) sets which end of the label sits at the curve point. Every label (functions, points, segments, polygons, angles) keeps clear of every curve and of the axes, moving up or down (below first for `labelSide: "below"`).
- A `functions` entry in a state patch merges by id: `{ "functions": [{ "id": "f", "expr": "2*x" }] }` keeps the authored `domain`, `label` and colour unless it gives them again.
- Expressions: `-x^2` is $-(x^2)$ (a unary minus before a power applies to the whole power), and `e` is Euler's number (`e^x` equals `exp(x)`).
- `axes: false` draws no axes, ticks or grid: a geometry figure.
- `xTicks: "integer"` and `yTicks: "integer"` keep whole-number ticks only, for sequence plots on small ranges.
- `xStep` and `yStep` put a tick and a grid line at every multiple of the step (90 for a degree axis, 3 for months).
- Points outside the `x` and `y` ranges are not drawn; when a point or curve sits under the x-axis title near y = 0, the title moves below the axis.
- `yScale: "log"` (a positive `y` range): log-price charts, ticks at 1, 2 and 5 times powers of ten; `money: "£"` labels them as prices (£10, £20, £50). Points and functions use the same scale; areas under curves are for linear scales.
  - `expr` uses `x`, numbers, `+ - * / ^`, `sin cos tan exp ln log sqrt abs min max floor ceil pi e`, and any name in `params`.
  - Paths break at NaN, at asymptotes and at jumps.
- `params: { a: 1 }` are the expression parameters.
- `holes: [x]` on a function draws an open circle at the limit there (for $\frac{x^2-1}{x-1}$ at 1); a point dragged onto a hole takes the limit instead of vanishing.
- Curves that are not $y = f(x)$, as `functions` entries: parametric `{ id, x: "2*cos(t)", y: "sin(t)", t: [0, 6.2832] }` and implicit `{ id, implicit: "x^3 + y^3 - 6*x*y" }` (the curve where the expression is 0, traced on a 160 by 120 grid). A point with `on` rides either (it moves to the nearest point of the curve, so it goes all the way round a circle), and `tangent: { f, at: pointId | [x, y] }` (or `t` on a parametric curve) draws the tangent there; a vertical tangent is labelled "vertical". `labelAt` places a curve's label (a `t` value or `[x, y]`).
- A function listed in `hide` is not drawn but is still evaluated, so a point can ride it (`on`) and a tangent or area can use it.

**state**
- `points: [{ id, x, y, drag, snap, snapX, on: "f", lockX, lockY, label, labelPos: "ne"|"n"|..., colour, open }]`.
  - `on` keeps a dragged point on function `f`, inside f's `domain`.
  - `tap: false` keeps a decorative point out of tap mode.
  - `trace: true` leaves a trail where the point has been (a derive-driven point traces the curve it follows, such as $f'$ while the learner drags along $f$); `trace: "x"` joins the trail in x order. The trail clears on Start over, or with the `clearTrace()` method.
  - While sketching, a draggable point is drawn as a square, so it is not mistaken for a sketch handle.
  - `label` may contain `{x}` and `{y}`, which are filled with the current coordinates.
- `segments: [{ id, from: [x, y] | pointId, to, dashed, arrow, label, labelOffset: [dx, dy], colour }]`. The label sits at the midpoint, nudged by `labelOffset` (default 8 right, 10 up; a negative dx anchors it at its end).
- `polygons: [{ id, points: [[x, y] | pointId, ...], colour, label, vertexLabels: ["A", "B", "C"], dashed }]`: a filled shape (a light series wash) with its vertices labelled just outside it.
- `angles: [{ id, at, from, to, label, right, radius }]`: an arc between the rays at → from and at → to (the smaller angle), or a square mark with `right: true`; the label sits on the bisector; `radius` in px (default 22).
- `tangent: { f, x: number | pointId, label: "slope" | "text {slope}", length, lengthPx, side, dashed }`. It can also be an array of these. `length` spans that many x units (since pass 5; before, it was measured along the line), `lengthPx` is pixels along the line. At a corner (the one-sided slopes differ, as on `abs(x)` at 0) no tangent is drawn unless `side: "left"` or `"right"` picks one. `labelOffset: [dx, dy]` moves the slope label clear of the point's own label.
- `area: { id, f, g, from, to, label: "auto" | "text {value}", colour }`. `g` is an optional lower curve. It can also be an array.
- `riemann: { id, f, from, to, n, rule: "left"|"right"|"mid"|"trap", showSum, sumLabel }`.
- `vectors: [{ id, v: [dx, dy], from: [x, y] | pointId, label, colour }]`.
- `functions: [...]` adds functions or overrides them by id. `hide: [ids]` hides them.
- `params: {...}` overrides `params.params`.
- `sketch: { points: [[x, y], ...], target, band, showBand }` and `showTarget: true`. These are written by the sketch widget.

**ids:** function ids, point ids, segment ids, vector ids, `tangent` (or its id), `area`, `riemann`, `riemann-{i}` (rectangle `i`), `target`, `sketch`, `seg{i}` (the sketch span between control points `i` and `i+1`).

**modes and events**
- `drag` (on points with `drag: true`): `{ type: "drag", id, x, y, phase }`.
- `tap` (on points without `drag`): points become buttons, so `tap-regions` can ask "which point is (−2, 4)?" with point ids as the answer.
- Controls: `"bind": "points.p1.x"` (or `.y`) moves that point from an explore slider, which opens at the point's current value.
- `tap` also works on points without `drag`, for tap-regions.
- drag-point targets on a plane: `[x, y]`, or `{ "on": "f", "x": 12.3 }` (graded on x alone, for a steep curve), with `tol` a radius, `tol: [dx, dy]` per axis, or `tolX` for x alone.
- `slider`: no events; the slider writes `state.params`.
- `sketch`: started with `enable('sketch', { control, xRange, target, band, start, snap, reset })`. Each control point moves vertically. Emits `{ type: "sketch", points, phase }`.

**methods:** `sample(xs)` returns the sketched curve's y values (Catmull-Rom through the control points), `evaluate(fnId, x)`, `points()`, `place(id, [x, y])`.

```json
{ "kind": "plane",
  "params": { "x": [-1, 5], "y": [-1, 6], "functions": [{ "id": "f", "expr": "a*x^2", "label": "$f(x)$" }], "params": { "a": 0.25 } },
  "state": { "points": [{ "id": "p1", "x": 2, "y": 1, "drag": true, "on": "f", "label": "P" }], "tangent": { "f": "f", "x": "p1", "label": "slope" }, "riemann": { "f": "f", "from": 0, "to": 4, "n": 4, "rule": "left", "showSum": true } },
  "controls": [{ "bind": "a", "min": 0.1, "max": 1, "step": 0.05, "label": "$a$" }] }
```

**Integration pass 5 additions**
- Contour family: a function entry `{ id, contour: "x^2 + y^2", levels: [1, 4, 9], colour, dashed }` draws each level curve as joined polylines (closed curves have no gap at vertical tangents; dashes run on), each labelled with its level (`levelLabels: false` hides them). `implicit` entries are joined the same way, so `dashed: true` works on them.
- Heat map: `{ id, heat: "x*y", range: [lo, hi], colour }` fills the view behind everything with the function's colour, its opacity rising with the value (range defaults to the values seen).
- `labelAvoid: false` on a function: other labels no longer keep clear of it (background contours). `labelAt: x` holds a function's label at that x (others keep clear of it), so dense contours keep their order; on a parametric curve `labelAt` is a t, or `[x, y]`.
- Views: `state.view: { x: [a, b], y: [c, d] }` sets the ranges and animates; `state.zoom: { at: [x, y] | pointId, scale }` zooms about a point. A control binds `zoom` (the scale).
- `domain: ["0", "b"]`: a domain end may be a param name or expression, so a line stops where a slider says.
- Areas: `{ id, polar: "1 + cos(theta)", inner: "0.5", from: 0, to: "pi" }` shades a polar region (limits may be expressions); its value is ½∫(r² − r₀²) dθ. `label: "auto"` on an ordinary area integrates over the authored bounds, not the visible part. Area values reach derive as `values.<id>`.
- `riemann` may be a list (left and right sums on one plane); each sum label stacks in the top right and is typeset (`sumLabel: "$L_4$"`).
- Tap mode: areas (by id), polygons (by id) and Riemann rectangles (`riemann-0`, `riemann-1`, ...; `<id>-<i>` for a named sum) are tap targets as well as points.
- Polygons: `sector: { cx, cy, r1, r2, theta1, theta2, degrees }` is a sector or annulus wedge with curved edges; vertices may be points with `hidden: true` (no dot) moved by derive; `vertexLabels` follow them; `glyph: true` draws an F in the shape's own frame (first vertex, edges to the second and last vertex), so a reflection shows a mirrored F.
- Point labels substitute `{x}` and `{y}` only outside `$...$`, so `$\mathbf{x}$` stays a bold x.
- Tick labels sit above the curves with a halo, so a curve just below y = 0 never hides them.
- `equal: true` narrows the frame instead of widening x past the authored range.
- A tangent's `length` spans that many x units (`lengthPx`: pixels along the line); on parametric and implicit curves `length` is measured along the line.
- Curve formulas may call `sum(k, 0, n, term)` (a partial sum: Taylor polynomials with a slider on `n`) and `fact(k)`.
- `values()` returns area values by id; `setParam` / `getParam` handle `zoom`, dotted state paths (`tangent.x`) and params.

**Integration pass 7 additions**
- A point with `on: "f"` stays on its curve whenever its x changes (a control on `points.p1.x`, a derive, an explanation patch) or the curve's params change, not only while dragged; on a polyline or parametric curve it moves to the nearest point.
- Function entries: `exprs: ["1", "a*x", ...]` with `index: "d"` (a param name, or a number; `indexFrom` shifts it) picks one formula, so a control switches between precomputed fits without a ternary chain; `points: [[x, y], ...]` is a polyline (an empirical ROC curve) that a point can ride with `on`; `steps: { at: [b1, b2], levels: [l0, l1, l2], from, to, closed: "left" | "right" }` is a step function (closed dot at the left end of each piece by default, open at the right; a list of these with `index` switches them); `cells: { x: [x0, x1], y: [y0, y1], values: [[...], ...], colours, opacity }` is a classified-region layer (values[0] is the bottom row; class k washes in series slot k + 1, null is clear), for a k-NN or tree decision region computed offline. `contour` and `heat` entries are accepted by the validator in params and state.
- `hide: [ids]` also hides points, segments, polygons, angles, vectors and reference lines, by id or by a `group` name on the item (`hide: ["test"]` hides every point with `group: "test"`), so a control plus derive can reveal a set.
- `xAxis: "bottom"` keeps the x axis at the bottom edge even when the y range spans 0 (signed coefficient paths); `xScale: "log"` (a positive x range) with ticks at 1, 2 and 5 times powers of ten; `xFormat` / `yFormat: "percent"` (or `"%"`) label ticks as percentages (0.05 reads 5%).
- Point labels take `{x:.2f}` and `{y:.0f}` (fixed places, trailing zeros kept: `£{y:.2f}` reads £100.00).
- Labels keep clear of points as well as curves (`labelsAvoidPoints: false` turns that off); a function label pushed more than 14px off its curve gets a thin dashed leader back to it (`leaders: false` turns that off). Close vertical reference lines put the earlier label on the left of its line, so neither vanishes. The x-axis title also moves for the sketch's control points.
- `state.ci: { n, size, mu, sigma, seed, level, known, label }` draws n confidence intervals from repeated seeded samples, one per row (give `y: [0, n + 1]`), the misses in the negative colour, mu dashed, and "k of n miss" at the top (`label: "{misses} of {n} miss"`); `values().misses` and `values().covered` feed a derive caption, and a control on `ci.n` adds samples (the same draws each time).
- Segments are tap targets in tap mode (by id; `tap: false` opts out).
- Derive targets for `vlines` and `hlines` work by id like any list item: `"derive": { "v1.x": "mu + 1.96 * se" }`.

**Integration pass 8 additions: vector fields, slope fields and trajectories (item 431)**

Three optional layers on a `plane`, in `params` (fixed) or `state` (a state entry merges over the params entry with the same `id`; give the whole entry with its `id` when patching). Each is one object or a list of objects. Formulas use the same expression language as curves: `x`, `y`, the `params` (so a slider bound to a param redraws the layer, like a slider-bound curve), `+ - * / ^` and the usual functions. `hide: ["F"]` hides a layer by id but it still runs, so a trajectory can follow a field that is not drawn. All three are untouched by existing planes: a plane without these keys draws exactly as before.

- `field: { id, P, Q, grid, spacing, normalise, length, colour, colourBy, colourHigh, range, anchor, maxArrows }`: arrows of (P(x, y), Q(x, y)).
  - `grid` is the number of columns (default about one per 34 px of the plot) or `[columns, rows]`. Arrows sit at multiples of a nice step (so the origin and integers are nodes) and are kept clear of the frame. `spacing: s | [dx, dy]` sets the step in data units instead.
  - `normalise: true` draws every arrow the same length (`length` px, default 80% of the cell, 8 to 30); otherwise length grows with magnitude, the largest arrow (or `range[1]`) taking the full length.
  - `colour` is a slot 1 to 6 or a named colour (default `"muted"`, a quiet grey, so a trajectory stands out). `colourBy: "magnitude"` ramps the colour from `colour` (default slot 1) at the weakest arrow to `colourHigh` (default slot 2) at the strongest, in eight steps (one path element per step, so it stays cheap). `range: [lo, hi]` fixes the magnitudes at the two ends, so the colours and lengths do not shift as a slider moves.
  - `anchor: "tail"` puts each arrow's tail on its node (default: centred). `maxArrows` (default 360, at most 600) caps the count: the step widens until the grid fits, so a phone never draws more.
  - Arrow directions are drawn in screen space, so use `equal: true` for true angles. A zero or undefined vector leaves its node empty.
- `slopeField: { id, f, grid, spacing, length, colour, colourBy, colourHigh, range, maxArrows }`: for dy/dx = f(x, y), a short segment of that slope at each node, all the same length (`length` px). `colourBy: "magnitude"` colours by steepness (the angle, by default; `range` instead gives |f| for the two ends). Same grid options as `field`.
- `trajectory: { id, in, from, starts, step, length, back, by, maxSteps, arrow, dashed, colour, label }`: the solution curve through a start, by fixed-step RK4.
  - `in` is the id of a `field` or `slopeField` (default: the first field, else the first slope field).
  - `from` is a point id (a point with `drag: true`, or one a `drag-point` widget moves, so the curve redraws on every pointer frame) or `[x, y]`. `starts: [[x, y] | pointId, ...]` adds fixed starts (up to 24), each drawn the same way with a dot where it begins.
  - A field is followed in time: `dx/dt = P, dy/dt = Q`. A slope field is followed in x. `length` is how far to go (default 10 for a field, the plot width for a slope field); `step` the RK4 step (default `length / 200`; the steps are adjusted to divide `length` exactly, so a full orbit closes). `back: true` also runs backwards for the same distance, or `back: 4` for that distance. `by: "arc"` follows the field normalised, so `length` and `step` are distances along the curve (default length three times the plot diagonal): use it for fields whose speed varies wildly, or for steep slope fields.
  - `maxSteps` (default 2000, at most 5000) caps the work per curve and direction: a curve that would need more is cut short. The curve stops at the plot's edge (the last step is cut exactly at the edge), at a stationary point and where the field is undefined (a square root of a negative number).
  - `arrow: false` removes the arrowhead at the forward end. `label` sits at the forward end.
  - `values()` gives `<id>EndX` and `<id>EndY`, the forward end of the `from` curve, to `derive` (`values.TEndX`) and captions.

## bars

Bar chart or histogram. It can draw dashed exact-value lines and fill itself from a seeded simulation.

**params**
- `categories: [2, 3, ...]` or `[{ id, label, value }]`. Alternatively `bins: { min, max, width }`.
- `yLabel`, `xLabel`, `height`, `colour`, `showValues`, `yMax`, `yMin`.
- Histograms: with `bins` and `data: [raw observations]`, the bars are the counts in the bins; a control bound to `binWidth` re-cuts them (`state.binWidth`). Bin ids are `b0`, `b1`, … (zero-based).
- `truncate: true` with a `yMin` above 0 starts the axis there, the truncated-axis trick to show directly.
- Negative values hang below a zero baseline (a profit and loss by month); the axis runs down to a tick under the lowest bar unless `yMin` fixes it, and a negative bar's value label sits under it.
- Value labels (`showValues`): `decimals: 2` fixes the places and keeps trailing zeros (0.50, not 0.5); `money: "£"` prefixes the currency and uses two places unless `decimals` says otherwise (£12.50).
- `exact: [{ x: "7", y: 0.1667 }]`. `x` is a category label or id; for bins it is any value inside the bin.
- `exactLabel` (default "exact"; false hides it).
- `proportion`: plot proportions. Defaults to true when `exact` is given.
- `sim: { trials: [10, 100, 1000], outcome: "d6()+d6()", seed: 7 }`. `outcome` is a `ZQ.sim.outcome` expression.

**state**
- `values: { "7": 6 }`, keyed by category label or id. An object category `{ id, label, colour }` keeps its own `id` (not `x{label}`) and may take its own series slot; `state.colours: { "<id or label>": slot }` changes them.
- `params: { k: 7 }`: free parameters. `setParam(name, v)` with a name that is no category writes here, so one control and a `derive` block can drive every bar: `"derive": { "values.a": "k", "values.b": "10 - k" }`.
- `ran: n` is the number of simulated trials. Trials are the first `n` outcomes of the seeded stream, so Run 10 then Run 100 shows trials 1 to 110, the same every time.
- `params: { trials: n }` is an alias for `ran`, for a slider.
- `showExact: false`, `selected`, `highlight`.

**ids:** `x{label}` for categories (`x7`, `xHeads`), `b{i}` for bins (0-based), `exact`, `exact-x7`.

**sim:** a Run 10 / Run 100 / Run 1,000 / Reset chip row and an "n trials" count sit under the chart. A run fills the bars over at most 1,200 ms and emits `{ type: "run", ran, added }`. Methods: `run(n)`, `reset()`, `values()`, `counts()`, `setParam(category, v)`, `getParam(category)`.

**controls:** bind a category's label or id (or `"values.<label>"`) to move that bar's height: `"controls": [{ "bind": "7", "min": 0, "max": 10, "step": 1, "label": "Sevens" }]`. Set `yMax` so the scale stays put while the bar moves.

**modes:** `tap` (on bars) and `slider`.

```json
{ "kind": "bars",
  "params": { "categories": [2,3,4,5,6,7,8,9,10,11,12], "xLabel": "Total of two dice",
    "exact": [{ "x": "7", "y": 0.1667 }, { "x": "6", "y": 0.1389 }, { "x": "8", "y": 0.1389 }],
    "sim": { "trials": [10, 100, 1000], "outcome": "d6()+d6()", "seed": 7 } },
  "state": { "ran": 0, "caption": "Run some rolls and watch the 7 bar." } }
```

**Integration pass 5 additions:** value labels on negative or near-zero bars sit clear of the baseline and category labels (with a halo). `state.dim: [ids or labels]` (or `dim: true` on a category) fades bars, for "keep the largest singular values".

**Integration pass 6 additions**
- `groups: [{ id, label, colour }]`: two or more bars per category side by side, with a legend; heights from `state.values.<group id>` (`{ category: value }`), from a category's `value: [a, b]`, or from a sim whose outcome is a list (`"[binomial(6, 0.3), binomial(6, 0.6)]"`). Bar ids are `<category id>-<group id>`.
- `yScale: "log"`: positive heights on a log axis.
- `xAxis: "value"` (or `x: [min, max]`) sets numeric categories at their values on a numeric axis; `state.transform: { a, b }` moves them to aX + b, so a linear transformation slides along the axis.
- `state.cut: { at, side: "above" | "below", colour, label, line }` recolours every bar whose category value is beyond the cut and draws the cut line (`{at}` in the label); a control binds `cut.at`.
- `hlines` (params or state, patchable): dashed reference lines with labels. `curves: [{ id, expr, colour, dashed, label, shade: { from, to } }]` (params or state): a curve over the bars in category units (bins, value axes, or numeric categories), reading params, `state.params` and `w` (the bin width), so a normal curve follows a slider on n; `shade` fills under it from a cut.
- `showMean` draws the weighted mean of the heights; `state.pivot` draws a fulcrum under the axis, draggable with `drag: true` or a drag-point widget (target: a number), for "balance the see-saw".
- Simulations: `sim.outcome` reads params and `state.params` by name, so a slider on sample size re-runs the seeded stream; `sim.let: { xs: "sample(k, n())" }` binds names per trial; `sim.filter: "xs[0] > 0"` discards trials (the count reads "1,000 trials (195 discarded)"); outcome helpers `sample`, `mean`, `var`, `varp`, `sd`, `sum`, `len`, `tstat(k)` (see `engine/sim.js`). Methods `discarded()`, `points()`, `place("pivot", x)`.

**Integration pass 7 additions**
- A catch-all category: a label ending in `+` (`"4+"`) or `{ "label": "4 or more", "atLeast": 4 }` (or `atMost`) takes every outcome from there on, so a capped count needs no `min(..., 4)` trick.
- Sim outcomes gain `maxn(k, e)`, `minn(k, e)` (the largest or smallest of k fresh draws), `count(k, e)`, `repeat(k, e)`, `argmax(list)`, `argmin(list)`, and `max` / `min` accept a list (`max(sample(N, n()))`).
- Bins are half-open, [lo, hi), with the top edge of the last bin counted in it, for data and sims alike.
- `state.categories` replaces the category list, so a derive such as `"categories": "seq(0, n)"` gives one bar per value of n.
- `dataSets: [[...], [...]]` with `index: "k"` picks one data set by a param (precomputed C++ draws following a control stop).
- With `showValues`, a bar of height 0 shows its 0 (`showZero: false` hides it). With `state.cut`, `values()` adds `beyondCut` (the height past the cut) and `beyondShare` (its share of the total).

## distribution

A pmf drawn as bars, or a pdf drawn as a curve, with a shaded probability.

**params**
- `family`: `binomial` (`n`, `p`), `geometric` (`p`; support 1, 2, ...), `poisson` (`lambda`), `uniform` (`a`, `b`), `normal` (`mu`, `sigma`), `exponential` (`lambda`) or `t` (`nu`).
- `params`: the family parameters. Greek keys (`μ`, `σ`, `λ`, `ν`) also work.
- `x: [min, max]` (default from the family), `yMax`, `height`, `xLabel`, `yLabel`.
- `showMean`, `showSd`, `showValues`, `variable` (default `X`), `dp` (default 4), `snap` (drag step for continuous families, default 0.01), `colour`.

**state**
- `shade: { from, to }`. Either end may be `null` for an open tail. Discrete bounds are inclusive integers. The probability label, for example `P(0 ≤ X ≤ 3) = 0.6496`, is computed and placed automatically. `probLabel` overrides its text and `showProb: false` hides it.
- `params`: animates. The axes only ever grow, so the shapes can be compared.
- `showMean`, `showSd`.
- `overlay: [{ id, family, params, label, colour }]`: dashed comparison curves, such as a normal over a t.

**ids:** `x{k}` (pmf bars), `curve`, `shade`, `prob`, `mean`, `sd`, overlay ids.

**modes:** `drag` (diamond handles on the shade bounds) emits `{ type: "drag", id: "from"|"to", x, y: 0, from, to, phase }`. `slider` is also supported.

**methods:** `probability(from?, to?)`, `stats()`, `points()`, `place("from"|"to", value)`.

```json
{ "kind": "distribution",
  "params": { "family": "normal", "params": { "mu": 0, "sigma": 1 }, "showMean": true, "showSd": true },
  "state": { "shade": { "from": -1, "to": 1 } } }
```

**Integration pass 6 additions**
- Families `hypergeometric` (`N`, `K`, `n`), `lognormal` (`mu`, `sigma`; `showMedian` adds a median marker beside the mean) and `discrete` (alias `custom`: `values` and `probs`, in params or in `params.params`, any spacing; the mean and sd follow).
- `cdf: true` (params or state) draws the CDF: steps with a closed dot where each lands and an open dot where it leaves, or the curve for a continuous family; shading is not drawn in CDF mode.
- Axes: a discrete family's x range and y axis follow its support as a slider moves `n` (`axes: "grow"` keeps the old only-grow behaviour; continuous families grow, `axes: "follow"` tracks). Discrete ticks fall on every integer when there is room, else every 2nd, 5th, 10th.
- `shade` may be a list of regions: the label sums them (`P(X ≤ 14) + P(X ≥ 26) = 0.0807`); each may carry `id` (default `shade`, `shade1`, …) and `colour`. Bounds may be expressions in the family's params (`"from": "mu - sigma"`), so shading follows a slider. A region with `under: "<overlay id>"` fills under that overlay curve, hatched (a continuity-correction strip, or β under the alternative), with an optional `label` (`{value}` is its probability).
- Overlays live in state (patchable by id) or params; an overlay's params may be expressions in the main params (`{ "mu": "n * p", "sigma": "sqrt(n * p * (1 - p))" }`), so it follows the sliders. Derive can also address one by id: `"nrm.params.mu": "n * p"`.
- `observed: 2.1`, `{ x, label, colour }` or a list: solid marker lines with labels (`{x}` in the label), drawn under the probability pill.
- `rug: [x, …]` or `{ x: [..], sticks: true, colour }`: short ticks on the axis, or sticks up to the density with a dot.
- `drag: true` (params or state) shows the shade handles on an explore screen without a drag-point widget; dragging moves the first region.
- ids: `cdf`, `median`, `rug`, `observed`, `observed1`, …, named shade regions.

**Integration pass 7 additions:** `family: "beta"` with `params: { a, b }` on [0, 1] (mean, sd and the usual shading and labels), for posteriors and credible intervals.

## scatter

Points, a least squares line, a given or learner-placed line, and residuals.

**params**
- `points: [[x, y], ...]` or `[{ id, x, y, label }]`.
- `x`, `y`: an axis label string or a range `[min, max]`. Alternatively use `xLabel`, `yLabel`, `xRange`, `yRange`.
- `fit: true` draws the least squares line (ink, id `fit`). `fitLabel` is `"auto"` (the equation) or text.
- `drag`: true or a list of point ids. `dragLine: false`. `snap`. `height`.

**state**
- `points`: the current positions, patchable by id.
- `line: { m, b, label, dashed, colour }`. This is the learner's or a given line. It is drawn in slot 2, or manipulable blue in drag mode.
- `residuals`: true, `"fit"` or `"line"`. Residuals are coloured by sign.
- `showSSE`: shows the sum of squared residuals. `showFit`, `highlight`, `selected`.

**ids:** `p{i}` (0-based, in the order of `points`), `fit`, `line`, `r-p{i}` (residual segments).

**modes:** `drag` and `tap`.
- Dragging a point emits `{ type: "drag", id: "p3", x, y, phase }`.
- Dragging a line end emits `{ type: "drag", id: "line", m, b, phase }`.

**methods:** `fit()` returns `{ m, b }`. Also `points()` and `place(id, [x, y])`; `place("line", { m, b })` sets the line.

```json
{ "kind": "scatter",
  "params": { "points": [[1, 2.1], [2, 2.9], [3, 3.2], [4, 4.8], [5, 5.1]], "x": "Hours studied", "y": "Score" },
  "state": { "line": { "m": 0.5, "b": 2 }, "residuals": "line", "showSSE": true } }
```

**Integration pass 5 additions:** `curves: [{ id, expr: "f(x)" } | { id, x: "...", y: "...", t: [a, b] } | { id, implicit: "F(x, y)" }]` (params or state, with `colour`, `dashed`, `label`, `labelAt: [x, y]`) draws curves over the cloud, such as a risk ellipse. Controls and derive reach `line.m` and `line.b` directly (a missing line starts flat at 0).

**Integration pass 6 additions:** `sim: { n, rho, seed, mx, my, sx, sy }` draws n seeded normal pairs with correlation `rho`; a control on `rho` (state.params.rho) re-correlates the same draws, and `values()` gives `r`, the sample correlation, for captions.

**Integration pass 7 additions**
- Curves take `thin: true` and `opacity` (a band of resampled fits).
- A point with `exclude: true` is drawn as a ring and joins neither the fit nor the residuals (an (x̄, ȳ) marker); `showSAE: true` adds the sum of absolute residuals under `showSSE`; `xTicks: "integer"`; `state.lines: [{ id, m, b, label, colour, dashed }]` draws more straight lines, each with its label.
- Points carry a `group` (on an object point, or a third entry `[x, y, "A"]`) and are coloured by it with a legend in the top right; `params.groups: ["A", { "id": "B", "label": "Bonds" }]` orders and names them, `legend: false` hides it.
- The validator accepts `fit`, `line`, curve ids and residual ids `r-p{i}` as highlight targets.

## series

One or more time series, with optional candles.

**params**
- `series: [{ id, label, values: [...], ohlc: [[o, h, l, c], ...], colour, dashed, thin }]`.
- `x`: `"index"` or `"dates"`. With `"dates"`, `dates` holds ISO dates, one per value.
- `candles: true` draws the `ohlc` arrays as candles.
- `format`: `"pct"` (values are fractions), `"money"` (with `currency`, default `$`) or none. `money: "£"` is the same as `format: "money"` with that currency, and its `{value}` labels keep two places (£12.50). `decimals: n` fixes the places of `{value}` labels in any format, keeping trailing zeros.
- A `null` in `values` leaves a gap: the line lifts and starts again at the next number (use it for a missing day or a series that starts late).
- `y: [min, max]`, `baseline` (for example 0 for returns), `yLabel`, `xLabel`, `indexFrom`, `height`, `drawdownLabel`.
- Each series is labelled directly at its line end; there is no legend.
- `title`: a heading above the plot. `dateFormat` (with `x: "dates"`): tick labels by `%Y`, `%y`, `%m`, `%d`, `%e`, `%b`, `%B`, for example `"%b %Y"` (Jan 2024) or `"%d/%m"`, to match matplotlib's `DateFormatter`.
- A series with `fill: "below"` (or `true`) shades between its line and zero (or `baseline`, or its own `fillTo`), as `fill_between` does.
- A second y axis: series with `axis: 2` use the right-hand axis, with `y2: [min, max]` (else from their values), `y2Label` and `y2Format: "pct" | "money"`. It is the dual-axis chart for the "two scales" trap.
- `margins: { left, right }` fixes the plot's side margins in px; a `pair` with `shareMargins: true` sets them for you so stacked panels line up.
- A short chart (a stacked panel 190px high) still gets at least three y ticks.

**state**
- `markers: [{ id, i, series, label, below, colour, y }]`. `i` is a 0-based index into the values array (even with `indexFrom: 1`, which only changes the axis labels) or an ISO date. `label` may contain `{value}`, which keeps the canvas `decimals` unless the marker has its own `decimals`. A marker sits on its series' value at `i`; give `y` to place it explicitly, which you must do where that value is `null` (a marker on a gap is otherwise skipped).
- `shade: [{ id, from, to, label, tone: "neg"|"pos"|"neutral" }]`. `from` and `to` are 0-based indices into the values array (or ISO dates), whatever `indexFrom` says.
- `yScale: "log"` in params: a log-price chart (positive values), ticks at 1, 2 and 5 times powers of ten in the money format.
- `drawdown: true` finds and shades the maximum drawdown of the first series, labelled `Max drawdown −x%`. `drawdown: "money"` measures the absolute fall instead, labelled in the money format (`Max drawdown −£90.00`), for cumulative P&L that starts at zero; `"abs"` gives the plain number.
- `window`: `{ from, to, label }`, or `[from, to]`. A slider can bind to `window.to`.
- `reveal`: 0 to 1. Animating it draws the lines from left to right.
- `hide: [seriesIds]`, `highlight`, `selected`.

**ids:** series ids, marker ids, shade ids (`shade{i}` by default), `drawdown`, `window`, candles `{seriesId}-{i}`.

**modes:** `slider` and `tap` (on markers). **methods:** `maxDrawdown(id)`.

```json
{ "kind": "series",
  "params": { "series": [{ "id": "px", "label": "Strategy", "values": [100, 104, 101, 97, 99, 106] }], "format": "money", "currency": "£" },
  "state": { "drawdown": true, "markers": [{ "id": "peak", "i": 1, "label": "peak" }] } }
```

**Integration pass 5 additions:** horizontal reference lines, `hlines: [{ id, y, label, dashed, colour, axis: 2 }]` in params (fixed, and inside the auto y range) or state (patchable by id). Dashed unless `dashed: false`; the label sits at the right end above or below the line, or at the left, wherever no series passes.

**Integration pass 6 additions**
- A series may be simulated: `sim: { outcome, n, seed, running: "mean" | "varp" | "var" | "sd" | "sum" | "none", let, filter }` plots the running statistic of n seeded outcomes (params read by name).
- `xScale: "log"` spaces the index on a log axis (from `indexFrom`, default 1); `xStep: 250` fixes the tick spacing.
- Controls bind `reveal` (0 to 1), `revealAt` (an index) and `markers.<id>.i`; a marker with `i: "reveal"` rides the end of the reveal.

**Integration pass 7 additions**
- `xValues: [0.01, 0.1, 1, 10]` gives each index its real x (with `xScale: "log"` on a log axis; `xStep` sets linear ticks); markers and shades still take indices.
- `step: true` on a series draws a step line (flat, then a jump at each point), for balances that jump.
- `sim` with `band: 2` on a running mean shades mean ± 2·sd/√i; a series may also carry `band: { lo: [...], hi: [...] }` (error bands from precomputed values).
- `state.series: { "<id>": { values: [...] } }` overrides a series, so a derive can redraw a line from a slider (`"series.x.values": "ar1(phi, 60, 7)"`, `"series.net.values": "cumsum(vsub(gross, vscale(traded, c)))"`); give `params.y` so the axis holds still. `hide` (state, and so derive) still hides lines by id.
- Marker labels take `labelSize` (or `params.markerLabelSize`) and `labelOffset: [dx, dy]`, and keep clear of the end labels.
- `hlines` and the `window` are tap targets in tap mode; `vlines: [{ id, i, label, colour, dashed }]` (params or state, patchable: a control binds `vlines.v1.i`) draws a vertical reference at an index or date.
- With a `dateFormat` that shows only the year (`"%Y"`), ticks fall on the first date of each year; with only a month (`"%b %y"`), on the first of each month.

## walk

Random walks or price paths from the seeded RNG.

**params**
- `model`: `"coin"` (steps of ±`step` with up probability `p`) or `"normal"` (increments of `mu` + `sigma`·Z).
- `steps`, `p`, `step` (default 1), `mu`, `sigma`, `start`, `paths` (count).
- `barriers: [lower, upper]`. Either may be null.
- `sim: { seed }`. `bold` is the index of the bold path (default 0).
- `label` (end label of the bold path), `upLabel`, `downLabel`, `meanLabel`, `y`, `yLabel`, `xLabel`, `height`.
- Other paths are faint.
- The uniform and normal draws are fixed per run, path and step. So sliding `p`, `mu` or `sigma` morphs the same paths instead of redrawing new ones.

**state**
- `run: n` re-samples: run `n` is the next independent batch from the same seed. A new run draws in over 800 ms.
- `showMean`: the expected path, dashed.
- `showSpread`: true, or k for ±kσ√t dashed envelopes.
- `showHits`: first-hit dots and an "h of N paths hit" count. `hitsLabel` may use `{hits}` and `{paths}`.
- `stopAtBarrier`: paths stop at their first hit.
- `params`: slider overrides.
- `highlight: [pathIndex | "path3"]`.

**ids:** `path{i}` (0-based), `barrier-up`, `barrier-down`, `mean`, `spread`.

**modes:** `slider` and `tap` (on paths). **methods:** `run()`, `paths()`, `hits()` (first-hit step per path, -1 if none).

```json
{ "kind": "walk",
  "params": { "steps": 60, "p": 0.5, "paths": 40, "barriers": [-10, 10], "sim": { "seed": 1 } },
  "state": { "showMean": true, "showHits": true } }
```

**Integration pass 6 additions:** `model: "markov"` with `states: ["Bull", "Flat", "Bear"]`, `P` (row-stochastic) and `start` (a state or an index) simulates state paths, drawn as steps on a y axis labelled with the states. `xStep: 1` gives whole-number step ticks. With both barriers, `showHits` counts the top and the bottom separately ("6 hit the top, 11 the bottom (of 20)"; `{up}` and `{down}` in `hitsLabel`; method `hitCounts()`). A control `{ "reseed": true, "label": "New paths" }` is a button that draws the next seeded run.

**Integration pass 8 additions (item 436)**

- `model: "ou"` (also `"mean-reverting"`, `"ar1"`): X(n+1) = X(n) + `theta` (`mu` - X(n)) + `sigma` Z on the seeded normal draws, from `start`. `theta`, `mu` and `sigma` are slider-bindable, and sliding them morphs the same paths. The level `mu` is a dashed line labelled "mu = 2" (`meanLine: false` hides it, `levelLabel` renames it). `showMean` draws the expected path mu + (start - mu)(1 - theta)^n; `showSpread: k` draws the +/- k sd band of the AR(1) variance. Give `y: [lo, hi]` so the axis holds still while sliders move.
- `lower`, `upper` (params): barrier levels that replace `barriers[0]` and `barriers[1]`. A control `{ "bind": "upper", "min": 2, "max": 20, "step": 1 }` moves the barrier; hit dots, counts, `stopAtBarrier` paths and the stopped average redraw live, and the slider opens on the barrier. The held y range resets when a barrier moves.
- `stopAt: n` (param): a fixed stopping step; tau = min(first barrier hit, `stopAt`, `steps`). A dashed line marks it (`stopLabel` renames "stop"). With `stopAtBarrier` paths end at tau.
- `drawn: n` (param): draw only n paths (and the bold one); all `paths` still count in hits, stopped values and the running average. Use 300 paths with `drawn: 30`.
- `overlays` (params): the panels that can sit under the walk, each on the walk's step axis and its own y scale. An entry is an id string or `{ id, type, label, chip, colour, y, ... }`:
  - `"sq"`: (S_n - n m)^2 - n v^2 for the walk's drift m and variance v^2; at p = 1/2 and step 1 it is S_n^2 - n. `centred: false` gives the literal S_n^2 - n.
  - `"ratio"`: (q/p)^S_n with p and q the walk's own step probabilities (coin); for the normal model exp(-2 mu S_n / sigma^2). Not defined for markov or ou, or p of 0 or 1.
  - `"bankroll"`: `bankroll` (start, default 100) plus the winnings of a bet every step. `bet` (param, overlay key or `state.bet`): `"fixed"` (`stake`, default 1), `"double"` (stake, doubled after each loss, back to stake after a win), `"fraction"` (`fraction` of the bankroll, default 0.1). A bet never exceeds the bankroll or `maxBet`; at zero the bankroll stays ruined. `bankroll`, `stake` and `fraction` take sliders.
  - `{ "id": "cube", "expr": "S^3 - 3 * n * S" }`: any formula in `n` (step), `x` (position), `S` (position less start, in steps for the coin), `p`, `q`, `start`, `step` and the numeric params; `label` and `stopLabel` take `$...$`.
  - `y: [lo, hi]` fixes an overlay's range; otherwise ratio and bankroll trim the top at the 95th percentile of the per-path maxima. `overlayHeight` (default 84) is each panel's plot height in px. `toggles: false` hides the chips.
- `state.overlays`: the ids shown (a list; `true` for all, the default; `false` for none). Each overlay also has a chip under the canvas (`chip` renames it). A chip emits `{ type: "overlay", id, on, overlays }`.
- `state.showStopped`: `true` or `"walk"` (S_tau), an overlay id, or a list. Adds a panel per entry: the running mean of the stopped value over the first k paths against k, a dashed line at the start value, and "start" and "mean" labels; stopped values are dots at tau on the paths. Needs several seeded paths (100 or more).
- `state.bet`: the bankroll rule, patchable.
- **ids:** also `mean-level` (ou), `stop-time`, `ov-{id}` (an overlay), `stopped-{key}` (a running-mean line), `stopped-ref`.
- **methods:** also `values()` (numbers for derive: `paths`, `hits`, `hitsUp`, `hitsDown`, `stopAt`, `tau`, `tauMean`, `endMean`, `stopped`, `stoppedSE`, `stoppedValues`, `runningMean`, and `stopped<Id>`, `stopped<Id>SE`, `runningMean<Id>`, `ruined<Id>` per overlay, for example `stoppedRatio`), `stopTimes()`, `stopped(key)`, `runningMean(key)` (key `"walk"` or an overlay id) and `getParam(name)`.

```json
{ "kind": "walk",
  "params": { "steps": 80, "p": 0.5, "paths": 300, "drawn": 30, "barriers": [-8, 8], "overlays": ["sq"], "sim": { "seed": 7 } },
  "state": { "stopAtBarrier": true, "showStopped": true },
  "derive": { "caption": "Mean at the stop: {{fixed(values.stopped, 2)}}" },
  "controls": [{ "bind": "upper", "min": 2, "max": 20, "step": 1, "label": "Upper barrier" }] }
```

## matrix

**params**
- `matrices: [{ id, rows: [[...]], label }]`. Cells may be numbers or strings, including `$...$`.
- `ops: ["×", "="]`: the operators between consecutive matrices.
- `cellHeight`.
- When the matrices, operators and any row-operation label are wider than the column, the whole drawing scales down to fit (cells keep their proportions).

**state**
- `highlight`: ids, or the object form `{ "A": { "rows": [0], "cols": [1], "cells": [[0, 1]] } }`. In the object form, rows take a slot 1 wash, columns a slot 2 wash and cells a pear wash. These washes are persistent and do not pulse.
- `pivot: ["A-0-0"]`, or `{ "A": [[0, 0]] }`. Each pivot is circled.
- `rowOp: { m, from, to, k, swap, label }`. This draws a curved arrow on the right of matrix `m`, labelled for example $R_2 \to R_2 - 3R_1$. Use `from` = `to` to scale one row, and `swap: true` for a swap.
- `hidden: ["C"]` or `["C-0-1"]`: those cells show as dashed empty boxes.
- `cell: "C-0-1"` (or a list): shows those result cells even when hidden. A newly shown cell fades in.
- `product: { a: "A", b: "B", c: "C", i, j }`. Row `i` of `a` lights up, then column `j` of `b`, then cell `c-i-j` fills in (1.1 s).
- `rows: { "A": [[...]] }` replaces a matrix's entries, for row reduction steps.
- `values: { "C-0-1": 7 }` overrides single cells.

**ids:** `A` (the whole matrix), `A-r0`, `A-c1`, `A-0-1`, `rowop`.

**modes:** `tap` (on cells). **methods:** `product("A", "B")` returns the product rows.

```json
{ "kind": "matrix",
  "params": { "matrices": [{ "id": "A", "rows": [[1, 2], [3, 4]], "label": "$\\mathbf{A}$" }, { "id": "B", "rows": [[5, 6], [7, 8]], "label": "$\\mathbf{B}$" }, { "id": "C", "rows": [[19, 22], [43, 50]], "label": "$\\mathbf{AB}$" }], "ops": ["×", "="] },
  "state": { "hidden": ["C"], "product": { "a": "A", "b": "B", "c": "C", "i": 0, "j": 1 } } }
```

**Integration pass 5 additions**
- `highlight` object form draws (`{ "A": { "rows": [1] } }`), and a matrix may take several groups with their own colours: `{ "A": [{ "rows": [0], "cols": [0], "colour": 2 }, { "cells": [[1, 1], [1, 2]], "colour": 3 }] }` (a cofactor's crossed-out row and column in one wash, the minor in another). A later patch replaces the groups whole. `hidden` applies before `highlight`, so a patch that shows a matrix and highlights it works in the Why? copy.
- `rowLabels: ["$R_1$", ...]`, `colLabels: ["$x$", ...]` per matrix; `scale: "\\tfrac{1}{\\sqrt{2}}"` (a factor before the brackets); `bar: k` (an augmented bar before column k).
- Operators in `ops` may be KaTeX (`"$\\cdot$"`, `"\\otimes"`). Cell widths are measured from the rendered KaTeX, so `\cos\theta` and `\tfrac{5}{6}` fit. Negative numbers print with the minus sign. `{{expr}}` in a cell fills live from params and `state.params` (controls write them).
- The pivot ring grows with a wide entry; `rowOp` defaults to the matrix that has the rows it names.
- `fit: true` narrows the frame to the matrices (the default for a matrix inside a pair), so each side of a pair keeps its size; a pair with a matrix side stacks when side by side would draw either below 80% (`minScale` on any pair sets the threshold).

## vectors

**params**
- `x`, `y` ranges (the frame keeps square units), `grid`, `snap`, `height`, `xLabel`, `yLabel`.
- `vectors: [{ id, v: [x, y], label, from: [x, y] | vectorId, colour, labelPos, labelSide }]`. `labelPos` is `"end"` (default, just past the head), `"mid"` (beside the middle of the arrow) or `"start"` (by the tail); `labelSide: "right"` puts a mid or start label on the arrow's right (default left).
- `points: [{ id, x, y, label, labelPos, colour }]`: labelled dots such as O, A, B and M; `labelPos` is a compass point (`"ne"` default, `"n"`, `"e"`, `"se"`, `"s"`, `"sw"`, `"w"`, `"nw"`). Patchable by id like `vectors`.
- `showCoords`, `basisLabels`, `sumLabel`, `projLabel`.

**state**
- `vectors`: patchable by id, for example `{ "u": { "v": [3, 1] } }`.
- `show: ["sum", "projection", "span"]`.
- `sum: ["u", "v"]` (default: the first two). The parallelogram sides are dashed and the sum arrow is slot 3.
- `project: { of, onto }`: draws the projection arrow, the dashed perpendicular and a right-angle mark.
- `span: ["u"]`: a shaded line, or the whole plane when two independent vectors are given.
- `scale: { "u": 2 }`: draws the scaled arrow and leaves a dashed ghost of the original. The label becomes `2u`.
- `basis: [[1, 0.5], [-0.5, 1]]`: replaces the grid with the skewed basis grid and draws `b1`, `b2`. It animates.
- `drag: ["u"]`: which heads move. In drag mode all heads move unless `drag` is given. Only a vector drawn from the origin (no `from`) has a draggable head; one drawn from another vector's head follows it.
- `hide`, `highlight`, `sumColour`, `projColour`.

**ids:** vector ids, point ids, `sum`, `proj`, `perp`, `span`, `b1`, `b2`.

**modes:** `drag` (vector heads) emits `{ type: "drag", id, v: [x, y], x, y, phase }`. `tap` (whole arrows and points; tap-regions `answer` and `among` name vector or point ids) emits `{ type: "tap", id, on, selected }`. `slider` is also supported. **methods:** `points()`, `place(id, [x, y])`.

```json
{ "kind": "vectors",
  "params": { "x": [-1, 6], "y": [-1, 5], "vectors": [{ "id": "u", "v": [3, 1], "label": "$\\mathbf{u}$" }, { "id": "v", "v": [1, 3], "label": "$\\mathbf{v}$" }] },
  "state": { "show": ["sum"], "drag": ["u", "v"] } }
```

**Integration pass 5 additions**
- Chains: a vector drawn `from` another starts at that vector's tip, its own tail included, so head-to-tail chains of any length need no derive.
- `angles: [{ id, a, b, label, right: true, radius }]`: an arc (or a right-angle square) between two arrows at `a`'s tail.
- `lines: [ids]`: each vector's span as its own band (several eigen-lines at once). `segments: [{ id, from: [x, y] | vectorId, to: [x, y] | vectorId, dashed, colour, label }]`: plain lines without heads. `head: false` on a vector drops its arrowhead.
- `lockTo: "u"` (a vector id) or `[dx, dy]` on a vector holds its dragged head to that line through the origin, for projection drags.
- `state.matrix: [[a, b], [c, d]]` or `state.transform: { angle (degrees), shear, scale }` gives the basis (its columns): the grid, `b1`, `b2` and the image of the unit square (`unitsq`) follow. Item 435: the matrix also acts on every vector, each drawn as its image (a `from: [x, y]` tail is mapped too, a chain follows its vector), so `sum`, `project`, `span`, `lines`, `angles` and `segments` that name vectors work on the images; `fixed: true` on a vector keeps it where it is (an input shown beside its image). Points and bare-coordinate segment ends are not mapped. `state.basis` alone still draws the grid and leaves vectors alone. Controls bind `m11`, `m12`, `m21`, `m22`, `angle`, `shear`, `scale`, or a derive writes `"matrix": "[[a, b], [c, d]]"` from params `a` to `d`.
- Dragging a mapped vector moves its head in the image plane and stores the preimage; a singular matrix (det 0) uses the pseudo-inverse, so the head slides along the image line. `points()` gives heads as drawn and `place(id, [x, y])` takes a drawn position.
- Derive reads (names, from `state.params`, only while a matrix is set): `matrix`, `m11`, `m12`, `m21`, `m22`, `det`, `trace`, and `image.<id>` (each vector's arrow as drawn: the matrix applied unless `fixed`, then `scale`), for example `"caption": "det = {{fixed(det, 2)}}, T u = ({{fixed(image.u[0], 2)}}, {{fixed(image.u[1], 2)}})"`.
- Default colours: a vector without `colour` takes the next slot no other vector uses, so two never share by accident. A vector added by a keyed patch gets its colour too.
- A `sumLabel` that would sit on a vector label moves below; a scaled plain-text label reads "0.6 × Equity fund".

## complex-map

A z-plane beside a w-plane showing what `w = f(z)` does to a grid, the unit circle, curves and points. Panels are side by side at 540 px and stack (one above the other) under 500 px wide; both use equal units, so angles stay true and `x`, `y`, `wx`, `wy` are minimum ranges.

**params**
- `f`: a formula in `z` (default `"z"`). Operators `+ - * /`, `^` or `**`, unary minus, implicit multiplication (`2z`, `a z`, `2(z + 1)`); constants `i`, `pi`, `e`; functions `exp`, `log` (alias `ln`, principal branch, arg in (-pi, pi]), `sqrt` (principal), `sin`, `cos`, `tan`, `sinh`, `cosh`, `tanh`, `conj`, `abs`, `arg`, `re`, `im` (the last three return a real number), `pow(a, b)`. Whole powers up to 64 use repeated multiplication. A pole or an undefined value is not drawn.
- `params: { "a": 1 }`: numbers (or `[re, im]`) usable by name in `f` and in curve formulas; state.params overrides, so controls bind them (`{ "bind": "a" }`).
- `x`, `y` (z-plane, default `[-2, 2]`), `wx`, `wy` (w-plane, default as `x`, `y`), `height` (panel height in px), `stack` (`true` or `false` forces the layout), `xLabel`, `yLabel` (default Re, Im), `zLabel`, `wLabel` (panel titles, KaTeX allowed; default "z-plane", "w-plane").
- `grid`: `"cartesian"` (default), `"polar"`, `"both"` or `"none"`; `gridStep` (default a round number giving about eight lines), `rStep` (polar circles, default `gridStep`), `rays` (polar rays, default 12); `unitCircle: true` draws |z| = 1 and its image dashed.
- `curves: [{ id, z: "formula in t", t: [from, to], colour, dashed, n }]`: any curve z(t) and its image, such as `"t + 2i"` (a line) or `"2 exp(i t)"` (a circle).
- `points: [{ id, x, y, label, imageLabel, colour, drag }]` (also in state): `x`, `y` are the real and imaginary parts of z.

**state**: `f`, `grid`, `gridStep`, `rStep`, `rays`, `unitCircle` (patchable; a frames control can switch `f`), `params` (numbers for `f`), `points` and `curves` (keyed patches by id), `hide: [ids]`, `highlight`, `caption`.

**ids**: `grid-x` (lines Re z = const), `grid-y` (Im z = const), `grid-r` (circles), `grid-th` (rays), `unit`, curve ids, point ids (z) and `<id>-image` (f(z)). A group's id lights it in both panels.

**modes**: `drag` (a point with `drag: true`, or those named by a `drag-point` widget; emits `{ type: "drag", id, x, y, phase }`) and `slider`. **methods**: `points()`, `place(id, [x, y])`, `evaluate(z)` (z an id or `[re, im]`, returns `[re, im]`), `setParam`, `getParam`.

**derive**: each point carries `u` and `v`, the real and imaginary parts of f(z) (`p1.u`, `p1.v`), for captions such as `"f(z) = {{fixed(p1.u, 2)}} + {{fixed(p1.v, 2)}}i"`.

Sampling: each curve starts with 180 to 240 samples, is subdivided where the image moves more than 9 px between samples, clipped to the panel, and broken at poles and at jumps such as the branch cut of `log`. A point whose image is outside the w-plane is drawn hollow at the edge.

```json
{ "kind": "complex-map",
  "params": { "f": "z + a/z", "params": { "a": 1 }, "x": [-2, 2], "y": [-2, 2], "wx": [-3, 3], "wy": [-3, 3], "grid": "both", "unitCircle": true, "wLabel": "$w = z + a/z$" },
  "state": { "points": [{ "id": "p1", "x": 0.8, "y": 0.6, "label": "$z$", "drag": true }] },
  "derive": { "caption": "f(z) = {{fixed(p1.u, 2)}} + {{fixed(p1.v, 2)}}i" },
  "controls": [{ "bind": "a", "min": 0.2, "max": 1.6, "step": 0.1, "start": 1, "label": "a" }] }
```

## graph

**params**
- `nodes: [{ id, label, x, y, colour }]`. `x` and `y` are fractions from 0 to 1 of the frame.
- `edges: [{ from, to, w, label, directed, dashed, bend, colour }]`. Edge ids are `e-{from}-{to}`.
- `directed: true` (params, for all edges, or per edge) draws arrowheads; without it edges are undirected (a flowchart or pipeline needs `directed: true`), `markov: true`, `nodeRadius`, `height`.
- `layout: "ring"`: the nodes sit evenly round a circle in list order (seats round a table), ignoring `x` and `y`.
- Without `nodeRadius` the radius grows to fit the longest label (22 up to 34); a label still too long shrinks (down to 10px).
- A node may carry its own `r`, `shape: "pill"` (a rounded box as wide as its label, for branch names and variable names) and `dashed: true` (for example a fetched commit not yet merged). Edges stop at each node's rim.
- Node `shape`: `"circle"` (default), `"pill"`, `"rect"` (a rounded box sized to its label; a label with `\n` takes two lines) or `"diamond"`. Labels never shrink below 12px: a long one wraps at a space onto two lines, then ends with …
- `tapEdges: true` makes edges tappable in tap mode (ids `e-from-to`); a tap-regions widget whose `among` or `only` names an edge does the same.
- `lanes: [{ "y": 0.15, "label": "origin" }, { "y": 0.85, "label": "local" }]`: labelled dotted lines behind the graph, at the same 0 to 1 heights as node `y`.
- Names and objects (aliasing, mutation): draw each name as a pill node and each object as a node, with an edge from name to object; re-point a name by patching its edge (`{ "edges": { "e-b-obj1": null, "e-b-obj2": { "from": "b", "to": "obj2" } } }`), which animates.
- `markov: true` makes edges directed and labels them with probabilities. Self-loops (`from` = `to`) point away from the graph's centre. A pair of opposite edges curves apart.

**state**
- `visited: [ids]`: order badges 1, 2, 3 and a light fill.
- `current: id`: a manipulable-blue ring.
- `distribution: { "n1": 0.5 }`: a fill bar inside each node, with the value under it.
- `show: "none"` hides the edge labels. `order: false` hides the badges.
- `labels: { "A": "Alice" }`: relabels nodes.
- `rotate: 1`: turns a ring by that many seats (fractions too); it animates.
- `nodes`, `edges`: the graph itself lives in state (seeded from params). A list replaces it; a map keyed by id merges into a node, adds one (a new id) or removes one (`null`): `{ "nodes": { "D": { "label": "D", "x": 0.8, "y": 0.2 } }, "edges": { "e-C-D": { "from": "C", "to": "D" } } }`, then `{ "nodes": { "D": null } }`. Edges of a removed node go with it. Arriving nodes and edges fade and grow in, leaving ones fade out where they were; in a ring the others slide to their new seats.
- `highlight`, `selected`.

**ids:** node ids and `e-n1-n2`. An undirected edge also answers to `e-n2-n1`.

**modes:** `tap` (on nodes) emits `{ type: "tap", id, on, selected }`.

```json
{ "kind": "graph",
  "params": { "markov": true, "nodes": [{ "id": "bull", "label": "Bull", "x": 0.2, "y": 0.5 }, { "id": "bear", "label": "Bear", "x": 0.8, "y": 0.5 }],
    "edges": [{ "from": "bull", "to": "bull", "w": 0.9 }, { "from": "bull", "to": "bear", "w": 0.1 }, { "from": "bear", "to": "bull", "w": 0.3 }, { "from": "bear", "to": "bear", "w": 0.7 }] },
  "state": { "distribution": { "bull": 0.75, "bear": 0.25 } } }
```

**Integration pass 6 additions:** an edge's `loopAngle` (degrees: 0 right, 90 up) points a self-loop that way; a node's `valueSide` (`below` default, `above`, `left`, `right`, or `state.valueSide: { id: side }`) moves its distribution value; on a column narrower than 540px the frame narrows (down to 300) instead of shrinking the drawing, so labels keep their 12px minimum on a phone (`fitWidth: false` keeps the fixed frame).

**Integration pass 7 additions**
- Edges are undirected unless `directed` is set (the line above used to say otherwise); flowcharts and pipelines need `params.directed: true`.
- The circle radius follows labels set later (`state.labels`) as well as the opening ones; the frame padding follows the nodes' own sizes, so rect and pill nodes neither waste the frame nor run off it; below 440px pill and rect labels are set at 12px.
- Edge labels may hold KaTeX (`"label": "$\\lambda$"`).
- `state.pointers: { "slow": "n2", "fast": { "at": "n4", "side": "below" } }` (or a list of `{ id, at, label, side }`) draws a labelled arrow onto a node; several on one node stack; a patch moves them (linked lists without re-pointing pills).
- `state.values: { "<node>": "17.71" }` writes a value under a node (`valueSide` moves it).
- `params.lattice: { steps: 3, S0: 100, u: 1.1, d, decimals: 2, money: "£", labels, shape, stepLabels: true | [...] }` lays out a recombining binomial lattice: nodes `n{t}_{k}` (k up moves after t steps), edges up and down, prices as labels (or `labels` by id), step labels along the bottom. Values per node come from `state.values`, so a table widget (`bind: "values.n2_1"`) or a derive can fill them.
- Not added: a side panel for auxiliary state (a heap's contents); put an `array` beside the graph in a `pair`.

## array

**params**
- `cells: [5, 2, 9]`, `indexFrom` (default 0).
- `mode`: `"array"`, `"stack"` (vertical, top marked), `"queue"` (front and back labels) or `"linked"` (boxes with next arrows ending in `null`).
- `capacity` (stack height), `showIndex`, `pointersBelow`, `topLabel`, `frontLabel`, `backLabel`, `nullLabel`, `height`.
- Cells widen to their text (a date, `102.50`) as far as the column allows, and long text shrinks to fit.

**state**
- `cells`: replaces the values.
- `pointers: [{ id, at, label, below, colour }]`. `at` is a displayed index. Pointers that share a cell fan out side by side.
- `highlight`: ids, or `{ "range": [lo, hi], "label": "..." }` for a wash behind a run of cells.
- `active: [lo, hi]` dims the cells outside it, for example in a binary search. `done: [indices]` draws those cells in slot 3, bold.
- `swap: [i, j]` (displayed indices) is an action. It animates the two cells along arcs (640 ms) and updates `cells`. In demonstrate steps, give `cells` alongside `swap` so that stepping back and forth stays correct.
- `selected`.

**ids:** `c{i}` using the displayed index (so with `indexFrom: 1` the first cell is `c1`), pointer ids, `range`.

**modes and events**
- `tap` (on cells) emits the tap payload.
- `drag` reorders cells in array and queue modes. It emits `{ type: "order", order: ["c2", "c0", ...], cells, phase: "end" }`, where `order` lists the original cell ids in their new order.

**methods:** `order()`.

```json
{ "kind": "array",
  "params": { "cells": [2, 5, 8, 12, 16, 23, 38, 56] },
  "state": { "pointers": [{ "id": "lo", "at": 0, "label": "lo" }, { "id": "mid", "at": 3, "label": "mid" }, { "id": "hi", "at": 7, "label": "hi" }], "highlight": { "range": [0, 3] } } }
```

**Integration pass 6 additions:** `wrap: 12` (or `true`) puts a long array on rows of that many cells, ranges drawn row by row.

**Integration pass 7 additions**
- Pointers are tap targets (by id) in tap mode, beside cells.
- The layout follows the current number of cells and the widest text in any state (or `params.steps`); `cellWidth` fixes the cell width.
- `state.insert: { at, value }` shifts the later cells right and fades the new one in; `state.remove: i` closes the gap (both animated).
- A cell may be `{ "v": 6, "label": "i2" }`: a small label above the value (a monotonic stack of indices and values).
- `params.steps: [state patch, ...]` with a control bound to `step` is a built-in stepper: each step applies over the opening state and the caption reads "Step k of n" (`stepCounter: false` to drop it). A `frames` control (AUTHORING section 4) does the same on any kind.
- `highlight.ranges: [[a, b], { range: [c, d], colour: 3, label: "test" }]` draws several bands at once (train, purge, test), beside `highlight.range`.
- `place` with `mode: "array"` grades the order after a drag (README.md, "Canvas-bound widgets").

## payoff

Payoff or profit and loss at expiry against the price of the underlying.

**params**
- `legs: [{ id, type: "call"|"put"|"stock", side: "long"|"short", strike, premium, qty, label, colour, strikeLabel }]`. For `stock`, `strike` is the entry price.
- `range: [min, max]`.
- `pl` (default true) subtracts premiums for long legs and adds them for short legs.
- `y`, `yLabel`, `xLabel`, `label` (the combined line's label), `spotLabel`, `snap` (strike drag step, default 1), `drag` (leg ids), `height`.
- `value: { t: 0.25, sigma: 0.2, r: 0, label }` (params or state): the position's value before expiry (Black-Scholes, `t` years left), a smooth curve over the payoff; patch `t` towards 0 and it settles onto the payoff. `tangent: true` (or `{ at: S, label: "delta {delta}", labelOffset }`) draws the tangent to that curve at the spot, labelled with its slope, delta.

**Drawing**
- The combined line is bold, slot 1. With more than one leg, each leg is drawn faint and dashed in its own slot.
- Strikes get ticks, and each kink is labelled `K = 100`.
- Breakevens (P&L only) are hollow markers on the zero line with their value.
- The spot marker shows `S = 104, P&L 1`.

**state**
- `strike: { "c1": 105 }` and `premium: { "c1": 3 }` (both animate).
- `spot`.
- `pl`: true or false.
- `showLegs`, `kinkLabels: false`, `breakeven: false`, `spotValue: false`, `highlight`.
- `params: { "c1": 105, "spot": 104 }` is a slider shortcut.

**ids:** leg ids (with one leg, the single line takes the leg id), `total` (the combined line, with several legs), `strike-{legId}`, `breakeven`, `spot`.

**modes:** `drag` (diamond handles at the strikes) emits `{ type: "drag", id, strike, x, y: 0, phase }`. `slider` (bind `strike.c1`) and `tap` are also supported. **methods:** `value(S)`, `breakevens()`, `points()`, `place(id, strike)`.

```json
{ "kind": "payoff",
  "params": { "legs": [{ "id": "c1", "type": "call", "side": "long", "strike": 95, "premium": 7, "label": "long 95 call" }, { "id": "c2", "type": "call", "side": "short", "strike": 105, "premium": 2.5, "label": "short 105 call" }], "range": [80, 120], "label": "bull spread" },
  "state": { "spot": 102 } }
```

**Integration pass 6 additions**
- Tap targets: `strike-<leg id>` (the strike tick and kink), `breakeven` (`breakeven2`, … when there are several), each leg's line, and `total` when the combined line shows.
- `drag: "spot"` (or a drag-point widget naming `spot`) makes the spot a handle on the axis; `points()` and `place("spot", x)` include it.
- `showTotal: false` hides the combined line and draws each leg solid; a leg's `labelAt` (0 to 1 along the price range) places its label; `floor: false` on a leg drops its floor (the "forgot the right not to exercise" line).

**Integration pass 7 additions**
- Legs live in state: `state.legs` replaces them, or a map by id merges, adds or removes (`null`) one; `qty: 0` hides a leg. A `place` token's `onPlace` patch can add a leg, so dropping legs builds the position.
- A cash leg: `{ "type": "cash", "amount": 100 }` (a flat line; short it for a loan).
- Stock (or `"forward"`) legs mark their entry price on the axis ("F = 100", or their `strikeLabel`), and are dragged when `params.drag` (or a drag-point widget) names them.
- `value` may be a list of curves (`[{ "t": 0.5, "sigma": 0.2, "label": "σ = 20%" }, { "t": 0.5, "sigma": 0.4, "label": "σ = 40%" }]`), each with its own label, colour and `labelAt`; the tangent follows the first.
- Per-leg label positions were already `labelAt` (pass 6).

## orderbook

**params**
- `bids: [[price, size]]` and `asks: [[price, size]]`, in any order; they are sorted.
- `depth`: levels shown on each side.
- `dp`: price decimals. Inferred if omitted.
- `currency`, `bidLabel`, `askLabel`, `spreadLabel`, `showMid`. `spreadValue: false` keeps the spread row's label but hides the number, for the learner to work out.
- The ladder has three columns: bid size bars on the left (green side), the price, and ask size bars on the right (red side). Asks sit above the spread row and bids below it. The best levels are bold.

**state**
- `order: { side: "buy"|"sell", size }`: a market order. It walks the book level by level (about 420 ms per level).
  - The current level is washed. Consumed size turns manipulable blue. Each level shows "bought 200" or "sold 200".
  - The footer shows the remaining size during the walk, then the result, for example "Bought 750 at average 100.01".
- `fills: false` hides the per-level labels.
- `highlight`, `selected`.

**ids:** `bid{i}` and `ask{i}` (0 is the best level), `spread`, `order`.

**modes:** `tap` (on levels). **methods:** `walk(order)` returns `{ fills: [{ id, price, qty }], filled, left, cost }`. `spread()`.

```json
{ "kind": "orderbook",
  "params": { "bids": [[99.98, 300], [99.97, 500], [99.96, 200]], "asks": [[100.00, 200], [100.01, 400], [100.02, 300]] },
  "state": { "order": { "side": "buy", "size": 750 } } }
```

---

**Integration pass 7 additions**
- `bids` and `asks` live in state, seeded from params: a list replaces a side; a map keyed by price sets a size (`{ "100.5": 300 }`), adds a level or removes one (`null`); a map keyed by level index patches a level (`{ "0": { "1": 350 } }`, which a control bound to `bids.0.1` writes). A level's third entry is a label (`[100.5, 300, "#17"]`, an order id), shown beside its size. Give `depth` to reserve rows for levels that arrive.
- `state.quotes: { "bid": [p, s], "ask": [p, s] }` merges the learner's own quotes into the book, labelled "You" (`youLabel`), in the manipulable colour; `state.fair` (or `params.fair`) adds a fair value to the spread row, so sliders on fair, half-spread and skew (with a derive writing `quotes`) move the learner's quotes in the book.
- `decimals` for the average fill price, `midDecimals` for the mid (default: one more place when the mid falls between ticks), `spreadUnit: "pence" | "bp"` for the spread.

**The `trade` widget over an orderbook (item 459).** The market-making game (AUTHORING section 3, `trade`) drives this canvas through `state.quotes` (`{ bid: [price, room-trimmed size], ask: [...] }`, drawn as "You" rows in the manipulable colour; a side with no room, or the whole pair once the game is over, shows no row) and `state.fair` (the current mark, which a card's `fair` moves and a `reveal` card sets to the hidden value). Give the canvas `depth` and a background book (`bids`, `asks`, `currency`, `dp`, `showMid`) for context: the game never changes those. The learner's quote is updated on every stepper change, so the book shows where the quote sits against the market before it is sent.

## space

A rotatable 3D view in plain SVG: axes, a box and grid, points, vectors, curves, polylines, surfaces, planes and spans, and a vector field. Orthographic by default. Drawn with a painter's algorithm (far pieces first), so a vector through a surface, a curve over a surface or a plane cutting a bowl all read correctly. Built on `ZQ.cvb`; code in `space.js`.

**Camera**
- `params.camera: { az, el, zoom }` is the opening view: azimuth and elevation in degrees (z is up; az -60, el 25 by default; el stays within -89 and 89), zoom 0.4 to 3. `state.camera` patches it and tweens. `params.perspective` (0 to 1, default 0) adds weak perspective; patchable as `state.perspective`.
- Drag (mouse, pen or touch) rotates: right and left turn the azimuth, down and up the elevation. A drag starts after 5 px, so a tap on a target still taps. Two fingers pinch-zoom. With the picture focused: arrow keys rotate 5 degrees (Shift 15), `+` and `-` zoom, `0` or Home resets. A "Reset view" button (off with `resetButton: false`) animates back to the first-drawn camera. Controls may bind `az`, `el` and `zoom`.
- `touchScroll: true` lets a vertical touch scroll the page (touch then turns the azimuth only). Otherwise a finger on the picture never scrolls.
- The svg has `role="group"`, an `aria-label` made from `params.aria` plus the object names and the key help, and a polite live region that reads the angles after a key press.

**params**
- `x`, `y`, `z`: ranges `[min, max]` (default -5 to 5 each). `equal: true` keeps equal units on all three axes (use it when perpendicular must look perpendicular); `aspect: [a, b, c]` sets the box proportions; otherwise the box is a cube whatever the ranges. `height` 240 to 640 (default 420; the width is 540 like the other canvases).
- `axes`, `ticks`, `box` (true by default; patchable, and `state.hide: ["axes", "ticks", "box", "grid"]` hides them), `grid: "back"` (default: a faint grid on the three faces turned away from you), `"floor"` or `false`, `axisLabels: ["$x$", "$y$", "$z$"]`.
- `params: { "a": 1 }`: numbers usable in every formula; `state.params` overrides them, and a bound slider writes there.
- The lists below, each an array of objects with an `id`. Each is also patchable by id from state (`{ "vectors": { "u": { "v": [1, 2, 3] } } }`; a new id adds, `null` removes). Items may be `hidden: true` and revealed with `state.show: ["id"]`, or hidden with `state.hide`. Colour is `colour: 1..6`; unset items take the first free slot (a plane takes the colour of the first vector in its span).

**Formulas** are curve formulas as in `plane` (`^` is a power, `-x^2` is -(x^2), `pi`, `e`, `sin`, `exp`, `sqrt`, `sum(k, 0, n, term)` ...). A coordinate may be a number or a formula string (`"v": ["a", "b", "a + b"]`). The variable is `t` in a curve, `x` and `y` in `z = f(x, y)`, `u` and `v` in a parametric surface, `x`, `y`, `z` in a field; every name in `params.params` is available everywhere.

**Lists**
- `points: [{ id, p: [x, y, z], label, labelPos, open, drop, r, colour }]`. `x`, `y`, `z` may replace `p`. `on: "s"` takes z from surface `s` (give x and y); `at: "r", t: 1.5` rides curve `r` at parameter `t` (a number or a formula such as `"t0"`). `drop: true` adds a dashed line to the floor. `labelPos` is a compass point (default `ne`).
- `vectors: [{ id, v: [dx, dy, dz], from, label, labelPos, dashed, head, drop, colour }]`. `from` is `[x, y, z]`, a point id, or another vector's id (the arrow starts at that vector's tip, so chains work to any depth). `labelPos: "end"` (default) or `"mid"`. `head: false` draws a plain segment.
- `curves: [{ id, x, y, z, t: [from, to], n, label, labelAt, dashed, width, colour }]`: r(t) = (x(t), y(t), z(t)); `z` defaults to 0. The `t` ends may be formulas (`[0, "T"]`), so a slider grows the curve. `n` samples, 8 to 600 (default 160). `labelAt` is a `t`. `width: "bold"`.
- `lines: [{ id, pts: [[x, y, z], ...], closed, dashed, label, colour }]`: a polyline through given points.
- `surfaces: [{ id, z: "x^2 - y^2", x: [lo, hi], y: [lo, hi], n, ... }]` is z = f(x, y) over the given ranges (default: the box). `{ id, x: "...", y: "...", z: "...", u: [a, b], v: [c, d], n }` is parametric (a sphere is `1.5*sin(u)*cos(v)`, `1.5*sin(u)*sin(v)`, `1.5*cos(u)`). `n` is cells each way, 2 to 40 (default 24; `[nu, nv]` too). `shade: "light"` (default), `"flat"`, or `"height"` (colour runs from `colour` to `colour2` with z). `wire: true` draws the cell edges over the shading; `wire: "only"` is a hidden-line wireframe. `opacity` 0.05 to 1. `clip: "clamp"` (default for z = f: a surface leaving the box is cut flat at the top and bottom), `"drop"` (cells with a corner outside are dropped) or `"none"` (default for parametric). `label` sits at the highest point of the surface on screen (or at `labelAt: [x, y]`).
- `planes: [{ id, span: ["u", "v"], through, ... }]`: the plane spanned by two vectors (ids of vectors on this canvas, or `[x, y, z]`), through the origin or `through: [x, y, z]`, clipped to the box. One vector gives a line. Or `normal: [a, b, c]` with `through` (a point on it) or `d` (the plane `n . p = d`). `extent: [lo, hi]` (or `[a0, a1, b0, b1]`) draws a finite parallelogram patch of a span instead (`a u + b v` with the coefficients in the range). `res` cells each way, 3 to 24 (default 10). `opacity` (default 0.22). `labelAt: [x, y, z]`.
- `fields: [{ id, F: ["-y", "x", "0.3"], n: 5, normalise, scale, at, label, colour }]`: an arrow F(x, y, z) at each point of an n by n by n grid (1 to 7 each way, or `[nx, ny, nz]` up to 9, capped at 343 arrows). Lengths follow the size of F (the longest is 0.9 of a grid cell); `normalise: true` makes them equal; `scale` multiplies them. `n: [6, 6, 1]` with `at: [0, 0, 1]` is a flat slice at z = 1.

**state**
- `camera`, `perspective`, `params`, every list (patchable by id), `show`, `hide`, `highlight`, `caption`, `selected`.
- Object ids are the item ids; `highlight` glows every piece of the object, `mark` recolours it (graded classes, no badge).

**modes:** `tap` (every object is one target; a dot or arrow on a surface wins over the surface; tap-regions `answer` and `among` name item ids; emits `{ type: "tap", id, on, selected }`), `slider`. Rotation works without `enable` (and is off in a still copy: the Why? sheet, `clone`).
**events:** `change` with `{ type: "rotate", az, el, zoom, end }` on every rotation frame (`end: true` on release, a key press or reset). **methods:** `setParam(name, v)` (`az`, `el`, `zoom`, a dotted state path, or a param), `getParam(name)`, `camera()` (`{ az, el, zoom }`), `reset()`, `project(x, y, z)` (a data point's position in the 540-wide drawing: `{ x, y, depth }`), `values()`.

**derive:** items are read by id (`u.v`, `P.p`, `s.z`, `camera.az`) and written like any list (`"w.v.2": "a * 2"`). `values.P` is a point's resolved `[x, y, z]` (a point `on` a surface or `at` a curve included) and `values.u` a vector's tip: `"caption": "P is at height {{round(values.P[2], 2)}}"`.

**Limits:** the cells of all surfaces and planes together are held near 1,600 (every `n` is scaled down together above that), fields at 343 arrows, curves at 600 samples. Typical scenes redraw in under 10 ms; keep a phone in mind before asking for 40 by 40 and a wire.

```json
{ "kind": "space",
  "params": { "x": [-4, 4], "y": [-4, 4], "z": [-4, 4], "equal": true, "camera": { "az": -55, "el": 24 },
    "vectors": [{ "id": "u", "v": [3, 0, 1], "label": "$\\mathbf{u}$" }, { "id": "v", "v": [0, 3, 2], "label": "$\\mathbf{v}$" }],
    "planes": [{ "id": "cs", "span": ["u", "v"], "label": "column space" }] } }
```

## interleave

Threads as lanes of numbered steps over shared variables (item 471, E13). The learner taps a lane's **Step** button to run its next step, so any interleaving can be walked by hand. A lane whose next step is a lock another lane holds is disabled and drawn blocked; a wait sleeps until a notify that comes after it. When no lane can step the schedule ends: `complete`, `deadlock` or `asleep`. The same rules, run over every legal schedule (a memoised walk over states, cached per spec), give `values.outcomes`, so "162 of 168" is read from the canvas and never typed. HTML in the canvas wrapper, like `table`; readable at 390 px (three lanes sit side by side at about 110 px each) and in both themes.

**params**
- `lanes` (1 to 3, at most 8 steps a lane and 24 in all): `[{ "id": "a", "label": "Thread A", "short": "A", "steps": [...], "regs": { "r": 0 } }]`. `id` defaults to a, b, c; `label` to `Thread A`; `short` (on the Step button and in messages) to the id in capitals. `regs` are starting register values (a register not set reads 0).
- `vars`: shared variables and their starting numbers, `{ "x": 0 }` (alias `shared`). Names may not be `outcomes`, `outcomeList`, `schedules`, `complete`, `deadlock`, `asleep`, `ending`, `outcome`, `done`, `steps`, `remaining`, `order`, `reached`, `reachedList` or `regs` (they are keys of `values()`).
- `locks`: optional list of lock names. Every `lock` named in a step is found anyway; a declared list makes the validator reject a misspelt one.
- `outcome`: what makes two finished schedules the same outcome. A list of shared variable names, `"a.r1"` (register `r1` of lane `a`) or `{ "label": "r1", "of": "a.r1" }`. Default: every shared variable in `vars` order. `[]` means "complete" is the only finished outcome (a program with nothing to read, such as a lock ordering).
- `endings`: renames the end states in `values.outcomes`, `{ "complete": "awake", "asleep": "asleep forever" }` (keys `complete`, `deadlock`, `asleep`). A complete outcome that has values is named by them (`"x=1"`), so `endings.complete` only applies with `outcome: []`.
- `notation`: `"words"` (default: `load r from x`, `add r 10`, `store x from r`) or `"assign"` (`r = x`, `r += 10`, `x = r`, `x = 1`). A step's own `text` overrides both.
- `label`: accessible name of the lanes.

**A step** is one numbered operation, drawn as a row `a1 load r from x`. Its id is `id` if given, else the lane id plus its number (`a1`, `a2`), or lane id, a hyphen and the number when the lane id ends in a digit (`t1-1`, `t1-2`). A step is a single op written in place, or `ops: [...]` (several ops that run as one indivisible step, with `text` to say what it is):

| op | fields | does |
|---|---|---|
| `load` | `reg`, `var` | register = shared variable |
| `add` | `reg`, `by` | register += `by` (a number, or an expression over registers) |
| `store` | `var`, and `reg` (the register to store) or `value` (a number or an expression such as `"r - 80"`) | shared variable = ... |
| `set` | `reg`, `value` | register = an expression such as `"r >= 80"` or `"q == 0"` (a comparison gives true or false) |
| `fetch-add` | `var`, `by` (default 1), optional `reg` | atomic: shared variable += `by`, the old value into `reg` |
| `lock`, `unlock` | `lock` | the lane is blocked while another lane (or itself) holds the lock; `unlock` frees a lock the lane holds |
| `wait` | optional `lock` | the lane sleeps until a later `notify`; `lock` is released as it falls asleep. On waking the lane carries on with its next step and does not take the lock again (write a `lock` step if it should) |
| `notify` | none | wakes every sleeping lane (so a notify that runs before the wait wakes nobody: the lost wakeup) |

Any op may carry `if`: an expression over the lane's registers and the shared variables (`+ - * / %`, `< <= > >= == !=`, `&& || !`, `min max abs`, `true false`). The op does nothing when it is false. That is the **conditional step**: `{ "op": "store", "var": "bal", "value": "r - 80", "if": "ok" }` is "if ok: store". A lock step with `if` blocks only when the condition holds; a `wait` with `if` sleeps only then (U11: the consumer waits only if it saw an empty queue). A register shadows a shared variable of the same name.

**Ends.** A schedule ends when no lane can step. `complete`: every lane ran out and none sleeps. `deadlock`: some lane is blocked on a held lock. `asleep` (shown "asleep forever"): the only lanes left are asleep. The ending text names who waits for what.

**state**
- `schedule`: the lane ids stepped so far, `["a", "b", "a"]`. This is the whole state: tapping a Step button appends to it, Undo removes the last, Reset empties it. A patch replaces it, so `explain.canvas`, `demonstrate.steps[].canvas` and `enter` can show any interleaving (`{ "schedule": ["a", "b", "a", "b", "a", "b"] }`). An entry that cannot run (a blocked, sleeping or finished lane) ends the replay there and the validator rejects it.
- `outcomes`: `true` shows a table of every outcome with its schedule count (the current schedule's row is washed); `"found"` lists only the outcomes the learner has finished at ("Outcomes found: 2 of 3"), with no counts; `false` (default) hides it.
- `selected`, `highlight`, `caption`: as everywhere.

**ids** (tap mode, `highlight`, `mark`): every step id (`a1`, `t1-2`, or the step's own `id`); `lane-<id>`; `var-<name>` and `lock-<name>` for the shared chips. Only steps are tappable: `tap-regions` marks steps, and the Step buttons keep working in tap mode. **events:** `change` with `{ type: "step", lane, schedule, ending, outcome }` after a Step, Undo or Reset (`ending` is `running` until the schedule ends).

**derive and widgets.** `values()` gives derive and captions:
- each shared variable's current value (`values.x`), `values.ending` (`running`, `complete`, `deadlock`, `asleep`), `values.done` (1 once the schedule has ended, however it ended), `values.steps`, `values.remaining`, `values.order` (`"a1 b1 a2"`), `values.outcome` (the key of the finished outcome, else `""`), `values.regs.a.r` (a lane's register);
- `values.outcomes`: `{ "x=1": 18, "x=2": 2 }`, read as `values.outcomes["x=1"]`; the end states appear as `complete`, `deadlock` and `asleep` (or their `endings` names). `values.outcomeList`: `[{ key, count, ending }]` (complete outcomes first, then deadlock, then asleep). `values.schedules` is the total, and `values.complete`, `values.deadlock` and `values.asleep` count schedules by how they ended (0 when none). These are `undefined` (and a rule that reads them waits) when the spec has more than 200,000 states, which the validator rejects;
- `values.reached` and `values.reachedList`: the outcomes the learner has finished at on this canvas (kept across Reset).

`tap-regions` marks steps (`answer: ["a1", "b1"]`). `numeric`, `choice` and the other widgets sit beside the canvas as usual. No widget grades the schedule itself: ask what the learner can compute from it (a count, a final value, a marked step).

**methods** (the test hook, screenshots): `step(laneId)` (false when the lane cannot step), `play(["a", "b", ...])` (replaces the schedule, stops at the first entry that cannot run, returns the ending), `finish(pick?)` (steps the first enabled lane until the end, or the lane `pick(enabledIds)` returns), `undo()`, `reset()`, `enabled()` (the lane ids that can step), `ending()`, `outcomes()` (the enumeration: `{ outcomes, list, schedules, complete, deadlock, asleep }`).

**Validator.** `params.lanes` (1 to 3, 8 steps a lane, 24 in all), step and lane ids unique, `op` known, required fields per op, every name in an `if`, `by` or `value` expression a shared variable or a register the lane sets, every variable in `vars`, `lock` in `locks` when `locks` is given, reserved variable names, `outcome` entries that exist, `endings` keys, `state.schedule` that replays legally (also in `enter`), `state.outcomes`, and an enumeration under 200,000 states. A warning for an `unlock` with no earlier `lock` in the lane.

**Not supported (by design):** a store buffer for weak memory (the (0, 0) outcome of the store-buffering test stays a `choice`); `notify_one` (a notify wakes every sleeper); a lane that re-takes its lock on waking; more than three lanes.

Worked examples, one per acceptance criterion. Every count in them is reproduced by the canvas.

A lost update (U2: 20 schedules, 18 end at 1 and 2 at 2):

```json
{ "kind": "interleave",
  "params": { "vars": { "x": 0 }, "lanes": [
    { "id": "a", "steps": [{ "op": "load", "reg": "r", "var": "x" }, { "op": "add", "reg": "r", "by": 1 }, { "op": "store", "var": "x", "reg": "r" }] },
    { "id": "b", "steps": [{ "op": "load", "reg": "r", "var": "x" }, { "op": "add", "reg": "r", "by": 1 }, { "op": "store", "var": "x", "reg": "r" }] }] },
  "state": { "outcomes": true },
  "derive": { "caption": "{{values.outcomes['x=1']}} of {{values.schedules}} end at 1." } }
```

Pair it with `{ "kind": "tap-regions", "answer": ["a1", "b1"] }` ("tap the two steps that read the old value"). Stepping a, b, a, b, a, b ends at x = 1.

A deadlock (U6: complete 4, deadlock 2 of 6). The step ids are `t1-1` to `t1-4`:

```json
{ "kind": "interleave",
  "params": { "lanes": [
    { "id": "t1", "label": "T1", "steps": [{ "op": "lock", "lock": "A" }, { "op": "lock", "lock": "B" }, { "op": "unlock", "lock": "B" }, { "op": "unlock", "lock": "A" }] },
    { "id": "t2", "label": "T2", "steps": [{ "op": "lock", "lock": "B" }, { "op": "lock", "lock": "A" }, { "op": "unlock", "lock": "A" }, { "op": "unlock", "lock": "B" }] }] },
  "state": { "schedule": ["t1", "t2"], "outcomes": true } }
```

After `t1, t2` both lanes are blocked and the canvas ends "Deadlock: no lane can step. T1 waits for B (held by T2); T2 waits for A (held by T1)." `values.outcomes` is `{ "complete": 4, "deadlock": 2 }`. A ring of three lanes (A,B), (B,C), (C,A) gives `{ "complete": 162, "deadlock": 6 }` and breaking it (the third lane takes A then C) `{ "complete": 142 }`.

An asleep-forever wait (U11: awake 5, asleep 1 of 6). The consumer checks, then waits only if the queue was empty; the order c, p, p, c loses the wakeup:

```json
{ "kind": "interleave",
  "params": { "vars": { "q": 0 }, "outcome": [], "endings": { "complete": "awake", "asleep": "asleep forever" }, "lanes": [
    { "id": "c", "label": "Consumer", "steps": [{ "op": "set", "reg": "e", "value": "q == 0", "text": "check: queue empty?" }, { "op": "wait", "if": "e" }] },
    { "id": "p", "label": "Producer", "steps": [{ "op": "fetch-add", "var": "q", "by": 1, "text": "push" }, { "op": "notify" }] }] },
  "state": { "schedule": ["c", "p", "p", "c"] } }
```

`values.outcomes` is `{ "awake": 5, "asleep forever": 1 }`. The fix (lock held across check and wait, `wait` with `"lock": "m"`) has 5 schedules and none asleep.

A conditional step (U4: two withdrawals of 80 from 100; (bal 20, cash 80) 2 and (bal 20, cash 160) 4 of 6):

```json
{ "kind": "interleave",
  "params": { "vars": { "bal": 100, "cash": 0 }, "outcome": ["bal", "cash"], "lanes": [
    { "id": "a", "label": "Withdrawal A", "steps": [
      { "ops": [{ "op": "load", "reg": "r", "var": "bal" }, { "op": "set", "reg": "ok", "value": "r >= 80" }], "text": "check: balance at least 80" },
      { "ops": [{ "op": "store", "var": "bal", "value": "r - 80", "if": "ok" }, { "op": "fetch-add", "var": "cash", "by": 80, "if": "ok" }], "text": "if ok: store r - 80, cash out 80" }] },
    { "id": "b", "label": "Withdrawal B", "steps": [
      { "ops": [{ "op": "load", "reg": "r", "var": "bal" }, { "op": "set", "reg": "ok", "value": "r >= 80" }], "text": "check: balance at least 80" },
      { "ops": [{ "op": "store", "var": "bal", "value": "r - 80", "if": "ok" }, { "op": "fetch-add", "var": "cash", "by": 80, "if": "ok" }], "text": "if ok: store r - 80, cash out 80" }] }] } }
```

Outcomes enumeration (U3: three lanes of the lost-update program, 1,680 schedules: `x=1` 1,404, `x=2` 270, `x=3` 6). `"outcomes": true` draws the table, and a caption reads it: `"{{values.outcomes['x=3']}} of {{values.schedules}} end at 3."`. Registers can be outcomes too (the store-buffering test, U9): `"outcome": [{ "label": "r1", "of": "a.r1" }, { "label": "r2", "of": "b.r2" }]` gives `{ "r1=0, r2=1": 1, "r1=1, r2=0": 1, "r1=1, r2=1": 4 }`.

The gallery (`#system`) shows the canvas with a lost update, a deadlock, an asleep-forever wait, conditional steps and a three-lane enumeration. The engine sample `content/exams/mock-interleave-sample.json` (`"sample": true`, used by no course) plays all five.

## Widget: slider

```json
{ "kind": "slider", "min": 0, "max": 1, "step": 0.05, "start": 0.3, "bind": "p", "label": "$p$", "unitLabel": "",
  "answer": 0.5, "tol": 0.02, "wrong": [{ "id": "low", "from": 0, "to": 0.45 }] }
```

**Binding**
- `bind: "p"` sets `state.params.p` on every input, live and untweened.
- A dotted bind sets a state path. `"strike.c1"` sets `state.strike.c1` on a payoff. `"window.to"` sets a series window end.

**Display and keys**
- `unitLabel`: `%` is a suffix, `£`, `$` and `€` are prefixes, and a word is a suffix after a space.
- `format: "fraction"` writes the value as a fraction in lowest terms (0.375 reads 3/8), `format: "percent"` as a percentage (0.375 reads 37.5%), on the thumb and at the ends.
- The label sits on its own row above the value bubble, so the bubble never covers it at the left end.
- Snap ticks show when there are 20 steps or fewer.
- Arrow keys step; Shift+arrow steps ten times.

**Grading**
- `grade()`: `ok` when |value − answer| ≤ `tol`. `key` is the first `wrong[]` range (inclusive) that holds the value, else null.
- Without `answer` it is an explore control and `grade()` is always ok. The player renders `canvas.controls` entries as plain range inputs with the same binding rules (a canvas `setParam` wins when the kind has one), the same `format`, and `start`: given, the control opens there and applies it to the canvas; left out, it opens at the bound value's current value (`state.params`, `params.params` or the dotted state path), else at `min`.
- `reveal()` animates the thumb and the bound canvas to the answer over 600 ms, in hint indigo.

## Widget: sliders

Two or more sliders graded together (`sliders: [{ id, bind, min, max, step, start, label }]`, then `answer: { a, b }` with `tol`, or `check: "a * b"`, `value`, `tol` and `show`). Each drives its `bind` as a plain slider does; the full spec is in AUTHORING.md section 3. Explore controls (`canvas.controls`) also take `scale: "log"` (powers of ten from `min`, `perDecade` stops between, the readout in units).

## Widget: sketch

```json
{ "kind": "sketch", "control": 5, "target": "max(x - 100, 0)", "xRange": [80, 120], "band": 2,
  "wrong": [{ "id": "linear", "expr": "0.5*(x - 80)", "band": 2 }] }
```

**Setup**
- Needs a `plane` canvas. It calls `canvas.enable('sketch', ...)`.
- It places `control` points evenly across `xRange`. They start at `start` (default 0, or the middle of the y range).

**Grading**
- `grade()` samples 20 x values across `xRange`, both ends included. `ok` when every sample is within `band` of the target.
- `key` is the first `wrong[]` entry whose expression the whole curve matches within its band, else null.
- `detail` holds `{ worstX, worstError, errors }`.

**Feedback**
- `markGraded` recolours the curve.
- `showWhy()` highlights the span between control points with the worst error.
- `reveal()` moves the points onto the target and shows the dashed target. `answer()` (the test hook's correct answer) puts the same points on the target curve, so a sketch whose reveal leaves the band also fails the playthrough.

**Advice for authors:** use at least 5 control points for a kinked target. A smooth curve through 4 points cannot follow a kink within a small band.

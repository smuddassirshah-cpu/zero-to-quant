# Canvases B: plane, bars, distribution, scatter, series, walk, matrix, vectors, graph, array, payoff, orderbook

Authors write `canvas: { "kind", "params", "state", "controls" }` (AUTHORING.md section 4). This file gives, per kind, the exact params, state keys, highlightable ids and the `change` events each one emits, with one JSON example each. It also covers the `slider` and `sketch` widgets.

## Rules shared by every kind

- **Params fix the drawing; state is what changes.** `state` is merged with `ZQ.canvas.merge` (objects merge, arrays replace) and animated over 480 to 800 ms (ease-morph) unless the change is instant or the learner has reduced motion on. Numbers tween, so positions, bar heights, slopes, parameters and curves morph. Discrete things (run counters, swaps, fills) have their own animations, described per kind.
- **`state.highlight: [ids]`** puts a pear wash and a 2 px ink ring on the named elements. Hint rung 2 calls `canvas.highlight(ids)`, which pulses twice; `highlight(null, false)` clears everything.
- **`state.caption: "text"`** shows under the drawing. It may contain `$...$` maths.
- **Labels.** A label string with no `$` is plain text. A label that is entirely `$...$` is KaTeX. Mixed text and maths (`"slope of $f$"`) also works.
- **Series colours.** Series take slots 1 to 6 in order. Set `colour: 1..6` on a series, function, vector or leg to pick a slot. Learner-movable things are always manipulable blue.
- **Linked state (`derive`).** Any canvas may carry `"derive": { "<target>": "<expression>" }` beside `params` and `state`. After every change (a patch, a drag, a control) each target is set from its expression: `"p2.x": "0.8 * p1.x"` (an item's property, by id), `"values.7": "10 - values['3']"` (bars), `"params.b": "2 * a"`, `"caption": "Change: {{round((p1.x / 50 - 1) * 100, 1)}}%"` (a string fills each `{{expression}}`). Expressions see item ids (`p1.x`), param names, top-level numbers (`angle`, `ran`) and `values` (bar heights by label and id). The function set: `abs min max sqrt pow floor ceil sign hypot`, `round(v, places)`, `exp`, `log` and `ln` (natural), `log10`, `sin cos tan asin acos atan atan2` (radians), the constants `pi` and `e`, and for text `fixed(v, places)` and `money(v, symbol, places)`. `=` and `;` may appear only inside quoted strings. Rules run up to three passes, so a caption may read a value another rule derives. `fixed(3.5, 2)` is "3.50"; `money(1234.5)` is "£1,234.50" (`money(v, "$")` for dollars); negative numbers, in captions and from these helpers, print with the minus sign −; `(expr).toFixed(2)` and ternaries (`p1.x > 3 ? "high" : "low"`) work as in JavaScript. A plane explore screen often pairs points with `drag: true` and a `derive` caption: the validator accepts that as the screen's interaction. It is engine-wide (`ZQ.canvas.create`), so it works on number-line, plane, bars and every other kind, runs again in the Why? copy on the explained state, and on a `pair` reads both sides (README.md, "pair").
- **Keyed list patches.** Lists with ids (`points`, `vectors`, `segments`, `markers`, `pointers`) can be patched by id: `{ "points": { "p1": { "x": 2 } } }` changes only `p1`. Sending an array replaces the whole list.
- **`state.params` overrides params.** In `plane` and `distribution` it overrides the expression or family parameters (`params.params`). In `walk` it overrides top-level numbers (`p`, `mu`, `sigma`, `steps`, `paths`, `start`). This is what a bound slider writes.
- **Interactive modes.** A widget calls `canvas.enable(mode, opts)`. The modes each kind supports are listed below. Elements the author marks as movable (`"drag": true` on a plane point, `state.drag` on vectors) move without `enable`. Clones made for the Why? modal are always static.
- **Events.** `canvas.on('change', fn)` receives one of these payloads. Drags emit on every pointer frame with `phase: "move"`, then once with `phase: "end"`. Arrow keys move a focused handle (Shift moves ten steps).
  - drag: `{ type: "drag", id, x, y, phase }`, in data units.
  - tap: `{ type: "tap", id, on, selected: [ids] }`. Space toggles and the arrow keys move focus between targets.
  - Kind-specific payloads are listed under each kind.
- **Shared methods** (see `_base.js` header): `mark(ids, cls, on)`, `unmark(cls?)`, `flash(ids)`, `unflash()`, `lock(on)`, `caption(text)`, `clone(host)`, `destroy()`. Drag kinds also have `points()` returning `{ id: { x, y } }` and `place(id, pos, { instant })`.
- **Grading classes.** `is-correct`, `is-notyet`, `is-reveal` and `is-dim` go on `.cv-obj` groups through `mark()` and survive redraws. Lines inside a marked group recolour; series are never marked by the engine.

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
- `state.matrix: [[a, b], [c, d]]` or `state.transform: { angle (degrees), shear, scale }` gives the basis (its columns): the grid, `b1`, `b2` and the image of the unit square (`unitsq`) follow. Controls bind `m11`, `m12`, `m21`, `m22`, `angle`, `shear`, `scale`.
- Default colours: a vector without `colour` takes the next slot no other vector uses, so two never share by accident. A vector added by a keyed patch gets its colour too.
- A `sumLabel` that would sit on a vector label moves below; a scaled plain-text label reads "0.6 × Equity fund".

## graph

**params**
- `nodes: [{ id, label, x, y, colour }]`. `x` and `y` are fractions from 0 to 1 of the frame.
- `edges: [{ from, to, w, label, directed, dashed, bend, colour }]`. Edge ids are `e-{from}-{to}`.
- `directed` (the default for all edges), `markov: true`, `nodeRadius`, `height`.
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

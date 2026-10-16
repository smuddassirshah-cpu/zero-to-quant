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

**state**
- `points: [{ id, x, y, drag, snap, snapX, on: "f", lockX, lockY, label, labelPos: "ne"|"n"|..., colour, open }]`.
  - `on` keeps a dragged point on function `f`, inside f's `domain`.
  - `label` may contain `{x}` and `{y}`, which are filled with the current coordinates.
- `segments: [{ id, from: [x, y] | pointId, to, dashed, arrow, label, labelOffset: [dx, dy], colour }]`. The label sits at the midpoint, nudged by `labelOffset` (default 8 right, 10 up; a negative dx anchors it at its end).
- `polygons: [{ id, points: [[x, y] | pointId, ...], colour, label, vertexLabels: ["A", "B", "C"], dashed }]`: a filled shape (a light series wash) with its vertices labelled just outside it.
- `angles: [{ id, at, from, to, label, right, radius }]`: an arc between the rays at → from and at → to (the smaller angle), or a square mark with `right: true`; the label sits on the bisector; `radius` in px (default 22).
- `tangent: { f, x: number | pointId, label: "slope" | "text {slope}", length, lengthPx, side, dashed }`. It can also be an array of these. `length` is in x units, `lengthPx` in pixels along the line. At a corner (the one-sided slopes differ, as on `abs(x)` at 0) no tangent is drawn unless `side: "left"` or `"right"` picks one.
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

## bars

Bar chart or histogram. It can draw dashed exact-value lines and fill itself from a seeded simulation.

**params**
- `categories: [2, 3, ...]` or `[{ id, label, value }]`. Alternatively `bins: { min, max, width }`.
- `yLabel`, `xLabel`, `height`, `colour`, `showValues`, `yMax`.
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

**state**
- `markers: [{ id, i, series, label, below, colour, y }]`. `i` is an index or an ISO date. `label` may contain `{value}`. A marker sits on its series' value at `i`; give `y` to place it explicitly, which you must do where that value is `null` (a marker on a gap is otherwise skipped).
- `shade: [{ id, from, to, label, tone: "neg"|"pos"|"neutral" }]`.
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

## matrix

**params**
- `matrices: [{ id, rows: [[...]], label }]`. Cells may be numbers or strings, including `$...$`.
- `ops: ["×", "="]`: the operators between consecutive matrices.
- `cellHeight`.

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

## graph

**params**
- `nodes: [{ id, label, x, y, colour }]`. `x` and `y` are fractions from 0 to 1 of the frame.
- `edges: [{ from, to, w, label, directed, dashed, bend, colour }]`. Edge ids are `e-{from}-{to}`.
- `directed` (the default for all edges), `markov: true`, `nodeRadius`, `height`.
- `layout: "ring"`: the nodes sit evenly round a circle in list order (seats round a table), ignoring `x` and `y`.
- Without `nodeRadius` the radius grows to fit the longest label (22 up to 34); a label still too long shrinks (down to 10px).
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

## array

**params**
- `cells: [5, 2, 9]`, `indexFrom` (default 0).
- `mode`: `"array"`, `"stack"` (vertical, top marked), `"queue"` (front and back labels) or `"linked"` (boxes with next arrows ending in `null`).
- `capacity` (stack height), `showIndex`, `pointersBelow`, `topLabel`, `frontLabel`, `backLabel`, `nullLabel`, `height`.

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

## payoff

Payoff or profit and loss at expiry against the price of the underlying.

**params**
- `legs: [{ id, type: "call"|"put"|"stock", side: "long"|"short", strike, premium, qty, label, colour, strikeLabel }]`. For `stock`, `strike` is the entry price.
- `range: [min, max]`.
- `pl` (default true) subtracts premiums for long legs and adds them for short legs.
- `y`, `yLabel`, `xLabel`, `label` (the combined line's label), `spotLabel`, `snap` (strike drag step, default 1), `drag` (leg ids), `height`.

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

## orderbook

**params**
- `bids: [[price, size]]` and `asks: [[price, size]]`, in any order; they are sorted.
- `depth`: levels shown on each side.
- `dp`: price decimals. Inferred if omitted.
- `currency`, `bidLabel`, `askLabel`, `spreadLabel`, `showMid`.
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

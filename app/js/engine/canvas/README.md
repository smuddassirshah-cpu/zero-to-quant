# Canvases A: grid, tree, venn, number-line, boxes, area, balance, circle, table

Authoring reference for the canvas kinds built on `_base.js` by E3. The lesson schema is in `docs/AUTHORING.md` section 4; this file is the exact contract for these nine kinds. A canvas in a screen is

```json
"canvas": { "kind": "grid", "params": { }, "state": { } }
```

`params` fix the drawing. `state` is the starting state, and it is what `explain.canvas`, `demonstrate.steps[].canvas`, `wrong[].canvas` and hints patch. Patches merge: objects merge key by key, arrays replace, and an object patch for a list of items with ids is keyed: `{ "points": { "p2": { "x": 3 } } }` merges into `p2` and keeps the rest (in `ZQ.canvas.merge`, so it holds for every kind and for the explanation copy).

## Keys every kind accepts in state

| key | meaning |
|---|---|
| `caption` | text under the drawing (markdown with `$...$` maths) |
| `highlight` | `[ids]`: pear wash and a 2px ink ring that pulses twice, stays until cleared (`"highlight": []`) |
| `selected` | `[ids]`: the learner's tap selection, in manipulable blue. The `tap-regions` widget reads and writes it |

## Shared behaviour (for engine authors)

- `set(patch, { instant })` animates over about 600ms (beam swings 700ms on the spring) unless `instant` or reduced motion.
- `highlight(ids, on = true)`, `flash(ids)` (amber, twice at 150ms, for show-why), `unflash()`, `mark(ids, cls, on)`, `unmark(cls?)` for the graded classes `is-correct`, `is-notyet`, `is-reveal`, `is-dim` (an amber cross badge comes with `is-notyet`), `lock(on)`, `clone(host)`, `on('change', fn)`, `enable(mode, opts)`, `destroy()`.
- `enable('tap', { max, only })`: elements become buttons with `aria-pressed`; Space toggles, arrow keys move focus spatially, Enter is left to the player. Emits `{ selected, id, on }`.
- `enable('drag', { ids })`: emits `{ id, x, y, phase: 'move' | 'end' }` (x, y in canvas units). Drag canvases expose `points()` and `place(id, pos, { instant })`.
- Explore controls (`canvas.controls`) call `setParam(name, value)`: number-line moves the point with that id, circle accepts `angle`, area takes `split`, `split.rows`, `split.cols`, `grid`, `grid.rows`, `grid.cols` and `shade`. A control without `start` opens at the bound value's current value, read with `getParam(name)` when the canvas has it (number-line: the point's x; area: the current split, grid or fractional shade), else from the state; with `start` it opens there and applies it to the canvas. `format: "fraction"` writes the readout as a fraction (0.375 reads 3/8).
- Created with `ctx.static` or `ctx.mode: 'static'` (the explanation modal), a canvas has no interaction and no timed fades.

---

## grid

Sample spaces, two-dice tables, area models, Punnett squares. Square cells, at most 420px wide (344px compact), 6px gutters.

**params**

| key | default | meaning |
|---|---|---|
| `rows`, `cols` | 6, 6 | size |
| `rowLabel`, `colLabel` | none | axis titles ("First die" runs up the left side) |
| `rowHeads`, `colHeads` | 1..n | head labels; `false` hides them. `sum`, `product` and so on use their numbers |
| `cells` | blank | `"pair"` shows "r, c", `"sum"`, `"product"`, `"diff"` (absolute), `"max"`, `"min"`, or a 2D array of strings |
| `text` | `"always"` | `"marked"` hides cell text until a cell is shaded, selected, graded, flashed or highlighted (the prototype's look) |
| `compact` | false | smaller grid for title screens |

**state**: `shade: { "<set>": [ids] }` (or one array; sets take series slots in order: 18% fill and a 2px stroke; a cell in a second set gets an inner ring), `outline: "row5" | "col3" | "cross5" | "cross5-3" | [ids]` (dashed union outline in the gutters, one path), `dim: [ids]` (fades to 20%, row after row), `mark: { "<id>": "✓" | { "text": "×2", "tone": "notyet" | "correct" | "hint" } }`, `point: [ids]` (the prototype's hint box around the cells' bounding box; pulses twice, fades after 3.2s).

**ids**: `r{i}c{j}`, one-based (`r5c1` is row 5, column 1). Any id list also accepts `row5`, `col3`, `cross5`, `cross5-3` and `all`.

**methods**: `flash(ids)`, `point(ids)`, `peek(ms)` (briefly undims), `expand(list)`. **events**: tap.

`highlight` on a grid draws the union of the cells as one washed shape with an ink ring.

```json
{ "kind": "grid",
  "params": { "rowLabel": "First die", "colLabel": "Second die", "cells": "pair", "text": "marked" },
  "state": { "shade": { "eight": ["r2c6", "r3c5", "r4c4", "r5c3", "r6c2"] }, "outline": "cross5", "dim": ["r1c1"], "mark": { "r5c5": { "text": "×2", "tone": "notyet" } } } }
```

## tree

Probability and decision trees, left to right or top to bottom; spacing is automatic.

**params**: `levels: [{ "label": "First draw", "branches": [{ "id": "r", "label": "Red", "p": "3/5" }] }]` (every node of a level gets the level's branches; `p` and `label` may be a map keyed by the parent path, with `"*"` as the default, for draws without replacement; a branch whose `p` map has no entry for a parent is left out there), or `nodes: [{ "id", "label", "p", "value", "children": [...] }]`; `leaves: { "<path>": "6/20" }`; `orient: "lr" | "tb"`; `levelLabels` (with `nodes`). Probabilities such as `"3/5"` render as fractions; `"$...$"` is TeX.

**state**: `highlight: [paths]` (every branch from the root to each path: bold stroke and pear wash), `shade: [paths]` or `{ "<set>": [paths] }` (series colour along the path), `show: "p" | "none"` (hide probabilities), `unknown: [paths]` (shows "?" for those probabilities), `values: false` (hide leaf values), `collapse: [paths]` (hide the subtree; the tree re-spaces with an animation).

**ids**: branch paths `a`, `a-b`, `a-b-c` (branch ids joined by `-`), leaf values `val-a-b`, the root `root`. **events**: tap (branches).

```json
{ "kind": "tree",
  "params": { "levels": [
    { "label": "First draw", "branches": [{ "id": "r", "label": "Red", "p": "3/5" }, { "id": "b", "label": "Blue", "p": "2/5" }] },
    { "label": "Second draw", "branches": [{ "id": "r", "label": "Red", "p": { "r": "2/4", "b": "3/4" } }, { "id": "b", "label": "Blue", "p": { "r": "2/4", "b": "1/4" } }] } ],
    "leaves": { "r-r": "6/20", "r-b": "6/20", "b-r": "6/20", "b-b": "2/20" } },
  "state": { "highlight": ["r-b"], "unknown": ["b-b"] } }
```

## venn

One to three sets in a universe; each region is its exact shape.

**params**: `sets: ["A", "B"]` (or three), `labels: { "A": "Rain" }` (or an array; shown outside the circles), `values: { "A": 12, "AB": 5, "B": 8, "none": 15 }` (numbers, or strings such as `"1/20"`), `mode: "count" | "prob"`, `universe: "All 40 days"`.

**state**: `shade: [regions]` or `{ "<set>": [regions] }`, `show: true | false` (values), `unknown: [regions]` ("?"), `values: {}` (overrides params, for filling in during a demonstration).

**ids**: `A`, `B`, `AB`, `C`, `AC`, `BC`, `ABC` (set ids in `sets` order, each region exclusive: `A` is A only) and `none`. **events**: tap (regions).

```json
{ "kind": "venn", "params": { "sets": ["A", "B"], "labels": { "A": "Rain", "B": "Wind" }, "values": { "A": 12, "B": 8, "AB": 5, "none": 15 }, "universe": "All 40 days" },
  "state": { "shade": ["AB"] } }
```

## number-line

**params**: `min` (0), `max` (10), `step` (1, tick spacing), `snap` (defaults to `step`), `labels` (true; a number k labels every k-th tick; or `[{ "x": 0.5, "text": "half" }]`; `false` for none; labels thin out automatically so they never collide), `format: "decimal" | "fraction"`, `ends: false` removes the axis arrowheads.

**state**: `points: [{ "id": "p1", "x": 2.5, "label": "a", "colour": 2, "drag": true, "labelPos": "above" }]`, `intervals: [{ "id": "i1", "from": 1, "to": 3, "open": [false, true], "label": "", "labelPos": "above" }]` (`from` or `to` null makes a ray; later intervals stack above the first), `arrows: [{ "id": "j1", "from": -2, "to": 1, "label": "+3" }]` (jumps drawn as arcs). `points`, `intervals` and `arrows` also take keyed patches: `{ "points": { "p1": { "x": 3 } } }` changes `p1` only (an id not yet listed is added).

**labels**: `labelPos` is `above`, `below` (under the tick labels), `left` or `right` (beside the point, raised clear of the axis; for an interval, beside its ends). Without it a point label goes above, or to the side away from a jump arrow that starts or ends at the point (below when arrows leave both ways). Labels that would overlap each other or an arrow's label are stacked 18px apart, and the drawing grows to fit.

**ids**: the point, interval and arrow ids. **events**: drag (`{ id, x, y: 0, phase }`, snapped); tap on points (`enable('tap')`, as the tap-regions widget does: points become buttons and their ids are the region ids). A point is drawn as a drag handle, and can be dragged, only when `enable('drag', { ids })` lists it (the drag-point widget) or it has `drag: true` (an explore point, movable without a widget); every other point, every point in tap mode and every point in a static copy (the Why? modal) is a plain dot. Points and intervals take `colour` (series slot 1 to 6), and a patch can change it (a drag handle stays manipulable blue). Intervals take `row` (0 on the axis, then 16px apart; default the interval's index); a `left` or `right` label on a ray (`from` or `to` null) sits above the bar at the drawing's edge. Arrow keys move a focused point by `snap` (Shift: ten times). **methods**: `points()`, `place(id, x)`, `setParam(id, x)`, `getParam(id)`.

```json
{ "kind": "number-line", "params": { "min": -5, "max": 5, "step": 1 },
  "state": { "points": [{ "id": "p1", "x": -2, "label": "a" }], "intervals": [{ "id": "i1", "from": -1, "to": 2, "open": [true, false] }], "arrows": [{ "id": "j1", "from": -2, "to": 1, "label": "+3" }] } }
```

## boxes

Containers and items for counting and drawing without replacement.

**params**: `containers: [{ "id": "urn", "label": "Urn", "kind": "urn" | "bag" | "box" | "hand" | "row", "items": [{ "id": "b1", "kind": "ball" | "card" | "coin" | "slot" | "bag", "colour": 1, "label": "1", "face": "up" }], "capacity": 3, "slots": 3, "cols": 3 }]`, `itemKind` (default for items, `"ball"`). A coin shows its face, H or T, unless it has a `label`. Without a `hand` container, drawn items wait in a band above the containers; the band is there only while an item is drawn, so a plain set of containers has no empty space on top. An item of kind `bag` (alias `sealed`) is a closed sack showing only its label (`"?"`, `"n"`), for a bag of counters whose contents stay hidden. `colour` is a series slot 1 to 6 (0 for a plain item). A `row` draws `slots` dashed places that fill left to right.

**state**: `draw: [ids]` (move to the container whose kind is `hand`; without one, drawn items lift above the containers), `move: { "<item>": "<container>" }` (key order is arrival order), `face: { "<card>": "up" | "down", "<coin>": "H" | "T" }` (flips animate).

**ids**: item ids, container ids, row places `<container>-<k>` (one-based). **events**: drag (`{ id, x, y, phase: 'move' }` while dragging, then `{ id, container, phase: 'end' }`; arrow keys move a focused item to the previous or next container); tap (items). **methods**: `contents()` returns `{ container: [item ids] }`, `place(id, containerId)`.

```json
{ "kind": "boxes", "params": { "containers": [
    { "id": "urn", "label": "Urn", "kind": "urn", "items": [{ "id": "b1", "colour": 1 }, { "id": "b2", "colour": 1 }, { "id": "b3", "colour": 2 }] },
    { "id": "hand", "label": "Drawn", "kind": "hand", "capacity": 2 } ] },
  "state": { "draw": ["b3"] } }
```

## area

Fraction and multiplication area models, geometric probability.

**params**: `shape: "rect" | "square" | "circle"`, `grid: [rows, cols]` (a circle uses `sectors: n`), `size: [w, h]` (rectangle proportions, default 3 by 2), `colSizes`, `rowSizes` (unequal widths for area models such as 30 + 4), `labels: { "top", "bottom", "left", "right" }`, `colLabels`, `rowLabels`.

**state**: `shade` as cell ids, a fraction (`0.375`: whole cells in reading order when it lands on whole cells, else a strip from the left or a sector from twelve o'clock; changes between fractions animate), `{ "rows": k }`, `{ "cols": k }`, or `{ "<set>": any of those }` to overlay up to three shadings (set 1 a solid wash, sets 2 and 3 hatched), `split: [rows, cols]` (dashed cut lines; for a circle `[n]` radii), `grid: [rows, cols]` (or `n` columns; for a circle `[n]` sectors: re-cuts the shape, rebuilding the cells, so a fractional `shade` lands on the new cells and the cell ids follow the new grid), `point: [x, y]` or a list (unit coordinates, y up; a circle uses -1 to 1). Grid lines inside a shading are redrawn over it in a darker tone of the shading's colour so the cuts stay legible.

**controls** (the learner re-cuts): bind `grid.cols` (or `grid`, `grid.rows`) to change the pieces, `split.rows` / `split.cols` (or `split`, the columns) to draw cut lines, `shade` to set a fractional shading; add `"format": "fraction"` to the `shade` control for a 3/8 readout.

```json
{ "kind": "area", "params": { "shape": "rect", "grid": [1, 2], "size": [4, 2] }, "state": { "shade": 0.5 },
  "controls": [{ "bind": "grid.cols", "min": 2, "max": 12, "step": 2, "label": "Pieces" }, { "bind": "shade", "min": 0, "max": 1, "step": 0.125, "label": "Shaded", "format": "fraction" }] }
```

**text on a piece**: `labels` (params) and `state.labels` also take cell ids, `{ "c11": "$3n$", "c12": "4" }`, drawn centred on the cell (on a circle, along the sector's middle); the state wins.

**ids**: cells `c{i}{j}` one-based from the top left (`c{i}-{j}` when either index is 10 or more), circle sectors `c1{j}` clockwise from twelve o'clock, points `pt1`, `pt2`. **events**: tap (cells).

```json
{ "kind": "area", "params": { "shape": "rect", "grid": [3, 4], "size": [4, 3], "labels": { "bottom": "$\\tfrac{3}{4}$ of the width", "left": "$\\tfrac{2}{3}$" } },
  "state": { "shade": { "width": { "cols": 3 }, "height": { "rows": 2 } } } }
```

## balance

Two-pan scale. The beam tilts by clamp(k × (right − left), ±15°) on the spring-physical easing.

**params**: `left`, `right` (item lists as in the widget: `{ "id": "x1", "kind": "unknown", "label": "x" }`, `{ "id": "w3", "kind": "weight", "value": 3 }`), `x` (the hidden value of an unknown; default: the value that balances the starting pans), `k` (degrees per unit, default 3), `unknownLabel` ("x"), `signed` (true forces signed pans). Signed pans: a weight may be negative (dashed, it lifts its pan) and an unknown may carry `coef` (`-1`, `0.5`, `-3`, labelled `−x`, `½x`, `−3x`); then every move works on the pan totals and each pan collapses to one unknown block per label and one weight block. Several unknown kinds: an unknown with its own `label` (y) and a hidden `value` weighs that value (else `state.params[label]`, else 1); `removeBoth("y")` takes one y from each pan.

**state**: `left`, `right` (current pans; setting them restarts the move list; both empty means back to params), `params: { "x": 4 }` (the unknown's value; patches, explanations and a control bound to `x` change it and the beam re-tilts).

**ids**: item ids, `beam`, `left`, `right` (the pans). **operations** (for the balance widget; each returns `{ ok, reason }` and emits `{ op, moves, left, right }`): `removeBoth(n)`, `removeBoth("x")` (one unknown from each pan), `halveBoth()`, `divideBoth(k)`, `subtractBoth(n)`, `addBoth(n)`, `removeItem(id)`; also `moves()`, `isLevel()`, `tilt()`, `reset()`, `setParam("x", v)`, `getParam("x")`. Reasons: `not-enough`, `no-unknown`, `uneven`, `bad-number`, `locked`.

```json
{ "kind": "balance", "params": { "left": [{ "id": "x1", "kind": "unknown" }, { "id": "x2", "kind": "unknown" }, { "id": "w3", "kind": "weight", "value": 3 }], "right": [{ "id": "w11", "kind": "weight", "value": 11 }] }, "state": {} }
```

## circle

The unit circle.

**params**: `degrees` (true; false means `angle` is in radians and tick labels read π/6 and so on), `showSin` (true), `showCos` (true), `showTan` (false), `ticks` (common angles; `"quadrants"`, `false`, or a list), `tickLabels` (true), `values` (show "cos θ = 0.5"), `coords` (label the point "(0.5, 0.87)"), `angleLabel: "theta"` (label the angle θ instead of its value), `snap` (degrees, default 1; common angles pull within 3°).

**state**: `angle` (default 30° or π/6), `shade: "arc" | "sector"`.

**ids**: `angle`, `pt`, `radius`, `cos`, `sin`, `tan`, `arc`. **events**: drag on `pt`: `{ id: "pt", angle, x: cos, y: sin, phase }`. A drag-point target is the angle (a number).

```json
{ "kind": "circle", "params": { "values": true }, "state": { "angle": 60, "shade": "sector" } }
```

## table

An HTML table in the canvas wrapper.

**params**: `columns`, `rows` (2D array; a cell may be text, a number, `{ "text": "..." }`, or `{ "edit": true, "placeholder": "?" }`), `editable: ["r1c1"]` (more editable cells), `align` (`"left" | "right" | "center"` or one per column; default first column left, others right), `rowHeads` (first column as row headers).

**state**: `highlight` as ids or `{ "rows": [0], "cols": [2], "cells": ["r1c1"] }` (one ring around the union), `shade: [ids]` or `{ "<set>": [ids] }`, `values: { "r1c1": "0.5" }` (fills inputs or replaces cell text).

**ids**: zero-based, as E2's table widget: `r{i}` a body row, `c{j}` a column (header and cells), `r{i}c{j}` a cell; `r0c0` is the first body cell. **methods**: `cells()` returns the editable inputs (each with `data-id`), `input(id)`. **events**: tap (non-editable cells).

```json
{ "kind": "table", "params": { "columns": ["$x$", "$P(X = x)$"], "rows": [["0", "0.25"], ["1", { "edit": true }], ["2", "0.25"]], "align": ["center", "right"] },
  "state": { "highlight": { "rows": [1] } } }
```

---

## Canvas-bound widgets

- **tap-regions** (`answer`, `max`, `wrong: [{ "id", "set", "flash" }]`, `countWord`): works on any canvas with tap mode (grid, tree, venn, area, boxes, table, number-line points, and E4's tappable kinds). Keys: a matching `wrong[]` id, else the first wrongly selected id, else the first missed answer id. `showWhy` flashes the extra ids of the matched set (or `flash`), else the wrong picks. Count mode: `{ "count": 3, "among": ["c11", "c12", "c13", "c14"] }` with no `answer` is correct when exactly `count` regions are selected, all within `among` when given; keys are a matching `wrong[]` id, else the first pick outside `among`, else `too-few` or `too-many`; the count reads "2 of 3 shaded" (with `countWord`); reveal selects the first `count` of `among`.
- **place** in `mode: "boxes"` (`answer: { "<container>": [itemIds] }`, `ordered`): the learner drags the canvas's items between containers; correct when every named container holds exactly its listed items. Keys: the first item out of place. `reveal` moves the items there in hint indigo.
- **balance** (`moves: ["remove-both", "remove-unknown-both", "halve-both", "divide-both", "subtract-both", "add-both", "remove-item"]`, `target: { "left": ["unknown"], "right": [4] }`): chips under the canvas and a live equation. Keys: `unbalanced`, `unsolved`. A target matches either way round; weights compare by total. The test hook's correct answer is the shortest list of the allowed moves (at most six) that reaches the target (`ZQ.grade.balanceMoves`), so the target must be reachable with them.
- **drag-point** (`points: [{ "id", "target", "tol" }]`, `wrong: [{ "id", "region": { "x": [a, b], "y": [c, d] } | { "angle": [a, b] }, "canvas": {patch} }]`): targets are `[x, y]`, or a number on number-line (x) and circle (angle). Default `tol` 0.25. Keys: a `wrong[]` id whose region holds a point, else the first point off target (its point id, which `byKey` may use).

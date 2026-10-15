# Canvases A: grid, tree, venn, number-line, boxes, area, balance, circle, table

Authoring reference for the canvas kinds built on `_base.js` by E3. The lesson schema is in `docs/AUTHORING.md` section 4; this file is the exact contract for these nine kinds. A canvas in a screen is

```json
"canvas": { "kind": "grid", "params": { }, "state": { } }
```

`params` fix the drawing. `state` is the starting state, and it is what `explain.canvas`, `demonstrate.steps[].canvas`, `wrong[].canvas` and hints patch. Patches merge: objects merge key by key, arrays replace.

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
- Explore controls (`canvas.controls`) call `setParam(name, value)`: number-line moves the point with that id, circle accepts `angle`.
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

**state**: `points: [{ "id": "p1", "x": 2.5, "label": "a", "colour": 2, "drag": true }]`, `intervals: [{ "id": "i1", "from": 1, "to": 3, "open": [false, true], "label": "" }]` (`from` or `to` null makes a ray; later intervals stack above the first), `arrows: [{ "id": "j1", "from": -2, "to": 1, "label": "+3" }]` (jumps drawn as arcs).

**ids**: the point, interval and arrow ids. **events**: drag (`{ id, x, y: 0, phase }`, snapped). Draggable points: those listed by `enable('drag', { ids })`, else those with `drag: true`, else all. Arrow keys move a focused point by `snap` (Shift: ten times).

```json
{ "kind": "number-line", "params": { "min": -5, "max": 5, "step": 1 },
  "state": { "points": [{ "id": "p1", "x": -2, "label": "a" }], "intervals": [{ "id": "i1", "from": -1, "to": 2, "open": [true, false] }], "arrows": [{ "id": "j1", "from": -2, "to": 1, "label": "+3" }] } }
```

## boxes

Containers and items for counting and drawing without replacement.

**params**: `containers: [{ "id": "urn", "label": "Urn", "kind": "urn" | "bag" | "box" | "hand" | "row", "items": [{ "id": "b1", "kind": "ball" | "card" | "coin" | "slot", "colour": 1, "label": "1", "face": "up" }], "capacity": 3, "slots": 3, "cols": 3 }]`, `itemKind` (default for items, `"ball"`). `colour` is a series slot 1 to 6 (0 for a plain item). A `row` draws `slots` dashed places that fill left to right.

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

**state**: `shade` as cell ids, a fraction (`0.375`: whole cells in reading order when it lands on whole cells, else a strip from the left or a sector from twelve o'clock; changes between fractions animate), `{ "rows": k }`, `{ "cols": k }`, or `{ "<set>": any of those }` to overlay up to three shadings (set 1 a solid wash, sets 2 and 3 hatched), `split: [rows, cols]` (dashed cut lines; for a circle `[n]` radii), `point: [x, y]` or a list (unit coordinates, y up; a circle uses -1 to 1).

**ids**: cells `c{i}{j}` one-based from the top left (`c{i}-{j}` when either index is 10 or more), circle sectors `c1{j}` clockwise from twelve o'clock, points `pt1`, `pt2`. **events**: tap (cells).

```json
{ "kind": "area", "params": { "shape": "rect", "grid": [3, 4], "size": [4, 3], "labels": { "bottom": "$\\tfrac{3}{4}$ of the width", "left": "$\\tfrac{2}{3}$" } },
  "state": { "shade": { "width": { "cols": 3 }, "height": { "rows": 2 } } } }
```

## balance

Two-pan scale. The beam tilts by clamp(k × (right − left), ±15°) on the spring-physical easing.

**params**: `left`, `right` (item lists as in the widget: `{ "id": "x1", "kind": "unknown", "label": "x" }`, `{ "id": "w3", "kind": "weight", "value": 3 }`), `x` (the hidden value of an unknown; default: the value that balances the starting pans), `k` (degrees per unit, default 3), `unknownLabel` ("x").

**state**: `left`, `right` (current pans; setting them restarts the move list; both empty means back to params).

**ids**: item ids, `beam`, `left`, `right` (the pans). **operations** (for the balance widget; each returns `{ ok, reason }` and emits `{ op, moves, left, right }`): `removeBoth(n)`, `removeBoth("x")` (one unknown from each pan), `halveBoth()`, `divideBoth(k)`, `removeItem(id)`; also `moves()`, `isLevel()`, `tilt()`, `reset()`. Reasons: `not-enough`, `no-unknown`, `uneven`, `bad-number`, `locked`.

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

- **tap-regions** (`answer`, `max`, `wrong: [{ "id", "set", "flash" }]`, `countWord`): works on any canvas with tap mode (grid, tree, venn, area, boxes, table, and E4's tappable kinds). Keys: a matching `wrong[]` id, else the first wrongly selected id, else the first missed answer id. `showWhy` flashes the extra ids of the matched set (or `flash`), else the wrong picks.
- **balance** (`moves: ["remove-both", "remove-unknown-both", "halve-both", "divide-both", "remove-item"]`, `target: { "left": ["unknown"], "right": [4] }`): chips under the canvas and a live equation. Keys: `unbalanced`, `unsolved`. A target matches either way round; weights compare by total.
- **drag-point** (`points: [{ "id", "target", "tol" }]`, `wrong: [{ "id", "region": { "x": [a, b], "y": [c, d] } | { "angle": [a, b] }, "canvas": {patch} }]`): targets are `[x, y]`, or a number on number-line (x) and circle (angle). Default `tol` 0.25. Keys: a `wrong[]` id whose region holds a point, else the first point off target.

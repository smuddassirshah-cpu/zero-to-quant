# Canvases A: grid, tree, venn, number-line, boxes, area, balance, circle, table

Authoring reference for the canvas kinds built on `_base.js` by E3. The lesson schema is in `docs/AUTHORING.md` section 4; this file is the exact contract for these nine kinds. A canvas in a screen is

```json
"canvas": { "kind": "grid", "params": { }, "state": { } }
```

`params` fix the drawing. `state` is the starting state, and it is what `explain.canvas`, `demonstrate.steps[].canvas`, `wrong[].canvas` and hints patch. Patches merge: objects merge key by key, arrays replace, and an object patch for a list of items with ids is keyed: `{ "points": { "p2": { "x": 3 } } }` merges into `p2` and keeps the rest (in `ZQ.canvas.merge`, so it holds for every kind and for the explanation copy).

## Keys every kind accepts in state

| key | meaning |
|---|---|
| `caption` | text under the drawing, rendered like lesson prose: `$...$` maths, `**bold**`, `*italic*` and inline code in backticks (where `$` and `*` stay literal) |
| `highlight` | `[ids]`: pear wash and a 2px ink ring that pulses twice, stays until cleared (`"highlight": []`) |
| `selected` | `[ids]`: the learner's tap selection, in manipulable blue. The `tap-regions` widget reads and writes it |

## Shared behaviour (for engine authors)

- `set(patch, { instant })` animates over about 600ms (beam swings 700ms on the spring) unless `instant` or reduced motion.
- `highlight(ids, on = true)`, `flash(ids)` (amber, twice at 150ms, for show-why), `unflash()`, `mark(ids, cls, on)`, `unmark(cls?)` for the graded classes `is-correct`, `is-notyet`, `is-reveal`, `is-dim` (an amber cross badge comes with `is-notyet`), `lock(on)`, `clone(host)`, `on('change', fn)`, `enable(mode, opts)`, `destroy()`.
- `enable('tap', { max, only })`: elements become buttons with `aria-pressed`; Space toggles, arrow keys move focus spatially, Enter is left to the player. Emits `{ selected, id, on }`.
- `enable('drag', { ids })`: emits `{ id, x, y, phase: 'move' | 'end' }` (x, y in canvas units). Drag canvases expose `points()` and `place(id, pos, { instant })`.
- Explore controls (`canvas.controls`) call `setParam(name, value)`: number-line moves the point with that id, circle accepts `angle`, area takes `split`, `split.rows`, `split.cols`, `grid`, `grid.rows`, `grid.cols` and `shade`. A control without `start` opens at the bound value's current value, read with `getParam(name)` when the canvas has it (number-line: the point's x; area: the current split, grid or fractional shade), else from the state; with `start` it opens there and applies it to the canvas. `format: "fraction"` writes the readout as a fraction (0.375 reads 3/8).
- Created with `ctx.static` or `ctx.mode: 'static'` (the explanation modal), a canvas has no interaction and no timed fades.


## Column width (ENGINE-BACKLOG 507)

A canvas draws into the lesson column: `--col` in `css/tokens.css`, 540px below a 768px viewport and 780px from 768px up (an iPad, a laptop). It scales to the column width; a canvas never sets its own pixel width. A tall `viewBox` gets taller on a wide column, so cap one with `canvas.maxHeight` if a widget has to stay in view beneath it. Test at 440, 1032 and 1376 (`--mobile --tablet`).

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
| `revealAfterGrade` | false | with `text: "marked"`, a tap selects a cell without showing its text; grading (or a hint) shows it |
| `lattice` | false | points instead of cells: a dot at each cell centre, joined to its neighbours by streets, its text above right of the dot (path counts). Ids, shading, taps, marks and `paths` work the same way |
| `rowOffsets` | none | per-row shift in cell widths, `[0, 0.25, 0.75]`, for staggered layouts such as a keyboard; outlines and highlights follow the shift |

**state**: `shade: { "<set>": [ids] }` (or one array; sets take series slots in the order 3, 2, 4, 5, 6, 1, so a pre-shaded set never matches the blue of a tap selection: 18% fill and a 2px stroke; a cell in a second set gets an inner ring; `{ "<set>": { "ids": [...], "colour": 3 } }` picks the slot), `cells: { "r2c3": "5" }` (or a 2D array: overrides `params.cells` for those cells, so an explanation can fill a cell; `""` blanks one, `null` restores them all), `paths: [{ "id": "route", "cells": ["r4c1", "r4c2", "r3c2"], "colour": 1, "arrow": true }]` (or `{ "route": [ids] }`: a route through the cell centres, drawn on as it appears, an arrowhead at the end unless `arrow: false`; its id highlights), `outline: "row5" | "col3" | "cross5" | "cross5-3" | [ids]` (dashed union outline in the gutters, one path), `dim: [ids]` (fades to 20%, row after row), `mark: { "<id>": "✓" | { "text": "×2", "tone": "notyet" | "correct" | "hint" } }`, `point: [ids]` (the prototype's hint box around the cells' bounding box; pulses twice, fades after 3.2s).

A grid's `values()` gives each cell's number (its shown text, when numeric), so a derive caption can keep a running total of a tap selection: `"caption": "{{selected.length}} tapped, total {{total(selected)}}"`.

**ids**: `r{i}c{j}`, one-based (`r5c1` is row 5, column 1), and path ids. Any id list also accepts `row5`, `col3`, `cross5`, `cross5-3` and `all`.

**methods**: `flash(ids)`, `point(ids)`, `peek(ms)` (briefly undims), `expand(list)`. **events**: tap.

`highlight` on a grid draws the union of the cells as one washed shape with an ink ring.

```json
{ "kind": "grid",
  "params": { "rowLabel": "First die", "colLabel": "Second die", "cells": "pair", "text": "marked" },
  "state": { "shade": { "eight": ["r2c6", "r3c5", "r4c4", "r5c3", "r6c2"] }, "outline": "cross5", "dim": ["r1c1"], "mark": { "r5c5": { "text": "×2", "tone": "notyet" } } } }
```

Lattice paths (counting routes on a 4 by 5 street grid):

```json
{ "kind": "grid",
  "params": { "rows": 4, "cols": 5, "rowHeads": false, "colHeads": false, "lattice": true },
  "state": { "cells": { "r4c1": "1", "r3c1": "1", "r4c2": "1", "r3c2": "2" }, "shade": { "start": { "ids": ["r4c1"], "colour": 3 } },
    "paths": [{ "id": "route", "cells": ["r4c1", "r4c2", "r3c2", "r3c3", "r2c3", "r2c4", "r1c4", "r1c5"] }] } }
```

**Integration pass 6 additions**
- `population: 1000` draws that many small dots in rows of `cols` (default 40); `state.groups: [{ id, count, colour, label }]` shades consecutive runs in order, and each group is one tap target by its id. `values()` gives each group's count.
- `margins: true` adds a column of row sums and a row of column sums (and the total) outside the cells, from the cells' numbers (state.cells included), or `margins: { rows, cols, total }` gives them; `state.margins: false` hides them until a patch shows them. Ids `rsum1`, `csum1`, `total`; named sets such as `row1` skip them.
- A dimmed blank cell greys its background (dashed), so `dim` shows without text.
- Tap-regions `answer`, `among` and `wrong` sets may use set names (`cross2`, `row5`, `all`).
- Typing into a canvas: a `table` widget cell with `bind: "cells.r2c3"` writes what the learner types into that grid cell (margins update), so "fill the product of the margins" happens on the grid.

**Integration pass 7 additions**
- `state.mark` entries set to `null` (or `""`) remove a badge instead of printing "null"; `{ "text": "♛", "pos": "centre" }` (or `params.markPos: "centre"`) draws the glyph large in the middle of the cell, hiding that cell's text.
- A cell text with a newline (`"£5\n£20"`, in `params.cells` or `state.cells`) is drawn on two lines, the second lighter; `values()` reads the first line.
- The text of every cell a `paths` route passes is repeated above the route with a halo, so the numbers on a route stay readable.
- Filling a DP table: a `table` widget cell may carry `deps: ["r1c2", "r2c1"]` (grid ids), highlighted on the grid while that cell has focus; with `bind: "cells.r2c2"` the typed value appears in the grid cell too. Grading stays in the table widget (a grid table-fill mode of its own is not added).

## tree

Probability and decision trees, left to right or top to bottom; spacing is automatic.

Collapsing (`state.collapse`) resizes the drawing to the leaves (or, top to bottom, the depth) still shown.

**params**: `label: "Project folder"` (a title drawn above the tree; also its accessible name), `compact: true` (smaller pills and closer leaves: a 16-leaf tree fits the column; top to bottom suits it best), `rootLabel: "Start"` (the root is a labelled pill instead of a dot; `"/"` for a folder tree), `levels: [{ "label": "First draw", "branches": [{ "id": "r", "label": "Red", "p": "3/5" }] }]` (every node of a level gets the level's branches; `p` and `label` may be a map keyed by the parent path, with `"*"` as the default, for draws without replacement; a branch whose `p` map has no entry for a parent is left out there), or `nodes: [{ "id", "label", "p", "value", "children": [...] }]`; `leaves: { "<path>": "6/20" }`; `orient: "lr" | "tb"`; `levelLabels` (with `nodes`). Probabilities such as `"3/5"` render as fractions; `"$...$"` is TeX.

**state**: `highlight: [paths]` (every branch from the root to each path: bold stroke and pear wash), `shade: [paths]` or `{ "<set>": [paths] }` (series colour along the path), `show: "p" | "none"` (hide probabilities), `unknown: [paths]` (shows "?" for those probabilities), `values: false` (hide leaf values), `collapse: [paths]` (hide the subtree; the tree re-spaces with an animation), `current: "a-b"` (a manipulable-blue ring round that node's pill, like graph's current node; `"root"` for the root), `branching` (a number, a list per level or `{ "0": 3, "1": 2 }`, level 0 the first: each node of that level shows only its first k branches, and the tree re-spaces; a control bound to `branching.1` or `branching` drives it, for "options per stage" sliders).

Label spacing: on a tree with 7 or more leaves shown, probability labels from the second level on alternate along their branches between neighbouring subtrees, an inner branch of a fan of three or more puts its label near the far end, and labels shrink a little from 9 leaves.

**ids**: branch paths `a`, `a-b`, `a-b-c` (branch ids joined by `-`), leaf values `val-a-b`, the root `root`. **events**: tap (branches).

```json
{ "kind": "tree",
  "params": { "levels": [
    { "label": "First draw", "branches": [{ "id": "r", "label": "Red", "p": "3/5" }, { "id": "b", "label": "Blue", "p": "2/5" }] },
    { "label": "Second draw", "branches": [{ "id": "r", "label": "Red", "p": { "r": "2/4", "b": "3/4" } }, { "id": "b", "label": "Blue", "p": { "r": "2/4", "b": "1/4" } }] } ],
    "leaves": { "r-r": "6/20", "r-b": "6/20", "b-r": "6/20", "b-b": "2/20" } },
  "state": { "highlight": ["r-b"], "unknown": ["b-b"] } }
```

**Integration pass 6 additions:** `state.p: { "a-b": "1/3" }` replaces a branch's probability ("" shows "?") and `state.leaves: { "a-b": "£12" }` a leaf's value (give `leaves: { "a-b": "" }` to keep room for values a patch fills). A `table` widget cell with `bind: "p.a-b"` draws what the learner types on that branch and focuses when the branch is tapped. First-level labels on a fan of three or more move along their branches, away from the root.

**Integration pass 7 additions**
- `state.collapse: [""]` (only the root shown) no longer throws.
- `state.labels: { "<path>": "text", "root": "text" }` replaces a pill's text (a question while expanded, counts when collapsed); the pill widens to fit.
- `state.values: { "<path>": "V = 3.10", "root": "V₀ = 8.6" }` (or `params.values`) writes a value above any node's pill (beside it top to bottom), inner nodes and the root included, for backward induction and call-by-call return values. `state.leaves` keeps leaf values to the right; `state.values: false` still hides every value.
- `state.dim: [paths]` greys those branches and everything under them (pruned branches).
- `state.arrows: { "<path>": "down" | "up" | "both" }` puts an arrowhead on a branch: down toward the child (a call), up toward the parent (a return).
- `params.binary: true` with `nodes` as one top node `{ "id": "n8", "label": "8", "left": {...}, "right": {...} }` (or `children` with `side: "left" | "right"`) draws a binary tree top to bottom: x is each node's in-order rank, so a single child sits on its own side and no placeholder nodes are needed; the top node is a real pill (path `n8`), tappable; `highlight`, `shade` and taps act on single nodes, not paths. Ids are paths as usual (`n8-n3-n6`).
- `params.spacing: 1.3` multiplies the leaf spacing (stacked pairs with long branch labels).
- A recombining binomial lattice is the `graph` canvas's `lattice` layout (README-B), not a tree option.
- Not added: a minimum font size under `canvas.maxHeight` (a capped tree still scales as a picture; prefer `compact`).

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

**state**: `points: [{ "id": "p1", "x": 2.5, "label": "a", "colour": 2, "drag": true, "labelPos": "above" }]`, `intervals: [{ "id": "i1", "from": 1, "to": 3, "open": [false, true], "label": "", "labelPos": "above" }]` (`from` or `to` null makes a ray; later intervals stack above the first), `arrows: [{ "id": "j1", "from": -2, "to": 1, "label": "+3", "side": "below" }]` (jumps drawn as arcs, above the axis unless `side: "below"`; arrows on one side whose spans overlap stack in levels; a jump from a number to itself is a small loop). An interval label is plain text (`"1/4 of the way"` stays as typed) unless it is wrapped in `$...$`. Controls may bind a free name (not a point id) for a `derive` block: it lands in `state.params`. `points`, `intervals` and `arrows` also take keyed patches: `{ "points": { "p1": { "x": 3 } } }` changes `p1` only (an id not yet listed is added).

**labels**: `labelPos` is `above`, `below` (under the tick labels), `left` or `right` (beside the point, raised clear of the axis; for an interval, beside its ends). Without it a point label goes above, or to the side away from a jump arrow that starts or ends at the point (below when arrows leave both ways). Labels that would overlap each other or an arrow's label are stacked 18px apart, and the drawing grows to fit.

**ids**: the point, interval and arrow ids. **events**: drag (`{ id, x, y: 0, phase }`, snapped); tap on points (`enable('tap')`, as the tap-regions widget does: points become buttons and their ids are the region ids). A point is drawn as a drag handle, and can be dragged, only when `enable('drag', { ids })` lists it (the drag-point widget) or it has `drag: true` (an explore point, movable without a widget); every other point, every point in tap mode and every point in a static copy (the Why? modal) is a plain dot. Points and intervals take `colour` (series slot 1 to 6), and a patch can change it (a drag handle stays manipulable blue). Intervals take `row` (0 on the axis, then 16px apart; default the interval's index); a `left` or `right` label on a ray (`from` or `to` null) sits above the bar at the drawing's edge. Arrow keys move a focused point by `snap` (Shift: ten times). **methods**: `points()`, `place(id, x)`, `setParam(id, x)`, `getParam(id)`.

```json
{ "kind": "number-line", "params": { "min": -5, "max": 5, "step": 1 },
  "state": { "points": [{ "id": "p1", "x": -2, "label": "a" }], "intervals": [{ "id": "i1", "from": -1, "to": 2, "open": [true, false] }], "arrows": [{ "id": "j1", "from": -2, "to": 1, "label": "+3" }] } }
```

**Integration pass 6 additions:** `scale: "log"` (positive values, ticks at 1, 2, 5 times powers of ten) and `scale: "log-odds"` (probabilities placed by ln(p/(1 − p)), ticks at 1%, 5%, 10%, 25%, 50%, …; `format: "percent"`); values, snapping and labels stay in the natural unit.

**Integration pass 7 additions:** negative tick labels use the minus sign −. `params.tapIntervals: true` (or `tap: true` on an interval) makes intervals tap targets by their ids, beside points.

## boxes

Containers and items for counting and drawing without replacement.

**params**: `containers: [{ "id": "urn", "label": "Urn", "kind": "urn" | "bag" | "box" | "hand" | "row", "items": [{ "id": "b1", "kind": "ball" | "card" | "coin" | "slot" | "bag", "colour": 1, "label": "1", "face": "up" }], "capacity": 3, "slots": 3, "cols": 3 }]`, `itemKind` (default for items, `"ball"`). A coin shows its face, H or T, unless it has a `label`. Without a `hand` container, drawn items wait in a band above the containers; the band is there only while an item is drawn, so a plain set of containers has no empty space on top. An item of kind `bag` (alias `sealed`) is a closed sack showing only its label (`"?"`, `"n"`), for a bag of counters whose contents stay hidden. `colour` is a series slot 1 to 6 (0 for a plain item). A `row` draws `slots` dashed places that fill left to right. `fill: "top"` or `"bottom"` on a container sets where its items start (default: top for `hand` and `row`, bottom for urns, bags and boxes). A `box` is closed on all four sides. A `card` is as wide as its label (a file name such as `prices.csv` fits on one card, which then draws a little shorter); every place in the drawing takes the widest item's width, so keep wide cards to their own canvas or to a few per container; card text shrinks with the cards. An empty container without `capacity` holds as many places as the fullest container (2 to 6), so items can be put in it.

**state**: `draw: [ids]` (move to the container whose kind is `hand`; without one, drawn items lift above the containers), `move: { "<item>": "<container>" }` (key order is arrival order), `face: { "<card>": "up" | "down", "<coin>": "H" | "T" }` (flips animate).

**ids**: item ids, container ids, row places `<container>-<k>` (one-based). **events**: drag (`{ id, x, y, phase: 'move' }` while dragging, then `{ id, container, phase: 'end' }`; arrow keys move a focused item to the previous or next container); tap (items). **methods**: `contents()` returns `{ container: [item ids] }`, `place(id, containerId)`.

```json
{ "kind": "boxes", "params": { "containers": [
    { "id": "urn", "label": "Urn", "kind": "urn", "items": [{ "id": "b1", "colour": 1 }, { "id": "b2", "colour": 1 }, { "id": "b3", "colour": 2 }] },
    { "id": "hand", "label": "Drawn", "kind": "hand", "capacity": 2 } ] },
  "state": { "draw": ["b3"] } }
```

**Integration pass 6 additions:** `size: "large"` (or `"medium"`, or a number) scales every item, so three large cards fill the canvas; item kind `door` (a tall card with a knob; face down shows its back).

**Integration pass 7 additions**
- `state.labels: { "<item>": "You 300" }` relabels an item (a card widens to fit).
- Dropping into a `row` places the item at the slot under the pointer (the others close up), kept in `state.at: { "<item>": slot }` (0-based); `contents()` (and `place` grading with `ordered: true`) follow that order.
- Four or more containers that would shrink below 80% wrap onto two or three rows; `params.rows: 2` sets the rows, `wrap: false` keeps one row. A container's own `cols` still sets its columns.
- A `card` whose label looks like code (brackets, `_`, `;`, `::`, `->`), or with `code: true` (or `params.code: true`), is set in the code face and sized from the label in that face.

## area

Fraction and multiplication area models, geometric probability.

**params**: `shape: "rect" | "square" | "circle"`, `grid: [rows, cols]` (a circle uses `sectors: n`), `size: [w, h]` (rectangle proportions, default 3 by 2), `colSizes`, `rowSizes` (unequal widths for area models such as 30 + 4), `labels: { "top", "bottom", "left", "right" }`, `colLabels`, `rowLabels`.

**state**: `shade` as cell ids, a fraction (`0.375`: whole cells in reading order when it lands on whole cells, else a strip from the left or a sector from twelve o'clock; changes between fractions animate), `{ "rows": k }`, `{ "cols": k }`, or `{ "<set>": any of those }` to overlay up to three shadings (set 1 a solid wash, sets 2 and 3 hatched), `split: [rows, cols]` (dashed cut lines; for a circle `[n]` radii), `grid: [rows, cols]` (or `n` columns; for a circle `[n]` sectors: re-cuts the shape, rebuilding the cells, so a fractional `shade` lands on the new cells and the cell ids follow the new grid), `point: [x, y]` or a list (unit coordinates, y up; a circle uses -1 to 1). Grid lines inside a shading are redrawn over it in a darker tone of the shading's colour so the cuts stay legible.

**controls** (the learner re-cuts): bind `grid.cols` (or `grid`, `grid.rows`) to change the pieces, `split.rows` / `split.cols` (or `split`, the columns) to draw cut lines, `shade` to set a fractional shading; add `"format": "fraction"` to the `shade` control for a 3/8 readout.

```json
{ "kind": "area", "params": { "shape": "rect", "grid": [1, 2], "size": [4, 2] }, "state": { "shade": 0.5 },
  "controls": [{ "bind": "grid.cols", "min": 2, "max": 12, "step": 2, "label": "Pieces" }, { "bind": "shade", "min": 0, "max": 1, "step": 0.125, "label": "Shaded", "format": "fraction" }] }
```

**signed pieces**: a negative entry in `colSizes` or `rowSizes` lays the strip out by its size and marks its pieces subtracted (hatched over any shading, dashed edge), so $(x + 5)(x - 2)$ is `colSizes: [3, 1.5]`, `rowSizes: [3, -1]`. **edge labels**: `state.colLabels`, `state.rowLabels` and `state.labels` (`top`, `bottom`, `left`, `right`) patch them; give a starting value in params so the drawing keeps room. **diagonals**: `state.diagonal: { "c11": "/" }` (bottom left to top right) or `"\\"`, dashed; shade ids `"c11/ul"`, `"c11/lr"`, `"c11/ur"`, `"c11/ll"` fill the triangle on that side. **moving a piece**: `state.move: { "id": "m1", "from": "c12", "to": "c31" }` (or a list) slides a copy of the piece (its first shading's colour and its text) to the `to` cell over about 700 ms, leaving its own place empty, for rearrangements such as the difference of two squares.

**text on a piece**: `labels` (params) and `state.labels` also take cell ids, `{ "c11": "$3n$", "c12": "4" }`, drawn centred on the cell (on a circle, along the sector's middle); the state wins. A key naming two cells, `"c11-c16"`, centres one label on the rectangle they span (a total over a row).

**sizes in state**: `state.colSizes` and `state.rowSizes` override the params (animating the re-cut), and a control can bind one entry, `"bind": "colSizes.0"`, so a cut moves at true proportions (a rectangle with growing sides). **dim**: `state.dim: [ids]` fades pieces under a light veil. A tap selection has a heavy blue edge, so it never reads as authored shading.

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

**Integration pass 6 additions:** the widget move `remove-unknown-part` (a number field: "Take away [1/2] E from both") takes k of an unknown from both pans; `removeUnknownBoth(label, k)` on the canvas. The engine's solver uses it, so E = 1 + E/2 is solved by taking E/2 from both, then dividing by 1/2.

## circle

The unit circle.

**params**: `drag` (true, or `state.drag`: the point drags without a widget, for an explore screen with a `derive` caption), `degrees` (true; false means `angle` is in radians and tick labels read π/6 and so on), `showSin` (true), `showCos` (true), `showTan` (false), `ticks` (common angles; `"quadrants"`, `false`, or a list), `tickLabels` (true), `values` (show "cos θ = 0.5"), `coords` (label the point "(0.5, 0.87)"), `angleLabel: "theta"` (label the angle θ instead of its value), `snap` (degrees, default 1; common angles pull within 3°).

**state**: `angle` (default 30° or π/6), `shade: "arc" | "sector"`.

**ids**: `angle`, `pt`, `radius`, `cos`, `sin`, `tan`, `arc`. **events**: drag on `pt`: `{ id: "pt", angle, x: cos, y: sin, phase }`. A drag-point target is the angle (a number). Labels keep clear of each other: the cos label starts past the angle mark when the mark sweeps over its side, and the sin label sits outside the rim (outside the circle altogether for a short segment). With `degrees: false` the default `tol` of 0.25 is about 14°: give `tol: 0.02` (about 1°).

```json
{ "kind": "circle", "params": { "values": true }, "state": { "angle": 60, "shade": "sector" } }
```

## table

An HTML table in the canvas wrapper. A table wider than its column (more than six columns, or a phone) scrolls sideways; while more of it lies to the right, a fade on the right edge says so (the `table` widget does the same; ENGINE-BACKLOG 607). Keep the column the question turns on, and every editable cell, in the first columns anyway: a learner may not scroll.

**params**: `columns`, `rows` (2D array; a cell may be text, a number, `{ "text": "..." }`, or `{ "edit": true, "placeholder": "?" }`), `editable: ["r1c1"]` (more editable cells), `align` (`"left" | "right" | "center"` or one per column; default first column left, others right), `rowHeads` (first column as row headers), `tap: "rows"` (tapping any cell selects the whole row, id `r{i}`: "tap the row the query returns first"). `state.dim: [ids]` greys rows, columns or cells (a row a join drops) without blanking them.

**state**: `highlight` as ids or `{ "rows": [0], "cols": [2], "cells": ["r1c1"] }` (one ring around the union), `shade: [ids]` or `{ "<set>": [ids] }`, `values: { "r1c1": "0.5" }` (fills inputs or replaces cell text).

Numbers print with the minus sign (−3), as does text that starts with a negative number ("-0.5 kg" reads −0.5 kg). `compact: true` (automatic above 6 columns) tightens the cells so a wide table fits the column; anything still wider scrolls sideways. Text cells and the caption render like prose (`$...$` maths, inline code in backticks, **bold**) and keep their spaces, so padded output lines up.

**ids**: zero-based, as E2's table widget: `r{i}` a body row, `c{j}` a column (header and cells), `r{i}c{j}` a cell; `r0c0` is the first body cell. **methods**: `cells()` returns the editable inputs (each with `data-id`), `input(id)`. **events**: tap (non-editable cells).

```json
{ "kind": "table", "params": { "columns": ["$x$", "$P(X = x)$"], "rows": [["0", "0.25"], ["1", { "edit": true }], ["2", "0.25"]], "align": ["center", "right"] },
  "state": { "highlight": { "rows": [1] } } }
```

---

**Integration pass 7 additions:** `canvas.maxHeight` now caps a table (and a console): it scrolls inside the cap instead of growing.

## console

Terminal sessions, pytest output, tracebacks: a monospace block where every line keeps its indentation and long lines scroll sideways. HTML inside the canvas wrapper, like the table.

**params**: `lines: ["$ pytest -q", "..F.", "E   assert 0.01 == 0.0"]` (or `text` with newlines), `title` (a small heading above the block, such as "Terminal"), `numbers: true` (line numbers in a gutter), `label` (accessible name). Lines starting with `$ `, `>>> ` or `... ` show the prompt muted and the command in bold.

**state**: `shade: { "<set>": [ids] }` (series slots, a 3px bar on the left), `tone: { "l3": "err" | "ok" | "muted" }` (text colour per line), `lines` (replaces the text, for output that grows during an explanation), `highlight`, `caption` (rendered like prose).

**ids**: `l1`, `l2`, ... one-based (l1 is the first line). **events**: tap (lines): `tap-regions` with `answer: ["l3"]` asks "tap the line that failed".

```json
{ "kind": "console", "params": { "title": "Terminal", "lines": ["$ pytest -q", "..F.", "E       assert 0.01 == 0.0", "1 failed, 3 passed"] },
  "state": { "shade": { "fail": ["l3"] }, "tone": { "l4": "muted" } } }
```

**Integration pass 7 additions:** `compact: true` (11.5px) or `fontSize: 10` to `14` fits 80-column output such as a statsmodels summary; `wrap: true` wraps long lines with a hanging indent so real compiler and sanitiser lines show verbatim. Without `wrap`, a box whose lines run past its edge shows a fade at the right while there is more to scroll.

## pair

Two canvases side by side (stacked below 480px, or always with `stack: true`), for a circle beside its sine graph, a tree beside its table, before beside after.

```json
{ "kind": "pair", "active": "right",
  "left": { "kind": "circle", "params": { "values": false }, "state": { "angle": 30 } },
  "right": { "kind": "plane", "params": { "x": [0, 6.3], "y": [-1.2, 1.2], "functions": [{ "id": "s", "expr": "sin(x)" }] }, "state": { "points": [{ "id": "P", "x": 0, "y": 0 }] } },
  "derive": { "right:P.x": "angle * pi / 180", "right:P.y": "sin(angle * pi / 180)", "caption": "sin {{angle}}° = {{fixed(sin(angle * pi / 180), 3)}}" },
  "controls": [{ "bind": "left:angle", "min": 0, "max": 360, "step": 15, "label": "Angle" }] }
```

- **state** patches take `{ "left": {...}, "right": {...}, "caption": "..." }`; any other key goes to the `active` side (default `left`), which is also the side canvas-bound widgets (tap-regions, drag-point, sketch, balance) drive.
- **ids** carry a prefix: `left:pt`, `right:P` in hints, `highlight`, marks and `explain.canvas`; an unprefixed id reaches both sides. A tap-regions answer on the active side uses its plain ids.
- **derive** reads both sides (ids directly, or `left.p1` and `right.p1` when they share an id) and writes `left:` or `right:` targets; a plain target writes the active side, and `caption` the pair's caption.
- **controls** bind `left:angle`, `right:a`, `right:points.P.x`; unprefixed binds reach the active side.
- **two tables** are drawn compact, and the pair stacks them (each at full width) whenever either would have to scroll side by side.
- **tap: "sides"** makes each whole side one tappable object, ids `left` and `right`, so "tap the misleading chart" is a tap-regions widget (`answer: ["right"]`); `leftLabel` and `rightLabel` name them for screen readers.
- **shareMargins: true** lines up the plot areas of two series (stacked or side by side) by giving both the larger left and right margins.
- The Why? copy of a pair keeps `stack`, `active` and `shareMargins`. The Why? copy is a pair too, with derive run on the explained state.
- **params by name:** derive reads both sides' params; when both sides use the same name, the right side's value wins in plain names, so give each side its own names or read `left.n` and `right.n`.
- An `explain.canvas` patch under the active side's key (`{ "right": {...} }`) wins over the flattened active state, so it shows in the Why? copy.
- A matrix side is drawn at its own width (`fit: true`), and a pair with a matrix side stacks whenever side by side would draw a side below 80% of its size; `minScale: 0.7` sets that threshold on any pair.

**Integration pass 7 additions:** `split: 0.6` (0.3 to 0.7) gives the left side that share of the width (a compact chart beside a wider table). A pair holding `bars` stacks automatically when side by side would shrink a chart below 70% (as matrices do at 80%); `minScale` overrides it.

## Canvas-bound widgets

- **tap-regions** (`answer`, `max`, `wrong: [{ "id", "set", "flash" }]`, `countWord`): works on any canvas with tap mode (grid, tree, venn, area, boxes, table, number-line points, and E4's tappable kinds). Keys: a matching `wrong[]` id, else the first wrongly selected id, else the first missed answer id. `showWhy` flashes the extra ids of the matched set (or `flash`), else the wrong picks. Count mode: `{ "count": 3, "among": ["c11", "c12", "c13", "c14"] }` with no `answer` is correct when exactly `count` regions are selected, all within `among` when given; keys are a matching `wrong[]` id, else the first pick outside `among`, else `too-few` or `too-many`; the count reads "2 of 3 shaded" (with `countWord`); reveal selects the first `count` of `among`.
- **tap-regions** with `ordered: true` grades the order of the taps against `answer` (a BFS visit order on a graph, the cells a search reads on an array); every canvas numbers each selected object 1, 2, 3 as it is tapped; a wrong order returns the key `order` (or the first id that should not be there, or the first missing one), and a `wrong[]` set is read as a sequence. Not with `count`.
- **place** in `mode: "array"` (`answer: ["c2", "c0", "c1"]`, the opening cell ids in the order wanted): the learner drags the cells of an `array` canvas into order; key the first id out of place.
- **place** in `mode: "boxes"` (`answer: { "<container>": [itemIds] }`, `ordered`, or `count: { "<container>": n }`, or `free: true`): the learner drags the canvas's items between containers; correct when every named container holds exactly its listed items. Keys: the first item out of place. `reveal` moves the items there in hint indigo.
- **balance** (`moves: ["remove-both", "remove-unknown-both", "halve-both", "divide-both", "subtract-both", "add-both", "remove-item"]`, `target: { "left": ["unknown"], "right": [4] }`): chips under the canvas and a live equation. Keys: `unbalanced`, `unsolved`. A target matches either way round; weights compare by total. The test hook's correct answer is the shortest list of the allowed moves (at most six) that reaches the target (`ZQ.grade.balanceMoves`), so the target must be reachable with them.
- **drag-point** (`points: [{ "id", "target", "tol" }]`, `wrong: [{ "id", "region": { "x": [a, b], "y": [c, d] } | { "angle": [a, b] }, "canvas": {patch} }]`): targets are `[x, y]`, or a number on number-line (x) and circle (angle). Default `tol` 0.25. Keys: a `wrong[]` id whose region holds a point, else the first point off target (its point id, which `byKey` may use).

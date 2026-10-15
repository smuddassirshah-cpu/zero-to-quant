# Authoring guide: lessons, reviews, homework, exams and drills

This is the contract between content authors and the engine. Every content file is JSON under `app/content/`. `node app/tools/validate.mjs` enforces section 7. Read `PLAN.md` sections 5, 8 and 9 for the engine side, and `design-research.md` sections 5, 8 and 9 for the pedagogy and voice this encodes.

## 1. Lesson file

`content/courses/<course>/<lesson>.json`

```json
{
  "id": "l3-shrinking",
  "course": "conditional",
  "title": "Shrinking the sample space",
  "minutes": 12,
  "objectives": ["Compute a conditional probability by counting what is left", "Explain why the condition shrinks the denominator"],
  "skills": ["cond-shrink"],
  "screens": [ ...8 to 12 screens... ],
  "summary": {
    "ideas": ["A condition throws away every outcome that contradicts it.", "...", "..."],
    "formula": { "name": "Conditional probability", "tex": "P(A \\mid B) = \\dfrac{P(A \\cap B)}{P(B)}", "note": "Count inside B, not inside everything." },
    "trap": "Adding the two chances counts the corner cell twice."
  },
  "quiz": [ ...3 to 5 items... ]
}
```

- `skills` are ids declared in the course's `course.json`. Every lesson names at least one.
- `minutes` is the planned time, 10 to 15.

## 2. Screens

Every screen has `type`, and most have `canvas`, `question` and `widget`. Prose supports inline `$...$` and display `$$...$$` KaTeX, `**bold**`, and fenced code blocks (```python). Keep prose under 60 words per screen.

```json
{
  "type": "problem",
  "difficulty": 2,
  "title": "Optional short heading",
  "prose": "Two fair dice. You learn the first die shows a 5. $P(\\text{total} = 7)$ before and after?",
  "canvas": { "kind": "grid", "params": { ... }, "state": { ... } },
  "question": "How many outcomes are still possible?",
  "widget": { "kind": "numeric", ... },
  "hints": [
    { "rung": "nudge", "text": "Which cells disagree with what you learned?" },
    { "rung": "point", "text": "The first die is fixed.", "highlight": ["r5c1", "r5c2", "r5c3", "r5c4", "r5c5", "r5c6"] },
    { "rung": "step", "text": "Only row 5 survives: six cells. Now count the ones summing to 7 inside that row." }
  ],
  "feedback": {
    "correct": "Six cells survive, one for each second die.",
    "generic": "Not quite right. Count only the cells that agree with the first die showing 5.",
    "byKey": { "36": "You counted the whole table. The condition rules most of it out.", "r5c2": "That cell is in the row, but you shaded more than the row." }
  },
  "explain": {
    "text": "Learning the first die shows 5 keeps row 5 and nothing else. That row is the new whole. Any probability now is a count within it over 6.",
    "canvas": { "shade": { "survivors": ["r5c1","r5c2","r5c3","r5c4","r5c5","r5c6"] }, "outline": "row5" }
  }
}
```

Screen types and what they require:

| type | Purpose | Requires |
|---|---|---|
| `title` | lesson name, one framing sentence, optional canvas in a static state | `prose`; no widget |
| `explore` | free manipulation, then one observation question | `canvas` with an interactive mode (`controls`, a canvas-bound widget, points with `drag: true`, vectors in `state.drag`, or a `sim`), `widget` |
| `problem` | a graded task | `question`, `widget`, `feedback` |
| `ladder` | same canvas, one new constraint | as `problem`; reuse the previous canvas kind |
| `demonstrate` | animated step-through | `steps: [{ "caption": "...", "canvas": {state patch} }]`, 3 to 6 steps; no widget |
| `trap` | the common misconception, met and resolved | as `problem`; at least one `byKey` line naming the misconception |
| `generalise` | the rule as a description of what the learner just did | `prose` with the formula in KaTeX; `widget` with one confirmation item |
| `derive` | complete a missing line | `widget` of kind `expression`, `order` or `choice` |
| `transfer` | same idea in a quant context | as `problem` |
| `summary` | not a screen: the `summary` block renders after the last screen | |

Lesson shape (design-research 8.3): hook (problem or explore), explore, name (generalise comes later, but the term is introduced on this screen by what was just done), ladder 2 to 4 screens, trap, generalise and derive, transfer, then summary and quiz. Eight to twelve screens, at most one `title` and at most two non-task screens (`title`, `demonstrate`, `generalise` without a task) per lesson. Difficulty runs 1 up to 3 across the screens.

`hints`: up to three rungs in the order nudge, point, step. `point` carries `highlight` ids for the canvas. Hints are optional on `explore`, required on `problem`, `ladder`, `trap`, `transfer` and `derive`.

`feedback.byKey`: keys are the `key` values the widget can return (option ids, `wrong[]` ids, region ids, token ids, state ids). Each line names the learner's own action, never the rule. At most three sentences.

The engine's end-of-lesson order is: summary card (last progress step), quiz, celebration with the streak moment, Next or Done.

`explain.text`: at most three sentences, refers to what the learner did, with the `explain.canvas` patch showing the annotated state.

## 3. Widgets

Each `widget` has `kind` and the fields below. `label` is the accessible name of the control.

### `choice`

```json
{ "kind": "choice", "layout": "grid|stack", "options": [
  { "id": "a", "text": "$1/6$", "correct": true },
  { "id": "b", "text": "$1/36$", "why": "You kept the whole table as the denominator." },
  { "id": "c", "text": "$2/6$", "why": "You counted (5, 2) and (2, 5), but (2, 5) is gone." }
] }
```

Exactly one `correct`. Every distractor has `why` (one named misconception each). Options may be text, KaTeX, or `{ "image": "art-id" }` for a course art glyph. `shuffle: true` is allowed except when options are ordered (ranges, steps).

Any `choice` or `multi` option, and any `numeric`, `slider` or `tap-regions` `wrong[]` entry, may carry a `canvas` patch: it is applied by Show why after that wrong answer and reverted on Try again. Use it to show the consequence of the misconception on the diagram (highlight the double-counted cell, mark it `×2`).

### `multi`

Same as `choice`, several `correct`. The question line must say "Select all that apply".

### `numeric`

```json
{ "kind": "numeric", "answer": 0.1667, "tol": { "abs": 0.0005 }, "unit": "", "placeholder": "fraction or decimal",
  "accept": "Any form equal to 1/6, or 0.1667 ± 0.0005",
  "wrong": [ { "id": "whole", "value": 0.0278, "tol": { "abs": 0.001 } }, { "id": "double", "value": 0.3333, "tol": { "abs": 0.001 } } ] }
```

`tol` is `{ "abs": x }` or `{ "rel": r }`. Integers use `{ "abs": 0 }`. `unit` may be `%`, `£`, `$`, or a word; with `%` the learner types 16.7 and the engine compares 0.167. `accept` is shown after grading. Each `wrong` entry id is a `byKey` key.

### `expression`

```json
{ "kind": "expression", "answer": "\\frac{x+1}{2}", "accept": ["(x+1)/2", "x/2+1/2", "0.5x+0.5"],
  "wrong": [ { "id": "forgot-half", "tex": "x+1" } ], "keyboard": "algebra|calculus|probability" }
```

Graded by symbolic equivalence; `accept` is the fallback list of forms (plain text as a learner would type).

`"form": "expanded" | "factorised" | "simplified"` also asks for a shape, for expand and factorise tasks with free entry. Expanded: no bracketed sum left inside a product or power (`2x + 6`, not `2(x + 3)`). Factorised: a product with a bracketed sum among its factors, or a power of one (`2(x + 3)`, `(x + 1)^2`, a leading minus allowed). Simplified: like terms collected and fractions cancelled (`5x`, not `3x + 2x`). An equal answer in the wrong shape returns the key `form` (give it a `byKey` line; the default line says what to do). Without the maths engine the text fallback accepts only `answer` and `accept[]`, so write every accepted form in the asked shape.

### `slider`

```json
{ "kind": "slider", "min": 0, "max": 1, "step": 0.01, "start": 0.5, "bind": "p", "unitLabel": "", "answer": 0.5, "tol": 0.02,
  "wrong": [ { "id": "too-high", "from": 0.6, "to": 1 } ] }
```

`bind` names a canvas parameter the slider drives live (the canvas redraws on every change). Without `answer` the slider is an explore control and the screen's task comes from another widget; in that case put the slider under `canvas.controls` instead (section 4). `"format": "fraction"` shows the value as a fraction in lowest terms (0.375 reads 3/8) on the thumb and the ends; `"percent"` shows 0.375 as 37.5%.

### `drag-point`

```json
{ "kind": "drag-point", "points": [ { "id": "p1", "target": [2, 4], "tol": 0.3 } ],
  "wrong": [ { "id": "on-axis", "region": { "x": [1.5, 2.5], "y": [-0.3, 0.3] } } ] }
```

The canvas must list the same point ids as draggable. On a number-line or circle `target` is a bare number (the x value, or the angle); elsewhere it is `[x, y]`. `tol` is optional (default 0.25). Keys: the id of a `wrong[]` region that holds a point, else the id of the first point that is off target, so `byKey` may speak to a point by its id.

### `place`

```json
{ "kind": "place", "tokens": [ { "id": "t1", "text": "$n!$" }, { "id": "t2", "text": "$(n-k)!$" } ],
  "slots": [ { "id": "num", "label": "numerator", "accepts": ["t1"] }, { "id": "den", "label": "denominator", "accepts": ["t2"] } ],
  "mode": "assign|order" }
```

`mode: "order"` uses one slot and grades the token sequence against `order: ["t1", "t2"]`.

Interchangeable tokens: with `"byText": true` tokens with the same text count as the same token (two `$x$` chips can go either way round); `"same": [["t1", "t2"]]` (or one list) names groups by id instead.

`mode: "boxes"` places the items of the screen's `boxes` canvas: the learner drags them between containers, with no tokens or slots of its own.

```json
{ "kind": "place", "mode": "boxes", "answer": { "hand": ["b2", "b3"] }, "ordered": false }
```

`answer` maps each container id that matters to the item ids it must hold (any order; `"ordered": true` for a row whose order matters); items not listed may be anywhere. Keys: the first item out of place (its item id).

### `tap-regions`

```json
{ "kind": "tap-regions", "answer": ["r5c2", "r2c5"], "max": null,
  "wrong": [ { "id": "double", "set": ["r5c2", "r2c5", "r5c5"] } ] }
```

The canvas provides the regions (grid cells, venn regions, tree branches, area cells, table cells, boxes items, and number-line points by their point ids). The question line shows the running count. Optional: `wrong[].flash` (ids to flash on Show why), `countWord` (the noun in the count, on every canvas; default "shaded" on a grid, else "selected"), `only` (restrict tappable ids).

Count mode, for "shade any 3 of the 4": give `count` instead of `answer`, and optionally `among`.

```json
{ "kind": "tap-regions", "count": 3, "among": ["c11", "c12", "c13", "c14"], "countWord": "parts" }
```

It is correct when exactly `count` regions are selected and, with `among`, every one is in `among`. The count reads "2 of 3 parts". Keys: a `wrong[]` id whose set matches, else the first selected id outside `among`, else `too-few` or `too-many`. Show solution selects the first `count` ids of `among`.

### `order`

```json
{ "kind": "order", "lines": [ { "id": "s1", "text": "Write $P(A \\cap B) = P(A \\mid B)P(B)$" }, { "id": "s2", "text": "..." } ], "answer": ["s1", "s2", "s3"] }
```

Lines are shuffled on render. Per-line marks after grading.

### `table`

```json
{ "kind": "table", "columns": ["x", "P(X=x)"], "rows": [ ["0", { "edit": true, "answer": 0.25, "tol": { "abs": 0.001 } }], ["1", "0.5"] ] }
```

### `manipulate`

An authored state graph. The learner taps an operation; the display animates to the next state.

```json
{ "kind": "manipulate", "start": "s0", "target": "s3",
  "states": {
    "s0": { "tex": "2x + 3 = 11", "ops": [ { "label": "Subtract 3 from both sides", "to": "s1" }, { "label": "Divide both sides by 2", "to": "s0b", "why": "Dividing now leaves a fraction on the left; clear the 3 first." } ] },
    "s0b": { "tex": "x + \\tfrac{3}{2} = \\tfrac{11}{2}", "ops": [ { "label": "Subtract 3/2 from both sides", "to": "s3" } ] },
    "s1": { "tex": "2x = 8", "ops": [ { "label": "Divide both sides by 2", "to": "s3" } ] },
    "s3": { "tex": "x = 4" }
  } }
```

Any path reaching `target` is correct. An op with `why` is a recorded misstep (its `why` is shown on the next Check if the learner has not reached the target).

### `balance`

```json
{ "kind": "balance", "left": [ { "id": "x1", "kind": "unknown", "label": "x" }, { "id": "w3", "kind": "weight", "value": 3 } ], "right": [ { "id": "w7", "kind": "weight", "value": 7 } ],
  "moves": ["remove-both", "halve-both"], "target": { "left": ["unknown"], "right": [4] } }
```

`moves` may include `remove-both`, `halve-both`, `divide-both`, `remove-unknown-both`, `subtract-both`, `add-both`, `remove-item`. Keys returned: `unbalanced`, `unsolved`.

Signed pans, for `x - 3 = 8` or `7 - 3x = 22`: a weight may have a negative `value` (drawn dashed, lifting its pan) and an unknown block may carry `"coef"` (`-1`, `0.5`, `-3`; drawn as `−x`, `½x`, `−3x`). `subtract-both` and `add-both` take any amount, `divide-both` any non-zero number (negatives too), and after each move a pan shows one unknown block (the total coefficient) and one weight block (the total). A target `"unknown"` means $1x$ alone.

```json
{ "kind": "balance", "left": [ { "id": "w7", "kind": "weight", "value": 7 }, { "id": "x", "kind": "unknown", "coef": -3 } ], "right": [ { "id": "w22", "kind": "weight", "value": 22 } ],
  "moves": ["subtract-both", "divide-both"], "target": { "left": ["unknown"], "right": [-5] } }
``` The `target` must be reachable from the starting pans with the listed moves (at most six): the playthrough's correct answer is the shortest such sequence, found by the engine. For `drag-point` on one-dimensional canvases (number-line, circle) `target` is a number (x or angle) and `wrong[].region` may be `{ "x": [a,b] }` or `{ "angle": [a,b] }`; default `tol` is 0.25.

### `sketch`

```json
{ "kind": "sketch", "control": 4, "target": "max(x - 100, 0)", "xRange": [80, 120], "band": 2 }
```

The learner drags control points of a curve on the `plane` canvas; graded on sampled x against the target function within `band` (y units). The control points are evenly spaced over `xRange`; Show solution (and the playthrough) puts each one on the target curve, so choose `control` and `band` so that the smooth curve through those points stays inside the band (a kink between two control points can leave it).

### `code`

```json
{ "kind": "code", "language": "python", "starter": "def max_drawdown(prices):\n    ...\n", "examples": [ { "call": "max_drawdown([100, 90, 95])", "expect": "0.1" } ],
  "tests": [ { "call": "max_drawdown([100, 90, 95])", "expect": "0.1", "compare": "isclose" } ], "how": "Submit runs 8 hidden tests. Each answer is accepted when math.isclose(actual, expected, rel_tol=1e-9)." }
```

`compare` is `isclose`, `equal` or `fraction`. At most 15 tests. Tests run in the Pyodide worker with a 5 s budget each.

## 4. Canvases

The binding reference for every canvas kind is the engine's own documentation: `app/js/engine/canvas/README.md` (grid, tree, venn, number-line, boxes, area, balance, circle, table) and `app/js/engine/canvas/README-B.md` (plane, bars, distribution, scatter, series, walk, matrix, vectors, graph, array, payoff, orderbook). Read the entry for a kind before using it; the table below is the summary and the READMEs win where they differ. Id conventions that differ by kind: grid and area ids are one-based (`r5c1`), table and matrix ids are zero-based (`r0c0`, `A-0-1`), scatter `p{i}` and walk `path{i}` are zero-based, bins are `b{i}`, array `c{i}` uses the displayed index.

`canvas: { "kind": ..., "params": {...}, "state": {...}, "enter": {...}, "controls": [...] }`. `enter` is a state patch applied 350 ms after the screen enters (use it for the "watch the space shrink" moment). Every kind also accepts `state.selected` (the current tap selection), `state.highlight` and `state.caption`. `params` fix the drawing; `state` is the initial state and the thing `explain.canvas`, `demonstrate.steps[].canvas` and `showWhy` patch. `controls` are explore-only sliders bound to params: `[{ "bind": "p", "min": 0, "max": 1, "step": 0.05, "label": "p", "start": 0.5, "format": "fraction" }]`. Where the canvas has its own binds (number-line: a point id moves that point; circle: `angle`; area: `split`, `split.rows`, `split.cols`, `grid`, `grid.rows`, `grid.cols`, `shade`) they are used; otherwise a plain `bind` sets `state.params[name]` and a dotted one such as `strike.c1` sets that state path. A control can also move one item of a list by id: `"bind": "points.p1.x"` (plane, number-line, any kind with `points`). `start` is optional: given, it is the slider's opening value and it is applied to the canvas when the screen opens; left out, the slider opens at the bound value's current value (the point's x, the current split, the param), else at `min`. `format: "fraction"` shows the readout as a fraction (0.375 reads 3/8), `"percent"` as a percentage (37.5%). A bars canvas binds a category label to move that bar. Ids below are the highlightable element ids.

`derive` links values and captions to the state, re-evaluated after every patch, drag and control: `"derive": { "p2.x": "0.8 * p1.x", "caption": "Change: {{round((p1.x / 50 - 1) * 100, 1)}}%" }`. A target is an item property by id (`p2.x`), `values.<label>` on bars, `params.<name>`, `caption` or another state key; an expression uses item ids (`p1.x`), param names, top-level numbers, `values`, and `abs min max sqrt pow exp log floor ceil round(v, places) pi`; a string target fills each `{{expression}}`. Details in README-B ("Linked state").

| kind | params | state | ids |
|---|---|---|---|
| `grid` | `rows`, `cols`, `rowLabel`, `colLabel`, `rowHeads[]`, `colHeads[]`, `cells` (`"sum"`, `"pair"`, `"product"`, or a 2D array of strings), `compact` | `shade: { "<setName>": [ids] }` (sets are drawn with series slots in order), `outline: "row5"|"col3"|"cross5"|[ids]`, `dim: [ids]`, `mark: { "<id>": "✓" }` | `r{i}c{j}` |
| `tree` | `levels: [{ "label": "First draw", "branches": [{ "id": "a", "label": "Red", "p": "3/5" }, ...] }]` or an explicit `nodes` tree with `children`, `leaves: { "<path>": "value" }` | `highlight: [paths]`, `shade: [paths]`, `show: "p"|"none"` , `collapse: [paths]` | branch paths like `a`, `a-b` |
| `venn` | `sets: ["A","B"]` or three, `labels`, `values: { "A": 20, "AB": 5, "B": 10, "none": 15 }`, `mode: "count"|"prob"` | `shade: [regions]`, `show: true|false` | `A`, `B`, `AB`, `C`, `AC`, `BC`, `ABC`, `none` |
| `number-line` | `min`, `max`, `step`, `labels` | `points: [{ "id": "p1", "x": 2.5, "label": "", "labelPos": "above", "drag": true }]` (a point is a plain dot unless `drag: true` or a drag-point widget moves it), `intervals: [{ "id": "i1", "from": 1, "to": 3, "open": [false,true], "labelPos": "below", "row": 1 }]` (`row` 0 sits on the axis, rows stack 16px apart; a side label on a ray goes above it at the edge), `arrows`; `labelPos` is `above`, `below`, `left` or `right` (default: above, or the side away from a jump arrow at that point; close labels stack); keyed patches `{ "points": { "p1": { "x": 3 } } }` work | point and interval ids; points are tappable for `tap-regions` |
| `boxes` | `containers: [{ "id": "urn", "label": "Urn", "items": [{ "id": "b1", "kind": "ball", "colour": 1, "label": "" }] }]`, `itemKind: ball|card|coin|slot|bag` (`bag`, alias `sealed`: a closed sack showing only its label, such as `"?"`; a coin shows H or T unless it has a `label`) | `draw: ["b1"]`, `move: { "b1": "hand" }`, `face: { "c1": "up" }`, `highlight` | item and container ids |
| `area` | `shape: "rect"|"square"|"circle"`, `grid: [rows, cols]` (a circle: `sectors`), `labels` (edges `top`, `bottom`, `left`, `right`, and text on a piece keyed by cell id: `{ "c11": "$3n$" }`; also `state.labels`) | `shade: [cells or fraction]`, `split`, `grid` (re-cuts the shape into a new grid), `point`; controls bind `split`, `grid` or `shade` | `c{i}{j}`, `c{i}-{j}` when either index is 10 or more |
| `balance` | `left`, `right` item lists as in the widget (signed weights and `coef` allowed), `x` | `left`, `right`, `params: { "x": 4 }` (the unknown's value: patchable, and a control can bind `x`) | item ids |
| `circle` | `radius`, `showSin`, `showCos`, `showTan`, `degrees: true|false`, `ticks` | `angle`, `shade: "arc"|"sector"` | `angle`, `sin`, `cos`, `pt` |
| `plane` | `x: [min,max]`, `y: [min,max]`, `grid`, `functions: [{ "id": "f", "expr": "x^2", "label": "f(x)", "domain": [a,b], "labelSide": "above|below", "labelOffset": [dx, dy] }]`, `params: { "a": 1 }` (usable in expr) | `points: [{ "id": "p1", "x": 1, "y": 1, "drag": true, "snap": 0.5, "label": "" }]`, `segments`, `tangent: { "f": "f", "x": 1 }`, `area: { "f": "f", "from": 0, "to": 2 }`, `riemann: { "f": "f", "from": 0, "to": 2, "n": 4, "rule": "left" }`, `vectors`, `params`, `highlight` | function, point, segment ids |
| `bars` | `categories: [...]` or `bins: { "min", "max", "width" }`, `yLabel`, `exact: [{ "x": "7", "y": 0.1667 }]`, `sim: { "trials": [10,100,1000], "outcome": "d6()+d6()", "seed": 7 }`, `showValues` with `decimals` or `money: "£"` | `values: {cat: v}`, `highlight`, `ran: n` | category ids (`x7`) |
| `distribution` | `family`, `params: {...}`, `x: [min,max]`, `showMean`, `showSd` | `shade: { "from": a, "to": b }`, `params` | `mean`, `shade`, `x{k}` for pmf bars |
| `scatter` | `points: [[x,y],...]`, `x`, `y` labels, `fit: true` | `line: { "m": 1, "b": 0 }`, `residuals: true`, `highlight` | `p{i}`, `line` |
| `series` | `series: [{ "id": "px", "label": "Price", "values": [...] }]` (`null` leaves a gap), `x: "dates"|"index"`, `candles: false`, `money: "£"`, `decimals` | `markers: [{ "id": "m1", "i": 30, "label": "peak" }]` (give `"y"` for a marker on a `null` gap), `shade: [{ "from": i, "to": j, "label": "drawdown" }]`, `window` | series and marker ids |
| `walk` | `steps`, `p`, `start`, `paths`, `barriers: [a,b]`, `sim: { "seed": 1 }` | `run: n`, `showMean`, `highlight: [pathIndex]` | `path{i}`, `barrier-up`, `barrier-down` |
| `matrix` | `matrices: [{ "id": "A", "rows": [[1,2],[3,4]], "label": "A" }]`, `ops: ["×", "="]` | `highlight: { "A": { "rows": [0], "cols": [], "cells": [[0,1]] } }`, `pivot`, `rowOp: { "from": 0, "to": 1, "k": -3 }`, `cell` | `A-r0`, `A-c1`, `A-0-1` |
| `vectors` | `x`, `y`, `vectors: [{ "id": "u", "v": [2,1], "label": "u" }]`, `grid` | `show: ["sum","projection","span","scale"]`, `scale: { "u": 2 }`, `drag: ["u"]`, `basis` | vector ids, `sum`, `proj` |
| `graph` | `nodes: [{ "id": "n1", "label": "A", "x": 0.2, "y": 0.3 }]`, `edges: [{ "from": "n1", "to": "n2", "w": 0.3, "directed": true }]`, `markov: true` | `visited: [ids]`, `current`, `highlight`, `distribution: { "n1": 0.5 }` | node and `e-n1-n2` ids |
| `array` | `cells: [5, 2, 9]`, `indexFrom: 0`, `mode: "array"|"stack"|"queue"|"linked"` | `pointers: [{ "id": "i", "at": 0, "label": "i" }]`, `highlight: { "range": [0,2] }`, `cells`, `swap: [i,j]` | `c{i}`, pointer ids |
| `payoff` | `legs: [{ "id": "c1", "type": "call"|"put"|"stock", "side": "long"|"short", "strike": 100, "premium": 3 }]`, `range: [80,120]`, `pl: true` | `strike: { "c1": 105 }`, `spot`, `highlight` | leg ids, `breakeven`, `spot` |
| `orderbook` | `bids: [[price, size]]`, `asks: [[price, size]]`, `depth` | `order: { "side": "buy", "size": 300 }`, `highlight: ["ask0"]`, `fills` | `bid{i}`, `ask{i}`, `spread` |
| `table` | `columns`, `rows`, `align` | `highlight: { "rows": [], "cols": [], "cells": [] }` | `r{i}`, `c{j}`, `r{i}c{j}` |

Every canvas accepts `state.highlight: [ids]` and `state.caption: "text"`. Every patch (`state`, `explain.canvas`, `demonstrate.steps[].canvas`, a wrong answer's `canvas`) may change one item of a list by id: `{ "points": { "p2": { "x": 3 } } }` merges into `p2` and keeps the rest of the list.

Two rendering limits to write around:

- A bare `£` inside `$...$` renders in italic maths type. Write `\\text{£}` in the JSON (for example `$\\text{£}12.50$`), or keep the amount outside the maths.
- Grid cell text (`params.cells` as a 2D array) is plain text and cannot hold KaTeX. Use Unicode where you need it: superscripts such as `2³`, `x²`, the minus sign `−`, `½`.

## 5. Quiz, level review, homework, exam and drill items

An item is a `problem` screen without hints: `{ "id", "difficulty", "skills": [...], "prose", "canvas", "question", "widget", "feedback", "explain" }`. Items in the quiz block of a lesson omit `skills` (they take the lesson's).

- **Quiz** (in the lesson file): 3 to 5 items, difficulty 2 to 3, one attempt each, no canvas interaction beyond static diagrams where possible (scaffold-free).
- **Level review** `review-<n>.json`: `{ "id": "review-1", "course", "level": 1, "items": [6 to 10 items] }`, difficulty 2 to 4, interleaving every lesson of the level.
- **Homework** `homework-<n>.json`: `{ "id", "course", "level", "dueDays": 7, "items": [6 to 12] }`, difficulty 3 to 5 with at least one 5, at least one `longform` item and at least one `code` item (code courses) or one `derive`-style `order`/`expression` item (maths courses). A `longform` item: `{ "kind": "longform", "prompt": "...", "model": "the full model answer in markdown with KaTeX", "rubric": [ { "points": 2, "text": "States the conditioning event" }, ... ] }` summing to 10. On the homework page the learner opens the model answer and the rubric with the Mark my answer button under the item; in a review, practice or redo set the Check button does it. Either way the working then locks and the learner ticks the rubric.
- **Topic exam** `exams/topic-<topic>.json`: `{ "id": "topic-1.5", "topic": "1.5", "name", "minutes": 60, "pass": 0.7, "skills": { "<skill>": "label" }, "items": [...] }`, 20 to 30 items at the 8.4 ramp (20% at 2, 50% at 3, 20% at 4, 10% at 5), every skill of the topic covered.
- **Stage exam** `exams/stage-<n>.json`: `{ "id": "stage-1", "stage": 1, "parts": [ { "kind": "paper", "name", "minutes", "pass", "items": [...] }, { "kind": "check", "name": "A ten-line Python script you wrote runs from the terminal" } ] }`.
- **Drill** `drills/<id>.json`: `{ "id", "name", "course", "skills", "difficulty", "brief": "markdown", "starter", "examples", "tests", "how", "solution" }` (the `code` widget fields plus a model solution shown after verification).

## 6. Voice and teaching rules

From `design-research.md` 9, binding:

- British English. No exclamation marks. No emoji. Sentences of at most 20 words.
- Second person for instructions, "we" for reasoning together.
- Puzzle first. Never state a rule before the learner has used it. Name a term only after it has been used.
- Derive rather than state. Every derivation line carries its justification. No "it can be shown".
- Every lesson has one trap (a `trap` screen) and one edge case somewhere in the ladder or quiz.
- Every distractor encodes one named misconception and its `why` names the learner's action.
- Explanations refer to the learner's action, three sentences at most, with a diagram state.
- Notation: random variables capitals, realisations lower case, vectors bold lower case, matrices bold capitals, `P(\cdot)`, `E[\cdot]`, `Var(\cdot)`, `\ln`, decimals in maths and percentages in prose only. Money is £ or $ consistently within a course.
- Transfer screens use real quant contexts: a bet, a price path, a portfolio, an order book, a dataset, a backtest, a signal.
- Honest about difficulty. Never praise the question. Never praise the learner beyond the sourced lines ("That's it.", "Correct.").
- Concreteness fades: the canvas is interactive early, static by the ladder's end, absent in the quiz where possible.
- Code lessons: explanations annotate only non-obvious lines; show the failing version beside the fix when the lesson is about a pitfall.

Sizing: a course has 3 to 5 levels of 4 to 6 lessons. Each level ends with a review and a homework. Size a course by its topic hours: about 60 h of topic per 12 lessons, within 12 to 30 lessons per course.

## 7. Validation rules (enforced by `tools/validate.mjs`)

Errors:

1. JSON parses; required fields present; ids kebab-case; lesson `id` matches the filename; `course` matches the folder.
2. Screens 8 to 12; at most one `title`; at most two non-task screens; `summary.ideas` has exactly 3; `quiz` has 3 to 5 items.
3. Every `problem`, `ladder`, `trap`, `transfer`, `derive` screen has `question`, `widget`, `feedback.correct`, `feedback.generic` and 1 to 3 hints in rung order.
4. Widget kinds and canvas kinds are known; required widget fields exist; `choice` has exactly one correct and every distractor has `why`; `multi` has at least one correct; `numeric` has a numeric `answer` and `tol`; `tap-regions` has `answer`, or `count` (a whole number no larger than `among`), and its `answer` and `among` ids exist in the canvas (for `grid`, `venn`, `area` with `c{i}{j}` or `c{i}-{j}` from 10 up, `table`, and `number-line` point ids); `drag-point` targets are `[x, y]`, or a bare number on a number-line or circle; list fields (`options`, `among`, `tokens`, `slots`, `lines`, `points`, `wrong`, `hints[].highlight` and list answers) are lists, and a field of the wrong shape is one error, never a crash; `expression` `form` is `expanded`, `factorised` or `simplified`; `place` in `boxes` mode names containers and items on its boxes canvas; `balance` `moves` are known and the `target` is reachable with them (the engine's own solver); `order` answer is a permutation of line ids; `place` slots accept known tokens; `manipulate` target is reachable from start; `code` has at least 3 tests.
5. Every `feedback.byKey` key is a key the widget can produce (this includes `form` for an `expression` with `form`, item ids for `place` in `boxes` mode, `too-few` and `too-many` for a `tap-regions` in count mode, and point ids for `drag-point`); every `hints[].highlight` id is a plausible id for the canvas kind.
6. `difficulty` 1 to 5 and within the range for the context; quiz items 2 to 3; review 2 to 4; homework 3 to 5 with one 5; exams at the ramp within ±10%.
7. `skills` exist in the course; every course skill is used by at least one lesson.
8. Copy rules: no `!` in prose, question or feedback; no emoji; no "it can be shown"; no American spellings from a fixed list (color, center, favorite, analyze, optimize, behavior, modeling, labeled, math class... the validator ships the list).
9. KaTeX: every `$...$` is balanced; `\\` is escaped in JSON.
10. Course: levels 3 to 5, lessons per level 4 to 6, every lesson file referenced exists or is listed in `--summary` as unwritten (warning, not error); `review` and `homework` files exist for every level (warning until written).

Warnings: prose over 60 words; a screen without a canvas in a `problem` before the ladder's end; a lesson with no `transfer`; a quiz with any interactive canvas.

## 8. A complete minimal example

See `content/courses/conditional/l3-shrinking.json` (the reference lesson, ported from the prototype) and `content/courses/conditional/course.json`.

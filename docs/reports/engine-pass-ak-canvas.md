# Engine pass AK canvas (AI strand A3, canvas part)

Source: `docs/briefs/ai-strand-curriculum.md` "Engine work" items 1 to 3, finding F13 of `docs/reviews/review-ai-strand.md` (no new `network`, `compgraph`, `contour`, `tokens` or `kernel` canvases). Backlog items 1227 to 1229 (highest existing 1217, plus 10).

## What was built (all opt-in by new keys)

**1227 graph** (`app/js/engine/canvas/graph.js`)
- `params.valueLines: [{ label, colour }, ...]` (one or two). `state.values` is line one, new `state.values2` line two, drawn under the node as `label = value` in the line's colour token (slot 1 to 6, `ink`, `manip`, `hint`, `neg`, `pos`, `muted`). `valueSide` places the pair (below, above, left, right); frame padding grows 16 px with two lines.
- `params.edgeWidth: true | { min, max, norm, sign }`: stroke width from `|w|` (`min` px at zero, `max` px at `|w| = norm`, default the largest). A negative weight is dashed; `sign: "colour"` (default) draws positive edges `--div-pos` and negative `--div-neg`, `"dash"` leaves colour alone. An edge's own `colour` wins.

**1228 matrix** (`matrix.js`)
- Per matrix `heat: true | { mode: "seq" | "div", range, legend, decimals, label }`. Sequential walks `--seq-1` to `--seq-6` via `color-mix`; diverging mixes `--div-mid` towards `--div-pos` or `--div-neg`, symmetric. Mode is automatic (diverging when any entry is negative). A colour bar legend with end values (and 0) sits under the matrix (+30 px) unless `legend: false`. Text on the strong end takes the page colour (`.cvb-heat-hi`), which works in both themes because the sequential ramp reverses in dark. Non-numeric and KaTeX cells get no fill. Follows `state.rows` and `state.values`.

**1229 grid** (`grid.js`)
- `state.arrows`: rows-by-cols list or `{ r2c3: "up" | { dir, colour } }`; directions up, down, left, right, none. SVG shapes, so no font dependency. A cell with text keeps it, the arrow moves up and the text drops. The arrow layer joins the DOM only while arrows exist; `"arrows": null` removes it.

## Validator (`app/tools/validate.mjs`)
Types and sizes: `valueLines` is one or two `{ label, colour }`; `values2` needs two lines and node ids that exist (also `values`, when nodes are listed in params and not a lattice); `edgeWidth` shape, `min <= max`, numeric `w`; matrix `heat` mode, range (two numbers, lo below hi), legend, decimals, and a sequential heat with negative entries needs a range; grid `arrows` list is exactly `rows` by `cols`, ids inside the grid, direction names, colour 1 to 6.

## Unchanged rendering
Graph without the keys: no `.cvb-vline`, no inline edge style (tested on an l17-like spec). Matrix without `heat`: no heat rect or legend, same frame height. Grid without arrows: no layer, no text transforms. `node tools/validate.mjs`: 0 errors.

## Tests
- `app/tools/test-validate-canvas-ai.mjs`: 7 good and 24 bad scratch cases on the mini-app fixture (all pass).
- `app/tools/test-canvas-ai.mjs` (Playwright, light and dark at 1280 and 440 px): line text and distinct colours, edge widths, dashed red negative edge, no overflow, heat fills, legend, text flip, contrast at least 3 to 1 on every heat cell in both themes (sequential and diverging), arrows count and text moves, nothing extra without the keys (all pass).
- Also re-run: `test-validate-harness.mjs`, `test-validate-dice-sim.mjs` (pass). Playthrough smoke `--all --changed --shard 1/16` ran in the background; see the status line in the hand-back.

## Gallery
Three entries in `app/js/screens/system.js`: "graph (computation graph)", "matrix (heat, attention and signed)", "grid (policy arrows)". Screenshots checked in light and dark at 440 px.

## Docs
`README-B.md` (graph, matrix), `README.md` (grid), `docs/AUTHORING.md` section 4 (one paragraph), `docs/ENGINE-BACKLOG.md` (items and status block).

## Not done
No heat on `plane` or `table`; no arrow tap targets; `valueLines` is capped at two. The `trainer` canvas (brief item 4) is another agent's.

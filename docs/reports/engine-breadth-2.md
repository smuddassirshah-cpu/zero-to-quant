# Engine breadth pass 2: integration report (items 429 to 437 and 241)

Five parallel agents built the engine parts; this pass wired their shared-file changes, added the gallery examples, merged the documentation and ran the full playthrough. Part reports, for detail:

- [grading](engine-breadth-2-grading.md): 429, 430, 433, 434, 437 (`grade.js`, `expression.js`, `order.js`, `code.js`, `cpp-grade.js`)
- [plane](engine-breadth-2-plane.md): 431
- [cmap-vectors](engine-breadth-2-cmap-vectors.md): 432 (complex half), 435
- [walk](engine-breadth-2-walk.md): 436
- [space](engine-breadth-2-space.md): 432 (3D half), 241

## What was integrated

- `app/index.html`: script tags for `complex-map.js` (after `vectors.js`) and `space.js` (after `orderbook.js`). No other file lists canvas scripts (the playthrough and the sample page read `ZQ.canvas.kinds`).
- `app/tools/validate.mjs`: the grading patch (C++ complex `expect`, `order` `distractors`, `length` key, the capital N and D warning removed), the plane field rules, the `vectors` matrix rules and the `complex-map` rules (the validator now `require`s `complex-map.js` for `compile`), the walk rules and `PLAUSIBLE.walk` ids, and the `space` checker with its `regionIds` branch; `complex-map` and `space` are in `CANVASES`. The patches touch different places and did not conflict. Checked on scratch lessons: good canvases of each kind give no error, bad ones give one error per fault with the right path (plane 7, complex-map 5, vectors 3, walk 9, space 4, plus `order` and C++ cases).
- `app/js/engine/canvas/plane.js`: one line, `isStatic = !!(ctx.static || ctx.mode === 'static')`, so every `ZQ.cvb` canvas in the Why? sheet is a still copy (the player passes `mode: 'static'`). `space.js` keeps its own mapping, which is now redundant but harmless. Checked with `playthrough --why --shots` on `limits/l1-getting-closer` (plane and table in the sheet): passes, the plane copy has no live controls.
- Playthrough: no change needed (`drag-point` on `complex-map` works through `points()` and `place()`).
- `app/js/screens/system.js`: `CANVAS_SAMPLES` and `CANVAS_ABOUT` entries for `complex-map` and `space`; the gallery cards listed below; the code card now loads Pyodide on request for every Python variant, and a failed check shows the line (`... key "length". Your answer has 2 components...`).
- `vectors (transform)` gallery sample: its vectors now move with the transform. Chosen: keep them moving (not `fixed: true`), relabel them `$T\mathbf{u}$` and `$T\mathbf{w}$` and say in the blurb that the angle mark follows the images and `fixed: true` opts a vector out. That shows what an author gets by setting `transform`; the unmoved reference arrow is shown in the new "matrix moves every vector" card.
- Docs: `docs/AUTHORING.md` (expression, order, code Python and C++, canvas table rows for `complex-map` and `space`, new `walk` row, derive values for `walk`, an "Engine breadth pass 2" group of paragraphs, section 7 rules), `app/js/engine/canvas/README-B.md` (plane layers, walk additions, the `vectors` matrix bullets, new `complex-map` and `space` sections, title line), `docs/ENGINE-BACKLOG.md` (see below).

## Items

| item | author-facing options | state |
|---|---|---|
| 429 | `expression`: an `i` (or `\mathrm{i}`) makes both sides complex; real and imaginary parts compared at every seeded point; `\overline{}` and `\bar{}` are the conjugate | done, 1,837 old answer and wrong pairs unchanged |
| 430 | `code` `compare: "isclose"`: complex results and `expect` in Python (`cmath.isclose`, NumPy complex too); in C++ `expect: { "re": 5, "im": 5 }`, `CHECK_CLOSE` takes complex | done |
| 431 | `plane`: `field { id, P, Q, grid, normalise, colourBy: "magnitude", range }`, `slopeField { id, f }`, `trajectory { id, in, from, starts, back, length, step, by: "arc", maxSteps }`; `values()` gives `<id>EndX`, `<id>EndY` | done |
| 432 | `complex-map { f, params, x, y, wx, wy, grid, gridStep, rStep, rays, unitCircle, curves, points, stack }`, derive `p1.u`, `p1.v`; `space { x, y, z, camera, perspective, points, vectors, curves, lines, surfaces, planes, fields }`, `bind: "az"`, derive `values.P` | done (both halves) |
| 433 | `expression`: a vector or matrix answer (`(2, -1, 3)`, `pmatrix`, `\langle\rangle`); wrong size returns key `length` | done |
| 434 | `order`: `distractors: [ids]`, keys are the distractor id and `left-out`; `same` already existed | done |
| 435 | `vectors`: `state.matrix` or `transform` maps every vector (`fixed: true` opts out), drag stores the preimage, derive reads `matrix`, `m11` to `m22`, `det`, `trace`, `image.<id>` and may write `matrix` | done |
| 436 | `walk`: `overlays` (`sq`, `ratio`, `bankroll`, `{ id, expr }`), `showStopped`, `stopAt`, `drawn`, `lower` and `upper` (slider-bindable), `model: "ou"` with `theta`, `mu`, `sigma`, derive `values.stopped` and friends | done |
| 437 | `expression`: `\min`, `\max`, capital `N` and `D`, `\epsilon` equals `\varepsilon` | done |
| 241 | covered by `space` (spans and planes as translucent patches, vectors from origin or base, rotation) | done by 432 |

## Gallery examples added (`#system`)

Widgets: `expression (complex)`, `expression (vector)`, `order (distractors)`, `code (complex)` (Python), `code (C++ complex)`.
Canvases: `plane (vector field)`, `plane (slope field)`, `plane (dragged trajectory)`; `complex-map` (sample), `complex-map (slider f, dragged z)`, `(side by side)`, `(1/z, poles)`, `(exp and log)`, `(log, branch cut)`; `vectors (matrix moves every vector)`, `vectors (derived matrix, dragged head)`; `walk (overlays under the walk)`, `(stopped average, slider barriers)`, `(optional stopping with drift)`, `(mean-reverting)`, `(custom overlay, fixed stop)`; `space` (sample), `space (vectors and a span)`, `(helix and tangent)`, `(surface z = f(x, y))`, `(mesh, height and a sphere)`, `(vector field)`.

Screenshots (all in `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/gallery-shots/`): `<card>-<light|dark>-<desktop|mobile>.png` for each of the 28 cards (112 files, desktop 1280 wide, mobile 390 wide at 2x), for example `plane-vector-field-light-desktop.png`, `complex-map-slider-f-dragged-z-dark-mobile.png`, `space-surface-z-f-x-y-light-mobile.png`. Interaction states, light and dark: `interact-expression-complex-{right,wrong}-*.png` (the conjugate shows key `conj`), `interact-expression-vector-{wrong,right}-*.png` (the `length` line), `interact-order-{filled,right,wrong}-*.png`, `interact-code-complex-{start,wrong,right}-*.png`, `interact-code-c-complex-{start,wrong,right}-*.png`. Every screenshot was looked at. Nothing was clipped, overlapping or unreadable in either theme at either width. Two screenshot-only problems were fixed in the script (sticky bars over a card; element screenshots misplaced on mobile). The first light C++ run read "compiler still loading": the script clicked Check before the compiler was ready; the second pass is correct.

## Playthrough (local CDN, `--local-cdn` on the pkgs folder)

RESULTS_PLACEHOLDER

## Follow-ups

Numbered in `docs/ENGINE-BACKLOG.md`: 438 to 444 the `space` follow-ups (3D drag, true arrowheads, exact intersections, wheel zoom and auto-rotate, tangent-plane shorthand, smooth shading, highlight glow), 445 (done by `complex-map`), 446 a bare `i` in a real answer is now the imaginary unit (only `markov/homework-3` uses it and it still passes), 447 `drill.js` keeps a float-only `isclose`, 448 `complex-map` tap mode, grid domain, curve labels and a conformal grid.

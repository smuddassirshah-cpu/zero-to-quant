# Engine breadth 2: complex-map canvas and vectors matrix (items 432 complex half, 435)

Owned files: `app/js/engine/canvas/vectors.js` (edited) and `app/js/engine/canvas/complex-map.js` (new). Nothing else in the repo was touched. Everything below under "Shared-file changes" is for the integration agent.

## What changed

### Item 435, `vectors`: the matrix acts on every vector and derive can read it
- `state.matrix` (or `state.transform`) now maps every vector it does not skip: a vector is drawn as its image, `from: [x, y]` tails are mapped too, and chain tails follow their vector. `sum`, `project`, `span`, `lines`, `angles` and `segments` that name vectors therefore work on the images. `fixed: true` on a vector keeps it unmapped (a reference arrow). Points and bare-coordinate segment ends are not mapped (a drag-point target keeps its meaning).
- Dragging: the pointer is in the image plane, so the stored `v` is the preimage `M^-1 p / scale`. A singular matrix uses the pseudo-inverse (rank 1: `M^T p / |M|^2`), so the head slides along the image line. Keyboard drag, `points()` (heads as drawn) and `place(id, [x, y])` (drawn position) follow the same rule. `lockTo` is applied in vector space after the inverse.
- Derive: with a matrix set, `get()` adds to `state.params` (which a derive reads by name): `matrix`, `m11`, `m12`, `m21`, `m22`, `det`, `trace` and `image.<id>` (each vector's arrow as drawn: matrix applied unless `fixed`, then `scale`). The stored state is not changed, and nothing is added when no matrix is set. A derive can also write the matrix: `"matrix": "[[a, b], [c, d]]"` from sliders bound to params `a` to `d`, or `"matrix": "[[cos(t), -sin(t)], [sin(t), cos(t)]]"`.
- Current behaviour checked first: `matrix` and `transform` only drew the basis grid, `b1`, `b2` and the unit square; vectors stayed put. No lesson, set or exam in `app/content/` sets `matrix` or `transform` on a `vectors` canvas with vectors or binds `m11` to `m22` (the one `matrix` hit, `exams/topic-1.4.json` item a-det-area, has no vectors). `state.basis` (used by eigen l3, l13, vectors l6 and elimination l7) is unchanged and does not move vectors.
- Side effect to know: the gallery sample `vectors (transform)` in `system.js` sets a transform and two vectors, so `u` and `w` now move with it (and the angle mark follows). Add `fixed: true` to both if the old look is wanted; the new look is arguably the point of the sample.

### Item 432, complex half: new canvas kind `complex-map`
- A z-plane panel beside a w-plane panel (equal units in both, so angles stay true; `x`, `y`, `wx`, `wy` are minimum ranges and the longer side of each box shows more). Stacks vertically when the column is under 500 px (a `ResizeObserver` re-lays it out; `params.stack: true | false` forces either).
- `f` is a formula in `z` with `+ - * /`, `^` (or `**`), unary minus, implicit multiplication (`2z`, `a z`, `2(z + 1)`), `i`, `pi`, `e`, `exp`, `log` (alias `ln`, principal), `sqrt`, `sin`, `cos`, `tan`, `sinh`, `cosh`, `tanh`, `conj`, `abs`, `arg`, `re`, `im`, `pow(a, b)`. Names in `params.params` and `state.params` are numbers usable in `f`, so a slider binds them. Whole powers use repeated multiplication (exact, no branch cut); other powers are `exp(b log a)`.
- Drawing: Cartesian grid (`grid-x` for Re z = const, `grid-y` for Im z = const), polar grid (`grid-r` circles, `grid-th` rays), the unit circle, authored `curves` and `points`. Each curve is sampled (180 to 240 points) and subdivided where an image step exceeds 9 px (to 12 levels), clipped to the panel exactly (Liang-Barsky), broken at a pole or a branch-cut jump (a step still over 30 px at the finest level) and closed in on at a limit (so `log z` runs on to the left edge). A segment wholly beyond one edge is skipped without subdividing. Rendering is cached on formula, params, layout and grid, so dragging `z` redraws only the dots.
- A point `{ id, x, y, label, drag }` is z; its image f(z) is drawn in the w-plane (hollow and pinned to the edge when it lands outside the view; `f(<label>)` label, or `imageLabel`). `drag: true` makes z draggable (mouse, touch, arrow keys); the `drag-point` widget works through `points()` and `place()` with `[x, y]` targets in the z-plane.
- Derive: each point in `get()` carries `u` and `v`, the real and imaginary parts of f(z) (`p1.u`, `p1.v`). A control binds a params name (`a`) or a path (`points.p1.x`).
- Theme: marks use the slot colour classes, ink and the existing `cvb-` classes only (no CSS change), so both themes work; checked below.

## How it was checked
- Scratch copy of `app/` at `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap/` with the new files, the script tag and gallery examples in its `index.html` and `js/screens/system.js`. Never in the repo.
- Regression, no matrix: all 126 `vectors` canvases in `app/content/` (35 files) rendered with the old `vectors.js` (from `git show HEAD`) and the new one in two browsers, SVG compared byte for byte (uid-normalised): 0 differences, 0 throws. Script: `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-regress.mjs`.
- Matrix behaviour (Playwright, `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-vtest.mjs`): `[[2,0],[0,1]]` maps (1,1) to (2,1), `fixed` stays; `derive` caption reads `det`, `trace`, `image.u`; `place` takes drawn coordinates; a patched matrix and a cleared one (`matrix: null`) redraw; `transform: { angle: 90 }` gives the rotation and maps a `from` tail; a drag on a singular matrix `[[1,1],[1,1]]` to (2, 0) stores `v = (0.5, 0.5)`, image (1, 1).
- complex-map (`/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-ctest.mjs`): 15 formulas (`1/z`, `tan(z)`, `1/(z^2-1)`, `exp(1/z)`, `sqrt`, `log`, `sin(z)/z`, Mobius, `abs(z) + i*arg(z)`, `conj(z)^2`, `z^1.5` and others) with both grids and the unit circle: no non-finite path coordinate, longest drawn step 9 px except 22 and 30 px at a branch cut and at the essential singularity of `exp(1/z)`; 8 to 118 ms to build (first call includes JIT), about 2 ms per redraw while dragging a point, about 16 ms when a slider forces a rebuild. Layout flip (`/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-rtest.mjs`): viewBox `0 0 540 286` at 540 px, `0 0 358 678` at 358 px, back at 540; a `clone()` (the Why? copy) stacks at its width and has no handles. Formula parser checked on 15 good and 7 bad inputs (signed zero fixed so `log(-1)` is +pi).
- Screenshots in both themes, desktop (`name-light.png`, `name-dark.png`), mobile 390 px wide (`-390`), and after a slider move and a drag (`-moved`), all in `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/` (script `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shoot.mjs`, run from the scratch copy, which hides the page's sticky bars). Names: `complex-map-slider-f-dragged-z`, `complex-map-side-by-side`, `complex-map-1-z-poles`, `complex-map-exp-and-log`, `complex-map-log-branch-cut`, `vectors-matrix-moves-every-vector`, `vectors-derived-matrix-dragged-head`. For example `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/complex-map-slider-f-dragged-z-light.png`, `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/complex-map-slider-f-dragged-z-dark-390.png`, `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/vectors-matrix-moves-every-vector-moved.png`. The gallery card is about 470 px wide, so the default examples show the stacked layout there; `complex-map-side-by-side` forces `stack: false` and shows the 540 px layout.
- Repo: `node tools/validate.mjs` from `app/`: 0 errors. `node tools/playthrough.mjs` with `--local-cdn /tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/pkgs` on every lesson, set and exam whose JSON has a `vectors` canvas: 29 lessons (counting l9 to l13, eigen l1, l3, l5, l13, elimination l5 to l7, least-squares l1 to l7, trig l12, vectors l1 to l3, l5 to l10), `counting/review-3`, `counting/homework-3`, `vectors/review-2`, `vectors/homework-2`, `topic-0.3`, `topic-1.4`: all passed (no failure, no re-run needed). I did not run the full `--all`: four sibling agents were editing `plane.js`, `walk.js`, grading and the 3D canvas at the same time, so a full run would not isolate my change; the integration agent should run it once everything is in. `vectors.js` is the only existing engine file I changed, and the regression above covers every canvas that uses it.

## Shared-file changes (for the integration agent)

### 1. `app/index.html`
After the `vectors.js` tag (line 51), add:
```html
<script src="js/engine/canvas/complex-map.js"></script>
```
`complex-map.js` also loads under node (`require`) for the validator: it only registers the canvas when `window.ZQ` exists, and exports `{ compile }`.

### 2. `app/tools/validate.mjs`
Add `'complex-map'` to the `CANVASES` set (after `'vectors'`). Then apply the rest of this diff (an `import`, a `require` of the compiler, and two rule blocks in `checkCanvas`, placed before the `(c.controls || []).forEach` block). Written against the file as it stood; the `CANVASES` hunk below is only the line to change.
```diff
--- app/tools/validate.mjs	2026-10-27 20:25:37.709979537 +0000
+++ /tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap/tools/validate.mjs	2026-10-27 20:51:24.110819921 +0000
@@ -13,6 +13,8 @@
 import path from 'node:path';
 import vm from 'node:vm';
 import { fileURLToPath } from 'node:url';
+import { createRequire } from 'node:module';
+const cmap = createRequire(import.meta.url)('../js/engine/canvas/complex-map.js'); // { compile }: formula check for complex-map (item 432)
 
 const HERE = path.dirname(fileURLToPath(import.meta.url));
 const APP = path.resolve(HERE, '..');
@@ -30,7 +32,7 @@
 /* ---------- Vocabulary ---------- */
 const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
 const WIDGETS = new Set(['choice', 'multi', 'numeric', 'expression', 'slider', 'sliders', 'drag-point', 'place', 'tap-regions', 'order', 'table', 'manipulate', 'balance', 'sketch', 'code', 'longform']);
-const CANVASES = new Set(['pair', 'grid', 'tree', 'venn', 'number-line', 'boxes', 'area', 'balance', 'circle', 'plane', 'bars', 'distribution', 'scatter', 'series', 'walk', 'matrix', 'vectors', 'graph', 'array', 'payoff', 'orderbook', 'table', 'console']);
+const CANVASES = new Set(['pair', 'grid', 'tree', 'venn', 'number-line', 'boxes', 'area', 'balance', 'circle', 'plane', 'bars', 'distribution', 'scatter', 'series', 'walk', 'matrix', 'vectors', 'complex-map', 'graph', 'array', 'payoff', 'orderbook', 'table', 'console']);
 const SCREEN_TYPES = new Set(['title', 'explore', 'problem', 'ladder', 'demonstrate', 'trap', 'generalise', 'derive', 'transfer']);
 const GRADED = new Set(['problem', 'ladder', 'trap', 'transfer', 'derive']);
 const CANVAS_BOUND = new Set(['tap-regions', 'drag-point', 'sketch', 'balance', 'slider', 'sliders']);
@@ -625,6 +627,33 @@
   if (c.kind === 'table' && P.tap != null && P.tap !== 'rows') err(file, `${where}.params.tap`, 'tap is "rows" (or leave it out to tap cells)');
   if (c.kind === 'tree' && S.current != null && typeof S.current !== 'string') err(file, `${where}.state.current`, 'current is a branch path such as "a-b", or "root"');
   if (c.kind === 'vectors' && P.points != null && !(Array.isArray(P.points) && P.points.every(q => isObj(q) && typeof q.x === 'number' && typeof q.y === 'number'))) err(file, `${where}.params.points`, 'points is a list of { id, x, y, label }');
+  /* item 435: vectors state.matrix [[a, b], [c, d]] (or transform { angle, shear, scale }) moves every vector not marked fixed: true */
+  if (c.kind === 'vectors') {
+    const okNum = (v) => typeof v === 'number' && Number.isFinite(v);
+    if (S.matrix != null && !(Array.isArray(S.matrix) && S.matrix.length === 2 && S.matrix.every(r => Array.isArray(r) && r.length === 2 && r.every(okNum)))) err(file, `${where}.state.matrix`, 'matrix is [[a, b], [c, d]], four numbers (a derive may write it: "matrix": "[[a, b], [c, d]]")');
+    if (S.transform != null && !(isObj(S.transform) && Object.values(S.transform).every(okNum))) err(file, `${where}.state.transform`, 'transform is { angle (degrees), shear, scale }, all numbers');
+    [...listOf(P.vectors), ...listOf(S.vectors)].forEach((v, i) => { if (isObj(v) && v.fixed != null && typeof v.fixed !== 'boolean') err(file, `${where}.vectors[${i}].fixed`, 'fixed is true or false (true: the matrix does not move this vector)'); });
+  }
+  /* item 432: complex-map, a z-plane beside the w-plane image of f(z) */
+  if (c.kind === 'complex-map') {
+    const okNum = (v) => typeof v === 'number' && Number.isFinite(v);
+    ['x', 'y', 'wx', 'wy'].forEach(k => { if (P[k] != null && !(Array.isArray(P[k]) && P[k].length === 2 && P[k].every(okNum) && P[k][0] < P[k][1])) err(file, `${where}.params.${k}`, `${k} is [min, max] with min below max`); });
+    [['params', P.grid], ['state', S.grid]].forEach(([w, v]) => { if (v != null && !['cartesian', 'polar', 'both', 'none'].includes(v)) err(file, `${where}.${w}.grid`, 'grid is "cartesian", "polar", "both" or "none"'); });
+    ['gridStep', 'rStep'].forEach(k => { [['params', P[k]], ['state', S[k]]].forEach(([w, v]) => { if (v != null && !(okNum(v) && v > 0)) err(file, `${where}.${w}.${k}`, `${k} is a number above 0`); }); });
+    [['params', P.rays], ['state', S.rays]].forEach(([w, v]) => { if (v != null && !(Number.isInteger(v) && v >= 0)) err(file, `${where}.${w}.rays`, 'rays is a whole number, 0 or more'); });
+    [['params', P.unitCircle], ['state', S.unitCircle], ['params', P.stack]].forEach(([w, v], i) => { if (v != null && typeof v !== 'boolean') err(file, `${where}.${w}.${i === 2 ? 'stack' : 'unitCircle'}`, 'true or false'); });
+    const named = { ...(isObj(P.params) ? P.params : {}), ...(isObj(S.params) ? S.params : {}) };
+    Object.entries(named).forEach(([k, v]) => { if (!(okNum(v) || (Array.isArray(v) && v.length === 2 && v.every(okNum)))) err(file, `${where}.params.params.${k}`, 'a name in f is a number (or [re, im])'); if (!/^[A-Za-z_][A-Za-z_0-9]*$/.test(k) || ['z', 'i', 'e', 'pi'].includes(k)) err(file, `${where}.params.params.${k}`, 'a name in f is letters, digits and _, and not z, i, e or pi'); });
+    const names = ['z', ...Object.keys(named).filter(k => k !== 'z')];
+    [['params.f', P.f], ['state.f', S.f]].forEach(([w, v]) => { if (v == null) return; if (typeof v !== 'string') { err(file, `${where}.${w}`, 'f is a formula in z, such as "(z - 1)/(z + 1)"'); return; } try { cmap.compile(v, names); } catch (er) { err(file, `${where}.${w}`, `f does not read: ${er.message}`); } });
+    [['params', P.curves], ['state', S.curves]].forEach(([w, list]) => listOf(list).forEach((q, i) => {
+      if (!isObj(q)) return;
+      if (typeof q.z !== 'string') err(file, `${where}.${w}.curves[${i}].z`, 'a curve is { z: "formula in t", t: [from, to] }');
+      else { try { cmap.compile(q.z, ['t', ...names.filter(k => k !== 'z')]); } catch (er) { err(file, `${where}.${w}.curves[${i}].z`, `does not read: ${er.message}`); } }
+      if (q.t != null && !(Array.isArray(q.t) && q.t.length === 2 && q.t.every(okNum))) err(file, `${where}.${w}.curves[${i}].t`, 't is [from, to]');
+    }));
+    [['params', P.points], ['state', S.points]].forEach(([w, list]) => listOf(list).forEach((q, i) => { if (isObj(q) && !(okNum(q.x) && okNum(q.y))) err(file, `${where}.${w}.points[${i}]`, 'a point is { id, x, y, label, drag }: x and y are the real and imaginary parts of z'); }));
+  }
   (c.controls || []).forEach((k, i) => {
     if (!k.bind && !k.reseed && k.frames == null) err(file, `${where}.controls[${i}].bind`, 'required');
     if (k.frames != null && !(Array.isArray(k.frames) && k.frames.length >= 2 && k.frames.every(isObj))) err(file, `${where}.controls[${i}].frames`, 'frames is a list of at least two state patches');
```
Rules added: vectors `state.matrix` is `[[n, n], [n, n]]`, `state.transform` numbers only, vector `fixed` boolean; complex-map `x`, `y`, `wx`, `wy` are `[min, max]` with min below max, `grid` is `cartesian | polar | both | none` (params and state), `gridStep` and `rStep` above 0, `rays` a whole number, `unitCircle` and `stack` booleans, names in `params.params` are numbers (or `[re, im]`) and not `z`, `i`, `e`, `pi`, `f` (params and state) compiles with those names, each curve has a compiling `z` (variable `t`) and `t: [from, to]`, each point has numeric `x` and `y`. Tested in a scratch copy with one good lesson canvas (0 errors) and one bad one (19 errors, one per fault above, each with its own path).

### 3. `app/tools/playthrough.mjs`
No change needed. A `drag-point` widget on a `complex-map` works through `points()` and `place()` (targets `[x, y]` in the z-plane); `canvas.controls` bind through `setParam`.

### 4. `app/js/screens/system.js` (gallery)
Add this entry to `CANVAS_SAMPLES` (the gallery warns about a kind with no sample):
```js
    "complex-map": {"params": {"f": "z^2", "x": [-2, 2], "y": [-2, 2], "wx": [-4, 4], "wy": [-4, 4], "grid": "cartesian", "unitCircle": true, "zLabel": "z-plane", "wLabel": "$w = z^2$"}, "state": {"points": [{"id": "p1", "x": 1, "y": 0.5, "label": "$z$", "drag": true}]}},
```
Add these entries at the start of `CANVAS_EXTRAS` (complex-map with a slider-bound f and a dragged z, then poles, exp, log, and the vectors matrix examples; the first and the last two are the ones asked for). Screenshots: `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/complex-map-slider-f-dragged-z-light.png`, `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/complex-map-slider-f-dragged-z-dark-390.png`, `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/vectors-matrix-moves-every-vector-light.png`, `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/cmap-shots/vectors-derived-matrix-dragged-head-moved-390.png`.
```js
    { name: 'complex-map (slider f, dragged z)', about: 'f(z) = z + a/z: a Cartesian and polar grid, the unit circle and a draggable z; the slider a reshapes f, derive reads p1.u and p1.v', spec: { kind: 'complex-map',
      params: { f: 'z + a/z', params: { a: 1 }, x: [-2, 2], y: [-2, 2], wx: [-3, 3], wy: [-3, 3], grid: 'both', rays: 12, unitCircle: true, zLabel: '$z$-plane', wLabel: '$w = z + a/z$' },
      state: { points: [{ id: 'p1', x: 0.8, y: 0.6, label: '$z$', drag: true }], caption: 'Drag $z$.' },
      derive: { caption: 'z = {{fixed(p1.x, 2)}} + {{fixed(p1.y, 2)}}i, f(z) = {{fixed(p1.u, 2)}} + {{fixed(p1.v, 2)}}i, a = {{a}}' },
      controls: [{ bind: 'a', min: 0.2, max: 1.6, step: 0.1, start: 1, label: 'a' }] } },
    { name: 'complex-map (side by side)', about: 'stack: false keeps the panels side by side whatever the width', spec: { kind: 'complex-map',
      params: { f: 'z^2', stack: false, x: [-2, 2], y: [-2, 2], wx: [-4, 4], wy: [-4, 4], grid: 'cartesian', unitCircle: true, wLabel: '$w = z^2$' },
      state: { points: [{ id: 'p1', x: 1, y: 0.5, label: '$z$', drag: true }] } } },
    { name: 'complex-map (1/z, poles)', about: 'f(z) = 1/z: the grid lines through 0 run off to infinity without spikes; circles map to circles; a dragged z lands pinned to the edge when 1/z leaves the view', spec: { kind: 'complex-map',
      params: { f: '1/z', x: [-2, 2], y: [-2, 2], wx: [-2, 2], wy: [-2, 2], grid: 'both', rays: 8, unitCircle: true, wLabel: '$w = 1/z$' },
      state: { points: [{ id: 'p1', x: 0.5, y: 0.25, label: '$z$', drag: true }] } } },
    { name: 'complex-map (exp and log)', about: 'exp maps horizontal lines to rays and vertical lines to circles; the curve is the line Im z = 2 and its image', spec: { kind: 'complex-map',
      params: { f: 'exp(z)', x: [-2, 2], y: [-4, 4], wx: [-4, 4], wy: [-4, 4], gridStep: 1, curves: [{ id: 'line', z: 't + 2i', t: [-4, 4] }], wLabel: '$w = e^z$' },
      state: { points: [{ id: 'p1', x: 0, y: 1, label: '$z$', drag: true }] } } },
    { name: 'complex-map (log, branch cut)', about: 'Principal log: the polar grid maps to a rectangle and the cut along the negative real axis is not joined', spec: { kind: 'complex-map',
      params: { f: 'log(z)', x: [-3, 3], y: [-3, 3], wx: [-3, 3], wy: [-4, 4], grid: 'polar', rays: 16, wLabel: '$w = \\operatorname{Log} z$' } } },
    { name: 'vectors (matrix moves every vector)', about: 'state.matrix maps every vector as well as the grid and unit square (fixed: true opts one out); sliders bind m11..m22; derive reads det, trace and image.u', spec: { kind: 'vectors',
      params: { x: [-4, 4], y: [-4, 4] },
      state: { matrix: [[1, 0], [0, 1]], vectors: [{ id: 'u', v: [1, 1], label: '$T\\mathbf{u}$' }, { id: 'w', v: [-1, 0.5], label: '$T\\mathbf{w}$' }, { id: 'x', v: [0.5, 1.5], label: '$\\mathbf{x}$ (fixed)', fixed: true, dashed: true }], show: ['sum'], sumLabel: '$T(\\mathbf{u}+\\mathbf{w})$' },
      derive: { caption: 'det = {{fixed(det, 2)}}, trace = {{fixed(trace, 2)}}, image of u = ({{fixed(image.u[0], 2)}}, {{fixed(image.u[1], 2)}})' },
      controls: [{ bind: 'm11', min: -2, max: 2, step: 0.25, start: 1, label: 'a' }, { bind: 'm12', min: -2, max: 2, step: 0.25, start: 0, label: 'b' }, { bind: 'm21', min: -2, max: 2, step: 0.25, start: 0, label: 'c' }, { bind: 'm22', min: -2, max: 2, step: 0.25, start: 1, label: 'd' }] } },
    { name: 'vectors (derived matrix, dragged head)', about: 'derive writes state.matrix from a slider t (a rotation); the head of u drags in the image plane and the stored vector is its preimage', spec: { kind: 'vectors',
      params: { x: [-3, 3], y: [-3, 3], params: { t: 0.6 } },
      state: { matrix: [[1, 0], [0, 1]], vectors: [{ id: 'u', v: [1.5, 0.5], label: '$T\\mathbf{u}$' }], drag: ['u'] },
      derive: { matrix: '[[cos(t), -sin(t)], [sin(t), cos(t)]]', caption: 'angle = {{round(t * 180 / pi)}} degrees, T u = ({{fixed(image.u[0], 2)}}, {{fixed(image.u[1], 2)}}), |T u| = {{fixed(hypot(image.u[0], image.u[1]), 2)}}' },
      controls: [{ bind: 't', min: 0, max: 3.1416, step: 0.1, start: 0.6, label: 't' }] } },
```
Also decide on the existing `vectors (transform)` entry: its `u` and `w` now move with the transform; add `fixed: true` to both to keep it as it was.

### 5. `docs/AUTHORING.md`
In the canvas table (section 4), add after the `vectors` row:

| `complex-map` | `f` (a formula in `z`: `+ - * / ^`, `i`, `pi`, `e`, `exp`, `log`, `sqrt`, `sin`, `cos`, `tan`, `sinh`, `cosh`, `tanh`, `conj`, `abs`, `arg`, `re`, `im`, `pow(a, b)`), `params: { "a": 1 }` (numbers usable in `f`, bound by controls), `x`, `y` (z-plane ranges, default `[-2, 2]`), `wx`, `wy` (w-plane ranges, default as `x`, `y`), `grid: "cartesian"|"polar"|"both"|"none"`, `gridStep`, `rStep`, `rays`, `unitCircle`, `curves: [{ "id", "z": "formula in t", "t": [from, to] }]`, `points`, `zLabel`, `wLabel`, `stack` | `f`, `grid`, `gridStep`, `rStep`, `rays`, `unitCircle` (patchable), `params`, `points: [{ "id": "p1", "x": 1, "y": 0.5, "label": "$z$", "drag": true }]` (`x`, `y` are the real and imaginary parts of z; its image f(z) is drawn in the w-plane), `curves`, `hide: [ids]` | `grid-x`, `grid-y`, `grid-r`, `grid-th`, `unit`, curve ids, point ids and `<id>-image` |

And one paragraph in the same section, after the pass 7 summary:

> `vectors` and a matrix (item 435): `state.matrix: [[a, b], [c, d]]` (or `state.transform`) now acts on every vector, so one matrix moves all of them with the grid and the unit square; `fixed: true` on a vector keeps it still. A `derive` reads `matrix`, `m11` to `m22`, `det`, `trace` and `image.<id>` (the arrow as drawn), and may write `"matrix": "[[a, b], [c, d]]"` from sliders bound to params `a` to `d`. Dragging a head in the image plane stores the preimage. `complex-map` (item 432) draws a z-plane beside the image of a grid under f(z); a `derive` reads `p1.u` and `p1.v`, the real and imaginary parts of f at the point `p1`.

### 6. `app/js/engine/canvas/README-B.md`
Replace the integration-pass-5 bullet on `state.matrix` (in `## vectors`) with:

> - `state.matrix: [[a, b], [c, d]]` or `state.transform: { angle (degrees), shear, scale }` gives the basis (its columns): the grid, `b1`, `b2` and the image of the unit square (`unitsq`) follow. Item 435: the matrix also acts on every vector, each drawn as its image (a `from: [x, y]` tail is mapped too, a chain follows its vector), so `sum`, `project`, `span`, `lines`, `angles` and `segments` that name vectors work on the images; `fixed: true` on a vector keeps it where it is (an input shown beside its image). Points and bare-coordinate segment ends are not mapped. `state.basis` alone still draws the grid and leaves vectors alone. Controls bind `m11`, `m12`, `m21`, `m22`, `angle`, `shear`, `scale`, or a derive writes `"matrix": "[[a, b], [c, d]]"` from params `a` to `d`.
> - Dragging a mapped vector moves its head in the image plane and stores the preimage; a singular matrix (det 0) uses the pseudo-inverse, so the head slides along the image line. `points()` gives heads as drawn and `place(id, [x, y])` takes a drawn position.
> - Derive reads (names, from `state.params`, only while a matrix is set): `matrix`, `m11`, `m12`, `m21`, `m22`, `det`, `trace`, and `image.<id>` (each vector's arrow as drawn: the matrix applied unless `fixed`, then `scale`), for example `"caption": "det = {{fixed(det, 2)}}, T u = ({{fixed(image.u[0], 2)}}, {{fixed(image.u[1], 2)}})"`.

And add a new section after `## vectors`:

> ## complex-map
>
> A z-plane beside a w-plane showing what `w = f(z)` does to a grid, the unit circle, curves and points. Panels are side by side at 540 px and stack (one above the other) under 500 px wide; both use equal units, so angles stay true and `x`, `y`, `wx`, `wy` are minimum ranges.
>
> **params**
> - `f`: a formula in `z` (default `"z"`). Operators `+ - * /`, `^` or `**`, unary minus, implicit multiplication (`2z`, `a z`, `2(z + 1)`); constants `i`, `pi`, `e`; functions `exp`, `log` (alias `ln`, principal branch, arg in (-pi, pi]), `sqrt` (principal), `sin`, `cos`, `tan`, `sinh`, `cosh`, `tanh`, `conj`, `abs`, `arg`, `re`, `im` (the last three return a real number), `pow(a, b)`. Whole powers up to 64 use repeated multiplication. A pole or an undefined value is not drawn.
> - `params: { "a": 1 }`: numbers (or `[re, im]`) usable by name in `f` and in curve formulas; state.params overrides, so controls bind them (`{ "bind": "a" }`).
> - `x`, `y` (z-plane, default `[-2, 2]`), `wx`, `wy` (w-plane, default as `x`, `y`), `height` (panel height in px), `stack` (`true` or `false` forces the layout), `xLabel`, `yLabel` (default Re, Im), `zLabel`, `wLabel` (panel titles, KaTeX allowed; default "z-plane", "w-plane").
> - `grid`: `"cartesian"` (default), `"polar"`, `"both"` or `"none"`; `gridStep` (default a round number giving about eight lines), `rStep` (polar circles, default `gridStep`), `rays` (polar rays, default 12); `unitCircle: true` draws |z| = 1 and its image dashed.
> - `curves: [{ id, z: "formula in t", t: [from, to], colour, dashed, n }]`: any curve z(t) and its image, such as `"t + 2i"` (a line) or `"2 exp(i t)"` (a circle).
> - `points: [{ id, x, y, label, imageLabel, colour, drag }]` (also in state): `x`, `y` are the real and imaginary parts of z.
>
> **state**: `f`, `grid`, `gridStep`, `rStep`, `rays`, `unitCircle` (patchable; a frames control can switch `f`), `params` (numbers for `f`), `points` and `curves` (keyed patches by id), `hide: [ids]`, `highlight`, `caption`.
>
> **ids**: `grid-x` (lines Re z = const), `grid-y` (Im z = const), `grid-r` (circles), `grid-th` (rays), `unit`, curve ids, point ids (z) and `<id>-image` (f(z)). A group's id lights it in both panels.
>
> **modes**: `drag` (a point with `drag: true`, or those named by a `drag-point` widget; emits `{ type: "drag", id, x, y, phase }`) and `slider`. **methods**: `points()`, `place(id, [x, y])`, `evaluate(z)` (z an id or `[re, im]`, returns `[re, im]`), `setParam`, `getParam`.
>
> **derive**: each point carries `u` and `v`, the real and imaginary parts of f(z) (`p1.u`, `p1.v`), for captions such as `"f(z) = {{fixed(p1.u, 2)}} + {{fixed(p1.v, 2)}}i"`.
>
> Sampling: each curve starts with 180 to 240 samples, is subdivided where the image moves more than 9 px between samples, clipped to the panel, and broken at poles and at jumps such as the branch cut of `log`. A point whose image is outside the w-plane is drawn hollow at the edge.
>
> ```json
> { "kind": "complex-map",
>   "params": { "f": "z + a/z", "params": { "a": 1 }, "x": [-2, 2], "y": [-2, 2], "wx": [-3, 3], "wy": [-3, 3], "grid": "both", "unitCircle": true, "wLabel": "$w = z + a/z$" },
>   "state": { "points": [{ "id": "p1", "x": 0.8, "y": 0.6, "label": "$z$", "drag": true }] },
>   "derive": { "caption": "f(z) = {{fixed(p1.u, 2)}} + {{fixed(p1.v, 2)}}i" },
>   "controls": [{ "bind": "a", "min": 0.2, "max": 1.6, "step": 0.1, "start": 1, "label": "a" }] }
> ```

### 7. `docs/ENGINE-BACKLOG.md`
Items 435 (vectors matrix) and 432 (complex mapping half) can be marked done. Not done under 432: the 3D canvas half (another agent). Not added: tap mode on `complex-map`, a domain restriction on the grid (lines span the visible z-plane), curve labels, a conformal-grid option for non-equal units.

## Notes and limits
- `complex-map` ignores the `tap` mode (modes are `drag` and `slider`).
- `vectors.js` mapped-drag: `snap` rounds the head in the image plane, not the preimage.
- Mapped vectors keep their `colour` slot, label text and `labelPos`; the author writes the label (`$T\mathbf{u}$`), the engine does not rename.
- Names the validator cannot check: a `derive` that reads `image.u` or `p1.u` only parses; a typo there is a runtime warning, as for any derive name.

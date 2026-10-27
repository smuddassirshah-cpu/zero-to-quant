# Engine breadth pass 2: the `space` canvas (items 241 and the 3D half of 432)

Agent: engine, `space`. Owned file: `app/js/engine/canvas/space.js` (new, about 630 lines). No helper file, no other repo file touched. The canvas builds on `ZQ.cvb` (`plane.js`) for its lifecycle and reuses the `cvb-*` classes in `canvases.css`; it injects one small `<style id="cv-space-css">` of its own (quad shading, highlight, hit shapes), so no CSS file changes are needed.

## What was built

A rotatable 3D view in plain SVG (no WebGL, no libraries), canvas kind `space`.

- **Camera.** Orthographic, or weak perspective with `perspective` (0 to 1). Azimuth `az` and elevation `el` in degrees (z up, right-handed), `zoom` 0.4 to 3. Initial view from `params.camera` (default az -60, el 25), patchable as `state.camera` (tweens like any state). Pointer drag (mouse, pen, touch) rotates after a 5 px threshold, so a tap on a target still taps; two fingers pinch-zoom; arrow keys rotate 5 degrees (Shift 15), `+` and `-` zoom, `0` or Home resets. A "Reset view" chip returns to the first-drawn camera (animated, disabled when already home). Redraws are coalesced to one per animation frame. The svg is focusable (`role="group"`, `aria-roledescription="3D view"`) with an `aria-label` that lists the objects and the keys, and a polite live region reads the new angles after a key press. A keyboard-only focus ring (not shown after a mouse press). `params.touchScroll: true` lets a vertical touch scroll the page (touch then turns the azimuth only).
- **Frame.** Axes through the origin (or along the low edges when 0 is out of range) with arrowheads, KaTeX axis names (`axisLabels`), tick numbers that sit beside their axis and are depth-sorted with the drawing (a surface hides them), the box edges, and a grid on the faces turned away from the camera (`grid: "back"` default, `"floor"`, `false`).
- **Objects** (each a list with ids, keyed-patchable by id like every list): `points` (literal, `on` a surface, or `at` a curve parameter; `open`, `drop` line to the floor, compass `labelPos`), `vectors` (from the origin, a triple, a point id, or chained from another vector; `dashed`, `head: false`, `drop`, `labelPos` end or mid), `curves` (parametric r(t) with a `t` range whose ends may be formulas, so a slider can grow the curve; `dashed`), `lines` (polylines through given points, `closed`), `surfaces` (z = f(x, y) over a range, or a parametric (x, y, z)(u, v); `shade` light, flat or height; `wire` true or `"only"` for a hidden-line wireframe; `opacity`; `clip` clamp, drop or none), `planes` (a plane by `normal` with `through` or `d`, a span of two vectors, or the line spanned by one; clipped to the box and cut into cells; `extent` gives a finite parallelogram patch; `opacity`), `fields` (F(x, y, z) as arrows on an n by n by n grid, capped at 343, `normalise`, `scale`, `at` for a one-deep slice).
- **Formulas** use the curve-formula language of `plane` (`ZQ.canvas.compile`): `^`, `-x^2`, `pi`, `e`, `sin`, `sum(k, ...)` and the rest. Variables are `t` (curves), `x` and `y` (explicit surfaces), `u` and `v` (parametric surfaces), `x`, `y`, `z` (fields), and every name in `params.params` / `state.params` everywhere (point and vector coordinates, plane normals, `t` ranges). A bound slider (`bind: "a"`) writes `state.params.a` and the picture redraws live. `bind: "az"`, `"el"` and `"zoom"` turn the camera.
- **Depth order.** Painter's algorithm per frame. Surfaces and planes are cut into small cells (a plane is clipped to the box cell by cell with Sutherland-Hodgman), vectors into up to nine pieces, curves into their samples. A cell sorts by its farthest corner, so a vector, curve or point lying in a flat cell always draws after it; lines and dots get a small lift (a tenth of a cell) for curved surfaces. Correct for ordinary intersections (a vector through a surface or plane, a curve over a surface, a plane cutting a bowl, a sphere in a bowl). Not exact for mutually interpenetrating large pieces (see follow-ups).
- **Shading.** Lambert with a fixed world-space light (so the lighting stays put as you rotate), two-sided, vertex normals averaged per cell, 16 levels, drawn with `color-mix` against the canvas background so it works in both themes. Opaque by default, so adjacent cells leave no seams.
- **Shared contract.** `state.show` (reveals items with `hidden: true`; feature words `axes`, `ticks`, `box`, `grid` hide with `hide`), `state.hide`, `state.highlight` and `highlight(ids)` (a pear glow and thicker lines on every piece of the object), `mark` (is-correct, is-notyet, is-reveal, is-dim recolour whole objects; no badge, `badges: false`), `flash`, `lock`, `caption`, `clone` (a still copy). Tap mode (`enable('tap')`, so `tap-regions` works): one transparent hit shape per object (dots on top, then arrows and curves, then surfaces and planes by their outline), ids are the item ids. A canvas given `ctx.mode === 'static'` (what the player's Why? sheet passes) is made fully static here (see the note under "Things the integration agent should know").
- **derive.** Items read by id as on every canvas (`u.v`, `P.p`, `s.z`), `camera.az` / `camera.el` / `camera.zoom`, `params`, and writes work (`"u.v.2": "a * 2"`, a whole `"u.v": "[a, b, c]"`). New: `values.P` is a point's resolved `[x, y, z]` (including one riding a curve or surface) and `values.u` a vector's tip, so `{{round(values.P[2], 2)}}` reads the height of a point on `z = f(x, y)`.
- **Performance.** Per frame: project, sort, one markup string, one `innerHTML`. Measured in headless Chromium here: about 8 to 10 ms for a typical scene (30 by 30 surface, a plane, a curve, vectors; about 1,700 nodes), about 22 to 27 ms for the worst case. The total of surface and plane cells is held near 1,600 (surfaces take `n` up to 40 a side, planes `res` up to 24; above the budget every `n` is scaled down together), curves take at most 600 samples, fields at most 343 arrows (one path each).

## How it was checked

Scratch copy of the app at `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/space/` (file, script tag and gallery entries added there only; the repo is untouched apart from `space.js`).

- **Screenshots** (Playwright, Chromium), each gallery example in light and dark, desktop (900 px) and phone (390 px, touch), before and after a scripted drag (mouse; CDP touch on the phone): `scratchpad/shots/` (48 files, names `<n>-space-<example>-<theme>-<desktop|mobile>-<before|after>.png`). Depth order was checked by eye on purpose-built scenes (a vector piercing a wavy surface, a curve and a point on it, an axis through it, a plane cutting a bowl, a sphere inside a bowl): `scratchpad/pierce3.png`, `scratchpad/mesh1.png`, `scratchpad/all1.png` (every option at once, perspective on), `scratchpad/hl-light.png` and `hl-dark.png` (highlight plus graded marks).
- **Behaviour script** (`scratchpad/tools/interact.js`): keyboard rotate and zoom and reset, live-region text, the Reset chip enabled and disabled, mouse drag, `rotate` events, `show` / `hide`, highlight, marks (no badges), keyed patch, `setParam` for params and for `az`, tap mode (roles, selection, a dot on a surface wins over the surface), clone is static (no tabindex, no chip), `lock` stops rotation, a camera patch tweens, `project()`; `derive` with `values.P` and a write into `w.v.2`; pinch zoom through CDP; sliders in the gallery redraw the curve and turn the camera. No console errors.
- **Lesson flow** (scratch lesson `scratchpad/space/content/courses/algo-think/lz-space.json`, three screens: a numeric on a space canvas with an `az` control, a `tap-regions` on the normal vector with an `explain.canvas` camera patch, a `slider` widget bound to a param with a derived caption): `node tools/playthrough.mjs --lesson algo-think/lz-space --why --shots ...` passes in the scratch copy; the Why? sheet shows the explained camera and highlight, and the still copy has no reset chip. Screenshots in `scratchpad/pt/`.
- **Validator** (patch below, applied to the scratch `validate.mjs`): the valid specs pass; a deliberately bad canvas (`scratchpad/space/content/courses/algo-think/lz-bad.json`) gives 46 errors, listed in the table at the end.
- **Repo**: `cd app && node tools/validate.mjs` stays at 0 errors (365 warnings, none new). The repo `index.html` does not load `space.js` yet, so no repo lesson, route or `--all` run can be affected by this file; the integration agent should run `--all` after wiring it.

## Things the integration agent should know

1. **`ZQ.cvb.make` ignores `ctx.mode === 'static'`.** It reads only `ctx.static`, but the player's Why? sheet creates its canvas with `{ mode: 'static' }` (`engine/player.js` line 324). So every `cvb` canvas shown in a Why? sheet is currently live, not a still copy (I saw a live Reset chip there before handling it in `space.js`). `space.js` maps `mode: 'static'` to `static: true` itself. One-line fix for everyone, in `plane.js` `make`: `const isStatic = !!(ctx.static || ctx.mode === 'static');`. I did not touch `plane.js`.
2. **Touch.** `.cvb .cvb-svg { touch-action: none }` (existing) means a finger on the picture rotates it and does not scroll the page. A tall `space` canvas filling a phone screen can trap a scroll. Authors can set `touchScroll: true` (vertical touch scrolls, horizontal turns the azimuth), or leave a margin; this is documented below.
3. **CSS.** Everything specific to `space` is in the `<style id="cv-space-css">` the file injects (selectors scoped to `.cv-space`). It may be moved into `canvases.css` inside `@layer cv-kinds` if the team prefers; nothing else depends on where it lives.

## Shared-file changes

### 1. `app/index.html`

Add after the `orderbook.js` script tag (any position after `plane.js` works; the factory reads `ZQ.cvb` lazily):

```html
<script src="js/engine/canvas/space.js"></script>
```

### 2. `app/tools/validate.mjs`

Four edits. The patch was applied to a scratch copy and tested (see the table at the end).

a. Canvas-kind list (line 33): add `'space'` at the end of `CANVASES`:

```js
const CANVASES = new Set(['pair', 'grid', ..., 'orderbook', 'table', 'console', 'space']);
```

b. Add the function below, in full, immediately above `const checkCanvas = (file, where, c) => {`:

```js
/* space canvas (docs/AUTHORING.md section 4, README-B "space"): shapes and formula names only, never a crash */
const SPACE_LISTS = ['points', 'vectors', 'curves', 'lines', 'surfaces', 'planes', 'fields'];
const SPACE_FNS = new Set(['sin', 'cos', 'tan', 'exp', 'ln', 'log', 'log10', 'sqrt', 'abs', 'max', 'min', 'floor', 'ceil', 'pow', 'pi', 'e', 'atan', 'asin', 'acos', 'sinh', 'cosh', 'tanh', 'sign', 'round', 'fact', 'lgamma', 'erf', 'erfc', 'Phi', 'PhiInv', 'Phiinv', 'NormInv', 'normcdf', 'normpdf', 'pnorm', 'dnorm', 'qnorm']);
const checkSpace = (file, where, P, S) => {
  const E = (at, msg) => err(file, `${where}${at}`, msg);
  const num = (v) => typeof v === 'number' && Number.isFinite(v);
  const names = new Set(Object.keys({ ...(isObj(P.params) ? P.params : {}), ...(isObj(S.params) ? S.params : {}) }));
  /* a coordinate or formula: a number, or a string using only its variables, the params and the curve-formula functions */
  const formula = (v, at, vars = []) => {
    if (num(v)) return true;
    if (typeof v !== 'string' || !v.trim()) { E(at, 'a coordinate is a number or a formula string'); return false; }
    if (/\b(sum|prod)\s*\(/.test(v)) return true; // sum(k, a, b, term) binds its own name
    const bad = [...v.replace(/\d+\.?\d*(e[+-]?\d+)?/gi, ' ').matchAll(/[A-Za-z_]\w*/g)].map(m => m[0]).find(w => !SPACE_FNS.has(w) && !vars.includes(w) && !names.has(w));
    if (bad) { E(at, `unknown name "${bad}" in "${v}": a formula here may use ${vars.length ? vars.join(', ') + ', ' : ''}the params${[...names].length ? ' (' + [...names].join(', ') + ')' : ''} and the usual functions`); return false; }
    let d = 0; for (const ch of v) { if (ch === '(') d++; else if (ch === ')' && --d < 0) break; }
    if (d !== 0) { E(at, `unbalanced brackets in "${v}"`); return false; }
    return true;
  };
  const triple = (v, at, vars) => { if (!(Array.isArray(v) && v.length === 3)) { E(at, 'a point or vector is three coordinates [x, y, z] (numbers or formulas)'); return; } v.forEach((q, i) => formula(q, `${at}[${i}]`, vars)); };
  const pair = (v, at, what) => { if (!(Array.isArray(v) && v.length === 2)) { E(at, `${what} is [from, to]`); return; } v.forEach((q, i) => formula(q, `${at}[${i}]`)); };
  const slotOk = (v) => v == null || (Number.isInteger(v) && v >= 1 && v <= 6);
  ['x', 'y', 'z'].forEach(k => { if (P[k] != null && !(Array.isArray(P[k]) && P[k].length === 2 && P[k].every(num) && P[k][1] > P[k][0])) E(`.params.${k}`, `${k} is [min, max] with min below max`); });
  if (P.aspect != null && !(Array.isArray(P.aspect) && P.aspect.length === 3 && P.aspect.every(v => num(v) && v > 0))) E('.params.aspect', 'aspect is three positive numbers [x, y, z]');
  if (P.height != null && !(num(P.height) && P.height >= 240 && P.height <= 640)) E('.params.height', 'height is 240 to 640');
  [['params', P], ['state', S]].forEach(([w, o]) => { if (o.perspective != null && !(num(o.perspective) && o.perspective >= 0 && o.perspective <= 1)) E(`.${w}.perspective`, 'perspective is 0 (flat, the default) to 1'); });
  [['params', P], ['state', S]].forEach(([w, o]) => { if (o.grid != null && !['back', 'floor', false].includes(o.grid)) E(`.${w}.grid`, 'grid is "back", "floor" or false'); ['box', 'axes', 'ticks'].forEach(k => { if (o[k] != null && typeof o[k] !== 'boolean') E(`.${w}.${k}`, `${k} is true or false`); }); });
  if (P.axisLabels != null && !(Array.isArray(P.axisLabels) && P.axisLabels.length === 3 && P.axisLabels.every(v => typeof v === 'string'))) E('.params.axisLabels', 'axisLabels is three strings, such as ["$x_1$", "$x_2$", "$x_3$"]');
  [['params', P.camera], ['state', S.camera]].forEach(([w, cam]) => {
    if (cam == null) return;
    if (!isObj(cam)) { E(`.${w}.camera`, 'camera is { az, el, zoom } (degrees, degrees, 0.4 to 3)'); return; }
    if (cam.az != null && !num(cam.az)) E(`.${w}.camera.az`, 'az (azimuth) is a number of degrees');
    if (cam.el != null && !(num(cam.el) && cam.el >= -89 && cam.el <= 89)) E(`.${w}.camera.el`, 'el (elevation) is -89 to 89 degrees');
    if (cam.zoom != null && !(num(cam.zoom) && cam.zoom >= 0.4 && cam.zoom <= 3)) E(`.${w}.camera.zoom`, 'zoom is 0.4 to 3');
  });
  /* every list entry, from params (whole entries) and state (whole lists, or keyed patches by id) */
  const all = {}, seen = new Map();
  const entries = (k, src, at) => (Array.isArray(src[k]) ? src[k].map((q, i) => [q, `${at}.${k}[${i}]`, true]) : isObj(src[k]) ? Object.entries(src[k]).map(([id, q]) => [isObj(q) ? { id, ...q } : q, `${at}.${k}.${id}`, false]) : []);
  SPACE_LISTS.forEach(k => { all[k] = new Set(); [[P, '.params'], [S, '.state']].forEach(([src, at]) => entries(k, src, at).forEach(([q]) => { if (isObj(q) && q.id != null) all[k].add(String(q.id)); })); });
  SPACE_LISTS.forEach(k => [[P, '.params'], [S, '.state']].forEach(([src, at]) => {
    if (src[k] != null && !Array.isArray(src[k]) && !isObj(src[k])) E(`${at}.${k}`, `${k} is a list of objects with ids`);
    entries(k, src, at).forEach(([q, w, full]) => {
      if (q === null && !full) return; // a keyed patch removing an item
      if (!isObj(q)) { E(w, 'each entry is an object'); return; }
      if (full && (typeof q.id !== 'string' || !q.id)) E(`${w}.id`, 'every entry needs an id (a string), so hints, taps and patches can name it');
      else if (full && at === '.params') { if (seen.has(q.id)) E(`${w}.id`, `duplicate id "${q.id}" (also in ${seen.get(q.id)})`); else seen.set(q.id, `${k}`); }
      if (!slotOk(q.colour)) E(`${w}.colour`, 'colour is a slot 1 to 6');
      if (q.hidden != null && typeof q.hidden !== 'boolean') E(`${w}.hidden`, 'hidden is true or false (state.show: ["id"] reveals it)');
      const need = (cond, msg) => { if (full && !cond) E(w, msg); };
      if (k === 'points') {
        need(q.p != null || (q.x != null && q.y != null) || q.at != null, 'a point needs p: [x, y, z] (or x, y and z, or at and t on a curve)');
        if (q.p != null) triple(q.p, `${w}.p`); else ['x', 'y', 'z'].forEach(a => { if (q[a] != null) formula(q[a], `${w}.${a}`); });
        if (q.on != null && !all.surfaces.has(String(q.on))) E(`${w}.on`, `on names a surface id (one of ${[...all.surfaces].join(', ') || 'none defined'}); the point's z is read from it`);
        if (q.at != null && !all.curves.has(String(q.at))) E(`${w}.at`, `at names a curve id (one of ${[...all.curves].join(', ') || 'none defined'}); t is the parameter value`);
        if (q.at != null && q.t != null) formula(q.t, `${w}.t`);
        if (q.at != null && q.t == null) E(`${w}.t`, 'a point on a curve needs t');
        if (q.labelPos != null && !['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'].includes(q.labelPos)) E(`${w}.labelPos`, 'labelPos is a compass point: n, ne, e, se, s, sw, w or nw');
      } else if (k === 'vectors') {
        need(q.v != null, 'a vector needs v: [dx, dy, dz]');
        if (q.v != null) triple(q.v, `${w}.v`);
        if (q.from != null) { if (Array.isArray(q.from)) triple(q.from, `${w}.from`); else if (!all.points.has(String(q.from)) && !all.vectors.has(String(q.from))) E(`${w}.from`, 'from is [x, y, z] or the id of a point or another vector (a chain starts at its tip)'); }
        if (q.labelPos != null && !['end', 'mid'].includes(q.labelPos)) E(`${w}.labelPos`, 'labelPos is "end" or "mid"');
      } else if (k === 'curves') {
        need(typeof q.x === 'string' && typeof q.y === 'string', 'a curve needs x and y formulas in t (z too, for a space curve), and t: [from, to]');
        ['x', 'y', 'z'].forEach(a => { if (q[a] != null) formula(q[a], `${w}.${a}`, ['t']); });
        if (q.t != null) pair(q.t, `${w}.t`, 't'); else need(false, 'a curve needs t: [from, to]');
        if (q.n != null && !(Number.isInteger(q.n) && q.n >= 8 && q.n <= 600)) E(`${w}.n`, 'n is 8 to 600 samples');
      } else if (k === 'lines') {
        need(Array.isArray(q.pts) && q.pts.length >= 2, 'a line needs pts: at least two [x, y, z] points');
        if (Array.isArray(q.pts)) q.pts.forEach((p, i) => triple(p, `${w}.pts[${i}]`));
      } else if (k === 'surfaces') {
        const param = typeof q.x === 'string';
        if (param) { ['x', 'y', 'z'].forEach(a => { if (typeof q[a] !== 'string') E(`${w}.${a}`, 'a parametric surface has x, y and z formulas in u and v'); else formula(q[a], `${w}.${a}`, ['u', 'v']); }); if (q.u != null) pair(q.u, `${w}.u`, 'u'); if (q.v != null) pair(q.v, `${w}.v`, 'v'); need(q.u != null && q.v != null, 'a parametric surface needs u: [from, to] and v: [from, to]'); }
        else { need(typeof q.z === 'string', 'a surface needs z (a formula in x and y), or x, y and z formulas in u and v'); if (q.z != null) formula(q.z, `${w}.z`, ['x', 'y']); ['x', 'y'].forEach(a => { if (q[a] != null && !(Array.isArray(q[a]) && q[a].length === 2 && q[a].every(num) && q[a][1] > q[a][0])) E(`${w}.${a}`, `${a} is the range [min, max] the surface covers`); }); }
        if (q.n != null && !((Number.isInteger(q.n) && q.n >= 2 && q.n <= 40) || (Array.isArray(q.n) && q.n.length === 2 && q.n.every(v => Number.isInteger(v) && v >= 2 && v <= 40)))) E(`${w}.n`, 'n is 2 to 40 cells each way (or [nu, nv])');
        if (q.shade != null && !['light', 'flat', 'height'].includes(q.shade)) E(`${w}.shade`, 'shade is "light" (default), "flat" or "height"');
        if (q.wire != null && q.wire !== true && q.wire !== 'only' && q.wire !== false) E(`${w}.wire`, 'wire is true (edges over the shading) or "only" (hidden-line wireframe)');
        if (q.opacity != null && !(num(q.opacity) && q.opacity >= 0.05 && q.opacity <= 1)) E(`${w}.opacity`, 'opacity is 0.05 to 1');
        if (q.clip != null && !['clamp', 'drop', 'none'].includes(q.clip)) E(`${w}.clip`, 'clip is "clamp", "drop" or "none"');
        if (q.colour2 != null && !slotOk(q.colour2)) E(`${w}.colour2`, 'colour2 is a slot 1 to 6');
        if (q.labelAt != null && !(Array.isArray(q.labelAt) && q.labelAt.length === 2 && q.labelAt.every(num))) E(`${w}.labelAt`, 'labelAt is [x, y]');
      } else if (k === 'planes') {
        const sp = Array.isArray(q.span) ? q.span : null;
        need(sp || Array.isArray(q.normal), 'a plane needs span (one or two vectors: ids or [x, y, z]) or normal: [a, b, c] with through or d');
        if (sp && !(sp.length >= 1 && sp.length <= 2)) E(`${w}.span`, 'span is one vector (a line) or two (a plane)');
        (sp || []).forEach((e, i) => { if (Array.isArray(e)) triple(e, `${w}.span[${i}]`); else if (!all.vectors.has(String(e))) E(`${w}.span[${i}]`, `"${e}" is not a vector id on this canvas`); });
        if (q.normal != null) triple(q.normal, `${w}.normal`);
        if (q.through != null) triple(q.through, `${w}.through`);
        if (q.d != null) formula(q.d, `${w}.d`);
        if (q.extent != null && !(Array.isArray(q.extent) && [2, 4].includes(q.extent.length) && q.extent.every(num))) E(`${w}.extent`, 'extent is [lo, hi] (both coefficients) or [a0, a1, b0, b1], for a finite patch of a span');
        if (q.res != null && !(Number.isInteger(q.res) && q.res >= 3 && q.res <= 24)) E(`${w}.res`, 'res is 3 to 24 cells each way');
        if (q.opacity != null && !(num(q.opacity) && q.opacity >= 0.03 && q.opacity <= 1)) E(`${w}.opacity`, 'opacity is 0.03 to 1');
      } else if (k === 'fields') {
        need(Array.isArray(q.F) && q.F.length === 3, 'a field needs F: three formulas in x, y and z (the arrow at each grid point)');
        if (Array.isArray(q.F)) q.F.forEach((f, i) => formula(f, `${w}.F[${i}]`, ['x', 'y', 'z']));
        if (q.n != null && !((Number.isInteger(q.n) && q.n >= 1 && q.n <= 7) || (Array.isArray(q.n) && q.n.length === 3 && q.n.every(v => Number.isInteger(v) && v >= 1 && v <= 9)))) E(`${w}.n`, 'n is 1 to 7 arrows each way (or [nx, ny, nz], 1 to 9; the grid is capped at 343 arrows)');
        if (q.at != null && !(Array.isArray(q.at) && q.at.length === 3 && q.at.every(num))) E(`${w}.at`, 'at is [x, y, z]: where a one-arrow-deep grid sits');
        if (q.scale != null && !(num(q.scale) && q.scale > 0)) E(`${w}.scale`, 'scale is a positive number');
      }
    });
  }));
  [S.show, S.hide].forEach((l, i) => { if (l != null && !Array.isArray(l)) E(`.state.${i ? 'hide' : 'show'}`, `${i ? 'hide' : 'show'} is a list of ids`); });
};
```

c. In `checkCanvas`, right after the line `const slotOk = (v) => v == null || (Number.isInteger(+v) && +v >= 1 && +v <= 6);` add:

```js
  if (c.kind === 'space') checkSpace(file, where, P, S);
```

d. In `regionIds` (tap-regions answers, hints' highlight ids), add this branch just before the `if (canvas.kind === 'console' && (Array.isArray(p.lines) ...` branch:

```js
  if (canvas.kind === 'space') { // every object id, from params, state and enter (tap mode: points, vectors, curves, lines, surfaces, planes, fields)
    const st = canvas.state || {}, en = canvas.enter || {}, ids = new Set();
    ['points', 'vectors', 'curves', 'lines', 'surfaces', 'planes', 'fields'].forEach(k => [p[k], st[k], en[k]].forEach(L => { if (Array.isArray(L)) L.forEach(q => { if (isObj(q) && q.id != null) ids.add(String(q.id)); }); else if (isObj(L)) Object.keys(L).forEach(id => ids.add(id)); }));
    return ids.size ? ids : null;
  }
```

`PLAUSIBLE` needs no entry (the default id pattern fits; `plausibleId` finds ids through `regionIds`). The `explore` screen rule "needs an interactive canvas" already accepts `canvas.controls`, which is how a `space` explore screen qualifies.

Rules the patch enforces (one error per problem, shapes and names only, never a crash):

- `x`, `y`, `z`: `[min, max]`, min below max. `aspect`: three positive numbers. `height`: 240 to 640. `perspective`: 0 to 1. `grid`: `"back"`, `"floor"` or `false`. `box`, `axes`, `ticks`: booleans. `axisLabels`: three strings. `camera` (params and state): `az` a number, `el` -89 to 89, `zoom` 0.4 to 3.
- Every list entry (`points`, `vectors`, `curves`, `lines`, `surfaces`, `planes`, `fields`) is an object with a string `id` (unique in params), `colour` 1 to 6, `hidden` boolean. State lists may be whole arrays or keyed patches by id (a patch is checked for the fields it gives only; `null` removes).
- Formulas (any coordinate that is a string, curve and surface and field formulas, `t` ranges, `d`) may use only their own variables (`t`; `x`, `y`; `u`, `v`; `x`, `y`, `z`), the names in `params.params` and `state.params`, and the curve-formula functions, with balanced brackets. A typo such as `sin(q)` is an error naming `q`.
- `points`: `p` (a triple) or `x`/`y`/`z`, or `at` a curve id with `t`; `on` must name a surface id; `labelPos` a compass point.
- `vectors`: `v` a triple; `from` a triple or the id of a point or vector; `labelPos` `end` or `mid`.
- `curves`: `x` and `y` strings (`z` optional) and `t: [from, to]`; `n` 8 to 600. `lines`: `pts` of at least two triples.
- `surfaces`: either `z` (with optional `x` and `y` ranges) or string `x`, `y`, `z` with `u` and `v` ranges; `n` 2 to 40 (or `[nu, nv]`); `shade` light, flat or height; `wire` true or `"only"`; `opacity` 0.05 to 1; `clip` clamp, drop or none; `colour2`; `labelAt` `[x, y]`.
- `planes`: `span` (one or two vector ids or triples) or `normal` (a triple, with `through` or `d`); `extent` of 2 or 4 numbers; `res` 3 to 24; `opacity` 0.03 to 1.
- `fields`: `F` three formulas; `n` 1 to 7 (or three values 1 to 9); `at` three numbers; `scale` positive.
- `state.show` and `state.hide` are lists.

### 3. `app/tools/playthrough.mjs`

No change needed. The canvas has no kind-specific hooks in the player or the test harness; `tap-regions`, `slider` (bind to a param), `explain.canvas` and `derive` all ran through `--lesson` in the scratch copy. (If a later content level wants the `drag-point` widget on a 3D point, `space` has no drag mode yet; see follow-up 1.)

### 4. `docs/AUTHORING.md`

a. Section 4, first paragraph: add `space` to the list of kinds documented in `README-B.md` ("... orderbook, space").

b. Section 4 table: add this row after `vectors`:

```markdown
| `space` | `x`, `y`, `z` ranges (default -5 to 5), `equal` (equal units), `aspect: [a, b, c]`, `height` (240 to 640, default 420), `camera: { az, el, zoom }` (opening view, default az -60, el 25), `perspective` (0 to 1), `grid: "back"\|"floor"\|false`, `box`, `axes`, `ticks`, `axisLabels`, `params: { "a": 1 }` (usable in formulas), and the lists `points: [{ "id": "P", "p": [1, 2, 3], "label": "P", "drop": true }]` (or `at` a curve with `t`, or `on` a surface), `vectors: [{ "id": "u", "v": [1, 2, 3], "from": [0, 0, 0] \| pointId \| vectorId, "label": "$\\mathbf{u}$" }]`, `curves: [{ "id": "r", "x": "cos(t)", "y": "sin(t)", "z": "t / 4", "t": [0, 12.57] }]`, `lines` (polylines through `pts`), `surfaces: [{ "id": "s", "z": "x^2 - y^2", "x": [-2, 2], "y": [-2, 2], "n": 24 }]` (or parametric `x`, `y`, `z` in `u`, `v`), `planes: [{ "id": "cs", "span": ["u", "v"] }]` (or `normal` with `through` or `d`; a one-vector span is a line), `fields: [{ "id": "F", "F": ["-y", "x", "0"], "n": 5 }]` | `camera`, `show`, `hide` (ids; `axes`, `ticks`, `box`, `grid` too), `highlight`, `params`, and every list patched by id | item ids; tap mode on every object |
```

c. Add after the table's trailing paragraphs (for instance after the "Pass 7 canvas options in brief" paragraph) this paragraph:

```markdown
`space` (pass 8) is the 3D canvas: drag to rotate, arrow keys turn the view, a Reset view button returns it. Formulas are written as in `plane` (`x^2 - y^2`, `cos(t)`), with the variable named for the object (`t` for a curve, `x` and `y` for `z = f(x, y)`, `u` and `v` for a parametric surface, `x`, `y`, `z` for a field) and any name from `params.params` usable everywhere, so a slider (`bind: "a"`) redraws the picture live. Coordinates in `points`, `vectors` and `planes` may be formulas too (`"v": ["a", "b", "a + b"]`). `bind: "az"`, `"el"` and `"zoom"` turn the camera. `derive` reads items by id as usual (`u.v`), `camera.az`, and `values.P` for a point's resolved `[x, y, z]` (a point `on` a surface or `at` a curve included) and `values.u` for a vector's tip. Keep the picture light: the cells of all surfaces and planes together are held near 1,600 so dragging stays smooth on a phone. Give `equal: true` when the maths needs equal units (perpendicular vectors must look perpendicular), and leave a margin round the canvas on a phone, because a finger on the picture rotates it instead of scrolling.
```

d. Section 7 (validation rules): if the guide lists canvas kinds, add `space`.

### 5. `app/js/engine/canvas/README-B.md`

Change the title line to add `space` ("... payoff, orderbook, space") and append this section after `## orderbook` (before `## Widget: slider`):

```markdown
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

```json
{ "kind": "space",
  "params": { "x": [-2, 2], "y": [-2, 2], "z": [-4, 4], "params": { "a": 1 },
    "surfaces": [{ "id": "s", "z": "a*(x^2 - y^2)/2", "colour": 1 }],
    "points": [{ "id": "P", "p": [1, 0.5, 0], "on": "s", "drop": true, "label": "P" }] },
  "controls": [{ "bind": "a", "min": -2, "max": 2, "step": 0.1, "label": "$a$" }],
  "derive": { "caption": "At P the height is {{round(values.P[2], 2)}}." } }
```
```

### 6. `docs/ENGINE-BACKLOG.md`

Status lines for the integration agent: item 241 (a simple 3D projected view for column spaces and nullspaces) is done by `space` (planes and spans as translucent patches, vectors from the origin or a base, rotation by drag and keys); item 432 (the 3D half: rotatable 3D canvas with drag, depth order, vectors, curves, surfaces, field arrows) is done; its other half (a z-plane grid beside its image under f, for the complex course) is not started. Follow-ups 1 to 8 below are new.

### 7. `app/js/screens/system.js` (gallery)

`CANVAS_ABOUT` entry (the gallery warns about a kind with no sample and no blurb):

```js
space: 'Rotatable 3D view: vectors, curves, surfaces, planes and fields',
```

`CANVAS_SAMPLES.space` (one per kind; plain `Z.canvas.create`):

```js
"space": {"params":{"x":[-4,4],"y":[-4,4],"z":[-4,4],"equal":true,"camera":{"az":-55,"el":24},"vectors":[{"id":"u","v":[3,0,1],"label":"$\\mathbf{u}$"},{"id":"v","v":[0,3,2],"label":"$\\mathbf{v}$"},{"id":"n","v":[-1,-2,3],"label":"$\\mathbf{n}$","colour":4}],"planes":[{"id":"cs","span":["u","v"],"label":"column space"}],"points":[{"id":"b","p":[-2,3,3],"label":"$\\mathbf{b}$","drop":true}]},"state":{}},
```

`CANVAS_EXTRAS` entries (these render through `ZQ.player.renderItem`, so the sliders work; paste the four objects into the array):

```js
{"name":"space (vectors and a span)","about":"Two vectors, the plane they span (column space) and its normal; drag to rotate, arrow keys turn the view, Reset view returns it","spec":{"kind":"space","params":{"x":[-4,4],"y":[-4,4],"z":[-4,4],"equal":true,"camera":{"az":-55,"el":24},"vectors":[{"id":"u","v":[3,0,1],"label":"$\\mathbf{u}$"},{"id":"v","v":[0,3,2],"label":"$\\mathbf{v}$"},{"id":"n","v":[-1,-2,3],"label":"$\\mathbf{n}$","colour":4}],"planes":[{"id":"cs","span":["u","v"],"label":"column space"}],"points":[{"id":"b","p":[-2,3,3],"label":"$\\mathbf{b}$","drop":true}]},"state":{"caption":"The normal $\\mathbf{n}$ is perpendicular to both $\\mathbf{u}$ and $\\mathbf{v}$."}}},
  {"name":"space (helix and tangent)","about":"A parametric curve r(t) with a slider on the pitch b and one on the point t0; the tangent vector is built from the same parameters","spec":{"kind":"space","params":{"x":[-3,3],"y":[-3,3],"z":[-4,4],"equal":true,"camera":{"az":-50,"el":22},"params":{"b":0.3,"t0":4},"curves":[{"id":"h","x":"2*cos(t)","y":"2*sin(t)","z":"b*(t - 6.2832)","t":[0,12.5664],"label":"$\\mathbf{r}(t)$","colour":1}],"points":[{"id":"P","at":"h","t":"t0","label":"P","drop":true}],"vectors":[{"id":"T","from":"P","v":["-2*sin(t0)","2*cos(t0)","b"],"label":"$\\mathbf{r}'$","colour":2}]},"controls":[{"bind":"b","min":0.1,"max":0.6,"step":0.05,"label":"Pitch $b$","start":0.3},{"bind":"t0","min":0,"max":12.5,"step":0.25,"label":"Point $t_0$","start":4}]}},
  {"name":"space (surface z = f(x, y))","about":"A shaded saddle with a slider on a, a point riding it (on: \"s\"), height shown by a drop line","spec":{"kind":"space","params":{"x":[-2,2],"y":[-2,2],"z":[-4,4],"camera":{"az":-62,"el":28},"params":{"a":1},"surfaces":[{"id":"s","z":"a*(x^2 - y^2)/2","n":26,"colour":1,"label":"$z = \\tfrac{a}{2}(x^2 - y^2)$"}],"points":[{"id":"P","p":[1,0.5,0],"on":"s","label":"P","drop":true,"colour":2}]},"controls":[{"bind":"a","min":-2,"max":2,"step":0.1,"label":"$a$","start":1}]}},
  {"name":"space (mesh, height and a sphere)","about":"Hidden-line wireframe (wire: \"only\"), height colouring with a mesh, and a parametric sphere cut open by a plane","spec":{"kind":"space","params":{"x":[-3,3],"y":[-3,3],"z":[-3,3],"equal":true,"camera":{"az":-40,"el":30},"perspective":0.35,"surfaces":[{"id":"bowl","z":"x^2/3 + y^2/3 - 2","n":22,"x":[-3,3],"y":[-3,3],"shade":"height","wire":true,"colour":1,"colour2":4,"opacity":1},{"id":"ball","x":"1.5*sin(u)*cos(v)","y":"1.5*sin(u)*sin(v)","z":"1.5*cos(u) + 0.5","u":[0,3.1416],"v":[0,6.2832],"n":20,"wire":"only","colour":2}],"planes":[{"id":"cut","normal":[0,0,1],"d":1.2,"colour":3,"opacity":0.2,"label":"$z = 1.2$"}]}}},
  {"name":"space (vector field)","about":"Arrows of F = (-y, x, 0.3) on a 5 by 5 by 3 grid with a circle through it; a slider on az turns the camera","spec":{"kind":"space","params":{"x":[-3,3],"y":[-3,3],"z":[-2,2],"equal":true,"camera":{"az":-45,"el":30},"fields":[{"id":"F","F":["-y","x","0.3"],"n":[5,5,3],"label":"$\\mathbf{F}$","colour":1}],"curves":[{"id":"c","x":"2*cos(t)","y":"2*sin(t)","z":"0","t":[0,6.2832],"colour":2,"dashed":true}]},"controls":[{"bind":"az","min":-180,"max":180,"step":5,"label":"Azimuth","start":-45}]}},
```

Screenshots of each (light and dark, desktop and phone, before and after a drag; file names are `<n>-space-<example>-<theme>-<desktop|mobile>-<before|after>.png` in `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/shots/`):

| gallery entry | n | example | desktop, light, before | phone, dark, after |
|---|---|---|---|---|
| `space` (the sample) | 0 | `space` | `shots/0-space-light-desktop-before.png` | `shots/0-space-dark-mobile-after.png` |
| vectors and a span | 1 | `space-vectors-and-a-span-` | `shots/1-space-vectors-and-a-span--light-desktop-before.png` | `shots/1-space-vectors-and-a-span--dark-mobile-after.png` |
| helix and tangent | 2 | `space-helix-and-tangent-` | `shots/2-space-helix-and-tangent--light-desktop-before.png` | `shots/2-space-helix-and-tangent--dark-mobile-after.png` |
| surface z = f(x, y) | 3 | `space-surface-z-f-x-y-` | `shots/3-space-surface-z-f-x-y--light-desktop-before.png` | `shots/3-space-surface-z-f-x-y--dark-mobile-after.png` |
| mesh, height and a sphere | 4 | `space-mesh-height-and-a-sphere-` | `shots/4-space-mesh-height-and-a-sphere--light-desktop-before.png` | `shots/4-space-mesh-height-and-a-sphere--dark-mobile-after.png` |
| vector field | 5 | `space-vector-field-` | `shots/5-space-vector-field--light-desktop-before.png` | `shots/5-space-vector-field--dark-mobile-after.png` |

(The sample and the "vectors and a span" entry show the same scene; the sample goes through `ZQ.canvas.create` and the entry through `renderItem` with a caption.)

## Follow-ups (not built)

1. **Drag in 3D.** A draggable point or vector head (held to a plane or an axis, for example the xy-plane at fixed z), with `points()` and `place()` so the `drag-point` widget works; the screen-space ray to plane maths is straightforward with the camera basis already in `space.js`.
2. **True 3D arrowheads.** Heads are flat screen-space triangles (they read well, but a vector pointing at the viewer shows only a dot-sized head). A small cone built from quads would also help depth cues.
3. **Exact intersections.** Painter's order is per piece; two large pieces that interpenetrate (a plane and a surface cutting each other through their middles) can show a jagged seam at the cut. A cut line (plane against surface, level curves, contours on a surface) would fix that and is useful in its own right.
4. **Wheel zoom and auto-rotate.** Left out on purpose (a wheel would hijack the page scroll); an opt-in `wheel: true` and an `autoRotate` camera patch are small.
5. **Tangent planes and gradient helpers.** Authors can build them from `planes` with `through` and `normal` formulas, but a `tangent: { surface, at }` shorthand would save a derive.
6. **Smooth shading.** Cells are flat-shaded in 16 levels from averaged vertex normals; a coarse surface still shows its cells. Gouraud shading would need per-vertex colour (SVG gradients per cell are too slow), so the likely route is more cells on the budget or a canvas bitmap for surfaces only.
7. **Highlight glow across interleaved pieces.** The glow is a filter per run of pieces; when other objects sort between an object's pieces the glow of a later run lies over the earlier one (cosmetic, seen on a vector lying in a highlighted plane).
8. **The other half of item 432** (a z-plane grid beside its image under f) is a separate canvas and was not part of this pass.

## Validator test cases (scratch)

Scratch lesson `scratchpad/space/content/courses/algo-think/lz-bad.json` holds one canvas with these mistakes; each gives the error shown (46 in all; paths are under `screens[0].canvas`).

| mistake | error |
|---|---|
| `x: [3, -3]` | `.params.x: x is [min, max] with min below max` |
| `aspect: [1, 0, 1]`, `height: 100`, `perspective: 2`, `grid: "all"`, `box: "yes"` | one error each (aspect, height, perspective, grid, box) |
| `camera: { az: "x", el: 120, zoom: 9 }` | `.params.camera.az`, `.el`, `.zoom` |
| two vectors with id `u`; a vector with no id | `duplicate id "u"`; `every entry needs an id` |
| `v: [1, 2]` | `a point or vector is three coordinates [x, y, z]` |
| vector `v: [1, 2, "a+q"]` | `unknown name "q" in "a+q": a formula here may use the params (a) ...` |
| `from: "nope"`, `labelPos: "left"` | `from is [x, y, z] or the id of a point or another vector`; `labelPos is "end" or "mid"` |
| point `on: "zz"`, `at: "cc"` without `t` | `on names a surface id (one of ...)`, `at names a curve id`, `a point on a curve needs t` |
| curve `y: "sin(q)"`, `t: [0]`, `n: 2` | unknown name `q`; `t is [from, to]`; `n is 8 to 600 samples` |
| line with one point | `a line needs pts: at least two [x, y, z] points` |
| surface `{ id }` only; `z: "x*y("`; `n: 99`, `shade: "matte"`, `wire: "lines"`, `opacity: 2`, `clip: "cut"` | one error each, including `unbalanced brackets in "x*y("` |
| parametric surface using `w`, no `u`, `v` | `unknown name "w"`; `a parametric surface needs u: [from, to] and v: [from, to]` |
| plane `{ id }` only; `span: ["u", "none"]`, `res: 2`, `extent: [1, 2, 3]` | `a plane needs span ... or normal`; `"none" is not a vector id on this canvas`; `res is 3 to 24`; `extent is [lo, hi] ...` |
| field `F` with two formulas; `F[2]: "k"`, `n: 9`, `at: [1, 2]` | `a field needs F: three formulas`; unknown name `k`; `n is 1 to 7 ...`; `at is [x, y, z]` |
| `state.camera.zoom: 0.1`, `state.hide: "u"`, `state.vectors.u.colour: 9` | one error each |

The valid specs (the six gallery objects, the scratch lesson) give no `space` error.

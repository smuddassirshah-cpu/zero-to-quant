# Engine breadth pass 2: plane (item 431)

Vector-field, slope-field and trajectory layers on the `plane` canvas. Only `app/js/engine/canvas/plane.js` changed (153 added lines, none removed or altered); no helper file was needed.

## What changed

Three optional layers read by `plane` (all new keys, so a plane without them draws exactly as before):

- `field: { id, P, Q, ... }`: arrows of (P(x, y), Q(x, y)) on a grid. Optional `normalise`, `colourBy: "magnitude"` (an eight-step ramp from `colour` to `colourHigh`, one SVG path per step), `range`, `grid`, `spacing`, `length`, `anchor`, `maxArrows`.
- `slopeField: { id, f, ... }`: unit-length segments of slope dy/dx = f(x, y), the same grid options, `colourBy` by steepness.
- `trajectory: { id, in, from | starts, ... }`: fixed-step RK4 from a start, forward and optionally backward, in a field (time) or slope field (x), or by arc length (`by: "arc"`). `from` is a point id, so the existing `points` drag machinery (`drag: true`, `drag-point` widgets, `place`, patches) moves the start and the curve redraws on every pointer frame. `starts` gives up to 24 fixed curves.

Design points:

- Each layer is one object or a list, in `params` or `state`; a state entry merges over the params entry with the same id (as `functions` do). Formulas go through `ZQ.cvb.fnOf` (the curve expression compiler) with the names `x`, `y` and the plane params, so a slider bound to a param redraws the layer through the existing `state.params` path. `hide` by id still evaluates, so a trajectory can follow an undrawn field.
- Cost caps: arrows default to at most 360 (hard 600; the step widens until the grid fits), one path element per colour step, not per arrow; trajectories cap at `maxSteps` 2000 (hard 5000) per curve and direction, and 24 fixed starts; paths thin to 0.75 px spacing. Arrow nodes sit at multiples of a nice step (the origin is a node) and keep half an arrow clear of the frame.
- The steps are adjusted to divide `length` exactly, so a full orbit closes. The curve stops at the view edge (the last step is cut exactly at the edge, so it is clipped cleanly), at a stationary point and where the field is NaN.
- Arrow and segment directions are computed in screen space through the scales (so log axes and unequal axes draw tangent to the drawn curves); `equal: true` gives true angles.
- `values()` adds `<id>EndX` and `<id>EndY` (forward end of the `from` curve) for `derive` and captions, for example a caption `{{round(values.TEndX, 2)}}`.
- The field and trajectory groups are `.cv-obj` groups with their id (highlightable, hideable); the field group has `pointer-events: none`. The trajectory group sits over curves and under points, so dragging is unaffected. Styling uses only existing classes and tokens (`cvb-ln`, `cvb-head`, `cvb-dot`, `--s1..6`, `--text-muted`); no CSS change was needed. Default field colour is the muted ink, default trajectory slot 2.

## How it was checked

- Numerical (Playwright on the scratch copy, `ZQ.canvas.create` and `values()`): rotation field (y, -x), one period, step 0.01 ends at (1, 0) exactly; dy/dx = y from (0, 1) to x = 1 ends at (1, 2.718282) (e = 2.718282); arc mode on (10y, -10x) over length 2π ends at (1, 0); a step cap with step 1e-9 draws nothing and does not hang; a stationary start, an undefined field (`ln(x)` at -1), a missing point id, `hide`, a state patch by id and a `clone()` (the Why? copy) all behave. Worst case (344 arrows plus two 5000-step curves) redraws in 11 ms (desktop Chromium), 20 slider steps averaged.
- Screenshots: three gallery examples in light and dark, desktop (1100 px) and 390 px, plus after moving the slider to its maximum and after dragging P (a Playwright script that drags the handle, moves the slider and switches the theme; caption `Ends near (...)` updated while dragging). No console errors (the only message is the offline CDN tunnel failure).
- Scratch copy `routes-only` playthrough (includes `#system` with the new gallery cards): all passed.
- Regression from `app/` in the repo: `node tools/validate.mjs`: 0 errors. Then `node tools/playthrough.mjs ... --local-cdn <pkgs>` on every file whose JSON contains canvas kind `plane`: **316 items, all passed** (292 lessons, 19 level reviews and homework sets, 5 exams), run as four parallel processes. I did not run the full `--all`; the integration agent runs it after merging the five parts.
- Validator rules (below) tested on a scratch copy of `validate.mjs` with 11 cases (two good, nine bad), all as expected.

Screenshots (all in `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/shots/`; `-390` is mobile width, `slid` is after the slider moved to its maximum, `dragged` is after moving P):

- `plane-vector-field-light.png`, `-dark.png`, `-light-390.png`, `-dark-390.png`, `-slid.png`, `-slid-390.png`
- `plane-slope-field-light.png`, `-dark.png`, `-light-390.png`, `-dark-390.png`, `-slid.png`, `-slid-390.png`
- `plane-dragged-trajectory-light.png`, `-dark.png`, `-light-390.png`, `-dark-390.png`, `-dragged.png`, `-dragged-390.png`

Known limits, by design: a slope field is followed in x (RK4 in x), so a near-vertical solution is inaccurate unless `by: "arc"` is set; the curve stops at its first exit from the view (it does not re-enter); the colour ramp mixes two series slots in sRGB, so blue to orange passes through a dusty purple.

## Shared-file changes

### validate.mjs

Insert after the line `listOf(S.points).forEach((q, i) => { if (isObj(q) && q.tap != null ...` (the last line inside `if (c.kind === 'plane') { ... }`, in `checkCanvas`), before the closing brace of that block. It uses `P`, `S`, `where`, `file`, `err`, `warn`, `isObj`, `listOf` and `slotOk`, all in scope there.

```js
    /* item 431: field, slopeField and trajectory layers on a plane (in params or state; an object or a list of objects) */
    {
      const COLOURS = ['ink', 'manip', 'hint', 'neg', 'pos', 'muted'], colourOk = (v) => v == null || slotOk(v) || COLOURS.includes(v);
      const num = (v, lo, hi) => typeof v === 'number' && Number.isFinite(v) && v >= lo && v <= hi, pair = (v) => Array.isArray(v) && v.length === 2 && v.every((x) => typeof x === 'number');
      const exprOk = (v) => typeof v === 'string' || typeof v === 'number';
      const merged = (key) => { // as the engine does: a state entry merges over the params entry with the same id
        const m = new Map();
        [['params', P], ['state', S]].forEach(([w, o]) => {
          if (o[key] == null) return;
          const list = Array.isArray(o[key]);
          [].concat(o[key]).forEach((q, i) => {
            const at = `${where}.${w}.${key}${list ? `[${i}]` : ''}`;
            if (!isObj(q)) { err(file, at, `${key} is an object (or a list of objects)`); return; }
            const id = q.id != null ? String(q.id) : i ? `${key}-${i}` : key;
            m.set(id, { ...(m.get(id) || {}), ...q, id, at });
          });
        });
        return m;
      };
      const fields = merged('field'), slopes = merged('slopeField'), trajs = merged('trajectory'), known = new Set([...fields.keys(), ...slopes.keys()]);
      const common = (q) => {
        if (q.grid != null && !(Array.isArray(q.grid) ? q.grid.length === 2 && q.grid.every((n) => num(n, 2, 60)) : num(q.grid, 2, 60))) err(file, `${q.at}.grid`, 'grid is a number of columns (2 to 60) or [columns, rows]');
        if (q.spacing != null && !(Array.isArray(q.spacing) ? q.spacing.length === 2 && q.spacing.every((n) => num(n, 1e-9, Infinity)) : num(q.spacing, 1e-9, Infinity))) err(file, `${q.at}.spacing`, 'spacing is a positive step in data units, or [dx, dy]');
        if (q.length != null && !num(q.length, 1e-9, Infinity)) err(file, `${q.at}.length`, 'length is a positive number (px for arrows and segments; the range of the variable for a trajectory)');
        if (q.maxArrows != null && !num(q.maxArrows, 4, 600)) err(file, `${q.at}.maxArrows`, 'maxArrows is 4 to 600');
        if (q.colourBy != null && q.colourBy !== 'magnitude' && q.colourBy !== true) err(file, `${q.at}.colourBy`, 'colourBy is "magnitude"');
        if (q.range != null && !(pair(q.range) && q.range[0] < q.range[1])) err(file, `${q.at}.range`, 'range is [lo, hi] with lo below hi');
        if (q.anchor != null && !['mid', 'tail'].includes(q.anchor)) err(file, `${q.at}.anchor`, 'anchor is "mid" or "tail"');
        if (q.normalise != null && typeof q.normalise !== 'boolean') err(file, `${q.at}.normalise`, 'normalise is true or false');
        if (!colourOk(q.colour) || !colourOk(q.colourHigh)) err(file, `${q.at}.colour`, 'colour and colourHigh are a slot 1 to 6 or ink, manip, hint, neg, pos, muted');
      };
      fields.forEach((q) => { ['P', 'Q'].forEach((k) => { if (!exprOk(q[k])) err(file, `${q.at}.${k}`, `a field needs P and Q: formulas in x, y and the params`); }); common(q); });
      slopes.forEach((q) => { if (!exprOk(q.f)) err(file, `${q.at}.f`, 'a slopeField needs f: the slope dy/dx as a formula in x, y and the params'); common(q); });
      const ptIds = new Set(listOf(S.points).filter(isObj).map((p) => String(p.id)));
      trajs.forEach((q) => {
        const startOk = (v) => (typeof v === 'string' && v !== '') || (pair(v));
        if (q.from == null && q.starts == null) err(file, q.at, 'a trajectory needs from (a point id or [x, y]) or starts (a list of them)');
        if (q.from != null && !startOk(q.from)) err(file, `${q.at}.from`, 'from is a point id or [x, y]');
        if (q.starts != null && !(Array.isArray(q.starts) && q.starts.length >= 1 && q.starts.length <= 24 && q.starts.every(startOk))) err(file, `${q.at}.starts`, 'starts is a list of 1 to 24 point ids or [x, y] pairs');
        [].concat(q.from ?? [], Array.isArray(q.starts) ? q.starts : []).forEach((s) => { if (typeof s === 'string' && !ptIds.has(s)) warn(file, `${q.at}`, `"${s}" is not a point id in state.points (a later patch may add it)`); });
        if (!known.size) err(file, q.at, 'a trajectory needs a field or slopeField layer to run in');
        else if (q.in != null && !known.has(String(q.in))) err(file, `${q.at}.in`, `in names a field or slopeField id (${[...known].join(', ')})`);
        if (q.step != null && !num(q.step, 1e-12, Infinity)) err(file, `${q.at}.step`, 'step is a positive number');
        if (q.length != null && !num(q.length, 1e-9, Infinity)) err(file, `${q.at}.length`, 'length is a positive number');
        if (q.back != null && typeof q.back !== 'boolean' && !num(q.back, 0, Infinity)) err(file, `${q.at}.back`, 'back is true (as far as length) or a length');
        if (q.by != null && !['arc', 'time'].includes(q.by)) err(file, `${q.at}.by`, 'by is "time" (the default; x for a slope field) or "arc" (length along the curve)');
        if (q.maxSteps != null && !(Number.isInteger(q.maxSteps) && q.maxSteps >= 10 && q.maxSteps <= 5000)) err(file, `${q.at}.maxSteps`, 'maxSteps is a whole number from 10 to 5000');
        ['arrow', 'dashed'].forEach((k) => { if (q[k] != null && typeof q[k] !== 'boolean') err(file, `${q.at}.${k}`, `${k} is true or false`); });
        if (!colourOk(q.colour)) err(file, `${q.at}.colour`, 'colour is a slot 1 to 6 or ink, manip, hint, neg, pos, muted');
      });
    }
```

Rules in words (for AUTHORING.md section 9, if the rules are listed): errors for a `field` without `P` and `Q`, a `slopeField` without `f`, a `trajectory` without `from` or `starts` or without any field layer, `in` naming no layer, `grid`, `spacing`, `length`, `maxArrows`, `colourBy`, `range`, `anchor`, `normalise`, `colour`, `step`, `back`, `by`, `maxSteps`, `arrow`, `dashed` of the wrong shape; a warning for a string `from` or `starts` entry that is not a point id in `state.points`.

Scratch cases run (patched copy, `content/courses/limits/l1-getting-closer.json` edited and restored): good field plus trajectory; good slope field plus a state trajectory from a point; field without Q; `grid: "big"`; `range: [3, 1]`; slope field without f; trajectory with no layer; `in: "Z"`; no start; six bad options in one trajectory (six errors); `from: "Q9"` (warning only).

### AUTHORING.md

Add to the plane sentence list in the pass notes (after the "Added in integration pass 5 ..." paragraph, or as its own paragraph):

> Plane field layers (item 431; the plane README has every option): `field: { "id": "F", "P": "-y", "Q": "x" }` draws arrows of (P(x, y), Q(x, y)) on a grid, `slopeField: { "id": "S", "f": "x - y" }` short segments of slope dy/dx = f(x, y), and `trajectory: { "id": "T", "in": "F", "from": "P" }` traces the solution through a start by fixed-step RK4. Formulas use `x`, `y` and the plane's `params`, so a slider bound to a param redraws the field. `from` is the id of a point with `drag: true` (or one a `drag-point` widget moves): the curve redraws live as it moves, and `starts: [[x, y], ...]` draws fixed curves. Options: `normalise: true` (equal arrows), `colourBy: "magnitude"` with `range`, `grid`, `back: true` (also run backwards), `length`, `step`, `by: "arc"`, `maxSteps`. Arrow counts and steps are capped, so a field costs little on a phone. `derive` can read the forward end as `values.TEndX` and `values.TEndY`. Use `equal: true` when arrow angles must be true.

### canvas/README-B.md

Add under `## plane`, after "Integration pass 7 additions" (title it "Integration pass 8 additions" if the integration agent keeps the pattern):

> **Vector fields, slope fields and trajectories (item 431)**
>
> Three optional layers on a `plane`, in `params` (fixed) or `state` (a state entry merges over the params entry with the same `id`; give the whole entry with its `id` when patching). Each is one object or a list of objects. Formulas use the same expression language as curves: `x`, `y`, the `params` (so a slider bound to a param redraws the layer, like a slider-bound curve), `+ - * / ^` and the usual functions. `hide: ["F"]` hides a layer by id but it still runs, so a trajectory can follow a field that is not drawn. All three are untouched by existing planes: a plane without these keys draws exactly as before.
>
> - `field: { id, P, Q, grid, spacing, normalise, length, colour, colourBy, colourHigh, range, anchor, maxArrows }`: arrows of (P(x, y), Q(x, y)).
>   - `grid` is the number of columns (default about one per 34 px of the plot) or `[columns, rows]`. Arrows sit at multiples of a nice step (so the origin and integers are nodes) and are kept clear of the frame. `spacing: s | [dx, dy]` sets the step in data units instead.
>   - `normalise: true` draws every arrow the same length (`length` px, default 80% of the cell, 8 to 30); otherwise length grows with magnitude, the largest arrow (or `range[1]`) taking the full length.
>   - `colour` is a slot 1 to 6 or a named colour (default `"muted"`, a quiet grey, so a trajectory stands out). `colourBy: "magnitude"` ramps the colour from `colour` (default slot 1) at the weakest arrow to `colourHigh` (default slot 2) at the strongest, in eight steps (one path element per step, so it stays cheap). `range: [lo, hi]` fixes the magnitudes at the two ends, so the colours and lengths do not shift as a slider moves.
>   - `anchor: "tail"` puts each arrow's tail on its node (default: centred). `maxArrows` (default 360, at most 600) caps the count: the step widens until the grid fits, so a phone never draws more.
>   - Arrow directions are drawn in screen space, so use `equal: true` for true angles. A zero or undefined vector leaves its node empty.
> - `slopeField: { id, f, grid, spacing, length, colour, colourBy, colourHigh, range, maxArrows }`: for dy/dx = f(x, y), a short segment of that slope at each node, all the same length (`length` px). `colourBy: "magnitude"` colours by steepness (the angle, by default; `range` instead gives |f| for the two ends). Same grid options as `field`.
> - `trajectory: { id, in, from, starts, step, length, back, by, maxSteps, arrow, dashed, colour, label }`: the solution curve through a start, by fixed-step RK4.
>   - `in` is the id of a `field` or `slopeField` (default: the first field, else the first slope field).
>   - `from` is a point id (a point with `drag: true`, or one a `drag-point` widget moves, so the curve redraws on every pointer frame) or `[x, y]`. `starts: [[x, y] | pointId, ...]` adds fixed starts (up to 24), each drawn the same way with a dot where it begins.
>   - A field is followed in time: `dx/dt = P, dy/dt = Q`. A slope field is followed in x. `length` is how far to go (default 10 for a field, the plot width for a slope field); `step` the RK4 step (default `length / 200`; the steps are adjusted to divide `length` exactly, so a full orbit closes). `back: true` also runs backwards for the same distance, or `back: 4` for that distance. `by: "arc"` follows the field normalised, so `length` and `step` are distances along the curve (default length three times the plot diagonal): use it for fields whose speed varies wildly, or for steep slope fields.
>   - `maxSteps` (default 2000, at most 5000) caps the work per curve and direction: a curve that would need more is cut short. The curve stops at the plot's edge (the last step is cut exactly at the edge), at a stationary point and where the field is undefined (a square root of a negative number).
>   - `arrow: false` removes the arrowhead at the forward end. `label` sits at the forward end.
>   - `values()` gives `<id>EndX` and `<id>EndY`, the forward end of the `from` curve, to `derive` (`values.TEndX`) and captions.
>

### js/screens/system.js

Add these three entries to `CANVAS_EXTRAS` (copied from the scratch gallery, which rendered and was screenshotted as listed above; the third reads `values.TEndX` in its caption):

```js
    { name: 'plane (vector field)', about: 'params.field: arrows of (P, Q) on a grid, normalise: true gives equal arrows, colourBy: "magnitude" ramps the colour; a bound slider redraws the field', spec: { kind: 'plane',
      params: { x: [-4, 4], y: [-4, 4], equal: true, height: 360, params: { a: 0.2 }, field: { id: 'F', P: 'a*x - y', Q: 'x + a*y', grid: 15, colourBy: 'magnitude', range: [0, 6] } },
      controls: [{ bind: 'a', min: -0.5, max: 0.5, step: 0.05, label: 'Spiral $a$', start: 0.2 }] } },
    { name: 'plane (slope field)', about: 'params.slopeField: segments of slope f(x, y) = sin(x) - a*y; two solution curves traced by RK4 forward and back; a slider on a', spec: { kind: 'plane',
      params: { x: [-6, 6], y: [-4, 4], params: { a: 0.5 }, xLabel: '$x$', yLabel: '$y$', slopeField: { id: 'S', f: 'sin(x) - a*y', grid: 17 }, trajectory: { id: 'T', in: 'S', starts: [[0, 2], [0, -1.5], [-4, 0]], back: true, colour: 2 } },
      controls: [{ bind: 'a', min: 0, max: 2, step: 0.1, label: 'Damping $a$', start: 0.5 }] } },
    { name: 'plane (dragged trajectory)', about: 'A damped pendulum field (y, -sin(x) - c*y) with a draggable start P; the RK4 trajectory runs forward and back and redraws as P or c moves', spec: { kind: 'plane',
      params: { x: [-6.3, 6.3], y: [-4, 4], params: { c: 0.3 }, xLabel: '$\\theta$', yLabel: '$\\omega$', field: { id: 'F', P: 'y', Q: '-sin(x) - c*y', grid: 19, normalise: true, colour: 'muted' }, trajectory: { id: 'T', in: 'F', from: 'P', length: 30, step: 0.05, back: 6 } },
      state: { points: [{ id: 'P', x: 1.5, y: 1.2, drag: true, label: 'P' }] }, derive: { caption: 'Ends near ({{round(values.TEndX, 2)}}, {{round(values.TEndY, 2)}})' },
      controls: [{ bind: 'c', min: 0, max: 1, step: 0.05, label: 'Friction $c$', start: 0.3 }] } },
```

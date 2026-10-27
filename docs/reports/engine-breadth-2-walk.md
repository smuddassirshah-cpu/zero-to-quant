# Engine breadth pass 2: walk (item 436)

Only `app/js/engine/canvas/walk.js` changed (223 lines added, 17 changed; 351 lines now). Every option is optional and a walk that uses none renders as before.

## What changed

1. **Overlays** (`params.overlays`: `"sq"`, `"ratio"`, `"bankroll"`, or objects `{ id, type, label, chip, colour, y, expr, ... }`). Each visible overlay is its own panel under the walk, on the walk's step axis and its own y scale, drawn like the walk (faint paths, the bold path, the bold index shared). The frame grows by the panels shown (`R.F.resize`). One chip per overlay (class `cvb-chip`, in `R.extra`, not in static copies) toggles it; `state.overlays` (a list of ids, `true`, `false`) does the same from lessons, `derive` and frames.
   - `sq`: `(S_n - n m)^2 - n v^2` with the walk's own drift m and variance v^2 (coin: m = (2p-1) step, v^2 = 4pq step^2). At p = 1/2 and step 1 this is S_n^2 - n and the label says so. `centred: false` gives the literal S_n^2 - n (not a martingale when p is not 1/2).
   - `ratio`: `(q/p)^(S_n)` with p, q the walk's own step probabilities (S_n in steps). The normal model gets `exp(-2 mu S_n / sigma^2)`. Not defined for the markov or mean-reverting model, or p of 0 or 1 (the panel says so).
   - `bankroll`: start `bankroll` (default 100), a bet every step won or lost with the step. Rule `bet` (param, overlay key or `state.bet`): `fixed` (`stake`), `double` (stake, doubled after each loss, back to stake after a win), `fraction` (`fraction` of the bankroll). A bet never exceeds the bankroll or `maxBet`; at zero the bankroll stays ruined. `bankroll`, `stake` and `fraction` are slider-bindable top-level numbers.
   - `expr`: any formula in `n`, `x` (position), `S` (position less start, in steps for the coin), `p`, `q`, `start`, `step` and every numeric param (so slider names work), for example the cubic martingale `S^3 - 3 * n * S`.
   - Axis ranges: sq uses min and max; ratio and bankroll trim the top at the 95th percentile of the per-path maxima so one explosive path does not flatten the rest (paths are clipped at the panel edge). `y: [lo, hi]` on an overlay fixes the range.
2. **Average at stopping** (`state.showStopped`: `true` or `"walk"` for S_tau, an overlay id, or a list). Stopping time tau = first barrier hit, capped by `params.stopAt` (a fixed step, drawn as a dashed "stop" line) and by `steps`, so tau is bounded and the optional stopping theorem applies. A panel under the walk plots the running mean of the stopped value over the first k paths (x = paths averaged, up to `paths`), a dashed line at the start value and the labels "start" and "mean". Stopped values are also marked as dots at tau on every drawn path. With `stopAtBarrier` the paths (and overlays) end at tau. `params.drawn: n` draws only n paths while all `paths` count in the statistics, so 300 paths stay readable. A new run builds the running mean up with the reveal.
3. **Barriers bound to sliders**: top-level `lower` and `upper` replace `barriers[0]` and `[1]`; a control `bind: "upper"` writes `state.params.upper` and the barrier, hit dots, counts, stopped paths and the stopped average redraw live. `getParam` makes the slider open on the barrier (so `barriers: [-8, 8]` with `bind: "upper"` opens at 8). The held y range resets when a barrier moves or the drawn set changes (otherwise the axis never shrank).
4. **Mean-reverting model**: `model: "ou"` (also `"mean-reverting"`, `"ar1"`): X(n+1) = X(n) + theta (mu - X(n)) + sigma Z on the same seeded normal draws, so sliders on `theta`, `mu`, `sigma` morph the same paths. The level mu is a dashed line labelled "mu = ..." (`meanLine: false` hides it, `levelLabel` renames it); `showMean` draws the expected path mu + (x0 - mu)(1 - theta)^n and `showSpread: k` the +/- k sd band sigma sqrt((1 - phi^2n)/(1 - phi^2)), phi = 1 - theta.
5. **derive**: `derive` already reads `canvas.values()` into `values.<name>`; walk now provides it (see below). New methods: `values()`, `stopTimes()`, `stopped(key)`, `runningMean(key)`, `getParam(name)`.

`values()` keys: `paths`, `hits`, `hitsUp`, `hitsDown`, `stopAt`, `tau` (list), `tauMean`, `endMean` (mean of the last step, no stopping), `stopped` (mean of S_tau), `stoppedSE`, `stoppedValues` (list), `runningMean` (list), and per overlay id (capitalised, non-word characters as `_`): `stoppedSq`, `stoppedRatio`, `stoppedBankroll` (each with `...SE`), `runningMeanSq` ..., and `ruinedBankroll` (paths at zero at tau). Example: `"caption": "Mean of S at the stop: {{fixed(values.stopped, 2)}}; {{values.hitsUp}} hit the top"`.

## How it was checked

Scratch copy of `app/` at `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/walk/app` (walk.js copied in, gallery entries added to the copy's `js/screens/system.js`, never to the repo). Scripts in `/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/walk`: `shots.mjs` (every example, light and dark, 1280 and 390 px, console errors collected: none), `inter.mjs` (moves the barrier, p, stake, theta, mu and sigma sliders, clicks the overlay chips, reads the derive caption and the viewBox), `misc.mjs` (animated `run()`, `clone()`, `enable('tap')`, highlight, markov and mean-reverting with overlays, normal-model ratio), `regress.mjs`, `num.mjs`.

- **Numbers**, 20,000 seeded paths, barriers -8 and 8, 80 steps, against an exact dynamic programme in Python (probability mass moved step by step, absorbed at the barriers, the rest stopped at step 80):

  | quantity | canvas | exact |
  |---|---|---|
  | p = 0.5, mean S_tau | -0.018 (SE 0.050) | 0 |
  | p = 0.5, mean S_tau^2 - tau | -0.0015 (SE 0.32) | 0 |
  | p = 0.5, hit top / bottom | 7340 / 7330 of 20000 (0.367) | 0.3669 each |
  | p = 0.5, mean tau | 49.998 | 50.012 |
  | p = 0.5, fixed-stake bankroll (stake 5, start 100) | 99.91 (SE 0.25) | 100 |
  | p = 0.5, doubling bankroll | 100.14 (SE 0.77) | 100 |
  | p = 0.45, mean S_tau | -4.598 (SE 0.041) | -4.533 |
  | p = 0.45, mean (q/p)^S_tau | 0.983 (SE 0.011) | 1 |
  | p = 0.45, centred sq at tau | -0.605 (SE 0.389) | 0 |
  | p = 0.45, hit top / bottom | 0.1329 / 0.679 | 0.1357 / 0.6758 |
  | p = 0.45, mean tau | 45.35 | 45.33 |
  | p = 0.45, fixed bankroll | 77.01 | 100 + 5 (-4.533) = 77.3 |

  All within about 1.6 standard errors. The gallery example with 300 paths shows -0.12 (start 0) with seed 7.
- **Existing walks unchanged**: `regress.mjs` renders all 24 walk canvases found in `app/content` (params and state), each plainly and with `showHits, stopAtBarrier, showMean, showSpread, run: 1`, with the old and new walk.js: 48 renders, 0 differences in the SVG markup.
- `node tools/validate.mjs` from `app/`: 0 errors.
- Playthrough with `--local-cdn` of every lesson and set that uses a walk: arma/l1-returns-not-prices, arma/l5-own-past, coint/l1-two-walks, garch/l1-calm-and-storms, markov/l9-coin-flip-walk, l10-gamblers-ruin, l11-reflection, l12-price-paths, l15-sampling-by-chain and set markov/review-3: all passed. `--routes-only` (includes `#system`): all passed.
- **Full `--all` run not completed**: it ran about 95 lessons cleanly and then Chromium was closed under it ("Target page, context or browser has been closed", every later line), most likely by another agent's process in the shared sandbox, and a full run is over two hours (775 lessons, 370 sets, 19 exams). No lesson outside the ten above instantiates a walk. The integration agent should run it once the five parts are in.
- Validator rules were tested on a scratch copy of `validate.mjs` with a scratch lesson (three valid walk specs and thirteen bad ones, each flagged with the expected message; no new errors on any existing file).

Screenshots (`/tmp/claude-0/-home-user-zero-to-quant/b05d2d5c-c0fd-5be4-a78a-5f4cfc7634ce/scratchpad/walk/shots/`, each as `-light`, `-dark`, `-light-390`, `-dark-390`): `walk_overlays_under_the_walk_overlays_p`, `walk_stopped_average_slider_barriers_b`, `walk_optional_stopping_with_drift_at_p_`, `walk_mean_reverting_model_ou_X_n_1_`, `walk_custom_overlay_fixed_stop_an_expr`; interaction shots `inter-barriers-3.png`, `inter-barriers-20.png`, `inter-chips-bank.png`, `inter-chips-p03.png`, `inter-ou.png`.

Known limits: the panels are 540 units wide like the rest of the canvas, so on a 390 px phone the type is small (the same as every walk today); a frame with four panels is about 900 units tall. A new overlay toggle changes the frame height, so the page below moves. The first 8 percent of a stopped average can leave the panel (the range follows the later, settled part).

## Shared-file changes

### ENGINE-BACKLOG.md
Item 436: `Done (engine breadth pass 2, walk): overlays sq, ratio, bankroll and expr, average at stopping, lower and upper barrier params, model "ou", values() for derive.`

### validate.mjs
1. Replace the `walk:` line of `PLAUSIBLE` (id check for highlight ids) with:

```js
  walk: /^(path\d+|barrier-up|barrier-down|mean|mean-level|spread|envelope|stop-time|stopped-ref|stopped-[\w-]+|ov-[\w-]+)$/,
```

2. Insert this block in `checkCanvas`, immediately before the existing line `if (c.kind === 'walk' && P.model === 'markov' && ...`:

```js
  /* item 436: walk overlays, the average at stopping, slider-bound barriers and the mean-reverting model */
  if (c.kind === 'walk') {
    const num = (v) => typeof v === 'number' && Number.isFinite(v);
    if (P.model != null && !['coin', 'normal', 'markov', 'ou', 'mean-reverting', 'ar1'].includes(P.model)) err(file, `${where}.params.model`, 'model is coin, normal, markov, ou (also mean-reverting or ar1)');
    ['theta', 'stopAt', 'stake', 'fraction', 'bankroll', 'maxBet', 'overlayHeight', 'drawn'].forEach(k => { if (P[k] != null && !(num(P[k]) && P[k] >= 0)) err(file, `${where}.params.${k}`, `${k} is a number, 0 or more`); });
    ['lower', 'upper'].forEach(k => { if (P[k] != null && !num(P[k])) err(file, `${where}.params.${k}`, `${k} is a number (a barrier level; a slider may bind it)`); });
    if (num(P.lower) && num(P.upper) && P.lower >= P.upper) err(file, `${where}.params`, 'lower must be below upper');
    if (P.bet != null && !['fixed', 'double', 'fraction'].includes(P.bet)) err(file, `${where}.params.bet`, 'bet is "fixed", "double" or "fraction"');
    if (P.model === 'ou' || P.model === 'mean-reverting' || P.model === 'ar1') { if (P.p != null || P.step != null) warn(file, `${where}.params`, 'a mean-reverting walk reads theta, mu, sigma and start; p and step are ignored'); }
    const ids = [];
    if (P.overlays != null) {
      if (!Array.isArray(P.overlays)) err(file, `${where}.params.overlays`, 'overlays is a list of "sq", "ratio", "bankroll" or objects { id, type, label, chip, colour, y, expr }');
      else P.overlays.forEach((o, i) => {
        const w = `${where}.params.overlays[${i}]`, ob = isObj(o) ? o : { id: o }, type = ob.type || (ob.expr ? 'expr' : ob.id);
        if (typeof o !== 'string' && !isObj(o)) { err(file, w, 'an overlay is an id string or an object'); return; }
        if (!['sq', 'ratio', 'bankroll', 'expr'].includes(type)) err(file, w, 'an overlay is "sq", "ratio" or "bankroll", or has an expr (type "expr")');
        if (type === 'expr' && typeof ob.expr !== 'string') err(file, `${w}.expr`, 'an expr overlay needs a formula in S, n, x, p, q, start, step and the numeric params');
        if (type === 'expr' && typeof ob.expr === 'string') { try { new Function('F', 'x', 'S', 'n', 'p', 'q', 'start', 'step', 'mu', 'sigma', 'theta', 'return (' + ob.expr.replace(/\^/g, '**') + ');'); } catch { err(file, `${w}.expr`, 'the formula does not parse'); } }
        if (type === 'expr' && !ob.id) warn(file, w, 'give an expr overlay an id (it names the chip, the highlight id ov-<id> and showStopped)');
        if (ob.bet != null && !['fixed', 'double', 'fraction'].includes(ob.bet)) err(file, `${w}.bet`, 'bet is "fixed", "double" or "fraction"');
        if (ob.y != null && !(Array.isArray(ob.y) && ob.y.length === 2 && ob.y.every(num))) err(file, `${w}.y`, 'y is [min, max] for the overlay panel');
        if (ob.colour != null && !(Number.isInteger(ob.colour) && ob.colour >= 1 && ob.colour <= 6)) err(file, `${w}.colour`, 'colour is a series slot, 1 to 6');
        const id = String(ob.id || type); if (ids.includes(id)) err(file, w, `two overlays share the id "${id}"`); ids.push(id);
      });
      if (P.model === 'markov') warn(file, `${where}.params.overlays`, 'overlays are not drawn for a markov walk');
      if (P.model === 'normal' || P.model === 'ou' || P.model === 'mean-reverting' || P.model === 'ar1') { if ((P.overlays || []).some(o => (isObj(o) ? o.type || o.id : o) === 'ratio') && (P.model !== 'normal')) warn(file, `${where}.params.overlays`, 'the ratio overlay is defined for the coin and normal models only'); }
    }
    const known = (id) => id === 'walk' || ids.includes(id);
    if (S.overlays != null && typeof S.overlays !== 'boolean' && !(Array.isArray(S.overlays) && S.overlays.every(x => typeof x === 'string'))) err(file, `${where}.state.overlays`, 'overlays is true, false or a list of overlay ids');
    if (Array.isArray(S.overlays)) S.overlays.forEach(id => { if (typeof id === 'string' && !ids.includes(id)) err(file, `${where}.state.overlays`, `no overlay "${id}" in params.overlays`); });
    if (S.showStopped != null) {
      const list = S.showStopped === true ? ['walk'] : [].concat(S.showStopped);
      if (S.showStopped !== false && !list.every(x => typeof x === 'string')) err(file, `${where}.state.showStopped`, 'showStopped is true ("walk"), an overlay id, or a list of them');
      else list.forEach(id => { if (!known(id)) err(file, `${where}.state.showStopped`, `"${id}" is not "walk" or an overlay id`); });
      if (S.showStopped !== false && !(Array.isArray(P.barriers) || P.lower != null || P.upper != null || P.stopAt != null)) warn(file, `${where}.state.showStopped`, 'showStopped without barriers or stopAt averages the value at the last step');
      if (S.showStopped !== false && !(num(P.paths) && P.paths >= 2)) warn(file, `${where}.params.paths`, 'the average at stopping needs several paths (use 100 or more, and drawn to draw fewer)');
    }
    if (S.bet != null && !['fixed', 'double', 'fraction'].includes(S.bet)) err(file, `${where}.state.bet`, 'bet is "fixed", "double" or "fraction"');
    if (Array.isArray(P.barriers) && (num(P.lower) || num(P.upper))) warn(file, `${where}.params`, 'lower and upper replace the matching entry of barriers');
  }
```

### docs/AUTHORING.md
In the canvas table, replace the `walk` row with:

```
| `walk` | `steps`, `p`, `start`, `paths`, `drawn`, `barriers: [a,b]`, `lower`, `upper`, `stopAt`, `sim: { "seed": 1 }`, `model: "ou"` with `theta`, `mu`, `sigma`, `overlays: ["sq", "ratio", "bankroll"]` with `bankroll`, `stake`, `fraction`, `bet` | `run: n`, `showMean`, `showSpread`, `showHits`, `stopAtBarrier`, `showStopped`, `overlays`, `bet`, `highlight: [pathIndex]` | `path{i}`, `barrier-up`, `barrier-down`, `mean`, `mean-level`, `spread`, `stop-time`, `ov-{id}`, `stopped-{key}`, `stopped-ref` |
```

In the derive paragraph (after "A derive reads plain objects in state by name too"), add:

```
A `walk` canvas gives derive `values.stopped` (the mean of the walk at its stopping time), `values.stoppedSq`, `values.stoppedRatio`, `values.stoppedBankroll` (an overlay's mean at the stop; the name is `stopped` plus the overlay id), `values.runningMean` (list), `values.hits`, `values.hitsUp`, `values.hitsDown`, `values.tauMean` and `values.endMean` (the mean of the last step with no stopping), so a caption can read "{{fixed(values.stopped, 2)}}" beside sliders that move the barriers.
```

Add to the "Added in integration pass" paragraph, or a new line below it:

```
Engine breadth pass 2 (walk): overlay panels under the walk (`overlays`: `"sq"` for S_n^2 - n, `"ratio"` for (q/p)^S_n, `"bankroll"` with a bet rule, or `{ id, expr }` for any formula in `n`, `S`, `x`, `p`, `q`), the running average of the stopped value across seeded paths (`showStopped`), barriers that follow sliders (`lower`, `upper`) and a mean-reverting model (`model: "ou"`, sliders on `theta`, `mu`, `sigma`).
```

### canvas/README-B.md (walk section)
Append under `**state**` and `**ids:**`, and add this block after the "Integration pass 6 additions" paragraph:

```
**Engine breadth pass 2 additions (item 436)**

- `model: "ou"` (also `"mean-reverting"`, `"ar1"`): X(n+1) = X(n) + `theta` (`mu` - X(n)) + `sigma` Z on the seeded normal draws, from `start`. `theta`, `mu` and `sigma` are slider-bindable, and sliding them morphs the same paths. The level `mu` is a dashed line labelled "mu = 2" (`meanLine: false` hides it, `levelLabel` renames it). `showMean` draws the expected path mu + (start - mu)(1 - theta)^n; `showSpread: k` draws the +/- k sd band of the AR(1) variance. Give `y: [lo, hi]` so the axis holds still while sliders move.
- `lower`, `upper` (params): barrier levels that replace `barriers[0]` and `barriers[1]`. A control `{ "bind": "upper", "min": 2, "max": 20, "step": 1 }` moves the barrier; hit dots, counts, `stopAtBarrier` paths and the stopped average redraw live, and the slider opens on the barrier. The held y range resets when a barrier moves.
- `stopAt: n` (param): a fixed stopping step; tau = min(first barrier hit, `stopAt`, `steps`). A dashed line marks it (`stopLabel` renames "stop"). With `stopAtBarrier` paths end at tau.
- `drawn: n` (param): draw only n paths (and the bold one); all `paths` still count in hits, stopped values and the running average. Use 300 paths with `drawn: 30`.
- `overlays` (params): the panels that can sit under the walk, each on the walk's step axis and its own y scale. An entry is an id string or `{ id, type, label, chip, colour, y, ... }`:
  - `"sq"`: (S_n - n m)^2 - n v^2 for the walk's drift m and variance v^2; at p = 1/2 and step 1 it is S_n^2 - n. `centred: false` gives the literal S_n^2 - n.
  - `"ratio"`: (q/p)^S_n with p and q the walk's own step probabilities (coin); for the normal model exp(-2 mu S_n / sigma^2). Not defined for markov or ou, or p of 0 or 1.
  - `"bankroll"`: `bankroll` (start, default 100) plus the winnings of a bet every step. `bet` (param, overlay key or `state.bet`): `"fixed"` (`stake`, default 1), `"double"` (stake, doubled after each loss, back to stake after a win), `"fraction"` (`fraction` of the bankroll, default 0.1). A bet never exceeds the bankroll or `maxBet`; at zero the bankroll stays ruined. `bankroll`, `stake` and `fraction` take sliders.
  - `{ "id": "cube", "expr": "S^3 - 3 * n * S" }`: any formula in `n` (step), `x` (position), `S` (position less start, in steps for the coin), `p`, `q`, `start`, `step` and the numeric params; `label` and `stopLabel` take `$...$`.
  - `y: [lo, hi]` fixes an overlay's range; otherwise ratio and bankroll trim the top at the 95th percentile of the per-path maxima. `overlayHeight` (default 84) is each panel's plot height in px. `toggles: false` hides the chips.
- `state.overlays`: the ids shown (a list; `true` for all, the default; `false` for none). Each overlay also has a chip under the canvas (`chip` renames it). A chip emits `{ type: "overlay", id, on, overlays }`.
- `state.showStopped`: `true` or `"walk"` (S_tau), an overlay id, or a list. Adds a panel per entry: the running mean of the stopped value over the first k paths against k, a dashed line at the start value, and "start" and "mean" labels; stopped values are dots at tau on the paths. Needs several seeded paths (100 or more).
- `state.bet`: the bankroll rule, patchable.
- **ids:** also `mean-level` (ou), `stop-time`, `ov-{id}` (an overlay), `stopped-{key}` (a running-mean line), `stopped-ref`.
- **methods:** also `values()` (numbers for derive: `paths`, `hits`, `hitsUp`, `hitsDown`, `stopAt`, `tau`, `tauMean`, `endMean`, `stopped`, `stoppedSE`, `stoppedValues`, `runningMean`, and `stopped<Id>`, `stopped<Id>SE`, `runningMean<Id>`, `ruined<Id>` per overlay, for example `stoppedRatio`), `stopTimes()`, `stopped(key)`, `runningMean(key)` (key `"walk"` or an overlay id) and `getParam(name)`.

```json
{ "kind": "walk",
  "params": { "steps": 80, "p": 0.5, "paths": 300, "drawn": 30, "barriers": [-8, 8], "overlays": ["sq"], "sim": { "seed": 7 } },
  "state": { "stopAtBarrier": true, "showStopped": true },
  "derive": { "caption": "Mean at the stop: {{fixed(values.stopped, 2)}}" },
  "controls": [{ "bind": "upper", "min": 2, "max": 20, "step": 1, "label": "Upper barrier" }] }
```

### js/screens/system.js
Insert at the start of `CANVAS_EXTRAS` (tested exactly as written in the scratch copy):

```js
    { name: 'walk (overlays under the walk)', about: 'overlays plot S_n^2 - n, (q/p)^S_n and a doubling bankroll against n, each on its own panel; chips toggle them; p and the base stake are sliders', spec: { kind: 'walk',
      params: { steps: 60, p: 0.45, paths: 25, xStep: 10, height: 240, overlays: ['sq', 'ratio', { id: 'bankroll', bet: 'double' }], bankroll: 100, stake: 2, sim: { seed: 4 } },
      state: { showMean: true },
      controls: [{ bind: 'p', min: 0.3, max: 0.7, step: 0.05, label: '$p$' }, { bind: 'stake', min: 1, max: 10, step: 1, label: 'Base stake' }] } },
    { name: 'walk (stopped average, slider barriers)', about: 'barriers bound to sliders (lower, upper) re-stop 300 paths live; the average of S_tau settles on the start value; derive reads values.stopped and values.hitsUp', spec: { kind: 'walk',
      params: { steps: 80, p: 0.5, paths: 300, drawn: 30, height: 240, barriers: [-8, 8], sim: { seed: 7 } },
      state: { stopAtBarrier: true, showHits: true, showStopped: true },
      derive: { caption: 'Mean of S at the stop: {{fixed(values.stopped, 2)}} (start 0). At step 80 without stopping: {{fixed(values.endMean, 2)}}. {{values.hitsUp}} hit the top, {{values.hitsDown}} the bottom.' },
      controls: [{ bind: 'upper', min: 2, max: 20, step: 1, label: 'Upper barrier' }, { bind: 'lower', min: -20, max: -2, step: 1, label: 'Lower barrier' }, { reseed: true, label: 'New paths' }] } },
    { name: 'walk (optional stopping with drift)', about: 'at p = 0.45 the average of S_tau misses the start, while the average of (q/p)^S_tau still settles on 1', spec: { kind: 'walk',
      params: { steps: 80, p: 0.45, paths: 300, drawn: 25, height: 220, barriers: [-8, 8], overlays: ['sq', 'ratio'], sim: { seed: 11 } },
      state: { stopAtBarrier: true, showStopped: ['walk', 'ratio'], overlays: ['ratio'] },
      derive: { caption: 'S at the stop averages {{fixed(values.stopped, 2)}}; (q/p)^S at the stop averages {{fixed(values.stoppedRatio, 3)}}.' },
      controls: [{ bind: 'p', min: 0.3, max: 0.7, step: 0.05, label: '$p$' }] } },
    { name: 'walk (mean-reverting)', about: 'model "ou": X(n+1) = X(n) + theta (mu - X(n)) + sigma Z; theta, mu and sigma are sliders; the expected path, a 2 sd band and the level mu are dashed', spec: { kind: 'walk',
      params: { model: 'ou', steps: 60, theta: 0.15, mu: 2, sigma: 1, start: -3, paths: 12, xStep: 10, height: 280, y: [-6, 10], sim: { seed: 3 } },
      state: { showMean: true, showSpread: 2 },
      controls: [{ bind: 'theta', min: 0, max: 0.6, step: 0.05, label: '$\\theta$' }, { bind: 'mu', min: -3, max: 3, step: 0.5, label: '$\\mu$' }, { bind: 'sigma', min: 0.2, max: 2, step: 0.2, label: '$\\sigma$' }] } },
    { name: 'walk (custom overlay, fixed stop)', about: 'an expr overlay (the cubic martingale S^3 - 3nS) with a fixed stopping step stopAt; both stopped averages are shown', spec: { kind: 'walk',
      params: { steps: 40, p: 0.5, paths: 40, stopAt: 25, height: 220, overlays: [{ id: 'cube', expr: 'S^3 - 3 * n * S', label: '$S_n^3-3nS_n$', chip: 'S³ − 3nS' }], sim: { seed: 2 } },
      state: { showStopped: ['walk', 'cube'], stopAtBarrier: true } } },
```

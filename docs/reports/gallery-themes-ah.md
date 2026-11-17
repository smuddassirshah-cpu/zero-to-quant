# System gallery: theme and width survey (session AH)

Read, screenshot and report only. Nothing in the app was changed.

## What was surveyed

- Screen: `app/js/screens/system.js`, route `#system`. Theme is `data-theme` on `<html>`, set through `ZQ.setSetting('theme', 'light' | 'dark')` (`app/js/core.js:85`).
- Entries: **123 gallery cards** in each combination: 90 canvas cards (25 registered kinds, 65 variants) and 33 widget cards (17 kinds, 16 variants).
- Combinations: light and dark, each at 440 x 956 and 1376 x 900, deviceScaleFactor 1. That is 492 card shots, plus five shots of the token sections per combination.
- Every shot was read: all 123 cards in all four combinations on contact sheets, then suspects again at native size or 2x.
- Console errors: 0 in all four. Failed requests: 0. Raw `$...$` maths left unrendered: 0.
- The six code cards (Python and C++) were loaded and rendered in every run.

## How to rerun

From `app/`:

```
node tools/gallery-shots.mjs --out <dir> --local-cdn <pkgs> [--sheets] [--only dark-440] [--no-load-code]
```

- `<pkgs>` is the local CDN folder named in `docs/LEVEL-BRIEF.md`. Without `--local-cdn` the page uses the real jsDelivr and Google Fonts.
- Output: `<dir>/<theme>-<width>/NNN-<c|w>-<name>.png`, `<dir>/report.json`, `<dir>/summary.txt`. `--sheets` adds packed contact sheets in `<dir>/sheets/`. Do not commit the output.
- A full run takes about two and a half minutes. The script serves `app/` itself on a free port.

Notes on the run:

- jsDelivr and Google Fonts were not blocked or stubbed. They were served from the local copies with the routing copied from `playthrough.mjs`. Nothing hung on the network.
- One run stalled once in dark at 440, after the reload and before any shot, with no error. It did not recur in six later runs. The script now abandons a combination after five minutes and tries it once more.
- For the shots only, the script unsticks `.ds-bar` and `.shell-header` and hides `.tabbar`, since they sit over cards in element shots. It does not use mobile emulation, because that shifts element shots when the page is wider than the viewport.
- An SVG group's box ignores `clip-path`, so the `overflow ... g` lines for the transformed vectors cards (37, 79, 80) and the repeated intervals card (64) are not page overflow. Only the console card widens the page.
- Contrast is computed from HTML backgrounds and the SVG shape under a label. It does not see halos, so halo figures are a lower bound.

## Faults

Entry numbers are the card's position in the gallery, as in the file names. "All four" means both themes at both widths.

| # | Entry | Theme | Width | What is wrong | Source | Severity |
|---|---|---|---|---|---|---|
| 1 | 52 `console (pytest run)` | both | 440 (3 px at 1376) | The terminal is 487 px wide in a 364 px column. It runs off the card, the ends of four lines are cut (`[10`, `assert 0`), and the whole page scrolls sideways by 84 px. The console's own scroll never engages. | `css/screens/lesson.css:224` `.lsn-canvas` is a grid item of `.lsn-step` with `min-width: auto`, so it grows to the longest line; `css/canvases.css:355-356` (`overflow-x: auto`, lines `min-width: max-content`) then has nothing to scroll. The same rule applies in lessons. | broken |
| 2 | 8 `console` | both | all four | Warning card only: "No sample canvas for this kind". No drawing. | `js/screens/system.js:9-34` `CANVAS_SAMPLES` has no `console` key (a console variant exists only in `CANVAS_EXTRAS`, line 158). | broken |
| 3 | 104 `sliders` | both | all four | Warning card only: "No sample item for this kind". | `js/screens/system.js:47-79` `WIDGET_SAMPLES` has no `sliders` key. | broken |
| 4 | 107 `trade` | both | all four | Warning card only: "No sample item for this kind". | `js/screens/system.js:47-79` `WIDGET_SAMPLES` has no `trade` key. | broken |
| 5 | 17 `plane` | both | all four | The Riemann label "Sum ≈ 3.5" is drawn on top of the function label "f(x)" at the top right. Neither can be read. | `js/engine/canvas/plane.js:1034` places the sum at the top right corner (`px1 - 4`, `py1 + 12`) without checking the curve's end label. | poor |
| 6 | 36 `plane (contours and heat)` | dark worst, light too | all four | Axis tick labels sit on the heat map in a fixed muted grey. Measured 2.3:1 to 2.9:1 in dark on the mid blues, 2.6:1 to 4.4:1 in light. The halo is the page colour, so it does not help on the heat. | `css/canvases.css:486` `.cvb-tick { fill: var(--text-muted) }` and `:490` `.cvb-halo { stroke: var(--cv-bg) }`; neither knows about the heat layer. | poor |
| 7 | 88 `space (surface z = f(x, y))`, 89 `space (mesh, height and a sphere)` | both | all four | Tick labels that fall over the surface are grey on blue or gold, 1.1:1 to 1.5:1. The page-coloured halo makes a blot and swallows the minus sign ("−1" reads as a smudge and "1"). | `js/engine/canvas/space.js:511` (`cvb-t cvb-tick cvb-halo` drawn over the surface) with `css/canvases.css:486, 490`. | poor |
| 8 | 26 `pair (circle and sine)` | both | 1376 | Side by side in a 484 px card, each panel is 236 px wide for a 540 unit viewBox. Tick and angle labels render 6 to 7 px high and cannot be read. At 440 the pair stacks and is fine. | `css/canvases.css:30` `.cv-pair-row` two equal columns whenever the card is not stacked; the stacking rule keys on viewport, not on the card's width. | poor |
| 9 | 39 `tree (27 leaves, branching)` | both | 440 | The branch fractions render with digits about 5 px high. They are not readable. At 1376 they are small but legible. | `js/engine/canvas/tree.js` compact branch labels (`cv-fo` foreignObject, 540 unit viewBox scaled to 364 px); spec at `js/screens/system.js:123-125`. | poor |
| 10 | 55 `interleave (conditional steps)` | both | all four | The order badge sits on the end of the first line of the step text: "balance at" at 440, "at least" at 1376. | `css/interleave.css:14` (right padding 20 px, 18 px at `:70`) is narrower than the badge placed by `:63`. | poor |
| 11 | 15 `orderbook`, 66 `orderbook (quotes in the book)` | light | both | Best bid price is #1BAF7A on white, 2.8:1. Best ask is #E34948 on white, 4.0:1. Both are 14 px. Dark passes. | `css/canvases.css:464` `--cvb-bid`, `--cvb-ask`; used as text fill by `js/engine/canvas/orderbook.js:107` (`cvb-price cvb-c`). | poor |
| 12 | 63 `plane (steps, regions, polyline)` | dark | both | The selected option chip is white on #4D8BFF, 3.3:1 at 14 px. Light is 4.5:1. Any canvas with option controls shares this. | `css/screens/lesson.css:246` `.lsn-ctl-opt.is-on` with `--manip` from `css/tokens.css:161, 194`. | minor |
| 13 | 93, 116 to 120 (all `code` cards) | light | both | Keywords are #456DFF on the #F2F2F2 editor, 3.8:1 at 13 px. Dark passes. | `css/tokens.css:86` `--code-keyword`; `css/widgets.css:156`. | minor |
| 14 | 6 `circle`, 26 `pair (circle and sine)` | light | both | The sine readout is #EB6834 on white, 3.2:1. Dark is 4.3:1. | `css/tokens.css:109` `--s2` used as text colour by the circle canvas. | minor |
| 15 | 53 `interleave (deadlock)` | dark | both | Pending steps in a blocked lane are #8C8C8C on the amber wash, 2.8:1 to 3.7:1. | `css/interleave.css:14-16` (`color: var(--text-muted)`) over the blocked lane background. | minor |
| 16 | 102 `sketch` | both | all four | The five control points start on the x axis and cover the tick labels 80, 90, 100 and 110. | Sample at `js/screens/system.js:72-73` (y range starts at −4, points start at 0); the sketch widget draws handles over the plane's tick labels. | minor |
| 17 | 49 `payoff (spot drag)` | both | all four | The spot handle sits on the axis and covers the tick label 110. | `js/engine/canvas/payoff.js` spot handle on the x axis; sample `js/screens/system.js:152-153`. | minor |
| 18 | 67 `array (labels, ranges)` | both | 440 | Cell labels (i0 to i4) render about 6 px high. | `js/engine/canvas/array.js:129` (`size: 10` in a 540 unit viewBox). | minor |
| 19 | 28 `area (signed pieces)` | both | all four | The piece label "5x" is struck through by the diagonal. | Sample at `js/screens/system.js:93-95` (label at the centre of the piece the diagonal halves); `area.js` does not move a label off a diagonal. | minor |
| 20 | 64 `plane (repeated intervals)` | both | all four | Most intervals are wider than the plot, so they are clipped at the frame and read as full-width bars. The last tick is 104 on a 94 to 106 axis. | Sample at `js/screens/system.js:194-195` (`sigma: 10`, `size: 25` gives a half-width near 3.9 on a range of ±6); intervals drawn at `js/engine/canvas/plane.js:1295`. | minor |

Totals: 4 broken, 7 poor, 9 minor. 27 entries carry at least one fault.

## Checked and not a fault

- No entry draws a fixed dark stroke on the dark theme or a fixed light stroke on the light theme. Every canvas line, fill and label follows the theme. The white ring on drag handles (`.cvb-hd`) is fixed, but the handle has its own ink ring and reads in both themes.
- No entry has zero height or an empty drawing apart from the three warning cards. No card holds a visible `<canvas>` element; every drawing is SVG or HTML and has marks in every combination.
- Dimmed nodes in 61 `tree (binary, node values)` are 2.1:1 in light and 2.7:1 in dark. That is `state.dim` working as designed.
- C++ editors (117, 118) cut long lines at the editor edge; the textarea scrolls, so nothing is lost.
- 75 `complex-map (side by side)` is small at 440 by its own spec (`stack: false`).

## Clean in all four

The other 96 entries are clean in both themes at both widths:

1 to 5, 7, 9 to 14, 16, 18 to 25, 27, 29 to 35, 37, 38, 40 to 48, 50, 51, 54, 56 to 62, 65, 68 to 87, 90 to 92, 94 to 101, 103, 105, 106, 108 to 115, 121 to 123.

By name, the fully clean kinds are: area, array, balance, bars, boxes, complex-map, distribution, graph, grid, interleave (base sample), matrix, number-line, payoff (base sample), scatter, series, table, tree (base sample), vectors, venn, walk, and the widgets balance, choice, drag-point, expression, longform, manipulate, multi, numeric, order, place, slider, table and tap-regions.

## Fix pass

Rerun in all four combinations with `tools/gallery-shots.mjs`: 123 entries each, console errors 0, failed requests 0, page overflow none at 440 and 1376 in light and dark (the console card no longer widens the page). The screenshot of every changed entry was read in the combinations it affects. Contrast figures from the tool still list halo text (it ignores halos); on the changed tick labels the glyph is the ink colour on a page-colour halo.

| # | Entry | Result |
|---|---|---|
| 1 | 52 `console (pytest run)` | Fixed. `.lsn-canvas { min-width: 0 }` (`css/screens/lesson.css`); the terminal scrolls inside its own box at 440, lessons get the same fix. |
| 2 | 8 `console` | Fixed. Sample added to `CANVAS_SAMPLES` (`js/screens/system.js`). |
| 3 | 104 `sliders` | Fixed. Sample copied in shape from `odes/l6-second-order`; the label uses `y^{\prime}` because a bare `'` in a slider label is HTML-escaped before KaTeX and prints `&#39;` (slider label escaping is in `widgets/slider.js`, not touched, worth an engine item). |
| 4 | 107 `trade` | Fixed. Sample copied from `mm-games/l10-position-limits` over an `orderbook`. |
| 5 | 17 `plane` | Fixed. `placeLabels` in `plane.js` takes an opt-in `slide` flag (plane only): with no clear spot above or below, the label slides along the line before it would overlap. "Sum" and "f(x)" now sit apart. |
| 6 | 36 `plane (contours and heat)` | Fixed. `.cvb-tick.cvb-halo` and `.cvb-muted.cvb-halo` take `--ink` with a 3px page-colour halo (`css/canvases.css`). |
| 7 | 88, 89 `space` | Fixed with the same rule; the minus signs read in both themes. |
| 8 | 26 `pair (circle and sine)` | Fixed in the sample: `minScale: 0.6`, so the pair stacks at 1376 and the labels reach about 11 px. Content pairs that want the same set `minScale` themselves. |
| 9 | 39 `tree (27 leaves, branching)` | Left. 27 leaves in 364 px leave no room for larger branch labels without them colliding; a plain `1/3` renders as the same stacked fraction. Legible at 1376. |
| 10 | 55 `interleave (conditional steps)` | Fixed. Step right padding 28 px (26 px at 440) clears the order badge (`css/interleave.css`). |
| 11 | 15, 66 `orderbook` | Fixed. Light-only text tokens `--cvb-bid-t` #0B7D55 (5.2:1) and `--cvb-ask-t` #C73231 (5.3:1); bars and candles keep the old hues. |
| 12 | 63 `plane (steps ...)` | Fixed. The dark theme's selected chip takes `--ink-fixed` (6.5:1) in `lesson.css`. |
| 13 | 93, 116 to 120 `code` | Fixed. `--code-keyword` light is #3055EC (5.2:1 on the editor). |
| 14 | 6, 26 circle | Fixed. Sine readout is `--s2` mixed 66% with ink; darker in light, lighter in dark. |
| 15 | 53 `interleave (deadlock)` | Fixed. Steps, ids and results in a blocked lane use `--text-2`. |
| 16 | 102 `sketch` | Fixed in the sample (`xAxis: 'bottom'`): tick labels sit under the plot. The first handle still covers the `0` y tick at the left edge. |
| 17 | 49 `payoff (spot drag)` | Fixed in the sample: spot 105, off a tick. |
| 18 | 67 `array (labels, ranges)` | Fixed. Cell label size 12 (was 10) in `array.js`; about 8 px at 440. |
| 19 | 28 `area (signed pieces)` | Fixed in `area.js`: a piece cut by a diagonal moves its label a fifth of the cell off the line. Applies to any content using `diagonal`. |
| 20 | 64 `plane (repeated intervals)` | Fixed in the sample: `sigma: 5`, x range 92 to 108. |

Other checks: `node tools/validate.mjs` 0 errors; `node tools/test-engine-runtime.mjs` all passed; playthrough green with and without `--mobile` for `backtest/l1-one-bar-at-a-time`, `algo-think/l1-counting-work`, `alpha/l1-choosing-a-universe` (console canvas) and `algebra/l17-roots-and-factors`, `algebra/l4-cyclic-groups`, `analysis/l1-gaps-in-the-rationals` (plane). `docs/AUTHORING.md` was outside the edit list; the README notes (plane label slide, console scrolling, area diagonal labels) are in `js/engine/canvas/README.md` and `README-B.md`.

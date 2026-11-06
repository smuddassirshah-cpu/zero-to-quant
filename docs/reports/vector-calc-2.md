# vector-calc level 2: Green's theorem

Author report (content wave 3, session T). Brief: `docs/briefs/vector-calc.md`, `## Level 2`. Level 1 was written first in this session, so its shared numbers (the rotation field's $2\pi$, the vortex, the rule $\mathbf h = (0, S_1 - 100)$ and its £50) are reused as written.

## Files

| file | screens / items | quiz | notes |
|---|---|---|---|
| `l5-divergence-and-curl.json` | 12 screens | 4 | dye-and-wheel hook (`frames` control, text table), table of eight div/curl cells, `order` derivation of divergence as outflow per area, heat maps of div and curl, `space` curl of $(xy, yz, zx)$, Laplacian table, shear trap (Show why draws the wheel), source-field edge case, rates-drift transfer (table, then four phase pictures with a dragged trajectory) |
| `l6-green.json` | 12 screens | 4 | square table (0, 1, 1, 0), curl times area, `order` rectangle proof, $8\pi$, half disc $\tfrac23$ by polar and by a direct table, $e^{x^2}$ field, open semicircle, four-formula trap, annulus and vortex, code `circulation` + `curl_integral_polar` (`dblquad`), closed price loop £50 |
| `l7-area-from-a-boundary.json` | 12 screens | 4 | `multi` curl-1 fields, drag-point with an `expr` target (any $D$ giving area 12.5) and a live caption, ellipse $6\pi$ and $\pi ab$, `order` shoelace derivation, cross-term table, astroid, cardioid by polar area, vertex-order trap (Show why patches draw the crossing path and the bow tie), ring with a hole, market-maker triangle (£30) and orientation |
| `l8-flux-across-a-curve.json` | 12 screens | 4 | outward vs rotation (`frames`), flux $2\pi$, which normal (four arrows), `order` normal form from Green, square side table, $(x^2, y^2)$, $(x^3, y^3)$, work-instead-of-flux trap, source field's hole (two screens), probability-flux transfer ($-\pi$) and its sign |
| `review-2.json` | 8 items, `pass` 0.8 | | difficulty 2 to 4, every lesson |
| `homework-2.json` | 9 items | | difficulty 3 to 5 (two at 5): `order` (Green, $Q$ part), annulus $\tfrac{45\pi}{2}$, folium $\tfrac32$, ellipse flux $12\pi$, code `green_check` (5), code `shoelace`, `longform` source field (10-point rubric, full model), rates drift (parts), triangle |

## Gates

- Validator: 0 errors; no warning names a level 2 file.
- Voice scan (`VOICE_BASE=app/content/courses/vector-calc/`): 0 and 0.
- Numbers: `docs/reports/vector-calc-L2-numbers.py` exits 0, 182 of 182 checks, `lv.check_wrongs()` called. Every circulation, flux, divergence and curl is computed twice: by the theorem (Green, the normal form, shoelace or polar area, `dblquad` over the region) and by direct parametrised integration with `quad`; point values of div and curl also by central differences and by small-circle limits. The "check by hand" lines were read: each byKey line explains its slip without restating the wrong value.
- Playthrough with `--local-cdn`: all four lessons, review-2 and homework-2 pass at desktop and with `--mobile` (l5 and l8 replayed both ways after a last prose and arrow-spacing fix).
- SciPy load time: about 7 s (l6 played in 23 s against 18 to 19 s for the other lessons).

## Numbers (key values; every one in the script)

l5: (2, 0), (0, 2), (0, −1), (0, 0); $2xy - 2y$ and $1 - x^2$, at $(2, 1)$ 2 and −3; curl $(-2, -3, -1)$, divergence 6; Laplacians 4 and 0; drift divergence −1, curl 0.6, eigenvalues $-0.5 \pm 0.3i$. l6: square 0, 1, 1, 0, total 2; $8\pi \approx 25.13$; half disc $\tfrac23$ (arc $-\tfrac43 + 2$, diameter 0); $2\pi$; semicircle $\pi$; trap values $-\tfrac23$, 0, $\tfrac{10}{3}$; vortex $2\pi$ at radii 2 and $\tfrac12$; price loop legs 0, 50, 0, 0. l7: quadrilateral 12.5 (cross terms 0, 12, 13, 0); ellipse $6\pi \approx 18.85$; astroid $\tfrac{3\pi}{8} \approx 1.178$; cardioid $\tfrac{3\pi}{2} \approx 4.712$; crossing listing 2, bow tie 0, clockwise −12.5; ring 12 (20, 16, 32 for the slips); triangle cash −2,000, 1,015, 1,015, total £30; rectangle £50. l8: $2\pi$ and 0; square 1, 1, 0, 0; $(x^2, y^2)$ 2; $\tfrac{3\pi}{2}$; source $2\pi$ for radii 1, 2, 5, 0 at $(3, 0)$; drift flux $-\pi$. Review: 5, −2, $\tfrac{3\pi}{2}$, 15, 3, −2, $4\pi$, 6, $2\pi$. Homework: $\tfrac{45\pi}{2} \approx 70.69$, $\tfrac32$, $12\pi$, green_check values $\tfrac{45\pi}{2}$, $8\pi$, 0, $6\pi$; 50-gon $25\sin\tfrac{2\pi}{50} \approx 3.1333$; drift $-4\pi$ and $2.4\pi$; triangle 2.

## Departures from the brief

- l5: the hook asks about three fields (rotation, uniform, outward), not four: the shear's spin is the trap, so it is not asked before the trap. The space screen asks for the curl only; the divergence 6 is in its explanation and is quiz q1. The transfer's "which picture" uses one canvas with a `frames` control over four drift fields and a dragged trajectory, not four canvases.
- l6: the "why does it extend to a region cut into rectangles" `choice` and the "why £50" `choice` moved to the quiz (q1, q2) under the 12-screen cap.
- l7: the market-maker transfer gives the triangle's legs in a `table` with the total (£30) as its last cell, and the rectangle's £50 in the explanation and quiz q4 (£40 for a £20.00 to £20.40 loop).
- Homework `green_check` takes the annulus radii `(P, Q, curl, r1, r2)` (a disc when `r1 = 0`) instead of a general parametrised boundary and region; the brief's tests (the annulus) still apply, plus a disc, the vortex annulus and the rotation field.
- Brief errors: none found; every planner number reproduced.

## Proposed course.json change

None.

## Backlog

No new bullet for level 2: every canvas need was met (field layers, `trajectory`, `frames`, `heat`, polar `area`, `polygons` with a dragged vertex and a `derive` caption, `drag-point` with an `expr` target).

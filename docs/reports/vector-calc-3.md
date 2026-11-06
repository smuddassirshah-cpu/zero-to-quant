# vector-calc level 3: Surfaces and space

Author report (content wave 3, session T). Brief: `docs/briefs/vector-calc.md`, `## Level 3`. Levels 1 and 2 were read first (reports, "Departures", l5, l6, l8): notation ($\mathbf F$ a field, $\oint$ counterclockwise, $\mathbf n$ outward, curl as $Q_x - P_y$ and in space by components), the rotation field's $2\pi$, the source field's hole, the holdings rule $\mathbf h = (0, S_1 - 100)$ and its £50, and the SciPy screen pattern (`dblquad` inner-first docstring, `pass` stubs, `isclose` with absolute 1e-6).

## Files

| file | screens / items | quiz | notes |
|---|---|---|---|
| `l9-parametric-surfaces.json` | 12 | 5 | `pair` hook (plane domain with a marked cell beside a `space` cylinder; `tap-regions` among four small patch `surfaces`), stretch factor 2, $\mathbf r_\theta$ with a $\theta$ slider, cross product $(-2, -3, 1)$ with its `planes` `extent` parallelogram, right-hand rule, `order` area element (distractor $\lvert\mathbf r_u\rvert\lvert\mathbf r_v\rvert$), cylinder $12\pi$, plane $\sqrt{14}$, sphere $4\pi$, trap $2\pi^2$ (wrong entries for the dot-product slip 0 and the true area), poles and double cover, portfolio triangle $\tfrac{\sqrt3}{2}$ |
| `l10-surface-integrals.json` | 11 | 3 | rain on a tilting roof (slider `a`, live area caption), naming flux, $\iint z\,dS = \pi$, $2\pi$ hemisphere, $\tfrac{2\pi}{3}$, paraboloid $\tfrac{3\pi}{2}$, Möbius strip with a slider carrying the normal round, parameter-order trap (Show why flips three normal arrows), tangent rotation field 0, code `flux`, random stress $\tfrac13$ |
| `l11-divergence-theorem.json` | 12 | 3 | six-face table (1, 0, 1, 0, 1, 0, total 3), sphere $4\pi$ naming the theorem with its hypotheses, `order` box proof (R part, bottom-sign distractor), $(xy, yz, zx)$ table $\tfrac32$ both ways, $\tfrac{12\pi}{5}$, cylinder $60\pi$, paraboloid closed by a disc $\tfrac{3\pi}{2}$, forgotten-faces trap ($24\pi$ wrong entry, Show why reveals the lids), inverse-square $4\pi$, code `box_flux` + `div_integral`, drift $-2\pi$, heat-equation `order` |
| `l12-stokes.json` | 12 | 4 | rotation field on disc and hemisphere (predict, then $2\pi$), Stokes named with hypotheses and the right-hand rule, curl of $(z, x, y)$ as $\nabla \times \mathbf F$, `order` surface independence, circle $\pi$, triangle edges table $\tfrac12$ each, triangle by Stokes $\tfrac32$, paraboloid swap $2\pi$, orientation trap $-\pi$, closed sphere 0, three-price loop table £0, £50, £0, £0 |
| `review-3.json` | 9 items, `pass` 0.8 | | difficulty 2 to 4, all four lessons |
| `homework-3.json` | 8 items | | difficulty 3 to 5 (two at 5): `order` (box, P part), plane triangle $4\sqrt6$ (parts), Stokes $(y, z, x)$ curl and $-\pi$ (parts), triangle flux $\tfrac12$, half ball $\tfrac{\pi}{2}$, code `sphere_flux` + `ball_divergence` (5), `longform` cylinder (10-point rubric, full model), inward triangle $-\tfrac32$ |

## Gates

- Validator: 0 errors; no warning names a level 3 file (from `app/`, `node tools/validate.mjs`).
- Voice scan (`VOICE_BASE=app/content/courses/vector-calc/`): 0 and 0 (no sentence over 20 words, no explanation over three sentences).
- Numbers: `docs/reports/vector-calc-L3-numbers.py` exits 0, 183 of 183 checks, `lv.check_wrongs()` called. Every surface integral, flux, divergence-theorem and Stokes value is computed twice: by the theorem or closed form (triple integral of the divergence with `tplquad`, flux of the curl, graph formula) and directly by parametrised `dblquad` with numerical $\mathbf r_u \times \mathbf r_v$, or `quad` round the boundary. The code screens' solutions are run against their own tests and the starters fail every test. The "check by hand" lines were read: each byKey line names its slip without restating a different number.
- Playthrough with `--local-cdn`: all four lessons, review-3 and homework-3 pass at desktop; and with `--mobile` (440 px): all passed, no console errors.
- SciPy load time: about 7 s, as in level 2 (l10 and l11 played in 22 to 24 s against 17 to 19 s for l9 and l12).

## Numbers (key values; every one in the script)

l9: $(-2, -3, 1)$, $\sqrt{14} \approx 3.742$, stretch 2 (0.6 to 1.2, 0.3 to 0.6), $\mathbf r_\theta = (-2, 0, 0)$, $12\pi \approx 37.70$ (slips $6\pi$, $20\pi$), $4\pi$, $2\pi^2 \approx 19.74$, $8\pi$ for the double cover, $\tfrac{\sqrt3}{2} \approx 0.866$; quiz $\tfrac{\pi}{6}(5\sqrt5 - 1) \approx 5.330$, $\sqrt2\pi \approx 4.443$, density $\tfrac{2}{\sqrt3}$. l10: roof $-1$ at every tilt, area $\sqrt2$; $\pi$, mean height $\tfrac12$ (half ball $\tfrac38$); $2\pi$ and $4\pi$; $\tfrac{2\pi}{3} \approx 2.094$; $\tfrac{3\pi}{2} \approx 4.712$ (sign slip $-\tfrac{\pi}{2}$); $-4\pi$; $\iint |z|\,dS = 2\pi$ against $\tfrac{4\pi}{3}$; tangent field 0 (area $6\pi$); $\tfrac{4\pi}{3}$ and $\tfrac13$; constant field 0 (top half $\pi$). l11: faces 1, 0, 1, 0, 1, 0 and 3; $\tfrac12, 0, \tfrac12, 0, \tfrac12, 0$ and $\tfrac32$; $\tfrac{12\pi}{5} \approx 7.540$ (slips $\tfrac{4\pi}{5}$, $2\pi^2$); $60\pi \approx 188.5$ = side $24\pi$ + top $36\pi$ + bottom 0; cap volume $\tfrac{\pi}{2}$, flux $\tfrac{3\pi}{2}$; $4\pi$ at radius 1 and 2; box 36 (faces 12, 6, 18); drift $-2\pi \approx -6.283$; quiz 2. l12: $2\pi$ on circle, disc and hemisphere; curl $(1, 1, 1)$; circle $\pi$; edges $\tfrac12$ each, $\tfrac32$; Stokes on the triangle $\tfrac32$; paraboloid $2\pi$; clockwise $-\pi$; sphere 0 (halves $\pm 2\pi$); loop £0, £50, £0, £0, total £50; quiz $4\pi \approx 12.566$. Review: $(1, -2, 2)$, 6, $4\pi$, 24, $5\pi$, $32\pi$, $-2\pi$, cube $4\pi$. Homework: $(8, 16, 8)$, $4\sqrt6 \approx 9.798$, $(-1, -1, -1)$, $-\pi$, $\tfrac12$, $\tfrac{\pi}{2}$, $4\pi$, $\tfrac{12\pi}{5}$, $\tfrac{384\pi}{5} \approx 241.27$, $60\pi$, $-\tfrac32$.

## Departures from the brief

- The 12-screen cap moved these l9 tasks to its quiz: paraboloid area (q1), cone area (q2), pick the parametrisation (q3), the Jacobian link (q4) and the density $\tfrac{2}{\sqrt3}$ (q5). The "both dot products are 0" check sits in the cross-product hint, feedback and explanation, not a separate widget.
- l10: the mean height $\tfrac12$ is quiz q1 and the symmetry `choice` is quiz q2. The trap's second distractor uses $\iint |\mathbf F|\,|\mathbf r_\theta \times \mathbf r_\phi|$ (equal to $4\pi$ here but $2\pi$ against $\tfrac{4\pi}{3}$ for $(0, 0, z)$), a number-preserving way to name "the scalar area element in a flux". The Möbius screen got a slider that carries the normal once round.
- l11: the cylinder is one `expression` ($60\pi$) by the theorem, then the trap screen asks the face-by-face total (188.5, with $24\pi$ and $36\pi$ as wrong entries); the brief's separate cylinder `table` is folded into that. The open-surface `choice` and Gauss at radius 2 are quiz q2 and q1.
- l12: the disc flux $\pi$ is in the circle screen's feedback and explanation; the Green-flat-case `choice`, the "why $z^2e^x$ drops out" `choice` and the general P&L rule `choice` are quiz q1 to q3. The four "orientation pictures" became one hemisphere with its normal and four described directions.
- Homework longform asks for the colleague's $24\pi$ error and both routes to $60\pi$ as the brief says; the `order` item is the divergence theorem's $P$ part (the lesson did the $R$ part).
- Scratchpad: the brief names another session's folder; this session used its own `vector-calc-3` subfolder and its own `pkgs`.
- Brief errors: none found; every planner number reproduced.

## Proposed course.json change

None.

## Backlog

One bullet under "Raised later (vector-calc level 3)": a direction marker on `space` curves (Stokes orientation), worked round with a tangent vector at one point.

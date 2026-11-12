# Problem sets: complex, levels 1 to 3 (brief `docs/briefs/chained.md`)

Files: `app/content/courses/complex/problems-1.json`, `problems-2.json`, `problems-3.json`, 4 problems and 20 parts each. Numbers: `docs/reports/problems-complex-numbers.py` (exit 0, 963 checks, 0 failures). Commits: 1e7162b (level 1), 29d4766 (level 2), af55f01 (level 3), then one commit with this report and the inbox bullets.

Read first: the screens and quizzes of l1 to l13, review-1 to 3, homework-1 to 3, both fluency sets and exam `topic-1.11`. The course's own settings are AR(2) spreads, a coin's and a trade's characteristic function, daily volume DFTs, a bond's duration, Poisson fills, the standard Cauchy as a daily move, Black-Scholes and Merton pricing. None is used. The sets use a parallel circuit, an animation, lamps on a plan, a three-phase cable, a mesh generator, a heated plate, a traffic island, a lighthouse, a share's moments and a print job. `l13-fourier-pricing` screens[10] (Merton drift, disputed sign) is not touched: no part uses Merton or a drift correction.

## Sets

| set | item | parts (numeric / expression / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-parallel-branches | 5 (3 / 2 / 0) | l1, l2 | 3 |
| problems-1 | p-turning-frames | 5 (3 / 2 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-four-lamps | 5 (2 / 3 / 0) | l1, l2, l4 | 5 |
| problems-1 | p-neutral-wire | 5 (3 / 2 / 0) | l2, l3, l4 | 4 |
| problems-2 | p-mesh-map | 5 (3 / 2 / 0) | l5, l6 | 4 |
| problems-2 | p-plate-heat | 5 (2 / 3 / 0) | l6, l7 | 5 |
| problems-2 | p-log-branches | 5 (3 / 2 / 0) | l5, l6, l8 | 4 |
| problems-2 | p-modulus-plus-z | 5 (0 / 4 / 1) | l6, l7 | 3 |
| problems-3 | p-traffic-island | 5 (2 / 2 / 1) | l9, l10 | 4 |
| problems-3 | p-lighthouse-flashes | 5 (3 / 2 / 0) | l11, l12 (l10) | 5 |
| problems-3 | p-share-moments | 5 (5 / 0 / 0) | l12, l13 | 4 |
| problems-3 | p-print-stages | 5 (3 / 2 / 0) | l10, l11, l12 | 4 |

Typed parts: level 1 20 of 20, level 2 19 of 20, level 3 19 of 20. The two choice parts are judgements: where $|z|^2 + z$ is differentiable and analytic, and why $\oint z^2\,dz = 0$ round the island.

Chains. Level 1: $Z_1Z_2 = 23 + 14i$, $Z = 4.15 + 0.95i$, $|Z| = 4.257$, current 2.819 A, lag $12.9^\circ$; $w = \tfrac32 + \tfrac{\sqrt3}{2}i$ from $z^2 - 3z + 3 = 0$, $|w| = 1.732$, $\operatorname{Arg} w = \tfrac{\pi}{6}$, $w^6 = -27$, first positive power 729; $|c| = 81$, $\operatorname{Arg} c = \tfrac{2\pi}{3}$, lamp $\tfrac{3\sqrt3}{2} + \tfrac32 i$, the fourth-quadrant lamp by $-i$, spacing $3\sqrt2 = 4.243$ m; phasor $q = 6\sqrt3 = 10.392$, $-\tfrac72 - \tfrac{7\sqrt3}{2}i$, $N = \tfrac52 + \tfrac{5\sqrt3}{2}i$, $|N| = 5$, lead $60^\circ$ (with $1 + \omega + \omega^2 = 0$, $N = -5\omega^2$). Level 2: $f(2.5 + 3i) = -12.75 + 3i$, $f' = 1 + 6i$, stretch $\sqrt{37} = 6.083$, turn $80.5^\circ$, area 0.0037; $v = y^2 - x^2 + 3y$, $f = 3z - iz^2$, $f'(1 + i) = 5 - 2i$, $u_y = 2$, gradient $\sqrt{29} = 5.385$; $|w| = 8$, $\operatorname{Arg} w = \tfrac{5\pi}{6}$, $z = \ln 8 - \tfrac{7\pi}{6}i$, Log stretch 0.125, $|w^i| = e^{-5\pi/6} = 0.0729$; $u = x^2 + y^2 + x$, $2x$, $2y$, quotient $1 - 0.01i$, differentiable only at 0. Level 3: integrand $9t + 2t^3 + 3it^2$, $5 + i$ along the curve, 5 along the edge, $\oint z^2\,dz = 0$, area 0.5; pole $1 + 3i$, residue $-\tfrac{i}{6}$, $c = 3/\pi = 0.955$, $|\varphi(1)| = e^{-3} = 0.0498$, the mean of two flashes again 0.0498; drift 0.015, $E[S_T] = £66.61$, $E[S_T^2] = 4665$, sd £15.08, $\psi(0) = 2241$; $\varphi_X = (1 - 2iu)^{-2}$, pole $-\tfrac{i}{2}$, $\oint \varphi_X/z^2 = -8\pi = -25.13$, $E[X] = 4$, $\operatorname{Var} X = 8$. Each later part restates the value it uses; where a slip carries, its `wrong` list holds the carried value (`carried-*`, 15 parts).

Judgement calls a reader may question:
- Several settings are not quant (circuit, animation, lamps, plate, island, lighthouse, print job). The brief asks only for freshness; the course's quant settings are all taken by its lessons.
- `p-neutral-wire` part 1 asks for $q$ as a decimal, not $-6 + 6\sqrt3 i$: `form: "rectangular"` refuses that key (inbox).
- `p-plate-heat` part 2 takes an answer in $z$; the grader samples $z$ as a real symbol, which still separates every listed slip (the script checks each).
- `p-traffic-island` part 5 gives $\oint \bar z\,dz = 2iA$ in the question (not taught); the explain checks the area by $\int_0^3 (\tfrac{x}{3} - \tfrac{x^2}{9})\,dx$.
- `p-lighthouse-flashes` is l11's "Cauchy characteristic function by residues" task (the same standard task, allowed by the reuse ruling) with its own location 1, scale 3 and setting; the last part is new (the mean of two flashes).
- `p-share-moments` part 5 gives the Carr-Madan $\psi$ with $\alpha = 1$; the script checks $\psi(0) = \int C(K)\,dK$ against Black-Scholes call prices integrated over strikes.
- `p-print-stages` parts 3 and 5 state the contour value or formula they use; the derivative form of Cauchy's formula is l10's.

Form. Every non-whole numeric part names its form. Exact angles use `form: "exact-angle"`, complex answers `form: "rectangular"`. Money parts carry `unit: "£"`. Negative keys ($-27$, $-25.13$) have a `sign` wrong at the absolute value; the drift key 0.015 has `sign` at $-0.015$.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (963 checks in all, exit 0) |
| validator | 0 errors; no warning on the file (total 4,522, as before) | same | same |
| grade-all `--local-cdn` | 0 failures (20 widgets) | 0 failures (20) | 0 failures (20) |
| playthrough `--local-cdn --why` | green, 55 slips routed | green, 49 slips routed | green |
| playthrough `--mobile` | green; 440 px shots read | green; shots read | green; shots read |
| voice scan 35 (`VOICE_BASE` the course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

The numbers script: route 1 is exact sympy (solve, arg, residue, symbolic integrals and derivatives, exact powers); route 2 is floating point by another method (Python complex and cmath, `numpy.roots`, `scipy.integrate.quad` including Fourier-weighted quadrature for the Cauchy characteristic function, the trapezium rule round contours, central differences for derivatives and Cauchy-Riemann partials, a line integral for the harmonic conjugate, Black-Scholes prices integrated over strikes, and Monte Carlo for the mean of two Cauchy flashes and the variance of two stages). It checks every key against both routes, every `wrong` value and form against its rebuilt slip, bands apart, byKey lines present, the key printed in `correct` and `explain`, and `vocab` (every printed number given or computed). It runs `numbers_lib` `Level`, `expect`, `check_wrongs` and `report`. Three slips were wrong in drafts and caught by the script or by hand before commit: $|w^i|$ first keyed 0.0730 (it is 0.0729), `no-chain` $3 - i$ (it is $4 - i$), and the `degrees` slip 10.411 (it is 0.439).

## Fresh-check and reuse

`fresh-check.mjs --file <set> --cross-numbers`: 0 hits on all three sets. Advisories: problems-1 none (a first draft of `p-four-lamps` with $c = -8 + 8\sqrt3 i$ shared 64, 192 and 256 with `trig/problems-1` item 2, a hexagon of side $8\sqrt3$; changed to $c = -\tfrac{81}{2} + \tfrac{81\sqrt3}{2}i$). problems-2 none (a draft at $z_0 = 3 + 2i$ shared $3 + 2i$ with l1 and $63.4^\circ$ with l5; then $2.5 + 3i$ drew two 3-number advisories on derived values, 6.25 and 36, which were taken out of the text). problems-3: eight advisories, all `p-share-moments` against unrelated Black-Scholes or rate items on 0.015, 0.03, 0.04, 0.03125, 0.13: chance, the arithmetic of $r = 5\%$, $\sigma = 25\%$ (a first version at 4% and 30% drew seven). A first `p-traffic-island` was a flower bed, the setting of `number-sense/problems-1`; renamed.

Own grep (`fresh.py` in the scratchpad; the course folder first, then all of `app/content/`, other problem sets of this course left out):

| problem | key numbers and nouns searched | course folder | all content |
|---|---|---|---|
| p-parallel-branches | 2 + 5i, 4 - 3i, 23 + 14i, 6 + 2i, 4.15, 18.125, 4.257, 2.819, 12.9, impedance | no hit | 4.15, 4.257, 2.819, 12.9 alone in unrelated lessons (arma, alpha); no pair |
| p-turning-frames | 3z + 3, 3/2 + sqrt3/2 i, -27, 729, 531441, animation | 729 only inside a float in an l2 test | single numbers only |
| p-four-lamps | 81/2, 6561, 4.243, 3 sqrt2, 110.648, 57.276, lamp | no hit | 4.243 a slip in `eigen/problems-4`; single numbers |
| p-neutral-wire | 12e^{2..}, 7e^{4..}, 10.392, 16.643, phasor, three-phase | no hit | 10.392 in two option lessons; single |
| p-mesh-map | z^2 - 4z, 2.5 + 3i, -12.75 + 3i, 1 + 6i, 6.083, 80.5, sqrt{37} | no hit | single numbers; `z^2 - 4z` is an eigenvalue polynomial in `linear-maps/l15` and `stage-1` |
| p-plate-heat | 2xy + 3x, y^2 - x^2 + 3y, 3z - iz^2, 5 - 2i, 5.385, sqrt{29}, plate | no hit | 5.385 and sqrt{29} in `trig/problems-3`, `taylor/l9` alone |
| p-log-branches | 4 sqrt3 + 4i, ln 8, 7pi/6, 0.0729, 13.708 | `\ln 8` in l8 (Log(-8) = ln 8 + i pi) | single numbers; the exam's $-2\sqrt3 - 2i$ was avoided on purpose |
| p-modulus-plus-z | abs(z)^2 + z, x^2 + y^2 + x, 1 - 0.01i | no hit | `x^2 + y^2 + x` once in `vector-calc/homework-1` |
| p-traffic-island | 3t + it^2, 3 + 2it, 9t + 2t^3, 5 + i, (3 + i)s | no hit | `5 + i` in two drills (code text) |
| p-lighthouse-flashes | x^2 - 2x + 10, 1 + 3i, 0.955, 0.0498, e^{-3 + i}, lighthouse | `1 + 3i` as a product in l5 | lighthouse in `trig/l5` (bearings); single numbers |
| p-share-moments | £64, 0.03125, 66.61, 4664.6, 4665, 15.08, 2241 | no hit | single numbers (see advisories) |
| p-print-stages | 1 - 2iu, -25.13, -8 pi, -24 pi i, print job | no hit | single numbers |

Judgement: no problem shares a setting, a story, a sentence or a set of numbers with a lesson, quiz, review, homework, exam, drill, bank item or other set; the remaining hits are lone common values.

## Engine limits

Four bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems complex)": rectangular form refusing $6\sqrt3 i$; exact-angle refusing a plain `pi`; `numbers_lib._numbers` joining tokens across nested-brace fractions; `--cross-numbers` advisories on Black-Scholes decimals. None blocked a problem.

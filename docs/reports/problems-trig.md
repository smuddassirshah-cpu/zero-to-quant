# Problem sets: trig (brief `docs/briefs/chained.md`)

Files: `app/content/courses/trig/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-trig-numbers.py` (exits 0, 1016 checks, 0 failures). Engine graders: `docs/reports/problems-trig-grade.mjs --local-cdn <pkgs>` (exits 0, 886 checks, 0 failures).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-zip-wire | 4 (4 / 0) | l1, l2, l3 | 3 |
| problems-1 | p-hexagon-tile | 4 (4 / 0) | l1, l2, l4 | 4 |
| problems-1 | p-lake-markers | 4 (3 / 1) | l3, l5 | 4 |
| problems-1 | p-desk-lamp | 5 (5 / 0) | l1, l3, l4 | 5 |
| problems-2 | p-water-wheel | 5 (5 / 0) | l6, l7 | 4 |
| problems-2 | p-two-buoys | 4 (4 / 0) | l8, l9 (and l6 for the sign) | 3 |
| problems-2 | p-observation-wheel | 5 (5 / 0) | l6, l7, l8, l9 | 5 |
| problems-3 | p-two-angles | 5 (5 / 0) | l10, l11, l12 | 4 |
| problems-3 | p-quadratic-in-sine | 4 (4 / 0) | l10, l11 (and l7 radians) | 5 |
| problems-3 | p-daylight-model | 5 (5 / 0) | l11, l13 (and l9) | 4 |
| problems-3 | p-garden-bed | 4 (4 / 0) | l10, l11, l12 (and l5) | 4 |

11 problems, 49 parts. Typed parts: level 1 16 of 17, level 2 14 of 14, level 3 18 of 18. The one choice part (lake markers, part 1) is a judgement: which rule fits two sides and the angle between them. Every lesson of each level appears in at least one problem, and every problem draws on at least two lessons of its level. Earlier-level ideas used: the cosine rule (l5) in the garden bed, radians (l7) in the quadratic.

Chains. Level 1: wire length, its sine, a rider's drop, the rider's level distance; triangle height, the short diagonal, $AC^2 + CD^2$, then the angle at A; which rule, AB, angle A by the sine rule, then the shortest path from P; elbow height exactly, OB, angle AOB, bulb height to 1 dp, then the same height exactly as a check. Level 2: angle from arc, to degrees, tip height, the mirror angle at the same height, then the arc to it; period, first peak, the lagged buoy's peak, then the gap between the buoys; amplitude, $b$, $c$, height at 8 minutes, then the other time at that height. Level 3: $\cos A$, $\sin B$, $\sin(A+B)$, $\cos(A+B)$, then $A + B$ from both signs; the quadratic in $s$, its roots, $x$ in degrees, the largest root in radians; $a$, $b$, $c$, the two crossing times, then the two times with 9.8 hours and the months above 9.8 hours; area as $65\sin C$, both angles for 25 m$^2$, $\cos C$ for the obtuse one, then its third edge. Every later part restates the value it uses. No dead end: each part's result is used later, or it is the last part.

Settings are everyday and short (a zip wire, a floor tile, a lake survey, a desk lamp, a water wheel, buoys, an observation wheel, daylight hours, a garden bed); `p-two-angles` and `p-quadratic-in-sine` are plain maths settings. Calculator values are given where level 1 needs a cosine or sine of a non-special angle, as the lessons do.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures (1016 checks for the three sets) | same | same |
| engine grade check | 0 failures (886 checks for the three sets) | same | same |
| validator | 0 errors, no warning on the file (total 4145 before and after) | same | same |
| playthrough `--local-cdn` | green (17 parts) | green (14 parts) | green (18 parts) |
| playthrough `--mobile` | green; 440 px shots read, no layout fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |
| `fresh-check --file` gate | 0 hits | 0 hits | 0 hits |

Census: "Problem sets 59 (items 225)".

The numbers script works each answer twice: exactly (sympy surds, fractions, `solveset` on the interval) and by a second route (coordinates of the points with a distance, an atan2 or a cross product; a complex number for the wheel tip; the physical wheel $28 - 25\cos$ against the fitted sine; grid scans for peaks and the time above a level; bisection; brute force over whole degrees). It rebuilds every `wrong` value from its named slip, and checks the key inside its band, the value at the asked rounding and any carried rounded value accepted (for example 6.48 from $20 \times 0.324$, 50.28 and 50.27, 47.1 and 47.2, 19.62 and 19.64, 4.8672 from 0.778), the figure printed in `feedback.correct` accepted, wrong bands off the key and off each other, a byKey line per wrong, three sentences at most per explanation, and a stated form in every numeric question. The grade script runs the real `grade.js` with the Compute Engine on every part: keys, accept lines and wrong forms, numeric and expression sets (order, `x =` labels, count), `form: "exact-angle"` (refuses `150^\circ` and $\tfrac{150\pi}{180}$), equations up to a multiple, and each typed slip routed to its own key.

Slips covered where the level makes them real: degrees against radians (radian-mode inverse at level 1; $\sin 2.25^\circ$, $\sin 128.9$ in radians, $\sin(1.1\pi)$ and $\sin(0.3\pi)$ in degree mode at level 2; 150 for $\tfrac{5\pi}{6}$ at level 3), the quadrant sign (level 3, three parts), the mirror rules mixed up (cosine's $360 - x$ and tangent's $x + 180$ for sine), the half left out of the area, $1 - \sin$ for $\sqrt{1 - \sin^2}$, and the commonest slip of the part before (tangent carried into the zip wire's drop, the undistributed bracket's roots 1 and 2, the no-half area's angles).

Known keyed coincidence, checked: in `p-two-angles` part 3 the sign slip on $\cos A$ and a minus in the formula give the same wrong value, 0.7449; one byKey line names both. No slip reaches a key: the two found cosines and sines sit in different products of $\sin(A+B)$, so flipping both signs gives $-0.2047$, not the key.

## Fresh-check hits and judgement

Gate (default): 0 hits on all three files. Loosened (`--min-run 8 --min-share 0`): stock phrasing only, "give your answer in metres to # decimal places" (between my own sets), "type the whole equation with its # sign" (equations problems-2), "with # in months and the angle in radians" (l11 transfer screen). No story or numbers reused.

My own reading against the course's lessons, quizzes, reviews, homework, fluency families and the 0.3 exam: no zip wire, hexagon, lake, lamp, water wheel, buoy, observation wheel, daylight or garden bed anywhere. Close shapes, judged acceptable: the cosine rule from two sides and an included angle (l5, the exam's two roads) is the rule itself; the garden bed avoids `review-3`'s 6 cm and 9 cm at $150^\circ$ (sides 10 and 13, $\sin C = \tfrac{5}{13}$, two beds; fix pass of 0.3 c, since l10 and the Stage 0 exam use 0.6 and 0.8); the daylight model asks the l13 transfer's last question shape (months above a level) with a new story and numbers; `p-two-angles` uses 28, 45, 53 and 7, 24, 25 (fix pass of 0.3 c; the exam's `e-tan-third-quadrant` has 8, 15, 17) where `homework-3` uses 3, 4, 5 and 5, 12, 13; the quadratic needs the identity first, which none of l11's, `review-3`'s or `homework-3`'s quadratics do.

## Engine limits (to `docs/BACKLOG-INBOX.md`)

Two bullets under "Raised later (problems trig)": the numeric field refuses a trailing degree sign, and the Accepted line's raw LaTeX met again.

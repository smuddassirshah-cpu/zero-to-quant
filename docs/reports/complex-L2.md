# Report: complex level 2 (Complex functions)

Level 1 was written first in this worktree (commit "complex L1"), so l5 to l8 build on its notation and numbers: $3 + 4i$, $1 + i$ as a 45-degree turn with stretch $\sqrt2$, and the course AR(2) convention.

## Files written

All in `app/content/courses/complex/`, generated from scripts kept in the scratchpad folder `complex-L2`.

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l5-functions-move-the-plane.json` | 10 screens, 4 quiz | `map_points` (50-point parabola test) and `square_roots` | cz-functions |
| `l6-complex-differentiability.json` | 10 screens, 4 quiz | `quotients` and `spread`; `complex_step` and `central_diff` (bond test, an `abs` case that returns 0) | cz-functions |
| `l7-cauchy-riemann.json` | 10 screens, 4 quiz | `cr_residuals` and `analytic_near` | cz-functions |
| `l8-exp-and-log.json` | 10 screens, 4 quiz | `principal_log` (starter has the `atan(b/a)` trap); `continuous_log` | cz-functions, cz-polar |
| `review-2.json` | 9 items, difficulty 2 to 4 | | cz-functions, cz-polar |
| `homework-2.json` | 9 items, difficulty 3 to 5 | `cs_delta` and `cs_vega` through SciPy's complex `erf` (4), `newton_root` (5) | cz-functions, cz-polar |

Homework also has expression items ($1/(1 + 2i)$, a harmonic conjugate, $\operatorname{Log}(-e)$), two numeric items (the amplitwist of $z^3$, $(-1)^i$), an `order` proof that $\bar z$ has no derivative (two distractor lines) and the Monte Carlo complex-step `longform` (10-point rubric, one required row). The level's objectives start "Picture", "Test", "Use" and "Work", so the verb rule does not match and no performance task is added.

Canvases: `complex-map` throughout (z², slide and turn frames, the line $a + it$ on a slider, the unit-square sides, $1/z$ with the circle $|z - 1| = 1$, the CF map of the real line, difference-quotient dials, the zoomed amplitwist square with a size slider, $z^2 + z$, $e^z$ and $\operatorname{Log}$ with its cut); `plane` contour families of $u$ and $v$ with a frames switch between $z^2$ and $\bar z$; `table` and `console`.

Traps: $1/z$ taken as $\bar z$ (l5); $\operatorname{Re} z$ called differentiable because it is smooth (l6); checking one Cauchy-Riemann equation, with the sign-slip distractor that would reject $z^2$ (l7); $\operatorname{Log}(zw) = \operatorname{Log} z + \operatorname{Log} w$ (l8). Edge cases: the pole of $1/z$ and the single preimage of 0 (l5 quiz); $|z|^2$ differentiable only at 0 (l6 quiz); $x^2 + iy^2$ differentiable on $y = x$ and analytic nowhere (l7 quiz and code); $\operatorname{Log} 0$ and Python's `(-8) ** (1/3)` (l8 code and quiz).

## Gates (SESSION PROTOCOL 4)

1. Validator: 0 errors. Level 2 files carry 7 warnings, all "a ladder screen usually reuses the previous canvas kind" (a table of rules or partials, or the plane polygon, between `complex-map` screens).
2. Voice scan (`VOICE_BASE=app/content/courses/complex/`): 0 sentences over 20 words, 0 explanations over three sentences.
3. Numbers: `python3 docs/reports/complex-L2-numbers.py` exits 0, 137 checks. Each figure is computed exactly or in closed form, and again in floating point by another route (cmath, NumPy, finite differences, SciPy's complex `erf`, a NumPy Newton iteration). It runs all 9 code widgets of the level in CPython: every solution passes, every starter fails.
4. Playthrough (`--local-cdn .../scratchpad/pkgs`), without and with `--mobile`: all six files green both times; lessons 14 checks each, quizzes 4/4, review-2 9 of 9 recorded, homework-2 9 of 9 right with the longform marked by the button. Screenshots at 1280 and 440 px were read; changes made from them: grids removed from the direction dials (the image grid fell outside the panel), the CF map stacked with a lower panel height.

## Numbers and sources

Every number is in the script with its two methods. Measured in Pyodide 0.27.7 (node, local copy) and CPython 3.13, identical to the last digit:

- Bond: $P = 102.54617478$, $P'(0.04) = -293.41504823$, duration 2.8613. Errors in $P'$: complex step $4 \times 10^{-15}$ against the exact value; central difference $4.3 \times 10^{-6}$ at $h = 10^{-4}$, $2.3 \times 10^{-7}$ at $10^{-8}$, $3.5 \times 10^{-3}$ at $10^{-12}$ (the brief's "compute and report" values; the table rounds them to one figure).
- CF residuals at $u = 1 - 0.5i$: $(1.04 \times 10^{-12}, -4.51 \times 10^{-12})$ for $e^{0.03iu - 0.02u^2}$; $(-0.040178, 0.018604)$ for the version with `abs(u) ** 2`.
- SciPy 1.14.1 in Pyodide evaluates `erf` at complex arguments: `erf(0.35 + 1e-20j)` has imaginary part $9.98 \times 10^{-21}$, and the complex-step delta and vega match $\Phi(0.35) = 0.6368306511756191$ and $37.52403469169379$ to within $10^{-15}$ relative. No prelude series was needed. SciPy loaded in 2.2 s in node from the local copy (a 13.5 MB wheel); the item's `how` warns that the first load can take ten seconds or more on a phone.
- Newton for $z^3 = 1$: starts 2, $-1 + i$, $-1 - i$, $-0.5$, $i$, $0$, $0.5 + 0.5i$ give 0, 1, 2, 0, 1, None, 1; from $0.5 + 0.5i$ the nearest root is 1 (0.7071 away) but Newton reaches $\omega$ (1.0649 away).
- `1j ** 1j` is $0.20787957635076193$; `cmath.log(-1 - 0.001j)` is $4.9999975 \times 10^{-7} - 3.14059265i$; `(-8) ** (1/3)` is `1.0000000000000002+1.7320508075688772j`.

Seeds: none (no random data in level 2).

## Report on the brief

- The brief's "spirals into 0" for the CF image of the real line: the angle only reaches 0.3 rad at $u = 10$, so the content says the curve "curls in towards 0".
- The brief's Heston transfer is taught with the reason the branch matters: $\varphi$ contains $e^{c\log G}$ with a non-whole $c$, so a $2\pi i$ jump in the logarithm becomes a factor $e^{2\pi ic}$. A distractor names the misconception that $e^{\operatorname{Log} G}$ cannot depend on the branch.
- Unit square (item 448): the prediction is a `choice` on a `plane` polygon (the complex-map would show the answer), then a `complex-map` with the four sides as curves, `t` in $[0, 1]$, `grid: "none"`.

## course.json

No change proposed.

## Backlog

Four bullets under "Raised later (complex level 2):" in `docs/BACKLOG-INBOX.md`: hiding only a curve's image, holding a complex-map point to a curve, a w-plane-only marker, and `atan2` in plane curve formulas.

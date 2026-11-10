# Fluency sets: odes (brief `docs/briefs/fluency.md`, second wave row 4, topic 1.11)

## Lessons chosen

- `l2-separable`: separate, integrate, exponentiate, fit the start; the same four moves on fresh rates.
- `l3-integrating-factor`: find $e^{\int p}$, and solve $y' = ay + q$ from its steady level; plus the lesson's savings balance to the penny.
- `l7-characteristic-equation`: roots of $r^2 + br + c = 0$, real or complex, then fitting $y(0)$ and $y'(0)$, also for a repeated root.

Considered and left out: `l16-euler-method` (procedural, but a step table is not a typed single answer at hand size; next candidate), `l6-second-order` and `l8-forcing` (l8 is procedural too; the six-set budget went to l7, which l8 builds on), `l1`, `l4`, `l5`, `l9` to `l15`, `l17`, `l18` (modelling, pictures, stability judgements, transforms and numerics whose answers are readings or code).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-separable | constant-rate | 136 | none | constant-added, start-not-used |
| | rate-that-varies | 171 | none | rate-kept-constant, not-halved |
| | square-rate ($y' = ky^2$) | 76 | none | solved-linear, sign-lost |
| | discount (numeric, £, to the penny) | 174 | none | simple-discount, yearly-discount (`when` it differs) |
| fluency-l3-integrating-factor | find-the-factor | 93 | none | e-to-the-p, sign-flipped |
| | constant-coefficient | 198 | none | steady-sign, inflow-dropped (`when` $y_0 \ne 0$) |
| | savings-balance (numeric, £) | 178 | none | deposits-only, minus-one-dropped |
| fluency-l7-characteristic-equation | real-roots (numeric set) | 124 | none (set) | signs-flipped, not-halved |
| | complex-root | 96 | rectangular | other-root, minus-b-dropped, not-halved |
| | fit-two-roots | 184 | none | constants-swapped (`when` $c_1 \ne c_2$), one-constant (`when` $y(0) \ne 0$) |
| | repeated-root | 150 | none | rc1-forgotten, t-term-dropped |

No solve family needs `form`: the prompt is an equation, and no retyped part of it equals the solution. The money families use `round(..., 2)` of `exp` with `tol` 0.0051, as the lesson's "to the penny" screens do.

## Skipped

No family skipped. One engine limit met here: the course page at 440 px (below).

## Checks

1. `docs/reports/fluency-odes-numbers.py` (shared reader `fluency_1_11_lib.py`), 200 draws a family: every closed form found again by sympy `dsolve` from the equation and starting values built from the vars; the integrating factor by integrating $p$ and checking $(\mu y)' = \mu(y' + py)$; money keys from `exp` rounded half up with `Decimal`. For the two root families the equation is also read back from the printed prompt and solved. 7,139 checks over 11 families, 0 failures, exit 0. A planted +1 on one key was caught.
2. Validator 0 errors, no warning on a fluency file. `test-fluency.mjs --local-cdn`: 305/305 (l2), 302/302 (l3), 307/307 (l7); the default run 1,036/1,036.
3. Playthrough `--fluency`: green on desktop for all three sets. With `--mobile` each fails one check only, the course page at 440 px (the topic 1.11 pill does not wrap; raised). The 440 px item, wrong-answer and result screenshots show no overflow.
4. `voice-scan.py 35` on `app/content/courses/odes`: 0 and 0.
5. I read 20 drawn items of every family and scanned 200 for `1x`, `+-`, `x^1`, `0x`, double minus, `+0`, float artefacts and unreduced fractions. Fixed from the reading: `1\,dt` in a separation step, `+1y` in a repeated-root prompt, `-1c_1` in a line, `1e^{...}` in a slip, an upside-down $\frac{-5}{-10t+1}$ key (now $\frac{-5}{1-10t}$), and "Find the roots" now says "Find both roots". The remaining hit is `1\%` in a prompt.

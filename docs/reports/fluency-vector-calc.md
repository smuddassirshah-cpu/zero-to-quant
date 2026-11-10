# Fluency sets: vector-calc (brief `docs/briefs/fluency.md`, second wave row 4, topic 1.11)

## Lesson chosen

- `l5-divergence-and-curl`: $P_x + Q_y$ and $Q_x - P_y$ of a polynomial field, at a point, and the space curl $(R_y - Q_z, P_z - R_x, Q_x - P_y)$; four partials and a sum each time.

Considered and left out: `l4-conservative-fields` (a gradient and a potential are procedural, the next candidate; the six-set budget allowed one set here), `l2-line-integrals` and `l3-work-done` (procedural but long: parametrise, substitute, integrate, beyond one hand-sized typed step), `l1`, `l6` to `l12` (pictures, theorems and surface integrals whose point is an idea or a choice of method).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l5-divergence-and-curl | divergence | 196 | none | curl-instead, stopped-at-px |
| | curl | 197 | none | reversed, divergence-instead |
| | at-a-point (numeric; asks for one of the two) | 200 | none | other-quantity (`when` it differs), curl-reversed (`when` a curl draw and it differs) |
| | curl-in-space (vector answer) | 199 | none | each-reversed, order-reversed |

The fields keep the lesson's shapes ($x^2y$ terms, a $y^2$ or $x^2$ term) with drawn coefficients, so every derivative prints with no `1x` or `x^1`. The space curl is typed as three components, which the vector answer format reads in any bracket style. No `form`: the prompt shows the field, which never equals its divergence or curl.

## Skipped

No family skipped.

## Checks

1. `docs/reports/fluency-vector-calc-numbers.py` (shared reader `fluency_1_11_lib.py`), 200 draws a family: divergence and planar curl by sympy `diff` of the field built from the vars; the space curl by `sympy.vector.curl`, a separate route from the template's formula; every slip rebuilt from the vars and shown to differ. 2,292 checks over 4 families, 0 failures, exit 0. A planted +1 on one component was caught.
2. Validator 0 errors, no warning on a fluency file. `test-fluency.mjs --local-cdn`: 305/305; the default run 1,036/1,036.
3. Playthrough `--fluency`: green on desktop (one earlier run reported "the same seed drew different questions"; two reruns passed and the sampler is deterministic, so it is raised as a flaky check). With `--mobile` it fails one check only, the course page at 440 px (the topic 1.11 pill does not wrap; raised). The 440 px item and wrong-answer screenshots show no overflow.
4. `voice-scan.py 35` on `app/content/courses/vector-calc`: 0 and 0.
5. I read 20 drawn items of every family and scanned 200 for `1x`, `+-`, `x^1`, `0x`, double minus, `+0`, float artefacts and unreduced fractions: no hits. No prompt gives the answer away.

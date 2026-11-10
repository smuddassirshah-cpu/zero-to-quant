# Fluency sets: complex (brief `docs/briefs/fluency.md`, second wave row 4, topic 1.11)

## Lessons chosen

- `l1-square-root-of-minus-one`: add, multiply and divide in $a + bi$, powers of $i$ and a quadratic with no real roots, all by rote once $i^2 = -1$ is understood.
- `l2-points-in-a-plane`: modulus, distance $|z - w|$, principal argument and polar form back to $x + iy$, each a fixed procedure on fresh numbers.

Considered and left out: `l3-euler` and `l4-roots-of-unity` (one procedural set per level-1 pair was the budget of six sets across three courses; their exponential-form and De Moivre work is the next candidate), `l5` to `l13` (ideas, proofs and judgements: mappings, differentiability, Cauchy-Riemann, contour theorems, Fourier pricing).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l1-square-root-of-minus-one | multiply | 199 | rectangular | i-squared-plus-one, parts-only |
| | divide (whole-number quotient) | 195 | rectangular | part-by-part, bottom-i-squared (`when` $\lvert c\rvert \ne \lvert d\rvert$) |
| | complex-roots (set answer) | 100 | none (set) | not-halved, plus-b |
| | power-of-i | 114 | rectangular | even-is-positive (`when` remainder 2), odd-sign (`when` odd) |
| fluency-l2-points-in-a-plane | modulus (numeric, 3 dp) | 151 | none | added-parts, no-root |
| | distance (numeric, 3 dp) | 200 | none | sum-not-difference, moduli-subtracted (`when` it differs), no-root |
| | principal-argument | 82 | exact-angle | arctan-only (`when` left half-plane), not-principal (`when` negative) |
| | from-polar | 71 | rectangular | cos-sin-swapped, forgot-r |

`rectangular` is set wherever the prompt shows an unevaluated complex number, so retyping $(2 - 5i)(1 - i)$, the quotient, $i^{178}$ or $r(\cos\theta + i\sin\theta)$ fails. The quotient family draws the top as $(c + di)(e + fi)$ so the answer is whole, as the lesson's own worked division would be at hand size.

## Narrowed

- `from-polar` draws $\pm\pi/6$ and $\pm 5\pi/6$ only: at $\pi/3$ the key $9 - 9\sqrt{3}i$ fails `rectangular` (raised in the inbox).
- `principal-argument` is exact only: no `atan` for a decimal argument (raised).

## Checks

1. `docs/reports/fluency-complex-numbers.py` (with the shared reader `fluency_1_11_lib.py`), 200 draws a family: keys from sympy arithmetic, `solve`, `arg`, `Abs` and the drawn angle's `cos` and `sin`; every slip rebuilt from the vars, the offered set of slips checked against each `when`, and each slip shown to differ from the key. 4,556 checks over 8 families, 0 failures, exit 0. A planted +1 on one key was caught.
2. Validator 0 errors, no warning on a fluency file (4,118 in all, none mine). `test-fluency.mjs --local-cdn`: 308/308 (l1), 308/308 (l2); the default run 1,036/1,036.
3. Playthrough `--fluency`: green on desktop for both sets. With `--mobile` each fails one check only, the course page at 440 px (the topic 1.11 pill does not wrap; raised). I read the 440 px item, wrong-answer, Today and result screenshots: no overflow on any set screen.
4. `voice-scan.py 35` on `app/content/courses/complex`: 0 and 0.
5. I read 20 drawn items of every family as a learner would and scanned 200 for `1x`, `+-`, `x^1`, `0x`, double minus, `+0`, float artefacts and unreduced fractions. The scan found `-1i` in the division slips (now `+cfrac`) and $i^1$ in a line (reworded); the rest are false hits (the numeric key value, `(-1)^2`). No prompt gives the answer away.

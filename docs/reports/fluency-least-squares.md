# Fluency sets: least-squares (brief `docs/briefs/fluency.md`, second wave, agent 2, topic 1.4)

One of the eight topic 1.4 sets. Chosen lesson:

- `l11-fitting-a-line`: the slope from centred sums, the normal equations solved for $(\hat\alpha, \hat\beta)$, and the intercept from the means are the lesson's three steps on fresh data.

Considered and left out: `l5-dropping-a-perpendicular` (its projection multiple is drilled in `vectors/fluency-l3-lengths-angles`; the projected vector is one multiplication more), `l4-straightening` (Gram-Schmidt is procedural with a vector answer, but the topic has eight sets; a candidate for a later wave), `l6-projection-matrix` and `l8-qr` (whole-matrix answers), `l1`, `l2`, `l3`, `l7`, `l9`, `l10` (ideas and derivations), `l12-beta-by-hand` (NumPy code).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l11-fitting-a-line | slope-from-points | 200 | none (numeric) | upside-down, not-centred |
| | solve-normal-equations | 181 | none (vector) | swapped-order |
| | intercept-from-means | 185 | none (numeric) | sign-slip, forgot-x-bar |

Four points with evenly spaced $x$ keep the centred sums hand-sized ($\sum (x_i - \bar x)^2$ is 5 or 20). The normal equations use the real $(n, \sum x_i, \sum x_i^2)$ of nine small data sets, so dividing row 1 by $n$ always gives a terminating decimal. `solve-normal-equations` has one slip only: the other errors a learner makes there are arithmetic, not a named step.

## Checks

1. `docs/reports/fluency-least-squares-numbers.py` (sympy, 200 draws a family): the slope by solving $\mathbf{A}^T\mathbf{A}\hat{\mathbf{x}} = \mathbf{A}^T\mathbf{y}$ with $\mathbf{A} = [\mathbf{1}, \mathbf{x}]$ (not the centred formula the family prints), the normal equations by `linsolve`, the intercept by solving $\bar y = \hat\alpha + \hat\beta\bar x$. 1,600 checks, 0 failures, exit 0 (a coinciding slip pair found on the first run is now excluded).
2. Validator 0 errors, no warning on this file. `test-fluency.mjs --local-cdn`: 303/303.
3. Playthrough `--fluency --local-cdn`, with and without `--mobile`: green; the 440 px wrong-answer screen shows the sums and the fraction with no overflow.
4. `voice-scan.py 35` on `app/content/courses/least-squares`: 0 and 0 (the first scan counted a long `let` expression as a sentence; the lets now build on each other).
5. I read 20 drawn items of every family and scanned 200 a family for `1x`, `+-`, `^1`, `0x`, `--`, `+0`, `-0` and float artefacts: no hits.

## Engine limits

None new for this set.

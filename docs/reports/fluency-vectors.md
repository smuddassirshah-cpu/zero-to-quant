# Fluency sets: vectors (brief `docs/briefs/fluency.md`, second wave, agent 2, topic 1.4)

Four of the eight topic 1.4 sets. Chosen lessons, one line of reason each:

- `l3-lengths-angles`: length, unit vector, cosine of the angle and the projection multiple are four rote formulas on fresh numbers.
- `l5-acting-on-a-vector`: $\mathbf{A}\mathbf{x}$ as a combination of columns is the one technique of the lesson.
- `l7-one-after-another`: an entry and a column of $\mathbf{AB}$, the lesson's row-times-column and column views.
- `l10-undoing`: $ad - bc$, a column of the $2 \times 2$ inverse, and solving a pair with $\mathbf{A}^{-1}$.

Considered and left out: `l1-mixing` and `l6-moving-the-plane` (an idea and a recognition), `l11-no-inverse` (a judgement), `l12-numpy-matrices` (code). `l2-lining-up` and `l4-portfolio-return` are the dot product, which every `l3` family uses as its first step; a separate set would drill the same sum. `l8-identity-transpose` and `l9-one-matrix-equation` need a whole matrix as the answer (see engine limits).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l3-lengths-angles | length | 82 | none (numeric) | no-square-root, added-sizes |
| | unit-vector | 80 | none (vector) | divided-by-dot, sign-dropped |
| | cosine-of-angle | 132 | none (numeric) | no-lengths, projection-instead |
| | projection-multiple | 199 | none (numeric) | upside-down, divided-by-uu |
| fluency-l5-acting-on-a-vector | two-by-two | 200 | none (vector) | combined-rows, diagonal-only |
| | taller-columns | 200 | none (vector) | amounts-swapped, added-columns |
| fluency-l7-one-after-another | one-entry | 200 | none (numeric) | order-swapped, row-column-swapped |
| | one-column | 200 | none (vector) | order-swapped, combined-rows |
| fluency-l10-undoing | determinant | 198 | none (numeric) | added-bc, ad-only |
| | inverse-column | 199 | none (vector) | not-divided, not-swapped, added-bc |
| | solve-with-inverse | 199 | none (vector) | multiplied-by-a, swapped-order |

No family needs `form`: each task is "find", and no prompt shows an expression equal to the key. Lengths come from Pythagorean triples and the cosine family from two triple vectors, so every key is exact and needs no calculator; the lesson's answer in degrees would need $\cos^{-1}$, so the family asks for $\cos\theta$ as a fraction. Slips are the lesson's own: dividing by $\mathbf{v} \cdot \mathbf{v}$, dropping a sign, combining rows, $\mathbf{BA}$ for $\mathbf{AB}$, $ad + bc$, not swapping $a$ and $d$. `when` switches a slip off where it equals the key (`sign-dropped` for a positive vector, `row-column-swapped` on the diagonal, `not-divided` when $\det = 1$).

## Checks

1. `docs/reports/fluency-vectors-numbers.py` (with `fluency_la_common.py`; sympy, 200 draws a family): products and inverses by `Matrix`, lengths by `sqrt`, the projection by solving $(\mathbf{u} - k\mathbf{v}) \cdot \mathbf{v} = 0$, the system by `solve`. Each wrong is rebuilt from the vars, must differ from the key and from every other offered wrong. 6,572 checks, 0 failures, exit 0. Its first runs found two coinciding slip pairs (now excluded by `where`).
2. Validator 0 errors, 4,116 warnings, none on a `fluency-*` file. `test-fluency.mjs --local-cdn`: 307/307, 298/298, 299/299, 302/302; the default run 1033/1033.
3. Playthrough `--fluency --local-cdn` of all four sets, with and without `--mobile`: green. One desktop run of l3 reported "the same seed drew different questions"; three reruns were green (raised as a flake). I looked at the 440 px item and wrong-answer screens: no overflow.
4. `voice-scan.py 35` on `app/content/courses/vectors`: 0 and 0.
5. I read 20 drawn items of every family as a learner would, and scanned 200 a family for `1x`, `+-`, `^1`, `0x`, `--`, `+0`, `-0`, float artefacts and `\frac{n}{1}`: no hits. No prompt gives the answer away.

## Engine limits

Raised in `docs/BACKLOG-INBOX.md` under `Raised later (fluency vectors elimination eigen least-squares):` a typed whole-matrix answer, and the playthrough flake.

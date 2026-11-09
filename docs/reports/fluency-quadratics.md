# Fluency: quadratics, and functions l8 (brief `docs/briefs/fluency.md`, agent 2)

Seven sets, 18 families. Each set follows its lesson's notation and instruction words: "Expand and simplify", "Factorise", "complete the square", "with the formula", "rise over run", $y = mx + c$. No set uses an idea from a later lesson.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
| --- | --- | --- | --- | --- |
| fluency-l1-two-brackets | expand-monic | 185 | expanded | firsts-lasts, swapped |
| | expand-coefficient | 192 | expanded | firsts-lasts, added-numbers |
| | expand-square | 82 | expanded | squares-only, one-strip |
| fluency-l2-product-and-sum | factorise-monic | 157 | factorised | signs-swapped, one-sign |
| | perfect-square | 83 | factorised | wrong-sign, difference |
| fluency-l3-leading-coefficient | factorise-non-monic | 188 | factorised | skipped-grouping, numbers-swapped |
| | split-product (numeric) | 188 | none | last-term-only, the-sum |
| fluency-l4-difference-of-squares | square-minus-number | 123 | factorised | squared-difference, squared-sum |
| | number-minus-square | 96 | factorised | order-swapped, squared-difference |
| | mental-difference (numeric) | 105 | none | difference-squared, sum-only |
| fluency-l6-completing-the-square | find-the-constant (numeric) | 188 | none | added-corner, b-not-halved |
| | solve-by-square (numeric) | 158 | none | other-root, centre-sign |
| | largest-value (numeric) | 189 | none | corner-sign, gave-the-input |
| fluency-l7-the-formula | discriminant (numeric) | 196 | none | sign-of-4ac, dropped-four |
| | rational-roots (numeric, tol 0.005) | 190 | none | other-root, b-for-minus-b, halved-root-only |
| | decimal-roots (numeric, 2 dp) | 195 | none | other-root, b-for-minus-b, halved-root-only |
| functions/fluency-l8-line-through-two-points | gradient (numeric) | 200 | none | run-over-rise, sign-slip |
| | line-equation | 196 | none (prompt shows no expression) | first-point-height, sign-of-c |

## Checks

1. `docs/reports/fluency-quadratics-numbers.py` (sympy venv) runs 200 draws of every family. It rebuilds each key from the vars by expanding, factorising, solving or using the discriminant, and checks each `wrong` is the slip it names and lies outside the key's tolerance. It also checks expand keys have no bracket and factorise keys are products. Result: 25,400 of 25,400 checks pass, exit 0.
2. Validator: 0 errors, 4103 warnings before and after (none on these files). `test-fluency.mjs --local-cdn`: 352 of 352 pass.
3. Playthrough `--fluency` for all 7 sets, with and without `--mobile`: all green. Screenshots of l7 and functions l8 at 440 px looked right, with no overflow.
4. Voice scan 35 on quadratics and on functions: 0 and 0.
5. I read 20 draws of every family as a learner would (2,820 lines). There is no `1x`, `+-`, `x^1`, `0x`, double minus or unreduced fraction, and no prompt gives the answer away. A grep for those patterns also finds none. I fixed four faults found while reading: `(t)^2`, a bracket with a common factor, a point on the y-axis in line-equation, and numbers written outside `$`.

## Skipped (raised in BACKLOG-INBOX under "Raised later (fluency quadratics)")

- l3 and l4 "factorise fully" with a common factor first: `form: "factorised"` cannot tell `(2x+4)(x+3)` from `2(x+2)(x+3)`.
- l6 "write in the form $(x+p)^2+q$" as one expression: there is no completed-square `form`.
- l6 and l7 "both roots" and "exact surd roots": there is no unordered-set or $\pm$ answer. The larger and smaller root is asked instead, by a pick pairing that rejects half of all draws (l7: 72% rejected).

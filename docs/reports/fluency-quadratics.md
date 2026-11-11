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

## Widening pass

Every skipped entry above is now written, with the formats of ENGINE-BACKLOG 830 to 833 (AUTHORING section 16). Families not in this table draw exactly what they drew before.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
| --- | --- | --- | --- | --- |
| fluency-l3-leading-coefficient | common-factor-first (new) | 195 | factorised-fully | factor-dropped, factor-sign (`when` k < 0), numbers-swapped (`when` p > 1) |
| fluency-l4-difference-of-squares | common-factor-first (new) | 150 | factorised-fully | factor-dropped, squared-difference |
| fluency-l6-completing-the-square | square-form (new) | 191 | completed-square | added-corner, b-not-halved |
| | solve-by-square (widened: both roots, numeric set) | 138 | none | centre-sign, no-square-root (`when` k > 1) |
| fluency-l7-the-formula | rational-roots (widened: both roots, numeric set, tol 0.005) | 174 | none | b-for-minus-b, halved-root-only |
| | decimal-roots (widened: both roots to 2 dp) | 181 | none | b-for-minus-b, halved-root-only |
| | exact-roots (new: surd roots, expression set, `\pm` accepted) | 178 | none | b-for-minus-b, over-a (`when` a > 1) |

The larger-or-smaller pick (`w`, `g`) is gone from l6 and l7, so those families reject 16 to 47% of draws, where the old pairing threw away half or more (72% in l7). The old `other-root` slip went with it: a set answer with one value returns the key `count`. Exact-roots draws odd $b$ and a discriminant with no square factor, so the key needs no surd simplifying, which the lesson does not teach.

Checks for the widening pass:
1. `docs/reports/fluency-quadratics-numbers.py` now covers the seven new or changed families: set answers against sympy's roots, each wrong set against its named slip and outside the key's tolerance, `when` conditions, the factorise-fully content and linear factors, the completed-square shape. 30,912 of 30,912 checks, exit 0.
2. Validator 0 errors, no warning on these files. `test-fluency.mjs --local-cdn`: 915 of 915.
3. Playthrough `--fluency` of l3, l4, l6 and l7, with and without `--mobile`: green. The l7 wrong-answer screen at 440 px read correctly (count line, then the working).
4. Voice scan 35 on the course folder: 0 and 0.
5. I read 20 draws of every new or changed family, and scanned 200 of each for `1x`, `+-`, `--`, `^1`, `0x`, `+0`, `/1`: no hits. Fixed on reading: an unclear factor-dropped line, a "no-square-root" line, bare minus signs outside maths in the decimal-roots accept line, and unsimplified surds such as $\sqrt{60}$.

Still blocked: none.

## Level 4

Four sets, fourteen families (brief `docs/briefs/fluency.md`; skill `quad-rational`, new this session, and `quad-solve`). The sets follow the lessons' own instruction words and shapes: "in simplest surd form, $a\sqrt{b}$", "Type the top", "a number times one bracket", "over the common denominator", "Factorise ... fully".

- l14-roots-that-stay: the largest square factor, collecting like surds, and the conjugate step of rationalising.
- l15-fractions-with-letters: cancelling a common bracket, multiplying and dividing with cancelling across.
- l16-adding-and-solving: adding and subtracting over a product denominator, clearing fractions to a quadratic, rejecting a root that makes a bottom zero.
- l17-dividing-polynomials: remainder theorem, factor theorem for a coefficient, the quotient, and a cubic factorised fully.

Considered and left out: l18-circles-on-a-grid (distance and the circle's equation: procedural, but the brief names fractions, division and surds for this pass, and the centre-and-radius answer is a pair with a reading step); l19-line-meets-curve (a substitution then a judgement on the discriminant: a problem, not a drill; it is in `problems-4`).

| set | family | distinct prompts in 200 | `form` | slips |
| --- | --- | --- | --- | --- |
| fluency-l14-roots-that-stay | simplest-surd (numeric) | 133 | none | stopped-early (`when` the root is composite), square-not-root |
| | collect-surds (numeric) | 145 | none | no-roots, sign (minus only) |
| | conjugate-bottom (numeric) | 185 | none | added, squared-q |
| fluency-l15-fractions-with-letters | cancel-common-bracket | 198 | expanded | shared-bracket, sign-slip, whole |
| | multiply-and-cancel | 187 | factorised | sign, number-lost |
| | divide-and-cancel | 166 | factorised | sign, letter-lost |
| fluency-l16-adding-and-solving | add-tops | 200 | simplified | own-bottoms, tops-added |
| | subtract-tops | 199 | simplified | sign-lost, own-bottoms |
| | solve-two-roots (numeric set) | 76 | none | signs (and `count`) |
| | reject-root (numeric) | 117 | none | kept-bad, sign |
| fluency-l17-dividing-polynomials | remainder (numeric) | 200 | none | sign, no-constant |
| | find-k (numeric) | 174 | none | sign, power-dropped |
| | quotient | 194 | expanded | sign, constant-sign |
| | factorise-cubic | 143 | factorised-fully | signs, one-sign |

Notes. A surd typed as an expression is graded by value and no `form` refuses $\sqrt{72}$ for $6\sqrt{2}$ (ENGINE-BACKLOG 670), so l14 asks for the number in front, as the lesson's own screen does. l15 asks for the top over a given bottom, as l15 s3 does; the multiply and divide keys carry `factorised`, and `test-fluency` confirms the retyped prompt is refused. l16 `solve-two-roots` draws from 90 tuples $(A, B, k, r, s)$ with whole, distinct roots that make no bottom zero; `reject-root` is $\tfrac{bx}{x - a} = \tfrac{ab}{x - a} + x$, whose cleared quadratic has roots $a$ and $b$. l17 `factorise-cubic` draws from 92 triples of distinct non-zero roots, one of them within 2 of zero so that trial division finds it fast.

### Checks

1. `docs/reports/fluency-quadratics-numbers.py` extended (sympy: `sqrt` and `factorint`, `cancel` and `factor`, `solve` on the uncleared equation, `rem`, `div`, `factor_list`; second routes: a search for the largest square, values at $x = \tfrac{7}{3}$, substitution back, trial of the constant's divisors), 200 draws a family: 55,533 of 55,533 checks across all 36 families, exit 0.
2. Validator: 0 errors, 4,664 warnings before and after (none on these files). `test-fluency.mjs --local-cdn`: 304, 304, 309 and 308 passed, no coinciding-slip notes after two `when` fixes (`sign` against `no-roots` when $p - q = 1$; `one-sign` against `signs` when two roots are opposite).
3. Playthrough `--fluency` of the four sets, desktop and `--mobile`: green. The 440 px shots of l15 (item, wrong answer) read: no layout fault.
4. Voice scan 35 on the course folder: 0 and 0.
5. I read 20 drawn items of every family as a learner would, and scanned 200 of each for `1x`, `+-`, `x^1`, `0x`, double minus, `+0` and float artefacts: no hits after fixes. Fixed on reading: `x -3` spacing in brackets, `1k` and `1(y+4)` coefficients, `+0` when $k = 0$ in find-k, and a quotient working that named a constant as "the $x$ term". A division by zero in a `let` of `simplest-surd` had been rejecting every prime-root draw silently (164 of 364): an `if` now guards it.

### Engine limits (inbox)

- A surd answer cannot be asked as an expression in simplest form (ENGINE-BACKLOG 670 still open): raised again.
- "Type the top" is the only way to ask for a cancelled fraction: no `form` is known to refuse an uncancelled fraction equal to the key (review-quadratics-4 finding 19), so a family cannot ask for the whole simplified fraction.

# Fluency: number-sense (docs/briefs/fluency.md, second wave, agent 1, topic 0.1)

Five sets, thirteen families. Topic 0.1 is the first thing a returning adult meets, so every number is hand-sized: denominators up to 12 with a common size of at most 36, signed whole numbers up to 15, factors up to 12, squares of 2 to 5.

## Lessons chosen

- l3-adding-pieces: adding and taking away fractions of different sizes is one rote move (rename over a common size, add the tops) that needs fresh numbers.
- l5-how-many-halves: dividing by a fraction is a fixed recipe (how many pieces, then how many portions), easy to reverse by mistake.
- l8-below-zero: adding and subtracting signed numbers is pure repetition of the move rule.
- l9-negative-times-negative: the sign rules for multiplying and dividing want drilling once the argument is understood.
- l12-which-first: order of operations is a procedure applied the same way to every expression.

Considered and left out: l1 (a fraction on a number line: an idea, answered by placing a point); l2 (equivalent fractions: procedural, but left out to keep ten sets; its cancelling step is drilled in every l3 and l5 answer, which must be in lowest terms); l4 (multiplying fractions: procedural, left out for ten; top times top is the second step of every l5 working); l6 (place value: comparing and placing decimals, judgements); l7 (fractions to decimals: procedural, the best candidate for a later set); l10 (index laws: taught by counting factors, and drilled in `exp-log/fluency-l3-strange-powers`); l11 (roots: trapping a root between whole numbers is a judgement); l13 (estimates: the answer's tolerance is itself the judgement); l14 (standard form: a typed answer must be in the shape $a \times 10^n$ with $1 \le a < 10$, and no `form` checks that shape; raised in the inbox).

| set | family | distinct prompts in 200 | `form` | slips |
| --- | --- | --- | --- | --- |
| fluency-l3-adding-pieces | add-unlike | 158 | fraction | tops-and-bottoms, tops-not-renamed |
| | subtract-unlike | 133 | fraction | tops-and-bottoms (when both tops and bottoms go down), tops-not-renamed |
| fluency-l5-how-many-halves | whole-by-fraction | 105 | fraction | multiplied, bottom-only (when the top is not 1) |
| | fraction-by-fraction | 137 | fraction | multiplied, flipped-first |
| fluency-l8-below-zero | add-signed | 176 | (numeric) | wrong-way, dropped-signs |
| | subtract-signed | 172 | (numeric) | added, reversed |
| fluency-l9-negative-times-negative | multiply-two | 146 | (numeric) | sign-flipped, added (two negatives only) |
| | divide-two | 138 | (numeric) | sign-flipped, upside-down |
| | multiply-three | 171 | (numeric) | sign-flipped, first-pair-only |
| fluency-l12-which-first | times-before-plus | 193 | (numeric) | left-to-right, lost-sign (negative answers) |
| | powers-next | 187 | (numeric) | multiplied-then-squared, doubled |
| | brackets-first | 179 | (numeric) | added-first, multiplied-then-squared |
| | left-to-right | 161 | (numeric) | right-pair-first, minus-lost |

Notes. The fraction families use `\tfrac` as the lessons do, draw a pick of (top, bottom) tuples of proper fractions in lowest terms, and ask for "a fraction in its lowest terms" with `form: "fraction"` (the lesson accepts decimals; a decimal for $\tfrac{7}{12}$ would only be near). Answers over one whole stay improper ($\tfrac{9}{8}$), as in the lesson. l8 draws the direction word with the sign (`["left", "right", -1]`). l12 `left-to-right` draws its shape with its two operators, $a - b + c$ or $a \div b \times c$, with $a$ a multiple of $b$.

## Checks
1. `docs/reports/fluency-number-sense-numbers.py` (Fraction, 200 draws a family, 21,253 checks): rebuilds each prompt as text from the vars and compares it; works the key again (l12 by evaluating the rebuilt expression with Python's own precedence); checks fraction keys are in lowest terms; rebuilds each slip, checks the slips offered are exactly those whose condition holds, and that each lies outside the key's tolerance and apart from the others. Exit 0. A mutation run (one slip shifted by 1) failed as it should.
2. Validator: 0 errors; no warning on these files (4,116 in all, unchanged). `test-fluency.mjs --local-cdn`: 300, 300, 300, 304 and 308 passed, all green.
3. Playthrough `--fluency` of all five sets, desktop and `--mobile`: green. Screenshots of l3 (item, wrong chip, end card, 440 px and desktop) read: no layout fault.
4. Voice scan 35 on the course folder: 0 and 0.
5. I read 20 drawn items of every family as a learner would, and scanned 200 of each for `1x`, `0x`, `+-`, double minus, `^1`, `+0`, an unreduced fraction in a prompt and an answer printed in the prompt: no hits. Fixed on reading: subtract slips that vanished whenever the first top was not the larger (now offered as a negative or zero top), two slips that met at $(-2) \times (-2)$, and a "both taken away" slip equal to the right-pair slip.

## Engine limits (inbox)
- No `form` for standard form, so l14 has no set.
- The accepted line under a `form: "fraction"` item reads "any expression equal to $\frac{41}{30}$", though a decimal or an unreduced fraction is refused.

## Level 4

Five sets, eighteen families, one set for each level 4 lesson (brief `docs/briefs/fluency.md`; skills `ns-powers`, `ns-fractions` and the new `ns-measures`). Every level 4 lesson teaches a procedure a learner repeats with fresh numbers, so none was left out.

- l15-building-blocks: splitting a number into primes and counting factors from the indices.
- l16-shared-factors: HCF and LCM from shared primes, and HCF times LCM.
- l17-around-and-inside: the four area rules the lesson builds (triangle, parallelogram, trapezium, a cut rectangle).
- l18-circles-and-units: circumference and area from a radius or a diameter, and the two unit changes the lesson drills (speed, square metres).
- l19-one-number-for-many: mean, median, range and the mean of a frequency table.

| set | family | distinct prompts in 200 | `form` | slips |
| --- | --- | --- | --- | --- |
| fluency-l15-building-blocks | largest-prime | 128 | (numeric) | largest-factor, prime-power (index above 1) |
| | count-from-primes | 116 | (numeric) | indices-multiplied, indices-added |
| | count-factors | 113 | (numeric) | pairs, no-plus-one |
| fluency-l16-shared-factors | hcf | 178 | (numeric) | lcm, one-prime (HCF not prime) |
| | lcm | 175 | (numeric) | product, hcf |
| | other-number | 175 | (numeric) | lcm-over-hcf, product |
| fluency-l17-around-and-inside | triangle-area | 180 | (numeric) | no-half, sloping-side |
| | parallelogram-area | 168 | (numeric) | slant-side, halved |
| | trapezium-area | 179 | (numeric) | no-half, longer-side |
| | l-shape-area | 186 | (numeric) | corner-kept, corner-added |
| fluency-l18-circles-and-units | circumference (tol 0.15, 1 dp) | 112 | (numeric) | area-rule, radius-diameter |
| | circle-area (tol 0.2, 1 dp) | 100 | (numeric) | diameter-squared (diameter given), circumference |
| | speed-units (tol 0.05, 1 dp) | 128 | (numeric) | wrong-way, minutes |
| | area-units | 159 | (numeric) | length-only, divided |
| fluency-l19-one-number-for-many | mean | 200 | (numeric) | divided-by-four, loss-added |
| | median | 200 | (numeric) | unsorted, mean |
| | range | 200 | (numeric) | first-last, sign-lost |
| | table-mean (tol 0.01, 2 dp) | 200 | (numeric) | values-only, rows |

Notes. l15 draws from a list of the 196 numbers from 24 to 999 with at least two different primes (all from 2 to 13) and at least three prime factors; each tuple carries the number, its index form and the bracket working, so the prompt never shows a power of 1 or a factor of $p^0$. l16 draws the HCF and a coprime pair, so the key is exact by construction, and keeps every number it prints under 10,000 (no thousands comma is needed). l18 asks for 1 decimal place with bands that take the values from $\pi \approx 3.14$ and $\tfrac{22}{7}$ (the review-4 fault); the speed family goes both ways; the area family writes its 10,000s as `{n}{,}000` in the working. l19 draws sorted values and shows them in one of twelve fixed orders, so the median and range are exact and the "middle as written" slip is real.

### Checks

1. `docs/reports/fluency-number-sense-numbers.py` extended (sympy `factorint`, `divisor_count`, `igcd`, `ilcm`, exact fractions; trial division, the shoelace formula on the drawn shapes, unit squares of the L-shape, the expanded data list), 200 draws a family: 55,164 of 55,164 checks across all 31 families, exit 0. It also probes each circle draw with $\pi = 3.14$ and $\tfrac{22}{7}$ at 1 dp against the band.
2. Validator: 0 errors, 4,664 warnings before and after (none on these files). `test-fluency.mjs --local-cdn`: 304, 304, 308, 308 and 308 passed, no coinciding-slip notes.
3. Playthrough `--fluency` of the five sets, desktop and `--mobile`: green. The 440 px shots of l19 (item, wrong answer) read: no layout fault.
4. Voice scan 35 on the course folder: 0 and 0.
5. I read 20 drawn items of every family as a learner would, and scanned 200 of each for `1x`, `+-`, `x^1`, `0x`, double minus, `+0` and float artefacts: no hits. Fixed on reading: "0 in 1 hours", "a hour", `\tfrac12` from an unescaped brace, a trapezium working that wrote $\tfrac{22}{2}$, 5- and 7-digit unit answers without commas (the volume half of the units family is dropped for that reason), and two slip pairs that met on some draws (`prime-power` with `largest-factor` at 54; `area-rule` with `radius-diameter` at diameter 8).

### Engine limits (inbox)

- No format writes a thousands comma, so a cm³ answer such as 3,300,000 cannot be shown in a working; the volume family was dropped.
- No `form` for a product of primes, so "write 360 as a product of primes" cannot be typed (360 itself would pass); l15 asks for the largest prime and the factor counts instead.

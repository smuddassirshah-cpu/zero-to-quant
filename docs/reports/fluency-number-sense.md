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

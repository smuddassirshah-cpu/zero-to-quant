# Claim ledger: audit fluency-ns-markov

Six Fluency sets at commit 96f27071. Number-sense is Stage 0 (reduced depth: keys, slips, stated rules, conventions); markov is Stage 1 (full depth: every prompt convention, key, slip, feedback line and solution step).

Basis shorthand. **E**: whole-range enumeration in exact fractions, `docs/reports/fluency-ns-markov-concepts.py` Part A (every combination of the family's vars, key and slips re-derived from the vars, not from the file's `let`). **S**: 300 sampler draws per family against that derivation, Part B (0 mismatches in all 16 families). **D**: derivation given in the row. Sources: Norris, *Markov Chains*, section 1.1 (Theorem 1.1.3: the distribution after n steps is the row vector times P^n, and the n-step chance is the (i, j) entry of P^n); order of operations as in any school text (brackets, powers, multiplication and division left to right, addition and subtraction left to right).

Paths are `families[<id>]` in the named file.

## number-sense/fluency-l3-adding-pieces.json

| # | path | claim | verdict | basis |
|---|---|---|---|---|
| 1 | add-unlike.vars | every listed fraction is proper and in lowest terms | correct | E (29 tuples, gcd 1) |
| 2 | add-unlike.widget.answer | key is a/b + c/d in lowest terms; never a whole number | correct | E 456 draws; two reduced fractions with different bottoms cannot sum to a whole number; S |
| 3 | add-unlike.prompt | "as a fraction in its lowest terms" fixes the form the grader wants | imprecise | 228 of 456 keys are above 1; `form: fraction` grades the mixed number `1\frac{5}{12}` wrong (key `form`, run on a scratch widget with grade-all); lesson l3 teaches the mixed number and its quiz accepts `1\tfrac{1}{2}`. Finding 1 |
| 4 | add-unlike.wrong.tops-and-bottoms | (a+c)/(b+d) is "added the tops and the bottoms"; never the key | correct | D: the mediant lies between the two fractions, the sum above both; E |
| 5 | add-unlike.wrong.tops-not-renamed | (a+c)/lcm is "over the common size with the old tops"; never the key; the renamed tops u, w stated are right | correct | D: u >= a, w >= c, one strict since b != d; E |
| 6 | add-unlike.wrong | the two slips never share a value | correct | D: b + d = lcm(b, d) forces b = d; E |
| 7 | add-unlike.solution | rename over the lcm, add the tops, reduce | correct | E (u + w)/L = key |
| 8 | subtract-unlike.widget.answer | key is a/b - c/d, positive, below 1, in lowest terms | correct | E 228 draws; S |
| 9 | subtract-unlike.wrong.tops-and-bottoms | (a-c)/(b-d), offered only when a > c, b > d and it differs from the key | correct | E (114 draws; it never equals the key on a draw where it is defined) |
| 10 | subtract-unlike.wrong.tops-not-renamed | (a-c)/lcm, "kept the old tops", is a wrong method on every draw | misleading | E: on 12 of 228 draws (2/3 - 1/2, 5/6 - 2/3, ...) it equals the key, the slip is switched off by `when`, and the wrong method scores. Finding 4 |
| 11 | subtract-unlike.solution | rename over the lcm, take the tops, reduce | correct | E |

## number-sense/fluency-l5-how-many-halves.json

| # | path | claim | verdict | basis |
|---|---|---|---|---|
| 12 | whole-by-fraction.widget.answer | n ÷ a/b = nb/a, whole or in lowest terms | correct | E 152 draws: key × a/b = n; S |
| 13 | whole-by-fraction.prompt | "a whole number or a fraction in its lowest terms" fixes the form | imprecise | 58 of 152 keys are top-heavy; mixed number refused; lesson l5 screen 3 accepts `1\tfrac{1}{2}`. Finding 2 |
| 14 | whole-by-fraction.wrong.multiplied | n × a/b; never the key | correct | D: equal only if a = b; E |
| 15 | whole-by-fraction.wrong.bottom-only | nb (pieces of size 1/b), offered when a > 1; line's rule "a portion is a of them, so divide by a" | correct | E 88 draws |
| 16 | whole-by-fraction.solution | n holds nb pieces of 1/b; each portion is a pieces | correct | D |
| 17 | fraction-by-fraction.widget.answer | (a/b) ÷ (c/d) = ad/bc, never 1, at most 12 | correct | E 259 draws; S |
| 18 | fraction-by-fraction.prompt | form wording | imprecise | 149 of 259 keys top-heavy. Finding 2 |
| 19 | fraction-by-fraction.wrong.multiplied | ac/bd; rule "dividing by it is multiplying by its upside-down, d/c" | correct | D: equal to the key only if c = d; E |
| 20 | fraction-by-fraction.wrong.flipped-first | (b/a)(c/d) = 1/key; never the key, never the other slip | correct | D: key != 1 by `where`; a != b; E |
| 21 | fraction-by-fraction.solution | a/b × d/c = ad/bc, then reduce | correct | E |

## number-sense/fluency-l8-below-zero.json

| # | path | claim | verdict | basis |
|---|---|---|---|---|
| 22 | add-signed.widget.answer | a + b with b = ±m; whole; may be 0 | correct | E 675 draws; S |
| 23 | add-signed.vars.sg | adding a negative moves left, a positive right | correct | E (direction word against sign on every draw) |
| 24 | add-signed.wrong.wrong-way | a - b, "moved the wrong way" | correct | D: differs from the key by 2m; E |
| 25 | add-signed.wrong.dropped-signs | abs(a) + m, offered when it is neither the key nor a - b | correct | E 450 draws |
| 26 | add-signed.solution | start at a, move m in the stated direction | correct | E |
| 27 | subtract-signed.widget.answer | a - b; never 0 (a != b) | correct | E 765 draws; S |
| 28 | subtract-signed.vars.sg | subtracting a negative moves right, a positive left | correct | E |
| 29 | subtract-signed.wrong.added | a + b; line "Subtracting undoes adding, so it moves the other way, to the {dir}" | correct | E: {dir} is the direction of the subtraction on every draw |
| 30 | subtract-signed.wrong.reversed | b - a is "You took a from b" | misleading | Arithmetically true on every draw (b - a = -key), but on 435 of 765 draws the same value is the sizes with the signs dropped (-5 - 3 typed as 8; -5 - (-3) typed as 2), the likelier slip, and the line then names a mistake the learner did not make. Finding 7 |
| 31 | subtract-signed.solution | "Subtracting b undoes adding it" | correct | D |

## number-sense/fluency-l9-negative-times-negative.json

| # | path | claim | verdict | basis |
|---|---|---|---|---|
| 32 | multiply-two.widget.answer | a × b with at least one negative factor | correct | E 264 draws; S |
| 33 | multiply-two.wrong.sign-flipped | -(ab); rule "two negatives give a positive, one negative gives a negative" | correct | E on every draw |
| 34 | multiply-two.wrong.added | a + b, offered when both are negative and it is not -(ab) | correct | E 87 draws; (a+1)(b+1) = 1 only at a = b = -2, which `when` removes |
| 35 | multiply-two.solution | size first, then the sign | correct | E |
| 36 | divide-two.widget.answer | (qb) ÷ b = q, whole, never 0 or ±1; no division by zero | correct | E 264 draws; S |
| 37 | divide-two.wrong.sign-flipped | -q; rule "division follows the same sign rules as multiplication" | correct | E |
| 38 | divide-two.wrong.upside-down | b ÷ a = 1/q, band 0.005; band never reaches the key or -q; a 2-place decimal of 1/q lies in the band | correct | E (largest size 0.5; rounding error at most 0.005) |
| 39 | divide-two.solution | multiplication check q × b = a | correct | E |
| 40 | multiply-three.widget.answer | abc; negative exactly when the count of negative factors is odd | correct | E 560 draws; S |
| 41 | multiply-three.wrong.sign-flipped | -(abc) | correct | E |
| 42 | multiply-three.wrong.first-pair-only | ab; never ±key since abs(c) >= 2 | correct | D; E |

## number-sense/fluency-l12-which-first.json

| # | path | claim | verdict | basis |
|---|---|---|---|---|
| 43 | times-before-plus.widget.answer | a ± (b × c) | correct | E 2,432 draws; S |
| 44 | times-before-plus.wrong.left-to-right | (a ± b) × c; never the key; rule "Multiply before you add or subtract" | correct | D: equal only if c = 1; E |
| 45 | times-before-plus.wrong.lost-sign | abs(key) when the key is negative and not the other slip; "Taking bc from a goes below zero" | correct | E 1,002 draws; a negative key arises only with the minus sign |
| 46 | powers-next.widget.answer | a ± b × (c^2): power, then product, then sum | correct | E 1,200 draws; S |
| 47 | powers-next.wrong.multiplied-then-squared | a ± (bc)^2; "The power belongs to c alone" | correct | D: equal only if b = 1; E |
| 48 | powers-next.wrong.doubled | a ± 2bc, offered when c != 2 | correct | D: c^2 = 2c only at c = 2; E |
| 49 | brackets-first.widget.answer | a + b × (c - d)^2, bracket at least 2 | correct | E 1,008 draws; S |
| 50 | brackets-first.wrong.added-first | (a + b) g^2; never the key | correct | D; E |
| 51 | brackets-first.wrong.multiplied-then-squared | a + (bg)^2; never the key | correct | D; E |
| 52 | brackets-first.wrong | the two slips are different values on every draw | wrong | E: at a = 8, b = 3, g = 2 (7 draws, any d) both are 44; the learner who squared 3 × 2 is told "You added 8 + 3 = 11 first". grade-all notes it as "1 coinciding Fluency draws". Finding 3 |
| 53 | left-to-right.widget.answer | (a - b) + c, or (a ÷ b) × c; whole | correct | E 400 draws; S |
| 54 | left-to-right.wrong.right-pair-first | a - (b + c), or a ÷ (b × c) = m/c, band 0.01; never reaches the key | correct | D: differs by 2c, or by m(c - 1/c); E |
| 55 | left-to-right.wrong.minus-lost | a + b + c (subtraction draws only) | correct | E |
| 56 | left-to-right (rule) | "Operations of the same rank go from left to right" | correct | standard convention; the lesson states it |

## markov/fluency-l2-transition-matrix.json (full depth)

| # | path | claim | verdict | basis |
|---|---|---|---|---|
| 57 | two-state-two-step.prompt | P is a transition matrix: entries in (0, 1), rows sum to 1 | correct | E 288 draws |
| 58 | two-state-two-step.prompt | convention "rows now and columns next, in the order bull, bear" | correct | Norris 1.1; the lesson's convention (row vector on the left) |
| 59 | two-state-two-step.where | a != b keeps the question from being a one-step question | correct | D and E: P^2 = P entrywise exactly when the two rows are equal (324 pairs checked) |
| 60 | two-state-two-step.widget.answer | key is the (i, j) entry of P^2 | correct | E; Chapman-Kolmogorov; S |
| 61 | two-state-two-step.widget.tol, accept | "key exactly", tolerance 0 | correct | E: every key has at most two decimal places |
| 62 | two-state-two-step.wrong.squared-entry | the square of the (i, j) entry; "add both paths" | correct | E (value is the entry squared on every offered draw) |
| 63 | two-state-two-step.wrong.squared-entry.when | squaring the entry is a wrong method on every draw | misleading | E: on 8 of 288 draws (i != j and the other row's top entry twice this one, as a = 0.1, b = 0.2, bull to bear: 0.9^2 = 0.81 = key) it gives the key and scores. Finding 5 |
| 64 | two-state-two-step.wrong.one-step | the (i, j) entry; "Two periods means a middle state: sum over it" | correct | E; never the key (row 59), so its `when` is always true |
| 65 | two-state-two-step.solution[0] | through bull: P[i][bull] × P[bull][j]; through bear likewise | correct | E |
| 66 | two-state-two-step.solution[1] | the two path products add to the key | correct | E; law of total probability over the middle state |
| 67 | three-state-two-step.vars | every listed row sums to 1 with entries in (0, 1) | correct | E 18 rows |
| 68 | three-state-two-step.prompt | "rows today and columns tomorrow", order Sunny, Cloudy, Rain; start in Sunny | correct | as row 58 |
| 69 | three-state-two-step.widget.answer | key is row Sunny of P times column j of P | correct | E 648 draws; S |
| 70 | three-state-two-step.widget.tol, accept | exact, at most two decimal places | correct | E |
| 71 | three-state-two-step.wrong.squared-entry | P[Sunny][j] squared; "add a path through each" | correct | E; never the key (the other two paths have positive chance) |
| 72 | three-state-two-step.wrong.one-step | P[Sunny][j]; "That is the chance for tomorrow" | correct | E |
| 73 | three-state-two-step.wrong.one-step.when | the one-step chance is a wrong answer on every draw | misleading | E: on 10 of 648 draws the two-step chance equals the one-step chance, the slip is switched off and reading the entry scores. Finding 6 |
| 74 | three-state-two-step.solution[0] | "Row Sunny times column j" | correct | D |
| 75 | three-state-two-step.solution[1] | the three products and their sum | correct | E |
| 76 | distribution-forward.prompt | today's chances u and 1 - u are a distribution; P as rows 57, 58 ("rows now") | correct | E 1,296 draws |
| 77 | distribution-forward.widget.answer | key is entry j of the row vector (u, 1 - u) times P | correct | E; Norris Theorem 1.1.3; pi_1 sums to 1 on every draw; S |
| 78 | distribution-forward.wrong.bull-row-only | P[bull][j]; "as if today were surely bull" | correct | D: differs from the key by (1 - u)(b - a) or its negative, never 0; E |
| 79 | distribution-forward.wrong.unweighted-column | sum of column j; never the key | correct | D: the key is a strict weighted mean of the column, below its sum; E |
| 80 | distribution-forward.solution[0] | "pi_1 = pi_0 P, so the j entry is today's row vector times the j column" | correct | Norris Theorem 1.1.3; the lesson's convention |
| 81 | distribution-forward.solution[1] | u × P[bull][j] + v × P[bear][j] and the two products | correct | E |

## Totals

81 rows: 73 correct, 3 imprecise, 4 misleading, 1 wrong, 0 unverified.

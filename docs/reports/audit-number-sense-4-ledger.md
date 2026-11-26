# Concept audit ledger: number-sense level 4 (round 1)

Blind read at commit 3222a0fe. Stage 0 depth (`docs/briefs/concept-audit.md`): definitions, rules, "always / never / every" claims, conventions, and every graded key, wrong option and slip. Generated families are judged over their whole range: pick tables exhaustively, integer ranges on 300 draws each, in `docs/reports/number-sense-L4-concepts.py` ("script" below).

Rows: 585. Verdicts: correct 571, wrong 0, imprecise 13, misleading 1, unverified 0.

## l15-building-blocks

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `screens[0].widget.answer` | key regions r1c1, r1c2, r1c3, r1c4, r1c6 | correct | 36 = 1*36 = 2*18 = 3*12 = 4*9 = 6*6; 36 mod 5 = 1, mod 7 = 1, mod 8 = 4 |
| `screens[0].feedback.byKey.r1c5` | wrong tap: Rows of 5 leave a tile over: $7 \times 5 = 35$. | correct | 36 = 1*36 = 2*18 = 3*12 = 4*9 = 6*6; 36 mod 5 = 1, mod 7 = 1, mod 8 = 4 |
| `screens[0].feedback.byKey.r1c7` | wrong tap: Rows of 7 leave a tile over: $5 \times 7 = 35$. | correct | 36 = 1*36 = 2*18 = 3*12 = 4*9 = 6*6; 36 mod 5 = 1, mod 7 = 1, mod 8 = 4 |
| `screens[0].feedback.byKey.r1c8` | wrong tap: Rows of 8 leave 4 tiles over: $4 \times 8 = 32$. | correct | 36 = 1*36 = 2*18 = 3*12 = 4*9 = 6*6; 36 mod 5 = 1, mod 7 = 1, mod 8 = 4 |
| `screens[1].widget.answer` | key 9 | correct | factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36 (9); slips 10 = 5 pairs * 2, 5 = pair count |
| `screens[1].widget.wrong[0]` | slip six-twice = 10: You counted 6 twice. The square row $6 \times 6$ gives one factor, not two. | correct | factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36 (9); slips 10 = 5 pairs * 2, 5 = pair count |
| `screens[1].widget.wrong[1]` | slip rectangles = 5: You counted the rectangles. Each rectangle has two numbers, so count the numbers. | correct | factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36 (9); slips 10 = 5 pairs * 2, 5 = pair count |
| `screens[2].widget.answer` | key 1 | correct | 37 is prime (2, 3, 5 fail; 7*7 > 37), so only 1 by 37; slips 2 = both orientations, 37 = tile count |
| `screens[2].widget.wrong[0]` | slip turned = 2: You counted $1 \times 37$ and $37 \times 1$. They are the same rectangle turned round. | correct | 37 is prime (2, 3, 5 fail; 7*7 > 37), so only 1 by 37; slips 2 = both orientations, 37 = tile count |
| `screens[2].widget.wrong[1]` | slip thirty-seven = 37: That is the number of tiles. Count the rectangles: only one shape uses them all. | correct | 37 is prime (2, 3, 5 fail; 7*7 > 37), so only 1 by 37; slips 2 = both orientations, 37 = tile count |
| `screens[3].widget.answer` | key regions r5c9, r8c7, r10c1 | correct | multiples of 7 to 100 with no factor 2, 3, 5: 49, 77, 91 (concepts script, sieve check) |
| `screens[3].feedback.byKey.r1c7` | wrong tap: 7 itself is prime: it is the number we are crossing out the multiples of. | correct | multiples of 7 to 100 with no factor 2, 3, 5: 49, 77, 91 (concepts script, sieve check) |
| `screens[3].feedback.byKey.r2c4` | wrong tap: 14 is already shaded: it is a multiple of 2. | correct | multiples of 7 to 100 with no factor 2, 3, 5: 49, 77, 91 (concepts script, sieve check) |
| `screens[3].feedback.byKey.r3c1` | wrong tap: 21 is already shaded: it is a multiple of 3. | correct | multiples of 7 to 100 with no factor 2, 3, 5: 49, 77, 91 (concepts script, sieve check) |
| `screens[4].widget.options[0]` | keyed correct: Divide by 2, 3, 5 and 7: the primes below $\sqrt{97}$ | correct | if 97 = ab with a <= b then a*a <= 97 so a <= 9; 97 = 2*48+1 = 3*32+1 = 5*19+2 = 7*13+6 |
| `screens[4].widget.options[1]` | wrong option: Divide by every number from 2 to 96. Why: That works, but most of it is wasted: a factor above 10 would n… | imprecise | Finding 1: dividing by every number from 2 to 96 IS enough to show 97 is prime (the why line says "That works"); the question asks what is "enough", not what is fewest |
| `screens[4].widget.options[2]` | wrong option: Divide by every number up to 48, half of 97. Why: Halfway is far too far. A factor pair always has one me… | imprecise | Finding 1: dividing by every number to 48 covers 2, 3, 5, 7, so it too is enough; marked wrong only because it is wasteful |
| `screens[4].widget.options[3]` | wrong option: Divide by 2 and 5 only, since 97 ends in 7. Why: The last digit only rules out 2 and 5. You still need to… | correct | if 97 = ab with a <= b then a*a <= 97 so a <= 9; 97 = 2*48+1 = 3*32+1 = 5*19+2 = 7*13+6 |
| `screens[5].widget.rows[0][1].answer` | cell key 3 (2) | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[0][1].wrong[0]` | slip missed-two = 2: Tree A has three 2s: one under each 6 and one under the 10. | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[0][2].answer` | cell key 3 (2) | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[0][2].wrong[0]` | slip missed-two-b = 2: Tree B has three 2s: one under the 8 and two under the 4. | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[1][1].answer` | cell key 2 (3) | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[1][1].wrong[0]` | slip one-three = 1: Tree A has two 3s, one under each 6. | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[1][2].answer` | cell key 2 (3) | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[1][2].wrong[0]` | slip one-three-b = 1: Tree B has two 3s, both under the 9. | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[2][1].answer` | cell key 1 (5) | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[5].widget.rows[2][2].answer` | cell key 1 (5) | correct | 360 = 36*10 = 8*45 = 2^3 * 3^2 * 5; uniqueness: fundamental theorem of arithmetic (Hardy and Wright, ch. 1, Theorem 2) |
| `screens[6].widget.answer` | key regions r1c2, r6c3, r6c9 | correct | 2, 53, 59 prime; 1 has one factor; 51 = 3*17, 57 = 3*19, 91 = 7*13 |
| `screens[6].feedback.byKey.r1c1` | wrong tap: 1 has only one factor, itself. A prime needs exactly two, so 1 is not prime. | correct | 2, 53, 59 prime; 1 has one factor; 51 = 3*17, 57 = 3*19, 91 = 7*13 |
| `screens[6].feedback.byKey.r6c1` | wrong tap: 51 looks prime, but $51 = 3 \times 17$. | correct | 2, 53, 59 prime; 1 has one factor; 51 = 3*17, 57 = 3*19, 91 = 7*13 |
| `screens[6].feedback.byKey.r6c7` | wrong tap: 57 looks prime, but $57 = 3 \times 19$. | correct | 2, 53, 59 prime; 1 has one factor; 51 = 3*17, 57 = 3*19, 91 = 7*13 |
| `screens[6].feedback.byKey.r10c1` | wrong tap: 91 looks prime, but $91 = 7 \times 13$. | correct | 2, 53, 59 prime; 1 has one factor; 51 = 3*17, 57 = 3*19, 91 = 7*13 |
| `screens[7].widget.answer` | key 24 | correct | d(n) = product of (e+1) (Hardy and Wright, section 16.7): 4*3*2 = 24; slips 6 = 3*2*1, 9 = 4+3+2 |
| `screens[7].widget.wrong[0]` | slip no-plus-one = 6: You multiplied the indices. Each prime can also be left out, so add 1 to each index first. | correct | d(n) = product of (e+1) (Hardy and Wright, section 16.7): 4*3*2 = 24; slips 6 = 3*2*1, 9 = 4+3+2 |
| `screens[7].widget.wrong[1]` | slip added = 9: You added the choices. Every choice of 2s goes with every choice of 3s and 5s, so multiply. | correct | d(n) = product of (e+1) (Hardy and Wright, section 16.7): 4*3*2 = 24; slips 6 = 3*2*1, 9 = 4+3+2 |
| `screens[8].widget.answer` | order pair > small > root > test | correct | a <= b and ab = 97 give a*a <= 97; the larger factor is at least the root, so the distractor is false |
| `screens[8].widget.lines[both]` | distractor (does not follow): So the larger number is under 10 as well. Why: The larger number is at least $\sqrt{97}$.… | correct | a <= b and ab = 97 give a*a <= 97; the larger factor is at least the root, so the distractor is false |
| `screens[9].widget.options[0]` | keyed correct: 21 days | correct | 252 = 2^2 * 3^2 * 7; 252/21 = 12, /63 = 4, /7 = 36, /12 = 21; 252 mod 5 = 2, mod 8 = 4, mod 24 = 12 |
| `screens[9].widget.options[1]` | keyed correct: 63 days | correct | 252 = 2^2 * 3^2 * 7; 252/21 = 12, /63 = 4, /7 = 36, /12 = 21; 252 mod 5 = 2, mod 8 = 4, mod 24 = 12 |
| `screens[9].widget.options[2]` | keyed correct: 7 days | correct | 252 = 2^2 * 3^2 * 7; 252/21 = 12, /63 = 4, /7 = 36, /12 = 21; 252 mod 5 = 2, mod 8 = 4, mod 24 = 12 |
| `screens[9].widget.options[3]` | keyed correct: 12 days | correct | 252 = 2^2 * 3^2 * 7; 252/21 = 12, /63 = 4, /7 = 36, /12 = 21; 252 mod 5 = 2, mod 8 = 4, mod 24 = 12 |
| `screens[9].widget.options[4]` | wrong option: 5 days. Why: 252 has no 5 among its primes, so periods of 5 leave 2 days over. | correct | 252 = 2^2 * 3^2 * 7; 252/21 = 12, /63 = 4, /7 = 36, /12 = 21; 252 mod 5 = 2, mod 8 = 4, mod 24 = 12 |
| `screens[9].widget.options[5]` | wrong option: 8 days. Why: 8 needs three 2s, and 252 has only two. Periods of 8 leave 4 days over. | correct | 252 = 2^2 * 3^2 * 7; 252/21 = 12, /63 = 4, /7 = 36, /12 = 21; 252 mod 5 = 2, mod 8 = 4, mod 24 = 12 |
| `screens[9].widget.options[6]` | wrong option: 24 days. Why: 24 needs three 2s as well. Ten periods of 24 use 240 days and leave 12. | correct | 252 = 2^2 * 3^2 * 7; 252/21 = 12, /63 = 4, /7 = 36, /12 = 21; 252 mod 5 = 2, mod 8 = 4, mod 24 = 12 |
| `quiz[0].widget.answer` | key 3 | correct | factors of 49: 1, 7, 49; slips 4 = 7 counted twice, 2 = treated as prime |
| `quiz[0].widget.wrong[0]` | slip seven-twice = 4: You counted 7 twice. The pair $7 \times 7$ gives one factor. | correct | factors of 49: 1, 7, 49; slips 4 = 7 counted twice, 2 = treated as prime |
| `quiz[0].widget.wrong[1]` | slip prime = 2: 49 is not prime: 7 divides it. | correct | factors of 49: 1, 7, 49; slips 4 = 7 counted twice, 2 = treated as prime |
| `quiz[1].widget.options[0]` | keyed correct: No: $87 = 3 \times 29$ | correct | 87 = 3*29 (8+7 = 15); 7*13 = 91 |
| `quiz[1].widget.options[1]` | wrong option: Yes: it is odd and not in the 7 times table. Why: Being odd only rules out 2. Try 3: $3 \times 29 = 87$. | correct | 87 = 3*29 (8+7 = 15); 7*13 = 91 |
| `quiz[1].widget.options[2]` | wrong option: No: $87 = 7 \times 13$. Why: $7 \times 13 = 91$, not 87. Try 3. | correct | 87 = 3*29 (8+7 = 15); 7*13 = 91 |
| `quiz[1].widget.options[3]` | wrong option: Yes: no number up to 9 divides it. Why: 3 divides it: $3 \times 29 = 87$. | correct | 87 = 3*29 (8+7 = 15); 7*13 = 91 |
| `quiz[2].widget.options[0]` | keyed correct: $2^3 \times 3^2$ | correct | 72 = 8*9 = 2^3 * 3^2; 2^2 * 3^3 = 108; 8*9 and 2*9*4 equal 72 but hold non-primes |
| `quiz[2].widget.options[1]` | wrong option: $2^2 \times 3^3$. Why: That is $4 \times 27 = 108$. Split 72 again and count the 2s. | correct | 72 = 8*9 = 2^3 * 3^2; 2^2 * 3^3 = 108; 8*9 and 2*9*4 equal 72 but hold non-primes |
| `quiz[2].widget.options[2]` | wrong option: $8 \times 9$. Why: That equals 72, but 8 and 9 are not prime. Keep splitting. | correct | 72 = 8*9 = 2^3 * 3^2; 2^2 * 3^3 = 108; 8*9 and 2*9*4 equal 72 but hold non-primes |
| `quiz[2].widget.options[3]` | wrong option: $2 \times 3^2 \times 4$. Why: 4 is not prime: it splits into $2 \times 2$. | correct | 72 = 8*9 = 2^3 * 3^2; 2^2 * 3^3 = 108; 8*9 and 2*9*4 equal 72 but hold non-primes |
| `quiz[3].widget.answer` | key 12 | correct | (3+1)(2+1) = 12; slips 6 = 3*2, 7 = 4+3 |
| `quiz[3].widget.wrong[0]` | slip no-plus-one = 6: You multiplied the indices. Add 1 to each first. | correct | (3+1)(2+1) = 12; slips 6 = 3*2, 7 = 4+3 |
| `quiz[3].widget.wrong[1]` | slip added = 7: You added the choices. Multiply them. | correct | (3+1)(2+1) = 12; slips 6 = 3*2, 7 = 4+3 |
| `screens[1].prose` | Definition: each number in a pair multiplying to 36 is a factor of 36, and 36 is a multiple of it | correct | Hardy and Wright, An Introduction to the Theory of Numbers, section 1.1 (divisibility); factors include 1 and the number itself, as the table shows |
| `screens[0].explain.text` | Convention: 1 by 36 and 36 by 1 are the same rectangle turned, so 36 tiles make five rectangles | correct | stated before screens[2] grades it (slip 2 "turned"); unordered factor pairs of 36 number 5 |
| `screens[3].prose` | Definition: exactly two factors, 1 and itself, is prime; above 1 with more factors is composite | correct | Hardy and Wright, section 1.2; excludes 1 (one factor) without a special case |
| `screens[3].explain.text` | First new multiple of 7 is 7*7; what stays white apart from 1 is the primes; 25 below 100, 15 below 50, 10 below 30 | correct | sieve of Eratosthenes: 11*11 > 100, so 2, 3, 5, 7 suffice; counts checked in script |
| `screens[4].prose` | sqrt(97) is between 9 and 10 because 81 < 97 < 100 | correct | squaring is increasing on positive numbers |
| `screens[4].widget.question` | "Which divisions are enough to show that 97 is prime?" with three sufficient options, one keyed | imprecise | Finding 1: "enough" is met by options all and half as well; the key is the unique answer only to "fewest" |
| `screens[4].explain.text` | Testing 2, 3, 5 and 7 covers 4, 6, 8 and 9 too | correct | a number divisible by 4, 6, 8 or 9 is divisible by 2 or 3 |
| `screens[5].explain.text` | Whichever pair you start with, the primes come out the same | correct | fundamental theorem of arithmetic, Hardy and Wright ch. 1 Theorem 2 |
| `screens[6].feedback.byKey.r1c1` | 1 has only one factor, so it is not prime; 2 is the only even prime | correct | every even number above 2 has the factor 2 besides 1 and itself |
| `screens[6].hints[1].text` | Rule: a number divides by 3 when its digits add to a multiple of 3 | correct | 10 = 9 + 1, so a number and its digit sum leave the same remainder on division by 3 |
| `screens[7].prose` | Each index gives one more choice than its value, because the power 0 counts too; factors of 2^2 * 3^2 number (2+1)(2+1) | correct | Hardy and Wright section 16.7, d(n) = product of (a_i + 1); checked for every n to 3,000 in script |
| `screens[8].feedback.correct` | A factor pair always has one member at most the square root | correct | a <= b and ab = n give a*a <= n; script checks every composite to 20,000 |
| `screens[9].prose` | Convention: a year has 252 trading days | correct | standard practitioner day count (Hull, Options, Futures and Other Derivatives, ch. 15, trading days and volatility) |
| `screens[9].hints[2].text` | "21, 63, 7 and 12 use only primes 252 has; 5, 8 and 24 do not" | imprecise | Finding 2: 8 = 2^3 and 24 = 2^3 * 3 use only the primes 2 and 3, which 252 has; they fail on the number of 2s |
| `screens[9].explain.text` | "5, 8 and 24 each need a prime that is not there" | imprecise | Finding 2: true only if "a prime" means a third copy of 2; a learner could carry away "same primes means it divides" |
| `screens[9].feedback.correct` | 21 days give 12 months, 63 give 4 quarters, 7 give 36 weeks, 12 give 21 blocks | misleading | Finding 3: 21 and 63 trading days are the practitioner month and quarter, but a trading week is 5 days; 252 trading days are about 50 weeks, not 36 |
| `summary.ideas[1]` | A prime has exactly two factors; 1 is not prime and 2 is the only even prime | correct | as screens[3] and screens[6] |
| `summary.ideas[2]` | Every whole number above 1 splits into one product of primes, however the factor tree starts | correct | fundamental theorem of arithmetic (a prime is its own product of one prime) |
| `summary.formula.note` | To test for a prime, divide by the primes up to its square root | correct | "up to" includes the root itself, which a square such as 49 needs |
| `quiz[0].explain.text` | Square numbers are the numbers with an odd count of factors | correct | factors pair off as k and n/k except when k*k = n; checked to 3,000 in script |

## l16-shared-factors

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `screens[0].widget.points[0].target` | target 36 | correct | multiples of 12: 12, 24, 36; of 18: 18, 36; first common 36 = lcm |
| `screens[0].widget.wrong[0]` | wrong region later: Both print at 72, but they meet earlier too. | correct | multiples of 12: 12, 24, 36; of 18: 18, 36; first common 36 = lcm |
| `screens[0].widget.wrong[1]` | wrong region a-only: Only feed A prints at 12. | correct | multiples of 12: 12, 24, 36; of 18: 18, 36; first common 36 = lcm |
| `screens[0].widget.wrong[2]` | wrong region b-only: Only feed B prints at 18. | correct | multiples of 12: 12, 24, 36; of 18: 18, 36; first common 36 = lcm |
| `screens[0].widget.wrong[3]` | wrong region a24: Only feed A prints at 24. | correct | multiples of 12: 12, 24, 36; of 18: 18, 36; first common 36 = lcm |
| `screens[1].widget.answer` | key 6 seconds | correct | common factors of 12 and 18: 1, 2, 3, 6; slips 3 and 2 are common but not highest, 36 = lcm, 216 = 12*18 |
| `screens[1].widget.wrong[0]` | slip three = 3: 3 divides both, but a longer block also works. | correct | common factors of 12 and 18: 1, 2, 3, 6; slips 3 and 2 are common but not highest, 36 = lcm, 216 = 12*18 |
| `screens[1].widget.wrong[1]` | slip two = 2: 2 divides both, but a longer block also works. | correct | common factors of 12 and 18: 1, 2, 3, 6; slips 3 and 2 are common but not highest, 36 = lcm, 216 = 12*18 |
| `screens[1].widget.wrong[2]` | slip meet = 36: 36 is when they print together. A block must fit inside each gap. | correct | common factors of 12 and 18: 1, 2, 3, 6; slips 3 and 2 are common but not highest, 36 = lcm, 216 = 12*18 |
| `screens[1].widget.wrong[3]` | slip product = 216: 216 is $12 \times 18$, longer than either gap. | correct | common factors of 12 and 18: 1, 2, 3, 6; slips 3 and 2 are common but not highest, 36 = lcm, 216 = 12*18 |
| `screens[2].widget.answer` | key 12 | correct | lcm(4, 6) = 12; slips 24 = product, 2 = hcf |
| `screens[2].widget.wrong[0]` | slip product = 24: 24 is $4 \times 6$, a common multiple, but not the lowest: 12 comes first. | correct | lcm(4, 6) = 12; slips 24 = product, 2 = hcf |
| `screens[2].widget.wrong[1]` | slip hcf = 2: 2 is the HCF, the biggest common factor. The LCM is a multiple. | correct | lcm(4, 6) = 12; slips 24 = product, 2 = hcf |
| `screens[3].widget.answer` | key 12 | correct | 84 = 2^2*3*7, 120 = 2^3*3*5, shared 2*2*3 = 12; slips 6 = 2*3, 2, 24 = 2^3*3, 840 = lcm |
| `screens[3].widget.wrong[0]` | slip one-two = 6: You used one 2. The overlap holds two 2s: $2 \times 2 \times 3 = 12$. | correct | 84 = 2^2*3*7, 120 = 2^3*3*5, shared 2*2*3 = 12; slips 6 = 2*3, 2, 24 = 2^3*3, 840 = lcm |
| `screens[3].widget.wrong[1]` | slip just-two = 2: You used one 2 only. Multiply everything in the overlap: $2 \times 2 \times 3$. | correct | 84 = 2^2*3*7, 120 = 2^3*3*5, shared 2*2*3 = 12; slips 6 = 2*3, 2, 24 = 2^3*3, 840 = lcm |
| `screens[3].widget.wrong[2]` | slip big-power = 24: You took three 2s, from 120. 84 has only two, so only two are shared. | correct | 84 = 2^2*3*7, 120 = 2^3*3*5, shared 2*2*3 = 12; slips 6 = 2*3, 2, 24 = 2^3*3, 840 = lcm |
| `screens[3].widget.wrong[3]` | slip lcm = 840: 840 is the LCM, built from every region. The HCF is the overlap alone. | correct | 84 = 2^2*3*7, 120 = 2^3*3*5, shared 2*2*3 = 12; slips 6 = 2*3, 2, 24 = 2^3*3, 840 = lcm |
| `screens[4].widget.answer` | key 840 | correct | lcm = 2^3*3*5*7 = 840; slips 10080 = 84*120, 12 = hcf, 420 = 7*12*5 |
| `screens[4].widget.wrong[0]` | slip product = 10080: $84 \times 120$ counts the overlap twice. Count each region once. | correct | lcm = 2^3*3*5*7 = 840; slips 10080 = 84*120, 12 = hcf, 420 = 7*12*5 |
| `screens[4].widget.wrong[1]` | slip hcf = 12: 12 is the HCF, the overlap alone. | correct | lcm = 2^3*3*5*7 = 840; slips 10080 = 84*120, 12 = hcf, 420 = 7*12*5 |
| `screens[4].widget.wrong[2]` | slip missed-two = 420: You left out a 2 from the right part. 120 needs three 2s. | correct | lcm = 2^3*3*5*7 = 840; slips 10080 = 84*120, 12 = hcf, 420 = 7*12*5 |
| `screens[5].widget.options[0]` | keyed correct: $\dfrac{7}{10}$ | correct | 84/12 = 7, 120/12 = 10; 42/60 and 21/30 not in lowest terms; 1/10 = 84/84 over 120/12 |
| `screens[5].widget.options[1]` | wrong option: $\dfrac{42}{60}$. Why: You divided by 2 only. Both can still be divided by 6. | correct | 84/12 = 7, 120/12 = 10; 42/60 and 21/30 not in lowest terms; 1/10 = 84/84 over 120/12 |
| `screens[5].widget.options[2]` | wrong option: $\dfrac{21}{30}$. Why: You divided by 4. Both can still be divided by 3. | correct | 84/12 = 7, 120/12 = 10; 42/60 and 21/30 not in lowest terms; 1/10 = 84/84 over 120/12 |
| `screens[5].widget.options[3]` | wrong option: $\dfrac{1}{10}$. Why: You divided the bottom by 12 but the top by 84. Divide both by 12. | correct | 84/12 = 7, 120/12 = 10; 42/60 and 21/30 not in lowest terms; 1/10 = 84/84 over 120/12 |
| `screens[6].widget.options[0]` | keyed correct: $\dfrac{29}{36}$ | correct | 5/12 = 15/36, 7/18 = 14/36, sum 29/36 (Fraction check in script); 12/30 = tops and bottoms added |
| `screens[6].widget.options[1]` | wrong option: $\dfrac{12}{30}$. Why: You added the tops and the bottoms. The pieces are different sizes, so cut both in… | correct | 5/12 = 15/36, 7/18 = 14/36, sum 29/36 (Fraction check in script); 12/30 = tops and bottoms added |
| `screens[6].widget.options[2]` | wrong option: $\dfrac{12}{36}$. Why: You changed the bottoms to 36 but not the tops. $\tfrac{5}{12} = \tfrac{15}{36}$. | correct | 5/12 = 15/36, 7/18 = 14/36, sum 29/36 (Fraction check in script); 12/30 = tops and bottoms added |
| `screens[6].widget.options[3]` | wrong option: $\dfrac{29}{216}$. Why: You scaled the tops for 36ths but wrote 216 below. Keep the piece size you scaled… | correct | 5/12 = 15/36, 7/18 = 14/36, sum 29/36 (Fraction check in script); 12/30 = tops and bottoms added |
| `screens[7].widget.rows[0][2].answer` | cell key 54 (252) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[0][2].wrong[0]` | slip added = 450: You added. Take 198 away from 252. | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[1][1].answer` | cell key 54 (198) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[1][2].answer` | cell key 36 (198) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[1][2].wrong[0]` | slip once = 144: You took 54 away once. Three 54s fit in 198, leaving 36. | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[2][0].answer` | cell key 54 (row 2) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[2][1].answer` | cell key 36 (row 2) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[2][2].answer` | cell key 18 (row 2) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[3][0].answer` | cell key 36 (row 3) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[3][1].answer` | cell key 18 (row 3) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[3][2].answer` | cell key 0 (row 3) | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[7].widget.rows[3][2].wrong[0]` | slip half = 18: Two 18s fit in 36 exactly, so nothing is left. | correct | Euclid: 252 = 198 + 54, 198 = 3*54 + 36, 54 = 36 + 18, 36 = 2*18 (Hardy and Wright, section 12.3); lcm 252*198/18 = 2772 |
| `screens[8].widget.options[0]` | keyed correct: HCF 4, LCM 24 | correct | hcf(8, 12) = 4, lcm = 24; 96 = product; 24 > 8 cannot divide 8 |
| `screens[8].widget.options[1]` | wrong option: HCF 4, LCM 96. Why: 96 is $8 \times 12$. It is a common multiple, but 24 comes first. | correct | hcf(8, 12) = 4, lcm = 24; 96 = product; 24 > 8 cannot divide 8 |
| `screens[8].widget.options[2]` | wrong option: HCF 24, LCM 4. Why: You swapped them. An HCF of 24 is bigger than 8, so it cannot divide 8. | correct | hcf(8, 12) = 4, lcm = 24; 96 = product; 24 > 8 cannot divide 8 |
| `screens[8].widget.options[3]` | wrong option: HCF 2, LCM 48. Why: 2 and 48 are a common factor and a common multiple, but not the highest and the lowes… | correct | hcf(8, 12) = 4, lcm = 24; 96 = product; 24 > 8 cannot divide 8 |
| `screens[9].widget.answer` | order c84 > c120 > prod > def > same > end | correct | each prime sits in one Venn region; both products use left once, overlap twice, right once; 12 + 840 = 852, not 204 |
| `screens[9].widget.lines[sum]` | distractor (does not follow): So HCF + LCM $= 84 + 120$. Why: Adding does not share out primes. $12 + 840 = 852$, not 2… | correct | each prime sits in one Venn region; both products use left once, overlap twice, right once; 12 + 840 = 852, not 204 |
| `screens[10].widget.answer` | key 30 shares | correct | 150 = 2*3*5^2, 240 = 2^4*3*5, hcf 30; slips 10 and 15 common but not highest, 1200 = lcm, 90 = 240 - 150 and 150 mod 90 = 60 |
| `screens[10].widget.wrong[0]` | slip ten = 10: 10 divides both, but so does 30. | correct | 150 = 2*3*5^2, 240 = 2^4*3*5, hcf 30; slips 10 and 15 common but not highest, 1200 = lcm, 90 = 240 - 150 and 150 mod 90 = 60 |
| `screens[10].widget.wrong[1]` | slip fifteen = 15: 15 divides 150 and 240, but 30 is bigger and still divides both. | correct | 150 = 2*3*5^2, 240 = 2^4*3*5, hcf 30; slips 10 and 15 common but not highest, 1200 = lcm, 90 = 240 - 150 and 150 mod 90 = 60 |
| `screens[10].widget.wrong[2]` | slip lcm = 1200: 1,200 is the LCM, larger than either order. | correct | 150 = 2*3*5^2, 240 = 2^4*3*5, hcf 30; slips 10 and 15 common but not highest, 1200 = lcm, 90 = 240 - 150 and 150 mod 90 = 60 |
| `screens[10].widget.wrong[3]` | slip diff = 90: You took 150 from 240. 90 does not divide 150. | correct | 150 = 2*3*5^2, 240 = 2^4*3*5, hcf 30; slips 10 and 15 common but not highest, 1200 = lcm, 90 = 240 - 150 and 150 mod 90 = 60 |
| `quiz[0].widget.answer` | key 12 months | correct | lcm(6, 4) = 12; slips 24 = product, 2 = hcf |
| `quiz[0].widget.wrong[0]` | slip product = 24: 24 is $6 \times 4$; they meet earlier, at 12. | correct | lcm(6, 4) = 12; slips 24 = product, 2 = hcf |
| `quiz[0].widget.wrong[1]` | slip hcf = 2: 2 is the HCF. You need a common multiple. | correct | lcm(6, 4) = 12; slips 24 = product, 2 = hcf |
| `quiz[1].widget.options[0]` | keyed correct: HCF 1, LCM 120 | correct | gcd(8, 15) = 1, lcm = 120; 23 = 8 + 15; hcf cannot exceed 8; 0 is not a factor of 8 |
| `quiz[1].widget.options[1]` | wrong option: HCF 0, LCM 120. Why: 0 divides nothing. 1 divides every whole number, so the HCF is 1. | correct | gcd(8, 15) = 1, lcm = 120; 23 = 8 + 15; hcf cannot exceed 8; 0 is not a factor of 8 |
| `quiz[1].widget.options[2]` | wrong option: HCF 1, LCM 23. Why: You added 8 and 15. 23 is not a multiple of 8. | correct | gcd(8, 15) = 1, lcm = 120; 23 = 8 + 15; hcf cannot exceed 8; 0 is not a factor of 8 |
| `quiz[1].widget.options[3]` | wrong option: HCF 120, LCM 1. Why: You swapped them: the HCF cannot be bigger than 8. | correct | gcd(8, 15) = 1, lcm = 120; 23 = 8 + 15; hcf cannot exceed 8; 0 is not a factor of 8 |
| `quiz[2].widget.answer` | key 18 | correct | 6 divides 18 so lcm = 18; slips 108 = product, 6 = hcf |
| `quiz[2].widget.wrong[0]` | slip product = 108: 108 is $6 \times 18$. 18 is already a multiple of both. | correct | 6 divides 18 so lcm = 18; slips 108 = product, 6 = hcf |
| `quiz[2].widget.wrong[1]` | slip hcf = 6: 6 is the HCF here, not the LCM. | correct | 6 divides 18 so lcm = 18; slips 108 = product, 6 = hcf |
| `quiz[3].widget.options[0]` | keyed correct: $\dfrac{3}{4}$ | correct | 18/24 = 3/4 by hcf 6; 9/12, 6/8 not lowest; 72 = lcm |
| `quiz[3].widget.options[1]` | wrong option: $\dfrac{9}{12}$. Why: You divided by 2. Both still divide by 3. | correct | 18/24 = 3/4 by hcf 6; 9/12, 6/8 not lowest; 72 = lcm |
| `quiz[3].widget.options[2]` | wrong option: $\dfrac{6}{8}$. Why: You divided by 3. Both still divide by 2. | correct | 18/24 = 3/4 by hcf 6; 9/12, 6/8 not lowest; 72 = lcm |
| `quiz[3].widget.options[3]` | wrong option: $\dfrac{18}{72}$. Why: You used the LCM. Cancel by the HCF instead. | correct | 18/24 = 3/4 by hcf 6; 9/12, 6/8 not lowest; 72 = lcm |
| `screens[2].prose` | Definitions: LCM is the smallest number in both times tables; HCF is the biggest number dividing both | correct | Hardy and Wright sections 2.9 and 5.1 (greatest common divisor, least common multiple), positive multiples understood |
| `screens[3].prose` | Method: write the primes of each number with repeats; shared primes pair off into the overlap | correct | gcd takes the minimum exponent of each prime, lcm the maximum (Hardy and Wright section 5.1) |
| `screens[4].prose` | The LCM holds every prime of both; each prime appears only as often as one of them needs it | correct | maximum exponent rule |
| `screens[5].explain.text` | 7 and 10 share no prime, so no further cancelling is possible | correct | a/g and b/g are coprime when g = gcd(a, b) |
| `screens[6].prose` | "The LCM is the smallest piece size that works" for adding fractions | imprecise | Finding 4: 36 is the smallest denominator, so 36ths are the LARGEST common piece; 72nds are smaller and also work (script INFO) |
| `screens[6].explain.text` | "The LCM, 36, is the smallest piece size both fractions cut into" | imprecise | Finding 4, same statement |
| `screens[7].prose` | Euclid's method: take away as many of the smaller as fit; any number dividing both also divides what is left; repeat until nothing is left | correct | Euclid, Elements VII.2; Hardy and Wright section 12.3. Only one direction of the invariance is stated, enough at Stage 0 |
| `screens[7].explain.text` | The HCF is the last remainder before 0; then LCM = product / HCF | correct | Euclidean algorithm; gcd * lcm = ab |
| `screens[8].prose` | The HCF is never bigger than the smaller number; the LCM is never smaller than the larger | correct | a divisor of a is at most a; a positive multiple of b is at least b; checked to 300 in script |
| `screens[9].explain.text` | HCF * LCM equals the product of the two numbers | correct | min(e, f) + max(e, f) = e + f for each prime; checked to 300 in script |
| `summary.ideas[0]` | The HCF is the product of the primes two numbers share: the overlap | correct | minimum exponent rule, repeats included as screens[3] says |
| `summary.ideas[2]` | "the LCM is the smallest common piece size for adding" | imprecise | Finding 4, same statement |
| `summary.trap` | The product is a common multiple, not always the lowest: 12 * 18 = 216, LCM 36 | correct | lcm = product / gcd, equal to the product only for coprime numbers (quiz[1]) |
| `quiz[1].explain.text` | With no shared prime the HCF is 1 and the LCM is the product | correct | coprime case of gcd * lcm = ab |

## l17-around-and-inside

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `screens[0].widget.points[0].target` | target [6, 6] | correct | x(12 - x) is largest at x = 6 (script); 10*2 = 20, 5*7 = 35 |
| `screens[0].widget.wrong[0]` | wrong region long: 10 by 2 uses the same 24 metres but encloses only 20 square metres. | correct | x(12 - x) is largest at x = 6 (script); 10*2 = 20, 5*7 = 35 |
| `screens[0].widget.wrong[1]` | wrong region near: 5 by 7 encloses 35 square metres. One step further gives more. | correct | x(12 - x) is largest at x = 6 (script); 10*2 = 20, 5*7 = 35 |
| `screens[1].widget.rows[0][1].answer` | cell key 22 (Perimeter (m)) | correct | perimeter 2(8+3) = 22, area 8*3 = 24; slips 11 = 8+3, and the two measures swapped |
| `screens[1].widget.rows[0][1].wrong[0]` | slip half = 11: You added two sides. The fence goes all the way round: $8 + 3 + 8 + 3 = 22$. | correct | perimeter 2(8+3) = 22, area 8*3 = 24; slips 11 = 8+3, and the two measures swapped |
| `screens[1].widget.rows[0][1].wrong[1]` | slip gave-area = 24: 24 is the number of squares inside. The perimeter is the distance round. | correct | perimeter 2(8+3) = 22, area 8*3 = 24; slips 11 = 8+3, and the two measures swapped |
| `screens[1].widget.rows[1][1].answer` | cell key 24 (Area (m²)) | correct | perimeter 2(8+3) = 22, area 8*3 = 24; slips 11 = 8+3, and the two measures swapped |
| `screens[1].widget.rows[1][1].wrong[0]` | slip gave-perimeter = 22: 22 is the distance round. The area counts the squares inside. | correct | perimeter 2(8+3) = 22, area 8*3 = 24; slips 11 = 8+3, and the two measures swapped |
| `screens[1].widget.rows[1][1].wrong[1]` | slip added = 11: You added the sides. Area is 3 rows of 8: $3 \times 8 = 24$. | correct | perimeter 2(8+3) = 22, area 8*3 = 24; slips 11 = 8+3, and the two measures swapped |
| `screens[2].widget.answer` | key 20 m² | correct | half of 8*5 = 20; slips 40 = no half, 13 = 8+5 |
| `screens[2].widget.wrong[0]` | slip no-half = 40: 40 is the whole rectangle. The triangle fills half of it. | correct | half of 8*5 = 20; slips 40 = no half, 13 = 8+5 |
| `screens[2].widget.wrong[1]` | slip added = 13: You added the lengths. An area multiplies two lengths. | correct | half of 8*5 = 20; slips 40 = no half, 13 = 8+5 |
| `screens[3].widget.answer` | key 28 m² | correct | base 7 * height 4 = 28 (slant 5 from 3-4-5); slips 35 = 7*5, 14 = half, 16 = 7+5+4 |
| `screens[3].widget.wrong[0]` | slip slant = 35: You used the slant side, 5. The height is the dashed line at right angles to the base, 4. | correct | base 7 * height 4 = 28 (slant 5 from 3-4-5); slips 35 = 7*5, 14 = half, 16 = 7+5+4 |
| `screens[3].widget.wrong[1]` | slip half = 14: You halved it. A parallelogram is a whole rectangle after the slide, not half of one. | correct | base 7 * height 4 = 28 (slant 5 from 3-4-5); slips 35 = 7*5, 14 = half, 16 = 7+5+4 |
| `screens[3].widget.wrong[2]` | slip added = 16: You added the lengths. Multiply base by height. | correct | base 7 * height 4 = 28 (slant 5 from 3-4-5); slips 35 = 7*5, 14 = half, 16 = 7+5+4 |
| `screens[4].widget.answer` | key 32 m² | correct | (6+10)/2 * 4 = 32; slips 64 = no half, 240 = 10*6*4, 20 = 10+6+4 |
| `screens[4].widget.wrong[0]` | slip no-half = 64: 64 is two trapeziums together. Halve it. | correct | (6+10)/2 * 4 = 32; slips 64 = no half, 240 = 10*6*4, 20 = 10+6+4 |
| `screens[4].widget.wrong[1]` | slip all = 240: You multiplied all three lengths. An area uses two: the average width and the height. | correct | (6+10)/2 * 4 = 32; slips 64 = no half, 240 = 10*6*4, 20 = 10+6+4 |
| `screens[4].widget.wrong[2]` | slip added = 20: You added the lengths. Areas multiply. | correct | (6+10)/2 * 4 = 32; slips 64 = no half, 240 = 10*6*4, 20 = 10+6+4 |
| `screens[5].widget.answer` | key 48 m² | correct | 10*6 - 4*3 = 48 = 36 + 12; slips 60, 12, 72 = 60+12 |
| `screens[5].widget.wrong[0]` | slip whole = 60: 60 is the full rectangle. The corner is missing. | correct | 10*6 - 4*3 = 48 = 36 + 12; slips 60, 12, 72 = 60+12 |
| `screens[5].widget.wrong[1]` | slip corner = 12: 12 is the missing corner. Take it away from 60. | correct | 10*6 - 4*3 = 48 = 36 + 12; slips 60, 12, 72 = 60+12 |
| `screens[5].widget.wrong[2]` | slip added = 72: You added the corner. It is cut away, so subtract it. | correct | 10*6 - 4*3 = 48 = 36 + 12; slips 60, 12, 72 = 60+12 |
| `screens[6].widget.answer` | key 32 m | correct | 10+3+4+3+6+6 = 32 = 2(10+6); slips 25 = 32-7, 18 = 32-14, 48 = area, 46 = 32+14 |
| `screens[6].widget.wrong[0]` | slip subtracted = 25: You took the corner's two sides off 32. The notch puts two new sides back, 4 m and 3 m. | correct | 10+3+4+3+6+6 = 32 = 2(10+6); slips 25 = 32-7, 18 = 32-14, 48 = area, 46 = 32+14 |
| `screens[6].widget.wrong[1]` | slip corner = 18: You took the corner's whole perimeter off. The notch's inner sides are still part of the fence. | correct | 10+3+4+3+6+6 = 32 = 2(10+6); slips 25 = 32-7, 18 = 32-14, 48 = area, 46 = 32+14 |
| `screens[6].widget.wrong[2]` | slip area = 48: 48 is the area. The perimeter adds lengths round the edge. | correct | 10+3+4+3+6+6 = 32 = 2(10+6); slips 25 = 32-7, 18 = 32-14, 48 = area, 46 = 32+14 |
| `screens[6].widget.wrong[3]` | slip added = 46: You added the corner's perimeter on. Its outer sides are gone. | correct | 10+3+4+3+6+6 = 32 = 2(10+6); slips 25 = 32-7, 18 = 32-14, 48 = area, 46 = 32+14 |
| `screens[7].widget.answer` | key 10000 cm² | correct | 100 cm * 100 cm = 10,000 cm^2; slips 100 = linear scale, 1,000 |
| `screens[7].widget.wrong[0]` | slip linear = 100: You scaled once, as for a length. An area scales twice: $100 \times 100$. | correct | 100 cm * 100 cm = 10,000 cm^2; slips 100 = linear scale, 1,000 |
| `screens[7].widget.wrong[1]` | slip thousand = 1000: 1,000 has one zero too few. Each side is 100 cm, and $100 \times 100 = 10{,}000$. | correct | 100 cm * 100 cm = 10,000 cm^2; slips 100 = linear scale, 1,000 |
| `screens[8].widget.answer` | key 1.21 | correct | 1.1*1.1 = 1.21 (6,050/5,000); slips 1.2 = 6,000/5,000, 2.2 = 1.1+1.1, 1.1 |
| `screens[8].widget.wrong[0]` | slip corner = 1.2: You added the two strips but missed the corner, 100 extra shares times the extra £0.50. | correct | 1.1*1.1 = 1.21 (6,050/5,000); slips 1.2 = 6,000/5,000, 2.2 = 1.1+1.1, 1.1 |
| `screens[8].widget.wrong[1]` | slip added = 2.2: You added 1.1 and 1.1. Both sides grew, so multiply: $1.1 \times 1.1$. | correct | 1.1*1.1 = 1.21 (6,050/5,000); slips 1.2 = 6,000/5,000, 2.2 = 1.1+1.1, 1.1 |
| `screens[8].widget.wrong[2]` | slip once = 1.1: Only one side grew by 1.1 that way. Both sides grew, so multiply twice. | correct | 1.1*1.1 = 1.21 (6,050/5,000); slips 1.2 = 6,000/5,000, 2.2 = 1.1+1.1, 1.1 |
| `quiz[0].widget.answer` | key 30 cm² | correct | 10*6/2 = 30; slips 60, 16 = 10+6 |
| `quiz[0].widget.wrong[0]` | slip no-half = 60: 60 is the rectangle round it. The triangle is half. | correct | 10*6/2 = 30; slips 60, 16 = 10+6 |
| `quiz[0].widget.wrong[1]` | slip added = 16: You added. Area multiplies. | correct | 10*6/2 = 30; slips 60, 16 = 10+6 |
| `quiz[1].widget.answer` | key 22 m | correct | 2(7+4) = 22; slips 28 = area, 11 = 7+4 |
| `quiz[1].widget.wrong[0]` | slip area = 28: 28 is the area. The perimeter adds the sides. | correct | 2(7+4) = 22; slips 28 = area, 11 = 7+4 |
| `quiz[1].widget.wrong[1]` | slip half = 11: You added two sides. There are four. | correct | 2(7+4) = 22; slips 28 = area, 11 = 7+4 |
| `quiz[2].widget.answer` | key 81 m² | correct | 9 m sides: 81; slips 27 = 9*3, 12 = 9+3 |
| `quiz[2].widget.wrong[0]` | slip linear = 27: You scaled the area by 3. Areas scale by $3^2 = 9$. | correct | 9 m sides: 81; slips 27 = 9*3, 12 = 9+3 |
| `quiz[2].widget.wrong[1]` | slip added = 12: You added 3 to the area. Scaling multiplies. | correct | 9 m sides: 81; slips 27 = 9*3, 12 = 9+3 |
| `quiz[3].widget.answer` | key 45 cm² | correct | 9*5 = 45; slips 54 = 9*6, 22.5 = half |
| `quiz[3].widget.wrong[0]` | slip slant = 54: You used the slant side. The height is the 5 cm at right angles. | correct | 9*5 = 45; slips 54 = 9*6, 22.5 = half |
| `quiz[3].widget.wrong[1]` | slip half = 22.5: You halved it, as for a triangle. A parallelogram is a whole rectangle after a slide. | correct | 9*5 = 45; slips 54 = 9*6, 22.5 = half |
| `screens[1].prose` | Definitions: perimeter is the distance all the way round; area is how many 1 metre squares fit inside, in m² | correct | standard school definitions (Euclid I for rectilinear area by unit squares) |
| `screens[0].explain.text` | With a fixed perimeter the square encloses the most; perimeter and area are different measures | correct | xy with x + y = 12 is largest at x = y (AM-GM); script |
| `screens[1].explain.text` | Rule: area of a rectangle = length * width | correct | rows of unit squares |
| `screens[2].prose` | Definition: the height meets the base at a right angle | correct | Euclid VI def. 4 (altitude) |
| `screens[2].explain.text` | Rule: triangle area = half * base * height, because the triangle is half of each of two rectangles | correct | Euclid I.41; argument valid for an apex above the base, as drawn |
| `screens[3].explain.text` | Rule: parallelogram area = base * height, using the height not the slant side | correct | Euclid I.35 (shear to a rectangle) |
| `screens[4].prose` | Definition: "A trapezium has two parallel sides" | imprecise | Finding 8: no "four-sided" and no "one pair"; as worded it also fits a parallelogram or a hexagon. UK usage: a quadrilateral with one pair of parallel sides |
| `screens[4].explain.text` | Rule: trapezium area = average of the parallel sides * height, from two copies making a parallelogram | correct | two congruent trapezia form a parallelogram of base a + b |
| `screens[6].explain.text` | Cutting a rectangular corner out changes the area, not the perimeter | correct | the two removed outer edges reappear as the two inner edges of the notch |
| `screens[7].prose` | Scaling every side by k multiplies the perimeter by k and the area by k squared | correct | similarity: lengths scale by k, areas by k^2 (Euclid VI.19, VI.20) |
| `screens[7].explain.text` | 1 m² = 10,000 cm²; every unit change for an area squares the length scale | correct | (100 cm)^2 |
| `screens[8].explain.text` | Both sides growing by 1.1 gives 1.21, not 1.2: the corner is growth on growth | correct | (1 + x)^2 = 1 + 2x + x^2 |
| `summary.ideas[1]` | A triangle is half a rectangle; a parallelogram slides into one; a trapezium uses the average of its parallel sides | correct | as screens[2] to screens[4] |

## l18-circles-and-units

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `screens[0].widget.rows[0][3].answer` | cell key 3.14 (Coaster) | correct | 22/7 = 3.1429, 31.4/10 = 3.14, 62.8/20 = 3.14; slips 7/22 = 0.32, 31.4-10 = 21.4, 3.14/2 = 1.57 |
| `screens[0].widget.rows[0][3].wrong[0]` | slip upside = 0.32: You divided across by round. Put the distance round on top. | correct | 22/7 = 3.1429, 31.4/10 = 3.14, 62.8/20 = 3.14; slips 7/22 = 0.32, 31.4-10 = 21.4, 3.14/2 = 1.57 |
| `screens[0].widget.rows[1][3].answer` | cell key 3.14 (Plate) | correct | 22/7 = 3.1429, 31.4/10 = 3.14, 62.8/20 = 3.14; slips 7/22 = 0.32, 31.4-10 = 21.4, 3.14/2 = 1.57 |
| `screens[0].widget.rows[1][3].wrong[0]` | slip subtract = 21.4: You subtracted. Divide instead. | correct | 22/7 = 3.1429, 31.4/10 = 3.14, 62.8/20 = 3.14; slips 7/22 = 0.32, 31.4-10 = 21.4, 3.14/2 = 1.57 |
| `screens[0].widget.rows[2][3].answer` | cell key 3.14 (Tray) | correct | 22/7 = 3.1429, 31.4/10 = 3.14, 62.8/20 = 3.14; slips 7/22 = 0.32, 31.4-10 = 21.4, 3.14/2 = 1.57 |
| `screens[0].widget.rows[2][3].wrong[0]` | slip half = 1.57: You halved the answer, as if the tape went half way round. | correct | 22/7 = 3.1429, 31.4/10 = 3.14, 62.8/20 = 3.14; slips 7/22 = 0.32, 31.4-10 = 21.4, 3.14/2 = 1.57 |
| `screens[1].widget.answer` | key 157.1 cm | correct | 50 pi = 157.08; slips 25 pi = 78.54, 100 pi = 314.16, 625 pi = 1963.5; 3.14 and 22/7 answers accepted (script) |
| `screens[1].widget.wrong[0]` | slip radius = 78.5: You used half the diameter. The formula takes the full 50 cm across. | correct | 50 pi = 157.08; slips 25 pi = 78.54, 100 pi = 314.16, 625 pi = 1963.5; 3.14 and 22/7 answers accepted (script) |
| `screens[1].widget.wrong[1]` | slip doubled = 314.2: You used $2 \pi \times 50$, as if 50 cm were the radius. It is the diameter. | correct | 50 pi = 157.08; slips 25 pi = 78.54, 100 pi = 314.16, 625 pi = 1963.5; 3.14 and 22/7 answers accepted (script) |
| `screens[1].widget.wrong[2]` | slip area = 1963.5: That is an area, $\pi \times 25^2$. A distance round uses one length, not two multiplied. | correct | 50 pi = 157.08; slips 25 pi = 78.54, 100 pi = 314.16, 625 pi = 1963.5; 3.14 and 22/7 answers accepted (script) |
| `screens[2].widget.options[0]` | keyed correct: Half the circumference, $\pi \times$ radius | correct | wedge rearrangement: half the rim, pi r, along the top, height r, so area pi r^2 (Archimedes, Measurement of a Circle, Prop. 1) |
| `screens[2].widget.options[1]` | wrong option: The whole circumference, $2 \pi \times$ radius. Why: Only the arcs of the up wedges run along the top. Th… | correct | wedge rearrangement: half the rim, pi r, along the top, height r, so area pi r^2 (Archimedes, Measurement of a Circle, Prop. 1) |
| `screens[2].widget.options[2]` | wrong option: The diameter, $2 \times$ radius. Why: The top edge is made of arcs of the rim, not of radii. It is longer… | correct | wedge rearrangement: half the rim, pi r, along the top, height r, so area pi r^2 (Archimedes, Measurement of a Circle, Prop. 1) |
| `screens[2].widget.options[3]` | wrong option: The radius. Why: The radius is the height, the length of each wedge's straight side. | correct | wedge rearrangement: half the rim, pi r, along the top, height r, so area pi r^2 (Archimedes, Measurement of a Circle, Prop. 1) |
| `screens[3].widget.rows[0][1].answer` | cell key 30 (With $\pi \approx 3$) | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[0][1].wrong[0]` | slip one-r = 15: You used $\pi \times 5$. The circumference is $\pi \times$ diameter, and the diameter is 10. | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[0][2].answer` | cell key 75 (With $\pi \approx 3$) | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[0][2].wrong[0]` | slip d-sq = 300: You squared the diameter. Square the radius: $3 \times 25$. | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[0][2].wrong[1]` | slip 2r = 30: You multiplied by 2 instead of squaring: $5^2 = 25$, not 10. | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[1][1].answer` | cell key 31.42 (With $\pi$) | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[1][1].wrong[0]` | slip no-two = 15.71: You used $\pi \times 5$. The diameter is 10. | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[1][2].answer` | cell key 78.54 (With $\pi$) | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[1][2].wrong[0]` | slip diameter = 314.16: You squared the diameter. $\pi r^2$ uses the radius, 5. | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[3].widget.rows[1][2].wrong[1]` | slip swap = 31.42: That is the circumference. The area multiplies two lengths: $\pi \times 5 \times 5$. | correct | 2*3*5 = 30, 3*25 = 75, 10 pi = 31.42, 25 pi = 78.54; slips 15, 300, 30, 15.71, 314.16, 31.42 |
| `screens[4].widget.answer` | key 20.57 m | correct | 4 pi + 8 = 20.57; slips 4 pi = 12.57, 8 pi = 25.13, 4 pi + 4 = 16.57 |
| `screens[4].widget.wrong[0]` | slip no-edge = 12.57: You found the curve only. The fence also runs along the straight edge, 8 m. | correct | 4 pi + 8 = 20.57; slips 4 pi = 12.57, 8 pi = 25.13, 4 pi + 4 = 16.57 |
| `screens[4].widget.wrong[1]` | slip whole = 25.13: That is the whole circle's rim. The bed is half a circle. | correct | 4 pi + 8 = 20.57; slips 4 pi = 12.57, 8 pi = 25.13, 4 pi + 4 = 16.57 |
| `screens[4].widget.wrong[2]` | slip radius-edge = 16.57: You added the radius. The straight edge is the full diameter, 8 m. | correct | 4 pi + 8 = 20.57; slips 4 pi = 12.57, 8 pi = 25.13, 4 pi + 4 = 16.57 |
| `screens[5].widget.answer` | key 20 m/s | correct | 72*1000/3600 = 20; slips 72,000 (m/h), 1.2 (km/min), 259.2 (inverted), 0.02 (km/s) |
| `screens[5].widget.wrong[0]` | slip no-hours = 72000: That is metres an hour. Divide by the 3,600 seconds in an hour. | correct | 72*1000/3600 = 20; slips 72,000 (m/h), 1.2 (km/min), 259.2 (inverted), 0.02 (km/s) |
| `screens[5].widget.wrong[1]` | slip minutes = 1.2: You divided by 60 and stopped at kilometres a minute. | correct | 72*1000/3600 = 20; slips 72,000 (m/h), 1.2 (km/min), 259.2 (inverted), 0.02 (km/s) |
| `screens[5].widget.wrong[2]` | slip wrong-way = 259.2: You multiplied by 3,600 and divided by 1,000. Turn both round: multiply by 1,000, divide by 3,6… | correct | 72*1000/3600 = 20; slips 72,000 (m/h), 1.2 (km/min), 259.2 (inverted), 0.02 (km/s) |
| `screens[5].widget.wrong[3]` | slip no-km = 0.02: You divided by 3,600 but left kilometres. Multiply by 1,000 too. | correct | 72*1000/3600 = 20; slips 72,000 (m/h), 1.2 (km/min), 259.2 (inverted), 0.02 (km/s) |
| `screens[6].widget.rows[0][1].answer` | cell key 25000 ($2.5\ \text{m}^2$ in $\text{cm}^2$) | correct | 2.5*10,000 = 25,000; 2*3*4 = 24; slips 250, 2,500, 9 = 2+3+4, 52 = 2(6+8+12) |
| `screens[6].widget.rows[0][1].wrong[0]` | slip linear = 250: You multiplied by 100, as for a length. An area scales by $100 \times 100$. | correct | 2.5*10,000 = 25,000; 2*3*4 = 24; slips 250, 2,500, 9 = 2+3+4, 52 = 2(6+8+12) |
| `screens[6].widget.rows[0][1].wrong[1]` | slip thousand = 2500: You multiplied by 1,000. An area in cm² needs 10,000. | correct | 2.5*10,000 = 25,000; 2*3*4 = 24; slips 250, 2,500, 9 = 2+3+4, 52 = 2(6+8+12) |
| `screens[6].widget.rows[1][1].answer` | cell key 24 (Volume of the box in $\text{m}^3$) | correct | 2.5*10,000 = 25,000; 2*3*4 = 24; slips 250, 2,500, 9 = 2+3+4, 52 = 2(6+8+12) |
| `screens[6].widget.rows[1][1].wrong[0]` | slip added = 9: You added the sides. A volume multiplies three lengths. | correct | 2.5*10,000 = 25,000; 2*3*4 = 24; slips 250, 2,500, 9 = 2+3+4, 52 = 2(6+8+12) |
| `screens[6].widget.rows[1][1].wrong[1]` | slip surface = 52: 52 m² is the outside surface. The volume counts the 1 m cubes inside. | correct | 2.5*10,000 = 25,000; 2*3*4 = 24; slips 250, 2,500, 9 = 2+3+4, 52 = 2(6+8+12) |
| `screens[7].widget.answer` | key 78.54 m² | correct | radius 5: 25 pi = 78.54; slips 100 pi = 314.16, 10 pi = 31.42, 20 pi = 62.83 |
| `screens[7].widget.wrong[0]` | slip diameter = 314.16: Like the gardener, you used the diameter in $\pi r^2$. That is 4 times too big: use 5. | correct | radius 5: 25 pi = 78.54; slips 100 pi = 314.16, 10 pi = 31.42, 20 pi = 62.83 |
| `screens[7].widget.wrong[1]` | slip circumference = 31.42: That is the circumference, $10\pi$. An area multiplies two lengths, so it needs a square. | correct | radius 5: 25 pi = 78.54; slips 100 pi = 314.16, 10 pi = 31.42, 20 pi = 62.83 |
| `screens[7].widget.wrong[2]` | slip two-r = 62.83: You worked out $2 \times \pi \times 10$: the distance-round rule, with the diameter in place of the… | correct | radius 5: 25 pi = 78.54; slips 100 pi = 314.16, 10 pi = 31.42, 20 pi = 62.83 |
| `screens[8].widget.options[0]` | keyed correct: $25\pi$ | correct | 25 pi exact; 78.54 rounded; 10 pi circumference; 100 pi uses the diameter |
| `screens[8].widget.options[1]` | wrong option: $78.54$. Why: That is rounded to 2 decimal places, so it is not exact. | correct | 25 pi exact; 78.54 rounded; 10 pi circumference; 100 pi uses the diameter |
| `screens[8].widget.options[2]` | wrong option: $10\pi$. Why: That is the circumference, $2\pi \times 5$. | correct | 25 pi exact; 78.54 rounded; 10 pi circumference; 100 pi uses the diameter |
| `screens[8].widget.options[3]` | wrong option: $100\pi$. Why: You squared the diameter, 10. Square the radius. | correct | 25 pi exact; 78.54 rounded; 10 pi circumference; 100 pi uses the diameter |
| `screens[9].widget.rows[0][1].answer` | cell key 5000 (Per trading day) | correct | 1,260,000/252 = 5,000; /7.5 = 666.67; slips 1,260,000/365 = 3,452, 5,000/24 = 208, 5,000*7.5 = 37,500 |
| `screens[9].widget.rows[0][1].wrong[0]` | slip calendar = 3452: You divided by 365. The desk earns on its 252 trading days. | correct | 1,260,000/252 = 5,000; /7.5 = 666.67; slips 1,260,000/365 = 3,452, 5,000/24 = 208, 5,000*7.5 = 37,500 |
| `screens[9].widget.rows[1][1].answer` | cell key 667 (Per trading hour) | correct | 1,260,000/252 = 5,000; /7.5 = 666.67; slips 1,260,000/365 = 3,452, 5,000/24 = 208, 5,000*7.5 = 37,500 |
| `screens[9].widget.rows[1][1].wrong[0]` | slip clock = 208: You divided by 24. The desk trades 7.5 hours a day. | correct | 1,260,000/252 = 5,000; /7.5 = 666.67; slips 1,260,000/365 = 3,452, 5,000/24 = 208, 5,000*7.5 = 37,500 |
| `screens[9].widget.rows[1][1].wrong[1]` | slip times = 37500: You multiplied by 7.5. Going from a day to an hour divides. | correct | 1,260,000/252 = 5,000; /7.5 = 666.67; slips 1,260,000/365 = 3,452, 5,000/24 = 208, 5,000*7.5 = 37,500 |
| `quiz[0].widget.answer` | key 18.85 cm | correct | 6 pi = 18.85; slips 3 pi = 9.42, 9 pi = 28.27 |
| `quiz[0].widget.wrong[0]` | slip no-two = 9.42: You used $\pi \times 3$. The diameter is 6. | correct | 6 pi = 18.85; slips 3 pi = 9.42, 9 pi = 28.27 |
| `quiz[0].widget.wrong[1]` | slip area = 28.27: That is the area. The distance round uses one length. | correct | 6 pi = 18.85; slips 3 pi = 9.42, 9 pi = 28.27 |
| `quiz[1].widget.answer` | key 28.27 cm² | correct | 9 pi = 28.27; slips 36 pi = 113.1, 6 pi = 18.85 |
| `quiz[1].widget.wrong[0]` | slip diameter = 113.1: You squared the diameter. Square the radius, 3. | correct | 9 pi = 28.27; slips 36 pi = 113.1, 6 pi = 18.85 |
| `quiz[1].widget.wrong[1]` | slip circ = 18.85: That is the circumference. An area squares a length. | correct | 9 pi = 28.27; slips 36 pi = 113.1, 6 pi = 18.85 |
| `quiz[2].widget.answer` | key 25 m/s | correct | 90*1000/3600 = 25; slips 324, 90,000 |
| `quiz[2].widget.wrong[0]` | slip wrong-way = 324: You multiplied by 3,600 and divided by 1,000. Turn both round. | correct | 90*1000/3600 = 25; slips 324, 90,000 |
| `quiz[2].widget.wrong[1]` | slip no-hours = 90000: That is metres an hour. Divide by 3,600. | correct | 90*1000/3600 = 25; slips 324, 90,000 |
| `quiz[3].widget.options[0]` | keyed correct: Its decimal never ends and never repeats | correct | pi is irrational (Lambert 1761; Niven, Irrational Numbers, ch. 2), so its decimal neither ends nor repeats; 22/7 = 3.142857 recurring |
| `quiz[3].widget.options[1]` | wrong option: It equals $\tfrac{22}{7}$ exactly. Why: $\tfrac{22}{7} = 3.142857\ldots$ repeats; $\pi = 3.14159\ldots$ d… | correct | pi is irrational (Lambert 1761; Niven, Irrational Numbers, ch. 2), so its decimal neither ends nor repeats; 22/7 = 3.142857 recurring |
| `quiz[3].widget.options[2]` | wrong option: It equals 3.14 exactly. Why: 3.14 is $\pi$ rounded to 2 decimal places. | correct | pi is irrational (Lambert 1761; Niven, Irrational Numbers, ch. 2), so its decimal neither ends nor repeats; 22/7 = 3.142857 recurring |
| `quiz[3].widget.options[3]` | wrong option: Its decimal repeats, like $\tfrac{1}{3}$. Why: A repeating decimal is a fraction. $\pi$ is not a fraction… | correct | pi is irrational (Lambert 1761; Niven, Irrational Numbers, ch. 2), so its decimal neither ends nor repeats; 22/7 = 3.142857 recurring |
| `screens[0].explain.text` | Round divided by across is the same for every circle | correct | all circles are similar (Euclid XII.2 for areas; Archimedes, Measurement of a Circle, Prop. 3 bounds the ratio between 3 10/71 and 3 1/7) |
| `screens[1].prose` | Definitions: diameter is the distance across through the centre; circumference is the distance round; pi is their ratio; circumference = pi * diameter | correct | definition of pi |
| `screens[1].prose#2` | 22/7 = 3.142857... is a handy fraction; pi = 3.14159... never ends and never repeats | correct | pi irrational (Lambert 1761; Niven, Irrational Numbers, ch. 2); 22/7 - pi = 0.00126 |
| `screens[1].explain.text` | Definition: radius is the distance from the centre to the edge; diameter is twice the radius; C = 2 pi r | correct | definition |
| `screens[1].widget.accept` | Convention: 157 from pi = 3.14 is accepted alongside 157.1 | correct | tolerance 0.15; every pi item in the level accepts 3.14 and 22/7 answers rounded as asked (script, pi_item) |
| `screens[2].explain.text` | Area of a circle = pi r * r = pi r squared, from the wedge rectangle | correct | Archimedes, Measurement of a Circle, Prop. 1 (area equals half circumference times radius) |
| `screens[3].explain.text` | Estimates with pi = 3 are a little low, since pi is a little over 3 | correct | 3 < pi |
| `screens[5].prose` | Changing units multiplies by 1 written as a fraction of two equal amounts; unwanted units cancel | correct | factor-label method; 1,000 m = 1 km, 1 hour = 3,600 s |
| `screens[6].explain.text` | Length scales once, area twice, volume three times; volume of a cuboid = product of three sides | correct | (100)^1, (100)^2, (100)^3 |
| `screens[8].prose` | A multiple of pi such as 25 pi is exact; a decimal such as 78.54 is rounded | correct | pi irrational, so no finite decimal equals 25 pi |
| `screens[9].prose` | Conventions: 252 trading days a year, 7.5 trading hours a day (given) | correct | 252 is the standard count; 7.5 hours is a stated premise of the item, not a market fact, and is used consistently |
| `summary.ideas[0]` | pi is the distance round a circle divided by the distance across, about 3.14159, for every circle | correct | definition |
| `summary.ideas[2]` | To change units multiply by fractions worth 1; area scales the length factor twice, volume three times | correct | as screens[5] and screens[6] |
| `quiz[3].widget.options[3].why` | A repeating decimal is a fraction; pi is not a fraction of whole numbers | correct | recurring decimals are exactly the rationals (Hardy and Wright section 9.2); pi irrational |

## l19-one-number-for-many

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `screens[0].widget.points[0].target` | target [60, 0] | correct | sum 420, mean 60; distances below 140+120+20+20 = 300, above 60+240 = 300; at 40: 220 below, 360 above |
| `screens[0].widget.wrong[0]` | wrong region middle: At £40 the distance above is bigger than below. The £300 day pulls the balance higher. | correct | sum 420, mean 60; distances below 140+120+20+20 = 300, above 60+240 = 300; at 40: 220 below, 360 above |
| `screens[0].widget.wrong[1]` | wrong region centre-axis: That is the middle of the axis, not the balance point. Read the caption. | correct | sum 420, mean 60; distances below 140+120+20+20 = 300, above 60+240 = 300; at 40: 220 below, 360 above |
| `screens[1].widget.order` | order t2 t6 t3 t4 t7 t1 t5 | correct | -80 < -60 < 40 = 40 < 60 < 120 < 300 |
| `screens[2].widget.answer` | key regions d4 | correct | 4th of 7 sorted values is 40 |
| `screens[2].feedback.byKey.d5` | wrong tap: £60 is the mean. The middle day is the fourth of seven. | correct | 4th of 7 sorted values is 40 |
| `screens[2].feedback.byKey.d3` | wrong tap: That bar is third of seven. The middle is fourth, which also reads £40. | correct | 4th of 7 sorted values is 40 |
| `screens[2].feedback.byKey.d1` | wrong tap: That is the smallest day. Count three in from each end. | correct | 4th of 7 sorted values is 40 |
| `screens[3].widget.answer` | key 380 £ | correct | 300 - (-80) = 380; slips 220 = 300 - 80, 7 = count |
| `screens[3].widget.wrong[0]` | slip sign = 220: You worked out $300 - 80$. The smallest is $-80$, and taking away $-80$ adds 80. | correct | 300 - (-80) = 380; slips 220 = 300 - 80, 7 = count |
| `screens[3].widget.wrong[1]` | slip count = 7: 7 is the number of days. The range is a difference of profits. | correct | 300 - (-80) = 380; slips 220 = 300 - 80, 7 = count |
| `screens[4].widget.rows[0][1].answer` | cell key 460 (Mean) | correct | (420 + 2,800)/7 = 460; 4th sorted value still 40; slips 60, 3,220, 460, 3,100 |
| `screens[4].widget.rows[0][1].wrong[0]` | slip unchanged = 60: The mean uses every value, so changing one day changes it: $3{,}220 \div 7 = 460$. | correct | (420 + 2,800)/7 = 460; 4th sorted value still 40; slips 60, 3,220, 460, 3,100 |
| `screens[4].widget.rows[0][1].wrong[1]` | slip total = 3220: That is the new total. Share it over 7 days. | correct | (420 + 2,800)/7 = 460; 4th sorted value still 40; slips 60, 3,220, 460, 3,100 |
| `screens[4].widget.rows[1][1].answer` | cell key 40 (Median) | correct | (420 + 2,800)/7 = 460; 4th sorted value still 40; slips 60, 3,220, 460, 3,100 |
| `screens[4].widget.rows[1][1].wrong[0]` | slip moved = 460: The median is the middle day, not the mean. It is still the fourth day, £40. | correct | (420 + 2,800)/7 = 460; 4th sorted value still 40; slips 60, 3,220, 460, 3,100 |
| `screens[4].widget.rows[1][1].wrong[1]` | slip big = 3100: £3,100 is the largest day, not the middle one. | correct | (420 + 2,800)/7 = 460; 4th sorted value still 40; slips 60, 3,220, 460, 3,100 |
| `screens[5].widget.answer` | key 6.5 | correct | (5+8)/2 = 6.5; slips 5, 8, 13 |
| `screens[5].widget.wrong[0]` | slip lower = 5: 5 is the lower of the two middle values. Go halfway to 8. | correct | (5+8)/2 = 6.5; slips 5, 8, 13 |
| `screens[5].widget.wrong[1]` | slip upper = 8: 8 is the upper of the two middle values. Go halfway to 5. | correct | (5+8)/2 = 6.5; slips 5, 8, 13 |
| `screens[5].widget.wrong[2]` | slip no-half = 13: You added the middle two. Halve the sum. | correct | (5+8)/2 = 6.5; slips 5, 8, 13 |
| `screens[6].widget.rows[0][1].answer` | cell key 37 (Total trades) | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[0][1].wrong[0]` | slip added-values = 10: You added 0 to 4. Each count happens on several days: weight it. | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[0][1].wrong[1]` | slip days = 20: 20 is the number of days. Count the trades. | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[1][1].answer` | cell key 1.85 (Mean trades a day) | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[1][1].wrong[0]` | slip per-row = 7.4: You divided by the 5 rows. Divide by the 20 days. | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[1][1].wrong[1]` | slip freq-mean = 4: You averaged the bar heights. Divide the trades by the days. | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[2][1].answer` | cell key 2 (Median) | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[2][1].wrong[0]` | slip tallest = 8: 8 is the height of the tallest bar, a number of days. The median is a number of trades. | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[3][1].answer` | cell key 2 (Mode) | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[6].widget.rows[3][1].wrong[0]` | slip count = 8: 8 is how many days made 2 trades. The mode is the trade count itself, 2. | correct | n = 20, total 0+5+16+12+4 = 37, mean 1.85; 10th and 11th values are 2; mode 2; slips 10, 20, 37/5 = 7.4, 20/5 = 4, 8 |
| `screens[7].widget.answer` | key 180 £ | correct | 5*60 - (120-80+40+40) = 180; slips 60, 300, 4*60 - 120 = 120 |
| `screens[7].widget.wrong[0]` | slip mean = 60: £60 is the average. Friday must make up what the other four days lack. | correct | 5*60 - (120-80+40+40) = 180; slips 60, 300, 4*60 - 120 = 120 |
| `screens[7].widget.wrong[1]` | slip total = 300: £300 is the five-day total. Take away the four known days. | correct | 5*60 - (120-80+40+40) = 180; slips 60, 300, 4*60 - 120 = 120 |
| `screens[7].widget.wrong[2]` | slip four-days = 120: You used $4 \times 60 = 240$. The mean is over 5 days: $5 \times 60 = 300$. | correct | 5*60 - (120-80+40+40) = 180; slips 60, 300, 4*60 - 120 = 120 |
| `screens[8].widget.answer` | key 65000 £ | correct | (10*50,000 + 30*70,000)/40 = 65,000; slips 60,000 = mean of means, 120,000 = sum |
| `screens[8].widget.wrong[0]` | slip simple = 60000: Like the manager, you averaged the two averages. The bigger team counts three times as much. | correct | (10*50,000 + 30*70,000)/40 = 65,000; slips 60,000 = mean of means, 120,000 = sum |
| `screens[8].widget.wrong[1]` | slip added = 120000: You added the averages. Total the pay, then share it over 40. | correct | (10*50,000 + 30*70,000)/40 = 65,000; slips 60,000 = mean of means, 120,000 = sum |
| `screens[9].widget.answer` | key 1.1 | correct | 55,000/50,000 = 1.1; bars above 45,000 are 5,000 and 10,000, ratio 2 |
| `screens[9].widget.wrong[0]` | slip bars = 2: You compared the bar heights. The axis starts at £45,000, so the bars show only the part above it. | correct | 55,000/50,000 = 1.1; bars above 45,000 are 5,000 and 10,000, ratio 2 |
| `screens[10].widget.answer` | order share > write > add > zero > check | correct | sum of (x - mean) = sum x - n*mean = 0 (Freedman, Pisani and Purves, Statistics, ch. 4); only 120 and 300 exceed 60 |
| `screens[10].widget.lines[half]` | distractor (does not follow): So half the days lie above the mean. Why: That describes the median. Here only 2 of the 7… | correct | sum of (x - mean) = sum x - n*mean = 0 (Freedman, Pisani and Purves, Statistics, ch. 4); only 120 and 300 exceed 60 |
| `screens[11].widget.options[0]` | keyed correct: The median, £40 | correct | median 40 unaffected by the size of the top value; mean 3,220/7 = 460; range 3,100 + 80 = 3,180 |
| `screens[11].widget.options[1]` | wrong option: The mean, £460. Why: £460 is the mean the note quotes. Six of the seven days made far less: one day drags… | correct | median 40 unaffected by the size of the top value; mean 3,220/7 = 460; range 3,100 + 80 = 3,180 |
| `screens[11].widget.options[2]` | wrong option: The range, £3,180. Why: The range measures spread, not a typical day. | correct | median 40 unaffected by the size of the top value; mean 3,220/7 = 460; range 3,100 + 80 = 3,180 |
| `screens[11].widget.options[3]` | wrong option: The mean, £60. Why: £60 was the mean before the big day. This week's mean is £460. | correct | median 40 unaffected by the size of the top value; mean 3,220/7 = 460; range 3,100 + 80 = 3,180 |
| `quiz[0].widget.options[0]` | keyed correct: Both 3 and 7 | correct | 3 and 7 each occur twice; median 5; mean 36/7 = 5.14 |
| `quiz[0].widget.options[1]` | wrong option: There is no mode. Why: 3 and 7 each appear twice, more than any other value. | correct | 3 and 7 each occur twice; median 5; mean 36/7 = 5.14 |
| `quiz[0].widget.options[2]` | wrong option: 5. Why: 5 is the median, the middle value. | correct | 3 and 7 each occur twice; median 5; mean 36/7 = 5.14 |
| `quiz[0].widget.options[3]` | wrong option: About 5.14. Why: That is the mean, $36 \div 7$. | correct | 3 and 7 each occur twice; median 5; mean 36/7 = 5.14 |
| `quiz[1].widget.options[0]` | keyed correct: 6 trades were between 200 and 300 shares | correct | bins: 2, 3, 6, 2, 1; no value on a bin edge; largest value 410 |
| `quiz[1].widget.options[1]` | wrong option: 6 trades were exactly 250 shares. Why: A histogram bar covers a range of sizes, not one size. | correct | bins: 2, 3, 6, 2, 1; no value on a bin edge; largest value 410 |
| `quiz[1].widget.options[2]` | wrong option: The biggest trade was 300 shares. Why: The height counts trades; the biggest trade, 410, is in the last b… | correct | bins: 2, 3, 6, 2, 1; no value on a bin edge; largest value 410 |
| `quiz[1].widget.options[3]` | wrong option: 6 shares were traded in all. Why: The height counts trades, not shares. | correct | bins: 2, 3, 6, 2, 1; no value on a bin edge; largest value 410 |
| `quiz[2].widget.answer` | key 20 £ | correct | (-20+50+10-40+100)/5 = 20; slips 220/5 = 44, 100 |
| `quiz[2].widget.wrong[0]` | slip ignored-signs = 44: You added the losses as gains. $-20$ and $-40$ lower the total. | correct | (-20+50+10-40+100)/5 = 20; slips 220/5 = 44, 100 |
| `quiz[2].widget.wrong[1]` | slip total = 100: £100 is the total. Share it over 5 days. | correct | (-20+50+10-40+100)/5 = 20; slips 220/5 = 44, 100 |
| `quiz[3].widget.answer` | key 70 £ | correct | 40 - (-30) = 70; slips 40 - 30 = 10, 25 - (-15) = 40 |
| `quiz[3].widget.wrong[0]` | slip sign = 10: You worked out $40 - 30$. The smallest is $-30$; taking it away adds 30. | correct | 40 - (-30) = 70; slips 40 - 30 = 10, 25 - (-15) = 40 |
| `quiz[3].widget.wrong[1]` | slip first-last = 40: You used the first and last values listed. Use the largest and smallest. | correct | 40 - (-30) = 70; slips 40 - 30 = 10, 25 - (-15) = 40 |
| `quiz[4].widget.answer` | key 30 £ | correct | sorted -20, 10, 30, 70, 90: median 30; slips 10 = middle as written, 180/5 = 36 |
| `quiz[4].widget.wrong[0]` | slip unsorted = 10: 10 is the middle of the list as written. Sort first: $-20$, 10, 30, 70, 90. | correct | sorted -20, 10, 30, 70, 90: median 30; slips 10 = middle as written, 180/5 = 36 |
| `quiz[4].widget.wrong[1]` | slip mean = 36: 36 is the mean, $180 \div 5$. The median is the middle value after sorting. | correct | sorted -20, 10, 30, 70, 90: median 30; slips 10 = middle as written, 180/5 = 36 |
| `screens[0].explain.text` | The balance point is the share each day would get: total 420 over 7 days is 60 | correct | sum of deviations from the mean is zero |
| `screens[2].prose` | Definition: the mean is the total shared equally | correct | Freedman, Pisani and Purves, Statistics, ch. 4 section 1 |
| `screens[3].prose` | Definitions: median is the middle value of a sorted list; mode is the most common value; range is largest minus smallest and measures spread | correct | Freedman, Pisani and Purves ch. 4; UK GCSE conventions for mode and range |
| `screens[4].explain.text` | "One extreme day, an outlier, moves the mean a lot and the median not at all" | imprecise | Finding 5: exact when an existing extreme value is made more extreme (script), but an added outlier does move the median (2, 3, 4 to 2, 3, 4, 100: 3 to 3.5) |
| `screens[5].prose` | Convention: with an even count the median is the mean of the middle two | correct | standard convention (Freedman, Pisani and Purves ch. 4), stated before it is graded |
| `screens[5].explain.text` | A median or mean need not be a possible value | correct | 6.5 trades |
| `screens[6].feedback.correct` | In a frequency table the median comes from counting days, not rows | correct | the table stands for 20 values; 10th and 11th |
| `screens[8].explain.text` | Averaging two averages gives the small team as much weight as the big one | correct | overall mean = weighted mean with weights 10 and 30 |
| `screens[9].explain.text` | A cut-off axis makes small changes look big | correct | bar heights above 45,000 are in ratio 2 while the values are in ratio 1.1 (Tufte, The Visual Display of Quantitative Information, ch. 2, lie factor) |
| `screens[10].widget.lines[half].why` | "Half the days above" describes the median, not the mean | correct | at most half the values lie above the median; here 2 of 7 lie above the mean |
| `screens[11].explain.text` | The median says what a typical day looked like when one day drags the mean | correct | median is resistant to the size of extreme values (Freedman, Pisani and Purves ch. 4 section 3) |
| `summary.ideas[0]` | The mean shares the total equally and is the balance point; one extreme value can drag it far | correct | as screens[0], screens[4] |
| `summary.ideas[2]` | A frequency table weights each value by its count | correct | mean = sum(x f)/sum(f) |
| `quiz[0].explain.text` | Convention: two values tied for most common are both modes; a list where every value appears once has no mode | correct | UK school convention, stated in the item; the wrong option "no mode" is wrong under every convention in use for 2, 3, 3, 5, 7, 7, 9 |
| `quiz[1].explain.text` | In a histogram a bar covers a range and its height counts the values in it | correct | equal-width bins, so height is frequency |

## review-4

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `items[0].widget.options[0]` | keyed correct: $2^2 \times 3^2 \times 5$ | correct | 180 = 4*45 = 2^2*3^2*5; 2^3*3*5 = 120; 2*3^2*5 = 90 |
| `items[0].widget.options[1]` | wrong option: $2^3 \times 3 \times 5$. Why: That is $8 \times 15 = 120$. Count the 3s in 180 again. | correct | 180 = 4*45 = 2^2*3^2*5; 2^3*3*5 = 120; 2*3^2*5 = 90 |
| `items[0].widget.options[2]` | wrong option: $4 \times 9 \times 5$. Why: That equals 180, but 4 and 9 are not prime. | correct | 180 = 4*45 = 2^2*3^2*5; 2^3*3*5 = 120; 2*3^2*5 = 90 |
| `items[0].widget.options[3]` | wrong option: $2 \times 3^2 \times 5$. Why: That is 90. 180 has two 2s. | correct | 180 = 4*45 = 2^2*3^2*5; 2^3*3*5 = 120; 2*3^2*5 = 90 |
| `items[1].widget.answer` | key 18 | correct | 3*3*2 = 18; slips 4 = 2*2*1, 8 = 3+3+2 |
| `items[1].widget.wrong[0]` | slip no-plus-one = 4: You multiplied the indices, $2 \times 2 \times 1$. Add 1 to each first. | correct | 3*3*2 = 18; slips 4 = 2*2*1, 8 = 3+3+2 |
| `items[1].widget.wrong[1]` | slip added = 8: You added the choices. Multiply them. | correct | 3*3*2 = 18; slips 4 = 2*2*1, 8 = 3+3+2 |
| `items[2].widget.answer` | key 180 | correct | lcm(36, 60) = 180; slips 2,160 = product, 12 = hcf, 360 = 2^3*3^2*5 |
| `items[2].widget.wrong[0]` | slip product = 2160: $36 \times 60$ counts the shared $2^2 \times 3$ twice. | correct | lcm(36, 60) = 180; slips 2,160 = product, 12 = hcf, 360 = 2^3*3^2*5 |
| `items[2].widget.wrong[1]` | slip hcf = 12: 12 is the HCF, the shared part only. | correct | lcm(36, 60) = 180; slips 2,160 = product, 12 = hcf, 360 = 2^3*3^2*5 |
| `items[2].widget.wrong[2]` | slip big-only = 360: You took three 2s. Neither number has more than two. | correct | lcm(36, 60) = 180; slips 2,160 = product, 12 = hcf, 360 = 2^3*3^2*5 |
| `items[3].widget.options[0]` | keyed correct: $\dfrac{5}{7}$ | correct | 30/42 = 5/7 by hcf 6; 15/21, 10/14 not lowest; 1/7 = 30/30 over 42/6 |
| `items[3].widget.options[1]` | wrong option: $\dfrac{15}{21}$. Why: You divided by 2. Both still divide by 3. | correct | 30/42 = 5/7 by hcf 6; 15/21, 10/14 not lowest; 1/7 = 30/30 over 42/6 |
| `items[3].widget.options[2]` | wrong option: $\dfrac{10}{14}$. Why: You divided by 3. Both still divide by 2. | correct | 30/42 = 5/7 by hcf 6; 15/21, 10/14 not lowest; 1/7 = 30/30 over 42/6 |
| `items[3].widget.options[3]` | wrong option: $\dfrac{1}{7}$. Why: You divided the bottom by 6 but the top by 30. Divide both by 6. | correct | 30/42 = 5/7 by hcf 6; 15/21, 10/14 not lowest; 1/7 = 30/30 over 42/6 |
| `items[4].widget.answer` | key 34 m² | correct | 8*5 - 3*2 = 34; slips 40, 6, 46 |
| `items[4].widget.wrong[0]` | slip whole = 40: 40 is the full rectangle. The corner is cut away. | correct | 8*5 - 3*2 = 34; slips 40, 6, 46 |
| `items[4].widget.wrong[1]` | slip corner = 6: 6 is the corner. Take it away from 40. | correct | 8*5 - 3*2 = 34; slips 40, 6, 46 |
| `items[4].widget.wrong[2]` | slip added = 46: You added the corner. It is missing, so subtract. | correct | 8*5 - 3*2 = 34; slips 40, 6, 46 |
| `items[5].widget.answer` | key 42 cm² | correct | 12*7/2 = 42; slips 84, 12*9/2 = 54 |
| `items[5].widget.wrong[0]` | slip no-half = 84: 84 is the rectangle round it. Halve it. | correct | 12*7/2 = 42; slips 84, 12*9/2 = 54 |
| `items[5].widget.wrong[1]` | slip slant = 54: You used the slant side, 9 cm. Use the height, 7 cm. | correct | 12*7/2 = 42; slips 84, 12*9/2 = 54 |
| `items[6].widget.answer` | key 153.94 cm² | correct | 49 pi = 153.94; slips 196 pi = 615.75, 14 pi = 43.98; 3.14 and 22/7 answers accepted (script) |
| `items[6].widget.wrong[0]` | slip diameter = 615.75: You squared the diameter. The radius is 7. | correct | 49 pi = 153.94; slips 196 pi = 615.75, 14 pi = 43.98; 3.14 and 22/7 answers accepted (script) |
| `items[6].widget.wrong[1]` | slip circ = 43.98: That is the circumference, $14\pi$. An area squares a length. | correct | 49 pi = 153.94; slips 196 pi = 615.75, 14 pi = 43.98; 3.14 and 22/7 answers accepted (script) |
| `items[7].widget.answer` | key 15 m/s | correct | 54*1000/3600 = 15; slips 194.4, 54,000 |
| `items[7].widget.wrong[0]` | slip wrong-way = 194.4: You multiplied by 3,600 and divided by 1,000. Turn both round. | correct | 54*1000/3600 = 15; slips 194.4, 54,000 |
| `items[7].widget.wrong[1]` | slip no-hours = 54000: That is metres an hour. Divide by 3,600. | correct | 54*1000/3600 = 15; slips 194.4, 54,000 |
| `items[8].widget.answer` | key 1.1 | correct | (0*3+1*4+2*2+3*1)/10 = 1.1; slips 11/4 = 2.75, 6/4 = 1.5 |
| `items[8].widget.wrong[0]` | slip per-row = 2.75: You divided by the 4 rows. Divide by the 10 days. | correct | (0*3+1*4+2*2+3*1)/10 = 1.1; slips 11/4 = 2.75, 6/4 = 1.5 |
| `items[8].widget.wrong[1]` | slip values = 1.5: You averaged 0, 1, 2, 3 without their days. | correct | (0*3+1*4+2*2+3*1)/10 = 1.1; slips 11/4 = 2.75, 6/4 = 1.5 |
| `items[9].widget.answer` | key 38 £ | correct | (6*50 - 110)/5 = 38; slips 190/6 = 31.67, 50, 410/5 = 82 |
| `items[9].widget.wrong[0]` | slip six = 31.67: You still divided by 6. Five days are left. | correct | (6*50 - 110)/5 = 38; slips 190/6 = 31.67, 50, 410/5 = 82 |
| `items[9].widget.wrong[1]` | slip unchanged = 50: Removing a day above the mean lowers the mean. | correct | (6*50 - 110)/5 = 38; slips 190/6 = 31.67, 50, 410/5 = 82 |
| `items[9].widget.wrong[2]` | slip added = 82: You added the £110 instead of taking it away: $(300 + 110) \div 5 = 82$. | correct | (6*50 - 110)/5 = 38; slips 190/6 = 31.67, 50, 410/5 = 82 |
| `items[2].explain.text` | HCF is the shared part, LCM takes every prime as often as needed; 12 * 180 = 36 * 60 | correct | min and max exponent rules |
| `items[9].feedback.byKey.unchanged` | Removing a value above the mean lowers the mean | correct | new mean = (n*m - x)/(n - 1) < m exactly when x > m |

## homework-4

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `items[0].parts[0].widget.options[0]` | keyed correct: $2 \times 3^2 \times 7$ | correct | 126 = 2*63 = 2*3^2*7; 2^2*3*7 = 84; 2*3^3*7 = 378 |
| `items[0].parts[0].widget.options[1]` | wrong option: $2^2 \times 3 \times 7$. Why: That is 84. 126 has one 2 and two 3s. | correct | 126 = 2*63 = 2*3^2*7; 2^2*3*7 = 84; 2*3^3*7 = 378 |
| `items[0].parts[0].widget.options[2]` | wrong option: $2 \times 9 \times 7$. Why: That equals 126, but 9 is not prime. | correct | 126 = 2*63 = 2*3^2*7; 2^2*3*7 = 84; 2*3^3*7 = 378 |
| `items[0].parts[0].widget.options[3]` | wrong option: $2 \times 3^3 \times 7$. Why: That is 378. Count the 3s again. | correct | 126 = 2*63 = 2*3^2*7; 2^2*3*7 = 84; 2*3^3*7 = 378 |
| `items[0].parts[1].widget.answer` | key 18 | correct | hcf(90, 126) = 2*3^2 = 18; slips 6, 630 = lcm, 2 |
| `items[0].parts[1].widget.wrong[0]` | slip one-three = 6: You shared one 3. Both numbers have two. | correct | hcf(90, 126) = 2*3^2 = 18; slips 6, 630 = lcm, 2 |
| `items[0].parts[1].widget.wrong[1]` | slip lcm = 630: 630 is the LCM. | correct | hcf(90, 126) = 2*3^2 = 18; slips 6, 630 = lcm, 2 |
| `items[0].parts[1].widget.wrong[2]` | slip two = 2: You shared only the 2. They share two 3s as well. | correct | hcf(90, 126) = 2*3^2 = 18; slips 6, 630 = lcm, 2 |
| `items[0].parts[2].widget.answer` | key 630 | correct | lcm = 2*3^2*5*7 = 630; slips 11,340 = product, 18, 210 = 2*3*5*7 |
| `items[0].parts[2].widget.wrong[0]` | slip product = 11340: $90 \times 126$ counts the shared 18 twice. Divide by 18. | correct | lcm = 2*3^2*5*7 = 630; slips 11,340 = product, 18, 210 = 2*3*5*7 |
| `items[0].parts[2].widget.wrong[1]` | slip hcf = 18: 18 is the HCF. | correct | lcm = 2*3^2*5*7 = 630; slips 11,340 = product, 18, 210 = 2*3*5*7 |
| `items[0].parts[2].widget.wrong[2]` | slip missed = 210: You took one 3. Both numbers need two. | correct | lcm = 2*3^2*5*7 = 630; slips 11,340 = product, 18, 210 = 2*3*5*7 |
| `items[1].parts[0].widget.answer` | key 74.14 m² | correct | 60 + 4.5 pi = 74.14; slips 60 + 9 pi = 88.27, 60 + 18 pi = 116.55, 60 |
| `items[1].parts[0].widget.wrong[0]` | slip full-circle = 88.27: You added a whole circle. Only half of it is there. | correct | 60 + 4.5 pi = 74.14; slips 60 + 9 pi = 88.27, 60 + 18 pi = 116.55, 60 |
| `items[1].parts[0].widget.wrong[1]` | slip diameter = 116.55: You used 6 as the radius. The semicircle's diameter is 6, so its radius is 3. | correct | 60 + 4.5 pi = 74.14; slips 60 + 9 pi = 88.27, 60 + 18 pi = 116.55, 60 |
| `items[1].parts[0].widget.wrong[2]` | slip rect = 60: 60 is the rectangle alone. | correct | 60 + 4.5 pi = 74.14; slips 60 + 9 pi = 88.27, 60 + 18 pi = 116.55, 60 |
| `items[1].parts[1].widget.answer` | key 35.42 m | correct | 26 + 3 pi = 35.42; slips 41.42 = +6, 26 + 6 pi = 44.85, 26 |
| `items[1].parts[1].widget.wrong[0]` | slip shared = 41.42: You counted the dashed 6 m side. It is inside the lawn, not on its edge. | correct | 26 + 3 pi = 35.42; slips 41.42 = +6, 26 + 6 pi = 44.85, 26 |
| `items[1].parts[1].widget.wrong[1]` | slip full = 44.85: You used a full circle's rim. Only half is on the edge. | correct | 26 + 3 pi = 35.42; slips 41.42 = +6, 26 + 6 pi = 44.85, 26 |
| `items[1].parts[1].widget.wrong[2]` | slip no-arc = 26: You left out the curved edge, $3\pi$. | correct | 26 + 3 pi = 35.42; slips 41.42 = +6, 26 + 6 pi = 44.85, 26 |
| `items[2].widget.answer` | key 126 km/h | correct | 35*3600/1000 = 126; slips 9.72, 35*60/1000 = 2.1, 126,000 |
| `items[2].widget.wrong[0]` | slip wrong-way = 9.72: You divided by 3,600 and multiplied by 1,000. Turn both round. | correct | 35*3600/1000 = 126; slips 9.72, 35*60/1000 = 2.1, 126,000 |
| `items[2].widget.wrong[1]` | slip minutes = 2.1: You multiplied by 60 only: that is km a minute. | correct | 35*3600/1000 = 126; slips 9.72, 35*60/1000 = 2.1, 126,000 |
| `items[2].widget.wrong[2]` | slip no-km = 126000: That is metres an hour. Divide by 1,000. | correct | 35*3600/1000 = 126; slips 9.72, 35*60/1000 = 2.1, 126,000 |
| `items[3].parts[0].widget.answer` | key 2.6 | correct | (3+12+21+16)/20 = 2.6; slips 52/4 = 13, 2.5, 20/4 = 5 |
| `items[3].parts[0].widget.wrong[0]` | slip per-row = 13: You divided 52 by the 4 rows. Divide by the 20 hours. | correct | (3+12+21+16)/20 = 2.6; slips 52/4 = 13, 2.5, 20/4 = 5 |
| `items[3].parts[0].widget.wrong[1]` | slip values = 2.5: You averaged 1, 2, 3, 4 without their hours. | correct | (3+12+21+16)/20 = 2.6; slips 52/4 = 13, 2.5, 20/4 = 5 |
| `items[3].parts[0].widget.wrong[2]` | slip hours = 5: You averaged the hours column, $20 \div 4$. | correct | (3+12+21+16)/20 = 2.6; slips 52/4 = 13, 2.5, 20/4 = 5 |
| `items[3].parts[1].widget.answer` | key 3 | correct | cumulative 3, 9, 16: 10th and 11th are 3; slips 2.5, 7 |
| `items[3].parts[1].widget.wrong[0]` | slip middle-row = 2.5: You went halfway between the middle two rows. Count hours, not rows. | correct | cumulative 3, 9, 16: 10th and 11th are 3; slips 2.5, 7 |
| `items[3].parts[1].widget.wrong[1]` | slip tallest = 7: 7 is a number of hours. The median is a number of orders. | correct | cumulative 3, 9, 16: 10th and 11th are 3; slips 2.5, 7 |
| `items[4].widget.answer` | key 39000 £ | correct | (8*45,000 - 87,000)/7 = 39,000; slips 45,000, 273,000/8 = 34,125, 360,000/7 = 51,429 |
| `items[4].widget.wrong[0]` | slip unchanged = 45000: Removing a bonus above the mean lowers the mean. | correct | (8*45,000 - 87,000)/7 = 39,000; slips 45,000, 273,000/8 = 34,125, 360,000/7 = 51,429 |
| `items[4].widget.wrong[1]` | slip eight = 34125: You still divided by 8. Seven traders are left. | correct | (8*45,000 - 87,000)/7 = 39,000; slips 45,000, 273,000/8 = 34,125, 360,000/7 = 51,429 |
| `items[4].widget.wrong[2]` | slip old-total = 51429: You divided the old total by 7. Take the £87,000 out first. | correct | (8*45,000 - 87,000)/7 = 39,000; slips 45,000, 273,000/8 = 34,125, 360,000/7 = 51,429 |
| `items[5].widget.answer` | order s1 > s2 > s3 > s4 > s5 | correct | Euclid: 1071 = 2*462 + 147, 462 = 3*147 + 21, 147 = 7*21; 1071 = 21*51, 462 = 21*22; lcm 23,562 (script) |
| `items[5].widget.lines[bad]` | distractor (does not follow): The first remainder is 147, so the HCF of 1,071 and 462 is 147. Why: 147 does not divide … | correct | Euclid: 1071 = 2*462 + 147, 462 = 3*147 + 21, 147 = 7*21; 1071 = 21*51, 462 = 21*22; lcm 23,562 (script) |
| `items[6].model` | model answer: mean 35, median 20, axis from 15 makes 1.15 times look 1.6 times | correct | sum 420, mean 35; sorted 6th and 7th both 20; 23/20 = 1.15, 8/5 = 1.6; 220/11 = 20 |
| `items[6].rubric[0]` | rubric: Explains that an axis starting at £15,000 exaggerates differences between months, with an example from the figu… | correct | sum 420, mean 35; sorted 6th and 7th both 20; 23/20 = 1.15, 8/5 = 1.6; 220/11 = 20 |
| `items[6].rubric[1]` | rubric: Checks the mean: a total of £420,000 over 12 months gives £35,000. | correct | sum 420, mean 35; sorted 6th and 7th both 20; 23/20 = 1.15, 8/5 = 1.6; 220/11 = 20 |
| `items[6].rubric[2]` | rubric: Names December's £200,000, about ten times a usual month, as the value that pulls the mean up. | correct | sum 420, mean 35; sorted 6th and 7th both 20; 23/20 = 1.15, 8/5 = 1.6; 220/11 = 20 |
| `items[6].rubric[3]` | rubric: Sorts the twelve values and takes the mean of the 6th and 7th to get a median of £20,000. | correct | sum 420, mean 35; sorted 6th and 7th both 20; 23/20 = 1.15, 8/5 = 1.6; 220/11 = 20 |
| `items[6].rubric[4]` | rubric: Writes an honest description using the median, the usual range of months and the outlier, with an axis from £0. | correct | sum 420, mean 35; sorted 6th and 7th both 20; 23/20 = 1.15, 8/5 = 1.6; 220/11 = 20 |
| `items[6].rubric[5]` | rubric: Says what the mean does answer: the year's total shared over twelve months. | correct | sum 420, mean 35; sorted 6th and 7th both 20; 23/20 = 1.15, 8/5 = 1.6; 220/11 = 20 |
| `items[7].widget.answer` | key 48 | correct | 2520 = lcm(1..10) = 2^3*3^2*5*7; 4*3*2*2 = 48; slips 7 = 3+2+1+1, 6 = 3*2*1*1, 11 = 4+3+2+2 |
| `items[7].widget.wrong[0]` | slip added = 7: You added the indices. Add 1 to each, then multiply. | correct | 2520 = lcm(1..10) = 2^3*3^2*5*7; 4*3*2*2 = 48; slips 7 = 3+2+1+1, 6 = 3*2*1*1, 11 = 4+3+2+2 |
| `items[7].widget.wrong[1]` | slip no-plus-one = 6: You multiplied the indices. Add 1 to each first. | correct | 2520 = lcm(1..10) = 2^3*3^2*5*7; 4*3*2*2 = 48; slips 7 = 3+2+1+1, 6 = 3*2*1*1, 11 = 4+3+2+2 |
| `items[7].widget.wrong[2]` | slip added-plus = 11: You added the choices. Multiply them. | correct | 2520 = lcm(1..10) = 2^3*3^2*5*7; 4*3*2*2 = 48; slips 7 = 3+2+1+1, 6 = 3*2*1*1, 11 = 4+3+2+2 |
| `items[5].explain.text` | Each Euclid step keeps every common factor, because what divides both numbers divides the remainder | correct | d divides a and b implies d divides a - qb |
| `items[6].model#2` | The mean is right for the year's total spread over twelve months; the median for a usual month | correct | 12 * 35,000 = 420,000; median 20,000 |
| `items[7].prose` | 2,520 is the smallest number that every whole number from 1 to 10 divides | correct | lcm(1..10) = 2^3 * 3^2 * 5 * 7 (script) |

## problems-4

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `items[0].parts[0].widget.answer` | key 120 cm | correct | 360 = 2^3*3^2*5, 600 = 2^3*3*5^2, hcf 120; slips 1,800 = lcm, 24 = 2^3*3 |
| `items[0].parts[0].widget.wrong[0]` | slip lcm = 1800: 1,800 is the LCM, a multiple of both lengths. The tile side must divide both, so use the shared primes. | correct | 360 = 2^3*3^2*5, 600 = 2^3*3*5^2, hcf 120; slips 1,800 = lcm, 24 = 2^3*3 |
| `items[0].parts[0].widget.wrong[1]` | slip missing-prime = 24: 24 divides both, but you left out the shared 5. Multiply every shared prime: $2^3 \times 3 \ti… | correct | 360 = 2^3*3^2*5, 600 = 2^3*3*5^2, hcf 120; slips 1,800 = lcm, 24 = 2^3*3 |
| `items[0].parts[1].widget.answer` | key 16 | correct | d(120) = 4*2*2 = 16; slips 3 = 3*1*1, 8 = 4+2+2, 36 = d(1,800) |
| `items[0].parts[1].widget.wrong[0]` | slip indices-multiplied = 3: You multiplied the indices, $3 \times 1 \times 1$. Add 1 to each first, because the power … | correct | d(120) = 4*2*2 = 16; slips 3 = 3*1*1, 8 = 4+2+2, 36 = d(1,800) |
| `items[0].parts[1].widget.wrong[1]` | slip indices-added = 8: You added the choices, $4 + 2 + 2$. Every choice of 2s goes with every choice of 3s and 5s, so … | correct | d(120) = 4*2*2 = 16; slips 3 = 3*1*1, 8 = 4+2+2, 36 = d(1,800) |
| `items[0].parts[1].widget.wrong[2]` | slip lcm-carried = 36: 36 counts the factors of 1,800, the LCM. The sides that fit are the factors of 120. | correct | d(120) = 4*2*2 = 16; slips 3 = 3*1*1, 8 = 4+2+2, 36 = d(1,800) |
| `items[0].parts[2].widget.answer` | key 15 | correct | 3*5 = 15; slips 8 = 3+5, 375 = 15*25 for 24 cm tiles |
| `items[0].parts[2].widget.wrong[0]` | slip rows-added = 8: 3 across and 5 along make a grid, so multiply: $3 \times 5 = 15$. | correct | 3*5 = 15; slips 8 = 3+5, 375 = 15*25 for 24 cm tiles |
| `items[0].parts[2].widget.wrong[1]` | slip small-tile-carried = 375: 375 is the count for 24 cm tiles. With 120 cm tiles it is $3 \times 5$. | correct | 3*5 = 15; slips 8 = 3+5, 375 = 15*25 for 24 cm tiles |
| `items[0].parts[3].widget.answer` | key 21.6 m² | correct | 15*14,400 = 216,000 cm^2 = 21.6 m^2 = 3.6*6; slips 2,160, 216,000 |
| `items[0].parts[3].widget.wrong[0]` | slip hundred = 2160: You divided by 100. A square metre is 100 cm by 100 cm, which is 10,000 cm². | correct | 15*14,400 = 216,000 cm^2 = 21.6 m^2 = 3.6*6; slips 2,160, 216,000 |
| `items[0].parts[3].widget.wrong[1]` | slip cm-squared = 216000: 216,000 is in square centimetres. Divide by 10,000 for square metres. | correct | 15*14,400 = 216,000 cm^2 = 21.6 m^2 = 3.6*6; slips 2,160, 216,000 |
| `items[1].parts[0].widget.answer` | key 19.635 m² | correct | 6.25 pi = 19.635; slips 25 pi = 78.54, 5 pi = 15.71 |
| `items[1].parts[0].widget.wrong[0]` | slip diameter = 78.5398: You squared the 5. The basin is 5 m across, so its radius is 2.5 m: $\pi \times 2.5^2$. | correct | 6.25 pi = 19.635; slips 25 pi = 78.54, 5 pi = 15.71 |
| `items[1].parts[0].widget.wrong[1]` | slip circumference = 15.708: That is the distance round, $\pi \times 5$. The area is $\pi r^2$ with $r = 2.5$. | correct | 6.25 pi = 19.635; slips 25 pi = 78.54, 5 pi = 15.71 |
| `items[1].parts[1].widget.answer` | key 134.37 m² | correct | 154 - 19.63 = 134.37; slips 154 - 15.71 = 138.29, 50 - 19.63 = 30.37 |
| `items[1].parts[1].widget.wrong[0]` | slip circumference-carried = 138.29: You took away 15.71, the basin's distance round. Take away its area, 19.63 m². | correct | 154 - 19.63 = 134.37; slips 154 - 15.71 = 138.29, 50 - 19.63 = 30.37 |
| `items[1].parts[1].widget.wrong[1]` | slip perimeter = 30.37: 50 m is the distance round the courtyard. Its area is $14 \times 11 = 154$ m². | correct | 154 - 19.63 = 134.37; slips 154 - 15.71 = 138.29, 50 - 19.63 = 30.37 |
| `items[1].parts[2].widget.answer` | key 12 | correct | 134.37/12 = 11.2, round up to 12; slips 11, ceil(154/12) = 13 |
| `items[1].parts[2].widget.wrong[0]` | slip rounded-down = 11: 11 tins cover only 132 m². You need $134.37 \div 12 \approx 11.20$ tins, so buy 12. | correct | 134.37/12 = 11.2, round up to 12; slips 11, ceil(154/12) = 13 |
| `items[1].parts[2].widget.wrong[1]` | slip whole-courtyard = 13: That seals all 154 m², basin included. Only 134.37 m² is paving. | correct | 134.37/12 = 11.2, round up to 12; slips 11, ceil(154/12) = 13 |
| `items[2].parts[0].widget.answer` | key 32 | correct | 160/5 = 32; slips 160/4 = 40, 27 = median |
| `items[2].parts[0].widget.wrong[0]` | slip four-days = 40: You divided by 4. There are five rides, so divide 160 by 5. | correct | 160/5 = 32; slips 160/4 = 40, 27 = median |
| `items[2].parts[0].widget.wrong[1]` | slip median = 27: 27 is the middle time once sorted, the median. The mean shares the total: $160 \div 5$. | correct | 160/5 = 32; slips 160/4 = 40, 27 = median |
| `items[2].parts[1].widget.answer` | key 27 | correct | sorted 24, 26, 27, 31, 52: 27; slips 24 = middle as written, 32 |
| `items[2].parts[1].widget.wrong[0]` | slip unsorted = 24: 24 is the middle of the list as written. Sort first: 24, 26, 27, 31, 52. | correct | sorted 24, 26, 27, 31, 52: 27; slips 24 = middle as written, 32 |
| `items[2].parts[1].widget.wrong[1]` | slip mean = 32: 32 is the mean. The median is the middle time once the list is sorted. | correct | sorted 24, 26, 27, 31, 52: 27; slips 24 = middle as written, 32 |
| `items[2].parts[2].widget.options[0]` | keyed correct: The median, 27 minutes | correct | median 27 sits among the four usual rides (24 to 31); mean 32 exceeds all four; range is spread |
| `items[2].parts[2].widget.options[1]` | wrong option: The mean, 32 minutes. Why: The puncture day drags the mean up: four of the five rides took less than 32 m… | correct | median 27 sits among the four usual rides (24 to 31); mean 32 exceeds all four; range is spread |
| `items[2].parts[2].widget.options[2]` | wrong option: The range, 28 minutes. Why: The range measures spread, from 24 to 52 minutes. It says nothing about a usu… | correct | median 27 sits among the four usual rides (24 to 31); mean 32 exceeds all four; range is spread |
| `items[2].parts[3].widget.answer` | key 20 km/h | correct | 9/(27/60) = 20; slips 9/27 = 0.33, 9*60/32 = 16.875 |
| `items[2].parts[3].widget.wrong[0]` | slip per-minute = 0.3333: $9 \div 27 \approx 0.33$ is km a minute. There are 60 minutes in an hour, so multiply by 60. | correct | 9/(27/60) = 20; slips 9/27 = 0.33, 9*60/32 = 16.875 |
| `items[2].parts[3].widget.wrong[1]` | slip mean-time = 16.875: That uses the mean, 32 minutes. A usual ride takes the median, 27 minutes. | correct | 9/(27/60) = 20; slips 9/27 = 0.33, 9*60/32 = 16.875 |
| `items[2].parts[4].widget.answer` | key 5.5556 m/s | correct | 20,000/3,600 = 5.56; slips 72, 20,000/60 = 333.33 |
| `items[2].parts[4].widget.wrong[0]` | slip wrong-way = 72: You multiplied by 3,600 and divided by 1,000. Turn both round: $20 \times 1{,}000 \div 3{,}600$. | correct | 20,000/3,600 = 5.56; slips 72, 20,000/60 = 333.33 |
| `items[2].parts[4].widget.wrong[1]` | slip minutes = 333.3333: You divided by 60, which gives metres a minute. An hour is 3,600 seconds. | correct | 20,000/3,600 = 5.56; slips 72, 20,000/60 = 333.33 |
| `items[3].parts[0].widget.answer` | key 144 | correct | lcm(48, 18) = 2^4*3^2 = 144; slips 864 = product, 6 = hcf |
| `items[3].parts[0].widget.wrong[0]` | slip product = 864: $48 \times 18 = 864$ is a common multiple, but not the lowest. Take each prime as often as one numb… | correct | lcm(48, 18) = 2^4*3^2 = 144; slips 864 = product, 6 = hcf |
| `items[3].parts[0].widget.wrong[1]` | slip hcf = 6: 6 is the HCF, which divides both. The painted teeth meet after a multiple of both. | correct | lcm(48, 18) = 2^4*3^2 = 144; slips 864 = product, 6 = hcf |
| `items[3].parts[1].widget.answer` | key 8 | correct | 144/18 = 8; slips 144/48 = 3, 864/18 = 48 |
| `items[3].parts[1].widget.wrong[0]` | slip big-gear = 3: 3 is the large gear's turns, $144 \div 48$. The small gear has 18 teeth. | correct | 144/18 = 8; slips 144/48 = 3, 864/18 = 48 |
| `items[3].parts[1].widget.wrong[1]` | slip product-carried = 48: That follows from 864 teeth. With 144 teeth, $144 \div 18 = 8$. | correct | 144/18 = 8; slips 144/48 = 3, 864/18 = 48 |
| `items[3].parts[2].widget.answer` | key 30 | correct | 4*60/8 = 30; slips 0.5 per second, 240/3 = 80 |
| `items[3].parts[2].widget.wrong[0]` | slip per-second = 0.5: 0.5 is the meetings a second. A minute has 60 seconds: $0.5 \times 60 = 30$. | correct | 4*60/8 = 30; slips 0.5 per second, 240/3 = 80 |
| `items[3].parts[2].widget.wrong[1]` | slip big-gear-carried = 80: That divides by 3, the large gear's turns. The small gear makes 8 turns a meeting. | correct | 4*60/8 = 30; slips 0.5 per second, 240/3 = 80 |
| `items[3].parts[3].widget.answer` | key 45 m | correct | 240*6 pi = 4,523.9 cm = 45.24 m; slips 240*12 pi = 90.48 m, 4,524 cm |
| `items[3].parts[3].widget.wrong[0]` | slip radius = 90: You used 6 cm as the radius. The gear is 6 cm across, so one turn is $\pi \times 6$. | correct | 240*6 pi = 4,523.9 cm = 45.24 m; slips 240*12 pi = 90.48 m, 4,524 cm |
| `items[3].parts[3].widget.wrong[1]` | slip centimetres = 4524: 4,524 is in centimetres. Divide by 100 for metres. | correct | 240*6 pi = 4,523.9 cm = 45.24 m; slips 240*12 pi = 90.48 m, 4,524 cm |
| `items[0].parts[1].explain.text` | A side that fits divides both lengths, so it divides their HCF | correct | every common divisor divides the gcd (Hardy and Wright section 2.9) |
| `items[1].parts[2].explain.text` | Tins come whole, so round up | correct | ceiling of 11.2 |
| `items[2].parts[2].explain.text` | "One extreme day moves the mean a lot and the median not at all" | imprecise | Finding 5: same general sentence as l19 screens[4] |
| `items[2].parts[3].explain.text` | Speed is distance over time | correct | definition of average speed |
| `items[3].parts[0].explain.text` | The painted teeth meet after a common multiple of 48 and 18 teeth; the lowest is the LCM | correct | each gear's painted tooth returns every 48 or 18 teeth passed |

## fluency-l15-building-blocks

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `families[largest-prime].widget.answer` | generated key {lp} for: Write ${nn}$ as a product of primes. What is its largest prime factor? | correct | all 196 rows: exponents multiply to n, largest prime correct, none a power of 2; n/smallest prime is composite whenever it is not the key (script) |
| `families[largest-prime].wrong[0]` | slip largest-factor = {big}: ${big}$ is ${nn} \div {sp}$, the largest factor below ${nn}$, but it is not prime. Keep sp… | correct | all 196 rows: exponents multiply to n, largest prime correct, none a power of 2; n/smallest prime is composite whenever it is not the key (script) |
| `families[largest-prime].wrong[1]` | slip prime-power = {lpp} when elp > 1 and lpp != big: ${lpp}$ is ${lp}^{elp}$, a power of ${lp}$. The prime itself is $… | correct | all 196 rows: exponents multiply to n, largest prime correct, none a power of 2; n/smallest prime is composite whenever it is not the key (script) |
| `families[count-from-primes].widget.answer` | generated key {key} for: How many factors does ${ptex}$ have? | correct | all 160 rows: d(n) = product (e+1) checked against a direct count; slips product of indices, sum of (e+1) |
| `families[count-from-primes].wrong[0]` | slip indices-multiplied = {mul} when mul != add: You multiplied the indices. Each index gives one more choice, because … | correct | all 160 rows: d(n) = product (e+1) checked against a direct count; slips product of indices, sum of (e+1) |
| `families[count-from-primes].wrong[1]` | slip indices-added = {add} when add != key: You added the choices for each prime. Every choice for one prime goes with … | correct | all 160 rows: d(n) = product (e+1) checked against a direct count; slips product of indices, sum of (e+1) |
| `families[count-factors].widget.answer` | generated key {key} for: How many factors does ${nn}$ have? | correct | all 160 rows: d(n) checked against a direct count; slips ceil(d/2) = pairs, product of indices |
| `families[count-factors].wrong[0]` | slip pairs = {pairs} when pairs != mul: ${pairs}$ is the number of factor pairs, the rectangles. Each pair holds two fa… | imprecise | Finding 7: value ceil(d(n)/2) is the pair count, but for the 11 square rows the pair n = k*k holds one factor, so "Each pair holds two factors" points to d(n)+1 |
| `families[count-factors].wrong[1]` | slip no-plus-one = {mul} when mul > 1: You multiplied the indices of ${ptex}$. Add 1 to each index first, because the p… | correct | all 160 rows: d(n) checked against a direct count; slips ceil(d/2) = pairs, product of indices |
| `families[largest-prime].wrong[0]#line` | n divided by its smallest prime is the largest factor below n | correct | the largest proper divisor is n/p for the smallest prime p |
| `families[count-from-primes].solution[0]` | Each index gives one more choice than its value, because the power 0 counts too | correct | d(n) rule as l15 screens[7] |

## fluency-l16-shared-factors

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `families[hcf].widget.answer` | generated key {g} for: What is the highest common factor of ${m}$ and ${n}$? | correct | exhaustive over all 29*43 (g, p) x (a, b) picks: gcd(ga, gb) = g since every (a, b) is coprime; lcm = gab; p is a prime factor of g (script) |
| `families[hcf].wrong[0]` | slip lcm = {l}: ${l}$ is the lowest common multiple. The HCF is the biggest number dividing both, so it is never bigger… | correct | exhaustive over all 29*43 (g, p) x (a, b) picks: gcd(ga, gb) = g since every (a, b) is coprime; lcm = gab; p is a prime factor of g (script) |
| `families[hcf].wrong[1]` | slip one-prime = {p} when g != p: ${p}$ divides both, but it is one shared prime only. Multiply every prime the two num… | correct | exhaustive over all 29*43 (g, p) x (a, b) picks: gcd(ga, gb) = g since every (a, b) is coprime; lcm = gab; p is a prime factor of g (script) |
| `families[lcm].widget.answer` | generated key {l} for: What is the lowest common multiple of ${m}$ and ${n}$? | correct | as hcf family: lcm(ga, gb) = gab for coprime a, b; product g^2 ab; 300 draws recomputed (script) |
| `families[lcm].wrong[0]` | slip product = {prod}: ${m} \times {n} = {prod}$ is a common multiple, but not the lowest: the shared ${g}$ is counted … | correct | as hcf family: lcm(ga, gb) = gab for coprime a, b; product g^2 ab; 300 draws recomputed (script) |
| `families[lcm].wrong[1]` | slip hcf = {g}: ${g}$ is the highest common factor. The LCM is a multiple of both, so it is never smaller than ${n}$. | correct | as hcf family: lcm(ga, gb) = gab for coprime a, b; product g^2 ab; 300 draws recomputed (script) |
| `families[other-number].widget.answer` | generated key {n} for: The HCF of ${m}$ and another number is ${g}$, and their LCM is ${l}$. What is the other number? | correct | x = hcf*lcm/m is the only x with that hcf and lcm (brute force to 2,000 in script); slips ab = lcm/hcf, g^2 ab = product |
| `families[other-number].wrong[0]` | slip lcm-over-hcf = {lg} when a*b != g*b: ${l} \div {g} = {lg}$ leaves out ${m}$. The two numbers multiply to HCF times… | correct | x = hcf*lcm/m is the only x with that hcf and lcm (brute force to 2,000 in script); slips ab = lcm/hcf, g^2 ab = product |
| `families[other-number].wrong[1]` | slip product = {prod}: ${prod}$ is HCF times LCM, the two numbers multiplied. Divide it by ${m}$. | correct | x = hcf*lcm/m is the only x with that hcf and lcm (brute force to 2,000 in script); slips ab = lcm/hcf, g^2 ab = product |
| `families[hcf].wrong[0]#line` | The HCF is never bigger than the smaller number m | correct | m = ga < n = gb for every pick (a < b checked in script) |
| `families[lcm].wrong[1]#line` | The LCM is never smaller than the larger number n | correct | lcm is a positive multiple of n |
| `families[other-number].solution[0]` | HCF times LCM is the two numbers multiplied | correct | as l16 screens[9] |

## fluency-l17-around-and-inside

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `families[triangle-area].widget.answer` | generated key {key} for: A triangle has base ${b}$ cm, a sloping side of ${s}$ cm and height ${h}$ cm. Work out its are… | correct | bh/2 with bh even; slips bh, b(h+k)/2; a side h+k >= h always gives a real triangle; 300 draws recomputed |
| `families[triangle-area].wrong[0]` | slip no-half = {bh}: ${b} \times {h} = {bh}$ is the rectangle round the triangle. The triangle is half of it. | correct | bh/2 with bh even; slips bh, b(h+k)/2; a side h+k >= h always gives a real triangle; 300 draws recomputed |
| `families[triangle-area].wrong[1]` | slip sloping-side = {bs} when s != 2*h: You used the sloping side. The height is the one that meets the base at a right… | correct | bh/2 with bh even; slips bh, b(h+k)/2; a side h+k >= h always gives a real triangle; 300 draws recomputed |
| `families[parallelogram-area].widget.answer` | generated key {key} for: A parallelogram has base ${b}$ cm, slant side ${s}$ cm and height ${h}$ cm. Work out its area … | correct | bh; slips b(h+k), bh/2; 300 draws recomputed |
| `families[parallelogram-area].wrong[0]` | slip slant-side = {bs}: You multiplied by the slant side. Sliding the end triangle across makes a rectangle as tall as … | correct | bh; slips b(h+k), bh/2; 300 draws recomputed |
| `families[parallelogram-area].wrong[1]` | slip halved = {half}: You halved, as for a triangle. A parallelogram slides into a whole rectangle, base times height. | correct | bh; slips b(h+k), bh/2; 300 draws recomputed |
| `families[trapezium-area].widget.answer` | generated key {key} for: A trapezium has parallel sides of ${a}$ m and ${c}$ m, and height ${h}$ m. Work out its area i… | correct | (a + c)h/2 with c = a + d; slips (a+c)h, ch; 300 draws recomputed |
| `families[trapezium-area].wrong[0]` | slip no-half = {full}: ${full}$ is two copies of the trapezium, which make a parallelogram. Halve it. | correct | (a + c)h/2 with c = a + d; slips (a+c)h, ch; 300 draws recomputed |
| `families[trapezium-area].wrong[1]` | slip longer-side = {long} when (a + d)*h != (2*a + d)*h/2: You used only the longer parallel side. Use the average of t… | correct | (a + c)h/2 with c = a + d; slips (a+c)h, ch; 300 draws recomputed |
| `families[l-shape-area].widget.answer` | generated key {key} for: An L-shaped floor is a ${w}$ m by ${t}$ m rectangle with a ${p}$ m by ${q}$ m corner cut away.… | correct | wt - pq with p < w - 1, q < t - 1; slips wt, wt + pq; 300 draws recomputed |
| `families[l-shape-area].wrong[0]` | slip corner-kept = {whole}: ${whole}$ m² is the full rectangle. Take away the corner that was cut out. | correct | wt - pq with p < w - 1, q < t - 1; slips wt, wt + pq; 300 draws recomputed |
| `families[l-shape-area].wrong[1]` | slip corner-added = {added}: You added the corner. It was cut away, so take ${cut}$ off. | correct | wt - pq with p < w - 1, q < t - 1; slips wt, wt + pq; 300 draws recomputed |
| `families[triangle-area].solution[0]` | Area = half * base * height, with the height at right angles to the base | correct | Euclid I.41 |
| `families[trapezium-area].wrong[0]#line` | Two copies of the trapezium make a parallelogram; halve it | correct | as l17 screens[4] |

## fluency-l18-circles-and-units

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `families[circumference].widget.answer` | generated key {circ} for: A round {obj} has {word} ${m}$ {u}. Work out its circumference in {u}, to 1 decimal place. | correct | pi d; slips pi r^2 (suppressed within 1 of key or other slip), pi r or 2 pi d; 3.14 and 22/7 answers to 1 dp accepted on all 300 draws (script) |
| `families[circumference].wrong[0]` | slip area-rule = {area} when abs(area - circ) > 1 and abs(area - swap) > 1: You used $\pi r^2$, the area. The distance … | correct | pi d; slips pi r^2 (suppressed within 1 of key or other slip), pi r or 2 pi d; 3.14 and 22/7 answers to 1 dp accepted on all 300 draws (script) |
| `families[circumference].wrong[1]` | slip radius-diameter = {swap}: You mixed up the radius and the diameter. The diameter is twice the radius: ${d}$ {u} he… | correct | pi d; slips pi r^2 (suppressed within 1 of key or other slip), pi r or 2 pi d; 3.14 and 22/7 answers to 1 dp accepted on all 300 draws (script) |
| `families[circle-area].widget.answer` | generated key {area} for: A round {obj} has {word} ${m}$ {u}. Work out its area in {u}², to 1 decimal place. | correct | pi r^2, r <= 8; slips pi d^2 (diameter given), 2 pi r; 3.14 and 22/7 answers to 1 dp accepted on all 300 draws (script) |
| `families[circle-area].wrong[0]` | slip diameter-squared = {dsq} when k == 2: You squared the diameter. $\pi r^2$ takes the radius: halve ${m}$ first. | correct | pi r^2, r <= 8; slips pi d^2 (diameter given), 2 pi r; 3.14 and 22/7 answers to 1 dp accepted on all 300 draws (script) |
| `families[circle-area].wrong[1]` | slip circumference = {circ} when abs(area - circ) > 1: That is the distance round, $2\pi r$. The area is $\pi r^2$. | correct | pi r^2, r <= 8; slips pi d^2 (diameter given), 2 pi r; 3.14 and 22/7 answers to 1 dp accepted on all 300 draws (script) |
| `families[speed-units].widget.answer` | generated key {key} for: Change ${x}$ {from} into {to}, to 1 decimal place. | correct | x*1000/3600 or x*3600/1000; slips inverted, and *1000/60 or *60/1000; 300 draws recomputed |
| `families[speed-units].wrong[0]` | slip wrong-way = {back}: You turned the fractions the wrong way round. Pick the ones that cancel the units you have. | correct | x*1000/3600 or x*3600/1000; slips inverted, and *1000/60 or *60/1000; 300 draws recomputed |
| `families[speed-units].wrong[1]` | slip minutes = {mins}: An hour is 3,600 seconds, not 60. You changed hours into minutes only. | imprecise | Finding 6: value is right for both directions (x*1000/60, x*60/1000) but for m/s to km/h the learner changed seconds to minutes, not "hours into minutes"; concepts script INFO |
| `families[area-units].widget.answer` | generated key {key} for: A {ob} has an area of ${a}$ m². What is its area in cm²? | correct | a m^2 = 10,000a cm^2; slips 100a, a/10,000; 300 draws recomputed |
| `families[area-units].wrong[0]` | slip length-only = {once}: You multiplied by 100, as for a length. A square metre is 100 cm by 100 cm, so multiply by 1… | correct | a m^2 = 10,000a cm^2; slips 100a, a/10,000; 300 draws recomputed |
| `families[area-units].wrong[1]` | slip divided = {down}: You divided. A square centimetre is far smaller than a square metre, so there are more of them: … | correct | a m^2 = 10,000a cm^2; slips 100a, a/10,000; 300 draws recomputed |
| `families[circle-area].widget.tol` | Convention: answers to 1 decimal place within 0.2; pi = 3.14 and 22/7 accepted for r up to 8 | correct | worst case 64 * 0.0016 + 0.05 = 0.15 < 0.2; all draws in script |
| `families[area-units].solution[0]` | 1 m² is 100 * 100 = 10,000 cm² | correct | as l17 screens[7] |

## fluency-l19-one-number-for-many

| JSON path | Claim | Verdict | Basis |
|---|---|---|---|
| `families[mean].widget.answer` | generated key {m} for: Five daily profits, in pounds, are ${b}$, ${a}$, ${c}$, ${e}$ and ${d}$. What is the mean daily … | correct | e chosen so the five values sum to 5m; slips 5m/4, (5m - 2a)/5 = total with the loss a entered as +\|a\|; recomputed from the prompt values |
| `families[mean].wrong[0]` | slip divided-by-four = {four}: You divided by 4. There are five days, so share the total of ${tot}$ by 5. | correct | e chosen so the five values sum to 5m; slips 5m/4, (5m - 2a)/5 = total with the loss a entered as +\|a\|; recomputed from the prompt values |
| `families[mean].wrong[1]` | slip loss-added = {pos} when 5*m/4 != (5*m - 2*a)/5: You added the loss of ${a}$ as a profit. A loss takes away from th… | correct | e chosen so the five values sum to 5m; slips 5m/4, (5m - 2a)/5 = total with the loss a entered as +\|a\|; recomputed from the prompt values |
| `families[median].widget.answer` | generated key {s3} for: Five readings, in the order they came, are ${d1}$, ${d2}$, ${d3}$, ${d4}$ and ${d5}$. What is t… | correct | five distinct values, key the 3rd sorted; slips the 3rd as written (when not the median), the mean (when distinct); recomputed from the prompt values |
| `families[median].wrong[0]` | slip unsorted = {d3} when o3 != 3: ${d3}$ is the middle of the list as written. Sort the values first. | correct | five distinct values, key the 3rd sorted; slips the 3rd as written (when not the median), the mean (when distinct); recomputed from the prompt values |
| `families[median].wrong[1]` | slip mean = {mean} when mean != s3 and mean != d3: That is the mean. The median is the middle value once the list is so… | correct | five distinct values, key the 3rd sorted; slips the 3rd as written (when not the median), the mean (when distinct); recomputed from the prompt values |
| `families[range].widget.answer` | generated key {key} for: Five daily results, in pounds, are ${d1}$, ${d2}$, ${d3}$, ${d4}$ and ${d5}$. What is the rang… | correct | s5 - s1 with s1 < 0 < s5; slips \|last - first\|, s5 - \|s1\|; recomputed from the prompt values |
| `families[range].wrong[0]` | slip first-last = {fl} when abs(d5 - d1) != g1 + g2 + g3 + g4 and abs(d5 - d1) != s5 + s1: You used the first and last … | correct | s5 - s1 with s1 < 0 < s5; slips \|last - first\|, s5 - \|s1\|; recomputed from the prompt values |
| `families[range].wrong[1]` | slip sign-lost = {lost} when s5 + s1 != g1 + g2 + g3 + g4: Taking away ${s1}$ adds ${-s1}$: ${s5} - {s1:()} = {key}$. | correct | s5 - s1 with s1 < 0 < s5; slips \|last - first\|, s5 - \|s1\|; recomputed from the prompt values |
| `families[table-mean].widget.answer` | generated key {key} for: {tcap} {one}, counted over ${n}$ {unit}: ${f0}$ {unit} had 0, ${f1}$ had 1, ${f2}$ had 2, ${f3… | correct | sum(i f_i)/sum(f_i); slips 2 = mean of 0..4, total/5; both kept at least 0.03 from the key by the where lines |
| `families[table-mean].wrong[0]` | slip values-only = {plain}: You took the mean of 0, 1, 2, 3 and 4 without their counts. Weight each value by how often … | correct | sum(i f_i)/sum(f_i); slips 2 = mean of 0..4, total/5; both kept at least 0.03 from the key by the where lines |
| `families[table-mean].wrong[1]` | slip rows = {rows}: You divided the total by the 5 rows. Divide by the {n} {unit}. | correct | sum(i f_i)/sum(f_i); slips 2 = mean of 0..4, total/5; both kept at least 0.03 from the key by the where lines |
| `families[median].solution[1]` | The median of five sorted values is the third | correct | definition; the five values are distinct by construction (gaps of at least 1) |
| `families[range].wrong[1]#line` | Taking away a negative adds its size | correct | a - (-b) = a + b |

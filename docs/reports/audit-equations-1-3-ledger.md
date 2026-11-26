# Claim ledger: equations levels 1 to 3 (audit equations-1-3, round 1)

Stage 0 depth: definitions, rules, "always / never / every" claims, conventions, and every graded key, wrong option and slip. Rows marked "concepts script" are recomputed by `docs/reports/equations-L1-3-concepts.py` from the item's own givens. Sources: Gelfand and Shen, Algebra; a standard GCSE and A-level algebra text (expressions, linear equations, inequalities, rearranging formulae).

Rows: 1068. Verdicts: correct 1064, imprecise 3, wrong 1.

## l1-letters-for-numbers

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.answer` | key 19 | correct | concepts script: recomputed 19.0 |
| `screens[0].widget.wrong[added]` | slip added = 12 | correct | concepts script: named slip gives 12.0; differs from key |
| `screens[0].widget.wrong[all-envelopes]` | slip all-envelopes = 35 | correct | concepts script: named slip gives 35.0; differs from key |
| `screens[0].widget.wrong[coins-inside]` | slip coins-inside = 27 | correct | concepts script: named slip gives 27.0; differs from key |
| `screens[0].widget.wrong[one-envelope]` | slip one-envelope = 9 | correct | concepts script: named slip gives 9.0; differs from key |
| `screens[1].widget.points[0].target` | target 22 | correct | concepts script: recomputed 22 |
| `screens[1].widget.wrong[added]` | slip region 12.7 to 13.3 | correct | concepts script: named slip gives 13; key outside the region |
| `screens[1].widget.wrong[one-envelope]` | slip region 9.7 to 10.3 | correct | concepts script: named slip gives 10; key outside the region |
| `screens[1].widget.wrong[coins-inside]` | slip region 29.7 to 30.3 | correct | concepts script: named slip gives 30; key outside the region |
| `screens[1].widget.wrong[old]` | slip region 18.7 to 19.3 | correct | concepts script: named slip gives 19; key outside the region |
| `screens[4].widget.answer` | key 103 | correct | concepts script: recomputed 103.0 |
| `screens[4].widget.wrong[side-by-side]` | slip side-by-side = 253 | correct | concepts script: named slip gives 253.0; differs from key |
| `screens[4].widget.wrong[plus-first]` | slip plus-first = 250 | correct | concepts script: named slip gives 250.0; differs from key |
| `screens[4].widget.wrong[added]` | slip added = 55 | correct | concepts script: named slip gives 55.0; differs from key |
| `quiz[1].widget.answer` | key 4 | correct | concepts script: recomputed 4.0 |
| `quiz[1].widget.wrong[three]` | slip three = 7 | correct | concepts script: named slip gives 7.0; differs from key |
| `quiz[1].widget.wrong[side-by-side]` | slip side-by-side = 34 | correct | concepts script: named slip gives 34.0; differs from key |
| `quiz[1].widget.wrong[all-zero]` | slip all-zero = 0 | correct | concepts script: named slip gives 0.0; differs from key |
| `quiz[3].widget.answer` | key 26 | correct | concepts script: recomputed 26.0 |
| `quiz[3].widget.wrong[side-by-side]` | slip side-by-side = 52 | correct | concepts script: named slip gives 52.0; differs from key |
| `quiz[3].widget.wrong[subtract-first]` | slip subtract-first = 6 | correct | concepts script: named slip gives 6.0; differs from key |
| `quiz[3].widget.wrong[added]` | slip added = 7 | correct | concepts script: named slip gives 7.0; differs from key |
| `screens[2].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[2].widget.options[right]` | $2n + 5$ equals the source expression | correct | concepts script: sympy identity test against 2*n + 5 |
| `screens[2].widget.options[all-n]` | $7n$ differs from the source expression | correct | concepts script: sympy identity test against 2*n + 5 |
| `screens[2].widget.options[swapped]` | $2 + 5n$ differs from the source expression | correct | concepts script: sympy identity test against 2*n + 5 |
| `screens[2].widget.options[one-each]` | $n + 7$ differs from the source expression | correct | concepts script: sympy identity test against 2*n + 5 |
| `screens[3].widget.answer` | 3+2n equals the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.accept[0]` | 3+2n equals the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.accept[1]` | 2n+3 equals the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.accept[2]` | 3+2*n equals the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.accept[3]` | 2*n+3 equals the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.accept[4]` | 3 + 2n equals the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.accept[5]` | 2n + 3 equals the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.wrong[fee-each]` | 5n differs from the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.wrong[swapped]` | 3n+2 differs from the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[3].widget.wrong[added-once]` | n+5 differs from the source expression | correct | concepts script: sympy identity test against 2*n + 3 |
| `screens[8].widget.answer` | 25+12m equals the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.accept[0]` | 25+12m equals the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.accept[1]` | 12m+25 equals the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.accept[2]` | 25+12*m equals the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.accept[3]` | 12*m+25 equals the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.accept[4]` | 25 + 12m equals the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.accept[5]` | 12m + 25 equals the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.wrong[fee-monthly]` | 37m differs from the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[8].widget.wrong[swapped]` | 25m+12 differs from the source expression | correct | concepts script: sympy identity test against 12*m + 25 |
| `screens[9].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[9].widget.options[right]` | $1.50 + 0.02n$ equals the source expression | correct | concepts script: sympy identity test against n/50 + 3/2 |
| `screens[9].widget.options[pence]` | $1.50 + 2n$ differs from the source expression | correct | concepts script: sympy identity test against n/50 + 3/2 |
| `screens[9].widget.options[fee-each]` | $1.52n$ differs from the source expression | correct | concepts script: sympy identity test against n/50 + 3/2 |
| `screens[9].widget.options[swapped]` | $0.02 + 1.50n$ differs from the source expression | correct | concepts script: sympy identity test against n/50 + 3/2 |
| `quiz[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[0].widget.options[right]` | $9t + 2$ equals the source expression | correct | concepts script: sympy identity test against 9*t + 2 |
| `quiz[0].widget.options[fee-each]` | $11t$ differs from the source expression | correct | concepts script: sympy identity test against 9*t + 2 |
| `quiz[0].widget.options[swapped]` | $2t + 9$ differs from the source expression | correct | concepts script: sympy identity test against 9*t + 2 |
| `quiz[0].widget.options[added]` | $t + 11$ differs from the source expression | correct | concepts script: sympy identity test against 9*t + 2 |
| `quiz[2].widget.answer` | 12.4q+150 equals the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.accept[0]` | 12.4q+150 equals the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.accept[1]` | 150+12.4q equals the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.accept[2]` | 12.40q+150 equals the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.accept[3]` | 150+12.40q equals the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.accept[4]` | 12.4*q+150 equals the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.accept[5]` | 150+12.4*q equals the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.wrong[cash-each]` | 162.4q differs from the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `quiz[2].widget.wrong[swapped]` | 150q+12.4 differs from the source expression | correct | concepts script: sympy identity test against 62*q/5 + 150 |
| `screens[5].widget.options[right]` | key: The right pan | correct | substitution: left 2(5)+4 = 14, right 3(5) = 15; equal only at n = 4 |
| `screens[5].widget.options[left]` | wrong option: The left pan / why: You assumed the heavier pan stays heavier. Substitute $n = 5$: the left is $2 \times 5 + 4... | correct | substitution: left 2(5)+4 = 14, right 3(5) = 15; equal only at n = 4 |
| `screens[5].widget.options[level]` | wrong option: Neither: they balance / why: You may have tried $n = 4$, where both pans weigh 12. At $n = 5$ the right pan has 15 and ... | correct | substitution: left 2(5)+4 = 14, right 3(5) = 15; equal only at n = 4 |
| `screens[6].widget.options[right]` | key: £11 | correct | order of operations: 3 + 2(4) = 11; (3+2)4 = 20; 3 + 24 = 27; 3+2+4 = 9 |
| `screens[6].widget.options[plus-first]` | wrong option: £20 / why: That is Ravi's answer. Adding 3 and 2 first charges the £3 fee on every share. | correct | order of operations: 3 + 2(4) = 11; (3+2)4 = 20; 3 + 24 = 27; 3+2+4 = 9 |
| `screens[6].widget.options[side-by-side]` | wrong option: £27 / why: You read $2n$ as 24, the digits side by side. $2n$ means $2 \times 4 = 8$. | correct | order of operations: 3 + 2(4) = 11; (3+2)4 = 20; 3 + 24 = 27; 3+2+4 = 9 |
| `screens[6].widget.options[added]` | wrong option: £9 / why: You added 3, 2 and 4. The £2 is paid for each share, so it multiplies the 4. | correct | order of operations: 3 + 2(4) = 11; (3+2)4 = 20; 3 + 24 = 27; 3+2+4 = 9 |
| `screens[7].widget.options[right]` | key: $35$ | correct | juxtaposition means product (Gelfand and Shen, Algebra, sections on letters and notation): 5(7) = 35 |
| `screens[7].widget.options[side-by-side]` | wrong option: $57$ / why: You wrote 5 and 7 side by side. $5n$ means $5 \times n$. | correct | juxtaposition means product (Gelfand and Shen, Algebra, sections on letters and notation): 5(7) = 35 |
| `screens[7].widget.options[added]` | wrong option: $12$ / why: You added 5 and 7. A number against a letter means multiply. | correct | juxtaposition means product (Gelfand and Shen, Algebra, sections on letters and notation): 5(7) = 35 |
| `screens[2].prose` | a letter stands for a number not yet known; 3 x n is written 3n | correct | Gelfand and Shen, Algebra, letters in algebra; standard GCSE algebra text, algebraic notation |
| `screens[2].explain.text` | definition: an expression is a combination of numbers and letters | correct | standard GCSE algebra text, expressions |
| `screens[4].prose` | definition: substituting is putting a number in for the letter; table rows 5 and 23 | correct | derivation: 3 + 2(1) = 5, 3 + 2(10) = 23 |
| `screens[5].explain.text` | n = 4 is the one value that balances 2n + 4 and 3n | correct | derivation: 2n + 4 = 3n has the single root 4 |
| `screens[6].explain.text` | Ravi's order gives 5n, overcharging by 9 at n = 4 | correct | derivation: 20 - 11 = 9 |
| `screens[7].prose` | rule: a number against a letter means multiply; multiply before you add | correct | Gelfand and Shen, Algebra, order of operations; standard GCSE algebra text |
| `screens[7].explain.text` | always claim: the hidden sign between a number and a letter is always a multiplication | correct | standard GCSE algebra text: notation convention for a coefficient |
| `screens[9].canvas` | table rows 3.50, 11.50, 41.50 for 100, 500, 2,000 shares | correct | derivation: 1.50 + 0.02n at each n |
| `summary` | ideas, formula cost = 3 + 2n, trap 3 + 2n is not 5n | correct | derivation: differ at every n except 1 |

## l2-like-terms

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[1].widget.points[0].target` | target 20 | correct | concepts script: recomputed 20 |
| `screens[1].widget.wrong[lost-one]` | slip region 15.7 to 16.3 | correct | concepts script: named slip gives 16; key outside the region |
| `screens[1].widget.wrong[times]` | slip region 26.7 to 27.3 | correct | concepts script: named slip gives 27; key outside the region |
| `screens[1].widget.wrong[tray-a]` | slip region 10.7 to 11.3 | correct | concepts script: named slip gives 11; key outside the region |
| `screens[5].widget.answer` | key 22 | correct | concepts script: recomputed 22.0 |
| `screens[5].widget.wrong[sams]` | slip sams = 32 | correct | concepts script: named slip gives 32.0; differs from key |
| `screens[5].widget.wrong[old]` | slip old = 16 | correct | concepts script: named slip gives 16.0; differs from key |
| `screens[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[0].widget.options[right]` | $3n + 8$ equals the source expression | correct | concepts script: sympy identity test against 3*n + 8 |
| `screens[0].widget.options[all-n]` | $11n$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 8 |
| `screens[0].widget.options[lost-one]` | $2n + 8$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 8 |
| `screens[0].widget.options[times]` | $3n + 15$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 8 |
| `screens[4].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[4].widget.options[right]` | $3n + 2$ equals the source expression | correct | concepts script: sympy identity test against 3*n + 2 |
| `screens[4].widget.options[no-signs]` | $7n + 10$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 2 |
| `screens[4].widget.options[half-signs]` | $3n + 10$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 2 |
| `screens[4].widget.options[added-n]` | $7n + 2$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 2 |
| `screens[9].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[9].widget.options[right]` | $0.60n - 8$ equals the source expression | correct | concepts script: sympy identity test against 3*n/5 - 8 |
| `screens[9].widget.options[added]` | $25.60n - 8$ differs from the source expression | correct | concepts script: sympy identity test against 3*n/5 - 8 |
| `screens[9].widget.options[one-fee]` | $0.60n - 4$ differs from the source expression | correct | concepts script: sympy identity test against 3*n/5 - 8 |
| `screens[9].widget.options[unlike]` | $-7.40n$ differs from the source expression | correct | concepts script: sympy identity test against 3*n/5 - 8 |
| `quiz[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[0].widget.options[right]` | $7a + 9$ equals the source expression | correct | concepts script: sympy identity test against 7*a + 9 |
| `quiz[0].widget.options[all]` | $16a$ differs from the source expression | correct | concepts script: sympy identity test against 7*a + 9 |
| `quiz[0].widget.options[times-a]` | $10a + 9$ differs from the source expression | correct | concepts script: sympy identity test against 7*a + 9 |
| `quiz[0].widget.options[times-n]` | $7a + 18$ differs from the source expression | correct | concepts script: sympy identity test against 7*a + 9 |
| `quiz[1].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[1].widget.options[right]` | $3n$ equals the source expression | correct | concepts script: sympy identity test against 3*n |
| `quiz[1].widget.options[cube]` | $n^3$ differs from the source expression | correct | concepts script: sympy identity test against 3*n |
| `quiz[1].widget.options[plus]` | $3 + n$ differs from the source expression | correct | concepts script: sympy identity test against 3*n |
| `quiz[2].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[2].widget.options[right]` | $3x + 4$ equals the source expression | correct | concepts script: sympy identity test against 3*x + 4 |
| `quiz[2].widget.options[plus-5x]` | $13x + 4$ differs from the source expression | correct | concepts script: sympy identity test against 3*x + 4 |
| `quiz[2].widget.options[minus-7]` | $3x - 10$ differs from the source expression | correct | concepts script: sympy identity test against 3*x + 4 |
| `quiz[2].widget.options[unlike]` | $7x$ differs from the source expression | correct | concepts script: sympy identity test against 3*x + 4 |
| `quiz[3].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[3].widget.options[right]` | $5$ equals the source expression | correct | concepts script: sympy identity test against 5 |
| `quiz[3].widget.options[kept-n]` | $5n$ differs from the source expression | correct | concepts script: sympy identity test against 5 |
| `quiz[3].widget.options[added]` | $12n + 5$ differs from the source expression | correct | concepts script: sympy identity test against 5 |
| `quiz[3].widget.options[one-n]` | $n + 5$ differs from the source expression | correct | concepts script: sympy identity test against 5 |
| `screens[5].explain.text` | Sam's 16n matches the expression only at n = 1 | correct | concepts script: two different linear expressions agree at one n at most: 6n + 10 = 16n only at n = 1 |
| `screens[5].explain.text` | n = 0 would in fact expose this particular slip (10 against 0); the advice is a rule of thumb | correct | concepts script: direct substitution |
| `screens[6].widget.options[right]` | key: No. $3n$ and 2 are not like terms | correct | 3n + 2 and 5n differ at n = 10 (32 against 50); unlike terms do not combine |
| `screens[6].widget.options[five-n]` | wrong option: Yes, to $5n$: add the 3 and the 2 / why: You added the coins to the envelopes. $5n$ means five envelopes, but the tray has three. | correct | 3n + 2 and 5n differ at n = 10 (32 against 50); unlike terms do not combine |
| `screens[6].widget.options[six-n]` | wrong option: Yes, to $6n$: multiply 3 by 2 / why: You multiplied 3 by 2. The 2 is loose coins, not a number of envelopes. | correct | 3n + 2 and 5n differ at n = 10 (32 against 50); unlike terms do not combine |
| `screens[6].widget.options[five]` | wrong option: Yes, to 5: drop the letter / why: You dropped the letter. Three envelopes hold $3n$ pounds, not £3. | correct | 3n + 2 and 5n differ at n = 10 (32 against 50); unlike terms do not combine |
| `screens[7].widget.options[right]` | key: $7n$ and $-2n$ | correct | like terms share the same letter part; n and n^2, and 3n and 3m, do not |
| `screens[7].widget.options[same-number]` | wrong option: $7n$ and $7$ / why: You matched the number in front. Like terms share the letter part; 7 has no letter. | correct | like terms share the same letter part; n and n^2, and 3n and 3m, do not |
| `screens[7].widget.options[square]` | wrong option: $n$ and $n^2$ / why: You matched the letter, but $n^2$ is $n \times n$. Its letter part is different. | correct | like terms share the same letter part; n and n^2, and 3n and 3m, do not |
| `screens[7].widget.options[letters]` | wrong option: $3n$ and $3m$ / why: These have different letters, which can stand for different amounts. $3n + 3m$ does not si... | correct | like terms share the same letter part; n and n^2, and 3n and 3m, do not |
| `screens[2].prose` | definitions: terms are the parts joined by + or -; like terms have the same letter part | correct | standard GCSE algebra text, collecting like terms |
| `screens[2].widget` | place: 3n and n are n terms; 4 and 2 numbers | correct | definition of like terms |
| `screens[3].widget` | place: terms of 5n + 6 - 2n - 4 are 5n, +6, -2n, -4; a sign belongs to the term after it | correct | standard GCSE algebra text |
| `screens[7].prose` | rule: an + bn = (a + b)n; unlike terms stay apart | correct | Gelfand and Shen, Algebra, distributive law read right to left |
| `screens[8].widget` | order: 4n+7+2n+3 = 4n+2n+7+3 = (4+2)n+(7+3) = 6n+10, with commutativity then distributivity | correct | Gelfand and Shen, Algebra, commutative and distributive laws |
| `screens[9].explain.text` | profit 0.60n - 8; 292 at 500 shares | correct | derivation: 300 - 8 |
| `summary` | ideas, formula an + bn = (a + b)n, trap 3n + 2 is not 5n | correct | Gelfand and Shen, Algebra, distributive law |

## l3-opening-brackets

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.answer` | key 21 | correct | concepts script: recomputed 21.0 |
| `screens[0].widget.wrong[first-only]` | slip first-only = 17 | correct | concepts script: named slip gives 17.0; differs from key |
| `screens[0].widget.wrong[added]` | slip added = 10 | correct | concepts script: named slip gives 10.0; differs from key |
| `screens[0].widget.wrong[left-only]` | slip left-only = 15 | correct | concepts script: named slip gives 15.0; differs from key |
| `quiz[2].widget.answer` | key 70 | correct | concepts script: recomputed 70.0 |
| `quiz[2].widget.wrong[first-only]` | slip first-only = 46 | correct | concepts script: named slip gives 46.0; differs from key |
| `quiz[2].widget.wrong[added]` | slip added = 17 | correct | concepts script: named slip gives 17.0; differs from key |
| `screens[2].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[2].widget.options[right]` | $3n + 6$ equals the source expression | correct | concepts script: sympy identity test against 3*n + 6 |
| `screens[2].widget.options[one-strip]` | $n + 6$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 6 |
| `screens[2].widget.options[first-only]` | $3n + 2$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 6 |
| `screens[2].widget.options[added]` | $5n$ differs from the source expression | correct | concepts script: sympy identity test against 3*n + 6 |
| `screens[4].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[4].widget.options[right]` | $10n + 5$ equals the source expression | correct | concepts script: sympy identity test against 10*n + 5 |
| `screens[4].widget.options[first-only]` | $10n + 1$ differs from the source expression | correct | concepts script: sympy identity test against 10*n + 5 |
| `screens[4].widget.options[added]` | $7n + 5$ differs from the source expression | correct | concepts script: sympy identity test against 10*n + 5 |
| `screens[4].widget.options[last-only]` | $2n + 5$ differs from the source expression | correct | concepts script: sympy identity test against 10*n + 5 |
| `screens[5].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[5].widget.options[right]` | $-2n + 8$ equals the source expression | correct | concepts script: sympy identity test against 8 - 2*n |
| `screens[5].widget.options[neg-neg]` | $-2n - 8$ differs from the source expression | correct | concepts script: sympy identity test against 8 - 2*n |
| `screens[5].widget.options[first-only]` | $-2n - 4$ differs from the source expression | correct | concepts script: sympy identity test against 8 - 2*n |
| `screens[5].widget.options[lost-sign]` | $2n - 8$ differs from the source expression | correct | concepts script: sympy identity test against 8 - 2*n |
| `screens[7].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[7].widget.options[right]` | $6n - 12$ equals the source expression | correct | concepts script: sympy identity test against 6*n - 12 |
| `screens[7].widget.options[first-only]` | $6n - 2$ differs from the source expression | correct | concepts script: sympy identity test against 6*n - 12 |
| `screens[7].widget.options[sign]` | $6n + 12$ differs from the source expression | correct | concepts script: sympy identity test against 6*n - 12 |
| `screens[7].widget.options[last-only]` | $n - 12$ differs from the source expression | correct | concepts script: sympy identity test against 6*n - 12 |
| `screens[9].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[9].widget.options[right]` | $40n + 250$ equals the source expression | correct | concepts script: sympy identity test against 40*n + 250 |
| `screens[9].widget.options[first-only]` | $40n + 6.25$ differs from the source expression | correct | concepts script: sympy identity test against 40*n + 250 |
| `screens[9].widget.options[added]` | $46.25n$ differs from the source expression | correct | concepts script: sympy identity test against 40*n + 250 |
| `screens[9].widget.options[decimal]` | $40n + 25$ differs from the source expression | correct | concepts script: sympy identity test against 40*n + 250 |
| `quiz[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[0].widget.options[right]` | $5n + 15$ equals the source expression | correct | concepts script: sympy identity test against 5*n + 15 |
| `quiz[0].widget.options[first-only]` | $5n + 3$ differs from the source expression | correct | concepts script: sympy identity test against 5*n + 15 |
| `quiz[0].widget.options[added]` | $5n + 8$ differs from the source expression | correct | concepts script: sympy identity test against 5*n + 15 |
| `quiz[0].widget.options[all-n]` | $8n$ differs from the source expression | correct | concepts script: sympy identity test against 5*n + 15 |
| `quiz[1].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[1].widget.options[right]` | $8n - 4$ equals the source expression | correct | concepts script: sympy identity test against 8*n - 4 |
| `quiz[1].widget.options[first-only]` | $8n - 1$ differs from the source expression | correct | concepts script: sympy identity test against 8*n - 4 |
| `quiz[1].widget.options[added]` | $6n - 4$ differs from the source expression | correct | concepts script: sympy identity test against 8*n - 4 |
| `quiz[1].widget.options[sign]` | $8n + 4$ differs from the source expression | correct | concepts script: sympy identity test against 8*n - 4 |
| `quiz[3].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[3].widget.options[right]` | $n^2 + 3n$ equals the source expression | correct | concepts script: sympy identity test against n*(n + 3) |
| `quiz[3].widget.options[added]` | $2n + 3n$ differs from the source expression | correct | concepts script: sympy identity test against n*(n + 3) |
| `quiz[3].widget.options[first-only]` | $n^2 + 3$ differs from the source expression | correct | concepts script: sympy identity test against n*(n + 3) |
| `quiz[3].widget.options[lost-square]` | $n + 3n$ differs from the source expression | correct | concepts script: sympy identity test against n*(n + 3) |
| `screens[6].widget.options[right]` | key: No. The 3 multiplies the 2 as well, giving $3n + 6$ | correct | distributive law a(b+c) = ab+ac (Gelfand and Shen, Algebra, distributive law): 3(n+2) = 3n+6; at n = 10, 36 against 32 |
| `screens[6].widget.options[jo]` | wrong option: Yes. The 3 only goes with the $n$ next to it / why: You let the 3 multiply only the $n$. The rectangle is 3 tall all the way across. | correct | distributive law a(b+c) = ab+ac (Gelfand and Shen, Algebra, distributive law): 3(n+2) = 3n+6; at n = 10, 36 against 32 |
| `screens[6].widget.options[added]` | wrong option: No. It should be $3n + 5$ / why: You added 3 and 2 for the second term. The 3 multiplies the 2: $3 \times 2 = 6$. | correct | distributive law a(b+c) = ab+ac (Gelfand and Shen, Algebra, distributive law): 3(n+2) = 3n+6; at n = 10, 36 against 32 |
| `screens[6].widget.options[five-n]` | wrong option: No. It should be $5n$ / why: You added 3 and 2 and put $n$ after them. The 2-wide column does not depend on $n$. | correct | distributive law a(b+c) = ab+ac (Gelfand and Shen, Algebra, distributive law): 3(n+2) = 3n+6; at n = 10, 36 against 32 |
| `screens[1].widget` | tap: the three pieces of the 2-wide column have fixed area | correct | area 3 x 2 = 6 does not involve n |
| `screens[2].explain.text` | definition: expanding rewrites a bracket as separate terms; 3(n+2) = 3n+6 | correct | Gelfand and Shen, Algebra, distributive law |
| `screens[3].widget` | place: 4 by n is 4n, 4 by 5 is 20 | correct | area model |
| `screens[5].canvas` | table: -2(n-4) is 8 at n = 0 and -12 at n = 10 | correct | derivation |
| `screens[6].explain.text` | Jo's 3n + 2 is short by 4 for every n | correct | derivation: (3n+6) - (3n+2) = 4 |
| `screens[7].prose` | rule: a(b + c) = ab + ac, signs included; a minus inside stays a minus after a positive multiplier | correct | Gelfand and Shen, Algebra, distributive law; sign rules |
| `screens[8].widget` | order: 3(n+2) = (n+2)+(n+2)+(n+2) = n+n+n+2+2+2 = 3n+6 | correct | multiplication by 3 as repeated addition |
| `screens[9].explain.text` | 40 x 6.25 = 250; at 8.10 the portfolio is 324 + 250 = 574 | correct | derivation |
| `summary` | ideas, formula, trap 3(n+2) is not 3n+2 | correct | Gelfand and Shen, Algebra, distributive law |

## l4-putting-brackets-back

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[7].widget.answer` | key 4 | correct | concepts script: recomputed 4.0 |
| `screens[7].widget.wrong[two]` | slip two = 2 | correct | concepts script: named slip gives 2.0; differs from key |
| `screens[7].widget.wrong[eight]` | slip eight = 8 | correct | concepts script: named slip gives 8.0; differs from key |
| `screens[7].widget.wrong[twenty]` | slip twenty = 20 | correct | concepts script: named slip gives 20.0; differs from key |
| `screens[9].widget.answer` | key 40 | correct | concepts script: recomputed 40.0 |
| `screens[9].widget.wrong[subtract]` | slip subtract = 585 | correct | concepts script: named slip gives 585.0; differs from key |
| `screens[9].widget.wrong[times]` | slip times = 9000 | correct | concepts script: named slip gives 9000.0; differs from key |
| `screens[9].widget.wrong[add]` | slip add = 615 | correct | concepts script: named slip gives 615.0; differs from key |
| `screens[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[0].widget.options[right]` | $n + 3$ equals the source expression | correct | concepts script: sympy identity test against n + 3 |
| `screens[0].widget.options[only-n]` | $n + 12$ differs from the source expression | correct | concepts script: sympy identity test against n + 3 |
| `screens[0].widget.options[only-12]` | $4n + 3$ differs from the source expression | correct | concepts script: sympy identity test against n + 3 |
| `screens[0].widget.options[subtract]` | $n + 8$ differs from the source expression | correct | concepts script: sympy identity test against n + 3 |
| `screens[3].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[3].widget.options[right]` | $3(2n + 3)$ equals the source expression | correct | concepts script: sympy identity test against 6*n + 9 |
| `screens[3].widget.options[first-only]` | $3(2n + 9)$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 9 |
| `screens[3].widget.options[n-out]` | $3n(2 + 3)$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 9 |
| `screens[3].widget.options[six]` | $6(n + 9)$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 9 |
| `screens[4].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[4].widget.options[right]` | $6(2n + 3)$ equals the source expression | correct | concepts script: sympy identity test against 12*n + 18 |
| `screens[4].widget.options[two]` | $2(6n + 9)$ equals the source expression (equal in value, refused for form: not fully factorised) | correct | concepts script: sympy identity test against 12*n + 18 |
| `screens[4].widget.options[three]` | $3(4n + 6)$ equals the source expression (equal in value, refused for form: not fully factorised) | correct | concepts script: sympy identity test against 12*n + 18 |
| `screens[4].widget.options[first-only]` | $6(2n + 18)$ differs from the source expression | correct | concepts script: sympy identity test against 12*n + 18 |
| `screens[5].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[5].widget.options[right]` | $7(n + 1)$ equals the source expression | correct | concepts script: sympy identity test against 7*n + 7 |
| `screens[5].widget.options[nothing]` | $7n$ differs from the source expression | correct | concepts script: sympy identity test against 7*n + 7 |
| `screens[5].widget.options[undivided]` | $7(n + 7)$ differs from the source expression | correct | concepts script: sympy identity test against 7*n + 7 |
| `screens[5].widget.options[added]` | $14n$ differs from the source expression | correct | concepts script: sympy identity test against 7*n + 7 |
| `quiz[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[0].widget.options[right]` | $3(2n + 5)$ equals the source expression | correct | concepts script: sympy identity test against 6*n + 15 |
| `quiz[0].widget.options[first-only]` | $3(2n + 15)$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 15 |
| `quiz[0].widget.options[n-out]` | $3n(2 + 5)$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 15 |
| `quiz[0].widget.options[six]` | $6(n + 15)$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 15 |
| `quiz[1].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[1].widget.options[right]` | $10(2n - 3)$ equals the source expression | correct | concepts script: sympy identity test against 20*n - 30 |
| `quiz[1].widget.options[not-fully]` | $5(4n - 6)$ equals the source expression (equal in value, refused for form: not fully factorised) | correct | concepts script: sympy identity test against 20*n - 30 |
| `quiz[1].widget.options[sign]` | $10(2n + 3)$ differs from the source expression | correct | concepts script: sympy identity test against 20*n - 30 |
| `quiz[1].widget.options[first-only]` | $10(2n - 30)$ differs from the source expression | correct | concepts script: sympy identity test against 20*n - 30 |
| `quiz[2].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[2].widget.options[right]` | $9(n + 1)$ equals the source expression | correct | concepts script: sympy identity test against 9*n + 9 |
| `quiz[2].widget.options[nothing]` | $9n$ differs from the source expression | correct | concepts script: sympy identity test against 9*n + 9 |
| `quiz[2].widget.options[undivided]` | $9(n + 9)$ differs from the source expression | correct | concepts script: sympy identity test against 9*n + 9 |
| `quiz[2].widget.options[added]` | $18n$ differs from the source expression | correct | concepts script: sympy identity test against 9*n + 9 |
| `quiz[3].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[3].widget.options[right]` | $n(n + 4)$ equals the source expression | correct | concepts script: sympy identity test against n**2 + 4*n |
| `quiz[3].widget.options[four-out]` | $4n(n + 1)$ differs from the source expression | correct | concepts script: sympy identity test against n**2 + 4*n |
| `quiz[3].widget.options[undivided]` | $n(n + 4n)$ differs from the source expression | correct | concepts script: sympy identity test against n**2 + 4*n |
| `quiz[3].widget.options[square-out]` | $n^2(1 + 4)$ differs from the source expression | correct | concepts script: sympy identity test against n**2 + 4*n |
| `screens[6].widget.options[right]` | key: No. Expanding gives $5n + 50$ | correct | expanding 5(n+10) gives 5n+50, not 5n+10; correct form 5(n+2) |
| `screens[6].widget.options[kim]` | wrong option: Yes. The 5 only multiplies the $n$ / why: You let the outside 5 multiply only the $n$. It multiplies the 10 too: $5 \times 10 = 50$. | correct | expanding 5(n+10) gives 5n+50, not 5n+10; correct form 5(n+2) |
| `screens[6].widget.options[n-out]` | wrong option: No. It should be $5n(1 + 2)$ / why: 10 has no $n$ in it, so $n$ cannot come out of it. | correct | expanding 5(n+10) gives 5n+50, not 5n+10; correct form 5(n+2) |
| `screens[6].widget.options[subtract]` | wrong option: No. It should be $5(n + 5)$ / why: You took 5 away from 10. Divide instead: $10 \div 5 = 2$. | correct | expanding 5(n+10) gives 5n+50, not 5n+10; correct form 5(n+2) |
| `screens[1].widget` | tap: heights 1 and 3 leave whole widths for 6n and 9; table rows 6n,9 / 3n,4.5 / 2n,3 / n,1.5 | correct | common factors of 6 and 9 are 1 and 3 |
| `screens[1].explain.text` | definition: highest common factor; HCF(6, 9) = 3 | correct | gcd(6, 9) = 3 |
| `screens[2].prose` | definition: factorising turns a sum back into a bracket; place 5(n + 4) | correct | standard GCSE algebra text, factorising |
| `screens[4].prose` | factorise fully means take out the highest common factor; factor lists of 12 and 18 | correct | divisors of 12: 1,2,3,4,6,12; of 18: 1,2,3,6,9,18; gcd 6 |
| `screens[5].explain.text` | a term equal to the factor leaves a 1; 7n alone would drop 7 from every value | correct | derivation: 7(n+1) - 7n = 7 |
| `screens[7].prose` | rule: ab + ac = a(b + c); expand to check | correct | Gelfand and Shen, Algebra, distributive law |
| `screens[8].widget` | order: 12n+18 = 6(2n) + 6(3) = 6(2n+3); check by expanding | correct | derivation |
| `screens[9].explain.text` | definition: break-even where profit is zero; 15n - 600 = 15(n - 40); table -300, 300, 900 | correct | derivation at n = 20, 60, 100 |
| `summary` | ideas, formula, trap 5n + 10 is not 5(n + 10) | correct | expand: 5n + 50 |

## l5-keeping-the-balance

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[5].widget.points[0].target` | target 11 | correct | concepts script: recomputed 11 |
| `screens[5].widget.wrong[subtracted]` | slip region 4.5 to 5.5 | correct | concepts script: named slip gives 5; key outside the region |
| `screens[9].widget.answer` | key 32.15 | correct | concepts script: recomputed 32.15 |
| `screens[9].widget.wrong[times]` | slip times = 51440 | correct | concepts script: named slip gives 51440.0; differs from key |
| `screens[9].widget.wrong[minus]` | slip minus = 1246 | correct | concepts script: named slip gives 1246.0; differs from key |
| `screens[9].widget.wrong[flipped]` | slip flipped = 0.0311 | correct | concepts script: named slip gives 0.0311; differs from key |
| `quiz[0].widget.answer` | key 6.35 | correct | concepts script: recomputed 6.35 |
| `quiz[0].widget.wrong[added]` | slip added = 11.85 | correct | concepts script: named slip gives 11.85; differs from key |
| `quiz[1].widget.answer` | key 4.5 | correct | concepts script: recomputed 4.5 |
| `quiz[1].widget.wrong[multiplied]` | slip multiplied = 162 | correct | concepts script: named slip gives 162.0; differs from key |
| `quiz[1].widget.wrong[subtracted]` | slip subtracted = 21 | correct | concepts script: named slip gives 21.0; differs from key |
| `quiz[1].widget.wrong[flipped]` | slip flipped = 0.2222 | correct | concepts script: named slip gives 0.2222; differs from key |
| `quiz[2].widget.answer` | key 12.6 | correct | concepts script: recomputed 12.6 |
| `quiz[2].widget.wrong[divided]` | slip divided = 1.4 | correct | concepts script: named slip gives 1.4; differs from key |
| `screens[7].widget.options[add]` | key: Add 7.5 to both sides | correct | x - 7.5 = 12 gives x = 19.5; subtracting again gives x - 15 = 4.5 |
| `screens[7].widget.options[sub]` | wrong option: Subtract 7.5 from both sides / why: You repeated the operation already there. That gives $x - 15 = 4.5$, further from $x$ alon... | correct | x - 7.5 = 12 gives x = 19.5; subtracting again gives x - 15 = 4.5 |
| `screens[7].widget.options[one-side]` | wrong option: Add 7.5 to the left side only / why: Changing one side only tips the scale. The right side must gain 7.5 too. | correct | x - 7.5 = 12 gives x = 19.5; subtracting again gives x - 15 = 4.5 |
| `screens[7].widget.options[divide]` | wrong option: Divide both sides by 7.5 / why: $x$ was not multiplied by 7.5. The 7.5 was taken away, so add it back. | correct | x - 7.5 = 12 gives x = 19.5; subtracting again gives x - 15 = 4.5 |
| `quiz[3].widget.options[one-side]` | key: Took 8 off the left side only | correct | x + 8 = 20 gives x = 12; writing x = 20 changed the left side only |
| `quiz[3].widget.options[both]` | wrong option: Took 8 off both sides / why: Taking 8 off both sides gives $x = 12$, not 20. | correct | x + 8 = 20 gives x = 12; writing x = 20 changed the left side only |
| `quiz[3].widget.options[added]` | wrong option: Added 8 to both sides / why: That gives $x + 16 = 28$. Mo's line has no 16 or 28. | correct | x + 8 = 20 gives x = 12; writing x = 20 changed the left side only |
| `screens[1..4].widget` | balance targets: x+5 = 12 gives 7; 3x = 21 gives 7; 4x = 6 gives 1.5; x+4 = 10 gives 6 | correct | derivation; grade is either way round (balance.js header) |
| `screens[2].prose` | definitions: an equation is a level scale; solving is finding x | correct | Gelfand and Shen, Algebra, equations; standard GCSE algebra text |
| `screens[4].explain.text` | lifting the 4 off one pan only tips the scale; x = 10 is false | correct | x = 6 |
| `screens[6].widget` | manipulate x/4 = 5: times 4 gives x = 20; divide again x/16 = 5/4; subtract 4 gives x/4 - 4 = 1 | correct | derivation, each state |
| `screens[7].prose` | definition: inverse operation; the four one-step rules x+a=b, x-a=b, ax=b, x/a=b | correct | standard GCSE algebra text; ax = b needs a != 0, said in the summary note |
| `screens[8].widget` | order: x + 2.5 = 9, subtract 2.5, x = 6.5, check | correct | derivation |
| `summary.formula` | a = b gives a+c = b+c, a-c = b-c, ac = bc, a/c = b/c; divide only by a number that is not zero | correct | Gelfand and Shen, Algebra, equations: equal quantities treated alike stay equal; division by zero excluded |

## l6-undoing-in-reverse

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[1].widget.rows cell 0` | cell key 32 | correct | concepts script: recomputed 32.0 |
| `screens[1].widget.rows cell 1` | cell key 8 | correct | concepts script: recomputed 8.0 |
| `screens[3].widget.answer` | key 6 | correct | concepts script: recomputed 6.0 |
| `screens[3].widget.wrong[half-divided]` | slip half-divided = 1.5 | correct | concepts script: named slip gives 1.5; differs from key |
| `screens[3].widget.wrong[added]` | slip added = 9 | correct | concepts script: named slip gives 9.0; differs from key |
| `screens[3].widget.wrong[multiplied]` | slip multiplied = 96 | correct | concepts script: named slip gives 96.0; differs from key |
| `screens[4].widget.answer` | key 25 | correct | concepts script: recomputed 25.0 |
| `screens[4].widget.wrong[wrong-order]` | slip wrong-order = 21 | correct | concepts script: named slip gives 21.0; differs from key |
| `screens[4].widget.wrong[divided]` | slip divided = 1 | correct | concepts script: named slip gives 1.0; differs from key |
| `screens[4].widget.wrong[plus]` | slip plus = 29 | correct | concepts script: named slip gives 29.0; differs from key |
| `screens[5].widget.answer` | key -4 | correct | concepts script: recomputed -4.0 |
| `screens[5].widget.wrong[sign]` | slip sign = 4 | correct | concepts script: named slip gives 4.0; differs from key |
| `screens[5].widget.wrong[added]` | slip added = 11 | correct | concepts script: named slip gives 11.0; differs from key |
| `screens[8].widget.answer` | key 300 | correct | concepts script: recomputed 300.0 |
| `screens[8].widget.wrong[added-fee]` | slip added-fee = 305.88 | correct | concepts script: named slip gives 305.8824; differs from key |
| `screens[8].widget.wrong[no-fee]` | slip no-fee = 302.94 | correct | concepts script: named slip gives 302.9412; differs from key |
| `screens[8].widget.wrong[divide-first]` | slip divide-first = 290.44 | correct | concepts script: named slip gives 290.4412; differs from key |
| `quiz[0].widget.answer` | key 6.5 | correct | concepts script: recomputed 6.5 |
| `quiz[0].widget.wrong[added]` | slip added = 10.1667 | correct | concepts script: named slip gives 10.1667; differs from key |
| `quiz[0].widget.wrong[half-divided]` | slip half-divided = -2.6667 | correct | concepts script: named slip gives -2.6667; differs from key |
| `quiz[1].widget.answer` | key 35 | correct | concepts script: recomputed 35.0 |
| `quiz[1].widget.wrong[subtracted]` | slip subtracted = 5 | correct | concepts script: named slip gives 5.0; differs from key |
| `quiz[1].widget.wrong[divided]` | slip divided = 1.4 | correct | concepts script: named slip gives 1.4; differs from key |
| `quiz[2].widget.answer` | key 4 | correct | concepts script: recomputed 4.0 |
| `quiz[2].widget.wrong[subtracted]` | slip subtracted = 0.5 | correct | concepts script: named slip gives 0.5; differs from key |
| `quiz[3].widget.answer` | key 10 | correct | concepts script: recomputed 10.0 |
| `quiz[3].widget.wrong[wrong-order]` | slip wrong-order = 14 | correct | concepts script: named slip gives 14.0; differs from key |
| `quiz[3].widget.wrong[divided]` | slip divided = 5.5 | correct | concepts script: named slip gives 5.5; differs from key |
| `screens[6].widget.options[add]` | key: Add 4 to both sides | correct | 7x - 4 = 31: adding 4 gives 7x = 35; dividing first gives x - 4/7 = 31/7 |
| `screens[6].widget.options[divide]` | wrong option: Divide both sides by 7 / why: That is allowed, but it leaves $x - \tfrac{4}{7} = \tfrac{31}{7}$. Clear the $-4$ first. | correct | 7x - 4 = 31: adding 4 gives 7x = 35; dividing first gives x - 4/7 = 31/7 |
| `screens[6].widget.options[sub]` | wrong option: Subtract 4 from both sides / why: The 4 is already being subtracted. Adding it back undoes it. | correct | 7x - 4 = 31: adding 4 gives 7x = 35; dividing first gives x - 4/7 = 31/7 |
| `screens[0].widget` | balance 3x + 4 = 19: target 5; dividing first makes the 4 into 1.33 | correct | derivation: 4/3 |
| `screens[1].prose` | rule: undo the steps in reverse order, the last step first | correct | standard GCSE algebra text, inverse operations (function machine) |
| `screens[2].widget` | manipulate 5x - 7 = 18: 5x = 25, x = 5; x - 7/5 = 18/5, x = 25/5; 5x - 14 = 11; 5x - 5 = 20 | correct | derivation, each state |
| `screens[3].explain.text` | dividing first is fine only if every term is divided: x + 1.5 = 7.5 | correct | derivation |
| `screens[4].explain.text` | x/3 + 2 = 9 gives 21; (x+2)/3 = 9 gives 25 | correct | derivation |
| `screens[6].prose` | general route ax + b = c, x = (c - b)/a | correct | derivation; a != 0 stated in the summary note |
| `screens[7].widget` | order: 3(x-2)+5 = 20, 3(x-2) = 15, x-2 = 5, x = 7; dividing first would leave 5/3 | correct | derivation |
| `summary` | ideas, formula x = (c - b)/a with a != 0, trap x + 1.5 = 7.5 | correct | derivation |

## l7-unknowns-both-sides

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[3].widget.answer` | key 3 | correct | concepts script: recomputed 3.0 |
| `screens[3].widget.wrong[kept-sign]` | slip kept-sign = 1.6667 | correct | concepts script: named slip gives 1.6667; differs from key |
| `screens[3].widget.wrong[added-three]` | slip added-three = 4.2 | correct | concepts script: named slip gives 4.2; differs from key |
| `screens[3].widget.wrong[two-slips]` | slip two-slips = 2.3333 | correct | concepts script: named slip gives 2.3333; differs from key |
| `screens[7].widget.rows cell 0` | cell key 20 | correct | concepts script: recomputed 20.0 |
| `screens[7].widget.rows cell 1` | cell key 23 | correct | concepts script: recomputed 23.0 |
| `screens[7].widget.rows cell 2` | cell key 25 | correct | concepts script: recomputed 25.0 |
| `screens[7].widget.rows cell 3` | cell key 25 | correct | concepts script: recomputed 25.0 |
| `screens[8].widget.answer` | key 12.82 | correct | concepts script: recomputed 12.82 |
| `screens[8].widget.wrong[short-as-long]` | slip short-as-long = 14.5 | correct | concepts script: named slip gives 14.5; differs from key |
| `screens[8].widget.wrong[average]` | slip average = 12.75 | correct | concepts script: named slip gives 12.75; differs from key |
| `quiz[0].widget.answer` | key 5 | correct | concepts script: recomputed 5.0 |
| `quiz[0].widget.wrong[kept-sign]` | slip kept-sign = 1.1538 | correct | concepts script: named slip gives 1.1538; differs from key |
| `quiz[0].widget.wrong[constant-sign]` | slip constant-sign = 3 | correct | concepts script: named slip gives 3.0; differs from key |
| `quiz[1].widget.answer` | key 10 | correct | concepts script: recomputed 10.0 |
| `quiz[1].widget.wrong[bracket]` | slip bracket = 6.5 | correct | concepts script: named slip gives 6.5; differs from key |
| `quiz[3].widget.answer` | key 5.2 | correct | concepts script: recomputed 5.2 |
| `quiz[3].widget.wrong[kept-sign]` | slip kept-sign = 2.6 | correct | concepts script: named slip gives 2.6; differs from key |
| `screens[5].widget.options[none]` | key: No value of $x$ works | correct | 4x + 7 = 4x + 3 reduces to 7 = 3: no solution (a linear equation ax+b = cx+d with a = c, b != d) |
| `screens[5].widget.options[zero]` | wrong option: $x = 0$ / why: At $x = 0$ the sides are 7 and 3. Taking $4x$ from both leaves $7 = 3$, which no $x$ can f... | correct | 4x + 7 = 4x + 3 reduces to 7 = 3: no solution (a linear equation ax+b = cx+d with a = c, b != d) |
| `screens[5].widget.options[all]` | wrong option: Every value of $x$ works / why: That happens when both sides match exactly, such as $4x + 7 = 4x + 7$. Here 7 and 3 differ... | correct | 4x + 7 = 4x + 3 reduces to 7 = 3: no solution (a linear equation ax+b = cx+d with a = c, b != d) |
| `screens[5].widget.options[four]` | wrong option: $x = 4$ / why: You worked out $7 - 3 = 4$, but that is not $x$. The $x$ terms cancelled, so there is noth... | correct | 4x + 7 = 4x + 3 reduces to 7 = 3: no solution (a linear equation ax+b = cx+d with a = c, b != d) |
| `quiz[2].widget.options[all]` | key: Every value of $x$ | correct | 3x + 5 = 3x + 5 reduces to 5 = 5: an identity, true for every x |
| `quiz[2].widget.options[none]` | wrong option: No value of $x$ / why: Removing $3x$ leaves $5 = 5$, which is true, not false. | correct | 3x + 5 = 3x + 5 reduces to 5 = 5: an identity, true for every x |
| `quiz[2].widget.options[zero]` | wrong option: Only $x = 0$ / why: 0 works, but so does every other number. Try $x = 2$. | correct | 3x + 5 = 3x + 5 reduces to 5 = 5: an identity, true for every x |
| `screens[0..1].widget` | balance 5x+2 = 2x+14 gives 4 (both sides 22); 3x+10 = 7x+2 gives 2 | correct | derivation; target accepted either way round |
| `screens[2].widget` | manipulate 6x-5 = 2x+11: 4x-5 = 11, 4x = 16, x = 4; 8x-5 = 4x+11; one side only 6x-5 = 11; x - 5/4 = 11/4 | correct | derivation, each state; the one-side move is not equivalent |
| `screens[3].explain.text` | "move it and change its sign" is short for subtracting the same from both sides | correct | Gelfand and Shen, Algebra, moving a term across the equals sign |
| `screens[4].widget` | manipulate 3(x+4) = 5(x-2): 3x+12 = 5x-10, 22 = 2x, x = 11 (both 45); other route -2x = -22; mis-expansion ends at x = 3 with 21 against 5 | correct | derivation, each state |
| `screens[5].explain.text` | if the x terms cancel: a false line means no solution, a true line means every x works | correct | standard GCSE algebra text: ax + b = ax + d has no solution if b != d and is an identity if b = d |
| `screens[6].widget` | order 5(x-1) = 2x+13: 5x-5 = 2x+13, 3x-5 = 13, 3x = 18, x = 6; the route solves any linear equation whose x terms do not cancel | correct | derivation; general solution (d - b)/(a - c), a != c |
| `screens[8].explain.text` | 200p - 2480 = 3930 - 300p, 500p = 6410, p = 12.82, each side 84.00; a short gains as the price falls | correct | derivation: 200(0.42) = 300(0.28) = 84 |
| `summary` | ideas; formula x = (d - b)/(a - c) needs a != c; when a = c no solution or every x | correct | derivation |

## l8-clearing-fractions

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.answer` | key 12 | correct | concepts script: recomputed 12.0 |
| `screens[0].widget.wrong[times-six]` | slip times-six = 60 | correct | concepts script: named slip gives 60.0; differs from key |
| `screens[0].widget.wrong[one-sixth]` | slip one-sixth = 2 | correct | concepts script: named slip gives 2.0; differs from key |
| `screens[0].widget.wrong[added-denoms]` | slip added-denoms = 50 | correct | concepts script: named slip gives 50.0; differs from key |
| `screens[2].widget.answer` | key 11 | correct | concepts script: recomputed 11.0 |
| `screens[2].widget.wrong[lost-bracket]` | slip lost-bracket = 3 | correct | concepts script: named slip gives 3.0; differs from key |
| `screens[2].widget.wrong[swapped]` | slip swapped = -10 | correct | concepts script: named slip gives -10.0; differs from key |
| `screens[3].widget.answer` | key 10 | correct | concepts script: recomputed 10.0 |
| `screens[3].widget.wrong[fractions-only]` | slip fractions-only = 1.6667 | correct | concepts script: named slip gives 1.6667; differs from key |
| `screens[3].widget.wrong[missed-one]` | slip missed-one = 8.3333 | correct | concepts script: named slip gives 8.3333; differs from key |
| `screens[3].widget.wrong[missed-four]` | slip missed-four = 3.3333 | correct | concepts script: named slip gives 3.3333; differs from key |
| `screens[4].widget.answer` | key 6 | correct | concepts script: recomputed 6.0 |
| `screens[4].widget.wrong[missed-term]` | slip missed-term = 5.1 | correct | concepts script: named slip gives 5.1; differs from key |
| `screens[4].widget.wrong[sign]` | slip sign = 4 | correct | concepts script: named slip gives 4.0; differs from key |
| `screens[7].widget.answer` | key 21000 | correct | concepts script: recomputed 21000.0 |
| `screens[7].widget.wrong[invested]` | slip invested = 15000 | correct | concepts script: named slip gives 15000.0; differs from key |
| `screens[7].widget.wrong[stopped]` | slip stopped = 105000 | correct | concepts script: named slip gives 105000.0; differs from key |
| `screens[7].widget.wrong[times]` | slip times = 5104.17 | correct | concepts script: named slip gives 5104.1667; differs from key |
| `quiz[0].widget.answer` | key 6 | correct | concepts script: recomputed 6.0 |
| `quiz[0].widget.wrong[added-denoms]` | slip added-denoms = 32 | correct | concepts script: named slip gives 32.0; differs from key |
| `quiz[1].widget.answer` | key 15 | correct | concepts script: recomputed 15.0 |
| `quiz[1].widget.wrong[missed-two]` | slip missed-two = 1 | correct | concepts script: named slip gives 1.0; differs from key |
| `quiz[2].widget.answer` | key 6 | correct | concepts script: recomputed 6.0 |
| `quiz[2].widget.wrong[sign]` | slip sign = -2 | correct | concepts script: named slip gives -2.0; differs from key |
| `screens[5].widget.options[twelve]` | key: 12 | correct | lcm(4, 6) = 12; 24 is a common multiple but not the least; 10 and 6 are not common multiples |
| `screens[5].widget.options[product]` | wrong option: 24 / why: 24 clears both fractions, but it is not the smallest. 4 and 6 both divide 12. | correct | lcm(4, 6) = 12; 24 is a common multiple but not the least; 10 and 6 are not common multiples |
| `screens[5].widget.options[sum]` | wrong option: 10 / why: You added the denominators. 10 is not a multiple of 4 or 6. | correct | lcm(4, 6) = 12; 24 is a common multiple but not the least; 10 and 6 are not common multiples |
| `screens[5].widget.options[six]` | wrong option: 6 / why: 6 clears the sixths but leaves $\tfrac{6x}{4} = \tfrac{3x}{2}$. | correct | lcm(4, 6) = 12; 24 is a common multiple but not the least; 10 and 6 are not common multiples |
| `quiz[3].widget.options[top]` | key: The 3 should multiply the whole top: $3(x + 1) = 3x + 3$ | correct | 6(x+1)/2 = 3(x+1) = 3x+3; correct line 5x + 3 = 24, x = 4.2 |
| `quiz[3].widget.options[four]` | wrong option: The 4 should have stayed as 4 / why: The 4 is a term too. It must be multiplied by 6, so 24 is right. | correct | 6(x+1)/2 = 3(x+1) = 3x+3; correct line 5x + 3 = 24, x = 4.2 |
| `quiz[3].widget.options[lcd]` | wrong option: 6 is the wrong number to multiply by / why: 6 is the lowest common denominator of 2 and 3, so it is the right choice. | correct | 6(x+1)/2 = 3(x+1) = 3x+3; correct line 5x + 3 = 24, x = 4.2 |
| `screens[1].widget` | manipulate x/2 + x/3 = 10: 3x + 2x = 60, 5x = 60, x = 12; left only gives x = 2 (fails); times 5 gives 5x/2 + 5x/3 = 50 | correct | derivation, each state |
| `screens[1].explain.text` | definition: 6 is the lowest common denominator of 2 and 3 | correct | lcm(2, 3) = 6 |
| `screens[3].explain.text` | times 6 every term: 4x - 24 = x + 6; both sides 8/3 at x = 10 | correct | derivation |
| `screens[4].prose` | decimals are fractions: 0.2 = 2/10; times 10 clears one decimal place | correct | place value |
| `screens[5].prose` | definition: lowest common denominator is the lowest common multiple of the denominators | correct | standard GCSE algebra text, adding fractions |
| `screens[6].widget` | order (x-3)/2 + x/5 = 9: 5(x-3)+2x = 90, 7x-15 = 90, 7x = 105, x = 15 | correct | derivation; check 6 + 3 = 9 |
| `screens[7].explain.text` | 12C - 4C - 3C = 105000, C = 21000; fund 7000, bonds 5250, cash 8750 | correct | derivation |
| `summary` | ideas; formula x/a + x/b = c gives bx + ax = abc; multiplying by ab always works | correct | derivation; a and b are denominators so non-zero |

## l9-story-to-equation

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.rows cell 0` | cell key 12.45 | correct | concepts script: recomputed 12.45 |
| `screens[0].widget.rows cell 1` | cell key 14.3 | correct | concepts script: recomputed 14.3 |
| `screens[0].widget.rows cell 2` | cell key 16.15 | correct | concepts script: recomputed 16.15 |
| `screens[2].widget.answer` | key 120 | correct | concepts script: recomputed 120.0 |
| `screens[2].widget.wrong[no-double]` | slip no-double = 171.43 | correct | concepts script: named slip gives 171.4286; differs from key |
| `screens[2].widget.wrong[other-batch]` | slip other-batch = 240 | correct | concepts script: named slip gives 240.0; differs from key |
| `screens[2].widget.wrong[all]` | slip all = 360 | correct | concepts script: named slip gives 360.0; differs from key |
| `screens[3].widget.answer` | key 11 | correct | concepts script: recomputed 11.0 |
| `screens[3].widget.wrong[reversed]` | slip reversed = -6 | correct | concepts script: named slip gives -6.0; differs from key |
| `screens[3].widget.wrong[bracket]` | slip bracket = 13.5 | correct | concepts script: named slip gives 13.5; differs from key |
| `screens[3].widget.wrong[subtracted]` | slip subtracted = 6 | correct | concepts script: named slip gives 6.0; differs from key |
| `screens[5].widget.answer` | key 200 | correct | concepts script: recomputed 200.0 |
| `screens[5].widget.wrong[no-commission]` | slip no-commission = 201 | correct | concepts script: named slip gives 201.0; differs from key |
| `screens[5].widget.wrong[percent-as-whole]` | slip percent-as-whole = 134 | correct | concepts script: named slip gives 134.0; differs from key |
| `screens[6].widget.answer` | key 185 | correct | concepts script: recomputed 185.0 |
| `screens[6].widget.wrong[rounded-up]` | slip rounded-up = 186 | correct | concepts script: named slip gives 186.0; differs from key |
| `screens[6].widget.wrong[unrounded]` | slip unrounded = 185.94 | correct | concepts script: named slip gives 185.9453; differs from key |
| `screens[8].widget.answer` | key 38 | correct | concepts script: recomputed 38.0 |
| `screens[8].widget.wrong[one-way]` | slip one-way = 30 | correct | concepts script: named slip gives 30.0; differs from key |
| `screens[8].widget.wrong[rounded-down]` | slip rounded-down = 37 | correct | concepts script: named slip gives 37.0; differs from key |
| `screens[8].widget.wrong[unrounded]` | slip unrounded = 37.5 | correct | concepts script: named slip gives 37.5; differs from key |
| `screens[8].widget.wrong[no-fees]` | slip no-fees = 25 | correct | concepts script: named slip gives 25.0; differs from key |
| `quiz[1].widget.answer` | key 100 | correct | concepts script: recomputed 100.0 |
| `quiz[1].widget.wrong[added-fee]` | slip added-fee = 106 | correct | concepts script: named slip gives 106.0; differs from key |
| `quiz[1].widget.wrong[no-fee]` | slip no-fee = 103 | correct | concepts script: named slip gives 103.0; differs from key |
| `quiz[2].widget.answer` | key 4 | correct | concepts script: recomputed 4.0 |
| `quiz[2].widget.wrong[no-per-user]` | slip no-per-user = 2.5 | correct | concepts script: named slip gives 2.5; differs from key |
| `quiz[2].widget.wrong[added]` | slip added = 1.82 | correct | concepts script: named slip gives 1.8182; differs from key |
| `quiz[3].widget.answer` | key 24 | correct | concepts script: recomputed 24.0 |
| `quiz[3].widget.wrong[added]` | slip added = 36 | correct | concepts script: named slip gives 36.0; differs from key |
| `quiz[3].widget.wrong[halved]` | slip halved = 6 | correct | concepts script: named slip gives 6.0; differs from key |
| `screens[1].widget.options[right]` | key: $3.20 + 1.85m = 16.15$ | correct | fare = 3.20 + 1.85m; the other three forms give m different from 7 |
| `screens[1].widget.options[swapped]` | wrong option: $1.85 + 3.20m = 16.15$ / why: You swapped the start charge and the rate. The 3.20 is paid once; the 1.85 is paid per mil... | correct | fare = 3.20 + 1.85m; the other three forms give m different from 7 |
| `screens[1].widget.options[every-mile]` | wrong option: $(3.20 + 1.85)m = 16.15$ / why: That charges the 3.20 start fee every mile. It is paid once. | correct | fare = 3.20 + 1.85m; the other three forms give m different from 7 |
| `screens[1].widget.options[added]` | wrong option: $1.85m = 16.15 + 3.20$ / why: You added the start charge to the fare. The fare already includes it, so it belongs beside... | correct | fare = 3.20 + 1.85m; the other three forms give m different from 7 |
| `screens[4].widget.options[right]` | key: $30 + 12m = 186$ | correct | 30 + 12m = 186 gives m = 13; the fee is paid once |
| `screens[4].widget.options[swapped]` | wrong option: $12 + 30m = 186$ / why: You swapped the charges. The £12 is paid each month, so it multiplies $m$. | correct | 30 + 12m = 186 gives m = 13; the fee is paid once |
| `screens[4].widget.options[every-month]` | wrong option: $42m = 186$ / why: You charged the connection fee every month. It is paid once. | correct | 30 + 12m = 186 gives m = 13; the fee is paid once |
| `screens[4].widget.options[added]` | wrong option: $12m = 186 + 30$ / why: You added the fee to the total. The £186 already includes it. | correct | 30 + 12m = 186 gives m = 13; the fee is paid once |
| `quiz[0].widget.options[right]` | key: $4n + 3 = 31$ | correct | "three more than four times a number" is 4n + 3; n = 7 |
| `quiz[0].widget.options[swapped]` | wrong option: $3n + 4 = 31$ / why: You swapped the 3 and the 4. “Four times” goes with the number. | correct | "three more than four times a number" is 4n + 3; n = 7 |
| `quiz[0].widget.options[bracket]` | wrong option: $4(n + 3) = 31$ / why: That is four times “three more than $n$”. The 3 is added after multiplying. | correct | "three more than four times a number" is 4n + 3; n = 7 |
| `quiz[0].widget.options[reversed]` | wrong option: $3 - 4n = 31$ / why: “Three more than” adds 3. It does not take $4n$ away from 3. | correct | "three more than four times a number" is 4n + 3; n = 7 |
| `screens[1].prose` | definition: forming an equation is writing the story as one line with a letter for the unknown | correct | standard GCSE algebra text, forming equations |
| `screens[3].explain.text` | "5 less than twice p" is 2p - 5; a negative price flags a reversed equation | correct | standard GCSE algebra text, translating words |
| `screens[4].prose` | once + rate x units = total | correct | linear cost model |
| `screens[5].prose` | percent of what: commission is 0.5% of the value of the shares, 0.005 x 8n; cost per share 8.04 | correct | derivation: 8 x 1.005 |
| `screens[6].explain.text` | round down for a budget: 185 cost 1,492.40, 186 cost 1,500.44 | correct | derivation |
| `screens[7].widget` | order: profit 3.40q - 0.40q - 1200 = 0, 3q = 1200, q = 400 | correct | derivation |
| `screens[8].explain.text` | round trip nets 6.00 - 2.00 = 4.00; zero at 37.5; round up to 38 | correct | derivation: fees on both sides, 2 x 100 x 0.01 |
| `summary` | ideas; break-even q = fixed cost / net earnings per unit, rounded up | correct | derivation; needs net earnings per unit positive, true in every item |

## l10-ranges-of-answers

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[4].widget.points[0].target` | target -2 | correct | concepts script: recomputed -2 |
| `screens[4].widget.wrong[outside]` | slip region -3.2 to -2.8 | correct | concepts script: named slip gives -3; key outside the region |
| `screens[4].widget.wrong[not-whole]` | slip region -2.7 to -2.3 | correct | concepts script: named slip gives -2.5; key outside the region |
| `screens[8].widget.answer` | key 21.99 | correct | concepts script: recomputed 21.99 |
| `screens[8].widget.wrong[included]` | slip included = 22.0 | correct | concepts script: named slip gives 22.0; differs from key |
| `screens[8].widget.wrong[tenth]` | slip tenth = 21.9 | correct | concepts script: named slip gives 21.9; differs from key |
| `screens[1].widget.options[five]` | wrong option: Five: 4, 5, 6, 7 and 8 / why: You counted only the whole numbers. 3.5 and 3.1 are bigger than 3 too. | correct | x > 3 is the open half-line (3, infinity): uncountably many numbers, 3 excluded, no upper end |
| `screens[1].widget.options[all]` | key: Every number above 3, too many to list | correct | x > 3 is the open half-line (3, infinity): uncountably many numbers, 3 excluded, no upper end |
| `screens[1].widget.options[from-three]` | wrong option: Every number from 3 upwards / why: That takes in 3 itself. But 3 is not bigger than 3. | correct | x > 3 is the open half-line (3, infinity): uncountably many numbers, 3 excluded, no upper end |
| `screens[1].widget.options[to-eight]` | wrong option: Every number from 3 up to 8 / why: The line stops at 8 only because the drawing does. 20 and 1,000 pass too. | correct | x > 3 is the open half-line (3, infinity): uncountably many numbers, 3 excluded, no upper end |
| `screens[2].widget.options[A]` | key: Bar A | correct | x >= 3 includes 3: closed end (filled dot), ray to the right |
| `screens[2].widget.options[B]` | wrong option: Bar B / why: B has a hollow dot, so it leaves 3 out. “At least 3” lets 3 in. | correct | x >= 3 includes 3: closed end (filled dot), ray to the right |
| `screens[2].widget.options[C]` | wrong option: Bar C / why: C runs left, to the numbers below 3. “At least 3” means 3 or more. | correct | x >= 3 includes 3: closed end (filled dot), ray to the right |
| `screens[3].widget.options[lt]` | key: $x < -1$ | correct | open end at -1, ray to the left: x < -1 |
| `screens[3].widget.options[le]` | wrong option: $x \le -1$ / why: That needs a filled dot. The hollow dot at −1 leaves −1 out. | correct | open end at -1, ray to the left: x < -1 |
| `screens[3].widget.options[gt]` | wrong option: $x > -1$ / why: The bar covers −2, −3 and so on. Those are smaller than −1, since they lie further left. | correct | open end at -1, ray to the left: x < -1 |
| `screens[3].widget.options[lt1]` | wrong option: $x < 1$ / why: You read the boundary as 1. The dot sits at −1, left of 0. | correct | open end at -1, ray to the left: x < -1 |
| `screens[5].widget.options[A]` | wrong option: Bar A / why: You followed the symbol, which points left. But $-2 < x$ says $x$ is bigger than −2, so th... | correct | -2 < x is x > -2: open end at -2, ray to the right; -4 fails since -2 < -4 is false |
| `screens[5].widget.options[B]` | key: Bar B | correct | -2 < x is x > -2: open end at -2, ray to the right; -4 fails since -2 < -4 is false |
| `screens[5].widget.options[C]` | wrong option: Bar C / why: C has a filled dot, which lets −2 in. The symbol $<$ has no line under it, so −2 is out. | correct | -2 < x is x > -2: open end at -2, ray to the right; -4 fails since -2 < -4 is false |
| `screens[6].widget.options[right]` | key: Filled dot at 6, bar running left | correct | x <= 6: closed end at 6, ray to the left |
| `screens[6].widget.options[hollow]` | wrong option: Hollow dot at 6, bar running left / why: The line under $\le$ lets 6 in, so the dot is filled. | correct | x <= 6: closed end at 6, ray to the left |
| `screens[6].widget.options[dir]` | wrong option: Filled dot at 6, bar running right / why: Less than means smaller numbers, and those lie to the left. | correct | x <= 6: closed end at 6, ray to the left |
| `screens[7].widget.options[le]` | key: $p \le 22.00$ | correct | "falls to 22.00 or lower" is p <= 22.00 |
| `screens[7].widget.options[lt]` | wrong option: $p < 22.00$ / why: You left £22.00 out. The order fires at £22.00 too: “falls to £22.00 or lower”. | correct | "falls to 22.00 or lower" is p <= 22.00 |
| `screens[7].widget.options[ge]` | wrong option: $p \ge 22.00$ / why: That covers every price at or above the stop, your £24.50 entry included. The sale is on t... | correct | "falls to 22.00 or lower" is p <= 22.00 |
| `screens[7].widget.options[entry]` | wrong option: $p \le 24.50$ / why: You used the entry price. Between £22.00 and £24.50 you still hold the share. | correct | "falls to 22.00 or lower" is p <= 22.00 |
| `quiz[0].widget.options[a]` | key: $-3$ | correct | x >= -3: -3, -2.5 and 0 pass; -3.5 and -4 fail |
| `quiz[0].widget.options[b]` | key: $-2.5$ | correct | x >= -3: -3, -2.5 and 0 pass; -3.5 and -4 fail |
| `quiz[0].widget.options[c]` | key: $0$ | correct | x >= -3: -3, -2.5 and 0 pass; -3.5 and -4 fail |
| `quiz[0].widget.options[d]` | wrong option: $-3.5$ / why: −3.5 lies left of −3, so it is smaller than −3. | correct | x >= -3: -3, -2.5 and 0 pass; -3.5 and -4 fail |
| `quiz[0].widget.options[e]` | wrong option: $-4$ / why: −4 lies left of −3. With negatives, the bigger digit is the smaller number. | imprecise | -4 is correctly a wrong pick, but the rule in its why, "With negatives, the bigger digit is the smaller number", is a digit rule that fails as stated (-19 and -21; -3.5 and -3.25) (finding 2) |
| `quiz[1].widget.options[a]` | key: $x \le 1.5$ | correct | closed end at 1.5, ray left: x <= 1.5 |
| `quiz[1].widget.options[b]` | wrong option: $x < 1.5$ / why: The dot at 1.5 is filled, so 1.5 is in. That needs $\le$. | correct | closed end at 1.5, ray left: x <= 1.5 |
| `quiz[1].widget.options[c]` | wrong option: $x \ge 1.5$ / why: The bar runs left, towards smaller numbers. That is less than. | correct | closed end at 1.5, ray left: x <= 1.5 |
| `quiz[1].widget.options[d]` | wrong option: $x \le 2$ / why: You rounded the boundary. The dot is at 1.5, halfway between 1 and 2. | correct | closed end at 1.5, ray left: x <= 1.5 |
| `quiz[2].widget.options[a]` | key: $x$ is less than 7 | correct | 7 > x is x < 7, strict |
| `quiz[2].widget.options[b]` | wrong option: $x$ is more than 7 / why: You read the symbol as pointing at $x$. But 7 is on the big side, so $x$ is the smaller on... | correct | 7 > x is x < 7, strict |
| `quiz[2].widget.options[c]` | wrong option: $x$ is at most 7 / why: At most would let 7 in. The symbol $>$ has no line under it, so 7 is out. | correct | 7 > x is x < 7, strict |
| `quiz[2].widget.options[d]` | wrong option: $x$ is at least 7 / why: This turns the meaning round and lets 7 in as well. | correct | 7 > x is x < 7, strict |
| `quiz[3].widget.options[a]` | key: $n \le 400$ | correct | "at most 400" is n <= 400 |
| `quiz[3].widget.options[b]` | wrong option: $n < 400$ / why: That bans exactly 400 shares. “At most 400” allows 400 itself. | correct | "at most 400" is n <= 400 |
| `quiz[3].widget.options[c]` | wrong option: $n \ge 400$ / why: That says 400 or more. A limit caps the position from above. | correct | "at most 400" is n <= 400 |
| `quiz[3].widget.options[d]` | wrong option: $n > 400$ / why: That is the shares that would break the limit, not the ones allowed. | correct | "at most 400" is n <= 400 |
| `screens[0].widget` | tap: whole numbers 4 to 8 satisfy x > 3; 3 fails | correct | strict inequality |
| `screens[2].prose` | definitions: inequality; solution set; hollow dot leaves the number out, filled dot keeps it in | correct | standard GCSE algebra text, inequalities on a number line |
| `screens[4].prose` | convention: whole numbers here include 0 and negatives; exam papers call them integers | correct | stated convention; integers in the GCSE sense |
| `screens[5].explain.text` | the symbol is not an arrow; -2 < x is the same as x > -2 | correct | Gelfand and Shen, Algebra, inequalities: a < b means the same as b > a |
| `screens[6].prose` | four kinds; a line under the symbol fills the dot; with x first, bigger-than runs right | correct | standard GCSE algebra text |
| `screens[8].explain.text` | with ticks of 0.01 the highest price below 22.00 is 21.99 | correct | derivation |
| `summary` | ideas; a < x means x > a | correct | Gelfand and Shen, Algebra |

## l11-one-twist

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `quiz[3].widget.answer` | key 3 | correct | concepts script: recomputed 3.0 |
| `quiz[3].widget.wrong[boundary]` | slip boundary = 2 | correct | concepts script: named slip gives 2.0; differs from key |
| `quiz[3].widget.wrong[kept]` | slip kept = 1 | correct | concepts script: named slip gives 1.0; differs from key |
| `screens[0]` | x + 4 > 9 is x > 5 | correct | concepts script: sympy.solveset gives Interval.open(5, oo) |
| `screens[1]` | 3x - 2 >= 10 is x >= 4 | correct | concepts script: sympy.solveset gives Interval(4, oo) |
| `screens[4]` | -3x > 12 is x < -4 | correct | concepts script: sympy.solveset gives Interval.open(-oo, -4) |
| `screens[5]` | 2x + 5 < 1 is x < -2 | correct | concepts script: sympy.solveset gives Interval.open(-oo, -2) |
| `screens[6]` | 5 - x/2 >= 3 is x <= 4 | correct | concepts script: sympy.solveset gives Interval(-oo, 4) |
| `screens[7]` | 7 - 2x <= 1 is x >= 3 | correct | concepts script: sympy.solveset gives Interval(3, oo) |
| `screens[8]` | -2.5n >= -600 is n <= 240 | correct | concepts script: sympy.solveset gives Interval(-oo, 240) |
| `quiz[0]` | 4x + 1 > 13 is x > 3 | correct | concepts script: sympy.solveset gives Interval.open(3, oo) |
| `quiz[1]` | -5x <= 20 is x >= -4 | correct | concepts script: sympy.solveset gives Interval(-4, oo) |
| `quiz[3]` | 10 - 3x < 4 is x > 2 | correct | concepts script: sympy.solveset gives Interval.open(2, oo) |
| `screens[3].explain.text / summary.formula.tex` | a < b gives ka > kb for k < 0, and ka < kb for k > 0 | correct | concepts script: exhaustive on a grid of 25 values each; follows from b - a > 0 times k |
| `screens[7].prose` | adding or subtracting the same number keeps the sign | correct | concepts script: exhaustive on the same grid |
| `screens[3].widget.options[kept]` | wrong option: $-6 < -15$ / why: You kept the sign. But −6 lies right of −15 on the line, so −6 is the bigger number. | correct | -3(2) = -6 and -3(5) = -15; -6 > -15 |
| `screens[3].widget.options[flip]` | key: $-6 > -15$ | correct | -3(2) = -6 and -3(5) = -15; -6 > -15 |
| `screens[3].widget.options[drop]` | wrong option: $6 > 15$ / why: You dropped the minus signs, and 6 is not bigger than 15. Multiplying by −3 makes both num... | correct | -3(2) = -6 and -3(5) = -15; -6 > -15 |
| `screens[6].widget.options[right]` | key: $x \le 4$ | correct | concepts script solution set x <= 4; x = 6 gives 2, not >= 3 |
| `screens[6].widget.options[kept]` | wrong option: $x \ge 4$ / why: You multiplied by $-2$ but kept $\ge$. Test $x = 6$: $5 - 3 = 2$, which is not $\ge 3$. | correct | concepts script solution set x <= 4; x = 6 gives 2, not >= 3 |
| `screens[6].widget.options[half]` | wrong option: $x \le 1$ / why: You divided $-2$ by $-2$. To undo $\div 2$ you multiply, so multiply both sides by $-2$: $... | correct | concepts script solution set x <= 4; x = 6 gives 2, not >= 3 |
| `screens[6].widget.options[neg]` | wrong option: $x \le -4$ / why: You multiplied the right side by 2, not $-2$: $-2 \times 2 = -4$. Multiply both sides by $... | correct | concepts script solution set x <= 4; x = 6 gives 2, not >= 3 |
| `screens[8].widget.options[right]` | key: $n \le 240$ | correct | concepts script solution set n <= 240; 300 shares lose 750 |
| `screens[8].widget.options[kept]` | wrong option: $n \ge 240$ / why: You divided by $-2.50$ and kept $\ge$. Test $n = 300$: P&L $= -750$, worse than $-600$. | correct | concepts script solution set n <= 240; 300 shares lose 750 |
| `screens[8].widget.options[sign]` | wrong option: $n \le -240$ / why: You lost a minus sign: $-600 \div -2.50 = 240$, a positive number. | correct | concepts script solution set n <= 240; 300 shares lose 750 |
| `screens[8].widget.options[both]` | wrong option: $n \ge -240$ / why: Two slips: the sign of 240 and the direction. $-600 \div -2.50 = 240$, and the sign revers... | correct | concepts script solution set n <= 240; 300 shares lose 750 |
| `quiz[0].widget.options[a]` | key: $x > 3$ | correct | concepts script solution set x > 3; 13/4 - 1 = 2.25 |
| `quiz[0].widget.options[b]` | wrong option: $x > 2.25$ / why: You divided 13 by 4 before taking the 1 away. Subtract 1 first, then divide. | correct | concepts script solution set x > 3; 13/4 - 1 = 2.25 |
| `quiz[0].widget.options[c]` | wrong option: $x < 3$ / why: You reversed the sign, but you only divided by 4, a positive number. | correct | concepts script solution set x > 3; 13/4 - 1 = 2.25 |
| `quiz[0].widget.options[d]` | wrong option: $x > 12$ / why: You stopped at $4x > 12$. Divide by 4 to get $x$ alone. | correct | concepts script solution set x > 3; 13/4 - 1 = 2.25 |
| `quiz[1].widget.options[a]` | key: $x \ge -4$ | correct | concepts script solution set x >= -4; x = -5 gives 25 |
| `quiz[1].widget.options[b]` | wrong option: $x \le -4$ / why: You divided by $-5$ and kept $\le$. Test $x = -5$: $-5 \times -5 = 25$, not $\le 20$. | correct | concepts script solution set x >= -4; x = -5 gives 25 |
| `quiz[1].widget.options[c]` | wrong option: $x \ge 4$ / why: $20 \div -5 = -4$, not 4. | correct | concepts script solution set x >= -4; x = -5 gives 25 |
| `quiz[1].widget.options[d]` | wrong option: $x \le 4$ / why: Two slips: $20 \div -5$ is $-4$, and the sign must reverse. | correct | concepts script solution set x >= -4; x = -5 gives 25 |
| `quiz[2].widget.options[a]` | key: Multiply both sides by $-2$ | correct | order is reversed exactly by a negative multiplier or divisor (Gelfand and Shen, Algebra, inequalities; concepts script grid check) |
| `quiz[2].widget.options[b]` | key: Divide both sides by $-0.5$ | correct | order is reversed exactly by a negative multiplier or divisor (Gelfand and Shen, Algebra, inequalities; concepts script grid check) |
| `quiz[2].widget.options[c]` | wrong option: Subtract 6 from both sides / why: Subtracting slides both sides the same way along the line, so their order holds. | correct | order is reversed exactly by a negative multiplier or divisor (Gelfand and Shen, Algebra, inequalities; concepts script grid check) |
| `quiz[2].widget.options[d]` | wrong option: Divide both sides by 3 when the right side is negative / why: The number on the right does not matter. Only the sign of what you divide by does, and 3 i... | correct | order is reversed exactly by a negative multiplier or divisor (Gelfand and Shen, Algebra, inequalities; concepts script grid check) |
| `quiz[2].widget.options[e]` | wrong option: Add $-4$ to both sides / why: Adding a negative is a subtraction. Both sides slide left together, so the order holds. | correct | order is reversed exactly by a negative multiplier or divisor (Gelfand and Shen, Algebra, inequalities; concepts script grid check) |
| `screens[0].widget` | tap: whole numbers 6 to 10 satisfy x + 4 > 9 | correct | concepts script: x > 5 |
| `screens[1].widget` | manipulate 3x - 2 >= 10: 3x >= 12, x >= 4; x - 2/3 >= 10/3; wrong moves 3x - 4 >= 8, 3x - 3 >= 9 | correct | derivation, each state |
| `screens[2].widget` | drag: -a = -2 and -b = -5; order flips | correct | derivation |
| `screens[3].explain.text` | rule: multiplying or dividing both sides by a negative reverses the sign; adding, subtracting and positive multipliers keep it | correct | Gelfand and Shen, Algebra, inequalities; concepts script grid check |
| `screens[4].widget` | manipulate -3x > 12: x < -4; route without a negative 0 > 12 + 3x, -12 > 3x, -4 > x; unflipped x > -4 fails at x = 0 | correct | concepts script solution set; derivation of each state |
| `screens[5].widget` | manipulate 2x + 5 < 1: 2x < -4, x < -2; a negative right side does not flip the sign | correct | concepts script solution set |
| `screens[7].widget` | order 7 - 2x <= 1: 7 <= 1 + 2x, 6 <= 2x, 3 <= x, x >= 3 | correct | concepts script solution set |
| `summary` | ideas; formula a < b gives ka > kb when k < 0; trap | correct | concepts script grid check |

## l12-trapped

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[4].widget.answer` | key 5 | correct | concepts script: recomputed 5.0 |
| `screens[4].widget.wrong[both-ends]` | slip both-ends = 6 | correct | concepts script: named slip gives 6.0; differs from key |
| `screens[4].widget.wrong[no-ends]` | slip no-ends = 4 | correct | concepts script: named slip gives 4.0; differs from key |
| `screens[4].widget.wrong[subtract]` | slip subtract = 3 | correct | concepts script: named slip gives 3.0; differs from key |
| `screens[7].widget.answer` | key 320 | correct | concepts script: recomputed 320.0 |
| `screens[7].widget.wrong[to-zero]` | slip to-zero = 120 | correct | concepts script: named slip gives 120.0; differs from key |
| `screens[7].widget.wrong[limit-only]` | slip limit-only = 200 | correct | concepts script: named slip gives 200.0; differs from key |
| `screens[7].widget.wrong[flipped]` | slip flipped = 80 | correct | concepts script: named slip gives 80.0; differs from key |
| `screens[8].widget.answer` | key 9 | correct | concepts script: recomputed 9.0 |
| `screens[8].widget.wrong[not-whole]` | slip not-whole = 9.33 | correct | concepts script: named slip gives 9.3333; differs from key |
| `screens[8].widget.wrong[no-buffer]` | slip no-buffer = 11 | correct | concepts script: named slip gives 11.0; differs from key |
| `screens[8].widget.wrong[added-buffer]` | slip added-buffer = 12 | correct | concepts script: named slip gives 12.0; differs from key |
| `screens[8].widget.wrong[rounded-up]` | slip rounded-up = 10 | correct | concepts script: named slip gives 10.0; differs from key |
| `quiz[1].widget.answer` | key 5 | correct | concepts script: recomputed 5.0 |
| `quiz[1].widget.wrong[both]` | slip both = 6 | correct | concepts script: named slip gives 6.0; differs from key |
| `quiz[1].widget.wrong[neither]` | slip neither = 4 | correct | concepts script: named slip gives 4.0; differs from key |
| `screens[3]` | 1 < 2x + 3 <= 11 is -1 < x <= 4 | correct | concepts script: sympy.solveset gives Interval.Lopen(-1, 4) |
| `screens[5]` | -3 <= 1 - 2x < 7 is -3 < x <= 2 | correct | concepts script: sympy.solveset gives Interval.Lopen(-3, 2) |
| `screens[7]` | -200 <= 120 - n <= 200 is -80 <= n <= 320 | correct | concepts script: sympy.solveset gives Interval(-80, 320) |
| `screens[8]` | 5000 - 450n >= 800 is n <= 28/3 | correct | concepts script: sympy.solveset gives Interval(-oo, 28/3) |
| `quiz[0]` | 5 <= x + 3 < 9 is 2 <= x < 6 | correct | concepts script: sympy.solveset gives Interval.Ropen(2, 6) |
| `quiz[2]` | -1 < -x <= 4 is -4 <= x < 1 | correct | concepts script: sympy.solveset gives Interval.Ropen(-4, 1) |
| `quiz[3]` | 5 < x < 2 is empty | correct | concepts script: sympy.solveset gives EmptySet |
| `screens[6].widget and explain.text` | integers in a < x <= b number b - a; closed both ends b - a + 1; open both b - a - 1 | correct | concepts script: exhaustive for -10 <= a < b <= 10 |
| `screens[1].widget.options[both]` | key: Right of −2, and at 3 or left of it | correct | x > -2 and x <= 3 is the intersection (-2, 3] |
| `screens[1].widget.options[either]` | wrong option: Anywhere on either bar / why: A spot under just one bar passes only one test. It must sit under both. | correct | x > -2 and x <= 3 is the intersection (-2, 3] |
| `screens[1].widget.options[outside]` | wrong option: Left of −2 or right of 3 / why: Those spots fail a test. Left of −2 fails the first; right of 3 fails the second. | correct | x > -2 and x <= 3 is the intersection (-2, 3] |
| `screens[2].widget.options[right]` | key: $-2 < x \le 3$ | correct | (-2, 3] is written -2 < x <= 3 |
| `screens[2].widget.options[swapped]` | wrong option: $-2 \le x < 3$ / why: You swapped the ends. The dot at −2 is hollow, so −2 is out; the dot at 3 is filled, so 3 ... | correct | (-2, 3] is written -2 < x <= 3 |
| `screens[2].widget.options[open]` | wrong option: $-2 < x < 3$ / why: That leaves 3 out. The dot at 3 is filled, so 3 belongs. | correct | (-2, 3] is written -2 < x <= 3 |
| `screens[2].widget.options[order]` | wrong option: $3 \ge x < -2$ / why: Each symbol must point the same way. Read from left to right, smallest first: $-2 < x \le ... | correct | (-2, 3] is written -2 < x <= 3 |
| `screens[6].widget.options[right]` | key: $b - a$ | correct | concepts script: integers in a < x <= b number b - a |
| `screens[6].widget.options[plus]` | wrong option: $b - a + 1$ / why: That counts both ends. But $a$ is left out by the hollow end. | correct | concepts script: integers in a < x <= b number b - a |
| `screens[6].widget.options[minus]` | wrong option: $b - a - 1$ / why: That leaves out both ends. But $b$ is kept in by the filled end. | correct | concepts script: integers in a < x <= b number b - a |
| `quiz[0].widget.options[a]` | key: $2 \le x < 6$ | correct | concepts script solution set [2, 6) |
| `quiz[0].widget.options[b]` | wrong option: $5 \le x < 6$ / why: You took 3 from the right only. The left part must lose 3 as well. | correct | concepts script solution set [2, 6) |
| `quiz[0].widget.options[c]` | wrong option: $8 \le x < 12$ / why: You added 3. To undo $+3$, subtract 3 from all three parts. | correct | concepts script solution set [2, 6) |
| `quiz[0].widget.options[d]` | wrong option: $2 < x \le 6$ / why: The signs stay where they were. Subtracting does not change which ends are in. | correct | concepts script solution set [2, 6) |
| `quiz[2].widget.options[a]` | key: $-4 \le x < 1$ | correct | concepts script solution set [-4, 1) |
| `quiz[2].widget.options[b]` | wrong option: $1 < x \le -4$ / why: You multiplied by $-1$ but kept the signs. No number is above 1 and below −4. | correct | concepts script solution set [-4, 1) |
| `quiz[2].widget.options[c]` | wrong option: $-1 < x \le 4$ / why: You dropped the minus on $x$ without changing anything else. Multiply all three parts by $... | correct | concepts script solution set [-4, 1) |
| `quiz[2].widget.options[d]` | wrong option: $-4 < x \le 1$ / why: You flipped, but the ends swapped too. The 4 came with $\le$, so −4 is the end that is kep... | correct | concepts script solution set [-4, 1) |
| `quiz[3].widget.options[a]` | key: None: no number is above 5 and below 2 | correct | concepts script: x > 5 and x < 2 is the empty set |
| `quiz[3].widget.options[b]` | wrong option: Every number between 2 and 5 / why: You read it as between 2 and 5. It asks for $x$ above 5 and below 2 at once. | correct | concepts script: x > 5 and x < 2 is the empty set |
| `quiz[3].widget.options[c]` | wrong option: 3 and 4 / why: 3 is below 5, so it fails $5 < x$. It asks for both tests at once. | correct | concepts script: x > 5 and x < 2 is the empty set |
| `quiz[3].widget.options[d]` | wrong option: Every number above 5 or below 2 / why: That would be either test. A double inequality asks for both. | correct | concepts script: x > 5 and x < 2 is the empty set |
| `screens[0].widget` | tap: whole numbers -1, 0, 1, 2, 3 pass x > -2 and x <= 3 | correct | intersection (-2, 3] |
| `screens[2].prose` | definition: double inequality, smaller limit on the left | correct | standard GCSE algebra text |
| `screens[3].widget` | manipulate 1 < 2x+3 <= 11: -2 < 2x <= 8, -1 < x <= 4; middle-only 1 < 2x <= 11; needless flip -1 > x >= 4 | correct | concepts script solution set; derivation |
| `screens[5].widget` | manipulate -4 <= -2x < 6: both signs reverse, 2 >= x > -3, that is -3 < x <= 2; 2 <= x < -3 is empty | correct | concepts script solution set |
| `screens[6].prose` | a < x <= b means x > a and x <= b; act on all three parts; a negative divisor reverses both signs | correct | Gelfand and Shen, Algebra, inequalities |
| `screens[7].explain.text` | -320 <= -n <= 80, so -80 <= n <= 320: sell up to 320 or buy up to 80 | correct | concepts script solution set |
| `screens[8].explain.text` | n <= 9 1/3; 9 contracts leave 950 free, 10 leave 500 | correct | derivation |
| `summary` | ideas; formula; note "smaller limit on the left, both symbols point the same way"; trap | correct | convention for the final written form |
| `quiz[3].explain.text` | always claim: "the smaller limit always goes on the left" | imprecise | the same lesson writes 2 >= x > -3 with the larger limit on the left (screens[5]); the limit order is tied to the direction of the symbols, not "always" (finding 3) |

## l13-changing-the-subject

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `screens[0].widget.rows cell 0` | cell key 300 | correct | concepts script: recomputed 300.0 |
| `screens[0].widget.rows cell 1` | cell key 120 | correct | concepts script: recomputed 120.0 |
| `screens[0].widget.rows cell 2` | cell key 80 | correct | concepts script: recomputed 80.0 |
| `screens[1].widget.answer` | key 2.5 | correct | concepts script: recomputed 2.5 |
| `screens[1].widget.wrong[principal]` | slip principal = 0.125 | correct | concepts script: named slip gives 0.125; differs from key |
| `screens[1].widget.wrong[rate]` | slip rate = 5000 | correct | concepts script: named slip gives 5000.0; differs from key |
| `screens[4].widget.answer` | key 300 | correct | concepts script: recomputed 300.0 |
| `screens[4].widget.wrong[price-only]` | slip price-only = 126.32 | correct | concepts script: named slip gives 126.3158; differs from key |
| `screens[4].widget.wrong[cost-only]` | slip cost-only = 218.18 | correct | concepts script: named slip gives 218.1818; differs from key |
| `screens[4].widget.wrong[added]` | slip added = 80 | correct | concepts script: named slip gives 80.0; differs from key |
| `screens[7].widget.rows cell 0` | cell key 50 | correct | concepts script: recomputed 50.0 |
| `screens[7].widget.rows cell 1` | cell key 40 | correct | concepts script: recomputed 40.0 |
| `screens[7].widget.rows cell 2` | cell key 110 | correct | concepts script: recomputed 110.0 |
| `screens[8].widget.answer` | key 500 | correct | concepts script: recomputed 500.0 |
| `screens[8].widget.wrong[no-rate]` | slip no-rate = 125 | correct | concepts script: named slip gives 125.0; differs from key |
| `screens[8].widget.wrong[times-rate]` | slip times-rate = 31.25 | correct | concepts script: named slip gives 31.25; differs from key |
| `screens[8].widget.wrong[all-times]` | slip all-times = 72000 | correct | concepts script: named slip gives 72000.0; differs from key |
| `quiz[2].widget.answer` | key 60 | correct | concepts script: recomputed 60.0 |
| `quiz[2].widget.wrong[off-exit]` | slip off-exit = 59.4 | correct | concepts script: named slip gives 59.4; differs from key |
| `quiz[2].widget.wrong[times]` | slip times = 72.6 | correct | concepts script: named slip gives 72.6; differs from key |
| `screens[5].widget.options` | exactly one correct option | correct | concepts script: count |
| `screens[5].widget.options[right]` |  \dfrac{C - 5}{2}$ equals the source expression | correct | concepts script: sympy identity test against C/2 - 5/2 |
| `screens[5].widget.options[one-term]` |  \dfrac{C}{2} - 5$ differs from the source expression | correct | concepts script: sympy identity test against C/2 - 5/2 |
| `screens[5].widget.options[added]` |  \dfrac{C + 5}{2}$ differs from the source expression | correct | concepts script: sympy identity test against C/2 - 5/2 |
| `screens[5].widget.options[order]` |  C - \dfrac{5}{2}$ differs from the source expression | correct | concepts script: sympy identity test against C/2 - 5/2 |
| `quiz[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[0].widget.options[a]` |  \dfrac{I}{Pt}$ equals the source expression | correct | concepts script: sympy identity test against I/(P*t) |
| `quiz[0].widget.options[b]` |  I - Pt$ differs from the source expression | correct | concepts script: sympy identity test against I/(P*t) |
| `quiz[0].widget.options[c]` |  \dfrac{Pt}{I}$ differs from the source expression | correct | concepts script: sympy identity test against I/(P*t) |
| `quiz[0].widget.options[d]` |  IPt$ differs from the source expression | correct | concepts script: sympy identity test against I/(P*t) |
| `quiz[1].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[1].widget.options[a]` |  \dfrac{v - u}{t}$ equals the source expression | correct | concepts script: sympy identity test against (-u + v)/t |
| `quiz[1].widget.options[b]` |  \dfrac{v}{t} - u$ differs from the source expression | correct | concepts script: sympy identity test against (-u + v)/t |
| `quiz[1].widget.options[c]` |  \dfrac{v + u}{t}$ differs from the source expression | correct | concepts script: sympy identity test against (-u + v)/t |
| `quiz[1].widget.options[d]` |  v - u - t$ differs from the source expression | correct | concepts script: sympy identity test against (-u + v)/t |
| `quiz[3].widget.options` | exactly one correct option | correct | concepts script: count |
| `quiz[3].widget.options[a]` |  \dfrac{F}{q} + c$ equals the source expression | correct | concepts script: sympy identity test against F/q + c |
| `quiz[3].widget.options[b]` |  \dfrac{F}{q} - c$ differs from the source expression | correct | concepts script: sympy identity test against F/q + c |
| `quiz[3].widget.options[c]` |  \dfrac{F - c}{q}$ differs from the source expression | correct | concepts script: sympy identity test against F/q + c |
| `quiz[3].widget.options[d]` |  Fq + c$ differs from the source expression | correct | concepts script: sympy identity test against F/q + c |
| `screens[0].prose` | convention: I = Prt, simple interest, r the yearly rate as a decimal, t in years | correct | standard GCSE algebra text, simple interest; convention stated on the screen |
| `screens[2].prose` | definitions: subject of a formula; changing the subject | correct | standard GCSE algebra text, rearranging formulae |
| `screens[2].widget` | manipulate I = Prt: I/(Pr) = t; subtracting gives I - Pr = Prt - Pr | correct | derivation |
| `screens[3].widget` | manipulate s = d/t: st = d, t = d/s; sd = d^2/t; s - d = d/t - d; st/d = 1; check 240 km at 80 km/h is 3 hours | correct | derivation, each state |
| `screens[4].explain.text` | q = F/(p - c); table -800, -400, 800 at 100, 200, 500 mugs | correct | derivation: 4q - 1200 |
| `screens[6].widget` | order: rP0 = P1 - P0, rP0 + P0 = P1, P0(1 + r) = P1, P0 = P1/(1 + r); check 55/1.1 = 50 | correct | derivation; simple return convention r = (P1 - P0)/P0 stated |
| `screens[7].feedback.byKey.r0c3` | taking 5% off 52.50 gives 49.88, which is wrong | correct | derivation: 52.50 x 0.95 = 49.875 |
| `screens[8].explain.text` | q = M/(mp); 0.25 x 48 = 12 per share | correct | derivation |
| `summary` | ideas; formula P0 = P1/(1 + r); trap | correct | derivation |
| `screens[4], screens[6], summary.formula.note` | dividing by a bracket or a letter (p - c, 1 + r, s, Pr) is done with no word that it must not be zero | imprecise | division by an expression is valid only where it is not zero (Gelfand and Shen, Algebra, equations; l5 and l6 state it for numbers): p = c, r = -1 and y = 1 in homework-3 items[4] are never excluded (finding 4) |

## review-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[4].widget.answer` | key 16 | correct | concepts script: recomputed 16.0 |
| `items[4].widget.wrong[square-3n]` | slip square-3n = 40 | correct | concepts script: named slip gives 40.0; differs from key |
| `items[4].widget.wrong[add-first]` | slip add-first = 28 | correct | concepts script: named slip gives 28.0; differs from key |
| `items[8].widget.answer` | key 40 | correct | concepts script: recomputed 40.0 |
| `items[8].widget.wrong[no-unit-cost]` | slip no-unit-cost = 20 | correct | concepts script: named slip gives 20.0; differs from key |
| `items[8].widget.wrong[added-cost]` | slip added-cost = 13.33 | correct | concepts script: named slip gives 13.3333; differs from key |
| `items[0].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[0].widget.options[right]` | $2.80 + 1.60m$ equals the source expression | correct | concepts script: sympy identity test against 8*m/5 + 14/5 |
| `items[0].widget.options[start-each]` | $4.40m$ differs from the source expression | correct | concepts script: sympy identity test against 8*m/5 + 14/5 |
| `items[0].widget.options[swapped]` | $1.60 + 2.80m$ differs from the source expression | correct | concepts script: sympy identity test against 8*m/5 + 14/5 |
| `items[0].widget.options[added]` | $2.80 + 1.60 + m$ differs from the source expression | correct | concepts script: sympy identity test against 8*m/5 + 14/5 |
| `items[1].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[1].widget.options[right]` | $6n + 24$ equals the source expression | correct | concepts script: sympy identity test against 6*n + 24 |
| `items[1].widget.options[first-only]` | $6n + 4$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 24 |
| `items[1].widget.options[added]` | $6n + 10$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 24 |
| `items[1].widget.options[all-n]` | $10n$ differs from the source expression | correct | concepts script: sympy identity test against 6*n + 24 |
| `items[2].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[2].widget.options[right]` | $6n - 5$ equals the source expression | correct | concepts script: sympy identity test against 6*n - 5 |
| `items[2].widget.options[no-signs]` | $12n + 13$ differs from the source expression | correct | concepts script: sympy identity test against 6*n - 5 |
| `items[2].widget.options[minus-2n]` | $2n - 5$ differs from the source expression | correct | concepts script: sympy identity test against 6*n - 5 |
| `items[2].widget.options[sign-9]` | $6n + 5$ differs from the source expression | wrong | the option 6n + 5 equals the wrong value as the key requires, but its why says "You added the 9"; adding the 9 gives 6n + 13, not 6n + 5 (finding 1) |
| `items[3].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[3].widget.options[right]` | $6(3n + 4)$ equals the source expression | correct | concepts script: sympy identity test against 18*n + 24 |
| `items[3].widget.options[two]` | $2(9n + 12)$ equals the source expression (equal in value, refused for form: not fully factorised) | correct | concepts script: sympy identity test against 18*n + 24 |
| `items[3].widget.options[three]` | $3(6n + 8)$ equals the source expression (equal in value, refused for form: not fully factorised) | correct | concepts script: sympy identity test against 18*n + 24 |
| `items[3].widget.options[first-only]` | $6(3n + 24)$ differs from the source expression | correct | concepts script: sympy identity test against 18*n + 24 |
| `items[5].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[5].widget.options[right]` | $-6n + 15$ equals the source expression | correct | concepts script: sympy identity test against 15 - 6*n |
| `items[5].widget.options[neg-neg]` | $-6n - 15$ differs from the source expression | correct | concepts script: sympy identity test against 15 - 6*n |
| `items[5].widget.options[first-only]` | $-6n - 5$ differs from the source expression | correct | concepts script: sympy identity test against 15 - 6*n |
| `items[5].widget.options[lost-sign]` | $6n - 15$ differs from the source expression | correct | concepts script: sympy identity test against 15 - 6*n |
| `items[6].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[6].widget.options[right]` | $7n - 4$ equals the source expression | correct | concepts script: sympy identity test against 7*n - 4 |
| `items[6].widget.options[first-only]` | $7n + 1$ differs from the source expression | correct | concepts script: sympy identity test against 7*n - 4 |
| `items[6].widget.options[sign]` | $7n + 16$ differs from the source expression | correct | concepts script: sympy identity test against 7*n - 4 |
| `items[6].widget.options[unlike]` | $3n$ differs from the source expression | correct | concepts script: sympy identity test against 7*n - 4 |
| `items[7].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[7].widget.options[right]` | $300p + 135$ equals the source expression | correct | concepts script: sympy identity test against 300*p + 135 |
| `items[7].widget.options[first-only]` | $300p + 0.45$ differs from the source expression | correct | concepts script: sympy identity test against 300*p + 135 |
| `items[7].widget.options[added]` | $300.45p$ differs from the source expression | correct | concepts script: sympy identity test against 300*p + 135 |
| `items[7].widget.options[decimal]` | $300p + 13.5$ differs from the source expression | correct | concepts script: sympy identity test against 300*p + 135 |
| `items[8].explain.text` | profit 2.25n - 90 = 2.25(n - 40) | correct | derivation |

## review-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.answer` | key 16.95 | correct | concepts script: recomputed 16.95 |
| `items[0].widget.wrong[subtracted]` | slip subtracted = 7.65 | correct | concepts script: named slip gives 7.65; differs from key |
| `items[1].widget.answer` | key 9 | correct | concepts script: recomputed 9.0 |
| `items[1].widget.wrong[subtracted]` | slip subtracted = 3.6667 | correct | concepts script: named slip gives 3.6667; differs from key |
| `items[1].widget.wrong[half-divided]` | slip half-divided = 14.3333 | correct | concepts script: named slip gives 14.3333; differs from key |
| `items[3].widget.answer` | key 5.5 | correct | concepts script: recomputed 5.5 |
| `items[3].widget.wrong[kept-sign]` | slip kept-sign = 1.5714 | correct | concepts script: named slip gives 1.5714; differs from key |
| `items[4].widget.answer` | key 24 | correct | concepts script: recomputed 24.0 |
| `items[4].widget.wrong[added-denoms]` | slip added-denoms = 98 | correct | concepts script: named slip gives 98.0; differs from key |
| `items[4].widget.wrong[no-right]` | slip no-right = 2 | correct | concepts script: named slip gives 2.0; differs from key |
| `items[5].widget.answer` | key 875 | correct | concepts script: recomputed 875.0 |
| `items[5].widget.wrong[asha]` | slip asha = 1275 | correct | concepts script: named slip gives 1275.0; differs from key |
| `items[5].widget.wrong[half]` | slip half = 1075 | correct | concepts script: named slip gives 1075.0; differs from key |
| `items[7].widget.answer` | key 13 | correct | concepts script: recomputed 13.0 |
| `items[7].widget.wrong[minus-slip]` | slip minus-slip = 19 | correct | concepts script: named slip gives 19.0; differs from key |
| `items[7].widget.wrong[lost-bracket]` | slip lost-bracket = 23 | correct | concepts script: named slip gives 23.0; differs from key |
| `items[8].widget.answer` | key 300 | correct | concepts script: recomputed 300.0 |
| `items[8].widget.wrong[added]` | slip added = 128.57 | correct | concepts script: named slip gives 128.5714; differs from key |
| `items[8].widget.wrong[one-rate]` | slip one-rate = 180 | correct | concepts script: named slip gives 180.0; differs from key |
| `items[8].widget.wrong[pence]` | slip pence = 3 | correct | concepts script: named slip gives 3.0; differs from key |
| `items[9].widget.answer` | key 79 | correct | concepts script: recomputed 79.0 |
| `items[9].widget.wrong[rounded-down]` | slip rounded-down = 78 | correct | concepts script: named slip gives 78.0; differs from key |
| `items[9].widget.wrong[unrounded]` | slip unrounded = 78.125 | correct | concepts script: named slip gives 78.125; differs from key |
| `items[9].widget.wrong[no-cost]` | slip no-cost = 66.67 | correct | concepts script: named slip gives 66.6667; differs from key |
| `items[2].widget.options[times]` | key: Multiply both sides by 4 | correct | (x+5)/4 = 6: multiply by 4, then subtract 5; x = 19 |
| `items[2].widget.options[minus]` | wrong option: Subtract 5 from both sides / why: The 5 is inside the fraction. It was added before dividing, so it comes off last. | correct | (x+5)/4 = 6: multiply by 4, then subtract 5; x = 19 |
| `items[2].widget.options[divide]` | wrong option: Divide both sides by 4 / why: The top was already divided by 4. Multiply to undo it. | correct | (x+5)/4 = 6: multiply by 4, then subtract 5; x = 19 |
| `items[6].widget.options[yes]` | key: Yes: both sides are 20 | correct | 4(3+2) = 20 and 7(3) - 1 = 20; 4x+8 = 7x-1 has the single root 3 |
| `items[6].widget.options[no-left]` | wrong option: No: the left side is 14 / why: You worked out $4 \times 3 + 2$. The 4 multiplies the whole bracket: $4 \times 5 = 20$. | correct | 4(3+2) = 20 and 7(3) - 1 = 20; 4x+8 = 7x-1 has the single root 3 |
| `items[6].widget.options[no-right]` | wrong option: No: the right side is 22 / why: You added the 1. The right side is $7 \times 3 - 1 = 20$. | correct | 4(3+2) = 20 and 7(3) - 1 = 20; 4x+8 = 7x-1 has the single root 3 |
| `items[9].explain.text` | net 6.40 a subscriber; 78 net 499.20; 79 needed | correct | derivation |

## review-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[3].widget.answer` | key 4 | correct | concepts script: recomputed 4.0 |
| `items[3].widget.wrong[took-three]` | slip took-three = 5 | correct | concepts script: named slip gives 5.0; differs from key |
| `items[3].widget.wrong[dropped-low]` | slip dropped-low = 3 | correct | concepts script: named slip gives 3.0; differs from key |
| `items[5].widget.answer` | key 48 | correct | concepts script: recomputed 48.0 |
| `items[5].widget.wrong[times]` | slip times = 47.88 | correct | concepts script: named slip gives 47.88; differs from key |
| `items[5].widget.wrong[off-exit]` | slip off-exit = 43.32 | correct | concepts script: named slip gives 43.32; differs from key |
| `items[6].widget.answer` | key 5 | correct | concepts script: recomputed 5.0 |
| `items[6].widget.wrong[smallest]` | slip smallest = 2 | correct | concepts script: named slip gives 2.0; differs from key |
| `items[6].widget.wrong[sign]` | slip sign = -2 | correct | concepts script: named slip gives -2.0; differs from key |
| `items[7].widget.answer` | key 251 | correct | concepts script: recomputed 251.0 |
| `items[7].widget.wrong[break-even]` | slip break-even = 250 | correct | concepts script: named slip gives 250.0; differs from key |
| `items[2].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[2].widget.options[a]` |  \dfrac{P - 2l}{2}$ equals the source expression | correct | concepts script: sympy identity test against P/2 - l |
| `items[2].widget.options[b]` |  \dfrac{P}{2} + l$ differs from the source expression | correct | concepts script: sympy identity test against P/2 - l |
| `items[2].widget.options[c]` |  P - 2l$ differs from the source expression | correct | concepts script: sympy identity test against P/2 - l |
| `items[2].widget.options[d]` |  \dfrac{P}{2} - 2l$ differs from the source expression | correct | concepts script: sympy identity test against P/2 - l |
| `items[1]` | 6 - 2x > 14 is x < -4 | correct | concepts script: sympy.solveset gives Interval.open(-oo, -4) |
| `items[3]` | -2 <= 3x + 1 < 10 is -1 <= x < 3 | correct | concepts script: sympy.solveset gives Interval.Ropen(-1, 3) |
| `items[6]` | 80 <= 100 - 4y <= 92 is 2 <= y <= 5 | correct | concepts script: sympy.solveset gives Interval(2, 5) |
| `items[7]` | 8q - 2000 > 0 is q > 250 | correct | concepts script: sympy.solveset gives Interval.open(250, oo) |
| `items[0].widget.options[a]` | key: $x \ge -3$ | correct | closed end at -3, ray right: x >= -3, the same as -3 <= x |
| `items[0].widget.options[b]` | wrong option: $x > -3$ / why: The dot at −3 is filled, so −3 is in. That needs $\ge$. | correct | closed end at -3, ray right: x >= -3, the same as -3 <= x |
| `items[0].widget.options[c]` | wrong option: $x \le -3$ / why: The bar runs right, towards bigger numbers such as 0. That is greater than. | correct | closed end at -3, ray right: x >= -3, the same as -3 <= x |
| `items[0].widget.options[d]` | wrong option: $-3 \ge x$ / why: That reads $x \le -3$, with the bar running left. Read it with $x$ first. | correct | closed end at -3, ray right: x >= -3, the same as -3 <= x |
| `items[1].widget.options[a]` | key: $x < -4$ | correct | concepts script solution set x < -4 |
| `items[1].widget.options[b]` | wrong option: $x > -4$ / why: You divided by $-2$ and kept $>$. Test $x = 0$: $6 > 14$ is false. | correct | concepts script solution set x < -4 |
| `items[1].widget.options[c]` | wrong option: $x < -10$ / why: You added 6 to 14. Subtract 6 from both sides: $-2x > 8$. | correct | concepts script solution set x < -4 |
| `items[1].widget.options[d]` | wrong option: $x > 4$ / why: Two slips: $8 \div -2 = -4$, and dividing by $-2$ reverses the sign. | correct | concepts script solution set x < -4 |
| `items[4].widget.options[a]` | key: $v > 2000$ | correct | "more than 2,000" is v > 2000, strict |
| `items[4].widget.options[b]` | wrong option: $v \ge 2000$ / why: That pays on exactly 2,000 shares too. “More than 2,000” leaves 2,000 out. | correct | "more than 2,000" is v > 2000, strict |
| `items[4].widget.options[c]` | wrong option: $v < 2000$ / why: That is the quiet days, which earn nothing. | correct | "more than 2,000" is v > 2000, strict |
| `items[4].widget.options[d]` | wrong option: $v \le 2000$ / why: That is every day without the rebate, 2,000 itself included. | correct | "more than 2,000" is v > 2000, strict |
| `items[6].explain.text` | -20 <= -4y <= -8, so 5 >= y >= 2 | correct | concepts script solution set |

## homework-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[1].widget.answer` | key 39.75 | correct | concepts script: recomputed 39.75 |
| `items[1].widget.wrong[fee-each]` | slip fee-each = 2850 | correct | concepts script: named slip gives 2850.0; differs from key |
| `items[1].widget.wrong[pence]` | slip pence = 3752.25 | correct | concepts script: named slip gives 3752.25; differs from key |
| `items[1].widget.wrong[no-fee]` | slip no-fee = 37.5 | correct | concepts script: named slip gives 37.5; differs from key |
| `items[5].widget.answer` | key 3000 | correct | concepts script: recomputed 3000.0 |
| `items[5].widget.wrong[four]` | slip four = 30 | correct | concepts script: named slip gives 30.0; differs from key |
| `items[5].widget.wrong[point-four]` | slip point-four = 300 | correct | concepts script: named slip gives 300.0; differs from key |
| `items[5].widget.wrong[times]` | slip times = 4.8 | correct | concepts script: named slip gives 4.8; differs from key |
| `items[7].widget.answer` | key 25 | correct | concepts script: recomputed 25.0 |
| `items[7].widget.wrong[no-share-cost]` | slip no-share-cost = 20.83 | correct | concepts script: named slip gives 20.8333; differs from key |
| `items[7].widget.wrong[added-cost]` | slip added-cost = 17.86 | correct | concepts script: named slip gives 17.8571; differs from key |
| `items[7].widget.wrong[fee-only]` | slip fee-only = 125 | correct | concepts script: named slip gives 125.0; differs from key |
| `items[0].widget.answer` | 3.2n+5 equals the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.accept[0]` | 3.2n+5 equals the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.accept[1]` | 5+3.2n equals the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.accept[2]` | 3.20n+5 equals the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.accept[3]` | 5+3.20n equals the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.accept[4]` | 3.2*n+5 equals the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.accept[5]` | 5+3.2*n equals the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.wrong[fee-each]` | 8.2n differs from the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[0].widget.wrong[swapped]` | 5n+3.2 differs from the source expression | correct | concepts script: sympy identity test against 16*n/5 + 5 |
| `items[2].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[2].widget.options[right]` | $4n + 5$ equals the source expression | correct | concepts script: sympy identity test against 4*n + 5 |
| `items[2].widget.options[neg-neg]` | $4n - 11$ differs from the source expression | correct | concepts script: sympy identity test against 4*n + 5 |
| `items[2].widget.options[first-only]` | $4n + 1$ differs from the source expression | correct | concepts script: sympy identity test against 4*n + 5 |
| `items[2].widget.options[added]` | $8n + 5$ differs from the source expression | correct | concepts script: sympy identity test against 4*n + 5 |
| `items[3].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[3].widget.options[right]` | $15 - 10n$ equals the source expression | correct | concepts script: sympy identity test against 15 - 10*n |
| `items[3].widget.options[first-only]` | $15 - 2n$ differs from the source expression | correct | concepts script: sympy identity test against 15 - 10*n |
| `items[3].widget.options[sign]` | $15 + 10n$ differs from the source expression | correct | concepts script: sympy identity test against 15 - 10*n |
| `items[3].widget.options[last-only]` | $3 - 10n$ differs from the source expression | correct | concepts script: sympy identity test against 15 - 10*n |
| `items[6].widget.options` | exactly one correct option | correct | concepts script: count |
| `items[6].widget.options[right]` | $3n(2n + 3)$ equals the source expression | correct | concepts script: sympy identity test against 6*n**2 + 9*n |
| `items[6].widget.options[no-n]` | $3(2n^2 + 3n)$ equals the source expression (equal in value, refused for form: not fully factorised) | correct | concepts script: sympy identity test against 6*n**2 + 9*n |
| `items[6].widget.options[no-three]` | $n(6n + 9)$ equals the source expression (equal in value, refused for form: not fully factorised) | correct | concepts script: sympy identity test against 6*n**2 + 9*n |
| `items[6].widget.options[undivided]` | $3n(2n + 9)$ differs from the source expression | correct | concepts script: sympy identity test against 6*n**2 + 9*n |
| `items[4].widget` | order: n + (n+1) + (n+2) = 3n + 3 = 3(n + 1), a multiple of 3 for every whole n | correct | Gelfand and Shen, Algebra, a standard divisibility argument |
| `items[8].model` | longform: values 12/3, 16/7, 52/43; difference 9 for every n; book understated by 9,000 | correct | derivation: 4(n+3) - (4n+3) = 9 |

## homework-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].widget.answer` | key -5 | correct | concepts script: recomputed -5.0 |
| `items[0].widget.wrong[sign]` | slip sign = 5 | correct | concepts script: named slip gives 5.0; differs from key |
| `items[0].widget.wrong[added]` | slip added = -9.6667 | correct | concepts script: named slip gives -9.6667; differs from key |
| `items[1].widget.answer` | key 9.5 | correct | concepts script: recomputed 9.5 |
| `items[1].widget.wrong[lost-bracket]` | slip lost-bracket = 2 | correct | concepts script: named slip gives 2.0; differs from key |
| `items[1].widget.wrong[swapped]` | slip swapped = 2.1667 | correct | concepts script: named slip gives 2.1667; differs from key |
| `items[3].widget.answer` | key 3.87 | correct | concepts script: recomputed 3.87 |
| `items[3].widget.wrong[short]` | slip short = 3.86 | correct | concepts script: named slip gives 3.86; differs from key |
| `items[3].widget.wrong[unrounded]` | slip unrounded = 3.864 | correct | concepts script: named slip gives 3.864; differs from key |
| `items[3].widget.wrong[no-fees]` | slip no-fees = 3.84 | correct | concepts script: named slip gives 3.84; differs from key |
| `items[4].widget.answer` | key 314 | correct | concepts script: recomputed 314.0 |
| `items[4].widget.wrong[under]` | slip under = 313 | correct | concepts script: named slip gives 313.0; differs from key |
| `items[4].widget.wrong[unrounded]` | slip unrounded = 313.78 | correct | concepts script: named slip gives 313.7813; differs from key |
| `items[4].widget.wrong[percent-as-whole]` | slip percent-as-whole = 418 | correct | concepts script: named slip gives 418.0; differs from key |
| `items[5].widget.answer` | key 12 | correct | concepts script: recomputed 12.0 |
| `items[5].widget.wrong[one-fund]` | slip one-fund = 40 | correct | concepts script: named slip gives 40.0; differs from key |
| `items[5].widget.wrong[other-fund]` | slip other-fund = 17.14 | correct | concepts script: named slip gives 17.1429; differs from key |
| `items[5].widget.wrong[kept-sign]` | slip kept-sign = 30 | correct | concepts script: named slip gives 30.0; differs from key |
| `items[7].widget.answer` | key 420 | correct | concepts script: recomputed 420.0 |
| `items[7].widget.wrong[monday]` | slip monday = 960 | correct | concepts script: named slip gives 960.0; differs from key |
| `items[7].widget.wrong[half]` | slip half = 630 | correct | concepts script: named slip gives 630.0; differs from key |
| `items[7].widget.wrong[added]` | slip added = 500 | correct | concepts script: named slip gives 500.0; differs from key |
| `items[8].widget.options[all]` | key: Kai is wrong: every $x$ works | correct | 2(x+3) and 2x+6 are the same expression: an identity |
| `items[8].widget.options[none]` | wrong option: Kai is right: no $x$ works / why: Removing $2x$ leaves $6 = 6$, which is true, so nothing is ruled out. | correct | 2(x+3) and 2x+6 are the same expression: an identity |
| `items[8].widget.options[zero]` | wrong option: Neither: only $x = 0$ works / why: 0 works, but so does every number. Try $x = 5$: both sides are 16. | correct | 2(x+3) and 2x+6 are the same expression: an identity |
| `items[8].widget.options[three]` | wrong option: Neither: only $x = 3$ works / why: 3 works, but so does every number. The two sides are the same expression. | correct | 2(x+3) and 2x+6 are the same expression: an identity |
| `items[2].widget` | order: general solution x = (d - b)/(a - c), allowed only when a != c | correct | derivation; condition stated |
| `items[6].model` | longform: 3x + 24 = 2x + 36, x = 12; x = 1 gives 2.25 against about 3.17; times 24 also works; any non-zero multiplier keeps the balance | correct | derivation |
| `items[8].explain.text` | definition: an equation true for every x is an identity | correct | standard GCSE algebra text, identities |

## homework-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[1].widget.answer` | key 48.88 | correct | concepts script: recomputed 48.88 |
| `items[1].widget.wrong[pounds]` | slip pounds = 46 | correct | concepts script: named slip gives 46.0; differs from key |
| `items[1].widget.wrong[above]` | slip above = 55.12 | correct | concepts script: named slip gives 55.12; differs from key |
| `items[1].widget.wrong[drop]` | slip drop = 3.12 | correct | concepts script: named slip gives 3.12; differs from key |
| `items[2].widget.answer` | key 8 | correct | concepts script: recomputed 8.0 |
| `items[2].widget.wrong[took-six]` | slip took-six = 9 | correct | concepts script: named slip gives 9.0; differs from key |
| `items[2].widget.wrong[dropped-low]` | slip dropped-low = 7 | correct | concepts script: named slip gives 7.0; differs from key |
| `items[3].widget.answer` | key 5 | correct | concepts script: recomputed 5.0 |
| `items[3].widget.wrong[no-buffer]` | slip no-buffer = 7 | correct | concepts script: named slip gives 7.0; differs from key |
| `items[3].widget.wrong[subtract]` | slip subtract = 4 | correct | concepts script: named slip gives 4.0; differs from key |
| `items[3].widget.wrong[from-one]` | slip from-one = 6 | correct | concepts script: named slip gives 6.0; differs from key |
| `items[5].widget.rows cell 0` | cell key 180 | correct | concepts script: recomputed 180.0 |
| `items[5].widget.rows cell 1` | cell key 400 | correct | concepts script: recomputed 400.0 |
| `items[5].widget.rows cell 2` | cell key 500 | correct | concepts script: recomputed 500.0 |
| `items[6].widget.answer` | key -2 | correct | concepts script: recomputed -2.0 |
| `items[6].widget.wrong[rounded]` | slip rounded = -1 | correct | concepts script: named slip gives -1.0; differs from key |
| `items[6].widget.wrong[dropped-minus]` | slip dropped-minus = 13 | correct | concepts script: named slip gives 13.0; differs from key |
| `items[6].widget.wrong[boundary]` | slip boundary = -1.43 | correct | concepts script: named slip gives -1.4286; differs from key |
| `items[6].widget.wrong[sign]` | slip sign = 2 | correct | concepts script: named slip gives 2.0; differs from key |
| `items[0]` | (3 - x)/4 >= -2 is x <= 11 | correct | concepts script: sympy.solveset gives Interval(-oo, 11) |
| `items[2]` | 2x - 3 < 9 and 5 - x <= 7 is -2 <= x < 6 | correct | concepts script: sympy.solveset gives Interval.Ropen(-2, 6) |
| `items[3]` | 12000 - 1500n >= 3000 is n <= 6 | correct | concepts script: sympy.solveset gives Interval(-oo, 6) |
| `items[6]` | (2x - 1)/3 < (x + 4)/(-2) is x < -10/7 | correct | concepts script: sympy.solveset gives Interval.open(-oo, -10/7) |
| `items[7]` | 40(75 - p) >= -400 is p <= 85 | correct | concepts script: sympy.solveset gives Interval(-oo, 85) |
| `items[0].widget.options[a]` | key: $x \le 11$ | correct | concepts script solution set x <= 11; x = 15 gives -3 |
| `items[0].widget.options[b]` | wrong option: $x \ge 11$ / why: You reached $-x \ge -11$ and dropped the minus signs without reversing. Test $x = 15$: $\d... | correct | concepts script solution set x <= 11; x = 15 gives -3 |
| `items[0].widget.options[c]` | wrong option: $x \le 5$ / why: You multiplied the left by 4 but not the right. Both sides: $3 - x \ge -8$. | correct | concepts script solution set x <= 11; x = 15 gives -3 |
| `items[0].widget.options[d]` | wrong option: $x \le -11$ / why: From $-x \ge -11$, multiplying by $-1$ changes both signs: $x \le 11$. | correct | concepts script solution set x <= 11; x = 15 gives -3 |
| `items[4].widget` | order: y = (x+2)/(x-1) rearranges to x = (y+2)/(y-1); check x = 4, y = 2 | correct | derivation (needs y != 1, see the l13 finding) |
| `items[7].model` | longform: 40(75 - p) >= -400 gives p <= 85; checks at 80 and 90; general p = 75 + L/40, and P0 + L/n | correct | concepts script solution set; derivation |

## problems-1

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].parts[3].widget.answer` | key 75 | correct | concepts script: recomputed 75.0 |
| `items[0].parts[3].widget.wrong[five-off]` | slip five-off = 85 | correct | concepts script: named slip gives 85.0; differs from key |
| `items[0].parts[3].widget.wrong[sign]` | slip sign = 105 | correct | concepts script: named slip gives 105.0; differs from key |
| `items[0].parts[3].widget.wrong[no-child]` | slip no-child = 90 | correct | concepts script: named slip gives 90.0; differs from key |
| `items[1].parts[3].widget.answer` | key 582 | correct | concepts script: recomputed 582.0 |
| `items[1].parts[3].widget.wrong[carried]` | slip carried = 646 | correct | concepts script: named slip gives 646.0; differs from key |
| `items[1].parts[3].widget.wrong[one-pitch]` | slip one-pitch = 627 | correct | concepts script: named slip gives 627.0; differs from key |
| `items[1].parts[3].widget.wrong[sunday]` | slip sunday = 414 | correct | concepts script: named slip gives 414.0; differs from key |
| `items[2].parts[2].widget.answer` | key 40 | correct | concepts script: recomputed 40.0 |
| `items[2].parts[2].widget.wrong[sign]` | slip sign = 28 | correct | concepts script: named slip gives 28.0; differs from key |
| `items[2].parts[2].widget.wrong[one-term]` | slip one-term = 66 | correct | concepts script: named slip gives 66.0; differs from key |
| `items[2].parts[2].widget.wrong[letter]` | slip letter = 196 | correct | concepts script: named slip gives 196.0; differs from key |
| `items[2].parts[2].widget.wrong[half]` | slip half = 27 | correct | concepts script: named slip gives 27.0; differs from key |
| `items[3].parts[3].widget.answer` | key 136 | correct | concepts script: recomputed 136.0 |
| `items[3].parts[3].widget.wrong[squared-last]` | slip squared-last = 808 | correct | concepts script: named slip gives 808.0; differs from key |
| `items[3].parts[3].widget.wrong[doubled]` | slip doubled = 80 | correct | concepts script: named slip gives 80.0; differs from key |
| `items[3].parts[3].widget.wrong[three-reach]` | slip three-reach = 120 | correct | concepts script: named slip gives 120.0; differs from key |
| `items[0].parts[0].widget.answer` | a-5 equals the source expression | correct | concepts script: sympy identity test against a - 5 |
| `items[0].parts[0].widget.accept[0]` | a-5 equals the source expression | correct | concepts script: sympy identity test against a - 5 |
| `items[0].parts[0].widget.wrong[reversed]` | 5-a differs from the source expression | correct | concepts script: sympy identity test against a - 5 |
| `items[0].parts[0].widget.wrong[times]` | 5a differs from the source expression | correct | concepts script: sympy identity test against a - 5 |
| `items[0].parts[1].widget.answer` | 5a-15 equals the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[1].widget.accept[0]` | 5a-15 equals the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[1].widget.wrong[three-reach]` | 5a-5 differs from the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[1].widget.wrong[sign]` | 5a+15 differs from the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[1].widget.wrong[carried]` | 15-a differs from the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[2].widget.answer` | 5(a-3) equals the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[2].widget.accept[0]` | 5(a-3) equals the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[2].widget.wrong[one-term]` | 5(a-15) differs from the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[0].parts[2].widget.wrong[sign]` | 5(a+3) differs from the source expression | correct | concepts script: sympy identity test against 5*a - 15 |
| `items[1].parts[0].widget.answer` | 4.2n-45 equals the source expression | correct | concepts script: sympy identity test against 21*n/5 - 45 |
| `items[1].parts[0].widget.accept[0]` | 4.2n-45 equals the source expression | correct | concepts script: sympy identity test against 21*n/5 - 45 |
| `items[1].parts[0].widget.accept[1]` | 4.20n-45 equals the source expression | correct | concepts script: sympy identity test against 21*n/5 - 45 |
| `items[1].parts[0].widget.wrong[no-cost]` | 6.5n-45 differs from the source expression | correct | concepts script: sympy identity test against 21*n/5 - 45 |
| `items[1].parts[0].widget.wrong[added-cost]` | 8.8n-45 differs from the source expression | correct | concepts script: sympy identity test against 21*n/5 - 45 |
| `items[1].parts[1].widget.answer` | 4.2n-129 equals the source expression | correct | concepts script: sympy identity test against 21*n/5 - 129 |
| `items[1].parts[1].widget.accept[0]` | 4.2n-129 equals the source expression | correct | concepts script: sympy identity test against 21*n/5 - 129 |
| `items[1].parts[1].widget.wrong[twenty-reach]` | 4.2n-65 differs from the source expression | correct | concepts script: sympy identity test against 21*n/5 - 129 |
| `items[1].parts[1].widget.wrong[sign]` | 4.2n+39 differs from the source expression | correct | concepts script: sympy identity test against 21*n/5 - 129 |
| `items[1].parts[2].widget.answer` | 8.4n-174 equals the source expression | correct | concepts script: sympy identity test against 42*n/5 - 174 |
| `items[1].parts[2].widget.accept[0]` | 8.4n-174 equals the source expression | correct | concepts script: sympy identity test against 42*n/5 - 174 |
| `items[1].parts[2].widget.wrong[carried]` | 8.4n-110 differs from the source expression | correct | concepts script: sympy identity test against 42*n/5 - 174 |
| `items[1].parts[2].widget.wrong[one-pitch]` | 8.4n-129 differs from the source expression | correct | concepts script: sympy identity test against 42*n/5 - 174 |
| `items[2].parts[0].widget.answer` | 2n+26 equals the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[2].parts[0].widget.accept[0]` | 2n+26 equals the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[2].parts[0].widget.wrong[sign]` | 2n+14 differs from the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[2].parts[0].widget.wrong[five-reach]` | 2n+10 differs from the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[2].parts[1].widget.answer` | 2(n+13) equals the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[2].parts[1].widget.accept[0]` | 2(n+13) equals the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[2].parts[1].widget.wrong[one-term]` | 2(n+26) differs from the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[2].parts[1].widget.wrong[letter]` | 2n(1+13) differs from the source expression | correct | concepts script: sympy identity test against 2*n + 26 |
| `items[3].parts[0].widget.answer` | s^2+2s equals the source expression | correct | concepts script: sympy identity test against s*(s + 2) |
| `items[3].parts[0].widget.accept[0]` | s^2+2s equals the source expression | correct | concepts script: sympy identity test against s*(s + 2) |
| `items[3].parts[0].widget.wrong[two-reach]` | s^2+2 differs from the source expression | correct | concepts script: sympy identity test against s*(s + 2) |
| `items[3].parts[0].widget.wrong[doubled]` | 4s differs from the source expression | correct | concepts script: sympy identity test against s*(s + 2) |
| `items[3].parts[1].widget.answer` | 7s^2+6s equals the source expression | correct | concepts script: sympy identity test against 4*s**2 + 3*s*(s + 2) |
| `items[3].parts[1].widget.accept[0]` | 7s^2+6s equals the source expression | correct | concepts script: sympy identity test against 4*s**2 + 3*s*(s + 2) |
| `items[3].parts[1].widget.wrong[three-reach]` | 7s^2+2s differs from the source expression | correct | concepts script: sympy identity test against 4*s**2 + 3*s*(s + 2) |
| `items[3].parts[1].widget.wrong[unlike]` | 13s^2 differs from the source expression | correct | concepts script: sympy identity test against 4*s**2 + 3*s*(s + 2) |
| `items[3].parts[1].widget.wrong[carried]` | 7s^2+6 differs from the source expression | correct | concepts script: sympy identity test against 4*s**2 + 3*s*(s + 2) |
| `items[3].parts[2].widget.answer` | s(7s+6) equals the source expression | correct | concepts script: sympy identity test against 7*s**2 + 6*s |
| `items[3].parts[2].widget.accept[0]` | s(7s+6) equals the source expression | correct | concepts script: sympy identity test against 7*s**2 + 6*s |
| `items[3].parts[2].widget.wrong[square-out]` | s^2(7+6) differs from the source expression | correct | concepts script: sympy identity test against 7*s**2 + 6*s |
| `items[3].parts[2].widget.wrong[seven-out]` | 7s(s+6) differs from the source expression | correct | concepts script: sympy identity test against 7*s**2 + 6*s |
| `items[2].parts[3].widget.options[same]` | key: They always agree: Leo's trick is $2n + 26$ too | correct | 2(n+9)+8 = 2n+26 = 5(n+4)-3(n-2) for every n |
| `items[2].parts[3].widget.options[seven]` | wrong option: They agree for 7, but other numbers will differ / why: One matching value does not prove it, nor rule it out. Expanding settles it: $2(n + 9) + 8... | correct | 2(n+9)+8 = 2n+26 = 5(n+4)-3(n-2) for every n |
| `items[2].parts[3].widget.options[smaller]` | wrong option: Leo's result is smaller, since 9 is less than 13 / why: You compared the 9 with the 13 and left out the 8 Leo adds after doubling. $2n + 18 + 8 = ... | correct | 2(n+9)+8 = 2n+26 = 5(n+4)-3(n-2) for every n |
| `items[2].parts[3].widget.options[test-all]` | wrong option: We cannot tell without testing every number / why: Expanding Leo's expression covers every number at once: it is $2n + 26$, exactly Mia's. | correct | 2(n+9)+8 = 2n+26 = 5(n+4)-3(n-2) for every n |

## problems-2

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].parts[1].widget.answer` | key 21 | correct | concepts script: recomputed 21.0 |
| `items[0].parts[1].widget.wrong[no-fee]` | slip no-fee = 26.625 | correct | concepts script: named slip gives 26.625; differs from key |
| `items[0].parts[1].widget.wrong[add-fee]` | slip add-fee = 32.25 | correct | concepts script: named slip gives 32.25; differs from key |
| `items[0].parts[2].widget.answer` | key 31 | correct | concepts script: recomputed 31.0 |
| `items[0].parts[2].widget.wrong[rounded-up]` | slip rounded-up = 32 | correct | concepts script: named slip gives 32.0; differs from key |
| `items[0].parts[2].widget.wrong[no-fee]` | slip no-fee = 37 | correct | concepts script: named slip gives 37.0; differs from key |
| `items[0].parts[3].widget.answer` | key 7.28 | correct | concepts script: recomputed 7.28 |
| `items[0].parts[3].widget.wrong[rounded-up]` | slip rounded-up = 7.29 | correct | concepts script: named slip gives 7.29; differs from key |
| `items[0].parts[3].widget.wrong[no-fee]` | slip no-fee = 8.5714 | correct | concepts script: named slip gives 8.5714; differs from key |
| `items[0].parts[3].widget.wrong[pence]` | slip pence = 728 | correct | concepts script: named slip gives 728.0; differs from key |
| `items[1].parts[1].widget.answer` | key 750 | correct | concepts script: recomputed 750.0 |
| `items[1].parts[1].widget.wrong[lone-twenty]` | slip lone-twenty = 170 | correct | concepts script: named slip gives 170.0; differs from key |
| `items[1].parts[1].widget.wrong[top]` | slip top = 630 | correct | concepts script: named slip gives 630.0; differs from key |
| `items[1].parts[1].widget.wrong[carried-plus]` | slip carried-plus = -450 | correct | concepts script: named slip gives -450.0; differs from key |
| `items[1].parts[2].widget.answer` | key 130 | correct | concepts script: recomputed 130.0 |
| `items[1].parts[2].widget.wrong[no-bed]` | slip no-bed = 125 | correct | concepts script: named slip gives 125.0; differs from key |
| `items[1].parts[2].widget.wrong[old-share]` | slip old-share = 150 | correct | concepts script: named slip gives 150.0; differs from key |
| `items[1].parts[3].widget.answer` | key 115.71 | correct | concepts script: recomputed 115.7143 |
| `items[1].parts[3].widget.wrong[no-bed]` | slip no-bed = 111.43 | correct | concepts script: named slip gives 111.4286; differs from key |
| `items[1].parts[3].widget.wrong[six]` | slip six = 135 | correct | concepts script: named slip gives 135.0; differs from key |
| `items[2].parts[0].widget.answer` | key 7.2 | correct | concepts script: recomputed 7.2 |
| `items[2].parts[0].widget.wrong[times]` | slip times = 6480 | correct | concepts script: named slip gives 6480.0; differs from key |
| `items[2].parts[0].widget.wrong[minus]` | slip minus = 186 | correct | concepts script: named slip gives 186.0; differs from key |
| `items[2].parts[1].widget.answer` | key 7.5 | correct | concepts script: recomputed 7.5 |
| `items[2].parts[1].widget.wrong[one-rate]` | slip one-rate = 1.875 | correct | concepts script: named slip gives 1.875; differs from key |
| `items[2].parts[1].widget.wrong[added]` | slip added = 0.8333 | correct | concepts script: named slip gives 0.8333; differs from key |
| `items[2].parts[1].widget.wrong[sign]` | slip sign = -7.5 | correct | concepts script: named slip gives -7.5; differs from key |
| `items[2].parts[3].widget.answer` | key 9 | correct | concepts script: recomputed 9.0 |
| `items[2].parts[3].widget.wrong[unit-gap]` | slip unit-gap = 1.5 | correct | concepts script: named slip gives 1.5; differs from key |
| `items[2].parts[3].widget.wrong[no-charge]` | slip no-charge = 54 | correct | concepts script: named slip gives 54.0; differs from key |
| `items[3].parts[2].widget.answer` | key 4800 | correct | concepts script: recomputed 4800.0 |
| `items[3].parts[2].widget.wrong[sign]` | slip sign = -4800 | correct | concepts script: named slip gives -4800.0; differs from key |
| `items[3].parts[2].widget.wrong[bracket-sign]` | slip bracket-sign = -1142.86 | correct | concepts script: named slip gives -1142.8571; differs from key |
| `items[3].parts[2].widget.wrong[rhs]` | slip rhs = 31173.6 | correct | concepts script: named slip gives 31173.6; differs from key |
| `items[3].parts[3].widget.answer` | key 2400 | correct | concepts script: recomputed 2400.0 |
| `items[3].parts[3].widget.wrong[sign]` | slip sign = -2400 | correct | concepts script: named slip gives -2400.0; differs from key |
| `items[3].parts[3].widget.wrong[added]` | slip added = 60000 | correct | concepts script: named slip gives 60000.0; differs from key |
| `items[3].parts[3].widget.wrong[old]` | slip old = 4800 | correct | concepts script: named slip gives 4800.0; differs from key |
| `items[3].parts[0].widget.answer` | 12000-s equals the source expression | correct | concepts script: sympy identity test against 12000 - s |
| `items[3].parts[0].widget.accept[0]` | 12000-s equals the source expression | correct | concepts script: sympy identity test against 12000 - s |
| `items[3].parts[0].widget.wrong[reversed]` | s-12000 differs from the source expression | correct | concepts script: sympy identity test against 12000 - s |
| `items[3].parts[0].widget.wrong[added]` | 12000+s differs from the source expression | correct | concepts script: sympy identity test against 12000 - s |
| `items[0].parts[0].widget.answer` | 45+8c=213 has the root 21 | correct | concepts script: sympy.solve |
| `items[0].parts[0].widget.accept[0]` | 8c+45=213 has the root 21 | correct | concepts script: sympy.solve |
| `items[0].parts[0].widget.wrong[added]` | 53c=213 is a different equation | correct | concepts script: sympy.solve: different root |
| `items[0].parts[0].widget.wrong[swapped]` | 8+45c=213 is a different equation | correct | concepts script: sympy.solve: different root |
| `items[0].parts[0].widget.wrong[fee-side]` | 8c=213+45 is a different equation | correct | concepts script: sympy.solve: different root |
| `items[1].parts[0].widget.answer` | \frac{x}{5}-20=\frac{x+30}{6} has the root 750 | correct | concepts script: sympy.solve |
| `items[1].parts[0].widget.accept[0]` | x/5-20=(x+30)/6 has the root 750 | correct | concepts script: sympy.solve |
| `items[1].parts[0].widget.wrong[plus]` | \frac{x}{5}+20=\frac{x+30}{6} is a different equation | correct | concepts script: sympy.solve: different root |
| `items[1].parts[0].widget.wrong[bed-each]` | \frac{x}{5}-20=\frac{x}{6}+30 is a different equation | correct | concepts script: sympy.solve: different root |
| `items[1].parts[0].widget.wrong[no-bed]` | \frac{x}{5}-20=\frac{x}{6} is a different equation | correct | concepts script: sympy.solve: different root |
| `items[3].parts[1].widget.answer` | 0.04s+0.065(12000-s)=660 has the root 4800 | correct | concepts script: sympy.solve |
| `items[3].parts[1].widget.accept[0]` | 0.04s+780-0.065s=660 has the root 4800 | correct | concepts script: sympy.solve |
| `items[3].parts[1].widget.wrong[no-minus]` | 0.04s+0.065\times12000=660 is a different equation | correct | concepts script: sympy.solve: different root |
| `items[3].parts[1].widget.wrong[per-cent]` | 4s+6.5(12000-s)=660 is a different equation | correct | concepts script: sympy.solve: different root |
| `items[2].parts[2].widget.options[b]` | key: Tariff B, since it costs less below 7.5 units a day | correct | A = 45+24u, B = 30u; B cheaper for u < 7.5; at 7.2, 217.8p against 216p |
| `items[2].parts[2].widget.options[a-rate]` | wrong option: Tariff A, since 24p a unit is the lower rate / why: The lower rate only wins once it has paid back the 45p daily charge, which takes 7.5 units... | correct | A = 45+24u, B = 30u; B cheaper for u < 7.5; at 7.2, 217.8p against 216p |
| `items[2].parts[2].widget.options[a-below]` | wrong option: Tariff A, since 7.2 units is below the 7.5 match / why: Below the match the tariff with no daily charge is cheaper. At 7.2 units A costs 217.8p an... | correct | A = 45+24u, B = 30u; B cheaper for u < 7.5; at 7.2, 217.8p against 216p |
| `items[2].parts[2].widget.options[same]` | wrong option: Neither, as the two cost the same at 7.2 units / why: They match only at 7.5 units. At 7.2 units A costs $45 + 24 \times 7.2 = 217.8$p. | correct | A = 45+24u, B = 30u; B cheaper for u < 7.5; at 7.2, 217.8p against 216p |
| `items[0].parts[3].explain.text` | 7.29 costs 300.15; 7.28 costs 299.80 | correct | derivation |

## problems-3

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `items[0].parts[3].widget.answer` | key 6 | correct | concepts script: recomputed 6.0 |
| `items[0].parts[3].widget.wrong[with-four]` | slip with-four = 7 | correct | concepts script: named slip gives 7.0; differs from key |
| `items[0].parts[3].widget.wrong[no-ten]` | slip no-ten = 5 | correct | concepts script: named slip gives 5.0; differs from key |
| `items[1].parts[1].widget.answer` | key 5 | correct | concepts script: recomputed 5.0 |
| `items[1].parts[1].widget.wrong[order]` | slip order = -9.2222 | correct | concepts script: named slip gives -9.2222; differs from key |
| `items[1].parts[1].widget.wrong[sign]` | slip sign = 40.5556 | correct | concepts script: named slip gives 40.5556; differs from key |
| `items[1].parts[1].widget.wrong[times]` | slip times = 16.2 | correct | concepts script: named slip gives 16.2; differs from key |
| `items[1].parts[3].widget.answer` | key 19 | correct | concepts script: recomputed 19.0 |
| `items[1].parts[3].widget.wrong[gap]` | slip gap = 18 | correct | concepts script: named slip gives 18.0; differs from key |
| `items[1].parts[3].widget.wrong[celsius]` | slip celsius = 11 | correct | concepts script: named slip gives 11.0; differs from key |
| `items[1].parts[3].widget.wrong[both-out]` | slip both-out = 17 | correct | concepts script: named slip gives 17.0; differs from key |
| `items[2].parts[1].widget.answer` | key 6 | correct | concepts script: recomputed 6.0 |
| `items[2].parts[1].widget.wrong[value-only]` | slip value-only = 4 | correct | concepts script: named slip gives 4.0; differs from key |
| `items[2].parts[1].widget.wrong[sign]` | slip sign = -6 | correct | concepts script: named slip gives -6.0; differs from key |
| `items[2].parts[1].widget.wrong[added]` | slip added = 14 | correct | concepts script: named slip gives 14.0; differs from key |
| `items[2].parts[4].widget.answer` | key 6 | correct | concepts script: recomputed 6.0 |
| `items[2].parts[4].widget.wrong[no-two]` | slip no-two = 5 | correct | concepts script: named slip gives 5.0; differs from key |
| `items[2].parts[4].widget.wrong[rounded-up]` | slip rounded-up = 7 | correct | concepts script: named slip gives 7.0; differs from key |
| `items[3].parts[1].widget.answer` | key 4000 | correct | concepts script: recomputed 4000.0 |
| `items[3].parts[1].widget.wrong[dropped]` | slip dropped = 2400 | correct | concepts script: named slip gives 2400.0; differs from key |
| `items[3].parts[1].widget.wrong[sign]` | slip sign = 1714.29 | correct | concepts script: named slip gives 1714.2857; differs from key |
| `items[3].parts[2].widget.answer` | key 2000 | correct | concepts script: recomputed 2000.0 |
| `items[3].parts[2].widget.wrong[dropped]` | slip dropped = 1500 | correct | concepts script: named slip gives 1500.0; differs from key |
| `items[3].parts[2].widget.wrong[sign]` | slip sign = 1200 | correct | concepts script: named slip gives 1200.0; differs from key |
| `items[3].parts[3].widget.answer` | key 9 | correct | concepts script: recomputed 9.0 |
| `items[3].parts[3].widget.wrong[gap]` | slip gap = 8 | correct | concepts script: named slip gives 8.0; differs from key |
| `items[3].parts[3].widget.wrong[both-out]` | slip both-out = 7 | correct | concepts script: named slip gives 7.0; differs from key |
| `items[1].parts[0].widget.answer` | \frac{F-32}{1.8} equals the source expression | correct | concepts script: sympy identity test against 5*F/9 - 160/9 |
| `items[1].parts[0].widget.accept[0]` | \frac{5(F-32)}{9} equals the source expression | correct | concepts script: sympy identity test against 5*F/9 - 160/9 |
| `items[1].parts[0].widget.accept[1]` | (F-32)/1.8 equals the source expression | correct | concepts script: sympy identity test against 5*F/9 - 160/9 |
| `items[1].parts[0].widget.wrong[order]` | \frac{F}{1.8}-32 differs from the source expression | correct | concepts script: sympy identity test against 5*F/9 - 160/9 |
| `items[1].parts[0].widget.wrong[sign]` | \frac{F+32}{1.8} differs from the source expression | correct | concepts script: sympy identity test against 5*F/9 - 160/9 |
| `items[1].parts[0].widget.wrong[times]` | 1.8(F-32) differs from the source expression | correct | concepts script: sympy identity test against 5*F/9 - 160/9 |
| `items[2].parts[0].widget.answer` | \frac{P-V}{k} equals the source expression | correct | concepts script: sympy identity test against (P - V)/k |
| `items[2].parts[0].widget.accept[0]` | (P-V)/k equals the source expression | correct | concepts script: sympy identity test against (P - V)/k |
| `items[2].parts[0].widget.accept[1]` | \frac{V-P}{-k} equals the source expression | correct | concepts script: sympy identity test against (P - V)/k |
| `items[2].parts[0].widget.wrong[sign]` | \frac{V-P}{k} differs from the source expression | correct | concepts script: sympy identity test against (P - V)/k |
| `items[2].parts[0].widget.wrong[top]` | \frac{P}{k}-V differs from the source expression | correct | concepts script: sympy identity test against (P - V)/k |
| `items[2].parts[0].widget.wrong[not-gathered]` | P-\frac{V}{k} differs from the source expression | correct | concepts script: sympy identity test against (P - V)/k |
| `items[3].parts[0].widget.answer` | \frac{wb}{1-w} equals the source expression | correct | concepts script: sympy identity test against -b*w/(w - 1) |
| `items[3].parts[0].widget.accept[0]` | \frac{bw}{1-w} equals the source expression | correct | concepts script: sympy identity test against -b*w/(w - 1) |
| `items[3].parts[0].widget.accept[1]` | wb/(1-w) equals the source expression | correct | concepts script: sympy identity test against -b*w/(w - 1) |
| `items[3].parts[0].widget.accept[2]` | \frac{-wb}{w-1} equals the source expression | correct | concepts script: sympy identity test against -b*w/(w - 1) |
| `items[3].parts[0].widget.wrong[sign]` | \frac{wb}{1+w} differs from the source expression | correct | concepts script: sympy identity test against -b*w/(w - 1) |
| `items[3].parts[0].widget.wrong[dropped]` | wb differs from the source expression | correct | concepts script: sympy identity test against -b*w/(w - 1) |
| `items[3].parts[0].widget.wrong[not-alone]` | w(a+b) differs from the source expression | correct | concepts script: sympy identity test against -b*w/(w - 1) |
| `items[0].parts[1]` | 240 - 18h >= 60 is h <= 10 | correct | concepts script: sympy.solveset gives Interval(-oo, 10) |
| `items[1].parts[2]` | (F - 32)/1.8 <= 5 is F <= 41 | correct | concepts script: sympy.solveset gives Interval(-oo, 41) |
| `items[1].parts[3]` | -25 <= (F - 32)/1.8 <= -15 is -13 <= F <= 5 | correct | concepts script: sympy.solveset gives Interval(-13, 5) |
| `items[2].parts[2]` | 24000 - 2400t > 6000 is t < 7.5 | correct | concepts script: sympy.solveset gives Interval.open(-oo, 15/2) |
| `items[2].parts[3]` | 6000 < 24000 - 2400t <= 19200 is 2 <= t < 7.5 | correct | concepts script: sympy.solveset gives Interval.Ropen(2, 15/2) |
| `items[0].parts[2].widget.options[filled-left]` | key: A filled dot at 10, with the bar running left | correct | h <= 10: closed end at 10, ray left |
| `items[0].parts[2].widget.options[hollow-left]` | wrong option: A hollow dot at 10, with the bar running left / why: A hollow dot leaves 10 out, but 10 hours leaves exactly 60 loaves, which is allowed. | correct | h <= 10: closed end at 10, ray left |
| `items[0].parts[2].widget.options[filled-right]` | wrong option: A filled dot at 10, with the bar running right / why: Running right shows $h \ge 10$, the answer with the sign not reversed. | correct | h <= 10: closed end at 10, ray left |
| `items[0].parts[2].widget.options[hollow-right]` | wrong option: A hollow dot at 10, with the bar running right / why: That shows $h > 10$: 10 is left out and the bar points the wrong way. | correct | h <= 10: closed end at 10, ray left |
| `items[2].parts[3].widget.options[right]` | key: $2 \le t < 7.5$ | correct | concepts script solution set [2, 7.5) |
| `items[2].parts[3].widget.options[ends-kept]` | wrong option: $2 < t \le 7.5$ / why: Reversing the signs also moves which end is included: the $\le$ beside 19,200 becomes $\ge... | correct | concepts script solution set [2, 7.5) |
| `items[2].parts[3].widget.options[no-flip]` | wrong option: $7.5 < t \le 2$ / why: You divided by $-2{,}400$ without reversing the signs. No number is above 7.5 and at most ... | correct | concepts script solution set [2, 7.5) |
| `items[2].parts[3].widget.options[negative]` | wrong option: $-7.5 < t \le -2$ / why: $-18{,}000 \div (-2{,}400)$ is $+7.5$: a negative divided by a negative is positive. | correct | concepts script solution set [2, 7.5) |
| `items[3].parts[2].explain.text` | with bonds fixed, a smaller w needs less in shares | correct | derivation: wb/(1-w) increases with w on 0 < w < 1 |

## fluency-l2-like-terms

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0]` | key solves the item and both slips differ from the key, all 45177 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[0].vars` | ranges in the file match the ranges enumerated | correct | concepts script: read from the file |

## fluency-l3-opening-brackets

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0]` | key solves the item and both slips differ from the key, all 1440 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1]` | key solves the item and both slips differ from the key, all 6284 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1].vars` | ranges in the file match the ranges enumerated | correct | concepts script: read from the file |

## fluency-l4-putting-brackets-back

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0]` | key solves the item and both slips differ from the key, all 284 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1]` | key solves the item and both slips differ from the key, all 306 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1].vars` | ranges in the file match the ranges enumerated | correct | concepts script: read from the file |

## fluency-l6-undoing-in-reverse

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0]` | key solves the item and both slips differ from the key, all 4320 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1]` | key solves the item and both slips differ from the key, all 1620 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[0].vars` | ranges in the file match the ranges enumerated | correct | concepts script: read from the file |

## fluency-l7-unknowns-both-sides

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0]` | key solves the item and both slips differ from the key, all 1514 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1]` | key solves the item and both slips differ from the key, all 132 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1].vars` | ranges in the file match the ranges enumerated | correct | concepts script: read from the file |

## fluency-l8-clearing-fractions

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0]` | key solves the item and both slips differ from the key, all 90 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[1]` | key solves the item and both slips differ from the key, all 177 draws | correct | concepts script: own enumeration of the whole variable range (not the engine templates) |
| `families[0].vars` | ranges in the file match the ranges enumerated | correct | concepts script: read from the file |

## fluency-l13-changing-the-subject

| JSON path | claim | verdict | basis |
|---|---|---|---|
| `families[0]` | key is the rearrangement; slips are different expressions for a >= 2, b != 0 | correct | concepts script: sympy.solve with symbols; u/a - b = (u - b)/a only if a = 1 or b = 0 |
| `families[1]` | key is the rearrangement; slips are different expressions for a >= 2, b != 0 | correct | concepts script: sympy.solve with symbols; u/a - b = (u - b)/a only if a = 1 or b = 0 |
| `families[2]` | key is the rearrangement; slips are different expressions for a >= 2, b != 0 | correct | concepts script: sympy.solve with symbols; u/a - b = (u - b)/a only if a = 1 or b = 0 |


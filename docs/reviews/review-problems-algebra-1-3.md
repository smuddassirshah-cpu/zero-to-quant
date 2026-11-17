# Problem sets 3.4, algebra levels 1 to 3: second-reader findings

Scope: `app/content/courses/algebra/problems-1.json`, `-2`, `-3`: 9 problems, 38 parts (35 numeric, 3 choice), 78 `wrong` entries. Rules: `docs/briefs/wave-c-reader-ag.md`, `chained-prompts.md`, `chained.md`, `wave-c-author-ag.md`. Pattern: `review-problems-analysis-1-3.md`.

## Verdict per problem

`re-author` = the problem walks course items in a row or retells lesson screens; the items not to walk are in the numbered finding, with no replacement text. `reuse` = one part or one number set is the course's; exact fix given. `clean` = its own chain.

| set | problem | verdict | closest lesson screen | closest quiz, review, homework, set | closest exam item | finding |
|---|---|---|---|---|---|---|
| 1 | `p-probe-stride` | reuse (part 1) | l4 s0 "how many seats does a walk from 0 visit, counting 0"; l4 s4 generators of $\mathbb{Z}_{12}$; l3 s7 Euclid on 26 and 7 | review-1 i4 ($7^{-1} \bmod 40$), i5 (order of 18 in $\mathbb{Z}_{30}$); homework-1 i7 ($6x \equiv 9$) | "An inverse modulo 60" | 3, 4 |
| 1 | `p-octagon-orders` | clean | l2 s7 ($(rs)^{-1}$ in $D_4$); l4 s7 (order of a power) | l1 quiz 0; review-1 i2 ($(r \cdot r^2s)^{-1}$), i7 (hexagon count); homework-1 i3 | "Elements of order 3 in S_6" (a count by order, other group) | none |
| 1 | `p-shifted-product` | re-author | l2 s9 and s10 (returns under $\oplus$, identity 0, inverse, nothing at $-100\%$) | l2 quiz 2; homework-1 i5 (order of 2 in $\mathbb{Z}_{11}^{\times}$), i6 ($a + b + 1$) | "Orders modulo 17", both parts | 1, 2 |
| 2 | `p-desk-rota` | re-author | l8 s0, s1, s5, s8; l9 s9 | review-2 i4, i5, i6 in a row; homework-2 i7; l9 quiz 2 | "A permutation from its bottom row"; "Even or odd" | 5 |
| 2 | `p-units-21-cosets` | clean | l6 s1 (cosets of $\langle 4 \rangle$, additive), s6 (a coset is not a subgroup); l5 s2 | l5 quiz 2; review-2 i1, i7; homework-2 i1 | "The order of 15 modulo 36" (additive cosets) | none |
| 2 | `p-fixing-five` | reuse ($\sigma$) | l5 s4 ("Which step proves $\det(\mathbf{AB}^{-1}) = 1$"); l6 s7 (left and right cosets of $\{e, s\}$) | l6 quiz 2; review-2 i7; homework-2 i7 | "A product of two permutations" ($\sigma = (1\,3\,5)(2\,4)$) | 6, 7 |
| 3 | `p-fifteen-times` | re-author | l12 s0 to s2 ($3x$ on $\mathbb{Z}_{12}$, a coset per value); l11 s4 | l10 quiz 3; review-3 i4, i5; homework-3 i1 | "Doubling from 18 to 12", both parts; "The order of 15 modulo 36" (same 15 and 36) | 8 |
| 3 | `p-powers-of-seven` | clean | l13 s0, s1 (period, then the exponent modulo the period); l13 s7 ($7^{222} \bmod 10$) | l13 quiz 0; review-3 i7; homework-3 i5 ($3^{2026} \bmod 100$) | "A large power modulo 14" | none |
| 3 | `p-hexagon-quotient` | re-author | l11 s3, s4, s5, s6 in a row | review-3 i3, i4; l11 quiz 3; homework-3 i2 | "A normal subgroup of S_4" | 9 |

Four of nine are ruled re-author, above the quarter expected. Findings 5 and 8 rest on texts that match item for item. Finding 1 rests on the taught operation. Finding 9 is the least clear of the four: the result ($S_3$, not abelian) is new, the three steps to it are not.

Method. The author's script was run first. Every lesson of levels 1 to 3 (l1 to l13), `review-1` to `-3`, `homework-1` to `-3` and the 13 items of `exams/topic-3.4.json` that carry `ag-groups`, `ag-cosets`, `ag-perm` or `ag-hom` were read (prose, question, explanation of every screen and item; `read-algebra/taught.py` in the scratch folder prints them). No other exam file or bank file carries an `ag-` skill. Every part was solved by hand from its text and again in `docs/reports/problems-algebra-numbers-read.py`, which imports nothing from the author's script and uses no quoted rule: the probe is walked slot by slot, $D_8$ and $D_6$ are built as permutations of the corners, $S_5$ is listed in full (120 elements, cosets as sets), the sign is an inversion count, powers are iterated, and each quotient is built from its cosets. Every `wrong` value was rebuilt from the slip its line names, and each figure printed in a feedback or explanation line was recomputed. Each claim was read for its hypotheses and each definition against the lesson that states it: order (l4 s2), unit (l3 s2), one-step test (l5 s2), left and right coset (l6 s1, s7), $k$-cycle as $k - 1$ transpositions (l9 s2), right-to-left products (l8 s2), normal subgroup (l11 s2), kernel and image (l10 s2), first isomorphism theorem (l12 s2), Euler (l13 s5). Stories and moduli were grepped across `app/content`.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-algebra-numbers.py` 529 of 529, exit 0 |
| reader's script | `problems-algebra-numbers-read.py` 423 checks passed, 5 FINDING lines (findings 2, 3, 6, 7, 8), exit 0 |
| validator | 0 errors, 4561 warnings, none on the three files; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --files <three sets> --pairs` | 0 hits (see Engine: it misses findings 5, 6 and 8) |
| `grade-all.mjs --file`, three sets | 12, 14 and 12 widgets, 0 failures each |
| browser, `playthrough.mjs` | not run (reader rule) |

Result. All 35 numeric keys and the 3 choice keys agree with mine, and so does each of the 78 `wrong` values and every printed figure. No learner is marked wrongly: no `wrong` finding. Bands: every numeric part is a whole number or a set of residues with `abs` 0, states its form, and no `wrong` value meets a key; no percentage, table value or rounding occurs. Rule 3: no part can be passed by working back from a printed target; one definition drops a condition (finding 7) and one step leans on a theorem taught later (finding 2).

## A. `problems-1`

1. `algebra/problems-1.json` | `items[2]` (`p-shifted-product`), whole item | reuse | re-author: the operation is l2's, and parts 3 and 4 walk an exam item.
   Evidence, operation. l2 s9: "Returns combine by $r_1 \oplus r_2 = (1 + r_1)(1 + r_2) - 1$", explain "The identity of $\oplus$ is $0\%$". l2 s10: "The inverse of a return $r$ is the return that brings the factor back to 1 ... Inverses exist only for $r > -100\%$, so the group is returns above $-100\%$ under $\oplus$." The problem: "$a \ast b = (a + b + ab) \bmod 19$ ... 0 is an identity", part 1 finds that $18 \equiv -1$ has no inverse and is left out, part 2 finds an inverse that "must give the identity 0", part 3 says "$1 + (a \ast b) \equiv (1 + a)(1 + b)$". $a + b + ab$ is $(1 + a)(1 + b) - 1$ expanded: the taught formula in an equivalent form (session AE addition), with the same three steps in the same order. homework-1 i6 has the same frame ("On $\mathbb{Z}$ define $a \ast b = a + b + 1$. It is closed and associative. What is its identity element?").
   Evidence, parts 3 and 4. Exam "Orders modulo 17": "What is $\operatorname{ord}(2)$ in $\mathbb{Z}_{17}^{\times}$?" then "How many elements of $\mathbb{Z}_{17}^{\times}$ generate it?", feedback "A cyclic group of order 16 has Euler's $\varphi(16) = 8$ generators", explain "$\operatorname{ord}(g^k) = \tfrac{16}{\gcd(k, 16)}$". The problem: the order of 1 "is $\operatorname{ord}(2)$ in $\mathbb{Z}_{19}^{\times}$", then "How many elements of $G$ generate it?", feedback "In a cyclic group of order 18 ... $\varphi(18) = 6$", explain "order $18/\gcd(k, 18)$". homework-1 i5 asks the order of 2 in $\mathbb{Z}_{11}^{\times}$, also a generator.
   Not to walk: l2 s9, s10, l2 quiz 2; homework-1 i5, i6; review-1 i6; exam "Orders modulo 17" parts 1 and 2. Level 1 still needs a difficulty 5 problem that draws on l2, l3 and l4.

2. `algebra/problems-1.json` | `items[2].parts[2].feedback.correct`, `.explain.text` | continuity | a step needs a theorem from a later level.
   "The order of 1 is $\operatorname{ord}(2)$ in $\mathbb{Z}_{19}^{\times}$. It divides 18" and "The order of 2 divides 18". That is Lagrange (l7, level 2) or Fermat (l13, level 3). Level 1 has only l4 s2: $g^k = e$ exactly when $\operatorname{ord}(g) \mid k$, which needs $2^{18} \equiv 1$ first. The part's own numbers give it. Applies only if finding 1 is waived and the item kept.
   Fix, `feedback.correct`: "The order of 1 is $\operatorname{ord}(2)$ in $\mathbb{Z}_{19}^{\times}$. Since $2^9 \equiv 18 \equiv -1$, $2^{18} \equiv 1$, so the order divides 18. As $2^6 \equiv 7$ and $2^9 \equiv 18$ are not 1, it is 18."
   Fix, `explain.text`: "The $k$-fold product of 1 is the identity 0 exactly when $2^k \equiv 1 \pmod{19}$. Now $2^9 \equiv -1$ gives $2^{18} \equiv 1$, so the order divides 18 (l4). Since $2^6 \equiv 7$ and $2^9 \equiv 18$ are not 1, no proper divisor works, and the order is 18."
   (Every proper divisor of 18 divides 6 or 9; $2^9 = 512 = 26 \cdot 19 + 18$.)

3. `algebra/problems-1.json` | `items[0].parts[0]` (`p-probe-stride`) | reuse | part 1 is l4 screen 0 with slots for seats.
   l4 s0: "Six seats ... Each arrow adds the step modulo 6 ... With steps of 2, how many seats does a walk from 0 visit, counting 0?" Part 1: "A probe starts at slot 0 and jumps by a fixed stride ... With stride $s = 21$, how many different slots does the probe visit, counting slot 0?" Same picture, same question, other nouns and numbers. The part's own explanation already answers a different question ("The probe returns to 0 at the least $k$ with $56 \mid 21k$"), which is the standard order task and matches parts 3 and 4 ("after how many jumps"). Ask that. Key 8 and both `wrong` values (7, 56) stay.
   Fix, `question`: "With stride $s = 21$, after how many jumps is the probe first back at slot 0? Give a whole number."
   Fix, `feedback.correct`: "The probe is back when $56 \mid 21k$. Since $\gcd(21, 56) = 7$, that first happens at $k = 56/7 = 8$."
   Fix, `byKey.gcd`: "7 is $\gcd(21, 56)$, the gap between the slots visited. The number of jumps is 56 divided by that gap."
   Fix, `byKey.full`: "A probe needs all 56 jumps only when its stride is coprime to 56. Here 21 and 56 share the factor 7."
   Fix, `items[0].parts[1].feedback.byKey.all`: "Not every stride works: by part 1, stride 21 is back at slot 0 after 8 jumps, so it visits only 8 slots."
   `generic` and `explain` stay. The rest of the problem is its own: the hash table and the probing stride occur nowhere else in `app/content`, and parts 3 and 4 (which jump lands on slot 1, then slot 13) have no course counterpart.

4. `algebra/problems-1.json` | `items[0].parts[1].question`, `.parts[2].question` | continuity | parts 2 and 3 use no earlier result.
   Part 2 counts generators without part 1; part 3 inverts 9 without part 2. Only part 4 restates a value. `chained.md`: "part k + 1 uses the result of part k ... each later part restates the value it needs".
   Fix, part 2 `question`: "By part 1, stride 21 is back at slot 0 after only 8 jumps, so it misses slots. A stride reaches all 56 slots exactly when it generates $\mathbb{Z}_{56}$. How many strides $s$ from 1 to 55 do that? Give a whole number."
   Fix, part 3 `question`: "Double hashing gives one key the stride $s = 9$, one of the 24 generators from part 2. After how many jumps does its probe first land on slot 1? Give a whole number from 1 to 55."

## B. `problems-2`

5. `algebra/problems-2.json` | `items[0]` (`p-desk-rota`), whole item | reuse | re-author: the four parts are review-2 items 4, 5, 6 and homework-2 item 7 in a row, opened by the exam's sentence.
   Prose. Exam "A permutation from its bottom row": "A permutation $\sigma$ of $\{1, \dots, 6\}$ has bottom row $3, 5, 1, 2, 6, 4$. So $\sigma(1) = 3$, $\sigma(2) = 5$, and so on." The problem: "$\sigma$ has bottom row $7, 9, 10, 6, 8, 2, 3, 1, 4, 5$. So $\sigma(1) = 7$, $\sigma(2) = 9$, and so on."
   Part 1 (cycle through 1). l8 s0 "Tap the nodes of the loop through 1"; review-2 i4 "has bottom row $3, 6, 1, 5, 4, 2$. Which is its cycle form?"
   Part 2 (order). Exam explain: "Disjoint cycles commute, so $\sigma^k = e$ exactly when both lengths divide $k$. The least such $k$ is $\operatorname{lcm}(2, 4) = 4$." The problem: "disjoint cycles commute, so the order is $\operatorname{lcm}(6, 4) = 12$" and "$\sigma^k = e$ exactly when both cycles are home, so 6 and 4 must divide $k$. The least such $k$ is $\operatorname{lcm}(6, 4) = 12$." review-2 i5 has the same answer by the same rule ("$\operatorname{lcm}(3, 2, 4) = 12$"). The `product` slip is l8 s8 ("the product of the lengths, 6, was the order. Now take $\tau = (1\,2\,3\,4)(5\,6)$").
   Part 3 (sign). review-2 i6: "The 5-cycle is 4 transpositions and the swap is 1, so 5 in all: odd. Equally, $n - c = 7 - 2 = 5$." The problem: "$\sigma$ is $5 + 3 = 8$ transpositions, an even number. The cycle count agrees: $n - c = 10 - 2 = 8$." Exam "Even or odd" has the same case ("$(1\,2)(3\,4\,5\,6)$ uses $1 + 3 = 4$").
   Part 4 (index). homework-2 i7: "A 5-cycle has order 5 ... By Lagrange the index is $5!/5 = 24$." The problem: "by Lagrange the index is $1{,}814{,}400/12 = 151{,}200$", with $|A_n| = n!/2$ from l9 s9 and l9 quiz 2.
   Not to walk: l8 s0, s1, s5, s8; l9 s9, quiz 2; review-2 i4, i5, i6; homework-2 i7; exam "A permutation from its bottom row" and "Even or odd". The rota story itself is free (no permutation use in `app/content`). Level 2 still needs l8 and l9 drawn on by a problem; `p-fixing-five` touches l8 only through notation.

6. `algebra/problems-2.json` | `items[2].parts[2].question`, `.parts[3].question` (`p-fixing-five`) | reuse | $\sigma$ is the exam's permutation inverted.
   Exam "A product of two permutations": "In $S_5$ take $\sigma = (1\,3\,5)(2\,4)$ ... Products read right to left". The problem: "In $S_5$ ... Products read right to left ... Take $\sigma = (1\,5\,3)(2\,4)$". $(1\,5\,3)(2\,4)$ is $((1\,3\,5)(2\,4))^{-1}$: same letter, same group, same cycle type, same points.
   Fix: write $\sigma = (1\,5\,3\,2)$ in both questions ("Take $\sigma = (1\,5\,3\,2)$." and "Now the right coset $H\sigma$, with $\sigma = (1\,5\,3\,2)$."). It still has $\sigma(5) = 3$ and $\sigma(1) = 5$, so $\sigma^{-1}(5) = 1$: keys 3, 1 and 6, every `wrong` value and every feedback line stand unchanged (reader's script, `fix 6`, lists both cosets in full). $(1\,5\,3\,2)$ occurs nowhere in `app/content`. The author's script takes the new $\sigma$.

7. `algebra/problems-2.json` | `items[2].parts[0].explain.text`, `.widget.options[3].why` | misleading | the one-step test is stated without its first condition.
   l5 s2: "a non-empty $H \subseteq G$ is a subgroup when $a, b \in H$ implies $ab^{-1} \in H$"; l5 s4 closes with "With $\mathbf{I} \in H$, the test makes $H$ a subgroup." The problem: "The one-step test asks that $ab^{-1} \in H$ for $a, b \in H$", and part 2 goes on "Using that $H$ is a subgroup". The empty set passes the stated condition. Option d's `why` also leaves the learner thinking that holding $e$ plays no part.
   Fix, `explain.text`: "The one-step test needs $H$ non-empty, and $e \in H$ since $e(5) = 5$. For $a, b \in H$, $b(5) = 5$ gives $b^{-1}(5) = 5$. Then $ab^{-1}(5) = a(5) = 5$, so $ab^{-1} \in H$."
   Fix, `options[3].why`: "Holding $e$ shows only that $H$ is non-empty: $\{e, (1\,2), (2\,3)\}$ holds $e$ and is not a subgroup."

## C. `problems-3`

8. `algebra/problems-3.json` | `items[0]` (`p-fifteen-times`), whole item | reuse | re-author: the exam's two-part item with the numbers of another exam item.
   Chain. Exam "Doubling from 18 to 12": "Define $\varphi : \mathbb{Z}_{18} \to \mathbb{Z}_{12}$ by $\varphi(x) = 2x \bmod 12$. It is well defined, since $2 \times 18 = 36 \equiv 0 \pmod{12}$, and it is a homomorphism." Part 1 "How many elements does $\ker\varphi$ have?", part 2 "How many elements does $\operatorname{im}\varphi$ have?" The problem: "$\varphi(x) = 15x \bmod 36$. Because $15 \cdot 24 = 360 = 10 \cdot 36$, the rule gives one value per residue", part 1 "How many elements does $\ker\varphi$ have?", part 2 "how many elements does $\operatorname{im}\varphi$ have?" The questions are word for word. l10 quiz 3, homework-3 i1 and review-3 i5 ask the same two counts.
   Numbers. Exam "The order of 15 modulo 36": "$36 \mid 15k$ means $12 \mid 5k$, so $12 \mid k$, since $\gcd(5, 12) = 1$. So $H = \langle 15 \rangle$ has 12 elements, the multiples of 3." The problem, part 1: "$15x \equiv 0 \pmod{36}$ means $12 \mid 5x$, so $12 \mid x$"; part 2: "The image is the multiples of 3 in $\mathbb{Z}_{36}$", 12 of them. The image is the exam's $H = \langle 15 \rangle$ and part 2's key is the exam's answer. The author's report says the pair appears nowhere; it does (reader's script, FINDING 8).
   Parts 3 and 4. l12 s2: "Each row is a coset $x + K$ ... and it goes to one value" is part 3's "The solutions are the coset $11 + \ker\varphi$". l11 s4 and review-3 i4 ("What is the order of $1 + \langle 4 \rangle$ in the quotient?") are part 4, which `p-hexagon-quotient` part 3 asks again in the same set.
   Not to walk: exam "Doubling from 18 to 12" parts 1 and 2 and "The order of 15 modulo 36"; l10 quiz 3; l12 s0 to s2; l11 s4; review-3 i4, i5; homework-3 i1. No multiplier and modulus pair from those items.

9. `algebra/problems-3.json` | `items[2]` (`p-hexagon-quotient`), whole item | reuse | re-author: l11 screens 3 to 6 with the hexagon for the square.
   Part 2. review-3 i3: "$r(rs)r^{-1} = r^3s$, which is not in $\{e, rs\}$. So the subgroup is not normal. Only $\{e, r^2\}$ among the order 2 subgroups is normal." l11 s3: "a two-element flip subgroup is never kept". The problem: "A flip moves, since $r(r^js)r^{-1} = r^{j+2}s$ ... Of the 7 elements of order 2, only $r^3$ stays".
   Part 3. l11 s4: "What is the order of $1 + \langle 4 \rangle$ in the quotient? ... the identity coset. So it has order 4". The problem: "What is the order of the coset $rN$ in $G/N$? ... A power of $rN$ is the identity coset when $r^k \in N$".
   Part 4. l11 s5 and s6: "every coset squares to the identity coset. So the quotient has no element of order 4 and is not $\mathbb{Z}_4$. It is the Klein four-group." l12 s4: "An isomorphism keeps the order of every element." The problem: "each flip coset has order 2. That makes 3 elements of order 2, and $Q \cong S_3$, not $\mathbb{Z}_6$."
   Part 1 (kernel size from $|G|/|Q|$) is review-3 i5 run the other way. The quotient $D_n/\{e, r^{n/2}\}$, named by the orders of its cosets, is the lesson's worked example with 6 for 4.
   Not to walk: l11 s3, s4, s5, s6; l12 s4; l11 quiz 3; review-3 i3, i4, i5. A dihedral group over its half turn is the lesson's case whatever the polygon.

## Same-course reuse, read by eye

- `p-octagon-orders`: clean. review-1 i2 inverts a product in $D_4$ that is a flip; here the product of two flips is a turn, so "a flip undoes itself" is the `self-inverse` slip. The count of $x^4 = e$ has no level 1 counterpart (l5 s7 and homework-2 i6 count $x^2 = e$ at level 2, in $D_4$ and $S_4$). No octagon in `app/content`.
- `p-units-21-cosets`: clean. Cosets in the course are additive ($\mathbb{Z}_{12}$, $\mathbb{Z}_9$) or in $D_4$; here they are multiplicative, with the additive coset as the `added` slip. Part 5 (which union of cosets is a subgroup) has no counterpart; l6 s6 only says one coset is not a subgroup. $\mathbb{Z}_{21}^{\times}$ occurs nowhere else.
- `p-powers-of-seven`: clean. The large power is one part of four, and the course has four such items (l13 s7, review-3 i7, homework-3 i5, exam). The base 7 is l13 s7's and the exponent 2027 sits next to homework-3's 2026; neither changes a step. The chain is its own: the kernel $12\mathbb{Z}$ of $k \mapsto 7^k$ below $\varphi(45) = 24$, the `used-44` slip, and $7^{-1} = 7^{11}$ fed to a congruence.
- `p-fixing-five`: clean apart from finding 6. No stabiliser and no overlap of a left with a right coset in the course.
- `p-probe-stride`: clean apart from finding 3.

## Verified

- Chain and coverage. Every lesson of each level is drawn on (l1 to l4; l5 to l9; l10 to l13) and each problem draws on two or more. Nothing beyond the level is needed, apart from finding 2. Each last part is the result. Loose links only in `p-probe-stride` (finding 4); `p-fifteen-times` part 3 restates nothing but falls under finding 8.
- Claims checked true: a stride reaches every slot exactly when coprime to 56; $sr^j = r^{-j}s$ in $D_8$ and $D_6$ (all $j$, by enumeration); $\ast$ is associative with two-sided identity 0, 18 absorbs, and $\{0, \dots, 17\}$ is closed with inverses; 2 is a primitive root modulo 19; every power of an even permutation is even; a subgroup holding $H$ is a union of cosets of $H$; $H \cup 2H = \langle 2 \rangle$ in $\mathbb{Z}_{21}^{\times}$; $\sigma H = \{\tau : \tau(5) = 3\}$ and $H\sigma = \{\tau : \tau(1) = 5\}$ (all 24 each), overlap 6, and $(3\,5)$ lies in the first only; $15x$ is well defined and additive from $\mathbb{Z}_{24}$; $7^k \not\equiv 1 \pmod{45}$ for $k = 1, 2, 3, 4, 6, 8$ and $7^{44} \not\equiv 1$; $\{e, z\}$ is normal exactly when $z$ is central, and in $D_6$ only $r^3$ is; $D_6/\{e, r^3\}$ has 3 elements of order 2 and is not abelian.
- Skills: every `skills` id is carried by a lesson of its level. Typed parts 12 of 12, 11 of 14, 12 of 12. One difficulty 5 per set.
- Stories: hash table with a probing stride, octagon, desk rota as a permutation, and the moduli 56, 21, 45 and 19 occur in no other file of `app/content`. `a + b + ab` occurs in `brainteasers` l1 and `bank/brainteasers-4` as an invariant puzzle (other course; moot under finding 1).

## Counts

| severity | count | findings |
|---|---|---|
| wrong | 0 | |
| misleading | 1 | 7 |
| reuse | 6 | 1, 5, 8, 9 (re-author); 3, 6 (exact fix) |
| continuity | 2 | 2, 4 |
| voice | 0 | |

Keys changed by the exact fixes: none. Re-author: `p-shifted-product`, `p-desk-rota`, `p-fifteen-times`, `p-hexagon-quotient`.

## Engine

1. `fresh-check --files` reported 0 hits on sets that carry findings 5, 6 and 8. Three gaps, raised in `docs/BACKLOG-INBOX.md` under `Raised later (review problems algebra):`: a key pair inside one formula (`15x \bmod 36` against "order of 15 modulo 36") with a shared derivation line ("$12 \mid 5x$, so $12 \mid x$"); a sentence skeleton whose masked part is a comma list ("has bottom row ... So $\sigma(1) = 7$, $\sigma(2) = 9$, and so on."); a permutation in cycle form against its inverse or a relabelled start.
2. Findings 5, 8 and 9 are one class, a problem whose parts each match a different item of one review, lesson or exam file. If other reviews of this wave show it too, protocol 6 applies: a checker could flag a set problem whose parts each match a different item of one review or exam file by task shape (same question skeleton after masking numbers).

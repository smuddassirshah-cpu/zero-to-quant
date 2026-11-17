# Problem sets: algebra levels 1 to 3 (brief `docs/briefs/wave-c-author-ag.md`, `chained-prompts.md`, `chained.md`)

Files: `app/content/courses/algebra/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-algebra-numbers.py` (529 of 529 checks, exit 0). Level 4 is left to another author.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-probe-stride | 4 (4 / 0) | l3, l4 | 4 |
| problems-1 | p-octagon-orders | 4 (4 / 0) | l1, l2, l4 | 4 |
| problems-1 | p-shifted-product | 4 (4 / 0) | l2, l3, l4 | 5 |
| problems-2 | p-desk-rota | 4 (3 / 1) | l8, l9, l7 | 4 |
| problems-2 | p-units-21-cosets | 5 (4 / 1) | l5, l6, l7 | 4 |
| problems-2 | p-fixing-five | 5 (4 / 1) | l5, l6, l7, l8 | 5 |
| problems-3 | p-fifteen-times | 4 (4 / 0) | l10, l11, l12 | 4 |
| problems-3 | p-powers-of-seven | 4 (4 / 0) | l10, l12, l13 | 4 |
| problems-3 | p-hexagon-quotient | 4 (4 / 0) | l10, l11, l12 | 5 |

Typed parts: 12 of 12, 11 of 14, 12 of 12. Every lesson of each level appears; every problem draws on two or more. The three choice parts are judgements: which reason makes a permutation even, which set is a subgroup, which step passes the one-step test. Skills: level 1 `ag-groups`; level 2 `ag-perm`, `ag-cosets`; level 3 `ag-hom`, `ag-cosets`, `ag-groups`.

Proof-heavy rule (brief rule 6): no part grades a typed formula. Each idea is tested through a number (an absorbing element, a one-step test product, a conjugate, a count of normal subgroups of order 2, an overlap of a left and a right coset) or a choice of the valid step. No part prints its own target: later parts restate earlier results only after those parts are checked.

## Gates (in the brief's order)

1. Validator: 0 errors; no warning on these files (4580 in all, three long-sentence warnings met while drafting were fixed).
2. Voice scan 35 on the course folder: 0 and 0.
3. `fresh-check --file` each set: 0 hits after one rewrite (below).
4. Number script: 529 of 529, exit 0. Each key twice: by rule (phi, gcd, lcm, n/gcd(k, n), Lagrange, first isomorphism theorem, Euclid) and by brute enumeration of the group (Z_n, D_8, D_6, S_5, S_10 composed right to left). Every `wrong` value recomputed from its named slip, has a byKey line and differs from the key; set slips keep the right count; choice keys and the facts their options claim are checked; `numbers_lib` expects each key in its feedback and runs `check_wrongs` (the 27 "check by hand" byKey lines were read: each states only figures from its own working).
5. `grade-all --file` on the three sets: 0 failures (38 widgets).
6. Playthrough `--problems algebra/problems-<n> --local-cdn <pkgs>`: green for all three, with and without `--mobile`. Part shots at 440 px read: no overflow; the 6-cycle with entry 10 was respaced with `\;` after the first shot ran "3 10" together.

## Freshness

`fresh-check` first run: problems-1 and problems-2 0 hits. problems-3 had three errors and one warning, all fixed by rewriting: `p-fifteen-times` part 2 retold the explain and generic line of `review-3` item 5 ("By the first isomorphism theorem, |im| = ...", "Use |G| = |ker| |im|"), and its prose shared 10 words with exam item `e-hom-z18-z12`; `p-powers-of-seven` part 2 listed the divisor set 1, 2, 3, 4, 6, as `l5` screen 6 and `l7` screen 5 do. `p-hexagon-quotient` part 1 had copied the same generic line; rewritten. Rerun: 0 hits on each set.

Own-course greps (numbers, moduli, groups and nouns): 56, 21 as a modulus of a unit group, 19, 45, $\mathbb{Z}_{24} \to \mathbb{Z}_{36}$, $S_{10}$, the octagon and the desk rota appear nowhere in `courses/algebra` or the topic exam. Hash tables appear in `ds` l2 (no probing stride); `a + b + ab` appears in `brainteasers` as an invariant puzzle on rationals, not as a group modulo a prime. The hexagon appears in `review-1` (a count of 12) and a `why` line of `l7`; its quotient is new.

## Closest material per problem (lesson screen, quiz, review, homework, exam)

- **p-probe-stride.** l4 s4 (generators of $\mathbb{Z}_{12}$): here $\mathbb{Z}_{56}$ and the count is $\varphi(56)$. l3 quiz 3 ($\varphi(12)$): here phi counts generators. review-1 i4 ($7^{-1} \bmod 40$): here $9^{-1} \bmod 56$ then solves $9k \equiv 13$. homework-1 i7 ($6x \equiv 9 \pmod{15}$, 3 solutions): here a unit coefficient and one solution. Exam inverse of 17 mod 60: Euclid lines are not given, and the inverse feeds a further equation.
- **p-octagon-orders.** l1 s3 and l2 s7 ($D_4$ table, $(rs)^{-1}$): here 16 elements and the relation used algebraically. l1 quiz 0 (undo $r$): here undo a product of two flips, which is a turn. review-1 i2 ($(r \cdot r^2s)^{-1}$): here the product is a turn, so it is not its own inverse. homework-1 i3 (proof that orders of $g$ and $g^{-1}$ agree): here a numeric order and a count of $x^4 = e$. Exam `e-order-three-s6`: counts in $S_6$, not $D_8$.
- **p-shifted-product.** l2 s9 to s10 (returns under $\oplus$): here modulo 19, with the absorbing element found by a computation, then order and generators. l2 quiz 2 (returns above $-100\%$): here the excluded element is 18, found from $18 \ast 5$. review-1 i1 ($\max$ fails inverses): here inverses exist once 18 is out. homework-1 i6 ($a + b + 1$, identity): the identity is given; parts ask an inverse, an order and a generator count. Exam orders modulo 17: here the order comes through the shifted operation, and phi of 18.
- **p-desk-rota.** l8 s0 and s5 ($S_8$, order 6): here $S_{10}$ with lengths 6 and 4, so lcm differs from product. l9 quiz 2 ($|A_5|$): here an index in $A_{10}$. review-2 i6 (sign of a 5-cycle and a swap): here two even-length cycles, and a right-answer-wrong-reason option. homework-2 i7 (cosets of a 5-cycle in $S_5$): here the index is in $A_{10}$ and needs the sign. Exam bottom-row permutation (order 4): here $S_{10}$, then sign and index.
- **p-units-21-cosets.** l6 s1 (cosets of $\langle 4 \rangle$ in $\mathbb{Z}_{12}$, additive): here the multiplicative $\mathbb{Z}_{21}^{\times}$, with the additive coset as a slip. l5 quiz 2 (finite closure): here used to pick $H \cup 2H$. review-2 i1 (cosets in $\mathbb{Z}_9$): additive there. homework-2 i1 (proof of finite closure): here a numeric one-step test and a choice. Exam order of 15 mod 36 and its cosets: additive there.
- **p-fixing-five.** l6 s7 (left and right cosets of $\{e, s\}$ in $D_4$): here the stabiliser of 5 in $S_5$, cosets described by images, and the size of a left and right coset's overlap. l6 quiz 2 (cosets of $\{e\}$ in $D_4$): here index 5. review-2 i7 (cosets of $\langle s \rangle$): $D_4$ there. homework-2 i7 (cosets of $\langle(1\,2\,3\,4\,5)\rangle$ in $S_5$): a cyclic subgroup there, no left versus right. Exam: no stabiliser item; the nearest is the cosets of $\langle 15 \rangle$ in $\mathbb{Z}_{36}$, abelian.
- **p-fifteen-times.** l12 s0 to s2 ($3x$ on $\mathbb{Z}_{12}$, a coset per value): here $\mathbb{Z}_{24} \to \mathbb{Z}_{36}$ with a multiplier that is not a unit, and a preimage solved. l10 quiz 3 (kernel of $4x$ on $\mathbb{Z}_{12}$): one group there. review-3 i5 (image of $4x$ on $\mathbb{Z}_{20}$): here two groups, a preimage set and an order in the quotient. homework-3 i1 and i3 (kernel of $6x$ on $\mathbb{Z}_{18}$; homomorphisms $\mathbb{Z}_{12} \to \mathbb{Z}_8$): counts only there. Exam `e-hom-z18-z12` (kernel and image of $2x$): here also the preimage of 21 and the order of $2 + K$.
- **p-powers-of-seven.** l13 s7 ($7^{222}$ mod 10): here modulo 45, where the order 12 is below $\varphi(45) = 24$, the kernel of $k \mapsto 7^k$, and an inverse read off a power. l13 quiz 0 ($3^{-1} = 3^5 \bmod 7$): here a composite modulus, then a linear congruence. review-3 i7 ($2^{50} \bmod 15$) and homework-3 i5 ($3^{2026} \bmod 100$): one power there. Exam $5^{100} \bmod 14$: one power there.
- **p-hexagon-quotient.** l11 s5 and s6 ($D_4/\{e, r^2\}$, Klein): here $D_6/\{e, r^3\} \cong S_3$, found by counting elements of order 2, with the kernel size from the first isomorphism theorem. l11 quiz 3 ($|D_4/\langle r \rangle|$): a size only. review-3 i3 ($\{e, rs\}$ not normal in $D_4$): here a count of the normal subgroups of order 2 in $D_6$. homework-3 i2 ($\{e, (1\,2)\}$ in $S_3$): one subgroup there. Exam normal subgroup of $S_4$: a choice there.

No problem walks through several course items in a row; each is a chain on the level's skills in its own setting.

## Notes

- Commit trailers use the attribution the session's system reminder gives (`Claude Opus 5.5`); the brief named another model.
- `course.json`: no change proposed.
- Inbox: 1 bullet under `Raised later (problems algebra):`.

## Level 4

File: `app/content/courses/algebra/problems-4.json` (title "Problems: rings and fields", 40 minutes). Numbers: `docs/reports/problems-algebra-4-numbers.py` (173 of 173 checks, exit 0; `problems-algebra-numbers.py` is not touched).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-cipher-29 | 5 (4 / 1) | l14, l15 | 4 |
| problems-4 | p-sixteen-factorial | 5 (4 / 1) | l15, l16, l17 | 5 |
| problems-4 | p-three-year-return | 4 (4 / 0) | l16, l17 | 4 |

Typed parts: 12 of 14 (one `expression`, the rest `numeric`). Every lesson of level 4 appears; every problem draws on two or more. Skills: `ag-rings`, `ag-poly`, as the level's lessons carry them. The two choice parts are judgements: which reason makes a matrix a unit of $M_2(\mathbb{Z}_{29})$, and which step turns 16 roots into 16 linear factors.

Proof-heavy rule (brief rule 6): no part grades a typed formula and none prints its own target. The ideas are tested through numbers: a determinant and its inverse in a field, an adjugate entry, the constant term of $\prod(x - a)$ (Wilson's theorem, never named or printed), a count of rational-root candidates, a quotient polynomial, a count of real roots. Later parts restate earlier results only after those parts are checked.

### Gates (in the brief's order)

1. Validator: 0 errors; no warning on this file (two `[key-length]` warnings while drafting fixed by shortening the keyed options).
2. Voice scan 35 on the course folder: 0 and 0.
3. `fresh-check --file`: 0 hits. One error on the first run: the IRR quotient $2x^2 + 2x + 1$ matched a polynomial of `l16` screen 7; the cash flows were changed (now £6,000, £1,000, £5,000) so $f = (4x - 5)(2x^2 + x + 1)$. One advisory left: three shared parameters (27, 28, 23) with `mock-oa-trader` item 0, a mental-arithmetic item with no ring content; no action.
4. Number script: 173 of 173, exit 0. Method 1 by rule (ad - bc, Euclid, the adjugate, constant terms, the rational root test with exact fractions, long division in sympy, the discriminant); method 2 by brute force (inverse search in $\mathbb{Z}_{29}$, `inv_mod`, solving $\mathbf{K}\mathbf{p} = \mathbf{c}$ by search, multiplying $1 \cdots 16$ out, evaluating $x^{16} - 1$ at all 17 residues, expanding $\prod(x - a)$ in $\mathbb{Z}_{17}[x]$, `numpy.roots`). Each `wrong` value is recomputed from its named slip, has a byKey line and differs from the key; option claims are checked. `check_wrongs` passes; its two "check by hand" lines were read ("real" states $\pm 1$, the two roots; "discount" states 20% and 0.8).
5. `grade-all --file`: 0 failures (14 widgets).
6. Playthrough `--problems algebra/problems-4 --local-cdn <pkgs>`: green, with and without `--mobile`. Part shots at 440 px read: the matrices, the adjugate in feedback and the long prose of the deal fit; no overflow.

### Freshness

Own-course greps: $\mathbb{Z}_{29}$, $x^{16}$, $15!$, Hill, the matrix $\begin{pmatrix}9&4\\5&7\end{pmatrix}$, $8x^3$ and "rate of return" appear nowhere else in `courses/algebra` or the exams (an $8x^3$ in `topic-1.3` is calculus). $\mathbb{Z}_{17}^{\times}$ appears in `topic-3.4` as orders of elements, not a product of residues; $16!$ in `l9` counts the 15-puzzle; "cipher" in `l13` is RSA. IRR stories exist in `markets` l4 and `numerics` problems-2 (other courses, solved by search or Newton); here the rate comes from the rational root test and a factorisation.

### Closest material per problem (lesson screen, quiz, review, homework, exam)

- **p-cipher-29.** l14 s6 and s7 (matrix ring, $\mathbf{AB} \ne \mathbf{BA}$ over $\mathbb{R}$): here $M_2(\mathbb{Z}_{29})$, units by the determinant, then decoding. l14 quiz 0 (units form a group): here a matrix unit found through its determinant. review-4 i1 ($7^{-1} \bmod 15$): here the inverse feeds an adjugate and a decode. homework-4 i4 (secret from two shares over $\mathbb{Z}_{13}$, $3^{-1}$ given): here nothing is given and the step is a matrix inverse. Exam `e-which-fields`: a choice of fields there; here the field fact is used to invert a matrix.
- **p-sixteen-factorial.** l17 s2 and s3 (factor theorem, at most $d$ roots): here used to factor $x^{16} - 1$ completely and read $16!$ off the constant term. l17 quiz 1 (count of irreducible quadratics): a count there, no product. review-4 i5 (roots of $x^2 - 4$ in $\mathbb{Z}_{12}$): a non-field there; here every root is found by Fermat. homework-4 i8 (prove the $d$-roots bound; $x^2 - 1$ in $\mathbb{Z}_8$): here the bound is attained and turned into a factorisation. Exam `e-remainder-z7` (one remainder modulo 7): one evaluation there.
- **p-three-year-return.** l17 s7 (rational root test on $x^3 - 2$, monic, no root): here a non-monic cubic, 8 candidates, one root. l16 s6 (divide by $x - 3$ over $\mathbb{Q}$): here by $4x - 5$, with the quotient then judged by its discriminant. l16 quiz 1 (validity of a division): a judgement there. review-4 i4 (remainder of $x^3 + x + 1$ at 2): one remainder there. homework-4 i2 (division over $\mathbb{Z}_3$): coefficients modulo 3 there. Exam `e-irreducible-z3`: a choice over $\mathbb{Z}_3$; here the count of real roots over $\mathbb{R}$ fixes a unique rate of return.

No problem walks through several course items in a row; each is a chain on the level's skills in its own setting.

### Notes

- Commit trailers use the attribution the session's system reminder gives (`Claude Opus 5.5`).
- `course.json`: no change proposed. Inbox: no new bullet (no engine limit met).

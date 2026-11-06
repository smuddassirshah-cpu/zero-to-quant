# algebra level 3: Maps between groups

Author: content agent, worktree `worktree-agent-a2e95e571628c4b33`. Brief: `docs/briefs/algebra.md` `## Level 3`. Levels 1 and 2 were written in parallel by another agent and are not in this worktree; the lessons cite them by id (l1, l3, l5, l6, l7, l9) and restate the fact used on the screen.

## Files

| file | screens / items | quiz | canvases and widgets |
|---|---|---|---|
| `l10-homomorphisms.json` | 12 | 4 | table + table widget (log returns), complex-map $z^k$ on $\mu_{12}$ with a `stops` control, multi, order x3 (identity and inverses, kernel subgroup, injective iff trivial kernel), trap choice (well-definedness), SEDOL transfer numeric and choice, code `is_hom` / `kernel` (10 tests) |
| `l11-normal-subgroups.json` | 11 | 4 | grid $D_4$ Cayley table (tap row $s$; a `frames` control shading the cosets of $\langle r \rangle$; the table reordered by cosets of $\{e, s\}$ with four shade sets), table widget yes/no for the 10 subgroups, numeric, text table of coset squares, trap choice, order x2 (kernel normal; coset product well defined), choice (index 2), transfer numeric 480 |
| `l12-first-isomorphism-theorem.json` | 11 | 4 | grid 1 x 12 filled through a table widget with `bind`, tap-regions on it, grid of cosets, multi, trap choice, order (well defined), choice (homomorphism step), order (injective), order (whole proof, 8 lines, `same` on injective/onto), spot-the-flaw table with `tap: "rows"`, bars filled through a table widget (`values.k`) |
| `l13-fermat-and-euler.json` | 11 | 4 | grid of $a^k \bmod 7$ (row 2 typed in with `bind`), numeric, tap the first 1 in each row, generalise choice, order (Fermat), order with `same` (Euler), table ladder, numeric x2, RSA table, code `fermat_liars` / `is_carmichael` (10 tests) |
| `review-3.json` | 8 items, `pass` 0.8 | | homomorphism check, kernel, well-definedness, normality from a conjugate, quotient structure, isomorphism-theorem count, Fermat, Euler; difficulties 2, 2, 3, 3, 3, 3, 2, 4 |
| `homework-3.json` | 9 items | | difficulties 3, 3, 3, 4, 4, 4, 4, 4, 5: multi, numeric x4, choice, `order` ($g^m \in N$), `code` `quotient_table` (6 tests, two raise), `longform` performance task (`derivation`, 10-point rubric, full model) |

Performance task: the level matches the verb rule (objectives start "Prove"); `h-prove-fit` is `performance: "derivation"`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Warnings on these files: one "ladder reuses the previous canvas kind" per lesson (a ladder moving from a grid or complex-map to a table), the course's unwritten-lesson count, and level 3 locked until level 2 is written.
2. `VOICE_BASE=app/content/courses/algebra python3 docs/reviews/voice-scan.py`: explanations over three sentences 0; sentences over 20 words 0.
3. `python3 docs/reports/algebra-L3-numbers.py`: exit 0, 146 of 146 numbers_lib checks, every two-way computation and claim ok, 3 code widgets (solution passes, starter fails). `check_wrongs` prints nine "check by hand" lines; each byKey text names the wrong value in words or as a set (for example "the image $\{1, \zeta^4, \zeta^8\}$" for the wrong value 3), checked by hand.
4. Playthrough with `--local-cdn <scratchpad>/pkgs`: all 6 files passed without `--mobile` and with `--mobile` (l10 16 checks, l11 15, l12 15, l13 15, quizzes 4/4; review 8 of 8; homework 9 of 9, 39 of 39 marks, longform marked by the button). Screenshots looked at: complex-map at 440 px (image labels removed after the first run: overlapping images showed misleading "f(9)" labels), the 8 by 8 grids, the 12-column grid, the bars transfer, the spot-the-flaw table and the SEDOL tables (headers shortened to "1, 2").

## Proofs taught and the widget that grades each step

- $\varphi(e) = e$ and $\varphi(a^{-1}) = \varphi(a)^{-1}$: `order`, distractor "because $\varphi$ is a function" (l10 s5).
- $\ker\varphi$ is a subgroup by the one-step test: `order`, distractor "closure under products only" (l10 s6).
- Injective exactly when $\ker\varphi = \{e\}$, backward direction: `derive` `order`, distractor "so $a = b$ since $\varphi$ is a homomorphism" (l10 s8). The forward direction is stated.
- Kernels are normal: `order`, distractor $gkg^{-1} = k$ (l11 s7).
- Coset product well defined for normal $N$: `derive` `order`, distractor $n_1b = bn_1$ (l11 s8); which line uses normality: quiz `choice`.
- Index 2 implies normal: `choice` (l11 s9).
- First isomorphism theorem: step 2 well defined `order` (l12 s5), step 3 homomorphism `choice` for the reason (l12 s6), step 4 injective `order` (l12 s7), the whole skeleton `derive` `order` with distractor "$\psi$ injective because $\varphi$ is" (l12 s8), spot-the-flaw `tap-regions` on a table with `tap: "rows"`, the bad row skipping well-definedness (l12 s9); full written proof: homework `longform`.
- Fermat from Lagrange: `derive` `order`, distractor "$\mathbb{Z}_p$ has $p$ elements, so $a^p = 1$" (l13 s4); corollary $a^p \equiv a$: quiz `choice`.
- Euler: `order` with `same` on the two setup lines, distractor "ord divides $n - 1$" (l13 s5).
- RSA decryption: quiz `order`.
- $g^m \in N$ for $|G/N| = m$: homework `order` with `same`.

## Numbers and their sources

Every value below is recomputed two ways in `docs/reports/algebra-L3-numbers.py` and checked at its JSON path.

- l10: $\ln 1.10 = 0.09531$, $\ln 0.90 = -0.10536$, sum $-0.01005 = \ln 0.99$ (math.log and the atanh series); prices £110.00, £99.00; kernel of $z^4$ on $\mu_{12}$ is $j = 0, 3, 6, 9$, image 3 points; $\varphi(1 + 1) = 4$ against 2 for $x^2 \bmod 8$; $6 \bmod 4 = 2$ and $3 + 3 \equiv 2 \pmod 4$; SEDOL weighted sum 126, check digit 4 (wrong 6), 130, code 0263494; all 63 single-digit errors caught; undetected neighbour swaps are exactly digits 5 apart; stems 16 and 61 give 19 and 9; kernel of $4x$ on $\mathbb{Z}_{12}$ has 4 elements (wrong 3).
- l11: the Cayley table agrees with the matrix model of $D_4$; row $s$ holds rotations in columns 5 to 8; $rsr^{-1} = r^2s$; the conjugation table; 10 subgroups, 6 normal, 4 not; $1 + \langle 4 \rangle$ has order 4; every coset of $\{e, r^2\}$ squares into it; 1380 + 540 = 1920 ≡ 480 (mod 1440); $|D_4/\langle r \rangle| = 2$.
- l12: $3x \bmod 12$ table, kernel $\{0, 4, 8\}$, 4 cosets, $12 = 3 \times 4$; $|A_n| = n!/2$ for $n = 2$ to 6 by counting inversions; counts mod 6 on $\mathbb{Z}_{16}$ 3, 3, 3, 3, 2, 2 and mod 8 all 2; $15 + 1$ wraps differently; $|\mu_{12}/\mu_4| = 3$; $2^{32} \bmod 6 = 4$, 715,827,883 and 715,827,882, summing to $2^{32}$.
- l13: the power grid mod 7 and its orders 1, 3, 6, 3, 6, 2; $2^{100} \equiv 2 \pmod 7$ (wrong 4 from reducing the exponent mod 7); $\varphi(9) = 6$, $\varphi(12) = 4$, $5^4 = 625 \equiv 1 \pmod{12}$; $7^{222} \equiv 9 \pmod{10}$; $2^8 \equiv 4$, $2^6 \equiv 1 \pmod 9$; RSA $\varphi(33) = 20$, $3 \times 7 = 21$, $4^3 \equiv 31$, $31^7 \equiv 4$, $(-2)^7 = -128$, and decryption works for all 33 messages; $3^{340} \equiv 56 \pmod{341}$, $2^{340} \equiv 1$; $3^{560} \equiv 375 \pmod{561}$; $\varphi(561) = 320$; 561 is the smallest Carmichael number below 2,000; liars of 15 are 1, 4, 11, 14; $3^{-1} \equiv 3^5 \equiv 5 \pmod 7$.
- review-3: kernel of $z^3$ on $\mu_{12}$ has 3 elements; $8 \bmod 3 = 2$; $r(rs)r^{-1} = r^3s$; $|\operatorname{im} 4x| = 5$ on $\mathbb{Z}_{20}$; $5^{38} \equiv 4 \pmod 7$; $2^{50} \equiv 4 \pmod{15}$, $\varphi(15) = 8$.
- homework-3: kernel of $6x$ on $\mathbb{Z}_{18}$ has 6 elements; $(1\,3)(1\,2)(1\,3)^{-1} = (2\,3)$; 4 homomorphisms $\mathbb{Z}_{12} \to \mathbb{Z}_8$ ($\varphi(1) \in \{0, 2, 4, 6\}$, each checked on all pairs); $2^{100} \equiv 3 \pmod{13}$; $3^{2026} \equiv 29 \pmod{100}$ with $\varphi(100) = 40$, $3^{10} \equiv 49$; `quotient_table` tables for (12, 4), (12, 3), (12, 6), (5, 1), and (10, 4), (8, 3) raising.

## Conventions

Composition right to left, $D_4$ elements as $r^as^m$ with $sr = r^3s$, Cayley cell = row times column ("do the column, then the row"). Grid cell text in Unicode (r², r³s). Residue answers are numeric with a `wrong` entry for the unreduced value. Code screens say that checking every case proves the claim for that finite group only. No seeds or data files.

## Proposed course.json change

None.

## Backlog

Two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (algebra level 3):`.

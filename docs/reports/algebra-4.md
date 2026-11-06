# algebra level 4: Rings and fields

Author: content agent, worktree `worktree-agent-a2e95e571628c4b33`. Brief: `docs/briefs/algebra.md` `## Level 4`. Levels 1 and 2 are written in parallel elsewhere; the lessons cite l2, l3 and the level 3 lessons by id and restate the fact used.

## Files

| file | screens / items | quiz | canvases and widgets |
|---|---|---|---|
| `l14-rings.json` | 10 | 4 | grid $\mathbb{Z}_{12}$ multiplication table (tap 3 of the 17 off-axis zeros, count mode), table widget at $x = 6, 11$, multi for the four roots, order x3 ($0a = 0$ with a distractor, $(-a)b = -(ab)$, a unit is not a zero divisor), yes/no table of four rings beside a `matrix` canvas $\mathbf{AB} = \mathbf{0}$, `expression` pmatrix for $\mathbf{BA}$, trap choice, LCG `series` transfer |
| `l15-fields.json` | 10 | 3 | `pair` of grids $\mathbb{Z}_7$ and $\mathbb{Z}_6$ (tap the 1 in each row), inverse table, choice naming integral domain and field, order x3 ($\mathbb{Z}_p$ a field; finite integral domain a field, with distractor; composite $n$ fails), multi for $n = 2$ to 12, numeric $3x + 4 \equiv 2$, trap on a `pair` of $\mathbb{Z}_4$ and $\mathbb{F}_4$ grids, secret-sharing table over $\mathbb{Z}_{11}$ |
| `l16-polynomials.json` | 11 | 4 | grid of $x^i \cdot x^j$ (tap the $x^7$ cells), bars of two-dice counts, numeric x2, choice, $\mathbb{Z}_4[x]$ coefficient table, order (division algorithm existence), long division table with an `expression` for $q$, $\mathbb{Z}_5$ coefficient table, trap choice, CRC `console` with a bit table, code `poly_divmod` (8 tests) |
| `l17-roots-and-factors.json` | 11 | 4 | `plane` with three points dragged along the cubic to its roots (`drag-point` with `on` targets), synthetic division table, order x3 (factor theorem; at most $d$ roots, with distractor; degree 2 or 3 and roots), multi for roots in $\mathbb{Z}_8$, root-count table, choice for $x^3 - 2$, trap on a `plane` with $x^4 + 4$ and its factors, Sicherman `bars` with groups and a faces table, code `roots_mod` / `irreducible_small` (9 tests) |
| `review-4.json` | 8 items, `pass` 0.8 | | zero divisor, unit, field decision, inverse mod 11, remainder, root count in $\mathbb{Z}_{12}$, cubic over $\mathbb{Z}_3$, degree-4 trap; difficulties 2, 2, 3, 2, 3, 3, 3, 4 |
| `homework-4.json` | 9 items | | difficulties 3, 3, 4, 4, 4, 4, 4, 5, 5: unit of $\mathbb{Z}_4[x]$, $\mathbb{Z}_{221}$, division over $\mathbb{Z}_3$ (table), textbook CRC (table), secret over $\mathbb{Z}_{13}$, `order` (division algorithm uniqueness), roots in $\mathbb{Z}_{15}$, `code` `count_irreducible` with `poly_divmod` in the prelude (8 tests), `longform` performance task (`derivation`) |

Performance task: objective "Prove that the integers modulo a prime form a field" matches the verb rule; `h-prove-roots` is `performance: "derivation"`.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Warnings on these files: one ladder canvas-kind change (l14 screen 6, a grid to a matrix).
2. Voice scan on the whole course folder: explanations over three sentences 0; sentences over 20 words 0.
3. `python3 docs/reports/algebra-L4-numbers.py`: exit 0, 83 of 83 numbers_lib checks, every two-way computation and claim ok, 3 code widgets (solution passes, starter fails). `check_wrongs` prints eight "check by hand" lines; each byKey text names the slip in words (for example "You counted the points, 0 to 16" for the wrong value 17), checked by hand.
4. Playthrough with `--local-cdn`: all 6 files passed without `--mobile` (l14 14 checks, l15 13, l16 15, l17 15; review 8 of 8; homework 9 of 9, 41 of 41 marks) and with `--mobile`. Screenshots looked at: the 12 by 12 grid at 440 px (fits), the matrix pair, the CRC console, the Sicherman bars, the quartic plane (labels moved apart with `labelAt`) and the $\mathbb{Z}_4$ / $\mathbb{F}_4$ pair (a mark badge replaced by a shade).

## Proofs taught and the widget that grades each step

- $0a = 0$: `derive` `order`, distractor "because 0 times anything is 0" (l14 s3). $(-a)b = -(ab)$: `order` (l14 s4). Units form a group (closure): quiz `choice`. A unit is never a zero divisor: `order`, distractor using the zero product rule (l14 s5).
- $\mathbb{Z}_p$ is a field: `order`, distractor "$a < p$ so the gcd is 1" (l15 s3); why the gcd is 1: quiz `choice`. A finite integral domain is a field: `derive` `order`, distractor "onto because it is a homomorphism" (l15 s4); also homework-ready. Composite $n$ is not a field: `order` (l15 s5).
- $\deg(fg) = \deg f + \deg g$ over an integral domain: `choice` (l16 s3), with the $\mathbb{Z}_4[x]$ counterexample as a coefficient `table` (l16 s4). Division algorithm existence by induction: `derive` `order`, distractor without dividing by $b$ (l16 s5); where the field is used: quiz `choice`. Uniqueness: homework `order` with `same`.
- Factor theorem: `order`, distractor dropping $r$ (l17 s2). At most $d$ roots: `derive` `order`, distractor "in any ring" pointing at $\mathbb{Z}_8$ (l17 s3); in full with the $\mathbb{Z}_8$ failure: homework `longform`. Degree 2 or 3 reducible exactly when a root exists: `order` (l17 s5).

## Numbers and their sources

All recomputed two ways in `docs/reports/algebra-L4-numbers.py` (brute force against formula, or two independent polynomial routines) and checked at their JSON paths.

- l14: 17 off-axis zeros in $\mathbb{Z}_{12}$; zero divisors 2, 3, 4, 6, 8, 9, 10 and units 1, 5, 7, 11; $(x - 2)(x - 3)$ table, roots 2, 3, 6, 11, values 12 and 72 before reducing, 30 and 42 for the distractors; $\mathbf{AB} = \begin{pmatrix}2&1\\1&1\end{pmatrix}$, $\mathbf{BA} = \begin{pmatrix}1&1\\1&2\end{pmatrix}$, $E_{11}E_{22} = \mathbf{0}$; LCG periods 16, 8, 8 and both sequences; the Hull and Dobell rule checked against brute force for all 256 pairs $(a, c)$ mod 16; idempotents 0, 1, 4, 9.
- l15: inverses mod 7 ($2 \leftrightarrow 4$, $3 \leftrightarrow 5$, $6 \leftrightarrow 6$); rows 2, 3, 4 of $\mathbb{Z}_6$ without a 1; fields for $n \le 12$: 2, 3, 5, 7, 11; $x = 4$ for $3x + 4 \equiv 2 \pmod 7$; the $\mathbb{F}_4$ table ($\alpha(\alpha + 1) = 1$, $(\alpha + 1)^2 = \alpha$); shares $(1, 10), (2, 2), (3, 5)$, secret 7 from B and C, slope 3 from A and C with $2^{-1} = 6$ and $-30 \equiv 3$; over $\mathbb{Z}_{10}$ the lines $2 + 8x$ and $7 + 3x$ through $(1, 0)$ and $(3, 6)$.
- l16: coefficient of $x^7$ is 6, degree 12, coefficients 1 to 6 to 1; $(2x + 1)^2 = 1$ in $\mathbb{Z}_4[x]$; $x^3 - 2x^2 - 4 = (x^2 + x + 3)(x - 3) + 5$, with $f(3) = 5$; over $\mathbb{Z}_5$, $q = 3x^2 + x + 3$, $r = 3$, by long division and by brute-force search; $x^2 + 1 = (\tfrac12 x - \tfrac14)(2x + 1) + \tfrac54$ over $\mathbb{Q}$; CRC 1110 by XOR and by polynomial division, packet 11010110111110; `poly_divmod` tests including the monic $\mathbb{Z}_7$ case $x^3 + 3x + 2 = x(x^2 + 1) + (2x + 2)$ and $(4 + 3x^2 + x^3) \div (3x + 2)$ over $\mathbb{Z}_7$ giving $q = 5x^2$, $r = 4$.
- l17: roots 1, 2, 3 and $f = (x - 1)(x^2 - 5x + 6)$; roots of $x^2 - 1$ in $\mathbb{Z}_8$ (1, 3, 5, 7) and $\mathbb{Z}_7$ (1, 6); roots of $x^2 + 1$ in $\mathbb{Z}_2, \mathbb{Z}_3, \mathbb{Z}_5$ (1, 0, 2); $x^3 - 2$ at $\pm 1, \pm 2$; $x^4 + 4$ and $x^4 + x^2 + 1$ factorisations; $x^4 + x + 1$ irreducible over $\mathbb{Z}_2$; irreducible counts 1, 3, 10, 2, 8, 3, 18 and 2 by trial division and by the Möbius formula; Sicherman faces and equal distributions.
- review-4: $6 \times 5 \equiv 0$, $7^{-1} \equiv 13 \pmod{15}$, $91 = 7 \times 13$, $4^{-1} \equiv 3 \pmod{11}$, remainder $f(2) = 11$ (wrong $f(-2) = -9$), four roots of $x^2 - 4$ in $\mathbb{Z}_{12}$, the cubic over $\mathbb{Z}_3$, $(x^2 + 1)^2$.
- homework-4: $2x + 1$ the only unit among the options; $221 = 13 \times 17$; over $\mathbb{Z}_3$, $x^4 + 2x^3 + x + 1 = (2x^2 + 1)(2x^2 + x + 2) + 2$ by two routines; textbook CRC 100; secret 5 over $\mathbb{Z}_{13}$ with slope 4; four roots of $x^2 - 1$ in $\mathbb{Z}_{15}$; the `count_irreducible` starter (no-root count) gives 4 at $(2, 4)$.

## Conventions

Polynomials as coefficient lists lowest degree first in code; residues typed as numbers in $\{0, \dots, p - 1\}$ with a `wrong` entry for the unreduced value or $\tfrac12$. Code screens state that tests on chosen inputs are evidence, and exhaustive search proves a claim for one field only.

## Proposed course.json change

None.

## Backlog

One bullet in `docs/BACKLOG-INBOX.md` under `Raised later (algebra level 4):`.

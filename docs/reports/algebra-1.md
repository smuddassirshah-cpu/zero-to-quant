# algebra level 1 (Groups): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l1-symmetries.json` | 10 screens (problem, explore, derive, problem, ladder, problem, trap, problem, derive, transfer) | 4 |
| `l2-group-axioms.json` | 12 screens (problem, explore, 3 ladder, derive, problem, trap, derive, 2 transfer, code) | 4 |
| `l3-modular-arithmetic.json` | 12 screens (problem, explore, 2 ladder, derive, derive, problem, problem, trap, problem, transfer, code) | 4 |
| `l4-cyclic-groups.json` | 11 screens (2 explore, derive, problem, ladder, 2 problem, trap, 2 transfer, code) | 4 |
| `review-1.json` | 8 items, difficulty 2 to 4, `pass: 0.8`, every item `ag-groups` | |
| `homework-1.json` | 8 items, difficulty 3 to 5: longform (5), order Bezout (4), code `is_cyclic_units` (4), order ord(g⁻¹) (4), table missing row (4), three numerics (3, 3, 4) | |

Skill `ag-groups` throughout; objectives copied from `course.json`. No lesson objective starts with a verb of the performance rule (Combine, Check, Work, Find), and the validator does not flag the level, so there is no performance task.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors; no warning on a level 1 file.
2. `VOICE_BASE=app/content/courses/algebra python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words, 0 explanations over three sentences.
3. `python3 docs/reports/algebra-L1-numbers.py`: exit 0, 122 of 122 checks (plus every two-way recompute and both code checks per widget). The "check by hand" lines were read: each byKey names the slip and states the right count, not the wrong value.
4. Playthrough with `--local-cdn` (scratchpad `pkgs`): all six files green on desktop and with `--mobile` (440 px). Screenshots read at 1280 and 440: the 8 by 8 Cayley grid fits at 440, the l2 axiom table was made compact after a 440 shot showed it scrolling.

## Proofs and the widget that grades each step

- l1: count of $D_4$, `order` with the 4 × 3 distractor (derive); closure and undo, `order` with "two flips make a flip".
- l2: inverses unique, `order` of five lines with the $a^{-1}$ distractor (derive); identity unique, three-line `order` (quiz, no `same`); cancellation, `order` with "divide by a"; $(ab)^{-1} = b^{-1}a^{-1}$, `choice` on $D_4$ then `order` with the commuting distractor.
- l3: addition well defined, `order`; unit implies gcd 1, `order` with "a is odd" (derive); converse, `choice` (Bezout step); homework repeats the converse as an `order` with the divide-by-a distractor.
- l4: $g^k = e \iff m \mid k$, `order` with "$k = m$" (derive). Homework: $\operatorname{ord}(g^{-1}) = \operatorname{ord}(g)$, `order`; $x^2 = e \Rightarrow$ abelian, longform with a 10-point rubric.

## Numbers and sources

All recomputed in the script, method 1 by brute force (matrices, corner maps, enumeration of residues), method 2 by formula:
$|D_4| = 8$ (4 × 2; 12 is the distractor), 4 flips; $sr = r^3s = \begin{pmatrix}0&1\\1&0\end{pmatrix}$ fixing corners 1, 3 and $rs$ fixing 2, 4; the full $D_4$ table and its 8 identity cells; triangle corners $(\mp 0.8660, -0.5)$, 6 symmetries; rectangle $\{e, r^2, s, r^2s\}$; straddle and butterfly symmetric, call and risk reversal not (its mirror is its negative); pentagon 10, hexagon 12. $(5-3)-1 = 1$ against 3; $1.10 \times 0.90 - 1 = -1\%$; undoing $-20\%$ needs $25\%$ ($0.8 \times 1.2 = 0.96$). $7 + 9 \equiv 4 \pmod{12}$; units of $\mathbb{Z}_{10}$ and $\varphi(10) = 4$; solutions $\{2, 7\}$ and $\{8\}$; Euclid remainders 5, 2, 1 and $1 = 3 \times 26 - 11 \times 7$; $7^{-1} \equiv 15$, $7^{24} \equiv 1 \pmod{26}$; units of 12 square to 1, $\varphi(12) = 4$; $90 \equiv 6 \pmod 7$, Thursday; $17^{-1} \equiv 2753 \pmod{3120}$ (confirmed). Orders 3, 4, 2 of 8, 9, 6 in $\mathbb{Z}_{12}$; generators 1, 5, 7, 11; $z^4$ gives 3 images, $z^5$ gives 12; $\zeta = 0.5 + 0.866i$, $\zeta^3 = -1$, $\operatorname{ord}(\zeta^2) = 3$; $\mathbb{Z}_8^{\times}$ orders 2, 2, 2; $\operatorname{ord}(2) = 3$, $\operatorname{ord}(3) = 6$ mod 7; quarterly cycle 4; $\operatorname{lcm}(8, 12) = 24$. Review: $7^{-1} \equiv 23 \pmod{40}$ ($7^{38} \equiv 9$ is the prime-rule slip), $\operatorname{ord}(18) = 5$ in $\mathbb{Z}_{30}$, 2 generates $\mathbb{Z}_9^{\times}$. Homework: $\operatorname{ord}(2) = 10$ mod 11, identity $-1$ of $a + b + 1$, three solutions 4, 9, 14 of $6x \equiv 9 \pmod{15}$; `is_cyclic_units` True for 2, 7, 9, 10, 18, 25, 27 and False for 8, 12, 15, 20, by brute force and by the $1, 2, 4, p^k, 2p^k$ theorem.

`generators(1)` (l4 code): decided as `[0]`, since $\mathbb{Z}_1 = \{0\}$ and 0 has order $1 = n$; the screen's hint says so.

## Code widgets (CPython check in the script; Pyodide in the playthrough)

- l2 `is_group`: 8 tests; the closure-only starter fails `mul5-zero` and `sub5`.
- l3 `inverse_mod`: 8 tests; the `pow(a, n - 2, n)` starter fails 6 (7-26, 3-10, 4-10, 17-3120, 9-10, 6-9) and passes (1, 2) and (3, 7).
- l4 `element_order`, `generators`: 8 tests (one `raises`); the starter's stub and odd-number `generators` fail all 8.
- homework `is_cyclic_units`: 11 tests; the prime-test starter fails 9, 10, 18, 25, 27.

## Choices worth a second look

- l3 trap: the inverse of 7 modulo 26 is asked after the Euclid table, with `wrong` 1 for $7^{24}$ (the prime rule) and 11 for the dropped sign.
- l1 transfer uses a `frames` control over four payoffs on a `plane`; the mirror curve sits on top of a symmetric payoff.
- `course.json`: no change proposed.

## Backlog

Three bullets under `Raised later (algebra level 1):` in `docs/BACKLOG-INBOX.md`. The matrix overlay on `vectors` (basis arrows and unit square cannot be hidden) is already in the inbox and was not raised again.

# algebra level 2 (Inside a group): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l5-subgroups.json` | 12 screens (explore, problem, derive one-step test, problem, problem, derive subgroups of Z, problem, ladder, trap, problem, transfer, code) | 4 |
| `l6-cosets.json` | 11 screens (explore, problem, ladder, problem, derive, derive, trap, problem, problem, transfer, code) | 3 |
| `l7-lagrange.json` | 11 screens (explore, problem, derive, place, 4 problem, trap, 2 transfer); no code, as the brief says | 3 |
| `l8-permutations-and-cycles.json` | 12 screens (problem, ladder, 2 problem, derive, 3 problem, trap, 2 transfer, code) | 4 |
| `l9-odd-and-even.json` | 12 screens (2 problem, problem, derive, 3 problem, problem, trap, problem, transfer, code) | 3 |
| `review-2.json` | 8 items, difficulty 2 to 4, `pass: 0.8`; skills `ag-cosets` (5) and `ag-perm` (3) | |
| `homework-2.json` | 8 items, difficulty 3 to 5: performance longform (5), order (4), code `solvable` (5), code `has_subgroup_of_order` (4), four numerics or choices (3 to 4) | |

Skills `ag-cosets` (l5 to l7) and `ag-perm` (l8, l9); objectives and titles copied from `course.json` (typographic apostrophes kept). The objectives of l5 and l7 start with "Prove", so the level matches the performance rule: `h-lagrange` carries `"performance": "derivation"` (no hints, rubric of six rows summing to 10, model shown on marking). It is the level's only performance task.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Level 2 warnings left: "a problem screen without a canvas before the ladder ends" on proof and count screens with no diagram (l7, l8, l9).
2. `VOICE_BASE=app/content/courses/algebra python3 docs/reviews/voice-scan.py`: 0 sentences over 20 words, 0 explanations over three sentences (whole course folder, levels 1 and 2).
3. `python3 docs/reports/algebra-L2-numbers.py`: exit 0, 126 of 126 checks, every two-way recompute agreeing, both code checks per widget. The 17 "check by hand" lines were read: each byKey names its slip and states the right figure.
4. Playthrough with `--local-cdn`: all seven files green on desktop and with `--mobile`. Screenshots read at 1280 and 440 (D4 lattice, the 12 by 12 addition grid, the 15-puzzle board, the card boxes, the lattice of Z12).

## Proofs and the widget that grades each step

- l5: one-step test, `order` with "H is closed, so e ∈ H" (derive); every subgroup of Z is nZ, `order` with "H contains 1" (derive); nZ by the test, `order` (quiz); det(AB⁻¹) = 1, `choice`; N not a subgroup, `choice` (trap); finite closure suffices, `choice` (quiz) and `order` with the a⁰ distractor (homework).
- l6: aH = bH ⇒ a⁻¹b ∈ H, `order` (quiz), the converse used by a `choice`; equal or disjoint, `order` with "the overlap is a subgroup" (derive; its last line cites the previous one, so no `same`); |aH| = |H| by the bijection, `order`.
- l7: Lagrange, `order` of five lines with the "subset whose size divides" distractor (derive), then `place` in assign mode matching reasons to claims; ord(g) divides |G|, `choice`; prime order cyclic, `choice`; the converse, `choice` (trap); full proof as the performance longform.
- l8: order = lcm of lengths, `order` with "product of the lengths" (derive).
- l9: parity well defined by inversions, `order` with "a transposition changes the count by exactly 1" (derive); the 15-puzzle invariant, `order` with "the blank has moved" on a chessboard-shaded grid.

## Numbers and sources (all recomputed twice in the script)

Z12: 6 subgroups, 7 Hasse lines; D4: 10 subgroups (1, five of size 2, three of size 4, 8), 15 Hasse lines; ⟨8⟩ = {0, 4, 8}, ⟨4, 6⟩ = ⟨2⟩, ⟨9, 6⟩ = ⟨3⟩, ⟨5⟩ = Z12, |⟨r⟩| = 4, |⟨r, s⟩| = 8; 2 + 3 = 5; gcd(100, 250) = 50 = 3 × 100 − 250. Cosets of ⟨4⟩ and of {0, 3, 6} in Z9; left cosets of {e, s} and Hr = {r, r³s}; 6 cosets of ⟨6⟩; 250/5 = 50. Orders mod 13: 12, 3, 4, 2; A4 has subgroups of orders 1, 2, 3, 4, 12 and none of 6 (462 subsets checked); 2³¹ − 1 = 2147483647 prime, p − 1 = 2 · 3² · 7 · 11 · 31 · 151 · 331, 16807 = 7⁵ of order p − 1. σ = (1 5 4)(2 3 8)(6 7): order 6, 15 inversions, sign −1; (1 2)(2 3) = (1 2 3), (2 3)(1 2) = (1 3 2); orders 6, 15, 4; maxima 12 (S7) and 15 (S8); 8-card out-shuffle order 3, (1 2 4)(3 6 5), sign +1; 52-card out-shuffle order 8 (2⁷ ≡ 26 mod 51) and in-shuffle 52; 16! = 20,922,789,888,000 and half 10,461,394,944,000; a breadth-first search of the 2 by 3 puzzle reaches 360 of 720; |A4| = 12, |A5| = 60; derangements of 4: 9 (six 4-cycles, three double swaps); Kendall: 3 discordant pairs, τ = 0.4 (two formulas; SciPy is not installed here, so not against `kendalltau`). Homework: 100 prisoners 1 − Σ 1/k = 0.3118 (exact, and again by counting permutations with a long cycle; no simulated figure is stated in the content); 9 elements of order 2 in S4; 24 cosets of a 5-cycle in S5.

## Code widgets (CPython in the script; Pyodide in the playthrough)

- l5 `generate`: 8 tests; the starter `sorted(set(gens) | {e})` fails 6 (passes `s`, `0`).
- l6 `left_cosets`: 7 tests; the starter `[H]` fails 6 (passes H = G).
- l8 `cycles`, `perm_order`: 8 tests; the starter fails 6 (passes the identity cases).
- l9 `sign`: 9 tests; the starter, (−1) to the number of non-trivial cycles, fails only the even cycles of odd length: the 3-cycle `(1, 2, 0)` and the 5-cycle `(1, 2, 3, 4, 0)`. The 52-card out-shuffle has sign −1.
- homework `solvable`: 6 tests. Planted board: `random.seed(2026)`, 200 random legal slides from solved, giving `[1, 2, 3, 6, 9, 0, 10, 11, 8, 15, 14, 4, 5, 13, 7, 12]` (solvable); with its first two tiles swapped, unsolvable. The tile-inversion starter fails only `slide-up` (blank moved up one: the tiles' inversion count changes by 3). The rule is also checked against a breadth-first search of every 2 by 3 board.
- homework `has_subgroup_of_order`: 6 tests; the Lagrange-converse starter fails `(A4, 6)` only.

## Choices worth a second look

- l9 hook: a `manipulate` target must be reachable, so the learner brings the blank home with a four-slide loop (three tiles cycle, 14 and 15 stay swapped), and a refused "swap 14 and 15" chip states the rule. The next screen asks whether the board can be solved.
- l5 hook: grid heads cannot be tapped, so the learner taps the e cells inside the rotation block (the rest dimmed).
- `course.json`: no change proposed.

## Backlog

Two bullets under `Raised later (algebra level 2):` in `docs/BACKLOG-INBOX.md`.

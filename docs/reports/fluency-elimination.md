# Fluency sets: elimination (brief `docs/briefs/fluency.md`, second wave, agent 2, topic 1.4)

Two of the eight topic 1.4 sets. Chosen lessons, one line of reason each:

- `l2-back-substitution`: solving a triangular $3 \times 3$ system, bottom up and (as the lesson's last screens do) top down.
- `l10-computing-dets`: cofactor expansion along row 1, the effect of row operations, and the determinant from pivots and swaps.

Considered and left out: `l1-one-pivot-at-a-time` and `l3-factorisation` (the answer is a reduced matrix or $\mathbf{L}$ and $\mathbf{U}$, a whole matrix; see engine limits), `l4-zero-pivot`, `l5` to `l8` (column space, nullspace, bases, rank: ideas and judgements whose answers are spaces or sentences), `l9-area-scale` (the $2 \times 2$ determinant is drilled in `vectors/fluency-l10-undoing`), `l11-squashed` and `l12-redundant-assets` (judgements).

| set | family | distinct prompts in 200 | `form` | slips (`wrong` ids) |
|---|---|---|---|---|
| fluency-l2-back-substitution | bottom-up | 200 | none (vector) | pivot-not-divided, found-order, sign-not-changed |
| | top-down | 200 | none (vector) | pivot-not-divided, sign-not-changed |
| fluency-l10-computing-dets | cofactors-row-one | 200 | none (numeric) | no-checkerboard, minus-on-last |
| | row-operations | 198 | none (numeric) | swap-ignored, scale-ignored, add-counted |
| | pivots-and-swaps | 191 | none (numeric) | swaps-ignored, flipped-once, added-pivots |

The answers to the systems are the vector $(x, y, z)$, as in the lesson. The slips are the lesson's: stopping at $2x = 4$, moving a term without changing its sign (worked through to the wrong $x$ and $y$), listing $z$ first, the missing minus at position $(1, 2)$, forgetting a swap, and two swaps flipping once. Every unknown and coefficient is non-zero, so no working line reads `+0` or `1y`.

## Checks

1. `docs/reports/fluency-elimination-numbers.py` (sympy, 200 draws a family): systems by `linsolve`, determinants by `Matrix.det` and `minor`, the row operations applied to a real matrix built with the drawn determinant, then `det` again. 3,227 checks, 0 failures, exit 0 (a coinciding slip pair found on the first run is now excluded).
2. Validator 0 errors, no warning on these files. `test-fluency.mjs --local-cdn`: 298/298 and 304/304.
3. Playthrough `--fluency --local-cdn`, with and without `--mobile`: green for both sets. The 440 px screenshots of a $3 \times 3$ item and its wrong-answer screen show no overflow.
4. `voice-scan.py 35` on `app/content/courses/elimination`: 0 and 0.
5. I read 20 drawn items of every family and scanned 200 a family for `1x`, `+-`, `^1`, `0x`, `--`, `+0`, `-0` and float artefacts: no hits. Reading found "There were one row swap", reworded.

## Engine limits

The whole-matrix answer that `l1` and `l3` would need is raised in `docs/BACKLOG-INBOX.md` under `Raised later (fluency vectors elimination eigen least-squares):`.

# Topic 0.5 exam: mental arithmetic

File: `app/content/exams/topic-0.5.json` (id `topic-0.5`, 45 minutes, pass 0.7). Minutes follow `examMinutes` in `learn.js`: topic 0.5 is 20 h, at most 60 h, so 45.
Generator and checks: `scratchpad/exam-0.3-0.5/gen05.py` (builds the file and asserts every answer two ways: directly, and by the mental method the item teaches).

## Shape

20 numeric items, each a sum done in the head ("In your head, no paper."), to suit the topic's exit, a Zetamac score. The brief asked for 16 to 22; the validator requires at least 20.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 4 | 20% | 20% |
| 3 | 10 | 50% | 50% |
| 4 | 4 | 20% | 20% |
| 5 | 2 | 10% | 10% |

| # | id | d | skills | sum | answer |
|---|---|---|---|---|---|
| 1 | m-add-bridge | 2 | ma-add | 47 + 38 | 85 |
| 2 | m-table-seven | 2 | ma-mult | 7 × 12 | 84 |
| 3 | m-divide-eight | 2 | ma-div | 56 ÷ 8 | 7 |
| 4 | m-seven-twentieths | 2 | ma-frac | 7/20 as a decimal | 0.35 |
| 5 | m-change-100 | 3 | ma-add | change from £100 for £36.40 | £63.60 |
| 6 | m-chain | 3 | ma-add | 38 + 27 − 15 + 42 | £92 |
| 7 | m-count-up | 3 | ma-add | 512 − 268 | 244 |
| 8 | m-split-78 | 3 | ma-mult, ma-add | 6 × 78 | 468 |
| 9 | m-times-98 | 3 | ma-mult | 8 × 98 | 784 |
| 10 | m-times-25 | 3 | ma-mult | 25 × 36 | 900 |
| 11 | m-square-23 | 3 | ma-mult | 23² | 529 |
| 12 | m-halve-336 | 3 | ma-div | 336 ÷ 8 | 42 |
| 13 | m-fifteen-pc | 3 | ma-frac | 15% of £480 | £72 |
| 14 | m-three-fortieths | 3 | ma-frac, ma-div | 3/40 as a decimal | 0.075 |
| 15 | m-either-side | 4 | ma-mult | 47 × 53 | 2491 |
| 16 | m-halve-both | 4 | ma-div | 378 ÷ 14 | 27 |
| 17 | m-fee | 4 | ma-frac | 0.35% of £2,400 | £8.40 |
| 18 | m-near-70 | 4 | ma-mult | 68 × 47 | 3196 |
| 19 | m-net-pnl | 5 | ma-mult, ma-add | 35 × £2.40 − 15 × £1.80 | £57 |
| 20 | m-return-pc | 5 | ma-div, ma-frac | £1,170 on £18,000 | 6.5% |

Skills: all 4 of the topic are covered: ma-add 6, ma-mult 8, ma-div 5, ma-frac 5. Every item names one or two slips as `wrong[]` entries with a `byKey` line, taken from the course's traps: the dropped carry (75, 428), paying back the gap alone (798, 3288), the missing middle strip of a square (409, 469), halving too few times (84, 168), a decimal point one place out (7.2, 84, 0.84, 0.65%), a flipped fraction (2.857, 15.38%).

Fresh against the course: each sum was searched in the mental course. Three first drafts matched and were replaced: 7 × 99 (l7) became 8 × 98, 3/8 (l10) became 7/20, and a return on £24,000 (homework 3) became £1,170 on £18,000.

## Numbers computed twice

`gen05.py` asserts each answer by direct arithmetic (exact `Fraction` for the decimals and percentages) and by the item's own method: tens then units, rounding and paying back, $a^2 - b^2$, $(a + b)^2$, three halvings, halving both, 10% plus 5%, 1% then a fraction of it. The wrong values are asserted too (3150, 64.60, 12 and 15.38).

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no warning for this file.
- Copy lint (`lint.py`): no `!`, no em or en dash, no sentence of 20 words or more, no American spellings.
- `playthrough.mjs --exam topic-0.5 --local-cdn <pkgs>`: 20 of 20, passed, desktop and `--mobile`.
- Screenshots reviewed (`scratchpad/exam-0.3-0.5/shots05`): the £ and % units sit inside the input on both widths; nothing to fix.

## Engine notes

In `docs/BACKLOG-INBOX.md`: a topic exam has one clock and no per-question timing, so the mental exam cannot time each sum as Zetamac does; the 20-item floor for a 20-hour topic.

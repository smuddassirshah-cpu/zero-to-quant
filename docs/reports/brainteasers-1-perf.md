# brainteasers level 1: performance task

- File: `app/content/courses/brainteasers/homework-1.json`, item `hw9-l-pieces-6x10` appended (index 8, item 9 of 9). Nothing converted; the homework had 8 items.
- Kind: `derivation` (longform, empty box, no hints or steps). Difficulty 5, skill `bz-invariant`, no `tags`.
- Objective (verb rule, "prove"): l2 "Prove a tiling or a route impossible by colouring the board." The only objective of the level that matches.
- Task: prove fifteen L-tetrominoes cannot cover a 6 × 10 board. The chessboard balances every L (2 and 2), so the learner must choose stripes. The model gives a reason for every line: area, why the chessboard fails, both orientation cases of the 3 and 1 split, $4a - 30 \ne 0$, the board's 30 and 30.
- Rubric: 2, 2, 3, 3; the count row (±2 per piece, $4a - 30$ never 0, against 0) is `required`. Bundled rows open "Tick only if".
- Freshness grep: L-tetromino, L-shaped, stripe, column, 6 × 10, alternate rows. No hit uses the piece, the board or the stripe colouring as a proof; l2 shows alternate rows only as a wrong option for 1 × 3 tiles. `fresh-check --file` gives no hit on the item.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; "brainteasers/L1: has a performance task, remove from perf-pending" as expected.
2. `VOICE_BASE=app/content/courses/brainteasers python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/brainteasers-1-perf-numbers.py`: exit 0, 40 checks. Colour counts square by square and by formula; the 8 orientations generated and hand-written; every one of 304 placements is 3 and 1 on stripes, 2 and 2 on the chessboard; two independent exhaustive searches find 0 tilings of 6 × 10 (controls: 2 × 4 gives 2, 4 × 4 gives 10, 3 × 8 gives 4).
4. `node tools/playthrough.mjs --set brainteasers/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed. Shots at 1280 and 440 px: the display equation fits; no sideways scroll.

Backlog: 0 new bullets (the coach tip over the marked shot is BACKLOG-INBOX "Homework page: the first-visit coach tip").

Overlapping screens: l2 screens[4] (straight 1 × 4 tiles on a 6 × 6 board by stripes) and [7] (that proof in order), screens[8] (T-tetrominoes by the chessboard colouring), review-1 `r4-t-pieces-4x7`, homework-1 `hw8-say-it-10x10` (the stripe colouring said aloud); new parts: the L-tetromino, which the chessboard cannot separate (2 and 2), so the learner must choose stripes on a 6 × 10 board, both orientation cases of the 3 and 1 split, and the count $4a - 30 \ne 0$.

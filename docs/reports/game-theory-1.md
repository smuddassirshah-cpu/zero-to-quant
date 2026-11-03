# Report: game-theory level 1 (Games in a table)

Brief: `docs/briefs/game-theory.md`, `## Level 1`, its preamble and `## Number checks`. Ids, names, objectives and skills from `app/content/courses/game-theory/course.json` (`gm-normal` on l1 to l3, `gm-mixed` on l4 and l5).

## Files written

| File | Screens or items | Quiz | Shape |
|---|---|---|---|
| `l1-payoff-tables.json` | 9 screens | 4 | hook tap (Ana's best replies), Ben's best replies, story into a table (table widget bound to the grid), best reply to Wait, trap (whose numbers), tie edge case, generalise, drill (pair of grids, table), follow-up spread table |
| `l2-dominated-moves.json` | 11 screens | 3 | hook choice (desks), prisoner's dilemma numeric, deletion by `manipulate` on the 3 × 3 with refused steps, beaten by a mix (choice, then numeric), trap (weak deletion), edge (matching pennies), generalise, drill (table), two follow-up screens (three desks: choice, then numeric 3000) |
| `l3-nash-equilibrium.json` | 9 screens | 3 | hook tap (both sets shaded), nobody moves alone, venues, race, trap (desks), edge (pennies), generalise, drill (three games through a `frames` control, table), follow-up tap on the spread table |
| `l4-mixing.json` | 9 screens | 3 | explore (plane, slider on q), each half the time, unequal venues (table), raised prize, trap (whose payoffs set the mix), edge (crossing at q = −1/2), generalise, drill (table), follow-up rock, paper, scissors |
| `l5-zero-sum.json` | 10 screens | 3 | hook tap of row minima (table canvas), column maxima and the saddle (table), penalty kick (plane, slider), 2 × 3 lower envelope (plane, slider), trap (unequal pennies, choice), its value (numeric), edge (formula gives p = 3), generalise, drill (table), follow-up Ben's seat |
| `review-1.json` | 9 items, difficulty 2 to 4 | | every game unseen, interleaved l1, l2, l5, l3, l4, l2, l3, l5, l3; each item has `skills` and `tags` |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5) | | `order` derivation with a distractor, `code` `pure_nash`, deletion numeric, mixed numeric, `code` `solve_zero_sum_2x2` (5), `multi`, 2 × 3 value, `longform` (5) with a 10-point rubric |

Every drill screen, review item and homework item carries `tags` from the brief's families; quiz items are tagged too. `shuffle: true` on every `choice` and `multi`. Each lesson's first screen with a table says Ana is the row, Ben the column, cells (Ana, Ben) in £. Free resources are named once, in the l1 drill prose: the *Probability and Markets* guide (a trading firm about its own interviews), Open Yale Courses' *Game Theory* lectures, and Zhou's green book and Crack's *Heard on the Street* as holding "a few game and betting questions". No firm is named.

## Validator

`node tools/validate.mjs`: 0 errors; no warnings on game-theory files other than the course's unwritten levels 2 and 3. Voice scan (`VOICE_BASE=/home/user/zero-to-quant/app/content/courses/game-theory/`): 0 sentences over 20 words, 0 explanations over three sentences.

## Playthrough

`node tools/playthrough.mjs --lesson game-theory/<id> (all five) --set game-theory/review-1 --set game-theory/homework-1 --mobile --why --local-cdn <pkgs>`: all passed. l1 13 checks, quiz 4/4; l2 14 checks, quiz 3/3; l3 12 checks, quiz 3/3; l4 12 checks, quiz 3/3; l5 13 checks, quiz 3/3; review-1 9 of 9; homework-1 8 of 8 right, 37 of 37 marks. After the last label fix, l4 and l5 were replayed (desktop and 390 px): both passed. Screenshots (desktop, 390 px, Why? sheets) in the scratchpad `game-theory-1/shots` and `shots2`. Layout fixes made after looking: the drill pair now sits side by side on desktop (it was forced to stack) and the prose names the tables "2 × 3" and "3 × 3"; every tap screen's `explain.canvas` clears `selected` so the two shade sets show; the l4 pennies and edge planes put the x axis at the bottom (the x label hit a line label at 390 px); the l5 envelope pins each line label with `labelAt` (one had landed beside the wrong line); the l5 penalty x label is shorter. Four-column tables (three desks, rock, paper, scissors, the savings table) fit at 390 px.

## Numbers and their sources

All checked twice in `<scratchpad>/game-theory-1/checks.py` (output `checks.log`) and `checks_new.py` (`checks_new.log`). Method 1: exact best-reply sets, iterated strict deletion in rounds, closed-form 2 × 2 mixing with `fractions`. Method 2: a direct "no gain from moving alone" test on every cell, a one-move-at-a-time deletion order, the indifference re-evaluated in floats at the mix, and a grid search over p in steps of 1/200,000 (1/20,000 for the code tests; a 400 or 600 step simplex grid for the two rock, paper, scissors games).

- l1: Ana's best replies r1c1, r3c2, r2c3; Ben's r1c3, r2c1, r3c2; trap L (Ben's 3, 1, 0); tie L and R; drill counts 3 and 2, beliefs U 2.6, M 2.2, D 1.6; Buy best to both; spread table cells, Ana's best reply to 3 ticks is 2 ticks, £200 (100 at 1 tick, 150 at 3). Quiz: T against R, R against B, T worth 3.4 (B 2.2), two best replies to L.
- l2: desks (Tight, Tight) £2,000 against £4,000; 3 × 3 deletion C, then M and B, then R, ending (T, L) = (4, 3) in 3 rounds; mix of U and M pays 1.5 each way; weak deletion ends (2, 1) or (1, 1), four pure equilibria; pennies has nothing dominated; drill (B, R), Ana 6, 3 rounds; half L, half C pays Ben 2; three desks: Tight £3,000 ahead in every case, £3,000 each against £4,000. Quiz: R dominated by the mix; (T, L), Ben 1; fees end at (1, 1).
- l3: (D, C) only; from it Ana's best switch 2, Ben's 2 or 1; venues two; race (A, P) and (P, A); desks (Tight, Tight); pennies none; drill 0, 1, 2 and 2; spread equilibria (1, 1) and (2, 2), (3, 3) fails at £200 against £150. Quiz: 0 equilibria in the 2 × 3.
- l4: pennies q = 1/2, value 0; venues p = 3/5, q = 2/5, each £1.20; raised prize q = 1/4, Ana 1.5, Ana's p still 3/5; edge q = −1/2; drill race 1/3 and £2, venues 1/4 and £0.75, new game Ben's L 3/4 (Ana 1/2, each 1.5); rock beating scissors at £2: rock 1/4, paper 1/2, scissors 1/4, value 0. Quiz: p = 1/4 (q = 3/4, Ana 7/4); scissors beating paper at £3: rock 3/5, paper 1/5, scissors 1/5.
- l5: row minima 2, 3, 0, column maxima 6, 3, 7, saddle £300; penalty p = 5/13 = 0.3846, keeper 6/13 = 0.4615, 199/260 = 0.7654 (cell average 0.7625, half and half 0.725); 2 × 3 value 2.5 at p = 1/2, Ben 1/4 and 3/4 (columns 1 and 2 cross at 8/3, 1 and 3 at 2.4); unequal pennies 3/8, value −1/8; edge p = 3, saddle 2; Morra 9/16 and −1/16; (5, 1), (2, 4) gives 1/3 and 3; (4, 6), (3, 2) saddle 4; Ben's 100 rounds £12.50. Quiz: (6, 2), (3, 4) value 3.6 at p = 1/5; (2, 4), (1, 3) saddle 2; a mix pays the value against either column.
- Review: Ben's best replies r1c1, r2c2, r3c3 and no equilibrium; deletion R, T, L, B to (M, C), 7; counts 1 at (T, L) and 2 at (T, C), (B, L); mix of U and M pays 2.5; Ana's p = 2/5 (Ben 1/3); saddle 5 (the formula would give −1); 2 × 3 value 2.4 at p = 2/5, Ben 1/5 and 4/5 (best pure guarantee 1).
- Homework: deletion M, then L and C, then B to (T, R), 3; Ben's L 2/5 (Ana 3/4, Ana expects 8/5); 2 × 3 value 8/3 at p = 2/3, Ben 1/6 and 5/6 (best pure guarantee 1); longform p = q = 3/10, value +£0.10, cell average +£0.50.
- Code items, run locally on the solution and starter: `pure_nash` solution 7 of 7, starter (returns `[]`) 2 of 7, so it fails five; `solve_zero_sum_2x2` solution 7 of 7, starter (formula only) 5 of 7, failing the two saddle games. Tests compare `[tuple(c) for c in ...]` and `tuple(...)` with `equal`, so a list of lists or a list result also passes.

## Correction to the brief

The brief's longform model answer ends "against a Ben who shows heads too often, show tails more". With Ben's heads chance q, Ana's heads pays 7q − 2 and her tails 1 − 3q, so above q = 3/10 heads pays more. The model answer says the opposite of the brief: lean to heads against too much heads (matching pays £5), to tails against too much tails.

## Departures from the brief, and why

- One widget per screen: l2's three-desk follow-up uses two screens (choice, then numeric); l3's "why does (3, 3) fail" choice and l4's rock, paper, scissors choice moved to the quiz (l4's quiz uses a new variant, scissors beating paper at £3, so the transfer is not repeated). l2's drill asks "what does half L, half C pay Ben in row T" (2) as a number; the brief's `choice` on that game is quiz item 1.
- l1's story screen fills the four pairs as text cells (`1, 1`, with `1,1`, `(1, 1)` and `(1,1)` accepted) bound to the grid, so the table appears on the canvas as the learner types.
- l5's hook taps the row minima on the table canvas (an interaction before any rule); the table widget of minima, maxima and the value follows on screen 2.
- l4 and l5 drills list their 2 × 2 games as rows of a `table` canvas, since a `frames` control cannot change a grid's move names (backlog bullet).

## Conventions

No randomness and no seeds: every number is exact. Payoffs in £ unless a story says £1,000 a day, £m a year or £100s. Grid cells use the Unicode minus. Generators and checks: `<scratchpad>/game-theory-1/gen_l1.py` to `gen_l5.py`, `gen_review.py`, `gen_homework.py` (which also runs the code harness), `common.py`, `checks.py`, `checks_new.py`.

## Proposed course.json change

None.

## Backlog

Six bullets under "Raised later (game-theory level 1):" in `docs/BACKLOG-INBOX.md`.

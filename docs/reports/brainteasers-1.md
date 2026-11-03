# Report: brainteasers level 1 (Invariants and counting arguments)

Author: content agent, 3 November 2026. Brief: `docs/briefs/brainteasers.md`, course context and `## Level 1`. Standards: full LEVEL-BRIEF acceptance (DECISIONS "Standards restored").

## Files written

All in `app/content/courses/brainteasers/`. Generators and checks in the scratchpad folder `brainteasers-1/` (`gen_l1.py` to `gen_l5.py`, `gen_sets.py`, `lib.py`, `check_l1.py` to `check_l5.py`, `check_l2b.py`).

| File | Screens or items | Quiz | Skills | Notes |
|---|---|---|---|---|
| `l1-what-stays-the-same.json` | 12 screens (problem, problem, ladder, ladder, derive, trap, problem, generalise, 3 drills, transfer) | 4 | bz-invariant | hook: `manipulate` over all 9 lizard states on a `bars` canvas |
| `l2-colouring-boards.json` | 12 (problem, 3 ladders, trap, problem, generalise, derive, 3 drills, transfer) | 3 | bz-invariant | hook: `tap-regions` on a blank 5 × 5 `grid` |
| `l3-pigeonhole.json` | 12 (problem, problem, problem, derive, trap, generalise, 4 drills, 2 transfers) | 3 | bz-invariant | hook: `place` in boxes mode (`count: { hand: 4 }`) on a sock drawer |
| `l4-weighing-coins.json` | 12 (3 problems, ladder, trap, problem, generalise, derive, 3 drills, transfer) | 3 | bz-search | hook: `manipulate` with worst-case states on a `boxes` canvas; `balance` canvases with labelled coins |
| `l5-ropes-and-jugs.json` | 12 (problem, ladder, problem, derive, trap, problem, generalise, 3 drills, 2 transfers) | 3 | bz-search | hook: `manipulate` over every jug state, ticks on a 9 × 6 `grid` lattice |
| `review-1.json` | 9 items, difficulty 2 to 4, interleaved l1, l2, l3, l4, l5, l1, l2, l3, l4 | | both | every item has `skills`, `tags`, `pace` |
| `homework-1.json` | 8 items, difficulty 3 to 5 (three at 5) | | both | `order` derivations (h1, h5), `longform` h8 with a 10-point rubric and model answer |

No lesson has a non-task screen (every generalise screen carries a confirmation widget). Each lesson has a real interactive canvas on screen 1, one `trap` with `byKey` lines, one edge case, a drill block with tags, and a follow-up `transfer`.

Tags (kebab-case families from the brief) are on every drill screen, every quiz item, every review item and every homework item. **`pace`:** the validator accepted an optional `pace` field (0 errors; it does not inspect it yet), so every tagged screen and item carries `"pace": 180`; the drill prose also states the pace ("about three minutes each, as an interview allows; say the argument aloud before you answer").

## Validator

`node tools/validate.mjs` from `app/`: **0 errors** (393 warnings, none on a brainteasers lesson, review or homework file; the only brainteasers warning is course.json's "not yet written: 11 of 16 lessons", levels 2 and 3). During the session the validator briefly showed errors in other agents' files (`mm-games/l8-informed-flow.json`, `mental-pressure/l15-probability-at-speed.json`); they cleared on later runs and were not touched.

Voice: `VOICE_BASE=/home/user/zero-to-quant/app/content/courses/brainteasers/ python3 docs/reviews/voice-scan.py` reports **0 sentences over 20 words and 0 explanations over three sentences** (3,154 sentences scanned). The relative form in the orchestrator prompt (`VOICE_BASE=app/content/courses/brainteasers`) scans 0 sentences, because the script globs `BASE + '*.json'` without a slash; the absolute path with a trailing slash was used (backlog bullet).

## Playthrough

All with `--local-cdn <scratchpad>/pkgs`.

| Run | Result |
|---|---|
| `--lesson` l1 to l5 (desktop) | all ok: 16, 15, 15, 15, 15 checks; quizzes 4/4, 3/3, 3/3, 3/3, 3/3 |
| `--lesson` l1 to l5 `--mobile` (with `--shots`) | all ok |
| `--set brainteasers/review-1` | ok, recorded 9 of 9 |
| `--set brainteasers/homework-1` | ok, marked 8 of 8, 39 of 39 marks |

Screenshots (desktop, 390 px, and `--why` for each lesson) were inspected. Fixes made from them: the knight route in l2 drew as one straight line, so the landing squares are now numbered; the sock drawer was tiny at 390 px (now `size: "medium"`, `rows: 2`, 7 columns); handshake counts sat on an edge (now `valueSide` outward); rope interval labels on rows 1 and 2 collided (now `labelPos` below and above, B's two stages on one row); the jug lattices pushed the step chips off a phone screen (now `canvas.maxHeight: 300`); multi-selects over short numbers now use `layout: "grid"`.

## Numbers and their sources

Every number was computed by hand (or from the brief's hand working) and again by exhaustive search or exact count in the scratchpad scripts.

| Number | Where | Second computation |
|---|---|---|
| 9 lizard states from (1, 2, 3); (4, 2, 0) in 3 meetings via (0, 4, 2), (2, 3, 1); one colour unreachable | l1 s1, s2 | BFS, `check_l1.py` (also finds (1, 5, 0) at 3, so the target was set to 4, 2, 0) |
| 9 coins, turn 4: heads stay odd; reachable 1, 3, 5, 7, 9 | l1 s3 | BFS |
| $a + b + ab$ on 1 to 6 ends at $7! - 1 = 5039$; orders A and B line by line | l1 s4, s5 | 300 random orders; both tables recomputed in `gen_l1.py` with an assert |
| 3 × 3 lamps: 32 of 512 reachable, lit counts 0, 3, 4, 5, 6, 9; row 1 + columns 2, 3 leaves 5 on; row + column leaves 4 | l1 s6, quiz | enumeration of all row and column masks |
| 10 coins, turn 4: 3 moves (10, 6, 4, 0) | l1 s7 | BFS |
| 1 to 20 with $a + b - 1$: 191 | l1 drill | random orders |
| (2, 5, 8): all three colours reachable, all blue in 5; (4, 6, 8) and (3, 4, 8) never | l1 drill, hw1 | BFS |
| Reversing 6 by neighbour swaps: 15 | l1 drill | BFS over permutations |
| 11 coins turn 2, 15 coins turn 6: never all tails | l1 quiz, r1 | BFS |
| $a + b + 2ab$ on 1 to 4: 472 | l1 transfer | random orders and $(3 \cdot 5 \cdot 7 \cdot 9 - 1)/2$ |
| 1 to 10 with $a + b + 1$: 64 | l1 quiz | $55 + 9$ and the same sum argument |
| 5 × 5 minus one square: the 13 squares with $i + j$ even | l2 s1 | exact-cover tiling search of all 25 |
| Knight corner to corner: 6 moves; route r1c1, r2c3, r3c5, r4c7, r6c8, r7c6, r8c8 | l2 s2, s3 | BFS |
| 5 × 5 tours from r1c1: 824, ending on exactly the 12 other dark squares | l2 s4 | DFS of all Hamiltonian paths |
| 6 × 6, $(i + j) \bmod 4$ from the corner: 9, 10, 9, 8; no 1 × 4 tiling | l2 trap, derive | count and tiling search |
| 1 × 6 strip: removing 2 and 5 fails, 1 and 4 tiles | l2 edge | tiling search |
| Nine T pieces on 6 × 6: no; four on 4 × 4: yes; seven on 4 × 7: no | l2 drill, r4 | tiling search |
| 4 × 4 has a closed tour (shown), 5 × 5 not | l2 drill | DFS |
| 7 × 7 minus r1c2: no (25 dark, 23 light); minus r1c1, r1c3, centre: yes | l2 drill, r3 | tiling search |
| 3 × 3 × 3 cube from a corner: 392,628 paths, 13 end cubes, centre not one; 14 even cubes; no path starts at the centre | l2 transfer, quiz | DFS |
| Socks 7, 9, 4: pair 4, two blue 13, two of each 18 | l3 s1, trap, drill | exhaustive over all draws |
| Three of one colour from four colours: 9; $k(r - 1) + 1$ checked at (4, 3), (3, 2), (5, 4) | l3 transfers | exhaustive draws |
| Sum 13 from 1 to 12: 7; 1 to 6 shows 6 fails | l3 s2, quiz | all subsets |
| Six guests always share a handshake count | l3 s3, s4 | all $2^{15}$ graphs |
| Ten points in 3 × 3 within $\sqrt{2} \approx 1.414$; nine points 1.5 apart (min distance 1.5) | l3 drill | direct computation |
| $\lceil 40/13 \rceil = 4$; $\lceil 100/4 \rceil = 25$; months 13 | l3 drill, quiz | arithmetic |
| Sum or difference divisible by 10: 7; 0 to 5 fails | l3 drill | all residue subsets |
| Gloves: 11; consecutive from 1 to 100: 51; not-grey pair (5, 3, 8): 11 | r5, r6, hw7 | exhaustive draws; path DP for 51 |
| Heavy coin: 9 in 2, 27 in 3, 81 in 4, 243 in 5 (244 not); 50 need 4; 10 need 3; 100 need 5 | l4 | adaptive strategy search `heavy(n, k)` |
| Heavy or light: 12 in 3 yes, 13 no, 13 + genuine yes, 14 + genuine no; 39 in 4 yes, 40 no, 40 + genuine yes; 2 coins never | l4, hw4 | strategy search over (unknown, heavy-only, light-only, genuine) states |
| After 1–4 against 5–8 tips: 8 cases; {1, 2, 5} against {3, 6, 9} leaves 3, 2, 3 | l4 s3, s4 | case simulation |
| 13 coins: tilt needs $a \le 4$, level $a \ge 5$ | l4 derive | hand bound, agrees with the search |
| Bags: 36 coins, 180 g, 185 g reads bag 5; 55 coins, 550 g, 542 g reads bag 8 | l4 drill, r8 | arithmetic twice |
| Jugs: (5, 8) → 2 in 4; (4, 9) → 6 in 8 (route as brief); (3, 7) → 5 in 8; (5, 11) → 3 in 12; (6, 9) never 4; (6, 15) make 0, 3, 6, 9, 12, 15; (4, 6) never 3 | l5, quiz, hw6 | BFS over jug states |
| (10, 7, 3) without a tap: 9 pours, route as brief | l5 transfers | BFS, and an assert in `gen_l5.py` that each step is a legal pour |
| Ropes of 80: marks 40, 60, 80, 120, 160 only; of 120: 60, 90, 120, 180, 240; of 60: shortest 30 | l5, hw5, quiz | event-driven search over every lighting plan (exact fractions) |
| Hourglasses (5, 9) → 13, (4, 7) → 9, (6, 11) → 16 | l5 drills, r9 | event search over turn plans |
| 7 × 7 minus one, 16 straight trominoes: exactly r1c1, r1c4, r1c7, r4c1, r4c4, r4c7, r7c1, r7c4, r7c7; classes 17, 16, 16 under both mod 3 colourings | hw2 | tiling search and class count |
| Triangle of side 2: 5 points; centre $2/\sqrt{3} \approx 1.155$ from each corner | hw3 | direct computation |
| 10 × 10, $(i + j) \bmod 4$ from the corner: 25, 26, 25, 24 | hw8 | count |
| 4 × 4 lamps: 128 reachable, lit counts 0, 4, 6, 8, 10, 12, 16 ($4r + 4c - 2rc$) | r2 | enumeration |

## Departures from the brief

- **Twelve-screen cap.** The brainteasers shape (hook, three worked teasers, derive, trap, edge, generalise, three to five drills, a follow-up) exceeds 12 screens, so some brief items moved into each lesson's quiz: l1's lamp-count `multi`, the eleven-coins drill and the transfer's invariant `choice`; l5's jugs 3 and 7 drill (8 steps). l4's "8 cases after the first tip" became the first step of worked teaser 3 instead of a drill. l3's tight bound {1, ..., 6} is the wrong-answer canvas on screen 2 and a quiz item.
- **l1 hook target.** Two states have no blue lizard, (4, 2, 0) and (1, 5, 0), both 3 meetings away; `manipulate` takes one target, so the question asks for 4 red, 2 green, 0 blue. In l5 the two states with 2 litres in the small jug, (2, 8) and (2, 0), are merged into one `goal` node.
- **l3 hook.** "How many to be sure of a pair" is graded as `place` in boxes mode with `count: { hand: 4 }` (the learner leaves the forcing number of socks in the hand), not as a separate `numeric` screen.
- **l5 transfer.** The no-tap split is two transfer screens: a `manipulate` try on a `bars` canvas, then the `numeric` 9.
- **Review item r7.** The brief's "50 coins, one heavier: 4" repeats l4's drill word for word, so the review asks 100 coins (5 weighings) to keep every review puzzle unseen.
- **Homework h5** has two distractors (cut into quarters; a third rope) rather than one.
- The table `byKey` lines in l1 s4 and the l2 trap key on cell ids (`r4c1` is the yes/no cell) because the validator refuses a cell's own `wrong[]` id (backlog).

## Conventions

No datasets or seeds. Colour series: red = slot 2, green = slot 3, blue = slot 1 (lizards); grid ids one-based, table ids zero-based. Coins on `balance` are unknowns labelled 1 to 12 with hidden values 10 (genuine), 11 (heavy) and `k: 6`. Books named once, in l1's generalise screen, in the curriculum's order. No firm names. Prior lessons cited by id: contests l8-invariants (l1 edge, l1 transfer, l2 generalise), proof l9-one-to-one-onto and counting-chance l10-birthday (l3 generalise, l3 transfer).

## Proposed course.json change

None.

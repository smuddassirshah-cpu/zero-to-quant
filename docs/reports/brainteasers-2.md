# Report: brainteasers level 2 (Strategy and logic)

Author: content agent, 3 November 2026. Brief: `docs/briefs/brainteasers.md`, course context and `## Level 2`. Standards: `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`.

## Files written

All in `app/content/courses/brainteasers/`. Generators and checks are in the scratchpad folder `brainteasers-2/`: `lib.py` (helpers), `gen_l6.py` to `gen_l11.py`, `gen_sets.py`, `check_all.py` (every number by search or exact count), `check_muddy.py` (a possible-worlds model of the muddy-children game), `solvers.py` (bridge shortest path, $f(d, e)$), `hatlib.py` (line-of-hats calls), `codecheck.py` (homework code: solution against the DP, starter against the tests), `fixvoice.py`. The generators assert their numbers before writing.

| File | Screens or items | Quiz | Skills | Notes |
|---|---|---|---|---|
| `l6-back-from-the-end.json` | 12 (problem, ladder, problem, trap, problem, generalise, derive, 4 drills, transfer) | 4 | bz-strategy | hook: `table` fill of the 3- and 4-aboard splits under a `tree` of failed proposals; lions on a 7-node `tree` |
| `l7-hat-strategies.json` | 12 (problem, ladder, ladder, problem, trap, problem, generalise, 4 drills, transfer) | 3 | bz-strategy, bz-invariant | hook: 1 × 8 `grid` of hats with a `frames` control ("Whose view", dims what each person cannot see) and a `table` of calls |
| `l8-prisoners-and-boxes.json` | 12 (problem, problem, ladder, trap, derive, problem, problem, generalise, 3 drills, transfer) | 3 | bz-strategy | hook: `graph` ring of 4 boxes with directed edges, `tap-regions` `ordered: true` along prisoner 1's cycle |
| `l9-egg-drop.json` | 12 (explore, problem, ladder, trap, problem, derive, problem, generalise, 3 drills, transfer) | 3 | bz-search | hook: `number-line` with a draggable first drop and a `derive` caption giving both cases and the worst case; $f(d, e)$ filled on a 3 × 9 `grid` with `deps` and `bind` |
| `l10-what-they-know.json` | 12 (problem, ladder, problem, problem, trap, problem, generalise, derive, 3 drills, transfer) | 3 | bz-strategy | hook: 1 × 3 `grid` of children with a `frames` control for 1, 2 or 3 muddy, and a `table` of rounds |
| `l11-crossings-and-schedules.json` | 12 (problem, problem, problem, trap, derive, problem, generalise, 4 drills, transfer) | 3 | bz-search | hook: generated `manipulate` (46 states) on a `boxes` canvas of the two banks |
| `review-2.json` | 10 items, difficulty 2 to 4, order l6, l7, l8, l9, l10, l11, l6, l7, l8, l10 | | all three level skills | every item has `skills`, `tags`, `pace` |
| `homework-2.json` | 8 items, difficulty 3 to 5 (two at 5) | | all three | `order` derivations hw1 and hw4 (with distractors), `code` hw2 (Python, standard library), `longform` hw8 with a 10-point rubric and model answer |

No lesson has a non-task screen: every generalise screen carries a confirmation widget. Each lesson has an interactive canvas or widget on screen 1, one `trap` with `byKey` lines, one edge case (merciful pirates, a line of one, one prisoner's own chance, one egg, a single islander, two walkers), a drill block of three or four tagged screens, and a follow-up `transfer`. Tags are on every drill screen, quiz item, review item and homework item, with `"pace": 180`; the drill prose states the pace ("about three minutes each, as an interview allows; say the argument aloud before you answer"). Every `choice` and `multi` has `shuffle: true`.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, no warning on any level 2 file (391 warnings in all, other courses). Brainteasers warnings left are course.json's unwritten count and level 3's own.

Voice: `VOICE_BASE=/home/user/zero-to-quant/app/content/courses/brainteasers/ python3 docs/reviews/voice-scan.py` reports **0 sentences over 20 words and 0 explanations over three sentences** (9,287 sentences scanned, the whole course). No em-dashes, no exclamation marks (the `!` in the files are factorials inside KaTeX), no firm names.

## Playthrough

All with `--local-cdn <scratchpad>/pkgs`.

| Run | Result |
|---|---|
| `--lesson` l6 to l11, with `--shots --mobile --why` | all ok: 16, 15, 15, 15, 15, 15 checks; quizzes 4/4, 3/3, 3/3, 3/3, 3/3, 3/3 |
| `--lesson` l6 to l11, plain | all ok (final run after the last edits) |
| `--set brainteasers/review-2` | ok, recorded 10 of 10 |
| `--set brainteasers/homework-2` | ok, marked 8 of 8, 37 of 37 marks (the code item runs in Pyodide) |

Screenshots (desktop, 390 px, and every Why? sheet) were inspected. Fixes made from them:
- The seven-lions chain drawn top to bottom was 700 px tall; it now runs left to right.
- The $f(d, e)$ grid as 9 rows × 3 columns with `maxHeight` shrank its text to unreadable; it is now 3 rows (eggs) × 9 columns (drops), full size.
- The bridge `manipulate` overflowed at 390 px: the state line and the second chip of each row ran off the card. The state line is now "Over: 1, 3   3 min" and the chips read "1, 3 cross (3 min)" and "1 returns (1 min)"; the boxes canvas is `size: "medium"`.
- A self-loop in the 4-box ring hid the "holds 3" value; loop nodes now put their value above. The 8-box Why? sheet clears the "holds" values once the arrows are drawn.
- The homework starter's comment line scrolled at 390 px; shortened.

## Numbers and their sources

Every number was worked by hand (or from the brief's working) and again by search or exact count in the scratchpad scripts.

| Number | Where | Second computation |
|---|---|---|
| 60 coins: 2 aboard (60, 0); 3 aboard (59, 0, 1); 4 aboard (59, 0, 1, 0); 5 (58, 0, 1, 0, 1); 6 (58, 0, 1, 0, 1, 0); 7 keeps 57; formula $60 - \lfloor (n-1)/2 \rfloor$ for $n$ = 2 to 10 | l6 hook, ladder, trap, derive, drills, quiz | backward-induction solver over every set of bought votes, all optimal splits listed (each unique) |
| 3 aboard, 40 coins: 39; 4 aboard, 100 coins: (99, 0, 1, 0) | l6 drill, r1, hw1 | solver |
| Merciful: proposer keeps 60 for 2 to 5 aboard; (60, 0, 0) and (60, 0, 0, 0, 0) | l6 edge, quiz, hw6 | solver with the mercy tie rule |
| More than half: 2 aboard proposer overboard; (60, 0, 0); (58, 0, 1, 1), unique; 5 aboard ties | l6 transfer | solver with strict majority |
| Lions eat exactly when the count is odd: 7 eat, 4, 10, 12 do not | l6, quiz, r7 | recursion |
| Line R, B, B, R, R, B, R, R: back sees 4 reds, says B; calls R, B, B, R, R, B, R, B from the front; 7 right | l7 hook, ladder, trap | simulation of the code |
| Person 4 knows 1 red in front and 2 red calls behind | l7 ladder | by hand and the simulation |
| Three colours, hats 0, 2, 1, 2, 1: calls 2, 2, 1 | l7 ladder | simulation modulo 3 |
| Lines of 6, 8, 10, 12, 20 guarantee $n - 1$, two or three colours; a line of one: 1/2 | l7 drills, edge, r2 | 3,000 random lines per case, worst case |
| Seven at once, hats 3, 5, 0, 6, 2, 2, 4: total 22, person 4 guesses 5, person 1 right; exactly one right in all $7^7 = 823{,}543$ patterns | l7 | exhaustive |
| Total 30: person 2; five people, person 3 sees 1, 4, 0, 2: guess 1 | l7 quiz, hw3 | arithmetic modulo 7 and 5 |
| Six-person lines: B, R, R, B, R, B gives R, R, B, R, R, B from the back; R, R, B, B, B, R gives B, B, B, B, R, R | l7 drill, r8 | simulation |
| Pass game, 3 players: 3/4 is the best of all $81^3$ strategies; Hamming, 7 players: 7/8 (16 codewords of 128) | l7 drill, transfer | exhaustive search; all 128 patterns |
| 4 prisoners, 2 boxes: cycle types 1, 6, 3, 8, 6; 10/24 = 5/12 = 0.4167; random 1/16 | l8 | all 24 orders |
| 6 open 3: 23/60 = 0.3833; 8 open 4: 307/840 = 0.3655; 10 open 5: 893/2520 = 0.3544; 12 open 6: 9613/27720 = 0.3468 | l8, quiz, r3 | all 720 and 40,320 orders; a cycle-count DP for 10 and 12; the harmonic formula |
| 100 open 50: 0.3118; $1 - \ln 2 = 0.3069$; long cycle 0.6882; 100 open 60: 0.4925; $H_{100} = 5.1874$, $H_{50} = 4.4992$, $H_{60} = 4.6799$ | l8 | exact fractions |
| One prisoner's own chance: 1/2 | l8 edge, r9 | all 40,320 orders of 8 |
| Boxes 1→3, 2→5, 3→7, 4→4, 5→8, 6→2, 7→1, 8→6: cycles 3, 4, 1 | l8 drill | cycle finder |
| Eggs: (1, 10) 10; (2, 10) 4 with drops 4, 7, 9, 10 (forced); (2, 100) 14 with drops 14, 27, ..., 100; first drop 9 to 14 all work; (3, 100) 9; (1, 100) 100; (2, 50) 10; (2, 36) 8, first drop 8 only; (2, 200) 20; (2, 21) 6; (2, 80) 13; (2, 300) 24 | l9, quiz, r4, hw5 | full minimax DP and the $f(d, e)$ count |
| Every 10 floors: worst 19; binary search: worst 50 | l9 trap | simulation of both plans |
| $f(8, 3) = 92$, $f(9, 2) = 45$, $f(9, 3) = 129$, $f(5, 4) = 30$, $f(14, 2) = 105$, $f(44, 2) = 990$, $f(45, 2) = 1035$, $f(18, 3) = 987$, $f(19, 3) = 1159$; 1,000 floors: 45 and 19 | l9, hw2 | sum of binomials and the recurrence |
| Muddy children: $k$ muddy act in round $k$ (3, 5 of 9, 4 of 6, 8); "at least two": $k - 1$; "at least three", 4 of 6: round 2; round $= k - m + 1$ for $m$ = 1 to 4; no announcement: never | l10, quiz, r5 | possible-worlds model, every case |
| Islanders: night 7, 100, 1; sees five, night 6 | l10 | the same model (7 islanders, every $k$) and induction for 100 |
| Bridge: (1, 3, 6, 8) 18, escort 19; (1, 4, 5, 6) 17, shuttle 19; (1, 3, 4, 9) 18 escort; (2, 3, 8, 9) 20; (1, 5, 6, 7) 20; (1, 2, 7, 8) 15; (1, 2, 4, 9) 16; (3, 8) 8; (1, 3, 6, 8, 12) 29; (1, 2, 5, 8, 10) 23 | l11, quiz, r6, hw7 | Dijkstra over every crossing of one or two people |
| Auditors and traders: 11 crossings, with an auditor and a trader returning together at crossing 6 | l11 drill | BFS over safe states, route printed |
| Burgers: 3 on a grill for 2 at 4 min a side, 12; 5 on 2 at 3 min, 15; 4 on 3 at 5 min, 15 | l11, quiz | sides over places, schedules written out |
| Bridge hook: 46 states with pairs over and singles back up to 18 minutes; only one finishing state, at 18 | l11 hook | generator BFS with assert |
| hw2 code: solution passes all 8 tests and 3 extra cases, agreeing with the DP up to 200 floors; the halving starter passes 5 of 11 cases and fails the hidden set | hw2 | `codecheck.py` |

## Departures from the brief

- **Twelve-screen cap.** As in level 1, some brief items moved to the quiz: l8's "10 prisoners opening 5" and the "60 of 100" follow-up (the transfer screen keeps the swap); l9's "two eggs and 200 floors"; l10's "4 muddy among 6 with at least three". l11's "fifth person" transfer and five burgers stayed; the "1, 4, 5, 6" teaser is a `problem`, not a ladder.
- **l6 hook.** The worked teasers 2, 3 and 4 aboard are all in the hook's table, then the ladder asks whose vote A buys. Pirates are named A to D so the smaller crews keep their names (C and D with 2 aboard).
- **l6 derive.** A `choice` of the closed form $60 - \lfloor (n-1)/2 \rfloor$, checked against the solver for 2 to 10 aboard.
- **l8 derive and hw4.** The lesson orders the count $\binom{n}{k}(k-1)!(n-k)! = n!/k$, as the brief says. The homework orders the whole success argument (fail event, uniqueness, count, disjoint sum) with two distractors, so the two items do not repeat.
- **l11 proof.** The brief's case 2 says the return after 6 and 8 cross "is by someone other than the fastest". That fails when 3 returns first and 1 second. The proof line now says the two returns are made by 1 and 3, costing $1 + 3$ in either order. The step "more trips cost more" is stated as checked by search, in the prose.
- **l11 hook.** The ops are pairs going over and single people coming back (the prose says so), so the graph has 46 states; any crossing past 18 minutes is a `reject` op with its total. Allowing every one- or two-person trip both ways gave 158 states and over 600 ops.
- **l11 generalise.** Confirms the rule on a new set, 1, 3, 4 and 9 (escort 18, shuttle 19).
- **l10 trap.** The choice joins the night and the reason ("Night 7: the sentence became common knowledge"), so both candidate errors are distractors.
- **Review.** All ten brief items, in the order above; r6 asks the 1, 2, 4, 9 bridge (16).

## Conventions

No datasets or seeds. Colours: red hats slot 2, blue hats and blue eyes slot 1, mud slot 4, the torch card slot 4. Grid ids one-based, table ids zero-based (table `byKey` lines key on cell ids such as `r1c2`). Books named once, in l6's generalise screen, in the curriculum's order. Later lessons cited by id: puzzles l19-who-wins and game-theory l6-game-trees (l6 generalise). No firm names; desk uses are a committee vote (l6), data codes between trading systems (l7), a release manager bisecting builds (l9), an expected rate cut (l10) and trade allocation (l11).

## Proposed course.json change

None.

# Report: puzzles level 5 (Puzzles firms keep asking)

Author: content agent, 3 November 2026. Brief: `docs/briefs/puzzles.md` section "Level 5" and the course context, with the orchestrator's session rules (`tags` and `pace` on drill, quiz, review and homework items; no firm names; `longform` only in homework; `shuffle: true` on choices; no 4-column tables). Generators and checks live in the scratchpad folder `puzzles-5`: `zq.py` (builders; titles and objectives are read from `course.json`; a `£` inside `$...$` is written as `\text{£}`), `gen_l25.py` to `gen_l30.py`, `gen_sets.py`, `check_numbers.py`, `check2.py`, `check3.py`, `check4.py`, `explore_truel.py`, `fix_voice.py`, `play.sh`, and the screenshots in `shots/`.

## Files written

All in `app/content/courses/puzzles/`. Ids, titles, objectives and skills follow `course.json` and the brief: `pz-expectation` and `pz-symmetry` on l25, `pz-conditioning` and `pz-expectation` on l26, `pz-conditioning` on l27, `pz-recursion` and `pz-games` on l28, `pz-geometry` and `pz-symmetry` on l29, all six skills on l30.

| File | Screens | Quiz / items | Shape and canvases |
|---|---|---|---|
| `l25-fair-from-biased.json` | 12 | 3 | title (the four books in order and *Probability and Markets* as "a free guide from a trading firm"); tap the two equal outcomes on a `tree` of one round at p = 2/3; expected flips 4.5 (von Neumann's trick named); `plane` drag along 1/(pq), p = 0.6 gives 25/6; die from a fair coin on a 2 × 4 `grid` (4 flips); trap "call HH heads" (4/9); generalise with the edge case p = 0 or 1; `order` derivation (independence, not fairness, as the distractor); `code` `von_neumann` and `expected_flips`; drill table (100/9, 0.42, 8/3); follow-up three people at 0.6 (125/12); transfer tick feed at 0.8 (6.25 ticks) |
| `l26-estimating-n.json` | 10 | 3 | `number-line` drag N until one cab averages 60 (119); four serials with the gaps drawn (74); `bars` of the larger of two from 1 to 20, drag the balance point to 14; trap (60, 74, 79.5 or 119: 74, with the variance remark linking estimation l3); generalise with the edge case k = N; `order` gap derivation of E[m] (63/4 check in the explanation); `code` `tank_estimate` and `tank_sim`; drill table (119, 15.75, 1.2); follow-up unknown start by the range (202/3); transfer order ids (973.4) |
| `l27-given-the-total.json` | 12 | 3 | 6 × 6 `grid` throughout: tap the rolls totalling 8 (reduced sample space named); both even 3/5; expected larger given 10 (17/3); tap the L of larger die 5; trap "the other die is still fair" (1/9, not 1/6); generalise with the edge case total 12; `order` derivation of E[total given max 5] = 70/9; `code` `conditional` and `cond_mean`; drill table (2/5, 36/11, 1/2); drill choice (a six given total 7: 1/3); follow-up n-sided dice with total n + 1 (5, 8, 75.5: (3n + 2)/4 for even n); transfer two-day P&L grid (0.5) |
| `l28-duels.json` | 12 | 3 | duel `tree` (1/2; first-step analysis named); `plane` with a slider on B's accuracy to the even point q = 1/3; truel after A misses on a `graph` (`markov: true`), 25/63; A aims at C on a `tree`, 59/189; trap "shoot the best shooter" (air wins: 75/189, 59/189, 50/189); generalise with the edge case p = 1 firing first; `order` derivation of the duel formula (p/(p + q) as the distractor); `code` `duel` and `truel_air` (one case with p_C = 0.9, so the round can repeat); drill table (4/7, 2/3, 3/7); drill choice who survives (A, 25/63); follow-up A at 1/2 (17/30 against 23/60); transfer a price war |
| `l29-random-chords.json` | 12 | 3 | `plane` disc, one procedure a screen: drag the second endpoint (1/3), drag the point on a radius (1/2), drag the midpoint (1/4; Bertrand's paradox named); trap "just give a number"; two envelopes on a `table` canvas, tap the cases where you see £20 (switching worth £25), then keep and switch both £22.50; generalise (the procedure decides; link to conditional l18's host rule) with the edge case "see £80: keep"; `order` derivation of 1/4; `code` `chord_sim`; drill table of expected lengths (4/π, π/2, 4/3); follow-up threshold √2 (1/2, 0.7071, 1/2); transfer "a random day" in a backtest (£40 against −£230) |
| `l30-follow-ups.json` | 12 | 3 | tap the L of larger face 4 on a `grid` (2m − 1); `plane` of (n + 1)(4n − 1)/(6n) with a table (161/36 check, 13.825); reroll game with a cost on a `bars` chart of threshold rules with a cost slider (£4.50, £3.60, £3.50; the option is worthless from £2.50); more players on a `graph` (6/11 check, 36/91); trap (a formula 2n/3 + 1/3 that passes n = 1 and fails n = 6); generalise with the edge case n = 1; `order` derivation of the max formula (2n/3 as the distractor); `code` `max_of_two` and `reroll_value`; drill tables tagged with the level 1 families (7.15 and 37.2385; 4/7 and 57/8); follow-up the threshold rule (choice); transfer a market on the larger of two 100-sided dice (£67.165) |
| `review-5.json` | | 10 items (3, 2, 4, 2, 3, 2, 3, 3, 3, 4) | every lesson twice; `timed: { "seconds": 1440 }` as a guide clock (no lock) |
| `homework-5.json` | | 10 items (5, 4, 4, 4, 5, 4, 3, 4, 4, 4) | `code` `truel(pa, pb, pc)` with best play (5); `code` `tank_estimates` (4); `order` gap derivation of E[R] = (k − 1)(N + 1)/(k + 1); `longform` spoken answer, about 5 minutes: a fair decision with a biased coin, then three people (10-point rubric, full model); weak-B truel, A's best move is to aim at C (5); two-bit method for three people (100/9); sum given max 6 (102/11); three dice total 10 (1/3); "switch unless £80" (125/3); d20 reroll at £1 (91/6) |

Interview form. Every drill and follow-up screen and every quiz, review and homework item carries `tags` (the family first: `fair-from-biased`, `estimating-n`, `given-the-total`, `duels`, `random-chords`, `follow-ups`; l30 adds the level 1 or 4 family it extends, `dice-games`, `every-coupon`, `waiting-for-hh` or `who-wins`; the spoken item adds `spoken`) and `pace` in seconds. Drill prose states about 3 minutes a puzzle, kept by the learner, with the argument said aloud. Each lesson has one "Follow-up: ..." screen with the brief's extension. No firm names: "trading firms" and "banks" only. Each lesson has a real interactive canvas on its first or second screen (tap, drag, slider). Edge cases: l25 p = 0 or 1 (generalise, quiz), l26 k = N (generalise), l27 total 12 (generalise), l28 a perfect shot firing first (generalise), l29 the largest amount in the prior (generalise), l30 n = 1 (generalise) and a cost of £2.50 or more (screen 3).

Departures from the brief, all small: the l25 drill choice on why HT and TH are equally likely is a quiz item (12-screen cap); the l28 choice of A's best first move is the trap screen, so the l28 drill choice asks who survives; the l29 chords use `plane` (the `circle` canvas cannot draw a chord); the homework `order` item derives E[R] by the gap argument (a variant of the E[m] derivation, which the lesson already orders); the homework truel fixes p_C = 1, so the three-player round happens once and backward induction is finite (tests avoid every tie between moves, for A, B and C).

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**. No warnings in level 5 files. `VOICE_BASE=/home/user/zero-to-quant/app/content/courses/puzzles/ python3 docs/reviews/voice-scan.py`: 0 long sentences and 0 long explanations in level 5 files (the 6 remaining course-wide hits are in levels 1 and 3).

## Playthrough

`node tools/playthrough.mjs --local-cdn <scratchpad>/pkgs`, all six lessons, plain and with `--mobile --shots --why`; sets with `--set`:

| File | Plain | `--mobile` |
|---|---|---|
| l25-fair-from-biased | ok, 14 checks, quiz 3/3 | ok, 14 checks, quiz 3/3 |
| l26-estimating-n | ok, 13 checks, quiz 3/3 | ok, 13 checks, quiz 3/3 |
| l27-given-the-total | ok, 15 checks, quiz 3/3 | ok, 15 checks, quiz 3/3 |
| l28-duels | ok, 15 checks, quiz 3/3 | ok, 15 checks, quiz 3/3 |
| l29-random-chords | ok, 15 checks, quiz 3/3 | ok, 15 checks, quiz 3/3 |
| l30-follow-ups | ok, 15 checks, quiz 3/3 | ok, 15 checks, quiz 3/3 |
| review-5 | ok, recorded 10 of 10 | |
| homework-5 | ok, marked 10 of 10 right, 47 of 47 marks | |

Every code solution passes its hidden tests in the browser (the playthrough checks Show solution), and every starter fails them (each returns `None` or does not raise). Each solution was also run against its tests in plain Python first.

Screenshots (desktop, 390 px and Why sheets) are in the scratchpad `puzzles-5/shots`. Fixed after looking: the l26 bars were flat under the default 0 to 1 axis (`yMax: 0.12`); l26 gap labels crowded the point labels at 390 px (moved below the axis); the l27 transfer split "+ £2k" across a line (now `$+2$` in £k); the l27 derive grid pushed the order list off screen (`maxHeight: 240`); the l28 tree caption promised chances the leaves did not show; the l29 radius was drawn in the chord's colour; `£` inside maths would have been italic (now `\text{£}`); the l30 three-player graph had a bent edge crossing B's node (re-laid as a triangle).

## Numbers and their sources

Every number was computed exactly (fractions) and again by a second method: enumeration, `random.Random(seed)` simulation (100,000 to 200,000 trials), value iteration, or a best-response solver over every stationary strategy. Scripts: `check_numbers.py` (116 checks), `check2.py`, `check3.py`, `check4.py`.

| Number | Exact | Second method |
|---|---|---|
| Fair bit, E[flips] = 1/(pq) | 9/2 (2/3), 25/6 (0.6), 100/9 (0.9), 4 (1/2) | sim 4.5043, 4.1682, 11.073 (1.2 standard errors off), 4.0068 |
| Round kept at 0.7; HH at 2/3 | 0.42; 4/9 | direct |
| Die from a coin; three or five people from a coin | 4; 8/3; 24/5 | 3 × 8/6; sim 4.7922 |
| Three people at 0.6 (one head in three) | 125/12 = 10.4167 | sim 10.414 |
| Two bits, four people at 0.6; two-bit three-way | 25/3; 100/9 = 11.1111 | sim 11.105 |
| Tick feed at 0.8; kept share | 6.25; 0.32 | direct |
| von Neumann code, 20,000 flips at 0.8 | about 3,200 bits | seed 2 gives 3,177; seed 1 share 0.4997 |
| Serial estimates m + m/k − 1 | 119 (60), 74, 119 (five, max 100), 74 (30, 50), 59, 973.4, 10 (k = N) | unbiased by enumeration at (20, 3), (12, 4), (15, 2) |
| E[m] = k(N + 1)/(k + 1) | 63/4 (3 of 20), 14 (2 of 20), 44/5 (4 of 10) | enumeration of all subsets |
| Twice the mean less one | 79.5; variance 28 against 14 at N = 20, k = 4 | enumeration |
| Uniform maximum | 1.2 (k = 3, 0.9), 2.5 (k = 4, 2) | (k + 1)/k |
| Range estimate | 202/3 (23 to 64), 84.5 (105 to 162) | E[R] = 153/5 at N = 50, k = 4 by enumeration; sim with a random start 50.03 |
| `tank_sim(100, 5, 20000, s)` | mean est. 99.94 (s = 1), mean max 84.09 (s = 2); exact 100 and 505/6 | SE 0.117 and 0.098 |
| Given a total (two dice) | 3/5, 17/3, 1/9, 70/9, 2/5, 36/11, 1/3, 1/5, 9/2, 5/6, 16/7, 102/11, 1 (total 12) | enumeration of 36 |
| Three dice | 1/2 (total 5, a 3), 1/3 (total 10, a 6) | enumeration of 216; sim 0.3353 |
| Same colour, both hearts | 78/650 = 0.12 | enumeration of 1,326 pairs |
| n-sided, total n + 1, larger | 5, 8, 75.5 = (3n + 2)/4 for even n (odd n differ: 21/5 at n = 5) | enumeration at n = 5 to 20 |
| Two-day P&L, total +1 | P(a losing day) 1/2; unconditional 0.64 | enumeration |
| Duels | 1/2, 4/7, 2/3, 3/7, 10/19, 1/2 (1/5 v 1/4), 1/2 (B first), 1 (p = 1) | sim 0.4967, 0.4282 for the first and fourth |
| Even point | q = p/(1 − p): 1/3 at p = 1/4 | solve |
| Truel (1/3, 2/3, 1) | air 25/63, at C 59/189, at B 50/189; B 8/21, C 2/9 | best-response solver over stationary strategies; sim 0.3971, 0.3803, 0.2226; at C sim 0.3121 |
| Truel (1/2, 2/3, 1) | air 17/30, at C 23/60; B 4/15, C 1/6 | solver |
| Truel, homework tests | (1/2, 3/4) 31/56 air; (1/3, 1/2) 5/12 air; (1/5, 1/4) 59/200 at C (air 11/40); (1/6, 1/4) 109/432 at C | backward induction and the solver agree; sim 0.2949 and 0.2744 for (1/5, 1/4) |
| `truel_air` with p_C = 0.9 | 165/406, 80/203, 81/406 | solver |
| Bertrand, longer than √3 | 1/3, 1/2, 1/4 | sim 0.3337, 0.5019, 0.2468 (code seeds 1 to 3, 20,000 chords) |
| Longer than the radius | 2/3, √3/2 = 0.8660, 3/4 | sim 0.6686, 0.8661, 0.7489 |
| Longer than √2 | 1/2, 1/√2 = 0.7071, 1/2 | sim 0.4991, 0.7087, 0.4993 |
| Expected chord length | 4/π = 1.2732, π/2 = 1.5708, 4/3 | sim 1.2734, 1.5711, 1.3322 |
| Envelopes | see £20: £25; before looking £22.50 each; three pairs see £40: £50, see £80: keep, before looking £35; (£5, £10, £20, £40) see £10: £12.50; switch unless £80: 125/3 | enumeration; sim 41.60 |
| Backtest day | random day £40; day of a random trade −£230 | direct |
| Larger of two n-sided dice | 161/36, 553/40 = 13.825, 143/20 = 7.15, 1 (n = 1), 13433/200 = 67.165 (n = 100) | enumeration of n × n |
| Reroll with cost (d6) | £4 (1), £4.50 (0.50), £3.60 (2), £3.50 (2.50, 3, 10), £3.75 (1.50) | value iteration |
| Reroll, other dice at £1 | d8 £5.50, d10 £7, d20 91/6 | value iteration |
| Players in turn | 6/11, 36/91, 4/7 (coin, three), 8/15 (coin, four) | p/(1 − q^k) |
| Coupons; runs | 12 H₁₂ = 86021/2310 = 37.2385; 6 H₆ = 14.7; HHH at 2/3 = 57/8; HHHH fair = 30 | sim 7.1274 for 57/8 |

Conventions: Python simulations use `random.Random(seed)` with the seeds named in each code widget; no screen asks the learner to type a value read from a canvas simulation (there are none). Money is £ throughout.

## Proposed `course.json` change

None.

## Backlog

Five bullets under "Raised later (puzzles level 5)" in `docs/BACKLOG-INBOX.md`: the bars pivot target the validator refuses as a number, chords on the `circle` canvas, a region constraint for plane points, a loop-back arrow on `tree`, and another vote for a drill block beyond the 12-screen cap.

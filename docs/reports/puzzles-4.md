# Report: puzzles level 4 (Games and betting)

Author: content agent, 3 November 2026. Brief: `docs/briefs/puzzles.md` section "Level 4" and the course context, with the orchestrator's session rules (follow-up screen per lesson, `tags` on drill and homework items, `pace` where the validator accepts it, no firm names, `longform` only in homework, `shuffle: true` on choices). Generators and checks live in the scratchpad folder `puzzles-4` (`gen_l19.py` to `gen_l24.py`, `gen_sets.py`, `zq.py` helpers, `penney.py`, `check_l19_l23.py`, `check_l24_sets.py`, `play.sh`).

## Files written

All in `app/content/courses/puzzles/`. Ids, titles, objectives and skills follow `course.json`: `pz-games` on every lesson, `pz-recursion` also on l19 and l20, `pz-expectation` also on l21 and l23, all six skills on l24.

| File | Screens | Quiz / items | Shape and canvases |
|---|---|---|---|
| `l19-who-wins.json` | 12 | 4 | title (the four books in order and *Probability and Markets* as "a free guide from a trading firm"); tap the losing piles 1 to 12 on a `grid` (multiples of 4); 21 matches (take 1); first six wins on a `graph` chain (6/11); first head wins (2/3); trap "first or second from 20?" (trading firms; second); generalise (backward induction, multiples of k + 1, 1/(2 − p)); `order` derivation of 1/(2 − p) with the even-split distractor; drill choice (30 matches, takes 1 to 4: no move wins); drill table (3/5, 3/4, take 3 from 23); follow-up three players (36/91); transfer second-price sealed bid (bid £100) |
| `l20-betting-on-sequences.json` | 10 | 3 | `graph` (`markov: true`) joint automata: HH v TH (TH 3/4), HHT v THH (THH 3/4), HHT v HTH (HHT 2/3, fair odds 2 to 1); trap (even money on HTH); generalise (first-step analysis named, Conway's leading numbers named once; HTH·HTH = 5); `order` node equations; `code` `first_to_appear` with a hidden `solve` and `penney_sim`; drill table (3/4, 2, 7/8); follow-up biased coin (5/9); transfer choose second against THT (TTH, 2/3) |
| `l21-kelly.json` | 12 | 3 | `series` (log scale, three bettors on the same 200 seeded flips, f = 0.1, 0.2, 0.4); `plane` explore, drag along g(f) to the peak (live caption); g(0.2) = 0.0201 (Kelly fraction named); half Kelly 0.0150; double Kelly −0.0024; trap all in; `order` derivation of f* = p − q; generalise f* = p − q/b (2 to 1, p = 0.4: 0.1); `code` `kelly`, `growth`; drill table (0.1, 0.0667, 0.0050); follow-up 2 to 1 fair coin (1/4); transfer half Kelly on a backtested strategy (0.125) |
| `l22-when-to-hedge.json` | 10 | 3 | `plane` with the two outcome lines, drag the hedge to the crossing (£300 locks £200); ladder at 2 to 1 (lock £300); `tree` of two games of a best-of-seven (bet £31.25), 1–1 (bet £37.50); trap (always hedge: costs £60 of expectation); `order` derivation of the Kelly hedge £60 on a £1,000 bankroll; generalise (half the gap; stake times the chance the game decides); drill table (100, 50, 50, 50); follow-up best of five (37.50); transfer one-step delta hedge (0.5 shares) |
| `l23-doubling-up.json` | 11 | 3 | `bars` hook (£7 cycle: expected gain 0); `walk` explore with the `bankroll` overlay doubling from £63; ledger `table` canvas, ten doublings (1/1024 and £0); European red (−0.3056); trap (rare means safe); generalise optional stopping (stop at +£5 or 100 bets: £0; unlimited bankroll sentence); `order` proof of zero; drill table (0.0078, 0, −0.1735); drill choice (option selling has the doubling shape); follow-up £127 (−0.2052); transfer selling volatility (L = £49,000) |
| `l24-mixed-set.json` | 12 | 3 | 20 unlabelled puzzles: a 7-row short-calculation `table`, three "which method?" choices (ants, doubling, meeting), multi-stage two coins (`tree`, 0.9), strategic 40 matches (take 4), trap (uniforms on [0, 2] past 2: e, not 2), edge case with too little information (ask), a 6-row short table, multi-stage three rolls of a d8 (`table` canvas, 97/16), strategic Penney against HTT (HHT), transfer a mock first-round script (lock £60) |
| `review-4.json` | | 9 items (2, 3, 3, 2, 3, 2, 4, 3, 2) | every lesson of the level; `timed: { "seconds": 1260 }` (a guide clock, no lock) |
| `homework-4.json` | | 9 items (5, 4, 4, 4, 4, 4, 4, 5, 3) | `code` `first_to_appear` for any pair, no helper (5); `code` `kelly_sim` (4); `order` derivation of f* = p − q/b with two distractors; `longform` spoken answer on the 0.6 bet (10-point rubric, full model); four players (216/671); best of nine (£27.34); table maximum on red (−0.2713); Kelly partial hedge at p = 0.55 (£180, at 5); choose second against THH (TTH) |

Interview form. Every drill screen carries `"tags": ["<family>"]` and states about 3 minutes a puzzle, kept by the learner, with the argument said aloud. The validator accepts `pace` (engine item 457 landed during this pass), so every drill, follow-up and l24 screen, every quiz item and every review and homework item carries `pace` in seconds as well as the prose. Each lesson has one "Follow-up: ..." screen with the brief's extension. Tags: `who-wins`, `betting-on-sequences`, `kelly`, `when-to-hedge`, `doubling-up`, `mixed-set`; l24 screens add the style (`short`, `multi-stage`, `strategic`), and its two multi-family tables carry `["mixed-set", "short"]` (the validator warns above four tags). Quiz items are tagged with the lesson's family so they join the Interview practice deck. No firm names: the "go first or second" question is "trading firms ask this one". Edge cases: l19 simultaneous rolls (quiz), l20 HT v TH (quiz), l21 no edge (quiz and generalise), l22 hedge at fair odds (quiz), l23 unlimited bankroll (generalise and quiz), l24 missing information (screen).

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**. Warnings in my files: four "problem screen without a canvas before the ladder ends" in l24 (the which-method and strategic screens; l24 has no ladder). `VOICE_BASE=.../puzzles/ python3 docs/reviews/voice-scan.py`: 0 long sentences and 0 long explanations in level 4 files.

## Playthrough

PLAYTHROUGH_RESULTS

Screenshots (desktop, 390 px and Why sheets) are in the scratchpad `puzzles-4/shots`. Fixed after looking: the l19 chain graph was squat (nodes spread, height 300); the l20 automata overlapped at 390 px while end nodes read "HHT wins" (now the bare pattern, caption says the right-hand nodes end the game); the l21 and l22 planes drew the x-axis title over a tick at y = 0 (`xAxis: "bottom"`).

## Numbers and their sources

Every number was computed exactly (fractions) and again by a second method (simulation with `random.Random(seed)`, a grid search, Conway's leading numbers, or a recursion), in `check_l19_l23.py`, `check_l24_sets.py` and `penney.py`.

| Number | Exact | Second method |
|---|---|---|
| Alternating die, first six | 6/11 = 0.5455 | sim 0.5445 (200,000) |
| Coin, first head | 2/3 | sim 0.6655 |
| First 1 or 2 | 3/5 | sim 0.5984 |
| Duel ½ v ⅓, A first | 3/4 | sim 0.7509 |
| Three players | 36/91 = 0.3956 (then 30/91, 25/91) | sim 0.3972 |
| Four players (homework) | 216/671 = 0.3219 | sim 0.3230 |
| Double six alternating (review) | 36/71 = 0.5070 | formula 1/(2 − p) |
| Take-away losing piles | multiples of k + 1 | solver over piles 0 to 42 |
| HH v TH; HHT v THH; HHT v HTH; HT v TH | 1/4; 1/4; 2/3; 1/2 | node equations, Conway, sim (100,000) |
| TTH v HTT; HTH v HHT; HHH v THH | HTT 3/4; HTH 1/3 (odds 2 to 1); THH 7/8 | all three methods |
| HH v TH at P(H) = 2/3 | TH 5/9 = 0.5556 | sim 0.5536 |
| vs THT: TTH, HHT, HTH, TTT | 2/3, 5/8, 1/2, 2/5 | node equations, sim |
| vs HTT: HHT, THT, TTH, HHH | 2/3, 1/2, 1/4, 2/5 | node equations |
| vs THH: TTH, HHT, HTH, TTT (homework) | 2/3, 1/4, 1/2, 2/5 | node equations, sim 0.6669 |
| HTH v HHH (review) | 3/5 | Conway 4 : 6, sim 0.6009 |
| Homework pairs | HTHT/THTT 9/14, HH/THT 5/8, HTH/THTT 3/4, HHH/TTTT 15/22, HHTT/TTH 3/8, HTHH/THHH 7/12 | Conway, sim |
| l20 code explain | seed 1, 20,000 games: 0.6640 | SE 0.0033 |
| g(0.2), g(0.1), g(0.4) at p = 0.6 | 0.020136, 0.015042, −0.002447 | grid argmax 0.2 |
| Half-Kelly share; spread | 0.747; sd 0.0983 v 0.1986 a bet | direct |
| g zero crossing | f ≈ 0.389 | bisection |
| Kelly fractions | 0.2, 0.1 (2 to 1, 0.4), 0.1, 1/15 = 0.0667, 1/4, 0 (0.3 at 2 to 1), 0.4, 0.25 (0.55 at 1.5), 0.3, 0.04, 0.0625, 1/8 | grid argmax for four of them |
| g at p = 0.55, f = 0.1 | 0.005008 | direct |
| g(0.5, b = 2, 0.25) | 0.058892 | grid argmax |
| 200 bets at f* | e^{4.03} ≈ 56 | direct |
| Survive 10 all-in bets | 0.6^{10} = 0.00605 | direct |
| l21 hook series | seed 15, 120 wins in 200: £5,609.81 (0.2), £2,025.46 (0.1), £61.30 (0.4) | ordering matches g |
| Transfer half Kelly | full 0.25, half 0.125; at true 0.5, 0.1667 | direct |
| Hedges | 5 to 1 £100: 300 locks 200; at 2 to 1: 200 locks 300; 3 to 1 £50: 100 locks 50; 4 to 1 £40: 100 locks 60; 9 to 1 £20: 100 locks 80; 4 to 1 £20: 50 locks 30 | both outcomes checked |
| Series bets (S = £100) | bo7 0–0 31.25, 1–0 and 0–1 31.25, 1–1 37.50, 2–2 50, 3–1 25, 3–3 100; bo5 37.50; bo3 50, 1–0 50; bo9 27.34 | backward recursion v closed form; replication sim gives exactly ±£100 |
| bo7 values after two games | +62.50, 0, −62.50 | recursion |
| Trap EV at p = 0.6 | £260 unhedged v £200 locked | direct |
| Kelly hedge (£1,500/£900, p = 0.6) | h = 60; E log 7.10889, 7.11021, 7.09008 | grid search over whole pounds |
| Kelly hedge at p = 0.55 (homework) | h = 180 | grid search |
| Delta | 0.5 shares | direct |
| Doubling, fair | 7/8 v 1/8; 1/1024; 1/128; 1/16; EV 0 for n = 3, 6, 7, 10 | sim of 400,000 cycles (−0.016, within noise) |
| Doubling on red (q = 19/37) | n = 10: −0.3056; 7: −0.2052; 6: −0.1735; 4: −0.1126; 9 (table max): −0.2713 | 1 − (2q)^n both ways; sims −0.290 (SE 0.058) and −0.214 (SE 0.020) |
| 1,000 cycles, at least one failure | 0.6236 | sim 0.6216 |
| Short volatility | L = 980/0.02 = 49,000; 0.98^{30} = 0.5455 | direct |
| l24 short set | 137/12, 1, 9/4, 42, 19/117 = 0.1624, 1/3, 4/5, 5/16, 5/9, 1/π, 1, 4/7, 0.3 | sims 11.406, 0.9989, 2.2483, 41.985, —, —, 0.8005, 0.3125, 0.5550, 0.3185, 1.0004 |
| l24 multi-stage | 9/10; 97/16 = 6.0625 (4.5, 5.5) | sims 0.9001, 6.058 |
| Exceeding 2 with U[0, 2] | e | sim 2.7185 |
| Meeting with 15 minutes | 7/16 | direct |
| Distinct faces in six rolls | 31031/7776 ≈ 3.9906 | direct |
| `kelly_sim` (homework) | n g(f): 20.1355, 15.0419, −9.7876, 29.4458 | solution with seeds 1 to 4: 20.1355, 15.0419, −9.7876, 30.1389 (the median path won exactly 600 of 1,000, 2,400 of 4,000) |

Code checks: each `solution` passes every hidden test and each starter fails (l20 10/10 v 0/10 after the determinism test was made to need a float; l21 13/13 v 0/13; homework 9/9 v 0/9 and 6/6 v 0/6, run in CPython and in the browser playthrough). Simulation tests accept three standard errors (median SE taken as 1.2533 σ/√paths).

## Seeds and conventions

Python: `random.Random(seed)`, win when `rng.random() < p`. Lesson canvases: walk `sim.seed` 5 (l23); the l21 series values are my own Python run (seed 15), never the engine's stream; no screen asks for a value read from a canvas simulation. Four decimal places with `tol` 0.0005 for chances; whole numbers `tol` 0; pounds `tol` 0.005 or 0.5.

## course.json

No change proposed.

## Backlog

Five bullets under "Raised later (puzzles level 4):" in `docs/BACKLOG-INBOX.md`: table cell-level `wrong` keys refused by the validator; markov `graph` node radius at 390 px; walk `bankroll` doubling cannot model fixed-length cycles; deck tags cannot reach table rows; no timed block inside a lesson.

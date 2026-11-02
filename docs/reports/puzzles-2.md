# Report: puzzles level 2 (Conditioning)

Author: content agent, 2 November 2026. Brief: `docs/briefs/puzzles.md` section "Level 2", with the orchestrator's additions (follow-up screens, a pace, `tags`, no firm names, `longform` only in homework, `shuffle: true` on choices).

## Files written

All in `app/content/courses/puzzles/`. Ids, titles, objectives and skills are those of `course.json`.

| File | Screens | Quiz / items | Skills | Notes |
|---|---|---|---|---|
| `l7-cards-and-colours.json` | 11 | 4 | pz-conditioning, pz-symmetry | title (books), tap hook on `boxes`, trap, gap `order`, drill table, follow-up, P&L transfer |
| `l8-urns.json` | 10 | 3 | pz-symmetry | explore with a `frames` shuffle slider on `boxes`, Pólya tree filled by a bound `table`, trap, swap `order`, drill, follow-up, audit transfer |
| `l9-bayes-in-a-minute.json` | 11 | 3 | pz-conditioning | natural-frequency tree filled by a bound `table`, `population: 100` witness, two-headed coin, trap, odds `order`, drill, follow-up, crash-alert transfer |
| `l10-ruin-in-interviews.json` | 10 | 3 | pz-recursion | `walk` with barriers and hits (reseed and `p` controls), infinite-time screen, trap, duration check `order`, `code` (ruin_prob, ruin_sim), drill with the drunkard's walk, follow-up, trader transfer |
| `l11-largest-of-several.json` | 10 | 3 | pz-conditioning | 6 x 6 grid tap hook, `plane` density with an `n` slider, two normals on `distribution`, trap with the `3x` line, `expression` derive, drill, follow-up, best-of-20 backtests transfer |
| `l12-ants.json` | 11 | 3 | pz-symmetry | explore with a time slider and derive-driven ants on a `plane`, 100 ants, ants from the ends, fly and trains, trap, ghost `order`, drill, follow-up, netting and frog transfers |
| `review-2.json` | | 10 items (difficulty 2, 2, 3, 3, 2, 3, 3, 4, 3, 4) | all four used skills | every lesson twice or once; `timed: { "seconds": 1800 }` (a guide clock, 3 minutes an item, no lock) |
| `homework-2.json` | | 10 items (5, 4, 4, 4, 4, 4, 5, 4, 4, 3) | | two `code` (ruin_duration at 5, natural_frequency at 4), one `order` (fair ruin k/N), one `longform` (spoken Bayes, 10-point rubric, full model), six numeric |

Interview form, per lesson: one `Drill` screen (a two-column `table` of three to six new puzzles, prose stating "about 3 minutes each" and the total, the learner keeping time) carrying `"tags": ["<family>"]`; one screen titled "Follow-up: ..." with the interviewer's next question on the worked puzzle; the brief's follow-up numbers. Tags (lesson id without its number: `cards-and-colours`, `urns`, `bayes-in-a-minute`, `ruin-in-interviews`, `largest-of-several`, `ants`) are on every drill screen, on quiz items that are drill puzzles, and on every review and homework item. Every `choice` has `shuffle: true`. No `longform` in lessons. No firm names: the drunkard's walk says "reported at hedge funds", the frog "reported at trading firms". The l7 title screen names Mosteller, Zhou (the green book), Crack, Joshi and co-authors, and "*Probability and Markets*, a free guide from a trading firm": the brief asks to name the Jane Street guide, but the orchestrator's rule is that no firm is named outside `recruiting` l4 and mock descriptions, so the guide is named by its title only.

Edge cases: l7 one special card (26.5, quiz); l8 an urn of one colour (quiz); l9 a test with no false positives (quiz); l10 k = 0 (quiz) and k = N (code tests); l11 the minimum of two uniforms (generalise); l12 a single ant (generalise).

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 386 warnings, none in a level-2 puzzles file (the only puzzles warning is the course's own count of unwritten lessons). The `tags` field on lesson screens, quiz items and set items passes the validator.

## Playthrough

`node tools/playthrough.mjs --lesson puzzles/<id> --local-cdn <pkgs>`, each lesson alone, all passed:

| File | Result |
|---|---|
| l7-cards-and-colours | ok, 14 checks, quiz 4/4 |
| l8-urns | ok, 13 checks, quiz 3/3 |
| l9-bayes-in-a-minute | ok, 14 checks, quiz 3/3 |
| l10-ruin-in-interviews | ok, 13 checks (code screen run in Pyodide), quiz 3/3 |
| l11-largest-of-several | ok, 13 checks, quiz 3/3 |
| l12-ants | ok, 14 checks, quiz 3/3 |
| review-2 (`--set`) | ok, recorded 10 of 10 |
| homework-2 (`--set`) | ok, marked 10 of 10 right, 47 of 47 marks |

Screenshots (1280 px and 390 px, with `--why`) are in the scratchpad `pz2/shots`, `pz2/shots2` and `pz2/shots-sets`. Faults found and fixed from them: `bag` items overlapping their labels (replaced by cards); small `boxes` canvases (now `size: "large"`); population grids with no visible legend (captions now name each colour and count); `highlight` on population groups hiding their colours (replaced by caption patches); the l12 explanation patch at t = 0.5, where the ants happen to sit at their starting points (now t = 0.6); the `x^3` curve in the l11 trap explanation drawn in the same colour as `3x`.

The starters of the three code widgets return `None`, so they fail their tests; the solutions pass (checked by the playthrough).

## Numbers

Every number was computed exactly (Python `fractions`, scratchpad `pz2/check.py`) and by simulation twice: a pure-Python `random.Random(2026)` run (`check.py`, 50,000 to 2,000,000 trials) and a NumPy run with standard errors (`check2.py`, seed 20261102); ruin chances and durations were also checked by a linear solve of the first-step equations. Every simulated value below is within 2 standard errors of the exact one.

| Where | Quantity | Exact | Decimal | Simulation (NumPy, se) |
|---|---|---|---|---|
| l7 hook | 2nd red given 1st red, 3R 3B | 2/5 | 0.4 | by count |
| l7 | 2nd red given 1st red, full deck | 25/51 | 0.4902 | 0.4904 (Python) |
| l7 | 2nd card an ace | 1/13 | 0.0769 | 0.0762 (Python) |
| l7 | position of first ace | 53/5 | 10.6 | 10.588 (0.013) |
| l7 trap | card after first ace is A♠ (and 2♣) | 1/52 | 0.0192 | 0.0196, 0.0194 (Python) |
| l7 drill | two cards share a suit | 12/51 = 4/17 | 0.2353 | 0.2347 (Python) |
| l7 drill | at least one ace in two | 33/221 | 0.1493 | 0.1496 (Python) |
| l7 drill | reds before first black | 26/27 | 0.9630 | 0.9616 (0.0021) |
| l7 follow-up | position of first heart | 53/14 | 3.7857 | 3.7789 (0.0048) |
| l7 transfer | two losing days of 8 in 21 | 2/15 | 0.1333 | 0.1345 (Python) |
| l7 quiz | 3rd heart after two spades; bottom red after two reds; ace of spades position; 10th is A♥ | 13/50; 12/25; 53/2; 1/52 | 0.26; 0.48; 26.5; 0.0192 | 0.4814 for 12/25 (Python) |
| l8 | last ball red, 5R 3B | 5/8 | 0.625 | 0.6270 (Python) |
| l8 | reds before first blue, 5R 3B | 5/4 | 1.25 | 1.2477 (Python) |
| l8 Pólya | paths RR, RB, BR, BB | 1/3, 1/6, 1/6, 1/3 | | exact enumeration |
| l8 Pólya | exactly 2 reds in 4 draws (binomial blurt 3/8) | 1/5 | 0.2 | 0.2005 (Python); each path 1/30 |
| l8 trap | 3rd ball red, unseen | 5/8 | 0.625 | 0.6263 (Python) |
| l8 drill | whites before first black 6W 4B; 7th black; Pólya 2R 1B second red | 6/5; 2/5; 2/3 | 1.2; 0.4; 0.6667 | 1.1991; 0.3973; 0.6656 (Python) |
| l8 follow-up | reds before first blue, 10R 4B | 2 | 2 | 2.0045 (Python) |
| l8 transfer | clean trades before first error, 188 and 12; 5th checked is an error | 188/13; 3/50 | 14.4615; 0.06 | 14.445 (0.031); 0.0607 |
| l8 quiz | first and last red | 5/14 | 0.3571 | 0.3564 (Python) |
| l9 | medical test 1%, 99%, 5% (99 and 495 of 10,000) | 1/6 | 0.1667 | 0.1660 (Python) |
| l9 | witness 15%, 80% (12 and 17 of 100) | 12/29 | 0.4138 | 0.4148 (Python) |
| l9 | two-headed coin, 1 in 1,000, ten heads (1,024 and 999) | 1024/2023 | 0.5062 | 0.5077 (0.0025) |
| l9 trap | 1 in 500, 99% both ways (198 and 998 of 100,000) | 99/598 | 0.1656 | by count |
| l9 drill | Monty Hall switch; signal 60%/30% at 40% (24 and 18); two tests (9,801 and 2,475 of 1,000,000) | 2/3; 4/7; 99/124 | 0.6667; 0.5714; 0.7984 | 0.6672; 0.5714 (Python); 0.7996 (0.0008) |
| l9 follow-up | three tests: odds (1/99) × 19.8³ = 78.408 | 9801/9926 | 0.9874 | 0.9873 (0.0003) |
| l9 transfer | crash alert 2%, 90%, 10% (18 and 98 of 1,000) | 9/58 | 0.1552 | 0.1559 (Python) |
| l9 quiz | spam (180 and 16 of 1,000); 2.5% false positives | 45/49; 2/7 | 0.9184; 0.2857 | by count |
| l10 | fair £3 to £10: P, duration | 3/10, 21 | | 0.3004, 21.02 (Python); linear solve 0.3000, 21.0000 |
| l10 | p = 0.6, £3 to £10 | 41553/58025 | 0.7161 | 0.7159 (0.0007); linear solve 0.7161 |
| l10 trap | fair £5 to £20 | 1/4 | 0.25 | 0.2501 (Python) |
| l10 drill | fair 5 of 10: P, D | 1/2, 25 | | 0.5004, 25.00 (Python) |
| l10 drill | p = 0.45, £2 to £4: 1/(1 + r²), r = 11/9 | 81/202 | 0.4010 | 0.3998 (Python) |
| l10 drill | p = 18/38, £10 to £20, r = 10/9 | 3486784401/13486784401 | 0.2585 | 0.2584 (0.0007) |
| l10 drill | drunkard 4 of 10: P, D | 2/5, 24 | | 0.4007 (0.0008), 23.97 (0.03) |
| l10 follow-up | duration p = 0.6, £3 to £10 | 48291/2321 | 20.8061 | 20.825 (0.024); linear solve 20.8061 |
| l10 transfer | p = 0.52, £20 to £40, r = 12/13 (duration 332.14) | ratio of 23-digit integers | 0.8321 | 0.8326 (0.0006); duration 331.4 (0.41) |
| l10 code | seeded `ruin_sim(3, 10, 0.6, 20000, 1)`; `(3, 10, 0.5, 20000, 2)` | test bands 0.0096, 0.0098 (3 se) | 0.7147; 0.29815 | identical in CPython and Pyodide (Mersenne Twister) |
| l10 quiz | fair 7 of 10; fair 2 of 5 duration | 7/10; 6 | | 0.6995; 6.00 (Python) |
| l11 | P(max of two dice ≤ 5) | 25/36 | | count |
| l11 | max of three dice is 6 | 91/216 | 0.4213 | 0.4200 (Python) |
| l11 | E max of 3 uniforms | 3/4 | 0.75 | 0.7500 (Python) |
| l11 | E max of two standard normals | 1/√π | 0.5642 | 0.5643 (0.0006) |
| l11 trap | P(max of 3 uniforms ≤ 0.5) | 1/8 | 0.125 | 0.1243 (Python) |
| l11 generalise | E min of two uniforms | 1/3 | 0.3333 | 0.3331 (Python) |
| l11 drill | larger of two dice; middle of three uniforms; P(max of 10 > 0.9); min of three Exp(1) | 161/36; 1/2; 1 − 0.9¹⁰; 1/3 | 4.4722; 0.5; 0.6513; 0.3333 | 4.4706; 0.4987; 0.6523; 0.3334 (Python) |
| l11 follow-up | (n + 1)(4n − 1)/(6n) at n = 6, 10 (and 20) | 161/36, 143/20, 553/40 | 4.4722, 7.15, 13.825 | brute-force sums agree exactly |
| l11 transfer | best of 20 zero-skill backtests past 1.645 | 1 − 0.95²⁰ | 0.6415 | 0.6413 (0.0005) |
| l11 quiz | min of three dice ≥ 4; E max of 4 uniforms | 1/8; 4/5 | 0.125; 0.8 | 0.1250; 0.7999 (Python) |
| l12 explore | ants at 0.2 R and 0.7 L | 0.8 | | step-by-step bounce simulation 0.8 |
| l12 | 100 ants, 1 m | 100/101 | 0.9901 | 0.99010 (0.00002) |
| l12 | ants from both ends | 1 | | bounce simulation 1.0 |
| l12 | fly 75 mph for 1 hour; first leg 60 miles | 75 | | arithmetic |
| l12 trap | five-ant set-up check, ghost max equals bounce simulation | 0.9 | | bounce simulation 0.9 |
| l12 generalise | one ant | 1/2 | 0.5 | 0.5005 (Python) |
| l12 drill | 10 ants; ants at 0.3 R and 0.6 L; collisions 3 × 2 | 10/11; 0.7; 6 | 0.9091 | 0.9089 (0.0002) |
| l12 follow-up | 100 ants, 2 m | 200/101 | 1.9802 | 1.98020 (0.00005) |
| l12 transfer | net of +300 +200 +500 −400 −100; frog 1 or 2 to 10 | 500; 89 | | brute-force enumeration 89 |
| l12 quiz | 4 × 4 crossings; bird 90 miles | 16; 90 | | arithmetic |
| review | two hearts; 9th red of 4R 6B; screen 5%, 80%, 10%; fair 4 of 12 duration; min of two dice ≥ 3; 50 ants; first face card; p = 0.4, £2 to £5; 1 in 1,000 at 95%; Pólya R R B | 1/17; 2/5; 8/27; 32; 4/9; 50/51; 53/13; 40/211; 19/1018; 1/12 | 0.0588; 0.4; 0.2963; 32; 0.4444; 0.9804; 4.0769; 0.1896; 0.0187; 0.0833 | 0.0588; 0.3989; 0.2980; 31.95; 0.4431; 0.9802; 4.0694; 0.1903 (0.0006); 0.0188; 0.0843 |
| homework | ruin_duration tests: (3, 10, 3/5), (2, 4, 9/20), (2, 5, 2/5), fair 21 and 25, edges 0; p = 0.5001 gives 21.0056 | 48291/2321, 400/101, 1110/211 | 20.8061, 3.9604, 5.2607 | hidden seeded sims 20.8391 and 19.4935 against exact 20.8061 and 19.4340, within the 0.34 band (3 se, sd about 15.2) |
| homework | natural_frequency tests (99, 495, 1/6), (12, 17, 12/29), (24, 18, 4/7), (18, 98, 9/58), 495/2 | | | exact |
| homework | spoken answer, two tests | 99/124 | 0.7984 | as l9 |
| homework | second ace position; last two differ 7R 5B; next head after HH (biased 9/13); ever reach +1 at p = 0.4; E max three dice; frog 1, 2 or 3 to 10 | 106/5; 35/66; 35/52; 2/3; 119/24; 274 | 21.2; 0.5303; 0.6731; 0.6667; 4.9583; 274 | 21.211 (0.016); 0.5317; 0.6734 (0.0004); 0.6674; 4.9601; enumeration 274 |

Wrong-answer values in `wrong[]` were computed the same way (for example 0.4808 = 25/52, 0.5098 = 26/51, 0.6398 = 135/211 for r = p/q, 0.3906 = (5/8)², 0.4861 = 70/144).

## Seeds and conventions

- Canvas pictures use the engine's seeded streams (`walk` seed 11, the `frames` shuffles in l8 are authored orders); no answer is read from a canvas simulation.
- Code tests use pure Python `random.Random(seed)`; simulated tests accept three standard errors of the exact value (stated in each `how`).
- Answers to four decimal places with `tol` 0.0005; counts with `tol` 0; money in £.

## Proposed change to course.json

None.

## Backlog

Eight bullets appended to `docs/BACKLOG-INBOX.md` under "Raised later (puzzles level 2):".

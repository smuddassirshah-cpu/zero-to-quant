# Report: brainteasers level 3 (Quick reasoning)

Author: content agent, 3 November 2026. Brief: `docs/briefs/brainteasers.md`, course context and `## Level 3`. Standards: `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`. Ids, names, objectives and skills from `course.json` (`bz-quick` on l12 to l15; all four skills on l16).

## Files written

All in `app/content/courses/brainteasers/`. Generators and checks in the scratchpad folder `brainteasers-3/` (`lib.py`, `gen_l12.py` to `gen_l16.py`, `gen_sets.py`, `check_numbers.py`). `lib.write` wraps every bare factorial in KaTeX and keeps `7 × 7` on one line (no-break spaces).

| File | Screens or items | Quiz | Interactive canvas early | Notes |
|---|---|---|---|---|
| `l12-clocks-and-trains.json` | 12: explore, ladder, problem, trap, problem (edge), generalise, derive, 4 drills, transfer | 4 | `plane` clock: two hand `segments`, a minutes control, `derive` moves the hands and writes the time and both hand angles | chase on a `number-line` with a time control; trip table (4 columns, fits at 390 px) |
| `l13-digits-and-remainders.json` | 12: problem (table widget), problem, problem, problem (tap), trap, generalise, derive, 3 drills, 2 transfers | 3 | `table` widget: the learner extends the last digits of $7^4$ to $7^8$, beside a grid of "× 7" last digits | 60-cell `grid` with `tap-regions` on the multiples of 5, then the trap on the same grid |
| `l14-sums-in-one-line.json` | 12: problem (drag), ladder, problem, derive, problem, trap, problem (edge), generalise, 3 drills, transfer | 3 | `number-line` 0 to 21 with pairing `arrows`; `drag-point` to the partner of 7 | handshake trap on a `graph` ring (A's 11 edges, all 66 in the explanation) |
| `l15-numbers-to-know.json` | 12: explore, ladder, problem, problem, trap, generalise, derive, 3 drills, 2 transfers | 5 | log-scale `number-line` with a doublings control and a `derive` point at $2^n$ | √2 by dragging $x$ with a live $x^2$ caption; a `plane` of the "right numerator" $r \ln 2 / \ln(1 + r)$ against 72 and 69.3 |
| `l16-mixed-set.json` | 12 puzzles: 10 problems, trap (puzzle 10), transfer (puzzle 12) | 5 | neutral setup canvases (`boxes` coins, drawer, crew, hats; `grid` board; `number-line` times) | graded by `numeric` or `choice` only, as the brief says |
| `review-3.json` | 10 items, difficulty 2 to 4, order l12, l13, l14, l15, l12, l13, l14, l15, l14, then the level 1 jug recall | | | `skills`, `tags`, `pace` on every item; jug item uses `bz-search` |
| `homework-3.json` | 8 items, difficulty 3 to 5 (two at 5) | | | `order` with distractors (hw1, hw2), `longform` hw8 with a 10-point rubric and full model answer |

Every lesson has one `trap` with `byKey` lines, an edge case, a drill block of 3 or 4 tagged screens with the pace in the prose ("about a minute each, as an interview allows; say the argument aloud before you answer"), and a follow-up `transfer`. No lesson has a non-task screen (each generalise screen carries a confirmation task). Each worked teaser and drill ends its explanation with a one-sentence principle. The three books are named once, in l12's generalise screen. Prerequisites are cited by id: `contests` l5-modulo (l13 generalise and transfer), `series` l6-gauss (l14 ladder), `mental` l8-squaring and `mental-pressure` l8 (l15 screen 3, one screen only). `exp-log` l12-doubling-time already met the rule of 72; l15 goes past it with the numerator curve and the $r^2/2$ derivation.

**Tags and pace.** Drill screens, quiz, review and homework items carry `tags` from the brief's families (`clock-angle`, `relative-speed`, `average-speed`, `work-rate`, `last-digit`, `divisibility`, `trailing-zeros`, `pairing`, `telescoping`, `double-counting`, `constants`, `powers-of-two`, `rule-of-72`; l16 uses each puzzle's family: `invariant-parity`, `which-method`, `weighing-heavy`, `colouring-chequer`, `pigeonhole-worst-case`, `pirates`, `hats-line-parity`, `bridge-crossing`, `average-speed`, `missing-information`, `cycle-following`, `egg-drop`). `pace`: 60 s on l12 to l15 drills and quizzes and the review, 120 s on l16 and homework, 180 s on the jug recall and the longform.

## Departures from the brief (screen budget of 12)

- l12: the walkway drill (24 s) moved to the quiz; the stock link (£48) is a quiz item and a sentence in the transfer's prose and explanation; the 12:00 edge case is the generalise confirmation ($|30 \cdot 12| = 360$, so 0°); the round trip at 40 km/h is the edge screen. Quiz adds two new items: 6:30 (15°) and a tap with a drain (18 hours).
- l13: the edge case (0, 1, 5, 6), $2^{100} \bmod 7$ and the factorial-sum digit are quiz items. The trap follows a tap screen whose answer (12 multiples of 5) is the number candidates blurt. The generalise confirmation is new: 30! ends in 7 zeros. The derive proves the 11 test ($10 \equiv -1$).
- l14: the digit sum (13,500), the odd sum and the alternating sum are quiz items; the decagon (35) is the generalise confirmation.
- l15: $e^\pi$ against $\pi^e$, the 72% edge case (1.28), $0.99^{100}$, ln 2 and $2^{16}$ are quiz items; the drills are π², 9% and $1.01^{100}$. The "choice, then numeric" trap is split: screen 4 is the choice (72 or 69.3 at 8%), screen 5 the numeric 2.25. The generalise confirmation is new: ln 5 = 1.61.
- l16: puzzle 1 (eleven coins, turn two) is the brief's puzzle and repeats level 1 quiz `q-eleven-coins` word for word in substance; a later pass may want 13 coins. The 30-coin puzzle is tagged `weighing-heavy`, level 1's family for one odd coin.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 391 warnings, none on a brainteasers file. Voice: `VOICE_BASE=/home/user/zero-to-quant/app/content/courses/brainteasers/ python3 docs/reviews/voice-scan.py` reports **0 sentences over 20 words and 0 explanations over three sentences** (9,287 sentences scanned, levels 1 to 3). No em-dashes; minus signs are U+2212.

## Playthrough

All with `--local-cdn <scratchpad>/pkgs`.

| Run | Result |
|---|---|
| `--lesson` l12 to l16, desktop | all ok: 16, 15, 15, 17, 17 checks; quizzes 4/4, 3/3, 3/3, 5/5, 5/5 |
| `--lesson` l12 to l16 `--mobile` | all ok, same counts |
| `--set brainteasers/review-3` | ok, recorded 10 of 10 |
| `--set brainteasers/homework-3` | ok, marked 8 of 8 right |

Screenshots (desktop, 390 px and `--why`) were inspected. Fixes made from them: the clock had no numerals (hidden labelled points draw nothing; now tick labels); the clock drew about 410 px tall on desktop (now `maxHeight: 300`); the edge-case interval labels overlapped (now below and above); "No speed is enough" as a title gave the answer away (now "A target average"); the l13 tap screen's explanation marked 25 and 50 before the trap (removed); the l16 board was pre-shaded like a chessboard, naming the method in an unlabelled set (now plain); `order` lines in l14's derive and homework hw2 pushed the leave-out cross off the card at 390 px (now `\tfrac` and shorter lines); `7 ×` broke from `7` at a line end (no-break spaces).

## Numbers and their sources

Every number was computed by hand and again in `check_numbers.py` (exact fractions, exhaustive search, simulation or scans); all checks report OK.

| Number | Where | Second computation |
|---|---|---|
| 3:40 is 130°; hour hand stuck gives 150; reflex 230 | l12 s1 | hand rates 0.5° and 6° a minute |
| first meeting after 3:00 at $180/11 = 16.36$ min (3:16:22); every $720/11 = 65.45$ min, 11 in 12 h | l12 s2 | exact fractions; meetings listed |
| chase 6 km at 18 km/h: 20 min; ignoring lorry 4; adding speeds 2.22 | l12 s3 | direct |
| 60 and 40 average 48 (240 km in 5 h) | l12 trap, derive | harmonic mean and times |
| 20 km at 40 km/h uses 30 min, the whole budget of 40 km at 80; 160 km/h gives 64 | l12 edge | direct |
| 12:00 gives 360, so 0° | l12 generalise | formula |
| 9:15 is 172.5 (raw 187.5); 2:20 is 50 (stuck 60) | l12 drills | hand rates |
| right angles 22 in 12 h; opposite 11 in 12 h, 22 a day | l12 drill, transfer | exact roots of $5.5t = 90 + 180k$ and $180 + 360k$, plus a scan at 1/600 min |
| pipes 4 h and 12 h: 3 h; walkway 24 s; 6:30 is 15°; tap 6 h, drain 9 h: 18 h | l12 drill, quiz | direct |
| £100 at £40 and £60: 4.17 shares, £48 | l12 quiz, transfer | 200/(2.5 + 1.667) |
| 7^n last digits 7, 9, 3, 1; $7^{2026}$ ends in 9 ($2026 = 4 \cdot 506 + 2$) | l13 s1, s2, hw1 | `pow(7, 2026, 10)` |
| 123456789: digit sum 45; mod 11 is 5 (alternating sum); 45 mod 11 is 1 | l13 s3, derive | direct mod |
| 60! has 14 zeros (12 + 2); multiples of 10: 6 | l13 s4, trap | Legendre and stripping zeros from 60! |
| 30! has 7 zeros | l13 generalise | stripping zeros |
| $3^{2027}$ ends in 7; 125! has 31; $1! + \cdots + 99!$ ends in 3; 111111 = 7 × 15873, remainders 1, 4, 6, 5, 2, 0 | l13 drills, quiz | `pow`, factorials, loop |
| fixed last digits 0, 1, 5, 6 (4 and 9 alternate) | l13 quiz | powers 1 to 5 of each digit |
| $2^{100} \bmod 7 = 2$; $2^{20}$ ends 76; 60! in binary ends in 56 zeros | l13 quiz, transfers | `pow`, Legendre with 2, stripping factors of 2 |
| 1 to 20 is 210; 1 to 200 is 20,100; 1 to 150 is 11,325; 1 to 300 is 45,150 | l14, review | `sum(range)` |
| $\sum_{k=1}^{49} 1/(k(k+1)) = 49/50$; 2 to 9 gives 2/5; 3 to 11 gives 1/4; $n = 7$ gives 7/8 | l14, review, hw2 | exact `Fraction` sums |
| knockout of 50: 49 matches (rounds 50, 25, 13, 7, 4, 2, 1); of 1: 0 | l14 s5, edge | simulation with byes |
| handshakes: 12 people 66, 20 people 190 | l14 trap, review | `comb` |
| digit sum 1 to 999 is 13,500 | l14 quiz | brute force |
| odd 1 to 199 is 10,000; $1 - 2 + \cdots - 100 = -50$; decagon 35 diagonals | l14 quiz, generalise | direct |
| squares on 8 × 8: 204; rectangles 1,296 (8 × 8), 225 (5 × 5); squares on 5 × 5: 55 | l14, hw5 | brute force over line pairs |
| $\binom{50}{2} = 1225$ | l14 transfer | `comb` |
| $2^{19} = 524{,}288$, $2^{20} = 1{,}048{,}576$, $2^{30} = 1{,}073{,}741{,}824$, $2^{32} = 4.29 \times 10^9$, $2^{31} = 2.15 \times 10^9$, $1.024^3 = 1.0737$ | l15 s1, s2 | exact integers |
| 1.41² = 1.9881, 1.42² = 2.0164, 1.415² = 2.0022; √5: 2.23² = 4.9729, 2.24² = 5.0176, 2.235² = 4.9952 | l15 s3, hw6 | direct |
| doubling: 8% 9.006, 6% 11.90, 9% 8.04, 4% 17.67, 7% 10.24, 36% 2.254, 72% 1.278; right numerator 70.35 at 3%, 72.05 at 8%, 81.15 at 36% | l15, review, hw8 | `log(2)/log(1 + r)` |
| $e \ln \pi = 3.1117$, $e^\pi = 23.14$, $\pi^e = 22.46$ | l15 quiz | direct |
| π² = 9.8696; $1.01^{100} = 2.7048$; $0.99^{100} = 0.3660$; ln 5 = 1.6094; ln 2 ≈ 0.3 × 2.303 = 0.691 | l15 | direct |
| quadruple at 8%: 18.01 years; tenfold: 29.92 (3.32 × 9 = 29.88); £1,000 to £8,000 at 9%: 24.13 | l15 transfers, hw7 | `log` |
| $2^{100} = 1.27 \times 10^{30}$ | review | exact integer |
| eleven coins, turn two: never all tails | l16 p1 | BFS over head counts |
| 30 coins, one light: 4 weighings ($27 < 30 \le 81$) | l16 p3 | powers of 3 |
| 7 × 7 less the square next to a corner: 25 against 23 | l16 p4 | colour count |
| 3 pirates, 40 coins: (39, 0, 1); 5 pirates, 60: (58, 0, 1, 0, 1) as level 2 | l16 p7 | backward induction under level 2's rules |
| bridge 1, 2, 6, 9: 16 (escort 19); add 12: 26 (escort 32, pairing 6 with 9: 29) | l16 p9, p12 | Dijkstra over all crossing states |
| 20 prisoners opening 10: 0.3312 | l16 quiz | $1 - \sum_{11}^{20} 1/k$; simulation of 200,000 shuffles, 0.3309 |
| two eggs, 120 floors: 15 (14 gives 105) | l16 quiz | DP over drops |
| 4:50 is 155°; $9^{2027}$ ends in 9; 80! has 19 zeros; 10:10 is 115°; $13^{47}$ ends in 7; 200! has 49 | l16 quiz, review | hand rates, `pow`, stripping zeros |
| 45 and 90 average 60 | review | harmonic mean |
| jugs 5 and 7 to 1 litre: 8 steps (10 starting with the 7) | review | BFS from each first move |
| first opposite after 7:00: $60/11 = 5.45$ min (7:05:27); meeting at 38.18 | hw3 | exact fraction; angle at that time is 180 |
| $3^{100} \bmod 7 = 4$ ($3^6 = 729 = 7 \cdot 104 + 1$, $100 = 6 \cdot 16 + 4$) | hw4 | `pow` |
| ln 1.07 = 0.06766, $0.07 - 0.07^2/2 = 0.06755$; 72/7 = 10.29; 69.3/7 = 9.90; $69.3 \times 1.04 = 72.07$ | hw8 model | direct |

Tolerances: integers exact; decimals as stated in each `accept` line (for example 16.36 ± 0.01, 2.25 ± 0.01, 4.29 ± 0.011, doubling at 9% 8.04 ± 0.1 so the rule's 8 passes, tenfold 29.92 ± 0.5 so 30 passes).

## course.json

No change proposed.

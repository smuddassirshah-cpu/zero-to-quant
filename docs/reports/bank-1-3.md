# Report: interview bank part 1, session 3 (50 items)

Brief: `docs/briefs/bank.md` sections 1 to 4, "Session 3" in section 5, sections 6 to 9 and "Changes after session 1 (3 Nov)". Files written in `app/content/bank/`; nothing else in the repo was edited except this report and an append to `docs/BACKLOG-INBOX.md`.

| File | Items | Families |
| --- | --- | --- |
| `probability-3.json` | 14 | dice-ev, every-coupon, at-least-one, hats, waiting-for-hh, bayes-in-a-minute, ruin-in-interviews, betting-on-sequences, kelly, when-to-hedge, doubling-up, random-chords, expected-distance, buffon |
| `brainteasers-3.json` | 10 | hats-mod-k, weighing-heavy, backward-induction, scheduling, divisibility, powers-of-two, telescoping, double-counting, relative-speed, constants |
| `mental-3.json` | 10 | mental-arithmetic 2, percent-chain, fraction-odds, estimate-product, sequence-woven, sqrt-newton, word-time, net-score, ranking |
| `market-making-3.json` | 8 | card-fair, fermi-error, intervals, coverage, quote-centre, ledger-pnl, hedge-ratio, thinking-aloud |
| `behavioural-3.json` | 8 | star-story 3, why-us, video-answer, final-round, cv-lines, reasoning-aloud |

## Results

- `node tools/validate.mjs 2>&1 | tail -5` (from `app/`): **0 errors**, 392 warnings, none from `content/bank/` (no `style`, `source` or bank warning). The manifest lists all 21 bank files (sessions 1 to 4 and `sample.json`).
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: **All passed** (`#bank 124 drawable of 210, deck, pace line, schedule, miss, old save`). With `--mobile`: **All passed**. 210 = 200 session items + 10 sample items, with every session's files present.
- **Deck loop**, `scratchpad/s3/play-bank.mjs` (full path `/tmp/claude-0/-home-user-zero-to-quant/4b8cce5e-d242-5446-84a4-7179e480b15a/scratchpad/s3/play-bank.mjs`). It copies the `bankChecks` loop of `tools/playthrough.mjs` (`#bank`, `ZQ.test.continue()`, `answerCorrect()`, `check()`), at 390 x 844 with the local CDN routed. How it covers all 50:
  - it completes setup, then imports a save that marks the 19 `requires` lessons finished (locked count 86 before, 51 after: the 51 still locked belong to other sessions);
  - it schedules every foreign item 30 days away with four right `ZQ.state.bankResult` calls, so decks deal only session-3 items;
  - it wraps `ZQ.select.bankDeck` to record each dealt deck, so `current().screenIndex` names the item shown;
  - pass 0 answers every item right; passes 1 to 4 mark that pass's items missed, move the clock on 1.2 days, and answer each numeric `wrong` value (typed into the field, times 100 for `unit: "%"`) or each choice distractor (clicked) in turn.
  - Result: **50 of 50 items dealt and accepted** with the authored answer (8 longform included); **114 of 114** wrong ids and distractors routed, each returning its own key and showing its `byKey` or `why` text in the verdict; every `choice` showed exactly one correct option among its 4; all 13 choice items were seen in more than one option order; no console errors; no page wider than 390 px. Output at the end of this report.
- Screenshots: 92 at 390 px (pass 0 for every item, pass 1 for every first wrong route), looked at as contact sheets in `scratchpad/s3/sheets/`. No overlap, no clipped option, KaTeX readable (the telescoping sum, the ruin formula and the hats options all fit). Longform models scroll inside their box, as in session 1. No layout fault needed a fix.
- **Voice scan**, `VOICE_BASE=/home/user/zero-to-quant/app/content/bank/ python3 docs/reviews/voice-scan.py --summary`: **explanations over three sentences: 0; over 20 words: 0** (5,397 sentences across the whole folder). The first run found 5 long sentences in my files (two file descriptions, two prose lines and the ledger list), all fixed. A mid-session run also listed 15 long sentences in `*-4.json`; that session fixed them itself before my last run.
- No `!`, no em-dash or en-dash (asserted by `gen.py` on every item), British spelling, £ throughout, no firm names.

## Counts against the brief

- Per file: 14, 10, 10, 8, 8 (section 2).
- Per difficulty: D2 9, D3 21, D4 14, D5 6. Per kind: numeric 29, choice 13, longform 8, expression 0. Both match the session 3 row of section 2.
- Per family: as the session 3 column of section 3, except `3b02`, which is `weighing-heavy` instead of `weighing-scale` (below). `requires` on all 20 difficulty 4 and 5 items, on none below. Every `pace` is the table's value; the largest is 180 (`3p07`).
- Behavioural rubrics use the session 1 shape: six lines worth 2, 2, 2, 2, 1, 1, in the order direct answer, situation or substance, own actions, number or result, lesson or what would change it, length and clarity. Models are 137 to 153 words, in the first person of an invented candidate, with generic settings only.

## Items, refs and keys

| Ref | Id | Family | Kind | D | Pace | Key | `wrong` values |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3p01 | `dice-ev-middle-of-three` | dice-ev | numeric | 4 | 150 | 3.5 | 4.9583, 2.0417, 3 |
| 3p02 | `every-coupon-nine-stickers` | every-coupon | numeric | 3 | 120 | 25.4607 | 9, 81, 16.4607 |
| 3p03 | `at-least-one-signal-sixty-days` | at-least-one | numeric | 3 | 75 | 0.8392 | 1.8, 0.1608, 0.8347 |
| 3p04 | `hats-twelve-coats` | hats | choice | 4 | 150 | mean 1, variance 1 | 3 distractors |
| 3p05 | `waiting-for-hh-three-losing-days` | waiting-for-hh | numeric | 5 | 150 | 24.375 | 8.75, 15.625, 7.5 |
| 3p06 | `bayes-in-a-minute-good-day-signal` | bayes-in-a-minute | numeric | 4 | 120 | 0.4853 | 0.6875, 0.55, 0.3 |
| 3p07 | `ruin-in-interviews-three-to-nine` | ruin-in-interviews | numeric | 5 | 180 | 0.1624 | 0.3333, 0.5412, 0.0083 |
| 3p08 | `betting-on-sequences-htt-or-tth` | betting-on-sequences | numeric | 4 | 150 | 0.25 | 0.5, 0.75, 0.3333 |
| 3p09 | `kelly-five-to-two` | kelly | numeric | 4 | 120 | 0.09 | −0.3, 0.35, 0.225 |
| 3p10 | `when-to-hedge-small-bankroll` | when-to-hedge | choice | 4 | 100 | close below about £24 | 3 distractors |
| 3p11 | `doubling-up-cap-sixteen` | doubling-up | numeric | 4 | 120 | 0.038 | 0.0731, 0.03125, 0.0198 |
| 3p12 | `random-chords-midpoint-in-disc` | random-chords | numeric | 4 | 150 | 0.75 | 0.6667, 0.866, 0.25 |
| 3p13 | `expected-distance-squared-gap` | expected-distance | numeric | 3 | 120 | 1.5 | 1, 0.1667, 0.5 |
| 3p14 | `buffon-three-on-five` | buffon | numeric | 5 | 150 | 0.382 | 0.6, 0.191, 0.7639 |
| 3b01 | `hats-mod-k-six-prisoners` | hats-mod-k | choice | 5 | 150 | prisoner k aims at total k mod 6 | 3 distractors |
| 3b02 | `weighing-heavy-eight-one-light` | weighing-heavy | choice | 2 | 75 | 2 weighings, 3 against 3 | 3 distractors |
| 3b03 | `backward-induction-doubling-pot` | backward-induction | choice | 3 | 120 | take at once, £3 | 3 distractors |
| 3b04 | `scheduling-four-jobs-two-machines` | scheduling | numeric | 3 | 120 | 8 | 16, 11, 6 |
| 3b05 | `divisibility-one-to-ten` | divisibility | numeric | 2 | 60 | 2520 | 3628800, 5040, 1260 |
| 3b06 | `powers-of-two-eight-weeds` | powers-of-two | numeric | 2 | 60 | 21 | 3, 16 |
| 3b07 | `telescoping-ten-to-ninety-nine` | telescoping | numeric | 3 | 75 | 0.09 | 0.99, 0.1, 0.9 |
| 3b08 | `double-counting-eleven-guests` | double-counting | choice | 3 | 100 | no, parity of the degree sum | 3 distractors |
| 3b09 | `relative-speed-bird-between-trains` | relative-speed | numeric | 2 | 75 | 72 | 180, 360 |
| 3b10 | `constants-twenty-cubes` | constants | numeric | 3 | 75 | 44100 | 2870, 210 |
| 3m01 | `mental-arithmetic-73-by-28` | mental-arithmetic | numeric | 2 | 25 | 2044 | 2117, 1960 |
| 3m02 | `mental-arithmetic-4357-by-13` | mental-arithmetic | numeric | 3 | 30 | 335.2 | 335.1, 33.5 |
| 3m03 | `percent-chain-three-moves` | percent-chain | numeric (%) | 3 | 30 | 0.122 (12.2%) | 0.15, 0.02 |
| 3m04 | `fraction-odds-three-to-seven` | fraction-odds | numeric (%) | 2 | 20 | 0.7 (70%) | 0.3, 0.4286 |
| 3m05 | `estimate-product-three-factors` | estimate-product | choice | 3 | 30 | 310 | 3 distractors |
| 3m06 | `sequence-woven-two-doublings` | sequence-woven | numeric | 4 | 35 | 16 | 80, 48 |
| 3m07 | `sqrt-newton-eleven` | sqrt-newton | numeric | 4 | 40 | 3.32 | 3.33, 3.3 |
| 3m08 | `word-time-crew-days` | word-time | choice | 3 | 40 | 15 days, then 30 | 3 distractors |
| 3m09 | `net-score-eighty-questions` | net-score | numeric | 2 | 20 | 52 | 63, 46 |
| 3m10 | `ranking-five-mixed-forms` | ranking | choice | 4 | 45 | A, D, B, C, E | 3 distractors |
| 3k01 | `card-fair-heart-and-club-shown` | card-fair | numeric | 3 | 90 | 14.8 | 15, 14.7059, 10, 4.8 |
| 3k02 | `fermi-error-divisor-low` | fermi-error | choice | 2 | 60 | twice too high | 3 distractors |
| 3k03 | `intervals-heads-in-100` | intervals | choice | 3 | 75 | 40 to 60 | 3 distractors |
| 3k04 | `coverage-twelve-of-twenty` | coverage | choice | 3 | 75 | widen | 3 distractors |
| 3k05 | `quote-centre-per-lot` | quote-centre | numeric | 3 | 75 | 49.04 | 48.8, 49.76 |
| 3k06 | `ledger-pnl-five-trades` | ledger-pnl | numeric | 3 | 100 | 26 | −17, 27 |
| 3k07 | `hedge-ratio-five-baskets` | hedge-ratio | numeric | 2 | 60 | 15 | 3, 9.6 |
| 3k08 | `thinking-aloud-own-name` | thinking-aloud | choice | 3 | 75 | clarify, then quote tight | 3 distractors |
| 3h01 | `star-story-disagreed-with-senior` | star-story | longform | 4 | 150 | model and rubric | |
| 3h02 | `star-story-incomplete-information` | star-story | longform | 4 | 150 | model and rubric | |
| 3h03 | `star-story-failing-team` | star-story | longform | 3 | 150 | model and rubric | |
| 3h04 | `why-us-first-six-months` | why-us | longform | 5 | 120 | model and rubric | |
| 3h05 | `video-answer-biggest-strength` | video-answer | longform | 3 | 120 | model and rubric | |
| 3h06 | `final-round-stumped` | final-round | longform | 4 | 150 | model and rubric | |
| 3h07 | `cv-lines-weakest-line` | cv-lines | longform | 3 | 150 | model and rubric | |
| 3h08 | `reasoning-aloud-coffee-estimate` | reasoning-aloud | longform | 5 | 150 | model and rubric | |

Numeric keys with a stated rounding accept that rounding: 25.46, 24.37 or 24.38, 0.1624, 0.0380, 0.3820, 14.80, 3.32 (3.3167 also), 12.2 typed into a `%` field, and the exact fractions 7129/280, 195/8, 33/68, 1/4, 3/4 and 9/100. Every `wrong` band lies outside the key band and outside every other band (`gen.py` asserts it).

## Changes from the session 3 table

For rule 10 (a course, exam or bank item with the same structure and numbers), found by grep of `courses/`, `exams/` and `bank/` (including the session 2 and 4 files as they appeared):

1. `3p02`: 6 stickers → 9 stickers (25.46). `puzzles/l2` works the die (14.7), and its quiz uses 4 suits and 10 toys; `sample.json` uses 12 months; `1p03` uses 8 faces.
2. `3p04`: eight guests → twelve coats. `puzzles/l5` quiz 0 is eight people in eight seats, expected 1.
3. `3p05`: two losing days in a row at 0.4 → **three** losing days in a row at 0.4 (24.375). `puzzles/l3` screen 9 is the two-day version (8.75), as the session 1 note said.
4. `3p08`: idea swapped within `puzzles/l20` (rule: same family, kind and difficulty). The briefed "Kelly growth of a 0.6 coin" is `puzzles/l21` screen 2 (0.0201) word for word, and it is a Kelly item under the `betting-on-sequences` family, which `puzzles/l20` uses for pattern races. The item is now a race, HTT against TTH on a fair coin: TTH first with chance 1/4. `puzzles/l20` races HH/TH, HHT/THH, HHT/HTH and HHT/HTT; none uses this pair.
5. `3p09`: 2 to 1 at 0.4 → 5 to 2 at 0.35 (f* = 0.09). `puzzles/l21` screen 7 is 2 to 1 at 0.4 (0.1); l21's drill, `game-theory` l15 and review 3, and `mm-games` l18 use 3 to 1, 4 to 1 and 2 to 1 bets. Section 6 asked for a different bet.
6. `3p11`: the brief gave no win chance; I set 0.48 (course uses a fair coin and European red, 18/37).
7. `3p12`: two random endpoints → a uniform midpoint in the disc, same threshold (the radius). `puzzles/l29` quiz 1 is exactly the endpoints and radius case (2/3). The midpoint and radius pair (3/4) appears nowhere.
8. `3p13`: unit segment → a 3 km road (1.5), so the scaling is the twist; `puzzles/l18` uses [0, 1] and [0, 6] for the plain distance.
9. `3b01`: five prisoners mod 5 → six prisoners mod 6. `brainteasers/homework-2` item 4 is five people with hats 0 to 4 and the mod-5 rule; `brainteasers/l7` uses seven.
10. `3b02`: nine coins, one lighter → eight coins, one lighter (first split 3, 3, 2). `brainteasers/l4` screens 0 and 4 are nine coins.
11. `3b06`: full on day 30 → day 24 with eight weeds (day 21). No course hit, but the briefed numbers give 28 for both the quarter-full day and the four-weed day, so the two readings could not be told apart.
12. `3b07`: 1/(k(k+1)) for k = 1 to 99 → k = 10 to 99 (0.09). `brainteasers/l14` sums to 49 (0.98) and from 2·3 to 9·10.
13. `3m02`: 4,355 ÷ 13 → 4,357 ÷ 13. Not a duplicate: 4,355/13 is exactly 335, which leaves nothing to round to one decimal place.
14. `3m03`: +10%, −10%, +10% → +20%, −15%, +10% (+12.2%). `mental-pressure/l6` shows 1.1 × 0.9 × 1.1 = 1.089 in its table (row 9).
15. `3m04`: "3 to 7 against" → "odds of 3 to 7: a £7 stake wins £3 profit". "3 to 7 against" is odds-on written backwards and reads both ways; the stake form is the `mental-pressure/l5` convention.
16. `3m09`: 61 right, 14 wrong, 5 skipped → 63, 11, 6 (net 52). `mental-pressure/l12` has 60 right, 14 wrong and 6 blank (46); l13 has 58 right and 14 wrong.
17. `3k01`: one heart shown → a heart and a club shown (£14.80). Session 2's `2k01`, written in parallel, reveals one heart from three cards; two reveals keep the two items apart.
18. `3k04`: opening reworded ("In a practice week") so it does not read like session 4's `4k08` (60 ranges at 90%, 45 held). Numbers differ.

Readings of loose ideas (not duplicates): `3p10` asks below which bankroll a sure £0.50 beats holding the +£6 or −£4 position under the log rule (W < 24.25); `3k05` gives 5 lots for the move from 50 to 49.4 and asks the value after 3 more lots (49.04); `3k06` invents the five-trade ledger and asks the P&L (the losing trade is named in the explanation); `3k07` holds 5 baskets (sell 15); `3b03` sets the pot game as £4 doubling, a 3/4 take, and an equal split if round 3 passes.

**Family changed:** `3b02` is tagged `weighing-heavy`, not `weighing-scale`. In the courses `weighing-scale` is the digital-scale bag puzzle (`brainteasers/l4` screen 10 and `review-1` `r8-ten-bags`), while every balance item with one odd coin of known direction is `weighing-heavy`. The brief says to use the nearest existing tag in that case. So session 3 has no `weighing-scale` item and one more `weighing-heavy`.

The five closest course items found (acceptance 6), with what changed: `puzzles/l3` screen 9 (two losing days at 0.4) → three days; `puzzles/l21` screen 7 (2 to 1 at 0.4) → 5 to 2 at 0.35; `puzzles/l29` quiz 1 (endpoints, longer than the radius) → midpoint in the disc; `brainteasers/homework-2` item 4 (five hats mod 5) → six mod 6; `mental-pressure/l6` row 9 (+10, −10, +10) → +20, −15, +10.

## Every number, two ways

Method A is the closed form or the stated working; method B is enumeration, a linear solve, a search, a grid integral or a seeded simulation (seed 20261103). `bank-1-3.py` asserts every pair; its output is below.

| Ref | Key | Method A | Method B |
| --- | --- | --- | --- |
| 3p01 | 7/2 | symmetry x → 7 − x | enumerate 216 rolls (756/216); simulation 3.50 |
| 3p02 | 7129/280 | 9H₉ | first-step recursion on stickers held; simulation 25.47 |
| 3p03 | 0.8392 | 1 − 0.97⁶⁰ | 1 − e^(60 ln 0.97); simulation 0.840 |
| 3p04 | 1 and 1 | indicators: E[X²] = 1 + 132 × 1/132 | enumerate all 5,040 orders of 7; simulation of 12: 1.00 and 0.997 |
| 3p05 | 195/8 | (1 − p³)/(q p³) | first-step equations solved exactly; simulation 24.37 |
| 3p06 | 33/68 | Bayes in chances | counts per 1,000 days, 165/340; simulation 0.4845 |
| 3p07 | 0.162356 | (1 − r³)/(1 − r⁹), r = 11/9 | linear recurrence by shooting; simulation 0.1614 |
| 3p08 | 1/4 | first two flips TT | first-step equations on joint states; Conway numbers; simulation 0.2504 |
| 3p09 | 0.09 | p − q/b | grid maximum of the log growth |
| 3p10 | W < 24.25 | (W + 6)(W − 4) = (W + 0.5)² | bisection on the log rule |
| 3p11 | 0.038020 | 0.52⁵ | simulation 0.03805 |
| 3p12 | 3/4 | (√3/2)² | simulation of uniform midpoints 0.7497 |
| 3p13 | 3/2 | Var X + Var Y = 2 × 9/12 | midpoint grid 600 × 600; simulation 1.503 |
| 3p14 | 6/(5π) | 2l/(πd) | integral of min(2.5, 1.5 sin θ); simulation 0.3825 |
| 3b01 | one right always | remainder argument | all 46,656 hat patterns checked; counterexamples for the three wrong plans |
| 3b02 | 2 | ⌈log₃ 8⌉ | minimax recursion over splits (4 against 4 needs 3) |
| 3b03 | Ann takes £3 | backward induction by hand (12 > 8, 6 > 4, 3 > 2) | recursive solver |
| 3b04 | 8 | 16/2 lower bound met | search of all 16 assignments; in-order greedy gives 11 |
| 3b05 | 2520 | 2³ × 3² × 5 × 7 | `math.lcm`; first n found by search |
| 3b06 | 21 | 24 − log₂ 8 | first day with 8 × 2^d ≥ 2²⁴ |
| 3b07 | 9/100 | 1/10 − 1/100 | Fraction sum of 90 terms |
| 3b08 | impossible | handshake lemma | 11 × 5 = 55 odd, checked |
| 3b09 | 72 | 60 × 90/75 | stepped zigzag at dt = 10⁻⁵ h |
| 3b10 | 44,100 | 210² | sum of 20 cubes |
| 3m01 | 2044 | 73 × 30 − 146 | 70 × 28 + 3 × 28 |
| 3m02 | 335.2 | 335 + 2/13 | Fraction 4357/13 rounded |
| 3m03 | +12.2% | 1.2 × 0.85 × 1.1 − 1 | step by step from £100 |
| 3m04 | 70% | 7/(3 + 7) | zero expected profit at 0.7 |
| 3m05 | 310 | 6.82 × 14.7 × 3.1 = 310.79 | 100.254 × 3.1; options 285.6 and 336 more than 3% off |
| 3m06 | 16 | odd strand doubles | strands listed |
| 3m07 | 3.32 | (3.3 + 11/3.3)/2 = 3.3167 | Newton form 3.3 + (11 − 10.89)/6.6; √11 = 3.3166 |
| 3m08 | 15 and 30 | 60 person-days / 4, then / 2 a day | Fraction check |
| 3m09 | 52 | 63 − 11 | 63 + 11 + 6 = 80 checked; accuracy 63/74 = 85% |
| 3m10 | A, D, B, C, E | exact Fraction sort | cross products (85 against 84) |
| 3k01 | £14.80 | 10 × (1 + 2 × 12/50) | enumerate all 1,225 pairs of the 50 cards left |
| 3k02 | × 2 | halving a divisor | numeric check |
| 3k03 | 40 to 60 | exact binomial: 96.48%; 41 to 59 holds 94.31% | simulation 0.9650; normal 50 ± 9.8 |
| 3k04 | widen | 12/20 = 60% | P(at most 12 of 20 at 0.8) = 0.0321 exact; simulation 0.0321 |
| 3k05 | 49.04 | 49.4 − 3 × 0.12 | 50 − 8 × 0.12 |
| 3k06 | 26 | each trade at the mark (+3, +10, +8, +6, −1) | cash −17 plus long 1 at 43 |
| 3k07 | 15 | 5 × 2.4 / 0.8 | exposure 12 − 15 × 0.8 = 0 |
| 3h08 | figures in the model | 67m × 0.6 × 0.5 × 2 ≈ 40m | 10m / 30,000 ≈ 333 a shop |

Every numeric `wrong` value is a named slip computed in the script from that slip (for example (1 − ρ³)/(1 − ρ⁹) with ρ = p/q for "flipped the ratio", 0.52⁴ for "stopped at the £8 stake", 10 × (1 + 2 × 12/51) for "took only the heart out").

## Proposals (not edited)

- `brainteasers/homework-2` item 4 (five people, hats 0 to 4, person i assumes the total is i modulo 5) carries `hats-simultaneous`, but it is the modulo strategy that `hats-mod-k` names. Retagging it `hats-mod-k` would deal it with `3b01`.
- The brief's section 3 table should list `3b02` under `weighing-heavy`, or the idea should become a digital-scale bag puzzle if a `weighing-scale` bank item is wanted.
- No `course.json` change.

## Open questions

1. Is `weighing-heavy` the right family for `3b02`, or should a later session add a digital-scale item for `weighing-scale`?
2. `3p08` swapped a Kelly-growth idea for a pattern race to keep `betting-on-sequences` meaning what `puzzles/l20` means by it. Is that the intended reading of the family?
3. `3p01` uses `dice-ev` while drawing on `puzzles/l11`; session 1's open question on `dice-ev` against `dice-games` still stands.

## Inbox

Three bullets under `Bank session 3 (3 Nov)` at the end of `docs/BACKLOG-INBOX.md`.

## Scripts

`scratchpad/s3/bank-1-3/` holds `bank-1-3.py` (numbers, below) and `gen.py`, which builds the five files from item data and asserts: one correct option of 3 or 4, the rubric shape 2, 2, 2, 2, 1, 1, models of 120 to 180 words, `requires` only at D4 and D5, `pace` at most 180, ids prefixed by their family and unique, no `!` or dashes, and no `wrong` band touching the key band or another band. `scratchpad/s3/play-bank.mjs` is the deck loop; `scratchpad/s3/sheets/` holds the contact sheets of the 390 px screenshots.

### `bank-1-3.py`

```python
"""Bank part 1, session 3: every keyed answer and every numeric wrong value, two ways each, with asserts.
Writes nothing. Run: python3 bank-1-3.py"""
from fractions import Fraction as F
from itertools import product, permutations
from math import comb, log, exp, pi, sqrt, acos
import random, math
rng = random.Random(20261103)
OUT = []
def rec(ref, name, a, b, tol=0):
    a_, b_ = float(a), float(b)
    assert abs(a_ - b_) <= tol, (ref, name, a_, b_)
    OUT.append(f'{ref:5} {name:38} {a_:14.6f}  check {b_:14.6f}')
def sim(f, n=200000):
    return sum(f() for _ in range(n)) / n

# ---------- probability-3 ----------
# 3p01 middle of three d6
mids = [sorted(r)[1] for r in product(range(1, 7), repeat=3)]
emid = F(sum(mids), 216)
rec('3p01', 'E middle of three d6 (enum)', emid, F(7, 2))          # symmetry x -> 7 - x
rec('3p01', 'sim', 3.5, sim(lambda: sorted(rng.randint(1, 6) for _ in range(3))[1]), 0.02)
emax = F(sum(max(r) for r in product(range(1, 7), repeat=3)), 216)
rec('3p01', 'wrong largest 119/24', emax, F(sum(1 - F(k - 1, 6) ** 3 for k in range(1, 7))))
emin = F(sum(min(r) for r in product(range(1, 7), repeat=3)), 216)
rec('3p01', 'wrong smallest 49/24', emin, 7 - emax)
rec('3p01', 'wrong continuous 3', F(6) * F(2, 4), 3)               # uniform on [0, 6]: E[2nd of 3] = 6 * 2/4
# 3p02 coupon collector, 9 stickers
H = lambda n: sum(F(1, k) for k in range(1, n + 1))
def coupon_lin(n):
    E = F(0)
    for k in range(n - 1, -1, -1): E = (1 + F(n - k, n) * E) / (1 - F(k, n))
    return E
rec('3p02', '9 H9 = 7129/280', 9 * H(9), coupon_lin(9))
def coup_sim(n):
    seen, c = set(), 0
    while len(seen) < n: seen.add(rng.randrange(n)); c += 1
    return c
rec('3p02', 'sim', 9 * H(9), sim(lambda: coup_sim(9), 100000), 0.1)
rec('3p02', 'last sticker alone 9', F(9, 1), 1 / F(1, 9))
rec('3p02', 'wrong left out last 16.4607', 9 * H(9) - 9, 9 * (H(9) - 1))
rec('3p02', 'wrong n^2 81', 81, 9 * 9)
# 3p03 at least one fire in 60 days at 3%
p3 = 1 - 0.97 ** 60
rec('3p03', '1 - 0.97^60', p3, 1 - exp(60 * log(0.97)), 1e-12)
rec('3p03', 'sim', p3, sim(lambda: any(rng.random() < 0.03 for _ in range(60)), 100000), 0.005)
rec('3p03', 'wrong added 1.8', 60 * 0.03, 1.8, 1e-12)
rec('3p03', 'wrong none 0.1608', 0.97 ** 60, 1 - p3, 1e-12)
rec('3p03', 'wrong Poisson 0.8347', 1 - exp(-1.8), 1 - math.e ** -1.8, 1e-12)
print('3p03 key 4dp', round(p3, 4))
# 3p04 twelve coats: mean and variance of matches (choice); enumerate n = 7 fully, formula for 12
def match_moments(n):
    c = [sum(1 for i in range(n) if s[i] == i) for s in permutations(range(n))]
    m = F(sum(c), len(c)); v = F(sum(x * x for x in c), len(c)) - m * m
    return m, v
m7, v7 = match_moments(7)
rec('3p04', 'mean n=7 by enumeration', m7, 1); rec('3p04', 'var n=7 by enumeration', v7, 1)
n = 12
mean12 = n * F(1, n)
ex2 = mean12 + n * (n - 1) * F(1, n * (n - 1))                     # E[X^2] = sum E[I_i] + sum_{i!=j} E[I_i I_j]
rec('3p04', 'mean n=12 indicators', mean12, 1)
rec('3p04', 'var n=12 indicators', ex2 - mean12 ** 2, 1)
def match_sim(n):
    s = list(range(n)); rng.shuffle(s); return sum(s[i] == i for i in range(n))
xs = [match_sim(12) for _ in range(100000)]
mu = sum(xs) / len(xs); var = sum((x - mu) ** 2 for x in xs) / len(xs)
rec('3p04', 'sim mean', 1, mu, 0.02); rec('3p04', 'sim var', 1, var, 0.03)
rec('3p04', 'option binomial var 11/12', n * F(1, n) * F(n - 1, n), F(11, 12))
rec('3p04', 'option one guest 1/12, 11/144', F(1, 12) * F(11, 12), F(11, 144))
rec('3p04', 'option E[X^2] = 2', ex2, 2)
# 3p05 three losing days in a row, loss chance 0.4
def wait_run(p, k):
    """first-step equations E_j = 1 + p E_{j+1} + q E_0, E_k = 0, solved exactly by substitution E_j = a_j + b_j E_0"""
    q = 1 - p
    a, b = F(0), F(0)                       # E_k = 0
    for j in range(k - 1, -1, -1):
        a, b = 1 + p * a, p * b + q          # E_j = 1 + p E_{j+1} + q E_0
    return a / (1 - b)
p = F(2, 5)
rec('3p05', 'E three in a row (states)', wait_run(p, 3), (1 - p ** 3) / ((1 - p) * p ** 3))
rec('3p05', 'closed (1+p+p^2)/p^3 = 24.375', (1 + p + p * p) / p ** 3, F(195, 8))
def run_sim(p, k):
    c = r = 0
    while r < k:
        c += 1; r = r + 1 if rng.random() < p else 0
    return c
rec('3p05', 'sim', F(195, 8), sim(lambda: run_sim(0.4, 3), 100000), 0.2)
rec('3p05', 'wrong two in a row 8.75', wait_run(p, 2), (1 + p) / p ** 2)
rec('3p05', 'wrong 1/p^3 15.625', 1 / p ** 3, F(125, 8))
rec('3p05', 'wrong 3/p 7.5', 3 / p, F(15, 2))
# 3p06 Bayes: fires on 55% good, 25% bad, good 30%
post = F(55, 100) * F(30, 100) / (F(55, 100) * F(30, 100) + F(25, 100) * F(70, 100))
rec('3p06', 'P(good | fire) = 33/68', post, F(165, 340))          # counts per 1,000 days: 165 of 340
def bayes_sim():
    g = rng.random() < 0.3; fire = rng.random() < (0.55 if g else 0.25)
    return (g, fire)
s = [bayes_sim() for _ in range(300000)]
rec('3p06', 'sim', post, sum(1 for g, f in s if g and f) / sum(1 for g, f in s if f), 0.006)
print('3p06 key 4dp', round(float(post), 4))
rec('3p06', 'wrong no base rate 0.6875', F(55, 80), F(11, 16))
rec('3p06', 'wrong hit rate 0.55', F(55, 100), 0.55)
rec('3p06', 'wrong base rate 0.3', F(3, 10), 0.3)
# 3p07 ruin p = 0.45 from 3 to 9
def ruin_lin(k, N, p):
    """solve P_j = p P_{j+1} + q P_{j-1}, P_0 = 0, P_N = 1 by shooting: P_1 = x, linear in x"""
    q = 1 - p
    P = [F(0), F(1)]
    for j in range(1, N): P.append((P[j] - q * P[j - 1]) / p)
    return P[k] / P[N]
p = F(9, 20); r = (1 - p) / p
closed = (1 - r ** 3) / (1 - r ** 9)
rec('3p07', 'reach 9 from 3 at 0.45', closed, ruin_lin(3, 9, p))
def ruin_sim(k, N, p):
    while 0 < k < N: k += 1 if rng.random() < p else -1
    return k == N
rec('3p07', 'sim', closed, sim(lambda: ruin_sim(3, 9, 0.45), 200000), 0.004)
print('3p07 key 4dp', round(float(closed), 4))
rec('3p07', 'wrong fair 1/3', F(3, 9), ruin_lin(3, 9, F(1, 2)))
rp = p / (1 - p)
rec('3p07', 'wrong r = p/q 0.5412', (1 - rp ** 3) / (1 - rp ** 9), ruin_lin(3, 9, 1 - p) * 0 + (1 - rp ** 3) / (1 - rp ** 9))
rec('3p07', 'wrong r = p/q equals reaching 9 from 3 at p = 0.55', (1 - rp ** 3) / (1 - rp ** 9), ruin_lin(3, 9, F(11, 20)))
rec('3p07', 'wrong six straight wins 0.0083', p ** 6, F(9, 20) ** 6)
# 3p08 Penney race HTT against TTH, fair coin: chance TTH first
def race(a, b, p=F(1, 2)):
    """first-step equations on the longest suffix that is a prefix of a or b; solved by Gaussian elimination"""
    states = sorted({a[:i] for i in range(len(a))} | {b[:i] for i in range(len(b))}, key=len)
    idx = {s: i for i, s in enumerate(states)}
    def nxt(s, c):
        t = s + c
        if t.endswith(a): return 'A'
        if t.endswith(b): return 'B'
        for j in range(len(t), -1, -1):
            if t[len(t) - j:] in idx: return t[len(t) - j:]
    m = len(states); A = [[F(0)] * m for _ in range(m)]; rhs = [F(0)] * m
    for s in states:
        i = idx[s]; A[i][i] += 1
        for c, pr in (('H', p), ('T', 1 - p)):
            t = nxt(s, c)
            if t == 'B': rhs[i] += pr
            elif t != 'A': A[i][idx[t]] -= pr
    for i in range(m):
        piv = A[i][i]
        A[i] = [x / piv for x in A[i]]; rhs[i] /= piv
        for r_ in range(m):
            if r_ != i and A[r_][i] != 0:
                f_ = A[r_][i]; A[r_] = [x - f_ * y for x, y in zip(A[r_], A[i])]; rhs[r_] -= f_ * rhs[i]
    return rhs[idx['']]                                              # chance b comes first
def conway(x, y):
    return sum(2 ** (k - 1) for k in range(1, 4) if x[-k:] == y[:k])
A_, B_ = 'HTT', 'TTH'
odds_b = F(conway(A_, A_) - conway(A_, B_), conway(B_, B_) - conway(B_, A_))   # P(B first) / P(A first)
rec('3p08', 'P(TTH first) linear solve', race(A_, B_), odds_b / (1 + odds_b))
rec('3p08', 'P(TTH first) = first two flips TT', race(A_, B_), F(1, 4))
def race_sim(a, b):
    s = ''
    while True:
        s += 'H' if rng.random() < 0.5 else 'T'
        if s.endswith(a): return 0
        if s.endswith(b): return 1
rec('3p08', 'sim', F(1, 4), sim(lambda: race_sim(A_, B_), 100000), 0.006)
rec('3p08', 'wrong HTT chance 0.75', 1 - race(A_, B_), F(3, 4))
rec('3p08', 'wrong odds ratio 1/3', odds_b, F(1, 3))
# 3p09 Kelly, pays 5 to 2, wins 0.35
p, b = F(35, 100), F(5, 2)
fk = p - (1 - p) / b
def growth(f): return float(p) * log(1 + float(b) * f) + float(1 - p) * log(1 - f)
fgrid = max((i / 100000 for i in range(0, 40000)), key=growth)
rec('3p09', 'Kelly fraction 0.09', fk, fgrid, 1e-4)
rec('3p09', 'edge per £1 0.225 > 0', p * b - (1 - p), F(9, 40))
rec('3p09', 'wrong p - q -0.3', p - (1 - p), F(-3, 10))
rec('3p09', 'wrong staked p 0.35', p, 0.35)
rec('3p09', 'wrong edge 0.225', p * b - (1 - p), 0.225)
# 3p10 hedge: +6 or -4 at evens, or close now for +0.50; log rule threshold
def prefers_close(W): return log(W + 0.5) > 0.5 * log(W + 6) + 0.5 * log(W - 4)
lo, hi = 4.0001, 1000.0
for _ in range(200):
    mid = (lo + hi) / 2
    if prefers_close(mid): lo = mid
    else: hi = mid
rec('3p10', 'threshold W by bisection', F(97, 4), lo, 1e-6)        # (W+6)(W-4) = (W+0.5)^2 gives W = 24.25
assert prefers_close(20) and not prefers_close(30)
rec('3p10', 'EV of holding 1', F(1, 2) * 6 + F(1, 2) * -4, 1)
rec('3p10', 'certainty equivalent at W=20', sqrt(26 * 16) - 20, 0.396, 0.001)
rec('3p10', 'certainty equivalent at W=100', sqrt(106 * 96) - 100, 0.876, 0.001)
# 3p11 doubling 1, 2, 4, 8, 16 at win chance 0.48: lose all five
q = F(52, 100)
rec('3p11', 'lose five in a row', q ** 5, F(52 ** 5, 100 ** 5))
rec('3p11', 'sim', q ** 5, sim(lambda: all(rng.random() >= 0.48 for _ in range(5)), 400000), 0.0015)
print('3p11 key 4dp', round(float(q ** 5), 4))
rec('3p11', 'stakes to the cap', sum(2 ** i for i in range(5)), 31)
rec('3p11', 'wrong four bets 0.0731', q ** 4, F(52, 100) ** 4)
rec('3p11', 'wrong fair coin 0.0313', F(1, 2) ** 5, F(1, 32))
rec('3p11', 'wrong six bets 0.0198', q ** 6, F(52, 100) ** 6)
# 3p12 chord by uniform midpoint in the unit disc: longer than the radius
# length 2 sqrt(1 - d^2) > 1  <=>  d < sqrt(3)/2 ; P = (sqrt(3)/2)^2
key12 = (sqrt(3) / 2) ** 2
def chord_mid():
    while True:
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y < 1: return 2 * sqrt(1 - x * x - y * y) > 1
rec('3p12', 'midpoint method 3/4', key12, 0.75, 1e-12)
rec('3p12', 'sim', 0.75, sim(chord_mid, 200000), 0.004)
def chord_end():
    a, b = rng.uniform(0, 2 * pi), rng.uniform(0, 2 * pi)
    return 2 * abs(math.sin((a - b) / 2)) > 1
rec('3p12', 'wrong endpoints 2/3 (sim)', F(2, 3), sim(chord_end, 200000), 0.004)
rec('3p12', 'wrong radius point sqrt(3)/2', sqrt(3) / 2, 0.8660, 0.0001)
rec('3p12', 'wrong shorter 1/4', 1 - key12, 0.25, 1e-12)
# 3p13 E[(X - Y)^2] for two uniforms on [0, 3]
L = 3
rec('3p13', 'E sq distance L^2/6 = 1.5', F(L * L, 6), 2 * F(L * L, 12))      # Var X + Var Y
grid = 600
acc = sum(((i + 0.5) / grid * L - (j + 0.5) / grid * L) ** 2 for i in range(grid) for j in range(grid)) / grid ** 2
rec('3p13', 'midpoint grid', 1.5, acc, 1e-4)
rec('3p13', 'sim', 1.5, sim(lambda: (rng.uniform(0, 3) - rng.uniform(0, 3)) ** 2), 0.02)
rec('3p13', 'wrong E|X-Y| = 1', F(L, 3), 1)
rec('3p13', 'wrong unscaled 1/6', F(1, 6), 0.1667, 0.0001)
rec('3p13', 'wrong scaled by L once 0.5', F(L, 6), 0.5)
# 3p14 Buffon, needle 3, lines 5 apart
key14 = 2 * 3 / (pi * 5)
def buffon():
    yc = rng.uniform(0, 2.5); th = rng.uniform(0, pi / 2)
    return yc < 1.5 * math.sin(th)
rec('3p14', '2l/(pi d)', key14, 6 / (5 * pi), 1e-12)
N_ = 2000
area = sum(min(2.5, 1.5 * math.sin((i + 0.5) / N_ * pi / 2)) for i in range(N_)) / N_ / 2.5
rec('3p14', 'integral of crossing region', key14, area, 1e-5)
rec('3p14', 'sim', key14, sim(buffon, 400000), 0.003)
print('3p14 key 4dp', round(key14, 4))
rec('3p14', 'wrong l/d 0.6', F(3, 5), 0.6)
rec('3p14', 'wrong dropped the 2 0.1910', 3 / (5 * pi), key14 / 2, 1e-12)

# ---------- brainteasers-3 ----------
# 3b01 hats mod 6: prisoner k aims for total = k (mod 6): exactly one right on every pattern
for hats in product(range(6), repeat=6):
    right = sum(1 for k in range(6) if (k - (sum(hats) - hats[k])) % 6 == hats[k])
    assert right == 1
    same = sum(1 for k in range(6) if (0 - (sum(hats) - hats[k])) % 6 == hats[k])
    assert same in (0, 6)
rec('3b01', 'all 46,656 patterns: exactly one right', 1, 1)
bad = (1, 2, 3, 4, 5, 0)
rec('3b01', 'guess own index: all wrong on 1,2,3,4,5,0', sum(1 for k in range(6) if bad[k] == k), 0)
crowd = (0, 0, 1, 1, 2, 2)
def most_seen(k):
    from collections import Counter
    c = Counter(crowd[:k] + crowd[k + 1:]); top = max(c.values())
    return {v for v, n in c.items() if n == top}
rec('3b01', 'crowd rule: every guess wrong on 0,0,1,1,2,2', sum(1 for k in range(6) if crowd[k] in most_seen(k)), 0)
# 3b02 eight coins, one lighter: minimax weighings over splits
from functools import lru_cache
@lru_cache(None)
def W(n):
    if n <= 1: return 0
    best = 99
    for a in range(1, n // 2 + 1):
        rest = n - 2 * a
        best = min(best, 1 + max(W(a), W(rest)))
    return best
rec('3b02', 'eight coins: 2 weighings', W(8), math.ceil(log(8, 3)))
assert 1 + max(W(3), W(2)) == 2 and 1 + max(W(4), W(0)) == 3
rec('3b02', 'halving 4 v 4 needs 3', 1 + max(W(4), W(0)), 3)
# 3b03 pot of £4 doubling each pass; mover takes 3/4; split at the end
def solve_pot(pot, rnd, last=3):
    mover = 0 if rnd % 2 == 1 else 1
    take = [0, 0]; take[mover] = F(3, 4) * pot; take[1 - mover] = F(1, 4) * pot
    if rnd == last:
        cont = [pot / 2, pot / 2]                    # pass in the last round: the pot is split equally
    else:
        cont = solve_pot(2 * pot, rnd + 1, last)
    return take if take[mover] >= cont[mover] else cont
rec('3b03', 'A takes at once: A gets 3', solve_pot(F(4), 1)[0], 3)
rec('3b03', 'B would get 1', solve_pot(F(4), 1)[1], 1)
rec('3b03', 'round 3 take 12 vs split 8', F(3, 4) * 16, 12)
rec('3b03', 'round 2: B takes 6 vs 4 after A takes in round 3', F(3, 4) * 8, 6)
rec('3b03', 'wrong: pass to round 3 and take 12', solve_pot(F(16), 3)[0], 12)
# 3b04 jobs 3, 5, 2, 6 on two machines
jobs = [3, 5, 2, 6]
best = min(max(sum(j for j, s in zip(jobs, a) if s), sum(j for j, s in zip(jobs, a) if not s)) for a in product([0, 1], repeat=4))
rec('3b04', 'makespan by search', best, sum(jobs) / 2)
loads = [0, 0]
for j in jobs: loads[loads.index(min(loads))] += j
rec('3b04', 'wrong greedy in given order 11', max(loads), 11)
rec('3b04', 'wrong serial 16', sum(jobs), 16)
# 3b05 lcm 1..10
rec('3b05', 'lcm 1..10', math.lcm(*range(1, 11)), 2 ** 3 * 3 ** 2 * 5 * 7)
rec('3b05', 'smallest by search', next(n for n in range(1, 10 ** 5) if all(n % k == 0 for k in range(1, 11))), 2520)
rec('3b05', 'wrong 2^4 5040', 2 ** 4 * 9 * 5 * 7, 5040)
rec('3b05', 'wrong 2^2 1260', 2 ** 2 * 9 * 5 * 7, 1260)
rec('3b05', 'wrong 10! 3628800', math.factorial(10), 3628800)
assert 1260 % 8 != 0
# 3b06 one weed fills the pond on day 24; start with eight
day = next(d for d in range(0, 30) if 8 * 2 ** d >= 2 ** 24)
rec('3b06', 'eight weeds: day', day, 24 - 3)
rec('3b06', 'wrong 24/8', F(24, 8), 3)
rec('3b06', 'wrong 24-8', 24 - 8, 16)
# 3b07 sum 1/(k(k+1)) for k = 10..99
t7 = sum(F(1, k * (k + 1)) for k in range(10, 100))
rec('3b07', 'sum k=10..99', t7, F(1, 10) - F(1, 100))
rec('3b07', 'wrong from k=1 0.99', sum(F(1, k * (k + 1)) for k in range(1, 100)), F(99, 100))
rec('3b07', 'wrong 1/10 only', F(1, 10), 0.1)
rec('3b07', 'wrong 1 - 1/10', 1 - F(1, 10), 0.9)
# 3b08 handshake parity: degree sum is even, 11 odd degrees sum to odd
rec('3b08', '11 x 5 = 55 is odd', 11 * 5 % 2, 1)
# 3b09 trains 90 miles apart at 30 and 45 mph, bird at 60
t9 = F(90, 30 + 45)
rec('3b09', 'bird distance 72', 60 * t9, 72)
pos_a, pos_b, bird, dist, dt = 0.0, 90.0, 0.0, 0.0, 1e-5           # step the zigzag
dirn = 1
while pos_b - pos_a > 1e-9:
    pos_a += 30 * dt; pos_b -= 45 * dt
    bird += dirn * 60 * dt; dist += 60 * dt
    if dirn == 1 and bird >= pos_b: dirn = -1
    elif dirn == -1 and bird <= pos_a: dirn = 1
rec('3b09', 'stepped zigzag', 72, dist, 0.01)
rec('3b09', 'wrong slower train 180', 60 * F(90, 30), 180)
rec('3b09', 'wrong speed difference 360', 60 * F(90, 45 - 30), 360)
# 3b10 sum of first 20 cubes
rec('3b10', 'sum cubes 1..20', sum(k ** 3 for k in range(1, 21)), (20 * 21 // 2) ** 2)
rec('3b10', 'wrong squares 2870', sum(k * k for k in range(1, 21)), 20 * 21 * 41 // 6)
rec('3b10', 'wrong 1..20 210', sum(range(1, 21)), 210)

# ---------- mental-3 ----------
rec('3m01', '73 x 28', 73 * 28, 73 * 30 - 73 * 2)
rec('3m01', 'check 2044', 2044, 70 * 28 + 3 * 28)
rec('3m01', 'wrong took 73 once 2117', 73 * 30 - 73, 2117)
rec('3m01', 'wrong dropped 3 x 28 1960', 70 * 28, 1960)
q2 = F(4357, 13)
rec('3m02', '4357/13', q2, 335 + F(2, 13))
print('3m02 1dp', round(float(q2), 1))
rec('3m02', 'wrong truncated 335.1', 335.1, math.floor(float(q2) * 10) / 10, 1e-9)
rec('3m02', 'wrong decimal slip 33.5', 33.5, round(float(q2) / 10, 1), 1e-9)
g3 = F(12, 10) * F(85, 100) * F(11, 10) - 1
rec('3m03', '+20, -15, +10', g3, F(122, 1000))
rec('3m03', 'check step by step', g3, ((100 * F(12, 10)) * F(85, 100) * F(11, 10) - 100) / 100)
rec('3m03', 'wrong added 0.15', F(20 - 15 + 10, 100), 0.15)
rec('3m03', 'wrong stopped after two 0.02', F(12, 10) * F(85, 100) - 1, 0.02)
rec('3m04', 'odds 3 to 7: chance 7/10', F(7, 10), 1 - F(3, 10))
rec('3m04', 'check: fair stake', F(7, 10) * 3 - F(3, 10) * 7, 0)    # a £7 stake winning £3 is fair at 70%
rec('3m04', 'wrong 3/10', F(3, 3 + 7), 0.3)
rec('3m04', 'wrong 3/7', F(3, 7), 0.428571, 1e-6)
v5 = 6.82 * 14.7 * 3.1
rec('3m05', 'product 310.79', v5, 100.254 * 3.1, 1e-9)
assert abs(310 - v5) / v5 < 0.03 and abs(290 - v5) / v5 > 0.03 and abs(340 - v5) / v5 > 0.03
rec('3m05', 'option all down 6.8 x 14 x 3', 6.8 * 14 * 3, 285.6, 1e-9)
rec('3m05', 'option all up 7 x 15 x 3.2', 7 * 15 * 3.2, 336, 1e-9)
seq = [2, 10, 4, 20, 8, 40]
rec('3m06', 'odd strand doubles', seq[4] * 2, 16)
rec('3m06', 'check: strands', [seq[i] for i in (0, 2, 4)] + [16] == [2, 4, 8, 16], True)
rec('3m06', 'wrong 80', 40 * 2, 80)
rec('3m06', 'wrong 48', 40 + 8, 48)
x1 = (3.3 + 11 / 3.3) / 2
rec('3m07', 'Newton step', x1, 3.3 + (11 - 3.3 ** 2) / (2 * 3.3), 1e-12)
rec('3m07', 'close to sqrt(11)', x1, sqrt(11), 1e-4)
print('3m07 2dp', round(x1, 2))
rec('3m07', 'wrong 11/3.3 not averaged', round(11 / 3.3, 2), 3.33, 1e-9)
rec('3m08', '60 person-days / 4', F(6 * 10, 4), 15)
rec('3m08', 'half time doubles', F(6 * 10, 4 * F(1, 2)), 30)
rec('3m08', 'option wrong scaling 6.67', F(10 * 4, 6), 6.6667, 1e-4)
rec('3m09', 'net 63 - 11', 63 - 11, 52)
assert 63 + 11 + 6 == 80
rec('3m09', 'wrong ignored penalty 63', 63, 63)
rec('3m09', 'wrong skips cost 46', 63 - 11 - 6, 46)
rank = {'A odds 3 to 2 against': F(2, 5), 'B 5/12': F(5, 12), 'C 0.42': F(42, 100), 'D 7/17': F(7, 17), 'E odds 4 to 3 against': F(3, 7)}
order = sorted(rank, key=rank.get)
rec('3m10', 'order A D B C E', order == ['A odds 3 to 2 against', 'D 7/17', 'B 5/12', 'C 0.42', 'E odds 4 to 3 against'], True)
rec('3m10', 'cross 5x17 vs 7x12', 5 * 17 - 7 * 12, 1)
rec('3m10', 'read-for trap order D B C E A', sorted({'A': F(3, 5), 'B': F(5, 12), 'C': F(42, 100), 'D': F(7, 17), 'E': F(4, 7)}, key=lambda k: {'A': F(3, 5), 'B': F(5, 12), 'C': F(42, 100), 'D': F(7, 17), 'E': F(4, 7)}[k]) == ['D', 'B', 'C', 'E', 'A'], True)

# ---------- market-making-3 ----------
# 3k01 four cards; the first two shown are a heart and a club; £10 per heart among the four
fv = 10 * (1 + 2 * F(12, 50))
rest = ['H'] * 12 + ['x'] * 38                                        # 50 cards left, 12 hearts
from itertools import combinations
cnt = tot = 0
for c in combinations(range(50), 2):
    tot += 1; cnt += 1 + sum(1 for i in c if rest[i] == 'H')
rec('3k01', 'fair value 14.80', fv, 10 * F(cnt, tot))
rec('3k01', 'wrong fresh deck 15', 10 * (1 + 2 * F(13, 52)), 15)
rec('3k01', 'wrong ignored reveals 10', 10 * 4 * F(13, 52), 10)
rec('3k01', 'wrong dropped shown heart 4.80', 10 * 2 * F(12, 50), F(24, 5))
rec('3k01', 'wrong one card out 14.7059', 10 * (1 + 2 * F(12, 51)), F(750, 51))
# 3k02 fermi error: a divisor 2x low makes the answer 2x high
rec('3k02', 'ratio', F(1000 * 2, 4000 // 2) / F(1000 * 2, 4000), 2)
# 3k03 heads in 100 flips: exact coverage of intervals
def cover(lo, hi, n=100): return F(sum(comb(n, k) for k in range(lo, hi + 1)), 2 ** n)
for lo, hi in ((45, 55), (41, 59), (40, 60), (35, 65)): OUT.append(f'3k03  P({lo}..{hi}) = {float(cover(lo, hi)):.4f}')
assert cover(40, 60) >= F(95, 100) > cover(41, 59)
rec('3k03', 'normal check 50 +- 1.96 x 5', 50 + 1.96 * 5, 59.8, 1e-9)
rec('3k03', 'sim P(40..60)', cover(40, 60), sim(lambda: 40 <= sum(rng.random() < 0.5 for _ in range(100)) <= 60, 50000), 0.005)
# 3k04 coverage: 12 of 20 at 80%
pl = sum(comb(20, k) * F(4, 5) ** k * F(1, 5) ** (20 - k) for k in range(0, 13))
rec('3k04', 'P(at most 12 of 20) 0.0321', pl, 1 - sum(comb(20, k) * F(4, 5) ** k * F(1, 5) ** (20 - k) for k in range(13, 21)))
rec('3k04', 'sim', pl, sim(lambda: sum(rng.random() < 0.8 for _ in range(20)) <= 12, 200000), 0.003)
print('3k04 P 3dp', round(float(pl), 3))
rec('3k04', 'hit rate 60%', F(12, 20), 0.6)
# 3k05 fair 50 -> 49.4 after 5 lots sold; 3 more lots
per = (F(50) - F(494, 10)) / 5
rec('3k05', 'per lot 0.12', per, F(12, 100))
rec('3k05', 'new fair 49.04', F(494, 10) - 3 * per, 50 - 8 * per)
rec('3k05', 'wrong same move 48.8', F(494, 10) - F(6, 10), 48.8)
rec('3k05', 'wrong wrong way 49.76', F(494, 10) + 3 * per, 49.76)
# 3k06 ledger
trades = [(+3, 42), (-5, 45), (+4, 41), (-2, 46), (+1, 44)]
pos = sum(q for q, _ in trades); cash = -sum(q * px for q, px in trades)
rec('3k06', 'P&L at mark 43', cash + pos * 43, sum(q * (43 - px) for q, px in trades))
rec('3k06', 'per-trade check', [q * (43 - px) for q, px in trades] == [3, 10, 8, 6, -1], True)
rec('3k06', 'wrong cash only -17', cash, -17)
rec('3k06', 'wrong left out the loser 27', sum(q * (43 - px) for q, px in trades if q * (43 - px) > 0), 27)
# 3k07 hedge: 5 baskets at 2.4 a point, instrument 0.8 a point
rec('3k07', 'units 15', F(5 * 24, 10) / F(8, 10), 15)
rec('3k07', 'check exposure zero', 5 * 2.4 - 15 * 0.8, 0, 1e-12)
rec('3k07', 'wrong one basket 3', F(24, 8), 3)
rec('3k07', 'wrong multiplied 9.6', 5 * 2.4 * 0.8, 9.6, 1e-12)

rec('3p14', 'wrong whole needle 0.7639', 2 * key14, 12 / (5 * pi), 1e-12)
rec('3m09', 'accuracy 63/74 = 85%', round(63 / 74, 2), 0.85)
rec('3h08', '10 million cups over 30,000 shops', round(10_000_000 / 30_000), 333)
rec('3h08', '67m x 0.6 x 0.5 x 2 = 40m cups', 67e6 * 0.6 * 0.5 * 2, 40.2e6, 1)
for line in OUT: print(line)
print(f'all {len(OUT)} checks passed')
```

### Its output

```text
3p03 key 4dp 0.8392
3p06 key 4dp 0.4853
3p07 key 4dp 0.1624
3p11 key 4dp 0.038
3p14 key 4dp 0.382
3m02 1dp 335.2
3m07 2dp 3.32
3k04 P 3dp 0.032
3p01  E middle of three d6 (enum)                  3.500000  check       3.500000
3p01  sim                                          3.500000  check       3.501890
3p01  wrong largest 119/24                         4.958333  check       4.958333
3p01  wrong smallest 49/24                         2.041667  check       2.041667
3p01  wrong continuous 3                           3.000000  check       3.000000
3p02  9 H9 = 7129/280                             25.460714  check      25.460714
3p02  sim                                         25.460714  check      25.468240
3p02  last sticker alone 9                         9.000000  check       9.000000
3p02  wrong left out last 16.4607                 16.460714  check      16.460714
3p02  wrong n^2 81                                81.000000  check      81.000000
3p03  1 - 0.97^60                                  0.839193  check       0.839193
3p03  sim                                          0.839193  check       0.837880
3p03  wrong added 1.8                              1.800000  check       1.800000
3p03  wrong none 0.1608                            0.160807  check       0.160807
3p03  wrong Poisson 0.8347                         0.834701  check       0.834701
3p04  mean n=7 by enumeration                      1.000000  check       1.000000
3p04  var n=7 by enumeration                       1.000000  check       1.000000
3p04  mean n=12 indicators                         1.000000  check       1.000000
3p04  var n=12 indicators                          1.000000  check       1.000000
3p04  sim mean                                     1.000000  check       0.998880
3p04  sim var                                      1.000000  check       0.997079
3p04  option binomial var 11/12                    0.916667  check       0.916667
3p04  option one guest 1/12, 11/144                0.076389  check       0.076389
3p04  option E[X^2] = 2                            2.000000  check       2.000000
3p05  E three in a row (states)                   24.375000  check      24.375000
3p05  closed (1+p+p^2)/p^3 = 24.375               24.375000  check      24.375000
3p05  sim                                         24.375000  check      24.366220
3p05  wrong two in a row 8.75                      8.750000  check       8.750000
3p05  wrong 1/p^3 15.625                          15.625000  check      15.625000
3p05  wrong 3/p 7.5                                7.500000  check       7.500000
3p06  P(good | fire) = 33/68                       0.485294  check       0.485294
3p06  sim                                          0.485294  check       0.484512
3p06  wrong no base rate 0.6875                    0.687500  check       0.687500
3p06  wrong hit rate 0.55                          0.550000  check       0.550000
3p06  wrong base rate 0.3                          0.300000  check       0.300000
3p07  reach 9 from 3 at 0.45                       0.162356  check       0.162356
3p07  sim                                          0.162356  check       0.161360
3p07  wrong fair 1/3                               0.333333  check       0.333333
3p07  wrong r = p/q 0.5412                         0.541215  check       0.541215
3p07  wrong r = p/q equals reaching 9 from 3 at p = 0.55       0.541215  check       0.541215
3p07  wrong six straight wins 0.0083               0.008304  check       0.008304
3p08  P(TTH first) linear solve                    0.250000  check       0.250000
3p08  P(TTH first) = first two flips TT            0.250000  check       0.250000
3p08  sim                                          0.250000  check       0.250390
3p08  wrong HTT chance 0.75                        0.750000  check       0.750000
3p08  wrong odds ratio 1/3                         0.333333  check       0.333333
3p09  Kelly fraction 0.09                          0.090000  check       0.090000
3p09  edge per £1 0.225 > 0                        0.225000  check       0.225000
3p09  wrong p - q -0.3                            -0.300000  check      -0.300000
3p09  wrong staked p 0.35                          0.350000  check       0.350000
3p09  wrong edge 0.225                             0.225000  check       0.225000
3p10  threshold W by bisection                    24.250000  check      24.250000
3p10  EV of holding 1                              1.000000  check       1.000000
3p10  certainty equivalent at W=20                 0.396078  check       0.396000
3p10  certainty equivalent at W=100                0.876162  check       0.876000
3p11  lose five in a row                           0.038020  check       0.038020
3p11  sim                                          0.038020  check       0.038047
3p11  stakes to the cap                           31.000000  check      31.000000
3p11  wrong four bets 0.0731                       0.073116  check       0.073116
3p11  wrong fair coin 0.0313                       0.031250  check       0.031250
3p11  wrong six bets 0.0198                        0.019771  check       0.019771
3p12  midpoint method 3/4                          0.750000  check       0.750000
3p12  sim                                          0.750000  check       0.749670
3p12  wrong endpoints 2/3 (sim)                    0.666667  check       0.667345
3p12  wrong radius point sqrt(3)/2                 0.866025  check       0.866000
3p12  wrong shorter 1/4                            0.250000  check       0.250000
3p13  E sq distance L^2/6 = 1.5                    1.500000  check       1.500000
3p13  midpoint grid                                1.500000  check       1.499996
3p13  sim                                          1.500000  check       1.503059
3p13  wrong E|X-Y| = 1                             1.000000  check       1.000000
3p13  wrong unscaled 1/6                           0.166667  check       0.166700
3p13  wrong scaled by L once 0.5                   0.500000  check       0.500000
3p14  2l/(pi d)                                    0.381972  check       0.381972
3p14  integral of crossing region                  0.381972  check       0.381972
3p14  sim                                          0.381972  check       0.382543
3p14  wrong l/d 0.6                                0.600000  check       0.600000
3p14  wrong dropped the 2 0.1910                   0.190986  check       0.190986
3b01  all 46,656 patterns: exactly one right       1.000000  check       1.000000
3b01  guess own index: all wrong on 1,2,3,4,5,0       0.000000  check       0.000000
3b01  crowd rule: every guess wrong on 0,0,1,1,2,2       0.000000  check       0.000000
3b02  eight coins: 2 weighings                     2.000000  check       2.000000
3b02  halving 4 v 4 needs 3                        3.000000  check       3.000000
3b03  A takes at once: A gets 3                    3.000000  check       3.000000
3b03  B would get 1                                1.000000  check       1.000000
3b03  round 3 take 12 vs split 8                  12.000000  check      12.000000
3b03  round 2: B takes 6 vs 4 after A takes in round 3       6.000000  check       6.000000
3b03  wrong: pass to round 3 and take 12          12.000000  check      12.000000
3b04  makespan by search                           8.000000  check       8.000000
3b04  wrong greedy in given order 11              11.000000  check      11.000000
3b04  wrong serial 16                             16.000000  check      16.000000
3b05  lcm 1..10                                 2520.000000  check    2520.000000
3b05  smallest by search                        2520.000000  check    2520.000000
3b05  wrong 2^4 5040                            5040.000000  check    5040.000000
3b05  wrong 2^2 1260                            1260.000000  check    1260.000000
3b05  wrong 10! 3628800                      3628800.000000  check 3628800.000000
3b06  eight weeds: day                            21.000000  check      21.000000
3b06  wrong 24/8                                   3.000000  check       3.000000
3b06  wrong 24-8                                  16.000000  check      16.000000
3b07  sum k=10..99                                 0.090000  check       0.090000
3b07  wrong from k=1 0.99                          0.990000  check       0.990000
3b07  wrong 1/10 only                              0.100000  check       0.100000
3b07  wrong 1 - 1/10                               0.900000  check       0.900000
3b08  11 x 5 = 55 is odd                           1.000000  check       1.000000
3b09  bird distance 72                            72.000000  check      72.000000
3b09  stepped zigzag                              72.000000  check      72.000000
3b09  wrong slower train 180                     180.000000  check     180.000000
3b09  wrong speed difference 360                 360.000000  check     360.000000
3b10  sum cubes 1..20                          44100.000000  check   44100.000000
3b10  wrong squares 2870                        2870.000000  check    2870.000000
3b10  wrong 1..20 210                            210.000000  check     210.000000
3m01  73 x 28                                   2044.000000  check    2044.000000
3m01  check 2044                                2044.000000  check    2044.000000
3m01  wrong took 73 once 2117                   2117.000000  check    2117.000000
3m01  wrong dropped 3 x 28 1960                 1960.000000  check    1960.000000
3m02  4357/13                                    335.153846  check     335.153846
3m02  wrong truncated 335.1                      335.100000  check     335.100000
3m02  wrong decimal slip 33.5                     33.500000  check      33.500000
3m03  +20, -15, +10                                0.122000  check       0.122000
3m03  check step by step                           0.122000  check       0.122000
3m03  wrong added 0.15                             0.150000  check       0.150000
3m03  wrong stopped after two 0.02                 0.020000  check       0.020000
3m04  odds 3 to 7: chance 7/10                     0.700000  check       0.700000
3m04  check: fair stake                            0.000000  check       0.000000
3m04  wrong 3/10                                   0.300000  check       0.300000
3m04  wrong 3/7                                    0.428571  check       0.428571
3m05  product 310.79                             310.787400  check     310.787400
3m05  option all down 6.8 x 14 x 3               285.600000  check     285.600000
3m05  option all up 7 x 15 x 3.2                 336.000000  check     336.000000
3m06  odd strand doubles                          16.000000  check      16.000000
3m06  check: strands                               1.000000  check       1.000000
3m06  wrong 80                                    80.000000  check      80.000000
3m06  wrong 48                                    48.000000  check      48.000000
3m07  Newton step                                  3.316667  check       3.316667
3m07  close to sqrt(11)                            3.316667  check       3.316625
3m07  wrong 11/3.3 not averaged                    3.330000  check       3.330000
3m08  60 person-days / 4                          15.000000  check      15.000000
3m08  half time doubles                           30.000000  check      30.000000
3m08  option wrong scaling 6.67                    6.666667  check       6.666700
3m09  net 63 - 11                                 52.000000  check      52.000000
3m09  wrong ignored penalty 63                    63.000000  check      63.000000
3m09  wrong skips cost 46                         46.000000  check      46.000000
3m10  order A D B C E                              1.000000  check       1.000000
3m10  cross 5x17 vs 7x12                           1.000000  check       1.000000
3m10  read-for trap order D B C E A                1.000000  check       1.000000
3k01  fair value 14.80                            14.800000  check      14.800000
3k01  wrong fresh deck 15                         15.000000  check      15.000000
3k01  wrong ignored reveals 10                    10.000000  check      10.000000
3k01  wrong dropped shown heart 4.80               4.800000  check       4.800000
3k01  wrong one card out 14.7059                  14.705882  check      14.705882
3k02  ratio                                        2.000000  check       2.000000
3k03  P(45..55) = 0.7287
3k03  P(41..59) = 0.9431
3k03  P(40..60) = 0.9648
3k03  P(35..65) = 0.9982
3k03  normal check 50 +- 1.96 x 5                 59.800000  check      59.800000
3k03  sim P(40..60)                                0.964800  check       0.964980
3k04  P(at most 12 of 20) 0.0321                   0.032143  check       0.032143
3k04  sim                                          0.032143  check       0.032060
3k04  hit rate 60%                                 0.600000  check       0.600000
3k05  per lot 0.12                                 0.120000  check       0.120000
3k05  new fair 49.04                              49.040000  check      49.040000
3k05  wrong same move 48.8                        48.800000  check      48.800000
3k05  wrong wrong way 49.76                       49.760000  check      49.760000
3k06  P&L at mark 43                              26.000000  check      26.000000
3k06  per-trade check                              1.000000  check       1.000000
3k06  wrong cash only -17                        -17.000000  check     -17.000000
3k06  wrong left out the loser 27                 27.000000  check      27.000000
3k07  units 15                                    15.000000  check      15.000000
3k07  check exposure zero                          0.000000  check       0.000000
3k07  wrong one basket 3                           3.000000  check       3.000000
3k07  wrong multiplied 9.6                         9.600000  check       9.600000
3p14  wrong whole needle 0.7639                    0.763944  check       0.763944
3m09  accuracy 63/74 = 85%                         0.850000  check       0.850000
3h08  10 million cups over 30,000 shops          333.000000  check     333.000000
3h08  67m x 0.6 x 0.5 x 2 = 40m cups         40200000.000000  check 40200000.000000
all 175 checks passed
```

### Final run of `play-bank.mjs`

```text
requires lessons 19; locked before 86, after 51; drawable 291; my items drawable 50 of 50
pass 0: right answers, 7 decks, 0 not reached
pass 1: wrong #1, 6 decks, 42 routed, 0 not reached
pass 2: wrong #2, 6 decks, 42 routed, 0 not reached
pass 3: wrong #3, 7 decks, 29 routed, 0 not reached
pass 4: wrong #4, 4 decks, 1 routed, 0 not reached
wrong ids and distractors in the files: 114
choice items seen with more than one option order: 13 of 13
  orders hats-twelve-coats dbca acbd abdc cadb
  orders when-to-hedge-small-bankroll adbc acbd acdb
  orders hats-mod-k-six-prisoners cabd dbac
  orders weighing-heavy-eight-one-light dcba bdca
  orders backward-induction-doubling-pot bacd cbad dacb
  orders double-counting-eleven-guests dacb cdab acbd
  orders estimate-product-three-factors bacd adcb cbad
  orders word-time-crew-days bcad badc bacd abdc cadb
  orders ranking-five-mixed-forms cbad cdab dcba
  orders fermi-error-divisor-low cbda bdca dabc dbca
  orders intervals-heads-in-100 cdab bcad badc dacb
  orders coverage-twelve-of-twenty acbd acdb cdba dacb
  orders thinking-aloud-own-name bdac dabc adbc
no console errors
ALL OK
```

## After the answer check (4 Nov)
The fix pass in `docs/reviews/answers-2026-11-03-bank.md` changed some keys, `wrong` values and numbers quoted above; that file's `## Fix pass` section is the current record.

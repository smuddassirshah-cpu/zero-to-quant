# Report: interview bank part 1, session 4 (50 items)

Brief: `docs/briefs/bank.md` sections 1 to 4, "### Session 4", sections 6 to 9 and "Changes after session 1 (3 Nov)". Files written in `app/content/bank/`; nothing else in `content/` was touched (`sample.json` and the other sessions' files left alone).

| File | Items | Families |
| --- | --- | --- |
| `probability-4.json` | 12 | dice-ev, every-coupon, indicator-tricks, bayes-in-a-minute, largest-of-several, ants, broken-stick, estimating-n, duels, who-wins, given-the-total, kelly |
| `brainteasers-4.json` | 10 | weighing-heavy-or-light, pirates, egg-drop-dp, river-crossing, pairing, invariant-product, monovariant, hats-simultaneous, common-knowledge, missing-information |
| `mental-4.json` | 10 | mental-arithmetic 2, percent-chain, fraction-compare, estimate-exact, sequences, sqrt-newton, word-filled, probability, battery |
| `market-making-4.json` | 8 | card-fair, dice-ev, informed-loss, position-limit, hedge-ratio, arbitrage, game-edge, calibration |
| `behavioural-4.json` | 10 | star-story 3, why-us 2, video-answer, after-rejection, final-round, project-account, reasoning-aloud |

## Results

- `node tools/validate.mjs 2>&1 | tail -5`: **0 errors**, 392 warnings, none from `content/bank/` (no `style` or `source` warning). Item ids are unique across all 21 bank files (sessions 1 to 4 and the sample).
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: **All passed** (`#bank 124 drawable of 210, deck, pace line, schedule, miss, old save`). With `--mobile`: **All passed**.
- **Deck loop** `scratchpad/s4/bank-1-4/play-bank.mjs` (copies the `bankChecks` loop: `ZQ.select.bankDeck`, `ZQ.test.answerCorrect()`, `check()`, `continue()`), at 390 x 844, local CDN routed as the playthrough does. It completes setup, imports a save with the 19 `requires` lessons finished (locked count 86 before, 45 after, all from other sessions' files), schedules every other drawable item 30 days away with `ZQ.state.bankResult`, wraps `bankDeck` to record each deal, then plays:
  - pass 0: **50 of 50** session-4 items dealt and accepted with the authored answer (the 10 longform items open the model on Check, every rubric line is ticked, and the item is accepted);
  - passes 1 to 4: the items are marked missed and the clock moves 2 days; each numeric `wrong` value is typed (times 100 for the one `%` item) and each distractor clicked in turn. **116 of 116** wrong ids and distractors returned their own key and showed their `byKey` or `why` line;
  - every `choice` (12) has exactly one correct option of 4, and all 12 were seen in more than one option order, so `shuffle: true` works;
  - no console errors, no page wider than 390 px. Output at the end of this report.
- Screenshots: 100 at 390 px (pass 0 every item and every longform rubric, pass 1 every first wrong route), looked at as contact sheets in `scratchpad/s4/bank-1-4/sheets/`. No layout fault: prose, lists (the battery item's five steps), options and models wrap cleanly. The longform rubric sits below the model and is reached by scrolling, as session 1 found.
- **Voice scan**, `VOICE_BASE=/home/user/zero-to-quant/app/content/bank/ python3 docs/reviews/voice-scan.py --summary`: **explanations over three sentences: 0; over 20 words: 0** (5,397 sentences across the folder). The first run found 15 sentences of 21 to 28 words in my files, mostly in models; all were split or cut, and a stricter run at 19 words now reports none in my files.
- No `!` outside KaTeX, no em-dashes or en-dashes, British spelling, £ throughout, no firm names ("a market maker", "a hedge fund" only).

## Counts against the brief

- Per file: 12, 10, 10, 8, 10 (matches section 2). Per difficulty: D2 6, D3 23, D4 13, D5 8 (matches). Per kind: numeric 28, choice 12, longform 10, expression 0 (matches).
- Per family: the session-4 column of section 3 exactly (dice-ev twice: `4p01` in probability and `4k02` in market making). `requires` on all 21 difficulty 4 and 5 items and none below, each the "Draws on" lesson. Every `pace` is the table's, the largest 180. Roles as the table.
- `skills` are copied from each "Draws on" lesson file's `skills` field (the `course.json` maps hold lesson ids only).
- Behavioural rubrics: six lines of 2, 2, 2, 2, 1, 1 on all ten, in session 1's order for each family (the `why-us` and `project-account` lines follow session 1's wording for those families). Models are 139 to 158 words, first person, generic settings (a society quiz, a statistics group project, a society trading game, a summer backtest); no real firm, university or grade body.

## Items, refs and changes from the table

| Ref | Id | Family | Kind | D | Pace | Key | `wrong` values or distractors |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4p01 | `dice-ev-twelve-sided-three-rolls` | dice-ev | numeric | 4 | 150 | 8.8333 | 8.0 (two-rolls), 6.5 (one-roll), 8.75 (first-vs-fresh), 9.4792 (best-of-three) |
| 4p02 | `every-coupon-paid-rolls` | every-coupon | numeric | 3 | 150 | 2.95 | 16.0 (six-rolls), -29.0 (thirty-six), 4.45 (skip-first) |
| 4p03 | `indicator-tricks-empty-boxes` | indicator-tricks | numeric | 3 | 120 | 1.6113 | 0.2014 (one-box), 6.3887 (filled), 2.7489 (eighth-power) |
| 4p04 | `bayes-in-a-minute-two-flags` | bayes-in-a-minute | numeric | 4 | 150 | 0.7209 | 0.1867 (one-screen), 0.9922 (no-base), 0.81 (sens-squared) |
| 4p05 | `largest-of-several-first-alarm` | largest-of-several | numeric | 3 | 120 | 6.0 | 20.6667 (mean-of-means), 12.0 (fastest-only), 62.0 (add-means), 18.0 (avg-rate) |
| 4p06 | `ants-fly-between-trains` | ants | numeric | 2 | 90 | 135.0 | 270.0 (one-train), 120.0 (gap), 60.0 (meeting-point) |
| 4p07 | `broken-stick-longer-piece` | broken-stick | choice | 3 | 90 | 45 cm | 3 distractors |
| 4p08 | `estimating-n-tagged-fish` | estimating-n | numeric | 2 | 75 | 250.0 | 10.0 (flipped), 82.0 (seen-only), 200.0 (catch-ratio) |
| 4p09 | `duels-weakest-fires-first` | duels | choice | 5 | 180 | Fire into the air: A then wins with chance ab | 3 distractors |
| 4p10 | `who-wins-take-one-two-five` | who-wins | numeric | 3 | 120 | 1.0 | 4.0 (mod-six), 5.0 (most), 2.0 (two) |
| 4p11 | `given-the-total-three-dice` | given-the-total | numeric | 4 | 120 | 0.3333 | 0.1667 (one-order), 0.0556 (whole-table), 0.0741 (forgot-first) |
| 4p12 | `kelly-twice-the-fraction` | kelly | choice | 5 | 150 | Slightly negative, about −0.005: the bankroll | 3 distractors |
| 4b01 | `weighing-heavy-or-light-twelve` | weighing-heavy-or-light | choice | 5 | 180 | Weigh 4 against 4. If level, weigh 3 of the o | 3 distractors |
| 4b02 | `pirates-five-strict-majority` | pirates | numeric | 5 | 180 | 77.0 | 78.0 (tie-passes), 79 (one-vote), 76.0 (pay-two-each) |
| 4b03 | `egg-drop-dp-three-eggs` | egg-drop-dp | numeric | 5 | 180 | 10.0 | 9 (nine), 18.0 (two-eggs), 8.0 (halving) |
| 4b04 | `river-crossing-fox-hen-grain` | river-crossing | numeric | 2 | 90 | 7.0 | 5.0 (no-returns-with-cargo), 3.0 (once-each) |
| 4b05 | `pairing-knockout-matches` | pairing | choice | 2 | 60 | 36: each match removes one team, and 36 teams | 3 distractors |
| 4b06 | `invariant-product-unit-fractions` | invariant-product | numeric | 4 | 150 | 9.0 | 2.829 (sum), 10.0 (no-minus) |
| 4b07 | `monovariant-splitting-piles` | monovariant | choice | 4 | 150 | Each move adds one pile and piles can never p | 3 distractors |
| 4b08 | `hats-simultaneous-fifteen` | hats-simultaneous | numeric | 4 | 150 | 0.9375 | 0.5 (one-guesser), 0.75 (three-rule), 0.875 (seven) |
| 4b09 | `common-knowledge-marked-badges` | common-knowledge | numeric | 5 | 180 | 7.0 | 6.0 (seen), 1 (first), 8.0 (late) |
| 4b10 | `missing-information-no-unit` | missing-information | choice | 3 | 75 | What the 40 and the prices are in: shares or  | 3 distractors |
| 4m01 | `mental-arithmetic-97-by-53` | mental-arithmetic | numeric | 2 | 25 | 5141.0 | 5297.0 (sub-three), 5459.0 (added) |
| 4m02 | `mental-arithmetic-7448-by-28` | mental-arithmetic | numeric | 3 | 30 | 266.0 | 26.6 (place-down), 2660.0 (place-up) |
| 4m03 | `percent-chain-recover-35` | percent-chain | numeric | 3 | 25 | 0.54 | 0.35 (same), 0.26 (over-135) (unit %) |
| 4m04 | `fraction-compare-middle-of-three` | fraction-compare | choice | 3 | 30 | 13/18 | 3 distractors |
| 4m05 | `estimate-exact-small-decimal` | estimate-exact | choice | 3 | 25 | 99.09 | 3 distractors |
| 4m06 | `sequences-twelfth-term` | sequences | numeric | 3 | 35 | 4095.0 | 2047.0 (eleventh), 4096.0 (power), 127.0 (next) |
| 4m07 | `sqrt-newton-2400` | sqrt-newton | numeric | 3 | 35 | 49.0 | 48.9 (rounded-down), 4.9 (root-24), 15.5 (root-240) |
| 4m08 | `word-filled-tank-and-drain` | word-filled | numeric | 3 | 40 | 30.0 | 7.5 (added), 8.0 (difference), 16.0 (average) |
| 4m09 | `probability-two-heads-in-four` | probability | numeric | 3 | 30 | 0.6875 | 0.375 (exactly-two), 0.9375 (at-least-one), 0.3125 (at-most-one) |
| 4m10 | `battery-five-step-chain` | battery | numeric | 5 | 60 | 114.0 | 111.8333 (next-square-49), 19.0 (one-in-36), 18.0 (quarter-of) |
| 4k01 | `card-fair-five-face-up` | card-fair | numeric | 3 | 75 | 6.9149 | 7.0 (full-deck), 6.25 (over-52), 7.8 (seen-mean) |
| 4k02 | `dice-ev-product-d4-d8` | dice-ev | numeric | 3 | 90 | 11.25 | 16.5 (range-mid), 7.0 (added) |
| 4k03 | `informed-loss-trades-to-recover` | informed-loss | numeric | 4 | 100 | 5.0 | 4.5 (fraction), 6.0 (from-fair), 3.0 (full-width) |
| 4k04 | `position-limit-order-of-fills` | position-limit | choice | 3 | 60 | Sell 4 to the buyer first, then buy 3 from th | 3 distractors |
| 4k05 | `hedge-ratio-call-delta` | hedge-ratio | numeric | 2 | 60 | 1400.0 | 14.0 (per-share), 4000.0 (no-delta), 2600.0 (one-minus) |
| 4k06 | `arbitrage-three-outcomes` | arbitrage | choice | 3 | 90 | Buy one of each at the offers: pay £97, colle | 3 distractors |
| 4k07 | `game-edge-square-less-ten` | game-edge | numeric | 4 | 100 | 2.8333 | 0.1667 (negatives), -2.75 (square-mean), 7.8333 (no-cost) |
| 4k08 | `calibration-ninety-percent` | calibration | choice | 3 | 75 | You are overconfident: 75% held against 90% c | 3 distractors |
| 4h01 | `star-story-short-handed-deadline` | star-story | longform | 3 | 150 | rubric 2, 2, 2, 2, 1, 1 | model 154 words |
| 4h02 | `star-story-hard-feedback` | star-story | longform | 4 | 150 | rubric 2, 2, 2, 2, 1, 1 | model 156 words |
| 4h03 | `star-story-changed-my-mind` | star-story | longform | 4 | 150 | rubric 2, 2, 2, 2, 1, 1 | model 148 words |
| 4h04 | `why-us-research-not-trading` | why-us | longform | 3 | 120 | rubric 2, 2, 2, 2, 1, 1 | model 151 words |
| 4h05 | `why-us-how-you-think` | why-us | longform | 3 | 120 | rubric 2, 2, 2, 2, 1, 1 | model 150 words |
| 4h06 | `video-answer-under-pressure` | video-answer | longform | 3 | 150 | rubric 2, 2, 2, 2, 1, 1 | model 143 words |
| 4h07 | `after-rejection-gave-up-early` | after-rejection | longform | 4 | 150 | rubric 2, 2, 2, 2, 1, 1 | model 141 words |
| 4h08 | `final-round-offer-deadline` | final-round | longform | 4 | 150 | rubric 2, 2, 2, 2, 1, 1 | model 139 words |
| 4h09 | `project-account-hardest-bug` | project-account | longform | 4 | 180 | rubric 2, 2, 2, 2, 1, 1 | model 158 words |
| 4h10 | `reasoning-aloud-harder-follow-up` | reasoning-aloud | longform | 5 | 150 | rubric 2, 2, 2, 2, 1, 1 | model 155 words |

Changes from the table's ideas (structure kept, numbers or twist changed):

- `4p01`: a d12, not a d6. A d6 with three rolls is `graphs-dp/l17-dice-stopping` screen 4 (14/3) and is quoted in `puzzles/l6` screen 6; a d8 with three rolls is `puzzles/l24` screen 9.
- `4p02`: rolls cost £1.50 and the prize is £25. The d6 coupon wait of 14.7 is `puzzles/l2` screen 3, so the twist (a costed wait and a prize) carries the item; d8 and d10 were already used by bank `1p03` and `puzzles/l2` quiz 2.
- `4p05`: rates 2, 3 and 5 an hour, answer in minutes. Rates 1, 2 and 3 are `limits-thm/l17` quiz 1.
- `4p12`: p = 0.62. Kelly at 0.6 and twice Kelly (f = 0.4) is `puzzles/l21` screen 4; 0.55 at evens is in its drill (screen 9); 0.58 is in `fin-ml/l9` near twice Kelly.
- `4b01`: twelve coins kept (the classic), but the item asks for the first weighing together with its level branch. `brainteasers/l4` screens 2 and 3 give the first weighing and treat only the tilt branch.
- `4b02`: 80 coins and a strict majority. Bank `1b07` is four pirates with 100 coins (strict); `brainteasers/l6` and homework 2 use 60 coins with ties passing.
- `4b03`: 170 floors. Three eggs and 100 floors (9) and 1,000 floors (19) are in `brainteasers/l9` screens 4 and 11.
- `4b05`: 37 teams, reworded. `brainteasers/l14` screen 4 has 50 players in a knockout with the same bye sentence.
- `4b06`: the brief's rule "sum minus one" gives a sum invariant, not a product, and `a + b + 1` on 1 to 10 is `brainteasers/l1` quiz 4. To fit the family `invariant-product`, the move is `a + b + ab` on 1, 1/2, ..., 1/9 (answer 9). `brainteasers/l1` screen 3 uses `a + b + ab` on 1 to 6 (5039).
- `4b07`: the idea "a move splits a pile" made concrete: one pile of 30, any split, exactly 29 moves.
- `4b08`: fifteen players (15/16). Three players (3/4) and seven players (7/8) are `brainteasers/l7` screens 10 and 11.
- `4b09`: seven marked badges among fifty traders. The 100 blue-eyed islanders and 5 of 9 muddy children are in `brainteasers/l10`; the cheating-spouse wording was replaced by a neutral setting.
- `4b04`: a fox, a hen and grain, the same 7-crossing puzzle as wolf, goat and cabbage (no course item has it).
- `4m03`: a 35% fall (54%). Recovery rises are drilled in `mental-pressure/l6` (20% and 25%) and `ratio/homework-2`; 30% (42.9%) is the textbook case.
- `4m06`: the 12th term (4,095). The 10th term, 1,023, is `series/l7-shifted-copy` (the sum of ten doubling stakes).
- `4m07`: kept at 2,400 as briefed; it rounds to 49.0, so a learner who stops at 49 is right, and the Newton step only confirms it.
- `4k02`: a d4 times a d8 (11.25). The product of two d6 (12.25) is `mm-games/l2` and `l5`. The question asks the fair value; the explanation says how to widen.
- `4k07`: the brief's "the square of a d6 in pounds over 10" read as "the square less 10, or nothing if negative".
- `4k08`: 60 ranges, 45 held. `mm-games/review-1` has 50 ranges at 90% with 38 held, too close to the brief's 50 and 40.
- `4k05`: delta 0.35 on 40 contracts of 100 shares; `mm-games/l11` quiz has 10 contracts at 0.6.

## Every number, two ways

The script `bank-1-4.py` (full text below) computes every key and every numeric `wrong` value with an `assert` against a second method:

| Ref | Key | First way | Second way |
| --- | --- | --- | --- |
| 4p01 | 53/6 ≈ 8.83 | backward values 6.5, 8, 53/6 | every pair of thresholds over all 12³ rolls |
| 4p02 | £2.95 | 25 − 1.5 × 6H₆ | stage sum 6/(6 − k); seeded simulation within 0.05 |
| 4p03 | 1.6113 | 8 × (7/8)¹² | 8 × 7¹²/8¹²; seeded simulation within 0.01 |
| 4p04 | 0.7209 | Bayes with two flags | odds 2:98 times 11.25² |
| 4p05 | 6 min | 60/(2 + 3 + 5) | seeded simulation of three exponentials |
| 4p06 | 135 miles | 90 × 120/80 | the zigzag legs summed, 200 terms |
| 4p07 | 45 cm | (30 + 60)/2 | lattice average of max(x, 60 − x); the 40 and 36.67 distractors by simulation |
| 4p08 | 250 | 50 × 40/8 | 50 ÷ (8/40) |
| 4p09 | 473/1025 ≈ 0.461 (air), 0.335 (C), 0.277 (B) | duel formula | seeded simulation of the truel for each first move |
| 4p10 | 1 | backward induction on piles 0 to 40 | losing piles equal the multiples of 3 |
| 4p11 | 1/3 | 2 of 6 pairs | enumeration of the 27 rolls totalling 10 |
| 4p12 | g(0.48) ≈ −0.0054 | closed form | logs typed by hand; seeded simulation of 2,000,000 bets |
| 4b01 | 4 v 4, then 3 unknown v 3 genuine | case counts against 3^k | exhaustive search over class-count weighings (unknown, maybe heavy, maybe light, genuine) |
| 4b02 | 77 | vote pricing from 1 pirate up | search over every allocation of 0 to 3 coins to each voter |
| 4b03 | 10 | Σ C(d, i) ≥ 170 | full min-max DP over floors |
| 4b04 | 7 | the plan | breadth-first search of all safe states |
| 4b05 | 36 | n − 1 | round-by-round simulation with byes |
| 4b06 | 9 | Π(1 + 1/k) − 1 | 20 random move orders in Fractions |
| 4b07 | 29 | piles − 1 | 50 random split games |
| 4b08 | 15/16 | 1 − 2¹¹/2¹⁵ | the Hamming strategy played on all 32,768 patterns; 3/4 proved best for three players by all 531,441 strategy profiles |
| 4b09 | evening 7 | k marks leave on evening k | possible-worlds simulation for 10 traders with 7 marks (and 8 with 3) |
| 4m01 to 4m10 | 5,141; 266; 54%; 13/18; 99.09; 4,095; 49.0; 30; 11/16; 114 | the stated working | a second route each (exact product, 1,862/7, 1/0.65 − 1, sorted fractions, 481 × 206/1000, the recursion, Newton and `sqrt`, rates, enumeration of 16 flips, the chain step by step) |
| 4k01 | 325/47 ≈ 6.91 | (364 − 39)/47 | deck list with the five cards removed |
| 4k02 | 11.25 | 2.5 × 4.5 | all 32 products averaged |
| 4k03 | 5 | ⌈9/2⌉ | 4 × 2 < 9 ≤ 5 × 2 |
| 4k04 | path 9, 5, 8 | limit check after each fill | buy-first peak 12 > 10 |
| 4k05 | 1,400 | 0.35 × 4,000 | 40 × 100 × 35/100 |
| 4k06 | £3 | 100 − 97 | offers summed |
| 4k07 | 17/6 ≈ £2.83 | 47/6 − 5 | payouts listed face by face |
| 4k08 | widen; P(X ≤ 45) ≈ 0.00067 | binomial pmf | seeded simulation within 0.0015 |

Every `wrong` value is a named slip computed in the script from that slip, and `gen.py` asserts that each lies outside the key's tolerance. Behavioural models carry story numbers only; the one maths figure (`4h10`: the largest of three dice averages about 4.96, two dice 161/36) is 6 − 225/216 = 4.958, checked in the script by enumeration.

## Duplicates (rule 10, DECISIONS "Duplicates (6 Nov)")

Searched `app/content/courses`, `app/content/exams` and `app/content/bank` (sessions 1, 2 and 3 and `sample.json`; session 2's files arrived late and were re-checked before this report) with targeted greps per structure (`three rolls`, `every face`, `rates 1, 2 and 3`, `product of two`, `heavier or lighter`, `pirate`, `eggs`, `knockout`, `a + b + ab`, `hats`, `muddy`, `30% fall`, `1, 3, 7, 15`, `kelly` items with 0.55 and 0.58, `90%` calibration) and with `dups.py`, a scan that lists every course, exam and bank unit sharing an item's parameters and key. The scan's hits are all coincidental (common numbers in unrelated structures). The five closest items, and what changed:

1. `graphs-dp/l17-dice-stopping` screen 4, a d6 with three rolls (14/3): `4p01` uses a d12 (53/6).
2. `puzzles/l21-kelly` screen 4, twice Kelly at p = 0.6: `4p12` uses p = 0.62 and asks for the sign.
3. `brainteasers/l9-egg-drop` screen 4, three eggs and 100 floors (9): `4b03` uses 170 floors (10).
4. `brainteasers/l7-hat-strategies` screens 10 and 11, three and seven players: `4b08` uses fifteen.
5. `mm-games/l2-dice-sum` and `l5-two-sided`, the product of two d6 (12.25): `4k02` uses a d4 and a d8.

Session 2's `when-to-stop-d12-paid-reroll` is also a d12 stopping game, but with a paid reroll and no third roll; its key differs from `4p01`'s 53/6, so neither was changed. Items given fresh numbers for this reason: 15 (`4p01`, `4p02` twist, `4p05`, `4p12`, `4b01` twist, `4b02`, `4b03`, `4b05`, `4b06`, `4b08`, `4b09`, `4m03`, `4m06`, `4k02`, `4k08`).

## Proposals (course items to tag; not edited)

- `puzzles/l26-estimating-n` has no capture-recapture item; `4p08` (tagged fish) draws on it for the family. A course screen on the Lincoln estimate would make the family match its lesson.
- `ants` family items in `puzzles/l12` include the fly between trains (screen 3, quiz 2); `4p06` joins them.
- `dice-games` (puzzles l1) against `dice-ev` (mm-games and the bank), as session 1 raised: `4p01` draws on `puzzles/l6-when-to-stop` but carries `dice-ev` as briefed.

## Open questions

1. `4b06`: the brief's move ("sum minus one") is a sum invariant; I used `a + b + ab` to fit `invariant-product`. Is that the intended family?
2. `4m07`: the brief's 2,400 rounds to 49.0, so the Newton step is barely needed. Should a later pass prefer a root such as 2,200 (46.9)?

## Inbox

Three bullets under "Bank session 4 (3 Nov)" in `docs/BACKLOG-INBOX.md`.

## Scripts

`scratchpad/s4/bank-1-4/` holds `bank-1-4.py` (numbers), `gen.py` (builds the five files from item data and imports the numbers, asserting one correct option, `shuffle`, rubric shape, model length, `requires` only at D4 and D5, pace at most 180, and wrong values outside the key's tolerance), `dups.py` (the duplicate scan), `play-bank.mjs` (the deck loop) and `sheets/` (contact sheets).

### `bank-1-4.py`

```python
"""Bank part 1, session 4: every keyed answer and every numeric `wrong` value, two ways, with asserts.
Writes nothing. Run: python3 bank-1-4.py"""
from fractions import Fraction as F
from itertools import product, permutations, combinations
from math import comb, log, sqrt, isclose
import random

N = {}          # name -> value used by gen.py
ROWS = []
def check(ref, name, a, b, tol=1e-9):
    a_, b_ = float(a), float(b)
    assert isclose(a_, b_, rel_tol=0, abs_tol=tol), (ref, name, a, b)
    ROWS.append((ref, name, a_, b_))
    N[(ref, name)] = a
    return a

# ---------- probability-4 ----------
# 4p01 d12, up to three rolls, keep the last you choose
def stop_value(sides, rolls):
    v = F(sides + 1, 2)
    for _ in range(rolls - 1):
        v = sum(max(F(k), v) for k in range(1, sides + 1)) / sides
    return v
def stop_enum(sides, rolls):       # brute force over all policies given by thresholds per stage
    faces = range(1, sides + 1)
    best = None
    for t1 in range(1, sides + 2):
        for t2 in range(1, sides + 2):
            tot = F(0)
            for a, b, c in product(faces, repeat=3):
                tot += a if a >= t1 else (b if b >= t2 else c)
            val = tot / sides ** 3
            best = val if best is None or val > best else best
    return best
check('4p01', 'key', stop_value(12, 3), stop_enum(12, 3))
assert stop_value(12, 3) == F(53, 6)
check('4p01', 'two-rolls', stop_value(12, 2), F(8))
check('4p01', 'one-roll', stop_value(12, 1), F(13, 2))
# first roll compared with a fresh roll (6.5): keep 7..12, else play the two-roll game worth 8
fv = sum(F(k) if k >= 7 else F(8) for k in range(1, 13)) / 12
check('4p01', 'first-vs-fresh', fv, F(1, 2) * F(19, 2) + F(1, 2) * 8)
emax = sum(max(t) for t in product(range(1, 13), repeat=3)) / F(12 ** 3)
check('4p01', 'best-of-three', emax, 12 - F(sum(j ** 3 for j in range(12)), 1728))

# 4p02 d6 coupon, £1.50 a roll, £25 prize
H6 = sum(F(1, k) for k in range(1, 7))
rolls = 6 * H6
def coupon_sim(n, trials, seed):
    rng = random.Random(seed); tot = 0
    for _ in range(trials):
        seen = set(); c = 0
        while len(seen) < n: seen.add(rng.randrange(n)); c += 1
        tot += c
    return tot / trials
sim = coupon_sim(6, 200000, 4)
assert abs(sim - float(rolls)) < 0.05, sim
check('4p02', 'rolls', rolls, sum(F(6, 6 - k) for k in range(6)))
check('4p02', 'key', 25 - F(3, 2) * rolls, F(295, 100))
check('4p02', 'six-rolls', 25 - F(3, 2) * 6, F(16))
check('4p02', 'thirty-six', 25 - F(3, 2) * 36, F(-29))
check('4p02', 'skip-first', 25 - F(3, 2) * (rolls - 1), F(445, 100))

# 4p03 12 balls, 8 boxes, expected empty boxes
key = 8 * F(7, 8) ** 12
# exact by counting: each box is missed by 7^12 of the 8^12 assignments
enum = F(8 * 7 ** 12, 8 ** 12)
rng = random.Random(3); T = 200000; tot = 0
for _ in range(T):
    tot += 8 - len({rng.randrange(8) for _ in range(12)})
assert abs(tot / T - float(key)) < 0.01
check('4p03', 'key', key, enum)
check('4p03', 'one-box', F(7, 8) ** 12, F(7 ** 12, 8 ** 12))
check('4p03', 'filled', 8 - key, 8 - enum)
check('4p03', 'eighth-power', 8 * F(7, 8) ** 8, F(8 * 7 ** 8, 8 ** 8))

# 4p04 two independent flags, sens 0.9, fp 0.08, base 0.02
s, fp, b = F(9, 10), F(8, 100), F(2, 100)
post = b * s * s / (b * s * s + (1 - b) * fp * fp)
odds = (b / (1 - b)) * (s / fp) ** 2
check('4p04', 'key', post, odds / (1 + odds))
check('4p04', 'one-screen', b * s / (b * s + (1 - b) * fp), F(18, 1000) / (F(18, 1000) + F(784, 10000)))
check('4p04', 'no-base', s * s / (s * s + fp * fp), F(81, 100) / (F(81, 100) + F(64, 10000)))
check('4p04', 'sens-squared', s * s, F(81, 100))

# 4p05 first of three exponential alarms, rates 2, 3, 5 an hour, in minutes
check('4p05', 'key', F(60, 10), F(60) / (2 + 3 + 5))
rng = random.Random(5); T = 400000
m = sum(min(rng.expovariate(2), rng.expovariate(3), rng.expovariate(5)) for _ in range(T)) / T * 60
assert abs(m - 6) < 0.05, m
check('4p05', 'mean-of-means', F(60) * (F(1, 2) + F(1, 3) + F(1, 5)) / 3, F(62, 3))
check('4p05', 'fastest-only', F(60, 5), F(12))
check('4p05', 'add-means', F(60) * (F(1, 2) + F(1, 3) + F(1, 5)), F(62))
check('4p05', 'avg-rate', F(60) / (F(10, 3)), F(18))

# 4p06 trains 120 miles apart at 40 mph each, fly at 90 mph
t = F(120, 80)
# second way: sum the zigzag legs as a series
pos_gap, total = F(120), F(0)
for _ in range(200):
    leg_t = pos_gap / (90 + 40)          # fly meets the oncoming train
    total += 90 * leg_t
    pos_gap -= 80 * leg_t
check('4p06', 'key', 90 * t, total, tol=1e-6)
check('4p06', 'one-train', 90 * F(120, 40), F(270))
check('4p06', 'gap', F(120), F(120))
check('4p06', 'meeting-point', F(60), 40 * t)

# 4p07 60 cm stick, one break, longer piece (choice)
check('4p07', 'key', F(45), sum(max(F(k, 1000), 60 - F(k, 1000)) for k in range(0, 60000)) / 60000, tol=1e-3)
check('4p07', 'random-piece', F(30), F(60, 2))
emax2 = F(2, 3) * 60   # E max of two independent U(0, 60)
rng = random.Random(7); T = 200000
assert abs(sum(max(rng.random(), rng.random()) for _ in range(T)) / T * 60 - 40) < 0.1
check('4p07', 'independent-max', emax2, F(40))
check('4p07', 'three-pieces', F(11, 18) * 60, F(110, 3))
rng = random.Random(8); tot = 0
for _ in range(T):
    x, y = sorted((rng.random(), rng.random())); tot += max(x, y - x, 1 - y)
assert abs(tot / T * 60 - 110 / 3) < 0.1

# 4p08 capture-recapture
check('4p08', 'key', F(50 * 40, 8), F(50) / F(8, 40))
check('4p08', 'flipped', F(50 * 8, 40), F(10))
check('4p08', 'seen-only', F(50 + 40 - 8), F(82))
check('4p08', 'catch-ratio', F(40 * 40, 8), F(200))

# 4p09 truel: A 0.4, B 0.7, C 1, order A, B, C; B and C aim at each other
pa, pb, pc = F(2, 5), F(7, 10), F(1)
def duel(p, q):   # first shooter p, second q, alternate
    return p / (1 - (1 - p) * (1 - q))
after_air = pb * duel(pa, pb) + (1 - pb) * pc * pa       # B hits C -> A first vs B; else C kills B, A one shot
aim_c = pa * ((1 - pb) * duel(pa, pb)) + (1 - pa) * after_air
aim_b = pa * 0 + (1 - pa) * after_air
# second way: value iteration over the full game (A chooses each turn while all three alive)
def truel_mc(first, trials, seed):
    rng = random.Random(seed); wins = 0
    for _ in range(trials):
        alive = {'A', 'B', 'C'}; turn = 0; firstshot = True
        while len(alive) > 1:
            sh = 'ABC'[turn % 3]; turn += 1
            if sh not in alive: continue
            if sh == 'A':
                if len(alive) == 3:
                    tgt = first if firstshot else None
                    firstshot = False
                else:
                    tgt = (alive - {'A'}).pop()
                if tgt and rng.random() < pa: alive.discard(tgt)
            elif sh == 'B':
                tgt = 'C' if 'C' in alive else 'A'
                if rng.random() < pb: alive.discard(tgt)
            else:
                tgt = 'B' if 'B' in alive else 'A'
                alive.discard(tgt)
        wins += 'A' in alive
    return wins / trials
check('4p09', 'key-air', after_air, F(473, 1025))
check('4p09', 'aim-c', aim_c, F(2, 5) * F(3, 10) * F(20, 41) + F(3, 5) * F(473, 1025))
check('4p09', 'aim-b', aim_b, F(3, 5) * F(473, 1025))
for tgt, exact in ((None, after_air), ('C', aim_c), ('B', aim_b)):
    est = truel_mc(tgt, 200000, 9)
    assert abs(est - float(exact)) < 0.005, (tgt, est, float(exact))
assert after_air > aim_c > aim_b

# 4p10 take 1, 2 or 5 from 40, last counter wins
def losing(n, moves):
    L = []
    for k in range(n + 1):
        L.append(all(L[k - m] is False for m in moves if m <= k) if k else True)
        L[k] = not any(L[k - m] for m in moves if m <= k) if k else True
    return L
L = losing(40, (1, 2, 5))
assert [k for k in range(41) if L[k]] == [k for k in range(41) if k % 3 == 0]
good = [m for m in (1, 2, 5) if L[40 - m]]
check('4p10', 'key', F(good[0]), F(40 % 3)); assert good == [1]
check('4p10', 'mod-six', F(40 % 6), F(4))
check('4p10', 'most', F(5), F(5))
check('4p10', 'two', F(2), F(2))

# 4p11 three dice total 10, first shows 3: others are (3, 4) in some order
rolls3 = [r for r in product(range(1, 7), repeat=3) if sum(r) == 10]
cond = [r for r in rolls3 if r[0] == 3]
hit = [r for r in cond if sorted(r[1:]) == [3, 4]]
check('4p11', 'key', F(len(hit), len(cond)), F(2, 6))
check('4p11', 'one-order', F(1, 6), F(1, len(cond)))
check('4p11', 'whole-table', F(2, 36), F(len(hit), 36))
check('4p11', 'forgot-first', F(len(hit), len(rolls3)), F(2, 27))
assert len(rolls3) == 27

# 4p12 Kelly at evens, p = 0.62, twice Kelly
p = 0.62; fk = 2 * p - 1
g = lambda f: p * log(1 + f) + (1 - p) * log(1 - f)
rng = random.Random(12); T = 2000000
mc = sum(log(1 + 2 * fk) if rng.random() < p else log(1 - 2 * fk) for _ in range(T)) / T
assert abs(mc - g(2 * fk)) < 0.002, mc
check('4p12', 'kelly-fraction', fk, 0.24, tol=1e-12)
check('4p12', 'key-g-2k', g(0.48), 0.62 * 0.39204208777602367 + 0.38 * -0.6539264674066639, tol=1e-12)
check('4p12', 'g-kelly', g(0.24), 0.62 * log(1.24) + 0.38 * log(0.76))
check('4p12', 'twice-g', 2 * g(0.24), 2 * (0.62 * log(1.24) + 0.38 * log(0.76)))
# the parabola g(f) ~ f*edge - f^2/2 is zero at twice Kelly
check('4p12', 'parabola', 0.48 * 0.24 - 0.48 ** 2 / 2, 0.0)
assert g(0.48) < 0

# ---------- brainteasers-4 ----------
# 4b01 twelve coins, heavy or light, three weighings: state search over (u, h, l, g)
from functools import lru_cache
@lru_cache(None)
def solvable(u, h, l, g, k):
    cases = 2 * u + h + l
    if cases <= 1: return True
    if cases > 3 ** k: return False
    for u1 in range(u + 1):
        for u2 in range(u - u1 + 1):
            for h1 in range(h + 1):
                for h2 in range(h - h1 + 1):
                    for l1 in range(l + 1):
                        for l2 in range(l - l1 + 1):
                            n1 = u1 + h1 + l1; n2 = u2 + h2 + l2
                            if n1 == 0 and n2 == 0: continue
                            d = n1 - n2
                            g1 = max(0, -d); g2 = max(0, d)
                            if g1 + g2 > g: continue
                            outs = [(0, u1 + h1, u2 + l2), (0, u2 + h2, u1 + l1), (u - u1 - u2, h - h1 - h2, l - l1 - l2)]
                            if all(solvable(a, bb, c, 12 - a - bb - c, k - 1) for a, bb, c in outs):
                                return True
    return False
# helper to evaluate a given first plan exactly
def plan_ok(first_left, first_right, second_if_level):
    # first weighing on 12 unknown coins
    tilt = (0, first_left, first_right)          # left heavy: left coins maybe heavy, right maybe light
    rest = 12 - first_left - first_right
    ok_tilt = solvable(0, first_left, first_right, 12 - first_left - first_right, 2)
    if second_if_level is None:
        ok_level = solvable(rest, 0, 0, 12 - rest, 2)
    else:
        a_unknown, b_unknown, a_genuine = second_if_level     # left: a_unknown + a_genuine ; right: b_unknown
        tl = solvable(0, a_unknown, b_unknown, 12, 1)
        tr = solvable(0, b_unknown, a_unknown, 12, 1)
        lv = solvable(rest - a_unknown - b_unknown, 0, 0, 12, 1)
        ok_level = tl and tr and lv
    return ok_tilt and ok_level
assert solvable(12, 0, 0, 0, 3)
check('4b01', 'key-4v4-then-3-v-3genuine', F(int(plan_ok(4, 4, (3, 0, 3)))), F(1))
check('4b01', 'six-v-six', F(int(plan_ok(6, 6, None))), F(0))
check('4b01', 'three-v-three', F(int(plan_ok(3, 3, None))), F(0))
check('4b01', '4v4-then-2v2', F(int(plan_ok(4, 4, (2, 2, 0)))), F(0))
check('4b01', 'cases-after-6v6-tilt', F(12), F(6 + 6)); assert 12 > 3 ** 2
check('4b01', 'cases-after-3v3-level', F(12), F(2 * 6))

# 4b02 five pirates, 80 coins, strict majority, bloodthirsty tiebreak
def pirates(n, coins, strict):
    # returns allocation list for pirates in seniority order among n alive (index 0 proposes), or None if proposer dies
    alloc = {1: [coins]}
    for m in range(2, n + 1):
        fallback = [None] + alloc[m - 1]          # pirate 0 dies -> others get fallback (None = dead, at m-1 his slot)
        # fallback for each other pirate j (1..m-1): coins under m-1 plan, or None if that plan kills its proposer (j=1)
        need = (m // 2 + 1) if strict else ((m + 1) // 2)
        votes_needed = need - 1
        prices = []
        for j in range(1, m):
            fb = fallback[j]
            if fb is None: prices.append((0, j))       # would die otherwise: votes yes for 0
            else: prices.append((fb + 1, j))
        prices.sort()
        buy = prices[:votes_needed]
        cost = sum(c for c, _ in buy)
        if cost <= coins:
            a = [0] * m; a[0] = coins - cost
            for c, j in buy: a[j] = c
            alloc[m] = a
        else:
            alloc[m] = [None] + alloc[m - 1]
        # proposer death in the m-1 plan is represented by None at index 0 of alloc[m-1]
    return alloc
def pirates_brute(n, coins, strict):
    # exhaustive search over allocations for small coin totals is too big; check by full game tree on 5 pirates with
    # vote rules: a voter says yes iff his coins under the plan exceed his outcome if it fails (dead counts as -1)
    memo = {}
    def outcome(m):
        if m in memo: return memo[m]
        if m == 1: memo[1] = [coins]; return memo[1]
        fail = [None] + outcome(m - 1)
        need = (m // 2 + 1) if strict else ((m + 1) // 2)
        best = None
        # search every allocation to the others with coins only to the cheapest voters, small enough: 0..3 each
        for a in product(range(0, 4), repeat=m - 1):
            if sum(a) > coins: continue
            yes = 1 + sum(1 for j in range(1, m) if (a[j - 1] > (fail[j] if fail[j] is not None else -1)))
            if yes >= need:
                keep = coins - sum(a)
                if best is None or keep > best[0]: best = [keep] + list(a)
        memo[m] = best if best else [None] + outcome(m - 1)
        return memo[m]
    return outcome(n)
A = pirates(5, 80, True)[5]
B = pirates_brute(5, 80, True)
check('4b02', 'key', F(A[0]), F(B[0])); assert A[0] == 77
check('4b02', 'tie-passes', F(pirates(5, 80, False)[5][0]), F(pirates_brute(5, 80, False)[0]))
assert pirates(5, 80, False)[5][0] == 78
check('4b02', 'four-aboard', F(pirates(4, 80, True)[4][0]), F(78))
check('4b02', 'pay-two-each', F(80 - 4), F(76))

# 4b03 three eggs, 170 floors
def f(d, e): return sum(comb(d, i) for i in range(1, e + 1))
@lru_cache(None)
def drops(eggs, floors):
    if floors == 0: return 0
    if eggs == 1: return floors
    return 1 + min(max(drops(eggs - 1, x - 1), drops(eggs, floors - x)) for x in range(1, floors + 1))
key = min(d for d in range(1, 50) if f(d, 3) >= 170)
check('4b03', 'key', F(key), F(drops(3, 170)))
check('4b03', 'nine', F(9), F(9)); assert f(9, 3) == 129 < 170 <= f(10, 3) == 175
check('4b03', 'two-eggs', F(min(d for d in range(1, 50) if f(d, 2) >= 170)), F(drops(2, 170)))
check('4b03', 'halving', F(8), F(len(bin(170)) - 2))

# 4b04 farmer, fox, hen, grain: BFS
from collections import deque
items = ('farmer', 'fox', 'hen', 'grain')
def safe(side):
    if 'farmer' in side: return True
    return not ({'fox', 'hen'} <= side or {'hen', 'grain'} <= side)
start = frozenset(items); goal = frozenset()
dist = {start: 0}; q = deque([start])
while q:
    left = q.popleft()
    farmer_left = 'farmer' in left
    here = left if farmer_left else frozenset(items) - left
    for cargo in [None] + [x for x in here if x != 'farmer']:
        move = {'farmer'} | ({cargo} if cargo else set())
        nl = left - move if farmer_left else left | move
        right = frozenset(items) - nl
        if safe(nl) and safe(right) and nl not in dist:
            dist[nl] = dist[left] + 1; q.append(nl)
check('4b04', 'key', F(dist[goal]), F(7))
check('4b04', 'no-returns-with-cargo', F(5), F(2 * 3 - 1))
check('4b04', 'once-each', F(3), F(3))

# 4b05 37 teams knockout
def knockout(n):
    m = 0
    while n > 1: m += n // 2; n = n - n // 2
    return m
check('4b05', 'key', F(knockout(37)), F(36))
check('4b05', 'one-each', F(37), F(37))
check('4b05', 'first-round', F(37 // 2), F(18))
check('4b05', 'league', F(comb(37, 2)), F(666))

# 4b06 board 1, 1/2, ..., 1/9, move a + b + ab
nums = [F(1, k) for k in range(1, 10)]
prod_ = F(1)
for x in nums: prod_ *= (x + 1)
for seed in range(20):
    rng = random.Random(seed); b_ = nums[:]
    while len(b_) > 1:
        i, j = rng.sample(range(len(b_)), 2); a1, a2 = b_[i], b_[j]
        b_ = [x for t_, x in enumerate(b_) if t_ not in (i, j)] + [a1 + a2 + a1 * a2]
    assert b_[0] == prod_ - 1
check('4b06', 'key', prod_ - 1, F(9))
check('4b06', 'sum', sum(nums), F(7129, 2520))
check('4b06', 'no-minus', prod_, F(10))

# 4b07 splitting a pile of 30: number of moves always 29
for seed in range(50):
    rng = random.Random(seed); piles = [30]; mv = 0
    while any(p_ >= 2 for p_ in piles):
        i = rng.choice([t_ for t_, p_ in enumerate(piles) if p_ >= 2]); p_ = piles.pop(i)
        a1 = rng.randint(1, p_ - 1); piles += [a1, p_ - a1]; mv += 1
    assert mv == 29
check('4b07', 'key-moves', F(29), F(30 - 1))
check('4b07', 'halving', F(5), F(len(bin(30)) - 2 - 0))

# 4b08 fifteen hats, Hamming code strategy
def hamming_codeword(x, n=15):
    s = 0
    for i in range(n):
        if x >> i & 1: s ^= (i + 1)
    return s == 0
codewords = sum(hamming_codeword(x) for x in range(2 ** 15))
assert codewords == 2 ** 11
def play(x, n=15):
    guesses = []
    for i in range(n):
        x0, x1 = x & ~(1 << i), x | (1 << i)
        c0, c1 = hamming_codeword(x0), hamming_codeword(x1)
        if c0 and not c1: guesses.append((i, 1))
        elif c1 and not c0: guesses.append((i, 0))
    return bool(guesses) and all((x >> i & 1) == v for i, v in guesses)
wins = sum(play(x) for x in range(2 ** 15))
check('4b08', 'key', F(wins, 2 ** 15), 1 - F(2 ** 11, 2 ** 15))
assert F(wins, 2 ** 15) == F(15, 16)
# three players: brute force every strategy profile proves 3/4 is best
views = list(product((0, 1), repeat=2))
best3 = F(0)
choices = list(product((None, 0, 1), repeat=4))
pats = list(product((0, 1), repeat=3))
def team_win(strats):
    w = 0
    for pat in pats:
        gs = []
        for i in range(3):
            others = tuple(pat[j] for j in range(3) if j != i)
            gs.append((i, strats[i][views.index(others)]))
        act = [(i, v) for i, v in gs if v is not None]
        w += bool(act) and all(pat[i] == v for i, v in act)
    return F(w, 8)
# full 81^3 search is 531441 profiles: run it
best3 = F(0)
for a in choices:
    for b_ in choices:
        for c in choices:
            v = team_win((a, b_, c))
            if v > best3: best3 = v
check('4b08', 'three-players-best', best3, F(3, 4))
check('4b08', 'one-guesser', F(1, 2), F(1, 2))
check('4b08', 'seven', F(7, 8), 1 - F(2 ** 4, 2 ** 7))

# 4b09 seven marked of fifty: possible-worlds simulation on a smaller village (n = 10, k = 7)
def leave_evening(n, marked):
    worlds = [w for w in product((0, 1), repeat=n) if any(w)]          # the mayor's words remove all-unmarked
    actual = tuple(1 if i < marked else 0 for i in range(n))
    alive = set(worlds)
    for evening in range(1, n + 2):
        def knows(w, i):   # i knows own mark in w if every world alive that agrees off i has w_i = 1
            alt = tuple(1 - w[j] if j == i else w[j] for j in range(n))
            return w[i] == 1 and alt not in alive
        if any(knows(actual, i) for i in range(n)): return evening
        # nobody left: remove every world in which someone would have known
        alive = {w for w in alive if not any(knows(w, i) for i in range(n))}
    return None
check('4b09', 'key', F(leave_evening(10, 7)), F(7))
check('4b09', 'small-check', F(leave_evening(8, 3)), F(3))
check('4b09', 'seen', F(6), F(7 - 1))
check('4b09', 'late', F(8), F(7 + 1))

# 4b10 missing information (choice): the numbers in the options
check('4b10', 'naive', F(40) * (F(28, 10) - F(25, 10)), F(12))
check('4b10', 'lots', F(40 * 100) * (F(28, 10) - F(25, 10)), F(1200))

# ---------- mental-4 ----------
check('4m01', 'key', F(97 * 53), F(5300 - 159))
check('4m01', 'sub-three', F(5300 - 3), F(5297))
check('4m01', 'added', F(5300 + 159), F(5459))
check('4m02', 'key', F(7448, 28), F(1862, 7)); assert 7448 % 28 == 0 and 7448 // 28 == 266
check('4m02', 'place-down', F(266, 10), F(7448, 280))
check('4m02', 'place-up', F(2660), F(74480, 28))
check('4m03', 'key', F(35, 65), 1 / F(65, 100) - 1)
assert round(float(F(35, 65)) * 100) == 54
check('4m03', 'same', F(35, 100), F(35, 100))
check('4m03', 'over-135', F(35, 135), F(7, 27))
fr = {'5/7': F(5, 7), '8/11': F(8, 11), '13/18': F(13, 18)}
order = sorted(fr, key=fr.get)
check('4m04', 'middle-is-13/18', F(int(order[1] == '13/18')), F(1))
check('4m04', 'gaps', 1 - F(13, 18), F(5, 18)); assert F(3, 11) < F(5, 18) < F(2, 7)
check('4m05', 'key', F(481, 10000) * 2060, F(481 * 206, 1000)); assert round(481 * 2060 / 10000, 2) == 99.09
check('4m05', 'drop-digit', F(48, 1000) * 2060, F(9888, 100))
check('4m05', 'drop-60', F(481, 10000) * 2000, F(962, 10))
check('4m05', 'place', F(481, 1000) * 2060, F(99086, 100))
seq = [1]
while len(seq) < 12: seq.append(2 * seq[-1] + 1)
assert seq[:6] == [1, 3, 7, 15, 31, 63]
check('4m06', 'key', F(seq[11]), F(2 ** 12 - 1))
check('4m06', 'eleventh', F(seq[10]), F(2 ** 11 - 1))
check('4m06', 'power', F(2 ** 12), F(4096))
check('4m06', 'next', F(seq[6]), F(127))
r = 49 - F(1, 98)
check('4m07', 'key-newton', r, F(4801, 98))
check('4m07', 'true-root', sqrt(2400), 48.98979485566356)
assert round(sqrt(2400), 1) == 49.0 and abs(float(r) - sqrt(2400)) < 1e-4
check('4m07', 'root-24', round(sqrt(24), 1), 4.9)
check('4m07', 'root-240', round(sqrt(240), 1), 15.5)
check('4m08', 'key', 1 / (F(1, 12) - F(1, 20)), F(30))
check('4m08', 'added', 1 / (F(1, 12) + F(1, 20)), F(15, 2))
check('4m08', 'difference', F(20 - 12), F(8))
check('4m08', 'average', F(12 + 20, 2), F(16))
fl = list(product((0, 1), repeat=4))
check('4m09', 'key', F(sum(sum(x) >= 2 for x in fl), 16), F(16 - 1 - 4, 16))
check('4m09', 'exactly-two', F(sum(sum(x) == 2 for x in fl), 16), F(comb(4, 2), 16))
check('4m09', 'at-least-one', F(sum(sum(x) >= 1 for x in fl), 16), 1 - F(1, 16))
check('4m09', 'at-most-one', F(sum(sum(x) <= 1 for x in fl), 16), F(5, 16))
s1 = F(3, 8) * 96; s2 = s1 * F(5, 4); s3 = s2 * 16
sq = [4, 9, 16, 25]; nxt = 36
s4 = s3 - nxt
pdouble = F(sum(a == b for a, b in product(range(1, 7), repeat=2)), 36)
s5 = s4 * pdouble
check('4m10', 'key', s5, F((720 - 36), 6))
assert (s1, s2, s3, s4) == (36, 45, 720, 684)
check('4m10', 'next-square-49', (s3 - 49) * pdouble, F(671, 6))
check('4m10', 'one-in-36', s4 / 36, F(19))
check('4m10', 'quarter-of', (s1 * F(1, 4) * 16 - 36) * pdouble, F(18))

# ---------- market-making-4 ----------
deck = [r for r in range(1, 14) for _ in range(4)]
seen = [13, 12, 9, 4, 1]
left = deck[:]
for c in seen: left.remove(c)
check('4k01', 'key', F(sum(left), len(left)), F(364 - 39, 47))
check('4k01', 'full-deck', F(sum(deck), 52), F(7))
check('4k01', 'over-52', F(sum(left), 52), F(325, 52))
check('4k01', 'seen-mean', F(sum(seen), 5), F(39, 5))
prod_vals = [a * b for a in range(1, 5) for b in range(1, 9)]
check('4k02', 'key', F(sum(prod_vals), 32), F(5, 2) * F(9, 2))
check('4k02', 'range-mid', F(1 + 32, 2), F(33, 2))
check('4k02', 'added', F(5, 2) + F(9, 2), F(7))
loss = 111 - 102
check('4k03', 'key', F(-(-loss // 2)), F(5)); assert 4 * 2 < loss <= 5 * 2
check('4k03', 'fraction', F(loss, 2), F(9, 2))
check('4k03', 'from-fair', F(-(-(111 - 100) // 2)), F(6))
check('4k03', 'full-width', F(-(-loss // 4)), F(3))
pos = [9, 9 - 4, 9 - 4 + 3]; assert max(abs(x) for x in pos) <= 10
assert 9 + 3 > 10
check('4k04', 'path-sell-first', F(pos[2]), F(8))
check('4k04', 'buy-first-peak', F(9 + 3), F(12))
check('4k05', 'key', F(40 * 100) * F(35, 100), F(1400))
check('4k05', 'per-share', F(40) * F(35, 100), F(14))
check('4k05', 'no-delta', F(4000), F(40 * 100))
check('4k05', 'one-minus', F(4000) * F(65, 100), F(2600))
bids, offers = [28, 33, 30], [30, 35, 32]
check('4k06', 'offers-sum', F(sum(offers)), F(97))
check('4k06', 'profit', F(100 - sum(offers)), F(3))
check('4k06', 'sell-at-bids', F(sum(bids) - 100), F(-9))
pay = [max(k * k - 10, 0) for k in range(1, 7)]
check('4k07', 'key', F(sum(pay), 6) - 5, F(17, 6))
check('4k07', 'payout', F(sum(pay), 6), F(6 + 15 + 26, 6))
check('4k07', 'negatives', F(sum(k * k - 10 for k in range(1, 7)), 6) - 5, F(91, 6) - 15)
check('4k07', 'square-mean', F(7, 2) ** 2 - 10 - 5, F(-11, 4))
check('4k07', 'no-cost', F(sum(pay), 6), F(47, 6))
pmf = [comb(60, k) * F(9, 10) ** k * F(1, 10) ** (60 - k) for k in range(61)]
tail = sum(pmf[:46])
rng = random.Random(8); T = 200000
mc = sum(sum(rng.random() < 0.9 for _ in range(60)) <= 45 for _ in range(T)) / T
assert abs(mc - float(tail)) < 0.0015, (mc, float(tail))
check('4k08', 'hit-rate', F(45, 60), F(3, 4))
check('4k08', 'expected-hits', F(60) * F(9, 10), F(54))
check('4k08', 'sd-hits', sqrt(60 * 0.9 * 0.1), sqrt(5.4))
check('4k08', 'sds-short', (54 - 45) / sqrt(5.4), 9 / 2.32379000772445, tol=1e-9)
check('4k08', 'tail-p', tail, sum(pmf[k] for k in range(0, 46)))
N[('4k08', 'tail-float')] = float(tail)

# ---------- behavioural-4: the one maths figure in a model (4h10) ----------
check('4h10', 'max-two-dice', F(sum(max(a, b) for a, b in product(range(1, 7), repeat=2)), 36), F(161, 36))
check('4h10', 'max-three-dice', F(sum(max(t) for t in product(range(1, 7), repeat=3)), 216), 6 - F(225, 216))

if __name__ == '__main__':
    for ref, name, a, b in ROWS:
        print(f'{ref:5} {name:30} {a:14.6f}  check {b:14.6f}')
    print(f'all {len(ROWS)} checks passed')
```

### Its output

```text
4p01  key                                  8.833333  check       8.833333
4p01  two-rolls                            8.000000  check       8.000000
4p01  one-roll                             6.500000  check       6.500000
4p01  first-vs-fresh                       8.750000  check       8.750000
4p01  best-of-three                        9.479167  check       9.479167
4p02  rolls                               14.700000  check      14.700000
4p02  key                                  2.950000  check       2.950000
4p02  six-rolls                           16.000000  check      16.000000
4p02  thirty-six                         -29.000000  check     -29.000000
4p02  skip-first                           4.450000  check       4.450000
4p03  key                                  1.611338  check       1.611338
4p03  one-box                              0.201417  check       0.201417
4p03  filled                               6.388662  check       6.388662
4p03  eighth-power                         2.748871  check       2.748871
4p04  key                                  0.720897  check       0.720897
4p04  one-screen                           0.186722  check       0.186722
4p04  no-base                              0.992161  check       0.992161
4p04  sens-squared                         0.810000  check       0.810000
4p05  key                                  6.000000  check       6.000000
4p05  mean-of-means                       20.666667  check      20.666667
4p05  fastest-only                        12.000000  check      12.000000
4p05  add-means                           62.000000  check      62.000000
4p05  avg-rate                            18.000000  check      18.000000
4p06  key                                135.000000  check     135.000000
4p06  one-train                          270.000000  check     270.000000
4p06  gap                                120.000000  check     120.000000
4p06  meeting-point                       60.000000  check      60.000000
4p07  key                                 45.000000  check      45.000000
4p07  random-piece                        30.000000  check      30.000000
4p07  independent-max                     40.000000  check      40.000000
4p07  three-pieces                        36.666667  check      36.666667
4p08  key                                250.000000  check     250.000000
4p08  flipped                             10.000000  check      10.000000
4p08  seen-only                           82.000000  check      82.000000
4p08  catch-ratio                        200.000000  check     200.000000
4p09  key-air                              0.461463  check       0.461463
4p09  aim-c                                0.335415  check       0.335415
4p09  aim-b                                0.276878  check       0.276878
4p10  key                                  1.000000  check       1.000000
4p10  mod-six                              4.000000  check       4.000000
4p10  most                                 5.000000  check       5.000000
4p10  two                                  2.000000  check       2.000000
4p11  key                                  0.333333  check       0.333333
4p11  one-order                            0.166667  check       0.166667
4p11  whole-table                          0.055556  check       0.055556
4p11  forgot-first                         0.074074  check       0.074074
4p12  kelly-fraction                       0.240000  check       0.240000
4p12  key-g-2k                            -0.005426  check      -0.005426
4p12  g-kelly                              0.029083  check       0.029083
4p12  twice-g                              0.058166  check       0.058166
4p12  parabola                             0.000000  check       0.000000
4b01  key-4v4-then-3-v-3genuine            1.000000  check       1.000000
4b01  six-v-six                            0.000000  check       0.000000
4b01  three-v-three                        0.000000  check       0.000000
4b01  4v4-then-2v2                         0.000000  check       0.000000
4b01  cases-after-6v6-tilt                12.000000  check      12.000000
4b01  cases-after-3v3-level               12.000000  check      12.000000
4b02  key                                 77.000000  check      77.000000
4b02  tie-passes                          78.000000  check      78.000000
4b02  four-aboard                         78.000000  check      78.000000
4b02  pay-two-each                        76.000000  check      76.000000
4b03  key                                 10.000000  check      10.000000
4b03  nine                                 9.000000  check       9.000000
4b03  two-eggs                            18.000000  check      18.000000
4b03  halving                              8.000000  check       8.000000
4b04  key                                  7.000000  check       7.000000
4b04  no-returns-with-cargo                5.000000  check       5.000000
4b04  once-each                            3.000000  check       3.000000
4b05  key                                 36.000000  check      36.000000
4b05  one-each                            37.000000  check      37.000000
4b05  first-round                         18.000000  check      18.000000
4b05  league                             666.000000  check     666.000000
4b06  key                                  9.000000  check       9.000000
4b06  sum                                  2.828968  check       2.828968
4b06  no-minus                            10.000000  check      10.000000
4b07  key-moves                           29.000000  check      29.000000
4b07  halving                              5.000000  check       5.000000
4b08  key                                  0.937500  check       0.937500
4b08  three-players-best                   0.750000  check       0.750000
4b08  one-guesser                          0.500000  check       0.500000
4b08  seven                                0.875000  check       0.875000
4b09  key                                  7.000000  check       7.000000
4b09  small-check                          3.000000  check       3.000000
4b09  seen                                 6.000000  check       6.000000
4b09  late                                 8.000000  check       8.000000
4b10  naive                               12.000000  check      12.000000
4b10  lots                              1200.000000  check    1200.000000
4m01  key                               5141.000000  check    5141.000000
4m01  sub-three                         5297.000000  check    5297.000000
4m01  added                             5459.000000  check    5459.000000
4m02  key                                266.000000  check     266.000000
4m02  place-down                          26.600000  check      26.600000
4m02  place-up                          2660.000000  check    2660.000000
4m03  key                                  0.538462  check       0.538462
4m03  same                                 0.350000  check       0.350000
4m03  over-135                             0.259259  check       0.259259
4m04  middle-is-13/18                      1.000000  check       1.000000
4m04  gaps                                 0.277778  check       0.277778
4m05  key                                 99.086000  check      99.086000
4m05  drop-digit                          98.880000  check      98.880000
4m05  drop-60                             96.200000  check      96.200000
4m05  place                              990.860000  check     990.860000
4m06  key                               4095.000000  check    4095.000000
4m06  eleventh                          2047.000000  check    2047.000000
4m06  power                             4096.000000  check    4096.000000
4m06  next                               127.000000  check     127.000000
4m07  key-newton                          48.989796  check      48.989796
4m07  true-root                           48.989795  check      48.989795
4m07  root-24                              4.900000  check       4.900000
4m07  root-240                            15.500000  check      15.500000
4m08  key                                 30.000000  check      30.000000
4m08  added                                7.500000  check       7.500000
4m08  difference                           8.000000  check       8.000000
4m08  average                             16.000000  check      16.000000
4m09  key                                  0.687500  check       0.687500
4m09  exactly-two                          0.375000  check       0.375000
4m09  at-least-one                         0.937500  check       0.937500
4m09  at-most-one                          0.312500  check       0.312500
4m10  key                                114.000000  check     114.000000
4m10  next-square-49                     111.833333  check     111.833333
4m10  one-in-36                           19.000000  check      19.000000
4m10  quarter-of                          18.000000  check      18.000000
4k01  key                                  6.914894  check       6.914894
4k01  full-deck                            7.000000  check       7.000000
4k01  over-52                              6.250000  check       6.250000
4k01  seen-mean                            7.800000  check       7.800000
4k02  key                                 11.250000  check      11.250000
4k02  range-mid                           16.500000  check      16.500000
4k02  added                                7.000000  check       7.000000
4k03  key                                  5.000000  check       5.000000
4k03  fraction                             4.500000  check       4.500000
4k03  from-fair                            6.000000  check       6.000000
4k03  full-width                           3.000000  check       3.000000
4k04  path-sell-first                      8.000000  check       8.000000
4k04  buy-first-peak                      12.000000  check      12.000000
4k05  key                               1400.000000  check    1400.000000
4k05  per-share                           14.000000  check      14.000000
4k05  no-delta                          4000.000000  check    4000.000000
4k05  one-minus                         2600.000000  check    2600.000000
4k06  offers-sum                          97.000000  check      97.000000
4k06  profit                               3.000000  check       3.000000
4k06  sell-at-bids                        -9.000000  check      -9.000000
4k07  key                                  2.833333  check       2.833333
4k07  payout                               7.833333  check       7.833333
4k07  negatives                            0.166667  check       0.166667
4k07  square-mean                         -2.750000  check      -2.750000
4k07  no-cost                              7.833333  check       7.833333
4k08  hit-rate                             0.750000  check       0.750000
4k08  expected-hits                       54.000000  check      54.000000
4k08  sd-hits                              2.323790  check       2.323790
4k08  sds-short                            3.872983  check       3.872983
4k08  tail-p                               0.000666  check       0.000666
4h10  max-two-dice                         4.472222  check       4.472222
4h10  max-three-dice                       4.958333  check       4.958333
all 154 checks passed
```

### Final run of `play-bank.mjs`

```text
locked before 86, after 45; drawable 292; session-4 items drawable 50 of 50; 19 requires lessons
pass 0 (right): 50 of 50 distinct items played and accepted
pass 1 (wrong #1): 40 wrong answers routed or checked, 40 expected
pass 2 (wrong #2): 40 wrong answers routed or checked, 40 expected
pass 3 (wrong #3): 34 wrong answers routed or checked, 34 expected
pass 4 (wrong #4): 2 wrong answers routed or checked, 2 expected
wrong ids and distractors in the files: 116; routed: 116
choice items: 12; seen in more than one option order so far: 12; each with exactly one correct in the file: true
no console errors
ALL OK
EXIT 0
```

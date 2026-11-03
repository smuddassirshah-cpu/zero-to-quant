# Answer check, 3 November 2026 (bank part 1, sessions 2 to 4)

**File name.** The brief asked for `answers-2026-11-03.md`, but that name is already a committed review (answer check part 1: mental-pressure, puzzles and topic 0.5). To avoid overwriting it, this review is `answers-2026-11-03-bank.md`. Rename it if you prefer another scheme.

**Summary.** 150 items checked: the 15 files `probability`, `brainteasers`, `mental`, `market-making` and `behavioural` `-2`, `-3` and `-4` (probability 41, brainteasers 30, mental 30, market making 24, behavioural 25; 85 numeric, 39 choice, 1 expression, 25 longform). 233 numeric `wrong` values, 117 choice distractors and 2 expression `wrong` forms checked against their `why` or `byKey` line. Wrong keys: 0. Other findings: 2 distractor whys that do not fit their option, 1 wording claim, 2 format points, 9 duplicates (3 exact, 6 same set-up and key), plus notes and the two rulings you asked for.

I recomputed every key from the question text before reading any explanation, then compared with explanations, feedback, `accept` lines and the author reports `docs/reports/bank-1-2.md` to `bank-1-4.md`. Every figure the explanations state also agrees with mine (checked line by line; no stale number found).

Scripts are in the scratchpad folder `/tmp/claude-0/-home-user-zero-to-quant/4b8cce5e-d242-5446-84a4-7179e480b15a/scratchpad/answers`:

- `prob.py`, `prob3.py` and `p2b.py` recompute the probability keys with `Fraction`s, enumeration (all 216 three-dice rolls, all 5-card orders), dynamic programs (the three-red-two-black stopping game, the twelve-sided die with one and two rerolls) and closed forms. `sim.py` is the second check, two million numpy draws or 100,000 to 400,000 Python runs per item: 40 probability items, all within sampling error of the key (the truel at 0.4622, 0.3355 and 0.2763 for the three first moves; the estimator mean for five tickets from 100 is 99.997).
- `bt.py` searches the brainteasers: hourglass states (breadth first, so the fewest turns is 4), a backward-induction pirate solver with strict majority (77), an exact egg-drop table and a brute-force egg DP (10), a simulation of 200 prisoners (0.3092), brute force over all 6^6 hat assignments for the modulo plan (wins always; "everyone aims at total 0" wins 1/6; "prisoner k guesses k" wins 0.665), the fox, hen and grain search (7), list scheduling (11) and exhaustive splits (8).
- `mm.py` recomputes the market-making keys (card values, digit count, intervals with exact binomial tails, the call, the ledger).
- `tolscan.py` checks every numeric key band against its wrong bands and the wrong bands against each other. `structchk.py` and `brief_cmp.py` check shape and compare every item with its row in `docs/briefs/bank.md` (family, kind, difficulty, pace, roles, `requires`). `dups.py` and `show.py` score every item against all 22,000 course, exam and bank items by shared numbers and words, then by key; I read the nearest hits and the review, homework and mixed-set pools of the matching courses by hand.

## Mismatches

### Wrong keys

None. Every key, every `wrong` value and every option agrees with my recomputation. Three that I worked twice because the explanation is terse: `duels-weakest-fires-first` (air 0.4615, aim at C 0.3354, aim at B 0.2769; simulated 0.4622, 0.3355, 0.2763), `kelly-twice-the-fraction` (growth at 0.48 is −0.00543) and `when-to-hedge-small-bankroll` (break-even bankroll 24.25).

### Distractor does not fit its option

| Path | Item | Stored | Recomputed | Fix |
|---|---|---|---|---|
| `bank/mental-4.json` | `fraction-compare-middle-of-three` option b (5/7) | why: "You picked the one in the middle of the list" | 5/7 is the first fraction listed and the smallest of the three | "You picked the first one listed. 5/7 is 2/7 short of 1, the largest gap, so it is the smallest." |
| same | same, option c (8/11) | why: "You picked the largest denominator" | 8/11 has the middle denominator (11, against 7 and 18). It is the middle of the list and the largest value | "You picked the middle one listed. 8/11 is 3/11 short of 1, the smallest gap, so it is the largest." |
| `bank/mental-3.json` | `estimate-product-three-factors` option c (340) | why: "rounded every factor up, to 7 × 15 × 3.2 = 336. That is about 8% high" | 340 is 9.4% above 310.79; 336 is 8.1% above | Say "That is about 9% high" or make the option 336. Also option a: 290 is 6.7% low, so "about 7% low" is right |

Key right in all three. The two mental-4 whys are swapped slips (the options are right, the text names the wrong position).

### Wording claim that is wrong

| Path | Item | Stored text | Recomputed |
|---|---|---|---|
| `bank/market-making-3.json` | `intervals-heads-in-100` question "the tightest interval for the number of heads that holds it at least 95% of the time" | key "40 to 60" | Width 19 beats width 20: 40 to 59 and 41 to 60 both hold 95.40%. 40 to 60 holds 96.48%; 41 to 59 holds 94.31% (right as the why says); 45 to 55, 72.87%; 35 to 65, 99.82%. So 40 to 60 is the tightest only among centred intervals |

Fix: "Which of these intervals, centred on 50, is the tightest that holds at least 95%?" and add "centred on 50" to the explanation's first sentence. No option or value changes.

### Answer format and tags

| Path | Item | Problem | Fix |
|---|---|---|---|
| `bank/probability-4.json` | `given-the-total-three-dice` | The question gives no places. Key 0.3333, tol 0.0005, so "1/3" and "0.3333" pass but "0.33" fails (also "33.3%" is 0.333, which passes only just) | Append "Give four decimal places or a fraction." |
| `bank/brainteasers-3.json` | `hats-mod-k-six-prisoners` first tag `hats-mod-k` | In the courses `hats-mod-k` means the line version with k colours (`brainteasers/l7` screens[8], quiz[1], `review-2` items[1]). Every simultaneous modulo plan carries `hats-simultaneous` (`l7` screens[10], quiz[2], `homework-2` item 4). This item is the simultaneous plan, so the deck deals it under the wrong family | Retag `hats-simultaneous` (the brief assigned `hats-mod-k`, so this is a brief error, not an author slip). See the ruling below |

Tag spot check: all 150 items match their brief row on family, kind, difficulty, pace, roles and `requires`, except 3b02 (below). Every choice item has exactly one correct option and `shuffle: true` (39 of 39). Every difficulty 4 and 5 item has `requires`, none below does, every lesson exists in its `course.json`, every `pace` is at most 180 (largest 180), `tags` has one entry each, `source` is "Original" or a plain line. Session counts match the brief: difficulty 10/18/16/6, 9/21/14/6, 6/23/13/8; kinds 28/14/1/7, 29/13/0/8, 28/12/0/10. All 25 longform rubrics are 2, 2, 2, 2, 1, 1. No firm names (the string "sig" in "signal" is the only hit of an unbounded scan). No exclamation marks, em-dashes or en-dashes; no American spellings.

3b02 `weighing-heavy-eight-one-light` carries `weighing-heavy`, not the brief's `weighing-scale`. Accepted: in the courses `weighing-scale` is the digital-scale bag puzzle, and every balance item with one odd coin is `weighing-heavy` (author report, bank-1-3). Note for the brief, not a fix.

### Duplicates

Rule: DECISIONS "Duplicates (6 Nov)": the newer item takes fresh numbers. Every bank item here is newer than every course and exam item, except where noted for 2p06. The session reports compared against the puzzles, brainteasers and mental-pressure lessons only for the items they changed; these nine escaped. Proposed replacements are checked for numbers by grep of `courses`, `exams` and `bank`, and recomputed.

| Item | Duplicates | Kind | Proposed fresh version (recomputed) |
|---|---|---|---|
| `bank/probability-3.json` `waiting-for-hh-three-losing-days` (0.4 loss, three in a row, 24.375) | `courses/markov/l21-waiting-for-patterns.json` screens[10]: same prose, same key | exact | Four losing days in a row at 0.4: key 63.4375 = 2.5 + 6.25 + 15.625 + 39.0625. Wrong values: 24.375 (three days), 39.0625 ($1/0.4^4$), 10 (4 ÷ 0.4). Update the explanation, `accept`, `byKey` and the first-step line ($E_4 = 0$, $E_0 = (1 - 0.4^4)/(0.6 \times 0.4^4)$) |
| `bank/probability-3.json` `random-chords-midpoint-in-disc` (midpoint uniform, longer than the radius, 0.75) | `courses/puzzles/review-5.json` items[8]: same question, same key. The report's claim that the pair "appears nowhere" is wrong | exact | Keep the method, change the threshold to 1.5: chord $2\sqrt{1 - d^2} > 1.5$ when $d^2 < 0.4375$, so key 0.4375 (7/16). Wrong values: 0.4601 (two random endpoints: $1 - 2\arcsin(0.75)/\pi$), 0.6614 (uniform distance, $\sqrt{0.4375}$), 0.5625 (the complement). `puzzles/l29` uses thresholds $\sqrt3$, $\sqrt2$ and 1 only |
| `bank/probability-2.json` `semicircle-seven-points` (7/64) | `courses/puzzles/review-3.json` items[2]: "Seven points fall uniformly on a circle. Chance in one semicircle?" | exact | Nine points: key 9/256 ≈ 0.035. Options: b 1/256 ≈ 0.004, c 9/512 ≈ 0.018, d 1/2 (same slips). Update the explanation's $(1/2)^8$ and the 9 starts. `l14` quiz[0] uses six points, review-3 seven |
| `bank/probability-4.json` `every-coupon-paid-rolls` (die, 14.7 rolls, £2.95) | The die's 14.7 is `puzzles/l2` screens[5], `puzzles/homework-1` `hw1-spoken` and `mock-superday-trader` `a1-coupon-collector`. The price wrapper does not change the stage sums | same set-up and key sub-result | A seven-sector spinner at £1.20 a spin with a £30 prize: $7 H_7 = 363/20 = 18.15$ spins, cost £21.78, profit £8.22. Wrong values: 21.6 (seven spins), −28.8 (49 spins), 9.42 (first spin skipped) |
| `bank/probability-2.json` `fair-from-biased-quarter-coin` (1/4 coin, pairs, 16/3) | `exams/mock-superday-trader.json` `a4-fair-from-biased`: coin 0.25, pairs, stop at the first HT or TH | same numbers | The superday item took 0.25 in fix pass 1eee951 (22:19), before the bank file (23:31), so the bank item is newer. Use a 1/5 coin: pairs kept with chance $2 \times 0.2 \times 0.8 = 0.32$, so 3.125 pairs and 6.25 flips. Wrong values: 3.125 (rounds), 2 (one pair) |
| `bank/mental-3.json` `net-score-eighty-questions` (80 questions, 63 right, 11 wrong, 6 skipped, 52) | `courses/mental-pressure/l13-negative-marking.json` screens[0]: 80 questions, 62 right, 10 wrong, 8 blank, same rule, same key 52 | same set-up and key | 57 right, 15 wrong, 8 skipped: net 42, and accuracy on the 72 answered is 79%. Wrong values: 57 (no penalty), 34 (skips charged). The report cited `l12` and `l13` quiz rows but not this screen |
| `bank/mental-3.json` `sequence-woven-two-doublings` (2, 10, 4, 20, 8, 40, key 16) | `mental-pressure/l10` quiz `q-woven`: 2, 5, 4, 10, 8, 20, key 16. Same first strand and key, second strand rescaled | same set-up and key | 3, 7, 6, 14, 12, 28, next 24. Wrong values: 56 (doubled last), 40 (added last two). Explanation: odd places 3, 6, 12, 24, even places 7, 14, 28 |
| `bank/brainteasers-2.json` `cycle-following-two-hundred-boxes` ("About 31%", options 31%, 0%, 50%, 69%) | `brainteasers/l8-prisoners-and-boxes.json` screens[3]: 100 prisoners, the same four options, the same figures | same question | 100 prisoners each open 70 boxes: success $1 - (H_{100} - H_{70}) = 0.6455$, "about 65%". Distractors: about 0% (the $(1/2)^{100}$ slip), about 70% (each prisoner succeeds with chance 70%), about 35% (the failure chance, $H_{100} - H_{70} = 0.3545$, not taken from 1). Cycles over 70 cannot coexist in 100 boxes, so the formula is exact. `l8` quiz[1] uses 60 |
| `bank/probability-4.json` `given-the-total-three-dice` (three dice total 10, first die 3, key 1/3) | `courses/puzzles/homework-5.json` items[7]: "Three dice total 10. Chance that at least one shows a six?" 0.3333 | same set-up, same key | Total 12, first die 4, other two a 3 and a 5 in either order: 5 ordered pairs make 8, so 2/5 = 0.4 exactly. Wrong values: 0.2 (one order), 0.0556 (2/36, all pairs), 0.08 (2/25, all rolls totalling 12, first die ignored) |

### Known overlap: `2p04` and the session 4 twelve-sided die

`bank/probability-2.json` `when-to-stop-d12-paid-reroll` (one paid reroll at £1, keep the second roll, 181/24 ≈ 7.54) and `bank/probability-4.json` `dice-ev-twelve-sided-three-rolls` (up to three free rolls, 53/6 ≈ 8.83). **Ruling: not a duplicate, no change required.** Both start from the one-roll value 6.5, but the games differ in cost, number of rolls, threshold (keep 6 or more, against 9 or more then 7 or more) and key; no wrong value of one is the key of the other, and they sit in different families (`when-to-stop`, `dice-ev`), so the deck rarely deals them together. If you want the strict reading of "numbers", change 4p03 to a 20-sided die: values 10.5, 13 and 14.4 (keep 14 or more, then 11 or more). Wrong values: 13 (two rolls), 10.5 (one roll), 14.25 (first roll against one fresh roll: $(155 + 10 \times 13)/20$), 15.4875 (best of three). Two other near variants of the same game exist outside this scope: `puzzles/l24` (eight-sided, up to three rolls) and `bank/probability-1` (ten-sided, one reroll).

### Ruling: retag `brainteasers/homework-2` item 4 from `hats-simultaneous` to `hats-mod-k`

**Reject.** What the course items and the bank tags are:

- `hats-mod-k` in `brainteasers`: `l7` screens[8] (twelve people in a line, three colours, calling from the back, 11 guaranteed), `l7` quiz[1] (four in a line, hats 0 to 2, the back person calls the sum mod 3), `review-2` items[1] (ten in a line, three colours). All are the sequential calling game with k colours.
- `hats-simultaneous`: `l7` screens[10] (three players guess or pass at once, 0.75), `l7` quiz[2] (seven people, hats 0 to 6, all at once, "person $i$ assumes the total is $i$ modulo 7", which person is right), and `homework-2` item 4 (five people, hats 0 to 4, all at once, person $i$ assumes the total is $i$ modulo 5). Item 4 is the twin of `l7` quiz[2]; both are correctly `hats-simultaneous`.
- Bank: `hats-mod-k-six-prisoners` (simultaneous, plan "prisoner $k$ aims at total $k$ mod 6") and `hats-simultaneous-fifteen` (simultaneous, the Hamming-code chance).

Retagging the homework item would split it from its own twin and make `hats-mod-k` mean two different games. The author's reason (it "is the modulo strategy `hats-mod-k` names") reads the tag by the arithmetic, but the courses name the family by the game. The consistent fix is the other way round: retag the bank item `hats-mod-k-six-prisoners` to `hats-simultaneous` (see the format table). The item id stays, so schedules are unaffected. After that `hats-mod-k` has no bank item, and `hats-simultaneous` has two (which is how `common-knowledge` already works). This also answers the inbox bullet that asks for a family registry: the registry line for `hats-mod-k` should read "line, k colours, sequential calls".

## Notes

- **Tolerances.** No key band touches a wrong band and no two wrong bands overlap (`tolscan.py`, 85 numeric items). Every item that rejects two-place rounding states its places, except `given-the-total-three-dice` (above). Items where a common form is accepted: fractions on the four-place items (47/12, 16/3, 2/11, 15/29, 12/35, 25/17, 22/13 and so on) and the three-place and two-place forms the question names. `percent-chain-recover-35` accepts 53.5 to 54.5, so 53.8, 54 and 54.4 pass. Percent-unit items (`sqrt-vol`, `percent-chain-three-moves`, `fraction-odds`, `percent-chain-recover-35`) store fractions with `unit: "%"`, as the 6 Nov fix recommended; "70" and "70%" both pass, a bare "0.7" is read as 0.7% and fails, as intended.
- **Expression item.** `dice-ev-square-n-sides` has the two accept forms and the answer; the engine's numeric comparison decides all equivalent forms. Without the CDN script the text fallback accepts only the listed forms, so "(1/6)(n+1)(2n+1)" would fail offline. Optional: add it to `accept`.
- **Choice reading.** All four items where two options look close have one correct option on recomputation: `weighing-heavy-eight-one-light` (c fails: 4 against 4 leaves four suspects), `position-limit-order-of-fills` (b and d breach the limit at 12), `skip-budget-fifty-in-six` (c fails: skipping 15 s as well loses a question) and `when-to-hedge-small-bankroll` (d is reversed).
- **Near variants, not flagged** (same method, different figures): `percent-chain-recover-35` and `mental-pressure/homework-2` (a 40% fall); `word-filled-tank-and-drain` (12 and 20 hours, key 30) and `brainteasers/l12` `q-fill-and-drain` (6 and 9 hours, key 18); `kelly-twice-the-fraction` (0.62, stake 0.48) and `mm-games/review-3` (0.6, stake 0.4); `when-to-stop-three-red-two-black` (3 red, 2 black, 1.5) and `puzzles/homework-1` (2 red, 3 black, 0.2); `common-knowledge-three-marks`, `common-knowledge-marked-badges` and `brainteasers/review-2` (muddy children, six with four); `pairing-knockout-matches` (37 teams) and `brainteasers/l14` (50 players); `sequences-twelfth-term` (1, 3, 7, 15, 31, 63) and `bank/mental-1` `sequences-double-plus-one` (2, 5, 11, 23, 47); `digit-count-ones-to-200` and `mm-games/review-1` (the 7s from 1 to 100); `percent-chain-three-moves` and `topic-3.3` `e-three-moves`; `star-story-incomplete-information` and `bank/behavioural-1` `reasoning-aloud-half-the-information` (same theme, one story and one aloud-reasoning item).
- **Cross-session pairs inside this scope.** `ants-fly-between-trains` (session 4, 120 miles, 40 mph each, fly 90 mph) and `relative-speed-bird-between-trains` (session 3, 90 miles, 30 and 45 mph, bird 60) are the same puzzle in different families; numbers differ, keep both. `dice-ev-twelve-sided-three-rolls` and `when-to-stop-d12-paid-reroll` as ruled above. Nothing else in sessions 2 to 4 overlaps another session.
- **`when-to-stop-three-red-two-black` wrong `tie-zero` (1.1).** Checked: valuing the position with two red and two black left at 0 gives $0.6 \times 1 + 0.4 \times 1.25 = 1.1$, which matches the line. Both stopping rules in `turn-all` (always turn all, or stop at +1) give 1.0.
- **`pirates-five-strict-majority`.** The solver gives 80, 80, 78 and 77 coins for three, four and five aboard (two aboard, the proposer loses). With ties passing A would keep 78, which matches `tie-passes`.
- **`egg-drop-dp-three-eggs`.** 170 floors and the possibility of "none or top" make 171 outcomes; 9 drops settle 130 outcomes and 10 settle 176, so 10 either way (the `wrong` 9 is right to fail). Brute-force dynamic program agrees.
- **`fermi-london-black-cabs`.** The explanation's route gives 18,000 cabs, and the licensed fleet is about 14,000, so "About 10,000" is the right order of magnitude. Option b's why ("one cab trip per person a year") reads 1,000 cabs as 20,000 trips a day, which is below one trip per person per year, so it fits.
- **Voice.** The 13 explanations my crude sentence counter flags (it counts symbols as words) are all at most three sentences, and the author's scan (`voice-scan.py`) found none over 20 words. I did not recount.
- **Not done.** I did not run the playthrough or the deck loop: the authors report both green, and `node tools/validate.mjs` from `app/` gives 0 errors, 392 warnings, none in `content/bank/`, with `manifest.json` unchanged.

## Recomputed keys

All values agree with the stored key; "ok" means key and every wrong value recomputed.

**probability-2.** dice-ev-larger-d6-d4 47/12 = 3.9167; dice-ev-square-n-sides (n+1)(2n+1)/6, 38.5 at n = 10; indicator-tricks-biased-runs 5.62; when-to-stop-d12-paid-reroll 181/24 = 7.5417; when-to-stop-three-red-two-black 1.5; fair-from-biased-quarter-coin 16/3; estimating-n-five-tickets 99.8; given-the-total-a-four-shows 2/11; duels-weaker-shoots-first 15/29; semicircle-seven-points 7/64; exceeding-one-past-three-halves 3.6573 (simulated 3.6576); meeting-forty-minute-window 0.51; who-wins-last-stone-loses go first, take 1; cards-and-colours-reds-before-ace 24/5; urns-polya-three-red-two-blue 12/35.

**probability-3.** dice-ev-middle-of-three 3.5; every-coupon-nine-stickers 7129/280 = 25.4607; at-least-one-signal-sixty-days 0.83919; hats-twelve-coats mean 1, variance 1 (simulated 0.9952, 0.9960); waiting-for-hh-three-losing-days 195/8; bayes-in-a-minute-good-day-signal 33/68; ruin-in-interviews-three-to-nine 0.16236; betting-on-sequences-htt-or-tth 1/4 (simulated 0.2515); kelly-five-to-two 0.09; when-to-hedge-small-bankroll below £24.25; doubling-up-cap-sixteen 0.038020; random-chords-midpoint-in-disc 3/4; expected-distance-squared-gap 1.5; buffon-three-on-five 6/(5π) = 0.38197.

**probability-4.** dice-ev-twelve-sided-three-rolls 53/6; every-coupon-paid-rolls 2.95; indicator-tricks-empty-boxes 1.61134; bayes-in-a-minute-two-flags 0.72090; largest-of-several-first-alarm 6 minutes; ants-fly-between-trains 135; broken-stick-longer-piece 45; estimating-n-tagged-fish 250; duels-weakest-fires-first air (0.4615); who-wins-take-one-two-five 1; given-the-total-three-dice 1/3; kelly-twice-the-fraction −0.00543.

**brainteasers-2.** hourglasses-five-and-eight 4; common-knowledge-three-marks round 3; pigeonhole-pairs-birth-months 3; pigeonhole-worst-case-four-alike 16; cycle-following-two-hundred-boxes 0.3093; last-digit-17-to-2031 3; rule-of-72-tripling 18.85, so 19; average-speed-there-and-back 42; work-rate-two-of-three-pumps 24/7; colouring-chequer-ten-board no.

**brainteasers-3.** hats-mod-k-six-prisoners plan a wins in all 46,656 cases; weighing-heavy-eight-one-light 2; backward-induction-doubling-pot take £3; scheduling-four-jobs-two-machines 8; divisibility-one-to-ten 2,520; powers-of-two-eight-weeds day 21; telescoping-ten-to-ninety-nine 9/100; double-counting-eleven-guests no; relative-speed-bird-between-trains 72; constants-twenty-cubes 44,100.

**brainteasers-4.** weighing-heavy-or-light-twelve 4 against 4; pirates-five-strict-majority 77; egg-drop-dp-three-eggs 10; river-crossing-fox-hen-grain 7; pairing-knockout-matches 36; invariant-product-unit-fractions 9 (three random move orders also end at 9); monovariant-splitting-piles 29; hats-simultaneous-fifteen 15/16; common-knowledge-marked-badges 7; missing-information-no-unit units first.

**mental-2.** 86 × 44 = 3,784; 3,150 ÷ 14 = 225; percent-reverse £120; percent-points 2 points, 50%; fraction-gap 1/28 against 1/45; 31.2 × 19.8 = 617.76; sequence 28; ratio 20.25; daily vol 1.5%; skip-budget 7.2 s, skip the 22 s one.

**mental-3.** 73 × 28 = 2,044; 4,357 ÷ 13 = 335.154, so 335.2; +12.2%; odds of 3 to 7 imply 70%; estimate 310 (exact 310.79); woven 16; Newton 3.3167, so 3.32; crew 15 and 30 days; net 52; ranking A, D, B, C, E.

**mental-4.** 97 × 53 = 5,141; 7,448 ÷ 28 = 266; recover 53.85%, so 54%; middle 13/18; 0.0481 × 2,060 = 99.086; term 12 is 4,095; √2,400 = 48.990, so 49.0; 30 hours; 11/16; battery 114 (36, 45, 720, 684, 114).

**market-making-2.** hearts 25/17; ones 140; cabs about 10,000; skew up; arbitrage £1; larger-minus-three offer 1.6722; call 22/13; judge by edge.

**market-making-3.** heart and club £14.80; divisor twice too high; interval 40 to 60 (see wording); widen (P(12 or fewer) = 0.0321); quote centre 49.04; ledger 26; hedge 15; clarify then quote tight.

**market-making-4.** five face-up 325/47 = 6.9149; product 11.25; informed loss 5 trades (4.5); position limit sell 4 first; delta hedge 1,400; arbitrage buy the set at the offers for £97; edge 17/6 = 2.8333; calibration 75% against 90%, overconfident.

**behavioural-2 to -4.** 25 items, none keyed. Rubrics 2, 2, 2, 2, 1, 1 on all 25; every `prompt` is distinct from the five in `behavioural-1` and from the others; no firm names.

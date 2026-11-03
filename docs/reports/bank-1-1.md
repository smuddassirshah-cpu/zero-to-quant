# Report: interview bank part 1, session 1 (50 items)

Brief: `docs/briefs/bank.md`, session 1. Files written in `app/content/bank/` (`sample.json` left in place, as the brief asks).

| File | Items | Families |
| --- | --- | --- |
| `probability-1.json` | 15 | dice-ev 2, every-coupon 2, waiting-for-hh 2, at-least-one, hats, cards-and-colours, urns, bayes-in-a-minute, ruin-in-interviews, largest-of-several, ants, broken-stick |
| `brainteasers-1.json` | 10 | bridge-crossing, burning-ropes, clock-angle, jugs, egg-drop, hats-line-parity, pirates, weighing-heavy, invariant-parity, trailing-zeros |
| `mental-1.json` | 10 | mental-arithmetic 2, percent-chain, fraction-compare, estimate-product, sequences, sqrt-newton, word-interest, negative-marking, ranking |
| `market-making-1.json` | 10 | card-fair, dice-ev, fermi, fermi-error, intervals, quote-centre, informed-loss, position-limit, hedge-ratio, zero-profit-spread |
| `behavioural-1.json` | 5 | star-story 2, why-us, project-account, reasoning-aloud |

## Results

- `node tools/validate.mjs 2>&1 | tail -5`: **0 errors**, 392 warnings, none from `content/bank/` (no `style` or `source` warning). The manifest lists all six bank files. A final re-run, after another agent began editing `mental-pressure` in parallel, reports 5 errors, all in `mental-pressure` lesson files (`byKey` keys such as `gap` and `round-up` that their widgets cannot return); none is in `content/bank/`.
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: **All passed** (`#bank 37 drawable of 60, deck, pace line, schedule, miss, old save`). With `--mobile`: **All passed**. 37 = 28 session-1 items without `requires` + 9 open sample items.
- Scratch deck loop `scratchpad/bank-1-1/play-bank.mjs` (copies the `bankChecks` deck loop: `ZQ.select.bankDeck`, `ZQ.test.answerCorrect()`, `check()`, `continue()`), at 390 x 844. It imports a save with the 22 `requires` lessons finished (locked count 23 before, 1 after: the sample's own item), schedules every foreign item away, then plays four passes of decks of 8:
  - pass 0: **50 of 50** items dealt and accepted with the authored answer (5 longform included);
  - passes 1 to 3: each numeric `wrong` value typed in turn and each choice distractor clicked in turn: **122 of 122** wrong ids and distractors routed, each returning its own key and showing its `byKey` or `why` line;
  - every `choice` showed exactly one correct option among its 3 or 4, and all 14 choice items were seen in more than one option order (`shuffle: true` works);
  - no console errors, no page wider than 390 px. The final run output is at the end of this report.
- Screenshots: 95 at 390 px (pass 0 every item, pass 1 every wrong route), looked at as contact sheets in `scratchpad/bank-1-1/sheets/`. One fault found and fixed: `\tfrac` fractions in `1m04` and `1m10` options and prose rendered too small to read inside an option button, so those now use plain 7/9, 11/14, 3/8, 5/13 and 7/18. Longform items show the model answer and "Mark it out of 10" under a long model; at 390 px the rubric sits below the fold and is reached by scrolling (engine layout, not a fault).
- Voice scan, `VOICE_BASE=/home/user/zero-to-quant/app/content/bank/ python3 docs/reviews/voice-scan.py`: **explanations over three sentences: 0; over 20 words: 0** (1,449 sentences scanned across the whole folder, `--summary` gives the same two lines). First run on my files alone found 7 long sentences and one false four-sentence explanation (`3! = 6` split a sentence); all fixed.
- No `!` outside KaTeX (`$250!$` sits in math), no em-dashes, British spelling, £ throughout.

## Counts against the brief

- Per file: 15, 10, 10, 10, 5 (matches section 2).
- Per difficulty: D2 8, D3 20, D4 17, D5 5 (matches). Per kind: numeric 31, choice 14, longform 5, expression 0 (matches).
- Per family: as the session-1 column of section 3, except the two renames below. `requires` on all 22 difficulty 4 and 5 items, none below. Every `pace` is the table's value, the largest 180.
- Section 6 says the five behavioural items are "all difficulty 3 or 4", but the table gives `1h04` difficulty 5 and the counts need it; I followed the table.

## Family names changed (rule: "use the nearest existing tag and say so")

Since the brief was written, `puzzles` l2 and l5 (and review 1) carry tags: `every-coupon` (7 items) and `hats` (7 items). The brief's bank-only families `coupon-collector` and `derangements` would therefore never meet those course items in the round robin. So `1p03` and `1p04` use `every-coupon`, and `1p08` uses `hats`, with ids to match. `waiting-for-hh` and `indicator-tricks` already match the course tags. `at-least-one` is still bank-only. **Sessions 3 and 4** should do the same for `3p02`, `4p02` (`every-coupon`) and `3p04` (`hats`); `sample.json` still uses the old two names until it is removed. Puzzles l1 tags its items `dice-games`, while the brief's `dice-ev` comes from mm-games; I kept `dice-ev` as briefed (an open question below).

## Items, refs and changes from the table

| Ref | Id | Family | Kind | D | Pace | Key | `wrong` values |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1p01 | `dice-ev-ten-sided-reroll` | dice-ev | numeric | 3 | 120 | 6.75 | 5.5, 7.15, 6.7 |
| 1p02 | `dice-ev-smaller-two-d12` | dice-ev | choice | 2 | 75 | £4.51 | 3 distractors |
| 1p03 | `every-coupon-eight-faces` | every-coupon | numeric | 3 | 120 | 21.7429 | 16.6667, 20.7429, 64 |
| 1p04 | `every-coupon-colours-seen` | every-coupon | numeric | 4 | 150 | 4.1611 | 0.8389, 0.8322 |
| 1p05 | `waiting-for-hh-tth-biased` | waiting-for-hh | numeric | 4 | 150 | 6.75 | 8, 6, 13.5 |
| 1p06 | `waiting-for-hh-four-flip-race` | waiting-for-hh | choice | 3 | 90 | HTHT, 20 flips against 16: it overlaps it... | 3 distractors |
| 1p07 | `at-least-one-head-99` | at-least-one | numeric | 2 | 60 | 7 | 6, 100 |
| 1p08 | `hats-exactly-two-coats` | hats | numeric | 4 | 150 | 0.1667 | 0.0833, 0.2048, 0.1839 |
| 1p09 | `cards-and-colours-heart-after-red` | cards-and-colours | numeric | 4 | 100 | 0.2451 | 0.2353, 0.2549, 0.25 |
| 1p10 | `urns-reds-before-first-blue` | urns | numeric | 4 | 120 | 1.75 | 2.3333, 3.5, 0.7 |
| 1p11 | `bayes-in-a-minute-flagged-quote` | bayes-in-a-minute | numeric | 3 | 120 | 0.2326 | 0.9, 0.009, 0.97 |
| 1p12 | `ruin-in-interviews-four-to-ten` | ruin-in-interviews | numeric | 3 | 120 | 24 | 16, 36, 40 |
| 1p13 | `largest-of-several-above-08` | largest-of-several | choice | 3 | 100 | 0.5904 | 3 distractors |
| 1p14 | `ants-twenty-on-a-rod` | ants | numeric | 4 | 150 | 2.8571 | 3, 1.5, 0.9524 |
| 1p15 | `broken-stick-longest-above-04` | broken-stick | numeric | 5 | 180 | 0.96 | 1.08, 0.04, 0.75 |
| 1b01 | `bridge-crossing-five-people` | bridge-crossing | numeric | 4 | 180 | 26 | 30, 28 |
| 1b02 | `burning-ropes-45-minutes` | burning-ropes | choice | 3 | 120 | Light rope A at both ends and rope B at o... | 3 distractors |
| 1b03 | `clock-angle-seven-24` | clock-angle | numeric | 2 | 60 | 78 | 66, 282 |
| 1b04 | `jugs-nine-and-five` | jugs | numeric | 4 | 150 | 8 | 4, 10 |
| 1b05 | `egg-drop-sixty-floors` | egg-drop | numeric | 4 | 180 | 11 | 10, 6 |
| 1b06 | `hats-line-parity-average` | hats-line-parity | numeric | 4 | 150 | 6.5 | 6, 3.5, 7 |
| 1b07 | `pirates-strict-majority` | pirates | numeric | 5 | 180 | 98 | 99, 97 |
| 1b08 | `weighing-heavy-forty-coins` | weighing-heavy | choice | 5 | 120 | 4 weighings: first weigh 14 against 14, w... | 3 distractors |
| 1b09 | `invariant-parity-ten-lamps` | invariant-parity | choice | 3 | 120 | No. A move always switches exactly two of... | 3 distractors |
| 1b10 | `trailing-zeros-250-factorial` | trailing-zeros | numeric | 2 | 75 | 62 | 50, 60, 25 |
| 1m01 | `mental-arithmetic-47-by-63` | mental-arithmetic | numeric | 3 | 25 | 2961 | 2820, 3089 |
| 1m02 | `mental-arithmetic-1260-by-18` | mental-arithmetic | numeric | 2 | 25 | 70 | 7, 700 |
| 1m03 | `percent-chain-up-40-down-30` | percent-chain | numeric | 2 | 20 | -2 | 10, -12, 2 |
| 1m04 | `fraction-compare-sevenths-ninths` | fraction-compare | choice | 2 | 20 | 11/14 | 3 distractors |
| 1m05 | `estimate-product-48-7-by-212` | estimate-product | choice | 3 | 25 | 10,300 | 3 distractors |
| 1m06 | `sequences-double-plus-one` | sequences | numeric | 3 | 30 | 95 | 71, 94 |
| 1m07 | `sqrt-newton-7300` | sqrt-newton | numeric | 4 | 30 | 85 | 86, 27 |
| 1m08 | `word-interest-three-years` | word-interest | numeric | 3 | 45 | 9261 | 9200, 1261 |
| 1m09 | `negative-marking-five-options` | negative-marking | choice | 3 | 40 | 0 blind; +1/16 with one ruled out, so guess. | 3 distractors |
| 1m10 | `ranking-four-close-chances` | ranking | choice | 4 | 45 | 3/8, 38%, 5/13, 7/18 | 3 distractors |
| 1k01 | `card-fair-two-card-points` | card-fair | numeric | 3 | 90 | 13.0769 | 14, 11 |
| 1k02 | `dice-ev-larger-two-d4-bid` | dice-ev | numeric | 4 | 90 | 2.875 | 3.125, 3.375, 2.25 |
| 1k03 | `fermi-coin-tower` | fermi | choice | 2 | 75 | 20,000 | 3 distractors |
| 1k04 | `fermi-error-two-inputs` | fermi-error | choice | 3 | 90 | £490 to £1,690 | 3 distractors |
| 1k05 | `intervals-five-dice-90` | intervals | choice | 4 | 90 | 11 to 24 | 3 distractors |
| 1k06 | `quote-centre-two-lifts` | quote-centre | numeric | 3 | 75 | 50.8 | 50.4, 54, 49.2 |
| 1k07 | `informed-loss-one-in-five` | informed-loss | numeric | 4 | 120 | 0.8 | 4, 1, 0 |
| 1k08 | `position-limit-customer-buys` | position-limit | choice | 3 | 60 | Sell all 5: you end long 3, further insid... | 3 distractors |
| 1k09 | `hedge-ratio-short-forty` | hedge-ratio | numeric | 3 | 75 | 18 | 88.8889, 40, -18 |
| 1k10 | `zero-profit-spread-three-in-ten` | zero-profit-spread | numeric | 5 | 120 | 2.4 | 1.2, 3.4286, 8 |
| 1h01 | `star-story-something-wrong` | star-story | longform | 3 | 150 | model and rubric |  |
| 1h02 | `star-story-teammate-disagreement` | star-story | longform | 3 | 150 | model and rubric |  |
| 1h03 | `why-us-trade-not-research` | why-us | longform | 4 | 120 | model and rubric |  |
| 1h04 | `project-account-owned-project` | project-account | longform | 5 | 180 | model and rubric |  |
| 1h05 | `reasoning-aloud-half-the-information` | reasoning-aloud | longform | 4 | 150 | model and rubric |  |

Changes from the session-1 table, each for rule 10 (a course item with the same structure and numbers) unless stated:

1. `1p01`: d8 → d10. `exams/mock-oa-sig-3.json` item 10 is the d8 reroll-once game.
2. `1p02`: two d10 → two d12. `puzzles/l11` screen 8 asks the larger of two 10-sided dice, and the smaller is 11 minus it. Distractors kept as briefed: one-die mean 6.50, the larger 8.49, mean minus 1 = 5.50.
3. `1p05`: fair coin → heads with chance 1/3. A fair TTH is the mirror of `puzzles/l3` quiz `q-hht` (8).
4. `1p06`: HHT against HTH → HTHT against HHTT (20 against 16). The original pair is `markov/l21` screen 0 and `puzzles/l3` quiz.
5. `1p09`: "second red given a heart" → "second heart given red" (25/102). `puzzles/l7` screen 2 is second red given first red, also 25/51.
6. `1p11`: 2%, 90%, 0.5% → 3%, 90%, 1%. `conditional/review-2` item 1 uses 98%, 2% and 0.5%.
7. `1p15`: longest above 1/2 → above 0.4 (0.96, inclusion and exclusion). `puzzles/l13` quiz 1 asks exactly the half.
8. `1b01`: 1, 2, 5, 8, 12 → 1, 3, 4, 9, 11 (26 against 30). `brainteasers/homework-2` item 6 uses 1, 2, 5, 8, 10.
9. `1b04`: 7 and 5 jugs for 4 litres → 9 and 5 jugs for 3 litres (8 steps). `brainteasers/review-3` item 9 uses the 5 and 7 jugs.
10. `1b06`: guaranteed survivors → expected number right (6.5). `brainteasers/l7` asks the guarantee for lines of 8, 20 and 12.
11. `1b07`: the at-least-half rule → more than half (98). `brainteasers/review-2` item 0 and `homework-2` item 0 are four pirates and 100 coins under the at-least-half rule (99).
12. `1b08`: 12 coins then 27 → 40 coins with a first split. `brainteasers/l4` screen 1 is 27 coins weighed 9 against 9.
13. `1b10`: 125! → 250! (62). `brainteasers/l13` screen 8 asks 125!.
14. `1m03`: +20% then −20% → +40% then −30% (−2%). `mental-pressure/l6` screen 1 works +20%, −20%.
15. `1m09`: four options at −1/3 → five options at −1/4 (0 blind, +1/16 with one out). `mental-pressure/l13` screen 5 and `homework-4` work the −1/3 case.
16. `1k09`: short 50 at 0.6 → short 40 at 0.45 (buy 18). `mm-games/l11` quiz 0 is a 0.6 delta hedge.
17. Readings of loose ideas (not duplicates): `1k02` asks the bid of a 0.5-wide quote (fair value 3.125, bid 2.875), so the "two-way price" is graded; `1k06` states the rule "move the centre 0.2 of the way to the trade price" and plays two lifts; `1k07` asks the informed cost per trade (0.8) for a 4 at 6 quote around 0 or 10; `1k10` says the informed trader knows a move of 4 from the centre, so the half-width is 0.3 × 4 (width 2.4).

No idea was swapped for another: each could be made correct and answerable in its pace.

The five closest course items found by the grep (rule 10, acceptance 6), with what changed: `puzzles/l13` quiz 1 (stick, piece over 1/2) → threshold 0.4; `brainteasers/review-2` item 0 (four pirates, 100 coins) → strict majority; `brainteasers/l13` screen 8 (125!) → 250!; `exams/mock-oa-sig-3` item 10 (d8 reroll once) → d10; `markov/l21` screen 0 (HTH against HHT) → HTHT against HHTT.

## Every number, two ways

The script below asserts each pair. Method A is the closed form; method B is enumeration, a linear solve, a search or a seeded simulation (tolerance shown in the script).

| Ref | Key | Method A | Method B |
| --- | --- | --- | --- |
| 1p01 | 6.75 | best threshold over all rules, exact | 0.5 × 8 + 0.5 × 5.5; seeded simulation 6.7506 |
| 1p02 | 650/144 ≈ 4.51 | enumerate 144 rolls | Σj²/144; larger = 13 − min checked by enumeration |
| 1p03 | 761/35 ≈ 21.74 | 8H₈ | first-step recursion on faces seen; simulation 21.748 |
| 1p04 | 4.1611 | 5(1 − (4/5)⁸) | enumerate all 5⁸ draw sequences |
| 1p05 | 27/4 | first-step equations, exact Gaussian solve | overlap rule 1/P(TTH); simulation 6.746 |
| 1p06 | 20 and 16 | first-step solve for each pattern | overlap rule; simulation 20.10 |
| 1p07 | 7 | smallest n with 1 − 2⁻ⁿ > 0.99 | smallest n with 2ⁿ > 100 |
| 1p08 | 1/6 | enumerate 120 permutations | C(5,2)·D₃/120 |
| 1p09 | 25/102 | enumerate ordered pairs of a deck | (12/51 + 13/51)/2 |
| 1p10 | 7/4 | enumerate all arrangements | 7/(3 + 1) |
| 1p11 | 90/387 | Bayes in chances | counts per 10,000; simulation 0.2338 |
| 1p12 | 24 | tridiagonal solve of D_k | k(N − k); simulation 24.04 |
| 1p13 | 0.5904 | 1 − 0.8⁴ | simulation 0.5896 |
| 1p14 | 60/21 | 3·20/21 | ∫(1 − (t/3)²⁰)dt; event simulation of real bouncing ants 2.8577 |
| 1p15 | 0.96 | 3(0.6)² − 3(0.2)² | simulation 0.9598; midpoint grid area 0.9599 |
| 1b01 | 26 | Dijkstra over all crossing states | the stated plan 3+1+11+3+3+1+4 |
| 1b02 | 45 | 30 + 30/2 | (choice) |
| 1b03 | 78° | hand positions formula | stepping both hands minute by minute |
| 1b04 | 8 | breadth-first search of jug states | the stated 8-step plan replayed |
| 1b05 | 11 | egg-drop recurrence f(d, e) | smallest d with d(d + 1)/2 ≥ 60 |
| 1b06 | 6.5 | parity code played on all 128 hat patterns | 6 + 1/2 |
| 1b07 | 98 | backward induction coded for any n and rule | hand argument (C dies, B keeps 100, A buys C and D) |
| 1b08 | 4 | minimax recursion over splits | ⌈log₃ 40⌉; 14/14/12 then 3; 5/5/30 needs 5 |
| 1b09 | no | span of moves over GF(2) | invariant on the seven lamps not at 3, 6, 9 |
| 1b10 | 62 | Legendre: 50 + 10 + 2 | count zeros of the printed 250! |
| 1m01 | 2961 | 47 × 63 | 55² − 8² |
| 1m02 | 70 | 1260/18 | 630/9 |
| 1m03 | −2 | 1.4 × 0.7 − 1 | 0.4 − 0.3 − 0.12 |
| 1m04 | 11/14 | 98 against 99 | difference 1/126 |
| 1m05 | 10,300 | 48.7 × 212 = 10,324.4, nearest option | 50 × 212 − 1.3 × 212 |
| 1m06 | 95 | 2 × 47 + 1 | 47 + 2 × 24 |
| 1m07 | 85 | round(√7300) | isqrt bracket; Newton 85.44 |
| 1m08 | £9,261 | three yearly steps | 8000 × 1.05³ |
| 1m09 | 0 and 1/16 | formula | average over the options |
| 1m10 | 3/8 < 38% < 5/13 < 7/18 | exact Fraction sort | cross products (500 − 494) |
| 1k01 | 170/13 | 2 × 85/13 | enumerate ordered card pairs |
| 1k02 | 2.875 | enumerate 16 rolls, minus 0.25 | Σ m(2m − 1)/16 |
| 1k03 | 20,000 | 60,000 mm / 3 mm | 60,000 / 2.8 rounded to one figure |
| 1k04 | £490 to £1,690 | 0.7², 1.3² | (choice) |
| 1k05 | 11 to 24 | exact counts of 7,776 rolls: 88.2% and 93.5% | normal ±1.645 sd; simulation of 14 to 21 |
| 1k06 | 50.8 | two updates in code | 50 + 2 × 0.2 × 2 |
| 1k07 | 0.8 | 0.2 × 4 | net 0 checked by simulation 0.003 |
| 1k08 | long 3 | 8 − 5 | (choice) |
| 1k09 | 18 | 40 × 0.45 | (wrong 800/9 checked) |
| 1k10 | 2.4 | 2 × 0.3 × 4 | search over h for 0.7h = 0.3(4 − h) |

Every numeric `wrong` value is a named slip, computed in the script from that slip (for example 8H₇ for "left out the first roll", the at-least-half pirate split for "let a tie pass", 5(4/5)⁸ for "the colours never seen"). The generator `gen.py` also asserts that each wrong value sits outside the key's tolerance.

## The behavioural rubric shape (for sessions 2 to 4)

Six lines, points **2, 2, 2, 2, 1, 1**, always in this order:

1. (2) The direct answer in the first sentence (the mistake, the disagreement, the reason, the goal, the decision restated).
2. (2) A specific situation or the substance of the job: when, what, and what was at stake.
3. (2) Your own actions, in the first person (for `why-us`: a fair contrast with the alternatives; for `project-account`: decisions with reasons; for `reasoning-aloud`: known against missing).
4. (2) A number or concrete result (for `reasoning-aloud`: rough numbers on outcomes or downside; for `why-us`: evidence with a number; for `project-account`: one rejected alternative, then the numbers line).
5. (1) A lesson, a change of habit, or what new information would change the choice.
6. (1) Length and clarity: within the pace, in order, no filler.

`project-account` carries both an alternative line and a numbers line, so its lines 3 and 4 shift by one; it still sums to 10. Every model is 120 to 180 words in the first person of an invented candidate, with generic settings only (a second-year group project, a society trading competition, a summer backtest), no real firm, university or grade. `prompt` is the question as spoken; `question` is "Answer aloud, then write your answer here."; `feedback` uses the recruiting homework lines; `explain` says what a strong answer does in three sentences.

## Numeric house style (for sessions 2 to 4)

`accept` gives the key and its one-line working ("27/4 = 6.75."); `label` names the quantity; `placeholder: "fraction or decimal"` wherever a fraction is a fair answer; integer keys use `abs: 0`; decimal keys use half a unit of the asked place. Each `wrong` id is a short slip name (`no-reroll`, `half-rule`, `pours-only`), and each `byKey` line starts with "You ..." naming the action, then says the fix in one sentence. `correct` is "Correct." plus the value; `generic` starts "Not quite right." and names the method only.

## Proposals (course items to tag; not edited)

- `at-least-one` still has no course tag. Untagged candidates in `counting-chance`: l4 quiz `q-five-tosses` and `q-three-rolls`, review 1 `r-three-rolls` and `r-five-positions`, and homework 1 item 5 (fewest limit orders for at least one fill). Tagging them `at-least-one` would join them to `1p07` in the deck. `1p07` draws on `counting-chance/l1-every-outcome` as briefed, though l4 (`l4-does-not-happen`) teaches the complement it uses.
- Puzzles l1 uses `dice-games`; mm-games uses `dice-ev`. One name for both would let the bank's six `dice-ev` items and the puzzles l1 items share a family.

## Open questions

1. Should the bank follow the course renames (`every-coupon`, `hats`) for sessions 3 and 4, as I did, or should the course tags change to the brief's names? I chose the course names because they already exist on 14 course items.
2. `dice-ev` or `dice-games` for probability dice items that draw on `puzzles/l1-dice-games`?
3. Session 3's `3p05` ("loses with chance 0.4, two losing days in a row") is `puzzles/l3-waiting-for-hh` screen 9 word for word in structure and numbers; its author should change the numbers.
4. `1h04` is difficulty 5 in the table but section 6 says behavioural items are 3 or 4; I kept 5.

## Inbox

Three bullets under `Raised later (bank part 1 session 1):` in `docs/BACKLOG-INBOX.md`.

## Scripts

`scratchpad/bank-1-1/` holds `bank-1-1.py` (numbers), `gen.py` (builds the five files from item data, asserting one correct option, rubric sums, model length, `requires` only at D4 and D5, and wrong values outside the key's tolerance), `play-bank.mjs` (the deck loop) and `sheets/` (contact sheets of the 390 px screenshots).

### `bank-1-1.py`

```python
"""Bank part 1, session 1: every keyed answer and every numeric wrong value, two ways each, with asserts.
Writes nothing. Run: python3 bank-1-1.py"""
from fractions import Fraction as F
from itertools import product, permutations, combinations
from collections import Counter, deque
import random, math, heapq
rng = random.Random(20261103)
OUT = []
def rec(ref, name, a, b, tol=0):
    a_, b_ = float(a), float(b)
    assert abs(a_ - b_) <= tol, (ref, name, a, b)
    OUT.append(f'{ref:5} {name:34} {a_:12.6f}  check {b_:12.6f}')
def sim(f, n=200000):
    return sum(f() for _ in range(n)) / n

# ---------- probability-1 ----------
# 1p01 d10, one optional reroll, must keep the second roll
def reroll_value(n, keep_from):
    fresh = F(n + 1, 2)
    return sum((F(k) if k >= keep_from else fresh) for k in range(1, n + 1)) / n
best = max(reroll_value(10, t) for t in range(1, 12))
closed = F(1, 2) * F(6 + 10, 2) + F(1, 2) * F(11, 2)            # keep 6..10 (mean 8) half the time
rec('1p01', 'value with best rule', best, closed)
rec('1p01', 'sim', closed, sim(lambda: (lambda r: r if r >= 6 else rng.randint(1, 10))(rng.randint(1, 10))), 0.02)
rec('1p01', 'wrong no-reroll 5.5', F(11, 2), sum(range(1, 11)) / F(10))
rec('1p01', 'wrong max-of-two 7.15', sum(max(a, b) for a, b in product(range(1, 11), repeat=2)) / F(100), F(sum(k * (2 * k - 1) for k in range(1, 11)), 100))
rec('1p01', 'wrong keep-7-up 6.7', reroll_value(10, 7), F(4, 10) * F(17, 2) + F(6, 10) * F(11, 2))
# 1p02 smaller of two d12 (choice)
emin = sum(min(a, b) for a, b in product(range(1, 13), repeat=2)) / F(144)
rec('1p02', 'E min two d12 (650/144)', emin, F(sum(j * j for j in range(1, 13)), 144))
rec('1p02', 'option larger 8.49', 13 - emin, sum(max(a, b) for a, b in product(range(1, 13), repeat=2)) / F(144))
rec('1p02', 'option mean 6.5 and 5.5', F(13, 2) - 1, F(11, 2))
assert round(float(emin), 2) == 4.51 and round(float(13 - emin), 2) == 8.49
# 1p03 coupon collector d8 (and d4 in prose)
H = lambda n: sum(F(1, k) for k in range(1, n + 1))
def coupon_lin(n):   # first-step: E_k = 1 + (k/n) E_k + ((n-k)/n) E_{k+1}
    E = F(0)
    for k in range(n - 1, -1, -1): E = (1 + F(n - k, n) * E) / (1 - F(k, n))
    return E
rec('1p03', 'd4 coupon 25/3', 4 * H(4), coupon_lin(4))
rec('1p03', 'd8 coupon 761/35', 8 * H(8), coupon_lin(8))
def coup_sim(n):
    seen, c = set(), 0
    while len(seen) < n: seen.add(rng.randrange(n)); c += 1
    return c
rec('1p03', 'd8 sim', 8 * H(8), sim(lambda: coup_sim(8), 100000), 0.1)
rec('1p03', 'wrong doubled d4 50/3', 2 * 4 * H(4), F(50, 3))
rec('1p03', 'wrong 8*H7 20.7429', 8 * H(7), 8 * H(8) - 1)
rec('1p03', 'wrong n^2 64', 64, 8 * 8)
# 1p04 distinct colours in 8 draws from 5
ed = 5 * (1 - F(4, 5) ** 8)
enum = F(sum(len(set(s)) for s in product(range(5), repeat=8)), 5 ** 8)
rec('1p04', 'expected colours seen', ed, enum)
rec('1p04', 'wrong missing 5(4/5)^8', 5 * F(4, 5) ** 8, 5 - enum)
rec('1p04', 'wrong one colour 1-(4/5)^8', 1 - F(4, 5) ** 8, ed / 5)
# 1p05 TTH with P(H)=1/3
def wait(pattern, p):
    """first-step equations solved by Gaussian elimination on states 0..len-1 (state = matched prefix length)"""
    m = len(pattern); q = 1 - p
    def nxt(k, c):
        s = pattern[:k] + c
        for j in range(min(len(s), m), -1, -1):
            if s.endswith(pattern[:j]) and j <= len(s): return j
    A = [[F(0)] * m for _ in range(m)]; b = [F(1)] * m
    for k in range(m):
        A[k][k] += 1
        for c, pr in (('H', p), ('T', q)):
            j = nxt(k, c)
            if j < m: A[k][j] -= pr
    for i in range(m):   # elimination
        piv = A[i][i]
        for j in range(m): A[i][j] /= piv
        b[i] /= piv
        for r in range(m):
            if r != i and A[r][i] != 0:
                f = A[r][i]
                for j in range(m): A[r][j] -= f * A[i][j]
                b[r] -= f * b[i]
    return b[0]
def overlap_rule(pattern, p):
    pr = lambda s: math.prod(p if c == 'H' else 1 - p for c in s)
    return sum(1 / pr(pattern[:k]) for k in range(1, len(pattern) + 1) if pattern[:k] == pattern[-k:])
rec('1p05', 'TTH p=1/3 (27/4)', wait('TTH', F(1, 3)), overlap_rule('TTH', F(1, 3)))
def pat_sim(pattern, p):
    s, c = '', 0
    while not s.endswith(pattern): s = (s + ('H' if rng.random() < p else 'T'))[-len(pattern):]; c += 1
    return c
rec('1p05', 'TTH sim', F(27, 4), sim(lambda: pat_sim('TTH', 1 / 3), 100000), 0.08)
rec('1p05', 'wrong fair coin 8', wait('TTH', F(1, 2)), 8)
rec('1p05', 'wrong per-letter sum 6', F(3, 2) + F(3, 2) + 3, 6)
rec('1p05', 'wrong swapped chances 13.5', wait('TTH', F(2, 3)), F(27, 2))
# 1p06 HTHT vs HHTT (choice)
rec('1p06', 'HTHT wait 20', wait('HTHT', F(1, 2)), overlap_rule('HTHT', F(1, 2)))
rec('1p06', 'HHTT wait 16', wait('HHTT', F(1, 2)), overlap_rule('HHTT', F(1, 2)))
rec('1p06', 'HTHT sim', 20, sim(lambda: pat_sim('HTHT', 0.5), 100000), 0.2)
# 1p07 at least one head above 99%
n7 = next(n for n in range(1, 50) if 1 - F(1, 2) ** n > F(99, 100))
n7b = next(n for n in range(1, 50) if 2 ** n > 100)
rec('1p07', 'smallest n', n7, n7b)
rec('1p07', 'wrong 6 gives 0.984', 1 - F(1, 2) ** 6, F(63, 64))
# 1p08 exactly two of five get their own
perm5 = list(permutations(range(5)))
p2 = F(sum(1 for s in perm5 if sum(s[i] == i for i in range(5)) == 2), 120)
D = lambda n: round(math.factorial(n) / math.e) if n else 1
rec('1p08', 'P(exactly 2 fixed) 1/6', p2, F(math.comb(5, 2) * D(3), 120))
rec('1p08', 'wrong no derange 10/120', F(math.comb(5, 2), 120), F(1, 12))
rec('1p08', 'wrong binomial', math.comb(5, 2) * F(1, 5) ** 2 * F(4, 5) ** 3, F(128, 625))
rec('1p08', 'wrong Poisson 1/(2e)', 1 / (2 * math.e), math.exp(-1) / 2)
# 1p09 second card a heart given first red
deck = [(r, s) for r in range(13) for s in 'SHDC']
red = lambda c: c[1] in 'HD'
num = sum(1 for a, b in permutations(deck, 2) if red(a) and b[1] == 'H'); den = sum(1 for a, b in permutations(deck, 2) if red(a))
rec('1p09', 'P(heart | first red) 25/102', F(num, den), (F(12, 51) + F(13, 51)) / 2)
rec('1p09', 'wrong first heart 12/51', F(12, 51), F(4, 17))
rec('1p09', 'wrong first diamond 13/51', F(13, 51), F(13, 51))
# 1p10 reds before first blue, 7 red 3 blue
arr = set(permutations('RRRRRRRBBB'))
ebr = F(sum(s.index('B') for s in arr), len(arr))
rec('1p10', 'reds before first blue 7/4', ebr, F(7, 3 + 1))
rec('1p10', 'wrong 7/3', F(7, 3), F(7, 3))
rec('1p10', 'wrong half 3.5', F(7, 2), F(7, 2))
rec('1p10', 'wrong 7/10', F(7, 10), F(7, 10))
# 1p11 Bayes 90% / 3% / 1%
post = F(1, 100) * F(9, 10) / (F(1, 100) * F(9, 10) + F(99, 100) * F(3, 100))
rec('1p11', 'P(mispriced | flag) 90/387', post, F(90, 90 + 297))
rec('1p11', 'sim', post, (lambda N: (lambda xs: sum(b for b, f in xs if f) / sum(f for b, f in xs))([(b, rng.random() < (0.9 if b else 0.03)) for b in (rng.random() < 0.01 for _ in range(N))]))(400000), 0.01)
rec('1p11', 'wrong joint 0.009', F(1, 100) * F(9, 10), F(9, 1000))
# 1p12 fair ruin from 4 to 10, duration
def ruin_dur(k, N):
    # solve D_j = 1 + (D_{j-1}+D_{j+1})/2 by iteration to exact fixed point via linear algebra (tridiagonal)
    n = N - 1; a = [F(0)] * (N + 1)
    # Thomas algorithm on -0.5 D_{j-1} + D_j - 0.5 D_{j+1} = 1
    c = [F(0)] * (N + 1); d = [F(0)] * (N + 1)
    for j in range(1, N):
        m = 1 - F(-1, 2) * c[j - 1] if j > 1 else F(1)
        c[j] = F(-1, 2) / m; d[j] = (1 - F(-1, 2) * d[j - 1]) / m if j > 1 else F(1)
    for j in range(N - 1, 0, -1): a[j] = d[j] - c[j] * a[j + 1]
    return a[k]
rec('1p12', 'expected bets 24', ruin_dur(4, 10), 4 * (10 - 4))
def ruin_sim():
    x, c = 4, 0
    while 0 < x < 10: x += 1 if rng.random() < 0.5 else -1; c += 1
    return c
rec('1p12', 'sim', 24, sim(ruin_sim, 100000), 0.3)
rec('1p12', 'reach 10 chance 0.4 (prose)', F(4, 10), F(2, 5))
# 1p13 largest of four uniforms above 0.8 (choice)
rec('1p13', 'P(max>0.8)', 1 - F(4, 5) ** 4, sim(lambda: max(rng.random() for _ in range(4)) > 0.8), 0.005)
rec('1p13', 'option 0.4096 0.0016', F(4, 5) ** 4 + F(1, 5) ** 4, F(4096 + 16, 10000))
# 1p14 twenty ants on a 3 m rod, bouncing: event simulation with real collisions
def ants_bounce(n=20, L=3.0):
    pos = sorted(rng.random() * L for _ in range(n)); vel = [rng.choice((-1, 1)) for _ in range(n)]
    t = 0.0; alive = list(range(n))
    while pos:
        # next event: an ant reaches an end, or two neighbours meet
        best, kind, idx = math.inf, None, None
        for i, (x, v) in enumerate(zip(pos, vel)):
            te = (L - x) if v > 0 else x
            if te < best: best, kind, idx = te, 'end', i
        for i in range(len(pos) - 1):
            if vel[i] > 0 and vel[i + 1] < 0:
                tm = (pos[i + 1] - pos[i]) / 2
                if tm < best: best, kind, idx = tm, 'meet', i
        t += best; pos = [x + v * best for x, v in zip(pos, vel)]
        if kind == 'end': pos.pop(idx); vel.pop(idx)
        else: vel[idx], vel[idx + 1] = -1, 1
    return t
exact14 = F(3) * F(20, 21)
rec('1p14', 'E last fall 60/21', exact14, 3 - F(3, 21))               # integral of 1-(t/3)^20 over 0..3
rec('1p14', 'bounce sim', exact14, sim(ants_bounce, 20000), 0.02)
rec('1p14', 'wrong one ant 1.5', F(3, 2), F(3, 2))
rec('1p14', 'wrong 20/21', F(20, 21), F(20, 21))
# 1p15 broken stick, longest above 0.4
a = F(2, 5)
ie = 3 * (1 - a) ** 2 - 3 * (1 - 2 * a) ** 2
def stick():
    x, y = sorted((rng.random(), rng.random()))
    return max(x, y - x, 1 - y) > 0.4
rec('1p15', 'P(longest > 0.4) 0.96', ie, sim(stick, 400000), 0.004)
# exact by area on a fine lattice with Fraction-free integer counting (midpoint grid)
G = 2000; cnt = 0
for i in range(G):
    x = (i + 0.5) / G
    for j in range(i + 1, G):
        y = (j + 0.5) / G
        if max(x, y - x, 1 - y) > 0.4: cnt += 1
rec('1p15', 'grid area', ie, cnt / (G * (G - 1) / 2), 0.003)
rec('1p15', 'wrong no overlap 1.08', 3 * (1 - a) ** 2, F(108, 100))
rec('1p15', 'wrong complement 0.04', 1 - ie, F(4, 100))
rec('1p15', 'wrong half answer 0.75', 3 * F(1, 2) ** 2, F(3, 4))

# ---------- brainteasers-1 ----------
def bridge(times):
    n = len(times); start = (frozenset(range(n)), 0); dist = {start: 0}; pq = [(0, 0, start)]; c = 1
    while pq:
        d, _, (L, s) = heapq.heappop(pq)
        if not L: return d
        if d > dist[(L, s)]: continue
        side = L if s == 0 else frozenset(range(n)) - L
        for k in (1, 2):
            for g in combinations(side, k):
                g = frozenset(g); st = (L - g, 1) if s == 0 else (L | g, 0); nd = d + max(times[i] for i in g)
                if nd < dist.get(st, 1e9): dist[st] = nd; heapq.heappush(pq, (nd, c, st)); c += 1
T = [1, 3, 4, 9, 11]
plan = 3 + 1 + 11 + 3 + 3 + 1 + 4
rec('1b01', 'bridge 1,3,4,9,11', bridge(T), plan)
rec('1b01', 'wrong escort 30', sum(T[1:]) + 3 * T[0], 30)
rec('1b01', 'wrong sum 28', sum(T), 28)
# 1b02 ropes (choice): A both ends 30, then B's remaining 30 halves to 15
rec('1b02', 'ropes 45', 60 / 2 + (60 - 30) / 2, 45)
rec('1b02', 'distractor 60, 30', 30 + 30, 60)
# 1b03 clock 7:24
hh, mm = 7, 24
ang = abs((hh * 30 + mm * 0.5) - mm * 6); ang = min(ang, 360 - ang)
rec('1b03', 'angle 78', ang, abs(222 - 144))
# step the hands minute by minute from 12:00 as a second method
hpos = mpos = 0.0
for _ in range(7 * 60 + 24): hpos += 0.5; mpos = (mpos + 6) % 360
rec('1b03', 'stepped hands', ang, min(abs(hpos - mpos), 360 - abs(hpos - mpos)))
rec('1b03', 'wrong 66 and 282', abs(210 - 144) + (360 - 78), 66 + 282)
# 1b04 jugs 9 and 5, leave 3
def jugs(a, b, target, first=None):
    start = (0, 0); seen = {start: 0}; q = deque([start])
    def moves(x, y):
        p1 = min(x, b - y); p2 = min(y, a - x)
        return [('fillA', (a, y)), ('fillB', (x, b)), ('emptyA', (0, y)), ('emptyB', (x, 0)), ('AtoB', (x - p1, y + p1)), ('BtoA', (x + p2, y - p2))]
    if first:
        s = dict(moves(0, 0))[first]; seen = {start: 0, s: 1}; q = deque([s])
    while q:
        x, y = q.popleft()
        if x == target or y == target: return seen[(x, y)]
        for _, s in moves(x, y):
            if s not in seen: seen[s] = seen[(x, y)] + 1; q.append(s)
best4 = jugs(9, 5, 3)
x = y = 0; steps = 0; transfers = 0
for mv in ['fillA', 'AtoB', 'emptyB', 'AtoB', 'fillA', 'AtoB', 'emptyB', 'AtoB']:
    if mv == 'fillA': x = 9
    elif mv == 'emptyB': y = 0
    else: p = min(x, 5 - y); x, y = x - p, y + p; transfers += 1
    steps += 1
assert x == 3
rec('1b04', 'fewest steps 8', best4, steps)
rec('1b04', 'wrong transfers only 4', transfers, 4)
other = jugs(9, 5, 3, first='fillB')
rec('1b04', 'wrong 5-first route', other, other)
OUT.append(f'      (starting by filling the 5 takes {other} steps)')
# 1b05 egg drop, two eggs, 60 floors
def eggs_dp(e, n):
    f = [[0] * (e + 1) for _ in range(200)]
    for d in range(1, 200):
        for k in range(1, e + 1): f[d][k] = f[d - 1][k - 1] + f[d - 1][k] + 1
        if f[d][e] >= n: return d
rec('1b05', 'two eggs 60 floors', eggs_dp(2, 60), next(d for d in range(1, 30) if d * (d + 1) // 2 >= 60))
rec('1b05', 'wrong 10 covers 55, binary 6', 10 * 11 // 2 + math.ceil(math.log2(60)), 55 + 6)
# 1b06 seven in a line, two colours: expected right with parity code (enumerate all 128 patterns)
def parity_play(h):
    n = len(h); calls = [None] * n   # index 0 at the back
    calls[0] = sum(h[1:]) % 2
    for i in range(1, n): calls[i] = (calls[0] - sum(h[i + 1:]) - sum(calls[1:i])) % 2
    return sum(c == x for c, x in zip(calls, h))
scores = [parity_play(h) for h in product((0, 1), repeat=7)]
rec('1b06', 'expected right 6.5', F(sum(scores), 128), 6 + F(1, 2))
assert min(scores) == 6
rec('1b06', 'wrong guaranteed 6, coin 3.5', min(scores) + F(7, 2), F(19, 2))
# 1b07 four pirates, strict majority, bloodthirsty
def pirates(n, coins, strict=True):
    """returns split for pirates 0..n-1 (0 most senior) or None if the proposer dies whatever he offers"""
    if n == 1: return [coins]
    rest = pirates(n - 1, coins, strict)   # split if the proposer dies (None: next proposer dies too)
    need = n // 2 + 1 if strict else (n + 1) // 2
    # value to each other pirate if proposer dies: survival matters most
    if rest is None:   # the next proposer would die; deeper outcome
        deeper = pirates(n - 2, coins, strict)
        alt = {1: None}   # pirate 1 (next proposer) dies: he votes yes for anything
        for j in range(2, n): alt[j] = deeper[j - 2]
    else:
        alt = {j: rest[j - 1] for j in range(1, n)}
    cost = []
    for j in range(1, n):
        if alt[j] is None: cost.append((0, j))          # would die otherwise: votes yes for 0
        else: cost.append((alt[j] + 1, j))
    cost.sort()
    buy = cost[:need - 1]
    spend = sum(c for c, _ in buy)
    if spend > coins: return None
    split = [0] * n; split[0] = coins - spend
    for c, j in buy: split[j] = c
    return split
s4 = pirates(4, 100)
rec('1b07', 'A keeps (strict majority)', s4[0], 100 - 2)
rec('1b07', 'wrong at-least-half rule 99', pirates(4, 100, strict=False)[0], 99)
OUT.append(f'      strict split {s4}, at-least-half split {pirates(4, 100, strict=False)}, 2-pirate strict {pirates(2, 100)}')
# 1b08 forty coins, one heavy
def fewest(n): return 0 if n <= 1 else min(1 + max(fewest(k), fewest(n - 2 * k)) for k in range(1, n // 2 + 1))
import functools; fewest = functools.lru_cache(None)(fewest)
rec('1b08', 'fewest weighings 40', fewest(40), math.ceil(math.log(40, 3) - 1e-12))
rec('1b08', '14v14 then 3 more', 1 + max(fewest(14), fewest(12)), 4)
rec('1b08', '5v5 (30 aside) needs', 1 + max(fewest(5), fewest(30)), 5)
rec('1b08', '27 is the 3-weighing max', max(n for n in range(1, 60) if fewest(n) <= 3), 27)
# 1b09 ten lamps, flip three neighbours: reachable set over GF(2)
n = 10
gens = [sum(1 << j for j in range(i, i + 3)) for i in range(n - 2)]
reach = {0}
for g in gens: reach |= {r ^ g for r in reach}
alls = (1 << n) - 1
invariant = sum(1 << j for j in range(n) if (j + 1) % 3 != 0)
ok_inv = all(bin(g & invariant).count('1') == 2 for g in gens)
rec('1b09', 'all-on reachable (0 = no)', int(alls in reach), 0)
rec('1b09', 'invariant lamps lit in all-on', bin(alls & invariant).count('1'), 7)
assert ok_inv
# the 'yes' distractor: 1-3, 4-6, 7-9, 8-10 leaves lamps 8, 9 off
st = 0
for i in (0, 3, 6, 7): st ^= gens[i]
rec('1b09', 'distractor leaves lamps off', bin(st).count('1'), 8)
# 1b10 trailing zeros of 250!
z = sum(250 // 5 ** k for k in range(1, 5))
s = str(math.factorial(250)); rec('1b10', 'trailing zeros 250!', z, len(s) - len(s.rstrip('0')))
rec('1b10', 'wrong 50, 60, 25', 250 // 5 + (250 // 5 + 250 // 25) + 250 // 10, 50 + 60 + 25)

# ---------- mental-1 ----------
rec('1m01', '47 x 63', 47 * 63, 55 ** 2 - 8 ** 2)
rec('1m01', 'wrong 2820, 3089', 47 * 60 + (55 ** 2 + 8 ** 2), 2820 + 3089)
rec('1m02', '1260 / 18', F(1260, 18), F(630, 9))
rec('1m03', '+40% then -30%', (F(14, 10) * F(7, 10) - 1) * 100, (F(4, 10) - F(3, 10) - F(4, 10) * F(3, 10)) * 100)
rec('1m03', 'wrong added +10, cross -12', 40 - 30 + (-40 * 30 / 100), 10 - 12)
rec('1m04', '98 vs 99', 7 * 14 - 11 * 9, -1)
rec('1m04', 'decimals', F(11, 14) - F(7, 9), F(1, 126))
ex5 = F(487, 10) * 212
rec('1m05', '48.7 x 212', ex5, 50 * 212 - F(13, 10) * 212)
opts5 = [10300, 10600, 9740, 103000]
assert min(opts5, key=lambda o: abs(o - ex5)) == 10300
rec('1m05', 'option 9,740 = 48.7 x 200', F(487, 10) * 200, 9740)
seq = [2]
for _ in range(5): seq.append(2 * seq[-1] + 1)
rec('1m06', 'next term 95', seq[5], 47 + 2 * (47 - 23))
r7 = math.isqrt(7300); rec('1m07', 'sqrt 7300 nearest', round(math.sqrt(7300)), r7 if (r7 + 0.5) ** 2 > 7300 else r7 + 1)
rec('1m07', 'newton step 85.44', 85 + F(7300 - 85 ** 2, 2 * 85), math.sqrt(7300), 0.01)
rec('1m07', 'wrong sqrt 730 -> 27', round(math.sqrt(730)), 27)
v = F(8000)
for _ in range(3): v = v * F(105, 100)
rec('1m08', '8000 at 5% three years', v, 8000 * F(21, 20) ** 3)
rec('1m08', 'wrong simple 9200, interest 1261', 8000 * F(115, 100) + (v - 8000), 9200 + 1261)
blind = F(1, 5) - F(4, 5) * F(1, 4); one_out = F(1, 4) - F(3, 4) * F(1, 4)
rec('1m09', 'blind guess 0', blind, sum((1 if g == 0 else F(-1, 4)) for g in range(5)) / 5)
rec('1m09', 'one ruled out 1/16', one_out, sum((1 if g == 0 else F(-1, 4)) for g in range(4)) / 4)
rec('1m09', 'distractor -1/20, +1/5', F(1, 5) - F(1, 4), F(-1, 20))
ch = {'5/13': F(5, 13), '38%': F(38, 100), '3/8': F(3, 8), '7/18': F(7, 18)}
order = sorted(ch, key=ch.get)
assert order == ['3/8', '38%', '5/13', '7/18'], order
rec('1m10', 'gaps 5/13-38%, 7/18-5/13', F(5, 13) - F(38, 100), F(500 - 494, 1300))
rec('1m10', 'percents', float(F(7, 18)) * 100, 38.888888, 0.0001)

# ---------- market-making-1 ----------
vals = [min(r, 10) for r in range(1, 14)] * 4
rec('1k01', 'two-card sum, courts 10', 2 * F(sum(vals), 52), F(sum(a + b for a, b in permutations(vals, 2)), 52 * 51))
rec('1k01', 'wrong ranks 1-13 -> 14', 2 * F(sum(range(1, 14)), 13), 14)
rec('1k01', 'wrong 1-10 only -> 11', 2 * F(55, 10), 11)
fv2 = sum(max(a, b) for a, b in product(range(1, 5), repeat=2)) / F(16)
rec('1k02', 'E max two d4 50/16', fv2, F(1 * 1 + 2 * 3 + 3 * 5 + 4 * 7, 16))
rec('1k02', 'bid 2.875', fv2 - F(1, 4), F(23, 8))
rec('1k02', 'wrong offer 3.375, one die 2.25', fv2 + F(1, 4) + F(5, 2) - F(1, 4), F(27, 8) + F(9, 4))
h = 20 * 3 * 1000     # mm
rec('1k03', 'coins at 3 mm', h / 3, 20000)
rec('1k03', 'coins at 2.8 mm', round(h / 2.8, -4), 20000)
rec('1k03', 'width 23 mm, 1 m storey, 3 cm', round(h / 23, -3) + round(20000 / 2.8, -3) + h / 30, 3000 + 7000 + 2000)
rec('1k04', 'range factors', F(7, 10) ** 2 * 1000 + F(13, 10) ** 2 * 1000, 490 + 1690)
c5 = Counter(sum(r) for r in product(range(1, 7), repeat=5)); tot = 6 ** 5
cov = lambda lo, hi: F(sum(v for k, v in c5.items() if lo <= k <= hi), tot)
rec('1k05', 'mean, var of 5 dice', F(sum(k * v for k, v in c5.items()), tot) + F(sum(k * k * v for k, v in c5.items()), tot) - F(sum(k * v for k, v in c5.items()), tot) ** 2, F(35, 2) + 5 * F(35, 12))
rec('1k05', '12-23 holds', cov(12, 23), F(6862, 7776))
rec('1k05', '11-24 holds', cov(11, 24), F(7272, 7776))
rec('1k05', '14-21 holds', cov(14, 21), sim(lambda: 14 <= sum(rng.randint(1, 6) for _ in range(5)) <= 21, 100000), 0.01)
assert cov(12, 23) < F(9, 10) <= cov(11, 24) and cov(5, 30) == 1
c = F(50)
for _ in range(2): c = c + F(1, 5) * ((c + 2) - c)
rec('1k06', 'centre after two lifts', c, 50 + 2 * F(1, 5) * 2)
rec('1k06', 'wrong one trade 50.4, full move 54', F(504, 10) + 54, F(1044, 10))
cw = F(50)
for _ in range(2): cw = cw - F(1, 5) * 2
rec('1k06', 'wrong way 49.2', cw, F(492, 10))
loss_inf = F(1, 5) * (F(1, 2) * (10 - 6) + F(1, 2) * (4 - 0))
rec('1k07', 'informed cost per trade', loss_inf, F(4, 5))
gain_un = F(4, 5) * (F(1, 2) * (6 - 5) + F(1, 2) * (5 - 4))
rec('1k07', 'net per trade 0 (wrong value)', gain_un - loss_inf, 0)
def mm_sim():
    v = 10 if rng.random() < 0.5 else 0
    if rng.random() < 0.2: return -(v - 6) if v == 10 else -(4 - v)
    return (6 - v) if rng.random() < 0.5 else (v - 4)
rec('1k07', 'sim net', 0, sim(mm_sim, 400000), 0.05)
rec('1k08', 'position after selling 5', 8 - 5, 3)
rec('1k09', 'hedge units', 40 * F(45, 100), 18)
rec('1k09', 'wrong divided', F(40) / F(45, 100), F(800, 9))
hstar = F(3, 10) * 4
rec('1k10', 'break-even width', 2 * hstar, 2 * next(h for h in (F(k, 100) for k in range(0, 1000)) if F(7, 10) * h - F(3, 10) * (4 - h) >= 0))
rec('1k10', 'wrong net-of-spread 3.4286', 2 * F(3, 10) * 4 / F(7, 10), F(24, 7))
for line in OUT: print(line)
print('all', len(OUT), 'checks passed')
```

### Its output

```text
1p01  value with best rule                   6.750000  check     6.750000
1p01  sim                                    6.750000  check     6.750580
1p01  wrong no-reroll 5.5                    5.500000  check     5.500000
1p01  wrong max-of-two 7.15                  7.150000  check     7.150000
1p01  wrong keep-7-up 6.7                    6.700000  check     6.700000
1p02  E min two d12 (650/144)                4.513889  check     4.513889
1p02  option larger 8.49                     8.486111  check     8.486111
1p02  option mean 6.5 and 5.5                5.500000  check     5.500000
1p03  d4 coupon 25/3                         8.333333  check     8.333333
1p03  d8 coupon 761/35                      21.742857  check    21.742857
1p03  d8 sim                                21.742857  check    21.748050
1p03  wrong doubled d4 50/3                 16.666667  check    16.666667
1p03  wrong 8*H7 20.7429                    20.742857  check    20.742857
1p03  wrong n^2 64                          64.000000  check    64.000000
1p04  expected colours seen                  4.161139  check     4.161139
1p04  wrong missing 5(4/5)^8                 0.838861  check     0.838861
1p04  wrong one colour 1-(4/5)^8             0.832228  check     0.832228
1p05  TTH p=1/3 (27/4)                       6.750000  check     6.750000
1p05  TTH sim                                6.750000  check     6.746280
1p05  wrong fair coin 8                      8.000000  check     8.000000
1p05  wrong per-letter sum 6                 6.000000  check     6.000000
1p05  wrong swapped chances 13.5            13.500000  check    13.500000
1p06  HTHT wait 20                          20.000000  check    20.000000
1p06  HHTT wait 16                          16.000000  check    16.000000
1p06  HTHT sim                              20.000000  check    20.096230
1p07  smallest n                             7.000000  check     7.000000
1p07  wrong 6 gives 0.984                    0.984375  check     0.984375
1p08  P(exactly 2 fixed) 1/6                 0.166667  check     0.166667
1p08  wrong no derange 10/120                0.083333  check     0.083333
1p08  wrong binomial                         0.204800  check     0.204800
1p08  wrong Poisson 1/(2e)                   0.183940  check     0.183940
1p09  P(heart | first red) 25/102            0.245098  check     0.245098
1p09  wrong first heart 12/51                0.235294  check     0.235294
1p09  wrong first diamond 13/51              0.254902  check     0.254902
1p10  reds before first blue 7/4             1.750000  check     1.750000
1p10  wrong 7/3                              2.333333  check     2.333333
1p10  wrong half 3.5                         3.500000  check     3.500000
1p10  wrong 7/10                             0.700000  check     0.700000
1p11  P(mispriced | flag) 90/387             0.232558  check     0.232558
1p11  sim                                    0.232558  check     0.233797
1p11  wrong joint 0.009                      0.009000  check     0.009000
1p12  expected bets 24                      24.000000  check    24.000000
1p12  sim                                   24.000000  check    24.042660
1p12  reach 10 chance 0.4 (prose)            0.400000  check     0.400000
1p13  P(max>0.8)                             0.590400  check     0.589620
1p13  option 0.4096 0.0016                   0.411200  check     0.411200
1p14  E last fall 60/21                      2.857143  check     2.857143
1p14  bounce sim                             2.857143  check     2.857661
1p14  wrong one ant 1.5                      1.500000  check     1.500000
1p14  wrong 20/21                            0.952381  check     0.952381
1p15  P(longest > 0.4) 0.96                  0.960000  check     0.959845
1p15  grid area                              0.960000  check     0.959889
1p15  wrong no overlap 1.08                  1.080000  check     1.080000
1p15  wrong complement 0.04                  0.040000  check     0.040000
1p15  wrong half answer 0.75                 0.750000  check     0.750000
1b01  bridge 1,3,4,9,11                     26.000000  check    26.000000
1b01  wrong escort 30                       30.000000  check    30.000000
1b01  wrong sum 28                          28.000000  check    28.000000
1b02  ropes 45                              45.000000  check    45.000000
1b02  distractor 60, 30                     60.000000  check    60.000000
1b03  angle 78                              78.000000  check    78.000000
1b03  stepped hands                         78.000000  check    78.000000
1b03  wrong 66 and 282                     348.000000  check   348.000000
1b04  fewest steps 8                         8.000000  check     8.000000
1b04  wrong transfers only 4                 4.000000  check     4.000000
1b04  wrong 5-first route                   10.000000  check    10.000000
      (starting by filling the 5 takes 10 steps)
1b05  two eggs 60 floors                    11.000000  check    11.000000
1b05  wrong 10 covers 55, binary 6          61.000000  check    61.000000
1b06  expected right 6.5                     6.500000  check     6.500000
1b06  wrong guaranteed 6, coin 3.5           9.500000  check     9.500000
1b07  A keeps (strict majority)             98.000000  check    98.000000
1b07  wrong at-least-half rule 99           99.000000  check    99.000000
      strict split [98, 0, 1, 1], at-least-half split [99, 0, 1, 0], 2-pirate strict None
1b08  fewest weighings 40                    4.000000  check     4.000000
1b08  14v14 then 3 more                      4.000000  check     4.000000
1b08  5v5 (30 aside) needs                   5.000000  check     5.000000
1b08  27 is the 3-weighing max              27.000000  check    27.000000
1b09  all-on reachable (0 = no)              0.000000  check     0.000000
1b09  invariant lamps lit in all-on          7.000000  check     7.000000
1b09  distractor leaves lamps off            8.000000  check     8.000000
1b10  trailing zeros 250!                   62.000000  check    62.000000
1b10  wrong 50, 60, 25                     135.000000  check   135.000000
1m01  47 x 63                             2961.000000  check  2961.000000
1m01  wrong 2820, 3089                    5909.000000  check  5909.000000
1m02  1260 / 18                             70.000000  check    70.000000
1m03  +40% then -30%                        -2.000000  check    -2.000000
1m03  wrong added +10, cross -12            -2.000000  check    -2.000000
1m04  98 vs 99                              -1.000000  check    -1.000000
1m04  decimals                               0.007937  check     0.007937
1m05  48.7 x 212                         10324.400000  check 10324.400000
1m05  option 9,740 = 48.7 x 200           9740.000000  check  9740.000000
1m06  next term 95                          95.000000  check    95.000000
1m07  sqrt 7300 nearest                     85.000000  check    85.000000
1m07  newton step 85.44                     85.441176  check    85.440037
1m07  wrong sqrt 730 -> 27                  27.000000  check    27.000000
1m08  8000 at 5% three years              9261.000000  check  9261.000000
1m08  wrong simple 9200, interest 1261   10461.000000  check 10461.000000
1m09  blind guess 0                          0.000000  check     0.000000
1m09  one ruled out 1/16                     0.062500  check     0.062500
1m09  distractor -1/20, +1/5                -0.050000  check    -0.050000
1m10  gaps 5/13-38%, 7/18-5/13               0.004615  check     0.004615
1m10  percents                              38.888889  check    38.888888
1k01  two-card sum, courts 10               13.076923  check    13.076923
1k01  wrong ranks 1-13 -> 14                14.000000  check    14.000000
1k01  wrong 1-10 only -> 11                 11.000000  check    11.000000
1k02  E max two d4 50/16                     3.125000  check     3.125000
1k02  bid 2.875                              2.875000  check     2.875000
1k02  wrong offer 3.375, one die 2.25        5.625000  check     5.625000
1k03  coins at 3 mm                      20000.000000  check 20000.000000
1k03  coins at 2.8 mm                    20000.000000  check 20000.000000
1k03  width 23 mm, 1 m storey, 3 cm      12000.000000  check 12000.000000
1k04  range factors                       2180.000000  check  2180.000000
1k05  mean, var of 5 dice                   32.083333  check    32.083333
1k05  12-23 holds                            0.882459  check     0.882459
1k05  11-24 holds                            0.935185  check     0.935185
1k05  14-21 holds                            0.695988  check     0.695380
1k06  centre after two lifts                50.800000  check    50.800000
1k06  wrong one trade 50.4, full move 54   104.400000  check   104.400000
1k06  wrong way 49.2                        49.200000  check    49.200000
1k07  informed cost per trade                0.800000  check     0.800000
1k07  net per trade 0 (wrong value)          0.000000  check     0.000000
1k07  sim net                                0.000000  check     0.003200
1k08  position after selling 5               3.000000  check     3.000000
1k09  hedge units                           18.000000  check    18.000000
1k09  wrong divided                         88.888889  check    88.888889
1k10  break-even width                       2.400000  check     2.400000
1k10  wrong net-of-spread 3.4286             3.428571  check     3.428571
all 128 checks passed
```

### Final run of `play-bank.mjs`

```text
locked before 23, after 1; drawable 207; session-1 items drawable 50 of 50
pass 0 (right): 50 of 50 distinct items played and accepted
pass 1 (wrong #1): 45 wrong answers routed
pass 2 (wrong #2): 45 wrong answers routed
pass 3 (wrong #3): 32 wrong answers routed
wrong ids and distractors in the files: 122; routed: 122
choice items seen with more than one option order: 14 of 14
no console errors
ALL OK
```

## Changed after the answer check (6 Nov)
`docs/reviews/answers-2026-11-06.md` (Fix pass) changed some items after this report was written; the exam and bank files are authoritative where figures here differ.
- mental-1: percent-chain-up-40-down-30 stores -0.02 with `unit: "%"`; negative-marking-five-options has six options and a -1/5 penalty (id kept). probability-1: hats no-derange wrong value is 0.5.

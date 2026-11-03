# Report: interview bank part 1, session 2 (50 items)

Brief: `docs/briefs/bank.md`, sections 1 to 4, "Session 2" in section 5, sections 6 to 9 and "Changes after session 1 (3 Nov)" (families `every-coupon` and `hats`, rubric shape 2, 2, 2, 2, 1, 1). Pattern copied from `app/content/bank/*-1.json` and `docs/reports/bank-1-1.md`. Files written in `app/content/bank/`; nothing else in the repo was edited apart from this report and the inbox bullets.

| File | Items | Families |
| --- | --- | --- |
| `probability-2.json` | 15 | dice-ev 2, when-to-stop 2, indicator-tricks, fair-from-biased, estimating-n, given-the-total, duels, semicircle, exceeding-one, meeting, who-wins, cards-and-colours, urns |
| `brainteasers-2.json` | 10 | hourglasses, common-knowledge, pigeonhole-pairs, pigeonhole-worst-case, cycle-following, last-digit, rule-of-72, average-speed, work-rate, colouring-chequer |
| `mental-2.json` | 10 | mental-arithmetic 2, percent-reverse, percent-points, fraction-gap, estimate-exact, sequence-differences, sequence-ratio, sqrt-vol, skip-budget |
| `market-making-2.json` | 8 | card-fair, digit-count, fermi, skew, arbitrage, contracts, options-game, outcome-vs-edge |
| `behavioural-2.json` | 7 | star-story 2, why-us, video-answer, after-rejection, project-account, reasoning-aloud |

## Results

- `node tools/validate.mjs 2>&1 | tail -5` (from `app/`): **0 errors**, 392 warnings, none from `content/bank/` (no `style` or `source` warning). The manifest lists the five new files.
- `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>`: **All passed** (`#bank 124 drawable of 210`, deck, pace line, schedule, miss, old save). With `--mobile`: **All passed**. The 210 are all four sessions' files plus `sample.json`; sessions 3 and 4 had landed by the time of the run.
- **Deck loop** (acceptance 3): `scratchpad/s2/bank-1-2/play-bank.mjs` (full path `/tmp/claude-0/-home-user-zero-to-quant/4b8cce5e-d242-5446-84a4-7179e480b15a/scratchpad/s2/bank-1-2/play-bank.mjs`), at 390 × 844, serving the CDN from the `pkgs` folder as `--local-cdn` does. It copies the `bankChecks` loop (`#bank`, `ZQ.test.continue()`, `answerCorrect()`, `check()`, `continue()`), wraps `ZQ.select.bankDeck` only to record the uids it deals, finishes the 18 lessons named in `requires` with `ZQ.state.lessonFinished` (locked count 86 before, 48 after: the other sessions' prerequisites), and schedules every other drawable item 30 days away with `ZQ.state.bankResult`, so only session-2 items are new. Then:
  - pass 0: **50 of 50** items dealt and accepted with the authored answer, in 7 decks of 8 (the 7 longform items and the expression included);
  - passes 1 to 4: the session-2 schedule entries are removed (export, delete, import) and decks are dealt again. Each numeric `wrong` value is typed, each choice distractor clicked and each expression `wrong` set in the maths field, one per pass. **122 of 122** wrong ids and distractors routed: each returned its own key, and its result line equalled the `byKey` line or the option's `why`;
  - every `choice` showed exactly one correct option among its 3 or 4, and all **14 of 14** choice items were seen in more than one option order (`shuffle: true` works);
  - no console errors, no page wider than 390 px. The run output is at the end of this report.
- Screenshots: 93 at 390 px (pass 0 every item before Check, pass 1 every wrong route after Check), looked at as contact sheets in `scratchpad/s2/bank-1-2/sheets/`. One fault found and fixed: the key option of `2p11` used `\tfrac12`, which rendered too small inside an option button (the session-1 fault), so it now reads $e^{1.5} - 0.5e^{0.5}$. Longform model answers fill a scrolling box under the prompt, as in session 1.
- **Voice scan**, `VOICE_BASE=/home/user/zero-to-quant/app/content/bank/ python3 docs/reviews/voice-scan.py --summary`: **explanations over three sentences: 0; over 20 words: 0** (5,395 sentences across the whole folder: all four sessions and `sample.json`). The first scan found the five file `description` lines of my files at 21 to 31 words; all were shortened. `gen.py` also refuses any sentence of 20 words or more, so every sentence in my files is at most 19 words.
- No `!` outside KaTeX, no em-dashes or en-dashes, British spelling, £ throughout, no firm names (the models use "a trading firm", "a small charity", "a society team").

## Counts against the brief

- Per file: 15, 10, 10, 8, 7 (section 2).
- Per difficulty: D2 10, D3 18, D4 16, D5 6. Per kind: numeric 28, choice 14, expression 1, longform 7 (the session-2 rows of section 2).
- Per family: the session-2 column of section 3, each family once except dice-ev, when-to-stop, mental-arithmetic and star-story, twice each. Every family already has course items carrying it as first tag except `mental-arithmetic`, which the engine gives generated items.
- `requires` on all 22 difficulty 4 and 5 items, none below. Every `pace` is the table's value; the largest is 180.
- Rubric shape: six lines worth 2, 2, 2, 2, 1, 1 on all seven longform items. Models are 134 to 156 words, first person, invented candidates, generic settings.
- Item ids are unique across the whole bank (checked after sessions 3 and 4 landed: no id appears twice in the 210 items).

## Items, refs and changes from the table

| Ref | Id | Family | Kind | D | Pace | Key | `wrong` values |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2p01 | `dice-ev-larger-d6-d4` | dice-ev | numeric | 3 | 100 | 3.9167 | 3.5, 4.4722, 3 |
| 2p02 | `dice-ev-square-n-sides` | dice-ev | expression | 4 | 120 | `\frac{(n+1)(2n+1)}{6}` | `\frac{(n+1)^2}{4}`, `\frac{n(n+1)(2n+1)}{6}` |
| 2p03 | `indicator-tricks-biased-runs` | indicator-tricks | numeric | 4 | 150 | 5.62 | 6.04, 4.62, 6.5 |
| 2p04 | `when-to-stop-d12-paid-reroll` | when-to-stop | numeric | 3 | 120 | 7.5417 | 6.5, 8, 7.5 |
| 2p05 | `when-to-stop-three-red-two-black` | when-to-stop | numeric | 5 | 180 | 1.5 | 1, 1.1 |
| 2p06 | `fair-from-biased-quarter-coin` | fair-from-biased | numeric | 3 | 120 | 5.3333 | 2.6667, 2 |
| 2p07 | `estimating-n-five-tickets` | estimating-n | numeric | 3 | 120 | 99.8 | 84, 100.8, 104 |
| 2p08 | `given-the-total-a-four-shows` | given-the-total | numeric | 4 | 120 | 0.1818 | 0.1667, 0.1111, 0.0909 |
| 2p09 | `duels-weaker-shoots-first` | duels | numeric | 4 | 120 | 0.5172 | 0.3, 0.4286, 0.4828 |
| 2p10 | `semicircle-seven-points` | semicircle | choice | 4 | 150 | 7/64 ≈ 0.109 | 3 distractors |
| 2p11 | `exceeding-one-past-three-halves` | exceeding-one | choice | 5 | 180 | $e^{1.5} - 0.5e^{0.5} \approx 3.66$ | 3 distractors |
| 2p12 | `meeting-forty-minute-window` | meeting | numeric | 3 | 120 | 0.51 | 0.3, 0.6, 0.49 |
| 2p13 | `who-wins-last-stone-loses` | who-wins | choice | 3 | 100 | Go first and take 1, leaving 26. | 3 distractors |
| 2p14 | `cards-and-colours-reds-before-ace` | cards-and-colours | numeric | 5 | 150 | 4.8 | 5.2, 9.6, 6 |
| 2p15 | `urns-polya-three-red-two-blue` | urns | numeric | 4 | 150 | 0.3429 | 0.432, 0.1143, 0.6286, 0.6 |
| 2b01 | `hourglasses-five-and-eight` | hourglasses | numeric | 3 | 120 | 4 | 2, 3 |
| 2b02 | `common-knowledge-three-marks` | common-knowledge | choice | 5 | 150 | Round 3: two silent rounds rule out one ma... | 3 distractors |
| 2b03 | `pigeonhole-pairs-birth-months` | pigeonhole-pairs | choice | 2 | 60 | 3 | 3 distractors |
| 2b04 | `pigeonhole-worst-case-four-alike` | pigeonhole-worst-case | numeric | 4 | 90 | 16 | 6, 20, 15 |
| 2b05 | `cycle-following-two-hundred-boxes` | cycle-following | choice | 5 | 180 | About 31%: all succeed exactly when no loo... | 3 distractors |
| 2b06 | `last-digit-17-to-2031` | last-digit | numeric | 2 | 60 | 3 | 7, 9, 1 |
| 2b07 | `rule-of-72-tripling` | rule-of-72 | numeric | 3 | 60 | 19 | 12, 24, 33 |
| 2b08 | `average-speed-there-and-back` | average-speed | numeric | 2 | 60 | 42 | 50, 21 |
| 2b09 | `work-rate-two-of-three-pumps` | work-rate | numeric | 2 | 75 | 3.4286 | 7, 2.6667, 14 |
| 2b10 | `colouring-chequer-ten-board` | colouring-chequer | choice | 3 | 100 | No. Both corners have one colour, leaving ... | 3 distractors |
| 2m01 | `mental-arithmetic-86-by-44` | mental-arithmetic | numeric | 2 | 25 | 3784 | 3440, 37840 |
| 2m02 | `mental-arithmetic-3150-by-14` | mental-arithmetic | numeric | 2 | 25 | 225 | 22.5, 2250 |
| 2m03 | `percent-reverse-after-a-rise` | percent-reverse | numeric | 2 | 20 | 120 | 112.5, 125 |
| 2m04 | `percent-points-rate-move` | percent-points | choice | 2 | 20 | 2 percentage points, a 50% rise | 3 distractors |
| 2m05 | `fraction-gap-two-pairs` | fraction-gap | choice | 3 | 30 | 3/4 and 5/7: the gap is 1/28, against 1/45... | 3 distractors |
| 2m06 | `estimate-exact-31-2-by-19-8` | estimate-exact | choice | 4 | 25 | 617.76 | 3 distractors |
| 2m07 | `sequence-differences-odd-steps` | sequence-differences | numeric | 4 | 30 | 28 | 26, 31, 27 |
| 2m08 | `sequence-ratio-half-again` | sequence-ratio | numeric | 3 | 25 | 20.25 | 18, 27 |
| 2m09 | `sqrt-vol-daily-from-annual` | sqrt-vol | numeric | 3 | 30 | 0.015 (%) | 0.0009375, 0.012562, 3.84 |
| 2m10 | `skip-budget-fifty-in-six` | skip-budget | choice | 4 | 30 | 7.2 s a question; skip only the 22 s one a... | 3 distractors |
| 2k01 | `card-fair-hearts-revealed` | card-fair | numeric | 3 | 90 | 1.4706 | 1.5, 0.75, 1.75 |
| 2k02 | `digit-count-ones-to-200` | digit-count | numeric | 4 | 100 | 140 | 40, 100, 120 |
| 2k03 | `fermi-london-black-cabs` | fermi | choice | 2 | 75 | About 10,000 | 3 distractors |
| 2k04 | `skew-short-six` | skew | choice | 3 | 60 | Raise both the bid and the offer by the sa... | 3 distractors |
| 2k05 | `arbitrage-sum-contract` | arbitrage | numeric | 3 | 90 | 1 | 4, 5, 6 |
| 2k06 | `contracts-larger-minus-three` | contracts | numeric | 4 | 90 | 1.6722 | 1.4722, 0.7, 1.8722, 4.6722 |
| 2k07 | `options-game-card-call` | options-game | numeric | 5 | 120 | 1.6923 | 0.5385, 2.1538, 1.1538 |
| 2k08 | `outcome-vs-edge-losing-trade` | outcome-vs-edge | choice | 2 | 60 | Sound, if the £100 value was well founded ... | 3 distractors |
| 2h01 | `star-story-led-without-the-title` | star-story | longform | 4 | 150 | model and rubric |  |
| 2h02 | `star-story-learned-it-fast` | star-story | longform | 3 | 150 | model and rubric |  |
| 2h03 | `why-us-market-maker-not-fund` | why-us | longform | 3 | 120 | model and rubric |  |
| 2h04 | `video-answer-what-sets-you-apart` | video-answer | longform | 4 | 150 | model and rubric |  |
| 2h05 | `after-rejection-what-came-next` | after-rejection | longform | 3 | 150 | model and rubric |  |
| 2h06 | `project-account-in-plain-words` | project-account | longform | 4 | 180 | model and rubric |  |
| 2h07 | `reasoning-aloud-a-puzzle-you-know` | reasoning-aloud | longform | 4 | 150 | model and rubric |  |

Changes from the session-2 table. Each is for rule 10 and DECISIONS "Duplicates (6 Nov)" (a course, exam or bank item with the same structure and numbers) unless stated:

1. `2p04`: "a d10 up to twice" → a d12 with a £1 fee for the one reroll (181/24 ≈ £7.54). The free d10 reroll is `bank/probability-1` `dice-ev-ten-sided-reroll` (1p01), the same game and numbers.
2. `2p06`: heads chance 0.2 → 1/4 (16/3 flips). `puzzles/l25` screen 11 uses 0.8, the same $pq = 0.16$ and 6.25 flips.
3. `2p08`: the idea as written ("sum to 9 given a 4: chance it is (4, 5)") is certain, since a 9 with a 4 must be 4 and 5. Read as: given at least one 4, the chance the total is 9 (2/11). Not a duplicate change.
4. `2p09`: 1/3 against 1/2 → 0.3 against 0.4 (15/29). `puzzles/l28` screen 0 is the 1/3 and 1/2 duel with A first.
5. `2p10`: four points → seven (7/64). Four points is `puzzles/l14` screen 3; five is its drill; six its quiz.
6. `2p11`: sum past 2 → sum past 1.5 ($e^{1.5} - 0.5e^{0.5} \approx 3.66$). `puzzles/homework-3` item `hw3-exceed-two` asks the sum past 2.
7. `2p12`: a 45-minute window and 10-minute waits → 40 and 12 (0.51). `puzzles/l16` quiz 2 uses the 45-minute window; 30 and 6 (screen 9) gives 0.36, so 40 and 12 were chosen.
8. `2p13`: 23 stones → 27 (take 1). `puzzles/l19` screen 9 uses 23 matches with takes of 1 to 3.
9. `2p15`: Pólya from 2 red and 1 blue → 3 red and 2 blue (12/35). `puzzles/l8` screen 7 starts its Pólya urn from 2 red and 1 blue. (3 and 1, and 2 and 2, both give 0.3, so they were not used.)
10. `2b01`: 4- and 7-minute glasses for 9 → 5 and 8 for 11 (4 turns). `brainteasers/l5` screen 9 is 4 and 7 for 9; screen 7 is 5 and 9 for 13; `review-1` item 4 is 6 and 11 for 16. The idea's "fewest flips" is defined in the prose: turns that start a glass count.
11. `2b02`: three logicians → five with three marked (round 3). `brainteasers/l10` covers three children, seven islanders and four coffee logicians.
12. `2b03`: 13 people → 25 (three share a month). `brainteasers/l3` quiz 2 is 13 people and a shared month.
13. `2b04`: four colours, three alike → five colours, four alike (16). `brainteasers/l3` screen 10 is exactly four colours, three alike (9).
14. `2b06`: $7^{2026}$ → $17^{2031}$ (3). `brainteasers/l13` screens 0 and 1 and `homework-3` item 0 use $7^{2026}$; $3^{2027}$ is its drill and $8^{2027}$ is in `mock-superday-trader`.
15. `2b08`: 40 then 60 mph → 30 then 70 mph over 63 miles (42). `brainteasers/l12` screen 3 is 60 then 40 km/h (48); 30 and 60 is `l16`; 45 and 90 is `review-3`.
16. `2b10`: an 8 by 8 board → 10 by 10 (no). Not a course duplicate, but rule 1 asks for our own numbers on the classic board.
17. `2m04`: 4% to 5% → 4% to 6% (2 points, 50%). 4% to 5% is `mental-pressure/l6` screen 4 and `ratio/l3` screen 6.
18. `2m05`: 5/8 and 3/5 against 7/12 and 4/7 → 3/4 and 5/7 against 4/5 and 7/9 (1/28 against 1/45). `mental-pressure/l5` screen 5 asks the gap of 7/12 and 5/9; its quiz uses 8/13; its drill holds 4/9 against 3/7.
19. `2m10`: 80 questions in 8 minutes → 50 in 6 minutes, with 42 s left and five questions of 6, 22, 9, 15 and 7 s. `mental-pressure/l9` is the 80-in-8 lesson (6 s each) and its quiz 0 has "40 s left".
20. `2k01`: "fair value of hearts in three cards and a two-way price" → the fair value after the first card shows a heart (25/17), with the opening quote in the prose. A two-way price cannot be graded as one number (inbox bullet).
21. `2k06`: the graded number is the offer of a quote 0.4 wide around 53/36, so "a price you would quote" is marked (as session 1's `1k02` marks a bid).
22. `2k07`: "call struck at 6 on a card game" is made a difficulty-5 item by counting court cards as 10 (22/13), so the plain 1 to 13 answer (28/13) is a distractor. `mm-games/l17` uses the two-dice sum only.

No idea was swapped for another family or kind.

The five closest course items found (acceptance 6), with what changed: `puzzles/homework-3` `hw3-exceed-two` (sum past 2) → past 1.5; `brainteasers/l3` screen 10 (four colours, three alike) → five colours, four alike; `puzzles/l28` screen 0 (duel 1/3 against 1/2) → 0.3 against 0.4; `brainteasers/l13` screens 0 and 1 ($7^{2026}$) → $17^{2031}$; `brainteasers/l12` screen 3 (there and back at 60 and 40, 48) → 30 and 70 (42).

Near items kept, for the second reader: `2p04` (d12, one paid reroll) and session 4's `dice-ev-twelve-sided-three-rolls` (d12, up to three free rolls) share a die but not the game, written in parallel; `2b04`'s wrong value 6 is the key of `brainteasers/l16` screen 0 (five colours, a pair), which only routes feedback.

## Every number, two ways

The script below asserts each pair. Method A is the closed form; method B is enumeration, a recursion, a search or a seeded simulation (tolerance in the script). Every numeric `wrong` value is computed in the script from its named slip, and `gen.py` asserts that each item's key and wrong values equal the script's within tolerance, and that no wrong value sits inside the key's tolerance.

| Ref | Key | Method A | Method B |
| --- | --- | --- | --- |
| 2p01 | 47/12 ≈ 3.9167 | enumerate the 24 rolls | tail sum $\sum_k P(\max > k)$ |
| 2p02 | $(n+1)(2n+1)/6$ | sum of squares over $n$ | enumeration for $n = 1$ to 30; 38.5 at ten sides |
| 2p03 | 5.62 | $1 + 11 \times 2pq$ | all $2^{12}$ sequences, weighted |
| 2p04 | 181/24 ≈ 7.5417 | best threshold over all 13 rules | $\tfrac{7}{12} \times 9 + \tfrac{5}{12} \times 5.5$; simulation 7.539 |
| 2p05 | 3/2 | backward induction $V(r, b)$ | the optimal rule played on all 10 arrangements |
| 2p06 | 16/3 | $1/(pq)$ | $2/(2pq)$; simulation 5.342 |
| 2p07 | 99.8 | $m + m/k - 1$ | $m + (m - k)/k$; unbiased in a simulation with $N = 120$ |
| 2p08 | 2/11 | count the 11 rolls with a 4 | $2/(36 - 25)$ |
| 2p09 | 15/29 | $p/(1 - (1-p)(1-q))$ | series to 400 terms; simulation 0.5172 |
| 2p10 | 7/64 | $n/2^{n-1}$ | simulation of the largest gap 0.1094 |
| 2p11 | 3.6573 | $e^{1.5} - 0.5e^{0.5}$ | renewal series; simulation 3.661 |
| 2p12 | 0.51 | $1 - (28/40)^2$ | simulation 0.511; grid 0.5104 |
| 2p13 | take 1 | backward induction on piles | losing piles are 1 mod 5, checked to 60 |
| 2p14 | 24/5 | $24 \times 1/5$ | $(53/5 - 1) \times 24/48$; simulation 4.792 |
| 2p15 | 12/35 | path enumeration of the urn | $3 \times \tfrac{3 \cdot 4 \cdot 2}{5 \cdot 6 \cdot 7}$ |
| 2b01 | 4 turns | Dijkstra over glass states and events | the stated plan replayed to 11 |
| 2b02 | round 3 | possible-worlds model of five logicians | the one and two mark cases (rounds 1 and 2); unmarked know in round 4 |
| 2b03 | 3 | $\lceil 25/12 \rceil$ | 24 people fit two a month |
| 2b04 | 16 | $k(r - 1) + 1$ | 15 = three of each colour |
| 2b05 | 0.3093 | $1 - (H_{200} - H_{100})$ | simulation of 40,000 shuffles 0.310; near $1 - \ln 2$ |
| 2b06 | 3 | `pow(17, 2031, 10)` | cycle 7, 9, 3, 1 at remainder 3 |
| 2b07 | 19 | $\ln 3/\ln 1.06 = 18.85$ | compound year by year until at least 3 |
| 2b08 | 42 | $126/(2.1 + 0.9)$ | $2 \times 30 \times 70/100$ |
| 2b09 | 24/7 | $1/(1/6 + 1/8)$ | $6 \times 8/(6 + 8)$ |
| 2b10 | no | colour count 48 and 50 | maximum matching on the 98 squares is 48 |
| 2m01 | 3,784 | 86 × 44 | $65^2 - 21^2$ |
| 2m02 | 225 | 3150/14 | 1575/7 |
| 2m03 | £120 | 150/1.25 | 150 × 4/5 |
| 2m04 | 2 points, 50% | 6 − 4, 2/4 | (choice) |
| 2m05 | 1/28 > 1/45 | Fraction differences | cross products over products of bottoms |
| 2m06 | 617.76 | 31.2 × 19.8 | $25.5^2 - 5.7^2$ |
| 2m07 | 28 | 19 + 7 + 2 | $5^2 + 3$ |
| 2m08 | 20.25 | 13.5 × 1.5 | $4 \times 1.5^4$ |
| 2m09 | 1.5% | 24%/√256 | 24%/16 |
| 2m10 | 7.2 s; skip the 22 s | best subset by search | 360/50; the in-order run answers 3 |
| 2k01 | 25/17 | pairs of the 51 cards left | $1 + 2 \times 12/51$ |
| 2k02 | 140 | count every 1 written | 20 + 100 + 20 |
| 2k03 | about 10,000 | 108 million trips ÷ 6,000 = 18,000 | (choice; nearer $10^4$ than $10^5$ on a log scale) |
| 2k04 | raise both | (choice) | (choice) |
| 2k05 | £1 | the four trade directions | 56 − (22 + 33) |
| 2k06 | 1.6722 | enumerate the 36 rolls, + 0.2 | $161/36 - 3 + 0.2$ |
| 2k07 | 22/13 | put plus mean less strike | $(1 + 2 + 3 + 16)/13$ |
| 2k08 | sound decision | (choice) | (choice) |

## Proposals (course items to tag; not edited)

- Every session-2 family except `mental-arithmetic` is already the first tag of some course item, so no new tagging is needed for session 2.
- The session-1 question stands: `puzzles/l1` tags its items `dice-games`, while `2p01` and `2p02` (which draw on that lesson) use `dice-ev` as briefed.

## Open questions

1. `dice-ev` or `dice-games` for the probability dice items that draw on `puzzles/l1-dice-games` (repeats session 1's question 2)?
2. `2p04` and session 4's `4p01` both use a twelve-sided die in a stopping game (one paid reroll against three free rolls). The second reader may want one of them on another die; every die size from 8 to 20 is already used by a stopping item somewhere.
3. The brief's `2p08` idea was ambiguous; the item asks P(total 9 | at least one 4). Confirm that is the intended reading.

## Inbox

Five bullets under `Bank session 2 (3 Nov):` at the end of `docs/BACKLOG-INBOX.md`: the test hook for wrong answers (with the expression case), duplicates across parallel sessions, a factor tolerance for Fermi numerics, a two-way quote widget, and `\tfrac` in options (second vote).

## Scripts

`scratchpad/s2/bank-1-2/` holds `bank-1-2.py` (numbers), `hg.py` (the hourglass search it imports), `gen.py` (builds the five files from item data and asserts one correct option, the rubric shape, model length, `requires` only at D4 and D5, pace at most 180, sentences under 20 words, ids unique, and key and wrong values against the script), `play-bank.mjs` (the deck loop), `shots/` and `sheets/` (390 px screenshots and contact sheets).

### `bank-1-2.py`

```python
"""Bank part 1, session 2: every keyed answer and every numeric wrong value, two ways each, with asserts.
Writes nothing into the repo. Run: python3 bank-1-2.py  (KEYS is imported by gen.py to check the item files)."""
from fractions import Fraction as F
from itertools import product, permutations, combinations
from math import comb, log, e, sqrt, ceil
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hg import solve as hourglass
rng = random.Random(20261103)
OUT, KEYS = [], {}
def rec(ref, name, a, b, tol=0):
    a_, b_ = float(a), float(b)
    assert abs(a_ - b_) <= tol, (ref, name, a, b)
    OUT.append(f'{ref:5} {name:34} {a_:12.6f}  check {b_:12.6f}')
    KEYS.setdefault(ref, {})[name] = a_
def sim(f, n=200000):
    return sum(f() for _ in range(n)) / n

# ---------- probability-2 ----------
# 2p01 larger of a d6 and a d4
enum = F(sum(max(a, b) for a in range(1, 7) for b in range(1, 5)), 24)
tail = sum(1 - F(min(k, 6), 6) * F(min(k, 4), 4) for k in range(0, 6))
rec('2p01', 'key', enum, tail)
rec('2p01', 'd6-only', F(7, 2), F(sum(range(1, 7)), 6))
rec('2p01', 'two-d6', F(sum(max(a, b) for a in range(1, 7) for b in range(1, 7)), 36), F(161, 36))
rec('2p01', 'mean-of-means', (F(7, 2) + F(5, 2)) / 2, 3)
# 2p02 E[X^2] for an n-sided die, as an expression; check against enumeration for n = 1..30, and n = 10 gives 38.5
for n in range(1, 31):
    assert F(sum(k * k for k in range(1, n + 1)), n) == F((n + 1) * (2 * n + 1), 6)
    assert F(n * (n + 1) * (2 * n + 1), 6) != F((n + 1) * (2 * n + 1), 6) or n == 1
    assert F((n + 1) ** 2, 4) != F((n + 1) * (2 * n + 1), 6) or n == 1
rec('2p02', 'n=10 value', F(sum(k * k for k in range(1, 11)), 10), F(11 * 21, 6))
# 2p03 runs in 12 flips, P(H) = 0.3
p, q = F(3, 10), F(7, 10)
exact = 0
for s in product('HT', repeat=12):
    w = p ** s.count('H') * q ** s.count('T')
    exact += w * (1 + sum(s[i] != s[i - 1] for i in range(1, 12)))
rec('2p03', 'key', 1 + 11 * 2 * p * q, exact)
rec('2p03', 'twelve-gaps', 1 + 12 * 2 * p * q, F(604, 100))
rec('2p03', 'no-first', 11 * 2 * p * q, F(462, 100))
rec('2p03', 'fair-coin', 1 + 11 * F(1, 2), F(13, 2))
# 2p04 d12, one optional reroll that costs £1; you must keep the second roll
def reroll_once(n, keep_from, cost):
    fresh = F(n + 1, 2) - cost
    return F(sum(k if k >= keep_from else fresh for k in range(1, n + 1)), n)
best = max(reroll_once(12, t, 1) for t in range(1, 14))
assert best == reroll_once(12, 6, 1)
rec('2p04', 'key', best, F(7, 12) * F(6 + 12, 2) + F(5, 12) * (F(13, 2) - 1))
rec('2p04', 'key sim', best, sim(lambda: (lambda r: r if r >= 6 else rng.randint(1, 12) - 1)(rng.randint(1, 12))), 0.02)
rec('2p04', 'no-reroll', F(13, 2), F(sum(range(1, 13)), 12))
rec('2p04', 'free-reroll', reroll_once(12, 7, 0), F(1, 2) * F(19, 2) + F(1, 2) * F(13, 2))
rec('2p04', 'keep-seven', reroll_once(12, 7, 1), F(1, 2) * F(19, 2) + F(1, 2) * F(11, 2))
# 2p05 three red, two black, +1 / -1, stop any time
from functools import lru_cache
@lru_cache(None)
def V(r, b):
    if r == 0: return F(0)
    if b == 0: return F(r)
    go = F(r, r + b) * (1 + V(r - 1, b)) + F(b, r + b) * (-1 + V(r, b - 1))
    return max(F(0), go)
# second method: brute force over all deterministic stopping rules that depend on (cards seen so far) via enumeration of arrangements
arr = set(permutations('RRRBB'))
def value_of_rule(stop):
    tot = 0
    for a in arr:
        s = 0
        for i, c in enumerate(a):
            if stop(a[:i]): break
            s += 1 if c == 'R' else -1
        tot += s
    return F(tot, len(arr))
hist = sorted({a[:i] for a in arr for i in range(6)}, key=len)
# the optimal rule from V: stop when V(remaining) == 0
opt = value_of_rule(lambda h: V(3 - h.count('R'), 2 - h.count('B')) == 0)
rec('2p05', 'key', V(3, 2), opt)
rec('2p05', 'key closed', V(3, 2), F(3, 5) * (1 + F(2, 3)) + F(2, 5) * (-1 + F(9, 4)))
rec('2p05', 'turn-all', value_of_rule(lambda h: False), 3 - 2)
tie_stop = value_of_rule(lambda h: (3 - h.count('R'), 2 - h.count('B')) == (2, 2) or V(3 - h.count('R'), 2 - h.count('B')) == 0)
rec('2p05', 'tie-zero', tie_stop, F(3, 5) * (1 + 0) + F(2, 5) * (-1 + F(9, 4)))
rec('2p05', 'stop-when-ahead equals turn-all', value_of_rule(lambda h: h.count('R') - h.count('B') > 0), 1)
# 2p06 von Neumann, P(H) = 1/4: expected flips 1/(pq)
p = F(1, 4); q = 1 - p
rec('2p06', 'key', 1 / (p * q), 2 / (2 * p * q))
def vn():
    n = 0
    while True:
        a, b = rng.random() < 0.25, rng.random() < 0.25; n += 2
        if a != b: return n
rec('2p06', 'key sim', 1 / (p * q), sim(vn, 200000), 0.03)
rec('2p06', 'pairs', 1 / (2 * p * q), F(8, 3))
rec('2p06', 'one-pair', 2, 2)
# 2p07 five tickets from 1..N, largest 84: m + m/k - 1
m, k = 84, 5
rec('2p07', 'key', m + F(m, k) - 1, m + F(m - k, k))
Ntrue = 120
est = [ (lambda s: max(s) + F(max(s), k) - 1)(rng.sample(range(1, Ntrue + 1), k)) for _ in range(40000)]
rec('2p07', 'unbiased sim N=120', Ntrue, sum(map(float, est)) / len(est), 0.4)
rec('2p07', 'max-only', 84, 84)
rec('2p07', 'no-minus-one', m + F(m, k), F(m * (k + 1), k))
rec('2p07', 'k-minus-one', m + F(m, k - 1) - 1, 104)
# 2p08 given at least one 4, chance the total is 9
rolls = [(a, b) for a in range(1, 7) for b in range(1, 7)]
given = [r for r in rolls if 4 in r]
rec('2p08', 'key', F(sum(1 for r in given if sum(r) == 9), len(given)), F(2, 36 - 25))
rec('2p08', 'other-die', F(1, 6), F(1, 6))
rec('2p08', 'unconditional', F(sum(1 for r in rolls if sum(r) == 9), 36), F(1, 9))
rec('2p08', 'one-order', F(1, len(given)), F(1, 11))
# 2p09 duel, A hits 0.3 and fires first, B hits 0.4
pa, pb = F(3, 10), F(4, 10)
x = pa / (1 - (1 - pa) * (1 - pb))
series = sum(pa * ((1 - pa) * (1 - pb)) ** j for j in range(400))
rec('2p09', 'key', x, series, 1e-12)
def duel():
    while True:
        if rng.random() < 0.3: return 1
        if rng.random() < 0.4: return 0
rec('2p09', 'key sim', x, sim(duel), 0.005)
rec('2p09', 'first-shot', pa, F(3, 10))
rec('2p09', 'share', pa / (pa + pb), F(3, 7))
rec('2p09', 'b-chance', 1 - x, F(14, 29))
# 2p10 seven points on a circle in one semicircle (choice)
n = 7
def semi():
    pts = sorted(rng.random() for _ in range(n))
    gaps = [pts[i + 1] - pts[i] for i in range(n - 1)] + [1 - pts[-1] + pts[0]]
    return max(gaps) >= 0.5
rec('2p10', 'key', F(n, 2 ** (n - 1)), sim(semi, 300000), 0.003)
rec('2p10', 'one-start', F(1, 2 ** (n - 1)), F(1, 64))
rec('2p10', 'n-over-2n', F(n, 2 ** n), F(7, 128))
# 2p11 expected uniforms until the sum exceeds 1.5 (choice): e^1.5 - 0.5 e^0.5
import math
def renewal(t):
    return sum((-1) ** j * (t - j) ** j * math.exp(t - j) / math.factorial(j) for j in range(int(t) + 1))
def cnt(t=1.5):
    s_, c = 0.0, 0
    while s_ <= t: s_ += rng.random(); c += 1
    return c
key11 = math.exp(1.5) - 0.5 * math.exp(0.5)
rec('2p11', 'key', key11, renewal(1.5), 1e-12)
rec('2p11', 'key sim', key11, sim(cnt, 300000), 0.01)
rec('2p11', 'key t=1 check', renewal(1), e, 1e-12)
rec('2p11', 'scaled-e', 1.5 * e, 4.077423, 1e-6)
rec('2p11', 'corner-all-n', sum(1.5 ** j / math.factorial(j) for j in range(40)), math.exp(1.5), 1e-9)
rec('2p11', 'divide-by-mean', 1.5 / 0.5, 3)
# 2p12 window 40 minutes, each waits 12
w = F(12, 40)
def meet():
    return abs(rng.random() - rng.random()) <= 0.3
grid = 2000
cnt_ = sum(1 for i in range(grid) for j in range(grid) if abs(i - j) * 40 <= 12 * grid)
rec('2p12', 'key', 1 - (1 - w) ** 2, sim(meet, 300000), 0.004)
rec('2p12', 'key grid', 1 - (1 - w) ** 2, cnt_ / grid ** 2, 0.002)
rec('2p12', 'linear', w, F(3, 10))
rec('2p12', 'double', 2 * w, F(6, 10))
rec('2p12', 'complement', (1 - w) ** 2, F(49, 100))
# 2p13 27 stones, take 1 to 4, last stone LOSES (choice): winning first move
@lru_cache(None)
def mover_wins(s):  # s stones left, the player who takes the last stone loses
    if s == 0: return True  # the opponent took the last stone
    return any(not mover_wins(s - t) for t in range(1, 5) if t <= s)
good = [t for t in range(1, 5) if not mover_wins(27 - t)]
assert good == [1] and mover_wins(27)
assert all(mover_wins(s) == (s % 5 != 1) for s in range(1, 60))
rec('2p13', 'key take', good[0], 1)
# 2p14 red cards before the first ace
rec('2p14', 'key', F(24, 5), (F(53, 5) - 1) * F(24, 48))
deck = ['A'] * 4 + ['R'] * 24 + ['O'] * 24
def reds_before():
    d = deck[:]; rng.shuffle(d)
    return d[:d.index('A')].count('R')
rec('2p14', 'key sim', F(24, 5), sim(reds_before, 200000), 0.02)
rec('2p14', 'red-aces', F(26, 5), F(26, 5))
rec('2p14', 'all-cards', F(48, 5), F(53, 5) - 1)
rec('2p14', 'four-gaps', F(24, 4), 6)
# 2p15 Polya urn from 3 red 2 blue: exactly two reds in the first three draws
def polya_paths(r, b, n):
    out = {}
    def go(r_, b_, k, pr, reds):
        if k == n: out[reds] = out.get(reds, 0) + pr; return
        go(r_ + 1, b_, k + 1, pr * F(r_, r_ + b_), reds + 1)
        go(r_, b_ + 1, k + 1, pr * F(b_, r_ + b_), reds)
    go(r, b, 0, F(1), 0); return out
pp = polya_paths(3, 2, 3)
rec('2p15', 'key', pp[2], 3 * F(3 * 4 * 2, 5 * 6 * 7))
rec('2p15', 'no-reinforce', 3 * F(3, 5) ** 2 * F(2, 5), F(54, 125))
rec('2p15', 'one-order', F(3 * 4 * 2, 5 * 6 * 7), F(4, 35))
rec('2p15', 'at-least-two', pp[2] + pp[3], F(22, 35))
rec('2p15', 'no-replacement', F(comb(3, 2) * comb(2, 1), comb(5, 3)), F(6, 10))

# ---------- brainteasers-2 ----------
# 2b01 hourglasses 5 and 8, time 11 minutes, fewest turns (turns that start a glass count)
best = hourglass(5, 8, 11)
rec('2b01', 'key', best[0], 2 + 1 + 1)  # start both, turn the 5 at 5, turn the 5 again at 8
# replay the stated plan: the 5 runs 0-5, turned at 5 runs to 10, at 8 it has 2 on top and 3 below; turned, 3 run out at 11
top5 = 5; t = 5; top5 = 5; t2 = 8; top5 -= (t2 - t); top5 = 5 - top5
rec('2b01', 'plan replay end', t2 + top5, 11)
assert hourglass(5, 8, 11)[0] == 4 and all(hourglass(5, 8, 11)[0] <= 4 for _ in [0])
rec('2b01', 'starts-free', best[0] - 2, 2)
rec('2b01', 'one-start', best[0] - 1, 3)
# 2b02 five logicians, three marked, "at least one is marked", simultaneous rounds (choice): Kripke model
def rounds_to_know(actual):
    n = len(actual)
    worlds = [w for w in product((0, 1), repeat=n) if any(w)]
    def knows(i, w, W):
        cons = [v for v in W if all(v[j] == w[j] for j in range(n) if j != i)]
        return len({v[i] for v in cons}) == 1
    W = worlds[:]
    for rnd in range(1, n + 2):
        said = {w: tuple(knows(i, w, W) for i in range(n)) for w in W}
        if any(said[actual][i] for i in range(n)):
            return rnd, said[actual]
        W = [w for w in W if said[w] == said[actual]]
    return None, None
r_, who = rounds_to_know((1, 1, 1, 0, 0))
rec('2b02', 'key round', r_, 3)
assert who == (True, True, True, False, False)
def rounds_all(actual):
    n = len(actual); worlds = [w for w in product((0, 1), repeat=n) if any(w)]; W = worlds[:]; first = {}
    for rnd in range(1, 8):
        said = {w: tuple(len({v[i] for v in W if all(v[j] == w[j] for j in range(n) if j != i)}) == 1 for i in range(n)) for w in W}
        for i in range(n):
            if said[actual][i] and i not in first: first[i] = rnd
        W = [w for w in W if said[w] == said[actual]]
    return first
fa = rounds_all((1, 1, 1, 0, 0))
rec('2b02', 'unmarked know', fa[3], 4); assert fa == {0: 3, 1: 3, 2: 3, 3: 4, 4: 4}
rec('2b02', 'two marks check', rounds_to_know((1, 1, 0, 0, 0))[0], 2)
# 2b03 25 people, 12 months: largest number sure to share a month (choice)
rec('2b03', 'key', ceil(25 / 12), 3)
assert max(min(c) for c in [[2] * 12]) * 12 == 24  # 24 people can be two a month
# 2b04 five colours, four of one colour
k_, r__ = 5, 4
rec('2b04', 'key', k_ * (r__ - 1) + 1, 16)
assert 3 * 5 == 15  # the worst 15 holds three of each colour, no four
rec('2b04', 'pairs', k_ + 1, 6)
rec('2b04', 'all', k_ * r__, 20)
rec('2b04', 'no-plus-one', k_ * (r__ - 1), 15)
# 2b05 200 prisoners, 100 openings each, cycle-following (choice)
pwin = 1 - sum(F(1, j) for j in range(101, 201))
def maxcycle_ok(n=200, m=100):
    perm = list(range(n)); rng.shuffle(perm); seen = [False] * n
    for s in range(n):
        if seen[s]: continue
        L, x = 0, s
        while not seen[x]: seen[x] = True; x = perm[x]; L += 1
        if L > m: return 0
    return 1
rec('2b05', 'key', pwin, sim(maxcycle_ok, 40000), 0.008)
rec('2b05', 'key vs 1-ln2', pwin, 1 - log(2), 0.003)
rec('2b05', 'fail', 1 - pwin, sum(F(1, j) for j in range(101, 201)))
# 2b06 last digit of 17^2031
rec('2b06', 'key', pow(17, 2031, 10), [7, 9, 3, 1][(2031 - 1) % 4])
rec('2b06', 'r1', 7, pow(7, 1, 10)); rec('2b06', 'r2', 9, pow(7, 2, 10)); rec('2b06', 'r0', 1, pow(7, 4, 10))
# 2b07 years to triple at 6%
yrs = log(3) / log(1.06)
n_ = 0; bal = 1.0
while bal < 3: bal *= 1.06; n_ += 1
rec('2b07', 'key', round(yrs), n_)
rec('2b07', 'doubling', round(log(2) / log(1.06)), 72 / 6)
rec('2b07', 'simple', int(200 / 6), 33)
rec('2b07', 'quadruple', 2 * 12, 24)
# 2b08 63 miles out at 30 mph, back at 70 mph
rec('2b08', 'key', F(126, F(63, 30) + F(63, 70)), F(2 * 30 * 70, 100))
rec('2b08', 'mean', F(30 + 70, 2), 50)
rec('2b08', 'one-way', F(63, F(63, 30) + F(63, 70)), 21)
# 2b09 pumps 6 and 8 hours together
rec('2b09', 'key', 1 / (F(1, 6) + F(1, 8)), F(6 * 8, 6 + 8))
rec('2b09', 'average', F(6 + 8, 2), 7)
rec('2b09', 'all-three', 1 / (F(1, 6) + F(1, 8) + F(1, 12)), F(8, 3))
rec('2b09', 'sum', 6 + 8, 14)
# 2b10 10 x 10 board without two opposite corners: colour count and a maximum matching
cells = [(i, j) for i in range(10) for j in range(10) if (i, j) not in [(0, 0), (9, 9)]]
dark = [c for c in cells if (c[0] + c[1]) % 2 == 0]; light = [c for c in cells if (c[0] + c[1]) % 2 == 1]
cs = set(cells); match = {}
def aug(u, seen):
    for d in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        v = (u[0] + d[0], u[1] + d[1])
        if v in cs and v not in seen:
            seen.add(v)
            if v not in match or aug(match[v], seen):
                match[v] = u; return True
    return False
mm = sum(aug(u, set()) for u in dark)
rec('2b10', 'dark squares', len(dark), 48)
rec('2b10', 'max dominoes', mm, min(len(dark), len(light)))
assert len(light) == 50 and mm < 49

# ---------- mental-2 ----------
rec('2m01', 'key', 86 * 44, 65 ** 2 - 21 ** 2)
rec('2m01', 'forty-only', 86 * 40, 3440); rec('2m01', 'zero', 86 * 440, 37840)
rec('2m02', 'key', F(3150, 14), F(1575, 7))
rec('2m02', 'tenth', F(315, 14), 22.5); rec('2m02', 'tenfold', F(31500, 14), 2250)
rec('2m03', 'key', F(150) / F(5, 4), 150 * F(4, 5))
rec('2m03', 'took-off', 150 * F(3, 4), 112.5); rec('2m03', 'minus-25', 150 - 25, 125)
# 2m04 rate 4% to 6% (choice)
rec('2m04', 'points', 6 - 4, 2); rec('2m04', 'percent', F(6 - 4, 4) * 100, 50)
rec('2m04', 'new-base', F(2, 6) * 100, 33.333333, 1e-5)
# 2m05 gaps (choice)
g1, g2 = F(3, 4) - F(5, 7), F(4, 5) - F(7, 9)
rec('2m05', 'gap A', g1, F(3 * 7 - 5 * 4, 28)); rec('2m05', 'gap B', g2, F(4 * 9 - 7 * 5, 45))
rec('2m05', 'tops-bottoms slip', F(7 - 4, 9 - 5), F(3, 4))
assert g1 > g2 > 0
# 2m06 31.2 x 19.8 (choice)
rec('2m06', 'key', F(312, 10) * F(198, 10), F(2550, 100) ** 2 - F(570, 100) ** 2)
rec('2m06', 'added', 624 + F(624, 100), 630.24); rec('2m06', 'wrong-piece', 624 - 4, 620)
rec('2m06', 'double-gap', 624 - F(312, 10) * F(4, 10), 611.52)
# 2m07 3, 4, 7, 12, 19 -> 28
seq = [3, 4, 7, 12, 19]
rec('2m07', 'key', seq[-1] + (seq[-1] - seq[-2]) + 2, 5 ** 2 + 3)
rec('2m07', 'same-step', 19 + 7, 26); rec('2m07', 'fib', 12 + 19, 31); rec('2m07', 'plus-eight', 19 + 8, 27)
# 2m08 4, 6, 9, 13.5 -> 20.25
rec('2m08', 'key', F(27, 2) * F(3, 2), 4 * F(3, 2) ** 4)
rec('2m08', 'add-gap', F(27, 2) + F(9, 2), 18); rec('2m08', 'double', 27, F(27, 2) * 2)
# 2m09 24% a year, 256 days -> daily vol 1.5%
rec('2m09', 'key', 0.24 / sqrt(256), 0.24 / 16)
rec('2m09', 'no-root', 0.24 / 256, 0.0009375); rec('2m09', 'calendar', 0.24 / sqrt(365), 0.012562, 1e-6)
rec('2m09', 'times', 0.24 * 16, 3.84)
# 2m10 50 in 6 minutes; 42 s left, costs 6, 22, 9, 15, 7 (choice)
costs = [6, 22, 9, 15, 7]
bestset = max((c for r in range(6) for c in combinations(range(5), r) if sum(costs[i] for i in c) <= 42), key=lambda c: (len(c), -sum(costs[i] for i in c)))
rec('2m10', 'pace', F(360, 50), 7.2)
rec('2m10', 'answered', len(bestset), 4); rec('2m10', 'seconds used', sum(costs[i] for i in bestset), 37)
assert [costs[i] for i in range(5) if i not in bestset] == [22]
assert sum(1 for r in [4] for c in combinations(range(5), r) if sum(costs[i] for i in c) <= 42) == 1
inorder = 0; tleft = 42
for c in costs:
    if c <= tleft: tleft -= c; inorder += 1
    else: break
rec('2m10', 'in order count', inorder, 3)
rec('2m10', 'per-minute slip', F(50, 6), 8.333333, 1e-5)

# ---------- market-making-2 ----------
# 2k01 three cards, first shows a heart: expected hearts
cards = ['H'] * 12 + ['X'] * 39
ex = F(sum((a == 'H') + (b == 'H') for a, b in combinations(cards, 2)), comb(51, 2))
rec('2k01', 'key', 1 + ex, 1 + 2 * F(12, 51))
rec('2k01', 'old-deck', 1 + 2 * F(1, 4), F(3, 2)); rec('2k01', 'no-update', 3 * F(13, 52), F(3, 4))
rec('2k01', 'add-one', 1 + 3 * F(1, 4), F(7, 4))
# 2k02 digit 1 in 1..200
rec('2k02', 'key', sum(str(i).count('1') for i in range(1, 201)), 20 + 100 + 20)
rec('2k02', 'no-hundreds', 20 + 20, sum(str(i)[-2:].count('1') for i in range(1, 201)))
rec('2k02', 'hundreds-only', 100, sum(1 for i in range(100, 200)))
rec('2k02', 'from-100', 120, sum(str(i).count('1') for i in range(100, 200)))
# 2k03 London black cabs (choice): 9 million people x 12 trips a year / (20 trips a day x 300 days)
rec('2k03', 'estimate', 9e6 * 12 / (20 * 300), 18000)
assert abs(log(18000, 10) - 4) < abs(log(18000, 10) - 5)
# 2k05 A 20-22, B 30-33, A+B 56-59
legs = {'buy A, buy B, sell A+B': 56 - (22 + 33), 'sell A, sell B, buy A+B': (20 + 30) - 59}
rec('2k05', 'key', max(legs.values()), 1)
rec('2k05', 'offers', 59 - (22 + 33), 4); rec('2k05', 'mids', F(56 + 59, 2) - (F(42, 2) + F(63, 2)), 5)
rec('2k05', 'bids', 56 - (20 + 30), 6)
# 2k06 larger of two d6 minus 3, quote 0.4 wide: the offer
fair = F(sum(max(a, b) - 3 for a in range(1, 7) for b in range(1, 7)), 36)
rec('2k06', 'key', fair + F(2, 10), F(161, 36) - 3 + F(1, 5))
rec('2k06', 'fair', fair, F(53, 36)); rec('2k06', 'one-die', F(7, 2) - 3 + F(1, 5), 0.7)
rec('2k06', 'full-width', fair + F(4, 10), F(53, 36) + 0.4); rec('2k06', 'no-minus', F(161, 36) + F(1, 5), 4.672222, 1e-6)
# 2k07 one card, ace 1, number cards face value, J/Q/K count 10; call struck at 6
vals = [min(r, 10) for r in range(1, 14)]
call = F(sum(max(v - 6, 0) for v in vals), 13); put = F(sum(max(6 - v, 0) for v in vals), 13)
rec('2k07', 'key', call, put + F(sum(vals), 13) - 6)  # put-call parity
rec('2k07', 'key direct', call, F(1 + 2 + 3 + 4 * 4, 13))
rec('2k07', 'intrinsic', F(sum(vals), 13) - 6, F(7, 13))
rec('2k07', 'court-ranks', F(sum(max(r - 6, 0) for r in range(1, 14)), 13), F(28, 13))
rec('2k07', 'put', put, F(15, 13))

# ---------- behavioural: model word counts are checked in gen.py ----------
for line in OUT: print(line)
print(f'all {len(OUT)} checks passed')
```

### `hg.py`

```python
import heapq, itertools
def solve(a,b,target,maxt=60):
    # state: (t, topA, topB) top sand amounts; a glass runs when top>0
    caps=(a,b)
    start=(0,0,0)
    # at decision time we may flip any subset (nonempty at t=0)
    best={}
    pq=[(0,0,(0,0),())]
    res=None
    while pq:
        fl,t,tops,plan=heapq.heappop(pq)
        key=(t,tops)
        if key in best and best[key]<=fl: continue
        best[key]=fl
        for sub in [(),(0,),(1,),(0,1)]:
            if t==0 and not sub: continue
            nt=list(tops); 
            for g in sub: nt[g]=caps[g]-nt[g]
            nf=fl+len(sub)
            run=[x for x in nt if x>0]
            if not run: continue
            dt=min(run); T=t+dt
            if T>maxt: continue
            nt2=tuple(max(0,x-dt) if x>0 else 0 for x in nt)
            np_=plan+((t,sub),)
            if T==target:
                if res is None or nf<res[0]: res=(nf,np_)
            heapq.heappush(pq,(nf,T,nt2,np_))
    return res
if __name__=='__main__':
    for a,b in [(3,5),(4,7),(5,7),(5,8),(3,8),(4,9),(7,11),(5,9),(6,11),(4,11),(5,11)]:
        out=[]
        for T in range(1,30):
            r=solve(a,b,T)
            if r and T not in (a,b): out.append((T,r[0]))
        print(a,b,out)
```

### Its output

```text
2p01  key                                    3.916667  check     3.916667
2p01  d6-only                                3.500000  check     3.500000
2p01  two-d6                                 4.472222  check     4.472222
2p01  mean-of-means                          3.000000  check     3.000000
2p02  n=10 value                            38.500000  check    38.500000
2p03  key                                    5.620000  check     5.620000
2p03  twelve-gaps                            6.040000  check     6.040000
2p03  no-first                               4.620000  check     4.620000
2p03  fair-coin                              6.500000  check     6.500000
2p04  key                                    7.541667  check     7.541667
2p04  key sim                                7.541667  check     7.539420
2p04  no-reroll                              6.500000  check     6.500000
2p04  free-reroll                            8.000000  check     8.000000
2p04  keep-seven                             7.500000  check     7.500000
2p05  key                                    1.500000  check     1.500000
2p05  key closed                             1.500000  check     1.500000
2p05  turn-all                               1.000000  check     1.000000
2p05  tie-zero                               1.100000  check     1.100000
2p05  stop-when-ahead equals turn-all        1.000000  check     1.000000
2p06  key                                    5.333333  check     5.333333
2p06  key sim                                5.333333  check     5.342880
2p06  pairs                                  2.666667  check     2.666667
2p06  one-pair                               2.000000  check     2.000000
2p07  key                                   99.800000  check    99.800000
2p07  unbiased sim N=120                   120.000000  check   119.946140
2p07  max-only                              84.000000  check    84.000000
2p07  no-minus-one                         100.800000  check   100.800000
2p07  k-minus-one                          104.000000  check   104.000000
2p08  key                                    0.181818  check     0.181818
2p08  other-die                              0.166667  check     0.166667
2p08  unconditional                          0.111111  check     0.111111
2p08  one-order                              0.090909  check     0.090909
2p09  key                                    0.517241  check     0.517241
2p09  key sim                                0.517241  check     0.514980
2p09  first-shot                             0.300000  check     0.300000
2p09  share                                  0.428571  check     0.428571
2p09  b-chance                               0.482759  check     0.482759
2p10  key                                    0.109375  check     0.109677
2p10  one-start                              0.015625  check     0.015625
2p10  n-over-2n                              0.054688  check     0.054688
2p11  key                                    3.657328  check     3.657328
2p11  key sim                                3.657328  check     3.660930
2p11  key t=1 check                          2.718282  check     2.718282
2p11  scaled-e                               4.077423  check     4.077423
2p11  corner-all-n                           4.481689  check     4.481689
2p11  divide-by-mean                         3.000000  check     3.000000
2p12  key                                    0.510000  check     0.509983
2p12  key grid                               0.510000  check     0.510350
2p12  linear                                 0.300000  check     0.300000
2p12  double                                 0.600000  check     0.600000
2p12  complement                             0.490000  check     0.490000
2p13  key take                               1.000000  check     1.000000
2p14  key                                    4.800000  check     4.800000
2p14  key sim                                4.800000  check     4.794525
2p14  red-aces                               5.200000  check     5.200000
2p14  all-cards                              9.600000  check     9.600000
2p14  four-gaps                              6.000000  check     6.000000
2p15  key                                    0.342857  check     0.342857
2p15  no-reinforce                           0.432000  check     0.432000
2p15  one-order                              0.114286  check     0.114286
2p15  at-least-two                           0.628571  check     0.628571
2p15  no-replacement                         0.600000  check     0.600000
2b01  key                                    4.000000  check     4.000000
2b01  plan replay end                       11.000000  check    11.000000
2b01  starts-free                            2.000000  check     2.000000
2b01  one-start                              3.000000  check     3.000000
2b02  key round                              3.000000  check     3.000000
2b02  unmarked know                          4.000000  check     4.000000
2b02  two marks check                        2.000000  check     2.000000
2b03  key                                    3.000000  check     3.000000
2b04  key                                   16.000000  check    16.000000
2b04  pairs                                  6.000000  check     6.000000
2b04  all                                   20.000000  check    20.000000
2b04  no-plus-one                           15.000000  check    15.000000
2b05  key                                    0.309347  check     0.309700
2b05  key vs 1-ln2                           0.309347  check     0.306853
2b05  fail                                   0.690653  check     0.690653
2b06  key                                    3.000000  check     3.000000
2b06  r1                                     7.000000  check     7.000000
2b06  r2                                     9.000000  check     9.000000
2b06  r0                                     1.000000  check     1.000000
2b07  key                                   19.000000  check    19.000000
2b07  doubling                              12.000000  check    12.000000
2b07  simple                                33.000000  check    33.000000
2b07  quadruple                             24.000000  check    24.000000
2b08  key                                   42.000000  check    42.000000
2b08  mean                                  50.000000  check    50.000000
2b08  one-way                               21.000000  check    21.000000
2b09  key                                    3.428571  check     3.428571
2b09  average                                7.000000  check     7.000000
2b09  all-three                              2.666667  check     2.666667
2b09  sum                                   14.000000  check    14.000000
2b10  dark squares                          48.000000  check    48.000000
2b10  max dominoes                          48.000000  check    48.000000
2m01  key                                 3784.000000  check  3784.000000
2m01  forty-only                          3440.000000  check  3440.000000
2m01  zero                               37840.000000  check 37840.000000
2m02  key                                  225.000000  check   225.000000
2m02  tenth                                 22.500000  check    22.500000
2m02  tenfold                             2250.000000  check  2250.000000
2m03  key                                  120.000000  check   120.000000
2m03  took-off                             112.500000  check   112.500000
2m03  minus-25                             125.000000  check   125.000000
2m04  points                                 2.000000  check     2.000000
2m04  percent                               50.000000  check    50.000000
2m04  new-base                              33.333333  check    33.333333
2m05  gap A                                  0.035714  check     0.035714
2m05  gap B                                  0.022222  check     0.022222
2m05  tops-bottoms slip                      0.750000  check     0.750000
2m06  key                                  617.760000  check   617.760000
2m06  added                                630.240000  check   630.240000
2m06  wrong-piece                          620.000000  check   620.000000
2m06  double-gap                           611.520000  check   611.520000
2m07  key                                   28.000000  check    28.000000
2m07  same-step                             26.000000  check    26.000000
2m07  fib                                   31.000000  check    31.000000
2m07  plus-eight                            27.000000  check    27.000000
2m08  key                                   20.250000  check    20.250000
2m08  add-gap                               18.000000  check    18.000000
2m08  double                                27.000000  check    27.000000
2m09  key                                    0.015000  check     0.015000
2m09  no-root                                0.000937  check     0.000937
2m09  calendar                               0.012562  check     0.012562
2m09  times                                  3.840000  check     3.840000
2m10  pace                                   7.200000  check     7.200000
2m10  answered                               4.000000  check     4.000000
2m10  seconds used                          37.000000  check    37.000000
2m10  in order count                         3.000000  check     3.000000
2m10  per-minute slip                        8.333333  check     8.333333
2k01  key                                    1.470588  check     1.470588
2k01  old-deck                               1.500000  check     1.500000
2k01  no-update                              0.750000  check     0.750000
2k01  add-one                                1.750000  check     1.750000
2k02  key                                  140.000000  check   140.000000
2k02  no-hundreds                           40.000000  check    40.000000
2k02  hundreds-only                        100.000000  check   100.000000
2k02  from-100                             120.000000  check   120.000000
2k03  estimate                           18000.000000  check 18000.000000
2k05  key                                    1.000000  check     1.000000
2k05  offers                                 4.000000  check     4.000000
2k05  mids                                   5.000000  check     5.000000
2k05  bids                                   6.000000  check     6.000000
2k06  key                                    1.672222  check     1.672222
2k06  fair                                   1.472222  check     1.472222
2k06  one-die                                0.700000  check     0.700000
2k06  full-width                             1.872222  check     1.872222
2k06  no-minus                               4.672222  check     4.672222
2k07  key                                    1.692308  check     1.692308
2k07  key direct                             1.692308  check     1.692308
2k07  intrinsic                              0.538462  check     0.538462
2k07  court-ranks                            2.153846  check     2.153846
2k07  put                                    1.153846  check     1.153846
all 152 checks passed
```

### Final run of `play-bank.mjs`

```text
locked before 86, after 48; drawable 325; session-2 items drawable 50 of 50
pass 0 (right): 50 of 50 distinct items played and accepted, in 7 decks
pass 1 (wrong #1): 43 wrong answers routed, 50 items dealt
pass 2 (wrong #2): 43 wrong answers routed, 50 items dealt
pass 3 (wrong #3): 34 wrong answers routed, 50 items dealt
pass 4 (wrong #4): 2 wrong answers routed, 50 items dealt
wrong ids and distractors in the files: 122; routed: 122
choice items seen with more than one option order: 14 of 14
no console errors
ALL OK
```

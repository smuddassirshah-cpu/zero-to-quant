# Topic 3.3 exam: interview preparation

File: `app/content/exams/topic-3.3.json` (id `topic-3.3`, 75 minutes, pass 0.7, 30 items, the validator cap).
Generator and checks: `scratchpad/exam-3.3/` (`gen1.py`, `gen2.py` and `gen.py` build the file; `check.py` recomputes every number; `tradesim*.cjs` and `tradelog.cjs` play the trade game through the engine's own pure module).

## Brief (written before the items)

### Trade games in a topic exam

`docs/AUTHORING.md` section 3 puts the `trade` widget on "a problem, ladder or transfer screen (or a set or exam item)". `tools/validate.mjs` refuses only generated items in topic exams (`generators: false`); it checks a `trade` exam item like any other and replays its `strategy`. `mock-trade-sample.json` already plays one on an exam screen. So one trade game sits in this exam. `carry` cannot be read in an exam, so every other market-making item uses fixed numbers (DECISIONS "Trading games (3 Nov)").

### Skill coverage by level

A level counts as covered when an item tests a skill first met in it (DECISIONS "Exam coverage (3 Nov)"). Skills first met were read from the lesson files.

| Course | Level | Skills first met | Items testing them |
|---|---|---|---|
| puzzles | 1 Expected value | pz-expectation, pz-recursion, pz-symmetry | 7, 15, 21, 22, 26, 30 |
| puzzles | 2 Conditioning | pz-conditioning | 12 |
| puzzles | 3 Continuous and geometric | pz-geometry | 28 |
| puzzles | 4 Games and betting | pz-games | 18, 21 |
| puzzles | 5 Puzzles firms keep asking | none (shared) | 26 tests l25 (fair bit from a biased coin) through pz-expectation and pz-symmetry |
| mental-pressure | 1 Speed | mp-speed, mp-formats | 1, 8, 13 |
| mental-pressure | 2 Fractions and estimates | mp-fractions, mp-estimate | 4, 19, 23 |
| mental-pressure | 3 Test formats | none (shared) | 13 tests l10 (next in the sequence) through mp-formats |
| mental-pressure | 4 Assessment batteries | none (shared) | 8 tests l13 (negative marking) and 23 tests l14 (ranking likelihoods) through mp-formats, mp-estimate, mp-fractions |
| mm-games | 1 Fair value | mg-fair, mg-quote | 2, 5, 24, 29, 30 |
| mm-games | 2 Quoting | mg-update, mg-risk | 11, 16, 29, 30 |
| mm-games | 3 Risk | none (shared) | 29, the trade game (position limit, updating, informed flow), and 16 (skew) through mg-risk |
| mm-games | 4 Trading games firms run | none (shared) | 24 tests l17 (options on a game, parity) through mg-quote and mg-fair |
| brainteasers | 1 Invariants and counting | bz-invariant, bz-search | 10, 6 |
| brainteasers | 2 Strategy and logic | bz-strategy | 17 |
| brainteasers | 3 Quick reasoning | bz-quick | 3 |
| game-theory | 1 Games in a table | gm-normal, gm-mixed | 9, 14 |
| game-theory | 2 Sequential games and auctions | gm-sequential, gm-auction | 25, 20 |
| game-theory | 3 Poker and decisions | gm-poker | 27 |

Levels covered only through shared skills: puzzles L5, mental-pressure L3 and L4, mm-games L3 and L4. Each has at least one item built on one of its own lessons, named above.

All 23 skills of the five courses are in the `skills` map and each is tested: pz-expectation 5, mg-quote 4, mg-update 4, mg-fair 3, mg-risk 3, pz-recursion 2, pz-symmetry 2, pz-games 2, mp-fractions 2, mp-formats 2, mp-estimate 2, and one each for the other twelve.

### Item plan

Ramp: 6 at difficulty 2 (20%), 15 at 3 (50%), 6 at 4 (20%), 3 at 5 (10%). Easy items first, courses interleaved. Widgets: 23 numeric (each `wrong` value with a `byKey` line), 2 choice (`shuffle: true`), 1 tap-regions on a table, 1 order, 1 trade on an orderbook, 1 longform with a 10-point rubric. No firm names. Every item has `tags` (its family) and `pace`.

| # | id | d | skills | widget | key |
|---|---|---|---|---|---|
| 1 | e-mult-58-64 | 2 | mp-speed | numeric | 3712 |
| 2 | e-six-counts-zero | 2 | mg-fair | numeric | £7.50 |
| 3 | e-clock-824 | 2 | bz-quick | numeric | 108° |
| 4 | e-three-moves | 2 | mp-fractions | numeric (%) | −12.6% |
| 5 | e-edge-lift | 2 | mg-quote | numeric | £5.10 |
| 6 | e-two-hundred-coins | 2 | bz-search | numeric | 5 |
| 7 | e-even-faces | 3 | pz-expectation | numeric | 11 |
| 8 | e-guess-or-blank | 3 | mp-formats | numeric | 0.0625 |
| 9 | e-nash-cell | 3 | gm-normal | tap-regions on a 3 by 3 table | (Middle, Centre) |
| 10 | e-stones | 3 | bz-invariant | choice | white |
| 11 | e-ten-cards | 3 | mg-update | numeric | 19.22 |
| 12 | e-three-coins | 3 | pz-conditioning | numeric | 16/29 = 0.5517 |
| 13 | e-next-term | 3 | mp-formats | numeric | 56 |
| 14 | e-mix-share | 3 | gm-mixed | numeric, table canvas | 3/7 = 0.4286 |
| 15 | e-cube-walk | 3 | pz-recursion, pz-expectation | numeric | 10 |
| 16 | e-skew-short | 3 | mg-risk, mg-update | choice | £49 at £51 |
| 17 | e-last-one-loses | 3 | bz-strategy | numeric | 2 |
| 18 | e-kelly-three-two | 3 | pz-games | numeric | 1/6 = 0.1667 |
| 19 | e-root-1900 | 3 | mp-estimate | numeric | 43.59 |
| 20 | e-curse-six | 3 | gm-auction | numeric | £8.57 |
| 21 | e-die-then-coin | 3 | pz-games, pz-recursion | numeric | 0.5 |
| 22 | e-next-in-line | 4 | pz-symmetry, pz-expectation | numeric | 0.9 |
| 23 | e-rank-five | 4 | mp-estimate, mp-fractions | order | a, b, c, e, d |
| 24 | e-twelve-put | 4 | mg-quote, mg-fair | numeric | 25/12 = 2.0833 |
| 25 | e-bonus-split | 4 | gm-sequential | numeric | £60 |
| 26 | e-biased-bits | 4 | pz-expectation, pz-symmetry | numeric | 4.76 |
| 27 | e-bluff-catcher | 4 | gm-poker | numeric | £8.33 |
| 28 | e-late-window | 5 | pz-geometry | numeric | 7/36 = 0.1944 |
| 29 | e-four-dice-desk | 5 | mg-risk, mg-quote, mg-update | trade on orderbook | P&L at least £4, no breaks |
| 30 | e-roll-to-six | 5 | mg-fair, mg-quote, mg-update, mg-risk, pz-expectation | longform, 10 points | fair £6, then £10 |

### Freshness against the courses and mocks

Every item was checked against a dump of all titles, prose and questions in the five courses and the mock files (`existing.txt`) and by targeted greps. Planned items dropped or changed because a course or mock already had them: HTH waiting (puzzles l3), 6 then 1 waiting (puzzles review-1 has 6 then 5), the 10 and 20 minute meeting (puzzles l16), Kelly at 2 to 1 and 3 to 1 (puzzles l21, game-theory l15), the square of a die (puzzles l1, mm-games l16), take 1 to 5 (puzzles l19 and l24), 3:40 on a clock (brainteasers l12), distinct faces in three rolls (mm-games homework-1), four bidders on £0 to £100 (game-theory review-2), the 7-put (mm-games l17), +25% then −20% (mental-pressure l6) and 73 × 67 (mental-pressure l2). What remains uses our own numbers and set-ups: windows offset by half an hour with unequal waits, a misère take-away, a 12-put on three dice by parity, a four-round shrinking pool with absolute cuts, six bidders with ±£12 errors, and so on. The trade game's opening (four dice, fair £14) matches the setting of mm-games l6, but its quote, cards, limit and informed client are new.

## Numbers computed twice (`check.py`)

Each answer and each `wrong` value was computed exactly (Fraction or closed form) and again by brute force, enumeration or a 200,000-run simulation:

- Even faces 11 (coupon sum; simulation 11.002). Cube walk 10, with $E_2 = 9$ and $E_1 = 7$ (linear solve; simulation 9.97).
- Next in line 0.9 ($(n-1)/n$ checked by enumerating all $7!$ rows; simulation 0.899 for $n = 10$).
- Three coins 16/29 = 0.5517 (Bayes; simulation 0.5518); one-toss slip 4/9, ratio slip 16/25.
- Two windows 7/36 = 0.1944 (exact piecewise-linear integration; simulation 0.1952); same window 0.2986, swapped waits 0.1389, both 15 minutes 0.25.
- Kelly 1/6 (formula; numerical maximum of the growth rate 0.16667). Die then coin 1/2 (round equation; simulation 0.5015).
- Biased bits 4.762 (formula $1/(pq)$; simulation 4.769); pairs 2.381.
- 58 × 64 = 3712 two ways; guessing EV 0.0625 and 0 for a blind guess from five; sequence 56 from the square gaps; −12.6% two ways; $\sqrt{1900} = 43.589$ against the hand estimate 43.593 (the tolerance 0.01 holds both).
- Ranking: 0.5177, 0.4902, 0.3125, 0.3077, 0.2778, each by formula and by full enumeration of rolls, tosses or card pairs.
- Sixes count zero £7.50 (linearity; enumeration of 216 rolls). Edge £5.10 and its slips. Ten cards 19.22 (formula; enumeration of the 72 ordered pairs). Skew centre £50.
- 12-call 7/12 and 12-put 25/12 on three dice (enumeration of 216 rolls; parity $P = C + 1.5$).
- Stones: 20,000 random plays all end white. 200 coins: $\lceil \log_3 200 \rceil = 5$ two ways. Misère take-away: brute-force game search gives take 2 (losing piles 1, 6, 11, ..., 36). Clock 108° two ways.
- Nash: best-reply search gives the unique pure equilibrium (Middle, Centre). Mixed share 3/7 (formula; grid search 0.4286), Column's share 2/7, value 1/7.
- Bonus pool £60 (backward induction; the alternating sum 100 − 70 + 40 − 10).
- Winner's curse £8.571 ($12 \times 5/7$; simulation 8.574). Bluff-catcher EV £8.33 two ways, pot odds 28.6%.
- Longform: geometric mean 6 and sd $\sqrt{30} \approx 5.48$ by series sums; median 4; fair after four misses 10 (memoryless; conditional simulation 9.99); short 3 at £7 marks at −£9.

### The trade game (item 29)

Four dice, fair £14, settling at £17 (6, 5, 4, then 2). Cards: turn 3 the first two dice show 6 and 5 (fair £18); turn 6 the third shows 4 (fair £18.50) and an informed client takes over. Noise trader turns 1 to 5 (rate 0.8, `reach` 1), informed turns 6 to 8 (edge 0.5). Limit 4, size 1 to 2, spread £1 to £4, opening quote £12.50 at £15.50, benchmark £4, no breaks, seed 7. The seed was chosen by playing eight strategies over seeds 1 to 80 in the engine's pure module (`tradesim3.cjs`):

| run (seed 7) | P&L | breaks | result |
|---|---|---|---|
| model `strategy`: centred on each fair, width 2, size 1 | £10 | 0 | pass |
| skewed £0.50 a lot, size 1 | £6.50 | 0 | pass |
| skewed, size up to 2 inside the limit | £6.50 | 0 | pass |
| width 1, size 1 | £5 | 0 | pass |
| centred, always size 2 | £12 | 3 (limit) | fail |
| stale quote £13 at £15 throughout | −£6 | 1 | fail |
| width 4, any centre | £0 | 0 | fail (noise trader stays out) |
| opening quote left untouched | −£6 | 2 | fail (no validator warning) |

The model run's log (`tradelog.cjs`): bought 1 at £13 on turn 1, sold 1 at £19 on each of turns 3 to 5, no trades with the informed client, short 2, P&L $44 - 2 \times 17 = \text{£}10$, which the explanation states. The validator's own replay and `ZQ.trade.play` agree (P&L 10, 0 breaks).

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors and 0 warnings for `topic-3.3.json`; the manifest now lists it. At the last run the whole tree showed 4 errors, all in `mm-games/l8-informed-flow.json` and `mm-games/l10-position-limits.json`, files another agent was editing in parallel; none in this file.
- `playthrough.mjs --exam topic-3.3 --local-cdn <pkgs>`: 30 items, scored 30 of 30, passed. Again with `--mobile --shots`: passed.
- Screenshots (`scratchpad/exam-3.3/shots`) reviewed at 390 px and desktop. Fixes made from them: the order book's levels moved off the opening quote, because a book level at the learner's price drew two rows at one price; money placeholders changed from "an amount in £" to "an amount", because the £ unit already shows in front. The 3 by 3 payoff table, the 2 by 2 game, the five-line ranking, the trade ledger and the longform prompt all fit at 390 px.
- Voice scan (`VOICE_BASE=<scratch>/voice/`): 0 sentences over 20 words, 0 explanations over three sentences, 638 sentences scanned. No exclamation marks, em-dashes or firm names.

## prep.json

`content/prep.json` lists no topic exams: its steps name courses or course levels, and its `mocks` lists name mock exams only. Nothing to add. If paths later gain topic exams, topic-3.3 belongs at the end of the 3.3 steps in `general`, `interview-trader` and `superday-trader`.

## course.json

No change proposed.

## Backlog

Two bullets under "Raised later (exam topic-3.3):" in `docs/BACKLOG-INBOX.md`.

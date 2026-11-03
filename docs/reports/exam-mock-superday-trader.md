# Report: mock exam `mock-superday-trader`

Brief: `docs/briefs/mocks.md`, section `## mock-superday-trader` (binding), with the shared rules at the top. Author: content agent, 3 Nov 2026.

## Files

- `app/content/exams/mock-superday-trader.json` (new, written by `gen_superday.py`). One file, no versions, as the brief says.
- `docs/BACKLOG-INBOX.md`: 5 bullets under `Raised later (mock-superday-trader):`.
- This report.
- Scratch (not in the repo): `/tmp/claude-0/-home-user-zero-to-quant/7da692d4-a4e3-50a3-8a6e-3e8b2ccfe9ff/scratchpad/superday/` holds `gen_superday.py`, `play.js` (replays trade specs through `app/js/engine/widgets/trade.js`), `shots.mjs` (full-page screenshots of every screen after each answer), `gen_output.txt` and the screenshot folders `shots/`, `shots3/`, `shots4/`.

`content/prep.json` already lists `mock-superday-trader` (paths at lines 263, 364, 393, 418, 440 and 462); the id matches the file. No `prep.json` change proposed. No `course.json` change.

## Shape

| # | Part | Minutes | Items | Pass | Navigation | `pace` sum |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | paper `probability`, Probability and expected value | 45 | 6 (4 choice, 2 longform) | `pass: 0.65` (4 of 6) | free | 2,520 s |
| 2 | paper `mental`, Mental maths and Fermi | 15 | 12 (8 numeric, 4 interval choice) | `pass: 0.7` (9 of 12) | forward, `skip: false` | 800 s |
| 3 | paper `market`, Market-making game | 30 | 4 (3 trade, 1 longform) | `pass: 0.75` (3 of 4) | free | 1,800 s |
| 4 | paper `fit`, Fit and motivation | 18 | 2 longform | `pass: 0.5` (1 of 2) | free | 960 s |
| 5 | check `game-aloud` | | | ticked | | |
| 6 | check `why-aloud` | | | ticked | | |

24 items, 108 minutes, 5 longform. Every paper scores `right 1, wrong 0, blank 0`. The script asserts the counts, minutes, pace sums and that `ceil(pass x n)` gives 4, 9, 3 and 1.

**By difficulty:** 2: 4 items, 3: 12, 4: 7, 5: 1. Exactly: d2 = b1, b4, b6, b8; d3 = a1, a2, b2, b3, b5, b7, b9, b11, b12, c1, d1, d2; d4 = a3, a4, a6, b10, c2, c3, c4; d5 = a5. (Mocks have no difficulty ramp.)

**By family (first tag):** `coupon-collector`, `fixed-points`, `kelly`, `fair-from-biased`, `card-stopping`, `pot-odds`, `percent-of`, `difference-of-squares`, `two-by-two`, `fraction-sum`, `compound`, `gauss-sum`, `last-digit`, `net-percent`, `fermi-interval` (4 items, second tags `stack-of-coins`, `balls-in-a-room`, `heartbeats`, `quote-rate`), `three-dice`, `bad-news`, `interviewer-flow`, `market-defence`, `why-trading`, `decision-under-uncertainty`.

**Skills:** all 13 of the brief's map are used by at least one item (asserted): `pz-expectation` (a1, a4, a5), `pz-conditioning` (a2), `pz-games` (a3, a5), `gm-poker` (a6), `mp-speed` (b2, b3, b5, b6, b7), `mp-fractions` (b1, b4, b8), `mp-estimate` (b9 to b12), `bz-quick` (b6, b7, as a second skill), `mg-fair` (c1), `mg-quote` (c3, c4), `mg-update` (c1, c2), `mg-risk` (c2, c3, c4), `rk-behave` (c4, d1, d2).

## Results

- Validator, from `app/`: `node tools/validate.mjs 2>&1 | tail -5` gives `0 errors, 393 warnings`, none of them on this file. (One mid-session run showed 4 errors in `mm-games/l8-informed-flow.json` and `l10-position-limits.json`, files another agent was editing at the time; they had gone on the next run.)
- Playthrough, from `app/`: `node tools/playthrough.mjs --exam mock-superday-trader --local-cdn <pkgs>`: `ok mock-superday-trader 24 items, scored 24 of 24, passed`; `ok (mock checks) seed, clock at zero, attempts kept`; `All passed.` Again with `--mobile --shots <scratch>/shots`: the same, all passed. The forward-only probe ran on paper 2 (no jump ahead, no step back, no move on unanswered) and raised nothing.
- The playthrough passes the three trade items by their `strategy` and marks the five longform items with every rubric point ticked, at 1280 and at 390 px.
- Voice: `VOICE_BASE=<scratch>/voice/ python3 docs/reviews/voice-scan.py` on a copy of the file: `explanations over three sentences: 0`, `sentences scanned: 527; over 20 words: 0`. No exclamation marks (the one `!` is $3!$ inside KaTeX), no em-dashes, £ throughout. Model answers are 108 to 138 words (a5 137, a6 108, c4 138, d1 135, d2 137), under the brief's 150.
- "Pass mark NaN%": not shown. The results page reads "6 of 6 correct, 100%. Pass mark 65%." and so on for all four papers, and a scripted check of the page text found no `NaN`. The known bug is on `passNet` papers only; these papers use `pass`. So no NaN bullet was raised.

## Screenshots looked at

Viewport shots from the playthrough (`shots/`) and full-page shots of every screen before and after each answer (`shots3/`, `shots4/`, made by `shots.mjs` with a tall viewport so the inner scroll shows). Checked: the start card at 1280 and 390 (four papers with 45, 15, 30 and 18 minutes, the two checks, "108 minutes in 4 papers", "24 questions", "Pass every part" listing 65%, 70%, 75% and 50%); each choice item (options fit in the two-column grid at 390); each numeric item; the four Fermi items; each trade item before and after the game at 390 (book, "You" row on top, the four ledger tiles two by two, the three steppers with 44 px buttons and Send quote, the cards and the results table, nothing overlapping); each longform before and after marking at 390 (model answer, rubric, 10 of 10); the check page; the results page.

Fault found and fixed: in the first build the order book's resting levels sat at the learner's own prices (£102 shown twice, once as "You"), as the topic-3.3 bullet describes. The book now starts half a tick outside the opening quote on each side. Faults left to the engine (inbox bullets): the start card's part cards squeeze their text into a narrow column at 390 px (seen on `mock-oa-trader` too), and the book's `depth: 3` counts the "You" row.

## Deviations from the brief, with reasons

1. `models` reworded from the brief's one 25-word sentence to two sentences (175 characters): "Reported, as of Nov 2026: trading-firm final rounds at Jane Street, Optiver, SIG, IMC and Citadel Securities. Probability, mental maths, market-making games and fit questions." The voice scan counts `models` and required 0 sentences over 20 words.
2. Q1 three-dice card on turn 3: the brief has "The first die shows 6. Fair is now 13.5." (`fair: 13.5`). After a 6 the fair total is $6 + 3.5 + 3.5 = 13$, so the card reads "Fair is now 13." with `fair: 13` (asserted by enumeration of the two dice left). The turn 6 card, $6 + 4 + 3.5 = 13.5$, is as the brief. The mark does not enter the counterparty's choices (no `reach`), so the played P&L is unchanged.
3. Q1 strategy, turns 3 to 5: `[11.5, 14.5, 1]` in place of the brief's `[12, 15, 1]` and `[12.5, 14.5, 1]`, so the quote is centred on the corrected fair of 13. Replayed: the same fills (no trade on 3, a noise buyer lifts £14.50 on 4) and the same P&L, £9.50. Turns 6 to 8 stay `[12.5, 14.5, 1]`, centred on 13.5.
4. Q2 (hats), distractor $\tfrac14$: the brief's reason "one named person only" does not give $\tfrac14$ for "nobody gets their own hat". The option is kept, with the real slip behind it: counting only the single four-cycles, $3! = 6$ of 24, and missing the 3 double swaps (asserted by enumeration: 6 four-cycles, 3 double swaps).
5. Q3 (Kelly), distractor 10% replaced by 40%: options 10% and 100% are a times-ten pair with the key 20% between them, which "Distractors (4 Nov)" forbids. 40% is the Kelly formula $p - q/b$ with even money misread as odds of 2 to 1 ($0.6 - 0.4/2$). The options 20%, 40%, 60%, 100% pass every option rule.
6. Q5 (card stopping), follow-up: the brief's "stake anything from £0 to £1 on every card ... the stakes £0 then £1 give £1" holds only if the stake may go on either colour; betting on red only, one red and one black is worth $\tfrac12$ (both asserted: `W(1,1) = 1` either colour, `W(1,1, red only) = 1/2`). The prompt therefore says "on either colour".
7. Q6 (pot odds), follow-up: phrased from the caller's side ("your hand beats only a bluff; how often must the £50 bet be a bluff for your call to break even?"), which is exactly the brief's sum $150x - 50(1 - x) = 0$.
8. Q4 debrief (c4) model: the brief says "a second fill at £97.5 would leave +4 and break the limit". With the quoted size of 1, a fill leaves +3; +4 is what selling 2 would do. The model says both: 2 more would be +4, over the limit, and even 1 more leaves +3, at the limit, where any bid breaks it (asserted from the replay: position +2 after turn 1, limit 3).
9. Inbox heading: `Raised later (mock-superday-trader):`, as the orchestrator asked (the brief has `Raised later (exam mock-superday-trader):`).
10. Fermi why lines: the two misses name a slip where one exists (asserted: 2.5 mm read as 3 mm; a ball rounded to 6 cm gives 283 thousand, in 250 to 300; a cube of 6.5 cm gives 116.5 thousand, in 100 to 150; 1,500 minutes a day gives 3.07 billion, in 3.0 to 3.2; 60 beats a minute gives 2.52 billion, in 2.4 to 2.6). Q12's misses have no clean slip, so they say which step to check.
11. The brief's "recorded" spoken answers (plan E10) are replaced, as the brief says, by the description's "say each written answer aloud before you type it", the "Say your answer aloud first" line on every longform prompt, and the two checks.

## Items, keys and their two computations

All values are `Fraction`s in the script; each line below is an `assert` there.

| Item | Key | Method 1 | Method 2 | Distractors or `wrong` values (slip) |
| --- | --- | --- | --- | --- |
| a1 coupon-collector | $\tfrac{147}{10} = 14.7$ rolls | $6(1 + \tfrac12 + \dots + \tfrac16)$ | stage waits $1 + \tfrac65 + \tfrac64 + \tfrac63 + \tfrac62 + 6$; a backward Markov solve on faces seen | 36 ($6 \times 6$); 2.45 ($H_6 = \tfrac{49}{20}$, no factor 6); 8.7 (five faces, $14.7 - 6$) |
| a2 fixed-points | $\tfrac38$ | inclusion-exclusion $1 - 1 + \tfrac12 - \tfrac16 + \tfrac1{24}$ | enumeration: 9 of 24 permutations | $\tfrac58$ (complement); $\tfrac{81}{256}$ ($(\tfrac34)^4$); $\tfrac14$ (four-cycles only, 6 of 24) |
| a3 kelly | 20% | $p - q = 0.2$ | linear solve $0.6(1-f) = 0.4(1+f)$; float grid in 1% steps peaks at 20%, growth 0.0201 | 60% ($p$); 100% (max EV); 40% ($p - q/2$) |
| a4 fair-from-biased | $\tfrac{100}{21} \approx 4.76$ tosses | $2 / (2 \times 0.3 \times 0.7)$ | toss-level solve $S = 2 + 0.58S$; series $\sum 2n\,s(1-s)^{n-1}$ | 2.38 (pairs); 3.33 ($1/0.3$); 1.43 ($1/0.7$) |
| a5 card-stopping (longform) | £0; with free stakes on either colour, one red and one black gives £1 | recursion $V(r,b) = \max(\tfrac{r-b}{r+b}, \text{wait})$: $V(26,26) = V(3,3) = V(1,1) = 0$, $V(2,1) = \tfrac13$ | martingale identity at every state to (26, 26); brute force over all 128 stopping rules on (2, 2), all 0, and 8 on (2, 1), best $\tfrac13$; free stakes $W(1,1) = 1$ (either colour), $\tfrac12$ (red only) | rubric |
| a6 pot-odds (longform) | call, EV +£10; bluffs $\tfrac14$ | break-even $\tfrac{50}{200} = 25\%$; $0.3 \times 150 - 0.7 \times 50 = 10$ | $0.3 \times 200 - 50 = 10$; $150x - 50(1-x) = 0$ at $x = \tfrac14$ | rubric |
| b1 percent-of | 98.8 (tol 0.05) | $76 + 22.8$ | $0.13 \times 760 = \tfrac{494}{5}$ | 9.88 (point); 76 (10% only) |
| b2 difference-of-squares | 2491 | $50^2 - 3^2$ | $47 \times 53$ | 2500 (no $-9$); 2209 ($47^2$) |
| b3 two-by-two | 988 | $38 \times 25 + 38$ | $40 \times 26 - 2 \times 26$ | 1040 (rounded 38 to 40); 948 (digit) |
| b4 fraction-sum | $\tfrac{5}{24} \approx 0.208$ (tol 0.0005) | $\tfrac{3}{24} + \tfrac{2}{24}$ | $0.125 + 0.0833$ | 0.1 ($\tfrac{2}{20}$); 0.0104 ($\tfrac{1}{96}$) |
| b5 compound | 2.01 (exact 2.0122, tol 0.03) | squaring: 1.1236, 1.2625, 1.5938, then $\times 1.2625$ | binomial sum $\sum \binom{12}{k} 0.06^k$; rule of 72 gives about 2 | 1.72 ($1 + 12 \times 0.06$) |
| b6 gauss-sum | 7260 | $\tfrac{120 \times 121}{2}$ | 60 pairs of 121; direct sum | 7140 (to 119); 14520 (no halving) |
| b7 last-digit | 9 | cycle 7, 9, 3, 1 and $2026 \bmod 4 = 2$ | `pow(7, 2026, 10)` | 3 (one step on); 7 (remainder read as 1) |
| b8 net-percent | +5% (answer 0.05, unit %) | $1.4 \times 0.75 = 1.05$ | from 100: 140, then 105 | 15% (added); 10% (40% of 25%) |
| b9 stack-of-coins | 2.5 km; key 2.0 to 3.0 | $10^6 \times 2.5$ mm | 1,000 coins is 2.5 m, times 1,000 | wide 1.0 to 4.0; adjacent 3.0 to 4.0; far 0.0 to 1.0 |
| b10 balls-in-a-room | about 222.5 thousand; key 200 to 250 | $\tfrac{0.64 \times 50}{\tfrac43\pi(0.0325)^3}$ in m | the same in cm, $\tfrac{0.64 \times 5 \times 10^7}{(\pi/6)\,6.5^3}$; $\pi$ bounded by 3.14159 and 3.14160, both in 222 to 223 | wide 100 to 400; adjacent 250 to 300 (6 cm ball: 283); far 100 to 150 (cube: 116.5) |
| b11 heartbeats | 2.945 billion; key 2.8 to 3.0 | $70 \times 60 \times 24 \times 365.25 \times 80$ | 36,817,200 a year, times 80 | wide 2.0 to 4.0; adjacent 3.0 to 3.2 (1,500 minutes a day: 3.07); far 2.4 to 2.6 (60 a minute: 2.52) |
| b12 quote-rate | 187.2 thousand; key 180 to 190 | $4 \times 2 \times 6.5 \times 3600$ | 28,800 an hour, times 6.5 | wide 100 to 300; adjacent 190 to 200; far 160 to 170 |
| c1 three-dice | P&L £9.50 against £8 | `trade.js` `play`: bought 2 at £9 (turn 2, noise), sold 1 at £14.50 (turn 4, noise), held 1 | cash $-18 + 14.5 = -3.5$, plus $1 \times 13$; fairs $3 \times 3.5$, $6 + 3.5 + 3.5 = 13$, $6 + 4 + 3.5 = 13.5$ by enumeration | idle quote: £1, limit breaks on turns 7 and 8 (informed buyers took the £12 ask until short 5) |
| c2 bad-news | P&L £19.50 against £12 | `play`: bought 1 at £48.50, sold 2 at £51.50 on turns 2 and 3, short 3 | cash 157.5, minus $3 \times 46$ | idle quote: £2, limit breaks on turns 4, 7 and 8 (informed sellers hit £48.50 until long 4) |
| c3 interviewer-flow | P&L £7 against £6 | `play`: bought 2 at £98, sold 1 at £102 and 1 at £101, flat | cash $-196 + 102 + 101 = 7$ | idle quote: £14 but limit breaks on turns 2, 3 and 4, so it fails on the rules |
| c4 market-defence (longform) | quote £96.50 to £100.50 for 1 | replay: position +2 after turn 1; limit 3, so 2 more is +4 and 1 more is +3 | $96.5 < 97.5$; $100.5 > 100$; width $4 \in [2, 6]$ | rubric |
| d1 why-trading, d2 decision-under-uncertainty (longform) | example answers, labelled as such | | | rubric (10 each, from the brief) |

**Option rules** (asserted on every choice): exactly one correct, `shuffle: true`, a `why` on every distractor; for every pair of distractors either side of the key, no times-ten pair, no equal additive slips and no equal ratio slips. On the Fermi items the rule runs on interval midpoints (b9: 0.5, 2.5, 3.5; b10: 125, 225, 250, 275; b11: 2.5, 2.9, 3.0, 3.1; b12: 165, 185, 195, 200), and the script also asserts: the key holds the value and is the tightest that does; the wide interval holds it and is wider; both misses have the key's width and miss it; one miss shares an end with the key and the other is a full width away, on opposite sides. Numeric `wrong` values are each asserted outside the key's `tol` (the times-ten rule does not apply to them, DECISIONS "Numeric distractors").

**No duplicates.** The script reads all of `mock-oa-trader.json`, `-2`, `-3`, `mock-oa-sig.json`, `-2`, `-3`: 171 authored items with 46 tags. It asserts that no tag here (family or second tag) is any tag there or in the brief's list of taken families, that no question text and no question-plus-key pair repeats, and that every question here is under 0.8 similar (difflib) to every question there. Output: "duplicate check: 24 items against 171 items in 6 files; 46 tags taken; none repeated".

## The three trade games (as written and played)

Shared: `tick 0.5`, `currency £`, `dp 1`, `maxBreaks 0`, an `orderbook` canvas (three resting levels a side starting half a tick outside the opening quote, `showMid: true`, `state: {}`).

- **c1 three-dice**: seed 23, 8 turns, fair 10.5, value 13, range 3 to 18, size 1 to 2 (start 1), limit 5, spread 1 to 4, opening quote 9 / 12 for 2; noise rate 0.8 on turns 1 to 4, informed edge 0.5 on turns 5 to 8; cards on turns 1 (rule), 3 (first die 6, fair 13), 6 (second die 4, fair 13.5), 8 (third die 3, total 13, reveal); benchmark 8. Strategy `[9,12,2] [9,12,2] [11.5,14.5,1] x3 [12.5,14.5,1] x3`. Played £9.50, 0 breaks; idle £1, 2 breaks.
- **c2 bad-news**: seed 31, 8 turns, fair 50, value 46, range 38 to 58, size 1 to 3, limit 4, spread 1 to 5, opening 48.5 / 51.5 for 2; noise rate 0.7 on turns 1 to 3, informed edge 0.5 on 4 to 8; cards on 1, 4 (fair 48), 7 (reveal £46); benchmark 12. Strategy as the brief. Played £19.50, 0 breaks; idle £2, 3 breaks.
- **c3 interviewer-flow**: seed 41, 6 turns, fair 100, value 104, range 92 to 112, size 1 to 2, limit 3, spread 2 to 6, opening 98 / 102 for 2; scripted: hit 2 at 98, hit 2 at 97.5, hit 2 at 97, lift 2 at 102, lift 2 at 101, none; cards on 1, 4 (fair 102), 6 (reveal £104); benchmark 6. Strategy as the brief. Played £7, 0 breaks; idle £14 with 3 limit breaks.

`gen_superday.py` replays each through `play.js` (which calls `play(widget, strategy)` and `play(widget, null)` from `app/js/engine/widgets/trade.js`) and asserts the strategy verdict `ok` with 0 breaks and the stated P&L, the idle verdict not `ok`, a margin of at least £1 over the benchmark, and the P&L again from the fills (cash plus position at the value). The validator replays the strategies too and warns about none of them.

## Prerequisites (cited; nothing is gated)

puzzles `l2-every-coupon`, `l5-hats`, `l20-betting-on-sequences`, `l21-kelly`, `l24-mixed-set`, `l25-fair-from-biased`; game-theory `l11-pot-odds`; mental-pressure `l1-towards-fifty`, `l2-two-by-two`, `l7-estimating-products`; brainteasers `l13-digits-and-remainders`, `l14-sums-in-one-line`; mm-games `l2-dice-sum`, `l4-fermi`, `l7-skewing`, `l8-informed-flow`, `l10-position-limits`, `l12-thinking-aloud`, `l13-full-game`; recruiting `l8-why-this-firm`, `l11-stories-that-answer`, `l12-reasoning-aloud`, `l13-the-final-round`.

## Proposals

- `prep.json`: no change; the entry exists and its id matches.
- `course.json`: none.
- Inbox (5 bullets, `Raised later (mock-superday-trader):`): the E3 bank draw for this mock; a trade item scored by P&L; longform marks all or nothing at 7 of 10; the start card's part cards at 390 px; `orderbook` `depth` counting the "You" row. No NaN bullet: the pass marks print correctly on these `pass` papers.

## Script output

```
models length 175
duplicate check: 24 items against 171 items in 6 files; 46 tags taken; none repeated
wrote /home/user/zero-to-quant/app/content/exams/mock-superday-trader.json
item | key | method 1 | method 2
a1-coupon-collector | 147/10 = 14.7 | 6(1 + 1/2 + ... + 1/6) | stage waits 1 + 6/5 + ... + 6; Markov solve on faces seen
a2-fixed-points | 3/8 | inclusion-exclusion 1 - 1 + 1/2 - 1/6 + 1/24 = 9/24 | enumeration: 9 of 24 permutations have no fixed point
a3-kelly | 20% | f = p - q = 0.6 - 0.4 | linear solve 0.6(1 - f) = 0.4(1 + f); grid in 1% steps peaks at 20%, growth 0.0201
a4-fair-from-biased | 100/21 = 4.76 | 2 / (2 x 0.3 x 0.7) = 2 / 0.42 | toss-level linear solve S = 2 + 0.58 S; series of 2n s (1-s)^(n-1)
a5-card-stopping | £0 (single bet); £1 with free stakes on one red and one black | recursion V(r,b) = max(stop, wait): V(26,26) = V(3,3) = 0, V(2,1) = 1/3 | martingale identity at every state; brute force over all 128 stopping rules on (2,2) (all worth 0) and 8 on (2,1) (best 1/3)
a6-pot-odds | call, EV +£10; bluffs 1/4 of bets | break-even 50/200 = 25%; EV 0.3 x 150 - 0.7 x 50 = 10 | EV 0.3 x 200 - 50 = 10; solve 150x - 50(1 - x) = 0 gives x = 1/4
b1-percent-of | 98.8 | 76 + 22.8 | 0.13 x 760 = 494/5
b2-difference-of-squares | 2491 | 50^2 - 3^2 | direct product 47 x 53
b3-two-by-two | 988 | 38 x 25 + 38 | 40 x 26 - 2 x 26
b4-fraction-sum | 5/24 = 0.208 | 3/24 + 2/24 | 0.125 + 0.0833
b5-compound | 2.0122 (2.01) | squaring: 1.1236, 1.2625, 1.5938, then x 1.2625 | binomial sum of C(12,k) 0.06^k; rule of 72 gives about 2
b6-gauss-sum | 7260 | 120 x 121 / 2 | 60 pairs of 121; direct sum
b7-last-digit | 9 | cycle 7, 9, 3, 1 and 2026 mod 4 = 2 | pow(7, 2026, 10)
b8-net-percent | +5% | 1.4 x 0.75 = 1.05 | from 100: 140, then 105
b9-stack-of-coins | 2.5 km: key 2.0 to 3.0 | 10^6 x 2.5 mm = 2,500 m | 1,000 coins is 2.5 m, times 1,000
b10-balls-in-a-room | 222.5 thousand: key 200 to 250 | 0.64 x 50 / ((4/3) pi 0.0325^3) | 0.64 x 5e7 cm^3 / ((pi/6) 6.5^3 cm^3), pi bounded either side
b11-heartbeats | 2.945 billion: key 2.8 to 3.0 | 70 x 60 x 24 x 365.25 x 80 | 36.8 million a year, times 80
b12-quote-rate | 187.2 thousand: key 180 to 190 | 4 x 2 x 6.5 x 3600 | 28,800 an hour, times 6.5
c1-three-dice | P&L £9.50 (benchmark £8) | trade.js play: bought 2 at £9, sold 1 at £14.50, settled 1 at £13 | cash -18 + 14.5 + 13 = 9.5; idle quote £1 with 2 limit breaks
c2-bad-news | P&L £19.50 (benchmark £12) | trade.js play: bought 1 at £48.50, sold 2 at £51.50 twice, short 3 into £46 | cash 157.5 - 3 x 46 = 19.5; idle quote £2 with 3 limit breaks
c3-interviewer-flow | P&L £7 (benchmark £6) | trade.js play: bought 2 at £98, sold 1 at £102 and 1 at £101 | cash -196 + 102 + 101 = 7; idle quote £14 with 3 limit breaks
c1-three-dice strategy {'ok': True, 'key': None, 'pnl': 9.5, 'breaks': 0} idle {'ok': False, 'key': 'limit', 'pnl': 1, 'breaks': 2} ['7:limit', '8:limit']
c2-bad-news strategy {'ok': True, 'key': None, 'pnl': 19.5, 'breaks': 0} idle {'ok': False, 'key': 'limit', 'pnl': 2, 'breaks': 3} ['4:limit', '7:limit', '8:limit']
c3-interviewer-flow strategy {'ok': True, 'key': None, 'pnl': 7, 'breaks': 0} idle {'ok': False, 'key': 'limit', 'pnl': 14, 'breaks': 3} ['2:limit', '3:limit', '4:limit']
```

## The script, `gen_superday.py`

```python
"""gen_superday.py: writes app/content/exams/mock-superday-trader.json.
Every number is a Fraction and is asserted two ways. The three trade games are replayed through
app/js/engine/widgets/trade.js (play.js beside this file). The duplicate check reads every
mock-oa-trader*.json and mock-oa-sig*.json. random.Random(2601) sets option order only."""
import json, glob, itertools, math, os, random, subprocess, difflib, re
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/zero-to-quant'
EXAMS = f'{REPO}/app/content/exams'
OUT = f'{EXAMS}/mock-superday-trader.json'
rng = random.Random(2601)
KEYS = []  # (item id, key, method 1, method 2) for the report table

def key(item_id, value, m1, m2):
    KEYS.append((item_id, value, m1, m2))

def dec(x, dp):
    return float(round(F(x), dp)) if dp is not None else float(x)

# ---------------------------------------------------------------- option rules
def option_rules(item_id, key_value, distractor_values):
    """No times-ten pair, no equal additive slips and no equal ratio slips with the key between them."""
    lo = [v for v in distractor_values if v < key_value]
    hi = [v for v in distractor_values if v > key_value]
    for a in lo:
        for b in hi:
            assert b != 10 * a, (item_id, 'times-ten pair around the key', a, b)
            assert b - key_value != key_value - a, (item_id, 'equal slips around the key', a, b)
            if a > 0:
                assert b * a != key_value * key_value, (item_id, 'equal ratio slips around the key', a, b)
    assert len(set(distractor_values)) == len(distractor_values) and key_value not in distractor_values, item_id

def choice(options):
    """options: list of dicts (text, correct or why). Shuffled by the seeded rng, ids a to d."""
    opts = options[:]
    rng.shuffle(opts)
    out = []
    for i, o in enumerate(opts):
        e = {'id': 'abcdef'[i], 'text': o['text']}
        if o.get('correct'):
            e['correct'] = True
        else:
            e['why'] = o['why']
        out.append(e)
    assert sum(1 for o in out if o.get('correct')) == 1
    return {'kind': 'choice', 'layout': 'grid', 'shuffle': True, 'label': 'Answer options', 'options': out}

# ================================================================ Paper 1
p1 = []

# Q1 coupon collector
H6 = sum(F(1, k) for k in range(1, 7))
q1a = 6 * H6
q1b = sum(F(6, 6 - k) for k in range(6))           # stage waits 1, 6/5, ..., 6
E = F(0)                                              # Markov solve on faces seen: E_k = 6/(6-k) + E_{k+1}
for k in range(5, -1, -1):
    # E_k = 1 + (k/6) E_k + ((6-k)/6) E_{k+1}  =>  E_k = (1 + ((6-k)/6) E_{k+1}) / (1 - k/6)
    E = (1 + F(6 - k, 6) * E) / (1 - F(k, 6))
q1c = E
assert q1a == q1b == q1c == F(147, 10)
d36, dH, d87 = F(36), H6, q1a - 6
assert dH == F(49, 20) and d87 == F(87, 10)
option_rules('a1', q1a, [d36, dH, d87])
key('a1-coupon-collector', '147/10 = 14.7', '6(1 + 1/2 + ... + 1/6)', 'stage waits 1 + 6/5 + ... + 6; Markov solve on faces seen')
p1.append({
    'id': 'a1-coupon-collector', 'difficulty': 3, 'skills': ['pz-expectation'], 'tags': ['coupon-collector'], 'pace': 300,
    'title': 'Every face once',
    'question': 'A fair die is rolled until every face from 1 to 6 has appeared. What is the expected number of rolls?',
    'widget': choice([
        {'text': '$14.7$', 'correct': True},
        {'text': '$36$', 'why': 'You waited 6 rolls for every face, as if each were the last one left. Early faces come much faster.'},
        {'text': '$2.45$', 'why': 'You added $1 + \\tfrac12 + \\dots + \\tfrac16$ but left out the factor of 6.'},
        {'text': '$8.7$', 'why': 'You stopped once five faces had appeared. The sixth face alone takes 6 rolls on average.'},
    ]),
    'feedback': {'correct': 'Add the waits for each new face, $1 + \\tfrac65 + \\tfrac64 + \\tfrac63 + \\tfrac62 + 6$.',
                 'generic': 'Split the wait into stages: the first new face, then the second, and so on.'},
    'explain': {'text': 'With $k$ faces seen, a new face comes with chance $\\tfrac{6-k}{6}$, so that stage takes $\\tfrac{6}{6-k}$ rolls on average. '
                        'The six stages add to $6\\left(1 + \\tfrac12 + \\tfrac13 + \\tfrac14 + \\tfrac15 + \\tfrac16\\right) = 14.7$. '
                        'A step-by-step solve on the number of faces seen gives the same.'},
})

# Q2 four hats, no fixed point
q2a = sum(F((-1) ** k, math.factorial(k)) for k in range(5))
perms = list(itertools.permutations(range(4)))
der = [p for p in perms if all(p[i] != i for i in range(4))]
q2b = F(len(der), len(perms))
assert q2a == q2b == F(3, 8) and len(der) == 9
cycles4 = [p for p in der if all(p[p[i]] != i for i in range(4))]
assert len(cycles4) == 6                               # one four-cycle: 3! = 6; the other 3 are double swaps
d_some, d_ind, d_cyc = 1 - q2a, F(3, 4) ** 4, F(len(cycles4), 24)
assert d_some == F(5, 8) and d_ind == F(81, 256) and d_cyc == F(1, 4)
option_rules('a2', q2a, [d_some, d_ind, d_cyc])
key('a2-fixed-points', '3/8', 'inclusion-exclusion 1 - 1 + 1/2 - 1/6 + 1/24 = 9/24', 'enumeration: 9 of 24 permutations have no fixed point')
p1.append({
    'id': 'a2-fixed-points', 'difficulty': 3, 'skills': ['pz-conditioning'], 'tags': ['fixed-points'], 'pace': 300,
    'title': 'Nobody gets their own hat',
    'question': 'Four people leave their hats at a cloakroom. The hats are handed back in a random order. What is the chance that nobody gets their own hat?',
    'widget': choice([
        {'text': '$\\dfrac{3}{8}$', 'correct': True},
        {'text': '$\\dfrac{5}{8}$', 'why': 'You found the chance that somebody gets their own hat. The question asks for nobody.'},
        {'text': '$\\dfrac{81}{256}$', 'why': 'You treated each person as missing their hat independently, $(\\tfrac34)^4$. The hats are not independent.'},
        {'text': '$\\dfrac{1}{4}$', 'why': 'You counted only the orders where the hats go round in one cycle, $3! = 6$ of 24. The 3 double swaps count too.'},
    ]),
    'feedback': {'correct': '9 of the 24 orders give nobody their own hat.',
                 'generic': 'List the 24 orders, or use inclusion-exclusion on the people who get their own hat.'},
    'explain': {'text': 'By inclusion-exclusion the chance is $1 - 1 + \\tfrac12 - \\tfrac16 + \\tfrac1{24} = \\tfrac{9}{24} = \\tfrac38$. '
                        'Listing the 24 orders finds 9 with no fixed point: 6 four-cycles and 3 double swaps.'},
})

# Q3 Kelly
p, q = F(3, 5), F(2, 5)
q3a = p - q                                           # closed form for even money
q3b = (p - q) / (p + q)                               # root of p/(1+f) = q/(1-f): p(1-f) = q(1+f)
grid = [(i, 0.6 * math.log(1 + i / 100) + 0.4 * math.log(1 - i / 100)) for i in range(0, 100)]
best = max(grid, key=lambda t: t[1])
assert q3a == q3b == F(1, 5) and best[0] == 20 and abs(best[1] - 0.0201) < 0.00005
d_p, d_all, d_b2 = p, F(1), p - q / 2                  # stake the win chance; all in; odds read as 2 to 1
assert d_b2 == F(2, 5)
option_rules('a3', q3a, [d_p, d_all, d_b2])
key('a3-kelly', '20%', 'f = p - q = 0.6 - 0.4', 'linear solve 0.6(1 - f) = 0.4(1 + f); grid in 1% steps peaks at 20%, growth 0.0201')
p1.append({
    'id': 'a3-kelly', 'difficulty': 4, 'skills': ['pz-games'], 'tags': ['kelly'], 'pace': 360,
    'title': 'How much to stake',
    'prose': 'You may stake any share of your bankroll on an even-money bet. You win it with chance 0.6. The bet repeats many times.',
    'question': 'What share of your bankroll should you stake each time to maximise its long-run growth?',
    'widget': choice([
        {'text': '20%', 'correct': True},
        {'text': '60%', 'why': 'You staked the chance of winning. The stake depends on the edge, the win chance less the loss chance.'},
        {'text': '100%', 'why': 'You maximised the expected value of one bet. One loss at 100% ends the game, so long-run growth is lost.'},
        {'text': '40%', 'why': 'You read even money as odds of 2 to 1, from the £2 returned. Even money pays 1 to 1.'},
    ]),
    'feedback': {'correct': 'For an even-money bet the stake is $p - q = 0.6 - 0.4$.',
                 'generic': 'Maximise the expected log of your bankroll after one bet.'},
    'explain': {'text': 'The log growth $0.6\\ln(1+f) + 0.4\\ln(1-f)$ peaks where $0.6(1-f) = 0.4(1+f)$, so $f = 0.2$. '
                        'A grid in 1% steps also peaks at 20%, with growth of about 0.0201 a bet. '
                        'Staking everything maximises the mean, but one loss ends the game.'},
})

# Q4 fair from biased
ph = F(3, 10); pt = 1 - ph
s = 2 * ph * pt
q4a = 2 / s
# toss-level solve: S = 1 + ph*H + pt*T, H = 1 + ph*S, T = 1 + pt*S  =>  S = 2 + (ph^2 + pt^2) S
q4b = 2 / (1 - ph * ph - pt * pt)
# series: sum over pairs n >= 1 of 2n * s (1-s)^(n-1), partial sums converge to 100/21
part = sum(2 * n * s * (1 - s) ** (n - 1) for n in range(1, 200))
assert q4a == q4b == F(100, 21) and abs(float(part) - 100 / 21) < 1e-9
d_pairs, d_head, d_tail = q4a / 2, 1 / ph, 1 / pt
for v, t in [(q4a, 4.76), (d_pairs, 2.38), (d_head, 3.33), (d_tail, 1.43)]:
    assert round(float(v), 2) == t
option_rules('a4', q4a, [d_pairs, d_head, d_tail])
key('a4-fair-from-biased', '100/21 = 4.76', '2 / (2 x 0.3 x 0.7) = 2 / 0.42', 'toss-level linear solve S = 2 + 0.58 S; series of 2n s (1-s)^(n-1)')
p1.append({
    'id': 'a4-fair-from-biased', 'difficulty': 4, 'skills': ['pz-expectation'], 'tags': ['fair-from-biased'], 'pace': 360,
    'title': 'A fair call from a biased coin',
    'prose': 'A coin lands heads with chance 0.3. To make a fair call, you toss it in pairs. You stop at the first pair that is HT or TH.',
    'question': 'What is the expected number of tosses?',
    'widget': choice([
        {'text': '$4.76$', 'correct': True},
        {'text': '$2.38$', 'why': 'You counted pairs, not tosses. Each pair is two tosses.'},
        {'text': '$3.33$', 'why': 'You waited for the first head, $1/0.3$. A head alone does not end the game.'},
        {'text': '$1.43$', 'why': 'You waited for the first tail, $1/0.7$. The pair must hold one of each.'},
    ]),
    'feedback': {'correct': 'A pair ends it with chance $0.42$, so $\\tfrac{2}{0.42}$ tosses.',
                 'generic': 'Find the chance that one pair ends the game.'},
    'explain': {'text': 'A pair is HT or TH with chance $2 \\times 0.3 \\times 0.7 = 0.42$. '
                        'So the pairs average $\\tfrac{1}{0.42}$, and the tosses $\\tfrac{2}{0.42} = \\tfrac{100}{21} \\approx 4.76$. '
                        'Solving $E = 2 + 0.58E$ gives the same.'},
})

# Q5 red card stopping
from functools import lru_cache

@lru_cache(None)
def V(r, b):
    """Best value of 'bet £1 on red now, or wait', with a forced bet on the last card."""
    n = r + b
    now = F(r - b, n)
    if n == 1:
        return now
    wait = (F(r, n) * V(r - 1, b) if r else 0) + (F(b, n) * V(r, b - 1) if b else 0)
    return max(now, wait)

assert V(26, 26) == 0 and V(3, 3) == 0 and V(2, 1) == F(1, 3) and V(1, 1) == 0
# martingale check: the stop value equals the expected stop value one card later, at every state
for r in range(0, 27):
    for b in range(0, 27):
        n = r + b
        if n < 2:
            continue
        nxt = (F(r, n) * F(r - 1 - b, n - 1) if r else 0) + (F(b, n) * F(r - b + 1, n - 1) if b else 0)
        assert nxt == F(r - b, n), (r, b)

def brute(r0, b0):
    """Every stopping rule on a small deck, by enumeration of decision points (prefixes)."""
    orders = set(itertools.permutations('R' * r0 + 'B' * b0))
    prefixes = sorted({o[:k] for o in orders for k in range(r0 + b0 - 1)})   # free choices before every card but the last
    vals = []
    for mask in range(1 << len(prefixes)):
        stop = {prefixes[i] for i in range(len(prefixes)) if mask >> i & 1}
        tot = F(0)
        for o in orders:
            k = next((k for k in range(r0 + b0 - 1) if o[:k] in stop), r0 + b0 - 1)
            tot += 1 if o[k] == 'R' else -1
        vals.append(tot / len(orders))
    return min(vals), max(vals), len(prefixes)

lo22, hi22, n22 = brute(2, 2)
lo21, hi21, n21 = brute(2, 1)
assert lo22 == hi22 == 0 and n22 == 7
assert hi21 == F(1, 3) and n21 == 3
# follow-up: free stake 0 to 1 on either colour on each card: the best is |r - b| / (r + b) each card
@lru_cache(None)
def W(r, b, either=True):
    n = r + b
    if n == 0:
        return F(0)
    edge = F(abs(r - b), n) if either else max(F(r - b, n), F(0))
    return edge + (F(r, n) * W(r - 1, b, either) if r else 0) + (F(b, n) * W(r, b - 1, either) if b else 0)
assert W(1, 1) == 1 and W(1, 1, False) == F(1, 2) and W(26, 26) > 0
key('a5-card-stopping', '£0 (single bet); £1 with free stakes on one red and one black', 'recursion V(r,b) = max(stop, wait): V(26,26) = V(3,3) = 0, V(2,1) = 1/3', 'martingale identity at every state; brute force over all 128 stopping rules on (2,2) (all worth 0) and 8 on (2,1) (best 1/3)')
p1.append({
    'id': 'a5-card-stopping', 'difficulty': 5, 'skills': ['pz-games', 'pz-expectation'], 'tags': ['card-stopping'], 'pace': 600,
    'title': 'When to bet on red',
    'kind': 'longform',
    'prompt': 'Say your answer aloud first, then type it.\n\n'
              'A deck of 26 red and 26 black cards is shuffled. The cards are turned over one at a time. '
              'At any moment you may stop and bet £1 that the next card is red. '
              'You win £1 if it is red and lose £1 if it is black. You must bet by the last card.\n\n'
              '(a) What is the bet worth with your best play, and how should you play?\n\n'
              '(b) The interviewer follows up. Now you may stake from £0 to £1 on either colour, on every card. What changes?',
    'model': '**(a)** The question is whether any stopping rule beats betting at once. '
             'With $r$ red and $b$ black cards left, the next card is red with chance $\\tfrac{r}{r+b}$. '
             'So stopping now is worth $\\tfrac{r-b}{r+b}$ pounds. '
             'This is a fair game: one card later, its expected value is unchanged. '
             'So every stopping rule has expected gain £0. '
             'Check one red and one black card. Betting now gains 0. '
             'Waiting, the last card is red half the time, so 0 again. '
             'So the bet is worth £0, and how I play does not matter.\n\n'
             '**(b)** With free stakes I can win. '
             'I stake £0 while the colours are level, and back the leading colour otherwise. '
             'With one red and one black card, I stake £0 on the first, then £1 on the colour left. '
             'That gains £1 for sure.',
    'rubric': [
        {'points': 1, 'text': 'States that the question is whether any stopping time helps'},
        {'points': 1, 'text': 'The next card is red with chance equal to the red share of the cards left'},
        {'points': 2, 'text': 'Gives the value of stopping now as the red-minus-black share, $\\tfrac{r-b}{r+b}$'},
        {'points': 3, 'text': 'Argues that this is a fair game, so every stopping rule has expected gain 0'},
        {'points': 1, 'text': 'Checks a small deck by listing the cases'},
        {'points': 1, 'text': 'Answers £0 for the single bet'},
        {'points': 1, 'text': 'Says free stakes win, with the one-red, one-black example worth £1'},
    ],
})

# Q6 pot odds
pot, bet, eq = F(100), F(50), F(3, 10)
win = pot + bet
q6be_a = bet / (bet + win)                            # price over the final pot

q6be_b = bet / (win + bet)
q6ev_a = eq * win - (1 - eq) * bet
q6ev_b = eq * (pot + 2 * bet) - bet
bluff = bet / (win + bet)                             # x*150 - (1-x)*50 = 0
assert q6be_a == q6be_b == F(1, 4) and q6ev_a == q6ev_b == 10 and bluff * win - (1 - bluff) * bet == 0 and bluff == F(1, 4)
key('a6-pot-odds', 'call, EV +£10; bluffs 1/4 of bets', 'break-even 50/200 = 25%; EV 0.3 x 150 - 0.7 x 50 = 10', 'EV 0.3 x 200 - 50 = 10; solve 150x - 50(1 - x) = 0 gives x = 1/4')
p1.append({
    'id': 'a6-pot-odds', 'difficulty': 4, 'skills': ['gm-poker'], 'tags': ['pot-odds'], 'pace': 600,
    'title': 'Call or fold',
    'kind': 'longform',
    'prompt': 'Say your answer aloud first, then type it.\n\n'
              'You are heads-up and the pot holds £100. Your opponent bets £50. '
              'You think you win 30% of the time if you call.\n\n'
              '(a) Do you call or fold? Show the numbers.\n\n'
              '(b) The interviewer follows up. Say your hand beats only a bluff. '
              'How often must the £50 bet be a bluff for your call to break even?',
    'model': '**(a)** Calling costs £50. If I win, I collect £150: the pot of £100 and their £50. '
             'So I need to win $\\tfrac{50}{50 + 150} = 25\\%$ of the time to break even. '
             'At 30% the call is worth $0.3 \\times 150 - 0.7 \\times 50 = +£10$. '
             'Check: $0.3 \\times 200 - 50 = 10$. So I call. '
             'The 30% is my estimate, so I would test it against their range and how they have bet. '
             'A tighter player would push it down, and below 25% I fold.\n\n'
             '**(b)** If a share $x$ of their bets are bluffs, calling gains $150x - 50(1 - x)$. '
             'That is 0 at $x = \\tfrac14$. '
             'So the bet must be a bluff a quarter of the time, the same 25% as the pot odds.',
    'rubric': [
        {'points': 2, 'text': 'States the price of the call, £50, and what it wins, £150'},
        {'points': 2, 'text': 'Break-even equity of 25% by a stated formula'},
        {'points': 2, 'text': 'EV of +£10 and the decision to call'},
        {'points': 1, 'text': 'Says the 30% is an estimate and what would change it'},
        {'points': 2, 'text': 'Bluff share of $\\tfrac14$, with a reason'},
        {'points': 1, 'text': 'Reasons aloud in order and ends with a clear action'},
    ],
})

# ================================================================ Paper 2
p2 = []

def numeric(answer, tol, wrongs, unit='', placeholder='a number', accept=None, label='Your answer'):
    for w in wrongs:
        assert abs(w['value'] - answer) > tol + w['tol']['abs'], ('wrong value inside the key tolerance', w)
    wd = {'kind': 'numeric', 'answer': answer, 'tol': {'abs': tol}, 'placeholder': placeholder, 'label': label,
          'wrong': wrongs}
    if unit:
        wd['unit'] = unit
    if accept:
        wd['accept'] = accept
    return wd

def mental(i, tag, title, question, wd, correct, generic, by_key, explain, diff, skills):
    p2.append({'id': f'b{i}-{tag}', 'difficulty': diff, 'skills': skills, 'tags': [tag], 'pace': 40, 'title': title,
               'question': question, 'widget': wd,
               'feedback': {'correct': correct, 'generic': generic, 'byKey': by_key}, 'explain': {'text': explain}})

# B1 13% of 760
b1a = F(76) + F(228, 10)
b1b = F(13, 100) * 760
assert b1a == b1b == F(494, 5)
key('b1-percent-of', '98.8', '76 + 22.8', '0.13 x 760 = 494/5')
mental(1, 'percent-of', 'A percentage of a number', 'What is 13% of 760?',
       numeric(98.8, 0.05, [{'id': 'moved-point', 'value': 9.88, 'tol': {'abs': 0.005}},
                            {'id': 'ten-only', 'value': 76.0, 'tol': {'abs': 0.005}}], accept='98.8 (within 0.05)'),
       '10% is 76 and 3% is 22.8.', 'Split 13% into 10% and 3%.',
       {'moved-point': 'You moved the decimal point one place too far. 13% of 760 is near 100, not 10.',
        'ten-only': 'You took 10% only. Add the 3%, which is 22.8.'},
       '10% of 760 is 76, and 3% is $3 \\times 7.6 = 22.8$. So 13% is $76 + 22.8 = 98.8$. Check: $0.13 \\times 760 = 98.8$.',
       2, ['mp-fractions'])

# B2 47 x 53
b2a = 50 ** 2 - 3 ** 2
b2b = 47 * 53
assert b2a == b2b == 2491
key('b2-difference-of-squares', '2491', '50^2 - 3^2', 'direct product 47 x 53')
mental(2, 'difference-of-squares', 'Either side of 50', 'Work out $47 \\times 53$.',
       numeric(2491, 0, [{'id': 'no-nine', 'value': 2500, 'tol': {'abs': 0}},
                         {'id': 'squared', 'value': 2209, 'tol': {'abs': 0}}], accept='Exactly 2491'),
       '$50^2 - 3^2 = 2491$.', 'Both numbers sit 3 from 50.',
       {'no-nine': 'You squared 50 and stopped. Take off $3^2 = 9$.',
        'squared': 'You squared 47. The second number is 53, not 47.'},
       '47 and 53 sit 3 either side of 50. So $47 \\times 53 = 50^2 - 3^2 = 2500 - 9 = 2491$.',
       3, ['mp-speed'])

# B3 38 x 26
b3a = 38 * 25 + 38
b3b = 40 * 26 - 2 * 26
assert b3a == b3b == 38 * 26 == 988
key('b3-two-by-two', '988', '38 x 25 + 38', '40 x 26 - 2 x 26')
mental(3, 'two-by-two', 'Two digits by two digits', 'Work out $38 \\times 26$.',
       numeric(988, 0, [{'id': 'rounded', 'value': 1040, 'tol': {'abs': 0}},
                        {'id': 'digit', 'value': 948, 'tol': {'abs': 0}}], accept='Exactly 988'),
       '$38 \\times 25 + 38 = 988$.', 'Use $26 = 25 + 1$, or round 38 up to 40 and correct.',
       {'rounded': 'You rounded 38 up to 40 and did not correct. Take off $2 \\times 26 = 52$.',
        'digit': 'You slipped a digit in the tens. Check the last addition.'},
       '$38 \\times 25 = 950$, and one more 38 makes 988. Check: $40 \\times 26 - 2 \\times 26 = 1040 - 52 = 988$.',
       3, ['mp-speed'])

# B4 1/8 + 1/12
b4a = F(3, 24) + F(2, 24)
b4b = F(1, 8) + F(1, 12)
assert b4a == b4b == F(5, 24) and abs(float(F(125, 1000) + F(1, 12)) - 0.208333) < 1e-6 and round(float(b4a), 3) == 0.208
key('b4-fraction-sum', '5/24 = 0.208', '3/24 + 2/24', '0.125 + 0.0833')
mental(4, 'fraction-sum', 'Two fractions as a decimal', 'Write $\\tfrac18 + \\tfrac1{12}$ as a decimal, to 3 places.',
       numeric(0.208, 0.0005, [{'id': 'tops-bottoms', 'value': 0.1, 'tol': {'abs': 0.001}},
                               {'id': 'multiplied', 'value': float(round(F(1, 96), 4)), 'tol': {'abs': 0.001}}],
               placeholder='3 decimal places', accept='$\\tfrac{5}{24} \\approx 0.208$ (within 0.0005)'),
       'Over 24 the sum is $\\tfrac{5}{24}$.', 'Put both fractions over 24.',
       {'tops-bottoms': 'You added the tops and the bottoms, $\\tfrac{2}{20}$. Use a common denominator, 24.',
        'multiplied': 'You multiplied the fractions, $\\tfrac{1}{96}$. The question asks for the sum.'},
       'Over 24, $\\tfrac18 = \\tfrac{3}{24}$ and $\\tfrac1{12} = \\tfrac{2}{24}$, so the sum is $\\tfrac{5}{24} \\approx 0.208$. '
       'Check: $0.125 + 0.0833 = 0.2083$.',
       2, ['mp-fractions'])

# B5 1.06^12
b5a = F(106, 100) ** 12
sq = F(106, 100) ** 2; q4_ = sq * sq; q8_ = q4_ * q4_
b5b = q8_ * q4_
b5c = sum(math.comb(12, k) * F(6, 100) ** k for k in range(13))
assert b5a == b5b == b5c and round(float(b5a), 4) == 2.0122 and round(float(b5a), 2) == 2.01
assert F(72, 6) == 12                                 # rule of 72: 6% doubles in about 12 years
key('b5-compound', '2.0122 (2.01)', 'squaring: 1.1236, 1.2625, 1.5938, then x 1.2625', 'binomial sum of C(12,k) 0.06^k; rule of 72 gives about 2')
mental(5, 'compound', 'Twelve years at 6%', 'Estimate $1.06^{12}$ to 2 decimal places. Answers within 0.03 count.',
       numeric(2.01, 0.03, [{'id': 'simple', 'value': 1.72, 'tol': {'abs': 0.005}}], placeholder='2 decimal places',
               accept='2.01 (exactly 2.0122; within 0.03)'),
       'By the rule of 72, 6% doubles in about 12 years.', 'Use the rule of 72, or square three times.',
       {'simple': 'You added $12 \\times 6\\% = 72\\%$. Growth compounds, so each year earns on the last.'},
       'The rule of 72 says 6% doubles money in $72 / 6 = 12$ years, so the answer is near 2. '
       'Squaring gives $1.06^2 = 1.1236$, $1.06^4 \\approx 1.2625$ and $1.06^8 \\approx 1.5938$. '
       'Then $1.06^{12} = 1.06^8 \\times 1.06^4 \\approx 2.012$.',
       3, ['mp-speed'])
assert round(float(sq), 4) == 1.1236 and round(float(q4_), 4) == 1.2625 and round(float(q8_), 4) == 1.5938

# B6 Gauss
b6a = 120 * 121 // 2
b6b = 60 * 121
assert b6a == b6b == sum(range(1, 121)) == 7260 and sum(range(1, 120)) == 7140
key('b6-gauss-sum', '7260', '120 x 121 / 2', '60 pairs of 121; direct sum')
mental(6, 'gauss-sum', 'A sum in one line', 'What is $1 + 2 + 3 + \\dots + 120$?',
       numeric(7260, 0, [{'id': 'stopped', 'value': 7140, 'tol': {'abs': 0}},
                         {'id': 'no-half', 'value': 14520, 'tol': {'abs': 0}}], accept='Exactly 7260'),
       '60 pairs, each adding to 121.', 'Pair the first number with the last.',
       {'stopped': 'You stopped at 119. The sum runs to 120, so add 120.',
        'no-half': 'You worked out $120 \\times 121$ and did not halve it.'},
       'Pair 1 with 120, 2 with 119, and so on: 60 pairs, each adding to 121. So the sum is $60 \\times 121 = 7260$, which is $\\tfrac{120 \\times 121}{2}$.',
       2, ['mp-speed', 'bz-quick'])

# B7 last digit 7^2026
cycle = [pow(7, k, 10) for k in range(1, 5)]
assert cycle == [7, 9, 3, 1]
b7a = cycle[(2026 % 4) - 1]
b7b = pow(7, 2026, 10)
assert b7a == b7b == 9 and 2026 % 4 == 2 and cycle[(2027 % 4) - 1] == 3
key('b7-last-digit', '9', 'cycle 7, 9, 3, 1 and 2026 mod 4 = 2', 'pow(7, 2026, 10)')
mental(7, 'last-digit', 'The last digit of a power', 'What is the last digit of $7^{2026}$?',
       numeric(9, 0, [{'id': 'one-on', 'value': 3, 'tol': {'abs': 0}},
                      {'id': 'one-mod', 'value': 7, 'tol': {'abs': 0}}], placeholder='one digit', accept='Exactly 9'),
       'The last digits cycle 7, 9, 3, 1, and $2026 = 4 \\times 506 + 2$.', 'Write out the last digits of $7, 7^2, 7^3, 7^4$.',
       {'one-on': 'You went one step too far round the cycle. $2026 \\bmod 4 = 2$, so take the second entry.',
        'one-mod': 'You took $2026 \\bmod 4$ as 1. It is 2, since 2024 is a multiple of 4.'},
       'The last digits of the powers of 7 cycle 7, 9, 3, 1, every 4 steps. '
       'Since $2026 = 4 \\times 506 + 2$, the last digit is the second in the cycle, 9.',
       3, ['mp-speed', 'bz-quick'])

# B8 net percent
b8a = F(14, 10) * F(75, 100) - 1
b8b = (F(100) * F(14, 10) * F(3, 4) - 100) / 100
assert b8a == b8b == F(1, 20)
key('b8-net-percent', '+5%', '1.4 x 0.75 = 1.05', 'from 100: 140, then 105')
mental(8, 'net-percent', 'Up, then down', 'A price rises 40%, then falls 25%. What is the net change, in percent? Write a fall as a negative number.',
       numeric(0.05, 0.0005, [{'id': 'added', 'value': 0.15, 'tol': {'abs': 0.0005}},
                              {'id': 'multiplied', 'value': 0.10, 'tol': {'abs': 0.0005}}],
               unit='%', placeholder='a percentage', accept='+5%'),
       '$1.4 \\times 0.75 = 1.05$.', 'Start at 100 and apply each change in turn.',
       {'added': 'You added the changes, $40 - 25$. The 25% fall is taken from the higher price.',
        'multiplied': 'You took 40% of 25%. Apply the two changes one after the other.'},
       'From 100, a 40% rise gives 140. A 25% fall takes off 35, leaving 105. So the net change is +5%, as $1.4 \\times 0.75 = 1.05$.',
       2, ['mp-fractions'])

# Fermi B9 to B12
def interval_item(i, sub, title, question, value, key_iv, wide, adj, far, unit_word, whys, explain, diff, value_text):
    txt = {'key': key_iv, 'wide': wide, 'adj': adj, 'far': far}
    ivs = {k: (F(v[0]), F(v[1])) for k, v in txt.items()}
    key_iv, wide, adj, far = ivs['key'], ivs['wide'], ivs['adj'], ivs['far']
    w = key_iv[1] - key_iv[0]
    holds = {k: v[0] < value < v[1] for k, v in ivs.items()}
    assert holds == {'key': True, 'wide': True, 'adj': False, 'far': False}, (i, holds)
    assert wide[1] - wide[0] > w and adj[1] - adj[0] == w and far[1] - far[0] == w
    assert adj[0] == key_iv[1] or adj[1] == key_iv[0], 'adjacent miss shares an end with the key'
    gap = (far[0] - key_iv[1]) if far[0] >= key_iv[1] else (key_iv[0] - far[1])
    assert gap == w, 'far miss is a full width away'
    above_adj, above_far = adj[0] >= key_iv[1], far[0] >= key_iv[1]
    assert above_adj != above_far, 'the two misses sit on different sides'
    containing = [k for k, v in ivs.items() if v[0] < value < v[1]]
    assert min(containing, key=lambda k: ivs[k][1] - ivs[k][0]) == 'key'
    mids = {k: (v[0] + v[1]) / 2 for k, v in ivs.items()}
    option_rules(f'b{i}', mids['key'], [mids['adj'], mids['far']])
    option_rules(f'b{i}', mids['key'], [mids['wide'], mids['adj'], mids['far']] if mids['wide'] != mids['key'] else [mids['adj'], mids['far']])
    fmt = lambda k: f'{txt[k][0]} to {txt[k][1]}'
    opts = [{'text': fmt('key'), 'correct': True},
            {'text': fmt('wide'), 'why': f'This holds the value, but {fmt("key")} holds it too and is tighter. A wider interval scores less on the day.'},
            {'text': fmt('adj'), 'why': whys['adj']},
            {'text': fmt('far'), 'why': whys['far']}]
    wd = choice(opts); wd['label'] = 'Intervals'; del wd['layout']
    p2.append({'id': f'b{i}-{sub}', 'difficulty': diff, 'skills': ['mp-estimate'], 'tags': ['fermi-interval', sub], 'pace': 120,
               'title': title, 'question': question + ' Choose the tightest interval that holds your estimate.', 'widget': wd,
               'feedback': {'correct': f'{fmt("key")} holds the value, {value_text}, and is the tightest that does.',
                            'generic': 'Multiply the figures step by step, rounding only at the end. Then pick the narrowest interval that holds it.'},
               'explain': {'text': explain}})

# B9 coins
b9a = F(10 ** 6) * F(25, 10) / 10 ** 6               # mm to km
b9b = F(1000) * F(25, 10) / 1000 * 1000 / 1000        # 1,000 coins is 2.5 m; times 1,000 is 2,500 m
assert b9a == b9b == F(5, 2)
assert 0 < F(1, 4) < 1                                # one zero lost in mm to m lands in 0 to 1
key('b9-stack-of-coins', '2.5 km: key 2.0 to 3.0', '10^6 x 2.5 mm = 2,500 m', '1,000 coins is 2.5 m, times 1,000')
interval_item(9, 'stack-of-coins', 'A stack of coins',
              'A coin is 2.5 mm thick. How tall, in km, is a stack of 1,000,000 coins?',
              F(5, 2), ('2.0', '3.0'), ('1.0', '4.0'), ('3.0', '4.0'), ('0.0', '1.0'), 'km',
              {'adj': 'This sits wholly above the value, 2.5 km. You may have rounded 2.5 mm up to 3 mm.',
               'far': 'This sits wholly below the value, 2.5 km. Losing one zero between millimetres and metres lands here.'},
              'A million coins of 2.5 mm make 2,500,000 mm, which is 2,500 m or 2.5 km. Check: 1,000 coins stand 2.5 m, and 1,000 such stacks stand 2.5 km. '
              'The interval 1.0 to 4.0 holds it too, but it is wider, so it scores less on the day.',
              3, '2.5 km')

# B10 balls in a room
room = F(4) * 5 * F(5, 2)                              # 50 m^3
d_ = F(65, 1000); r_ = d_ / 2
def balls(pi):  # thousands
    return F(64, 100) * room / (F(4, 3) * pi * r_ ** 3) / 1000
def balls_cm(pi):  # second route in cm: (pi/6) d^3 with d = 6.5 cm, room 5e7 cm^3
    return F(64, 100) * room * 10 ** 6 / (pi / 6 * F(65, 10) ** 3) / 1000
PI_LO, PI_HI = F(314159, 100000), F(314160, 100000)
for pi in (PI_LO, PI_HI):
    assert balls(pi) == balls_cm(pi) and 222 < balls(pi) < 223
v10 = (balls(PI_LO) + balls(PI_HI)) / 2
assert round(float(v10), 1) == 222.5
cube = F(64, 100) * room / d_ ** 3 / 1000              # used a cube 6.5 cm on a side
six = F(64, 100) * room / (PI_LO / 6 * F(6, 100) ** 3) / 1000   # rounded the diameter down to 6 cm
assert 100 < cube < 150 and round(float(cube), 1) == 116.5 and 250 < six < 300 and round(float(six)) == 283
key('b10-balls-in-a-room', '222.5 thousand: key 200 to 250', '0.64 x 50 / ((4/3) pi 0.0325^3)', '0.64 x 5e7 cm^3 / ((pi/6) 6.5^3 cm^3), pi bounded either side')
interval_item(10, 'balls-in-a-room', 'Balls in a room',
              'A room is 4 m by 5 m by 2.5 m. Balls 6.5 cm across fill 64% of its volume. How many balls are there, in thousands?',
              v10, ('200', '250'), ('100', '400'), ('250', '300'), ('100', '150'), 'thousand',
              {'adj': 'This sits wholly above the value, about 222,500. Rounding the ball down to 6 cm lands near 283,000.',
               'far': 'This sits wholly below the value, about 222,500. You used a cube 6.5 cm on a side, so a ball filled $\\tfrac{\\pi}{6}$ of your space.'},
              'The room is 50 m³, and a ball is $\\tfrac{\\pi}{6} \\times 0.065^3 \\approx 0.000144$ m³. '
              'So $\\tfrac{0.64 \\times 50}{0.000144} \\approx 222{,}500$ balls, and the same sum in centimetres agrees. '
              'The interval 100 to 400 holds it too, but it is wider, so it scores less on the day.',
              4, 'about 222.5 thousand')
assert abs(float(PI_LO / 6 * d_ ** 3) - 0.000144) < 0.0000005

# B11 heartbeats
b11a = F(70) * 60 * 24 * F(36525, 100) * 80 / 10 ** 9
per_year = F(70) * 60 * 24 * F(36525, 100)
b11b = per_year * 80 / 10 ** 9
assert b11a == b11b and per_year == 36817200 and round(float(b11a), 3) == 2.945
slip_1500 = F(70) * 1500 * F(36525, 100) * 80 / 10 ** 9
slip_60 = F(60) * 60 * 24 * F(36525, 100) * 80 / 10 ** 9
assert F(3) < slip_1500 < F(32, 10) and F(24, 10) < slip_60 < F(26, 10)
key('b11-heartbeats', '2.945 billion: key 2.8 to 3.0', '70 x 60 x 24 x 365.25 x 80', '36.8 million a year, times 80')
interval_item(11, 'heartbeats', 'Heartbeats in a lifetime',
              'A heart beats 70 times a minute. How many beats is that in 80 years, in billions? Take a year as 365.25 days.',
              b11a, ('2.8', '3.0'), ('2.0', '4.0'), ('3.0', '3.2'), ('2.4', '2.6'), 'billion',
              {'adj': 'This sits wholly above the value, 2.945 billion. Rounding the 1,440 minutes in a day up to 1,500 lands here.',
               'far': 'This sits wholly below the value, 2.945 billion. Using 60 beats a minute, not 70, lands here.'},
              'A year holds $70 \\times 60 \\times 24 \\times 365.25 = 36{,}817{,}200$ beats. '
              'Times 80, that is about 2.945 billion. The interval 2.0 to 4.0 holds it too, but it is wider, so it scores less on the day.',
              3, '2.945 billion')

# B12 quote updates
b12a = F(4) * 2 * F(65, 10) * 3600 / 1000
per_hour = F(4) * 2 * 3600
b12b = per_hour * F(65, 10) / 1000
assert b12a == b12b == F(1872, 10) and per_hour == 28800
key('b12-quote-rate', '187.2 thousand: key 180 to 190', '4 x 2 x 6.5 x 3600', '28,800 an hour, times 6.5')
interval_item(12, 'quote-rate', 'Quote updates in a day',
              'A desk quotes 4 markets. Each quote is updated twice a second for a 6.5-hour day. How many updates is that, in thousands?',
              b12a, ('180', '190'), ('100', '300'), ('190', '200'), ('160', '170'), 'thousand',
              {'adj': 'This sits wholly above the value, 187,200. You rounded up a step: check that 6.5 hours stayed 6.5.',
               'far': 'This sits wholly below the value, 187,200. Check that you used 3,600 seconds an hour.'},
              'Each hour brings $4 \\times 2 \\times 3600 = 28{,}800$ updates. Over 6.5 hours that is 187,200. '
              'The interval 100 to 300 holds it too, but it is wider, so it scores less on the day.',
              3, '187,200')

# ================================================================ Paper 3
def book(g):
    # three resting levels a side, just outside the opening quote, so the learner's quote shows as the best bid and offer
    bq, aq = g['quote']['bid'], g['quote']['ask']
    return {'kind': 'orderbook', 'params': {
        'bids': [[bq - 0.5, 300], [bq - 1, 500], [bq - 1.5, 200]],
        'asks': [[aq + 0.5, 200], [aq + 1, 400], [aq + 1.5, 300]],
        'depth': 3, 'currency': '£', 'dp': 1, 'showMid': True}, 'state': {}}

def Q(b, a, s):
    return {'bid': b, 'ask': a, 'size': s}

g1 = {'kind': 'trade', 'seed': 23, 'turns': 8, 'fair': 10.5, 'value': 13, 'tick': 0.5, 'range': [3, 18], 'currency': '£', 'dp': 1,
      'size': {'min': 1, 'max': 2, 'start': 1}, 'limit': 5, 'spread': {'min': 1, 'max': 4}, 'quote': {'bid': 9, 'ask': 12, 'size': 2},
      'counterparty': [{'type': 'noise', 'rate': 0.8, 'turns': [1, 4]}, {'type': 'informed', 'edge': 0.5, 'turns': [5, 8]}],
      'schedule': [{'turn': 1, 'text': 'Three fair dice will be rolled, one at a time. Their total settles the game. Fair starts at 10.5.'},
                   {'turn': 3, 'text': 'The first die shows 6. Fair is now 13.', 'fair': 13},
                   {'turn': 6, 'text': 'The second die shows 4. Fair is now 13.5.', 'fair': 13.5},
                   {'turn': 8, 'text': 'The third die shows 3. The total is 13.', 'reveal': True}],
      'benchmark': 8, 'maxBreaks': 0,
      'strategy': [Q(9, 12, 2), Q(9, 12, 2), Q(11.5, 14.5, 1), Q(11.5, 14.5, 1), Q(11.5, 14.5, 1), Q(12.5, 14.5, 1), Q(12.5, 14.5, 1), Q(12.5, 14.5, 1)]}
# fair values twice: 3 x 3.5; 6 + 3.5 + 3.5; 6 + 4 + 3.5; and by enumeration of the dice left
dice = range(1, 7)
assert 3 * F(7, 2) == F(21, 2) == F(sum(a + b + c for a in dice for b in dice for c in dice), 216)
assert 6 + 2 * F(7, 2) == 13 == F(sum(6 + b + c for b in dice for c in dice), 36)
assert 6 + 4 + F(7, 2) == F(27, 2) == F(sum(10 + c for c in dice), 6)
assert 6 + 4 + 3 == 13

g2 = {'kind': 'trade', 'seed': 31, 'turns': 8, 'fair': 50, 'value': 46, 'tick': 0.5, 'range': [38, 58], 'currency': '£', 'dp': 1,
      'size': {'min': 1, 'max': 3, 'start': 1}, 'limit': 4, 'spread': {'min': 1, 'max': 5}, 'quote': {'bid': 48.5, 'ask': 51.5, 'size': 2},
      'counterparty': [{'type': 'noise', 'rate': 0.7, 'turns': [1, 3]}, {'type': 'informed', 'edge': 0.5, 'turns': [4, 8]}],
      'schedule': [{'turn': 1, 'text': 'The share last traded at £50.'},
                   {'turn': 4, 'text': 'A weak report. Fair is now £48.', 'fair': 48},
                   {'turn': 7, 'text': 'The value is revealed: £46.', 'reveal': True}],
      'benchmark': 12, 'maxBreaks': 0,
      'strategy': [Q(48.5, 51.5, 2)] * 3 + [Q(46, 50, 1), Q(45, 49, 1), Q(44.5, 48.5, 1), Q(44.5, 47.5, 1), Q(44.5, 47.5, 1)]}

g3 = {'kind': 'trade', 'seed': 41, 'turns': 6, 'fair': 100, 'value': 104, 'tick': 0.5, 'range': [92, 112], 'currency': '£', 'dp': 1,
      'size': {'min': 1, 'max': 2, 'start': 1}, 'limit': 3, 'spread': {'min': 2, 'max': 6}, 'quote': {'bid': 98, 'ask': 102, 'size': 2},
      'counterparty': {'type': 'scripted', 'trades': [{'act': 'hit', 'size': 2, 'price': 98}, {'act': 'hit', 'size': 2, 'price': 97.5},
                                                      {'act': 'hit', 'size': 2, 'price': 97}, {'act': 'lift', 'size': 2, 'price': 102},
                                                      {'act': 'lift', 'size': 2, 'price': 101}, {'act': 'none'}]},
      'schedule': [{'turn': 1, 'text': 'The interviewer will trade against you. Fair starts at £100, and the position limit is 3.'},
                   {'turn': 4, 'text': 'The interviewer says the level looks higher. Fair is now £102.', 'fair': 102},
                   {'turn': 6, 'text': 'The value is revealed: £104.', 'reveal': True}],
      'benchmark': 6, 'maxBreaks': 0,
      'strategy': [Q(98, 102, 2), Q(96.5, 100.5, 1), Q(96.5, 100.5, 1), Q(100, 102, 1), Q(99, 101, 1), Q(101, 105, 1)]}

res = json.loads(subprocess.run(['node', os.path.join(HERE, 'play.js')], input=json.dumps([g1, g2, g3]),
                                capture_output=True, text=True, check=True).stdout)
expect = [(9.5, 1, 2), (19.5, 2, 3), (7, 14, 3)]
for g, r, (pnl, idle_pnl, idle_breaks) in zip([g1, g2, g3], res, expect):
    assert r['strategy']['ok'] and r['strategy']['breaks'] == 0 and r['strategy']['pnl'] == pnl, r['strategy']
    assert not r['idle']['ok'] and r['idle']['pnl'] == idle_pnl and r['idle']['breaks'] == idle_breaks, r['idle']
    assert r['strategy']['pnl'] - g['benchmark'] >= 1, 'keep a margin of at least £1'
    # second check of the P&L by hand: cash from the fills plus the position at the value
    cash = sum((-1 if t['fill']['side'] == 'buy' else 1) * t['fill']['qty'] * t['fill']['price'] for t in res[[g1, g2, g3].index(g)]['log'] if t['fill'])
    pos = sum((1 if t['fill']['side'] == 'buy' else -1) * t['fill']['qty'] for t in r['log'] if t['fill'])
    assert F(cash).limit_denominator() + pos * F(g['value']) == F(pnl).limit_denominator()
# the debrief: after turn 1 of g3 the position is +2 at £98; a sale of 2 more would leave +4, of 1 more +3 (the limit)
assert res[2]['log'][0]['fill'] == {'side': 'buy', 'qty': 2, 'price': 98, 'edge': 12} and res[2]['log'][0]['pos'] == 2
assert res[2]['log'][1]['fill'] is None and 2 + 2 > g3['limit'] and 2 + 1 == g3['limit']
assert 100.5 > 100 and 2 <= 100.5 - 96.5 <= 6 and 96.5 < 97.5
key('c1-three-dice', 'P&L £9.50 (benchmark £8)', 'trade.js play: bought 2 at £9, sold 1 at £14.50, settled 1 at £13', 'cash -18 + 14.5 + 13 = 9.5; idle quote £1 with 2 limit breaks')
key('c2-bad-news', 'P&L £19.50 (benchmark £12)', 'trade.js play: bought 1 at £48.50, sold 2 at £51.50 twice, short 3 into £46', 'cash 157.5 - 3 x 46 = 19.5; idle quote £2 with 3 limit breaks')
key('c3-interviewer-flow', 'P&L £7 (benchmark £6)', 'trade.js play: bought 2 at £98, sold 1 at £102 and 1 at £101', 'cash -196 + 102 + 101 = 7; idle quote £14 with 3 limit breaks')

def trade_item(iid, diff, skills, tag, pace, title, prose, question, g, fb, explain):
    return {'id': iid, 'difficulty': diff, 'skills': skills, 'tags': [tag], 'pace': pace, 'title': title, 'prose': prose,
            'question': question, 'canvas': book(g), 'widget': g, 'feedback': fb, 'explain': {'text': explain}}

p3 = [
    trade_item('c1-three-dice', 3, ['mg-fair', 'mg-update'], 'three-dice', 420, 'Make a market on three dice',
               'The game settles at the total of three fair dice, shown one card at a time. Each turn you quote a bid, an ask and a size. '
               'A counterparty may then trade at your prices. Later in the game the interviewer may know more than you.',
               'Finish the eight turns with a P&L of at least £8, and no rule breaks.', g1,
               {'correct': 'You moved your quote up with each die and kept it either side of fair.',
                'generic': 'After each card, centre your quote on the new fair value and keep your position small.',
                'byKey': {'low': 'You kept your opening prices after the first die showed 6, so buyers took your ask below fair.',
                          'limit': 'You kept quoting 2 a side as your position grew, so a quote passed the limit of 5.',
                          'crossed': 'You set your bid at or above your ask, so nobody could trade that turn.',
                          'spread': 'You set a spread outside £1 to £4. Keep the ask £1 to £4 above the bid.'}},
               'The model run bought 2 at £9, then sold 1 at £14.50 after the first die. It held 1 into the total of 13, for a P&L of £9.50. '
               'Its later quotes sat either side of fair, so the informed traders had nothing to take.'),
    trade_item('c2-bad-news', 4, ['mg-update', 'mg-risk'], 'bad-news', 480, 'Bad news, then informed sellers',
               'A share opens at £50 and settles at a hidden value after turn 8. Each turn you quote a bid, an ask and a size. '
               'After the news, the traders you meet may know the value.',
               'Finish the eight turns with a P&L of at least £12, and no rule breaks.', g2,
               {'correct': 'You sold to the noise traders early and kept your bid low once the sellers knew more.',
                'generic': 'After a weak report, move your bid well down: an informed seller only hits a bid above the value.',
                'byKey': {'low': 'You kept your bid near £48.50 after the weak report, so informed sellers hit it above the value.',
                          'limit': 'You kept quoting 2 as informed sellers hit your bid, so a quote passed the limit of 4.',
                          'crossed': 'You set your bid at or above your ask, so nobody could trade that turn.',
                          'spread': 'You set a spread outside £1 to £5. Keep the ask £1 to £5 above the bid.'}},
               'The model run bought 1 at £48.50 and sold 2 at £51.50 twice, ending short 3. '
               'After the report its bid stayed at £46 or lower, so informed sellers had nothing to hit. '
               'Short 3 into a value of £46, its P&L was £19.50.'),
    trade_item('c3-interviewer-flow', 4, ['mg-quote', 'mg-risk'], 'interviewer-flow', 420, 'The interviewer tests your limit',
               'The interviewer is your only counterparty and plays to a script. Each turn you quote a bid, an ask and a size. '
               'Your position limit is 3 either way. The interviewer may know more than you.',
               'Finish the six turns with a P&L of at least £6, and no rule breaks.', g3,
               {'correct': 'You stepped your bid away before your position reached the limit.',
                'generic': 'Watch your position. When the interviewer keeps selling, lower your bid so you stop buying.',
                'byKey': {'low': 'You sold to the interviewer too far below the value, or bought too little at £98.',
                          'limit': 'You kept buying until your position reached the limit of 3. Then even a size of 1 breaks it, so lower your bid before you get there.',
                          'crossed': 'You set your bid at or above your ask, so nobody could trade that turn.',
                          'spread': 'You set a spread outside £2 to £6. Keep the ask £2 to £6 above the bid.'}},
               'The model run bought 2 at £98, then bid £96.50 so the interviewer could sell no more. '
               'It sold 1 at £102 and 1 at £101 to finish flat, for a P&L of £7. '
               'Both sales were under the value of £104: the interviewer knew more.'),
    {'id': 'c4-defend-the-skew', 'difficulty': 4, 'skills': ['mg-quote', 'mg-risk', 'rk-behave'], 'tags': ['market-defence'], 'pace': 480,
     'title': 'Defend your quote', 'kind': 'longform',
     'prompt': 'Say your answer aloud first, then type it.\n\n'
               'Fair is £100, your limit is 3 either way, and spreads must be £2 to £6. '
               'You bought 2 at £98 on turn 1. The interviewer offers to sell again at £97.50. '
               'You quote £96.50 to £100.50 for 1. Explain the quote.',
     'model': 'I am long 2 against a limit of 3, so I have room to buy only 1 more. '
              'If the interviewer sold me 2 at £97.50, I would be long 4, over the limit. '
              'Even 1 more leaves me at the limit, where any bid breaks it. '
              'So my bid of £96.50 sits under their £97.50, and they cannot sell to me. '
              'My ask of £100.50 is above fair at £100, so a sale still earns. '
              'The quote is skewed down because of my inventory, not a view on the price. '
              'A seller who keeps selling may also know more, which is one more reason to stop buying. '
              'The width is £4, inside the £2 to £6 allowed. '
              'A card, a new price or a fill would change it. '
              'So my quote is £96.50 to £100.50 for 1.',
     'rubric': [
         {'points': 2, 'text': 'States the position, long 2, and the limit of 3'},
         {'points': 2, 'text': 'Says the bid sits below the interviewer\'s £97.50, so no more is bought'},
         {'points': 1, 'text': 'Gives the ask against the fair value of £100'},
         {'points': 2, 'text': 'Names the skew as inventory management, not a view'},
         {'points': 1, 'text': 'Mentions adverse selection: a seller who keeps selling may know more'},
         {'points': 1, 'text': 'States what would change the quote: a card, a price or a fill'},
         {'points': 1, 'text': 'Reasons aloud, in order, with a clear final quote'},
     ]},
]

# ================================================================ Paper 4
EXAMPLE = '*An example answer. Your own story is the real answer, so use this for its shape only.*\n\n'
p4 = [
    {'id': 'd1-why-trading', 'difficulty': 3, 'skills': ['rk-behave'], 'tags': ['why-trading'], 'pace': 480,
     'title': 'Why trading', 'kind': 'longform',
     'prompt': 'Say your answer aloud first, then type it in at most 200 words.\n\n'
               'Why do you want to trade rather than work at a bank or a lab?',
     'model': EXAMPLE +
              'I want to trade because I like pricing things I cannot know for sure. '
              'I also want fast, honest feedback: a trading decision is scored within hours, not years. '
              'At university I ran a prediction-market club for 40 students. '
              'I set the weekly prices and logged every call. My hit rate rose from 52% to 61% over a term. '
              'What I find hard is letting go of a loss. '
              'I now write my reason before each trade and review the reason afterwards, not the result. '
              'A bank puts the client first, and a lab works on long cycles. '
              'A trading firm puts the decision and its feedback at the centre. That is the work I want every day.',
     'rubric': [
         {'points': 1, 'text': 'Gives a one-sentence answer first'},
         {'points': 2, 'text': 'Two reasons tied to the daily work, such as pricing under uncertainty and fast feedback'},
         {'points': 3, 'text': 'One piece of your own evidence, with a number or an outcome'},
         {'points': 2, 'text': 'Says what you dislike or find hard about trading, and how you handle it'},
         {'points': 1, 'text': 'Says why a trading firm rather than another route'},
         {'points': 1, 'text': 'Takes about 90 seconds aloud, with no clichés'},
     ]},
    {'id': 'd2-decision-under-uncertainty', 'difficulty': 3, 'skills': ['rk-behave'], 'tags': ['decision-under-uncertainty'], 'pace': 480,
     'title': 'A decision without all the facts', 'kind': 'longform',
     'prompt': 'Say your answer aloud first, then type it in at most 200 words.\n\n'
               'Tell me about a decision you made with incomplete information, and what you would change.',
     'model': EXAMPLE +
              'In my second year I led a four-person project with a fixed deadline. '
              'Two weeks out, our data supplier stopped replying. '
              'I did not know whether the data would arrive in time. '
              'I put the chance it would be late at about one in three. '
              'Waiting cost nothing if it came, but the whole grade if it did not. '
              'Switching to a public data set cost about two days of extra work. '
              'So I switched that week. '
              'The supplier\'s data came four days late. '
              'We handed in on time with a narrower analysis and scored 68%. '
              'I would change one thing. '
              'I would set a check-in date with the supplier at the start, so the warning came a week sooner.',
     'rubric': [
         {'points': 1, 'text': 'Sets out the situation in one or two sentences'},
         {'points': 2, 'text': 'Says what you did not know'},
         {'points': 3, 'text': 'The decision and its reason, with a rough probability or cost'},
         {'points': 1, 'text': 'States the result honestly'},
         {'points': 2, 'text': 'Says what you would change, and how you would know sooner'},
         {'points': 1, 'text': 'Speaks in the first person, in under two minutes'},
     ]},
]

# ================================================================ Exam
exam = {
    'id': 'mock-superday-trader',
    'name': 'Trader superday',
    'style': 'trader',
    'models': 'Reported, as of Nov 2026: trading-firm final rounds at Jane Street, Optiver, SIG, IMC and Citadel Securities. Probability, mental maths, market-making games and fit questions.',
    'description': "This is the reported shape of a trading firm's final-round day, as candidates described it by Nov 2026. "
                   'Jane Street, Optiver, SIG, IMC and Citadel Securities all report these rounds. '
                   'They cover probability and betting games, mental maths, market-making games and fit questions. '
                   'There are four papers, each on its own clock. '
                   'Real rounds are spoken, so say each written answer aloud before you type it. '
                   'Mental maths is one question at a time with no going back. '
                   'No calculator is allowed. '
                   'Orders and lengths differ by firm and office. '
                   'Two checks at the end ask for what the app cannot see.',
    'skills': {'pz-expectation': 'Expected value puzzles', 'pz-conditioning': 'Conditioning puzzles', 'pz-games': 'Games and betting',
               'gm-poker': 'Poker and betting decisions', 'mp-speed': 'Speed arithmetic', 'mp-fractions': 'Fractions and percentages at speed',
               'mp-estimate': 'Fast estimation', 'bz-quick': 'Quick reasoning', 'mg-fair': 'Fair value', 'mg-quote': 'Quoting',
               'mg-update': 'Updating on trades', 'mg-risk': 'Position and risk', 'rk-behave': 'Behavioural answers'},
    'parts': [
        {'kind': 'paper', 'id': 'probability', 'name': 'Probability and expected value', 'minutes': 45,
         'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 0.65, 'items': p1},
        {'kind': 'paper', 'id': 'mental', 'name': 'Mental maths and Fermi', 'minutes': 15,
         'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 0.7, 'navigation': 'forward', 'skip': False, 'items': p2},
        {'kind': 'paper', 'id': 'market', 'name': 'Market-making game', 'minutes': 30,
         'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 0.75, 'items': p3},
        {'kind': 'paper', 'id': 'fit', 'name': 'Fit and motivation', 'minutes': 18,
         'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 0.5, 'items': p4},
        {'kind': 'check', 'id': 'game-aloud', 'name': 'I played a full market-making game aloud with a partner',
         'detail': 'Tick this only if a real person played the counterparty and you spoke your reasoning at every quote.'},
        {'kind': 'check', 'id': 'why-aloud', 'name': 'I said my why-trading answer aloud in under 90 seconds',
         'detail': 'Tick this only if you timed it.'},
    ],
}

# ---------------------------------------------------------------- structure asserts
MODELS_LEN = len(exam['models']); print('models length', MODELS_LEN)
papers = [p for p in exam['parts'] if p['kind'] == 'paper']
assert [len(p['items']) for p in papers] == [6, 12, 4, 2]
assert [p['minutes'] for p in papers] == [45, 15, 30, 18] and sum(p['minutes'] for p in papers) == 108
assert [sum(i['pace'] for i in p['items']) for p in papers] == [2520, 800, 1800, 960]
assert sum(1 for p in papers for i in p['items'] if i.get('kind') == 'longform') == 5
for p, need in zip(papers, [4, 9, 3, 1]):
    n = len(p['items'])
    assert math.ceil(p['pass'] * n - 1e-9) == need, (p['id'], p['pass'] * n)
assert len(exam['models']) <= 200 and len(exam['models']) == MODELS_LEN
all_items = [i for p in papers for i in p['items']]
used = {s for i in all_items for s in i['skills']}
assert used == set(exam['skills']), (used ^ set(exam['skills']))
for i in all_items:
    assert i['tags'] and i['pace'] and i['skills'] and 1 <= i['difficulty'] <= 5
    if i.get('widget', {}).get('kind') == 'choice':
        assert i['widget']['shuffle'] is True
        assert all('why' in o for o in i['widget']['options'] if not o.get('correct'))
    if i.get('kind') == 'longform':
        assert sum(r['points'] for r in i['rubric']) == 10 and 'widget' not in i
FIRMS = ['Jane Street', 'Optiver', 'SIG', 'IMC', 'Citadel']
for i in all_items:
    blob = json.dumps(i)
    assert not any(f in blob for f in FIRMS), i['id']
assert 'reported' in exam['description'] and 'Nov 2026' in exam['description'] and 'Reported' in exam['models'] and 'Nov 2026' in exam['models']

# ---------------------------------------------------------------- duplicates against the OA mocks
def text_of(it):
    return ' '.join(str(it.get(k, '')) for k in ('prose', 'question', 'prompt')).strip()
def key_of(it):
    w = it.get('widget') or {}
    if w.get('kind') == 'choice':
        return next(o['text'] for o in w['options'] if o.get('correct'))
    if w.get('kind') == 'numeric':
        return str(w['answer'])
    if w.get('kind') == 'order':
        return ','.join(w['answer'])
    return None
theirs = []
src_files = sorted(glob.glob(f'{EXAMS}/mock-oa-trader*.json') + glob.glob(f'{EXAMS}/mock-oa-sig*.json'))
assert len(src_files) >= 4 and any(f.endswith('mock-oa-sig.json') for f in src_files) and sum('mock-oa-trader' in f for f in src_files) == 3
for f in src_files:
    for p in json.load(open(f))['parts']:
        for it in p.get('items', []):
            if 'generator' in it:
                continue
            theirs.append((os.path.basename(f), it.get('tags', []), text_of(it), key_of(it)))
their_tags = {t for _, tags, _, _ in theirs for t in tags}
their_families = {tags[0] for _, tags, _, _ in theirs if tags}
their_text = {re.sub(r'\s+', ' ', t.lower()) for _, _, t, _ in theirs}
their_pairs = {(re.sub(r'\s+', ' ', t.lower()), k) for _, _, t, k in theirs}
TAKEN = set('dice-ev linearity ev-fee indicator at-least-one cards-conditional binomial weighing bayes waiting-time stopping max-of-draws '
            'bayes-multi ruin-fair ruin-biased bayes-ruin dice-sum same-suit reroll-ev distinct-days first-success committee urn '
            'natural-frequency max-of-dice given-the-total first-to-six pattern-race likelihood-ranking interval sequence'.split())
for it in all_items:
    fam = it['tags'][0]
    assert fam not in their_tags and fam not in TAKEN and fam not in their_families, (it['id'], fam)
    for t in it['tags']:
        assert t not in their_tags, (it['id'], t)
    mine = re.sub(r'\s+', ' ', text_of(it).lower())
    assert mine not in their_text, it['id']
    assert (mine, key_of(it)) not in their_pairs, it['id']
    for _, _, t, _ in theirs:
        r = difflib.SequenceMatcher(None, mine, t.lower()).ratio()
        assert r < 0.8, (it['id'], r, t)
print(f'duplicate check: {len(all_items)} items against {len(theirs)} items in {len(src_files)} files; {len(their_tags)} tags taken; none repeated')

with open(OUT, 'w') as fh:
    json.dump(exam, fh, ensure_ascii=False, indent=2)
    fh.write('\n')

print(f'wrote {OUT}')
print('item | key | method 1 | method 2')
for row in KEYS:
    print(' | '.join(row))
for g, r in zip(['c1-three-dice', 'c2-bad-news', 'c3-interviewer-flow'], res):
    print(g, 'strategy', r['strategy'], 'idle', r['idle'], r['idleBreaks'])
```

## `play.js`

```js
// Replays trade specs through the app's own game. stdin: JSON list of widget specs. stdout: one verdict pair per spec.
const T = require('/home/user/zero-to-quant/app/js/engine/widgets/trade.js');
let s = '';
process.stdin.on('data', (d) => (s += d));
process.stdin.on('end', () => {
  const out = JSON.parse(s).map((w) => {
    const run = T.play(w, w.strategy), idle = T.play(w, null);
    return {
      strategy: run.verdict, idle: idle.verdict,
      idleBreaks: idle.g.breaks.map((b) => `${b.turn}:${b.kind}`),
      log: run.g.log.map((r) => ({ turn: r.turn, bid: r.bid, ask: r.ask, size: r.size, who: r.who, fill: r.fill, pos: r.pos, cash: r.cash })),
    };
  });
  process.stdout.write(JSON.stringify(out));
});
```

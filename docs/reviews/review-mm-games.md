# Topic 3.3 (Market-Making Games): second-reader findings

Scope: every lesson, review and homework file in `app/content/courses/mm-games/`: l1 to l18, review-1 to review-4, homework-1 to homework-4 (26 files, 18 lessons, 40 review items, 38 homework items).
Method: every stated number recomputed in Python (exact `Fraction`s, `math.comb` binomials, `statistics.NormalDist`, the gambler's ruin formula, exhaustive dice and card enumeration); every `trade` game (11 of them) replayed with the engine's own module, `require('app/js/engine/widgets/trade.js')` under node (`trades.mjs`), for the authored `strategy`, the opening quote and every alternative run the text quotes (stale, no skew, size 2, king and queen cases: `alt.mjs`); the l11 scatter (seed 11) and the l6 and l8 seeded rolls rebuilt from the engine's mulberry32 and from Python `random.Random`; all 26 code widgets run, solution and starter, through a copy of the `code.js` judge (`codecheck.py`); every choice, numeric, table-cell and slider item scanned for `shuffle`, `why`, `byKey`, tolerance overlap, `tags`, `pace`, difficulty and unit (`scan.py`); copy scanned for `!`, em-dashes, American spellings, firm names and currency; `voice-scan.py` run (output `docs/reviews/voice-3.3-mm-games.txt`). Scripts are in the session scratchpad `read-mm-games/`. Validator not run (it rewrites `content/manifest.json`, and this pass is read-only on content).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, missing feedback or teaching issue; note = style or layout.

**Counts: 2 errors, 7 warnings, 27 notes (6 of them voice).**

**Clean results.** No keyed answer is wrong, and every stated number in all 26 files recomputes. All 26 code widgets pass their hidden tests with the solution, and every starter fails them. All 11 trade games replay to the figures quoted in their own explain, in later screens, in the review and in the homework: each strategy meets its benchmark with no rule breaks, and each opening quote misses it or breaks a rule. The 16 distractor values and 4 wordings fixed on 5 November (`answers-2026-11-05.md`, fix pass) are in place and now match their slips. No exclamation marks (the `!` hits are `$7!$` and KaTeX `\!`), no em-dashes, no American spellings, £ throughout (dollars, euros and yen appear only as currencies in the FX loops).

## Trade games replayed (engine module)

| File | Seed | Strategy P&L, position, cash | Benchmark | Opening quote | Quoted elsewhere, all matched |
|---|---|---|---|---|---|
| l10 `screens[2]` | 38 | +3.50, +3, −26.50 | 2 | 4.00, limit break turn 8 | l10 `screens[3]` table and −5.50 at a roll of 7 |
| l11 `screens[4]` | 16 | +6.00, −2, +20 | 5 | 3.00 | l11 `screens[5]`, `screens[6]` (+4.80 hedged, sd 4.83 to 3.42) |
| l13 `screens[1]` | 13 | +12.50, −1, +27.50 | 10 | 0.00, +1 | l13 `screens[4]` to `[6]`, quiz, review-3 `r-judge`, homework-3 model (no skew +13 short 2, king +4.50, queen +5.50) |
| l14 `screens[3]` | 14 | 0, 0, 0 | 0 | −200 | l14 `screens[4]` (−100 a turn) |
| l15 `screens[3]` | 5 | +0.80, +4, −27.20 | 0.30 | −0.80 | l15 `screens[4]` (edges 0.30, 0.20, 0.30) |
| l16 `screens[4]` | 6 | +0.70, −1, +2.70 | 0.30 | −5.40 (buys 3 at 3.8) | l16 `screens[5]` |
| l17 `screens[3]` | 17 | +1.70, −1, +2.70 | 1.50 | −0.20 | l17 `screens[4]` (−0.30 with a 6) |
| review-3 `items[0]` | 10 | +2.00, −1, +10 | 1.50 | 2.00 with 5 limit breaks | explain |
| review-4 `items[0]` | 41 | 0, 0, 0 | 0 | −160 | explain |
| homework-3 `items[4]` | 131 | +18.50, +1, −11.50 | 12 | −3.00 | `h-mock-pnl` (+18.50, 14.40 at 25.9), `h-mock-aloud` model (no skew +21, long 2) |
| homework-4 `items[3]` | 4 | +1.80, 0, +1.80 | 0.80 | +0.20 (stale at size 2: +0.40) | `h4-mock-pnl`, `h4-mock-aloud` model |

## Level 1 (l1 to l4, review-1, homework-1)

- app/content/courses/mm-games/l1-unknown-quantity.json | screens[11] prose | warning | Names a firm: "Jane Street's free Probability and Markets guide". DECISIONS "Firm names (2 Nov)" allows firm names only in recruiting l4 and mock descriptions; l5, l10 and l14 already cite the same guide firm-neutrally. | "*Probability and Markets*, a free guide written by a trading firm, describes rounds like this."
- app/content/courses/mm-games/l1-unknown-quantity.json, l2-dice-sum.json, l3-how-wide.json, l4-fermi.json | quiz[0] to quiz[3] (13 items) | warning | No `tags` (and no `pace`) on any level-1 quiz item, while every quiz in levels 2 to 4 has both. An untagged item never joins the Interview practice deck. | Tag each, for example `q-500-pages` `["digit-count"]`, `q-four-board` `["chess-squares"]`, `q-first-six` `["dice-ev"]`, `q-three-nine-twelve` `["coverage"]`, `q-lse-minutes` `["fermi"]`; pace 30 to 60.
- app/content/courses/mm-games/review-1.json, homework-1.json | all items (19) | note | No `pace` on any item; reviews 2 to 4 and homeworks 2 to 4 carry it. | Add pace (30 to 120 for numeric and choice items, 900 to 1500 for the code items, 600 for `h-mock-opening`).
- app/content/courses/mm-games/l1-unknown-quantity.json | screens[5] option `narrow` why | note | "It is a point estimate with decimals": 8,700 to 8,710 has no decimals. | "It is a guess dressed as a range, and it misses the true 8,784."
- app/content/courses/mm-games/l4-fermi.json | screens[3] prose | note | "the trick from mental-pressure lesson 7" shows the course slug to the learner. | "the trick from Mental Maths Under Pressure, lesson 7".
- app/content/courses/mm-games/review-1.json | `r-abs-diff` explain | note | "A seeded check of 200,000 rolls gives 1.949" states no seed; seeds 0 to 7, 11 and 42 of `random.Random` give 1.937 to 1.945, never 1.949 (exact 35/18 = 1.9444). `r-max-three` (4.958) and homework-1 `h-distinct-faces` (2.527) also name no seed, though common seeds reproduce them. | Drop the simulation sentence, or state the seed: "Seed 0 gives 1.945."
- app/content/courses/mm-games/review-1.json | `r-coins-mile` option `precise` | note | 71,526.4 comes from 1,609.344 m and 2.25 cm, figures the learner is not given; the prose gives 1,600 m and 2.3 cm, which give 69,565.2. | Option text "69,565.2 coins."

## Level 2 (l5 to l9, review-2, homework-2)

- app/content/courses/mm-games/l9-cards-revealed.json | screens[4] explain | error | "Short 1, you might lean a little higher, as the last lesson showed": the last lesson is l8 (informed flow); the inventory skew was taught in l7. | "...as lesson 7 showed."
- app/content/courses/mm-games/l8-informed-flow.json | quiz[2] `q-alpha-up` wrong `added` (10.4) | warning | No `byKey` line, so the learner who adds 0.4 to 10 gets only the generic line. | byKey `added`: "You added 0.4 to 10p. The half-spread is the share times the move: 0.4 × 10."
- app/content/courses/mm-games/review-2.json | `r-fresh-vs-shared` wrong `seven` (1) | warning | No `byKey` line, and no stated slip gives 1. The likely slip is taking the shared deck's mean as 6 (7 − 6). | byKey `seven`: "You took the shared deck's mean as 6. It is 351/51, so the gap is 7 − 351/51 = 2/17."
- app/content/courses/mm-games/l8-informed-flow.json | screens[2] table cell wrongs `one-side` (0.0833), `count` (0.6667) | warning | Neither id has a `byKey` line. The generic line covers counting trades but not the one-sided slip. | byKey `one-side`: "You counted only face 6. Face 1 sits 0.5 below the bid too."; byKey `count`: "That is the share of faces that trade. Weight each by how far outside it lands."
- app/content/courses/mm-games/l8-informed-flow.json | screens[4] table cell wrongs `full` (1.1667, 0.3333) | note | No `byKey` line; the generic line does name the slip ("only half the counterparties are informed"). | byKey `full`: "You took the whole informed loss. Only half the flow is informed, so halve it."
- app/content/courses/mm-games/l6-edge.json | screens[1] choice | note | No `shuffle`; the options (£0.50, £0, £3.50, keeps swinging) are not ordered. | `"shuffle": true`.
- app/content/courses/mm-games/l7-skewing.json | screens[1] choice | note | No `shuffle`; up, down, wider, unmoved are not ordered. | `"shuffle": true`.
- app/content/courses/mm-games/l6-edge.json | screens[7] explain | note | "One £100 play has the same edge with an sd of £170.78" reads as a £100 stake. The figure is one play at 100 times the size (stake £300, edge £50). | "One play at 100 times the size has the same £50 edge, with an sd of £170.78."
- app/content/courses/mm-games/l7-skewing.json | screens[10] explain | note | "the seeded four trades give the table you filled in": nothing is seeded; the four trades are the fixed list of screen 3. | "...so the four trades from the table give the bids you filled in."
- app/content/courses/mm-games/l5-two-sided.json, l7-skewing.json | screens[10] widget.how | note | "math.isclose" in prose without code formatting. | `` `math.isclose` ``.
- app/content/courses/mm-games/homework-2.json | items[0], items[1] (code) | note | No `pace` (homework-3 and homework-4 code items carry 900 to 1500). | Add pace 1500 and 900.

## Level 3 (l10 to l13, review-3, homework-3)

- app/content/courses/mm-games/l10-position-limits.json | screens[11] wrong `conviction` (250) | warning | 250 is 50 + 200, both traders' counts added; the why "You added lots for conviction" does not name that slip. | why and byKey: "You added the two traders' counts. Each has its own £40,000 of risk: 40,000/800 = 50."
- app/content/courses/mm-games/l12-thinking-aloud.json | screens[6] option `finish` and explain | note | The keyed reply quotes 12.5 at 14.5, which needs a skew of 0.25 a lot and a half-width of 1; the prose states neither, so the learner cannot check the numbers. | Prose: "You quote with half-width 1 and skew 0.25 a lot."
- app/content/courses/mm-games/l13-full-game.json | screens[1] explain | note | "missed the sale after the 4" is the interviewer's sale, a purchase for the model; it reads as the model failing to sell. | "...and its 16.5 bid missed the interviewer's sale at 19 after the 4."
- app/content/courses/mm-games/l13-full-game.json, homework-3.json | screens[1] / items[4] byKey `limit` | note | "Size 2 after the first sale (buy) breaks the limit of 3" holds only if the first fill was 2. Replayed: size 1 on turn 1 then size 2 on turn 2 breaks nothing; size 2 on turns 1 and 2 breaks on turns 2, 5 and 6. | "A quote was larger than your room. Short (long) 2, a size of 2 breaks the limit of 3."
- app/content/courses/mm-games/l11-hedging.json | screens[10] explain | note | "An options desk short calls does the same" is ungrammatical. | "A desk that is short calls does the same with shares: it buys the calls' delta."

## Level 4 (l14 to l18, review-4, homework-4)

- app/content/courses/mm-games/l16-several-contracts.json | screens[2] option `same` why and byKey | error | "E and F pay less than A on every face" is false: E pays exactly A on faces 2, 4 and 6, and F on 1, 3 and 5. | "E and F each pay A on half the faces and nothing on the rest, so each is worth less than A."
- app/content/courses/mm-games/l18-betting-board.json | screens[11] wrong `cut` (60,000) | warning | "You cut by the whole £200,000 loss twice over" gives −£300,000, not £60,000. The stored value is a 40% cut, twice the 20% fall. | why and byKey: "You cut the size by 40%, twice the 20% fall. Take 10% of £800,000."
- app/content/courses/mm-games/l14-quoting-an-interval.json | screens[9] wrongs `width` (4) and `noweight` (5) | note | Both tolerances are 0.5, so the two ranges touch at 4.5 (that typed value takes the first). | tol 0.4 on each.
- app/content/courses/mm-games/l17-options-on-a-game.json | screens[9] explain | note | "Any gap is a trade, as the twist showed": no screen is called a twist; the parity break is screen 6. | "...as the parity break on the sum showed."
- app/content/courses/mm-games/l15-arbitrage-in-a-book.json | quiz[2] `q-fx` | note | The answer is pounds ("what does £1 become?") but `unit` is empty. | `"unit": "£"`.
- app/content/courses/mm-games/l18-betting-board.json | screens[0] canvas caption | note | "Odds of b to 1 pay £b" uses `b` for the odds on a board whose second bet is named b (at 2 to 1). | "Odds of 2 to 1 pay £2 for each £1 staked."
- app/content/courses/mm-games/l13-full-game.json screens[4] (right) and [6], l14-quoting-an-interval.json screens[4], l18-betting-board.json screens[3] and [6], l10-position-limits.json screens[3] (right), l16-several-contracts.json screens[3] | table canvases | note | Five-column tables with headers such as "Fair then", "Holds 25?" and "Win chance"; at 390 px (about 50 characters a line) these are likely to go compact or scroll sideways. Pairs stack below 480 px, so only width matters. | Shorten headers ("Fair", "Hit?", "p") or drop a column (the l18 tables can lose "Odds" once the board is known); check with `playthrough.mjs --mobile`.

## Voice (`docs/reviews/voice-3.3-mm-games.txt`: 6 sentences over 20 words, 0 explanations over three sentences, 9,780 sentences scanned)

KNOWN_ISSUES records this debt (mm-games L1, l4-fermi). Three of the six are a display formula with no full stop, which the scan joins to the next sentence.

- app/content/courses/mm-games/homework-1.json | items[7] prose | note | 27 words. | "You estimate an exchange's trades in a day. It lists 2,000 shares, good to a factor of 2. Each trades about 3,000 times, good to a factor of 3."
- app/content/courses/mm-games/l1-unknown-quantity.json | screens[7] prose | note | 32 words (the display has no full stop). | "You are **calibrated** when your ranges at level $p$ hold the truth a share $p$ of the time. $$\text{hit rate} = \dots \approx p.$$ The fair value is the centre of a belief, and the range is its spread."
- app/content/courses/mm-games/l3-how-wide.json | screens[8] prose | note | 28 words (the display has no full stop). | "For a near-normal total, a quote of $\mu \pm k\sigma$ holds a share fixed by $k$. $$P(|X - \mu| \le \sigma) \approx 0.68.$$ On two dice, $7 \pm 2.42$ holds the totals 5 to 9, which is 2/3."
- app/content/courses/mm-games/l3-how-wide.json | summary.ideas[0] | note | 21 words. | "A range of fair value ± k sd holds a share set by k. On two dice, 5 to 9 holds 2/3."
- app/content/courses/mm-games/l4-fermi.json | screens[7] prose | note | 24 words (the display has no full stop). | "Logs turn a product into a sum. $$\ln Q = \ln f_1 + \ln f_2 + \ln f_3.$$ If factor $i$ is good to a factor $r_i$, the total is good to about $r_1 r_2 r_3$."
- app/content/courses/mm-games/l4-fermi.json | quiz[1] prose | note | 24 words. | "A Fermi estimate has four factors. Two are good to a factor of 2, one to a factor of 3, and one is exact."

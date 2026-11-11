# Concept audit, round 2: mm-games levels 1 to 3

Auditor: blind Fable reader, round 2. Scope: `app/content/courses/mm-games/` files `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3`. Level 4 is out of scope.

Blind rule: the ledger, the findings below and the three concepts scripts were written and committed before any earlier review, audit, ledger, concepts script, author report or diff of the course folder was opened. The overlap table and the gate results were added in a second commit.

Ledger: `docs/reports/audit-mm-games-1-3-r2-ledger.md` (3,207 rows: correct 3,177, wrong 1, imprecise 22, misleading 1, unverified 6).
Scripts: `docs/reports/mm-games-L1-concepts-r2.py` (86 checks, exit 0), `-L2-` (72 checks, exit 1: the two failing checks are findings 4 and 6), `-L3-` (70 checks, exit 0). They rerun every Python solution against its examples and hidden tests, check that each starter fails, recompute every stated number by enumeration or exact arithmetic, replay the five trade games through the engine's pure game module, and run Monte Carlo checks for the empirical claims.

## Findings

Pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

1. `l1-unknown-quantity.json` | `screens[7].feedback.byKey.none`, `screens[7].explain.text` | imprecise | minor | Zero misses in 20 is stated as showing the ranges are too wide. | Under calibration zero misses in 20 has chance 0.9^20 = 0.122, which is not small. The course's own scorer (homework-1 `calibration_score`, 5% two-sided) returns `calibrated` for 20 hits in 20 (hidden test 10, p = 0.25). Screen 4 of the same lesson is careful at 7% ("a warning, not proof"); this screen is not at 12%. Basis: binomial pmf, L1 script check "l1 s7". | `feedback.byKey.none`: "Calibrated 90% ranges still miss about 1 time in 10. Never missing, round after round, means the ranges are too wide." `explain.text`: "A 90% range misses 10% of the time, so about 2 of 20 should miss. Missing none is a hint that the ranges are too wide, not proof. Zero misses in 20 happens by chance about 12% of the time."

2. `homework-1.json` | `items[5].feedback.generic`, `items[5].explain.text` | imprecise | minor | "Adding 100 makes 901" and "then add 100" read as the sum 900 + 100. | The digit sums of 0 to 99 add to 900 and the number 100 contributes its digit sum, 1. The key 9.01 is right (L1 script "homework-1 digit sum 9.01"). | `feedback.generic`: "Not quite right. Add the units digits and the tens digits of 1 to 99 separately, then add the 1 from 100." `explain.text`: "From 0 to 99, each digit appears 10 times in each place. So the digit sums add to $2 \times 10 \times 45 = 900$. The number 100 adds a digit sum of 1, so the fair value is $901/100 = 9.01$."

3. `l8-informed-flow.json` | `screens[4].explain.text` | imprecise | minor | "Narrowing gains less from random traders than it loses to informed ones" says narrowing gains something from random traders. In this toy it gains nothing: the random half trades at any width and pays the half-width, so narrowing earns less from them as well. | Table on the screen: random earnings fall 1, 0.75, 0.5 as the quote narrows while the informed loss rises 1/12, 1/6, 1/3 (L2 script "l8 s4"). The sentence describes real flow, which the next sentence then says the toy lacks. | "2 at 5 earns $0.75 - \tfrac16 = 0.5833$, and 2.5 at 4.5 earns $0.5 - \tfrac13 = 0.1667$. Here narrowing earns less from each random trader and loses more to informed ones. In this toy the random half trades at any width; real flow thins as you widen."

4. `homework-2.json` | `items[0].prose` | wrong | minor | "The hidden tests deal three seeded games." Four hidden tests call `make_script` (seeds 1, 2, 3 and 7). | L2 script check "homework-2 play: the prose says three seeded games" (stays failing). Homework-3's matching sentence says four and is right. | "Code the scripted card game end to end. The hidden tests deal four seeded games with `random.Random(seed)`, plus this homework's mock round and some edge cases. Each trade happens at the quote your rule gives for the fair value and position of that moment."

5. `homework-2.json` | `items[2].widget.answer` (order key) | imprecise | serious | The key accepts only information, skew, limit, quote. The limit check does not depend on the skew, so skew and limit in either order is a valid answer that is marked wrong. | The skew needs the fair value first (m = V − γq), and the quote comes last; nothing orders the limit check against the skew. The explanation gives no reason either. The `order` widget marks lines one by one, so a learner is told a correct line is misplaced. Basis: dependency of the steps; `docs/AUTHORING.md` section 3, `order`, `same`. | Add to the widget: `"same": [["skew", "limit"]]`. `feedback.correct`: "Information first, then inventory and the limit, then the quote." `explain.text`: "A trade first changes what the number is likely to be, so the fair value moves. Then the position sets the skew and the limit says how much more you can take, in either order. Only then can you quote."

6. `homework-2.json` | `items[5].widget.wrong[0]` (id `first`, value 20.8824), `items[5].feedback.byKey.first` | imprecise | minor | The slip value is 14 + 351/51. In this item no deck holds 351 points: 351/51 is the mean after a king, from lesson 9. The slip the feedback names (the mean after one card) is 361/51, giving 21.0784, and that value gets only the generic line. | After the 3 the deck holds 361 points in 51 cards; after the 3 and the jack, 350 in 50. L2 script check "homework-2 h-mock-fair-2 slip" (stays failing). | `wrong[0]`: `{ "id": "first", "value": 21.0784, "tol": { "abs": 0.001 } }`. `feedback.byKey.first`: "You used 361/51, the mean after the first card. Two cards have left the deck, so the last card averages 350/50."

7. `l10-position-limits.json` | `screens[5].title`, `screens[5].widget.options[3].why`, `screens[5].feedback.byKey.same`, `screens[5].explain.text`, `screens[10].explain.text`; `homework-3.json` | `items[10].explain.text` | imprecise | minor | "The edge per bet is the same" for £1, £10 and £20 stakes. By the course's own definition (lesson on edge: expected payout minus stake) the edge of a bet at 0.55 and evens is 0.1 times the stake: 10p, £1 and £2. What is equal is the win chance, or the edge per pound staked. | E = 0.55s − 0.45s = 0.1s. The ruin figures themselves are right (L3 script "l10 s5", exact and Monte Carlo). | `screens[5].title`: "Bigger stakes, same coin". `options[3].why` and `feedback.byKey.same`: "The edge per pound staked is the same, but the number of bets is not. Fewer bets give the edge less time." `screens[5].explain.text`, last sentence: "The win chance never changed, only the bet against the bankroll." `screens[10].explain.text`, last sentence: "The win chance is the same in each; the stake decides the ruin." `homework-3 items[10].explain.text`, second sentence: "The win chance is the same as with £1 bets, but there are fewer bets."

8. `l10-position-limits.json` | `screens[6].explain.text` | imprecise | minor | "Past it, the losses cost more in log terms than the wins add." As written this says growth is negative past f = 0.2. Growth stays positive up to about f = 0.39; only the marginal pound costs more than it adds. | At f = 0.3: 0.6 ln 1.3 = 0.157 against 0.4 |ln 0.7| = 0.143, so g = +0.015. g crosses zero near 0.389, and screen 7 of the lesson itself gives g(0.4) = −0.0024 (L3 script "l10 s6", "l10 s7"). Basis: Kelly (1956); Thorp (2006), section 2. | "Growth is highest at $f = 0.2$, where $g = 0.0201$ a bet. That is £20 of a £100 bankroll. Past it, each extra pound staked costs more in log terms on a loss than it adds on a win."

9. `l10-position-limits.json` | `screens[9].feedback.byKey.edge`, `screens[9].explain.text`, `screens[10].explain.text` | imprecise | minor | The same screen uses q for the position ("room to buy = L − q") and then writes Kelly as p − q with q meaning 1 − p, without saying so. | Notation clash inside one screen; the formula block itself uses 1 − p. | `feedback.byKey.edge`: "You halved the edge. At evens, $f^*$ is the whole edge $p - (1 - p)$, which is 0.1." `screens[9].explain.text`, first sentence: "At evens Kelly is $p - (1 - p) = 0.55 - 0.45 = 0.1$, a tenth of the bankroll." `screens[10].explain.text`, first sentence: "`kelly_stake` is $\max(0, p - (1 - p)/b)$ times the bankroll."

10. `l11-hedging.json` | `screens[3].prose` | imprecise | minor | "A hedge removes the share ρ² of A's variance." Only the minimum-variance hedge does. | Var(A − hB) = σ_A² + h²σ_B² − 2hρσ_Aσ_B equals σ_A²(1 − ρ²) only at h = ρσ_A/σ_B; at h = 2 on the same pair nothing is removed (the lesson's own quiz). Basis: Hull, *Options, Futures and Other Derivatives*, section 3.4; L3 script Monte Carlo. | "Back to the first pair, hedged at $h = 1.0$. The best hedge removes the share $\rho^2$ of A's variance. The share $1 - \rho^2$ is left."

11. `l11-hedging.json` | `quiz[3].explain.text` | imprecise | minor | "You now hold a short in B instead of a long in A." The book is still long £1 of A and short £2 of B. | A − 2B = (A − B) − B. A − B is the hedged residual (sd 1.2%), uncorrelated with B, and −B has sd 1.6%: √(1.44 + 2.56) = 2%. So the risk equals a net short of £1 of B plus A's own noise. | "At $h = 2$ the variance is $4 + 4 \times 2.56 - 2 \times 2 \times 0.8 \times 2 \times 1.6 = 4$. The sd is 2%, as with no hedge. In effect you now hold a net short of £1 of B, plus A's own noise."

12. `l13-full-game.json` | `quiz[0].question`, `quiz[0].widget.options[1]`, `quiz[0].widget.options[2].why` | imprecise | serious | "Why did the model take this trade?" with the distractor "For edge: 16 is below fair". The distractor is true: by the course's definition the buy at 16 against fair 17.08 had edge +1.08, and the `why` concedes it. A learner who picks it is marked wrong for a correct statement. | Edge of a purchase is fair minus price (lesson on edge). What the item means to ask is why the bid sat at 16 and not at 15, where the unskewed rule puts it (centre 17, width 4). Engine replay of the unskewed rule: bid 15 on turn 6, no fill (L3 script "l13 s5"). | `question`: "Why did the model's bid sit as high as 16?" `options[1].text`: "For edge alone: an unskewed bid would sit there too". `options[1].why`: "An unskewed bid would sit at 15, 2 below the rounded fair of 17. The short moved it up to 16." `options[2].why`: "The model cannot see what the interviewer knows. Its bid moved up because of the short."

13. `l13-full-game.json` | `quiz[0].explain.text` | misleading | minor | "Against the true 15 it lost £1, a fair price for halving the position." This grades the trade by its outcome and calls a trade with positive edge a cost. The level's own rule is to judge a trade at the fair value of its moment. | At fair 17.08 the buy at 16 had +1.08 of edge and cut the short; the −£1 against 15 is the last card's luck (the card was a 5 against a mean of 7.08). | "The bid was 16 because the centre moved up 1 for the short 2. That made the bid more likely to trade, buying back risk. At fair 17.08 the buy still had 1.08 of edge; the £1 lost against the true 15 was luck."

14. `homework-3.json` | `items[2].widget.answer` (order key) | imprecise | serious | The key accepts only position, bankroll, hedge, quote. The three checks are independent, so five other valid orders of them are marked wrong. | No check uses the result of another, and the explanation gives no reason for the order. Only "the quote comes last" and "leave out size by conviction" are forced. Basis: dependency of the steps; `docs/AUTHORING.md` section 3, `order`, `same`. | Add to the widget: `"same": [["pos", "bank", "hedge"]]`. `question`: "Put the three checks before the quote, and leave out the line that does not belong." `feedback.correct`: "The three risk checks, in any order, then the quote."

Findings by severity: wrong 1 (minor 1); imprecise 12 (serious 3, minor 9); misleading 1 (minor 1). Total 14.

The one `wrong`: homework-2 `items[0].prose` says the hidden tests deal three seeded games when four do.

## Unverified claims (not passes)

- U1. `l4-fermi.json` `screens[2].prose`: "Zhou's green book and Crack's *Heard on the Street* are full of them [Fermi estimates]." Crack's book has a chapter of estimation questions. I could not confirm any in Zhou's guide, whose chapters are brain teasers, calculus and linear algebra, probability, stochastic calculus, finance and algorithms. Suggested text: "Breaking a quantity into factors you can guess is a **Fermi estimate**. Crack's *Heard on the Street* has a chapter of them. Take the central guesses: 500 instruments, 20 fills each an hour, 8 hours."
- U2. `l3-how-wide.json` `screens[3].prose`: "Many interviewers set a rule: your width may be at most 2." A frequency claim with no source. Suggested: "An interviewer may set a rule".
- U3. `l3-how-wide.json` `screens[6].explain.text`: "Interviewers test both mistakes." No source.
- U4. `l9-cards-revealed.json` `screens[7].explain.text`: "Interviewers check this exact step." No source; the arithmetic in the line is correct.
- U5. `l12-thinking-aloud.json` `screens[5].widget.options[3].why`: "Many interviewers move on." No source.
- U6. `l12-thinking-aloud.json` `screens[9].prose`: "A real trader interview's first round often opens like this." No source; the trade arithmetic is correct.

The general claim that interviewers assess the reasoning as it is spoken is taken as correct on the basis of the firm guide the course cites (Jane Street, *Probability and Markets*).

## Notes on the new-text rule (learner text must not cite a lesson by number)

Not concept findings. All minor.

- N1. `l4-fermi.json` `screens[3].prose`: "This is the trick from Mental Maths Under Pressure, lesson 7." Fix: "This is the estimating-products trick from Mental Maths Under Pressure."
- N2. `l4-fermi.json` `screens[10].explain.text`: "Lesson 5 turns that into a two-sided price, and lesson 7 moves it after a trade." Fix: "The next level turns that into a two-sided price and moves it after a trade."
- N3. `l9-cards-revealed.json` `screens[4].explain.text`: "as lesson 7 showed". Fix: "Short 1, you might lean a little higher, as the skew rule says."
- N4. `l8-informed-flow.json` `quiz[0].feedback.generic`: "quote as in the first lesson of this level" (a lesson cited by position). Fix: "Not quite right. Without information, quote a plain two-sided market around the fair value."
- N5. `homework-3.json` `items[3].prompt`: "Replay lesson 13's game aloud". Fix: "Replay the full game from this level's last lesson aloud".

## What was checked with particular care and held

- Graded keys and slips: every numeric key, table cell, slider target, expression key and `wrong[]` value recomputed. No slip value is a correct answer under another valid method. The two order keys in findings 5 and 14 and the choice item in finding 12 are the only keys that reject a valid answer.
- Python: all 19 code widgets. Every solution passes its examples and hidden tests under plain Python 3, every starter fails, and every stated count of hidden tests matches. No solution looks ahead: `quote_path`, `quote_after_reveals`, `play` and `full_game` each quote from the position and the cards revealed before the fill, and `full_game` hedges before the first card turns. The model strategies in the two card games equal the stated rule (width 4, skew 0.5 a lot, centre rounded to 0.5) when replayed turn by turn with past information only.
- Fair value and edge: fair value is the expectation throughout (mean, not mode); edge is price minus fair for a sale and fair minus price for a purchase; a round trip earns the width. Signs of position (long positive) and P&L hold in every ledger.
- Card updates: F = S + (n − k)(T − S)/(N − k) holds by exchangeability and by Monte Carlo for all 13 first cards.
- Informed flow: the die-game losses, the mixed-flow averages and s = αδ hold exactly and by Monte Carlo. The break-even half-widths in homework-2 match an independent bisection.
- Limits, ruin and Kelly: room L − q and L + q; ruin 0.0178, 0.401, 0.45; f* = p − (1 − p)/b; growth 0.0150, 0.0201, −0.0024; median £273.68 and mean £711 after 50 bets.
- Hedging: h = ρσ_A/σ_B in pounds of B per pound of A with sds in per cent; residual σ_A√(1 − ρ²); the dice hedge has ratio 1; the over-hedge figures 2.68% and 2% hold.
- Trade games: the five games replayed through `app/js/engine/widgets/trade.js`. Fills, positions, cash and P&L match every sentence that describes the model, stale and unskewed runs.
- Real-world facts: Olympic pool 50 by 25 by 2 m; mile 1,609.344 m; 12-sided £1 coin 23.03 mm across the flats; 252 trading days of 8.5 hours.

## Overlap with earlier reads

Opened only after commit `51f1d6a5` (ledger, findings and scripts): `docs/reviews/review-mm-games.md` (second reader, with its fix pass), `docs/reviews/audit-mm-games-1-3.md` (audit round 1, its fix pass, the fix-pass read and its follow-up) and `docs/reports/audit-mm-games-1-3-ledger.md`. The round 1 concepts scripts and the author reports were not used.

Conceptual findings, levels 1 to 3:

| | Count | Which |
|---|---|---|
| Found by this audit only | 14 | Findings 1 to 14 |
| Found by earlier reads only | 35 | Review: 6 (as counted by audit round 1). Audit round 1: 25. Fix-pass read: 4. All 35 were fixed in the text before this read, so a blind read of the present text could not find them again. None of the 35 has come back: each of those places reads `correct` in the round 2 ledger, except l10 `screens[9].explain.text` (finding 9, below). |
| Found by both | 0 | |

`wrong` verdicts: this audit 1 (finding 4, minor), found by no earlier read. Earlier reads: 2 (audit round 1, findings 9 and 17, both fixed).

Where the reads touch:

- Finding 4 (homework-2 says three seeded games, four are dealt) is the sibling of fix-pass read finding 2, which fixed the same slip in homework-3 `items[0].prose` and did not look at homework-2.
- Finding 9 (q for 1 − p beside q for the position) sits in l10 `screens[9].explain.text`, a sentence the round 1 fix pass rewrote for its finding 19. The rewrite kept "p − q". So one finding of this round is in fix-pass text.
- Findings 1 and 7 are on rows the round 1 ledger marked `correct` (its rows for l1 `screens[7]` and l10 `screens[5]`).
- Findings 12 and 13 are in l13 `quiz[0]`. Round 1 finding 23 separated edge at the time from P&L at settlement across l13 and did not reach this quiz item.
- Lesson-number notes: N1, N2, N3 and N5 are also in round 1's "Noted, not conceptual" list and are still in the text (round 1 raised a validator rule instead of fixing them). N4 is new. The review's own fix for l9 `screens[4]` wrote "as lesson 7 showed", which is N3.
- Seen by round 1 and not by this audit: its note that l11 `screens[7]` gives an index future a daily sd of 4% against 2% for a single share, which is unrealistic (an index moves less than its members). The method and key are right. It is still in the text.
- New in this round and not conceptual findings: the six unverified claims U1 to U6. Round 1 softened one claim of the same kind (its finding 22) and removed two attributions (its finding 20). The seeded figures round 1 could not rebuild (l6 `screens[7]` seed 6, l8 `screens[6]` seed 4) reproduce with Python's `random.Random(seed).randint(1, 6)` (L2 script notes).

Miss rate of a single read, on this evidence: three earlier reads left 14 findings (3 serious, 11 minor), none of them a wrong graded number.

## Gates

Run on the worktree at commit `51f1d6a5`, content unchanged.

- `node tools/validate.mjs 2>&1 | tail -5` (from `app/`): 0 errors, 4137 warnings. `content/manifest.json` was not changed by the run.
- `python3 docs/reports/mm-games-3-perf-numbers.py`: 0 failures, exit 0. It is the only committed number script for the course whose name ends in `numbers.py`.
- `VOICE_BASE=app/content/courses/mm-games/ python3 docs/reviews/voice-scan.py 35`: 9,888 sentences scanned, 0 over 35 words, 0 explanations over three sentences.
- Playthroughs with `--local-cdn` (Pyodide 0.27.7 from the scratchpad `pkgs` folder), desktop and `--mobile`: lessons `l3-how-wide`, `l9-cards-revealed`, `l13-full-game`; sets `review-1`, `review-2`, `review-3`, `homework-1`, `homework-2`, `homework-3`. 18 of 18 runs "All passed", 0 browser relaunches.
- Round 2 concepts scripts: `mm-games-L1-concepts-r2.py` 86 checks, 0 failed, exit 0. `mm-games-L2-concepts-r2.py` 72 checks, 2 failed, exit 1 (findings 4 and 6; both stay failing until the content is fixed). `mm-games-L3-concepts-r2.py` 70 checks, 0 failed, exit 0 (needs `node` for the trade-game replays).
- Inbox: two bullets under "Raised later (audit mm-games round 2):" in `docs/BACKLOG-INBOX.md` (a validator rule for stated test counts; a validator warning for `order` keys with no `same` or `after`).
- No content, engine file, `course.json` or state file was changed.

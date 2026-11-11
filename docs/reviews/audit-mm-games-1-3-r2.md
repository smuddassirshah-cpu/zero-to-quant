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

## Fix pass

Fixer: Opus, own worktree, content commit `323619ba`. Each basis below was worked out independently (enumeration, exact arithmetic or reading the hidden tests); nothing was pasted from the findings unchecked. All 14 findings fixed, 0 disputed, 0 not applied; U1 to U6 and N1 to N5 all applied.

Graded keys, keyed option texts and slip values changed (listed explicitly):

- homework-2 `items[2].widget.after` added: `{"skew": ["info"], "requote": ["info", "skew", "limit"]}`. Recomputed by enumerating all 24 orders of the four lines against an independent dependency table (skew needs the fair value; the quote needs all three; the limit check needs only the position): exactly 3 valid orders, and the engine's `after` rule accepts exactly those 3 (info-skew-limit-requote, info-limit-skew-requote, limit-info-skew-requote). This is wider than the audit's `same [skew, limit]`, which would still reject limit-first.
- homework-3 `items[2].widget.after` added: `{"quote": ["pos", "bank", "hedge"]}`. Enumeration: 6 of 24 orders valid (the three checks in any order, quote last), the engine accepts exactly those 6.
- homework-2 `items[5].widget.wrong[0].value` 20.8824 to 21.0784 (id `first`): after the 3 the deck holds 364 − 3 = 361 points in 51 cards, and 14 + 361/51 = 21.0784; the key 21 = 14 + 350/50 is unchanged and outside the slip's tolerance.
- l13 `quiz[0]` options: `inv.text` "Its short: the skew lifted the bid to buy back risk" (correct, unchanged id); `edge.text` "For edge alone: an unskewed bid would sit at 16 too" (now false). Recomputed with the lesson's rule (width 4, skew 0.5 a lot, centre rounded to 0.5): unskewed centre round(17.08) = 17, bid 15; skewed centre round(18.08) = 18, bid 16. Buy at 16 against fair 17.08 has edge +1.08; the last card was 5, so the true value is 15.

Per finding:

1. fixed. Basis: P(0 misses in 20 | calibrated) = 0.9^20 = 0.1216, not small. l1 `screens[7].feedback.byKey.none`, `screens[7].explain.text`.
2. fixed. Basis: sum of digit sums over 1 to 100 = 901 by direct count; 100 contributes 1, not 100. homework-1 `items[5].feedback.generic`, `items[5].explain.text`.
3. fixed. Basis: random earnings 1, 0.75, 0.5 fall as the quote narrows; informed loss 1/12, 1/6, 1/3 rises. l8 `screens[4].explain.text` (middle sentence only).
4. fixed. Basis: the hidden tests call `make_script` with seeds 1, 2, 3 and 7: four games. homework-2 `items[0].prose`.
5. fixed (key, see above). homework-2 `items[2].widget.after`, `items[2].feedback.correct`, `.feedback.generic`, `.explain.text`.
6. fixed (slip value, see above). homework-2 `items[5].widget.wrong[0].value`, `items[5].feedback.byKey.first`.
7. fixed. Basis: edge of a stake s at 0.55 and evens is 0.55s − 0.45s = 0.1s, so 10p, £1, £2; the win chance is what is equal. Ruin rechecked: (r^20 − r^40)/(1 − r^40) = 0.0178, (r^2 − r^4)/(1 − r^4) = 0.401, 0.45, r = 9/11. l10 `screens[5].title`, `screens[5].widget.options[3].why`, `screens[5].feedback.byKey.same`, `screens[5].explain.text`, `screens[10].explain.text`; homework-3 `items[10].explain.text`.
8. fixed, with my own wording. Basis: g(f) = 0.6 ln(1 + f) + 0.4 ln(1 − f); g(0.3) = +0.0147, g(0.4) = −0.0024, root by bisection 0.3894. New sentence: growth falls past 0.2 and turns negative near f = 0.39. l10 `screens[6].explain.text`.
9. fixed: one notation, q for the position only, 1 − p for the losing chance. l10 `screens[9].feedback.byKey.edge`, `screens[9].explain.text`, `screens[10].explain.text`. The `kelly_stake` solution already uses `1 - p`.
10. fixed. Basis: Var(A − hB) is minimised at h = ρσ_A/σ_B = 1.0 with residual σ_A²(1 − ρ²); any other h leaves more. The text now names the minimum-variance hedge (the term the previous screen defines). l11 `screens[3].prose`.
11. fixed. Basis: A − 2B = (A − B) − B; residual sd 1.2%, uncorrelated with B; 1.44 + 2.56 = 4. l11 `quiz[3].explain.text`.
12. fixed (option texts, see above). l13 `quiz[0].question`, `options[inv].text`, `options[edge].text` and `.why`, `options[info].why`, `options[limit].why`, `feedback.correct`.
13. fixed. Basis: the level judges a trade at the fair value of its moment; +1.08 of edge at the time, −£1 at settlement from a 5 against a mean of 7.08. l13 `quiz[0].explain.text`.
14. fixed (key, see above). homework-3 `items[2].widget.after`, `items[2].feedback.correct`, `items[2].explain.text`. The question was left as it was, so the item does not announce that the order of the checks is free.

Unverified claims: U1 fixed by removing both book attributions (I cannot confirm Fermi questions in either book) and naming the source of the term instead, Enrico Fermi, l4 `screens[2].prose`. U2 "An interviewer may set a rule", l3 `screens[3].prose`. U3 "Avoid both mistakes.", l3 `screens[6].explain.text`. U4 "Remove both kings, not one: that is the step to check.", l9 `screens[7].explain.text`. U5 "An interviewer may simply move on", l12 `screens[5].widget.options[3].why`. U6 "A market-making round can open like this.", l12 `screens[9].prose`.

Lesson-number notes: N1 l4 `screens[3].prose` (course named, lesson number dropped; that course's l7 is "Estimating products"); N2 l4 `screens[10].explain.text` ("The next level", which holds the two-sided and skewing lessons); N3 l9 `screens[4].explain.text` ("the skewing lesson"); N4 l8 `quiz[0].feedback.generic`; N5 homework-3 `items[3].prompt`. Also fixed: homework-3 `items[0].prose` "level 2's scripted engine" now "the scripted card game you coded in the quoting homework", and l13 `screens[0].explain.text` "level 2's skew" now "the same inventory skew as before". A grep of levels 1 to 3 finds no remaining "lesson N" or "level N" in learner text.

No hidden test, rubric row or code solution changed. No check script needed updating.

Gates after the fix (worktree at `323619ba`):

- `node tools/validate.mjs`: 0 errors, 4137 warnings (the same count as before the fix; two new under-20-word warnings from first drafts were removed by shortening the sentences). `content/manifest.json` unchanged.
- Concepts scripts: L1 r2 86 checks 0 failed, L2 r2 72 checks 0 failed (findings 4 and 6 now pass), L3 r2 70 checks 0 failed; round 1 L1 79, L2 76, L3 69 checks, 0 failed; `mm-games-3-perf-numbers.py` 0 failures. All exit 0, no script edited.
- `VOICE_BASE=app/content/courses/mm-games/ python3 docs/reviews/voice-scan.py 35`: 9,897 sentences, 0 over 35 words, 0 explanations over three sentences. No em-dash, exclamation mark or lesson number in the added text.
- Playthroughs with `--local-cdn`, desktop and `--mobile`: lessons l1, l3, l4, l8, l9, l10, l11, l12, l13 and sets homework-1, homework-2, homework-3. 24 of 24 "All passed", 0 browser relaunches.

For the fix-pass read: the two `after` keys are wider than the audit proposed for homework-2 (limit-first is also accepted), and U1 replaces the book attribution with the origin of the term rather than keeping Crack.

## Fix-pass read

Blind read of `git diff 323619ba~1 323619ba -- app/content/courses/mm-games` by a fresh reader who has not seen the audit, its ledgers or the reviews. The commit touches 12 files (l1, l3, l4, l8 to l13, homework-1 to 3; no review file changed), 53 changed JSON leaves. Each changed string was read with its whole screen or item. Numbers were recomputed in Python; the two `order` keys were enumerated over all 326 arrangements (every ordered subset of the five lines) with a port of `orderOk` and `late` from `app/js/engine/widgets/order.js` (`after` set, no `same`, so the rule is: exactly the four answer lines, each after all its named predecessors).

| # | file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|---|
| 1 | homework-1 | items[5].feedback.generic | Add units and tens digits of 1 to 99, then the digit sum of 100 | correct | Derivation: digits 0 to 99 sum to 2 × 10 × 45 = 900; 100 adds 1; 901. |
| 2 | homework-1 | items[5].explain.text | 100 adds its digit sum of 1; fair value 901/100 = 9.01 | correct | Same derivation: 900 + 1 = 901, over 100 equally likely draws. |
| 3 | homework-2 | items[0].prose | Hidden tests deal four seeded games, plus the mock round and edge cases | correct | Counted `tests`: `make_script` seeds 1, 2, 3, 7 (four), the mock script (sell 2, 3, buy 1, 11, 9), four edge cases; 9 in all, matching `how`. |
| 4 | homework-2 | items[2].widget.after | skew after info; requote after info, skew, limit | correct | Enumeration: 3 of 326 accepted (info-skew-limit-requote, info-limit-skew-requote, limit-info-skew-requote). Under the course rule m = F − γq (l12 screens[7]) these are exactly the valid orders: 0 valid rejected, 0 invalid accepted. `answer` satisfies the rules. |
| 5 | homework-2 | items[2].feedback.correct | Fair value before skew, quote last, limit check anywhere before the quote | correct | Matches the key as the engine applies it (row 4). |
| 6 | homework-2 | items[2].feedback.generic | Fair value before the skew; the quote last | correct | Matches the key; l12 screens[7] says F, then q, then m. |
| 7 | homework-2 | items[2].explain.text | "The skew is set from that fair value and the new position" | imprecise | m = F − γq: the size of the skew, γq, depends on the position alone; only the skewed centre needs F. See finding 1. The other two sentences are correct. |
| 8 | homework-2 | items[5].widget.wrong[0].value | Slip 21.0784 | correct | Key: 14 + (364 − 14)/50 = 21. Slip: 14 + 361/51 = 21.0784, the last card priced at the deck mean after the first card only (the jack not removed). A real slip (361/51 is the per-card mean of the step before), outside the key's tolerance, and not an answer under any valid method. |
| 9 | homework-2 | items[5].feedback.byKey.first | Used 361/51; two cards have left, so the last card averages 350/50 | correct | (364 − 3)/51 = 361/51; (364 − 14)/50 = 7. |
| 10 | homework-3 | items[0].prose | Extends the card game coded in the quoting homework; four seeded scripts and edge cases | correct | Level 2 is named "Quoting" in `course.json` and its homework item 0 is `play`. Counted `tests`: seeds 1, 2, 3, 7 (four) and four edge cases; 8, matching `how`. |
| 11 | homework-3 | items[2].widget.after | quote after pos, bank, hedge | correct | Enumeration: 6 of 326 accepted, the six orders of the three checks followed by the quote. The checks are independent (limit room, bankroll against stake, hedge availability), so those six are exactly the valid orders: 0 valid rejected, 0 invalid accepted. |
| 12 | homework-3 | items[2].feedback.correct | Three risk checks in any order, then the quote | correct | Matches row 11. |
| 13 | homework-3 | items[2].explain.text | No check needs another's answer, so any order works; quote last | correct | Each check reads a different input (position, bankroll, hedge market); agrees with `feedback.generic`. |
| 14 | homework-3 | items[3].prompt | The full game is in this level's last lesson | correct | `course.json`: level 3 ends with l13 "A full game with a partner"; cards 4, 6, 5, width 4, limit 3, skew 0.5 match l13. |
| 15 | homework-3 | items[10].explain.text | Win chance the same as with £1 bets, fewer bets; ruin 1.8% to 40.1% | correct | Gambler's ruin (Feller vol. 1, ch. XIV): r = 9/11, (r² − r⁴)/(1 − r⁴) = 81/202 = 0.40099; £1 stakes 0.01775. |
| 16 | l1 | screens[7].feedback.byKey.none | Never missing, round after round, is the sign of ranges too wide | correct | A hit rate above p over many rounds is over-wide by the screen's own definition of calibration. |
| 17 | l1 | screens[7].explain.text | Missing none hints at too wide but is not proof; chance about 12% | correct | 0.9^20 = 0.1216. |
| 18 | l3 | screens[3].prose | An interviewer may set a width rule | correct | Hedged statement of possibility; 6 to 8 spans three totals. |
| 19 | l3 | screens[6].explain.text | "Avoid both mistakes." | correct | Instruction, no claim; agrees with the two distractor lines. |
| 20 | l4 | screens[2].prose | The name Fermi estimate comes from the physicist Enrico Fermi, known for such guesses | correct | Standard attribution: Fermi's Trinity blast-yield estimate and his "piano tuners in Chicago" classroom problems (Weinstein and Adam, *Guesstimation*, introduction). |
| 21 | l4 | screens[3].prose (sentence 3) | The estimating-products trick is in Mental Maths Under Pressure | correct | `mental-pressure/course.json`: the course name matches and l7 is "Estimating products". No lesson number cited. |
| 22 | l4 | screens[3].prose (sentence 1, unchanged, inside the changed string) | "Interviewers want the order of magnitude first." | unverified | A generalisation about all interviewers with no source; the same commit hedged the like lines in l3 and l12. See finding 2. |
| 23 | l4 | screens[10].explain.text | The next level gives a two-sided price and moves it after a trade | correct | `course.json` level 2: l5 "A two-sided price", l7 "Moving after a trade". |
| 24 | l8 | screens[4].explain.text | Narrowing earns less from each random trader and loses more to informed ones | correct | Half-width 2, 1.5, 1; informed loss 1/6, 1/3, 2/3 on a die; averages 0.9167, 0.5833, 0.1667 recomputed. |
| 25 | l8 | quiz[0].feedback.generic | Without information, quote a plain two-sided market around fair | correct | Agrees with the key (3 at 4 around 3.5) and the explain. |
| 26 | l9 | screens[4].explain.text | Short 1, lean a little higher, as the skewing lesson showed | correct | m = F − γq with q = −1 raises the centre; l7 teaches the skew (38 uses of the word). |
| 27 | l9 | screens[7].explain.text | Remove both kings, not one; 338/50 = 6.76, fair 32.76 | correct | 364 − 26 = 338; 26 + 6.76 = 32.76. |
| 28 | l10 | screens[5].title | "Bigger stakes, same coin" | correct | p = 0.55 at every stake on the screen. |
| 29 | l10 | screens[5].widget.options[3].why | Edge per pound staked is the same; the number of bets is not | correct | Edge per £1 at evens is 2p − 1 = 0.1 at any stake; edge per bet scales with the stake. |
| 30 | l10 | screens[5].feedback.byKey.same | Same text as row 29 | correct | As row 29. |
| 31 | l10 | screens[5].explain.text | Ruin 1.8%, 40.1%, 45%; the win chance never changed, only bet size against bankroll | correct | Ruin formula: 0.01775, 0.40099, 0.45. |
| 32 | l10 | screens[6].explain.text | Peak g = 0.0201 at f = 0.2; growth falls past it, negative near f = 0.39 | correct | g(f) = 0.6 ln(1 + f) + 0.4 ln(1 − f): g(0.2) = 0.020136; root by bisection at f = 0.3894 (Kelly 1956). |
| 33 | l10 | screens[9].feedback.byKey.edge | At evens f* is the whole edge p − (1 − p) = 0.1 | correct | f* = p − (1 − p)/b with b = 1. The screen now uses q only for position. |
| 34 | l10 | screens[9].explain.text | Kelly at evens is 0.55 − 0.45 = 0.1 | correct | As row 33. |
| 35 | l10 | screens[10].explain.text | `kelly_stake` is max(0, p − (1 − p)/b) times bankroll; win chance the same in each run | correct | Matches the solution code and the three `ruin_sim` tests (p = 0.55). |
| 36 | l11 | screens[3].prose | h = 1.0 is the minimum-variance hedge; it removes ρ² of A's variance and any other h removes less | correct | Hull, *Options, Futures and Other Derivatives*, ch. 3 (minimum variance hedge ratio): h* = ρσA/σB = 0.8 × 2/1.6 = 1; variance left (1 − ρ²)σA². |
| 37 | l11 | quiz[3].explain.text | At h = 2 you are in effect net short £1 of B plus the part of A that B cannot hedge | correct | A = 1.0·B + e with e uncorrelated with B, var(e) = 1.44; A − 2B = −B + e; variance 2.56 + 1.44 = 4. |
| 38 | l12 | screens[5].widget.options[3].why | An interviewer may simply move on | correct | Hedged possibility; no generalisation. |
| 39 | l12 | screens[9].prose | A market-making round can open like this | correct | Hedged possibility; short 3 at 8 against fair 7 is +£3. |
| 40 | l13 | screens[0].explain.text | Same inventory skew as before; 19.5 at 23.5 | correct | Centre 21 − 0.5 × (−1) = 21.5, ± 2. |
| 41 | l13 | quiz[0].question | Why did the bid sit as high as 16 | correct | Lesson rule: centre = fair − 0.5q rounded to 0.5, width 4. Skewed: 17.08 + 1 = 18.08, rounds to 18, bid 16, ask 20. Unskewed: 17.08 rounds to 17, bid 15. |
| 42 | l13 | quiz[0].widget.options[0].text | Key: the short, through the skew, lifted the bid | correct | Row 41: 16 against 15. Uniquely right. |
| 43 | l13 | quiz[0].widget.options[1].text and .why | Distractor: an unskewed bid would be 16 too. Why: it would be 15, 2 below the rounded fair of 17 | correct | The option is false and the why is exact (row 41). |
| 44 | l13 | quiz[0].widget.options[2].why | The model cannot see what the interviewer knows; the bid moved for the short | correct | The quoting rule takes fair and position only; the option is false as a reason for the bid. |
| 45 | l13 | quiz[0].widget.options[3].why | Short 2 was inside the limit of 3; the skew moved the bid | correct | Limit 3 in l13; the limit does not enter the centre. |
| 46 | l13 | quiz[0].feedback.correct | The short lifted the bid | correct | Row 41. |
| 47 | l13 | quiz[0].explain.text | Centre up 1 for short 2, bid 16 not 15; 1.08 of edge at fair 17.08; £1 lost against the true 15 was the last card | correct | 17.08 − 16 = 1.08; cards 4, 6, 5 sum to 15, so the buy at 16 lost £1; the last card was 5 against a mean of 7.08. Agrees with l13's "Turn 6 was an inventory trade" and homework-3's rubric step +9.34 to +10.42. |

Verdict counts: 47 rows. correct 45, wrong 0, imprecise 1, misleading 0, unverified 1.

Other checks, all clean on the changed strings: British English; no exclamation marks; no em-dashes; longest changed sentence 22 words; every changed explanation has at most three sentences; no lesson or level cited by number ("the next level", "this level's last lesson", "the quoting homework", "the skewing lesson"). Notation: after the change l10 uses q only for position (L − q, L + q) and writes the losing chance as 1 − p throughout; no symbol is used for two things in any changed screen.

Recomputations asked for:
- homework-2 `items[2]`: 3 orders accepted of 326 arrangements; no valid order rejected and no invalid order accepted under m = F − γq. If "skew" is read as only the shift γq, the three orders with skew before info give the same quote and are rejected; finding 1 fixes the wording so the key's reading is the stated one.
- homework-3 `items[2]`: 6 orders accepted of 326; exactly the valid set.
- homework-2 `items[5]`: key 21 = 14 + 350/50. `wrong[0]` 21.0784 = 14 + 361/51 is a real slip (jack not removed from the deck) and not correct under any valid method.
- l13 `quiz[0]`: unskewed bid 15, skewed bid 16, edge 1.08; the keyed option is right and uniquely right, each distractor is false, and the explain agrees.
- Seeded games: homework-2 has four (seeds 1, 2, 3, 7) of 9 tests; homework-3 has four of 8.

Findings:

1. homework-2.json | items[2].explain.text | imprecise | minor | The second sentence says the skew is "set from that fair value". The size of the skew depends on the position alone; it is the skewed centre that needs the fair value. As written the reason for marking skew-before-information wrong is loose. | m = F − γq (l12 screens[7]); enumeration shows the three skew-before-info orders are rejected, which is right only on the skewed-centre reading. | Replace the explain text with: "A trade first changes what the number is likely to be, so the fair value moves. The skewed centre is that fair value moved for the new position, short 3, so it comes second. The limit check needs only the position, so it can come anywhere before the quote, which goes last."

2. l4-fermi.json | screens[3].prose | imprecise | minor | "Interviewers want the order of magnitude first" is an unsourced generalisation about all interviewers, left in a string this commit edited; the like lines in l3 and l12 were hedged. Ledger verdict `unverified`. | No source in the lesson; the lesson summary already gives it as advice ("say the power of ten first"). | Replace the prose with: "Say the order of magnitude first. Round each factor to one significant figure and count powers of ten: $5 \\times 10^2$, $2 \\times 10^1$ and $8$. This is the estimating-products trick from Mental Maths Under Pressure." (in the JSON the backslashes stay doubled as shown).

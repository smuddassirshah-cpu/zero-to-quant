# Concept audit: mm-games level 4 (blind)

Scope: `l14-quoting-an-interval`, `l15-arbitrage-in-a-book`, `l16-several-contracts`, `l17-options-on-a-game`, `l18-betting-board`, `review-4`, `homework-4`. Stage 3, full ledger.

Written blind: the ledger and the findings below were committed before `docs/reviews/review-mm-games.md`, `docs/reports/mm-games-4.md` or any earlier audit file was opened.

- Ledger: `docs/reports/audit-mm-games-4-ledger.md`, 908 rows: correct 874, wrong 1, imprecise 30, misleading 0, unverified 3.
- Concepts script: `docs/reports/mm-games-L4-concepts.py`, 293 checks pass, 1 fails (finding 1), 10 notes (the counterexamples behind findings 2 to 11). It exits 1 until finding 1 is fixed.
- Every graded key and every slip value was recomputed. No key is wrong. No slip value is right under an alternative method. One choice option is defensible under the lesson's own test (finding 4).
- All seven code solutions pass their hidden tests and every starter fails them. Two solutions test a narrower condition than the word they teach (findings 2 and 3).
- The trade screens were replayed through `trade.js` `play()`. Every model-run and opening-quote figure in the explains matches the engine.

What the level gets right, since the brief asks for it: arbitrage is taught as riskless on every outcome and is set against a merely positive expected value (l15 trap, l16 and l17 ledgers). Odds are fractional throughout, with implied chance $1/(o+1)$. Parity is stated with its no-discounting condition each time. The interval score is the standard one and its weight $2/\alpha$ is named.

## Findings

Pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

1. `review-4.json` | `items[2].explain.text` | wrong | minor | The last sentence says "Five more units of width would have saved 90." The range it has just named, 90 to 140, is ten units wider than 100 to 140. | Scores: 100 to 140 on 95 is 140; 90 to 140 is 50, a saving of 90 for ten more units; 95 to 140 (five more units) is 45, a saving of 95. Concepts script section 7 fails on this line. Basis: the interval score as the lesson defines it. | Replace the last sentence with: `Ten more units of width would have saved 90.`

2. `l15-arbitrage-in-a-book.json`, `l16-several-contracts.json`, `homework-4.json` | l15 `screens[9].prose`, `summary.ideas[0]`, `summary.trap`, `screens[6].hints[0]`, `screens[6].hints[1]`, `screens[6].explain.text`; l16 `screens[10].prose`, `screens[10].widget.how`, `screens[10].explain.text`; homework-4 `items[2].widget.lines[4].why` and `items[2].feedback.byKey.trade` | imprecise | serious | Arbitrage is defined as trades "whose payoffs cancel on every outcome, with money left over", and the trap says an arbitrage "needs both". That is one kind of arbitrage, given as the definition. The standard definition is wider: a position that cannot lose on any outcome and gains on at least one. A learner taught that the legs must cancel will deny real arbitrages, such as an option quoted outside its bounds, which the prerequisite options level teaches. | Bjork, *Arbitrage Theory in Continuous Time*, ch. 2: zero cost, never negative, positive with positive chance. Hull, ch. 11, option bounds are arbitrages whose payoffs do not cancel. Counterexample in the lesson's own code (concepts script section 6): selling L, which pays at most 3, at a bid of 3.2 gains at least 0.20 on every face, yet `find_arb` returns 0 and the explain says a combination "that leaves a face exposed returns 0, however good its cash". | The fix is wording on six strings; the code and its tests can stay, labelled as the cancelling kind. Paste-ready text: (a) l15 `screens[9].prose`, first sentence: `An arbitrage is a set of trades that cannot lose on any outcome and leaves money over. The simplest kind has payoffs that cancel on every outcome, with cash left.` (b) l15 `summary.ideas[0]`: `An arbitrage cannot lose on any outcome and leaves money over. The simplest kind has payoffs that cancel, with cash left.` (c) l15 `screens[6].hints[0].text`: `A cancelling arbitrage needs two things. Check each plan for both.` (d) l15 `screens[6].explain.text`, last sentence: `This kind of arbitrage needs both: legs that cancel on every outcome, and money in.` (e) l15 `summary.trap`: `Calling a trade arbitrage when a leg is missing or the cash is negative: it must be unable to lose.` (f) l16 `screens[10].prose`, second sentence: `Then check whether a combination locks the same profit on every face.` (g) l16 `screens[10].explain.text`, last sentence: `The check returns 0 when a face is left exposed, so it finds only arbitrages whose payoffs cancel.` (h) homework-4 `items[2].widget.lines[4].why` and `items[2].feedback.byKey.trade`: `Trading before checking can leave a leg open. A gap is only an arbitrage once no face can lose.`

3. `l15-arbitrage-in-a-book.json`, `review-4.json` | l15 `screens[9].prose`, `screens[7].prose`, `summary.ideas[2]`, `screens[10].widget.starter` and `.solution` (docstring of `book_arb`); review-4 `items[4].prose` | imprecise | serious | The board rule is stated for "exclusive outcomes". It also needs one of the listed outcomes to happen. `screens[5]` says "Exactly one of them happens"; the general statement, the summary, the code docstring and the review item drop it. With three runners of a larger field the implied chances can sum below 1 with no arbitrage. | Derivation: stakes $1/(o_i+1)$ return 1 only if a listed outcome occurs; on an unlisted outcome the 2, 3 and 4 to 1 board loses all £47 (concepts script section 2 note). Basis: de Finetti's Dutch-book argument is over a partition, that is exclusive and exhaustive events. | (a) l15 `screens[9].prose`: replace `on exclusive outcomes, it exists when` with `on outcomes of which exactly one happens, it exists when`. (b) l15 `screens[7].prose`: `Another bookmaker offers evens, 2 to 1 and 5 to 1 on three outcomes. Exactly one of them happens.` (c) l15 `summary.ideas[2]`: `When exactly one outcome happens, implied chances totalling below 1 lock a profit. Exactly 1 is fair; above 1 is the overround.` (d) `book_arb` docstring, first line, in starter and solution: `"""odds: list of o for o-to-1 bets; exactly one outcome happens.` (e) review-4 `items[4].prose`: `A bookmaker offers evens, 4 to 1 and 4 to 1 on three outcomes. Exactly one of them happens.`

4. `l16-several-contracts.json` | `screens[2].widget.options[2]` (`skewE`) with its `why` and `feedback.byKey.skewE` | imprecise | minor | The question asks which set is "consistent", and the explain tests consistency by whether any combination can be traded through. Option `skewE` (E 2.3 to 2.7) also passes that test: its bids for E and F total 3.6, below the A ask of 3.7, and its asks total 4.4, above the A bid. It is off fair and loses on average, as its `why` says, but it is not inconsistent in the lesson's sense. | Concepts script section 3: `no_arb_three` is true for the key and for `skewE`, false for `evens` and `same`. | Make the option break the family, so one test covers all three wrong sets. Option text: `A 3.3 to 3.7, E 2.5 to 2.9, F 1.3 to 1.7`. `why` and `feedback.byKey.skewE`: `Your E sits 0.7 above fair. The interviewer sells you E at 2.5 and F at 1.3, buys A at 3.7 and locks 0.10 a set.` Basis: 2.5 + 1.3 − 3.7 = 0.10, flat on every face.

5. `l18-betting-board.json`, `review-4.json` | l18 `screens[4].explain.text`, `summary.ideas[1]`; review-4 `items[9].explain.text` | imprecise | minor | Scaling every Kelly stake by the same factor under a cap is presented as the method, with "the mix Kelly chose" kept. Under a binding cap the growth-optimal mix changes: it trims the low-edge bet most. Equal scaling is a simple and common rule, not the optimum. The keys are right for the rule as instructed. | Concepts script section 5: maximising expected log growth for a, b, d with £30 at risk on £100 gives about £6.03, £7.82, £16.15 (growth 0.03259) against 0.03240 for £7.50, £7.50, £15. Basis: Kelly (1956) objective with a budget constraint; Thorp (2006), section 7. | l18 `screens[4].explain.text`, replace the last sentence with: `It is a simple rule, close to the best capped mix, which trims bet a a little more.` l18 `summary.ideas[1]`: `When the stakes break the limit, a simple rule scales them all alike: £40 capped at £30 means 0.75 of each.` review-4 `items[9].explain.text`, last sentence: `Equal scaling keeps the mix the same under the cap.` (no change needed if the l18 line is fixed).

6. `l17-options-on-a-game.json` | `screens[8].explain.text` | imprecise | minor | "A short straddle earns small sums often and loses large ones rarely" is the market intuition, and it does not hold on this game. Sold at 2.0, the straddle gains on 16 of 36 rolls (2 or 1), breaks even on 8, and loses on 12 (1, 2 or 3). | Enumeration, concepts script section 4. | Replace the last sentence with: `A short straddle keeps most of its premium near 7 and owes most at the extremes.`

7. `l17-options-on-a-game.json` | `quiz[0].explain.text` | imprecise | minor | "Strikes far from 7 are cheap." True for options out of the money only. The next quiz item prices the 2-call at 5. | Enumeration: 2-call 5, 12-put 5 (concepts script section 4). | Replace with: `Calls far above 7 and puts far below it are cheap.`

8. `l15-arbitrage-in-a-book.json` | `quiz[1].explain.text` (and "above 1 is the margin" in `summary.ideas[2]`, covered by fix 3c) | imprecise | minor | The excess of the implied chances over 1 is called the overround. "The bookmaker's margin" also names the share of stakes the bookmaker keeps on a balanced book, which here is 1/13, not 1/12. | Stakes 13 return 12 on a balanced book: margin on turnover 1 − 12/13 = 1/13; overround 13/12 − 1 = 1/12. Basis: standard betting usage, for example Cortis (2015), *Journal of Prediction Markets* 9(1). | Replace the last sentence with: `The excess, 1/12, is called the overround.`

9. `l15-arbitrage-in-a-book.json` | `screens[8].feedback.byKey.rev` (slip value −12) | imprecise | minor | "You went round the other way" does not produce −12. The reverse loop is not quoted; at reciprocal rates it would give −£11.86. The slip is a sign error. | $1000/1.012 - 1000 = -11.86$ (concepts script section 2). | `You have the sign reversed. The loop ends above £1,000, so the profit is positive.`

10. `l14-quoting-an-interval.json` | `summary.ideas[2]` | imprecise | minor | "a calibrated set does that only 1.3% of the time", where "that" is six hits in ten. Exactly six has chance 1.1%; 1.3% is six or fewer, as `screens[6]` and `screens[7]` say. | Binomial(10, 0.9): P(6) = 0.0112, P(≤ 6) = 0.0128. | `Six hits in ten says the ranges are too narrow: a calibrated set scores six or fewer only 1.3% of the time.`

11. `l14-quoting-an-interval.json` | `screens[11].explain.text` | imprecise | minor | "More misses mean the sd was set too low." A calibrated range misses on four or more of 21 days with chance 0.15, and a mean that is off adds misses too. | Binomial(21, 0.1) tail, concepts script section 1. | Replace the last sentence with: `Many more misses suggest the sd was set too low, or the mean was off.`

12. `l14-quoting-an-interval.json`, `l18-betting-board.json` | l14 `screens[11].prose`, l14 `screens[7].explain.text`, l18 `screens[11].explain.text` | imprecise | minor | Three real-world statements are `unverified`. (a) "A trader's battery often has an intervals paper, and desks do the same each morning. The free guide *Probability and Markets* ... treats ranges this way." I could not open the guide, and "this way" reads as the interval score, which I doubt it uses. (b) "six or seven hits in ten is a common report": overconfidence in interval estimates is well documented, but I could not source this figure. (c) "Desks do this by rule, not by feel." | Hosts other than jsDelivr were unreachable. Known literature: Alpert and Raiffa (1982) and Russo and Schoemaker (1992) report hit rates far below the stated level. | Either a human confirms each line, or use: (a) `Trading interviews often ask for 90% ranges, and a desk can make the same range each morning. Your belief for today's close: mean £102.40, sd £1.20.` (b) `Candidates often give ranges that are too narrow, with hit rates well below nine in ten.` (c) `Many desks set this by rule, not by feel.`

### Project-rule notes (not concept findings)

A. `l16-several-contracts.json` | `screens[11].explain.text` | "Lesson 17 plays this on dice." cites a lesson by number. Suggested: `The next lesson plays this on dice.`

B. `l17-options-on-a-game.json` `screens[3].prose` and `homework-4.json` `items[3].prose` ask for a skew of 0.05 per unit on a 0.1 tick. The model strategies follow it to the nearest tick, so no finding.

## Overlap with the earlier review

Read after commit `a9cadaa8`: `docs/reviews/review-mm-games.md` (Level 4 section and Fix pass items 24 to 30) and `docs/reports/mm-games-4.md`.

The earlier review raised seven Level 4 findings. Two are conceptual: the l16 `screens[2]` option `same` line ("E and F pay less than A on every face", false) and the l18 `screens[11]` slip `cut` line (reasoning that did not give the stored value). Both were fixed before this audit, and the fixed text is `correct` in the ledger. The other five are mechanical (tolerances that touch, a missing unit, a caption letter, a stale word, table widths).

| Conceptual findings | Count | Which |
|---|---|---|
| Found by this audit only | 12 | findings 1 to 12 (1 wrong, 11 imprecise; 2 serious) |
| Found by the earlier review only | 2 | l16 `same` why; l18 `cut` feedback (both already fixed, so not visible to a later read) |
| Found by both | 0 | |

The earlier read checked numbers and wording and found no definitional gap. The two serious findings here (the definition of arbitrage, and the missing "one outcome must happen") are of the kind a number check cannot see. The author report's joint-Kelly figures (about 0.094, 0.095, 0.195) agree with this audit's gradient-ascent result.

## Gates

Run on branch `worktree-agent-a3943be3d29330bd0`, content unchanged.

- Validator (`node tools/validate.mjs`, from `app/`): 0 errors, 4,137 warnings. The manifest was not changed.
- Concepts script `docs/reports/mm-games-L4-concepts.py`: exit 1. 293 checks pass, 1 fails (finding 1, review-4 `items[2].explain`), 10 notes. It exits 0 once finding 1 is fixed.
- Number scripts: no committed script named for level 4. The course's one number script, `docs/reports/mm-games-3-perf-numbers.py`, exits 0 (0 failures).
- Voice scan (`VOICE_BASE=.../mm-games/ python3 docs/reviews/voice-scan.py 35 --summary`): 0 sentences over 35 words, 0 explanations over three sentences, 9,888 sentences scanned.
- Playthrough with `--local-cdn`, desktop: all passed. l14 16 checks, quiz 4/4; l15, l16, l17, l18 15 checks each, quiz 3/3; review-4 10 of 10 recorded; homework-4 9 of 9 right, 40 of 40 marks.
- Playthrough with `--local-cdn --mobile`: all passed, same counts.
- Trade games replayed through `app/js/engine/widgets/trade.js` `play()`: strategy and opening-quote runs match every explain (l14 0 and −200; l15 +0.80; l16 +0.70 and −5.40; l17 +1.70; review-4 0 and −160; homework-4 +1.80).
- Engine limits: none found. No bullet added to `docs/BACKLOG-INBOX.md`.

Proposed fixes were checked against the voice gate by hand: all under 35 words, no exclamation marks or em-dashes. In fix 5, "bet a a little more" is intended: the first "a" is the bet's name.

## Fix pass

Fixer: Opus, content commit `6bc15e4e`. Each basis below was established independently (derivation or a run of code in `scratchpad/chk.py` and `scratchpad/hw.py`, outside the repo), not taken from the audit.

Definition used for arbitrage: the standard one (Björk, *Arbitrage Theory in Continuous Time*; Delbaen and Schachermayer): a set of trades that cannot lose on any outcome and gains on at least one, counting the cash. Trades whose payoffs cancel, with money left over, are taught as the plainest kind. The two code widgets now return the profit locked on the worst face, which finds every sure-profit arbitrage; a weak one (zero on some faces, never negative) still returns 0, and the text never says 0 means "no arbitrage".

1. **fixed.** Basis: interval score width + 20 × miss; 100 to 140 on 95 scores 140, 90 to 140 scores 50 (10 more units, saving 90); 95 to 140 scores 45. `review-4.json` `items[2].explain.text`.
2. **fixed, with code repaired.** Basis: selling L (pays at most 3) at 3.2 nets at least 0.20 on every face; old `find_arb` returned 0 on it (run). Text: l15 `screens[9].prose`, `summary.ideas[0]`, `summary.trap`, `screens[6].hints[0..2].text`, `screens[6].feedback.generic`, `screens[6].explain.text`; l16 `screens[10].prose`, `.widget.how`, `.hints[1..2].text`, `.feedback.generic`, `.explain.text`; homework-4 `items[2].widget.lines[1].text`, `lines[2].text`, `lines[4].why`, `feedback.byKey.trade`, `explain.text`. Code: l16 `screens[10].widget.starter` and `.solution` (docstring; solution now `max(0, min(net) + cash)`), `.tests` (two added); homework-4 `items[0].widget.starter` and `.solution` (docstring; solution drops the constant-payoff filter, profit `min(net) + cash`), `.tests` (two added), `.how`, `feedback.generic`, `explain.text`. Went beyond the audit's wording-only fix because `find_all_arb` asks for "a sure profit" yet missed dominance trades.
3. **fixed.** Basis: stakes £20, £15, £12 on 2, 3, 4 to 1 lose all £47 if an unlisted outcome occurs; the Dutch-book bound needs a partition. l15 `screens[9].prose`, `screens[7].prose`, `quiz[1].prose` (same defect, not named by the audit), `summary.ideas[2]`, `screens[10].widget.starter` and `.solution` (`book_arb` docstring only); review-4 `items[4].prose`.
4. **fixed.** Basis: old skewE bids 2.3 + 1.3 = 3.6 < 3.7 and asks 2.7 + 1.7 = 4.4 > 3.3, so no trade-through; new E 2.5 to 2.9 gives 2.5 + 1.3 − 3.7 = 0.10 flat on every face (A = E + F). l16 `screens[2].widget.options[2].text`, `.why`, `feedback.byKey.skewE`.
5. **fixed.** Basis: grid search of expected log growth under a £30 cap (independent bets): best about £6.05, £7.80, £16.15 (0.03259) against equal scaling 0.03240. l18 `screens[4].explain.text`, `summary.ideas[1]`; review-4 `items[9].explain.text` (clarity only; the claim was already true of the rule).
6. **fixed.** Basis: enumeration of 36 rolls: |S − 7| ≤ 1 on 16, = 2 on 8, ≥ 3 on 12. My text gives the counts rather than the audit's "keeps most of its premium near 7", which fails at 6 and 8 (keeps half). l17 `screens[8].explain.text`.
7. **fixed.** Basis: 2-call and 12-put are each worth 5; 9-call 5/18. l17 `quiz[0].explain.text`.
8. **fixed.** Basis: overround 13/12 − 1 = 1/12; hold on a balanced book 1 − 12/13 = 1/13. l15 `quiz[1].explain.text`, `summary.ideas[2]` (with fix 3).
9. **fixed.** Basis: −12 = 1,000 − 1,012, a sign error; no reverse rates are quoted. l15 `screens[8].feedback.byKey.rev`.
10. **fixed.** Basis: Binomial(10, 0.9): P(6) = 0.0112, P(≤ 6) = 0.0128. l14 `summary.ideas[2]`.
11. **fixed.** Basis: Binomial(21, 0.1): P(≥ 4 misses) = 0.152; a shifted mean also raises misses. l14 `screens[11].explain.text`.
12. **fixed (softened, not verified).** No web access. (a) guide attribution removed and the battery and desk claim reduced to "may" and "can": l14 `screens[11].prose`. (b) "six or seven hits in ten" removed; kept only that people often make 90% ranges too narrow (the well-known overconfidence finding): l14 `screens[7].explain.text`. (c) "Desks do this by rule" replaced by a normative line: l18 `screens[11].explain.text`.

A. **fixed.** l16 `screens[11].explain.text`: now "Options on a dice game, later in this level, use the same parity."
B. No change (the audit records no finding).

Graded items changed. No numeric key or slip value changed. Keyed option text: l16 `screens[2]` option `skewE` (distractor; key `good` unchanged, recomputed above). Order lines: homework-4 `items[2]` `combo` and `cash` texts (answer order unchanged). Hidden tests added: l16 `screens[10]` `find_arb(PAY, {'L': (3.2, 3.3)}, {'L': -1}) == 1/5` (3.2 − 3 on faces 3) and `find_arb(PAY, {'A': (0.8, 0.9)}, {'A': 1}) == 1/10` (1 − 0.9 on face 1); homework-4 `items[0]` L sold at 3.1 against L and U gives (1/10, L sell) (3.1 − 3; L with U gives only 0.05) and A bought at 2.3 against H sold at 2.4 gives (1/10, A buy, H sell) (A − H = L ≥ 0, zero on faces 4 to 6). All seven old tests per widget were re-run under the new solutions with the same results; old solutions fail the new tests, starters fail all. No rubric changed.

Concepts script: section 8 added with four checks for the new text (ten units, new skewE traded through, find_arb on L, straddle counts). The old checks keyed on the replaced text now skip.

Gates: validator 0 errors (4,137 warnings, as before; manifest unchanged); concepts script exit 0 (297 checks, 0 failed, 5 notes, all unconditional notes on the old wording's counterexamples); `mm-games-3-perf-numbers.py` exit 0; voice scan 35: 0 and 0; playthrough with `--local-cdn` of l14 to l18, review-4 and homework-4, desktop and `--mobile`: all passed (review-4 10 of 10; homework-4 9 of 9, 40 of 40 marks).

## Fix-pass read

Blind read of the content-string diff of fix commit `6bc15e4e` (`git diff 6bc15e4e~1 6bc15e4e -- app/content/courses/mm-games`; 7 files). The reader did not open the audit above, its ledger, the earlier review or the concepts script. Paths use screen and item indices as they stand after the commit.

### Ledger

| # | File | JSON path | Claim (short) | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l14 | screens[7].explain.text | People asked for 90% ranges often make them too narrow; fix is wider ranges | correct | Alpert and Raiffa (1982), Lichtenstein, Fischhoff and Phillips (1982): stated 90% or 98% ranges hold well under their nominal rate. No figure is now quoted. |
| 2 | l14 | screens[11].prose | Interviews may ask for 90% ranges; a desk can set one each morning; mean £102.40, sd £1.20 | correct | Hedged with "may" and "can"; no source claimed. |
| 3 | l14 | screens[11].explain.text | Range £100.43 to £104.37; about two misses a month; many more suggest sd too low or mean off | correct | 1.645 × 1.20 = 1.974; 102.40 ∓ 1.974 = 100.426, 104.374. About 21 trading days × 0.1 = 2.1. A shifted mean also raises the miss rate. |
| 4 | l14 | summary.ideas[2] | Calibrated set scores six or fewer in ten only 1.3% of the time | correct | Bin(10, 0.9): P(X ≤ 6) = 0.012795 (computed). Agrees with screens[6] (0.0128) and screens[7] option `luck`. |
| 5 | l15 | screens[6].hints[0].text | An arbitrage can lose on no roll; find each plan's worst roll | correct | Necessary condition of the standard definition (Shreve, *Stochastic Calculus for Finance I*, Def. 1.1.2; Hull ch. 1). |
| 6 | l15 | screens[6].hints[1].text | Add the cash to what each plan pays on its worst roll | correct | Worst-outcome total is the test for "cannot lose". |
| 7 | l15 | screens[6].hints[2].text | First plan loses £0.10 on every roll; second loses when the second die shows 4 or more | correct | Plan 1: 7.0 − 7.1 = −0.10, legs cancel. Plan 2: +3.50 − second die, negative for 4, 5, 6. |
| 8 | l15 | screens[6].feedback.generic | Add the cash and check each plan's worst roll | correct | As row 6. |
| 9 | l15 | screens[6].explain.text | Arbitrage can lose on no roll; each plan loses on some | correct | As row 7. Key `neither` still unique; options `first`, `second`, `both` still false. |
| 10 | l15 | screens[7].prose | Evens, 2 to 1, 5 to 1 on three outcomes, exactly one happens | correct | 1/2 + 1/3 + 1/6 = 1. Key `none` unique: `equal` returns £20 on £30, `half` returns £20 on £20, `long` is a bet. |
| 11 | l15 | screens[8].feedback.byKey.rev | −12 has the sign reversed; loop ends at £1,012 | correct | 1,000 × 1.25 × 0.92 × 0.88 = 1,012. |
| 12 | l15 | screens[9].prose (sentences 1 and 2) | Arbitrage: trades that cannot lose on any outcome and gain on at least one; cancelling payoffs with money left over is the plainest kind | correct | Standard definition on a finite outcome set: Shreve I, Def. 1.1.2 (zero probability of loss, positive probability of gain); Björk, *Arbitrage Theory in Continuous Time*, Def. 2.3. The cancelling case is a special case. |
| 13 | l15 | screens[9].prose (sentence 3) | Board with odds o_i to 1 on outcomes of which exactly one happens has an arbitrage when Σ 1/(o_i + 1) < 1 | correct | Stake 1/(o_i + 1) per £1 payout on each: cost Σ < 1, return 1 on the one outcome that happens. Exclusive and exhaustive is the needed hypothesis; exclusive alone is not enough (no outcome may happen). |
| 14 | l15 | screens[10].widget.starter and solution, `book_arb` docstring | "exactly one outcome happens" | correct | As row 13. The code is unchanged by the diff. |
| 15 | l15 | summary.ideas[0] | Same definition as row 12 | correct | As row 12; matches screens[9]. |
| 16 | l15 | summary.ideas[2] | Exactly one outcome happens: sum below 1 locks a profit; exactly 1 fair; above 1 is the overround | correct | As row 13. Overround = excess of the summed implied chances over 1 (standard bookmaking usage). |
| 17 | l15 | summary.trap | Calling a trade arbitrage when some outcome loses money | correct | As row 5. |
| 18 | l15 | quiz[1].prose | 1 to 1, 2 to 1, 3 to 1 on three outcomes, exactly one happens | correct | Hypothesis stated; key 13/12 = 1.0833 unchanged. |
| 19 | l15 | quiz[1].explain.text | Excess 1/12 is called the overround | correct | 13/12 − 1 = 1/12; standard term. |
| 20 | l15 | screens[0].explain.text (unchanged) | "That is an **arbitrage**: a profit on every outcome, with nothing left to settle." | imprecise | First bold definition is the strong form; screens[9] and summary.ideas[0] now define the weak form (no loss anywhere, gain somewhere). Two definitions in one lesson. Finding 1. |
| 21 | l16 | screens[2].widget.options[2].text | A 3.3 to 3.7, E 2.5 to 2.9, F 1.3 to 1.7 is not consistent | correct | Run: buy A 3.7, sell E 2.5 and F 1.3 locks 0.10 (payoffs cancel since E + F = A). The old text (E 2.3 to 2.7) had no arbitrage, so the old distractor was a second right answer. |
| 22 | l16 | screens[2].widget.options[2].why; feedback.byKey.skewE | E sits 0.7 above fair; interviewer sells E at 2.5 and F at 1.3, buys A at 3.7, locks 0.10 a set | correct | Centre 2.7 − 2 = 0.7. 2.5 + 1.3 − 3.7 = 0.10. Key `good` unique: exhaustive search of ±1 on up to three of A, E, F finds no strict or weak arbitrage in `good`, and one in each of `evens` (1.4), `skewE` (0.10), `same` (2.9). |
| 23 | l16 | screens[10].prose | "find the profit a combination locks on every face" | correct | Matches the code: min over faces of payoff plus cash. |
| 24 | l16 | screens[10].widget.starter and solution, `find_arb` docstring | Return smallest of six totals if positive, else 0 | correct | Run: solution passes 9 of 9 hidden tests and the example; starter fails all. 20,000-case fuzz against an independent reference, 0 mismatches. |
| 25 | l16 | screens[10].widget.solution (code) | `max(Fraction(0), min(net) + cash)` | correct | As row 24. Returns an exact Fraction in every fuzz case. |
| 26 | l16 | screens[10].widget.tests[7] | Sell L at 3.2 gives 1/5 | correct | L pays at most 3; 3.2 − 3 = 0.2. |
| 27 | l16 | screens[10].widget.tests[8] | Buy A at 0.9 gives 1/10 | correct | A pays at least 1; 1 − 0.9 = 0.1. |
| 28 | l16 | screens[10].widget.how | 9 hidden tests; a combination that can lose on some face returns 0 | imprecise | True, but a combination that breaks even on its worst face and gains elsewhere also returns 0 (35 such cases in the fuzz). Under the definition taught one lesson earlier that trade is an arbitrage. Finding 2. |
| 29 | l16 | screens[10].hints[1].text | Take the worst face: the smallest of the six totals | correct | As row 24. |
| 30 | l16 | screens[10].hints[2].text | Buying pays the ask; selling receives the bid; add the cash to each face | correct | As row 24. |
| 31 | l16 | screens[10].feedback.generic | Check the worst face and the sign of the cash | correct | As row 24. |
| 32 | l16 | screens[10].explain.text | Sell U at 1.1 locks 0.10; H and L for 3.5 against A at 3.6 locks 0.10; sell L at 3.2 locks 0.20 since L never pays more than 3 | correct | All three are hidden tests and pass. |
| 33 | l16 | screens[11].explain.text | "Options on a dice game, later in this level, use the same parity." | correct | No lesson number; the options lesson states C_K − P_K = E[S] − K. |
| 34 | l17 | screens[8].explain.text | Short straddle at 2.0 gains only on sums 6 to 8, 16 rolls in 36, "and loses on 12" | imprecise | Gains when the sum is within 1 of 7: 5 + 6 + 5 = 16 rolls. Loses on sums 2, 3, 4, 10, 11, 12: 12 rolls. "Loses on 12" follows "the worst rolls, 2 and 12" and reads as the sum 12. Finding 3. |
| 35 | l17 | quiz[0].explain.text | Calls struck well above 7, and puts well below it, are cheap | correct | 9-call = 10/36 = 5-put by symmetry of the sum about 7. Low-strike calls are not cheap, which the old text implied. |
| 36 | l17 | summary.ideas[2] (unchanged) | "A short straddle earns small sums often and owes most at the extremes" | imprecise | The explain now says it gains on only 16 rolls in 36, with 8 level and 12 losing. "Often" is the half of the old claim the fix removed from the explain. Finding 4. |
| 37 | l18 | screens[4].explain.text | Equal scaling is close to the best capped mix, which cuts a to about £6 | correct | Grid maximisation of expected log wealth, three independent bets, stakes summing to £30: a £6.05, b £7.80, d £16.15, growth 0.03259 against 0.03240 for £7.50, £7.50, £15. |
| 38 | l18 | screens[11].explain.text | Resizing works best as a fixed rule, not a choice made by feel | correct | Practice statement, now hedged; £80,000 = 10% of £800,000. |
| 39 | l18 | summary.ideas[1] | A simple rule scales all stakes alike: £40 capped at £30 is 0.75 of each | correct | 30/40 = 0.75; agrees with row 37 and summary.formula. |
| 40 | review-4 | items[2].explain.text | Range 90 to 140 would score 50; ten more units of width would have saved 90 | correct | Width 50, truth 95 inside. 140 − 50 = 90; 50 − 40 = 10. |
| 41 | review-4 | items[4].prose | Evens, 4 to 1, 4 to 1 on three outcomes, exactly one happens | correct | 1/2 + 1/5 + 1/5 = 9/10; stakes £5, £2, £2 return £10; key £1. |
| 42 | review-4 | items[9].explain.text | Kelly £10 and £12.50; scaled by 2/3 to £6.67 and £8.33; equal scaling keeps the mix | correct | f = 0.6 − 0.4 = 0.2; f = 0.5 − 0.5/2 = 0.25; 15/22.5 = 2/3. |
| 43 | review-4 | items[9].prose (unchanged) | "At most £15 at risk in the round." Key £8.33 | imprecise | The key holds only under equal scaling, which the item does not ask for. The lesson now says equal scaling is not the best capped mix; here the growth-optimal split is £5.10 and £9.90 (grid search). Finding 5. |
| 44 | homework-4 | items[0].widget.starter and solution, docstring | Score each set by its profit on the worst face; keep those above 0; tie-break; none gives (Fr(0), ()) | correct | Run: solution passes 9 of 9 hidden tests and the example; starter fails all. 20,000-case fuzz against a brute-force reference written from the docstring, 0 mismatches. Layout only: finding 6. |
| 45 | homework-4 | items[0].widget.solution (code) | `profit = min(net) + cash`, strict `> 0`, key (−profit, count, trades) | correct | As row 44. "Above 0" is stated, so a trade level on its worst face is openly left out. |
| 46 | homework-4 | items[0].widget.tests[7] | L at 3.1 to 3.2 with fair U: (1/10, sell L) | correct | 3.1 − 3 = 0.1; no better set. |
| 47 | homework-4 | items[0].widget.tests[8] | A at 2.2 to 2.3 with fair H: (1/10, buy A, sell H) | correct | Cash 2.4 − 2.3 = 0.1; A − H is 1, 2, 3, 0, 0, 0, never negative. |
| 48 | homework-4 | items[0].widget.how | 9 hidden tests: seven planted arbitrages, two consistent sets with none | correct | Counted: tests 0 and 5 expect (0, ()); the other seven expect a trade. |
| 49 | homework-4 | items[0].feedback.generic | Check the profit on the worst face, and the tie-break | correct | As row 44. |
| 50 | homework-4 | items[0].explain.text | Cheap A against E and F locks 0.10; buy A at 2.3, sell H at 2.4 locks at least 0.10; a fair set returns nothing | correct | Tests 2 and 8. Fair set: enumeration of every set of up to three finds no non-losing combination; in general each quote straddles its fair value, so every trade has negative mean. |
| 51 | homework-4 | items[2].widget.lines[1].text | Find a combination to test, such as one whose payoffs cancel | correct | Cancelling is one kind, as row 12. |
| 52 | homework-4 | items[2].widget.lines[2].text | Price at the quotes; is it in profit on every face? | correct | The prose asks for money "for sure", the strong form. Order pay, combo, cash, size is still the only valid order; `trade` is still the one left out. |
| 53 | homework-4 | items[2].widget.lines[4].why; feedback.byKey.trade | A gap is only an arbitrage once no face can lose | correct | Necessary condition, as row 5. |
| 54 | homework-4 | items[2].explain.text | Table shows each combination's pay per face; with the cash, a profit on every face is money for sure; size says how much | correct | As rows 12 and 52. |

### Verdict counts

54 rows: 49 correct, 0 wrong, 5 imprecise, 0 misleading, 0 unverified. Three of the five imprecise rows (20, 36, 43) are sentences the diff did not touch that a changed sentence now sits beside.

### Checks run

- `find_arb` (l16 screens[10]) and `find_all_arb` (homework-4 items[0]): prelude, starter, solution and hidden tests extracted from the JSON and run in Python 3. Each solution passes 9 of 9 hidden tests plus its example; each starter fails all 10.
- Fuzz: 20,000 random families (1 to 5 contracts, payoffs 0 to 4, quotes on a 0.1 grid so ties occur). `find_arb` against a face-by-face reference, and `find_all_arb` against a brute-force reference that enumerates every buy, sell or skip assignment and sorts by the docstring's tie-break. No mismatch. 291 positive `find_arb` cases, 5,977 positive `find_all_arb` cases, 35 weak-only cases (level on the worst face, gain elsewhere) that return 0.
- l16 screens[2]: exhaustive ±1 search on A, E, F for each option, strict and weak.
- l18 screens[4] and review-4 items[9]: grid maximisation of expected log wealth under the cap.
- Binomial tail for l14; straddle roll counts for l17.
- Voice on every changed string: no exclamation mark, no em-dash, no sentence over 35 words, no explanation over three sentences, no lesson cited by number.
- Not run: validator and playthrough (no content was edited by this read).

### Findings

1. l15-arbitrage-in-a-book.json | screens[0].explain.text | imprecise | minor | The lesson's first, bold definition of arbitrage is "a profit on every outcome", the strong form. screens[9].prose and summary.ideas[0] now define it as no loss on any outcome and a gain on at least one. A learner meets two definitions in one lesson. | Shreve, *Stochastic Calculus for Finance I*, Def. 1.1.2 is the form the fix adopted; the screens[0] trade does profit on every outcome, so only the definition clause is off. | Replace the whole explain with three sentences: `X's best offer, 103.0, is below Y's best bid, 104.0, so buying from one and selling to the other locks £1 a unit. That is an **arbitrage**: a trade that cannot lose on any outcome and gains on at least one. Here it gains £1 a unit whatever happens.`

2. l16-several-contracts.json | screens[10].widget.how | imprecise | minor | "A combination that can lose on some face returns 0" leaves out the other case that returns 0: a combination level on its worst face that gains on others. By the definition taught one lesson earlier that trade is an arbitrage, yet `find_arb` scores it like a losing one. The docstring is right ("profit locked on every face"); only the meaning of 0 is unstated. | Fuzz: 35 of 20,000 random cases have worst-face total 0 and a positive total elsewhere; all return `Fraction(0)`. | `Check runs 9 hidden tests. Values are exact Fractions. A combination that can lose, or only break even, on some face returns 0.`

3. l17-options-on-a-game.json | screens[8].explain.text | imprecise | minor | "and loses on 12" means 12 rolls in 36, but it follows "The worst rolls, 2 and 12" and reads as the sum 12. | Loses when the sum is more than 2 from 7: sums 2, 3, 4, 10, 11, 12, which is 1 + 2 + 3 + 3 + 2 + 1 = 12 rolls. | Replace the third sentence with: `The short straddle gains only on sums 6 to 8, 16 rolls in 36, and loses on 12 rolls in 36.`

4. l17-options-on-a-game.json | summary.ideas[2] | imprecise | minor | The summary still says a short straddle "earns small sums often". The explain on screens[8] now says it gains on only 16 rolls in 36; it is level on 8 and loses on 12. The two no longer agree. | Same count as finding 3; at 2.0 the gains are 1 or 2 and the losses 1, 2 or 3. | `A short straddle gains near the middle and owes most at the extremes; a revealed die moves every option.`

5. review-4.json | items[9].prose | imprecise | minor | The key £8.33 is right only if both Kelly stakes are scaled by one factor, and the item does not say to do so. The betting-board lesson now states that equal scaling is a simple rule and not the best capped mix, so a careful learner may reasonably look for the best mix. | Grid search of expected log wealth with £15 at risk: about £5.10 on bet 1 and £9.90 on bet 2, against £6.67 and £8.33 under equal scaling. The feedback and explain already assume equal scaling. | `£50 bankroll. Bet 1: evens with chance 0.6. Bet 2: 2 to 1 with chance 0.5. At most £15 at risk in the round, so scale both Kelly stakes by the same factor.`

6. homework-4.json | items[0].widget.starter and items[0].widget.solution (docstring) | imprecise | minor | Layout only: the edited docstring line `face (payoff plus cash) and keep those above 0. Return (profit, trades) for the` is 82 characters where every other line is under 60, so it wraps or scrolls on a phone. No change of meaning. | Line lengths read from the JSON. | In both strings replace the docstring text from `(at the bid).` to its end with: `(at the bid). Score each by its profit on the worst\n    face (payoff plus cash) and keep those above 0.\n    Return (profit, trades) for the best: highest profit,\n    then fewest trades, then the first in sorted order;\n    trades is a sorted tuple of (name, \"buy\" or \"sell\").\n    With none: (Fr(0), ()).\"\"\"`

No `wrong` and no `serious` finding. The arbitrage definition, the board rule, both code items and every changed key and distractor hold.

## Fix pass (fix-pass read follow-up)

Six findings: 6 fixed, 0 disputed. No key, option, test or rubric changed.

1. Fixed. l15-arbitrage-in-a-book.json `screens[0].explain.text`. Basis: Shreve I, Def. 1.1.2 (no chance of loss, some chance of gain), the form screens[9] and summary.ideas[0] use. Third sentence now: "That is an **arbitrage**: a trade that cannot lose on any outcome and gains on at least one." The second sentence still states the £1 a unit gain.
2. Fixed. l16-several-contracts.json `screens[10].widget.how`. Basis: the solution returns `max(0, min(net) + cash)`, so a worst-face total of 0 gives 0 whatever the other faces pay. Now: "A combination that can lose, or only break even, on some face returns 0."
3. Fixed. l17-options-on-a-game.json `screens[8].explain.text`. Basis: short straddle at strike 7 for 2.0 pays 2 − |S − 7|; counted over 36 rolls: gain 16 (sums 6 to 8), level 8 (sums 5, 9), loss 12 (sums 2 to 4, 10 to 12). Third sentence now ends "and loses on 12 rolls in 36."
4. Fixed. l17-options-on-a-game.json `summary.ideas[2]`. Basis: same count; 16 gains in 36 is under half, so "often" was wrong in spirit. Now: "A short straddle gains near the middle and owes most at the extremes; a revealed die moves every option."
5. Fixed. review-4.json `items[9].prose`. Basis: Kelly f = 0.2 (£10) and f = 0.5 − 0.5/2 = 0.25 (£12.50); scaled by 15/22.5 gives £6.67 and £8.33; my own grid of expected log wealth with £15 at risk gives £5.10 and £9.90 (growth 3.98320 against 3.98188). The prompt now states the method, so the key £8.33 is right by construction: "At most £15 at risk in the round, so scale both Kelly stakes by the same factor." Key, wrong values and feedback unchanged.
6. Fixed. homework-4.json `items[0].widget.starter` and `items[0].widget.solution` docstring rewrapped; longest line now 57 characters; wording unchanged; the two docstrings are identical. Run: solution passes 10 of 10 (9 hidden tests plus example), starter fails 10 of 10.

Concepts script: the l17 check at the straddle count matched the old text "and loses on 12"; it now matches "and loses on 12 rolls in 36" (same assertion).

Gates: validator 0 errors; `mm-games-L4-concepts.py` 297 passed, 0 failed, exit 0; voice scan 35 over the course 0 and 0; playthrough of l15, l16, l17, review-4 and homework-4, desktop and `--mobile`, all passed.

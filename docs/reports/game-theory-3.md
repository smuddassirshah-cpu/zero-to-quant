# Report: game-theory level 3 (Poker and decisions)

Brief: `docs/briefs/game-theory.md`, `## Level 3`, its preamble and `## Number checks`. Ids, names, objectives and skills from `app/content/courses/game-theory/course.json` (`gm-poker` on l11, l12, l14 and l15; `gm-poker` and `gm-mixed` on l13).

## Files written

| File | Screens or items | Quiz | Shape |
|---|---|---|---|
| `l11-pot-odds.json` | 10 screens | 3 | explore: the reported spot (£50 into £100) as a `plane` line 200x − 50 with a control on the chance and a live caption (break-even 25%); its value at 30% (+£10, free resources named here); rules in one screen and the outs tapped on a transposed deck `grid` (13 ranks by 4 suits, seen cards dimmed); the turn call (−£0.65); two cards to come (34.97%, then 37.98% against K♣ Q♦ in the explanation); trap (what chance do you need); edge (a free card, an all-in call has no implied odds); generalise; drill (table); follow-up implied odds (£15) |
| `l12-ranges.json` | 10 screens | 3 | hook: tap the 12 live ace-king combos on a 4 × 4 suit `grid`; pairs (6, then 3); the river call (4-column table: hand, combos, you win, wins; 4 of 23); blockers (A♥ A♣ leave 8 ace-king combos); trap (king-queen suited added: fold); the call's cost (−£2); edge (0 combos of aces); generalise; drill (table); follow-up a pot-sized bet (4 bluff combos) |
| `l13-toy-poker.json` | 9 screens | 3 | explore: Ben's call against the bluff share, 300x − 100, with a control (1/3); Ben's calling frequency (1/2); a half-pot bet (1/4 and 2/3, linked to l11's 25%); Kuhn's three-card poker, cut down (`boxes` of J, Q, K; table of four frequencies; value +1/18); trap (bet a sure loser?); edge (an unbalanced bettor is called every time); generalise (£150 into £100: 3/8); drill (table, five answers including the betting queen, −1/9); follow-up the full game (−1/18) |
| `l14-value-of-information.json` | 9 screens | 3 | hook: three face-down cards, one turned at £0, tap the card you take (count mode); the look's worth (table: 30, 60, 30); perfect information on a +£30 or −£20 trade (`tree`, £10); the 80% analyst (4-column table, £5); trap (+£50 or −£10: worth £0); edge (60% analyst £0, 70% £2.50); generalise; drill (table: die £0.50, seeing his cards £36, the analyst at most £5); follow-up an 80% tell (`tree` with exact branch chances, £21.20) |
| `l15-sizing-and-risk.json` | 9 screens | 3 | explore: draggable point on the growth curve g(f) at 4 to 1 and 30%, with the expected-profit line (0.125); all-in survival 0.3^10; Kelly, half and double (table); ruin at a fixed stake (`walk`, 300 seeded bankrolls of 10 stakes, seed 4, stopped at 0, table of (9/11)^n); trap (stake 30%?); edge (no edge, f* = 0); generalise (three yardsticks, the poker bankroll form); drill (table); follow-up an uncertain edge (0.0012) |
| `review-3.json` | 10 items, difficulty 2 to 4 | | interleaves l11, l11, l11, l12, l12, l13, l13, l14, l15, l15; every spot unseen |
| `homework-3.json` | 8 items, difficulty 3 to 5 (two at 5) | | `order` derivation of B/(P + 2B) with the calling-frequency distractor (4), `code` `combos` and `range_equity` (5), implied odds £27.78 (4), bluff share 2/7 (3), the 75% analyst £5 (4), Kelly under doubt 0.0012 (4), `multi` on ruin (3), `longform` defend the river line (5) |

Every drill screen, quiz item, review item and homework item carries `tags` from the brief's families and a `pace` (drills 120 s, about two minutes a question as the brief asks; quiz 30 to 60; review 30 to 90; homework 60 to 900). `shuffle: true` on every `choice` and `multi`. Free resources are named once, in l11 screen 2; the toy game is named as Kuhn's three-card poker in l13. The reported question (30% to win, £100 in the pot, a £50 bet) is "reported in trading-firm interviews", with no firm named; the homework longform is introduced the same way. Lessons cite `counting-chance` l12, `markov` l10 and l19, `fin-ml` l9, `puzzles` l21 (as a sibling lesson, for the Kelly derivation) and `graphs-dp` l17; no number from `puzzles` l21, l23 or `mm-games` l10, l18 is used. Every 4-column table fits at 390 px.

## Validator

`node tools/validate.mjs`: 0 errors and no warnings on any game-theory file (the course is now fully written). Voice scan (`VOICE_BASE=/home/user/zero-to-quant/app/content/courses/game-theory/ python3 docs/reviews/voice-scan.py`): 0 sentences over 20 words and 0 explanations over three sentences, for the whole course.

## Playthrough

From `app/`, with `--local-cdn <scratchpad>/pkgs`, desktop and again `--mobile`: l11 13 checks, quiz 3/3; l12 13 checks, 3/3; l13 12 checks, 3/3; l14 12 checks, 3/3; l15 12 checks, 3/3; `--set game-theory/review-3` 10 of 10; `--set game-theory/homework-3` 8 of 8 right, 37 of 37 marks. All passed, both widths (log: `<scratchpad>/game-theory-3/playthrough.log`). Screenshots, desktop and 390 px, in `<scratchpad>/game-theory-3/shots`.

Layout fixes made after looking: the l15 growth planes keep the x axis at the bottom (the axis title sat on the curve at y = 0) and the expected-profit label moved below its line; the l11 and l13 live captions say "pounds" rather than "£−70.00" (backlog bullet); the board cards are drawn `size: "large"`; a boxes canvas with no board drops the empty board row; the l14 analyst table header is "Best value (£)", so its fourth column fits; the homework code docstring is wrapped.

## Numbers and their sources

All recomputed in `<scratchpad>/game-theory-3/checks3.py` (cards; output `checks3.log`) and `checks3b.py` (bluffing, information, sizing; `checks3b.log`). Method 1: formulas with `fractions`. Method 2: a seven-card hand evaluator over every river and runout, combo enumeration over all 1,326 holdings, best responses over every pure strategy, seeded simulations.

- l11: price 25%, +£10 (both 0.3 × 150 − 0.7 × 50 and 0.3 × 200 − 50); 9 outs, and the enumeration of all 44 rivers against K♣ Q♦ finds exactly the 9 hearts; 9/46 = 19.57%, price 20%, −15/23 = −£0.65; 1 − (38/47)(37/46) = 378/1081 = 34.97% (rule of four 36%), price 33.3%; equity 376/990 = 37.98% (all 990 runouts, no ties; seeded simulation of 200,000 runouts 0.3816); drill 20%, 8/46 = 17.39%, 31.45% (rule of four 32%), 25%; implied odds X = 95 − 80 = £15. Quiz: 20%, 10/46 = 21.74%, fold.
- l12: ace-king 16, 12 with the A♠ seen; aces 6, then 3; river range 12 + 3 + 4 + 4 = 23, you beat 4, 17.39%, price 25%; A♥ A♣ held leaves 8 ace-king; king-queen suited 2 combos, 6/25 = 24%, −£2 (each of the 25 combos scored by the evaluator); counted as 4: 8/27 = 29.6%, +£9.26; aces with three seen 0; queen-jack offsuit 12; drill 9, 78/1326 = 1/17 = 0.0588, 1 bluff (7/26 = 26.9%); pot-sized bet needs 33.3%, 4 bluffs (10/29 = 34.5%; 3 give 9/28 = 32.1%). Quiz: 1, 3, call (+£10).
- l13: 1/3 and 1/2; 1/4 and 2/3; cut-down Kuhn: Ana bets K, bluffs J 1/3, checks Q; Ben calls K, folds J, calls Q 1/3; value +1/18, and each side's best pure reply to the other's mix earns exactly 1/18 (8 pure plans each); £150 into £100 3/8 and 2/5; drill 2/5 and 1/3, 3/10 and 4/7, the betting queen −1/9 (against Ben's mix and against his best reply); the full game −1/18, confirmed by best replies over all 64 pure plans on each side (α = 0 equilibrium). Quiz: 1/5, 3/4, fold.
- l14: cards £30, £60, look £30 (simulated 59.95 in the brief's check; recomputed exactly); perfect information £15 − £5 = £10; 80% analyst +£20 and −£10, worth £5 (seeded simulation of 400,000 trades 9.996); +£50 or −£10 trade: bad call still +£2, worth £0; 60% analyst £0, 70% £2.50; die £4 against £3.50, £0.50; seeing his cards 6/25 × 150 = £36; the tell 43/125, 24/43, 3/41, £21.20 (simulated 21.14). Quiz: £16, £0, £5.
- l15: f* = 0.125, g = 0.02817 (grid over 100,000 fractions peaks at 0.125; simulated 0.0271 over 200,000 bets); half Kelly 0.02177 (77%), double 0.00657, zero growth at 0.2685, g(0.3) = −0.0131; 0.3^10 = 0.0000059; ruin (9/11)^n 0.3666, 0.1344, 0.0181 (simulated 0.369 and 0.134; the seed-4 walk shows 46 of 300, about 15%, stated as within sampling error); poker 0.2096, 0.0960, 0.0439; continuous form for 20 stakes 0.0176; edge f* = 0; drill 0.175 and 0.02924, (12/13)^15 = 0.3010; doubt 0.0625 and 0.1875, 0.0012, half Kelly 0.0074. Quiz: 0.2, (2/3)^8 = 0.0390, about three quarters.
- Review: +£8; 4/46 = 8.70%; 44.96% (rule of four 48%); 3; 9; 2/3 (bluffs 1/4); +£40 a bluff; 90% analyst £7.50 (+£25 and −£15); 1/15 = 0.0667; (9/11)^15 = 0.0493.
- Homework: X = 250/9 = £27.78; 2/7 (calls 3/5); 75% analyst: good call 0.45, +£20, bad −£9.09, worth £5 (perfect £12); 0.0012; longform price 25%, 24%, −£2.40, 7/26 with one more bluff.
- Code item, run locally: `combos` and `range_equity` solution 14 of 14; the starter (counts without removing `dead`) passes only the four tests with no dead card and fails ten, as the brief asks.

## Departures from the brief, and why

- l11: the hook is an `explore` with a numeric (the break-even chance); the reported spot's +£10 is screen 2. The rules screen is the outs screen.
- l12: worked (3), the blocker, uses a new example (A♥ A♣ against ace-king, 8 combos) so that the trap, king-queen suited on the river, is not answered one screen earlier; the brief's 24% and −£2 come in the trap's explanation and the next screen.
- l14: the hook taps the card you take after one is turned (count mode), since a boxes card cannot be flipped by a tap (backlog bullet); the trap is a single `choice`, with £0 in its explanation.
- l15: worked (3) shows the ruin chances for 5, 10 and 20 stakes in one table under the `walk`; the poker bankroll form sits in the generalise screen and the drill.

## Conventions

Seeds: l15 walk seed 4 (300 paths, 30 drawn). Cards are written rank then suit symbol (`K♥`, `10♥` on the deck grid). The deck grid is ranks A to 2 down, suits ♠ ♥ ♦ ♣ across. Generators: `<scratchpad>/game-theory-3/gt.py` (helpers, copied from level 2), `l11.py` to `l15.py`, `sets3.py` (which also runs the code harness).

## Proposed course.json change

None.

## Backlog

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (game-theory level 3)".

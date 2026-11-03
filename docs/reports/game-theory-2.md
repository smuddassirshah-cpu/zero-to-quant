# Report: game-theory level 2 (Sequential games and auctions)

Brief: `docs/briefs/game-theory.md`, `## Level 2`, its preamble and `## Number checks`. Ids, names, objectives and skills from `app/content/courses/game-theory/course.json` (`gm-sequential` on l6 and l10; `gm-sequential` and `gm-normal` on l7; `gm-auction` on l8 and l9).

## Files written

| File | Screens or items | Quiz | Shape |
|---|---|---|---|
| `l6-game-trees.json` | 9 screens | 3 | hook: ordered tap on the entry `tree` (Share, then In); the same game as a table (tap both equilibria); why (Out, Fight) fails (choice); four-move centipede (tree plus a 4-column table widget filled from node 4 up); trap (announced threat); edge (a tie at the last node); generalise; drill (three-stage tree, table of four games); follow-up spare capacity (£5m) |
| `l7-guess-two-thirds.json` | 9 screens | 3 | explore: draggable average on a `number-line` with a derived two-thirds point and caption; rounds of deletion (table, 12 rounds); levels of thinking (table); a seeded room (`bars`, table for average and target); trap (your guess against that room); edge (two players: 0 never loses); generalise; drill (table); follow-up 1.5 times the average, capped (`multi`) |
| `l8-sealed-bids.json` | 9 screens | 3 | explore: expected profit against your bid on a `plane`, draggable point, live caption (£40, £32); derive `order` with a distractor; second price (4-column table on a number-line); revenue with two bidders (table); trap (shade in second price); edge (reserve £50); generalise (three bidders, £60); drill (table); follow-up ten bidders (£81.82) |
| `l9-winners-curse.json` | 10 screens | 3 | explore: seeded `bars` sim of the winner's error, `max(sample(5, u(-10, 10)))`, seed 9, with exact bin heights; derive the overshoot (`order`); ten bidders (£8.18); acquiring a firm (`order` with the unconditional-average distractor, plane of expected profit); trap (offer £60m?, choice); its cost (−£7.2m); edge (twice the value breaks even); generalise; drill (table); follow-up the jar estimate (£93.33) |
| `l10-splitting-a-pie.json` | 10 screens | 3 | hook: three rounds as a 4-column table bound to `bars` (91, 9, 81); ultimatum game; two to five rounds (table bound to bars); derive unequal patience (`order` with `same` and a distractor); δ_A 0.9, δ_B 0.8 (0.7143); trap (52.63%); edge (δ = 0); generalise (δ = 0.99); drill (table bound to bars); follow-up outside offers £30 and £60 (table) |
| `review-2.json` | 9 items, difficulty 2 to 4 | | interleaves l6, l6, l7, l8, l8, l8, l9, l9, l10; every game unseen |
| `homework-2.json` | 8 items, difficulty 3 to 5 (two at 5) | | `order` derivation of b = v/2 (4), `code` `spe(tree)` (5), capacity £3m (4), unequal patience 25.97% (4), overshoot £11.67 (3), plus-12 equilibrium 36 (3), `multi` on second price (3), `longform` acquire-a-company (5) |

Every drill screen, quiz item, review item and homework item carries `tags` from the brief's families and a `pace` in seconds (drills 180; quiz 45 to 90; review 30 to 90; homework 90 to 600). `shuffle: true` on every `choice` and `multi`. Free resources are named once, in the l6 drill prose (the *Probability and Markets* guide, by a trading firm about its own interviews, and Open Yale Courses' *Game Theory* lectures). No firm is named. `graphs-dp` l17, `puzzles` l11, `limits` l14, `micro` l11 and `brainteasers` l6 (as a later lesson) are cited; no pirate, lion or take-away game is used. Every 4-column table fits at 390 px without scrolling.

## Validator

`node tools/validate.mjs`: 0 errors, and no warnings on level 2 files (the only game-theory warning is the course's unwritten level 3). Voice scan (`VOICE_BASE=/home/user/zero-to-quant/app/content/courses/game-theory/ python3 docs/reviews/voice-scan.py`): 0 sentences over 20 words, 0 explanations over three sentences, for the whole course.

## Playthrough

From `app/`, with `--local-cdn <scratchpad>/pkgs`, desktop and again `--mobile`: l6 12 checks, quiz 3/3; l7 12 checks, 3/3; l8 12 checks, 3/3; l9 13 checks, 3/3; l10 13 checks, 3/3; `--set game-theory/review-2` 9 of 9; `--set game-theory/homework-2` 8 of 8 right, 36 of 36 marks. All passed, both widths (log: `<scratchpad>/game-theory-2/playthrough.log`). Screenshots, desktop and 390 px, in `<scratchpad>/game-theory-2/shots`; Why? sheets for l6 in `why`.

Layout fixes made after looking: the l9 trap no longer shows the expected-profit curve (it gave the answer away; a number-line of the owner's value and the offer replaces it); the l9 planes take a y range per k (the k = 3 drill curve ran off the top); the l8 and l9 bar charts hide the empty bar the learner fills (`showZero: false`); the homework code docstring is wrapped under 54 characters; "£k m" in the l6 follow-up reads "a cost of $k$, in £m". Every point hint now highlights its canvas, and worked screens that change canvas kind are `problem` rather than `ladder`.

## Numbers and their sources

All recomputed in `<scratchpad>/game-theory-2/checks2.py` (output `checks2.log`). Method 1: a recursive tree solver, closed forms with `fractions`, a grid over bids. Method 2: hand backward induction, seeded simulations (200,000 rival bids, 100,000 auctions per n, 100,000 largest errors), midpoint integration over V (100,000 points), round-by-round bargaining recursion over 2,000 and 2,001 rounds.

- l6: entry (3, 5); table equilibria (Out, Fight) and (In, Share); four-move centipede (3, 5), (4, 2), (1, 3), (2, 0); tie gives (0, 10) or (3, 5); six-move centipede 2; three-stage tree (2, 2), Ana 2; venue game Ana first 3, Ben first 2; capacity threshold £5m (gains at 4.9, loses at 5.1). Quiz: entrant stays out (0, 7); Safe 2; chicken 3.
- l7: 66.67, 44.44, 29.63, 19.75, 13.17; 12 rounds (1.156 after 11, 0.771 after 12); levels 33.33, 22.22, 14.81; room 925/27 = 34.26, target 1850/81 = 22.84; two players: the lower guess always wins (all 5,050 ordered pairs checked); drill 7 rounds (1.5625, 0.78125), 12.5, 355/9 = 39.44 and 26.30, 30; capped 1.5 times: all 0 and all 100. Quiz: 56.25, 37.5, 20.
- l8: hook £40, £32 (grid over 8,001 bids); second-price table 10, 0, 10 / 0, 0, −10; two bidders £33.33 both ways, your profit £32 both ways (simulated 31.95 and 31.96); (n − 1)/(n + 1) × 100 = 33.33, 50, 60, 66.67, 81.82 (simulated within 0.15); bids 40, 72, £60 at n = 3 and v = 90; second price pays 55. Quiz: 45, 60, 75.
- l9: overshoot 20/3 = 6.67 (simulated 6.65; seed-9 run of 1,000 shown in the canvas, exact bin heights from ((x + 10)/20)^5); 90/11 = 8.18; bars 3.33 and 9.05 for 2 and 20 bidders; firm at k = 1.6, £60m: −12 given acceptance, −7.2 expected; k = 2 breaks even; drill 16.36, 7.20, 0 (k = 1.8), 50 (k = 3, offer £100m); jar 93.33. Quiz: 10; −10 (k = 1.2, £50m).
- l10: 91, 9, 81; ultimatum £0 (£99 in whole pounds); shares 0.1, 0.91, 0.181, 0.8371 and limit 1/1.9 = 0.5263; 0.2/0.28 = 0.7143 (Ben 0.2857); δ = 0.99 gives 0.5025; drill 20%, 55.56%, 68.97%, 84%; outside offers £30 (Ana still 52.63) and £60 (Ana 40). Quiz: 40%, 66.67%, Ana's share falls in δ_B.
- Review: entrant 2 (Out (0, 8), Fight (−1, 1), Share (2, 4)); three-move centipede (2, 0); two fifths level 2 = 8; bid 60; price 67; 66.67; overshoot 6; firm k = 1.5 at £40m −4; three rounds at δ = 0.7 79%, no last round at 0.95 51.28%.
- Homework: end check b = 50 earns v − 50 ≤ v²/200 for every v (as (v − 100)² ≥ 0); capacity £3m (2.9 gains, 3.1 loses); 0.05/0.1925 = 25.97% (recursion agrees); 15 × 7/9 = 11.67; 36; longform: loss 0.25b, −£9m at £60m, threshold at twice the value.
- Code item, run locally: `spe` solution 7 of 7, starter (follows the first move) 3 of 7, so it fails four (the entry tree, the three-stage tree, the venue game with Ben first, the review entry tree), as the brief asks.

## Departures from the brief, and why

- l6's (Out, Fight) question is its own screen after the tap screen (one widget per screen). The capacity screen names the cost "$k$, in £m".
- l7's rounds of deletion and "12 rounds" share one table; its crowd screen uses a plain `bars` chart of the four shares (no simulation needed: the room is given).
- l8's revenue screen asks the three numbers in one table; its trap gives £40 (half the value) as the cross-format distractor, and the reverse slip (bidding £80 in first price) is in the explanation.
- l9's drill asks the k = 1.8 best offer as a number (0) so the drill stays one table of numbers.
- l10's follow-up asks both outside offers in one table.

## Conventions

Seed 9 for the l9 winner's-curse simulation (the canvas states the exact value, £20/3). Values uniform from £0 to £100 (firms £0 to £100m); ties by coin; an indifferent responder accepts. Generators: `<scratchpad>/game-theory-2/gt.py` (helpers), `l6.py` to `l10.py`, `sets2.py`.

## Proposed course.json change

None.

## Backlog

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (game-theory level 2)".

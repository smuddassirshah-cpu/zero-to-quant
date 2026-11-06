# pairs-rep level 2 ("Trading"): report

Brief: `docs/briefs/pairs-rep.md` (preamble and `## Level 2`). Panel, normalisation and `trade_pair` conventions as in `docs/reports/pairs-rep-1.md`.

## Files

| File | Screens / items | Quiz | Interactive canvas early | Code screens |
|---|---|---|---|---|
| `l6-two-standard-deviations.json` | 10 | 3 | spread series with trigger frames 1.5 to 3 sd | `threshold`, `first_open`, `units` |
| `l7-closing.json` | 10 | 3 | spread series with open and close markers and a reveal slider | `trade_pair`, `holding_days` |
| `l8-committed-capital.json` | 10 | 3 | 127-cycle return series with top 20 / top 5 frames | `cycle_return`; `run` (step 126) and `monthly` |
| `l9-bid-ask-bounce.json` | 10 | 3 | pair of close and mid spreads with window frames; orderbook hook | `bounce_effect`, `net_of_costs`, `breakeven_cost` |
| `l10-matching-results.json` | 10 | 3 | results table with cell frames | `results_table` (step 126) |
| `review-2.json` | 9 items, `pass` 0.8 | | | |
| `homework-2.json` | 7 items: two code (full 127-cycle run at difficulty 5; `blotter`), order, longform, three others | | | |

No performance task: no level-2 objective starts with a verb from the rule (Open, Close, Compute, Account, Compare).

## Gates

1. Validator 0 errors; no warnings on pairs-rep files. Rule 581 (wrong values inside the answer band) checked by a scratch script over all pairs-rep files: no overlaps in levels 1 and 2.
2. Voice scan: 0 sentences over 20 words, 0 explanations over three sentences.
3. Numbers: `docs/reports/pairs-rep-L2-numbers.py` (shares `pairs_rep_common.py`) recomputes every stated figure independently, including a separate stop-loss, band-exit and Newey-West implementation, and runs every code widget's solution and starter. It is slow (several minutes: about a dozen full 127-cycle runs in pure Python).
4. Playthrough with `--local-cdn`: all five lessons, review-2 and homework-2 green at desktop and with `--mobile`. The homework's full 127-cycle run passes in Pyodide within `budget: 120000`.

## Numbers stated

- Pair (2, 3), first cycle: formation sd 0.0210; first open trading day 28 at spread −0.0532 (A = 1.1715, B = 1.2247; units 0.8536 and 0.8165); trips 28–43, 50–58, 86–97, 116–125, payoffs 0.0574, 0.0483, 0.0515, 0.0646, total 0.2218; holding days 15, 8, 11, 9; with the wait 0.1714. Opens at 1.5 / 2 / 2.5 / 3 sd: 6, 4, 3, 2; payoffs 0.2718, 0.2218, 0.1572, 0.1231.
- Band exit instead of crossing: pair (2, 3) 0.1955 from 9 trips; first-cycle top 20 11.27% against 14.24%.
- Forced close example: cycle from day 21, pair (48, 62), opened day 55, −0.3336. 35% of top-20 trades end at the forced close.
- Stop-loss at 4 sd, pair shut for the cycle (not in the paper): first cycle 10.68% against 14.24%; 127-cycle mean 4.32% against 6.02% a cycle.
- Returns: first cycle top 5 £0.5679 total, 11.36% / 14.20%; top 20 £2.8489, 14.24% / 14.99%. 127-cycle means per cycle 6.02% (top 20), 8.22% (top 5). Cycle from day 21: every pair opens, 9.59% both; 46 of 127 cycles have all 20 open.
- Monthly t statistics (top 20): naive 13.55, Newey-West (5 lags) 8.09; with the wait 11.09 and 6.91.
- Step 126 gives 22 cycles: monthly means top 20 1.05% / 0.82% (wait), top 5 1.43% / 1.03%, mids 0.79%.
- Bounce: closes 1.00%, mids 0.82%, wait 0.75%, mids with wait 0.75% a month; bounce 0.19 points; drift cost of the wait on mids 0.07 points. Spread's mean daily move 0.0146 on closes, 0.0119 on mids.
- Costs: 1.6886 round trips per top-20 pair per cycle with the wait; cost per pair at 0.1% per trade 0.675%; break-even 0.669% per trade; at 0.2% per trade net 0.53% a month.
- Annualised: top 20 12.7% / 9.4% (wait); top 5 17.7% / 12.8%: three of four cells above 11%.

## Brief errors recorded (not followed)

- `step = 126` gives 22 cycles (starts 0 to 2,646), not 21.
- The l7 stop-loss ladder needs a rule for after the stop; letting the pair reopen at once makes it churn (21,164 stops in 127 cycles). The course shuts a stopped pair for the rest of its cycle and says so.
- The homework full run uses `budget: 120000`, not 20000, to leave room on a slow phone; it passed in the playthrough.
- Momentum-rep l11 is named "Standard errors for overlapping returns"; the lesson links to it by that name.

## course.json

No change proposed.

## Ideas for topic-3.1 exam items

- Opening side and units from a spread sign and two normalised prices; sign-error payoff.
- Round-trip payoff from four prices; crossing against band exit.
- Last signal day with and without the wait (t + wait < n − 1).
- Committed against employed for a given total and count; dividing by shares or legs as distractors.
- Break-even cost = gross / (4 × round trips); the once-per-pair slip.
- Bounce share from close, mid and waited runs.
- Why overlapping cycles inflate a naive t statistic.
- Choosing the conservative cell to set beside a paper's headline; tuning to the target as a trap.

## Backlog

Two bullets under "Raised later (pairs-rep level 2)" in `docs/BACKLOG-INBOX.md`.

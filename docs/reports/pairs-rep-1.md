# pairs-rep level 1 ("The paper"): report

Author: content agent, wave 2 of session T. Brief: `docs/briefs/pairs-rep.md` (preamble and `## Level 1`).

## Files

| File | Screens / items | Quiz | Interactive canvas early | Code screens |
|---|---|---|---|---|
| `l1-ggr-design.json` | 9 screens | 3 | series with portfolio frames (explore) | `cycle_windows`, `live_portfolios` |
| `l2-normalised-paths.json` | 11 screens | 3 | pair of series with window frames (explore) | `normalise` + `ssd`; `ssd_matrix` |
| `l3-closest-pairs.json` | 11 screens | 3 | bars histogram of 4,950 SSDs with a cut slider (explore) | `top_pairs`; `one_partner_pairs` + `same_industry_share` |
| `l4-main-results.json` | 10 screens | 3 | bars with a slider on pairs opened, derive (explore) | `committed_and_employed` |
| `l5-plan.json` | 11 screens | 3 | series of three planted pairs' log gaps with frames (explore) | `checks`; `placebo_pairs` |
| `review-1.json` | 9 items, `pass` 0.8 | | | |
| `homework-1.json` | 7 items (two code, one order, one longform, three others) | | | `form_pairs` (difficulty 5, `performance: "code"`), `spread_stats` |

Every lesson has a trap, an edge case, a transfer screen and names Gatev, Goetzmann and Rouwenhorst (2006) once in full. "As in Replicating Momentum" appears once (l5 plan screen). "£1 a side" replaces the paper's dollar once (l4 hook). The performance task is required: l5's objective starts with "Write".

## Gates

1. Validator: `node tools/validate.mjs` 0 errors; no warnings on pairs-rep files (only "not yet written" for levels 2 and 3).
2. Voice scan (`VOICE_BASE=app/content/courses/pairs-rep/`): 0 sentences over 20 words, 0 explanations over three sentences.
3. Numbers: `docs/reports/pairs-rep-L1-numbers.py` exits 0, 144 of 144 checks (it imports `docs/reports/pairs_rep_common.py`, an independent second implementation: pairwise-difference SSDs, tuple sorting, a day-by-day trading state machine; plus every code widget run in CPython: solution passes all hidden tests, starter fails at least one).
4. Playthrough with `--local-cdn` (this session's pkgs): every lesson, review-1 and homework-1 green at desktop and with `--mobile`. Screenshots looked at (series frames, pair windows, bars cut, scatter, tables at 440 px); one fault fixed (the l5 explore first plotted six price lines whose hidden series still set the y range, so the break was hard to see; it now plots each pair's log gap).

## Seed and data conventions

- Panel: the brief's `pairs_panel()` with seed 2006, verbatim in every prelude that needs data; NumPy only.
- Normalisation once at the formation start, carried through the 126 trading days; sd is `np.std` (ddof 0).
- `trade_pair`: opens when |spread| > 2 sd and `t + wait < n − 1`, closes at the first sign change or the last day, and resumes scanning the day after the exit. With this resume rule our CPython values match every reference value in the brief (the brief does not state the rule; resuming the day after the crossing signal gives 11.91% instead of 11.73% for the first-cycle top 20 with a wait).
- Planted pairs never broken (seed 2006): pairs 4, 7, 16 (shares 8 and 9, 14 and 15, 32 and 33), as the brief says.

## Numbers stated (all recomputed by the script)

- First formation: top 20 = the 20 planted pairs; closest (2, 3) SSD 0.1117, sd 0.0210 (trading-period sd 0.0300); 20th SSD 0.6717; 21st 0.9989; median 19.69; 21 pairs below SSD 1.
- First cycle: top 20 committed 14.24%, employed 14.99%, 19 opened, total payoff £2.85; top 5 11.36% and 14.20%, 4 opened; pair (2, 3) 4 round trips, payoff 0.2218; fifth closest pair never opens.
- 127 cycles, monthly committed (employed): top 20 1.00% (1.12%), wait 0.75% (0.84%); top 5 1.37% (1.59%), wait 1.01% (1.17%); pairs 101 to 120 0.18% (0.18%), wait 0.08% (0.08%); share of pairs that open 89%, 92%, 95%; mid prices top 20 0.82%; no cycle with zero opened pairs.
- Annualised: 0.75% a month 9.38%; 0.84% 10.56%; 1.00% 12.68%.
- Late formations: start 1,512 top 10 repeats shares 15, 32, 80, 94 (10 repeated shares in the top 20; same-industry share 0.35; top 8 0.375); start 2,016 has 3 planted pairs in the top 20.
- Rank correlation of distance against next-period profit: −0.18 over all 4,950 pairs, −0.04 over the closest 200, 0.04 inside the top 20.
- Placebo (20 random pairs, first cycle): seed 0 −0.0393 on closes, −0.0307 on mids; mean of 200 seeds −0.0100 on closes, −0.0113 on mids.
- Toy values: SSD 0.0014, sd 0.0137 (n − 1 gives 0.0151, root mean square 0.0153); φ = 0.9170 for half-life 8.

## Brief errors recorded (not followed)

- The l5 trap says that on closes with no wait "even random pairs show a small profit from the bounce". They do not: random pairs lose about 1.00% a cycle on closes and 1.13% on mids (200 seeds). The bounce lifts them by about 0.13 points but leaves them negative. The lesson states this and puts the bounce on the top-20 run (1.00% on closes against 0.82% on mids).
- Homework `form_pairs` was to be tested at starts 0 and 1,134, but both rules give identical lists there; a test at start 2,016, where the rules differ, was added.
- The scatter of distance against profit uses the 200 closest pairs, not all 4,950 (a 4,950-point SVG is heavy on a phone); rank correlations for all three sets are stated.
- Scratchpad paths in the brief are stale; this session's were used.

## course.json

No change proposed.

## Ideas for topic-3.1 exam items

- Formation against trading: which statistics may use which days; the look-ahead of a trading-period sd.
- Counting: N(N − 1)/2 pairs; six overlapping portfolios from 126 / 21.
- SSD by hand on a short toy pair; the spread's sd with ddof 0 against n − 1.
- Committed against employed capital; employed / committed = k / n; the 0 / 0 rule.
- Compounding a monthly return (0.75% to 9.4%) and the multiply-then-compound slip.
- Distance is not correlation (doubled log returns, correlation 1, levels drift).
- The closest pair need not trade; the one-partner rule on a short list.
- Placebo and mid-price runs separating skill from the bid-ask bounce.

## Backlog

Three bullets under "Raised later (pairs-rep level 1)" in `docs/BACKLOG-INBOX.md`.

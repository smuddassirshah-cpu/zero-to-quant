# momentum-rep level 2 (Data and portfolios): report

## Files written

All in `app/content/courses/momentum-rep/`, ids, titles, objectives and skills from `course.json`, £ for money.

| File | Screens / items | Skills | Canvases | Code |
|---|---|---|---|---|
| `l6-data-you-can-get.json` | 12 screens, 4 quiz | `rm-data` | table (sources; tap the gaps), console (generator lines, NaN argsort, loader) | `load_panel`, `drop_short_history`, `survivor_bias` |
| `l7-winners-and-losers.json` | 12 screens, 4 quiz | `rm-portfolios` | scatter (month 100, 500 shares, fit), bars (ten deciles, no skip / skip frames), number-line (toy returns), console, grouped bars (transfer) | `formation_returns`, `cohort_weights`, `decile_means` |
| `l8-overlapping.json` | 12 screens, 3 quiz | `rm-portfolios` | table (one share's live cohorts), series (cumulative 6/K composite, K frames), bars (turnover by K) | `wml`, `n_obs`, `composite_turnover` |
| `l9-skip-month.json` | 11 screens, 3 quiz | `rm-portfolios` | console (generator), series (event-time spread, holding-window frames), table (no skip → skip; skip − no skip) | `skip_effect`, `reversal_spread` |
| `l10-matching-the-table.json` | 12 screens, 3 quiz | `rm-portfolios`, `rm-stats` | pair of series (6/6 and 12/3), table (4 × 4 with a skip control), table widget (gaps in se) | `jk_table`, `seed_spread` |
| `review-2.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | every lesson, skills tagged | | none |
| `homework-2.json` | 7 items, difficulty 3 to 5 (two at 5) | `rm-data`, `rm-portfolios`, `rm-stats` | | `wml_all` (5, `performance: "code"`, the level's one task: l8's objective starts "Build"), `decile_spread_by_month` (4); `order` with a distractor (4); `multi`; `longform` (5, 10-point rubric, full model answer: the Data and method section) |

Every lesson: hook, explore with a canvas-bound widget or control, a named term, ladders, a trap with a `byKey` line on the misconception, a generalise screen with the formula, code screens, a quant transfer. Edge cases: NaN ranked last by argsort (l6), n not divisible by q (l7), the first K − 1 months (l8), the 3/3 cell (l9), a hypothetical free-data cell above the paper (l10).

## Gates (SESSION PROTOCOL 4)

1. Validator, from `app/`: `0 errors`. My files carry two warnings, both "a ladder usually reuses the previous canvas kind" (l7 screen 3 number-line after bars; l8 screen 4 turnover bars after the series), kept on purpose.
2. Voice scan on the seven level 2 files: 0 sentences over 20 words, 0 explanations over three sentences. On the whole course folder it reports 7 and 3, all in level 1 files (`homework-1` model answer, `l1` table rows, `l4` screens 6 and 7, `l5` screens 4 and 8); I did not edit level 1. **Main session: route these to a level 1 fix pass.**
3. `docs/reports/momentum-rep-L2-numbers.py`: exits 0, 186 of 186 `expect` checks, every two-route agreement, 15 code widgets (every solution passes its hidden tests in CPython, every starter fails at least one).
4. Playthrough with `--local-cdn` (this session's `pkgs`): every lesson, `review-2` and `homework-2` pass without `--mobile` and with `--mobile` (l6 16 checks, l7 16, l8 15, l9 14, l10 15, quizzes all right; review 9 of 9; homework 7 of 7, 34 of 34 marks, the performance starter fails, the longform marked through the button). Screenshots at 1280 and 440 inspected; fixes made: console lines cut off at 440 (now `wrap: true`), the toy sort screen's irrelevant bar chart pushed the table off the phone screen (now a number-line of the ten returns).

Follow-up before hand-back (main session note on rule 581): every numeric `wrong` value is now outside its answer band (review-2 item 8's "gap in points" slip sat inside the band and was removed), negative numbers in prose use the minus sign, and four explanations that stated a rule without its conditions were qualified. Validator, voice scan, numbers script and playthrough were rerun after the change.

## Numbers and how each was computed twice

Route 1: the reference functions the preludes load (loop `formation_returns`, double stable argsort, averaged cohort weights). Route 2 (in the numbers script): cumulative-log formation returns, ranks by one argsort and a scatter, the composite as the mean of each live cohort's own spread, turnover from a cumulative sum of weights. Route 3: Pyodide, through the playthrough, for every code-test value (test `expect` values were produced by running each solution in CPython; no hand-typed expect survives).

| Number | Value | Where |
|---|---|---|
| Base panel mean monthly return | 1.52% | l6 loader |
| One-month spread (J = 6) with all shares / bottom 20% by total return dropped | 0.52% / 0.35% (base); 0.46% / 0.36% (n = 200, T = 120) | l6 screens 10, 11, quiz |
| Month 100 slope, R² | 0.025, 0.0034 | l7 hook |
| Decile means J = 6, next month, no skip | 1.21, 1.45, 1.26, 1.63, 1.46, 1.39, 1.67, 1.55, 1.60, 1.72%; D10 − D1 0.52% | l7 explore, decile code, quiz |
| Same with one-month skip | 0.88 … 2.07% | l7 explore |
| Look-ahead bug (window t − 5 to t) | 17.06% a month | l7 trap |
| 6/K composite, J = 6, K = 3, 6, 9, 12 | 0.91, 0.96, 0.91, 0.77%; 292, 289, 286, 283 months; £1 → £6.96, £9.60, £9.16, £6.27 | l8 explore |
| 6/6: mean, sd, n, t | 0.96%, 5.98%, 289, 2.74; summed six cohorts 5.78% | l8, l10 |
| Non-overlapping 6-month blocks over 300 months | 49 | l8 |
| Composite turnover J = 6, K = 1, 3, 6, 12 (buys plus sells) | 1.577, 0.866, 0.577, 0.293; one-sided 6/6 0.289 | l8 |
| Monthly cost, £10m a leg, 25 bp | 0.0025 × 0.577 × £10m ≈ £14,429 | l8 transfer |
| 1/1 spread | −0.88%, t −2.08, 299 months | l9 |
| Event-time J = 6 spread, months 1 to 12 | 0.56, 1.28, 1.03, 1.43, 0.89, 0.60, 1.04, … %; months 1–6 sum 5.78%, 2–7 sum 6.26%, 282 formation months | l9 explore |
| Skip minus no skip, 4 × 4 | +0.35 at 3/3 … −0.11; nine cells negative | l9 |
| 6/6 and 12/3 with skip | 1.04%, 1.35% | l9, l10 |
| se of 6/6, of 12/3 | 0.352%, 0.413%; gaps to the paper 0.04 and 0.01 se | l10, review |
| Rank of 6/6 among 16 no-skip cells | 5 (after 12/3, 9/3, 9/6, 12/6) | l10 |
| 6/6 across seeds 1 to 7 | 0.91, 0.96, 0.83, 0.87, 0.37, 0.48, 1.46%; range 3.1 se; sd 0.35% | l10 |
| 12/3 band at 2 se | 0.49% to 2.14% | l10 generalise |
| Net 6/6 at 25 bp a side | 0.964% − 0.144% = 0.820% | homework |
| Small arithmetic (4/300 = 0.0133, 505 deciles 51/50, 12/12 skip 276 months, 23 decile sizes 3/2, (1.40 − 0.95)/0.35 = 1.3) | | review, quizzes |

All the course-context reference values used here (the 4 × 4 tables, 0.0096, 0.0598, 289, t 2.74, −0.0088 and −2.08, 0.577, 0.37% to 1.46%, 0.82%) agree with my CPython values to the places stated. Pyodide agreed on every code test.

Paper figures quoted, always as "the paper reports": 6/6 about 0.95% a month; 12/3 about 1.31%, the most profitable; skipping a week raises every cell a little; NYSE and AMEX, CRSP. Later paper named: Jegadeesh (1990) on short-term reversal, one sentence (l9), as the brief directs.

Made-up numbers, labelled on screen: the two signals in l7's transfer, the delisting example's −60%, the colleague's 0.70% and 18 designs, the free-data 1.40% cell, the review's 1.10% against 0.30%.

## Seeds and conventions

- Generator verbatim in every prelude; base panel `momentum_panel()` (seed 2, 500 × 300); code tests on `momentum_panel(n=200, T=120)` (seed 2) unless stated, `n=60, T=40` for the decile homework item.
- Preludes are layered so a learner's slip never leaks: a screen that asks for a function never has it in its prelude (generator only for `formation_returns`; plus it for `cohort_weights`; plus both for `wml`, `decile_means`, `composite_turnover`, `wml_all`; all four after l8).
- Turnover: sum of |change in composite weight| month to month, no drift, both legs; costs charged on that amount. Alpha's one-sided figure named once.
- Survivorship plant: shares whose total log return is below the 20% quantile are "dead" for the whole sample.

## Departures from the brief

- l7 toy cross-section has 10 shares in quintiles of two, not 20: a 20-row table widget does not fit a phone screen beside its canvas.
- l8 non-overlapping count is 49, not the brief's 48: (300 − 6) // 6 full blocks after the first ranking. The code tests this definition.
- l9: on our panel the skip lowers nine long-K cells (down to −0.11 points), unlike the paper's "every cell a little". The lesson teaches why (month K + 1 replaces month 1) and says the panel differs from the paper here. The J = 6 event-time month 1 is positive (0.56%), only the lowest of months 1 to 6; the reversal itself is shown with the 1/1 spread.
- l7 decile means without a skip are not monotone (dips at D3, D6, D8); the explore shows both rankings and says so.
- l10: the brief's "the paper's long-K cells fall less" is not stated, because it is not in the quotable list; only the two quoted cells are compared. The edge case is a hypothetical free-data 6/6 of 1.40%, since "higher than the paper because no costs" would be wrong (JT's spreads are also gross).
- The look-ahead bug gives t 41.35 with my window; level 1 says 41.20. Both levels quote only 17% a month.
- `decile_spread_by_month` is defined as the ten equal-weighted decile composites by month (D10 − D1 = `wml`), so it is not a copy of `wml`.

## Proposed course.json change

None.

## For the topic-3.1 exam (levels 2 and 3)

See the level 3 report if written; from level 2: (1) survivorship biases the momentum spread down, delisting returns either way; (2) NaN ranked last by argsort turns gaps into winners; (3) composite weight = average of K cohort weights (4/300); (4) T − J − skip − K + 1 months against (T − J − skip) // K blocks; (5) summing cohorts is K-fold leverage; (6) the skip swaps holding month 1 for month K + 1; (7) gaps judged in standard errors with a rule fixed first, and the seed range ≈ the standard error.

## Backlog

Three bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (momentum-rep level 2):".

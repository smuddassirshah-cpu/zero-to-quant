# pairs-rep level 3 ("Beyond the paper"): report

Brief: `docs/briefs/pairs-rep.md` (preamble and `## Level 3`). Panel, normalisation, `trade_pair` (resume the day after exit) and `run` conventions as in `docs/reports/pairs-rep-1.md` and `-2.md`. Builders and Pyodide checks live in the scratchpad folder `pairs-rep-3`.

## Files

| File | Screens / items | Quiz | Interactive canvas early | Code screens |
|---|---|---|---|---|
| `l11-why-profits-fell.json` | 11 | 3 | 127-cycle series with a 12-cycle mean and a break marker, frames same day / wait | `planted_in_top` + `split_means`; `convergence_share` |
| `l12-cointegration-selection.json` | 11 | 3 | series of two pairs' formation prices with frames; tap-rows table of the top 20's p-values | `eg_pvalue` (statsmodels); `coint_pairs` + `false_positive_count` (statsmodels) |
| `l13-just-a-factor.json` | 11 | 3 | scatter of 22 cycles against the market with a slope control and live SSE | `market_by_cycle`; `pairs_alpha` (statsmodels OLS) |
| `l14-out-of-sample.json` | 11 | 3 | tap-cells table of the in-sample grid | `sweep`; `held_out` |
| `l15-pairs-note.json` | 10 | 3 | console draft note, tap the overclaiming line | `survival_sentence` |
| `review-3.json` | 10 items, difficulty 2 to 4, `pass: 0.8` | | | |
| `homework-3.json` | 7 items, difficulty 3 to 5 (two at 5) | | | `compare_selection` (5, `performance: "code"`, statsmodels, `budget: 40000`), `rolling_hit_rate` (4); `order` with two distractors; `longform` note (10-point rubric, one required row) |

Skills as the brief says (`pr-extend` everywhere, `pr-method` on l12, `pr-returns` on l13). Gatev, Goetzmann and Rouwenhorst (2006) named once per lesson; Do and Faff (2010) once, in l11's trap. Edge cases: the three unbroken pairs (l11), a hedge ratio of 2 (l12), a hedge that is not 1 to 1 (l13), a setting that rose out of sample (l14), a note where nothing survived (l15). The performance task is required: l15's objective starts with "Write".

## Gates (SESSION PROTOCOL 4)

1. Validator from `app/`: 0 errors; no warnings on level 3 files.
2. Voice scan (`VOICE_BASE=app/content/courses/pairs-rep/`): 0 sentences over 20 words, 0 explanations over three sentences.
3. `docs/reports/pairs-rep-L3-numbers.py` exits 0: 472 of 472 checks, about a minute (NumPy, statsmodels). Second route: `pairs_rep_common.py`'s state machine for distance trading, its own loops for convergence and for trading a cointegration residual, OLS by hand, statsmodels `coint` called directly. Every code widget: solution passes, starter fails (raises cases included); `lv.check_wrongs()` run.
4. Playthrough with `--local-cdn` and `--mobile --tablet`: all five lessons, review-3 (10 of 10) and homework-3 (7 of 7, 34 of 34 marks, performance starter fails, longform marked by the button). Also green without `--mobile`. Screens looked at at 440 and 1280 px; fixes: the histogram's hline label overprinted bars (shortened), the l15 results table was cramped at 440 px (three columns), l12 tap table capped with `maxHeight`.

Pyodide against CPython: every statsmodels figure in a test or the prose was recomputed in Pyodide 0.27.7 (statsmodels 0.14.4) in node and agrees exactly (p-values to 4 places, the 407 count and the histogram, OLS to 4 places, `compare_selection`). Timings: statsmodels and its dependencies load in 3 to 6 s from the local CDN in node, and a statsmodels lesson plays about 9 s slower than a NumPy one (l12 36 s against l11 27 s). Engle-Granger on 50 pairs: 0.6 to 0.8 s in Pyodide, 0.3 s in CPython; on all 4,950 pairs: 56.5 s in Pyodide, 30 s in CPython, so lessons test the 50 closest only.

## Numbers stated (all recomputed by the script)

- Split, monthly committed: top 20 same day 1.50% before, 0.64% after (42% survived); with the wait 1.14% and 0.48% (42%); top 5 1.68% / 1.19% (71%), wait 1.28% / 0.88% (69%). Before = 55 cycles whose trading ends by day 1,512; after = 67 that start trading on it or later; 5 straddle. 22 cycles (step 126): 1.53% / 0.64%.
- Planted pairs in the top 20 at starts 0, 1,134, 1,512, 2,016, 2,646: 20, 16, 4, 3, 3. `break_frac = 0.3`: 9 pairs break, after 1.07% a month against 1.50%; 10 and 9 planted at 1,512 and 2,016.
- Convergence (trades closed at a crossing), same day: 1,458 of 1,895 before (77%), 1,158 of 2,159 after (54%); wait 1,458 / 1,882 and 1,155 / 2,143. One cycle: start 0, 47 of 49; start 2,016, 18 of 33; top 5 at 2,016, 7 of 9.
- After the break, per pair-cycle: unbroken 195, 10.45%, 80% converged; broken 77, 7.13%, 62%; chance 1,068, 2.37%, 47%; unbroken before 9.89%.
- l12, start 0: distance top 20 all planted, 5 fail Engle-Granger at 5% (p up to 0.3040); Engle-Granger from the 50 closest picks 10 planted (distance 20), committed 12.83% against 14.24%; at 2,016 both pick 3, 7.32% against 7.22%. 22 cycles: Engle-Granger 0.63% a month, distance 1.05%. All 4,950 pairs at start 0: 407 pass at 5%, 15 planted (247.5 expected under the null). Explore pairs (38, 39): SSD 0.1557, rank 2, p 0.2955; (28, 87): SSD 1.1452, rank 23, p 0.0009. Trap pair (12, 13) at start 1,260: p 0.0009, trading z reaches −9.7, ends −7.9. Hedge-2 toy: SSD 2.86, rank 177, slope 1.99, p 0.0002.
- l13 (22 cycles, same day): α 0.0623 a cycle (1.04% a month), se 0.0088, t 7.11; β 0.0529, se 0.0816, t 0.65; R² 0.021. Wait: α 0.0489, β 0.0434, t 6.31. 127 overlapping cycles: t 13.48. Residual correlation top 5 against pairs 21 to 40: −0.12 (raw −0.14) on 22 cycles, −0.07 (−0.08) on 127. With the wait 24 of 127 cycles lose money, worst −10.8%.
- l14 (wait, step 126; 10 in-sample and 12 held-out cycles): best in-sample 1.5 sd, k = 10, 1.97% → 0.55% (28%, fall 1.42 points, the largest); paper's setting 1.19% → 0.51% (43%); best held-out cell 1.5 sd, k = 5, 1.20%; only 3 sd, k = 5 rises, 0.43% → 0.45%.
- l15: 0.7531% a month, 4.52% a cycle, 9.4% a year; 1.6886 round trips; break-even 0.67% per trade; 5,000 shares give 12,497,500 pairs, 2,525 times 4,950.
- Homework `compare_selection` (planted distance, planted EG, committed distance, committed EG): start 0 (20, 10, 0.1424, 0.1283); 2,016 (3, 3, 0.0722, 0.0732); start 0 with k 5 (5, 5, 0.1136, 0.1819); 1,134 (16, 11, 0.0766, 0.0441).

## Brief errors and choices (recorded, not followed)

- "Cycles formed after the break (start ≥ 1,260)": a start-1,260 cycle is formed before the break and trades after it. The 0.64% and 0.48% are for cycles trading after the break; cycles formed after it (start ≥ 1,512) give 0.58% and 0.42%. The lessons say "start trading on it or later".
- "At 5% about 250 false positives": 247.5 is the null expectation. The panel gives 407 passes with 15 planted, so 392 chance passes; on mids 361 pass (16 planted). The lessons state the expectation and the observed count, and no cause.
- "4,950 times more pairs" on real data: the multiple depends on N; 5,000 shares give 2,525 times as many. The lesson states that figure.
- "The best in-sample setting usually falls furthest": true here, but its held-out 0.55% still edges the paper's setting's 0.51%. Stated as found.
- `split_means(results, split_start)` is written `split_means(results, break_day=1512)`: one split start cannot drop the five straddling cycles.
- Cointegration trading: `trade_coint` (in the prelude) uses `coint`'s `positions(z, 2.0, 0.0, inf)`, so the exit is a crossing as in distance; the brief's `positions` stop at 4 would add a rule the paper lacks. The `coint` helpers are copied verbatim (`eg_decision`'s import moved inside it).
- Scratchpad paths in the brief are stale; this session's were used. The brief's "no git write commands" is superseded by the orchestrator's commit instruction.

## course.json

No change proposed.

## Ideas for topic-3.1 exam items (from level 3)

1. Survival share after / before, the points-against-share slip, and "None of the effect survived" for a ratio at or below 0.
2. Convergence share pooled over trades (51 / 90) against the average of cycle shares; what it says about crowding against broken pairs.
3. Expected chance passes n × α: 4,950 at 5% is 247.5; a 50-pair shortlist 2.5; 450 within-industry pairs 22.5.
4. Distance fixes a 1 to 1 hedge; Engle-Granger estimates it; a fund with twice its index's moves ranks 177th by distance.
5. Factor regression: predict α + βR_m; why β is near 0 for £1 against £1; net industry exposure 1 − h for a hedge h.
6. Overlapping cycles inflate a plain OLS t (7.11 on 22 against 13.48 on 127).
7. Counting in-sample cycles under a lock (start + 378 ≤ split day); choosing on the held-out half makes it in sample.
8. A formation p-value is not a promise: the planted break the day trading begins.

## Backlog

Three bullets under "Raised later (pairs-rep level 3)" in `docs/BACKLOG-INBOX.md`.

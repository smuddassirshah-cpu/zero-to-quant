# coint level 3 (Pairs trading): report

The content agent was stopped by a container restart before it reported, and its scratchpad generators were lost. This report is from a triage pass: every file kept, every stated number recomputed independently, a handful of targeted fixes. Nothing was regenerated. Triage scratch work is in `coint-3` of the session scratchpad (`c1.py` to `c8.py`, `harness.py`, `voice.py`).

## Files

All in `app/content/courses/coint/`. Verdict: kept, all six.

| File | Screens or items | Quiz | Code screens | Notes |
|---|---|---|---|---|
| `l9-entry-exit.json` | 12 screens (difficulty 1 to 3) | 4 | 2: `positions`; `trade_log` with `round_trip_pnl` | skill `co-pairs`; 14 minutes |
| `l10-backtesting-a-pair.json` | 12 screens | 3 | 2: `rolling_fit`; `daily_pnl` with `backtest` and `lookahead_backtest` | skill `co-pairs`; 15 minutes |
| `l11-breakdown.json` | 12 screens | 3 | 2: `rolling_adf_pvalues` with `stop_day`; `rolling_half_life` with `drawdown_stop` | skills `co-pairs`, `co-test` |
| `l12-real-pair.json` | 12 screens | 3 | 2: `pair_report`; `train_test_backtest` with `is_tradable` | skills `co-test`, `co-spread`, `co-pairs`; says on screen 1 that the pair is simulated |
| `review-3.json` | 8 items: 1 at difficulty 2, 5 at 3, 2 at 4 | | | covers l9 to l12 |
| `homework-3.json` | 9 items: 2 at 3, 5 at 4, 2 at 5 | | 2 (`cost_table` with `breakeven_bp` d4; `pairs_pipeline` d5) | one `order` (d3), one `multi`, one `longform` (d5, rubric sums to 10, full model answer) |

Each lesson has a hook, an explore screen with a live control, one `trap`, a generalise screen and a transfer screen. Edge cases: l9 (z exactly 2.0; a jump from 1.9 to 4.2 past the stop), l10 (NaN z before day 249; the cost of a two-leg round trip), l11 (a healing shock and the 20-seed false-alarm count), l12 (levels against logs).

## Validator

`node tools/validate.mjs`: 0 errors, 328 warnings overall. Warnings on these files: three "a ladder screen usually reuses the previous canvas kind" (l10 s10, l11 s7, l12 s8).

## Playthrough

`node tools/playthrough.mjs --lesson|--set coint/<id> --local-cdn <scratchpad>/pkgs`, run before and after the fixes below. Set mode was run alone.

- l9: ok, 16 checks, quiz 4/4
- l10: ok, 15 checks, quiz 3/3
- l11: ok, 15 checks, quiz 3/3
- l12: ok, 15 checks, quiz 3/3
- review-3: ok, 8 of 8 recorded
- homework-3: ok, 9 of 9, 40 of 40 marks

## Numbers checked

Second computation: CPython 3.13, NumPy 2.5.3, statsmodels 0.15.0, with my own code (`roll_ols` by cumulative sums, which matches `rolling_fit` to 1e-10, and a separate event-loop backtest `bt2`) and the generators from the level's preludes. The first computation is the Pyodide 0.27.7 playthrough, which runs every solution against its hidden tests, so each expected value in the tests was checked in both. All values below agree to the places shown, except the ones listed under Fixes.

**l9** (`make_pair(3, 1500)`, window 250, entry 2, exit 0, stop 4, 5 bp)
- Default: P&L £28.56, Sharpe 1.124, 25 changes, costs £2.64.
- Entry 1 to 3 in steps of 0.25 (the caption table): Sharpe 1.104, 0.920, 1.060, 1.088, 1.124, 1.105, 0.912, 0.959, 0.784; changes 65, 45, 39, 33, 25, 18, 14, 10, 4; P&L £40.74, 31.73, 33.33, 31.53, 28.56, 23.20, 16.97, 13.94, 6.24.
- Exit +0.5, 0, −0.5: Sharpe 1.172, 1.124, 0.944; changes 31, 25, 23; P&L £23.96, 28.56, 29.04; costs £3.37 against £2.64.
- Halves (days 0 to 749, 750 to 1,499), all nine bars of each group: first-half best entry 2.75 at 0.978 (entry 3 has no trade); second half at 2.75 is 0.976; second half at 2 is 1.314.
- The 30-day path: entries on days 5, 15, 24, closes on 11, 20, 28; trade 1 P&L £2.01 (−(−0.84 − 1.5 × 0.78)); the jump case 1.9 to 4.2 stays flat, then opens a short at 3.1.
- Reference log: 13 round trips, the last open on day 1,499; the first opens on day 272 at β 1.8653 and earns £3.2461 (£3.25).
- Quiz: £0.90, £1.26.

**l10**
- Look-ahead backtest: P&L £37.29, Sharpe 1.647, 22 changes; gap £8.73 and 0.52; full-sample β 1.4888.
- Costs 0, 5, 10, 20, 40 bp: £31.21, 28.56, 25.92, 20.63, 10.05 and Sharpe 1.218, 1.124, 1.025, 0.817, 0.387; £0.5289 a basis point, break-even 59.0 bp; the frame series end at those values and differ from mine by under £0.005.
- Windows 60, 120, 250, 500: Sharpe 0.841, 0.931, 1.124, 1.155; changes 72, 39, 25, 16.
- `rolling_fit`: day 249 gives α −6.6979, β 1.8033, sd 1.3645; day 1,000 gives 13.8278, 1.3850, 1.5695.
- Sharpe standard error: 1,251 days = 4.96 years, se 0.449, t = 2.50, band 0.24 to 2.00; round trip £0.155; quiz £0.041 and 1.56.
- The re-hedging variant (spread y − β_t x, 60-day rolling z, daily re-hedge at yesterday's β, no costs): £−4.44, Sharpe −0.1149.

**l11** (`make_broken_pair(3)`)
- P&L £18.01 on days 0 to 999 and −£16.89 on days 1,000 to 1,499; final £1.12; peak £29.66 on day 1,141; maximum drawdown £31.06.
- Engle-Granger p: 0.0001 (9.4e-5) and 0.9456.
- Rolling ADF p (ends 250 to 1,500 step 125): 0.0643, 0.0585, 0.1551, 0.0286, 0.0102, 0.1683, 0.0717, 0.7239, 0.5028, 0.7608, 0.9548; also the two other test sets.
- Rolling half-life: 12.2, 10.05, 16.49, 8.41, 5.96, 14.61, 13.76, 44.64, 30.24, 52.43, ∞; days 0 to 999 give 13.29, so the limit is 39.9.
- Rules: one check above 0.10 fires at 500 keeping £10.43; half-life above 39.9 fires at 1,125 keeping £29.22; two checks above 0.5 fire at 1,250 keeping £29.46; the £15 loss limit fires on day 1,390 at £14.46, saving £13.34; never stopping ends at £1.12.
- Healing shock (£6 fading 1% a day): checks 0.5637 and 0.5021, fires at 1,250, trading on earns £5.91 more.
- Seeds 3 to 22 of `make_pair(seed, 1500)`: the two-checks rule fires once (seed 7, at 375).
- The broken spread falls as low as −£50.16 after day 1,000.

**l12** (`make_share_pair()`)
- Prices: A £25.47 to £24.87 (low £8.48 on 2019-05-24), B £34.05 to £34.16 (low £11.80).
- ADF levels 0.5216 and 0.4716, changes 0.0000.
- β̂ 1.2370, α̂ 2.1999.
- Engle-Granger −7.5196 (p 5e-10), critical values −3.901, −3.339, −3.046; halves −5.606 and −5.8962; logs −7.85.
- Residual fit b −0.04418 (se 0.005876); half-life 15.34, interval 12.10 to 20.88; true 22.76.
- Gap sd £1.01 at β 1.24, £1.91 at 1.0, £2.68 at 1.6.
- Entries 1, 1.5, 2, 2.5, 3: first-half Sharpe 0.801 at 2.5 and so on as in the bars (1.540, 1.155, 1.257, 0.801, 0.701), second half 1.383, 1.253, 1.278, 1.271, 0.810. Choice 1.0, test 1.383. Entry 2: P&L £17.00 and £16.74, costs £1.40.
- Calls: `train_test_backtest(y, x, 750, [2.5, 3.0])` gives (2.5, 0.448, 1.27); with the nine entries (2.75, 0.978, 0.976).
- Pair report on the first 1,260 days: β 1.2138, −5.606, half-life 12.4408. Pair C: 1.4744, 6.4908, −5.1315, 13.2877. Pair A: p 0.80.
- Quiz: 22.8 days; shortcut 23.1.

**Review**: positions 0, +1, +1, +1, 0; £1.26; 15 bp gives £23.28 (23.29 from the rounded figures); drawdown fires at close 7; ADF run fires at check 6; the leg check and `is_tradable` logic.

**Homework**
- Round trip £0.144; break-even 59.0 bp (answer 59.1 ± 0.3); the best-of-nine bar 1.14 (z 2.5392 over √4.96).
- `cost_table` and `breakeven_bp`: pair 3 59.0 bp, pair 5 £40.45, £34.85 and 72.2 bp, share pair £33.74, Sharpe 1.267, 125.1 bp.
- `pairs_pipeline`, my own implementation from the docstring: pair 3 (10.56, 1.24, 9, no stop); pair 5 (14.99, 1.806, 16); pair 7 (10.34, 1.463, 12); broken pair (11.45, 0.799, 14, stop day 1,249, loss limit would fire on 1,390); with an 800-day formation the check at 1,300 reads 0.1367 and the loss limit fires first (2.69, 0.103, 19, 1,390); a £2.50 limit on pair 3 (1.74, 0.439, 3, 1,255); pair A refused.
- Longform model: formation ADF 0.7883 and 0.7046, β̂ 1.2138, −5.606 against −3.905, half-life 12.44, 37 days = 3 × 12.4, t = 3.09 for 1.383 over 5 years.

## Starters

Each solution passes all its hidden tests in CPython (statsmodels 0.15.0) as well as in Pyodide. Each starter fails the Check; it passes only the cases that the written part or an empty result already covers. Starter passes, out of the tests: l9 `positions` 3 of 11 (the short side is written for the learner), `trade_log` 1 of 9, l10 `rolling_fit` 0 of 9, `daily_pnl` 0 of 10, l11 `rolling_adf_pvalues` 1 of 9, `rolling_half_life` 2 of 9, l12 `pair_report` 0 of 8, `train_test_backtest` 0 of 10, homework `cost_table` 1 of 8 (the empty list), `pairs_pipeline` 1 of 9 (pair A returns `None`).

## Fixes made

Screens and items are numbered from 1, as the player shows them. All are targeted text edits; no graded answer was changed except the one in the last item.
- l9 s1 `byKey.long`: "Days 15 and 20 are a dip" read as if day 20 were below −2; it now says they open and close the dip.
- l10 s9 (re-hedging variant, prose): the Sharpe was −0.12; the computation gives −0.1149, so −0.11. The brief's −0.12 does not reproduce (the P&L −£4.44 does).
- l10 s9 and homework item 8: "a price near £65 ... £0.15" did not follow from 0.0025 × 65 = 0.1625. The mean price on days with a β is £69.4 and the mean change in β is 0.00252, giving £0.175. Now "near £70" and "about £0.17" (option, hint, arithmetic and explanation in l10; option and explanation in the homework).
- l11 s1 option `why`: "wanders by up to £40" now £50 (the spread reaches −£50.16).
- l12 s2 explanation: the gap sd at β 1.6 is £2.675 with `ddof=1`, so £2.68, not £2.67.
- l12 s12 prose: one sentence added pointing to Tsay chapter 8 and Chan's *Algorithmic Trading*, as the brief asked.
- homework item 4 (best of nine): the wrong-answer value for "one pre-set rule" was 0.88 = 1.96/√4.96, but the item's own formula is one-sided, so one rule needs 1.645/√4.96 = 0.74 (the Testing course's lesson 11 gives 0.74 for one strategy over 5 years). The `wrong` entry `one` now has value 0.74, and its `byKey` line and the explanation say 0.74. The correct answer, 1.14, did not change.
- Homework item 9 (longform): three sentences over 20 words split, "either share" for the short-sale assumption, and the prompt split in two. No rubric or number change.

## Open issues

- Re-hedging variant (l10): the brief's −0.12 Sharpe could not be reproduced; the P&L matches exactly. The stated −0.11 follows the same convention as the other Sharpe figures (daily P&L over all 1,500 days, ddof 1).
- The drag on l9 s2 moves only the entry; exit and stop are shown on the series, not dragged.
- l12 s7 shades the formation and trading years by sampled weekly dates, so the formation shade ends on 2019-10-25 (day 1,255), not day 1,259.
- No change to `course.json` is proposed.

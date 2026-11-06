# momentum-rep level 3 (Evidence and extension): report

## Files written

All in `app/content/courses/momentum-rep/`, ids, titles, objectives and skills from `course.json`, £ for money.

| File | Screens / items | Skills | Canvases | Code |
|---|---|---|---|---|
| `l11-overlapping-errors.json` | 12 screens, 3 quiz | `rm-stats` | bars (t under three methods; autocorrelation lags 1 to 8, cohort series / composite frames), table widget ((6 − j)/6) | `overlap_returns`, `nw_t` (statsmodels), `nw_t_by_hand` |
| `l12-adjusting-for-risk.json` | 12 screens, 3 quiz | `rm-stats` | scatter (spread on market, base panel; 24 months after the crash, fit), series (rolling 24/60-month beta, frames), table (OLS output) | `factor_alpha` (statsmodels), `rolling_beta` |
| `l13-after-publication.json` | 12 screens, 3 quiz | `rm-extend` | series (cumulative 1965 to 2004 with "published" and "crash" markers; rolling 60-month mean with a reveal slider), distribution (180-month mean, observed marked, 0.5% overlay) | `pre_post`, `subperiod_means` |
| `l14-crashes.json` | 12 screens, 3 quiz | `rm-extend` | series (monthly spread; cumulative with `drawdown: true`), bars (legs in the three rebound months, frames), scatter (loser − winner beta against trailing market, fit), table (volatility scaling) | `worst_months`, `loser_winner_beta`, `vol_scaled` |
| `l15-replication-note.json` | 11 screens, 3 quiz | `rm-extend`, `rm-paper` | table (results), console (draft note, tap the overclaim), `order` derive with a `same` pair | `survival_ratio` |
| `review-3.json` | 9 items, difficulty 2 to 4, `pass: 0.8` | all five lessons, skills tagged | | none |
| `homework-3.json` | 6 items, difficulty 3 to 5 (two at 5) | all five skills | | `replicate(seed)` (5, `performance: "code"`, statsmodels, `budget: 30000`; l15's objective starts "Write"), `net_table` (4); `order` derivation of (K − j)/K with a flawed-line distractor (4); `longform` (5, 10-point rubric, full model note) |

Later papers named once each where used: Fama and French (1996) and Carhart (1997) in l12; McLean and Pontiff (2016) and Jegadeesh and Titman (2001) in l13; Daniel and Moskowitz (2016) in l14; Hong, Lim and Stein (2000) and Lesmond, Schill and Zhou (2004) in l15. Edge cases: K = 1 (l11 quiz), a factor built from the same shares (l12), the effect in sub-periods (l13), a long-only winners book (l14 quiz), a result that did not survive (l15).

## Gates (SESSION PROTOCOL 4)

1. Validator, from `app/`: `0 errors`; four "ladder reuses the previous canvas kind" warnings in my files (l13 screens 4 and 5, l14 screens 3 and 4), kept on purpose.
2. Voice scan on the seven level 3 files: 0 sentences over 20 words, 0 explanations over three sentences. (Course-folder residue is level 1's, as the level 2 report says.)
3. `docs/reports/momentum-rep-L3-numbers.py` (needs NumPy and statsmodels): exits 0, 174 of 174 `expect` checks, every two-route agreement, 13 code widgets (solutions pass in CPython, starters fail).
4. Playthrough with `--local-cdn`: every lesson, `review-3` and `homework-3` pass with `--mobile` (l11 15 checks in 37.4 s, l12 15 in 41.2 s, l13 15, l14 15, l15 all passed; review 9 of 9; homework 6 of 6, 30 of 30 marks, the performance starter fails, the longform marked by the button) and without it (see the hand-back line). **statsmodels load time:** the first statsmodels screen of a lesson takes the lesson to 37 to 41 s in total against about 30 s for a NumPy-only lesson, so the first statsmodels import costs about 10 s from the local CDN; every statsmodels `how` says 20 to 40 s for a first load over the network.

Screens inspected at 440 and 1280. Fixes made after my own read: l13's explore first keyed "no post-1990 window reaches the old level", which was false (the window ending at month 359 averages 1.14%); it now keys yes, briefly, and the numbers script asserts it. Rule 581 (from the main session): every numeric `wrong` value in levels 2 and 3 is outside its answer band (one review-2 slip removed), and unqualified general claims in explanations now carry their conditions. Other fixes: the rolling-beta axis clipped the post-crash dip (now from −1.5), and l13's text probability now matches the distribution label (5.5%, computed from the same rounded inputs).

## Numbers and how each was computed twice

Route 1: the lessons' form (statsmodels HAC and OLS; loop composites). Route 2 (numbers script): Newey-West and OLS by hand in NumPy; overlapping returns from the cohort-by-month matrix `W @ r.T`; rolling betas by `polyfit`; drawdown by a loop; legs rebuilt separately and checked to sum to the spread. Route 3: Pyodide in the playthrough for every code test.

| Number | Value | Where |
|---|---|---|
| Summed 6-month cohort returns, 6/6 | 289, mean 5.72%, naive t 5.58, Newey-West (5) t 3.59, lag-0 t 5.59 | l11 |
| Their autocorrelations, lags 1 to 8 | 0.62, 0.30, 0.05, −0.06, −0.09, −0.03, −0.03, −0.06 | l11 explore |
| Composite: plain t, HAC lag 0, lag 5 | 2.7412, 2.7459, 2.9925; autocorrelations at lags 2 to 5 −0.050, −0.072, −0.041, −0.033 | l11 |
| Naive t / √6 | 2.28 | l11 |
| Alpha on market and four factors | 0.0102 (1.02%), t 2.79, R² 0.023; Newey-West t 2.97 | l12, l15 |
| Market alone | alpha 1.07% (t 2.95), beta −0.093 (t −1.15), R² 0.0046 | l12 hook |
| Spread on market, months 420 to 443 / all 468 | slope −0.72 / −0.07; rolling 24-month beta −0.72 ending month 443, −0.13 ending 408 | l12 |
| Extension 6/6 skip: before 1990, after | 1.04% (t 2.95), 0.27% (t 0.57), 288 and 180 months; decline 74%; t of the difference −1.28; se after 0.48% | l13, l15 |
| Distribution label | P(mean ≤ 0.27 | true 1.04) = 5.5%; 0.27% is 0.5 se from 0.5% | l13 |
| Four sub-periods | 1.37%, 1.02%, 0.72%, −0.13%; after 1990 without the crash 0.58%; 40-year mean 0.74% | l13 |
| Best 60-month window wholly after 1990 | 1.14%, ending month 359 (months 300 to 359); 1 of 121 such windows reaches 1.04% | l13 explore |
| Crash months 420 to 422 | −25.4%, −13.3%, −15.2%; losers +25.9%, +12.4%, +10.9%; winners +0.5%, −0.9%, −4.3% | l14 |
| Five worst months | 420, 136, 220, 422, 253 | l14 code |
| Loser − winner beta | +0.45 at month 420, −0.53 at month 300; correlation with the past 12-month market −0.53 over 432 formation months | l14 |
| Maximum drawdown | 63.5%, month 333 to 443 (£10m to £3.6m) | l14 |
| Volatility scaling (6 months, 5% target, cap 1) | scales 0.77, 0.38, 0.35; crash months −19.7%, −5.0%, −5.4%; mean 0.68% → 0.61%; with cap 2 the worst month is −30.6% (month 220) | l14 |
| Winner-only book beta | 1.00 | l14 quiz |
| Survival | 0.27 / 1.04 ≈ 26%; net of 25 bp a side 0.82% a month; after 1990 net 0.13% (assuming 0.577 turnover) | l15, homework |

All the course-context reference values for this level reproduce to the places stated (the composite's 2.7412, 2.7459, 2.9925 and its four autocorrelations; alpha 0.0102, t 2.79, R² 0.023; 1.04%, 0.27%, t 0.57; −25.4%, −13.3%, −15.2%; 0.82%), except the overlapping-returns figures, below.

## Departures from the brief

- Overlapping cohort returns: the brief's mean 0.0569, naive t 5.53 and Newey-West t 3.56 do not reproduce. With the brief's own definition for `overlap_returns` (each cohort's summed 6-month return) I get 0.0572, 5.58 and 3.59; with compounded buy-and-hold returns 0.0598, 5.50 and 3.52. The lessons use the summed definition and its values.
- The cohort series' autocorrelation falls to about 0 by lag 3, not lag 6 as the brief expects, because neighbouring cohorts hold different shares. l11 teaches the (K − j)/K pattern as the independent-returns theory and says ours decays faster.
- Volatility scaling uses the trailing 6-month **sd** (target 5%, cap 1), not the inverse variance; with leverage allowed (cap 2) the worst month becomes −30.6%, which the lesson states.
- The three crash months are not the three worst: month 421 (−13.3%) is eighth; the worst five are 420, 136, 220, 422 and 253.
- `loser_winner_beta` takes `skip=1` by default, to match the extension's 6/6 skip strategy.
- `survival_ratio` raises `ValueError` when the in-sample mean is not positive and says "None of the effect survived" when the ratio is not positive.

## Proposed course.json change

None.

## For the topic-3.1 exam (ideas from levels 2 and 3)

1. Composite weight as the average of K cohort weights (4/300), and T − J − skip − K + 1 months against (T − J − skip) // K blocks.
2. The skip swaps holding month 1 (reversal) for month K + 1; it helps short K most.
3. Gaps to the paper judged in standard errors with a rule fixed first; seed-to-seed spread ≈ the standard error.
4. Overlapping K-month sums: autocorrelation (K − j)/K, naive t too large by up to √K, Newey-West with L = K − 1; lag 0 corrects nothing.
5. Alpha on factors with a low R²: unexplained variance is still risk.
6. Out-of-sample split at a date fixed in advance, with the index offset (300 − 12 = 288) and the t of the difference.
7. Crash mechanism: (β_W − β_L) m_t after a bear market; −0.9 × 12% ≈ −10.8%.
8. Survival ratio and an honest survival sentence.

## Backlog

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (momentum-rep level 3):".

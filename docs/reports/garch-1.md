# Report: garch level 1 (Clustering)

## Files written

All in `app/content/courses/garch/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l1-calm-and-storms.json` | 12 screens, 4 quiz | `block_sds`, `rolling_vol` (pandas), `vol_range` | gv-clustering |
| `l2-squared-returns.json` | 12 screens, 4 quiz | `squared_acf` (statsmodels `acf`), `arch_effects` (`acorr_ljungbox`), `arch_lm` by hand (NumPy + SciPy, matches `het_arch`) | gv-clustering |
| `l3-fat-tails.json` | 12 screens, 4 quiz | `excess_kurtosis` (matches `scipy.stats.kurtosis` to 9 places), `tail_count` + `normal_tail_expected` | gv-clustering |
| `l4-realised-vol.json` | 12 screens, 4 quiz | `annualise` + `realised_vol`, `best_window` | gv-clustering, gv-forecast |
| `review-1.json` | 10 items, difficulty 2 to 4, at least two per lesson, interleaved | | |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5) | `rolling_vol` with `periods_per_year` and `zero_mean` (4), `tail_report` (QQ correlation, 3-sd count, ratio to normal; 4), `stylised_facts` (5) | |

Homework also has an `order` item (61 closes to an annualised 60-day volatility), two numerics (weekly sd from a 20% annual limit; the √(3/5) scaling of a t5), a choice (ARCH-LM that does not reject), and a `longform` (the colleague who reads a flat ACF as independence and uses a 250-day sd) with a 10-point rubric and a full model answer.

Lesson shapes (hook, explore, name, ladder, trap, edge case, generalise or derive, transfer):

- l1: tap the real share on a stacked `pair` (`tap: "sides"`: course path against the seed-8 normal); 20-day vol of both on one `series` with a `revealAt` control (5.8% to 49.2% against 8.3% to 23.8%); name clustering on the five largest days (all between days 1,402 and 1,468, three up, two down, 1,455 and 1,456 back to back); `block_sds` code (2.56 against 1.15); sign against size table (next day beyond 2 sd: 27.8% after a big day against 4.5%; next day up 53.1% after big rises, 48.8% after big falls); Calm/Storm `walk` `model: "markov"` (P = [[0.98, 0.02], [0.05, 0.95]], mean storm 20 days; GARCH has no regimes, said in the prose); trap on the ACF of returns (lag 3 at 0.0531 pokes out; Ljung-Box p = 0.27); `rolling_vol` code; edge case series C with one variance break (blocks 0.67% to 0.74%, then 1.29% to 1.32%); `vol_range` code; generalise (conditional probabilities of size and sign); transfer (VIX in 2008 and 2020 qualitatively; on day 1,404 the 250-day vol reads 19.3% against a true 43.6%).
- l2: predict r²'s lag-1 ACF (0.3596); scatter of |r_t| on |r_{t-1}| with a slope control (fit 0.257; signed returns 0.021); grouped correlograms of r, |r|, r² (multi); `squared_acf` code; Ljung-Box table (r: Q = 12.242, p = 0.2692; r²: Q = 1451.43, p below 1e-300) named McLeod and Li; `arch_effects` code (A: p 0.7528 and 0.0772, no ARCH at 5%, yes at 10%); trap (white noise read as independence, on a `console`); ARCH-LM by hand (B: LM 463.61, p 2.6e-93; A: 17.13, p 0.0716); |r| against r² at lags 1, 10, 50 (0.1502 against 0.1221 at lag 50) and A's tests; edge case one −10% day in A (r² lag 1 −0.0126, Ljung-Box p = 0.99, sd 1.015% to 1.039%, excess kurtosis −0.05 to 3.92); generalise (Ljung-Box formula, independence implies, not the reverse); transfer (AR(1) residual check list before a VaR; the market makers' wider quotes).
- l3: expected normal days beyond 3 sds (5.40; B had 28); log-scale histogram with a normal `curves` overlay reading `w` and a bin-width control; kurtosis by hand in a `table` widget (six 0s and ±2: κ = 4); `excess_kurtosis` code; QQ plot on `scatter` (200 points with the 25 most extreme at each end kept; tap 3 of 32 that leave the line; correlation 0.9830, A 0.9998); Student's t with a ν control and a same-variance normal overlay (ν = 6 gives B's raw 6.01); trap on the `fisher` flag; normal shocks fatten tails (theory 1.4328; dropping the 1, 2, 3, 5, 10 largest days: 2.71, 2.50, 2.34, 2.02, 1.42); edge case 40 blocks of 50 days (−0.79 to 1.66, 29 below 0; a t4 never settles: raw 9.4, 15.2, 12.2, 11.1 after 1,000 to 100,000 draws, seed 12); tail-count code; generalise (shift and scale invariance); transfer (5-sigma: 5.733e-7 a day, about 6,920 trading years; the smile from `trees` l11).
- l4: four analysts (11.44%, 15.11%, 12.18%, 13.90%); rolling vol over days 1,200 to 1,699 with a window control and the true σ dashed; name and annualise (0.9516% daily to 15.11%); zero-mean against sample sd (5 days: 11.44% against 17.43%, because the 5-day mean is −0.89% a day; 60 and 250 days agree to 0.1 point); standard error table (31.6%, 15.8%, 4.5%); `realised_vol` code; error against window on a `plane` (RMSE in (% a day)²: 5 days 1.017, 20 days 0.435, 250 days 1.047; tap 20); `best_window` code (20 among nine windows, 22 over 5 to 250, 250 for the independent series); trap on annualising (15.87% against 19.10%, 3.98%, 252%); edge case the ghost (A with −10% on day 1,000: 16.7% to 38.4%, back to 12.4% on day 1,020); derive √252 as an `order` (uncorrelated, not independent, is what it needs); transfer (realised 16% against implied 24.1% for the `trees` l11 call at £12.00; the variance risk premium).

## Validator

`node app/tools/validate.mjs`: 0 errors. One run in between showed 3 errors in another course's files being written at the same time; the next run was clean. The garch files have only warnings: a ladder screen that changes canvas kind (five) and point hints without a highlight (six), all deliberate.

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set garch/review-1 --set garch/homework-1 --local-cdn .../scratchpad/pkgs --shots .../garch-1/shots --mobile`, final run after the last edit, no console errors:

| File | Result |
|---|---|
| l1-calm-and-storms | 16 checks, quiz 4/4 |
| l2-squared-returns | 16 checks, quiz 4/4 |
| l3-fat-tails | 16 checks, quiz 4/4 |
| l4-realised-vol | 16 checks, quiz 4/4 |
| review-1 | 10 of 10 recorded |
| homework-1 | 8 of 8 right, 36 of 36 marks |

I looked at the screenshots at 1280 and 390 px. Fixed along the way: controls placed on the screen instead of the canvas (the explore was not interactive); KaTeX in the grouped-bars legend showing as raw text (now Unicode labels); a hyphen where a minus sign belonged. The five crowded marker labels on l1's "five largest days" chart stack and stay legible.

## Numbers and their sources

Every number was computed in CPython (NumPy 2.5.3, SciPy 1.18.1, statsmodels 0.15.0, pandas 3.0.5) by the builders and fact scripts in the scratchpad. Every code test's expected value comes from the reference solution in CPython (`checkcode.py`: every solution passes, no starter passes), and the browser playthrough then ran every test in Pyodide 0.27.7 (NumPy 2.0.2, SciPy 1.14.1, statsmodels 0.14.4, pandas 2.2.3). All passed, so the two platforms agree on every tested value. The course-context facts were reproduced exactly: first five returns, sample sd 0.010289, excess kurtosis 3.0135, 28 days beyond 3 sds against 5.40, ACFs of r, r² and |r|, both Ljung-Box results, 20-day vol range (0.058, 0.4921) with its peak on day 1,409, and the four windows (0.1144, 0.1511, 0.1218, 0.1390).

Values I computed that the brief left open:
- Normal contrast (seed 8): 20-day vol 8.29% to 23.81%; block sds 0.945% to 1.085% (ratio 1.15, B's is 2.56); Ljung-Box p 0.7528 on r and 0.0772 on r²; het_arch(10) 17.126, p 0.0716; QQ correlation 0.9998. Its |r| Ljung-Box gives p = 0.0148, a 5% false positive, so the lessons report only the r and r² tests for it.
- het_arch on B: 463.605 (10 lags), 258.483 (1 lag); my hand `arch_lm` agrees to 9 significant figures.
- Up share after a rise beyond 2 sd: 53.1% (49 days); after a fall: 48.8% (41); any day 46.4%. Next day beyond 2 sd: 27.8% after any big day, 4.5% overall; A: 5.2% against 4.8%.
- Variance-break series C (seed 9, sd 0.7% then 1.3%): 20-day vol 5.38% to 30.04%; its r² ACF over the whole series is 0.1356 at lag 1, but inside each half Ljung-Box on r² does not reject (p 0.063 and 0.320). B rejects in both halves (p 0.0028 and 2.6e-131). This gives the homework's `stylised_facts` verdict: 'clustered' needs a rejection on the whole series and on both halves, 'break' a rejection on the whole series only. Seed 11 of the same GARCH is also 'clustered'.
- Kurtosis: dropping B's largest 1, 2, 3, 5, 10 days gives 2.706, 2.503, 2.338, 2.023, 1.418; 50-day blocks run −0.794 to 1.657; `bias=False` gives 3.024; GARCH seed 11 has excess kurtosis 0.697 (another sign that the sample statistic is noisy).
- Best window (estimate for day t from days t − w to t − 1, sample variance, scored on days max(windows) to 1,999): 20 among [5, 10, 20, 40, 60, 90, 120, 180, 250]; 22 over 5 to 250; 30 between 30 and 40; 20 on the first 600 days.
- Ghost: 20-day vol 16.73% on day 999, 38.42% on day 1,000, 38.27% on day 1,019, 12.44% on day 1,020.
- Storm (true annual vol above 25%) from day 1,392; on day 1,404 the true vol is 43.62%, yesterday's 20-day 45.55%, 60-day 31.34%, 250-day 19.35%.

## Deviations from the brief, stated honestly

- l1's transfer: the brief asked why yesterday's 20-day vol lags a storm's first days. On this path it does not lag much: the 20-day figure tracks the true GARCH vol within 1 to 2 points as the storm starts, because GARCH's own variance is a weighted average of recent squares. The transfer therefore shows the 250-day figure lagging (19.3% against 43.6%) and mentions the lag on the way out.
- l4's zero-mean point: "nearly equal for daily data" holds at 20, 60 and 250 days. At 5 days the two differ by half (11.44% against 17.43%), and l4 teaches that as the reason desks drop the mean.
- l3's edge case: 50-day block kurtosis is not "wildly unstable" in both directions. All 40 blocks fall below the full-sample 3.01, because inside 50 days σ_t barely moves. The screen teaches that the fat tails come from mixing calm and storm.
- `qq_correlation` is a homework code item (`tail_report`), not an l3 screen, to keep l3 at 12 screens. The QQ correlation is still reported on l3's QQ screen.
- The ARCH-LM screen of l2 is a code screen (`arch_lm` by hand) and reports `het_arch`'s statistic and p-value in its table.

## Conventions

- Data: `r, s2 = simulate_garch(2e-6, 0.08, 0.90, 2000, 7)` (the brief's function verbatim in every code prelude), described as share B; contrast `iid = 0.01 * np.random.default_rng(8).standard_normal(2000)`, series A. Planted series: C, the variance break `np.where(np.arange(2000) < 1000, 0.007, 0.013) * default_rng(9).standard_normal(2000)` (l1, review, homework); A with day 1,000 set to −10% (l2 and l4 edge cases); `r11` from seed 11 (homework).
- Returns are decimals in code and charts (series `format: "pct"`), and per cent in prose. Days are indexed from 0. Rolling windows are trailing: the value on day t uses days t − w + 1 to t. The forecast-style estimate in `best_window` uses days up to t − 1.
- Sample sd with ddof 1 for realised vol and tail counts; population moments for kurtosis (matches `scipy.stats.kurtosis`, default `bias=True`). Every kurtosis is labelled raw or excess on its screen, and `fisher=True` is named as scipy's default.
- Annualising by √252, and √52 for weeks. Correlogram band ±1.96/√2000 = ±0.0438. Money in £.

## Load times

Measured under Node with the local wheels (`pyrun.mjs`): NumPy and pandas about 36 s from cold (Pyodide start included); SciPy about 5 s more; statsmodels about 17 s more on top of NumPy and pandas. In the browser playthrough, l2 (three statsmodels screens) took 47 to 71 s against 30 to 36 s for l3 and l4. Every statsmodels `how` says "20 to 40 seconds"; SciPy screens say "a few seconds".

## course.json

No change needed.

## Engine and canvas limitations

Seven bullets in `docs/BACKLOG-INBOX.md` under "Raised later (garch level 1):".

Scratch files: `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/garch-1/` (`data.py`, `common.py`, `build_l1.py` to `build_l4.py`, `build_sets.py`, `facts*.py`, `checkcode.py`, `code_*.json`, `shots/`, `sheet_*.png`).

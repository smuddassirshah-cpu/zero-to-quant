# Topic 2.3 exam: projects (backtest, alpha, opt-dash)

File: `app/content/exams/topic-2.3.json` (id `topic-2.3`, 90 minutes, pass 0.7). Minutes follow `examMinutes` in `learn.js`: topic 2.3 is 400 h, over 150 h, so 90.
Generator and checks: `scratchpad/exam-2.3/`. `gen.py` builds the file from `items1.py` to `items4.py` (non-code items) and `code_b6.py`, `code_b8.py`, `code_a15.py`, `code_a20.py`, `code_o5.py`, `code_o8.py` (each holds prelude, starter, solution, cases and wrong versions). `codekit.py` is the mini grader, `verify_*.py` run each code item, `ref_*.py` and `ref_rest.py` are independent second implementations, `final_check.py` grades the finished JSON, `calc*.py` recompute the numbers, `lint.py` checks the voice, `pyrun.mjs` runs any script in Pyodide 0.27.7.

## Exit line tested

"Every project ships with a README, tests and a one-page results note that includes what failed. Treat any simple rule that backtests to a Sharpe above 2 as a bug until you have proved otherwise." Items 21 (a net Sharpe above 3 with fills at the signal close and no look-ahead check), 22 (finding where an engine starts to peek) and 30 (the longform: review a results note that reports a best-of-60 Sharpe of 2.4, a spent held-out year and "what failed: nothing") test it directly. The reports in all three courses (Sharpe, Calmar, drawdown; IC, turnover, Sharpe after costs; pricers, IV surface, Greeks) are each tested by at least two items.

## Shape

30 items, interleaved by course within each difficulty band.

| Difficulty | Items | Share | Ramp |
|---|---|---|---|
| 2 | 6 | 20% | 20% |
| 3 | 15 | 50% | 50% |
| 4 | 6 | 20% | 20% |
| 5 | 3 | 10% | 10% |

Widgets: 8 numeric, 6 code (Python), 5 tap-regions (table rows or cells), 4 table, 3 choice (two with a console), 1 multi, 1 order, 1 drag-point (plane), 1 longform. Canvases: table 9, console 3, bars 1, series 1, plane 1.

| # | id | d | skills | widget / canvas |
|---|---|---|---|---|
| 1 | e-visible-rows | 2 | bt-design | tap rows (table) |
| 2 | e-universe-date | 2 | al-universe | tap rows (table) |
| 3 | e-clean-tap | 2 | od-data | tap rows (table) |
| 4 | e-ticket-cost | 2 | bt-execution | numeric |
| 5 | e-mom-window | 2 | al-signal | numeric, bars |
| 6 | e-newton-step | 2 | od-iv | numeric |
| 7 | e-bar-order | 3 | bt-design, bt-execution | order |
| 8 | e-split-div | 3 | al-universe | numeric |
| 9 | e-implied-q | 3 | od-data | numeric |
| 10 | e-impact-double | 3 | bt-execution | numeric |
| 11 | e-ic-tstat | 3 | al-ic | numeric |
| 12 | e-three-pricers | 3 | od-pricers | tap cells (table) |
| 13 | e-peek-lines | 3 | bt-bias | multi |
| 14 | e-rank-ic-hand | 3 | al-ic | numeric, table |
| 15 | e-code-forward-vols | 3 | od-surface | code |
| 16 | e-drawdown-calmar | 3 | bt-metrics | table, series |
| 17 | e-rank-weights | 3 | al-portfolio | table |
| 18 | e-explain-pnl | 3 | od-greeks | table |
| 19 | e-code-tear-line | 3 | bt-metrics, bt-execution | code |
| 20 | e-cost-drag | 3 | al-costs | table |
| 21 | e-too-good | 3 | bt-bias, bt-report | choice, console |
| 22 | e-code-first-leak | 4 | bt-bias | code |
| 23 | e-code-sector-z | 4 | al-signal | code |
| 24 | e-flat-vega | 4 | od-iv | choice, console |
| 25 | e-reversal-crossover | 4 | al-costs, al-portfolio | drag-point, plane |
| 26 | e-calendar-cells | 4 | od-surface | tap cells (table) |
| 27 | e-bump-size | 4 | od-greeks | choice, console |
| 28 | e-code-bermudan | 5 | od-pricers | code |
| 29 | e-code-net-book | 5 | al-portfolio, al-costs | code |
| 30 | e-results-note | 5 | bt-report, bt-bias | longform, 10-point rubric, full model answer |

Skills: all 15 covered, none fewer than 2 items: bt-design 2, bt-execution 4, bt-bias 4, bt-metrics 2, bt-report 2, al-universe 2, al-signal 2, al-ic 2, al-portfolio 3, al-costs 3, od-data 2, od-pricers 2, od-iv 2, od-greeks 2, od-surface 2. The `skills` map is the union of the three `course.json` maps.

Time-ordered validation only: nothing in the exam is shuffled; the held-out year in item 30 is the last year and the look-ahead items cut by row position.

## Code items (Pyodide 0.27.7, NumPy 2.0.2, pandas 2.2.3, node and the browser playthrough; CPython NumPy 2.5.3, pandas 3.0.5)

Data are generated in code with seeds: `make_bars` (verbatim from the backtest brief, seed 2301, 400 rows) for item 22; `default_rng` frames (seeds 3, 5, 9, 11, 21, 22, 31, 32) for items 19, 23 and 29; hand trees and lists for items 15 and 28.

| item | tests | solution | starter passes | wrong versions (each fails at least one test) |
|---|---|---|---|---|
| e-code-first-leak | 8 | 8/8 | 4 of 8 (the `None` cases) | last row only (test 5, a gap leak that the last row hides), unsorted cuts (2, 3), `iloc[:cut+1]` (1), returns last leaking cut, returns a bool |
| e-code-tear-line | 8 | 8/8 | 0 of 8 | ddof 0, turnover over n − 1, drawdown from the first value, CAGR exponent over n, global-range drawdown, Calmar 0 instead of inf, one-sided turnover |
| e-code-sector-z | 7 | 7/7 | 2 of 7 | whole-universe z, ddof 0, z over time, `min_names` ignored, constant sector, demean only |
| e-code-net-book | 9 | 9/9 | 0 of 9 | no lag, cost every row, cost on the rebalance row, NaN signal not zeroed, one-sided cost, `min_names` ignored, warm-up rows kept, exits not charged |
| e-code-bermudan | 11 | 11/11 | 4 of 11 (European-price cases) | exercise at every step, step off by one, step 0 skipped, r in p instead of r − q, exercise value discounted, European only |
| e-code-forward-vols | 10 | 10/10 | 2 of 10 | raises on a fall, vol average, no division by the gap, vol difference, no input checks, `<=` for equal variance |

Float cases carry `tol` of 2e-6 absolute and 1e-6 relative, with expected values rounded to 6 places in the call. Second methods: `tear_line` against a pure-Python loop (30 random series), `sector_zscore` against a nested loop (15 frames with ties and NaN), `net_book` against a list-based simulation (20 random panels with NaN, ties and deaths, plus the hand case checked by arithmetic: first row −0.005 gross, −0.006 net), `bermudan_put` against an explicit-node dictionary tree (40 random parameter sets, max difference 4e-14) and against Black-Scholes (European 500 steps 3.9057 against 3.9043), `forward_vols` against a NumPy formula, `first_leak` against a brute-force scan over every cut 1 to 400 (leak starts at cut 1, 3, 301 and 119 for the peek, scaled, late and bfill engines; honest and ffill never). Every check gave identical output in CPython and Pyodide.

## Numbers computed twice

Each answer was computed in `calc*.py` in CPython and again in Pyodide (identical to every digit shown), and checked by a second method.

- Ticket (3): 3,000 × £0.005 = £15.00; 2 bp of £127,500 = £25.50; total £40.50.
- Impact (10): 0.015 × √(40,000 / 1,600,000) = 23.717 bp, £5,692.10; at 80,000 shares 33.541 bp on £4.8m = £16,099.69; ratio 2.8284; linear wrong value £11,384.20, old-notional wrong value £8,049.84.
- Drawdown (16): `[100 … 118.4]` by running peak and by an explicit loop: −10.0917% (109 to 98); CAGR 18.4%; Calmar 1.8233; global range 19.01%, wrong Calmar 0.968. `tear_line` returns the same.
- Split and dividend (8): 2 × (123 + 1.5) / 240 − 1 = 3.75%; raw −48.75%; split only 2.5%; dividend per old share 3.125%.
- Momentum (5): months Jan to Nov sum to 15; all twelve 10; December alone −5; dropping January 8.
- IC t statistic (11): 0.036 / (0.081 / 6) = 2.667; IR 0.444; annualised 1.540.
- Rank IC (14): signal ranks 5, 2, 6, 3, 1, 4, return ranks 2, 3, 6, 5, 1, 4, Σd² = 14, IC 0.6 (`spearmanr` 0.6, Pearson of ranks 0.6); raw Pearson 0.7627; n = 7 formula 0.75.
- Rank weights (17): centred ranks −3 to 3 over 12: ±0.25, ±0.1667, ±0.0833, 0.
- Cost drag (20): 4.5 × 14 bp = 63 bp; net 4.77%; Sharpe 5.4 / 3.0 = 1.80 gross and 1.59 net; break-even 5.4% / 4.5 = 120 bp.
- Crossover (25): weekly = monthly at 4.0 bp (net 1.2); daily = weekly at 2.667; daily = monthly at 3.333.
- Newton step (6): price at 25% £12.3360 (shown 12.34), vega 37.842 (shown 37.8); 0.25 + 0.66 / 37.8 = 0.26746; true implied vol 0.267534 (brentq).
- Implied q (9): F = 100 + e^0.05 × 2.60 = 102.7333; q = 0.05 − ln 1.027333 = 2.3034%; without discounting 2.433%; without r −2.567%; linear 2.267%.
- Pricer grid (12): puts, S 100, r 5%, q 1%, σ 20%, T 0.5; BS, 500-step trees, 100,000 antithetic paths seed 1. Real values: tree differences under 0.003 at every strike, Monte Carlo within 1.9 standard errors, American premium 0.004 to 1.52. Three planted errors (tree EU at 110 +0.12, MC at 90 to −3.5 standard errors, American at 100 below European by 0.100); a script asserts the three rules flag exactly those cells.
- Greeks (18): S = K = 100, r 5%, σ 20%, T 0.5: delta 0.5977, gamma 0.0274, vega 0.2736 per point, theta −0.0222 a day (closed form and central bumps agree); terms 1.7931, 0.1233, 0.5472, −0.0222; explained 2.4414; repriced change +£2.4155; residual −0.0259.
- Newton on a flat vega (24): S 100, K 130, T 1/12, mid 0.03: σ 0.2000, 50.6361, −3.03e12; vega 5.9e-4 at the start; true implied vol 36.81%.
- Bump size (27): S 50, K 55, r 3%, σ 30%, T 0.25: closed-form gamma 0.046696; central bumps 0.046632, 0.046695, 0.046696, 0.046696, 0.046696, 0.042633, 0.000000 for h = 1 down to 1e-8 (identical in Pyodide). Best error 2.9e-10 at 1e-3.
- Calendar (26): total variance σ²T checked for all 15 adjacent pairs: only strike 80 at 6M (0.0225 to 0.0200), strike 90 at 3M (0.01763 to 0.01563) and strike 120 at 3M (0.01021 to 0.00810) fall.
- Longform (30): E[max of 60 standard normals] 2.3193 by integration and 2.3185 by simulation; 0.5 + 0.7 × 2.3193 = 2.1235, so 2.4 is 0.40 sd above; hit rate for a daily Sharpe of 2.4 is 0.5747; Sharpe standard error over a year 1.02.
- Universe (2): 4 May to 15 June 2021 is 31 weekdays, under 60.

## Fresh against the courses

Lessons teach the pieces; the items recombine them on new inputs: a cut-and-noise test over several cuts with a backfill leak the last row hides; a tear line that mixes Sharpe, drawdown, Calmar and the course's turnover convention; sector-neutral z-scores with a `min_names` rule; a rank book from signal to net return with a death and a gap; a CRR tree whose exercise steps are chosen (an extension of the American tree: the taught early-exercise check is applied only at listed steps); forward vols with a calendar flag.

## Validation and playthrough

- `node tools/validate.mjs`: 0 errors, no warning for this file; the manifest lists `exams/topic-2.3.json`. The ramp is 6 / 15 / 6 / 3.
- `playthrough.mjs --exam topic-2.3 --local-cdn <pkgs>`: 30 of 30, passed, desktop and `--mobile` (42 to 51 s with the six Python items).
- Copy lint (`lint.py`): no `!`, no em-dash, no sentence of 20 words or more (prose, options, feedback, explanations, rubric, model answer and `how` lines), no American spellings, at most three sentences in every explanation.
- Screenshots reviewed in `scratchpad/exam-2.3/shots`. Fixes made: a pricer table that ran off a phone (shorter headers, 3 decimals); axis title crossing a line on the plane item (`xAxis: "bottom"`) and curve labels moved to the left (`labelAt`); correct choice options no longer all first; starter comments moved above their lines so they do not scroll away; long bulleted rules in place of long sentences.

## Engine notes

Two backlog bullets under "Raised later (exam 2.3)": exact float `.equals` differs between pandas 3.0.5 (CPython) and 2.2.3 (Pyodide), and `order` feedback names only the first misplaced line. The table-cell `wrong[]` ids cannot be `byKey` keys (already in the inbox); items 14, 17, 18, 20 and 16 use `r{i}c{j}` keys. `how` text is not shown in the exam item screenshots I could crop, so the test lists there were linted from the JSON.

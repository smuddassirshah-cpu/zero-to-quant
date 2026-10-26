# Report: fin-ml level 3 (From prediction to profit)

## Files written

All in `app/content/courses/fin-ml/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l9-probability-to-position.json` | 12 screens, 4 quiz | `bet_size_from_prob`, `kelly_fraction`, `fractional_kelly` (one screen); `discretise`, `average_active_bets` (one screen) | fm-sizing |
| `l10-costs-eat-edges.json` | 12 screens, 4 quiz | `turnover` + `net_pnl`; `break_even_cost_bp` (bisection) + `smooth_positions` (no-trade band); `net_sharpe_by_cost` on the seeded market | fm-eval |
| `l11-deflated-sharpe.json` | 12 screens, 4 quiz | `sharpe_se` + `psr`; `expected_max_sharpe` + `dsr` | fm-eval |
| `l12-end-to-end.json` | 11 screens, 3 quiz | `trial_log_add` + `trial_count`; `study_pipeline(seed)` (scikit-learn, four gaps: purge, sizes, net P&L, DSR); `results_table` + `write_up_sections` | fm-eval, fm-labels, fm-features, fm-sizing |
| `review-3.json` | 9 items, difficulty 2 to 4, two or more per lesson | | |
| `homework-3.json` | 8 items, difficulty 3 to 5 (two at 5) | `simulate` (sizing-and-costs simulator, 4 rules, difficulty 4); `full_study(seed, cost_bp)` (whole study as one function: gross and net Sharpe, hit rate, base rate, effective n, trial count, DSR; difficulty 5) | |

Homework also has an `order` item (the steps from a walk-forward run to a DSR, with interchangeable pairs), three numeric items (three-quarter Kelly growth 0.94, impact capacity £142k, a turnover cost of £4,000) and a DSR item (Sharpe 1.8 over 4 years, best of 25: 0.945), plus a `longform` item (the one-page write-up of the seed-11 study with a weak result) with a 10-point rubric and full model answer showing the DSR calculation.

Lesson shapes.
- l9: hook (edge per £1 at p = 0.51 against 0.9: 40 times), explore on a `plane` with a slider on p (AFML curve; size 0.08 at 0.55), naming z and m = 2Φ(z) − 1 (AFML ch. 10 named; 0.34 at 0.7), Kelly with odds b on a slider (p = 0.4, b = 2: 0.1; links conditional "Bayes on a trading signal", where Kelly is taught), half Kelly keeps 75% of growth, flipping on noise (7 units traded on four near coin flips; rounding to 0.1 makes all 0), averaging overlapping bets in a `table` widget (0.6, 0.3, −0.2), trap (model says 0.6, truth 0.55: Kelly 0.2 is double Kelly, growth ≈ 0; link stat-learning "Probabilities you can trust"), Kelly derivation (`order`), two code screens, transfer (a desk's table at double Kelly: −1.5% a bet against +4.6%; the risk cap). Edge cases p = 0.5 (size 0, screen 3) and p = 1 (quiz: leak or overfit); side × size with a cap (quiz, links level 1 meta-labelling).
- l10: hook (seeded ±1 signal, hit rate exactly 52.5%, 927 units traded in 1,000 days: costs £927k against £731k gross), explore (net P&L against cost on a `plane`; break-even 7.9 bp), naming turnover and c* = gross per day / turnover (second signal: 12 bp), smoothing `table` widget (raw, EMA span 10, EMA + band 0.3: net −4.93%, +4.07%, +3.12% a year), grouped `bars` of five signals' net Sharpes at 5, 10, 20 bp (tap the survivors at 20 bp: EMA 30, EMA 100), capacity with the square-root impact rule (zero profit at £800k, peak £356k; links micro "Slippage and market impact"), trap (costs follow trades: same £400k gross, £50k against £900k), buy-and-hold edge case (one trade, £1,000), three code screens, transfer (desk rule: survive twice the expected cost; net Sharpe −0.12 at 16 bp). Wide-band and cost-above-every-edge cases are in the quiz.
- l11: hook (seeded `bars` sim, best of 10 noise strategies over 3 years reaches 1.5 in 4.6% of searches; links testing "Is this Sharpe ratio real?"), the Sharpe standard error and PSR (Bailey and López de Prado 2014, AFML ch. 14 named; 0.0365, PSR 0.995), SE `table` for normal, skewed, fat-tailed (0.1331, 0.1592, 0.1454), E[max] formula (0.91 a year for N = 10; compared with testing's seeded best of 100 over 5 years, 1.12 at seed 77, formula 1.13, gap about 1%), DSR against N on a `plane` with a slider (falls below 0.95 at N = 4; N = 1 is the PSR, 0.995), haircut `bars` for N = 1, 10, 100, 1,000 (noise explains 0%, 61%, 97%, 125% of 1.5), trap (3 reported against 60 logged trials: DSR 0.96 against 0.60; links validation "Trying too many models"), overlapping returns (effective n 76 of 756: SE 3.2 times larger; links level 1 "Overlapping labels"), two code screens, transfer (Sharpe 2.1 over 2 years, best of 40, skew −0.5, kurtosis 5: DSR 0.772). Short-record and negative-skew edge cases are in the quiz.
- l12: order the study checklist (11 stages), tap the stage where look-ahead hides on a `graph` of the pipeline (features), the trial log in code, the small complete run (`study_pipeline(7)`), the results `table` filled from the run's output, the write-up helpers in code, trap (starting with the model: 58% means nothing without the base rate), edge case (an honest "no edge" is a valid deliverable), drafting "what failed" (a `multi` against the rubric), transfer (which of three research notes can be acted on), closing (the exit line is met when this plan is run on real data in the backtest and alpha projects; this course's data are synthetic). Too-short-data edge case in the quiz.

£ is the only currency. Every `how` on a scikit-learn screen says the first load takes 10 to 30 seconds; the two study screens carry a `budget` (30 s and 60 s) and memoise each seed's run in the `postlude` so every test reads one run.

## Validator

`node app/tools/validate.mjs`: 0 errors overall. One warning in my files: `l12-end-to-end` screen 0 (the `order` hook) has no canvas; a canvas there would give away the order.

## Playthrough

`node app/tools/playthrough.mjs --lesson ... --set fin-ml/review-3 --set fin-ml/homework-3 --local-cdn <scratchpad>/pkgs`, all passed:

- l9-probability-to-position: 16 checks, quiz 4/4
- l10-costs-eat-edges: 16 checks, quiz 4/4
- l11-deflated-sharpe: 15 checks, quiz 4/4
- l12-end-to-end: 14 checks, quiz 3/3 (Pyodide and scikit-learn loaded)
- review-3: 9 of 9; homework-3: 8 of 8, 37 of 37 marks

Screenshots of every screen are in the scratchpad folder `fin-ml-3` (`shots9` to `shots12`, `shotsets`) and were reviewed; fixed after review: overlapping pipeline graph labels (now 3 per row), an empty bars chart (replaced by SE curves), a doubled £ placeholder, a too-wide summary formula, the left-axis on the SE plane.

## Proposed change to course.json

None.

## Dataset generators and key numbers

- l10 market (pure Python `random.Random(160)`, shipped in the preludes): 1,000 days, drift μ AR(1) with φ = 0.97 and sd 0.12%, return noise 1%, forecast noise 0.6%. Signal = sign(forecast): hit rate 52.5% exactly, turnover 0.927, gross Sharpe 1.178, net 0.431 / −0.313 / −1.765 at 5 / 10 / 20 bp, break-even 7.89 bp. EMA spans 3, 10, 30, 100 give the five-signal bars. Homework `simulate` reuses it with probs = logistic(forecast / 0.004).
- l11: no data; worked example 1.5 a year over 756 days, V = 1/755. Hook sim: app RNG seed 11 (49 of 1,000 searches reach 1.5; exact 0.046).
- l12 / homework study (NumPy `default_rng(seed)`): 600 days, drift AR(1) φ = 0.97 sd 0.15%, noise 1%; features 5-day and 20-day log return and 5/20 vol ratio; triple-barrier ±3%, 10 days; walk-forward blocks of 90 from row 300 (271 test days), purge 10; scaled logistic (C = 1) against boosting (25 trees, depth 2); AFML sizes averaged over 10 open bets, rounded to 0.1; 5 bp a side; DSR with N = 2, V = 1/(n − 1), measured skew and kurtosis.
  - Seed 7 (lesson): model logistic, hit rate 0.5314, base rate 0.4908, gross Sharpe 0.3149, net Sharpe 0.2757, DSR 0.4082.
  - Seed 11 (homework, longform): hit 0.5683, base 0.5277, gross 0.8204, net 0.7631 / 0.7058 / 0.5911 at 5 / 10 / 20 bp, DSR 0.6058 at 5 bp, effective n 28.0, skew −0.17, kurtosis 8.56. Seed 12 at 0 bp: boosting, net = gross 0.4949.
  - CPython (scikit-learn 1.6.1) and Pyodide 0.27.7 gave identical values to 4 places; a run takes 1 to 3 s in Pyodide.

Every stated number was computed by the generator scripts in the scratchpad (`lib.py`, `gen10.py`, `pipe.py`, `pipe2.py`, `num10.py`, `num11.py`, `numhw.py`) and checked a second way: closed forms against bisection or simulation (break-even, E[max] against a 10,000-search seeded simulation), canvas curve formulas against the library, and the code screens' expected values by Pyodide in the playthrough.

## Engine or canvas limitations

Appended to `docs/BACKLOG-INBOX.md` under "Raised later (fin-ml level 3):" (7 bullets): longform not allowed in lessons; series values cannot follow a control; no log x scale on plane; no Φ⁻¹ in curve formulas and derive; table widget cells cannot bind to bars or plane values; per-case tolerance for Python code tests; graph rect nodes overlapping at 4 per row.

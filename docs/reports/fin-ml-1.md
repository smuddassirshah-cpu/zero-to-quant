# Report: fin-ml level 1 (Labels)

## Files written

All in `app/content/courses/fin-ml/`:

| File | Screens or items | Code screens | Skills |
|---|---|---|---|
| `l1-fixed-horizon.json` | 12 screens, 4 quiz | `fixed_horizon_label` (alignment: last h rows dropped; h = 1 and an exact zero return), `dead_zone_label` (volatility-scaled dead zone on log returns), `label_balance` | fm-labels, fm-eval |
| `l2-triple-barrier.json` | 11 screens, 4 quiz | `first_touch` (hand-made paths, exact touches, a path shorter than h), `triple_barrier_labels` (seeded series; one test calls it twice), `barrier_hit_shares` | fm-labels |
| `l3-meta-labelling.json` | 12 screens, 4 quiz | `primary_crossover_side`, `meta_labels`, `meta_precision_recall` (threshold 0 and a threshold that takes nothing), `fit_meta_model` (scikit-learn `LogisticRegression`, compared to 0.002 with `np.allclose`) | fm-labels, fm-eval |
| `l4-overlapping-labels.json` | 11 screens, 4 quiz | `concurrency`, `average_uniqueness`, `effective_n` + `weighted_hit_rate_se` | fm-labels, fm-eval |
| `review-1.json` | 8 items, difficulty 2 to 4, two per lesson | | |
| `homework-1.json` | 8 items, difficulty 3 to 5 | `label_spans` (4), `labelling_pipeline` (5: rolling vol, 5/20 crossover primary, triple-barrier outcomes, meta-labels, uniqueness weights; returns n, hit rate, weighted hit rate, effective n) | |

Homework also has an `order` item (the triple-barrier procedure for one entry), a uniqueness `table` item, three numeric/choice items (fixed per cent bar in typical moves, reading a low secondary probability, close-only labels) and a `longform` item (a colleague's 5-day labels, shuffled 10-fold CV, 56% hit rate, 54% base rate) with a 10-point rubric and a full model answer.

Lesson shapes.
- l1: tap the days labelled up on a 12-close path (days 7 to 11 have no label), tap the near-zero bars of a 746-label histogram (229 labels, 31%, from moves under 1%), the fixed-horizon label in code (linked to validation l7's `forward_label`), the path ignored (stopped out at −3.6%, labelled +1), calm and wild halves in a `table` widget (45.8% against 79.1% labelled ±1 at a fixed 1%), trap (a fixed per cent bar is 0.81 typical moves when calm, 0.22 when wild), a volatility-scaled dead zone on a `number-line`, the dead-zone label in code (65% and 56% ±1 per half), class balance, the base-rate trap (58.0% against 62.9% always +1; link to stat-learning l14), the rule in KaTeX with the zero-return edge case, transfer (55% hit rate from sub-0.1% moves: −0.095% a trade after a 0.10% cost; link to the costs lesson in level 3).
- l2: tap the first exit on a path with three barriers, explore with a slider on k (barriers and caption follow; time-out from k = 2.5), `first_touch` in code (AFML named), label shares against k on `bars` (time-outs pass half at k = 3.5), barrier prices in a `table` widget (calm and wild entries), trap (fixed ±2%: 66% time-outs calm, 0.5% wild; at ±2σ, 23% and 20%), closes only and the same-day double touch on a candle chart, two code screens (a 2-day limit with k = 3 gives 94% time-outs), the first-touch formula with asymmetric barriers, transfer (desk trades labelled as managed: the model learns which trades are worth entering).
- l3: tap the calls that paid (shorts win on the lower barrier), win rate by volatility bucket (0.74 and 0.69 calm, about 0.41 wild), the two-stage picture on a `graph` (AFML named), three code screens, F1 against threshold on a `plane` (tap 0.5; 0.6 discussed for a desk paying costs), trap (p = 0.72 on a short is the chance the call pays, not that the price rises), the logistic secondary in code (trained on the earlier block), threshold 0 gives the primary's base rate (40.6%), the rule in KaTeX with the always-right primary edge case, transfer (a discretionary trader's side, the model's size: 0.53% a kept call against 0.075%).
- l4: tap shared days on stacked label windows and an `array`, fill the four uniqueness weights in a `table` (0.75, 0.5, 0.6667, 1), two code screens (AFML named; return weighting in one sentence), effective n on `bars` (971 labels worth 156), trap (57.1% on 961 labels: 4.5 naive se, 1.7 honest se on n_eff = 140, on a `number-line`), the weighted se in code, weighted fitting and bootstrap (sequential bootstrap in one sentence), the one-long-label edge case (0.85), the rule in KaTeX with the no-overlap edge case, transfer (2,000 trades worth 180: t falls from 2.69 to 0.81).

Traps not on a trap screen are in the quizzes and review: shuffled rows (validation l5), a label horizon longer than the feature's step, training the secondary on the primary's training years, meta-labelling a primary with no edge, bootstrapping overlapping rows, purging with a fixed span instead of each label's first touch.

Every `how` on a scikit-learn screen says the first load takes 10 to 30 seconds. £ is the only currency.

## Conventions fixed

- Vertical barrier: a time-out is labelled **0** (three classes), with days held = h (or the last available close if the data end first).
- Same-day double touch: the course reads **closes only**, so it cannot happen; with highs and lows, the **stop wins** (−1), the cautious reading. In code the stop is tested before the profit barrier.
- Barriers: `P_t(1 ± kσ_t)` in simple returns, with `σ_t` the 20-day sample sd (ddof 1) of daily simple returns up to day t; no √h (AFML's way). Asymmetric widths allowed.
- Fixed-horizon dead zone: on daily log returns, 0 when |R| ≤ kσ√h; `np.sign` gives 0 to an exact zero return.
- A label's window is entry day to exit day, both included; concurrency and uniqueness use it.
- Crossover side: +1 when the fast mean of closes is strictly above the slow one, else −1.

## Dataset generators (all `np.random.default_rng(seed)`, in the preludes)

- `make_prices(n, seed, mu=0.0003, sigma=0.012)`: closes from 100, log returns mu + sigma·noise. Seed 21, 750 days in l1; 1,000 days in l2 and l4.
- `make_regime_prices(500, seed=11)`: daily vol 0.6% for 250 days, then 2.0%.
- `make_trend_prices(1500, seed=20)`: 60-day blocks, half trending (±0.3% a day, vol 0.8%), half chop (vol 1.6%); l3 and the homework. Seed 9 is a second test series.
- `rolling_vol`, `tb_events`, `meta_dataset(seed)` (two features: 20-day vol and the 10-day return in the side's direction) and `label_windows(seed, k, h)` are prelude helpers.

Every stated number was computed twice: by the builder (CPython, reference loops in `data.py`) and by an independent pandas/vectorised script (`check.py`, cumulative-sum concurrency), all matching. Every code test's expected value comes from the solution in CPython and was rerun in Pyodide 0.27.7 in Node (106 cases pass), then in the browser playthrough. The slowest test is under 1 s once packages are loaded; the scikit-learn screen's first run spends about 12 s importing.

## Validator

`node app/tools/validate.mjs`: 0 errors in fin-ml files (the 12 errors in the run were in `ensembles/l7-out-of-bag.json`, another agent's work, and later cleared: the last run reported 0 errors overall). No warnings on level 1 files.

## Playthrough

`node app/tools/playthrough.mjs --local-cdn .../scratchpad/pkgs --shots ... --mobile`, one run, no console errors:

| File | Result |
|---|---|
| l1-fixed-horizon | 16 checks, quiz 4/4 |
| l2-triple-barrier | 15 checks, quiz 4/4 |
| l3-meta-labelling | 16 checks, quiz 4/4 (replayed alone after a graph relayout: all passed) |
| l4-overlapping-labels | 15 checks, quiz 4/4 |
| review-1 | 8 of 8 recorded |
| homework-1 | 8 of 8 right, 35 of 35 marks |

Screenshots at 1280 and 390 px were checked; fixed along the way: a marker label colliding with the series end label (l2), a graph whose row of boxes overlapped on a phone (l3), crowded number-line points (l1).

## course.json

No change needed. l1, l3 and l4 also use `fm-eval` (they score a hit rate or a filter); each lesson's first objective is the course.json objective, with a second one added.

## Engine and canvas limitations

Five bullets, in `docs/BACKLOG-INBOX.md` under "Raised later (fin-ml level 1):".

Scratch files: `/tmp/claude-0/-home-user-zero-to-quant/d67d8e29-6ca4-501d-86ce-60a98b12eb8a/scratchpad/fin-ml-1/` (`build_l1.py` to `build_l4.py`, `build_sets.py`, `data.py`, `prel.py`, `check.py`, `checkcode.mjs`, `shots/`).
